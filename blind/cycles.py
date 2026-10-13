"""
WHY RUN 1 CLOSED CYCLES. Run 1 of `PLAN_BLIND.md` refused 20 of its placement
declarations for closing a cycle, and its 43 CONFLICTs came from them; runs 2 and
3 refused 0 and 1. A placement round lists its rules in a seeded order, recorded
with the call (§6.5 of the plan), so whether the cycles follow the listing slot
can be read from the records. This reads it, and what else they follow.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Rung 2's engine refuses an edge that would close a cycle, following subsumption
and the declared edges together (`PriorityEngine._reaches`). A birth installs
its `beats` first and its `loses_to` after
(`authorship.loop.install_declarations`). So a placement closes a cycle when it
puts the new rule above a listed rule X and below a listed rule Y that the base
already ranks below X, when it cites one rule on both sides, or when it goes
against a rule the new one is nested in or that is nested in it. **Which edge of
an inverted pair is refused is the installation's order**: always the
`loses_to`, and nothing is read into it.

If the proposer placed by slot, a pair the list showed in the order opposite to
the base's would be inverted more often than a pair shown in the base's order.
The list is `sorted(O)` shuffled by `Random(f"17/{idx}/0")`, so the slot is
independent of the rules, and permuting the slots within each round is the exact
null of "the slot moves nothing". It reads no truth: only the placements and the
order the engine already held.

--------------------------------------------------------------------------
WHAT IT READS, per run, on the births with a placement round
--------------------------------------------------------------------------
Each run is replayed through `blind/loop.py` with its own answers, and the engine
is forked at every call, before the answer the call receives is installed. For
each placement round that bore a rule, with the new rule born on its fork and
none of its declarations installed:

  placed        each listed rule's side: `loses_to`, above the new rule;
                `beats`, below it; or both.
  mixed pairs   two listed rules placed on opposite sides. The slot statistic
                counts +1 when the one placed above was listed first, -1 when it
                was listed second.
  ordered pairs two listed rules, each placed on one side, the first of which
                reaches the second on the fork: the base ranks it higher.
  inverted      an ordered pair with the new rule placed above the higher rule
                and below the lower one: a cycle whatever the order of
                installation. The inversion statistic counts +1 when the lower
                rule, the one placed above, was listed first, -1 when second.

Both statistics are tested against `N_PERM` within-round permutations of the
slots, seeded by `PERM_SEED`, pooled over the three runs and for each run alone,
two-sided. Beside them, how the rule at the first slot, at the last and at the
slots between was placed.

Every edge the engine refused for a cycle, on either channel, is installed again
on the fork of its call in the order logged, with a shortest path that closes it
and what closes it: an inverted pair (`pair`), one rule cited on both sides
(`both`), or subsumption, through a rule the new one is nested in (`inside`) or
one nested in it (`contains`); an order edge is `order`. Then the births with a
refusal, and how many each has. On the order channel, whether an edge refused
for a cycle repeats, winner and loser, one refused on the write channel earlier
in the run, and whether an accepted one reverses one.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the run**: its records, rules, edge log, channels, metrics
     and calls, every one equal to the record's.
  2. **The slot is the seeded deal**: every placement list is
     `protocol.listing` of the rules the draft overlapped.
  3. **The forks are the engine**: every logged edge, installed again on the fork
     of its call, gets the verdict the record logged; every rule born on a fork
     gets the id the run gave it; and an escalation that bore nothing and
     ordered nothing logged nothing.
  4. **Every cycle is accounted for**: the refusals read, on both channels, are
     `score.json`'s `cierra_ciclo` in every run.
  5. **The null is a function of its seed**: the tests, at `N_CHECK`
     permutations, give the same counts twice.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **The slot does not move the side.** Pooled over the three runs, the slot
     statistic over mixed pairs has a two-sided p of at least 0.05.
  2. **The cycles do not follow the slot.** Pooled, the inversion statistic has
     a two-sided p of at least 0.05.
  3. **Run 1's cycles are a few births.** Its write-channel refusals for a cycle
     come from at most 6 births.
  4. **Not room alone.** Run 1's share of ordered pairs inverted is at least
     twice the share of runs 2 and 3 pooled.
  5. **Asked again, it answered the same.** At least 9 of run 1's 12 order-channel
     refusals for a cycle repeat, winner and loser, an edge refused for a cycle
     on the write channel earlier in the run.

**What the drafter had seen**: `FINDINGS_BLIND.md` and `score.json`, with K-f's
counts: the placement rounds and the sizes of their lists, the declarations by
verdict, 20 cycles closed at a placement in run 1 and 0 and 1 in runs 2 and 3,
12 order answers and 12 order edges refused for a cycle in run 1, the 43, 0 and
2 CONFLICTs, and the copies of `R0034`. Run 1's edges by channel and verdict and
its escalations by verdict, which give back those counts. One escalation's
calls: run 1's case 2, one rule listed, placed above the new one. The code: the
seeded listing, `beats` installed before `loses_to`, and the cycle check through
subsumption. And the gates, run before this commit, which print pass or fail.
**Not seen**: any statistic over slots, any count of ordered or inverted pairs,
which births or rules the refusals sit on, and which order edges repeat a
placement. The first two clauses are the bets on the question. The third and
fourth bet that run 1's cycles are a few placements made against an order the
other runs also had, rather than the same rate over more room. The fifth bets
that the inverted side is the proposer's judgement and not a draw.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_BLIND.md`'s verdicts existed and after
`FINDINGS_BLIND.md` named the question, with the expectation above written
before the reading and committed before it ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. No verdict moves. Zero API
calls.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: WHAT THE BASE HAD ALREADY DECIDED
--------------------------------------------------------------------------
The first run found every refusal for a cycle to be `contains`: a `beats` from
a new rule to a listed rule that already reached it, through an earlier rule
nested in the new one. None was an inverted pair, so the pairs the first
statistics read are not what closed the cycles. `already` reads what did, on
each placement that bore a rule, on the fork with the new rule born and none of
its declarations installed: the listed rules the base already ranked **above**
the new rule, through a rule nested in it or by being nested in it, and those it
already ranked **below**, through a rule it is nested in or by containing it.
For each, the side the answer put it on, whether that side agrees with the
base, the verdict the engine gave the declaration, and the rules the base's
order runs through, whether the list showed them and whether they are of the
new rule's own queue, which the placement never lists. Beside them, the sides
of the listed rules the base had not ranked against the new one.

A decomposition of the records the first run read, not a measurement, and no
expectation goes with it. Added in its own commit, after the first run of this
module; the record comes from a second run, which must give back every figure
of the first.

Usage:  PYTHONHASHSEED=0 python3 -m blind.cycles
"""

from __future__ import annotations

import collections
import json
import random
import sys
from dataclasses import asdict
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from authorship import gates as egates
from authorship import protocol as e
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, PriorityEngine, Space, validate_conditions

from . import gates, loop, plan
from . import protocol as p

READ_PATH = plan.OUT / "cycles.json"
N_PERM = 10_000                    # within-round permutations, fixed before the reading
N_CHECK = 500                      # gate 5's permutations, drawn twice
PERM_SEED = 17
ALPHA = 0.05                       # clauses 1 and 2
MAX_BIRTHS = 6                     # clause 3
RATE_FACTOR = 2.0                  # clause 4
MIN_REPEATS = 9                    # clause 5
ABOVE, BELOW, BOTH = "loses_to", "beats", "both"
STATS = ("mixed", "inverted")
PROVENANCE = (
    "POST-RUN: asked for after PLAN_BLIND.md's verdicts existed and after "
    "FINDINGS_BLIND.md named the question. The expectation in the module's "
    "docstring was written before the reading and committed before it ran. Not a "
    "signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# The replay, forked at every call
# ---------------------------------------------------------------------------

def fork(engine: PriorityEngine) -> PriorityEngine:
    """The engine's order as it stands, on sets of its own. The space and the
    rules are shared and never written; the log is not carried."""
    return PriorityEngine(
        space=engine.space, rules=list(engine.rules), ext=dict(engine.ext),
        sub_below={k: set(v) for k, v in engine.sub_below.items()},
        sub_above={k: set(v) for k, v in engine.sub_above.items()},
        decl_below={k: set(v) for k, v in engine.decl_below.items()},
        decl_above={k: set(v) for k, v in engine.decl_above.items()},
        _next_id=engine._next_id)


class ReplayV2B(gates.ReplayV2E):
    """A v2b run's answers, served back by case and round with v2b's screens,
    forking the engine at every call, before the answer it serves is installed.
    It never reaches a model."""

    name = "replay(v2b)"

    def __init__(self, record: dict, engine: PriorityEngine):
        super().__init__(record)
        self.engine = engine
        self.forks: dict[tuple[int, int], tuple[PriorityEngine, int]] = {}

    def build_base(self, engine, case, undefeated):
        return p.build_base(engine, case, undefeated)

    def _fork(self, idx: int, round_: int) -> None:
        self.forks[(idx, round_)] = (fork(self.engine), len(self.engine.edge_log))

    def first(self, case, base_text, idx):
        self._fork(idx, 0)
        return self._serve(idx, 0)

    def repair(self, case, base_text, previous, message, idx):
        self._fork(idx, 1)
        return self._serve(idx, 1)


def replay(record: dict, space: Space, corpus) -> tuple[ReplayV2B, dict[str, bool]]:
    """One of the runs through `blind/loop.py` with its own answers. Gate 1:
    every record, rule, edge, channel, metric and call back."""
    engine = PriorityEngine(space=space)
    proposer = ReplayV2B(record, engine)
    res = loop.run_loop(corpus, egates.labels_of(record), engine, proposer, blind=True)
    got = egates.as_json([asdict(x) for x in res.escalations])
    return proposer, {
        "records": egates.as_json([vars(r) for r in res.run.records]) == record["records"],
        "rules": egates.as_json([r.as_dict() for r in engine.rules]) == record["rules"],
        "edge_log": egates.as_json(engine.edge_log) == record["edge_log"],
        "edge_channels": res.edge_channels == record["edge_channels"],
        "metrics": egates.as_json(res.run.metrics) == record["metrics"],
        "calls": gates.without_seconds(got) == gates.without_seconds(record["escalations"]),
    }


def segments(record: dict, forks: dict) -> list[dict[str, Any]]:
    """Each escalation with the fork of the call whose answer was installed and
    the slice of the edge log it wrote: edges are logged only after an
    escalation's last call, and only during escalations."""
    escs = record["escalations"]
    starts = [forks[(x["idx"], 0)][1] for x in escs]
    out = []
    for k, x in enumerate(escs):
        last = max(c["round"] for c in x["calls"])
        f, start = forks[(x["idx"], last)]
        end = starts[k + 1] if k + 1 < len(escs) else len(record["edge_log"])
        out.append({"esc": x, "last": last, "fork": f, "start": start, "end": end})
    return out


# ---------------------------------------------------------------------------
# One placement, and why an edge closes a cycle
# ---------------------------------------------------------------------------

def sides(payload: dict, listed: list[str]) -> dict[str, str]:
    """Where the answer places each listed rule against the new one. A citation
    of a rule not listed is the loop's to drop, and is not read here."""
    cited = {d: set(e.citations(payload, d)) for d in (BELOW, ABOVE)}
    out = {}
    for rid in listed:
        b, a = rid in cited[BELOW], rid in cited[ABOVE]
        if a or b:
            out[rid] = BOTH if a and b else (BELOW if b else ABOVE)
    return out


def ordered_pairs(engine: PriorityEngine, listed: list[str],
                  side: dict[str, str]) -> list[tuple[str, str]]:
    """(X, Y) for two listed rules placed on one side each, X reaching Y on the
    engine as it stands: the base ranks X above Y."""
    single = [r for r in listed if side.get(r) in (ABOVE, BELOW)]
    return [(x, y) for x in single for y in single if x != y and engine._reaches(x, y)]


def inverted(pairs: list[tuple[str, str]], side: dict[str, str]) -> list[tuple[str, str]]:
    """The ordered pairs with the new rule above the higher and below the lower."""
    return [(x, y) for x, y in pairs if side[x] == BELOW and side[y] == ABOVE]


def path(engine: PriorityEngine, src: str, dst: str) -> list[list[str]]:
    """A shortest chain of 'beats' from src to dst, each hop marked by what makes
    it: subsumption, a declared edge, or both."""
    parent: dict[str, str | None] = {src: None}
    queue = collections.deque([src])
    while queue and dst not in parent:
        cur = queue.popleft()
        for nxt in sorted(engine.wins_over(cur)):
            if nxt not in parent:
                parent[nxt] = cur
                queue.append(nxt)
    if dst not in parent:
        return []
    hops, node = [], dst
    while parent[node] is not None:
        prev = parent[node]
        sub, decl = node in engine.sub_above[prev], node in engine.decl_above[prev]
        hops.append([prev, node, "sub+decl" if sub and decl else "sub" if sub else "decl"])
        node = prev
    return hops[::-1]


def classify(engine: PriorityEngine, new: str | None, w: str, l: str) -> dict[str, Any]:
    """Why `w beats l` closes a cycle on `engine`, read before it is tried."""
    hops = path(engine, l, w)
    if new is None:
        return {"kind": "order", "through": [], "path": hops}
    if l == new:                                   # a `loses_to`: new already reaches w
        if w in engine.decl_above[new]:
            return {"kind": "both", "through": [w], "path": hops}
        pair = sorted(x for x in engine.decl_above[new] if engine._reaches(x, w))
        if pair:
            return {"kind": "pair", "through": pair, "path": hops}
        inside = sorted(z for z in engine.sub_above[new] if engine._reaches(z, w))
        return {"kind": "inside", "through": inside, "path": hops}
    contains = sorted(z for z in engine.sub_below[new] if engine._reaches(l, z))
    return {"kind": "contains", "through": contains, "path": hops}


def reinstall(engine: PriorityEngine, entries: list, channels: list[str],
              new: str | None) -> tuple[list[dict[str, Any]], bool]:
    """The logged edges of one escalation, tried again in order on its fork.
    Returns every refusal for a cycle, classified, and whether every verdict is
    the one the record logged."""
    refusals, same = [], True
    for (w, l, logged), ch in zip(entries, channels):
        mine = new if ch == e.WRITE else None
        info = classify(engine, mine, w, l) if engine._reaches(l, w) else None
        why = engine.try_edge(w, l)
        same = same and why == logged
        if why == EDGE_CYCLE:
            refusals.append({"edge": [w, l], "channel": ch,
                             "side": (None if mine is None else BELOW if w == mine else ABOVE),
                             **info})
    return refusals, same


def already(engine: PriorityEngine, new: str, listed: list[str], side: dict[str, str],
            entries: list, action: dict[str, str]) -> list[dict[str, Any]]:
    """The listed rules the base had already ranked against the new one, read on
    its fork before any of its declarations: above it, through a rule nested in
    it, or below it, through a rule it is nested in. With the side the answer
    put each on, the verdict the engine gave that declaration, and the rules the
    base's order runs through. Added after the first run."""
    logged: dict[tuple[str, str], str] = {}
    for w, l, why in entries:
        logged.setdefault((w, l), why)
    out = []
    for slot, rid in enumerate(listed):
        s = side.get(rid)
        if s is None:
            continue
        if engine._reaches(rid, new):
            base = ABOVE
            through = sorted(w for w in engine.sub_below[new]
                             if w == rid or engine._reaches(rid, w))
        elif engine._reaches(new, rid):
            base = BELOW
            through = sorted(z for z in engine.sub_above[new]
                             if z == rid or engine._reaches(z, rid))
        else:
            continue
        edges = (([(new, rid)] if s in (BELOW, BOTH) else [])
                 + ([(rid, new)] if s in (ABOVE, BOTH) else []))
        out.append({"rule": rid, "slot": slot, "base": base, "side": s,
                    "agrees": s == base,
                    "verdicts": [logged.get(edge) for edge in edges],
                    "through": through,
                    "through_listed": [t in listed for t in through],
                    "through_own_queue": [action.get(t) == action.get(new) for t in through]})
    return out


def already_summary(rounds: list[dict]) -> dict[str, Any]:
    """`already` over a run's placements, beside the sides of the listed rules
    the base had not ranked against the new one. Added after the first run."""
    rows = [a for r in rounds for a in r["already"]]

    def tally(base: str) -> dict[str, Any]:
        sel = [a for a in rows if a["base"] == base]
        bad = [a for a in sel if not a["agrees"]]
        return {"rules": len(sel), "agree": len(sel) - len(bad), "contradict": len(bad),
                "sides": dict(sorted(collections.Counter(str(a["side"]) for a in sel).items())),
                "contradictions_by_verdict": dict(sorted(collections.Counter(
                    str(v) for a in bad for v in a["verdicts"]).items())),
                "contradictions_only_through_unlisted": sum(
                    1 for a in bad if a["through"] and not any(a["through_listed"])),
                "contradictions_only_through_own_queue": sum(
                    1 for a in bad if a["through"] and all(a["through_own_queue"]))}

    ranked = {(r["idx"], a["rule"]) for r in rounds for a in r["already"]}
    free = [s for r in rounds for rid, s in r["listed"] if (r["idx"], rid) not in ranked]
    return {"births_with_one": sum(bool(r["already"]) for r in rounds),
            "above": tally(ABOVE), "below": tally(BELOW),
            "unranked_sides": dict(sorted(collections.Counter(str(s) for s in free).items()))}


def read_segment(seg: dict, record: dict, corpus, action: dict[str, str]) -> dict[str, Any]:
    """One escalation on its fork: the rule it bore, if any, the placement it
    made, and the refusals for a cycle it logged."""
    x, f = seg["esc"], seg["fork"]
    entries = record["edge_log"][seg["start"]:seg["end"]]
    channels = record["edge_channels"][seg["start"]:seg["end"]]
    out: dict[str, Any] = {"idx": x["idx"], "kind": x["kind"], "verdict": x["verdict"],
                           "logged": len(entries), "id_ok": True, "placement": None}
    new = None
    if x["verdict"] == e.BORN:
        payload = next(c["payload"] for c in x["calls"] if c["round"] == seg["last"])
        rule = validate_conditions(payload, case=corpus[x["idx"]])
        f.add(rule, born_at=x["idx"])
        new = rule.rule_id
        out.update(rule=new, queue=rule.action, id_ok=new == x["rule_id"])
        if x["kind"] == "IMPASSE" and x["listed"]:
            side = sides(payload, x["listed"])
            pairs = ordered_pairs(f, x["listed"], side)
            out["placement"] = {
                "listed": [[rid, side.get(rid)] for rid in x["listed"]],
                "queues": [action[rid] for rid in x["listed"]],
                "ordered": [list(q) for q in pairs],
                "inverted": [list(q) for q in inverted(pairs, side)]}
            out["already"] = already(f, new, x["listed"], side, entries, action)
    refusals, same = reinstall(f, entries, channels, new)
    out.update(refusals=refusals, verdicts_ok=same,
               quiet_ok=x["verdict"] in (e.BORN, e.ORDER) or not entries)
    return out


# ---------------------------------------------------------------------------
# The slot
# ---------------------------------------------------------------------------

def slot_pairs(placement: dict) -> dict[str, list[tuple[int, int]]]:
    """The pairs each statistic counts, as slots (i, j): the rule at slot i
    placed above the new one, the rule at slot j below it."""
    listed = [rid for rid, _ in placement["listed"]]
    slot = {rid: i for i, rid in enumerate(listed)}
    above = [i for i, (_, s) in enumerate(placement["listed"]) if s == ABOVE]
    below = [j for j, (_, s) in enumerate(placement["listed"]) if s == BELOW]
    return {"mixed": [(i, j) for i in above for j in below],
            "inverted": [(slot[y], slot[x]) for x, y in placement["inverted"]]}


def statistic(pairs: list[tuple[int, int]], pos: list[int]) -> int:
    """+1 for each pair whose rule placed above is listed first, -1 otherwise."""
    return sum(1 if pos[i] < pos[j] else -1 for i, j in pairs)


def slot_test(rounds: dict[int, list[dict]], n_perm: int, seed: int) -> dict[str, Any]:
    """Both statistics, observed and against `n_perm` within-round permutations
    of the slots: per run and pooled, two-sided."""
    reps = sorted(rounds)
    sized = {rep: [(len(r["listed"]), slot_pairs(r)) for r in rounds[rep]] for rep in reps}
    keys = [str(rep) for rep in reps] + ["pooled"]

    def totals(draw) -> dict[str, dict[str, int]]:
        out = {s: {} for s in STATS}
        for rep in reps:
            acc = {s: 0 for s in STATS}
            for n, pairs in sized[rep]:
                pos = draw(n)
                for s in STATS:
                    acc[s] += statistic(pairs[s], pos)
            for s in STATS:
                out[s][str(rep)] = acc[s]
        for s in STATS:
            out[s]["pooled"] = sum(out[s][str(rep)] for rep in reps)
        return out

    observed = totals(lambda n: list(range(n)))
    rng = random.Random(seed)

    def shuffled(n: int) -> list[int]:
        pos = list(range(n))
        if n > 1:
            rng.shuffle(pos)
        return pos

    extreme = {s: {k: 0 for k in keys} for s in STATS}
    for _ in range(n_perm):
        got = totals(shuffled)
        for s in STATS:
            for k in keys:
                extreme[s][k] += abs(got[s][k]) >= abs(observed[s][k])
    n_pairs = {s: {str(rep): sum(len(pairs[s]) for _, pairs in sized[rep]) for rep in reps}
               for s in STATS}
    for s in STATS:
        n_pairs[s]["pooled"] = sum(n_pairs[s][str(rep)] for rep in reps)
    return {s: {k: {"pairs": n_pairs[s][k], "statistic": observed[s][k],
                    "per_pair": (observed[s][k] / n_pairs[s][k] if n_pairs[s][k] else None),
                    "as_extreme": extreme[s][k],
                    "p": (1 + extreme[s][k]) / (n_perm + 1)}
                for k in keys}
            for s in STATS} | {"n_perm": n_perm, "seed": seed}


def by_slot(rounds: list[dict]) -> dict[str, dict[str, int]]:
    """For the rounds listing two rules or more: how the rule at the first slot,
    at the last, and at the slots between was placed."""
    out = {k: collections.Counter() for k in ("first", "between", "last")}
    for r in rounds:
        placed = [s for _, s in r["listed"]]
        if len(placed) < 2:
            continue
        out["first"][str(placed[0])] += 1
        out["last"][str(placed[-1])] += 1
        out["between"].update(str(s) for s in placed[1:-1])
    return {k: dict(sorted(v.items())) for k, v in out.items()}


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict, space: Space, corpus) -> dict[str, Any]:
    proposer, parity = replay(record, space, corpus)
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    segs = [read_segment(s, record, corpus, action)
            for s in segments(record, proposer.forks)]
    listing_ok = all(x["listed"] == p.listing(x["calls"][0]["overlapped"], x["idx"], 0)
                     for x in record["escalations"] if x["kind"] == "IMPASSE" and x["listed"])
    placed_segs = [s for s in segs if s["placement"] is not None]
    rounds = [dict(s["placement"], idx=s["idx"], rule=s["rule"], queue=s["queue"],
                   refused=sum(r["channel"] == e.WRITE for r in s["refusals"]))
              for s in placed_segs]
    refusals = [dict(r, idx=s["idx"], rule=s.get("rule"))
                for s in segs for r in s["refusals"]]
    write = [r for r in refusals if r["channel"] == e.WRITE]
    order = [r for r in refusals if r["channel"] == e.ORDER_CHANNEL]
    per_birth = collections.Counter((r["idx"], r["rule"]) for r in write)

    seen: list[tuple[str, str]] = []
    repeats = 0
    for r in refusals:
        if r["channel"] == e.WRITE:
            seen.append(tuple(r["edge"]))
        elif tuple(r["edge"]) in seen:
            repeats += 1
    accepted_order, reversing = 0, 0
    write_refused_before: list[tuple[str, str]] = []
    for (w, l, why), ch in zip(record["edge_log"], record["edge_channels"]):
        if ch == e.WRITE and why == EDGE_CYCLE:
            write_refused_before.append((w, l))
        elif ch == e.ORDER_CHANNEL and why != EDGE_CYCLE:
            accepted_order += 1
            reversing += (l, w) in write_refused_before

    ordered = sum(len(r["ordered"]) for r in rounds)
    inv = sum(len(r["inverted"]) for r in rounds)
    placed = collections.Counter(str(s) for r in rounds for _, s in r["listed"])
    mixed_ordered = {"higher_first": {"consistent": 0, "inverted": 0},
                     "lower_first": {"consistent": 0, "inverted": 0}}
    for r in rounds:
        slot = {rid: i for i, (rid, _) in enumerate(r["listed"])}
        side = dict((rid, s) for rid, s in r["listed"])
        for x, y in r["ordered"]:
            if side[x] == side[y]:
                continue
            first = "higher_first" if slot[x] < slot[y] else "lower_first"
            mixed_ordered[first]["inverted" if side[x] == BELOW else "consistent"] += 1
    return {
        "gates": {"replay": parity, "listing": listing_ok,
                  "forks": {"verdicts": all(s["verdicts_ok"] for s in segs),
                            "ids": all(s["id_ok"] for s in segs),
                            "quiet": all(s["quiet_ok"] for s in segs)},
                  "cycles_read": len(refusals)},
        "placement_births": len(rounds),
        "listing_two_or_more": sum(len(r["listed"]) >= 2 for r in rounds),
        "placed": dict(sorted(placed.items())),
        "mixed_pairs": sum(len(slot_pairs(r)["mixed"]) for r in rounds),
        "ordered_pairs": ordered,
        "inverted_pairs": inv,
        "inverted_share": inv / ordered if ordered else None,
        "mixed_ordered_by_listing": mixed_ordered,
        "write_refusals": {
            "total": len(write),
            "in_placement_rounds": sum(r["refused"] for r in rounds),
            "by_kind": dict(sorted(collections.Counter(r["kind"] for r in write).items())),
            "by_side": dict(sorted(collections.Counter(r["side"] for r in write).items())),
            "births_with_a_cycle": len(per_birth),
            "per_birth": [[idx, rule, n] for (idx, rule), n in
                          sorted(per_birth.items(), key=lambda kv: (-kv[1], kv[0][0]))]},
        "order_refusals": {"total": len(order),
                           "distinct": len({tuple(r["edge"]) for r in order}),
                           "repeating_a_write_refusal": repeats,
                           "accepted_order_edges": accepted_order,
                           "accepted_reversing_a_write_refusal": reversing},
        "by_slot": by_slot(rounds),
        "rounds": rounds,
        "refusals": refusals,
        "added": {"already_decided": already_summary(
                      [dict(r, already=s["already"]) for r, s in zip(rounds, placed_segs)]),
                  "already": {str(s["idx"]): s["already"] for s in placed_segs
                              if s["already"]}},
    }


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def check(score: dict, runs: dict[int, dict], first: dict, second: dict) -> list[dict]:
    published = {r["rep"]: r["K-f"]["declarations"].get(EDGE_CYCLE, 0) for r in score["runs"]}
    out = []
    for rep, run in runs.items():
        g = run["gates"]
        out += [
            {"gate": 1, "rep": rep, "what": "the replay is the run",
             "passes": all(g["replay"].values())},
            {"gate": 2, "rep": rep, "what": "the slot is the seeded deal",
             "passes": g["listing"]},
            {"gate": 3, "rep": rep, "what": "the forks are the engine",
             "passes": all(g["forks"].values())},
            {"gate": 4, "rep": rep, "what": "every cycle is accounted for",
             "measured": g["cycles_read"], "published": published.get(rep),
             "passes": g["cycles_read"] == published.get(rep)},
        ]
    same = all(first[s][k]["as_extreme"] == second[s][k]["as_extreme"]
               for s in STATS for k in first[s])
    out.append({"gate": 5, "rep": "pooled", "what": "the null is a function of its seed",
                "passes": same})
    return out


def read_expectation(tests: dict, runs: dict[str, dict]) -> list[dict]:
    r1 = runs["1"]
    others = [runs[k] for k in runs if k != "1"]
    ordered = sum(r["ordered_pairs"] for r in others)
    share23 = (sum(r["inverted_pairs"] for r in others) / ordered) if ordered else None
    share1 = r1["inverted_share"]
    births = r1["write_refusals"]["births_with_a_cycle"]
    repeats = r1["order_refusals"]["repeating_a_write_refusal"]
    return [
        {"clause": 1, "what": "pooled, the slot statistic over mixed pairs has p >= 0.05",
         "reading": tests["mixed"]["pooled"]["p"],
         "holds": tests["mixed"]["pooled"]["p"] >= ALPHA},
        {"clause": 2, "what": "pooled, the inversion statistic has p >= 0.05",
         "reading": tests["inverted"]["pooled"]["p"],
         "holds": tests["inverted"]["pooled"]["p"] >= ALPHA},
        {"clause": 3, "what": "run 1's write-channel refusals for a cycle come from at "
                              "most 6 births",
         "reading": births, "holds": births <= MAX_BIRTHS},
        {"clause": 4, "what": "run 1's share of ordered pairs inverted is at least twice "
                              "that of runs 2 and 3 pooled",
         "reading": [share1, share23],
         "holds": (None if share1 is None or share23 is None
                   else share1 >= RATE_FACTOR * share23)},
        {"clause": 5, "what": "at least 9 of run 1's 12 order-channel refusals for a cycle "
                              "repeat a write-channel refusal",
         "reading": repeats, "holds": repeats >= MIN_REPEATS},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"blind/cycles.py writes {READ_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    space = Space()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    records = {rep: json.loads(plan.run_path(rep).read_text())
               for rep in range(1, plan.REPS + 1)}
    runs = {rep: read_run(records[rep], space, corpus) for rep in records}
    rounds = {rep: runs[rep]["rounds"] for rep in runs}
    first = slot_test(rounds, N_CHECK, PERM_SEED)
    second = slot_test(rounds, N_CHECK, PERM_SEED)
    checked = check(score, runs, first, second)
    for g in checked:
        print(f"  gate {g['gate']} run {g['rep']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    tests = slot_test(rounds, N_PERM, PERM_SEED)
    by_run = {str(rep): {k: v for k, v in r.items() if k not in ("gates", "added")}
              for rep, r in runs.items()}
    with_already = [dict(r, already=runs[rep]["added"]["already"].get(str(r["idx"]), []))
                    for rep in runs for r in runs[rep]["rounds"]]
    READ_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"records": {str(rep): str(plan.run_path(rep)) for rep in records},
                   "their_commits": {str(rep): records[rep]["_env"].get("git_commit")
                                     for rep in records},
                   "score": str(plan.SCORE_PATH),
                   "its_commit": score["_env"].get("git_commit")},
        "surface": "none: the placements the runs recorded and the order the engine "
                   "held when each was made; no truth is read",
        "constants": {"N_PERM": N_PERM, "N_CHECK": N_CHECK, "PERM_SEED": PERM_SEED,
                      "LISTING_SEED": plan.LISTING_SEED},
        "gates": checked,
        "tests": tests,
        "by_slot_pooled": by_slot([r for rep in rounds for r in rounds[rep]]),
        "runs": by_run,
        "expectation": read_expectation(tests, by_run),
        "added_after_the_first_run": {
            "what": "what the base had already decided: the listed rules the base "
                    "already ranked above or below the new rule before any of its "
                    "declarations, the side the answer put each on, and the rules the "
                    "base's order runs through; a decomposition, with no expectation",
            "runs": {str(rep): r["added"] for rep, r in runs.items()},
            "pooled": already_summary(with_already)},
    }), indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
