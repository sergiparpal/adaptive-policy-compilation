"""
THE CENTRAL INVARIANT: the transcription of the hidden policy into the DSL is
faithful.

The claim rung 1 closes on depends on this: "the DSL is not the culprit; it is
an execution failure, not a representation failure". If the transcription were
not faithful, the 0.5875 ceiling would not measure the arbitration but a copying
error, and the whole rung would change meaning.

The check is EXHAUSTIVE over the 134,400 combinations of the space, not over the
corpus: a rule can be equivalent on the 2000 sampled cases and not in the space.
It costs ~1.5 s and is the most expensive test in the suite.

It is the same check `verify_encoding()` performs in
`harness/ceiling_check.py`, rewritten here so that a failure says WHICH rule and
in WHICH case, instead of printing a count.
"""

from __future__ import annotations

import unittest

from harness.ceiling_check import HIDDEN_DSL, all_cases, build_rules
from harness.hidden_policy import HIDDEN_POLICY_SIZE, HIDDEN_RULES, true_action

from .fixtures import SPACE_SIZE, corpus, space


class TestExhaustiveSpace(unittest.TestCase):

    def test_all_cases_walks_the_whole_space_without_repeats(self):
        cases = list(all_cases())
        self.assertEqual(len(cases), SPACE_SIZE)
        self.assertEqual(len({c.key() for c in cases}), SPACE_SIZE)

    def test_the_corpus_is_a_subset_of_the_space(self):
        universe = {c.key() for c in all_cases()}
        self.assertTrue({c.key() for c in corpus()} <= universe)


class TestTranscription(unittest.TestCase):
    """The 29 DSL rules against the 29 original predicates."""

    @classmethod
    def setUpClass(cls):
        cls.rules = build_rules()
        cls.cases = list(all_cases())

    def test_same_identifiers_in_the_same_order(self):
        self.assertEqual([r[0] for r in HIDDEN_DSL],
                         [h[0] for h in HIDDEN_RULES])

    def test_same_actions(self):
        self.assertEqual([r[2] for r in HIDDEN_DSL],
                         [h[2] for h in HIDDEN_RULES])

    def test_there_are_29(self):
        self.assertEqual(len(self.rules), HIDDEN_POLICY_SIZE)
        self.assertEqual(HIDDEN_POLICY_SIZE, 29)

    def test_each_DSL_rule_is_equivalent_to_its_lambda(self):
        """Over the 134,400 combinations, not over the corpus."""
        failures = {}
        for case in self.cases:
            for rule, (hid, pred, _act) in zip(self.rules, HIDDEN_RULES):
                if rule.matches(case) != bool(pred(case)):
                    failures.setdefault(hid, case)
        self.assertEqual(failures, {}, msg="\n".join(
            f"  {hid}: discrepa ya en {c}" for hid, c in failures.items()))

    def test_first_match_reproduces_true_action(self):
        for case in self.cases:
            for rule in self.rules:
                if rule.matches(case):
                    if rule.action != true_action(case):
                        self.fail(f"{rule.rule_id} da {rule.action} y la verdad "
                                  f"es {true_action(case)} en {case}")
                    break
            else:
                self.fail(f"ninguna regla DSL casa {case}: falta el catch-all")

    def test_H29_is_the_catch_all_of_the_whole_space(self):
        """`lambda c: True` is encoded as `severity gte 1` because the validator
        requires at least one condition. It must cover the WHOLE space."""
        h29 = self.rules[-1]
        self.assertEqual(h29.rule_id, "H29")
        self.assertEqual(space().extension(h29.conditions), space().full)

    def test_true_action_is_defined_over_the_whole_space(self):
        for case in self.cases:
            self.assertIn(true_action(case), {a for _h, _p, a in HIDDEN_RULES})


if __name__ == "__main__":
    unittest.main()
