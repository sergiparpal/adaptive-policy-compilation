"""
`channel/oncall.py` — the POST-RUN reading of why c r2 recalled less
`ONCALL_ESCALATION` than its draws allow, no figure.

What is pinned is what this module adds to `channel/lost.py`'s reading, which
`tests/test_channel_lost.py` pins:
- the queue's points split by the two listed regions, and gate 5 on a split that
  overlaps or misses a point;
- each way's points in each part;
- the rules of the queue holding a part whole;
- the expectation's clauses at their edges;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from blind import rows as brows
from channel import lost as L
from channel import oncall as O
from channel import plan
from fidelity.replay import rule_from
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
REGIONS = {O.REACHED: H04, O.UNREACHED: H05}


class TestTheParts(unittest.TestCase):

    def test_the_parts_hold_the_queue_and_do_not_meet(self):
        p = O.parts(TRUTH, REGIONS)
        self.assertEqual((p[O.REACHED], p[O.UNREACHED]), (H04, H05))
        self.assertTrue(O.parts_partition(p, TRUTH))

    def test_gate_5_fails_on_a_split_that_meets_or_misses(self):
        self.assertFalse(O.parts_partition({O.REACHED: TRUTH, O.UNREACHED: H05}, TRUTH))
        self.assertFalse(O.parts_partition({O.REACHED: H04, O.UNREACHED: 0}, TRUTH))

    def test_each_way_in_each_part(self):
        w = {k: 0 for k in O.SPLIT}
        w["right"], w["unwritten"] = H04, H05
        got = O.split(w, O.parts(TRUTH, REGIONS))
        self.assertEqual(got["right"], {O.REACHED: H04.bit_count(), O.UNREACHED: 0})
        self.assertEqual(got["unwritten"], {O.REACHED: 0, O.UNREACHED: H05.bit_count()})
        self.assertEqual(got["conflict"], {O.REACHED: 0, O.UNREACHED: 0})


class TestHoldingWhole(unittest.TestCase):

    def test_the_rules_of_the_queue_that_hold_a_part(self):
        eng = PriorityEngine(space=SPACE)
        for r in (r_("A", 0, OC, severity=1), r_("B", 1, OC, severity=1, product="api"),
                  r_("C", 2, T2, severity=1)):
            eng.add(rule_from(r), born_at=r["born_at"], keep_id=True)
        self.assertEqual(O.holds_whole(eng, OC, H04), ["A"])
        self.assertEqual(O.holds_whole(eng, T2, H04), ["C"])


class TestTheContestedPairs(unittest.TestCase):
    """Added after the first run."""

    def test_a_pair_left_contested_with_its_refused_edge(self):
        q = r_("Q", 0, OC, severity=1, customer_tier="enterprise")
        x = r_("X", 1, T2, severity=1, product="integrations")
        y = r_("Y", 2, T2, severity=1, product="api", customer_tier="enterprise")
        eng = PriorityEngine(space=SPACE)
        for r in (q, x, y):
            eng.add(rule_from(r), born_at=r["born_at"], keep_id=True)
        eng.try_edge("Q", "Y")
        log = [["Q", "Y", "ok"], ["Q", "X", "cierra_ciclo"]]
        w = L.ways(eng, ext(q), OC)
        got = O.contested_pairs(eng, {"edge_log": log}, w, OC)
        self.assertEqual([(p["queue_rule"], p["other_rule"]) for p in got], [("Q", "X")])
        self.assertEqual(got[0]["points"], (ext(q) & ext(x)).bit_count())
        self.assertEqual(got[0]["edges"], [{"winner": "Q", "loser": "X",
                                            "verdict": "cierra_ciclo"}])
        self.assertEqual(got[0]["other_born_at"], 1)


def run_(lost=10, contested=5, holding=("R1",), verdicts=(L.BORN, L.BORN), most=11,
         final=10, right_h05=0):
    by = {k: {O.REACHED: 0, O.UNREACHED: 0} for k in O.SPLIT}
    by["conflict"][O.REACHED] = contested
    by["contested"][O.REACHED] = contested
    by["unwritten"][O.REACHED] = lost - contested
    by["right"][O.UNREACHED] = right_h05
    escs = [{"verdict": v} for v in verdicts]
    return {"by_part": by, "holding_h04_whole": list(holding),
            "reading": {"escalations": escs, "escalation_verdicts": {},
                        "ways": {"right": final},
                        "curve": {"most_right": most, "at_birth": 3}}}


class TestTheExpectation(unittest.TestCase):

    def holds(self, r):
        return [c["holds"] for c in O.read_expectation({"c_r2": r}, "c_r2")]

    def test_clause_by_clause_at_their_edges(self):
        self.assertEqual(self.holds(run_()), [True] * 5)
        self.assertEqual(self.holds(run_(contested=4, holding=(), verdicts=(L.BORN, L.UNPLACED),
                                         most=10, right_h05=1)), [False] * 5)

    def test_a_reading_without_value_does_not_hold(self):
        x = self.holds(run_(lost=0, contested=0, verdicts=()))
        self.assertEqual((x[0], x[2]), (False, False))

    def test_the_lines(self):
        self.assertEqual((O.O_HALF, O.QUEUE, O.RUN, O.REACHED, O.UNREACHED),
                         (Fraction(1, 2), OC, ("c", 2), "H04", "H05"))


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
                    O.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
