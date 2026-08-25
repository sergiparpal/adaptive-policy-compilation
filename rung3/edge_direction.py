"""
DOES THE DECLARED DIRECTION POINT THE WRONG WAY, AND WOULD THE RIGHT WAY HELP?

--------------------------------------------------------------------------
PROVENANCE, FIRST, BECAUSE IT IS NOT A PRE-REGISTERED MEASUREMENT
--------------------------------------------------------------------------
This was written AFTER P-d and P-e were adjudicated and refuted, by someone who
had already seen the direction control land 0.96 deviations below a coin. Nothing
here is a bet that could have failed and no signed row is touched: P-d and P-e
keep the verdicts `results3/declared_order.json` gave them. What this can be
worth is that the primitive is exact and the two controls are blocking.

`PLAN_PAIRWISE.md` §10 says *there is no truth for these pairs*, and about the
object it means — the hidden policy's LAYER ORDER over rules it never wrote —
that is right and stays right. This measures a different object, and says so on
every line: **over the region where two rules compete, which of them gets more of
it right.** That is not a layer relation and it is not what P-d was about. It is
computable offline, it costs nothing, and it is the only thing that can turn "the
signal has the wrong sign" from a sign into a measurement.

--------------------------------------------------------------------------
THE PRIMITIVE
--------------------------------------------------------------------------
For a pair (A, B) whose extensions overlap and whose actions differ, over the
cases in `ext(A) & ext(B)`:

    wins_A = cases whose TRUE action is A's
    wins_B = cases whose TRUE action is B's

The **better** rule is the one with more; equal counts are a tie and go outside
every denominator. So do pairs where both are zero — there the truth over the
whole shared region is some third queue, which is the material problem showing up
again and not a judgement anyone got wrong.

**Two surfaces and both are reported.** Over the exhaustive space every case
counts once; over the corpus they count as often as they arrive. They do not have
to agree, and where they disagree the record says so rather than picking one.

--------------------------------------------------------------------------
THE THREE QUESTIONS
--------------------------------------------------------------------------
1. **Is the sign really inverted?** Of the declared edges on pairs with a strict
   better rule, what fraction point at it. Against 0.50, with `n` around 300 the
   standard error is about 0.03, so this can separate 0.45 from a coin where the
   order-level control could not.

2. **Would the right direction have helped?** The same 400 pairs with every edge
   pointing at the better rule, compiled and scored exactly as the run's were.
   This is the **ceiling of the channel at this budget** — and it is the control
   that decides whose failure the refutation is. If the oracle's own directions
   also land near the floor, the model's choices were never the story.

3. **How far below a coin is the run, sharply?** The order-level control used 50
   draws because that is what every random baseline in this repository uses. The
   same null with more draws costs seconds and gives the run a rank rather than a
   deviation count.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It spends nothing and rewrites nothing. It adjudicates no row. It does not import
the oracle by name: the per-class space masks come from
`order_search_ls.space_truth_masks`, which exists for exactly this and is on the
allowlist, and the corpus labels come through `order_search.build_tables`.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.edge_direction
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung2.pair_judgement import learned_rules
from rung3.declared_order import (accepted_from, fresh_engine,
                                  topological_order)
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import space_truth_masks

OUT = Path("results3")
RECORD = "edge_direction.json"
SOURCE = Path("results2/pair_judgement_learned.json")

N_NULL_DRAWS = 2000
NULL_SEED = 17
SPLIT_SEED = 17


def parse_source(argv):
    """
    `--source` names the answers, `--out` the record, `--split` the pre-call
    partition `B-d` is a claim about.

    Source and out come as a pair for the reason `declared_order.parse_source`
    gives: `results3/edge_direction.json` is the closed thread's record and no
    other population may land on it by omission.

    `--split` is separate and optional because it is not a scoring choice. The
    partition is computed BEFORE any call, by `rung2.pair_sample_1600`, and read
    here rather than recomputed: a split derived from the answers afterwards
    would be free to move with them, and `B-d` would stop being a prediction.
    """
    # `split_path`, not `split`: this module imports `order_search.split`, which
    # is the train/test partition of the corpus and has nothing to do with B-d's.
    source, split_path = SOURCE, None
    out = OUT / RECORD
    if "--source" in argv:
        source = Path(argv[argv.index("--source") + 1])
    if "--split" in argv:
        split_path = Path(argv[argv.index("--split") + 1])
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    elif source != SOURCE:
        raise SystemExit(
            f"\nABORTED: --source {source} without --out.\n\n"
            f"  {OUT / RECORD} belongs to the 400 pairs of Stage D. Another "
            f"population\n  needs another destination:\n\n"
            f"    --out {OUT}/edge_direction_1600.json\n")
    return source, out, split_path


PROVENANCE = (
    "POST-RUN measurement, written after P-d and P-e were adjudicated and by "
    "someone who had already seen the direction control. Nothing here is a bet "
    "that could have failed and no signed row moves. PLAN_PAIRWISE.md §10's "
    "`there is no truth for these pairs` is about the hidden policy's LAYER "
    "ORDER over rules it never wrote, and stays true; this measures a different "
    "object — which of two competing rules gets more of their shared region "
    "right — and never calls it a layer relation.")


# ---------------------------------------------------------------------------
# The primitive
# ---------------------------------------------------------------------------

def better_over_space(a, b, ext, action, tmask):
    """(wins_a, wins_b) over `ext(a) & ext(b)`, every case counted once."""
    inter = ext[a] & ext[b]
    return ((inter & tmask[action[a]]).bit_count(),
            (inter & tmask[action[b]]).bit_count())


def better_over_corpus(a, b, matched_sets, truth, action, idxs):
    """The same, counted as often as the cases arrive."""
    wa = wb = 0
    for i in idxs:
        s = matched_sets[i]
        if a in s and b in s:
            if truth[i] == action[a]:
                wa += 1
            elif truth[i] == action[b]:
                wb += 1
    return wa, wb


def verdict(wa, wb):
    if wa == 0 and wb == 0:
        return "neither_ever_right"
    if wa > wb:
        return "a"
    if wb > wa:
        return "b"
    return "tie"


# ---------------------------------------------------------------------------
# Question 1 — does the declared direction point at the better rule?
# ---------------------------------------------------------------------------

def agreement(rows, key):
    """
    Of the declared edges on pairs with a STRICT better rule, how many point at
    it.

    Ties and pairs where neither rule is ever right are outside the denominator
    and counted apart: the first is not a judgement anyone can get wrong, and the
    second is the material problem, not a direction error.
    """
    hit = miss = 0
    apart = Counter()
    for r in rows:
        v = r[key]
        if v in ("tie", "neither_ever_right"):
            apart[v] += 1
            continue
        if r["declared"] == "none":
            apart["no_edge"] += 1
            continue
        pointed = "a" if r["declared"] == "a_beats_b" else "b"
        if pointed == v:
            hit += 1
        else:
            miss += 1
    n = hit + miss
    rate = hit / n if n else None
    se = (0.25 / n) ** 0.5 if n else None
    return {
        "what": "of the declared edges on pairs where one rule is strictly "
                "better over the shared region, the fraction pointing at it. "
                "0.50 is a coin; below it means the direction carries signal "
                "with the wrong sign.",
        "surface": key,
        "n": n, "pointed_at_the_better_rule": hit, "pointed_away": miss,
        "rate": round(rate, 4) if rate is not None else None,
        "standard_error": round(se, 4) if se else None,
        "deviations_from_a_coin": round((rate - 0.5) / se, 3) if se else None,
        "outside_the_denominator": dict(apart),
    }


# ---------------------------------------------------------------------------
# B-d — where the errors fall
# ---------------------------------------------------------------------------

def read_split(path, key):
    """
    `{(a, b): "reachable" | "unreachable"}` from the Stage A record.

    Read, not recomputed. The partition is a property of the SAMPLE and of the
    oracle, both fixed before a call was made and both gated there; deriving it
    again from the answers would let it move with the thing it is supposed to
    predict.
    """
    rec = json.loads(Path(path).read_text())
    field = {"better_space": "queue_ranking_space",
             "better_corpus": "queue_ranking_corpus"}[key]
    return {(r["rule_a"], r["rule_b"]): r[field] for r in rec["oracle"]
            if r[field] is not None}


def agreement_by_side(rows, key, side):
    """
    `B-d`: the same rate as `agreement`, on each side of the split, each with
    its own `n`.

    The two sides are scored by calling `agreement` rather than by a second
    implementation of it, so a difference between them is a difference in the
    pairs and not in the arithmetic.

    A pair with no side is one with no strict better rule — a tie or the material
    problem — and `agreement` already puts those outside every denominator, so
    the partition loses nothing it would have counted.
    """
    parts = {"reachable": [], "unreachable": [], "no_side": []}
    for r in rows:
        parts[side.get((r["rule_a"], r["rule_b"]), "no_side")].append(r)
    scored = {k: agreement(parts[k], key) for k in ("reachable", "unreachable")}
    ru, rr = scored["unreachable"]["rate"], scored["reachable"]["rate"]
    return {
        "what": "B-d of PLAN_PROPOSER_1600.md: the direction rate on the pairs a "
                "fixed queue ranking cannot answer, against the rate on the ones "
                "it can. The band says the first is LOWER — that the proposer's "
                "errors concentrate where they cost most.",
        "the_split": "a queue-pair a ranking cannot answer is one that appears "
                     "with both better-rules. Computed before any call by "
                     "rung2.pair_sample_1600 and read here, never recomputed "
                     "from the answers.",
        "surface": key,
        "reachable": scored["reachable"],
        "unreachable": scored["unreachable"],
        "n_without_a_side": len(parts["no_side"]),
        "rate_unreachable": ru, "rate_reachable": rr,
        "difference": round(ru - rr, 4) if (ru is not None and rr is not None)
                      else None,
        "band_holds": (ru < rr) if (ru is not None and rr is not None) else None,
        "adjudication":
            "the band is `rate(unreachable) < rate(reachable)` and its edge is "
            "its own refutation line. `band_holds` is the reading; whether the "
            "row is adjudicated at all depends on §0 being signed, which is "
            "checked where the calls are made and not here.",
    }


# ---------------------------------------------------------------------------
# Question 2 — the ceiling of the channel at this budget
# ---------------------------------------------------------------------------

def directions_from(rows, key):
    """True where the better rule is `a`. Ties keep the model's own answer, so
    the comparison isolates the direction and not the population."""
    out = []
    for r in rows:
        v = r[key]
        if v == "a":
            out.append(True)
        elif v == "b":
            out.append(False)
        else:
            out.append(r["declared"] == "a_beats_b")
    return out


# ---------------------------------------------------------------------------
# Question 3 — a sharper null
# ---------------------------------------------------------------------------

def null_distribution(rows, rules, ids, born, instance, n_draws, seed,
                      engine=None):
    """
    `n_draws` coins on direction, each compiled and scored like the run.

    The engine is built once and reset between draws. Rebuilding it is a
    577x577 subsumption lattice over 134,400-bit masks — about a quarter of a
    second — and it is identical in every draw, so paying for it 2,000 times
    would be the entire cost of this measurement and none of its content.
    `reset_declared` is checked against a fresh engine in
    `tests/test_declared_order.py`.
    """
    engine = fresh_engine(rules) if engine is None else engine
    draws = []
    for k in range(n_draws):
        rnd = random.Random(seed + k)
        dirs = [rnd.random() < 0.5 for _ in rows]
        draws.append(floor(topological_order(
            ids, accepted_from(rows, dirs, rules, engine), born), instance))
    return draws


def rank_in(draws, value):
    """Where a score sits in the null, as a one-sided rank. The honest reading
    of a permutation test with a finite number of draws."""
    below = sum(1 for d in draws if d <= value)
    return {"n_draws": len(draws), "draws_at_or_below": below,
            "one_sided_p_low": round((below + 1) / (len(draws) + 1), 4),
            "one_sided_p_high": round(
                (sum(1 for d in draws if d >= value) + 1) / (len(draws) + 1), 4)}


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    t_start = time.time()
    source, out, split_path = parse_source(argv)
    if not source.exists():
        print(f"ABORTED: {source} is not there. Stage D has not run.")
        return 1
    src = json.loads(source.read_text())
    rows = list(src["answers"])

    corpus, rule_records, ext_c, conds = load()
    ids = [r["rule_id"] for r in rule_records]
    action = {r["rule_id"]: r["action"] for r in rule_records}
    born = {r["rule_id"]: r["born_at"] for r in rule_records}
    below = subsumption_below(rule_records, ext_c)
    matched, undef, truth = build_tables(corpus, rule_records, conds, below)
    matched_sets = [set(m) for m in matched]
    _tr0, te0 = split(corpus, truth, seed=SPLIT_SEED)
    instance = (*build_masks(ids, undef, truth, action, te0), len(te0))

    space = Space()
    ext = {rid: space.extension(conds[rid]) for rid in ids}
    tmask = space_truth_masks(space)
    allidx = list(range(len(corpus)))

    print("=" * 78)
    print("THE DIRECTION OF THE DECLARED EDGES, AGAINST WHICH RULE IS BETTER")
    print("=" * 78)
    print(f"  {len(rows)} pairs already paid for · zero API calls")
    print("  POST-RUN: written after P-d and P-e were adjudicated")
    print(f"  {describe()}")

    for r in rows:
        a, b = r["rule_a"], r["rule_b"]
        wa, wb = better_over_space(a, b, ext, action, tmask)
        r["space_wins_a"], r["space_wins_b"] = wa, wb
        r["better_space"] = verdict(wa, wb)
        ca, cb = better_over_corpus(a, b, matched_sets, truth, action, allidx)
        r["corpus_wins_a"], r["corpus_wins_b"] = ca, cb
        r["better_corpus"] = verdict(ca, cb)

    agr = {k: agreement(rows, f"better_{k}") for k in ("space", "corpus")}
    print()
    print("1. DOES THE DECLARED DIRECTION POINT AT THE BETTER RULE?")
    for k, g in agr.items():
        print(f"  {k:<8}{g['pointed_at_the_better_rule']}/{g['n']} = "
              f"{g['rate']}   se {g['standard_error']}   "
              f"{g['deviations_from_a_coin']:+.2f} deviations from a coin")
        print(f"          outside: {g['outside_the_denominator']}")

    by_side = None
    if split_path is not None:
        by_side = {k: agreement_by_side(rows, f"better_{k}",
                                        read_split(split_path, f"better_{k}"))
                   for k in ("space", "corpus")}
        print()
        print("1b. B-d — WHERE THE ERRORS FALL "
              "(band: unreachable BELOW reachable)")
        for k, b in by_side.items():
            u, r = b["unreachable"], b["reachable"]
            print(f"  {k:<8}unreachable {u['rate']} (n {u['n']})   "
                  f"reachable {r['rate']} (n {r['n']})   "
                  f"difference {b['difference']:+}")

    rules = learned_rules()
    engine = fresh_engine(rules)
    with_edge = [r for r in rows if r["declared"] != "none"]
    model_dirs = [r["declared"] == "a_beats_b" for r in with_edge]

    def score(dirs):
        return floor(topological_order(
            ids, accepted_from(with_edge, dirs, rules, engine), born), instance)

    scores = {"model": score(model_dirs),
              "inverted": score([not d for d in model_dirs])}
    for k in ("space", "corpus"):
        scores[f"better_{k}"] = score(directions_from(with_edge, f"better_{k}"))
    floor_born = floor(sorted(ids, key=lambda r: born[r]), instance)

    print()
    print("2. WOULD THE RIGHT DIRECTION HAVE HELPED? "
          "(hibrido, corpus test split 0)")
    for k in ("model", "inverted", "better_space", "better_corpus"):
        print(f"  {k:<16}{scores[k]:>9.4f}")
    print(f"  {'born_at floor':<16}{floor_born:>9.4f}")

    print()
    print(f"3. THE NULL, SHARPENED — {N_NULL_DRAWS} draws")
    draws = null_distribution(with_edge, rules, ids, born, instance,
                              N_NULL_DRAWS, NULL_SEED, engine)
    nulls = {k: rank_in(draws, v) for k, v in scores.items()}
    print(f"  coin: mean {statistics.mean(draws):.4f} sd "
          f"{statistics.pstdev(draws):.4f} "
          f"[{min(draws):.4f}, {max(draws):.4f}]")
    for k in ("model", "inverted", "better_space", "better_corpus"):
        n = nulls[k]
        print(f"  {k:<16}{scores[k]:>9.4f}   p(low) {n['one_sided_p_low']:.4f}"
              f"   p(high) {n['one_sided_p_high']:.4f}")

    payload = {
        "_env": environment(n_null_draws=N_NULL_DRAWS, null_seed=NULL_SEED),
        "what": "whether the declared direction points at the rule that gets "
                "more of the shared region right, and whether pointing the "
                "right way would have produced a better order. Reads the answers "
                "stage D already paid for; zero API calls.",
        "provenance": PROVENANCE,
        "what_better_means":
            "over the cases of ext(A) & ext(B), which rule's action is the TRUE "
            "action more often. It is NOT a layer relation and it is not what "
            "P-d was about — PLAN_PAIRWISE.md §10's `no truth for these pairs` "
            "concerns the hidden policy's layer order over rules it never wrote, "
            "and remains true.",
        "surfaces":
            "space counts every case once; corpus counts them as often as they "
            "arrive. Both are reported and neither is picked.",
        "n_pairs": len(rows),
        "source": str(source),
        "agreement_with_the_better_rule": agr,
        "scores_hibrido_corpus_test_split0": {
            k: round(v, 6) for k, v in scores.items()},
        "born_at_floor": round(floor_born, 6),
        "null": {"n_draws": N_NULL_DRAWS, "seed": NULL_SEED,
                 "mean": round(statistics.mean(draws), 6),
                 "sd": round(statistics.pstdev(draws), 6),
                 "min": round(min(draws), 6), "max": round(max(draws), 6),
                 "ranks": nulls},
        "pairs": [{k: r[k] for k in (
            "rule_a", "rule_b", "action_a", "action_b", "declared",
            "space_wins_a", "space_wins_b", "better_space",
            "corpus_wins_a", "corpus_wins_b", "better_corpus")} for r in rows],
        "seconds": round(time.time() - t_start, 1),
    }
    if by_side is not None:
        payload["B_d_direction_by_queue_ranking_side"] = by_side
        payload["split_source"] = str(split_path)
    OUT.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
