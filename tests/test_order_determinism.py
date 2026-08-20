"""
REGRESSION test for the August 6, 2026 fix: the greedy search no longer depends
on the hash.

WHAT HAPPENED. The greedy argmax walked a `set` of rule identifiers, so the
tie-break was at the mercy of the iteration order of a set of strings, which
depends on `PYTHONHASHSEED`. The same cell gave between 0.5880 and 0.5991
depending on the hash. It was discovered with two rungs already closed on top of
it. The fix —iterating over `sorted(left)`— is one line; the problem is that
nothing would have caught it.

This is what catches it. `tests/hashseed_child.py` runs the greedy search of
both rungs in a separate process and signs the resulting order; the parent
invokes it with three different `PYTHONHASHSEED` values and compares.

THE WITNESS. The child also signs the iteration order of a set of those same
identifiers. That witness MUST change between seeds: if it did not, the test
would pass without checking anything —it would mean that in this version of
Python hashing is no longer randomized, not that the greedy search is
deterministic.

NO accuracy value is pinned here. The published figures of rungs 3 and 4 are
those of the code PRIOR to the fix and are pending a re-run together with a
serious optimizer; pinning the new values here would create a second official
figure that no FINDINGS backs. See IDEAS.md.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from rung3.order_search import (build_tables, greedy_order, load, split,
                                   subsumption_below)

REPO = Path(__file__).resolve().parent.parent
HASH_SEEDS = ("0", "1", "2")


def run_child(hashseed: str) -> dict:
    env = dict(os.environ, PYTHONHASHSEED=hashseed)
    p = subprocess.run([sys.executable, "-m", "tests.hashseed_child"],
                       cwd=REPO, env=env, capture_output=True, text=True,
                       timeout=300)
    if p.returncode != 0:
        raise AssertionError(f"el hijo fallo con PYTHONHASHSEED={hashseed}:\n"
                             f"{p.stderr}")
    return json.loads(p.stdout)


class TestHashSeedInvariance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = {s: run_child(s) for s in HASH_SEEDS}

    def test_the_witness_confirms_the_hash_is_randomized(self):
        """If this fails, the other tests in this class prove nothing."""
        seen = {r["set_iteration"] for r in self.runs.values()}
        self.assertEqual(len(seen), len(HASH_SEEDS),
                         "el orden de iteracion del set no cambio entre "
                         "semillas: el resto de esta clase es vacuo")

    def test_the_rung_3_greedy_does_not_depend_on_the_hash(self):
        seen = {r["greedy_p3"] for r in self.runs.values()}
        self.assertEqual(len(seen), 1, f"ordenes distintos: {self.runs}")

    def test_the_rung_4_greedy_does_not_depend_on_the_hash(self):
        seen = {r["greedy_p4"] for r in self.runs.values()}
        self.assertEqual(len(seen), 1, f"ordenes distintos: {self.runs}")

    def test_the_multistart_local_search_does_not_depend_on_the_hash(self):
        """Added August 8, 2026 with the optimizer. Its starts come from a
        declared seed and its argmax never walks a set, but that was believed of
        the greedy too until it was checked here."""
        for field in ("multistart_order", "multistart_score", "multistart_from"):
            with self.subTest(field):
                seen = {r[field] for r in self.runs.values()}
                self.assertEqual(len(seen), 1, f"{field} difiere: {seen}")

    def test_the_resulting_accuracy_is_identical(self):
        seen = {r["test_p3"] for r in self.runs.values()}
        self.assertEqual(len(seen), 1, f"exactitudes distintas: {seen}")

    def test_the_input_material_is_the_expected_one(self):
        """577 rules: the rung 1 base that rungs 3 and 4 start from. If this
        changes, somebody rewrote results/llm_run.json."""
        for s, r in self.runs.items():
            with self.subTest(hashseed=s):
                self.assertEqual(r["n_rules"], 577)


class TestTheGreedyContract(unittest.TestCase):
    """Properties of the produced order, in the same process."""

    @classmethod
    def setUpClass(cls):
        corpus, rules, ext, conds = load()
        cls.rules = rules
        cls.action = {r["rule_id"]: r["action"] for r in rules}
        below = subsumption_below(rules, ext)
        cls.matched, _undef, cls.truth = build_tables(corpus, rules, conds, below)
        cls.train, _test = split(corpus, cls.truth, seed=17)

    def computed_order(self):
        return greedy_order(self.rules, self.matched, self.truth,
                            self.action, self.train)

    def test_is_a_permutation_of_every_rule(self):
        order = self.computed_order()
        self.assertEqual(len(order), len(self.rules))
        self.assertEqual(set(order), {r["rule_id"] for r in self.rules})

    def test_two_calls_give_the_same_order(self):
        self.assertEqual(self.computed_order(), self.computed_order())

    def test_the_partition_is_stable_and_disjoint(self):
        corpus, rules, ext, conds = load()
        below = subsumption_below(rules, ext)
        _m, _u, truth = build_tables(corpus, rules, conds, below)
        tr1, te1 = split(corpus, truth, seed=17)
        tr2, te2 = split(corpus, truth, seed=17)
        self.assertEqual((tr1, te1), (tr2, te2))
        self.assertEqual(set(tr1) & set(te1), set())
        self.assertEqual(len(tr1) + len(te1), 2000)

    def test_the_copies_of_a_case_fall_on_the_same_side(self):
        """The split is grouped by case identity: otherwise the test would
        reward memorizing, because 12.8% of the corpus has an exact twin."""
        corpus, rules, ext, conds = load()
        below = subsumption_below(rules, ext)
        _m, _u, truth = build_tables(corpus, rules, conds, below)
        tr, te = split(corpus, truth, seed=17)
        train_keys = {corpus[i].key() for i in tr}
        test_keys = {corpus[i].key() for i in te}
        self.assertEqual(train_keys & test_keys, set())


if __name__ == "__main__":
    unittest.main()
