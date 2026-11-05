"""
Stage A of `PLAN_CHANNEL.md`: the references (§8). **Free, and gated**: it
refuses while §0 is unsigned, because what the gate protects is the order of
events, not money (§11 of the plan).

It records, after `CH-g1` to `CH-g3` have passed, §0's figures 1 to 6 and 8,
each with whether it came back as §0 declares it:

- 1. the rare queues' tickets, off the labels the triggers read;
- 2. the space by true queue, and the points `H05` governs;
- 3. each channel run's draws: their seed strings and digests, their reportable
  cases, and their reportable rare tickets by governing rule;
- 4. and 5. the transcriber under every draw and trigger (§5.4): each channel
  run's draws, the error trigger, and the smoke run's draws over its 30 cases,
  which §0 does not declare;
- 6. the schedule;
- 8. the supply each run's draws leave, by governing rule, beside
  `PLAN_REASONED_LOOP.md`'s error runs' escalations and its impasse runs' wrong
  decisions that stood.

And the hidden policy through v1b's path, and the texts' digests.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

    python3 -m channel.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m channel.sample
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
    tx = references.transcribed()
    out: dict[str, Any] = {"transcriber": {}}
    for name, got in tx.items():
        out["transcriber"][name] = {"stream": got["stream"], "n": got["n"],
                                    "figures": got["figures"],
                                    "as_declared": references.as_declared(name, got["figures"])}
    smoke = references.transcriber(plan.SMOKE_ARM)
    out["transcriber"]["smoke"] = {"stream": smoke["stream"], "n": smoke["n"],
                                   "figures": smoke["figures"], "as_declared": None}
    rare, space = references.rare_tickets(), references.space_by_queue()
    h05 = references.governed_points("H05")
    draws = references.draws_by_run()
    supply = references.supply(tx["e"])
    hidden = {k: v for k, v in references.hidden_through_path().items() if k != "engine"}
    order = [list(x) for x in plan.schedule()]
    out.update({
        "rare": {**rare, "as_declared": rare == plan.DECLARED["rare"]},
        "space_by_queue": {"points": space,
                           "as_declared": space == plan.DECLARED["space_by_queue"]},
        "h05_points": {"points": h05, "as_declared": h05 == plan.DECLARED["h05_points"]},
        "draws": {"runs": draws, "as_declared": references.draws_as_declared(draws),
                  "streams": {name: {"seed": plan.draw_seed(name),
                                     "sha16": plan.draws_digest(name)}
                              for name in plan.STREAMS}},
        "supply": {**supply, "as_declared": references.supply_as_declared(supply)},
        "hidden": hidden,
        "schedule": order, "schedule_as_declared": order == plan.DECLARED["schedule"],
        "channels": {plan.tag(a, r): plan.channel_of(a, r) for a, r in plan.schedule()},
        "texts_sha16": p.digests(), "fingerprint": p.fingerprint(),
    })
    return out


def not_back(refs: dict[str, Any]) -> list[str]:
    """Every figure §0 declared that did not come back as declared."""
    off = [k for k in ("rare", "space_by_queue", "h05_points")
           if refs[k]["as_declared"] is False]
    off += [f"draws {k}" for k, v in refs["draws"]["as_declared"].items() if not v]
    off += [f"supply {k}" for k, v in refs["supply"]["as_declared"].items() if not v]
    off += [f"transcriber {name}" for name, v in refs["transcriber"].items()
            if v["as_declared"] is not None and not all(v["as_declared"].values())]
    if not refs["schedule_as_declared"]:
        off.append("schedule")
    return off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_CHANNEL.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CH-g1 to CH-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("channel/sample.py writes Stage A")
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
