"""
WHAT SEPARATES A RUN THAT OVERLAPS — the reading and its gates, no figure.

**No figure is pinned here.** They live in `results_overlap/readings.json` and in
`results_overlap/FINDINGS_OVERLAP.md`. What is pinned is what makes the reading
the one the module's docstring describes:

  * the births are replayed in order, each with its `O` of another queue and its
    `S` of its own, as §5.2 of the plan computes them;
  * the top rule is the one in the most `O`s, the first born among equals, and
    `O-a` without it still counts it as a birth;
  * the expectation is read clause by clause;
  * the module refuses while `PLAN_OVERLAP.md` is unsigned, before it reads a
    record or writes anything.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from overlap import plan
from overlap import readings as rd
from rung2.engine2 import Space

X, Y = "QUEUE_X", "QUEUE_Y"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


class TestTheReplay(unittest.TestCase):

    def setUp(self):
        # B is broad and of another queue: C and D meet it; D also meets C, its own.
        self.rules = [r_("A", 0, X, product="billing"),
                      r_("B", 3, Y, customer_tier="free"),
                      r_("C", 7, X, product="api"),
                      r_("D", 9, X, channel="email")]
        self.births = rd.replay(self.rules, Space())

    def test_o_and_s_against_the_rules_born_before(self):
        got = {b["rule_id"]: (b["O"], b["S"]) for b in self.births}
        self.assertEqual(got, {"A": ([], []), "B": (["A"], []), "C": (["B"], []),
                               "D": (["B"], ["A", "C"])})

    def test_the_top_rule_and_o_a_without_it(self):
        top = rd.top_rule(self.births)
        self.assertEqual((top["rule_id"], top["in_o_of"], top["births_with_o"]),
                         ("B", 2, 3))
        self.assertEqual(rd.o_a_without(self.births, None), 0.25)
        self.assertEqual(rd.o_a_without(self.births, "B"), 0.75)

    def test_ties_go_to_the_first_born(self):
        births = [{"rule_id": "P", "born_at": 0, "O": [], "action": X, "conditions": [],
                   "share": 0.5},
                  {"rule_id": "Q", "born_at": 1, "O": [], "action": Y, "conditions": [],
                   "share": 0.5},
                  {"rule_id": "R", "born_at": 2, "O": ["P", "Q"], "action": X,
                   "conditions": [], "share": 0.1}]
        self.assertEqual(rd.top_rule(births)["rule_id"], "P")
        self.assertIsNone(rd.top_rule(births[:2]))


class TestTheExpectation(unittest.TestCase):

    def run_(self, top_in, with_o, without, median, attrs, n):
        births = [{"rule_id": str(i)} for i in range(n)]
        return {"births": births, "top": {"in_o_of": top_in, "births_with_o": with_o},
                "o_a_without_top": without, "breadth": {"median_share": median},
                "attributes": attrs}

    def test_clause_by_clause(self):
        runs = {1: self.run_(5, 10, 0.51, 0.1, {"product": 2}, 4),
                2: self.run_(1, 2, 0.9, 0.2, {"product": 3}, 4),
                3: self.run_(0, 0, 1.0, 0.3, {"tier": 3}, 4)}
        got = {e["clause"]: e["holds"] for e in rd.read_expectation(runs)}
        self.assertEqual(got, {1: True, 2: True, 3: True, 4: True})
        runs[1] = self.run_(4, 10, 0.50, 0.4, {"product": 2}, 4)
        runs[2] = self.run_(1, 2, 0.9, 0.2, {"product": 2}, 4)
        got = {e["clause"]: e["holds"] for e in rd.read_expectation(runs)}
        self.assertEqual(got, {1: False, 2: False, 3: False, 4: False})


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(rd.gates, "load",
                               side_effect=AssertionError("read")) as load, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                rd.main([])
        load.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
