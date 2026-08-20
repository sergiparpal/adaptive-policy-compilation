"""
The parsing of what the proposer returns.

It is the only part of the LLM path that can be tested without spending money,
and it is what decides whether a long run survives. The extraction is TOLERANT
on purpose —markdown fences, preambles, epilogues— because cheap models decorate
the response, and losing a 2000-case run at case 1500 over a badly closed JSON
would be absurd. What it must NOT do is tolerate too much: if it accepts
rubbish, the rubbish enters the base as a rule.

`failed_proposals` in the metrics counts exactly the cases where this raises
`ProposalError`.
"""

from __future__ import annotations

import unittest

from harness.proposers import ProposalError, parse_payload
from rung2.proposers2 import ProposalError as ProposalError2
from rung2.proposers2 import parse_payload as parse_payload2

RULE_PAYLOAD = '{"action": "T2_TECHNICAL", "conditions": [{"attr": "severity", ' \
        '"op": "lte", "value": 2}]}'


class ParseBase:
    """The two versions of the parser must behave the same.

    Each rung has its own, with its own error class: rung 2 was written as a
    separate package precisely so as not to touch rung 1. The duplication is
    deliberate; what must not happen is that they diverge.
    """

    parse = staticmethod(parse_payload)
    error = ProposalError

    def test_bare_json(self):
        self.assertEqual(self.parse(RULE_PAYLOAD)["action"], "T2_TECHNICAL")

    def test_with_a_markdown_fence(self):
        self.assertEqual(self.parse(f"```json\n{RULE_PAYLOAD}\n```")["action"],
                         "T2_TECHNICAL")

    def test_with_a_fence_and_no_language(self):
        self.assertEqual(self.parse(f"```\n{RULE_PAYLOAD}\n```")["action"],
                         "T2_TECHNICAL")

    def test_with_preamble_and_epilogue(self):
        text = f"Claro, aqui tienes la regla:\n{RULE_PAYLOAD}\nEspero que te sirva."
        self.assertEqual(self.parse(text)["action"], "T2_TECHNICAL")

    def test_with_a_preamble_inside_the_fence(self):
        text = f"Analizando el ticket...\n```json\n{RULE_PAYLOAD}\n```\nListo."
        self.assertEqual(self.parse(text)["action"], "T2_TECHNICAL")

    def test_with_spaces_and_newlines(self):
        self.assertEqual(self.parse(f"\n\n  {RULE_PAYLOAD}  \n\n")["action"],
                         "T2_TECHNICAL")

    def test_without_json_it_raises_ProposalError(self):
        with self.assertRaises(self.error):
            self.parse("No puedo ayudarte con eso.")

    def test_broken_json_raises_ProposalError(self):
        with self.assertRaises(self.error):
            self.parse('{"action": "T2_TECHNICAL", "conditions": [')

    def test_closing_brace_before_the_opening_one(self):
        with self.assertRaises(self.error):
            self.parse("} esto no es un objeto {")

    def test_empty_text(self):
        with self.assertRaises(self.error):
            self.parse("")

    def test_the_error_carries_the_reason(self):
        """`rejected_reason` ends up in the raw record of each case, so the
        reason has to say something."""
        try:
            self.parse("nada")
        except self.error as exc:
            self.assertIn("sin objeto JSON", str(exc))
        else:
            self.fail("no levanto ProposalError")


class TestParseRung1(ParseBase, unittest.TestCase):
    parse = staticmethod(parse_payload)
    error = ProposalError


class TestParseRung2(ParseBase, unittest.TestCase):
    parse = staticmethod(parse_payload2)
    error = ProposalError2


class TestTheTwoParsersAgree(unittest.TestCase):

    INPUTS = [RULE_PAYLOAD, f"```json\n{RULE_PAYLOAD}\n```", f"bla\n{RULE_PAYLOAD}\nbla"]

    def test_same_result_on_the_good_inputs(self):
        for text in self.INPUTS:
            with self.subTest(text[:30]):
                self.assertEqual(parse_payload(text), parse_payload2(text))

    def test_same_rejection_on_the_bad_ones(self):
        for text in ("", "no", '{"a":'):
            with self.subTest(text):
                with self.assertRaises(ProposalError):
                    parse_payload(text)
                with self.assertRaises(ProposalError2):
                    parse_payload2(text)

    def test_each_loop_catches_its_own_error_class(self):
        """They are DIFFERENT classes and neither inherits from the other:
        catching the wrong one would let a long run die on the first decorated
        JSON. Each shadow loop imports the one from its own package, and it must
        stay that way."""
        self.assertIsNot(ProposalError, ProposalError2)
        self.assertNotIsInstance(ProposalError2("x"), ProposalError)

        import rung2.shadow2 as shadow2

        import harness.shadow as shadow1
        self.assertIs(shadow1.ProposalError, ProposalError)
        self.assertIs(shadow2.ProposalError, ProposalError2)


if __name__ == "__main__":
    unittest.main()
