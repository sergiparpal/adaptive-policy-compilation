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
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import PriorityEngine, Rule2, Space
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

# P-d and P-e, as signed in §0 of PLAN_PAIRWISE.md on 2026-08-24. Carried so the
# verdicts can be read off, never to be adjusted.
P_D_MARGIN = 0.03
P_E_BAND = 0.25


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
    t_start = time.time()
    if not SOURCE.exists():
        print(f"ABORTED: {SOURCE} is not there. Stage D has not run.")
        return 1
    src = json.loads(SOURCE.read_text())
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
        "source": str(SOURCE),
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
        "P_d": p_d,
        "P_e": p_e,
        "control":
            "the queue-ranking column is read from "
            "results3/queue_hierarchy_floor.json and is the order a fixed "
            "ranking of the eight queues induces, at zero calls. It is reported "
            "beside P-d and never in place of it: P-d is adjudicated on its "
            "signed band.",
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
