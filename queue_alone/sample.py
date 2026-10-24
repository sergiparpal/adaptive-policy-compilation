"""
Stage A of `PLAN_QUEUE_ALONE.md`: the design and the free readout. **Free, and
gated.**

It writes `results_queue_alone/sample.json`:

  * `QA-g1` to `QA-g3`, the blocking checks, run first;
  * **the design**: every prompt of the three arms with its level, ticket,
    digest and the decisions it serves; the decisions; the three sessions'
    orders at `ORDER_SEED`; every arm's system prompt at every level, whole;
  * **`QA-g`'s reference columns**, computed here for the first time, at level
    3: how many of the 29 rules each decision's ticket matches, where its first
    match lies, and whether a lower match gives another queue; two copiers
    scored on the truth, one answering the queue of the matching rule with the
    most conditions and one the commonest queue among the matching rules; and
    `PLAN_APPLY.md`'s ticket and screen arms in §5.6's classes.

**It produces nothing adjudicable**, and it runs after §0 is signed so that none
of its figures can inform a band: where the first match lies, and how
`PLAN_APPLY.md`'s answers fall in §5.6's classes, is what `QA-c`'s and `QA-e`'s
bands would have been drawn from (§10 of the plan).

    PYTHONHASHSEED=0 python3 -m queue_alone.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m queue_alone.sample
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from . import gates, plan, population, prompts, rules
from .score import apply_answers, apply_records, frac, labels


def references(design: population.Design, lab: dict[str, dict[str, Any]],
               before: dict[str, dict[str, tuple]]) -> dict[str, Any]:
    rs = rules.rules()
    depth: Counter = Counter()
    count: Counter = Counter()
    lower_other = most = commonest = n = 0
    classes = {arm: Counter() for arm in before}
    for i, e in sorted(design.decisions.items()):
        if e.level != 3:
            continue
        ticket = e.prompt.case.as_dict()
        hit = rules.matching(ticket, rs)
        y = lab[i]["y"]
        n += 1
        count[len(hit)] += 1
        depth[rs.index(hit[0]) + 1] += 1
        lower_other += int(any(r.queue != hit[0].queue for r in hit[1:]))
        most += int(rules.most_conditions_queue(ticket, rs) == y)
        queues = Counter(r.queue for r in hit)
        top = max(queues.values())
        commonest += int(next(r.queue for r in hit if queues[r.queue] == top) == y)
        for arm, by in before.items():
            for a in by.get(i, (None, None)):
                if a is not None:
                    classes[arm][rules.classify(a, ticket, rs)] += 1
    return {"decisions_at_L3": n,
            "matching_rules": {str(k): v for k, v in sorted(count.items())},
            "first_match_at": {str(k): v for k, v in sorted(depth.items())},
            "a_lower_match_gives_another_queue": lower_other,
            "copiers": {"most_conditions": frac(Fraction(most, n)) if n else None,
                        "commonest_queue": frac(Fraction(commonest, n)) if n else None},
            "plan_apply_classes": {arm: dict(c) for arm, c in classes.items()}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_QUEUE_ALONE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run QA-g1 to QA-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("queue_alone/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    design = checks.design
    before = apply_answers(design, apply_records())
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(),
              "design": design.summary(),
              "system_prompts": {f"{arm} L{lv}": {
                  "sha256": hashlib.sha256(prompts.system_prompt(arm, lv).encode()).hexdigest(),
                  "text": prompts.system_prompt(arm, lv)}
                  for arm in prompts.ARMS for lv in plan.LEVELS},
              "references": references(design, labels(), before)}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
