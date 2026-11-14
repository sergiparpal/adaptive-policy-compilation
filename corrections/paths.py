"""
WHY A RULE'S WINS REACH THE RULE IT SHOULD LOSE TO.
`corrections/fall.py` found most of what L's bases lost after their peaks left
in conflicts. At those conflicts the newborn had been declared below a rule of
the point's true queue, mostly `SECURITY_INCIDENT`'s, and the engine refused the
edge for closing a cycle: the newborn's own wins, installed first, already
reached that rule. Its *What it does not settle*, item 2, and `IDEAS.md` leave
why. The paths may run through rules wrongly above `SECURITY_INCIDENT`'s, or
through rules that do not match the contested points. Asked for by Sergi on
2026-11-14, after that reading. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**A refused right side** is a pair `(n, u)` that `corrections/fall.py`'s `beside`
classes below_refused. At the last loss of a point lost by a conflict, `u`, a
rule of the point's true queue `q`, stands undefeated beside the newborn `n`, and
the edge `u` beats `n`, which `n`'s answer declared, was refused for closing a
cycle. The pair's *points* are the points lost by that conflict where `u` stands
beside `n`. Each pair is weighed by its points, as `beside` weighs it.

**The pair is read in the base right after `n`'s birth and its edges.** The
edges tried after the refusal at that birth point into `n`. They open no path
out of it, so what `n` reaches is what it reached at the refusal.
- **The paths** are the chains of what beats what, by containment and by
  declared edges, from `n` to `u`. Their *rules* are the rules on some such
  chain, `n` and `u` left out.
- **A crossing** is a step of a path from a rule of another queue to a rule of
  `q`: a rule of another queue above one of `q`, nested inside it or declared
  above it. Every path has one, since `n` is not of `q` and `u` is.
- **The policy's verdict on a crossing** reads the points both of its rules
  match. It is *wrong* when more of them are `q`'s than the upper rule's queue's,
  *right* when fewer, and *even* when as many.

**Every pair is in one class**:
  wrong_declared  no path is left once the wrong declared crossings are taken
                  out;
  wrong_nested    some path is left then, and none once the wrong nested
                  crossings are taken out too;
  right           some path is left once every wrong crossing is taken out.

**The cycle is never at the pair's points.** `u` is undefeated there, so no rule
that beats `u` matches them, and every path enters `u` through a rule that misses
them. Gate 4 checks it. So the reading asks where else the cycle is, over the
pair's *shared region*, the points both `n` and `u` match:
  somewhere  some path runs through rules that all match some point of it, and
             the edge refused would close a cycle there;
  nowhere    no path does: every path runs through a rule that misses every
             point either rule of the pair decides.

**Also read**, per pair: the shortest path's length, whether the paths' rules
touch the pair's points, and whether the newborn itself crosses into `q`. Per
run: the distinct crossings on the paths by kind and verdict, and the wrong
declared ones by the cause of the birth that installed them.

**Arm N is read the same way**, as the control.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its rules, their extensions and its declared
     edges are `manual.instrument.final_engine`'s, compared as `channel/lost.py`'s
     gate 1 compares them.
  2. **The pairs are `fall.json`'s.** In every run, the pairs' points sum to
     `beside`'s below_refused, and the conflicts they are read at hold
     `beside`'s points.
  3. **Every refusal is the engine's.** Each pair's edge is in the record's log
     at `n`'s birth, refused for closing a cycle, and `n` reaches `u` right after
     that birth.
  4. **No path touches the pair's points.** No rule that beats `u` matches
     them, and no path runs through rules that all match one of them.
  5. **The classes partition the pairs' points**, and so do somewhere and
     nowhere.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
K1 to K4 pool L's three runs. K5 reads N r3, the one N run whose refused right
sides held many points: `fall.json` gives N r1 and N r2 few.

  K1. **Wrong above.** At least half of the pairs' points are in pairs of
      wrong_declared or wrong_nested.
  K2. **Placed, not nested.** At least half of those are wrong_declared.
  K3. **Placed by the corrections.** Of the distinct wrong declared crossings
      on the paths, the share installed at a birth at a reported error is at
      least the share of the runs' births at a reported error.
  K4. **The cycle is real somewhere.** At least half of the pairs' points are in
      pairs whose cycle is somewhere.
  K5. **N alike.** In N r3, at least half of the pairs' points are in pairs of
      wrong_declared or wrong_nested.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account.**
- **The newborn beats a rule that sits above `SECURITY_INCIDENT`'s.** Its answer
  declares wins over many rules of other queues. Some of those rules were placed
  above a rule of `SECURITY_INCIDENT` by an earlier declaration, wrong on the
  keyword points they share.
- **The corrections placed them.** Told that the engine had erred, a correction
  declares itself above the rules it overlaps, `SECURITY_INCIDENT`'s among them.
- **The rule above `SECURITY_INCIDENT`'s cannot match the contested points**,
  since `SECURITY_INCIDENT`'s rule is undefeated there. It shares other points
  with both rules of the pair, so the cycle the engine refuses is real
  somewhere in their shared region, where the rule above already decides.
- **N r3 refuses the same way**, through its own rules placed above
  `SECURITY_INCIDENT`'s, with no label.

**The bet is K4.** It says the engine's refusals guard a cycle that exists, and
not only one through unrelated rules, as `PLAN_CHANNEL.md`'s reading of a
refused right edge found. **K1 is trusted most**: on the keyword's points the
policy puts `SECURITY_INCIDENT` above every other queue but at `H03`'s, so a
rule of another queue above one of its rules errs on most of the keyword points
they share. **K3 is trusted least**: `corrections/forgotten.py`'s F5 and
`corrections/fall.py`'s Q3 bet that the corrections did more than their share,
and both failed.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, `fall.json`, `forgotten.json` and
  `broad.json`, including `beside`'s classes and what closed each refusal;
- in L r1's record: R0089's and R0214's placement answers, their edges tried
  and refused, and their rules;
- the hidden policy and the level 1 catalogue's text;
- `rung2/engine2.py`'s arbitration and `try_edge`, `authorship/loop.py`'s
  installation order, and `corrections/fall.py`'s replay and `beside`.

**What the drafter had not seen**: any path from a newborn to a rule it was
refused a loss to, any crossing, or any verdict of the policy on an edge of the
base.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: THE EVEN CROSSINGS, AND AN ENGINE THAT REFUSES
ONLY WHERE THE CYCLE IS
--------------------------------------------------------------------------
The first run found almost every pair right, and almost every cycle nowhere.
Read by hand, the largest pairs' paths entered `SECURITY_INCIDENT`'s rule
through a rule of `T2_TECHNICAL` nested inside it. The verdict on that crossing
is even: the nested rule matches as many of `SECURITY_INCIDENT`'s points as of
its own queue's. So this part reads:
- **the even crossings.** Each pair's paths are cut again, with the wrong and the
  even crossings taken out. The pairs of class right that this cuts are read
  apart. Per run, the distinct rules above those even crossings are given with
  their conditions, the cause of their birth and the policy's rule for the
  ticket they were born at.
- **an engine that refuses only where the cycle is.** The same births and the
  same declarations, in the record's order, are replayed with an edge refused for
  a cycle only when the cycle runs through rules that all match some point both
  of its rules match. That is a point the edge decides. Such an engine leaves a
  cycle through rules that miss every such point in the base, where no point
  sees it. The replay gives the peak, the final share, the fall, the recall of
  `SECURITY_INCIDENT`, the conflicts and the edges refused, beside the record's
  engine. It is not the loop that would have run: a base ordered otherwise
  decides the arrivals otherwise, and would have escalated other cases.

It adds gate 6. The replayed engine leaves no point that some rule matches with
no rule undefeated. Every 997th point is decided by its masks as
`PriorityEngine.decide` decides it, and its masks are
`blind.rows.undefeated_masks`' over its final base. Both parts were tried on
the records in a scratch script before they were written here. They were
written after the five clauses above had been read: K2 holds, and K1, K3, K4 and
K5 fail. They carry no expectation and move no clause.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-14, after `corrections/fall.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m corrections.paths --dry-run   # gates 1 to 6; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.paths
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.ceiling_check import all_cases
from harness.provenance import describe, environment

from channel import lost as ch_lost
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from blind import rows as brows
from rung2.engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK, EDGE_SELF,
                           EDGE_UNKNOWN, PriorityEngine, Space, strictly_below)

from . import fall as fl
from . import forgotten as fg
from . import plan

F = Fraction
UNLABELLED = fl.UNLABELLED

# A pair's classes, and where its cycle is.
WRONG_DECLARED, WRONG_NESTED, RIGHT = "wrong_declared", "wrong_nested", "right"
CLASSES = (WRONG_DECLARED, WRONG_NESTED, RIGHT)
SOMEWHERE, NOWHERE = "somewhere", "nowhere"
# A crossing's kind and the policy's verdict on it.
NESTED, DECLARED = "nested", "declared"
WRONG, EVEN, RIGHT_VERDICT = "wrong", "even", "right"

# The expectation's lines.
K1_SHARE = F(1, 2)
K2_SHARE = F(1, 2)
K4_SHARE = F(1, 2)
K5_SHARE = F(1, 2)
K5_RUN = plan.tag(UNLABELLED, 3)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-14, after corrections/fall.py. The expectation "
    "in the module's docstring was written and committed before the reading ran. Not a "
    "signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its five clauses were read: each pair cut again with "
    "the wrong and the even crossings taken out, the rules above the even crossings, and the "
    "same births replayed with an engine that refuses an edge only where its cycle runs "
    "through rules that all match a point the edge decides. Both were tried in a scratch "
    "script first. No expectation; no clause moves.")
# Gate 6 reads every STRIDE-th point of the replayed engine's final base.
STRIDE = fl.STRIDE

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "paths.json"


# ---------------------------------------------------------------------------
# The conflicts `corrections/fall.py` read
# ---------------------------------------------------------------------------

def last_conflicts(record: dict[str, Any], space: Space, truth: dict[str, int],
                   cases: Sequence) -> dict[int, int]:
    """At every birth after the peak, the points lost by a conflict there at their
    last loss, as `corrections/fall.py`'s `read_run` reads them. Gate 2 holds
    them to `fall.json`."""
    steps = fl.replay(record, space, truth, cases)["steps"]
    if not steps:
        return {}
    counts = [s["right"].bit_count() for s in steps]
    p = counts.index(max(counts))
    lost = steps[p]["right"] & ~steps[-1]["right"]
    assigned = 0
    out: dict[int, int] = {}
    for s in reversed(steps[p + 1:]):
        last = s["lost"] & lost & ~assigned
        if not last:
            continue
        assigned |= last
        if last & s[fl.CONFLICT]:
            out[s["idx"]] = last & s[fl.CONFLICT]
    return out


# ---------------------------------------------------------------------------
# The paths
# ---------------------------------------------------------------------------

def forward(engine: PriorityEngine, src: str, skip: set[tuple[str, str]] | None = None
            ) -> set[str]:
    """Every rule `src` reaches by what beats what, the steps in `skip` left out."""
    seen: set[str] = set()
    stack = [src]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        for y in engine.wins_over(x):
            if not skip or (x, y) not in skip:
                stack.append(y)
    return seen


def backward(engine: PriorityEngine, dst: str) -> set[str]:
    """Every rule that reaches `dst`."""
    seen: set[str] = set()
    stack = [dst]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(engine.beats_me(x))
    return seen


def shortest(engine: PriorityEngine, src: str, dst: str, nodes: set[str]) -> int | None:
    """The fewest steps from `src` to `dst` through `nodes`."""
    level, seen, dist = [src], {src}, 0
    while level:
        if dst in level:
            return dist
        dist += 1
        nxt = []
        for x in level:
            for y in engine.wins_over(x):
                if y in nodes and y not in seen:
                    seen.add(y)
                    nxt.append(y)
        level = nxt
    return None


def local_reach(engine: PriorityEngine, src: str, dst: str, nodes: set[str],
                region: int) -> int:
    """The points of `region` where `src` reaches `dst` through rules of `nodes`
    that all match the point."""
    m = {src: region & engine.ext[src]}
    stack = [src]
    while stack:
        x = stack.pop()
        for y in engine.wins_over(x):
            if y not in nodes:
                continue
            new = m[x] & engine.ext[y]
            if new & ~m.get(y, 0):
                m[y] = m.get(y, 0) | new
                stack.append(y)
    return m.get(dst, 0)


def verdict(engine: PriorityEngine, upper: str, lower: str, action: dict[str, str],
            truth: dict[str, int]) -> str:
    """The policy on the points both rules match: `wrong` when more are the lower
    rule's queue's than the upper's, `right` when fewer, `even` when as many."""
    both = engine.ext[upper] & engine.ext[lower]
    low = (both & truth.get(action[lower], 0)).bit_count()
    up = (both & truth.get(action[upper], 0)).bit_count()
    return WRONG if low > up else RIGHT_VERDICT if up > low else EVEN


def analyse(engine: PriorityEngine, n: str, u: str, at: int, action: dict[str, str],
            truth: dict[str, int], installed_at: dict[tuple[str, str], int],
            cause_of: dict[int, str | None]) -> dict[str, Any]:
    """One refused right side, read in the base right after `n`'s birth."""
    q = action[u]
    reach_n = forward(engine, n)
    nodes = reach_n & backward(engine, u)
    rules = nodes - {n, u}
    crossings = []
    for x in sorted(nodes - {u}):
        for y in sorted(engine.wins_over(x)):
            if y in nodes and action[x] != q and action[y] == q:
                kind = NESTED if y in engine.sub_above[x] else DECLARED
                born = installed_at.get((x, y)) if kind == DECLARED else None
                crossings.append({"upper": x, "lower": y, "kind": kind,
                                  "verdict": verdict(engine, x, y, action, truth),
                                  "installed_at": born,
                                  "cause": None if born is None else cause_of.get(born)})
    wrong_declared = {(c["upper"], c["lower"]) for c in crossings
                      if c["verdict"] == WRONG and c["kind"] == DECLARED}
    wrong_all = {(c["upper"], c["lower"]) for c in crossings if c["verdict"] == WRONG}
    if u not in forward(engine, n, wrong_declared):
        cls = WRONG_DECLARED
    elif u not in forward(engine, n, wrong_all):
        cls = WRONG_NESTED
    else:
        cls = RIGHT
    not_right = {(c["upper"], c["lower"]) for c in crossings
                 if c["verdict"] != RIGHT_VERDICT}
    even_cut = cls == RIGHT and u not in forward(engine, n, not_right)
    shared = engine.ext[n] & engine.ext[u]
    touched = 0
    for x in rules:
        touched |= engine.ext[x] & at
    return {"newborn": n, "rule": u, "queue": q, "points": at.bit_count(), "class": cls,
            "where": SOMEWHERE if local_reach(engine, n, u, nodes, shared) else NOWHERE,
            "shortest": shortest(engine, n, u, nodes), "path_rules": len(rules),
            "touched": touched.bit_count(),
            "own_crossing": any(c["upper"] == n for c in crossings),
            "even_cut": even_cut,
            "crossings": crossings,
            "reaches": u in reach_n,
            "beaters_miss": not any(engine.ext[b] & at for b in engine.beats_me(u)),
            "local_at_points": local_reach(engine, n, u, nodes, at)}


def trace(record: dict[str, Any], space: Space, truth: dict[str, int],
          conflicts: dict[int, int]) -> dict[str, Any]:
    """The base in birth order. At every birth with points lost by a conflict,
    each refused right side standing on them, read right after the birth."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    escs = fg.escalation_at(record)
    cause_of = {i: (escs.get(i) or {}).get("kind") for i in born}
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    installed_at: dict[tuple[str, str], int] = {}
    pairs: list[dict[str, Any]] = []
    logged_ok = True
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        refused: list[str] = []
        for e in by_birth.get(idx, []):
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            logged_ok &= why == e.verdict
            if why == EDGE_OK and not before and e.loser in engine.decl_above[e.winner]:
                installed_at[(e.winner, e.loser)] = idx
            if why == EDGE_CYCLE and e.loser == rid and e.winner not in refused:
                refused.append(e.winner)
        fl.settle(engine, und, action, rid, d["action"])
        c = conflicts.get(idx, 0)
        if not c:
            continue
        for u in refused:
            at = und.get(u, 0) & c
            if at:
                got = analyse(engine, rid, u, at, action, truth, installed_at, cause_of)
                got["born_at"] = idx
                pairs.append(got)
    return {"engine": engine, "pairs": pairs, "logged_ok": logged_ok,
            "births_by_cause": dict(Counter(cause_of.values()))}


# ---------------------------------------------------------------------------
# Added after the first run: an engine that refuses only where the cycle is
# ---------------------------------------------------------------------------

def try_edge_where(engine: PriorityEngine, winner: str, loser: str) -> str:
    """`PriorityEngine.try_edge`, with a cycle refused only when it runs through
    rules that all match some point both of the edge's rules match. The engine
    is not edited: this installs the edge in its sets as `try_edge` does."""
    if winner == loser:
        return EDGE_SELF
    if winner not in engine.ext or loser not in engine.ext:
        return EDGE_UNKNOWN
    ew, el = engine.ext[winner], engine.ext[loser]
    if ew & el == 0:
        return EDGE_DISJOINT
    if strictly_below(el, ew):
        return EDGE_CONTRADICTS
    if strictly_below(ew, el):
        return EDGE_OK
    if fl.reaches(engine, loser, winner):
        nodes = forward(engine, loser) & backward(engine, winner)
        if local_reach(engine, loser, winner, nodes, ew & el):
            return EDGE_CYCLE
    engine.decl_below[loser].add(winner)
    engine.decl_above[winner].add(loser)
    return EDGE_OK


def where_replay(record: dict[str, Any], space: Space, truth: dict[str, int],
                 cases: Sequence) -> dict[str, Any]:
    """The same births and declarations, in the record's order, with
    `try_edge_where` for `try_edge`; and gate 6's checks on its final base."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    curve: list[int] = []
    refused = 0
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            refused += try_edge_where(engine, e.winner, e.loser) == EDGE_CYCLE
        fl.settle(engine, und, action, rid, d["action"])
        curve.append(fl.right_of(fl.decision(und, action), truth).bit_count())
    dec = fl.decision(und, action)
    right = fl.right_of(dec, truth)
    matched = 0
    for r in engine.rules:
        matched |= engine.ext[r.rule_id]
    n = space.n
    decide_ok = all(fl.is_the_engines(engine, cases[n - 1 - j], dec, j)
                    for j in range(0, n, STRIDE))
    return {"curve": curve, "refused": refused, "right": right.bit_count(),
            "security": (right & truth.get(fl.SEC, 0)).bit_count(),
            "conflict": dec["two"].bit_count(),
            "ok": (matched & ~dec["one"]) == 0 and decide_ok
                  and und == brows.undefeated_masks(engine)}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], space: Space, truth: dict[str, int], cases: Sequence,
             fall_run: dict[str, Any], final: PriorityEngine | None = None) -> dict[str, Any]:
    """One run's refused right sides, classed, and the gates. `fall_run` is the
    run's entry in `fall.json`. `final` is the run's final base,
    `manual.instrument.final_engine`'s by default."""
    final = final if final is not None else MI.final_engine(record)
    conflicts = last_conflicts(record, space, truth, cases)
    got = trace(record, space, truth, conflicts)
    pairs = got["pairs"]
    points = sum(p["points"] for p in pairs)

    def weigh(key) -> dict[str, int]:
        c: Counter = Counter()
        for p in pairs:
            c[key(p)] += p["points"]
        return dict(c)

    distinct: dict[tuple[str, str], dict[str, Any]] = {}
    for p in pairs:
        for c in p["crossings"]:
            distinct.setdefault((c["upper"], c["lower"]), c)
    wrong_declared = [c for c in distinct.values()
                      if c["kind"] == DECLARED and c["verdict"] == WRONG]
    newborns = {(p["newborn"], p["born_at"]) for p in pairs}
    by_class = weigh(lambda p: p["class"])
    where = weigh(lambda p: p["where"])
    summary = {
        "pairs": len(pairs), "points": points,
        "by_class": {k: by_class.get(k, 0) for k in CLASSES},
        "where": {k: where.get(k, 0) for k in (SOMEWHERE, NOWHERE)},
        "by_queue": weigh(lambda p: p["queue"]),
        "shortest": {str(k): v for k, v in sorted(weigh(lambda p: p["shortest"]).items(),
                                                   key=lambda kv: (kv[0] is None, kv[0]))},
        "touched": sum(p["touched"] for p in pairs),
        "own_crossing": sum(p["points"] for p in pairs if p["own_crossing"]),
        "crossings": dict(Counter(f"{c['kind']}:{c['verdict']}" for c in distinct.values())),
        "wrong_declared": {
            "distinct": len(wrong_declared),
            "by_cause": dict(Counter(c["cause"] for c in wrong_declared)),
            "installed_by_the_newborn": sum(1 for c in wrong_declared
                                            if (c["upper"], c["installed_at"]) in newborns)},
        "births_by_cause": got["births_by_cause"],
    }
    beside = fall_run["added_after_the_first_run"]["beside"]
    gates = [
        {"gate": 1, "what": "the replay is the base",
         "passes": ch_lost.same_base(final, got["engine"])},
        {"gate": 2, "what": "the pairs are fall.json's",
         "passes": points == beside["pairs"]["below_refused"]
                   and sum(m.bit_count() for m in conflicts.values()) == beside["points"]},
        {"gate": 3, "what": "every refusal is the engine's",
         "passes": got["logged_ok"] and all(p["reaches"] for p in pairs)},
        {"gate": 4, "what": "no path touches the pair's points",
         "passes": all(p["beaters_miss"] and p["local_at_points"] == 0 for p in pairs)},
        {"gate": 5, "what": "the classes partition the pairs' points",
         "passes": sum(summary["by_class"].values()) == points
                   and sum(summary["where"].values()) == points},
    ]
    rows = {r["idx"]: r for r in record["records"]}
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    above_even: dict[str, int] = {}
    for p in pairs:
        if p["even_cut"]:
            for upper in {c["upper"] for c in p["crossings"] if c["verdict"] == EVEN}:
                above_even[upper] = above_even.get(upper, 0) + p["points"]
    where_run = where_replay(record, space, truth, cases)
    gates.append({"gate": 6, "what": "the engine that refuses only where the cycle is leaves "
                                     "no point without a rule undefeated, and decides as "
                                     "its masks do",
                  "passes": where_run["ok"]})
    added = {
        "even_cut": sum(p["points"] for p in pairs if p["even_cut"]),
        "stands_on_right": sum(p["points"] for p in pairs
                               if p["class"] == RIGHT and not p["even_cut"]),
        "rules_above_even": [
            {"rule_id": rid, "action": rules[rid]["action"],
             "conditions": rules[rid]["conditions"], "born_at": rules[rid]["born_at"],
             "cause": (escs.get(rules[rid]["born_at"]) or {}).get("kind"),
             "ticket_rule": (rows.get(rules[rid]["born_at"]) or {}).get("truth_rule"),
             "points": pts}
            for rid, pts in sorted(above_even.items(), key=lambda kv: (-kv[1], kv[0]))],
        "where": {"engine": fl.order_summary({**where_run, "cycles": where_run["refused"]},
                                             truth, space.n),
                  "record": fall_run["added_after_the_first_run"]["orders"]["declared"]},
    }
    keep = ("born_at", "newborn", "rule", "queue", "points", "class", "where", "shortest",
            "path_rules", "touched", "own_crossing", "even_cut")
    out_pairs = [{**{k: p[k] for k in keep},
                  "crossings": [{k: c[k] for k in ("upper", "lower", "kind", "verdict",
                                                   "installed_at", "cause")}
                                for c in p["crossings"]]} for p in pairs]
    return {"summary": summary, "pairs": out_pairs, "gates": gates,
            "added_after_the_first_run": added}


def read_all_runs(records: dict[str, dict], fall_record: dict[str, Any], space: Space,
                  truth: dict[str, int], cases: Sequence,
                  finals: dict[str, PriorityEngine] | None = None) -> dict[str, dict]:
    finals = finals or {}
    return {tag: read_run(rec, space, truth, cases, fall_record["runs"][tag],
                          final=finals.get(tag))
            for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    L = [runs[plan.tag(plan.LABELLED, k)]["summary"] for k in range(1, plan.REPS + 1)
         if plan.tag(plan.LABELLED, k) in runs]
    pts = sum(s["points"] for s in L)
    wrong = sum(s["by_class"][WRONG_DECLARED] + s["by_class"][WRONG_NESTED] for s in L)
    declared = sum(s["by_class"][WRONG_DECLARED] for s in L)
    somewhere = sum(s["where"][SOMEWHERE] for s in L)
    crossings = sum(s["wrong_declared"]["distinct"] for s in L)
    at_error = sum(s["wrong_declared"]["by_cause"].get(plan.ERROR, 0) for s in L)
    births = sum(sum(s["births_by_cause"].values()) for s in L)
    births_error = sum(s["births_by_cause"].get(plan.ERROR, 0) for s in L)
    k3, k3b = share(at_error, crossings), share(births_error, births)
    n3 = runs.get(K5_RUN, {}).get("summary")
    n3_wrong = (n3["by_class"][WRONG_DECLARED] + n3["by_class"][WRONG_NESTED]) if n3 else 0
    n3_pts = n3["points"] if n3 else 0
    return [
        {"clause": "K1", "what": "at least half of L's pairs' points are in pairs of "
                                 "wrong_declared or wrong_nested",
         "reading": {"wrong": wrong, "of": pts, "share": frac(share(wrong, pts))},
         "holds": pts > 0 and F(wrong, pts) >= K1_SHARE},
        {"clause": "K2", "what": "at least half of those are wrong_declared",
         "reading": {"wrong_declared": declared, "of": wrong,
                     "share": frac(share(declared, wrong))},
         "holds": wrong > 0 and F(declared, wrong) >= K2_SHARE},
        {"clause": "K3", "what": "the share of the distinct wrong declared crossings "
                                 "installed at a reported error is at least the share of "
                                 "births at a reported error",
         "reading": {"crossings_at_a_reported_error": at_error, "of_crossings": crossings,
                     "crossings_share": frac(k3), "births_at_a_reported_error": births_error,
                     "of_births": births, "births_share": frac(k3b)},
         "holds": k3 is not None and k3b is not None and k3 >= k3b},
        {"clause": "K4", "what": "at least half of L's pairs' points are in pairs whose "
                                 "cycle is somewhere",
         "reading": {"somewhere": somewhere, "of": pts, "share": frac(share(somewhere, pts))},
         "holds": pts > 0 and F(somewhere, pts) >= K4_SHARE},
        {"clause": "K5", "what": "in N r3, at least half of the pairs' points are in pairs of "
                                 "wrong_declared or wrong_nested",
         "reading": {"wrong": n3_wrong, "of": n3_pts, "share": frac(share(n3_wrong, n3_pts))},
         "holds": n3_pts > 0 and F(n3_wrong, n3_pts) >= K5_SHARE},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return records, json.loads(fl.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why a rule's wins reach the rule it should "
                                             "lose to (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 6 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/paths.py writes {record_path()}")
    records, fall_record = read_all()
    runs = read_all_runs(records, fall_record, MI.space(), MI.space_truth(),
                         list(all_cases()))
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
        "added_after_the_first_run": ADDED,
        "source": {"fall": str(fl.record_path()),
                   "fall_from": fall_record["_env"].get("git_commit")},
        "surface": "the refused right sides at the points lost by a conflict after each "
                   "run's peak, as fall.json reads them; their paths over the whole space",
        "constants": {"K1_SHARE": str(K1_SHARE), "K2_SHARE": str(K2_SHARE),
                      "K4_SHARE": str(K4_SHARE), "K5_SHARE": str(K5_SHARE),
                      "K5_RUN": K5_RUN},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: {s['pairs']} pairs on {s['points']} points; {s['by_class']}; "
              f"{s['where']}")
        a = r["added_after_the_first_run"]
        print(f"    even cut {a['even_cut']}, stands on right {a['stands_on_right']}; final "
              f"share, the record's engine {a['where']['record']['final']['share']['value']:.4f}, "
              f"refusing only where the cycle is {a['where']['engine']['final']['share']['value']:.4f}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
