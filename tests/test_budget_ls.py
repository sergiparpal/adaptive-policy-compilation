"""
The harness of step 3 of the audit (`peldano3.budget_and_balance_ls`).

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
import random
import unittest
from pathlib import Path

from peldano3.budget_and_balance import FRACTIONS, N_DRAWS, N_SPLITS
from peldano3.budget_and_balance_ls import ESPERADO, POOL, subsample

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
    """`peldano3.budget_and_balance` has no guard and dumps over its own record
    on finishing. Step 3 obtains greedy-today by importing the function, never
    by running the script."""

    FUENTE = REPO / "peldano3" / "budget_and_balance_ls.py"

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


if __name__ == "__main__":
    unittest.main()
