"""
DOES DELIBERATE DROPPING BEAT ACCIDENTAL DROPPING? The last route §13 left open.

--------------------------------------------------------------------------
WHAT THIS IS, AND THE TRAP IT IS BUILT AROUND
--------------------------------------------------------------------------
§13 found that the cycle-refusing topological sort was **accidentally protecting
the score**: it discards 169 of 1,479 declared edges first-come-first-served, and
honouring more of them makes the order worse. So the dropping was doing useful
work by luck, and the one route it left open is a compilation that drops
**deliberately**.

**`Drop edges until the score improves` is hard rule 6 wearing a hat.** A selection
rule that consults the score is search with extra steps, and it would reproduce
`order_search_ls` while calling itself a channel result. So every rule here obeys
three constraints, all declared before the run:

  1. **It reads only the answers.** No truth, no labels, no score. §12's
     reachable/unreachable split is derived from the ORACLE and is therefore
     forbidden as a dropping criterion, however tempting — it is the right
     diagnostic and the wrong instrument.
  2. **Every rule is reported.** Not the best one. The rules are fixed below
     before any figure of them exists, and a rule that does badly appears in the
     table beside one that does well.
  3. **Every filter is read against a RANDOM DROP OF THE SAME SIZE.** §13 showed
     that dropping at all moves the score, so a filter compared only against
     `keep everything` would measure how many edges it removed and call it
     selection. What a rule is worth is its distance from dropping that many at
     random.

--------------------------------------------------------------------------
THE RANKING IS THE PROPOSER'S OWN, AND THAT IS THE POINT
--------------------------------------------------------------------------
`results3/queue_hierarchy_floor.json`'s **0.4824** is Stage C's hierarchy,
transferred unchanged from the HIDDEN policy's labelled pairs. It costs no labels
*on this cell* because it was fitted on a different object — which makes it a fair
reference line and a poor dropping criterion, since the fitting happened somewhere
with a key.

The ranking used here is derived from **the 1,600 run's own 1,479 answers**: for
each unordered queue pair, which side the proposer named more often; then Copeland
score over those pairs, ties broken by how often the queue was named a winner at
all and then alphabetically, so it is total and deterministic. Nothing outside the
answers enters it. It is what the proposer would have if it were asked to be
self-consistent.

  `consistent`    edges the proposer's own ranking agrees with. Dropping the rest
                  keeps its self-consistent core.
  `inconsistent`  the complement — every edge where the proposer contradicted its
                  own majority. §12 says this is where the winnable order is and
                  also where the proposer is random, so both outcomes are
                  interesting and neither is expected to be good.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE RUN AND NOT SIGNED
--------------------------------------------------------------------------
`consistent` lands near the queue ranking's level and beats neither it nor the
baseline by anything that survives its own random control — because compiling the
proposer's self-consistent core IS compiling a queue ranking. `inconsistent` lands
at or below the floor. **And the baseline's own 169-edge accident is not special**:
the same edges fed in a random arrival order should reach about what the
topological sort reaches, which would say the 0.4804 was never a selection at
all.

This is **not a signed row**, is not on `STATUS.md`'s scoreboard, and is not a
calibration event.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.edge_dropping
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from harness.provenance import describe, environment
from rung2.pair_judgement import learned_rules
from rung3.declared_order import (accepted_from, fresh_engine,
                                  topological_order)
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.mfas_compilation import mfas_order, violations
from rung3.order_search import build_tables, load, split, subsumption_below

OUT = Path("results3")
RECORD = "edge_dropping.json"
SOURCE = Path("results2/pair_judgement_1600.json")

RANDOM_DRAWS = 50
RANDOM_SEED = 17
SPLIT_SEED = 17
QUEUE_RANKING_REFERENCE = 0.4824   # queue_hierarchy_floor.json, stage_c row

PROVENANCE = (
    "POST-RUN with an expectation written before the run, in the module and in "
    "this record. NOT a signed row, not on STATUS.md's scoreboard, not a "
    "calibration event. Zero API calls.")

EXPECTATION = (
    "Written before the run. `consistent` lands near the queue ranking's level "
    "and beats neither it nor the baseline by anything surviving its own random "
    "control, because compiling the proposer's self-consistent core is compiling "
    "a queue ranking. `inconsistent` lands at or below the arrival floor. And the "
    "baseline's 169-edge cycle accident is not special: the same edges in a "
    "random arrival order should reach about what the topological sort "
    "reaches.")


# ---------------------------------------------------------------------------
# The proposer's own ranking, from the answers and nothing else
# ---------------------------------------------------------------------------

def revealed_ranking(rows):
    """
    Copeland over the queue pairs the proposer itself decided.

    For each unordered pair of queues, the side named winner more often takes the
    pair; a queue's score is the pairs it takes. Ties on the pair go to neither.
    The total order breaks Copeland ties by how often the queue was named a winner
    at all, then alphabetically — declared here so it is deterministic and so that
    nothing outside the answers can enter it.
    """
    byp = defaultdict(Counter)
    named = Counter()
    for r in rows:
        w = r["action_a"] if r["declared"] == "a_beats_b" else r["action_b"]
        l = r["action_b"] if r["declared"] == "a_beats_b" else r["action_a"]
        byp[tuple(sorted((w, l)))][w] += 1
        named[w] += 1
    queues = sorted({q for p in byp for q in p})
    copeland = Counter({q: 0 for q in queues})
    for (x, y), c in byp.items():
        if c[x] > c[y]:
            copeland[x] += 1
        elif c[y] > c[x]:
            copeland[y] += 1
    order = sorted(queues, key=lambda q: (-copeland[q], -named[q], q))
    return order, {q: k for k, q in enumerate(order)}, dict(copeland)


def ranking_follower_rows(rows, rank):
    """
    The same 1,479 pairs, answered by a PERFECT follower of the ranking.

    **Added after seeing `consistent` fall short of 0.4824, and labelled as
    such.** It is a diagnostic and not a filter: it changes what was declared
    rather than which declarations are kept, so it never enters the filter table
    and it is not a candidate dropping rule.

    It asks one thing the thread had assumed rather than measured: is the free
    queue ranking's 0.4824 REACHABLE through this channel at this budget at all?
    A ranking applied as a lookup orders all 577 rules; 1,479 pairs is 4.6% of the
    31,850 that could carry an edge, so the edges encode a sparse shadow of the
    same ranking and the two need not score alike.
    """
    out = []
    for r in rows:
        a, b = r["action_a"], r["action_b"]
        out.append(dict(r, declared=("a_beats_b" if rank[a] < rank[b]
                                     else "b_beats_a")))
    return out


def agrees(row, rank):
    """Does the proposer's own ranking endorse the edge the proposer declared?"""
    w = row["action_a"] if row["declared"] == "a_beats_b" else row["action_b"]
    l = row["action_b"] if row["declared"] == "a_beats_b" else row["action_a"]
    return rank[w] < rank[l]


# ---------------------------------------------------------------------------
# Compiling a kept subset, both ways
# ---------------------------------------------------------------------------

def compile_subset(kept, rules, ids, born, instance, engine):
    """The two compilations of a kept subset, with fidelity on that subset."""
    dirs = [r["declared"] == "a_beats_b" for r in kept]
    edges = [(r["rule_a"], r["rule_b"]) if d else (r["rule_b"], r["rule_a"])
             for r, d in zip(kept, dirs)]
    accepted = accepted_from(kept, dirs, rules, engine)
    topo = topological_order(ids, accepted, born)
    mfas, _search = mfas_order(edges, ids, born, topo)
    return {
        "n_kept": len(kept),
        "topological": round(floor(topo, instance), 6),
        "mfas": round(floor(mfas, instance), 6),
        "violations_topological": violations(topo, edges),
        "violations_mfas": violations(mfas, edges),
    }


def random_control(rows, n_keep, rules, ids, born, instance, engine,
                   n_draws=RANDOM_DRAWS, seed=RANDOM_SEED):
    """
    The same NUMBER of edges kept, chosen at random.

    This is what a filter has to beat. §13 showed dropping at all moves the
    score, so a filter read only against `keep everything` measures how many
    edges it removed and calls it selection.
    """
    t, m = [], []
    for k in range(n_draws):
        kept = random.Random(seed + k).sample(rows, n_keep)
        r = compile_subset(kept, rules, ids, born, instance, engine)
        t.append(r["topological"])
        m.append(r["mfas"])
    return {"n_draws": n_draws, "n_kept": n_keep,
            "topological": {"mean": round(statistics.mean(t), 6),
                            "sd": round(statistics.pstdev(t), 6)},
            "mfas": {"mean": round(statistics.mean(m), 6),
                     "sd": round(statistics.pstdev(m), 6)}}


def devs(value, control):
    sd = control["sd"]
    return round((value - control["mean"]) / sd, 2) if sd else None


def main(argv=None) -> int:
    t_start = time.time()
    if not SOURCE.exists():
        print(f"ABORTED: {SOURCE} is not there.")
        return 1
    src = json.loads(SOURCE.read_text())
    rows = [r for r in src["answers"] if r["declared"] != "none"]

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

    order, rank, copeland = revealed_ranking(rows)
    keep = {"keep_all": rows,
            "consistent": [r for r in rows if agrees(r, rank)],
            "inconsistent": [r for r in rows if not agrees(r, rank)]}

    print("=" * 78)
    print("DOES DELIBERATE DROPPING BEAT ACCIDENTAL DROPPING?")
    print("=" * 78)
    print(f"  {len(rows)} declared edges · hibrido, corpus test split 0 · "
          f"zero API calls")
    print("  POST-RUN, expectation written before the run, NOT a signed row")
    print(f"  {describe()}")
    print()
    print("  the proposer's OWN ranking, from its answers and nothing else:")
    for k, q in enumerate(order):
        print(f"    {k + 1}. {q:<22}copeland {copeland[q]}")

    # the baseline: what the arrival accident keeps
    dirs_all = [r["declared"] == "a_beats_b" for r in rows]
    n_accepted = len(accepted_from(rows, dirs_all, rules, engine))

    out = {}
    for name, kept in keep.items():
        r = compile_subset(kept, rules, ids, born, instance, engine)
        r["control_random_same_size"] = random_control(
            rows, len(kept), rules, ids, born, instance, engine)
        r["topological_in_control_deviations"] = devs(
            r["topological"], r["control_random_same_size"]["topological"])
        r["mfas_in_control_deviations"] = devs(
            r["mfas"], r["control_random_same_size"]["mfas"])
        out[name] = r

    # Is the arrival accident special? The control is the SAME EDGES IN A RANDOM
    # ARRIVAL ORDER, which is `keep_all`'s control: sampling all 1,479 returns a
    # permutation, and `accepted_from` refuses cycles sequentially, so each draw
    # is the same mechanism with a different sequence.
    #
    # A first version of this control sampled 1,310 rows instead — the number the
    # accident keeps — and it was WRONG. Those subsets go through `try_edge`
    # again and install about 1,166, some 144 fewer than the baseline's 1,310,
    # so the gap it reported was partly a smaller edge set and not selection at
    # all. The measured confound is recorded rather than quietly fixed.
    acc_ctrl = out["keep_all"]["control_random_same_size"]
    baseline = {
        "what": "the topological sort's own cycle refusal — 169 of 1,479 edges "
                "dropped first-come-first-served — read against the SAME edges "
                "fed in a random arrival order and refused by the same "
                "mechanism. It isolates whether arrival order specifically is "
                "worth anything.",
        "n_installed_by_the_accident": n_accepted,
        "score": out["keep_all"]["topological"],
        "control_same_edges_random_arrival_order": acc_ctrl["topological"],
        "in_control_deviations": devs(out["keep_all"]["topological"],
                                      acc_ctrl["topological"]),
        "a_control_that_was_wrong_and_is_recorded":
            "keeping 1,310 rows at random instead. Those go through try_edge "
            "again and install about 1,166 — some 144 fewer than the baseline's "
            "1,310, which are all installed by construction — so the gap would "
            "have been partly a smaller edge set. Measured at 20 draws before "
            "being discarded.",
    }

    follower = compile_subset(ranking_follower_rows(rows, rank), rules, ids,
                              born, instance, engine)

    print()
    print(f"  {'filter':<14}{'kept':>6}{'topo':>9}{'mfas':>9}"
          f"{'rnd topo':>10}{'sd':>8}{'devs':>7}{'rnd mfas':>10}{'sd':>8}{'devs':>7}")
    for name in ("keep_all", "consistent", "inconsistent"):
        r = out[name]
        c = r["control_random_same_size"]
        print(f"  {name:<14}{r['n_kept']:>6}{r['topological']:>9.4f}"
              f"{r['mfas']:>9.4f}{c['topological']['mean']:>10.4f}"
              f"{c['topological']['sd']:>8.4f}"
              f"{r['topological_in_control_deviations']:>+7.2f}"
              f"{c['mfas']['mean']:>10.4f}{c['mfas']['sd']:>8.4f}"
              f"{r['mfas_in_control_deviations']:>+7.2f}")
    print()
    print(f"  the arrival accident: installs {n_accepted}, scores "
          f"{baseline['score']:.4f}; the SAME edges in a random arrival order "
          f"give {acc_ctrl['topological']['mean']:.4f} "
          f"sd {acc_ctrl['topological']['sd']:.4f} "
          f"({baseline['in_control_deviations']:+.2f} devs)")
    print(f"  reference lines: born_at floor {floor_born:.4f}, "
          f"a free queue ranking {QUEUE_RANKING_REFERENCE:.4f}")
    print()
    print(f"  DIAGNOSTIC (added after seeing `consistent`): a PERFECT follower of "
          f"the same ranking,")
    print(f"  answering all 1,479 pairs, scores {follower['topological']:.4f} "
          f"topological / {follower['mfas']:.4f} mfas.")
    print(f"  The ranking as a LOOKUP over all 577 rules scores "
          f"{QUEUE_RANKING_REFERENCE:.4f}. 1,479 pairs is 4.6% of the 31,850.")

    payload = {
        "_env": environment(random_draws=RANDOM_DRAWS, random_seed=RANDOM_SEED),
        "what": "whether a truth-free rule for dropping declared edges beats "
                "dropping the same number at random, and whether the "
                "topological sort's cycle accident was ever a selection. Zero "
                "API calls.",
        "provenance": PROVENANCE,
        "expectation_written_before_the_run": EXPECTATION,
        "adjudicates_nothing":
            "no row of any plan is read here and none moves. The rules were "
            "fixed before the run and every one of them is reported, not the "
            "best.",
        "no_rule_here_sees_the_truth":
            "the ranking is Copeland over the queue pairs the proposer itself "
            "decided, from the 1,479 answers and nothing else. §12's "
            "reachable/unreachable split is derived from the ORACLE and is "
            "therefore forbidden as a dropping criterion — it is the right "
            "diagnostic and the wrong instrument.",
        "every_filter_has_a_same_size_random_control":
            "§13 showed that dropping at all moves the score, so a filter read "
            "only against `keep everything` would measure how many edges it "
            "removed and call it selection.",
        "surface": "hibrido pool, corpus test split 0",
        "source": str(SOURCE),
        "born_at_floor": round(floor_born, 6),
        "queue_ranking_reference": QUEUE_RANKING_REFERENCE,
        "queue_ranking_reference_note":
            "results3/queue_hierarchy_floor.json's stage_c row: Stage C's "
            "hierarchy transferred from the HIDDEN policy's labelled pairs. Free "
            "on this cell because it was fitted on another object, which makes "
            "it a fair reference line and a poor dropping criterion.",
        "revealed_ranking": {"order": order, "copeland": copeland,
                             "derived_from": "the 1,479 declared answers"},
        "filters": out,
        "diagnostic_a_perfect_ranking_follower": dict(
            follower,
            what="the same 1,479 pairs answered by a perfect follower of the "
                 "proposer's own revealed ranking. NOT a filter and not a "
                 "candidate dropping rule: it changes what was declared rather "
                 "than which declarations are kept.",
            provenance="added AFTER seeing `consistent` land near the floor "
                       "rather than near 0.4824, to test whether that line is "
                       "reachable through this channel at this budget at all. "
                       "Labelled rather than folded in.",
            the_line_it_is_read_against=QUEUE_RANKING_REFERENCE,
            why_they_can_differ="a ranking applied as a LOOKUP orders all 577 "
                                "rules; 1,479 pairs is 4.6% of the 31,850 that "
                                "could carry an edge, so the edges encode a "
                                "sparse shadow of the same ranking."),
        "the_arrival_accident": baseline,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
