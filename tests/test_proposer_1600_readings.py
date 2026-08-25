"""
THE READINGS OF §0 — B-a, B-b, B-c, and the two figures that make them legible.

**No figure of `PLAN_PROPOSER_1600.md` is pinned here and none can be**: all four
rows need calls that have not been made. What is pinned is that each reading says
the right thing about a number it is handed, which is the part that must be
settled BEFORE the number exists — otherwise the arithmetic gets chosen once the
answer is visible, which is hard rule 6.

  * `B-a` is TWO-SIDED. It claims stability between budgets, so a rate far above
    the anchor refutes it exactly as one far below does. A one-sided reading would
    quietly convert "the proposer is the same instrument at both budgets" into
    "the proposer did not get worse", and only one of those is what §0 says.
  * `B-b` and `B-c` are strict and non-strict respectively, exactly as §0 writes
    them: `> 0.4824` and `>= 0.4981`. A band's edge is its own refutation line, so
    the two must not both be strict or both be loose.
  * The lines are transcribed from §0 and owned by two other records. If a record
    drifts, the gate says so and the band does not follow it.
  * On Stage D's 400 neither row is read at all: they are claims about the 1,600.
  * The presentation-position split is outside every denominator, and the
    positional rate is computed from `a_shown_as` rather than from the declared
    counts, which are a different question.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rung3.declared_order import (ABOUT, B_B_LINE, B_C_LINE, READING_DRAWS,
                                  READING_SEED, b_b_reading, b_c_reading,
                                  gate_lines_still_hold,
                                  not_the_population_for,
                                  oracle_directions_from_split)
from rung3.edge_direction import (B_A_ANCHOR, B_A_BAND, b_a_reading,
                                  direction_by_position)


def agr(rate, n=300):
    return {"rate": rate, "n": n, "surface": "better_space",
            "standard_error": round((0.25 / n) ** 0.5, 4)}


class TestBaIsTwoSided(unittest.TestCase):

    def test_the_anchor_itself_holds(self):
        self.assertTrue(b_a_reading(agr(B_A_ANCHOR))["band_holds"])

    def test_just_inside_the_band_below_holds(self):
        self.assertTrue(b_a_reading(agr(B_A_ANCHOR - B_A_BAND))["band_holds"])

    def test_just_inside_the_band_above_holds(self):
        self.assertTrue(b_a_reading(agr(B_A_ANCHOR + B_A_BAND))["band_holds"])

    def test_below_the_band_refutes(self):
        self.assertFalse(
            b_a_reading(agr(B_A_ANCHOR - B_A_BAND - 0.001))["band_holds"])

    def test_ABOVE_the_band_also_refutes(self):
        """The row claims STABILITY. A proposer that got much better between
        budgets is not the same instrument either, and a one-sided reading would
        hide it."""
        self.assertFalse(
            b_a_reading(agr(B_A_ANCHOR + B_A_BAND + 0.001))["band_holds"])

    def test_the_edge_is_inside_so_band_and_refutation_partition_the_axis(self):
        edge = b_a_reading(agr(B_A_ANCHOR + B_A_BAND))
        self.assertTrue(edge["band_holds"])
        self.assertEqual(edge["absolute_difference"], B_A_BAND)

    def test_an_empty_denominator_is_unadjudicable_rather_than_zero(self):
        r = b_a_reading({"rate": None, "n": 0, "surface": "better_space",
                         "standard_error": None})
        self.assertFalse(r["adjudicable"])

    def test_it_names_its_denominator(self):
        self.assertIn("strict better rule", b_a_reading(agr(0.7))["denominator"])


class TestBbAndBcReadTheirBandsExactly(unittest.TestCase):

    def test_b_b_is_strict_at_the_line(self):
        """§0 says `> 0.4824`, so the line itself is refutation, not a hold."""
        self.assertFalse(b_b_reading(B_B_LINE, B_B_LINE)["band_holds"])

    def test_b_b_holds_just_above(self):
        self.assertTrue(b_b_reading(B_B_LINE + 1e-6, B_B_LINE)["band_holds"])

    def test_b_c_is_not_strict_at_the_line(self):
        """§0 says `>= 0.4981`, so the line itself is a hold."""
        self.assertTrue(b_c_reading(B_C_LINE, None)["band_holds"])

    def test_b_c_refutes_just_below(self):
        self.assertFalse(b_c_reading(B_C_LINE - 1e-6, None)["band_holds"])

    def test_the_margin_is_signed_the_way_it_reads(self):
        self.assertLess(b_b_reading(0.40, B_B_LINE)["margin"], 0)
        self.assertGreater(b_b_reading(0.60, B_B_LINE)["margin"], 0)

    def test_b_c_survives_without_the_recomputed_baselines(self):
        """The signed line is enough to read the row; the recomputed figures make
        it legible and are not required for it."""
        r = b_c_reading(0.44, None)
        self.assertIn("band_holds", r)
        self.assertIsNone(r["read_against_this_sample"])

    def test_b_c_reports_the_gap_in_projection_deviations_when_it_can(self):
        recomputed = {"projection": {"mean": 0.50, "sd": 0.02},
                      "coin": {"mean": 0.45, "sd": 0.018}, "oracle": 0.55}
        r = b_c_reading(0.46, recomputed)
        self.assertEqual(
            r["read_against_this_sample"]["gap_in_projection_deviations"], -2.0)


class TestTheLinesAreTheSignedOnes(unittest.TestCase):
    """Transcribed from §0 before any figure of the plan existed."""

    def test_b_b_line(self):
        self.assertEqual(B_B_LINE, 0.4824)

    def test_b_c_line(self):
        self.assertEqual(B_C_LINE, 0.4981)

    def test_b_a_anchor_and_band(self):
        self.assertEqual((B_A_ANCHOR, B_A_BAND), (0.6978, 0.05))

    def test_the_reading_draws_are_declared_not_chosen_later(self):
        self.assertEqual((READING_DRAWS, READING_SEED), (200, 17))


class TestTheGateOnTheLines(unittest.TestCase):

    def row(self, noisy):
        return {"budget": 1600, "noisy_mean": noisy}

    def test_it_passes_when_both_records_still_say_it(self):
        self.assertTrue(
            gate_lines_still_hold(B_B_LINE, self.row(B_C_LINE))["passes"])

    def test_a_drifted_hierarchy_fails_it(self):
        self.assertFalse(
            gate_lines_still_hold(0.4900, self.row(B_C_LINE))["passes"])

    def test_a_drifted_projection_fails_it(self):
        self.assertFalse(
            gate_lines_still_hold(B_B_LINE, self.row(0.5100))["passes"])

    def test_a_missing_budget_row_fails_it_rather_than_passing_quietly(self):
        self.assertFalse(gate_lines_still_hold(B_B_LINE, None)["passes"])


class TestTheRowsAreNotReadOnTheWrongPopulation(unittest.TestCase):

    def test_the_reading_is_removed_and_the_figure_kept(self):
        block = b_b_reading(0.60, B_B_LINE)
        off = not_the_population_for(block, ABOUT)
        self.assertNotIn("band_holds", off)
        self.assertFalse(off["adjudicates"])
        self.assertEqual(off["measured"], block["measured"])

    def test_the_note_names_the_population_the_row_is_about(self):
        off = not_the_population_for(b_b_reading(0.60, B_B_LINE), ABOUT)
        self.assertIn("1,600", off["note"])


class TestTheOracleDirectionsAreRead(unittest.TestCase):
    """A pair the split record does not carry is not a tie. Folding the two
    together would shrink the projection's offers without saying so."""

    RECORD = "results2/pair_sample_1600.json"

    def rows(self, pairs):
        return [{"rule_a": a, "rule_b": b} for a, b in pairs]

    def test_the_real_record_covers_stage_ds_pairs_with_nothing_missing(self):
        answers = json.loads(
            Path("results2/pair_judgement_learned.json").read_text())["answers"]
        _dirs, missing = oracle_directions_from_split(answers, self.RECORD)
        self.assertEqual(missing, 0)

    def test_a_pair_outside_the_record_is_counted_as_missing(self):
        dirs, missing = oracle_directions_from_split(
            self.rows([("R9998", "R9999")]), self.RECORD)
        self.assertEqual(missing, 1)
        self.assertEqual(dirs, [None])

    def test_a_tie_is_not_counted_as_missing(self):
        tie = next(r for r in json.loads(Path(self.RECORD).read_text())["oracle"]
                   if r["better_space"] not in ("a", "b"))
        dirs, missing = oracle_directions_from_split(
            self.rows([(tie["rule_a"], tie["rule_b"])]), self.RECORD)
        self.assertEqual((dirs, missing), ([None], 0))

    def test_a_strict_verdict_becomes_a_direction(self):
        strict = next(r for r in json.loads(Path(self.RECORD).read_text())["oracle"]
                      if r["better_space"] == "a")
        dirs, _ = oracle_directions_from_split(
            self.rows([(strict["rule_a"], strict["rule_b"])]), self.RECORD)
        self.assertEqual(dirs, [True])


class TestThePresentationPosition(unittest.TestCase):

    def rows(self, spec):
        """(declared, a_shown_as, better_space)."""
        return [{"declared": d, "a_shown_as": p, "better_space": v,
                 "rule_a": f"R{k}", "rule_b": f"S{k}"}
                for k, (d, p, v) in enumerate(spec)]

    def test_a_winner_always_shown_first_is_a_rate_of_one(self):
        rows = self.rows([("a_beats_b", "A", "a"), ("b_beats_a", "B", "b")])
        r = direction_by_position(rows, "better_space")
        self.assertEqual(r["rate_first"], 1.0)
        self.assertEqual(r["winner_shown_second"], 0)

    def test_a_winner_always_shown_second_is_a_rate_of_zero(self):
        rows = self.rows([("a_beats_b", "B", "a"), ("b_beats_a", "A", "b")])
        r = direction_by_position(rows, "better_space")
        self.assertEqual(r["rate_first"], 0.0)

    def test_pairs_with_no_edge_are_outside_it(self):
        rows = self.rows([("a_beats_b", "A", "a"), ("none", "A", "a")])
        self.assertEqual(direction_by_position(rows, "better_space")["n_edges"],
                         1)

    def test_the_declared_counts_are_a_different_question_from_position(self):
        """Stage D's 203/162 is about which RULE won; the positional rate is
        about where it was shown. A sample can be lopsided in one and balanced
        in the other, and conflating them is how the asymmetry stayed
        unexplained."""
        rows = self.rows([("b_beats_a", "A", "b"), ("b_beats_a", "B", "b")])
        r = direction_by_position(rows, "better_space")
        self.assertEqual(r["declared_counts"], {"b_beats_a": 2})
        self.assertEqual(r["rate_first"], 0.5)

    def test_it_is_outside_every_denominator_and_says_so(self):
        rows = self.rows([("a_beats_b", "A", "a")])
        r = direction_by_position(rows, "better_space")
        self.assertIn("No row of §0 predicts it",
                      r["outside_every_denominator"])


if __name__ == "__main__":
    unittest.main()
