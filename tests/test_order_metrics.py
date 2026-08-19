"""
Tests for the instrument that compares orders instead of scores.

The instrument exists to say that two orders scoring alike are or are not the
same machine. An instrument with a bug would answer that in whichever direction
its bug points, and — unlike an accuracy figure — nobody has an intuition for
what a behavioural distance "should" be, so nothing downstream would catch it.
So what is pinned here is not a number from the real instance: it is that the
answers are right on instances whose answer is written out by hand, and that the
fast path reproduces a naive case-by-case walk that knows nothing about masks.

NO figure from the 577 rules is pinned here, for the reason
`tests/test_local_search.py` states: the findings that own those figures do not
exist yet, and a test carrying them would create a second official home for a
number. The gate over the 29 hidden rules, whose answers ARE known by
construction, is `tests/test_order_metrics_gate.py`.
"""

from __future__ import annotations

import ast
import math
import random
import unittest
from itertools import combinations
from pathlib import Path

from rung3.order_metrics import (agreement_masks, attribution_agreement,
                                    behavioural_distance, conflicting_pairs,
                                    decisions, pair_census,
                                    per_class_disagreement, positions_moved,
                                    signature, tau, winners)

REPO = Path(__file__).resolve().parent.parent
ACCIONES = ("A", "B", "C")


def mascara(casos):
    """A mask from case indices, which is how every expectation below is
    written: the bit convention is the one `build_masks` uses."""
    m = 0
    for i in casos:
        m |= 1 << i
    return m


def instancia(n_reglas, n_casos, seed, p_match=0.35):
    """A random synthetic instance, with the pool kept so that the naive
    reference can be written without touching a mask."""
    rng = random.Random(seed)
    ids = [f"X{k:03d}" for k in range(n_reglas)]
    action = {rid: rng.choice(ACCIONES) for rid in ids}
    pool = [[rid for rid in ids if rng.random() < p_match]
            for _ in range(n_casos)]
    M = {rid: 0 for rid in ids}
    for i, casan in enumerate(pool):
        for rid in casan:
            M[rid] |= 1 << i
    return ids, pool, action, M, (1 << n_casos) - 1


def decide_ingenuo(order, pool, action):
    """First-match-wins, case by case, the obvious way: what each case is
    decided to be, or None if no rule matched it."""
    rank = {rid: k for k, rid in enumerate(order)}
    return [action[min(p, key=lambda rid: rank[rid])] if p else None
            for p in pool]


def orden_aleatorio(ids, seed):
    o = sorted(ids)
    random.Random(seed).shuffle(o)
    return o


# ---------------------------------------------------------------------------
# The three-rule instance, with its decision table written out by hand
# ---------------------------------------------------------------------------
#
#            case 0    case 1    case 2    case 3
#   R0 (A)     x         x
#   R1 (B)               x         x
#   R2 (A)                         x         x
#
# In R0 R1 R2:  case 1 goes to R0 (A) and case 2 to R1 (B).
# In R1 R0 R2:  case 1 goes to R1 (B) and case 2 to R1 (B).
# One case changes hands, and it is case 1. Everything below is that table.

def tres_reglas(n_casos=4):
    ids = ["R0", "R1", "R2"]
    action = {"R0": "A", "R1": "B", "R2": "A"}
    M = {"R0": mascara([0, 1]), "R1": mascara([1, 2]), "R2": mascara([2, 3])}
    return ids, M, action, mascara(range(n_casos))


class TestLaTablaEscritaAMano(unittest.TestCase):

    def test_el_orden_de_diseno_decide_lo_que_dice_la_tabla(self):
        ids, M, action, full = tres_reglas()
        d, undecided = decisions(ids, M, action, full)
        self.assertEqual(d, {"A": mascara([0, 1, 3]), "B": mascara([2])})
        self.assertEqual(undecided, 0)

    def test_adelantar_R1_le_quita_el_caso_1_a_R0(self):
        ids, M, action, full = tres_reglas()
        d, undecided = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(d, {"A": mascara([0, 3]), "B": mascara([1, 2])})
        self.assertEqual(undecided, 0)

    def test_la_distancia_entre_esos_dos_es_exactamente_el_caso_1(self):
        ids, M, action, full = tres_reglas()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 0))
        _agree, dis, _und = agreement_masks(dA, dB, full)
        self.assertEqual(dis, mascara([1]))

    def test_mover_R2_al_frente_no_cambia_nada(self):
        """R2 and R0 share no case and R2 only outranks R1 on case 2, which R1
        would have taken — so this is a real reordering with no decision behind
        it, on the smallest instance where that can happen."""
        ids, M, action, full = tres_reglas()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R0", "R2", "R1"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 0))
        _a, dis, _u = agreement_masks(dA, dB, full)
        self.assertEqual(dis, mascara([2]))

    def test_las_clases_por_verdad_se_cuentan_donde_toca(self):
        """`truth` is by class, and a class the two orders never disagree on
        must come back at rate 0 rather than absent."""
        ids, M, action, full = tres_reglas()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        # cases 0 and 1 are truly A, cases 2 and 3 truly B
        truth = {"A": mascara([0, 1]), "B": mascara([2, 3])}
        por_clase = per_class_disagreement(dA, dB, truth)
        self.assertEqual(por_clase["A"], {"n": 2, "disagree": 1, "rate": 0.5,
                                          "undecided_either": 0})
        self.assertEqual(por_clase["B"], {"n": 2, "disagree": 0, "rate": 0.0,
                                          "undecided_either": 0})


class TestLoQueNadieCasa(unittest.TestCase):
    """The undecided branch: 'no rule matched' is not a disagreement, and the
    two are not to be averaged together."""

    def test_un_caso_sin_regla_queda_sin_decidir(self):
        ids, M, action, full = tres_reglas(n_casos=5)     # case 4 matches nothing
        d, undecided = decisions(ids, M, action, full)
        self.assertEqual(undecided, mascara([4]))
        self.assertEqual(d, {"A": mascara([0, 1, 3]), "B": mascara([2])})

    def test_no_cuenta_como_desacuerdo_ni_como_acuerdo(self):
        ids, M, action, full = tres_reglas(n_casos=5)
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 1))

    def test_un_orden_vacio_lo_deja_todo_sin_decidir(self):
        _ids, M, action, full = tres_reglas()
        d, undecided = decisions([], M, action, full)
        self.assertEqual((d, undecided), ({}, full))
        self.assertEqual(behavioural_distance(d, d, full), (0, 0, 4))

    def test_las_tres_cantidades_parten_el_espacio(self):
        """The invariant that makes the triple readable: nothing is counted
        twice and nothing is lost."""
        for seed in range(10):
            ids, pool, action, M, full = instancia(9, 40, seed, p_match=0.2)
            dA, _ = decisions(orden_aleatorio(ids, seed), M, action, full)
            dB, _ = decisions(orden_aleatorio(ids, 100 + seed), M, action, full)
            with self.subTest(seed=seed):
                self.assertEqual(sum(behavioural_distance(dA, dB, full)), 40)
                masks = agreement_masks(dA, dB, full)
                self.assertEqual(masks[0] | masks[1] | masks[2], full)
                self.assertEqual(masks[0] & masks[1], 0)
                self.assertEqual(masks[0] & masks[2], 0)
                self.assertEqual(masks[1] & masks[2], 0)


class TestContraElRecorridoIngenuo(unittest.TestCase):
    """The bitmask sweep against a walk that reads the pool case by case and
    knows nothing about masks."""

    def test_decisions_reproduce_el_recorrido_caso_a_caso(self):
        for seed in range(12):
            ids, pool, action, M, full = instancia(10, 50, seed)
            order = orden_aleatorio(ids, seed)
            esperado = decide_ingenuo(order, pool, action)
            d, undecided = decisions(order, M, action, full)
            with self.subTest(seed=seed):
                for a in ACCIONES:
                    self.assertEqual(
                        d.get(a, 0),
                        mascara([i for i, v in enumerate(esperado) if v == a]))
                self.assertEqual(
                    undecided,
                    mascara([i for i, v in enumerate(esperado) if v is None]))

    def test_la_distancia_reproduce_la_comparacion_caso_a_caso(self):
        for seed in range(12):
            ids, pool, action, M, full = instancia(10, 50, seed)
            a = orden_aleatorio(ids, seed)
            b = orden_aleatorio(ids, 500 + seed)
            va, vb = decide_ingenuo(a, pool, action), decide_ingenuo(b, pool, action)
            esperado = (
                sum(1 for x, y in zip(va, vb) if x is not None and x == y),
                sum(1 for x, y in zip(va, vb)
                    if x is not None and y is not None and x != y),
                sum(1 for x, y in zip(va, vb) if x is None or y is None),
            )
            dA, _ = decisions(a, M, action, full)
            dB, _ = decisions(b, M, action, full)
            with self.subTest(seed=seed):
                self.assertEqual(behavioural_distance(dA, dB, full), esperado)


class TestIdentidadYSimetria(unittest.TestCase):

    def test_un_orden_no_se_diferencia_de_si_mismo(self):
        for seed in range(10):
            ids, _pool, action, M, full = instancia(9, 40, seed)
            d, und = decisions(orden_aleatorio(ids, seed), M, action, full)
            agree, dis, undecided = behavioural_distance(d, d, full)
            with self.subTest(seed=seed):
                self.assertEqual(dis, 0)
                self.assertEqual(undecided, und.bit_count())
                self.assertEqual(agree + undecided, 40)

    def test_la_distancia_es_simetrica(self):
        for seed in range(10):
            ids, _pool, action, M, full = instancia(9, 40, seed)
            dA, _ = decisions(orden_aleatorio(ids, seed), M, action, full)
            dB, _ = decisions(orden_aleatorio(ids, 900 + seed), M, action, full)
            with self.subTest(seed=seed):
                self.assertEqual(behavioural_distance(dA, dB, full),
                                 behavioural_distance(dB, dA, full))


# ---------------------------------------------------------------------------
# The motivating property
# ---------------------------------------------------------------------------
#
# Six rules over eight cases. Only ONE pair can change a decision: R0 and R2
# both match case 7 and prescribe different actions. R0/R1 and R2/R3 co-match
# too, with the same action, so they are free; R4 and R5 share nothing with
# anyone.
#
#          0  1  2  3  4  5  6  7
#  R0 (A)  x  x                 x
#  R1 (A)     x  x
#  R2 (B)           x           x
#  R3 (B)           x  x
#  R4 (C)                 x
#  R5 (C)                    x

def instancia_de_un_solo_conflicto():
    ids = ["R0", "R1", "R2", "R3", "R4", "R5"]
    action = {"R0": "A", "R1": "A", "R2": "B", "R3": "B", "R4": "C", "R5": "C"}
    M = {"R0": mascara([0, 1, 7]), "R1": mascara([1, 2]),
         "R2": mascara([3, 7]), "R3": mascara([3, 4]),
         "R4": mascara([5]), "R5": mascara([6])}
    return ids, M, action, mascara(range(8))


class TestLaPropiedadQueMotivaElInstrumento(unittest.TestCase):
    """Two orders differing only in non-conflicting pairs are the same machine,
    however far apart they look positionally. It is the whole argument for
    measuring behaviour instead of rank, and P3 pins it again on the 29 hidden
    rules, where the pairs are not hand-picked."""

    def test_solo_un_par_puede_cambiar_una_decision(self):
        ids, M, action, _full = instancia_de_un_solo_conflicto()
        self.assertEqual(conflicting_pairs(ids, M, action), {("R0", "R2")})
        self.assertEqual(pair_census(ids, M, action),
                         {"pairs": 15, "co_match": 3, "conflicting": 1,
                          "same_action": 2})

    def test_permutar_solo_pares_libres_deja_la_maquina_intacta(self):
        ids, M, action, full = instancia_de_un_solo_conflicto()
        otro = ["R1", "R0", "R3", "R2", "R5", "R4"]     # R0 sigue antes que R2
        dA, uA = decisions(ids, M, action, full)
        dB, uB = decisions(otro, M, action, full)

        self.assertEqual(behavioural_distance(dA, dB, full)[1], 0)
        self.assertEqual(signature(dA, uA), signature(dB, uB))

        churn = positions_moved(ids, otro)
        self.assertEqual(churn["moved"], 6)             # every rule moved
        self.assertEqual(churn["fraction_moved"], 1.0)

        pares = conflicting_pairs(ids, M, action)
        self.assertLess(tau(ids, otro), 1.0)            # rank says they differ
        self.assertEqual(tau(ids, otro, pares), 1.0)    # restricted says they do not

    def test_invertir_el_par_en_conflicto_si_cambia_una_decision(self):
        """The control: the same instance, the one pair that is not free."""
        ids, M, action, full = instancia_de_un_solo_conflicto()
        otro = ["R2", "R1", "R0", "R3", "R4", "R5"]
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(otro, M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (7, 1, 0))
        self.assertEqual(tau(ids, otro, conflicting_pairs(ids, M, action)), -1.0)


class TestParesEnConflicto(unittest.TestCase):

    def test_iguala_al_doble_bucle_sobre_el_pool(self):
        """Brute force from the pool, which never looks at a mask: a pair
        conflicts when some case lists both and the actions differ."""
        for seed in range(10):
            ids, pool, action, M, _full = instancia(12, 60, seed)
            bruto = set()
            for a, b in combinations(sorted(ids), 2):
                if action[a] == action[b]:
                    continue
                if any(a in p and b in p for p in pool):
                    bruto.add((a, b))
            with self.subTest(seed=seed):
                self.assertEqual(conflicting_pairs(ids, M, action), bruto)

    def test_el_censo_cuadra_con_el_conjunto(self):
        for seed in range(8):
            ids, _pool, action, M, _full = instancia(11, 50, seed)
            censo = pair_census(ids, M, action)
            with self.subTest(seed=seed):
                self.assertEqual(censo["conflicting"],
                                 len(conflicting_pairs(ids, M, action)))
                self.assertEqual(censo["co_match"],
                                 censo["conflicting"] + censo["same_action"])
                self.assertLessEqual(censo["co_match"], censo["pairs"])
                self.assertEqual(censo["pairs"], 11 * 10 // 2)

    def test_una_misma_accion_nunca_esta_en_conflicto(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "A"}
        M = {"R0": mascara([0, 1]), "R1": mascara([0, 1])}
        self.assertEqual(conflicting_pairs(ids, M, action), set())

    def test_sin_casos_en_comun_tampoco(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "B"}
        M = {"R0": mascara([0]), "R1": mascara([1])}
        self.assertEqual(conflicting_pairs(ids, M, action), set())


class TestTau(unittest.TestCase):

    @staticmethod
    def tau_ingenuo(a, b, pares=None):
        ra = {x: k for k, x in enumerate(a)}
        rb = {x: k for k, x in enumerate(b)}
        pares = list(combinations(a, 2)) if pares is None else list(pares)
        con = sum(1 for x, y in pares if (ra[x] < ra[y]) == (rb[x] < rb[y]))
        return (con - (len(pares) - con)) / len(pares)

    def test_iguala_a_la_fuerza_bruta_sobre_todos_los_pares(self):
        for seed in range(20):
            ids = [f"X{k:03d}" for k in range(8)]
            a = orden_aleatorio(ids, seed)
            b = orden_aleatorio(ids, 300 + seed)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(tau(a, b), self.tau_ingenuo(a, b))

    def test_iguala_a_la_fuerza_bruta_sobre_un_conjunto_dado(self):
        rng = random.Random(7)
        for seed in range(20):
            ids = [f"X{k:03d}" for k in range(8)]
            a = orden_aleatorio(ids, seed)
            b = orden_aleatorio(ids, 400 + seed)
            todos = list(combinations(sorted(ids), 2))
            pares = set(rng.sample(todos, rng.randint(1, len(todos))))
            with self.subTest(seed=seed):
                self.assertAlmostEqual(tau(a, b, pares),
                                       self.tau_ingenuo(a, b, pares))

    def test_consigo_mismo_es_uno_y_con_el_inverso_menos_uno(self):
        ids = [f"X{k:03d}" for k in range(8)]
        self.assertEqual(tau(ids, ids), 1.0)
        self.assertEqual(tau(ids, list(reversed(ids))), -1.0)

    def test_el_orden_del_par_no_importa(self):
        ids = [f"X{k:03d}" for k in range(8)]
        a, b = orden_aleatorio(ids, 1), orden_aleatorio(ids, 2)
        pares = {("X000", "X003"), ("X002", "X005")}
        self.assertEqual(tau(a, b, pares),
                         tau(a, b, {(y, x) for x, y in pares}))

    def test_sin_pares_que_correlacionar_devuelve_nan(self):
        self.assertTrue(math.isnan(tau(["R0"], ["R0"])))
        self.assertTrue(math.isnan(tau([], [])))
        self.assertTrue(math.isnan(tau(["R0", "R1"], ["R1", "R0"], set())))

    def test_exige_dos_permutaciones_del_mismo_conjunto(self):
        with self.assertRaises(ValueError):
            tau(["R0", "R1"], ["R0", "R2"])
        with self.assertRaises(ValueError):
            tau(["R0", "R1", "R1"], ["R1", "R0", "R1"])


class TestPosicionesMovidas(unittest.TestCase):

    def test_consigo_mismo_no_mueve_nada(self):
        ids = [f"X{k:03d}" for k in range(6)]
        m = positions_moved(ids, ids)
        self.assertEqual((m["moved"], m["max"], m["total"]), (0, 0, 0))
        self.assertEqual(m["fraction_moved"], 0.0)

    def test_el_inverso_mueve_todo_menos_el_centro(self):
        ids = [f"X{k:03d}" for k in range(5)]
        m = positions_moved(ids, list(reversed(ids)))
        self.assertEqual(m["moved"], 4)                 # el central se queda
        self.assertEqual(m["max"], 4)
        self.assertEqual(m["displacement"]["X000"], 4)
        self.assertEqual(m["displacement"]["X004"], -4)
        self.assertEqual(m["total"], 4 + 2 + 0 + 2 + 4)
        self.assertEqual(m["median"], 2)

    def test_exige_dos_permutaciones_del_mismo_conjunto(self):
        with self.assertRaises(ValueError):
            positions_moved(["R0", "R1"], ["R0", "R2"])


class TestAtribucion(unittest.TestCase):
    """Two rules with the same action decide a case the same way. Measuring
    agreement by which rule fired would report a difference a deployed system
    would not show — so the two quantities are computed separately, and this is
    the instance where they come apart."""

    def test_deciden_igual_y_sin_embargo_dispara_otra_regla(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "A"}
        M = {"R0": mascara([0, 1]), "R1": mascara([0, 1])}
        full = mascara([0, 1])
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0"], M, action, full)
        agree, dis, und = behavioural_distance(dA, dB, full)
        self.assertEqual((agree, dis, und), (2, 0, 0))

        wA, _ = winners(ids, M, full)
        wB, _ = winners(["R1", "R0"], M, full)
        self.assertEqual(wA, {"R0": full})
        self.assertEqual(wB, {"R1": full})
        self.assertEqual(attribution_agreement(wA, wB), 0)

    def test_la_atribucion_esta_contenida_en_el_acuerdo(self):
        """A case won by the same rule in both orders is decided by the same
        action in both, so restricting the attribution to the agreement mask can
        never remove anything. What the two quantities measure is the SHORTFALL
        between them: agreeing for different reasons."""
        for seed in range(10):
            ids, _pool, action, M, full = instancia(9, 40, seed, p_match=0.2)
            a = orden_aleatorio(ids, seed)
            b = orden_aleatorio(ids, 600 + seed)
            wA, _ = winners(a, M, full)
            wB, _ = winners(b, M, full)
            dA, _ = decisions(a, M, action, full)
            dB, _ = decisions(b, M, action, full)
            agree_mask, _dis, _und = agreement_masks(dA, dB, full)
            agree = behavioural_distance(dA, dB, full)[0]
            with self.subTest(seed=seed):
                self.assertEqual(attribution_agreement(wA, wB),
                                 attribution_agreement(wA, wB, agree_mask))
                self.assertLessEqual(attribution_agreement(wA, wB), agree)

    def test_se_restringe_a_la_mascara_que_se_le_da(self):
        """Case 2 is won by R1 in both orders even though R1 moved, so the
        attribution is cases 0, 2 and 3; restricted to case 0 it is one."""
        ids, M, action, full = tres_reglas()
        otro = ["R1", "R0", "R2"]
        wA, _ = winners(ids, M, full)
        wB, _ = winners(otro, M, full)
        self.assertEqual(attribution_agreement(wA, wB), 3)
        self.assertEqual(attribution_agreement(wA, wB, mascara([0])), 1)
        self.assertEqual(attribution_agreement(wA, wB, mascara([1])), 0)

    def test_los_ganadores_parten_el_espacio_igual_que_las_decisiones(self):
        for seed in range(8):
            ids, _pool, action, M, full = instancia(9, 40, seed, p_match=0.2)
            o = orden_aleatorio(ids, seed)
            d, ud = decisions(o, M, action, full)
            w, uw = winners(o, M, full)
            with self.subTest(seed=seed):
                self.assertEqual(ud, uw)
                junto = 0
                for m in w.values():
                    junto |= m
                self.assertEqual(junto, full & ~uw)


class TestFirma(unittest.TestCase):

    def test_es_igual_exactamente_cuando_deciden_lo_mismo(self):
        for seed in range(10):
            ids, _pool, action, M, full = instancia(9, 40, seed)
            a = orden_aleatorio(ids, seed)
            b = orden_aleatorio(ids, 700 + seed)
            fa = signature(*decisions(a, M, action, full))
            fb = signature(*decisions(b, M, action, full))
            dA, _ = decisions(a, M, action, full)
            dB, _ = decisions(b, M, action, full)
            iguales = behavioural_distance(dA, dB, full)[1] == 0
            with self.subTest(seed=seed):
                self.assertEqual(fa == fb, iguales)

    def test_es_hashable_y_no_depende_del_orden_de_las_claves(self):
        _ids, M, action, full = tres_reglas()
        d, und = decisions(["R0", "R1", "R2"], M, action, full)
        self.assertEqual(len({signature(d, und),
                              signature(dict(reversed(list(d.items()))), und)}),
                         1)

    def test_una_accion_que_no_decide_nada_no_cambia_la_firma(self):
        """Whether a caller's dict carries an empty entry is an accident of how
        it was built, not a difference in behaviour."""
        d = {"A": mascara([0, 1]), "B": 0}
        self.assertEqual(signature(d, 0), signature({"A": mascara([0, 1])}, 0))


class TestElInstrumentoEsPuro(unittest.TestCase):
    """§1 of the plan: no oracle, no corpus, no JSON, nothing about optimizers.
    `tests/test_oracle_separation.py` already fails if the oracle appears; this
    is the wider claim, and it is what lets the same code measure a toy and the
    exhaustive space."""

    def test_no_importa_nada_del_repositorio(self):
        arbol = ast.parse((REPO / "rung3" / "order_metrics.py").read_text())
        modulos = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                modulos.update(a.name.split(".")[0] for a in nodo.names)
            elif isinstance(nodo, ast.ImportFrom):
                modulos.add((nodo.module or "").split(".")[0])
        self.assertEqual(modulos & {"harness", "rung2", "rung3",
                                    "rung4", "run_experiment", "json"},
                         set())

    def test_no_escribe_nada(self):
        src = (REPO / "rung3" / "order_metrics.py").read_text()
        for prohibido in ("write_text", "open(", "Path("):
            with self.subTest(prohibido=prohibido):
                self.assertNotIn(prohibido, src)


if __name__ == "__main__":
    unittest.main()
