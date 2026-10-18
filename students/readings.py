"""
THE THREE READINGS `PLAN_STUDENTS.md` LEFT OPEN. `FINDINGS_STUDENTS.md`, *What
this does not settle*, names three things the stage's record cannot say, and
`IDEAS.md` carries them as free readings of the record. This reads all three.
POST-RUN.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **What the `ONCALL_ESCALATION` leaves cost.** The tree on rung 1's 579
     answers decides that queue's three test cases right, through two leaves
     that send severity-1 tickets there: `L015`, *severity 1 outside billing*,
     and `L024`, *severity 1 in billing, off hours, without the keyword*. They
     take every other severity-1 ticket they cover. On the cases and points
     they decide, by true queue, how often are they right, and how often are
     the rules in arrival order, and reversed?
  B. **Why the train-half tree beats the all-answers tree.** 500 against 470 on
     corpus test split 0. On the 347 test cases whose ticket an answer carries,
     the all-answers students hold the proposer's own answer. How do the three
     students of the train half do on those 347 and on the other 648?
  C. **What the `PLAN_REUSE.md` trees are.** Their rules, and which of the six
     decide every point of the space alike. Three of them score alike on both
     surfaces.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
The students are refitted by the stage's own functions, called and not copied:
`students/score.py`'s `read_students` over every answer set of
`students/material.py`, rung 1's and each run's, with the proposer's queues.
The stage is deterministic, so a refit is the stage's student. Gate 1 says so.

  * **A** reads the refitted tree on `rung1/all`. Its leaves whose queue is
    `ONCALL_ESCALATION` are found by queue, not by name. On the test split it
    reads every case they decide, its true queue, and whether the tree, arrival
    and reversed arrival are right there, arrival's decisions coming from
    `students/score.py`'s `order_decider`. Over the space it reads each leaf's
    extension, by true queue, against the masks of the points arrival and
    reversed arrival get right.
  * **B** reads the three students of `rung1/train` on the reach's partition:
    the 347 test cases `material.reached` gives for `rung1/all`, and the 648
    others.
  * **C** reads the trees of the six `PLAN_REUSE.md` sets: their rules, written
    by `students/tree.py`'s `rules`, and their predictions over the space by
    queue. Two trees decide alike when those masks are equal.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The students are the record's.** Refitted, every student of every set
     scores on the test split and over the space what `score.json` says. The
     tree on `rung1/all` writes the rules `score.json` holds as
     `the_tree_in_the_dsl`, rule for rule.
  2. **The rules' side is the record's.** Arrival order and its reverse, as
     masks of the points they get right, count 42,310 and 76,180 over the space.
     Arrival's decisions on the test split give 519, 173 on the 347 and 346 on
     the 648.
  3. **The space is what the policy forces.** The two leaves' points, by true
     queue, are the counts derived by hand below, before the run.

It refuses to write if any fails, and while `PLAN_STUDENTS.md` is unsigned, like
every writer of the package.

--------------------------------------------------------------------------
WHAT THE POLICY FORCES, DERIVED BEFORE THE RUN
--------------------------------------------------------------------------
From `harness/hidden_policy.py` and the two leaves `score.json` records. These
are not bets; gate 3 checks the run against them.

  `L015`, severity 1 outside billing: 26,880 points. Half carry the keyword,
  and every severity-1 keyword ticket is `SECURITY_INCIDENT`: 13,440. Of the
  13,440 without it, enterprise is `ONCALL_ESCALATION` (3,360), business off
  hours too (1,680) and business on hours `T3_ENGINEERING` (1,680). Free and
  pro go to `T3_ENGINEERING` on the api (1,680) and to `T2_TECHNICAL` elsewhere
  (5,040).
  `L024`, severity 1 in billing, off hours, without the keyword: 1,680 points.
  Enterprise and business are `ONCALL_ESCALATION` (840), and free and pro
  `T2_TECHNICAL` (840).

  So the two leaves cover 28,560 points: 13,440 `SECURITY_INCIDENT`, 5,880
  `ONCALL_ESCALATION`, 5,880 `T2_TECHNICAL` and 3,360 `T3_ENGINEERING`. The tree
  is right on 5,880 of them. The space holds 6,300 `ONCALL_ESCALATION` points;
  the other 420 fall in `L025`, which sends them to `T3_ENGINEERING`.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  A1. **On the test split the two leaves decide between 30 and 50 cases.** The
      corpus's weights put about 41 there.
  A2. **At least two thirds of them are `T2_TECHNICAL` or `T3_ENGINEERING` in
      truth.** The weights put it near six in seven.
  A3. **Arrival order is right on at least 10 more of them than the tree.** The
      tree is right on 3, the queue's three test cases. So the leaves account
      for at least ten of the tree's 49-case gap to arrival.
  A4. **Over the space, arrival order is right on more of the leaves' 28,560
      points than the tree's 5,880.** The drafter trusts this one least: half
      the points are keyword tickets, which arrival mostly sends elsewhere.
  B1. **The train-half tree is right on more of the 347 than the all-answers
      tree's 146.**
  B2. **More than half of its 30-case lead is on the 347**: it is right on more
      than 161 of them.
  B3. **The train-half cache is right on fewer of the 347 than the all-answers
      cache's 154.** Holding the proposer's own answer for the ticket is worth
      something to a retrieval student.
  C1. **The trees on all of run 2's answers, all of run 3's and the train half
      of run 3's decide every point of the space alike.**
  C2. **That one function sends the keyword to `SECURITY_INCIDENT`, billing
      without it to `BILLING_SPECIALIST`, and everything else to
      `T2_TECHNICAL`.**
  C3. **The tree on all of run 1's answers sends every keyword ticket to
      `SECURITY_INCIDENT`.** 29 of its 62 answers name that queue.

**What the drafter had seen**: `results_students/score.json` whole, the tree on
`rung1/all` in the DSL and every student's totals and sizes among it;
`FINDINGS_STUDENTS.md`; the material's counts; `harness/hidden_policy.py`, for
the derivation above; the corpus's sampling weights in `harness/domain.py`, for
A1 and A2.

**Not seen**: which test cases the two leaves decide; what arrival or reversed
arrival does on them or on their points; the train-half students on the 347
and the 648; any `PLAN_REUSE.md` tree's rules; whether any two trees decide
alike.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-18, after the stage, with the expectation
above written and committed before the first run. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls; a few
minutes, most of them the refits.

Usage:  PYTHONHASHSEED=0 python3 -m students.readings
"""

from __future__ import annotations

import json
import sys
import time
from typing import Any

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.provenance import describe, environment

from . import gates, material, plan, rules, score, tree

RECORD = plan.OUT / "readings.json"
ONCALL = "ONCALL_ESCALATION"
REACHED_BY = ("rung1", "all")
SAME = ("reuse2/all", "reuse3/all", "reuse3/train")
PROVENANCE = (
    "POST-RUN: asked for on 2026-10-18, after PLAN_STUDENTS.md's stage. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")

# The derivation of the docstring, before the run: the two leaves' points by
# true queue.
DERIVED = {
    "L015": {"SECURITY_INCIDENT": 13440, "ONCALL_ESCALATION": 5040,
             "T3_ENGINEERING": 3360, "T2_TECHNICAL": 5040},
    "L024": {"ONCALL_ESCALATION": 840, "T2_TECHNICAL": 840},
}
DERIVED_TOTAL = 28560
DERIVED_RIGHT = 5880
SPACE_ONCALL = 6300

# The expectation's lines.
A1_RANGE = (30, 50)
A2_SHARE = (2, 3)
A3_MARGIN = 10
B2_LINE = 161
FIGURES = {"tree_all_reached": 146, "cache_all_reached": 154,
           "tree_all": 470, "tree_train": 500}


# ---------------------------------------------------------------------------
# Masks
# ---------------------------------------------------------------------------

def won_mask(order, M, W, full) -> int:
    """The points an order gets right, first match wins: the mask whose count
    is `score_order`'s."""
    pending, won = full, 0
    for rid in order:
        m = M[rid] & pending
        if m:
            won |= W[rid] & pending
            pending &= ~M[rid]
            if not pending:
                break
    return won


def by_queue(mask: int, truth: dict[str, int]) -> dict[str, int]:
    """A mask's points by true queue, the queues it holds none of left out."""
    out = {}
    for a in ACTIONS:
        k = (mask & truth.get(a, 0)).bit_count()
        if k:
            out[a] = k
    return out


def same_function(a: dict[str, int], b: dict[str, int]) -> bool:
    """Two predictions, as masks by queue, decide every point alike."""
    keys = set(a) | set(b)
    return all(a.get(k, 0) == b.get(k, 0) for k in keys)


# ---------------------------------------------------------------------------
# The three readings
# ---------------------------------------------------------------------------

def oncall_leaves(fitted_tree, test, truth, arrival, reverse,
                  arrival_won, reverse_won) -> dict[str, Any]:
    """Reading A, on the tree of `rung1/all`."""
    payloads = [p for p in tree.rules(fitted_tree.tree) if p["action"] == ONCALL]
    nodes = {p["node"]: p["rule_id"] for p in payloads}
    corpus = material.corpus()
    t = rules.space_truth()
    masks = {p["rule_id"]: m for p, m in gates.leaf_masks(fitted_tree.tree)
             if p["action"] == ONCALL}
    out = {"leaves": payloads, "test": {}, "space": {}}
    decided = [i for i in test
               if fitted_tree.tree.leaf_of(tree.encode(corpus[i])) in nodes]
    for name, idx in (("both", decided),) + tuple(
            (rid, [i for i in decided
                   if nodes[fitted_tree.tree.leaf_of(tree.encode(corpus[i]))] == rid])
            for rid in nodes.values()):
        classes: dict[str, int] = {}
        for i in idx:
            classes[truth[i]] = classes.get(truth[i], 0) + 1
        out["test"][name] = {
            "cases": len(idx), "by_queue": classes,
            "tree_right": sum(1 for i in idx if truth[i] == ONCALL),
            "arrival_right": sum(1 for i in idx if arrival(i) == truth[i]),
            "reversed_right": sum(1 for i in idx if reverse(i) == truth[i])}
    both = 0
    for rid, m in masks.items():
        both |= m
    for name, m in (("both", both),) + tuple(masks.items()):
        out["space"][name] = {
            "points": m.bit_count(), "by_queue": by_queue(m, t),
            "tree_right": (m & t.get(ONCALL, 0)).bit_count(),
            "arrival_right": (m & arrival_won).bit_count(),
            "reversed_right": (m & reverse_won).bit_count()}
    out["space_oncall_points"] = t.get(ONCALL, 0).bit_count()
    return out


def reach_of_the_train_half(rows: dict, record: dict) -> dict[str, Any]:
    """Reading B, beside the record's all-answers students and arrival."""
    rec = record["students"]["rung1/all"]
    arrival = record["rules_side"]["arrival"]
    return {
        "train_half": {n: {"reached": r["reached"], "not_reached": r["not_reached"],
                           "right": r["right"]}
                       for n, r in rows["rung1/train"].items()},
        "all_answers": {n: {"reached": r["reached"], "not_reached": r["not_reached"],
                            "right": r["right"]} for n, r in rec.items()},
        "arrival": {"reached": arrival["reached"], "not_reached": arrival["not_reached"],
                    "right": arrival["right"]},
    }


def reuse_trees(fitted: dict) -> tuple[dict[str, Any], dict]:
    """Reading C: each `PLAN_REUSE.md` tree's rules and its predictions by
    queue; which pairs decide alike."""
    trees, preds = {}, {}
    for name, studs in fitted.items():
        if not name.startswith("reuse"):
            continue
        t = studs["tree"]
        preds[name] = gates.tree_masks(t.tree)
        trees[name] = {"leaves": len(t.tree.leaves()),
                       "rules": tree.rules(t.tree),
                       "predicts_over_the_space": {a: m.bit_count()
                                                   for a, m in preds[name].items()}}
    names = sorted(preds)
    pairs = [{"a": a, "b": b, "alike": same_function(preds[a], preds[b])}
             for k, a in enumerate(names) for b in names[k + 1:]]
    return {"trees": trees, "pairs": pairs}, preds


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def check(rows, fitted, record, arrival_rows, arrival_won, reverse_won,
          oncall) -> list[dict[str, Any]]:
    bad = []
    for name, studs in rows.items():
        for n, r in studs.items():
            rec = record["students"][name][n]
            if (r["right"], r["space"]["right"]) != (rec["right"], rec["space"]["right"]):
                bad.append(f"{name} {n}")
    dsl = tree.rules(fitted["rung1/all"]["tree"].tree)
    arr = record["rules_side"]["arrival"]
    derived = {k: oncall["space"][k]["by_queue"] for k in DERIVED if k in oncall["space"]}
    return [
        {"gate": 1, "what": "the refitted students score what score.json says, and "
                            "rung1/all's tree writes its rules",
         "mismatches": bad, "rules_equal": dsl == record["the_tree_in_the_dsl"],
         "passes": not bad and dsl == record["the_tree_in_the_dsl"]},
        {"gate": 2, "what": "arrival and its reverse are the record's",
         "space": [arrival_won.bit_count(), reverse_won.bit_count()],
         "test": [arrival_rows["right"], arrival_rows["reached"]["right"],
                  arrival_rows["not_reached"]["right"]],
         "passes": (arrival_won.bit_count(), reverse_won.bit_count()) == (
             plan.ARRIVAL_SPACE, record["rules_side"]["reversed"]["space"]["right"])
                   and (arrival_rows["right"], arrival_rows["reached"]["right"],
                        arrival_rows["not_reached"]["right"]) == (
             arr["right"], arr["reached"]["right"], arr["not_reached"]["right"])},
        {"gate": 3, "what": "the two leaves' points are what the policy forces, "
                            "derived before the run",
         "measured": derived, "derived": DERIVED,
         "passes": derived == DERIVED
                   and oncall["space"]["both"]["points"] == DERIVED_TOTAL
                   and oncall["space"]["both"]["tree_right"] == DERIVED_RIGHT
                   and oncall["space_oncall_points"] == SPACE_ONCALL},
    ]


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(oncall, reach, preds, space) -> list[dict[str, Any]]:
    t = oncall["test"]["both"]
    s = oncall["space"]["both"]
    tt = reach["train_half"]
    kw = space.mask["has_security_keyword"][True]
    billing = space.mask["product"]["billing"]
    full = space.full
    target = {"SECURITY_INCIDENT": kw,
              "BILLING_SPECIALIST": billing & ~kw & full,
              "T2_TECHNICAL": full & ~kw & ~billing}
    alike = all(same_function(preds[SAME[0]], preds[n]) for n in SAME[1:])
    run1_sec = preds["reuse1/all"].get("SECURITY_INCIDENT", 0)
    t2_t3 = t["by_queue"].get("T2_TECHNICAL", 0) + t["by_queue"].get("T3_ENGINEERING", 0)
    return [
        {"clause": "A1", "reading": t["cases"],
         "holds": A1_RANGE[0] <= t["cases"] <= A1_RANGE[1]},
        {"clause": "A2", "reading": [t2_t3, t["cases"]],
         "holds": t2_t3 * A2_SHARE[1] >= A2_SHARE[0] * t["cases"]},
        {"clause": "A3", "reading": [t["arrival_right"], t["tree_right"]],
         "holds": t["arrival_right"] - t["tree_right"] >= A3_MARGIN},
        {"clause": "A4", "reading": [s["arrival_right"], s["tree_right"]],
         "holds": s["arrival_right"] > s["tree_right"]},
        {"clause": "B1", "reading": [tt["tree"]["reached"]["right"],
                                     FIGURES["tree_all_reached"]],
         "holds": tt["tree"]["reached"]["right"] > FIGURES["tree_all_reached"]},
        {"clause": "B2", "reading": tt["tree"]["reached"]["right"],
         "holds": tt["tree"]["reached"]["right"] > B2_LINE},
        {"clause": "B3", "reading": [tt["cache"]["reached"]["right"],
                                     FIGURES["cache_all_reached"]],
         "holds": tt["cache"]["reached"]["right"] < FIGURES["cache_all_reached"]},
        {"clause": "C1", "reading": alike, "holds": alike},
        {"clause": "C2", "reading": alike and same_function(preds[SAME[0]], target),
         "holds": alike and same_function(preds[SAME[0]], target)},
        {"clause": "C3", "reading": (kw & ~run1_sec).bit_count(),
         "holds": (kw & ~run1_sec) == 0},
    ]


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("students/readings.py writes nothing")
    t0 = time.time()
    record = json.loads(plan.SCORE_PATH.read_text())
    truth = material.truth()
    test = material.split()[1]
    space_cases = list(all_cases())
    points = gates.sample_points()
    reached = set(material.reached(material.answer_set(*REACHED_BY)))
    sets = material.answer_sets()

    print("=" * 78)
    print("PLAN_STUDENTS.md — THE THREE READINGS LEFT OPEN — POST-RUN")
    print("=" * 78)
    rows, fitted = score.read_students(
        sets, lambda s: list(s.labels), truth, test, space_cases, points,
        lambda s: reached if s.run == "rung1" else None)
    base = rules.rung1()
    arrival = score.order_decider(base, base.arrival())
    reverse = score.order_decider(base, base.reversed_arrival())
    arrival_rows = score.on_test(arrival, test, truth, reached)
    sM, sW, sfull = base.space_masks()
    arrival_won = won_mask(base.arrival(), sM, sW, sfull)
    reverse_won = won_mask(base.reversed_arrival(), sM, sW, sfull)
    oncall = oncall_leaves(fitted["rung1/all"]["tree"], test, truth, arrival,
                           reverse, arrival_won, reverse_won)
    checked = check(rows, fitted, record, arrival_rows, arrival_won, reverse_won,
                    oncall)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")

    reach = reach_of_the_train_half(rows, record)
    reuse, preds = reuse_trees(fitted)
    expectation = read_expectation(oncall, reach, preds, rules.space())
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  {e['reading']}")

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, folds=plan.FOLDS,
                            fold_seed=plan.FOLD_SEED),
        "what": "the three readings PLAN_STUDENTS.md left open: what the "
                "ONCALL_ESCALATION leaves cost, the train half on the reach's "
                "partition, and what the PLAN_REUSE.md trees are",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "students": "refitted by students/score.py's read_students"},
        "surface": "corpus test split 0, 995 cases, and the exhaustive space, "
                   "134,400 points; every count against the truth",
        "gates": checked,
        "oncall_leaves": oncall,
        "reach_of_the_train_half": reach,
        "reuse_trees": reuse,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
