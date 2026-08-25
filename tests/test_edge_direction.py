"""
THE DIRECTION OF THE DECLARED EDGES — its plumbing, and B-d's split.

`edge_direction` measures whether a declared edge points at the rule that gets
more of the shared region right. **No rate is pinned here**: the 400-pair figures
live in `results3/edge_direction.json` and in `results3/FINDINGS3.md` §9, and
`PLAN_PROPOSER_1600.md` asks the same question again at 1,600 with no figure of
its own yet.

What is pinned is the machinery that keeps the two measurements comparable and
the closed one intact:

  * a second population cannot land on the closed thread's record by omission;
  * `B-d`'s split is READ from the record that fixed it before any call, never
    recomputed from the answers it is supposed to predict;
  * both sides of the split are scored by calling `agreement`, so a difference
    between them is a difference in the pairs and not in the arithmetic.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from rung3.edge_direction import (OUT, RECORD, SOURCE, agreement,
                                  agreement_by_side, parse_source, read_split)

A, B, C, D = "R0001", "R0002", "R0003", "R0004"


def row(a, b, declared, better):
    return {"rule_a": a, "rule_b": b, "declared": declared,
            "better_space": better}


class TestTheSourceAndItsDestination(unittest.TestCase):

    def test_no_arguments_reads_and_writes_the_closed_thread(self):
        source, out, split = parse_source([])
        self.assertEqual(source, SOURCE)
        self.assertEqual(out, OUT / RECORD)
        self.assertIsNone(split)

    def test_another_source_without_a_destination_aborts(self):
        """`results3/edge_direction.json` belongs to the 400 pairs of Stage D.
        A larger population must not reach it by forgetting a flag."""
        with self.assertRaises(SystemExit):
            parse_source(["--source", "results2/other.json"])

    def test_another_source_with_a_destination_is_allowed(self):
        source, out, _ = parse_source(
            ["--source", "results2/pair_judgement_1600.json",
             "--out", "results3/edge_direction_1600.json"])
        self.assertEqual(source, Path("results2/pair_judgement_1600.json"))
        self.assertEqual(out, Path("results3/edge_direction_1600.json"))

    def test_the_default_source_may_be_written_elsewhere(self):
        """Re-running the closed figure into a scratch file is how it is checked
        that it still reproduces, and that must not need a source flag."""
        source, out, _ = parse_source(["--out", "/tmp/scratch.json"])
        self.assertEqual(source, SOURCE)
        self.assertEqual(out, Path("/tmp/scratch.json"))

    def test_the_split_is_optional_and_independent(self):
        _s, _o, split = parse_source(["--split", "results2/pair_sample_1600.json"])
        self.assertEqual(split, Path("results2/pair_sample_1600.json"))


class TestTheSplitIsRead(unittest.TestCase):

    def record(self, tmp):
        path = Path(tmp) / "sample.json"
        path.write_text(json.dumps({"oracle": [
            {"rule_a": A, "rule_b": B, "queue_ranking_space": "reachable",
             "queue_ranking_corpus": "unreachable"},
            {"rule_a": C, "rule_b": D, "queue_ranking_space": None,
             "queue_ranking_corpus": None},
        ]}))
        return path

    def test_it_reads_the_side_of_the_surface_it_is_asked_for(self):
        with TemporaryDirectory() as tmp:
            path = self.record(tmp)
            self.assertEqual(read_split(path, "better_space"),
                             {(A, B): "reachable"})
            self.assertEqual(read_split(path, "better_corpus"),
                             {(A, B): "unreachable"})

    def test_pairs_with_no_side_are_absent_rather_than_null(self):
        """A pair with no strict better rule has no side, and `agreement`
        already puts it outside every denominator."""
        with TemporaryDirectory() as tmp:
            self.assertNotIn((C, D), read_split(self.record(tmp),
                                                "better_space"))


class TestBdReadsTwoRatesOnOneDenominatorRule(unittest.TestCase):

    ROWS = [
        row(A, B, "a_beats_b", "a"),       # reachable, hit
        row(A, C, "b_beats_a", "a"),       # reachable, miss
        row(B, C, "a_beats_b", "b"),       # unreachable, miss
        row(B, D, "b_beats_a", "a"),       # unreachable, miss
        row(C, D, "a_beats_b", "tie"),     # no side at all
    ]
    SIDE = {(A, B): "reachable", (A, C): "reachable",
            (B, C): "unreachable", (B, D): "unreachable"}

    def result(self):
        return agreement_by_side(self.ROWS, "better_space", self.SIDE)

    def test_each_side_gets_its_own_n(self):
        r = self.result()
        self.assertEqual(r["reachable"]["n"], 2)
        self.assertEqual(r["unreachable"]["n"], 2)

    def test_the_two_rates_are_the_ones_agreement_would_give(self):
        """Scored by calling `agreement`, not by a second implementation of it."""
        r = self.result()
        reach = [x for x in self.ROWS
                 if self.SIDE.get((x["rule_a"], x["rule_b"])) == "reachable"]
        self.assertEqual(r["reachable"], agreement(reach, "better_space"))

    def test_a_pair_with_no_side_is_counted_apart(self):
        self.assertEqual(self.result()["n_without_a_side"], 1)

    def test_the_band_holds_when_the_unreachable_rate_is_lower(self):
        r = self.result()
        self.assertEqual(r["rate_unreachable"], 0.0)
        self.assertEqual(r["rate_reachable"], 0.5)
        self.assertTrue(r["band_holds"])

    def test_the_band_is_refuted_when_the_rates_are_equal(self):
        """Its edge is its own refutation line: `<` holds and `>=` refutes, so
        nothing can fall between them."""
        rows = [row(A, B, "a_beats_b", "a"), row(B, C, "a_beats_b", "b")]
        side = {(A, B): "reachable", (B, C): "unreachable"}
        r = agreement_by_side(rows, "better_space", side)
        self.assertEqual((r["rate_reachable"], r["rate_unreachable"]),
                         (1.0, 0.0))
        rows = [row(A, B, "a_beats_b", "a"), row(B, C, "a_beats_b", "b")]
        side = {(A, B): "reachable", (B, C): "reachable"}
        r = agreement_by_side(rows, "better_space", side)
        self.assertIsNone(r["rate_unreachable"])
        self.assertIsNone(r["band_holds"])

    def test_an_empty_side_gives_no_rate_rather_than_a_zero(self):
        """A rate of None is `nothing to read`; a rate of 0.0 would read as a
        proposer that got everything wrong."""
        r = agreement_by_side([row(A, B, "a_beats_b", "a")], "better_space",
                              {(A, B): "reachable"})
        self.assertIsNone(r["unreachable"]["rate"])
        self.assertIsNone(r["difference"])


if __name__ == "__main__":
    unittest.main()
