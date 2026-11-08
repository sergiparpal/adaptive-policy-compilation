"""
`placement/births.py` — the POST-RUN reading of whether the cut is why the loop's
births are narrow, no figure.

What is pinned, on a list and births built by hand:
- each class a birth falls in: the wrong queue, whole, cut by one listed rule
  with the first match a cut changes and the cutting rule's queue, cut by two,
  and other;
- gate 1 on a row that names another governing rule, gate 2 on counts that
  differ from Stage C's, and gate 3;
- the counts, pooled by arm;
- the expectation's clauses at their edges, and a reading without value;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from blind import rows as brows
from harness.domain import Case
from placement import births as B
from placement import plan
from rung2.engine2 import Space

SPACE = Space()
OC, T1, T2, T3 = "ONCALL_ESCALATION", "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def cond_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def ext(*conds):
    return brows.ext_of({"conditions": list(conds)}, SPACE)


SEV1, ENT = cond_("severity", "eq", 1), cond_("customer_tier", "eq", "enterprise")
API, OFF = cond_("product", "eq", "api"), cond_("off_hours", "eq", True)
REGIONS = {"H04": ext(SEV1, ENT), "H07": ext(SEV1, API), "H08": ext(SEV1),
           "H12": ext(OFF), "H29": ext(cond_("severity", "gte", 1))}
QUEUES = {"H04": OC, "H07": T3, "H08": T2, "H12": T2, "H29": T1}
TRUTH = {OC: REGIONS["H04"], T3: REGIONS["H07"] & ~REGIONS["H04"],
         T2: (REGIONS["H08"] | REGIONS["H12"]) & ~REGIONS["H04"] & ~REGIONS["H07"],
         T1: REGIONS["H29"] & ~REGIONS["H08"] & ~REGIONS["H12"]}
TICKET = Case(has_security_keyword=False, severity=1, customer_tier="enterprise",
              product="api", channel="email", prior_tickets_30d=0, off_hours=True,
              language="en")


def rule_(rid, action, *conds, born=0):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds)}


def read(rule):
    return B.classify(rule, TICKET, SPACE, REGIONS, TRUTH, QUEUES)


class TestTheClasses(unittest.TestCase):

    def test_the_wrong_queue(self):
        got = read(rule_("R1", T2, SEV1, ENT))
        self.assertEqual((got["class"], got["governing"], got["governing_queue"]),
                         ("wrong_queue", "H04", OC))
        self.assertIsNone(got["cut_by_one"])

    def test_whole(self):
        got = read(rule_("R1", OC, SEV1, ENT))
        self.assertEqual(got["class"], "whole")
        self.assertTrue(got["is_the_region"])
        self.assertEqual(got["part_points_held"], got["part_points"])

    def test_cut_by_one_by_the_first_match_a_cut_changes(self):
        got = read(rule_("R1", OC, SEV1, ENT, API))
        self.assertEqual((got["class"], got["cut_by_one"]), ("cut_by_one", ["H07"]))
        self.assertEqual(got["matched"], ["H04", "H07", "H08", "H12", "H29"])
        self.assertEqual(got["first_cutting_match"], "H07")
        self.assertTrue(got["cut_by_the_first_cutting_match"])
        self.assertEqual(got["cutting_queue"], T3)

    def test_cut_by_two(self):
        got = read(rule_("R1", OC, SEV1, ENT, API, OFF))
        self.assertEqual((got["class"], got["cut_by_one"], got["cut_by_two"]),
                         ("cut_by_two", [], [["H07", "H12"]]))
        self.assertFalse(got["cut_by_the_first_cutting_match"])

    def test_other(self):
        got = read(rule_("R1", OC, SEV1, ENT, API, OFF, cond_("language", "eq", "en")))
        self.assertEqual((got["class"], got["cut_by_two"]), ("other", []))
        self.assertTrue(got["covers_its_ticket"])


def birth_(cls, first="H07", by_first=False, cutting=T3, action=OC, region=False):
    return {"class": cls, "first_cutting_match": first, "cut_by_the_first_cutting_match": by_first,
            "cutting_queue": cutting, "action": action, "is_the_region": region}


class TestTheGates(unittest.TestCase):

    def test_gate_1(self):
        b = read(rule_("R1", OC, SEV1, ENT, born=0))
        self.assertTrue(B.governed_as_the_record_says(
            {"records": [{"idx": 0, "truth_rule": "H04"}]}, [b]))
        self.assertFalse(B.governed_as_the_record_says(
            {"records": [{"idx": 0, "truth_rule": "H07"}]}, [b]))

    def test_gate_2(self):
        bs = [birth_("whole", region=True), birth_("cut_by_one")]
        self.assertTrue(B.as_stage_c_counts(bs, {"rules": 2, "the_governing_rules_region": 1}))
        self.assertFalse(B.as_stage_c_counts(bs, {"rules": 2, "the_governing_rules_region": 2}))
        self.assertFalse(B.as_stage_c_counts(bs, {"rules": 3, "the_governing_rules_region": 1}))

    def test_gate_3(self):
        bs = [birth_("whole"), birth_("other")]
        self.assertTrue(B.partition(bs, B.counts(bs)["by_class"]))
        self.assertFalse(B.partition(bs + [birth_("nested")], B.counts(bs)["by_class"]))


class TestTheCounts(unittest.TestCase):

    def test_the_counts(self):
        bs = [birth_("wrong_queue"), birth_("whole"), birth_("cut_by_one", by_first=True),
              birth_("cut_by_one", cutting=OC), birth_("cut_by_two"), birth_("other", first=None)]
        got = B.counts(bs)
        self.assertEqual((got["births"], got["narrow"], got["narrow_where_a_cut_is_possible"]),
                         (6, 4, 3))
        self.assertEqual((got["of_them_cut_by_one"], got["cut_by_one"]), (2, 2))
        self.assertEqual((got["cut_by_the_first_cutting_match"], got["cut_by_another_queue"]),
                         (1, 1))


def runs_(v1b, v1c):
    out = {}
    for arm, bs in (("v1b", v1b), ("v1c", v1c)):
        out[plan.tag(arm, 1)] = bs
        for rep in (2, 3):
            out[plan.tag(arm, rep)] = []
    return out


class TestTheExpectation(unittest.TestCase):

    def holds(self, v1b, v1c):
        return [c["holds"] for c in B.read_expectation(runs_(v1b, v1c))]

    def test_clause_by_clause_at_their_edges(self):
        good = [birth_("cut_by_one", by_first=True)] * 3 + [birth_("other")]
        self.assertEqual(self.holds(good, [birth_("cut_by_one", by_first=True),
                                           birth_("other")]), [True] * 4)
        bad = [birth_("cut_by_one", cutting=OC), birth_("other"), birth_("other")]
        self.assertEqual(self.holds(bad, bad), [False] * 4)

    def test_n2_reads_each_arm(self):
        """Pooled above half, with one arm below it."""
        x = self.holds([birth_("cut_by_one", by_first=True)] * 2,
                       [birth_("cut_by_one", by_first=True), birth_("other"), birth_("other")])
        self.assertEqual(x[:2], [True, False])

    def test_a_reading_without_value_does_not_hold(self):
        self.assertEqual(self.holds([birth_("whole")], [birth_("whole")]), [False] * 4)

    def test_the_lines(self):
        self.assertEqual((B.N_HALF, B.N_MOST), (B.F(1, 2), B.F(3, 4)))
        self.assertEqual(sorted(B.PLANS), ["channel", "placement", "reasoned_loop"])
        self.assertEqual(B.CLASSES, ("wrong_queue", "whole", "cut_by_one", "cut_by_two",
                                     "other"))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read_, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    B.main(argv)
                read_.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
