"""
Run comparator for rung 2.

It serves to isolate the prompt confound: if the narrowing of the rules (more
conditions, less overlap) repeats across different corpora with the same prompt,
it is an effect of the prompt; if it wobbles, it was non-determinism noise.

Usage:  python3 -m rung2.compare_runs results2/llm_run2_*.json
"""

from __future__ import annotations

import itertools
import json
import statistics
import sys
from pathlib import Path

from harness.dsl import Condition
from harness.provenance import environment
from harness.record_guard import FLAG, or_exit, refuse_shrink

from .engine2 import Space, strictly_below

RECORD = Path("results2/comparison.json")


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
    # No argparse: everything here is positional except the escape hatch, and
    # a shell glob already arrives expanded.
    overwrite = FLAG in argv
    files = [a for a in argv if a != FLAG]

    space = Space()
    rows = [analyse(Path(p), space) for p in sorted(files)]

    # The record is written at the end because computing it is free, but it is
    # checked HERE, before printing a report that suggests everything went
    # fine. Shrinking is the failure this cannot see from the destination: the
    # path never changes, the rows do.
    or_exit(refuse_shrink, RECORD, rows, overwrite=overwrite,
            hint="    python3 -m rung2.compare_runs results2/llm_run2_*.json")

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

    # Aug 7, 2026: the output goes from a bare list to an object so that the
    # `_env` block can be hung off it. The rows are the same, under the "rows"
    # key. The record was re-run that same day with the 8 runs and adopted the
    # new shape without a single row changing; see results2/RECORD_NOTES.md.
    # It still rewrites with whatever is passed as an ARGUMENT — that has not
    # changed and cannot change, it is what the command is for. What is guarded
    # since Aug 8, 2026 is the consequence: it refuses to shrink the record.
    RECORD.write_text(json.dumps({"_env": environment(), "rows": rows}, indent=2))
    print(f"\n-> {RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
