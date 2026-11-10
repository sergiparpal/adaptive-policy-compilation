"""
`whole/paragraph.py` — the POST-RUN reading of whether the blind paragraph is why
the loop's first call cuts, no figure of the reading.

What is pinned:
- an answer classed as Stage C classes a first-call draft, on a real ticket: the
  governing rule's region whole, a wrong queue and no rule;
- a group's share over right-queue answers, and the ticket-weighted share;
- the five gates, each failing on its own;
- the expectation's clauses at their edges, and a group without value;
- the record's fractions written as fractions, and private keys left out;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import hashlib
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from reasoned_loop import protocol as LP
from reasoned_loop import references as rl_refs
from reasoned_rule import plan as rr_plan
from reasoned_rule import prompts as RP
from whole import paragraph as G
from whole import plan, protocol, references

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def sha16(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


class TestClassing(unittest.TestCase):

    def setUp(self):
        _, self.cases, _, _, _ = references._world()
        self.idx = 0
        self.gov = rl_refs.governing(self.cases[self.idx])

    def test_the_governing_rule_whole(self):
        self.assertEqual(G.classed(self.idx, rl_refs.payload_of(self.gov)), "whole")

    def test_a_wrong_queue_and_no_rule(self):
        other = next(q for q in ("T1_GENERAL", "T2_TECHNICAL") if q != self.gov.queue)
        wrong = {**rl_refs.payload_of(self.gov), "action": other}
        self.assertEqual(G.classed(self.idx, wrong), "wrong_queue")
        self.assertEqual(G.classed(self.idx, {"action": self.gov.queue, "conditions": []}),
                         "no_rule")
        self.assertEqual(G.classed(self.idx, None), "no_rule")


class TestShares(unittest.TestCase):

    def test_a_share_over_right_queue_answers(self):
        got = G.share(["whole", "cut_by_one", "wrong_queue", "whole", "no_rule", "other"])
        self.assertEqual((got["answers"], got["right_queue"], got["whole"], got["share"]),
                         (6, 4, 2, Fraction(1, 2)))
        self.assertEqual(got["by_class"]["whole"], 2)
        self.assertIsNone(G.share(["wrong_queue", "no_rule"])["share"])

    def test_the_ticket_weighted_share(self):
        got = G.ticket_weighted({1: ["whole", "whole"], 2: ["cut_by_one"], 3: ["no_rule"]})
        self.assertEqual(got, Fraction(1, 2))
        self.assertIsNone(G.ticket_weighted({3: ["no_rule"]}))


def header(paragraph="blind_base", model=None, settings=None):
    texts = {"system_prompt": sha16(RP.system_prompt(G.RULE_ARM)),
             paragraph: sha16(LP.BLIND_BASE if paragraph == "blind_base" else protocol.WHOLE_BASE)}
    return {"texts_sha16": texts, "model": model or rr_plan.MODEL,
            "settings": settings or rr_plan.settings(G.RULE_ARM)}


class TestTheGates(unittest.TestCase):

    def setUp(self):
        self.rows = [{"arm": "w", "ticket": 0}]
        self.loops = {g: [("x_r1", header("whole_base" if g == "whole_v1d" else "blind_base"))]
                      for g in G.LOOPS}
        self.shared = {g: {0} for g in G.LOOPS}

    def passes(self, rows=None, loops=None, shared=None, ok=True):
        return [g["passes"] for g in G.gates(rows if rows is not None else self.rows,
                                             loops or self.loops, shared or self.shared, ok)]

    def test_every_gate_passing(self):
        self.assertEqual(self.passes(), [True] * 5)

    def test_each_gate_failing(self):
        bad_sys = {**self.loops, "channel": [("x", {**header(), "texts_sha16": {
            "system_prompt": "0" * 16, "blind_base": sha16(LP.BLIND_BASE)}})]}
        self.assertFalse(self.passes(loops=bad_sys)[0])
        self.assertFalse(self.passes(loops={**self.loops, "placement": [
            ("x", header(settings={"reasoning": {"effort": "low"}, "max_tokens": 1}))]})[1])
        self.assertFalse(self.passes(loops={**self.loops, "whole_v1d": [("x", header())]})[2])
        self.assertFalse(self.passes(shared={g: set() for g in G.LOOPS})[2])
        self.assertFalse(self.passes(rows=[{"arm": "t", "ticket": 0}])[3])
        self.assertFalse(self.passes(rows=[])[3])
        self.assertFalse(self.passes(ok=False)[4])


def groups(**gaps):
    base = {g: Fraction(1, 5) for g in G.LOOPS}
    base["whole_v1d"] = Fraction(1, 10)
    base.update(gaps)
    return {g: {"gap": v} for g, v in base.items()}


class TestTheExpectation(unittest.TestCase):

    def holds(self, **gaps):
        return [c["holds"] for c in G.expectation(groups(**gaps))]

    def test_every_clause_holding(self):
        self.assertEqual(self.holds(), [True] * 4)

    def test_the_edges(self):
        tenth = Fraction(1, 10)
        self.assertTrue(self.holds(channel=tenth)[0])
        self.assertFalse(self.holds(channel=tenth - Fraction(1, 100))[0])
        self.assertFalse(self.holds(whole_v1c=Fraction(0))[1])
        self.assertFalse(self.holds(placement=Fraction(3, 10))[2])
        self.assertTrue(self.holds(placement=Fraction(29, 100))[2])
        self.assertFalse(self.holds(whole_v1d=Fraction(0))[3])
        self.assertFalse(self.holds(whole_v1d=Fraction(1, 5))[3])

    def test_a_group_without_value_holds_nothing_it_enters(self):
        got = self.holds(reasoned_loop=None, whole_v1d=None)
        self.assertEqual((got[0], got[2], got[3]), (False, False, False))
        self.assertTrue(got[1])


class TestTheRecord(unittest.TestCase):

    def test_fractions_and_private_keys(self):
        got = G.jsonable({"a": Fraction(1, 3), "_shared": {1}, "b": [Fraction(1, 2), None]})
        self.assertEqual(got, {"a": {"fraction": "1/3", "value": 1 / 3},
                               "b": [{"fraction": "1/2", "value": 0.5}, None]})

    def test_the_record_keeps_its_env(self):
        got = G.record_of({"passes": True}, [], {"rule_arm": {}, "groups": {}, "providers": {},
                                                "_shared": {}, "_stage_c_ok": True}, [])
        self.assertEqual(next(iter(got)), "_env")
        self.assertIn("git_commit", got["_env"])
        self.assertNotIn("_shared", got)

    def test_the_lines(self):
        self.assertEqual((G.RULE_ARM, G.GAP, G.BAIDU, G.DEEPINFRA),
                         ("w", Fraction(1, 10), ("reasoned_loop", "channel"),
                          ("placement", "whole_v1c")))
        self.assertTrue(G.EMPTY_BASE.startswith("BASE DE REGLAS: vacia."))
        self.assertEqual(G.PARAGRAPH["whole_v1d"], "whole_base")

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", G.PROVENANCE)
        self.assertIn("before the reading ran", G.PROVENANCE)
        self.assertEqual(G.record_path(), plan.OUT / "paragraph.json")


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
