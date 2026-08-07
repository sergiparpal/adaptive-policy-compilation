"""
REGRESION del arreglo del 6 de agosto de 2026: el voraz ya no depende del hash.

QUE PASO. El argmax del voraz recorria un `set` de identificadores de regla, asi
que el desempate quedaba a merced del orden de iteracion de un set de cadenas,
que depende de `PYTHONHASHSEED`. La misma celda daba entre 0,5880 y 0,5991 segun
el hash. Se descubrio con dos peldanos ya cerrados encima. El arreglo —iterar
sobre `sorted(left)`— es de una linea; el problema es que nada lo habria pillado.

Esto es lo que lo pilla. `tests/hashseed_child.py` corre el voraz de los dos
peldanos en un proceso aparte y firma el orden que sale; el padre lo invoca con
tres `PYTHONHASHSEED` distintos y compara.

EL TESTIGO. El hijo firma tambien el orden de iteracion de un set de esos mismos
identificadores. Ese testigo DEBE cambiar entre semillas: si no cambiase, la
prueba pasaria sin comprobar nada —querria decir que en esta version de Python
el hash ya no se aleatoriza, no que el voraz sea determinista.

NO se clava aqui ningun valor de exactitud. Las cifras publicadas de los
peldanos 3 y 4 son las del codigo ANTERIOR al arreglo y estan pendientes de
re-correr junto con un optimizador serio; fijar aqui los valores nuevos crearia
una segunda cifra oficial que no respalda ningun FINDINGS. Ver IDEAS.md.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from peldano3.order_search import (build_tables, greedy_order, load, split,
                                   subsumption_below)

REPO = Path(__file__).resolve().parent.parent
HASH_SEEDS = ("0", "1", "2")


def correr_hijo(hashseed: str) -> dict:
    env = dict(os.environ, PYTHONHASHSEED=hashseed)
    p = subprocess.run([sys.executable, "-m", "tests.hashseed_child"],
                       cwd=REPO, env=env, capture_output=True, text=True,
                       timeout=300)
    if p.returncode != 0:
        raise AssertionError(f"el hijo fallo con PYTHONHASHSEED={hashseed}:\n"
                             f"{p.stderr}")
    return json.loads(p.stdout)


class TestInvarianciaAlHashSeed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = {s: correr_hijo(s) for s in HASH_SEEDS}

    def test_el_testigo_confirma_que_el_hash_se_aleatoriza(self):
        """Si esto falla, las demas pruebas de esta clase no prueban nada."""
        vistos = {r["set_iteration"] for r in self.runs.values()}
        self.assertEqual(len(vistos), len(HASH_SEEDS),
                         "el orden de iteracion del set no cambio entre "
                         "semillas: el resto de esta clase es vacuo")

    def test_el_voraz_del_peldano_3_no_depende_del_hash(self):
        vistos = {r["greedy_p3"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"ordenes distintos: {self.runs}")

    def test_el_voraz_del_peldano_4_no_depende_del_hash(self):
        vistos = {r["greedy_p4"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"ordenes distintos: {self.runs}")

    def test_la_exactitud_resultante_es_identica(self):
        vistos = {r["test_p3"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"exactitudes distintas: {vistos}")

    def test_el_material_de_entrada_es_el_esperado(self):
        """577 reglas: la base del peldano 1 de la que parten los peldanos 3 y
        4. Si esto cambia, alguien reescribio results/llm_run.json."""
        for s, r in self.runs.items():
            with self.subTest(hashseed=s):
                self.assertEqual(r["n_rules"], 577)


class TestContratoDelVoraz(unittest.TestCase):
    """Propiedades del orden producido, en el mismo proceso."""

    @classmethod
    def setUpClass(cls):
        corpus, rules, ext, conds = load()
        cls.rules = rules
        cls.action = {r["rule_id"]: r["action"] for r in rules}
        below = subsumption_below(rules, ext)
        cls.matched, _undef, cls.truth = build_tables(corpus, rules, conds, below)
        cls.train, _test = split(corpus, cls.truth, seed=17)

    def orden(self):
        return greedy_order(self.rules, self.matched, self.truth,
                            self.action, self.train)

    def test_es_una_permutacion_de_todas_las_reglas(self):
        order = self.orden()
        self.assertEqual(len(order), len(self.rules))
        self.assertEqual(set(order), {r["rule_id"] for r in self.rules})

    def test_dos_llamadas_dan_el_mismo_orden(self):
        self.assertEqual(self.orden(), self.orden())

    def test_la_particion_es_estable_y_disjunta(self):
        corpus, rules, ext, conds = load()
        below = subsumption_below(rules, ext)
        _m, _u, truth = build_tables(corpus, rules, conds, below)
        tr1, te1 = split(corpus, truth, seed=17)
        tr2, te2 = split(corpus, truth, seed=17)
        self.assertEqual((tr1, te1), (tr2, te2))
        self.assertEqual(set(tr1) & set(te1), set())
        self.assertEqual(len(tr1) + len(te1), 2000)

    def test_las_copias_de_un_caso_caen_del_mismo_lado(self):
        """La particion se agrupa por identidad de caso: si no, el test
        premiaria memorizar, porque el 12,8% del corpus tiene gemelo exacto."""
        corpus, rules, ext, conds = load()
        below = subsumption_below(rules, ext)
        _m, _u, truth = build_tables(corpus, rules, conds, below)
        tr, te = split(corpus, truth, seed=17)
        claves_train = {corpus[i].key() for i in tr}
        claves_test = {corpus[i].key() for i in te}
        self.assertEqual(claves_train & claves_test, set())


if __name__ == "__main__":
    unittest.main()
