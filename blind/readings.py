"""
WHAT K-d'S FILL WOULD BE UNDER OTHER DIRECTIONS. `K-d` held: the edges the three
runs installed fill a share of the order's room over the half of the space
without the keyword that clears its line. Its statistic may reward resolving, as
`W-c`'s did. This reads what the same edges fill when something other than the
proposer chooses their direction. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
The room is the points where some rule subsumption leaves undefeated carries the
true queue and subsumption alone does not decide it right: nearly all of them are
points where rules of different queues are left in conflict. An edge between two
such rules resolves the point whichever way it points, and is right there about
as often as its direction is. So a fill can come from resolving as much as from
pointing right, and `K-b` read the declared direction beyond the keyword near a
coin's. `PLAN_EDGES.md`'s `W-c` counted right decisions and so rewarded
resolution; `CLAUDE.md` asks that a coin control over declared edges compare
accuracy among the cases each arm resolves. This reading does both.

--------------------------------------------------------------------------
WHAT IT READS, per run, over the half of the space without the keyword
--------------------------------------------------------------------------
Every arm installs the same edges, the ones the engine accepted in the run, in
the order it accepted them, through `try_edge`, on the run's final rules. An edge
between two rules of one queue keeps its declared direction in every arm: no
direction makes it right or wrong. Each other edge is pointed:

  declared  as the proposer declared it: `K-d` itself.
  coin      by a fair coin, `N_COIN` draws seeded by `COIN_SEED`, the run and the
            draw. An edge the engine refuses, because it would close a cycle or
            contradict subsumption, is left out and counted.
  ranking   at the rule whose queue rung 3's Stage C hierarchy ranks higher.
  newborn   at the rule born later.
  oracle    at the better rule over its shared region on the half without the
            keyword; a tie, or a pair neither rule is ever right on there, keeps
            the declared direction. What the best direction of each edge alone
            could fill.

For each arm: the fill, `K-d`'s share; the share of the room it resolves, and
the share of what it resolves that it gets right; the points subsumption alone
decided right that it gets wrong; and the edges refused. For the coin, each of
these as a mean and a deviation over the draws, and the share of draws that do at
least as well as the declared arm. On the 1,929 corpus cases without the keyword
the deterministic arms' fills are reported, and nothing is read for the coin.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The declared arm is `K-d`**: per run its share equals `score.json`'s.
  2. **It is the run's graph**: with the declared directions every accepted edge
     re-installs as accepted.
  3. **The coin is a function of its seed**: each run's first draw, drawn twice,
     gives the same fill.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  1. **A coin fills about half.** The coin's mean fill is between 0.40 and 0.60
     in every run.
  2. **The declared fill is a coin's.** It sits inside the central 90% of the
     coin's draws in at least two runs of three.
  3. **Part of the declared arm's lead is resolution.** In every run the declared
     arm resolves more of the room than the coin does on average, because a
     coin's directions close cycles the declared ones did not.
  4. **A ranking fills more.** The ranking arm's fill is above the declared
     arm's in every run.
  5. **The edges themselves can order.** The oracle arm fills at least 0.85 of
     the room in every run.

**What the drafter had seen**: `score.json`, with `K-d` per run, its rooms and
its fills by channel, on the corpus and over the whole space; `K-b`'s direction
by older rule and the ranking's on the same pairs; `B-d`'s split; and the runs'
declarations by verdict, which give run 1's 32 refused for closing a cycle. The
first clause follows from the room's makeup if it is mostly conflicts between two
rules, and the third from that cycle count, so both are close to known for run 1.
**The second, the fourth and the fifth are the bets.** Not seen: any fill under
any direction but the declared one.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_BLIND.md`'s verdicts existed, with the
expectation above written before the reading and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. `K-d`
stands as signed. Zero API calls.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: K-b, K-c AND K-e RUN BY RUN
--------------------------------------------------------------------------
§0 says each run's own value is published beside every row's reading, and
`score.json` pools the edges of K-b, K-c and K-e over the runs without giving
each run's. `per_run_directions` reads them off `score.json`'s own edge rows, run
by run, with the instrument that pooled them: a decomposition of three published
rows, not a measurement, and no expectation goes with it. Added in its own
commit, after the first run of this module; the record comes from a second run,
which must give back every figure of the first.

Usage:  PYTHONHASHSEED=0 python3 -m blind.readings
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from typing import Any, Callable

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from authorship import gates as egates
from reuse import structure as st
from rung2.engine2 import EDGE_OK, PriorityEngine, Space
from rung3.edge_direction import better_over_space, verdict
from rung3.order_search_ls import space_truth_masks
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from . import plan, rows

READ_PATH = plan.OUT / "readings.json"
N_COIN = 200                       # draws per run, fixed before the reading
COIN_SEED = 17
COIN_BAND = (0.40, 0.60)           # clause 1
CENTRAL = 0.90                     # clause 2
ORACLE_MIN = 0.85                  # clause 5
PROVENANCE = (
    "POST-RUN: asked for after PLAN_BLIND.md's verdicts existed. The expectation "
    "in the module's docstring was written before the reading and committed before "
    "it ran. Not a signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# The arms
# ---------------------------------------------------------------------------

def accepted(record: dict) -> list[tuple[str, str]]:
    """Every edge the engine accepted in the run, in the order it accepted it."""
    return [(w, l) for w, l, why in record.get("edge_log") or [] if why == EDGE_OK]


def install(record: dict, space: Space, point: Callable[[str, str], tuple[str, str]]
            ) -> tuple[PriorityEngine, dict[str, int]]:
    """The run's final rules, then its accepted edges in order, each pointed by
    `point`, through `try_edge`. Returns the engine and the verdicts."""
    engine, _ = egates.rebuild_final(record, space, set())
    verdicts: dict[str, int] = {}
    for w, l in accepted(record):
        why = engine.try_edge(*point(w, l))
        verdicts[why] = verdicts.get(why, 0) + 1
    return engine, verdicts


def pointers(record: dict, ext: dict[str, int], tmask_out: dict[str, int],
             rng: random.Random | None = None) -> dict[str, Callable]:
    """How each arm points an edge between two queues; within a queue, as declared."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    born = {r["rule_id"]: (r["born_at"], r["rule_id"]) for r in record["rules"]}
    rank = {q: i for i, q in enumerate(STAGE_C_HIERARCHY)}

    def same(w, l):
        return action[w] == action[l]

    def declared(w, l):
        return w, l

    def ranking(w, l):
        if same(w, l):
            return w, l
        return (w, l) if rank[action[w]] < rank[action[l]] else (l, w)

    def newborn(w, l):
        if same(w, l):
            return w, l
        return (w, l) if born[w] > born[l] else (l, w)

    def oracle(w, l):
        if same(w, l):
            return w, l
        v = verdict(*better_over_space(w, l, ext, action, tmask_out))
        return (l, w) if v == rows.MISS else (w, l)

    out = {"declared": declared, "ranking": ranking, "newborn": newborn, "oracle": oracle}
    if rng is not None:
        out["coin"] = lambda w, l: (w, l) if same(w, l) or rng.random() < 0.5 else (l, w)
    return out


# ---------------------------------------------------------------------------
# What an arm does over the half without the keyword
# ---------------------------------------------------------------------------

def decided_and_right(engine: PriorityEngine, tmask: dict[str, int], mask: int
                      ) -> tuple[int, int]:
    """The points of `mask` the engine decides, and those it decides right, as
    masks: a point is decided where the undefeated rules carry one queue."""
    action = {r.rule_id: r.action for r in engine.rules}
    by_queue: dict[str, int] = {}
    for rid, m in rows.undefeated_masks(engine).items():
        by_queue[action[rid]] = by_queue.get(action[rid], 0) | (m & mask)
    one = two = 0
    for m in by_queue.values():
        two |= one & m
        one |= m
    only = one & ~two
    right = 0
    for q, m in by_queue.items():
        right |= m & only & tmask[q]
    return only, right


def arm_reading(engine: PriorityEngine, base: dict[str, Any], tmask: dict[str, int],
                mask: int, refused: dict[str, int]) -> dict[str, Any]:
    """`K-d`'s share for this engine, and what it resolves and gets right in the
    room, against subsumption alone (`base`)."""
    decided, right = decided_and_right(engine, tmask, mask)
    n = mask.bit_count()
    room = base["room_mask"]
    e2e = right.bit_count() / n
    resolved = (decided & room).bit_count()
    right_in_room = (right & room).bit_count()
    return {
        "share": egates.share(e2e, base["alone"], base["bound"]),
        "resolved_of_room": resolved / base["room_points"] if base["room_points"] else None,
        "right_of_resolved": right_in_room / resolved if resolved else None,
        "right_of_room": right_in_room / base["room_points"] if base["room_points"] else None,
        "lost": (base["alone_right"] & ~right).bit_count(),
        "refused": {k: x for k, x in refused.items() if k != EDGE_OK},
    }


def base_of(record: dict, space: Space, tmask: dict[str, int], mask: int) -> dict[str, Any]:
    """Subsumption alone over `mask`, and the room: the points some undefeated
    rule gets right that subsumption alone does not decide right."""
    alone, _ = egates.rebuild_final(record, space, set())
    action = {r.rule_id: r.action for r in alone.rules}
    reach = 0
    for rid, m in rows.undefeated_masks(alone).items():
        reach |= m & tmask[action[rid]]
    _decided, alone_right = decided_and_right(alone, tmask, mask)
    n = mask.bit_count()
    room_mask = reach & mask & ~alone_right
    return {"alone": alone_right.bit_count() / n, "bound": (reach & mask).bit_count() / n,
            "room_mask": room_mask, "room_points": room_mask.bit_count(),
            "alone_right": alone_right}


def read_run(record: dict, rep: int, space: Space, tmask: dict[str, int], outside: int,
             corpus, cases_out: list[int]) -> dict[str, Any]:
    ext = {r["rule_id"]: rows.ext_of(r, space) for r in record["rules"]}
    t_out = rows.restrict(tmask, outside)
    base = base_of(record, space, tmask, outside)
    out: dict[str, Any] = {"room_points": base["room_points"], "alone": base["alone"],
                           "bound": base["bound"], "edges": len(accepted(record))}
    fixed = pointers(record, ext, t_out)
    labels = egates.labels_of(record)
    sub = [corpus[i] for i in cases_out]
    lab = [labels[i] for i in cases_out]
    for name, point in fixed.items():
        engine, verdicts = install(record, space, point)
        out[name] = arm_reading(engine, base, tmask, outside, verdicts)
        out[name]["corpus_e2e"] = egates.on_corpus(engine, sub, lab)["e2e"]
    draws = []
    for k in range(N_COIN):
        rng = random.Random(f"{COIN_SEED}/{rep}/{k}")
        engine, verdicts = install(record, space, pointers(record, ext, t_out, rng)["coin"])
        draws.append(arm_reading(engine, base, tmask, outside, verdicts))
    out["coin"] = summary_of_draws(draws, out["declared"])
    return out


def summary_of_draws(draws: list[dict], declared: dict) -> dict[str, Any]:
    out: dict[str, Any] = {"draws": len(draws)}
    for key in ("share", "resolved_of_room", "right_of_resolved", "right_of_room"):
        xs = [d[key] for d in draws if d[key] is not None]
        if not xs:
            out[key] = None
            continue
        xs.sort()
        lo = xs[round(len(xs) * (1 - CENTRAL) / 2)]
        hi = xs[round(len(xs) * (1 + CENTRAL) / 2) - 1]
        out[key] = {"mean": statistics.mean(xs), "sd": statistics.pstdev(xs),
                    "central": [lo, hi],
                    "at_least_declared": (sum(1 for x in xs if x >= declared[key]) / len(xs)
                                          if declared[key] is not None else None)}
    refusals = [sum(d["refused"].values()) for d in draws]
    out["refused_mean"] = statistics.mean(refusals)
    out["draws_with_a_refusal"] = sum(1 for x in refusals if x)
    return out


# ---------------------------------------------------------------------------
# Added after the first run: K-b, K-c and K-e run by run
# ---------------------------------------------------------------------------

def per_run_directions(score: dict) -> dict[str, Any]:
    """K-b's, K-c's and K-e's readings for each run alone, off `score.json`'s
    edge rows, with `rows.comparators`, the function that pooled them. The pooled
    readings are given back beside them, and must equal `score.json`'s."""
    def one(edge_rows_by_run):
        space_ = rows.comparators(edge_rows_by_run, "space_out")
        corpus_ = rows.comparators(edge_rows_by_run, "corpus_out")
        kb, rank, ke = space_["declared"], space_["stage_c_ranking"], corpus_["declared"]
        return {"K-b": {k: kb[k] for k in ("units", "reading", "hits", "strict")},
                "K-c": (None if kb["reading"] is None or rank["reading"] is None
                        else kb["reading"] - rank["reading"]),
                "ranking": rank["reading"],
                "K-e": {k: ke[k] for k in ("units", "reading", "hits", "strict")}}
    out = {str(r["rep"]): one([r["edge_rows"]]) for r in score["runs"]}
    out["pooled"] = one([r["edge_rows"] for r in score["runs"]])
    return out


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def check(score: dict, records: dict[int, dict], runs: dict[int, dict], space: Space,
          tmask: dict[str, int], outside: int) -> list[dict]:
    by_rep = {r["rep"]: r for r in score["runs"]}
    out = []
    for rep, got in runs.items():
        published = by_rep[rep]["K-d"]
        out.append({"gate": 1, "rep": rep, "what": "the declared arm is K-d",
                    "measured": got["declared"]["share"], "published": published,
                    "passes": (got["declared"]["share"] is not None and published is not None
                               and round(got["declared"]["share"], 6) == round(published, 6))})
        out.append({"gate": 2, "rep": rep, "what": "it is the run's graph",
                    "passes": not got["declared"]["refused"]})
        ext = {r["rule_id"]: rows.ext_of(r, space) for r in records[rep]["rules"]}
        t_out = rows.restrict(tmask, outside)
        base = base_of(records[rep], space, tmask, outside)
        twice = []
        for _ in range(2):
            rng = random.Random(f"{COIN_SEED}/{rep}/0")
            engine, verdicts = install(records[rep], space,
                                       pointers(records[rep], ext, t_out, rng)["coin"])
            twice.append(arm_reading(engine, base, tmask, outside, verdicts)["share"])
        out.append({"gate": 3, "rep": rep, "what": "the coin is a function of its seed",
                    "passes": twice[0] == twice[1]})
    return out


def read_expectation(runs: dict[int, dict]) -> list[dict]:
    reps = sorted(runs)

    def inside(r):
        lo, hi = runs[r]["coin"]["share"]["central"]
        return lo <= runs[r]["declared"]["share"] <= hi

    coin_means = {r: runs[r]["coin"]["share"]["mean"] for r in reps}
    return [
        {"clause": 1, "what": "the coin's mean fill is between 0.40 and 0.60 in every run",
         "reading": coin_means,
         "holds": all(COIN_BAND[0] <= x <= COIN_BAND[1] for x in coin_means.values())},
        {"clause": 2, "what": "the declared fill is inside the coin's central 90% in at "
                              "least two runs of three",
         "reading": {r: inside(r) for r in reps},
         "holds": sum(inside(r) for r in reps) >= 2},
        {"clause": 3, "what": "the declared arm resolves more of the room than the coin's "
                              "mean in every run",
         "reading": {r: [runs[r]["declared"]["resolved_of_room"],
                         runs[r]["coin"]["resolved_of_room"]["mean"]] for r in reps},
         "holds": all(runs[r]["declared"]["resolved_of_room"]
                      > runs[r]["coin"]["resolved_of_room"]["mean"] for r in reps)},
        {"clause": 4, "what": "the ranking fills more than the declared arm in every run",
         "reading": {r: [runs[r]["ranking"]["share"], runs[r]["declared"]["share"]]
                     for r in reps},
         "holds": all(runs[r]["ranking"]["share"] > runs[r]["declared"]["share"]
                      for r in reps)},
        {"clause": 5, "what": "the oracle fills at least 0.85 of the room in every run",
         "reading": {r: runs[r]["oracle"]["share"] for r in reps},
         "holds": all(runs[r]["oracle"]["share"] >= ORACLE_MIN for r in reps)},
    ]


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"blind/readings.py writes {READ_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    space = Space()
    tmask = space_truth_masks(space)
    outside = rows.outside_mask(space)
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    cases_out = rows.outside_cases(corpus)
    records = {rep: json.loads(plan.run_path(rep).read_text())
               for rep in range(1, plan.REPS + 1)}
    runs = {rep: read_run(records[rep], rep, space, tmask, outside, corpus, cases_out)
            for rep in records}
    checked = check(score, records, runs, space, tmask, outside)
    by_run = per_run_directions(score)
    v = score["verdicts"]
    checked.append({"gate": 4, "rep": "pooled",
                    "what": "the run-by-run decomposition pools back to K-b, K-c and K-e",
                    "passes": (round(by_run["pooled"]["K-b"]["reading"], 6) == v["K-b"]["reading"]
                               and round(by_run["pooled"]["K-c"], 6) == v["K-c"]["reading"]
                               and round(by_run["pooled"]["K-e"]["reading"], 6)
                               == v["K-e"]["reading"])})
    for g in checked:
        print(f"  gate {g['gate']} run {g['rep']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    READ_PATH.write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "its_commit": score["_env"].get("git_commit")},
        "surface": "the half of the space without the keyword, 67,200 points; the "
                   "corpus cases without it reported for the deterministic arms",
        "constants": {"N_COIN": N_COIN, "COIN_SEED": COIN_SEED},
        "gates": checked,
        "runs": {str(rep): r for rep, r in runs.items()},
        "expectation": read_expectation(runs),
        "added_after_the_first_run": {
            "what": "K-b, K-c and K-e run by run, off score.json's edge rows; a "
                    "decomposition of published rows, with no expectation",
            "per_run_directions": by_run},
    }), indent=2, default=str) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
