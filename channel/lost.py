"""
WHY c r1 LOST `SECURITY_INCIDENT`.
Stage C found it: run c r1's final base recalls 0.3238 of the queue's points
over the space, where every other run of either arm recalls 0.97 or more. The
channel had reported 11 of c r1's 17 wrong decisions on the queue's tickets, each
of those escalated, and the proposer drafted the queue at 12 of its 13
escalations whose ticket was the queue's. Under c r1's draws the transcriber
compiles the whole queue. `FINDINGS_CHANNEL.md`, *What Stage C does not settle*,
item 1, and `IDEAS.md` carry the question: which of its rules decide those
points, and when they came to. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
A point whose true queue is the queue, and which the final base does not decide
right, was lost in one of five ways, and every lost point is in exactly one:
  impasse      no rule of the base matches it;
  conflict     undefeated rules of different queues match it. *Contested* when
               a rule of the queue is among them;
  unwritten    one other queue decides it, and no rule of the queue matches it;
  outranked    one other queue decides it, though a rule of the queue matches
               it. Split by how the queue's rules lose there:
               - by an edge: a rule of another queue that matches the point beats
                 one of the queue's rules by a declared edge;
               - by containment: no such edge, so every matching rule of the
                 queue is beaten by rules nested inside it.

**When they came to.** The base is replayed in birth order, each rule added at
its case and its edges tried after it in `edge_log` order, as
`reasoned_loop/governed.py` does. After every birth the queue's points decided
right are counted. The curve gives the most the run ever decided right, and
every birth that moved it.

**The queue's escalations**, those whose ticket's true queue is the queue:
- each one's cause and its draft's queue;
- the draft's points of the queue over the space;
- its verdict: born, unplaced, refused or changed.

**Every run is read**, the six of them, so that c r1 is set beside the five that
compiled the queue. The expectation reads c r1 and the other five's rules.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its rules, their extensions and its declared
     edges are `manual.instrument.final_engine`'s rebuild. The queue's points
     decided right are Stage C's.
  2. **The ways partition the loss.** Right, impasse, conflict, unwritten and
     outranked are disjoint and cover the queue's points. By an edge and by
     containment cover outranked.
  3. **The curve ends at the base.** The last birth's count is the final base's.
  4. **The escalations are the record's.** Every one of the queue's escalations
     is a row that escalated on a ticket of the queue. Every born verdict names a
     rule of the base.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads c r1, the queue `SECURITY_INCIDENT`, over the space. *Lost*
means the queue's points c r1's final base does not decide right.

  L1. **Unwritten, not outranked.** At least half of the lost points are
      unwritten: one other queue decides them, and no rule of the queue matches.
  L2. **To one queue.** At least half of the lost points go to `T2_TECHNICAL`.
  L3. **The queue's rules are narrow.** No rule of the queue in the final base
      covers half of the queue's points or more.
  L4. **The drafts were born.** At least 10 of the queue's escalations ended
      with their rule born.
  L5. **Never compiled.** After no birth did the base decide half of the queue's
      points right or more.
  L6. **The other runs wrote it broad.** In each of the other five runs, some
      rule of the queue in the final base covers half of the queue's points or
      more.

**The drafter's account.** c r1 never wrote the queue whole. Its proposer drafted
the queue at the tickets, but drafted each rule narrow. The points no rule of the
queue reaches go to a broad rule of `T2_TECHNICAL`, written for the keyword's
default, `H03`'s queue, which decides them by default.
- **The drafter derived the default's part from Stage C.** c r1 decides every
  point of `T2_TECHNICAL` right, so it decides all of `H03`'s 16,800 keyword
  points right, and its keyword half's 0.4929 is those points and the queue's
  16,320.
- **The bet is L1.** Under an edge the proposer pointed wrong, the lost points
  would be outranked instead, and L1 would fail while L2 held.
- **L4 is trusted least.** The placement round lists every rule of another
  queue a keyword draft meets, and in c r1 16 escalations ended unplaced. A
  draft left unplaced is not born, and its region stays unwritten whatever its
  breadth.
- **L6 is trusted second least.** A run may tile the queue with narrow rules
  rather than write it broad.

**What the drafter had seen**:
- `FINDINGS_CHANNEL.md` whole, and `score.json`'s `CH-g` for every run: both
  surfaces, the recall of every queue, the channel's reports by queue, rule and
  time, the error escalations by governing rule, the rare queues, the
  placements and the births;
- the field names of an escalation, read in c r2's record;
- e r3's first draft whole, from its partial file during the run;
- `reasoned_loop/governed.py`, `edges/rebuild.py`, `manual/instrument.py`,
  `blind/rows.py` and `rung2/engine2.py`'s arbitration.

**What the drafter had not seen**: any rule, edge or escalation of c r1 or of any
other run of this plan, any point's winner, or the curve.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: WHAT THE UNPLACED ANSWERS LEFT OUT
--------------------------------------------------------------------------
The first run found c r1's escalations on the queue's tickets mostly unplaced:
the placement round's answer left a listed rule without a side, and the draft
was not born. So, for each of the queue's unplaced escalations in every run,
this part reads:
- the rules the round listed, and the ones the answer left out;
- each one's relation to the draft, by `reasoned_loop/unplaced.py`'s
  `relation`: inside the draft, containing it, equal to it, or crossing it.
  A rule nested with the draft is one the system prompt says needs no
  declaration;
- how many of the queue's unplaced escalations left each rule out;
- every rule of another queue whose region holds every point of the queue.
  Such a rule contains every draft of the queue, so every placement round of
  the queue lists it once it is born.

It was written after the six clauses above had been read. It carries no
expectation and moves no clause.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-07, after Stage C. The expectation
above was written and committed before the reading ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m channel.lost --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m channel.lost
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any

from harness.dsl import Condition, RuleValidationError
from harness.provenance import describe, environment

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reasoned_loop import unplaced as un
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import plan

F = Fraction
QUEUE = "SECURITY_INCIDENT"
RUN = ("c", 1)                     # the run the expectation reads
WAYS = ("impasse", "conflict", "unwritten", "outranked")

# The expectation's lines.
L_HALF = F(1, 2)
L4_BORN = 10

# The verdicts an escalation ends with, as the loop records them.
BORN, UNPLACED, REFUSED, CHANGED = "nacida", "sin_situar", "rechazada", "cambiada"
VERDICTS = (BORN, UNPLACED, REFUSED, CHANGED)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-07, after Stage C. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a "
    "signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its six clauses were read: what the queue's "
    "unplaced answers left out, by relation to the draft. No expectation; no clause "
    "moves.")


def record_path():
    return plan.OUT / "lost.json"


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


# ---------------------------------------------------------------------------
# The ways a point is lost
# ---------------------------------------------------------------------------

def by_action(engine: PriorityEngine) -> tuple[dict[str, int], dict[str, int], int]:
    """Where each rule is undefeated, where each queue's rules are, and where any
    rule matches."""
    und = brows.undefeated_masks(engine)
    out: dict[str, int] = {}
    covered = 0
    for r in engine.rules:
        out[r.action] = out.get(r.action, 0) | und[r.rule_id]
        covered |= engine.ext[r.rule_id]
    return und, out, covered


def decided_alone(undefeated: dict[str, int]) -> dict[str, int]:
    """Where each queue is the only one undefeated: the points it decides."""
    out = {}
    for a, m in undefeated.items():
        others = 0
        for b, n in undefeated.items():
            if b != a:
                others |= n
        out[a] = m & ~others
    return out


def edge_beaten(engine: PriorityEngine, queue: str) -> int:
    """The points where a rule of another queue beats one of the queue's rules by
    a declared edge, both matching."""
    action = {r.rule_id: r.action for r in engine.rules}
    out = 0
    for r in engine.rules:
        if r.action != queue:
            continue
        for x in engine.decl_below.get(r.rule_id, ()):
            if action.get(x) != queue:
                out |= engine.ext[r.rule_id] & engine.ext[x]
    return out


def ways(engine: PriorityEngine, truth: int, queue: str = QUEUE) -> dict[str, Any]:
    """The queue's points, as masks: right, and lost in each way."""
    by_rule, und, covered = by_action(engine)
    alone = decided_alone(und)
    right = truth & alone.get(queue, 0)
    lost = truth & ~right
    decided = 0
    for m in alone.values():
        decided |= m
    impasse = lost & ~covered
    conflict = lost & covered & ~decided
    wrong = {b: lost & m for b, m in alone.items() if b != queue and lost & m}
    wrong_all = 0
    for m in wrong.values():
        wrong_all |= m
    written = 0
    for r in engine.rules:
        if r.action == queue:
            written |= engine.ext[r.rule_id]
    edged = edge_beaten(engine, queue)
    outranked = wrong_all & written
    return {"right": right, "lost": lost, "impasse": impasse, "conflict": conflict,
            "contested": conflict & und.get(queue, 0),
            "unwritten": wrong_all & ~written, "outranked": outranked,
            "by_edge": outranked & edged, "by_containment": outranked & ~edged,
            "wrong": wrong, "undefeated": by_rule}


def partitions(w: dict[str, Any], truth: int) -> bool:
    """Gate 2: the ways are disjoint and cover the queue's points."""
    parts = [w["right"], w["impasse"], w["conflict"], w["unwritten"], w["outranked"]]
    union, total = 0, 0
    for p in parts:
        union |= p
        total += p.bit_count()
    return (union == truth and total == truth.bit_count()
            and w["by_edge"] | w["by_containment"] == w["outranked"]
            and not w["by_edge"] & w["by_containment"])


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------

def birth_row(record: dict, idx: int) -> dict[str, Any]:
    row = next((r for r in record["records"] if r["idx"] == idx), {})
    return {"cause": row.get("cause"), "truth": row.get("truth"),
            "governing": row.get("truth_rule")}


def winners(engine: PriorityEngine, record: dict, w: dict[str, Any]) -> list[dict[str, Any]]:
    """Every rule of another queue undefeated on lost points the other queue
    decides, with the points and its birth. A point several such rules share is
    counted for each."""
    wrong_all = 0
    for m in w["wrong"].values():
        wrong_all |= m
    rules = {r["rule_id"]: r for r in record["rules"]}
    out = []
    for r in engine.rules:
        pts = w["undefeated"][r.rule_id] & wrong_all
        if not pts:
            continue
        out.append({"rule_id": r.rule_id, "action": r.action, "born_at": r.born_at,
                    "conditions": rules[r.rule_id]["conditions"],
                    "points": engine.ext[r.rule_id].bit_count(),
                    "lost_points": pts.bit_count(),
                    "unwritten": (pts & w["unwritten"]).bit_count(),
                    "outranked": (pts & w["outranked"]).bit_count(),
                    **birth_row(record, r.born_at)})
    return sorted(out, key=lambda x: (-x["lost_points"], x["born_at"]))


def queue_rules(engine: PriorityEngine, record: dict, w: dict[str, Any], truth: int,
                regions: dict[str, int], queue: str = QUEUE) -> list[dict[str, Any]]:
    """Every rule of the queue in the base: its points of the queue, where it is
    undefeated on them, which listed rule's region it is, if any, and its birth."""
    by_region = {m: k for k, m in sorted(regions.items(), reverse=True)}
    rules = {r["rule_id"]: r for r in record["rules"]}
    out = []
    for r in engine.rules:
        if r.action != queue:
            continue
        e = engine.ext[r.rule_id]
        out.append({"rule_id": r.rule_id, "born_at": r.born_at,
                    "conditions": rules[r.rule_id]["conditions"],
                    "points": e.bit_count(), "queue_points": (e & truth).bit_count(),
                    "undefeated_on_queue": (w["undefeated"][r.rule_id] & truth).bit_count(),
                    "lost_inside": (e & w["lost"]).bit_count(),
                    "is_listed_region": by_region.get(e),
                    **birth_row(record, r.born_at)})
    return sorted(out, key=lambda x: x["born_at"])


# ---------------------------------------------------------------------------
# When: the replay
# ---------------------------------------------------------------------------

def replay(record: dict, space: Space, truth: int,
           queue: str = QUEUE) -> dict[str, Any]:
    """The base in birth order, and after every birth the queue's points decided
    right."""
    born = erb.births(record)
    by_birth = erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    curve = []
    prev = 0
    for idx in sorted(born):
        engine.add(rule_from(born[idx]), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            engine.try_edge(e.winner, e.loser)
        right = ways(engine, truth, queue)["right"].bit_count()
        curve.append({"born_at": idx, "rule_id": born[idx]["rule_id"],
                      "action": born[idx]["action"], "right": right,
                      "delta": right - prev, **birth_row(record, idx)})
        prev = right
    return {"engine": engine, "curve": curve}


def same_base(a: PriorityEngine, b: PriorityEngine) -> bool:
    """Gate 1's comparison: the same rules, extensions and declared edges."""
    ids = [(r.rule_id, r.action) for r in a.rules]
    return (ids == [(r.rule_id, r.action) for r in b.rules]
            and all(a.ext[r.rule_id] == b.ext[r.rule_id] for r in a.rules)
            and all(a.decl_below.get(r.rule_id, set()) == b.decl_below.get(r.rule_id, set())
                    for r in a.rules))


# ---------------------------------------------------------------------------
# The queue's escalations
# ---------------------------------------------------------------------------

def draft_points(payload: dict | None, space: Space, truth: int) -> int | None:
    """A draft's points of the queue over the space, or None if it names none."""
    try:
        conds = [Condition(c["attr"], c["op"], c["value"])
                 for c in (payload or {}).get("conditions") or []]
        return (space.extension(conds) & truth).bit_count() if conds else None
    except (KeyError, TypeError, ValueError, RuleValidationError):
        return None


def escalations(record: dict, engine: PriorityEngine, space: Space, truth: int,
                queue: str = QUEUE) -> list[dict[str, Any]]:
    rows = {r["idx"]: r for r in record["records"]}
    out = []
    for esc in record["escalations"]:
        row = rows.get(esc["idx"], {})
        if row.get("truth") != queue:
            continue
        calls = esc.get("calls") or []
        payload = (calls[0].get("payload") if calls else None) or {}
        out.append({"idx": esc["idx"], "cause": row.get("cause"),
                    "escalated": bool(row.get("escalated")),
                    "governing": row.get("truth_rule"),
                    "draft_action": payload.get("action"),
                    "draft_queue_points": draft_points(payload, space, truth),
                    "verdict": esc.get("verdict"), "rule_id": esc.get("rule_id"),
                    "in_base": esc.get("rule_id") in engine.ext,
                    "listed": len(esc.get("listed") or [])})
    return out


def escalations_are_the_record(escs: list[dict[str, Any]], queue: str = QUEUE) -> bool:
    """Gate 4."""
    return all(e["escalated"] and e["verdict"] in VERDICTS
               and (e["verdict"] != BORN or e["in_base"]) for e in escs)


def left_out(record: dict, space: Space, truth: int,
             queue: str = QUEUE) -> list[dict[str, Any]]:
    """ADDED AFTER THE FIRST RUN. Each of the queue's unplaced escalations: the
    rules its placement round listed and the ones its answer left out, by their
    relation to the draft."""
    rows = {r["idx"]: r for r in record["records"]}
    ext = {r["rule_id"]: brows.ext_of(r, space) for r in record["rules"]}
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    out = []
    for esc in record["escalations"]:
        if rows.get(esc["idx"], {}).get("truth") != queue or esc.get("verdict") != UNPLACED:
            continue
        c1 = un.placement(esc)
        payload = (esc.get("calls") or [{}])[0].get("payload") or {}
        draft = brows.ext_of({"conditions": payload.get("conditions") or []}, space)
        listed = list(esc.get("listed") or [])
        missing = list((c1 or {}).get("unplaced") or [])
        rel = {rid: un.relation(ext[rid], draft) for rid in listed}
        out.append({"idx": esc["idx"], "answered": c1 is not None,
                    "draft_queue_points": (draft & truth).bit_count(),
                    "listed": len(listed),
                    "listed_nested": sum(1 for r in listed if un.nested(rel[r])),
                    "left_out": len(missing), "left_out_rules": missing,
                    "left_out_nested": sum(1 for r in missing if un.nested(rel[r])),
                    "left_out_by_relation": dict(sorted(Counter(rel[r] for r in missing).items())),
                    "left_out_by_queue": dict(sorted(Counter(action[r] for r in missing).items()))})
    return out


# ---------------------------------------------------------------------------
# A run, read whole
# ---------------------------------------------------------------------------

def counts(w: dict[str, Any]) -> dict[str, Any]:
    lost = w["lost"].bit_count()
    out = {"right": w["right"].bit_count(), "lost": lost}
    for k in WAYS + ("contested", "by_edge", "by_containment"):
        out[k] = w[k].bit_count()
    out["lost_by_queue"] = {b: m.bit_count() for b, m in sorted(w["wrong"].items())}
    out["of_lost"] = {k: frac(share(out[k], lost)) for k in WAYS}
    return out


def read_run(record: dict, space: Space, truth: int, regions: dict[str, int],
             stage_c_right: int | None, queue: str = QUEUE) -> dict[str, Any]:
    final = MI.final_engine(record)
    rep = replay(record, space, truth, queue)
    w = ways(final, truth, queue)
    escs = escalations(record, final, space, truth, queue)
    curve = rep["curve"]
    top = max(curve, key=lambda c: c["right"]) if curve else None
    gates = [
        {"gate": 1, "what": "the replay is the base, and the queue's right points are "
                            "Stage C's",
         "passes": same_base(final, rep["engine"])
                   and (stage_c_right is None or w["right"].bit_count() == stage_c_right)},
        {"gate": 2, "what": "the ways partition the loss", "passes": partitions(w, truth)},
        {"gate": 3, "what": "the curve ends at the base",
         "passes": bool(curve) and curve[-1]["right"] == w["right"].bit_count()},
        {"gate": 4, "what": "the escalations are the record's",
         "passes": escalations_are_the_record(escs, queue)},
    ]
    verdicts: dict[str, int] = {}
    for e in escs:
        verdicts[e["verdict"]] = verdicts.get(e["verdict"], 0) + 1
    return {"queue_points": truth.bit_count(), "ways": counts(w),
            "winners": winners(final, record, w),
            "queue_rules": queue_rules(final, record, w, truth, regions, queue),
            "curve": {"most_right": top["right"] if top else 0,
                      "at_birth": top["born_at"] if top else None,
                      "moves": [c for c in curve if c["delta"]]},
            "escalations": escs, "escalation_verdicts": verdicts,
            "added_after_the_first_run": added(record, space, truth, queue),
            "gates": gates}


def containers(record: dict, space: Space, truth: int,
               queue: str = QUEUE) -> list[dict[str, Any]]:
    """ADDED AFTER THE FIRST RUN. Every rule of another queue whose region holds
    every point of the queue, so that it contains every draft of the queue and a
    placement round lists it beside each one."""
    return [{"rule_id": r["rule_id"], "action": r["action"], "born_at": r["born_at"],
             "conditions": r["conditions"]}
            for r in sorted(record["rules"], key=lambda r: r["born_at"])
            if r["action"] != queue and brows.ext_of(r, space) & truth == truth]


def added(record: dict, space: Space, truth: int, queue: str = QUEUE) -> dict[str, Any]:
    """ADDED AFTER THE FIRST RUN: the queue's unplaced escalations, how many of
    them left each rule out, and the rules of another queue that contain the whole
    queue."""
    out = left_out(record, space, truth, queue)
    return {"left_out": out,
            "times_each_rule_was_left_out": dict(Counter(
                r for e in out for r in e["left_out_rules"]).most_common()),
            "containers_of_the_queue": containers(record, space, truth, queue)}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    r = runs[tag]
    n = r["queue_points"]
    half = L_HALF * n
    lost, wy = r["ways"]["lost"], r["ways"]
    t2 = wy["lost_by_queue"].get("T2_TECHNICAL", 0)
    widest = max((q["queue_points"] for q in r["queue_rules"]), default=0)
    born = r["escalation_verdicts"].get(BORN, 0)
    others = {t: max((q["queue_points"] for q in o["queue_rules"]), default=0)
              for t, o in runs.items() if t != tag}
    return [
        {"clause": "L1", "what": "at least half of the lost points are unwritten",
         "reading": {"unwritten": wy["unwritten"], "of": lost,
                     "share": frac(share(wy["unwritten"], lost))},
         "holds": lost > 0 and F(wy["unwritten"], lost) >= L_HALF},
        {"clause": "L2", "what": "at least half of the lost points go to T2_TECHNICAL",
         "reading": {"to_T2_TECHNICAL": t2, "of": lost, "share": frac(share(t2, lost))},
         "holds": lost > 0 and F(t2, lost) >= L_HALF},
        {"clause": "L3", "what": "no rule of the queue covers half of the queue's points "
                                 "or more",
         "reading": {"widest": widest, "of": n, "share": frac(share(widest, n))},
         "holds": widest < half},
        {"clause": "L4", "what": f"at least {L4_BORN} of the queue's escalations ended "
                                 "with their rule born",
         "reading": {"born": born, "of": len(r["escalations"]),
                     "verdicts": r["escalation_verdicts"]},
         "holds": born >= L4_BORN},
        {"clause": "L5", "what": "after no birth did the base decide half of the queue's "
                                 "points right or more",
         "reading": {"most_right": r["curve"]["most_right"], "at_birth":
                     r["curve"]["at_birth"], "of": n,
                     "share": frac(share(r["curve"]["most_right"], n))},
         "holds": r["curve"]["most_right"] < half},
        {"clause": "L6", "what": "in each other run some rule of the queue covers half of "
                                 "the queue's points or more",
         "reading": {t: {"widest": v, "share": frac(share(v, n))} for t, v in others.items()},
         "holds": bool(others) and all(v >= half for v in others.values())},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {}
    for arm, rep in plan.schedule():
        records[plan.tag(arm, rep)] = json.loads(plan.run_path(arm, rep).read_text())
    return records, json.loads(plan.score_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why c r1 lost SECURITY_INCIDENT "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"channel/lost.py writes {record_path()}")
    records, stage_c = read_all()
    space = MI.space()
    truth = MI.space_truth()[QUEUE]
    regions = rl_refs.regions()
    runs = {}
    for t, rec in records.items():
        right = stage_c["CH-g"]["runs"][t]["recall_space"][QUEUE][0]
        runs[t] = read_run(rec, space, truth, regions, right)
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
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
        "added_after_the_first_run": ADDED,
        "source": {"score": str(plan.score_path()),
                   "score_from": stage_c["_env"].get("git_commit")},
        "surface": "the exhaustive space, 134,400 points",
        "queue": QUEUE,
        "run": plan.tag(*RUN),
        "constants": {"L_HALF": str(L_HALF), "L4_BORN": L4_BORN},
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
