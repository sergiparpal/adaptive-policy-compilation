"""
Stage A of `PLAN_RANKED.md`: the references (§8). **Free, and gated**: it
refuses while §0 is unsigned, because what the gate protects is the order of
events, not money (§11 of the plan).

It records, after `RK-g1` to `RK-g3` have passed, §0's figures 2 to 7, each with
whether it came back as §0 declares it:

- 2. the two designs set aside, and rung 2's engine, under the transcriber and
  each draw;
- 3. `PLAN_CORRECTIONS.md`'s three L runs' final bases, replayed under each
  design;
- 4. arm K's engine on those runs after every birth: the whole curve, its peak,
  and the recall of two queues at the end;
- 5. the conflicts those runs asked about: what the ranking of the votes so far
  decides there, and what the proposer's first call named;
- 6. the arrivals at which the policy's own rules exercise one pair of queues;
- 7. the schedule.

And Step 0's figures, the channel of every run, the streams, the texts' digests,
each arm's engine and the at-once asks' constants.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

**Its figures were seen before the signature**, and the record says so in its
`provenance` (`EXTERNAL_REVIEW.md` §3). None of them is a figure of the runs this
plan buys: figures 3 to 5 are replays of another plan's runs.

    python3 -m ranked.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m ranked.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from corrections import plan as cr_plan
from corrections import prompts as cr_prompts
from corrections import protocol as cr_protocol
from manual import instrument as MI

from . import gates, plan
from . import reading as R
from . import run as rrun

PROVENANCE = (
    "Figure 6 was counted while drafting, on 2026-11-17, for a row the plan no longer has. "
    "Figure 2 was computed on 2026-11-17, when the first draft's engine was held to the "
    "transcriber and failed, and figures 3 to 5 on 2026-11-17 and 2026-11-18, when the "
    "designs were read on PLAN_CORRECTIONS.md's L runs: all before §0's lines were drawn "
    "again for the engine the plan signs, and before the signature. Figure 7 was computed "
    "while drafting. This record recomputes all six and owns them. Figures 3 to 5 are "
    "replays of PLAN_CORRECTIONS.md's runs, whose rules were written under rung 2's "
    "engine. None of them is a figure of the runs this plan buys.")


def closed_curves() -> dict[str, Any]:
    """Figure 4, whole: each closed L run after every birth, under rung 2's
    engine, which is the run, and under arm K's, which is a replay."""
    space, truth = MI.space(), MI.space_truth()
    out = {}
    for rep, tag in enumerate(gates.L_TAGS, start=1):
        got = R.as_it_went(gates.closed(rep), space, truth)
        curve = got["curve"]
        out[tag] = {"births": len(curve), "points": space.n,
                    "rung2": R.summary(curve, "rung2"), "ranked": R.summary(curve, "ranked"),
                    "final_ranking": list(got["tally"].ranking),
                    "curve": [{k: p[k] for k in ("born_at", "rule_id", "ranking", "tied",
                                                 "conflict", "rung2", "ranked")}
                              for p in curve]}
    return out


def references_record(checks: gates.Checks) -> dict[str, Any]:
    drafting = gates.drafting_reading()
    order = [list(x) for x in plan.schedule()]
    return {
        "drafting": {**drafting,
                     "as_declared": {k: drafting[k] == plan.DECLARED[k] for k in plan.DECLARED}},
        "closed_runs": closed_curves(),
        "step_zero": checks.g3["step_zero"],
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "streams": {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
                    for name in plan.STREAMS},
        "texts_sha16": cr_protocol.digests(plan.TEXTS_OF),
        "fingerprint": cr_protocol.fingerprint(plan.TEXTS_OF),
        "engines": {a: {"engine": plan.ENGINE[a], "rule": rrun.engine_rule(a)}
                    for a in plan.ARMS},
        "report_template": cr_protocol.REPORT,
        "at_once": {"texts_sha16": cr_prompts.digests(), "header": cr_prompts.HEADER,
                    "checkpoints": list(plan.CHECKPOINTS),
                    "asks_per_checkpoint": plan.ASKS_PER_CHECKPOINT,
                    "prior_asks": plan.PRIOR_ASKS, "workers": plan.WORKERS,
                    "max_reasks": plan.MAX_REASKS, "settings": plan.at_once_settings(),
                    "sessions": list(plan.sessions())},
        "closed_runs_from": {tag: str(cr_plan.run_path(cr_plan.LABELLED, rep))
                             for rep, tag in enumerate(gates.L_TAGS, start=1)},
    }


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [f"drafting {k}" for k, v in refs["drafting"]["as_declared"].items() if not v]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_RANKED.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run RK-g1 to RK-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("ranked/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    refs = references_record(checks)
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "provenance": PROVENANCE, "signature": gate, "gates": checks.summary(),
              "references": refs}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\nfigures §0 declared that did not come back: {not_back(refs) or 'none'}")
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
