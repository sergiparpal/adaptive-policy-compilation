"""
§16'S CUTS OVER THE FUNCTION. The queue cut, and the headroom it was read
inside, scored on the exhaustive space.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
§16 read seven cuts of the 1,600 run's declared edges against a same-size random
choice, and one came near the ceiling: dropping the edges whose stated reason is
a queue's importance, mostly the security keyword. §16 named three things that
keep it a lead, and one of them is free to settle: **it was measured on the
corpus only.** The keyword is 3% of the arrivals and half of the space, and over
the function the write-time edges of that rule of thumb point at the better rule
three times in four. So the same cut was expected to cost on the space, and
nothing had measured it there.

This module re-reads every selection §16 compiled, scored on the `hibrido` pool
over the 134,400 points of the exhaustive space. **It does not test the lead
itself**: that needs a population the lead was not found on, which means new
answers. It asks whether the lead belongs to the surface.

--------------------------------------------------------------------------
WHAT IT MEASURES
--------------------------------------------------------------------------
Everything §16 measured, compiled the same way and from the same draws: the
random control kept in arrival order at every size a filter cuts, the oracle and
anti selections under both definitions of the better rule, §14's shuffled control
at §14's sizes, and the eight filters. Each compiled order is scored twice:

  corpus   §16's cell, the `hibrido` pool on corpus test split 0. Only a gate:
           every figure must reproduce `results3/filter_headroom.json`, and none
           is written again, because that record owns them.
  space    the `hibrido` pool over the exhaustive space. What is new.

Beside them, as diagnostics: how often each cut's edges point at the better rule
under each definition, and which queue the edges of the two queue cuts name.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **§16 reproduces, to the digit**: the `born_at` floor, the controls at
     every size, the oracle and anti selections, §14's shuffled controls and the
     eight filters, exactly as `results3/filter_headroom.json` holds them. So the
     orders scored on the space are §16's orders.
  2. **The space is the published one**: `born_at` scores
     `results3/queue_hierarchy_floor.json`'s floor for `hibrido` over the space,
     and `keep_all` compiled topologically scores
     `results3/declared_order_1600.json`'s figure on the same cell.

The module refuses to write if either fails.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE RUN AND NOT SIGNED
--------------------------------------------------------------------------
On the space the queue cut reverses.

  1. `no_queue` lands below its same-size random control, in both
     compilations.
  2. `queue` lands above its same-size random control, in both compilations.
  3. The reversal is weaker than the corpus gain: `no_queue`'s MFAS reading on
     the space is smaller in absolute value than its +2.52 on the corpus.

The reasons. The queue edges are mostly the security keyword, half of the space
against 3% of the arrivals. Over the function the write-time edges of that rule
of thumb point at the better rule three times in four, and the held-out batch's
`queue` answers name it more often than the rest do. But that advantage is small
on the space, and development has it the other way, against a gap on the corpus
that is larger and has the same sign in both batches. `EXPECTED` carries the
three clauses in a form the module reads mechanically.

**What the drafter had seen**, declared so that the expectation can be weighed:
everything §16 publishes, on the corpus. On the space, three figures and no
selection: `keep_all` compiled topologically, 0.5463 on `hibrido`
(`declared_order_1600.json`), the free queue ranking, 0.5838, and the `born_at`
floor, 0.4257 (`queue_hierarchy_floor.json`). The direction rates by code that
`FINDINGS_WHY.md` publishes: on the held-out batch `queue` answers name the
better rule 0.8008 of the time on the space and 0.6300 on the corpus, against
0.7424 and 0.6860 for all of them, and in development the `queue` answers were
behind the rest on both. And `FINDINGS_EDGES.md`'s `W-b`: the write-time edges,
nearly all the same rule of thumb, point at the better rule three times in four
over the function. No score of any selection or filter on the space had been
computed.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN with an expectation written before the run**, in this module and in
its record, and committed before it ran. Not a signed row, not on `STATUS.md`'s
scoreboard, not a calibration event. Zero API calls.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN, AND LABELLED SO
--------------------------------------------------------------------------
The first run put `no_queue` in MFAS eleven deviations below its control, far
under every anti selection, so `post_run` says where that loss sits: for each
filter's two orders, the cases of the space each queue decides and decides
right, beside how many cases of the space each queue is the truth for; and the
winners `queues_named` reads now cover every filter, not two. It was written
after the readings above existed, it reads nothing they did not, and it changes
none of them. §17 of `FINDINGS3.md` says whether the run from the commit that
added it reproduced the first run's figures.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.filter_space
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
from rung3.declared_order import accepted_from, fresh_engine, topological_order
from rung3.edge_direction import agreement
from rung3.edge_dropping import revealed_ranking
from rung3.filter_headroom import (DRAWS, SAMPLE, SEED, SHUFFLED_FILTERS, SOURCE,
                                   deviations, filters, in_arrival_order,
                                   oracle_rank, select, shuffled)
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.mfas_compilation import mfas_order
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import space_pools, space_truth_masks

OUT = Path("results3")
RECORD = "filter_space.json"
HEADROOM = Path("results3/filter_headroom.json")
DECLARED = Path("results3/declared_order_1600.json")
HIERARCHY = Path("results3/queue_hierarchy_floor.json")

SPLIT_SEED = 17
SURFACES = ("corpus", "space")
COMPILATIONS = ("topological", "mfas")
# The parts of §16's record gate 1 compares, which is all of its figures.
GATED = ("born_at_floor", "headroom_by_size", "shuffled_controls_at_14s_sizes",
         "filters")
CORPUS_MFAS_NO_QUEUE = 2.52        # §16's reading, the line clause 3 is read against

PROVENANCE = (
    "POST-RUN with an expectation written before the run, in the module and in "
    "this record, and committed before it ran. Not a signed row, not on "
    "STATUS.md's scoreboard, not a calibration event. Zero API calls.")

EXPECTATION = (
    "Written before the run and committed before it ran. On the space the queue "
    "cut reverses. (1) `no_queue` lands below its same-size random control, in "
    "both compilations. (2) `queue` lands above its same-size random control, in "
    "both compilations. (3) The reversal is weaker than the corpus gain: "
    "`no_queue`'s MFAS reading on the space is smaller in absolute value than its "
    "+2.52 on the corpus. The reasons: the queue edges are mostly the security "
    "keyword, half of the space against 3% of the arrivals. Over the function the "
    "write-time edges of that rule of thumb point at the better rule three times "
    "in four, and the held-out batch's `queue` answers name it more often than the "
    "rest do. But that advantage is small on the space, and development has it the "
    "other way, against a gap on the corpus that is larger and has the same sign "
    "in both batches.")

SEEN = (
    "Everything §16 publishes, on the corpus. On the space, three figures and no "
    "selection: keep_all compiled topologically, 0.5463 on hibrido "
    "(declared_order_1600.json), the free queue ranking, 0.5838, and the born_at "
    "floor, 0.4257 (queue_hierarchy_floor.json). The direction rates by code in "
    "FINDINGS_WHY.md: on the held-out batch `queue` answers name the better rule "
    "0.8008 of the time on the space and 0.6300 on the corpus, against 0.7424 and "
    "0.6860 for all, and in development the `queue` answers were behind the rest "
    "on both. FINDINGS_EDGES.md's W-b: the write-time edges point at the better "
    "rule three times in four over the function. No score of any selection or "
    "filter on the space had been computed.")

# The three clauses of EXPECTATION, as (filter, compilation, test on the
# deviations from the random control of the same size, on the space).
EXPECTED = (
    ("1", "no_queue", "topological", "below the control", lambda d: d < 0),
    ("1", "no_queue", "mfas", "below the control", lambda d: d < 0),
    ("2", "queue", "topological", "above the control", lambda d: d > 0),
    ("2", "queue", "mfas", "above the control", lambda d: d > 0),
    ("3", "no_queue", "mfas", f"|deviations| < {CORPUS_MFAS_NO_QUEUE}",
     lambda d: abs(d) < CORPUS_MFAS_NO_QUEUE),
)


# ---------------------------------------------------------------------------
# One compilation, two surfaces
# ---------------------------------------------------------------------------

def compile_orders(kept, rules, ids, born, engine) -> dict:
    """
    `edge_dropping.compile_subset`'s two orders, before they are scored.

    The same three steps in the same order: the edges fed through `try_edge`,
    the topological sort of what it accepted, and the minimum feedback arc set
    started from that sort. Unscored, so that each order is scored on both
    surfaces from a single compilation. Gate 1 is what says they are §14's and
    §16's orders.
    """
    dirs = [r["declared"] == "a_beats_b" for r in kept]
    edges = [(r["rule_a"], r["rule_b"]) if d else (r["rule_b"], r["rule_a"])
             for r, d in zip(kept, dirs)]
    topo = topological_order(ids, accepted_from(kept, dirs, rules, engine), born)
    mfas, _search = mfas_order(edges, ids, born, topo)
    return {"topological": topo, "mfas": mfas}


def scored(orders: dict, instances: dict) -> dict:
    """{surface: {compilation: score}}, each rounded as `compile_subset` rounds."""
    return {s: {c: round(floor(o, inst), 6) for c, o in orders.items()}
            for s, inst in instances.items()}


def control(rows, n, sampler, name, compile_both, draws=DRAWS) -> dict:
    """`filter_headroom.control`, the same draws, read on both surfaces."""
    vals = {s: {c: [] for c in COMPILATIONS} for s in SURFACES}
    for k in range(draws):
        sc = compile_both(sampler(rows, n, random.Random(f"{SEED}/{name}/{n}/{k}")))
        for s in SURFACES:
            for c in COMPILATIONS:
                vals[s][c].append(sc[s][c])
    return {s: {"n_kept": n, "draws": draws,
                **{c: {"mean": statistics.mean(v), "sd": statistics.pstdev(v)}
                   for c, v in vals[s].items()}}
            for s in SURFACES}


def against(value: dict, ctl: dict) -> dict:
    return {f"{c}_deviations": deviations(value[c], ctl[c]) for c in COMPILATIONS}


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def differences(mine, theirs, path="") -> list[str]:
    """The paths at which two records disagree, leaves and keys alike."""
    if isinstance(mine, dict) and isinstance(theirs, dict):
        out = [f"{path}/{k}: missing on one side"
               for k in sorted(set(mine) ^ set(theirs))]
        for k in sorted(set(mine) & set(theirs)):
            out += differences(mine[k], theirs[k], f"{path}/{k}")
        return out
    return [] if mine == theirs else [f"{path}: {mine!r} != {theirs!r}"]


def leaves(x) -> int:
    if isinstance(x, dict):
        return sum(leaves(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return sum(leaves(v) for v in x)
    return 1


def gate_headroom(corpus_side: dict, published: dict) -> dict:
    """Gate 1: every figure of §16's record, reproduced to the digit."""
    rows = {}
    for key in GATED:
        diff = differences(_rounded(corpus_side[key]), published[key], key)
        rows[key] = {"figures": leaves(published[key]), "passes": not diff,
                     "first_differences": diff[:10]}
    return {"what": "every figure of results3/filter_headroom.json, from the orders "
                    "this module compiled, scored on §16's own cell",
            "rows": rows, "passes": all(r["passes"] for r in rows.values())}


def published_space() -> dict:
    """The two published figures gate 2 reads, and the reference line beside
    them, each from the record that owns it."""
    hier = [r for r in json.loads(HIERARCHY.read_text())["rows"]
            if (r["pool"], r["surface"], r["tiebreak"]) == ("hibrido", "space", "born_at")]
    dec = [r for r in json.loads(DECLARED.read_text())["as_an_order"]
           if (r["pool"], r["surface"]) == ("hibrido", "space")]
    if len(hier) != 1 or len(dec) != 1:
        raise ValueError("the published space rows are not where gate 2 reads them")
    return {"born_at_floor": hier[0]["born_at_floor"],
            "keep_all_topological": dec[0]["declared"],
            "queue_ranking_stage_c": hier[0]["stage_c"]}


def gate_space(born_at_floor: float, keep_all_topological: float,
               published: dict) -> dict:
    """Gate 2: the space this module scores on is the one already published."""
    rows = {
        "born_at_floor": {"measured": round(born_at_floor, 6),
                          "published": published["born_at_floor"],
                          "owner": str(HIERARCHY)},
        "keep_all_topological": {"measured": round(keep_all_topological, 6),
                                 "published": published["keep_all_topological"],
                                 "owner": str(DECLARED)},
    }
    for r in rows.values():
        r["passes"] = r["measured"] == r["published"]
    return {"what": "born_at and keep_all, scored on hibrido over the space, "
                    "against the records that published them",
            "rows": rows, "passes": all(r["passes"] for r in rows.values())}


# ---------------------------------------------------------------------------
# The readings
# ---------------------------------------------------------------------------

def read_expectation(filters_space: dict) -> list[dict]:
    """The clauses of EXPECTATION, read off the space side and nothing else."""
    out = []
    for clause, name, comp, claim, test in EXPECTED:
        d = filters_space[name]["against_random_in_arrival_order"][f"{comp}_deviations"]
        out.append({"clause": clause, "filter": name, "compilation": comp,
                    "claim": claim, "deviations": d,
                    "holds": None if d is None else bool(test(d))})
    return out


def direction_by_cut(cuts: dict, truth: dict) -> dict:
    """How often each cut's edges point at the better rule, on each definition,
    by `edge_direction.agreement`'s convention."""
    out = {}
    for name, kept in cuts.items():
        rows = [dict(r, better_space=truth[r["index"]]["better_space"],
                     better_corpus=truth[r["index"]]["better_corpus"]) for r in kept]
        out[name] = {}
        for d in ("space", "corpus"):
            a = agreement(rows, f"better_{d}")
            out[name][d] = {k: a[k] for k in ("n", "rate", "standard_error",
                                              "outside_the_denominator")}
    return out


def queues_named(kept) -> dict:
    """Which queue the kept edges name as the winner, and how often."""
    return dict(Counter(r["action_a"] if r["declared"] == "a_beats_b"
                        else r["action_b"] for r in kept).most_common())


def decided_by_queue(order, instance, action) -> dict:
    """
    {queue: {"decided", "right"}} over an instance: the cases the rules of each
    queue decide under `order`, and how many of those they decide right.

    The same walk as `local_search.score_order`, kept apart by the deciding
    rule's queue, so the `right` column sums to the score times the size.
    Added after the first run; see the module's last section.
    """
    M, W, full, _n = instance
    remaining, out = full, {}
    for rid in order:
        fires = M[rid] & remaining
        if fires:
            q = out.setdefault(action[rid], {"decided": 0, "right": 0})
            q["decided"] += fires.bit_count()
            q["right"] += (W[rid] & fires).bit_count()
            remaining ^= fires
            if not remaining:
                break
    return dict(sorted(out.items()))


# ---------------------------------------------------------------------------

def instruments():
    """§16's instrument, and the same pool over the space."""
    corpus, rr, ec, conds = load()
    ids = [r["rule_id"] for r in rr]
    born = {r["rule_id"]: r["born_at"] for r in rr}
    act = {r["rule_id"]: r["action"] for r in rr}
    below = subsumption_below(rr, ec)
    _m, undef, truth = build_tables(corpus, rr, conds, below)
    te0 = split(corpus, truth, seed=SPLIT_SEED)[1]
    instances = {"corpus": (*build_masks(ids, undef, truth, act, te0), len(te0)),
                 "space": space_pools(ids, conds, act, below)["hibrido"]}
    rules = learned_rules()
    return rules, ids, born, instances, fresh_engine(rules)


def measure():
    """Everything but the printing and the file. Returns the payload and the
    gates, so that a refusal can say why."""
    t_start = time.time()
    rows = [r for r in json.loads(SOURCE.read_text())["answers"]
            if r["declared"] != "none"]
    truth = {o["index"]: o for o in json.loads(SAMPLE.read_text())["oracle"]}
    rules, ids, born, instances, engine = instruments()
    action = {rid: rules[rid].action for rid in ids}

    def compile_both(kept):
        return scored(compile_orders(kept, rules, ids, born, engine), instances)

    _order, rank, _c = revealed_ranking(rows)
    cuts = filters(rows, rank)
    orders = {name: compile_orders(kept, rules, ids, born, engine)
              for name, kept in cuts.items()}
    scores = {name: scored(o, instances) for name, o in orders.items()}
    sizes = sorted({len(k) for k in cuts.values()} - {len(rows)}, reverse=True)

    headroom = {s: {} for s in SURFACES}
    for n in sizes:
        ctl = control(rows, n, in_arrival_order, "arrival", compile_both)
        row = {s: {"random_in_arrival_order": ctl[s]} for s in SURFACES}
        for definition in ("corpus", "space"):
            for name, sign in (("oracle", 1), ("anti", -1)):
                kept = select(rows, n, lambda r, d=definition, g=sign:
                              g * oracle_rank(r, truth, d))
                sc = compile_both(kept)
                for s in SURFACES:
                    row[s][f"{name}_{definition}"] = {**sc[s],
                                                      **against(sc[s], ctl[s])}
        for s in SURFACES:
            headroom[s][str(n)] = row[s]

    shuffled_ctl = {name: control(rows, len(cuts[name]), shuffled, "shuffled",
                                  compile_both)
                    for name in SHUFFLED_FILTERS}

    read = {s: {} for s in SURFACES}
    for name, kept in cuts.items():
        for s in SURFACES:
            v = scores[name][s]
            entry = {"n_kept": len(kept), **v}
            if str(len(kept)) in headroom[s]:
                entry["against_random_in_arrival_order"] = against(
                    v, headroom[s][str(len(kept))]["random_in_arrival_order"])
            if name in shuffled_ctl:
                entry["against_shuffled_control_as_in_14"] = against(
                    v, shuffled_ctl[name][s])
            read[s][name] = entry

    born_order = sorted(ids, key=lambda r: born[r])
    side = {s: {"born_at_floor": floor(born_order, instances[s]),
                "headroom_by_size": headroom[s],
                "shuffled_controls_at_14s_sizes": {name: shuffled_ctl[name][s]
                                                   for name in SHUFFLED_FILTERS},
                "filters": read[s]}
            for s in SURFACES}

    published = published_space()
    g1 = gate_headroom(side["corpus"], json.loads(HEADROOM.read_text()))
    g2 = gate_space(side["space"]["born_at_floor"],
                    side["space"]["filters"]["keep_all"]["topological"], published)
    space = side["space"]

    payload = {
        "_env": environment(draws=DRAWS, seed=SEED),
        "what": "§16's selections of the 1,600 run's declared edges, compiled as §16 "
                "compiled them and scored on the hibrido pool over the exhaustive "
                "space: the headroom of any selection there, and the eight filters "
                "inside it. Zero API calls.",
        "provenance": PROVENANCE,
        "expectation_written_before_the_run": EXPECTATION,
        "what_the_drafter_had_seen": SEEN,
        "adjudicates_nothing": "no row of any plan is read here and none moves.",
        "surface": "hibrido pool, exhaustive space, 134,400 points",
        "the_corpus_side_is_not_written_again":
            "every corpus figure of the same orders is results3/filter_headroom.json's, "
            "which owns it. Gate 1 says each one reproduced; none is copied here.",
        "gates": {"filter_headroom_reproduces": g1,
                  "the_space_is_the_published_one": g2,
                  "passes": g1["passes"] and g2["passes"]},
        "references": {
            "queue_ranking_stage_c": published["queue_ranking_stage_c"],
            "queue_ranking_owner": str(HIERARCHY),
            "keep_all_topological_owner": str(DECLARED),
            "born_at_floor_owner": str(HIERARCHY)},
        "born_at_floor": space["born_at_floor"],
        "headroom_by_size": space["headroom_by_size"],
        "shuffled_controls_at_14s_sizes": space["shuffled_controls_at_14s_sizes"],
        "filters": space["filters"],
        "expectation_read": read_expectation(space["filters"]),
        "diagnostics": {
            "what": "read beside the scores, not against anything: how often each "
                    "cut's edges point at the better rule under each definition, by "
                    "rung3/edge_direction.py's convention, and which queue each "
                    "cut's edges name as the winner",
            "direction_by_cut": direction_by_cut(cuts, truth),
            "queues_named": {name: queues_named(kept) for name, kept in cuts.items()}},
        "post_run": {
            "what": "where each filter's two orders decide on the space, and decide "
                    "right, by the queue of the deciding rule, beside the cases of the "
                    "space each queue is the truth for",
            "provenance": "ADDED AFTER THE FIRST RUN, which put no_queue in MFAS "
                          "eleven deviations below its control, to say where that loss "
                          "sits. It reads nothing new and moves no reading above.",
            "truth_by_queue": {q: m.bit_count() for q, m in
                               sorted(space_truth_masks(Space()).items())},
            "by_filter": {name: {c: decided_by_queue(o, instances["space"], action)
                                 for c, o in orders[name].items()}
                          for name in cuts}},
        "seconds": round(time.time() - t_start, 1),
    }
    return _rounded(payload), g1, g2


def main(argv=None) -> int:
    payload, g1, g2 = measure()
    print("=" * 78)
    print("§16'S CUTS OVER THE FUNCTION")
    print("=" * 78)
    print(f"  hibrido, exhaustive space · {DRAWS} draws per control · zero API calls"
          f" · POST-RUN, expectation written before the run")
    print(f"  {describe()}")
    print(f"  gate 1, §16 reproduces on its own cell: "
          f"{'PASS' if g1['passes'] else 'FAIL'}")
    for key, r in g1["rows"].items():
        print(f"    {key:<32} {r['figures']:>4} figures  "
              f"{'ok' if r['passes'] else r['first_differences']}")
    print(f"  gate 2, the space is the published one: "
          f"{'PASS' if g2['passes'] else 'FAIL'}")
    for key, r in g2["rows"].items():
        print(f"    {key:<32} measured {r['measured']}  published {r['published']}")
    if not (g1["passes"] and g2["passes"]):
        print("\nREFUSED: nothing was written.")
        return 1

    print(f"\n  {'n':>5}  {'random topo':>16}  {'random mfas':>16}  "
          f"{'oracle cor':>11}  {'oracle spa':>11}  {'anti cor':>11}  {'anti spa':>11}")
    for n, row in payload["headroom_by_size"].items():
        ctl = row["random_in_arrival_order"]

        def d(key):
            r = row[key]
            return f"{r['topological_deviations']:+.1f}/{r['mfas_deviations']:+.1f}"
        print(f"  {n:>5}  {ctl['topological']['mean']:.4f} sd {ctl['topological']['sd']:.4f}"
              f"  {ctl['mfas']['mean']:.4f} sd {ctl['mfas']['sd']:.4f}  "
              f"{d('oracle_corpus'):>11}  {d('oracle_space'):>11}  "
              f"{d('anti_corpus'):>11}  {d('anti_space'):>11}")

    print(f"\n  {'filter':<13}{'kept':>6}{'topo':>9}{'mfas':>9}"
          f"{'devs topo':>11}{'devs mfas':>11}   (against the random control in "
          f"arrival order; §14's own beside)")
    for name, e in payload["filters"].items():
        a = e.get("against_random_in_arrival_order")
        sh = e.get("against_shuffled_control_as_in_14")
        print(f"  {name:<13}{e['n_kept']:>6}{e['topological']:>9.4f}{e['mfas']:>9.4f}"
              + (f"{a['topological_deviations']:>+11.2f}{a['mfas_deviations']:>+11.2f}"
                 if a else f"{'—':>11}{'—':>11}")
              + (f"   §14: {sh['topological_deviations']:+.2f}/"
                 f"{sh['mfas_deviations']:+.2f}" if sh else ""))
    ref = payload["references"]
    print(f"\n  reference lines on the space: born_at floor "
          f"{payload['born_at_floor']:.4f}, a free queue ranking "
          f"{ref['queue_ranking_stage_c']:.4f}")

    print("\n  the expectation, written before the run:")
    for e in payload["expectation_read"]:
        d = "—" if e["deviations"] is None else f"{e['deviations']:+.2f}"
        verdict = {True: "holds", False: "does not hold", None: "unreadable"}
        print(f"    ({e['clause']}) {e['filter']:<9} {e['compilation']:<12}"
              f"{e['claim']:<22} {d:>6}  {verdict[e['holds']]}")

    print("\n  diagnostics, direction rate by cut (space / corpus definition):")
    for name, by in payload["diagnostics"]["direction_by_cut"].items():
        print(f"    {name:<13} {by['space']['rate']:.4f} (n {by['space']['n']})"
              f"   {by['corpus']['rate']:.4f} (n {by['corpus']['n']})")
    for name, q in payload["diagnostics"]["queues_named"].items():
        print(f"    queues named by `{name}`: {q}")

    post = payload["post_run"]
    truth_si = post["truth_by_queue"]["SECURITY_INCIDENT"]
    print(f"\n  post-run: SECURITY_INCIDENT decided right on the space, of {truth_si}"
          f" points whose truth it is (topological / mfas):")
    for name, by in post["by_filter"].items():
        got = [by[c].get("SECURITY_INCIDENT", {"right": 0})["right"] for c in COMPILATIONS]
        print(f"    {name:<13} {got[0]:>6} / {got[1]:>6}")

    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


def _rounded(x, places: int = 6):
    if isinstance(x, float):
        return round(x, places)
    if isinstance(x, dict):
        return {k: _rounded(v, places) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_rounded(v, places) for v in x]
    return x


if __name__ == "__main__":
    sys.exit(main())
