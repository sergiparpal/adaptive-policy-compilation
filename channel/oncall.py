"""
WHY c r2 RECALLED LESS `ONCALL_ESCALATION` THAN ITS DRAWS ALLOW.
Stage C found it: run c r2's final base recalls 128/315 of the queue's points
over the space, 2,560 of 6,300. Its draws make no `H05` ticket reportable, so a
proposer that never errs recalls 2/3 under them. That proposer is the
transcriber, and the 2/3 is all of `H04`'s 4,200 points and none of `H05`'s
2,100. c r2 recalls less than that. `FINDINGS_CHANNEL.md`, *What Stage C does
not settle*, item 2, and `IDEAS.md` carry the question. Free on the records.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
`channel/lost.py`'s reading, called for this queue in every run, and not copied:
- every point of the queue the final base does not decide right, by the way it
  was lost: an impasse, a conflict, contested or not, unwritten, or outranked
  by an edge or by containment;
- the rules that decide those points, and the queue's own rules;
- the curve of the queue's points decided right, birth by birth;
- the queue's escalations by verdict;
- the part `channel/lost.py` added after its first run: what the unplaced
  answers left out, and the rules of another queue that contain the whole
  queue.

**Each way is split by the listed rule whose region holds the point.** The
queue's points lie in `H04`'s region or in `H05`'s, never in both:
- *`H04`'s part*, 4,200 points, which c r2's draws let the channel reach;
- *`H05`'s part*, 2,100 points, which they do not.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
`channel/lost.py`'s four, for this queue in every run:
  1. the replay is the base, and the queue's points decided right are Stage C's;
  2. the ways partition the loss;
  3. the curve ends at the base;
  4. the escalations are the record's.

And a fifth, this reading's:
  5. the two parts are disjoint and hold every point of the queue.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads c r2, the queue `ONCALL_ESCALATION`, over the space.

  O1. **Contested.** At least half of the points of `H04`'s part that c r2's
      final base does not decide right are contested conflicts: a rule of the
      queue is undefeated there beside a rule of another queue.
  O2. **Its rule is broad.** Some rule of the queue in c r2's final base holds
      `H04`'s part whole.
  O3. **Born.** Every one of c r2's escalations on the queue's tickets ended
      with its rule born.
  O4. **The curve fell.** After some birth the base decided more of the
      queue's points right than the final base does.
  O5. **Not `H05`.** c r2's final base decides no point of `H05`'s part right.

**The drafter's account.** c r2 wrote `H04`'s region at the queue's escalations.
Rules of other queues born later cross that region, with no edge between them
that held, so the region is contested.
- **Why it expects that.** c r2 met more conflicts than any other run, 33
  against 1 to 20. Its placement rounds listed the most rules, a median of 9.
  Its engine refused the most edges for closing a cycle, 84. A refused edge
  leaves its pair's shared region to a conflict.
- **The bet is O1.** O4 follows from it if the crossing rules came after the
  queue's.
- **O3 is trusted least.** c r1 lost its broad drafts of `SECURITY_INCIDENT` to
  the placement round, which refused each answer that left out a rule
  containing the draft.
- **O5 is trusted most.** c r2 escalated on two of the queue's tickets, both
  `H04`'s and both reported errors (`CH-g`), so no ticket of `H05` reached its
  proposer. Only a rule written at an `H04` ticket that reaches into `H05`'s
  region could break it.

**What the drafter had seen**:
- `FINDINGS_CHANNEL.md` whole, its POST-RUN section on c r1 included;
- `score.json`'s `CH-g` for every run;
- `lost.json` whole: every run's reading of `SECURITY_INCIDENT`;
- the queue's points in `H04`'s and `H05`'s regions, computed from the space
  alone.

**What the drafter had not seen**: any rule, edge or escalation of the queue
`ONCALL_ESCALATION` in any run, any winner on its points, or its curve.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-07, after `channel/lost.py`'s
reading. The expectation above was written and committed before the reading
ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration event.
Zero API calls.

Usage:  python3 -m channel.oncall --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m channel.oncall
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reuse import structure as st

from . import lost as L
from . import plan

F = Fraction
QUEUE = "ONCALL_ESCALATION"
RUN = ("c", 2)                     # the run the expectation reads
REACHED, UNREACHED = "H04", "H05"  # the listed rules whose regions hold the queue
SPLIT = ("right",) + L.WAYS + ("contested", "by_edge", "by_containment")

# The expectation's line.
O_HALF = F(1, 2)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-07, after channel/lost.py's reading. "
    "The expectation in the module's docstring was written and committed before "
    "the reading ran. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "oncall.json"


def parts(truth: int, regions: dict[str, int]) -> dict[str, int]:
    """The queue's points in each listed rule's region."""
    return {REACHED: truth & regions[REACHED], UNREACHED: truth & regions[UNREACHED]}


def parts_partition(p: dict[str, int], truth: int) -> bool:
    """Gate 5."""
    return not p[REACHED] & p[UNREACHED] and p[REACHED] | p[UNREACHED] == truth


def split(w: dict[str, Any], p: dict[str, int]) -> dict[str, dict[str, int]]:
    """Each way's points in each part."""
    return {k: {name: (w[k] & m).bit_count() for name, m in p.items()} for k in SPLIT}


def holds_whole(engine, queue: str, part: int) -> list[str]:
    """The rules of the queue whose region holds the whole part."""
    return [r.rule_id for r in engine.rules
            if r.action == queue and engine.ext[r.rule_id] & part == part]


def read_expectation(runs: dict[str, dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    r = runs[tag]
    by = r["by_part"]
    lost = by["impasse"][REACHED] + by["conflict"][REACHED] + by["unwritten"][REACHED] \
        + by["outranked"][REACHED]
    contested = by["contested"][REACHED]
    escs = r["reading"]["escalations"]
    born = sum(1 for e in escs if e["verdict"] == L.BORN)
    final = r["reading"]["ways"]["right"]
    most = r["reading"]["curve"]["most_right"]
    return [
        {"clause": "O1", "what": "at least half of H04's lost points are contested",
         "reading": {"contested": contested, "of": lost,
                     "share": L.frac(L.share(contested, lost))},
         "holds": lost > 0 and F(contested, lost) >= O_HALF},
        {"clause": "O2", "what": "some rule of the queue holds H04's part whole",
         "reading": {"rules": r["holding_h04_whole"]},
         "holds": bool(r["holding_h04_whole"])},
        {"clause": "O3", "what": "every escalation on the queue's tickets ended born",
         "reading": {"born": born, "of": len(escs),
                     "verdicts": r["reading"]["escalation_verdicts"]},
         "holds": bool(escs) and born == len(escs)},
        {"clause": "O4", "what": "after some birth the base decided more of the queue "
                                 "right than the final base does",
         "reading": {"most_right": most, "at_birth": r["reading"]["curve"]["at_birth"],
                     "final": final},
         "holds": most > final},
        {"clause": "O5", "what": "the final base decides no point of H05's part right",
         "reading": {"right_in_h05": by["right"][UNREACHED]},
         "holds": by["right"][UNREACHED] == 0},
    ]


def read_all_runs(records: dict[str, dict], stage_c: dict[str, Any]) -> dict[str, Any]:
    space = MI.space()
    truth = MI.space_truth()[QUEUE]
    regions = rl_refs.regions()
    p = parts(truth, regions)
    runs = {}
    for t, rec in records.items():
        right = stage_c["CH-g"]["runs"][t]["recall_space"][QUEUE][0]
        reading = L.read_run(rec, space, truth, regions, right, QUEUE)
        final = MI.final_engine(rec)
        w = L.ways(final, truth, QUEUE)
        gates = reading["gates"] + [{"gate": 5, "what": "the two parts are disjoint and hold "
                                                        "every point of the queue",
                                     "passes": parts_partition(p, truth)}]
        runs[t] = {"reading": {**reading, "gates": gates}, "by_part": split(w, p),
                   "holding_h04_whole": holds_whole(final, QUEUE, p[REACHED])}
    return runs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why c r2 recalled less ONCALL_ESCALATION "
                                             "than its draws allow (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"channel/oncall.py writes {record_path()}")
    records, stage_c = L.read_all()
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
    expectation = read_expectation(runs, plan.tag(*RUN))
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": stage_c["_env"].get("git_commit")},
        "surface": "the exhaustive space, 134,400 points",
        "queue": QUEUE,
        "run": plan.tag(*RUN),
        "parts": {REACHED: "the queue's points in H04's region, which the run's draws let "
                           "the channel reach",
                  UNREACHED: "the queue's points in H05's region, which they do not"},
        "constants": {"O_HALF": str(O_HALF)},
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
