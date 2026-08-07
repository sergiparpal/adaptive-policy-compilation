"""
EL INVARIANTE CENTRAL: la transcripcion de la politica oculta al DSL es fiel.

De esto depende la afirmacion sobre la que se cierra el peldano 1: "el DSL no es
el culpable; es fallo de ejecucion, no de representacion". Si la transcripcion
no fuese fiel, el techo de 0,5875 no mediria el arbitraje sino un error de
copia, y el peldano entero cambiaria de significado.

La comprobacion es EXHAUSTIVA sobre las 134.400 combinaciones del espacio, no
sobre el corpus: una regla puede ser equivalente en los 2000 casos muestreados y
no serlo en el espacio. Cuesta ~1,5 s y es la prueba mas cara de la suite.

Es la misma comprobacion que hace `verify_encoding()` en
`harness/ceiling_check.py`, reescrita aqui para que un fallo diga QUE regla y
en QUE caso, en vez de imprimir un recuento.
"""

from __future__ import annotations

import unittest

from harness.ceiling_check import HIDDEN_DSL, all_cases, build_rules
from harness.hidden_policy import HIDDEN_POLICY_SIZE, HIDDEN_RULES, true_action

from .fixtures import SPACE_SIZE, corpus, space


class TestEspacioExhaustivo(unittest.TestCase):

    def test_all_cases_recorre_el_espacio_entero_sin_repetir(self):
        cases = list(all_cases())
        self.assertEqual(len(cases), SPACE_SIZE)
        self.assertEqual(len({c.key() for c in cases}), SPACE_SIZE)

    def test_el_corpus_es_un_subconjunto_del_espacio(self):
        universo = {c.key() for c in all_cases()}
        self.assertTrue({c.key() for c in corpus()} <= universo)


class TestTranscripcion(unittest.TestCase):
    """Las 29 reglas del DSL contra los 29 predicados originales."""

    @classmethod
    def setUpClass(cls):
        cls.rules = build_rules()
        cls.cases = list(all_cases())

    def test_mismos_identificadores_en_el_mismo_orden(self):
        self.assertEqual([r[0] for r in HIDDEN_DSL],
                         [h[0] for h in HIDDEN_RULES])

    def test_mismas_acciones(self):
        self.assertEqual([r[2] for r in HIDDEN_DSL],
                         [h[2] for h in HIDDEN_RULES])

    def test_son_29(self):
        self.assertEqual(len(self.rules), HIDDEN_POLICY_SIZE)
        self.assertEqual(HIDDEN_POLICY_SIZE, 29)

    def test_cada_regla_DSL_es_equivalente_a_su_lambda(self):
        """Sobre las 134.400 combinaciones, no sobre el corpus."""
        fallos = {}
        for case in self.cases:
            for regla, (hid, pred, _act) in zip(self.rules, HIDDEN_RULES):
                if regla.matches(case) != bool(pred(case)):
                    fallos.setdefault(hid, case)
        self.assertEqual(fallos, {}, msg="\n".join(
            f"  {hid}: discrepa ya en {c}" for hid, c in fallos.items()))

    def test_primera_que_casa_reproduce_true_action(self):
        for case in self.cases:
            for regla in self.rules:
                if regla.matches(case):
                    if regla.action != true_action(case):
                        self.fail(f"{regla.rule_id} da {regla.action} y la verdad "
                                  f"es {true_action(case)} en {case}")
                    break
            else:
                self.fail(f"ninguna regla DSL casa {case}: falta el catch-all")

    def test_H29_es_el_catch_all_del_espacio_entero(self):
        """`lambda c: True` se codifica como `severity gte 1` porque el
        validador exige al menos una condicion. Debe cubrir TODO el espacio."""
        h29 = self.rules[-1]
        self.assertEqual(h29.rule_id, "H29")
        self.assertEqual(space().extension(h29.conditions), space().full)

    def test_true_action_esta_definida_en_todo_el_espacio(self):
        for case in self.cases:
            self.assertIn(true_action(case), {a for _h, _p, a in HIDDEN_RULES})


if __name__ == "__main__":
    unittest.main()
