"""
PLAN_SPOTCHECK.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §9 and the lines of §0, so that moving one after a figure
    exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The draws by hand: seeded, nested, the two arms, and `selections.py` naming
    no truth in a name or a string.
  * The material of §1 and each draw's make-up, recomputed, and the endpoints
    as their records hold them.
  * That `spotcheck/gates.py`, which the dry run runs, hands the instrument only
    the train half, the escalations and the record's own draws.
  * The stage's verdicts and labels at their edges, on results built by hand.

**No test here searches an order on a set holding decisions.**
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from escalations import instrument as I
from escalations.selections import escalations
from spotcheck import gates, plan, score, selections

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_and_the_sets(self):
        self.assertEqual(plan.PLAN, Path("PLAN_SPOTCHECK.md"))
        self.assertEqual(plan.OUT, Path("results_spotcheck"))
        self.assertEqual((plan.SPLIT, plan.SPLIT_SEED, plan.N_SPACE), (0, 17, 134400))
        self.assertEqual(plan.BUDGETS, (10, 50, 100, 251))
        self.assertEqual((plan.N_ESCALATIONS, plan.N_DECISIONS, plan.DRAWS,
                          plan.AUDIT_SEED), (316, 689, 5, 18000))
        self.assertEqual(plan.ARMS, ("mix", "audit"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_endpoints_and_the_lines_of_section_0(self):
        self.assertEqual((plan.ARRIVAL, plan.ARRIVAL_SPACE, plan.FULL), (519, 42310, 843))
        self.assertEqual(plan.ESC_ALL, {"test": 814, "space": 73020})
        self.assertEqual(plan.FULL_RARE["T3_ENGINEERING"], 18)
        self.assertEqual(plan.ESC_ALL_RARE["T3_ENGINEERING"], 0)
        self.assertEqual((plan.N_A_LINE, plan.N_B_LINE, plan.N_C_LINE, plan.N_D_LINE,
                          plan.N_E_LINE), (814, 829, 9, 73020, 829))

    def test_the_material_of_section_1_adds_up(self):
        m = plan.MATERIAL
        self.assertEqual(plan.N_ESCALATIONS + plan.N_DECISIONS, 1005)
        self.assertEqual(m["outcome"], {"ACTION": 689})
        for key in ("by_truth", "decided", "queues_matching"):
            self.assertEqual(sum(m[key].values()), 689, key)

    def test_the_draws_make_up_nests(self):
        for d, row in plan.DRAW_MAKE_UP.items():
            for small, large in zip(plan.BUDGETS, plan.BUDGETS[1:]):
                self.assertTrue(all(a <= b for a, b in zip(row[small], row[large])),
                                (d, small, large))


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
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-20)**\n")["passes"])

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)

    def test_the_plan_on_disk_carries_one_line(self):
        self.assertEqual(plan.gate_signature()["found"], 1)


class TestTheDrawsByHand(unittest.TestCase):

    decs = tuple(range(200, 260))
    escs = (3, 7, 11)

    def test_a_shuffle_is_seeded(self):
        a = selections.shuffle(self.decs, 0)
        self.assertEqual(a, selections.shuffle(self.decs, 0))
        self.assertNotEqual(a, selections.shuffle(self.decs, 1))
        self.assertEqual(sorted(a), list(self.decs))

    def test_the_budgets_nest_and_are_sorted(self):
        for d in range(plan.DRAWS):
            sets = [selections.audited(self.decs, k, d) for k in (5, 20, 60)]
            for s, k in zip(sets, (5, 20, 60)):
                self.assertEqual((len(s), s), (k, sorted(s)))
            self.assertTrue(set(sets[0]) <= set(sets[1]) <= set(sets[2]))

    def test_the_two_arms(self):
        decs = tuple(range(1000, 1400))
        sels = selections.selections(self.escs, decs)
        self.assertEqual(len(sels), 2 * len(plan.BUDGETS) * plan.DRAWS)
        for k in plan.BUDGETS:
            for d in range(plan.DRAWS):
                alone, mix = sels[f"audit|{k}|{d}"], sels[f"mix|{k}|{d}"]
                self.assertEqual(alone, selections.audited(decs, k, d))
                self.assertEqual(mix, sorted(set(self.escs) | set(alone)))

    def test_the_selections_never_name_the_truth(self):
        path = REPO / "spotcheck/selections.py"
        self.assertEqual((gates.esc_gates.names_in(path) | gates.literals_in(path))
                         & gates.FORBIDDEN, set())

    def test_the_literal_check_catches_a_subscript(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.py"
            p.write_text('def f(r):\n    return r["truth"]\n')
            self.assertEqual(gates.esc_gates.names_in(p) & gates.FORBIDDEN, set())
            self.assertEqual(gates.literals_in(p) & gates.FORBIDDEN, {"truth"})


class TestTheMaterialAndTheEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inst = I.instance()
        cls.tr, cls.te = I.halves(cls.inst)
        cls.decs = selections.decisions(cls.tr)

    def test_the_decisions_are_the_train_half_less_the_escalations(self):
        escs = set(escalations(self.tr))
        self.assertEqual(set(self.decs), set(self.tr) - escs)
        self.assertEqual(len(self.decs), plan.N_DECISIONS)

    def test_the_material_recomputes(self):
        self.assertEqual(gates.material(self.inst, self.decs), plan.MATERIAL)

    def test_each_draw_s_make_up_recomputes(self):
        self.assertEqual(gates.draw_make_up(self.inst, self.decs), plan.DRAW_MAKE_UP)

    def test_the_records_hold_the_endpoints(self):
        held = gates.held_by_records()
        self.assertEqual(held["escalations"], {**plan.ESC_ALL, "rare": plan.ESC_ALL_RARE})
        self.assertEqual(held["full_rare"], plan.FULL_RARE)
        self.assertEqual(held["rare_of"], plan.RARE_OF)
        self.assertEqual(held["ceiling"]["T3_ENGINEERING"], 20)

    def test_no_label_reaches_the_test_split(self):
        self.assertTrue(gates.gate_ng3()["passes"])

    def test_the_selections_pass_n_g2(self):
        self.assertTrue(gates.gate_ng2()["passes"])


class TestTheDryRunSearchesNoDecisionSet(unittest.TestCase):
    """Every call of `instrument.read` in `gates.py` is handed the train half,
    the escalations, or one of the optimizer audit's own draws."""

    def test_every_read_is_handed_a_published_set(self):
        tree = ast.parse((REPO / "spotcheck/gates.py").read_text())
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
        self.assertEqual(kinds, {"tr", "escs", "record_draw"})

    def test_the_gates_build_no_selection_for_the_instrument(self):
        self.assertNotIn("verdicts", gates.esc_gates.names_in(REPO / "spotcheck/gates.py"))


def per_class(t3):
    return {"T3_ENGINEERING": {"right": t3, "of": 57}}


def results(m50, m251, t50, s50):
    out = {}
    for d in range(plan.DRAWS):
        out[f"mix|50|{d}"] = {"test": m50[d], "space": s50[d], "per_class": per_class(t50[d])}
        out[f"mix|251|{d}"] = {"test": m251[d], "space": 0, "per_class": per_class(0)}
    return out


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def rows(self, **kw):
        base = dict(m50=[810, 815, 820, 825, 830], m251=[820, 825, 829, 835, 840],
                    t50=[5, 8, 9, 10, 12], s50=[70000, 72000, 73021, 75000, 76000])
        base.update(kw)
        return {r["row"]: r for r in score.verdicts(results(**base))}

    def test_inside_every_band(self):
        v = self.rows(m50=[829, 830, 831, 835, 840])
        self.assertEqual([v[k]["holds"] for k in ("N-a", "N-b", "N-c", "N-d", "N-e")],
                         [True, True, True, True, True])

    def test_at_the_lines(self):
        v = self.rows(m50=[800, 810, 814, 820, 830], t50=[5, 8, 8, 10, 12],
                      s50=[70000, 72000, 73020, 75000, 76000],
                      m251=[820, 825, 828, 835, 840])
        self.assertFalse(v["N-a"]["holds"])               # 814 is not above 814
        self.assertFalse(v["N-b"]["holds"])               # 814 is below 829
        self.assertFalse(v["N-c"]["holds"])               # 8 is below 9
        self.assertFalse(v["N-d"]["holds"])               # 73,020 is not above 73,020
        self.assertFalse(v["N-e"]["holds"])               # 828 is below 829
        v = self.rows(m50=[800, 810, 829, 830, 840], m251=[820, 825, 829, 835, 840])
        self.assertTrue(v["N-b"]["holds"])                # 829 >= 829
        self.assertTrue(v["N-e"]["holds"])
        self.assertTrue(v["N-c"]["holds"])                # 9 >= 9

    def test_the_thin_label(self):
        v = self.rows()
        self.assertTrue(v["N-a"]["thin"])                 # 814 inside 810..830
        self.assertTrue(v["N-d"]["thin"])
        v = self.rows(m50=[815, 816, 820, 825, 828], t50=[0, 1, 2, 3, 4])
        self.assertFalse(v["N-a"]["thin"])
        self.assertFalse(v["N-b"]["thin"])                # 829 above 828
        self.assertFalse(v["N-c"]["thin"])


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
