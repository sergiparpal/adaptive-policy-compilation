"""
THE STAGE of `PLAN_STUDENTS.md` §9: the students against the rules, scored.

It refuses while §0 is unsigned, before it builds or measures anything; no flag
skips that. `--dry-run` runs `T-g1` to `T-g3` and writes nothing. Then, in this
order, and every step blocking:

  1. **The blocking checks**, `students/gates.py`.
  2. **The students**: the tree, the regression and the cache, each fitted on
     every answer set of `students/material.py`, rung 1's and each
     `PLAN_REUSE.md` run's, `all` and `train`; and, labelled so, the same three
     on the same tickets handed the truth.
  3. **The rules' side**, `students/rules.py`: arrival order and its reverse,
     rung 1's own engine, the order searched on the answers (the 286 and the
     579) and on the truth at the 286, and each `PLAN_REUSE.md` base under rung
     2's engine and in arrival order.
  4. **Every figure by a second route** (rule G of §6): the tree's predictions
     against the frozen `RuleEngine` running its rules, on every test case;
     every space mask against point-by-point prediction on `T-g2`'s 2,000
     points; each base's regions against its `decide` on every test case. A
     disagreement stops the stage before anything is written.
  5. **`T-a` to `T-e`**, each with its discordance and §0's label, and the
     readings of `T-f`.

Surfaces: corpus test split 0, 995 cases, and the exhaustive space, 134,400
points, every count against the truth. A case an engine leaves in CONFLICT or
IMPASSE counts as not right. A student always answers.

PROVENANCE: PRE-REGISTERED. §0 was signed before any figure here existed; the
gate is what says so.

    python3 -m students.score --dry-run           # T-g1..T-g3, blocking; writes nothing
    PYTHONHASHSEED=0 python3 -m students.score    # T-a to T-e, and the readings of T-f
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from typing import Any, Callable, Sequence

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.provenance import describe, environment

from . import cache, gates, logistic, material, plan, rules, tree

RARE = ("ACCOUNT_MANAGER", "T3_ENGINEERING", "SECURITY_INCIDENT",
        "ONCALL_ESCALATION")
STUDENTS: dict[str, Callable] = {"tree": tree.fit, "logistic": logistic.fit,
                                 "cache": cache.fit}


class Disagreement(Exception):
    """Two routes to one figure disagree: the instrument, not a row."""


# ---------------------------------------------------------------------------
# Reading one artefact on the test split
# ---------------------------------------------------------------------------

def on_test(decide: Callable[[int], str | None], test: Sequence[int],
            truth: Sequence[str], reached: set[int] | None = None) -> dict[str, Any]:
    """An artefact's decision on every test case, by corpus index, and what §9
    reads off it. `None` is an abstention, which is not right."""
    decided = {i: decide(i) for i in test}
    right = {i for i in test if decided[i] == truth[i]}
    out = {"right": len(right), "of": len(test),
           "abstained": sum(1 for i in test if decided[i] is None),
           "per_class": {c: {"right": sum(1 for i in right if truth[i] == c),
                             "of": sum(1 for i in test if truth[i] == c)}
                         for c in RARE}}
    if reached is not None:
        out["reached"] = {"right": len(right & reached), "of": len(reached)}
        out["not_reached"] = {"right": len(right - reached),
                              "of": len(test) - len(reached)}
    return out | {"_decided": decided, "_right": right}


def discordance(a: dict, b: dict) -> dict[str, Any]:
    """`b` where only the first is right and `c` where only the second is, and
    §0's label."""
    only_a = len(a["_right"] - b["_right"])
    only_b = len(b["_right"] - a["_right"])
    return {"b": only_a, "c": only_b, "thin": plan.thin(only_a, only_b)}


def agreement(a: dict, b: dict) -> int:
    return sum(1 for i, d in a["_decided"].items() if d == b["_decided"][i])


# ---------------------------------------------------------------------------
# The students
# ---------------------------------------------------------------------------

def fit_students(cases, labels) -> dict[str, Any]:
    return {name: fn(cases, labels) for name, fn in STUDENTS.items()}


def student_space(name: str, student, space_cases) -> dict[str, int]:
    if name == "tree":
        return gates.tree_masks(student.tree)
    if name == "cache":
        return cache.space_masks(student, rules.space())
    return gates.predictions_mask(student, space_cases)


def check_masks(name, student, masks, space_cases, points) -> None:
    bad = sum(1 for i in points
              if gates._decided_at(masks, i, plan.N_SPACE) != student.predict(space_cases[i]))
    if bad:
        raise Disagreement(f"{name}'s space masks disagree on {bad} points")


def check_tree_engine(fitted, test) -> None:
    corpus = material.corpus()
    bad = gates.engine_problems(fitted.tree, [corpus[i] for i in test])
    if bad:
        raise Disagreement(f"the frozen engine disagrees with the tree on {bad} test cases")


def describe_student(name: str, student) -> dict[str, Any]:
    if name == "tree":
        return tree.describe(student)
    if name == "logistic":
        return logistic.describe(student)
    return {"stored": len(student.store)}


def read_students(sets, labels_of, truth, test, space_cases, points,
                  reached_of) -> tuple[dict, dict]:
    """Every student on every set, on both surfaces; and the fitted students,
    kept out of the record."""
    rows, fitted = {}, {}
    for s in sets:
        labels = labels_of(s)
        studs = fit_students(s.cases(), labels)
        fitted[s.name] = studs
        rows[s.name] = {}
        corpus = material.corpus()
        for name, st in studs.items():
            t = on_test(lambda i, st=st: st.predict(corpus[i]), test, truth,
                        reached_of(s))
            masks = student_space(name, st, space_cases)
            check_masks(f"{s.name} {name}", st, masks, space_cases, points)
            if name == "tree":
                check_tree_engine(st, test)
            rows[s.name][name] = t | {
                "space": {"right": rules.right_over_space(masks), "of": plan.N_SPACE},
                "fit": describe_student(name, st)}
    return rows, fitted


def majority_floor(s, labels, truth, test) -> dict[str, Any]:
    """The set's commonest label, answered everywhere; ties to `ACTIONS` order."""
    counts = {a: labels.count(a) for a in ACTIONS}
    top = max(ACTIONS, key=lambda a: (counts[a], -ACTIONS.index(a)))
    t = rules.space_truth()
    return {"queue": top, "test": sum(1 for i in test if truth[i] == top),
            "space": t.get(top, 0).bit_count()}


# ---------------------------------------------------------------------------
# The rules' side
# ---------------------------------------------------------------------------

def order_decider(base: rules.Rung1, order: list[str]) -> Callable[[int], str | None]:
    """First match in `order` over the `puro` pool, by corpus index."""
    rank = {rid: k for k, rid in enumerate(order)}

    def decide(i: int) -> str | None:
        m = base.matched[i]
        return base.action[min(m, key=rank.__getitem__)] if m else None
    return decide


def specificity_point(base: rules.Rung1, case, ncond) -> str | None:
    """Rung 1's engine on any ticket, from the rules' conditions: the second
    route to its masks over the space."""
    m = [rid for rid in base.ids if all(c.holds(case) for c in base.conds[rid])]
    if not m:
        return None
    top = max(ncond[r] for r in m)
    finalists = {base.action[r] for r in m if ncond[r] == top}
    return finalists.pop() if len(finalists) == 1 else None


def read_order(base, order, test, truth, test_masks, space_masks, reached) -> dict:
    row = on_test(order_decider(base, order), test, truth, reached)
    if row["right"] != rules.scored(order, test_masks):
        raise Disagreement("an order's test count is not score_order's")
    return row | {"space": {"right": rules.scored(order, space_masks),
                            "of": plan.N_SPACE}}


def read_rules(base, test, truth, reached, space_cases, points) -> dict[str, Any]:
    tm, sm = base.test_masks(), base.space_masks()
    out = {
        "arrival": read_order(base, base.arrival(), test, truth, tm, sm, reached),
        "reversed": read_order(base, base.reversed_arrival(), test, truth, tm, sm,
                               reached),
    }
    ncond = {r["rule_id"]: len(r["conditions"]) for r in base.rules}
    spec = on_test(lambda i: gates._specificity_case(base, i, ncond),
                   test, truth, reached)
    if spec["right"] != round(rules.specificity_test(base) * len(test)):
        raise Disagreement("rung 1's engine on the test split is not eval_specificity's")
    sspace = rules.specificity_space(base)
    bad = sum(1 for i in points
              if gates._decided_at(sspace, i, plan.N_SPACE)
              != specificity_point(base, space_cases[i], ncond))
    if bad:
        raise Disagreement(f"rung 1's engine over the space disagrees on {bad} points")
    out["specificity"] = spec | {"space": {
        "right": rules.right_over_space(sspace), "of": plan.N_SPACE,
        "abstained": plan.N_SPACE - sum(m.bit_count() for m in sspace.values())}}
    named = material.answers("rung1")
    for name, idx, labels in (
            ("answers_order_286", material.answer_set("rung1", "train").idx, named),
            ("answers_order_579", material.answer_set("rung1", "all").idx, named),
            ("truth_order_286", material.answer_set("rung1", "train").idx, base.truth)):
        order, st = rules.search_order(base, labels, idx)
        out[name] = read_order(base, order, test, truth, tm, sm, reached) | {
            "search": st}
    return out


def test_masks_of(rules_in_order, test, truth):
    """`(M, W, full)` of a base's rules over the test split, built from their
    conditions: the second route to a base's count in arrival order."""
    corpus = material.corpus()
    M = {r.rule_id: 0 for r in rules_in_order}
    W = dict(M)
    for k, i in enumerate(test):
        for r in rules_in_order:
            if r.matches(corpus[i]):
                M[r.rule_id] |= 1 << k
                if r.action == truth[i]:
                    W[r.rule_id] |= 1 << k
    return M, W, (1 << len(test)) - 1


def read_reuse_bases(test, truth, space_cases, points) -> dict[str, Any]:
    out = {}
    corpus = material.corpus()
    for run in material.RUNS[1:]:
        engine = rules.reuse_base(run).engine
        row = on_test(lambda i, e=engine: rules.decide_action(e, corpus[i]), test,
                      truth, set(material.reached(material.answer_set(run, "all"))))
        reg = rules.regions(engine)
        bad = sum(1 for i in test if gates._decided_at(
            reg, rules.space_index(corpus[i]), plan.N_SPACE) != row["_decided"][i])
        bad += sum(1 for i in points if gates._decided_at(reg, i, plan.N_SPACE)
                   != rules.decide_action(engine, space_cases[i]))
        if bad:
            raise Disagreement(f"{run}: the regions disagree with decide on {bad} cases")
        decided = sum(m.bit_count() for m in reg.values())
        order, M, W, full = rules.reuse_arrival(engine)
        in_order = sorted(engine.rules, key=lambda r: (r.born_at, r.rule_id))
        arrival = on_test(lambda i, rs=in_order: rules.first_match(rs, corpus[i]),
                          test, truth)
        tM, tW, tfull = test_masks_of(in_order, test, truth)
        if arrival["right"] != rules.scored(order, (tM, tW, tfull)):
            raise Disagreement(f"{run}: the base in arrival order is not score_order's")
        out[run] = {
            "base": row | {"space": {"right": rules.right_over_space(reg),
                                     "of": plan.N_SPACE,
                                     "abstained": plan.N_SPACE - decided},
                           "rules": len(engine.rules)},
            "arrival": arrival | {"space": {"right": rules.scored(order, (M, W, full)),
                                            "of": plan.N_SPACE}},
        }
    return out


# ---------------------------------------------------------------------------
# The rows
# ---------------------------------------------------------------------------

def verdicts(students: dict, rules_side: dict, reuse: dict) -> list[dict[str, Any]]:
    rung1 = students["rung1/all"]
    arrival = rules_side["arrival"]
    tree_row = rung1["tree"]
    best_name = max(STUDENTS, key=lambda n: (rung1[n]["right"], n == "tree"))
    best = rung1[best_name]
    order = rules_side["answers_order_286"]
    diffs = {}
    for run in material.RUNS[1:]:
        t = students[f"{run}/all"]["tree"]
        b = reuse[run]["base"]
        diffs[run] = {"tree": t["right"], "base": b["right"],
                      "difference": t["right"] - b["right"]} | discordance(t, b)
    med = statistics.median(d["difference"] for d in diffs.values())
    median_run = sorted(diffs, key=lambda r: diffs[r]["difference"])[1]
    return [
        {"row": "T-a", "statistic": "the tree's right decisions, rung1/all, test split 0",
         "value": tree_row["right"], "line": plan.T_A_LINE,
         "holds": tree_row["right"] < plan.T_A_LINE} | discordance(tree_row, arrival),
        {"row": "T-b", "statistic": "the best student's right decisions, rung1/all, test split 0",
         "best": best_name, "value": best["right"], "line": plan.T_B_LINE,
         "holds": best["right"] < plan.T_B_LINE} | discordance(best, arrival),
        {"row": "T-c", "statistic": "the tree's right decisions, rung1/all, over the space",
         "value": tree_row["space"]["right"], "line": plan.T_C_LINE,
         "holds": tree_row["space"]["right"] > plan.T_C_LINE},
        {"row": "T-d", "statistic": "the order searched on the 286 train-half answers, test split 0",
         "value": order["right"], "line": plan.T_D_LINE,
         "holds": order["right"] > plan.T_D_LINE} | discordance(order, arrival),
        {"row": "T-e", "statistic": "the median over PLAN_REUSE.md's runs of the tree "
                                    "less the base, test split 0",
         "value": med, "line": plan.T_E_LINE, "holds": med < plan.T_E_LINE,
         "per_run": diffs, "median_run": median_run,
         "thin": diffs[median_run]["thin"]},
    ]


def strip(tree_of_rows):
    if isinstance(tree_of_rows, dict):
        return {k: strip(v) for k, v in tree_of_rows.items() if not str(k).startswith("_")}
    return tree_of_rows


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if not dry:
        gate = plan.refuse_unsigned("students/score.py writes nothing")
    t0 = time.time()
    print("=" * 78)
    print("PLAN_STUDENTS.md — THE STUDENTS AGAINST THE RULES")
    print("=" * 78)
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the checks ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    truth = material.truth()
    test = material.split()[1]
    space_cases = list(all_cases())
    points = gates.sample_points()
    reached = {s.name: set(material.reached(s)) if s.kind == "all" else None
               for s in material.answer_sets()}
    sets = material.answer_sets()
    students, fitted = read_students(sets, lambda s: list(s.labels), truth, test,
                                     space_cases, points, lambda s: reached[s.name])
    handed, _ = read_students(sets, lambda s: [truth[i] for i in s.idx], truth,
                              test, space_cases, points, lambda s: reached[s.name])
    base = rules.rung1()
    rules_side = read_rules(base, test, truth, reached["rung1/all"], space_cases,
                            points)
    reuse = read_reuse_bases(test, truth, space_cases, points)

    arrival = rules_side["arrival"]
    for set_rows in students.values():
        for row in set_rows.values():
            row["agrees_with_arrival"] = agreement(row, arrival)
            row["against_arrival"] = discordance(row, arrival)
    rows = verdicts(students, rules_side, reuse)
    floors = {s.name: majority_floor(s, list(s.labels), truth, test) for s in sets}
    tree_rules = tree.rules(fitted["rung1/all"]["tree"].tree)

    for r in rows:
        print(f"  {r['row']}: {'holds' if r['holds'] else 'REFUTED'}"
              f"{', thin' if r.get('thin') else ''}  {r['value']} against {r['line']}")

    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, folds=plan.FOLDS,
                            fold_seed=plan.FOLD_SEED),
        "what": "three students trained on the proposer's answers, against the "
                "rules it wrote from the same answers",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": "PRE-REGISTERED: §0 signed before any figure here existed",
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, "
                   "134,400 points; every count against the truth; an engine's "
                   "CONFLICT or IMPASSE is not right; a student always answers",
        "gates": strip({"T-g1": checks.tg1, "T-g2": checks.tg2, "T-g3": checks.tg3,
                        "T-g4": checks.tg4}),
        "rows": strip({r["row"]: r for r in rows}),
        "students": strip(students),
        "handed_the_truth": strip(handed),
        "rules_side": strip(rules_side),
        "reuse_bases": strip(reuse),
        "majority_answer": floors,
        "the_tree_in_the_dsl": tree_rules,
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
