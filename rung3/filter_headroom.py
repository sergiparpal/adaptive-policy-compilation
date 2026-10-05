"""
HOW MUCH COULD ANY SELECTION OF THE DECLARED EDGES HAVE SHOWN? The resolution
of §14's instrument.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
§14 found that no truth-free rule for keeping the 1,600 run's declared edges
beats keeping the same number at random. `PLAN_WHY.md` §10.5 then asked the same
of the proposer's stated reasons. Before any filter is read against chance, this
module asks what the instrument could show at all.

**An ORACLE selector is the best a selection of a given size can do**: it keeps
first the edges whose declared winner is the better rule over the shared
region, then the edges with no strictly better rule, and the wrong ones last. Its
distance from a same-size random choice is therefore the ceiling of every
truth-free filter of that size. If the ceiling is low, a filter that lands near
chance has been tested by nothing. The ANTI selector, the same order reversed,
is the floor.

--------------------------------------------------------------------------
WHAT IT MEASURES
--------------------------------------------------------------------------
On §14's cell, the `hibrido` pool and corpus test split 0, in both of §14's
compilations, at every size a filter below cuts:

  random      the same number of edges chosen at random, KEPT IN THE ORDER THEY
              ARRIVED; `DRAWS` draws. The topological compilation refuses
              cycles first-come-first-served, so arrival order is part of what a
              control must hold fixed when it measures selection alone.
  shuffled    §14's own control, at §14's sizes: the same number at random in a
              RANDOM arrival order. §14 measured the arrival accident at +1.24
              deviations, so the two controls need not agree.
  oracle      as above, under each definition of the better rule, space and
              corpus, read from `results2/pair_sample_1600.json`.
  anti        the oracle's order reversed.
  filters     §14's two, `consistent` and `inconsistent`, and the five cuts
              `PLAN_WHY.md`'s frozen codebook makes: `spec`, `no_spec`,
              `queue`, `no_queue`, `no_count`. Each is read against the random
              control of its own size. **They adjudicate nothing.**

--------------------------------------------------------------------------
THE GATE
--------------------------------------------------------------------------
§14's three published scores reproduce exactly, `keep_all`, `consistent` and
`inconsistent` in both compilations, from `results3/edge_dropping.json`. So the
instrument is §14's, and a difference between the two records is a difference
of controls and not of machinery. The module refuses to write otherwise.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** The headroom was first measured on 2026-10-05 with a scratch probe
of 60 draws, at the sizes of `PLAN_WHY.md`'s codes and of §14's filters, while
deciding whether that plan's §10.5 could be pre-registered. It could not: even
the oracle sat only about one or two deviations above chance. This module was
written after seeing that, so nothing in it is a bet. It is not a signed row, not
on `STATUS.md`'s scoreboard, and not a calibration event. Zero API calls.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.filter_headroom
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
from rung3.declared_order import fresh_engine
from rung3.edge_dropping import agrees, compile_subset, revealed_ranking
from rung3.floor_by_pool import floor
from rung3.local_search import build_masks
from rung3.order_search import build_tables, load, split, subsumption_below
from why import codebook

OUT = Path("results3")
RECORD = "filter_headroom.json"
SOURCE = Path("results2/pair_judgement_1600.json")
SAMPLE = Path("results2/pair_sample_1600.json")
PUBLISHED = Path("results3/edge_dropping.json")

DRAWS = 200
SEED = "filter_headroom"           # string seeds: no draw depends on PYTHONHASHSEED
SPLIT_SEED = 17
SHUFFLED_FILTERS = ("keep_all", "consistent", "inconsistent")   # §14's own

PROVENANCE = (
    "POST-RUN. The headroom was first measured on 2026-10-05 by a scratch probe "
    "of 60 draws, while deciding whether PLAN_WHY.md's §10.5 could be "
    "pre-registered, and this module was written after seeing it. Not a signed "
    "row, not on STATUS.md's scoreboard, not a calibration event. The filters "
    "are read against the headroom and adjudicate nothing. Zero API calls.")


# ---------------------------------------------------------------------------
# The selectors and the samplers, pure
# ---------------------------------------------------------------------------

def winner(row: dict) -> str:
    return row["rule_a"] if row["declared"] == "a_beats_b" else row["rule_b"]


def oracle_rank(row: dict, truth: dict[int, dict], surface: str) -> int:
    """0 when the declared winner is the better rule, 1 when neither rule is
    strictly better, 2 when the declared winner is the worse one."""
    b = truth[row["index"]][f"better_{surface}"]
    best = row["rule_a"] if b == "a" else row["rule_b"] if b == "b" else None
    if best is None:
        return 1
    return 0 if best == winner(row) else 2


def select(rows: list[dict], n: int, key) -> list[dict]:
    """The `n` rows a selector ranks first, ties broken by arrival, returned in
    the order they arrived."""
    chosen = sorted(range(len(rows)), key=lambda i: (key(rows[i]), i))[:n]
    return [rows[i] for i in sorted(chosen)]


def in_arrival_order(rows: list[dict], n: int, rng: random.Random) -> list[dict]:
    """`n` rows at random, kept in the order they arrived."""
    return [rows[i] for i in sorted(rng.sample(range(len(rows)), n))]


def shuffled(rows: list[dict], n: int, rng: random.Random) -> list[dict]:
    """`n` rows at random in a random order: §14's own control."""
    return rng.sample(rows, n)


def filters(rows: list[dict], rank: dict) -> dict[str, list[dict]]:
    """§14's two filters and the five cuts of `PLAN_WHY.md`'s codebook, each in
    arrival order."""
    codes = [codebook.code(r.get("why", "")) for r in rows]
    return {
        "keep_all": list(rows),
        "consistent": [r for r in rows if agrees(r, rank)],
        "inconsistent": [r for r in rows if not agrees(r, rank)],
        "spec": [r for r, c in zip(rows, codes) if "spec" in c],
        "no_spec": [r for r, c in zip(rows, codes) if "spec" not in c],
        "queue": [r for r, c in zip(rows, codes) if "queue" in c],
        "no_queue": [r for r, c in zip(rows, codes) if "queue" not in c],
        "no_count": [r for r, c in zip(rows, codes) if "count" not in c],
    }


def deviations(value: float, control: dict) -> float | None:
    sd = control["sd"]
    return round((value - control["mean"]) / sd, 2) if sd else None


# ---------------------------------------------------------------------------
# The instrument, §14's
# ---------------------------------------------------------------------------

def instrument():
    corpus, rr, ec, conds = load()
    ids = [r["rule_id"] for r in rr]
    born = {r["rule_id"]: r["born_at"] for r in rr}
    act = {r["rule_id"]: r["action"] for r in rr}
    below = subsumption_below(rr, ec)
    _m, undef, truth = build_tables(corpus, rr, conds, below)
    te0 = split(corpus, truth, seed=SPLIT_SEED)[1]
    inst = (*build_masks(ids, undef, truth, act, te0), len(te0))
    rules = learned_rules()
    floor_born = floor(sorted(ids, key=lambda r: born[r]), inst)
    return rules, ids, born, inst, fresh_engine(rules), floor_born


def control(rows, n, sampler, name, compile_one, draws=DRAWS) -> dict:
    t, m = [], []
    for k in range(draws):
        c = compile_one(sampler(rows, n, random.Random(f"{SEED}/{name}/{n}/{k}")))
        t.append(c["topological"])
        m.append(c["mfas"])
    return {"n_kept": n, "draws": draws,
            "topological": {"mean": statistics.mean(t), "sd": statistics.pstdev(t)},
            "mfas": {"mean": statistics.mean(m), "sd": statistics.pstdev(m)}}


def gate_published(scores: dict, published: dict) -> dict:
    """§14's three published scores, reproduced to the digit."""
    rows = {}
    for name in SHUFFLED_FILTERS:
        got = (round(scores[name]["topological"], 6), round(scores[name]["mfas"], 6))
        want = (published["filters"][name]["topological"],
                published["filters"][name]["mfas"])
        rows[name] = {"measured": got, "published": want, "passes": got == want}
    return {"what": "§14's keep_all, consistent and inconsistent, both compilations, "
                    "from results3/edge_dropping.json",
            "rows": rows, "passes": all(r["passes"] for r in rows.values())}


def main(argv=None) -> int:
    t_start = time.time()
    rows = [r for r in json.loads(SOURCE.read_text())["answers"]
            if r["declared"] != "none"]
    truth = {o["index"]: o for o in json.loads(SAMPLE.read_text())["oracle"]}
    published = json.loads(PUBLISHED.read_text())
    rules, ids, born, inst, engine, floor_born = instrument()

    def compile_one(kept):
        return compile_subset(kept, rules, ids, born, inst, engine)

    _order, rank, _c = revealed_ranking(rows)
    cuts = filters(rows, rank)
    scores = {name: compile_one(kept) for name, kept in cuts.items()}
    gate = gate_published(scores, published)

    print("=" * 78)
    print("HOW MUCH COULD ANY SELECTION OF THE DECLARED EDGES HAVE SHOWN?")
    print("=" * 78)
    print(f"  {len(rows)} declared edges · hibrido, corpus test split 0 · "
          f"{DRAWS} draws per control · zero API calls · POST-RUN")
    print(f"  {describe()}")
    print(f"  gate, §14's scores reproduce: {'PASS' if gate['passes'] else 'FAIL'}")
    for name, g in gate["rows"].items():
        print(f"    {name:<13} measured {g['measured']}  published {g['published']}")
    if not gate["passes"]:
        print("\nREFUSED: the instrument is not §14's; nothing was written.")
        return 1

    sizes = sorted({len(k) for k in cuts.values()} - {len(rows)}, reverse=True)
    headroom = {}
    print(f"\n  {'n':>5}  {'random topo':>16}  {'random mfas':>16}  "
          f"{'oracle cor':>11}  {'oracle spa':>11}  {'anti cor':>11}  {'anti spa':>11}")
    for n in sizes:
        ctl = control(rows, n, in_arrival_order, "arrival", compile_one)
        row = {"random_in_arrival_order": ctl}
        for surface in ("corpus", "space"):
            for name, sign in (("oracle", 1), ("anti", -1)):
                kept = select(rows, n, lambda r, s=surface, g=sign:
                              g * oracle_rank(r, truth, s))
                c = compile_one(kept)
                row[f"{name}_{surface}"] = {
                    "topological": c["topological"], "mfas": c["mfas"],
                    "topological_deviations": deviations(c["topological"],
                                                         ctl["topological"]),
                    "mfas_deviations": deviations(c["mfas"], ctl["mfas"])}
        headroom[n] = row

        def d(key):
            r = row[key]
            return f"{r['topological_deviations']:+.1f}/{r['mfas_deviations']:+.1f}"
        print(f"  {n:>5}  {ctl['topological']['mean']:.4f} sd {ctl['topological']['sd']:.4f}"
              f"  {ctl['mfas']['mean']:.4f} sd {ctl['mfas']['sd']:.4f}  {d('oracle_corpus'):>11}"
              f"  {d('oracle_space'):>11}  {d('anti_corpus'):>11}  {d('anti_space'):>11}")

    shuffled_controls = {name: control(rows, len(cuts[name]), shuffled, "shuffled",
                                       compile_one)
                         for name in SHUFFLED_FILTERS}

    read = {}
    print(f"\n  {'filter':<13}{'kept':>6}{'topo':>9}{'mfas':>9}"
          f"{'devs topo':>11}{'devs mfas':>11}   (against the random control in "
          f"arrival order; §14's own beside)")
    for name, kept in cuts.items():
        s = scores[name]
        entry = {"n_kept": len(kept), "topological": s["topological"], "mfas": s["mfas"]}
        if len(kept) in headroom:
            ctl = headroom[len(kept)]["random_in_arrival_order"]
            entry["against_random_in_arrival_order"] = {
                "topological_deviations": deviations(s["topological"], ctl["topological"]),
                "mfas_deviations": deviations(s["mfas"], ctl["mfas"])}
        if name in shuffled_controls:
            ctl = shuffled_controls[name]
            entry["against_shuffled_control_as_in_14"] = {
                "topological_deviations": deviations(s["topological"], ctl["topological"]),
                "mfas_deviations": deviations(s["mfas"], ctl["mfas"])}
        read[name] = entry
        a = entry.get("against_random_in_arrival_order")
        sh = entry.get("against_shuffled_control_as_in_14")
        print(f"  {name:<13}{len(kept):>6}{s['topological']:>9.4f}{s['mfas']:>9.4f}"
              + (f"{a['topological_deviations']:>+11.2f}{a['mfas_deviations']:>+11.2f}"
                 if a else f"{'—':>11}{'—':>11}")
              + (f"   §14: {sh['topological_deviations']:+.2f}/{sh['mfas_deviations']:+.2f}"
                 if sh else ""))

    payload = {
        "_env": environment(draws=DRAWS, seed=SEED),
        "what": "the ceiling and floor of any selection of the 1,600 run's declared "
                "edges against a same-size random choice, on §14's cell, and §14's "
                "and PLAN_WHY.md's filters read inside them. Zero API calls.",
        "provenance": PROVENANCE,
        "adjudicates_nothing": "no row of any plan is read here and none moves.",
        "surface": "hibrido pool, corpus test split 0",
        "selectors": {
            "oracle": "the edges whose declared winner is the better rule over the "
                      "shared region first, then those with no strictly better rule, "
                      "then the wrong ones, ties by arrival, kept in arrival order",
            "anti": "the oracle's order reversed",
            "definitions": "rung3/edge_direction.py's space and corpus, read from "
                           "results2/pair_sample_1600.json"},
        "controls": {
            "random_in_arrival_order": "the same number at random, kept in the order "
                                       "they arrived; the control for selection alone",
            "shuffled_as_in_14": "the same number at random in a random arrival "
                                 "order, §14's own; only at §14's sizes"},
        "gate_14_reproduces": gate,
        "born_at_floor": floor_born,
        "headroom_by_size": {str(n): v for n, v in headroom.items()},
        "shuffled_controls_at_14s_sizes": shuffled_controls,
        "filters": read,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(_rounded(payload), indent=2) + "\n")
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
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
