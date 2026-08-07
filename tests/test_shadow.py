"""
The shadow loop and the metrics it produces.

The figures the four FINDINGS cite are defined here, so what is tested is their
SEMANTICS, not their value:

  * silent error = failures among the cases a rule decided with complete
    confidence. Computed ONLY over ACTION. An impasse is not a silent error:
    the system knows that it does not know.
  * reuse = fraction of rules that got to fire after being born. A firing is a
    case resolved without calling the LLM.
  * the ONLY escalation trigger is the impasse (coverage or conflict), never
    "the answer was incorrect". It is precisely that separation that makes the
    silent error measurable: if the loop escalated on being wrong, it would be
    using the oracle and there would be no silent error to measure.
"""

from __future__ import annotations

import unittest

from harness.domain import Case, generate_corpus
from harness.dsl import RuleEngine
from harness.proposers import ProposalError
from harness.shadow import run_shadow


class ProponenteGuionizado:
    """Returns whatever it is told to, case by case. No LLM, no heuristic."""

    name = "guionizado"

    def __init__(self, guion):
        self.guion = list(guion)
        self.vistos = []

    def propose(self, case, true_action_hint):
        self.vistos.append((case, true_action_hint))
        siguiente = self.guion.pop(0) if self.guion else None
        if isinstance(siguiente, Exception):
            raise siguiente
        if siguiente is None:                      # rule that memorizes the case
            siguiente = {
                "action": true_action_hint,
                "conditions": [{"attr": a, "op": "eq", "value": getattr(case, a)}
                               for a in ("severity", "product")],
            }
        return siguiente["action"], siguiente


def corpus_corto(n: int = 40):
    return generate_corpus(n, seed=17)


class TestDisparadorDeEscalacion(unittest.TestCase):

    def test_el_primer_caso_siempre_escala(self):
        """Empty base: coverage IMPASSE."""
        res = run_shadow(corpus_corto(1), RuleEngine(), ProponenteGuionizado([]))
        self.assertEqual(res.records[0].outcome, "IMPASSE")
        self.assertTrue(res.records[0].escalated)

    def test_una_regla_equivocada_que_casa_NO_escala(self):
        """This is the definition of silent error: the system decides wrongly
        and carries on unaware. If this escalated, the loop would see the
        oracle."""
        prop = ProponenteGuionizado([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
        }])
        res = run_shadow(corpus_corto(30), RuleEngine(), prop)
        self.assertEqual(sum(1 for r in res.records if r.escalated), 1)
        fallos = [r for r in res.records[1:] if r.correct is False]
        self.assertGreater(len(fallos), 0)
        self.assertTrue(all(not r.escalated for r in fallos))

    def test_el_conflicto_escala_por_defecto(self):
        engine = RuleEngine()
        prop = ProponenteGuionizado([])
        res = run_shadow(corpus_corto(60), engine, prop)
        conflictos = [r for r in res.records if r.outcome == "CONFLICT"]
        for r in conflictos:
            self.assertTrue(r.escalated)

    def test_escalate_on_conflict_False_no_escala(self):
        engine = RuleEngine()
        engine.rules = []
        prop = ProponenteGuionizado([])
        res = run_shadow(corpus_corto(60), engine, prop, escalate_on_conflict=False)
        for r in res.records:
            if r.outcome == "CONFLICT":
                self.assertFalse(r.escalated)
                self.assertIsNone(r.predicted)


class TestToleranciaAFallos(unittest.TestCase):
    """A 2000-case run cannot die at case 1500 over a broken JSON."""

    def test_una_propuesta_fallida_se_cuenta_y_el_bucle_sigue(self):
        prop = ProponenteGuionizado([ProposalError("JSON mal cerrado")])
        res = run_shadow(corpus_corto(10), RuleEngine(), prop)
        self.assertEqual(res.failed, 1)
        self.assertEqual(len(res.records), 10)
        self.assertIn("proposal_failed", res.records[0].rejected_reason)

    def test_una_regla_invalida_se_rechaza_sin_entrar_en_la_base(self):
        prop = ProponenteGuionizado([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "urgencia", "op": "eq", "value": 9}],
        }])
        engine = RuleEngine()
        res = run_shadow(corpus_corto(3), engine, prop)
        self.assertEqual(res.rejected, 1)
        self.assertIsNotNone(res.records[0].rejected_reason)
        # the failed proposal leaves no rule, so case 2 escalates again
        self.assertTrue(res.records[1].escalated)

    def test_la_accion_propuesta_se_registra_aunque_la_regla_se_rechace(self):
        """The two error axes are independent: choosing the wrong queue when
        proposing is measured separately from the rule's scope."""
        prop = ProponenteGuionizado([{
            "action": "T1_GENERAL",
            "conditions": [{"attr": "urgencia", "op": "eq", "value": 9}],
        }])
        res = run_shadow(corpus_corto(1), RuleEngine(), prop)
        self.assertEqual(res.records[0].predicted, "T1_GENERAL")
        self.assertIsNotNone(res.records[0].proposal_action_correct)


class TestMetricas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res = run_shadow(corpus_corto(200), RuleEngine(),
                             ProponenteGuionizado([]))
        cls.m = cls.res.metrics

    def test_hay_un_registro_por_caso(self):
        self.assertEqual(len(self.res.records), 200)
        self.assertEqual(self.m["n_cases"], 200)
        self.assertEqual([r.idx for r in self.res.records], list(range(200)))

    def test_el_error_silencioso_solo_mira_los_casos_cubiertos(self):
        cubiertos = [r for r in self.res.records if r.outcome == "ACTION"]
        aciertos = sum(1 for r in cubiertos if r.correct)
        self.assertAlmostEqual(self.m["silent_error_rate"],
                               1 - aciertos / len(cubiertos), places=4)
        self.assertEqual(self.m["silent_errors_abs"], len(cubiertos) - aciertos)

    def test_la_cobertura_es_la_fraccion_de_ACTION(self):
        cubiertos = sum(1 for r in self.res.records if r.outcome == "ACTION")
        self.assertAlmostEqual(self.m["coverage"], cubiertos / 200, places=4)

    def test_la_reutilizacion_cuenta_reglas_con_al_menos_un_disparo(self):
        vivas = sum(1 for r in self.res.rules if r.fire_count >= 1)
        self.assertAlmostEqual(self.m["reuse_rate"],
                               vivas / len(self.res.rules), places=4)
        self.assertEqual(self.m["dead_rules"],
                         len(self.res.rules) - vivas)

    def test_una_llamada_al_LLM_por_escalacion(self):
        self.assertEqual(self.m["llm_calls"], self.m["escalations"])
        self.assertEqual(self.m["escalations"],
                         sum(1 for r in self.res.records if r.escalated))

    def test_los_aciertos_por_regla_no_superan_sus_disparos(self):
        for r in self.res.rules:
            self.assertLessEqual(r.correct_count, r.fire_count)

    def test_la_curva_de_escalacion_tiene_diez_deciles(self):
        self.assertEqual(len(self.m["escalation_curve_by_decile"]), 10)
        self.assertEqual(self.m["final_decile_escalation_rate"],
                         self.m["escalation_curve_by_decile"][-1])

    def test_la_compresion_es_reglas_entre_politica_oculta(self):
        self.assertEqual(self.m["hidden_policy_size"], 29)
        self.assertAlmostEqual(self.m["compression_ratio"],
                               round(self.m["n_rules"] / 29, 2), places=2)


class TestLaSombraNoActua(unittest.TestCase):
    """CENTRAL PROPERTY: no rule is ever activated; what WOULD have happened is
    recorded. Since tickets share no state, the shadow is exact and not an
    approximation: the recorded decision does not alter the rest of the corpus.
    """

    def test_el_corpus_no_cambia_al_correr_el_bucle(self):
        corpus = corpus_corto(50)
        antes = [c.key() for c in corpus]
        run_shadow(corpus, RuleEngine(), ProponenteGuionizado([]))
        self.assertEqual([c.key() for c in corpus], antes)

    def test_dos_tiradas_identicas_dan_lo_mismo(self):
        def tirada():
            res = run_shadow(corpus_corto(80), RuleEngine(),
                             ProponenteGuionizado([]))
            return [(r.outcome, r.predicted, r.winner_id) for r in res.records]
        self.assertEqual(tirada(), tirada())

    def test_al_proponente_solo_se_le_da_el_caso_y_la_accion(self):
        prop = ProponenteGuionizado([])
        run_shadow(corpus_corto(5), RuleEngine(), prop)
        for case, hint in prop.vistos:
            self.assertIsInstance(case, Case)
            self.assertIsInstance(hint, str)


if __name__ == "__main__":
    unittest.main()
