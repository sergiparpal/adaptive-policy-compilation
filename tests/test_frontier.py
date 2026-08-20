"""
SNAPSHOT of the mock frontier: the dry-run verification of Step 1.

CLAUDE.md publishes these figures as an integrity check: "expected result, exact
(seed 17, n=2000); if it does not match, something got corrupted in copying".
Here they stop depending on somebody reading them in a terminal.

THE WARNING THAT ACCOMPANIES THESE FIGURES, and must not be lost: they are
reproducible but they are NOT a quality reference. All keep_k rules have exactly
k conditions, so their specificity is uniform and arbitration can never invert
them: the mocks are structurally immune to the defect that destroys the real
policy. keep_k(k=4) scores BETTER than the true policy under this engine. The
"region to beat" is above the ceiling of the system.

Source: results/frontier.json, results/FINDINGS.md and Step 1 of CLAUDE.md. This
test calls `run_shadow`, not `cmd_frontier`, so as not to rewrite
results/frontier.json.
"""

from __future__ import annotations

import unittest

from harness.cache_baseline import run_cache_baseline
from harness.dsl import RuleEngine
from harness.proposers import KeepKProposer
from harness.shadow import run_shadow

from .fixtures import corpus

# k -> (rules, reuse, silent error, escalation)
KEEP_K = {
    4: (113, 0.7965, 0.1728, 0.0565),
    5: (304, 0.7237, 0.1568, 0.1520),
    8: (1743, 0.1176, 0.0000, 0.8715),
}

CACHE_D2 = {"n_rules": 211, "silent": 0.4477, "escal": 0.1055, "cov": 0.8945}

# Memorization floor. keep_k(8) keeps all eight attributes: each rule matches a
# single case and is only reused thanks to the corpus's literal duplicates. Any
# reuse close to this is noise, not learning.
MEMORIZATION_FLOOR = 0.1176
UNIQUE_CASES = 1743


def run_keep_k(k: int) -> dict:
    engine = RuleEngine()
    return run_shadow(list(corpus()), engine, KeepKProposer(k)).metrics


class TestKeepKFrontier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.m = {k: run_keep_k(k) for k in KEEP_K}

    def test_published_figures(self):
        for k, (n_rules, reuse, silent, escal) in KEEP_K.items():
            with self.subTest(k=k):
                m = self.m[k]
                self.assertEqual(m["n_rules"], n_rules)
                self.assertAlmostEqual(m["reuse_rate"], reuse, places=4)
                self.assertAlmostEqual(m["silent_error_rate"], silent, places=4)
                self.assertAlmostEqual(m["escalation_rate"], escal, places=4)

    def test_the_mock_gets_the_correct_action_for_free(self):
        """Deliberate: it isolates the GENERALIZATION axis from the ACTING one.
        With the real LLM the second source of error appears, measured
        separately."""
        for k in KEEP_K:
            with self.subTest(k=k):
                self.assertEqual(self.m[k]["proposal_action_accuracy"], 1.0)

    def test_the_mocks_never_enter_conflict(self):
        """All their rules have k conditions: uniform specificity, so the
        tie-break always falls to age. It is the reason these figures do not
        serve as a quality reference."""
        for k in KEEP_K:
            with self.subTest(k=k):
                self.assertEqual(self.m[k]["conflicts"], 0)

    def test_more_conditions_is_less_reuse_and_less_error(self):
        reusos = [self.m[k]["reuse_rate"] for k in sorted(KEEP_K)]
        errors = [self.m[k]["silent_error_rate"] for k in sorted(KEEP_K)]
        self.assertEqual(reusos, sorted(reusos, reverse=True))
        self.assertEqual(errors, sorted(errors, reverse=True))


class TestMemorizationFloor(unittest.TestCase):
    """keep_k(8) induces nothing: it is the case cache under another name."""

    @classmethod
    def setUpClass(cls):
        cls.m = run_keep_k(8)

    def test_one_rule_per_unique_case(self):
        self.assertEqual(self.m["n_rules"], UNIQUE_CASES)
        self.assertEqual(len({c.key() for c in corpus()}), UNIQUE_CASES)

    def test_memorizing_produces_no_silent_error(self):
        self.assertEqual(self.m["silent_error_rate"], 0.0)

    def test_the_floor_is_pure_effect_of_the_duplicates(self):
        self.assertAlmostEqual(self.m["reuse_rate"], MEMORIZATION_FLOOR, places=4)
        # coverage of keep_k(8) = duplicate rate of the corpus
        self.assertAlmostEqual(self.m["coverage"], 1 - UNIQUE_CASES / 2000, places=4)


class TestCacheBaseline(unittest.TestCase):
    """The project's null hypothesis: no rules, nearest neighbour."""

    @classmethod
    def setUpClass(cls):
        cls.m = run_cache_baseline(list(corpus()), max_dist=2)

    def test_published_figures(self):
        self.assertEqual(self.m["n_rules"], CACHE_D2["n_rules"])
        self.assertAlmostEqual(self.m["silent_error_rate"], CACHE_D2["silent"], places=4)
        self.assertAlmostEqual(self.m["escalation_rate"], CACHE_D2["escal"], places=4)
        self.assertAlmostEqual(self.m["coverage"], CACHE_D2["cov"], places=4)

    def test_covers_slightly_less_than_keep_k4_and_errs_far_more(self):
        """It is the comparison that justifies rules existing at all: at similar
        coverage (0.894 versus 0.944), the cache fails on 45% of what it covers
        and keep_k(4) on 17%. Two and a half times more silent error."""
        keep4 = run_keep_k(4)
        self.assertLess(abs(self.m["coverage"] - keep4["coverage"]), 0.06)
        self.assertGreater(self.m["silent_error_rate"],
                           2.5 * keep4["silent_error_rate"])

    def test_d0_is_exact_memorization(self):
        m0 = run_cache_baseline(list(corpus()), max_dist=0)
        self.assertEqual(m0["silent_error_rate"], 0.0)
        self.assertEqual(m0["n_rules"], UNIQUE_CASES)


if __name__ == "__main__":
    unittest.main()
