"""
WHICH EDGE OF A CYCLE SHOULD YIELD. Rung 2's engine refuses a declaration that
would close a cycle, so the edges it already holds stand and the new one yields.
`blind/closure.py` read the order those refusals kept, and in run 1 of
`PLAN_BLIND.md` it is the wrong one: wherever a side in contention is right on
the CONFLICT points they left, it is almost always the declaration the engine
refused. Subsumption does not yield. So letting the new declaration stand means
dropping an older declared edge of the cycle, which changes the order where that
edge's two rules meet. This reads whether the trade gains, and against what.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Which edge yields is a priority over the declarations. The engine installs them
in turn and refuses each that would close a cycle with subsumption and the edges
it kept; whatever it refuses, the pair is already ordered the other way. The
engine's priority is arrival, so in every cycle the newest edge yields. Read
newest first, the oldest yields. Every priority keeps an acyclic graph into which
no declaration it refused fits, and subsumption, which is the semantics, is in
every one.

**The trajectory is held fixed.** Each run's final rules and every declaration
it made are read as they are, and only which declarations the engine keeps
changes. Under another priority the loop would have decided other cases, been
asked other questions and written other rules; none of that is free to read.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
The final base of each of the twelve paid runs of rung 2's loop at n=2000, three
per protocol, as `blind/closure.py` reads them: v1, v1e, v2e and v2b. Every
entry of each run's edge log is attributed to the escalation that wrote it,
through the verdicts each case's record carries. The arms order the declarations
the engine accepted or refused for closing a cycle, on either channel; those it
refused for anything else stay refused in every arm. Five priorities:

  arrival   the order the declarations were made: the engine as it is. The
            newest edge of a cycle yields.
  recency   the newest escalation's declarations first, those of one escalation
            in the order the engine installs them. The oldest edge yields.
  coin      a shuffle, `N_COIN` draws seeded by `YIELD_SEED`, the base and the
            draw. A random edge yields.
  ranking   first the declarations whose winner's queue rung 3's Stage C
            hierarchy ranks above the loser's, then those within one queue, then
            those against it, each group in arrival order. An edge against the
            ranking yields first.
  oracle    first the declarations whose winner is the better rule over the
            pair's shared region of the space, then ties and pairs neither rule
            is ever right on there, then those whose winner is the worse, each
            group in arrival order. It reads the truth: what the truth's
            direction would keep. It is not the best selection, which
            `FINDINGS3.md` §17 found to be another object.

Each arm's graph is read by two engines: rung 2's, which defeats a rule only with
a matching rule that beats it directly, and `blind/closure.py`'s, which defeats
it with any matching rule that reaches it. **Under rung 2's engine a count of
right decisions rewards resolving**, the lesson of `W-c` and `K-d`: an arm that
lets a refused declaration stand also resolves the CONFLICT the refusal left,
where the pair was ordered only through a rule that does not match there.
**Through the closure every declared pair is ordered in every arm**, since a
declaration is refused only when its pair is already ordered the other way.
There the arms differ in direction, and in what they resolve only where a pair
nobody declared is ordered through the edges one arm kept and another did not.

For each base, arm and engine, over the exhaustive space, uniform over its
134,400 points, and over the 2,000 corpus cases, counted as they arrive:

  right        the points decided, to the true queue.
  wrong        those decided to another queue: the silent error.
  conflict     those left in CONFLICT.
  gained, lost against the arrival arm on the same engine: right here and not
               there, and the converse.
  resolved     the points the arrival arm leaves in CONFLICT that the arm
               decides, rightly and wrongly.
  unresolved   the points the arrival arm decides that the arm leaves in
               CONFLICT, and whether the arrival arm was right there.
  flipped      the points both decide, to different queues: the arm right, the
               arrival arm right, or neither.

And the declarations each arm refused: the edges that yielded. For the coin,
each count's mean, deviation and central 90% over the draws, and the share of
draws right on at least as many points as each arm. Pooled over the bases with a
refusal for a cycle, beside each base's own reading. A base with none reads the
same under every arm, which gate 4 checks; it is named, and nothing else is read.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The log is the escalations'.** Every entry of each edge log is the next
     engine verdict its case's record carries, in order, and the whole log is
     used.
  2. **The arrival arm is the engine.** In the order made, every declaration it
     orders gets back the verdict the record logged, and its graph is the one
     `authorship.gates.rebuild_final` rebuilds.
  3. **The arrival arm is `closure.json`'s.** For every base, under both engines
     and on both surfaces, its right points and its CONFLICT points are the
     counts `closure.json` publishes.
  4. **Without a cycle the arms are one.** In every base with no refusal for a
     cycle, every arm and the coin's first draw keep the arrival arm's edges.
  5. **Every arm is acyclic and full.** No rule reaches itself in any arm's
     graph, the coin's draws included, and every declaration an arm refused
     would close a cycle in it.
  6. **The coin is a function of its seed.** Each base's first draw, drawn
     twice, refuses the same declarations.
  7. **STOP 0.** The hidden policy's engine, its edges installed in reverse and
     in a shuffle, keeps every edge and decides the whole space right under both
     engines.
  8. **The truth is the records'.** On every corpus case the truth masks give
     the label every base's record carries.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause is read over the space. "Pooled" is over the bases with a refusal
for a cycle: v2e's run 1 and v2b's runs 1 and 3.

  1. **As the engine is, the trade buys right decisions with silent errors.** In
     v2b's run 1, under rung 2's engine, the recency arm is right on more points
     than the arrival arm, and wrong on more.
  2. **Through the closure the trade gains on the pool, and not in every base.**
     Pooled, the recency arm is right on more points than the arrival arm. In
     v2e's run 1 and in v2b's run 3 it is right on fewer.
  3. **Age chooses as a coin does.** Pooled, through the closure, the arrival
     arm's and the recency arm's right points both lie inside the central 90% of
     the coin's draws.
  4. **The ranking chooses better than age.** Pooled, through the closure, the
     ranking arm is right on more points than the recency arm and than the
     arrival arm.
  5. **The truth's direction chooses better still.** Pooled, through the
     closure, the oracle arm is right on more points than every other arm and
     than the coin's mean.

**What the drafter had seen**:
  - `FINDINGS_BLIND.md`, `score.json`, `readings.json`, `cycles.json` and
    `closure.json`. Among them, `closure.json`'s counts on the CONFLICT points
    the arrival arm leaves over the space. In v2b's run 1, 1,825 points: the
    order the refusals kept is right on 10, the refused declarations' side on
    535, neither on 1,280, and the Stage C ranking on 520. In v2b's run 3, 60
    points: 60, 0, 0 and 0. In v2e's run 1, 1,580 points: 950, 630, 0 and 950.
    And the same counts on the corpus.
  - `cycles.json`'s path for every refusal of v2b's runs 1 and 3, the queues
    and birth cases of the rules on them, and run 1's order-channel log: which
    pairs the order answers declared, in which direction and in what sequence.
  - Each run's edge verdicts by channel: refusals for a cycle in v2e's run 1
    (2), v2b's run 1 (32) and v2b's run 3 (3), and none in the other nine. And
    that each case's `edge_reasons` give back its log's verdicts in order, less
    the `fuera_del_vecindario` the engine never logs.
  - The Stage C hierarchy, the engine's code, and `FINDINGS3.md` §§13-14 and
    §§16-17, which read arrival order against random orders on the pairwise
    answers.
  - The gates, run before this commit, which print pass or fail.

**Not seen**: the paths of v2e's run 1, the graph of any arm but arrival, which
edges yield in any other arm, any decision but the arrival arm's, and any truth
where a yielding edge's two rules meet.

**What is close to known, and what is bet.** An arm that lets a refused
declaration stand decides that declaration's CONFLICT points for its side. On
those points the recency arm reads near `closure.json`'s refused side and the
ranking arm near its ranking: pooled through the closure, about 1,165 of them
right for recency against 1,020 for arrival and 1,470 for the ranking. On those
points alone the first clause, the second and the fourth follow. What none of it
says is what the yielding edges cost where their two rules meet. Every clause but
the third bets that this cost does not overturn the split, and the fifth bets
too that the truth's direction over each pair's whole shared region points where
it points on the CONFLICT points. **The third is the bet on the question**: that
age, either way, chooses which edge yields no better than a draw.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_BLIND.md`'s verdicts existed and after
`blind/closure.py` read the order the refusals kept, with the expectation above
written before the reading and committed before it ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. No verdict moves. Zero API
calls.

Usage:  PYTHONHASHSEED=0 python3 -m blind.yielding
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from authorship import gates as egates
from reuse import structure as st
from rung2.engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK,
                           EDGE_SELF, EDGE_UNKNOWN, PriorityEngine, Space)
from rung2.hidden_priority import build_hidden_engine
from rung3.edge_direction import better_over_space, verdict
from rung3.order_search_ls import space_truth_masks
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from . import closure, plan, rows
from .cycles import fork

READ_PATH = plan.OUT / "yielding.json"
ARMS = ("arrival", "recency", "ranking", "oracle")
ENGINES = ("direct", "closure")
SURFACES = ("space", "corpus")
N_COIN = 200                       # draws per base, fixed before the reading
YIELD_SEED = 17
CENTRAL = 0.90                     # clause 3
GAINS = ("v2b", 1)                 # clause 1, and the base clause 2 expects to gain
FEWER = (("v2e", 1), ("v2b", 3))   # clause 2: the bases it expects to lose
VERDICTS = (EDGE_OK, EDGE_UNKNOWN, EDGE_DISJOINT, EDGE_SELF, EDGE_CONTRADICTS,
            EDGE_CYCLE)            # what the engine logs; the loop records more
ORDERED = (EDGE_OK, EDGE_CYCLE)    # the declarations the arms order
COUNTS = ("right", "wrong", "conflict", "gained", "lost", "resolved_right",
          "resolved_wrong", "unresolved_was_right", "unresolved_was_wrong",
          "flipped_arm_right", "flipped_arrival_right", "flipped_neither")
DRAWN = ("right", "wrong", "conflict", "gained", "lost")
PROVENANCE = (
    "POST-RUN: asked for after PLAN_BLIND.md's verdicts existed and after "
    "blind/closure.py read the order the refusals kept. The expectation in the "
    "module's docstring was written before the reading and committed before it "
    "ran. Not a signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# The declarations, by escalation
# ---------------------------------------------------------------------------

def attribute(record: dict) -> tuple[list[dict], bool]:
    """Every entry of the edge log, with the case of the escalation that wrote
    it. Each case's record carries its escalation's verdicts in order, and the
    engine logs exactly the engine's. Returns the entries, and whether the whole
    log was given back that way."""
    log = record.get("edge_log") or []
    chans = rows.channels_of(record)
    out: list[dict] = []
    for rec in record["records"]:
        for why in rec.get("edge_reasons") or []:
            if why not in VERDICTS:
                continue
            k = len(out)
            if k >= len(log) or log[k][2] != why:
                return out, False
            w, l, _ = log[k]
            out.append({"k": k, "case": rec["idx"], "winner": w, "loser": l,
                        "verdict": why, "channel": chans[k]})
    return out, len(out) == len(log)


def ordered(decls: list[dict]) -> list[dict]:
    """The declarations the arms order: accepted, or refused for a cycle."""
    return [d for d in decls if d["verdict"] in ORDERED]


def priority(arm: str, decls: list[dict], action: dict[str, str], ext: dict[str, int],
             tmask: dict[str, int], rng: random.Random | None = None) -> list[dict]:
    """The declarations in the order an arm installs them."""
    ds = sorted(ordered(decls), key=lambda d: d["k"])
    if arm == "arrival":
        return ds
    if arm == "recency":
        return sorted(ds, key=lambda d: (-d["case"], d["k"]))
    if arm == "coin":
        rng.shuffle(ds)
        return ds
    if arm == "ranking":
        rank = {q: i for i, q in enumerate(STAGE_C_HIERARCHY)}

        def group(d):
            a, b = rank[action[d["winner"]]], rank[action[d["loser"]]]
            return 0 if a < b else 1 if a == b else 2
    elif arm == "oracle":
        def group(d):
            v = verdict(*better_over_space(d["winner"], d["loser"], ext, action, tmask))
            return 0 if v == rows.HIT else 2 if v == rows.MISS else 1
    else:
        raise ValueError(arm)
    return sorted(ds, key=lambda d: (group(d), d["k"]))


def coin_order(decls: list[dict], key: tuple[str, int], draw: int) -> list[dict]:
    rng = random.Random(f"{YIELD_SEED}/{key[0]}/{key[1]}/{draw}")
    return priority("coin", decls, {}, {}, {}, rng)


def install(bare: PriorityEngine, order: list[dict]) -> tuple[PriorityEngine, list[dict]]:
    """The base's rules with the declarations installed in `order` through
    `try_edge`. Returns the engine and the declarations it refused: every one
    for closing a cycle, since the arms order only those that can be."""
    engine = fork(bare)
    refused = []
    for d in order:
        why = engine.try_edge(d["winner"], d["loser"])
        if why == EDGE_CYCLE:
            refused.append(d)
        elif why != EDGE_OK:
            raise AssertionError(f"{d['winner']} over {d['loser']}: {why}")
    return engine, refused


def edges_of(engine: PriorityEngine) -> set[tuple[str, str]]:
    return {(w, l) for w, ls in engine.decl_above.items() for l in ls}


def acyclic_and_full(engine: PriorityEngine, refused: list[dict]) -> bool:
    """No rule reaches itself, and every refused declaration would close a
    cycle: its loser reaches its winner."""
    anc = closure.ancestors(engine)
    return (all(r.rule_id not in anc[r.rule_id] for r in engine.rules)
            and all(engine._reaches(d["loser"], d["winner"]) for d in refused))


# ---------------------------------------------------------------------------
# What an arm decides, against the arrival arm
# ---------------------------------------------------------------------------

def masks(engine: PriorityEngine, tmask: dict[str, int]) -> dict[str, dict[str, Any]]:
    """For each engine, the points decided right, decided wrong and left in
    CONFLICT, with the undefeated rules' masks by queue."""
    out = {}
    for name, queues in closure.engines(engine).items():
        one, two = closure.cover(queues)
        decided = one & ~two
        right = 0
        for a, m in queues.items():
            right |= m & decided & tmask.get(a, 0)
        out[name] = {"right": right, "wrong": decided & ~right, "conflict": two,
                     "queues": queues}
    return out


def multiplicity(bits: list[int]) -> dict[int, int]:
    """The corpus as masks: `out[k]` is the points it touches exactly k times."""
    count: dict[int, int] = {}
    for b in bits:
        count[b] = count.get(b, 0) + 1
    out: dict[int, int] = {}
    for b, k in count.items():
        out[k] = out.get(k, 0) | b
    return out


def weigh(mask: int, mult: dict[int, int] | None) -> int:
    """Points of `mask` over the space, or corpus cases on them as they arrive."""
    if mult is None:
        return mask.bit_count()
    return sum(k * (mask & m).bit_count() for k, m in mult.items())


def against(x: dict[str, Any], a: dict[str, Any], mult: dict[int, int] | None
            ) -> dict[str, int]:
    """An arm's counts under one engine, and what changes from the arrival arm's."""
    x_dec, a_dec = x["right"] | x["wrong"], a["right"] | a["wrong"]
    resolved = x_dec & a["conflict"]
    unresolved = a_dec & x["conflict"]
    same = 0
    for q, m in x["queues"].items():
        same |= m & a["queues"].get(q, 0)
    flipped = x_dec & a_dec & ~same

    def w(mask: int) -> int:
        return weigh(mask, mult)

    return {"right": w(x["right"]), "wrong": w(x["wrong"]), "conflict": w(x["conflict"]),
            "gained": w(x["right"] & ~a["right"]), "lost": w(a["right"] & ~x["right"]),
            "resolved_right": w(resolved & x["right"]),
            "resolved_wrong": w(resolved & x["wrong"]),
            "unresolved_was_right": w(unresolved & a["right"]),
            "unresolved_was_wrong": w(unresolved & a["wrong"]),
            "flipped_arm_right": w(flipped & x["right"]),
            "flipped_arrival_right": w(flipped & a["right"]),
            "flipped_neither": w(flipped & x["wrong"] & a["wrong"])}


def reading(m: dict, arrival: dict, mult: dict[int, int]) -> dict[str, dict]:
    return {e: {"space": against(m[e], arrival[e], None),
                "corpus": against(m[e], arrival[e], mult)} for e in ENGINES}


def brief(d: dict) -> dict:
    return {k: d[k] for k in ("k", "case", "winner", "loser", "channel", "verdict")}


# ---------------------------------------------------------------------------
# The coin
# ---------------------------------------------------------------------------

def central(xs: list[float]) -> list[float]:
    s = sorted(xs)
    return [s[round(len(s) * (1 - CENTRAL) / 2)], s[round(len(s) * (1 + CENTRAL) / 2) - 1]]


def summary(draws: list[dict], arms: dict[str, dict]) -> dict[str, Any]:
    """Each drawn count's mean, deviation and central 90%, per engine and surface,
    and the share of draws right on at least as many points as each arm."""
    out: dict[str, Any] = {"draws": len(draws)}
    for e in ENGINES:
        out[e] = {}
        for s in SURFACES:
            out[e][s] = {}
            for key in DRAWN:
                xs = [d[e][s][key] for d in draws]
                out[e][s][key] = {"mean": statistics.mean(xs), "sd": statistics.pstdev(xs),
                                  "central": central(xs)}
            xs = [d[e][s]["right"] for d in draws]
            out[e][s]["at_least"] = {a: sum(x >= arms[a][e][s]["right"] for x in xs) / len(xs)
                                     for a in arms}
    return out


# ---------------------------------------------------------------------------
# One base
# ---------------------------------------------------------------------------

def read_base(key: tuple[str, int], record: dict, space: Space, tmask: dict[str, int],
              mult: dict[int, int]) -> dict[str, Any]:
    decls, attributed = attribute(record)
    bare, _ = egates.rebuild_final(record, space, set())
    action = {r.rule_id: r.action for r in bare.rules}
    cycle = any(d["verdict"] == EDGE_CYCLE for d in decls)
    graphs = {a: install(bare, priority(a, decls, action, bare.ext, tmask)) for a in ARMS}
    m = {a: masks(g[0], tmask) for a, g in graphs.items()}
    arms = {a: reading(m[a], m["arrival"], mult) for a in ARMS}

    logged, _ = egates.rebuild_final(record, space)
    arrival_eng, arrival_refused = graphs["arrival"]
    refused_logged = sorted(d["k"] for d in ordered(decls) if d["verdict"] == EDGE_CYCLE)
    full = all(acyclic_and_full(*g) for g in graphs.values())
    first = [coin_order(decls, key, 0), coin_order(decls, key, 0)]
    seeded = ([d["k"] for d in install(bare, first[0])[1]]
              == [d["k"] for d in install(bare, first[1])[1]])
    one = all(edges_of(g[0]) == edges_of(arrival_eng) for g in graphs.values())
    one = one and edges_of(install(bare, first[0])[0]) == edges_of(arrival_eng)

    out: dict[str, Any] = {
        "rules": len(bare.rules),
        "declarations": {"logged": len(decls), "ordered": len(ordered(decls)),
                         "refused_for_a_cycle": len(refused_logged)},
        "cycle": cycle,
        "arms": {a: {"kept": len(edges_of(g[0])),
                     "refused": [brief(d) for d in g[1]],
                     **arms[a]} for a, g in graphs.items()},
    }
    if cycle:
        draws, refusals = [], []
        for k in range(N_COIN):
            eng, refused = install(bare, coin_order(decls, key, k))
            full = full and acyclic_and_full(eng, refused)
            draws.append(reading(masks(eng, tmask), m["arrival"], mult))
            refusals.append(len(refused))
        out["coin"] = summary(draws, arms) | {"refused_mean": statistics.mean(refusals)}
        out["_draws"] = draws
    out["gates"] = {
        "attributed": attributed,
        "arrival_is_the_engine": ([d["k"] for d in arrival_refused] == refused_logged
                                  and edges_of(arrival_eng) == edges_of(logged)),
        "arms_are_one": None if cycle else one,
        "acyclic_and_full": full,
        "coin_seeded": seeded,
    }
    return out


def pooled(bases: dict) -> dict[str, Any]:
    """The deterministic arms' counts summed over the bases with a cycle, and the
    coin's draws summed draw by draw."""
    keys = [k for k, b in bases.items() if b["cycle"]]
    arms = {a: {e: {s: {c: sum(bases[k]["arms"][a][e][s][c] for k in keys) for c in COUNTS}
                    for s in SURFACES} for e in ENGINES} for a in ARMS}
    draws = [{e: {s: {c: sum(bases[k]["_draws"][i][e][s][c] for k in keys) for c in DRAWN}
                  for s in SURFACES} for e in ENGINES} for i in range(N_COIN)]
    return {"bases": [f"{p} {r}" for p, r in keys], "arms": arms,
            "coin": summary(draws, arms),
            "coin_right_by_draw": {e: [d[e]["space"]["right"] for d in draws]
                                   for e in ENGINES}}


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def stop_zero(space: Space, tmask: dict[str, int]) -> dict[str, Any]:
    """The hidden policy's edges, installed in reverse and in a shuffle on its
    rules alone: every one kept, and the whole space right under both engines."""
    hidden, _, _ = build_hidden_engine(space)
    bare = PriorityEngine(space=space)
    for r in hidden.rules:
        bare.add(r, born_at=r.born_at, keep_id=True)
    edges = sorted(edges_of(hidden))
    shuffled = list(edges)
    random.Random(f"{YIELD_SEED}/hidden").shuffle(shuffled)
    out = {}
    for name, order in (("reversed", edges[::-1]), ("shuffled", shuffled)):
        eng, refused = install(bare, [{"winner": w, "loser": l} for w, l in order])
        right = {e: m["right"].bit_count() for e, m in masks(eng, tmask).items()}
        out[name] = {"edges": len(edges), "refused": len(refused), "right": right,
                     "passes": not refused and edges_of(eng) == edges_of(hidden)
                     and all(x == space.n for x in right.values())}
    return out


def check(bases: dict, records: dict, published: dict, stop: dict, tmask: dict[str, int],
          bits: list[int]) -> list[dict]:
    out = []
    truth_at = [next(a for a, m in tmask.items() if m & bit) for bit in bits]
    for (protocol, rep), b in bases.items():
        name, g = f"{protocol} {rep}", b["gates"]
        pub = published["bases"][name]
        same = True
        for s in SURFACES:
            c = pub[s]["counts"]
            d, cl = b["arms"]["arrival"]["direct"][s], b["arms"]["arrival"]["closure"][s]
            same = same and (d["right"], d["conflict"], cl["right"], cl["conflict"]) == (
                c["direct_correct"], c["conflicts"], c["closure_correct"],
                c["conflicts"] - c["resolved"])
        labels = [t for t, _ in egates.labels_of(records[(protocol, rep)])]
        out += [
            {"gate": 1, "base": name, "what": "the log is the escalations'",
             "passes": g["attributed"]},
            {"gate": 2, "base": name, "what": "the arrival arm is the engine",
             "passes": g["arrival_is_the_engine"]},
            {"gate": 3, "base": name, "what": "the arrival arm is closure.json's",
             "passes": same},
            {"gate": 4, "base": name, "what": "without a cycle the arms are one",
             "passes": True if g["arms_are_one"] is None else g["arms_are_one"]},
            {"gate": 5, "base": name, "what": "every arm is acyclic and full",
             "passes": g["acyclic_and_full"]},
            {"gate": 6, "base": name, "what": "the coin is a function of its seed",
             "passes": g["coin_seeded"]},
            {"gate": 8, "base": name, "what": "the truth is the records'",
             "passes": labels == truth_at},
        ]
    out.append({"gate": 7, "base": "the hidden policy", "what": "STOP 0 under every order",
                "measured": stop, "passes": all(x["passes"] for x in stop.values())})
    return out


def read_expectation(bases: dict, pool: dict) -> list[dict]:
    def right(source, arm, engine="closure"):
        return source[arm][engine]["space"]["right"]

    g = bases[GAINS]["arms"]
    d_right = right(g, "recency", "direct") - right(g, "arrival", "direct")
    d_wrong = g["recency"]["direct"]["space"]["wrong"] - g["arrival"]["direct"]["space"]["wrong"]
    arms = pool["arms"]
    gain = right(arms, "recency") - right(arms, "arrival")
    fewer = {f"{p} {r}": right(bases[(p, r)]["arms"], "recency")
             - right(bases[(p, r)]["arms"], "arrival") for p, r in FEWER}
    coin = pool["coin"]["closure"]["space"]["right"]
    lo, hi = coin["central"]
    ages = {a: right(arms, a) for a in ("arrival", "recency")}
    others = {a: right(arms, a) for a in ("arrival", "recency", "ranking")}
    return [
        {"clause": 1, "what": "in v2b's run 1, under rung 2's engine, recency is right on "
                              "more points than arrival, and wrong on more",
         "reading": {"right": d_right, "wrong": d_wrong},
         "holds": d_right > 0 and d_wrong > 0},
        {"clause": 2, "what": "pooled through the closure recency is right on more points "
                              "than arrival; in v2e's run 1 and v2b's run 3 on fewer",
         "reading": {"pooled": gain, **fewer},
         "holds": gain > 0 and all(x < 0 for x in fewer.values())},
        {"clause": 3, "what": "pooled through the closure, arrival's and recency's right "
                              "points lie inside the coin's central 90%",
         "reading": {**ages, "coin_central": [lo, hi]},
         "holds": all(lo <= x <= hi for x in ages.values())},
        {"clause": 4, "what": "pooled through the closure, the ranking is right on more "
                              "points than recency and than arrival",
         "reading": others,
         "holds": others["ranking"] > max(others["recency"], others["arrival"])},
        {"clause": 5, "what": "pooled through the closure, the oracle is right on more "
                              "points than every other arm and than the coin's mean",
         "reading": {"oracle": right(arms, "oracle"), **others, "coin_mean": coin["mean"]},
         "holds": right(arms, "oracle") > max(*others.values(), coin["mean"])},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"blind/yielding.py writes {READ_PATH}")
    published = json.loads(closure.READ_PATH.read_text())
    space = Space()
    tmask = space_truth_masks(space)
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    bits = [closure.point_of(space, c) for c in corpus]
    mult = multiplicity(bits)
    records = {(p, r): json.loads(closure.record_path(p, r).read_text())
               for p in closure.PROTOCOLS for r in plan.BASELINE_REPS}
    bases = {key: read_base(key, rec, space, tmask, mult) for key, rec in records.items()}
    pool = pooled(bases)
    checked = check(bases, records, published, stop_zero(space, tmask), tmask, bits)
    for g in checked:
        print(f"  gate {g['gate']} {g['base']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    for b in bases.values():
        b.pop("_draws", None)
    READ_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"records": {f"{p} {r}": str(closure.record_path(p, r)) for p, r in records},
                   "closure": str(closure.READ_PATH)},
        "surfaces": {"space": "the exhaustive space, 134,400 points, uniform",
                     "corpus": "the 2,000 cases of seed 17, as they arrive"},
        "constants": {"N_COIN": N_COIN, "YIELD_SEED": YIELD_SEED, "CENTRAL": CENTRAL,
                      "ranking": STAGE_C_HIERARCHY},
        "gates": checked,
        "bases": {f"{p} {r}": b for (p, r), b in bases.items()},
        "pooled": pool,
        "expectation": read_expectation(bases, pool),
    }), indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
