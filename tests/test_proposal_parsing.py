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
from peldano2.proposers2 import ProposalError as ProposalError2
from peldano2.proposers2 import parse_payload as parse_payload2

REGLA = '{"action": "T2_TECHNICAL", "conditions": [{"attr": "severity", ' \
        '"op": "lte", "value": 2}]}'


class BaseParseo:
    """The two versions of the parser must behave the same.

    Each rung has its own, with its own error class: rung 2 was written as a
    separate package precisely so as not to touch rung 1. The duplication is
    deliberate; what must not happen is that they diverge.
    """

    parse = staticmethod(parse_payload)
    error = ProposalError

    def test_json_pelado(self):
        self.assertEqual(self.parse(REGLA)["action"], "T2_TECHNICAL")

    def test_con_valla_markdown(self):
        self.assertEqual(self.parse(f"```json\n{REGLA}\n```")["action"],
                         "T2_TECHNICAL")

    def test_con_valla_sin_lenguaje(self):
        self.assertEqual(self.parse(f"```\n{REGLA}\n```")["action"],
                         "T2_TECHNICAL")

    def test_con_preambulo_y_epilogo(self):
        texto = f"Claro, aqui tienes la regla:\n{REGLA}\nEspero que te sirva."
        self.assertEqual(self.parse(texto)["action"], "T2_TECHNICAL")

    def test_con_preambulo_dentro_de_la_valla(self):
        texto = f"Analizando el ticket...\n```json\n{REGLA}\n```\nListo."
        self.assertEqual(self.parse(texto)["action"], "T2_TECHNICAL")

    def test_con_espacios_y_saltos(self):
        self.assertEqual(self.parse(f"\n\n  {REGLA}  \n\n")["action"],
                         "T2_TECHNICAL")

    def test_sin_json_levanta_ProposalError(self):
        with self.assertRaises(self.error):
            self.parse("No puedo ayudarte con eso.")

    def test_json_roto_levanta_ProposalError(self):
        with self.assertRaises(self.error):
            self.parse('{"action": "T2_TECHNICAL", "conditions": [')

    def test_llave_de_cierre_antes_que_la_de_apertura(self):
        with self.assertRaises(self.error):
            self.parse("} esto no es un objeto {")

    def test_texto_vacio(self):
        with self.assertRaises(self.error):
            self.parse("")

    def test_el_error_lleva_el_motivo(self):
        """`rejected_reason` ends up in the raw record of each case, so the
        reason has to say something."""
        try:
            self.parse("nada")
        except self.error as exc:
            self.assertIn("sin objeto JSON", str(exc))
        else:
            self.fail("no levanto ProposalError")


class TestParseoPeldano1(BaseParseo, unittest.TestCase):
    parse = staticmethod(parse_payload)
    error = ProposalError


class TestParseoPeldano2(BaseParseo, unittest.TestCase):
    parse = staticmethod(parse_payload2)
    error = ProposalError2


class TestLosDosParseadoresCoinciden(unittest.TestCase):

    ENTRADAS = [REGLA, f"```json\n{REGLA}\n```", f"bla\n{REGLA}\nbla"]

    def test_mismo_resultado_en_las_entradas_buenas(self):
        for texto in self.ENTRADAS:
            with self.subTest(texto[:30]):
                self.assertEqual(parse_payload(texto), parse_payload2(texto))

    def test_mismo_rechazo_en_las_malas(self):
        for texto in ("", "no", '{"a":'):
            with self.subTest(texto):
                with self.assertRaises(ProposalError):
                    parse_payload(texto)
                with self.assertRaises(ProposalError2):
                    parse_payload2(texto)

    def test_cada_bucle_captura_su_propia_clase_de_error(self):
        """They are DIFFERENT classes and neither inherits from the other:
        catching the wrong one would let a long run die on the first decorated
        JSON. Each shadow loop imports the one from its own package, and it must
        stay that way."""
        self.assertIsNot(ProposalError, ProposalError2)
        self.assertNotIsInstance(ProposalError2("x"), ProposalError)

        import peldano2.shadow2 as shadow2

        import harness.shadow as shadow1
        self.assertIs(shadow1.ProposalError, ProposalError)
        self.assertIs(shadow2.ProposalError, ProposalError2)


if __name__ == "__main__":
    unittest.main()
