"""
Stage A of `PLAN_PLACEMENT.md`: the references (§8). **Free, and gated**: it
refuses while §0 is unsigned, because what the gate protects is the order of
events, not money (§11 of the plan).

It records, after `PL-g1` to `PL-g3` have passed, §0's figures 1 to 8, each with
whether it came back as §0 declares it:

- 1. to 4. the drafting reading: the new round's list on v1b's twelve recorded
  runs, by run; by the draft's queue; the two rarest queues in
  `PLAN_CHANNEL.md`'s channel runs; and the breadth of drafts and births;
- 5. the hidden policy through v1c's path, beside v1b's;
- 6. the transcriber through both paths, under each of `PLAN_CHANNEL.md`'s draws
  and the smoke draws;
- 7. the schedule;
- 8. the bridge's tickets and its order of providers.

And what v1c leaves out on those paths, which decides nothing, the channel of
every run, and the texts' digests.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

    python3 -m placement.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m placement.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from reasoned_loop import protocol as p

from . import gates, plan, references


def references_record() -> dict[str, Any]:
    drafting = references.drafting_reading()
    hidden_v1c = references.hidden("v1c")
    hidden_v1c_figures = references.hidden_v1c_figures(hidden_v1c)
    v1b = references.hidden("v1b")
    transcriber = {}
    for name, got in references.transcribed().items():
        transcriber[name] = {"stream": got["stream"], "n": got["n"], "figures": got["figures"],
                             "as_declared": references.transcriber_as_declared(name, got["figures"])}
    bridge = references.bridge_reading()
    order = [list(x) for x in plan.schedule()]
    return {
        "drafting": {**drafting, "as_declared": references.drafting_as_declared(drafting)},
        "hidden": {"v1c": {**hidden_v1c_figures,
                           "as_declared": hidden_v1c_figures == plan.DECLARED["hidden_v1c"],
                           "installed": hidden_v1c["installed"]},
                   "v1b": {"born": v1b["born"], "declarations": v1b["declarations"],
                           "installed": v1b["installed"],
                           "space": [v1b["space"]["correct"], v1b["space"]["n"]],
                           "corpus": [v1b["corpus"]["correct"], v1b["corpus"]["n"]]}},
        "transcriber": transcriber,
        "left_out": references.left_out_decides_nothing(),
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "bridge": {**bridge, "as_declared": references.bridge_as_declared(bridge),
                   "tickets": plan.bridge_tickets(),
                   "asks": [list(x) for x in plan.bridge_asks()]},
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "streams": {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
                    for name in plan.STREAMS},
        "texts_sha16": p.digests(), "fingerprint": p.fingerprint(),
    }


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [f"drafting {k}" for k, v in refs["drafting"]["as_declared"].items() if not v]
    if not refs["hidden"]["v1c"]["as_declared"]:
        off.append("hidden v1c")
    off += [f"transcriber {name}" for name, v in refs["transcriber"].items()
            if not all(v["as_declared"].values())]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    off += [f"bridge {k}" for k, v in refs["bridge"]["as_declared"].items() if not v]
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_PLACEMENT.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run PL-g1 to PL-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("placement/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    refs = references_record()
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(), "references": refs}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\nfigures §0 declared that did not come back: {not_back(refs) or 'none'}")
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
