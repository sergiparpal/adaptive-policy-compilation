"""
Subsumption arbitration applied to the LEARNED BASE, offline.

Over the hidden policy, subsumption turned out to be sound: 0 silent errors over
1263 decided cases, because its author put the exceptions before the defaults,
so that ext(A) ⊊ ext(B) always implied priority(A) < priority(B).

A base written by an LLM has no such author. This script checks whether the
property survives: how often the minimal rule under subsumption proposes an
action different from the truth.

IT IS A BOUND, NOT A SIMULATION. The 577 rules were learned UNDER
specificity-based arbitration: which case escalated, and therefore which rule
was born, depended on that arbitration. Under subsumption the base would have
been a different one from the first case. What is measured here is how THIS base
behaves under a DIFFERENT arbitration, not what the loop would have produced.

Second caveat: here the 577 rules are loaded from case 0, whereas in the run
they accumulated. The figures are not directly comparable with those in
results/llm_run.json; that is why static specificity is recomputed as well.

ANALYSIS, NOT MODIFICATION. It does not touch dsl.py.

Usage:  python3 -m harness.learned_subsumption
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from .ceiling_check import all_cases
from .domain import ATTRIBUTES, DOMAINS, generate_corpus
from .dsl import Condition, Rule, RuleEngine
from .hidden_policy import true_action, true_rule_id
from .provenance import environment

RESULTS = Path("results")


# ---------------------------------------------------------------------------
# Fast extensions: masks per (attribute, value), then AND per rule
# ---------------------------------------------------------------------------

def attribute_masks():
    """For each (attr, value), the mask of cases in the space satisfying it."""
    space = list(all_cases())
    n = len(space)
    bits: dict[str, dict] = {a: {v: bytearray(n) for v in DOMAINS[a]} for a in ATTRIBUTES}
    for i, c in enumerate(space):
        for a in ATTRIBUTES:
            bits[a][getattr(c, a)][i] = 1
    # bit i (counting from the left) = case i of the space. The absolute
    # position does not matter as long as it is the same in every mask.
    masks = {a: {v: int("".join(map(str, b)), 2) for v, b in d.items()}
             for a, d in bits.items()}
    return masks, n


def condition_mask(cond: Condition, amask, full: int) -> int:
    dom = DOMAINS[cond.attr]
    m = amask[cond.attr]
    if cond.op == "eq":
        return m.get(cond.value, 0)
    if cond.op == "neq":
        return full & ~m.get(cond.value, 0)
    if cond.op == "lte":
        out = 0
        for v in dom:
            if v <= cond.value:
                out |= m[v]
        return out
    if cond.op == "gte":
        out = 0
        for v in dom:
            if v >= cond.value:
                out |= m[v]
        return out
    if cond.op == "in":
        out = 0
        for v in cond.value:
            out |= m.get(v, 0)
        return out
    raise AssertionError(cond.op)


def build_extensions(rules, amask, n):
    full = (1 << n) - 1
    out = {}
    for r in rules:
        acc = full
        for c in r.conditions:
            acc &= condition_mask(c, amask, full)
            if acc == 0:
                break
        out[r.rule_id] = acc
    return out


# ---------------------------------------------------------------------------

def load_learned() -> list[Rule]:
    d = json.loads((RESULTS / "llm_run.json").read_text())
    rules = []
    for r in d["rules"]:
        rules.append(Rule(
            rule_id=r["rule_id"],
            conditions=[Condition(c["attr"], c["op"], c["value"]) for c in r["conditions"]],
            action=r["action"],
            born_at=r["born_at"],
        ))
    return d["model"], rules


def strict_below_sets(rules, ext):
    """below[A] = {B : ext(B) ⊊ ext(A)}. Pruned by popcount."""
    pc = {r.rule_id: ext[r.rule_id].bit_count() for r in rules}
    order = sorted(rules, key=lambda r: pc[r.rule_id])
    below = {r.rule_id: set() for r in rules}
    for i, b in enumerate(order):           # b is a candidate for being below
        eb, pb = ext[b.rule_id], pc[b.rule_id]
        if eb == 0:
            continue
        for a in order[i + 1:]:             # a has >= bits than b
            if pc[a.rule_id] == pb:
                continue                    # same popcount -> cannot be strict
            if (eb | ext[a.rule_id]) == ext[a.rule_id]:
                below[a.rule_id].add(b.rule_id)
    return below


def decide_subsumption(matched, below):
    if not matched:
        return "IMPASSE", None, []
    ids = {r.rule_id for r in matched}
    minimal = [a for a in matched if not (below[a.rule_id] & ids)]
    if len({r.action for r in minimal}) == 1:
        return "ACTION", minimal[0], minimal
    return "CONFLICT", None, minimal


def main() -> int:
    corpus = generate_corpus(2000, seed=17)
    model, rules = load_learned()
    print("=" * 74)
    print("SUBSUNCION SOBRE LA BASE APRENDIDA")
    print("=" * 74)
    print(f"  modelo: {model}   reglas: {len(rules)}")

    amask, n_space = attribute_masks()
    ext = build_extensions(rules, amask, n_space)
    print(f"  espacio: {n_space:,} casos   extensiones calculadas")

    empty = [r.rule_id for r in rules if ext[r.rule_id] == 0]
    print(f"  reglas con extension vacia (no casan nada): {len(empty)}")

    below = strict_below_sets(rules, ext)
    n_pairs = sum(len(s) for s in below.values())
    total_pairs = len(rules) * (len(rules) - 1) // 2
    print(f"  parejas ordenadas (A ≺ B): {n_pairs} de {total_pairs} "
          f"({n_pairs/total_pairs:.2%})")

    engine = RuleEngine()
    engine.rules = rules

    sub = collections.Counter()
    spec = collections.Counter()
    n_sub_ok = n_spec_ok = 0
    unsound = []          # subsumption commits with action != truth
    residue = collections.Counter()
    for case in corpus:
        truth = true_action(case)
        matched = [r for r in rules if r.matches(case)]

        outcome, winner, minimal = decide_subsumption(matched, below)
        sub[outcome] += 1
        if outcome == "ACTION":
            if winner.action == truth:
                n_sub_ok += 1
            else:
                unsound.append((case, truth, winner.action, winner.rule_id,
                                true_rule_id(case)))
        elif outcome == "CONFLICT":
            residue[tuple(sorted(r.rule_id for r in minimal))] += 1

        so, sw, _ = engine.decide(case)
        spec[so] += 1
        if so == "ACTION" and sw.action == truth:
            n_spec_ok += 1

    n = len(corpus)
    print()
    print("=" * 74)
    print("RESULTADO (base completa cargada desde el caso 0, en ambos casos)")
    print("=" * 74)
    print(f"  {'arbitraje':<20}{'ACTION':>8}{'IMPASSE':>9}{'CONFLICT':>10}"
          f"{'cobert':>9}{'err.sil':>9}{'e2e':>9}")
    for label, c, ok in (("especificidad", spec, n_spec_ok), ("SUBSUNCION", sub, n_sub_ok)):
        act = c["ACTION"]
        print(f"  {label:<20}{act:>8}{c['IMPASSE']:>9}{c['CONFLICT']:>10}"
              f"{act/n:>9.4f}{(1 - ok/act) if act else 0:>9.4f}{ok/n:>9.4f}")

    print()
    print("=" * 74)
    print("SOUNDNESS: ¿la minimal bajo subsuncion coincide con la verdad?")
    print("=" * 74)
    act = sub["ACTION"]
    print(f"  casos en que la subsuncion se compromete: {act}")
    print(f"  de esos, accion DISTINTA de la verdad   : {len(unsound)}"
          f"   ({len(unsound)/act:.2%})" if act else "")
    print(f"\n  politica oculta (referencia): 0 de 1263  (0.00%)")

    if unsound:
        print(f"\n  por capa verdadera de la politica oculta:")
        c = collections.Counter((u[4], u[1], u[2]) for u in unsound)
        print(f"    {'capa':<8}{'verdad':<22}{'predicho':<22}{'casos':>6}")
        for (hid, t, p), k in c.most_common(12):
            print(f"    {hid:<8}{t:<22}{p:<22}{k:>6}")
        print(f"\n  reglas aprendidas responsables (top 10):")
        for rid, k in collections.Counter(u[3] for u in unsound).most_common(10):
            r = next(x for x in rules if x.rule_id == rid)
            conds = " AND ".join(f"{c.attr} {c.op} {c.value}" for c in r.conditions)
            print(f"    {rid} ({k} casos)  SI {conds} -> {r.action}")

    print()
    print(f"  residuo incomparable: {sub['CONFLICT']} casos, "
          f"{len(residue)} conjuntos minimales distintos")
    ranked = residue.most_common()
    print(f"  {'k conjuntos':>12}{'casos ganados':>15}{'e2e si se desempatan':>23}")
    for k in (0, 10, 20, 50, 100, len(ranked)):
        won = sum(c for _s, c in ranked[:k])
        print(f"  {k:>12}{won:>15}{(n_sub_ok + won)/n:>23.4f}")
    print("  (cota optimista: supone que el desempate acierta siempre)")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "learned_subsumption.json").write_text(json.dumps({
        "_env": environment(),
        "model": model,
        "n_rules": len(rules),
        "caveat": "cota, no simulacion: la base se aprendio bajo arbitraje por "
                  "especificidad; bajo subsuncion habria sido otra. Ademas aqui "
                  "se carga completa desde el caso 0.",
        "ordered_pairs": n_pairs,
        "possible_pairs": total_pairs,
        "specificity": {"action": spec["ACTION"], "impasse": spec["IMPASSE"],
                        "conflict": spec["CONFLICT"], "correct": n_spec_ok,
                        "coverage": round(spec["ACTION"] / n, 4),
                        "silent_error": round(1 - n_spec_ok / spec["ACTION"], 4),
                        "e2e": round(n_spec_ok / n, 4)},
        "subsumption": {"action": sub["ACTION"], "impasse": sub["IMPASSE"],
                        "conflict": sub["CONFLICT"], "correct": n_sub_ok,
                        "coverage": round(sub["ACTION"] / n, 4),
                        "silent_error": round(1 - n_sub_ok / sub["ACTION"], 4) if sub["ACTION"] else None,
                        "e2e": round(n_sub_ok / n, 4)},
        "soundness": {"committed": act, "wrong": len(unsound),
                      "rate": round(len(unsound) / act, 4) if act else None,
                      "hidden_policy_reference": {"committed": 1263, "wrong": 0}},
        "residue_sets": len(residue),
    }, indent=2))
    print(f"\n-> {RESULTS/'learned_subsumption.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
