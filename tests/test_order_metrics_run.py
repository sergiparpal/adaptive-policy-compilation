"""
The pieces of the P4 runner that something else rests on.

Not the figures: those live in `results3/order_metrics.json` and in the findings
that own them, and pinning them here would create a second official home for a
number, which is the mistake `tests/test_local_search.py` and
`tests/test_order_metrics.py` both decline to make.

What is pinned is the arithmetic the run cannot be wrong about:

  * `prefix_winner` reproduces `multistart`'s tie-break — strictly greater wins,
    so a tie goes to the lowest index. Three published figures are read off a
    prefix, and if this drifted they would silently become a different order's;
  * `spearman` is a rank correlation and not something that merely resembles
    one, ties included, because the whole of Q-d is one number it returns;
  * a behavioural signature's digest changes when the behaviour changes, which
    is what makes counting distinct digests a count of distinct machines.
"""

from __future__ import annotations

import unittest

from rung3.order_metrics import signature
from rung3.order_metrics_run import (digest, prefix_winner, summary,
                                        slice_pairs, spearman)


def rows(puntuaciones):
    return [{"index": k, "end_score": s, "order": [f"R{k:03d}"]}
            for k, s in enumerate(puntuaciones)]


class TestThePrefixWinner(unittest.TestCase):

    def test_the_best_score_wins(self):
        f = rows([3, 9, 5])
        self.assertEqual(prefix_winner(f, 3)["index"], 1)

    def test_a_tie_goes_to_the_lowest_index(self):
        """`multistart` applies `if st["end"] > best_score`, so the first of an
        equal pair keeps the crown. The prefix has to agree or the winner it
        reports is not the winner the record reports."""
        f = rows([7, 7, 7])
        self.assertEqual(prefix_winner(f, 3)["index"], 0)

    def test_looks_only_at_the_requested_prefix(self):
        """The point of the shortcut: a better order further down the 257 rows
        must not leak into the 65-start answer."""
        f = rows([4, 6, 99])
        self.assertEqual(prefix_winner(f, 2)["index"], 1)
        self.assertEqual(prefix_winner(f, 3)["index"], 2)

    def test_a_prefix_of_one_is_the_greedy(self):
        f = rows([2, 100])
        self.assertEqual(prefix_winner(f, 1)["index"], 0)


class TestTheMatrixTrim(unittest.TestCase):

    def test_keeps_the_pairs_of_the_first_k(self):
        pairs = [{"i": 0, "j": 1}, {"i": 0, "j": 5}, {"i": 2, "j": 3},
                 {"i": 4, "j": 6}]
        self.assertEqual(slice_pairs(pairs, 4), [{"i": 0, "j": 1},
                                                 {"i": 2, "j": 3}])
        self.assertEqual(len(slice_pairs(pairs, 7)), 4)
        self.assertEqual(slice_pairs(pairs, 1), [])


class TestSpearman(unittest.TestCase):

    def test_monotone_increasing_is_one_and_decreasing_minus_one(self):
        xs = [1, 2, 3, 4, 5]
        self.assertEqual(spearman(xs, [10, 20, 30, 40, 50]), 1.0)
        self.assertEqual(spearman(xs, [50, 40, 30, 20, 10]), -1.0)

    def test_does_not_depend_on_scale_only_on_order(self):
        xs = [1, 2, 3, 4]
        self.assertEqual(spearman(xs, [1, 100, 1000, 10000]),
                         spearman(xs, [1, 2, 3, 4]))

    def test_ties_share_the_rank(self):
        """Average ranks, computed by hand: x ranks 1,2.5,2.5,4 against y ranks
        1,2,3,4 give 0.9487."""
        self.assertAlmostEqual(spearman([1, 2, 2, 3], [1, 2, 3, 4]),
                               0.9487, places=4)

    def test_with_no_variation_there_is_no_correlation(self):
        self.assertIsNone(spearman([5, 5, 5], [1, 2, 3]))

    def test_with_fewer_than_two_points_it_returns_nothing(self):
        self.assertIsNone(spearman([1], [2]))


class TestTheSignatureDigest(unittest.TestCase):

    def test_the_same_behaviour_gives_the_same_name(self):
        a = signature({"A": 0b1010, "B": 0b0101}, 0)
        b = signature({"B": 0b0101, "A": 0b1010}, 0)
        self.assertEqual(digest(a), digest(b))

    def test_a_different_behaviour_gives_another(self):
        a = signature({"A": 0b1010, "B": 0b0101}, 0)
        b = signature({"A": 0b1011, "B": 0b0100}, 0)
        self.assertNotEqual(digest(a), digest(b))

    def test_tells_apart_who_leaves_cases_undecided(self):
        a = signature({"A": 0b0010}, 0b1000)
        b = signature({"A": 0b0010}, 0)
        self.assertNotEqual(digest(a), digest(b))

    def test_does_not_confuse_the_action_with_the_mask(self):
        a = signature({"A": 0b1100, "B": 0b0011}, 0)
        b = signature({"A": 0b0011, "B": 0b1100}, 0)
        self.assertNotEqual(digest(a), digest(b))


class TestTheSummary(unittest.TestCase):

    def test_gives_the_declared_quantiles(self):
        r = summary([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual((r["n"], r["min"], r["max"]), (8, 1, 8))
        self.assertEqual(r["median"], 4.5)
        self.assertEqual((r["p25"], r["p75"]), (3, 7))

    def test_does_not_care_about_the_input_order(self):
        self.assertEqual(summary([3, 1, 2]), summary([1, 2, 3]))

    def test_empty_is_nothing(self):
        self.assertIsNone(summary([]))


if __name__ == "__main__":
    unittest.main()
