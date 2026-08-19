"""
The pieces of the P4 runner that something else rests on.

Not the figures: those live in `results3/order_metrics.json` and in the findings
that own them, and pinning them here would create a second official home for a
number, which is the mistake `tests/test_local_search.py` and
`tests/test_order_metrics.py` both decline to make.

What is pinned is the arithmetic the run cannot be wrong about:

  * `prefix_winner` reproduces `multistart`'s tie-break — strictly greater wins,
    so a tie goes to the lowest index. Three published figures are read off a
    prefix, and if this drifted they would silently become a different order's;
  * `spearman` is a rank correlation and not something that merely resembles
    one, ties included, because the whole of Q-d is one number it returns;
  * a behavioural signature's digest changes when the behaviour changes, which
    is what makes counting distinct digests a count of distinct machines.
"""

from __future__ import annotations

import unittest

from rung3.order_metrics import signature
from rung3.order_metrics_run import (digest, prefix_winner, resumen,
                                        slice_pairs, spearman)


def filas(puntuaciones):
    return [{"index": k, "end_score": s, "order": [f"R{k:03d}"]}
            for k, s in enumerate(puntuaciones)]


class TestElGanadorDeUnPrefijo(unittest.TestCase):

    def test_gana_la_mejor_puntuacion(self):
        f = filas([3, 9, 5])
        self.assertEqual(prefix_winner(f, 3)["index"], 1)

    def test_un_empate_va_al_indice_mas_bajo(self):
        """`multistart` applies `if st["end"] > best_score`, so the first of an
        equal pair keeps the crown. The prefix has to agree or the winner it
        reports is not the winner the record reports."""
        f = filas([7, 7, 7])
        self.assertEqual(prefix_winner(f, 3)["index"], 0)

    def test_solo_mira_el_prefijo_pedido(self):
        """The point of the shortcut: a better order further down the 257 rows
        must not leak into the 65-start answer."""
        f = filas([4, 6, 99])
        self.assertEqual(prefix_winner(f, 2)["index"], 1)
        self.assertEqual(prefix_winner(f, 3)["index"], 2)

    def test_un_prefijo_de_uno_es_el_voraz(self):
        f = filas([2, 100])
        self.assertEqual(prefix_winner(f, 1)["index"], 0)


class TestElRecorteDeLaMatriz(unittest.TestCase):

    def test_se_queda_con_los_pares_de_los_primeros_k(self):
        pares = [{"i": 0, "j": 1}, {"i": 0, "j": 5}, {"i": 2, "j": 3},
                 {"i": 4, "j": 6}]
        self.assertEqual(slice_pairs(pares, 4), [{"i": 0, "j": 1},
                                                 {"i": 2, "j": 3}])
        self.assertEqual(len(slice_pairs(pares, 7)), 4)
        self.assertEqual(slice_pairs(pares, 1), [])


class TestSpearman(unittest.TestCase):

    def test_monotona_creciente_es_uno_y_decreciente_menos_uno(self):
        xs = [1, 2, 3, 4, 5]
        self.assertEqual(spearman(xs, [10, 20, 30, 40, 50]), 1.0)
        self.assertEqual(spearman(xs, [50, 40, 30, 20, 10]), -1.0)

    def test_no_depende_de_la_escala_solo_del_orden(self):
        xs = [1, 2, 3, 4]
        self.assertEqual(spearman(xs, [1, 100, 1000, 10000]),
                         spearman(xs, [1, 2, 3, 4]))

    def test_los_empates_reparten_el_rango(self):
        """Average ranks, computed by hand: x ranks 1,2.5,2.5,4 against y ranks
        1,2,3,4 give 0.9487."""
        self.assertAlmostEqual(spearman([1, 2, 2, 3], [1, 2, 3, 4]),
                               0.9487, places=4)

    def test_sin_variacion_no_hay_correlacion(self):
        self.assertIsNone(spearman([5, 5, 5], [1, 2, 3]))

    def test_con_menos_de_dos_puntos_devuelve_nada(self):
        self.assertIsNone(spearman([1], [2]))


class TestElDigestoDeUnaFirma(unittest.TestCase):

    def test_la_misma_conducta_da_el_mismo_nombre(self):
        a = signature({"A": 0b1010, "B": 0b0101}, 0)
        b = signature({"B": 0b0101, "A": 0b1010}, 0)
        self.assertEqual(digest(a), digest(b))

    def test_una_conducta_distinta_da_otro(self):
        a = signature({"A": 0b1010, "B": 0b0101}, 0)
        b = signature({"A": 0b1011, "B": 0b0100}, 0)
        self.assertNotEqual(digest(a), digest(b))

    def test_distingue_quien_deja_casos_sin_decidir(self):
        a = signature({"A": 0b0010}, 0b1000)
        b = signature({"A": 0b0010}, 0)
        self.assertNotEqual(digest(a), digest(b))

    def test_no_confunde_la_accion_con_la_mascara(self):
        a = signature({"A": 0b1100, "B": 0b0011}, 0)
        b = signature({"A": 0b0011, "B": 0b1100}, 0)
        self.assertNotEqual(digest(a), digest(b))


class TestElResumen(unittest.TestCase):

    def test_da_los_cuantiles_declarados(self):
        r = resumen([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual((r["n"], r["min"], r["max"]), (8, 1, 8))
        self.assertEqual(r["median"], 4.5)
        self.assertEqual((r["p25"], r["p75"]), (3, 7))

    def test_no_le_importa_el_orden_de_entrada(self):
        self.assertEqual(resumen([3, 1, 2]), resumen([1, 2, 3]))

    def test_vacio_es_nada(self):
        self.assertIsNone(resumen([]))


if __name__ == "__main__":
    unittest.main()
