"""
WHY L LOSES `ONCALL_ESCALATION`.
Stage C found it: L's final bases recall 0.4, 0.4476 and 0.4341 of the queue's
points over the space. N's, whose proposer was never handed a label, recall 1,
0.7333 and 1 (`CR-f` refuted). `FINDINGS_CORRECTIONS.md`, *What Stage C does
not settle*, item 1, `STATUS.md` and `IDEAS.md` carry the question: which rules
decide the points L loses, and from which labels they were drafted.
`corrections/fall.py` read the points of `SECURITY_INCIDENT` right at each L
run's peak and lost after it. It did not read the rest of that queue's, nor any
of this queue's. Proposed by the agent and asked for by Sergi on 2026-11-15,
after `corrections/conditions.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**`channel/oncall.py`'s reading, called for every run of this plan and not
copied**, both arms:
- `channel/lost.py`'s ways a point of the queue is lost: an impasse, a
  conflict, contested or not, unwritten, or outranked by an edge or by
  containment;
- the rules that decide the lost points, and the queue's own rules;
- the curve of the queue's points decided right, birth by birth;
- the queue's escalations by verdict, and what its unplaced answers left out;
- the rules of another queue that contain the whole queue;
- each way split by `H04`'s part, 4,200 points, and `H05`'s, 2,100;
- the rules of the queue that hold `H04`'s part whole, and `H05`'s;
- the contested pairs, with every edge between their two rules.
Stage C keeps each run's recall under `CR-g` as a fraction, so the reader is
handed it as a count of the queue's points.

**And three parts of its own.**

**1. Who takes the points.** A lost point that one other queue decides,
unwritten or outranked, is *taken*. The rules of that queue undefeated there
decide it. Each such rule is read with its birth:
- the kind of the escalation it was born at: a reported error, an impasse or a
  conflict;
- its ticket's true queue and governing rule;
- at a reported error of an L run, the queue the report named.
A rule born at a reported error of an L run is a *correction*. The taken points
are partitioned two ways, each in three:
- by whether every rule undefeated there was born at a reported error, some
  was, or none was;
- by whether every one was born at a ticket that `H06`, `H07` or `H08` governs,
  the layer of the policy right below the queue's, some was, or none was.
They are also counted by the queue that decides them.

**2. When they were lost.** The base is replayed in birth order, as
`corrections/fall.py` replays it, and read over the space after every birth. A
lost point was either never right after any birth, or right after some birth
and lost later. A point of the second kind is read at its *last loss*: the last
birth at which it went from right to not right. That birth gives `fall.py`'s
kind of loss, by containment, by an edge or a conflict, and the newborn's queue,
cause, label and ticket. Each lost point is also set against the run's peak,
`fall.py`'s:
  at_the_peak      right after the peak birth, and lost later: the points
                   `fall.py` read;
  before_the_peak  not right after the peak birth.
Each of `channel/lost.py`'s ways, and each deciding queue, is split the same
way.

**3. What the levers give back.** The queue's points decided right in the final
base of each replay this plan's readings have built, beside the record's order:
  losses_first  the same births and declarations, each birth's losses tried
                before its wins, as `corrections/fall.py`'s `order_replay`;
  where         the same, with the engine that refuses a cycle only where it is,
                `corrections/paths.py`'s `try_edge_where`;
  doors         the doors' edges left out, as `corrections/carry.py`'s `replay`
                leaves them out. A run with no gateway has no door, and its
                replay is the record's order.
A replay *gives back* the queue's points it decides right less those the
record's final base does. None of them is the loop that would have run.

**And the rest of `SECURITY_INCIDENT`'s.** `channel/lost.py`'s reading of that
queue in every run, and the three parts above for it. Its points at the peak are
`fall.py`'s, and those before it are the ones nothing has read.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
`channel/oncall.py`'s five for the queue, and `channel/lost.py`'s four for
`SECURITY_INCIDENT`, in every run. Gate 1 of each holds the final base's right
points to Stage C's recall. And three of this reading's, for both queues:
  6. **The takers partition the taken points.** Each of part 1's two partitions
     is disjoint and covers the taken points. At every reported error of an L
     run the record handed a report, and it names the ticket's true queue. An N
     record handed none.
  7. **The last losses partition what was right once.** The points never right
     and those with a last loss are disjoint and cover the lost points, and each
     last loss's kinds cover it. The replay's final base decides right exactly
     what the ways call right, and every check of `fall.py`'s replay passes.
     The peak birth is `fall.json`'s, and so are the points lost at the peak, by
     true queue.
  8. **Each lever is its record's.** The record's order is `fall.json`'s curve
     at every birth. Each replay's peak, final share, recall of
     `SECURITY_INCIDENT`, conflicts and refusals for a cycle are the ones
     `fall.json`, `paths.json` and `carry.json` keep. Every replay's masks are
     its engine's.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
O1 to O6 read the queue `ONCALL_ESCALATION`, and O7 reads `SECURITY_INCIDENT`.
Every clause pools L's three runs. *Lost* means a queue's points a run's final
base does not decide right.

  O1. **What fell was left in conflict.** At least half of the queue's points
      lost at the peak are contested conflicts: a rule of the queue is
      undefeated there beside a rule of another queue.
  O2. **Before the peak, outranked.** At least half of the queue's points lost
      before the peak are outranked: one other queue decides them, though a
      rule of the queue matches them.
  O3. **By an edge.** At least half of the queue's outranked points are
      outranked by an edge.
  O4. **By the corrections.** At least half of the queue's taken points are
      decided only by rules born at a reported error.
  O5. **From the layer below.** At least half of the queue's taken points are
      decided only by rules born at tickets that `H06`, `H07` or `H08` governs.
  O6. **The losses first give back what fell.** The replay that tries each
      birth's losses before its wins gives back at least half as many of the
      queue's points as the runs lost at the peak.
  O7. **The rest of `SECURITY_INCIDENT`'s went to `T2_TECHNICAL`.** At least
      half of that queue's points lost before the peak are decided by
      `T2_TECHNICAL`.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account.**
- **The catalogue writes the queue broad.** Its line calls on-call the queue of
  critical incidents that cannot wait for the next shift, at any hour. N's
  bases, never told a queue, keep the queue whole and recall none of
  `T3_ENGINEERING` in two runs of three. So the catalogue's rule of the queue
  takes the tickets of the layer below it too: `H06`'s and `H07`'s, which are
  `T3_ENGINEERING`'s, and `H08`'s, which are `T2_TECHNICAL`'s.
- **The reports come where that rule errs.** At those tickets the report names
  `T3_ENGINEERING` or `T2_TECHNICAL`. The first call writes that queue's
  general rule, as `corrections/broad.py` found, broader than the ticket's
  governing rule, and it reaches `H04`'s and `H05`'s parts.
- **The correction goes above the rule that erred.** At reported errors, 813 of
  833 placements against a listed rule that holds the ticket put the newborn
  above it (`corrections/above.py`). A correction that crosses the queue's rule
  takes their shared points by that edge. So before the peak the queue's rule
  stays, and loses its points: O2 to O5.
- **After the peak the newborns cede to the queue, and are refused.** A rule of
  the queue holds an answer down (`corrections/above.py`, E2). Where the
  newborn's own wins already reach that rule, the engine refuses its loss, and
  their shared points are left contested, as `SECURITY_INCIDENT`'s were
  (`corrections/fall.py`). After L r1's peak such refusals stood against rules
  of the queue on 6,300 pair-points (`paths.json`): O1. Installed losses
  first, they go in: O6.
- **The rest of `SECURITY_INCIDENT`'s is the gateways'.** They are rules of
  `T2_TECHNICAL` nested in the keyword's region, born at reported tickets of
  `H03`, and they take its points by containment: O7.

**The bet is O2.** If the points lost before the peak were unwritten instead,
L would have written the queue narrow, and the lever would be the first call,
not the order. **O1 is trusted most**, because the drafter saw the refusals
against the queue's rules after L r1's peak. **O3 is trusted least**: a
correction nested in a rule of the queue that writes the severity alone takes
its points by containment, with no edge.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md`'s verdicts and Stage C, with its table of each
  queue's recall by run and its *What Stage C does not settle*, and its
  POST-RUN sections as `STATUS.md` and `IDEAS.md` summarise them;
- the lines of that record's POST-RUN sections that name the queue, found by a
  search and cut at 190 characters. Two are about the points lost after a
  peak: "**Two of them took most.** An `ONCALL_ESCALATION` rule, `severity = 1
  ∧" and "way, and 8,400 points to one rule of `ONCALL_ESCALATION` declared
  above 74". The rest are about the placement rounds' answers, which
  `corrections/above.py` and `corrections/conditions.py` read;
- `fall.json`'s summary of each L run: its peak, its final share, its points
  lost at the peak by true queue, of which this queue's are 2,100, 2,220 and
  1,360, and over every queue its losses by kind and by cause, and after the
  peak. Also the first entry or two of its points lost by the newborn's queue,
  where the print cut them;
- `paths.json`'s L r1 summary of refused right sides by the queue of the rule
  the newborn declared below, of which this queue's weigh 6,300 pair-points,
  and the keys of its `where` replay; the keys of `carry.json` and
  `gateway.json`;
- `score.json`'s `CR-g` recalls, and from them the queue's lost points,
  counted for this reading: 3,780, 3,480 and 3,565 in L's runs. Also the
  queue's 6,300 points, 4,200 in `H04`'s part and 2,100 in `H05`'s, and every
  queue's points of the space;
- `PLAN_CORRECTIONS.md`'s reasons for `CR-f`: run 2's draws make no ticket of
  `H05` reportable;
- the field names of a run's record, L r1's escalations by kind and by verdict,
  and each run's reported errors: 216, 209 and 235 in L's, each with a report,
  and 318, 326 and 323 in N's, with none. L r1's reports name each ticket's
  true queue, 216 of 216;
- the hidden policy and the level 1 catalogue's text;
- `channel/lost.py`, `channel/oncall.py`, `placement/oncall.py`,
  `corrections/fall.py`, `corrections/carry.py`, `corrections/paths.py` and
  `corrections/forgotten.py`'s helpers.

**What the drafter had not seen**: any rule of the queue in any run of this
plan but the two lines above, any rule that decides any of its points, any
escalation on its tickets, its curve, any replay's recall of it, and any point
of `SECURITY_INCIDENT` lost before a peak.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: THE RULE THAT ERRED, AND THE EDGES
--------------------------------------------------------------------------
The first run found the queue written whole in every L run, and its taken points
decided by corrections of the layer below, mostly by an edge. So this part
reads, for every rule that takes a queue's points:
- **the rule that erred**: at a reported error, the rule that had decided the
  ticket, and its queue, as the record keeps them;
- **the edges between it and the queue's rules**, each with the engine's
  verdict:
  own    those its answer declared at its birth, wins over the queue's rules
         and losses to them;
  later  those a rule of the queue born after it declared against it.
The taken points are weighed by the queue of the rule that erred, a point
several takers share counted for each.

It was tried on the records in a scratch script before it was written here,
after the seven clauses above had been read: O1 to O6 hold, and O7 fails. It
carries no expectation and moves no clause.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-15, after
`corrections/conditions.py`. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not
a calibration event. Zero API calls.

Usage:  python3 -m corrections.oncall --dry-run   # gates 1 to 8; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.oncall
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Callable, Sequence

from harness.ceiling_check import all_cases
from harness.provenance import describe, environment

from blind import rows as brows
from channel import lost as L
from channel import oncall as O
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, PriorityEngine, Space

from . import carry as cr
from . import fall as fl
from . import forgotten as fg
from . import gateway as gw
from . import paths as pa
from . import plan

F = Fraction
QUEUE, SEC, T2 = O.QUEUE, fl.SEC, fl.T2
QUEUES = (QUEUE, SEC)
H04, H05 = O.REACHED, O.UNREACHED  # the listed rules whose regions hold the queue
LAYER = ("H06", "H07", "H08")      # the policy's layer right below the queue's
UNLABELLED = fl.UNLABELLED
L_RUNS = tuple(plan.tag(plan.LABELLED, k) for k in range(1, plan.REPS + 1))

# Whether the rules undefeated on a taken point were born so: all, some, none.
EVERY, SOME, NONE = "every", "some", "none"
THREE = (EVERY, SOME, NONE)
# A lost point against the run's peak.
AT_PEAK, BEFORE_PEAK = "at_the_peak", "before_the_peak"
# The replays read beside the record's order.
RECORD, LOSSES_FIRST, WHERE, DOORS = "record", "losses_first", "where", "doors"
LEVERS = (LOSSES_FIRST, WHERE, DOORS)
# The ways a lost point is split by.
WAYS = ("lost",) + L.WAYS + ("contested", "by_edge", "by_containment")
# The keys of `fall.py`'s `order_summary` that the gates compare.
SUMMARY_KEYS = ("peak", "final", "fall", "security_recall", "conflict", "refused_for_a_cycle")

# The expectation's line.
O_HALF = F(1, 2)

PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-15, after "
    "corrections/conditions.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its seven clauses were read: for every rule that takes "
    "a queue's points, the rule that had decided its ticket at a reported error, and the "
    "edges between it and the queue's rules, those its own answer declared at its birth and "
    "those later rules of the queue declared against it, each with the engine's verdict. "
    "Tried in a scratch script first. No expectation; no clause moves.")
OWN, LATER = "own", "later"
WINS, LOSSES = "wins", "losses"


def record_path():
    return plan.OUT / "oncall.json"


share, frac = fg.share, fg.frac


def plain(x: Any) -> Any:
    """`forgotten.py`'s `plain`, and a string for anything else."""
    y = fg.plain(x)
    return str(y) if y is x else y


# ---------------------------------------------------------------------------
# Stage C, as the channel's readers take it
# ---------------------------------------------------------------------------

def stage_c_counts(score: dict[str, Any], points: dict[str, int]) -> dict[str, Any]:
    """Stage C's recall of each queue in each run, in the shape `channel/oncall.py`
    and `channel/lost.py` read: the count of the queue's points decided right,
    and the queue's points. A recall that is not a whole count gives -1, which no
    base matches, so gate 1 fails on it."""
    runs = {}
    for tag, r in score["CR-g"]["runs"].items():
        got = {}
        for q, n in points.items():
            x = F(r["recall"][q]["fraction"]) * n
            got[q] = [x.numerator if x.denominator == 1 else -1, n]
        runs[tag] = {"recall_space": got}
    return {"CH-g": {"runs": runs}}


# ---------------------------------------------------------------------------
# Part 1: who takes the points
# ---------------------------------------------------------------------------

def births_of(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Each rule's birth: the kind of the escalation it was born at, its ticket's
    true queue and governing rule, and the queue the report named, if the
    record handed one there."""
    rows = {r["idx"]: r for r in record["records"]}
    escs = fg.escalation_at(record)
    handed = record.get("reports_handed") or {}
    out = {}
    for r in record["rules"]:
        idx = r["born_at"]
        row = rows.get(idx, {})
        out[r["rule_id"]] = {"born_at": idx, "cause": (escs.get(idx) or {}).get("kind"),
                             "truth": row.get("truth"), "governing": row.get("truth_rule"),
                             "label": handed.get(str(idx))}
    return out


def reports_are_the_truth(record: dict[str, Any]) -> bool:
    """Gate 6's second half. An L record handed a report at every reported error
    and nowhere else, each naming its ticket's true queue; an N record handed
    none."""
    handed = record.get("reports_handed") or {}
    if record.get("arm") != plan.LABELLED:
        return not handed
    rows = {r["idx"]: r for r in record["records"]}
    errors = {e["idx"] for e in record["escalations"] if e["kind"] == plan.ERROR}
    return ({int(k) for k in handed} == errors
            and all(rows[int(k)].get("truth") == q for k, q in handed.items()))


def taken_of(w: dict[str, Any]) -> int:
    """The lost points one other queue decides."""
    out = 0
    for m in w["wrong"].values():
        out |= m
    return out


def partition(undefeated: dict[str, int], taken: int,
              keep: Callable[[str], bool]) -> dict[str, int]:
    """The taken points by whether every rule undefeated there is one `keep`
    accepts, some is, or none is."""
    yes = no = 0
    for rid, m in undefeated.items():
        pts = m & taken
        if not pts:
            continue
        if keep(rid):
            yes |= pts
        else:
            no |= pts
    return {EVERY: yes & ~no, SOME: yes & no, NONE: no & ~yes}


def partitions_ok(parts: dict[str, int], taken: int) -> bool:
    """Gate 6's first half, for one partition."""
    union, total = 0, 0
    for m in parts.values():
        union |= m
        total += m.bit_count()
    return union == taken and total == taken.bit_count()


def takers(w: dict[str, Any], births: dict[str, dict[str, Any]], engine: PriorityEngine,
           record: dict[str, Any], regions: dict[str, int] | None = None
           ) -> tuple[dict[str, Any], dict[str, dict[str, int]]]:
    """The taken points, read by the rules that decide them: the two partitions,
    the deciding queues, and every rule undefeated on them with its birth. A
    point several such rules share is counted for each rule, and once in each
    partition. `regions`, when given, splits each rule's taken points by part.
    Also returns the partitions' masks, for gate 6."""
    taken = taken_of(w)
    und = w["undefeated"]
    masks = {"by_cause": partition(und, taken, lambda r: births[r]["cause"] == plan.ERROR),
             "by_layer": partition(und, taken, lambda r: births[r]["governing"] in LAYER)}
    conds = {r["rule_id"]: r["conditions"] for r in record["rules"]}
    rows = []
    for r in engine.rules:
        pts = und[r.rule_id] & taken
        if not pts:
            continue
        row = {"rule_id": r.rule_id, "action": r.action, "conditions": conds[r.rule_id],
               **births[r.rule_id], "points": engine.ext[r.rule_id].bit_count(),
               "taken": pts.bit_count(), "unwritten": (pts & w["unwritten"]).bit_count(),
               "outranked": (pts & w["outranked"]).bit_count(),
               "by_edge": (pts & w["by_edge"]).bit_count()}
        if regions:
            row["by_part"] = {k: (pts & m).bit_count() for k, m in regions.items()}
        rows.append(row)
    rows.sort(key=lambda x: (-x["taken"], x["born_at"]))

    def weigh(key: Callable[[dict], Any]) -> dict[str, int]:
        c: Counter = Counter()
        for row in rows:
            c[str(key(row))] += row["taken"]
        return dict(sorted(c.items()))

    summary = {
        "points": taken.bit_count(),
        "by_queue": {b: m.bit_count() for b, m in sorted(w["wrong"].items())},
        "by_cause": {k: m.bit_count() for k, m in masks["by_cause"].items()},
        "by_layer": {k: m.bit_count() for k, m in masks["by_layer"].items()},
        "rules": len(rows),
        "weighed": {"by_cause": weigh(lambda x: x["cause"]),
                    "by_label": weigh(lambda x: x["label"]),
                    "by_governing": weigh(lambda x: x["governing"]),
                    "by_queue_and_cause": weigh(lambda x: f"{x['action']} {x['cause']}")},
        "takers": rows,
    }
    return summary, masks


def erred_and_edges(record: dict[str, Any], rows_taken: Sequence[dict[str, Any]], queue: str,
                    action: dict[str, str]) -> dict[str, Any]:
    """ADDED AFTER THE FIRST RUN. For every taker: the rule that had decided its
    ticket, at a reported error, and the edges between it and the queue's rules,
    those its answer declared at its birth and those a later rule of the queue
    declared against it, by the engine's verdict. The taken points weighed by the
    queue of the rule that erred, a point several takers share counted for
    each."""
    rows = {r["idx"]: r for r in record["records"]}
    by_birth = erb.edges_by_birth(record)
    born_at = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    out, weighed = [], Counter()
    for t in rows_taken:
        rid, born = t["rule_id"], t["born_at"]
        row = rows.get(born, {})
        edges = {OWN: {WINS: Counter(), LOSSES: Counter()},
                 LATER: {WINS: Counter(), LOSSES: Counter()}}
        for idx, es in by_birth.items():
            for e in es:
                if rid not in (e.winner, e.loser):
                    continue
                other = e.loser if e.winner == rid else e.winner
                if action.get(other) != queue:
                    continue
                side = WINS if e.winner == rid else LOSSES
                if idx == born:
                    edges[OWN][side][e.verdict] += 1
                elif born_at.get(other) == idx:
                    edges[LATER][side][e.verdict] += 1
        erred = {"rule_id": row.get("engine_rule"), "action": row.get("engine_action")}
        weighed[str(erred["action"])] += t["taken"]
        out.append({"rule_id": rid, "action": t["action"], "born_at": born,
                    "cause": t["cause"], "taken": t["taken"], "erred": erred,
                    "edges": {k: {s: dict(sorted(c.items())) for s, c in v.items()}
                              for k, v in edges.items()}})
    return {"takers": out, "taken_by_the_erred_queue": dict(sorted(weighed.items()))}


# ---------------------------------------------------------------------------
# Part 2: when they were lost
# ---------------------------------------------------------------------------

def peak_of(steps: Sequence[dict[str, Any]]) -> int | None:
    """`fall.py`'s peak: the first birth after which the most points are right,
    as an index into the steps."""
    counts = [s["right"].bit_count() for s in steps]
    return counts.index(max(counts)) if counts else None


def history(steps: Sequence[dict[str, Any]], peak: int, truth: int, lost: int,
            births: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, int]]:
    """Each lost point by when it was lost: never right after any birth, or at
    its last loss, the last birth at which it went from right to not right. Also
    returns the masks, for gate 7."""
    ever = 0
    for s in steps:
        ever |= s["right"] & truth
    never = lost & ~ever
    assigned = after = 0
    rows = []
    for i in range(len(steps) - 1, -1, -1):
        s = steps[i]
        last = s["lost"] & lost & ~assigned
        if not last:
            continue
        assigned |= last
        if i > peak:
            after |= last
        b = births[s["rule_id"]]
        rows.append({"born_at": s["idx"], "rule_id": s["rule_id"], "action": s["action"],
                     "cause": s["cause"], "label": b["label"], "governing": b["governing"],
                     "after_the_peak": i > peak, "points": last.bit_count(),
                     "by_kind": {k: (last & s[k]).bit_count() for k in fl.LOSSES}})
    rows.reverse()

    def tally(key: Callable[[dict], Any], rows_: list[dict]) -> dict[str, int]:
        c: Counter = Counter()
        for row in rows_:
            c[str(key(row))] += row["points"]
        return dict(sorted(c.items()))

    def kinds(rows_: list[dict]) -> dict[str, int]:
        return {k: sum(row["by_kind"][k] for row in rows_) for k in fl.LOSSES}

    late = [row for row in rows if row["after_the_peak"]]
    early = [row for row in rows if not row["after_the_peak"]]
    summary = {
        "lost": lost.bit_count(), "never_right": never.bit_count(),
        "last_losses": {"points": assigned.bit_count(), "births": len(rows),
                        "after_the_peak": after.bit_count(),
                        "by_kind": kinds(rows),
                        "after_the_peak_by_kind": kinds(late),
                        "at_or_before_the_peak_by_kind": kinds(early),
                        "by_newborn_queue": tally(lambda x: x["action"], rows),
                        "by_cause": tally(lambda x: x["cause"], rows),
                        "by_label": tally(lambda x: x["label"], rows),
                        "by_governing": tally(lambda x: x["governing"], rows)},
        "losses": rows,
    }
    return summary, {"ever": ever, "never": never, "once": assigned}


def history_ok(masks: dict[str, int], summary: dict[str, Any], lost: int) -> bool:
    """Gate 7's partition: never right and last lost are disjoint and cover the
    lost points, every point right once has a last loss, and each last loss's
    kinds cover it."""
    never, once = masks["never"], masks["once"]
    rows = summary["losses"]
    return (not never & once and never | once == lost
            and masks["ever"] & lost == once
            and sum(r["points"] for r in rows) == once.bit_count()
            and all(sum(r["by_kind"].values()) == r["points"] for r in rows))


def by_peak(w: dict[str, Any], at_peak: int) -> dict[str, dict[str, Any]]:
    """Each way of a queue's lost points, and each deciding queue's, split by
    whether the point was right after the peak birth."""
    lost = w["lost"]
    out = {}
    for name, m in ((AT_PEAK, lost & at_peak), (BEFORE_PEAK, lost & ~at_peak)):
        out[name] = {**{k: (w[k] & m).bit_count() for k in WAYS},
                     "by_queue": {b: (mm & m).bit_count() for b, mm in sorted(w["wrong"].items())
                                  if mm & m}}
    return out


# ---------------------------------------------------------------------------
# Part 3: what the levers give back
# ---------------------------------------------------------------------------

def masks_replay(record: dict[str, Any], space: Space, truth: dict[str, int], *,
                 losses_first: bool = False, where: bool = False) -> dict[str, Any]:
    """The same births and declarations, each birth's edges in the record's
    order or with the newborn's losses first, as `fall.py`'s `order_replay`
    tries them, and each edge tried by the engine or by `paths.py`'s
    `try_edge_where`. `order_replay` and `where_replay` keep no masks, so this
    keeps them; gate 8 holds it to their records."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    curve: list[int] = []
    cycles = 0
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        edges = by_birth.get(idx, [])
        if losses_first:
            edges = ([e for e in edges if e.loser == rid]
                     + [e for e in edges if e.loser != rid])
        for e in edges:
            why = (pa.try_edge_where(engine, e.winner, e.loser) if where
                   else engine.try_edge(e.winner, e.loser))
            cycles += why == EDGE_CYCLE
        fl.settle(engine, und, action, rid, d["action"])
        curve.append(fl.right_of(fl.decision(und, action), truth).bit_count())
    dec = fl.decision(und, action)
    right = fl.right_of(dec, truth)
    return {"und": und, "action": action, "curve": curve, "cycles": cycles,
            "right": right.bit_count(), "security": (right & truth.get(SEC, 0)).bit_count(),
            "conflict": dec["two"].bit_count(),
            "masks_ok": und == brows.undefeated_masks(engine)}


def right_mask(got: dict[str, Any], truth: dict[str, int]) -> int:
    """A replay's final base's right points."""
    return fl.right_of(fl.decision(got["und"], got["action"]), truth)


def summary_of(got: dict[str, Any], truth: dict[str, int], n: int) -> dict[str, Any]:
    """`fall.py`'s `order_summary` of a replay, rounded as the records keep it."""
    s = st._rounded(fl.order_summary(got, truth, n))
    return {k: s[k] for k in SUMMARY_KEYS}


def kept(stored: dict[str, Any]) -> dict[str, Any]:
    return {k: stored.get(k) for k in SUMMARY_KEYS}


def levers(record: dict[str, Any], space: Space, truth: dict[str, int],
           gateway_run: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """The record's order and the three replays, each with its final base's
    right points."""
    got = {RECORD: cr.replay(record, space, truth),
           LOSSES_FIRST: masks_replay(record, space, truth, losses_first=True),
           WHERE: masks_replay(record, space, truth, where=True),
           DOORS: cr.replay(record, space, truth, frozenset(cr.door_edges(gateway_run)))}
    for g in got.values():
        g["right_mask"] = right_mask(g, truth)
    return got


def levers_ok(got: dict[str, dict[str, Any]], truth: dict[str, int], n: int,
              fall_run: dict[str, Any], paths_run: dict[str, Any],
              carry_run: dict[str, Any]) -> bool:
    """Gate 8."""
    orders = fall_run["added_after_the_first_run"]["orders"]
    return (got[RECORD]["curve"] == [c["right"] for c in fall_run["curve"]]
            and summary_of(got[RECORD], truth, n) == kept(orders["declared"])
            and summary_of(got[LOSSES_FIRST], truth, n) == kept(orders["losses_first"])
            and summary_of(got[WHERE], truth, n)
            == kept(paths_run["added_after_the_first_run"]["where"]["engine"])
            and summary_of(got[DOORS], truth, n) == kept(carry_run["replays"][DOORS])
            and all(g["masks_ok"] for g in got.values()))


def given_back(got: dict[str, dict[str, Any]], truth: int) -> dict[str, dict[str, int]]:
    """For one queue: its points each replay decides right, what it gives back
    against the record's order, and the points it turns right and wrong."""
    rec = got[RECORD]["right_mask"] & truth
    out = {RECORD: {"right": rec.bit_count()}}
    for k in LEVERS:
        m = got[k]["right_mask"] & truth
        out[k] = {"right": m.bit_count(), "gives_back": m.bit_count() - rec.bit_count(),
                  "turned_right": (m & ~rec).bit_count(),
                  "turned_wrong": (rec & ~m).bit_count()}
    return out


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], oncall_run: dict[str, Any], space: Space,
             truth: dict[str, int], cases: Sequence, regions: dict[str, int],
             stage_c: dict[str, Any], fall_run: dict[str, Any], paths_run: dict[str, Any],
             carry_run: dict[str, Any], gateway_run: dict[str, Any], tag: str) -> dict[str, Any]:
    """One run: `channel/oncall.py`'s reading of the queue, handed in as
    `oncall_run`, `channel/lost.py`'s of `SECURITY_INCIDENT`, the three parts of
    this reading for both, and the gates."""
    n = space.n
    final = MI.final_engine(record)
    births = births_of(record)
    parts = O.parts(truth[QUEUE], regions)
    sec_right = stage_c["CH-g"]["runs"][tag]["recall_space"][SEC][0]
    security = L.read_run(record, space, truth[SEC], regions, sec_right, SEC)

    rep = fl.replay(record, space, truth, cases)
    steps = rep["steps"]
    p = peak_of(steps)
    at_peak = steps[p]["right"] if steps else 0
    final_right = steps[-1]["right"] if steps else 0
    fall_lost = fall_run["summary"]["lost"]["by_true_queue"]
    fall_peak = fall_run["summary"]["peak"]
    got = levers(record, space, truth, gateway_run)

    out: dict[str, Any] = {"peak": None if p is None else {
        "birth": p + 1, "born_at": steps[p]["idx"], "rule_id": steps[p]["rule_id"]}}
    gates = []
    taken_part, hist_part, peak_part, lever_part, added = {}, {}, {}, {}, {}
    action = {r.rule_id: r.action for r in final.rules}
    ok6 = reports_are_the_truth(record)
    ok7 = (all(rep["ok"].values()) and p is not None and fall_peak is not None
           and p + 1 == fall_peak["birth"])
    for q in QUEUES:
        w = L.ways(final, truth[q], q)
        summ, masks = takers(w, births, final, record, parts if q == QUEUE else None)
        taken_part[q] = summ
        added[q] = erred_and_edges(record, summ["takers"], q, action)
        ok6 = ok6 and all(partitions_ok(m, taken_of(w)) for m in masks.values())
        h, hm = history(steps, p, truth[q], w["lost"], births)
        hist_part[q] = h
        ok7 = (ok7 and history_ok(hm, h, w["lost"])
               and final_right & truth[q] == w["right"]
               and (at_peak & ~final_right & truth[q]).bit_count() == fall_lost.get(q, 0))
        peak_part[q] = by_peak(w, at_peak)
        lever_part[q] = given_back(got, truth[q])
    gates.append({"gate": 6, "what": "the takers partition the taken points, and every report "
                                     "names its ticket's true queue",
                  "passes": ok6})
    gates.append({"gate": 7, "what": "the last losses partition what was right once, the "
                                     "replay is the final base, and the peak is fall.json's",
                  "passes": ok7})
    gates.append({"gate": 8, "what": "each lever is its record's",
                  "passes": levers_ok(got, truth, n, fall_run, paths_run, carry_run)})
    out.update({
        "oncall": oncall_run,
        "security": security,
        "takers": taken_part,
        "history": hist_part,
        "by_peak": peak_part,
        "levers": {"summaries": {k: summary_of(g, truth, n) for k, g in got.items()},
                   "doors_left_out": [list(e) for e in cr.door_edges(gateway_run)],
                   "by_queue": lever_part},
        "gates": [{"queue": QUEUE, **g} for g in oncall_run["reading"]["gates"]]
                 + [{"queue": SEC, **g} for g in security["gates"]]
                 + [{"queue": None, **g} for g in gates],
        "added_after_the_first_run": added,
    })
    return out


def read_all_runs(records: dict[str, dict], score: dict[str, Any], fall_record: dict[str, Any],
                  paths_record: dict[str, Any], carry_record: dict[str, Any],
                  gateway_record: dict[str, Any], space: Space, truth: dict[str, int],
                  cases: Sequence) -> dict[str, dict]:
    regions = rl_refs.regions()
    stage_c = stage_c_counts(score, {q: truth[q].bit_count() for q in QUEUES})
    oncall = O.read_all_runs(records, stage_c)
    for t, rec in records.items():
        oncall[t]["holding_h05_whole"] = O.holds_whole(
            MI.final_engine(rec), QUEUE, O.parts(truth[QUEUE], regions)[H05])
    return {t: read_run(rec, oncall[t], space, truth, cases, regions, stage_c,
                        fall_record["runs"][t], paths_record["runs"][t], carry_record["runs"][t],
                        gateway_record["runs"][t], t)
            for t, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    got = {t: runs[t] for t in L_RUNS if t in runs}

    def reading(part: Callable[[dict], tuple[int, int]]) -> dict[str, Any]:
        per = {t: part(r) for t, r in got.items()}
        num = sum(v[0] for v in per.values())
        den = sum(v[1] for v in per.values())
        return {"part": num, "of": den, "share": frac(share(num, den)),
                "runs": {t: {"part": a, "of": b} for t, (a, b) in per.items()}}

    def holds(rd: dict[str, Any]) -> bool:
        return bool(got) and rd["of"] > 0 and F(rd["part"], rd["of"]) >= O_HALF

    def at(r, q, when, k):
        return r["by_peak"][q][when][k]

    o1 = reading(lambda r: (at(r, QUEUE, AT_PEAK, "contested"), at(r, QUEUE, AT_PEAK, "lost")))
    o2 = reading(lambda r: (at(r, QUEUE, BEFORE_PEAK, "outranked"),
                            at(r, QUEUE, BEFORE_PEAK, "lost")))
    o3 = reading(lambda r: (r["oncall"]["reading"]["ways"]["by_edge"],
                            r["oncall"]["reading"]["ways"]["outranked"]))
    o4 = reading(lambda r: (r["takers"][QUEUE]["by_cause"][EVERY], r["takers"][QUEUE]["points"]))
    o5 = reading(lambda r: (r["takers"][QUEUE]["by_layer"][EVERY], r["takers"][QUEUE]["points"]))
    o6 = reading(lambda r: (r["levers"]["by_queue"][QUEUE][LOSSES_FIRST]["gives_back"],
                            at(r, QUEUE, AT_PEAK, "lost")))
    o7 = reading(lambda r: (r["by_peak"][SEC][BEFORE_PEAK]["by_queue"].get(T2, 0),
                            at(r, SEC, BEFORE_PEAK, "lost")))
    return [
        {"clause": "O1", "what": "at least half of the queue's points lost at the peak are "
                                 "contested conflicts",
         "reading": o1, "holds": holds(o1)},
        {"clause": "O2", "what": "at least half of the queue's points lost before the peak are "
                                 "outranked",
         "reading": o2, "holds": holds(o2)},
        {"clause": "O3", "what": "at least half of the queue's outranked points are outranked "
                                 "by an edge",
         "reading": o3, "holds": holds(o3)},
        {"clause": "O4", "what": "at least half of the queue's taken points are decided only by "
                                 "rules born at a reported error",
         "reading": o4, "holds": holds(o4)},
        {"clause": "O5", "what": "at least half of the queue's taken points are decided only by "
                                 "rules born at tickets H06, H07 or H08 governs",
         "reading": o5, "holds": holds(o5)},
        {"clause": "O6", "what": "installed losses first, the replay gives back at least half "
                                 "as many of the queue's points as were lost at the peak",
         "reading": o6, "holds": holds(o6)},
        {"clause": "O7", "what": "at least half of SECURITY_INCIDENT's points lost before the "
                                 "peak are decided by T2_TECHNICAL",
         "reading": o7, "holds": holds(o7)},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], ...]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return (records, json.loads(plan.score_path().read_text()),
            json.loads(fl.record_path().read_text()), json.loads(pa.record_path().read_text()),
            json.loads(cr.record_path().read_text()), json.loads(gw.record_path().read_text()))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why L loses ONCALL_ESCALATION (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 8 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/oncall.py writes {record_path()}")
    records, score, fall_record, paths_record, carry_record, gateway_record = read_all()
    runs = read_all_runs(records, score, fall_record, paths_record, carry_record,
                         gateway_record, MI.space(), MI.space_truth(), list(all_cases()))
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        q = f" {g['queue']}" if g["queue"] else ""
        print(f"  gate {g['gate']} run {g['run']}{q}: {'PASS' if g['passes'] else 'FAIL'}"
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
        "added_after_the_first_run": ADDED,
        "source": {"score": str(plan.score_path()), "fall": str(fl.record_path()),
                   "paths": str(pa.record_path()), "carry": str(cr.record_path()),
                   "gateway": str(gw.record_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "fall_from": fall_record["_env"].get("git_commit"),
                   "paths_from": paths_record["_env"].get("git_commit"),
                   "carry_from": carry_record["_env"].get("git_commit"),
                   "gateway_from": gateway_record["_env"].get("git_commit")},
        "surface": "the whole space, 134,400 points: each run's final base, its base after "
                   "every birth, and the final base of each replay",
        "queues": list(QUEUES),
        "parts": {H04: "the queue's points in H04's region, 4,200",
                  H05: "the queue's points in H05's region, 2,100"},
        "constants": {"O_HALF": str(O_HALF), "LAYER": list(LAYER)},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        w = r["oncall"]["reading"]["ways"]
        g = r["levers"]["by_queue"][QUEUE]
        print(f"  {t}: {QUEUE} lost {w['lost']}, contested {w['contested']}, unwritten "
              f"{w['unwritten']}, outranked {w['outranked']} (by edge {w['by_edge']}); "
              f"gives back " + ", ".join(f"{k} {g[k]['gives_back']}" for k in LEVERS))
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
