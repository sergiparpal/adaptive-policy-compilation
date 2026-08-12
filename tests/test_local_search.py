"""
Tests for the optimizer that the audit of rungs 3 and 4 puts on trial.

The point of the audit is to find out whether the greedy search was leaving
accuracy on the table. A local search with a bug that reports gains it did not
make would answer that question wrongly and in the flattering direction, which
is exactly the Goodhart failure this project studies. So what is pinned here is
not an accuracy figure: it is that the instrument does what it claims.

  * the score reproduces first-match-wins computed naively, case by case;
  * `best_insertion` equals brute force over every insertion position;
  * when the search stops, it really is at a local optimum of the neighbourhood
    it used — checked exhaustively over the neighbourhood;
  * a move is never applied on a tie, so the result does not depend on the
    traversal order;
  * on instances small enough to enumerate, the optimum found is compared with
    the true optimum over all permutations.

The class-weighted objective, added on 2026-08-12 for step 3 of the audit, is
pinned to the same standard, and to one more: with all-ones weights it must
return exactly what `wt=None` returns, function by function. `wt=None` is the
path every published figure was measured on, and the weighted branch must not
become a second algorithm that quietly scores something else.

NO figure from the real base is pinned here, and the search is not run over it.
The audit has not been reported yet; pinning its numbers in a test would create
an official figure that no FINDINGS backs, which is the same mistake
`tests/test_order_determinism.py` declines to make.
"""

from __future__ import annotations

import itertools
import random
import time
import unittest
from collections import Counter

from peldano3.local_search import (MULTISTART_STARTS, balanced_weights,
                                   best_insertion, build_masks, coverage_length,
                                   declared_starts, greedy_order_from_masks,
                                   local_search, move_pass, multistart,
                                   random_order, score_order, swap_pass,
                                   weights_from_counts)

ACCIONES = ("A", "B", "C")


def instancia(n_reglas, n_casos, seed, p_match=0.35):
    """A random synthetic instance: rules with an action and a set of matched
    cases, cases with a label. Small enough to brute force."""
    rng = random.Random(seed)
    ids = [f"X{k:03d}" for k in range(n_reglas)]
    action = {rid: rng.choice(ACCIONES) for rid in ids}
    label = [rng.choice(ACCIONES) for _ in range(n_casos)]
    pool = [[rid for rid in ids if rng.random() < p_match] for _ in range(n_casos)]
    idxs = list(range(n_casos))
    M, W, full = build_masks(ids, pool, label, action, idxs)
    return ids, pool, label, action, idxs, M, W, full


def puntua_ingenuo(order, pool, label, action, idxs):
    """First-match-wins, written the obvious way. The reference the bitmask
    sweep has to reproduce."""
    rank = {rid: k for k, rid in enumerate(order)}
    ok = 0
    for i in idxs:
        p = pool[i]
        if not p:
            continue
        if action[min(p, key=lambda rid: rank[rid])] == label[i]:
            ok += 1
    return ok


def puntua_ingenuo_con_pesos(order, pool, label, action, idxs, L, n):
    """The same walk, weighting each case won by L // |its class|. It knows
    nothing about the lemma the fast path rests on — it reads the class off the
    CASE, not off the rule — which is what makes it a reference for it."""
    rank = {rid: k for k, rid in enumerate(order)}
    ok = 0
    for i in idxs:
        p = pool[i]
        if not p:
            continue
        if action[min(p, key=lambda rid: rank[rid])] == label[i]:
            ok += L // n[label[i]]
    return ok


class TestPuntuacion(unittest.TestCase):

    def test_reproduce_primera_que_casa_calculada_a_mano(self):
        for seed in range(12):
            ids, pool, label, action, idxs, M, W, full = instancia(8, 40, seed)
            o = random_order(ids, seed=seed)
            with self.subTest(seed=seed):
                self.assertEqual(score_order(o, M, W, full),
                                 puntua_ingenuo(o, pool, label, action, idxs))

    def test_coincide_con_evaluate_del_peldano_3(self):
        """`order_search.evaluate` is what produced the published figures. The
        two must agree, or the audit would not be comparable with the record."""
        from peldano3.order_search import evaluate
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instancia(9, 50, seed)
            o = random_order(ids, seed=100 + seed)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(
                    score_order(o, M, W, full) / len(idxs),
                    evaluate(o, pool, label, action, idxs))

    def test_los_casos_que_nadie_casa_cuentan_como_fallo(self):
        ids = ["X000"]
        action = {"X000": "A"}
        pool = [[], ["X000"]]
        label = ["A", "A"]
        M, W, full = build_masks(ids, pool, label, action, [0, 1])
        self.assertEqual(score_order(ids, M, W, full), 1)

    def test_la_cola_mas_alla_de_la_cobertura_no_puntua(self):
        """Rules past the point where nothing is pending decide nothing on the
        evaluated set. It is a property of the objective, and it is why the
        search can neither improve nor damage that tail."""
        ids, pool, label, action, idxs, M, W, full = instancia(10, 30, seed=3)
        o = random_order(ids, seed=3)
        L = coverage_length(o, M, full)
        base = score_order(o, M, W, full)
        for p in range(L, len(o)):
            for q in range(p + 1, len(o)):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                self.assertEqual(score_order(alt, M, W, full), base)


class TestVorazSobreMascaras(unittest.TestCase):
    """The audit starts from the greedy of the record. If the mask rewrite were
    not the same construction, everything measured afterwards would be a gain
    over a different baseline."""

    def test_produce_el_mismo_orden_que_el_voraz_del_peldano_3(self):
        from peldano3.order_search import greedy_order
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(11, 60, seed)
            born = {rid: k for k, rid in enumerate(ids)}
            rules = [{"rule_id": rid, "action": action[rid], "born_at": born[rid],
                      "conditions": []} for rid in ids]

            def prec(rid):
                w = W[rid].bit_count()
                miss = (M[rid] ^ W[rid]).bit_count()
                return (w / (w + miss)) if (w + miss) else -1.0

            esperado = greedy_order(rules, pool, label, action, idxs)
            obtenido = greedy_order_from_masks(
                ids, M, W, full, tail_key=lambda rid: (-prec(rid), born[rid]))
            with self.subTest(seed=seed):
                self.assertEqual(obtenido, esperado)


class TestMejorInsercion(unittest.TestCase):

    def test_iguala_a_la_fuerza_bruta_sobre_todas_las_posiciones(self):
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(7, 40, seed)
            o = random_order(ids, seed=seed)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                bruto = []
                for j in range(len(o)):
                    cand = resto[:j] + [o[k]] + resto[j:]
                    bruto.append(score_order(cand, M, W, full))
                mejor_k, mejor = best_insertion(o, k, M, W, full)
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(mejor, max(bruto))
                    self.assertEqual(bruto[mejor_k], max(bruto))

    def test_en_la_posicion_actual_devuelve_la_puntuacion_actual(self):
        """The internal invariant: score(k_cur) must be the score of the order
        as it stands. If it drifts, every reported gain is fiction."""
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(9, 50, seed)
            o = random_order(ids, seed=seed)
            base = score_order(o, M, W, full)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                cand = resto[:k] + [o[k]] + resto[k:]
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(score_order(cand, M, W, full), base)

    def test_no_mueve_nada_ante_un_empate(self):
        """Two rules with the same action are interchangeable: no relocation
        may be applied, or the result would depend on the traversal order the
        way the old tie-break did."""
        ids = ["X000", "X001", "X002"]
        action = {"X000": "A", "X001": "A", "X002": "A"}
        pool = [ids, ids, ids]
        label = ["A", "A", "A"]
        M, W, full = build_masks(ids, pool, label, action, [0, 1, 2])
        for k in range(3):
            self.assertEqual(best_insertion(ids, k, M, W, full)[0], k)


class TestPasadas(unittest.TestCase):

    def test_ninguna_pasada_empeora(self):
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(10, 60, seed)
            for pasada in (move_pass, swap_pass):
                o = random_order(ids, seed=seed)
                antes = score_order(o, M, W, full)
                pasada(o, M, W, full)
                with self.subTest(seed=seed, pasada=pasada.__name__):
                    self.assertGreaterEqual(score_order(o, M, W, full), antes)
                    self.assertEqual(sorted(o), sorted(ids))


class TestBusquedaLocal(unittest.TestCase):

    def test_devuelve_una_permutacion_y_la_ganancia_declarada_es_real(self):
        for seed in range(8):
            ids, pool, label, action, idxs, M, W, full = instancia(12, 80, seed)
            o0 = random_order(ids, seed=seed)
            for vec in ("move", "swap", "move+swap"):
                o, st = local_search(o0, M, W, full, neighbourhood=vec)
                with self.subTest(seed=seed, vecindario=vec):
                    self.assertEqual(sorted(o), sorted(ids))
                    self.assertEqual(st["start"], score_order(o0, M, W, full))
                    self.assertEqual(st["end"], score_order(o, M, W, full))
                    self.assertEqual(st["gain"], st["end"] - st["start"])
                    self.assertGreaterEqual(st["gain"], 0)
                    self.assertFalse(st["exhausted"])

    def test_al_parar_esta_en_un_optimo_local_de_su_vecindario(self):
        """The property that makes the audit's answer mean anything: when it
        says 'no improvement left', there really is none in that neighbourhood.
        Checked by enumerating the whole neighbourhood."""
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instancia(11, 70, seed)
            o0 = random_order(ids, seed=seed)
            n = len(ids)

            o, _ = local_search(o0, M, W, full, neighbourhood="swap")
            base = score_order(o, M, W, full)
            for p, q in itertools.combinations(range(n), 2):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                with self.subTest(seed=seed, vecindario="swap", par=(p, q)):
                    self.assertLessEqual(score_order(alt, M, W, full), base)

            o, _ = local_search(o0, M, W, full, neighbourhood="move")
            base = score_order(o, M, W, full)
            for k in range(n):
                resto = o[:k] + o[k + 1:]
                for j in range(n):
                    alt = resto[:j] + [o[k]] + resto[j:]
                    with self.subTest(seed=seed, vecindario="move", k=k, j=j):
                        self.assertLessEqual(score_order(alt, M, W, full), base)

    def test_es_determinista(self):
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instancia(12, 80, seed)
            o0 = random_order(ids, seed=seed)
            for vec in ("move", "swap", "move+swap"):
                a, sa = local_search(o0, M, W, full, neighbourhood=vec)
                b, sb = local_search(o0, M, W, full, neighbourhood=vec)
                with self.subTest(seed=seed, vecindario=vec):
                    self.assertEqual(a, b)
                    self.assertEqual(sa, sb)

    def test_no_toca_el_orden_de_partida(self):
        ids, pool, label, action, idxs, M, W, full = instancia(10, 50, seed=1)
        o0 = random_order(ids, seed=1)
        copia = list(o0)
        local_search(o0, M, W, full)
        self.assertEqual(o0, copia)

    def test_alcanza_el_optimo_global_en_instancias_enumerables(self):
        """Not a guarantee — it is a heuristic and this only says it is not
        obviously broken. What Step 0 of the audit measures is precisely this,
        on the one instance whose optimum is known for a reason."""
        alcanzados = 0
        total = 0
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(6, 40, seed)
            optimo = max(score_order(list(p), M, W, full)
                         for p in itertools.permutations(ids))
            o0 = random_order(ids, seed=seed)
            _o, st = local_search(o0, M, W, full, neighbourhood="move+swap")
            total += 1
            alcanzados += (st["end"] == optimo)
            self.assertLessEqual(st["end"], optimo)
        self.assertGreaterEqual(alcanzados, total // 2)

    def test_rechaza_un_vecindario_desconocido(self):
        ids, pool, label, action, idxs, M, W, full = instancia(5, 20, seed=0)
        with self.assertRaises(ValueError):
            local_search(ids, M, W, full, neighbourhood="2-opt")


class TestPesosBalanceados(unittest.TestCase):
    """`balanced_weights` is the whole of the balanced objective: if the weights
    are wrong, the search maximizes something nobody declared."""

    def test_son_enteros_y_compensan_exactamente_el_tamano_de_la_clase(self):
        for seed in range(20):
            ids, _pool, label, action, idxs, _M, _W, _full = instancia(15, 60, seed)
            wt, L, n = balanced_weights(ids, action, label, idxs)
            with self.subTest(seed=seed):
                for rid in ids:
                    self.assertIsInstance(wt[rid], int)
                for c in n:
                    self.assertEqual(L % n[c], 0)
                for rid in ids:
                    if action[rid] in n:
                        # every class contributes the same total weight
                        self.assertEqual(wt[rid] * n[action[rid]], L)

    def test_una_accion_ausente_del_subconjunto_pesa_cero(self):
        """It can win nothing there — W[r] is empty — so the value only has to
        exist for the lookup, and it must not invent score."""
        ids = ["X000", "X001"]
        action = {"X000": "A", "X001": "C"}
        pool = [ids, ids]
        label = ["A", "A"]
        idxs = [0, 1]
        M, W, full = build_masks(ids, pool, label, action, idxs)
        wt, L, n = balanced_weights(ids, action, label, idxs)
        self.assertEqual(wt["X001"], 0)
        self.assertNotIn("C", n)
        self.assertEqual(W["X001"], 0)
        self.assertEqual(score_order(["X001", "X000"], M, W, full, wt), 0)
        self.assertEqual(score_order(["X000", "X001"], M, W, full, wt), L)


class TestObjetivoPonderado(unittest.TestCase):
    """The weighted path against the unweighted one it must generalize, and
    against a naive recomputation it must reproduce."""

    def test_todo_unos_devuelve_exactamente_lo_mismo_que_sin_pesos(self):
        """The equivalence that keeps the weighted branch from being a second
        algorithm. Every function that takes `wt`, on 50 instances."""
        for seed in range(50):
            ids, _pool, _label, _action, _idxs, M, W, full = instancia(20, 40, seed)
            unos = {rid: 1 for rid in ids}
            o0 = random_order(ids, seed=seed)
            with self.subTest(seed=seed):
                self.assertEqual(score_order(o0, M, W, full),
                                 score_order(o0, M, W, full, unos))
                for k in range(len(o0)):
                    self.assertEqual(best_insertion(o0, k, M, W, full),
                                     best_insertion(o0, k, M, W, full, unos))
                for pasada in (move_pass, swap_pass):
                    a, b = list(o0), list(o0)
                    self.assertEqual(pasada(a, M, W, full),
                                     pasada(b, M, W, full, unos))
                    self.assertEqual(a, b)
                for vec in ("move", "swap", "move+swap"):
                    oa, sa = local_search(o0, M, W, full, neighbourhood=vec)
                    ob, sb = local_search(o0, M, W, full, neighbourhood=vec,
                                          wt=unos)
                    self.assertEqual(oa, ob)
                    self.assertEqual(sa, sb)

    def test_la_puntuacion_iguala_el_recuento_caso_a_caso(self):
        """The lemma made falsifiable: the fast path reads the class off the
        RULE, the reference reads it off the CASE, and they must agree."""
        for seed in range(20):
            ids, pool, label, action, idxs, M, W, full = instancia(12, 60, seed)
            wt, L, n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=100 + seed)
            with self.subTest(seed=seed):
                self.assertEqual(
                    score_order(o, M, W, full, wt),
                    puntua_ingenuo_con_pesos(o, pool, label, action, idxs, L, n))

    def test_es_el_acierto_balanceado_por_una_constante(self):
        """What makes this objective the BALANCED one, checked against the
        `per_class` of the module that owns the published figure:
        score / (L * |clases|) is exactly its balanced accuracy."""
        from peldano3.budget_and_balance import per_class

        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instancia(12, 60, seed)
            wt, L, n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=200 + seed)
            _tot, _ok, _ceil, balanceado = per_class(o, pool, label, action, idxs)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(
                    score_order(o, M, W, full, wt) / (L * len(n)), balanceado)

    def test_la_mejor_insercion_iguala_a_la_fuerza_bruta_con_pesos(self):
        for seed in range(10):
            ids, _pool, label, action, idxs, M, W, full = instancia(7, 40, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=seed)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                bruto = [score_order(resto[:j] + [o[k]] + resto[j:],
                                     M, W, full, wt) for j in range(len(o))]
                mejor_k, mejor = best_insertion(o, k, M, W, full, wt)
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(mejor, max(bruto))
                    self.assertEqual(bruto[mejor_k], max(bruto))

    def test_termina_y_la_ganancia_declarada_es_real(self):
        """Termination is what the integer weights buy. If `exhausted` ever
        comes back True, the score stopped being a bounded integer and the
        no-move-on-a-tie rule went with it."""
        for seed in range(20):
            ids, _pool, label, action, idxs, M, W, full = instancia(14, 70, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            o0 = random_order(ids, seed=seed)
            for vec in ("move", "swap", "move+swap"):
                o, st = local_search(o0, M, W, full, neighbourhood=vec, wt=wt)
                with self.subTest(seed=seed, vecindario=vec):
                    self.assertFalse(st["exhausted"])
                    self.assertEqual(sorted(o), sorted(ids))
                    self.assertEqual(st["start"], score_order(o0, M, W, full, wt))
                    self.assertEqual(st["end"], score_order(o, M, W, full, wt))
                    self.assertGreaterEqual(st["gain"], 0)

    def test_al_parar_esta_en_un_optimo_local_de_su_vecindario(self):
        """The same guarantee the unweighted search is held to, enumerated over
        the whole neighbourhood."""
        for seed in range(6):
            ids, _pool, label, action, idxs, M, W, full = instancia(11, 70, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            o0 = random_order(ids, seed=seed)
            n = len(ids)

            o, _ = local_search(o0, M, W, full, neighbourhood="swap", wt=wt)
            base = score_order(o, M, W, full, wt)
            for p, q in itertools.combinations(range(n), 2):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                with self.subTest(seed=seed, vecindario="swap", par=(p, q)):
                    self.assertLessEqual(score_order(alt, M, W, full, wt), base)

            o, _ = local_search(o0, M, W, full, neighbourhood="move", wt=wt)
            base = score_order(o, M, W, full, wt)
            for k in range(n):
                resto = o[:k] + o[k + 1:]
                for j in range(n):
                    alt = resto[:j] + [o[k]] + resto[j:]
                    with self.subTest(seed=seed, vecindario="move", k=k, j=j):
                        self.assertLessEqual(score_order(alt, M, W, full, wt),
                                             base)

    def test_el_multiarranque_acepta_pesos_y_no_empeora_su_primer_arranque(self):
        for seed in range(5):
            ids, _pool, label, action, idxs, M, W, full = instancia(11, 70, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            primero = random_order(ids, seed=seed)
            starts = declared_starts(ids, first=primero)
            _solo, st_solo = local_search(primero, M, W, full, wt=wt)
            a, sa = multistart(starts, M, W, full, wt=wt)
            b, sb = multistart(starts, M, W, full, wt=wt)
            with self.subTest(seed=seed):
                self.assertGreaterEqual(sa["best_score"], st_solo["end"])
                self.assertEqual(a, b)
                self.assertEqual(sa, sb)

    def test_el_camino_sin_pesos_no_paga_por_los_pesos(self):
        """P1 asks that the unweighted path not slow down. The gate itself was
        measured against the previous revision, which a test cannot import; what
        is pinned here is the structural half of it — that `wt=None` really is a
        fast path and not the weighted branch with ones — with a loose bound, so
        that it catches a regression and not a busy machine."""
        ids, _pool, label, action, idxs, M, W, full = instancia(60, 300, seed=7)
        unos = {rid: 1 for rid in ids}
        o = random_order(ids, seed=7)

        def cronometra(wt):
            mejor = float("inf")
            for _ in range(5):
                t0 = time.perf_counter()
                for _ in range(20):
                    score_order(o, M, W, full, wt)
                mejor = min(mejor, time.perf_counter() - t0)
            return mejor

        cronometra(None)                       # calienta
        self.assertLess(cronometra(None), 1.5 * cronometra(unos))


class TestRecuentoDeClasesSobreMascaras(unittest.TestCase):
    """`optimizer_check_wt` derives the cases per class from the MASKS instead
    of from the oracle, and gates on a weighted optimum of L x |clases|. A wrong
    count there would validate the instrument against the wrong number, which is
    the one failure mode a step 0 cannot afford."""

    def instancia_cubierta(self, seed, n_reglas=12, n_casos=60):
        """Every case matched by at least one rule carrying its correct label —
        the precondition of the derivation, which the hidden policy satisfies by
        construction because every case is covered by its own rule."""
        rng = random.Random(seed)
        ids = [f"X{k:03d}" for k in range(n_reglas)]
        action = {rid: ACCIONES[k % len(ACCIONES)] for k, rid in enumerate(ids)}
        label = [rng.choice(ACCIONES) for _ in range(n_casos)]
        pool = []
        for y in label:
            p = {rid for rid in ids if rng.random() < 0.3}
            p.add(rng.choice([rid for rid in ids if action[rid] == y]))
            pool.append(sorted(p))
        return ids, action, label, pool, list(range(n_casos))

    def test_reproduce_el_recuento_directo_de_etiquetas(self):
        from peldano3.optimizer_check_wt import class_counts_from_masks

        for seed in range(10):
            ids, action, label, pool, idxs = self.instancia_cubierta(seed)
            _M, W, _full = build_masks(ids, pool, label, action, idxs)
            with self.subTest(seed=seed):
                self.assertEqual(class_counts_from_masks(ids, action, W),
                                 Counter(label))

    def test_un_orden_perfecto_puntua_exactamente_L_por_clases(self):
        """The criterion the weighted gate rests on, in miniature: a policy that
        gets every case right reaches recall 1 in every class at once, so it
        maximizes the balanced objective and its score is L x |clases|."""
        from peldano3.optimizer_check_wt import class_counts_from_masks

        ids = ["X000", "X001", "X002"]
        action = {"X000": "A", "X001": "B", "X002": "C"}
        label = ["A"] * 5 + ["B"] * 3 + ["C"] * 2
        pool = [[rid for rid in ids if action[rid] == y] for y in label]
        idxs = list(range(len(label)))
        M, W, full = build_masks(ids, pool, label, action, idxs)
        wt, L, n = balanced_weights(ids, action, label, idxs)
        self.assertEqual(score_order(ids, M, W, full, wt), L * len(n))
        self.assertEqual(class_counts_from_masks(ids, action, W), Counter(label))

    def test_los_pesos_por_recuento_coinciden_con_los_pesos_por_etiquetas(self):
        for seed in range(10):
            ids, action, label, _pool, idxs = self.instancia_cubierta(seed)
            with self.subTest(seed=seed):
                self.assertEqual(balanced_weights(ids, action, label, idxs),
                                 weights_from_counts(ids, action,
                                                     Counter(label)))


class TestPoolPorMascara(unittest.TestCase):
    """`order_search_ls.space_pools` derives the subsumption-undefeated pool
    with bit arithmetic instead of walking cases one at a time, because over
    134,400 cases the walk is not affordable. It has to agree, case for case,
    with the `build_tables` that computed the record."""

    def test_el_pool_indefenso_coincide_con_build_tables(self):
        from peldano3.order_search import (build_tables, load,
                                           subsumption_below)

        corpus, rules, ext, conds = load()
        ids = [r["rule_id"] for r in rules]
        below = subsumption_below(rules, ext)
        matched, undef, _truth = build_tables(corpus, rules, conds, below)

        # extensions over the corpus, the same way space_pools does it
        cext = {rid: 0 for rid in ids}
        for i, case in enumerate(corpus):
            bit = 1 << i
            for rid in ids:
                if all(c.holds(case) for c in conds[rid]):
                    cext[rid] |= bit
        cundef = {}
        for rid in ids:
            dominado = 0
            for b in below[rid]:
                dominado |= cext[b]
            cundef[rid] = cext[rid] & ~dominado

        for i in range(0, len(corpus), 13):
            with self.subTest(caso=i):
                self.assertEqual({rid for rid in ids if cext[rid] >> i & 1},
                                 set(matched[i]))
                self.assertEqual({rid for rid in ids if cundef[rid] >> i & 1},
                                 set(undef[i]))


class TestElRegistroParcialNoPisaElCompleto(unittest.TestCase):
    """`sweep_ls` rewrites its whole document from the rows of the running
    process. A partial run landing on the canonical name would drop the cells
    that carry the finding — it nearly did on 2026-08-08, which is why this is
    pinned rather than left to the comment."""

    def test_solo_la_corrida_completa_usa_el_nombre_canonico(self):
        from peldano4.sweep_ls import GROUPS, record_name

        self.assertEqual(record_name(list(GROUPS)), "sweep_ls.json")
        self.assertEqual(record_name(list(reversed(GROUPS))), "sweep_ls.json")
        for parcial in (["noise"], ["anchors"], ["anchors", "asymmetry"]):
            with self.subTest(parcial=parcial):
                self.assertNotEqual(record_name(parcial), "sweep_ls.json")
                self.assertTrue(record_name(parcial).endswith(".json"))

    def test_cada_subconjunto_tiene_su_propio_nombre(self):
        from peldano4.sweep_ls import record_name

        nombres = {record_name(g) for g in (["anchors"], ["asymmetry"],
                                            ["noise"], ["anchors", "noise"])}
        self.assertEqual(len(nombres), 4)


class TestMultiArranque(unittest.TestCase):
    """Added on August 8, 2026 after Step 0 of the audit found a single run
    insufficient. What is pinned is that the restarts are declared and that
    knowing the optimum cannot leak into the search."""

    def test_los_arranques_son_fijos_y_reproducibles(self):
        ids = [f"X{k:03d}" for k in range(9)]
        a = declared_starts(ids)
        b = declared_starts(ids)
        self.assertEqual(a, b)
        self.assertEqual(len(a), MULTISTART_STARTS)
        for _nombre, o in a:
            self.assertEqual(sorted(o), sorted(ids))

    def test_el_voraz_ocupa_la_posicion_cero(self):
        """So that a tie goes to it and the multi-start is never worse than the
        single run the audit asked for (`results3/FINDINGS_AUDIT.md`, Step 0)."""
        ids = [f"X{k:03d}" for k in range(9)]
        voraz = list(reversed(sorted(ids)))
        starts = declared_starts(ids, first=voraz)
        self.assertEqual(len(starts), MULTISTART_STARTS + 1)
        self.assertEqual(starts[0], ("voraz", voraz))

    def test_no_devuelve_nada_peor_que_su_primer_arranque(self):
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instancia(11, 70, seed)
            primero = random_order(ids, seed=seed)
            starts = declared_starts(ids, first=primero)
            solo, st_solo = local_search(primero, M, W, full)
            _o, st = multistart(starts, M, W, full)
            with self.subTest(seed=seed):
                self.assertGreaterEqual(st["best_score"], st_solo["end"])
                self.assertEqual(st["n_starts"], MULTISTART_STARTS + 1)

    def test_conocer_el_optimo_no_cambia_lo_que_encuentra(self):
        """`optimum` is for reporting the cost. If it steered the search, Step 0
        would be validating an instrument that cannot exist in Step 1, where no
        optimum is known."""
        for seed in range(5):
            ids, pool, label, action, idxs, M, W, full = instancia(10, 60, seed)
            starts = declared_starts(ids)
            a, sa = multistart(starts, M, W, full, optimum=None)
            b, sb = multistart(starts, M, W, full, optimum=len(idxs))
            with self.subTest(seed=seed):
                self.assertEqual(a, b)
                self.assertEqual(sa["best_score"], sb["best_score"])
                self.assertEqual(sa["best_from_index"], sb["best_from_index"])

    def test_declara_el_coste_de_los_reinicios(self):
        """The first hit and how many hit have to be on the record: they are
        what says whether the restarts were cheap or lucky."""
        ids, pool, label, action, idxs, M, W, full = instancia(8, 50, seed=2)
        starts = declared_starts(ids)
        optimo = max(score_order(list(p), M, W, full)
                     for p in itertools.permutations(ids))
        _o, st = multistart(starts, M, W, full, optimum=optimo)
        self.assertTrue(st["reached_optimum"])
        self.assertEqual(st["best_score"], optimo)
        self.assertGreaterEqual(st["n_hits"], 1)
        self.assertEqual(st["starts_until_first_hit"], st["first_hit_index"] + 1)
        self.assertEqual(st["rows"][st["first_hit_index"]]["end_score"], optimo)

    def test_es_determinista(self):
        ids, pool, label, action, idxs, M, W, full = instancia(10, 60, seed=4)
        starts = declared_starts(ids)
        for vec in ("move", "swap", "move+swap"):
            a, sa = multistart(starts, M, W, full, neighbourhood=vec)
            b, sb = multistart(starts, M, W, full, neighbourhood=vec)
            with self.subTest(vecindario=vec):
                self.assertEqual(a, b)
                self.assertEqual(sa, sb)

    def test_sin_optimo_no_inventa_aciertos(self):
        """With no optimum declared there is nothing to hit, and the fields that
        report the cost must say so rather than defaulting to a success."""
        ids, pool, label, action, idxs, M, W, full = instancia(9, 50, seed=5)
        _o, st = multistart(declared_starts(ids), M, W, full)
        self.assertFalse(st["reached_optimum"])
        self.assertIsNone(st["first_hit_index"])
        self.assertIsNone(st["starts_until_first_hit"])
        self.assertEqual(st["n_hits"], 0)


if __name__ == "__main__":
    unittest.main()
