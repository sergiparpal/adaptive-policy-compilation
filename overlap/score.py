"""
Stage C of `PLAN_OVERLAP.md` — the three rows and the reported fourth, read off
Stage B's runs with the instrument `O-g2` checked on the baselines. Free.

WHAT EACH ROW READS (§0 and §10). Every final base is read whole, from case 0:

  O-a  the share of born rules that overlap no rule born before them with a
       different queue, from the births replayed in order and checked against
       the `O` each birth recorded. Median over the runs. **A run in which no
       rule is born counts at 1.00**, the most partitioned a run can be (§0).
  O-b  `E-c`'s share of the order's room over the exhaustive space, with every
       installed edge. **The median over the runs whose room is not zero**: a
       run without room is named and left out, the median of two runs is their
       mean, and with fewer than two runs with room the row is unadjudicable
       (§0, `rows.o_b_reading`).
  O-c  `W-b`'s reading of the installed edges between rules of different queues,
       over the exhaustive space, **pooled over the runs**. With no such edge
       that has a strict better rule, in any run, the row is unadjudicable (§0).
  O-d  reported, outside every denominator: O-b on the corpus and pooled; O-b
       and O-c with each channel's edges alone; the loop's online figures beside
       both baselines'; calls, rounds, refusals and `finish_reason`; born rules
       that overlap nothing at all, and overlap among distinct rules; `S`'s
       sizes; declarations by verdict, queue and channel; every
       `contradice_subsuncion` read against the truth as `authorship/refused.py`
       reads it; CONFLICTs and order answers; the two rare queues.

It refuses while the plan is unsigned and while a run is missing, and it runs
`O-g1` to `O-g3` before writing.

    PYTHONHASHSEED=0 python3 -m overlap.score     # writes results_overlap/score.json
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
from authorship import refused
from authorship.score import ONCALL, ONLINE, SECURITY, base_rules, distinct_overlap, rare
from reuse import structure as st
from rung2.engine2 import EDGE_CONTRADICTS, Space
from rung3.order_search_ls import space_truth_masks

from . import gates, plan, rows

CHANNELS = {"all": None, "write": {e.WRITE}, "order": {e.ORDER_CHANNEL}}


def of_channel(record: dict, keep: set[str] | None) -> dict:
    """The record with the edges of the channels in `keep` only."""
    if keep is None:
        return record
    log = record.get("edge_log") or []
    chans = record.get("edge_channels") or [e.WRITE] * len(log)
    pairs = [(x, ch) for x, ch in zip(log, chans) if ch in keep]
    return dict(record, edge_log=[x for x, _ in pairs], edge_channels=[ch for _, ch in pairs])


def score_run(record: dict, corpus, space: Space, tmask: dict[str, int]) -> dict[str, Any]:
    """Everything one run contributes: its share of each row, and O-d."""
    rules = base_rules(record)
    b = rows.births(rules, space)
    o_a = b["alone_from_other_queues"] / b["born"] if b["born"] else 1.0
    escalations = record.get("escalations") or []
    born = [x for x in escalations if x["verdict"] == e.BORN]
    born_without_o = sum(1 for x in born if not (x["calls"][-1].get("overlapped") or []))
    profile = st.profile(rules, corpus, space, tmask)
    by_channel = {}
    for name, keep in CHANNELS.items():
        sub = of_channel(record, keep)
        engine, _ = egates.rebuild_final(sub, space)
        by_channel[name] = {"fill": rows.fill(sub, corpus, space, tmask, profile=profile),
                            "direction": rows.direction(sub, engine, tmask)}
    engine, _ = egates.rebuild_final(record, space)
    log = record.get("edge_log") or []
    chans = record.get("edge_channels") or [e.WRITE] * len(log)
    rules_by_id = {r["rule_id"]: r for r in record["rules"]}
    truth = [r["truth"] for r in record["records"]]
    sets = refused.matched_sets(engine, corpus)
    contradictions = [refused.read_pair(w, l, ch, rules_by_id, engine.ext, tmask, sets, truth)
                      for (w, l, why), ch in zip(log, chans) if why == EDGE_CONTRADICTS]
    calls = [c for x in escalations for c in x["calls"]]
    return {
        "rep": record.get("rep"),
        "O-a": o_a,
        "O-b": by_channel["all"]["fill"]["space"]["share"],
        "O-c": by_channel["all"]["direction"],
        "O-d": {
            "births": b,
            "born_without_o_recorded": born_without_o,
            "the_two_readings_agree": born_without_o == b["alone_from_other_queues"],
            "o_b_on_the_corpus": by_channel["all"]["fill"]["corpus"]["share"],
            "by_channel": by_channel,
            "profile": profile,
            "online": {k: record["metrics"].get(k) for k in ONLINE},
            "calls": len(calls),
            "rounds_per_escalation": dict(Counter(len(x["calls"]) for x in escalations)),
            "verdicts": dict(Counter(x["verdict"] for x in escalations)),
            "finish_reasons": dict(Counter(str(c["finish_reason"]) for c in calls)),
            "distinct_overlap": distinct_overlap(rules, space),
            "same_queue_sizes": dict(Counter(len(c["same_queue"]) for c in calls
                                             if "same_queue" in c)),
            "declarations": rows.by_queue(record, engine),
            "declarations_by_channel": dict(Counter(f"{ch}:{why}" for (_w, _l, why), ch
                                                    in zip(log, chans))),
            "contradictions": contradictions,
            "order_answers": sum(1 for x in escalations if x["verdict"] == e.ORDER),
            ONCALL: rare(record, ONCALL),
            SECURITY: rare(record, SECURITY),
        },
    }


def verdicts(runs: list[dict]) -> dict[str, Any]:
    """The three rows against §0's lines, each with every run's value beside it."""
    a = statistics.median(r["O-a"] for r in runs)
    b = rows.o_b_reading([r["O-b"] for r in runs])
    c = rows.o_c_reading([r["O-c"] for r in runs])
    return {
        "O-a": {"row": "O-a", "reading": a, "line": f"<= {plan.O_A_MAX_ALONE}",
                "per_run": [r["O-a"] for r in runs],
                "holds": a <= plan.O_A_MAX_ALONE, "unadjudicable": False},
        "O-b": {"row": "O-b", "reading": b["reading"],
                "line": f">= {plan.O_B_MIN_FILL}, on at least "
                        f"{plan.O_B_MIN_RUNS_WITH_ROOM} runs with room",
                "per_run": [r["O-b"] for r in runs],
                "runs_with_room": b["runs_with_room"], "left_out": b["left_out"],
                "holds": None if b["unadjudicable"] else b["reading"] >= plan.O_B_MIN_FILL,
                "unadjudicable": b["unadjudicable"]},
        "O-c": {"row": "O-c", "reading": c["reading"], "line": f">= {plan.O_C_MIN_DIRECTION}",
                "hits": c["hits"], "strict": c["strict"],
                "per_run": [(r["O-c"]["hits"], r["O-c"]["hits"] + r["O-c"]["misses"])
                            for r in runs],
                "holds": None if c["reading"] is None else c["reading"] >= plan.O_C_MIN_DIRECTION,
                "unadjudicable": c["reading"] is None},
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
    plan.refuse_unsigned(f"overlap/score.py writes {plan.SCORE_PATH}")
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
    runs = [score_run(r, corpus, space, tmask) for r in found]
    rows_ = verdicts(runs)
    for name, x in rows_.items():
        state = ("unadjudicable" if x["unadjudicable"] else
                 "holds" if x["holds"] else "refuted")
        print(f"  {name}  {state:<14} {x['reading']}  (line {x['line']}; per run "
              f"{x['per_run']})")
    pooled = rows.pooled_fill([r["O-d"]["by_channel"]["all"]["fill"] for r in runs])

    plan.SCORE_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "surfaces": {"O-a": "births, overlap read over the exhaustive space",
                     "O-b": "the exhaustive space, 134,400 points",
                     "O-c": "the exhaustive space, over each edge's shared region"},
        "read_whole": "every final base read from case 0",
        "gates": checks.summary(),
        "verdicts": rows_,
        "o_b_pooled_reported": pooled,
        "runs": runs,
        "baselines": checks.og2["measured"],
    }), indent=2, default=str) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
