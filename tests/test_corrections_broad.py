"""
`corrections/broad.py` — the POST-RUN reading of why the first call writes broad
corrections, no figure.

What is pinned is the instrument, on records built by hand:
- a draft's region, and the payloads that build none;
- the two codes, each matched and each refused where a longer word, a far
  ticket or a full stop would fool it;
- the first calls of a record, with their breadth and codes;
- the pairs of first calls on the same ticket, overall and on the same queue;
- the corrections born at a report against the base: duplicates, the right
  ones among them, and the one written most often;
- the nested rules of another queue left out of the round, and gate 3 failing
  on one listed;
- the four gates on six runs built by hand, and gate 4 on `DEVELOPMENT`;
- the expectation's clauses at their edges, and a clause over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import broad as B
from corrections import plan
from rung2.engine2 import Space

SPACE = Space()
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
BI, SS, AM = "BILLING_SPECIALIST", "SELF_SERVICE_DEFLECT", "ACCOUNT_MANAGER"


def cond(attr, value, op="eq"):
    return {"attr": attr, "op": op, "value": value}


def call(conditions, action=BI, reasoning="", **extra):
    return {"payload": {"action": action, "conditions": conditions, "beats": [],
                        "loses_to": [], "note": ""}, "reasoning": reasoning, **extra}


def esc(idx, kind, verdict, calls, rule_id=None, copy_of=None, listed=()):
    return {"idx": idx, "kind": kind, "verdict": verdict, "calls": calls,
            "rule_id": rule_id, "copy_of": copy_of, "listed": list(listed)}


class TestARegion(unittest.TestCase):

    def test_a_valid_draft_and_its_points(self):
        one = B.region({"conditions": [cond("product", "billing")]}, SPACE)
        two = B.region({"conditions": [cond("product", "billing"), cond("severity", 4)]}, SPACE)
        self.assertGreater(one.bit_count(), two.bit_count())
        self.assertEqual(one & two, two)

    def test_payloads_that_build_no_region(self):
        for payload in (None, {}, {"conditions": []}, {"conditions": "x"},
                        {"conditions": [{"attr": "product"}]}, "text"):
            with self.subTest(payload=payload):
                self.assertIsNone(B.region(payload, SPACE))


class TestTheCodes(unittest.TestCase):

    def test_defer(self):
        for text in ("si se solapa, se te listaran despues", "they will be listed after",
                     "luego nos mostrarán las reglas", "then the system will tell us",
                     "after seeing the conflicts we adjust"):
            with self.subTest(text=text):
                self.assertTrue(B.codes(text)["DEFER"])
        for text in ("the list of actions", "we show the rule", ""):
            with self.subTest(text=text):
                self.assertFalse(B.codes(text)["DEFER"])

    def test_any(self):
        for text in ("any billing ticket goes there", "Todos los tickets de billing",
                     "cualquier caso analogo", "every ticket with product billing"):
            with self.subTest(text=text):
                self.assertTrue(B.codes(text)["ANY"])
        for text in ("anyway, this ticket is billing", "many tickets look alike",
                     "any rule. The ticket is billing",
                     "all the conditions we could possibly want to add here for the ticket"):
            with self.subTest(text=text):
                self.assertFalse(B.codes(text)["ANY"])

    def test_none_is_no_code(self):
        self.assertEqual(B.codes(None), {"DEFER": False, "ANY": False})


def l_record():
    """An L run: two reported errors, an impasse, a conflict."""
    return {
        "draws_sha16": "d1",
        "rules": [
            {"rule_id": "R1", "action": BI, "born_at": 0,
             "conditions": [cond("product", "billing")]},
            {"rule_id": "R2", "action": SS, "born_at": 1,
             "conditions": [cond("product", "billing"), cond("severity", 4)]},
            {"rule_id": "R3", "action": BI, "born_at": 2,
             "conditions": [cond("product", "billing")]},
            {"rule_id": "R4", "action": AM, "born_at": 3,
             "conditions": [cond("product", "api"), cond("severity", 3),
                            cond("customer_tier", "enterprise")]},
        ],
        "escalations": [
            esc(0, "IMPASSE", "nacida", [call([cond("product", "billing")])], "R1"),
            esc(1, "CONFLICT", "nacida", [call([cond("product", "billing"), cond("severity", 4)],
                                               SS)], "R2"),
            esc(2, "ERROR", "nacida",
                [call([cond("product", "billing")], BI,
                      "Any billing ticket goes to billing; overlaps will be listed after.",
                      left_out={"R2": "inside"})], "R3", copy_of="R1"),
            esc(3, "ERROR", "nacida",
                [call([cond("product", "api"), cond("severity", 3),
                       cond("customer_tier", "enterprise")], AM, "This exact ticket.")], "R4"),
            esc(4, "ERROR", "sin_situar", [{"payload": {}, "reasoning": ""}]),
        ],
    }


def n_record():
    return {
        "draws_sha16": "d1",
        "rules": [],
        "escalations": [
            esc(2, "ERROR", "nacida", [call([cond("product", "billing"), cond("severity", 2)],
                                            SS, "It will be listed later.")], "S1"),
            esc(3, "ERROR", "nacida", [call([cond("product", "api")], AM)], "S2"),
            esc(5, "ERROR", "nacida", [call([cond("channel", "chat")], AM)], "S3"),
        ],
    }


def forgotten_run():
    """`forgotten.read_run`'s reading of `l_record`: the report at 2 left wrong,
    R2 nested inside it; the report at 3 right."""
    return {"gates": [{"gate": g, "passes": True} for g in range(1, 6)],
            "points": [
                {"at_born_reports": [{"report": 2, "rule_id": "R3", "right": False,
                                      "why": "nested", "nested": ["R2"]}]},
                {"at_born_reports": [{"report": 3, "rule_id": "R4", "right": True,
                                      "why": None}]},
            ]}


class TestAFirstCall(unittest.TestCase):

    def test_first_calls(self):
        got = B.first_calls(l_record(), SPACE)
        self.assertEqual(sorted(got), [0, 1, 2, 3, 4])
        self.assertEqual((got[2]["cause"], got[2]["conditions"], got[2]["valid"]),
                         ("ERROR", 1, True))
        self.assertEqual(got[2]["codes"], {"DEFER": True, "ANY": True})
        self.assertFalse(got[4]["valid"])
        self.assertIsNone(got[4]["points"])

    def test_code_counts_by_breadth(self):
        got = B.code_counts(B.first_calls(l_record(), SPACE), "ERROR")
        self.assertEqual(got, {"broad": {"drafts": 1, "DEFER": 1, "ANY": 1},
                               "narrow": {"drafts": 1, "DEFER": 0, "ANY": 0}})

    def test_breadth(self):
        self.assertEqual([B.breadth(n) for n in (1, 2, 3, 6)],
                         ["broad", "broad", "narrow", "narrow"])


class TestThePairs(unittest.TestCase):

    def test_pairs_on_the_same_ticket(self):
        got = B.pairs(B.first_calls(l_record(), SPACE), B.first_calls(n_record(), SPACE))
        # Cases 2 and 3 were reported in both; 4 is L's alone and invalid, 5 N's alone.
        self.assertEqual(got["reported_in_both"], 2)
        self.assertEqual(got["valid_pairs"], 2)
        # At 2, L's one condition is broader than N's two; at 3, N's one is broader.
        self.assertEqual((got["l_broader"], got["n_broader"], got["equal"]), (1, 1, 0))
        self.assertEqual(got["same_queue"], {"pairs": 1, "l_broader": 0, "n_broader": 1,
                                             "equal": 0})


class TestTheCorrections(unittest.TestCase):

    def test_duplicates_and_the_most_written(self):
        got = B.corrections(l_record(), forgotten_run())
        self.assertEqual((got["born"], got["left_wrong"], got["left_wrong_duplicates"]),
                         (2, 1, 1))
        self.assertEqual((got["duplicates"], got["duplicates_right"]), (1, 0))
        self.assertEqual(got["most_written"]["born_at_reports"], 1)

    def test_a_copy_of_another_queue_is_no_duplicate(self):
        rec = l_record()
        next(e for e in rec["escalations"] if e["idx"] == 2)["copy_of"] = "R2"
        got = B.corrections(rec, forgotten_run())
        self.assertEqual(got["duplicates"], 0)

    def test_the_signature_ignores_order(self):
        a = {"action": BI, "conditions": [cond("product", "billing"), cond("severity", 4)]}
        b = {"action": BI, "conditions": [cond("severity", 4), cond("product", "billing")]}
        self.assertEqual(B.signature(a), B.signature(b))

    def test_the_nested_rules_left_out(self):
        self.assertEqual(B.nested_left_out(l_record(), forgotten_run()),
                         {"left_out:inside": 1})
        rec = l_record()
        next(e for e in rec["escalations"] if e["idx"] == 2)["listed"] = ["R2"]
        self.assertEqual(B.nested_left_out(rec, forgotten_run()), {"listed": 1})


def six_runs():
    records, fr = {}, {}
    for k in (1, 2, 3):
        records[f"l_r{k}"], records[f"n_r{k}"] = l_record(), n_record()
        fr[f"l_r{k}"] = forgotten_run()
    return records, fr


class TestTheGates(unittest.TestCase):

    def gates(self, records, fr, development=None):
        with mock.patch.object(B, "DEVELOPMENT", development or B.DEVELOPMENT):
            got = B.read_all_runs(records, {}, [], SPACE, forgotten_runs=fr)
        return {g["gate"]: g["passes"] for g in got["gates"]}

    def test_they_pass_on_runs_built_by_hand(self):
        records, fr = six_runs()
        dev = B.code_counts(B.first_calls(l_record(), SPACE), "ERROR")
        dev_n = B.code_counts(B.first_calls(n_record(), SPACE), "ERROR")
        self.assertEqual(self.gates(records, fr, {"l": dev, "n": dev_n}),
                         {1: True, 2: True, 3: True, 4: True})

    def test_gate_4_reads_the_frozen_counts(self):
        records, fr = six_runs()
        self.assertFalse(self.gates(records, fr)[4])

    def test_gate_1_on_a_failing_forgotten_gate(self):
        records, fr = six_runs()
        fr["l_r2"] = {**fr["l_r2"], "gates": [{"gate": 1, "passes": False}]}
        self.assertFalse(self.gates(records, fr)[1])

    def test_gate_2_on_other_draws(self):
        records, fr = six_runs()
        records["n_r3"] = {**records["n_r3"], "draws_sha16": "d2"}
        self.assertFalse(self.gates(records, fr)[2])

    def test_gate_3_on_a_listed_nested_rule(self):
        records, fr = six_runs()
        next(e for e in records["l_r2"]["escalations"] if e["idx"] == 2)["listed"] = ["R2"]
        self.assertFalse(self.gates(records, fr)[3])


def run(**over):
    base = {"pairs": {"l_broader": 4, "n_broader": 6},
            "corrections": {"left_wrong": 10, "left_wrong_duplicates": 4, "duplicates": 5,
                            "duplicates_right": 1,
                            "most_written": {"conditions": 1, "born_at_reports": 5}},
            "codes": {"l": {"broad": {"drafts": 20, "DEFER": 15, "ANY": 11},
                            "narrow": {"drafts": 20, "DEFER": 15, "ANY": 8}}}}
    for k, v in over.items():
        base[k] = {**base[k], **v}
    return base


class TestTheExpectation(unittest.TestCase):

    def clauses(self, r2, r3):
        return {c["clause"]: c["holds"]
                for c in B.read_expectation({"r1": run(), "r2": r2, "r3": r3})}

    def test_at_the_edges(self):
        # 8 of 20 differing pairs broader in L; 8 of 20 left wrong duplicates;
        # 2 of 10 duplicates right; 60 of 80 DEFER; ANY 22/40 against 16/40, a
        # gap of 3/20; five births of one condition.
        self.assertEqual(self.clauses(run(), run()),
                         {"B1": True, "B2": True, "B3": True, "B4": True, "B5": True,
                          "B6": True})

    def test_just_past_each_edge(self):
        past = run(pairs={"l_broader": 8, "n_broader": 2},
                   corrections={"left_wrong": 10, "left_wrong_duplicates": 3,
                                "duplicates": 5, "duplicates_right": 2,
                                "most_written": {"conditions": 3, "born_at_reports": 9}},
                   codes={"l": {"broad": {"drafts": 20, "DEFER": 14, "ANY": 10},
                                "narrow": {"drafts": 20, "DEFER": 15, "ANY": 8}}})
        self.assertEqual(self.clauses(run(), past),
                         {"B1": False, "B2": False, "B3": False, "B4": False, "B5": False,
                          "B6": False})

    def test_b6_reads_each_run(self):
        few = run(corrections={**run()["corrections"],
                               "most_written": {"conditions": 2, "born_at_reports": 4}})
        self.assertFalse(self.clauses(run(), few)["B6"])

    def test_the_development_run_is_not_read(self):
        got = B.read_expectation({"r1": run(pairs={"l_broader": 99, "n_broader": 0}),
                                  "r2": run(), "r3": run()})
        self.assertTrue(next(c for c in got if c["clause"] == "B1")["holds"])

    def test_a_share_over_nothing_fails(self):
        none = run(pairs={"l_broader": 0, "n_broader": 0},
                   corrections={"left_wrong": 0, "left_wrong_duplicates": 0, "duplicates": 0,
                                "duplicates_right": 0, "most_written": None},
                   codes={"l": {"broad": {"drafts": 0, "DEFER": 0, "ANY": 0},
                                "narrow": {"drafts": 0, "DEFER": 0, "ANY": 0}}})
        self.assertEqual(set(self.clauses(none, none).values()), {False})

    def test_the_lines(self):
        self.assertEqual((B.B1_SHARE, B.B2_SHARE, B.B3_SHARE, B.B4_SHARE, B.B5_GAP, B.B6_TIMES),
                         (Fraction(1, 2), Fraction(2, 5), Fraction(1, 5), Fraction(3, 4),
                          Fraction(3, 20), 5))
        self.assertEqual((B.DEVELOPMENT_REP, B.HELD_OUT, B.BROAD_MOST), (1, (2, 3), 2))


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(B, "read_all") as reads, \
                mock.patch.object(B, "record_path") as path:
            with self.assertRaises(SystemExit):
                B.main([])
            reads.assert_not_called()
            path.return_value.write_text.assert_not_called()

    def test_the_record_lands_in_the_plan_s_directory(self):
        self.assertEqual(B.record_path(), plan.OUT / "broad.json")


if __name__ == "__main__":
    unittest.main()
