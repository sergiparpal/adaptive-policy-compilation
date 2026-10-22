"""
`manual/readings.py`, the POST-RUN readings of what `PLAN_MANUAL.md`'s Stage C
left free on the records.

WHAT IS PINNED HERE, AND WHY.
  * The counts it checks, the translations it names and the expectation's
    lines, so that moving one after the reading is visible in a diff.
  * A birth read against its ticket's rule, crossing, nested or partial, on
    masks built by hand; a level's pooled summary, and the gap split by the
    classes' mix, exactly.
  * A birth's declarations come back in the answer's order, and a record that
    does not keep them is refused. Translated edges are written into a copy of
    the record where the declaration stood, and only there.
  * A dropped declaration read against the policy, the rules each translation
    names, and the edges it becomes.
  * The points where two bases decide differently, on the space.
  * Each clause of the expectation at its edge, on readings built by hand.
  * The writer refusing unsigned before it reads a record, and an argument
    printing the docstring.

**No figure of the reading is pinned here**, and no test reads a loop record.
"""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from harness.dsl import Condition

from edges.rebuild import Edge, edges_by_birth
from fidelity.replay import OUTSIDE
from manual import instrument as I
from manual import plan
from manual import readings as R
from rung2.engine2 import PriorityEngine, Rule2

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

# A toy space of eight points. Bits 0 to 3 carry the keyword; bits 4 to 7 do not.
OUT = 0b11110000
TOY_HIDDEN = {
    "HK": {"queue": "S", "ext": 0b00001111, "region": 0b00001111},
    "HA": {"queue": "A", "ext": 0b11110000, "region": 0b00110000},
    "HB": {"queue": "B", "ext": 0b11000000, "region": 0b11000000},
}
TOY_EXT = {"k1": 0b00000011, "r1": 0b00010000, "r2": 0b11000000, "r3": 0b11110000,
           "r4": 0b00011100}
TOY_RULES = [
    {"rule_id": "k1", "born_at": 0, "action": "S", "conditions": [{}]},
    {"rule_id": "r1", "born_at": 1, "action": "A", "conditions": [{}] * 3},
    {"rule_id": "r2", "born_at": 2, "action": "B", "conditions": [{}]},
    {"rule_id": "r3", "born_at": 3, "action": "A", "conditions": [{}]},
    {"rule_id": "r4", "born_at": 4, "action": "B", "conditions": [{}] * 2},
]
TOY_ROWS = {0: {"truth_rule": "HK", "truth": "S", "outcome": "IMPASSE"},
            1: {"truth_rule": "HA", "truth": "A", "outcome": "IMPASSE"},
            2: {"truth_rule": "HB", "truth": "B", "outcome": "IMPASSE"},
            3: {"truth_rule": "HA", "truth": "A", "outcome": "CONFLICT"},
            4: {"truth_rule": "HB", "truth": "A", "outcome": "IMPASSE"}}


def toy_births() -> list[dict]:
    return R.births_read(TOY_RULES, TOY_ROWS, TOY_HIDDEN, TOY_EXT, OUT)


def toy_record() -> dict:
    """Two births. The second answered: beats H07, beats R0001, loses_to H03,
    loses_to R0001. The first and third were dropped outside the neighbourhood,
    the second accepted, the fourth refused for a cycle."""
    return {
        "rules": [
            {"rule_id": "R0001", "born_at": 0, "action": "A", "conditions": [],
             "beats": [], "loses_to": [], "dropped_edges": []},
            {"rule_id": "R0002", "born_at": 1, "action": "B", "conditions": [],
             "beats": ["R0001"], "loses_to": [],
             "dropped_edges": ["beats:H07", "loses_to:H03", "loses_to:R0001:cierra_ciclo"]},
        ],
        "records": [{"idx": 0, "edge_reasons": []},
                    {"idx": 1, "edge_reasons": [OUTSIDE, "ok", OUTSIDE, "cierra_ciclo"]}],
        "edge_log": [["R0002", "R0001", "ok"], ["R0001", "R0002", "cierra_ciclo"]],
    }


class TestTheNamesAndLines(unittest.TestCase):

    def test_the_counts_it_checks(self):
        self.assertEqual(R.DROPPED, {(3, 1): 29, (3, 2): 26, (3, 3): 6})
        self.assertEqual(sum(R.DROPPED.values()), 61)
        self.assertEqual(R.record_path(), Path("results_manual/readings.json"))
        self.assertEqual(R.CLASSES, ("region", "rule", "beyond"))
        self.assertEqual(R.TRANSLATIONS, ("T1", "T2"))
        self.assertEqual(R.A1_LEVELS, (1, 2, 3))

    def test_the_expectations_lines(self):
        self.assertEqual((R.A3_SHARE, R.B1_IDLE, R.B2_HIT, R.B3_T1, R.C1_SHARE),
                         (Fraction(1, 2), Fraction(1, 4), Fraction(3, 4),
                          Fraction(1, 4), Fraction(1, 2)))
        self.assertEqual((R.B4_POINTS, R.B4_ARRIVALS), (1344, 20))
        self.assertEqual(R.B4_POINTS, I.space().n // 100)

    def test_the_hidden_rules_regions_partition_the_space(self):
        hidden = R.hidden_rules()
        self.assertEqual(len(hidden), 29)
        union = 0
        for H in hidden.values():
            self.assertTrue(R.contains(H["ext"], H["region"]))
            self.assertFalse(union & H["region"])
            union |= H["region"]
        self.assertEqual(union, (1 << I.space().n) - 1)


class TestABirthAgainstItsTicketsRule(unittest.TestCase):

    def test_the_three_classes(self):
        H = TOY_HIDDEN["HA"]
        self.assertEqual(R.classify(0b00010000, H), "region")
        self.assertEqual(R.classify(0b00110000, H), "region")
        self.assertEqual(R.classify(0b11110000, H), "rule")
        self.assertEqual(R.classify(0b01010000, H), "rule")
        self.assertEqual(R.classify(0b00011000, H), "beyond")

    def test_a_keyword_rule_is_not_read_and_is_still_met(self):
        got = toy_births()
        self.assertEqual([b["rule_id"] for b in got], ["r1", "r2", "r3", "r4"])

    def test_crossing_nested_and_partial(self):
        got = {b["rule_id"]: b for b in toy_births()}
        self.assertEqual([got[r]["class"] for r in ("r1", "r2", "r3", "r4")],
                         ["region", "region", "rule", "beyond"])
        self.assertEqual([got[r]["crosses"] for r in ("r1", "r2", "r3", "r4")],
                         [False, False, True, True])
        self.assertEqual(got["r3"]["met"], ["r2"])
        self.assertTrue(got["r3"]["nested"])
        self.assertEqual(got["r4"]["met"], ["r1", "r3"])
        self.assertFalse(got["r4"]["nested"])
        self.assertTrue(got["r3"]["as_written"])
        self.assertTrue(got["r2"]["region_exactly"])
        self.assertTrue(got["r1"]["one_point"])
        self.assertFalse(got["r4"]["right_queue"])
        self.assertEqual(got["r4"]["points_outside"], 1)

    def test_the_summary(self):
        s = R.summary(toy_births())
        self.assertEqual((s["births"], s["alone"], s["k_a"]), (4, 2, Fraction(1, 2)))
        self.assertEqual(s["classes"]["region"], {"births": 2, "cross": 0,
                                                  "right_queue": 2, "nested": 0})
        self.assertEqual(s["class_share"]["beyond"], Fraction(1, 4))
        self.assertEqual(s["cross_rate"]["rule"], Fraction(1))
        self.assertEqual(s["crossing"], {"nested": 1, "partial": 1})
        # r2 is HB's region and HB as written: HB's region is its extension.
        self.assertEqual((s["as_written"], s["region_exactly"], s["one_point"]),
                         (2, 1, 1))
        self.assertEqual(s["conditions_median"], 1.5)
        self.assertEqual(s["points_outside_median"], 1.5)

    def test_the_gap_split_by_the_mix_exactly(self):
        def level(region, rule, beyond=(0, 0)):
            classes = {c: {"births": b, "cross": x}
                       for c, (b, x) in zip(R.CLASSES, (region, rule, beyond))}
            n = sum(b for b, _ in (region, rule, beyond))
            alone = n - sum(x for _, x in (region, rule, beyond))
            return {"k_a": Fraction(alone, n), "classes": classes}
        low, high = level((2, 1), (2, 2)), level((6, 1), (2, 1))
        m = R.mix_split(low, high)
        self.assertEqual(m["gap"], Fraction(1, 2))
        self.assertEqual(m["low_rates_on_high_mix"], Fraction(3, 8))
        self.assertEqual(m["high_rates_on_low_mix"], Fraction(2, 3))
        self.assertEqual(m["mix_share_low_rates"], Fraction(1, 4))
        self.assertEqual(m["mix_share_high_rates"], Fraction(1, 6))

    def test_a_class_without_a_rate_gives_no_share(self):
        low, high = ({"k_a": Fraction(1, 2), "classes": {
            "region": {"births": 2, "cross": 1}, "rule": {"births": 0, "cross": 0},
            "beyond": {"births": 0, "cross": 0}}},
            {"k_a": Fraction(1), "classes": {
                "region": {"births": 1, "cross": 0}, "rule": {"births": 1, "cross": 0},
                "beyond": {"births": 0, "cross": 0}}})
        m = R.mix_split(low, high)
        self.assertIsNone(m["low_rates_on_high_mix"])
        self.assertIsNone(m["mix_share_low_rates"])
        self.assertIsNotNone(m["mix_share_high_rates"])


class TestTheAnswersInOrder(unittest.TestCase):

    def test_the_declarations_come_back_in_order(self):
        got = R.answers(toy_record())
        self.assertEqual(list(got), [1])
        self.assertEqual(got[1], [("outside", "beats", "H07"),
                                  ("logged", Edge(0, 1, "R0002", "R0001", "ok")),
                                  ("outside", "loses_to", "H03"),
                                  ("logged", Edge(1, 1, "R0001", "R0002", "cierra_ciclo"))])
        self.assertEqual(R.dropped(toy_record()), [
            {"case": 1, "k": 0, "rule": "R0002", "direction": "beats", "cites": "H07"},
            {"case": 1, "k": 1, "rule": "R0002", "direction": "loses_to", "cites": "H03"}])

    def test_a_record_that_does_not_keep_them_is_refused(self):
        rec = toy_record()
        rec["rules"][1]["dropped_edges"].remove("loses_to:H03")
        with self.assertRaises(R.AnswerError):
            R.answers(rec)
        rec = toy_record()
        rec["rules"][1]["beats"] = []
        with self.assertRaises(R.AnswerError):
            R.answers(rec)
        rec = toy_record()
        rec["rules"][1]["dropped_edges"].append("beats:H09")
        with self.assertRaises(R.AnswerError):
            R.answers(rec)
        rec = toy_record()
        rec["rules"][1]["dropped_edges"][2] = "loses_to:R0001:no_solapan"
        with self.assertRaises(R.AnswerError):
            R.answers(rec)

    def test_translated_edges_are_written_where_the_declaration_stood(self):
        rec = toy_record()
        before = json.dumps(rec, sort_keys=True)
        copy_, keys = R.written_in(rec, {(1, 0): [("R0002", "R0009")],
                                         (1, 1): [("R0008", "R0002"), ("R0007", "R0002")]})
        self.assertEqual(json.dumps(rec, sort_keys=True), before)
        self.assertEqual(copy_["records"][1]["edge_reasons"],
                         [R.TRANSLATED, "ok", R.TRANSLATED, R.TRANSLATED, "cierra_ciclo"])
        self.assertEqual(keys, {(1, 0): [0], (1, 1): [2, 3]})
        self.assertEqual([(e.winner, e.loser) for e in edges_by_birth(copy_)[1]],
                         [("R0002", "R0009"), ("R0002", "R0001"), ("R0008", "R0002"),
                          ("R0007", "R0002"), ("R0001", "R0002")])

    def test_a_declaration_without_translation_stays_dropped(self):
        copy_, keys = R.written_in(toy_record(), {(1, 1): [("R0008", "R0002")]})
        self.assertEqual(copy_["records"][1]["edge_reasons"],
                         [OUTSIDE, "ok", R.TRANSLATED, "cierra_ciclo"])
        self.assertEqual(keys, {(1, 1): [1]})
        same, none = R.written_in(toy_record(), {})
        self.assertEqual(json.dumps(same, sort_keys=True),
                         json.dumps(toy_record(), sort_keys=True))
        self.assertEqual(none, {})


class TestTheClaimAndItsTranslations(unittest.TestCase):

    HIDDEN = {"H1": {"ext": 0b1111, "queue": "X"}}

    def claim(self, direction, e_r, q_r, tmask):
        d = {"rule": "R", "direction": direction, "cites": "H1"}
        return R.claim(d, {"R": e_r}, {"R": q_r}, self.HIDDEN, tmask)

    def test_inert_and_idle(self):
        self.assertEqual(self.claim("beats", 0b10000, "Y", {"X": 0, "Y": 0})["kind"],
                         "inert")
        self.assertEqual(self.claim("beats", 0b0011, "X", {"X": 0, "Y": 0})["kind"],
                         "idle")

    def test_at_stake_hit_miss_tie_and_neither(self):
        tm = {"Y": 0b0011, "X": 0}
        self.assertEqual(self.claim("beats", 0b0011, "Y", tm)["point"], "hit")
        self.assertEqual(self.claim("loses_to", 0b0011, "Y", tm)["point"], "miss")
        self.assertEqual(self.claim("beats", 0b0011, "Y",
                                    {"Y": 0b0001, "X": 0b0010})["point"], "tie")
        self.assertEqual(self.claim("beats", 0b0011, "Y",
                                    {"Y": 0, "X": 0})["point"], "neither_ever_right")
        self.assertEqual(self.claim("beats", 0b0011, "Y", tm)["wins"], [2, 0])

    def test_containment_and_whether_it_agrees(self):
        tm = {"Y": 0, "X": 0}
        c = self.claim("beats", 0b0011, "Y", tm)
        self.assertEqual((c["containment"], c["agrees_with_containment"]),
                         ("rule_inside_cited", True))
        c = self.claim("beats", 0b11111, "Y", tm)
        self.assertEqual((c["containment"], c["agrees_with_containment"]),
                         ("cited_inside_rule", False))
        c = self.claim("loses_to", 0b11111, "Y", tm)
        self.assertTrue(c["agrees_with_containment"])
        c = self.claim("beats", 0b11000, "Y", tm)
        self.assertEqual((c["containment"], c["agrees_with_containment"]), (None, None))

    def test_the_rules_each_translation_names(self):
        H = {"ext": 0b1100, "queue": "X"}
        ext = {"R1": 0b1100, "R2": 0b0100, "R3": 0b1100, "R4": 0b1110}
        action = {"R1": "X", "R2": "X", "R3": "Y", "R4": "X"}
        self.assertEqual(R.counterparts(H, ["R1", "R2", "R3", "R4"], ext, action),
                         {"T1": ["R1"], "T2": ["R1", "R2"]})

    def test_the_edges_a_declaration_becomes(self):
        self.assertEqual(R.pairs_of({"rule": "R9", "direction": "beats"}, ["R1", "R2"]),
                         [("R9", "R1"), ("R9", "R2")])
        self.assertEqual(R.pairs_of({"rule": "R9", "direction": "loses_to"}, ["R1"]),
                         [("R1", "R9")])


class TestThePointsThatChange(unittest.TestCase):

    def engine(self, rules):
        eng = PriorityEngine(space=I.space())
        for i, (conds, action) in enumerate(rules):
            eng.add(Rule2(rule_id=f"R{i:04d}", conditions=conds, action=action),
                    born_at=i, keep_id=True)
        return eng

    def test_a_narrower_rule_changes_its_extension(self):
        sev1 = [Condition("severity", "eq", 1)]
        api = sev1 + [Condition("product", "eq", "api")]
        a = self.engine([(sev1, "A")])
        b = self.engine([(sev1, "A"), (api, "B")])
        self.assertEqual(R.points_changed(a, a), 0)
        self.assertEqual(R.points_changed(a, b), I.space().n // 4 // 5)
        c = self.engine([(sev1, "A"), (api, "A")])
        self.assertEqual(R.points_changed(a, c), 0)


def drafted(**over):
    """A world where every clause holds; `over` replaces one piece."""
    def level(region, rule, beyond):
        classes = {c: {"births": b, "cross": x}
                   for c, (b, x) in zip(R.CLASSES, (region, rule, beyond))}
        n = sum(b for b, _ in (region, rule, beyond))
        return {"classes": classes,
                "class_share": {c: Fraction(classes[c]["births"], n) for c in R.CLASSES}}
    A = {"levels": {"0": level((5, 0), (5, 0), (0, 0)),
                    "1": level((10, 1), (5, 3), (5, 3)),
                    "2": level((4, 1), (6, 4), (10, 8)),
                    "3": level((14, 2), (4, 2), (2, 2))},
         "mix": {"gap": Fraction(3, 10), "mix_share_low_rates": Fraction(3, 5),
                 "mix_share_high_rates": Fraction(2, 3)}}
    B = {"declarations": 8, "kinds": {"idle": 1, "inert": 1, "at_stake": 6},
         "points": {"hit": 3, "miss": 1, "tie": 2},
         "counterparts": {"T1": {"shown": 1, "unshown": 0, "none": 7}},
         "translations": {t: {"runs": {"L3 r1": {"points_changed": 1343,
                                                 "arrivals_changed": 19}}}
                          for t in R.TRANSLATIONS}}
    C = {"runs": {f"L2 r{r}": {
        "decided": 3,
        "deciders": [{"rule_id": "R1", "decided": 2, "queue": R.T2, "keyword_rule": True}],
        "tickets": [{"outcome": "ACTION", "right": False, "class_rules": []},
                    {"outcome": "ACTION", "right": True, "class_rules": ["R5"]},
                    {"outcome": "IMPASSE", "right": False}]} for r in (1, 2, 3)}}
    world = {"A": A, "B": B, "C": C}
    for path, value in over.items():
        node = world
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    return {e["clause"]: e["holds"]
            for e in R.read_expectation(world["A"], world["B"], world["C"])}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_holds_on_the_drafted_world(self):
        self.assertEqual(drafted(), {c: True for c in (
            "A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4")})

    def test_a1_is_strict_and_does_not_read_l0(self):
        self.assertFalse(drafted(A__levels__1__classes__region={"births": 10, "cross": 6})["A1"])
        self.assertTrue(drafted(A__levels__0__classes__region={"births": 5, "cross": 5})["A1"])

    def test_a2_and_a4_are_strict(self):
        share = {"region": Fraction(7, 10), "rule": Fraction(1, 5), "beyond": Fraction(1, 2)}
        self.assertFalse(drafted(A__levels__2__class_share=share)["A2"])
        share = {"region": Fraction(7, 10), "rule": Fraction(1, 5), "beyond": Fraction(1, 10)}
        self.assertFalse(drafted(A__levels__2__class_share=share)["A4"])

    def test_a3_needs_a_gap_and_both_shares_above_a_half(self):
        self.assertFalse(drafted(A__mix__gap=Fraction(0))["A3"])
        self.assertFalse(drafted(A__mix__gap=Fraction(-1, 10))["A3"])
        self.assertFalse(drafted(A__mix__mix_share_low_rates=Fraction(1, 2))["A3"])
        self.assertFalse(drafted(A__mix__mix_share_high_rates=None)["A3"])

    def test_b1_at_a_quarter(self):
        self.assertFalse(drafted(B__kinds={"idle": 1, "at_stake": 7})["B1"])

    def test_b2_at_three_quarters_and_with_no_strict_side(self):
        self.assertFalse(drafted(B__points={"hit": 2, "miss": 1})["B2"])
        self.assertFalse(drafted(B__points={"tie": 6})["B2"])

    def test_b3_is_strict(self):
        self.assertFalse(drafted(B__counterparts={"T1": {"shown": 2}})["B3"])

    def test_b4_in_every_run_under_either(self):
        bad = {"L3 r1": {"points_changed": 1343, "arrivals_changed": 19},
               "L3 r2": {"points_changed": 1344, "arrivals_changed": 0}}
        self.assertFalse(drafted(B__translations__T2__runs=bad)["B4"])
        bad = {"L3 r1": {"points_changed": 0, "arrivals_changed": 20}}
        self.assertFalse(drafted(B__translations__T1__runs=bad)["B4"])

    def test_c1_is_strict_and_needs_a_decider(self):
        self.assertFalse(drafted(**{"C__runs__L2 r2__decided": 4})["C1"])
        self.assertFalse(drafted(**{"C__runs__L2 r3__deciders": []})["C1"])

    def test_c2_and_c3_read_the_top_rule(self):
        top = [{"rule_id": "R1", "decided": 2, "queue": "T1_GENERAL", "keyword_rule": True}]
        self.assertFalse(drafted(**{"C__runs__L2 r1__deciders": top})["C2"])
        top = [{"rule_id": "R1", "decided": 2, "queue": R.T2, "keyword_rule": False}]
        self.assertFalse(drafted(**{"C__runs__L2 r1__deciders": top})["C3"])

    def test_c4_reads_wrong_decisions_only(self):
        tickets = [{"outcome": "ACTION", "right": False, "class_rules": ["R5"]}]
        self.assertFalse(drafted(**{"C__runs__L2 r3__tickets": tickets})["C4"])


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_reading_a_record(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(R, "load_runs",
                               side_effect=AssertionError("read")) as read:
            with self.assertRaises(SystemExit):
                R.main([])
        read.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(R.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
