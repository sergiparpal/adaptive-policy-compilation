"""
WHAT SEPARATES A RUN THAT OVERLAPS FROM ONE THAT PARTITIONS. Under v2e, run 1's
births overlapped rules of other queues far more often than runs 2 and 3's
(`O-a`: 0.2545, against 0.8049 and 1.0000). This reads the three final bases for
what separates them. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
`O-a` counts the births that overlap no earlier rule of another queue. A low
share can mean a proposer that writes rules across the others' regions, or one
broad rule that every later birth happens to meet. The first is the overlap
`PLAN_OVERLAP.md` asked for; the second is one rule's breadth. The records tell
them apart: each birth's `O` names the rules it met.

--------------------------------------------------------------------------
WHAT IT READS, per run
--------------------------------------------------------------------------
From the births replayed in order, the replay `O-a` reads, checked against the
`O` each birth recorded:

  births      each rule: when it was born, its queue, how many conditions it
              has and on which attributes, the share of the exhaustive space it
              covers, and its `O` and `S` at birth.
  top         the earlier rule that appears in the most `O`s: which, when born,
              its queue and conditions, its share of the space, and in how many
              of the run's births with a non-empty `O` it appears.
  without     `O-a`'s share recomputed as if the top rule met nothing: every
              birth reads its `O` without it. The top rule is still a birth.
  breadth     the median share of the space a rule covers, and the mean number
              of conditions per rule.
  attributes  how many rules condition on each attribute.
  timing      births, and births with a non-empty `O`, by quarter of the corpus.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is `O-a`'s**: per run, its births with an empty `O` number what
     `score.json` gives.
  2. **It is the loop's**: every born rule's last call recorded the `O` the
     replay gives it, rule for rule and in order.

It refuses to write if either fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **One rule carries run 1's overlap.** Run 1's top rule is in the `O` of at
     least half of its births with a non-empty `O`.
  2. **Without it, run 1 partitions like the others.** Its `O-a` share without
     the top rule is above 0.50, the line `O-a` was signed at.
  3. **Run 3's rules are the broadest.** Its median share of the space is the
     largest of the three runs.
  4. **The runs that partitioned tile the space on one attribute.** In runs 2
     and 3, the attribute most rules condition on is conditioned on by at least
     three rules in four.

**What the drafter had seen**: `FINDINGS_OVERLAP.md`, which names `R0017`, born
at case 19 in run 1, and `R0024`, born at case 44 in run 2, and the edges each
won; and `score.json`'s per-run births, profiles and declarations. Run 1's 50
edges won by `R0017` already say that many later births met it, so the first
clause is close to known, and so is the third, given that run 3's eleven rules
leave subsumption deciding nearly the whole space. **The second and the fourth
are the bets.** Not seen: any rule's conditions beyond those two, its size, or
the attributes the rules use.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_OVERLAP.md`'s verdicts existed, with the
expectation above written before the reading and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  PYTHONHASHSEED=0 python3 -m overlap.readings
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from typing import Any

from harness.provenance import describe, environment
from rung2.engine2 import Space

from . import gates, plan, rows

READ_PATH = plan.OUT / "readings.json"
QUARTER = plan.N // 4
PROVENANCE = (
    "POST-RUN: asked for after PLAN_OVERLAP.md's verdicts existed. The expectation "
    "in the module's docstring was written before the reading and committed before "
    "it ran. Not a signed row; no verdict moves.")


def replay(rules: list[dict], space: Space) -> list[dict]:
    """The births in order, each with its `O` and `S` against the rules born
    before it, as §5.2 computes them."""
    out: list[dict] = []
    seen: list[tuple[str, int, Any]] = []
    for r in sorted(rules, key=lambda r: (r["born_at"], r["rule_id"])):
        ext = rows.ext_of(r, space)
        out.append({
            "rule_id": r["rule_id"], "born_at": r["born_at"], "action": r["action"],
            "conditions": [(c["attr"], c["op"], c["value"]) for c in r["conditions"]],
            "attributes": sorted({c["attr"] for c in r["conditions"]}),
            "share": ext.bit_count() / space.n,
            "O": [rid for rid, e, a in seen if e & ext and a != r["action"]],
            "S": [rid for rid, e, a in seen if e & ext and a == r["action"]],
        })
        seen.append((r["rule_id"], ext, r["action"]))
    return out


def top_rule(births: list[dict]) -> dict[str, Any] | None:
    """The earlier rule in the most `O`s, the first born among equals."""
    count = Counter(rid for b in births for rid in b["O"])
    if not count:
        return None
    order = {b["rule_id"]: i for i, b in enumerate(births)}
    rid = min(count, key=lambda x: (-count[x], order[x]))
    me = births[order[rid]]
    return {"rule_id": rid, "born_at": me["born_at"], "action": me["action"],
            "conditions": me["conditions"], "share": me["share"],
            "in_o_of": count[rid],
            "births_with_o": sum(1 for b in births if b["O"])}


def o_a_without(births: list[dict], rid: str | None) -> float | None:
    """`O-a`'s share as if `rid` met nothing."""
    if not births:
        return None
    return sum(1 for b in births if not [x for x in b["O"] if x != rid]) / len(births)


def read_run(record: dict, space: Space) -> dict[str, Any]:
    births = replay(record["rules"], space)
    top = top_rule(births)
    attrs = Counter(a for b in births for a in b["attributes"])
    return {
        "births": births,
        "o_a": o_a_without(births, None),
        "top": top,
        "o_a_without_top": o_a_without(births, top["rule_id"] if top else None),
        "breadth": {"median_share": statistics.median(b["share"] for b in births),
                    "mean_conditions": statistics.fmean(len(b["conditions"])
                                                        for b in births)},
        "attributes": dict(attrs.most_common()),
        "timing": {"births": dict(sorted(Counter(b["born_at"] // QUARTER
                                                 for b in births).items())),
                   "births_with_o": dict(sorted(Counter(b["born_at"] // QUARTER
                                                        for b in births
                                                        if b["O"]).items()))},
    }


def recorded_o(record: dict) -> dict[str, list[str]]:
    """Each born rule's `O`, as its escalation's last call recorded it."""
    return {x["rule_id"]: x["calls"][-1].get("overlapped") or []
            for x in record.get("escalations") or [] if x["verdict"] == "nacida"}


def check(score: dict, records: dict[int, dict], runs: dict[int, dict]) -> list[dict]:
    by_rep = {r["rep"]: r for r in score["runs"]}
    out = []
    for rep, got in runs.items():
        alone = sum(1 for b in got["births"] if not b["O"])
        published = by_rep[rep]["O-d"]["births"]["alone_from_other_queues"]
        out.append({"gate": 1, "rep": rep, "what": "the replay is O-a's",
                    "measured": alone, "published": published,
                    "passes": alone == published})
        recorded = recorded_o(records[rep])
        replayed = {b["rule_id"]: b["O"] for b in got["births"]}
        out.append({"gate": 2, "rep": rep, "what": "it is the loop's",
                    "passes": recorded == replayed})
    return out


def read_expectation(runs: dict[int, dict]) -> list[dict]:
    one = runs[1]
    top = one["top"]
    medians = {rep: r["breadth"]["median_share"] for rep, r in runs.items()}

    def tiles(r):
        n = len(r["births"])
        return max(r["attributes"].values()) / n if n else None

    return [
        {"clause": 1, "what": "run 1's top rule is in at least half of its O's",
         "reading": None if top is None else [top["in_o_of"], top["births_with_o"]],
         "holds": None if top is None else top["in_o_of"] >= top["births_with_o"] / 2},
        {"clause": 2, "what": "run 1's O-a without its top rule is above 0.50",
         "reading": one["o_a_without_top"],
         "holds": None if one["o_a_without_top"] is None
                  else one["o_a_without_top"] > plan.O_A_MAX_ALONE},
        {"clause": 3, "what": "run 3's median share of the space is the largest",
         "reading": medians,
         "holds": medians[3] > max(medians[1], medians[2])},
        {"clause": 4, "what": "in runs 2 and 3 one attribute is in three rules in four",
         "reading": {rep: tiles(runs[rep]) for rep in (2, 3)},
         "holds": all(tiles(runs[rep]) is not None and tiles(runs[rep]) >= 0.75
                      for rep in (2, 3))},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"overlap/readings.py writes {READ_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    space = Space()
    records = {rep: gates.load(plan.run_path(rep)) for rep in range(1, plan.REPS + 1)}
    runs = {rep: read_run(records[rep], space) for rep in records}
    checked = check(score, records, runs)
    for g in checked:
        print(f"  gate {g['gate']} run {g['rep']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    READ_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "its_commit": score["_env"].get("git_commit")},
        "surface": "births, overlap and shares read over the exhaustive space",
        "gates": checked,
        "runs": {str(rep): r for rep, r in runs.items()},
        "expectation": read_expectation(runs),
    }, indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
