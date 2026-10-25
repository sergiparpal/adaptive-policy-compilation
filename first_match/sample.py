"""
Stage A of `PLAN_FIRST_MATCH.md`: the design and the references. **Free, and
gated.**

It writes `results_first_match/sample.json`:

  * `FM-g1` to `FM-g3`, the blocking checks, run first;
  * **the design**: every prompt of the three arms with its ticket, digest and
    the decisions it serves; the decisions; the three sessions' orders at
    `ORDER_SEED`; every arm's system prompt, whole;
  * **the references**, computed here after the signature: for every decision,
    the identifiers of the rules its ticket matches, in the list's order, and
    its runner-up, read from level 3's frozen text; and `qᴬ`,
    `PLAN_QUEUE_ALONE.md`'s plain-arm answers on every plain prompt, with the
    provider that served each.

**It produces nothing adjudicable**, and it runs after §0 is signed: a record
of this plan written before the signature would be a figure that existed
before its band (§10 of the plan).

    PYTHONHASHSEED=0 python3 -m first_match.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m first_match.sample
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from queue_alone import orders as qorders
from queue_alone import rules as qrules

from . import gates, plan, population, prompts


def references(design: population.Design,
               before: dict[int, dict[str, dict]]) -> dict[str, Any]:
    """Which rules match each decision's ticket, and `PLAN_QUEUE_ALONE.md`'s
    plain answers by prompt. `before` holds that plan's two passes."""
    rs = qrules.rules()
    matches = {}
    for i, e in sorted(design.decisions.items()):
        hit = qrules.matching(e.prompt.case.as_dict(), rs)
        up = qorders.runner_up(hit)
        matches[i] = {"ticket": e.ticket, "matching": [r.id for r in hit],
                      "runner_up": up.id if up else None}
    q_before = {}
    for a in sorted(design.asks_of(prompts.PLAIN), key=lambda a: a.id):
        q_before[a.id] = [{"pass": k, "action": (row or {}).get("action"),
                           "served_by": (row or {}).get("served_by")}
                          for k in (1, 2) for row in (before[k].get(a.id),)]
    return {"matches": matches, "queue_alone_plain": q_before}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_FIRST_MATCH.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run FM-g1 to FM-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("first_match/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    design = checks.design
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(),
              "design": design.summary(),
              "system_prompts": {arm: {
                  "sha256": hashlib.sha256(prompts.system_prompt(arm).encode()).hexdigest(),
                  "text": prompts.system_prompt(arm)} for arm in prompts.ARMS},
              "settings": {arm: plan.settings(arm) for arm in prompts.ARMS},
              "references": references(design, gates.queue_alone_passes())}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
