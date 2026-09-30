"""
PLAN_REUSE.md — the package that executes it, checked before §0 is signed.

WHAT IS PINNED HERE, AND WHY. The constants of §10 and the five band lines of
§0, so that moving one after a figure exists is visible in a diff — the reason
`tests/test_sensitivity.py` pins `PLAN_SENSITIVITY.md`'s. The gate: that it
reads every signature line and not the first, and that every writer of the
package — the free ones too — exits on an unsigned plan before it builds,
measures or writes anything, and `reuse/run.py` before it builds the client.
The arithmetic of §5.2 and §5.3 on records small enough to check by hand. And
`U-g2` and `U-g3` on the real inputs, which print nothing: a check that passes is
silent, and a figure of Stage A is never computed for display here.

**No test here writes under `results*/` and none spends.** The one path that
could — `reuse/run.py` past its gate — is exercised with the client replaced by
something that fails the test if it is ever constructed.
"""

from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from reuse import analysis, frontier, gates, plan
from reuse import readout as stage_a
from reuse import run as stage_b
from reuse import score as stage_c

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_protocol_of_section_10(self):
        self.assertEqual(plan.N, 2000)
        self.assertEqual(plan.SEED, 17)
        self.assertEqual(plan.PROMPT, "v1")
        self.assertEqual(plan.MODEL, "deepseek/deepseek-v4-flash")
        self.assertEqual(plan.REPS, 3)
        self.assertEqual(plan.SMOKE_N, 20)

    def test_the_five_lines_of_section_0(self):
        self.assertEqual(plan.U_A_MIN_REUSE, 0.30)
        self.assertEqual(plan.U_B_REFUTED_AT_OR_BELOW, 0.0)
        self.assertEqual(plan.U_C_MIN_SHARE, 0.60)
        self.assertEqual(plan.U_D_MIN_ONCALL, 1)
        self.assertEqual(plan.U_E_MAX_CONFLICTS, 20)
        self.assertEqual(plan.U_A_CAVEAT_CONFLICT_SHARE, 0.25)

    def test_the_eight_records_are_the_eight_on_disk(self):
        self.assertEqual(len(plan.EIGHT), 8)
        self.assertEqual({(p, s) for p, s, _ in plan.EIGHT},
                         {(p, s) for p in ("v1", "v2") for s in plan.EIGHT_SEEDS})
        for _, _, path in plan.EIGHT:
            self.assertTrue(path.is_file(), path)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_REUSE.md"))
        self.assertTrue(plan.PLAN.is_file())
        self.assertGreaterEqual(plan.gate_signature()["found"], 1)


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_no_signature_line_no_pass(self):
        self.assertFalse(self.gate("# a plan\n")["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ________________________ (date: ______________)**\n"
        )["passes"])

    def test_a_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-01)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-01)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


class TestF(unittest.TestCase):
    """§5.2's frontier, on points small enough to check by hand."""

    POINTS = [(1.0, 0.9), (1.0, 0.8), (0.8, 0.2), (0.4, 0.0)]

    def test_a_shared_reuse_keeps_the_lower_error(self):
        self.assertEqual(analysis.F(self.POINTS, 1.0), 0.8)

    def test_linear_between_the_bracketing_points(self):
        self.assertAlmostEqual(analysis.F(self.POINTS, 0.9), 0.5)
        self.assertAlmostEqual(analysis.F(self.POINTS, 0.6), 0.1)

    def test_a_point_is_its_own_value(self):
        self.assertEqual(analysis.F(self.POINTS, 0.8), 0.2)

    def test_flat_beyond_the_ends(self):
        self.assertEqual(analysis.F(self.POINTS, 0.1), 0.0)
        self.assertEqual(analysis.F([(0.5, 0.3), (0.2, 0.1)], 0.9), 0.3)

    def test_an_empty_frontier_has_no_value(self):
        with self.assertRaises(ValueError):
            analysis.F([], 0.5)

    def test_a_keep_k_that_decided_nothing_is_dropped(self):
        pts = analysis.frontier_points({
            7: {"reuse_rate": 0.1, "silent_error": 0.0},
            8: {"reuse_rate": 0.0, "silent_error": None}})
        self.assertEqual(pts, [(0.1, 0.0)])

    def test_the_published_frontier_has_all_eight_points(self):
        """At n=2000 every keep_k decides something, so none is dropped."""
        pts = frontier.published_points()
        self.assertEqual(len(pts), 8)
        self.assertEqual(max(r for r, _ in pts), 1.0)


def tiny_record() -> dict:
    """Six cases, two rules: R1 born right at case 0, R2 born wrong at case 2.
    R1 then decides cases 1 (right) and 4 (wrong); R2 decides case 3 (wrong);
    case 5 conflicts."""
    rec = [
        dict(idx=0, outcome="IMPASSE", predicted="A", truth="A", truth_rule="H1",
             correct=True, winner_id=None, escalated=True,
             proposal_action_correct=True, rejected_reason=None),
        dict(idx=1, outcome="ACTION", predicted="A", truth="A", truth_rule="H1",
             correct=True, winner_id="R1", escalated=False,
             proposal_action_correct=None, rejected_reason=None),
        dict(idx=2, outcome="IMPASSE", predicted="B", truth="C", truth_rule="H2",
             correct=False, winner_id=None, escalated=True,
             proposal_action_correct=False, rejected_reason=None),
        dict(idx=3, outcome="ACTION", predicted="B", truth="C", truth_rule="H2",
             correct=False, winner_id="R2", escalated=False,
             proposal_action_correct=None, rejected_reason=None),
        dict(idx=4, outcome="ACTION", predicted="A", truth="ONCALL_ESCALATION",
             truth_rule="H4", correct=False, winner_id="R1", escalated=False,
             proposal_action_correct=None, rejected_reason=None),
        dict(idx=5, outcome="CONFLICT", predicted=None, truth="ONCALL_ESCALATION",
             truth_rule="H4", correct=None, winner_id=None, escalated=True,
             proposal_action_correct=None,
             rejected_reason="proposal_failed: sin objeto JSON"),
    ]
    for r in rec:
        r.update(n_matched=0, shown_ids=[], shown_kind="vecindario",
                 edges_proposed=0, edges_accepted=0, edge_reasons=[])
    rules = [
        dict(rule_id="R1", action="A", born_at=0, fire_count=2, correct_count=1,
             beats=[], loses_to=[]),
        dict(rule_id="R2", action="B", born_at=2, fire_count=1, correct_count=0,
             beats=[], loses_to=[]),
    ]
    record = {"n": 6, "seed": 17, "records": rec, "rules": rules}
    record["metrics"] = analysis.recompute_metrics(record)
    return record


class TestTheArithmeticOnATinyRecord(unittest.TestCase):

    def setUp(self):
        self.rec = tiny_record()
        self.born, self.problems = analysis.births(self.rec)

    def test_a_consistent_record_reproduces_itself(self):
        self.assertEqual(self.problems, [])
        self.assertEqual(analysis.metric_mismatches(self.rec), [])
        self.assertEqual(analysis.fire_mismatches(self.rec), [])

    def test_the_metrics_it_publishes(self):
        m = self.rec["metrics"]
        self.assertEqual((m["reuse_rate"], m["silent_errors_abs"], m["conflicts"],
                          m["failed_proposals"], m["escalations"]),
                         (1.0, 2, 1, 1, 3))

    def test_the_split_by_birth(self):
        s = analysis.split_silent(self.rec, self.born)
        self.assertEqual((s["silent_errors"], s["by_rules_born_wrong"],
                          s["by_rules_born_right"]), (2, 1, 1))
        self.assertEqual(s["share_born_wrong"], 0.5)

    def test_the_right_born_subset_and_its_gap(self):
        rb = analysis.right_born(self.rec, self.born)
        self.assertEqual((rb["rules"], rb["reused"], rb["decided"], rb["correct"]),
                         (1, 1, 2, 1))
        self.assertEqual((rb["reuse_rate"], rb["silent_error"]), (1.0, 0.5))
        self.assertAlmostEqual(analysis.gap(rb, [(1.0, 0.25), (0.5, 0.0)]), 0.25)

    def test_the_ledgers(self):
        self.assertEqual(analysis.escalations_by_truth(self.rec),
                         {"A": 1, "C": 1, "ONCALL_ESCALATION": 1})
        self.assertEqual(analysis.class_ledger(self.rec, "ONCALL_ESCALATION"),
                         {"cases": 2, "escalated": 1, "decided_by_a_rule": 1,
                          "decided_rightly": 0})
        self.assertAlmostEqual(analysis.conflict_share(self.rec), 1 / 3)

    def test_a_tampered_fire_count_is_caught(self):
        rec = copy.deepcopy(self.rec)
        rec["rules"][0]["fire_count"] = 3
        self.assertTrue(analysis.fire_mismatches(rec))

    def test_a_rule_born_from_another_action_is_caught(self):
        rec = copy.deepcopy(self.rec)
        rec["rules"][1]["action"] = "C"
        self.assertTrue(any("proposal of" in p for p in analysis.births(rec)[1]))

    def test_two_rules_on_one_birth_are_caught(self):
        rec = copy.deepcopy(self.rec)
        rec["rules"][1]["born_at"] = 0
        self.assertTrue(any("shared" in p for p in analysis.births(rec)[1]))

    def test_a_birth_that_did_not_escalate_is_caught(self):
        rec = copy.deepcopy(self.rec)
        rec["rules"][1]["born_at"] = 1
        self.assertTrue(any("did not escalate" in p
                            for p in analysis.births(rec)[1]))


class TestTheVerdictsAtTheirEdges(unittest.TestCase):
    """Each band's edge is its own refutation line (§0)."""

    def test_u_a(self):
        self.assertEqual(stage_c.verdict_u_a(0.30), "holds")
        self.assertEqual(stage_c.verdict_u_a(0.2999), "refuted")

    def test_u_b(self):
        self.assertEqual(stage_c.verdict_u_b(1e-9), "holds")
        self.assertEqual(stage_c.verdict_u_b(0.0), "refuted")
        self.assertEqual(stage_c.verdict_u_b(None), "unadjudicable")

    def test_u_c(self):
        self.assertEqual(stage_c.verdict_u_c(0.60), "holds")
        self.assertEqual(stage_c.verdict_u_c(0.5999), "refuted")

    def test_u_d(self):
        self.assertEqual(stage_c.verdict_u_d(1), "holds")
        self.assertEqual(stage_c.verdict_u_d(0), "refuted")

    def test_u_e(self):
        self.assertEqual(stage_c.verdict_u_e(20), "holds")
        self.assertEqual(stage_c.verdict_u_e(21), "refuted")

    def test_the_median_skips_an_undefined_run(self):
        self.assertEqual(analysis.median_of([None, 0.1, 0.3]), 0.2)
        self.assertIsNone(analysis.median_of([None, None]))


class TestTheRealInputs(unittest.TestCase):
    """`U-g2` and `U-g3` on what Stage A will read. Silent when they pass."""

    @classmethod
    def setUpClass(cls):
        cls.runs_n = frontier.keep_k_runs(plan.N, plan.SEED)
        cls.runs_100 = {s: frontier.keep_k_runs(plan.N_EIGHT, s)
                        for s in plan.EIGHT_SEEDS}

    def test_u_g2_the_eight_records_reproduce_themselves(self):
        g = gates.gate_ug2(self.runs_100)
        self.assertEqual([p for r in g["rows"] for p in r["problems"]], [])
        self.assertTrue(g["passes"])

    def test_u_g3_the_frontier_does_not_depend_on_the_engine(self):
        g = frontier.gate_ug3(self.runs_n, self.runs_100)
        self.assertTrue(g["reproduces_published"], g["k_not_reproduced"])
        self.assertEqual(g["most_rules_matching_one_case"], 1)

    def test_the_n100_corpus_is_the_head_of_the_n2000_one(self):
        """Not assumed anywhere, and worth knowing: seed 17's first hundred
        cases are the same draws at both horizons."""
        head = frontier.truth_sequence(self.runs_n[1])[:plan.N_EIGHT]
        self.assertEqual(head, frontier.truth_sequence(self.runs_100[17][1]))


def fake_checks(passes: bool = True) -> gates.Checks:
    ok = {"passes": passes}
    return gates.Checks(ug1={**ok, "surfaces": {}, "suite": {"ran": False}},
                        ug2={**ok, "rows": []}, ug3=ok, ug4=dict(UNSIGNED),
                        runs_n={}, runs_100={})


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):
    """The signature comes first, in every writer: before the checks, the
    destination, the corpus or the client."""

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(stage_b, "OpenRouterProposer2",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        self.refuses(stage_b.main, ["--rep", "1"])
        self.refuses(stage_b.main, ["--smoke"])

    def test_the_free_writers_refuse_too(self):
        self.refuses(stage_a.main, [])
        self.refuses(stage_c.main, [])
        self.refuses(frontier.main, [])

    def test_the_dry_run_builds_no_client_and_writes_nothing(self):
        with mock.patch.object(gates, "run_all", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(stage_b, "OpenRouterProposer2",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            self.assertEqual(stage_b.main(["--dry-run"]), 0)
        client.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_all", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            self.assertEqual(stage_b.main(["--dry-run"]), 1)


SIGNED = {**UNSIGNED, "passes": True, "unsigned": 0}
FIRST_SMOKE = Path("results_reuse/run_n20_smoke_401.json")


def smoke_record(**over) -> dict:
    rec = {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
           "seed": plan.SEED, "n": plan.SMOKE_N,
           "metrics": {"escalations": 20, "failed_proposals": 0, "n_rules": 12}}
    rec.update(over)
    return rec


class TestTheFullRunsWaitForASmokeRunThatWorked(unittest.TestCase):
    """Step 2b of `reuse/run.py`, added on 2026-09-30 after the first smoke run
    met a key OpenRouter rejected on all 20 calls and still wrote a record."""

    def check(self, rec: dict | None) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "smoke.json"
            if rec is not None:
                p.write_text(json.dumps(rec))
            return stage_b.smoke_check(p)

    def test_no_smoke_record_no_run(self):
        self.assertFalse(self.check(None)[0])

    def test_a_smoke_run_whose_every_proposal_failed(self):
        self.assertFalse(self.check(smoke_record(metrics={
            "escalations": 20, "failed_proposals": 20, "n_rules": 0}))[0])

    def test_parsed_proposals_and_no_rule(self):
        self.assertFalse(self.check(smoke_record(metrics={
            "escalations": 20, "failed_proposals": 3, "n_rules": 0}))[0])

    def test_a_smoke_run_under_another_protocol(self):
        self.assertFalse(self.check(smoke_record(model="another/model"))[0])
        self.assertFalse(self.check(smoke_record(prompt_version="v2"))[0])

    def test_a_smoke_run_that_worked(self):
        self.assertTrue(self.check(smoke_record())[0])

    def test_the_first_smoke_run_would_not_have_opened_the_runs(self):
        """The record that motivated the check fails it."""
        ok, why = stage_b.smoke_check(FIRST_SMOKE)
        self.assertFalse(ok)
        self.assertIn("none of the 20 proposals", why)

    def test_rep_refuses_before_the_checks_or_the_client(self):
        with tempfile.TemporaryDirectory() as d:
            missing = Path(d) / "no_smoke.json"
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(plan, "SMOKE_PATH", missing), \
                 mock.patch.object(gates, "run_all",
                                   side_effect=AssertionError("checks ran")) as checks, \
                 mock.patch.object(stage_b, "OpenRouterProposer2",
                                   side_effect=AssertionError("client built")) as client, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    stage_b.main(["--rep", "1"])
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_rep_goes_on_to_the_checks_after_a_smoke_run_that_worked(self):
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "smoke.json"
            good.write_text(json.dumps(smoke_record()))
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(plan, "SMOKE_PATH", good), \
                 mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}), \
                 mock.patch.object(stage_b, "fetch_key_info", return_value=API_KEY), \
                 mock.patch.object(gates, "run_all",
                                   side_effect=RuntimeError("reached the checks")), \
                 mock.patch.object(stage_b, "OpenRouterProposer2",
                                   side_effect=AssertionError("client built")) as client, \
                 mock.patch("builtins.print"):
                with self.assertRaisesRegex(RuntimeError, "reached the checks"):
                    stage_b.main(["--rep", "1"])
        client.assert_not_called()

    def test_the_second_smoke_run_would_not_have_opened_the_runs_either(self):
        ok, why = stage_b.smoke_check(SECOND_SMOKE)
        self.assertFalse(ok)
        self.assertIn("none of the 20 proposals", why)


SECOND_SMOKE = Path("results_reuse/run_n20_smoke_401_management_key.json")
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
MANAGEMENT_KEY = (200, {"data": {"is_management_key": True, "is_provisioning_key": True}})


class TestTheKeyIsCheckedBeforeAnythingIsCalled(unittest.TestCase):
    """Step 2c of `reuse/run.py`, added on 2026-09-30 after the second smoke run
    met a management key: OpenRouter's key endpoint accepts one — it answered
    200 — and every completion call refuses it. **No test here reaches the
    network**: the endpoint is always replaced."""

    def check(self, answer=None, *, key: str | None = "test", raises=None):
        fetch = mock.Mock(return_value=answer, side_effect=raises)
        with mock.patch.dict(os.environ):
            os.environ.pop("OPENROUTER_API_KEY", None)
            if key is not None:
                os.environ["OPENROUTER_API_KEY"] = key
            return stage_b.key_check(fetch), fetch

    def test_an_api_key(self):
        (ok, _), _ = self.check(API_KEY)
        self.assertTrue(ok)

    def test_a_management_key_is_refused(self):
        (ok, why), _ = self.check(MANAGEMENT_KEY)
        self.assertFalse(ok)
        self.assertIn("management key", why)

    def test_a_key_the_endpoint_rejects(self):
        (ok, why), _ = self.check((401, {"error": {"code": 401}}))
        self.assertFalse(ok)
        self.assertIn("HTTP 401", why)

    def test_no_key_in_the_environment_asks_nothing(self):
        (ok, why), fetch = self.check(API_KEY, key=None)
        self.assertFalse(ok)
        self.assertIn("hard rule 7", why)
        fetch.assert_not_called()

    def test_an_unreachable_endpoint_refuses_rather_than_crashes(self):
        (ok, why), _ = self.check(raises=OSError("no route"))
        self.assertFalse(ok)
        self.assertIn("could not be reached", why)

    def test_nothing_it_says_carries_the_key(self):
        secret = "sk-or-v1-" + "0" * 64
        for answer in (API_KEY, MANAGEMENT_KEY, (401, {})):
            (_, why), _ = self.check(answer, key=secret)
            self.assertNotIn(secret, why)

    def refused(self, argv: list[str], smoke: dict | None) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            if smoke is not None:
                path.write_text(json.dumps(smoke))
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(plan, "SMOKE_PATH", path), \
                 mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}), \
                 mock.patch.object(stage_b, "fetch_key_info",
                                   return_value=MANAGEMENT_KEY), \
                 mock.patch.object(gates, "run_all",
                                   side_effect=AssertionError("checks ran")) as checks, \
                 mock.patch.object(stage_b, "OpenRouterProposer2",
                                   side_effect=AssertionError("client built")) as client, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write, \
                 mock.patch("builtins.print"):
                with self.assertRaises(SystemExit):
                    stage_b.main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_the_smoke_run_refuses_a_management_key_before_the_checks(self):
        self.refused(["--smoke"], None)

    def test_a_full_run_refuses_one_even_after_a_smoke_run_that_worked(self):
        self.refused(["--rep", "1"], smoke_record())

    def test_the_dry_run_needs_no_key(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(gates, "run_all", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(stage_b, "fetch_key_info",
                               side_effect=AssertionError("asked")) as fetch, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            self.assertEqual(stage_b.main(["--dry-run"]), 0)
        fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
