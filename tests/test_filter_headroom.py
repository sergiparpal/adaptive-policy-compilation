"""
THE HEADROOM OF A SELECTION — the selectors, the samplers and the cuts, no figure.

**No score is pinned here.** The figures live in `results3/filter_headroom.json`
and in `results3/FINDINGS3.md` §16. What is pinned is what makes the ceiling a
ceiling and the control a control:

  * the oracle keeps the right edges first, the undefined ones next and the
    wrong ones last, and the anti selector is exactly its reverse;
  * every selection and every control returns its rows IN THE ORDER THEY
    ARRIVED, except §14's own shuffled control, which is kept for comparison;
  * the filters partition where they claim to: `spec` and `no_spec`, `queue`
    and `no_queue`, `consistent` and `inconsistent`;
  * the draws are seeded by strings, so no control depends on the hash seed.
"""

from __future__ import annotations

import random
import unittest

from rung3 import filter_headroom as fh

X, Y = "QUEUE_X", "QUEUE_Y"


def row(i, declared="a_beats_b", why=""):
    return {"index": i, "rule_a": f"R{i}a", "rule_b": f"R{i}b", "action_a": X,
            "action_b": Y, "declared": declared, "why": why}


TRUTH = {0: {"better_space": "a", "better_corpus": "b"},
         1: {"better_space": "b", "better_corpus": "tie"},
         2: {"better_space": "neither_ever_right", "better_corpus": "a"},
         3: {"better_space": "a", "better_corpus": "a"}}


class TestTheConstants(unittest.TestCase):

    def test_they_are_the_declared_ones(self):
        self.assertEqual(fh.DRAWS, 200)
        self.assertEqual(fh.SEED, "filter_headroom")
        self.assertEqual(fh.SPLIT_SEED, 17)
        self.assertEqual(fh.SHUFFLED_FILTERS, ("keep_all", "consistent", "inconsistent"))


class TestTheOracle(unittest.TestCase):

    def test_right_undefined_wrong(self):
        rows = [row(0), row(1), row(2), row(3, "b_beats_a")]
        self.assertEqual([fh.oracle_rank(r, TRUTH, "space") for r in rows], [0, 2, 1, 2])
        self.assertEqual([fh.oracle_rank(r, TRUTH, "corpus") for r in rows], [2, 1, 0, 2])

    def test_select_ranks_first_and_returns_arrival_order(self):
        rows = [row(0), row(1), row(2), row(3, "b_beats_a")]
        kept = fh.select(rows, 2, lambda r: fh.oracle_rank(r, TRUTH, "space"))
        self.assertEqual([r["index"] for r in kept], [0, 2])
        anti = fh.select(rows, 2, lambda r: -fh.oracle_rank(r, TRUTH, "space"))
        self.assertEqual([r["index"] for r in anti], [1, 3])

    def test_ties_go_to_the_earlier_arrival(self):
        rows = [row(i) for i in range(4)]
        kept = fh.select(rows, 2, lambda r: 0)
        self.assertEqual([r["index"] for r in kept], [0, 1])


class TestTheSamplers(unittest.TestCase):

    def test_arrival_order_is_kept(self):
        rows = [row(i) for i in range(50)]
        kept = fh.in_arrival_order(rows, 20, random.Random("x"))
        idx = [r["index"] for r in kept]
        self.assertEqual(len(idx), 20)
        self.assertEqual(idx, sorted(idx))
        self.assertEqual(idx, [r["index"] for r in
                               fh.in_arrival_order(rows, 20, random.Random("x"))])

    def test_the_shuffled_control_keeps_the_size_and_not_the_order(self):
        rows = [row(i) for i in range(50)]
        kept = fh.shuffled(rows, 20, random.Random("x"))
        idx = [r["index"] for r in kept]
        self.assertEqual(len(set(idx)), 20)
        self.assertNotEqual(idx, sorted(idx))

    def test_deviations(self):
        self.assertEqual(fh.deviations(0.5, {"mean": 0.4, "sd": 0.05}), 2.0)
        self.assertIsNone(fh.deviations(0.5, {"mean": 0.4, "sd": 0.0}))


class TestTheFiltersPartition(unittest.TestCase):

    def test_the_cuts(self):
        rows = [row(0, why="La regla A es más específica (3 condiciones)."),
                row(1, why="Security keyword present, overriding the rest."),
                row(2, "b_beats_a", why="Product is billing."),
                row(3, why="")]
        _o, rank, _c = fh.revealed_ranking(rows)
        cuts = fh.filters(rows, rank)
        for a, b in (("spec", "no_spec"), ("queue", "no_queue"),
                     ("consistent", "inconsistent")):
            with self.subTest(a=a):
                self.assertEqual(sorted(r["index"] for r in cuts[a] + cuts[b]),
                                 [0, 1, 2, 3])
                self.assertFalse({r["index"] for r in cuts[a]}
                                 & {r["index"] for r in cuts[b]})
        self.assertEqual([r["index"] for r in cuts["spec"]], [0])
        self.assertEqual([r["index"] for r in cuts["queue"]], [1])
        self.assertEqual([r["index"] for r in cuts["no_count"]], [1, 2, 3])
        self.assertEqual(len(cuts["keep_all"]), 4)


if __name__ == "__main__":
    unittest.main()
