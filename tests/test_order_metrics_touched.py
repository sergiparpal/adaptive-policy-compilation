"""
THE MASK THAT CARRIES THE CORPUS ONTO THE SPACE, AND THE CONVENTION IT IS IN.

`order_metrics_touched` measures `touched(c)` — a per-class rate over the points
of the exhaustive space the corpus actually reaches. Everything it computes is
in `Space`'s bit convention, case k at bit n-1-k; the corpus contributes exactly
one object, the mask of the points its 2,000 draws land on. That mask is the
single place where something built from the corpus meets something built from
the space, and if it were built in the OTHER convention — `build_masks`' case
`idxs[k]` at bit k — every per-class number would be noise with the right shape:
a mask of 1,743 bits either way, and class masks that partition it either way,
because intersecting a partition with any mask gives a partition of that mask.

**So partitioning does not catch the reversed convention, and the run's own gate
does not either.** What catches it is a count that has to come out the same by
two independent routes:

    (truth_space[c] & touched).bit_count()
        ==  the number of DISTINCT corpus cases whose label is c

the left side from the oracle's labelling of the 134,400 space points, the right
side from `inst["truth"]`, the corpus label list, and the corpus keys. Both are
the same oracle, so on the correct convention they agree class by class; under
the reversed one they do not, and a test below shows that rather than assuming
it.

The rest of what is pinned is the adjudication rule: that the bands and
refutation lines in `adjudicate` are the ones `IDEAS.md` wrote, checked at their
boundaries. No measured figure is pinned here — `f(T2_TECHNICAL)`, the
reconstruction and the ratios live in the record and in the findings that own
them, and a second official home for a number is exactly what this file must not
become.
"""

from __future__ import annotations

import unittest
from collections import Counter
from functools import cache

from harness.ceiling_check import all_cases
from rung2.engine2 import Space
from rung3.budget_and_balance_ls import load_instance
from rung3.order_metrics_touched import (CLASE_C_A, TOUCHED_PUBLISHED,
                                            adjudicate, partitions,
                                            ratio_summary, restrict, signo,
                                            touched_mask)
from rung3.order_search_ls import space_truth_masks


@cache
def espacio():
    return Space()


@cache
def instancia():
    return load_instance()


@cache
def mascara():
    return touched_mask(instancia()["corpus"], espacio())


@cache
def verdad():
    return space_truth_masks(espacio())


class TestLaMascaraDePuntosTocados(unittest.TestCase):

    def test_tiene_los_bits_que_el_registro_publica(self):
        """1,743 distinct cases: a fact about the corpus and the domain, and the
        one published figure that pins this mask."""
        m, censo = mascara()
        self.assertEqual(m.bit_count(), TOUCHED_PUBLISHED)
        self.assertEqual(censo["n_distinct_points"], TOUCHED_PUBLISHED)

    def test_el_censo_cuadra_con_el_corpus(self):
        _m, censo = mascara()
        inst = instancia()
        self.assertEqual(censo["n_corpus_draws"], len(inst["corpus"]))
        self.assertEqual(censo["n_space"], espacio().n)
        self.assertEqual(
            sum(int(k) * v
                for k, v in censo["points_by_multiplicity"].items()),
            len(inst["corpus"]))
        self.assertEqual(sum(censo["points_by_multiplicity"].values()),
                         censo["n_distinct_points"])

    def test_esta_dentro_del_espacio(self):
        m, _c = mascara()
        self.assertEqual(m & ~espacio().full, 0)

    def test_un_caso_fuera_del_espacio_revienta_en_vez_de_caer(self):
        """A corpus case the enumeration does not contain would be a broken
        domain, and dropping it silently would shrink the denominator."""
        class Falso:
            def key(self):
                return ("no", "such", "case")

        with self.assertRaises(ValueError):
            touched_mask([Falso()], espacio())

    def test_cada_caso_del_corpus_pone_su_bit_en_la_convencion_de_Space(self):
        """Bit n-1-i for case i of `all_cases()`, which is what `Space` builds
        and therefore what every space mask in the repository is in."""
        m, _c = mascara()
        indice = {c.key(): i for i, c in enumerate(all_cases())}
        n = espacio().n
        for caso in instancia()["corpus"][:50]:
            i = indice[caso.key()]
            self.assertTrue(m >> (n - 1 - i) & 1)


class TestLaConvencionSeComprueba(unittest.TestCase):
    """The check the partition cannot make."""

    def _distintos_por_clase(self):
        """Distinct corpus cases by label, from the corpus side alone: no mask,
        no space."""
        inst = instancia()
        vistos = {}
        for i, caso in enumerate(inst["corpus"]):
            vistos.setdefault(inst["truth"][i], set()).add(caso.key())
        return {c: len(v) for c, v in vistos.items()}

    def test_los_tamanos_por_clase_coinciden_por_dos_rutas(self):
        m, _c = mascara()
        esperado = self._distintos_por_clase()
        for c, mask in verdad().items():
            with self.subTest(c):
                self.assertEqual((mask & m).bit_count(), esperado.get(c, 0))

    def test_la_convencion_invertida_falla_esa_comprobacion(self):
        """Shown, not assumed: the reversed mask has the same 1,743 bits and
        still partitions, and the class sizes are what tells it apart."""
        inst = instancia()
        n = espacio().n
        indice = {c.key(): i for i, c in enumerate(all_cases())}
        al_reves = 0
        for i in {indice[c.key()] for c in inst["corpus"]}:
            al_reves |= 1 << i

        self.assertEqual(al_reves.bit_count(), TOUCHED_PUBLISHED)
        self.assertTrue(partitions(restrict(verdad(), al_reves), al_reves))

        esperado = self._distintos_por_clase()
        iguales = sum(1 for c, mask in verdad().items()
                      if (mask & al_reves).bit_count() == esperado.get(c, 0))
        self.assertLess(iguales, len(verdad()))
        self.assertNotEqual(al_reves, mascara()[0])
        # and n-1-i is not i for any case here, so the two masks are never the
        # same object by accident
        self.assertGreater(n, 1)


class TestLasMascarasDeClaseParten(unittest.TestCase):

    def test_parten_el_espacio(self):
        self.assertTrue(partitions(verdad(), espacio().full))

    def test_parten_la_mascara_de_tocados(self):
        m, _c = mascara()
        self.assertTrue(partitions(restrict(verdad(), m), m))

    def test_restrict_no_saca_bits_de_la_mascara(self):
        m, _c = mascara()
        for c, mask in restrict(verdad(), m).items():
            with self.subTest(c):
                self.assertEqual(mask & ~m, 0)

    def test_partitions_rechaza_solape_y_hueco(self):
        self.assertTrue(partitions({"a": 0b1100, "b": 0b0011}, 0b1111))
        self.assertFalse(partitions({"a": 0b1100, "b": 0b0111}, 0b1111))
        self.assertFalse(partitions({"a": 0b1000, "b": 0b0011}, 0b1111))


class TestElSignoYLasRazones(unittest.TestCase):

    def test_signo_distingue_el_cero(self):
        self.assertEqual((signo(-2), signo(0), signo(0.5)), (-1, 0, 1))

    def test_ratio_summary_descarta_denominador_cero(self):
        pares = [{"a": 1.0, "b": 2.0}, {"a": 3.0, "b": 0.0},
                 {"a": 1.0, "b": 4.0}]
        r = ratio_summary(pares, "a", "b")
        self.assertEqual(r["n"], 2)
        self.assertEqual(r["n_dropped_zero_denominator"], 1)
        self.assertEqual(r["resumen"]["min"], 0.25)
        self.assertEqual(r["resumen"]["max"], 0.5)


class TestLaReglaDeAdjudicacion(unittest.TestCase):
    """The bands and refutation lines of `IDEAS.md`, at their boundaries. No
    measured value is pinned; what is pinned is that the code reads the rows the
    way they are written."""

    CLASES = ("ACCOUNT_MANAGER", "BILLING_SPECIALIST", "ONCALL_ESCALATION",
              "SECURITY_INCIDENT", "SELF_SERVICE_DEFLECT", "T1_GENERAL",
              "T2_TECHNICAL", "T3_ENGINEERING")

    def _tasas(self, f_objetivo):
        """Eight classes whose `f` is `f_objetivo`."""
        return {c: {"all": 1.0, "arrivals": 0.0, "touched": 1.0 - f_objetivo}
                for c in self.CLASES}

    def _q(self, f_objetivo=0.8, tasas=None):
        tasas = self._tasas(f_objetivo) if tasas is None else tasas
        p = {c: 1 / len(tasas) for c in tasas}
        razones = {"touched_over_space": ratio_summary(
            [{"a": 1.0, "b": 2.0}], "a", "b")}
        return adjudicate(tasas, p, razones)

    def test_C_a_en_la_banda_y_en_sus_bordes(self):
        for f in (0.60, 0.75, 0.95):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "HOLDS", f)

    def test_C_a_en_la_zona_muerta(self):
        for f in (0.40, 0.599, 0.951, 1.10):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "NEITHER", f)

    def test_C_a_refutada_fuera(self):
        for f in (0.399, 1.101, -0.2, 2.0):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "REFUTED", f)

    def test_C_a_admite_f_fuera_de_cero_uno(self):
        """The row says so explicitly: f outside [0, 1] is a result, not an
        error."""
        q = self._q(1.05)
        self.assertEqual(q["C-a"]["f"], 1.05)
        self.assertEqual(len(q["C-a"]["f_outside_unit_interval"]), 8)

    def test_C_b_cuenta_los_signos(self):
        """Both go down together = a match; touched up while arrivals down = a
        mismatch. C-b counts classes and nothing else, so this is independent of
        C-a's f."""
        igual = {"all": 0.2, "touched": 0.1, "arrivals": 0.05}
        distinto = {"all": 0.2, "touched": 0.3, "arrivals": 0.05}
        for n_ok, esperado in ((8, "HOLDS"), (6, "HOLDS"), (5, "NEITHER"),
                               (4, "REFUTED"), (0, "REFUTED")):
            tasas = {c: dict(igual if k < n_ok else distinto)
                     for k, c in enumerate(self.CLASES)}
            with self.subTest(n_ok):
                q = self._q(tasas=tasas)
                self.assertEqual(q["C-b"]["n_matching"], n_ok)
                self.assertEqual(q["C-b"]["verdict"], esperado)

    def test_C_b_ve_el_signo_cero_como_su_propio_caso(self):
        """`touched == all` matches only if `arrivals == all` too: a rate that
        does not move is not the same event as one that moves the other way."""
        quieto = {"all": 0.2, "touched": 0.2, "arrivals": 0.05}
        q = self._q(tasas={c: dict(quieto) for c in self.CLASES})
        self.assertEqual(q["C-b"]["n_matching"], 0)
        self.assertEqual(q["C-b"]["by_class"][CLASE_C_A]["sign_touched"], 0)
        self.assertEqual(q["C-b"]["by_class"][CLASE_C_A]["sign_arrivals"], -1)

    def test_C_c_en_su_banda_y_fuera(self):
        for valor, esperado in ((0.043, "HOLDS"), (0.0575, "HOLDS"),
                                (0.072, "HOLDS"), (0.035, "NEITHER"),
                                (0.090, "NEITHER"), (0.0349, "REFUTED"),
                                (0.0901, "REFUTED")):
            tasas = {c: {"all": 0.2, "touched": valor, "arrivals": 0.05}
                     for c in self.CLASES}
            with self.subTest(valor):
                q = self._q(0.0, tasas=tasas)
                self.assertEqual(q["C-c"]["value"], valor)
                self.assertEqual(q["C-c"]["verdict"], esperado)

    def test_C_d_no_adjudica(self):
        q = self._q(0.8)
        self.assertFalse(q["C-d"]["adjudicates"])
        self.assertNotIn("verdict", q["C-d"])


if __name__ == "__main__":
    unittest.main()
