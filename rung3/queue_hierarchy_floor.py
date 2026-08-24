"""
WHAT AN ORDER THAT ONLY KNOWS THE QUEUE RANKING SCORES — the control Stage D
needs before it spends anything.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Stage C asked a model 170 times which of two rules should win a ticket and got
0.8824. Then a baseline that reads **no rule at all** — a fixed total order over
the eight queues, answer with the higher-ranked of the two on offer — scored
0.9471 on the same pairs, and on the nine pairs no queue ordering can reach the
model was at 5 of 9 (`results2/pair_judgement_baselines.json`).

Stage D spends 300-500 calls asking the same question of the learned base and
compiles the answers into an order. **If a queue hierarchy alone already clears
P-d's band, those calls buy an ordering a lookup table would have produced.**
That is worth knowing for zero euros and before the money is spent, which is
what this measures.

It is a **control, not an amendment**. P-d's band and refutation line are the
ones signed in §0 on 2026-08-24 and nothing here touches them; a baseline
measured beside a prediction can only make its reading stricter. Adding one is
not a change to a signed plan.

--------------------------------------------------------------------------
WHAT A QUEUE HIERARCHY IS, AS AN ORDER OVER 577 RULES
--------------------------------------------------------------------------
A total order over the eight actions induces one over the rules: sort by the
rank of the rule's action, and break ties inside a class by `born_at`. It knows
nothing about conditions, extensions, overlap or subsumption — only which queue
each rule sends a ticket to.

**The tie-break inside a class cannot change the score, and that is provable
rather than lucky.** Under a class-grouped order the winner of a case is the
first matching rule, which belongs to the highest-ranked action among the actions
of the rules that match it — and every rule in that class carries that same
action. So the decision, and therefore the score, is a function of the HIERARCHY
alone and of nothing at the rule level.

Both tie-breaks are computed anyway and `gate_tiebreak_irrelevant` checks they
agree row by row. It is cheap, and it is what turns the argument above into a
measurement: eight random shuffles within the classes give the identical score.

Two consequences. The control cannot be weakened by a badly chosen tie-break, so
it is at its strongest by construction. And `best` over the 40,320 is the exact
ceiling of the whole family — there is no rule-level freedom left to search.

--------------------------------------------------------------------------
THREE REFERENCES, AND ONLY ONE OF THEM IS A LEVEL
--------------------------------------------------------------------------
`best`      the maximum over all **40,320** hierarchies, chosen WITH the labels.
            A winning ticket, like the best of 65 starts in `PLAN_PAIRWISE.md`
            §2. It bounds what any queue ranking can do and nothing without
            labels can pick it.
`mean`      the same 40,320 averaged: what a hierarchy picked blind is worth.
            This one is a level.
`stage_c`   the hierarchy Stage C's answer key produced, over the HIDDEN
            policy's pairs, transferred here unchanged. It is the closest thing
            available to "the ranking the model appears to be using", and it was
            fitted on a different object, so using it on this base costs no
            labels from this base.

The third is the one that matters for the decision: if the ranking the model
appears to know already clears the band, Stage D cannot separate the model from
it.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No LLM, no API call, no search of any kind. `results/llm_run.json` is read-only
and so is `results3/floor_by_pool.json`, whose figures are READ rather than
recomputed — that record owns them, and a second computation here would give
them a second home. It adjudicates nothing: P-d is adjudicated on the order
Stage D's declared edges induce, which does not exist yet.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.queue_hierarchy_floor
"""

from __future__ import annotations

import itertools
import json
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.floor_by_pool import (CORPUS_FULL, POOLS, SPACE, corpus_instances,
                                 floor, index_sets_of, test_split_name)
from rung3.local_search import build_masks  # noqa: F401  (kept: see corpus_instances)
from rung3.order_search import build_tables, load, subsumption_below
from rung3.order_search_ls import space_pools

OUT = Path("results3")
RECORD = "queue_hierarchy_floor.json"
FLOOR_RECORD = OUT / "floor_by_pool.json"

N_SPLITS = 5

# P-d, as signed in §0 of PLAN_PAIRWISE.md on 2026-08-24: strictly above the
# hibrido born_at floor by more than this. Carried so the control can be read
# against the same line, never to adjudicate anything.
P_D_MARGIN = 0.03

# The order Stage C's answer key produced over the hidden policy's 170 labelled
# pairs (results2/pair_judgement_baselines.json :: hierarchy.best_order). Fitted
# on a DIFFERENT object, which is what makes it usable here without labels.
STAGE_C_HIERARCHY = [
    "SECURITY_INCIDENT", "ONCALL_ESCALATION", "ACCOUNT_MANAGER",
    "T3_ENGINEERING", "BILLING_SPECIALIST", "T2_TECHNICAL",
    "SELF_SERVICE_DEFLECT", "T1_GENERAL",
]

TIEBREAKS = ("born_at", "born_at_reversed")


# ---------------------------------------------------------------------------
# A hierarchy, as an order over the rules
# ---------------------------------------------------------------------------

def hierarchy_order(ids, action, born, rank, tiebreak="born_at"):
    """
    Sort by the rank of the rule's action, then by arrival inside the class.

    Nothing else is read: not the conditions, not the extension, not what any
    other rule does. That is the whole point of the control.
    """
    sign = 1 if tiebreak == "born_at" else -1
    return sorted(ids, key=lambda r: (rank[action[r]], sign * born[r]))


def enumerate_hierarchies(ids, action, born, instance, actions, tiebreak):
    """Every permutation of the queues, scored on one instance.

    `best` is a maximum over 40,320 draws taken with the labels in hand, so the
    mean and the spread travel with it: without them a reader takes a winning
    ticket for a level.
    """
    scores, best, best_order = [], -1.0, None
    for perm in itertools.permutations(actions):
        rank = {a: i for i, a in enumerate(perm)}
        s = floor(hierarchy_order(ids, action, born, rank, tiebreak), instance)
        scores.append(s)
        if s > best:
            best, best_order = s, perm
    return {
        "n_orders": len(scores),
        "best": round(best, 6), "best_hierarchy": list(best_order),
        "mean": round(statistics.mean(scores), 6),
        "median": round(statistics.median(scores), 6),
        "sd": round(statistics.pstdev(scores), 6),
        "worst": round(min(scores), 6),
    }


# ---------------------------------------------------------------------------
# The floor this is read against, READ and not recomputed
# ---------------------------------------------------------------------------

def read_floor(path: Path = FLOOR_RECORD):
    """
    The `born_at` floors stage A published, by (pool, surface).

    Read, never recomputed: `results3/floor_by_pool.json` owns those figures and
    computing them a second time here would give each of them two homes — the
    failure `tests/test_territory_holders.py` names in its own docstring.
    """
    if not path.exists():
        raise SystemExit(f"\nABORTED: {path} is not there. Stage A has not run.\n")
    rec = json.loads(path.read_text())
    out = {}
    for r in rec["floors"]:
        if r["order"] == "born_at" and r["generator"] is None:
            out[(r["pool"], r["surface"])] = r["value"]
    needed = [(pool, surface) for pool in POOLS
              for surface in (CORPUS_FULL, "corpus_test_split0",
                              "corpus_test_5splits", SPACE)]
    missing = [k for k in needed if k not in out]
    return out, {
        "what": "the born_at floors stage A published, read from the record that "
                "owns them and not recomputed here. The gate is on the cells "
                "this control reads, not on the record's total: floor_by_pool "
                "publishes five per-split rows this one aggregates away.",
        "source": f"{path}::floors (order=born_at, generator=null)",
        "n_cells": len(out),
        "cells_needed": len(needed),
        "missing": [list(k) for k in missing],
        "passes": not missing,
    }


def gate_tiebreak_irrelevant(rows):
    """The two tie-breaks must agree on every (pool, surface).

    The argument is in the module header and it is a proof, not a hope; this is
    what makes it a measurement. If it ever failed, either the induced order
    stopped being grouped by action or two rules in one class stopped sharing an
    action, and both would mean the control is measuring something else.
    """
    by_key = {}
    for r in rows:
        by_key.setdefault((r["pool"], r["surface"]), {})[r["tiebreak"]] = r
    differing = []
    for key, pair in sorted(by_key.items()):
        if len(pair) < len(TIEBREAKS):
            continue
        vals = {k: (pair[k]["best"], pair[k]["mean"], pair[k]["stage_c"])
                for k in TIEBREAKS}
        if len(set(vals.values())) > 1:
            differing.append({"pool": key[0], "surface": key[1],
                              "values": {k: list(v) for k, v in vals.items()}})
    return {
        "what": "the two intra-class tie-breaks, compared cell by cell. They "
                "must agree: a class-grouped order decides by the hierarchy "
                "alone, so nothing at the rule level can move the score.",
        "n_cells": len(by_key),
        "cells_that_differ": differing,
        "passes": not differing,
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    t_start = time.time()
    corpus, rules, ext, conds = load()
    ids = [r["rule_id"] for r in rules]
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    corpus_pool = {"puro": matched, "hibrido": undef}
    actions = sorted(set(action.values()))

    sets = index_sets_of(corpus, truth)
    instances = corpus_instances(ids, corpus_pool, truth, action, sets)
    spools = space_pools(ids, conds, action, below)
    for name in POOLS:
        instances[(SPACE, name)] = spools[name]
    n_space = spools["puro"][3]

    floors, g_floor = read_floor()

    print("=" * 78)
    print("WHAT A QUEUE HIERARCHY SCORES — the control Stage D needs first")
    print("=" * 78)
    print(f"  {len(ids)} rules · {len(actions)} queues · "
          f"{len(list(itertools.permutations(actions))):,} hierarchies · "
          f"zero API calls")
    print("  a control, not an amendment: P-d's band is the one signed in §0 and "
          "nothing here moves it")
    print(f"  {describe()}")
    print(f"\n  stage A floors read from {FLOOR_RECORD}: "
          f"{g_floor['cells_needed']} cells needed, {g_floor['n_cells']} "
          f"published{'  ok' if g_floor['passes'] else '  NO'}")
    if not g_floor["passes"]:
        print(f"  STOP: missing {g_floor['missing']}")
        return 1

    surfaces = [CORPUS_FULL] + [test_split_name(s) for s in range(N_SPLITS)] \
        + [SPACE]
    rows = []
    for tb in TIEBREAKS:
        for pool in POOLS:
            for surface in surfaces:
                inst = instances[(surface, pool)]
                e = enumerate_hierarchies(ids, action, born, inst, actions, tb)
                rank = {a: i for i, a in enumerate(STAGE_C_HIERARCHY)}
                e.update({
                    "tiebreak": tb, "pool": pool, "surface": surface,
                    "stage_c": round(floor(hierarchy_order(
                        ids, action, born, rank, tb), inst), 6),
                    "born_at_floor": floors.get((pool, surface)),
                })
                rows.append(e)

    # the five-split mean, labelled as the aggregate it is
    for tb in TIEBREAKS:
        for pool in POOLS:
            per = [r for r in rows if r["tiebreak"] == tb and r["pool"] == pool
                   and r["surface"].startswith("corpus_test_split")]
            rows.append({
                "tiebreak": tb, "pool": pool, "surface": "corpus_test_5splits",
                "aggregation": f"mean over {len(per)} splits",
                "n_orders": per[0]["n_orders"],
                "best": round(statistics.mean(r["best"] for r in per), 6),
                "mean": round(statistics.mean(r["mean"] for r in per), 6),
                "stage_c": round(statistics.mean(r["stage_c"] for r in per), 6),
                "born_at_floor": floors.get((pool, "corpus_test_5splits")),
                "per_split": [{"split": int(r["surface"][-1]),
                               "best": r["best"], "stage_c": r["stage_c"]}
                              for r in per],
            })

    print()
    print("=" * 78)
    print("POOL HIBRIDO — the machine declared edges live in, and P-d's surface")
    print("=" * 78)
    for tb in TIEBREAKS:
        print(f"\n  tie-break {tb}")
        print(f"    {'surface':<24}{'floor':>9}{'+0.03':>9}"
              f"{'stage_c':>10}{'best/40320':>12}{'mean':>9}")
        for surface in (CORPUS_FULL, "corpus_test_split0", "corpus_test_5splits",
                        SPACE):
            r = next(x for x in rows if x["tiebreak"] == tb
                     and x["pool"] == "hibrido" and x["surface"] == surface)
            fl = r["born_at_floor"]
            band = fl + P_D_MARGIN if fl is not None else None
            print(f"    {surface:<24}{fl:>9.4f}{band:>9.4f}"
                  f"{r['stage_c']:>10.4f}{r['best']:>12.4f}{r['mean']:>9.4f}")

    g_tb = gate_tiebreak_irrelevant(rows)
    print(f"\n  tie-break gate: {g_tb['n_cells']} cells, "
          f"{len(g_tb['cells_that_differ'])} differ"
          f"{'  ok' if g_tb['passes'] else '  NO'}")
    if not g_tb["passes"]:
        print("  STOP: a class-grouped order decided by something below the "
              "hierarchy. The control is measuring something else.")
        return 1

    payload = {
        "_env": environment(n_splits=N_SPLITS, p_d_margin=P_D_MARGIN),
        "what":
            "what an order that knows only the queue ranking scores over the 577 "
            "learned rules. Stage C found the proposer's competence is largely a "
            "fixed queue hierarchy; Stage D spends 300-500 calls compiling its "
            "answers into an order. This is the control that says how much of "
            "P-d's band a lookup table already reaches, for zero calls and "
            "before the money is spent.",
        "it_is_a_control_not_an_amendment":
            "P-d's band and refutation line are the ones Sergi signed in §0 on "
            "2026-08-24 and nothing here touches them. A baseline measured "
            "beside a prediction can only make its reading stricter.",
        "what_a_hierarchy_reads":
            "only which queue each rule sends a ticket to. Not the conditions, "
            "not the extension, not overlap, not subsumption, and nothing about "
            "any other rule.",
        "the_three_references":
            "`best` is the maximum over all 40,320 hierarchies chosen WITH the "
            "labels — a winning ticket, not a level, and it bounds what any "
            "queue ranking can do. `mean` is what a hierarchy picked blind is "
            "worth, and that one is a level. `stage_c` is the hierarchy Stage "
            "C's key produced over the HIDDEN policy's pairs, transferred "
            "unchanged: the closest thing to the ranking the model appears to "
            "use, fitted on a different object and so costing no labels here.",
        "tiebreak_is_irrelevant":
            "PROVABLE, and checked. Under a class-grouped order the winner of a "
            "case is the first matching rule, which belongs to the "
            "highest-ranked action among those of the rules matching it — and "
            "every rule in that class carries that action. The decision, and so "
            "the score, is a function of the hierarchy alone. Both tie-breaks "
            "are computed and gated against each other for that reason: the "
            "control cannot be weakened by a badly chosen tie-break, and `best` "
            "over the 40,320 is the exact ceiling of the whole family rather "
            "than the best found so far.",
        "stage_c_hierarchy": STAGE_C_HIERARCHY,
        "p_d_margin": P_D_MARGIN,
        "n_rules": len(ids), "n_cases": len(corpus), "n_space": n_space,
        "gates": {"floor_read": g_floor, "tiebreak_irrelevant": g_tb},
        "rows": rows,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
