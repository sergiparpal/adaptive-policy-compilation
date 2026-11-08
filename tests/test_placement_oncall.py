"""
`placement/oncall.py` — the POST-RUN reading of why the runs under run 3's draws
lost `ONCALL_ESCALATION`, no figure.

What is pinned is what this module adds to `channel/oncall.py`'s reading, which
`tests/test_channel_oncall.py` and `tests/test_channel_lost.py` pin:
- this plan's Stage C handed to that reader under the key it reads;
- each draft set against its ticket's part, on a record built by hand: a draft
  that holds its part, a narrower one, one with no condition, and a ticket of
  another queue left out;
- gate 6 on an escalation governed by a rule whose region holds no part;
- the expectation's clauses at their edges, and a reading without value;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from blind import rows as brows
from channel import lost as L
from fidelity.replay import rule_from
from placement import oncall as P
from placement import plan
from rung2.engine2 import PriorityEngine, Space

SPACE = Space()
OC, T2 = "ONCALL_ESCALATION", "T2_TECHNICAL"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


def ext(rule):
    return brows.ext_of(rule, SPACE)


H04 = ext(r_("", 0, OC, severity=1, customer_tier="enterprise"))
H05 = ext(r_("", 0, OC, severity=1, customer_tier="business", off_hours=True))
TRUTH = H04 | H05
REGIONS = {P.H04: H04, P.H05: H05}
PARTS = {P.H04: H04, P.H05: H05}


class TestStageC(unittest.TestCase):

    def test_this_plans_stage_c_under_the_key_the_channel_reader_reads(self):
        runs = {"v1c_r3": {"recall_space": {OC: [420, 6300]}}}
        got = P.stage_c_as_channel({"PL-g": {"runs": runs}, "verdicts": {}})
        self.assertEqual(got, {"CH-g": {"runs": runs}})
        self.assertEqual(got["CH-g"]["runs"]["v1c_r3"]["recall_space"][OC][0], 420)


def esc_(idx, verdict, rule_id=None, left_out=None, **conds):
    payload = {"action": OC,
               "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}
    return {"idx": idx, "verdict": verdict, "rule_id": rule_id, "copy_of": None,
            "listed": ["X"], "calls": [{"round": 0, "payload": payload, "left_out": left_out}]}


class TestTheDrafts(unittest.TestCase):

    def setUp(self):
        self.record = {
            "records": [{"idx": 0, "truth": OC, "truth_rule": P.H04, "cause": "error"},
                        {"idx": 1, "truth": OC, "truth_rule": P.H04, "cause": "error"},
                        {"idx": 2, "truth": OC, "truth_rule": P.H05, "cause": "impasse"},
                        {"idx": 3, "truth": T2, "truth_rule": "H20", "cause": "error"}],
            "escalations": [
                esc_(0, L.BORN, "R1", {"R9": "inside"}, severity=1, customer_tier="enterprise"),
                esc_(1, L.UNPLACED, None, None, severity=1, customer_tier="enterprise",
                     product="api"),
                esc_(2, L.REFUSED),
                esc_(3, L.BORN, "R2", None, severity=2),
            ]}
        self.engine = PriorityEngine(space=SPACE)
        rule = r_("R1", 0, OC, severity=1, customer_tier="enterprise")
        self.engine.add(rule_from(rule), born_at=0, keep_id=True)
        self.ds = P.drafts(self.record, self.engine, SPACE, PARTS, REGIONS, TRUTH)

    def test_only_the_queues_tickets_are_read(self):
        self.assertEqual([d["idx"] for d in self.ds], [0, 1, 2])

    def test_a_draft_that_holds_its_part(self):
        d = self.ds[0]
        self.assertTrue(d["holds_part"])
        self.assertEqual((d["governing"], d["part_points"], d["draft_part_points"]),
                         (P.H04, H04.bit_count(), H04.bit_count()))
        self.assertEqual(d["region_relation"], "equal")
        self.assertEqual(d["born_part_points"], H04.bit_count())
        self.assertEqual(d["left_out"], {"R9": "inside"})

    def test_a_narrower_draft(self):
        d = self.ds[1]
        narrow = ext(r_("", 0, OC, severity=1, customer_tier="enterprise", product="api"))
        self.assertFalse(d["holds_part"])
        self.assertEqual(d["draft_part_points"], narrow.bit_count())
        self.assertLess(d["draft_part_points"], d["part_points"])
        self.assertEqual(d["region_relation"], "contains_draft")
        self.assertIsNone(d["born_part_points"])

    def test_a_draft_with_no_condition(self):
        d = self.ds[2]
        self.assertFalse(d["holds_part"])
        self.assertEqual((d["draft_points"], d["draft_part_points"], d["region_relation"]),
                         (None, None, None))
        self.assertEqual((d["governing"], d["part_points"]), (P.H05, H05.bit_count()))

    def test_gate_6(self):
        self.assertTrue(P.governed_by_a_part(self.ds, PARTS))
        self.record["records"][1]["truth_rule"] = "H01"
        ds = P.drafts(self.record, self.engine, SPACE, PARTS, REGIONS, TRUTH)
        self.assertFalse(P.governed_by_a_part(ds, PARTS))
        self.assertIsNone(ds[1]["part_points"])


def run_(whole=0, h04=(), h05=(), lost=10, unwritten=5, verdicts=(L.BORN,), most=4, n=10):
    return {"drafts": [{"holds_part": i < whole} for i in range(max(len(verdicts), whole))],
            "holding_h04_whole": list(h04), "holding_h05_whole": list(h05),
            "reading": {"queue_points": n, "ways": {"lost": lost, "unwritten": unwritten},
                        "escalations": [{"verdict": v} for v in verdicts],
                        "escalation_verdicts": {}, "curve": {"most_right": most, "at_birth": 1}}}


class TestTheExpectation(unittest.TestCase):

    def holds(self, c, b):
        return [x["holds"] for x in P.read_expectation({"v1c_r3": c, "v1b_r3": b})]

    def test_clause_by_clause_at_their_edges(self):
        self.assertEqual(self.holds(run_(), run_(verdicts=(L.UNPLACED, L.UNPLACED))),
                         [True] * 6)
        self.assertEqual(self.holds(run_(whole=1, h04=("R1",), unwritten=4,
                                         verdicts=(L.BORN, L.UNPLACED), most=5),
                                    run_(verdicts=(L.BORN,))),
                         [False] * 6)

    def test_each_run_of_the_pair_counts(self):
        """A clause read on both runs fails when either run fails it."""
        x = self.holds(run_(), run_(whole=1, h05=("R7",), unwritten=4, verdicts=(L.UNPLACED,),
                                    most=5))
        self.assertEqual(x, [False, False, False, True, True, False])

    def test_a_reading_without_value_does_not_hold(self):
        x = self.holds(run_(lost=0, unwritten=0, verdicts=()), run_(verdicts=()))
        self.assertEqual((x[0], x[2], x[3], x[4]), (False, False, False, False))

    def test_the_lines(self):
        self.assertEqual((P.P_HALF, P.QUEUE, P.RUNS, P.H04, P.H05),
                         (Fraction(1, 2), OC, (("v1c", 3), ("v1b", 3)), "H04", "H05"))


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
                    P.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
