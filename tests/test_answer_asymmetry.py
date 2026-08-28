"""
THE a/b ASYMMETRY — the features, the conflict test, no figure.

**No rate is pinned here.** The figures live in `results3/answer_asymmetry.json`
and in `results3/FINDINGS3.md`. What is pinned is what makes the decomposition
capable of separating the hypotheses at all:

  * the features are computed from what was SAID and from the rules' shapes, and
    `names_b` and `names_later_born` are necessarily the same number — which is
    why `H3` restates the question instead of answering it;
  * the conflict test partitions on whether the ranking and breadth agree, and it
    is the only split that can tell a ranking-follower from a breadth-preferrer,
    since on the agreeing pairs both predict the same answer;
  * the position test measures ACCURACY — the rate of following one's own ranking
    from each slot — and not a preference, which is a different quantity from the
    `names_first_shown` marginal beside it.
"""

from __future__ import annotations

import unittest

from rung3.answer_asymmetry import (conflict_test, features, position_test,
                                    predicted_names_b, rate_block,
                                    symmetry_of_following)

RANK = {"HIGH": 0, "LOW": 1}


def row(declared, a_is_broader=True, action_a="HIGH", action_b="LOW",
        a_shown_as="A"):
    return {"declared": declared, "a_is_broader": a_is_broader,
            "action_a": action_a, "action_b": action_b,
            "a_shown_as": a_shown_as, "born_a": 1, "born_b": 2}


class TestTheFeatures(unittest.TestCase):

    def test_naming_a_is_not_naming_b(self):
        f = features([row("a_beats_b")], RANK)[0]
        self.assertFalse(f["names_b"])

    def test_names_b_and_names_later_born_are_the_same_number(self):
        """`b` is later-born in every pair by construction, so H3 cannot be
        separated from the asymmetry it is meant to explain."""
        rows = [row("a_beats_b"), row("b_beats_a"), row("b_beats_a")]
        for f in features(rows, RANK):
            with self.subTest(f=f):
                self.assertEqual(f["names_b"], f["names_later_born"])

    def test_following_the_ranking_reads_the_declared_winners_queue(self):
        self.assertTrue(features([row("a_beats_b")], RANK)[0]["follows_ranking"])
        self.assertFalse(features([row("b_beats_a")], RANK)[0]["follows_ranking"])

    def test_breadth_is_read_off_the_pair_not_the_answer(self):
        self.assertTrue(features([row("a_beats_b", a_is_broader=True)],
                                 RANK)[0]["names_broader"])
        self.assertFalse(features([row("a_beats_b", a_is_broader=False)],
                                  RANK)[0]["names_broader"])

    def test_position_is_read_off_the_slot_the_rule_occupied(self):
        self.assertTrue(features([row("a_beats_b", a_shown_as="A")],
                                 RANK)[0]["names_first_shown"])
        self.assertFalse(features([row("a_beats_b", a_shown_as="B")],
                                  RANK)[0]["names_first_shown"])


class TestTheConflictTest(unittest.TestCase):

    def test_it_splits_on_whether_the_two_hypotheses_agree(self):
        agree = row("a_beats_b", a_is_broader=True)      # ranking->a, broader->a
        clash = row("a_beats_b", a_is_broader=False)     # ranking->a, broader->b
        c = conflict_test(features([agree, clash], RANK))
        self.assertEqual(c["ranking_and_breadth_agree"]["n"], 1)
        self.assertEqual(c["they_disagree"]["n"], 1)

    def test_on_agreeing_pairs_the_two_rates_are_identical_by_construction(self):
        """Which is exactly why those pairs decide nothing."""
        rows = [row("a_beats_b", a_is_broader=True),
                row("b_beats_a", a_is_broader=True)]
        c = conflict_test(features(rows, RANK))["ranking_and_breadth_agree"]
        self.assertEqual(c["follows_ranking"]["rate"],
                         c["names_broader"]["rate"])

    def test_on_disagreeing_pairs_the_two_rates_are_complementary(self):
        rows = [row("a_beats_b", a_is_broader=False),
                row("b_beats_a", a_is_broader=False)]
        c = conflict_test(features(rows, RANK))["they_disagree"]
        self.assertAlmostEqual(c["follows_ranking"]["rate"]
                               + c["names_broader"]["rate"], 1.0)


class TestTheSymmetryTest(unittest.TestCase):

    def test_equal_following_on_both_sides_is_no_asymmetry(self):
        rows = [row("a_beats_b", action_a="HIGH", action_b="LOW"),
                row("b_beats_a", action_a="LOW", action_b="HIGH")]
        s = symmetry_of_following(features(rows, RANK))
        self.assertEqual(s["difference"], 0.0)

    def test_following_more_on_one_side_shows_up_as_a_difference(self):
        rows = ([row("a_beats_b", action_a="HIGH", action_b="LOW")] * 2
                + [row("a_beats_b", action_a="LOW", action_b="HIGH")] * 2)
        s = symmetry_of_following(features(rows, RANK))
        self.assertNotEqual(s["difference"], 0.0)


class TestThePrediction(unittest.TestCase):

    def test_a_perfect_follower_names_b_exactly_when_the_ranking_does(self):
        rows = [row("a_beats_b", action_a="HIGH", action_b="LOW"),
                row("b_beats_a", action_a="LOW", action_b="HIGH")]
        p = predicted_names_b(features(rows, RANK))
        self.assertEqual(p["follows_the_ranking"], 1.0)
        self.assertEqual(p["predicted"], p["observed"])
        self.assertEqual(p["residual"], 0.0)

    def test_it_reports_the_residual_in_standard_errors(self):
        rows = [row("a_beats_b"), row("b_beats_a")]
        self.assertIn("residual_in_standard_errors",
                      predicted_names_b(features(rows, RANK)))


class TestThePositionTest(unittest.TestCase):

    def test_it_measures_following_and_not_preference(self):
        """Same answer, same ranking, different slot: the two buckets must
        differ only in where the favoured rule sat."""
        rows = [row("a_beats_b", a_shown_as="A"),
                row("a_beats_b", a_shown_as="B")]
        p = position_test(features(rows, RANK))
        self.assertEqual(p["favoured_shown_first"]["n"], 1)
        self.assertEqual(p["favoured_shown_second"]["n"], 1)
        self.assertEqual(p["favoured_shown_first"]["rate"], 1.0)
        self.assertEqual(p["favoured_shown_second"]["rate"], 1.0)
        self.assertEqual(p["difference"], 0.0)


class TestTheRateBlock(unittest.TestCase):

    def test_a_coin_is_zero_deviations(self):
        self.assertEqual(rate_block(50, 100, "x")["deviations_from_a_coin"], 0.0)

    def test_the_standard_error_shrinks_with_n(self):
        self.assertLess(rate_block(500, 1000, "x")["standard_error"],
                        rate_block(50, 100, "x")["standard_error"])


if __name__ == "__main__":
    unittest.main()
