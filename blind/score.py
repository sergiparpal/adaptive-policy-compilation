"""
Stage C of `PLAN_BLIND.md` — the five rows and the reported sixth, read off Stage
B's runs with the instrument `K-g2` checked on the baselines. Free.

WHAT EACH ROW READS (§0 and §10). Every final base is read whole, from case 0, and
every row where `has_security_keyword` is False:

  K-a  the share of born rules, keyword rules left apart, that overlap no rule
       born before them with a different queue on the half of the space without
       the keyword. Median over the runs. **A run with no such birth counts at
       1.00** (§0).
  K-b  the installed edges declared at a birth on an impasse, between rules of
       different queues, neither a keyword rule, that have a strict better rule
       over their shared region on the half of the space without the keyword:
       the share whose declared winner is that rule, **each older rule counted
       once**, pooled over the runs. **With fewer than `plan.MIN_UNITS` older
       rules the row is unadjudicable** (§0).
  K-c  K-b's reading less the same reading for the rule rung 3's Stage C
       hierarchy names, on the same pairs and units, and unadjudicable with K-b.
  K-d  `O-b`'s share of the order's room over the half of the space without the
       keyword. **The median over the runs whose room is not zero**, a run
       without room named and left out, the median of two their mean; with
       fewer than two runs with room the row is unadjudicable (§0).
  K-e  K-b's edges read over the corpus cases without the keyword, counted as
       they arrive, clustered the same way, with its own count of units.
  K-f  reported, outside every denominator: §0's list.

It refuses while the plan is unsigned and while a run is missing, and it runs
`K-g1` to `K-g3` before writing.

    PYTHONHASHSEED=0 python3 -m blind.score     # writes results_blind/score.json
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from authorship import gates as egates
from authorship import protocol as e
from authorship.refused import matched_sets
from authorship.score import ONCALL, ONLINE, SECURITY, rare
from reuse import structure as st
from rung2.engine2 import Space
from rung3.order_search_ls import space_truth_masks

from . import gates, plan, rows
from . import protocol as p

CHANNELS = {"all": None, "write": {e.WRITE}, "order": {e.ORDER_CHANNEL}}


def keyword_edges(row: dict) -> bool:
    """The edges K-b leaves out for the keyword, read beside it (K-f)."""
    return (row["channel"] == e.WRITE and row["younger_born_on"] == rows.IMPASSE
            and not row["same_queue"] and row["keyword"])


def score_run(record: dict, corpus, space: Space, tmask: dict[str, int], outside: int,
              cases_out: list[int]) -> dict[str, Any]:
    """Everything one run contributes: its share of K-a and K-d, its edges for
    K-b, K-c and K-e, and K-f."""
    engine, problems = egates.rebuild_final(record, space)
    labels = egates.labels_of(record)
    truth = [t for t, _ in labels]
    b_out = rows.births_outside(record["rules"], space, outside)
    b_full = rows.births_outside(record["rules"], space, space.full)
    escalations = record.get("escalations") or []
    born = [x for x in escalations if x["verdict"] == e.BORN]
    born_without_o = sum(1 for x in born if not (x["calls"][0].get("overlapped") or []))
    calls = [c for x in escalations for c in x["calls"]]
    placements = [x for x in escalations if any(c["round"] == 1 for c in x["calls"])]
    edge_rows = rows.edge_rows(record, engine, tmask, outside, matched_sets(engine, corpus),
                               truth, cases_out)
    fills = {name: {"space_outside": rows.fill(record, space, tmask, outside, keep),
                    "space_full": rows.fill(record, space, tmask, space.full, keep)}
             for name, keep in CHANNELS.items()}
    return {
        "rep": record.get("rep"),
        "K-a": rows.k_a(record["rules"], space, outside),
        "K-d": fills["all"]["space_outside"]["share"],
        "edge_rows": edge_rows,
        "K-f": {
            "reinstall_problems": problems,
            "births_outside": b_out,
            "births_full": b_full,
            "o_a": rows.k_a(record["rules"], space, space.full),
            "born_without_o_recorded": born_without_o,
            "the_two_readings_agree": born_without_o == b_full["alone_outside"],
            "births_by_escalation": dict(Counter(x["kind"] for x in born)),
            "fills": fills,
            "fill_on_the_corpus_outside": rows.fill_on_corpus(record, space, corpus,
                                                              labels, cases_out),
            "online": {k: record["metrics"].get(k) for k in ONLINE},
            "calls": len(calls),
            "rounds_per_escalation": dict(Counter(len(x["calls"]) for x in escalations)),
            "verdicts": dict(Counter(x["verdict"] for x in escalations)),
            "verdicts_after_a_placement": dict(Counter(x["verdict"] for x in placements)),
            "listed_sizes": dict(Counter(len(x["listed"]) for x in placements)),
            "finish_reasons": dict(Counter(str(c["finish_reason"]) for c in calls)),
            "declarations": dict(Counter(why for _w, _l, why in record.get("edge_log") or [])),
            "order_answers": sum(1 for x in escalations if x["verdict"] == e.ORDER),
            "conflicts": sum(1 for x in escalations if x["kind"] == "CONFLICT"),
            "changed": sum(1 for x in escalations if x["verdict"] == p.CHANGED),
            ONCALL: rare(record, ONCALL),
            SECURITY: rare(record, SECURITY),
        },
    }


def direction_rows(runs: list[dict]) -> dict[str, Any]:
    """K-b, K-c and K-e, pooled over the runs, with what K-f reads beside them."""
    er = [r["edge_rows"] for r in runs]
    space_ = rows.comparators(er, "space_out")
    corpus_ = rows.comparators(er, "corpus_out")
    return {"space": space_, "corpus": corpus_,
            "split": rows.split_by_queue_pair(er, "space_out"),
            "keyword_edges_full_space": rows.direction(er, "space_full", keep=keyword_edges),
            "o_c_full_space": rows.direction(er, "space_full", keep=rows.across_queues)}


def verdicts(runs: list[dict], d: dict[str, Any]) -> dict[str, Any]:
    """The five rows against §0's lines, each with every run's value beside it."""
    a = statistics.median(r["K-a"] for r in runs)
    kb = d["space"]["declared"]
    ranking = d["space"]["stage_c_ranking"]
    ke = d["corpus"]["declared"]
    kd = rows.median_with_room([r["K-d"] for r in runs], plan.K_D_MIN_RUNS_WITH_ROOM)
    b_short = kb["units"] < plan.MIN_UNITS
    e_short = ke["units"] < plan.MIN_UNITS
    margin = None if b_short else kb["reading"] - ranking["reading"]
    return {
        "K-a": {"row": "K-a", "reading": a, "line": f"<= {plan.K_A_MAX_ALONE}",
                "per_run": [r["K-a"] for r in runs],
                "holds": a <= plan.K_A_MAX_ALONE, "unadjudicable": False},
        "K-b": {"row": "K-b", "reading": None if b_short else kb["reading"],
                "line": f">= {plan.K_B_MIN_DIRECTION}, on at least {plan.MIN_UNITS} units",
                "units": kb["units"], "hits": kb["hits"], "strict": kb["strict"],
                "holds": None if b_short else kb["reading"] >= plan.K_B_MIN_DIRECTION,
                "unadjudicable": b_short},
        "K-c": {"row": "K-c", "reading": margin,
                "line": f">= {plan.K_C_MIN_MARGIN}, on K-b's units",
                "declared": kb["reading"], "ranking": ranking["reading"],
                "holds": None if b_short else margin >= plan.K_C_MIN_MARGIN,
                "unadjudicable": b_short},
        "K-d": {"row": "K-d", "reading": kd["reading"],
                "line": f">= {plan.K_D_MIN_FILL}, on at least "
                        f"{plan.K_D_MIN_RUNS_WITH_ROOM} runs with room",
                "per_run": [r["K-d"] for r in runs],
                "runs_with_room": kd["runs_with_room"], "left_out": kd["left_out"],
                "holds": None if kd["unadjudicable"] else kd["reading"] >= plan.K_D_MIN_FILL,
                "unadjudicable": kd["unadjudicable"]},
        "K-e": {"row": "K-e", "reading": None if e_short else ke["reading"],
                "line": f">= {plan.K_E_MIN_DIRECTION}, on at least {plan.MIN_UNITS} units",
                "units": ke["units"], "hits": ke["hits"], "strict": ke["strict"],
                "holds": None if e_short else ke["reading"] >= plan.K_E_MIN_DIRECTION,
                "unadjudicable": e_short},
    }


def load_runs() -> tuple[list[dict], list[str]]:
    found, missing = [], []
    for rep in range(1, plan.REPS + 1):
        path = plan.run_path(rep)
        if path.exists():
            found.append(json.loads(path.read_text()))
        else:
            missing.append(str(path))
    return found, missing


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"blind/score.py writes {plan.SCORE_PATH}")
    found, missing = load_runs()
    if missing:
        sys.exit(f"\nREFUSED: Stage B is incomplete — missing {', '.join(missing)}\n")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")

    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    tmask = space_truth_masks(space)
    outside = rows.outside_mask(space)
    cases_out = rows.outside_cases(corpus)
    runs = [score_run(r, corpus, space, tmask, outside, cases_out) for r in found]
    d = direction_rows(runs)
    rows_ = verdicts(runs, d)
    for name, x in rows_.items():
        state = ("unadjudicable" if x["unadjudicable"] else
                 "holds" if x["holds"] else "refuted")
        print(f"  {name}  {state:<14} {x['reading']}  (line {x['line']})")

    plan.SCORE_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "surfaces": {"K-a": "births, overlap read over the half of the space without "
                            "the keyword",
                     "K-b": "the half of the space without the keyword, 67,200 points, "
                            "over each edge's shared region",
                     "K-c": "as K-b",
                     "K-d": "the half of the space without the keyword",
                     "K-e": "the 1,929 corpus cases without the keyword, as they arrive"},
        "read_whole": "every final base read from case 0",
        "gates": checks.summary(),
        "verdicts": rows_,
        "directions": d,
        "runs": runs,
        "baselines": checks.kg2["measured"],
    }), indent=2, default=str) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
