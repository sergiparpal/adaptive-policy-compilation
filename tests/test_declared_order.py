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

from pathlib import Path

from rung3.declared_order import (DIRECTION_SEED, N_DIRECTION_DRAWS, OUT,
                                  P_D_MARGIN, P_E_BAND, RECORD, SOURCE,
                                  accepted_from, direction_controls,
                                  fresh_engine, gate_order_respects_edges,
                                  not_adjudicated_here, parse_source,
                                  reset_declared,
                                  rules_moved, topological_order)

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


class TestTheDirectionControl(unittest.TestCase):
    """
    The line that separates `the model chose badly` from `compiling any edges
    this way hurts`. A single low score cannot tell them apart, and without this
    the whole reading of P-d's refutation would rest on an assumption.

    Everything below is on four rules written out by hand, so no figure of the
    finding appears here.
    """

    def rules(self):
        """
        Extensions that OVERLAP without either containing the other, which is
        what the real population requires. The first version of this fixture
        built nested ones — `severity gte k` for increasing k — and `try_edge`
        answered `contradice_subsuncion` one way and a redundant `ok` the other,
        so the forward direction accepted nothing. Those are exactly the pairs
        §10 filters out, and building the control on them tested nothing.
        """
        from harness.dsl import Condition
        from rung2.engine2 import Rule2 as R

        shapes = [("gte", 2, "AAA"), ("lte", 3, "BBB")]
        out = {}
        for i, rid in enumerate(IDS):
            op, value, act = shapes[i % 2]
            out[rid] = R(rule_id=rid, action=act, born_at=i,
                         conditions=[Condition("severity", op, value)])
        return out

    def rows(self):
        return [{"rule_a": "R0001", "rule_b": "R0002", "declared": "a_beats_b"},
                {"rule_a": "R0003", "rule_b": "R0004", "declared": "b_beats_a"}]

    def test_the_edges_follow_the_directions_given(self):
        rules = self.rules()
        fwd = accepted_from(self.rows(), [True, True], rules)
        back = accepted_from(self.rows(), [False, False], rules)
        self.assertEqual(fwd, [(lo, w) for w, lo in back])

    def test_it_runs_the_edges_through_try_edge_and_not_around_it(self):
        """A self-edge is refused, so it must not reach the compiled order. If
        the control installed edges any other way it would not be comparable
        with the run, where cycles are refused as they arrive."""
        rules = self.rules()
        same = [{"rule_a": "R0001", "rule_b": "R0001", "declared": "a_beats_b"}]
        self.assertEqual(accepted_from(same, [True], rules), [])

    def test_the_three_readings_are_all_present(self):
        rules = self.rules()
        inst = ({r: 0 for r in IDS}, {r: 0 for r in IDS}, 0, 1)
        c = direction_controls(self.rows(), rules, IDS, BORN, inst, n_draws=3)
        for k in ("model", "model_inverted", "coin"):
            self.assertIn(k, c)
        self.assertEqual(c["n_draws"], 3)
        self.assertEqual(c["n_pairs"], 2)

    def test_the_coin_is_read_in_its_own_deviations(self):
        """A gap without the spread beside it is unreadable, which is the whole
        lesson of the random-baseline rows in FINDINGS3."""
        rules = self.rules()
        inst = ({r: 0 for r in IDS}, {r: 0 for r in IDS}, 0, 1)
        c = direction_controls(self.rows(), rules, IDS, BORN, inst, n_draws=3)
        self.assertIn("sd", c["coin"])
        self.assertIn("model_in_coin_deviations", c)
        self.assertIn("inverted_in_coin_deviations", c)

    def test_it_is_deterministic(self):
        rules = self.rules()
        inst = ({r: 0 for r in IDS}, {r: 0 for r in IDS}, 0, 1)
        a = direction_controls(self.rows(), rules, IDS, BORN, inst, n_draws=4)
        b = direction_controls(self.rows(), rules, IDS, BORN, inst, n_draws=4)
        self.assertEqual(a, b)

    def test_a_reset_engine_is_indistinguishable_from_a_fresh_one(self):
        """The optimisation that makes a 2,000-draw null affordable, and the
        only way it could be wrong: `try_edge` mutates `decl_below` and
        `decl_above` and nothing else, so clearing them must be the identity.
        If it ever stopped being one, every null in this thread would be
        computed on an engine carrying somebody else's edges."""
        rules = self.rules()
        engine = fresh_engine(rules)
        for dirs in ([True, True], [False, False], [True, False]):
            with self.subTest(dirs=dirs):
                fresh = accepted_from(self.rows(), dirs, rules)
                reused = accepted_from(self.rows(), dirs, rules, engine)
                self.assertEqual(fresh, reused)

    def test_the_reset_leaves_subsumption_alone(self):
        rules = self.rules()
        engine = fresh_engine(rules)
        before = {r: set(v) for r, v in engine.sub_below.items()}
        accepted_from(self.rows(), [True, True], rules, engine)
        reset_declared(engine)
        self.assertEqual(engine.sub_below, before)
        self.assertEqual({r for r, v in engine.decl_below.items() if v}, set())

    def test_a_reused_engine_does_not_carry_the_previous_draws_edges(self):
        """Without the reset the second call would see the first call's graph
        and refuse edges as cycles that are not."""
        rules = self.rules()
        engine = fresh_engine(rules)
        first = accepted_from(self.rows(), [True, True], rules, engine)
        second = accepted_from(self.rows(), [True, True], rules, engine)
        self.assertEqual(first, second)

    def test_the_constants_are_the_repositorys_own(self):
        self.assertEqual(N_DIRECTION_DRAWS, 50)
        self.assertEqual(DIRECTION_SEED, 17)


class TestTheBandsAreTheSignedOnes(unittest.TestCase):
    """Transcribed from §0. If either moves, somebody adjusted a signed row."""

    def test_p_d_margin(self):
        self.assertEqual(P_D_MARGIN, 0.03)

    def test_p_e_band(self):
        self.assertEqual(P_E_BAND, 0.25)


class TestTheSourceAndItsDestination(unittest.TestCase):
    """`PLAN_PROPOSER_1600.md` scores a second population with this same code —
    rule C of its §4 — and the closed thread's record must stay out of reach."""

    def test_no_arguments_reads_and_writes_the_closed_thread(self):
        source, out, is_stage_d = parse_source([])
        self.assertEqual(source, SOURCE)
        self.assertEqual(out, OUT / RECORD)
        self.assertTrue(is_stage_d)

    def test_another_source_without_a_destination_aborts(self):
        with self.assertRaises(SystemExit):
            parse_source(["--source", "results2/pair_judgement_1600.json"])

    def test_another_source_with_a_destination_is_not_stage_d(self):
        source, out, is_stage_d = parse_source(
            ["--source", "results2/pair_judgement_1600.json",
             "--out", "results3/declared_order_1600.json"])
        self.assertEqual(source, Path("results2/pair_judgement_1600.json"))
        self.assertEqual(out, Path("results3/declared_order_1600.json"))
        self.assertFalse(is_stage_d)

    def test_the_closed_source_may_be_written_elsewhere(self):
        source, out, is_stage_d = parse_source(["--out", "/tmp/scratch.json"])
        self.assertEqual(source, SOURCE)
        self.assertTrue(is_stage_d)


class TestASignedRowIsNotReAdjudicated(unittest.TestCase):
    """P-d and P-e were signed in §0 of `PLAN_PAIRWISE.md` and adjudicated on
    Stage D's 400 pairs. The same code on a bigger population produces the same
    number shaped like a verdict, and a record that printed it as one would let a
    row be re-adjudicated by rerunning it on more data."""

    BLOCK = {"row": "P-d", "band": "> floor + 0.03", "measured": 0.52,
             "threshold": 0.4632, "verdict": "HOLDS"}

    def test_the_word_verdict_is_gone(self):
        self.assertNotIn("verdict", not_adjudicated_here(self.BLOCK))

    def test_the_figure_stays(self):
        out = not_adjudicated_here(self.BLOCK)
        self.assertEqual(out["measured"], 0.52)
        self.assertEqual(out["threshold"], 0.4632)

    def test_it_still_says_which_side_of_the_line_it_fell(self):
        """Withholding the verdict is not withholding the reading."""
        self.assertTrue(not_adjudicated_here(self.BLOCK)["above_the_threshold"])
        below = dict(self.BLOCK, verdict="REFUTED")
        self.assertFalse(not_adjudicated_here(below)["above_the_threshold"])

    def test_it_names_the_row_and_where_it_was_adjudicated(self):
        note = not_adjudicated_here(self.BLOCK)["note"]
        self.assertIn("P-d", note)
        self.assertIn("PLAN_PAIRWISE.md", note)
        self.assertFalse(not_adjudicated_here(self.BLOCK)["adjudicates"])


if __name__ == "__main__":
    unittest.main()
