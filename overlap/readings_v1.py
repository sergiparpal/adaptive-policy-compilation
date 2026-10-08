"""
WHAT V1'S OVERLAP IS MADE OF. `overlap/readings.py` found that the one v2e run
under `O-a`'s line was under it through one broad rule. `O-a`'s baseline is v1,
`PLAN_REUSE.md`'s three runs, at 0.3226, 0.4839 and 0.3333. This reads those
three bases the same way, so that the comparison is between like and like.
POST-RUN.

--------------------------------------------------------------------------
WHAT IT READS, per run
--------------------------------------------------------------------------
`overlap/readings.py`'s reading, called and not copied: the births replayed in
order with their `O` and `S`, the earlier rule in the most `O`s, `O-a`'s share
as if that rule met nothing, breadth, attributes and timing. And one thing v1
adds: **what each rule was born on**, an impasse or a CONFLICT, read off the
loop's record of the case that bore it. v1 answered a CONFLICT with a rule, so
a third of its births or more came on one.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is `O-g2`'s**: per run, its share of births with an empty `O`
     is the one §0 of `PLAN_OVERLAP.md` declares for v1, to four decimals.
  2. **The bases are `structure.json`'s**: per run, as many rules as its
     profile.
  3. **The births on a CONFLICT are the loop's**: per run, as many as the
     CONFLICTs its record counts, since every v1 escalation bore a rule.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **By construction, every birth on a CONFLICT has a non-empty `O`.** The
     ticket was matched by rules of at least two queues, the rule born on it
     matches it, so it meets at least one rule of a queue not its own.
  2. **v1's overlap is not one rule's breadth.** Without each run's top rule,
     the median of v1's three `O-a` shares stays at or below 0.50. The births on
     a CONFLICT, 30, 5 and 12, meet the rules in conflict, which are not one
     rule, and in run 1 they alone are nearly half the base.
  3. **v1's top rules are the keyword's.** In every run the top rule sends
     tickets to `SECURITY_INCIDENT` and conditions on the security keyword, as
     47 of v1's 50 installed edges did.

**What the drafter had seen**: `FINDINGS_REUSE.md`, its reading of these three
bases included, and `structure.json`; `FINDINGS_EDGES.md`; `FINDINGS_OVERLAP.md`,
whose baselines include v1's `O-a` counts, 20 of 62, 15 of 31 and 14 of 42, and
whose POST-RUN sections include the v2e reading this one mirrors; and the three
records' escalation and CONFLICT counts. Not seen: any v1 rule's conditions,
its size, or which rules are in which `O`. **The second clause is the bet**, and
the drafter gives it about even odds: run 2, with five CONFLICTs, needs only one
more birth alone to cross the line.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN, AND LABELLED SO
--------------------------------------------------------------------------
**The births on an impasse, apart.** The first run showed v1's run 1 overlapping
through its 30 births on a CONFLICT, which meet rules of another queue by
construction, while v2e's three runs bore no rule on a CONFLICT at all. So `O-a`
compares a protocol that wrote rules on CONFLICTs with one that did not. This
block reads v1's births on an impasse alone, with and without the top rule, and
checks against the records that every v2e birth came on an impasse. It was
written after the first run, by someone who had read it; the record comes from
a second run, which reproduced every figure of the first. Nothing in it is a bet.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `overlap/readings.py`'s reading existed, with the
expectation above written before this one and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  PYTHONHASHSEED=0 python3 -m overlap.readings_v1
"""

from __future__ import annotations

import json
import statistics
import sys
from typing import Any

from harness.provenance import describe, environment
from rung2.engine2 import Space

from . import gates, plan
from . import readings as rd

READ_PATH = plan.OUT / "readings_v1.json"
SECURITY = "SECURITY_INCIDENT"
KEYWORD = "has_security_keyword"
PROVENANCE = (
    "POST-RUN: asked for after overlap/readings.py's reading existed. The "
    "expectation in the module's docstring was written before this reading and "
    "committed before it ran. Not a signed row; no verdict moves.")


def read_run(record: dict, space: Space) -> dict[str, Any]:
    """`overlap/readings.py`'s reading of one base, with what each rule was born
    on."""
    got = rd.read_run(record, space)
    outcome = {row["idx"]: row["outcome"] for row in record["records"]}
    for b in got["births"]:
        b["born_on"] = outcome[b["born_at"]]
    on_conflict = [b for b in got["births"] if b["born_on"] == "CONFLICT"]
    got["on_conflict"] = {"births": len(on_conflict),
                          "with_o": sum(1 for b in on_conflict if b["O"])}
    return got


def on_impasse(got: dict) -> dict[str, Any]:
    """The births on an impasse alone: how many met no earlier rule of another
    queue, with and without the run's top rule."""
    births = [b for b in got["births"] if b["born_on"] != "CONFLICT"]
    top = got["top"]["rule_id"] if got["top"] else None
    n = len(births)
    alone = sum(1 for b in births if not b["O"])
    alone_without = sum(1 for b in births if not [x for x in b["O"] if x != top])
    return {"births": n, "alone": alone, "alone_without_top": alone_without,
            "share": alone / n if n else None,
            "share_without_top": alone_without / n if n else None}


def v2e_births_on_conflict(rep: int) -> dict[str, int]:
    """How many of a v2e run's rules were born on a CONFLICT, off its record."""
    record = gates.load(plan.run_path(rep))
    outcome = {row["idx"]: row["outcome"] for row in record["records"]}
    on = [r for r in record["rules"] if outcome[r["born_at"]] == "CONFLICT"]
    return {"births": len(record["rules"]), "on_conflict": len(on)}


def check(structure: dict, records: dict[int, dict], runs: dict[int, dict]) -> list[dict]:
    out = []
    for k, (rep, got) in enumerate(runs.items()):
        share = round(got["o_a"], 4)
        out.append({"gate": 1, "rep": rep, "what": "the replay is O-g2's",
                    "measured": share, "declared": plan.DECLARED_O_A["v1"][k],
                    "passes": share == plan.DECLARED_O_A["v1"][k]})
        rules = structure["profiles"][f"reuse_r{rep}"]["rules"]
        out.append({"gate": 2, "rep": rep, "what": "the bases are structure.json's",
                    "measured": len(got["births"]), "published": rules,
                    "passes": len(got["births"]) == rules})
        conflicts = records[rep]["metrics"]["conflicts"]
        out.append({"gate": 3, "rep": rep, "what": "the births on a CONFLICT are the loop's",
                    "measured": got["on_conflict"]["births"], "published": conflicts,
                    "passes": got["on_conflict"]["births"] == conflicts})
    return out


def read_expectation(runs: dict[int, dict]) -> list[dict]:
    without = [r["o_a_without_top"] for r in runs.values()]
    median = statistics.median(without)

    def keyword_rule(top) -> bool:
        return (top is not None and top["action"] == SECURITY
                and any(c[0] == KEYWORD for c in top["conditions"]))

    return [
        {"clause": "by construction", "what": "every birth on a CONFLICT has a non-empty O",
         "reading": {rep: [r["on_conflict"]["with_o"], r["on_conflict"]["births"]]
                     for rep, r in runs.items()},
         "holds": all(r["on_conflict"]["with_o"] == r["on_conflict"]["births"]
                      for r in runs.values())},
        {"clause": 2, "what": "without each top rule, v1's median O-a is at most 0.50",
         "reading": {"per_run": without, "median": median},
         "holds": median <= plan.O_A_MAX_ALONE},
        {"clause": 3, "what": "every v1 top rule is SECURITY_INCIDENT on the keyword",
         "reading": {rep: None if r["top"] is None else [r["top"]["rule_id"], r["top"]["action"]]
                     for rep, r in runs.items()},
         "holds": all(keyword_rule(r["top"]) for r in runs.values())},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"overlap/readings_v1.py writes {READ_PATH}")
    structure = json.loads(plan.BASELINE_STRUCTURE.read_text())
    space = Space()
    records = {rep: gates.load(plan.v1_path(rep)) for rep in plan.BASELINE_REPS}
    runs = {rep: read_run(records[rep], space) for rep in records}
    checked = check(structure, records, runs)
    for g in checked:
        print(f"  gate {g['gate']} run {g['rep']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    READ_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"records": [str(plan.v1_path(rep)) for rep in plan.BASELINE_REPS]},
        "surface": "births, overlap and shares read over the exhaustive space",
        "gates": checked,
        "runs": {str(rep): r for rep, r in runs.items()},
        "expectation": read_expectation(runs),
        "added_after_the_first_run": {
            "what": "v1's births on an impasse alone, with and without each run's "
                    "top rule; and v2e's births on a CONFLICT, off its records",
            "provenance": "Written after this module's first run, by someone who had "
                          "read it. The record comes from a second run, which "
                          "reproduced every figure of the first. Not a bet.",
            "v1_on_impasse": {str(rep): on_impasse(r) for rep, r in runs.items()},
            "v2e_births_on_conflict": {str(rep): v2e_births_on_conflict(rep)
                                       for rep in range(1, plan.REPS + 1)},
        },
    }, indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
