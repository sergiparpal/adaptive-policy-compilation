"""
The shadow loop and the metrics it produces.

The figures the four FINDINGS cite are defined here, so what is tested is their
SEMANTICS, not their value:

  * silent error = failures among the cases a rule decided with complete
    confidence. Computed ONLY over ACTION. An impasse is not a silent error:
    the system knows that it does not know.
  * reuse = fraction of rules that got to fire after being born. A firing is a
    case resolved without calling the LLM.
  * the ONLY escalation trigger is the impasse (coverage or conflict), never
    "the answer was incorrect". It is precisely that separation that makes the
    silent error measurable: if the loop escalated on being wrong, it would be
    using the oracle and there would be no silent error to measure.
"""

from __future__ import annotations

import unittest

from harness.domain import Case, generate_corpus
from harness.dsl import RuleEngine
from harness.proposers import ProposalError
from harness.shadow import run_shadow


class ScriptedProposer:
    """Returns whatever it is told to, case by case. No LLM, no heuristic."""

    name = "guionizado"

    def __init__(self, script):
        self.script = list(script)
        self.seen = []

    def propose(self, case, true_action_hint):
        self.seen.append((case, true_action_hint))
        next = self.script.pop(0) if self.script else None
        if isinstance(next, Exception):
            raise next
        if next is None:                      # rule that memorizes the case
            next = {
                "action": true_action_hint,
                "conditions": [{"attr": a, "op": "eq", "value": getattr(case, a)}
                               for a in ("severity", "product")],
            }
        return next["action"], next


def corpus_short(n: int = 40):
    return generate_corpus(n, seed=17)


class TestEscalationTrigger(unittest.TestCase):

    def test_the_first_case_always_escalates(self):
        """Empty base: coverage IMPASSE."""
        res = run_shadow(corpus_short(1), RuleEngine(), ScriptedProposer([]))
        self.assertEqual(res.records[0].outcome, "IMPASSE")
        self.assertTrue(res.records[0].escalated)

    def test_a_wrong_rule_that_matches_does_NOT_escalate(self):
        """This is the definition of silent error: the system decides wrongly
        and carries on unaware. If this escalated, the loop would see the
        oracle."""
        prop = ScriptedProposer([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
        }])
        res = run_shadow(corpus_short(30), RuleEngine(), prop)
        self.assertEqual(sum(1 for r in res.records if r.escalated), 1)
        failures = [r for r in res.records[1:] if r.correct is False]
        self.assertGreater(len(failures), 0)
        self.assertTrue(all(not r.escalated for r in failures))

    def test_conflict_escalates_by_default(self):
        engine = RuleEngine()
        prop = ScriptedProposer([])
        res = run_shadow(corpus_short(60), engine, prop)
        conflicts = [r for r in res.records if r.outcome == "CONFLICT"]
        for r in conflicts:
            self.assertTrue(r.escalated)

    def test_escalate_on_conflict_False_does_not_escalate(self):
        engine = RuleEngine()
        engine.rules = []
        prop = ScriptedProposer([])
        res = run_shadow(corpus_short(60), engine, prop, escalate_on_conflict=False)
        for r in res.records:
            if r.outcome == "CONFLICT":
                self.assertFalse(r.escalated)
                self.assertIsNone(r.predicted)


class TestFaultTolerance(unittest.TestCase):
    """A 2000-case run cannot die at case 1500 over a broken JSON."""

    def test_a_failed_proposal_is_counted_and_the_loop_goes_on(self):
        prop = ScriptedProposer([ProposalError("JSON mal cerrado")])
        res = run_shadow(corpus_short(10), RuleEngine(), prop)
        self.assertEqual(res.failed, 1)
        self.assertEqual(len(res.records), 10)
        self.assertIn("proposal_failed", res.records[0].rejected_reason)

    def test_an_invalid_rule_is_rejected_without_entering_the_base(self):
        prop = ScriptedProposer([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "urgencia", "op": "eq", "value": 9}],
        }])
        engine = RuleEngine()
        res = run_shadow(corpus_short(3), engine, prop)
        self.assertEqual(res.rejected, 1)
        self.assertIsNotNone(res.records[0].rejected_reason)
        # the failed proposal leaves no rule, so case 2 escalates again
        self.assertTrue(res.records[1].escalated)

    def test_the_proposed_action_is_recorded_even_when_the_rule_is_rejected(self):
        """The two error axes are independent: choosing the wrong queue when
        proposing is measured separately from the rule's scope."""
        prop = ScriptedProposer([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "urgencia", "op": "eq", "value": 9}],
        }])
        res = run_shadow(corpus_short(1), RuleEngine(), prop)
        self.assertEqual(res.records[0].predicted, "T1_GENERAL")
        self.assertIsNotNone(res.records[0].proposal_action_correct)


class TestMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res = run_shadow(corpus_short(200), RuleEngine(),
                             ScriptedProposer([]))
        cls.m = cls.res.metrics

    def test_there_is_one_record_per_case(self):
        self.assertEqual(len(self.res.records), 200)
        self.assertEqual(self.m["n_cases"], 200)
        self.assertEqual([r.idx for r in self.res.records], list(range(200)))

    def test_the_silent_error_looks_only_at_covered_cases(self):
        covered = [r for r in self.res.records if r.outcome == "ACTION"]
        hits = sum(1 for r in covered if r.correct)
        self.assertAlmostEqual(self.m["silent_error_rate"],
                               1 - hits / len(covered), places=4)
        self.assertEqual(self.m["silent_errors_abs"], len(covered) - hits)

    def test_coverage_is_the_fraction_of_ACTION(self):
        covered = sum(1 for r in self.res.records if r.outcome == "ACTION")
        self.assertAlmostEqual(self.m["coverage"], covered / 200, places=4)

    def test_reuse_counts_rules_with_at_least_one_firing(self):
        live_ones = sum(1 for r in self.res.rules if r.fire_count >= 1)
        self.assertAlmostEqual(self.m["reuse_rate"],
                               live_ones / len(self.res.rules), places=4)
        self.assertEqual(self.m["dead_rules"],
                         len(self.res.rules) - live_ones)

    def test_one_LLM_call_per_escalation(self):
        self.assertEqual(self.m["llm_calls"], self.m["escalations"])
        self.assertEqual(self.m["escalations"],
                         sum(1 for r in self.res.records if r.escalated))

    def test_per_rule_hits_do_not_exceed_its_firings(self):
        for r in self.res.rules:
            self.assertLessEqual(r.correct_count, r.fire_count)

    def test_the_escalation_curve_has_ten_deciles(self):
        self.assertEqual(len(self.m["escalation_curve_by_decile"]), 10)
        self.assertEqual(self.m["final_decile_escalation_rate"],
                         self.m["escalation_curve_by_decile"][-1])

    def test_compression_is_rules_over_hidden_policy(self):
        self.assertEqual(self.m["hidden_policy_size"], 29)
        self.assertAlmostEqual(self.m["compression_ratio"],
                               round(self.m["n_rules"] / 29, 2), places=2)


class TestTheShadowDoesNotAct(unittest.TestCase):
    """CENTRAL PROPERTY: no rule is ever activated; what WOULD have happened is
    recorded. Since tickets share no state, the shadow is exact and not an
    approximation: the recorded decision does not alter the rest of the corpus.
    """

    def test_the_corpus_does_not_change_when_the_loop_runs(self):
        corpus = corpus_short(50)
        before = [c.key() for c in corpus]
        run_shadow(corpus, RuleEngine(), ScriptedProposer([]))
        self.assertEqual([c.key() for c in corpus], before)

    def test_two_identical_runs_give_the_same(self):
        def run():
            res = run_shadow(corpus_short(80), RuleEngine(),
                             ScriptedProposer([]))
            return [(r.outcome, r.predicted, r.winner_id) for r in res.records]
        self.assertEqual(run(), run())

    def test_the_proposer_is_given_only_the_case_and_the_action(self):
        prop = ScriptedProposer([])
        run_shadow(corpus_short(5), RuleEngine(), prop)
        for case, hint in prop.seen:
            self.assertIsInstance(case, Case)
            self.assertIsInstance(hint, str)


if __name__ == "__main__":
    unittest.main()
