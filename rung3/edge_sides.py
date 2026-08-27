"""
WHAT DO THE INFORMATIVE EDGES BUY? The order, decomposed by B-d's split.

--------------------------------------------------------------------------
PROVENANCE, FIRST
--------------------------------------------------------------------------
**POST-RUN**, like §9 and §10 of `results3/FINDINGS3.md` and for the same reason:
written after `B-a` to `B-d` were adjudicated, by someone who had already seen
`B-d` hold at 0.6391 against 0.8647. **Nothing here is a bet that could have
failed and no signed row moves.** It adjudicates nothing, it spends nothing, and
it is reported beside `PLAN_PROPOSER_1600.md`'s rows rather than among them.

--------------------------------------------------------------------------
THE QUESTION §11 LEFT AND THIS ANSWERS
--------------------------------------------------------------------------
`B-d` measured the proposer's direction RATE on each side of the split: 0.8647 on
the pairs a fixed ranking of the eight queues can already answer, 0.6391 on the
ones it cannot. `B-b` measured what all 1,310 accepted edges compile into: 0.4804,
level with the free ranking.

Neither says **what each side buys**. A rate is not a score: the reachable side
could be carrying the entire order and the unreachable side none of it, or the
reverse, and `B-b` would read the same either way. That is the decomposition here,
and it is free because the answers are already paid for.

  `reachable`    pairs whose queue-pair appears with ONE better-rule across the
                 sample. A ranking that puts that queue first gets all of them,
                 so an edge here tells the order something a free baseline knows.
  `unreachable`  pairs whose queue-pair appears with BOTH. No fixed ranking gets
                 both, so these are the only edges that can carry what a ranking
                 cannot — and they are where B-d says the proposer is worst.
  `no_side`      no strict better rule: a tie, or neither rule ever right. The
                 material problem, outside every denominator of §0 and kept here
                 only so the three subsets sum to the whole.

--------------------------------------------------------------------------
THE CONTROL THAT MAKES IT READABLE
--------------------------------------------------------------------------
**A subset with more edges scores higher for having more edges.** 654 edges and
451 edges do not start level, so comparing their two scores directly would measure
the split's sizes and call it the proposer's competence.

So each subset is read against **its own coin**: the same rows, the same
compilation, the same scoring, with only the DIRECTION randomised — `N_DRAWS` of
them. What the subset is worth is its distance from that, in that coin's own
deviations, and a subset that lands on its coin bought nothing however high its
raw score. Each is also read against **its own oracle**, every direction pointed
at the rule that gets more of the shared region right, which is the ceiling
available to any proposer on those rows.

**Each subset is compiled independently, through a fresh engine.** Whether an edge
closes a cycle depends on the ones already in, so the edges a subset yields alone
are not the subset of the edges the whole run yielded. Compiling it alone is the
honest reading of *what these edges would have produced by themselves*, and the
record publishes both counts.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.edge_sides
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung2.pair_judgement import learned_rules
from rung3.declared_order import (accepted_from, fresh_engine,
                                  topological_order)
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.order_search import build_tables, load, split, subsumption_below

OUT = Path("results3")
RECORD = "edge_sides.json"
SOURCE = Path("results2/pair_judgement_1600.json")
SPLIT = Path("results2/pair_sample_1600.json")

# Declared here, before any figure of this module exists. 200 is what
# `declared_order.READING_DRAWS` uses for the same job on the same sample, so the
# two records' deviations are the same kind of quantity.
N_DRAWS = 200
SEED = 17
SPLIT_SEED = 17
SIDES = ("reachable", "unreachable", "no_side")

PROVENANCE = (
    "POST-RUN: written after B-a to B-d were adjudicated, by someone who had "
    "already seen B-d hold. Nothing here is a bet that could have failed, no "
    "signed row moves, and it adjudicates nothing. Zero API calls.")


def sides_of(split_path=SPLIT, key="queue_ranking_space"):
    """`{(a, b): side}` from the Stage A record — read, never recomputed."""
    rec = json.loads(Path(split_path).read_text())
    return {(r["rule_a"], r["rule_b"]): (r[key] or "no_side")
            for r in rec["oracle"]}


def oracle_of(split_path=SPLIT, key="better_space"):
    """`{(a, b): True | False | None}`, the better rule as Stage A recorded it."""
    rec = json.loads(Path(split_path).read_text())
    out = {}
    for r in rec["oracle"]:
        v = r[key]
        out[(r["rule_a"], r["rule_b"])] = (True if v == "a" else
                                           False if v == "b" else None)
    return out


def score_of(rows, dirs, rules, ids, born, instance, engine):
    """Rows whose direction is None offer nothing; the rest are compiled."""
    keep = [(r, d) for r, d in zip(rows, dirs) if d is not None]
    edges = accepted_from([r for r, _ in keep], [d for _, d in keep], rules,
                          engine)
    return floor(topological_order(ids, edges, born), instance), len(edges)


def subset_report(rows, oracle, rules, ids, born, instance, engine,
                  n_draws=N_DRAWS, seed=SEED):
    """One side: the model, its own coin, its own oracle, and the distance."""
    model = [r["declared"] == "a_beats_b" for r in rows]
    m_score, m_edges = score_of(rows, model, rules, ids, born, instance, engine)

    draws = []
    for k in range(n_draws):
        rnd = random.Random(seed + k)
        draws.append(score_of(rows, [rnd.random() < 0.5 for _ in rows], rules,
                              ids, born, instance, engine)[0])
    mean, sd = statistics.mean(draws), statistics.pstdev(draws)

    o_dirs = [oracle[(r["rule_a"], r["rule_b"])] for r in rows]
    o_score, o_edges = score_of(rows, o_dirs, rules, ids, born, instance, engine)
    return {
        "n_rows": len(rows),
        "model": round(m_score, 6), "model_edges_accepted": m_edges,
        "coin": {"mean": round(mean, 6), "sd": round(sd, 6),
                 "min": round(min(draws), 6), "max": round(max(draws), 6)},
        "model_minus_coin": round(m_score - mean, 6),
        "model_in_coin_deviations": round((m_score - mean) / sd, 2) if sd else None,
        "oracle": round(o_score, 6), "oracle_edges_accepted": o_edges,
        "oracle_offers": sum(1 for d in o_dirs if d is not None),
        "oracle_in_coin_deviations": round((o_score - mean) / sd, 2) if sd else None,
        "headroom_model_to_oracle": round(o_score - m_score, 6),
    }


def main(argv=None) -> int:
    t_start = time.time()
    if not SOURCE.exists() or not SPLIT.exists():
        print(f"ABORTED: {SOURCE} or {SPLIT} is not there.")
        return 1
    rows_all = [r for r in json.loads(SOURCE.read_text())["answers"]
                if r["declared"] != "none"]
    side, oracle = sides_of(), oracle_of()

    corpus, rr, ec, conds = load()
    ids = [r["rule_id"] for r in rr]
    born = {r["rule_id"]: r["born_at"] for r in rr}
    act = {r["rule_id"]: r["action"] for r in rr}
    below = subsumption_below(rr, ec)
    _m, undef, truth = build_tables(corpus, rr, conds, below)
    te0 = split(corpus, truth, seed=SPLIT_SEED)[1]
    instance = (*build_masks(ids, undef, truth, act, te0), len(te0))
    rules = learned_rules()
    engine = fresh_engine(rules)
    floor_born = floor(sorted(ids, key=lambda r: born[r]), instance)

    print("=" * 78)
    print("WHAT DO THE INFORMATIVE EDGES BUY? The order, split by B-d's sides")
    print("=" * 78)
    print(f"  {len(rows_all)} declared edges · hibrido, corpus test split 0 · "
          f"zero API calls")
    print("  POST-RUN: written after B-a to B-d were adjudicated")
    print(f"  {describe()}")

    groups = {s: [r for r in rows_all
                  if side.get((r["rule_a"], r["rule_b"]), "no_side") == s]
              for s in SIDES}
    groups["all"] = rows_all

    out = {}
    for name in (*SIDES, "all"):
        out[name] = subset_report(groups[name], oracle, rules, ids, born,
                                  instance, engine)

    print()
    print(f"  {'side':<13}{'rows':>6}{'edges':>7}{'model':>9}{'coin':>9}"
          f"{'sd':>8}{'devs':>7}{'oracle':>9}{'o devs':>8}")
    for name in (*SIDES, "all"):
        r = out[name]
        print(f"  {name:<13}{r['n_rows']:>6}{r['model_edges_accepted']:>7}"
              f"{r['model']:>9.4f}{r['coin']['mean']:>9.4f}{r['coin']['sd']:>8.4f}"
              f"{r['model_in_coin_deviations']:>+7.2f}{r['oracle']:>9.4f}"
              f"{r['oracle_in_coin_deviations']:>+8.2f}")
    print(f"  {'born_at floor':<13}{'':>6}{'':>7}{floor_born:>9.4f}")

    payload = {
        "_env": environment(n_draws=N_DRAWS, seed=SEED),
        "what": "the 1,600-pair run's declared edges split by whether a fixed "
                "queue ranking could answer their queue-pair, each subset "
                "compiled and scored on its own against its own coin and its own "
                "oracle. Reads answers already paid for; zero API calls.",
        "provenance": PROVENANCE,
        "adjudicates_nothing":
            "no row of PLAN_PROPOSER_1600.md is read here and none moves. B-d "
            "measured the RATE on each side; this measures what each side's "
            "edges BUY, which is a different quantity and carries no band.",
        "surface": "hibrido pool, corpus test split 0 — B-b's own cell",
        "the_split": "read from results2/pair_sample_1600.json, fixed and gated "
                     "before any call was made, never recomputed from answers.",
        "why_each_subset_has_its_own_coin":
            "a subset with more edges scores higher for having more edges. "
            "Comparing two sides' raw scores would measure the split's sizes. "
            "Each is read against the same rows with only the direction "
            "randomised, so what it is worth is its distance from that.",
        "compiled_independently":
            "whether an edge closes a cycle depends on the edges already in, so "
            "the edges a subset yields ALONE are not the subset of the edges the "
            "whole run yielded. Both counts are published.",
        "source": str(SOURCE), "split": str(SPLIT),
        "born_at_floor": round(floor_born, 6),
        "n_declared_edges": len(rows_all),
        "by_side": out,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
