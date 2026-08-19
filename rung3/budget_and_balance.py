"""
STEP A, extension. Two measurements that bound what can be claimed about the
result of the searched order. Zero LLM calls.

1. LABEL BUDGET. The Step A greedy search uses `true_action` over the 1000 train
   cases. That is full supervision. Here the search is repeated seeing labels
   for only a fraction, and it is always evaluated over the whole test set.

   The subsampling is SIMPLE RANDOM, not stratified: stratifying by class
   requires knowing the labels in advance, which is exactly the resource being
   rationed. Stratifying here would be cheating.

   At small fractions the variance of the draw dominates, so each
   (split, fraction) is repeated with several draws and the mean and standard
   deviation are reported.

2. BALANCED GREEDY. The Step A greedy search maximizes total correct decisions
   and therefore sacrifices the rare classes: on test it gave 0/21 on
   ACCOUNT_MANAGER and 0/3 on ONCALL_ESCALATION. The variant weights each case
   by 1/|class| on train, so that every class contributes equally to the
   objective. Both are reported, in aggregate and per class.
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from harness.hidden_policy import true_action
from harness.provenance import environment

from .order_search import (build_tables, ceiling, evaluate, load, split,
                           subsumption_below)

OUT = Path("results3")
FRACTIONS = [1.0, 0.25, 0.10, 0.05, 0.01]
N_DRAWS = 5
N_SPLITS = 5


def greedy(rules, pool, truth, action, label_idx, weights=None):
    """Decision-list greedy. `weights` None -> total correct decisions;
    dict class->weight -> weighted objective (class-balanced)."""
    ids = [r["rule_id"] for r in rules]
    pos = {i: k for k, i in enumerate(label_idx)}

    if weights is None:
        win = defaultdict(int)
        lose = defaultdict(int)
        for i in label_idx:
            bit = 1 << pos[i]
            for rid in pool[i]:
                if action[rid] == truth[i]:
                    win[rid] |= bit
                else:
                    lose[rid] |= bit
        remaining = (1 << len(label_idx)) - 1
        left = set(ids)
        order = []
        while left and remaining:
            best, bs = None, None
            for rid in sorted(left):     # FIX 2026-08-06, see order_search.py
                s = ((win[rid] & remaining).bit_count()
                     - (lose[rid] & remaining).bit_count())
                if bs is None or s > bs:
                    best, bs = rid, s
            order.append(best)
            left.discard(best)
            remaining &= ~(win[best] | lose[best])
        def prec(rid):
            w, l = win[rid].bit_count(), lose[rid].bit_count()
            return w / (w + l) if (w + l) else -1.0
    else:
        # per-class masks, so weighting does not require walking case by case
        classes = sorted({truth[i] for i in label_idx})
        win = {rid: {c: 0 for c in classes} for rid in ids}
        lose = {rid: {c: 0 for c in classes} for rid in ids}
        covered = defaultdict(int)
        for i in label_idx:
            bit, t = 1 << pos[i], truth[i]
            for rid in pool[i]:
                covered[rid] |= bit
                if action[rid] == t:
                    win[rid][t] |= bit
                else:
                    lose[rid][t] |= bit
        remaining = (1 << len(label_idx)) - 1
        left = set(ids)
        order = []
        while left and remaining:
            best, bs = None, None
            for rid in sorted(left):     # FIX 2026-08-06, see order_search.py
                s = 0.0
                for c in classes:
                    s += weights[c] * ((win[rid][c] & remaining).bit_count()
                                       - (lose[rid][c] & remaining).bit_count())
                if bs is None or s > bs:
                    best, bs = rid, s
            order.append(best)
            left.discard(best)
            remaining &= ~covered[best]
        def prec(rid):
            w = sum(win[rid][c].bit_count() for c in classes)
            l = sum(lose[rid][c].bit_count() for c in classes)
            return w / (w + l) if (w + l) else -1.0

    born = {r["rule_id"]: r["born_at"] for r in rules}
    order += sorted(left, key=lambda rid: (-prec(rid), born[rid]))
    return order


def per_class(order, pool, truth, action, idxs):
    rank = {rid: k for k, rid in enumerate(order)}
    tot, ok, ceil_c = Counter(), Counter(), Counter()
    for i in idxs:
        tot[truth[i]] += 1
        if any(action[r] == truth[i] for r in pool[i]):
            ceil_c[truth[i]] += 1
        if pool[i]:
            w = min(pool[i], key=lambda r: rank[r])
            if action[w] == truth[i]:
                ok[truth[i]] += 1
    recalls = [ok[c] / tot[c] for c in tot]
    return tot, ok, ceil_c, statistics.mean(recalls)


def main() -> int:
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)

    splits = [split(corpus, truth, seed=17 + s) for s in range(N_SPLITS)]

    # ------------------------------------------------------ 1. PRESUPUESTO
    print("=" * 78)
    print("1. PRESUPUESTO DE ETIQUETAS  (muestreo aleatorio simple del train)")
    print("=" * 78)
    print(f"  {'fraccion':>10}{'etiquetas':>11}{'test e2e':>12}{'desv':>9}"
          f"{'min':>9}{'max':>9}")
    budget_rows = []
    for frac in FRACTIONS:
        scores = []
        for s, (tr, te) in enumerate(splits):
            k = max(1, round(frac * len(tr)))
            for d in range(1 if frac == 1.0 else N_DRAWS):
                rng = random.Random(1000 * s + d)
                sub = sorted(rng.sample(tr, k)) if frac < 1.0 else tr
                o = greedy(rules, matched, truth, action, sub)
                scores.append(evaluate(o, matched, truth, action, te))
        budget_rows.append({
            "fraction": frac, "labels": max(1, round(frac * len(splits[0][0]))),
            "test_mean": round(statistics.mean(scores), 4),
            "test_sd": round(statistics.pstdev(scores), 4),
            "test_min": round(min(scores), 4), "test_max": round(max(scores), 4),
            "n_runs": len(scores),
        })
        r = budget_rows[-1]
        print(f"  {frac:>9.0%}{r['labels']:>11}{r['test_mean']:>12.4f}"
              f"{r['test_sd']:>9.4f}{r['test_min']:>9.4f}{r['test_max']:>9.4f}")

    tr0, te0 = splits[0]
    print(f"\n  referencias en test: aleatorio 0.4227 · born_at 0.5216 · "
          f"especificidad 0.1829 · techo {ceiling(matched, truth, action, te0):.4f}")

    # ------------------------------------------------------- 2. BALANCEADO
    print()
    print("=" * 78)
    print("2. VORAZ BALANCEADO POR CLASE  (supervision completa del train)")
    print("=" * 78)
    agg = {"total": [], "balanced": []}
    bal_acc = {"total": [], "balanced": []}
    last = {}
    for s, (tr, te) in enumerate(splits):
        counts = Counter(truth[i] for i in tr)
        w = {c: 1.0 / counts[c] for c in counts}
        o_tot = greedy(rules, matched, truth, action, tr)
        o_bal = greedy(rules, matched, truth, action, tr, weights=w)
        for name, o in (("total", o_tot), ("balanced", o_bal)):
            agg[name].append(evaluate(o, matched, truth, action, te))
            t, ok, cc, ba = per_class(o, matched, truth, action, te)
            bal_acc[name].append(ba)
            if s == 0:
                last[name] = (t, ok, cc)

    print(f"  {'objetivo':<24}{'e2e test':>11}{'acierto balanceado':>21}")
    for name, label in (("total", "aciertos totales"), ("balanced", "balanceado por clase")):
        print(f"  {label:<24}{statistics.mean(agg[name]):>11.4f}"
              f"{statistics.mean(bal_acc[name]):>21.4f}")
    print(f"\n  coste en agregado de balancear: "
          f"{statistics.mean(agg['total']) - statistics.mean(agg['balanced']):+.4f}")
    print(f"  ganancia en acierto balanceado : "
          f"{statistics.mean(bal_acc['balanced']) - statistics.mean(bal_acc['total']):+.4f}")

    print(f"\n  POR CLASE en test (particion 0):")
    t_tot, ok_tot, cc = last["total"]
    _, ok_bal, _ = last["balanced"]
    print(f"  {'clase':<24}{'test':>6}{'techo':>7}{'total':>8}{'balanc.':>9}"
          f"{'% techo tot':>13}{'% techo bal':>13}")
    for c in sorted(t_tot, key=lambda k: -t_tot[k]):
        ce = cc.get(c, 0)
        pt = 100 * ok_tot.get(c, 0) / ce if ce else 0
        pb = 100 * ok_bal.get(c, 0) / ce if ce else 0
        print(f"  {c:<24}{t_tot[c]:>6}{ce:>7}{ok_tot.get(c,0):>8}"
              f"{ok_bal.get(c,0):>9}{pt:>12.0f}%{pb:>12.0f}%")

    OUT.mkdir(exist_ok=True)
    (OUT / "budget_and_balance.json").write_text(json.dumps({
        "_env": environment(),
        "label_budget": budget_rows,
        "objective_comparison": {
            name: {"e2e_test_mean": round(statistics.mean(agg[name]), 4),
                   "balanced_acc_mean": round(statistics.mean(bal_acc[name]), 4)}
            for name in ("total", "balanced")},
        "per_class_split0": {
            c: {"test": t_tot[c], "ceiling": cc.get(c, 0),
                "greedy_total": ok_tot.get(c, 0), "greedy_balanced": ok_bal.get(c, 0)}
            for c in t_tot},
        "notes": "submuestreo aleatorio simple; estratificar exigiria conocer "
                 "las etiquetas racionadas",
    }, indent=2))
    print(f"\n-> {OUT/'budget_and_balance.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
