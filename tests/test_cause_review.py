"""
`cause/review.py` — the POST-RUN reading of which queue the review notice
names, and why, no figure of the reading.

What is pinned:
- the code's window, matched where the governing rule or its queue comes before
  a word of the mark, and refused after it, too far before it, or inside a
  longer word;
- the places of a named queue in a ticket's list, and the support ladder;
- answers on real tickets: 1998, where the runner-up's queue is drafted nested
  in the governing rule and in the runner-up, a later queue and the governing
  one; and 102, which only the catch-all matches, where the tier above is named;
- that a session's reading keeps every valid answer of its arms, of any queue;
- the development counts recomputed on pass 1, which gate 4 reads;
- the four gates, each failing on its own;
- the expectation's clauses at their edges, and clauses without value;
- the record's fractions, its `_env`, what it keeps of each arm, and that it is
  POST-RUN;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from cause import plan
from cause import review as R
from whole import references

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
WORLD = references._world()
QUEUES = WORLD[4]
SEVEN = sorted(plan.ONCALL)


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


class TestTheCode(unittest.TestCase):

    def test_the_governing_rule_or_its_queue_before_the_mark(self):
        self.assertTrue(R.mark("H18 sends it to T2. But the reviewer marked it wrong.",
                               "H18", "T2_TECHNICAL"))
        self.assertTrue(R.mark("the engine routed it to T2_TECHNICAL; the revisor disagrees",
                               "H18", "T2_TECHNICAL"))
        self.assertTrue(R.mark("H18 applies, y el revisor la marca como errónea",
                               "H18", "T2_TECHNICAL"))
        self.assertTrue(R.mark("H18 applies. REVIEWER: no", "H18", "T2_TECHNICAL"))

    def test_refused(self):
        after = "The reviewer says so. The decision was made by H18."
        self.assertIsNone(R.mark(after, "H18", "T2_TECHNICAL"))
        far = "H18" + "x" * (R.BEFORE + 1) + " reviewer"
        self.assertIsNone(R.mark(far, "H18", "T2_TECHNICAL"))
        self.assertIsNone(R.mark("H180 then the reviewer", "H18", "T2_TECHNICAL"))
        self.assertIsNone(R.mark("T2_TECHNICAL_X then the reviewer", "H18", "T2_TECHNICAL"))
        self.assertIsNone(R.mark("H18, then something wrongly placed", "H18", "T2_TECHNICAL"))
        self.assertIsNone(R.mark(None, "H18", "T2_TECHNICAL"))

    def test_the_window_ends_at_the_mark(self):
        got = R.mark("abc H18 def reviewer ghi", "H18", "T2_TECHNICAL")
        self.assertTrue(got.endswith("reviewer"))
        self.assertIn("H18", got)


class TestPlaces(unittest.TestCase):

    def test_queues_in_order(self):
        self.assertEqual(R.queues_in_order(["H01", "H03", "H28", "H29"], QUEUES),
                         ["SECURITY_INCIDENT", "T2_TECHNICAL", "T1_GENERAL"])

    def test_place(self):
        order = ["SECURITY_INCIDENT", "T2_TECHNICAL", "T1_GENERAL"]
        self.assertEqual(R.place("SECURITY_INCIDENT", order), R.GOVERNING)
        self.assertEqual(R.place("T2_TECHNICAL", order), R.RUNNER_UP)
        self.assertEqual(R.place("T1_GENERAL", order), R.LATER)
        self.assertEqual(R.place("BILLING_SPECIALIST", order), R.UNMATCHED)
        self.assertEqual(R.place(None, order), R.UNMATCHED)

    def test_the_ladder(self):
        self.assertEqual(R.tier_above("T1_GENERAL"), "T2_TECHNICAL")
        self.assertEqual(R.tier_above("T2_TECHNICAL"), "T3_ENGINEERING")
        self.assertIsNone(R.tier_above("T3_ENGINEERING"))
        self.assertIsNone(R.tier_above("ONCALL_ESCALATION"))


class TestAnAnswer(unittest.TestCase):

    def row(self, ticket, payload, arm="r", **kw):
        return {"arm": arm, "id": f"{arm}:{ticket}", "ticket": ticket, "payload": payload,
                "failure": None, "served_by": plan.PROVIDER_NAME,
                "reasoning": "H01 would send it to SECURITY_INCIDENT. But the reviewer...", **kw}

    def test_the_runner_up_nested_in_both(self):
        p = {"action": "T2_TECHNICAL", "beats": [], "loses_to": [], "note": "un subcaso de H01",
             "conditions": [cond("has_security_keyword", "eq", True),
                            cond("customer_tier", "eq", "business"),
                            cond("severity", "gte", 3)]}
        x = R.answer(self.row(1998, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["runner_up"], x["runner_up_queue"], x["place"]),
                         ("H01", "H03", "T2_TECHNICAL", R.RUNNER_UP))
        self.assertEqual(x["queues_in_order"], ["SECURITY_INCIDENT", "T2_TECHNICAL", "T1_GENERAL"])
        self.assertTrue(x["wrong_queue"])
        self.assertEqual(x["first_of_the_named_queue"], "H03")
        self.assertTrue(x["inside_the_governing_rule"])
        self.assertTrue(x["inside_the_named_queue_rule"])
        self.assertFalse(x["is_their_intersection"])
        self.assertTrue(x["covers_its_ticket"])
        self.assertFalse(x["declares"])
        self.assertTrue(x["MARK"])
        self.assertEqual(x["class"], "wrong_queue")

    def test_a_later_queue_and_the_governing_one(self):
        later = {"action": "T1_GENERAL", "beats": ["H01"], "loses_to": [], "note": "",
                 "conditions": [cond("customer_tier", "eq", "business")]}
        x = R.answer(self.row(1998, later), "pass2", WORLD)
        self.assertEqual((x["place"], x["first_of_the_named_queue"]), (R.LATER, "H28"))
        self.assertFalse(x["inside_the_governing_rule"])
        self.assertTrue(x["inside_the_named_queue_rule"])
        self.assertTrue(x["beats_the_governing_rule"])
        right = {"action": "SECURITY_INCIDENT", "beats": [], "loses_to": [], "note": "",
                 "conditions": [cond("has_security_keyword", "eq", True)]}
        x = R.answer(self.row(1998, right), "pass2", WORLD)
        self.assertEqual(x["place"], R.GOVERNING)
        self.assertFalse(x["wrong_queue"])

    def test_the_tier_above_where_only_the_catch_all_matches(self):
        p = {"action": "T2_TECHNICAL", "beats": [], "loses_to": [], "note": "",
             "conditions": [cond("product", "eq", "mobile"), cond("customer_tier", "eq", "pro")]}
        x = R.answer(self.row(102, p), "pass2", WORLD)
        self.assertEqual((x["governing"], x["runner_up"], x["place"]), ("H29", None, R.UNMATCHED))
        self.assertTrue(x["names_the_tier_above"])
        self.assertIsNone(x["first_of_the_named_queue"])
        self.assertIsNone(x["inside_the_named_queue_rule"])
        self.assertTrue(x["inside_the_governing_rule"])

    def test_a_draft_naming_no_valid_condition(self):
        x = R.answer(self.row(102, {"action": "T2_TECHNICAL", "conditions": []}), "pass2", WORLD)
        self.assertIsNone(x["inside_the_governing_rule"])
        self.assertIsNone(x["covers_its_ticket"])

    def test_a_session_keeps_every_valid_answer_of_its_arms(self):
        p = {"action": "T2_TECHNICAL", "conditions": [cond("product", "eq", "mobile")]}
        rows = [self.row(102, p), self.row(102, p, arm="e"), self.row(102, p, failure="boom"),
                self.row(102, p, served_by="Baidu"), self.row(102, None)]
        self.assertEqual(len(R.read_session("pass2", rows, WORLD)), 2)
        self.assertEqual(len(R.read_session("pass2", rows, WORLD, arms=("r",))), 1)


class TestDevelopment(unittest.TestCase):

    def test_the_counts_come_back_on_pass_1(self):
        rows = json.loads(plan.ask_path("pass1").read_text())["rows"]
        self.assertEqual(R.development(rows, WORLD), (R.DEVELOPMENT, R.DEVELOPMENT_PLACES))

    def test_the_split(self):
        self.assertEqual(R.DEVELOPMENT_SESSIONS, ("pass1",))
        self.assertEqual(R.HELD_OUT, ("pass2", "oncall"))
        self.assertEqual(R.OTHERS, ("e", "v", "i"))


def ans(place=R.RUNNER_UP, arm="r", ticket=1, **kw):
    x = {"arm": arm, "ticket": ticket, "place": place, "wrong_queue": place != R.GOVERNING,
         "runner_up": "H03", "inside_the_governing_rule": True,
         "first_of_the_named_queue": "H03" if place in (R.RUNNER_UP, R.LATER) else None,
         "inside_the_named_queue_rule": True if place in (R.RUNNER_UP, R.LATER) else None,
         "names_the_tier_above": place == R.UNMATCHED, "MARK": arm == "r"}
    x.update(kw)
    return x


def holding() -> list[dict]:
    """Answers on which every clause holds."""
    xs = [ans() for _ in range(3)]
    xs += [ans(ticket=SEVEN[0]), ans(ticket=SEVEN[1])]
    xs += [ans(R.UNMATCHED, runner_up=None)]
    xs += [ans(arm=a) for a in ("e", "v", "i")]
    return xs


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, xs):
        return {c["clause"]: c["holds"] for c in R.expectation(xs)}

    def test_every_clause_holding(self):
        self.assertTrue(all(self.verdicts(holding()).values()))

    def test_the_edges(self):
        # V1: 7 of 10 at the runner-up is 0.70 and holds; 6 does not.
        for n, want in ((7, True), (6, False)):
            xs = [ans() if i < n else ans(R.LATER) for i in range(10)]
            with self.subTest(v1=n):
                self.assertEqual(self.verdicts(xs)["V1"], want)
        # V2: 4 of 5 inside the governing rule holds; 3 does not.
        for n, want in ((4, True), (3, False)):
            xs = [ans(inside_the_governing_rule=i < n) for i in range(5)]
            with self.subTest(v2=n):
                self.assertEqual(self.verdicts(xs)["V2"], want)
        # V5: the other arms' MARK at 1 in 4 holds, 2 in 4 does not.
        for n, want in ((1, True), (2, False)):
            xs = [ans()] * 10 + [ans(arm="e", MARK=i < n) for i in range(4)]
            with self.subTest(v5=n):
                self.assertEqual(self.verdicts(xs)["V5"], want)
        # V5: r's MARK at 9 in 10 holds, 8 in 10 does not.
        for n, want in ((9, True), (8, False)):
            xs = [ans(MARK=i < n) for i in range(10)] + [ans(arm="e")]
            with self.subTest(v5r=n):
                self.assertEqual(self.verdicts(xs)["V5"], want)
        # V6: exactly half at T7's tickets holds.
        xs = [ans(ticket=SEVEN[0]), ans(R.LATER, ticket=SEVEN[1])]
        self.assertTrue(self.verdicts(xs)["V6"])

    def test_clauses_without_value_fail(self):
        got = self.verdicts([ans(R.GOVERNING)])
        self.assertFalse(got["V1"])     # no wrong-queue answer
        self.assertFalse(got["V4"])     # none naming an unmatched queue
        self.assertFalse(got["V5"])     # no answer of another arm
        self.assertFalse(got["V6"])     # none at T7's tickets

    def test_the_lines(self):
        self.assertEqual((R.V1_LINE, R.V2_LINE, R.V3_LINE, R.V4_LINE, R.V5_R, R.V5_OTHERS,
                          R.V6_LINE),
                         (Fraction(7, 10), Fraction(4, 5), Fraction(4, 5), Fraction(7, 10),
                          Fraction(9, 10), Fraction(1, 4), Fraction(1, 2)))


class TestTheGates(unittest.TestCase):

    def records(self):
        row = {"arm": "e", "ticket": 1, "payload": {"a": 1}, "reasoning": "r",
               "failure": None, "served_by": plan.PROVIDER_NAME}
        return {s: {"rows": [dict(row)]} for s in R.SESSIONS}

    def stage_c(self, n=2):
        return {"CA-g": {"classes": {"e": {"whole": n}, "v": {}, "i": {}, "r": {}}}}

    def run_gates(self, records, stage_c, dev=None):
        dev = dev or (R.DEVELOPMENT, R.DEVELOPMENT_PLACES)
        with mock.patch.object(R.W, "classed", return_value="whole"), \
             mock.patch.object(R, "development", return_value=dev):
            return {g["gate"]: g["passes"] for g in R.gates(records, stage_c, WORLD)}

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

    def test_fractions_private_keys_env_and_what_is_kept(self):
        r = {"session": "pass2", "arm": "r", "id": "r:1", "ticket": 1, "governing": "H29",
             "MARK": True, "mark_window": "w", "note": "kept"}
        e = {**r, "arm": "e", "id": "e:1", "note": "dropped"}
        got = R.record_of({"passes": True}, [], [], [],
                          [{"clause": "V1", "holds": True, "reading": Fraction(1, 3)}])
        self.assertEqual(next(iter(got)), "_env")
        self.assertEqual(got["expectation"][0]["reading"], {"fraction": "1/3", "value": 1 / 3})
        kept = R.kept([r, e])
        self.assertEqual(kept[0]["note"], "kept")
        self.assertNotIn("note", kept[1])
        self.assertEqual(kept[1]["mark_window"], "w")
        self.assertEqual(R.jsonable({"_private": 1, "kept": 2}), {"kept": 2})

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", R.PROVENANCE)
        self.assertIn("before the reading ran", R.PROVENANCE)
        self.assertEqual(R.record_path(), plan.OUT / "review.json")


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
                    R.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
