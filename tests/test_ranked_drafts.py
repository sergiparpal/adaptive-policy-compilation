"""
`ranked/drafts.py` — the POST-RUN reading of why one prompt drew different
drafts. No figure of the reading.

What is pinned is the instrument:
- where two reasonings part, and the median of a count;
- a first call's prompt: the ticket and the report, nothing else;
- a pair's class: the same draft, the same queue, two queues, or invalid, with
  drafts read over the real space;
- where a set of pairs part: the counts within each bound, the same text, one
  reasoning inside the other;
- how many drafts a prompt's calls drew;
- two drafts of one queue: an attribute in one draft only, and one in both with
  other conditions;
- the exception's pairs: only tickets of `H03` told `T2_TECHNICAL`, with a
  window from where the reasonings part;
- the gates with teeth, on K r3's record: they pass on it, and a figure moved
  fails them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

from manual import instrument as MI
from ranked import drafts as DR
from ranked import plan

T2, SEC, SS = DR.T2, "SECURITY_INCIDENT", "SELF_SERVICE_DEFLECT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
KW = {"attr": "has_security_keyword", "op": "eq", "value": True}
SEV3 = {"attr": "severity", "op": "gte", "value": 3}
SEV_NOT1 = {"attr": "severity", "op": "neq", "value": 1}
FREE = {"attr": "customer_tier", "op": "eq", "value": "free"}


class TestSmallParts(unittest.TestCase):

    def test_where_two_reasonings_part(self):
        self.assertEqual(DR.parted_at("We need to decide", "We need to determine"), 13)
        self.assertEqual(DR.parted_at("same", "same"), 4)
        self.assertEqual(DR.parted_at("abc", "abcdef"), 3)
        self.assertEqual(DR.parted_at("", "abc"), 0)

    def test_the_median(self):
        self.assertEqual(DR.median_of([5, 1, 3]), 3)
        self.assertEqual(DR.median_of([4, 1, 3, 2]), DR.F(5, 2))
        self.assertIsNone(DR.median_of([]))

    def test_a_prompt_is_the_ticket_and_the_report(self):
        a = {"key": [True, 3, "free"], "report": T2}
        self.assertEqual(DR.prompt_of(a), DR.prompt_of(dict(a)))
        self.assertNotEqual(DR.prompt_of(a), DR.prompt_of(dict(a, report=None)))
        self.assertNotEqual(DR.prompt_of(a), DR.prompt_of(dict(a, key=[True, 4, "free"])))


def call(run="k_r1", case=1, action=T2, conditions=(KW, SEV3), reasoning="We need to decide",
         report=T2, governing="H03", kind="ERROR", key=(1,), space=None):
    payload = {"action": action, "conditions": list(conditions)} if action else None
    ext = DR.RD.region(payload, space) if payload else None
    return {"run": run, "case": case, "kind": kind, "verdict": "nacida", "rule_id": None,
            "report": report, "key": list(key), "truth": T2, "governing": governing,
            "action": action, "extension": ext,
            "conditions": DR.RD.conditions_of(payload["conditions"]) if ext is not None else None,
            "attributes": DR.RD.attrs(payload["conditions"]) if ext is not None else None,
            "reasoning": reasoning}


class TestPairs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()

    def c(self, **kw):
        return call(space=self.space, **kw)

    def test_each_class(self):
        a = self.c()
        self.assertEqual(DR.pair_class(a, self.c(run="l_r3")), "same")
        self.assertEqual(DR.pair_class(a, self.c(conditions=(KW, SEV_NOT1))), "same_queue")
        self.assertEqual(DR.pair_class(a, self.c(action=SEC)), "other_queue")
        self.assertEqual(DR.pair_class(a, self.c(action=None)), "invalid")
        self.assertEqual(DR.pair_class(a, self.c(conditions=())), "invalid")

    def test_the_same_extension_in_other_words_is_the_same_draft(self):
        a = self.c(conditions=(KW, SEV3))
        b = self.c(conditions=(KW, {"attr": "severity", "op": "in", "value": [3, 4]}))
        self.assertEqual(DR.pair_class(a, b), "same")

    def test_where_a_set_of_pairs_part(self):
        groups = {((1,), T2): [self.c(reasoning="x" * 300),
                               self.c(run="l_r1", reasoning="x" * 300),
                               self.c(run="l_r2", reasoning="x" * 120),
                               self.c(run="l_r3", reasoning="x" * 40 + "y")]}
        pairs = DR.pairs_of(groups)
        got = DR.where_they_part(pairs)
        self.assertEqual(got["pairs"], 6)
        self.assertEqual(got["same_text"], 1)
        # the two of 300 alike, and each with the 120 that is their prefix
        self.assertEqual(got["one_inside_the_other"], 3)
        self.assertEqual(got["within"], {"50": 3, "100": 3, "200": 5, "500": 6, "1000": 6})
        self.assertEqual((got["least"], got["most"]), (40, 300))
        self.assertEqual(got["median"], DR.frac(DR.F(80)))

    def test_drafts_by_calls(self):
        groups = {("a",): [self.c(), self.c(run="l_r1"), self.c(run="l_r2", action=SEC)],
                  ("b",): [self.c()],
                  ("c",): [self.c(), self.c(run="l_r1", conditions=(KW, FREE, SEV3))]}
        self.assertEqual(DR.drafts_by_size(groups), {"2": {"2": 1}, "3": {"2": 1}})

    def test_two_drafts_of_one_queue(self):
        pairs = DR.pairs_of({((1,), T2): [self.c(),
                                          self.c(run="l_r1", conditions=(KW, FREE, SEV3))],
                             ((2,), T2): [self.c(),
                                          self.c(run="l_r1", conditions=(KW, SEV_NOT1))]})
        got = DR.read_c(pairs)
        self.assertEqual((got["pairs"], got["other_attributes"],
                          got["same_attributes_other_values"]), (2, 1, 1))
        self.assertEqual(got["attribute_in_one_draft_only"]["customer_tier"], 1)
        self.assertEqual(got["attribute_in_both_other_conditions"]["severity"], 1)
        self.assertEqual(got["attribute_in_both_other_conditions"]["customer_tier"], 0)

    def test_the_exceptions_pairs_alone(self):
        text = "We need to decide " + "a" * 900
        groups = {((1,), T2): [self.c(reasoning=text), self.c(run="l_r3", reasoning=text + "b")],
                  ((2,), T2): [self.c(governing="H01"), self.c(run="l_r3", governing="H01")],
                  ((3,), SEC): [self.c(report=SEC), self.c(run="l_r3", report=SEC)]}
        got = DR.read_d(groups)
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["parted_at"], len(text))
        self.assertEqual(got[0]["a"]["window"], text[len(text) - DR.WINDOW_BEFORE:])
        self.assertEqual(got[0]["b"]["tail"], (text + "b")[-DR.TAIL:])


class TestGatesWithTeeth(unittest.TestCase):
    """On K r3's record: the gates pass, and one figure moved fails them. Nothing
    of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        cls.space = MI.space()
        cls.corpus = list(MI.corpus())
        cls.calls = DR.first_calls(cls.record, "k_r3", cls.corpus, cls.space)

    def test_gate_one(self):
        self.assertTrue(DR.texts_are_the_protocols(self.record))
        moved = dict(self.record, system_prompt=self.record["system_prompt"] + " ")
        self.assertFalse(DR.texts_are_the_protocols(moved))
        self.assertFalse(DR.texts_are_the_protocols(dict(self.record, report_template=None)))

    def test_gate_two(self):
        self.assertTrue(DR.one_attempt(self.calls))
        moved = copy.deepcopy(self.calls)
        moved[0]["attempts"] = 2
        self.assertFalse(DR.one_attempt(moved))
        moved = copy.deepcopy(self.calls)
        moved[-1]["retries"] = ["a parse"]
        self.assertFalse(DR.one_attempt(moved))
        self.assertFalse(DR.one_attempt([]))

    def test_gate_three(self):
        self.assertTrue(DR.one_count(DR.by_prompt({"k_r3": self.calls})))
        a = self.calls[0]
        b = dict(a, prompt_tokens=list(a["prompt_tokens"]))
        self.assertTrue(DR.one_count({"x": [a, b]}))
        b["prompt_tokens"] = [b["prompt_tokens"][0] + 1]
        self.assertFalse(DR.one_count({"x": [a, b]}))
        self.assertFalse(DR.one_count({}))

    def test_gate_four(self):
        self.assertTrue(DR.reports_are_the_tickets(self.calls))
        moved = copy.deepcopy(self.calls)
        i = next(i for i, c in enumerate(moved) if c["report"])
        moved[i]["report"] = SS if moved[i]["truth"] != SS else T2
        self.assertFalse(DR.reports_are_the_tickets(moved))
        moved = copy.deepcopy(self.calls)
        j = next(i for i, c in enumerate(moved) if not c["report"])
        moved[j]["report"] = moved[j]["truth"]
        self.assertFalse(DR.reports_are_the_tickets(moved))

    def test_gate_five(self):
        self.assertTrue(DR.born_drafts_are_rules(self.record, self.calls, self.space))
        moved = copy.deepcopy(self.calls)
        i = next(i for i, c in enumerate(moved) if c["verdict"] == "nacida")
        moved[i]["extension"] ^= 1 << (moved[i]["extension"].bit_length() - 1)
        self.assertFalse(DR.born_drafts_are_rules(self.record, moved, self.space))

    def test_every_call_is_a_first_call(self):
        self.assertEqual(len(self.calls), len(self.record["escalations"]))
        self.assertTrue(all(c["round"] == 0 for c in self.calls))


def classes(same=1, same_queue=1, other_queue=0, invalid=0):
    return {"same": same, "same_queue": same_queue, "other_queue": other_queue,
            "invalid": invalid}


def fake(every=classes(same=4, same_queue=6), told=classes(same=4, same_queue=6),
         untold=classes(same=3, same_queue=3, other_queue=4), within=6, same_text=0,
         queue_pairs=4, other_attributes=3):
    return {"pairs": {"classes": {"all": every, "with_a_report": told, "without": untold},
                      "parted": {"all": {"within": {"200": within}, "same_text": same_text}}},
            "one_queue": {"pairs": queue_pairs, "other_attributes": other_attributes}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in DR.read_expectation(readings)}


CLAUSES = ["H1", "H2", "H3", "H4", "H5", "H6"]


class TestTheExpectation(unittest.TestCase):

    def test_six_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(every=classes(same=5, same_queue=5), told=classes(same=5, same_queue=4,
                                                                           other_queue=1),
                         untold=classes(same=2, same_queue=3, other_queue=5), within=5,
                         same_text=1, queue_pairs=4, other_attributes=2))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_each_edge_alone(self):
        self.assertTrue(holds(fake(told=classes(same=1, same_queue=18, invalid=1)))["H2"])
        self.assertFalse(holds(fake(told=classes(same=1, same_queue=8, invalid=1)))["H2"])
        self.assertFalse(holds(fake(same_text=2))["H4"])
        self.assertTrue(holds(fake(same_text=2))["H3"])

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        empty = classes(same=0, same_queue=0)
        self.assertEqual(holds(fake(every=empty, told=empty, untold=empty, within=0,
                                    queue_pairs=0, other_attributes=0)),
                         {c: False for c in CLAUSES})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(DR, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                DR.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
