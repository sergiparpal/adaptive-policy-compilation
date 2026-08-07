"""
THE CENTRAL INVARIANT: the transcription of the hidden policy into the DSL is
faithful.

The claim rung 1 closes on depends on this: "the DSL is not the culprit; it is
an execution failure, not a representation failure". If the transcription were
not faithful, the 0.5875 ceiling would not measure the arbitration but a copying
error, and the whole rung would change meaning.

The check is EXHAUSTIVE over the 134,400 combinations of the space, not over the
corpus: a rule can be equivalent on the 2000 sampled cases and not in the space.
It costs ~1.5 s and is the most expensive test in the suite.

It is the same check `verify_encoding()` performs in
`harness/ceiling_check.py`, rewritten here so that a failure says WHICH rule and
in WHICH case, instead of printing a count.
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
    """The 29 DSL rules against the 29 original predicates."""

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
        """Over the 134,400 combinations, not over the corpus."""
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
        """`lambda c: True` is encoded as `severity gte 1` because the validator
        requires at least one condition. It must cover the WHOLE space."""
        h29 = self.rules[-1]
        self.assertEqual(h29.rule_id, "H29")
        self.assertEqual(space().extension(h29.conditions), space().full)

    def test_true_action_esta_definida_en_todo_el_espacio(self):
        for case in self.cases:
            self.assertIn(true_action(case), {a for _h, _p, a in HIDDEN_RULES})


if __name__ == "__main__":
    unittest.main()
