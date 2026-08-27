"""
THE SIDE DECOMPOSITION — its partition, its controls, no figure.

`edge_sides` asks what each side of B-d's split BUYS, as opposed to what the
proposer's RATE is on it. **No value of that answer is pinned here**; the figures
live in `results3/edge_sides.json` and in `results3/FINDINGS3.md`. What is pinned
is the machinery that decides whether the comparison means anything:

  * the three sides PARTITION the declared edges, so nothing is counted twice and
    nothing is dropped between them;
  * a pair the split record leaves without a side becomes `no_side` rather than
    silently joining one of the two that carry a claim;
  * a direction of `None` offers no edge — the channel has nothing to say on a
    tie, and forcing one would credit it with a coin flip it never made;
  * each subset is read against a coin on ITS OWN rows, because a subset with
    more edges scores higher for having more edges;
  * `no_side`'s oracle is arrival order exactly — those pairs have no strict
    better rule, so a perfect chooser offers nothing there and the compiled order
    is the floor. It is the one structural invariant of the decomposition, and it
    would break the moment the split and the oracle stopped agreeing about which
    pairs have a winner.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rung3.edge_sides import SIDES, oracle_of, score_of, sides_of

SPLIT = "results2/pair_sample_1600.json"
SOURCE = "results2/pair_judgement_1600.json"


class TestTheSplitIsReadNotInvented(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.side = sides_of(SPLIT)
        cls.oracle = oracle_of(SPLIT)

    def test_every_side_is_one_of_the_three(self):
        self.assertEqual(set(self.side.values()) - set(SIDES), set())

    def test_a_pair_without_a_side_becomes_no_side_not_a_claim(self):
        rec = json.loads(Path(SPLIT).read_text())
        blank = [(r["rule_a"], r["rule_b"]) for r in rec["oracle"]
                 if r["queue_ranking_space"] is None]
        self.assertTrue(blank, "the sample should contain ties and never-right pairs")
        for p in blank[:20]:
            self.assertEqual(self.side[p], "no_side")

    def test_no_side_is_exactly_where_the_oracle_offers_nothing(self):
        """The invariant the whole decomposition rests on: a pair has a side if
        and only if one rule is strictly better over the shared region."""
        for pair, s in self.side.items():
            with self.subTest(pair=pair):
                self.assertEqual(s == "no_side", self.oracle[pair] is None)

    def test_the_sides_partition_the_declared_edges(self):
        rows = [r for r in json.loads(Path(SOURCE).read_text())["answers"]
                if r["declared"] != "none"]
        counted = sum(
            1 for s in SIDES
            for r in rows
            if self.side.get((r["rule_a"], r["rule_b"]), "no_side") == s)
        self.assertEqual(counted, len(rows))


class TestADirectionOfNoneOffersNothing(unittest.TestCase):
    """Checked on the primitive rather than argued from the caller: a tie must
    contribute no edge, or the channel is credited with a flip it never made."""

    def test_none_rows_are_dropped_before_compilation(self):
        import rung3.edge_sides as mod
        seen = {}
        real = (mod.accepted_from, mod.topological_order, mod.floor)
        mod.accepted_from = lambda rows, dirs, rules, engine=None: (
            seen.update(n=len(rows), dirs=list(dirs)) or [])
        mod.topological_order = lambda ids, edges, born: []
        mod.floor = lambda order, instance: 0.0
        try:
            rows = [{"rule_a": f"A{k}", "rule_b": f"B{k}"} for k in range(4)]
            score_of(rows, [True, None, False, None], None, [], {}, None, None)
        finally:
            mod.accepted_from, mod.topological_order, mod.floor = real
        self.assertEqual(seen["n"], 2)
        self.assertEqual(seen["dirs"], [True, False])

    def test_every_direction_present_keeps_every_row(self):
        import rung3.edge_sides as mod
        seen = {}
        real = (mod.accepted_from, mod.topological_order, mod.floor)
        mod.accepted_from = lambda rows, dirs, rules, engine=None: (
            seen.update(n=len(rows)) or [])
        mod.topological_order = lambda ids, edges, born: []
        mod.floor = lambda order, instance: 0.0
        try:
            rows = [{"rule_a": f"A{k}", "rule_b": f"B{k}"} for k in range(3)]
            score_of(rows, [True, False, True], None, [], {}, None, None)
        finally:
            mod.accepted_from, mod.topological_order, mod.floor = real
        self.assertEqual(seen["n"], 3)


class TestTheRecordsControls(unittest.TestCase):
    """Each subset must be read against a coin on its own rows, and the record
    has to carry the counts that let that be checked by hand."""

    @classmethod
    def setUpClass(cls):
        p = Path("results3/edge_sides.json")
        if not p.exists():
            raise unittest.SkipTest("edge_sides has not been run")
        cls.rec = json.loads(p.read_text())

    def test_every_subset_carries_its_own_coin_and_oracle(self):
        for name, r in self.rec["by_side"].items():
            with self.subTest(name):
                for k in ("coin", "oracle", "model", "n_rows",
                          "model_in_coin_deviations",
                          "oracle_in_coin_deviations"):
                    self.assertIn(k, r)

    def test_the_three_sides_sum_to_all(self):
        b = self.rec["by_side"]
        self.assertEqual(sum(b[s]["n_rows"] for s in SIDES), b["all"]["n_rows"])
        self.assertEqual(b["all"]["n_rows"], self.rec["n_declared_edges"])

    def test_no_sides_oracle_is_the_arrival_floor(self):
        """A perfect chooser offers nothing where no rule is better, so its
        compiled order is born_at exactly."""
        self.assertEqual(self.rec["by_side"]["no_side"]["oracle"],
                         self.rec["born_at_floor"])
        self.assertEqual(self.rec["by_side"]["no_side"]["oracle_offers"], 0)

    def test_it_says_it_adjudicates_nothing(self):
        self.assertIn("POST-RUN", self.rec["provenance"])
        self.assertIn("no row", self.rec["adjudicates_nothing"])


if __name__ == "__main__":
    unittest.main()
