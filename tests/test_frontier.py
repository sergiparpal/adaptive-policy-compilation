"""
SNAPSHOT de la frontera de mocks: la verificacion en seco del Paso 1.

CLAUDE.md publica estas cifras como comprobacion de integridad: "resultado
esperado, exacto (semilla 17, n=2000); si no coincide, algo se corrompio al
copiar". Aqui dejan de depender de que alguien las lea en una terminal.

ADVERTENCIA QUE ACOMPANA A ESTAS CIFRAS, y que no hay que perder: son
reproducibles pero NO son una referencia de calidad. Todas las reglas de keep_k
tienen exactamente k condiciones, asi que su especificidad es uniforme y el
arbitraje nunca puede invertirlas: los mocks son estructuralmente inmunes al
defecto que destroza la politica real. keep_k(k=4) puntua MEJOR que la politica
verdadera bajo este motor. La "region a batir" esta por encima del techo del
sistema.

Fuente: results/frontier.json, results/FINDINGS.md y el Paso 1 de CLAUDE.md.
Esta prueba llama a `run_shadow`, no a `cmd_frontier`, para no reescribir
results/frontier.json.
"""

from __future__ import annotations

import unittest

from harness.cache_baseline import run_cache_baseline
from harness.dsl import RuleEngine
from harness.proposers import KeepKProposer
from harness.shadow import run_shadow

from .fixtures import corpus

# k -> (reglas, reuso, error silencioso, escalacion)
KEEP_K = {
    4: (113, 0.7965, 0.1728, 0.0565),
    5: (304, 0.7237, 0.1568, 0.1520),
    8: (1743, 0.1176, 0.0000, 0.8715),
}

CACHE_D2 = {"n_rules": 211, "silent": 0.4477, "escal": 0.1055, "cov": 0.8945}

# Suelo de memorizacion. keep_k(8) conserva los ocho atributos: cada regla casa
# un unico caso y solo se reutiliza por los duplicados literales del corpus.
# Cualquier reutilizacion cercana a esto es ruido, no aprendizaje.
MEMORIZATION_FLOOR = 0.1176
UNIQUE_CASES = 1743


def correr_keep_k(k: int) -> dict:
    engine = RuleEngine()
    return run_shadow(list(corpus()), engine, KeepKProposer(k)).metrics


class TestFronteraKeepK(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.m = {k: correr_keep_k(k) for k in KEEP_K}

    def test_cifras_publicadas(self):
        for k, (n_rules, reuse, silent, escal) in KEEP_K.items():
            with self.subTest(k=k):
                m = self.m[k]
                self.assertEqual(m["n_rules"], n_rules)
                self.assertAlmostEqual(m["reuse_rate"], reuse, places=4)
                self.assertAlmostEqual(m["silent_error_rate"], silent, places=4)
                self.assertAlmostEqual(m["escalation_rate"], escal, places=4)

    def test_el_mock_recibe_la_accion_correcta_gratis(self):
        """Deliberado: aisla el eje de GENERALIZACION del de ACTUACION. Con el
        LLM real aparece la segunda fuente de error, que se mide aparte."""
        for k in KEEP_K:
            with self.subTest(k=k):
                self.assertEqual(self.m[k]["proposal_action_accuracy"], 1.0)

    def test_los_mocks_nunca_entran_en_conflicto(self):
        """Todas sus reglas tienen k condiciones: especificidad uniforme, asi
        que el desempate cae siempre en antiguedad. Es la razon por la que
        estas cifras no sirven como referencia de calidad."""
        for k in KEEP_K:
            with self.subTest(k=k):
                self.assertEqual(self.m[k]["conflicts"], 0)

    def test_mas_condiciones_es_menos_reutilizacion_y_menos_error(self):
        reusos = [self.m[k]["reuse_rate"] for k in sorted(KEEP_K)]
        errores = [self.m[k]["silent_error_rate"] for k in sorted(KEEP_K)]
        self.assertEqual(reusos, sorted(reusos, reverse=True))
        self.assertEqual(errores, sorted(errores, reverse=True))


class TestSueloDeMemorizacion(unittest.TestCase):
    """keep_k(8) no induce nada: es la cache de casos con otro nombre."""

    @classmethod
    def setUpClass(cls):
        cls.m = correr_keep_k(8)

    def test_una_regla_por_caso_unico(self):
        self.assertEqual(self.m["n_rules"], UNIQUE_CASES)
        self.assertEqual(len({c.key() for c in corpus()}), UNIQUE_CASES)

    def test_memorizar_no_produce_error_silencioso(self):
        self.assertEqual(self.m["silent_error_rate"], 0.0)

    def test_el_suelo_es_puro_efecto_de_los_duplicados(self):
        self.assertAlmostEqual(self.m["reuse_rate"], MEMORIZATION_FLOOR, places=4)
        # cobertura de keep_k(8) = tasa de duplicados del corpus
        self.assertAlmostEqual(self.m["coverage"], 1 - UNIQUE_CASES / 2000, places=4)


class TestBaselineDeCache(unittest.TestCase):
    """La hipotesis nula del proyecto: sin reglas, vecino mas cercano."""

    @classmethod
    def setUpClass(cls):
        cls.m = run_cache_baseline(list(corpus()), max_dist=2)

    def test_cifras_publicadas(self):
        self.assertEqual(self.m["n_rules"], CACHE_D2["n_rules"])
        self.assertAlmostEqual(self.m["silent_error_rate"], CACHE_D2["silent"], places=4)
        self.assertAlmostEqual(self.m["escalation_rate"], CACHE_D2["escal"], places=4)
        self.assertAlmostEqual(self.m["coverage"], CACHE_D2["cov"], places=4)

    def test_cubre_algo_menos_que_keep_k4_y_se_equivoca_mucho_mas(self):
        """Es la comparacion que justifica que existan reglas: a cobertura
        parecida (0,894 frente a 0,944), la cache falla en el 45% de lo que
        cubre y keep_k(4) en el 17%. Dos veces y media mas error silencioso."""
        keep4 = correr_keep_k(4)
        self.assertLess(abs(self.m["coverage"] - keep4["coverage"]), 0.06)
        self.assertGreater(self.m["silent_error_rate"],
                           2.5 * keep4["silent_error_rate"])

    def test_d0_es_memorizacion_exacta(self):
        m0 = run_cache_baseline(list(corpus()), max_dist=0)
        self.assertEqual(m0["silent_error_rate"], 0.0)
        self.assertEqual(m0["n_rules"], UNIQUE_CASES)


if __name__ == "__main__":
    unittest.main()
