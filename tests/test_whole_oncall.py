"""
`whole/oncall.py` — the POST-RUN reading of why v1d cut at the rarest queue's
tickets, no figure of the reading.

What is pinned is what this module adds to `placement/oncall.py`'s reading, which
`tests/test_placement_oncall.py` pins:
- the codebook's patterns, anchored, each matched and each refused where a
  longer word or another phrase would fool it;
- the quotes of T1 kept with their windows, one inside the last window not kept
  again, and at most `QUOTES` a call;
- the development counts recomputed on the smoke run, which gate 5 reads;
- each first call on a ticket of the queue read on a record built by hand: a
  cut by the first match a cut by would change, its added condition, its codes,
  its note, its placement round, and a ticket of another queue left out;
- the five gates, each failing on its own;
- the expectation's clauses at their edges, and a reading without value;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import Case
from reasoned_loop import references as rl_refs
from rung2.engine2 import Space
from whole import oncall as W
from whole import plan

OC, T2, T3 = "ONCALL_ESCALATION", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def cond_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def case_(**kw):
    values = dict(has_security_keyword=False, severity=1, customer_tier="enterprise",
                  product="api", channel="email", prior_tickets_30d=0, off_hours=False,
                  language="en")
    values.update(kw)
    return Case(**values)


class TestTheCodebook(unittest.TestCase):

    def test_t1_quoted(self):
        for text in ("con la region entera de la regla", "la REGIÓN  ENTERA",
                     "No le anadas condiciones", "no le añadas condiciones"):
            with self.subTest(text=text):
                self.assertEqual(W.count("T1", text), 1)
        for text in ("regiones enteras", "la región enteramente", "añadas condicionesx",
                     "subregión entera"):
            with self.subTest(text=text):
                self.assertEqual(W.count("T1", text), 0)

    def test_t1_said_in_english(self):
        for text in ("the whole region of H04", "its entire region", "the full region",
                     "we should not add extra conditions", "must not add any condition"):
            with self.subTest(text=text):
                self.assertEqual(W.count("T1e", text), 1)
        for text in ("a wholesale region", "should not address the conditions",
                     "should not add it. The conditions"):
            with self.subTest(text=text):
                self.assertEqual(W.count("T1e", text), 0)

    def test_inside_in_a_note(self):
        for text in ("es un caso particular de H07", "contenida en H17", "contenidos",
                     "queda dentro de H07", "un subconjunto", "la intersección de",
                     "la interseccion de"):
            with self.subTest(text=text):
                self.assertEqual(W.count("INSIDE", text), 1)
        for text in ("contenidamente", "adentro de", "particularmente", None):
            with self.subTest(text=text):
                self.assertEqual(W.count("INSIDE", text), 0)

    def test_where_each_code_is_read(self):
        self.assertEqual(W.READ_IN, {"T1": "reasoning", "T1e": "reasoning",
                                     "INSIDE": "note"})
        self.assertEqual(set(W.CODEBOOK), set(W.READ_IN))

    def test_reads_t1(self):
        self.assertTrue(W.reads_t1("... la region entera ..."))
        self.assertTrue(W.reads_t1("... the whole region ..."))
        self.assertFalse(W.reads_t1("H04 casa; nivel 1 lo ordena"))
        self.assertFalse(W.reads_t1(None))

    def test_the_quotes_and_their_windows(self):
        pad = " " + "x" * (W.WINDOW + 10) + " "
        text = "a region entera b " + "y" * 10 + " whole region" + pad + "region entera" + pad \
            + "region entera" + pad + "region entera"
        got = W.quotes(text)
        self.assertEqual(len(got), W.QUOTES)
        self.assertEqual(got[0]["at"], 2)
        self.assertEqual(got[0]["text"], text[2:2 + W.WINDOW])
        self.assertTrue(all(b["at"] >= a["at"] + W.WINDOW for a, b in zip(got, got[1:])))
        self.assertEqual(W.quotes("nada que ver"), [])

    def test_the_development_counts_on_the_smoke_run(self):
        smoke = json.loads(plan.smoke_path().read_text())
        self.assertEqual(W.development(smoke), W.DEVELOPMENT)

    def test_the_lines(self):
        self.assertEqual((W.WINDOW, W.QUOTES, W.TAIL, W.Q3_SKIPPED, W.Q5_HALF),
                         (700, 3, 1500, 4, (1, 2)))
        self.assertEqual((W.QUEUE, W.PARTS), (OC, ("H04", "H05")))
        self.assertEqual(W.DEVELOPMENT, {"calls": 14, "T1": 6, "T1e": 1, "T1_or_T1e": 6,
                                         "INSIDE": 7})


def call_(round_, conditions=None, note=None, reasoning=None, listed=None, unplaced=None,
          beats=(), loses_to=()):
    payload = None if conditions is None else {
        "action": OC, "conditions": conditions, "note": note,
        "beats": list(beats), "loses_to": list(loses_to)}
    return {"round": round_, "payload": payload, "reasoning": reasoning, "listed": listed,
            "unplaced": unplaced, "failure": None,
            "call_attempts": [{"error": None, "reasoning_tokens": 1234}]}


class TestTheFirstCalls(unittest.TestCase):

    def setUp(self):
        h04_api = [cond_("severity", "eq", 1), cond_("customer_tier", "eq", "enterprise"),
                   cond_("product", "eq", "api")]
        self.record = {
            "records": [{"idx": 0, "truth": OC, "truth_rule": "H04", "cause": "ERROR",
                         "engine_action": T3},
                        {"idx": 1, "truth": T2, "truth_rule": "H08"}],
            "escalations": [
                {"idx": 0, "verdict": "sin_situar", "rule_id": None,
                 "calls": [call_(0, h04_api, note="Caso particular de H07: gana por nivel 1.",
                                 reasoning="Leo: no le anadas condiciones. " + "z" * 2000,
                                 listed=["R0002"], unplaced=["R0002"]),
                           call_(1, h04_api, note="sitúo", unplaced=["R0002"],
                                 beats=["R0001"])]},
                {"idx": 1, "verdict": "nacida", "rule_id": "R0003",
                 "calls": [call_(0, [cond_("severity", "eq", 1)], reasoning="r")]}],
            "rules": [{"rule_id": "R0001", "action": T3}, {"rule_id": "R0002", "action": T2}]}
        self.stage_c = [{"idx": 0, "governing": "H04", "class": "cut_by_one",
                         "breadth": "within_or_across", "verdict": "sin_situar"},
                        {"idx": 1, "governing": "H08", "class": "whole",
                         "breadth": "the_region", "verdict": "nacida"}]
        self.space = Space()
        self.regions = rl_refs.regions()
        self.conds = {r.id: rl_refs.payload_of(r)["conditions"] for r in rl_refs.text_rules()}
        self.cases = (case_(), case_(customer_tier="pro"))
        self.rows = W.first_calls("v1d_r1", self.record, self.stage_c, self.space,
                                  self.regions, self.cases, self.conds)

    def test_only_the_queues_tickets_are_read(self):
        self.assertEqual([(r["run"], r["arm"], r["idx"]) for r in self.rows], [("v1d_r1", "v1d", 0)])

    def test_the_cut(self):
        r = self.rows[0]
        self.assertEqual((r["governing"], r["first_cutting_match"], r["cut_by"]),
                         ("H04", "H07", ["H07", "H15", "H16"]))
        self.assertTrue(r["cut_by_the_first_cutting_match"])
        self.assertTrue(r["first_match_is_governing"])
        self.assertEqual(r["extra_conditions"], [cond_("product", "eq", "api")])
        self.assertTrue(W.is_cut(r))

    def test_its_codes_note_and_passages(self):
        r = self.rows[0]
        self.assertEqual(r["codes"], {"T1": 1, "T1e": 0, "INSIDE": 1})
        self.assertTrue(r["reads_t1"])
        self.assertEqual(r["note_cites"], ["H07"])
        self.assertEqual(len(r["quotes_of_t1"]), 1)
        self.assertEqual(len(r["answer_composed"]), W.TAIL)
        self.assertEqual((r["reasoning_tokens"], r["has_reasoning"], r["has_payload"]),
                         (1234, True, True))

    def test_what_the_escalation_was_added_after_the_first_run(self):
        r = self.rows[0]
        self.assertEqual((r["cause"], r["base_decided"]), ("ERROR", T3))
        self.assertIn("after the first run", W.ADDED)
        self.assertEqual(W.summary(self.rows)["v1d"]["causes"], {"ERROR": 1})

    def test_its_placement_round(self):
        p = self.rows[0]["placement"]
        self.assertEqual(p["listed"], [["R0002", T2]])
        self.assertEqual((p["left_without_a_side"], p["beats"], p["note"]),
                         (["R0002"], ["R0001"], "sitúo"))
        self.assertIsNone(W.placement_of({"calls": [call_(0, [])]}, {}))

    def test_extra_conditions_read_lists_in_any_order(self):
        gov = [cond_("product", "in", ["api", "mobile"])]
        self.assertEqual(W.extra_conditions([cond_("product", "in", ["mobile", "api"])], gov), [])
        self.assertEqual(W.extra_conditions(None, gov), [])

    def test_the_gates(self):
        dev = dict(W.DEVELOPMENT)
        self.assertTrue(all(g["passes"] for g in W.gates(self.rows, dev)))
        self.assertFalse(W.gates([], dev)[0]["passes"])
        for gate, change in ((1, {"governing": "H07"}), (2, {"first_match_is_governing": False}),
                             (3, {"stage_c_verdict": "nacida"}), (3, {"class": None}),
                             (4, {"has_reasoning": False})):
            with self.subTest(gate=gate, change=change):
                rows = [{**self.rows[0], **change}]
                self.assertFalse(W.gates(rows, dev)[gate - 1]["passes"])
        self.assertFalse(W.gates(self.rows, {**dev, "T1": 5})[4]["passes"])


def row_(arm, idx, cls, cut=("H07",), first=True, reads=False, inside=False):
    return {"run": f"{arm}_r1", "arm": arm, "idx": idx, "class": cls, "cause": "ERROR",
            "cut_by": list(cut) if cls.startswith("cut_by") else [],
            "first_cutting_match": "H07", "cut_by_the_first_cutting_match": first,
            "reads_t1": reads, "codes": {"T1": int(reads), "T1e": 0, "INSIDE": int(inside)}}


class TestTheExpectation(unittest.TestCase):

    def holds(self, rows):
        return [c["holds"] for c in W.expectation(rows)]

    def test_every_clause_holding(self):
        rows = [row_("v1d", i, "cut_by_one", inside=i < 3) for i in range(6)] + \
               [row_("v1d", 10, "whole", reads=True), row_("v1d", 11, "whole", reads=True),
                row_("v1c", 0, "cut_by_one", inside=True), row_("v1c", 12, "whole")]
        self.assertEqual(self.holds(rows), [True] * 5)

    def test_every_clause_failing(self):
        rows = [row_("v1d", i, "cut_by_one", first=i > 0, reads=i < 3) for i in range(6)] + \
               [row_("v1d", 10, "whole", reads=True), row_("v1d", 11, "whole"),
                row_("v1c", 0, "cut_by_one", cut=("H17",))]
        self.assertEqual(self.holds(rows), [False] * 5)

    def test_the_edges(self):
        """Q3 at four skipped of six, Q5 at half, Q2 on one shared ticket."""
        base = [row_("v1d", i, "cut_by_one", reads=i >= 4, inside=i < 3) for i in range(6)] + \
               [row_("v1d", 10, "whole", reads=True), row_("v1c", 0, "cut_by_one")]
        got = W.expectation(base)
        self.assertEqual((got[2]["reading"], got[2]["holds"]), ({"skipped": 4, "of": 6}, True))
        self.assertEqual((got[4]["reading"], got[4]["holds"]), ({"saying_it": 3, "of": 7}, False))
        base[6 - 1]["codes"]["INSIDE"] = 1
        self.assertTrue(W.expectation(base)[4]["holds"])
        self.assertEqual(list(got[1]["reading"]), [0])

    def test_a_reading_without_value_does_not_hold(self):
        self.assertEqual(self.holds([]), [False] * 5)


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
                    W.main(argv)
                read.assert_not_called()
                write.assert_not_called()

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", W.PROVENANCE)
        self.assertIn("before the reading ran", W.PROVENANCE)
        self.assertEqual(W.record_path(), plan.OUT / "oncall.json")


if __name__ == "__main__":
    unittest.main()
