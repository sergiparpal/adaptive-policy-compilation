"""
THE QUEUE-HIERARCHY CONTROL — its arithmetic and its read gate, no figure.

`queue_hierarchy_floor` answers one question with zero API calls: how much of
P-d's band does an order that knows only the queue ranking already reach? **No
figure of that answer is pinned here** — what the best of 40,320 hierarchies
scores, what Stage C's transferred ranking scores, and where either sits against
the floor live in `results3/queue_hierarchy_floor.json` and in the write-up.

What is pinned:

  * a hierarchy order reads the rule's ACTION and nothing else — not its
    conditions, not its extension, not what any other rule does. That is the
    whole content of the control, and a version that peeked would make the
    comparison meaningless while still producing a plausible number;
  * both tie-breaks do what they say, so the control is reported at its
    strongest rather than at whichever one happened to be written first;
  * the enumeration covers the whole permutation group and its maximum is a
    maximum;
  * the floor is READ from the record that owns it, and the gate fails when a
    cell this control needs is absent.
"""

from __future__ import annotations

import itertools
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from rung3.floor_by_pool import POOLS
from rung3.queue_hierarchy_floor import (P_D_MARGIN, STAGE_C_HIERARCHY,
                                         TIEBREAKS, enumerate_hierarchies,
                                         gate_tiebreak_irrelevant,
                                         hierarchy_order, read_floor)

IDS = ["R1", "R2", "R3", "R4"]
ACTION = {"R1": "AAA", "R2": "BBB", "R3": "AAA", "R4": "BBB"}
BORN = {"R1": 10, "R2": 20, "R3": 30, "R4": 40}


class TestTheInducedOrder(unittest.TestCase):

    def test_it_sorts_by_the_rank_of_the_action(self):
        o = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1})
        self.assertEqual(o, ["R1", "R3", "R2", "R4"])
        o = hierarchy_order(IDS, ACTION, BORN, {"BBB": 0, "AAA": 1})
        self.assertEqual(o, ["R2", "R4", "R1", "R3"])

    def test_the_tiebreak_inside_a_class_is_arrival_order(self):
        o = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1}, "born_at")
        self.assertEqual(o[:2], ["R1", "R3"])

    def test_the_reversed_tiebreak_flips_only_inside_the_class(self):
        o = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1},
                            "born_at_reversed")
        self.assertEqual(o, ["R3", "R1", "R4", "R2"])

    def test_both_declared_tiebreaks_are_exercised(self):
        """They produce different ORDERS. That they produce the same SCORE is a
        separate fact, proved and gated below."""
        self.assertEqual(set(TIEBREAKS), {"born_at", "born_at_reversed"})
        a = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1}, TIEBREAKS[0])
        b = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1}, TIEBREAKS[1])
        self.assertNotEqual(a, b)

    def test_it_reads_the_action_and_nothing_else(self):
        """Two rules with different conditions, extensions and fire counts and
        the same action must be interchangeable to it. A control that peeked at
        the material would still return a number, and the number would mean
        nothing."""
        o = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1})
        other_action = dict(ACTION, R3="BBB")
        o2 = hierarchy_order(IDS, other_action, BORN, {"AAA": 0, "BBB": 1})
        self.assertNotEqual(o, o2)          # the action moves it
        self.assertEqual(hierarchy_order(IDS, ACTION, BORN,
                                         {"AAA": 0, "BBB": 1}), o)

    def test_every_rule_appears_exactly_once(self):
        o = hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1})
        self.assertEqual(sorted(o), sorted(IDS))


# Four cases and four rules that actually compete, which the first version of
# this fixture did not: there, every rule matched a case of its own and no order
# could change anything.
#
#   truth   c0=AAA  c1=AAA  c2=AAA  c3=BBB
#   R1 AAA  matches {0,1}   right on both
#   R3 AAA  matches {1,2}   right on both      (shares c1 with R1, and agrees:
#   R2 BBB  matches {0,1}   right on neither    two rules of one class cannot
#   R4 BBB  matches {3}     right on it         disagree, they carry one action)
#
# AAA > BBB scores 4/4; BBB > AAA scores 2/4; and no reordering INSIDE a class
# moves either, which is the property under test.
N = 4
FULL = (1 << N) - 1


def _mask(cases):
    return sum(1 << c for c in cases)


M = {"R1": _mask([0, 1]), "R3": _mask([1, 2]),
     "R2": _mask([0, 1]), "R4": _mask([3])}
W = {"R1": _mask([0, 1]), "R3": _mask([1, 2]),
     "R2": 0, "R4": _mask([3])}
INSTANCE = (M, W, FULL, N)


class TestTheEnumeration(unittest.TestCase):

    def test_it_covers_the_whole_permutation_group(self):
        e = enumerate_hierarchies(IDS, ACTION, BORN, INSTANCE, ["AAA", "BBB"],
                                  "born_at")
        self.assertEqual(e["n_orders"], 2)
        e3 = enumerate_hierarchies(IDS, ACTION, BORN, INSTANCE,
                                   ["AAA", "BBB", "CCC"], "born_at")
        self.assertEqual(e3["n_orders"], 6)

    def test_the_best_is_a_maximum_over_that_group(self):
        actions = ["AAA", "BBB"]
        e = enumerate_hierarchies(IDS, ACTION, BORN, INSTANCE, actions,
                                  "born_at")
        from rung3.floor_by_pool import floor
        by_hand = max(
            floor(hierarchy_order(IDS, ACTION, BORN,
                                  {a: i for i, a in enumerate(p)}), INSTANCE)
            for p in itertools.permutations(actions))
        self.assertAlmostEqual(e["best"], round(by_hand, 6))

    def test_the_spread_travels_with_the_maximum(self):
        """`best` is a winning ticket chosen with the labels. Without the mean
        and the deviation beside it a reader takes it for a level."""
        e = enumerate_hierarchies(IDS, ACTION, BORN, INSTANCE, ["AAA", "BBB"],
                                  "born_at")
        for k in ("mean", "median", "sd", "worst"):
            self.assertIn(k, e)
        self.assertLessEqual(e["worst"], e["mean"])
        self.assertLessEqual(e["mean"], e["best"])

    def test_it_names_the_hierarchy_that_won(self):
        e = enumerate_hierarchies(IDS, ACTION, BORN, INSTANCE, ["AAA", "BBB"],
                                  "born_at")
        self.assertEqual(sorted(e["best_hierarchy"]), ["AAA", "BBB"])


class TestTheTiebreakCannotChangeTheScore(unittest.TestCase):
    """
    Under a class-grouped order the winner of a case belongs to the
    highest-ranked action among those of the rules matching it, and every rule in
    that class carries that action. So the score is a function of the hierarchy
    alone. It is a proof; these are the checks that the code obeys it.

    It matters twice: the control cannot be weakened by a badly chosen
    tie-break, and `best` over the 40,320 is the exact ceiling of the family
    rather than the best anyone happened to find.
    """

    def test_any_shuffle_inside_the_classes_scores_the_same(self):
        import random

        from rung3.floor_by_pool import floor

        rank = {"AAA": 0, "BBB": 1}
        seen = set()
        for seed in range(6):
            rnd = random.Random(seed)
            order = sorted(IDS, key=lambda r: (rank[ACTION[r]], rnd.random()))
            seen.add(floor(order, INSTANCE))
        self.assertEqual(len(seen), 1)

    def test_the_two_declared_tiebreaks_score_the_same(self):
        from rung3.floor_by_pool import floor

        rank = {"AAA": 0, "BBB": 1}
        vals = {floor(hierarchy_order(IDS, ACTION, BORN, rank, tb), INSTANCE)
                for tb in TIEBREAKS}
        self.assertEqual(len(vals), 1)

    def test_changing_the_hierarchy_does_move_it(self):
        """The counterpart. If nothing moved the score the test above would be
        vacuous."""
        from rung3.floor_by_pool import floor

        a = floor(hierarchy_order(IDS, ACTION, BORN, {"AAA": 0, "BBB": 1}),
                  INSTANCE)
        b = floor(hierarchy_order(IDS, ACTION, BORN, {"BBB": 0, "AAA": 1}),
                  INSTANCE)
        self.assertNotEqual(a, b)

    def test_the_gate_passes_when_the_two_agree(self):
        rows = [{"pool": "hibrido", "surface": "space", "tiebreak": tb,
                 "best": 0.6, "mean": 0.3, "stage_c": 0.58} for tb in TIEBREAKS]
        self.assertTrue(gate_tiebreak_irrelevant(rows)["passes"])

    def test_the_gate_fails_when_they_do_not(self):
        rows = [{"pool": "hibrido", "surface": "space", "tiebreak": TIEBREAKS[0],
                 "best": 0.6, "mean": 0.3, "stage_c": 0.58},
                {"pool": "hibrido", "surface": "space", "tiebreak": TIEBREAKS[1],
                 "best": 0.6, "mean": 0.3, "stage_c": 0.59}]
        g = gate_tiebreak_irrelevant(rows)
        self.assertFalse(g["passes"])
        self.assertEqual(g["cells_that_differ"][0]["surface"], "space")

    def test_a_cell_with_only_one_tiebreak_is_not_a_disagreement(self):
        rows = [{"pool": "puro", "surface": "space", "tiebreak": TIEBREAKS[0],
                 "best": 0.6, "mean": 0.3, "stage_c": 0.58}]
        self.assertTrue(gate_tiebreak_irrelevant(rows)["passes"])


class TestTheFloorIsReadAndNotRecomputed(unittest.TestCase):

    def _record(self, cells):
        return {"floors": [
            {"order": "born_at", "generator": None, "pool": p,
             "surface": s, "value": v} for (p, s), v in cells.items()]}

    def _all_cells(self):
        return {(p, s): 0.4 for p in POOLS
                for s in ("corpus_full", "corpus_test_split0",
                          "corpus_test_5splits", "space")}

    def write(self, tmp, rec):
        path = Path(tmp) / "floor_by_pool.json"
        path.write_text(json.dumps(rec))
        return path

    def test_it_passes_when_every_cell_it_needs_is_published(self):
        with TemporaryDirectory() as tmp:
            out, g = read_floor(self.write(tmp, self._record(self._all_cells())))
            self.assertTrue(g["passes"])
            self.assertEqual(g["missing"], [])
            self.assertEqual(len(out), 8)

    def test_a_missing_cell_stops_the_run(self):
        cells = self._all_cells()
        del cells[("hibrido", "corpus_test_split0")]
        with TemporaryDirectory() as tmp:
            _out, g = read_floor(self.write(tmp, self._record(cells)))
            self.assertFalse(g["passes"])
            self.assertIn(["hibrido", "corpus_test_split0"], g["missing"])

    def test_extra_cells_do_not_bother_it(self):
        """floor_by_pool publishes five per-split rows this control aggregates
        away. The gate is on what it reads, not on the record's total."""
        cells = self._all_cells()
        cells[("puro", "corpus_test_split3")] = 0.51
        with TemporaryDirectory() as tmp:
            _out, g = read_floor(self.write(tmp, self._record(cells)))
            self.assertTrue(g["passes"])

    def test_only_the_born_at_rows_are_read(self):
        """The record also carries reversed and random rows. Picking one of
        those up would compare the control against the wrong floor."""
        rec = self._record(self._all_cells())
        rec["floors"].append({"order": "born_at_reversed", "generator": None,
                              "pool": "hibrido", "surface": "space",
                              "value": 0.99})
        with TemporaryDirectory() as tmp:
            out, _g = read_floor(self.write(tmp, rec))
            self.assertEqual(out[("hibrido", "space")], 0.4)

    def test_a_random_row_is_never_mistaken_for_the_floor(self):
        rec = self._record(self._all_cells())
        rec["floors"].append({"order": "born_at", "generator": "whatever",
                              "pool": "puro", "surface": "space",
                              "value": 0.99})
        with TemporaryDirectory() as tmp:
            out, _g = read_floor(self.write(tmp, rec))
            self.assertEqual(out[("puro", "space")], 0.4)


class TestWhatTheControlCarries(unittest.TestCase):

    def test_the_margin_is_the_one_p_d_was_signed_with(self):
        self.assertEqual(P_D_MARGIN, 0.03)

    def test_the_transferred_hierarchy_is_a_permutation_of_the_eight_queues(self):
        from harness.domain import ACTIONS

        self.assertEqual(sorted(STAGE_C_HIERARCHY), sorted(ACTIONS))

    def test_it_is_the_order_stage_c_published(self):
        """Transcribed from results2/pair_judgement_baselines.json. If that
        record ever moves, this is what says the control stopped tracking it."""
        rec = Path("results2/pair_judgement_baselines.json")
        if not rec.exists():
            self.skipTest("stage C baselines not recorded here")
        published = json.loads(rec.read_text())["hierarchy"]["best_order"]
        self.assertEqual(STAGE_C_HIERARCHY, published)


if __name__ == "__main__":
    unittest.main()
