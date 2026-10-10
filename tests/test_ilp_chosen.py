"""
THE INDUCER ON THE QUEUES THE PROPOSER CHOSE — the reading and its gates, no
figure.

**No figure is pinned here.** They live in `results_ilp/chosen.json` and in
`results_ilp/FINDINGS_ILP.md`. What is pinned is how `ilp/chosen.py` builds and
reads, on cases small enough to check by hand:

  * a training example is an escalation whose proposal named a queue — not one
    that failed, not a payload with no queue, not a case a rule decided — and
    its label is that queue;
  * the masks it trains on are `instances.masks`', labelled by whatever it is
    handed;
  * the expectation is read clause by clause;
  * the space splits by the security keyword's condition and its complement,
    and accuracy and each half's majority queue are read within the half —
    added after the first run;
  * the module refuses while `PLAN_ILP.md` is unsigned, before it reads a record
    or writes anything, and writes nothing when a gate fails.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from ilp import chosen as ch
from ilp import compare as cmp
from ilp import induce as ind

UNSIGNED = {"passes": False, "found": 1, "unsigned": ["**Signed by Sergi: ___"]}


def rec(idx, escalated, predicted, correct):
    return {"idx": idx, "escalated": escalated, "predicted": predicted,
            "proposal_action_correct": correct, "truth": "T"}


class TestTheTrainingSet(unittest.TestCase):

    def test_only_escalations_that_named_a_queue_and_with_that_queue(self):
        records = [rec(0, True, "A", True),        # named, right
                   rec(1, True, "B", False),       # named, wrong
                   rec(2, True, None, None),       # the proposal failed
                   rec(3, True, None, False),      # a payload with no queue
                   rec(4, False, "C", None)]       # a rule decided it
        self.assertEqual(ch.chosen(records), {0: "A", 1: "B"})

    def test_the_masks_carry_the_labels_they_are_handed(self):
        ext, lab, n = ch.instance_of((0, 1, 2), {0: "A", 1: "B", 2: "A"})
        self.assertEqual(n, 3)
        self.assertEqual(lab, {"A": 0b101, "B": 0b010})
        self.assertEqual(len(ext), len(ch.inst.masks([], [])[0]))


class TestTheSpaceByTheKeyword(unittest.TestCase):
    """Added after the first run."""

    def test_the_halves_are_the_keywords_condition_and_its_complement(self):
        k = ch.language().index(ch.KEYWORD)
        ext = [0] * len(ch.language())
        ext[k] = 0b0101
        halves = ch.keyword_halves((ext, {}, 4))
        self.assertEqual(halves, {"keyword": 0b0101, "no_keyword": 0b1010})

    def test_accuracy_and_majority_are_read_within_each_half(self):
        halves = {"keyword": 0b0011, "no_keyword": 0b1100}
        self.assertEqual(ch.by_half(0b0111, halves), {"keyword": 1.0, "no_keyword": 0.5})
        truth = {"S": 0b0111, "T": 0b1000}
        got = ch.majority(truth, halves)
        self.assertEqual(got["keyword"], {"points": 2, "most_common_queue": "S",
                                          "share": 1.0})
        self.assertEqual(got["no_keyword"]["points"], 2)
        self.assertEqual(got["no_keyword"]["share"], 0.5)


class TestTheExpectation(unittest.TestCase):

    REFS = {"test_cases": 995, "order": {"test_correct": 843},
            "born_at": {"test": 519 / 995},
            "handed_the_truth": {"train_316|40": {"test_correct": 772},
                                 "train_316|120": {"test_correct": 759}}}

    def lists(self, small, big, am):
        out = {}
        for b in ind.BEAM_WIDTHS:
            for s, c in (("chosen_316", small), ("chosen_632", big)):
                out[f"{s}|{b}"] = {"test": {"correct": c, "per_class": {
                    "ACCOUNT_MANAGER": {"accuracy": am}}}}
        return out

    def holds(self, small, big, am):
        return {e["clause"]: e["holds"]
                for e in ch.read_expectation(self.lists(small, big, am), self.REFS)}

    def test_clause_by_clause(self):
        self.assertEqual(self.holds(600, 600, 0.2), {1: True, 2: True, 3: True, 4: True})
        self.assertEqual(self.holds(850, 780, 0.4), {1: False, 2: False, 3: True, 4: False})
        self.assertEqual(self.holds(500, 500, 0.2), {1: True, 2: True, 3: False, 4: True})

    def test_the_edges(self):
        """Below the order is at most 842; above born_at is at least 520; the
        ceiling itself counts as at or below it."""
        self.assertTrue(self.holds(842, 520, cmp.I_B_CEILING["ACCOUNT_MANAGER"])[1])
        self.assertFalse(self.holds(843, 520, 0.2)[1])
        self.assertTrue(self.holds(600, 520, 0.2)[3])
        self.assertFalse(self.holds(600, 519, 0.2)[3])
        self.assertTrue(self.holds(600, 600, cmp.I_B_CEILING["ACCOUNT_MANAGER"])[4])


class TestItWritesNothingItShouldNot(unittest.TestCase):

    def test_it_refuses_unsigned_before_reading_or_writing(self):
        with mock.patch.object(cmp, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                ch.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_a_failed_gate_writes_nothing(self):
        failing = [{"gate": 1, "what": "forced", "passes": False}]
        with mock.patch.object(ch, "compute", return_value={}), \
             mock.patch.object(ch, "check", return_value=failing), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                ch.main([])
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
