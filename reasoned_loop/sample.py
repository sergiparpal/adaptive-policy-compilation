"""
Stage A of `PLAN_REASONED_LOOP.md`: the references (§8). **Free, and gated**: it
refuses while §0 is unsigned, because what the gate protects is the order of
events, not money (§11 of the plan).

It records, after `RL-g1` to `RL-g3` have passed:

- the transcriber under both triggers, with every figure §0 declares, and
  whether each came back;
- the hidden policy through v1b's path;
- the `H29` tickets and the rare queues' tickets, off the labels the error
  trigger reads;
- the rules `PLAN_REASONED_RULE.md`'s two rule arms wrote, by governing rule;
- `PLAN_MANUAL.md`'s three level-3 runs through this plan's instrument;
- the schedule, and the texts' digests.

**It produces nothing adjudicable.** A figure §0 declared that does not come back
is recorded so, and the findings carry an erratum to §0, dated; no band moves.

    python3 -m reasoned_loop.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m reasoned_loop.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from blind import rows as brows

from . import gates, plan, references, score
from . import protocol as p


def direction_of(record: dict) -> dict[str, Any]:
    """RL-e's and RL-f's statistics on one run of the transcriber: what a placer
    that follows the list exactly reads, and what the Stage C ranking reads on
    the same pairs."""
    rows = [score.read_run(json.loads(json.dumps(record, default=str)))["edges"]]
    d = score.direction(rows)
    k = score.direction(rows, predict=brows.stage_c_names)
    out = {"units": d["units"]}
    if d["units"]:
        out.update(hits=d["hits"], strict=d["strict"], reading=str(d["reading"]),
                   ranking=str(k["reading"]))
    return out


def references_record() -> dict[str, Any]:
    out: dict[str, Any] = {"transcriber": {}}
    for arm in plan.ARMS:
        got = references.transcriber_figures(arm)
        figs = got["figures"]
        direction = direction_of(got["record"])
        out["transcriber"][arm] = {
            "figures": figs, "direction": direction,
            "as_declared": {**references.as_declared(arm, figs),
                            "direction": direction == plan.DECLARED[
                                "transcriber_direction"][arm]}}
    hidden = {k: v for k, v in references.hidden_through_path().items() if k != "engine"}
    h29, rare, written = (references.h29_tickets(), references.rare_tickets(),
                          references.rules_written())
    out.update({
        "hidden": {**hidden, "as_declared": {k: hidden[k] if k != "installed"
                                             else len(hidden[k]) for k in plan.DECLARED["hidden"]}
                   == plan.DECLARED["hidden"]},
        "h29": {**h29, "as_declared": h29 == plan.DECLARED["h29"]},
        "rare": {**rare, "as_declared": rare == plan.DECLARED["rare"]},
        "rules_written": {**written, "as_declared": (
            written["rows"] == plan.DECLARED["rules_written"]
            and written["catch_all_without_reasoning"]
            == plan.DECLARED["catch_all_without_reasoning"])},
        "manual_level_3": references.manual_level_3(),
        "schedule": [list(x) for x in plan.schedule()],
        "texts_sha16": p.digests(), "fingerprint": p.fingerprint(),
    })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_REASONED_LOOP.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run RL-g1 to RL-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("reasoned_loop/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    refs = references_record()
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(), "references": refs}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    off = [k for k, v in refs.items() if isinstance(v, dict) and v.get("as_declared") is False]
    off += [f"transcriber {a}" for a, v in refs["transcriber"].items()
            if not all(v["as_declared"].values())]
    print(f"\nfigures §0 declared that did not come back: {off or 'none'}")
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
