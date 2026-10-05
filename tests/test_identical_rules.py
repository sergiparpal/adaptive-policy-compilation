"""
RULES WRITTEN TWICE — the two definitions and the census, no figure.

**No count is pinned here.** The figures live in `results3/identical_rules.json`
and in `results3/FINDINGS3.md` §18. What is pinned is what makes a pair the same
rule and what the census says about it:

  * `written` ignores the order of the conditions and of an `in` list, and
    nothing else: operators, values and their types still tell rules apart;
  * groups hold two or more rules, and their pairs split by queue;
  * the better rule is said of the rule written first or second, and the census
    reads population, sample and both surfaces off what it is handed;
  * the gates fail where they should, and the expectation's interval is the
    exact Poisson interval on 5, scaled.
"""

from __future__ import annotations

import math
import unittest

from rung3 import identical_rules as ir


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


class TestWritten(unittest.TestCase):

    def test_the_order_of_the_conditions_does_not_count(self):
        a = [cond("severity", "gte", 3), cond("product", "eq", "billing")]
        self.assertEqual(ir.written(a), ir.written(list(reversed(a))))

    def test_an_in_list_is_a_set(self):
        self.assertEqual(ir.written([cond("channel", "in", ["chat", "email"])]),
                         ir.written([cond("channel", "in", ["email", "chat"])]))

    def test_a_repeated_condition_counts_once(self):
        c = cond("severity", "gte", 3)
        self.assertEqual(ir.written([c, c]), ir.written([c]))

    def test_operators_values_and_types_tell_rules_apart(self):
        base = ir.written([cond("severity", "gte", 3)])
        for other in (cond("severity", "lte", 3), cond("severity", "gte", 4),
                      cond("severity", "gte", "3"), cond("tier", "gte", 3)):
            with self.subTest(other):
                self.assertNotEqual(base, ir.written([other]))
        self.assertNotEqual(ir.written([cond("flag", "eq", True)]),
                            ir.written([cond("flag", "eq", 1)]))


class TestGroupsAndPairs(unittest.TestCase):

    def test_groups_hold_two_or_more(self):
        self.assertEqual(ir.groups({"R3": "k", "R1": "k", "R2": "j", "R4": "m",
                                    "R5": "m"}),
                         [["R1", "R3"], ["R4", "R5"]])

    def test_pairs_split_by_queue(self):
        action = {"R1": "X", "R2": "X", "R3": "Y"}
        got = ir.pairs_of([["R1", "R2", "R3"]], action)
        self.assertEqual(got, {"same_queue": [("R1", "R2")],
                               "different_queue": [("R1", "R3"), ("R2", "R3")]})

    def test_oriented(self):
        self.assertEqual(ir.oriented("a", True), "first")
        self.assertEqual(ir.oriented("a", False), "second")
        self.assertEqual(ir.oriented("b", True), "second")
        self.assertEqual(ir.oriented("b", False), "first")
        for v in ("tie", "neither_ever_right"):
            self.assertEqual(ir.oriented(v, True), v)


class TestTheCensus(unittest.TestCase):

    def world(self):
        # Four space points. R1 and R2 cover the same two, R3 another two.
        ext = {"R1": 0b0011, "R2": 0b0011, "R3": 0b1100}
        action = {"R1": "X", "R2": "Y", "R3": "X"}
        born = {"R1": 40, "R2": 7, "R3": 1}            # R2 was written first
        tmask = {"X": 0b0001, "Y": 0b0010 | 0b1100}    # one point each in R1/R2
        matched_sets = [{"R1", "R2"}, {"R1", "R2"}, {"R3"}, set()]
        truth = ["Y", "Y", "X", "X"]
        population = {frozenset(("R1", "R2"))}
        sample = {frozenset(("R1", "R2")): {"index": 9, "source": "new"}}
        return ext, action, born, tmask, matched_sets, truth, population, sample

    def test_one_pair_read_whole(self):
        ext, action, born, tmask, ms, truth, pop, sample = self.world()
        c = ir.census([["R1", "R2"]], action, born, ext, tmask, ms, truth, pop, sample)
        self.assertEqual(c["pairs"], {"same_queue": 0, "different_queue": 1})
        dq = c["different_queue"]
        row = dq["rows"][0]
        self.assertEqual((row["rule_first"], row["rule_second"]), ("R2", "R1"))
        self.assertEqual(row["extension"], 2)
        self.assertEqual(row["better_space"], "tie")         # one point each
        self.assertEqual(row["better_corpus"], "first")      # both arrivals are Y
        self.assertEqual((row["in_population"], row["in_sample"],
                          row["sample_batch"], row["sample_index"]),
                         (True, True, "new", 9))
        self.assertEqual(row["corpus_cases_both_match"], 2)
        self.assertEqual((dq["space_points_covered"], dq["corpus_cases_covered"]), (2, 2))
        self.assertEqual(dq["written_apart_in_cases"], {"min": 33, "median": 33, "max": 33})
        self.assertEqual(dq["queue_pairs"], {"X vs Y": 1})


class TestTheGates(unittest.TestCase):

    def written_census(self, batches=("new",) * 5, named=ir.WHY_NAMED):
        rows = [{"rule_first": a, "rule_second": b} for a, b in named]
        return {"different_queue": {"rows": rows, "in_sample": len(batches),
                                    "in_sample_by_batch": dict(
                                        __import__("collections").Counter(batches))}}

    def test_why_passes_on_its_own_reading(self):
        self.assertTrue(ir.gate_why(self.written_census())["passes"])

    def test_why_fails_on_a_count_a_batch_or_a_missing_name(self):
        for census in (self.written_census(batches=("new",) * 6),
                       self.written_census(batches=("new",) * 4 + ("base",)),
                       self.written_census(named=ir.WHY_NAMED[:1])):
            with self.subTest(census["different_queue"]["in_sample_by_batch"]):
                self.assertFalse(ir.gate_why(census)["passes"])

    def test_nesting(self):
        covering = {"same_queue": [], "different_queue": [("R1", "R2")]}
        self.assertTrue(ir.gate_nesting({"same_queue": [],
                                         "different_queue": [("R1", "R2")]},
                                        covering)["passes"])
        g = ir.gate_nesting({"same_queue": [("R3", "R4")], "different_queue": []},
                            covering)
        self.assertEqual(g["pairs_that_do_not"], ["R3/R4"])

    def test_population(self):
        self.assertTrue(ir.gate_population({"population": 31850})["passes"])
        self.assertFalse(ir.gate_population({"population": 31849})["passes"])


class TestTheExpectation(unittest.TestCase):

    def test_the_centre_is_the_sample_scaled(self):
        self.assertEqual(ir.EXPECTED_CENTRE, 99.53)

    def test_the_interval_is_the_exact_poisson_interval_on_5(self):
        def cdf(k, lam):
            return sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k + 1))
        scale = 31850 / 1600
        lo, hi = 1.6235, 11.6683
        self.assertAlmostEqual(1 - cdf(4, lo), 0.025, places=4)   # P(X >= 5)
        self.assertAlmostEqual(cdf(5, hi), 0.025, places=4)       # P(X <= 5)
        self.assertEqual(ir.EXPECTED_INTERVAL, (round(lo * scale), round(hi * scale)))

    def test_read(self):
        def c(n):
            return {"different_queue": {"in_population": n}}
        self.assertTrue(ir.read_expectation(c(100))["inside"])
        self.assertTrue(ir.read_expectation(c(32))["inside"])
        self.assertFalse(ir.read_expectation(c(31))["inside"])
        self.assertFalse(ir.read_expectation(c(233))["inside"])


if __name__ == "__main__":
    unittest.main()
