"""
THE GATES OF `pair_benchmark`, ITS BIT CONVENTION AND ITS TWO ASSERTIONS.

That module publishes a benchmark: 199 pairs of hidden rules with a known
winner, 170 of them carrying a witness ticket. **No finding is pinned here** —
there is none to pin. The module measures nothing, scores nobody and spends no
API call; what it can be worth is that the population is the one the next stage
was budgeted for and that every witness is what it says it is.

What is pinned:

  * the four boxes of the 406 pairs, which are a property of the FROZEN hidden
    policy and of `hidden_priority.py`, not a result of this run;
  * the two counts `PLAN_PAIRWISE.md` §7 made a gate on this stage, 170 and 29,
    through the gate function rather than as bare numbers — and that the gate
    fails when either moves;
  * **the bit convention**, twice: directly on hand-written masks, and by
    rebuilding every one of the 199 witnesses with the plan's own list
    comprehension over `true_action` and checking the mask formulation agrees.
    An LSB-first reading here draws witnesses from the wrong cases and every
    figure downstream is quietly wrong, so this is the check that matters most;
  * **the two assertions of `pair_row` fire**, each provoked separately;
  * determinism across three `PYTHONHASHSEED` values, in separate processes.
    The child prints its own randomization witness, so the test cannot pass by
    proving that hashing stopped being randomized.

Nothing here calls `main()` without `--digest`, so nothing here writes to
`results2/`.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.domain import ATTRIBUTES
from harness.hidden_policy import true_action
from rung2.hidden_priority import build_hidden_engine
from rung2.pair_benchmark import (GATE_CLEAN, GATE_UNCLEAN, N_PAIRS, N_RULES,
                                  build, case_indices, digest, gate_determinism,
                                  gate_partition, gate_witnesses,
                                  lowest_case_index, pair_row)

REPO = Path(__file__).resolve().parent.parent
HASH_SEEDS = ("0", "1", "2")


# ---------------------------------------------------------------------------
# The bit convention (trap 5.1)
# ---------------------------------------------------------------------------

class TestTheBitConvention(unittest.TestCase):
    """`Space` is MSB-first: case index i is bit n-1-i. Eight cases, written
    out by hand."""

    N = 8

    def mask(self, points):
        return sum(1 << (self.N - 1 - i) for i in points)

    def test_the_lowest_case_index_is_the_highest_set_bit(self):
        self.assertEqual(lowest_case_index(self.mask([3, 5, 7]), self.N), 3)
        self.assertEqual(lowest_case_index(self.mask([0]), self.N), 0)
        self.assertEqual(lowest_case_index(self.mask([7]), self.N), 7)

    def test_an_empty_mask_has_no_lowest_case(self):
        self.assertIsNone(lowest_case_index(0, self.N))

    def test_case_indices_come_out_ascending(self):
        self.assertEqual(case_indices(self.mask([0, 3, 4, 7]), self.N),
                         [0, 3, 4, 7])

    def test_an_lsb_first_reading_would_disagree(self):
        """The mistake this convention exists to prevent is silent: both
        readings return a valid case index, and only one of them is the case the
        two rules actually compete over."""
        m = self.mask([3, 5])
        lsb_first = (m & -m).bit_length() - 1
        self.assertNotEqual(lowest_case_index(m, self.N), lsb_first)


# ---------------------------------------------------------------------------
# The gates, on material built to hit or miss them
# ---------------------------------------------------------------------------

class TestThePartitionGate(unittest.TestCase):

    GOOD = {"skipped_disjoint": 112, "skipped_subsumed_by_structure": 61,
            "skipped_same_action": 34, "declared": 199, "rejected": []}

    def test_it_passes_on_the_four_published_boxes(self):
        g = gate_partition(dict(self.GOOD))
        self.assertTrue(g["passes"])
        self.assertEqual(g["total"], N_PAIRS)

    def test_the_four_boxes_partition_the_pairs_of_the_29_rules(self):
        self.assertEqual(N_PAIRS, N_RULES * (N_RULES - 1) // 2)
        self.assertEqual(112 + 61 + 34 + 199, N_PAIRS)

    def test_a_box_off_by_one_fails_even_though_the_total_still_could(self):
        bad = dict(self.GOOD, skipped_disjoint=113, skipped_same_action=33)
        g = gate_partition(bad)
        self.assertEqual(g["total"], N_PAIRS)
        self.assertFalse(g["passes"])

    def test_a_total_that_is_not_406_fails(self):
        g = gate_partition(dict(self.GOOD, declared=198))
        self.assertFalse(g["passes"])

    def test_a_rejected_edge_fails(self):
        """`hidden_priority` has never rejected one. If it starts to, the edge
        set is no longer the one rung 2 published."""
        g = gate_partition(dict(self.GOOD, rejected=[("H01", "H02", "cierra_ciclo")]))
        self.assertFalse(g["passes"])


class TestTheWitnessGate(unittest.TestCase):

    def rows(self, clean, unclean):
        return ([{"clean": True}] * clean) + ([{"clean": False}] * unclean)

    def test_it_passes_at_the_two_counts_the_plan_budgeted_for(self):
        g = gate_witnesses(self.rows(GATE_CLEAN, GATE_UNCLEAN))
        self.assertTrue(g["passes"])
        self.assertEqual(g["n_declared"], 199)

    def test_one_witness_more_fails(self):
        g = gate_witnesses(self.rows(GATE_CLEAN + 1, GATE_UNCLEAN - 1))
        self.assertFalse(g["passes"])

    def test_one_witness_fewer_fails(self):
        g = gate_witnesses(self.rows(GATE_CLEAN - 1, GATE_UNCLEAN + 1))
        self.assertFalse(g["passes"])

    def test_a_different_population_fails_even_at_the_right_ratio(self):
        g = gate_witnesses(self.rows(2 * GATE_CLEAN, 2 * GATE_UNCLEAN))
        self.assertFalse(g["passes"])


class TestTheDeterminismGate(unittest.TestCase):

    def rows(self, idx):
        return [{"winner": "H01", "loser": "H04", "witness_index": idx,
                 "witness": {"severity": 1}}]

    def test_two_identical_builds_pass(self):
        g = gate_determinism(self.rows(79800), self.rows(79800))
        self.assertTrue(g["passes"])

    def test_one_witness_moving_fails(self):
        g = gate_determinism(self.rows(79800), self.rows(79801))
        self.assertFalse(g["passes"])

    def test_the_digest_covers_the_witness_and_not_only_the_index(self):
        a = [{"winner": "H01", "loser": "H04", "witness_index": 1,
              "witness": {"severity": 1}}]
        b = [{"winner": "H01", "loser": "H04", "witness_index": 1,
              "witness": {"severity": 2}}]
        self.assertNotEqual(digest(a), digest(b))


# ---------------------------------------------------------------------------
# The whole benchmark, over the frozen policy
# ---------------------------------------------------------------------------

class TestTheBenchmarkOverTheHiddenPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rows, cls.stats, cls.n = build()
        cls.cases = list(all_cases())
        engine, _declared, _s = build_hidden_engine()
        cls.engine = engine
        cls.action = {r.rule_id: r.action for r in engine.rules}

    def test_the_three_gates_pass(self):
        self.assertTrue(gate_partition(self.stats)["passes"])
        self.assertTrue(gate_witnesses(self.rows)["passes"])

    def test_every_witness_is_matched_by_both_rules(self):
        """Assertion 1 of the module header. `pair_row` raises on a failure, so
        this could only fire if it stopped checking — which is the point."""
        by_id = {r.rule_id: r for r in self.engine.rules}
        for r in self.rows:
            if not r["clean"]:
                continue
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                case = self.cases[r["witness_index"]]
                self.assertTrue(by_id[r["winner"]].matches(case))
                self.assertTrue(by_id[r["loser"]].matches(case))

    def test_every_witness_is_sent_to_the_winners_queue(self):
        """Assertion 2. It is what makes the pair answerable: the correct queue
        for the ticket is on the menu, and it is the winner's."""
        for r in self.rows:
            if not r["clean"]:
                continue
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertEqual(true_action(self.cases[r["witness_index"]]),
                                 r["winner_action"])

    def test_the_mask_formulation_equals_the_plans_list_comprehension(self):
        """
        The strongest check of the bit convention there is. `PLAN_PAIRWISE.md`
        §7 writes the witness as the first element of

            [i for i in cases_of(inter) if true_action(cases[i]) == action[w]]

        and the module computes it as one AND against a per-action mask. They
        must agree on all 199 pairs, the 29 without a witness included.
        """
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                inter = (self.engine.ext[r["winner"]]
                         & self.engine.ext[r["loser"]])
                want = self.action[r["winner"]]
                brute = next((i for i in case_indices(inter, self.n)
                              if true_action(self.cases[i]) == want), None)
                self.assertEqual(brute, r["witness_index"])

    def test_the_pairs_with_no_witness_lose_the_region_to_another_rule(self):
        """Not to an empty intersection: overlap is what made the edge
        declarable. `owned_by` names the rules that hold it instead."""
        for r in self.rows:
            if r["clean"]:
                continue
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertGreater(r["overlap_cases"], 0)
                self.assertEqual(r["clean_cases"], 0)
                self.assertTrue(r["owned_by"])
                self.assertEqual(sum(o["cases"] for o in r["owned_by"]),
                                 r["overlap_cases"])
                self.assertNotIn(r["winner_action"],
                                 r["true_actions_over_the_overlap"])

    def test_the_winner_always_comes_from_an_earlier_layer(self):
        """The edges are derived from the layer order, so the winner is the
        lower index. If that inverted, the key would be backwards and every
        assertion above would still pass."""
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertLess(r["winner_layer_index"], r["loser_layer_index"])

    def test_the_two_rules_of_a_pair_never_share_an_action(self):
        """`hidden_priority` filters same-action pairs out upstream. It is what
        makes the three outcomes of the next stage well defined."""
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertNotEqual(r["winner_action"], r["loser_action"])

    def test_every_witness_is_a_complete_ticket(self):
        for r in self.rows:
            if not r["clean"]:
                continue
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertEqual(set(r["witness"]), set(ATTRIBUTES))


# ---------------------------------------------------------------------------
# The two assertions, provoked
# ---------------------------------------------------------------------------

class TestTheAssertionsFire(unittest.TestCase):
    """A record that looks plausible and is wrong is the failure mode here, so
    both guards are provoked rather than trusted."""

    @classmethod
    def setUpClass(cls):
        cls.engine, cls.declared, _s = build_hidden_engine()
        cls.n = cls.engine.space.n
        cls.cases = list(all_cases())
        cls.action = {r.rule_id: r.action for r in cls.engine.rules}
        cls.layer = {r.rule_id: k for k, r in enumerate(cls.engine.rules)}
        # The pair both tests below run on, chosen exactly rather than
        # hopefully. It must satisfy two things at once: its LOWEST overlapping
        # case is decided by neither rule — otherwise the wrong-key assertion is
        # never provoked and the test passes for the wrong reason — and it does
        # have a clean witness further in, so the counterpart test can show the
        # same pair coming out clean under the real key. 52 of the 199 qualify.
        cls.truth = {a: cls._truth_mask(cls.cases, cls.n, a)
                     for a in {cls.action[w] for w, _l in cls.declared}}
        cls.pair = next(
            (w, lo) for w, lo in cls.declared
            if cls.action[w] != true_action(cls.cases[lowest_case_index(
                cls.engine.ext[w] & cls.engine.ext[lo], cls.n)])
            and (cls.engine.ext[w] & cls.engine.ext[lo]
                 & cls.truth[cls.action[w]]) != 0)

    @staticmethod
    def _truth_mask(cases, n, want):
        bits = bytearray(n)
        for i, c in enumerate(cases):
            if true_action(c) == want:
                bits[i] = 1
        return int("".join(map(str, bits)), 2)

    def call(self, engine, truth, w, lo):
        return pair_row(engine, self.cases, truth, {}, self.action, self.layer,
                        w, lo, self.n)

    def test_a_witness_whose_truth_is_not_the_winners_action_stops_the_run(self):
        """Simulates a wrong key: a truth mask that calls every case clean, so
        the first case of the overlap is taken and its queue is somebody
        else's."""
        w, lo = self.pair
        lying = {self.action[w]: self.engine.space.full}
        with self.assertRaises(AssertionError) as ctx:
            self.call(self.engine, lying, w, lo)
        self.assertIn("truth", str(ctx.exception))

    def test_the_same_pair_is_clean_under_the_real_key(self):
        """The counterpart, so the test above is known to be provoking the
        assertion and not merely hitting a pair that has no witness at all."""
        w, lo = self.pair
        row = self.call(self.engine, self.truth, w, lo)
        self.assertTrue(row["clean"])
        self.assertEqual(true_action(self.cases[row["witness_index"]]),
                         self.action[w])

    def test_a_mask_that_disagrees_with_the_rule_stops_the_run(self):
        """Simulates the LSB-first mistake and every other way of building a
        witness outside the region: the mask says the rule is there and
        `Rule2.matches` says it is not."""
        w, lo = self.declared[0]
        engine = build_hidden_engine()[0]
        engine.ext[w] = engine.space.full          # the mask now lies
        truth = {self.action[w]: engine.space.full}
        with self.assertRaises(AssertionError) as ctx:
            self.call(engine, truth, w, lo)
        self.assertIn("not matched by both rules", str(ctx.exception))


# ---------------------------------------------------------------------------
# Determinism across processes
# ---------------------------------------------------------------------------

def run_child(hashseed: str) -> dict:
    env = dict(os.environ, PYTHONHASHSEED=hashseed)
    p = subprocess.run([sys.executable, "-m", "rung2.pair_benchmark", "--digest"],
                       cwd=REPO, env=env, capture_output=True, text=True,
                       timeout=300)
    if p.returncode != 0:
        raise AssertionError(f"the child failed with PYTHONHASHSEED={hashseed}:"
                             f"\n{p.stderr}")
    return json.loads(p.stdout)


class TestTheWitnessesDoNotDependOnTheHash(unittest.TestCase):
    """`--digest` writes nothing. Three processes, three seeds, one digest."""

    @classmethod
    def setUpClass(cls):
        cls.runs = {s: run_child(s) for s in HASH_SEEDS}

    def test_the_witness_confirms_the_hash_is_randomized(self):
        """If this fails the rest of the class proves nothing — it would mean
        hashing is no longer randomized in this Python, not that the benchmark
        is deterministic. The precedent is rung 4's false zero."""
        seen = {r["set_iteration"] for r in self.runs.values()}
        self.assertEqual(len(seen), len(HASH_SEEDS))

    def test_the_witnesses_are_identical_across_seeds(self):
        seen = {r["digest"] for r in self.runs.values()}
        self.assertEqual(len(seen), 1, f"different witnesses: {self.runs}")

    def test_the_population_is_identical_across_seeds(self):
        for field in ("n_declared", "n_clean"):
            with self.subTest(field):
                seen = {r[field] for r in self.runs.values()}
                self.assertEqual(len(seen), 1)


if __name__ == "__main__":
    unittest.main()
