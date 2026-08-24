"""
COMPILING THE DECLARED EDGES INTO AN ORDER — the part that could silently
misadjudicate P-d.

`declared_order` scores what Stage D's edges do. **No figure of that is pinned
here**: what the order scores, what the engine's e2e and silent error are, and
where P-d and P-e land live in `results3/declared_order.json` and in the
write-up. The bands themselves are declared constants of the module, transcribed
from a signed §0.

What is pinned is the compilation, because it is the step where a wrong answer
would look right. If the topological sort dropped an edge, or drained its ready
set by something other than arrival, P-d would be adjudicated on an order the
edges did not induce — and every figure downstream would still print.

  * every accepted edge places its winner before its loser;
  * a rule no edge touches keeps its arrival position, which is what makes the
    comparison against the `born_at` floor mean "what the edges added";
  * the gate detects a broken edge rather than trusting the sort;
  * `rules_moved_off_arrival` counts what actually moved, so a run that moved
    nothing cannot read like one that moved everything.
"""

from __future__ import annotations

import unittest

from rung3.declared_order import (P_D_MARGIN, P_E_BAND,
                                  gate_order_respects_edges, rules_moved,
                                  topological_order)

IDS = [f"R{i:04d}" for i in range(1, 7)]
BORN = {rid: i for i, rid in enumerate(IDS)}


class TestTheCompiledOrder(unittest.TestCase):

    def test_with_no_edges_it_is_exactly_arrival_order(self):
        """`born_at` IS the floor P-d is measured against, so an empty edge set
        must reproduce it exactly. Anything else would make the comparison read
        a difference the edges did not cause."""
        self.assertEqual(topological_order(IDS, [], BORN),
                         sorted(IDS, key=lambda r: BORN[r]))

    def test_one_edge_moves_its_loser_behind_its_winner(self):
        order = topological_order(IDS, [("R0003", "R0001")], BORN)
        self.assertLess(order.index("R0003"), order.index("R0001"))

    def test_a_rule_no_edge_touches_keeps_its_arrival_position(self):
        order = topological_order(IDS, [("R0006", "R0005")], BORN)
        for rid in ("R0001", "R0002", "R0003", "R0004"):
            with self.subTest(rid):
                self.assertEqual(order.index(rid), BORN[rid])

    def test_ties_are_drained_by_arrival_and_not_by_identifier_luck(self):
        order = topological_order(IDS, [("R0002", "R0004")], BORN)
        self.assertEqual(order[0], "R0001")
        self.assertLess(order.index("R0002"), order.index("R0004"))

    def test_it_is_a_permutation_of_the_rules(self):
        order = topological_order(IDS, [("R0005", "R0002"), ("R0004", "R0001")],
                                  BORN)
        self.assertEqual(sorted(order), sorted(IDS))

    def test_a_chain_comes_out_in_the_chains_own_direction(self):
        edges = [("R0006", "R0005"), ("R0005", "R0004"), ("R0004", "R0003")]
        order = topological_order(IDS, edges, BORN)
        for w, loser in edges:
            with self.subTest(f"{w}>{loser}"):
                self.assertLess(order.index(w), order.index(loser))

    def test_a_duplicated_edge_does_not_break_the_degree_count(self):
        edges = [("R0004", "R0002"), ("R0004", "R0002")]
        order = topological_order(IDS, edges, BORN)
        self.assertEqual(sorted(order), sorted(IDS))
        self.assertLess(order.index("R0004"), order.index("R0002"))

    def test_every_rule_survives_even_if_a_cycle_slipped_in(self):
        """`try_edge` refuses cycles, so this cannot arrive — but if it did, the
        leftovers are appended in arrival order and the gate reports the broken
        edges instead of the run dying with a plausible-looking order."""
        edges = [("R0002", "R0003"), ("R0003", "R0002")]
        order = topological_order(IDS, edges, BORN)
        self.assertEqual(sorted(order), sorted(IDS))


class TestTheEdgeGate(unittest.TestCase):

    def test_it_passes_on_an_order_the_edges_induce(self):
        edges = [("R0004", "R0002"), ("R0006", "R0001")]
        g = gate_order_respects_edges(topological_order(IDS, edges, BORN), edges)
        self.assertTrue(g["passes"])
        self.assertEqual(g["n_edges"], 2)

    def test_it_catches_an_order_that_breaks_one(self):
        edges = [("R0004", "R0002")]
        g = gate_order_respects_edges(sorted(IDS, key=lambda r: BORN[r]), edges)
        self.assertFalse(g["passes"])
        self.assertEqual(g["broken"], [["R0004", "R0002"]])

    def test_it_counts_every_broken_edge(self):
        edges = [("R0004", "R0002"), ("R0005", "R0003"), ("R0006", "R0001")]
        g = gate_order_respects_edges(sorted(IDS, key=lambda r: BORN[r]), edges)
        self.assertEqual(g["n_broken"], 3)

    def test_an_empty_edge_set_passes_trivially(self):
        g = gate_order_respects_edges(list(IDS), [])
        self.assertTrue(g["passes"])
        self.assertEqual(g["n_edges"], 0)


class TestHowMuchActuallyMoved(unittest.TestCase):

    def test_nothing_moves_without_edges(self):
        self.assertEqual(rules_moved(topological_order(IDS, [], BORN), BORN,
                                     IDS), 0)

    def test_a_swap_moves_two(self):
        order = topological_order(IDS, [("R0002", "R0001")], BORN)
        self.assertEqual(rules_moved(order, BORN, IDS), 2)

    def test_it_counts_positions_and_not_edges(self):
        """One edge that drags a rule across the base moves many positions. A
        run that moved nothing must not read like one that moved everything."""
        order = topological_order(IDS, [("R0006", "R0001")], BORN)
        self.assertGreater(rules_moved(order, BORN, IDS), 1)


class TestTheBandsAreTheSignedOnes(unittest.TestCase):
    """Transcribed from §0. If either moves, somebody adjusted a signed row."""

    def test_p_d_margin(self):
        self.assertEqual(P_D_MARGIN, 0.03)

    def test_p_e_band(self):
        self.assertEqual(P_E_BAND, 0.25)


if __name__ == "__main__":
    unittest.main()
