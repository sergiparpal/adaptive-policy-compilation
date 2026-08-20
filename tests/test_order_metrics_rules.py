"""
THE PREDICTOR MAY NOT READ `T` PER CASE, AND THIS IS WHERE THAT IS A FACT.

`order_metrics_rules` scores each pair of end orders with `rho_hat`, the mean
over its disagreement set of the two winners' arrival concentration. The measured
quantity it is scored against, `touched/space`, IS the arrival density of that
same disagreement set — so a predictor allowed to intersect `D_ij` with `T` case
by case returns the answer and D-a comes out 1 by construction, having measured
nothing.

`IDEAS.md` therefore requires a test and not a promise: permuting `T` within each
rule's extension must leave `rho_hat` unchanged for every pair. The run executes
it on the real instance and stops if it fails; what is pinned here is the
property itself, on instances small enough to write out by hand, plus the two
things the real run cannot show about its own test:

  * that PERM-1 is the LITERAL form and not an approximation — the permutations
    of a space preserving every extension setwise are exactly those acting inside
    the atoms, and a mask built from them keeps every `|M_r & T|`;
  * that PERM-2 has teeth — a reshuffle preserving all the per-rule counts while
    moving mass between atoms leaves `kappa` alone and moves the per-case
    quantity, which is what tells the two predictors apart. PERM-1 cannot: a
    winner is constant on an atom, so `|D & T|` survives it too, and a test below
    SHOWS that rather than the module's docstring asserting it.

The rest is the adjudication rule — that the bands of D-a, D-b and D-c are the
ones `IDEAS.md` wrote, checked at their edges, and that none of them has a dead
zone. No measured figure is pinned: `rho_hat`'s correlation, the residual spread
and the D-c fraction live in the record and in the findings that own them, and a
second official home for a number is what this file must not become.
"""

from __future__ import annotations

import unittest
from functools import cache

from rung3.order_metrics import winners
from rung3.order_metrics_rules import (CLASS_FLOOR_DECLARED,
                                          KAPPA_DECLARED,
                                          PAIRS_BELOW_FLOOR_DECLARED,
                                          adjudicate, apply_moves, arrangement,
                                          count_preserving_reshuffle,
                                          gate_kappa, gate_territories,
                                          kappa_over_rules, mask_from_points,
                                          pair_scan, permutation_test,
                                          permute_within_atoms, points_of_mask,
                                          sweep_pairs, touch_by_atom,
                                          winners_by_atom)


# ---------------------------------------------------------------------------
# A toy whose answers are written out by hand
# ---------------------------------------------------------------------------
#
# Eight cases, four rules, `Space`'s bit convention: case i is bit n-1-i, so
# case 0 is the high bit. The extensions overlap on purpose — the whole subject
# is what happens where two rules with different actions both match.

N = 8
FULL = (1 << N) - 1
IDS = ["A", "B", "C", "D"]
POINTS = {
    "A": [0, 1, 2, 3],
    "B": [2, 3, 4, 5],
    "C": [4, 5, 6, 7],
    "D": [0, 1, 2, 3, 4, 5, 6, 7],
}
M = {rid: mask_from_points(p, N) for rid, p in POINTS.items()}
ACTION = {"A": "uno", "B": "dos", "C": "uno", "D": "tres"}


@cache
def atoms():
    return arrangement(IDS, M, N)


class TestTheBitConvention(unittest.TestCase):

    def test_mask_and_points_are_inverses(self):
        for rid, pts in POINTS.items():
            with self.subTest(rid):
                self.assertEqual(points_of_mask(M[rid], N), pts)

    def test_case_zero_is_the_high_bit(self):
        """`Space` puts case k at bit n-1-k, and every space mask in the
        repository is in that convention. A mask built the other way round would
        make every figure noise of the right shape."""
        self.assertEqual(mask_from_points([0], N), 1 << (N - 1))


class TestTheFix(unittest.TestCase):
    """The atoms: the classes of cases matched by exactly the same rules."""

    def test_the_atoms_are_the_ones_counted_by_hand(self):
        a = atoms()
        # {A,D}: 0,1 · {A,B,D}: 2,3 · {B,C,D}: 4,5 · {C,D}: 6,7
        self.assertEqual(sorted(a["points"]), [[0, 1], [2, 3], [4, 5], [6, 7]])
        self.assertEqual(sorted(a["sizes"]), [2, 2, 2, 2])

    def test_the_atoms_partition_the_space(self):
        a = atoms()
        all_ids = [i for pts in a["points"] for i in pts]
        self.assertEqual(sorted(all_ids), list(range(N)))

    def test_each_point_knows_its_atom(self):
        a = atoms()
        for k, pts in enumerate(a["points"]):
            for i in pts:
                self.assertEqual(a["atom_of_point"][i], k)

    def test_a_case_with_no_rule_is_its_own_atom(self):
        m = {"A": mask_from_points([0, 1], 4)}
        a = arrangement(["A"], m, 4)
        self.assertEqual(sorted(a["points"]), [[0, 1], [2, 3]])
        self.assertIn((), a["rules"])


class TestTheTerritories(unittest.TestCase):
    """First-match-wins, read off the matching set instead of the case."""

    def test_the_winner_is_the_first_matching_rule_in_the_order(self):
        a = atoms()
        w = winners_by_atom(["D", "A", "B", "C"], IDS, a)
        self.assertEqual({IDS[k] for k in w}, {"D"})
        w = winners_by_atom(["A", "B", "C", "D"], IDS, a)
        winner = {tuple(a["points"][i]): IDS[k] for i, k in enumerate(w)}
        self.assertEqual(winner, {(0, 1): "A", (2, 3): "A", (4, 5): "B",
                                   (6, 7): "C"})

    def test_the_territories_are_disjoint_and_cover(self):
        a = atoms()
        for order in (["A", "B", "C", "D"], ["D", "C", "B", "A"],
                      ["C", "A", "D", "B"]):
            with self.subTest(order):
                g = gate_territories(order, IDS, M, FULL, N, a,
                                     winners_by_atom(order, IDS, a))
                self.assertTrue(g["passes"])
                self.assertEqual(g["undecided"], 0)
                self.assertTrue(g["atom_route_equals_mask_route"])

    def test_the_atom_route_is_the_mask_sweep_route(self):
        """Two implementations of the same definition, and the gate is that they
        agree — the mask sweep is the one every other figure in this thread is
        built on."""
        a = atoms()
        order = ["B", "C", "A", "D"]
        w = winners_by_atom(order, IDS, a)
        terr, _und = winners(order, M, FULL)
        by_atom = {}
        for i, k in enumerate(w):
            by_atom.setdefault(IDS[k], []).extend(a["points"][i])
        self.assertEqual({r: sorted(p) for r, p in by_atom.items()},
                         {r: points_of_mask(m, N) for r, m in terr.items()})

    def test_a_case_with_no_winner_counts_as_undecided(self):
        m = {"A": mask_from_points([0, 1], 4)}
        a = arrangement(["A"], m, 4)
        w = winners_by_atom(["A"], ["A"], a)
        self.assertIn(None, w)
        g = gate_territories(["A"], ["A"], m, (1 << 4) - 1, 4, a, w)
        self.assertFalse(g["passes"])
        self.assertEqual(g["undecided"], 2)


class TestKappa(unittest.TestCase):

    def test_is_the_arrival_concentration_of_the_extension(self):
        """A rule holding half the space and all of T scores 2 over this toy:
        (4/4)/(4/8). One holding half of each scores 1."""
        t = mask_from_points([0, 1, 2, 3], N)
        k = kappa_over_rules(IDS, M, t, 4, N)
        self.assertAlmostEqual(k["A"], 2.0)
        self.assertAlmostEqual(k["B"], 1.0)
        self.assertAlmostEqual(k["C"], 0.0)
        self.assertAlmostEqual(k["D"], 1.0)

    def test_a_rule_with_no_extension_has_no_concentration(self):
        """None rather than a made-up 1.0: a rule matching nothing has no
        arrival density, and averaging it in would be inventing one."""
        k = kappa_over_rules(["Z"], {"Z": 0}, mask_from_points([0], N), 1, N)
        self.assertIsNone(k["Z"])

    def test_the_gate_compares_against_what_is_declared(self):
        """It reads the declared summary and reports each of the five, so a pool
        that is not the one the prediction was written about stops the run."""
        self.assertEqual(set(KAPPA_DECLARED),
                         {"min", "p25", "median", "p75", "max"})
        g = gate_kappa({f"r{i}": 1.0 for i in range(8)})
        self.assertFalse(g["passes"])
        self.assertEqual(g["n_with_extension"], 8)
        self.assertEqual(set(g["comparison"]), set(KAPPA_DECLARED))


class TestThePairSweep(unittest.TestCase):

    def test_rho_hat_is_the_case_weighted_mean(self):
        """Two atoms in disagreement, of 2 and 6 cases, with winner kappas
        (1, 3) and (5, 5): the mean over CASES of (kappa_i + kappa_j)/2, not
        over atoms — the six-case atom weighs three times the two-case one."""
        dis, hit, rho = pair_scan(["x", "x"], ["y", "y"], [1.0, 5.0],
                                  [3.0, 5.0], [2, 6], [1, 0])
        self.assertEqual((dis, hit), (8, 1))
        self.assertAlmostEqual(rho, (2 * 2.0 + 6 * 5.0) / 8)

    def test_the_atoms_where_they_agree_do_not_enter(self):
        dis, hit, rho = pair_scan(["x", "y"], ["x", "z"], [9.0, 1.0],
                                  [9.0, 1.0], [5, 3], [4, 2])
        self.assertEqual((dis, hit), (3, 2))
        self.assertAlmostEqual(rho, 1.0)

    def test_with_no_disagreement_there_is_no_mean(self):
        """None, not 0.0: a pair that decides everything alike has no
        disagreement set to average over."""
        self.assertEqual(pair_scan(["x"], ["x"], [1.0], [1.0], [4], [1]),
                         (0, 0, None))

    def test_the_sweep_walks_the_triangle(self):
        pairs = sweep_pairs([["a"], ["b"], ["c"]], [[1.0]] * 3, [4], [1])
        self.assertEqual([(p["i"], p["j"]) for p in pairs],
                         [(0, 1), (0, 2), (1, 2)])


class TestThePermutationTest(unittest.TestCase):
    """The blocking one. Both arms, on the toy, including what PERM-1 cannot
    catch."""

    def _montar(self, t_points, order_a, order_b):
        a = atoms()
        t = mask_from_points(t_points, N)
        k = kappa_over_rules(IDS, M, t, len(t_points), N)
        w = [winners_by_atom(o, IDS, a) for o in (order_a, order_b)]
        acts = [[ACTION[IDS[i]] for i in ww] for ww in w]
        kaps = [[k[IDS[i]] for i in ww] for ww in w]
        touch = touch_by_atom(a, t_points)
        return a, t, k, acts, kaps, touch

    def test_PERM_1_leaves_kappa_and_rho_hat_where_they_were(self):
        a, t, k, acts, kaps, touch = self._montar(
            [0, 2, 4, 6], ["A", "B", "C", "D"], ["C", "B", "A", "D"])
        pairs = sweep_pairs(acts, kaps, a["sizes"], touch)

        p1 = permute_within_atoms(a, touch, seed=17)
        t1 = mask_from_points(p1, N)
        k1 = kappa_over_rules(IDS, M, t1, t1.bit_count(), N)
        kaps1 = [[k1[IDS[i]] for i in winners_by_atom(o, IDS, a)]
                 for o in (["A", "B", "C", "D"], ["C", "B", "A", "D"])]
        pairs1 = sweep_pairs(kaps1 and acts, kaps1, a["sizes"],
                             touch_by_atom(a, p1))

        arm = permutation_test("PERM-1", "toy", k, k1, pairs, pairs1, t, t1,
                               catches=False)
        self.assertTrue(arm["kappa_identical"])
        self.assertTrue(arm["rho_hat_identical"])
        self.assertTrue(arm["passes"])
        self.assertEqual(t1.bit_count(), t.bit_count())

    def test_PERM_1_really_moves_T(self):
        """A permutation that moved nothing would pass every arm and prove
        nothing. On the toy each atom holds one of the four touched points, so
        the other half of each atom is where they can go."""
        a = atoms()
        touch = touch_by_atom(a, [0, 2, 4, 6])
        moved_ids = {tuple(permute_within_atoms(a, touch, seed=s))
                     for s in range(12)}
        self.assertGreater(len(moved_ids), 1)

    def test_PERM_1_does_NOT_catch_the_cheat(self):
        """Shown, not assumed. A winner is constant on an atom, so `D` is a
        union of atoms and `|D & T|` — the quantity a per-case predictor would
        use — is invariant under PERM-1 exactly as `rho_hat` is. It is why
        PERM-2 exists."""
        a, t, k, acts, kaps, touch = self._montar(
            [0, 2, 4, 6], ["A", "B", "C", "D"], ["C", "B", "A", "D"])
        pairs = sweep_pairs(acts, kaps, a["sizes"], touch)
        for s in range(8):
            p1 = permute_within_atoms(a, touch, seed=s)
            pairs1 = sweep_pairs(acts, kaps, a["sizes"], touch_by_atom(a, p1))
            self.assertEqual([p["disagree_touched"] for p in pairs],
                             [p["disagree_touched"] for p in pairs1])

    # A chain of three rules, so that a cancelling pair of moves exists and can
    # be checked by hand. Atoms: {P}: 0,1 · {P,Q}: 2,3 · {Q,R}: 4,5 · {R}: 6,7.
    # T = {0, 4} is one touched point in {P} and one in {Q,R}; the cancelling
    # pair for rule Q moves the first up into {P,Q} and the second down into
    # {R}, which leaves |M_P & T|, |M_Q & T| and |M_R & T| all at 1.
    CHAIN_IDS = ["P", "Q", "R"]
    CHAIN_M = {"P": mask_from_points([0, 1, 2, 3], 8),
               "Q": mask_from_points([2, 3, 4, 5], 8),
               "R": mask_from_points([4, 5, 6, 7], 8)}
    CHAIN_ACTION = {"P": "uno", "Q": "dos", "R": "uno"}
    CHAIN_T = [0, 4]

    def _chain(self):
        a = arrangement(self.CHAIN_IDS, self.CHAIN_M, 8)
        touch = touch_by_atom(a, self.CHAIN_T)
        mov, census = count_preserving_reshuffle(a, touch, 10)
        p2, detail = apply_moves(a, self.CHAIN_T, mov)
        return a, touch, mov, census, p2, detail

    def test_PERM_2_preserves_every_per_rule_count(self):
        """The reshuffle with teeth: every one of the rules' `|M_r & T|` is
        preserved exactly, so kappa cannot move."""
        a, _touch, mov, census, p2, _d = self._chain()
        self.assertTrue(mov)
        self.assertGreaterEqual(census["n_rules_with_both"], 1)
        t0 = mask_from_points(self.CHAIN_T, 8)
        t2 = mask_from_points(p2, 8)
        self.assertEqual(t2.bit_count(), len(self.CHAIN_T))
        for rid in self.CHAIN_IDS:
            with self.subTest(rid):
                self.assertEqual((self.CHAIN_M[rid] & t2).bit_count(),
                                 (self.CHAIN_M[rid] & t0).bit_count())
        self.assertEqual(kappa_over_rules(self.CHAIN_IDS, self.CHAIN_M, t0,
                                          2, 8),
                         kappa_over_rules(self.CHAIN_IDS, self.CHAIN_M, t2,
                                          2, 8))

    def test_PERM_2_moves_the_per_case_quantity_and_not_rho_hat(self):
        """The teeth themselves. T'' has the same per-rule counts and sits in
        different atoms, so `rho_hat` cannot move and a predictor reading T per
        case must — here from 0 touched points inside the disagreement set to
        1."""
        a, touch, _mov, _c, p2, _d = self._chain()
        t0 = mask_from_points(self.CHAIN_T, 8)
        t2 = mask_from_points(p2, 8)
        self.assertNotEqual(touch, touch_by_atom(a, p2))

        orders = (["P", "Q", "R"], ["Q", "R", "P"])
        w = [winners_by_atom(o, self.CHAIN_IDS, a) for o in orders]
        acts = [[self.CHAIN_ACTION[self.CHAIN_IDS[i]] for i in ww] for ww in w]
        pairs = []
        for t, n_t in ((t0, 2), (t2, 2)):
            k = kappa_over_rules(self.CHAIN_IDS, self.CHAIN_M, t, n_t, 8)
            kaps = [[k[self.CHAIN_IDS[i]] for i in ww] for ww in w]
            pairs.append(sweep_pairs(acts, kaps, a["sizes"],
                                     touch_by_atom(a, points_of_mask(t, 8))))
        arm = permutation_test("PERM-2", "toy",
                               kappa_over_rules(self.CHAIN_IDS, self.CHAIN_M,
                                                t0, 2, 8),
                               kappa_over_rules(self.CHAIN_IDS, self.CHAIN_M,
                                                t2, 2, 8),
                               pairs[0], pairs[1], t0, t2, catches=True)
        self.assertTrue(arm["kappa_identical"])
        self.assertTrue(arm["rho_hat_identical"])
        self.assertTrue(arm["disagreement_sets_untouched"])
        self.assertEqual(arm["n_pairs_whose_per_case_quantity_moved"], 1)
        self.assertTrue(arm["passes"])

    def test_a_permutation_that_moves_kappa_does_not_pass(self):
        """The failure mode the gate exists for: if the mask handed to the
        second run is not count-preserving, kappa moves and the arm fails."""
        a, t, k, acts, kaps, touch = self._montar(
            [0, 2, 4, 6], ["A", "B", "C", "D"], ["C", "B", "A", "D"])
        pairs = sweep_pairs(acts, kaps, a["sizes"], touch)
        bad = mask_from_points([0, 1, 2, 3], N)
        k_bad = kappa_over_rules(IDS, M, bad, 4, N)
        kaps_bad = [[k_bad[IDS[i]] for i in winners_by_atom(o, IDS, a)]
                    for o in (["A", "B", "C", "D"], ["C", "B", "A", "D"])]
        pairs_bad = sweep_pairs(acts, kaps_bad, a["sizes"],
                                touch_by_atom(a, [0, 1, 2, 3]))
        arm = permutation_test("roto", "toy", k, k_bad, pairs, pairs_bad, t,
                               bad, catches=True)
        self.assertFalse(arm["kappa_identical"])
        self.assertFalse(arm["passes"])


class TestTheAdjudicationRule(unittest.TestCase):
    """The bands of `IDEAS.md`, at their edges. No measured value is pinned;
    what is pinned is that the code reads the rows the way they are written —
    and that none of them has a dead zone, which the entry declares
    deliberately."""

    def _q(self, spearman=0.8, p75_p25=1.5, below=478, rho_below=400):
        return adjudicate(spearman,
                          {"p75_over_p25": p75_p25, "resumen": None, "n": 2080},
                          {"n_measured_below": below,
                           "n_rho_hat_below": rho_below},
                          CLASS_FLOOR_DECLARED)

    def test_D_a_inside_the_band_and_on_its_edges(self):
        for s in (0.75, 0.85, 0.97):
            self.assertEqual(self._q(spearman=s)["D-a"]["verdict"], "HOLDS", s)

    def test_D_a_refuted_on_both_sides(self):
        for s in (0.7499, 0.9701, 0.0, 1.0, -0.5):
            self.assertEqual(self._q(spearman=s)["D-a"]["verdict"], "REFUTED", s)

    def test_D_b_is_strict_at_its_threshold(self):
        self.assertEqual(self._q(p75_p25=1.2001)["D-b"]["verdict"], "HOLDS")
        for v in (1.20, 1.1999, 1.0):
            self.assertEqual(self._q(p75_p25=v)["D-b"]["verdict"], "REFUTED", v)

    def test_D_c_counts_three_quarters_of_the_pairs_below_the_floor(self):
        for below, rho, expected in ((478, 359, "HOLDS"), (478, 358, "REFUTED"),
                                     (4, 3, "HOLDS"), (4, 2, "REFUTED")):
            with self.subTest((below, rho)):
                q = self._q(below=below, rho_below=rho)
                self.assertEqual(q["D-c"]["verdict"], expected)

    def test_no_row_has_a_dead_zone(self):
        """The entry says so in as many words, after two rows of the previous
        sets landed between a band and its refutation line."""
        q = self._q()
        for row in ("D-a", "D-b", "D-c"):
            with self.subTest(row):
                self.assertTrue(q[row]["no_dead_zone"])
                self.assertIn(q[row]["verdict"], ("HOLDS", "REFUTED"))

    def test_what_the_entry_declared_it_derived_travels_as_a_constant(self):
        """The floor and the count below it are the entry's own, copied with
        their source so that a run that does not reproduce them is visible."""
        self.assertEqual(CLASS_FLOOR_DECLARED, 0.1952)
        self.assertEqual(PAIRS_BELOW_FLOOR_DECLARED, 478)
        q = self._q()
        self.assertEqual(q["D-c"]["n_pairs_below_declared"], 478)


if __name__ == "__main__":
    unittest.main()
