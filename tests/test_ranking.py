"""
PLAN_RANKING.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the client is rung 2's pairwise judge's,
    imported rather than retyped, with `PLAN_REUSE.md`'s reasoning setting
    (rule A). That three lines are read from the records that own them, and
    round to the figures §0 states.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `ranking/ask.py` exits before it builds the client.
  * `M-g2` on the real presentations, and its teeth: an injected ticket, rule,
    queue or omission is caught, and a changed order moves a digest.
  * What makes an answer valid, at every edge §0 names.
  * `M-g1` and `M-g3` on the real records, where they are cheap: one cell of
    the enumeration, every published reproduction of `M-g3`, and the
    comparison's teeth against a tampered record. And that the checks compute
    nothing §0 declares unseen, watched at the call, where `PLAN_BOUND.md`'s
    package walked its syntax tree.
  * The request: through the SDK double, every call carries the judge's
    settings and reasoning off, and keeps its attempts and their texts.
  * Stage B end to end through the double, including resuming and stopping on
    an outage; Stage C's arithmetic on values small enough to check by hand.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double or something that fails the test if it is ever built. **No figure §0
declares unseen is computed, not even silently**: the only rankings scored on a
cell are Stage C's, whose scores are published, and Stage C's rate over the
model's answers is never computed — wherever the scorer would compute it, the
answers are replaced by invented ones.
"""

from __future__ import annotations

import functools
import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import ACTIONS
from reuse import plan as reuse_plan
from rung2 import pair_judgement
from rung2.proposers2 import ProposalError
from rung3 import queue_hierarchy_floor as qhf

from ranking import ask, gates, plan, question, sample, score
from ranking import instrument as I
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
MANAGEMENT_KEY = (200, {"data": {"is_management_key": True}})
SC = list(qhf.STAGE_C_HIERARCHY)


def good(order=SC, why="una frase") -> str:
    return json.dumps({"ranking": list(order), "why": why})


@functools.lru_cache(maxsize=1)
def real_instrument() -> I.Instrument:
    return I.build()


def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes, "problems": [], "rows": [], "rows_compared": 0,
         "seconds": 0, "tiebreak_gate": {"n_cells": 0}, "suite": {"ran": False}}
    return gates.Checks(mg1=g, mg2={"passes": True, "presentations": 12, "teeth": True,
                                    "problems": [], "digests": {}},
                        mg3={"passes": True, "problems": []}, mg4=UNSIGNED)


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_the_judges_imported(self):
        self.assertEqual((plan.MODEL, plan.TEMPERATURE, plan.MAX_TOKENS, plan.MAX_RETRIES),
                         (pair_judgement.MODEL, pair_judgement.TEMPERATURE,
                          pair_judgement.MAX_TOKENS, pair_judgement.MAX_RETRIES))
        src = Path("ranking/plan.py").read_text()
        self.assertNotIn('"deepseek/', src, "the model name is retyped")

    def test_reasoning_is_off_as_plan_reuse_amended(self):
        self.assertIs(plan.REASONING, reuse_plan.REASONING)
        self.assertEqual(plan.REASONING, {"effort": "none"})

    def test_the_constants_of_section_10(self):
        self.assertEqual((plan.PRESENTATIONS, plan.PASSES, plan.SMOKE_ASKS), (12, 2, 2))
        self.assertEqual(plan.PRESENTATION_SEED, 59)
        self.assertEqual((plan.MIN_SIGNATURES, plan.MIN_VALID_SHARE, plan.MIN_VALID_ASKS,
                          plan.MAX_CONSECUTIVE_FAILURES), (1, 0.90, 4, 5))
        self.assertEqual(plan.SIGNED_CELL, ("hibrido", "corpus_test_split0"))
        self.assertEqual(plan.LINE_PLACES, 6)
        self.assertEqual(plan.QUEUES, tuple(ACTIONS))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertNotIn(plan.PRESENTATION_SEED, {17, 18, 19, 20, 25, 41, 43, 47, 53})
        self.assertLess(plan.PRESENTATION_SEED, 1000)

    def test_the_two_lines_that_are_edges(self):
        self.assertEqual((plan.M_A_MAX_SLOT_GAP, plan.M_D_MIN_GAP), (0.05, 0.0))

    def test_the_three_read_lines_are_section_0s(self):
        """Read from the records, and round to the figures §0 states."""
        lines = plan.signed_lines()
        self.assertEqual(round(lines["M-b"]["line"], 4), 0.4632)
        self.assertEqual(round(lines["M-c"]["line"], 4), 0.4824)
        self.assertEqual(round(lines["M-e"]["line"], 4), 0.5460)
        self.assertEqual(lines["M-e"]["units"], 65)
        self.assertIs(plan.P_D_MARGIN, qhf.P_D_MARGIN)

    def test_a_read_line_moves_with_its_record(self):
        """Teeth: the lines are read, not typed."""
        rec = json.loads(plan.HIERARCHY_RECORD.read_text())
        for r in rec["rows"]:
            if (r.get("tiebreak"), r["pool"], r["surface"]) == ("born_at", *plan.SIGNED_CELL):
                r["stage_c"] = 0.5
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "h.json"
            p.write_text(json.dumps(rec))
            self.assertEqual(plan.signed_lines(hierarchy=p)["M-c"]["line"], 0.5)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_RANKING.md"))

    def test_the_sessions_and_where_they_land(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "session"))
        self.assertEqual(plan.ask_path("session"), Path("results_ranking/ask_session.json"))
        with self.assertRaises(ValueError):
            plan.ask_path("another")


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ______________________ (date: ______________)**\n"
        )["passes"])

    def test_the_plan_as_drafted_does_not_pass(self):
        g = plan.gate_signature()
        if g["passes"]:
            self.skipTest("PLAN_RANKING.md is signed")
        self.assertEqual((g["found"], g["unsigned"]), (1, 1))

    def test_one_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-18)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-18)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


# ---------------------------------------------------------------------------
# The question
# ---------------------------------------------------------------------------

class TestTheQuestionReadsNothingButTheNames(unittest.TestCase):

    def test_m_g2_passes(self):
        g = question.gate_mg2()
        self.assertTrue(g["passes"], g["problems"])
        self.assertTrue(g["teeth"])

    def test_the_presentations(self):
        pres = question.presentations()
        self.assertEqual(len(pres), 12)
        self.assertEqual(pres[0].order, tuple(ACTIONS))
        self.assertEqual(len({p.order for p in pres}), 12)
        self.assertEqual([p.pid for p in pres], [f"p{k:02d}" for k in range(1, 13)])
        for p in pres:
            self.assertEqual(sorted(p.order), sorted(ACTIONS))

    def test_they_are_the_seeds_alone(self):
        here = question.presentations()
        self.assertEqual(here, question.presentations())
        with mock.patch.object(plan, "PRESENTATION_SEED", 60):
            other = question.presentations()
        self.assertEqual(other[0].order, here[0].order)
        self.assertNotEqual([p.order for p in other[1:]], [p.order for p in here[1:]])

    def test_one_stream_per_pass(self):
        orders = question.pass_orders(question.presentations())
        self.assertEqual(len(orders), 2)
        self.assertNotEqual(orders[0], orders[1])
        for o in orders:
            self.assertEqual(sorted(o), [f"p{k:02d}" for k in range(1, 13)])
        self.assertEqual(question.smoke_order(question.presentations()), ["p01", "p02"])

    def test_each_name_once_in_the_whole_request(self):
        for p in question.presentations():
            whole = question.SYSTEM_PROMPT + question.user_message(p.order)
            for q in ACTIONS:
                self.assertEqual(whole.count(q), 1, (p.pid, q))

    def test_the_system_prompt_names_no_queue(self):
        for q in ACTIONS:
            self.assertNotIn(q, question.SYSTEM_PROMPT)

    def test_an_injected_ticket_is_caught(self):
        with mock.patch.object(question, "SYSTEM_PROMPT",
                               question.SYSTEM_PROMPT + "\nTICKET: severity 1, channel phone"):
            leaks = question.leaks(tuple(ACTIONS), set())
        self.assertTrue(any("severity" in x for x in leaks), leaks)
        self.assertTrue(any("phone" in x for x in leaks), leaks)

    def test_an_injected_rule_or_queue_is_caught(self):
        with mock.patch.object(question, "SYSTEM_PROMPT",
                               question.SYSTEM_PROMPT + "\nR0042 manda a T1_GENERAL"):
            leaks = question.leaks(tuple(ACTIONS), {"R0042"})
        self.assertTrue(any("rule ids" in x for x in leaks), leaks)
        self.assertTrue(any("T1_GENERAL appears 2" in x for x in leaks), leaks)
        with mock.patch.object(question, "SYSTEM_PROMPT",
                               question.SYSTEM_PROMPT + "\nNEW_QUEUE"):
            self.assertTrue(any("no queue" in x
                                for x in question.leaks(tuple(ACTIONS), set())))

    def test_an_omitted_name_is_caught(self):
        self.assertTrue(any("appears 0" in x
                            for x in question.leaks(tuple(ACTIONS)[:-1], set())))

    def test_a_changed_order_moves_the_digest(self):
        o = list(ACTIONS)
        o[3], o[4] = o[4], o[3]
        self.assertNotEqual(question.digest(o), question.digest(ACTIONS))

    def test_the_user_message_takes_the_order_alone(self):
        msg = question.user_message(ACTIONS)
        self.assertEqual(msg.splitlines(), ["LAS COLAS:"] + [f"  {q}" for q in ACTIONS])


class TestWhatMakesAnAnswerValid(unittest.TestCase):

    def test_a_permutation_of_the_eight(self):
        self.assertEqual(question.ranking_of({"ranking": SC}), SC)

    def test_whitespace_is_stripped_and_nothing_else_is_forgiven(self):
        self.assertEqual(question.ranking_of({"ranking": [f" {q} " for q in SC]}), SC)
        self.assertIsNone(question.ranking_of({"ranking": [q.lower() for q in SC]}))

    def test_every_edge_of_section_0(self):
        for bad in (None, [], "x", {"ranking": "T1_GENERAL"},
                    {"ranking": SC[:-1]},                     # an omission
                    {"ranking": SC[:-1] + [SC[0]]},           # a repetition
                    {"ranking": SC + ["NEW_QUEUE"]},          # nine entries
                    {"ranking": SC[:-1] + ["NEW_QUEUE"]},     # an invented name
                    {"ranking": SC[:-1] + [[SC[-1]]]},        # a tie, as a list
                    {"order": SC}):
            with self.subTest(bad=bad):
                self.assertIsNone(question.ranking_of(bad))


# ---------------------------------------------------------------------------
# The instrument, on values small enough to check by hand
# ---------------------------------------------------------------------------

class TestTheInstrumentsArithmetic(unittest.TestCase):

    def test_predicts(self):
        answers = [I.Answer(("T1_GENERAL", "T2_TECHNICAL"), "T2_TECHNICAL"),
                   I.Answer(("T2_TECHNICAL", "T1_GENERAL"), "T1_GENERAL"),
                   I.Answer(("SECURITY_INCIDENT", "T1_GENERAL"), "SECURITY_INCIDENT")]
        self.assertEqual(I.predicts(SC, answers), (2, 3))

    def test_agreement(self):
        self.assertEqual(I.agreement(SC, SC), 1.0)
        self.assertEqual(I.agreement(SC, list(reversed(SC))), 0.0)
        o = list(SC)
        o[0], o[1] = o[1], o[0]
        self.assertEqual(I.agreement(SC, o), 27 / 28)
        self.assertEqual(len(I.QUEUE_PAIRS), 28)

    def test_the_slot_gap(self):
        o = list(SC)
        o[0], o[1] = o[1], o[0]
        g = I.slot_gap([("p01", 1, SC), ("p01", 2, SC), ("p02", 1, o), ("p02", 2, o)])
        self.assertEqual(g["W"], 1.0)
        self.assertAlmostEqual(g["A"], 27 / 28)
        self.assertAlmostEqual(g["gap"], 1 / 28)
        self.assertEqual(g["presentations_with_both_passes"], 2)
        none = I.slot_gap([("p01", 1, SC)])
        self.assertIsNone(none["gap"])

    def test_borda_and_its_ties(self):
        self.assertEqual(I.borda([SC, SC]), SC)
        tie = I.borda([SC, list(reversed(SC))])
        self.assertEqual(tie, list(ACTIONS))      # every queue tied: the domain's order

    def test_the_mid_rank_percentile(self):
        dist = [0.1, 0.2, 0.2, 0.3]
        self.assertEqual(I.percentile(0.2, dist), 0.5)
        self.assertEqual(I.percentile(0.05, dist), 0.0)
        self.assertEqual(I.percentile(0.4, dist), 1.0)

    def test_names_for_is_stage_c_names_on_any_row(self):
        name = I.names_for(SC)
        rng = random.Random(1)
        for _ in range(50):
            qw, ql = rng.sample(list(ACTIONS), 2)
            row = {"winner": "R1", "loser": "R2", "queues": [qw, ql]}
            self.assertEqual(name(row), I.blind_rows.stage_c_names(row))


class TestThePublishedFiguresComeBack(unittest.TestCase):
    """`M-g3` in full, and the cheap half of `M-g1`, on the real records."""

    def test_m_g3_passes(self):
        g = gates.gate_mg3()
        self.assertTrue(g["passes"], g["problems"])
        self.assertEqual((g["learned_declared_answers"], g["hidden_two_way_answers"]),
                         (1479, 166))
        self.assertEqual(g["revealed_predicts_its_own_answers"], [1194, 1479])
        self.assertEqual(g["rows_where_the_predicts_differ"], 0)

    def test_stage_cs_score_and_the_floor_on_the_signed_cell(self):
        inst = real_instrument()
        lines = plan.signed_lines()
        self.assertEqual(round(I.score(inst, SC, *plan.SIGNED_CELL), 6), lines["M-c"]["line"])
        self.assertEqual(round(I.born_at_score(inst, *plan.SIGNED_CELL), 6),
                         lines["M-b"]["floor"])

    def test_one_cell_of_m_g1_against_the_record(self):
        inst = real_instrument()
        rows = gates.measured_rows(inst, cells=(plan.SIGNED_CELL,))
        rec = json.loads(plan.HIERARCHY_RECORD.read_text())
        pub = {(r["tiebreak"], r["pool"], r["surface"]): r for r in rec["rows"]}
        self.assertEqual(len(rows), 2)
        for r in rows:
            p = pub[(r["tiebreak"], r["pool"], r["surface"])]
            for f in gates.FLOAT_FIELDS:
                self.assertTrue(gates.close(r[f], p[f]), (f, r[f], p[f]))
            self.assertEqual(r["best_hierarchy"], p["best_hierarchy"])

    def test_the_comparison_has_teeth(self):
        rec = json.loads(plan.HIERARCHY_RECORD.read_text())
        floors, _ = qhf.read_floor(plan.FLOOR_RECORD)
        own = [dict(r, born_at=r["born_at_floor"]) for r in rec["rows"]
               if r["surface"] != I.FIVE_SPLITS]
        self.assertEqual(gates.compare_with_record(own, rec["rows"], floors), [])
        tampered = [dict(r) for r in own]
        k = next(i for i, r in enumerate(tampered) if r["surface"] == "space")
        tampered[k]["mean"] += 0.001
        problems = gates.compare_with_record(tampered, rec["rows"], floors)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("space", problems[0])
        split = next(i for i, r in enumerate(own) if r["surface"] == I.SPLITS[0])
        tampered = [dict(r) for r in own]
        tampered[split]["mean"] += 0.001
        # the row and its five-split aggregate both disagree
        self.assertEqual(len(gates.compare_with_record(tampered, rec["rows"], floors)), 2)
        self.assertTrue(gates.compare_with_record(own[:-1], rec["rows"], floors))

    def test_floats_agree_to_a_unit_in_the_last_place(self):
        self.assertTrue(gates.close(0.482412, 0.482413))
        self.assertFalse(gates.close(0.482412, 0.482416))


class TestTheDryRunComputesNothingSection0DeclaresUnseen(unittest.TestCase):
    """What `PLAN_BOUND.md`'s package checked by walking its syntax tree, checked
    here by watching the calls: the checks score no ranking but Stage C's, and
    compute no rate over the model's answers but the revealed ranking's, whose
    1,194 of 1,479 is published."""

    def spies(self):
        calls = {"predicts": [], "score": 0, "scores": 0, "distribution": 0}
        real = I.predicts

        def predicts(order, answers):
            calls["predicts"].append(list(order))
            return real(order, answers)

        def counting(name):
            def f(*a, **k):
                calls[name] += 1
                raise AssertionError(f"the checks called {name}")
            return f
        patches = [mock.patch.object(I, "predicts", side_effect=predicts)] + \
            [mock.patch.object(I, n, side_effect=counting(n))
             for n in ("score", "scores", "distribution")]
        return calls, patches

    def test_m_g3_reads_one_rate_and_it_is_the_published_one(self):
        calls, patches = self.spies()
        for p in patches:
            p.start()
        try:
            self.assertTrue(gates.gate_mg3()["passes"])
        finally:
            for p in patches:
                p.stop()
        revealed = json.loads(plan.EDGE_DROPPING.read_text())["revealed_ranking"]["order"]
        self.assertEqual(calls["predicts"], [revealed])
        self.assertEqual((calls["score"], calls["scores"], calls["distribution"]), (0, 0, 0))

    def test_m_g1_scores_stage_c_and_the_floor_and_nothing_else(self):
        calls, patches = self.spies()
        for p in patches:
            p.start()
        try:
            gates.measured_rows(real_instrument(), cells=(plan.SIGNED_CELL,))
        finally:
            for p in patches:
                p.stop()
        self.assertEqual(calls["predicts"], [])
        self.assertEqual((calls["score"], calls["scores"], calls["distribution"]), (0, 0, 0))


# ---------------------------------------------------------------------------
# Nothing is built or written unsigned
# ---------------------------------------------------------------------------

class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        for s in plan.SESSIONS:
            with self.subTest(s):
                self.refuses(ask.main, ["--session", s])

    def test_the_free_writers_refuse_too(self):
        self.refuses(sample.main, [])
        self.refuses(score.main, [])

    def test_the_dry_run_builds_no_client_needs_no_key_and_writes_nothing(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            self.assertEqual(ask.main(["--dry-run"]), 0)
            self.assertEqual(sample.main(["--dry-run"]), 0)
            self.assertEqual(score.main(["--dry-run"]), 0)
        fetch.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            self.assertEqual(ask.main(["--dry-run"]), 1)
            self.assertEqual(sample.main(["--dry-run"]), 1)
            self.assertEqual(score.main(["--dry-run"]), 1)


# ---------------------------------------------------------------------------
# The smoke run and the key come first
# ---------------------------------------------------------------------------

def smoke_record(valid: bool = True, **over) -> dict:
    rec = {**ask.protocol(), "rows": [{"valid": valid}, {"valid": False}]}
    rec.update(over)
    return rec


class TestTheSessionWaitsForASmokeRunThatWorked(unittest.TestCase):

    def check(self, rec: dict | None):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ask_smoke.json"
            if rec is not None:
                p.write_text(json.dumps(rec))
            return ask.smoke_check(p)

    def test_no_smoke_record_no_session(self):
        self.assertFalse(self.check(None)[0])

    def test_a_smoke_run_under_another_protocol(self):
        self.assertFalse(self.check(smoke_record(max_tokens=1200))[0])
        self.assertFalse(self.check(smoke_record(reasoning=None))[0])

    def test_a_smoke_run_without_a_valid_ranking(self):
        self.assertFalse(self.check(smoke_record(valid=False))[0])

    def test_a_smoke_run_that_worked(self):
        self.assertTrue(self.check(smoke_record())[0])

    def test_the_session_refuses_before_the_key_the_checks_or_the_client(self):
        signed = {**UNSIGNED, "passes": True, "unsigned": 0}
        with mock.patch.object(plan, "gate_signature", return_value=signed), \
             mock.patch.object(ask, "smoke_check", return_value=(False, "none")), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")), \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("client built")):
            with self.assertRaises(SystemExit):
                ask.main(["--session", "session"])
        fetch.assert_not_called()

    def test_the_smoke_run_refuses_a_management_key(self):
        signed = {**UNSIGNED, "passes": True, "unsigned": 0}
        with mock.patch.object(plan, "gate_signature", return_value=signed), \
             mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-test"}), \
             mock.patch("reuse.run.fetch_key_info", return_value=MANAGEMENT_KEY), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")), \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("client built")):
            with self.assertRaises(SystemExit):
                ask.main(["--session", "smoke"])


# ---------------------------------------------------------------------------
# Stage B through the SDK double
# ---------------------------------------------------------------------------

class TestASessionThroughTheSDKDouble(unittest.TestCase):

    def run_session(self, script, session="smoke", partial=None, header=None):
        client = OpenRouterShapedClient(script)
        with fake_sdk(openai=client), mock.patch("builtins.print"):
            asker = ask.Asker()
            with tempfile.TemporaryDirectory() as d:
                p = partial or Path(d) / "x.partial.jsonl"
                rows, resumed = ask.ask(session, asker, p, header or {"h": 1})
        return rows, resumed, client

    def test_every_request_carries_the_judges_settings_and_reasoning_off(self):
        rows, _, client = self.run_session(FixedResponses(good()))
        self.assertEqual(len(client.peticiones), 2)
        pres = {p.pid: p for p in question.presentations()}
        for req, row in zip(client.peticiones, rows):
            self.assertEqual(req["model"], plan.MODEL)
            self.assertEqual(req["temperature"], plan.TEMPERATURE)
            self.assertEqual(req["max_tokens"], plan.MAX_TOKENS)
            self.assertEqual(req["extra_body"], {"reasoning": {"effort": "none"}})
            self.assertEqual(req["response_format"], {"type": "json_object"})
            self.assertEqual(req["messages"], question.messages(pres[row["pid"]].order))
        self.assertEqual([r["pid"] for r in rows], ["p01", "p02"])

    def test_each_row_keeps_its_attempts_and_their_texts(self):
        rows, _, _ = self.run_session(FixedResponses("no es json", good()))
        first = rows[0]
        self.assertTrue(first["valid"])
        self.assertEqual(len(first["call_attempts"]), 2)
        self.assertEqual(first["call_attempts"][0]["provider"],
                         OpenRouterShapedClient.PROVIDER)
        self.assertEqual(first["raw_answers"], ["no es json", good()])
        self.assertEqual(first["ranking"], SC)

    def test_the_retry_drops_the_response_format_as_the_judge_does(self):
        _, _, client = self.run_session(FixedResponses("no es json", good()))
        self.assertIn("response_format", client.peticiones[0])
        self.assertNotIn("response_format", client.peticiones[1])
        self.assertEqual(client.peticiones[1]["messages"][-1]["content"],
                         question.RETRY_MSG)

    def test_an_invalid_ranking_is_an_answer_not_a_failure(self):
        rows, _, _ = self.run_session(FixedResponses(good(SC[:-1])))
        self.assertTrue(all(not r["valid"] and r["failure"] is None for r in rows))
        self.assertEqual(len(rows), 2)

    def test_a_resumed_session_asks_nothing_twice(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.partial.jsonl"
            self.run_session(FixedResponses(good()), partial=p)
            rows, resumed, client = self.run_session(FixedResponses(good()), partial=p)
            self.assertEqual(len(client.peticiones), 0)
            self.assertEqual(len(rows), 2)
            self.assertTrue(resumed)

    def test_an_outage_stops_the_session_and_records_none_of_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.partial.jsonl"
            with self.assertRaises(ask.Outage):
                self.run_session(FixedResponses("no"), session="session", partial=p)
            kept = p.read_text().splitlines()
            self.assertEqual(len(kept), 1)            # the header alone

    def test_an_isolated_failure_is_an_answer_and_is_recorded(self):
        texts = ["no", "no", "no", good()]           # three attempts fail, then one parses
        rows, _, _ = self.run_session(FixedResponses(*texts))
        self.assertIsNotNone(rows[0]["failure"])
        self.assertEqual(len(rows[0]["raw_answers"]), 3)
        self.assertTrue(rows[1]["valid"])

    def test_the_session_is_the_passes_in_their_orders(self):
        sched = ask.schedule("session")
        self.assertEqual(len(sched), 24)
        orders = question.pass_orders(question.presentations())
        self.assertEqual([pid for p, pid in sched if p == 1], orders[0])
        self.assertEqual([pid for p, pid in sched if p == 2], orders[1])


# ---------------------------------------------------------------------------
# Stage C's arithmetic
# ---------------------------------------------------------------------------

class TestTheArithmeticOfSection0(unittest.TestCase):

    def test_below_four_valid_asks_unadjudicable(self):
        v = score.adjudicate([0.9, 0.9, 0.9], 0.5, strict=True, record_precision=False)
        self.assertTrue(v["unadjudicable"])
        self.assertIsNone(v["holds"])

    def test_the_median_and_the_edges(self):
        v = score.adjudicate([0.1, 0.5, 0.5, 0.9], 0.5, strict=False, record_precision=False)
        self.assertTrue(v["holds"])               # median 0.5, >= 0.5
        v = score.adjudicate([0.1, 0.5, 0.5, 0.9], 0.5, strict=True, record_precision=False)
        self.assertFalse(v["holds"])              # median 0.5, not > 0.5

    def test_thin_is_an_ask_on_the_other_side(self):
        v = score.adjudicate([0.6, 0.6, 0.7, 0.4], 0.5, strict=True, record_precision=False)
        self.assertTrue(v["holds"] and v["thin"])
        v = score.adjudicate([0.6, 0.6, 0.7, 0.8], 0.5, strict=True, record_precision=False)
        self.assertTrue(v["holds"] and not v["thin"])

    def test_record_precision_keeps_an_equal_reading_equal(self):
        exact = 480 / 995                          # Stage C's cases on the signed cell
        v = score.adjudicate([exact] * 4, 0.482412, strict=False, record_precision=True)
        self.assertTrue(v["holds"])
        v = score.adjudicate([0.5460261] * 4, 0.546026, strict=True, record_precision=True)
        self.assertFalse(v["holds"])

    def test_m_a(self):
        o = list(SC)
        o[0], o[1] = o[1], o[0]
        rows = [{"pid": "p01", "pass": 1, "valid": True, "ranking": SC},
                {"pid": "p01", "pass": 2, "valid": True, "ranking": SC},
                {"pid": "p02", "pass": 1, "valid": True, "ranking": o},
                {"pid": "p02", "pass": 2, "valid": True, "ranking": o}]
        v = score.m_a(rows)
        self.assertTrue(v["holds"])               # gap 1/28 <= 0.05
        rows.append({"pid": "p03", "pass": 1, "valid": False, "ranking": None})
        self.assertFalse(score.m_a(rows)["validity_holds"])   # 4 of 5

    def test_m_d_values(self):
        answers = [I.Answer(("T1_GENERAL", "T2_TECHNICAL"), "T1_GENERAL"),
                   I.Answer(("T1_GENERAL", "T2_TECHNICAL"), "T1_GENERAL")]
        o = list(SC)
        i, j = o.index("T1_GENERAL"), o.index("T2_TECHNICAL")
        o[i], o[j] = o[j], o[i]
        vals, base = score.m_d_values([SC, o], answers)
        self.assertEqual(base, {"stage_c_hits": 0, "n": 2})
        self.assertEqual(vals, [0.0, 1.0])


class TestStageCOverASessionTheDoubleCouldHaveProduced(unittest.TestCase):
    """Every ask is Stage C's ranking, whose scores and readings are published,
    and the pairwise answers are invented: nothing unseen is computed."""

    def test_it_scores_every_valid_ask_and_reads_every_row(self):
        rows = [{"pid": f"p{k:02d}", "pass": p, "valid": True, "ranking": SC,
                 "payload": {"ranking": SC, "why": "x"}, "failure": None,
                 "call_attempts": [{"provider": "x", "finish_reason": "stop"}]}
                for k in range(1, 4) for p in (1, 2)]
        rows.append({"pid": "p04", "pass": 1, "valid": False, "ranking": None,
                     "payload": {"ranking": SC[:-1]}, "failure": None,
                     "raw_answers": ["..."], "call_attempts": []})
        toy = [I.Answer(("T1_GENERAL", "T2_TECHNICAL"), "T2_TECHNICAL")] * 3
        fake_sample = {"lines": sample.lines(),
                       "revealed": {"learned": {"order": SC, "by_queue_pair": {}},
                                    "hidden": {"order": SC, "by_queue_pair": {}}},
                       "declarations": {"corpus_out": {"reading": 0.5}},
                       "stage_c": {"k_b_pairs": {"corpus_out": {"reading": 0.6}}}}
        with mock.patch.object(I, "learned_answers", return_value=toy), \
             mock.patch.object(I, "hidden_answers", return_value=toy):
            out = score.score_session(real_instrument(), fake_sample,
                                      {"rows": rows}, percentiles=False)
        v = out["verdicts"]
        self.assertEqual(v["M-a"]["valid"], 6)
        self.assertFalse(v["M-a"]["validity_holds"])          # 6 of 7
        self.assertTrue(v["M-c"]["holds"])                    # Stage C reaches itself
        self.assertEqual(v["M-c"]["median"], plan.signed_lines()["M-c"]["line"])
        self.assertTrue(v["M-b"]["holds"])
        self.assertEqual(v["M-d"]["median"], 0.0)             # the same ranking
        self.assertTrue(v["M-d"]["holds"])
        self.assertTrue(v["M-e"]["holds"])                    # 0.7219 > 0.5460
        self.assertEqual(len(out["M-f"]["invalid"]), 1)
        self.assertEqual(out["M-f"]["borda"]["order"], SC)


if __name__ == "__main__":
    unittest.main()
