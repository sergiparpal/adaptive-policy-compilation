"""
THE MFAS COMPILATION — its objective, its gate, and the property that keeps it
comparable. No figure.

`mfas_compilation` changes how declared edges become a total order while holding
the answers fixed. **No score is pinned here**; the figures live in
`results3/mfas_compilation.json` and in `results3/FINDINGS3.md`. What is pinned is
what would make a score difference mean something other than compilation:

  * `violations` counts what the order contradicts, and `declared_edges` builds
    the set from EVERY answered pair — including the ones `try_edge` refused,
    because a refusal is a property of the compilation and scoring the baseline
    only on the edges it chose to keep would score it against its own choices;
  * the search moves a vertex only on STRICT improvement, so a rule with no
    incident edge is never moved on its own account and the untouched rules keep
    their arrival order relative to each other — the property that makes the
    comparison against the floor mean `what did the edges add`;
  * the baseline is one of the starts, so `mfas <= topological` on violations
    holds by construction — and `gate_beats_the_baseline` checks it anyway,
    because the first run of this module lost to the baseline by four violations
    on the oracle's edges and would have reported a compilation difference that
    was a fact about the search.
"""

from __future__ import annotations

import unittest

from rung3.mfas_compilation import (adjacency, best_move, declared_edges,
                                    gate_beats_the_baseline, local_search_fas,
                                    mfas_order, net_wins_order, violations)

IDS = [f"R{i:04d}" for i in range(1, 7)]
BORN = {rid: i for i, rid in enumerate(IDS)}
A, B, C, D, E, F = IDS


class TestTheObjective(unittest.TestCase):

    def test_an_order_honouring_every_edge_has_no_violations(self):
        self.assertEqual(violations(IDS, [(A, B), (B, C), (A, C)]), 0)

    def test_a_reversed_order_violates_every_edge(self):
        self.assertEqual(violations(IDS[::-1], [(A, B), (B, C), (A, C)]), 3)

    def test_it_counts_only_the_edges_it_is_given(self):
        self.assertEqual(violations(IDS, [(C, A)]), 1)

    def test_a_three_cycle_always_costs_at_least_one(self):
        """The reason a topological sort has to drop something and MFAS has to
        violate something: no linear order satisfies a cycle."""
        cycle = [(A, B), (B, C), (C, A)]
        for order in ([A, B, C], [B, C, A], [C, A, B], [C, B, A]):
            with self.subTest(order=order):
                self.assertGreaterEqual(violations(order + [D, E, F], cycle), 1)


class TestTheDeclaredSetIsWhatWasSaid(unittest.TestCase):

    def rows(self, spec):
        return [{"rule_a": a, "rule_b": b, "declared": d} for a, b, d in spec]

    def test_a_beats_b_points_from_a(self):
        self.assertEqual(declared_edges(self.rows([(A, B, "a_beats_b")])),
                         [(A, B)])

    def test_b_beats_a_points_from_b(self):
        self.assertEqual(declared_edges(self.rows([(A, B, "b_beats_a")])),
                         [(B, A)])

    def test_a_pair_with_no_edge_contributes_nothing(self):
        self.assertEqual(declared_edges(self.rows([(A, B, "none")])), [])

    def test_it_does_not_consult_try_edge(self):
        """Every answered pair is in the set. A cycle-refused edge is still
        something the proposer said, and the fidelity metric has to see it or the
        baseline is scored against its own choices."""
        rows = self.rows([(A, B, "a_beats_b"), (B, C, "a_beats_b"),
                          (C, A, "a_beats_b")])
        self.assertEqual(len(declared_edges(rows)), 3)


class TestTheSearchKeepsUntouchedRulesPut(unittest.TestCase):

    def test_a_vertex_with_no_edges_never_moves_on_its_own_account(self):
        out, inc = adjacency([(A, B)], IDS)
        for i, rid in enumerate(IDS):
            if rid in (A, B):
                continue
            with self.subTest(rid):
                _j, delta = best_move(IDS, i, out, inc)
                self.assertEqual(delta, 0, "an untouched rule has no incentive")

    def test_untouched_rules_keep_their_relative_arrival_order(self):
        order, _ = local_search_fas(IDS, [(F, A)], IDS)
        untouched = [r for r in order if r not in (A, F)]
        self.assertEqual(untouched, [B, C, D, E])

    def test_an_order_already_optimal_is_left_alone(self):
        order, moves = local_search_fas(IDS, [(A, B), (B, C)], IDS)
        self.assertEqual(order, IDS)
        self.assertEqual(moves, 0)

    def test_a_single_bad_edge_is_repaired(self):
        order, moves = local_search_fas(IDS, [(F, A)], IDS)
        self.assertEqual(violations(order, [(F, A)]), 0)
        self.assertGreater(moves, 0)


class TestBestMove(unittest.TestCase):

    def test_it_reports_the_improvement_as_a_negative_delta(self):
        out, inc = adjacency([(F, A)], IDS)
        _j, delta = best_move(IDS, 0, out, inc)
        self.assertLess(delta, 0)

    def test_it_never_reports_a_positive_delta(self):
        """Staying put is always available, so the best move cannot be worse."""
        out, inc = adjacency([(A, B), (C, D), (F, A)], IDS)
        for i in range(len(IDS)):
            with self.subTest(i=i):
                self.assertLessEqual(best_move(IDS, i, out, inc)[1], 0)


class TestTheStartsAndTheGate(unittest.TestCase):

    def test_the_baseline_is_one_of_the_starts(self):
        """So the search cannot finish worse than what it is improving on."""
        edges = [(A, B), (B, C), (C, A), (D, E)]
        topo = [C, A, B, D, E, F]
        _order, info = mfas_order(edges, IDS, BORN, topo)
        self.assertIn("topological", info["starts"])
        self.assertLessEqual(info["violations"],
                             violations(topo, edges))

    def test_it_reports_which_start_won(self):
        edges = [(F, A)]
        _o, info = mfas_order(edges, IDS, BORN, list(IDS))
        self.assertIn(info["best_start"], ("born_at", "topological", "net_wins"))

    def test_net_wins_puts_the_biggest_winner_first(self):
        order = net_wins_order([(A, B), (A, C), (A, D)], IDS, BORN)
        self.assertEqual(order[0], A)

    def test_net_wins_breaks_ties_by_arrival(self):
        self.assertEqual(net_wins_order([], IDS, BORN), IDS)

    def test_the_gate_passes_when_the_search_matches_the_baseline(self):
        arm = {"topological": {"violations_of_the_declared_set": 24},
               "mfas": {"violations_of_the_declared_set": 5}}
        self.assertTrue(gate_beats_the_baseline(arm)["passes"])

    def test_the_gate_passes_on_a_tie(self):
        arm = {"topological": {"violations_of_the_declared_set": 5},
               "mfas": {"violations_of_the_declared_set": 5}}
        self.assertTrue(gate_beats_the_baseline(arm)["passes"])

    def test_the_gate_blocks_when_the_search_loses_to_the_baseline(self):
        """The failure that actually happened on the first run: 28 against 24 on
        the oracle's edges. A score difference would have been a fact about the
        search."""
        arm = {"topological": {"violations_of_the_declared_set": 24},
               "mfas": {"violations_of_the_declared_set": 28}}
        self.assertFalse(gate_beats_the_baseline(arm)["passes"])


if __name__ == "__main__":
    unittest.main()
