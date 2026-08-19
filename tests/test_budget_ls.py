"""
The harness of step 3 of the audit (`rung3.budget_and_balance_ls`).

What is pinned here is that the instances are the RECORD'S instances. The whole
point of the step is to change one thing — the optimizer — and read the
difference; if the draws, the fractions or the splits moved as well, the
difference would be uninterpretable and no test downstream would notice.

NO figure is pinned here. The three parity checks of phase P3 compare against
published numbers, and they live in the module because they gate its own run;
duplicating them here would create a second official figure, which is the
mistake `tests/test_order_determinism.py` declines to make.

The suite never calls the module's `main()`, so nothing here writes to
`results*/`.
"""

from __future__ import annotations

import ast
import json
import random
import unittest
from collections import Counter
from pathlib import Path

from rung3.budget_and_balance import FRACTIONS, N_DRAWS, N_SPLITS
from rung3.budget_and_balance_ls import (ESPERADO, GROUPS, POOL, PUBLICADO,
                                            PUBLICADO_OBJETIVO,
                                            balanced_objective, record_name,
                                            start_spread, subsample)

REPO = Path(__file__).resolve().parent.parent


class TestElMuestreoEsElDelRegistro(unittest.TestCase):
    """`budget_and_balance` draws its subsample inline. This reproduces that
    expression literally, because the two have to stay the same draw."""

    TREN = list(range(1005))

    def draw_del_registro(self, tr, frac, s, d):
        # copied from `budget_and_balance.main`, deliberately, so that a change
        # there shows up here as a failure and not as a silent divergence
        k = max(1, round(frac * len(tr)))
        rng = random.Random(1000 * s + d)
        return sorted(rng.sample(tr, k)) if frac < 1.0 else tr

    def test_reproduce_la_extraccion_original_en_toda_la_rejilla(self):
        for frac in FRACTIONS:
            for s in range(N_SPLITS):
                for d in range(1 if frac == 1.0 else N_DRAWS):
                    with self.subTest(frac=frac, s=s, d=d):
                        self.assertEqual(
                            subsample(self.TREN, frac, s, d),
                            self.draw_del_registro(self.TREN, frac, s, d))

    def test_la_supervision_plena_es_el_train_entero_y_no_una_muestra(self):
        self.assertIs(subsample(self.TREN, 1.0, 0, 0), self.TREN)

    def test_el_tamano_es_el_declarado_y_nunca_cero(self):
        for frac in FRACTIONS:
            with self.subTest(frac=frac):
                n = len(subsample(self.TREN, frac, 0, 0))
                self.assertEqual(n, max(1, round(frac * len(self.TREN))))
                self.assertGreaterEqual(n, 1)
        self.assertEqual(len(subsample(list(range(3)), 0.01, 0, 0)), 1)

    def test_extracciones_distintas_dan_muestras_distintas(self):
        """If the draw seed stopped depending on (s, d), the five repetitions
        would be one repetition and the reported dispersion would be fiction."""
        muestras = {tuple(subsample(self.TREN, 0.05, s, d))
                    for s in range(N_SPLITS) for d in range(N_DRAWS)}
        self.assertEqual(len(muestras), N_SPLITS * N_DRAWS)


def cadenas_de_codigo(path):
    """
    String literals the module could actually open or write: every `str`
    constant except the docstrings. Comments never reach the AST, so they are
    excluded too — which is the point. The published record has to be NAMED in
    the prose, precisely to say it is not to be touched; what must not exist is
    the name in a place that can become a path.
    """
    arbol = ast.parse(path.read_text(), filename=str(path))
    docs = set()
    for nodo in ast.walk(arbol):
        cuerpo = getattr(nodo, "body", None)
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)) and cuerpo:
            primero = cuerpo[0]
            if isinstance(primero, ast.Expr) and \
                    isinstance(primero.value, ast.Constant) and \
                    isinstance(primero.value.value, str):
                docs.add(id(primero.value))
    return [n.value for n in ast.walk(arbol)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in docs]


class TestElRegistroPublicadoNoSeToca(unittest.TestCase):
    """`rung3.budget_and_balance` has no guard and dumps over its own record
    on finishing. Step 3 obtains greedy-today by importing the function, never
    by running the script."""

    FUENTE = REPO / "rung3" / "budget_and_balance_ls.py"

    def test_no_importa_el_main_del_modulo_sin_guarda(self):
        arbol = ast.parse(self.FUENTE.read_text(), filename=str(self.FUENTE))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ImportFrom) and nodo.module and \
                    nodo.module.endswith("budget_and_balance"):
                nombres = {a.name for a in nodo.names}
                with self.subTest(modulo=nodo.module):
                    self.assertNotIn("main", nombres)

    def test_el_nombre_del_registro_publicado_no_aparece_en_el_codigo(self):
        for s in cadenas_de_codigo(self.FUENTE):
            with self.subTest(cadena=s[:40]):
                self.assertNotIn("budget_and_balance.json", s)


class TestElObjetivoBalanceadoEsUnoSolo(unittest.TestCase):
    """`budget_and_balance.greedy` weights classes with floats and the local
    search weights rules with integers. If those two stopped being the same
    objective, §2 would compare a greedy maximizing one thing against a search
    maximizing another and report the difference as the optimizer."""

    IDS = ["X000", "X001", "X002", "X003"]
    ACTION = {"X000": "A", "X001": "B", "X002": "C", "X003": "A"}
    TRUTH = ["A"] * 7 + ["B"] * 5 + ["C"] * 3

    def test_los_dos_pesos_salen_del_mismo_recuento(self):
        idxs = list(range(len(self.TRUTH)))
        weights, wt, counts, L = balanced_objective(
            self.IDS, self.ACTION, self.TRUTH, idxs)
        self.assertEqual(counts, Counter(self.TRUTH))
        for c in counts:
            # the float form and the integer form, one constant apart
            self.assertAlmostEqual(weights[c] * counts[c], 1.0)
        for rid in self.IDS:
            self.assertEqual(wt[rid] * counts[self.ACTION[rid]], L)
            self.assertAlmostEqual(wt[rid] / L, weights[self.ACTION[rid]])

    def test_el_recuento_es_el_de_budget_and_balance(self):
        """Copied from `budget_and_balance.main`, deliberately: the counts are
        over the LABELLED SUBSET, and the record's are Counter(truth)."""
        idxs = [0, 1, 2, 7, 8, 12]
        _weights, _wt, counts, _L = balanced_objective(
            self.IDS, self.ACTION, self.TRUTH, idxs)
        self.assertEqual(counts, Counter(self.TRUTH[i] for i in idxs))

    def test_no_se_construye_desde_las_mascaras(self):
        """The mask route gives the per-class ceiling, which over the 577 rules
        is not the class size. It must not appear in this module."""
        self.assertNotIn("class_counts_from_masks",
                         (REPO / "rung3" / "budget_and_balance_ls.py")
                         .read_text().split('"""')[-1])


class TestElPresupuestoDeReinicios(unittest.TestCase):
    """The claim `local_search.py` makes for its 64 starts is calibrated at a
    one-in-four hit rate measured WITHOUT weights. `optimizer_check_wt`
    recomputes it at the measured rate; the arithmetic has to be right."""

    def test_el_intervalo_exacto_contiene_la_tasa_y_esta_ordenado(self):
        from rung3.optimizer_check_wt import clopper_pearson

        for k in (0, 1, 6, 12, 32, 64):
            lo, hi = clopper_pearson(k, 64)
            with self.subTest(k=k):
                self.assertLessEqual(lo, k / 64)
                self.assertLessEqual(k / 64, hi)
                self.assertLessEqual(0.0, lo)
                self.assertLessEqual(hi, 1.0)
        self.assertEqual(clopper_pearson(0, 64)[0], 0.0)
        self.assertEqual(clopper_pearson(64, 64)[1], 1.0)

    def test_la_probabilidad_de_fallo_baja_al_subir_la_tasa(self):
        from rung3.optimizer_check_wt import restart_budget

        anterior = None
        for k in (0, 1, 6, 12, 32):
            b = restart_budget(k, 64)
            with self.subTest(k=k):
                self.assertAlmostEqual(b["miss_probability"],
                                       (1 - k / 64) ** 64)
                lo, hi = b["miss_probability_ci95"]
                self.assertLessEqual(lo, b["miss_probability"])
                self.assertLessEqual(b["miss_probability"], hi)
                if anterior is not None:
                    self.assertLess(b["miss_probability"], anterior)
            anterior = b["miss_probability"]

    def test_no_se_toca_la_constante_declarada(self):
        """What was recomputed is the claim about the constant, never the
        constant: changing it after seeing a result is CLAUDE.md rule 6."""
        from rung3.local_search import (DECLARED_NEIGHBOURHOOD,
                                           MULTISTART_SEED, MULTISTART_STARTS)

        self.assertEqual((MULTISTART_SEED, MULTISTART_STARTS,
                          DECLARED_NEIGHBOURHOOD), (17, 64, "move+swap"))

    def test_la_afirmacion_heredada_queda_registrada_para_comparar(self):
        from rung3.optimizer_check_wt import restart_budget

        b = restart_budget(6, 64)
        self.assertAlmostEqual(b["inherited_claim"]["miss_probability"],
                               0.75 ** 64)
        self.assertGreater(b["miss_probability"],
                           b["inherited_claim"]["miss_probability"])


class TestLasExpectativasSonConstantes(unittest.TestCase):
    """A check that reads its expectation out of the file it is checking is not
    a check. The published numbers are literals in the module."""

    def test_las_cifras_esperadas_estan_escritas_a_mano(self):
        self.assertEqual(
            ESPERADO,
            {"voraz test": 0.7487, "busqueda local test": 0.8472,
             "longitud de cobertura": 559, "born_at espacio": 0.3148})

    def test_el_pool_es_el_puro(self):
        """`budget_and_balance` never used the hybrid one; naming the pool is
        required of every figure (`STATUS.md`)."""
        self.assertEqual(POOL, "puro")

    def test_lo_publicado_es_de_verdad_lo_publicado(self):
        """The three-column table compares against constants. They are pinned
        against the record they claim to quote, so they cannot drift from it —
        and the record itself is only ever READ."""
        d = json.loads((REPO / "results3" / "budget_and_balance.json")
                       .read_text())
        for fila in d["label_budget"]:
            pub = PUBLICADO[round(fila["fraction"], 2)]
            with self.subTest(fraccion=fila["fraction"]):
                for k in ("labels", "test_mean", "test_sd", "test_min",
                          "test_max"):
                    self.assertEqual(pub[k], fila[k])
        for nombre, v in d["objective_comparison"].items():
            with self.subTest(objetivo=nombre):
                self.assertEqual(PUBLICADO_OBJETIVO[nombre], v)


class TestElRegistroParcialNoPisaElCompleto(unittest.TestCase):
    """Every save rewrites the whole document from the rows of THIS process, so
    a partial run landing on the canonical name would drop the section it did
    not run. `sweep_ls` nearly lost its anchors that way on 2026-08-08."""

    def test_solo_la_corrida_completa_usa_el_nombre_canonico(self):
        self.assertEqual(record_name(list(GROUPS)),
                         "budget_and_balance_ls.json")
        self.assertEqual(record_name(list(reversed(GROUPS))),
                         "budget_and_balance_ls.json")
        for parcial in (["budget"], ["balanced"]):
            with self.subTest(parcial=parcial):
                self.assertNotEqual(record_name(parcial),
                                    "budget_and_balance_ls.json")
                self.assertTrue(record_name(parcial).endswith(".json"))

    def test_cada_subconjunto_tiene_su_propio_nombre(self):
        nombres = {record_name(g) for g in (["budget"], ["balanced"],
                                            list(GROUPS))}
        self.assertEqual(len(nombres), 3)


class TestLoQueHicieronLosArranques(unittest.TestCase):
    """With the seed fixed there is no rate to estimate and, on the real
    instance, no optimum to hit. What `start_spread` records is the shape of the
    sample, which is what says whether 64 restarts are comfortable or tight."""

    def fila(self, scores, best_at):
        return {"best_score": max(scores), "best_from_index": best_at,
                "best_from": f"aleatorio {best_at}",
                "rows": [{"end_score": s} for s in scores]}

    def test_cuenta_los_que_empatan_en_el_mejor(self):
        d = start_spread(self.fila([10, 12, 12, 9, 12], 1))
        self.assertEqual(d["n_at_best"], 3)
        self.assertEqual(d["end_score_max"], 12)
        self.assertEqual(d["end_score_min"], 9)
        self.assertEqual(d["end_score_distinct"], 3)
        self.assertEqual(d["n_starts"], 5)
        self.assertEqual(d["best_from_index"], 1)

    def test_el_maximo_es_el_mejor_por_construccion(self):
        for scores in ([5], [1, 2, 3], [7, 7, 7]):
            with self.subTest(scores=scores):
                d = start_spread(self.fila(scores, 0))
                self.assertEqual(d["end_score_max"], max(scores))

    def test_un_solo_arranque_en_el_mejor_es_visible(self):
        """The case that matters: one start at the best out of 65 distinct
        values means the result rides on a single lucky shuffle."""
        d = start_spread(self.fila(list(range(65)), 64))
        self.assertEqual(d["n_at_best"], 1)
        self.assertEqual(d["end_score_distinct"], 65)


if __name__ == "__main__":
    unittest.main()
