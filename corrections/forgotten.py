"""
WHY THE FINAL BASE FORGETS ITS CORRECTIONS.
Stage C found it. At the end of each L run its final base decides right 128 of
the 252 arrivals that are labelled tickets or their repeats, 128 of 249 and 115
of 263. Yet its proposer named the reported queue at every first call that named
a queue (`CR-a`). `FINDINGS_CORRECTIONS.md`, *What Stage C does not settle*,
item 2, and `IDEAS.md` carry the question: whether a later rule, a declared edge
or a refused placement takes each one back. Asked for by Sergi on 2026-11-14,
after Stage C. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
A *labelled point* of an L run is the ticket of an escalation caused by a
reported error, which the run handed its own label. It is a point of the space,
counted once however often it arrived or was reported. Its *first report* is the
first such escalation at it. It is *forgotten* when the run's final base does not
decide it right.

**The base is replayed in birth order**, each rule added at its case and its
edges tried after it in `edge_log` order, as `channel/lost.py` replays it. A
birth changes a point's decision only when the newborn rule matches the point,
because every edge tried at a birth has the newborn at one end. So each labelled
point is read right after its first report's birth, and then right after every
later birth whose rule matches it.

**Every labelled point is in one class**:
  kept         the final base decides it right;
  never_born   forgotten, no base from its first report on decided it right,
               and none of its reports bore a rule;
  never_right  forgotten, no base from its first report on decided it right,
               though some report of it bore a rule;
  taken_back   forgotten, though some base from its first report on decided it
               right.

**A point taken back is read at its last loss**: the last birth after which it
went from right to wrong. The newborn rule matches the point there, and the loss
is one of three:
  by_containment  the newborn decides the point alone, and its region is nested
                  inside that of every rule undefeated there before;
  by_edge         the newborn decides it alone, and beats some rule undefeated
                  there before by a declared edge;
  conflict        the newborn is left undefeated beside a rule of the point's
                  queue, or no rule is left undefeated.
Each loss also gives the newborn's queue, and the cause of the escalation it was
born at: a reported error, an impasse or a conflict. It gives whether the point
arrived again after the loss, and was reported.

**A point never right is read at each of its reports that bore a rule**, right
after the birth. It gives why the newborn did not decide its own ticket:
  not_matching   the rule does not match its ticket;
  wrong_queue    its queue is not the label's;
  nested         a matching rule nested inside it beats it there by
                 containment. It says whether that rule decided the reported
                 case;
  edge           it is beaten there by a declared edge, and by no rule nested
                 inside it;
  conflict       it is undefeated there beside a rule of another queue.
The same reading, at every born report of every labelled point, gives how often
a report that bore a rule left its point right.

**A point never born is read at its reports**: the verdict each ended with. It
was unplaced, refused or changed, or its call failed. An empty object is
refused, as an invalid rule.

**Every forgotten point is also read in the final base**, in `channel/lost.py`'s
ways, here for one point and its true queue:
- an impasse;
- a conflict;
- unwritten: another queue decides it, and no rule of its queue matches it;
- outranked: another queue decides it though a rule of its queue matches it, by
  an edge or by containment.

**Arm N is not read.** No label reached its proposer, so it has no labelled
point.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its rules, their extensions and its declared
     edges are `manual.instrument.final_engine`'s rebuild, compared as
     `channel/lost.py`'s gate 1 compares them.
  2. **The labels are the record's.** `corrections.ask.labelled` reads every
     reported error with its own label. The run's labels, and its labelled
     points, are as many as Stage C's table of tickets counts.
  3. **The final base on the labelled arrivals is Stage C's.** It decides right
     as many of the labelled tickets and their repeats as `score.json` says, of
     as many.
  4. **Every reading is the engine's.** At every point read, the outcome and the
     queue the reading gives are `PriorityEngine.decide`'s. Every loss to a
     decision is the newborn's alone, and each point's last reading is the
     final base's decision.
  5. **The classes partition the labelled points, and the reports are the
     record's.** Each report's verdict is its escalation's, and each born
     verdict names the rule born at its case.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
F1 and F2 read each L run. F3 to F6 pool the three.

  F1. **Never compiled.** In each L run, at least a quarter of the forgotten
      points are never_born.
  F2. **Compiled, then taken back.** In each L run, at least a quarter of the
      forgotten points are taken_back.
  F3. **Right at birth.** Of the reports of labelled points that bore a rule, at
      least three quarters left their point decided right just after the birth.
  F4. **Taken by a rule alone.** At least half of the last losses are
      by_containment or by_edge, and not a conflict.
  F5. **Corrections take back corrections.** Among the newborns of the last
      losses, the share born at a reported error is at least the share of
      births at a reported error among all of the three runs' births.
  F6. **Never seen again.** At least three quarters of the points taken back did
      not arrive again after their last loss.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account.** The base forgets in two ways of comparable size.
- **Some corrections were never compiled.** The placement round left the draft
  unplaced, or the provider answered with an empty object. The point was not
  reported again, or its next report was not born either.
- **The rest were compiled, and right at birth.** The proposer named the label,
  and the draft beat the rule that had erred there.
- **Later rules took them back.** A later rule matching the point decided it for
  another queue. It was mostly another correction, placed above the earlier one
  in its placement round, or nested inside it.
- **The channel could not mend them.** It reports a wrong decision only at an
  arrival. Few arrivals repeat an earlier ticket, so a point lost after its
  report was mostly not seen again.

**The bet is F5.** Told that the engine had erred, the proposer placed its
correction above the listed rules, so corrections take the points of earlier
ones more often than the other births do. **F6 is trusted most**: Stage A
counted 257 of the 2,000 arrivals repeating an earlier ticket. **F1 is trusted
least**: L r3 met no empty object, so its points never born are the unplaced
ones alone.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and `score.json`'s `CR-g`. That includes the
  final bases on the labelled arrivals and the rest, the online figures, the
  curves at the checkpoints, and each run's escalations by cause. It includes
  the empty objects, the labels handed and the distinct labelled tickets;
- the field names of a loop record, an escalation, a call and a rule;
- in L r1's record: the verdicts over all its escalations, 282 born, 65
  unplaced, 27 refused and 3 changed; the length of its edge log, 7,254; its
  first escalation, an impasse born as `R0001`; its second row; and its rule
  `R0006` whole;
- `channel/lost.py`, `edges/rebuild.py`, `reasoned_loop/governed.py`,
  `placement/protocol.py`'s v1c escalation, `rung2/engine2.py`'s arbitration and
  `corrections/score.py`.

**What the drafter had not seen**: any labelled point's decision after any
birth, the verdicts of any run's escalations by cause, or any of L r2's or L
r3's verdicts. Nor which rule decides a labelled point, or any rule, region or
edge of any L run but `R0006`.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-14, after Stage C. The expectation
above was written and committed before the reading ran. Not a signed row, not
on `STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m corrections.forgotten --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.forgotten
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.domain import ATTRIBUTES
from harness.provenance import describe, environment

from authorship import protocol as e
from channel import lost as ch_lost
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reasoned_loop import protocol as p
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import ask, plan

F = Fraction

# The classes of a labelled point.
KEPT, NEVER_BORN, NEVER_RIGHT, TAKEN_BACK = "kept", "never_born", "never_right", "taken_back"
CLASSES = (KEPT, NEVER_BORN, NEVER_RIGHT, TAKEN_BACK)
FORGOTTEN = (NEVER_BORN, NEVER_RIGHT, TAKEN_BACK)

# How a point taken back was lost, at its last loss.
BY_CONTAINMENT, BY_EDGE, CONFLICT = "by_containment", "by_edge", "conflict"
LOSSES = (BY_CONTAINMENT, BY_EDGE, CONFLICT)

# Why a born report did not leave its point right.
NOT_MATCHING, WRONG_QUEUE, NESTED, EDGE = "not_matching", "wrong_queue", "nested", "edge"
WHY_NOT = (NOT_MATCHING, WRONG_QUEUE, NESTED, EDGE, CONFLICT)

# The engine's outcomes.
ACTION, IMPASSE, CONFLICT_OUTCOME = "ACTION", "IMPASSE", "CONFLICT"

# The ways a forgotten point is lost in the final base, as `channel/lost.py`
# names them.
WAYS = ("impasse", "conflict", "unwritten", "outranked_by_edge",
        "outranked_by_containment")

# The verdicts an escalation ends with, as the loop records them.
BORN, UNPLACED, REFUSED, CHANGED, FAILED = (e.BORN, e.UNPLACED, e.REJECTED, p.CHANGED,
                                            e.FAILED)

# The expectation's lines.
F1_SHARE = F(1, 4)
F2_SHARE = F(1, 4)
F3_SHARE = F(3, 4)
F4_SHARE = F(1, 2)
F6_SHARE = F(3, 4)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-14, after Stage C. The expectation in the "
    "module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")


def record_path():
    return plan.OUT / "forgotten.json"


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


# ---------------------------------------------------------------------------
# One point, read in a base
# ---------------------------------------------------------------------------

def read_point(engine: PriorityEngine, case, truth: str) -> dict[str, Any]:
    """The point's matching rules, the undefeated among them, the outcome, the
    queue decided and whether it is right. It is `PriorityEngine.decide`'s
    arbitration, keeping the undefeated on an ACTION too; gate 4 holds it to
    `decide` at every reading."""
    matched = [r for r in engine.rules if r.matches(case)]
    ids = {r.rule_id for r in matched}
    und = [r for r in matched if not (engine.beats_me(r.rule_id) & ids)]
    if not matched:
        outcome = IMPASSE
    elif und and len({r.action for r in und}) == 1:
        outcome = ACTION
    else:
        outcome = CONFLICT_OUTCOME
    action = und[0].action if outcome == ACTION else None
    return {"outcome": outcome, "action": action, "right": action == truth,
            "matched": sorted(ids), "undefeated": sorted(r.rule_id for r in und)}


def is_the_engines(engine: PriorityEngine, case, reading: dict[str, Any]) -> bool:
    """Gate 4: the reading's outcome and queue are `decide`'s."""
    outcome, winner, _ = engine.decide(case)
    return (outcome, winner.action if winner else None) == (reading["outcome"],
                                                             reading["action"])


def loss_of(engine: PriorityEngine, before: dict[str, Any], after: dict[str, Any],
            newborn: str) -> str:
    """How a point went from right to wrong at the birth of `newborn`."""
    if after["outcome"] != ACTION:
        return CONFLICT
    for w in before["undefeated"]:
        if (newborn in engine.decl_below.get(w, set())
                and newborn not in engine.sub_below.get(w, set())):
            return BY_EDGE
    return BY_CONTAINMENT


def why_not(engine: PriorityEngine, case, truth: str, rule_id: str,
            erred: str | None) -> dict[str, Any]:
    """Right after the birth of `rule_id` at a report of the point: why it did
    not leave the point right, or `why` None if it did."""
    rules = {r.rule_id: r for r in engine.rules}
    rule = rules[rule_id]
    reading = read_point(engine, case, truth)
    out: dict[str, Any] = {"rule_id": rule_id, "right": reading["right"], "why": None}
    if reading["right"]:
        return out
    if not rule.matches(case):
        out["why"] = NOT_MATCHING
        return out
    if rule.action != truth:
        out["why"] = WRONG_QUEUE
        return out
    beaters = sorted(engine.beats_me(rule_id) & set(reading["matched"]))
    out["beaten_by"] = [{"rule_id": x, "action": rules[x].action} for x in beaters]
    if not beaters:
        out["why"] = CONFLICT
        out["beside"] = [{"rule_id": x, "action": rules[x].action}
                         for x in reading["undefeated"] if rules[x].action != truth]
        return out
    nested = [x for x in beaters if x in engine.sub_below.get(rule_id, set())]
    if nested:
        out["why"] = NESTED
        out["nested"] = nested
        out["erred_is_nested"] = erred in nested
    else:
        out["why"] = EDGE
    out["erred_beats_it"] = erred in beaters
    return out


def final_way(engine: PriorityEngine, case, truth: str) -> str | None:
    """How the final base loses one point of its true queue, in
    `channel/lost.py`'s ways, or None if it decides it right."""
    reading = read_point(engine, case, truth)
    if reading["right"]:
        return None
    if reading["outcome"] == IMPASSE:
        return "impasse"
    if reading["outcome"] == CONFLICT_OUTCOME:
        return "conflict"
    action = {r.rule_id: r.action for r in engine.rules}
    matched = set(reading["matched"])
    own = [x for x in reading["matched"] if action[x] == truth]
    if not own:
        return "unwritten"
    for o in own:
        if any(action[w] != truth for w in engine.decl_below.get(o, set()) & matched):
            return "outranked_by_edge"
    return "outranked_by_containment"


# ---------------------------------------------------------------------------
# The labelled points of a run
# ---------------------------------------------------------------------------

def labelled_points(record: dict[str, Any], corpus: Sequence) -> dict[tuple, dict[str, Any]]:
    """Every labelled point of an L record, keyed by its ticket: its label, its
    reports in arrival order, and every arrival of it. `ask.labelled` refuses a
    record whose labels are not its reported errors'."""
    out: dict[tuple, dict[str, Any]] = {}
    for idx, label in ask.labelled(record):
        key = corpus[idx].key()
        pt = out.setdefault(key, {"case": corpus[idx], "label": label, "reports": [],
                                  "labels": set()})
        pt["reports"].append(idx)
        pt["labels"].add(label)
    for i, case in enumerate(corpus):
        if case.key() in out:
            out[case.key()].setdefault("arrivals", []).append(i)
    return out


def escalation_at(record: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {esc["idx"]: esc for esc in record["escalations"]}


# ---------------------------------------------------------------------------
# The replay
# ---------------------------------------------------------------------------

def replay(record: dict[str, Any], corpus: Sequence, space: Space,
           pts: dict[tuple, dict[str, Any]]) -> dict[str, Any]:
    """The base in birth order. Each labelled point is read right after its
    first report's birth, then right after every later birth whose rule matches
    it. At every report of it that bore a rule, the reading says why that rule
    did not leave it right, if it did not."""
    born = erb.births(record)
    by_birth = erb.edges_by_birth(record)
    rows = {r["idx"]: r for r in record["records"]}
    escs = escalation_at(record)
    starts: dict[int, list[tuple]] = {}
    reports_at: dict[int, list[tuple]] = {}
    for k, pt in pts.items():
        starts.setdefault(pt["reports"][0], []).append(k)
        for idx in pt["reports"]:
            reports_at.setdefault(idx, []).append(k)
    engine = PriorityEngine(space=space)
    tracked: set[tuple] = set()
    state: dict[tuple, dict[str, Any]] = {}
    start: dict[tuple, dict[str, Any]] = {}
    events: dict[tuple, list[dict[str, Any]]] = {k: [] for k in pts}
    at_reports: dict[tuple, list[dict[str, Any]]] = {k: [] for k in pts}
    engines_ok = True
    for idx in sorted(set(born) | set(starts)):
        if idx in born:
            d = born[idx]
            rule = rule_from(d)
            hit = [k for k in sorted(tracked) if rule.matches(pts[k]["case"])]
            before = {k: state[k] for k in hit}
            engine.add(rule, born_at=idx, keep_id=True)
            for edge in by_birth.get(idx, []):
                engine.try_edge(edge.winner, edge.loser)
            for k in hit:
                after = read_point(engine, pts[k]["case"], pts[k]["label"])
                engines_ok &= is_the_engines(engine, pts[k]["case"], after)
                if after["right"] != before[k]["right"]:
                    ev = {"born_at": idx, "rule_id": d["rule_id"], "action": d["action"],
                          "cause": (escs.get(idx) or {}).get("kind"),
                          "lost": before[k]["right"],
                          "before": before[k]["undefeated"], "after": after["undefeated"]}
                    if before[k]["right"]:
                        ev["how"] = loss_of(engine, before[k], after, d["rule_id"])
                        if ev["how"] != CONFLICT and after["undefeated"] != [d["rule_id"]]:
                            engines_ok = False      # a loss to a decision is the newborn's
                    events[k].append(ev)
                state[k] = after
            for k in reports_at.get(idx, []):
                if k in tracked:
                    at_reports[k].append({"report": idx, **why_not(
                        engine, pts[k]["case"], pts[k]["label"], d["rule_id"],
                        (rows.get(idx) or {}).get("engine_rule"))})
        for k in starts.get(idx, []):
            reading = read_point(engine, pts[k]["case"], pts[k]["label"])
            engines_ok &= is_the_engines(engine, pts[k]["case"], reading)
            state[k] = start[k] = reading
            tracked.add(k)
            if idx in born:
                at_reports[k].append({"report": idx, **why_not(
                    engine, pts[k]["case"], pts[k]["label"], born[idx]["rule_id"],
                    (rows.get(idx) or {}).get("engine_rule"))})
    return {"engine": engine, "state": state, "start": start, "events": events,
            "at_reports": at_reports, "engines_ok": engines_ok}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def class_of(verdicts: list[str], start: dict[str, Any], events: list[dict[str, Any]],
             final_right: bool) -> str:
    """A labelled point's class, from its reports' verdicts, its reading right
    after its first report's birth, its later changes and its final decision."""
    if final_right:
        return KEPT
    ever_right = start["right"] or any(not ev["lost"] for ev in events)
    if ever_right:
        return TAKEN_BACK
    return NEVER_RIGHT if BORN in verdicts else NEVER_BORN


def after(record_rows: dict[int, dict], arrivals: list[int], since: int) -> dict[str, int]:
    """The point's arrivals after case `since`, and how many were reported."""
    later = [i for i in arrivals if i > since]
    return {"arrivals": len(later),
            "reported": sum(1 for i in later if (record_rows.get(i) or {}).get("reported")),
            "escalated": sum(1 for i in later if (record_rows.get(i) or {}).get("escalated"))}


def key_of(case) -> dict[str, Any]:
    return {a: getattr(case, a) for a in ATTRIBUTES}


def read_run(record: dict[str, Any], corpus: Sequence, space: Space,
             stage_c: dict[str, Any], truth: Sequence[str] | None = None,
             final: PriorityEngine | None = None) -> dict[str, Any]:
    """Every labelled point of one L run, classed, and the gates. `truth` is
    every arrival's corpus label, `plan.labels()` by default, and `final` the
    run's final base, `manual.instrument.final_engine`'s by default."""
    final = final if final is not None else MI.final_engine(record)
    truth = list(truth) if truth is not None else [t for t, _ in plan.labels()]
    pts = labelled_points(record, corpus)
    rep = replay(record, corpus, space, pts)
    rows = {r["idx"]: r for r in record["records"]}
    escs = escalation_at(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    out_points = []
    classes: Counter = Counter()
    last_is_final = True
    for k in sorted(pts, key=lambda k: pts[k]["reports"][0]):
        pt = pts[k]
        verdicts = [escs[i]["verdict"] for i in pt["reports"]]
        final_reading = read_point(final, pt["case"], pt["label"])
        last = rep["state"][k]
        last_is_final &= (last["outcome"], last["action"]) == (final_reading["outcome"],
                                                              final_reading["action"])
        c = class_of(verdicts, rep["start"][k], rep["events"][k], final_reading["right"])
        classes[c] += 1
        row: dict[str, Any] = {
            "ticket": key_of(pt["case"]), "label": pt["label"], "class": c,
            "reports": [{"idx": i, "verdict": escs[i]["verdict"],
                         "rule_id": escs[i].get("rule_id")} for i in pt["reports"]],
            "arrivals": pt["arrivals"], "right_after_first_report": rep["start"][k]["right"],
            "events": rep["events"][k], "at_born_reports": rep["at_reports"][k],
            "final": {"outcome": final_reading["outcome"], "action": final_reading["action"],
                      "undefeated": final_reading["undefeated"]},
        }
        if c != KEPT:
            row["final_way"] = final_way(final, pt["case"], pt["label"])
        if c == TAKEN_BACK:
            last = [ev for ev in rep["events"][k] if ev["lost"]][-1]
            row["last_loss"] = {**last, "newborn": {
                "rule_id": last["rule_id"], "action": last["action"], "cause": last["cause"],
                "conditions": rules[last["rule_id"]]["conditions"]}}
            row["after_last_loss"] = after(rows, pt["arrivals"], last["born_at"])
        elif c in (NEVER_BORN, NEVER_RIGHT):
            row["after_first_report"] = after(rows, pt["arrivals"], pt["reports"][0])
        out_points.append(row)

    labelled_keys = set(pts)
    arrivals_right = arrivals_n = 0
    for i, case in enumerate(corpus):
        if case.key() in labelled_keys:
            outcome, winner, _ = final.decide(case)
            arrivals_right += (winner is not None and outcome != CONFLICT_OUTCOME
                               and winner.action == truth[i])
            arrivals_n += 1
    sc_corpus = stage_c["runs"]["corpus"]["labelled"]
    sc_curve = stage_c["curve_last"]["learners"]
    n_labels = sum(len(pt["reports"]) for pt in pts.values())
    reports_ok = all(len(pt["labels"]) == 1 for pt in pts.values()) and all(
        escs[i]["verdict"] in (BORN, UNPLACED, REFUSED, CHANGED, FAILED)
        and (escs[i]["verdict"] != BORN
             or (escs[i].get("rule_id") in rules
                 and rules[escs[i]["rule_id"]]["born_at"] == i))
        for pt in pts.values() for i in pt["reports"])
    gates = [
        {"gate": 1, "what": "the replay is the base",
         "passes": ch_lost.same_base(final, rep["engine"])},
        {"gate": 2, "what": "the labels are the record's, as many as Stage C counts",
         "passes": n_labels == sc_curve["labels"]
                   and len(pts) == sc_curve["distinct_tickets"]},
        {"gate": 3, "what": "the final base on the labelled arrivals is Stage C's",
         "passes": [arrivals_right, arrivals_n] == list(sc_corpus)},
        {"gate": 4, "what": "every reading is the engine's, and each point's last "
                            "reading is the final base's",
         "passes": rep["engines_ok"] and last_is_final},
        {"gate": 5, "what": "the classes partition the labelled points, and the reports "
                            "are the record's",
         "passes": sum(classes.values()) == len(pts) and set(classes) <= set(CLASSES)
                   and reports_ok},
    ]
    return {"points": out_points, "summary": summarise(out_points, record),
            "labelled_points": len(pts), "labels": n_labels,
            "labelled_arrivals": [arrivals_right, arrivals_n], "gates": gates}


def summarise(points: list[dict[str, Any]], record: dict[str, Any]) -> dict[str, Any]:
    classes = Counter(x["class"] for x in points)
    taken = [x for x in points if x["class"] == TAKEN_BACK]
    forgotten = [x for x in points if x["class"] != KEPT]
    born_reports = [r for x in points for r in x["at_born_reports"]]
    births_by_cause = Counter(esc["kind"] for esc in record["escalations"]
                              if esc["verdict"] == BORN)
    return {
        "classes": {c: classes.get(c, 0) for c in CLASSES},
        "forgotten": len(forgotten),
        "last_losses": {h: sum(1 for x in taken if x["last_loss"]["how"] == h)
                        for h in LOSSES},
        "last_loss_newborn_cause": dict(Counter(x["last_loss"]["cause"] for x in taken)),
        "last_loss_newborn_queue": dict(Counter(x["last_loss"]["action"] for x in taken)),
        "taken_back_arrived_again": sum(1 for x in taken
                                        if x["after_last_loss"]["arrivals"]),
        "taken_back_reported_again": sum(1 for x in taken
                                         if x["after_last_loss"]["reported"]),
        "born_reports": len(born_reports),
        "born_reports_right": sum(1 for r in born_reports if r["right"]),
        "why_not": dict(Counter(r["why"] for r in born_reports if not r["right"])),
        "why_not_never_right": dict(Counter(
            r["why"] for x in points if x["class"] == NEVER_RIGHT
            for r in x["at_born_reports"])),
        "never_born_verdicts": dict(Counter(
            r["verdict"] for x in points if x["class"] == NEVER_BORN for r in x["reports"])),
        "final_ways": {w: sum(1 for x in forgotten if x.get("final_way") == w)
                       for w in WAYS},
        "losses_in_all": sum(1 for x in points for ev in x["events"] if ev["lost"]),
        "kept_after_a_loss": sum(1 for x in points if x["class"] == KEPT
                                 and any(ev["lost"] for ev in x["events"])),
        "births_by_cause": dict(births_by_cause),
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    sums = {t: r["summary"] for t, r in runs.items()}

    def per_run(cls: str) -> dict[str, Any]:
        return {t: {cls: s["classes"][cls], "of_forgotten": s["forgotten"],
                    "share": frac(share(s["classes"][cls], s["forgotten"]))}
                for t, s in sums.items()}

    def each(cls: str, line: Fraction) -> bool:
        return bool(sums) and all(s["forgotten"] and F(s["classes"][cls], s["forgotten"]) >= line
                                  for s in sums.values())

    born = sum(s["born_reports"] for s in sums.values())
    right = sum(s["born_reports_right"] for s in sums.values())
    taken = sum(s["classes"][TAKEN_BACK] for s in sums.values())
    alone = sum(s["last_losses"][BY_CONTAINMENT] + s["last_losses"][BY_EDGE]
                for s in sums.values())
    takers_error = sum(s["last_loss_newborn_cause"].get(plan.ERROR, 0) for s in sums.values())
    births = sum(sum(s["births_by_cause"].values()) for s in sums.values())
    births_error = sum(s["births_by_cause"].get(plan.ERROR, 0) for s in sums.values())
    again = sum(s["taken_back_arrived_again"] for s in sums.values())
    takers_share, births_share = share(takers_error, taken), share(births_error, births)
    return [
        {"clause": "F1", "what": "in each L run, at least a quarter of the forgotten points "
                                 "are never_born",
         "reading": per_run(NEVER_BORN), "holds": each(NEVER_BORN, F1_SHARE)},
        {"clause": "F2", "what": "in each L run, at least a quarter of the forgotten points "
                                 "are taken_back",
         "reading": per_run(TAKEN_BACK), "holds": each(TAKEN_BACK, F2_SHARE)},
        {"clause": "F3", "what": "at least three quarters of the born reports left their "
                                 "point right just after the birth",
         "reading": {"right": right, "of": born, "share": frac(share(right, born))},
         "holds": born > 0 and F(right, born) >= F3_SHARE},
        {"clause": "F4", "what": "at least half of the last losses are to a newborn "
                                 "deciding the point alone",
         "reading": {"alone": alone, "of": taken, "share": frac(share(alone, taken))},
         "holds": taken > 0 and F(alone, taken) >= F4_SHARE},
        {"clause": "F5", "what": "the share of the last losses' newborns born at a reported "
                                 "error is at least that of all births",
         "reading": {"takers_at_a_reported_error": takers_error, "of_takers": taken,
                     "takers_share": frac(takers_share),
                     "births_at_a_reported_error": births_error, "of_births": births,
                     "births_share": frac(births_share)},
         "holds": takers_share is not None and births_share is not None
                  and takers_share >= births_share},
        {"clause": "F6", "what": "at least three quarters of the points taken back did not "
                                 "arrive again after their last loss",
         "reading": {"not_again": taken - again, "of": taken,
                     "share": frac(share(taken - again, taken))},
         "holds": taken > 0 and F(taken - again, taken) >= F6_SHARE},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(plan.LABELLED, k): json.loads(
        plan.run_path(plan.LABELLED, k).read_text()) for k in range(1, plan.REPS + 1)}
    return records, json.loads(plan.score_path().read_text())


def stage_c_of(score: dict[str, Any], tag: str) -> dict[str, Any]:
    return {"runs": score["CR-g"]["runs"][tag], "curve_last": score["CR-g"]["curves"][tag][-1]}


def plain(x: Any) -> Any:
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, (set, frozenset)):
        return sorted(x)
    if isinstance(x, tuple):
        return list(x)
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the final base forgets its corrections "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/forgotten.py writes {record_path()}")
    records, score = read_all()
    corpus = list(MI.corpus())
    space = MI.space()
    runs = {t: read_run(rec, corpus, space, stage_c_of(score, t)) for t, rec in records.items()}
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
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
                   "score_from": score["_env"].get("git_commit")},
        "surface": "the labelled points of each L run, points of the space read at "
                   "their tickets",
        "constants": {"F1_SHARE": str(F1_SHARE), "F2_SHARE": str(F2_SHARE),
                      "F3_SHARE": str(F3_SHARE), "F4_SHARE": str(F4_SHARE),
                      "F6_SHARE": str(F6_SHARE)},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: {s['classes']}, last losses {s['last_losses']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
