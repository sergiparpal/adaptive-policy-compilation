"""
SNAPSHOT of the default-rule control: the pair, on both surfaces, to the digit.

**Why a figure is pinned here at all.** The standing rule is that duplicating a
figure in a test gives it a second owner (`tests/test_floor_by_pool.py`, and
CLAUDE.md about the audit's optimizer). The exception is the one
`tests/test_ceilings.py` already is: a ceiling with the PERFECT policy loaded is
a deterministic function of two frozen things — the 29 rules and the corpus of
seed 17 — with no search, no sampling and no paid call in it. There is nothing
for a snapshot to drift against except a change in the frozen material, which is
exactly what a snapshot is for. Item 2 of `EXTERNAL_REVIEW.md` asks for this in
those words: *a test pins both, so neither drifts*.

What is pinned:

  corpus, as published            0.7475 / 0.5875 / 505 CONFLICT   (the gate)
  corpus, catch-all at its rank   0.8480 / 0.6880 / 304 CONFLICT
  space,  as published            0.4621 / 0.2725 / 72,298 CONFLICT
  space,  catch-all at its rank   0.5354 / 0.3458 / 62,445 CONFLICT

The first row is `results/FINDINGS.md` route 1 and is pinned in
`tests/test_ceilings.py` as well; it is repeated here because the control's
whole meaning is *beside that number*, and a control whose baseline has moved is
not a control. The other three are owned by
[`results/FINDINGS_DEFAULT_RULE.md`](../results/FINDINGS_DEFAULT_RULE.md).

If one of these fails, the expected number is NOT updated: you find out what
changed and date the erratum in the FINDINGS that owns it (hard rule 6).

Also pinned, and worth more than the figures: **what the control cannot do.** It
never changes a decision already taken and never resolves a conflict wrongly —
proved in the module's docstring and checked here over all 134,400 cases, because
a proof about code that quietly stops holding is the kind of thing this
repository has already been bitten by.

Nothing here calls `main()`, so nothing here writes to `results/`.
"""

from __future__ import annotations

import json
import unittest
from functools import cache
from pathlib import Path

from harness.ceiling_check import all_cases, build_rules, measure
from harness.default_rule_control import (CATCHALL, CONTROL, PUBLISHED,
                                          PUBLISHED_ROW, compare,
                                          decide_by_effective_specificity,
                                          describe_artifact,
                                          effective_specificity, is_vacuous)
from harness.domain import DOMAINS
from harness.dsl import Condition, RuleEngine

from .fixtures import SPACE_SIZE, corpus

RECORD = Path(__file__).resolve().parent.parent / "results" / "default_rule_control.json"

# --- corpus (n=2000, seed 17) ------------------------------------------------
PUB_ACTION, PUB_CONFLICT, PUB_COVERAGE, PUB_E2E = 1495, 505, 0.7475, 0.5875
CTL_ACTION, CTL_CONFLICT, CTL_COVERAGE, CTL_E2E = 1696, 304, 0.8480, 0.6880
SILENT_ABS = 320                    # the same under both arbitrations

# --- exhaustive space (134,400) ----------------------------------------------
PUB_SPACE_CONFLICT, PUB_SPACE_E2E, PUB_SPACE_COVERAGE = 72_298, 0.2725, 0.4621
CTL_SPACE_CONFLICT, CTL_SPACE_E2E, CTL_SPACE_COVERAGE = 62_445, 0.3458, 0.5354
SILENT_ABS_SPACE = 25_474           # the same under both arbitrations

# --- what the control moves, on the corpus -----------------------------------
WITH_CATCHALL, RESOLVED, STILL = 276, 201, 304


@cache
def rules():
    return tuple(build_rules())


@cache
def spec():
    return {r.rule_id: effective_specificity(r) for r in rules()}


@cache
def engine():
    e = RuleEngine()
    e.rules = list(rules())
    return e


@cache
def space_cases():
    return tuple(all_cases())


def published(cases):
    return measure(list(cases), engine().decide, PUBLISHED)


def controlled(cases):
    return measure(list(cases),
                   lambda c: decide_by_effective_specificity(
                       list(rules()), spec(), c), CONTROL)


class TestTheArtifact(unittest.TestCase):
    """One rule of the 29 pays a condition that constrains nothing, and it is
    the catch-all. If that ever stops being true, the control is measuring
    something else."""

    def test_the_catchall_is_the_only_rule_with_a_vacuous_condition(self):
        a = describe_artifact(list(rules()), spec())
        self.assertEqual(a["rules_with_a_vacuous_condition"], [CATCHALL])
        self.assertEqual(a["vacuous_conditions"][CATCHALL],
                         [{"attr": "severity", "op": "gte", "value": 1}])

    def test_the_engine_counts_one_and_the_policy_declares_none(self):
        a = describe_artifact(list(rules()), spec())
        self.assertEqual(a["specificity_in_the_dsl"], 1)
        self.assertEqual(a["effective_specificity"], 0)

    def test_vacuous_means_what_it_says_over_the_whole_space(self):
        """`is_vacuous` reads the declared domain; the catch-all's extension is
        checked against the 134,400 cases themselves, so the cheap definition is
        never taken on trust."""
        catchall = next(r for r in rules() if r.rule_id == CATCHALL)
        self.assertTrue(all(catchall.matches(c) for c in space_cases()))
        self.assertEqual(len(space_cases()), SPACE_SIZE)

    def test_a_real_condition_is_not_vacuous(self):
        self.assertFalse(is_vacuous(Condition(attr="severity", op="lte", value=2)))
        self.assertTrue(is_vacuous(
            Condition(attr="severity", op="in", value=list(DOMAINS["severity"]))))


class TestThePairOnTheCorpus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pub = published(corpus())
        cls.ctl = controlled(corpus())

    def test_the_published_row_is_the_gate_and_still_reproduces(self):
        """The control means nothing if 0.5875 has moved. The module blocks on
        exactly this comparison before printing a single row."""
        for k, expected in PUBLISHED_ROW.items():
            with self.subTest(k):
                got = self.pub[k]
                if isinstance(expected, float):
                    self.assertAlmostEqual(got, expected, places=4)
                else:
                    self.assertEqual(got, expected)
        self.assertEqual(self.pub["action"], PUB_ACTION)
        self.assertEqual(self.pub["conflict"], PUB_CONFLICT)
        self.assertAlmostEqual(self.pub["coverage"], PUB_COVERAGE, places=4)
        self.assertAlmostEqual(self.pub["accuracy_end_to_end"], PUB_E2E, places=4)

    def test_the_control_row(self):
        self.assertEqual(self.ctl["action"], CTL_ACTION)
        self.assertEqual(self.ctl["conflict"], CTL_CONFLICT)
        self.assertEqual(self.ctl["impasse"], 0)
        self.assertAlmostEqual(self.ctl["coverage"], CTL_COVERAGE, places=4)
        self.assertAlmostEqual(self.ctl["accuracy_end_to_end"], CTL_E2E, places=4)

    def test_the_silent_error_count_does_not_move(self):
        """Only the denominator does. The control converts abstentions into
        decisions; it never converts one into a wrong decision."""
        self.assertEqual(self.pub["silent_errors_abs"], SILENT_ABS)
        self.assertEqual(self.ctl["silent_errors_abs"], SILENT_ABS)
        self.assertGreater(self.pub["silent_error_rate"],
                           self.ctl["silent_error_rate"])

    def test_it_is_still_nowhere_near_the_ceiling_it_would_need(self):
        """The reading that must survive: the finding survives. 0.6880 does not
        approach the 1.0000 that first-match-wins gets over the same rules."""
        self.assertLess(self.ctl["accuracy_end_to_end"], 0.7)


class TestThePairOnTheSpace(unittest.TestCase):
    """Rung 1 published corpus figures without labelling them. The effect is on
    both surfaces and it is not the same size on the two."""

    @classmethod
    def setUpClass(cls):
        cls.pub = published(space_cases())
        cls.ctl = controlled(space_cases())

    def test_the_published_arbitration_over_the_space(self):
        self.assertEqual(self.pub["conflict"], PUB_SPACE_CONFLICT)
        self.assertAlmostEqual(self.pub["coverage"], PUB_SPACE_COVERAGE, places=4)
        self.assertAlmostEqual(self.pub["accuracy_end_to_end"], PUB_SPACE_E2E,
                               places=4)

    def test_the_control_over_the_space(self):
        self.assertEqual(self.ctl["conflict"], CTL_SPACE_CONFLICT)
        self.assertAlmostEqual(self.ctl["coverage"], CTL_SPACE_COVERAGE, places=4)
        self.assertAlmostEqual(self.ctl["accuracy_end_to_end"], CTL_SPACE_E2E,
                               places=4)

    def test_the_silent_error_count_does_not_move_here_either(self):
        self.assertEqual(self.pub["silent_errors_abs"], SILENT_ABS_SPACE)
        self.assertEqual(self.ctl["silent_errors_abs"], SILENT_ABS_SPACE)

    def test_the_two_surfaces_disagree_about_how_big_the_artifact_is(self):
        """39.8% of the corpus conflicts against 13.6% of the space's. Citing
        either without its surface is the defect `STATUS.md` opens with."""
        corpus_share = (PUB_CONFLICT - CTL_CONFLICT) / PUB_CONFLICT
        space_share = ((PUB_SPACE_CONFLICT - CTL_SPACE_CONFLICT)
                       / PUB_SPACE_CONFLICT)
        self.assertAlmostEqual(corpus_share, 0.398, places=3)
        self.assertAlmostEqual(space_share, 0.136, places=3)
        self.assertGreater(corpus_share, 2 * space_share)


class TestWhatTheControlCannotDo(unittest.TestCase):
    """The two invariants the module proves and blocks on. Checked over every
    case of both surfaces."""

    @classmethod
    def setUpClass(cls):
        cls.corpus = compare(corpus(), list(rules()), engine(), spec())
        cls.space = compare(space_cases(), list(rules()), engine(), spec())

    def test_no_decision_already_taken_changes(self):
        for name, mv in (("corpus", self.corpus), ("space", self.space)):
            with self.subTest(name):
                self.assertTrue(mv["gate_no_action_changes"])

    def test_no_conflict_is_resolved_wrongly(self):
        for name, mv in (("corpus", self.corpus), ("space", self.space)):
            with self.subTest(name):
                self.assertTrue(mv["gate_no_resolution_is_wrong"])
                self.assertEqual(mv["resolved_wrong"], 0)
                self.assertEqual(mv["resolved_correct"], mv["of_those_resolved"])

    def test_the_corpus_decomposition(self):
        mv = self.corpus
        self.assertEqual(
            mv["published_conflicts_with_the_catchall_as_finalist"],
            WITH_CATCHALL)
        self.assertEqual(mv["of_those_resolved"], RESOLVED)
        self.assertEqual(mv["still_conflict"], STILL)
        self.assertEqual(RESOLVED + STILL, PUB_CONFLICT)
        self.assertEqual(PUB_ACTION + RESOLVED, CTL_ACTION)

    def test_not_every_conflict_the_catchall_is_in_gets_resolved(self):
        """75 of the 276 keep disagreeing once it yields: the catch-all was in
        the conflict without being what caused it."""
        self.assertLess(RESOLVED, WITH_CATCHALL)

    def test_the_catchall_is_in_no_residual_conflict(self):
        for name, mv in (("corpus", self.corpus), ("space", self.space)):
            with self.subTest(name):
                self.assertEqual(mv["residual_conflict_sets_with_the_catchall"], 0)

    def test_the_residue_is_the_thesis_and_not_the_encoding(self):
        """Every remaining conflict is a set of finalists of EQUAL effective
        specificity and different actions: exactly what no criterion monotone in
        the number of conditions can order."""
        for r in self.corpus["top_residual_conflicts"]:
            with self.subTest(r["finalists"]):
                self.assertGreater(len(r["finalists"]), 1)
                self.assertGreater(len(set(r["actions"])), 1)
                self.assertNotIn(CATCHALL, r["finalists"])

    def test_the_critical_rare_classes_gain_nothing(self):
        """The reading CLAUDE.md Step 5 asks for: the aggregate hides them, and
        the control does nothing for either."""
        resolved = self.corpus["resolved_by_true_class"]
        self.assertNotIn("SECURITY_INCIDENT", resolved)
        self.assertNotIn("ONCALL_ESCALATION", resolved)
        per_class = self.corpus["per_class"]
        for cls in ("SECURITY_INCIDENT", "ONCALL_ESCALATION"):
            with self.subTest(cls):
                self.assertEqual(per_class[cls]["pub_CONFLICT"],
                                 per_class[cls]["ctl_CONFLICT"])


class TestTheRecordOnDisk(unittest.TestCase):
    """The published record must still say what the code measures, and must
    still declare what it is."""

    @classmethod
    def setUpClass(cls):
        cls.rec = json.loads(RECORD.read_text())

    def test_it_declares_itself_post_run(self):
        self.assertTrue(self.rec["provenance"].startswith("POST-RUN"))

    def test_it_carries_its_environment(self):
        self.assertIn("_env", self.rec)
        self.assertIn("code_digest", self.rec["_env"])

    def test_the_four_rows_are_the_ones_measured_here(self):
        rows = {(r["surface"], r["arbitration"]): r for r in self.rec["rows"]}
        self.assertEqual(len(rows), 4)
        for (_surface, arbitration), r in rows.items():
            with self.subTest(r["surface"], arbitration=arbitration):
                cases = corpus() if r["n"] == len(corpus()) else space_cases()
                m = published(cases) if arbitration == PUBLISHED else controlled(cases)
                self.assertEqual(r["conflict"], m["conflict"])
                self.assertEqual(r["action"], m["action"])
                self.assertAlmostEqual(r["accuracy_end_to_end"],
                                       m["accuracy_end_to_end"], places=6)

    def test_the_gate_it_records_passed(self):
        self.assertTrue(self.rec["gate_published_row"]["passes"])
        self.assertTrue(all(c["passes"] for c
                            in self.rec["gate_published_row"]["checks"].values()))


if __name__ == "__main__":
    unittest.main()
