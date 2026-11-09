"""
Stage A of `PLAN_WHOLE.md`: the references (§8). **Free, and gated**: it refuses
while §0 is unsigned, because what the gate protects is the order of events, not
money (§11 of the plan).

It records, after `WR-g1` to `WR-g3` have passed, §0's figures 1 to 5, each with
whether it came back as §0 declares it:

- 1. `whole(r)` on `PLAN_PLACEMENT.md`'s six runs, and v1c's median;
- 2. the lists v1c would have sent a draft of the governing rule's region whole,
  on v1c's three bases rebuilt before each recorded escalation, beside the lists
  sent, with the rarest queue's escalations apart;
- 3. the transcriber's recall of `ONCALL_ESCALATION` under v1c and each of
  `PLAN_CHANNEL.md`'s draws;
- 4. the schedule;
- 5. off the text's 29 regions alone, the lower rules that contain each listed
  rule and those it crosses.

And the transcriber's figures under every draw, the channel of every run, the
streams, and both arms' texts and fingerprints.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

**Its figures were seen before the signature**, and the record says so in its
`provenance` (`EXTERNAL_REVIEW.md` §3): figures 1 to 4 while drafting, on
2026-11-08, before §0's lines were drawn, and figure 5 while completing the plan,
on 2026-11-09, after them. None of them is a figure of the runs this plan buys.

    python3 -m whole.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m whole.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from . import gates, plan, protocol, references

PROVENANCE = (
    "Figures 1 to 4 were computed while drafting, on 2026-11-08, from PLAN_PLACEMENT.md's "
    "records, and seen before §0's lines were drawn. Figure 5 was computed from level 3's "
    "text while completing the plan, on 2026-11-09, after the lines and before the "
    "signature. This record recomputes all five and owns them. None of them is a figure of "
    "the runs this plan buys.")


def references_record() -> dict[str, Any]:
    drafting = references.drafting_reading()
    order = [list(x) for x in plan.schedule()]
    return {
        "drafting": {**drafting, "as_declared": references.drafting_as_declared(drafting)},
        "transcriber": references.transcriber_figures(),
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "streams": {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
                    for name in plan.STREAMS},
        "texts_sha16": {arm: protocol.digests(arm) for arm in plan.ARMS},
        "fingerprints": {arm: protocol.fingerprint(arm) for arm in plan.ARMS},
        "base_texts": dict(protocol.BASES),
    }


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [f"drafting {k}" for k, v in refs["drafting"]["as_declared"].items() if not v]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_WHOLE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run WR-g1 to WR-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("whole/sample.py writes Stage A")
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
