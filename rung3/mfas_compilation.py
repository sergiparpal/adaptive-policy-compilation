"""
IS IT THE ANSWERS OR THE COMPILATION? The same edges, compiled to lose fewer.

--------------------------------------------------------------------------
THE CONTROL THIS IS
--------------------------------------------------------------------------
§12 of `results3/FINDINGS3.md` left exactly two candidates for where the pairwise
channel loses what it is told. On the pairs a queue ranking cannot answer the
oracle's directions reach **+3.33 coin deviations** and the proposer's reach
**−0.58**, so the information is in the protocol and something downstream of it is
discarded. Either

  1. the proposer's errors are correlated in the ranking's direction, so its
     answers do not contain the order however they are compiled; or
  2. the compilation loses it — a topological sort that **refuses** any edge
     closing a cycle, first-come-first-served, and breaks ties by arrival.

**This changes the second while holding the answers completely fixed.** Same 1,479
declared edges, same rules, same cell; only the rule that turns a set of pairwise
claims into a total order. If a compilation that honours more of the same edges
scores no better, candidate 2 is out and the answers are the problem.

--------------------------------------------------------------------------
WHAT THE CURRENT COMPILATION THROWS AWAY, AND WHY IT IS NOT VISIBLE
--------------------------------------------------------------------------
`try_edge` refuses an edge that would close a cycle **in the order it arrives**.
Of 1,479 declared edges, 1,310 were installed and **169 were dropped**, and which
169 depends on nothing but sequence. The resulting order honours every edge it
kept — `gate_order_respects_edges` checks that — so the pipeline looks lossless
from inside while having discarded 11% of what it was told.

**Minimum feedback arc set** asks the opposite question: keep every declared edge,
and find the linear order that violates as few of them as possible. It is NP-hard,
so this is a heuristic and says so; what matters is that it is a *better* answer to
*the same* question, and that its fidelity is measured on all 1,479 rather than on
the subset that survived.

**Both orders are therefore scored on the same fidelity metric**: violations over
the whole declared set. That is the number the two compilations can be compared
on, and neither record so far has published it.

--------------------------------------------------------------------------
THE ONE PROPERTY THAT KEEPS IT COMPARABLE
--------------------------------------------------------------------------
`topological_order` drains its ready set by `born_at`, so **a rule no edge touches
keeps its arrival position** — that is what makes `born_at` the floor and the
comparison *what did the edges add*.

Every start here has the same property and the search preserves it: a rule with
no incident declared edge has a delta of zero at every position, so it is never
moved on its own account and **the untouched rules keep their arrival order
relative to each other**. Their absolute positions shift as constrained rules move
past them — which is equally true of Kahn's algorithm, and is why §11 reports 576
of 577 rules off their arrival index while the comparison against the floor still
means what it says.

**Random restarts are not used.** They would scramble the untouched rules against
each other and change the score for a reason having nothing to do with the edges,
which is the one thing this control cannot afford.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
**It never optimises against the truth.** The objective is violations of declared
edges and nothing else; the truth enters only to score the finished order, exactly
as in every other module here. That separation is the whole point — an optimizer
that saw the labels would be `order_search_ls`, which already reaches 0.7678 and
answers a different question.

It adjudicates nothing. No row of any plan is read and none moves.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.mfas_compilation
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
RECORD = "mfas_compilation.json"
SOURCE = Path("results2/pair_judgement_1600.json")
SPLIT = Path("results2/pair_sample_1600.json")

# Declared before any figure of this module exists.
FAS_MAX_ROUNDS = 200      # passes; the search stops earlier when a pass moves nothing
FAS_SEED = 17
FAS_RANDOM_STARTS = 8     # the optimum check only — never compared to the baseline
COIN_DRAWS = 50
COIN_SEED = 17
SPLIT_SEED = 17

PROVENANCE = (
    "POST-RUN with a stated expectation. Written after §12, by someone who had "
    "already seen the proposer sit at -0.58 coin deviations on the unreachable "
    "side. The expectation below was written BEFORE this module was run and is "
    "NOT a signed row: it is not on STATUS.md's scoreboard and it is not a "
    "calibration event. Zero API calls.")

EXPECTATION = (
    "Written before the run. MFAS honours materially more of the 1,479 declared "
    "edges than the topological compilation, which discards 169 to cycle "
    "refusal. The MODEL's score does not improve materially, because §12 "
    "measured its directions at coin level exactly where the winnable order is, "
    "and compiling noise more faithfully compiles noise. The ORACLE's score does "
    "improve, because those directions carry signal and losing 169 of them is a "
    "real loss. If both improve, the compilation was the bottleneck for both; if "
    "neither does, the sort was losing nothing and the loss is in the answers.")


# ---------------------------------------------------------------------------
# The objective: violations of the declared set
# ---------------------------------------------------------------------------

def declared_edges(rows):
    """`(winner, loser)` per answered pair — every one of them, refused included.

    `try_edge`'s refusals are a property of the COMPILATION, not of what the
    proposer said, so a fidelity metric that dropped them would be scoring the
    baseline against its own choices.
    """
    return [(r["rule_a"], r["rule_b"]) if r["declared"] == "a_beats_b"
            else (r["rule_b"], r["rule_a"])
            for r in rows if r["declared"] != "none"]


def violations(order, edges):
    """Declared edges the order contradicts: the winner placed after the loser."""
    rank = {rid: k for k, rid in enumerate(order)}
    return sum(1 for w, l in edges if rank[w] > rank[l])


def adjacency(edges, ids):
    out = {r: set() for r in ids}
    inc = {r: set() for r in ids}
    for w, l in edges:
        out[w].add(l)
        inc[l].add(w)
    return out, inc


def best_move(order, i, out, inc):
    """
    Where vertex `order[i]` would sit to violate fewest edges, and by how much.

    Moving it past a vertex `u` flips the sense of any edge between them and of
    no other edge, so the delta accumulates in one outward scan: O(n) per vertex
    rather than a rescore. Returns `(best_j, best_delta)` with `best_delta < 0`
    only on a STRICT improvement — which is what leaves a rule with no incident
    edge exactly where it arrived.
    """
    v = order[i]
    ov, iv = out[v], inc[v]
    best_j, best_delta, run = i, 0, 0
    for j in range(i + 1, len(order)):          # later: v ends up after u
        u = order[j]
        run += (1 if u in ov else 0) - (1 if u in iv else 0)
        if run < best_delta:
            best_delta, best_j = run, j
    run = 0
    for j in range(i - 1, -1, -1):              # earlier: v ends up before u
        u = order[j]
        run += (1 if u in iv else 0) - (1 if u in ov else 0)
        if run < best_delta:
            best_delta, best_j = run, j
    return best_j, best_delta


def local_search_fas(order, edges, ids, max_rounds=FAS_MAX_ROUNDS):
    """Reinsertion passes until no vertex moves. Strict improvement only."""
    out, inc = adjacency(edges, ids)
    order = list(order)
    moves = 0
    for _ in range(max_rounds):
        moved = False
        for i in range(len(order)):
            j, delta = best_move(order, i, out, inc)
            if delta < 0:
                v = order.pop(i)
                order.insert(j, v)
                moved, moves = True, moves + 1
        if not moved:
            break
    return order, moves


def net_wins_order(edges, ids, born):
    """Vertices by (wins - losses), ties by arrival. The standard cheap start for
    a tournament, and a different basin from either of the other two."""
    out, inc = adjacency(edges, ids)
    return sorted(ids, key=lambda r: (-(len(out[r]) - len(inc[r])), born[r]))


def mfas_order(edges, ids, born, topo):
    """
    The best order found, over three declared starts.

    **`topo` is one of them and that is not an optimisation detail.** A local
    search started only from `born_at` can finish with MORE violations than the
    baseline it is meant to improve on — it did, by four, on the oracle's edges
    the first time this ran — and a search that loses to the baseline at the
    baseline's own objective cannot say anything about compilation. Including the
    baseline as a start makes `mfas <= topological` true by construction, and
    `gate_beats_the_baseline` checks it rather than trusting it.

    The other two starts are `born_at`, which is the floor every figure in this
    repository is read against, and net wins, which is the cheap tournament
    heuristic and lands in a different basin.
    """
    base = sorted(ids, key=lambda r: born[r])
    starts = {"born_at": base,
              "topological": list(topo),
              "net_wins": net_wins_order(edges, ids, born)}
    best, best_v, best_from, best_moves = None, None, None, 0
    per_start = {}
    for name, start in starts.items():
        order, moves = local_search_fas(start, edges, ids)
        v = violations(order, edges)
        per_start[name] = {"violations_from_this_start": v, "moves": moves}
        if best_v is None or v < best_v:
            best, best_v, best_from, best_moves = order, v, name, moves
    return best, {"starts": per_start, "best_start": best_from,
                  "violations": best_v, "moves": best_moves}


def gate_beats_the_baseline(arm):
    """
    MFAS must violate no more of the declared set than the topological sort.

    Blocking, and it measures the INSTRUMENT before the instrument measures
    anything — the same reason `harness.ceiling_check` runs before any LLM run.
    If the search cannot match the baseline at the baseline's own objective, a
    difference in score between them is a fact about the search.
    """
    t = arm["topological"]["violations_of_the_declared_set"]
    m = arm["mfas"]["violations_of_the_declared_set"]
    return {
        "what": "the FAS search must honour at least as many declared edges as "
                "the topological sort. Otherwise a score difference between the "
                "two compilations is a fact about the search and not about "
                "compilation.",
        "topological_violations": t, "mfas_violations": m,
        "passes": m <= t,
    }


# ---------------------------------------------------------------------------
# One arm: a set of directions, compiled both ways and scored
# ---------------------------------------------------------------------------

def compile_both_ways(rows, dirs, rules, ids, born, instance, engine):
    """The two compilations of the same declared set, with their fidelity."""
    keep = [(r, d) for r, d in zip(rows, dirs) if d is not None]
    edges = [(r["rule_a"], r["rule_b"]) if d else (r["rule_b"], r["rule_a"])
             for r, d in keep]
    base = sorted(ids, key=lambda r: born[r])

    accepted = accepted_from([r for r, _ in keep], [d for _, d in keep], rules,
                             engine)
    topo = topological_order(ids, accepted, born)
    mfas, search = mfas_order(edges, ids, born, topo)

    n = len(edges)
    return {
        "n_declared_edges": n,
        "topological": {
            "edges_installed": len(accepted),
            "edges_refused_as_cycles": n - len(accepted),
            "violations_of_the_declared_set": violations(topo, edges),
            "honoured": n - violations(topo, edges),
            "score": round(floor(topo, instance), 6),
        },
        "mfas": {
            "search": search,
            "violations_of_the_declared_set": violations(mfas, edges),
            "honoured": n - violations(mfas, edges),
            "score": round(floor(mfas, instance), 6),
        },
        "extra_edges_honoured": (violations(topo, edges)
                                 - violations(mfas, edges)),
        "score_gain": round(floor(mfas, instance) - floor(topo, instance), 6),
    }


def main(argv=None) -> int:
    t_start = time.time()
    if not SOURCE.exists() or not SPLIT.exists():
        print(f"ABORTED: {SOURCE} or {SPLIT} is not there.")
        return 1
    rows = [r for r in json.loads(SOURCE.read_text())["answers"]
            if r["declared"] != "none"]
    oracle_by_pair = {}
    for r in json.loads(SPLIT.read_text())["oracle"]:
        v = r["better_space"]
        oracle_by_pair[(r["rule_a"], r["rule_b"])] = (
            True if v == "a" else False if v == "b" else None)

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
    print("IS IT THE ANSWERS OR THE COMPILATION?")
    print("=" * 78)
    print(f"  {len(rows)} declared edges · hibrido, corpus test split 0 · "
          f"zero API calls")
    print("  POST-RUN, with an expectation written before the run and NOT signed")
    print(f"  {describe()}")

    arms = {
        "model": [r["declared"] == "a_beats_b" for r in rows],
        "oracle": [oracle_by_pair[(r["rule_a"], r["rule_b"])] for r in rows],
    }
    rnd = random.Random(COIN_SEED)
    arms["coin"] = [rnd.random() < 0.5 for _ in rows]

    out, gates = {}, {}
    for name, dirs in arms.items():
        out[name] = compile_both_ways(rows, dirs, rules, ids, born, instance,
                                      engine)
        gates[name] = gate_beats_the_baseline(out[name])

    print()
    print("INSTRUMENT GATE — the search must match the baseline on fidelity")
    for name, g in gates.items():
        print(f"  {name:<9}mfas {g['mfas_violations']:>5} violations vs "
              f"topological {g['topological_violations']:>5}"
              f"{'   ok' if g['passes'] else '   NO'}")
    if not all(g["passes"] for g in gates.values()):
        print("\n  STOP: the FAS search loses to the baseline at the baseline's")
        print("  own objective. A score difference would be a fact about the")
        print("  search. Nothing is written.")
        return 1

    print()
    print(f"  {'arm':<9}{'edges':>7}{'topo hon.':>11}{'mfas hon.':>11}"
          f"{'+held':>7}{'topo':>9}{'mfas':>9}{'gain':>9}")
    for name in ("model", "oracle", "coin"):
        r = out[name]
        print(f"  {name:<9}{r['n_declared_edges']:>7}"
              f"{r['topological']['honoured']:>11}{r['mfas']['honoured']:>11}"
              f"{r['extra_edges_honoured']:>+7}"
              f"{r['topological']['score']:>9.4f}{r['mfas']['score']:>9.4f}"
              f"{r['score_gain']:>+9.4f}")
    print(f"  {'born_at':<9}{'':>7}{'':>11}{'':>11}{'':>7}{floor_born:>9.4f}")

    payload = {
        "_env": environment(fas_seed=FAS_SEED, coin_seed=COIN_SEED,
                            fas_max_rounds=FAS_MAX_ROUNDS),
        "what": "the same 1,479 declared edges compiled two ways — the "
                "topological sort that refuses cycle-closing edges as they "
                "arrive, and a minimum-feedback-arc-set search that keeps every "
                "edge and minimises violations. Zero API calls.",
        "provenance": PROVENANCE,
        "expectation_written_before_the_run": EXPECTATION,
        "adjudicates_nothing":
            "no row of any plan is read here and none moves. This is a control "
            "for §12, not a prediction anyone signed.",
        "the_objective_never_sees_the_truth":
            "the search minimises violations of declared edges and nothing else. "
            "The truth enters only to score the finished order, as in every "
            "other module here. An optimizer that saw the labels would be "
            "order_search_ls, which answers a different question.",
        "why_it_stays_comparable":
            "the search starts from born_at and moves a vertex only on strict "
            "improvement, so a rule with no incident declared edge has delta "
            "zero everywhere and keeps its arrival position — the property that "
            "makes born_at the floor and the comparison `what did the edges "
            "add`.",
        "fidelity_is_measured_on_all_declared_edges":
            "including the ones try_edge refused. A refusal is a property of the "
            "compilation, not of what the proposer said, so scoring the baseline "
            "only on the edges it chose to keep would score it against its own "
            "choices.",
        "surface": "hibrido pool, corpus test split 0",
        "source": str(SOURCE), "split": str(SPLIT),
        "born_at_floor": round(floor_born, 6),
        "gates": gates,
        "arms": out,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
