"""
The corpus and the case space.

The determinism of the corpus is what makes runs comparable (hard rule 4 of
CLAUDE.md): same n, same seed, same 2000 cases in the same order. If this
breaks, no figure in the repository can be compared with any other again.
"""

from __future__ import annotations

import unittest
from collections import Counter

from harness.domain import (ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case,
                            generate_corpus)
from harness.hidden_policy import true_action

from .fixtures import CORPUS_N, CORPUS_SEED, SPACE_SIZE, corpus

# Statistics of the canonical corpus. Published in the header of
# results/FINDINGS.md and in Step 1 of CLAUDE.md.
UNIQUE_CASES = 1743
DUPLICATE_RATE = 0.1285

# Distribution of the true class. The last two are the critical, rare classes
# the aggregate hides: 20 and 7 cases out of 2000.
ACTION_DISTRIBUTION = {
    "T2_TECHNICAL": 726,
    "SELF_SERVICE_DEFLECT": 495,
    "BILLING_SPECIALIST": 271,
    "T1_GENERAL": 255,
    "T3_ENGINEERING": 117,
    "ACCOUNT_MANAGER": 109,
    "SECURITY_INCIDENT": 20,
    "ONCALL_ESCALATION": 7,
}


class TestCaseSpace(unittest.TestCase):

    def test_the_product_of_the_domains_is_134400(self):
        n = 1
        for attr in ATTRIBUTES:
            n *= len(DOMAINS[attr])
        self.assertEqual(n, SPACE_SIZE)

    def test_every_attribute_has_a_declared_domain(self):
        self.assertEqual(set(ATTRIBUTES), set(DOMAINS))

    def test_the_numeric_ones_are_the_two_declared(self):
        self.assertEqual(NUMERIC_ATTRS, {"severity", "prior_tickets_30d"})
        for attr in NUMERIC_ATTRS:
            for v in DOMAINS[attr]:
                self.assertIsInstance(v, int)
                self.assertNotIsInstance(v, bool)

    def test_there_are_eight_actions_without_repeats(self):
        self.assertEqual(len(ACTIONS), 8)
        self.assertEqual(len(set(ACTIONS)), 8)


class TestCanonicalCorpus(unittest.TestCase):

    def test_size_and_uniques(self):
        c = corpus()
        self.assertEqual(len(c), CORPUS_N)
        self.assertEqual(len({x.key() for x in c}), UNIQUE_CASES)

    def test_duplicate_rate(self):
        c = corpus()
        rate = 1 - len({x.key() for x in c}) / len(c)
        self.assertAlmostEqual(rate, DUPLICATE_RATE, places=4)

    def test_is_reproducible(self):
        a = generate_corpus(CORPUS_N, seed=CORPUS_SEED)
        b = generate_corpus(CORPUS_N, seed=CORPUS_SEED)
        self.assertEqual(a, b)
        self.assertEqual(tuple(a), corpus())

    def test_a_prefix_of_larger_n_is_the_corpus_of_smaller_n(self):
        """Case i does not depend on how many are requested: --n 100 is a prefix
        of --n 2000. Hence the smoke test and the full run see the same cases
        (what is NOT deterministic is the proposer; see CLAUDE.md, Step 3)."""
        self.assertEqual(generate_corpus(100, seed=CORPUS_SEED),
                         list(corpus()[:100]))

    def test_another_seed_gives_another_corpus(self):
        self.assertNotEqual(generate_corpus(CORPUS_N, seed=18), list(corpus()))

    def test_every_value_falls_in_its_domain(self):
        for case in corpus():
            for attr in ATTRIBUTES:
                self.assertIn(getattr(case, attr), DOMAINS[attr],
                              msg=f"{attr} fuera de dominio en {case}")

    def test_true_class_distribution(self):
        got = Counter(true_action(c) for c in corpus())
        self.assertEqual(dict(got.most_common()), ACTION_DISTRIBUTION)
        self.assertEqual(sum(ACTION_DISTRIBUTION.values()), CORPUS_N)

    def test_the_eight_classes_appear(self):
        self.assertEqual(set(ACTION_DISTRIBUTION), set(ACTIONS))

    def test_majority_class_baseline(self):
        top = max(ACTION_DISTRIBUTION.values())
        self.assertAlmostEqual(top / CORPUS_N, 0.363, places=3)


class TestCase(unittest.TestCase):

    def test_key_follows_the_order_of_ATTRIBUTES(self):
        c = corpus()[0]
        self.assertEqual(c.key(), tuple(getattr(c, a) for a in ATTRIBUTES))

    def test_as_dict_carries_the_eight_attributes(self):
        self.assertEqual(set(corpus()[0].as_dict()), set(ATTRIBUTES))

    def test_is_immutable_and_hashable(self):
        c = corpus()[0]
        hash(c)
        with self.assertRaises(Exception):
            c.severity = 1                      # frozen dataclass

    def test_equality_by_value(self):
        c = corpus()[0]
        self.assertEqual(c, Case(**c.as_dict()))


if __name__ == "__main__":
    unittest.main()
