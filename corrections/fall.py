"""
WHY THE LOOP'S SHARE OF THE SPACE PEAKED AND FELL.
Stage C read L's base after the label at each checkpoint. Its share of the
space peaked well before its last label in every run, and fell: L r2's from
0.7597 at its 20th label to 0.4221 at its 209th. `IDEAS.md`, *What
`PLAN_CORRECTIONS.md` opens*, carries the question. Asked for by Sergi on
2026-11-14, after the readings of why the final base forgets its corrections
and why the first call writes them broad. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**The base is replayed in birth order**, each rule added at its case and its
edges tried after it in `edge_log` order, as `corrections/forgotten.py` replays
it. It is read over the whole space after every birth, by masks, as
`manual.instrument.over_space` reads it. A point is *right* when the base
decides it for its true queue.

**The peak** is the first birth after which the most points are right. **The
fall** is the share right at the peak less the share right in the final base.
**The points lost** are those right at the peak and not right in the final
base, and **the points gained** the reverse. The fall is the points lost less
the points gained, over the space's 134,400.

**A birth changes a point only where its rule matches it**, because every edge
tried at a birth has the newborn at one end. A point the birth leaves not right
that was right before is a *loss* at that birth, of one of three kinds, as
`corrections/forgotten.py` names them:
  by_containment  the newborn decides the point alone, and beats every rule
                  undefeated there before by containment;
  by_edge         the newborn decides it alone, and beats some rule undefeated
                  there before by a declared edge;
  conflict        the newborn is left undefeated beside a rule of the point's
                  true queue.

**Each point lost is read at its last loss**: the last birth after the peak at
which it went from right to not right. That birth gives the kind, the newborn's
queue and conditions, and the cause of the escalation it was born at: a
reported error, an impasse or a conflict. Each point lost is also read in the
final base: the queue that decides it there, or a conflict, or an impasse. The
points gained are read by their true queue.

**Arm N is read the same way**, as the control. Its proposer was never handed a
label nor told that the base had erred, and both arms of run `k` read the same
draws.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its rules, their extensions and its declared
     edges are `manual.instrument.final_engine`'s rebuild, compared as
     `channel/lost.py`'s gate 1 compares them.
  2. **The curve is Stage C's.** At every checkpoint of an L run, the share
     right after the last birth at or before the checkpoint's case is
     `score.json`'s `loop`. Every run's final share is `score.json`'s `space`.
  3. **Every reading is the engine's.** At every birth, the lowest and the
     highest point of what it lost, of what it gained and of the newborn's
     extension are decided by the masks as `PriorityEngine.decide` decides
     them, and so is every 997th point of the final base. Also:
     - every edge tried at a birth has the newborn at one end;
     - every change of a decision lies inside the newborn's extension;
     - every loss to a decision is the newborn's alone;
     - no point lost is left with no rule undefeated;
     - the masks kept birth by birth are `blind.rows.undefeated_masks`' over
       the final base.
  4. **The last losses partition the points lost.** Each point lost has one
     last loss after the peak, and its three kinds partition the points lost.
     From the peak on, the points right move at each birth by what it gained
     less what it lost.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Q1 and Q5 read each L run. Q2 to Q4 pool the three. Q6 reads each pair of runs
under the same draws.

  Q1. **The keyword's queue.** In each L run, at least half of the points lost
      are `SECURITY_INCIDENT`'s.
  Q2. **Taken whole.** At least half of the points lost were lost, at their last
      loss, to a newborn that decides them alone, by containment or by an edge.
  Q3. **Taken by the corrections.** The share of the points lost whose last loss
      was to a rule born at a reported error is at least the share of births at
      a reported error among the births after the peaks.
  Q4. **By `T2_TECHNICAL`.** At least half of the `SECURITY_INCIDENT` points
      lost were lost to rules of `T2_TECHNICAL`.
  Q5. **At a few births.** In each L run, the ten births that took the most of
      its points lost, at their last losses, took at least half of them.
  Q6. **The label's, not the loop's.** In each pair of runs under the same
      draws, N's fall is smaller than L's.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account.**
- **The peak is the catalogue's.** The early base holds what the catalogue
  says, the security keyword's rule above all. `SECURITY_INCIDENT` is three
  eighths of the space, all of it in the keyword half.
- **Then the labels come where the catalogue errs.** At the tickets of `H03`,
  security mentions on small accounts at low severity, the label is
  `T2_TECHNICAL`. The correction is placed above the rule that decided the
  ticket, or nested inside it. Its region reaches past `H03`'s tickets into
  `H01`'s and `H02`'s.
- **So the share falls in the keyword half.** A few corrections take it, mostly
  of `T2_TECHNICAL`, each over a region far larger than its ticket.
- **N's proposer is never told.** At the same tickets it writes the catalogue's
  queue again, and its share does not fall as far.

**The bet is Q4.** `PLAN_WHOLE.md`'s v1c lost part of the keyword half to a rule
of `T2_TECHNICAL` drafted at a ticket of `H03` that dropped the tier. Here the
report names `T2_TECHNICAL` at every reported ticket of `H03`. **Q1 is trusted
most**: L's final bases recall 0.3514, 0.1437 and 0.2976 of
`SECURITY_INCIDENT`, where N's recall 0.925, 1 and 0.6929. **Q3 is trusted
least**: `corrections/forgotten.py`'s F5 bet the same of the labelled points'
takers, and failed. They were born at conflicts more often.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and `score.json`'s `CR-g`. That includes the
  final bases' shares and recalls, the curves at the checkpoints, and each
  run's escalations by cause;
- `forgotten.json` and `broad.json`, and their sections;
- the hidden policy and the level 1 catalogue's text;
- each queue's points of the space and of the keyword half, counted for this
  reading: `SECURITY_INCIDENT` holds 50,400 points, all in the keyword half,
  and `T2_TECHNICAL` 36,720, of which 16,800 are in it;
- `placement/protocol.py`'s v1c list, `rung2/engine2.py`'s arbitration,
  `manual/instrument.py`'s `over_space`, `blind/rows.py`'s masks,
  `corrections/score.py`'s `base_after` and `corrections/forgotten.py`'s
  replay.

**What the drafter had not seen**: any base's share after any birth but at the
checkpoints, so neither any run's peak between checkpoints nor any N run's
curve. Nor any point lost or gained, nor which rule decides any point of the
space in any base.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-14, after the two readings above.
The expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m corrections.fall --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.fall
"""

from __future__ import annotations

import argparse
import json
import sys
from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.provenance import describe, environment

from blind import rows as brows
from channel import lost as ch_lost
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import forgotten as fg
from . import plan

F = Fraction
SEC, T2 = "SECURITY_INCIDENT", "T2_TECHNICAL"
UNLABELLED = next(a for a in plan.ARMS if a != plan.LABELLED)

# How a point was lost at a birth, as `corrections/forgotten.py` names it.
BY_CONTAINMENT, BY_EDGE, CONFLICT = fg.BY_CONTAINMENT, fg.BY_EDGE, fg.CONFLICT
LOSSES = fg.LOSSES

# The engine's outcomes.
ACTION, IMPASSE, CONFLICT_OUTCOME = fg.ACTION, fg.IMPASSE, fg.CONFLICT_OUTCOME

# Gate 3 reads every STRIDE-th point of the final base against `decide`.
STRIDE = 997

# The expectation's lines.
Q1_SHARE = F(1, 2)
Q2_SHARE = F(1, 2)
Q4_SHARE = F(1, 2)
Q5_TOP = 10
Q5_SHARE = F(1, 2)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-14, after the readings of why the final base "
    "forgets its corrections and why the first call writes them broad. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")


def record_path():
    return plan.OUT / "fall.json"


share, frac = fg.share, fg.frac


# ---------------------------------------------------------------------------
# A base, by masks
# ---------------------------------------------------------------------------

def decision(und: dict[str, int], action: dict[str, str]) -> dict[str, Any]:
    """The base's decision over the space: each queue's points where one of its
    rules is undefeated, the points where some rule is (`one`), and those where
    rules of two queues are (`two`). `reuse.structure.subsumption_on_space`'s
    arbiter."""
    by_queue: dict[str, int] = {}
    for rid, m in und.items():
        by_queue[action[rid]] = by_queue.get(action[rid], 0) | m
    one = two = 0
    for m in by_queue.values():
        two |= one & m
        one |= m
    return {"by_queue": by_queue, "one": one, "two": two}


def right_of(dec: dict[str, Any], truth: dict[str, int]) -> int:
    """The points the base decides for their true queue."""
    only = dec["one"] & ~dec["two"]
    out = 0
    for q, m in dec["by_queue"].items():
        out |= m & only & truth.get(q, 0)
    return out


def reading_at(dec: dict[str, Any], j: int) -> tuple[str, str | None]:
    """The outcome and the queue the masks give at bit `j`."""
    if not (dec["one"] >> j) & 1:
        return IMPASSE, None
    if (dec["two"] >> j) & 1:
        return CONFLICT_OUTCOME, None
    return ACTION, next(q for q, m in dec["by_queue"].items() if (m >> j) & 1)


def is_the_engines(engine: PriorityEngine, case, dec: dict[str, Any], j: int) -> bool:
    """Gate 3: the masks' outcome and queue at bit `j` are `decide`'s at its
    case."""
    outcome, winner, _ = engine.decide(case)
    return (outcome, winner.action if winner else None) == reading_at(dec, j)


def ends(m: int) -> list[int]:
    """The lowest and the highest point of a mask."""
    if not m:
        return []
    lo, hi = (m & -m).bit_length() - 1, m.bit_length() - 1
    return [lo] if lo == hi else [lo, hi]


def counts_by_queue(m: int, truth: dict[str, int]) -> dict[str, int]:
    """A mask's points by true queue, the queues it holds none of left out."""
    out = {q: (m & truth[q]).bit_count() for q in ACTIONS if q in truth}
    return {q: k for q, k in out.items() if k}


def keyword(space: Space) -> int:
    return space.mask["has_security_keyword"][True]


# ---------------------------------------------------------------------------
# The replay
# ---------------------------------------------------------------------------

def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           cases: Sequence) -> dict[str, Any]:
    """The base in birth order, read over the space after every birth: what is
    right, and what the birth lost and gained, each loss by its kind. `cases` is
    the space's enumeration, case `k` at bit `n - 1 - k`."""
    born = erb.births(record)
    by_birth = erb.edges_by_birth(record)
    escs = fg.escalation_at(record)
    errors = sorted(e["idx"] for e in record["escalations"] if e["kind"] == plan.ERROR)
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    dec = decision(und, action)
    right = 0
    n = space.n
    steps: list[dict[str, Any]] = []
    ok = {"decide": True, "newborn_at_each_end": True, "inside": True, "alone": True,
          "undefeated": True}
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        edges = by_birth.get(idx, [])
        ok["newborn_at_each_end"] &= all(rid in (e.winner, e.loser) for e in edges)
        for e in edges:
            engine.try_edge(e.winner, e.loser)
        ext = engine.ext[rid]
        action[rid] = d["action"]
        # Where a rule the newborn beats by a declared edge was undefeated before.
        edge_beaten = 0
        for u in engine.decl_above[rid]:
            edge_beaten |= und.get(u, 0)
        for u in engine.wins_over(rid):
            und[u] &= ~ext
        dominated = 0
        for b in engine.beats_me(rid):
            dominated |= engine.ext[b]
        und[rid] = ext & ~dominated
        new = decision(und, action)
        new_right = right_of(new, truth)
        lost, gained = right & ~new_right, new_right & ~right
        changed = new["two"] ^ dec["two"]
        for q in set(new["by_queue"]) | set(dec["by_queue"]):
            changed |= new["by_queue"].get(q, 0) ^ dec["by_queue"].get(q, 0)
        ok["inside"] &= changed & ~ext == 0
        only = new["one"] & ~new["two"]
        taken, conflict = lost & only, lost & new["two"]
        ok["undefeated"] &= lost & ~new["one"] == 0
        same_queue = 0
        for other, m in und.items():
            if other != rid and action[other] == d["action"]:
                same_queue |= m
        ok["alone"] &= taken & ~und[rid] == 0 and taken & same_queue == 0
        for m in (lost, gained, ext):
            for j in ends(m):
                ok["decide"] &= is_the_engines(engine, cases[n - 1 - j], new, j)
        steps.append({"idx": idx, "rule_id": rid, "action": d["action"],
                      "cause": (escs.get(idx) or {}).get("kind"),
                      "conditions": len(d["conditions"]),
                      "errors": bisect_right(errors, idx),
                      "right": new_right, "lost": lost, "gained": gained,
                      BY_CONTAINMENT: taken & ~edge_beaten, BY_EDGE: taken & edge_beaten,
                      CONFLICT: conflict})
        dec, right = new, new_right
    for j in range(0, n, STRIDE):
        ok["decide"] &= is_the_engines(engine, cases[n - 1 - j], dec, j)
    ok["masks"] = und == brows.undefeated_masks(engine)
    return {"engine": engine, "steps": steps, "final": dec, "ok": ok}


def right_at(steps: list[dict[str, Any]], case: int) -> int:
    """The points right after the last birth at or before `case`."""
    got = [s for s in steps if s["idx"] <= case]
    return got[-1]["right"].bit_count() if got else 0


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], space: Space, truth: dict[str, int], cases: Sequence,
             stage_c: dict[str, Any], final: PriorityEngine | None = None) -> dict[str, Any]:
    """One run's curve, its peak and its fall, every point lost read at its last
    loss and in the final base, and the gates. `stage_c` carries the run's final
    share and, for an L run, its curve at the checkpoints. `final` is the run's
    final base, `manual.instrument.final_engine`'s by default."""
    final = final if final is not None else MI.final_engine(record)
    rep = replay(record, space, truth, cases)
    steps = rep["steps"]
    n = space.n
    kw = keyword(space)
    counts = [s["right"].bit_count() for s in steps]
    p = counts.index(max(counts)) if steps else None
    r_peak = steps[p]["right"] if steps else 0
    r_final = steps[-1]["right"] if steps else 0
    lost_pts, gained_pts = r_peak & ~r_final, r_final & ~r_peak
    after = steps[p + 1:] if steps else []

    assigned = 0
    takers: list[dict[str, Any]] = []
    for s in reversed(after):
        last = s["lost"] & lost_pts & ~assigned
        if not last:
            continue
        assigned |= last
        takers.append({"born_at": s["idx"], "rule_id": s["rule_id"], "action": s["action"],
                       "cause": s["cause"], "conditions": s["conditions"],
                       "points": last.bit_count(),
                       "by_kind": {k: (last & s[k]).bit_count() for k in LOSSES},
                       "by_true_queue": counts_by_queue(last, truth),
                       "keyword": (last & kw).bit_count()})
    takers.reverse()

    def total(key) -> Counter:
        c: Counter = Counter()
        for t in takers:
            c[key(t)] += t["points"]
        return c

    by_kind = Counter()
    sec_by_queue, sec_by_cause = Counter(), Counter()
    for t in takers:
        by_kind.update(t["by_kind"])
        sec_by_queue[t["action"]] += t["by_true_queue"].get(SEC, 0)
        sec_by_cause[t["cause"]] += t["by_true_queue"].get(SEC, 0)
    fin = rep["final"]
    only_final = fin["one"] & ~fin["two"]
    top = sum(sorted((t["points"] for t in takers), reverse=True)[:Q5_TOP])
    summary = {
        "births": len(steps),
        "peak": None if p is None else {
            "birth": p + 1, "born_at": steps[p]["idx"], "rule_id": steps[p]["rule_id"],
            "errors": steps[p]["errors"], "right": counts[p], "share": frac(F(counts[p], n))},
        "final": {"right": r_final.bit_count(), "share": frac(F(r_final.bit_count(), n))},
        "fall_points": (counts[p] - r_final.bit_count()) if steps else None,
        "fall": frac(F(counts[p] - r_final.bit_count(), n)) if steps else None,
        "lost": {
            "points": lost_pts.bit_count(),
            "by_true_queue": counts_by_queue(lost_pts, truth),
            "keyword": (lost_pts & kw).bit_count(),
            "by_kind": {k: by_kind.get(k, 0) for k in LOSSES},
            "by_cause": dict(total(lambda t: t["cause"])),
            "by_newborn_queue": dict(total(lambda t: t["action"])),
            "security_by_newborn_queue": {q: k for q, k in sec_by_queue.items() if k},
            "security_by_cause": {c: k for c, k in sec_by_cause.items() if k},
            "takers": len(takers),
            "top": top,
            "in_the_final_base": {
                "decided_by": {q: k for q, k in (
                    (q, (lost_pts & m & only_final).bit_count())
                    for q, m in fin["by_queue"].items()) if k},
                "conflict": (lost_pts & fin["two"]).bit_count(),
                "impasse": (lost_pts & ~fin["one"]).bit_count()},
        },
        "gained": {"points": gained_pts.bit_count(),
                   "by_true_queue": counts_by_queue(gained_pts, truth)},
        "after_the_peak": {
            "births": len(after),
            "by_cause": dict(Counter(s["cause"] for s in after)),
            "lost": sum(s["lost"].bit_count() for s in after),
            "gained": sum(s["gained"].bit_count() for s in after),
            "lost_by_kind": {k: sum(s[k].bit_count() for s in after) for k in LOSSES}},
    }

    sc_curve = stage_c.get("curve") or []
    curve_ok = all(F(right_at(steps, c["case"]), n) == F(c["loop"]["fraction"])
                   for c in sc_curve)
    final_ok = F(r_final.bit_count(), n) == F(stage_c["space"]["fraction"])
    moved = all(steps[i]["right"].bit_count() == steps[i - 1]["right"].bit_count()
                + steps[i]["gained"].bit_count() - steps[i]["lost"].bit_count()
                for i in range(p + 1, len(steps))) if steps else True
    partition = (assigned == lost_pts
                 and sum(t["points"] for t in takers) == lost_pts.bit_count()
                 and sum(by_kind.values()) == lost_pts.bit_count()
                 and all(sum(t["by_kind"].values()) == t["points"] for t in takers))
    gates = [
        {"gate": 1, "what": "the replay is the base",
         "passes": ch_lost.same_base(final, rep["engine"])},
        {"gate": 2, "what": "the curve is Stage C's at its checkpoints, and so is the final "
                            "share",
         "passes": curve_ok and final_ok},
        {"gate": 3, "what": "every reading is the engine's",
         "passes": all(rep["ok"].values())},
        {"gate": 4, "what": "the last losses partition the points lost",
         "passes": partition and moved},
    ]
    curve = [{"born_at": s["idx"], "rule_id": s["rule_id"], "cause": s["cause"],
              "errors": s["errors"], "right": c} for s, c in zip(steps, counts)]
    return {"summary": summary, "takers": takers, "curve": curve, "checks": rep["ok"],
            "gates": gates}


def read_all_runs(records: dict[str, dict], score: dict[str, Any], space: Space,
                  truth: dict[str, int], cases: Sequence,
                  finals: dict[str, PriorityEngine] | None = None) -> dict[str, dict]:
    """Every run read, each against Stage C's figures for it."""
    finals = finals or {}
    out = {}
    for tag, rec in records.items():
        stage_c = {"space": score["CR-g"]["runs"][tag]["space"],
                   "curve": score["CR-g"]["curves"].get(tag) or []}
        out[tag] = read_run(rec, space, truth, cases, stage_c, final=finals.get(tag))
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    def arm(a: str) -> dict[int, dict[str, Any]]:
        return {k: runs[plan.tag(a, k)]["summary"] for k in range(1, plan.REPS + 1)
                if plan.tag(a, k) in runs}

    L, N = arm(plan.LABELLED), arm(UNLABELLED)

    def per_run(part) -> dict[str, Any]:
        out = {}
        for k, s in L.items():
            num, den = part(s)
            out[plan.tag(plan.LABELLED, k)] = {"part": num, "of": den,
                                               "share": frac(share(num, den))}
        return out

    def each(part, line: Fraction) -> bool:
        return bool(L) and all(den and F(num, den) >= line
                               for num, den in (part(s) for s in L.values()))

    def pooled(part) -> tuple[int, int]:
        got = [part(s) for s in L.values()]
        return sum(g[0] for g in got), sum(g[1] for g in got)

    def keyword_queue(s):
        return s["lost"]["by_true_queue"].get(SEC, 0), s["lost"]["points"]

    def alone(s):
        k = s["lost"]["by_kind"]
        return k[BY_CONTAINMENT] + k[BY_EDGE], s["lost"]["points"]

    def by_error(s):
        return s["lost"]["by_cause"].get(plan.ERROR, 0), s["lost"]["points"]

    def births_error(s):
        a = s["after_the_peak"]
        return a["by_cause"].get(plan.ERROR, 0), a["births"]

    def by_t2(s):
        return (s["lost"]["security_by_newborn_queue"].get(T2, 0),
                s["lost"]["by_true_queue"].get(SEC, 0))

    def at_a_few(s):
        return s["lost"]["top"], s["lost"]["points"]

    q2, q3, q3b, q4 = pooled(alone), pooled(by_error), pooled(births_error), pooled(by_t2)
    q3_share, q3b_share = share(*q3), share(*q3b)
    pairs = {k: {"n": N[k], "l": L[k]} for k in sorted(set(L) & set(N))}
    return [
        {"clause": "Q1", "what": "in each L run, at least half of the points lost are "
                                 "SECURITY_INCIDENT's",
         "reading": per_run(keyword_queue), "holds": each(keyword_queue, Q1_SHARE)},
        {"clause": "Q2", "what": "at least half of the points lost were lost at their last "
                                 "loss to a newborn deciding them alone",
         "reading": {"alone": q2[0], "of": q2[1], "share": frac(share(*q2))},
         "holds": q2[1] > 0 and F(*q2) >= Q2_SHARE},
        {"clause": "Q3", "what": "the share of the points lost whose last loss was to a rule "
                                 "born at a reported error is at least the share of births at "
                                 "a reported error after the peaks",
         "reading": {"lost_to_a_reported_error": q3[0], "of_lost": q3[1],
                     "lost_share": frac(q3_share),
                     "births_at_a_reported_error": q3b[0], "of_births": q3b[1],
                     "births_share": frac(q3b_share)},
         "holds": q3_share is not None and q3b_share is not None and q3_share >= q3b_share},
        {"clause": "Q4", "what": "at least half of the SECURITY_INCIDENT points lost were "
                                 "lost to rules of T2_TECHNICAL",
         "reading": {"to_T2_TECHNICAL": q4[0], "of": q4[1], "share": frac(share(*q4))},
         "holds": q4[1] > 0 and F(*q4) >= Q4_SHARE},
        {"clause": "Q5", "what": "in each L run, the ten births that took the most of its "
                                 "points lost took at least half of them",
         "reading": per_run(at_a_few), "holds": each(at_a_few, Q5_SHARE)},
        {"clause": "Q6", "what": "in each pair of runs under the same draws, N's fall is "
                                 "smaller than L's",
         "reading": {f"r{k}": {"n_fall": v["n"]["fall"], "l_fall": v["l"]["fall"]}
                     for k, v in pairs.items()},
         "holds": len(pairs) == plan.REPS and all(
             v["n"]["fall_points"] is not None and v["l"]["fall_points"] is not None
             and v["n"]["fall_points"] < v["l"]["fall_points"] for v in pairs.values())},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return records, json.loads(plan.score_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the loop's share of the space peaked and "
                                             "fell (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/fall.py writes {record_path()}")
    records, score = read_all()
    space = MI.space()
    runs = read_all_runs(records, score, space, MI.space_truth(), list(all_cases()))
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
        "surface": "the whole space, 134,400 points, read after every birth of each run",
        "constants": {"STRIDE": STRIDE, "Q1_SHARE": str(Q1_SHARE), "Q2_SHARE": str(Q2_SHARE),
                      "Q4_SHARE": str(Q4_SHARE), "Q5_TOP": Q5_TOP,
                      "Q5_SHARE": str(Q5_SHARE)},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: peak {s['peak']['share']['value']:.4f} at birth {s['peak']['birth']} "
              f"of {s['births']}, final {s['final']['share']['value']:.4f}, "
              f"lost {s['lost']['points']}, gained {s['gained']['points']}, "
              f"by kind {s['lost']['by_kind']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
