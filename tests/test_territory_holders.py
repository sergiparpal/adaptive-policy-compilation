"""
THE GATES OF `territory_holders`, AND ONLY THE GATES.

That module publishes one primitive — which rules hold territory under each of
the 65 end orders of split 0 — and a derived block that is a lookup of a figure
another record owns. **No measured value of the finding is pinned here.** How
many rules the union holds, what kappa does over it, and whether the rule at
kappa's ceiling ever decides a case live in `results3/territory_holders.json` and
in the erratum in `FINDINGS_ORDERS.md`; repeating any of them in a test would
give a figure a second owner, which is the failure this repository already
decided not to commit (`IDEAS.md`, technical debt, the test that was considered
and deliberately not written).

What is pinned instead: that `holders` reads first-match-wins the way the rest of
the thread does, that the two gates this module adds are blocking and detect the
failures they exist for, and that the derived block is the arithmetic it claims —
all on instances small enough to write the answer out by hand.
"""

from __future__ import annotations

import unittest

from peldano3.order_metrics_rules import mask_from_points
from peldano3.territory_holders import (N_ORDERS, derive, gate_counts,
                                        gate_kappa_read, holders,
                                        territory_table)

# Eight cases, four rules, `Space`'s bit convention: case i is bit n-1-i.
N = 8
FULL = (1 << N) - 1
M = {
    "A": mask_from_points([0, 1, 2, 3], N),
    "B": mask_from_points([2, 3, 4, 5], N),
    "C": mask_from_points([4, 5, 6, 7], N),
    "D": mask_from_points([0, 1, 2, 3, 4, 5, 6, 7], N),
}


class TestElPrimitivo(unittest.TestCase):

    def test_gana_territorio_quien_es_el_primero_que_empareja(self):
        """A, B and C between them cover everything, so D — last and universal —
        wins nothing at all. That is the shape of the fact being audited."""
        ids, undecided = holders(["A", "B", "C", "D"], M, FULL)
        self.assertEqual(ids, ["A", "B", "C"])
        self.assertEqual(undecided, 0)

    def test_una_regla_universal_delante_deja_a_todas_las_demas_sin_nada(self):
        ids, _u = holders(["D", "A", "B", "C"], M, FULL)
        self.assertEqual(ids, ["D"])

    def test_las_ids_salen_ordenadas(self):
        ids, _u = holders(["C", "A", "B"], M, FULL)
        self.assertEqual(ids, sorted(ids))

    def test_lo_que_nadie_empareja_cuenta_como_indeciso(self):
        parcial = {"A": M["A"]}
        ids, undecided = holders(["A"], parcial, FULL)
        self.assertEqual(ids, ["A"])
        self.assertEqual(undecided, 4)

    def test_la_tabla_lleva_una_fila_por_orden(self):
        filas = territory_table([["A", "B", "C", "D"], ["D", "A", "B", "C"]],
                                M, FULL)
        self.assertEqual([f["order"] for f in filas], [0, 1])
        self.assertEqual([f["n_rules_with_territory"] for f in filas], [3, 1])
        self.assertEqual(filas[0]["rule_ids"], ["A", "B", "C"])


class TestLaPuertaDeKappa(unittest.TestCase):
    """kappa is READ from the record that owns it; the gate is that the values
    read still reproduce the summary published beside them."""

    def _rec(self, kappa, resumen):
        return {"kappa_by_rule": kappa, "kappa_summary": resumen}

    def test_pasa_cuando_los_valores_reproducen_el_resumen(self):
        kappa = {f"R{i:04d}": float(i) for i in range(1, 9)}
        resumen = {"n": 8, "min": 1.0, "p25": 3.0, "median": 4.5, "mean": 4.5,
                   "p75": 7.0, "max": 8.0}
        leidos, g = gate_kappa_read(self._rec(kappa, resumen))
        self.assertTrue(g["passes"])
        self.assertEqual(leidos, kappa)
        self.assertEqual(g["n_rules"], 8)

    def test_falla_si_el_resumen_publicado_no_cuadra(self):
        kappa = {f"R{i:04d}": float(i) for i in range(1, 9)}
        resumen = {"n": 8, "min": 1.0, "p25": 3.0, "median": 4.5, "mean": 4.5,
                   "p75": 7.0, "max": 9.0}          # the ceiling is wrong
        _leidos, g = gate_kappa_read(self._rec(kappa, resumen))
        self.assertFalse(g["passes"])
        self.assertFalse(g["comparison"]["max"][2])

    def test_ignora_las_reglas_sin_concentracion(self):
        """A rule with an empty extension has no arrival density and the record
        stores None for it; it must not enter the summary as a zero."""
        kappa = {"R0001": 1.0, "R0002": 3.0, "R0003": None}
        leidos, _g = gate_kappa_read(self._rec(kappa, {}))
        self.assertEqual(set(leidos), {"R0001", "R0002"})


class TestLaPuertaDeLosRecuentos(unittest.TestCase):
    """The count per order against the territory gate the earlier record already
    passed: it is what says these are the same territories."""

    def _rec(self, counts):
        return {"gates": {"territories": {"per_order": [
            {"order": k, "n_rules_with_territory": n}
            for k, n in enumerate(counts)]}}}

    def _filas(self, counts):
        return [{"order": k, "n_rules_with_territory": n, "rule_ids": []}
                for k, n in enumerate(counts)]

    def test_pasa_cuando_coinciden_orden_por_orden(self):
        cuentas = [30 + (k % 7) for k in range(N_ORDERS)]
        g = gate_counts(self._filas(cuentas), self._rec(cuentas))
        self.assertTrue(g["passes"])
        self.assertEqual(g["orders_that_differ"], [])

    def test_falla_si_un_solo_orden_discrepa(self):
        cuentas = [30 + (k % 7) for k in range(N_ORDERS)]
        publicadas = list(cuentas)
        publicadas[17] += 1
        g = gate_counts(self._filas(cuentas), self._rec(publicadas))
        self.assertFalse(g["passes"])
        self.assertEqual([f["order"] for f in g["orders_that_differ"]], [17])

    def test_falla_si_faltan_ordenes(self):
        """Fewer than the 65 the set has is a different set, not a subset to be
        compared on what happens to overlap."""
        cuentas = [30] * (N_ORDERS - 1)
        g = gate_counts(self._filas(cuentas), self._rec(cuentas))
        self.assertFalse(g["passes"])

    def test_falla_si_el_registro_no_publica_ese_orden(self):
        cuentas = [30] * N_ORDERS
        rec = self._rec(cuentas[:-1])
        g = gate_counts(self._filas(cuentas), rec)
        self.assertFalse(g["passes"])


class TestElBloqueDerivado(unittest.TestCase):
    """Arithmetic on synthetic inputs. Nothing here is a figure of the
    finding."""

    KAPPA = {"A": 1.0, "B": 2.0, "C": 10.0, "Z": 40.0}

    def _filas(self):
        return [{"order": 0, "n_rules_with_territory": 2, "rule_ids": ["A", "B"]},
                {"order": 1, "n_rules_with_territory": 3,
                 "rule_ids": ["A", "B", "C"]}]

    def test_la_union_es_la_de_los_conjuntos(self):
        d = derive(self._filas(), self.KAPPA, 40.0)
        u = d["union_over_the_65_orders"]
        self.assertEqual(u["rule_ids"], ["A", "B", "C"])
        self.assertEqual(u["n_rules"], 3)
        self.assertEqual(u["n_rules_in_the_pool"], 4)
        self.assertEqual(u["fraction_of_the_pool"], 0.75)

    def test_kappa_sobre_la_union_no_ve_a_quien_no_gana_nada(self):
        d = derive(self._filas(), self.KAPPA, 40.0)
        k = d["kappa_over_the_union"]
        self.assertEqual((k["min"], k["max"]), (1.0, 10.0))
        self.assertEqual((k["min_rule"], k["max_rule"]), ("A", "C"))
        self.assertEqual(k["n"], 3)

    def test_el_rango_dentro_de_un_orden_es_max_sobre_min(self):
        d = derive(self._filas(), self.KAPPA, 40.0)
        r = d["kappa_range_within_an_order"]
        self.assertEqual([v["range"] for v in r["per_order"]], [2.0, 10.0])
        self.assertEqual((r["min"], r["max"]), (2.0, 10.0))

    def test_el_tope_de_kappa_puede_no_ganar_nada(self):
        d = derive(self._filas(), self.KAPPA, 40.0)
        a = d["argmax_kappa_holds_territory"]
        self.assertEqual(a["rule_id"], "Z")
        self.assertTrue(a["matches_published_max"])
        self.assertFalse(a["holds_territory"])
        self.assertEqual(a["n_orders_where_it_holds"], 0)

    def test_y_puede_ganar_algo(self):
        """The other branch, so the boolean is measured and not assumed."""
        filas = self._filas() + [{"order": 2, "n_rules_with_territory": 1,
                                  "rule_ids": ["Z"]}]
        a = derive(filas, self.KAPPA, 40.0)["argmax_kappa_holds_territory"]
        self.assertTrue(a["holds_territory"])
        self.assertEqual(a["orders_where_it_holds"], [2])

    def test_avisa_si_el_tope_no_es_el_maximo_publicado(self):
        a = derive(self._filas(), self.KAPPA, 9.99)[
            "argmax_kappa_holds_territory"]
        self.assertFalse(a["matches_published_max"])

    def test_un_orden_de_una_sola_regla_tiene_rango_uno(self):
        filas = [{"order": 0, "n_rules_with_territory": 1, "rule_ids": ["C"]}]
        r = derive(filas, self.KAPPA, 40.0)["kappa_range_within_an_order"]
        self.assertEqual(r["per_order"][0]["range"], 1.0)


if __name__ == "__main__":
    unittest.main()
