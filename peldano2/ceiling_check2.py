"""
STEP 0 of rung 2: ceiling of the hybrid engine with the perfect policy loaded.

No LLM. Zero API calls. If this does not give ~100%, the redesign does not work
and there is no point running anything else.

Usage:  python3 -m peldano2.ceiling_check2
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from harness.domain import generate_corpus
from harness.hidden_policy import true_action, true_rule_id
from harness.provenance import environment

from .engine2 import Space, strictly_below
from .hidden_priority import build_hidden_engine

OUT = Path("results2")

REF = {
    "especificidad (peldano 1)": (0.5875, 0.2140, 505),
    "subsuncion sola (peldano 1)": (0.6315, 0.0000, 737),
}


def main() -> int:
    corpus = generate_corpus(2000, seed=17)
    space = Space()
    engine, declared, stats = build_hidden_engine(space)

    print("=" * 74)
    print("PELDANO 2 · PASO 0 — TECHO DEL MOTOR HIBRIDO")
    print("=" * 74)
    print(f"  espacio exhaustivo: {space.n:,} casos")
    print(f"  reglas cargadas   : {len(engine.rules)}")

    n_rules = len(engine.rules)
    total_pairs = n_rules * (n_rules - 1) // 2
    sub_pairs = sum(len(s) for s in engine.sub_below.values())
    print(f"\n  NIVEL 1 · subsuncion")
    print(f"    parejas ordenadas por estructura : {sub_pairs} de {total_pairs}"
          f"  ({sub_pairs/total_pairs:.1%})")
    print(f"\n  NIVEL 2 · prioridad declarada (minima, derivada del orden de capas)")
    print(f"    aristas DECLARADAS               : {stats['declared']}"
          f"  ({stats['declared']/total_pairs:.1%} de los pares)")
    print(f"    pares que no la necesitan:")
    print(f"      extensiones disjuntas          : {stats['skipped_disjoint']}")
    print(f"      ya ordenados por subsuncion    : {stats['skipped_subsumed_by_structure']}")
    print(f"      misma accion (da igual)        : {stats['skipped_same_action']}")
    print(f"    aristas rechazadas por el validador: {len(stats['rejected'])}")
    for a, b, why in stats["rejected"][:10]:
        print(f"      {a} -> {b}: {why}")

    # ------------------------------------------------------------- measurement
    out = collections.Counter()
    n_ok = 0
    wrong = []
    conflicts = []
    for case in corpus:
        outcome, winner, involved = engine.decide(case)
        out[outcome] += 1
        truth = true_action(case)
        if outcome == "ACTION":
            if winner.action == truth:
                n_ok += 1
            else:
                wrong.append((case, truth, winner.action, winner.rule_id))
        elif outcome == "CONFLICT":
            conflicts.append((true_rule_id(case), [r.rule_id for r in involved]))

    n = len(corpus)
    n_act = out["ACTION"]
    e2e = n_ok / n
    silent = (1 - n_ok / n_act) if n_act else 0.0

    print()
    print("=" * 74)
    print("RESULTADO (n=2000, semilla 17)")
    print("=" * 74)
    print(f"  {'arbitraje':<34}{'e2e':>9}{'err.sil':>10}{'CONFLICT':>10}{'IMPASSE':>9}")
    for name, (r_e2e, r_sil, r_cf) in REF.items():
        print(f"  {name:<34}{r_e2e:>9.4f}{r_sil:>10.4f}{r_cf:>10}{0:>9}")
    print(f"  {'HIBRIDO (peldano 2)':<34}{e2e:>9.4f}{silent:>10.4f}"
          f"{out['CONFLICT']:>10}{out['IMPASSE']:>9}")
    print(f"  {'objetivo':<34}{1.0:>9.4f}{0.0:>10.4f}{'~0':>10}{0:>9}")

    print(f"\n  ACTION {n_act}   aciertos {n_ok}   errores silenciosos {len(wrong)}")

    if wrong:
        print(f"\n  ERRORES SILENCIOSOS ({len(wrong)}):")
        c = collections.Counter((true_rule_id(w[0]), w[1], w[2]) for w in wrong)
        for (hid, t, p), k in c.most_common(15):
            print(f"    capa {hid}: verdad {t} -> predicho {p}  ({k})")
    if conflicts:
        print(f"\n  CONFLICTOS ({len(conflicts)}):")
        c = collections.Counter(tuple(x[1]) for x in conflicts)
        for combo, k in c.most_common(15):
            print(f"    {'  '.join(combo)}  ({k})")

    veredicto = "PASA" if e2e >= 0.995 and silent == 0.0 else "NO PASA"
    print(f"\n  PARADA 0 -> {veredicto}")

    OUT.mkdir(exist_ok=True)
    (OUT / "ceiling2.json").write_text(json.dumps({
        "_env": environment(),
        "n_rules": n_rules,
        "space": space.n,
        "subsumption_pairs": sub_pairs,
        "declared_edges": stats["declared"],
        "possible_pairs": total_pairs,
        "skipped": {k: v for k, v in stats.items() if k.startswith("skipped")},
        "rejected_edges": [{"winner": a, "loser": b, "reason": w}
                           for a, b, w in stats["rejected"]],
        "action": n_act, "conflict": out["CONFLICT"], "impasse": out["IMPASSE"],
        "correct": n_ok, "e2e": round(e2e, 4), "silent_error": round(silent, 4),
        "verdict": veredicto,
        "reference_peldano1": {k: {"e2e": v[0], "silent_error": v[1], "conflict": v[2]}
                               for k, v in REF.items()},
    }, indent=2))
    print(f"\n-> {OUT/'ceiling2.json'}")
    return 0 if veredicto == "PASA" else 1


if __name__ == "__main__":
    sys.exit(main())
