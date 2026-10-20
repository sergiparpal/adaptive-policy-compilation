"""
`Z-g1` to `Z-g4` of `PLAN_UNREACHED.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  Z-g1  The material and the instrument are the records'. The suite is green.
        §1's material recomputes: the counts, the table of the 25 rules no
        escalation reaches, their copies, and the curve's reach. Arrival order
        gives 519 and 42,310. The records hold §4's endpoints. The instrument
        reproduces both: their counts on both surfaces and by rare class, the
        start each came from, and the orders `results_spotcheck/readings.json`
        kept. The key rule moved to the front of the escalations' order gives
        the count that record published. Each of the optimizer audit's twenty
        draws of random arrivals gives the record's test and space shares and
        start.
  Z-g2  The moves read no truth. `unreached/moves.py` names none, in a name or
        a string literal; on a toy order built by hand, the front, the back and
        the coin are the permutations §3 defines, and reach is read off
        matching alone.
  Z-g3  No label reaches the test split. Every labelled case of every order
        read is in the train half, and no test case shares a ticket with one.
        **The rules do reach it**, by birth, and that is §6.1's trap, not this
        check's.
  Z-g4  The signature (`unreached/plan.py`). It does not block a dry run,
        which writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures already published.** It
searches the orders the stage reads, which the records already score, and the
one move it applies is the key rule's to the front of the escalations' order,
whose count `results_spotcheck/readings.json` published. It applies no other
front move, no back move and no coin to a searched order, and scores none.
`tests/test_unreached.py` walks this module's syntax tree to say so.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from escalations import gates as esc_gates
from escalations import instrument as I
from escalations.selections import escalations
from reuse.gates import run_suite
from rung3.local_search import score_order
from spotcheck import gates as sp_gates

from . import moves, plan

# The truth's names, and the record fields that carry it or the system's own
# decision: SPOTCHECK's list. `moves.py` reads none of them.
FORBIDDEN = sp_gates.FORBIDDEN


@dataclass
class Checks:
    zg1: dict
    zg2: dict
    zg3: dict
    zg4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.zg1["passes"] and self.zg2["passes"] and self.zg3["passes"]


def rare(per_class: dict) -> dict[str, int]:
    return {c: per_class[c]["right"] for c in plan.RARE}


# ---------------------------------------------------------------------------
# §1's material, recomputed: matching, halves, the escalated flag, birth
# indices, queues and extensions. No truth and no order.
# ---------------------------------------------------------------------------

def _block(inst, U: list[str], te) -> dict[str, Any]:
    matched, corpus, rules = inst["matched"], inst["corpus"], inst["rules"]
    born = {r["rule_id"]: r["born_at"] for r in rules}
    act = {r["rule_id"]: r["action"] for r in rules}
    sM = I.space_masks()[0]
    on_test = {r: [i for i in te if r in matched[i]] for r in U}
    us = set(U)
    tes = set(te)
    return {
        "unreached": len(U),
        "distinct": len(moves.distinct(rules, U)),
        "born_in_test": sum(1 for r in U if born[r] in tes),
        "by_queue": dict(Counter(act[r] for r in U).most_common()),
        "test_matches": sum(len(v) for v in on_test.values()),
        "birth_ticket_matches": sum(len(moves.birth_ticket(corpus, born[r], on_test[r]))
                                    for r in U),
        "test_cases_touched": sum(1 for i in te if us & set(matched[i])),
        "test_cases_only_unreached": sum(1 for i in te
                                         if matched[i] and set(matched[i]) <= us),
        "space_points": sum(sM[r].bit_count() for r in U),
    }


def material(inst) -> dict[str, Any]:
    """§1's counts."""
    tr, te = I.halves(inst)
    escs = escalations(tr)
    ids, matched, rules = inst["ids"], inst["matched"], inst["rules"]
    born = {r["rule_id"]: r["born_at"] for r in rules}
    tes, trs, es = set(te), set(tr), set(escs)
    return {
        "rules": len(ids),
        "born_in_test": sum(1 for r in ids if born[r] in tes),
        "born_in_train": sum(1 for r in ids if born[r] in trs),
        "match_their_birth_case": sum(1 for r in ids if r in matched[born[r]]),
        "born_at_a_train_escalation": sum(1 for r in ids if born[r] in es),
        "escalations": _block(inst, moves.unreached(ids, matched, escs), te),
        "full": _block(inst, moves.unreached(ids, matched, tr), te),
    }


def table(inst) -> dict[str, tuple]:
    """§1's table: every rule no escalation reaches."""
    tr, te = I.halves(inst)
    ids, matched, corpus, rules = (inst["ids"], inst["matched"], inst["corpus"],
                                   inst["rules"])
    by = {r["rule_id"]: r for r in rules}
    sM = I.space_masks()[0]
    full = set(moves.unreached(ids, matched, tr))
    out = {}
    for rid in moves.unreached(ids, matched, escalations(tr)):
        r = by[rid]
        on_test = [i for i in te if rid in matched[i]]
        out[rid] = (r["action"], r["born_at"], len(r["conditions"]), len(on_test),
                    len(moves.birth_ticket(corpus, r["born_at"], on_test)),
                    sM[rid].bit_count(), rid in full)
    return out


def curve_reach(inst) -> dict[int, tuple]:
    """§1's curve: the rules no label reaches, per draw and budget."""
    ids, matched = inst["ids"], inst["matched"]
    return {k: tuple(len(moves.unreached(ids, matched, I.record_draw(inst, k, d)))
                     for d in range(plan.DRAWS))
            for k in plan.BUDGETS}


def held_by_records() -> dict[str, Any]:
    """§4's endpoints and the key rule's move, as their records hold them."""
    esc = json.loads(plan.ESCALATIONS.read_text())["results"]["all"]
    full = json.loads(plan.SPOTCHECK.read_text())["endpoints"]["full"]
    pc = json.loads(plan.BUDGET.read_text())["per_class_split0"]
    rd = json.loads(plan.READINGS.read_text())
    return {
        "escalations": {"test": esc["test"], "space": esc["space"],
                        "best_from": esc["best_from"], "rare": rare(esc["per_class"])},
        "full": {"test": full["test"], "space": full["space"],
                 "best_from": full["best_from"]},
        "full_rare": {c: pc[c]["ls_total"] for c in plan.RARE},
        "key_rule": rd["key_rule"]["rule_id"],
        "key_moved_test": rd["readings"]["escalations"]["moved"]["test"],
        "orders": {name: rd["orders"][name] for name in plan.ENDPOINTS},
    }


def gate_zg1(suite: bool = True) -> dict[str, Any]:
    problems: list[str] = []
    inst = I.instance()
    tr, te = I.halves(inst)
    escs = escalations(tr)

    got = material(inst)
    if got != plan.MATERIAL:
        problems.append(f"the material is not §1's: {got}")
    tab = table(inst)
    if tab != plan.UNREACHED:
        problems.append(f"the table is not §1's: {tab}")
    cps = moves.copies(inst["rules"], list(plan.UNREACHED))
    if cps != [list(plan.COPIES)]:
        problems.append(f"the copies are not §1's: {cps}")
    reach = curve_reach(inst)
    if reach != plan.CURVE_REACH:
        problems.append(f"the curve's reach is not §1's: {reach}")

    test_m = I.test_masks()
    sM, sW, sfull, _sn = I.space_masks()
    arrival = sorted(inst["ids"], key=lambda r: (inst["born"][r], r))
    arr = (score_order(arrival, *test_m), score_order(arrival, sM, sW, sfull))
    if arr != (plan.ARRIVAL, plan.ARRIVAL_SPACE):
        problems.append(f"arrival order gives {arr}")

    held = held_by_records()
    want = {"escalations": {**plan.ESC_ALL, "best_from": plan.BEST_FROM["escalations"],
                            "rare": plan.ESC_ALL_RARE},
            "full": {**plan.FULL, "best_from": plan.BEST_FROM["full"]}}
    if {k: held[k] for k in want} != want or held["full_rare"] != plan.FULL_RARE:
        problems.append(f"the records hold {held}")
    if held["key_rule"] != plan.KEY_RULE:
        problems.append(f"the T3_ENGINEERING reading's key rule is {held['key_rule']}")

    orders: dict[str, Any] = {}
    starts: dict[str, str] = {}
    reproduced: dict[str, Any] = {}
    for name, labelled in (("escalations", escs), ("full", tr)):
        order, st = I.labelled_order(inst, labelled)
        order = list(order)
        orders[name], starts[name] = order, st["best_from"]
        got_e = {"test": score_order(order, *test_m),
                 "space": score_order(order, sM, sW, sfull),
                 "best_from": st["best_from"],
                 "rare": rare(I.per_class(inst, order, te))}
        reproduced[name] = got_e
        expect = ({**want[name]} if name == "escalations"
                  else {**want[name], "rare": plan.FULL_RARE})
        if got_e != expect:
            problems.append(f"the {name} order gives {got_e}")
        if order != held["orders"][name]:
            problems.append(f"the {name} order is not the one readings.json kept")
    shares = [round(reproduced["full"]["test"] / plan.N_TEST, plan.SPACE_PLACES),
              round(reproduced["full"]["space"] / plan.N_SPACE, plan.SPACE_PLACES)]
    if shares != [plan.PUBLISHED_FULL["ls_test"], plan.PUBLISHED_FULL["ls_space"]]:
        problems.append(f"the whole train half's shares are {shares}")

    moved = score_order(moves.front(orders["escalations"], plan.KEY_RULE), *test_m)
    reproduced["key_moved_test"] = moved
    if moved != held["key_moved_test"]:
        problems.append(f"the key rule at the front gives {moved}, "
                        f"not {held['key_moved_test']}")

    curve: dict[str, list[str]] = {}
    for k, rows in esc_gates.published_rows().items():
        if k not in plan.BUDGETS:
            continue
        for row in rows:
            key = f"{k}|{row['draw']}"
            order, st = I.labelled_order(inst, I.record_draw(inst, k, row["draw"]))
            order = list(order)
            curve[key], starts[key] = order, st["best_from"]
            got_c = [round(score_order(order, *test_m) / plan.N_TEST, plan.SPACE_PLACES),
                     round(score_order(order, sM, sW, sfull) / plan.N_SPACE,
                           plan.SPACE_PLACES),
                     st["best_from"]]
            reproduced[key] = got_c
            if got_c != [row["ls_test"], row["ls_space"], row["best_from"]]:
                problems.append(f"the record's draw {key} gives {got_c}")
    if sorted(curve) != sorted(f"{k}|{d}" for k in plan.BUDGETS
                               for d in range(plan.DRAWS)):
        problems.append(f"the curve holds {sorted(curve)}")

    tests = run_suite() if suite else {"ran": False, "passes": None}
    if tests["passes"] is False:
        problems.append("the suite is not green")
    return {"what": "the material and the instrument are the records'; the suite green",
            "material": got, "arrival": list(arr), "held": {k: v for k, v in held.items()
                                                           if k != "orders"},
            "reproduced": reproduced, "starts": starts,
            "orders": {"endpoints": orders, "curve": curve},
            "suite": tests, "problems": problems, "passes": not problems}


# ---------------------------------------------------------------------------

def gate_zg2() -> dict[str, Any]:
    """The moves read no truth, and they are the permutations §3 defines."""
    problems: list[str] = []
    path = Path(moves.__file__)
    leaked = sorted((esc_gates.names_in(path) | sp_gates.literals_in(path)) & FORBIDDEN)
    if leaked:
        problems.append(f"moves.py names the truth: {leaked}")

    toy = ["a", "b", "c", "d", "e", "f"]
    toy_unreached = ["e", "b"]
    if moves.front(toy, "e") != ["e", "a", "b", "c", "d", "f"]:
        problems.append("front is not the rule first and the rest as they were")
    if moves.back(toy, toy_unreached) != ["a", "c", "d", "f", "b", "e"]:
        problems.append("back is not the reached, then the unreached, each in order")
    placed = [moves.coin(toy, toy_unreached, d) for d in range(plan.COIN_DRAWS)]
    if placed != [moves.coin(toy, toy_unreached, d) for d in range(plan.COIN_DRAWS)]:
        problems.append("the coin is not seeded")
    for o in placed:
        if sorted(o) != toy or [r for r in o if r not in {"b", "e"}] != ["a", "c", "d", "f"]:
            problems.append(f"a placement is not a permutation keeping the reached: {o}")
            break
    if len({tuple(o) for o in placed}) < 2:
        problems.append("the coin places the unreached in one way only")
    toy_matched = [["a", "b"], ["c"], ["d", "a"]]
    if moves.unreached(toy, toy_matched, [0, 2]) != ["c", "e", "f"]:
        problems.append("reach is not read off matching")
    toy_rules = [
        {"rule_id": "a", "born_at": 5, "action": "Q", "conditions": [
            {"attr": "x", "op": "eq", "value": 1}, {"attr": "y", "op": "eq", "value": 2}]},
        {"rule_id": "b", "born_at": 3, "action": "Q", "conditions": [
            {"attr": "y", "op": "eq", "value": 2}, {"attr": "x", "op": "eq", "value": 1}]},
        {"rule_id": "c", "born_at": 4, "action": "R", "conditions": [
            {"attr": "x", "op": "eq", "value": 1}, {"attr": "y", "op": "eq", "value": 2}]},
    ]
    if (moves.copies(toy_rules, ["a", "b", "c"]) != [["b", "a"]]
            or moves.distinct(toy_rules, ["a", "b", "c"]) != ["b", "c"]):
        problems.append("copies are not the rules written the same, conditions and queue")
    return {"what": "the moves read no truth", "forbidden_names": leaked,
            "problems": problems, "passes": not problems}


def gate_zg3() -> dict[str, Any]:
    inst = I.instance()
    tr, te = I.halves(inst)
    sets = [escalations(tr), tr] + [I.record_draw(inst, k, d)
                                    for k in plan.BUDGETS for d in range(plan.DRAWS)]
    labelled = set().union(*map(set, sets))
    corpus = inst["corpus"]
    keys = {corpus[i].key() for i in labelled}
    reach = sum(1 for i in te if corpus[i].key() in keys)
    outside = sorted(labelled - set(tr))
    return {"what": "no label reaches the test split",
            "reach": reach, "outside_the_train_half": len(outside),
            "passes": reach == 0 and not outside}


def run_all(suite: bool = True) -> Checks:
    return Checks(gate_zg1(suite), gate_zg2(), gate_zg3(), plan.gate_signature())


def report(c: Checks) -> None:
    for name, g in (("Z-g1", c.zg1), ("Z-g2", c.zg2), ("Z-g3", c.zg3)):
        print(f"  {name}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        for p in g.get("problems", []):
            print(f"        - {p}")
    s = c.zg1.get("suite", {})
    if s.get("ran"):
        print(f"        suite: {s.get('tests')} tests, {s.get('result')}, "
              f"{s.get('seconds')} s")
    g4 = c.zg4
    print(f"  Z-g4: {'PASS' if g4['passes'] else 'UNSIGNED'}  {g4['found']} "
          f"signature line(s), {g4['unsigned']} blank")
