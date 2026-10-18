"""
`students/readings.py` — how it counts, and no figure.

WHAT IS PINNED HERE.
  * The derivation its docstring writes before the run: the two
    `ONCALL_ESCALATION` leaves' points by true queue, recomputed by brute force
    over the space from the hidden policy and the leaves' conditions as
    `score.json` records them. A derivation is not a bet, and this is what
    keeps it honest.
  * The mask arithmetic: the points an order gets right, a mask by true queue,
    and two predictions deciding alike.
  * Each clause of the expectation at its edge, on readings built by hand.
  * The writer refusing while the plan is unsigned, before it reads or fits
    anything.

**No test here refits a student on the proposer's answers or reads any figure
of the reading.**
"""

from __future__ import annotations

import random
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.dsl import Condition
from harness.hidden_policy import true_action
from rung2.engine2 import Space
from rung3.local_search import score_order

from students import plan, readings

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

# The two leaves as `score.json`'s `the_tree_in_the_dsl` records them.
L015 = [Condition("severity", "eq", 1), Condition("product", "neq", "billing")]
L024 = [Condition("has_security_keyword", "eq", False), Condition("severity", "eq", 1),
        Condition("product", "eq", "billing"), Condition("off_hours", "eq", True)]


class TestTheDerivationIsWhatThePolicyForces(unittest.TestCase):

    def test_by_brute_force(self):
        counts = {"L015": {}, "L024": {}}
        oncall = 0
        for case in all_cases():
            truth = true_action(case)
            oncall += truth == "ONCALL_ESCALATION"
            for name, conds in (("L015", L015), ("L024", L024)):
                if all(c.holds(case) for c in conds):
                    counts[name][truth] = counts[name].get(truth, 0) + 1
        self.assertEqual(counts, readings.DERIVED)
        self.assertEqual(oncall, readings.SPACE_ONCALL)

    def test_the_totals_add_up(self):
        total = sum(sum(v.values()) for v in readings.DERIVED.values())
        right = sum(v.get("ONCALL_ESCALATION", 0) for v in readings.DERIVED.values())
        self.assertEqual((total, right), (readings.DERIVED_TOTAL, readings.DERIVED_RIGHT))


class TestTheMaskArithmetic(unittest.TestCase):

    def test_won_mask_counts_what_score_order_counts(self):
        rng = random.Random(7)
        n, ids = 200, [f"R{k:03d}" for k in range(30)]
        full = (1 << n) - 1
        for _ in range(20):
            M = {r: rng.getrandbits(n) & rng.getrandbits(n) for r in ids}
            W = {r: M[r] & rng.getrandbits(n) for r in ids}
            order = ids[:]
            rng.shuffle(order)
            self.assertEqual(readings.won_mask(order, M, W, full).bit_count(),
                             score_order(order, M, W, full))

    def test_by_queue_and_same_function(self):
        truth = {"T1_GENERAL": 0b0011, "T2_TECHNICAL": 0b1100}
        self.assertEqual(readings.by_queue(0b0110, truth),
                         {"T1_GENERAL": 1, "T2_TECHNICAL": 1})
        self.assertTrue(readings.same_function({"A": 3, "B": 0}, {"A": 3}))
        self.assertFalse(readings.same_function({"A": 3}, {"A": 2, "B": 1}))


def built(cases=41, t2t3=28, arrival=13, tree_right=3, s_arrival=5881,
          train_reached=162, cache_reached=153):
    oncall = {"test": {"both": {"cases": cases, "tree_right": tree_right,
                                "arrival_right": arrival,
                                "by_queue": {"T2_TECHNICAL": t2t3, "T3_ENGINEERING": 0}}},
              "space": {"both": {"arrival_right": s_arrival,
                                 "tree_right": readings.DERIVED_RIGHT}}}
    reach = {"train_half": {"tree": {"reached": {"right": train_reached}},
                            "cache": {"reached": {"right": cache_reached}}}}
    return oncall, reach


class TestTheExpectationAtItsEdges(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sp = Space()
        cls.space = sp
        kw = sp.mask["has_security_keyword"][True]
        billing = sp.mask["product"]["billing"]
        f = {"SECURITY_INCIDENT": kw, "BILLING_SPECIALIST": billing & ~kw & sp.full,
             "T2_TECHNICAL": sp.full & ~kw & ~billing}
        cls.preds = {n: dict(f) for n in readings.SAME} | {"reuse1/all": dict(f)}

    def clauses(self, **kw):
        oncall, reach = built(**kw)
        return {e["clause"]: e["holds"] for e in readings.read_expectation(
            oncall, reach, self.preds, self.space)}

    def test_inside(self):
        self.assertTrue(all(self.clauses().values()))

    def test_each_edge(self):
        self.assertFalse(self.clauses(cases=51, t2t3=40)["A1"])
        self.assertTrue(self.clauses(cases=30, t2t3=20)["A1"])
        self.assertFalse(self.clauses(cases=30, t2t3=19)["A2"])
        self.assertFalse(self.clauses(arrival=12)["A3"])
        self.assertFalse(self.clauses(s_arrival=readings.DERIVED_RIGHT)["A4"])
        self.assertFalse(self.clauses(train_reached=146)["B1"])
        self.assertFalse(self.clauses(train_reached=161)["B2"])
        self.assertFalse(self.clauses(cache_reached=154)["B3"])

    def test_the_trees(self):
        preds = dict(self.preds)
        preds["reuse3/train"] = {"T2_TECHNICAL": self.space.full}
        oncall, reach = built()
        got = {e["clause"]: e["holds"] for e in readings.read_expectation(
            oncall, reach, preds, self.space)}
        self.assertFalse(got["C1"])
        self.assertFalse(got["C2"])
        preds = dict(self.preds)
        preds["reuse1/all"] = {"T2_TECHNICAL": self.space.full}
        got = {e["clause"]: e["holds"] for e in readings.read_expectation(
            oncall, reach, preds, self.space)}
        self.assertFalse(got["C3"])
        self.assertTrue(got["C1"])


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_anything(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch("students.score.read_students",
                        side_effect=AssertionError("fitted")) as fit, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                readings.main([])
        fit.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
