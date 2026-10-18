"""
THE RULES' SIDE — what executes the proposer's rules, and the space they are
scored over. `PLAN_STUDENTS.md` §4.

Everything here is rung 3's, `PLAN_EDGES.md`'s or rung 2's code, called and not
copied, so that a figure on this side is a figure of an instance some record
already describes:

  * **rung 1's 577 rules**: `rung3.order_search.load`, `subsumption_below` and
    `build_tables` give the `puro` pool, the one `results3/` searched on;
    `rung3.local_search.build_masks` and `score_order` score an order on a set of
    cases, and `rung3.order_search_ls.space_pools` over the space.
  * **arrival order** is the rules by birth; **reversed** is its reverse.
  * **the order on the answers** is `rung3.order_search_ls.search`, the greedy
    and then the declared multi-start, over masks labelled with the proposer's
    queues where rung 3 put the truth. Nothing else moves.
  * **rung 1's own engine** is `rung3.order_search.eval_specificity` on the
    corpus, and over the space `specificity_space`, which `T-g1` holds equal to
    it on every corpus case.
  * **`PLAN_REUSE.md`'s bases** are the engines `edges.rebuild.rebuild` leaves at
    the end of each run, every rule born and every edge installed. Over the
    space, `regions` decides each point where its undefeated rules agree, which
    `T-g1` holds equal to `decide` on every corpus case.

THE TRUTH enters through `build_tables` and `space_truth_masks`, which
`tests/test_oracle_separation.py` already allows. This module imports no oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Sequence

from edges.rebuild import rebuild
from harness.domain import ATTRIBUTES, DOMAINS, Case
from rung2.engine2 import Space
from rung3.local_search import build_masks, score_order
from rung3.order_search import (build_tables, eval_specificity, load,
                                subsumption_below)
from rung3.order_search_ls import search, space_pools, space_truth_masks

from . import material

# ---------------------------------------------------------------------------
# The space, in `Space`'s convention
# ---------------------------------------------------------------------------

_RADIX = [len(DOMAINS[a]) for a in ATTRIBUTES]


def space_index(case: Case) -> int:
    """The position of a ticket in `harness.ceiling_check.all_cases`, which is
    `itertools.product` over the attributes in `ATTRIBUTES` order."""
    k = 0
    for a, r in zip(ATTRIBUTES, _RADIX):
        k = k * r + DOMAINS[a].index(getattr(case, a))
    return k


@lru_cache(maxsize=None)
def space() -> Space:
    return Space()


@lru_cache(maxsize=None)
def space_truth() -> dict[str, int]:
    """`{queue: points whose true queue it is}`, rung 3's own masks."""
    return space_truth_masks(space())


def bit(mask: int, i: int, n: int) -> bool:
    """Point `i` of a mask in `Space`'s convention, whose first point is the
    most significant bit."""
    return (mask >> (n - 1 - i)) & 1 == 1


def mask_from_points(points: Sequence[int], n: int) -> int:
    flags = bytearray(n)
    for i in points:
        flags[i] = 1
    return int("".join(map(str, flags)), 2) if n else 0


def right_over_space(pred: dict[str, int]) -> int:
    """Points where a prediction mask names the true queue."""
    t = space_truth()
    return sum((m & t.get(a, 0)).bit_count() for a, m in pred.items())


# ---------------------------------------------------------------------------
# Rung 1's rules
# ---------------------------------------------------------------------------

@dataclass
class Rung1:
    corpus: list
    rules: list[dict]
    ids: list[str]
    action: dict[str, str]
    born: dict[str, int]
    ext: dict[str, int]
    conds: dict[str, Any]
    below: dict[str, set]
    matched: list[list[str]]
    truth: list[str]

    def arrival(self) -> list[str]:
        return sorted(self.ids, key=lambda r: (self.born[r], r))

    def reversed_arrival(self) -> list[str]:
        return list(reversed(self.arrival()))

    def masks(self, label, idxs):
        """`(M, W, full)` over `idxs` on the `puro` pool, `label` indexed by case."""
        return build_masks(self.ids, self.matched, label, self.action, list(idxs))

    @property
    def test(self) -> tuple[int, ...]:
        return material.split()[1]

    def test_masks(self):
        return self.masks(self.truth, self.test)

    def space_masks(self):
        M, W, full, _n = space_pools(self.ids, self.conds, self.action,
                                     self.below)["puro"]
        return M, W, full


@lru_cache(maxsize=None)
def rung1() -> Rung1:
    corpus, rules, ext, conds = load()
    below = subsumption_below(rules, ext)
    matched, _undef, truth = build_tables(corpus, rules, conds, below)
    return Rung1(corpus, rules, [r["rule_id"] for r in rules],
                 {r["rule_id"]: r["action"] for r in rules},
                 {r["rule_id"]: r["born_at"] for r in rules},
                 ext, conds, below, matched, truth)


def scored(order: list[str], masks) -> int:
    return score_order(order, *masks)


def search_order(base: Rung1, labels, idxs: Sequence[int]):
    """Rung 3's search over the `puro` pool, labelled by `labels` on `idxs`:
    the greedy, then the declared multi-start. `labels` is indexed by case: the
    truth for `T-g1`'s check, the proposer's queues for `T-d`. Returns the best
    order and the search's statistics."""
    M, W, full = base.masks(labels, idxs)
    _greedy, best, st = search(base.ids, M, W, full, base.born)
    return best, {k: st[k] for k in ("best_score", "best_from", "best_from_index",
                                     "n_starts", "neighbourhood")} | {
        "labelled_cases": len(idxs)}


def specificity_test(base: Rung1) -> float:
    rules = base.rules
    return eval_specificity(rules, base.matched, base.truth, base.action,
                            list(base.test))


def specificity_space(base: Rung1) -> dict[str, int]:
    """Rung 1's engine over the space, as masks: the most specific matching
    rules decide, and only where they agree. `{queue: points decided so}`."""
    full = space().full
    by_k: dict[int, dict[str, int]] = {}
    for r in base.rules:
        k = len(r["conditions"])
        d = by_k.setdefault(k, {})
        d[r["action"]] = d.get(r["action"], 0) | base.ext[r["rule_id"]]
    above = 0
    out: dict[str, int] = {}
    for k in sorted(by_k, reverse=True):
        level = by_k[k]
        here = 0
        for m in level.values():
            here |= m
        top = here & ~above
        for a, m in level.items():
            others = 0
            for b, mb in level.items():
                if b != a:
                    others |= mb
            decided = top & m & ~others
            if decided:
                out[a] = out.get(a, 0) | decided
        above |= here
    return {a: m & full for a, m in out.items()}


# ---------------------------------------------------------------------------
# `PLAN_REUSE.md`'s bases
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def reuse_base(run: str):
    """The run's engine as the run left it, and the rebuild's decisions."""
    rec = material.record(run)
    return rebuild(rec, list(material.corpus()), space())


def rebuild_mismatches(run: str) -> list[int]:
    """Cases the rebuild decides otherwise than the record: none, or the base
    is not the run's."""
    rec = material.record(run)
    got = reuse_base(run).decisions
    bad = []
    for row in rec["records"]:
        d = got[row["idx"]]
        if (d.outcome, d.winner_id) != (row["outcome"], row["winner_id"]):
            bad.append(row["idx"])
    return bad


def regions(engine) -> dict[str, int]:
    """`{queue: points the engine decides so}`: each rule's undefeated region is
    its extension less those of the rules that beat it, and a point is decided
    where its undefeated rules agree."""
    undefeated: dict[str, int] = {}
    for r in engine.rules:
        m = engine.ext[r.rule_id]
        for b in engine.beats_me(r.rule_id):
            m &= ~engine.ext[b]
        if m:
            undefeated[r.action] = undefeated.get(r.action, 0) | m
    out = {}
    for a, m in undefeated.items():
        others = 0
        for b, mb in undefeated.items():
            if b != a:
                others |= mb
        decided = m & ~others
        if decided:
            out[a] = decided
    return out


def decide_action(engine, case: Case) -> str | None:
    outcome, winner, _ = engine.decide(case)
    return winner.action if outcome == "ACTION" else None


def reuse_arrival(engine):
    """The base's rules first-match by birth, as `(order, M, W, full)` over the
    space, with `M` their extensions and `W` where their queue is the truth."""
    t = space_truth()
    order = [r.rule_id for r in sorted(engine.rules, key=lambda r: (r.born_at, r.rule_id))]
    act = {r.rule_id: r.action for r in engine.rules}
    M = {rid: engine.ext[rid] for rid in order}
    W = {rid: M[rid] & t.get(act[rid], 0) for rid in order}
    return order, M, W, space().full


def first_match(rules_in_order, case: Case) -> str | None:
    for r in rules_in_order:
        if r.matches(case):
            return r.action
    return None

