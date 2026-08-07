"""
SNAPSHOT de los techos: las cifras publicadas, clavadas al digito.

Los cuatro arbitrajes se miden sobre EXACTAMENTE las mismas 29 reglas y el
mismo corpus. Lo unico que cambia entre ellos es como se resuelve que regla
gana, que es justo lo que los cuatro peldanos investigan.

  especificidad   0,5875   el defecto del peldano 1; 505 CONFLICT
  subsuncion      0,6315   se abstiene en vez de inventar: 0 error silencioso
  hibrido         1,0000   subsuncion + 199 aristas declaradas (peldano 2)
  prioridad       1,0000   primera-que-casa, la semantica de la politica

Si una de estas pruebas falla, el numero esperado NO se actualiza: se averigua
que cambio y se fecha la errata en el FINDINGS correspondiente.

Fuentes: results/FINDINGS.md (0,5875 y 0,6315), results2/FINDINGS2.md (1,0000),
CLAUDE.md Paso 0. Ninguna prueba de aqui llama a un `main()`, de modo que
results/ y results2/ no se tocan.
"""

from __future__ import annotations

import unittest
from collections import Counter

from harness.ceiling_check import build_rules, decide_by_priority, measure
from harness.dsl import RuleEngine
from harness.hidden_policy import true_action
from peldano2.ceiling_check2 import REF
from peldano2.hidden_priority import build_hidden_engine

from .fixtures import corpus, space, subsumption_only_engine

# --- peldano 1, arbitraje por especificidad (RuleEngine.decide) -------------
SPEC_ACTION, SPEC_IMPASSE, SPEC_CONFLICT = 1495, 0, 505
SPEC_COVERAGE, SPEC_SILENT, SPEC_E2E = 0.7475, 0.2140, 0.5875
SPEC_SILENT_ABS = 320

# --- peldano 1, subsuncion sola --------------------------------------------
SUB_ACTION, SUB_CONFLICT, SUB_E2E = 1263, 737, 0.6315

# --- peldano 2, hibrido ------------------------------------------------------
HYB_DECLARED_EDGES = 199        # coste de autoria de esta politica
HYB_SUBSUMPTION_PAIRS = 61      # pares que la estructura ya ordena sola
HYB_POSSIBLE_PAIRS = 29 * 28 // 2


def medir(engine_decide) -> dict:
    """Cuenta ACTION/IMPASSE/CONFLICT y aciertos sobre el corpus canonico."""
    out = Counter()
    ok = 0
    for case in corpus():
        outcome, winner, _ = engine_decide(case)
        out[outcome] += 1
        if outcome == "ACTION" and winner.action == true_action(case):
            ok += 1
    n = len(corpus())
    return {"out": out, "correct": ok, "e2e": ok / n,
            "silent": (1 - ok / out["ACTION"]) if out["ACTION"] else 0.0}


class TestTechoPorEspecificidad(unittest.TestCase):
    """PARADA 0 de CLAUDE.md: mientras esto no sea ~100%, toda tirada con LLM
    queda anulada de antemano. Sigue sin serlo, y esa es la cifra registrada."""

    @classmethod
    def setUpClass(cls):
        engine = RuleEngine()
        engine.rules = build_rules()
        cls.m = measure(list(corpus()), engine.decide, "especificidad")

    def test_reparto_de_resultados(self):
        self.assertEqual(self.m["action"], SPEC_ACTION)
        self.assertEqual(self.m["impasse"], SPEC_IMPASSE)
        self.assertEqual(self.m["conflict"], SPEC_CONFLICT)

    def test_cobertura(self):
        self.assertAlmostEqual(self.m["coverage"], SPEC_COVERAGE, places=4)

    def test_error_silencioso(self):
        self.assertAlmostEqual(self.m["silent_error_rate"], SPEC_SILENT, places=4)
        self.assertEqual(self.m["silent_errors_abs"], SPEC_SILENT_ABS)

    def test_exactitud_extremo_a_extremo(self):
        self.assertAlmostEqual(self.m["accuracy_end_to_end"], SPEC_E2E, places=4)

    def test_el_25_por_ciento_de_conflictos(self):
        self.assertAlmostEqual(SPEC_CONFLICT / len(corpus()), 0.2525, places=4)

    def test_no_alcanza_la_PARADA_0(self):
        """Documenta el estado, no lo aprueba: si algun dia esto falla porque
        el techo subio a ~100%, hay que revisar CLAUDE.md entero."""
        self.assertLess(self.m["accuracy_end_to_end"], 0.995)


class TestTechoPorPrioridad(unittest.TestCase):
    """Con las reglas en el orden de HIDDEN_RULES, ganar la mas antigua ES la
    semantica primera-que-casa de la politica. Debe dar 100% exacto."""

    @classmethod
    def setUpClass(cls):
        rules = build_rules()
        cls.m = measure(list(corpus()),
                        lambda c: decide_by_priority(rules, c), "prioridad")

    def test_cubre_todo_y_acierta_todo(self):
        self.assertEqual(self.m["action"], len(corpus()))
        self.assertEqual(self.m["impasse"], 0)
        self.assertEqual(self.m["conflict"], 0)
        self.assertEqual(self.m["accuracy_end_to_end"], 1.0)
        self.assertEqual(self.m["silent_error_rate"], 0.0)

    def test_el_orden_inverso_no_lo_consigue(self):
        """El orden importa y no es un detalle: invertirlo destruye la
        politica (12,8% en FINDINGS.md). Aqui basta con que no siga en 1,0."""
        rules = build_rules()
        for i, r in enumerate(rules):
            r.born_at = -i
        m = measure(list(corpus()), lambda c: decide_by_priority(rules, c), "inv")
        self.assertLess(m["accuracy_end_to_end"], 0.5)


class TestSubsuncionSola(unittest.TestCase):
    """Nivel 1 del motor del peldano 2, sin ninguna arista declarada."""

    @classmethod
    def setUpClass(cls):
        cls.m = medir(subsumption_only_engine().decide)

    def test_reparto_y_exactitud(self):
        self.assertEqual(self.m["out"]["ACTION"], SUB_ACTION)
        self.assertEqual(self.m["out"]["CONFLICT"], SUB_CONFLICT)
        self.assertEqual(self.m["out"]["IMPASSE"], 0)
        self.assertAlmostEqual(self.m["e2e"], SUB_E2E, places=4)

    def test_error_silencioso_cero(self):
        """La propiedad que justifica el nivel 1: cuando no sabe, se abstiene.
        Abstenerse es correcto; inventar es lo que produce error silencioso."""
        self.assertEqual(self.m["silent"], 0.0)


class TestTechoHibrido(unittest.TestCase):
    """PASO 0 del peldano 2. Este si pasa: 100% con la politica cargada."""

    @classmethod
    def setUpClass(cls):
        cls.engine, cls.declared, cls.stats = build_hidden_engine(space())
        cls.m = medir(cls.engine.decide)

    def test_ejecuta_la_politica_al_cien_por_cien(self):
        self.assertEqual(self.m["e2e"], 1.0)
        self.assertEqual(self.m["silent"], 0.0)
        self.assertEqual(self.m["out"]["CONFLICT"], 0)
        self.assertEqual(self.m["out"]["IMPASSE"], 0)

    def test_aristas_declaradas(self):
        self.assertEqual(self.stats["declared"], HYB_DECLARED_EDGES)
        self.assertEqual(len(self.declared), HYB_DECLARED_EDGES)

    def test_ninguna_arista_minima_es_rechazada(self):
        """Las aristas se derivan del orden de capas verdadero, asi que el
        validador no deberia tumbar ninguna. Si tumbase alguna, la suposicion
        de que la subsuncion es sound sobre esta politica seria falsa."""
        self.assertEqual(self.stats["rejected"], [])

    def test_la_estructura_ordena_61_pares_por_si_sola(self):
        pares = sum(len(s) for s in self.engine.sub_below.values())
        self.assertEqual(pares, HYB_SUBSUMPTION_PAIRS)

    def test_no_se_declara_el_orden_total(self):
        """Declarar los 406 pares seria hacer trampa: mediria si funciona un
        orden total, cuya respuesta ya se conoce."""
        self.assertEqual(HYB_POSSIBLE_PAIRS, 406)
        self.assertLess(self.stats["declared"], HYB_POSSIBLE_PAIRS)

    def test_el_reparto_de_pares_cuadra(self):
        s = self.stats
        total = (s["declared"] + s["skipped_disjoint"]
                 + s["skipped_subsumed_by_structure"] + s["skipped_same_action"]
                 + len(s["rejected"]))
        self.assertEqual(total, HYB_POSSIBLE_PAIRS)


class TestTablaDeReferenciaDelPeldano2(unittest.TestCase):
    """`ceiling_check2.REF` imprime las cifras del peldano 1 como referencia.
    Estan escritas a mano; esta prueba comprueba que siguen siendo ciertas."""

    def test_referencia_de_especificidad(self):
        e2e, silent, conflict = REF["especificidad (peldano 1)"]
        self.assertAlmostEqual(e2e, SPEC_E2E, places=4)
        self.assertAlmostEqual(silent, SPEC_SILENT, places=4)
        self.assertEqual(conflict, SPEC_CONFLICT)

    def test_referencia_de_subsuncion(self):
        e2e, silent, conflict = REF["subsuncion sola (peldano 1)"]
        self.assertAlmostEqual(e2e, SUB_E2E, places=4)
        self.assertEqual(silent, 0.0)
        self.assertEqual(conflict, SUB_CONFLICT)


if __name__ == "__main__":
    unittest.main()
