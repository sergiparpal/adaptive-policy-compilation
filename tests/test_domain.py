"""
El corpus y el espacio de casos.

El determinismo del corpus es lo que hace comparables las tiradas (regla dura 4
de CLAUDE.md): mismo n, misma semilla, mismos 2000 casos en el mismo orden. Si
esto se rompe, ninguna cifra del repositorio se puede volver a comparar con
ninguna otra.
"""

from __future__ import annotations

import unittest
from collections import Counter

from harness.domain import (ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case,
                            generate_corpus)
from harness.hidden_policy import true_action

from .fixtures import CORPUS_N, CORPUS_SEED, SPACE_SIZE, corpus

# Estadisticas del corpus canonico. Publicadas en la cabecera de
# results/FINDINGS.md y en el Paso 1 de CLAUDE.md.
UNIQUE_CASES = 1743
DUPLICATE_RATE = 0.1285

# Distribucion de la clase verdadera. Las dos ultimas son las clases criticas y
# raras que el agregado esconde: 20 y 7 casos de 2000.
ACTION_DISTRIBUTION = {
    "T2_TECHNICAL": 726,
    "SELF_SERVICE_DEFLECT": 495,
    "BILLING_SPECIALIST": 271,
    "T1_GENERAL": 255,
    "T3_ENGINEERING": 117,
    "ACCOUNT_MANAGER": 109,
    "SECURITY_INCIDENT": 20,
    "ONCALL_ESCALATION": 7,
}


class TestEspacioDeCasos(unittest.TestCase):

    def test_el_producto_de_los_dominios_es_134400(self):
        n = 1
        for attr in ATTRIBUTES:
            n *= len(DOMAINS[attr])
        self.assertEqual(n, SPACE_SIZE)

    def test_todo_atributo_tiene_dominio_declarado(self):
        self.assertEqual(set(ATTRIBUTES), set(DOMAINS))

    def test_los_numericos_son_los_dos_declarados(self):
        self.assertEqual(NUMERIC_ATTRS, {"severity", "prior_tickets_30d"})
        for attr in NUMERIC_ATTRS:
            for v in DOMAINS[attr]:
                self.assertIsInstance(v, int)
                self.assertNotIsInstance(v, bool)

    def test_hay_ocho_acciones_sin_repetir(self):
        self.assertEqual(len(ACTIONS), 8)
        self.assertEqual(len(set(ACTIONS)), 8)


class TestCorpusCanonico(unittest.TestCase):

    def test_tamano_y_unicos(self):
        c = corpus()
        self.assertEqual(len(c), CORPUS_N)
        self.assertEqual(len({x.key() for x in c}), UNIQUE_CASES)

    def test_tasa_de_duplicados(self):
        c = corpus()
        rate = 1 - len({x.key() for x in c}) / len(c)
        self.assertAlmostEqual(rate, DUPLICATE_RATE, places=4)

    def test_es_reproducible(self):
        a = generate_corpus(CORPUS_N, seed=CORPUS_SEED)
        b = generate_corpus(CORPUS_N, seed=CORPUS_SEED)
        self.assertEqual(a, b)
        self.assertEqual(tuple(a), corpus())

    def test_un_prefijo_de_n_mayor_es_el_corpus_de_n_menor(self):
        """El caso i no depende de cuantos se pidan: --n 100 es prefijo de
        --n 2000. De ahi que la prueba corta y la larga vean los mismos casos
        (lo que NO es determinista es el proponente; ver CLAUDE.md, Paso 3)."""
        self.assertEqual(generate_corpus(100, seed=CORPUS_SEED),
                         list(corpus()[:100]))

    def test_otra_semilla_da_otro_corpus(self):
        self.assertNotEqual(generate_corpus(CORPUS_N, seed=18), list(corpus()))

    def test_todos_los_valores_caen_en_su_dominio(self):
        for case in corpus():
            for attr in ATTRIBUTES:
                self.assertIn(getattr(case, attr), DOMAINS[attr],
                              msg=f"{attr} fuera de dominio en {case}")

    def test_distribucion_de_la_clase_verdadera(self):
        got = Counter(true_action(c) for c in corpus())
        self.assertEqual(dict(got.most_common()), ACTION_DISTRIBUTION)
        self.assertEqual(sum(ACTION_DISTRIBUTION.values()), CORPUS_N)

    def test_las_ocho_clases_aparecen(self):
        self.assertEqual(set(ACTION_DISTRIBUTION), set(ACTIONS))

    def test_baseline_de_clase_mayoritaria(self):
        top = max(ACTION_DISTRIBUTION.values())
        self.assertAlmostEqual(top / CORPUS_N, 0.363, places=3)


class TestCase(unittest.TestCase):

    def test_key_sigue_el_orden_de_ATTRIBUTES(self):
        c = corpus()[0]
        self.assertEqual(c.key(), tuple(getattr(c, a) for a in ATTRIBUTES))

    def test_as_dict_lleva_los_ocho_atributos(self):
        self.assertEqual(set(corpus()[0].as_dict()), set(ATTRIBUTES))

    def test_es_inmutable_y_hashable(self):
        c = corpus()[0]
        hash(c)
        with self.assertRaises(Exception):
            c.severity = 1                      # frozen dataclass

    def test_igualdad_por_valor(self):
        c = corpus()[0]
        self.assertEqual(c, Case(**c.as_dict()))


if __name__ == "__main__":
    unittest.main()
