"""
WHAT THE DECLARED EDGES DO — the three scorings of Stage D, and the control.

--------------------------------------------------------------------------
WHAT THIS IS
--------------------------------------------------------------------------
Stage D asked a model 400 pairwise questions over the 577 learned rules and got
back a set of declared edges. **There is no truth for those pairs**, so nothing
here is a correct-edge rate. What is measured is what the edges DO, in the three
ways `PLAN_PAIRWISE.md` §10 asks for, plus one control §10 does not ask for and
that the Stage C result made necessary.

  1. **As a hybrid engine.** The edges installed into a `PriorityEngine` over the
     577 rules, deciding corpus test: e2e, silent error, CONFLICT, IMPASSE.
     Compared against `hibrido` figures and never against `puro` ones — scoring a
     hybrid result against 0.8530 inflates the bar by ~0.08 by reading another
     engine's surface.
  2. **As an order, against the floor Stage A measured.** This is **P-d**.
  3. **As a machine, against the 65.** Behavioural distance from 65 end orders
     regenerated **on the hybrid pool**, because the published 65 are `puro` and
     a hybrid order and a pure order can decide differently for no reason except
     the pool. This is **P-e**.

  +  **The control.** The same order against the one a fixed queue ranking
     induces (`results3/queue_hierarchy_floor.json`). Stage C found the
     proposer's competence is largely such a ranking, and that ranking already
     clears P-d's band at zero calls. Without this line a hold cannot be read.

--------------------------------------------------------------------------
THE ORDER, AND WHY MOST OF IT IS THE TIE-BREAK
--------------------------------------------------------------------------
The declared edges are a partial order. Compiling them to a total one is a
topological sort whose ready set is drained in `born_at` order, so **every rule
no edge touches keeps its arrival position**.

That is deliberate and it is what makes P-d readable: `born_at` IS the floor, so
the comparison is exactly *what did the edges add to the floor*. It also means
the order is overwhelmingly the tie-break — 400 edges is 1.3% of the 31,850
pairs that could carry one — and the record publishes how many rules actually
moved, because a figure that moves nothing and a figure that moves everything
should not read the same.

`gate_order_respects_edges` checks the compiled order honours every accepted
edge. If it ever failed, the order would not be the one the edges induce and P-d
would be adjudicated on something else.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It spends nothing: the calls are already made and their record is read-only. It
does not move a band — P-d and P-e were signed on 2026-08-24 and are adjudicated
exactly as written, with the control reported beside them and never in place of
them. The floors and the hierarchy figures are READ from the records that own
them.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.declared_order
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
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space
from rung2.pair_judgement import learned_rules
from rung3.floor_by_pool import (CORPUS_FULL, POOLS, SPACE, corpus_instances,
                                 floor, index_sets_of)
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                MULTISTART_STARTS, build_masks,
                                declared_starts, greedy_order_from_masks,
                                multistart)
from rung3.order_metrics import behavioural_distance, decisions
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import space_pools, tail_key_factory

OUT = Path("results3")
RECORD = "declared_order.json"
SOURCE = Path("results2/pair_judgement_learned.json")
FLOOR_RECORD = OUT / "floor_by_pool.json"
HIERARCHY_RECORD = OUT / "queue_hierarchy_floor.json"

N_ORDERS = 65
SPLIT = 0
SPLIT_SEED = 17


def parse_source(argv):
    """
    `--source` names the answers to score; `--out` names where the scoring goes.

    They come as a pair on purpose. `PLAN_PROPOSER_1600.md` scores a second,
    larger population with this same code — rule C of its §4, so that the
    400-point and the 1,600-point are not made incomparable by a
    reimplementation — and the destination of that scoring must never be able to
    land on the closed thread's record by omission. So a non-default `--source`
    without an `--out` aborts, and the default pair is the only one that writes
    `declared_order.json`.
    """
    source = SOURCE
    out = OUT / RECORD
    if "--source" in argv:
        source = Path(argv[argv.index("--source") + 1])
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    elif source != SOURCE:
        raise SystemExit(
            f"\nABORTED: --source {source} without --out.\n\n"
            f"  {OUT / RECORD} is the closed thread's record and P-d and P-e "
            f"were\n  adjudicated on it. Another population needs another "
            f"destination:\n\n"
            f"    --out {OUT}/declared_order_1600.json\n")
    return source, out, source == SOURCE


def not_adjudicated_here(block):
    """
    The same computation on another population, with the verdict taken off.

    P-d and P-e were signed in §0 of `PLAN_PAIRWISE.md` and adjudicated on Stage
    D's 400 pairs. Scoring a different population with the same code produces the
    same NUMBER shaped like a verdict, and a record that printed it as one would
    let a row be re-adjudicated by rerunning it on more data — which is hard rule
    6 with extra steps. So the figure stays and the word `verdict` goes.
    """
    out = {k: v for k, v in block.items() if k != "verdict"}
    out["adjudicates"] = False
    out["above_the_threshold"] = block["verdict"] == "HOLDS"
    out["note"] = (
        f"{block['row']} was signed in §0 of PLAN_PAIRWISE.md and adjudicated on "
        f"Stage D's 400 pairs; it keeps that verdict and this is not a second "
        f"reading of it. What is here is the same computation on another "
        f"population, reported and never substituted.")
    return out

# P-d and P-e, as signed in §0 of PLAN_PAIRWISE.md on 2026-08-24. Carried so the
# verdicts can be read off, never to be adjusted.
P_D_MARGIN = 0.03
P_E_BAND = 0.25

# The direction control. Declared here rather than chosen after seeing a
# figure: 50 draws is the count every random baseline in this repository
# uses, and 17 is the project's seed.
N_DIRECTION_DRAWS = 50
DIRECTION_SEED = 17

# §0 of PLAN_PROPOSER_1600.md, transcribed on 2026-08-25 before any figure of
# that plan existed. B-b says the order beats what a FREE ranking of the eight
# queues scores; B-c says it reaches the projection built from its own measured
# accuracy. Two other records own the figures these were transcribed from, and
# `gate_lines_still_hold` checks they still say so — a band is what was signed
# and the record is what it was signed against, so a drift between them is a
# discrepancy to report rather than to absorb.
B_B_LINE = 0.4824   # results3/queue_hierarchy_floor.json, hibrido / test split 0
B_C_LINE = 0.4981   # results3/edge_budget.json, the 1,600 row of the noisy curve

# This plan's own, declared before its figures exist. 200 rather than
# edge_budget's 10 because that module scored eight budgets and this one scores
# one, so the deviation can be ESTIMATED rather than merely indicated — and §8
# says the reading of B-c turns on it: a refutation by less than the projection's
# own deviation is a different event from one by three of them. The closed
# thread's N_DIRECTION_DRAWS stays at 50; it belongs to an adjudicated row.
READING_DRAWS = 200
READING_SEED = 17
READING_BUDGET = 1600
ABOUT = "the 1,600-pair sample of PLAN_PROPOSER_1600.md"
BUDGET_RECORD = OUT / "edge_budget.json"


# ---------------------------------------------------------------------------
# The order the edges induce
# ---------------------------------------------------------------------------

def topological_order(ids, edges, born):
    """
    A total order honouring every declared edge, ties drained by `born_at`.

    Kahn's algorithm with the ready set kept sorted by arrival, so a rule no
    edge touches keeps its arrival position and the comparison against the
    `born_at` floor is exactly *what the edges added*.

    Cycles cannot arrive here — `try_edge` refuses one — but if the graph ever
    carried one, the leftovers are appended in arrival order and
    `gate_order_respects_edges` reports the edges that were broken rather than
    the run dying silently.
    """
    import heapq

    after = {rid: set() for rid in ids}
    indeg = {rid: 0 for rid in ids}
    for w, loser in edges:
        if loser not in after[w]:
            after[w].add(loser)
            indeg[loser] += 1
    ready = [born[r] for r in ids if indeg[r] == 0]
    by_born = {born[r]: r for r in ids}
    heapq.heapify(ready)
    out = []
    while ready:
        rid = by_born[heapq.heappop(ready)]
        out.append(rid)
        for nxt in sorted(after[rid], key=lambda r: born[r]):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(ready, born[nxt])
    if len(out) < len(ids):
        placed = set(out)
        out += sorted((r for r in ids if r not in placed), key=lambda r: born[r])
    return out


def gate_order_respects_edges(order, edges):
    rank = {rid: k for k, rid in enumerate(order)}
    broken = [[w, loser] for w, loser in edges if rank[w] > rank[loser]]
    return {
        "what": "every accepted edge must place its winner before its loser. If "
                "it did not, the compiled order would not be the one the edges "
                "induce and P-d would be adjudicated on something else.",
        "n_edges": len(edges), "n_broken": len(broken),
        "broken": broken[:20], "passes": not broken,
    }


def rules_moved(order, born, ids):
    """How many rules sit somewhere other than their arrival position.

    400 edges is 1.3% of the pairs that could carry one, so most of the order is
    the tie-break. A figure that moves nothing and one that moves everything must
    not read the same.
    """
    base = sorted(ids, key=lambda r: born[r])
    return sum(1 for a, b in zip(base, order) if a != b)


# ---------------------------------------------------------------------------
# Scoring 1 — as a hybrid engine
# ---------------------------------------------------------------------------

def engine_metrics(rules, edges, corpus, idxs, truth):
    """
    e2e, silent error, CONFLICT and IMPASSE with the edges installed.

    `silent error` is the rung 1 definition: of the cases the engine COMMITS to
    an action on, the fraction it gets wrong. Abstaining is not an error here —
    that is the whole reason CONFLICT exists — so the two rates have different
    denominators and both are published with theirs.
    """
    engine = PriorityEngine(space=Space())
    for rid in sorted(rules):
        engine.add(Rule2(rule_id=rid, conditions=list(rules[rid].conditions),
                         action=rules[rid].action),
                   born_at=rules[rid].born_at, keep_id=True)
    installed = Counter()
    for w, loser in edges:
        installed[engine.try_edge(w, loser)] += 1

    tally = Counter()
    ok = 0
    for i in idxs:
        kind, rule, _m = engine.decide(corpus[i])
        tally[kind] += 1
        if kind == "ACTION":
            if rule.action == truth[i]:
                ok += 1
    committed = tally["ACTION"]
    return {
        "what": "the 577 rules in a PriorityEngine with the accepted edges "
                "installed, deciding corpus test. Compared against hibrido "
                "figures only: a hybrid result read against a pure one inflates "
                "the bar by about 0.08.",
        "n_cases": len(idxs),
        "edges_installed": dict(installed),
        "outcomes": dict(tally),
        "e2e": round(ok / len(idxs), 4),
        "committed": committed,
        "silent_error": round((committed - ok) / committed, 4) if committed else None,
        "silent_error_denominator": committed,
        "conflict_rate": round(tally["CONFLICT"] / len(idxs), 4),
        "impasse_rate": round(tally["IMPASSE"] / len(idxs), 4),
    }


# ---------------------------------------------------------------------------
# The direction control — is it the model's choices or the compilation?
# ---------------------------------------------------------------------------

def fresh_engine(rules):
    engine = PriorityEngine(space=Space())
    for rid in sorted(rules):
        engine.add(Rule2(rule_id=rid, conditions=list(rules[rid].conditions),
                         action=rules[rid].action),
                   born_at=rules[rid].born_at, keep_id=True)
    return engine


def reset_declared(engine):
    """
    Drop every declared edge and leave subsumption untouched.

    Exactly the state `fresh_engine` returns, and the reason it exists: building
    one costs a 577x577 subsumption lattice over 134,400-bit masks, which is
    seconds. A null distribution wants thousands of draws and only the declared
    edges differ between them, so rebuilding the lattice each time is the whole
    cost of the measurement and none of its content. `try_edge` mutates
    `decl_below` and `decl_above` and nothing else, so clearing them is the
    identity and not an approximation.
    """
    for rid in engine.decl_below:
        engine.decl_below[rid] = set()
        engine.decl_above[rid] = set()
    return engine


def accepted_from(rows, directions, rules, engine=None):
    """
    The edges a set of directions produces, fed sequentially into an engine
    carrying subsumption and no declared edge.

    Sequentially and through `try_edge`, because whether an edge closes a cycle
    depends on the ones already in — so a control that installed them any other
    way would not be comparable with the run.

    `engine` lets a caller hand in one already built; it is reset before use, so
    passing one is indistinguishable from building a fresh one except in time.
    """
    engine = fresh_engine(rules) if engine is None else reset_declared(engine)
    out = []
    for row, forward in zip(rows, directions):
        w, loser = ((row["rule_a"], row["rule_b"]) if forward
                    else (row["rule_b"], row["rule_a"]))
        if engine.try_edge(w, loser) == EDGE_OK:
            out.append((w, loser))
    return out


def direction_controls(rows, rules, ids, born, instance,
                       n_draws=N_DIRECTION_DRAWS, seed=DIRECTION_SEED):
    """
    The same 365 pairs, the same compilation, the same scoring — and only the
    DIRECTION of each edge changed.

    This is what separates two explanations of a low score that would otherwise
    be indistinguishable: the model chose badly, or compiling any set of edges
    this way hurts. If a coin on direction lands where the model does, the
    compilation is the problem and no conclusion about the proposer survives.

    Three readings: the model's own directions, every one of them reversed, and
    `n_draws` coins. The coin distribution is what the other two are read
    against, and its deviation is what says whether a gap is a difference or a
    sign.
    """
    model = [r["declared"] == "a_beats_b" for r in rows]
    engine = fresh_engine(rules)

    def score(dirs):
        return floor(topological_order(
            ids, accepted_from(rows, dirs, rules, engine), born), instance)

    draws = []
    for k in range(n_draws):
        rnd = random.Random(seed + k)
        draws.append(score([rnd.random() < 0.5 for _ in rows]))
    m, inv = score(model), score([not d for d in model])
    mean, sd = statistics.mean(draws), statistics.pstdev(draws)
    return {
        "what": "the same pairs, the same compilation and the same scoring, with "
                "only the DIRECTION of each edge changed. It separates `the "
                "model chose badly` from `compiling any edges this way hurts`, "
                "which a single low score cannot.",
        "surface": "corpus test split 0, hibrido pool — P-d's own cell",
        "n_pairs": len(rows), "n_draws": n_draws, "seed": seed,
        "model": round(m, 6),
        "model_inverted": round(inv, 6),
        "coin": {"mean": round(mean, 6), "sd": round(sd, 6),
                 "min": round(min(draws), 6), "max": round(max(draws), 6)},
        "model_minus_coin": round(m - mean, 6),
        "model_in_coin_deviations": round((m - mean) / sd, 3) if sd else None,
        "inverted_minus_coin": round(inv - mean, 6),
        "inverted_in_coin_deviations": round((inv - mean) / sd, 3) if sd else None,
    }


# ---------------------------------------------------------------------------
# B-b and B-c — the order against the free ranking and against the projection
# ---------------------------------------------------------------------------

def read_budget_row(path=BUDGET_RECORD, budget=READING_BUDGET):
    """The coin and the projection at this budget, from the record that owns
    them. Read, never transcribed twice."""
    rec = json.loads(Path(path).read_text())
    row = next((r for r in rec["curves"] if r["budget"] == budget), None)
    if row is None:
        return None
    return {k: row[k] for k in ("budget", "offered", "ties_offering_nothing",
                                "oracle", "noisy_mean", "noisy_sd",
                                "coin_mean", "coin_sd")}


def gate_lines_still_hold(hierarchy, budget_row):
    """
    The two lines §0 transcribed are still what their records say.

    §0 signed `> 0.4824` and `>= 0.4981` against figures two other records own.
    If one of those records moves — re-run, corrected, regenerated — the band
    does not follow it: what was signed is the number. So the mismatch is
    surfaced instead of being silently absorbed on either side.
    """
    got_b = hierarchy
    got_c = budget_row["noisy_mean"] if budget_row else None
    ok_b = got_b is not None and abs(got_b - B_B_LINE) < 5e-5
    ok_c = got_c is not None and abs(got_c - B_C_LINE) < 5e-5
    return {
        "what": "B-b's and B-c's lines were transcribed from §0 before any "
                "figure of this plan existed. Their owning records are checked "
                "to still say the same thing; a drift is reported, and the band "
                "stays as signed either way.",
        "B_b_line_signed": B_B_LINE,
        "B_b_line_in_its_record": got_b,
        "B_b_owner": "results3/queue_hierarchy_floor.json",
        "B_c_line_signed": B_C_LINE,
        "B_c_line_in_its_record": got_c,
        "B_c_owner": f"results3/edge_budget.json, budget {READING_BUDGET}",
        "passes": ok_b and ok_c,
    }


def oracle_directions_from_split(rows, split_path, key="better_space"):
    """
    The oracle's own direction per row, READ from the Stage A record.

    True where `a` is the better rule, False where `b` is, None on a tie or on
    the material problem — where the channel has nothing to say and forcing a
    direction would credit it with a coin flip it never made.

    Read rather than recomputed for the reason `read_split` gives: the verdicts
    were fixed and gated before a call was made, and deriving them again beside
    the thing they score would let them move with it.

    Returns `(directions, n_missing)`. A pair the split record does not carry is
    counted apart from a tie and never folded into it: the caller refuses to
    build the projection at all rather than build it on a silently smaller set
    of offers.
    """
    by_pair = {(r["rule_a"], r["rule_b"]): r[key]
               for r in json.loads(Path(split_path).read_text())["oracle"]}
    out, missing = [], 0
    for r in rows:
        pair = (r["rule_a"], r["rule_b"])
        if pair not in by_pair:
            # NOT the same event as a tie, and the caller must not be allowed to
            # confuse them. A tie is the channel having nothing to say; an absent
            # pair is the wrong split record, and it would quietly shrink the
            # projection's offers instead of failing.
            missing += 1
            out.append(None)
            continue
        v = by_pair[pair]
        out.append(True if v == "a" else False if v == "b" else None)
    return out, missing


def readings_on_this_sample(rows, oracle_dirs, miss_rate, rules, ids, born,
                            instance, engine, n_draws=READING_DRAWS,
                            seed=READING_SEED):
    """
    The coin and the projection, recomputed on THIS sample.

    `edge_budget`'s 0.4519 and 0.4981 sit on a prefix of its own shuffle, and
    this sample is a different 1,600 pairs — §5.1 of the plan is about exactly
    that, and over this population the shuffle's first 400 and Stage D's first
    400 share not one pair. So the lines §0 signed orient the reading and these
    two figures are what it is actually read against.

    The projection flips each oracle direction independently at `miss_rate`,
    which is the assumption `edge_budget` states and labels: the real proposer's
    errors need not be independent nor evenly spread, and B-d is the measurement
    of whether they are. If B-c is refuted while B-d holds, this is the figure
    that says the projection was the wrong model rather than the proposer being
    worse than one.

    The three offer different numbers of edges and the record says so rather
    than leaving it to be noticed: the coin offers one on every pair, the
    projection stays silent on the oracle's ties, and the model stays silent
    wherever it declined.
    """
    # Imported here and not at the top: `edge_budget` imports this module, so a
    # module-level import would close the cycle. The scoring is the closed
    # thread's, called and not copied — rule C of the plan.
    from rung3.edge_budget import score_directions

    coin, projection = [], []
    for k in range(n_draws):
        rnd = random.Random(seed + k)
        coin.append(score_directions(
            rows, [rnd.random() < 0.5 for _ in rows], rules, ids, born,
            instance, engine)[0])
        rnd = random.Random(seed + 100000 + k)
        flipped = [d if d is None or rnd.random() >= miss_rate else not d
                   for d in oracle_dirs]
        projection.append(score_directions(rows, flipped, rules, ids, born,
                                           instance, engine)[0])
    oracle_score, oracle_edges = score_directions(rows, oracle_dirs, rules, ids,
                                                  born, instance, engine)
    def block(draws):
        return {"mean": round(statistics.mean(draws), 6),
                "sd": round(statistics.pstdev(draws), 6),
                "min": round(min(draws), 6), "max": round(max(draws), 6)}
    return {
        "what": "the coin and the projection recomputed on THIS sample rather "
                "than on edge_budget's shuffle prefix, which is a different "
                "1,600 pairs.",
        "n_pairs": len(rows), "n_draws": n_draws, "seed": seed,
        "miss_rate_used": round(miss_rate, 4),
        "miss_rate_source": "1 - B-a's measured rate, space definition",
        "the_projections_assumption":
            "each direction flipped independently and at a uniform rate. Stage C "
            "found the proposer's accuracy varies by queue-pair, so its errors "
            "need not satisfy it; B-d is the measurement of whether they do.",
        "coin": block(coin),
        "projection": block(projection),
        "oracle": round(oracle_score, 6),
        "oracle_edges_accepted": oracle_edges,
        "offers": "the coin offers an edge on every pair, the projection stays "
                  "silent on the oracle's ties, and the model stays silent "
                  "wherever it declined. Three different offer counts, and the "
                  "scores are not interchangeable because of it.",
    }


def not_the_population_for(block, about):
    """
    The same computation on the population the row is NOT about.

    Symmetric with `not_adjudicated_here`, and for the same reason read the other
    way round. P-d and P-e were signed on Stage D's 400 and must not be
    re-adjudicated on 1,600; B-b and B-c are claims about the 1,600 and must not
    read like verdicts when this module runs on the 400. Both directions produce a
    number shaped like a reading, and in both the figure stays and the reading
    goes.
    """
    out = dict(block)
    out.pop("band_holds", None)
    out["adjudicates"] = False
    out["reading_on_another_population"] = block.get("band_holds")
    out["note"] = (
        f"{block['row']} is a claim about {about}. What is here is the same "
        f"computation on Stage D's 400 pairs, reported so the two budgets can be "
        f"compared, and never a reading of the row.")
    return out


def b_b_reading(score, hierarchy_measured):
    """`B-b`: does the order beat what a FREE ranking of the eight queues gets?"""
    return {
        "row": "B-b",
        "claim": "the order the proposer's edges induce beats what a free "
                 "ranking of the eight queues scores",
        "band": f"> {B_B_LINE}", "refuted_by": f"<= {B_B_LINE}",
        "denominator": "the order's score on hibrido, corpus test split 0",
        "line": B_B_LINE, "line_owner": "results3/queue_hierarchy_floor.json",
        "line_as_measured_now": hierarchy_measured,
        "measured": round(score, 6),
        "margin": round(score - B_B_LINE, 6),
        # Compared at the precision the record publishes, for the reason
        # `b_a_reading` gives: a verdict must not turn on a binary
        # representation of a decimal printed as exact.
        "band_holds": round(score, 6) > B_B_LINE,
        "why_it_matters":
            "the ranking reads no rule and costs no call. An order that does not "
            "beat it bought nothing with its budget, whatever it scores against "
            "the arrival floor.",
        "adjudication":
            "`band_holds` is the reading. Whether the row is adjudicated at all "
            "depends on §0 being signed, which is checked where the calls are "
            "made and not here.",
    }


def b_c_reading(score, recomputed):
    """`B-c`: does it reach the projection built from its own measured accuracy?"""
    proj = recomputed["projection"] if recomputed else None
    dev = proj["sd"] if proj else None
    gap = round(score - B_C_LINE, 6)
    return {
        "row": "B-c",
        "claim": "the order reaches the projection made from the proposer's own "
                 "measured accuracy",
        "band": f">= {B_C_LINE}", "refuted_by": f"< {B_C_LINE}",
        "denominator": "the same score — hibrido, corpus test split 0",
        "line": B_C_LINE,
        "line_owner": f"results3/edge_budget.json, budget {READING_BUDGET}",
        "measured": round(score, 6),
        "margin": gap,
        "band_holds": round(score, 6) >= B_C_LINE,
        "read_against_this_sample": recomputed and {
            "projection_mean": proj["mean"], "projection_sd": proj["sd"],
            "coin_mean": recomputed["coin"]["mean"],
            "coin_sd": recomputed["coin"]["sd"],
            "oracle": recomputed["oracle"],
            "gap_in_projection_deviations": (
                round((score - proj["mean"]) / dev, 2) if dev else None),
            "note": "§8: a refutation by less than the projection's own "
                    "deviation is a different event from one by three of them, "
                    "and the record says which. The signed line is the figure "
                    "edge_budget published on ITS shuffle; this is the same "
                    "quantity on the pairs actually asked about.",
        },
        "adjudication":
            "`band_holds` is the reading against the SIGNED line. Whether the "
            "row is adjudicated at all depends on §0 being signed, which is "
            "checked where the calls are made and not here.",
    }


# ---------------------------------------------------------------------------
# Reading what other records own
# ---------------------------------------------------------------------------

def read_floors(path=FLOOR_RECORD):
    rec = json.loads(path.read_text())
    return {(r["pool"], r["surface"]): r["value"] for r in rec["floors"]
            if r["order"] == "born_at" and r["generator"] is None}


def read_hierarchy(path=HIERARCHY_RECORD):
    rec = json.loads(path.read_text())
    return {(r["pool"], r["surface"]): r["stage_c"] for r in rec["rows"]
            if r.get("tiebreak") == "born_at"}


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    t_start = time.time()
    source, out, is_stage_d = parse_source(argv)
    split_path = (Path(argv[argv.index("--split") + 1])
                  if "--split" in argv else None)
    accuracy_path = (Path(argv[argv.index("--accuracy") + 1])
                     if "--accuracy" in argv else None)
    if not source.exists():
        print(f"ABORTED: {source} is not there. Stage D has not run.")
        return 1
    src = json.loads(source.read_text())
    edges = [tuple(e) for e in src["accepted_edges"]]

    corpus, rule_records, ext, conds = load()
    ids = [r["rule_id"] for r in rule_records]
    action = {r["rule_id"]: r["action"] for r in rule_records}
    born = {r["rule_id"]: r["born_at"] for r in rule_records}
    below = subsumption_below(rule_records, ext)
    matched, undef, truth = build_tables(corpus, rule_records, conds, below)
    corpus_pool = {"puro": matched, "hibrido": undef}
    sets = index_sets_of(corpus, truth)
    instances = corpus_instances(ids, corpus_pool, truth, action, sets)
    spools = space_pools(ids, conds, action, below)
    for name in POOLS:
        instances[(SPACE, name)] = spools[name]
    n_space = spools["puro"][3]

    order = topological_order(ids, edges, born)
    g_edges = gate_order_respects_edges(order, edges)
    moved = rules_moved(order, born, ids)

    print("=" * 78)
    print("WHAT THE DECLARED EDGES DO")
    print("=" * 78)
    print(f"  {len(edges)} accepted edges over {len(ids)} rules · "
          f"{moved} rules moved off their arrival position · zero API calls")
    print(f"  {describe()}")
    print(f"  edge gate: {g_edges['n_broken']} broken"
          f"{'  ok' if g_edges['passes'] else '  NO'}")
    if not g_edges["passes"]:
        print("  STOP: the compiled order does not honour the declared edges.")
        return 1

    floors, hier = read_floors(), read_hierarchy()
    tr0, te0 = split(corpus, truth, seed=SPLIT_SEED + SPLIT)

    # --- 1. as a hybrid engine -------------------------------------------
    eng = engine_metrics(learned_rules(), edges, corpus, te0, truth)

    # --- 2. as an order --------------------------------------------------
    as_order = []
    for pool in POOLS:
        for surface in (CORPUS_FULL, "corpus_test_split0", SPACE):
            v = floor(order, instances[(surface, pool)])
            fl = floors.get((pool, surface))
            hv = hier.get((pool, surface))
            as_order.append({
                "pool": pool, "surface": surface, "declared": round(v, 6),
                "born_at_floor": fl, "queue_hierarchy": hv,
                "over_floor": round(v - fl, 6) if fl is not None else None,
                "over_hierarchy": round(v - hv, 6) if hv is not None else None,
            })

    pd_row = next(r for r in as_order if r["pool"] == "hibrido"
                  and r["surface"] == "corpus_test_split0")
    pd_threshold = pd_row["born_at_floor"] + P_D_MARGIN
    p_d = {
        "row": "P-d", "band": f"> floor + {P_D_MARGIN}",
        "refuted_by": f"<= floor + {P_D_MARGIN}",
        "surface": "corpus test split 0, hibrido pool",
        "floor": pd_row["born_at_floor"], "threshold": round(pd_threshold, 6),
        "measured": pd_row["declared"],
        "verdict": "HOLDS" if pd_row["declared"] > pd_threshold else "REFUTED",
        "control_queue_hierarchy": pd_row["queue_hierarchy"],
        "control_note":
            "the queue-ranking order clears the same threshold at zero calls "
            "(results3/queue_hierarchy_floor.json). The verdict above is P-d as "
            "signed; this line is what says whether a hold means anything.",
    }

    print()
    print("=" * 78)
    print("AS AN ORDER — P-d is the hibrido, corpus test split 0 row")
    print("=" * 78)
    print(f"  {'pool':<9}{'surface':<22}{'declared':>10}{'floor':>9}"
          f"{'hierarchy':>11}{'vs floor':>10}{'vs hier':>9}")
    for r in as_order:
        print(f"  {r['pool']:<9}{r['surface']:<22}{r['declared']:>10.4f}"
              f"{r['born_at_floor']:>9.4f}{r['queue_hierarchy']:>11.4f}"
              f"{r['over_floor']:>+10.4f}{r['over_hierarchy']:>+9.4f}")
    print(f"\n  P-d: {p_d['measured']:.4f} against a threshold of "
          f"{p_d['threshold']:.4f}  ->  {p_d['verdict']}")
    print(f"       the free queue ranking scores "
          f"{p_d['control_queue_hierarchy']:.4f} on the same cell")

    # --- the direction control -------------------------------------------
    rows_with_edge = [r for r in src["answers"]
                      if r["declared"] != "none"]
    ctrl = direction_controls(rows_with_edge, learned_rules(), ids, born,
                              instances[("corpus_test_split0", "hibrido")])
    print()
    print("=" * 78)
    print("THE DIRECTION CONTROL — the model's choices, or the compilation?")
    print("=" * 78)
    print(f"  {'the model':<22}{ctrl['model']:>9.4f}")
    print(f"  {'a coin on direction':<22}{ctrl['coin']['mean']:>9.4f}  "
          f"sd {ctrl['coin']['sd']:.4f}   ({ctrl['n_draws']} draws)")
    print(f"  {'the model INVERTED':<22}{ctrl['model_inverted']:>9.4f}")
    print(f"  {'the born_at floor':<22}"
          f"{floors[('hibrido', 'corpus_test_split0')]:>9.4f}")
    print(f"  model sits {ctrl['model_in_coin_deviations']:+.2f} deviations from "
          f"the coin; inverted {ctrl['inverted_in_coin_deviations']:+.2f}")

    # --- B-b and B-c ------------------------------------------------------
    hier_now = pd_row["queue_hierarchy"]
    budget_row = read_budget_row() if BUDGET_RECORD.exists() else None
    g_lines = gate_lines_still_hold(hier_now, budget_row)
    b_b = b_b_reading(pd_row["declared"], hier_now)

    recomputed = None
    if split_path is not None and accuracy_path is not None:
        b_a = json.loads(Path(accuracy_path).read_text()).get("B_a") or {}
        rate = b_a.get("measured")
        if rate is None:
            print("\n  B-c's recomputed baselines need B-a's rate and "
                  f"{accuracy_path} does not carry one.")
        else:
            all_rows = list(src["answers"])
            oracle_dirs, missing = oracle_directions_from_split(all_rows,
                                                                split_path)
            if missing:
                print(f"\n  {missing} of {len(all_rows)} answered pairs are not "
                      f"in {split_path}. That is the wrong split record, not a "
                      f"set of ties, and the projection is NOT built on it.")
            else:
                recomputed = readings_on_this_sample(
                    all_rows, oracle_dirs, 1 - rate, learned_rules(), ids, born,
                    instances[("corpus_test_split0", "hibrido")],
                    fresh_engine(learned_rules()))
    b_c = b_c_reading(pd_row["declared"], recomputed)

    print()
    print("=" * 78)
    print("B-b AND B-c — against the free ranking, and against the projection")
    print("=" * 78)
    if is_stage_d:
        print(f"  NOT A READING OF EITHER ROW: they are claims about {ABOUT},")
        print("  and this is the same computation on Stage D's 400.")
    print(f"  {'the order':<34}{b_b['measured']:>9.4f}")
    print(f"  {'B-b: a free queue ranking':<34}{B_B_LINE:>9.4f}   "
          f"margin {b_b['margin']:+.4f}  "
          f"{'above' if b_b['band_holds'] else 'NOT above'}")
    print(f"  {'B-c: the projection at 1,600':<34}{B_C_LINE:>9.4f}   "
          f"margin {b_c['margin']:+.4f}  "
          f"{'reached' if b_c['band_holds'] else 'NOT reached'}")
    if not g_lines["passes"]:
        print("  WARNING: a line no longer matches the record that owns it — "
              "see the gate. The band stays as signed.")
    if recomputed:
        r = recomputed
        print(f"\n  recomputed on THIS sample ({r['n_draws']} draws, "
              f"miss rate {r['miss_rate_used']}):")
        print(f"    {'coin':<20}{r['coin']['mean']:>9.4f}  "
              f"sd {r['coin']['sd']:.4f}")
        print(f"    {'projection':<20}{r['projection']['mean']:>9.4f}  "
              f"sd {r['projection']['sd']:.4f}")
        print(f"    {'oracle':<20}{r['oracle']:>9.4f}")
        d = b_c["read_against_this_sample"]["gap_in_projection_deviations"]
        if d is not None:
            print(f"    the order sits {d:+.2f} projection deviations from it")

    # --- 3. as a machine, against 65 regenerated on the HYBRID pool -------
    print()
    print("=" * 78)
    print(f"AS A MACHINE — {N_ORDERS} end orders regenerated on the HYBRID pool")
    print("=" * 78)
    t0 = time.time()
    M, W, full = build_masks(ids, undef, truth, action, tr0)
    greedy = greedy_order_from_masks(ids, M, W, full,
                                     tail_key=tail_key_factory(M, W, born))
    _best, st = multistart(declared_starts(ids, first=greedy), M, W, full,
                           neighbourhood=DECLARED_NEIGHBOURHOOD,
                           keep_orders=True)
    ends = [r["order"] for r in st["rows"][:N_ORDERS]]
    print(f"  regenerated in {time.time() - t0:.0f}s "
          f"({DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} starts + the greedy)")

    sM, _sW, sfull, _sn = spools["hibrido"]
    dD, uD = decisions(order, sM, action, sfull)
    dists = []
    for o in ends:
        dO, uO = decisions(o, sM, action, sfull)
        agree, disagree, undec = behavioural_distance(dD, dO, sfull)
        dists.append(disagree / n_space)
    p_e = {
        "row": "P-e", "band": f"median pairwise disagreement <= {P_E_BAND}",
        "refuted_by": f"> {P_E_BAND}",
        "surface": "exhaustive space, hibrido pool, 65 end orders regenerated "
                   "there — never the published puro ones",
        "n_orders": len(dists),
        "median": round(statistics.median(dists), 6),
        "min": round(min(dists), 6), "max": round(max(dists), 6),
        "verdict": "HOLDS" if statistics.median(dists) <= P_E_BAND else "REFUTED",
    }
    print(f"  behavioural distance to the {len(dists)} orders: median "
          f"{p_e['median']:.4f}, min {p_e['min']:.4f}, max {p_e['max']:.4f}")
    print(f"  P-e: {p_e['verdict']}")

    payload = {
        "_env": environment(n_orders=N_ORDERS, split=SPLIT,
                            neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS),
        "what": "what the declared edges of stage D do: as a hybrid engine, as "
                "an order against the floor stage A measured, and as a machine "
                "against 65 end orders regenerated on the hybrid pool. Plus the "
                "queue-ranking control. Zero API calls.",
        "there_is_no_truth_for_the_pairs":
            "no correct-edge rate exists for the 400 pairs and none is computed "
            "anywhere. Every figure here is about what the edges DO.",
        "source": str(source),
        "n_edges": len(edges), "n_rules": len(ids), "n_space": n_space,
        "rules_moved_off_arrival": moved,
        "order_note":
            "topological sort of the declared edges with the ready set drained "
            "in born_at order, so a rule no edge touches keeps its arrival "
            "position. born_at IS the floor, so P-d compares exactly what the "
            "edges added to it — and most of the order is the tie-break, which "
            "is why `rules_moved_off_arrival` is published beside every figure.",
        "gates": {"order_respects_edges": g_edges},
        "as_a_hybrid_engine": eng,
        "as_an_order": as_order,
        "direction_control": ctrl,
        "B_b": not_the_population_for(b_b, ABOUT) if is_stage_d else b_b,
        "B_c": not_the_population_for(b_c, ABOUT) if is_stage_d else b_c,
        "recomputed_on_this_sample": recomputed,
        "gates_on_the_lines": g_lines,
        "P_d": p_d if is_stage_d else not_adjudicated_here(p_d),
        "P_e": p_e if is_stage_d else not_adjudicated_here(p_e),
        "control":
            "the queue-ranking column is read from "
            "results3/queue_hierarchy_floor.json and is the order a fixed "
            "ranking of the eight queues induces, at zero calls. It is reported "
            "beside P-d and never in place of it: P-d is adjudicated on its "
            "signed band.",
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
