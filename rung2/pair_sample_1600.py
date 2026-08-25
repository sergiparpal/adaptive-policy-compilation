"""
STAGE A OF PLAN_PROPOSER_1600 — the sample at the budget that discriminates.

--------------------------------------------------------------------------
WHAT THIS IS, AND WHY IT IS NOT A MEASUREMENT
--------------------------------------------------------------------------
`PLAN_PAIRWISE.md` asked its question at 400 pairs, and `results3/FINDINGS3.md`
§10 then showed that at 400 a perfect chooser, a 70%-accurate chooser and a coin
are the same number. `PLAN_PROPOSER_1600.md` goes to the budget where those three
curves separate. This module is its Stage A: it builds the 1,600-pair population
the calls will be spent on, and it checks — **before a cent is spent** — that the
rows §0 signs can be adjudicated on it.

It costs nothing, calls nothing and adjudicates nothing. §6 of the plan says so
in one line and this module repeats it: **it carries no prediction**. `B-a` and
`B-d` are about the proposer's rate on these pairs, which needs the calls; `B-b`
and `B-c` are about the order its answers induce. Nothing in §0 predicts the
sample, the population split, or the oracle's own directions. That check is
written down rather than assumed because `PLAN_PAIRWISE.md` §0.1 records two rows
lost to skipping it: costing no money is not the same as costing no prediction.

--------------------------------------------------------------------------
THE NESTING IS IN THE SAMPLE, NOT IN A SHUFFLE
--------------------------------------------------------------------------
`edge_budget` nests its budgets by shuffling the population once at seed 17 and
taking prefixes. Stage D did **not** use that shuffle: it used
`sample_population`, which is `random.Random(17).sample`. **The two do not
agree** — over this population their first 400 share not one pair — so a budget
curve built on the shuffle says nothing about the 400 that were paid for.

So the extension is built the only way that keeps the two points nested:
**Stage D's 400, plus 1,200 drawn from the 31,450 that are left**, at a seed
declared in the plan and distinct from every seed the closed thread used. Drawing
`k1` uniformly without replacement and then `k2` uniformly from the remainder
gives a subset distributed exactly as one uniform draw of `k1 + k2`, so the union
is a uniform sample of 1,600 on the same population the 400 came from, and the
comparison between the two budgets is nested rather than merely similar.

CORRECTION TO §5.1 OF THE PLAN, 2026-08-25. The plan gives a second reason and
that one is **false at this scale**: it says `random.sample(N, 1600)` is not a
superset of `random.sample(N, 400)`, and over 31,850 pairs under CPython 3.12 it
is — both budgets take the selection-set branch of `random.sample`, they share
one draw stream, and the 400 come out an exact prefix of the 1,600. The
instruction §5.1 gives is still the right one and the load-bearing word in it is
`hoping`: that nesting is an undocumented implementation detail, it disappears as
soon as the two budgets straddle the branch boundary of the setsize heuristic,
and no comparison should rest on it. `tests/test_pair_sample_1600.py` carries the
counterexample and the coincidence side by side. What this module rests on
instead is construction — the complement — and `gate_base_is_a_subset`, which
checks the result rather than trusting the route.

--------------------------------------------------------------------------
TWO BLOCKS, AND WHY THE RECORD IS SPLIT IN TWO
--------------------------------------------------------------------------
`pairs` carries identity only: which two rules, where they sit in the population,
and whether the answer is already paid for. `oracle` carries which of the two
gets more of the shared region right, under both surfaces.

They are separate because **Stage B reads this file**, and `rung2/pair_judgement`
is on the online-loop list of `tests/test_oracle_separation.py`. The plan asks for
one deliverable and this is one deliverable; what the split adds is that the block
the asking path reads cannot carry a verdict, as a property of the record's shape
rather than of anyone's care. `tests/test_pair_sample_1600.py` pins it.

--------------------------------------------------------------------------
WHAT `B-d` NEEDS, AND WHY IT IS CHECKED HERE
--------------------------------------------------------------------------
`B-d` says the proposer's errors fall harder on the pairs a queue ranking cannot
answer than on the ones it can. **A queue ranking cannot answer a queue-pair that
appears with both better-rules**: if the better rule is sometimes the one sending
to X and sometimes the one sending to Y, no fixed ranking of the eight queues gets
both right. Those pairs are the unreachable side; the rest are the reachable one.

The split is a property of the SAMPLE, so it is computable before any call, and
if either side is too thin the row is unadjudicable — which is worth finding out
now rather than after 1,200 calls. The gate is 100 pairs a side and it blocks.

Usage:  PYTHONHASHSEED=0 python3 -m rung2.pair_sample_1600
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung2.pair_judgement import (gate_population, learned_population,
                                  learned_rules)
from rung3.edge_direction import better_over_corpus, better_over_space, verdict
from rung3.order_search import build_tables, load, subsumption_below
from rung3.order_search_ls import space_truth_masks

OUT = Path("results2")
RECORD = "pair_sample_1600.json"
BASE = Path("results2/pair_judgement_learned.json")

# Declared in §6 of PLAN_PROPOSER_1600.md, before the sample existed. Distinct
# from every seed the closed pairwise thread used (17 throughout) so that no
# accident makes the extension share structure with the 400 it extends.
EXTENSION_SEED = 25

TARGET = 1600
N_BASE = 400
MIN_PER_SIDE = 100    # §6: below this, B-d is unadjudicable and this stage says so


# ---------------------------------------------------------------------------
# The extension
# ---------------------------------------------------------------------------

def read_base(path: Path = BASE):
    """Stage D's pairs, in the order its record holds them.

    Orientation is carried, not recomputed: `a_beats_b` means `rule_a` wins, so
    a pair whose two rules swapped places would silently invert every answer
    already paid for.
    """
    rec = json.loads(path.read_text())
    return [(r["rule_a"], r["rule_b"]) for r in rec["answers"]], rec


def extend(pairs, base, budget=TARGET, seed=EXTENSION_SEED):
    """Stage D's pairs plus `budget - len(base)` drawn from the complement.

    The complement is taken in the population's own order and the draw is
    `random.Random(seed).sample` over its indices, so nothing here depends on the
    iteration order of a set. The union is returned in the population's order,
    which is the convention `sample_population` already uses: the record then
    reads the same way whatever the budget.
    """
    held = set(base)
    complement = [p for p in pairs if p not in held]
    k = budget - len(held)
    if k < 0:
        raise ValueError(f"budget {budget} is below the {len(held)} already held")
    picked = set(random.Random(seed).sample(range(len(complement)), k))
    new = {p for j, p in enumerate(complement) if j in picked}
    union = held | new
    return [p for p in pairs if p in union], new


# ---------------------------------------------------------------------------
# The gates, all blocking, all before a call
# ---------------------------------------------------------------------------

def gate_base_is_a_subset(sample, base, pairs):
    """Stage D's 400 survive into the 1,600 with the same orientation."""
    inside = set(sample)
    population = set(pairs)
    missing = [list(p) for p in base if p not in inside]
    inverted = [list(p) for p in base if p not in inside and (p[1], p[0]) in inside]
    off = [list(p) for p in base if p not in population]
    return {
        "what": "every pair Stage D paid for is in the extended sample, with "
                "`rule_a` still first. An inverted pair would silently invert "
                "the answer already held, since `a_beats_b` names rule_a.",
        "n_base": len(base), "n_missing": len(missing),
        "n_inverted": len(inverted), "n_outside_the_population": len(off),
        "missing": missing[:10], "inverted": inverted[:10],
        "passes": not missing and not off and len(base) == N_BASE,
    }


def gate_sample_is_well_formed(sample, base, pairs, budget=TARGET):
    """`budget` distinct pairs, all of them from the population."""
    counts = Counter(sample)
    dupes = [list(p) for p, c in counts.items() if c > 1]
    population = set(pairs)
    held = set(base)
    off = [list(p) for p in sample if p not in population]
    held_in = sum(1 for p in sample if p in held)
    return {
        "what": "the union is exactly `budget` distinct pairs and every one of "
                "them belongs to the population the three conditions define.",
        "n_sample": len(sample), "n_distinct": len(counts),
        "expected": budget,
        "n_from_stage_d": held_in,
        "n_new": len(sample) - held_in,
        "n_duplicated": len(dupes), "n_outside_the_population": len(off),
        "outside": off[:10],
        "passes": (len(sample) == budget and len(counts) == budget
                   and not off),
    }


# ---------------------------------------------------------------------------
# B-d's split — which pairs a queue ranking cannot answer
# ---------------------------------------------------------------------------

def queue_pair_split(rows, key, action):
    """
    Partition the pairs with a strict better rule by whether a fixed ranking of
    the eight queues could get their queue-pair right.

    For each unordered queue-pair, collect which queues the better rule sends to
    across the sample. One queue: a ranking that puts it first gets every one of
    them. Both: no ranking gets both, so those pairs carry information a ranking
    does not have, and `B-d` says the proposer's errors fall harder there.

    The split is computed ON THE SAMPLE and says so: a queue-pair can be constant
    in 1,600 draws and vary in the population. What `B-d` needs is that the two
    sides of THIS sample are both populated, which is what the caller gates on.
    """
    winners = defaultdict(set)
    strict = []
    for r in rows:
        v = r[key]
        if v not in ("a", "b"):
            continue
        qa, qb = action[r["rule_a"]], action[r["rule_b"]]
        winners[tuple(sorted((qa, qb)))].add(qa if v == "a" else qb)
        strict.append(r)
    unreachable = {qp for qp, w in winners.items() if len(w) > 1}
    side = {}
    for r in strict:
        qp = tuple(sorted((action[r["rule_a"]], action[r["rule_b"]])))
        side[(r["rule_a"], r["rule_b"])] = ("unreachable" if qp in unreachable
                                            else "reachable")
    tally = Counter(side.values())
    return {
        "what": "of the pairs with a strict better rule, how many sit on a "
                "queue-pair a fixed ranking of the eight queues cannot answer — "
                "one that appears with BOTH better-rules across this sample.",
        "surface": key,
        "computed_on": "the sample, not the population. A queue-pair constant "
                       "in 1,600 draws can vary in the 31,850.",
        "n_strict": len(strict),
        "n_queue_pairs": len(winners),
        "n_queue_pairs_unreachable": len(unreachable),
        "unreachable_queue_pairs": [" vs ".join(qp)
                                    for qp in sorted(unreachable)],
        "n_reachable": tally["reachable"],
        "n_unreachable": tally["unreachable"],
        "denominator_note":
            "Stage C's own denominators are these minus the pairs the proposer "
            "declines an edge on, which is not known until the calls are made.",
    }, side


def gate_split_populated(split, minimum=MIN_PER_SIDE):
    ok = (split["n_reachable"] >= minimum
          and split["n_unreachable"] >= minimum)
    return {
        "what": f"B-d compares two rates, one per side of the split. Below "
                f"{minimum} pairs a side the row is unadjudicable, and §6 of the "
                f"plan wants that known before a call rather than after 1,200.",
        "surface": split["surface"],
        "minimum_per_side": minimum,
        "n_reachable": split["n_reachable"],
        "n_unreachable": split["n_unreachable"],
        "B_d_adjudicable": ok,
        "passes": ok,
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    t_start = time.time()
    if not BASE.exists():
        print(f"ABORTED: {BASE} is not there. Stage D has not run.")
        return 1

    print("=" * 78)
    print("STAGE A — the 1,600-pair sample, and whether B-d can be adjudicated "
          "on it")
    print("=" * 78)
    print(f"  extension seed {EXTENSION_SEED} · zero API calls · no prediction")
    print(f"  {describe()}")

    space = Space()
    rules = learned_rules()
    pairs, ext, stats = learned_population(rules, space)
    g_pop = gate_population(stats, len(rules))
    action = {rid: rules[rid].action for rid in rules}

    base, base_rec = read_base()
    sample, new = extend(pairs, base)
    g_base = gate_base_is_a_subset(sample, base, pairs)
    g_sample = gate_sample_is_well_formed(sample, base, pairs)

    print()
    print("POPULATION GATE — the three conditions over the 577 rules")
    for k, v in stats.items():
        print(f"  {k:<26}{v:>8}")
    print(f"  {'of the pairs':<26}{g_pop['n_pairs']:>8}   "
          f"population {g_pop['fraction']:.1%}, expected "
          f"{g_pop['expected_population']}"
          f"{'  ok' if g_pop['passes'] else '  NO'}")

    print()
    print("THE EXTENSION")
    print(f"  {'held from Stage D':<26}{len(base):>8}")
    print(f"  {'drawn from the complement':<26}{len(new):>8}   "
          f"at seed {EXTENSION_SEED}")
    print(f"  {'union':<26}{len(sample):>8}")

    if not g_pop["passes"]:
        print("\n  STOP: this is not the population Stage D was budgeted on.")
        return 1
    if not g_base["passes"]:
        print(f"\n  STOP: {g_base['n_missing']} of Stage D's pairs are not in "
              f"the union ({g_base['n_inverted']} inverted).")
        return 1
    if not g_sample["passes"]:
        print(f"\n  STOP: the union is {g_sample['n_distinct']} distinct pairs, "
              f"not {g_sample['expected']}.")
        return 1

    # --- the oracle's own direction, both surfaces -----------------------
    corpus, rule_records, ext_c, conds = load()
    below = subsumption_below(rule_records, ext_c)
    matched, _undef, truth = build_tables(corpus, rule_records, conds, below)
    matched_sets = [set(m) for m in matched]
    tmask = space_truth_masks(space)
    allidx = list(range(len(corpus)))

    held = set(base)
    rows = []
    for k, (a, b) in enumerate(sample):
        wa, wb = better_over_space(a, b, ext, action, tmask)
        ca, cb = better_over_corpus(a, b, matched_sets, truth, action, allidx)
        rows.append({
            "index": k, "rule_a": a, "rule_b": b,
            "space_wins_a": wa, "space_wins_b": wb,
            "better_space": verdict(wa, wb),
            "corpus_wins_a": ca, "corpus_wins_b": cb,
            "better_corpus": verdict(ca, cb),
        })

    census = {k: dict(Counter(r[f"better_{k}"] for r in rows))
              for k in ("space", "corpus")}
    print()
    print("THE ORACLE'S OWN DIRECTION OVER THE 1,600")
    for k, c in census.items():
        print(f"  {k:<8}" + "   ".join(f"{n} {v}" for v, n in sorted(c.items())))

    splits, sides = {}, {}
    for k in ("space", "corpus"):
        splits[k], sides[k] = queue_pair_split(rows, f"better_{k}", action)
    g_split = gate_split_populated(splits["space"])

    print()
    print("B-d's SPLIT — the pairs a free queue ranking cannot answer")
    for k, s in splits.items():
        print(f"  {k:<8}{s['n_unreachable']:>6} unreachable  "
              f"{s['n_reachable']:>6} reachable   of {s['n_strict']} with a "
              f"strict better rule")
        print(f"          {s['n_queue_pairs_unreachable']} of "
              f"{s['n_queue_pairs']} queue-pairs appear with both better-rules")
    print(f"\n  B-d adjudicable on the space definition: "
          f"{g_split['B_d_adjudicable']}   (minimum {MIN_PER_SIDE} a side)")

    for r in rows:
        p = (r["rule_a"], r["rule_b"])
        r["queue_ranking_space"] = sides["space"].get(p)
        r["queue_ranking_corpus"] = sides["corpus"].get(p)

    payload = {
        "_env": environment(extension_seed=EXTENSION_SEED, budget=TARGET,
                            base_record=str(BASE)),
        "what":
            "Stage A of PLAN_PROPOSER_1600.md: Stage D's 400 pairs plus 1,200 "
            "drawn from the complement, and the checks that say the plan's rows "
            "can be adjudicated on the union. Zero API calls.",
        "plan": "PLAN_PROPOSER_1600.md", "stage": "A",
        "carries_no_prediction":
            "nothing in §0 predicts the sample, the population split or the "
            "oracle's own directions. B-a and B-d are about the proposer's rate "
            "on these pairs and B-b and B-c about the order its answers induce; "
            "all four need the calls. This is checked rather than assumed "
            "because PLAN_PAIRWISE.md §0.1 records two rows lost to skipping it.",
        "nesting":
            "Stage D's 400 plus 1,200 drawn uniformly from the remaining "
            "31,450. Drawing k1 without replacement and then k2 from the "
            "remainder distributes the union exactly as one uniform draw of "
            "k1+k2, so the two budgets are nested. It is NOT edge_budget's "
            "shuffle: random.sample(N, 1600) is not a superset of "
            "random.sample(N, 400), and building it that way would break the "
            "nesting the 400-to-1,600 comparison rests on.",
        "the_two_blocks":
            "`pairs` carries identity only and `oracle` carries the verdicts. "
            "Stage B reads `pairs`, and rung2/pair_judgement is on the "
            "online-loop list of tests/test_oracle_separation.py: the block the "
            "asking path reads cannot carry a verdict, by the record's shape.",
        "base_record": str(BASE),
        "base_recorded_at": (base_rec.get("_env") or {}).get("recorded_at"),
        "date_is_not_held_fixed":
            "the 400 were asked on 2026-08-24 against a hosted model that can "
            "change underneath a name. §2 of the plan makes reusing them or "
            "re-asking all 1,600 a decision at signature time; this stage builds "
            "the same population either way and only §7's call list changes.",
        "n_population": len(pairs),
        "n_base": len(base), "n_new": len(new), "n_sample": len(sample),
        "extension_seed": EXTENSION_SEED,
        "gates": {"population": g_pop, "base_is_a_subset": g_base,
                  "sample_is_well_formed": g_sample,
                  "split_populated": g_split},
        "oracle_verdict_census": census,
        "split_for_B_d": splits,
        "pairs": [{"index": r["index"], "rule_a": r["rule_a"],
                   "rule_b": r["rule_b"],
                   "source": "stage_d" if (r["rule_a"], r["rule_b"]) in held
                             else "new"} for r in rows],
        "oracle": [{k: r[k] for k in (
            "index", "rule_a", "rule_b", "space_wins_a", "space_wins_b",
            "better_space", "corpus_wins_a", "corpus_wins_b", "better_corpus",
            "queue_ranking_space", "queue_ranking_corpus")} for r in rows],
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    if not g_split["passes"]:
        print("\n  B-d IS UNADJUDICABLE ON THIS SAMPLE and no call has been "
              "made. Report it; do not spend and do not move the split.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
