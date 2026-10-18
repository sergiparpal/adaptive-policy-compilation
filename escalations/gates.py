"""
`J-g1` to `J-g4` of `PLAN_ESCALATIONS.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  J-g1  The material and the instrument are the records'. The suite is green.
        The material of §1 recomputes. Arrival order gives 519 and 42,310. The
        instrument reproduces the audit record's split-0 rows: with all 1,005
        train cases, and with each of its five draws at 10 labels and at 50.
        On the 286 named escalations it reproduces `PLAN_STUDENTS.md`'s 814
        and 73,420.
  J-g2  The selections read no truth. Built twice they are equal, every set has
        its size and lies inside the 316, and `selections.py` never names the
        truth.
  J-g3  No label reaches the test split.
  J-g4  The signature (`escalations/plan.py`). It does not block a dry run,
        which writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures already published.** It
searches no order on a set of escalations but the 286 named, whose figures
`PLAN_STUDENTS.md` published. `J-g2` builds the selections to check them and
hands none of them to the instrument. `tests/test_escalations.py` walks this
module's syntax tree to say so: every call of `instrument.read` is handed the
train half, one of the audit record's own draws, or the 286.
"""

from __future__ import annotations

import ast
import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reuse.gates import run_suite
from rung3.local_search import score_order
from students import material as students_material

from . import instrument as I
from . import plan, selections

TRUTH_NAMES = {"truth", "true_action", "hidden_policy", "true_rule_id"}


@dataclass
class Checks:
    jg1: dict
    jg2: dict
    jg3: dict
    jg4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.jg1["passes"] and self.jg2["passes"] and self.jg3["passes"]

    def summary(self) -> dict[str, Any]:
        return {k: {"passes": v["passes"], "what": v.get("what")}
                for k, v in (("J-g1", self.jg1), ("J-g2", self.jg2),
                             ("J-g3", self.jg3))} | {"J-g4": self.jg4}


def published_rows() -> dict[int, list[dict]]:
    """The audit record's split-0 rows, by number of labels."""
    runs = json.loads(plan.BUDGET.read_text())["label_budget_runs"]
    out: dict[int, list[dict]] = {}
    for r in runs:
        if r["split"] == plan.SPLIT:
            out.setdefault(r["labels"], []).append(r)
    for rows in out.values():
        rows.sort(key=lambda r: r["draw"])
    return out


def material(inst, escs) -> dict[str, Any]:
    """§1's counts, recomputed."""
    corpus, truth, matched, action = (inst["corpus"], inst["truth"],
                                      inst["matched"], inst["action"])
    records = {r["idx"]: r for r in json.loads(plan.RUNG1.read_text())["records"]}
    by_truth: dict[str, int] = {}
    queues: dict[int, int] = {}
    for i in escs:
        by_truth[truth[i]] = by_truth.get(truth[i], 0) + 1
        q = len({action[r] for r in matched[i]})
        queues[q] = queues.get(q, 0) + 1
    counts = sorted(len(matched[i]) for i in escs)
    return {
        "escalations": len(escs),
        "conflict": sum(1 for i in escs if records[i]["outcome"] == "CONFLICT"),
        "impasse": sum(1 for i in escs if records[i]["outcome"] == "IMPASSE"),
        "distinct_tickets": len({corpus[i].key() for i in escs}),
        "keyword": sum(1 for i in escs if corpus[i].has_security_keyword),
        "by_truth": dict(sorted(by_truth.items(), key=lambda kv: -kv[1])),
        "queues_matching": dict(sorted(queues.items())),
        "rules_matching": {"min": counts[0], "median": statistics.median(counts),
                           "max": counts[-1]},
    }


def gate_jg1(suite: bool = True) -> dict[str, Any]:
    problems: list[str] = []
    inst = I.instance()
    tr, te = I.halves(inst)
    escs = selections.escalations(tr)
    got = material(inst, escs)
    if got != plan.MATERIAL:
        problems.append(f"the material is not §1's: {got}")

    arrival = sorted(inst["ids"], key=lambda r: (inst["born"][r], r))
    sM, sW, sfull, _sn = I.space_masks()
    arr = (score_order(arrival, *I.test_masks()), score_order(arrival, sM, sW, sfull))
    if arr != (plan.ARRIVAL, plan.ARRIVAL_SPACE):
        problems.append(f"arrival order gives {arr}")

    pub = published_rows()
    reproduced = {}
    full = I.read(inst, tr)
    reproduced["full"] = [full["test_share"], full["space_share"]]
    if reproduced["full"] != [plan.PUBLISHED_FULL["ls_test"],
                              plan.PUBLISHED_FULL["ls_space"]]:
        problems.append(f"the full search gives {reproduced['full']}")
    for k in (10, 50):
        for row in pub[k]:
            key = f"{k}|{row['draw']}"
            r = I.read(inst, I.record_draw(inst, k, row["draw"]))
            reproduced[key] = [r["test_share"], r["space_share"]]
            if reproduced[key] != [row["ls_test"], row["ls_space"]]:
                problems.append(f"the record's draw {key} gives {reproduced[key]}")

    named = students_material.answer_set("rung1", "train").idx
    r = I.read(inst, named)
    reproduced["named_286"] = [r["test"], r["space"]]
    if [r["test"], r["space"]] != [plan.NAMED_286["test"], plan.NAMED_286["space"]]:
        problems.append(f"the 286 named give {reproduced['named_286']}")

    tests = run_suite() if suite else {"ran": False, "passes": None}
    if tests["passes"] is False:
        problems.append("the suite is not green")
    return {"what": "the material and the instrument are the records'; the suite green",
            "material": got, "arrival": list(arr), "reproduced": reproduced,
            "suite": tests, "problems": problems, "passes": not problems}


# ---------------------------------------------------------------------------

def names_in(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    names |= {n.arg for n in ast.walk(tree) if isinstance(n, ast.arg)}
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            names |= {a.name for a in n.names}
            if isinstance(n, ast.ImportFrom) and n.module:
                names |= set(n.module.split("."))
    return names


def gate_jg2() -> dict[str, Any]:
    problems: list[str] = []
    inst = I.instance()
    tr, _te = I.halves(inst)
    escs = selections.escalations(tr)
    counts = I.matching(inst)
    a, b = selections.selections(escs, counts), selections.selections(escs, counts)
    if a != b:
        problems.append("two builds of the selections differ")
    pool = set(escs)
    for name, sel in a.items():
        k = len(escs) if name == "all" else int(name.split("|")[1])
        if len(sel) != k or len(set(sel)) != k or not set(sel) <= pool:
            problems.append(f"{name} is not {k} of the escalations")
    leaked = sorted(names_in(Path(selections.__file__)) & TRUTH_NAMES)
    if leaked:
        problems.append(f"selections.py names the truth: {leaked}")
    return {"what": "the selections read no truth",
            "sets": len(a), "truth_names": leaked,
            "problems": problems, "passes": not problems}


def gate_jg3() -> dict[str, Any]:
    inst = I.instance()
    tr, te = I.halves(inst)
    escs = selections.escalations(tr)
    corpus = inst["corpus"]
    keys = {corpus[i].key() for i in escs}
    reach = sum(1 for i in te if corpus[i].key() in keys)
    outside = sorted(set(escs) - set(tr))
    return {"what": "no label reaches the test split",
            "reach": reach, "outside_the_train_half": len(outside),
            "passes": reach == 0 and not outside}


def run_all(suite: bool = True) -> Checks:
    return Checks(gate_jg1(suite), gate_jg2(), gate_jg3(), plan.gate_signature())


def report(c: Checks) -> None:
    for name, g in (("J-g1", c.jg1), ("J-g2", c.jg2), ("J-g3", c.jg3)):
        print(f"  {name}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        for p in g.get("problems", []):
            print(f"        - {p}")
    s = c.jg1.get("suite", {})
    if s.get("ran"):
        print(f"        suite: {s.get('tests')} tests, {s.get('result')}, "
              f"{s.get('seconds')} s")
    g4 = c.jg4
    print(f"  J-g4: {'PASS' if g4['passes'] else 'UNSIGNED'}  {g4['found']} "
          f"signature line(s), {g4['unsigned']} blank")
