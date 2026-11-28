"""
Stage A of `PLAN_IMPASSE.md`: the references (§8). **Free, and gated**: it refuses
while §0 is unsigned, because what the gate protects is the order of events, not
money (§11 of the plan).

It records, after `IM-g1` to `IM-g3` have passed, §0's figures 1 to 8, each with
whether it came back as §0 declares it:

- 1. the escalations by cause on `PLAN_PLACEMENT.md`'s three v1c runs and
  `PLAN_WHOLE.md`'s six runs;
- 2. on the same runs, the first-call drafts classed whole by cause;
- 3. at the impasses, by the governing rule's group, and the impasses v1c met at
  each default's tickets;
- 4. what the round did with the whole drafts at impasses;
- 5. where each v1c base lost its points, by the causes its rules' tickets met;
- 6. how `H01`'s first ticket, case 44, met each base;
- 7. the schedule;
- 8. the groups, off the text's 29 regions alone.

And the transcriber's figures under every draw, the channel of every run, the
streams, and both arms' texts and fingerprints.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

**Its figures were seen before the signature**, and the record says so in its
`provenance` (`EXTERNAL_REVIEW.md` §3): all eight while drafting, on 2026-11-28,
before §0's lines were drawn. None of them is a figure of the runs this plan buys.

    python3 -m impasse.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m impasse.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from reasoned_loop import protocol as p

from . import gates, plan, protocol, references

PROVENANCE = (
    "Figures 1 to 8 were computed while drafting, on 2026-11-28, from PLAN_PLACEMENT.md's "
    "and PLAN_WHOLE.md's records and from level 3's text, and seen before §0's lines were "
    "drawn. This record recomputes all eight and owns them. None of them is a figure of the "
    "runs this plan buys.")


def references_record() -> dict[str, Any]:
    drafting = references.drafting_reading()
    order = [list(x) for x in plan.schedule()]
    return {
        "drafting": {**drafting, "as_declared": references.drafting_as_declared(drafting)},
        "groups": references.groups(),
        "transcriber": references.transcriber_figures(),
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "streams": {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
                    for name in plan.STREAMS},
        "texts_sha16": {arm: protocol.digests(arm) for arm in plan.ARMS},
        "fingerprints": {arm: protocol.fingerprint(arm) for arm in plan.ARMS},
        "base_text": p.BLIND_BASE,
        "notice_text": protocol.NOTICE_BASE,
    }


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [f"drafting {k}" for k, v in refs["drafting"]["as_declared"].items() if not v]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_IMPASSE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run IM-g1 to IM-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("impasse/sample.py writes Stage A")
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
