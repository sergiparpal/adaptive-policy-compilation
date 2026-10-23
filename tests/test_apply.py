"""
PLAN_APPLY.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the client is `PLAN_MANUAL.md`'s loop
    proposer, imported rather than retyped (rule A). That the lines are
    fractions, and every comparison with them exact.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `apply/ask.py` exits before it builds a client.
  * The population rebuilt from the twelve loop records: §0's counts, every
    screen the row's, the ticket names, what each ask serves, and nothing in
    the design that carries a label.
  * The prompts: the screen arm the escalation's own, the ticket arm v1's empty
    base under the level's prompt and case 0's prompt at every level, level 0
    `PLAN_SCREEN.md`'s, no builder taking a row, and the digests' teeth.
  * The requests, through the SDK double: at each level and in each arm, what
    `manual.run.build_proposer(level)` sends, which is the loop's request.
  * Stage B end to end through the double: no label in a row, the attempts
    kept, a session resumed, an outage stopping without recording, the turns.
  * Stage C by hand: every term of §0, the clustered error, *thin* both ways,
    the exact comparisons at each line, every reason a row has no value, the
    classes of a changed answer, and the whole stage over synthetic passes.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double, or something that fails the test if it is ever built. Every record
a test writes lands in a temporary directory that `plan.OUT` is pointed at.
**No figure of the plan is computed**: the only answers ever scored are the
double's or synthetic ones.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from harness.domain import ACTIONS, generate_corpus
from manual import plan as manual_plan
from manual.run import build_proposer
from rung2.proposers2 import OpenRouterProposer2, ProposalError, user_msg

from apply import ask, gates, plan, population, prompts, sample, score
from fidelity import prompts as fprompts
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
F = Fraction


def answer_json(action: str = "T2_TECHNICAL") -> str:
    return json.dumps({"action": action,
                       "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                       "beats": [], "loses_to": [], "note": "una nota"})


def fake_checks(passes: bool = True, design=None) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(xg1=g, xg2=g, xg3=g, xg4=SIGNED,
                        design=design or population.build())


class TempOut:
    """Points `plan.OUT` at a temporary directory for the block."""

    def __enter__(self) -> Path:
        self._d = tempfile.TemporaryDirectory()
        self._p = mock.patch.object(plan, "OUT", Path(self._d.name))
        self._p.start()
        return Path(self._d.name)

    def __exit__(self, *exc) -> None:
        self._p.stop()
        self._d.cleanup()


def small(design: population.Design, k: int = 12) -> population.Design:
    """The design with each session cut to its first `k` asks of pass 1's order,
    so that a test asks a few prompts of both arms and not 1,454."""
    head = design.sessions["pass1"][:k]
    return dataclasses.replace(design, sessions={"smoke": design.sessions["smoke"],
                                                 "pass1": head,
                                                 "pass2": list(reversed(head))})


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_manuals(self):
        self.assertEqual(plan.MODEL, manual_plan.MODEL)
        self.assertIs(plan.REASONING, manual_plan.REASONING)
        self.assertEqual(plan.REASONING, {"effort": "none"})
        self.assertEqual((plan.PROMPT, plan.TEMPERATURE), ("v1", 0))
        self.assertEqual((ask.TEMPERATURE, ask.MAX_TOKENS), (0, 1200))

    def test_the_inputs_are_plan_manuals(self):
        self.assertEqual((plan.LEVELS, plan.REPS, plan.N, plan.SEED),
                         ((0, 1, 2, 3), 3, 2000, 17))
        self.assertEqual(plan.loop_record(2, 3), Path("results_manual/loop_L2_r3.json"))
        self.assertEqual(plan.manual_sample(), Path("results_manual/sample.json"))
        self.assertEqual(plan.manual_score(), Path("results_manual/score.json"))
        self.assertEqual(plan.SCREEN_TICKET_ONLY,
                         Path("results_screen/ask_ticket_only.json"))

    def test_the_populations_are_section_0s(self):
        self.assertEqual(plan.DECISIONS, {0: 116, 1: 100, 2: 242, 3: 320})
        self.assertEqual(plan.CONFLICT_DECISIONS, {0: 11, 1: 37, 2: 75, 3: 70})
        self.assertEqual(plan.TICKET_PROMPTS, {0: 275, 1: 81, 2: 149, 3: 171})
        self.assertEqual((plan.EMPTY_SCREENS, plan.SHARED_WITH_SCREEN), (12, 183))
        self.assertEqual(sum(plan.DECISIONS.values()), 778)
        self.assertEqual(sum(plan.TICKET_PROMPTS.values()), 676)

    def test_the_sessions_and_the_limits(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "pass1", "pass2"))
        self.assertEqual((plan.PASSES, plan.SMOKE_PER_ARM_AND_LEVEL), (2, 1))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MAX_CONSECUTIVE_FAILURES,
                          plan.MIN_PULL_POPULATION), (1, 5, 100))
        self.assertEqual(plan.MAX_INVALID_SHARE, F(1, 20))
        self.assertIsInstance(plan.MAX_INVALID_SHARE, Fraction)

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 67)
        self.assertNotIn(plan.ORDER_SEED, {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_lines_are_section_0s_as_fractions(self):
        lines = {"X_A_MAX_GAP": F(1, 20), "X_B_LINE": F(0), "X_C_LINE": F(1, 2),
                 "X_D_LINE": F(1, 10), "X_E_LINE": F(0), "X_F_LINE": F(1, 10)}
        for name, value in lines.items():
            with self.subTest(name):
                self.assertIsInstance(getattr(plan, name), Fraction)
                self.assertEqual(getattr(plan, name), value)

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_APPLY.md").read_text()
        for needle in ("`ORDER_SEED = 67`", "`DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}`",
                       "`TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}`",
                       "`X_C_LINE = Fraction(1, 2)`", "`X_F_LINE = Fraction(1, 10)`"):
            with self.subTest(needle):
                self.assertIn(needle, text)

    def test_the_gate_reads_this_plan_and_the_records_land_in_results_apply(self):
        self.assertEqual(plan.PLAN, Path("PLAN_APPLY.md"))
        self.assertEqual(plan.ask_path("pass1"), Path("results_apply/ask_pass1.json"))
        self.assertEqual(plan.partial_path("smoke"),
                         Path("results_apply/ask_smoke.partial.jsonl"))
        self.assertEqual((plan.sample_path(), plan.score_path()),
                         (Path("results_apply/sample.json"), Path("results_apply/score.json")))
        self.assertEqual([plan.pass_of(s) for s in plan.SESSIONS], [0, 1, 2])
        for bad in (plan.ask_path, plan.partial_path, plan.pass_of, plan.order_rng):
            with self.subTest(bad.__name__), self.assertRaises(ValueError):
                bad("pass3")


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_blank_signed_and_a_blank_second_line(self):
        cases = (("**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-24)**\n", True),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-24)**\n"
                  "**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            for text, ok in cases:
                p.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(p)["passes"], ok)

    def test_the_plan_carries_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned here: a
        test that pinned the draft's blank line would fail at the signature,
        as one did on 2026-10-23. The verdicts on a blank and a filled line are
        the fakes' above."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_APPLY.md")["found"],
                         plan.MIN_SIGNATURES)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        proposer.assert_not_called()
        fetch.assert_not_called()
        write.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        for s in plan.SESSIONS:
            with self.subTest(s):
                self.refuses(ask.main, ["--session", s])

    def test_the_free_writers_refuse_too(self):
        self.refuses(sample.main, [])
        self.refuses(score.main, [])

    def test_the_dry_runs_build_no_client_need_no_key_and_write_nothing(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(ask, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        fetch.assert_not_called()
        proposer.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 1)

    def test_a_pass_refuses_before_the_key_without_its_smoke_run(self):
        with TempOut(), \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer:
            for s in ("pass1", "pass2"):
                with self.subTest(s), self.assertRaises(SystemExit):
                    ask.main(["--session", s])
        fetch.assert_not_called()
        checks.assert_not_called()
        proposer.assert_not_called()


# ---------------------------------------------------------------------------
# The population
# ---------------------------------------------------------------------------

class TestThePopulationIsSection0s(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.design = population.build()

    def test_the_counts(self):
        d = self.design
        self.assertEqual(len(d.escalations), 790)
        self.assertEqual({lv: len(d.decisions_at(lv)) for lv in plan.LEVELS}, plan.DECISIONS)
        self.assertEqual({lv: sum(1 for e in d.decisions_at(lv)
                                  if e.prompt.screen == prompts.CONFLICT)
                          for lv in plan.LEVELS}, plan.CONFLICT_DECISIONS)
        self.assertEqual(len(d.asks), 778 + 676)

    def test_the_empty_screens_are_case_0_of_every_run(self):
        self.assertEqual(len(self.design.empty), plan.EMPTY_SCREENS)
        for i in self.design.empty:
            e = self.design.escalations[i]
            with self.subTest(i):
                self.assertEqual(e.idx, 0)
                self.assertEqual(e.prompt.base_text, prompts.EMPTY_BASE)

    def test_every_screen_is_the_rows(self):
        self.assertTrue(gates.screens(self.design)["passes"])

    def test_a_ticket_is_named_by_the_first_case_with_its_attributes(self):
        corpus = population.corpus()
        for e in list(self.design.escalations.values())[:50]:
            first = next(i for i, c in enumerate(corpus) if c.key() == e.prompt.case.key())
            self.assertEqual(e.ticket, first)

    def test_each_decision_is_served_once_by_each_arm(self):
        served = {"s": {}, "t": {}, "u": {}}
        for aid, sv in self.design.serves.items():
            for role, ids in sv.items():
                for i in ids:
                    served[role].setdefault(i, []).append(aid)
        for role in ("s", "t", "u"):
            with self.subTest(role):
                self.assertEqual(set(served[role]), set(self.design.decisions))
                self.assertTrue(all(len(v) == 1 for v in served[role].values()))
        for i, e in self.design.decisions.items():
            self.assertEqual(served["t"][i], [population.ticket_ask_id(e.level, e.ticket)])
            self.assertEqual(served["u"][i], [population.ticket_ask_id(0, e.ticket)])

    def test_nothing_in_the_design_carries_a_label(self):
        fields = {f.name for cls in (population.Escalation, prompts.Ask)
                  for f in dataclasses.fields(cls)}
        self.assertFalse(fields & {"truth", "y", "predicted", "correct", "label"})
        text = json.dumps(self.design.summary())
        for word in ('"truth"', '"predicted"', '"correct"'):
            self.assertNotIn(word, text)


# ---------------------------------------------------------------------------
# The prompts
# ---------------------------------------------------------------------------

class TestThePromptsAreTheLoops(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.design = population.build()

    def test_the_four_gates_pass_without_the_suite(self):
        with mock.patch("builtins.print"):
            checks = gates.run_checks(suite=False)
            gates.report(checks)
        self.assertTrue(checks.blocking_pass)
        for g in (checks.xg1, checks.xg2, checks.xg3):
            self.assertTrue(g["passes"])
        # X-g4 reads the plan as it stands, signed or not; it never blocks a
        # check, so only what it found is pinned.
        self.assertEqual(checks.xg4["found"], plan.MIN_SIGNATURES)

    def test_the_screen_arm_is_the_escalations_prompt_under_the_levels_system(self):
        for i, e in list(self.design.decisions.items())[::37]:
            a = self.design.asks[population.screen_ask_id(i)]
            with self.subTest(i):
                self.assertEqual(a.system, population.record(e.level, e.run)["system_prompt"])
                self.assertEqual(a.user, user_msg(e.prompt.case, e.prompt.base_text))
                self.assertTrue(a.shown_ids)

    def test_level_0s_digest_is_fidelitys(self):
        for a in self.design.asks.values():
            if a.level == 0:
                p = (fprompts.ticket_only(a.case) if a.arm == prompts.TICKET
                     else self.design.escalations[a.id[2:]].prompt)
                self.assertEqual(a.digest, p.digest)

    def test_the_ticket_arm_is_the_empty_base_and_plan_screens_at_level_0(self):
        got = gates.tickets(self.design)
        self.assertTrue(got["passes"])
        self.assertEqual((got["shared_with_plan_screen"], got["same_digest"]), (183, 183))

    def test_no_builder_takes_a_row(self):
        self.assertTrue(gates.builders()["passes"])

    def test_the_digests_have_teeth_and_no_digest_stands_for_two_texts(self):
        got = gates.digests(self.design)
        self.assertTrue(got["passes"])
        self.assertEqual(got["collisions"], [])
        self.assertEqual(got["asks_sharing_a_text_with_another"], 13)

    def test_the_plurality_breaks_a_tie_toward_the_first_shown(self):
        case = generate_corpus(1, seed=17)[0]
        a = prompts.Ask(id="x", arm=prompts.SCREEN, level=0, case=case, screen=prompts.COVERAGE,
                        shown_ids=("R1", "R2", "R3", "R4"),
                        shown_actions=("T1_GENERAL", "T2_TECHNICAL", "T2_TECHNICAL", "T1_GENERAL"),
                        base_text="x")
        self.assertEqual(prompts.plurality(a), "T1_GENERAL")
        self.assertEqual(prompts.first_shown(a), "T1_GENERAL")

    def test_a_screen_arm_ask_must_be_a_birth_prompt(self):
        case = generate_corpus(1, seed=17)[0]
        with self.assertRaises(ValueError):
            prompts.screen_ask("x", 0, fprompts.ticket_only(case))

    def test_the_schedule(self):
        got = gates.schedule(self.design)
        self.assertTrue(got["passes"])
        self.assertEqual(len(got["smoke"]), 8)


# ---------------------------------------------------------------------------
# The requests, through the SDK double
# ---------------------------------------------------------------------------

class TestTheRequestIsTheLoops(unittest.TestCase):

    def test_each_level_and_arm_sends_the_loops_request(self):
        d = population.build()
        for lv in plan.LEVELS:
            for arm in prompts.ARMS:
                a = next(x for x in d.asks.values() if x.level == lv and x.arm == arm)
                client = OpenRouterShapedClient(FixedResponses(answer_json()))
                with fake_sdk(openai=client):
                    p = build_proposer(lv)
                    action, _ = p.propose(a.case, a.base_text)
                    attempts = p.calls.take()
                with self.subTest(level=lv, arm=arm):
                    self.assertEqual(action, "T2_TECHNICAL")
                    (req,) = client.peticiones
                    self.assertEqual(req["model"], plan.MODEL)
                    self.assertEqual(req["temperature"], ask.TEMPERATURE)
                    self.assertEqual(req["max_tokens"], ask.MAX_TOKENS)
                    self.assertEqual(req["response_format"], {"type": "json_object"})
                    self.assertEqual(req["extra_body"], {"reasoning": plan.REASONING})
                    self.assertEqual(req["messages"],
                                     [{"role": "system", "content": a.system},
                                      {"role": "user", "content": a.user}])
                    self.assertEqual(attempts[0]["provider"], OpenRouterShapedClient.PROVIDER)

    def test_it_differs_from_a_plain_v1_proposer_only_in_the_system_message(self):
        d = population.build()
        a = next(x for x in d.asks.values() if x.level == 3 and x.arm == prompts.SCREEN)
        sent = []
        for build in (lambda: build_proposer(3),
                      lambda: OpenRouterProposer2(model=plan.MODEL, prompt_version="v1",
                                                  reasoning=plan.REASONING)):
            client = OpenRouterShapedClient(FixedResponses(answer_json()))
            with fake_sdk(openai=client):
                build().propose(a.case, a.base_text)
            sent.append(client.peticiones[0])
        mine, plain = sent
        self.assertNotEqual(mine["messages"][0], plain["messages"][0])
        self.assertEqual(mine["messages"][1:], plain["messages"][1:])
        self.assertEqual({k: v for k, v in mine.items() if k != "messages"},
                         {k: v for k, v in plain.items() if k != "messages"})


# ---------------------------------------------------------------------------
# Stage B, through the double
# ---------------------------------------------------------------------------

class Failing:
    """A proposer that fails, as a dropped connection or a revoked key would."""
    max_retries = 2
    system_prompt = ""

    def propose(self, case, base_text):
        raise ProposalError("sin objeto JSON: ''")


class TestStageB(unittest.TestCase):

    def setUp(self):
        self.design = small(population.build())

    def run_session(self, out: Path, session: str, build=None, **kw):
        header = {"protocol": ask.protocol(), "session": session, "sample_sha256": "x"}
        return ask.ask(session, self.design, ask.Proposers(build), out / f"{session}.jsonl",
                       header, **kw)

    def test_a_pass_asks_every_prompt_and_keeps_the_attempts_and_no_label(self):
        client = OpenRouterShapedClient(FixedResponses(answer_json()))
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=client), \
             mock.patch("builtins.print"):
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(resumed, [])
        self.assertEqual({r["arm"] for r in rows}, set(prompts.ARMS))
        for r in rows:
            self.assertTrue(r["valid"])
            self.assertEqual(r["pass"], 1)
            self.assertEqual(r["digest"], self.design.asks[r["id"]].digest)
            self.assertEqual(r["call_attempts"][0]["provider"],
                             OpenRouterShapedClient.PROVIDER)
            self.assertFalse({"truth", "labels", "predicted", "y"} & set(r))

    def test_an_interrupted_session_resumes_where_it_stopped(self):
        client = OpenRouterShapedClient(FixedResponses(answer_json()))
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=client), \
             mock.patch("builtins.print"):
            n = {"calls": 0}

            def interrupting(level):
                p = build_proposer(level)
                inner = p.propose

                def propose(case, base_text):
                    n["calls"] += 1
                    if n["calls"] == 5:
                        raise KeyboardInterrupt
                    return inner(case, base_text)
                p.propose = propose
                return p

            with self.assertRaises(KeyboardInterrupt):
                self.run_session(Path(d), "pass1", build=interrupting)
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(len(resumed), 1)

    def test_an_outage_stops_the_session_without_recording_it(self):
        with tempfile.TemporaryDirectory() as d, mock.patch("builtins.print"):
            with self.assertRaises(ask.Outage):
                self.run_session(Path(d), "pass1", build=lambda lv: Failing())
            lines = (Path(d) / "pass1.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)          # the header, and no failure

    def test_an_isolated_failure_is_an_answer_and_is_recorded(self):
        client = OpenRouterShapedClient(FixedResponses("no es json", "tampoco", "nada",
                                                       answer_json()))
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=client), \
             mock.patch("builtins.print"):
            rows, _ = self.run_session(Path(d), "pass1")
        self.assertIsNotNone(rows[0]["failure"])
        self.assertFalse(rows[0]["valid"])
        self.assertEqual(rows[0]["attempts"], 3)
        self.assertTrue(all(r["valid"] for r in rows[1:]))

    def test_the_smoke_run_end_to_end_and_the_turns(self):
        client = OpenRouterShapedClient(FixedResponses(answer_json()))
        design = self.design
        with TempOut(), fake_sdk(openai=client), \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info", return_value=API_KEY), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks(design=design)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(ask, "sample_matches", return_value=(True, "same")), \
             mock.patch.object(ask, "sample_sha256", return_value="x"), \
             mock.patch("builtins.print"):
            self.assertEqual(ask.main(["--session", "smoke"]), 0)
            rec = json.loads(plan.ask_path("smoke").read_text())
            self.assertFalse(plan.partial_path("smoke").exists())
            self.assertTrue(ask.smoke_check()[0])
            self.assertEqual(sorted(rec["system_prompts_sha256"]), ["0", "1", "2", "3"])
            self.assertEqual(len(rec["rows"]), 8)
            self.assertIn("_env", rec)
            ok, why = ask.previous_check("pass2")
            self.assertFalse(ok)
            self.assertIn("pass 1", why)
            self.assertTrue(ask.previous_check("pass1")[0])
            with self.assertRaises(SystemExit):
                ask.main(["--session", "pass2"])
            with self.assertRaises(SystemExit):           # a paid record is never overwritten
                ask.main(["--session", "smoke"])

    def test_sample_matches_reads_the_sessions_and_the_digests(self):
        design = self.design
        with TempOut():
            summary = json.loads(json.dumps(design.summary()))
            plan.sample_path().write_text(json.dumps({"design": summary}))
            self.assertTrue(ask.sample_matches(design)[0])
            summary["asks"][design.sessions["pass1"][0]]["digest"] = "0" * 16
            plan.sample_path().write_text(json.dumps({"design": summary}))
            self.assertFalse(ask.sample_matches(design)[0])


class TestNoLabelReachesWhatIsSent(unittest.TestCase):
    """The modules that build and send read no `truth` and no loop answer: no
    subscript or attribute of either name, and no `labels` imported."""

    def test_the_proposer_path_reads_no_label(self):
        for rel in ("apply/prompts.py", "apply/ask.py"):
            tree = ast.parse((REPO / rel).read_text())
            keys = {n.slice.value for n in ast.walk(tree)
                    if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant)
                    and isinstance(n.slice.value, str)}
            attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
            names = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                     for a in n.names}
            with self.subTest(rel):
                self.assertFalse(keys & {"truth", "predicted", "correct"})
                self.assertFalse(attrs & {"truth", "predicted", "y", "loop"})
                self.assertNotIn("labels", names)
                self.assertNotIn("score", names)


# ---------------------------------------------------------------------------
# Stage C, by hand
# ---------------------------------------------------------------------------

def unit(level=3, run=1, ticket=1, y="T1_GENERAL", loop="T1_GENERAL", p="T2_TECHNICAL",
         s=("T1_GENERAL", "T1_GENERAL"), t=("T1_GENERAL", "T1_GENERAL"),
         u=("T1_GENERAL", "T1_GENERAL"), kind=prompts.COVERAGE, first=None, shown=None,
         uid=None) -> score.Unit:
    return score.Unit(id=uid or f"L{level}r{run}:{ticket}", level=level, run=run,
                      ticket=ticket, kind=kind, y=y, loop=loop, p=p,
                      first=first if first is not None else p,
                      shown=shown if shown is not None else (p,), s=tuple(s), t=tuple(t),
                      u=tuple(u))


Y, W, P = "T1_GENERAL", "BILLING_SPECIALIST", "T2_TECHNICAL"


class TestTheTermsByHand(unittest.TestCase):

    def test_hits(self):
        self.assertEqual(score.hits((Y, Y), Y), 1)
        self.assertEqual(score.hits((Y, None), Y), F(1, 2))
        self.assertEqual(score.hits((None, None), Y), 0)
        self.assertEqual(score.hits((Y, Y), None), 0)

    def test_the_terms(self):
        u = unit(s=(W, Y), t=(Y, Y), u=(W, W), loop=W)
        self.assertEqual(score.x_a_term(u), 0 - F(1, 2))
        self.assertEqual(score.accuracy_gap("t", "s")(u), F(1, 2))
        self.assertEqual(score.x_c_term(u), 2 - F(1, 2))
        self.assertEqual(score.accuracy_gap("t", "u")(u), 1)
        pull = unit(s=(P, Y), t=(Y, P), p=P)
        self.assertEqual(score.x_d_term(pull), F(1, 2) - 1)

    def test_the_share_and_its_comparison_agree(self):
        us = [unit(s=(W, W), t=(Y, Y)), unit(s=(Y, Y), t=(Y, Y)),
              unit(s=(W, W), t=(W, W)), unit(s=(W, Y), t=(Y, W))]
        # acc_s = 3/8 and acc_t = 5/8: the share is (2/8) / (5/8), and the
        # comparison 2·5/8 − 3/8 − 1 = −1/8 says the same thing.
        share = score.x_c_share(us)
        lin = score.statistic(score.SPECS[2], us)
        self.assertEqual(share, F(2, 5))
        self.assertEqual(lin, F(-1, 8))
        self.assertEqual(lin >= 0, share >= plan.X_C_LINE)

    def test_the_clustered_error(self):
        terms = [(1, F(1)), (1, F(1)), (2, F(0)), (2, F(0))]
        self.assertAlmostEqual(score.clustered_se(terms), 0.5)
        self.assertIsNone(score.clustered_se([(1, F(1)), (1, F(0))]))
        self.assertIsNone(score.clustered_se([(1, F(1))]))

    def test_changed_answers_are_classified(self):
        u = unit(s=(P, "SELF_SERVICE_DEFLECT"), t=(Y, Y), p=P, first=W,
                 shown=(W, P, P))
        self.assertEqual(score.changed(u, 0), "plurality")
        self.assertEqual(score.changed(u, 1), "not_shown")
        v = unit(s=(W, "ACCOUNT_MANAGER"), t=(Y, Y), p=P, first=W,
                 shown=(W, P, P, "ACCOUNT_MANAGER"))
        self.assertEqual(score.changed(v, 0), "first_shown")
        self.assertEqual(score.changed(v, 1), "other_shown")
        self.assertIsNone(score.changed(unit(s=(Y, None), t=(Y, Y)), 0))
        self.assertIsNone(score.changed(unit(s=(Y, None), t=(Y, Y)), 1))


class TestTheVerdictsByHand(unittest.TestCase):

    def spec(self, rid: str) -> score.Spec:
        return next(s for s in score.SPECS if s.id == rid)

    def many(self, n: int, **kw) -> list[score.Unit]:
        return [unit(ticket=i, run=1 + i % 3, uid=f"L{kw.get('level', 3)}r{1 + i % 3}:{i}", **kw)
                for i in range(n)]

    def test_each_line_is_exact_at_its_edge(self):
        # X-b holds above 0: a gap of exactly 0 is a refutation.
        even = self.many(120, s=(Y, Y), t=(Y, Y))
        self.assertEqual(score.adjudicate(self.spec("X-b"), even)["verdict"], "refuted")
        # X-c holds at 1/2: the share exactly 1/2 holds.
        half = (self.many(60, s=(W, W), t=(Y, Y)) + self.many(60, s=(W, W), t=(W, W)))
        half = [dataclasses.replace(u, ticket=i, id=f"x{i}") for i, u in enumerate(half)]
        got = score.adjudicate(self.spec("X-c"), half)
        self.assertEqual(got["share"]["fraction"], "1/2")
        self.assertEqual(got["verdict"], "holds")
        # X-a holds at <= 1/20: exactly 1/20 holds.
        a = (self.many(19, level=0, s=(Y, Y), loop=Y)
             + self.many(1, level=0, s=(Y, Y), loop=W))
        a = [dataclasses.replace(u, ticket=i, id=f"a{i}") for i, u in enumerate(a)]
        got = score.adjudicate(self.spec("X-a"), a)
        self.assertEqual(got["value"]["fraction"], "1/20")
        self.assertEqual(got["verdict"], "holds")

    def test_a_row_with_too_many_invalid_answers_has_no_value(self):
        us = self.many(100, s=(Y, Y), t=(Y, Y))
        us[:6] = [dataclasses.replace(u, s=(None, Y)) for u in us[:6]]
        got = score.adjudicate(self.spec("X-b"), us)
        self.assertEqual(got["verdict"], "unadjudicable")
        us[5] = dataclasses.replace(us[5], s=(Y, Y))
        self.assertNotEqual(score.adjudicate(self.spec("X-b"), us)["verdict"], "unadjudicable")

    def test_x_d_needs_a_hundred_decisions_off_the_plurality(self):
        off = self.many(99, s=(P, P), t=(Y, Y), p=P)
        on = self.many(50, s=(P, P), t=(P, P), p=P)
        on = [dataclasses.replace(u, ticket=1000 + u.ticket, id="on" + u.id) for u in on]
        got = score.adjudicate(self.spec("X-d"), off + on)
        self.assertEqual(got["verdict"], "unadjudicable")
        more = off + [dataclasses.replace(off[0], ticket=999, id="extra")]
        got = score.adjudicate(self.spec("X-d"), more + on)
        self.assertEqual((got["read"], got["verdict"]), (100, "holds"))

    def test_x_c_has_no_value_when_the_screen_arm_is_always_right(self):
        got = score.adjudicate(self.spec("X-c"), self.many(120, s=(Y, Y), t=(Y, Y)))
        self.assertEqual(got["verdict"], "unadjudicable")

    def test_thin_by_the_error_and_by_one_run(self):
        # A gap carried by one run: dropping it flips the verdict.
        us = (self.many(30, s=(W, W), t=(Y, Y))
              + self.many(90, s=(Y, Y), t=(Y, Y)))
        us = [dataclasses.replace(u, run=1 if i < 30 else 2 + i % 2, ticket=i, id=f"r{i}")
              for i, u in enumerate(us)]
        got = score.adjudicate(self.spec("X-b"), us)
        self.assertEqual(got["verdict"], "holds")
        self.assertTrue(got["thin"])
        self.assertIn("L3r1", got["thin_because"]["dropping_one_run_flips"])
        # A wide gap spread over every run is not thin.
        wide = self.many(120, s=(W, W), t=(Y, Y))
        got = score.adjudicate(self.spec("X-b"), wide)
        self.assertEqual((got["verdict"], got["thin"]), ("holds", False))

    def test_x_f_reads_the_ticket_arm_at_level_0(self):
        us = self.many(120, t=(Y, Y), u=(W, W))
        got = score.adjudicate(self.spec("X-f"), us)
        self.assertEqual((got["value"]["fraction"], got["verdict"]), ("1/1", "holds"))
        self.assertEqual(got["parts"]["acc_u"]["fraction"], "0/1")


class TestStageCEndToEnd(unittest.TestCase):
    """The whole of Stage C over synthetic passes: every ask answered with one
    queue, so that the scorer runs over the real design and the real labels
    and computes no figure of the plan."""

    def test_score_runs_over_the_whole_design(self):
        design = population.build()
        recs = {}
        for s in plan.SESSIONS[1:]:
            recs[s] = {"rows": [{"id": aid, "arm": design.asks[aid].arm, "valid": True,
                                 "action": ACTIONS[i % len(ACTIONS)],
                                 "payload": {"action": ACTIONS[i % len(ACTIONS)],
                                             "conditions": [{"attr": "severity", "op": "gte",
                                                             "value": 1}], "note": "n"},
                                 "failure": None, "attempts": 1, "seconds": 1.0,
                                 "call_attempts": [{"provider": "p", "finish_reason": "stop",
                                                    "prompt_tokens": 1, "completion_tokens": 1,
                                                    "reasoning_tokens": 0}]}
                                for i, aid in enumerate(design.sessions[s])]}
        lab = score.labels()
        self.assertEqual(len(lab), 790)
        out = score.score(design, recs, lab)
        self.assertEqual(set(out["verdicts"]), {"X-a", "X-b", "X-c", "X-d", "X-e", "X-f"})
        for v in out["verdicts"].values():
            self.assertIn(v["verdict"], {"holds", "refuted", "unadjudicable"})
        self.assertEqual(set(out["X-g"]), {"by_level", "by_true_queue", "rules_written",
                                           "against_plan_screen", "the_calls"})
        self.assertEqual(out["X-g"]["against_plan_screen"]["tickets"], 183)
        self.assertEqual(out["X-g"]["the_calls"]["pass1"]["answers"], 1454)
        self.assertFalse(out["X-g"]["the_calls"]["pass1"]["notes"]["coded"])
        json.dumps(out)


if __name__ == "__main__":
    unittest.main()
