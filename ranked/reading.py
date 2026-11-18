"""
What each engine decides of a finished record's base — the readings `RK-g1`,
Stage A and Stage C of `PLAN_RANKED.md` share. **Not on the proposer's path**:
this module reads the truth, over the space and at the arrivals.

A BASE IS READ TWO WAYS, off the same rules, containments and installed edges:

  rung 2   a point is decided where its undefeated rules carry one queue, and
           right where that queue is the point's; undefeated rules of two
           queues are a CONFLICT, which counts as wrong;
  ranked   rung 2's reading, and at every CONFLICT the queue the ranking puts
           first among the undefeated rules'. It is arm K's engine's.

`as_it_went` reads a record after every birth both ways, the ranking being the
one its votes so far choose. On an L record the ranked reading is a replay: its
rules are the ones L wrote under rung 2's engine. On a K record it is what K's
engine held.

`asked_conflicts` reads the CONFLICT cases an L run escalated: what the ranking
its votes chose so far would have decided there.
"""

from __future__ import annotations

from typing import Any, Iterator, Sequence

from harness.domain import ACTIONS, ATTRIBUTES, Case

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from rung2.engine2 import PriorityEngine, Space

from . import engine as E
from . import plan


def point_of(case: Case, space: Space) -> int:
    """The one point of the space a case is, as a mask."""
    m = space.full
    for a in ATTRIBUTES:
        m &= space.mask[a][getattr(case, a)]
    return m


def by_queue(und: dict[str, int], action: dict[str, str]) -> dict[str, int]:
    """Where a rule of each queue is undefeated."""
    out = {q: 0 for q in ACTIONS}
    for rid, m in und.items():
        out[action[rid]] |= m
    return out


def read(queues: dict[str, int], ranking: Sequence[str],
         truth: dict[str, int]) -> dict[str, int]:
    """Both readings of a base, as masks: the points in CONFLICT, the points
    rung 2's engine decides right, and those the ranked engine does."""
    seen = conflict = 0
    for q in ACTIONS:
        conflict |= seen & queues[q]
        seen |= queues[q]
    rung2 = 0
    for q in ACTIONS:
        rung2 |= queues[q] & ~conflict & truth.get(q, 0)
    taken = ranked = 0
    for q in ranking:
        ranked |= queues[q] & ~taken & truth.get(q, 0)
        taken |= queues[q]
    return {"conflict": conflict, "rung2": rung2, "ranked": ranked, "decided": seen}


def recall_of(right: int, truth: dict[str, int]) -> dict[str, tuple[int, int]]:
    """Each queue's points decided right, and its points."""
    return {q: ((right & truth.get(q, 0)).bit_count(), truth.get(q, 0).bit_count())
            for q in ACTIONS}


# ---------------------------------------------------------------------------
# A record, birth by birth
# ---------------------------------------------------------------------------

class Walk:
    """A record's base as its births come: rung 2's engine with the edges each
    birth tried, where each rule is undefeated, and the votes so far."""

    def __init__(self, record: dict[str, Any], space: Space):
        self.born = erb.births(record)
        self.edges = erb.edges_by_birth(record)
        self.engine = PriorityEngine(space=space)
        self.und: dict[str, int] = {}
        self.action: dict[str, str] = {}
        self.tally = E.Tally()
        self.whole = True                  # every edge had its newborn at one end

    def birth(self, idx: int) -> dict[str, Any]:
        d = self.born[idx]
        rid = d["rule_id"]
        engine = self.engine
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        for e in self.edges.get(idx, []):
            self.whole &= rid in (e.winner, e.loser)
            engine.try_edge(e.winner, e.loser)
        ext = engine.ext[rid]
        self.action[rid] = d["action"]
        for u in engine.wins_over(rid):
            self.und[u] &= ~ext
        beaten = 0
        for b in engine.beats_me(rid):
            beaten |= engine.ext[b]
        self.und[rid] = ext & ~beaten
        self.tally.born(d)
        return d

    def queues(self) -> dict[str, int]:
        return by_queue(self.und, self.action)

    def sound(self) -> bool:
        """The masks kept as the births came are the ones the engine gives."""
        return self.whole and self.und == brows.undefeated_masks(self.engine)


def as_it_went(record: dict[str, Any], space: Space,
               truth: dict[str, int]) -> dict[str, Any]:
    """After every birth: the ranking the votes so far choose, and the points
    each reading decides right. Then the final base, read whole."""
    walk = Walk(record, space)
    curve = []
    got: dict[str, int] = {}
    for idx in sorted(walk.born):
        walk.birth(idx)
        got = read(walk.queues(), walk.tally.ranking, truth)
        curve.append({**walk.tally.log[-1], "conflict": got["conflict"].bit_count(),
                      "rung2": got["rung2"].bit_count(), "ranked": got["ranked"].bit_count()})
    return {"curve": curve, "final": got, "tally": walk.tally, "engine": walk.engine,
            "sound": walk.sound()}


def summary(curve: list[dict[str, Any]], key: str) -> dict[str, Any]:
    """A curve's peak, the birth it comes at, counted from 1, and its end."""
    if not curve:
        return {"peak": 0, "peak_birth": None, "final": 0}
    at = max(range(len(curve)), key=lambda i: (curve[i][key], -i))
    return {"peak": curve[at][key], "peak_birth": at + 1, "final": curve[-1][key]}


def at_case(curve: list[dict[str, Any]], case: int) -> dict[str, Any] | None:
    """The curve's point after the last birth up to `case`."""
    before = [p for p in curve if p["born_at"] <= case]
    return before[-1] if before else None


# ---------------------------------------------------------------------------
# The conflicts a run asked about, under the ranking it had then
# ---------------------------------------------------------------------------

def asked_conflicts(record: dict[str, Any], corpus: Sequence[Case], space: Space
                    ) -> Iterator[dict[str, Any]]:
    """Each case the record escalated as a CONFLICT: the queue the ranking of
    the votes so far puts first among its undefeated rules', and the case's
    label. The base is the one the engine held when it decided the case."""
    walk = Walk(record, space)
    for row in sorted(record["records"], key=lambda r: r["idx"]):
        idx = row["idx"]
        if row["cause"] == plan.CONFLICT:
            queues = walk.queues()
            here = point_of(corpus[idx], space)
            present = [q for q in walk.tally.ranking if queues[q] & here]
            yield {"idx": idx, "queues": present, "decided": present[0] if present else None,
                   "truth": row["truth"], "ranking": walk.tally.state[0],
                   "tied": walk.tally.state[2]}
        if idx in walk.born:
            walk.birth(idx)


# ---------------------------------------------------------------------------
# A record's final base, as arm K's engine
# ---------------------------------------------------------------------------

def engine_of(final: PriorityEngine, record: dict[str, Any]) -> E.RankedEngine:
    """Arm K's engine over a record's final base: rung 2's rules, containments
    and installed edges, as `final` rebuilt them, and the record's citations."""
    eng = E.RankedEngine(space=final.space, rules=final.rules, ext=final.ext,
                         sub_below=final.sub_below, sub_above=final.sub_above,
                         decl_below=final.decl_below, decl_above=final.decl_above,
                         edge_log=final.edge_log)
    by_id = {d["rule_id"]: d for d in record["rules"]}
    for r in sorted(eng.rules, key=lambda r: (r.born_at, r.rule_id)):
        for k, v in E.cited(by_id[r.rule_id]).items():
            setattr(r, k, list(v))
    eng.rules = sorted(eng.rules, key=lambda r: (r.born_at, r.rule_id))
    eng.refresh()
    return eng
