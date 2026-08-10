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

NO figure from the real base is pinned here, and the search is not run over it.
The audit has not been reported yet; pinning its numbers in a test would create
an official figure that no FINDINGS backs, which is the same mistake
`tests/test_order_determinism.py` declines to make.
"""

from __future__ import annotations

import itertools
import random
import unittest

from peldano3.local_search import (MULTISTART_STARTS, best_insertion,
                                   build_masks, coverage_length, declared_starts,
                                   greedy_order_from_masks, local_search,
                                   move_pass, multistart, random_order,
                                   score_order, swap_pass)

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
