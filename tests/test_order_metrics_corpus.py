"""
WHERE THE PER-CLASS TRUTH OF THE CORPUS SURFACES COMES FROM.

S-c and S-d are per-class figures, and a per-class figure is only as good as the
masks it divides by. There are two sources of truth in this repository and they
are in DIFFERENT BIT CONVENTIONS:

  `local_search.build_masks`          case `idxs[k]` is bit k
  `order_search_ls.space_truth_masks` case k of the exhaustive space is bit
                                      n-1-k, `Space`'s convention

`order_metrics_corpus.truth_masks` builds the first kind out of `inst["truth"]`,
the corpus label list `build_masks` is itself built against. Had the second been
used on a corpus surface, every per-class number would have been noise with the
right shape — the totals would still add up, so nothing downstream would have
complained.

The G2 census gate in that module does NOT cover this: it pins the rule masks M
by reproducing a published pair count, and the pair count never looks at a
label. So the check lives here, and it is two things:

  * the class masks PARTITION each surface actually measured — pairwise
    disjoint, union exactly `full`, bit_counts summing to n;
  * they are in `build_masks`' convention, checked by the identity
    `W[r] == M[r] & truth[action[r]]` over all 577 rules, which is the same
    check `tests/test_order_metrics_gate.py` makes of the space truth against
    the optimizer's own. A reversed convention fails it, and a test below shows
    that it does rather than assuming it.

No figure is pinned here. The class sizes live in the record and in the findings
that own them; what is pinned is the structure, which is what a second official
home for a number would not be.
"""

from __future__ import annotations

import json
import unittest
from functools import cache
from pathlib import Path

from rung3.budget_and_balance_ls import load_instance
from rung3.order_metrics_corpus import (AUTHORIZATION,
                                           COMPETITION_IS_POST_HOC, POST_HOC,
                                           RECORD, RECORD_ANNOTATIONS,
                                           S_D_CLAUSE, SETS_MEASURED,
                                           TRUTH_PROVENANCE, s_d_readings,
                                           truth_masks)
from rung3.order_metrics_run import masks_for

REPO = Path(__file__).resolve().parent.parent


@cache
def instancia():
    return load_instance()


@cache
def superficies():
    """Exactly the three corpus surfaces the run measured: all 2000 cases, and
    the test half of each of the two splits it regenerated."""
    inst = instancia()
    fuera = [("corpus_full", list(range(len(inst["corpus"]))))]
    for s in (0, 4):
        fuera.append((f"corpus_test_split{s}", inst["splits"][s][1]))
    return fuera


class TestLaVerdadPorClaseParteCadaSuperficie(unittest.TestCase):

    def test_las_clases_son_disjuntas_y_cubren_la_superficie(self):
        for nombre, idxs in superficies():
            with self.subTest(nombre):
                truth = truth_masks(instancia(), idxs)
                junto = 0
                total = 0
                for m in truth.values():
                    self.assertEqual(junto & m, 0, "dos clases comparten un caso")
                    junto |= m
                    total += m.bit_count()
                self.assertEqual(junto, (1 << len(idxs)) - 1)
                self.assertEqual(total, len(idxs))

    def test_ninguna_mascara_se_sale_de_la_superficie(self):
        """A mask from another surface — the 134,400 of the space, say — would
        carry bits above n and the totals would still look plausible."""
        for nombre, idxs in superficies():
            with self.subTest(nombre):
                for c, m in truth_masks(instancia(), idxs).items():
                    self.assertLess(m.bit_length(), len(idxs) + 1, c)

    def test_estan_todas_las_clases_del_dominio(self):
        from harness.domain import ACTIONS

        truth = truth_masks(instancia(), list(range(2000)))
        self.assertEqual(set(truth), set(ACTIONS))


class TestLaConvencionEsLaDeBuildMasks(unittest.TestCase):
    """`W[r] = M[r] & truth[action[r]]` is true by construction if and only if
    the truth is in the same convention as the masks: `build_masks` sets bit k
    of W when `action[r]` equals the label of case `idxs[k]`."""

    def test_W_es_M_interseccion_la_clase_de_la_regla(self):
        inst = instancia()
        for nombre, idxs in superficies():
            M, W, _full = masks_for(inst, idxs)
            truth = truth_masks(inst, idxs)
            with self.subTest(nombre):
                for rid in inst["ids"]:
                    self.assertEqual(W[rid], M[rid] & truth[inst["action"][rid]],
                                     f"{nombre}: {rid}")

    def test_la_convencion_contraria_no_pasaria(self):
        """The teeth of the test above: with the bits reversed — which is what
        `Space` and `space_truth_masks` use — the identity breaks."""
        inst = instancia()
        idxs = inst["splits"][0][1]
        n = len(idxs)
        M, W, _full = masks_for(inst, idxs)
        al_reves = {}
        for k, i in enumerate(idxs):
            c = inst["truth"][i]
            al_reves[c] = al_reves.get(c, 0) | (1 << (n - 1 - k))
        rotas = [rid for rid in inst["ids"]
                 if W[rid] != M[rid] & al_reves[inst["action"][rid]]]
        self.assertGreater(len(rotas), 0,
                           "la convencion contraria pasaria: la prueba de "
                           "arriba no comprueba nada")


class TestElCasoKEsElBitK(unittest.TestCase):
    """The convention itself, on three cases whose answer is written by hand."""

    def test_sobre_una_instancia_de_juguete(self):
        inst = {"truth": ["A", "B", "A", "C"]}
        self.assertEqual(truth_masks(inst, [0, 1, 2]),
                         {"A": 0b101, "B": 0b010})

    def test_los_indices_pueden_ser_un_subconjunto_cualquiera(self):
        """`idxs` is the test half, not a prefix: bit k is the k-th element of
        the list given, not case number k."""
        inst = {"truth": ["A", "B", "A", "C"]}
        self.assertEqual(truth_masks(inst, [3, 1]), {"C": 0b01, "B": 0b10})


class TestLasAnotacionesDelRegistroSonLasDelModulo(unittest.TestCase):
    """
    The record was annotated by hand after the run, with text the module holds
    as constants. Two copies of a string is exactly the drift the project
    removed figures from `README.md` and `CLAUDE.md` to avoid, and here it would
    be worse than a stale figure: these strings say what the record IS —
    where its truth comes from, what in it is post hoc, what was authorized —
    so an edit to a constant that never reached the JSON would leave the
    committed record claiming something its own module no longer says, with
    nothing to catch it.

    This is not a second home for a figure. Every value below is prose, and the
    only measured numbers involved are the two shares S-d's readings quote,
    which are read out of the record itself rather than pinned here.
    """

    @classmethod
    def setUpClass(cls):
        cls.d = json.loads((REPO / "results3" / RECORD).read_text())

    def test_las_de_primer_nivel(self):
        for clave, esperado in (("truth_provenance", TRUTH_PROVENANCE),
                                ("post_hoc", POST_HOC),
                                ("sets_measured", SETS_MEASURED),
                                ("record_annotations", RECORD_ANNOTATIONS),
                                ("authorization", AUTHORIZATION)):
            with self.subTest(clave):
                self.assertEqual(self.d[clave], esperado)

    def test_las_tres_de_dentro_de_predictions(self):
        q = self.d["predictions"]
        self.assertEqual(q["S-b"]["competition_is_post_hoc"],
                         COMPETITION_IS_POST_HOC)
        self.assertEqual(q["S-d"]["clause_verbatim"], S_D_CLAUSE)
        self.assertEqual(q["S-d"]["readings"],
                         s_d_readings(q["S-d"]["share"]["corpus_full"],
                                      q["S-d"]["share"]["corpus_test"]))

    def test_la_clausula_de_S_d_es_la_de_IDEAS_palabra_por_palabra(self):
        """The point of quoting it is that it is quoted. If `IDEAS.md` and the
        record drifted apart, the row would be adjudicated against a
        paraphrase."""
        entrada = (REPO / "IDEAS.md").read_text()
        cuerpo = S_D_CLAUSE.split("—", 1)[1].strip()
        aplanado = " ".join(entrada.replace("\n", " ").split())
        self.assertIn(" ".join(cuerpo.split()), aplanado)


if __name__ == "__main__":
    unittest.main()
