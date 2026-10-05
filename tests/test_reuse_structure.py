"""
THE THREE BASES, READ FOR STAGE E — the readings and the gates, no figure.

**No figure is pinned here.** They live in `results_reuse/structure.json` and in
`results_reuse/FINDINGS_REUSE.md`. What is pinned is what makes each reading the
one its reference publishes:

  * the pair census counts overlap, nesting and the population the way
    `learned_population` draws it;
  * subsumption decides a case when the minimal matching rules agree, on the
    corpus case by case and over the space by masks, and the two agree;
  * the copies are `rung3/identical_rules.py`'s two definitions;
  * the expectation is read clause by clause against lines taken from the two
    references;
  * the module refuses while `PLAN_REUSE.md` is unsigned, before it measures or
    writes anything.
"""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

from reuse import plan
from reuse import structure as st
from rung3.order_search import subsumption_below

X, Y = "QUEUE_X", "QUEUE_Y"


def rules_of(ext):
    return [{"rule_id": r} for r in ext]


class TestThePairCensus(unittest.TestCase):

    def test_overlap_nesting_and_the_population(self):
        # A is inside B; C overlaps B without nesting; D touches nothing.
        ext = {"A": 0b0011, "B": 0b0111, "C": 0b1100, "D": 0}
        action = {"A": X, "B": Y, "C": X, "D": Y}
        below = subsumption_below(rules_of(ext), ext)
        got = st.pair_census(list(ext), ext, below, action)
        self.assertEqual((got["possible"], got["overlapping"], got["nested"],
                          got["population"]), (6, 2, 1, 1))
        self.assertEqual(got["overlap_degree"], {"mean": 1.0, "max": 2})

    def test_equal_extensions_are_not_nested_and_count_when_queues_differ(self):
        ext = {"A": 0b0110, "B": 0b0110}
        below = subsumption_below(rules_of(ext), ext)
        got = st.pair_census(list(ext), ext, below, {"A": X, "B": Y})
        self.assertEqual((got["nested"], got["population"]), (0, 1))


class TestSubsumptionTheArbiter(unittest.TestCase):

    def test_on_the_corpus(self):
        matched = [[], ["A"], ["A", "B"], ["B", "C"], ["A", "C"]]
        undef = [[], ["A"], ["A"], ["B", "C"], ["A", "C"]]
        truth = [X, X, Y, X, X]
        action = {"A": X, "B": Y, "C": X}
        got = st.subsumption_on_corpus(matched, undef, truth, action)
        self.assertEqual((got["action"], got["conflict"], got["impasse"],
                          got["correct"]), (3, 1, 1, 2))
        self.assertEqual((got["coverage"], got["silent_error"], got["e2e"]),
                         (3 / 5, 1 / 3, 2 / 5))

    def test_over_the_space_agrees_with_the_corpus_reading(self):
        # Five points: one with no rule, two decided right, one decided wrong,
        # one where two queues remain.
        undefeated = {"A": 0b00110, "C": 0b10000, "B": 0b11000}
        action = {"A": X, "B": Y, "C": X}
        tmask = {X: 0b00010, Y: 0b01100}
        got = st.subsumption_on_space(undefeated, action, tmask, 5)
        self.assertEqual((got["action"], got["conflict"], got["impasse"],
                          got["correct"]), (3, 1, 1, 2))

    def test_nothing_decided_has_no_silent_error(self):
        self.assertIsNone(st.arbitration(Counter(conflict=2), 0, 2)["silent_error"])


class TestTheCopies(unittest.TestCase):

    def test_both_definitions(self):
        rules = [
            {"rule_id": "R1", "conditions": [{"attr": "a", "op": "eq", "value": 1},
                                             {"attr": "b", "op": "eq", "value": 2}]},
            {"rule_id": "R2", "conditions": [{"attr": "b", "op": "eq", "value": 2},
                                             {"attr": "a", "op": "eq", "value": 1}]},
            {"rule_id": "R3", "conditions": [{"attr": "a", "op": "lte", "value": 1}]},
        ]
        ext = {"R1": 0b01, "R2": 0b01, "R3": 0b01}
        got = st.copies(rules, ext, {"R1": X, "R2": Y, "R3": X}, listed=True)
        self.assertEqual(got["written"]["pairs"], {"same_queue": 0, "different_queue": 1})
        self.assertEqual(got["written"]["different_queue_pairs"], [["R1", "R2"]])
        self.assertEqual(got["covering"]["pairs"], {"same_queue": 1, "different_queue": 2})
        self.assertNotIn("different_queue_pairs",
                         st.copies(rules, ext, {"R1": X, "R2": Y, "R3": X},
                                   listed=False)["written"])


class TestTheExpectation(unittest.TestCase):

    def profile(self, nested, coverage, silent, copies, gap):
        return {"pairs": {"nested_share": nested},
                "subsumption": {"corpus": {"coverage": coverage, "silent_error": silent}},
                "copies": {"written": {"pairs": {"same_queue": copies,
                                                 "different_queue": 0}}},
                "bounds": {"gap": {"corpus": gap}}}

    def profiles(self, base):
        return {"hand_written": self.profile(0.15, 0.6, 0.0, 0, 0.0),
                "rung1": self.profile(0.05, 0.08, 0.5, 748, 0.047),
                **{name: base for name in st.BASES}}

    def test_every_clause_on_every_base(self):
        read = st.read_expectation(self.profiles(self.profile(0.02, 0.9, 0.4, 0, 0.01)))
        self.assertEqual(len(read), 5 * len(st.BASES))
        self.assertTrue(all(r["holds"] for r in read))
        self.assertEqual({r["clause"]: r["line"] for r in read},
                         {"1": 0.15, "2": 0.08, "3": 0.25, "4": 0, "5": 0.047})

    def test_each_clause_can_fail(self):
        read = st.read_expectation(self.profiles(self.profile(0.2, 0.05, 0.2, 1, 0.05)))
        self.assertFalse(any(r["holds"] for r in read))

    def test_an_unreadable_reading_is_not_a_verdict(self):
        read = st.read_expectation(self.profiles(self.profile(0.02, 0.0, None, 0, 0.0)))
        self.assertTrue(all(r["holds"] is None for r in read if r["clause"] == "3"))


class TestTheGates(unittest.TestCase):

    def test_a_row_passes_only_on_equality(self):
        self.assertTrue(st.row("x", [1, 2], [1, 2], "o")["passes"])
        self.assertFalse(st.row("x", [1, 2], [1, 3], "o")["passes"])

    def test_the_hand_written_policy_is_transcribed_whole(self):
        rules = st.hand_written()
        self.assertEqual(len(rules), 29)
        self.assertEqual([r["born_at"] for r in rules], list(range(29)))


class TestNothingIsMeasuredOrWrittenUnsigned(unittest.TestCase):

    def test_it_refuses_before_measuring(self):
        unsigned = {"passes": False, "found": 2, "unsigned": 1}
        with mock.patch.object(plan, "gate_signature", return_value=unsigned), \
             mock.patch.object(st, "measure",
                               side_effect=AssertionError("measured")) as measured, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                st.main([])
        measured.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
