"""
WHAT EACH PLACED EDGE DECIDES. `FINDINGS_REASONED_LOOP.md`, *What Stage C does
not settle*, leaves why direction and fill part. `RL-e` reads each placed edge
alone, over its pair's shared region, and the proposer points fewer of them at
the better rule than a fixed ranking of the queues does. The fill reads the
base's points with every edge in place, and there, in the error arm, the same
edges decide more of the order's room right than that ranking does, in every
run, and more than the oracle by direction in e r1. `IDEAS.md` carries the
reading as free on the records: set each edge's verdict beside the points it
decides. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
An edge's verdict and the points it decides can part three ways:
- **Third rules.** `RL-e` reads the better rule over the whole shared region.
  Where a third rule defeats both rules of the pair, the edge decides nothing
  whichever way it points, and its verdict is read on points it does not
  decide. §0 of the plan names this for the transcriber's 71/75.
- **Weight.** `RL-e` weighs each older rule once, and the fill weighs points. An
  edge pointed the wrong way over a few points weighs in `RL-e` as much as one
  that decides thousands.
- **Together.** An edge acts beside the others. The better rule over a pair's
  region need not be the better winner among the rules left standing, and a
  point the edges decide together may be decided by none of them alone.

--------------------------------------------------------------------------
WHAT IT READS, per run, over the half of the space without the keyword
--------------------------------------------------------------------------
The surface is `RL-e`'s and the fill's: the 67,200 points without the keyword.
- **The base** is the fill's declared engine, `authorship.gates.rebuild_final`:
  the run's final rules, then every edge the engine accepted, in the order it
  accepted them. Its right points are `blind.readings.decided_and_right`'s.
- **The room** is `blind.readings.base_of`'s.
- **The edges** are Stage C's rows, `blind.rows.edge_rows` as
  `reasoned_loop.score.read_run` builds them: every edge entered in the graph.
  `RL-e`'s population is `reasoned_loop.score.placed_edge`'s.
- **The reversal** points one edge the other way and leaves every other edge in
  place. It is read by masks, with the engine's own rule: a rule is undefeated
  exactly where no rule that beats it matches. So the loser is no longer
  defeated by the winner, and the winner is defeated by the loser. A reversal
  the engine would refuse, because it closes a cycle, is still read, and
  `closes_cycle` counts it.
- **What an edge decides** is the points of the half whose rightness its
  reversal changes:
  - `gains`, right with the edge as declared and not reversed;
  - `losses`, right reversed and not as declared.
  Both are also counted inside the room.
- **The point verdict** is `rung3.edge_direction.verdict(gains, losses)`: `a`
  when the declared direction decides more of the half right, `b` when the
  reversal does, `tie`, or `neither_ever_right`, which here means that the
  reversal changes no point.
- **The free region** is the shared region less the points where third rules
  defeat both rules of the pair. Only there can the edge decide anything. The
  free verdict reads the better rule there, as `RL-e` reads it over the whole
  shared region, and `governed` counts the rest.
- **The ranking** is `blind.rows.stage_c_names`, the rule `RL-f`'s ranking names,
  read against each verdict on the same edges.
- **Pivotal points** are the room's right points some single reversal changes.
  The rest are decided right by several edges at once, or by none of them
  alone.

The readings, by arm and pooled, over `RL-e`'s population:
  1. its strict pairs, by pair verdict against point verdict;
  2. `RL-e`'s statistic, by older rule, read on the pair verdict as published,
     on the free verdict and on the point verdict, with the ranking beside each
     on the same pairs, and the pair verdict read again on the pairs whose point
     verdict is strict;
  3. the points the reversals change, summed by pair verdict;
  4. the share of each shared region third rules govern, by pair verdict;
  5. by run, the room's right points no single reversal changes.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **Stage C comes back.** `RL-e` and `RL-f`'s ranking, read by
     `reasoned_loop.score.direction` on Stage C's rows, are `score.json`'s
     fractions exactly.
  2. **The fill comes back.** Every run's room, and the share of it the base
     decides right, are `score.json`'s. The masks this module reads the base by
     give `blind.readings.decided_and_right`'s right points.
  3. **One graph.** The fill's engine has Stage C's rules, and Stage C's rows
     are the edges of its graph.
  4. **The reversal is the engine's.** In every run, for the first `RL-e` edges
     whose reversal, installed in place through `try_edge`, is accepted with
     every other edge, the masks give the reinstall's right points: up to
     `GATE_EDGES` of them, from at most `GATE_TRIES` tried, and at least one.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads `RL-e`'s population, and *missing* means a pair whose pair
verdict is `b`: its declared winner is the worse rule over the shared region.

  D1. **Most missing pairs cost nothing.** Over the error arm's runs, fewer than
      half of the missing pairs have point verdict `b`.
  D2. **Where an edge decides points, it decides them right.** `RL-e`'s
      statistic read on the point verdict, by older rule over the error arm's
      runs, is at least 0.90, `RL-e`'s own line.
  D3. **The ranking parts from the points as it parts from the fill.** On the
      point verdicts, the Stage C ranking reads below the declared direction
      over the error arm's runs, and above it over the impasse arm's.
  D4. **Third rules govern the missing pairs.** Over the error arm's runs, the
      median share of the shared region that third rules govern is higher among
      the missing pairs than among the pairs whose pair verdict is `a`.
  D5. **The missing pairs weigh less.** Over the error arm's runs, a reversal
      changes fewer points on average among the missing pairs than among the
      pairs whose pair verdict is `a`.

So the drafter expects the parting to lie in what `RL-e` counts, and not in
what the proposer does: the missing pairs sit mostly on regions third rules
govern, and where an edge does decide points, the proposer pointed it the way
the points ask. The drafter trusts D2 least, then D3, whose impasse half reads
few edges.

**What the drafter had seen**:
- `FINDINGS_REASONED_LOOP.md` whole, every figure in it;
- `STATUS.md`'s and `IDEAS.md`'s entries on `PLAN_REASONED_LOOP.md`;
- `score.json`'s verdicts for `RL-e` and `RL-f`, and its fill by run and arm:
  rooms, edges, the subsumption share and the bound, each arm's share of the
  room, the points it lost and the edges it had refused;
- `reasoned_loop/score.py`, `blind/readings.py`, `blind/rows.py` and
  `rung2/engine2.py`;
- e r2's counts of logged, accepted and distinct edges, and of the edges in its
  graph, while timing a rebuild.

**What the drafter had not seen**: any point verdict, any free verdict, any
governed share, any reversal's points, or any edge row of any run.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for on 2026-11-03, after `PLAN_REASONED_LOOP.md` closed. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. `RL-e` and
`RL-f` stand as signed. Zero API calls.

Usage:  python3 -m reasoned_loop.decided --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m reasoned_loop.decided
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from authorship import gates as egates
from blind import readings as breadings
from blind import rows as brows
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_OK, PriorityEngine
from rung3.edge_direction import verdict

from . import plan, score

F = Fraction
HIT, MISS, TIE, NEITHER = brows.HIT, brows.MISS, brows.TIE, brows.NEITHER
VERDICTS = (HIT, MISS, TIE, NEITHER)
GATE_EDGES = 3                     # gate 4: reversals checked per run
GATE_TRIES = 30                    # gate 4: reversals tried per run, at most
D1_LINE = F(1, 2)                  # holds below it
D2_LINE = plan.RL_E_LINE           # holds at or above it
PROVENANCE = (
    "POST-RUN: asked for on 2026-11-03, after PLAN_REASONED_LOOP.md closed. The "
    "expectation in the module's docstring was written and committed before the "
    "reading ran. Not a signed row; RL-e and RL-f stand as signed.")


def record_path():
    return plan.OUT / "decided.json"


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return score.frac(x)


# ---------------------------------------------------------------------------
# The base by masks, and one edge reversed
# ---------------------------------------------------------------------------

def right_within(undefeated: dict[str, int], action: dict[str, str],
                 tmask: dict[str, int], mask: int) -> int:
    """The points of `mask` decided right: where the undefeated rules carry one
    queue, and it is the true one. `blind.readings.decided_and_right`'s count,
    on a dictionary of masks rather than an engine."""
    by_queue: dict[str, int] = {}
    for rid, m in undefeated.items():
        by_queue[action[rid]] = by_queue.get(action[rid], 0) | (m & mask)
    one = two = 0
    for m in by_queue.values():
        two |= one & m
        one |= m
    only = one & ~two
    right = 0
    for q, m in by_queue.items():
        right |= m & only & tmask[q]
    return right


def defeaters(engine: PriorityEngine, rid: str, without: str | None = None) -> int:
    """Where some rule that beats `rid` matches, leaving out `without`."""
    out = 0
    for b in engine.beats_me(rid):
        if b != without:
            out |= engine.ext[b]
    return out


def reversed_undefeated(engine: PriorityEngine, undefeated: dict[str, int],
                        w: str, l: str) -> dict[str, int]:
    """The undefeated masks with the edge `w` over `l` pointed the other way:
    `l` no longer defeated by `w`, and `w` defeated by `l`."""
    out = dict(undefeated)
    out[l] = engine.ext[l] & ~defeaters(engine, l, without=w)
    out[w] = engine.ext[w] & ~(defeaters(engine, w) | engine.ext[l])
    return out


def closes_cycle(engine: PriorityEngine, w: str, l: str) -> bool:
    """Whether the engine would refuse `l` over `w` for closing a cycle: whether
    `w` reaches `l` by the beats relation without the edge itself."""
    seen, stack = set(), [w]
    while stack:
        cur = stack.pop()
        if cur == l:
            return True
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(n for n in engine.wins_over(cur) if (cur, n) != (w, l))
    return False


def graph_edges(engine: PriorityEngine) -> set[tuple[str, str]]:
    return {(w, l) for l, ws in engine.decl_below.items() for w in ws}


# ---------------------------------------------------------------------------
# One edge, read
# ---------------------------------------------------------------------------

def edge_reading(engine: PriorityEngine, undefeated: dict[str, int], right: int,
                 room: int, action: dict[str, str], tmask: dict[str, int], mask: int,
                 w: str, l: str) -> tuple[dict[str, Any], int]:
    """What reversing `w` over `l` changes, and the pair's free region. Returns
    the reading and the mask of the right points the reversal loses."""
    flipped = right_within(reversed_undefeated(engine, undefeated, w, l), action, tmask, mask)
    gains, losses = right & ~flipped, flipped & ~right
    shared = engine.ext[w] & engine.ext[l] & mask
    governed = shared & defeaters(engine, w) & defeaters(engine, l, without=w)
    free = shared & ~governed
    out = {"gains": gains.bit_count(), "losses": losses.bit_count(),
           "gains_room": (gains & room).bit_count(), "losses_room": (losses & room).bit_count(),
           "point": verdict(gains.bit_count(), losses.bit_count()),
           "shared": shared.bit_count(), "governed": governed.bit_count(),
           "closes_cycle": closes_cycle(engine, w, l)}
    if action[w] != action[l]:
        out["free"] = verdict((free & tmask[action[w]]).bit_count(),
                              (free & tmask[action[l]]).bit_count())
    return out, gains


def world() -> tuple[Any, dict[str, int], int]:
    """The space, its truth, and the half without the keyword."""
    return MI.space(), MI.space_truth(), MI.outside()


def read_run(record: dict, stage_c: dict[str, Any], on: tuple | None = None) -> dict[str, Any]:
    """Every edge of Stage C's rows beside the points it decides. A row that
    repeats an edge carries the edge's reading again, as Stage C counts it."""
    space, tmask, mask = on or world()
    engine, problems = egates.rebuild_final(record, space)
    base = breadings.base_of(record, space, tmask, mask)
    action = {r.rule_id: r.action for r in engine.rules}
    undefeated = brows.undefeated_masks(engine)
    right = right_within(undefeated, action, tmask, mask)
    room = base["room_mask"]
    read: dict[tuple[str, str], dict[str, Any]] = {}
    pivotal = 0
    rows = []
    for row in stage_c["edges"]:
        key = (row["winner"], row["loser"])
        if key not in read:
            read[key], lost = edge_reading(engine, undefeated, right, room, action, tmask,
                                           mask, *key)
            pivotal |= lost
        out = {k: row.get(k) for k in ("winner", "loser", "older", "younger", "queues",
                                       "same_queue", "keyword")}
        out.update(rl_e=score.placed_edge(row), pair=row.get("space_out"), **read[key])
        if not row["same_queue"]:
            out["ranking_names"] = brows.stage_c_names(row)
        rows.append(out)
    room_right = right & room
    return {"engine": engine, "reinstall_problems": problems, "undefeated": undefeated,
            "right": right, "room_mask": room, "action": action,
            "room_points": base["room_points"], "rows": rows,
            "distinct_edges": len(read), "graph_edges": len(graph_edges(engine)),
            "pivotal": {"room_right": room_right.bit_count(),
                        "pivotal": (room_right & pivotal).bit_count(),
                        "by_no_single_reversal": (room_right & ~pivotal).bit_count()}}


# ---------------------------------------------------------------------------
# The readings
# ---------------------------------------------------------------------------

def rl_e(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["rl_e"]]


def strict(r: dict, key: str) -> bool:
    return r.get(key) in (HIT, MISS)


def as_stage_c(rows: list[dict], key: str) -> list[dict]:
    """The rows as `reasoned_loop.score.direction` reads them: `key`'s verdict
    under the name it reads, `space_out`."""
    return [{**r, "space_out": r.get(key)} for r in rows]


def by_older(rows_by_run: list[list[dict]], key: str,
             keep: Callable[[dict], bool] = lambda r: True) -> dict[str, Any]:
    """`RL-e`'s statistic on `key`'s verdict, declared and ranked, exactly."""
    runs = [[r for r in as_stage_c(rows, key) if keep(r)] for rows in rows_by_run]
    keep_all = lambda r: True  # noqa: E731
    declared = score.direction(runs, keep=keep_all)
    ranking = score.direction(runs, keep=keep_all, predict=brows.stage_c_names)
    return {"units": declared["units"], "hits": declared["hits"], "strict": declared["strict"],
            "declared": frac(declared["reading"]), "ranking": frac(ranking["reading"]),
            "declared_exact": declared["reading"], "ranking_exact": ranking["reading"]}


def crosstab(rows: list[dict]) -> dict[str, dict[str, int]]:
    out = {p: {q: 0 for q in VERDICTS} for p in VERDICTS}
    for r in rows:
        out[r["pair"]][r["point"]] += 1
    return out


def points_by_pair(rows: list[dict]) -> dict[str, Any]:
    out = {}
    for p in (HIT, MISS):
        rs = [r for r in rows if r["pair"] == p]
        changed = [r["gains"] + r["losses"] for r in rs]
        out[p] = {"edges": len(rs),
                  "changing": sum(1 for c in changed if c),
                  **{k: sum(r[k] for r in rs) for k in ("gains", "losses", "gains_room",
                                                         "losses_room")},
                  "mean_changed": frac(F(sum(changed), len(changed)) if rs else None),
                  "mean_changed_exact": F(sum(changed), len(changed)) if rs else None}
    return out


def governed_by_pair(rows: list[dict]) -> dict[str, Any]:
    out = {}
    for p in (HIT, MISS):
        shares = [F(r["governed"], r["shared"]) for r in rows if r["pair"] == p and r["shared"]]
        med = statistics.median(shares) if shares else None
        out[p] = {"edges": len(shares), "median_share": frac(med), "median_exact": med,
                  "all_governed": sum(1 for s in shares if s == 1),
                  "none_governed": sum(1 for s in shares if s == 0)}
    return out


def arm_readings(rows_by_run: list[list[dict]]) -> dict[str, Any]:
    pop = [rl_e(rows) for rows in rows_by_run]
    flat = [r for rows in pop for r in rows]
    pairs = [r for r in flat if strict(r, "pair")]
    return {
        "rl_e_rows": len(flat), "strict_pairs": len(pairs),
        "crosstab": crosstab(flat),
        "direction": {
            "pair": by_older(pop, "pair"),
            "free": by_older(pop, "free"),
            "point": by_older(pop, "point"),
            "pair_where_the_point_is_strict": by_older(pop, "pair",
                                                       keep=lambda r: strict(r, "point"))},
        "points_by_pair": points_by_pair(pairs),
        "governed_by_pair": governed_by_pair(pairs),
        "closes_cycle": sum(1 for r in flat if r["closes_cycle"])}


def read_expectation(arms: dict[str, dict]) -> list[dict[str, Any]]:
    e, i = arms["e"], arms["i"]
    missing = e["crosstab"][MISS]
    n_missing = sum(missing.values())
    d1 = F(missing[MISS], n_missing) if n_missing else None
    point_e, point_i = e["direction"]["point"], i["direction"]["point"]
    gov, pts = e["governed_by_pair"], e["points_by_pair"]

    def below(d):
        return (d["ranking_exact"] is not None and d["declared_exact"] is not None
                and d["ranking_exact"] < d["declared_exact"])

    def above(d):
        return (d["ranking_exact"] is not None and d["declared_exact"] is not None
                and d["ranking_exact"] > d["declared_exact"])

    def higher(a, b):
        return a is not None and b is not None and a > b

    return [
        {"clause": "D1", "what": "over the error arm's runs, fewer than half of the missing "
                                 "pairs have point verdict b",
         "reading": {"missing": n_missing, "point_b": missing[MISS], "share": frac(d1)},
         "holds": d1 is not None and d1 < D1_LINE},
        {"clause": "D2", "what": "RL-e's statistic on the point verdict, by older rule over "
                                 "the error arm's runs, is at least 0.90",
         "reading": {"units": point_e["units"], "value": point_e["declared"]},
         "holds": point_e["declared_exact"] is not None and point_e["declared_exact"] >= D2_LINE},
        {"clause": "D3", "what": "on the point verdicts the ranking reads below the declared "
                                 "direction over the error arm, and above it over the "
                                 "impasse arm",
         "reading": {"e": [point_e["ranking"], point_e["declared"]],
                     "i": [point_i["ranking"], point_i["declared"]]},
         "holds": below(point_e) and above(point_i)},
        {"clause": "D4", "what": "over the error arm, third rules govern a higher median share "
                                 "of the shared region among the missing pairs than among "
                                 "the pairs with verdict a",
         "reading": {"b": gov[MISS]["median_share"], "a": gov[HIT]["median_share"]},
         "holds": higher(gov[MISS]["median_exact"], gov[HIT]["median_exact"])},
        {"clause": "D5", "what": "over the error arm, a reversal changes fewer points on "
                                 "average among the missing pairs than among the pairs with "
                                 "verdict a",
         "reading": {"b": pts[MISS]["mean_changed"], "a": pts[HIT]["mean_changed"]},
         "holds": higher(pts[HIT]["mean_changed_exact"], pts[MISS]["mean_changed_exact"])},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def same(a: float | None, b: float | None) -> bool:
    """A float recomputed against one a record keeps: CI runs 3.10 beside 3.12."""
    return a is not None and b is not None and math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-15)


def reinstalled_right(record: dict, w: str, l: str, on: tuple | None = None
                      ) -> tuple[bool, int]:
    """The run's final rules, then its accepted edges in order with `w` over `l`
    pointed the other way, through `try_edge`; whether every edge was accepted,
    and the right points."""
    space, tmask, mask = on or world()
    engine, _ = egates.rebuild_final(record, space, set())
    ok = True
    for a, b in breadings.accepted(record):
        got = engine.try_edge(*((b, a) if (a, b) == (w, l) else (a, b)))
        ok &= got == EDGE_OK
    return ok, breadings.decided_and_right(engine, tmask, mask)[1]


def reversal_gate(record: dict, run: dict[str, Any], on: tuple | None = None
                  ) -> dict[str, Any]:
    eng, und, action = run["engine"], run["undefeated"], run["action"]
    _, tmask, mask = on or world()
    checked = tried = 0
    agree = True
    seen = set()
    for r in run["rows"]:
        key = (r["winner"], r["loser"])
        if not r["rl_e"] or key in seen:
            continue
        seen.add(key)
        if checked >= GATE_EDGES or tried >= GATE_TRIES:
            break
        tried += 1
        ok, got = reinstalled_right(record, *key, on=on)
        if not ok:
            continue
        checked += 1
        agree &= got == right_within(reversed_undefeated(eng, und, *key), action, tmask, mask)
    return {"checked": checked, "tried": tried, "passes": agree and checked >= 1}


def check(records: dict[str, dict], stage_c: dict[str, dict], runs: dict[str, dict],
          published: dict) -> list[dict[str, Any]]:
    out = []
    rows_by_run = [stage_c[t]["edges"] for t in runs]
    d = score.direction(rows_by_run)
    rk = score.direction(rows_by_run, predict=brows.stage_c_names)
    v = published["verdicts"]
    out.append({"gate": 1, "run": "pooled", "what": "RL-e and RL-f's ranking are score.json's",
                "passes": (str(d["reading"]) == v["RL-e"]["value"]["fraction"]
                           and str(rk["reading"]) == v["RL-f"]["ranking"]["fraction"])})
    for t, run in runs.items():
        fill = published["RL-h"]["runs"][t]["fill"]
        mine = breadings.decided_and_right(run["engine"], MI.space_truth(), MI.outside())[1]
        share = F((run["right"] & run["room_mask"]).bit_count(), run["room_points"])
        out.append({"gate": 2, "run": t, "what": "the room and the declared fill are score.json's",
                    "passes": (run["room_points"] == fill["room_points"]
                               and same(float(share), fill["declared"]["right_of_room"])
                               and mine == run["right"])})
        c = stage_c[t]["engine"]
        same_rules = ([(r.rule_id, r.action) for r in c.rules]
                      == [(r.rule_id, r.action) for r in run["engine"].rules]
                      and all(c.ext[r.rule_id] == run["engine"].ext[r.rule_id] for r in c.rules))
        out.append({"gate": 3, "run": t, "what": "one graph: Stage C's rules, and its rows the "
                                                 "graph's edges",
                    "passes": (same_rules and not run["reinstall_problems"]
                               and graph_edges(c) == graph_edges(run["engine"])
                               == {(r["winner"], r["loser"]) for r in run["rows"]})})
        g = reversal_gate(records[t], run)
        out.append({"gate": 4, "run": t, "what": "the reversal is the engine's",
                    "checked": g["checked"], "tried": g["tried"], "passes": g["passes"]})
    return out


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict, dict, dict]:
    by_arm, missing = score.read_records()
    if missing:
        sys.exit(f"\nREFUSED: runs missing: {missing}; nothing was written.\n")
    records = {plan.tag(a, rec["rep"]): rec for a in plan.ARMS for rec in by_arm[a]}
    stage_c = {t: score.read_run(rec) for t, rec in records.items()}
    runs = {t: read_run(records[t], stage_c[t]) for t in records}
    return records, stage_c, runs


def plain(x: Any) -> Any:
    """A record's values: exact fractions dropped where `frac` already gave them."""
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items() if not k.endswith("_exact")}
    if isinstance(x, list):
        return [plain(v) for v in x]
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What each placed edge decides (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"reasoned_loop/decided.py writes {record_path()}")
    published = json.loads(plan.score_path().read_text())
    records, stage_c, runs = read_all()
    checked = check(records, stage_c, runs, published)
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    tags = {a: [t for t in runs if t.startswith(f"{a}_")] for a in plan.ARMS}
    arms = {a: arm_readings([runs[t]["rows"] for t in tags[a]]) for a in plan.ARMS}
    arms["pooled"] = arm_readings([runs[t]["rows"] for t in runs])
    expectation = read_expectation(arms)
    per_run = {t: {"room_points": r["room_points"], "graph_edges": r["graph_edges"],
                   "distinct_edges_read": r["distinct_edges"], "rows": len(r["rows"]),
                   "pivotal": r["pivotal"], "readings": arm_readings([r["rows"]]),
                   "edges": r["rows"]} for t, r in runs.items()}
    record_path().write_text(json.dumps(st._rounded(plain({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"record": str(plan.score_path()),
                   "its_commit": published["_env"].get("git_commit")},
        "surface": "the half of the space without the keyword, 67,200 points",
        "constants": {"GATE_EDGES": GATE_EDGES, "GATE_TRIES": GATE_TRIES,
                      "D1_LINE": str(D1_LINE), "D2_LINE": str(D2_LINE)},
        "gates": checked,
        "arms": arms,
        "runs": per_run,
        "expectation": expectation,
    })), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
