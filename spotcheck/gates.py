"""
`N-g1` to `N-g4` of `PLAN_SPOTCHECK.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  N-g1  The material and the instrument are the records'. The suite is green.
        The material of §1 recomputes, each draw's make-up with it. Arrival
        order gives 519 and 42,310. The records hold §4's endpoints, and the
        instrument reproduces them: the whole train half, the escalations
        alone, each by rare class too, and the optimizer audit's five draws at
        50 labels.
  N-g2  The selections read no truth. Built twice they are equal; every
        audited set holds the escalations and exactly its decisions; the
        budgets nest; `selections.py` names no truth, in a name or a string.
  N-g3  No label reaches the test split.
  N-g4  The signature (`spotcheck/plan.py`). It does not block a dry run,
        which writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures already published.** It
searches no order on a set holding decisions but the whole train half, and no
set of escalations but all 316: the optimizer audit published the first and
`PLAN_ESCALATIONS.md` the second. `N-g2` builds the selections to check them and
hands none of them to the instrument. `tests/test_spotcheck.py` walks this
module's syntax tree to say so: every call of `instrument.read` is handed the
train half, the escalations, or one of the record's own draws.
"""

from __future__ import annotations

import ast
import json
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from escalations import gates as esc_gates
from escalations import instrument as I
from escalations.selections import escalations
from reuse.gates import run_suite
from rung3.local_search import score_order

from . import plan, selections

# The truth's names, and the record fields that carry it or the system's own
# decision. The selection module reads none of them, in a name or a string.
FORBIDDEN = esc_gates.TRUTH_NAMES | {"truth_rule", "correct",
                                     "proposal_action_correct", "predicted"}


@dataclass
class Checks:
    ng1: dict
    ng2: dict
    ng3: dict
    ng4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.ng1["passes"] and self.ng2["passes"] and self.ng3["passes"]


def records() -> dict[int, dict]:
    return {r["idx"]: r for r in json.loads(plan.RUNG1.read_text())["records"]}


def rare(read: dict) -> dict[str, int]:
    """Right decisions on the four rare queues, from an instrument read."""
    return {c: read["per_class"][c]["right"] for c in plan.RARE}


def material(inst, decs) -> dict[str, Any]:
    """§1's counts, recomputed."""
    corpus, truth, matched, action = (inst["corpus"], inst["truth"],
                                      inst["matched"], inst["action"])
    recs = records()
    queues = Counter(len({action[r] for r in matched[i]}) for i in decs)
    counts = sorted(len(matched[i]) for i in decs)
    return {
        "decisions": len(decs),
        "outcome": dict(Counter(recs[i]["outcome"] for i in decs)),
        "decided_right": sum(1 for i in decs if recs[i]["correct"]),
        "distinct_tickets": len({corpus[i].key() for i in decs}),
        "keyword": sum(1 for i in decs if corpus[i].has_security_keyword),
        "by_truth": dict(Counter(truth[i] for i in decs).most_common()),
        "decided": dict(Counter(recs[i]["predicted"] for i in decs).most_common()),
        "queues_matching": dict(sorted(queues.items())),
        "rules_matching": {"min": counts[0], "median": statistics.median(counts),
                           "max": counts[-1]},
    }


def draw_make_up(inst, decs) -> dict[int, dict[int, tuple]]:
    """§1's table: per draw and budget, the T3_ENGINEERING, SECURITY_INCIDENT
    and keyword tickets, and the decisions rung 1 got wrong."""
    truth, corpus = inst["truth"], inst["corpus"]
    recs = records()
    out: dict[int, dict[int, tuple]] = {}
    for d in range(plan.DRAWS):
        perm = selections.shuffle(decs, d)
        out[d] = {}
        for k in plan.BUDGETS:
            sel = perm[:k]
            out[d][k] = (sum(1 for i in sel if truth[i] == "T3_ENGINEERING"),
                         sum(1 for i in sel if truth[i] == "SECURITY_INCIDENT"),
                         sum(1 for i in sel if corpus[i].has_security_keyword),
                         sum(1 for i in sel if not recs[i]["correct"]))
    return out


def held_by_records() -> dict[str, Any]:
    """§4's endpoints as their records hold them."""
    esc = json.loads(plan.ESCALATIONS.read_text())["results"]["all"]
    pc = json.loads(plan.BUDGET.read_text())["per_class_split0"]
    return {"escalations": {"test": esc["test"], "space": esc["space"],
                            "rare": rare(esc)},
            "full_rare": {c: pc[c]["ls_total"] for c in plan.RARE},
            "rare_of": {c: pc[c]["test"] for c in plan.RARE},
            "ceiling": {c: pc[c]["ceiling"] for c in plan.RARE}}


def gate_ng1(suite: bool = True) -> dict[str, Any]:
    problems: list[str] = []
    inst = I.instance()
    tr, _te = I.halves(inst)
    escs = escalations(tr)
    decs = selections.decisions(tr)

    got = material(inst, decs)
    if got != plan.MATERIAL:
        problems.append(f"the material is not §1's: {got}")
    make_up = draw_make_up(inst, decs)
    if make_up != plan.DRAW_MAKE_UP:
        problems.append(f"the draws' make-up is not §1's: {make_up}")

    arrival = sorted(inst["ids"], key=lambda r: (inst["born"][r], r))
    sM, sW, sfull, _sn = I.space_masks()
    arr = (score_order(arrival, *I.test_masks()), score_order(arrival, sM, sW, sfull))
    if arr != (plan.ARRIVAL, plan.ARRIVAL_SPACE):
        problems.append(f"arrival order gives {arr}")

    held = held_by_records()
    if held["escalations"] != {**plan.ESC_ALL, "rare": plan.ESC_ALL_RARE}:
        problems.append(f"the escalations' record holds {held['escalations']}")
    if held["full_rare"] != plan.FULL_RARE or held["rare_of"] != plan.RARE_OF:
        problems.append(f"the optimizer audit's record holds {held}")

    reads: dict[str, dict] = {}
    reproduced: dict[str, Any] = {}
    full = I.read(inst, tr)
    reads["full"] = full
    reproduced["full"] = [full["test_share"], full["space_share"], rare(full)]
    if reproduced["full"] != [plan.PUBLISHED_FULL["ls_test"],
                              plan.PUBLISHED_FULL["ls_space"], plan.FULL_RARE]:
        problems.append(f"the whole train half gives {reproduced['full']}")

    alone = I.read(inst, escs)
    reads["escalations"] = alone
    reproduced["escalations"] = [alone["test"], alone["space"], rare(alone)]
    if reproduced["escalations"] != [plan.ESC_ALL["test"], plan.ESC_ALL["space"],
                                     plan.ESC_ALL_RARE]:
        problems.append(f"the escalations alone give {reproduced['escalations']}")

    for row in esc_gates.published_rows()[50]:
        key = f"50|{row['draw']}"
        r = I.read(inst, I.record_draw(inst, 50, row["draw"]))
        reproduced[key] = [r["test_share"], r["space_share"]]
        if reproduced[key] != [row["ls_test"], row["ls_space"]]:
            problems.append(f"the record's draw {key} gives {reproduced[key]}")

    tests = run_suite() if suite else {"ran": False, "passes": None}
    if tests["passes"] is False:
        problems.append("the suite is not green")
    return {"what": "the material and the instrument are the records'; the suite green",
            "material": got, "make_up": make_up, "arrival": list(arr),
            "held": held, "reproduced": reproduced, "reads": reads,
            "suite": tests, "problems": problems, "passes": not problems}


# ---------------------------------------------------------------------------

def literals_in(path: Path) -> set[str]:
    """Every string literal in a module, docstrings included."""
    tree = ast.parse(path.read_text(), filename=str(path))
    return {n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def gate_ng2() -> dict[str, Any]:
    problems: list[str] = []
    inst = I.instance()
    tr, _te = I.halves(inst)
    escs = escalations(tr)
    decs = selections.decisions(tr)
    E, D = set(escs), set(decs)
    if (len(E), len(D)) != (plan.N_ESCALATIONS, plan.N_DECISIONS) or E & D:
        problems.append(f"{len(E)} escalations and {len(D)} decisions, "
                        f"{len(E & D)} in both")
    a, b = selections.selections(escs, decs), selections.selections(escs, decs)
    if a != b:
        problems.append("two builds of the selections differ")
    for k in plan.BUDGETS:
        for d in range(plan.DRAWS):
            mix, alone = a[f"mix|{k}|{d}"], a[f"audit|{k}|{d}"]
            if len(alone) != k or len(set(alone)) != k or not set(alone) <= D:
                problems.append(f"audit|{k}|{d} is not {k} of the decisions")
            if set(mix) != E | set(alone) or len(mix) != len(E) + k:
                problems.append(f"mix|{k}|{d} is not the escalations and its {k}")
    for d in range(plan.DRAWS):
        for small, large in zip(plan.BUDGETS, plan.BUDGETS[1:]):
            if not set(a[f"audit|{small}|{d}"]) <= set(a[f"audit|{large}|{d}"]):
                problems.append(f"draw {d}: {small} is not inside {large}")
    path = Path(selections.__file__)
    leaked = sorted((esc_gates.names_in(path) | literals_in(path)) & FORBIDDEN)
    if leaked:
        problems.append(f"selections.py names the truth: {leaked}")
    return {"what": "the selections read no truth",
            "sets": len(a), "forbidden_names": leaked,
            "problems": problems, "passes": not problems}


def gate_ng3() -> dict[str, Any]:
    inst = I.instance()
    tr, te = I.halves(inst)
    labelled = set(escalations(tr)) | set(selections.decisions(tr))
    corpus = inst["corpus"]
    keys = {corpus[i].key() for i in labelled}
    reach = sum(1 for i in te if corpus[i].key() in keys)
    outside = sorted(labelled - set(tr))
    return {"what": "no label reaches the test split",
            "reach": reach, "outside_the_train_half": len(outside),
            "passes": reach == 0 and not outside}


def run_all(suite: bool = True) -> Checks:
    return Checks(gate_ng1(suite), gate_ng2(), gate_ng3(), plan.gate_signature())


def report(c: Checks) -> None:
    for name, g in (("N-g1", c.ng1), ("N-g2", c.ng2), ("N-g3", c.ng3)):
        print(f"  {name}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        for p in g.get("problems", []):
            print(f"        - {p}")
    s = c.ng1.get("suite", {})
    if s.get("ran"):
        print(f"        suite: {s.get('tests')} tests, {s.get('result')}, "
              f"{s.get('seconds')} s")
    g4 = c.ng4
    print(f"  N-g4: {'PASS' if g4['passes'] else 'UNSIGNED'}  {g4['found']} "
          f"signature line(s), {g4['unsigned']} blank")
