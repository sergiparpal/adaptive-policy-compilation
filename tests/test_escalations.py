"""
PLAN_ESCALATIONS.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §9 and the lines of §0, so that moving one after a figure
    exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The three selection rules by hand, and that `selections.py` never names the
    truth.
  * The material of §1 and the comparators read off the audit's record.
  * That `escalations/gates.py`, which the dry run runs, hands the instrument
    only the train half, the record's own draws and the 286 named escalations.
  * The stage's verdicts and labels at their edges, on results built by hand.

**No test here searches an order on a set of escalations.**
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from escalations import gates, instrument, plan, score, selections

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_and_the_selections(self):
        self.assertEqual(plan.PLAN, Path("PLAN_ESCALATIONS.md"))
        self.assertEqual(plan.OUT, Path("results_escalations"))
        self.assertEqual((plan.SPLIT, plan.SPLIT_SEED, plan.N_SPACE), (0, 17, 134400))
        self.assertEqual(plan.BUDGETS, (10, 50, 100, 251))
        self.assertEqual(plan.FRACTIONS, {10: 0.01, 50: 0.05, 100: 0.10, 251: 0.25})
        self.assertEqual((plan.N_ESCALATIONS, plan.DRAWS, plan.DRAW_SEED),
                         (316, 5, 17000))
        self.assertEqual(plan.RULES, ("random", "arrival", "crowded"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_lines_of_section_0(self):
        self.assertEqual((plan.ARRIVAL, plan.ARRIVAL_SPACE, plan.FULL),
                         (519, 42310, 843))
        self.assertEqual((plan.J_A_LINE, plan.J_B_LINE, plan.J_C_LINE, plan.J_E_LINE),
                         (681, 717, 820, 0.3993))
        self.assertEqual(plan.NAMED_286, {"test": 814, "space": 73420})
        self.assertEqual(plan.PUBLISHED_FULL, {"ls_test": 0.8472, "ls_space": 0.6033})

    def test_the_material_of_section_1(self):
        self.assertEqual(plan.MATERIAL["escalations"], 316)
        self.assertEqual(sum(plan.MATERIAL["by_truth"].values()), 316)
        self.assertEqual(sum(plan.MATERIAL["queues_matching"].values()), 316)
        self.assertEqual(plan.MATERIAL["conflict"] + plan.MATERIAL["impasse"], 316)


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ____________________ (date: __________)**\n")["passes"])

    def test_one_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-19)**\n")["passes"])

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)

    def test_the_plan_on_disk_carries_one_line(self):
        self.assertEqual(plan.gate_signature()["found"], 1)


class TestTheSelectionsByHand(unittest.TestCase):

    escs = tuple(range(100, 140))
    matching = {i: (i * 7) % 11 for i in range(100, 140)}

    def test_random_is_seeded_sized_and_sorted(self):
        a = selections.random_draw(self.escs, 10, 0)
        self.assertEqual(a, selections.random_draw(self.escs, 10, 0))
        self.assertNotEqual(a, selections.random_draw(self.escs, 10, 1))
        self.assertEqual((len(a), len(set(a)), a), (10, 10, sorted(a)))
        self.assertTrue(set(a) <= set(self.escs))

    def test_arrival_is_the_first(self):
        self.assertEqual(selections.arrival(self.escs, 5), [100, 101, 102, 103, 104])

    def test_crowded_takes_the_most_matched_and_the_earlier_on_a_tie(self):
        m = {100: 3, 101: 9, 102: 9, 103: 1, 104: 9, 105: 7}
        self.assertEqual(selections.crowded(tuple(m), 3, m), [101, 102, 104])
        self.assertEqual(selections.crowded(tuple(m), 4, m), [101, 102, 104, 105])
        self.assertEqual(selections.crowded(tuple(m), 2, m), [101, 102])

    def test_every_set_the_stage_reads(self):
        escs = tuple(range(400))
        m = {i: i % 13 for i in escs}
        sels = selections.selections(escs, m)
        self.assertEqual(len(sels), len(plan.BUDGETS) * (plan.DRAWS + 2) + 1)
        self.assertEqual(sels["all"], list(escs))
        for k in plan.BUDGETS:
            self.assertEqual(len(sels[f"crowded|{k}"]), k)

    def test_the_selections_never_name_the_truth(self):
        self.assertEqual(gates.names_in(REPO / "escalations/selections.py")
                         & gates.TRUTH_NAMES, set())


class TestTheMaterialAndTheComparators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inst = instrument.instance()
        cls.tr, cls.te = instrument.halves(cls.inst)
        cls.escs = selections.escalations(cls.tr)

    def test_the_material_recomputes(self):
        self.assertEqual(gates.material(self.inst, self.escs), plan.MATERIAL)

    def test_no_label_reaches_the_test_split(self):
        self.assertTrue(gates.gate_jg3()["passes"])

    def test_the_selections_pass_j_g2(self):
        self.assertTrue(gates.gate_jg2()["passes"])

    def test_the_comparators_are_the_record_s(self):
        comp = score.comparators(gates.published_rows())
        self.assertEqual([comp[k]["test_median"] for k in plan.BUDGETS],
                         [532, 717, 791, 820])
        self.assertEqual(comp[50]["space_median"], plan.J_E_LINE)
        self.assertEqual(comp[251]["test_median"], plan.J_C_LINE)
        self.assertEqual(comp[50]["test_median"], plan.J_B_LINE)

    def test_the_record_draw_is_the_audit_s(self):
        from rung3.budget_and_balance_ls import subsample
        self.assertEqual(instrument.record_draw(self.inst, 50, 3),
                         subsample(self.tr, 0.05, 0, 3))


class TestTheDryRunSearchesNoSelection(unittest.TestCase):
    """Every call of `instrument.read` in `gates.py` is handed the train half,
    one of the audit record's own draws, or the 286 named escalations."""

    def test_every_read_is_handed_a_published_set(self):
        tree = ast.parse((REPO / "escalations/gates.py").read_text())
        reads = [c for c in ast.walk(tree) if isinstance(c, ast.Call)
                 and isinstance(c.func, ast.Attribute) and c.func.attr == "read"]
        self.assertEqual(len(reads), 3)
        kinds = set()
        for c in reads:
            arg = c.args[1]
            if isinstance(arg, ast.Name):
                kinds.add(arg.id)
            elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
                kinds.add(arg.func.attr)
        self.assertEqual(kinds, {"tr", "named", "record_draw"})

    def test_the_stage_is_not_imported_by_the_gates(self):
        names = gates.names_in(REPO / "escalations/gates.py")
        self.assertNotIn("verdicts", names)
        self.assertNotIn("score", names)


def results(e50, e251, s50, crowded):
    out = {}
    for d in range(plan.DRAWS):
        out[f"random|50|{d}"] = {"test": e50[d], "space_share": s50[d]}
        out[f"random|251|{d}"] = {"test": e251[d], "space_share": 0.5}
    out["crowded|50"] = {"test": crowded}
    return out


COMP = {50: {"test": [574, 708, 717, 734, 769], "space": [0.3569, 0.3614, 0.3993, 0.4513, 0.6044]},
        251: {"test": [768, 802, 820, 825, 829], "space": [0.3593, 0.5123, 0.5302, 0.5375, 0.5616]}}


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def rows(self, **kw):
        base = dict(e50=[600, 650, 681, 700, 720], e251=[790, 800, 819, 830, 840],
                    s50=[0.30, 0.35, 0.3992, 0.41, 0.42], crowded=682)
        base.update(kw)
        return {r["row"]: r for r in score.verdicts(results(**base), COMP)}

    def test_inside_every_band(self):
        v = self.rows(e50=[700, 710, 718, 730, 740], crowded=719)
        self.assertEqual([v[k]["holds"] for k in ("J-a", "J-b", "J-c", "J-d", "J-e")],
                         [True, True, True, True, True])

    def test_at_the_lines(self):
        v = self.rows(e50=[600, 650, 681, 700, 720], e251=[790, 800, 820, 830, 840],
                      s50=[0.30, 0.35, 0.3993, 0.41, 0.42], crowded=681)
        self.assertTrue(v["J-a"]["holds"])                # 681 >= 681
        self.assertFalse(v["J-b"]["holds"])               # 681 is not above 717
        self.assertFalse(v["J-c"]["holds"])               # 820 is not below 820
        self.assertFalse(v["J-d"]["holds"])               # 681 is not above 681
        self.assertFalse(v["J-e"]["holds"])               # 0.3993 is not below 0.3993
        v = self.rows(e50=[600, 650, 680, 700, 720])
        self.assertFalse(v["J-a"]["holds"])

    def test_the_thin_label(self):
        v = self.rows()
        self.assertTrue(v["J-a"]["thin"])                 # 681 inside 600..720
        v = self.rows(e50=[700, 705, 710, 715, 720])
        self.assertFalse(v["J-a"]["thin"])
        self.assertTrue(score.both_inside([1, 2, 3], [2, 3, 4]))
        self.assertFalse(score.both_inside([1, 2, 3], [10, 11, 12]))


class TestNothingIsMeasuredOrWrittenUnsigned(unittest.TestCase):

    def test_the_stage_refuses_before_anything(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                score.main([])
        checks.assert_not_called()
        write.assert_not_called()

    def test_the_dry_run_writes_nothing(self):
        with mock.patch.object(gates, "run_all",
                               return_value=SimpleNamespace(blocking_pass=True)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            self.assertEqual(score.main(["--dry-run"]), 0)
            write.assert_not_called()
        with mock.patch.object(gates, "run_all",
                               return_value=SimpleNamespace(blocking_pass=False)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")), \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                score.main(["--dry-run"])


if __name__ == "__main__":
    unittest.main()
