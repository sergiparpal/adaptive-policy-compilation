"""
`cause/narrow.py` — the POST-RUN reading of why the model narrows a missing
default, no figure of the reading.

What is pinned:
- the codebook: a sentence's bounds; `INSIDE` matched where a draft is placed
  inside the governing rule, in both orders and both languages, and refused on
  another rule, across a sentence, inside a longer identifier or where the
  governing rule holds the ticket and not the draft; `CONTAINER` matched where
  the other rules lie inside the draft or the draft yields to them, and refused
  where the draft is the more specific rule or yields to one rule by name;
- the structure: what the regions of `H08`, `H18` and `H29` hold of the rules of
  another queue, and the groups' bounds;
- answers on real tickets: 1, which only the catch-all matches, drafted as the
  ticket's own combination and as the catch-all whole; and 566, of a rule of the
  few;
- that a session's reading keeps only valid answers of the right queue, of the
  three arms it reads;
- the development counts recomputed on pass 1, which gate 4 reads, over the
  answers `cause/general.py` read there;
- the five gates, each failing on its own;
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
from cause import narrow as N
from cause import plan
from whole import references

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
WORLD = references._world()


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


class TestTheCodebook(unittest.TestCase):

    def test_sentences(self):
        self.assertEqual(N.sentences("A b. C d? E!\nF"), ["A b.", "C d?", "E!", "F"])
        self.assertEqual(N.sentences(None), [])

    def test_inside_matched(self):
        for text, rule in (
                ("So our rule is a subset of H08, so it would win over H08.", "H08"),
                ("If H08 exists, it contains our rule, so automatic.", "H08"),
                ("H29: if it existed, our rule would be contained, but it's not.", "H29"),
                ("it would be more specific than H29 (if H29 exists)", "H29"),
                ("If present, H29 would be a superset of it.", "H29"),
                ("Esta regla es un subconjunto de H28.", "H28"),
                ("Our rule is a strict subset of H08 and of H29.", "H29")):
            with self.subTest(text=text):
                self.assertTrue(N.inside(text, rule))

    def test_inside_refused(self):
        for text, rule in (
                ("our rule is a subset of H27", "H29"),
                ("So all rules are subsets of the catch-all.", "H29"),
                ("our rule is a subset. H29 is the catch-all.", "H29"),
                ("our rule is a subset of H290", "H29"),
                ("H29 would include our ticket if it existed.", "H29"),
                ("", "H29")):
            with self.subTest(text=text):
                self.assertIsNone(N.inside(text, rule))
        self.assertIsNone(N.inside(None, "H29"))

    def test_container_matched(self):
        for text in ("So all rules are subsets of catch-all.",
                     "So catch-all will automatically lose to all.",
                     "So my rule would automatically lose to H04-H07 because they are narrower.",
                     "The other rules are contained in ours.",
                     "Then the more specific rules will override it.",
                     "Es general, y las reglas más específicas la superan por contención."):
            with self.subTest(text=text):
                self.assertTrue(N.container(text))

    def test_container_refused(self):
        for text in ("the more specific rule (ours) would win automatically",
                     "our rule is a subset of H29",
                     "our rule would lose to H12",
                     "So automatically our rule wins.",
                     ""):
            with self.subTest(text=text):
                self.assertIsNone(N.container(text))
        self.assertIsNone(N.container(None))


class TestTheStructure(unittest.TestCase):

    def test_what_the_regions_hold(self):
        _, _, regions, _, queues = WORLD
        self.assertEqual(N.held(regions["H08"], "H08", regions, queues),
                         ["H04", "H05", "H06", "H07"])
        self.assertEqual(N.held(regions["H18"], "H18", regions, queues), ["H17"])
        self.assertEqual(len(N.held(regions["H29"], "H29", regions, queues)), 26)
        self.assertNotIn("H28", N.held(regions["H29"], "H29", regions, queues))  # its own queue

    def test_the_groups(self):
        self.assertEqual([N.group(n) for n in (0, 1, 3, 4, 26)],
                         [N.NONE, N.FEW, N.FEW, N.MANY, N.MANY])
        self.assertEqual(N.FEW_MAX, 3)


class TestAnAnswer(unittest.TestCase):

    def row(self, ticket, payload, arm="i", **kw):
        return {"arm": arm, "id": f"{arm}:{ticket}", "ticket": ticket, "payload": payload,
                "failure": None, "served_by": plan.PROVIDER_NAME,
                "reasoning": "H29 is missing. So our rule is a subset of H29, so it wins.", **kw}

    def test_the_tickets_own_combination(self):
        p = {"action": "T1_GENERAL", "beats": [], "loses_to": [], "note": "Fills gap",
             "conditions": [cond("product", "eq", "dashboard"), cond("severity", "eq", 3),
                            cond("customer_tier", "eq", "pro")]}
        x = N.answer(self.row(1, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["place"], x["group"], x["class"], x["kind"]),
                         ("H29", N.THREE, N.MANY, "other", N.NOT_WHOLE))
        self.assertEqual(len(x["governing_holds"]), 26)
        self.assertEqual(x["draft_holds"], [])
        self.assertTrue(x["inside_the_governing_rule"] and x["covers_its_ticket"])
        self.assertEqual(x["codes"], {"INSIDE": True, "CONTAINER": False, "HOLDS_NONE": True})
        self.assertIn("subset of H29", x["spans"]["INSIDE"])

    def test_the_catch_all_whole(self):
        p = {"action": "T1_GENERAL", "beats": [], "loses_to": [], "note": "Catch-all",
             "conditions": [cond("severity", "gte", 1)]}
        r = self.row(1, p, reasoning="So all rules are subsets of the catch-all.")
        x = N.answer(r, "pass2", WORLD)
        self.assertEqual((x["class"], x["kind"]), ("whole", N.WHOLE))
        self.assertEqual(len(x["draft_holds"]), 26)
        self.assertEqual(x["codes"], {"INSIDE": False, "CONTAINER": True, "HOLDS_NONE": False})

    def test_a_rule_of_the_few(self):
        p = {"action": "T2_TECHNICAL", "beats": [], "loses_to": [], "note": "",
             "conditions": [cond("product", "eq", "integrations")]}
        x = N.answer(self.row(566, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["place"], x["group"], x["class"]),
                         ("H18", N.OTHERS, N.FEW, "whole"))
        self.assertEqual(x["governing_holds"], ["H17"])
        self.assertFalse(x["codes"]["INSIDE"])      # the reasoning names H29, not H18

    def test_a_session_keeps_valid_right_queue_answers_of_its_arms(self):
        p = {"action": "T1_GENERAL", "conditions": [cond("severity", "gte", 1)]}
        wrong = {**p, "action": "T2_TECHNICAL"}
        rows = [self.row(1, p), self.row(1, p, arm="e"), self.row(1, p, arm="r"),
                self.row(1, wrong), self.row(1, p, failure="boom"),
                self.row(1, p, served_by="Baidu"), self.row(1, {})]
        got = N.read_session("pass2", rows, WORLD)
        self.assertEqual(sorted(x["arm"] for x in got), ["e", "i"])


class TestDevelopment(unittest.TestCase):

    def test_the_counts_come_back_on_pass_1(self):
        rows = json.loads(plan.ask_path("pass1").read_text())["rows"]
        self.assertEqual(N.development(rows, WORLD),
                         (N.DEVELOPMENT, N.DEVELOPMENT_ANSWERS, N.DEVELOPMENT_GROUPS))

    def test_the_answers_are_cause_general_s(self):
        self.assertEqual(N.DEVELOPMENT_ANSWERS, G.DEVELOPMENT_ANSWERS)

    def test_the_split_the_three_and_the_few(self):
        self.assertEqual(N.DEVELOPMENT_SESSIONS, ("pass1",))
        self.assertEqual(N.HELD_OUT, ("pass2", "oncall"))
        self.assertEqual(N.ARMS, ("e", "v", "i"))
        self.assertEqual(N.THE_THREE, ("H08", "H28", "H29"))
        self.assertEqual(N.THE_FEW, ("H03", "H12", "H16", "H18"))
        self.assertEqual(N.COUNTED, ("INSIDE", "CONTAINER", "HOLDS_NONE"))

    def test_the_structure_on_the_passes(self):
        rows = json.loads(plan.ask_path("pass1").read_text())["rows"]
        got = N.structure(rows, WORLD)
        self.assertEqual((got[N.MANY], got[N.FEW]), (list(N.THE_THREE), list(N.THE_FEW)))


def ans(arm="i", place=N.THREE, k=N.NOT_WHOLE, inside=True, container=False, holds_none=True,
        group=None, **kw):
    x = {"arm": arm, "place": place, "kind": k,
         "group": group or (N.MANY if place == N.THREE else N.NONE),
         "class": "whole" if k == N.WHOLE else "other",
         "codes": {"INSIDE": inside, "CONTAINER": container, "HOLDS_NONE": holds_none}}
    x.update(kw)
    return x


def holding() -> list[dict]:
    """Answers on which every clause holds."""
    xs = [ans() for _ in range(2)]
    xs += [ans(k=N.WHOLE, inside=False, container=True, holds_none=False)]
    xs += [ans("e")]
    xs += [ans("e", N.OTHERS, N.WHOLE, inside=False)] * 3
    xs += [ans("i", N.OTHERS, N.WHOLE, inside=False, group=N.FEW)] * 3
    xs += [ans("v")]
    return xs


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, xs):
        return {c["clause"]: c["holds"] for c in N.expectation(xs)}

    def test_every_clause_holding(self):
        got = self.verdicts(holding())
        self.assertEqual(sorted(got), ["S1", "S2", "S3", "S4", "S5", "S6"])
        self.assertTrue(all(got.values()))

    def test_the_edges(self):
        base = holding()
        # S1: 3 of 5 holds, 2 of 5 does not.
        for n, want in ((3, True), (2, False)):
            xs = [ans(inside=i < n) for i in range(5)] + [ans("e")]
            with self.subTest(s1=n):
                self.assertEqual(self.verdicts(xs)["S1"], want)
        # S2: whole answers with INSIDE at 1 in 4 holds, 2 in 4 does not.
        for n, want in ((1, True), (2, False)):
            xs = [ans()] + [ans(k=N.WHOLE, place=N.OTHERS, inside=i < n) for i in range(4)]
            with self.subTest(s2=n):
                self.assertEqual(self.verdicts(xs)["S2"], want)
        # S3: CONTAINER in 2 of 5 whole holds and 1 of 5 does not; 3 of 20 not whole holds,
        # 4 of 20 does not.
        for w, nw, want in ((2, 3, True), (1, 3, False), (2, 4, False)):
            xs = ([ans(k=N.WHOLE, container=i < w) for i in range(5)]
                  + [ans("v", container=i < nw) for i in range(20)])
            with self.subTest(s3=(w, nw)):
                self.assertEqual(self.verdicts(xs)["S3"], want)
        # S4: 17 of 20 holds, 16 of 20 does not.
        for n, want in ((17, True), (16, False)):
            xs = [ans("v", holds_none=i < n) for i in range(20)]
            with self.subTest(s4=n):
                self.assertEqual(self.verdicts(xs)["S4"], want)
        # S5: 7 of 10 whole holds, 6 of 10 does not.
        for n, want in ((7, True), (6, False)):
            xs = [ans(place=N.OTHERS, group=N.FEW, k=N.WHOLE if i < n else N.NOT_WHOLE)
                  for i in range(10)]
            with self.subTest(s5=n):
                self.assertEqual(self.verdicts(xs)["S5"], want)
        # S6: 3 of 5 holds, 2 of 5 does not.
        for n, want in ((3, True), (2, False)):
            xs = [ans("e", inside=i < n) for i in range(5)]
            with self.subTest(s6=n):
                self.assertEqual(self.verdicts(xs)["S6"], want)
        self.assertTrue(all(self.verdicts(base).values()))

    def test_clauses_without_value_fail(self):
        got = self.verdicts([ans()])
        self.assertTrue(got["S1"] and got["S4"])
        self.assertFalse(got["S2"])     # no whole answer of e or i
        self.assertFalse(got["S3"])     # no whole answer of v or i at the three rules' tickets
        self.assertFalse(got["S5"])     # no answer of i at the few's tickets
        self.assertFalse(got["S6"])     # no answer of e

    def test_the_lines(self):
        self.assertEqual((N.S1_LINE, N.S2_NOT_WHOLE, N.S2_WHOLE, N.S3_WHOLE, N.S3_NOT_WHOLE,
                          N.S4_LINE, N.S5_LINE, N.S6_LINE),
                         (Fraction(3, 5), Fraction(3, 4), Fraction(1, 4), Fraction(2, 5),
                          Fraction(3, 20), Fraction(17, 20), Fraction(7, 10), Fraction(3, 5)))


class TestTheGates(unittest.TestCase):

    def records(self):
        row = {"arm": "e", "ticket": 1, "payload": {"a": 1}, "reasoning": "r",
               "failure": None, "served_by": plan.PROVIDER_NAME}
        return {s: {"rows": [dict(row)]} for s in N.SESSIONS}

    def stage_c(self, n=2):
        return {"CA-g": {"classes": {"e": {"whole": n}, "v": {}, "i": {}, "r": {}}}}

    def found(self, many=None):
        return {N.NONE: [], N.FEW: list(N.THE_FEW), N.MANY: many or list(N.THE_THREE)}

    def run_gates(self, records, stage_c, dev=None, found=None):
        dev = dev or (N.DEVELOPMENT, N.DEVELOPMENT_ANSWERS, N.DEVELOPMENT_GROUPS)
        with mock.patch.object(N.W, "classed", return_value="whole"), \
             mock.patch.object(N, "development", return_value=dev), \
             mock.patch.object(N, "structure", return_value=found or self.found()):
            return {g["gate"]: g["passes"] for g in N.gates(records, stage_c, WORLD)}

    def test_every_gate_passing(self):
        self.assertTrue(all(self.run_gates(self.records(), self.stage_c()).values()))

    def test_each_gate_failing(self):
        ok = {1: True, 2: True, 3: True, 4: True, 5: True}
        r = self.records()
        r["oncall"]["rows"][0]["served_by"] = "Baidu"
        self.assertEqual(self.run_gates(r, self.stage_c()), {**ok, 1: False})
        self.assertEqual(self.run_gates(self.records(), self.stage_c(3)), {**ok, 2: False})
        r = self.records()
        r["pass2"]["rows"][0]["reasoning"] = ""
        self.assertEqual(self.run_gates(r, self.stage_c()), {**ok, 3: False})
        self.assertEqual(self.run_gates(self.records(), self.stage_c(), dev=({}, {}, {})),
                         {**ok, 4: False})
        self.assertEqual(self.run_gates(self.records(), self.stage_c(),
                                        found=self.found(many=["H08"])),
                         {**ok, 5: False})


class TestTheRecord(unittest.TestCase):

    def test_fractions_private_keys_and_env(self):
        got = N.record_of({"passes": True}, [], [], [],
                          [{"clause": "S1", "holds": True, "reading": Fraction(1, 3)}])
        self.assertEqual(next(iter(got)), "_env")
        self.assertEqual(got["expectation"][0]["reading"], {"fraction": "1/3", "value": 1 / 3})
        self.assertEqual(got["the_three_rules"], ["H08", "H28", "H29"])
        self.assertEqual(got["the_few_rules"], ["H03", "H12", "H16", "H18"])

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", N.PROVENANCE)
        self.assertIn("before the reading ran", N.PROVENANCE)
        self.assertEqual(N.record_path(), plan.OUT / "narrow.json")


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
                    N.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
