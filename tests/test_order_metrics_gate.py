"""
STEP 0 FOR THE INSTRUMENT — validate it before pointing it at anything.

--------------------------------------------------------------------------
THE PATTERN, AND WHY IT IS REPEATED A FOURTH TIME
--------------------------------------------------------------------------
`harness.ceiling_check` loaded the true policy into the engine and voided rung 1
before a cent had been spent interpreting it. `rung2.ceiling_check2` did it
for the hybrid engine. `rung3.optimizer_check` did it for the search, and
found the declared neighbourhood insufficient over 29 rules.

This does it for the instrument that compares orders. It is about to be asked
how different two permutations of 577 rules are, on a question nobody has an
intuition for — there is no "expected" behavioural distance the way there is an
expected accuracy — so a wrong answer would not look wrong. Before believing
any of it, it runs on the one instance whose answers are known FOR A REASON:
the 29 rules of the hidden policy over the exhaustive space, where the design
order is the policy itself.

Four checks, all of them known by construction rather than by running the code:

  design vs itself                     no disagreement, and the decisions it
                                       reports ARE the policy's own labels
  design vs a permutation touching      no disagreement, however large the
  only non-conflicting pairs            positional churn, with global tau < 1
                                       and tau restricted to the conflicting
                                       pairs exactly 1
  design with two conflicting rules     the size of the intersection of their
  swapped                               masks among the cases neither loses to
                                       an earlier rule — recomputed here by a
                                       loop that knows nothing about the
                                       instrument
  design vs the fully reversed order    the scale, and it is not a free
                                       parameter: the policy's last layer is
                                       the catch-all, so reversing puts it
                                       first and every case becomes T1_GENERAL

P3 of `PLAN_ORDER_METRICS.md`, and it is BLOCKING: an instrument that cannot
recover an answer known by construction does not get pointed at the real
instance. It costs about 1.5 s and zero API calls, and writes nothing.
"""

from __future__ import annotations

import unittest
from functools import cache

from rung3.optimizer_check import hidden_rules, masks_over_space
from rung3.order_metrics import (agreement_masks, attribution_agreement,
                                    behavioural_distance, conflicting_pairs,
                                    decisions, pair_census,
                                    per_class_disagreement, positions_moved,
                                    signature, tau, winners)
from rung3.order_search_ls import space_truth_masks

DEFECTO = "T1_GENERAL"      # the action of H29, the policy's catch-all layer


@cache
def instancia():
    """The 29 hidden rules over the 134,400 cases, built once for the module.

    `masks_over_space` is `optimizer_check`'s, unchanged: the instance this gate
    validates against has to be the instance the optimizer's own step 0 was
    validated against, or the two gates would be talking about different things.
    """
    ids, conds, action, born = hidden_rules()
    M, W, full, n = masks_over_space(ids, conds, action)
    design = sorted(ids, key=lambda r: born[r])
    return {"ids": ids, "action": action, "M": M, "W": W, "full": full, "n": n,
            "design": design, "truth": space_truth_masks(),
            "conflicting": conflicting_pairs(ids, M, action)}


def pendiente_antes_de(design, k, M, full):
    """Cases no rule before position k matches, by the obvious loop. The
    independent half of the third check: it does not call the instrument."""
    remaining = full
    for rid in design[:k]:
        remaining &= ~M[rid]
    return remaining


def permutacion_de_pares_libres(design, conflicting):
    """
    The design order with disjoint adjacent NON-conflicting pairs exchanged.

    Adjacent and disjoint is what makes the argument airtight: an adjacent
    transposition inverts exactly the pair it exchanges, and stepping past both
    positions means no pair is ever swapped back. So the set of inverted pairs
    is exactly the set returned, and every one of them is free.
    """
    o = list(design)
    invertidos = []
    k = 0
    while k < len(o) - 1:
        par = (min(o[k], o[k + 1]), max(o[k], o[k + 1]))
        if par not in conflicting:
            o[k], o[k + 1] = o[k + 1], o[k]
            invertidos.append(par)
            k += 2
        else:
            k += 1
    return o, invertidos


class TestElOrdenDeDisenoEsLaPolitica(unittest.TestCase):
    """The anchor. If the instrument, run on the policy, does not give back the
    policy, nothing below it means anything."""

    def test_decide_exactamente_las_etiquetas_verdaderas(self):
        inst = instancia()
        d, undecided = decisions(inst["design"], inst["M"], inst["action"],
                                 inst["full"])
        self.assertEqual(undecided, 0)
        self.assertEqual(d, inst["truth"])

    def test_la_verdad_por_clase_parte_el_espacio(self):
        inst = instancia()
        junto = 0
        total = 0
        for m in inst["truth"].values():
            self.assertEqual(junto & m, 0, "dos clases comparten un caso")
            junto |= m
            total += m.bit_count()
        self.assertEqual(junto, inst["full"])
        self.assertEqual(total, inst["n"])

    def test_es_la_misma_verdad_que_ya_usaba_el_optimizador(self):
        """`optimizer_check.masks_over_space` builds this truth for itself and
        keeps it private. The exposed one has to be that one, or two modules
        would be measuring against two oracles."""
        inst = instancia()
        for rid in inst["ids"]:
            with self.subTest(rid=rid):
                self.assertEqual(inst["W"][rid],
                                 inst["M"][rid] & inst["truth"][inst["action"][rid]])

    def test_no_se_diferencia_de_si_mismo(self):
        inst = instancia()
        d, _u = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        self.assertEqual(behavioural_distance(d, d, inst["full"]),
                         (inst["n"], 0, 0))


class TestLosParesLibresNoCambianLaMaquina(unittest.TestCase):
    """The property the whole instrument rests on, on an instance where the
    pairs are the policy's own and not hand-picked."""

    def test_una_permutacion_de_pares_libres_esta_a_distancia_cero(self):
        inst = instancia()
        otro, invertidos = permutacion_de_pares_libres(inst["design"],
                                                       inst["conflicting"])
        self.assertGreater(len(invertidos), 0, "no habria nada que comprobar")

        dA, uA = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        dB, uB = decisions(otro, inst["M"], inst["action"], inst["full"])
        self.assertEqual(behavioural_distance(dA, dB, inst["full"]),
                         (inst["n"], 0, 0))
        self.assertEqual(signature(dA, uA), signature(dB, uB))

    def test_y_sin_embargo_ha_movido_medio_orden(self):
        """Positional churn and behavioural difference are not the same
        quantity, which is the entire reason this module exists."""
        inst = instancia()
        otro, invertidos = permutacion_de_pares_libres(inst["design"],
                                                       inst["conflicting"])
        churn = positions_moved(inst["design"], otro)
        self.assertEqual(churn["moved"], 2 * len(invertidos))
        self.assertGreater(churn["fraction_moved"], 0.5)

    def test_el_tau_global_lo_nota_y_el_restringido_no(self):
        """Q-d's design premise, checked where the answer is known: a rank
        statistic over all pairs reports a difference that does not exist, and
        restricted to the conflicting pairs it reports none, correctly."""
        inst = instancia()
        otro, _inv = permutacion_de_pares_libres(inst["design"],
                                                 inst["conflicting"])
        self.assertLess(tau(inst["design"], otro), 1.0)
        self.assertEqual(tau(inst["design"], otro, inst["conflicting"]), 1.0)


class TestUnParEnConflictoDesplazaLoQueSeCalculaAMano(unittest.TestCase):

    def pares_adyacentes_en_conflicto(self, inst):
        design = inst["design"]
        return [(k, design[k], design[k + 1]) for k in range(len(design) - 1)
                if (min(design[k], design[k + 1]),
                    max(design[k], design[k + 1])) in inst["conflicting"]]

    def test_la_distancia_es_la_interseccion_entre_lo_aun_pendiente(self):
        """With the two rules adjacent, the cases that change hands are exactly
        those both match among the ones no earlier rule has taken. Computed here
        with masks and a loop, and compared against what the instrument says."""
        inst = instancia()
        design, M, action, full = (inst["design"], inst["M"], inst["action"],
                                   inst["full"])
        dA, _u = decisions(design, M, action, full)
        adyacentes = self.pares_adyacentes_en_conflicto(inst)
        self.assertGreater(len(adyacentes), 0)

        esperados = []
        for k, a, b in adyacentes:
            pendiente = pendiente_antes_de(design, k, M, full)
            esperado = (M[a] & M[b] & pendiente).bit_count()
            alt = list(design)
            alt[k], alt[k + 1] = alt[k + 1], alt[k]
            dB, _ = decisions(alt, M, action, full)
            agree, dis, undecided = behavioural_distance(dA, dB, full)
            with self.subTest(k=k, par=(a, b)):
                self.assertEqual(dis, esperado)
                self.assertEqual(agree, inst["n"] - esperado)
                self.assertEqual(undecided, 0)
            esperados.append(esperado)

        self.assertTrue(any(e > 0 for e in esperados),
                        "todos vacios: la comprobacion no comprobaria nada")

    def test_estar_en_conflicto_es_necesario_y_no_suficiente(self):
        """Some adjacent conflicting pairs change nothing at all: they co-match
        somewhere in the space, and nowhere that survives the rules above them.
        Worth pinning, because it is what stops the conflicting-pair census
        from being read as a count of differences that will happen."""
        inst = instancia()
        vacios = [
            (k, a, b) for k, a, b in self.pares_adyacentes_en_conflicto(inst)
            if not (inst["M"][a] & inst["M"][b]
                    & pendiente_antes_de(inst["design"], k, inst["M"],
                                         inst["full"]))
        ]
        self.assertGreater(len(vacios), 0)
        for k, a, b in vacios:
            alt = list(inst["design"])
            alt[k], alt[k + 1] = alt[k + 1], alt[k]
            dA, _ = decisions(inst["design"], inst["M"], inst["action"],
                              inst["full"])
            dB, _ = decisions(alt, inst["M"], inst["action"], inst["full"])
            with self.subTest(par=(a, b)):
                self.assertEqual(
                    behavioural_distance(dA, dB, inst["full"])[1], 0)

    def test_el_censo_de_pares_cuadra_consigo_mismo(self):
        inst = instancia()
        censo = pair_census(inst["ids"], inst["M"], inst["action"])
        self.assertEqual(censo["pairs"], 29 * 28 // 2)
        self.assertEqual(censo["conflicting"], len(inst["conflicting"]))
        self.assertEqual(censo["co_match"],
                         censo["conflicting"] + censo["same_action"])


class TestElOrdenInversoDaLaEscala(unittest.TestCase):
    """The fourth check is not a threshold picked to be passed. Reversing the
    design order puts H29 — `severity >= 1`, the catch-all of the last layer —
    first, so it matches everything and every case is decided T1_GENERAL. The
    numbers below all follow from that."""

    def test_el_inverso_lo_decide_todo_por_defecto(self):
        inst = instancia()
        d, undecided = decisions(list(reversed(inst["design"])), inst["M"],
                                 inst["action"], inst["full"])
        self.assertEqual(undecided, 0)
        self.assertEqual(d, {DEFECTO: inst["full"]})

    def test_acierta_exactamente_la_clase_por_defecto_y_nada_mas(self):
        inst = instancia()
        dA, _ = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        dB, _ = decisions(list(reversed(inst["design"])), inst["M"],
                          inst["action"], inst["full"])
        agree, dis, undecided = behavioural_distance(dA, dB, inst["full"])
        self.assertEqual(agree, inst["truth"][DEFECTO].bit_count())
        self.assertEqual(dis, inst["n"] - agree)
        self.assertEqual(undecided, 0)
        self.assertGreater(dis / inst["n"], 0.9)

        agree_mask, dis_mask, _und = agreement_masks(dA, dB, inst["full"])
        self.assertEqual(agree_mask, inst["truth"][DEFECTO])
        self.assertEqual(dis_mask, inst["full"] & ~inst["truth"][DEFECTO])

    def test_la_distancia_es_simetrica_a_esta_escala(self):
        inst = instancia()
        dA, _ = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        dB, _ = decisions(list(reversed(inst["design"])), inst["M"],
                          inst["action"], inst["full"])
        self.assertEqual(behavioural_distance(dA, dB, inst["full"]),
                         behavioural_distance(dB, dA, inst["full"]))

    def test_por_clase_falla_todas_menos_la_de_por_defecto(self):
        inst = instancia()
        dA, _ = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        dB, _ = decisions(list(reversed(inst["design"])), inst["M"],
                          inst["action"], inst["full"])
        por_clase = per_class_disagreement(dA, dB, inst["truth"])
        self.assertEqual(set(por_clase), set(inst["truth"]))
        for c, v in por_clase.items():
            with self.subTest(clase=c):
                self.assertEqual(v["undecided_either"], 0)
                self.assertEqual(v["rate"], 0.0 if c == DEFECTO else 1.0)
                self.assertEqual(v["n"], inst["truth"][c].bit_count())

    def test_el_tau_no_distingue_esta_escala_de_la_otra(self):
        """Both taus bottom out at -1 against the reversed order, where the
        behavioural distance is 96%: the calibration Q-d asks about cannot be
        read off a single pair of extremes."""
        inst = instancia()
        rev = list(reversed(inst["design"]))
        self.assertEqual(tau(inst["design"], rev), -1.0)
        self.assertEqual(tau(inst["design"], rev, inst["conflicting"]), -1.0)

    def test_donde_coinciden_no_siempre_dispara_la_misma_regla(self):
        """The attribution shortfall, on the real instance: they agree on the
        T1_GENERAL cases, and on part of those they agree for different
        reasons — H29 in one order, some earlier T1_GENERAL rule in the other."""
        inst = instancia()
        rev = list(reversed(inst["design"]))
        dA, _ = decisions(inst["design"], inst["M"], inst["action"], inst["full"])
        dB, _ = decisions(rev, inst["M"], inst["action"], inst["full"])
        agree, _dis, _und = behavioural_distance(dA, dB, inst["full"])
        wA, _ = winners(inst["design"], inst["M"], inst["full"])
        wB, _ = winners(rev, inst["M"], inst["full"])
        misma = attribution_agreement(wA, wB)
        self.assertGreater(misma, 0)
        self.assertLess(misma, agree)


if __name__ == "__main__":
    unittest.main()
