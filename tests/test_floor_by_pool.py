"""
THE GATES OF `floor_by_pool`, ITS TWO GENERATORS AND ITS LABELS — no figure.

That module publishes floors: what an order that searches for nothing scores on
each pool and each surface. **No measured value of the finding is pinned here.**
What `born_at` scores on the `hibrido` pool, what reversing it scores over the
space, and how far either sits from a shuffle live in
`results3/floor_by_pool.json` and in the section appended to
`results3/FINDINGS3.md`. Repeating any of them in a test would give a figure a
second owner, which is the failure this repository already decided not to commit
(`IDEAS.md`, technical debt; `tests/test_territory_holders.py` says the same).

The six reproduction targets are not figures of this record either: they are
declared constants of the module (`floor_by_pool.GATES`), each naming the record
or the probe it gates against. The test's job is that the gate is BLOCKING and
that it is reading what it says it reads.

What is pinned instead:

  * the two random-order generators of trap 5.5 are transcribed faithfully, and
    they really do disagree — the whole reason every random row names one;
  * `floor` reads first-match-wins the way the rest of the thread does, on an
    instance small enough to write the answer out by hand;
  * the five-split aggregation is the arithmetic it claims, and says out loud
    that for a random family it is a DOUBLE aggregation;
  * the gate passes when the figures reproduce and fails when one misses, per
    row and at that row's own tolerance;
  * the whole gate still passes over the real base, which is the regression
    guard that matters: it is what says the pool construction, the index sets
    and the generators are still the record's.

Nothing here calls `main()`, so nothing here writes to `results3/`.
"""

from __future__ import annotations

import random
import unittest

from rung3.floor_by_pool import (GATES, GEN_MODULE, GEN_RECORD,
                                 born_at_order, five_split_rows, floor,
                                 gate_generators_differ_only_in_the_rng,
                                 gate_rows, measure, module_random_orders,
                                 order_families, record_random_orders)
from rung3.local_search import random_order
from rung3.order_metrics_rules import mask_from_points

IDS = [f"R{i:04d}" for i in range(1, 21)]


# ---------------------------------------------------------------------------
# The two generators of trap 5.5
# ---------------------------------------------------------------------------

class TestTheRecordGenerator(unittest.TestCase):
    """`order_search.py:344-350` is four lines inline in a `main()`: there is
    nothing to import, so it is transcribed. These tests are the check that the
    transcription is the original."""

    def _inline(self, ids, n=50, seed=17):
        """The four lines of `order_search.main`, copied here on purpose."""
        rng = random.Random(seed)
        out = []
        for _ in range(n):
            o = ids[:]
            rng.shuffle(o)
            out.append(o)
        return out

    def test_it_is_the_four_lines_of_order_search(self):
        self.assertEqual(record_random_orders(IDS), self._inline(IDS))

    def test_each_draw_is_conditioned_on_the_ones_before_it(self):
        """One RNG advanced fifty times, not fifty RNGs. Draw 0 is a single
        shuffle of `Random(17)`; draw 1 is not."""
        one = list(IDS)
        random.Random(17).shuffle(one)
        draws = record_random_orders(IDS)
        self.assertEqual(draws[0], one)
        self.assertNotEqual(draws[1], one)

    def test_it_shuffles_the_order_it_is_given(self):
        """It does NOT sort first. Over the learned base that makes no
        difference — the ids are R%04d in birth order — and that is checked
        separately; over any other base it would."""
        scrambled = list(reversed(IDS))
        self.assertNotEqual(record_random_orders(scrambled),
                            record_random_orders(IDS))

    def test_it_does_not_touch_the_list_it_is_given(self):
        before = list(IDS)
        record_random_orders(IDS)
        self.assertEqual(IDS, before)


class TestTheModuleGenerator(unittest.TestCase):

    def test_it_is_random_order_over_seeds_zero_to_fortynine(self):
        draws = module_random_orders(IDS)
        self.assertEqual(len(draws), 50)
        self.assertEqual(draws, [random_order(IDS, seed=k) for k in range(50)])

    def test_it_sorts_before_shuffling(self):
        """`random_order` sorts, so the order it is handed cannot reach the
        result. This is the half of the difference that is NOT the RNG."""
        self.assertEqual(module_random_orders(list(reversed(IDS))),
                         module_random_orders(IDS))


class TestTheTwoGeneratorsDisagree(unittest.TestCase):
    """Trap 5.5. If these ever came out equal, naming the generator on every
    random row would be pointless — and the gate rows, which name one each,
    would stop isolating anything."""

    def test_they_produce_different_sequences(self):
        self.assertNotEqual(record_random_orders(IDS), module_random_orders(IDS))

    def test_they_are_named_apart(self):
        self.assertNotEqual(GEN_MODULE, GEN_RECORD)


class TestTheGeneratorsGate(unittest.TestCase):
    """Over the learned base the two generators start from the same list, so
    what trap 5.5 measures is the RNG alone. Checked, never assumed."""

    def _rules(self, ids):
        return [{"rule_id": r} for r in ids]

    def test_it_passes_when_the_appearance_order_is_sorted(self):
        g = gate_generators_differ_only_in_the_rng(IDS, self._rules(IDS))
        self.assertTrue(g["appearance_equals_sorted"])
        self.assertEqual(g["n_rules"], len(IDS))

    def test_it_fails_when_the_record_arrives_out_of_order(self):
        shuffled = list(reversed(IDS))
        g = gate_generators_differ_only_in_the_rng(IDS, self._rules(shuffled))
        self.assertFalse(g["appearance_equals_sorted"])


# ---------------------------------------------------------------------------
# The primitive
# ---------------------------------------------------------------------------

# Eight cases, three rules, `Space`'s bit convention: case i is bit n-1-i.
N = 8
FULL = (1 << N) - 1
M = {"A": mask_from_points([0, 1, 2, 3], N),
     "B": mask_from_points([2, 3, 4, 5], N),
     "C": mask_from_points([4, 5, 6, 7], N)}
W = {"A": mask_from_points([0, 1], N),
     "B": mask_from_points([2, 3, 4, 5], N),
     "C": mask_from_points([6, 7], N)}
INSTANCE = (M, W, FULL, N)


class TestTheFloorReadsFirstMatchWins(unittest.TestCase):

    def test_the_lowest_ranked_matching_rule_takes_the_case(self):
        """[A, B, C]: A takes 0-3 and is right on two of them, B takes what is
        left of its own (4, 5) and is right on both, C takes 6 and 7. Six of
        eight."""
        self.assertAlmostEqual(floor(["A", "B", "C"], INSTANCE), 6 / 8)

    def test_moving_one_rule_forward_changes_the_score(self):
        """[B, A, C]: B now takes 2-5, all four right. Eight of eight — and it
        is the same three rules. The order is the whole content of the
        measurement."""
        self.assertAlmostEqual(floor(["B", "A", "C"], INSTANCE), 1.0)

    def test_a_case_no_rule_matches_counts_as_a_failure(self):
        """Not as an abstention: the denominator is the whole index set, which
        is how `order_search.evaluate` counts and therefore how every figure in
        this thread was measured."""
        partial = ({"A": M["A"], "B": M["B"]}, {"A": W["A"], "B": W["B"]},
                   FULL, N)
        self.assertAlmostEqual(floor(["A", "B"], partial), 4 / 8)


class TestTheOrderFamilies(unittest.TestCase):

    def test_born_at_is_ascending_and_the_reverse_is_its_mirror(self):
        born = {rid: k for k, rid in enumerate(reversed(IDS))}
        fams = order_families(IDS, born)
        self.assertEqual(fams["born_at"], list(reversed(IDS)))
        self.assertEqual(fams["born_at_reversed"], IDS)

    def test_born_at_does_not_read_the_id(self):
        """The two coincide over the learned base and must not be assumed to."""
        born = {rid: (0 if rid == IDS[-1] else 1) for rid in IDS}
        self.assertEqual(born_at_order(IDS, born)[0], IDS[-1])


# ---------------------------------------------------------------------------
# The five-split aggregation (trap 5.6)
# ---------------------------------------------------------------------------

class TestTheFiveSplitAggregation(unittest.TestCase):

    def _rows(self, order, generator, values):
        return [{"order": order, "generator": generator, "pool": "puro",
                 "surface": f"corpus_test_split{s}", "value": v,
                 "n_cases": 1000}
                for s, v in enumerate(values)]

    def test_it_is_the_mean_of_the_per_split_values(self):
        rows = self._rows("born_at", None, [0.50, 0.52, 0.54, 0.56, 0.58])
        out = five_split_rows(rows)
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(out[0]["value"], 0.54)
        self.assertEqual(out[0]["surface"], "corpus_test_5splits")
        self.assertEqual([f["split"] for f in out[0]["per_split"]],
                         [0, 1, 2, 3, 4])

    def test_it_keeps_the_per_split_values_beside_the_mean(self):
        """Split 0 is the record's index set and the only one that reproduces
        0.5216. Reporting only the mean would drop it silently (trap 5.6)."""
        rows = self._rows("born_at", None, [0.50, 0.52, 0.54, 0.56, 0.58])
        out = five_split_rows(rows)
        self.assertEqual([f["value"] for f in out[0]["per_split"]],
                         [0.50, 0.52, 0.54, 0.56, 0.58])

    def test_a_random_family_is_labelled_a_double_aggregation(self):
        rows = self._rows("random", GEN_RECORD, [0.42] * 5)
        out = five_split_rows(rows)
        self.assertIn("mean over 5 splits of the mean over 50 draws",
                      out[0]["aggregation"])
        self.assertEqual(out[0]["generator"], GEN_RECORD)

    def test_the_two_generators_do_not_land_in_the_same_row(self):
        rows = (self._rows("random", GEN_RECORD, [0.42] * 5)
                + self._rows("random", GEN_MODULE, [0.43] * 5))
        out = five_split_rows(rows)
        self.assertEqual(len(out), 2)
        self.assertEqual({f["generator"] for f in out}, {GEN_RECORD, GEN_MODULE})

    def test_it_ignores_the_surfaces_that_are_not_splits(self):
        rows = self._rows("born_at", None, [0.5] * 5) + [
            {"order": "born_at", "generator": None, "pool": "puro",
             "surface": "corpus_full", "value": 0.9, "n_cases": 2000},
            {"order": "born_at", "generator": None, "pool": "puro",
             "surface": "space", "value": 0.1, "n_cases": 134400}]
        out = five_split_rows(rows)
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(out[0]["value"], 0.5)


# ---------------------------------------------------------------------------
# The gate, on instances built to hit or miss it
# ---------------------------------------------------------------------------

class TestTheGateIsBlocking(unittest.TestCase):
    """Built so that every deterministic row scores exactly its own target and
    every random row reports exactly its own target. Then one row is pushed off
    and the gate must say so."""

    SIZE = 100_000

    def _instance(self, value):
        k = round(value * self.SIZE)
        full = (1 << self.SIZE) - 1
        return ({"X": full}, {"X": (1 << k) - 1}, full, self.SIZE)

    def _material(self, bump=None, bump_id=None):
        instances, randoms = {}, {}
        for g in GATES:
            value = g["target"] + (bump if g["id"] == bump_id else 0.0)
            if g["order"] == "random":
                randoms[(g["generator"], g["surface"], g["pool"])] = {
                    "mean": value, "pstdev": g.get("sd_target") or 0.0,
                    "stdev": 0.0, "min": 0.0, "max": 1.0, "n_draws": 50}
            else:
                instances[(g["surface"], g["pool"])] = self._instance(value)
        return instances, {"born_at": ["X"]}, randoms

    def test_it_passes_when_every_row_reproduces(self):
        rows = gate_rows(*self._material())
        self.assertEqual(len(rows), len(GATES))
        self.assertTrue(all(r["passes"] for r in rows))

    def test_one_row_off_its_tolerance_fails_and_only_that_row(self):
        for g in GATES:
            with self.subTest(g["id"]):
                rows = gate_rows(*self._material(bump=10 * g["tol"],
                                                 bump_id=g["id"]))
                failed = [r["id"] for r in rows if not r["passes"]]
                self.assertEqual(failed, [g["id"]])

    def test_a_miss_inside_the_tolerance_still_passes(self):
        for g in GATES:
            with self.subTest(g["id"]):
                rows = gate_rows(*self._material(bump=g["tol"] / 2,
                                                 bump_id=g["id"]))
                self.assertTrue(all(r["passes"] for r in rows))

    def test_the_deviation_is_reported_and_never_blocking(self):
        """The plan writes the two published deviations as `sd ~`, not as `+-`.
        They are recorded next to the mean and they do not decide anything."""
        rows = gate_rows(*self._material())
        randoms = [r for r in rows if r["order"] == "random"]
        self.assertTrue(randoms)
        for r in randoms:
            self.assertIn("measured_sd", r)
            self.assertFalse(r["sd_is_blocking"])
            self.assertTrue(r["passes"])


class TestEveryGateRowSaysWhatItGatesAgainst(unittest.TestCase):

    def test_each_row_names_a_source_and_declares_record_or_probe(self):
        for g in GATES:
            with self.subTest(g["id"]):
                self.assertIn(g["kind"], ("record", "probe"))
                self.assertTrue(g["source"])
                self.assertTrue(g["protocol"])

    def test_the_probe_rows_are_the_full_corpus_ones(self):
        """G3 and G4 gate against figures no record owns. Giving them an owner
        is what this stage is for, and until it has run they are still a
        probe."""
        probes = {g["id"] for g in GATES if g["kind"] == "probe"}
        self.assertEqual(probes, {"G3", "G4"})

    def test_every_random_row_names_its_generator(self):
        for g in GATES:
            with self.subTest(g["id"]):
                if g["order"] == "random":
                    self.assertIn(g["generator"], (GEN_MODULE, GEN_RECORD))
                else:
                    self.assertIsNone(g["generator"])

    def test_the_generators_are_not_all_the_same_one(self):
        """The record's corpus figures came from one and its space figure from
        the other. A gate that prescribed a single generator would fail on a
        CORRECT implementation."""
        used = {g["generator"] for g in GATES if g["order"] == "random"}
        self.assertEqual(used, {GEN_MODULE, GEN_RECORD})


# ---------------------------------------------------------------------------
# The whole thing, over the real base
# ---------------------------------------------------------------------------

class TestTheGateOverTheLearnedBase(unittest.TestCase):
    """The regression guard: it says the pool construction, the index sets and
    the generators are still the ones the records were measured with. It pins no
    value of its own — the six targets are `floor_by_pool.GATES`, each naming
    the record or probe it comes from."""

    @classmethod
    def setUpClass(cls):
        cls.payload, cls.passes = measure()

    def test_the_six_rows_reproduce(self):
        rows = self.payload["gates"]["rows"]
        self.assertEqual([r["id"] for r in rows],
                         [g["id"] for g in GATES])
        for r in rows:
            with self.subTest(r["id"]):
                self.assertTrue(r["passes"],
                                f"{r['id']} measured {r['measured']} against "
                                f"{r['target']} +- {r['tol']}")
        self.assertTrue(self.passes)

    def test_the_two_generators_start_from_the_same_list_over_this_base(self):
        g = self.payload["gates"]["generators_differ_only_in_the_rng"]
        self.assertTrue(g["appearance_equals_sorted"])

    def test_every_floor_names_its_surface_its_pool_and_its_generator(self):
        for r in self.payload["floors"]:
            with self.subTest(r["order"], surface=r["surface"], pool=r["pool"]):
                self.assertIn(r["pool"], ("puro", "hibrido"))
                self.assertTrue(r["surface"])
                if r["order"] == "random":
                    self.assertIn(r["generator"], (GEN_MODULE, GEN_RECORD))
                else:
                    self.assertIsNone(r["generator"])

    def test_both_pools_are_measured_on_every_surface(self):
        """The cell that did not exist is `hibrido`, and the point of the stage
        is that it does now — on all of them, not only where it was cheap."""
        for surface in ("corpus_full", "corpus_test_split0",
                        "corpus_test_5splits", "space"):
            for order in ("born_at", "born_at_reversed"):
                with self.subTest(surface=surface, order=order):
                    pools = {r["pool"] for r in self.payload["floors"]
                             if r["surface"] == surface and r["order"] == order}
                    self.assertEqual(pools, {"puro", "hibrido"})

    def test_the_five_split_rows_carry_their_five(self):
        rows = [r for r in self.payload["floors"]
                if r["surface"] == "corpus_test_5splits"]
        self.assertTrue(rows)
        for r in rows:
            with self.subTest(r["order"], pool=r["pool"]):
                self.assertEqual([f["split"] for f in r["per_split"]],
                                 [0, 1, 2, 3, 4])

    def test_the_record_carries_its_environment(self):
        self.assertIn("pythonhashseed", self.payload["_env"])
        self.assertIn("code_digest", self.payload["_env"])


if __name__ == "__main__":
    unittest.main()
