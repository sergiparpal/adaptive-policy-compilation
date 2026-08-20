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
from rung3.order_metrics_touched import (CLASS_C_A, TOUCHED_PUBLISHED,
                                            adjudicate, partitions,
                                            ratio_summary, restrict, sign,
                                            touched_mask)
from rung3.order_search_ls import space_truth_masks


@cache
def space():
    return Space()


@cache
def instance():
    return load_instance()


@cache
def mask_and_census():
    return touched_mask(instance()["corpus"], space())


@cache
def truth():
    return space_truth_masks(space())


class TestTheTouchedPointsMask(unittest.TestCase):

    def test_has_the_bits_the_record_publishes(self):
        """1,743 distinct cases: a fact about the corpus and the domain, and the
        one published figure that pins this mask."""
        m, census = mask_and_census()
        self.assertEqual(m.bit_count(), TOUCHED_PUBLISHED)
        self.assertEqual(census["n_distinct_points"], TOUCHED_PUBLISHED)

    def test_the_census_adds_up_with_the_corpus(self):
        _m, census = mask_and_census()
        inst = instance()
        self.assertEqual(census["n_corpus_draws"], len(inst["corpus"]))
        self.assertEqual(census["n_space"], space().n)
        self.assertEqual(
            sum(int(k) * v
                for k, v in census["points_by_multiplicity"].items()),
            len(inst["corpus"]))
        self.assertEqual(sum(census["points_by_multiplicity"].values()),
                         census["n_distinct_points"])

    def test_is_inside_the_space(self):
        m, _c = mask_and_census()
        self.assertEqual(m & ~space().full, 0)

    def test_a_case_outside_the_space_blows_up_instead_of_falling_through(self):
        """A corpus case the enumeration does not contain would be a broken
        domain, and dropping it silently would shrink the denominator."""
        class Fake:
            def key(self):
                return ("no", "such", "case")

        with self.assertRaises(ValueError):
            touched_mask([Fake()], space())

    def test_each_corpus_case_sets_its_bit_in_the_Space_convention(self):
        """Bit n-1-i for case i of `all_cases()`, which is what `Space` builds
        and therefore what every space mask in the repository is in."""
        m, _c = mask_and_census()
        index = {c.key(): i for i, c in enumerate(all_cases())}
        n = space().n
        for case in instance()["corpus"][:50]:
            i = index[case.key()]
            self.assertTrue(m >> (n - 1 - i) & 1)


class TestTheConventionIsChecked(unittest.TestCase):
    """The check the partition cannot make."""

    def _distinct_by_class(self):
        """Distinct corpus cases by label, from the corpus side alone: no mask,
        no space."""
        inst = instance()
        seen = {}
        for i, case in enumerate(inst["corpus"]):
            seen.setdefault(inst["truth"][i], set()).add(case.key())
        return {c: len(v) for c, v in seen.items()}

    def test_the_per_class_sizes_agree_by_two_routes(self):
        m, _c = mask_and_census()
        expected = self._distinct_by_class()
        for c, mask in truth().items():
            with self.subTest(c):
                self.assertEqual((mask & m).bit_count(), expected.get(c, 0))

    def test_the_inverted_convention_fails_that_check(self):
        """Shown, not assumed: the reversed mask has the same 1,743 bits and
        still partitions, and the class sizes are what tells it apart."""
        inst = instance()
        n = space().n
        index = {c.key(): i for i, c in enumerate(all_cases())}
        reversed_order = 0
        for i in {index[c.key()] for c in inst["corpus"]}:
            reversed_order |= 1 << i

        self.assertEqual(reversed_order.bit_count(), TOUCHED_PUBLISHED)
        self.assertTrue(partitions(restrict(truth(), reversed_order), reversed_order))

        expected = self._distinct_by_class()
        equal_ones = sum(1 for c, mask in truth().items()
                         if (mask & reversed_order).bit_count() == expected.get(c, 0))
        self.assertLess(equal_ones, len(truth()))
        self.assertNotEqual(reversed_order, mask_and_census()[0])
        # and n-1-i is not i for any case here, so the two masks are never the
        # same object by accident
        self.assertGreater(n, 1)


class TestTheClassMasksPartition(unittest.TestCase):

    def test_they_partition_the_space(self):
        self.assertTrue(partitions(truth(), space().full))

    def test_they_partition_the_touched_mask(self):
        m, _c = mask_and_census()
        self.assertTrue(partitions(restrict(truth(), m), m))

    def test_restrict_takes_no_bits_out_of_the_mask(self):
        m, _c = mask_and_census()
        for c, mask in restrict(truth(), m).items():
            with self.subTest(c):
                self.assertEqual(mask & ~m, 0)

    def test_partitions_rejects_overlap_and_gap(self):
        self.assertTrue(partitions({"a": 0b1100, "b": 0b0011}, 0b1111))
        self.assertFalse(partitions({"a": 0b1100, "b": 0b0111}, 0b1111))
        self.assertFalse(partitions({"a": 0b1000, "b": 0b0011}, 0b1111))


class TestTheSignAndTheReasons(unittest.TestCase):

    def test_sign_tells_zero_apart(self):
        self.assertEqual((sign(-2), sign(0), sign(0.5)), (-1, 0, 1))

    def test_ratio_summary_discards_a_zero_denominator(self):
        pairs = [{"a": 1.0, "b": 2.0}, {"a": 3.0, "b": 0.0},
                 {"a": 1.0, "b": 4.0}]
        r = ratio_summary(pairs, "a", "b")
        self.assertEqual(r["n"], 2)
        self.assertEqual(r["n_dropped_zero_denominator"], 1)
        self.assertEqual(r["resumen"]["min"], 0.25)
        self.assertEqual(r["resumen"]["max"], 0.5)


class TestTheAdjudicationRule(unittest.TestCase):
    """The bands and refutation lines of `IDEAS.md`, at their boundaries. No
    measured value is pinned; what is pinned is that the code reads the rows the
    way they are written."""

    CLASSES = ("ACCOUNT_MANAGER", "BILLING_SPECIALIST", "ONCALL_ESCALATION",
               "SECURITY_INCIDENT", "SELF_SERVICE_DEFLECT", "T1_GENERAL",
               "T2_TECHNICAL", "T3_ENGINEERING")

    def _rates(self, objective_f):
        """Eight classes whose `f` is `objective_f`."""
        return {c: {"all": 1.0, "arrivals": 0.0, "touched": 1.0 - objective_f}
                for c in self.CLASSES}

    def _q(self, objective_f=0.8, rates=None):
        rates = self._rates(objective_f) if rates is None else rates
        p = {c: 1 / len(rates) for c in rates}
        reasons = {"touched_over_space": ratio_summary(
            [{"a": 1.0, "b": 2.0}], "a", "b")}
        return adjudicate(rates, p, reasons)

    def test_C_a_inside_the_band_and_on_its_edges(self):
        for f in (0.60, 0.75, 0.95):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "HOLDS", f)

    def test_C_a_in_the_dead_zone(self):
        for f in (0.40, 0.599, 0.951, 1.10):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "NEITHER", f)

    def test_C_a_refuted_outside(self):
        for f in (0.399, 1.101, -0.2, 2.0):
            self.assertEqual(self._q(f)["C-a"]["verdict"], "REFUTED", f)

    def test_C_a_admits_f_outside_zero_one(self):
        """The row says so explicitly: f outside [0, 1] is a result, not an
        error."""
        q = self._q(1.05)
        self.assertEqual(q["C-a"]["f"], 1.05)
        self.assertEqual(len(q["C-a"]["f_outside_unit_interval"]), 8)

    def test_C_b_counts_the_signs(self):
        """Both go down together = a match; touched up while arrivals down = a
        mismatch. C-b counts classes and nothing else, so this is independent of
        C-a's f."""
        equal = {"all": 0.2, "touched": 0.1, "arrivals": 0.05}
        different = {"all": 0.2, "touched": 0.3, "arrivals": 0.05}
        for n_ok, expected in ((8, "HOLDS"), (6, "HOLDS"), (5, "NEITHER"),
                               (4, "REFUTED"), (0, "REFUTED")):
            rates = {c: dict(equal if k < n_ok else different)
                     for k, c in enumerate(self.CLASSES)}
            with self.subTest(n_ok):
                q = self._q(rates=rates)
                self.assertEqual(q["C-b"]["n_matching"], n_ok)
                self.assertEqual(q["C-b"]["verdict"], expected)

    def test_C_b_sees_the_zero_sign_as_its_own_case(self):
        """`touched == all` matches only if `arrivals == all` too: a rate that
        does not move is not the same event as one that moves the other way."""
        unmoved = {"all": 0.2, "touched": 0.2, "arrivals": 0.05}
        q = self._q(rates={c: dict(unmoved) for c in self.CLASSES})
        self.assertEqual(q["C-b"]["n_matching"], 0)
        self.assertEqual(q["C-b"]["by_class"][CLASS_C_A]["sign_touched"], 0)
        self.assertEqual(q["C-b"]["by_class"][CLASS_C_A]["sign_arrivals"], -1)

    def test_C_c_inside_its_band_and_outside(self):
        for value, expected in ((0.043, "HOLDS"), (0.0575, "HOLDS"),
                                (0.072, "HOLDS"), (0.035, "NEITHER"),
                                (0.090, "NEITHER"), (0.0349, "REFUTED"),
                                (0.0901, "REFUTED")):
            rates = {c: {"all": 0.2, "touched": value, "arrivals": 0.05}
                     for c in self.CLASSES}
            with self.subTest(value):
                q = self._q(0.0, rates=rates)
                self.assertEqual(q["C-c"]["value"], value)
                self.assertEqual(q["C-c"]["verdict"], expected)

    def test_C_d_does_not_adjudicate(self):
        q = self._q(0.8)
        self.assertFalse(q["C-d"]["adjudicates"])
        self.assertNotIn("verdict", q["C-d"])


if __name__ == "__main__":
    unittest.main()
