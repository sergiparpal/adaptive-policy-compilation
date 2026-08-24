"""
THE BASELINE THAT READS NO RULE — its arithmetic, not its figures.

`pair_judgement_baselines` answers one question about Stage C: how much of the
benchmark is decidable **without looking at the rules at all**, by a fixed order
over the eight queues. **No figure of that finding is pinned here.** What the
best hierarchy scores, what the model scores inside each half of the split, and
how many queue-pairs reverse live in `results2/pair_judgement_baselines.json`
and in the section appended to `results2/FINDINGS2.md`.

What is pinned is the arithmetic, on instances small enough to write out by
hand, plus one structural invariant worth more than any of them: **the mean over
all permutations is exactly one half**, because a permutation and its reverse
answer every pair in opposite directions and their scores sum to `n`. If the
enumeration ever missed an order or double-counted one, that identity is what
breaks — and it is the only cheap check that the "best of 40,320" is a maximum
over the whole set rather than over a sample of it.
"""

from __future__ import annotations

import itertools
import unittest

from rung2.pair_judgement_baselines import (all_hierarchies, decomposition,
                                            model_consistency, queues_of,
                                            reversible_queue_pairs,
                                            score_hierarchy)

A, B, C = "AAA", "BBB", "CCC"


def row(winner_action, loser_action, outcome="correct", answer="?", k=0):
    return {"winner": f"H{k:02d}", "loser": f"H{k + 1:02d}",
            "winner_action": winner_action, "loser_action": loser_action,
            "outcome": outcome,
            "answer": (winner_action if outcome == "correct"
                       else loser_action if outcome == "wrong" else None)}


class TestTheHierarchyScore(unittest.TestCase):

    def test_it_answers_with_the_higher_ranked_queue(self):
        rows = [row(A, B), row(A, C), row(B, C)]
        self.assertEqual(score_hierarchy({A: 0, B: 1, C: 2}, rows), 3)
        self.assertEqual(score_hierarchy({C: 0, B: 1, A: 2}, rows), 0)

    def test_it_reads_nothing_but_the_two_queues(self):
        """The rule ids, the ticket and the outcome are all present in the row
        and none of them may change the answer."""
        rank = {A: 0, B: 1, C: 2}
        plain = [row(A, B)]
        loaded = [dict(row(A, B), witness={"severity": 1}, outcome="wrong",
                       winner="H99", overlap_cases=33600)]
        self.assertEqual(score_hierarchy(rank, plain),
                         score_hierarchy(rank, loaded))

    def test_the_queues_are_read_off_both_sides(self):
        self.assertEqual(queues_of([row(A, B), row(C, A)]), [A, B, C])


class TestTheEnumeration(unittest.TestCase):

    def test_it_finds_the_maximum(self):
        rows = [row(A, B), row(A, C), row(B, C)]
        h, order = all_hierarchies(rows)
        self.assertEqual(h["best"], 3)
        self.assertEqual(list(order), [A, B, C])
        self.assertEqual(h["best_rate"], 1.0)

    def test_it_scores_every_permutation_and_no_more(self):
        rows = [row(A, B), row(B, C)]
        h, _o = all_hierarchies(rows)
        self.assertEqual(h["n_queues"], 3)
        self.assertEqual(h["n_orders"], 6)

    def test_the_mean_over_all_orders_is_exactly_one_half(self):
        """A permutation and its reverse answer every pair the opposite way, so
        their scores sum to n. That makes the mean n/2 for ANY set of pairs —
        and it is the check that the enumeration covers the whole group."""
        for rows in ([row(A, B)],
                     [row(A, B), row(A, C), row(B, C)],
                     [row(A, B), row(B, A), row(C, A), row(A, C)]):
            with self.subTest(n=len(rows)):
                h, _o = all_hierarchies(rows)
                self.assertEqual(h["mean"], 0.5)

    def test_a_reversed_pair_caps_the_best_below_one(self):
        """The same two queues with both winners cannot both be served."""
        h, _o = all_hierarchies([row(A, B), row(B, A)])
        self.assertEqual(h["best"], 1)

    def test_the_best_really_is_the_maximum_by_brute_force(self):
        rows = [row(A, B), row(A, C), row(B, C), row(C, A)]
        h, _o = all_hierarchies(rows)
        by_hand = max(score_hierarchy({a: i for i, a in enumerate(p)}, rows)
                      for p in itertools.permutations(queues_of(rows)))
        self.assertEqual(h["best"], by_hand)


class TestWhereAHierarchyCannotReach(unittest.TestCase):

    def test_a_queue_pair_seen_with_both_winners_is_reported(self):
        r = reversible_queue_pairs([row(A, B), row(B, A), row(A, C)])
        self.assertEqual(r["n_queue_pairs"], 1)
        self.assertEqual(r["queue_pairs"], [[A, B]])
        self.assertEqual(r["n_rule_pairs_involved"], 2)

    def test_a_queue_pair_always_won_by_the_same_side_is_not(self):
        r = reversible_queue_pairs([row(A, B), row(A, B), row(A, C)])
        self.assertEqual(r["n_queue_pairs"], 0)
        self.assertEqual(r["n_rule_pairs_involved"], 0)

    def test_it_counts_every_rule_pair_of_a_reversed_queue_pair(self):
        """Both directions count, not only the minority one: the whole
        queue-pair is what no ordering can serve."""
        rows = [row(A, B), row(A, B), row(A, B), row(B, A)]
        self.assertEqual(reversible_queue_pairs(rows)["n_rule_pairs_involved"], 4)


class TestTheDecomposition(unittest.TestCase):

    def test_it_splits_by_the_hierarchy_and_scores_the_model_inside_each(self):
        rank = {A: 0, B: 1, C: 2}
        rows = [row(A, B, "correct"), row(A, C, "wrong"),
                row(B, A, "correct"), row(C, A, "wrong")]
        d = decomposition(rows, rank)
        right = d["where_the_hierarchy_is_right"]
        wrong = d["where_the_hierarchy_is_wrong"]
        self.assertEqual((right["n"], right["model_correct"]), (2, 1))
        self.assertEqual((wrong["n"], wrong["model_correct"]), (2, 1))
        self.assertEqual(right["model_rate"], 0.5)

    def test_the_unreachable_half_is_listed_pair_by_pair(self):
        rank = {A: 0, B: 1}
        d = decomposition([row(A, B, "correct"), row(B, A, "wrong")], rank)
        pairs = d["where_the_hierarchy_is_wrong"]["pairs"]
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["winner_action"], B)
        self.assertEqual(pairs[0]["model"], "wrong")

    def test_neither_counts_against_the_model_in_both_halves(self):
        rank = {A: 0, B: 1}
        d = decomposition([row(A, B, "neither"), row(B, A, "neither")], rank)
        self.assertEqual(d["where_the_hierarchy_is_right"]["model_rate"], 0.0)
        self.assertEqual(d["where_the_hierarchy_is_wrong"]["model_rate"], 0.0)

    def test_an_empty_half_reports_none_and_not_a_zero(self):
        d = decomposition([row(A, B, "correct")], {A: 0, B: 1})
        self.assertIsNone(d["where_the_hierarchy_is_wrong"]["model_rate"])


class TestWhetherTheModelIsAHierarchy(unittest.TestCase):

    def test_a_model_that_always_answers_the_same_queue_varies_nowhere(self):
        rows = [row(A, B, "correct"), row(B, A, "wrong")]   # both answered A
        c = model_consistency(rows)
        self.assertEqual(c["n_varying"], 0)
        self.assertEqual(c["n_queue_pairs_answered"], 1)

    def test_a_model_that_answers_both_ways_is_reported_as_varying(self):
        rows = [row(A, B, "correct"), row(B, A, "correct")]  # A then B
        c = model_consistency(rows)
        self.assertEqual(c["n_varying"], 1)
        self.assertEqual(c["varying"][f"{A} vs {B}"], {A: 1, B: 1})

    def test_an_unanswered_row_is_an_absence_and_not_a_disagreement(self):
        rows = [row(A, B, "correct"), row(A, B, "neither")]
        c = model_consistency(rows)
        self.assertEqual(c["n_varying"], 0)
        self.assertEqual(c["unanswered_rows"], 1)


class TestItRewritesNothing(unittest.TestCase):

    def test_the_source_record_is_only_read(self):
        """The Stage C record cost money. Nothing here may write to it."""
        import ast
        from pathlib import Path

        src = Path("rung2/pair_judgement_baselines.py").read_text()
        tree = ast.parse(src)
        writes = [n for n in ast.walk(tree)
                  if isinstance(n, ast.Attribute)
                  and n.attr in ("write_text", "write_bytes", "unlink")]
        # exactly one write, and it is the new record
        self.assertEqual(len(writes), 1)
        self.assertIn('(OUT / RECORD).write_text', src)
        self.assertNotIn("SOURCE.write", src)


if __name__ == "__main__":
    unittest.main()
