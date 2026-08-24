"""
DOES THE PAIRWISE CHANNEL PAY WITH MORE EDGES? The budget curve, for zero calls.

--------------------------------------------------------------------------
WHY IT CAN BE MEASURED WITHOUT SPENDING
--------------------------------------------------------------------------
Stage D bought 400 answers and `results3/FINDINGS3.md` §9 showed the resulting
order was indistinguishable from a coin — **and so was the ORACLE's own direction
on the same 400 pairs**. That is what said the refutation of P-d was about the
budget rather than about the proposer, and it left one question open: whether the
channel pays at all at a budget nobody has paid for.

It does not need paying for. The oracle's direction is computable offline for
**every** one of the 31,850 pairs, so the channel's ceiling as a function of
budget is a free measurement. What is not free is the proposer's own curve beyond
400, and this module does not pretend otherwise: it projects instead, at the
accuracy §9 measured, and labels the projection as one.

--------------------------------------------------------------------------
THE FOUR CURVES
--------------------------------------------------------------------------
`oracle`     every offered pair pointed at the rule that gets more of the shared
             region right. **The ceiling of the channel**, unavailable to any
             proposer, and the only one of the four that is exact.
`noisy`      the same, with each direction flipped independently at the rate §9
             measured the proposer missing. **A projection under a stated
             assumption** — that errors are independent and evenly spread — which
             the real proposer's need not satisfy: Stage C found its accuracy
             varies by queue-pair. It is the shape of the answer, not the answer.
`coin`       direction chosen at random. The null, and its SPREAD matters as much
             as its mean, because at small budgets it is what swamps everything.
`floor`      arrival order, which is where a budget of zero lands.

**The budgets are nested**: the population is shuffled once at seed 17 and every
budget is a prefix of that shuffle, so a larger budget contains the smaller one
and the curve is a curve rather than eight unrelated samples. A prefix of the
population's own order would not do — it is sorted by rule id, so the first 400
pairs are almost all about the same handful of early rules.

**A tie offers no edge.** Where the two rules get the shared region right equally
often the channel has nothing to say, so nothing is declared — the same shape as
the proposer answering with a third queue, which happened 35 times in 400.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No API call, no search, and no signed row moves: P-d and P-e keep the verdicts
`declared_order.json` gave them. **POST-RUN**, like §9: written after both were
adjudicated. The reference lines are READ from the records that own them.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.edge_budget
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung2.pair_judgement import learned_population, learned_rules
from rung3.declared_order import (accepted_from, fresh_engine,
                                  topological_order)
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import space_truth_masks

OUT = Path("results3")
RECORD = "edge_budget.json"

SHUFFLE_SEED = 17
COIN_DRAWS = 10
NOISY_DRAWS = 10
NOISY_SEED = 17
SPLIT_SEED = 17

BUDGETS = (400, 800, 1600, 3200, 6400, 12800, 25600, None)   # None = all

# Read from the records that own them, transcribed here only for the printout.
FLOOR = 0.4332            # floor_by_pool.json, hibrido / corpus_test_split0
QUEUE_HIERARCHY = 0.4824  # queue_hierarchy_floor.json, same cell
P_D_THRESHOLD = 0.4632    # FLOOR + the 0.03 margin §0 signed
MODEL_AT_400 = 0.4080     # declared_order.json
SEARCHED = 0.7678         # order_search_ls.json, hibrido, corpus test SPLIT 0,
                          # best of 65 starts — the same cell as everything
                          # else here, so it is the one landmark that compares
                          # directly rather than only orienting.
SEARCHED_5SPLIT = 0.7734  # the same, as the mean of five splits: what the
                          # record publishes, on a different index set
BOUND = 0.8540            # FINDINGS_AUDIT.md, hibrido, FULL corpus

PROVENANCE = (
    "POST-RUN, like FINDINGS3 §9: written after P-d and P-e were adjudicated. "
    "Nothing here is a bet that could have failed and no signed row moves. The "
    "oracle curve is exact and free; the noisy curve is a PROJECTION at the "
    "accuracy §9 measured, under the assumption that errors are independent and "
    "evenly spread, which the real proposer's need not satisfy.")


# ---------------------------------------------------------------------------

def oracle_directions(pairs, ext, action, tmask):
    """
    True where `a` gets more of `ext(a) & ext(b)` right, False where `b` does,
    None on a tie.

    A tie offers no edge: the channel has nothing to say there, and forcing one
    would credit it with a coin flip it never made.
    """
    out = {}
    for a, b in pairs:
        inter = ext[a] & ext[b]
        wa = (inter & tmask[action[a]]).bit_count()
        wb = (inter & tmask[action[b]]).bit_count()
        out[(a, b)] = True if wa > wb else False if wb > wa else None
    return out


def score_directions(rows, dirs, rules, ids, born, instance, engine):
    """Offered edges → accepted → total order → score. `None` offers nothing."""
    keep = [(r, d) for r, d in zip(rows, dirs) if d is not None]
    edges = accepted_from([r for r, _ in keep], [d for _, d in keep], rules,
                          engine)
    return floor(topological_order(ids, edges, born), instance), len(edges)


def curves(rows, oracle, rules, ids, born, instance, engine, budgets,
           miss_rate):
    """One row per budget: oracle, noisy at the measured accuracy, and coin."""
    out = []
    base = [oracle[(r["rule_a"], r["rule_b"])] for r in rows]
    for budget in budgets:
        n = len(rows) if budget is None else budget
        sub, sub_dirs = rows[:n], base[:n]
        t0 = time.time()
        o_score, o_edges = score_directions(sub, sub_dirs, rules, ids, born,
                                            instance, engine)
        noisy = []
        for k in range(NOISY_DRAWS):
            rnd = random.Random(NOISY_SEED + k)
            flipped = [d if d is None or rnd.random() >= miss_rate else not d
                       for d in sub_dirs]
            noisy.append(score_directions(sub, flipped, rules, ids, born,
                                          instance, engine)[0])
        coins = []
        for k in range(COIN_DRAWS):
            rnd = random.Random(9000 + k)
            coins.append(score_directions(
                sub, [rnd.random() < 0.5 for _ in sub_dirs], rules, ids, born,
                instance, engine)[0])
        out.append({
            "budget": n, "is_whole_population": budget is None,
            "offered": sum(1 for d in sub_dirs if d is not None),
            "ties_offering_nothing": sum(1 for d in sub_dirs if d is None),
            "oracle": round(o_score, 6), "oracle_edges_accepted": o_edges,
            "noisy_mean": round(statistics.mean(noisy), 6),
            "noisy_sd": round(statistics.pstdev(noisy), 6),
            "coin_mean": round(statistics.mean(coins), 6),
            "coin_sd": round(statistics.pstdev(coins), 6),
            "seconds": round(time.time() - t0, 1),
        })
    return out


def crossing(rows, key, line):
    """The smallest budget whose curve is above `line`, or None."""
    for r in rows:
        if r[key] > line:
            return r["budget"]
    return None


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    t_start = time.time()
    miss_rate = None
    src = OUT / "edge_direction.json"
    if src.exists():
        agr = json.loads(src.read_text())["agreement_with_the_better_rule"]
        miss_rate = 1 - agr["space"]["rate"]
    if miss_rate is None:
        print(f"ABORTED: {src} is not there; the projection needs the accuracy "
              f"it measured.")
        return 1

    space = Space()
    rules = learned_rules()
    pairs, ext, stats = learned_population(rules, space)
    action = {r: rules[r].action for r in rules}
    tmask = space_truth_masks(space)
    oracle = oracle_directions(pairs, ext, action, tmask)

    idx = list(range(len(pairs)))
    random.Random(SHUFFLE_SEED).shuffle(idx)
    rows = [{"rule_a": pairs[i][0], "rule_b": pairs[i][1]} for i in idx]

    corpus, rr, ec, conds = load()
    ids = [r["rule_id"] for r in rr]
    born = {r["rule_id"]: r["born_at"] for r in rr}
    act = {r["rule_id"]: r["action"] for r in rr}
    below = subsumption_below(rr, ec)
    _m, undef, truth = build_tables(corpus, rr, conds, below)
    te0 = split(corpus, truth, seed=SPLIT_SEED)[1]
    instance = (*build_masks(ids, undef, truth, act, te0), len(te0))
    engine = fresh_engine(rules)

    print("=" * 78)
    print("DOES THE PAIRWISE CHANNEL PAY WITH MORE EDGES?")
    print("=" * 78)
    print(f"  population {len(pairs):,} · nested at seed {SHUFFLE_SEED} · "
          f"zero API calls")
    print(f"  the noisy curve flips each direction at {miss_rate:.4f}, the rate "
          f"FINDINGS3 §9 measured")
    print("  POST-RUN: written after P-d and P-e were adjudicated")
    print(f"  {describe()}")

    rowsout = curves(rows, oracle, rules, ids, born, instance, engine, BUDGETS,
                     miss_rate)

    print()
    print(f"  {'budget':>8}{'edges':>8}{'oracle':>10}{'noisy':>10}{'coin':>10}"
          f"{'coin sd':>10}")
    for r in rowsout:
        print(f"  {r['budget']:>8}{r['oracle_edges_accepted']:>8}"
              f"{r['oracle']:>10.4f}{r['noisy_mean']:>10.4f}"
              f"{r['coin_mean']:>10.4f}{r['coin_sd']:>10.4f}")
    print("\n  reference lines, hibrido / corpus test split 0 unless said:")
    print(f"    born_at floor (budget zero)          {FLOOR:.4f}")
    print(f"    the model at 400                     {MODEL_AT_400:.4f}")
    print(f"    P-d's threshold                      {P_D_THRESHOLD:.4f}")
    print(f"    a free queue ranking                 {QUEUE_HIERARCHY:.4f}")
    print(f"    searched order, SAME cell, best of 65 {SEARCHED:.4f}")
    print(f"    the same as the mean of 5 splits      {SEARCHED_5SPLIT:.4f}")
    print(f"    coverage bound (FULL corpus)         {BOUND:.4f}")

    cross = {
        "oracle_over_P_d_threshold": crossing(rowsout, "oracle", P_D_THRESHOLD),
        "oracle_over_the_queue_ranking": crossing(rowsout, "oracle",
                                                  QUEUE_HIERARCHY),
        "noisy_over_P_d_threshold": crossing(rowsout, "noisy_mean",
                                             P_D_THRESHOLD),
        "noisy_over_the_queue_ranking": crossing(rowsout, "noisy_mean",
                                                 QUEUE_HIERARCHY),
    }
    print()
    for k, v in cross.items():
        print(f"  first budget with {k:<34}{v}")

    payload = {
        "_env": environment(shuffle_seed=SHUFFLE_SEED, coin_draws=COIN_DRAWS,
                            noisy_draws=NOISY_DRAWS, noisy_seed=NOISY_SEED),
        "what": "the pairwise channel's score as a function of how many pairs "
                "are asked about, on the hibrido pool at corpus test split 0. "
                "The oracle curve is exact and costs nothing; the noisy one is a "
                "projection at the accuracy FINDINGS3 §9 measured.",
        "provenance": PROVENANCE,
        "the_projection_is_not_a_measurement":
            "the noisy curve flips each direction independently at the measured "
            "miss rate. Stage C found the proposer's accuracy varies by "
            "queue-pair, so its errors are neither independent nor evenly "
            "spread, and the curve is the SHAPE of the answer rather than the "
            "answer. Measuring the proposer's own curve beyond 400 needs calls.",
        "nesting": f"the population is shuffled once at seed {SHUFFLE_SEED} and "
                   "every budget is a prefix of that shuffle, so a larger budget "
                   "contains the smaller. A prefix of the population's own order "
                   "would be sorted by rule id and would sample almost the same "
                   "handful of early rules.",
        "ties": "a tie offers no edge — the channel has nothing to say there, "
                "and forcing one would credit it with a coin flip it never made.",
        "surface": "hibrido pool, corpus test split 0 — P-d's own cell",
        "n_population": len(pairs), "miss_rate_used": round(miss_rate, 4),
        "reference_lines": {
            "born_at_floor": FLOOR, "model_at_400": MODEL_AT_400,
            "P_d_threshold": P_D_THRESHOLD, "queue_ranking": QUEUE_HIERARCHY,
            "searched_order_same_cell": SEARCHED,
            "searched_order_5split_mean": SEARCHED_5SPLIT,
            "coverage_bound": BOUND,
            "note": "searched_order_same_cell is hibrido, corpus test split 0, "
                    "best of 65 starts — the SAME cell as every curve here, so "
                    "it compares directly. The five-split mean is what the "
                    "record publishes and sits on another index set. The bound "
                    "is over the FULL corpus and orients rather than compares.",
        },
        "curves": rowsout,
        "crossings": cross,
        "reaches_the_searched_order": {
            "what": "whether an exhausted pairwise channel gets where search "
                    "does, on the same cell. It does not, and the gap is the "
                    "size of the finding.",
            "searched_same_cell": SEARCHED,
            "oracle_at_full_budget": rowsout[-1]["oracle"],
            "gap_oracle": round(SEARCHED - rowsout[-1]["oracle"], 6),
            "noisy_at_full_budget": rowsout[-1]["noisy_mean"],
            "gap_noisy": round(SEARCHED - rowsout[-1]["noisy_mean"], 6),
        },
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
