"""
THE BUDGET CURVE — its nesting, its ties and its crossings. No figure.

`edge_budget` answers whether the pairwise channel pays with more edges. **No
value of that answer is pinned here**; the curve lives in
`results3/edge_budget.json` and in `results3/FINDINGS3.md` §10.

What is pinned is the machinery that decides whether the curve IS a curve:

  * the oracle's direction is the rule that gets more of the shared region
    right, and a tie offers nothing rather than a coin flip;
  * a tie contributes no edge, so a budget is `pairs asked about` and not
    `edges obtained` — the record publishes both because they differ;
  * `crossing` finds the first budget above a line and says None when there is
    none, rather than silently returning the last one.

The nesting itself — every budget a prefix of one shuffle — is checked on the
real population in the module's own run, because it is a property of the shuffle
and not of a function.
"""

from __future__ import annotations

import unittest

from rung3.edge_budget import BUDGETS, crossing, oracle_directions

A, B = "R0001", "R0002"


class _Ext(dict):
    pass


class TestTheOraclesDirection(unittest.TestCase):

    def directions(self, ext_a, ext_b, truth_a, truth_b):
        ext = {A: ext_a, B: ext_b}
        action = {A: "AAA", B: "BBB"}
        tmask = {"AAA": truth_a, "BBB": truth_b}
        return oracle_directions([(A, B)], ext, action, tmask)[(A, B)]

    def test_it_points_at_the_rule_right_more_often(self):
        # overlap is 0b0110; AAA true on both of those bits, BBB on neither
        self.assertTrue(self.directions(0b1110, 0b0111, 0b0110, 0b0000))

    def test_it_points_the_other_way_when_the_other_wins(self):
        self.assertFalse(self.directions(0b1110, 0b0111, 0b0000, 0b0110))

    def test_an_equal_split_is_a_tie_and_offers_nothing(self):
        self.assertIsNone(self.directions(0b1110, 0b0111, 0b0100, 0b0010))

    def test_neither_ever_right_is_also_a_tie(self):
        """The material problem: the truth over the whole shared region is some
        third queue. Nothing to declare, and forcing a direction would credit
        the channel with a coin flip it never made."""
        self.assertIsNone(self.directions(0b1110, 0b0111, 0b0000, 0b0000))

    def test_only_the_overlap_counts(self):
        """Cases outside `ext(a) & ext(b)` are not a competition between these
        two rules and must not move the verdict."""
        # AAA is true all over ext(a) but nowhere in the overlap; BBB wins there
        self.assertFalse(self.directions(0b1110, 0b0111, 0b1000, 0b0010))


class TestTheCrossing(unittest.TestCase):

    def rows(self, values):
        return [{"budget": 100 * (k + 1), "oracle": v}
                for k, v in enumerate(values)]

    def test_it_returns_the_first_budget_above_the_line(self):
        self.assertEqual(crossing(self.rows([0.40, 0.45, 0.50]), "oracle",
                                  0.46), 300)

    def test_a_curve_that_never_crosses_returns_none(self):
        self.assertIsNone(crossing(self.rows([0.40, 0.41, 0.42]), "oracle",
                                   0.46))

    def test_a_curve_already_above_crosses_at_its_first_budget(self):
        self.assertEqual(crossing(self.rows([0.50, 0.55]), "oracle", 0.46), 100)

    def test_the_line_is_strict(self):
        """Equal is not above. P-d's own band is `strictly above the floor by
        more than the margin`, and the crossing has to read the same way."""
        self.assertIsNone(crossing(self.rows([0.46, 0.46]), "oracle", 0.46))


class TestTheBudgetLadder(unittest.TestCase):

    def test_it_is_increasing_and_ends_at_the_whole_population(self):
        named = [b for b in BUDGETS if b is not None]
        self.assertEqual(named, sorted(named))
        self.assertIsNone(BUDGETS[-1], "the ladder must end at everything")

    def test_it_starts_at_the_budget_stage_d_actually_spent(self):
        """So the curve's first point is the one there is a paid measurement
        for, and the rest is extrapolation off a shared anchor."""
        self.assertEqual(BUDGETS[0], 400)


if __name__ == "__main__":
    unittest.main()
