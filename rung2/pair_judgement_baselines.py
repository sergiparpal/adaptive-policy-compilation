"""
WHAT THE STAGE C RATE IS MADE OF — the baseline that reads no rule at all.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Stage C asked a model, 170 times, which queue a ticket goes to when two rules
that both match it disagree. It answered correctly 150 times: **0.8824** over
all 170, `neither` counting as a failure, the rate §0 adjudicates P-c on.

This asks the question `ARBITRATION_REPORT.md` turned into a rule of thumb after
`keep_k(k=4)` beat the hidden policy under specificity arbitration: **what does a
baseline that ignores the material score?** Here the dumbest available baseline
is a **fixed total order over the eight queues** — answer with the higher-ranked
of the two queues on offer, never reading a condition, a ticket or a rule.

It is a property of the benchmark, not of the model, and it costs nothing: it
reads `results2/pair_judgement_hidden.json` and calls no API.

--------------------------------------------------------------------------
THE BASELINE IS A WORLD RECORD, AND IT IS LABELLED AS ONE
--------------------------------------------------------------------------
The order is chosen by brute force over all **40,320** permutations of the eight
queues, **with the answer key in hand**. Nothing without labels could pick it.
That makes it the same kind of object as the best of 65 starts in
`PLAN_PAIRWISE.md` §2 — a winning ticket, not a level — and it is reported with
the whole distribution beside it so the ticket cannot be read as a floor.

What it can legitimately say is an upper bound on how much of the benchmark is
*decidable without the rules*. That bound is the point.

--------------------------------------------------------------------------
THE DECOMPOSITION, WHICH IS THE ACTUAL FINDING
--------------------------------------------------------------------------
Split the 170 by whether the best fixed hierarchy gets them right, and score the
model inside each half. The half the hierarchy cannot reach is the half where
priority genuinely lives in the RULES rather than in the queues: the same two
queues appear with opposite winners, so no ordering of queues can serve both.

`reversible_queue_pairs` names them. They are the only pairs in this benchmark
that a queue hierarchy is structurally unable to answer, and they are therefore
the only ones where a high rate is evidence about pairwise judgement.

--------------------------------------------------------------------------
AND WHETHER THE MODEL IS ONE
--------------------------------------------------------------------------
Separately: is the model itself applying a fixed hierarchy? If for every pair of
queues it always returned the same one, it would be — whatever it wrote in
`why`. `model_consistency` counts the queue-pairs where its answer is not
constant. A model that varies is reading something; whether it reads it well is
the decomposition's question, not this one.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It rewrites nothing. `pair_judgement_hidden.json` cost money and is read-only
here. It adjudicates no row: P-c was adjudicated on the rate that record
publishes, under the denominator §0 named before the run, and nothing here moves
it. What it changes is the READING, which is what a baseline is for.

Usage:  PYTHONHASHSEED=0 python3 -m rung2.pair_judgement_baselines
"""

from __future__ import annotations

import itertools
import json
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from harness.provenance import describe, environment

OUT = Path("results2")
SOURCE = OUT / "pair_judgement_hidden.json"
RECORD = "pair_judgement_baselines.json"


# ---------------------------------------------------------------------------
# The baseline
# ---------------------------------------------------------------------------

def queues_of(rows):
    return sorted({r["winner_action"] for r in rows}
                  | {r["loser_action"] for r in rows})


def score_hierarchy(rank, rows):
    """A fixed order over the queues answers with the higher-ranked of the two.

    It reads neither rule, neither ticket and no condition — only which two
    queues are on offer.
    """
    return sum(1 for r in rows
               if rank[r["winner_action"]] < rank[r["loser_action"]])


def all_hierarchies(rows):
    """Every permutation of the queues, scored. Returns (best, scores).

    The best is chosen WITH THE KEY, so the distribution travels with it: a
    maximum over 40,320 draws is not a level, and the mean is what says how far
    the ticket sits from one.
    """
    queues = queues_of(rows)
    scores, best, best_order = [], -1, None
    for perm in itertools.permutations(queues):
        rank = {a: i for i, a in enumerate(perm)}
        s = score_hierarchy(rank, rows)
        scores.append(s)
        if s > best:
            best, best_order = s, perm
    return {"n_queues": len(queues), "n_orders": len(scores),
            "best": best, "best_order": list(best_order),
            "best_rate": round(best / len(rows), 4),
            "mean": round(statistics.mean(scores) / len(rows), 4),
            "median": round(statistics.median(scores) / len(rows), 4),
            "min_rate": round(min(scores) / len(rows), 4),
            "sd": round(statistics.pstdev(scores) / len(rows), 4)}, best_order


# ---------------------------------------------------------------------------
# Where a hierarchy cannot reach
# ---------------------------------------------------------------------------

def reversible_queue_pairs(rows):
    """
    Unordered queue-pairs that appear with BOTH winners.

    No total order over the queues can answer both directions, so these are the
    pairs where priority is a fact about the two rules and not about the two
    queues. They are the only ones in this benchmark where a correct answer is
    evidence about pairwise judgement rather than about knowing the hierarchy.
    """
    seen = defaultdict(set)
    for r in rows:
        key = tuple(sorted((r["winner_action"], r["loser_action"])))
        seen[key].add(r["winner_action"])
    both = {k: sorted(v) for k, v in seen.items() if len(v) == 2}
    n_rows = sum(1 for r in rows
                 if tuple(sorted((r["winner_action"], r["loser_action"])))
                 in both)
    return {"what": "queue-pairs seen with both winners. No fixed order over "
                    "the queues can serve both directions, so these carry "
                    "whatever priority is not in the queue hierarchy.",
            "n_queue_pairs": len(both),
            "queue_pairs": [list(k) for k in sorted(both)],
            "n_rule_pairs_involved": n_rows}


def decomposition(rows, rank):
    """The model's rate inside each half of the hierarchy's split."""
    cells = Counter()
    unreachable = []
    for r in rows:
        h = rank[r["winner_action"]] < rank[r["loser_action"]]
        m = r["outcome"] == "correct"
        cells[(h, m)] += 1
        if not h:
            unreachable.append({
                "winner": r["winner"], "loser": r["loser"],
                "winner_action": r["winner_action"],
                "loser_action": r["loser_action"],
                "model": r["outcome"],
            })
    hit = cells[(True, True)] + cells[(True, False)]
    miss = cells[(False, True)] + cells[(False, False)]
    return {
        "what": "the 170 split by whether the BEST fixed queue hierarchy answers "
                "them, with the model scored inside each half. The second half "
                "is the part of the benchmark no queue ordering can reach.",
        "where_the_hierarchy_is_right": {
            "n": hit, "model_correct": cells[(True, True)],
            "model_rate": round(cells[(True, True)] / hit, 4) if hit else None},
        "where_the_hierarchy_is_wrong": {
            "n": miss, "model_correct": cells[(False, True)],
            "model_rate": round(cells[(False, True)] / miss, 4) if miss else None,
            "coin": 0.5,
            "pairs": unreachable},
    }


# ---------------------------------------------------------------------------
# Is the model a hierarchy?
# ---------------------------------------------------------------------------

def model_consistency(rows):
    """
    Queue-pairs on which the model's answer is not constant.

    If it were constant everywhere the model would BE a fixed hierarchy,
    whatever it wrote in `why`, and the decomposition would be the whole story.
    Rows with no parsed answer are excluded — they are not a disagreement, they
    are an absence — and their count is reported.
    """
    byp = defaultdict(list)
    unanswered = 0
    for r in rows:
        if r["answer"] is None:
            unanswered += 1
            continue
        byp[tuple(sorted((r["winner_action"], r["loser_action"])))].append(
            r["answer"])
    varying = {k: dict(Counter(v)) for k, v in byp.items() if len(set(v)) > 1}
    return {
        "what": "queue-pairs where the model did not always answer the same "
                "queue. A model constant on all of them would be a fixed "
                "hierarchy under another name.",
        "n_queue_pairs_answered": len(byp),
        "n_varying": len(varying),
        "varying": {" vs ".join(k): v for k, v in sorted(varying.items())},
        "unanswered_rows": unanswered,
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    t_start = time.time()
    if not SOURCE.exists():
        print(f"ABORTED: {SOURCE} is not there. Stage C has not run.")
        return 1
    src = json.loads(SOURCE.read_text())
    rows = src["answers"]
    n = len(rows)

    print("=" * 78)
    print("WHAT THE STAGE C RATE IS MADE OF")
    print("=" * 78)
    print(f"  {n} rule-pairs · read from {SOURCE} · zero API calls")
    print(f"  {describe()}")

    hier, best_order = all_hierarchies(rows)
    rank = {a: i for i, a in enumerate(best_order)}
    dec = decomposition(rows, rank)
    rev = reversible_queue_pairs(rows)
    cons = model_consistency(rows)
    model_rate = src["rates"]["over_all_pairs"]["value"]

    print()
    print("THE BASELINE THAT READS NO RULE")
    print(f"  best fixed queue hierarchy, chosen WITH the key over "
          f"{hier['n_orders']:,} orders")
    print(f"    {hier['best']}/{n} = {hier['best_rate']}")
    print(f"    {' > '.join(hier['best_order'])}")
    print(f"  the same {hier['n_orders']:,} orders: mean {hier['mean']}, "
          f"median {hier['median']}, sd {hier['sd']}, worst {hier['min_rate']}")
    print(f"  the model, shown both rules and the ticket: {model_rate}")

    a = dec["where_the_hierarchy_is_right"]
    b = dec["where_the_hierarchy_is_wrong"]
    print()
    print("THE DECOMPOSITION")
    print(f"  where the hierarchy is right   n={a['n']:<5}model "
          f"{a['model_correct']}/{a['n']} = {a['model_rate']}")
    print(f"  where the hierarchy is wrong   n={b['n']:<5}model "
          f"{b['model_correct']}/{b['n']} = {b['model_rate']}   "
          f"(a coin is {b['coin']})")
    print(f"  queue-pairs seen with both winners: {rev['n_queue_pairs']}, "
          f"covering {rev['n_rule_pairs_involved']} rule-pairs")
    print()
    print(f"  the model is NOT a fixed hierarchy: it varies on "
          f"{cons['n_varying']} of {cons['n_queue_pairs_answered']} queue-pairs")

    payload = {
        "_env": environment(n_rule_pairs=n),
        "what":
            "what the Stage C rate is made of. A fixed total order over the "
            "eight queues answers with the higher-ranked of the two on offer, "
            "reading no rule, no ticket and no condition. This scores every one "
            "of the 40,320 such orders against the same 170 pairs, splits the "
            "benchmark by whether the best of them is right, and scores the "
            "model inside each half.",
        "source": str(SOURCE),
        "reads_only": "results2/pair_judgement_hidden.json. Nothing is rewritten "
                      "and no API call is made. It adjudicates no row: P-c was "
                      "adjudicated on the rate that record publishes, under the "
                      "denominator §0 named before the run. What this changes is "
                      "the reading.",
        "denominator": "all 170 pairs asked, `neither` counting as a failure — "
                       "the same denominator the model's rate uses, so the two "
                       "are comparable.",
        "the_baseline_is_a_world_record":
            "the order is chosen by brute force over all 40,320 permutations "
            "WITH the answer key in hand. Nothing without labels could pick it, "
            "so it is a winning ticket and not a level — the same object as the "
            "best of 65 starts in PLAN_PAIRWISE.md §2. The whole distribution is "
            "published beside it for that reason. What it legitimately bounds is "
            "how much of this benchmark is decidable WITHOUT the rules.",
        "n_rule_pairs": n,
        "model_rate_over_all_pairs": model_rate,
        "hierarchy": hier,
        "decomposition": dec,
        "reversible_queue_pairs": rev,
        "model_consistency": cons,
        "seconds": round(time.time() - t_start, 1),
    }
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
