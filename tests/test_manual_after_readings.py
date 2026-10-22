"""
`manual/after_readings.py`, the POST-RUN reading written after
`results_manual/readings.json`: its A on `K-a`'s own surface, and what its B and C
showed beside their clauses.

WHAT IS PINNED HERE, AND WHY.
  * The names it reads by: the keyword's three hidden rules, the bands, and its
    record's path.
  * A hidden rule cut to the half without the keyword, and a birth classed
    there, on masks built by hand: a rule that reaches the keyword's half can
    lie inside a lower rule's region only once both are cut.
  * A band at its cut, and a level split by any partition when three runs share
    rule ids, which a split keyed by rule id alone gets wrong.
  * The mix split over any partition's keys giving back `manual/readings.py`'s
    over the classes.
  * A condition that admits only tickets without the keyword, and the class's
    arrivals counted by rule, outcome and rightness.
  * The writer refusing unsigned before it reads a record, and an argument
    printing the docstring.

**No figure of the reading is pinned here**, and no test reads a loop record.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from manual import after_readings as AR
from manual import plan
from manual import readings as R

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
OUT = 0b11110000           # bits 4 to 7 carry no keyword


class TestTheNames(unittest.TestCase):

    def test_the_names_it_reads_by(self):
        self.assertEqual(AR.KEYWORD_RULES, ("H01", "H02", "H03"))
        self.assertEqual(AR.BANDS, ("b1", "b2", "b3", "b4"))
        self.assertEqual(AR.record_path(), Path("results_manual/after_readings.json"))
        self.assertEqual(AR.KW, "has_security_keyword")


class TestOffTheKeyword(unittest.TestCase):

    def test_a_rule_reaching_the_keyword_is_inside_a_region_only_once_cut(self):
        H = {"ext": 0b11111111, "region": 0b00110000, "queue": "A"}
        E = 0b00010001                 # one point off the keyword, one on it
        self.assertEqual(R.classify(E, H), "rule")
        self.assertEqual(R.classify(E & OUT, AR.off_keyword(H, OUT)), "region")
        self.assertEqual(AR.off_keyword(H, OUT), {"ext": 0b11110000, "region": 0b00110000})

    def test_classes_off_by_rule(self):
        hidden = {"H": {"ext": 0b11111111, "region": 0b00110000, "queue": "A"}}
        births = [{"rule_id": "r1", "ticket_rule": "H"},
                  {"rule_id": "r2", "ticket_rule": "H"}]
        ext = {"r1": 0b00010001, "r2": 0b01000001}
        self.assertEqual(AR.classes_off(births, ext, hidden, OUT),
                         {"r1": "region", "r2": "rule"})


class TestBandsAndSplits(unittest.TestCase):

    def test_a_band_at_its_cut(self):
        cuts = [240.0, 840.0, 1680.0]
        self.assertEqual([AR.band(p, cuts) for p in (1, 240, 241, 840, 1680, 1681)],
                         ["b1", "b1", "b2", "b2", "b3", "b4"])

    def test_the_quartiles_are_statistics(self):
        self.assertEqual(AR.edges_of([1, 2, 3, 4, 5, 6, 7, 8]), [2.25, 4.5, 6.75])

    def test_runs_that_share_rule_ids_are_split_by_birth(self):
        run1 = [{"rule_id": "R0001", "crosses": False}, {"rule_id": "R0002", "crosses": True}]
        run2 = [{"rule_id": "R0001", "crosses": True}]
        items = [(run1[0], "x"), (run1[1], "y"), (run2[0], "y")]
        s = AR.split(items, ("x", "y"))
        self.assertEqual(s["parts"], {"x": {"births": 1, "cross": 0},
                                      "y": {"births": 2, "cross": 2}})
        self.assertEqual((s["births"], s["alone"], s["k_a"]), (3, 1, Fraction(1, 3)))
        self.assertEqual(s["part_share"]["y"], Fraction(2, 3))

    def test_the_mix_split_gives_back_the_readings_over_the_classes(self):
        def pair(region, rule, beyond):
            classes = {c: {"births": b, "cross": x}
                       for c, (b, x) in zip(R.CLASSES, (region, rule, beyond))}
            n = sum(b for b, _ in (region, rule, beyond))
            alone = n - sum(x for _, x in (region, rule, beyond))
            return ({"k_a": Fraction(alone, n), "classes": classes},
                    {"k_a": Fraction(alone, n), "parts": classes})
        (lo_r, lo_a), (hi_r, hi_a) = pair((2, 1), (2, 2), (1, 1)), pair((6, 1), (2, 1), (1, 0))
        self.assertEqual(AR.mix_split(lo_a, hi_a, R.CLASSES), R.mix_split(lo_r, hi_r))


class TestTheKeyword(unittest.TestCase):

    def test_conditions_that_admit_only_false(self):
        yes = [{"attr": AR.KW, "op": "eq", "value": False},
               {"attr": AR.KW, "op": "neq", "value": True},
               {"attr": AR.KW, "op": "in", "value": [False]}]
        no = [{"attr": AR.KW, "op": "eq", "value": True},
              {"attr": AR.KW, "op": "in", "value": [False, True]},
              {"attr": "off_hours", "op": "eq", "value": False}]
        self.assertTrue(all(AR.admits_only_false(c) for c in yes))
        self.assertFalse(any(AR.admits_only_false(c) for c in no))
        self.assertTrue(AR.excludes_keyword({"conditions": no + yes[:1]}))
        self.assertFalse(AR.excludes_keyword({"conditions": no}))

    def test_the_class_arrivals_by_rule_outcome_and_rightness(self):
        rec = {"records": [
            {"truth": R.SI, "truth_rule": "H01", "outcome": "CONFLICT", "correct": True},
            {"truth": R.SI, "truth_rule": "H02", "outcome": "ACTION", "correct": False},
            {"truth": R.SI, "truth_rule": "H02", "outcome": "ACTION", "correct": False},
            {"truth": "T1_GENERAL", "truth_rule": "H29", "outcome": "ACTION", "correct": True}]}
        self.assertEqual(AR.class_arrivals(rec), {"H01|CONFLICT|right": 1,
                                                  "H02|ACTION|wrong": 2})


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_reading_a_record(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(R, "load_runs",
                               side_effect=AssertionError("read")) as read:
            with self.assertRaises(SystemExit):
                AR.main([])
        read.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(AR.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
