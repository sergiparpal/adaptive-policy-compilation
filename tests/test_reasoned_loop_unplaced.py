"""
`reasoned_loop/unplaced.py` — the POST-RUN reading of where the unplaced answers
come from, no figure.

What is pinned is the instrument: the codebook's fingerprint written a second
time, how a reasoning splits into sentences, a rule's text with the sentence
after it, what each code matches in each of the three languages and the anchors
that keep a pattern inside its word, a negation or a question taking a sentence
out of `nested`, the relation to the draft on masks, each cause, a placement
round read from a record built by hand, the three gates on it with their teeth,
the readings on rows built by hand, the expectation's clauses at their edges,
and that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from authorship import protocol as e
from blind import rows as brows
from reasoned_loop import plan, unplaced as U
from rung2.engine2 import Space

SPACE = Space()
UNSIGNED = {"passes": False, "found": 3, "unsigned": 1}
T1, T2, SI = "T1_GENERAL", "T2_TECHNICAL", "SECURITY_INCIDENT"


class TestTheCodebook(unittest.TestCase):

    def test_the_fingerprint_written_a_second_time(self):
        self.assertEqual(U.CODEBOOK_DIGEST, "ccd5d3d68e09c8dc")
        self.assertEqual(U.digest(), U.CODEBOOK_DIGEST)
        self.assertEqual((U.FOLLOW, U.NEAR), (1, 25))

    def test_sentences(self):
        text = "R0001 contiene mi regla. Severity 0.5 stays\nR0002: 无重叠。下一句 Is R0003 a subset? Yes; done"
        self.assertEqual(U.sentences(text), ["R0001 contiene mi regla.", "Severity 0.5 stays",
                                             "R0002: 无重叠。", "下一句 Is R0003 a subset?",
                                             "Yes;", "done"])

    def test_a_rule_s_text_takes_one_sentence_after_it_naming_no_rule(self):
        sents = ["R0001: product eq api.", "So it is contained.", "And more.",
                 "R0002: billing.", "R0001 again.", "R0003 follows."]
        self.assertEqual(U.text_of("R0001", sents),
                         ["R0001: product eq api.", "So it is contained.", "R0001 again."])
        self.assertEqual(U.text_of("R0004", sents), [])
        self.assertEqual(U.text_of("R000", ["R0001 only."]), [])

    def test_what_each_code_matches(self):
        cases = {
            "R0006 es un subconjunto estricto y gana por nivel 1.": {"nested"},
            "No incluimos R0025 porque está contenida.": {"nested"},
            "Mi regla no está contenida en R0030.": {"not_nested"},
            "互不包含": {"not_nested"},
            "So our rule is contained in R0011.": {"nested"},
            "So our rule is not a subset of R0020.": {"not_nested"},
            "Is R0020 subset?": set(),
            "我们的规则是R0021的特例": {"nested"},
            "R0042: 无重叠": {"apart"},
            "R0007: product eq billing (no aplica)": {"apart"},
            "They do not overlap, mutually exclusive.": {"apart"},
            "R0004 no se solapa con la mía": {"apart"},
            "Las reglas son disjuntas.": {"apart"},
            "Un caso particular de R0021.": {"nested"},
        }
        for sentence, want in cases.items():
            with self.subTest(sentence=sentence):
                self.assertEqual(U.codes_of(sentence), want)

    def test_the_anchors_keep_a_pattern_inside_its_word(self):
        for sentence in ("Es no aplicable aquí.", "Noaplica.", "subsets are many",
                         "the containers", "nivel 10 de la lista"):
            with self.subTest(sentence=sentence):
                self.assertEqual(U.codes_of(sentence), set())

    def test_a_text_s_codes(self):
        self.assertEqual(U.code(["R0001 está contenida.", "R0001 no se solapa."]),
                         frozenset({"nested", "apart"}))
        self.assertEqual(U.code(["Not a subset of R0002, though R0003 is a subset."]),
                         frozenset({"nested", "not_nested"}))
        self.assertEqual(U.code([]), frozenset())


class TestTheRelation(unittest.TestCase):

    def test_relation_and_cause(self):
        self.assertEqual(U.relation(0b0110, 0b0110), "equal")
        self.assertEqual(U.relation(0b0010, 0b0110), "inside_draft")
        self.assertEqual(U.relation(0b1110, 0b0110), "contains_draft")
        self.assertEqual(U.relation(0b1100, 0b0110), "crossing")
        n, c = frozenset({"nested"}), frozenset({"apart", "nested"})
        self.assertEqual(U.cause("contains_draft", n, True), "nested_said_nested")
        self.assertEqual(U.cause("equal", frozenset(), True), "nested_not_said")
        self.assertEqual(U.cause("crossing", c, True), "crossing_said_apart")
        self.assertEqual(U.cause("crossing", n, True), "crossing_said_nested")
        self.assertEqual(U.cause("crossing", frozenset({"not_nested"}), True), "crossing_no_claim")
        self.assertEqual(U.cause("crossing", frozenset(), False), "crossing_unmentioned")


def rule(rid, action, **conds):
    return {"rule_id": rid, "action": action, "born_at": 0,
            "conditions": [{"attr": a, "op": "eq" if not isinstance(v, int) else "gte",
                            "value": v} for a, v in conds.items()]}


DRAFT = {"action": T2, "conditions": [{"attr": "product", "op": "eq", "value": "api"}]}
REASONING = ("R0001 contiene mi regla: caso particular, el nivel 1 lo resuelve.\n"
             "R0002: no se solapa con la mía.\n"
             "R0003 pierde.")


def record(cited=("R0003",), reasoning=REASONING, verdict=e.UNPLACED, unplaced=("R0001", "R0002"),
           finish="stop", answer=DRAFT):
    rules = [rule("R0001", T1, severity=1),                      # the whole space
             rule("R0002", SI, customer_tier="free"),            # crosses the draft
             rule("R0003", SI, channel="email")]                 # crosses the draft
    calls = [{"round": 0, "payload": dict(DRAFT)},
             {"round": 1, "payload": {**answer, "beats": list(cited), "loses_to": []},
              "unplaced": list(unplaced), "reasoning": reasoning,
              "call_attempts": [{"provider": "Baidu", "finish_reason": finish}]}]
    return {"arm": "e", "rep": 2, "rules": rules,
            "escalations": [{"idx": 7, "kind": "ERROR", "verdict": verdict,
                             "listed": ["R0002", "R0001", "R0003"], "calls": calls}]}


class TestARoundRead(unittest.TestCase):

    def test_the_rows_of_a_round(self):
        rows, escalations = U.rows_of(record(), SPACE)
        self.assertEqual(escalations, [{"run": "e_r2", "idx": 7, "cause": "ERROR",
                                        "verdict": e.UNPLACED, "listed": 3, "missing": 2}])
        by = {r["rule"]: r for r in rows}
        self.assertEqual((by["R0001"]["relation"], by["R0001"]["whole_space"]),
                         ("contains_draft", True))
        self.assertEqual(by["R0001"]["cause"], "nested_said_nested")
        self.assertEqual((by["R0002"]["relation"], by["R0002"]["cause"]),
                         ("crossing", "crossing_said_apart"))
        self.assertFalse(by["R0003"]["missing"])
        self.assertEqual(by["R0003"]["cause"], "crossing_no_claim")
        self.assertEqual(by["R0002"]["mentions"], 1)

    def test_an_answer_that_changed_the_rule_is_counted_apart(self):
        rows, escalations = U.rows_of(record(verdict=e.REJECTED), SPACE)
        self.assertEqual(rows, [])
        self.assertEqual(escalations[0]["verdict"], e.REJECTED)

    def test_the_gates_and_their_teeth(self):
        published = {"RL-h": {"runs": {"e_r2": {"placements": {"verdicts": {e.UNPLACED: 1}}}}}}
        self.assertTrue(U.census_gate(record(), published))
        self.assertFalse(U.census_gate(record(cited=("R0003", "R0001")), published))
        self.assertFalse(U.census_gate(record(unplaced=()), published))
        self.assertFalse(U.census_gate(record(unplaced=("R0009",)), published))
        self.assertFalse(U.census_gate(record(verdict=e.BORN), published))
        self.assertTrue(U.draft_gate(record(), SPACE))
        other = {"action": T2, "conditions": [{"attr": "product", "op": "eq", "value": "mobile"}]}
        self.assertFalse(U.draft_gate(record(answer=other), SPACE))
        self.assertTrue(U.reasoning_gate(record()))
        self.assertFalse(U.reasoning_gate(record(reasoning="")))
        self.assertFalse(U.reasoning_gate(record(finish="length")))


def row(rep, missing, relation, codes=(), mentions=1, whole=False, run=None, idx=1,
        verdict=e.UNPLACED, arm="e"):
    codes = frozenset(codes)
    return {"run": run or f"{arm}_r{rep}", "arm": arm, "rep": rep, "idx": idx, "rule": "R",
            "verdict": verdict, "missing": missing, "listed": 3, "relation": relation,
            "whole_space": whole, "mentions": mentions, "codes": sorted(codes),
            "cause": U.cause(relation, codes, bool(mentions)), "coded_sentences": ["s"]}


class TestTheReadings(unittest.TestCase):

    def setUp(self):
        self.rows = [row(2, True, "contains_draft", {"nested"}, whole=True, idx=1),
                     row(2, False, "inside_draft", {"nested"}, idx=2, verdict=e.BORN),
                     row(2, True, "crossing", {"apart"}, idx=1),
                     row(2, False, "crossing", (), idx=2, verdict=e.BORN),
                     row(2, False, "crossing", {"apart"}, idx=2, verdict=e.BORN),
                     row(3, True, "crossing", (), mentions=0, idx=3),
                     row(1, True, "equal", (), idx=9)]

    def test_omission_causes_and_codes(self):
        r = U.reading(self.rows)
        self.assertEqual((r["listed_rules"], r["missing_rules"], r["unplaced_escalations"]),
                         (7, 4, 3))
        self.assertEqual(r["omission"]["nested"]["rate_exact"], Fraction(2, 3))
        self.assertEqual(r["omission"]["crossing"]["rate_exact"], Fraction(2, 4))
        self.assertEqual(r["omission"]["equal"]["listed"], 1)
        self.assertEqual(r["causes"]["nested_said_nested"], 1)
        self.assertEqual(r["causes"]["nested_not_said"], 1)
        self.assertEqual(r["causes"]["crossing_unmentioned"], 1)
        self.assertEqual(r["codes"]["missing_crossing"]["apart"]["share_exact"], Fraction(1, 2))
        self.assertEqual(r["codes"]["placed_crossing"]["apart"]["share_exact"], Fraction(1, 2))
        self.assertEqual(r["codes"]["missing_crossing"]["unmentioned"]["count"], 1)
        self.assertEqual(r["escalations"], {"unplaced": 3, "every_missing_rule_stated": 1,
                                            "every_missing_rule_nested": 1})

    def test_the_sets_split_by_repetition(self):
        got = U.readings(self.rows)
        self.assertEqual(got["development"]["pooled"]["listed_rules"], 1)
        self.assertEqual(got["held_out"]["pooled"]["listed_rules"], 6)
        self.assertEqual(got["all"]["e"]["listed_rules"], 7)
        self.assertEqual(got["all"]["i"]["listed_rules"], 0)

    def test_the_whole_space_by_run(self):
        self.assertEqual(U.whole_space(self.rows)["e_r2"],
                         {"unplaced": 1, "left_out_the_whole_space": 1,
                          "listed_the_whole_space": 1})

    def test_the_quotes_read_held_out_rules_only(self):
        q = U.quotes(self.rows)
        self.assertEqual([x["run"] for x in q["nested_said_nested"]], ["e_r2"])
        self.assertEqual(q["nested_not_said"], [])


class TestTheExpectation(unittest.TestCase):

    def held_out(self, rn, rc, said, of_n, stated, of_c, apart_m, apart_p):
        def cell(n, a=None):
            return {"rules": n, "apart": {"share_exact": a}}
        return {"omission": {"nested": {"rate_exact": rn}, "crossing": {"rate_exact": rc}},
                "codes": {"missing_nested": cell(of_n), "missing_crossing": cell(of_c, apart_m),
                          "placed_crossing": cell(10, apart_p)},
                "causes": {"nested_said_nested": said, "crossing_said_apart": stated,
                           "crossing_said_nested": 0}}

    def test_clause_by_clause_at_their_edges(self):
        F = Fraction
        x = U.read_expectation(self.held_out(F(4, 10), F(1, 10), 3, 4, 2, 4, F(2, 5), F(1, 10)),
                               {"e_r3": {"unplaced": 4, "left_out_the_whole_space": 2}})
        self.assertEqual([c["holds"] for c in x], [True] * 5)
        x = U.read_expectation(self.held_out(F(39, 100), F(1, 10), 2, 4, 1, 4, F(39, 100),
                                             F(1, 10)),
                               {"e_r3": {"unplaced": 4, "left_out_the_whole_space": 1}})
        self.assertEqual([c["holds"] for c in x], [False] * 5)

    def test_a_reading_without_value_does_not_hold(self):
        x = U.read_expectation(self.held_out(None, None, 0, 0, 0, 0, None, None), {})
        self.assertEqual([c["holds"] for c in x], [False] * 5)


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
                    U.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
