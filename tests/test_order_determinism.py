"""
REGRESSION test for the August 6, 2026 fix: the greedy search no longer depends
on the hash.

WHAT HAPPENED. The greedy argmax walked a `set` of rule identifiers, so the
tie-break was at the mercy of the iteration order of a set of strings, which
depends on `PYTHONHASHSEED`. The same cell gave between 0.5880 and 0.5991
depending on the hash. It was discovered with two rungs already closed on top of
it. The fix —iterating over `sorted(left)`— is one line; the problem is that
nothing would have caught it.

This is what catches it. `tests/hashseed_child.py` runs the greedy search of
both rungs in a separate process and signs the resulting order; the parent
invokes it with three different `PYTHONHASHSEED` values and compares.

THE WITNESS. The child also signs the iteration order of a set of those same
identifiers. That witness MUST change between seeds: if it did not, the test
would pass without checking anything —it would mean that in this version of
Python hashing is no longer randomized, not that the greedy search is
deterministic.

NO accuracy value is pinned here. The published figures of rungs 3 and 4 are
those of the code PRIOR to the fix and are pending a re-run together with a
serious optimizer; pinning the new values here would create a second official
figure that no FINDINGS backs. See IDEAS.md.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from rung3.order_search import (build_tables, greedy_order, load, split,
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
        """If this fails, the other tests in this class prove nothing."""
        vistos = {r["set_iteration"] for r in self.runs.values()}
        self.assertEqual(len(vistos), len(HASH_SEEDS),
                         "el orden de iteracion del set no cambio entre "
                         "semillas: el resto de esta clase es vacuo")

    def test_el_voraz_del_rung_3_no_depende_del_hash(self):
        vistos = {r["greedy_p3"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"ordenes distintos: {self.runs}")

    def test_el_voraz_del_rung_4_no_depende_del_hash(self):
        vistos = {r["greedy_p4"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"ordenes distintos: {self.runs}")

    def test_la_busqueda_local_multiarranque_no_depende_del_hash(self):
        """Added August 8, 2026 with the optimizer. Its starts come from a
        declared seed and its argmax never walks a set, but that was believed of
        the greedy too until it was checked here."""
        for campo in ("multistart_order", "multistart_score", "multistart_from"):
            with self.subTest(campo):
                vistos = {r[campo] for r in self.runs.values()}
                self.assertEqual(len(vistos), 1, f"{campo} difiere: {vistos}")

    def test_la_exactitud_resultante_es_identica(self):
        vistos = {r["test_p3"] for r in self.runs.values()}
        self.assertEqual(len(vistos), 1, f"exactitudes distintas: {vistos}")

    def test_el_material_de_entrada_es_el_esperado(self):
        """577 rules: the rung 1 base that rungs 3 and 4 start from. If this
        changes, somebody rewrote results/llm_run.json."""
        for s, r in self.runs.items():
            with self.subTest(hashseed=s):
                self.assertEqual(r["n_rules"], 577)


class TestContratoDelVoraz(unittest.TestCase):
    """Properties of the produced order, in the same process."""

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
        """The split is grouped by case identity: otherwise the test would
        reward memorizing, because 12.8% of the corpus has an exact twin."""
        corpus, rules, ext, conds = load()
        below = subsumption_below(rules, ext)
        _m, _u, truth = build_tables(corpus, rules, conds, below)
        tr, te = split(corpus, truth, seed=17)
        claves_train = {corpus[i].key() for i in tr}
        claves_test = {corpus[i].key() for i in te}
        self.assertEqual(claves_train & claves_test, set())


if __name__ == "__main__":
    unittest.main()
