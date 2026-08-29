"""
SNAPSHOT of the hybrid ceiling on both surfaces, and of what the edges buy.

`tests/test_ceilings.py` pins the hybrid engine's **corpus** row. This pins the
same engine over the 134,400 combinations, the level-1 row on both surfaces, and
the three premises that make the space figure a consequence rather than a
coincidence.

Why a figure is pinned here at all: same exception as `test_ceilings.py` and
`test_default_rule_control.py`. A ceiling with the perfect policy loaded is a
deterministic function of frozen material — the 29 rules, their derived edges,
the corpus of seed 17 — with no search, no sampling and no paid call in it.

What is pinned:

  hybrid, corpus       1.0000   (the gate; owned by results2/FINDINGS2.md)
  hybrid, space        1.0000   policy-equivalent, not "fits the sample"
  level 1, corpus      0.6315   (the gate; owned by results/FINDINGS.md route 3)
  level 1, space       0.2612   what subsumption alone is worth as a function
  199 edges: 148 ever fire on the corpus, 199 on the space

The space figures are owned by `results2/FINDINGS2.md`, section *The same ceiling
on the other surface*.

If one of these fails the expected number is NOT updated: find out what changed
and date the erratum in the FINDINGS that owns it (hard rule 6).

**The premises matter more than the ceiling.** 1.0000 over the space follows from
them by the argument in the module's docstring, so a test that only pinned the
1.0000 would keep passing while the reason for it rotted. Nothing here calls
`main()`, so nothing here writes to `results2/`.
"""

from __future__ import annotations

import json
import unittest
from functools import cache
from pathlib import Path

from harness.ceiling_check import all_cases
from rung2.ceiling_check2_space import (CORPUS, GATE_DECLARED_EDGES,
                                        GATE_SUBSUMPTION_PAIRS, HYBRID, LEVEL1,
                                        SPACE, build_level1_engine,
                                        check_premises, edge_work, measure)
from rung2.hidden_priority import build_hidden_engine

from .fixtures import SPACE_SIZE, corpus, space

RECORD = Path(__file__).resolve().parent.parent / "results2" / "ceiling2_space.json"

# --- the ceiling, by level and by surface ------------------------------------
HYB_CORPUS_E2E, HYB_SPACE_E2E = 1.0000, 1.0000
LV1_CORPUS_E2E, LV1_CORPUS_CONFLICT = 0.6315, 737
LV1_SPACE_E2E, LV1_SPACE_CONFLICT = 0.2612, 99_298
LV1_SPACE_ACTION = 35_102

# --- what the 199 edges buy ---------------------------------------------------
FIRE_CORPUS, FIRE_SPACE = 148, 199
SOLE_CORPUS, SOLE_SPACE = 60, 72
NEVER_FIRING_ON_THE_CORPUS = 51
SOLE_ON_THE_SPACE_ONLY, SOLE_ON_THE_CORPUS_ONLY = 12, 0


@cache
def hybrid():
    engine, declared, stats = build_hidden_engine(space())
    return engine, declared, stats


@cache
def level1():
    return build_level1_engine(space())


@cache
def cases():
    return tuple(all_cases())


@cache
def rows():
    engine, _declared, _stats = hybrid()
    return {
        (CORPUS, HYBRID): measure(engine, corpus(), CORPUS, HYBRID),
        (SPACE, HYBRID): measure(engine, cases(), SPACE, HYBRID),
        (CORPUS, LEVEL1): measure(level1(), corpus(), CORPUS, LEVEL1),
        (SPACE, LEVEL1): measure(level1(), cases(), SPACE, LEVEL1),
    }


@cache
def work():
    engine, _declared, _stats = hybrid()
    return {CORPUS: edge_work(engine, corpus(), CORPUS),
            SPACE: edge_work(engine, cases(), SPACE)}


class TestThePremisesOfTheProof(unittest.TestCase):
    """1.0000 over the space is a consequence of these three, not a coincidence.
    Each is a fact another record publishes; here they are re-derived from the
    engine itself."""

    @classmethod
    def setUpClass(cls):
        engine, _declared, stats = hybrid()
        cls.p = check_premises(engine, stats)

    def test_subsumption_never_contradicts_the_layer_order(self):
        """results/FINDINGS.md, route 3: 'contradictions with the layer order:
        0'. If this ever fires, a later rule strictly inside an earlier one would
        beat it and the engine would return the wrong action."""
        self.assertEqual(self.p["subsumption_contradicts_the_layer_order"], [])

    def test_the_validator_rejected_no_edge(self):
        self.assertEqual(self.p["edges_rejected_by_the_validator"], [])

    def test_no_pair_that_needs_an_edge_lacks_one(self):
        """Overlapping, incomparable and disagreeing on the action is exactly the
        pair that nothing else can order."""
        self.assertEqual(self.p["pairs_that_need_an_edge_and_lack_one"], [])

    def test_the_premises_pass_as_a_whole(self):
        self.assertTrue(self.p["passes"])


class TestTheTwoEnginesDifferOnlyInLevelTwo(unittest.TestCase):
    """Every comparison below is between these two, so if they differed anywhere
    else the 'what the edges buy' figures would be measuring something else."""

    def test_same_extensions_and_same_subsumption(self):
        engine, _d, _s = hybrid()
        lv1 = level1()
        self.assertEqual(engine.ext, lv1.ext)
        self.assertEqual(engine.sub_below, lv1.sub_below)
        self.assertEqual(engine.sub_above, lv1.sub_above)

    def test_level_1_has_no_declared_edge(self):
        self.assertTrue(all(not s for s in level1().decl_below.values()))
        self.assertTrue(all(not s for s in level1().decl_above.values()))

    def test_the_structure_is_the_published_one(self):
        engine, declared, _s = hybrid()
        self.assertEqual(len(declared), GATE_DECLARED_EDGES)
        self.assertEqual(sum(len(s) for s in engine.sub_below.values()),
                         GATE_SUBSUMPTION_PAIRS)


class TestTheCeilingOnBothSurfaces(unittest.TestCase):

    def test_the_corpus_row_is_the_gate_and_still_reproduces(self):
        r = rows()[(CORPUS, HYBRID)]
        self.assertEqual(r["action"], len(corpus()))
        self.assertEqual(r["conflict"], 0)
        self.assertEqual(r["impasse"], 0)
        self.assertEqual(r["accuracy_end_to_end"], HYB_CORPUS_E2E)

    def test_the_space_row_is_policy_equivalence(self):
        """Coverage 1.0, zero conflicts, zero impasses and zero silent errors
        over all 134,400 cases: the engine decides what first-match-wins decides
        on every case that exists, not on the 1,743 the corpus touches."""
        r = rows()[(SPACE, HYBRID)]
        self.assertEqual(r["n"], SPACE_SIZE)
        self.assertEqual(r["action"], SPACE_SIZE)
        self.assertEqual(r["conflict"], 0)
        self.assertEqual(r["impasse"], 0)
        self.assertEqual(r["silent_errors_abs"], 0)
        self.assertEqual(r["accuracy_end_to_end"], HYB_SPACE_E2E)

    def test_level_1_alone_on_the_corpus(self):
        r = rows()[(CORPUS, LEVEL1)]
        self.assertEqual(r["conflict"], LV1_CORPUS_CONFLICT)
        self.assertAlmostEqual(r["accuracy_end_to_end"], LV1_CORPUS_E2E, places=4)

    def test_level_1_alone_on_the_space(self):
        r = rows()[(SPACE, LEVEL1)]
        self.assertEqual(r["action"], LV1_SPACE_ACTION)
        self.assertEqual(r["conflict"], LV1_SPACE_CONFLICT)
        self.assertAlmostEqual(r["accuracy_end_to_end"], LV1_SPACE_E2E, places=4)

    def test_level_1_abstains_instead_of_inventing_on_both_surfaces(self):
        """Rung 1's 0.0000 silent error was a corpus figure. Subsumption is sound
        over the whole function too, which is the property that justifies level 1
        being non-negotiable."""
        for surface in (CORPUS, SPACE):
            with self.subTest(surface):
                r = rows()[(surface, LEVEL1)]
                self.assertEqual(r["silent_errors_abs"], 0)
                self.assertEqual(r["coverage"], r["accuracy_end_to_end"])

    def test_the_two_surfaces_disagree_about_level_1_and_agree_about_the_hybrid(self):
        """The point of measuring both. Level 1 covers 63% of the arrivals and
        26% of the function; the hybrid covers all of both."""
        self.assertGreater(rows()[(CORPUS, LEVEL1)]["accuracy_end_to_end"],
                           2 * rows()[(SPACE, LEVEL1)]["accuracy_end_to_end"])
        self.assertEqual(rows()[(CORPUS, HYBRID)]["accuracy_end_to_end"],
                         rows()[(SPACE, HYBRID)]["accuracy_end_to_end"])


class TestWhatTheEdgesBuy(unittest.TestCase):

    def test_cases_needing_an_edge_equal_level_1_conflicts(self):
        """Two ways of counting the same cases: the ones level 1 leaves in
        conflict are exactly the ones a declared edge has to decide. The module
        blocks if they disagree."""
        for surface in (CORPUS, SPACE):
            with self.subTest(surface):
                self.assertEqual(
                    work()[surface]["cases_whose_decision_needs_a_declared_edge"],
                    rows()[(surface, LEVEL1)]["conflict"])

    def test_how_many_edges_ever_fire(self):
        self.assertEqual(work()[CORPUS]["edges_that_ever_fire"], FIRE_CORPUS)
        self.assertEqual(work()[SPACE]["edges_that_ever_fire"], FIRE_SPACE)
        self.assertEqual(GATE_DECLARED_EDGES - FIRE_CORPUS,
                         NEVER_FIRING_ON_THE_CORPUS)

    def test_how_many_edges_are_ever_the_sole_defeater(self):
        self.assertEqual(work()[CORPUS]["edges_ever_sole_defeater"], SOLE_CORPUS)
        self.assertEqual(work()[SPACE]["edges_ever_sole_defeater"], SOLE_SPACE)

    def test_the_corpus_load_bearing_set_is_inside_the_space_one(self):
        """The asymmetry is one-directional, which is what makes the corpus a
        floor on the authorship cost rather than a different reading of it."""
        only_space = set(work()[SPACE]["sole"]) - set(work()[CORPUS]["sole"])
        only_corpus = set(work()[CORPUS]["sole"]) - set(work()[SPACE]["sole"])
        self.assertEqual(len(only_space), SOLE_ON_THE_SPACE_ONLY)
        self.assertEqual(len(only_corpus), SOLE_ON_THE_CORPUS_ONLY)

    def test_every_edge_fires_somewhere_on_the_space(self):
        """No edge is inert: `hidden_priority` only declares edges between rules
        whose extensions overlap, and over the whole space every overlap is
        eventually sampled."""
        _engine, declared, _stats = hybrid()
        self.assertEqual(set(work()[SPACE]["fires"]), set(declared))


class TestTheRecordOnDisk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads(RECORD.read_text())

    def test_it_declares_itself_post_run(self):
        self.assertTrue(self.rec["provenance"].startswith("POST-RUN"))

    def test_it_says_which_limit_it_closes(self):
        self.assertIn("9.2", self.rec["closes"])

    def test_its_gates_passed(self):
        self.assertTrue(self.rec["gates"]["passes"])
        self.assertTrue(self.rec["gates"]["engines_differ_only_in_level_2"])
        self.assertTrue(all(g["passes"] for g in self.rec["gates"]["rows"]))

    def test_step_0_on_the_space_passed(self):
        self.assertTrue(self.rec["step_0_on_the_space"])

    def test_the_four_rows_are_the_ones_measured_here(self):
        self.assertEqual(len(self.rec["rows"]), 4)
        for r in self.rec["rows"]:
            with self.subTest(r["surface"], arbitration=r["arbitration"]):
                m = rows()[(r["surface"], r["arbitration"])]
                self.assertEqual(r["action"], m["action"])
                self.assertEqual(r["conflict"], m["conflict"])
                self.assertEqual(r["accuracy_end_to_end"],
                                 m["accuracy_end_to_end"])

    def test_the_per_edge_table_covers_every_declared_edge(self):
        _engine, declared, _stats = hybrid()
        self.assertEqual(len(self.rec["per_edge"]), len(declared))
        self.assertEqual({(e["winner"], e["loser"]) for e in self.rec["per_edge"]},
                         set(declared))


if __name__ == "__main__":
    unittest.main()
