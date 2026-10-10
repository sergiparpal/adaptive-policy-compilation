"""
WHO HAD THE LABELS — the reading and its gates, no figure.

**No figure is pinned here.** They live in `results_ilp/labels.json` and in
§5's erratum of `results_ilp/FINDINGS_ILP.md`. What is pinned is how
`ilp/labels.py` counts, on records small enough to check by hand:

  * a failed proposal and a payload with no queue are wrong over the
    escalations, as the run's own `proposal_action_accuracy` counts them, and
    absent over the proposals that named a queue;
  * a rule is right on its birth when its queue is the truth of the case it was
    born on;
  * a ceiling counts a case once however many rules carrying its queue match
    it, and a rule of another queue supplies nothing;
  * a test case identical to an example counts although it is not one;
  * the module refuses while `PLAN_ILP.md` is unsigned, before it reads a record
    or writes anything, and writes nothing when a gate fails.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from harness.domain import ATTRIBUTES, generate_corpus
from ilp import compare as cmp
from ilp import labels as lb

UNSIGNED = {"passes": False, "found": 1, "unsigned": ["**Signed by Sergi: ___"]}


def rec(idx, truth, escalated=False, predicted=None, correct=None):
    return {"idx": idx, "truth": truth, "escalated": escalated,
            "predicted": predicted, "proposal_action_correct": correct}


def matching(case) -> list[dict]:
    """Conditions that match `case` and every case identical to it."""
    return [{"attr": a, "op": "eq", "value": getattr(case, a)} for a in ATTRIBUTES]


class TestTheProposersTally(unittest.TestCase):

    def setUp(self):
        self.run = {
            "records": [rec(0, "A", True, "A", True),      # right
                        rec(1, "A", True, "B", False),     # wrong
                        rec(2, "B", True, None, None),     # failed
                        rec(3, "B", True, None, False),    # a payload, no queue
                        rec(4, "A")],                      # decided by a rule
            "rules": [{"rule_id": "R1", "born_at": 0, "action": "A"},
                      {"rule_id": "R2", "born_at": 1, "action": "B"}]}
        self.got = lb.proposer_side(self.run)

    def test_failed_and_empty_proposals_are_wrong_over_escalations_only(self):
        g = self.got
        self.assertEqual((g["escalations"], g["failed"], g["no_queue"],
                          g["named_a_queue"], g["right"]), (4, 1, 1, 2, 1))
        self.assertEqual(g["over_escalations"], 1 / 4)
        self.assertEqual(g["over_named"], 1 / 2)

    def test_a_rule_is_right_when_its_queue_is_its_births_truth(self):
        self.assertEqual((self.got["rules"], self.got["rules_right_on_birth"]),
                         (2, 1))

    def test_per_class_says_what_it_named_instead(self):
        pc = self.got["per_class"]
        self.assertEqual(pc["A"], {"escalations": 2, "right": 1,
                                   "named": {"A": 1, "B": 1}})
        self.assertEqual(pc["B"]["named"], {lb.FAILED: 1, lb.NO_QUEUE: 1})


class TestTheCeiling(unittest.TestCase):

    def setUp(self):
        corpus = generate_corpus(40, seed=17)
        first = corpus[0]
        other = next(c for c in corpus if c.key() != first.key())
        self.corpus = [first, other, first]
        self.truth = {0: "X", 1: "X", 2: "Y"}

    def test_a_case_two_rules_match_counts_once(self):
        rules = [{"rule_id": r, "born_at": 1, "action": "X",
                  "conditions": matching(self.corpus[0])} for r in ("R1", "R2")]
        got = lb.ceilings(rules, self.corpus, self.truth, classes=("X",))["X"]
        self.assertEqual((got["corpus_cases"], got["ceiling"]), (2, 1))
        self.assertEqual(got["rules_routing_here"], 2)
        self.assertEqual([s["cases"] for s in got["rules_supplying_it"]], [1, 1])
        self.assertEqual({s["born_on"] for s in got["rules_supplying_it"]}, {"X"})

    def test_a_rule_of_another_queue_supplies_nothing(self):
        rules = [{"rule_id": "R3", "born_at": 2, "action": "Y",
                  "conditions": matching(self.corpus[0])}]
        got = lb.ceilings(rules, self.corpus, self.truth, classes=("X",))["X"]
        self.assertEqual((got["ceiling"], got["rules_routing_here"]), (0, 0))


class TestTheReach(unittest.TestCase):

    def test_an_identical_case_counts_though_it_is_not_an_example(self):
        corpus = generate_corpus(40, seed=17)
        a = corpus[0]
        b = next(c for c in corpus if c.key() != a.key())
        cases = [a, b, a, b]
        escalations = {2: {"proposal_action_correct": True},
                       3: {"proposal_action_correct": False}}
        got = lb.reach(cases, {"train": (0,)}, (2, 3), escalations)
        self.assertEqual(got["train"], {"test_cases_among_its_examples": 0,
                                        "test_cases_identical_to_an_example": 1})
        self.assertEqual(got["escalations_in_the_test_split"],
                         {"n": 2, "proposer_right": 1})


class TestItWritesNothingItShouldNot(unittest.TestCase):

    def test_it_refuses_unsigned_before_reading_or_writing(self):
        with mock.patch.object(cmp, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                lb.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_a_failed_gate_writes_nothing(self):
        failing = [{"gate": 1, "what": "forced", "passes": False}]
        with mock.patch.object(lb, "check", return_value=failing), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                lb.main([])
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
