"""
WHY THE RUNS UNDER RUN 3'S DRAWS LOST `ONCALL_ESCALATION`.
Stage C found it: under run 3's draws the transcriber compiles the whole queue
under either round, and `PLAN_CHANNEL.md`'s c r3 recalled 14/15 of it on Baidu.
This plan's two runs under the same draws recall 1/15 of its points over the
space, v1c r3, and none, v1b r3, though the proposer drafted the queue at every
escalation of it. `FINDINGS_PLACEMENT.md`, *What Stage C does not settle*, item
2, and `IDEAS.md` carry the question: which rules decide its points, and when
they came. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
`channel/oncall.py`'s reading, called for every run of this plan and not copied:
- `channel/lost.py`'s ways a point of the queue is lost, split by the listed
  rule whose region holds the point, `H04`'s or `H05`'s;
- the rules that decide the lost points, and the queue's own rules;
- the curve of the queue's points decided right, birth by birth;
- the queue's escalations by verdict, and what its unplaced answers left out;
- the rules of another queue that contain the whole queue;
- the rules of the queue that hold `H04`'s part whole;
- the contested pairs, with every edge between their two rules.

This plan's Stage C keeps each run's recall under `PL-g`, in the shape
`PLAN_CHANNEL.md`'s keeps under `CH-g`, because `placement/score.py` reads each
run through `channel/score.py`. So that reader is called with the key renamed.

**And one part of its own: each draft set against its ticket's part.** For every
escalation on a ticket of the queue:
- the ticket's governing rule, `H04` or `H05`, and so its part;
- the first call's draft: its points, its points of the queue, and its points of
  the part;
- whether it holds the part whole, and the governing rule's region's relation to
  it, by `reasoned_loop/unplaced.py`'s `relation`;
- its verdict, and the born rule's points of the part in the final base;
- under v1c, the rules the round left out of its list, each with its reason:
  inside the draft, containing it, or governed.

Beside them, the rules of the queue that hold `H05`'s part whole.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
`channel/oncall.py`'s five, in every run, and a sixth, this reading's:
  6. every escalation on a ticket of the queue is governed by `H04` or `H05`,
     so each draft is set against one of the two parts.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the two runs under run 3's draws, v1c r3 and v1b r3, the
queue `ONCALL_ESCALATION`, over the space. *Lost* means the queue's points a
run's final base does not decide right.

  P1. **Narrow drafts.** In both runs, no draft at an escalation of the queue
      holds its ticket's part whole.
  P2. **No part held.** In both runs, no rule of the queue in the final base
      holds `H04`'s part whole, and none holds `H05`'s.
  P3. **Unwritten.** In both runs, at least half of the lost points are
      unwritten: another queue decides them, and no rule of the queue matches.
  P4. **v1c bore them.** In v1c r3, every escalation of the queue ended with its
      rule born.
  P5. **v1b bore none.** In v1b r3, no escalation of the queue ended with its
      rule born.
  P6. **Never compiled.** In both runs, after no birth did the base decide half
      of the queue's points right or more.

**The drafter's account.** The first call decides a rule's breadth, and under
run 3's draws it wrote each of the queue's tickets narrower than its governing
rule. No rule of the queue reached the part's other tickets, and the broad rules
of other queues that had decided them wrongly before any draft kept deciding
them. The transcriber writes the governing rule's region at the same tickets,
which is why it compiles the queue under the same draws.
- **Why it expects that.** Most births in these runs were not their governing
  rule's region: 26 of 75 in v1c r3 were, and 21 of 60 in v1b r3 (`PL-g`). In
  the bridge DeepInfra wrote the governing rule's region on 13 of its 39 rules,
  and Baidu, whose c r3 recalled 14/15 of the queue, on 18 of its 40.
- **Under v1b the narrow drafts were refused.** Each met a broad rule of another
  queue that contains it, of the kind that decided the queue's tickets before
  any draft. v1b lists such a rule. The answer leaves it out, as the system
  prompt says a nested rule needs no side, and the round refuses the answer, as
  c r1's did with `SECURITY_INCIDENT`. So v1b r3 bore none of them and recalls
  nothing. v1c does not list a containing rule, so v1c r3 bore its drafts, and
  the 420 points it recalls are theirs.
- **The bet is P1.** If a draft held its part whole, the loss would be the
  engine's or the round's, not the first call's.
- **P5 is trusted least.** A draft born narrow and later outranked, by an edge
  or by containment, would leave v1b r3 at none too.
- **P6 is trusted most.** In each run the rules decided four of the queue's seven
  tickets, all four wrongly, and the final bases recall 1/15 and none.

**What the drafter had seen**:
- `FINDINGS_PLACEMENT.md` whole, and in `score.json` the record's keys and v1c
  r3's recall of the queue over the space, 420 of 6,300, which the FINDINGS
  gives too;
- `FINDINGS_CHANNEL.md`'s two POST-RUN readings as `STATUS.md` and `IDEAS.md`
  summarise them, and the message of the commit that wrote
  `results_channel/oncall.json`, `0fce727` on `main`;
- the field names of an escalation, a call, a case's row and a rule, read in
  `loop_smoke.json`;
- `channel/lost.py`, `channel/oncall.py` and their tests, `placement/plan.py`
  and `placement/score.py`.

**What the drafter had not seen**: any rule, edge, escalation or draft of the
queue in any of this plan's six runs, any winner on its points, its curve,
`bridge.json`'s answers at the queue's tickets, and `results_channel/oncall.json`.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-08, after Stage C. The expectation
above was written and committed before the reading ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m placement.oncall --dry-run   # gates 1 to 6; writes nothing
        PYTHONHASHSEED=0 python3 -m placement.oncall
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any

from harness.dsl import Condition, RuleValidationError
from harness.provenance import describe, environment

from channel import lost as L
from channel import oncall as O
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reasoned_loop import unplaced as un
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import plan

F = Fraction
QUEUE = O.QUEUE                    # ONCALL_ESCALATION
H04, H05 = O.REACHED, O.UNREACHED  # the listed rules whose regions hold the queue
RUNS = (("v1c", 3), ("v1b", 3))    # the two runs under run 3's draws, which the expectation reads

# The expectation's line.
P_HALF = F(1, 2)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-08, after Stage C. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a "
    "signed row; no verdict moves.")


def record_path():
    return plan.OUT / "oncall.json"


def stage_c_as_channel(stage_c: dict[str, Any]) -> dict[str, Any]:
    """This plan's Stage C in the key `channel/oncall.py` reads. `PL-g` keeps each
    run's recall in the shape `CH-g` does, because `placement/score.py` reads each
    run through `channel/score.py`."""
    return {"CH-g": {"runs": stage_c["PL-g"]["runs"]}}


# ---------------------------------------------------------------------------
# Each draft against its ticket's part
# ---------------------------------------------------------------------------

def draft_ext(payload: dict | None, space: Space) -> int | None:
    """A draft's extension over the space, or None if it names no condition or
    one the DSL refuses."""
    try:
        conds = [Condition(c["attr"], c["op"], c["value"])
                 for c in (payload or {}).get("conditions") or []]
        return space.extension(conds) if conds else None
    except (KeyError, TypeError, ValueError, RuleValidationError):
        return None


def drafts(record: dict, engine: PriorityEngine, space: Space, parts: dict[str, int],
           regions: dict[str, int], truth: int) -> list[dict[str, Any]]:
    """Every escalation on a ticket of the queue, its first call's draft set
    against the ticket's part. `region_relation` is the governing rule's region
    against the draft, as `relation` reads it: `inside_draft` when the draft is
    broader, `contains_draft` when it is narrower."""
    rows = {r["idx"]: r for r in record["records"]}
    out = []
    for esc in record["escalations"]:
        row = rows.get(esc["idx"], {})
        if row.get("truth") != QUEUE:
            continue
        gov = row.get("truth_rule")
        part = parts.get(gov)
        c0 = (esc.get("calls") or [{}])[0]
        payload = c0.get("payload") or {}
        d = draft_ext(payload, space)
        rid = esc.get("rule_id")
        born = esc.get("verdict") == L.BORN and rid in engine.ext
        out.append({
            "idx": esc["idx"], "cause": row.get("cause"), "governing": gov,
            "part_points": part.bit_count() if part is not None else None,
            "draft_action": payload.get("action"),
            "draft_conditions": payload.get("conditions"),
            "draft_points": d.bit_count() if d is not None else None,
            "draft_queue_points": (d & truth).bit_count() if d is not None else None,
            "draft_part_points": (d & part).bit_count()
                                 if d is not None and part is not None else None,
            "holds_part": d is not None and part is not None and d & part == part,
            "region_relation": un.relation(regions[gov], d)
                               if d is not None and gov in regions else None,
            "verdict": esc.get("verdict"), "rule_id": rid, "copy_of": esc.get("copy_of"),
            "born_part_points": (engine.ext[rid] & part).bit_count()
                                if born and part is not None else None,
            "listed": len(esc.get("listed") or []),
            "left_out": c0.get("left_out"),
        })
    return out


def governed_by_a_part(ds: list[dict[str, Any]], parts: dict[str, int]) -> bool:
    """Gate 6."""
    return all(d["governing"] in parts for d in ds)


# ---------------------------------------------------------------------------
# Every run, read whole
# ---------------------------------------------------------------------------

def read_all_runs(records: dict[str, dict], stage_c: dict[str, Any]) -> dict[str, Any]:
    """`channel/oncall.py`'s reading of every run, with this reading's part and
    gate 6 beside it."""
    space = MI.space()
    truth = MI.space_truth()[QUEUE]
    regions = rl_refs.regions()
    p = O.parts(truth, regions)
    runs = O.read_all_runs(records, stage_c_as_channel(stage_c))
    for t, rec in records.items():
        final = MI.final_engine(rec)
        ds = drafts(rec, final, space, p, regions, truth)
        runs[t]["holding_h05_whole"] = O.holds_whole(final, QUEUE, p[H05])
        runs[t]["drafts"] = ds
        runs[t]["reading"]["gates"].append(
            {"gate": 6, "what": "every escalation on a ticket of the queue is governed "
                                "by H04 or H05",
             "passes": governed_by_a_part(ds, p)})
    return runs


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    tc, tb = (plan.tag(*r) for r in RUNS)
    pair = {t: runs[t] for t in (tc, tb)}

    def whole(r):
        return sum(1 for d in r["drafts"] if d["holds_part"])

    def ways(r):
        return r["reading"]["ways"]

    def escs(r):
        return r["reading"]["escalations"]

    def born(r):
        return sum(1 for e in escs(r) if e["verdict"] == L.BORN)

    n = runs[tc]["reading"]["queue_points"]
    half = P_HALF * n
    return [
        {"clause": "P1", "what": "in both runs no draft at an escalation of the queue "
                                 "holds its ticket's part whole",
         "reading": {t: {"drafts_holding_their_part": whole(r), "of": len(r["drafts"])}
                     for t, r in pair.items()},
         "holds": all(r["drafts"] and whole(r) == 0 for r in pair.values())},
        {"clause": "P2", "what": "in both runs no rule of the queue holds H04's part "
                                 "whole, and none holds H05's",
         "reading": {t: {H04: r["holding_h04_whole"], H05: r["holding_h05_whole"]}
                     for t, r in pair.items()},
         "holds": all(not r["holding_h04_whole"] and not r["holding_h05_whole"]
                      for r in pair.values())},
        {"clause": "P3", "what": "in both runs at least half of the lost points are "
                                 "unwritten",
         "reading": {t: {"unwritten": ways(r)["unwritten"], "of": ways(r)["lost"],
                         "share": L.frac(L.share(ways(r)["unwritten"], ways(r)["lost"]))}
                     for t, r in pair.items()},
         "holds": all(ways(r)["lost"] > 0
                      and F(ways(r)["unwritten"], ways(r)["lost"]) >= P_HALF
                      for r in pair.values())},
        {"clause": "P4", "what": f"in {tc} every escalation of the queue ended with its "
                                 "rule born",
         "reading": {"born": born(pair[tc]), "of": len(escs(pair[tc])),
                     "verdicts": pair[tc]["reading"]["escalation_verdicts"]},
         "holds": bool(escs(pair[tc])) and born(pair[tc]) == len(escs(pair[tc]))},
        {"clause": "P5", "what": f"in {tb} no escalation of the queue ended with its rule "
                                 "born",
         "reading": {"born": born(pair[tb]), "of": len(escs(pair[tb])),
                     "verdicts": pair[tb]["reading"]["escalation_verdicts"]},
         "holds": bool(escs(pair[tb])) and born(pair[tb]) == 0},
        {"clause": "P6", "what": "in both runs after no birth did the base decide half of "
                                 "the queue's points right or more",
         "reading": {t: {"most_right": r["reading"]["curve"]["most_right"],
                         "at_birth": r["reading"]["curve"]["at_birth"], "of": n}
                     for t, r in pair.items()},
         "holds": all(r["reading"]["curve"]["most_right"] < half for r in pair.values())},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(arm, rep): json.loads(plan.run_path(arm, rep).read_text())
               for arm, rep in plan.schedule()}
    return records, json.loads(plan.score_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the runs under run 3's draws lost "
                                             "ONCALL_ESCALATION (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 6 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"placement/oncall.py writes {record_path()}")
    records, stage_c = read_all()
    runs = read_all_runs(records, stage_c)
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["reading"]["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": stage_c["_env"].get("git_commit")},
        "surface": "the exhaustive space, 134,400 points",
        "queue": QUEUE,
        "runs_the_expectation_reads": [plan.tag(*r) for r in RUNS],
        "parts": {H04: "the queue's points in H04's region",
                  H05: "the queue's points in H05's region"},
        "constants": {"P_HALF": str(P_HALF)},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
