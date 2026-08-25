"""
THE 1,600-PAIR SAMPLE — its nesting, its gates and the split B-d needs.

`pair_sample_1600` builds the population Stage B of `PLAN_PROPOSER_1600.md` will
spend on. **No figure of that plan is pinned here** and none can be: every one of
its four rows needs calls that have not been made. What is pinned is the
machinery that decides whether the 400-point and the 1,600-point are the same
measurement at two budgets or two measurements that cannot be compared:

  * the union really contains Stage D's 400, with the same orientation — a pair
    whose two rules swapped places would invert an answer already paid for;
  * the 1,200 come from the COMPLEMENT, so nothing is asked twice;
  * the route §5.1 of the plan warns against is not safe, and not for the reason
    the plan gives: at this scale `random.sample` does nest, by an undocumented
    accident of which branch it takes, and the counterexample beside it shows the
    accident running out. Both are pinned so the complement route reads as
    necessary rather than as ceremony;
  * a queue-pair that appears with both better-rules puts its pairs on the side
    a fixed ranking cannot answer, which is the split `B-d` is a claim about;
  * the block Stage B reads carries no verdict. `rung2/pair_judgement` is on the
    online-loop list of `tests/test_oracle_separation.py`, and the record's shape
    is what keeps it there.

The constants come last, transcribed from §6 of the plan: they were declared
before the sample existed, and a test that says so is what makes moving one
visible.
"""

from __future__ import annotations

import json
import random
import unittest
from pathlib import Path

from rung2.pair_judgement import sample_population
from rung2.pair_sample_1600 import (EXTENSION_SEED, MIN_PER_SIDE, N_BASE,
                                    TARGET, extend, gate_base_is_a_subset,
                                    gate_split_populated,
                                    gate_sample_is_well_formed,
                                    queue_pair_split)

RECORD = Path(__file__).resolve().parent.parent / "results2/pair_sample_1600.json"

# A population in the same shape as the real one: ordered, deduplicated pairs.
POP = [(f"R{i:04d}", f"R{j:04d}") for i in range(1, 40) for j in range(i + 1, 40)]


class TestTheExtension(unittest.TestCase):

    def base(self, k=20):
        return sample_population(POP, k)

    def test_the_base_survives_into_the_union(self):
        base = self.base()
        union, _new = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        self.assertTrue(set(base) <= set(union))

    def test_the_union_has_exactly_the_budget(self):
        base = self.base()
        union, new = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        self.assertEqual(len(union), 80)
        self.assertEqual(len(set(union)), 80)
        self.assertEqual(len(new), 60)

    def test_the_new_pairs_come_from_the_complement(self):
        """Nothing is asked twice: the draw never touches a pair already held."""
        base = self.base()
        _union, new = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        self.assertEqual(new & set(base), set())

    def test_the_union_keeps_the_populations_own_order(self):
        """`sample_population`'s convention, so the record reads the same way
        whatever the budget."""
        base = self.base()
        union, _new = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        self.assertEqual(union, [p for p in POP if p in set(union)])

    def test_it_is_deterministic_at_the_declared_seed(self):
        base = self.base()
        a, _ = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        b, _ = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        self.assertEqual(a, b)

    def test_another_seed_draws_a_different_extension(self):
        base = self.base()
        a, _ = extend(POP, base, budget=80, seed=EXTENSION_SEED)
        b, _ = extend(POP, base, budget=80, seed=EXTENSION_SEED + 1)
        self.assertNotEqual(a, b)

    def test_a_budget_below_what_is_already_held_is_refused(self):
        with self.assertRaises(ValueError):
            extend(POP, self.base(), budget=10, seed=EXTENSION_SEED)

    def test_a_budget_equal_to_what_is_held_adds_nothing(self):
        base = self.base()
        union, new = extend(POP, base, budget=len(base), seed=EXTENSION_SEED)
        self.assertEqual(set(union), set(base))
        self.assertEqual(new, set())


class TestTheTrapItAvoids(unittest.TestCase):
    """
    §5.1 of the plan, and a correction to it dated 2026-08-25.

    The plan gives two reasons for building the extension from the complement.
    The first holds and holds hard: `edge_budget`'s shuffle and Stage D's
    `random.sample` do not agree, and over this population their first 400 share
    not one pair. The second is **false at this scale**: `random.sample(N, 1600)`
    IS a superset of `random.sample(N, 400)` for N = 31,850 under CPython 3.12,
    because both budgets take the selection-set branch, share one draw stream,
    and the smaller comes out an exact prefix of the larger.

    The instruction is still right and the load-bearing word in it is `hoping`.
    The nesting is an undocumented implementation detail: it disappears the
    moment the two budgets straddle the branch boundary of the setsize
    heuristic, as `test_the_resample_route_is_not_guaranteed_to_nest` shows on a
    population where they do. Both facts are pinned here rather than one, because
    a reader who meets only the counterexample would think §5.1 was right and a
    reader who meets only the coincidence would think the complement route was
    ceremony.
    """

    def test_the_resample_route_is_not_guaranteed_to_nest(self):
        """The counterexample: 20 of 200 and 40 of 200 fall in different
        branches of `random.sample`, and the small sample is not contained."""
        small = set(random.Random(0).sample(range(200), 20))
        large = set(random.Random(0).sample(range(200), 40))
        self.assertFalse(small <= large)

    def test_at_this_scale_it_happens_to_nest_and_that_is_the_correction(self):
        """Documented, not depended on. If this ever fails, the standard
        library changed its sampler — nothing in the module moves either way,
        because the module never takes this route."""
        small = set(random.Random(17).sample(range(31850), 400))
        large = set(random.Random(17).sample(range(31850), 1600))
        self.assertTrue(small <= large)

    def test_the_extension_nests_by_construction_at_every_budget(self):
        """What the module actually rests on: not a property of the sampler but
        a property of the complement, true at any budget and any seed."""
        small = sample_population(POP, 20)
        for budget in (20, 21, 80, 300, len(POP)):
            for seed in (EXTENSION_SEED, EXTENSION_SEED + 1):
                with self.subTest(budget=budget, seed=seed):
                    union, _ = extend(POP, small, budget=budget, seed=seed)
                    self.assertTrue(set(small) <= set(union))
                    self.assertEqual(len(union), budget)


class TestTheGates(unittest.TestCase):

    def test_a_complete_union_passes_the_subset_gate(self):
        base = [POP[k] for k in range(N_BASE)]
        g = gate_base_is_a_subset(base + POP[N_BASE:N_BASE + 10], base, POP)
        self.assertTrue(g["passes"])

    def test_a_missing_pair_fails_it(self):
        base = [POP[k] for k in range(N_BASE)]
        g = gate_base_is_a_subset(base[1:], base, POP)
        self.assertFalse(g["passes"])
        self.assertEqual(g["n_missing"], 1)

    def test_an_inverted_pair_fails_it_and_is_named_as_inverted(self):
        """`a_beats_b` names `rule_a`. A swapped pair is not the same question
        and would invert an answer already paid for."""
        base = [POP[k] for k in range(N_BASE)]
        swapped = [(base[0][1], base[0][0])] + base[1:]
        g = gate_base_is_a_subset(swapped, base, POP)
        self.assertFalse(g["passes"])
        self.assertEqual(g["n_inverted"], 1)

    def test_the_well_formed_gate_counts_the_two_sources(self):
        base = [POP[k] for k in range(10)]
        sample = base + POP[10:40]
        g = gate_sample_is_well_formed(sample, base, POP, budget=40)
        self.assertTrue(g["passes"])
        self.assertEqual((g["n_from_stage_d"], g["n_new"]), (10, 30))

    def test_a_duplicate_fails_the_well_formed_gate(self):
        base = [POP[k] for k in range(10)]
        g = gate_sample_is_well_formed(base + base, base, POP, budget=20)
        self.assertFalse(g["passes"])

    def test_a_pair_outside_the_population_fails_it(self):
        base = [POP[k] for k in range(10)]
        g = gate_sample_is_well_formed(base + [("R9998", "R9999")], base, POP,
                                       budget=11)
        self.assertFalse(g["passes"])
        self.assertEqual(g["n_outside_the_population"], 1)

    def test_the_split_gate_blocks_a_thin_side(self):
        thin = {"surface": "better_space", "n_reachable": MIN_PER_SIDE,
                "n_unreachable": MIN_PER_SIDE - 1}
        g = gate_split_populated(thin)
        self.assertFalse(g["passes"])
        self.assertFalse(g["B_d_adjudicable"])

    def test_the_split_gate_passes_at_exactly_the_minimum(self):
        both = {"surface": "better_space", "n_reachable": MIN_PER_SIDE,
                "n_unreachable": MIN_PER_SIDE}
        self.assertTrue(gate_split_populated(both)["passes"])


class TestTheSplitBdIsAbout(unittest.TestCase):

    ACTION = {"R1": "X", "R2": "Y", "R3": "Y", "R4": "X", "R5": "X", "R6": "Z"}

    def rows(self, spec):
        return [{"rule_a": a, "rule_b": b, "better_space": v}
                for a, b, v in spec]

    def test_a_queue_pair_that_never_varies_is_reachable(self):
        """X beats Y both times, so the ranking X > Y answers both."""
        rows = self.rows([("R1", "R2", "a"), ("R4", "R3", "a")])
        split, side = queue_pair_split(rows, "better_space", self.ACTION)
        self.assertEqual(split["n_reachable"], 2)
        self.assertEqual(split["n_unreachable"], 0)
        self.assertEqual(set(side.values()), {"reachable"})

    def test_a_queue_pair_that_varies_puts_all_of_its_pairs_unreachable(self):
        """X wins once and Y wins once on the same queue-pair: no fixed ranking
        gets both, which is exactly the information B-d says the proposer loses
        hardest."""
        rows = self.rows([("R1", "R2", "a"), ("R4", "R3", "b")])
        split, side = queue_pair_split(rows, "better_space", self.ACTION)
        self.assertEqual(split["n_unreachable"], 2)
        self.assertEqual(split["n_reachable"], 0)
        self.assertEqual(split["n_queue_pairs_unreachable"], 1)

    def test_the_two_sides_partition_the_strict_pairs(self):
        rows = self.rows([("R1", "R2", "a"), ("R4", "R3", "b"),
                          ("R5", "R6", "a")])
        split, side = queue_pair_split(rows, "better_space", self.ACTION)
        self.assertEqual(split["n_reachable"] + split["n_unreachable"],
                         split["n_strict"])
        self.assertEqual(len(side), split["n_strict"])

    def test_ties_and_never_right_are_outside_both_sides(self):
        """They are outside every denominator upstream too: a tie is not a
        judgement anyone can get wrong, and `neither_ever_right` is the material
        problem rather than a direction error."""
        rows = self.rows([("R1", "R2", "tie"),
                          ("R4", "R3", "neither_ever_right"),
                          ("R5", "R6", "a")])
        split, side = queue_pair_split(rows, "better_space", self.ACTION)
        self.assertEqual(split["n_strict"], 1)
        self.assertEqual(len(side), 1)

    def test_a_queue_pair_seen_once_is_reachable_by_construction(self):
        """One observation cannot contradict itself. The split is a property of
        the sample and the record says so."""
        rows = self.rows([("R1", "R2", "a")])
        split, _ = queue_pair_split(rows, "better_space", self.ACTION)
        self.assertEqual(split["n_reachable"], 1)


class TestTheRecordKeepsTheTruthOutOfTheAskingPath(unittest.TestCase):
    """Stage B reads `pairs` and `rung2/pair_judgement` is on the online-loop
    list. The separation is a property of the record's shape, not of care."""

    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads(RECORD.read_text())

    def test_the_pairs_block_carries_identity_and_nothing_else(self):
        allowed = {"index", "rule_a", "rule_b", "source"}
        for row in self.rec["pairs"]:
            self.assertEqual(set(row), allowed)

    def test_no_row_of_the_pairs_block_names_a_verdict(self):
        text = json.dumps(self.rec["pairs"])
        for leak in ("better_space", "better_corpus", "wins_a", "wins_b",
                     "queue_ranking"):
            self.assertNotIn(leak, text)

    def test_the_two_blocks_are_the_same_pairs_in_the_same_order(self):
        self.assertEqual([(r["rule_a"], r["rule_b"]) for r in self.rec["pairs"]],
                         [(r["rule_a"], r["rule_b"])
                          for r in self.rec["oracle"]])

    def test_the_record_is_the_budget_the_plan_names(self):
        self.assertEqual(self.rec["n_sample"], TARGET)
        self.assertEqual(self.rec["n_base"], N_BASE)
        self.assertEqual(self.rec["n_new"], TARGET - N_BASE)

    def test_every_gate_in_it_passed(self):
        for name, g in self.rec["gates"].items():
            with self.subTest(name):
                self.assertTrue(g["passes"])

    def test_the_pairs_marked_stage_d_are_the_ones_stage_d_paid_for(self):
        held = {(r["rule_a"], r["rule_b"]) for r in json.loads(
            (RECORD.parent / "pair_judgement_learned.json").read_text())
            ["answers"]}
        marked = {(r["rule_a"], r["rule_b"]) for r in self.rec["pairs"]
                  if r["source"] == "stage_d"}
        self.assertEqual(marked, held)


class TestTheConstantsAreThePlansOwn(unittest.TestCase):
    """Transcribed from §6, declared before the sample existed. If one moves,
    somebody changed the population after seeing something."""

    def test_the_extension_seed(self):
        self.assertEqual(EXTENSION_SEED, 25)

    def test_the_budget(self):
        self.assertEqual(TARGET, 1600)

    def test_what_is_already_paid_for(self):
        self.assertEqual(N_BASE, 400)

    def test_the_minimum_per_side_of_b_ds_split(self):
        self.assertEqual(MIN_PER_SIDE, 100)


if __name__ == "__main__":
    unittest.main()
