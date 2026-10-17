"""
The instrument of `PLAN_RANKING.md`: what a ranking of the eight queues scores,
what it predicts of the model's pairwise answers, and how it points
`PLAN_BLIND.md`'s pairs. Zero API calls. Every piece is another thread's
function, called and not reimplemented (rule A of the plan):

  the cells     rung 1's 577 rules over rung 3's pools, built exactly as
                `rung3/queue_hierarchy_floor.py` builds them: the tables by
                `rung3.order_search.build_tables`, the space by
                `rung3.order_search_ls.space_pools`, the splits by
                `rung3.floor_by_pool.index_sets_of`. The hybrid pool is rung 3's
                masks, never rung 2's engine (`CLAUDE.md`'s note on it).
  a score       `hierarchy_order` then `floor`. The intra-class tie-break
                provably cannot move it (§5.4), and `M-g1` checks that it does
                not.
  the answers   the declared answers of `results2/pair_judgement_1600.json`,
                derived by that thread's own `classify_learned`, which is the
                population `revealed_hierarchy` and `rung3/edge_dropping.py`
                read; and the two-way answers of
                `results2/pair_judgement_hidden.json`.
  the revealed  `rung3.edge_dropping.revealed_ranking`: Copeland over the queue
  ranking       pairs the model decided, which `FINDINGS3.md` §14 publishes.
  K-b's pairs   the edge rows `results_blind/score.json` stores, read by
                `blind.rows.direction` with a `predict` built from a ranking.

NOTHING HERE READS THE ORACLE BY ITS OWN IMPORT. The truth the cells are scored
against is what rung 3's instance builders label them with, as every rung 3
figure has been; `tests/test_oracle_separation.py` checks this module's imports.

WHAT THIS MODULE NEVER DOES BEFORE THE SIGNATURE. It computes what a ranking
scores or predicts only when asked, and the dry run asks it only for figures
that are already published (`ranking/gates.py`). The populations are counted
there; their rates under any ranking but the revealed one, whose agreement with
its own answers §14 publishes, are not.
"""

from __future__ import annotations

import bisect
import itertools
import json
import statistics
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

from blind import rows as blind_rows
from rung2.pair_judgement import classify_learned
from rung3.edge_dropping import revealed_ranking
from rung3.floor_by_pool import (CORPUS_FULL, POOLS, SPACE, born_at_order,
                                 corpus_instances, floor, index_sets_of,
                                 test_split_name)
from rung3.order_search import build_tables, load, subsumption_below
from rung3.order_search_ls import space_pools
from rung3.queue_hierarchy_floor import N_SPLITS, STAGE_C_HIERARCHY, hierarchy_order

from . import plan

SPLITS = tuple(test_split_name(s) for s in range(N_SPLITS))
SURFACES = (CORPUS_FULL,) + SPLITS + (SPACE,)
FIVE_SPLITS = "corpus_test_5splits"
CELLS = tuple((pool, surface) for pool in POOLS for surface in SURFACES)
QUEUE_PAIRS = tuple(itertools.combinations(sorted(plan.QUEUES), 2))   # the 28


def cell_name(pool: str, surface: str) -> str:
    return f"{pool}/{surface}"


# ---------------------------------------------------------------------------
# The cells
# ---------------------------------------------------------------------------

@dataclass
class Instrument:
    ids: list[str]
    action: dict[str, str]
    born: dict[str, int]
    actions: list[str]                       # sorted, as rung 3 enumerates them
    instances: dict[tuple[str, str], tuple] = field(repr=False)
    n_cases: int = 0
    n_space: int = 0

    def instance(self, pool: str, surface: str) -> tuple:
        return self.instances[(surface, pool)]


def build() -> Instrument:
    """Every cell, as `rung3.queue_hierarchy_floor.main` builds them."""
    corpus, rules, ext, conds = load()
    ids = [r["rule_id"] for r in rules]
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    sets = index_sets_of(corpus, truth)
    instances = corpus_instances(ids, {"puro": matched, "hibrido": undef}, truth,
                                 action, sets)
    spools = space_pools(ids, conds, action, below)
    for name in POOLS:
        instances[(SPACE, name)] = spools[name]
    return Instrument(ids=ids, action=action, born=born,
                      actions=sorted(set(action.values())), instances=instances,
                      n_cases=len(corpus), n_space=spools["puro"][3])


def rank_of(order: Sequence[str]) -> dict[str, int]:
    return {q: i for i, q in enumerate(order)}


def score(inst: Instrument, order: Sequence[str], pool: str, surface: str,
          tiebreak: str = "born_at") -> float:
    """What the order a ranking induces over the 577 rules scores on one cell."""
    return floor(hierarchy_order(inst.ids, inst.action, inst.born, rank_of(order),
                                 tiebreak), inst.instance(pool, surface))


def born_at_score(inst: Instrument, pool: str, surface: str) -> float:
    return floor(born_at_order(inst.ids, inst.born), inst.instance(pool, surface))


def scores(inst: Instrument, order: Sequence[str]) -> dict[str, float]:
    """Every cell, and the five-split mean of each pool labelled as the
    aggregate it is."""
    out = {cell_name(p, s): score(inst, order, p, s) for p, s in CELLS}
    for pool in POOLS:
        out[cell_name(pool, FIVE_SPLITS)] = statistics.mean(
            out[cell_name(pool, s)] for s in SPLITS)
    return out


def distribution(inst: Instrument, pool: str, surface: str) -> list[float]:
    """What all 40,320 rankings score on one cell, sorted. `best`, `mean` and
    `worst` of it are the record's (`M-g1` checks them with rung 3's own
    enumeration); this keeps every value, for the percentiles of `M-f`."""
    inst_ = inst.instance(pool, surface)
    return sorted(floor(hierarchy_order(inst.ids, inst.action, inst.born,
                                        rank_of(perm)), inst_)
                  for perm in itertools.permutations(inst.actions))


def percentile(value: float, dist: Sequence[float]) -> float:
    """The mid-rank share of the 40,320 at or below `value`: those strictly
    below, plus half of those it ties."""
    lo = bisect.bisect_left(dist, value)
    hi = bisect.bisect_right(dist, value)
    return (lo + (hi - lo) / 2) / len(dist)


# ---------------------------------------------------------------------------
# The model's pairwise answers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Answer:
    """One pairwise answer: the two queues on offer and the one named."""
    queues: tuple[str, str]
    named: str


def learned_rows(path: Path | None = None) -> list[dict]:
    """The 1,600 rows whose answer declared an edge, by that thread's own
    `classify_learned`, rederived and checked against the stored field."""
    rec = json.loads((path or plan.PAIRWISE_LEARNED).read_text())
    out = []
    for r in rec["answers"]:
        if classify_learned(r["answer"], r) != r["declared"]:
            raise ValueError(f"row {r['index']}: its declared field is not its answer's")
        if r["declared"] != "none":
            out.append(r)
    return out


def learned_answers(path: Path | None = None) -> list[Answer]:
    out = []
    for r in learned_rows(path):
        named = r["action_a"] if r["declared"] == "a_beats_b" else r["action_b"]
        out.append(Answer((r["action_a"], r["action_b"]), named))
    return out


def hidden_answers(path: Path | None = None) -> list[Answer]:
    """The hidden policy's pairs whose answer named one of the two queues on
    offer: `FINDINGS3.md` §15's two-way answers."""
    rec = json.loads((path or plan.PAIRWISE_HIDDEN).read_text())
    out = []
    for r in rec["answers"]:
        pair = (r["winner_action"], r["loser_action"])
        if r["parse_failed"] or r["off_menu"] or r["answer"] not in pair:
            continue
        out.append(Answer(pair, r["answer"]))
    return out


def predicts(order: Sequence[str], answers: Sequence[Answer]) -> tuple[int, int]:
    """(hits, n): the answers whose named queue is the one `order` ranks higher
    of the two on offer."""
    rank = rank_of(order)
    hits = sum(1 for a in answers
               if min(a.queues, key=lambda q: rank[q]) == a.named)
    return hits, len(answers)


def revealed_learned(path: Path | None = None) -> tuple[list[str], dict[str, int]]:
    """`rung3/edge_dropping.py`'s revealed ranking, over the same rows."""
    order, _rank, copeland = revealed_ranking(learned_rows(path))
    return order, copeland


def revealed_of(answers: Sequence[Answer]) -> tuple[list[str], dict[str, int]]:
    """The same Copeland, over any answers: each named queue as `a_beats_b`."""
    rows = [{"declared": "a_beats_b", "action_a": a.named,
             "action_b": a.queues[1] if a.named == a.queues[0] else a.queues[0]}
            for a in answers]
    order, _rank, copeland = revealed_ranking(rows)
    return order, copeland


def by_queue_pair(answers: Sequence[Answer]) -> dict[str, dict[str, int]]:
    """For each unordered pair of queues, how often each side was named."""
    out: dict[tuple[str, str], Counter] = {}
    for a in answers:
        key = tuple(sorted(a.queues))
        out.setdefault(key, Counter())[a.named] += 1
    return {" vs ".join(k): dict(v) for k, v in sorted(out.items())}


# ---------------------------------------------------------------------------
# Rankings against each other
# ---------------------------------------------------------------------------

def above(order: Sequence[str]) -> dict[tuple[str, str], bool]:
    """For each of the 28 queue pairs (x, y), sorted, whether x is ranked above y."""
    rank = rank_of(order)
    return {(x, y): rank[x] < rank[y] for x, y in QUEUE_PAIRS}


def agreement(a: Sequence[str], b: Sequence[str]) -> float:
    """The share of the 28 queue pairs two rankings order the same way."""
    da, db = above(a), above(b)
    return sum(da[p] == db[p] for p in QUEUE_PAIRS) / len(QUEUE_PAIRS)


def slot_gap(asks: Sequence[tuple[str, int, Sequence[str]]]) -> dict[str, Any]:
    """`M-a`'s slot clause over the valid asks, given as (presentation, pass,
    ranking). `W`: the mean agreement between the two passes of the same
    presentation. `A`: the mean agreement between asks of different
    presentations. Either is None where it has no pair to read."""
    by_p: dict[str, list[Sequence[str]]] = {}
    for pid, _pass, r in asks:
        by_p.setdefault(pid, []).append(r)
    within = [agreement(rs[0], rs[1]) for rs in by_p.values() if len(rs) == 2]
    across = [agreement(x[2], y[2]) for x, y in itertools.combinations(asks, 2)
              if x[0] != y[0]]
    w = statistics.mean(within) if within else None
    a = statistics.mean(across) if across else None
    return {"W": w, "A": a, "gap": None if w is None or a is None else w - a,
            "presentations_with_both_passes": len(within), "pairs_across": len(across)}


def borda(orders: Sequence[Sequence[str]]) -> list[str]:
    """The Borda aggregate of total orders: each queue scores the number of
    queues ranked below it, summed; ties go to the domain's own order."""
    points = Counter({q: 0 for q in plan.QUEUES})
    for o in orders:
        for i, q in enumerate(o):
            points[q] += len(o) - 1 - i
    return sorted(plan.QUEUES, key=lambda q: (-points[q], plan.QUEUES.index(q)))


# ---------------------------------------------------------------------------
# K-b's pairs (M-e)
# ---------------------------------------------------------------------------

def blind_edge_rows(path: Path | None = None) -> list[list[dict]]:
    """The edge rows `results_blind/score.json` stores, one list per run."""
    rec = json.loads((path or plan.BLIND_SCORE).read_text())
    return [run["edge_rows"] for run in rec["runs"]]


def names_for(order: Sequence[str]) -> Callable[[dict], str]:
    """The rule a fixed ranking names on one edge row: `blind.rows.stage_c_names`
    with the ranking as an argument."""
    rank = rank_of(order)

    def name(row: dict) -> str:
        qw, ql = row["queues"]
        return row["winner"] if rank[qw] < rank[ql] else row["loser"]
    return name


def blind_reading(order: Sequence[str] | None, er: list[list[dict]],
                  key: str = "space_out") -> dict[str, Any]:
    """`K-b`'s reading on its own pairs and units, for the rule `order` names;
    with `order=None`, for the declared winner, which is `K-b` itself."""
    return blind_rows.direction(er, key, keep=blind_rows.beyond_the_keyword,
                                predict=None if order is None else names_for(order))


STAGE_C = tuple(STAGE_C_HIERARCHY)
