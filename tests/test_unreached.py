"""
PLAN_UNREACHED.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §9 and the lines of §0, so that moving one after a figure
    exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The moves by hand: the front, the back and the coin are the permutations
    §3 defines, reach is read off matching, copies are rules written the same,
    and `moves.py` names no truth in a name or a string.
  * The material of §1, its table and the curve's reach, recomputed, and the
    endpoints as their records hold them.
  * A rule's reading by hand, on a toy instance: its move to the front read by
    first match, split at its birth ticket, agrees with the masks.
  * That `unreached/gates.py`, which the dry run runs, applies no move to a
    searched order but the key rule's to the front, whose count is published.
  * The stage's verdicts and labels at their edges, on readings built by hand.

**No test here searches an order.**
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from escalations import instrument as I
from rung3.local_search import build_masks
from unreached import gates, moves, plan, score

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_and_the_moves(self):
        self.assertEqual(plan.PLAN, Path("PLAN_UNREACHED.md"))
        self.assertEqual(plan.OUT, Path("results_unreached"))
        self.assertEqual((plan.SPLIT, plan.SPLIT_SEED, plan.N_SPACE, plan.N_TEST),
                         (0, 17, 134400, 995))
        self.assertEqual(plan.ENDPOINTS, ("escalations", "full"))
        self.assertEqual(plan.KEY_RULE, "R0545")
        self.assertEqual((plan.BUDGETS, plan.DRAWS), ((10, 50, 100, 251), 5))
        self.assertEqual((plan.COIN_DRAWS, plan.COIN_SEED), (100, 19000))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_endpoints_and_the_lines_of_section_0(self):
        self.assertEqual((plan.ARRIVAL, plan.ARRIVAL_SPACE), (519, 42310))
        self.assertEqual(plan.ESC_ALL, {"test": 814, "space": 73020})
        self.assertEqual(plan.FULL, {"test": 843, "space": 81089})
        self.assertEqual(plan.BEST_FROM, {"escalations": "aleatorio 57",
                                          "full": "aleatorio 13"})
        self.assertEqual((plan.GAP, plan.SPACE_GAP), (29, 8069))
        self.assertEqual((plan.Z_A_LINE, plan.Z_B_LINE, plan.Z_C_LINE, plan.Z_D_LINE,
                          plan.Z_E_LINE), (1, 15, 4035, 814, 73020))

    def test_the_table_adds_up_to_the_material(self):
        esc, full = plan.MATERIAL["escalations"], plan.MATERIAL["full"]
        rows = plan.UNREACHED.values()
        self.assertEqual(len(plan.UNREACHED), esc["unreached"])
        self.assertEqual(sum(r[3] for r in rows), esc["test_matches"])
        self.assertEqual(sum(r[4] for r in rows), esc["birth_ticket_matches"])
        self.assertEqual(sum(r[5] for r in rows), esc["space_points"])
        self.assertEqual(sum(esc["by_queue"].values()), esc["unreached"])
        in_full = [r for r in rows if r[6]]
        self.assertEqual(len(in_full), full["unreached"])
        self.assertEqual(sum(r[3] for r in in_full), full["test_matches"])
        self.assertEqual(sum(r[5] for r in in_full), full["space_points"])
        self.assertEqual(plan.MATERIAL["born_in_test"] + plan.MATERIAL["born_in_train"],
                         plan.MATERIAL["rules"])

    def test_the_copies_are_one_rule_four_times(self):
        rows = {plan.UNREACHED[r][:1] + plan.UNREACHED[r][2:4] + plan.UNREACHED[r][5:]
                for r in plan.COPIES}
        self.assertEqual(len(rows), 1)
        self.assertEqual(plan.MATERIAL["escalations"]["distinct"],
                         len(plan.UNREACHED) - len(plan.COPIES) + 1)
        self.assertIn(plan.KEY_RULE, plan.UNREACHED)
        self.assertNotIn(plan.KEY_RULE, plan.COPIES)


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


class TestTheMovesByHand(unittest.TestCase):

    order = ["a", "b", "c", "d", "e", "f"]

    def test_the_front(self):
        self.assertEqual(moves.front(self.order, "d"), ["d", "a", "b", "c", "e", "f"])
        self.assertEqual(moves.front(self.order, "a"), self.order)
        with self.assertRaises(ValueError):
            moves.front(self.order, "z")

    def test_the_back_keeps_both_orders(self):
        self.assertEqual(moves.back(self.order, ["f", "a", "c"]),
                         ["b", "d", "e", "a", "c", "f"])
        self.assertEqual(moves.back(self.order, []), self.order)

    def test_the_coin_is_seeded_and_keeps_the_reached(self):
        u = ["b", "e"]
        a = [moves.coin(self.order, u, d) for d in range(20)]
        self.assertEqual(a, [moves.coin(self.order, u, d) for d in range(20)])
        for o in a:
            self.assertEqual(sorted(o), self.order)
            self.assertEqual([r for r in o if r not in u], ["a", "c", "d", "f"])
        self.assertGreater(len({tuple(o) for o in a}), 1)
        self.assertEqual(moves.coin(self.order, [], 0), self.order)

    def test_reach_is_matching(self):
        matched = [["a", "b"], ["c"], ["d", "a"], []]
        self.assertEqual(moves.reached(matched, [0, 2]), {"a", "b", "d"})
        self.assertEqual(moves.unreached(self.order, matched, [0, 2]), ["c", "e", "f"])
        self.assertEqual(moves.unreached(self.order, matched, []), self.order)

    def test_copies_are_conditions_and_queue(self):
        def rule(rid, born, action, conds):
            return {"rule_id": rid, "born_at": born, "action": action,
                    "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds]}
        rules = [rule("p", 9, "Q", [("x", 1), ("y", True)]),
                 rule("q", 2, "Q", [("y", True), ("x", 1)]),
                 rule("r", 5, "R", [("x", 1), ("y", True)]),
                 rule("s", 1, "Q", [("x", 1)])]
        self.assertEqual(moves.copies(rules, ["p", "q", "r", "s"]), [["q", "p"]])
        self.assertEqual(moves.distinct(rules, ["p", "q", "r", "s"]), ["s", "q", "r"])

    def test_the_birth_ticket(self):
        corpus = [SimpleNamespace(key=lambda k=k: k) for k in ("x", "y", "x", "z")]
        self.assertEqual(moves.birth_ticket(corpus, 0, [1, 2, 3]), {2})

    def test_moves_never_name_the_truth(self):
        path = REPO / "unreached/moves.py"
        self.assertEqual((gates.esc_gates.names_in(path) | gates.sp_gates.literals_in(path))
                         & gates.FORBIDDEN, set())

    def test_the_moves_pass_z_g2(self):
        self.assertTrue(gates.gate_zg2()["passes"])


class TestTheMaterialAndTheEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inst = I.instance()

    def test_the_material_recomputes(self):
        self.assertEqual(gates.material(self.inst), plan.MATERIAL)

    def test_the_table_recomputes(self):
        self.assertEqual(gates.table(self.inst), plan.UNREACHED)

    def test_the_copies_recompute(self):
        self.assertEqual(moves.copies(self.inst["rules"], list(plan.UNREACHED)),
                         [list(plan.COPIES)])

    def test_the_curve_s_reach_recomputes(self):
        self.assertEqual(gates.curve_reach(self.inst), plan.CURVE_REACH)

    def test_the_records_hold_the_endpoints(self):
        held = gates.held_by_records()
        self.assertEqual(held["escalations"],
                         {**plan.ESC_ALL, "best_from": plan.BEST_FROM["escalations"],
                          "rare": plan.ESC_ALL_RARE})
        self.assertEqual(held["full"], {**plan.FULL, "best_from": plan.BEST_FROM["full"]})
        self.assertEqual(held["full_rare"], plan.FULL_RARE)
        self.assertEqual(held["key_rule"], plan.KEY_RULE)
        self.assertEqual({k: len(v) for k, v in held["orders"].items()},
                         {"escalations": 577, "full": 577})

    def test_no_label_reaches_the_test_split(self):
        self.assertTrue(gates.gate_zg3()["passes"])


class TestTheDryRunAppliesOnlyThePublishedMove(unittest.TestCase):
    """In `gates.py`, every front, back or coin is handed the toy order, but one:
    the key rule to the front of a searched order, whose count is published."""

    def test_every_move_is_the_toy_s_or_the_key_rule_s(self):
        tree = ast.parse((REPO / "unreached/gates.py").read_text())
        calls = [c for c in ast.walk(tree) if isinstance(c, ast.Call)
                 and isinstance(c.func, ast.Attribute)
                 and isinstance(c.func.value, ast.Name) and c.func.value.id == "moves"
                 and c.func.attr in ("front", "back", "coin")]
        searched = [c for c in calls
                    if not (isinstance(c.args[0], ast.Name) and c.args[0].id == "toy")]
        self.assertEqual(len(searched), 1)
        c = searched[0]
        self.assertEqual(c.func.attr, "front")
        self.assertIsInstance(c.args[1], ast.Attribute)
        self.assertEqual(c.args[1].attr, "KEY_RULE")

    def test_the_gates_read_no_verdict(self):
        names = gates.esc_gates.names_in(REPO / "unreached/gates.py")
        self.assertNotIn("verdicts", names)
        self.assertNotIn("read_order", names)


def toy_instance():
    """Four rules, eight cases; the test half is 4 to 7, and case 7 is case 4's
    ticket again."""
    keys = ["a", "b", "c", "d", "k4", "e", "f", "k4"]
    truth = ["T2_TECHNICAL", "T2_TECHNICAL", "T2_TECHNICAL", "T1_GENERAL",
             "T3_ENGINEERING", "T3_ENGINEERING", "T2_TECHNICAL", "T2_TECHNICAL"]
    return {
        "ids": ["A", "B", "C", "D"],
        "rules": [{"rule_id": r, "born_at": b, "action": a, "conditions": [
                      {"attr": "x", "op": "eq", "value": r}]}
                  for r, b, a in (("A", 0, "T2_TECHNICAL"), ("B", 4, "T3_ENGINEERING"),
                                  ("C", 1, "T2_TECHNICAL"), ("D", 3, "T1_GENERAL"))],
        "action": {"A": "T2_TECHNICAL", "B": "T3_ENGINEERING", "C": "T2_TECHNICAL",
                   "D": "T1_GENERAL"},
        "born": {"A": 0, "B": 4, "C": 1, "D": 3},
        "matched": [["A", "C"], ["C"], ["A"], ["D"], ["A", "B"], ["B", "C"], ["A"], ["B"]],
        "truth": truth,
        "corpus": [SimpleNamespace(key=lambda k=k: k) for k in keys],
        "splits": [([0, 1, 2, 3], [4, 5, 6, 7])],
    }


class TestARuleReadByHand(unittest.TestCase):

    def setUp(self):
        self.inst = toy_instance()
        tm = build_masks(self.inst["ids"], self.inst["matched"], self.inst["truth"],
                         self.inst["action"], [4, 5, 6, 7])
        self.masks = {"test": tm, "space": tm}
        self.order = ["A", "C", "D", "B"]

    def test_the_front_move_by_first_match_and_by_masks(self):
        base = {"test": 1, "space": 1}
        r = score.read_rule(self.inst, self.order, "B", base, self.masks)
        self.assertEqual((r["test_cases"], r["birth_ticket_cases"]), (3, 2))
        self.assertEqual((r["decided_in_order"], r["right_in_order"], r["right_moved"]),
                         (1, 0, 2))
        self.assertEqual((r["delta_test_birth"], r["delta_test_away"]), (1, 1))
        self.assertEqual(r["delta_test"], 2)
        self.assertTrue(r["routes_agree"])
        self.assertEqual(r["rank"], 3)

    def test_an_order_read_whole(self):
        r = score.read_order(self.inst, self.order, [0, 1, 2, 3], self.masks, coin=True)
        self.assertEqual(r["unreached"], ["B"])
        self.assertEqual(r["order"]["test"], 1)
        self.assertEqual(r["back"]["test"], 1)            # B was last already
        self.assertEqual(len(r["coin"]["test"]), plan.COIN_DRAWS)
        self.assertEqual(r["rules"]["B"]["delta_test"], 2)

    def test_the_stake_counts_losses_as_zero(self):
        read = {"rules": {"x": {"d": 3}, "y": {"d": -5}, "z": {"d": 0}, "w": {"d": 2}}}
        s = score.stake(read, ["x", "y", "z", "w"], "d")
        self.assertEqual(s, {"gainers": ["w", "x"], "losers": ["y"], "sum_of_gains": 5})


def endpoint(away=None, space=None, back=(814, 73020), coin=((810, 820), (70000, 76000))):
    away = away or {}
    space = space or {}
    rules = {}
    for r in plan.UNREACHED:
        rules[r] = {"delta_test_away": away.get(r, 0), "delta_space": space.get(r, 0)}
    distinct = [r for r in plan.UNREACHED if r not in plan.COPIES[1:]]
    return {"distinct": distinct, "rules": rules,
            "back": {"test": back[0], "space": back[1]},
            "coin": {"test": list(coin[0]), "space": list(coin[1])}}


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def rows(self, **kw):
        return {r["row"]: r for r in score.verdicts(endpoint(**kw))}

    def test_inside_every_band(self):
        v = self.rows(away={"R0570": 9, "R0016": 6, plan.KEY_RULE: 50},
                      space={"R0019": 4035}, back=(815, 73021))
        self.assertEqual([v[k]["holds"] for k in ("Z-a", "Z-b", "Z-c", "Z-d", "Z-e")],
                         [True, True, True, True, True])

    def test_at_the_lines(self):
        v = self.rows(away={plan.KEY_RULE: 13, "R0570": -2},
                      space={"R0019": 4034}, back=(814, 73020))
        self.assertFalse(v["Z-a"]["holds"])               # the key rule does not count
        self.assertFalse(v["Z-b"]["holds"])               # a loss counts as zero
        self.assertFalse(v["Z-c"]["holds"])               # 4,034 is below 4,035
        self.assertFalse(v["Z-d"]["holds"])               # 814 is not above 814
        self.assertFalse(v["Z-e"]["holds"])               # 73,020 is not above 73,020
        v = self.rows(away={"R0570": 1, "R0016": 14}, space={"R0019": 4000, plan.KEY_RULE: 35})
        self.assertTrue(v["Z-a"]["holds"])                # one gainer is enough
        self.assertTrue(v["Z-b"]["holds"])                # 15 >= 15
        self.assertTrue(v["Z-c"]["holds"])                # the key rule counts over the space

    def test_a_copy_counts_once(self):
        v = self.rows(away={c: 5 for c in plan.COPIES}, space={c: 2000 for c in plan.COPIES})
        self.assertEqual(v["Z-a"]["value"], 1)
        self.assertEqual(v["Z-b"]["value"], 5)
        self.assertEqual(v["Z-c"]["value"], 2000)

    def test_the_thin_label(self):
        v = self.rows(back=(815, 73021))
        self.assertTrue(v["Z-d"]["thin"])                 # 815 inside 810..820
        self.assertTrue(v["Z-e"]["thin"])
        v = self.rows(back=(821, 76001))
        self.assertFalse(v["Z-d"]["thin"])
        self.assertFalse(v["Z-e"]["thin"])
        self.assertIsNone(v["Z-a"]["thin"])
        self.assertIsNone(v["Z-b"]["thin"])
        self.assertIsNone(v["Z-c"]["thin"])


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
