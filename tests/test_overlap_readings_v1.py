"""
WHAT V1'S OVERLAP IS MADE OF — the reading and its gates, no figure.

**No figure is pinned here.** They live in `results_overlap/readings_v1.json` and
in `results_overlap/FINDINGS_OVERLAP.md`. What is pinned is what this module adds
to `overlap/readings.py`'s reading, which `tests/test_overlap_readings.py` pins:

  * each birth carries what it was born on, read off the loop's record of the
    case that bore it;
  * the expectation is read clause by clause;
  * the module refuses while `PLAN_OVERLAP.md` is unsigned, before it reads a
    record or writes anything.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from overlap import plan
from overlap import readings_v1 as v1
from rung2.engine2 import Space

X, Y = "QUEUE_X", "QUEUE_Y"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


class TestWhatEachRuleWasBornOn(unittest.TestCase):

    def test_it_reads_the_record_of_the_case_that_bore_it(self):
        record = {"rules": [r_("A", 0, X, product="billing"),
                            r_("B", 2, Y, customer_tier="free")],
                  "records": [{"idx": 0, "outcome": "IMPASSE"},
                              {"idx": 1, "outcome": "ACTION"},
                              {"idx": 2, "outcome": "CONFLICT"}]}
        got = v1.read_run(record, Space())
        self.assertEqual([b["born_on"] for b in got["births"]], ["IMPASSE", "CONFLICT"])
        self.assertEqual(got["on_conflict"], {"births": 1, "with_o": 1})


class TestTheExpectation(unittest.TestCase):

    def run_(self, births, with_o, without, top):
        return {"on_conflict": {"births": births, "with_o": with_o},
                "o_a_without_top": without, "top": top}

    def test_clause_by_clause(self):
        key = {"rule_id": "K", "action": v1.SECURITY,
               "conditions": [[v1.KEYWORD, "eq", True]]}
        runs = {1: self.run_(3, 3, 0.40, key), 2: self.run_(1, 1, 0.70, key),
                3: self.run_(2, 2, 0.50, key)}
        got = {e["clause"]: e["holds"] for e in v1.read_expectation(runs)}
        self.assertEqual(got, {"by construction": True, 2: True, 3: True})
        other = {"rule_id": "T", "action": X, "conditions": [["product", "eq", "api"]]}
        runs = {1: self.run_(3, 2, 0.51, key), 2: self.run_(1, 1, 0.70, other),
                3: self.run_(2, 2, 0.60, key)}
        got = {e["clause"]: e["holds"] for e in v1.read_expectation(runs)}
        self.assertEqual(got, {"by construction": False, 2: False, 3: False})


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(v1.gates, "load",
                               side_effect=AssertionError("read")) as load, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                v1.main([])
        load.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
