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

from rung3.local_search import (MULTISTART_STARTS, balanced_weights,
                                   best_insertion, build_masks, coverage_length,
                                   declared_starts, greedy_order_from_masks,
                                   local_search, move_pass, multistart,
                                   random_order, score_order, swap_pass,
                                   weights_from_counts)

ACTION_LIST = ("A", "B", "C")


def instance(n_rules, n_cases, seed, p_match=0.35):
    """A random synthetic instance: rules with an action and a set of matched
    cases, cases with a label. Small enough to brute force."""
    rng = random.Random(seed)
    ids = [f"X{k:03d}" for k in range(n_rules)]
    action = {rid: rng.choice(ACTION_LIST) for rid in ids}
    label = [rng.choice(ACTION_LIST) for _ in range(n_cases)]
    pool = [[rid for rid in ids if rng.random() < p_match] for _ in range(n_cases)]
    idxs = list(range(n_cases))
    M, W, full = build_masks(ids, pool, label, action, idxs)
    return ids, pool, label, action, idxs, M, W, full


def score_naive(order, pool, label, action, idxs):
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


def score_naive_with_weights(order, pool, label, action, idxs, L, n):
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


class TestScoring(unittest.TestCase):

    def test_reproduces_first_match_computed_by_hand(self):
        for seed in range(12):
            ids, pool, label, action, idxs, M, W, full = instance(8, 40, seed)
            o = random_order(ids, seed=seed)
            with self.subTest(seed=seed):
                self.assertEqual(score_order(o, M, W, full),
                                 score_naive(o, pool, label, action, idxs))

    def test_agrees_with_evaluate_from_rung_3(self):
        """`order_search.evaluate` is what produced the published figures. The
        two must agree, or the audit would not be comparable with the record."""
        from rung3.order_search import evaluate
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instance(9, 50, seed)
            o = random_order(ids, seed=100 + seed)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(
                    score_order(o, M, W, full) / len(idxs),
                    evaluate(o, pool, label, action, idxs))

    def test_cases_nobody_matches_count_as_failures(self):
        ids = ["X000"]
        action = {"X000": "A"}
        pool = [[], ["X000"]]
        label = ["A", "A"]
        M, W, full = build_masks(ids, pool, label, action, [0, 1])
        self.assertEqual(score_order(ids, M, W, full), 1)

    def test_the_tail_beyond_coverage_does_not_score(self):
        """Rules past the point where nothing is pending decide nothing on the
        evaluated set. It is a property of the objective, and it is why the
        search can neither improve nor damage that tail."""
        ids, pool, label, action, idxs, M, W, full = instance(10, 30, seed=3)
        o = random_order(ids, seed=3)
        L = coverage_length(o, M, full)
        base = score_order(o, M, W, full)
        for p in range(L, len(o)):
            for q in range(p + 1, len(o)):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                self.assertEqual(score_order(alt, M, W, full), base)


class TestGreedyOverMasks(unittest.TestCase):
    """The audit starts from the greedy of the record. If the mask rewrite were
    not the same construction, everything measured afterwards would be a gain
    over a different baseline."""

    def test_produces_the_same_order_as_the_rung_3_greedy(self):
        from rung3.order_search import greedy_order
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(11, 60, seed)
            born = {rid: k for k, rid in enumerate(ids)}
            rules = [{"rule_id": rid, "action": action[rid], "born_at": born[rid],
                      "conditions": []} for rid in ids]

            def prec(rid):
                w = W[rid].bit_count()
                miss = (M[rid] ^ W[rid]).bit_count()
                return (w / (w + miss)) if (w + miss) else -1.0

            expected = greedy_order(rules, pool, label, action, idxs)
            obtained = greedy_order_from_masks(
                ids, M, W, full, tail_key=lambda rid: (-prec(rid), born[rid]))
            with self.subTest(seed=seed):
                self.assertEqual(obtained, expected)


class TestBestInsertion(unittest.TestCase):

    def test_equals_brute_force_over_every_position(self):
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(7, 40, seed)
            o = random_order(ids, seed=seed)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                bruto = []
                for j in range(len(o)):
                    cand = resto[:j] + [o[k]] + resto[j:]
                    bruto.append(score_order(cand, M, W, full))
                best_k, best = best_insertion(o, k, M, W, full)
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(best, max(bruto))
                    self.assertEqual(bruto[best_k], max(bruto))

    def test_at_the_current_position_it_returns_the_current_score(self):
        """The internal invariant: score(k_cur) must be the score of the order
        as it stands. If it drifts, every reported gain is fiction."""
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(9, 50, seed)
            o = random_order(ids, seed=seed)
            base = score_order(o, M, W, full)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                cand = resto[:k] + [o[k]] + resto[k:]
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(score_order(cand, M, W, full), base)

    def test_moves_nothing_on_a_tie(self):
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


class TestPasses(unittest.TestCase):

    def test_no_pass_makes_it_worse(self):
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(10, 60, seed)
            for sweep_pass in (move_pass, swap_pass):
                o = random_order(ids, seed=seed)
                before = score_order(o, M, W, full)
                sweep_pass(o, M, W, full)
                with self.subTest(seed=seed, sweep_pass=sweep_pass.__name__):
                    self.assertGreaterEqual(score_order(o, M, W, full), before)
                    self.assertEqual(sorted(o), sorted(ids))


class TestLocalSearch(unittest.TestCase):

    def test_returns_a_permutation_and_the_declared_gain_is_real(self):
        for seed in range(8):
            ids, pool, label, action, idxs, M, W, full = instance(12, 80, seed)
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

    def test_on_stopping_it_is_at_a_local_optimum_of_its_neighbourhood(self):
        """The property that makes the audit's answer mean anything: when it
        says 'no improvement left', there really is none in that neighbourhood.
        Checked by enumerating the whole neighbourhood."""
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instance(11, 70, seed)
            o0 = random_order(ids, seed=seed)
            n = len(ids)

            o, _ = local_search(o0, M, W, full, neighbourhood="swap")
            base = score_order(o, M, W, full)
            for p, q in itertools.combinations(range(n), 2):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                with self.subTest(seed=seed, vecindario="swap", pair=(p, q)):
                    self.assertLessEqual(score_order(alt, M, W, full), base)

            o, _ = local_search(o0, M, W, full, neighbourhood="move")
            base = score_order(o, M, W, full)
            for k in range(n):
                resto = o[:k] + o[k + 1:]
                for j in range(n):
                    alt = resto[:j] + [o[k]] + resto[j:]
                    with self.subTest(seed=seed, vecindario="move", k=k, j=j):
                        self.assertLessEqual(score_order(alt, M, W, full), base)

    def test_is_deterministic(self):
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instance(12, 80, seed)
            o0 = random_order(ids, seed=seed)
            for vec in ("move", "swap", "move+swap"):
                a, sa = local_search(o0, M, W, full, neighbourhood=vec)
                b, sb = local_search(o0, M, W, full, neighbourhood=vec)
                with self.subTest(seed=seed, vecindario=vec):
                    self.assertEqual(a, b)
                    self.assertEqual(sa, sb)

    def test_does_not_touch_the_starting_order(self):
        ids, pool, label, action, idxs, M, W, full = instance(10, 50, seed=1)
        o0 = random_order(ids, seed=1)
        copy = list(o0)
        local_search(o0, M, W, full)
        self.assertEqual(o0, copy)

    def test_reaches_the_global_optimum_on_enumerable_instances(self):
        """Not a guarantee — it is a heuristic and this only says it is not
        obviously broken. What Step 0 of the audit measures is precisely this,
        on the one instance whose optimum is known for a reason."""
        reached = 0
        total = 0
        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(6, 40, seed)
            true_optimum = max(score_order(list(p), M, W, full)
                               for p in itertools.permutations(ids))
            o0 = random_order(ids, seed=seed)
            _o, st = local_search(o0, M, W, full, neighbourhood="move+swap")
            total += 1
            reached += (st["end"] == true_optimum)
            self.assertLessEqual(st["end"], true_optimum)
        self.assertGreaterEqual(reached, total // 2)

    def test_rejects_an_unknown_neighbourhood(self):
        ids, pool, label, action, idxs, M, W, full = instance(5, 20, seed=0)
        with self.assertRaises(ValueError):
            local_search(ids, M, W, full, neighbourhood="2-opt")


class TestBalancedWeights(unittest.TestCase):
    """`balanced_weights` is the whole of the balanced objective: if the weights
    are wrong, the search maximizes something nobody declared."""

    def test_they_are_integers_and_exactly_offset_the_class_size(self):
        for seed in range(20):
            ids, _pool, label, action, idxs, _M, _W, _full = instance(15, 60, seed)
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

    def test_an_action_absent_from_the_subset_weighs_zero(self):
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


class TestWeightedObjective(unittest.TestCase):
    """The weighted path against the unweighted one it must generalize, and
    against a naive recomputation it must reproduce."""

    def test_all_ones_returns_exactly_the_same_as_without_weights(self):
        """The equivalence that keeps the weighted branch from being a second
        algorithm. Every function that takes `wt`, on 50 instances."""
        for seed in range(50):
            ids, _pool, _label, _action, _idxs, M, W, full = instance(20, 40, seed)
            a_few = {rid: 1 for rid in ids}
            o0 = random_order(ids, seed=seed)
            with self.subTest(seed=seed):
                self.assertEqual(score_order(o0, M, W, full),
                                 score_order(o0, M, W, full, a_few))
                for k in range(len(o0)):
                    self.assertEqual(best_insertion(o0, k, M, W, full),
                                     best_insertion(o0, k, M, W, full, a_few))
                for sweep_pass in (move_pass, swap_pass):
                    a, b = list(o0), list(o0)
                    self.assertEqual(sweep_pass(a, M, W, full),
                                     sweep_pass(b, M, W, full, a_few))
                    self.assertEqual(a, b)
                for vec in ("move", "swap", "move+swap"):
                    oa, sa = local_search(o0, M, W, full, neighbourhood=vec)
                    ob, sb = local_search(o0, M, W, full, neighbourhood=vec,
                                          wt=a_few)
                    self.assertEqual(oa, ob)
                    self.assertEqual(sa, sb)

    def test_the_score_equals_the_case_by_case_count(self):
        """The lemma made falsifiable: the fast path reads the class off the
        RULE, the reference reads it off the CASE, and they must agree."""
        for seed in range(20):
            ids, pool, label, action, idxs, M, W, full = instance(12, 60, seed)
            wt, L, n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=100 + seed)
            with self.subTest(seed=seed):
                self.assertEqual(
                    score_order(o, M, W, full, wt),
                    score_naive_with_weights(o, pool, label, action, idxs, L, n))

    def test_it_is_balanced_accuracy_up_to_a_constant(self):
        """What makes this objective the BALANCED one, checked against the
        `per_class` of the module that owns the published figure:
        score / (L * |clases|) is exactly its balanced accuracy."""
        from rung3.budget_and_balance import per_class

        for seed in range(10):
            ids, pool, label, action, idxs, M, W, full = instance(12, 60, seed)
            wt, L, n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=200 + seed)
            _tot, _ok, _ceil, balanced = per_class(o, pool, label, action, idxs)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(
                    score_order(o, M, W, full, wt) / (L * len(n)), balanced)

    def test_best_insertion_equals_brute_force_with_weights(self):
        for seed in range(10):
            ids, _pool, label, action, idxs, M, W, full = instance(7, 40, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            o = random_order(ids, seed=seed)
            for k in range(len(o)):
                resto = o[:k] + o[k + 1:]
                bruto = [score_order(resto[:j] + [o[k]] + resto[j:],
                                     M, W, full, wt) for j in range(len(o))]
                best_k, best = best_insertion(o, k, M, W, full, wt)
                with self.subTest(seed=seed, k=k):
                    self.assertEqual(best, max(bruto))
                    self.assertEqual(bruto[best_k], max(bruto))

    def test_terminates_and_the_declared_gain_is_real(self):
        """Termination is what the integer weights buy. If `exhausted` ever
        comes back True, the score stopped being a bounded integer and the
        no-move-on-a-tie rule went with it."""
        for seed in range(20):
            ids, _pool, label, action, idxs, M, W, full = instance(14, 70, seed)
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

    def test_on_stopping_it_is_at_a_local_optimum_of_its_neighbourhood(self):
        """The same guarantee the unweighted search is held to, enumerated over
        the whole neighbourhood."""
        for seed in range(6):
            ids, _pool, label, action, idxs, M, W, full = instance(11, 70, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            o0 = random_order(ids, seed=seed)
            n = len(ids)

            o, _ = local_search(o0, M, W, full, neighbourhood="swap", wt=wt)
            base = score_order(o, M, W, full, wt)
            for p, q in itertools.combinations(range(n), 2):
                alt = list(o)
                alt[p], alt[q] = alt[q], alt[p]
                with self.subTest(seed=seed, vecindario="swap", pair=(p, q)):
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

    def test_the_multistart_accepts_weights_and_does_not_worsen_its_first_start(self):
        for seed in range(5):
            ids, _pool, label, action, idxs, M, W, full = instance(11, 70, seed)
            wt, _L, _n = balanced_weights(ids, action, label, idxs)
            first_start = random_order(ids, seed=seed)
            starts = declared_starts(ids, first=first_start)
            _only, st_only = local_search(first_start, M, W, full, wt=wt)
            a, sa = multistart(starts, M, W, full, wt=wt)
            b, sb = multistart(starts, M, W, full, wt=wt)
            with self.subTest(seed=seed):
                self.assertGreaterEqual(sa["best_score"], st_only["end"])
                self.assertEqual(a, b)
                self.assertEqual(sa, sb)

    def test_the_unweighted_path_does_not_pay_for_the_weights(self):
        """P1 asks that the unweighted path not slow down. The gate itself was
        measured against the previous revision, which a test cannot import; what
        is pinned here is the structural half of it — that `wt=None` really is a
        fast path and not the weighted branch with ones — with a loose bound, so
        that it catches a regression and not a busy machine."""
        ids, _pool, label, action, idxs, M, W, full = instance(60, 300, seed=7)
        a_few = {rid: 1 for rid in ids}
        o = random_order(ids, seed=7)

        def time_it(wt):
            best = float("inf")
            for _ in range(5):
                t0 = time.perf_counter()
                for _ in range(20):
                    score_order(o, M, W, full, wt)
                best = min(best, time.perf_counter() - t0)
            return best

        time_it(None)                       # calienta
        self.assertLess(time_it(None), 1.5 * time_it(a_few))


class TestTheStep0WeightedOptimum(unittest.TestCase):
    """The gate of `optimizer_check_wt` rests on one arithmetic claim: a policy
    that gets every case right reaches recall 1 in every class at once, so it
    maximizes the balanced objective and scores exactly L x |clases|. If that
    number were wrong the instrument would be validated against the wrong
    target, which is the one failure mode a step 0 cannot afford.

    The counts come from the oracle (`class_counts`), and after 2026-08-13 they
    come from nowhere else. An earlier version derived them from the masks to
    avoid the import; the masks give the per-class CEILING, which coincides with
    the class size only where every case is winnable — on the hidden policy, and
    not on the 577 rules."""

    def test_a_perfect_order_scores_exactly_L_over_classes(self):
        ids = ["X000", "X001", "X002"]
        action = {"X000": "A", "X001": "B", "X002": "C"}
        label = ["A"] * 5 + ["B"] * 3 + ["C"] * 2
        pool = [[rid for rid in ids if action[rid] == y] for y in label]
        idxs = list(range(len(label)))
        M, W, full = build_masks(ids, pool, label, action, idxs)
        wt, L, n = balanced_weights(ids, action, label, idxs)
        self.assertEqual(score_order(ids, M, W, full, wt), L * len(n))

    def test_the_oracle_count_counts_every_case(self):
        """What the mask route got wrong: every case belongs to its class,
        winnable or not."""
        from harness.domain import generate_corpus
        from rung3.optimizer_check_wt import class_counts

        corpus = generate_corpus(200, seed=17)
        n = class_counts(corpus)
        self.assertEqual(sum(n.values()), len(corpus))

    def test_count_weights_agree_with_label_weights(self):
        rng = random.Random(11)
        for seed in range(10):
            ids = [f"X{k:03d}" for k in range(12)]
            action = {rid: ACTION_LIST[k % len(ACTION_LIST)]
                      for k, rid in enumerate(ids)}
            label = [rng.choice(ACTION_LIST) for _ in range(60)]
            idxs = list(range(len(label)))
            with self.subTest(seed=seed):
                self.assertEqual(balanced_weights(ids, action, label, idxs),
                                 weights_from_counts(ids, action,
                                                     Counter(label)))


class TestPoolByMask(unittest.TestCase):
    """`order_search_ls.space_pools` derives the subsumption-undefeated pool
    with bit arithmetic instead of walking cases one at a time, because over
    134,400 cases the walk is not affordable. It has to agree, case for case,
    with the `build_tables` that computed the record."""

    def test_the_undefended_pool_agrees_with_build_tables(self):
        from rung3.order_search import (build_tables, load,
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
            dominated = 0
            for b in below[rid]:
                dominated |= cext[b]
            cundef[rid] = cext[rid] & ~dominated

        for i in range(0, len(corpus), 13):
            with self.subTest(case=i):
                self.assertEqual({rid for rid in ids if cext[rid] >> i & 1},
                                 set(matched[i]))
                self.assertEqual({rid for rid in ids if cundef[rid] >> i & 1},
                                 set(undef[i]))


class TestThePartialRecordDoesNotTreadOnTheFull(unittest.TestCase):
    """`sweep_ls` rewrites its whole document from the rows of the running
    process. A partial run landing on the canonical name would drop the cells
    that carry the finding — it nearly did on 2026-08-08, which is why this is
    pinned rather than left to the comment."""

    def test_only_the_full_run_uses_the_canonical_name(self):
        from rung4.sweep_ls import GROUPS, record_name

        self.assertEqual(record_name(list(GROUPS)), "sweep_ls.json")
        self.assertEqual(record_name(list(reversed(GROUPS))), "sweep_ls.json")
        for partial in (["noise"], ["anchors"], ["anchors", "asymmetry"]):
            with self.subTest(partial=partial):
                self.assertNotEqual(record_name(partial), "sweep_ls.json")
                self.assertTrue(record_name(partial).endswith(".json"))

    def test_each_subset_has_its_own_name(self):
        from rung4.sweep_ls import record_name

        names = {record_name(g) for g in (["anchors"], ["asymmetry"],
                                            ["noise"], ["anchors", "noise"])}
        self.assertEqual(len(names), 4)


class TestMultiStart(unittest.TestCase):
    """Added on August 8, 2026 after Step 0 of the audit found a single run
    insufficient. What is pinned is that the restarts are declared and that
    knowing the optimum cannot leak into the search."""

    def test_the_starts_are_fixed_and_reproducible(self):
        ids = [f"X{k:03d}" for k in range(9)]
        a = declared_starts(ids)
        b = declared_starts(ids)
        self.assertEqual(a, b)
        self.assertEqual(len(a), MULTISTART_STARTS)
        for _name, o in a:
            self.assertEqual(sorted(o), sorted(ids))

    def test_larger_budgets_are_nested(self):
        """The property the start-budget diagnostic rests on: the shuffles come
        off `random.Random(17)` in sequence, so 256 starts BEGIN with the same 64
        the record used. Without it, comparing budgets would be comparing two
        different samples and the diagnostic would say nothing."""
        ids = [f"X{k:03d}" for k in range(9)]
        greedy = list(reversed(sorted(ids)))
        pequeno = declared_starts(ids, first=greedy, n=64)
        for n in (128, 256):
            grande = declared_starts(ids, first=greedy, n=n)
            with self.subTest(n=n):
                self.assertEqual(grande[:len(pequeno)], pequeno)
                self.assertEqual(len(grande), n + 1)

    def test_the_greedy_occupies_position_zero(self):
        """So that a tie goes to it and the multi-start is never worse than the
        single run the audit asked for (`results3/FINDINGS_AUDIT.md`, Step 0)."""
        ids = [f"X{k:03d}" for k in range(9)]
        greedy = list(reversed(sorted(ids)))
        starts = declared_starts(ids, first=greedy)
        self.assertEqual(len(starts), MULTISTART_STARTS + 1)
        self.assertEqual(starts[0], ("voraz", greedy))

    def test_returns_nothing_worse_than_its_first_start(self):
        for seed in range(6):
            ids, pool, label, action, idxs, M, W, full = instance(11, 70, seed)
            first_start = random_order(ids, seed=seed)
            starts = declared_starts(ids, first=first_start)
            alone, st_only = local_search(first_start, M, W, full)
            _o, st = multistart(starts, M, W, full)
            with self.subTest(seed=seed):
                self.assertGreaterEqual(st["best_score"], st_only["end"])
                self.assertEqual(st["n_starts"], MULTISTART_STARTS + 1)

    def test_knowing_the_optimum_does_not_change_what_it_finds(self):
        """`optimum` is for reporting the cost. If it steered the search, Step 0
        would be validating an instrument that cannot exist in Step 1, where no
        optimum is known."""
        for seed in range(5):
            ids, pool, label, action, idxs, M, W, full = instance(10, 60, seed)
            starts = declared_starts(ids)
            a, sa = multistart(starts, M, W, full, optimum=None)
            b, sb = multistart(starts, M, W, full, optimum=len(idxs))
            with self.subTest(seed=seed):
                self.assertEqual(a, b)
                self.assertEqual(sa["best_score"], sb["best_score"])
                self.assertEqual(sa["best_from_index"], sb["best_from_index"])

    def test_declares_the_cost_of_the_restarts(self):
        """The first hit and how many hit have to be on the record: they are
        what says whether the restarts were cheap or lucky."""
        ids, pool, label, action, idxs, M, W, full = instance(8, 50, seed=2)
        starts = declared_starts(ids)
        true_optimum = max(score_order(list(p), M, W, full)
                           for p in itertools.permutations(ids))
        _o, st = multistart(starts, M, W, full, optimum=true_optimum)
        self.assertTrue(st["reached_optimum"])
        self.assertEqual(st["best_score"], true_optimum)
        self.assertGreaterEqual(st["n_hits"], 1)
        self.assertEqual(st["starts_until_first_hit"], st["first_hit_index"] + 1)
        self.assertEqual(st["rows"][st["first_hit_index"]]["end_score"], true_optimum)

    def test_is_deterministic(self):
        ids, pool, label, action, idxs, M, W, full = instance(10, 60, seed=4)
        starts = declared_starts(ids)
        for vec in ("move", "swap", "move+swap"):
            a, sa = multistart(starts, M, W, full, neighbourhood=vec)
            b, sb = multistart(starts, M, W, full, neighbourhood=vec)
            with self.subTest(vecindario=vec):
                self.assertEqual(a, b)
                self.assertEqual(sa, sb)

    def test_without_an_optimum_it_invents_no_hits(self):
        """With no optimum declared there is nothing to hit, and the fields that
        report the cost must say so rather than defaulting to a success."""
        ids, pool, label, action, idxs, M, W, full = instance(9, 50, seed=5)
        _o, st = multistart(declared_starts(ids), M, W, full)
        self.assertFalse(st["reached_optimum"])
        self.assertIsNone(st["first_hit_index"])
        self.assertIsNone(st["starts_until_first_hit"])
        self.assertEqual(st["n_hits"], 0)


# The output of `multistart` BEFORE `keep_orders` existed, captured on
# 2026-08-14 by running the previous revision on these three instances. It is
# the gate of P1 of `PLAN_ORDER_METRICS.md`: every figure in `results3/` and
# `results4/` was produced through this function, so the default path has to
# keep returning what it returned, and "it looks the same" is not a check.
# Small instances and three explicit starts, so the expectation is readable
# rather than a blob — the property under test is the SHAPE and the arithmetic
# of the dict, and 65 rows would only make it unreadable.
BEFORE_KEEP_ORDERS = {
    0: {"best_order": ["X005", "X003", "X002", "X004", "X001", "X000"],
        "stats": {
            "n_starts": 3, "neighbourhood": "move+swap", "best_score": 13,
            "best_from_index": 1, "best_from": "b", "reached_optimum": False,
            "first_hit_index": None, "first_hit_start": None,
            "starts_until_first_hit": None, "n_hits": 0,
            "rows": [
                {"index": 0, "start": "a", "start_score": 9, "end_score": 12,
                 "rounds": 3, "moves": 3, "swaps": 0, "exhausted": False},
                {"index": 1, "start": "b", "start_score": 10, "end_score": 13,
                 "rounds": 2, "moves": 2, "swaps": 0, "exhausted": False},
                {"index": 2, "start": "c", "start_score": 9, "end_score": 13,
                 "rounds": 2, "moves": 3, "swaps": 0, "exhausted": False}]}},
    1: {"best_order": ["X001", "X002", "X003", "X000", "X005", "X004"],
        "stats": {
            "n_starts": 3, "neighbourhood": "move+swap", "best_score": 9,
            "best_from_index": 0, "best_from": "a", "reached_optimum": False,
            "first_hit_index": None, "first_hit_start": None,
            "starts_until_first_hit": None, "n_hits": 0,
            "rows": [
                {"index": 0, "start": "a", "start_score": 7, "end_score": 9,
                 "rounds": 2, "moves": 2, "swaps": 0, "exhausted": False},
                {"index": 1, "start": "b", "start_score": 6, "end_score": 9,
                 "rounds": 2, "moves": 2, "swaps": 0, "exhausted": False},
                {"index": 2, "start": "c", "start_score": 7, "end_score": 9,
                 "rounds": 2, "moves": 2, "swaps": 0, "exhausted": False}]}},
    2: {"best_order": ["X003", "X000", "X001", "X004", "X005", "X002"],
        "stats": {
            "n_starts": 3, "neighbourhood": "move+swap", "best_score": 12,
            "best_from_index": 0, "best_from": "a", "reached_optimum": False,
            "first_hit_index": None, "first_hit_start": None,
            "starts_until_first_hit": None, "n_hits": 0,
            "rows": [
                {"index": 0, "start": "a", "start_score": 6, "end_score": 12,
                 "rounds": 2, "moves": 3, "swaps": 0, "exhausted": False},
                {"index": 1, "start": "b", "start_score": 6, "end_score": 12,
                 "rounds": 2, "moves": 3, "swaps": 0, "exhausted": False},
                {"index": 2, "start": "c", "start_score": 9, "end_score": 12,
                 "rounds": 2, "moves": 2, "swaps": 0, "exhausted": False}]}},
}


def three_starts(ids, seed):
    """The starts of the snapshot above: named, explicit and independent of
    `declared_starts`, so that changing the declared budget cannot silently
    rewrite the expectation."""
    return [("a", sorted(ids)),
            ("b", list(reversed(sorted(ids)))),
            ("c", random_order(ids, seed=seed))]


class TestMultiStartKeepsOrders(unittest.TestCase):
    """P1 of `PLAN_ORDER_METRICS.md`: the 64 end orders the multi-start used to
    drop are what the whole instrument is going to measure, and capturing them
    must be ADDITIVE. The risk is not that the new field is wrong — it is that
    reaching for it perturbs the search that produced every published figure."""

    def test_unasked_it_returns_exactly_what_it_did_before(self):
        """The gate: against output captured from the previous revision, not
        against the current code's opinion of itself."""
        for seed, expected in BEFORE_KEEP_ORDERS.items():
            ids, _pool, _label, _action, _idxs, M, W, full = instance(6, 30, seed)
            best, st = multistart(three_starts(ids, seed), M, W, full)
            with self.subTest(seed=seed):
                self.assertEqual(best, expected["best_order"])
                self.assertEqual(st, expected["stats"])

    def test_the_default_is_not_to_keep_them(self):
        """Explicit, because the default is what every record ran on."""
        ids, _pool, _label, _action, _idxs, M, W, full = instance(6, 30, seed=0)
        _b, st = multistart(three_starts(ids, 0), M, W, full)
        for row in st["rows"]:
            self.assertNotIn("order", row)

    def test_keeping_them_changes_nothing_else(self):
        """Additive over the declared 65 starts: strip the new key and the two
        dicts have to be the same object, best order included."""
        for seed in range(5):
            ids, _pool, _label, _action, _idxs, M, W, full = instance(11, 70, seed)
            starts = declared_starts(ids, first=random_order(ids, seed=seed))
            a, sa = multistart(starts, M, W, full)
            b, sb = multistart(starts, M, W, full, keep_orders=True)
            bare = dict(sb, rows=[{k: v for k, v in f.items() if k != "order"}
                                  for f in sb["rows"]])
            with self.subTest(seed=seed):
                self.assertEqual(a, b)
                self.assertEqual(sa, bare)

    def test_nor_under_weights(self):
        """The weighted path is the other one a caller can be on."""
        ids, _pool, label, action, idxs, M, W, full = instance(11, 70, seed=3)
        wt, _L, _n = balanced_weights(ids, action, label, idxs)
        starts = declared_starts(ids, first=random_order(ids, seed=3))
        a, sa = multistart(starts, M, W, full, wt=wt)
        b, sb = multistart(starts, M, W, full, wt=wt, keep_orders=True)
        bare = dict(sb, rows=[{k: v for k, v in f.items() if k != "order"}
                              for f in sb["rows"]])
        self.assertEqual(a, b)
        self.assertEqual(sa, bare)

    def test_the_saved_order_is_the_one_that_ends_that_round(self):
        """What makes the field worth having: each row's order is the end order
        of ITS start, re-derivable by running the same search alone, and it
        scores what the row says it scores."""
        for seed in range(3):
            ids, _pool, _label, _action, _idxs, M, W, full = instance(10, 60, seed)
            starts = three_starts(ids, seed)
            _b, st = multistart(starts, M, W, full, keep_orders=True)
            for row, (_name, o0) in zip(st["rows"], starts):
                alone, _ = local_search(o0, M, W, full)
                with self.subTest(seed=seed, arranque=row["start"]):
                    self.assertEqual(row["order"], alone)
                    self.assertEqual(sorted(row["order"]), sorted(ids))
                    self.assertEqual(
                        score_order(row["order"], M, W, full),
                        row["end_score"])

    def test_the_winner_is_the_order_of_its_row(self):
        """The winner is not stored twice with two meanings: what comes back as
        `best_order` is the row at `best_from_index`."""
        for seed in range(4):
            ids, _pool, _label, _action, _idxs, M, W, full = instance(10, 60, seed)
            best, st = multistart(declared_starts(ids), M, W, full,
                                  keep_orders=True)
            with self.subTest(seed=seed):
                self.assertEqual(st["rows"][st["best_from_index"]]["order"],
                                 best)

    def test_the_rows_do_not_share_a_list_with_the_winner(self):
        """A caller that reorders what it got back must not rewrite the record
        of the run it got it from."""
        ids, _pool, _label, _action, _idxs, M, W, full = instance(9, 50, seed=1)
        best, st = multistart(declared_starts(ids), M, W, full, keep_orders=True)
        row = st["rows"][st["best_from_index"]]["order"]
        copy = list(row)
        best.reverse()
        self.assertEqual(row, copy)


if __name__ == "__main__":
    unittest.main()
