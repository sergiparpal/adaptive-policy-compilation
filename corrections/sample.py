"""
Stage A of `PLAN_CORRECTIONS.md`: the references (§8). **Free, and gated**: it
refuses while §0 is unsigned, because what the gate protects is the order of
events, not money (§11 of the plan).

It records, after `CR-g1` to `CR-g3` have passed, §0's figures 1 to 4, each with
whether it came back as §0 declares it:

- 1. in the six level-3 v1c runs of `PLAN_PLACEMENT.md` and `PLAN_WHOLE.md`, the
  escalations caused by a reported error whose first call named the case's true
  queue;
- 2. the same runs' escalations, reports and calls;
- 3. the arrivals that repeat an earlier ticket;
- 4. the schedule.

And the channel of every run, the streams, both arms' texts and fingerprints,
and the at-once asks' texts.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

**Its figures were seen before the signature**, and the record says so in its
`provenance` (`EXTERNAL_REVIEW.md` §3). Figures 1 to 3 were computed while
drafting, on 2026-11-12, before §0's lines were drawn. Figure 4 was computed
while completing the plan, on 2026-11-12, after them. None of them is a figure
of the runs this plan buys.

    python3 -m corrections.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m corrections.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from . import gates, plan, prompts, protocol

PROVENANCE = (
    "Figures 1 to 3 were computed while drafting, on 2026-11-12, from PLAN_PLACEMENT.md's "
    "and PLAN_WHOLE.md's records and the corpus, and seen before §0's lines were drawn. "
    "Figure 4 was computed while completing the plan, on 2026-11-12, after the lines and "
    "before the signature. This record recomputes all four and owns them. None of them is "
    "a figure of the runs this plan buys.")


def references_record() -> dict[str, Any]:
    drafting = gates.drafting_reading()
    order = [list(x) for x in plan.schedule()]
    return {
        "drafting": {**drafting,
                     "as_declared": {k: drafting[k] == plan.DECLARED[k] for k in drafting}},
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "streams": {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
                    for name in plan.STREAMS},
        "texts_sha16": {arm: protocol.digests(arm) for arm in plan.ARMS},
        "fingerprints": {arm: protocol.fingerprint(arm) for arm in plan.ARMS},
        "report_template": protocol.REPORT,
        "at_once": {"texts_sha16": prompts.digests(), "header": prompts.HEADER,
                    "checkpoints": list(plan.CHECKPOINTS),
                    "asks_per_checkpoint": plan.ASKS_PER_CHECKPOINT,
                    "prior_asks": plan.PRIOR_ASKS, "workers": plan.WORKERS,
                    "max_reasks": plan.MAX_REASKS, "settings": plan.at_once_settings()},
    }


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [f"drafting {k}" for k, v in refs["drafting"]["as_declared"].items() if not v]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_CORRECTIONS.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CR-g1 to CR-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("corrections/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    refs = references_record()
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
