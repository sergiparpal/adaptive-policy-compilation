"""
`halves/hidden.py` — the POST-RUN reading of why the hidden half cuts, no figure
of the reading.

What is pinned:
- the codebook's anchored patterns, each matched and each refused where a
  longer word, another phrase or a distant impasse would fool it;
- an answer on a real ticket, 1432, read whole and read cut by the first
  crossing rule, with its note and its declarations;
- that a session's reading keeps only valid answers of the right queue;
- the development counts recomputed on pass 1, which gate 4 reads;
- the four gates, each failing on its own;
- the expectation's clauses at their edges, and a clause without value;
- the record's fractions, its `_env`, and that it is POST-RUN;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from halves import hidden as H
from halves import plan
from reasoned_loop import references as rl_refs
from whole import references

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
WORLD = references._world()


def codes(reasoning="", note=""):
    return H.codes(reasoning, note)


class TestTheCodebook(unittest.TestCase):

    def test_conflict_reads_only_after_an_impasse(self):
        self.assertTrue(codes("Why the impasse? Because H16 and H28 conflict.")["CONFLICT"])
        self.assertTrue(codes("The impasse: both rules match the ticket.")["CONFLICT"])
        self.assertTrue(codes("impasse, as neither rule contains the other")["CONFLICT"])
        self.assertTrue(codes("impasse: the engine cannot decide between them")["CONFLICT"])
        self.assertFalse(codes("They conflict. No word of the frame here.")["CONFLICT"])
        far = "impasse" + "x" * (H.WINDOW + 10) + " conflict"
        self.assertFalse(codes(far)["CONFLICT"])
        self.assertFalse(codes("impasse, nonconflicting rules")["CONFLICT"])

    def test_between_two_listed_rules(self):
        self.assertTrue(codes("a conflict between H16 and H28")["BETWEEN"])
        self.assertTrue(codes("el conflicto entre H04 y H07")["BETWEEN"])
        self.assertFalse(codes("between H1 and H2")["BETWEEN"])
        self.assertFalse(codes("between H30 and H31")["BETWEEN"])
        self.assertFalse(codes("between H16, H28 and H29")["BETWEEN"])

    def test_empty(self):
        for text in ("there are no rules yet", "The base is empty.", "la base vacía",
                     "Since this is the first rule, nothing to declare.",
                     "al ser la primera regla"):
            with self.subTest(text=text):
                self.assertTrue(codes(text)["EMPTY"])
        for text in ("no rulesets", "Se aplica la primera regla de la lista",
                     "the first rule of the list"):
            with self.subTest(text=text):
                self.assertFalse(codes(text)["EMPTY"])

    def test_hidden(self):
        for text in ("BASE DE REGLAS: no se te muestra en este paso", "the base is not shown",
                     "a hidden base", "la base oculta"):
            with self.subTest(text=text):
                self.assertTrue(codes(text)["HIDDEN"])
        for text in ("unhidden", "reglas ocultas"):
            with self.subTest(text=text):
                self.assertFalse(codes(text)["HIDDEN"])

    def test_the_note_codes(self):
        self.assertTrue(codes(note="Es un subcaso de H12")["INSIDE"])
        self.assertTrue(codes(note="cubre la intersección de H16 y H28")["INSIDE"])
        self.assertTrue(codes(note="contained in both")["INSIDE"])
        self.assertFalse(codes(note="an insider's rule")["INSIDE"])
        self.assertFalse(codes(reasoning="caso particular")["INSIDE"])   # read in the note
        self.assertTrue(codes(note="resuelve el conflicto")["RESOLVES"])
        self.assertFalse(codes(note="irresolute")["RESOLVES"])

    def test_windows(self):
        text = "a impasse b IMPASSE c"
        self.assertEqual(len(H.windows(text)), 2)
        self.assertEqual(H.windows(None), [])


class TestAnAnswer(unittest.TestCase):

    def setUp(self):
        self.gov = rl_refs.governing(WORLD[1][1432])
        self.whole = {**rl_refs.payload_of(self.gov), "note": "H04 sobre H07",
                      "beats": ["H07"], "loses_to": []}
        self.cut = {**self.whole, "beats": [], "note": "Es la intersección de H04 y H07",
                    "conditions": self.whole["conditions"]
                    + [{"attr": "product", "op": "eq", "value": "api"}]}

    def row(self, payload, **kw):
        return {"arm": "h", "id": "x", "ticket": 1432, "payload": payload, "failure": None,
                "served_by": plan.PROVIDER_NAME, "reasoning": "impasse: H04 and H07 overlap",
                **kw}

    def test_whole(self):
        x = H.answer(self.row(self.whole), "pass2", WORLD)
        self.assertEqual((x["class"], x["kind"], x["governing"], x["first_crossing"]),
                         ("whole", "whole", "H04", "H07"))
        self.assertIsNone(x["cut_by"])
        self.assertTrue(x["note_cites_a_crossing_rule"])
        self.assertTrue(x["declares_against_a_crossing_rule"])
        self.assertFalse(x["declares_against_the_governing_rule"])
        self.assertTrue(x["codes"]["CONFLICT"])

    def test_cut_by_the_first_crossing_rule(self):
        x = H.answer(self.row(self.cut), "pass2", WORLD)
        self.assertEqual(x["kind"], "cut")
        self.assertIn("H07", x["cut_by"])
        self.assertTrue(x["cut_by_the_first_crossing"])
        self.assertTrue(x["codes"]["INSIDE"])
        self.assertFalse(x["declares"])

    def test_a_session_keeps_valid_right_queue_answers(self):
        wrong = {**self.whole, "action": "T1_GENERAL"}
        rows = [self.row(self.whole), self.row(self.whole, failure="boom"),
                self.row(self.whole, served_by="Baidu"), self.row(wrong),
                self.row({})]
        got = H.read_session("pass2", rows, WORLD)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["session"], "pass2")


class TestDevelopment(unittest.TestCase):

    def test_the_counts_come_back_on_pass_1(self):
        rows = json.loads(plan.ask_path("pass1").read_text())["rows"]
        self.assertEqual(H.development(rows, WORLD), (H.DEVELOPMENT, H.DEVELOPMENT_ANSWERS))

    def test_the_split(self):
        self.assertEqual(H.DEVELOPMENT_SESSIONS, ("pass1",))
        self.assertEqual(H.HELD_OUT, ("pass2", "oncall"))
        self.assertEqual(set(H.CODES), set(H.READ_IN))


def ans(arm, kind, **codes_on):
    c = {k: False for k in H.CODES}
    c.update(codes_on)
    return {"arm": arm, "kind": kind, "codes": c, "cut_by_the_first_crossing": True,
            "note_cites_a_crossing_rule": True, "declares": False,
            "declares_against_a_crossing_rule": False,
            "declares_against_the_governing_rule": False}


def holding() -> list[dict]:
    """Answers on which every clause holds."""
    xs = []
    xs += [ans("h", "whole", CONFLICT=True, HIDDEN=True)] * 2
    xs += [ans("h", "cut", CONFLICT=True)] * 2
    xs += [ans("e", "whole", EMPTY=True)] * 4
    xs += [ans("e", "cut", EMPTY=True, BETWEEN=True, CONFLICT=True)]
    xs += [ans("o", "whole", EMPTY=True), ans("o", "cut")]
    return xs


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, xs):
        return {c["clause"]: c["holds"] for c in H.expectation(xs)}

    def test_every_clause_holding(self):
        self.assertTrue(all(self.verdicts(holding()).values()))

    def test_the_edges(self):
        # Q1: 17 of 20 cuts by the first crossing rule is 0.85 and holds; 16 does not.
        for n, want in ((17, True), (16, False)):
            xs = [ans("v", "cut") for _ in range(20)]
            for x in xs[n:]:
                x["cut_by_the_first_crossing"] = False
            with self.subTest(q1=n):
                self.assertEqual(self.verdicts(xs)["Q1"], want)
        # Q4: h's EMPTY at most 3 in 20 holds, 4 does not.
        for n, want in ((3, True), (4, False)):
            xs = [ans("h", "whole", EMPTY=i < n) for i in range(20)]
            xs += [ans("e", "whole", EMPTY=True)] * 5
            with self.subTest(q4=n):
                self.assertEqual(self.verdicts(xs)["Q4"], want)
        # Q6: a gap of exactly 1/4 holds.
        xs = [ans("h", "whole", HIDDEN=True), ans("h", "whole")] * 2
        xs += [ans("h", "cut", HIDDEN=True)] + [ans("h", "cut")] * 3
        self.assertTrue(self.verdicts(xs)["Q6"])

    def test_a_clause_without_value_fails(self):
        got = self.verdicts([ans("h", "whole", HIDDEN=True)])
        self.assertFalse(got["Q6"])     # no cut of h: no share, no value
        self.assertFalse(got["Q5"])     # no answer of o
        self.assertFalse(got["Q3"])     # no answer of e

    def test_the_lines(self):
        self.assertEqual((H.Q1_LINE, H.Q2_H, H.Q2_GAP, H.Q3_GAP, H.Q4_E, H.Q4_H, H.Q5_GAP,
                          H.Q6_GAP),
                         (Fraction(85, 100), Fraction(9, 10), Fraction(1, 4), Fraction(1, 10),
                          Fraction(4, 5), Fraction(3, 20), Fraction(1, 4), Fraction(1, 4)))


class TestTheGates(unittest.TestCase):

    def records(self):
        row = {"arm": "e", "ticket": 1, "payload": {"a": 1}, "reasoning": "r",
               "failure": None, "served_by": plan.PROVIDER_NAME}
        return {s: {"rows": [dict(row)]} for s in H.SESSIONS}

    def stage_c(self, n=2):
        return {"HV-g": {"classes": {"e": {"whole": n}, "v": {}, "h": {}, "o": {}}}}

    def run_gates(self, records, stage_c, dev=None):
        dev = dev or (H.DEVELOPMENT, H.DEVELOPMENT_ANSWERS)
        with mock.patch.object(H.W, "classed", return_value="whole"), \
             mock.patch.object(H, "development", return_value=dev):
            return {g["gate"]: g["passes"] for g in H.gates(records, stage_c, WORLD)}

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
        got = H.record_of({"passes": True}, [], [], [], [{"clause": "Q1", "holds": True,
                                                           "reading": Fraction(1, 3)}])
        self.assertEqual(next(iter(got)), "_env")
        self.assertEqual(got["expectation"][0]["reading"], {"fraction": "1/3",
                                                             "value": 1 / 3})
        self.assertEqual(H.jsonable({"_private": 1, "kept": 2}), {"kept": 2})

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", H.PROVENANCE)
        self.assertIn("before the reading ran", H.PROVENANCE)
        self.assertEqual(H.record_path(), plan.OUT / "hidden.json")


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
                    H.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
