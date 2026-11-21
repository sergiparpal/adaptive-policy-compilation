"""
WHY L r2 LOST UNDER THE COPIES' LOSSES FIRST. `FINDINGS_RANKED.md`, *One thing
the copies' refused sides left free*, O, replayed each run with the copies'
losses tried before their wins. In L r2 that replay's base decided 411 points
fewer than the record's: it gained 4,005 and lost 4,416. Its *What it does not
settle*, second item, asks what the lost points were lost through: the copies'
wins the replay refused, their losses, or edges at other births; and whether
those were right. `IDEAS.md` carries the item under *What `PLAN_RANKED.md`
opens*. Asked for by Sergi on 2026-11-21. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`, and **`losses.json`**,
whose replays this reading rebuilds: the record's order, and the copies' losses
first, with `ranked/losses.py`'s own `replay`.

**A changed edge** is an entry of the run's log the two replays gave different
verdicts. It is **missing** when the record installed it and the replay refused
it for closing a cycle, and **added** when the reverse. Its **kind**:
- **a copy's win**, tried at a copy's birth with the copy above the other rule;
- **a copy's loss**, the same with the copy below;
- **another birth's edge**, tried at a birth that is not a copy's.

**A lost point** is a point of the space the record's base decides right and
the replay's decides otherwise; **a gained point**, the reverse. Both are read
on the run's own engine, as `losses.json` reads them.
- **A missing edge `z` above `y` frees `y` at a point** where `z` matches the
  point, and `y` stands undefeated in the replay's base and not in the
  record's. It frees **a wrong rule** there when `y`'s queue is not the point's
  true queue.
- **An added edge `z` above `y` defeats `y` at a point** where `z` matches it,
  and `y` stands in the record's base and not in the replay's.

**The policy's verdict** on a changed edge is read over the points its two rules
share: `right`, `wrong` or `even`, as `corrections/paths.py`'s `verdict` reads
one.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **What the lost points are lost through.** In each run, the lost points
      by the kind of the missing edges that free a wrong rule there: any of
      each kind, and that kind alone. Each also by the point's true queue. And
      the lost points no changed edge reaches.
  (b) **The missing edges.** By kind: how many free a wrong rule at a lost
      point, with the policy's verdict on each. The ten that carry the most
      lost points, with their rules' queues, the birth that tried them and its
      newborn.
  (c) **What the gained points are gained through.** The same for the gained
      points and the added edges that defeat a wrong rule there.
  (d) **Why the replay refused the copies' wins.** For each copy's win that
      frees a wrong rule at a lost point, what closed its cycle in the replay,
      read at the moment it was tried as `ranked/refusals.py` reads a refusal.
      `own answer`: the copy's own losses, installed before it. `containment`:
      a rule nested in the copy. `either`: both kinds of path remain.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The record's order is the run.** As `ranked/losses.py`'s gate 1: every
     edge gets the log's verdict, and the base is Stage C's.
  2. **The replays are `losses.json`'s.** Both bases decide what that record
     keeps. The changed edges at the copies' births, by side, are as many as
     it counts.
  3. **Every changed point is reached.** In L, every lost point is reached by
     a missing edge that frees a wrong rule there, and every gained point by an
     added edge that defeats one. In K, every lost or gained point is reached
     by a changed edge whose rules match it.
  4. **The changed edges are the graphs' difference.** The missing edges are
     exactly the declared edges of the record's base that the replay's lacks,
     and the added edges the reverse.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  P1. **Through the copies' wins.** In L r2, at more than half of the lost
      points a copy's win the replay refused is among the missing edges that
      free a wrong rule there.
  P2. **Right wins.** In L r2, of the copies' wins the replay refused that free
      a wrong rule at a lost point, more than half are right by the policy.
  P3. **Through their own losses.** In L r2, more than half of those wins
      closed their cycle in the replay through the copy's own losses, installed
      before them: `own answer` or `either`.
  P4. **L r2 alone.** The lost points reached through the copies' refused wins
      are more in L r2 than in L r1 and L r3 together.

A clause that reads a missing value fails.

**The drafter's account.**
- **What the engine settles.** In L a point is decided where one queue stands
  undefeated. A lost point stood right in the record, with no rule of another
  queue undefeated. In the replay a rule of another queue stands there, so
  something that defeated it in the record is gone. Containment is the same in
  both, so that something is a declared edge the replay lacks. Gate 3 holds the
  reading to it, and no clause reads it.
- **P1, the bet.** O counted L r2's changed edges at the copies' births: 146 of
  their wins and 21 of their losses missing, and outside them 35 edges. A
  billing copy's win over a deflection rule, refused, frees the deflection rule
  on billing's tickets, and O found L r2's lost points mostly
  `BILLING_SPECIALIST`'s.
- **P2, trusted least.** At a lost point the copy stood right, so its win was
  right there. But a broad copy's region holds both of billing's layers, and
  over the points it shares with a deflection rule the policy may side with
  deflection.
- **P3, trusted most.** The record installed those wins: tried after the losses
  in the record's order, nothing closed them. In the replay the copy's losses
  went first, and a path into the copy through one of them closes the win. The
  base the copy meets differs a little in the replay, so `containment` can
  appear.
- **P4.** O found L r2 losing 4,416 points, L r1 545 and L r3 1,790. It also
  counted the copies' wins each refused: 146, 57 and 67.

**The bet is P1.** **P3 is trusted most.** **P2 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole;
- `losses.json` whole: every replay's base, its changed edges by kind and side,
  the points gained and lost by true queue, and the copy that costs most;
- `sides.json` and `copies.json` whole;
- `rung2/engine2.py`'s containment and `try_edge`, and `ranked/refusals.py`,
  whose reading of an edge's cycle this one reuses.

**What the drafter had not seen**: which changed edges reach any lost or gained
point, their verdicts, or what closed any of them in the replay.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-21, after `ranked/losses.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m ranked.lost --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.lost
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from blind import rows as brows
from corrections import paths as CP
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import copies as CO
from . import losses as LO
from . import plan
from . import readings as RD
from . import refusals as RF

RUNS, L_RUNS = RD.RUNS, RD.L_RUNS
WIN, LOSS = LO.WIN, LO.LOSS
CW, CL, OE = "a copy's win", "a copy's loss", "another birth's edge"
KINDS = (CW, CL, OE)
MISSING, ADDED = "missing", "added"
OWN, CONTAINMENT, EITHER = RF.OWN, RF.CONTAINMENT, RF.EITHER
CLOSES = RF.CLOSES
VERDICTS = RF.VERDICTS
TOP = 10
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-21, after ranked/losses.py. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")

plain = RD.plain


# ---------------------------------------------------------------------------
# The changed edges
# ---------------------------------------------------------------------------

def changed_edges(record: dict[str, Any], copies: set[str], rec: dict[str, Any],
                  got: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Every log entry the two replays gave different verdicts, with its birth,
    its newborn's side and its kind, missing or added."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    out = {}
    for idx in sorted(by_birth):
        rid = born[idx]["rule_id"]
        for e in by_birth[idx]:
            a, b = rec["verdict"][e.key], got["verdict"][e.key]
            if a == b:
                continue
            side = LOSS if e.loser == rid else WIN if e.winner == rid else None
            kind = (CW if side == WIN else CL) if rid in copies else OE
            out[e.key] = {"key": e.key, "winner": e.winner, "loser": e.loser, "birth": idx,
                          "newborn": rid, "side": side, "kind": kind,
                          "change": MISSING if (a, b) == (EDGE_OK, EDGE_CYCLE)
                          else ADDED if (a, b) == (EDGE_CYCLE, EDGE_OK) else None}
    return out


def declared(engine: PriorityEngine) -> set[tuple[str, str]]:
    return {(w, l) for w, ls in engine.decl_above.items() for l in ls}


def the_graphs_difference(changed: dict[int, dict], rec_eng: PriorityEngine,
                          got_eng: PriorityEngine) -> bool:
    """Gate 4: the missing edges are what the record's declared graph has and the
    replay's lacks, and the added edges the reverse."""
    a, b = declared(rec_eng), declared(got_eng)
    missing = {(c["winner"], c["loser"]) for c in changed.values() if c["change"] == MISSING}
    added = {(c["winner"], c["loser"]) for c in changed.values() if c["change"] == ADDED}
    return bool(all(c["change"] is not None for c in changed.values())
                and missing == a - b and added == b - a)


# ---------------------------------------------------------------------------
# Where a changed edge reaches
# ---------------------------------------------------------------------------

def freeing(points: int, before: dict[str, int], after: dict[str, int], ext: dict[str, int],
            action: dict[str, str], truth: dict[str, int], edges: Sequence[dict],
            wrong: bool = True) -> dict[int, int]:
    """For each edge `z` above `y`, the points of `points` where `z` matches and
    `y` stands in `after` and not in `before`: where taking the edge away frees
    `y`, or adding it defeats `y`, read with `before` and `after` swapped. With
    `wrong`, only where `y`'s queue is not the point's true queue."""
    out = {}
    for c in edges:
        z, y = c["winner"], c["loser"]
        m = points & after.get(y, 0) & ~before.get(y, 0) & ext[z]
        if wrong:
            m &= ~truth.get(action[y], 0)
        if m:
            out[c["key"]] = m
    return out


def by_kind(points: int, reach: dict[int, int], changed: dict[int, dict],
            truth: dict[str, int]) -> dict[str, Any]:
    """(a) and (c): the points by the kinds of the edges that reach them, any of
    each kind and that kind alone, each by true queue; and the points no edge
    reaches."""
    masks = {k: 0 for k in KINDS}
    for key, m in reach.items():
        masks[changed[key]["kind"]] |= m
    reached = 0
    for m in masks.values():
        reached |= m

    def alone(k):
        others = 0
        for j in KINDS:
            if j != k:
                others |= masks[j]
        return masks[k] & ~others

    return {"points": points.bit_count(),
            "any": {k: masks[k].bit_count() for k in KINDS},
            "alone": {k: alone(k).bit_count() for k in KINDS},
            "any_by_queue": {k: LO.by_queue(masks[k], truth) for k in KINDS},
            "unreached": (points & ~reached).bit_count()}


def edges_read(reach: dict[int, int], changed: dict[int, dict], engine: PriorityEngine,
               action: dict[str, str], truth: dict[str, int]) -> dict[str, Any]:
    """(b): the edges that reach a point, by kind and verdict, and the ten that
    reach the most."""
    rows = []
    for key, m in reach.items():
        c = changed[key]
        rows.append(dict(c, points=m.bit_count(),
                         queues=[action[c["winner"]], action[c["loser"]]],
                         newborn_queue=action[c["newborn"]],
                         verdict=CP.verdict(engine, c["winner"], c["loser"], action, truth)))
    tally = {k: {"edges": 0, **{v: 0 for v in VERDICTS}} for k in KINDS}
    for r in rows:
        tally[r["kind"]]["edges"] += 1
        tally[r["kind"]][r["verdict"]] += 1
    top = sorted(rows, key=lambda r: (-r["points"], r["key"]))[:TOP]
    return {"by_kind": tally, "top": top}


# ---------------------------------------------------------------------------
# (d): what closed a copy's win in the replay
# ---------------------------------------------------------------------------

def closing(record: dict[str, Any], space: Space, first: set[str],
            targets: set[int]) -> dict[int, str | None]:
    """The replay again, with the copies' losses first; each target edge read
    right before it is tried: what closes its cycle at its newborn, with the
    newborn's edges installed earlier at its birth as its own answer."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    eng = PriorityEngine(space=space)
    out: dict[int, str | None] = {}
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        eng.add(rule_from(d), born_at=idx, keep_id=True)
        own: set[tuple[str, str]] = set()
        for e in LO.ordered(by_birth.get(idx, []), rid, first):
            if e.key in targets:
                nodes = CP.forward(eng, e.loser) & CP.backward(eng, e.winner)
                out[e.key] = (RF.closes(eng, e.winner, e.loser, rid, own, nodes)
                              if e.winner in nodes else None)
            before = e.loser in eng.decl_above.get(e.winner, set())
            why = eng.try_edge(e.winner, e.loser)
            if why == EDGE_OK and not before and e.loser in eng.decl_above[e.winner]:
                own.add((e.winner, e.loser))
    return out


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def reached_all(points: int, before: dict[str, int], after: dict[str, int],
                ext: dict[str, int], missing: Sequence[dict], added: Sequence[dict]) -> bool:
    """Gate 3 in K: every point is reached by a changed edge whose rules match
    it, freeing or defeating a rule there, of any queue."""
    reach = 0
    for c in missing:
        reach |= after.get(c["loser"], 0) & ~before.get(c["loser"], 0) & ext[c["winner"]]
    for c in added:
        reach |= before.get(c["loser"], 0) & ~after.get(c["loser"], 0) & ext[c["winner"]]
    return bool(points & ~reach == 0)


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int],
             copies: Sequence[dict]) -> tuple[dict[str, Any], dict[str, Any]]:
    ids = {c["rule_id"] for c in copies}
    rec = LO.replay(record, space, truth, None)
    got = LO.replay(record, space, truth, ids)
    changed = changed_edges(record, ids, rec, got)
    missing = [c for c in changed.values() if c["change"] == MISSING]
    added = [c for c in changed.values() if c["change"] == ADDED]
    ru, gu = brows.undefeated_masks(rec["engine"]), brows.undefeated_masks(got["engine"])
    ext = got["engine"].ext
    action = {d["rule_id"]: d["action"] for d in record["rules"]}
    lost = rec["right"] & ~got["right"]
    gained = got["right"] & ~rec["right"]
    lost_reach = freeing(lost, ru, gu, ext, action, truth, missing)
    gained_reach = freeing(gained, gu, ru, ext, action, truth, added)
    targets = {k for k in lost_reach if changed[k]["kind"] == CW}
    closes = closing(record, space, ids, targets)
    lost_by_kind = by_kind(lost, lost_reach, changed, truth)
    gained_by_kind = by_kind(gained, gained_reach, changed, truth)
    if record.get("arm") == plan.RANKED:
        reached = (reached_all(lost, ru, gu, ext, missing, added)
                   and reached_all(gained, ru, gu, ext, missing, added))
    else:
        reached = lost_by_kind["unreached"] == 0 and gained_by_kind["unreached"] == 0
    reading = {
        "changed": {ch: {k: sum(1 for c in changed.values() if c["change"] == ch
                                and c["kind"] == k) for k in KINDS}
                    for ch in (MISSING, ADDED)},
        "lost": dict(lost_by_kind, **edges_read(lost_reach, changed, got["engine"], action,
                                                truth),
                     closes={v: sum(1 for k in targets if closes.get(k) == v) for v in CLOSES}),
        "gained": dict(gained_by_kind, **edges_read(gained_reach, changed, got["engine"], action,
                                                    truth)),
    }
    return reading, {"rec": rec, "got": got, "changed": changed, "reached": reached}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def get(x: Any, *path) -> Any:
    for p in path:
        x = x.get(p) if isinstance(x, dict) else None
    return x


def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    r2 = runs.get("l_r2")
    lost, through = get(r2, "lost", "points"), get(r2, "lost", "any", CW)
    edges, right = get(r2, "lost", "by_kind", CW, "edges"), get(r2, "lost", "by_kind", CW, "right")
    closes = get(r2, "lost", "closes")
    l1, l3 = get(runs.get("l_r1"), "lost", "any", CW), get(runs.get("l_r3"), "lost", "any", CW)

    def ints(*xs):
        return all(isinstance(x, int) for x in xs)

    p1 = ints(lost, through) and lost > 0 and 2 * through > lost
    p2 = ints(edges, right) and edges > 0 and 2 * right > edges
    p3 = (isinstance(closes, dict) and ints(*(closes.get(v) for v in CLOSES))
          and sum(closes.values()) > 0
          and 2 * (closes[OWN] + closes[EITHER]) > sum(closes.values()))
    p4 = ints(through, l1, l3) and through > l1 + l3

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("P1", "in L r2, at more than half of the lost points a copy's win the replay refused "
                  "is among the missing edges that free a wrong rule there", p1,
            {"lost": lost, "through_a_copys_win": through}),
        out("P2", "in L r2, of the copies' wins the replay refused that free a wrong rule at a "
                  "lost point, more than half are right by the policy", p2,
            {"edges": edges, "right": right}),
        out("P3", "in L r2, more than half of those wins closed their cycle in the replay "
                  "through the copy's own losses", p3, closes),
        out("P4", "the lost points reached through the copies' refused wins are more in L r2 "
                  "than in L r1 and L r3 together", p4,
            {"l_r2": through, "l_r1": l1, "l_r3": l3}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "lost.json"


def losses_path():
    return plan.OUT / "losses.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any]]:
    records = {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    return records, json.loads(losses_path().read_text()), json.loads(plan.score_path().read_text())


def as_kept(reading_changed: dict[str, dict[str, int]], kept_first: dict[str, Any]) -> bool:
    """Gate 2's count: the copies' edges the replay changed, by side, as many as
    `losses.json` counts."""
    c = kept_first["copies"]
    return bool(reading_changed[MISSING][CW] == c[WIN]["refused_now"]
                and reading_changed[ADDED][CW] == c[WIN]["installed_now"]
                and reading_changed[MISSING][CL] == c[LOSS]["refused_now"]
                and reading_changed[ADDED][CL] == c[LOSS]["installed_now"])


def read_everything(records: dict[str, dict], kept: dict[str, Any], score: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    keyword = space.mask["has_security_keyword"][True]
    stage_c = score["RK-g"]["runs"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in RUNS:
        if t not in records:
            continue
        copies, _ = CO.copies_of_run(records[t], space)
        runs[t], got = read_run(records[t], space, truth, copies)
        base = RD.base_of(records[t], space, truth)
        gates.append({"gate": 1, "run": t, "what": "the record's order is the run",
                      "passes": bool(LO.is_the_record(records[t], got["rec"], base)
                                     and RD.gate_one(base, stage_c[t], keyword, space.n))})
        k = kept["readings"]["runs"][t]
        gates.append({"gate": 2, "run": t, "what": "the replays are losses.json's",
                      "passes": bool(got["rec"]["right"].bit_count() == k[LO.RECORD]["right"]
                                     and got["got"]["right"].bit_count()
                                     == k[LO.COPIES_FIRST]["right"]
                                     and as_kept(runs[t]["changed"], k[LO.COPIES_FIRST]))})
        gates.append({"gate": 3, "run": t, "what": "every changed point is reached",
                      "passes": got["reached"]})
        gates.append({"gate": 4, "run": t, "what": "the changed edges are the graphs' difference",
                      "passes": the_graphs_difference(got["changed"], got["rec"]["engine"],
                                                      got["got"]["engine"])})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why L r2 lost under the copies' losses first "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/lost.py writes {record_path()}")
    records, kept, score = read_inputs()
    readings, gates = read_everything(records, kept, score)
    for g in sorted(gates, key=lambda g: (RUNS.index(g["run"]), g["gate"])):
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(RUNS)
    if not complete:
        print("  missing records")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0 if complete and all(g["passes"] for g in gates) else 1
    if not complete or not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(readings)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"losses": str(losses_path()), "losses_from": kept["_env"].get("git_commit"),
                   "score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "the whole space of 134,400 points, on each run's own engine: the points the "
                   "replay with the copies' losses first decides otherwise than the record's "
                   "base, each read through the edges whose verdict the replay changed",
        "constants": {"top": TOP},
        "gates": gates,
        "readings": readings,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for cl_ in expectation:
        print(f"  {cl_['clause']}: {'holds' if cl_['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
