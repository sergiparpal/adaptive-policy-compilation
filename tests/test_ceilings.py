"""
SNAPSHOT of the ceilings: the published figures, pinned to the digit.

The four arbitrations are measured over EXACTLY the same 29 rules and the same
corpus. The only thing that changes between them is how it is resolved which
rule wins, which is precisely what the four rungs investigate.

  specificity   0.5875   the rung 1 defect; 505 CONFLICT
  subsumption   0.6315   abstains instead of inventing: 0 silent error
  hybrid        1.0000   subsumption + 199 declared edges (rung 2)
  priority      1.0000   first-match-wins, the semantics of the policy

If one of these tests fails, the expected number is NOT updated: you find out
what changed and date the erratum in the corresponding FINDINGS.

Sources: results/FINDINGS.md (0.5875 and 0.6315), results2/FINDINGS2.md
(1.0000), CLAUDE.md Step 0. No test here calls a `main()`, so results/ and
results2/ are not touched.
"""

from __future__ import annotations

import unittest
from collections import Counter

from harness.ceiling_check import build_rules, decide_by_priority, measure
from harness.dsl import RuleEngine
from harness.hidden_policy import true_action
from rung2.ceiling_check2 import REF
from rung2.hidden_priority import build_hidden_engine

from .fixtures import corpus, space, subsumption_only_engine

# --- rung 1, specificity arbitration (RuleEngine.decide) --------------------
SPEC_ACTION, SPEC_IMPASSE, SPEC_CONFLICT = 1495, 0, 505
SPEC_COVERAGE, SPEC_SILENT, SPEC_E2E = 0.7475, 0.2140, 0.5875
SPEC_SILENT_ABS = 320

# --- rung 1, subsumption alone ---------------------------------------------
SUB_ACTION, SUB_CONFLICT, SUB_E2E = 1263, 737, 0.6315

# --- rung 2, hybrid ----------------------------------------------------------
HYB_DECLARED_EDGES = 199        # authorship cost of this policy
HYB_SUBSUMPTION_PAIRS = 61      # pairs the structure already orders on its own
HYB_POSSIBLE_PAIRS = 29 * 28 // 2


def medir(engine_decide) -> dict:
    """Counts ACTION/IMPASSE/CONFLICT and correct decisions over the corpus."""
    out = Counter()
    ok = 0
    for case in corpus():
        outcome, winner, _ = engine_decide(case)
        out[outcome] += 1
        if outcome == "ACTION" and winner.action == true_action(case):
            ok += 1
    n = len(corpus())
    return {"out": out, "correct": ok, "e2e": ok / n,
            "silent": (1 - ok / out["ACTION"]) if out["ACTION"] else 0.0}


class TestCeilingBySpecificity(unittest.TestCase):
    """STOP 0 of CLAUDE.md: while this is not ~100%, every LLM run is voided in
    advance. It still is not, and that is the recorded figure."""

    @classmethod
    def setUpClass(cls):
        engine = RuleEngine()
        engine.rules = build_rules()
        cls.m = measure(list(corpus()), engine.decide, "especificidad")

    def test_outcome_split(self):
        self.assertEqual(self.m["action"], SPEC_ACTION)
        self.assertEqual(self.m["impasse"], SPEC_IMPASSE)
        self.assertEqual(self.m["conflict"], SPEC_CONFLICT)

    def test_coverage(self):
        self.assertAlmostEqual(self.m["coverage"], SPEC_COVERAGE, places=4)

    def test_silent_error(self):
        self.assertAlmostEqual(self.m["silent_error_rate"], SPEC_SILENT, places=4)
        self.assertEqual(self.m["silent_errors_abs"], SPEC_SILENT_ABS)

    def test_end_to_end_accuracy(self):
        self.assertAlmostEqual(self.m["accuracy_end_to_end"], SPEC_E2E, places=4)

    def test_the_25_percent_of_conflicts(self):
        self.assertAlmostEqual(SPEC_CONFLICT / len(corpus()), 0.2525, places=4)

    def test_does_not_reach_STOP_0(self):
        """Documents the state, does not approve it: if one day this fails
        because the ceiling rose to ~100%, all of CLAUDE.md must be revisited."""
        self.assertLess(self.m["accuracy_end_to_end"], 0.995)


class TestCeilingByPriority(unittest.TestCase):
    """With the rules in HIDDEN_RULES order, the oldest winning IS the
    first-match-wins semantics of the policy. It must give exactly 100%."""

    @classmethod
    def setUpClass(cls):
        rules = build_rules()
        cls.m = measure(list(corpus()),
                        lambda c: decide_by_priority(rules, c), "prioridad")

    def test_covers_everything_and_gets_everything_right(self):
        self.assertEqual(self.m["action"], len(corpus()))
        self.assertEqual(self.m["impasse"], 0)
        self.assertEqual(self.m["conflict"], 0)
        self.assertEqual(self.m["accuracy_end_to_end"], 1.0)
        self.assertEqual(self.m["silent_error_rate"], 0.0)

    def test_the_reverse_order_does_not_manage_it(self):
        """The order matters and is not a detail: reversing it destroys the
        policy (12.8% in FINDINGS.md). Here it is enough that it is not 1.0."""
        rules = build_rules()
        for i, r in enumerate(rules):
            r.born_at = -i
        m = measure(list(corpus()), lambda c: decide_by_priority(rules, c), "inv")
        self.assertLess(m["accuracy_end_to_end"], 0.5)


class TestSubsumptionAlone(unittest.TestCase):
    """Level 1 of the rung 2 engine, with no declared edge at all."""

    @classmethod
    def setUpClass(cls):
        cls.m = medir(subsumption_only_engine().decide)

    def test_split_and_accuracy(self):
        self.assertEqual(self.m["out"]["ACTION"], SUB_ACTION)
        self.assertEqual(self.m["out"]["CONFLICT"], SUB_CONFLICT)
        self.assertEqual(self.m["out"]["IMPASSE"], 0)
        self.assertAlmostEqual(self.m["e2e"], SUB_E2E, places=4)

    def test_silent_error_zero(self):
        """The property that justifies level 1: when it does not know, it
        abstains. Abstaining is correct; inventing is what produces silent
        error."""
        self.assertEqual(self.m["silent"], 0.0)


class TestHybridCeiling(unittest.TestCase):
    """STEP 0 of rung 2. This one does pass: 100% with the policy loaded."""

    @classmethod
    def setUpClass(cls):
        cls.engine, cls.declared, cls.stats = build_hidden_engine(space())
        cls.m = medir(cls.engine.decide)

    def test_executes_the_policy_at_a_hundred_percent(self):
        self.assertEqual(self.m["e2e"], 1.0)
        self.assertEqual(self.m["silent"], 0.0)
        self.assertEqual(self.m["out"]["CONFLICT"], 0)
        self.assertEqual(self.m["out"]["IMPASSE"], 0)

    def test_declared_edges(self):
        self.assertEqual(self.stats["declared"], HYB_DECLARED_EDGES)
        self.assertEqual(len(self.declared), HYB_DECLARED_EDGES)

    def test_no_minimal_edge_is_rejected(self):
        """The edges are derived from the true layer order, so the validator
        should not knock any down. If it knocked one down, the assumption that
        subsumption is sound over this policy would be false."""
        self.assertEqual(self.stats["rejected"], [])

    def test_the_structure_orders_61_pairs_on_its_own(self):
        pairs = sum(len(s) for s in self.engine.sub_below.values())
        self.assertEqual(pairs, HYB_SUBSUMPTION_PAIRS)

    def test_the_total_order_is_not_declared(self):
        """Declaring all 406 pairs would be cheating: it would measure whether a
        total order works, whose answer is already known."""
        self.assertEqual(HYB_POSSIBLE_PAIRS, 406)
        self.assertLess(self.stats["declared"], HYB_POSSIBLE_PAIRS)

    def test_the_pair_split_adds_up(self):
        s = self.stats
        total = (s["declared"] + s["skipped_disjoint"]
                 + s["skipped_subsumed_by_structure"] + s["skipped_same_action"]
                 + len(s["rejected"]))
        self.assertEqual(total, HYB_POSSIBLE_PAIRS)


class TestRung2ReferenceTable(unittest.TestCase):
    """`ceiling_check2.REF` prints the rung 1 figures as a reference. They are
    written by hand; this test checks that they are still true."""

    def test_specificity_reference(self):
        e2e, silent, conflict = REF["especificidad (rung 1)"]
        self.assertAlmostEqual(e2e, SPEC_E2E, places=4)
        self.assertAlmostEqual(silent, SPEC_SILENT, places=4)
        self.assertEqual(conflict, SPEC_CONFLICT)

    def test_subsumption_reference(self):
        e2e, silent, conflict = REF["subsuncion sola (rung 1)"]
        self.assertAlmostEqual(e2e, SUB_E2E, places=4)
        self.assertEqual(silent, 0.0)
        self.assertEqual(conflict, SUB_CONFLICT)


if __name__ == "__main__":
    unittest.main()
