"""
THE STAGE of `PLAN_SPOTCHECK.md` §8: a random audit of the decisions, beside
the escalations, scored.

It refuses while §0 is unsigned, before it builds or measures anything; no flag
skips that. `--dry-run` runs `N-g1` to `N-g3` and writes nothing. Then, in this
order:

  1. **The blocking checks**, `spotcheck/gates.py`.
  2. **The selections** of `spotcheck/selections.py`: at 10, 50, 100 and 251
     audited decisions and for each of five nested draws, the escalations with
     the audited decisions, and the audited decisions alone.
  3. **One order per set**, `escalations/instrument.py`'s search labelled with
     the truth there, scored on test split 0, over the space and on the four
     rare queues.
  4. **The endpoints**, the escalations alone and the whole train half, as
     `N-g1` reproduced them; and the comparators of the audit alone, read from
     their records, never re-drawn.
  5. **`N-a` to `N-e`**, each with §0's label, and the readings of `N-f`.

Surfaces: corpus test split 0, 995 cases, and the exhaustive space, 134,400
points, every count against the truth.

PROVENANCE: PRE-REGISTERED. §0 was signed before any figure here existed; the
gate is what says so.

    python3 -m spotcheck.score --dry-run           # N-g1..N-g3, blocking; writes nothing
    PYTHONHASHSEED=0 python3 -m spotcheck.score    # N-a to N-e, and the readings of N-f
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from collections import Counter
from typing import Any

from escalations import gates as esc_gates
from escalations import instrument as I
from escalations import score as esc_score
from escalations.selections import escalations
from harness.provenance import describe, environment

from . import gates, plan, selections

N_TEST = 995
median = statistics.median


def inside(x, values) -> bool:
    return min(values) <= x <= max(values)


def draws(results: dict, arm: str, k: int, field: str) -> list:
    return [results[f"{arm}|{k}|{d}"][field] for d in range(plan.DRAWS)]


def t3_draws(results: dict, arm: str, k: int) -> list[int]:
    return [results[f"{arm}|{k}|{d}"]["per_class"]["T3_ENGINEERING"]["right"]
            for d in range(plan.DRAWS)]


def verdicts(results: dict) -> list[dict[str, Any]]:
    m50 = draws(results, "mix", 50, "test")
    m251 = draws(results, "mix", 251, "test")
    t50 = t3_draws(results, "mix", 50)
    s50 = draws(results, "mix", 50, "space")
    return [
        {"row": "N-a", "statistic": "test split 0: the escalations and 50 audited "
                                    "decisions, the median of five orders",
         "value": median(m50), "draws": m50, "line": plan.N_A_LINE,
         "holds": median(m50) > plan.N_A_LINE, "thin": inside(plan.N_A_LINE, m50)},
        {"row": "N-b", "statistic": "the same, against half the gap",
         "value": median(m50), "draws": m50, "line": plan.N_B_LINE,
         "holds": median(m50) >= plan.N_B_LINE, "thin": inside(plan.N_B_LINE, m50)},
        {"row": "N-c", "statistic": "test split 0's 57 T3_ENGINEERING cases: the "
                                    "same five orders, the median count right",
         "value": median(t50), "draws": t50, "line": plan.N_C_LINE,
         "holds": median(t50) >= plan.N_C_LINE, "thin": inside(plan.N_C_LINE, t50)},
        {"row": "N-d", "statistic": "space: the same five orders, the median count "
                                    "right of 134,400",
         "value": median(s50), "draws": s50, "line": plan.N_D_LINE,
         "holds": median(s50) > plan.N_D_LINE, "thin": inside(plan.N_D_LINE, s50)},
        {"row": "N-e", "statistic": "test split 0: the escalations and 251 audited "
                                    "decisions, the median of five orders",
         "value": median(m251), "draws": m251, "line": plan.N_E_LINE,
         "holds": median(m251) >= plan.N_E_LINE, "thin": inside(plan.N_E_LINE, m251)},
    ]


def make_up(inst, sel, decs: set, recs: dict) -> dict[str, Any]:
    """The audited decisions in a set: their true queues, keyword tickets, and
    how many rung 1 got wrong."""
    truth, corpus = inst["truth"], inst["corpus"]
    audited = [i for i in sel if i in decs]
    return {"audited": len(audited),
            "wrong": sum(1 for i in audited if not recs[i]["correct"]),
            "keyword": sum(1 for i in audited if corpus[i].has_security_keyword),
            "by_truth": dict(Counter(truth[i] for i in audited).most_common())}


def beside(results: dict, esc_results: dict, comp: dict) -> dict[int, Any]:
    """The audit alone at each budget, beside random escalations and random
    arrivals at the same budget; and, paired by draw, what the escalations add
    to the audit."""
    out = {}
    for k in plan.BUDGETS:
        alone_t = draws(results, "audit", k, "test")
        alone_s = draws(results, "audit", k, "space_share")
        esc_t = [esc_results[f"random|{k}|{d}"]["test"] for d in range(plan.DRAWS)]
        esc_s = [esc_results[f"random|{k}|{d}"]["space_share"] for d in range(plan.DRAWS)]
        mix_t = draws(results, "mix", k, "test")
        out[k] = {
            "audit_alone": {"test": alone_t, "test_median": median(alone_t),
                            "space": alone_s, "space_median": median(alone_s)},
            "random_escalations": {"test": esc_t, "test_median": median(esc_t),
                                   "space": esc_s, "space_median": median(esc_s)},
            "random_arrivals": {"test": comp[k]["test"],
                                "test_median": comp[k]["test_median"],
                                "space": comp[k]["space"],
                                "space_median": comp[k]["space_median"]},
            "escalations_add": [m - a for m, a in zip(mix_t, alone_t)],
        }
    return out


def curve(results: dict) -> dict[Any, Any]:
    """Each arm's median at every budget, the audited sets as a share of the gap
    and both as a share of the gain."""
    gap = plan.FULL - plan.ESC_ALL["test"]
    gain = plan.FULL - plan.ARRIVAL
    out: dict[Any, Any] = {}
    for k in plan.BUDGETS:
        m = median(draws(results, "mix", k, "test"))
        a = median(draws(results, "audit", k, "test"))
        out[k] = {"mix": {"median": m,
                          "share_of_gap": round((m - plan.ESC_ALL["test"]) / gap, 4),
                          "share_of_gain": round((m - plan.ARRIVAL) / gain, 4)},
                  "audit_alone": {"median": a,
                                  "share_of_gain": round((a - plan.ARRIVAL) / gain, 4)}}
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if not dry:
        gate = plan.refuse_unsigned("spotcheck/score.py writes nothing")
    t0 = time.time()
    print("=" * 78)
    print("PLAN_SPOTCHECK.md — A RANDOM AUDIT OF THE DECISIONS, BESIDE THE ESCALATIONS")
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
    escs = escalations(tr)
    decs = selections.decisions(tr)
    sels = selections.selections(escs, decs)
    recs = gates.records()
    dset = set(decs)
    results = {}
    for name, sel in sels.items():
        results[name] = I.read(inst, sel) | {"make_up": make_up(inst, sel, dset, recs)}
        print(f"  {name:<14} {results[name]['test']:>4} of {N_TEST}   "
              f"space {results[name]['space']:>6}   "
              f"T3 {results[name]['per_class']['T3_ENGINEERING']['right']}")
    rows = verdicts(results)
    for r in rows:
        print(f"  {r['row']}: {'holds' if r['holds'] else 'REFUTED'}"
              f"{', thin' if r['thin'] else ''}  {r['value']} against {r['line']}")

    esc_results = json.loads(plan.ESCALATIONS.read_text())["results"]
    comp = esc_score.comparators(esc_gates.published_rows())
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, draws=plan.DRAWS,
                            audit_seed=plan.AUDIT_SEED, budgets=list(plan.BUDGETS)),
        "what": "rung 3's search labelled with the truth of every escalation and a "
                "random audit of the decisions, and of the audit alone, between the "
                "escalations alone and the whole train half",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": "PRE-REGISTERED: §0 signed before any figure here existed",
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, "
                   "134,400 points; every count against the truth",
        "gates": {"N-g1": checks.ng1, "N-g2": checks.ng2, "N-g3": checks.ng3,
                  "N-g4": checks.ng4},
        "rows": {r["row"]: r for r in rows},
        "endpoints": {"escalations": checks.ng1["reads"]["escalations"],
                      "full": checks.ng1["reads"]["full"]},
        "selections": {name: {"cases": sel} for name, sel in sels.items()},
        "results": results,
        "beside": beside(results, esc_results, comp),
        "curve": curve(results),
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
