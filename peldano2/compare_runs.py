"""
Comparador de tiradas del peldano 2.

Sirve para aislar el confound del prompt: si el estrechamiento de las reglas
(mas condiciones, menos solape) se repite con corpus distintos y el mismo
prompt, es efecto del prompt; si baila, era ruido de no-determinismo.

Uso:  python3 -m peldano2.compare_runs results2/llm_run2_*.json
"""

from __future__ import annotations

import itertools
import json
import statistics
import sys
from pathlib import Path

from harness.dsl import Condition

from .engine2 import Space, strictly_below


def analyse(path: Path, space: Space) -> dict:
    d = json.loads(path.read_text())
    rules = d["rules"]
    m = d["metrics"]
    ext = {
        r["rule_id"]: space.extension(
            [Condition(c["attr"], c["op"], c["value"]) for c in r["conditions"]])
        for r in rules
    }
    ids = [r["rule_id"] for r in rules]
    act = {r["rule_id"]: r["action"] for r in rules}
    pairs = list(itertools.combinations(ids, 2))
    overlap = [(a, b) for a, b in pairs if ext[a] & ext[b]]
    nested = [(a, b) for a, b in pairs
              if strictly_below(ext[a], ext[b]) or strictly_below(ext[b], ext[a])]
    ov_diff = [(a, b) for a, b in overlap if act[a] != act[b]]
    ncond = [len(r["conditions"]) for r in rules]
    return {
        "file": path.name,
        "seed": d.get("seed"),
        "prompt_version": d.get("prompt_version", "v1"),
        "n_rules": len(rules),
        "mean_conditions": round(statistics.mean(ncond), 2) if ncond else 0,
        "median_conditions": statistics.median(ncond) if ncond else 0,
        "cond_hist": {k: ncond.count(k) for k in sorted(set(ncond))},
        "pairs": len(pairs),
        "overlapping_pairs": len(overlap),
        "overlap_pct": round(100 * len(overlap) / len(pairs), 1) if pairs else 0.0,
        "overlapping_diff_action": len(ov_diff),
        "nested_pairs": len(nested),
        "conflicts": m["conflicts"],
        "impasses": m["impasses"],
        "edges_proposed": m["edges_proposed"],
        "edges_accepted": m["edges_accepted"],
        "edge_reasons": m["edge_reasons"],
        "coverage": m["coverage"],
        "silent_error_rate": m["silent_error_rate"],
        "e2e": m["e2e_accuracy"],
        "mean_ext_size": round(statistics.mean(e.bit_count() for e in ext.values())),
    }


def main(argv: list[str]) -> int:
    space = Space()
    rows = [analyse(Path(p), space) for p in sorted(argv)]

    print("=" * 108)
    print("COMPARATIVA DE TIRADAS  (n=100, mismo modelo, mismo prompt salvo donde se indique)")
    print("=" * 108)
    h = (f"  {'fichero':<26}{'ver':>4}{'semilla':>8}{'reglas':>7}{'cond/regla':>11}"
         f"{'solape%':>9}{'sol.dif':>8}{'anid':>6}{'CONF':>6}{'arist':>7}{'acept':>7}")
    print(h)
    print("  " + "-" * 104)
    for r in rows:
        print(f"  {r['file']:<26}{r['prompt_version']:>4}{str(r['seed']):>8}"
              f"{r['n_rules']:>7}{r['mean_conditions']:>11.2f}"
              f"{r['overlap_pct']:>9.1f}{r['overlapping_diff_action']:>8}"
              f"{r['nested_pairs']:>6}{r['conflicts']:>6}"
              f"{r['edges_proposed']:>7}{r['edges_accepted']:>7}")

    print()
    print(f"  {'fichero':<26}{'cobert':>9}{'err.sil':>9}{'e2e':>9}{'ext.media':>11}"
          f"   motivos de rechazo de aristas")
    print("  " + "-" * 104)
    for r in rows:
        print(f"  {r['file']:<26}{r['coverage']:>9.3f}{r['silent_error_rate']:>9.4f}"
              f"{r['e2e']:>9.4f}{r['mean_ext_size']:>11,}   {r['edge_reasons']}")

    print()
    print("  histograma de condiciones por regla:")
    for r in rows:
        print(f"    {r['file']:<26}{r['cond_hist']}")

    v1 = [r for r in rows if r["prompt_version"] == "v1"]
    if len(v1) > 1:
        mc = [r["mean_conditions"] for r in v1]
        ov = [r["overlap_pct"] for r in v1]
        cf = [r["conflicts"] for r in v1]
        print()
        print("  DISPERSION ENTRE TIRADAS CON EL MISMO PROMPT (v1):")
        print(f"    condiciones/regla: {mc}   media {statistics.mean(mc):.2f}"
              f"   desv {statistics.pstdev(mc):.2f}")
        print(f"    solape %         : {ov}   media {statistics.mean(ov):.1f}"
              f"   desv {statistics.pstdev(ov):.1f}")
        print(f"    conflictos       : {cf}")

    out = Path("results2/comparativa.json")
    out.write_text(json.dumps(rows, indent=2))
    print(f"\n-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
