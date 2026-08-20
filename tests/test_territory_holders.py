"""
THE GATES OF `territory_holders`, AND ONLY THE GATES.

That module publishes one primitive — which rules hold territory under each of
the 65 end orders of split 0 — and a derived block that is a lookup of a figure
another record owns. **No measured value of the finding is pinned here.** How
many rules the union holds, what kappa does over it, and whether the rule at
kappa's ceiling ever decides a case live in `results3/territory_holders.json` and
in the erratum in `FINDINGS_ORDERS.md`; repeating any of them in a test would
give a figure a second owner, which is the failure this repository already
decided not to commit (`IDEAS.md`, technical debt, the test that was considered
and deliberately not written).

What is pinned instead: that `holders` reads first-match-wins the way the rest of
the thread does, that the two gates this module adds are blocking and detect the
failures they exist for, and that the derived block is the arithmetic it claims —
all on instances small enough to write the answer out by hand.
"""

from __future__ import annotations

import unittest

from rung3.order_metrics_rules import mask_from_points
from rung3.territory_holders import (N_ORDERS, derive, gate_counts,
                                        gate_kappa_read, holders,
                                        territory_table)

# Eight cases, four rules, `Space`'s bit convention: case i is bit n-1-i.
N = 8
FULL = (1 << N) - 1
M = {
    "A": mask_from_points([0, 1, 2, 3], N),
    "B": mask_from_points([2, 3, 4, 5], N),
    "C": mask_from_points([4, 5, 6, 7], N),
    "D": mask_from_points([0, 1, 2, 3, 4, 5, 6, 7], N),
}


class TestThePrimitive(unittest.TestCase):

    def test_territory_goes_to_whoever_matches_first(self):
        """A, B and C between them cover everything, so D — last and universal —
        wins nothing at all. That is the shape of the fact being audited."""
        ids, undecided = holders(["A", "B", "C", "D"], M, FULL)
        self.assertEqual(ids, ["A", "B", "C"])
        self.assertEqual(undecided, 0)

    def test_a_universal_rule_in_front_leaves_all_the_rest_with_nothing(self):
        ids, _u = holders(["D", "A", "B", "C"], M, FULL)
        self.assertEqual(ids, ["D"])

    def test_the_ids_come_out_sorted(self):
        ids, _u = holders(["C", "A", "B"], M, FULL)
        self.assertEqual(ids, sorted(ids))

    def test_what_nobody_matches_counts_as_undecided(self):
        partial = {"A": M["A"]}
        ids, undecided = holders(["A"], partial, FULL)
        self.assertEqual(ids, ["A"])
        self.assertEqual(undecided, 4)

    def test_the_table_carries_one_row_per_order(self):
        rows = territory_table([["A", "B", "C", "D"], ["D", "A", "B", "C"]],
                               M, FULL)
        self.assertEqual([f["order"] for f in rows], [0, 1])
        self.assertEqual([f["n_rules_with_territory"] for f in rows], [3, 1])
        self.assertEqual(rows[0]["rule_ids"], ["A", "B", "C"])


class TestTheKappaGate(unittest.TestCase):
    """kappa is READ from the record that owns it; the gate is that the values
    read still reproduce the summary published beside them."""

    def _rec(self, kappa, summary):
        return {"kappa_by_rule": kappa, "kappa_summary": summary}

    def test_passes_when_the_values_reproduce_the_summary(self):
        kappa = {f"R{i:04d}": float(i) for i in range(1, 9)}
        summary = {"n": 8, "min": 1.0, "p25": 3.0, "median": 4.5, "mean": 4.5,
                   "p75": 7.0, "max": 8.0}
        read_back, g = gate_kappa_read(self._rec(kappa, summary))
        self.assertTrue(g["passes"])
        self.assertEqual(read_back, kappa)
        self.assertEqual(g["n_rules"], 8)

    def test_fails_if_the_published_summary_does_not_add_up(self):
        kappa = {f"R{i:04d}": float(i) for i in range(1, 9)}
        summary = {"n": 8, "min": 1.0, "p25": 3.0, "median": 4.5, "mean": 4.5,
                   "p75": 7.0, "max": 9.0}          # the ceiling is wrong
        _read_back, g = gate_kappa_read(self._rec(kappa, summary))
        self.assertFalse(g["passes"])
        self.assertFalse(g["comparison"]["max"][2])

    def test_ignores_rules_with_no_concentration(self):
        """A rule with an empty extension has no arrival density and the record
        stores None for it; it must not enter the summary as a zero."""
        kappa = {"R0001": 1.0, "R0002": 3.0, "R0003": None}
        read_back, _g = gate_kappa_read(self._rec(kappa, {}))
        self.assertEqual(set(read_back), {"R0001", "R0002"})


class TestTheCountsGate(unittest.TestCase):
    """The count per order against the territory gate the earlier record already
    passed: it is what says these are the same territories."""

    def _rec(self, counts):
        return {"gates": {"territories": {"per_order": [
            {"order": k, "n_rules_with_territory": n}
            for k, n in enumerate(counts)]}}}

    def _rows(self, counts):
        return [{"order": k, "n_rules_with_territory": n, "rule_ids": []}
                for k, n in enumerate(counts)]

    def test_passes_when_they_agree_order_by_order(self):
        tallies = [30 + (k % 7) for k in range(N_ORDERS)]
        g = gate_counts(self._rows(tallies), self._rec(tallies))
        self.assertTrue(g["passes"])
        self.assertEqual(g["orders_that_differ"], [])

    def test_fails_if_a_single_order_disagrees(self):
        tallies = [30 + (k % 7) for k in range(N_ORDERS)]
        published_rates = list(tallies)
        published_rates[17] += 1
        g = gate_counts(self._rows(tallies), self._rec(published_rates))
        self.assertFalse(g["passes"])
        self.assertEqual([f["order"] for f in g["orders_that_differ"]], [17])

    def test_fails_if_orders_are_missing(self):
        """Fewer than the 65 the set has is a different set, not a subset to be
        compared on what happens to overlap."""
        tallies = [30] * (N_ORDERS - 1)
        g = gate_counts(self._rows(tallies), self._rec(tallies))
        self.assertFalse(g["passes"])

    def test_fails_if_the_record_does_not_publish_that_order(self):
        tallies = [30] * N_ORDERS
        rec = self._rec(tallies[:-1])
        g = gate_counts(self._rows(tallies), rec)
        self.assertFalse(g["passes"])


class TestTheDerivedBlock(unittest.TestCase):
    """Arithmetic on synthetic inputs. Nothing here is a figure of the
    finding."""

    KAPPA = {"A": 1.0, "B": 2.0, "C": 10.0, "Z": 40.0}

    def _rows(self):
        return [{"order": 0, "n_rules_with_territory": 2, "rule_ids": ["A", "B"]},
                {"order": 1, "n_rules_with_territory": 3,
                 "rule_ids": ["A", "B", "C"]}]

    def test_the_union_is_the_union_of_the_sets(self):
        d = derive(self._rows(), self.KAPPA, 40.0)
        u = d["union_over_the_65_orders"]
        self.assertEqual(u["rule_ids"], ["A", "B", "C"])
        self.assertEqual(u["n_rules"], 3)
        self.assertEqual(u["n_rules_in_the_pool"], 4)
        self.assertEqual(u["fraction_of_the_pool"], 0.75)

    def test_kappa_over_the_union_does_not_see_who_wins_nothing(self):
        d = derive(self._rows(), self.KAPPA, 40.0)
        k = d["kappa_over_the_union"]
        self.assertEqual((k["min"], k["max"]), (1.0, 10.0))
        self.assertEqual((k["min_rule"], k["max_rule"]), ("A", "C"))
        self.assertEqual(k["n"], 3)

    def test_the_range_within_an_order_is_max_over_min(self):
        d = derive(self._rows(), self.KAPPA, 40.0)
        r = d["kappa_range_within_an_order"]
        self.assertEqual([v["range"] for v in r["per_order"]], [2.0, 10.0])
        self.assertEqual((r["min"], r["max"]), (2.0, 10.0))

    def test_the_kappa_cap_may_win_nothing(self):
        d = derive(self._rows(), self.KAPPA, 40.0)
        a = d["argmax_kappa_holds_territory"]
        self.assertEqual(a["rule_id"], "Z")
        self.assertTrue(a["matches_published_max"])
        self.assertFalse(a["holds_territory"])
        self.assertEqual(a["n_orders_where_it_holds"], 0)

    def test_and_may_win_something(self):
        """The other branch, so the boolean is measured and not assumed."""
        rows = self._rows() + [{"order": 2, "n_rules_with_territory": 1,
                                "rule_ids": ["Z"]}]
        a = derive(rows, self.KAPPA, 40.0)["argmax_kappa_holds_territory"]
        self.assertTrue(a["holds_territory"])
        self.assertEqual(a["orders_where_it_holds"], [2])

    def test_warns_if_the_cap_is_not_the_published_max(self):
        a = derive(self._rows(), self.KAPPA, 9.99)[
            "argmax_kappa_holds_territory"]
        self.assertFalse(a["matches_published_max"])

    def test_a_single_rule_order_has_range_one(self):
        rows = [{"order": 0, "n_rules_with_territory": 1, "rule_ids": ["C"]}]
        r = derive(rows, self.KAPPA, 40.0)["kappa_range_within_an_order"]
        self.assertEqual(r["per_order"][0]["range"], 1.0)


if __name__ == "__main__":
    unittest.main()
