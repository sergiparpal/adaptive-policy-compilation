"""
`M-g1` to `M-g4` of `PLAN_RANKING.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  M-g1  The scorer reproduces the record. The suite is green. Over rung 1's 577
        rules, rung 3's own `enumerate_hierarchies`, `hierarchy_order` and
        `floor` give back `results3/queue_hierarchy_floor.json` on every cell
        and under both tie-breaks: `best`, `mean`, `median`, `sd`, `worst`,
        `stage_c` and the best hierarchy itself, and the five-split means. The
        `born_at` order gives back `results3/floor_by_pool.json`'s floors. Both
        tie-breaks agree on every cell (rung 3's own gate, called). Blocking in
        the sense of `harness.ceiling_check`: if the scorer does not reproduce,
        no score of a stated ranking means anything.
  M-g2  The question reads nothing but the eight names (`ranking/question.py`).
  M-g3  The prediction and substitution paths reproduce.
          * The learned base's declared answers are 1,479, which is the
            record's own `declared` count, and the hidden policy's two-way
            answers are 166, the record's 170 less its 4 parse failures.
          * `rung2/pair_judgement.py`'s `revealed_hierarchy` over those rows is
            the block the record stores, and `rung3/edge_dropping.py`'s
            revealed ranking over them is the one `edge_dropping.json` stores.
          * `predicts`, applied to that revealed ranking, gives back the 1,194
            answers of 1,479 that `edge_dropping.json` keeps as `consistent`.
            It is the only rate of a ranking over these answers that any record
            publishes, and the only one the dry run computes.
          * Over the edge rows `results_blind/score.json` stores, `blind.rows`
            gives back that record's `directions` on both keys, for the
            declarations, for Stage C's ranking and for the newborn rule; the
            declarations' readings are `K-b`'s and `K-e`'s verdicts; and the
            `predict` this plan builds from a ranking names the rule
            `blind.rows.stage_c_names` names on every row, when the ranking is
            Stage C's.
  M-g4  The signature (`ranking/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures that are already
published.** No ranking but Stage C's and the revealed one is scored, no rate
of Stage C's ranking over the model's answers is computed, and no presentation
is asked anything.
"""

from __future__ import annotations

import json
import statistics
import time
from dataclasses import dataclass, field
from typing import Any

from reuse.gates import run_suite
from rung2.pair_judgement import revealed_hierarchy
from rung3.floor_by_pool import POOLS, SPACE
from rung3.queue_hierarchy_floor import (STAGE_C_HIERARCHY, TIEBREAKS,
                                         enumerate_hierarchies,
                                         gate_tiebreak_irrelevant, read_floor)

from . import instrument as I
from . import plan, question

TOLERANCE = 2e-6     # the records publish six places; 3.10 and 3.12 may differ by one
FLOAT_FIELDS = ("best", "mean", "median", "sd", "worst", "stage_c")
EXACT_FIELDS = ("n_orders", "best_hierarchy")


@dataclass
class Checks:
    mg1: dict
    mg2: dict
    mg3: dict
    mg4: dict
    instrument: I.Instrument | None = field(default=None, repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.mg1["passes"] and self.mg2["passes"] and self.mg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"M-g1": {k: v for k, v in self.mg1.items() if k != "rows"},
                "M-g2": {k: v for k, v in self.mg2.items() if k != "digests"},
                "M-g3": self.mg3, "M-g4": self.mg4}


def close(a: Any, b: Any) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= TOLERANCE
    return a == b


# ---------------------------------------------------------------------------
# M-g1
# ---------------------------------------------------------------------------

def measured_rows(inst: I.Instrument, progress: bool = False,
                  cells: tuple[tuple[str, str], ...] = I.CELLS) -> list[dict]:
    """Every (tie-break, pool, surface) row of the record, measured again with
    rung 3's own functions. `cells` narrows it, for a test."""
    rows = []
    stage_c = I.rank_of(STAGE_C_HIERARCHY)
    for tb in TIEBREAKS:
        for pool, surface in cells:
            t0 = time.time()
            inst_ = inst.instance(pool, surface)
            e = enumerate_hierarchies(inst.ids, inst.action, inst.born, inst_,
                                      inst.actions, tb)
            e.update({"tiebreak": tb, "pool": pool, "surface": surface,
                      "stage_c": round(I.floor(I.hierarchy_order(
                          inst.ids, inst.action, inst.born, stage_c, tb), inst_), 6),
                      "born_at": round(I.born_at_score(inst, pool, surface), 6)})
            rows.append(e)
            if progress:
                print(f"    M-g1  {tb:<17}{pool:<8}{surface:<20}"
                      f"{time.time() - t0:5.1f}s", end="\r", flush=True)
    if progress:
        print(" " * 70, end="\r")
    return rows


def compare_with_record(rows: list[dict], published: list[dict],
                        floors: dict[tuple[str, str], float]) -> list[str]:
    """Every field of every measured row against the record, and every
    five-split mean against its aggregate row. The comparison is the gate; the
    measuring is `measured_rows`."""
    problems = []
    pub = {(r["tiebreak"], r["pool"], r["surface"]): r for r in published}
    for r in rows:
        key = (r["tiebreak"], r["pool"], r["surface"])
        p = pub.get(key)
        if p is None:
            problems.append(f"{key}: no such row in the record")
            continue
        for f in FLOAT_FIELDS + EXACT_FIELDS:
            if not close(r[f], p[f]):
                problems.append(f"{key}.{f}: measured {r[f]}, published {p[f]}")
        fl = floors.get((r["pool"], r["surface"]))
        if fl is not None and not close(r["born_at"], fl):
            problems.append(f"{key}.born_at: measured {r['born_at']}, "
                            f"floor_by_pool publishes {fl}")
        if p.get("born_at_floor") is not None and not close(r["born_at"],
                                                            p["born_at_floor"]):
            problems.append(f"{key}.born_at_floor: measured {r['born_at']}, "
                            f"published {p['born_at_floor']}")
    for tb in TIEBREAKS:
        for pool in POOLS:
            per = [r for r in rows if r["tiebreak"] == tb and r["pool"] == pool
                   and r["surface"] in I.SPLITS]
            p = pub.get((tb, pool, I.FIVE_SPLITS))
            if p is None or len(per) != len(I.SPLITS):
                problems.append(f"{(tb, pool, I.FIVE_SPLITS)}: not comparable")
                continue
            for f in ("best", "mean", "stage_c"):
                m = statistics.mean(r[f] for r in per)
                if not close(round(m, 6), p[f]):
                    problems.append(f"{(tb, pool, I.FIVE_SPLITS)}.{f}: "
                                    f"measured {m}, published {p[f]}")
    missing = set(pub) - {(r["tiebreak"], r["pool"], r["surface"]) for r in rows} \
        - {(tb, pool, I.FIVE_SPLITS) for tb in TIEBREAKS for pool in POOLS}
    if missing:
        problems.append(f"rows of the record not measured: {sorted(missing)}")
    return problems


def gate_mg1(inst: I.Instrument, suite: bool = True, progress: bool = False,
             rows: list[dict] | None = None) -> dict[str, Any]:
    t0 = time.time()
    rec = json.loads(plan.HIERARCHY_RECORD.read_text())
    floors, g_floor = read_floor(plan.FLOOR_RECORD)
    rows = measured_rows(inst, progress) if rows is None else rows
    problems = compare_with_record(rows, rec["rows"], floors)
    if not g_floor["passes"]:
        problems.append(f"floor_by_pool lacks cells: {g_floor['missing']}")
    if inst.actions != sorted(plan.QUEUES):
        problems.append("the base's actions are not the eight queues")
    if rec["stage_c_hierarchy"] != list(STAGE_C_HIERARCHY):
        problems.append("the record's Stage C hierarchy is not rung 3's constant")
    g_tb = gate_tiebreak_irrelevant(rows)
    if not g_tb["passes"]:
        problems.append(f"the tie-breaks disagree on {g_tb['cells_that_differ']}")
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {
        "what": "rung 3's enumeration, hierarchy order and floor give back "
                f"{plan.HIERARCHY_RECORD} on every cell under both tie-breaks, and "
                f"{plan.FLOOR_RECORD}'s born_at floors; the tie-breaks agree; the "
                "suite is green",
        "cells": len(I.CELLS), "rows_compared": len(rows),
        "n_rules": len(inst.ids), "n_cases": inst.n_cases, "n_space": inst.n_space,
        "tolerance": TOLERANCE,
        "tiebreak_gate": {k: v for k, v in g_tb.items() if k != "what"},
        "suite": tests,
        "problems": problems,
        "seconds": round(time.time() - t0, 1),
        "rows": rows,
        "passes": not problems and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# M-g3
# ---------------------------------------------------------------------------

def gate_mg3() -> dict[str, Any]:
    problems = []
    learned = json.loads(plan.PAIRWISE_LEARNED.read_text())
    hidden = json.loads(plan.PAIRWISE_HIDDEN.read_text())
    try:
        rows = I.learned_rows()
    except ValueError as exc:
        rows = []
        problems.append(str(exc))
    la, ha = I.learned_answers(), I.hidden_answers()
    published_declared = learned["declared"]["a_beats_b"] + learned["declared"]["b_beats_a"]
    if len(la) != published_declared:
        problems.append(f"{len(la)} declared answers, the record says {published_declared}")
    if len(la) + learned["declared"]["none"] != learned["n_sampled"]:
        problems.append("declared and undeclared answers do not make the sample")
    two_way = len(hidden["answers"]) - hidden["parse_failures"] - hidden["off_menu_answers"]
    if len(ha) != two_way:
        problems.append(f"{len(ha)} two-way answers, the record implies {two_way}")
    if any(a.queues[0] == a.queues[1] for a in la + ha):
        problems.append("a pair offers one queue twice")
    if any(a.named not in a.queues for a in la + ha):
        problems.append("an answer names a queue not on offer")

    if revealed_hierarchy(learned["answers"]) != learned["revealed_hierarchy"]:
        problems.append("revealed_hierarchy does not give back the stored block")
    dropping = json.loads(plan.EDGE_DROPPING.read_text())
    order, copeland = I.revealed_learned()
    if order != dropping["revealed_ranking"]["order"] or \
            copeland != dropping["revealed_ranking"]["copeland"]:
        problems.append("the revealed ranking is not edge_dropping.json's")
    hits, n = I.predicts(order, la)
    kept = dropping["filters"]["consistent"]["n_kept"]
    if (hits, n) != (kept, dropping["filters"]["keep_all"]["n_kept"]):
        problems.append(f"the revealed ranking predicts {hits} of {n}, "
                        f"edge_dropping.json keeps {kept} as consistent")

    blind = json.loads(plan.BLIND_SCORE.read_text())
    er = I.blind_edge_rows()
    for surface, key in (("space", "space_out"), ("corpus", "corpus_out")):
        mine = I.blind_rows.comparators(er, key)
        for arm, block in mine.items():
            pub = blind["directions"][surface][arm]
            for f, v in block.items():
                if not close(round(v, 6) if isinstance(v, float) else v, pub[f]):
                    problems.append(f"directions.{surface}.{arm}.{f}: {v} vs {pub[f]}")
        ours = I.blind_reading(STAGE_C_HIERARCHY, er, key)
        if any(not close(ours[f], mine["stage_c_ranking"][f]) for f in ours):
            problems.append(f"{key}: this plan's predict is not stage_c_names")
    name = I.names_for(STAGE_C_HIERARCHY)
    differ = sum(1 for run in er for row in run
                 if name(row) != I.blind_rows.stage_c_names(row))
    if differ:
        problems.append(f"this plan's predict names another rule on {differ} rows")
    for row_id, key in (("K-b", "space_out"), ("K-e", "corpus_out")):
        d = I.blind_reading(None, er, key)
        v = blind["verdicts"][row_id]
        if not (close(round(d["reading"], 6), v["reading"]) and d["units"] == v["units"]):
            problems.append(f"{row_id}: {d['reading']} on {d['units']} units, the record "
                            f"says {v['reading']} on {v['units']}")
    return {
        "what": "the populations the rows read are the records' own, the revealed "
                "ranking and its 1,194 of 1,479 come back, and blind.rows gives back "
                "K-b's, K-e's and the ranking's readings with this plan's predict",
        "learned_declared_answers": len(la),
        "hidden_two_way_answers": len(ha),
        "revealed_ranking": order,
        "revealed_predicts_its_own_answers": [hits, n],
        "k_b_units": blind["verdicts"]["K-b"]["units"],
        "rows_where_the_predicts_differ": differ,
        "problems": problems,
        "passes": not problems,
    }


# ---------------------------------------------------------------------------

def run_checks(suite: bool = True, progress: bool = False,
               inst: I.Instrument | None = None) -> Checks:
    inst = I.build() if inst is None else inst
    return Checks(mg1=gate_mg1(inst, suite=suite, progress=progress),
                  mg2=question.gate_mg2(),
                  mg3=gate_mg3(),
                  mg4=plan.gate_signature(),
                  instrument=inst)


def report(checks: Checks) -> None:
    def mark(g):
        return "PASS" if g["passes"] else "FAIL"
    g1, g2, g3, g4 = checks.mg1, checks.mg2, checks.mg3, checks.mg4
    print(f"  M-g1 {mark(g1)}  {g1['rows_compared']} rows of "
          f"{plan.HIERARCHY_RECORD} measured again in {g1['seconds']}s: "
          f"{len(g1['problems'])} differ; both tie-breaks agree on "
          f"{g1['tiebreak_gate']['n_cells']} cells")
    s = g1["suite"]
    print(f"           suite: " + (f"{s['tests']} tests, {s['result']} ({s['seconds']}s)"
                                    if s.get("ran") else "not run"))
    for p in g1["problems"][:10]:
        print(f"           {p}")
    print(f"  M-g2 {mark(g2)}  {g2['presentations']} presentations, each request "
          f"the eight names once and nothing else; teeth {g2['teeth']}")
    for p in g2["problems"][:10]:
        print(f"           {p}")
    print(f"  M-g3 {mark(g3)}  {g3['learned_declared_answers']} declared answers, "
          f"{g3['hidden_two_way_answers']} two-way; the revealed ranking predicts "
          f"{g3['revealed_predicts_its_own_answers'][0]} of "
          f"{g3['revealed_predicts_its_own_answers'][1]}, as published; K-b on "
          f"{g3['k_b_units']} units")
    for p in g3["problems"][:10]:
        print(f"           {p}")
    print(f"  M-g4 {'PASS' if g4['passes'] else 'NOT SIGNED'}  {g4['found']} "
          f"signature line(s), {g4['unsigned']} blank — it blocks every write, "
          "not a dry run")
