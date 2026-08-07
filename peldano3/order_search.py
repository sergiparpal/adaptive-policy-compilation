"""
STEP A of rung 3: search for the total order that maximizes accuracy over the
corpus, using the 577 rules the LLM wrote in rung 1. No LLM.

--------------------------------------------------------------------------
THE CEILING, FIRST
--------------------------------------------------------------------------
Under first-match-wins, the winner of a case is the lowest-ranked rule among
those matching it. So a case is WINNABLE by some order iff some rule matching it
has the correct action. If none has it, no order saves it. That count is exact
and requires no search; it bounds everything else.

Two ceilings are computed:
  * pure   : over the rules that MATCH the case
  * hybrid : over the rules UNDEFEATED by subsumption, which are the only ones
             that can win in the rung 2 engine. It is <= the pure one:
             subsumption may remove the only correct rule from the bidding.

--------------------------------------------------------------------------
THE SPLIT
--------------------------------------------------------------------------
Grouped by case identity and stratified by true action, 50/50.

  * GROUPED because 23.1% of the corpus cases have an exact twin. A random
    split would put copies of the same case on both sides and the test would
    reward memorizing. All copies of a case fall on the same side.
  * STRATIFIED because ONCALL_ESCALATION is 7 cases out of 2000 and
    SECURITY_INCIDENT 20. Without stratifying, one half can end up with none
    and the test would measure nothing about them.
  * 50/50 because with 577 rules and 2000 cases the search set is already
    small; trimming it further would make the order found be noise.

LEAKAGE THAT NO SPLIT UNDOES, and it has to be declared: the 577 rules were
learned over the 2000 cases (born_at runs from 0 to 1998). The test set is not
data unseen by the RULES; it is data unseen by the ORDER. What this setup
measures is overfitting of the order, and only that. The real gap of a complete
system would be larger.

--------------------------------------------------------------------------
THE SEARCH METHOD
--------------------------------------------------------------------------
Decision-list greedy search: repeatedly pick the rule that, placed in the next
position, maximizes (cases it wins - cases it loses) among the train cases not
yet decided; place it and remove the cases it matches.

It is the classic greedy construction of decision lists.

  GUARANTEES: optimality of each local step over the live cases, and that the
              order produced is a valid total order over the 577 rules.
  DOES NOT GUARANTEE: anything global. The problem is of the minimum feedback
              arc set kind; there is no known approximation ratio for this
              objective and no local search was run afterwards.

Tail of the order: once no train case remains to be decided, all remaining rules
score 0. They are sorted by train precision and then by born_at. That tail is
arbitrary with respect to train and is a known source of gap: on test it may
well get to decide.

Three orders that search for nothing are also compared: born_at (arrival order),
train precision, and averaged random.
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from harness.domain import generate_corpus
from harness.dsl import Condition
from harness.hidden_policy import true_action
from harness.provenance import environment
from peldano2.engine2 import Space, strictly_below   # reuse, not modification

OUT = Path("results3")
N_SPLITS = 5
N_RANDOM = 50


# ---------------------------------------------------------------------------
# Loading and structure
# ---------------------------------------------------------------------------

def load():
    corpus = generate_corpus(2000, seed=17)
    d = json.loads(Path("results/llm_run.json").read_text())
    rules = d["rules"]
    space = Space()
    ext, conds = {}, {}
    for r in rules:
        cs = [Condition(c["attr"], c["op"], c["value"]) for c in r["conditions"]]
        conds[r["rule_id"]] = cs
        ext[r["rule_id"]] = space.extension(cs)
    return corpus, rules, ext, conds


def subsumption_below(rules, ext):
    """below[A] = {B : ext(B) ⊊ ext(A)}, pruned by popcount."""
    pc = {r["rule_id"]: ext[r["rule_id"]].bit_count() for r in rules}
    order = sorted(rules, key=lambda r: pc[r["rule_id"]])
    below = {r["rule_id"]: set() for r in rules}
    for i, b in enumerate(order):
        eb, pb = ext[b["rule_id"]], pc[b["rule_id"]]
        if eb == 0:
            continue
        for a in order[i + 1:]:
            if pc[a["rule_id"]] == pb:
                continue
            if (eb | ext[a["rule_id"]]) == ext[a["rule_id"]]:
                below[a["rule_id"]].add(b["rule_id"])
    return below


def build_tables(corpus, rules, conds, below):
    """Per case: matching rules, rules undefeated by subsumption, truth."""
    matched, undef, truth = [], [], []
    for case in corpus:
        m = [r["rule_id"] for r in rules
             if all(c.holds(case) for c in conds[r["rule_id"]])]
        ids = set(m)
        u = [rid for rid in m if not (below[rid] & ids)]
        matched.append(m)
        undef.append(u)
        truth.append(true_action(case))
    return matched, undef, truth


# ---------------------------------------------------------------------------
# Ceiling
# ---------------------------------------------------------------------------

def ceiling(pool, truth, action, idxs):
    """Cases winnable by SOME order: some rule in the pool has the correct
    action. Exact, no search."""
    ok = sum(1 for i in idxs if any(action[r] == truth[i] for r in pool[i]))
    return ok / len(idxs)


# ---------------------------------------------------------------------------
# Greedy search
# ---------------------------------------------------------------------------

def greedy_order(rules, pool, truth, action, train_idx):
    """Decision-list greedy over `pool` (matched or undefeated)."""
    ids = [r["rule_id"] for r in rules]
    pos = {i: k for k, i in enumerate(train_idx)}
    win = {rid: 0 for rid in ids}
    lose = {rid: 0 for rid in ids}
    for i in train_idx:
        for rid in pool[i]:
            bit = 1 << pos[i]
            if action[rid] == truth[i]:
                win[rid] |= bit
            else:
                lose[rid] |= bit

    remaining = (1 << len(train_idx)) - 1
    left = set(ids)
    order = []
    while left and remaining:
        best, best_score = None, None
        # FIX 2026-08-06: iterate over a SORTED list, not over the set. Before,
        # the argmax walked `left` directly and the tie-break was at the mercy
        # of the iteration order of a set of strings, which depends on
        # PYTHONHASHSEED: the same cell gave between 0.5880 and 0.5991
        # depending on the hash. Sorting by rule_id is deterministic and, since
        # the ids are R%04d assigned in birth order, it amounts to breaking ties
        # by the oldest rule. Rungs 3 and 4 have NOT been re-run with this fix:
        # that will be done together with a serious optimizer, so as to
        # distinguish whether the fragility came from the tie-break or from the
        # algorithm.
        for rid in sorted(left):
            s = (win[rid] & remaining).bit_count() - (lose[rid] & remaining).bit_count()
            if best_score is None or s > best_score:
                best, best_score = rid, s
        order.append(best)
        left.discard(best)
        remaining &= ~(win[best] | lose[best])

    # tail: nothing left to decide on train. Train precision, then born_at.
    born = {r["rule_id"]: r["born_at"] for r in rules}
    def prec(rid):
        w, l = win[rid].bit_count(), lose[rid].bit_count()
        return (w / (w + l)) if (w + l) else -1.0
    order += sorted(left, key=lambda rid: (-prec(rid), born[rid]))
    return order


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(order, pool, truth, action, idxs):
    rank = {rid: k for k, rid in enumerate(order)}
    ok = 0
    for i in idxs:
        p = pool[i]
        if not p:
            continue
        w = min(p, key=lambda rid: rank[rid])
        if action[w] == truth[i]:
            ok += 1
    return ok / len(idxs)


def eval_specificity(rules, matched, truth, action, idxs):
    ncond = {r["rule_id"]: len(r["conditions"]) for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ok = 0
    for i in idxs:
        m = matched[i]
        if not m:
            continue
        top = max(ncond[r] for r in m)
        fin = [r for r in m if ncond[r] == top]
        if len({action[r] for r in fin}) > 1:
            continue                       # CONFLICT
        if action[min(fin, key=lambda r: born[r])] == truth[i]:
            ok += 1
    return ok / len(idxs)


def eval_subsumption(undef, truth, action, idxs):
    ok = 0
    for i in idxs:
        u = undef[i]
        if not u:
            continue
        if len({action[r] for r in u}) > 1:
            continue                       # CONFLICT
        if action[u[0]] == truth[i]:
            ok += 1
    return ok / len(idxs)


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

def split(corpus, truth, seed):
    """Grouped by case identity, stratified by action, 50/50."""
    groups = defaultdict(list)
    for i, c in enumerate(corpus):
        groups[c.key()].append(i)
    by_action = defaultdict(list)
    for key, idxs in groups.items():
        by_action[truth[idxs[0]]].append(idxs)
    rng = random.Random(seed)
    train, test = [], []
    for act, gs in sorted(by_action.items()):
        gs = sorted(gs)
        rng.shuffle(gs)
        for k, g in enumerate(gs):
            (train if k % 2 == 0 else test).extend(g)
    return sorted(train), sorted(test)


# ---------------------------------------------------------------------------

def main() -> int:
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    allidx = list(range(len(corpus)))

    print("=" * 78)
    print("PELDANO 3 · PASO A — ORDEN POR BUSQUEDA SOBRE EL CORPUS")
    print("=" * 78)
    print(f"  reglas: {len(rules)}   casos: {len(corpus)}   semilla del corpus: 17")
    nomatch = sum(1 for i in allidx if not matched[i])
    noundef = sum(1 for i in allidx if not undef[i])
    print(f"  casos sin ninguna regla que los case: {nomatch} ({nomatch/2000:.1%})")

    # ---------------------------------------------------------- CEILING
    print()
    print("=" * 78)
    print("TECHO — maximo alcanzable por CUALQUIER orden (exacto, sin buscar)")
    print("=" * 78)
    ceil_pure = ceiling(matched, truth, action, allidx)
    ceil_hyb = ceiling(undef, truth, action, allidx)
    print(f"  techo PURO    (primera-que-casa)      {ceil_pure:.4f}")
    print(f"  techo HIBRIDO (subsuncion + orden)    {ceil_hyb:.4f}")
    print(f"  perdida por subsuncion                {ceil_pure - ceil_hyb:.4f}")
    print(f"  casos sin regla correcta que los case: "
          f"{round((1-ceil_pure)*2000)} de 2000")

    lost = Counter()
    for i in allidx:
        if not any(action[r] == truth[i] for r in matched[i]):
            lost[truth[i]] += 1
    tot = Counter(truth)
    print("\n  casos irrecuperables por clase (ningun orden los salva):")
    print(f"    {'clase':<24}{'corpus':>8}{'irrecup.':>10}{'%':>8}")
    for cls in sorted(tot, key=lambda k: -tot[k]):
        print(f"    {cls:<24}{tot[cls]:>8}{lost.get(cls,0):>10}"
              f"{100*lost.get(cls,0)/tot[cls]:>7.1f}%")

    # ------------------------------------------------------ SEARCH PER SPLIT
    print()
    print("=" * 78)
    print(f"BUSQUEDA CON PARTICION agrupada+estratificada 50/50 · {N_SPLITS} particiones")
    print("=" * 78)

    rows = []
    for s in range(N_SPLITS):
        tr, te = split(corpus, truth, seed=17 + s)
        row = {"split": s, "seed": 17 + s, "n_train": len(tr), "n_test": len(te)}
        for name, pool in (("puro", matched), ("hibrido", undef)):
            order = greedy_order(rules, pool, truth, action, tr)
            row[f"{name}_train"] = evaluate(order, pool, truth, action, tr)
            row[f"{name}_test"] = evaluate(order, pool, truth, action, te)
            row[f"{name}_gap"] = row[f"{name}_train"] - row[f"{name}_test"]
            row[f"{name}_ceil_train"] = ceiling(pool, truth, action, tr)
            row[f"{name}_ceil_test"] = ceiling(pool, truth, action, te)
            if s == 0:
                row[f"{name}_order"] = order
        rows.append(row)

    print(f"  {'part':>5}{'train':>9}{'test':>9}{'GAP':>9}   "
          f"{'train':>9}{'test':>9}{'GAP':>9}")
    print(f"  {'':>5}{'--- primera-que-casa ---':^27}   {'--- hibrido ---':^27}")
    for r in rows:
        print(f"  {r['split']:>5}{r['puro_train']:>9.4f}{r['puro_test']:>9.4f}"
              f"{r['puro_gap']:>9.4f}   {r['hibrido_train']:>9.4f}"
              f"{r['hibrido_test']:>9.4f}{r['hibrido_gap']:>9.4f}")
    for name in ("puro", "hibrido"):
        tr = [r[f"{name}_train"] for r in rows]
        te = [r[f"{name}_test"] for r in rows]
        gp = [r[f"{name}_gap"] for r in rows]
        print(f"\n  {name}:  train {statistics.mean(tr):.4f}±{statistics.pstdev(tr):.4f}"
              f"   test {statistics.mean(te):.4f}±{statistics.pstdev(te):.4f}"
              f"   GAP {statistics.mean(gp):.4f}±{statistics.pstdev(gp):.4f}")

    # --------------------------------------------------------- REFERENCES
    print()
    print("=" * 78)
    print("REFERENCIAS sobre la misma base y las mismas particiones")
    print("=" * 78)
    tr0, te0 = split(corpus, truth, seed=17)
    rng = random.Random(17)
    ids = [r["rule_id"] for r in rules]
    rand_test = []
    for _ in range(N_RANDOM):
        o = ids[:]
        rng.shuffle(o)
        rand_test.append(evaluate(o, matched, truth, action, te0))
    born_order = sorted(ids, key=lambda r: born[r])

    print(f"  {'estrategia':<40}{'train':>9}{'test':>9}")
    print(f"  {'orden buscado (voraz), puro':<40}"
          f"{rows[0]['puro_train']:>9.4f}{rows[0]['puro_test']:>9.4f}")
    print(f"  {'orden buscado (voraz), hibrido':<40}"
          f"{rows[0]['hibrido_train']:>9.4f}{rows[0]['hibrido_test']:>9.4f}")
    print(f"  {'orden de llegada (born_at), puro':<40}"
          f"{evaluate(born_order, matched, truth, action, tr0):>9.4f}"
          f"{evaluate(born_order, matched, truth, action, te0):>9.4f}")
    print(f"  {'orden aleatorio, puro (media de 50)':<40}{'—':>9}"
          f"{statistics.mean(rand_test):>9.4f}")
    print(f"  {'arbitraje por especificidad':<40}"
          f"{eval_specificity(rules, matched, truth, action, tr0):>9.4f}"
          f"{eval_specificity(rules, matched, truth, action, te0):>9.4f}")
    print(f"  {'subsuncion sola (conflicto = fallo)':<40}"
          f"{eval_subsumption(undef, truth, action, tr0):>9.4f}"
          f"{eval_subsumption(undef, truth, action, te0):>9.4f}")
    print(f"\n  referencias del peldano 1 sobre los 2000 casos:"
          f" especificidad 0.1825 · subsuncion 0.0375")
    print(f"  techo sobre los 2000: puro {ceil_pure:.4f} · hibrido {ceil_hyb:.4f}")

    OUT.mkdir(exist_ok=True)
    (OUT / "order_search.json").write_text(json.dumps({
        "_env": environment(n_splits=N_SPLITS, n_random=N_RANDOM),
        "n_rules": len(rules), "n_cases": len(corpus),
        "ceiling_pure": round(ceil_pure, 4), "ceiling_hybrid": round(ceil_hyb, 4),
        "cases_without_matching_rule": nomatch,
        "unrecoverable_by_class": dict(lost),
        "splits": [{k: v for k, v in r.items() if not k.endswith("_order")}
                   for r in rows],
        "summary": {name: {
            "train_mean": round(statistics.mean([r[f"{name}_train"] for r in rows]), 4),
            "test_mean": round(statistics.mean([r[f"{name}_test"] for r in rows]), 4),
            "gap_mean": round(statistics.mean([r[f"{name}_gap"] for r in rows]), 4),
            "gap_sd": round(statistics.pstdev([r[f"{name}_gap"] for r in rows]), 4),
        } for name in ("puro", "hibrido")},
        "references_split0": {
            "born_at_train": round(evaluate(born_order, matched, truth, action, tr0), 4),
            "born_at_test": round(evaluate(born_order, matched, truth, action, te0), 4),
            "random_test_mean": round(statistics.mean(rand_test), 4),
            "specificity_test": round(eval_specificity(rules, matched, truth, action, te0), 4),
            "subsumption_test": round(eval_subsumption(undef, truth, action, te0), 4),
        },
        "best_order_split0_pure": rows[0]["puro_order"],
    }, indent=2))
    print(f"\n-> {OUT/'order_search.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
