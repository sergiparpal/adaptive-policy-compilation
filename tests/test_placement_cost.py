"""
`placement/cost.py` — the POST-RUN reading of what the cuts cost, no figure.

What is pinned, on a list, a base and records built by hand:
- the listed rules' governed regions partitioning the space, and gate 2 on a
  split that misses a point;
- the points a base decides right, a conflict left out;
- a draft classed as a birth is, born or not, and one naming no rule;
- each class a governing rule falls in, and their precedence;
- a run read whole, with each rule's lost points;
- gate 1 against Stage C's fraction, and gate 3 on a row naming another rule;
- the totals by class and the lost points by queue;
- the expectation's clauses at their edges, and a reading without value;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from blind import rows as brows
from fidelity.replay import rule_from
from harness.domain import Case
from placement import cost as C
from placement import plan
from rung2.engine2 import PriorityEngine, Space

SPACE = Space()
OC, T1, T2, T3 = "ONCALL_ESCALATION", "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def cond_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def ext(*conds):
    return brows.ext_of({"conditions": list(conds)}, SPACE)


SEV1, ENT, API = cond_("severity", "eq", 1), cond_("customer_tier", "eq", "enterprise"), \
    cond_("product", "eq", "api")
REGIONS = {"H04": ext(SEV1, ENT), "H07": ext(SEV1, API), "H08": ext(SEV1),
           "H29": ext(cond_("severity", "gte", 1))}
QUEUES = {"H04": OC, "H07": T3, "H08": T2, "H29": T1}
MASKS = C.governed_masks(REGIONS)
TRUTH = {QUEUES[g]: m for g, m in MASKS.items()}
TICKET = Case(has_security_keyword=False, severity=1, customer_tier="enterprise",
              product="api", channel="email", prior_tickets_30d=0, off_hours=False,
              language="en")


def esc_(idx, verdict, action, *conds):
    return {"idx": idx, "verdict": verdict,
            "calls": [{"round": 0, "payload": {"action": action, "conditions": list(conds)}}]}


class TestTheSpace(unittest.TestCase):

    def test_the_governed_regions_partition_the_space(self):
        self.assertEqual(MASKS["H04"], REGIONS["H04"])
        self.assertEqual(MASKS["H07"], REGIONS["H07"] & ~REGIONS["H04"])
        self.assertTrue(C.partitions(MASKS, SPACE.full))
        self.assertFalse(C.partitions({k: v for k, v in MASKS.items() if k != "H29"},
                                      SPACE.full))

    def test_the_points_a_base_decides_right(self):
        eng = PriorityEngine(space=SPACE)
        for rid, born, action, conds in (("R1", 0, OC, [SEV1, ENT]), ("R2", 1, T3, [SEV1, API])):
            eng.add(rule_from({"rule_id": rid, "born_at": born, "action": action,
                               "conditions": conds}), born_at=born, keep_id=True)
        contested = REGIONS["H04"] & REGIONS["H07"]
        expected = (REGIONS["H04"] & ~contested) | (TRUTH[T3] & REGIONS["H07"] & ~contested)
        self.assertEqual(C.right_mask(eng, TRUTH), expected)


class TestTheDrafts(unittest.TestCase):

    def cls(self, esc):
        return C.draft_class(esc, TICKET, SPACE, REGIONS, TRUTH, QUEUES)

    def test_a_draft_classed_as_a_birth(self):
        whole = self.cls(esc_(0, C.L.BORN, OC, SEV1, ENT))
        self.assertEqual((whole["class"], whole["born"], whole["governing"]),
                         ("whole", True, "H04"))
        cut = self.cls(esc_(0, C.L.UNPLACED, OC, SEV1, ENT, API))
        self.assertEqual((cut["class"], cut["born"]), ("cut_by_one", False))
        self.assertEqual(self.cls(esc_(0, C.L.BORN, T2, SEV1, ENT))["class"], "wrong_queue")

    def test_a_draft_naming_no_rule(self):
        self.assertEqual(self.cls({"idx": 0, "verdict": C.L.REFUSED,
                                   "calls": [{"payload": None}]})["class"], "no_rule")
        self.assertEqual(self.cls(esc_(0, C.L.REFUSED, OC))["class"], "no_rule")

    def test_each_class_of_a_governing_rule(self):
        d = lambda cls, born=False: {"class": cls, "born": born}  # noqa: E731
        self.assertEqual(C.rule_class([]), "no_escalation")
        self.assertEqual(C.rule_class([d("cut_by_one"), d("whole", True)]), "whole_born")
        self.assertEqual(C.rule_class([d("cut_by_one"), d("whole")]), "whole_not_born")
        self.assertEqual(C.rule_class([d("cut_by_one", True), d("cut_by_two")]), "cuts_only")
        self.assertEqual(C.rule_class([d("cut_by_one"), d("other")]), "narrow_other")
        self.assertEqual(C.rule_class([d("wrong_queue", True), d("no_rule")]), "no_right_draft")
        self.assertEqual(C.rule_class([d("wrong_queue", True), d("cut_by_one")]), "cuts_only")


class TestARun(unittest.TestCase):

    def test_a_run_read_whole_and_its_gates(self):
        eng = PriorityEngine(space=SPACE)
        eng.add(rule_from({"rule_id": "R1", "born_at": 0, "action": OC,
                           "conditions": [SEV1, ENT, API]}), born_at=0, keep_id=True)
        record = {"escalations": [esc_(0, C.L.BORN, OC, SEV1, ENT, API)],
                  "records": [{"idx": 0, "truth_rule": "H04"}]}
        with mock.patch.object(C.MI, "final_engine", return_value=eng):
            got = C.read_run(record, SPACE, REGIONS, MASKS, TRUTH, QUEUES, (TICKET,))
        h04 = got["rules"]["H04"]
        cut = REGIONS["H04"] & REGIONS["H07"]
        self.assertEqual((h04["class"], h04["points"], h04["lost"]),
                         ("cuts_only", REGIONS["H04"].bit_count(),
                          (REGIONS["H04"] & ~cut).bit_count()))
        self.assertEqual(got["rules"]["H08"]["class"], "no_escalation")
        self.assertEqual(got["right"], cut.bit_count())
        self.assertTrue(C.as_stage_c(got, str(Fraction(cut.bit_count(), C.POINTS))))
        self.assertFalse(C.as_stage_c(got, "1/2"))
        self.assertTrue(C.governed_as_the_record_says(record, got))
        record["records"][0]["truth_rule"] = "H07"
        self.assertFalse(C.governed_as_the_record_says(record, got))


def rule_(cls, points, lost, queue=T2):
    return {"class": cls, "points": points, "lost": lost, "queue": queue}


def runs_(v1c_rules, v1b_rules):
    out = {}
    for arm, rules in (("v1c", v1c_rules), ("v1b", v1b_rules)):
        out[plan.tag(arm, 1)] = {"rules": rules}
        for rep in (2, 3):
            out[plan.tag(arm, rep)] = {"rules": {}}
    return out


class TestTheTotals(unittest.TestCase):

    def test_by_class_and_by_queue(self):
        runs = {"a": {"rules": {"H04": rule_("cuts_only", 10, 6, OC),
                                "H08": rule_("whole_born", 20, 1)}},
                "b": {"rules": {"H08": rule_("cuts_only", 20, 4)}}}
        got = C.totals(runs, ["a", "b"])
        self.assertEqual((got["cuts_only"]["lost"], got["cuts_only"]["points"],
                          got["cuts_only"]["rules"]), (10, 30, 2))
        self.assertEqual(got["lost"], 11)
        self.assertEqual(C.totals(runs, ["a", "b"], ("H04",))["lost"], 5)
        self.assertEqual(C.by_queue(runs, ["a", "b"]),
                         {OC: {"cuts_only": 6}, T2: {"cuts_only": 4, "whole_born": 1}})


class TestTheExpectation(unittest.TestCase):

    def holds(self, v1c, v1b):
        return [c["holds"] for c in C.read_expectation(runs_(v1c, v1b))]

    def test_clause_by_clause_at_their_edges(self):
        v1c = {"H04": rule_("cuts_only", 100, 90, OC), "H08": rule_("cuts_only", 100, 20),
               "H10": rule_("whole_born", 100, 10), "H12": rule_("no_escalation", 50, 2),
               "H14": rule_("whole_not_born", 10, 1)}
        v1b = {"H14": rule_("whole_not_born", 10, 2)}
        self.assertEqual(self.holds(v1c, v1b), [True] * 4)
        v1c_bad = {"H08": rule_("cuts_only", 100, 19), "H10": rule_("whole_born", 100, 11),
                   "H12": rule_("no_escalation", 50, 20), "H14": rule_("whole_not_born", 10, 2)}
        self.assertEqual(self.holds(v1c_bad, v1b), [False] * 4)

    def test_k1_leaves_the_rarest_queue_out(self):
        v1c = {"H04": rule_("cuts_only", 100, 90, OC), "H05": rule_("cuts_only", 50, 40, OC),
               "H08": rule_("cuts_only", 10, 1), "H12": rule_("no_escalation", 50, 2)}
        self.assertFalse(self.holds(v1c, {})[0])

    def test_a_reading_without_value_does_not_hold(self):
        self.assertEqual(self.holds({}, {}), [False] * 4)

    def test_the_lines(self):
        self.assertEqual((C.K_HALF, C.K_TENTH, C.K_FIFTH), (Fraction(1, 2), Fraction(1, 10),
                                                           Fraction(1, 5)))
        self.assertEqual((C.RARE_RULES, C.POINTS), (("H04", "H05"), 134_400))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    C.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
