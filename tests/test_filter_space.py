"""
§16'S CUTS OVER THE FUNCTION — one compilation, two surfaces, no figure.

**No score is pinned here.** The figures live in `results3/filter_space.json` and
in `results3/FINDINGS3.md` §17. What is pinned is what makes the space side
§16's selections and nothing else:

  * the controls draw exactly the subsets `filter_headroom.control` draws, and
    on the corpus they return exactly what it returns;
  * one compilation is scored on every surface it is handed;
  * gate 1 compares every leaf and names the first that differs, and gate 2
    compares the two published space figures;
  * the expectation is read mechanically, clause by clause, and its third line
    is §16's own reading;
  * the diagnostics follow `edge_direction.agreement`'s convention.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rung3 import filter_headroom as fh
from rung3 import filter_space as fs

REPO = Path(__file__).resolve().parent.parent
X, Y = "QUEUE_X", "QUEUE_Y"


def row(i, declared="a_beats_b"):
    return {"index": i, "rule_a": f"R{i}a", "rule_b": f"R{i}b", "action_a": X,
            "action_b": Y, "declared": declared, "why": ""}


def value_of(kept):
    """A score that moves with the subset, so means and spreads are not trivial."""
    s = sum(r["index"] for r in kept)
    return {"topological": round((s % 97) / 97, 6), "mfas": round((s % 89) / 89, 6)}


class TestTheConstants(unittest.TestCase):

    def test_the_record_and_the_surfaces(self):
        self.assertEqual(fs.RECORD, "filter_space.json")
        self.assertEqual(fs.SURFACES, ("corpus", "space"))
        self.assertEqual(fs.COMPILATIONS, ("topological", "mfas"))

    def test_gate_1_reads_every_figure_section_of_16s_record(self):
        published = json.loads((REPO / fs.HEADROOM).read_text())
        for key in fs.GATED:
            with self.subTest(key):
                self.assertIn(key, published)

    def test_clause_3s_line_is_16s_own_reading(self):
        published = json.loads((REPO / fs.HEADROOM).read_text())
        reading = published["filters"]["no_queue"]["against_random_in_arrival_order"]
        self.assertEqual(fs.CORPUS_MFAS_NO_QUEUE, reading["mfas_deviations"])


class TestOneCompilationTwoSurfaces(unittest.TestCase):

    def test_each_order_is_scored_on_each_surface(self):
        # r1 is right on both of its cases, r2 on neither: the order matters.
        inst = ({"r1": 0b0011, "r2": 0b0110}, {"r1": 0b0011, "r2": 0b0000}, 0b1111, 4)
        orders = {"topological": ["r1", "r2"], "mfas": ["r2", "r1"]}
        got = fs.scored(orders, {"corpus": inst, "space": inst})
        self.assertEqual(got, {"corpus": {"topological": 0.5, "mfas": 0.25},
                               "space": {"topological": 0.5, "mfas": 0.25}})


class TestTheControlsAre16s(unittest.TestCase):

    def test_the_same_subsets_are_drawn(self):
        rows = [row(i) for i in range(60)]
        for sampler, name in ((fh.in_arrival_order, "arrival"), (fh.shuffled, "shuffled")):
            seen_fh, seen_fs = [], []

            def one(kept):
                seen_fh.append([r["index"] for r in kept])
                return value_of(kept)

            def both(kept):
                seen_fs.append([r["index"] for r in kept])
                return {s: value_of(kept) for s in fs.SURFACES}

            with self.subTest(name):
                fh.control(rows, 17, sampler, name, one, draws=6)
                fs.control(rows, 17, sampler, name, both, draws=6)
                self.assertEqual(seen_fh, seen_fs)

    def test_on_the_same_scores_it_returns_what_16_returns(self):
        rows = [row(i) for i in range(60)]
        a = fh.control(rows, 17, fh.in_arrival_order, "arrival", value_of, draws=6)
        b = fs.control(rows, 17, fh.in_arrival_order, "arrival",
                       lambda kept: {s: value_of(kept) for s in fs.SURFACES}, draws=6)
        self.assertEqual(b["corpus"], a)
        self.assertEqual(b["space"], a)
        self.assertGreater(a["topological"]["sd"], 0)

    def test_against_is_16s_deviations(self):
        ctl = {"topological": {"mean": 0.4, "sd": 0.05}, "mfas": {"mean": 0.5, "sd": 0.0}}
        self.assertEqual(fs.against({"topological": 0.5, "mfas": 0.6}, ctl),
                         {"topological_deviations": 2.0, "mfas_deviations": None})


class TestTheGates(unittest.TestCase):

    PUBLISHED = {"born_at_floor": 0.4, "headroom_by_size": {"10": {"x": 0.1}},
                 "shuffled_controls_at_14s_sizes": {"keep_all": {"y": 0.2}},
                 "filters": {"queue": {"topological": 0.3, "n_kept": 5}}}

    def test_differences_names_leaves_and_keys(self):
        self.assertEqual(fs.differences({"a": {"b": 1}}, {"a": {"b": 1}}), [])
        self.assertEqual(fs.differences({"a": {"b": 1}}, {"a": {"b": 2}}),
                         ["/a/b: 1 != 2"])
        self.assertEqual(fs.differences({"a": 1, "c": 2}, {"a": 1}),
                         ["/c: missing on one side"])

    def test_gate_1_passes_only_on_every_leaf(self):
        mine = json.loads(json.dumps(self.PUBLISHED))
        mine["born_at_floor"] = 0.40000004          # rounds to the published value
        g = fs.gate_headroom(mine, self.PUBLISHED)
        self.assertTrue(g["passes"])
        self.assertEqual(sum(r["figures"] for r in g["rows"].values()), 5)
        mine["filters"]["queue"]["topological"] = 0.3001
        g = fs.gate_headroom(mine, self.PUBLISHED)
        self.assertFalse(g["passes"])
        self.assertEqual(g["rows"]["filters"]["first_differences"],
                         ["filters/queue/topological: 0.3001 != 0.3"])

    def test_gate_2_compares_both_published_figures(self):
        pub = {"born_at_floor": 0.425, "keep_all_topological": 0.546,
               "queue_ranking_stage_c": 0.58}
        self.assertTrue(fs.gate_space(0.4250001, 0.546, pub)["passes"])
        g = fs.gate_space(0.425, 0.547, pub)
        self.assertFalse(g["passes"])
        self.assertFalse(g["rows"]["keep_all_topological"]["passes"])

    def test_the_published_space_rows_are_found(self):
        pub = fs.published_space()
        self.assertEqual(set(pub), {"born_at_floor", "keep_all_topological",
                                    "queue_ranking_stage_c"})
        for v in pub.values():
            self.assertIsInstance(v, float)


class TestTheExpectation(unittest.TestCase):

    def filters(self, nq_topo, nq_mfas, q_topo, q_mfas):
        def e(t, m):
            return {"against_random_in_arrival_order": {"topological_deviations": t,
                                                        "mfas_deviations": m}}
        return {"no_queue": e(nq_topo, nq_mfas), "queue": e(q_topo, q_mfas)}

    def test_the_clauses_as_written(self):
        read = fs.read_expectation(self.filters(-0.4, -1.1, 0.8, 1.9))
        self.assertEqual([r["clause"] for r in read], ["1", "1", "2", "2", "3"])
        self.assertTrue(all(r["holds"] for r in read))

    def test_each_clause_can_fail(self):
        read = fs.read_expectation(self.filters(0.4, -3.0, -0.8, 1.9))
        self.assertEqual([r["holds"] for r in read], [False, True, False, True, False])

    def test_an_unreadable_reading_is_not_a_verdict(self):
        read = fs.read_expectation(self.filters(None, -1.0, 1.0, 1.0))
        self.assertIsNone(read[0]["holds"])


class TestTheDiagnostics(unittest.TestCase):

    def test_direction_follows_agreements_convention(self):
        truth = {0: {"better_space": "a", "better_corpus": "b"},
                 1: {"better_space": "a", "better_corpus": "tie"},
                 2: {"better_space": "neither_ever_right", "better_corpus": "a"}}
        cuts = {"queue": [row(0), row(1, "b_beats_a"), row(2)]}
        got = fs.direction_by_cut(cuts, truth)["queue"]
        self.assertEqual((got["space"]["n"], got["space"]["rate"]), (2, 0.5))
        self.assertEqual(got["space"]["outside_the_denominator"],
                         {"neither_ever_right": 1})
        self.assertEqual((got["corpus"]["n"], got["corpus"]["rate"]), (2, 0.5))

    def test_queues_named_reads_the_declared_winner(self):
        self.assertEqual(fs.queues_named([row(0), row(1, "b_beats_a"), row(2)]),
                         {X: 2, Y: 1})


if __name__ == "__main__":
    unittest.main()
