"""
Stage A of `PLAN_APPLY.md`: the design and the free readout. **Free, and gated.**

It writes `results_apply/sample.json`:

  * `X-g1` to `X-g3`, the blocking checks, run first;
  * **the design**: every decision with its level, run, case, screen kind,
    ticket, shown ids and plurality; every ask of both arms with its digest and
    the decisions it serves; the three sessions' orders at `ORDER_SEED`;
  * **`X-g`'s reference columns**, computed here for the first time: the loop's
    own accuracy on the decisions by level, run, screen kind and true queue;
    how often the plurality is the true queue and how often it is the loop's
    answer; two copiers scored on the truth, one answering the plurality and one
    the first action shown; the decisions' class mix.

**It produces nothing adjudicable**, and it runs after §0 is signed so that none
of its figures can inform a band: the plurality's share of true queues is what
`X-b`'s and `X-d`'s bands would have been drawn from (§10 of the plan).

    PYTHONHASHSEED=0 python3 -m apply.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m apply.sample
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from . import gates, plan, population, prompts
from .score import frac, labels


def references(design: population.Design, lab: dict[str, dict[str, Any]]) -> dict[str, Any]:
    cells: dict[str, Counter] = defaultdict(Counter)
    mix: dict[int, Counter] = defaultdict(Counter)
    for i, e in sorted(design.decisions.items()):
        a = design.asks[population.screen_ask_id(i)]
        y, loop = lab[i]["y"], lab[i]["loop"]
        p, first = prompts.plurality(a), prompts.first_shown(a)
        mix[e.level][y] += 1
        for key in (f"L{e.level}", f"L{e.level}r{e.run}", f"L{e.level} {e.prompt.screen}",
                    f"L{e.level} {y}"):
            c = cells[key]
            c["decisions"] += 1
            c["loop_right"] += int(loop == y)
            c["plurality_is_truth"] += int(p == y)
            c["plurality_is_the_loops_answer"] += int(p == loop)
            c["first_shown_is_truth"] += int(first == y)
    out = {}
    for key, c in sorted(cells.items()):
        n = c["decisions"]
        out[key] = {"decisions": n, **{k: frac(Fraction(v, n)) for k, v in c.items()
                                       if k != "decisions"}}
    return {"cells": out,
            "class_mix": {str(lv): dict(sorted(m.items())) for lv, m in sorted(mix.items())},
            "shared_with_plan_screen": plan.SHARED_WITH_SCREEN}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_APPLY.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run X-g1 to X-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("apply/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    design = checks.design
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(),
              "design": design.summary(),
              "system_prompts": {lv: {"sha256": hashlib.sha256(
                                          prompts.system_prompt(lv).encode()).hexdigest(),
                                      "text": prompts.system_prompt(lv)}
                                 for lv in plan.LEVELS},
              "references": references(design, labels())}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
