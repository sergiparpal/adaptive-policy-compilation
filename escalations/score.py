"""
THE STAGE of `PLAN_ESCALATIONS.md` §8: labels at the escalations, scored.

It refuses while §0 is unsigned, before it builds or measures anything; no flag
skips that. `--dry-run` runs `J-g1` to `J-g3` and writes nothing. Then, in this
order:

  1. **The blocking checks**, `escalations/gates.py`.
  2. **The selections** of `escalations/selections.py`: at 10, 50, 100 and 251
     labels, five random draws of the 316 escalations, the first in arrival
     order and the most crowded; and all 316.
  3. **One order per selection**, `escalations/instrument.py`'s search labelled
     with the truth there, scored on test split 0 and over the space.
  4. **The random arrivals** at the same budgets: the audit record's own five
     draws on split 0, read as published, never re-drawn.
  5. **`J-a` to `J-e`**, each with §0's label, and the readings of `J-f`.

Surfaces: corpus test split 0, 995 cases, and the exhaustive space, 134,400
points, every count against the truth. Space figures are compared at four
decimals, the record's precision.

PROVENANCE: PRE-REGISTERED. §0 was signed before any figure here existed; the
gate is what says so.

    python3 -m escalations.score --dry-run           # J-g1..J-g3, blocking; writes nothing
    PYTHONHASHSEED=0 python3 -m escalations.score    # J-a to J-e, and the readings of J-f
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from typing import Any

from harness.provenance import describe, environment

from . import gates
from . import instrument as I
from . import plan, selections

N_TEST = 995


def comparators(pub: dict[int, list[dict]]) -> dict[int, dict[str, Any]]:
    """The random arrivals at each budget, from the record: each draw's test
    count, recovered exactly from its four decimals, and its space share."""
    out = {}
    for k in plan.BUDGETS:
        rows = pub[k]
        test = [round(r["ls_test"] * N_TEST) for r in rows]
        space = [r["ls_space"] for r in rows]
        out[k] = {"test": test, "space": space,
                  "test_median": statistics.median(test),
                  "space_median": statistics.median(space)}
    return out


def inside(x, values) -> bool:
    return min(values) <= x <= max(values)


def both_inside(a: list, b: list) -> bool:
    """§0's label for two sets of draws: each median inside the other's range."""
    return inside(statistics.median(a), b) and inside(statistics.median(b), a)


def make_up(inst, sel, records) -> dict[str, Any]:
    truth, corpus = inst["truth"], inst["corpus"]
    by_truth: dict[str, int] = {}
    for i in sel:
        by_truth[truth[i]] = by_truth.get(truth[i], 0) + 1
    return {"conflict": sum(1 for i in sel if records[i]["outcome"] == "CONFLICT"),
            "impasse": sum(1 for i in sel if records[i]["outcome"] == "IMPASSE"),
            "keyword": sum(1 for i in sel if corpus[i].has_security_keyword),
            "by_truth": dict(sorted(by_truth.items(), key=lambda kv: -kv[1]))}


def draws(results: dict, k: int, field: str) -> list:
    return [results[f"random|{k}|{d}"][field] for d in range(plan.DRAWS)]


def verdicts(results: dict, comp: dict) -> list[dict[str, Any]]:
    e50 = draws(results, 50, "test")
    e251 = draws(results, 251, "test")
    s50 = draws(results, 50, "space_share")
    m50, m251 = statistics.median(e50), statistics.median(e251)
    sm50 = statistics.median(s50)
    crowded = results["crowded|50"]["test"]
    return [
        {"row": "J-a", "statistic": "test split 0: random escalations at 50, the median",
         "value": m50, "draws": e50, "line": plan.J_A_LINE,
         "holds": m50 >= plan.J_A_LINE, "thin": inside(plan.J_A_LINE, e50)},
        {"row": "J-b", "statistic": "the same, against random arrivals at 50",
         "value": m50, "draws": e50, "line": plan.J_B_LINE,
         "comparator_draws": comp[50]["test"],
         "holds": m50 > plan.J_B_LINE, "thin": both_inside(e50, comp[50]["test"])},
        {"row": "J-c", "statistic": "test split 0: random escalations at 251, against "
                                    "random arrivals at 251",
         "value": m251, "draws": e251, "line": plan.J_C_LINE,
         "comparator_draws": comp[251]["test"],
         "holds": m251 < plan.J_C_LINE, "thin": both_inside(e251, comp[251]["test"])},
        {"row": "J-d", "statistic": "test split 0: the 50 most crowded escalations, "
                                    "against J-a's median",
         "value": crowded, "line": m50,
         "holds": crowded > m50, "thin": inside(crowded, e50)},
        {"row": "J-e", "statistic": "space: random escalations at 50, the median share "
                                    "at four decimals, against random arrivals' 0.3993",
         "value": sm50, "draws": s50, "line": plan.J_E_LINE,
         "comparator_draws": comp[50]["space"],
         "holds": sm50 < plan.J_E_LINE, "thin": both_inside(s50, comp[50]["space"])},
    ]


def curve(results: dict, comp: dict) -> dict[str, Any]:
    """Each selection's test count and share of the gain, at every budget."""
    gain = plan.FULL - plan.ARRIVAL

    def share(x):
        return round((x - plan.ARRIVAL) / gain, 4)

    out = {}
    for k in plan.BUDGETS:
        m = statistics.median(draws(results, k, "test"))
        out[k] = {
            "random_escalations": {"median": m, "share": share(m)},
            "arrival": {"test": results[f"arrival|{k}"]["test"],
                        "share": share(results[f"arrival|{k}"]["test"])},
            "crowded": {"test": results[f"crowded|{k}"]["test"],
                        "share": share(results[f"crowded|{k}"]["test"])},
            "random_arrivals": {"median": comp[k]["test_median"],
                                "share": share(comp[k]["test_median"])},
        }
    out["all"] = {"test": results["all"]["test"], "share": share(results["all"]["test"])}
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if not dry:
        gate = plan.refuse_unsigned("escalations/score.py writes nothing")
    t0 = time.time()
    print("=" * 78)
    print("PLAN_ESCALATIONS.md — A REVIEWER'S LABELS AT THE ESCALATIONS")
    print("=" * 78)
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the checks ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    inst = I.instance()
    tr, _te = I.halves(inst)
    escs = selections.escalations(tr)
    sels = selections.selections(escs, I.matching(inst))
    records = {r["idx"]: r for r in json.loads(plan.RUNG1.read_text())["records"]}
    results = {}
    for name, sel in sels.items():
        results[name] = I.read(inst, sel) | {"make_up": make_up(inst, sel, records)}
        print(f"  {name:<16} {results[name]['test']:>4} of {N_TEST}   "
              f"space {results[name]['space_share']:.4f}")
    comp = comparators(gates.published_rows())
    rows = verdicts(results, comp)
    for r in rows:
        print(f"  {r['row']}: {'holds' if r['holds'] else 'REFUTED'}"
              f"{', thin' if r['thin'] else ''}  {r['value']} against {r['line']}")

    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, draws=plan.DRAWS,
                            draw_seed=plan.DRAW_SEED, budgets=list(plan.BUDGETS)),
        "what": "rung 3's search labelled with the truth at sets of rung 1's "
                "escalations, against the audit's random draws at the same budgets",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": "PRE-REGISTERED: §0 signed before any figure here existed",
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, "
                   "134,400 points; every count against the truth; space figures "
                   "compared at four decimals",
        "gates": {"J-g1": checks.jg1, "J-g2": checks.jg2, "J-g3": checks.jg3,
                  "J-g4": checks.jg4},
        "rows": {r["row"]: r for r in rows},
        "selections": {name: {"cases": sel} for name, sel in sels.items()},
        "results": results,
        "random_arrivals": comp,
        "curve": curve(results, comp),
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
