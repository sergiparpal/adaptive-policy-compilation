"""
Stage C of `PLAN_AUTHORSHIP.md` — the four rows and the reported fifth, read
off Stage B's runs. Free.

WHAT EACH ROW READS (§0 and §10). Every final base is read whole, from case 0,
with `reuse/structure.py`'s instrument, as the baseline was:

  E-a  its share of nested pairs, `nested_share`. The runs refuse copies, so it
       compares with the baseline's nesting over distinct rules.
  E-b  subsumption alone over it, on the full corpus: silent error and coverage.
  E-c  over the exhaustive space, the share of the order's room its installed
       edges fill: (end to end with every installed edge − end to end of
       subsumption alone) / (hybrid bound − end to end of subsumption alone).
       The final engine is rebuilt as `authorship/gates.py` rebuilds the
       baseline's, which `E-g2` checked against `results_edges/score.json`.
  E-d  `contradice_subsuncion` verdicts, pooled over the runs.
  E-e  reported, outside every denominator: E-c on the corpus; E-a to E-c with
       each channel's edges alone; the loop's online figures beside the
       baseline's; calls, rounds, refusals and `finish_reason`; born rules that
       overlap nothing and overlap among distinct rules; declarations by verdict
       and channel; the two rare queues.

The median over runs adjudicates, each run's value beside it. **A share the
room leaves undefined in any run makes E-c unadjudicable**, and the record says
so rather than taking the median of what is left.

It refuses while the plan is unsigned and while a run is missing, and it runs
`E-g1` to `E-g3` before writing.

    python3 -m authorship.score     # writes results_authorship/score.json
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from typing import Any

from harness.domain import generate_corpus
from harness.dsl import Condition
from harness.provenance import describe, environment

from reuse import structure as st
from rung2.engine2 import EDGE_CONTRADICTS, Space
from rung3.order_search_ls import space_truth_masks

from . import gates, plan
from . import protocol as p

ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"
CHANNELS = {"all": None, "write": {p.WRITE}, "order": {p.ORDER_CHANNEL}}
ONLINE = ("reuse_rate", "silent_error_rate", "proposal_action_accuracy",
          "e2e_accuracy", "escalations", "conflicts", "n_rules")


def base_rules(record: dict) -> list[dict]:
    return [{k: r[k] for k in ("rule_id", "conditions", "action", "born_at")}
            for r in record["rules"]]


def distinct_overlap(rules: list[dict], space: Space) -> float | None:
    """Overlapping pairs over all pairs, among rules covering different tickets."""
    ext = {r["rule_id"]: space.extension([Condition(c["attr"], c["op"], c["value"])
                                          for c in r["conditions"]]) for r in rules}
    seen, distinct = set(), []
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        if ext[r["rule_id"]] not in seen:
            seen.add(ext[r["rule_id"]])
            distinct.append(r["rule_id"])
    n = len(distinct)
    pairs = n * (n - 1) // 2
    hit = sum(1 for i, a in enumerate(distinct) for b in distinct[i + 1:]
              if ext[a] & ext[b])
    return hit / pairs if pairs else None


def rare(record: dict, queue: str) -> dict[str, int]:
    rows = [r for r in record["records"] if r["truth"] == queue]
    decided = [r for r in rows if not r["escalated"] and r["outcome"] == "ACTION"]
    return {"cases": len(rows), "escalated": sum(r["escalated"] for r in rows),
            "decided": len(decided), "decided_right": sum(bool(r["correct"]) for r in decided)}


def score_run(record: dict, corpus, space: Space, tmask: dict[str, int]) -> dict[str, Any]:
    """Everything one run contributes: its share of each row, and E-e."""
    labels = gates.labels_of(record)
    rules = base_rules(record)
    profile = st.profile(rules, corpus, space, tmask)
    alone, bound = profile["subsumption"], profile["bounds"]["hibrido"]
    by_channel = {}
    for name, keep in CHANNELS.items():
        engine, problems = gates.rebuild_final(record, space, keep)
        sp, co = gates.on_space(engine, tmask, space.n), gates.on_corpus(engine, corpus, labels)
        by_channel[name] = {
            "space": {"e2e": sp["e2e"],
                      "share": gates.share(sp["e2e"], alone["space"]["e2e"], bound["space"])},
            "corpus": {"e2e": co["e2e"],
                       "share": gates.share(co["e2e"], alone["corpus"]["e2e"], bound["corpus"])},
            "reinstall_problems": problems}
    log = record.get("edge_log") or []
    chans = record.get("edge_channels") or [p.WRITE] * len(log)
    escalations = record.get("escalations") or []
    calls = [c for e in escalations for c in e["calls"]]
    born = [e for e in escalations if e["verdict"] == p.BORN]
    born_alone = sum(1 for e in born if not (e["calls"][-1].get("overlapped") or []))
    return {
        "rep": record.get("rep"),
        "E-a": profile["pairs"]["nested_share"],
        "E-b": {"silent_error": alone["corpus"]["silent_error"],
                "coverage": alone["corpus"]["coverage"]},
        "E-c": by_channel["all"]["space"]["share"],
        "E-d": sum(1 for _w, _l, why in log if why == EDGE_CONTRADICTS),
        "E-e": {
            "share_on_the_corpus": by_channel["all"]["corpus"]["share"],
            "by_channel": by_channel,
            "profile": profile,
            "online": {k: record["metrics"].get(k) for k in ONLINE},
            "calls": len(calls),
            "rounds_per_escalation": dict(Counter(len(e["calls"]) for e in escalations)),
            "verdicts": dict(Counter(e["verdict"] for e in escalations)),
            "finish_reasons": dict(Counter(str(c["finish_reason"]) for c in calls)),
            "born": len(born),
            "born_overlapping_nothing": born_alone,
            "distinct_overlap": distinct_overlap(rules, space),
            "declarations": dict(Counter(f"{ch}:{why}" for (_w, _l, why), ch
                                         in zip(log, chans))),
            ONCALL: rare(record, ONCALL),
            SECURITY: rare(record, SECURITY),
        },
    }


def median_or_none(values: list) -> float | None:
    """The median, or `None` if any run's value is undefined."""
    return None if any(v is None for v in values) else statistics.median(values)


def verdicts(runs: list[dict]) -> dict[str, Any]:
    """The four rows, each on the median over the runs, against §0's lines."""
    a = median_or_none([r["E-a"] for r in runs])
    b_err = median_or_none([r["E-b"]["silent_error"] for r in runs])
    b_cov = median_or_none([r["E-b"]["coverage"] for r in runs])
    c = median_or_none([r["E-c"] for r in runs])
    d = sum(r["E-d"] for r in runs)

    def row(name, reading, holds, line):
        return {"row": name, "reading": reading, "line": line,
                "per_run": [r[name] for r in runs],
                "holds": holds, "unadjudicable": holds is None}

    return {
        "E-a": row("E-a", a, None if a is None else a >= plan.E_A_MIN_NESTED,
                   f">= {plan.E_A_MIN_NESTED}"),
        "E-b": row("E-b", {"silent_error": b_err, "coverage": b_cov},
                   None if b_err is None or b_cov is None else
                   (b_err <= plan.E_B_MAX_SILENT and b_cov >= plan.E_B_MIN_COVERAGE),
                   f"silent error <= {plan.E_B_MAX_SILENT} and coverage >= "
                   f"{plan.E_B_MIN_COVERAGE}"),
        "E-c": row("E-c", c, None if c is None else c >= plan.E_C_MIN_FILL,
                   f">= {plan.E_C_MIN_FILL}"),
        "E-d": {"row": "E-d", "reading": d, "line": f">= {plan.E_D_MIN_CONTRADICTIONS}",
                "per_run": [r["E-d"] for r in runs],
                "holds": d >= plan.E_D_MIN_CONTRADICTIONS, "unadjudicable": False},
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
    plan.refuse_unsigned(f"authorship/score.py writes {plan.SCORE_PATH}")
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
    rows = verdicts(runs)
    for name, v in rows.items():
        state = ("unadjudicable" if v["unadjudicable"] else
                 "holds" if v["holds"] else "refuted")
        print(f"  {name}  {state:<14} {v['reading']}  (line {v['line']}; per run "
              f"{v['per_run']})")

    plan.SCORE_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "surfaces": {"E-a": "pairs, no surface", "E-b": "the full corpus, 2,000 cases",
                     "E-c": "the exhaustive space, 134,400 points",
                     "E-d": "the runs' edge verdicts, pooled"},
        "read_whole": "every final base read from case 0, as reuse/structure.py read "
                      "the baseline",
        "gates": checks.summary(),
        "verdicts": rows,
        "runs": runs,
    }), indent=2, default=str) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
