"""
WHY SO MANY RULES SIT ABOVE THE GATEWAY.
`corrections/paths.py` found the paths of the refused right sides entering
`SECURITY_INCIDENT`'s rule through a rule nested in the keyword's region, born
at a reported ticket of `H03`. Such a rule beats the keyword's rule by
containment, so every rule above it reaches the keyword's rule, and so does any
newborn whose wins reach one of them. Its *What it does not settle*, item 2, and
`IDEAS.md` leave which declarations put the rules of other queues above that
rule, and why the paths to it run so long. Asked for by Sergi on 2026-11-15,
after that reading. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**A run's gateways** are the rules `paths.json` gives above its even crossings,
born at a ticket of `H03`, of a queue other than `SECURITY_INCIDENT`: R0061 in
L r1, R0048 and R0120 in L r2, R0016 in L r3 and R0175 in N r3. N r1 and N r2
have none.

**The base is replayed in birth order**, as `corrections/paths.py` replays it.
After each birth:
- **the rules above the gateways** are the rules that reach a gateway born so
  far, by what beats what, by containment and by declared edges, the gateways
  left out;
- **a door** is a rule one step above a gateway: nested inside it, or declared
  above it;
- **a rule's depth** is the fewest steps from it to a gateway. A door's is one.

**Each rule above a gateway at the run's end entered at one birth**, the first
after which it reaches one. Every edge a birth tries has the rule born there on
one side (gate 3), so a rule enters at its own birth, or through the rule born
at a later one:
  containment  at its own birth, through a rule that contains it, which it
               beats by containment;
  own_wins     at its own birth, through one of its declared wins, and through
               no rule that contains it;
  brought      at a later birth, through the newborn, which is above a gateway
               from its birth: the rule reaches the newborn, through one of the
               newborn's declared losses or through a rule nested inside it;
  at_gateway   at a gateway's birth, through that gateway, in the same two ways.
A rule brought, or entered at a gateway, is *by_losses* when it reaches the rule
born then only through that rule's declared losses, and *by_region* otherwise.

**A door's edge into a gateway** is read by what installed it:
  nested        the door is nested inside the gateway;
  gateway_loss  declared at the gateway's birth: the gateway's answer put the
                door above it;
  door_win      declared at the door's birth: the door's answer put itself
                above the gateway.
The policy's verdict on it is `corrections/paths.py`'s, on the points both rules
match. Each door also carries the rules above it, itself included, and the rules
above a gateway that reach none once its edges into the gateways are taken out.

**The pairs through a gateway** are `paths.json`'s pairs that the even crossings
cut, among which one runs from a gateway. Each is read right after its newborn's
birth, as `paths.json` reads it. That reading gives:
- the newborn's distance to the pair's gateways;
- whether the newborn shares a point with one of them;
- its declared wins, how many are above a gateway, and the depth of the nearest;
- what its answer said of the pair's gateways, and whether its round listed
  them.
Each pair is weighed by its points, as `paths.json` weighs it, and each newborn
also by the points of its pairs taken once.

**Also read**, per run: the number of rules above the gateways after every
birth, by queue at the end, and the rules each birth brought.

**Arm N is read the same way**, as the control. Only N r3 has a gateway.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its rules, their extensions and its declared
     edges are `manual.instrument.final_engine`'s, compared as `channel/lost.py`'s
     gate 1 compares them.
  2. **The gateways and the pairs are `paths.json`'s.** Each gateway is in the
     base with the conditions and the birth `paths.json` gives, and lies inside
     the keyword's region. The refused right sides, traced again, are
     `paths.json`'s pairs, with their births, rules and points.
  3. **Every edge a birth tries has the rule born there on one side.**
  4. **The rules above the gateways only grow**: none leaves after a birth.
  5. **Every newborn of a pair through a gateway reaches one of the pair's
     gateways** right after its birth, and its distance, one step added, is at
     least `paths.json`'s shortest path.
  6. **Every rule above a gateway at the end is classed once, at a depth of at
     least one, and every door's edge is classed.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
D1 to D5 pool L's three runs. D6 reads N r3, the one N run with a gateway.

  D1. **Many above.** Of the rules born after their run's first gateway, at
      least half are above a gateway at the run's end.
  D2. **By their own wins.** Of the rules above a gateway at the end, at least
      half entered own_wins.
  D3. **Few doors.** Of the rules above a gateway at the end, at least half are
      at a depth of two or more.
  D4. **The doors placed themselves.** Of the declared edges from a door into a
      gateway at the end, at least half are door_win.
  D5. **No step from the newborn.** At least half of the points of the pairs
      through a gateway are in pairs whose newborn shares no point with any of
      the pair's gateways.
  D6. **N alike.** In N r3, of the rules born after its gateway, at least half
      are above it at the run's end.

A share over nothing has no value, and a clause that reads one fails.

**The drafter's account.**
- **The gateway meets most rules.** Its conditions are the keyword and a
  severity. They leave every other attribute free, so most rules of other queues
  share points with it.
- **An answer declares wins over many listed rules**, as R0214's declared 34.
  Once some rules sit above the gateway, a newborn whose wins include one of
  them is above it from its birth. So most rules born after the gateway end
  above it (D1), mostly through their own wins (D2).
- **The doors placed themselves.** The gateway was born early, beside few rules
  it could be listed against. The rules born after it that meet it were listed
  it in their rounds, and those that declared themselves above it did so in
  their own answers (D4).
- **The doors are few.** A round that listed the gateway mostly put it above the
  newborn, as R0214's did. So most rules above the gateway reach it through
  other rules (D3), and the paths run long.
- **The newborns of the pairs mostly miss the gateway** (D5). An edge between
  two rules that share no point is never installed, so such a newborn reaches
  the gateway only through rules that meet both, two steps or more. Many of the
  policy's rules below the keyword's layer hold severities of two or less, where
  no gateway has a point.
- **N r3 is alike**, with no label (D6).

**The bet is D2.** It says the proposer's own answers put the rules above the
gateway. Containment, and newborns that bring older rules up with them, would
not need those answers. **D3 is trusted most**: on most pair-points the shortest
path runs three steps or more to the gateway. **D5 is trusted least**: R0214,
whose pairs were L r1's largest, meets R0061, and R0135, in L r2, meets neither
of its gateways.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, `paths.json`, `fall.json`, `forgotten.json`
  and `broad.json`: each pair's newborn, rule, points, shortest path, number of
  rules on its paths and crossings, and the rules above the even crossings;
- in L r1's record: R0089's and R0214's placement answers, their edges tried
  and refused, and their rules. R0214's answer declared it below R0061, refused
  for a cycle. R0089's two declared wins, R0075 and R0062, were born after
  R0061, and its note calls them rules of `ACCOUNT_MANAGER` based on prior
  tickets. Its pair with R0069 has a shortest path of three and two rules on its
  paths, so a rule it beats is one step above R0061;
- in paths' exploration, the four largest pairs of L r1 and of L r2, with their
  newborns' and gateways' conditions;
- the hidden policy and the level 1 catalogue's text;
- `rung2/engine2.py`'s arbitration and `try_edge`, `authorship/loop.py`'s
  installation order, and `corrections/paths.py`'s replay.

**What the drafter had not seen**: the rules above any gateway or their number,
which rule is that door, any other door, any rule's entry or depth, or any
newborn's distance to a gateway.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: WHAT THE ANSWERS DECLARED
--------------------------------------------------------------------------
The first run found few rules above the gateways, through few doors, and every
declared door's edge was the door's own answer. Read by hand, the gateways'
answers had declared wins over the rules their rounds listed, and their losses
had been refused. So this part reads what the answers said, whatever the engine
did with it, as `corrections/fall.py`'s `declared` reads them:
- **the gateways' and the doors' answers**: how many rules each round listed,
  and how many the answer declared its rule above and below, by what the engine
  did with each;
- **every round that listed a gateway**, by what its answer declared of the
  gateway, above or below or nothing, and what the engine did;
- **every round of the run**, by the same counts, beside them.
It was tried on the records in a scratch script before it was written here. It
was written after the six clauses above had been read: D2, D3, D4 and D5 hold,
and D1 and D6 fail. It carries no expectation and moves no clause, and it adds
no gate.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/paths.py`.
The expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m corrections.gateway --dry-run   # gates 1 to 6; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.gateway
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
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import fall as fl
from . import forgotten as fg
from . import paths as pt
from . import plan

F = Fraction
UNLABELLED = fl.UNLABELLED
SEC = fl.SEC
H03 = "H03"

# A rule's entry above the gateways, and how it reached the rule born then.
CONTAINMENT, OWN_WINS, BROUGHT, AT_GATEWAY = "containment", "own_wins", "brought", "at_gateway"
ENTRIES = (CONTAINMENT, OWN_WINS, BROUGHT, AT_GATEWAY)
BY_LOSSES, BY_REGION = "by_losses", "by_region"
# What installed a door's edge into a gateway.
NESTED, GATEWAY_LOSS, DOOR_WIN = "nested", "gateway_loss", "door_win"
DOOR_KINDS = (NESTED, GATEWAY_LOSS, DOOR_WIN)
OTHER = "other"

# The expectation's lines.
D1_SHARE = F(1, 2)
D2_SHARE = F(1, 2)
D3_SHARE = F(1, 2)
D4_SHARE = F(1, 2)
D5_SHARE = F(1, 2)
D6_SHARE = F(1, 2)
D6_RUN = plan.tag(UNLABELLED, 3)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/paths.py. The expectation "
    "in the module's docstring was written and committed before the reading ran. Not a "
    "signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its six clauses were read: what the gateways' and the "
    "doors' answers declared, every round that listed a gateway by what its answer declared "
    "of it, and every answer of the run by the sides it declared. Tried in a scratch script "
    "first. No expectation; no clause moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "gateway.json"


# ---------------------------------------------------------------------------
# The gateways
# ---------------------------------------------------------------------------

def gateways_of(paths_run: dict[str, Any]) -> list[dict[str, Any]]:
    """The rules `paths.json` gives above the run's even crossings, born at a
    ticket of `H03`, of a queue other than `SECURITY_INCIDENT`, in birth order."""
    rules = paths_run["added_after_the_first_run"]["rules_above_even"]
    return sorted((r for r in rules if r["ticket_rule"] == H03 and r["action"] != SEC),
                  key=lambda r: r["born_at"])


# ---------------------------------------------------------------------------
# What reaches the gateways
# ---------------------------------------------------------------------------

def above(engine: PriorityEngine, gates: Sequence[str],
          skip: set[tuple[str, str]] | None = None) -> set[str]:
    """Every rule that reaches one of `gates` by what beats what, the steps in
    `skip` left out, the gates themselves left out."""
    seen: set[str] = set()
    stack = list(gates)
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        for y in engine.beats_me(x):
            if not skip or (y, x) not in skip:
                stack.append(y)
    return seen - set(gates)


def depths(engine: PriorityEngine, gates: Sequence[str]) -> dict[str, int]:
    """The fewest steps from every rule that reaches a gate to one; a gate's is 0."""
    depth = {g: 0 for g in gates}
    level = list(gates)
    while level:
        nxt = []
        for x in level:
            for y in sorted(engine.beats_me(x)):
                if y not in depth:
                    depth[y] = depth[x] + 1
                    nxt.append(y)
        level = nxt
    return depth


def distance(engine: PriorityEngine, src: str, targets: set[str]) -> int | None:
    """The fewest steps from `src` to one of `targets`, or None."""
    if src in targets:
        return 0
    level, seen, dist = [src], {src}, 0
    while level:
        dist += 1
        nxt = []
        for x in level:
            for y in engine.wins_over(x):
                if y in targets:
                    return dist
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        level = nxt
    return None


def entry_of(engine: PriorityEngine, x: str, newborn: str, gates: Sequence[str],
             now: set[str]) -> dict[str, Any]:
    """How `x` came to reach a gateway at the birth of `newborn`, read right after
    that birth. `now` is the rules above the gateways then."""
    hit = set(gates) | now
    if x == newborn:
        if engine.sub_above[x] & hit:
            return {"class": CONTAINMENT}
        if engine.decl_above[x] & hit:
            return {"class": OWN_WINS}
        return {"class": OTHER}
    if newborn not in hit or newborn not in pt.forward(engine, x):
        return {"class": OTHER}
    losses = {(y, newborn) for y in engine.decl_below[newborn]}
    through = BY_REGION if newborn in pt.forward(engine, x, losses) else BY_LOSSES
    return {"class": AT_GATEWAY if newborn in gates else BROUGHT, "through": through,
            "bridge": newborn}


def doors_of(engine: PriorityEngine, gates: Sequence[str], installed_at: dict[tuple[str, str], int],
             born_at: dict[str, int], action: dict[str, str], truth: dict[str, int],
             above_end: set[str]) -> list[dict[str, Any]]:
    """Every edge from a door into a gateway, by what installed it, with the
    policy's verdict, what the door carries above it, and the rules above a
    gateway that reach none once the door's edges into the gateways are out."""
    out = []
    door_ids = sorted({d for g in gates for d in engine.beats_me(g) if d not in gates})
    alone: dict[str, int] = {}
    for d in door_ids:
        skip = {(d, g) for g in gates}
        alone[d] = len(above_end - above(engine, gates, skip))
    for g in gates:
        for d in sorted(engine.beats_me(g)):
            if d in gates:
                continue
            if d in engine.sub_below[g]:
                kind, at = NESTED, None
            else:
                at = installed_at.get((d, g))
                kind = (GATEWAY_LOSS if at is not None and at == born_at[g] else
                        DOOR_WIN if at is not None and at == born_at[d] else OTHER)
            out.append({"door": d, "gateway": g, "action": action[d], "kind": kind,
                        "installed_at": at, "born_at": born_at[d],
                        "verdict": pt.verdict(engine, d, g, action, truth),
                        "carries": len((above(engine, [d]) | {d}) - set(gates)),
                        "alone": alone[d]})
    return out


# ---------------------------------------------------------------------------
# One run, traced
# ---------------------------------------------------------------------------

def trace(record: dict[str, Any], space: Space, truth: dict[str, int], gate_ids: list[str],
          conflicts: dict[int, int], through: dict[tuple[int, str, str], list[str]]
          ) -> dict[str, Any]:
    """The base in birth order. After every birth from the first gateway's, the
    rules above the gateways and each new one's entry. At every birth with
    points lost by a conflict, each refused right side, as `corrections/paths.py`
    traces it, and the newborn of each pair through a gateway, read right after
    its birth. `through` maps such a pair, by birth, newborn and rule, to its
    gateways."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    escs = fg.escalation_at(record)
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    born_at: dict[str, int] = {}
    installed_at: dict[tuple[str, str], int] = {}
    gates: list[str] = []
    prev: set[str] = set()
    entries: dict[str, dict[str, Any]] = {}
    curve: list[list[int]] = []
    pairs: list[dict[str, Any]] = []
    newborn_on_every_edge = True
    grows = True
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        born_at[rid] = idx
        refused: list[str] = []
        for e in by_birth.get(idx, []):
            newborn_on_every_edge &= rid in (e.winner, e.loser)
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            if why == EDGE_OK and not before and e.loser in engine.decl_above[e.winner]:
                installed_at[(e.winner, e.loser)] = idx
            if why == EDGE_CYCLE and e.loser == rid and e.winner not in refused:
                refused.append(e.winner)
        fl.settle(engine, und, action, rid, d["action"])
        if rid in gate_ids:
            gates.append(rid)
        now = above(engine, gates) if gates else set()
        if gates:
            grows &= prev <= now
            for x in sorted(now - prev):
                entries[x] = {**entry_of(engine, x, rid, gates, now), "at": idx}
            curve.append([idx, len(now)])
        prev = now
        c = conflicts.get(idx, 0)
        if not c:
            continue
        depth = None
        for u in refused:
            at = und.get(u, 0) & c
            if not at:
                continue
            pair = {"born_at": idx, "newborn": rid, "rule": u, "points": at.bit_count(),
                    "mask": at}
            gws = through.get((idx, rid, u))
            if gws:
                if depth is None:
                    depth = depths(engine, gates)
                pair.update(read_newborn(engine, rid, gws, gates, now, depth,
                                         fl.declared(d), escs.get(idx) or {}))
            pairs.append(pair)
    return {"engine": engine, "action": action, "born_at": born_at,
            "installed_at": installed_at, "gates": gates, "above": prev,
            "entries": entries, "curve": curve, "pairs": pairs,
            "newborn_on_every_edge": newborn_on_every_edge, "grows": grows}


def read_newborn(engine: PriorityEngine, n: str, gws: list[str], gates: list[str],
                 now: set[str], depth: dict[str, int], said: dict[str, tuple[str, str]],
                 esc: dict[str, Any]) -> dict[str, Any]:
    """A pair's newborn, right after its birth, against the pair's gateways."""
    hit = set(gates) | now
    wins = engine.decl_above[n]
    up = sorted(w for w in wins if w in hit)
    listed = set(esc.get("listed") or [])
    return {"gateways": gws,
            "distance": distance(engine, n, set(gws)),
            "meets": any(engine.ext[n] & engine.ext[g] for g in gws),
            "wins": len(wins), "wins_above": len(up),
            "nearest_win": min((depth[w] for w in up), default=None),
            "contained_above": len(engine.sub_above[n] & hit),
            "said": {g: (list(said[g]) if g in said else None) for g in gws},
            "listed": {g: g in listed for g in gws},
            "above_then": len(now),
            "doors_then": sum(1 for x in now if depth.get(x) == 1)}


# ---------------------------------------------------------------------------
# Added after the first run: what the answers declared
# ---------------------------------------------------------------------------

def sides(rule: dict[str, Any]) -> dict[str, Any]:
    """The rules an answer declared its rule above and below, whatever the
    engine did with each: `corrections/fall.py`'s `declared`, counted, and by
    side and what the engine did."""
    said = list(fl.declared(rule).values())
    return {"wins": sum(1 for side, _ in said if side == "beats"),
            "losses": sum(1 for side, _ in said if side == "loses_to"),
            "by_verdict": dict(sorted(Counter(f"{s}:{w}" for s, w in said).items()))}


def answers(record: dict[str, Any], gws: list[dict[str, Any]],
            doors: list[dict[str, Any]]) -> dict[str, Any]:
    """What the gateways' and the doors' answers declared; every round that
    listed a gateway, by what its answer declared of it and what the engine did;
    and every answer of the run, by the sides it declared."""
    born = erb.births(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)

    def listed(idx: int) -> list[str]:
        return list((escs.get(idx) or {}).get("listed") or [])

    def answer(rid: str) -> dict[str, Any]:
        r = rules[rid]
        return {"rule_id": rid, "action": r["action"], "born_at": r["born_at"],
                "cause": (escs.get(r["born_at"]) or {}).get("kind"),
                "listed": len(listed(r["born_at"])), **sides(r)}

    gate_born = {g["rule_id"]: g["born_at"] for g in gws}
    of_a_gateway: Counter = Counter()
    every: Counter = Counter()
    every_verdict: Counter = Counter()
    for idx in sorted(born):
        r = born[idx]
        s = sides(r)
        said = fl.declared(r)
        shown = set(listed(idx))
        if shown:
            every["rounds"] += 1
            every["wins"] += s["wins"]
            every["losses"] += s["losses"]
            every["without_a_loss"] += s["losses"] == 0
            every_verdict.update(s["by_verdict"])
        for g, b in gate_born.items():
            if idx > b and g in shown:
                side, why = said.get(g, ("none", "none"))
                of_a_gateway[f"{side}:{why}"] += 1
    return {"gateways": [answer(g["rule_id"]) for g in gws],
            "doors": [answer(d) for d in sorted({x["door"] for x in doors},
                                                key=lambda d: (rules[d]["born_at"], d))],
            "rounds_that_listed_a_gateway": dict(sorted(of_a_gateway.items())),
            "every_round": {**{k: every.get(k, 0)
                               for k in ("rounds", "wins", "losses", "without_a_loss")},
                            "by_verdict": dict(sorted(every_verdict.items()))}}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def through_a_gateway(paths_run: dict[str, Any], gate_ids: set[str]
                      ) -> dict[tuple[int, str, str], list[str]]:
    """`paths.json`'s pairs that the even crossings cut, among which one runs from
    a gateway, each with the gateways of its even crossings."""
    out = {}
    for p in paths_run["pairs"]:
        if not p["even_cut"]:
            continue
        gws = sorted({c["upper"] for c in p["crossings"]
                      if c["verdict"] == pt.EVEN and c["upper"] in gate_ids})
        if gws:
            out[(p["born_at"], p["newborn"], p["rule"])] = gws
    return out


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int], cases: Sequence,
             paths_run: dict[str, Any], final: PriorityEngine | None = None) -> dict[str, Any]:
    """One run's rules above its gateways, their entries, the doors, the pairs
    through a gateway, and the gates. `paths_run` is the run's entry in
    `paths.json`. `final` is the run's final base,
    `manual.instrument.final_engine`'s by default."""
    final = final if final is not None else MI.final_engine(record)
    gws = gateways_of(paths_run)
    gate_ids = [g["rule_id"] for g in gws]
    conflicts = pt.last_conflicts(record, space, truth, cases)
    through = through_a_gateway(paths_run, set(gate_ids))
    got = trace(record, space, truth, gate_ids, conflicts, through)
    engine, action, born_at = got["engine"], got["action"], got["born_at"]
    gates, above_end, entries = got["gates"], got["above"], got["entries"]
    rules = {r["rule_id"]: r for r in record["rules"]}
    rows = {r["idx"]: r for r in record["records"]}
    escs = fg.escalation_at(record)
    keyword = fl.keyword(space)
    first = born_at[gates[0]] if gates else None
    after = [r.rule_id for r in engine.rules if first is not None and born_at[r.rule_id] > first]
    depth = depths(engine, gates) if gates else {}
    doors = doors_of(engine, gates, got["installed_at"], born_at, action, truth, above_end)
    via = [p for p in got["pairs"] if "gateways" in p]

    def weigh(key, ps) -> dict[str, int]:
        c: Counter = Counter()
        for p in ps:
            c[key(p)] += p["points"]
        return dict(c)

    newborns: dict[tuple[int, str], dict[str, Any]] = {}
    for p in via:
        k = (p["born_at"], p["newborn"])
        nb = newborns.setdefault(k, {"born_at": p["born_at"], "newborn": p["newborn"],
                                     "action": action[p["newborn"]], "pairs": 0,
                                     "pair_points": 0, "mask": 0,
                                     **{f: p[f] for f in ("gateways", "distance", "meets",
                                                          "wins", "wins_above", "nearest_win",
                                                          "contained_above", "said", "listed",
                                                          "above_then", "doors_then")}})
        nb["pairs"] += 1
        nb["pair_points"] += p["points"]
        nb["mask"] |= p["mask"]
        nb["gateways"] = sorted(set(nb["gateways"]) | set(p["gateways"]))
    for nb in newborns.values():
        nb["points"] = nb.pop("mask").bit_count()
        nb["cause"] = (escs.get(nb["born_at"]) or {}).get("kind")
        nb["conditions"] = rules[nb["newborn"]]["conditions"]

    bridges: dict[str, dict[str, Any]] = {}
    for x, e in entries.items():
        if e["class"] in (BROUGHT, AT_GATEWAY):
            b = bridges.setdefault(e["bridge"], {
                "bridge": e["bridge"], "action": action[e["bridge"]],
                "born_at": born_at[e["bridge"]],
                "cause": (escs.get(born_at[e["bridge"]]) or {}).get("kind"),
                "entry": (entries.get(e["bridge"]) or {}).get("class"),
                "brought": 0, BY_LOSSES: 0, BY_REGION: 0})
            b["brought"] += 1
            b[e["through"]] += 1
    traced = [(p["born_at"], p["newborn"], p["rule"], p["points"]) for p in got["pairs"]]
    recorded = [(p["born_at"], p["newborn"], p["rule"], p["points"]) for p in paths_run["pairs"]]
    summary = {
        "gateways": gate_ids,
        "first_gateway_born_at": first,
        "rules": len(engine.rules),
        "born_after": len(after),
        "above": len(above_end),
        "above_born_after": sum(1 for x in after if x in above_end),
        "above_by_queue": dict(Counter(action[x] for x in above_end)),
        "born_after_by_queue": dict(Counter(action[x] for x in after)),
        "entries": {k: sum(1 for e in entries.values() if e["class"] == k) for k in ENTRIES},
        "through": dict(Counter(f"{e['class']}:{e['through']}" for e in entries.values()
                                if "through" in e)),
        "depth": {str(k): v for k, v in sorted(Counter(depth[x] for x in above_end
                                                       if x in depth).items())},
        "doors": {"rules": len({d["door"] for d in doors}),
                  "edges": {k: sum(1 for d in doors if d["kind"] == k) for k in DOOR_KINDS},
                  "verdicts": dict(Counter(f"{d['kind']}:{d['verdict']}" for d in doors))},
        "pairs": {"pairs": len(via), "points": sum(p["points"] for p in via),
                  "meets": sum(p["points"] for p in via if p["meets"]),
                  "misses": sum(p["points"] for p in via if not p["meets"]),
                  "distance": {str(k): v for k, v in sorted(
                      weigh(lambda p: p["distance"], via).items(),
                      key=lambda kv: (kv[0] is None, kv[0]))}},
        "newborns": len(newborns),
    }
    gates_out = [
        {"gate": 1, "what": "the replay is the base",
         "passes": ch_lost.same_base(final, engine)},
        {"gate": 2, "what": "the gateways and the pairs are paths.json's",
         "passes": traced == recorded
                   and all(g["rule_id"] in engine.ext
                           and rules[g["rule_id"]]["conditions"] == g["conditions"]
                           and rules[g["rule_id"]]["born_at"] == g["born_at"]
                           and engine.ext[g["rule_id"]] & ~keyword == 0 for g in gws)},
        {"gate": 3, "what": "every edge a birth tries has the rule born there on one side",
         "passes": got["newborn_on_every_edge"]},
        {"gate": 4, "what": "the rules above the gateways only grow",
         "passes": got["grows"]},
        {"gate": 5, "what": "every newborn of a pair through a gateway reaches one of its "
                            "gateways, at a distance no shorter than paths.json's path",
         "passes": all(p["distance"] is not None
                       and p["distance"] + 1 >= rec["shortest"]
                       for p, rec in zip(got["pairs"], paths_run["pairs"])
                       if "gateways" in p)},
        {"gate": 6, "what": "every rule above a gateway is classed once, at a depth of at "
                            "least one, and every door's edge is classed",
         "passes": set(entries) == above_end
                   and all(e["class"] in ENTRIES for e in entries.values())
                   and all(depth.get(x, 0) >= 1 for x in above_end)
                   and all(d["kind"] in DOOR_KINDS for d in doors)},
    ]
    keep_entry = ("class", "through", "bridge", "at")
    return {
        "summary": summary,
        "gateways": [{**g, "cause": (escs.get(g["born_at"]) or {}).get("kind"),
                      "ticket_rule": (rows.get(g["born_at"]) or {}).get("truth_rule")}
                     for g in gws],
        "curve": got["curve"],
        "entries": {x: {k: e[k] for k in keep_entry if k in e}
                    for x, e in sorted(entries.items(), key=lambda kv: (born_at[kv[0]], kv[0]))},
        "bridges": sorted(bridges.values(), key=lambda b: (-b["brought"], b["born_at"])),
        "doors": doors,
        "newborns": sorted(newborns.values(), key=lambda nb: (-nb["pair_points"], nb["born_at"])),
        "gates": gates_out,
        "added_after_the_first_run": {"answers": answers(record, gws, doors)},
    }


def read_all_runs(records: dict[str, dict], paths_record: dict[str, Any], space: Space,
                  truth: dict[str, int], cases: Sequence,
                  finals: dict[str, PriorityEngine] | None = None) -> dict[str, dict]:
    finals = finals or {}
    return {tag: read_run(rec, space, truth, cases, paths_record["runs"][tag],
                          final=finals.get(tag))
            for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    L = [runs[plan.tag(plan.LABELLED, k)]["summary"] for k in range(1, plan.REPS + 1)
         if plan.tag(plan.LABELLED, k) in runs]
    after = sum(s["born_after"] for s in L)
    above_after = sum(s["above_born_after"] for s in L)
    above_all = sum(s["above"] for s in L)
    own = sum(s["entries"][OWN_WINS] for s in L)
    deep = sum(v for s in L for k, v in s["depth"].items() if int(k) >= 2)
    declared = sum(s["doors"]["edges"][GATEWAY_LOSS] + s["doors"]["edges"][DOOR_WIN] for s in L)
    door_win = sum(s["doors"]["edges"][DOOR_WIN] for s in L)
    pts = sum(s["pairs"]["points"] for s in L)
    misses = sum(s["pairs"]["misses"] for s in L)
    n3 = runs.get(D6_RUN, {}).get("summary")
    n3_after = n3["born_after"] if n3 else 0
    n3_above = n3["above_born_after"] if n3 else 0
    return [
        {"clause": "D1", "what": "of the rules born after their run's first gateway, at least "
                                 "half are above a gateway at the run's end",
         "reading": {"above": above_after, "of": after, "share": frac(share(above_after, after))},
         "holds": after > 0 and F(above_after, after) >= D1_SHARE},
        {"clause": "D2", "what": "of the rules above a gateway at the end, at least half "
                                 "entered own_wins",
         "reading": {"own_wins": own, "of": above_all, "share": frac(share(own, above_all))},
         "holds": above_all > 0 and F(own, above_all) >= D2_SHARE},
        {"clause": "D3", "what": "of the rules above a gateway at the end, at least half are "
                                 "at a depth of two or more",
         "reading": {"deep": deep, "of": above_all, "share": frac(share(deep, above_all))},
         "holds": above_all > 0 and F(deep, above_all) >= D3_SHARE},
        {"clause": "D4", "what": "of the declared edges from a door into a gateway at the end, "
                                 "at least half are door_win",
         "reading": {"door_win": door_win, "of": declared,
                     "share": frac(share(door_win, declared))},
         "holds": declared > 0 and F(door_win, declared) >= D4_SHARE},
        {"clause": "D5", "what": "at least half of the points of the pairs through a gateway "
                                 "are in pairs whose newborn shares no point with any of the "
                                 "pair's gateways",
         "reading": {"misses": misses, "of": pts, "share": frac(share(misses, pts))},
         "holds": pts > 0 and F(misses, pts) >= D5_SHARE},
        {"clause": "D6", "what": "in N r3, of the rules born after its gateway, at least half "
                                 "are above it at the run's end",
         "reading": {"above": n3_above, "of": n3_after, "share": frac(share(n3_above, n3_after))},
         "holds": n3_after > 0 and F(n3_above, n3_after) >= D6_SHARE},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return records, json.loads(pt.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why so many rules sit above the gateway "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 6 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/gateway.py writes {record_path()}")
    records, paths_record = read_all()
    runs = read_all_runs(records, paths_record, MI.space(), MI.space_truth(),
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
        "source": {"paths": str(pt.record_path()),
                   "paths_from": paths_record["_env"].get("git_commit")},
        "surface": "the rules above each run's gateways over the whole base, as it is replayed "
                   "in birth order; the pairs through a gateway as paths.json reads them",
        "constants": {"D1_SHARE": str(D1_SHARE), "D2_SHARE": str(D2_SHARE),
                      "D3_SHARE": str(D3_SHARE), "D4_SHARE": str(D4_SHARE),
                      "D5_SHARE": str(D5_SHARE), "D6_SHARE": str(D6_SHARE),
                      "D6_RUN": D6_RUN},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: gateways {s['gateways']}; {s['above']} rules above, "
              f"{s['above_born_after']} of the {s['born_after']} born after the first; "
              f"entries {s['entries']}; depth {s['depth']}; doors {s['doors']['edges']}; "
              f"pairs {s['pairs']['points']} points, {s['pairs']['misses']} missing")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
