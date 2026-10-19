"""
`spotcheck/readings.py`, the POST-RUN reading of which tickets teach
`T3_ENGINEERING`.

WHAT IS PINNED HERE, AND WHY.
  * First match, the rules' right counts and the key rule by hand, the earlier
    rule winning a tie, and the move to the front.
  * The two routes of gate 2 agreeing on a real order that needs no search,
    arrival order.
  * Each clause of the expectation at its edge, on readings built by hand.
  * The writer refusing unsigned before it searches anything.

**No figure of the reading is pinned here**, and no test searches an order.
"""

from __future__ import annotations

import unittest
from unittest import mock

from escalations import instrument as I
from rung3.local_search import build_masks, score_order
from spotcheck import plan, readings as R

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


class TestTheOrderReadByHand(unittest.TestCase):

    matched = {1: ["a", "b"], 2: ["b"], 3: ["c", "a"], 4: [], 5: ["b", "c"]}
    truth = {1: "X", 2: "Y", 3: "X", 4: "X", 5: "X"}
    action = {"a": "X", "b": "Y", "c": "X"}

    def test_first_match_wins(self):
        fm = R.first_match(["b", "a", "c"], self.matched, [1, 2, 3, 4, 5])
        self.assertEqual(fm, {1: "b", 2: "b", 3: "a", 4: None, 5: "b"})

    def test_right_by_rule(self):
        got = R.right_by_rule(["a", "c", "b"], self.matched, self.truth, self.action,
                              [1, 2, 3, 4, 5])
        self.assertEqual(got, {"a": 2, "b": 1, "c": 1})

    def test_the_key_rule_and_its_tie(self):
        # a decides 1 and 3, c decides 5: a is the key rule
        self.assertEqual(R.key_rule(["a", "c", "b"], self.matched, self.truth,
                                    self.action, [1, 3, 5]), "a")
        # c decides 3 and 5, a decides 1: c
        self.assertEqual(R.key_rule(["c", "a", "b"], self.matched, self.truth,
                                    self.action, [1, 3, 5]), "c")
        # one case each: the earlier in the order wins the tie
        self.assertEqual(R.key_rule(["c", "a"], {1: ["a"], 5: ["c"]}, self.truth,
                                    self.action, [1, 5]), "c")

    def test_moved_to_front(self):
        self.assertEqual(R.moved_to_front(["x", "y", "z"], "z"), ["z", "x", "y"])
        self.assertEqual(R.moved_to_front(["x", "y", "z"], "x"), ["x", "y", "z"])


class TestTheTwoRoutesAgreeOnArrivalOrder(unittest.TestCase):

    def test_first_match_and_masks_count_alike(self):
        inst = I.instance()
        arrival = sorted(inst["ids"], key=lambda r: (inst["born"][r], r))
        cases = R.t3_cases(inst)
        self.assertEqual(len(cases), plan.RARE_OF["T3_ENGINEERING"])
        by_rank = sum(R.right_by_rule(arrival, inst["matched"], inst["truth"],
                                      inst["action"], cases).values())
        masks = build_masks(inst["ids"], inst["matched"], inst["truth"],
                            inst["action"], cases)
        self.assertEqual(by_rank, score_order(arrival, *masks))


def reading(t3, key, test=800, moved_t3=15, moved_test=810, lost=None, labels=()):
    return {"test": test, "t3_right": t3, "t3_right_by_masks": t3,
            "key_decides": key, "key_rank": 0, "deciding_rules": {},
            "key_matched_t3": 15, "key_matched_lost_to": lost or {},
            "moved": {"test": moved_test, "t3_right": moved_t3,
                      "t3_right_by_masks": moved_t3},
            "labelled_t3": [{"case": i, "key_matches": k, "right": k}
                            for i, k in enumerate(labels)]}


def readings(**over):
    base = {
        "full": reading(18, 15, labels=(True, False)),
        "escalations": reading(0, 0, test=814, moved_test=820,
                               lost={"T2_TECHNICAL": 12, "T1_GENERAL": 3},
                               labels=(False, False, False)),
        "audit|10|4": reading(13, 13, labels=(True,)),
        "audit|50|1": reading(1, 0, moved_test=805,
                              lost={"T2_TECHNICAL": 10, "BILLING_SPECIALIST": 2},
                              labels=(False, False, False)),
    }
    base.update(over)
    return {e["clause"]: e for e in R.read_expectation(base)}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_holds_on_the_drafted_world(self):
        got = readings()
        self.assertEqual({k: v["holds"] for k, v in got.items()},
                         {f"E{i}": True for i in range(1, 9)})

    def test_e1_at_its_line(self):
        self.assertFalse(readings(full=reading(18, 12, labels=(True,)))["E1"]["holds"])
        self.assertTrue(readings(full=reading(18, 13, labels=(True,)))["E1"]["holds"])

    def test_e3_needs_none_decided_and_two_thirds_to_t2(self):
        self.assertFalse(readings(**{"audit|50|1": reading(
            2, 1, lost={"T2_TECHNICAL": 9}, labels=(False,))})["E3"]["holds"])
        # 12 + 8 of 30 lost go to T2: two thirds exactly holds
        self.assertTrue(readings(**{
            "escalations": reading(0, 0, test=814, moved_test=820,
                                   lost={"T2_TECHNICAL": 12, "T1_GENERAL": 3},
                                   labels=(False, False, False)),
            "audit|50|1": reading(1, 0, moved_test=805,
                                  lost={"T2_TECHNICAL": 8, "T1_GENERAL": 7},
                                  labels=(False,))})["E3"]["holds"])
        self.assertFalse(readings(**{
            "audit|50|1": reading(1, 0, moved_test=805,
                                  lost={"T2_TECHNICAL": 7, "T1_GENERAL": 8},
                                  labels=(False,))})["E3"]["holds"])

    def test_e4_and_e5(self):
        self.assertFalse(readings(**{"audit|10|4": reading(
            13, 13, moved_t3=12, labels=(True,))})["E4"]["holds"])
        self.assertFalse(readings(**{"audit|50|1": reading(
            1, 0, test=805, moved_test=805, lost={"T2_TECHNICAL": 3},
            labels=(False,))})["E5"]["holds"])

    def test_e6_and_e7(self):
        self.assertFalse(readings(escalations=reading(
            0, 0, test=814, moved_test=820, lost={"T2_TECHNICAL": 3},
            labels=(False, True, False)))["E6"]["holds"])
        self.assertFalse(readings(**{"audit|10|4": reading(
            13, 13, labels=(False,))})["E6"]["holds"])
        self.assertFalse(readings(**{"audit|50|1": reading(
            1, 0, moved_test=805, lost={"T2_TECHNICAL": 3},
            labels=(True, False))})["E7"]["holds"])

    def test_e8_both_halves(self):
        # an order with no key-matched label that learns breaks the first half
        self.assertFalse(readings(**{"mix|50|0": reading(
            19, 15, labels=(False,))})["E8"]["holds"])
        # 4 of the 5 orders holding one learn: holds; 2 of 4 does not
        four = {f"mix|{k}|0": reading(15, 14, labels=(True,)) for k in (50, 100)}
        self.assertTrue(readings(**four, **{"mix|251|0": reading(1, 0, labels=(True,))})
                        ["E8"]["holds"])
        self.assertFalse(readings(**{"mix|50|0": reading(1, 0, labels=(True,)),
                                     "mix|100|0": reading(1, 0, labels=(True,))})
                         ["E8"]["holds"])


class TestNothingIsSearchedUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_searching(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(I, "labelled_order",
                               side_effect=AssertionError("searched")) as search:
            with self.assertRaises(SystemExit):
                R.main([])
        search.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(R.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
