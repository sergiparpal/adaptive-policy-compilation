"""
El parseo de lo que devuelve el proponente.

Es la unica parte de la ruta del LLM que se puede probar sin gastar dinero, y es
la que decide si una tirada larga sobrevive. La extraccion es TOLERANTE a
proposito —vallas markdown, preambulos, epilogos— porque los modelos baratos
adornan la respuesta, y perder una tirada de 2000 casos en el caso 1500 por un
JSON mal cerrado seria absurdo. Lo que NO puede hacer es tolerar de mas: si
acepta basura, la basura entra en la base como regla.

`failed_proposals` en las metricas cuenta exactamente los casos en que esto
levanta `ProposalError`.
"""

from __future__ import annotations

import unittest

from harness.proposers import ProposalError, parse_payload
from peldano2.proposers2 import ProposalError as ProposalError2
from peldano2.proposers2 import parse_payload as parse_payload2

REGLA = '{"action": "T2_TECHNICAL", "conditions": [{"attr": "severity", ' \
        '"op": "lte", "value": 2}]}'


class BaseParseo:
    """Las dos versiones del parseador deben comportarse igual.

    Cada peldano tiene la suya, con su propia clase de error: el peldano 2 se
    escribio como paquete aparte precisamente para no tocar el 1. La
    duplicacion es deliberada; lo que no puede pasar es que diverjan.
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
        """`rejected_reason` acaba en el registro crudo de cada caso, asi que
        el motivo tiene que decir algo."""
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
        """Son clases DISTINTAS y ninguna hereda de la otra: capturar la que no
        toca dejaria morir una tirada larga en el primer JSON adornado. Cada
        bucle en sombra importa la de su paquete, y asi debe seguir."""
        self.assertIsNot(ProposalError, ProposalError2)
        self.assertNotIsInstance(ProposalError2("x"), ProposalError)

        import peldano2.shadow2 as shadow2

        import harness.shadow as shadow1
        self.assertIs(shadow1.ProposalError, ProposalError)
        self.assertIs(shadow2.ProposalError, ProposalError2)


if __name__ == "__main__":
    unittest.main()
