"""
THE SENSITIVITY INSTRUMENT — its bands, its grid and its parity. No figure of the
sweep is pinned here.

`results_sensitivity/FINDINGS_SENSITIVITY.md` owns the five rows and the curve.
Repeating any of them here would give a figure a second owner, which is the
failure `tests/test_floor_by_pool.py` names and `IDEAS.md` carries as debt. What
is pinned instead is everything that would let a figure move without anyone
noticing:

  * **the five bands**, as named constants — §7 of the plan asks for exactly this,
    *"in the way `tests/test_declared_order.py` pins `P_D_MARGIN` and
    `P_E_BAND`, so that moving a band after seeing a figure is visible in a
    diff"*. Two of them are the lines Sergi tightened at signature time;
  * **the two constants §8 fixes**, `SWEEP_SEED` and `SWEEP_DRAWS`;
  * **the ρ grid**, which the plan left to the executor and three rows depend on:
    that it is 13 centres, that it contains ρ = 0 and the hidden policy's own ρ,
    that no two bins overlap, and that `RHO_HIDDEN` still equals what the
    generator computes from the material rather than a transcribed number;
  * **`A-g3`'s parity**, which is the whole licence for the fast path: the
    bitmask evaluation must return what the frozen `RuleEngine` returns on the
    hidden policy, field by field;
  * **the second implementation of the operator semantics.** `CorpusUniverse`
    repeats `Space`'s `condition_mask`, and a second implementation is a second
    place to be wrong, so it is checked against `Condition.holds` directly;
  * **the gate**, including the thing that made it necessary: it must count the
    signatures rather than stop at the first, because §0 is signed and §1's
    amendment carries its own.

Nothing here calls a `main()`, so nothing here writes to `results_sensitivity/`.
"""

from __future__ import annotations

import random
import unittest
from pathlib import Path

from harness.ceiling_check import build_rules, measure as harness_measure
from harness.dsl import Condition, RuleEngine
from sensitivity import generator as g
from sensitivity import measure as m
from sensitivity import sweep as sw
from sensitivity.generator_check import a_g4

from .fixtures import corpus, space

REPO = Path(__file__).resolve().parent.parent

# --- the signed bands, transcribed from §0 of PLAN_SENSITIVITY.md ------------
BANDS = {"A_A_CENTRAL": 0.90, "A_B_MIN_SPEARMAN": 0.85, "A_C_MAX_MEDIAN": 0.95,
         "A_D_MIN_FRACTION": 0.60, "A_E_MAX_DIFFERENCE": 0.15}
# --- the two constants §8 fixes ----------------------------------------------
SWEEP_SEED, SWEEP_DRAWS = 17, 100
# --- the grid the executor declared ------------------------------------------
N_BINS, TOLERANCE = 13, 0.02


class TestTheSignedBands(unittest.TestCase):
    """If one of these fails, a band moved. That is hard rule 6 and the diff is
    the point of this class."""

    def test_the_five_bands_are_the_signed_ones(self):
        for name, value in BANDS.items():
            with self.subTest(name):
                self.assertEqual(getattr(sw, name), value)

    def test_A_b_and_A_d_carry_the_tightened_lines(self):
        """Sergi tightened these two at signature time: `A-b` from 0.80 and `A-d`
        from 0.50. Both moves made the row harder to hold."""
        self.assertEqual(sw.A_B_MIN_SPEARMAN, 0.85)
        self.assertEqual(sw.A_D_MIN_FRACTION, 0.60)

    def test_the_two_constants_of_section_8(self):
        self.assertEqual(sw.SWEEP_SEED, SWEEP_SEED)
        self.assertEqual(sw.SWEEP_DRAWS, SWEEP_DRAWS)

    def test_the_bands_are_read_on_the_declared_surface_and_encoding(self):
        self.assertEqual(sw.BAND_SURFACE, "space")
        self.assertEqual(sw.BAND_ENCODING, m.PUBLISHED)


class TestTheRhoGrid(unittest.TestCase):
    """The plan fixes 13 bins and leaves the centres to the executor. Three rows
    depend on them, so they are pinned rather than adjustable."""

    def test_thirteen_centres(self):
        self.assertEqual(len(g.RHO_BINS), N_BINS)
        self.assertEqual(g.RHO_TOLERANCE, TOLERANCE)

    def test_it_contains_zero_and_the_hidden_policys_own_rho(self):
        """`A-d` is read at the ρ = 0 bin and `A-a` at the bin containing the
        hidden policy. On a round grid the second would fall into no bin at all."""
        self.assertIn(0.0, g.RHO_BINS)
        self.assertIn(g.RHO_HIDDEN, g.RHO_BINS)

    def test_no_two_bins_overlap(self):
        """A draw must belong to at most one bin, or the same policy would be
        counted at two values of the knob."""
        ordered = sorted(g.RHO_BINS)
        for a, b in zip(ordered, ordered[1:]):
            with self.subTest(f"{a} vs {b}"):
                self.assertGreater(b - a, 2 * g.RHO_TOLERANCE)

    def test_RHO_HIDDEN_is_what_the_material_gives(self):
        """The constant is a convenience; the material is the authority. This is
        what stops the grid from drifting away from the policy it is anchored
        on."""
        self.assertAlmostEqual(g.hidden_member().rho, g.RHO_HIDDEN, places=6)

    def test_rho_is_against_the_layer_index_and_not_the_rule_index(self):
        """−0.18 is the rule-index statistic and −0.1532 the layer-index one. §1
        defines the second; getting this backwards would move `A-a`'s bin."""
        by_rule = g.spearman(list(range(g.N_RULES)), list(g.COUNTS))
        self.assertAlmostEqual(by_rule, -0.1795, places=4)
        self.assertNotAlmostEqual(by_rule, g.RHO_HIDDEN, places=3)


class TestParityWithTheFrozenEngine(unittest.TestCase):
    """`A-g3`. Without it `A-a` compares two measurement paths and means
    nothing."""

    @classmethod
    def setUpClass(cls):
        cls.universe = m.CorpusUniverse()
        cls.hidden = g.hidden_member()
        cls.ext = [cls.universe.extension(list(r.conditions))
                   for r in cls.hidden.rules]
        cls.truth = g.truth_masks(cls.hidden, cls.ext, cls.universe.full)
        cls.mine = m.score(
            m.verdict(cls.hidden, cls.ext,
                      m.specificities(cls.hidden, m.PUBLISHED), cls.universe.full),
            cls.truth, cls.universe.n)
        engine = RuleEngine()
        engine.rules = build_rules()
        cls.theirs = harness_measure(list(corpus()), engine.decide, "frozen")

    def test_the_split_and_the_errors_agree_field_by_field(self):
        for field in ("action", "conflict", "impasse", "silent_errors_abs"):
            with self.subTest(field):
                self.assertEqual(self.mine[field], self.theirs[field])

    def test_the_rates_agree(self):
        for field in ("coverage", "accuracy_end_to_end", "silent_error_rate"):
            with self.subTest(field):
                self.assertAlmostEqual(self.mine[field], self.theirs[field],
                                       places=10)

    def test_the_policys_own_truth_is_the_hidden_policys(self):
        """The family scores each member against its own first-match-wins. For
        the hidden member that must be the oracle's labelling, or `A-g3` would be
        comparing the right numbers computed from the wrong truth."""
        from harness.hidden_policy import true_action

        for i, case in enumerate(corpus()):
            bit = self.universe.n - 1 - i
            action = next(a for a, mask in self.truth.items()
                          if (mask >> bit) & 1)
            self.assertEqual(action, true_action(case))


class TestTheCorpusUniverse(unittest.TestCase):
    """A second implementation of the operator semantics is a second place to get
    them wrong, so it is checked against the DSL rather than against `Space`."""

    @classmethod
    def setUpClass(cls):
        cls.universe = m.CorpusUniverse()

    def test_every_condition_in_the_vocabulary_masks_what_the_DSL_holds(self):
        cases = list(corpus())
        for triple in g.VOCABULARY:
            with self.subTest(triple):
                cond = g._as_condition(triple)
                mask = self.universe.condition_mask(cond)
                for i, case in enumerate(cases):
                    bit = (mask >> (self.universe.n - 1 - i)) & 1
                    self.assertEqual(bool(bit), cond.holds(case))

    def test_it_is_one_bit_per_draw_and_not_per_distinct_case(self):
        """The corpus is a distribution and its duplicates are part of it."""
        self.assertEqual(self.universe.n, m.N_CORPUS)
        self.assertGreater(self.universe.n, len({tuple(vars(c).values())
                                                 for c in corpus()}))


class TestTheGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rng = random.Random(SWEEP_SEED)
        cls.drawn = []
        for centre in (g.RHO_BINS[0], 0.0, g.RHO_BINS[-1]):
            while True:
                try:
                    cls.drawn.append((centre, *g.draw(rng, centre, space())))
                    break
                except g.DeadEnd:
                    continue

    def test_the_vocabulary_is_the_manuals_own_minus_the_catch_all(self):
        self.assertEqual(len(g.VOCABULARY), 23)
        self.assertNotIn(g.CATCHALL_CONDITION, g.VOCABULARY)

    def test_the_body_space_is_enumerated_and_not_sampled(self):
        """Rejection sampling reported `impossible` for merely rare, deep in a
        policy where only a handful of the 217 two-condition bodies qualify."""
        self.assertEqual([len(g.bodies(k)) for k in (1, 2, 3)], [23, 217, 1083])

    def test_A_g2_every_draw_lands_in_its_bin(self):
        for centre, policy, _ext in self.drawn:
            with self.subTest(centre):
                self.assertLessEqual(abs(policy.rho - centre), g.RHO_TOLERANCE)

    def test_A_g4_every_rule_is_live_and_the_catch_all_is_last(self):
        for centre, policy, ext in self.drawn:
            with self.subTest(centre):
                verdict = a_g4(policy, ext, space())
                self.assertEqual(verdict["dead_rules"], [])
                self.assertEqual(verdict["effective_size"], g.N_RULES)
                self.assertTrue(verdict["catch_all_is_last"])
                self.assertTrue(verdict["passes"])

    def test_the_counts_and_actions_are_the_hidden_policys_multisets(self):
        for centre, policy, _ext in self.drawn:
            with self.subTest(centre):
                self.assertEqual(sorted(policy.counts), sorted(g.COUNTS))
                self.assertEqual(sorted(policy.actions), sorted(g.ACTIONS))

    def test_a_dead_end_is_raised_and_not_swallowed(self):
        """The construction can genuinely paint itself into a corner, and that has
        to reach the caller as a rejected draw rather than as a policy with a dead
        rule."""
        self.assertTrue(issubclass(g.DeadEnd, RuntimeError))


class TestRequiredInequalities(unittest.TestCase):
    """`A-d`'s counter, on an instance small enough to check by hand."""

    def setUp(self):
        self.space = space()

    # Positions 0, 1 and 2 are all in layer 0 — `LAYER_SIZES[0]` is 3 — so a
    # two-rule instance has no cross-layer pair at all and would silently test
    # nothing. The pair under test is therefore at positions 0 and 3, with two
    # fillers between them that are disjoint from everything.
    FILLERS = [((("product", "eq", "mobile"),), "T1_GENERAL"),
               ((("product", "eq", "mobile"),), "T1_GENERAL")]

    def _policy(self, specs):
        rules = tuple(g.Rule(rule_id=f"X{i}",
                             conditions=tuple(g._as_condition(t) for t in conds),
                             action=action)
                      for i, (conds, action) in enumerate(specs))
        return g.Policy(rules=rules, rho=0.0)

    def _pair(self, first, second):
        return self._policy([first] + self.FILLERS + [second])

    def test_a_pair_that_needs_an_inequality_and_violates_it(self):
        """Layer 0 gets one condition, layer 1 gets two, they overlap and they
        disagree: specificity needs count(earlier) > count(later) and 1 > 2 is
        false."""
        pol = self._pair(
            ((("product", "eq", "api"),), "T2_TECHNICAL"),
            ((("product", "eq", "api"), ("severity", "lte", 2)), "T3_ENGINEERING"))
        ext = [self.space.extension(list(r.conditions)) for r in pol.rules]
        out = m.required_inequalities(pol, ext)
        self.assertEqual(out["required"], 1)
        self.assertEqual(out["violated"], 1)
        self.assertTrue(out["any_violation"])

    def test_same_action_needs_nothing(self):
        pol = self._pair(
            ((("product", "eq", "api"),), "T2_TECHNICAL"),
            ((("product", "eq", "api"), ("severity", "lte", 2)), "T2_TECHNICAL"))
        ext = [self.space.extension(list(r.conditions)) for r in pol.rules]
        self.assertEqual(m.required_inequalities(pol, ext)["required"], 0)

    def test_disjoint_needs_nothing(self):
        pol = self._pair(
            ((("product", "eq", "api"),), "T2_TECHNICAL"),
            ((("product", "eq", "billing"),), "BILLING_SPECIALIST"))
        ext = [self.space.extension(list(r.conditions)) for r in pol.rules]
        self.assertEqual(m.required_inequalities(pol, ext)["required"], 0)

    def test_same_layer_is_not_a_layer_relation(self):
        """Positions 0 and 1 are both in layer 0, so the pair is outside §2's
        definition however it is shaped."""
        pol = self._policy([
            ((("product", "eq", "api"),), "T2_TECHNICAL"),
            ((("severity", "lte", 2),), "T3_ENGINEERING"),
        ])
        ext = [self.space.extension(list(r.conditions)) for r in pol.rules]
        self.assertEqual(g.POSITION_LAYER[0], g.POSITION_LAYER[1])
        self.assertNotEqual(g.POSITION_LAYER[0], g.POSITION_LAYER[3])
        self.assertEqual(m.required_inequalities(pol, ext)["required"], 0)


class TestTheGate(unittest.TestCase):
    """§8. What it protects is not money: it is that the bands were signed before
    the figures existed."""

    def test_it_passes_on_the_real_plan(self):
        gate = sw.gate_signature(REPO / "PLAN_SENSITIVITY.md")
        self.assertTrue(gate["passes"])
        self.assertGreaterEqual(gate["found"], sw.MIN_SIGNATURES)
        self.assertEqual(gate["unsigned"], [])

    def test_it_counts_the_signatures_instead_of_stopping_at_the_first(self):
        """The failure this exists to prevent: §0 signed, §1's amendment not, and
        a gate that reads only the first reports `ok` over an unsigned plan."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("**Signed by Sergi: yes (date: x)**\n"
                         "**Signed by Sergi: ________ (date: ______)**\n")
            gate = sw.gate_signature(p)
            self.assertEqual(gate["found"], 2)
            self.assertFalse(gate["passes"])

    def test_one_signature_is_not_enough(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("**Signed by Sergi: yes (date: x)**\n")
            self.assertFalse(sw.gate_signature(p)["passes"])

    def test_a_signature_indented_into_a_blockquote_is_invisible(self):
        """Which is why §1's line sits outside the quotation, and why the plan
        says so where the line is."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("> **Signed by Sergi: yes (date: x)**\n")
            self.assertEqual(sw.gate_signature(p)["found"], 0)

    def test_a_missing_plan_does_not_pass(self):
        self.assertFalse(sw.gate_signature(Path("/nonexistent/PLAN.md"))["passes"])


class TestTheCentralBandConvention(unittest.TestCase):
    """`A-a`'s band. A percentile convention chosen after seeing where the hidden
    policy lands is a band chosen after the fact."""

    def test_it_excludes_five_draws_at_each_end_of_a_hundred(self):
        lo, hi, k = sw.central_band(list(range(100)))
        self.assertEqual((lo, hi, k), (5, 94, 5))

    def test_inside_is_inclusive(self):
        lo, hi, _k = sw.central_band([float(i) for i in range(100)])
        self.assertTrue(lo <= lo <= hi and lo <= hi <= hi)


if __name__ == "__main__":
    unittest.main()
