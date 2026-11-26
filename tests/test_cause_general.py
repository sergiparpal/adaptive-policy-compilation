"""
`cause/general.py` — the POST-RUN reading of why the impasse notice cuts at
`T1_GENERAL`'s tickets, no figure of the reading.

What is pinned:
- the codebook's anchored patterns: `ABSENT` matched on the governing rule in
  either order within one sentence, and refused on another rule, across a
  sentence, too far, or inside a longer word; `GAP` matched in its two
  languages and refused inside a longer word or where the rules are said to
  cover;
- answers on real tickets: 1, which only the catch-all matches, drafted as the
  ticket's own combination and as the catch-all whole; and 566, of another rule;
- that a session's reading keeps only valid answers of the right queue, of the
  three arms it reads;
- the development counts recomputed on pass 1, which gate 4 reads;
- the four gates, each failing on its own;
- the expectation's clauses at their edges, and clauses without value;
- the record's fractions, its `_env`, and that it is POST-RUN;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from cause import general as G
from cause import plan
from whole import references

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
WORLD = references._world()


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


class TestTheCodebook(unittest.TestCase):

    def test_absent_matched(self):
        for text, rule in (("H29 is not present in the base", "H29"),
                           ("That means H29 is not in the base?", "H29"),
                           ("the motor's base is missing H08", "H08"),
                           ("maybe the base lacks H28", "H28"),
                           ("H28 no está en la base", "H28"),
                           ("Since H29 is apparently absent", "H29")):
            with self.subTest(text=text):
                self.assertTrue(G.absent(text, rule))

    def test_absent_refused(self):
        far = "H29" + " x" * (G.AFTER // 2 + 1) + " missing"
        for text, rule in (("H28 is missing", "H29"),
                           ("H29 matches. Something else is missing", "H29"),
                           (far, "H29"),
                           ("H290 is missing", "H29"),
                           ("H29 keeps dismissing it", "H29"),
                           ("", "H29")):
            with self.subTest(text=text):
                self.assertIsNone(G.absent(text, rule))
        self.assertIsNone(G.absent(None, "H29"))

    def test_gap(self):
        for note in ("Fills gap for pro tier", "La regla propuesta llena ese vacío",
                     "not covered by any existing rule", "tickets no cubiertos por las reglas",
                     "Ninguna regla existente cubre tickets de tier pro", "no rule covers this",
                     "none of the existing rules apply", "cubre los huecos", "the gaps left"):
            with self.subTest(note=note):
                self.assertTrue(G.gap(note))
        for note in ("fulfills the policy", "a gapless list", "the existing rules cover it",
                     "rellenar el formulario", ""):
            with self.subTest(note=note):
                self.assertFalse(G.gap(note))
        self.assertFalse(G.gap(None))


class TestAnAnswer(unittest.TestCase):

    def row(self, ticket, payload, arm="i", **kw):
        return {"arm": arm, "id": f"{arm}:{ticket}", "ticket": ticket, "payload": payload,
                "failure": None, "served_by": plan.PROVIDER_NAME,
                "reasoning": "H29 should apply. That means H29 is not present?", **kw}

    def test_the_tickets_own_combination(self):
        p = {"action": "T1_GENERAL", "beats": [], "loses_to": [],
             "note": "Fills gap for pro tier, dashboard product, severity 3",
             "conditions": [cond("product", "eq", "dashboard"), cond("severity", "eq", 3),
                            cond("customer_tier", "eq", "pro")]}
        x = G.answer(self.row(1, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["place"], x["class"], x["kind"]),
                         ("H29", G.THREE, "other", G.NOT_WHOLE))
        self.assertTrue(x["inside_the_governing_rule"])
        self.assertTrue(x["covers_its_ticket"])
        self.assertTrue(G.is_a_narrowing(x))
        self.assertLess(x["part_held"], x["part_points"])
        self.assertEqual(x["codes"], {"ABSENT": True, "GAP": True})
        self.assertIn("H29", x["absent_span"])

    def test_the_catch_all_whole(self):
        p = {"action": "T1_GENERAL", "beats": [], "loses_to": [], "note": "Catch-all",
             "conditions": [cond("severity", "gte", 1)]}
        x = G.answer(self.row(1, p, reasoning="no word of absence"), "pass2", WORLD)
        self.assertEqual((x["class"], x["kind"]), ("whole", G.WHOLE))
        self.assertEqual(x["part_held"], x["part_points"])
        self.assertEqual(x["codes"], {"ABSENT": False, "GAP": False})
        self.assertFalse(G.is_a_narrowing(x))

    def test_another_rules_ticket(self):
        p = {"action": "T2_TECHNICAL", "beats": [], "loses_to": [], "note": "",
             "conditions": [cond("product", "eq", "integrations")]}
        x = G.answer(self.row(566, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["place"], x["class"]), ("H18", G.OTHERS, "whole"))
        self.assertFalse(x["codes"]["ABSENT"])      # the reasoning names H29, not H18

    def test_a_session_keeps_valid_right_queue_answers_of_its_arms(self):
        p = {"action": "T1_GENERAL", "conditions": [cond("severity", "gte", 1)]}
        wrong = {**p, "action": "T2_TECHNICAL"}
        rows = [self.row(1, p), self.row(1, p, arm="e"), self.row(1, p, arm="r"),
                self.row(1, wrong), self.row(1, p, failure="boom"),
                self.row(1, p, served_by="Baidu"), self.row(1, {})]
        got = G.read_session("pass2", rows, WORLD)
        self.assertEqual(sorted(x["arm"] for x in got), ["e", "i"])


class TestDevelopment(unittest.TestCase):

    def test_the_counts_come_back_on_pass_1(self):
        rows = json.loads(plan.ask_path("pass1").read_text())["rows"]
        self.assertEqual(G.development(rows, WORLD), (G.DEVELOPMENT, G.DEVELOPMENT_ANSWERS))

    def test_the_split_and_the_three(self):
        self.assertEqual(G.DEVELOPMENT_SESSIONS, ("pass1",))
        self.assertEqual(G.HELD_OUT, ("pass2", "oncall"))
        self.assertEqual(G.ARMS, ("e", "v", "i"))
        self.assertEqual(G.THE_THREE, ("H08", "H28", "H29"))
        self.assertEqual(set(G.CODES), set(G.READ_IN))


def ans(arm="i", place=G.THREE, k=G.NOT_WHOLE, cls=None, absent=True, gap=True, **kw):
    x = {"arm": arm, "place": place, "kind": k,
         "class": cls or ("whole" if k == G.WHOLE else "other"),
         "inside_the_governing_rule": True, "covers_its_ticket": True,
         "codes": {"ABSENT": absent, "GAP": gap}}
    x.update(kw)
    return x


def holding() -> list[dict]:
    """Answers on which every clause holds."""
    xs = [ans() for _ in range(2)]
    xs += [ans(place=G.OTHERS, k=G.WHOLE, gap=False)] * 5
    xs += [ans(place=G.OTHERS)]
    xs += [ans("v")]
    xs += [ans("e", absent=False, gap=False), ans("e", k=G.WHOLE, absent=False, gap=False)]
    return xs


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, xs):
        return {c["clause"]: c["holds"] for c in G.expectation(xs)}

    def test_every_clause_holding(self):
        self.assertTrue(all(self.verdicts(holding()).values()))

    def test_the_edges(self):
        # D1: e's ABSENT at 2 in 5 holds, 3 in 5 does not.
        for n, want in ((2, True), (3, False)):
            xs = [ans()] + [ans("e", absent=i < n, gap=False) for i in range(5)]
            with self.subTest(d1=n):
                self.assertEqual(self.verdicts(xs)["D1"], want)
        # D2: 4 of 5 narrowings holds; 3 does not.
        for n, want in ((4, True), (3, False)):
            xs = [ans(cls="other" if i < n else "cut_by_one") for i in range(5)]
            with self.subTest(d2=n):
                self.assertEqual(self.verdicts(xs)["D2"], want)
        # D5: e's GAP at 3 in 20 holds, 4 in 20 does not.
        for n, want in ((3, True), (4, False)):
            xs = [ans("e", gap=i < n) for i in range(20)]
            with self.subTest(d5=n):
                self.assertEqual(self.verdicts(xs)["D5"], want)
        # D6: exactly half holds.
        xs = [ans(place=G.OTHERS), ans(place=G.OTHERS, gap=False)]
        self.assertTrue(self.verdicts(xs)["D6"])

    def test_a_narrowing_must_cover_its_ticket_inside_the_rule(self):
        self.assertTrue(G.is_a_narrowing(ans()))
        self.assertFalse(G.is_a_narrowing(ans(covers_its_ticket=False)))
        self.assertFalse(G.is_a_narrowing(ans(inside_the_governing_rule=False)))
        self.assertFalse(G.is_a_narrowing(ans(cls="cut_by_one")))

    def test_clauses_without_value_fail(self):
        got = self.verdicts([ans()])
        self.assertFalse(got["D1"])     # no answer of e
        self.assertFalse(got["D3"])     # no answer of v
        self.assertFalse(got["D4"])     # no whole answer of i at the other tickets
        self.assertFalse(got["D5"])
        self.assertFalse(got["D6"])     # no answer of i not whole at the other tickets

    def test_the_lines(self):
        self.assertEqual((G.D1_I, G.D1_E, G.D2_LINE, G.D3_LINE, G.D4_THREE, G.D4_WHOLE_OTHERS,
                          G.D5_LINE, G.D6_LINE),
                         (Fraction(9, 10), Fraction(2, 5), Fraction(4, 5), Fraction(3, 5),
                          Fraction(3, 5), Fraction(1, 5), Fraction(3, 20), Fraction(1, 2)))


class TestTheGates(unittest.TestCase):

    def records(self):
        row = {"arm": "e", "ticket": 1, "payload": {"a": 1}, "reasoning": "r",
               "failure": None, "served_by": plan.PROVIDER_NAME}
        return {s: {"rows": [dict(row)]} for s in G.SESSIONS}

    def stage_c(self, n=2):
        return {"CA-g": {"classes": {"e": {"whole": n}, "v": {}, "i": {}, "r": {}}}}

    def run_gates(self, records, stage_c, dev=None):
        dev = dev or (G.DEVELOPMENT, G.DEVELOPMENT_ANSWERS)
        with mock.patch.object(G.W, "classed", return_value="whole"), \
             mock.patch.object(G, "development", return_value=dev):
            return {g["gate"]: g["passes"] for g in G.gates(records, stage_c, WORLD)}

    def test_every_gate_passing(self):
        self.assertTrue(all(self.run_gates(self.records(), self.stage_c()).values()))

    def test_each_gate_failing(self):
        r = self.records()
        r["oncall"]["rows"][0]["served_by"] = "Baidu"
        self.assertEqual(self.run_gates(r, self.stage_c()),
                         {1: False, 2: True, 3: True, 4: True})
        self.assertEqual(self.run_gates(self.records(), self.stage_c(3)),
                         {1: True, 2: False, 3: True, 4: True})
        r = self.records()
        r["pass2"]["rows"][0]["reasoning"] = ""
        self.assertEqual(self.run_gates(r, self.stage_c()),
                         {1: True, 2: True, 3: False, 4: True})
        self.assertEqual(self.run_gates(self.records(), self.stage_c(), dev=({}, {})),
                         {1: True, 2: True, 3: True, 4: False})


class TestTheRecord(unittest.TestCase):

    def test_fractions_private_keys_and_env(self):
        got = G.record_of({"passes": True}, [], [], [],
                          [{"clause": "D1", "holds": True, "reading": Fraction(1, 3)}])
        self.assertEqual(next(iter(got)), "_env")
        self.assertEqual(got["expectation"][0]["reading"], {"fraction": "1/3", "value": 1 / 3})
        self.assertEqual(got["the_three_rules"], ["H08", "H28", "H29"])

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", G.PROVENANCE)
        self.assertIn("before the reading ran", G.PROVENANCE)
        self.assertEqual(G.record_path(), plan.OUT / "general.json")


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    G.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
