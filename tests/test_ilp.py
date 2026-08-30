"""
THE ILP INSTRUMENT — its bands, its language, its gate. No figure of the four
rows is pinned here.

`results_ilp/FINDINGS_ILP.md` owns them. What is pinned is everything that would
let one move without anyone noticing:

  * **the four signed bands**, as named constants — §7 of the plan asks for this
    in the way `tests/test_declared_order.py` pins `P_D_MARGIN`;
  * **the declared language**: 224 conditions, and the 29 hidden rules inside it,
    which is `I-g2` and the reason the `in` restriction of §2 is not free;
  * **`I-g3`'s no-leak property**, checked on the inducer's signature and on what
    its module imports;
  * **the gate**, including that it counts signatures instead of stopping at the
    first — §0's table and §1's amendment each carry one;
  * **first-match-wins**, on a list small enough to check by hand, because every
    figure in the record is produced by that one function.

Nothing here calls a `main()`, so nothing here writes to `results_ilp/`. Nothing
here needs `clingo`: the inducer runs on the standard library and the solver is
only needed to reproduce the superseded encoding.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL
from ilp import compare as cmp
from ilp import induce as ind
from ilp import instances as inst
from ilp import language as lang

REPO = Path(__file__).resolve().parent.parent

N_CONDITIONS = 224
BANDS = {"I_A_MIN": 0.8530, "I_C_MIN": 0.50, "I_D_MAX": 58}
BEAMS = (40, 120)


class TestTheSignedBands(unittest.TestCase):
    """If one of these fails, a band moved. That is hard rule 6."""

    def test_the_four_bands_are_the_signed_ones(self):
        for name, value in BANDS.items():
            with self.subTest(name):
                self.assertEqual(getattr(cmp, name), value)

    def test_I_b_reads_the_learned_bases_own_per_class_ceiling(self):
        """39 of 117 and 39 of 109, owned by results3/FINDINGS3.md §2. Not a
        round number anyone chose: it is what the 577 rules can do."""
        self.assertAlmostEqual(cmp.I_B_CEILING["T3_ENGINEERING"], 39 / 117)
        self.assertAlmostEqual(cmp.I_B_CEILING["ACCOUNT_MANAGER"], 39 / 109)

    def test_the_beams_are_declared_and_there_are_two(self):
        """`I-g4`: a row whose verdict changes between them is not a verdict."""
        self.assertEqual(ind.BEAM_WIDTHS, BEAMS)


class TestTheLanguage(unittest.TestCase):

    def test_it_is_the_declared_size(self):
        self.assertEqual(len(lang.language()), N_CONDITIONS)

    def test_no_duplicates(self):
        self.assertEqual(len(set(lang.language())), N_CONDITIONS)

    def test_I_g2_every_hidden_condition_is_in_it(self):
        """The check §2 says is not free: `customer_tier` has FOUR values, so
        `in [business, enterprise]` is not `neq free`, and dropping `in` would
        put the target outside the language."""
        index = set(lang.language())
        for rid, conds, _action in HIDDEN_DSL:
            for attr, op, value in conds:
                key = (attr, op, tuple(value) if isinstance(value, list) else value)
                with self.subTest(f"{rid} {attr} {op}"):
                    self.assertIn(key, index)

    def test_the_in_operator_is_what_makes_that_true(self):
        without_in = {t for t in lang.language() if t[1] != "in"}
        self.assertNotIn(("customer_tier", "in", ("business", "enterprise")),
                         without_in)
        self.assertIn(("customer_tier", "in", ("business", "enterprise")),
                      set(lang.language()))

    def test_bodies_are_capped_at_the_hidden_policys_own_maximum(self):
        self.assertEqual(lang.MAX_CONDITIONS,
                         max(len(c) for _r, c, _a in HIDDEN_DSL))


class TestNoLeak(unittest.TestCase):
    """`I-g3`. The inducer sees masks and nothing else."""

    def test_the_signature_takes_only_masks(self):
        import inspect

        params = list(inspect.signature(ind.induce).parameters)
        self.assertEqual(params[:3], ["ext", "truth", "n"])

    def test_the_module_imports_nothing_from_the_oracle_or_the_run(self):
        source = Path(ind.__file__).read_text()
        for name in ("hidden_policy", "true_action", "true_rule_id", "llm_run",
                     "HIDDEN_DSL"):
            with self.subTest(name):
                self.assertNotIn(f"import {name}", source)

    def test_it_does_not_import_the_instances_either(self):
        """Which is what stops it from reaching the test split or the run
        record through a side door."""
        source = Path(ind.__file__).read_text()
        self.assertNotIn("from .instances", source)


class TestFirstMatchWins(unittest.TestCase):
    """Every figure in the record comes out of `score`, so it is checked on a
    list small enough to write the answer out by hand."""

    def setUp(self):
        # three cases; condition 0 covers {0,1}, condition 1 covers {1,2}
        self.ext = [0b011, 0b110] + [0] * (N_CONDITIONS - 2)
        self.truth = {"A": 0b001, "B": 0b110}

    def test_the_earlier_rule_wins_the_overlap(self):
        got = ind.Induced(rules=[((0,), "A"), ((1,), "B")])
        s = ind.score(got, self.ext, self.truth, 3)
        # rule 0 takes cases 0 and 1 and calls both A: case 0 right, case 1 wrong.
        # rule 1 gets only case 2, and calls it B: right.
        self.assertEqual(s["correct"], 2)
        self.assertEqual(s["decided"], 3)
        self.assertEqual(s["undecided"], 0)

    def test_reversing_the_list_changes_the_answer(self):
        got = ind.Induced(rules=[((1,), "B"), ((0,), "A")])
        s = ind.score(got, self.ext, self.truth, 3)
        # rule 1 takes cases 1 and 2 as B, both right; rule 0 gets case 0 as A.
        self.assertEqual(s["correct"], 3)

    def test_a_case_no_rule_covers_is_undecided_and_never_correct(self):
        got = ind.Induced(rules=[((0,), "A")])
        s = ind.score(got, self.ext, self.truth, 3)
        self.assertEqual(s["undecided"], 1)
        self.assertEqual(s["decided"], 2)

    def test_per_class_denominators_are_the_truths_and_not_the_decisions(self):
        got = ind.Induced(rules=[((0,), "A")])
        s = ind.score(got, self.ext, self.truth, 3)
        self.assertEqual(s["per_class"]["B"]["n"], 2)
        self.assertEqual(s["per_class"]["B"]["correct"], 0)


class TestTheInstances(unittest.TestCase):
    """Two training sets, because §1's amendment says neither is clean."""

    def test_the_split_is_rung_3s_own(self):
        train, test = inst.splits()
        self.assertEqual(len(train) + len(test), 2000)
        self.assertEqual(len(test), 995)

    def test_train_316_is_inside_train_632(self):
        small = set(inst._indices("train_316"))
        big = set(inst._indices("train_632"))
        self.assertTrue(small < big)
        self.assertEqual(len(big), 632)

    def test_the_scarcity_that_I_b_turns_on(self):
        """§1's amendment of 2026-08-30: the row can be refuted by scarcity.
        `ONCALL_ESCALATION` never escalated at all."""
        d = inst.describe("train_632")["by_class"]
        self.assertNotIn("ONCALL_ESCALATION", d)
        self.assertLess(d.get("T3_ENGINEERING", 0), 10)


class TestTheGate(unittest.TestCase):

    def test_it_passes_on_the_real_plan(self):
        gate = cmp.gate_signature(REPO / "PLAN_ILP.md")
        self.assertTrue(gate["passes"])
        self.assertGreaterEqual(gate["found"], cmp.MIN_SIGNATURES)

    def test_it_counts_instead_of_stopping_at_the_first(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("**Signed by Sergi: yes (date: x)**\n"
                         "**Signed by Sergi: ________ (date: ______)**\n")
            gate = cmp.gate_signature(p)
            self.assertEqual(gate["found"], 2)
            self.assertFalse(gate["passes"])

    def test_one_signature_is_not_enough(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("**Signed by Sergi: yes (date: x)**\n")
            self.assertFalse(cmp.gate_signature(p)["passes"])

    def test_a_signature_in_a_blockquote_is_invisible(self):
        """The drafter wrote §1's line inside the quotation first and this is
        what caught it."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN.md"
            p.write_text("> **Signed by Sergi: yes (date: x)**\n")
            self.assertEqual(cmp.gate_signature(p)["found"], 0)


if __name__ == "__main__":
    unittest.main()
