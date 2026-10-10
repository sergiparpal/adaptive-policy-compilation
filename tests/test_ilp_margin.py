"""
WHERE THE +0.0342 COMES FROM — the reading and its gates, no figure.

**No figure is pinned here.** They live in `results_ilp/margin.json` and in
`results_ilp/FINDINGS_ILP.md`. What is pinned is how `ilp/margin.py` counts, on
cases small enough to check by hand:

  * an order's cases right are `score_order`'s, kept as a mask, and a decision
    list's are `induce.score`'s;
  * the order replayed case by case is the masks, bit for bit — gate 5, added
    after the first run;
  * the partition counts a test case identical to an example, and marks apart
    the ones that are examples;
  * the margin is split part by part and adds up to the total, and the
    agreement tells a tie of cases from a tie of counts — added after the first
    run;
  * the expectation is read clause by clause;
  * the module refuses while `PLAN_ILP.md` is unsigned, before it reads a record
    or writes anything, and writes nothing when a gate fails.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from harness.domain import generate_corpus
from ilp import compare as cmp
from ilp import induce as ind
from ilp import margin as mg
from rung3.local_search import build_masks, score_order

UNSIGNED = {"passes": False, "found": 1, "unsigned": ["**Signed by Sergi: ___"]}


class TestTheMasks(unittest.TestCase):

    def test_an_orders_cases_right_are_the_ones_score_order_counts(self):
        # four cases; A matches 0 and 1 and is right on 0; B matches 1, 2, 3
        # and is right on 1 and 3; C matches 2 and is right on it
        M = {"A": 0b0011, "B": 0b1110, "C": 0b0100}
        W = {"A": 0b0001, "B": 0b1010, "C": 0b0100}
        for order in (["A", "B", "C"], ["C", "B", "A"], ["B", "A", "C"]):
            with self.subTest(order=order):
                won = mg.won_by_order(order, M, W, 0b1111)
                self.assertEqual(won.bit_count(), score_order(order, M, W, 0b1111))
        self.assertEqual(mg.won_by_order(["A", "B", "C"], M, W, 0b1111), 0b1001)

    def test_the_replay_case_by_case_is_the_masks(self):
        """Gate 5, added after the first run: the same pool read two ways."""
        pool = {0: ["A"], 1: ["A", "B"], 2: ["B", "C"], 3: ["B"], 4: []}
        action = {"A": "x", "B": "y", "C": "z"}
        truth = {0: "x", 1: "y", 2: "z", 3: "y", 4: "x"}
        idxs = [0, 1, 2, 3, 4]
        M, W, full = build_masks(["A", "B", "C"], pool, truth, action, idxs)
        for order in (["A", "B", "C"], ["C", "B", "A"], ["B", "A", "C"]):
            with self.subTest(order=order):
                self.assertEqual(mg.replay_order(order, pool, action, truth, idxs),
                                 mg.won_by_order(order, M, W, full))

    def test_a_lists_cases_right_are_the_ones_score_counts(self):
        ext = [0b011, 0b110]                      # two conditions, three cases
        truth = {"X": 0b001, "Y": 0b110}
        lst = ind.Induced(rules=[((0,), "X"), ((1,), "Y")])
        won = mg.won_by_list(lst, ext, truth, 3)
        self.assertEqual(won, 0b101)              # case 1 goes to X, wrongly
        self.assertEqual(won.bit_count(), ind.score(lst, ext, truth, 3)["correct"])


class TestThePartition(unittest.TestCase):

    def test_an_identical_case_is_reached_and_not_an_example(self):
        corpus = generate_corpus(40, seed=17)
        a = corpus[0]
        b = next(c for c in corpus if c.key() != a.key())
        cases = [a, b, a, a, b]
        reached, own = mg.partition(cases, examples=(0, 2), test=(2, 3, 4))
        self.assertEqual(reached, 0b011)          # positions of cases 2 and 3
        self.assertEqual(own, 0b001)              # only case 2 is an example


class TestTheMargin(unittest.TestCase):

    def test_it_splits_by_part_and_adds_up(self):
        a = {"reached": 10, "not_reached": 20, "total": 30}
        b = {"reached": 5, "not_reached": 22, "total": 27}
        m = mg.margin(a, b, 100)
        self.assertEqual([m[p]["cases"] for p in ("reached", "not_reached", "total")],
                         [5, -2, 3])
        self.assertEqual(m["reached"]["cases"] + m["not_reached"]["cases"],
                         m["total"]["cases"])
        self.assertEqual(m["total"]["points"], 0.03)
        self.assertEqual(m["share_from_reached"], 5 / 3)

    def test_parts_count_inside_the_test_split_only(self):
        self.assertEqual(mg.parts(0b1_0110, reached=0b0011, full=0b1111),
                         {"reached": 1, "not_reached": 1, "total": 2})

    def test_agreement_tells_a_tie_of_cases_from_a_tie_of_counts(self):
        """Added after the first run. Two masks right on two cases each, on
        different cases: the counts tie, the cases do not."""
        got = mg.agreement(0b0110, 0b0011, part=0b1111)
        self.assertEqual(got, {"both": 1, "only_the_list": 1, "only_the_order": 1,
                               "neither": 1})
        self.assertEqual(mg.agreement(0b0110, 0b0011, part=0b0001)["only_the_order"], 1)
        self.assertEqual(mg.agreement(0b0110, 0b0011, part=0b0001)["both"], 0)


class TestTheExpectation(unittest.TestCase):

    def readings(self, list_reached, order_reached, rest_margin):
        beams = [str(b) for b in ind.BEAM_WIDTHS]
        return {"parts": {"reached": 371, "not_reached": 624},
                "order": {"reached": order_reached, "not_reached": 843 - order_reached},
                "lists": {f"train_632|{b}": {"reached": list_reached} for b in beams},
                "margins": {b: {"not_reached": {"cases": rest_margin}} for b in beams}}

    def test_clause_by_clause(self):
        got = {e["clause"]: e["holds"]
               for e in mg.read_expectation(self.readings(371, 300, -37))}
        self.assertEqual(got, {"by construction": True, 2: True, 3: True})
        got = {e["clause"]: e["holds"]
               for e in mg.read_expectation(self.readings(370, 340, 3))}
        self.assertEqual(got, {"by construction": False, 2: False, 3: False})

    def test_clause_3_is_stricter_than_clause_2(self):
        """At 330 of the 371 the 624 still carry no margin, and the order is
        nonetheless right on a larger share of the 371 than of the 624."""
        got = {e["clause"]: e["holds"]
               for e in mg.read_expectation(self.readings(371, 330, -7))}
        self.assertEqual((got[2], got[3]), (True, False))


class TestItWritesNothingItShouldNot(unittest.TestCase):

    def test_it_refuses_unsigned_before_reading_or_writing(self):
        with mock.patch.object(cmp, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                mg.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_a_failed_gate_writes_nothing(self):
        failing = [{"gate": 1, "what": "forced", "passes": False}]
        with mock.patch.object(mg, "compute", return_value={}), \
             mock.patch.object(mg, "check", return_value=failing), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                mg.main([])
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
