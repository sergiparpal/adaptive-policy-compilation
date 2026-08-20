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
ACTION_LIST = ("A", "B", "C")


def mask(cases):
    """A mask from case indices, which is how every expectation below is
    written: the bit convention is the one `build_masks` uses."""
    m = 0
    for i in cases:
        m |= 1 << i
    return m


def instance(n_rules, n_cases, seed, p_match=0.35):
    """A random synthetic instance, with the pool kept so that the naive
    reference can be written without touching a mask."""
    rng = random.Random(seed)
    ids = [f"X{k:03d}" for k in range(n_rules)]
    action = {rid: rng.choice(ACTION_LIST) for rid in ids}
    pool = [[rid for rid in ids if rng.random() < p_match]
            for _ in range(n_cases)]
    M = {rid: 0 for rid in ids}
    for i, matching in enumerate(pool):
        for rid in matching:
            M[rid] |= 1 << i
    return ids, pool, action, M, (1 << n_cases) - 1


def decide_naive(order, pool, action):
    """First-match-wins, case by case, the obvious way: what each case is
    decided to be, or None if no rule matched it."""
    rank = {rid: k for k, rid in enumerate(order)}
    return [action[min(p, key=lambda rid: rank[rid])] if p else None
            for p in pool]


def shuffled_order(ids, seed):
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

def three_rules(n_cases=4):
    ids = ["R0", "R1", "R2"]
    action = {"R0": "A", "R1": "B", "R2": "A"}
    M = {"R0": mask([0, 1]), "R1": mask([1, 2]), "R2": mask([2, 3])}
    return ids, M, action, mask(range(n_cases))


class TestTheHandWrittenTable(unittest.TestCase):

    def test_the_design_order_decides_what_the_table_says(self):
        ids, M, action, full = three_rules()
        d, undecided = decisions(ids, M, action, full)
        self.assertEqual(d, {"A": mask([0, 1, 3]), "B": mask([2])})
        self.assertEqual(undecided, 0)

    def test_promoting_R1_takes_case_1_from_R0(self):
        ids, M, action, full = three_rules()
        d, undecided = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(d, {"A": mask([0, 3]), "B": mask([1, 2])})
        self.assertEqual(undecided, 0)

    def test_the_distance_between_those_two_is_exactly_case_1(self):
        ids, M, action, full = three_rules()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 0))
        _agree, dis, _und = agreement_masks(dA, dB, full)
        self.assertEqual(dis, mask([1]))

    def test_moving_R2_to_the_front_changes_nothing(self):
        """R2 and R0 share no case and R2 only outranks R1 on case 2, which R1
        would have taken — so this is a real reordering with no decision behind
        it, on the smallest instance where that can happen."""
        ids, M, action, full = three_rules()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R0", "R2", "R1"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 0))
        _a, dis, _u = agreement_masks(dA, dB, full)
        self.assertEqual(dis, mask([2]))

    def test_the_truth_classes_are_counted_where_they_belong(self):
        """`truth` is by class, and a class the two orders never disagree on
        must come back at rate 0 rather than absent."""
        ids, M, action, full = three_rules()
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        # cases 0 and 1 are truly A, cases 2 and 3 truly B
        truth = {"A": mask([0, 1]), "B": mask([2, 3])}
        by_class = per_class_disagreement(dA, dB, truth)
        self.assertEqual(by_class["A"], {"n": 2, "disagree": 1, "rate": 0.5,
                                         "undecided_either": 0})
        self.assertEqual(by_class["B"], {"n": 2, "disagree": 0, "rate": 0.0,
                                         "undecided_either": 0})


class TestWhatNobodyMatches(unittest.TestCase):
    """The undecided branch: 'no rule matched' is not a disagreement, and the
    two are not to be averaged together."""

    def test_a_case_with_no_rule_is_left_undecided(self):
        ids, M, action, full = three_rules(n_cases=5)     # case 4 matches nothing
        d, undecided = decisions(ids, M, action, full)
        self.assertEqual(undecided, mask([4]))
        self.assertEqual(d, {"A": mask([0, 1, 3]), "B": mask([2])})

    def test_counts_as_neither_disagreement_nor_agreement(self):
        ids, M, action, full = three_rules(n_cases=5)
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0", "R2"], M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (3, 1, 1))

    def test_an_empty_order_leaves_everything_undecided(self):
        _ids, M, action, full = three_rules()
        d, undecided = decisions([], M, action, full)
        self.assertEqual((d, undecided), ({}, full))
        self.assertEqual(behavioural_distance(d, d, full), (0, 0, 4))

    def test_the_three_quantities_partition_the_space(self):
        """The invariant that makes the triple readable: nothing is counted
        twice and nothing is lost."""
        for seed in range(10):
            ids, pool, action, M, full = instance(9, 40, seed, p_match=0.2)
            dA, _ = decisions(shuffled_order(ids, seed), M, action, full)
            dB, _ = decisions(shuffled_order(ids, 100 + seed), M, action, full)
            with self.subTest(seed=seed):
                self.assertEqual(sum(behavioural_distance(dA, dB, full)), 40)
                masks = agreement_masks(dA, dB, full)
                self.assertEqual(masks[0] | masks[1] | masks[2], full)
                self.assertEqual(masks[0] & masks[1], 0)
                self.assertEqual(masks[0] & masks[2], 0)
                self.assertEqual(masks[1] & masks[2], 0)


class TestAgainstTheNaiveWalk(unittest.TestCase):
    """The bitmask sweep against a walk that reads the pool case by case and
    knows nothing about masks."""

    def test_decisions_reproduces_the_case_by_case_walk(self):
        for seed in range(12):
            ids, pool, action, M, full = instance(10, 50, seed)
            order = shuffled_order(ids, seed)
            expected = decide_naive(order, pool, action)
            d, undecided = decisions(order, M, action, full)
            with self.subTest(seed=seed):
                for a in ACTION_LIST:
                    self.assertEqual(
                        d.get(a, 0),
                        mask([i for i, v in enumerate(expected) if v == a]))
                self.assertEqual(
                    undecided,
                    mask([i for i, v in enumerate(expected) if v is None]))

    def test_the_distance_reproduces_the_case_by_case_comparison(self):
        for seed in range(12):
            ids, pool, action, M, full = instance(10, 50, seed)
            a = shuffled_order(ids, seed)
            b = shuffled_order(ids, 500 + seed)
            goes, vb = decide_naive(a, pool, action), decide_naive(b, pool, action)
            expected = (
                sum(1 for x, y in zip(goes, vb) if x is not None and x == y),
                sum(1 for x, y in zip(goes, vb)
                    if x is not None and y is not None and x != y),
                sum(1 for x, y in zip(goes, vb) if x is None or y is None),
            )
            dA, _ = decisions(a, M, action, full)
            dB, _ = decisions(b, M, action, full)
            with self.subTest(seed=seed):
                self.assertEqual(behavioural_distance(dA, dB, full), expected)


class TestIdentityAndSymmetry(unittest.TestCase):

    def test_an_order_does_not_differ_from_itself(self):
        for seed in range(10):
            ids, _pool, action, M, full = instance(9, 40, seed)
            d, und = decisions(shuffled_order(ids, seed), M, action, full)
            agree, dis, undecided = behavioural_distance(d, d, full)
            with self.subTest(seed=seed):
                self.assertEqual(dis, 0)
                self.assertEqual(undecided, und.bit_count())
                self.assertEqual(agree + undecided, 40)

    def test_the_distance_is_symmetric(self):
        for seed in range(10):
            ids, _pool, action, M, full = instance(9, 40, seed)
            dA, _ = decisions(shuffled_order(ids, seed), M, action, full)
            dB, _ = decisions(shuffled_order(ids, 900 + seed), M, action, full)
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

def single_conflict_instance():
    ids = ["R0", "R1", "R2", "R3", "R4", "R5"]
    action = {"R0": "A", "R1": "A", "R2": "B", "R3": "B", "R4": "C", "R5": "C"}
    M = {"R0": mask([0, 1, 7]), "R1": mask([1, 2]),
         "R2": mask([3, 7]), "R3": mask([3, 4]),
         "R4": mask([5]), "R5": mask([6])}
    return ids, M, action, mask(range(8))


class TestThePropertyThatMotivatesTheInstrument(unittest.TestCase):
    """Two orders differing only in non-conflicting pairs are the same machine,
    however far apart they look positionally. It is the whole argument for
    measuring behaviour instead of rank, and P3 pins it again on the 29 hidden
    rules, where the pairs are not hand-picked."""

    def test_only_a_pair_can_change_a_decision(self):
        ids, M, action, _full = single_conflict_instance()
        self.assertEqual(conflicting_pairs(ids, M, action), {("R0", "R2")})
        self.assertEqual(pair_census(ids, M, action),
                         {"pairs": 15, "co_match": 3, "conflicting": 1,
                          "same_action": 2})

    def test_permuting_only_free_pairs_leaves_the_machine_intact(self):
        ids, M, action, full = single_conflict_instance()
        other = ["R1", "R0", "R3", "R2", "R5", "R4"]     # R0 still comes before R2
        dA, uA = decisions(ids, M, action, full)
        dB, uB = decisions(other, M, action, full)

        self.assertEqual(behavioural_distance(dA, dB, full)[1], 0)
        self.assertEqual(signature(dA, uA), signature(dB, uB))

        churn = positions_moved(ids, other)
        self.assertEqual(churn["moved"], 6)             # every rule moved
        self.assertEqual(churn["fraction_moved"], 1.0)

        pairs = conflicting_pairs(ids, M, action)
        self.assertLess(tau(ids, other), 1.0)            # rank says they differ
        self.assertEqual(tau(ids, other, pairs), 1.0)    # restricted says they do not

    def test_inverting_the_conflicting_pair_does_change_a_decision(self):
        """The control: the same instance, the one pair that is not free."""
        ids, M, action, full = single_conflict_instance()
        other = ["R2", "R1", "R0", "R3", "R4", "R5"]
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(other, M, action, full)
        self.assertEqual(behavioural_distance(dA, dB, full), (7, 1, 0))
        self.assertEqual(tau(ids, other, conflicting_pairs(ids, M, action)), -1.0)


class TestPairsInConflict(unittest.TestCase):

    def test_equals_the_double_loop_over_the_pool(self):
        """Brute force from the pool, which never looks at a mask: a pair
        conflicts when some case lists both and the actions differ."""
        for seed in range(10):
            ids, pool, action, M, _full = instance(12, 60, seed)
            bruto = set()
            for a, b in combinations(sorted(ids), 2):
                if action[a] == action[b]:
                    continue
                if any(a in p and b in p for p in pool):
                    bruto.add((a, b))
            with self.subTest(seed=seed):
                self.assertEqual(conflicting_pairs(ids, M, action), bruto)

    def test_the_census_adds_up_with_the_set(self):
        for seed in range(8):
            ids, _pool, action, M, _full = instance(11, 50, seed)
            census = pair_census(ids, M, action)
            with self.subTest(seed=seed):
                self.assertEqual(census["conflicting"],
                                 len(conflicting_pairs(ids, M, action)))
                self.assertEqual(census["co_match"],
                                 census["conflicting"] + census["same_action"])
                self.assertLessEqual(census["co_match"], census["pairs"])
                self.assertEqual(census["pairs"], 11 * 10 // 2)

    def test_one_and_the_same_action_is_never_in_conflict(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "A"}
        M = {"R0": mask([0, 1]), "R1": mask([0, 1])}
        self.assertEqual(conflicting_pairs(ids, M, action), set())

    def test_nor_without_cases_in_common(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "B"}
        M = {"R0": mask([0]), "R1": mask([1])}
        self.assertEqual(conflicting_pairs(ids, M, action), set())


class TestTau(unittest.TestCase):

    @staticmethod
    def tau_naive(a, b, pairs=None):
        ra = {x: k for k, x in enumerate(a)}
        rb = {x: k for k, x in enumerate(b)}
        pairs = list(combinations(a, 2)) if pairs is None else list(pairs)
        ctx = sum(1 for x, y in pairs if (ra[x] < ra[y]) == (rb[x] < rb[y]))
        return (ctx - (len(pairs) - ctx)) / len(pairs)

    def test_equals_brute_force_over_every_pair(self):
        for seed in range(20):
            ids = [f"X{k:03d}" for k in range(8)]
            a = shuffled_order(ids, seed)
            b = shuffled_order(ids, 300 + seed)
            with self.subTest(seed=seed):
                self.assertAlmostEqual(tau(a, b), self.tau_naive(a, b))

    def test_equals_brute_force_over_a_given_set(self):
        rng = random.Random(7)
        for seed in range(20):
            ids = [f"X{k:03d}" for k in range(8)]
            a = shuffled_order(ids, seed)
            b = shuffled_order(ids, 400 + seed)
            all_ids = list(combinations(sorted(ids), 2))
            pairs = set(rng.sample(all_ids, rng.randint(1, len(all_ids))))
            with self.subTest(seed=seed):
                self.assertAlmostEqual(tau(a, b, pairs),
                                       self.tau_naive(a, b, pairs))

    def test_with_itself_it_is_one_and_with_the_reverse_minus_one(self):
        ids = [f"X{k:03d}" for k in range(8)]
        self.assertEqual(tau(ids, ids), 1.0)
        self.assertEqual(tau(ids, list(reversed(ids))), -1.0)

    def test_the_order_of_the_pair_does_not_matter(self):
        ids = [f"X{k:03d}" for k in range(8)]
        a, b = shuffled_order(ids, 1), shuffled_order(ids, 2)
        pairs = {("X000", "X003"), ("X002", "X005")}
        self.assertEqual(tau(a, b, pairs),
                         tau(a, b, {(y, x) for x, y in pairs}))

    def test_with_no_pairs_to_correlate_it_returns_nan(self):
        self.assertTrue(math.isnan(tau(["R0"], ["R0"])))
        self.assertTrue(math.isnan(tau([], [])))
        self.assertTrue(math.isnan(tau(["R0", "R1"], ["R1", "R0"], set())))

    def test_requires_two_permutations_of_the_same_set(self):
        with self.assertRaises(ValueError):
            tau(["R0", "R1"], ["R0", "R2"])
        with self.assertRaises(ValueError):
            tau(["R0", "R1", "R1"], ["R1", "R0", "R1"])


class TestPositionsMoved(unittest.TestCase):

    def test_with_itself_it_moves_nothing(self):
        ids = [f"X{k:03d}" for k in range(6)]
        m = positions_moved(ids, ids)
        self.assertEqual((m["moved"], m["max"], m["total"]), (0, 0, 0))
        self.assertEqual(m["fraction_moved"], 0.0)

    def test_the_reverse_moves_everything_but_the_centre(self):
        ids = [f"X{k:03d}" for k in range(5)]
        m = positions_moved(ids, list(reversed(ids)))
        self.assertEqual(m["moved"], 4)                 # the middle one stays put
        self.assertEqual(m["max"], 4)
        self.assertEqual(m["displacement"]["X000"], 4)
        self.assertEqual(m["displacement"]["X004"], -4)
        self.assertEqual(m["total"], 4 + 2 + 0 + 2 + 4)
        self.assertEqual(m["median"], 2)

    def test_requires_two_permutations_of_the_same_set(self):
        with self.assertRaises(ValueError):
            positions_moved(["R0", "R1"], ["R0", "R2"])


class TestAttribution(unittest.TestCase):
    """Two rules with the same action decide a case the same way. Measuring
    agreement by which rule fired would report a difference a deployed system
    would not show — so the two quantities are computed separately, and this is
    the instance where they come apart."""

    def test_they_decide_alike_and_yet_a_different_rule_fires(self):
        ids = ["R0", "R1"]
        action = {"R0": "A", "R1": "A"}
        M = {"R0": mask([0, 1]), "R1": mask([0, 1])}
        full = mask([0, 1])
        dA, _ = decisions(ids, M, action, full)
        dB, _ = decisions(["R1", "R0"], M, action, full)
        agree, dis, und = behavioural_distance(dA, dB, full)
        self.assertEqual((agree, dis, und), (2, 0, 0))

        wA, _ = winners(ids, M, full)
        wB, _ = winners(["R1", "R0"], M, full)
        self.assertEqual(wA, {"R0": full})
        self.assertEqual(wB, {"R1": full})
        self.assertEqual(attribution_agreement(wA, wB), 0)

    def test_the_attribution_is_contained_in_the_agreement(self):
        """A case won by the same rule in both orders is decided by the same
        action in both, so restricting the attribution to the agreement mask can
        never remove anything. What the two quantities measure is the SHORTFALL
        between them: agreeing for different reasons."""
        for seed in range(10):
            ids, _pool, action, M, full = instance(9, 40, seed, p_match=0.2)
            a = shuffled_order(ids, seed)
            b = shuffled_order(ids, 600 + seed)
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

    def test_it_restricts_to_the_mask_it_is_given(self):
        """Case 2 is won by R1 in both orders even though R1 moved, so the
        attribution is cases 0, 2 and 3; restricted to case 0 it is one."""
        ids, M, action, full = three_rules()
        other = ["R1", "R0", "R2"]
        wA, _ = winners(ids, M, full)
        wB, _ = winners(other, M, full)
        self.assertEqual(attribution_agreement(wA, wB), 3)
        self.assertEqual(attribution_agreement(wA, wB, mask([0])), 1)
        self.assertEqual(attribution_agreement(wA, wB, mask([1])), 0)

    def test_the_winners_partition_the_space_just_as_the_decisions_do(self):
        for seed in range(8):
            ids, _pool, action, M, full = instance(9, 40, seed, p_match=0.2)
            o = shuffled_order(ids, seed)
            d, ud = decisions(o, M, action, full)
            w, uw = winners(o, M, full)
            with self.subTest(seed=seed):
                self.assertEqual(ud, uw)
                joined = 0
                for m in w.values():
                    joined |= m
                self.assertEqual(joined, full & ~uw)


class TestSignature(unittest.TestCase):

    def test_is_equal_exactly_when_they_decide_the_same(self):
        for seed in range(10):
            ids, _pool, action, M, full = instance(9, 40, seed)
            a = shuffled_order(ids, seed)
            b = shuffled_order(ids, 700 + seed)
            fa = signature(*decisions(a, M, action, full))
            fb = signature(*decisions(b, M, action, full))
            dA, _ = decisions(a, M, action, full)
            dB, _ = decisions(b, M, action, full)
            equal_ones = behavioural_distance(dA, dB, full)[1] == 0
            with self.subTest(seed=seed):
                self.assertEqual(fa == fb, equal_ones)

    def test_is_hashable_and_does_not_depend_on_key_order(self):
        _ids, M, action, full = three_rules()
        d, und = decisions(["R0", "R1", "R2"], M, action, full)
        self.assertEqual(len({signature(d, und),
                              signature(dict(reversed(list(d.items()))), und)}),
                         1)

    def test_an_action_deciding_nothing_does_not_change_the_signature(self):
        """Whether a caller's dict carries an empty entry is an accident of how
        it was built, not a difference in behaviour."""
        d = {"A": mask([0, 1]), "B": 0}
        self.assertEqual(signature(d, 0), signature({"A": mask([0, 1])}, 0))


class TestTheInstrumentIsPure(unittest.TestCase):
    """§1 of the plan: no oracle, no corpus, no JSON, nothing about optimizers.
    `tests/test_oracle_separation.py` already fails if the oracle appears; this
    is the wider claim, and it is what lets the same code measure a toy and the
    exhaustive space."""

    def test_imports_nothing_from_the_repository(self):
        tree = ast.parse((REPO / "rung3" / "order_metrics.py").read_text())
        modulos = set()
        for nodo in ast.walk(tree):
            if isinstance(nodo, ast.Import):
                modulos.update(a.name.split(".")[0] for a in nodo.names)
            elif isinstance(nodo, ast.ImportFrom):
                modulos.add((nodo.module or "").split(".")[0])
        self.assertEqual(modulos & {"harness", "rung2", "rung3",
                                    "rung4", "run_experiment", "json"},
                         set())

    def test_writes_nothing(self):
        src = (REPO / "rung3" / "order_metrics.py").read_text()
        for forbidden in ("write_text", "open(", "Path("):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, src)


if __name__ == "__main__":
    unittest.main()
