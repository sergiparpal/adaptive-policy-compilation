"""
RULES WRITTEN TWICE. How many pairs of rung 1's 577 rules carry the same
conditions and send the ticket to different queues.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
`results_why/FINDINGS_WHY.md` found five pairs among the 1,600 sampled whose two
rules are written with the same conditions in another order and name different
queues. On them the proposer fell back on the order and said so. How many such
pairs the whole base holds was not counted. This module counts them, and says
where they sit: in the population the pairwise thread sampled from, in its
sample, in the order they were written, and which of the two rules the hidden
policy agrees with.

**Such a pair is a choice no order can split.** The two rules cover the same
tickets, and subsumption does not separate them, since neither extension is
strictly inside the other; in the `hibrido` pool they even survive on the same
cases. So under any order, in either pool, the one placed first decides every
ticket of their territory and the other decides none.

--------------------------------------------------------------------------
WHAT IT COUNTS
--------------------------------------------------------------------------
Two definitions of the same rule, each reported:

  written    the same conditions as a set: the same (attribute, operator,
             value) triples in any order, an `in` list read as a set.
  covering   the same non-empty extension over the exhaustive space. It
             contains the first, and adds rules written differently that cover
             exactly the same tickets.

For each: the groups of rules that are the same, the pairs inside them split by
whether the two queues agree, and the queue pairs. For the pairs whose queues
differ: how many are in the 31,850-pair population and in the 1,600-pair sample,
how far apart they were written, which of the two the hidden policy agrees with
on each surface, and how much of each surface they cover.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The population is the published one**: `learned_population` over the
     base gives the 31,850 pairs `rung2/pair_judgement.py` gates on.
  2. **`FINDINGS_WHY.md`'s reading reproduces**: of the 1,600 sampled pairs,
     exactly five are written the same with different queues, all five in the
     batch answered on 2026-08-25; and the two pairs it names, `R0147`/`R0435`
     and `R0164`/`R0447`, are written the same with different queues.
  3. **The definitions nest**: every pair written the same covers the same
     tickets. If one did not, the canonical form would be wrong.

It refuses to write if any fails.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE COUNT AND NOT SIGNED
--------------------------------------------------------------------------
**The sample predicts the count.** The 1,600 pairs are a uniform draw from the
31,850, and every pair written the same with different queues and a non-empty
extension is in the population by construction: the two rules overlap, neither
is strictly inside the other, and their queues differ. So 5 of 1,600 scales to
about 100 such pairs in the population, 5 × 31,850 / 1,600 = 99.53, and an exact
Poisson interval on 5 puts the count between about 32 and 232. A count outside
it would say the sample misrepresented this property. Nothing is expected of the
`covering` definition beyond containing the first.

**What the drafter had seen**: `FINDINGS_WHY.md`'s five and the two pairs it
names, and the operators and value types the base's conditions use. No rule of
the base had been compared with another.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: a census asked for after `FINDINGS_WHY.md` reported its five, with
one expectation written before the count and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.identical_rules
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung2.pair_judgement import GATE_POPULATION, learned_population, learned_rules
from rung3.edge_direction import better_over_corpus, better_over_space, verdict
from rung3.order_search import build_tables, load, subsumption_below
from rung3.order_search_ls import space_truth_masks

OUT = Path("results3")
RECORD = "identical_rules.json"
SAMPLE = Path("results2/pair_sample_1600.json")

# `FINDINGS_WHY.md`'s reading, which gate 2 reproduces.
WHY_IN_SAMPLE = 5
WHY_BATCH = "new"                  # the batch answered on 2026-08-25, held out there
WHY_NAMED = (("R0147", "R0435"), ("R0164", "R0447"))

# The expectation, in numbers: 5 × 31,850 / 1,600, and the exact Poisson 95%
# interval on 5, (1.6235, 11.6683), scaled by the same factor.
EXPECTED_CENTRE = round(WHY_IN_SAMPLE * GATE_POPULATION / 1600, 2)
EXPECTED_INTERVAL = (32, 232)

PROVENANCE = (
    "POST-RUN: a census asked for after FINDINGS_WHY.md reported its five, with "
    "one expectation written before the count and committed before it ran. Not a "
    "signed row, not on STATUS.md's scoreboard, not a calibration event. Zero API "
    "calls.")

EXPECTATION = (
    "Written before the count and committed before it ran. The sample predicts "
    "the count: the 1,600 pairs are a uniform draw from the 31,850, and every "
    "pair written the same with different queues and a non-empty extension is in "
    "the population by construction. So 5 of 1,600 scales to about 100 such pairs "
    "in the population, 5 x 31,850 / 1,600 = 99.53, and an exact Poisson interval "
    "on 5 puts the count between about 32 and 232. A count outside it would say "
    "the sample misrepresented this property. Nothing is expected of the "
    "`covering` definition beyond containing the first.")

SEEN = (
    "FINDINGS_WHY.md's five and the two pairs it names, and the operators and "
    "value types the base's conditions use. No rule of the base had been compared "
    "with another.")


# ---------------------------------------------------------------------------
# The two definitions, pure
# ---------------------------------------------------------------------------

def written(conditions) -> tuple:
    """
    A rule's conditions as a set, in a canonical order.

    Each condition is its (attribute, operator, value) triple, with the value
    taken by its `repr`, so `True` and `1` stay apart, and an `in` list read as
    a set. A condition written twice in one rule counts once, since a conjunction
    does not change by repeating a term.
    """
    out = set()
    for c in conditions:
        v = c["value"]
        if isinstance(v, list):
            v = tuple(sorted(v, key=repr))
        out.add((c["attr"], c["op"], repr(v)))
    return tuple(sorted(out))


def groups(key_of: dict) -> list[list[str]]:
    """The rules that share a key, two or more to a group, each group sorted
    and the groups ordered by their first rule."""
    by = defaultdict(list)
    for rid, k in key_of.items():
        by[k].append(rid)
    return sorted((sorted(g) for g in by.values() if len(g) > 1), key=lambda g: g[0])


def pairs_of(gs, action) -> dict:
    """The pairs inside the groups, split by whether the two queues agree."""
    out = {"same_queue": [], "different_queue": []}
    for g in gs:
        for a, b in combinations(g, 2):
            out["same_queue" if action[a] == action[b] else "different_queue"].append((a, b))
    return out


def oriented(v: str, first_is_a: bool) -> str:
    """`edge_direction.verdict`'s answer, said of the rule written first or
    the one written second."""
    if v in ("tie", "neither_ever_right"):
        return v
    return "first" if (v == "a") == first_is_a else "second"


def summary(xs) -> dict | None:
    if not xs:
        return None
    return {"min": min(xs), "median": statistics.median(xs), "max": max(xs)}


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------

def census(gs, action, born, ext, tmask, matched_sets, truth, population, sample):
    """One definition's groups and pairs, and where the different-queue pairs
    sit."""
    pairs = pairs_of(gs, action)
    rows = []
    for a, b in pairs["different_queue"]:
        first, second = sorted((a, b), key=lambda r: (born[r], r))
        sa, sb = better_over_space(a, b, ext, action, tmask)
        ca, cb = better_over_corpus(a, b, matched_sets, truth, action,
                                    range(len(matched_sets)))
        drawn = sample.get(frozenset((a, b)))
        rows.append({
            "rule_first": first, "rule_second": second,
            "queue_first": action[first], "queue_second": action[second],
            "born_first": born[first], "born_second": born[second],
            "extension": (ext[a] & ext[b]).bit_count(),
            "in_population": frozenset((a, b)) in population,
            "in_sample": drawn is not None,
            "sample_batch": drawn["source"] if drawn else None,
            "sample_index": drawn["index"] if drawn else None,
            "better_space": oriented(verdict(sa, sb), first == a),
            "better_corpus": oriented(verdict(ca, cb), first == a),
            "corpus_cases_both_match": sum(1 for s in matched_sets if a in s and b in s),
        })
    covered_space = 0
    for r in rows:
        covered_space |= ext[r["rule_first"]] & ext[r["rule_second"]]
    covered_corpus = sum(1 for s in matched_sets
                         if any(r["rule_first"] in s and r["rule_second"] in s
                                for r in rows))
    return {
        "groups": len(gs),
        "group_sizes": dict(sorted(Counter(len(g) for g in gs).items())),
        "rules_in_groups": sum(len(g) for g in gs),
        "pairs": {k: len(v) for k, v in pairs.items()},
        "different_queue": {
            "pairs": len(rows),
            "in_population": sum(r["in_population"] for r in rows),
            "in_sample": sum(r["in_sample"] for r in rows),
            "in_sample_by_batch": dict(Counter(r["sample_batch"] for r in rows
                                               if r["in_sample"])),
            "queue_pairs": dict(Counter(" vs ".join(sorted((r["queue_first"],
                                                            r["queue_second"])))
                                        for r in rows).most_common()),
            "written_apart_in_cases": summary([r["born_second"] - r["born_first"]
                                               for r in rows]),
            "better_space": dict(Counter(r["better_space"] for r in rows)),
            "better_corpus": dict(Counter(r["better_corpus"] for r in rows)),
            "space_points_covered": covered_space.bit_count(),
            "corpus_cases_covered": covered_corpus,
            "rows": rows,
        },
        "groups_listed": gs,
    }


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gate_population(stats: dict) -> dict:
    return {"what": "the pairwise thread's population, recomputed",
            "measured": stats["population"], "published": GATE_POPULATION,
            "passes": stats["population"] == GATE_POPULATION}


def gate_why(written_census: dict) -> dict:
    """`FINDINGS_WHY.md`'s five, and the two pairs it names."""
    dq = written_census["different_queue"]
    found = {frozenset((r["rule_first"], r["rule_second"])) for r in dq["rows"]}
    named = {f"{a}/{b}": frozenset((a, b)) in found for a, b in WHY_NAMED}
    in_sample = dq["in_sample"]
    batches = dq["in_sample_by_batch"]
    passes = (in_sample == WHY_IN_SAMPLE and batches == {WHY_BATCH: WHY_IN_SAMPLE}
              and all(named.values()))
    return {"what": "of the 1,600 sampled pairs, five written the same with "
                    "different queues, all in the batch answered on 2026-08-25, "
                    "and the two pairs FINDINGS_WHY.md names among them",
            "in_sample": in_sample, "published": WHY_IN_SAMPLE,
            "by_batch": batches, "named_pairs_found": named, "passes": passes}


def gate_nesting(written_pairs: dict, covering_pairs: dict) -> dict:
    """Every pair written the same covers the same tickets."""
    covering = {frozenset(p) for kind in covering_pairs.values() for p in kind}
    loose = [f"{a}/{b}" for kind in written_pairs.values() for a, b in kind
             if frozenset((a, b)) not in covering]
    return {"what": "every pair written the same has the same non-empty extension",
            "pairs_that_do_not": loose, "passes": not loose}


def read_expectation(written_census: dict) -> dict:
    n = written_census["different_queue"]["in_population"]
    lo, hi = EXPECTED_INTERVAL
    return {"what": "pairs written the same with different queues, in the "
                    "population, against what 5 of 1,600 predicts",
            "count": n, "expected": EXPECTED_CENTRE, "interval": [lo, hi],
            "inside": lo <= n <= hi}


# ---------------------------------------------------------------------------

def measure():
    t_start = time.time()
    corpus, rr, ext_c, conds = load()
    ids = [r["rule_id"] for r in rr]
    action = {r["rule_id"]: r["action"] for r in rr}
    born = {r["rule_id"]: r["born_at"] for r in rr}
    below = subsumption_below(rr, ext_c)
    matched, _undef, truth = build_tables(corpus, rr, conds, below)
    matched_sets = [set(m) for m in matched]
    tmask = space_truth_masks(Space())

    pop, _ext, stats = learned_population(learned_rules(), Space())
    population = {frozenset(p) for p in pop}
    sample = {frozenset((p["rule_a"], p["rule_b"])): p
              for p in json.loads(SAMPLE.read_text())["pairs"]}

    key_written = {r["rule_id"]: written(r["conditions"]) for r in rr}
    key_covering = {rid: ext_c[rid] for rid in ids if ext_c[rid]}
    empty = sorted(rid for rid in ids if not ext_c[rid])

    args = (action, born, ext_c, tmask, matched_sets, truth, population, sample)
    g_written, g_covering = groups(key_written), groups(key_covering)
    by = {"written": census(g_written, *args), "covering": census(g_covering, *args)}

    gates = {"population": gate_population(stats),
             "findings_why": gate_why(by["written"]),
             "nesting": gate_nesting(pairs_of(g_written, action),
                                     pairs_of(g_covering, action))}
    gates["passes"] = all(g["passes"] for g in gates.values())

    written_pairs = {frozenset((r["rule_first"], r["rule_second"]))
                     for r in by["written"]["different_queue"]["rows"]}
    covering_only = [r for r in by["covering"]["different_queue"]["rows"]
                     if frozenset((r["rule_first"], r["rule_second"])) not in written_pairs]

    payload = {
        "_env": environment(),
        "what": "pairs of rung 1's 577 rules that are the same rule, written or by "
                "coverage, with the queues they send the ticket to; where the pairs "
                "whose queues differ sit, and which of the two the hidden policy "
                "agrees with. Zero API calls.",
        "provenance": PROVENANCE,
        "expectation_written_before_the_count": EXPECTATION,
        "what_the_drafter_had_seen": SEEN,
        "adjudicates_nothing": "no row of any plan is read here and none moves.",
        "base": "results/llm_run.json, the 577 rules of rung 1",
        "definitions": {
            "written": "the same (attribute, operator, value) triples in any order, "
                       "an `in` list read as a set",
            "covering": "the same non-empty extension over the exhaustive space"},
        "surfaces": {
            "space": "the exhaustive space, 134,400 points, each counted once",
            "corpus": "the full corpus, 2,000 arrivals, as rung3/edge_direction.py "
                      "defines the better rule"},
        "better_rule": "rung3/edge_direction.py's verdict over the shared region, "
                       "here the whole territory of both, said of the rule written "
                       "first or second",
        "n_rules": len(ids),
        "rules_with_empty_extension": empty,
        "gates": gates,
        "written": by["written"],
        "covering": by["covering"],
        "covering_but_not_written": covering_only,
        "expectation_read": read_expectation(by["written"]),
        "seconds": round(time.time() - t_start, 1),
    }
    return payload, gates


def main(argv=None) -> int:
    payload, gates = measure()
    print("=" * 78)
    print("RULES WRITTEN TWICE")
    print("=" * 78)
    print(f"  {payload['n_rules']} rules of rung 1 · zero API calls · POST-RUN, "
          f"expectation written before the count")
    print(f"  {describe()}")
    g = gates["population"]
    print(f"  gate 1, the population: {g['measured']} against {g['published']}  "
          f"{'PASS' if g['passes'] else 'FAIL'}")
    g = gates["findings_why"]
    print(f"  gate 2, FINDINGS_WHY's five: {g['in_sample']} in the sample, "
          f"by batch {g['by_batch']}, named {g['named_pairs_found']}  "
          f"{'PASS' if g['passes'] else 'FAIL'}")
    g = gates["nesting"]
    print(f"  gate 3, the definitions nest: {len(g['pairs_that_do_not'])} loose  "
          f"{'PASS' if g['passes'] else 'FAIL'}")
    if not gates["passes"]:
        print("\nREFUSED: nothing was written.")
        return 1

    for name in ("written", "covering"):
        c = payload[name]
        dq = c["different_queue"]
        print(f"\n  {name.upper()}: {c['groups']} groups of {c['rules_in_groups']} rules "
              f"{c['group_sizes']}, pairs {c['pairs']}")
        print(f"    different queues: {dq['pairs']} pairs, {dq['in_population']} in the "
              f"population, {dq['in_sample']} in the sample {dq['in_sample_by_batch']}")
        print(f"    queue pairs: {dq['queue_pairs']}")
        print(f"    written apart, in cases: {dq['written_apart_in_cases']}")
        print(f"    the better rule, space: {dq['better_space']}")
        print(f"    the better rule, corpus: {dq['better_corpus']}")
        print(f"    covered: {dq['space_points_covered']} space points, "
              f"{dq['corpus_cases_covered']} corpus arrivals")
    print(f"\n  rules with an empty extension: {payload['rules_with_empty_extension']}")
    print(f"  pairs that cover the same and are written differently, different "
          f"queues: {len(payload['covering_but_not_written'])}")
    e = payload["expectation_read"]
    print(f"\n  the expectation: {e['count']} against about {e['expected']}, "
          f"interval {e['interval']}: {'inside' if e['inside'] else 'OUTSIDE'}")

    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
