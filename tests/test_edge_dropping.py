"""
DELIBERATE DROPPING — the ranking it derives, the filters it cuts, no figure.

**No score is pinned here.** The figures live in `results3/edge_dropping.json` and
in `results3/FINDINGS3.md`. What is pinned is what keeps the experiment from being
hard rule 6 in disguise:

  * the ranking is Copeland over the queue pairs THE PROPOSER decided, and its
    tie-breaks are total and deterministic, so nothing outside the answers can
    enter it — no truth, no labels, no score;
  * `consistent` and `inconsistent` PARTITION the declared edges, so a filter
    cannot quietly drop a third category;
  * `ranking_follower_rows` changes what was declared and not which declarations
    are kept, which is why it is a diagnostic and never a candidate filter;
  * the random control keeps exactly as many edges as the filter it controls —
    the whole point, since §13 showed that dropping at all moves the score.
"""

from __future__ import annotations

import unittest

from rung3.edge_dropping import (agrees, devs, ranking_follower_rows,
                                 revealed_ranking)

X, Y, Z = "QUEUE_X", "QUEUE_Y", "QUEUE_Z"


def row(a, b, declared, ra="R1", rb="R2"):
    return {"rule_a": ra, "rule_b": rb, "action_a": a, "action_b": b,
            "declared": declared}


class TestTheRankingComesOnlyFromTheAnswers(unittest.TestCase):

    def test_a_queue_that_wins_its_pair_ranks_above(self):
        order, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        self.assertEqual(order[0], X)
        self.assertLess(rank[X], rank[Y])

    def test_the_majority_decides_the_pair_not_the_last_answer(self):
        rows = [row(X, Y, "a_beats_b"), row(X, Y, "a_beats_b"),
                row(X, Y, "b_beats_a")]
        _o, rank, _c = revealed_ranking(rows)
        self.assertLess(rank[X], rank[Y])

    def test_copeland_counts_pairs_won_not_answers_won(self):
        """A queue that wins one pair 10-0 and loses another 0-1 scores 1, not
        10. Otherwise a single lopsided queue pair would set the whole order."""
        rows = ([row(X, Y, "a_beats_b")] * 10) + [row(X, Z, "b_beats_a")]
        _o, _r, cop = revealed_ranking(rows)
        self.assertEqual(cop[X], 1)
        self.assertEqual(cop[Z], 1)

    def test_a_tied_pair_gives_neither_side_the_point(self):
        rows = [row(X, Y, "a_beats_b"), row(X, Y, "b_beats_a")]
        _o, _r, cop = revealed_ranking(rows)
        self.assertEqual((cop[X], cop[Y]), (0, 0))

    def test_the_order_is_total_and_deterministic(self):
        rows = [row(X, Y, "a_beats_b"), row(X, Y, "b_beats_a"),
                row(Y, Z, "a_beats_b"), row(Y, Z, "b_beats_a")]
        a, _r1, _c1 = revealed_ranking(rows)
        b, _r2, _c2 = revealed_ranking(rows)
        self.assertEqual(a, b)
        self.assertEqual(len(a), len(set(a)))

    def test_it_never_consults_anything_but_the_rows(self):
        """The signature admits nothing else — no labels, no masks, no score."""
        import inspect
        self.assertEqual(list(inspect.signature(revealed_ranking).parameters),
                         ["rows"])


class TestTheFiltersPartition(unittest.TestCase):

    def test_an_edge_the_ranking_endorses_agrees(self):
        _o, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        self.assertTrue(agrees(row(X, Y, "a_beats_b"), rank))

    def test_an_edge_contradicting_the_ranking_does_not(self):
        _o, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        self.assertFalse(agrees(row(X, Y, "b_beats_a"), rank))

    def test_agreement_reads_the_declared_winner_not_the_row_order(self):
        _o, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        self.assertTrue(agrees(row(Y, X, "b_beats_a"), rank))

    def test_the_two_filters_cover_every_edge_exactly_once(self):
        rows = [row(X, Y, "a_beats_b"), row(X, Y, "b_beats_a"),
                row(Y, Z, "a_beats_b")]
        _o, rank, _c = revealed_ranking(rows)
        yes = [r for r in rows if agrees(r, rank)]
        no = [r for r in rows if not agrees(r, rank)]
        self.assertEqual(len(yes) + len(no), len(rows))
        self.assertEqual([r for r in rows if r in yes and r in no], [])


class TestTheRankingFollowerIsADiagnosticNotAFilter(unittest.TestCase):

    def test_it_keeps_every_pair(self):
        rows = [row(X, Y, "a_beats_b"), row(Y, Z, "b_beats_a")]
        _o, rank, _c = revealed_ranking(rows)
        self.assertEqual(len(ranking_follower_rows(rows, rank)), len(rows))

    def test_it_rewrites_what_was_declared(self):
        """It changes the ANSWER, which is why it can never be a dropping rule:
        a filter chooses among what was said, this replaces it."""
        rows = [row(X, Y, "b_beats_a")]
        _o, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        self.assertEqual(ranking_follower_rows(rows, rank)[0]["declared"],
                         "a_beats_b")

    def test_every_row_it_returns_agrees_with_the_ranking(self):
        rows = [row(X, Y, "b_beats_a"), row(Y, Z, "b_beats_a"),
                row(X, Z, "b_beats_a")]
        _o, rank, _c = revealed_ranking(
            [row(X, Y, "a_beats_b"), row(Y, Z, "a_beats_b")])
        for r in ranking_follower_rows(rows, rank):
            with self.subTest(r=r):
                self.assertTrue(agrees(r, rank))

    def test_it_leaves_the_original_rows_untouched(self):
        rows = [row(X, Y, "b_beats_a")]
        _o, rank, _c = revealed_ranking([row(X, Y, "a_beats_b")])
        ranking_follower_rows(rows, rank)
        self.assertEqual(rows[0]["declared"], "b_beats_a")


class TestTheDeviationHelper(unittest.TestCase):

    def test_it_reports_distance_in_the_controls_own_deviations(self):
        self.assertEqual(devs(0.50, {"mean": 0.46, "sd": 0.02}), 2.0)

    def test_a_degenerate_control_gives_none_rather_than_dividing(self):
        self.assertIsNone(devs(0.50, {"mean": 0.46, "sd": 0.0}))


if __name__ == "__main__":
    unittest.main()
