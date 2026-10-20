"""
`unreached/keyword_half.py`, the POST-RUN reading of what the keyword holds over
the space.

WHAT IS PINNED HERE, AND WHY.
  * The rules it names, the material it derives and the expectation's lines, so
    that moving one after the reading is visible in a diff.
  * An order's split by the keyword and its copy place, and who decides a
    region, on masks built by hand.
  * The back move rule by rule on a toy order: the parts sum to the move, and
    no point a reached rule decided moves.
  * A rule's path read as rises, the largest the earliest on a tie, and the
    replay of a toy search ending where the whole search does.
  * The cells: the top and the squared deviations, exactly.
  * Each clause of the expectation at its edge, on readings built by hand.
  * The writer refusing unsigned before it searches anything, and an argument
    printing the docstring.

**No figure of the reading is pinned here**, and no test searches an order of
the records.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from escalations import instrument as I
from rung3.budget_and_balance_ls import greedy_from_record
from unreached import keyword_half as K
from unreached import plan

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

# A toy space of eight points. Bits 0 to 3 carry the keyword. The truth is
# SECURITY_INCIDENT on 0, 1 and 2, T2_TECHNICAL on 3 and 4, X on 5 and 6, Y on 7.
KW, OTHER, SI_PTS, T2_PTS = 0b00001111, 0b11110000, 0b0111, 0b1000
TOY_M = {"x": 0b01100001, "t2": 0b00011000, "c1": 0b1111, "y": 0b10000000,
         "c2": 0b1111}
TOY_W = {"x": 0b01100000, "t2": 0b00011000, "c1": 0b0111, "y": 0b10000000,
         "c2": 0b0111}
TOY_ACTION = {"x": "X", "t2": K.T2, "c1": K.SI, "y": "Y", "c2": K.SI}
TOY_ORDER = ["x", "t2", "c1", "y", "c2"]
SP = {"M": TOY_M, "W": TOY_W, "full": 0xFF, "kw": KW, "keyword": KW,
      "other": OTHER, "si": SI_PTS, "t2": T2_PTS}


class TestTheNamesAndLines(unittest.TestCase):

    def test_the_rules_it_names(self):
        self.assertEqual((K.SUB_RULE, K.FIRST_COPY, K.ONCALL),
                         ("R0019", "R0067", "R0506"))
        self.assertEqual(K.SWAP_DRAWS, ("10|0", "10|2"))
        self.assertEqual(K.RECORD, Path("results_unreached/keyword_half.json"))

    def test_the_material_and_the_deduction(self):
        self.assertEqual(K.MATERIAL, {"keyword_half": 67200, "keyword_si": 50400,
                                      "keyword_t2": 16800, "sub_rule": 16800,
                                      "copies": 12, "route_to_si": 13})
        self.assertEqual(K.DEDUCED_FROM, {"sub_rule_place": 55,
                                          "sub_rule_test_cases": 2,
                                          "sub_rule_front_space": 5900})

    def test_the_expectations_lines(self):
        self.assertEqual((K.E2_TAKES, K.E2_SHARE, K.E7_CELLS, K.N_CELLS),
                         (500, (3, 4), 9, 12))

    def test_the_cells(self):
        cells = K.cell_names()
        self.assertEqual(len(cells), K.N_CELLS)
        self.assertEqual(sorted(len(v) for v in cells.values()), [5] * 8 + [7] * 4)
        self.assertEqual(cells["escalations|50"][-2:], ["esc:arrival|50", "esc:crowded|50"])
        self.assertEqual(cells["audit|251"][0], "audit:audit|251|0")
        self.assertEqual(sorted(len(v) for v in K.beside_names().values()), [5] * 4)

    def test_the_keyword_rules_copies_are_the_bases(self):
        inst = I.instance()
        copies = K.keyword_copies(inst)
        self.assertEqual(len(copies), K.MATERIAL["copies"])
        self.assertEqual(copies[0], K.FIRST_COPY)
        route = {r for r in inst["ids"] if inst["action"][r] == K.SI}
        self.assertEqual(route, set(copies) | {K.SUB_RULE})


class TestAnOrderReadByHand(unittest.TestCase):

    def test_fires_first_match_wins(self):
        self.assertEqual(K.fires(TOY_ORDER, TOY_M, 0xFF),
                         {"x": 0b01100001, "t2": 0b00011000, "c1": 0b0110,
                          "y": 0b10000000})

    def test_the_split_and_the_copy_place(self):
        got = K.split(TOY_ORDER, SP, ["c1", "c2"])
        self.assertEqual(got, {"space": 7, "keyword": 3, "other": 4,
                               "keyword_si": 2, "keyword_t2": 1, "copy_place": 2,
                               "copy_rule": "c1", "keyword_above_copy": 2,
                               "keyword_above_copy_right": 1, "keyword_by_copy": 2})
        self.assertEqual(K.copy_place(["c2", "x", "c1"], ["c1", "c2"]), 0)

    def test_who_decides_a_region(self):
        inst = {"action": TOY_ACTION, "truth": {10: "X", 11: "Z"},
                "matched": {10: ["x", "t2"], 11: ["t2"]},
                "rules": [{"rule_id": r, "conditions": [{"attr": "a", "op": "eq",
                                                         "value": 1}]}
                          for r in TOY_ORDER]}
        got = K.takers(TOY_ORDER, SP, KW, inst, [10, 11])
        self.assertEqual([(r["rule"], r["decides"], r["right"], r["wrong"],
                           r["labelled_decided"], r["labelled_right"])
                          for r in got["rows"]],
                         [("x", 1, 0, 1, 1, 1), ("t2", 1, 1, 0, 1, 0),
                          ("c1", 2, 2, 0, 0, 0)])
        self.assertEqual(list(got["by_queue"]), ["X", K.SI, K.T2])
        self.assertEqual((got["decides"], got["right"], got["wrong"]), (4, 3, 1))


class TestTheBackMoveRuleByRule(unittest.TestCase):

    def test_the_parts_sum_to_the_move(self):
        got = K.back_parts(TOY_ORDER, ["x"], SP, TOY_ACTION)
        self.assertTrue(got["premise"])
        self.assertEqual((got["score"], got["score_after"], got["net"]), (7, 8, 1))
        x = got["parts"]["x"]
        self.assertEqual((x["decides"], x["before"], x["after"], x["delta"]),
                         (3, 2, 3, 1))
        self.assertEqual(x["regions"]["keyword"],
                         {"decides": 1, "before": 0, "after": 1, "delta": 1})
        self.assertEqual(x["regions"]["other"]["delta"], 0)
        self.assertEqual(x["taken_by"], {"X": {"points": 2, "right": 2},
                                         K.SI: {"points": 1, "right": 1}})
        self.assertEqual(got["regions"], {"keyword": 1, "other": 0, "si": 1})

    def test_a_rule_that_decides_nothing_has_no_part(self):
        got = K.back_parts(TOY_ORDER, ["c2"], SP, TOY_ACTION)
        self.assertEqual((got["parts"], got["net"]), ({}, 0))
        self.assertTrue(got["premise"])


class TestTheStartsAndThePasses(unittest.TestCase):

    def test_a_path_read_as_rises(self):
        got = K.path([10, 10, 4, 4, 3], ["move", "swap", "move", "swap"])
        self.assertEqual((got["rise_in_moves"], got["rise_in_swaps"],
                          got["largest_rise"], got["largest_in"],
                          got["swap_passes_that_moved_it"]), (0, 7, 6, "swap", 2))
        tie = K.path([10, 8, 8, 6, 6], ["move", "swap", "move", "swap"])
        self.assertEqual((tie["largest_rise"], tie["largest_in"],
                          tie["rise_in_moves"]), (2, "move", 4))
        flat = K.path([5, 5, 6], ["move", "swap"])
        self.assertEqual((flat["largest_rise"], flat["largest_in"]), (0, None))

    def toy(self):
        # Four rules over six labelled cases; the greedy is not the optimum.
        rules = [{"rule_id": r, "born_at": k} for k, r in enumerate("abcd")]
        matched = {0: ["a", "b"], 1: ["a", "b"], 2: ["a", "c"], 3: ["b", "d"],
                   4: ["c", "d"], 5: ["d"]}
        truth = {0: "P", 1: "P", 2: "Q", 3: "Q", 4: "Q", 5: "R"}
        action = {"a": "P", "b": "Q", "c": "Q", "d": "R"}
        return {"rules": rules, "ids": [r["rule_id"] for r in rules],
                "matched": matched, "truth": truth, "action": action}

    def test_the_greedy_start_is_the_records_greedy(self):
        inst = self.toy()
        got = K.rebuilt_start(inst, range(6), "voraz")
        self.assertEqual(got, greedy_from_record(inst["rules"], inst["matched"],
                                                 inst["truth"], inst["action"],
                                                 list(range(6))))
        self.assertEqual(sorted(K.rebuilt_start(inst, range(6), "aleatorio 3")),
                         ["a", "b", "c", "d"])
        with self.assertRaises(KeyError):
            K.rebuilt_start(inst, range(6), "aleatorio 99")

    def test_the_replay_ends_where_the_whole_search_does(self):
        inst = self.toy()
        for name in ("voraz", "aleatorio 0", "aleatorio 7"):
            start = K.rebuilt_start(inst, range(6), name)
            got = K.replay(inst, range(6), start, ["a", "d"])
            self.assertEqual(got["end"], got["whole"])
            self.assertEqual(len(got["trail"]["a"]), len(got["kinds"]) + 1)
            self.assertEqual(got["kinds"][-2:], ["move", "swap"])


class TestTheCells(unittest.TestCase):

    def test_the_top_and_the_squares(self):
        rows = [{"space": 10, "keyword": 6, "other": 4},
                {"space": 12, "keyword": 9, "other": 3},
                {"space": 12, "keyword": 7, "other": 5}]
        got = K.read_cell(rows)
        self.assertTrue(got["top_has_top_keyword"])
        self.assertEqual((got["ss_keyword"], got["ss_other"], got["ss_space"],
                          got["sp_keyword_space"]),
                         (Fraction(14, 3), Fraction(2), Fraction(8, 3), Fraction(8, 3)))
        self.assertEqual(K.pooled({"c": got})["keyword_share"], Fraction(1))

    def test_a_top_without_the_top_keyword(self):
        got = K.read_cell([{"space": 12, "keyword": 6, "other": 6},
                           {"space": 11, "keyword": 9, "other": 2}])
        self.assertFalse(got["top_has_top_keyword"])


def drafted(**over):
    """A world where every clause holds; `over` replaces one piece."""
    A = {"escalations": {"sub_rule": {
        "by_queue": {K.T2: {"wrong": 3000}, "BILLING_SPECIALIST": {"wrong": 2900}},
        "rows": [{"rule": "R1", "wrong": 3000, "labelled_decided": 4,
                  "labelled_right": 3},
                 {"rule": "R2", "wrong": 499, "labelled_decided": 0,
                  "labelled_right": 0}],
        "wrong": 5900}}}
    B = {"parts": {K.ONCALL: {"delta": -1}}, "copy_place": 20, "unreached_top": 35,
         "regions": {"keyword": 0}}
    C = {k: {"si_deciders": ["R0067"],
             "replay": {"paths": {"R0067": {"largest_in": "swap"}}},
             "space": {"net": -100, "regions": {"keyword": -150}}}
         for k in K.SWAP_DRAWS}
    D = {"cells": {f"c{i}": {"top_has_top_keyword": True} for i in range(12)},
         "pooled": {"ss_keyword": Fraction(10), "ss_other": Fraction(5)}}
    world = {"A": A, "B": B, "C": C, "D": D}
    for path, value in over.items():
        node = world
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    return {e["clause"]: e["holds"]
            for e in K.read_expectation(world["A"], world["B"], world["C"], world["D"])}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_holds_on_the_drafted_world(self):
        self.assertEqual(drafted(), {f"E{i}": True for i in range(1, 9)})

    def test_e1_is_strict(self):
        self.assertFalse(drafted(A__escalations__sub_rule__by_queue={
            K.T2: {"wrong": 2900}, "BILLING_SPECIALIST": {"wrong": 2900}})["E1"])

    def test_e2_at_three_quarters_and_with_no_escalation(self):
        rows = lambda n, ok: [{"rule": "R1", "wrong": 500, "labelled_decided": n,
                               "labelled_right": ok}]
        self.assertTrue(drafted(A__escalations__sub_rule__rows=rows(8, 6))["E2"])
        self.assertFalse(drafted(A__escalations__sub_rule__rows=rows(8, 5))["E2"])
        self.assertFalse(drafted(A__escalations__sub_rule__rows=rows(0, 0))["E2"])

    def test_e3_needs_a_loss(self):
        self.assertFalse(drafted(B__parts={K.ONCALL: {"delta": 0}})["E3"])
        self.assertFalse(drafted(B__parts={})["E3"])

    def test_e4_needs_both_halves(self):
        self.assertFalse(drafted(B__copy_place=35)["E4"])
        self.assertFalse(drafted(B__regions={"keyword": 5})["E4"])

    def test_e5_needs_a_swap_in_both_draws(self):
        self.assertFalse(drafted(**{"C__10|2__replay": {"paths": {
            "R0067": {"largest_in": "move"}}}})["E5"])
        self.assertFalse(drafted(**{"C__10|0__si_deciders": []})["E5"])
        self.assertFalse(drafted(**{"C__10|0__replay": {"paths": {}}})["E5"])

    def test_e6_at_its_edge(self):
        self.assertTrue(drafted(**{"C__10|0__space": {
            "net": -100, "regions": {"keyword": -100}}})["E6"])
        self.assertFalse(drafted(**{"C__10|0__space": {
            "net": -100, "regions": {"keyword": -99}}})["E6"])
        self.assertFalse(drafted(**{"C__10|2__space": {
            "net": 0, "regions": {"keyword": -5}}})["E6"])

    def test_e7_and_e8(self):
        cells = {f"c{i}": {"top_has_top_keyword": i < 9} for i in range(12)}
        self.assertTrue(drafted(D__cells=cells)["E7"])
        cells = {f"c{i}": {"top_has_top_keyword": i < 8} for i in range(12)}
        self.assertFalse(drafted(D__cells=cells)["E7"])
        self.assertFalse(drafted(D__pooled={"ss_keyword": Fraction(5),
                                            "ss_other": Fraction(5)})["E8"])


class TestNothingIsSearchedUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_searching(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(I, "labelled_order",
                               side_effect=AssertionError("searched")) as search:
            with self.assertRaises(SystemExit):
                K.main([])
        search.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(K.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
