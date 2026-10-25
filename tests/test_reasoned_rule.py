"""
PLAN_REASONED_RULE.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the client, the pin, both reasoning
    settings and both budgets are `PLAN_FIRST_MATCH.md`'s, imported rather than
    retyped (rule A), and that each arm carries the setting §1 gives it.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `reasoned_rule/ask.py` exits before it builds a client.
  * The design: `PLAN_QUEUE_ALONE.md`'s rule and plain prompts at level 3, two
    arms each, their ids and digests that plan's and `PLAN_FIRST_MATCH.md`'s,
    each reasoning arm's texts its quiet arm's, what each prompt serves, the
    schedule, and nothing in the design that carries a label.
  * The requests, through the SDK double: every arm's carries the model, the
    temperature, the pin and `response_format` first, with its own reasoning
    setting and budget. The rule arm's is `PLAN_QUEUE_ALONE.md`'s rule arm's,
    request for request; the plain and reasoning arms' are
    `PLAN_FIRST_MATCH.md`'s; the reasoning rule arm's is the rule arm's with the
    reasoning arm's settings. A failed call is retried with the same messages
    after a wait, and a failed parse with v1's message (rule H).
  * Stage B end to end through the double: the attempts, the provider, the
    reasoning and the keys' order kept, an answer from another provider
    invalid, a session resumed, an outage stopping without recording, the
    turns, and the smoke check's pin and reasoning.
  * Stage C by hand: every term of §0, `RR-d` held below its line and its
    condition for having no value, the anchor, every reason a row has no value,
    *thin* both ways, the reading of a rule written, and the whole stage over
    synthetic passes.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double, or something that fails the test if it is ever built. Every record
a test writes lands in a temporary directory that `plan.OUT` is pointed at.
**No figure of the plan is computed, and no reference Stage A computes after
the signature**: the only answers ever scored are the double's or synthetic
ones, and the rules a ticket matches are read on tickets and lists built by
hand, or stubbed where the whole design is scored.
"""

from __future__ import annotations

import dataclasses
import json
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import Case
from rung2.proposers2 import ProposalError

from apply import score as ascore
from first_match import ask as fm_ask
from first_match import plan as fm_plan
from first_match import population as fm_pop
from manual.run import build_proposer
from queue_alone import ask as qask
from queue_alone import population as qpop
from queue_alone import prompts as qprompts
from queue_alone import rules as qrules
from queue_alone import score as qscore

from reasoned_rule import ask, gates, plan, population, prompts, sample, score, shape
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
F = Fraction
S, P, Y, W = "SECURITY_INCIDENT", "T2_TECHNICAL", "T1_GENERAL", "BILLING_SPECIALIST"


class BaiduShaped(OpenRouterShapedClient):
    """The double, served by the provider the plan pins."""
    PROVIDER = plan.PROVIDER_NAME


class Reasons(BaiduShaped):
    """The double, reasoning when and only when the request asks it to: its
    message then carries a reasoning, and its usage reasoning tokens."""
    REASONING = "H01 no casa: el tier es free. H02 casa."

    def _create(self, **kwargs):
        resp = super()._create(**kwargs)
        on = kwargs["extra_body"]["reasoning"] != plan.REASONING_OFF
        resp.choices[0].message = SimpleNamespace(
            content=resp.choices[0].message.content,
            reasoning=self.REASONING if on else None)
        resp.usage.completion_tokens_details = SimpleNamespace(
            reasoning_tokens=321 if on else 0)
        return resp


class Raises:
    """A script that raises on the calls it is told to, as an upstream 429 does,
    and answers the rest."""

    def __init__(self, fail: set[int], text: str):
        self.fail, self.text, self.n = fail, text, 0

    def __call__(self, kwargs):
        self.n += 1
        if self.n in self.fail:
            raise RuntimeError("Error code: 429 - temporarily rate-limited upstream")
        return self.text


RULE_PAYLOAD = {"action": P, "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                "beats": [], "loses_to": [], "note": "una regla"}


def answer_json(action: str = P, rule: bool = False) -> str:
    return json.dumps({**RULE_PAYLOAD, "action": action} if rule else {"action": action})


def by_arm(kwargs: dict) -> str:
    """The double's answer: a rule and a queue to the rule arms, a queue to the
    others."""
    return answer_json(rule='"conditions"' in kwargs["messages"][0]["content"])


def fake_checks(passes: bool = True, design=None) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED, design=design or population.build())


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
    """The design with each pass cut to the first `k` prompts of pass 1's order,
    so that a test asks a few prompts of each arm and not 684."""
    head = design.sessions["pass1"][:k]
    return dataclasses.replace(design, sessions={"smoke": design.sessions["smoke"],
                                                 "pass1": head,
                                                 "pass2": list(reversed(head))})


def ticket(**kw) -> dict:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return {**base, **kw}


def case(**kw) -> Case:
    return Case(**ticket(**kw))


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_first_matchs(self):
        self.assertEqual(plan.MODEL, fm_plan.MODEL)
        self.assertEqual(plan.MODEL, "deepseek/deepseek-v4-flash")
        self.assertEqual((plan.PROMPT, plan.TEMPERATURE), ("v1", 0))
        self.assertIs(plan.REASONING_OFF, fm_plan.REASONING_OFF)
        self.assertIs(plan.REASONING_ON, fm_plan.REASONING_ON)
        self.assertEqual((plan.REASONING_OFF, plan.REASONING_ON),
                         ({"effort": "none"}, {"effort": "high"}))
        self.assertEqual((plan.MAX_TOKENS, plan.MAX_TOKENS_REASONING), (1200, 16000))
        self.assertEqual((plan.MAX_TOKENS, plan.MAX_TOKENS_REASONING),
                         (fm_plan.MAX_TOKENS, fm_plan.MAX_TOKENS_REASONING))
        self.assertEqual((plan.MAX_RETRIES, plan.CALL_RETRY_WAIT), (2, (10, 30)))
        self.assertIs(plan.CALL_RETRY_WAIT, fm_plan.CALL_RETRY_WAIT)

    def test_each_arm_carries_section_1s_settings(self):
        for arm in ("t", "q"):
            with self.subTest(arm):
                self.assertEqual(plan.settings(arm), {"reasoning": {"effort": "none"},
                                                      "max_tokens": 1200})
        for arm in ("w", "r"):
            with self.subTest(arm):
                self.assertEqual(plan.settings(arm), {"reasoning": {"effort": "high"},
                                                      "max_tokens": 16000})
        self.assertEqual(plan.settings("r"), fm_plan.settings("r"))
        self.assertEqual(plan.settings("q"), fm_plan.settings("q"))
        plan.settings("w")["reasoning"]["effort"] = "low"
        self.assertEqual(plan.REASONING_ON, {"effort": "high"})
        for bad in ("n", "i", "z"):
            with self.subTest(bad), self.assertRaises(ValueError):
                plan.settings(bad)

    def test_the_pin_is_the_closed_plans(self):
        self.assertEqual(plan.PROVIDER, {"order": ["baidu"], "allow_fallbacks": False})
        self.assertIs(plan.PROVIDER, fm_plan.PROVIDER)
        self.assertEqual(plan.PROVIDER_NAME, "Baidu")

    def test_the_inputs_and_the_population(self):
        self.assertEqual((plan.LEVEL, plan.REPS, plan.N, plan.SEED), (3, 3, 2000, 17))
        self.assertEqual((plan.TICKET_PROMPTS, plan.DECISIONS), (171, 320))
        self.assertEqual((plan.TICKET_PROMPTS, plan.DECISIONS),
                         (fm_plan.TICKET_PROMPTS, fm_plan.DECISIONS))
        self.assertEqual(plan.queue_alone_sample(), Path("results_queue_alone/sample.json"))
        self.assertEqual(plan.queue_alone_ask("pass2"),
                         Path("results_queue_alone/ask_pass2.json"))
        self.assertEqual((plan.first_match_sample(), plan.first_match_score()),
                         (Path("results_first_match/sample.json"),
                          Path("results_first_match/score.json")))
        self.assertEqual(plan.first_match_ask("pass1"),
                         Path("results_first_match/ask_pass1.json"))

    def test_the_arms(self):
        self.assertEqual(prompts.ARMS, ("t", "w", "q", "r"))
        self.assertEqual(set(plan.REASONING_ARMS + plan.QUIET_ARMS), set(prompts.ARMS))
        self.assertEqual((plan.REASONING_ARMS, plan.QUIET_ARMS), (("w", "r"), ("t", "q")))

    def test_the_sessions_and_the_limits(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "pass1", "pass2"))
        self.assertEqual((plan.PASSES, plan.SMOKE_PER_ARM), (2, 2))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MAX_CONSECUTIVE_FAILURES,
                          plan.MIN_ANCHOR_PROMPTS), (1, 5, 100))
        self.assertEqual(plan.MAX_INVALID_SHARE, F(1, 20))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 79)
        self.assertNotIn(plan.ORDER_SEED,
                         {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61, 67, 71, 73})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_lines_are_section_0s_as_fractions(self):
        lines = {"RR_A_MAX_GAP": F(1, 20), "RR_B_LINE": F(0), "RR_C_LINE": F(9, 10),
                 "RR_D_LINE": F(0)}
        for name, value in lines.items():
            with self.subTest(name):
                self.assertIsInstance(getattr(plan, name), Fraction)
                self.assertEqual(getattr(plan, name), value)

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_REASONED_RULE.md").read_text()
        for needle in ("`ORDER_SEED = 79`", "`TICKET_PROMPTS = 171`", "`DECISIONS = 320`",
                       '`ARMS = ("t", "w", "q", "r")`', "`SMOKE_PER_ARM = 2`",
                       "`MAX_TOKENS_REASONING = 16000`", "`CALL_RETRY_WAIT = (10, 30)`",
                       "`RR_A_MAX_GAP = Fraction(1, 20)`", "`RR_C_LINE = Fraction(9, 10)`",
                       "`RR_D_LINE = 0`, held below", "`MIN_ANCHOR_PROMPTS = 100`"):
            with self.subTest(needle):
                self.assertIn(needle, text)

    def test_the_gate_reads_this_plan_and_the_records_land_in_their_directory(self):
        self.assertEqual(plan.PLAN, Path("PLAN_REASONED_RULE.md"))
        self.assertEqual(plan.ask_path("pass1"), Path("results_reasoned_rule/ask_pass1.json"))
        self.assertEqual(plan.partial_path("smoke"),
                         Path("results_reasoned_rule/ask_smoke.partial.jsonl"))
        self.assertEqual((plan.sample_path(), plan.score_path()),
                         (Path("results_reasoned_rule/sample.json"),
                          Path("results_reasoned_rule/score.json")))
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
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-25)**\n", True),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-25)**\n"
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
        as two of `PLAN_APPLY.md`'s did on 2026-10-23."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_REASONED_RULE.md")["found"],
                         plan.MIN_SIGNATURES)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("asker built")) as asker, \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        for m in (checks, asker, fetch, write):
            m.assert_not_called()

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
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("asker built")) as asker, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        for m in (fetch, asker, write):
            m.assert_not_called()

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
                               side_effect=AssertionError("checks ran")) as checks:
            for s in ("pass1", "pass2"):
                with self.subTest(s), self.assertRaises(SystemExit):
                    ask.main(["--session", s])
        fetch.assert_not_called()
        checks.assert_not_called()


# ---------------------------------------------------------------------------
# The design
# ---------------------------------------------------------------------------

class TestTheDesignIsTheClosedPlansLevel3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.d = population.build()
        cls.qa = qpop.build()
        cls.fm = fm_pop.build()

    def test_four_arms_on_every_level_3_ticket(self):
        for arm in prompts.ARMS:
            with self.subTest(arm):
                self.assertEqual(len(self.d.asks_of(arm)), plan.TICKET_PROMPTS)
        self.assertEqual(len(self.d.asks), 4 * 171)
        self.assertEqual(len(self.d.decisions), plan.DECISIONS)
        self.assertEqual({e.level for e in self.d.decisions.values()}, {3})

    def test_the_rule_and_plain_arms_are_plan_queue_alones(self):
        for arm, theirs_arm in (("t", qprompts.RULE), ("q", qprompts.PLAIN)):
            theirs = {i: a for i, a in self.qa.asks.items()
                      if a.arm == theirs_arm and a.level == 3}
            mine = {i: a for i, a in self.d.asks.items() if a.arm == arm}
            with self.subTest(arm):
                self.assertEqual(set(mine), set(theirs))
                for i in sorted(mine)[::20]:
                    self.assertEqual((mine[i].system, mine[i].user, mine[i].digest),
                                     (theirs[i].system, theirs[i].user, theirs[i].digest))

    def test_the_plain_and_reasoning_arms_are_plan_first_matchs(self):
        for arm in ("q", "r"):
            mine = {i: a for i, a in self.d.asks.items() if a.arm == arm}
            theirs = {i: a for i, a in self.fm.asks.items() if a.arm == arm}
            with self.subTest(arm):
                self.assertEqual(set(mine), set(theirs))
                for i in sorted(mine)[::20]:
                    self.assertEqual(mine[i].messages(), theirs[i].messages())

    def test_each_reasoning_arm_is_its_quiet_arm_text_for_text(self):
        for arm, quiet in (("w", "t"), ("r", "q")):
            for a in self.d.asks_of(arm)[::20]:
                b = self.d.asks[prompts.ask_id(quiet, a.ticket)]
                with self.subTest(a.id):
                    self.assertEqual((a.system, a.user, a.digest), (b.system, b.user, b.digest))
                    self.assertEqual(a.messages(), b.messages())

    def test_each_prompt_serves_what_the_closed_plans_prompt_served(self):
        for i, a in list(self.d.asks.items())[::17]:
            qid = qprompts.ask_id(prompts.asked_as(a.arm), 3, a.ticket)
            with self.subTest(i):
                self.assertEqual(self.d.serves[i], self.qa.serves[qid]["own"])

    def test_nothing_in_the_design_carries_a_label(self):
        text = json.dumps(self.d.summary())
        for word in ("truth", "predicted", "correct", '"y"', "loop"):
            with self.subTest(word):
                self.assertNotIn(word, text)

    def test_the_schedule(self):
        self.assertEqual(population.sessions_for(self.d.asks), self.d.sessions)
        smoke = self.d.sessions["smoke"]
        self.assertEqual(len(smoke), len(set(smoke)))
        self.assertEqual(sorted(self.d.asks[i].arm for i in smoke),
                         ["q", "q", "r", "r", "t", "t", "w", "w"])
        for s in ("pass1", "pass2"):
            self.assertEqual(sorted(self.d.sessions[s]), sorted(self.d.asks))
        self.assertNotEqual(self.d.sessions["pass1"], self.d.sessions["pass2"])

    def test_the_four_gates_pass_without_the_suite(self):
        checks = gates.run_checks(suite=False)
        self.assertTrue(checks.g1["passes"], checks.g1)
        self.assertTrue(checks.g2["passes"], checks.g2)
        self.assertTrue(checks.g3["passes"], checks.g3)
        self.assertTrue(checks.blocking_pass)


# ---------------------------------------------------------------------------
# The prompts
# ---------------------------------------------------------------------------

class TestThePromptsAreTheClosedPlans(unittest.TestCase):

    def test_each_arm_sends_a_closed_plans_prompt(self):
        self.assertEqual({arm: prompts.asked_as(arm) for arm in prompts.ARMS},
                         {"t": qprompts.RULE, "w": qprompts.RULE,
                          "q": qprompts.PLAIN, "r": qprompts.PLAIN})
        c = case()
        for arm in prompts.ARMS:
            theirs = prompts.asked_as(arm)
            with self.subTest(arm):
                self.assertEqual(prompts.system_prompt(arm), qprompts.system_prompt(theirs, 3))
                self.assertEqual(prompts.user_message(arm, c),
                                 qprompts.user_message(theirs, c))
        self.assertTrue(prompts.user_message("w", c).startswith(qprompts.EMPTY_BASE))
        self.assertTrue(prompts.user_message("r", c).startswith("TICKET:\n"))
        self.assertEqual(prompts.RETRY_MSG, qprompts.RETRY_MSG)

    def test_the_ids(self):
        self.assertEqual([prompts.ask_id(arm, 17) for arm in prompts.ARMS],
                         ["t:L3:17", "w:L3:17", "q:L3:17", "r:L3:17"])

    def test_an_unknown_arm_is_refused(self):
        c = case()
        for bad in ("n", "i", "z"):
            with self.subTest(bad):
                with self.assertRaises(ValueError):
                    prompts.system_prompt(bad)
                with self.assertRaises(ValueError):
                    prompts.user_message(bad, c)
                with self.assertRaises(ValueError):
                    prompts.ask(bad, 1, c)


# ---------------------------------------------------------------------------
# The requests, through the SDK double
# ---------------------------------------------------------------------------

class TestTheRequests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.d = population.build()

    def asked(self, a: prompts.Ask, client, sleep=None, asker=None) -> tuple[dict, list[dict]]:
        with fake_sdk(openai=client):
            got = (asker or ask.Asker)(sleep=sleep or (lambda s: None)).ask(a)
        return got, client.peticiones

    def test_each_arm_sends_its_settings_with_the_pin(self):
        for arm in prompts.ARMS:
            a = self.d.asks_of(arm)[0]
            got, (req,) = self.asked(a, Reasons(by_arm))
            s = plan.settings(arm)
            with self.subTest(arm):
                self.assertEqual(req["model"], plan.MODEL)
                self.assertEqual(req["temperature"], 0)
                self.assertEqual(req["max_tokens"], s["max_tokens"])
                self.assertEqual(req["response_format"], {"type": "json_object"})
                self.assertEqual(req["extra_body"], {"reasoning": s["reasoning"],
                                                     "provider": plan.PROVIDER})
                self.assertEqual(req["messages"], a.messages())
                self.assertEqual(got["action"], P)
                self.assertEqual(got["retries"], [])

    def test_the_rule_arm_is_plan_queue_alones_rule_arm_request(self):
        a = self.d.asks_of("t")[0]
        theirs_client = BaiduShaped(FixedResponses(answer_json(rule=True)))
        with fake_sdk(openai=theirs_client):
            qask.pin(build_proposer(3)).propose(a.case, qprompts.EMPTY_BASE)
        _, (mine,) = self.asked(a, BaiduShaped(FixedResponses(answer_json(rule=True))))
        (theirs,) = theirs_client.peticiones
        self.assertEqual(mine, theirs)

    def test_the_plain_and_reasoning_arms_are_plan_first_matchs_requests(self):
        for arm in ("q", "r"):
            a = self.d.asks_of(arm)[0]
            _, (theirs,) = self.asked(a, BaiduShaped(FixedResponses(answer_json())),
                                      asker=fm_ask.Asker)
            _, (mine,) = self.asked(a, BaiduShaped(FixedResponses(answer_json())))
            with self.subTest(arm):
                self.assertEqual(mine, theirs)

    def test_the_reasoning_rule_arm_differs_from_the_rule_arm_in_its_settings_alone(self):
        t = self.d.asks_of("t")[0]
        w = self.d.asks[prompts.ask_id("w", t.ticket)]
        _, (rt,) = self.asked(t, BaiduShaped(FixedResponses(answer_json(rule=True))))
        _, (rw,) = self.asked(w, BaiduShaped(FixedResponses(answer_json(rule=True))))
        self.assertEqual({k: v for k, v in rt.items() if k not in ("max_tokens", "extra_body")},
                         {k: v for k, v in rw.items() if k not in ("max_tokens", "extra_body")})
        self.assertEqual(rw["extra_body"]["provider"], rt["extra_body"]["provider"])
        self.assertEqual((rw["max_tokens"], rw["extra_body"]["reasoning"]),
                         (16000, {"effort": "high"}))
        _, (rr,) = self.asked(self.d.asks[prompts.ask_id("r", t.ticket)],
                              BaiduShaped(FixedResponses(answer_json())))
        self.assertEqual((rw["max_tokens"], rw["extra_body"]), (rr["max_tokens"],
                                                                rr["extra_body"]))

    def test_the_answer_keeps_its_rule_its_keys_in_order_and_the_reasoning(self):
        w = self.d.asks_of("w")[0]
        got, _ = self.asked(w, Reasons(by_arm))
        self.assertEqual(got["payload"], RULE_PAYLOAD)
        self.assertEqual(got["keys"], ["action", "conditions", "beats", "loses_to", "note"])
        self.assertEqual(got["reasoning"], Reasons.REASONING)
        got, _ = self.asked(self.d.asks_of("t")[0], Reasons(by_arm))
        self.assertIsNone(got["reasoning"])

    def test_a_failed_parse_is_retried_with_v1s_message(self):
        a = self.d.asks_of("w")[0]
        waits = []
        got, reqs = self.asked(a, BaiduShaped(FixedResponses("no es json",
                                                             answer_json(rule=True))),
                               sleep=waits.append)
        self.assertEqual(len(reqs), 2)
        self.assertNotIn("response_format", reqs[1])
        self.assertEqual(reqs[1]["messages"][-1],
                         {"role": "user", "content": prompts.RETRY_MSG})
        self.assertEqual(reqs[1]["extra_body"]["reasoning"], {"effort": "high"})
        self.assertEqual((got["retries"], waits), (["parse"], []))

    def test_a_failed_call_is_retried_with_the_same_messages_after_a_wait(self):
        a = self.d.asks_of("t")[0]
        waits = []
        got, reqs = self.asked(a, BaiduShaped(Raises({1, 2}, answer_json(rule=True))),
                               sleep=waits.append)
        self.assertEqual(len(reqs), 3)
        for req in reqs:
            self.assertEqual(req["messages"], a.messages())
            self.assertNotIn(prompts.RETRY_MSG, json.dumps(req["messages"]))
        self.assertEqual(got["retries"], ["call", "call"])
        self.assertEqual(waits, list(plan.CALL_RETRY_WAIT))
        self.assertEqual(got["action"], P)

    def test_every_attempt_failing_says_why_each_did(self):
        a = self.d.asks_of("q")[0]
        with fake_sdk(openai=BaiduShaped(Raises({1, 2, 3}, answer_json()))):
            asker = ask.Asker(sleep=lambda s: None)
            with self.assertRaises(ask.AskFailed) as caught:
                asker.ask(a)
        self.assertEqual(caught.exception.causes, ["call", "call", "call"])
        self.assertIsInstance(caught.exception, ProposalError)

    def test_the_asker_is_plan_first_matchs(self):
        self.assertTrue(issubclass(ask.Asker, fm_ask.Asker))
        self.assertIs(ask.Asker.ask, fm_ask.Asker.ask)
        self.assertNotIn("ask", vars(ask.Asker))


# ---------------------------------------------------------------------------
# Stage B, through the double
# ---------------------------------------------------------------------------

class Failing:
    """An asker that fails, as a dropped connection or a pinned provider down."""

    def ask(self, a):
        raise ask.AskFailed("RuntimeError: 429", ["call", "call", "call"])


class TestStageB(unittest.TestCase):

    def setUp(self):
        self.design = small(population.build())

    def run_session(self, out: Path, session: str, asker=None, **kw):
        header = {"protocol": json.loads(json.dumps(ask.protocol())), "session": session,
                  "sample_sha256": "x"}
        return ask.ask(session, self.design, asker or ask.Asker(sleep=lambda s: None),
                       out / f"{session}.jsonl", header, **kw)

    def test_a_pass_keeps_the_attempts_the_provider_the_reasoning_and_no_label(self):
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=Reasons(by_arm)), \
             mock.patch("builtins.print"):
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(resumed, [])
        for r in rows:
            with self.subTest(r["id"]):
                self.assertTrue(r["valid"])
                self.assertEqual(r["served_by"], plan.PROVIDER_NAME)
                self.assertEqual(r["digest"], self.design.asks[r["id"]].digest)
                self.assertEqual(r["call_attempts"][-1]["provider"], plan.PROVIDER_NAME)
                self.assertEqual(r["retries"], [])
                self.assertFalse({"truth", "labels", "predicted", "y"} & set(r))
                if r["arm"] in plan.REASONING_ARMS:
                    self.assertEqual(r["reasoning"], Reasons.REASONING)
                    self.assertEqual(r["call_attempts"][-1]["reasoning_tokens"], 321)
                else:
                    self.assertIsNone(r["reasoning"])
                if r["arm"] in prompts.RULE_ARMS:
                    self.assertEqual(r["payload"], RULE_PAYLOAD)

    def test_an_answer_from_another_provider_is_invalid(self):
        with tempfile.TemporaryDirectory() as d, \
             fake_sdk(openai=OpenRouterShapedClient(by_arm)), mock.patch("builtins.print"):
            rows, _ = self.run_session(Path(d), "pass1")
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(r["action"], P)
            self.assertEqual(r["served_by"], OpenRouterShapedClient.PROVIDER)
            self.assertFalse(r["valid"])
            self.assertIsNone(score.answer(r))

    def test_an_interrupted_session_resumes_where_it_stopped(self):
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=Reasons(by_arm)), \
             mock.patch("builtins.print"):
            asker = ask.Asker(sleep=lambda s: None)
            real = asker.ask
            n = {"calls": 0}

            def interrupting(a):
                n["calls"] += 1
                if n["calls"] == 5:
                    raise KeyboardInterrupt
                return real(a)

            with mock.patch.object(asker, "ask", side_effect=interrupting), \
                 self.assertRaises(KeyboardInterrupt):
                self.run_session(Path(d), "pass1", asker=asker)
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(len(resumed), 1)

    def test_an_outage_stops_the_session_without_recording_it(self):
        with tempfile.TemporaryDirectory() as d, mock.patch("builtins.print"):
            with self.assertRaises(ask.Outage):
                self.run_session(Path(d), "pass1", asker=Failing())
            lines = (Path(d) / "pass1.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)          # the header, and no failure

    def test_an_isolated_failure_is_recorded_with_its_causes(self):
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=Reasons(by_arm)), \
             mock.patch("builtins.print"):
            asker = ask.Asker(sleep=lambda s: None)
            real = asker.ask
            n = {"calls": 0}

            def once(a):
                n["calls"] += 1
                if n["calls"] == 2:
                    raise ask.AskFailed("RuntimeError: 429", ["call", "call", "call"])
                return real(a)

            with mock.patch.object(asker, "ask", side_effect=once):
                rows, _ = self.run_session(Path(d), "pass1", asker=asker)
        failed = [r for r in rows if r["failure"]]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["retries"], ["call", "call", "call"])
        self.assertFalse(failed[0]["valid"])

    def test_the_smoke_run_end_to_end_and_the_turns(self):
        design = self.design
        with TempOut(), fake_sdk(openai=Reasons(by_arm)), \
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
            self.assertTrue(ask.smoke_check()[0], ask.smoke_check()[1])
            self.assertEqual(len(rec["rows"]), 8)
            self.assertEqual(rec["provider"], plan.PROVIDER)
            self.assertEqual(rec["settings"]["w"], {"reasoning": {"effort": "high"},
                                                    "max_tokens": 16000})
            self.assertEqual(rec["settings"]["t"], {"reasoning": {"effort": "none"},
                                                    "max_tokens": 1200})
            self.assertIn("_env", rec)
            ok, why = ask.previous_check("pass2")
            self.assertFalse(ok)
            self.assertIn("pass 1", why)
            self.assertTrue(ask.previous_check("pass1")[0])
            with self.assertRaises(SystemExit):
                ask.main(["--session", "pass2"])
            with self.assertRaises(SystemExit):           # a paid record is never overwritten
                ask.main(["--session", "smoke"])

    def test_the_smoke_check_wants_the_pin_and_the_reasoning(self):
        def row(arm, tokens=None, finish="stop", reasoning=None, provider=None):
            return {"id": f"{arm}:L3:1", "arm": arm, "valid": True,
                    "payload": {"action": P}, "reasoning": reasoning,
                    "call_attempts": [{"provider": provider or plan.PROVIDER_NAME,
                                       "finish_reason": finish,
                                       "reasoning_tokens": tokens}]}

        def check(rows):
            rec = {**json.loads(json.dumps(ask.protocol())), "rows": rows}
            plan.ask_path("smoke").write_text(json.dumps(rec))
            return ask.smoke_check()

        with TempOut():
            good = [row("t", tokens=0), row("w", tokens=321), row("q", tokens=0),
                    row("r", tokens=321)]
            self.assertTrue(check(good)[0])
            self.assertTrue(check([row("t"), row("w", reasoning="pienso"), row("q"),
                                   row("r", tokens=9)])[0])
            cases = {"did not reason": [row("t"), row("w", tokens=0), row("q"),
                                        row("r", tokens=321)],
                     "budget": [row("t"), row("w", tokens=321, finish="length"), row("q"),
                                row("r", tokens=321)],
                     "only the reasoning arms": [row("t", tokens=5), row("w", tokens=321),
                                                 row("q"), row("r", tokens=321)],
                     "Relace": [row("t"), row("w", tokens=321), row("q", provider="Relace"),
                                row("r", tokens=321)],
                     "no valid answer": [row("t"), row("q"), row("r", tokens=321)]}
            for why, rows in cases.items():
                with self.subTest(why):
                    ok, said = check(rows)
                    self.assertFalse(ok)
                    self.assertIn(why, said)
            rec = {**json.loads(json.dumps(ask.protocol())), "rows": good}
            rec["settings"]["w"]["reasoning"] = {"effort": "medium"}
            plan.ask_path("smoke").write_text(json.dumps(rec))
            self.assertIn("protocol", ask.smoke_check()[1])

    def test_sample_matches_reads_the_sessions_and_the_digests(self):
        design = self.design
        with TempOut():
            summary = json.loads(json.dumps(design.summary()))
            plan.sample_path().write_text(json.dumps({"design": summary}))
            self.assertTrue(ask.sample_matches(design)[0])
            summary["asks"][design.sessions["pass1"][0]]["digest"] = "0" * 16
            plan.sample_path().write_text(json.dumps({"design": summary}))
            self.assertFalse(ask.sample_matches(design)[0])


# ---------------------------------------------------------------------------
# Stage A's references, on a design built by hand
# ---------------------------------------------------------------------------

HAND = ("H01: SI severity eq 1 ENTONCES A_Q\n"
        "H02: SI product eq api ENTONCES B_Q\n"
        "H03: SI severity gte 1 ENTONCES A_Q\n")


class TestStageAsReferencesOnAHandBuiltDesign(unittest.TestCase):

    def test_the_references(self):
        rs = qrules.parse(HAND)
        cases = {"L3r1:1": ticket(severity=1, product="api"),
                 "L3r1:2": ticket(severity=2, product="api")}
        decisions = {i: SimpleNamespace(level=3, ticket=k, prompt=SimpleNamespace(
            case=SimpleNamespace(as_dict=lambda c=c: c)))
            for k, (i, c) in enumerate(cases.items(), start=1)}
        asks = {"t:L3:1": SimpleNamespace(id="t:L3:1", arm="t")}
        design = SimpleNamespace(decisions=decisions,
                                 asks_of=lambda arm: [a for a in asks.values() if a.arm == arm])
        before = {1: {"t:L3:1": {"action": "A_Q", "served_by": "Baidu"}}, 2: {}}
        with mock.patch.object(qrules, "rules", return_value=rs):
            got = sample.references(design, before)
        self.assertEqual(got["matches"]["L3r1:1"], {"ticket": 1,
                                                    "matching": ["H01", "H02", "H03"],
                                                    "runner_up": "H02"})
        self.assertEqual(got["matches"]["L3r1:2"], {"ticket": 2, "matching": ["H02", "H03"],
                                                    "runner_up": "H03"})
        self.assertEqual(got["queue_alone_rule"]["t:L3:1"],
                         [{"pass": 1, "action": "A_Q", "served_by": "Baidu"},
                          {"pass": 2, "action": None, "served_by": None}])


# ---------------------------------------------------------------------------
# The rules written, read by hand
# ---------------------------------------------------------------------------

LIST = ("H01: SI product eq api AND severity lte 2 ENTONCES T3_ENGINEERING\n"
        "H02: SI product eq api ENTONCES T2_TECHNICAL\n"
        "H03: SI severity gte 1 ENTONCES T1_GENERAL\n")


def rule(action, *conditions, **edges) -> dict:
    return {"action": action, "conditions": [{"attr": a, "op": o, "value": v}
                                             for a, o, v in conditions], **edges}


class TestTheRulesWrittenByHand(unittest.TestCase):
    """Against a three-rule list built by hand, over the whole space: an
    exception, its general rule and the catch-all."""

    @classmethod
    def setUpClass(cls):
        cls.rs = qrules.parse(LIST)
        sp = shape.space()
        cls.api = sp.extension([shape.Condition(attr="product", op="eq", value="api")])
        cls.low = sp.extension([shape.Condition(attr="severity", op="lte", value=2)])

    def read(self, payload, c=None):
        return shape.read(payload, c or case(product="api", severity=3), self.rs)

    def test_the_lists_first_match_over_the_space(self):
        fm = shape.first_match_masks(self.rs)
        sp = shape.space()
        self.assertEqual(fm["T3_ENGINEERING"], self.api & self.low)
        self.assertEqual(fm["T2_TECHNICAL"], self.api & ~self.low)
        self.assertEqual(fm["T1_GENERAL"], sp.full & ~self.api)
        self.assertEqual(sum(m.bit_count() for m in fm.values()), sp.n)

    def test_the_general_rule_written_as_listed(self):
        got = self.read(rule("T2_TECHNICAL", ("product", "eq", "api"), beats=["H01"]))
        self.assertEqual((got["validates"], got["matches_ticket"], got["conditions"]),
                         (True, True, 1))
        self.assertEqual(got["points"], self.api.bit_count())
        self.assertEqual(got["right"], (self.api & ~self.low).bit_count())
        self.assertFalse(got["all_right"])
        self.assertEqual((got["same_region_as"], got["governing"], got["is_governing"]),
                         (["H02"], "H02", True))
        self.assertEqual((got["declares"], got["cites"]), (True, True))

    def test_a_narrower_rule_gets_all_of_its_region(self):
        got = self.read(rule("T2_TECHNICAL", ("product", "eq", "api"),
                             ("severity", "gte", 3), ("language", "eq", "en")))
        self.assertTrue(got["all_right"])
        self.assertEqual(got["right"], got["points"])
        self.assertLess(got["points"], self.api.bit_count())
        self.assertEqual((got["same_region_as"], got["is_governing"]), ([], False))

    def test_a_rule_the_ticket_does_not_match_and_one_that_does_not_validate(self):
        got = self.read(rule("T3_ENGINEERING", ("product", "eq", "api"),
                             ("severity", "lte", 2)))
        self.assertEqual((got["validates"], got["matches_ticket"]), (True, False))
        self.assertEqual(got["same_region_as"], ["H01"])
        self.assertEqual(self.read(rule(P, ("product", "lte", 2)))["why"],
                         "lte sobre atributo no numerico")
        self.assertEqual(self.read({"action": P, "conditions": []})["validates"], False)
        self.assertEqual(self.read(None), {"validates": False, "why": "no payload"})

    def test_the_identifiers_an_edge_cites(self):
        ids = {"H01", "H02", "H29"}
        self.assertTrue(shape.cites(["H01"], ids))
        self.assertTrue(shape.cites(["la regla H29"], ids))
        self.assertFalse(shape.cites(["H030", "R0012", "H30"], ids))
        self.assertEqual(shape.edges({"beats": "H01", "loses_to": ["H02", 3]}),
                         ["H01", "H02", "3"])
        self.assertEqual(shape.edges({"beats": None}), [])

    def test_the_summary_sets_the_share_beside_the_points(self):
        readings = [self.read(rule("T2_TECHNICAL", ("product", "eq", "api"))),
                    self.read(rule("T2_TECHNICAL", ("product", "eq", "api"),
                                   ("severity", "gte", 3))),
                    self.read(rule(P, ("product", "lte", 2)))]
        got = shape.summary(readings)
        self.assertEqual((got["answers"], got["validates"], got["all_right"]), (3, 2, 1))
        self.assertEqual(got["why_not"], {"lte sobre atributo no numerico": 1})
        self.assertEqual(got["conditions"], {"1": 1, "2": 1})
        right = (self.api & ~self.low).bit_count()
        pooled = F(2 * right, self.api.bit_count() + right)
        self.assertEqual(got["right_share_pooled"]["fraction"],
                         f"{pooled.numerator}/{pooled.denominator}")
        self.assertEqual((got["same_region_as_a_listed_rule"], got["as_the_governing_rule"],
                          got["listed_rules_written"]), (1, 1, {"H02": 1}))
        self.assertEqual(set(got["points"]), {"min", "median", "max"})


# ---------------------------------------------------------------------------
# Stage C by hand
# ---------------------------------------------------------------------------

HIT = ("H02", "H03", "H29")        # an exception, its general rule, the catch-all
QUEUES = (S, P, Y)


def unit(run=1, ticket_=1, y=S, t=(S, S), w=(S, S), q=(S, S), r=(S, S),
         hit=HIT, queues=QUEUES, uid=None) -> score.Unit:
    return score.Unit(id=uid or f"L3r{run}:{ticket_}", run=run, ticket=ticket_, y=y,
                      hit=tuple(hit), queues=tuple(queues), t=tuple(t), w=tuple(w),
                      q=tuple(q), r=tuple(r))


def spec(row: str) -> score.Spec:
    return next(s for s in score.SPECS if s.id == row)


class TestTheTermsByHand(unittest.TestCase):

    def test_an_answer_is_valid_only_from_the_pinned_provider(self):
        row = {"action": P, "served_by": plan.PROVIDER_NAME}
        self.assertEqual(score.answer(row), P)
        self.assertIsNone(score.answer({**row, "served_by": "Relace"}))
        self.assertIsNone(score.answer({**row, "action": "NOT_A_QUEUE"}))
        self.assertIsNone(score.answer(None))

    def test_the_classes(self):
        u = unit()
        self.assertEqual([score.klass(a, u) for a in (S, P, Y, W)],
                         ["first", "order", "order", "matching"])

    def test_the_units_from_rows(self):
        rs = qrules.parse(HAND)
        c = SimpleNamespace(as_dict=lambda: ticket(severity=1, product="api"))
        decisions = {"L3r2:5": SimpleNamespace(level=3, run=2, ticket=5,
                                               prompt=SimpleNamespace(case=c))}
        design = SimpleNamespace(decisions=decisions)
        ok = {"served_by": plan.PROVIDER_NAME}
        by_pass = {1: {"t:L3:5": {**ok, "action": W}, "w:L3:5": {**ok, "action": P},
                       "q:L3:5": {**ok, "action": S}, "r:L3:5": {**ok, "action": Y}},
                   2: {"t:L3:5": {"action": W, "served_by": "Relace"},
                       "w:L3:5": {**ok, "action": "NOT_A_QUEUE"}}}
        with mock.patch.object(qrules, "rules", return_value=rs):
            (u,) = score.units(design, by_pass, {"L3r2:5": {"y": "A_Q"}})
        self.assertEqual((u.run, u.ticket, u.y, u.hit, u.queues),
                         (2, 5, "A_Q", ("H01", "H02", "H03"), ("A_Q", "B_Q", "A_Q")))
        self.assertEqual((u.t, u.w, u.q, u.r), ((W, None), (P, None), (S, None), (Y, None)))

    def test_the_terms(self):
        u = unit(t=(P, S), w=(S, S), q=(S, Y), r=(S, S))
        self.assertEqual(spec("RR-b").term(u), 1 - F(1, 2))
        self.assertEqual(spec("RR-c").term(u), 1)
        self.assertEqual(spec("RR-d").term(u), (1 - 1) - (F(1, 2) - F(1, 2)))
        u = unit(t=(P, P), w=(S, P), q=(S, S), r=(S, S))
        self.assertEqual(spec("RR-d").term(u), (1 - F(1, 2)) - (1 - 0))

    def test_the_clustered_error_is_plan_applys(self):
        self.assertIs(score.clustered_se, ascore.clustered_se)
        self.assertIs(score.hits, ascore.hits)
        self.assertIs(score.labels, ascore.labels)


class TestTheVerdictsByHand(unittest.TestCase):

    def test_each_line_is_exact_at_its_edge(self):
        # RR-c at exactly 9/10: nine right of ten tickets holds.
        us = [unit(ticket_=k, w=(S, S) if k < 9 else (P, P)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("RR-c"), us)["verdict"], "holds")
        us[0] = unit(ticket_=0, w=(S, P))
        self.assertEqual(score.adjudicate(spec("RR-c"), us)["verdict"], "refuted")
        # RR-b at exactly 0 is refuted: its line is held above.
        us = [unit(ticket_=k) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("RR-b"), us)["verdict"], "refuted")
        us = [unit(ticket_=k, t=(P, P)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("RR-b"), us)["verdict"], "holds")

    def test_rr_d_is_held_below_its_line(self):
        # A cost of a half without reasoning, and none with it: it shrank.
        us = [unit(ticket_=k, t=(S, P), q=(S, S)) for k in range(10)]
        got = score.adjudicate(spec("RR-d"), us)
        self.assertEqual((got["verdict"], got["value"]["fraction"]), ("holds", "-1/2"))
        self.assertEqual(got["parts"]["cost_without_reasoning"]["fraction"], "1/2")
        self.assertEqual(got["parts"]["cost_with_reasoning"]["fraction"], "0/1")
        # The same cost with reasoning as without: a tie, so refuted.
        us = [unit(ticket_=k, t=(S, P), q=(S, S), w=(S, P), r=(S, S)) for k in range(10)]
        got = score.adjudicate(spec("RR-d"), us)
        self.assertEqual((got["verdict"], got["value"]["fraction"]), ("refuted", "0/1"))

    def test_rr_d_has_no_value_without_a_cost_to_shrink(self):
        us = [unit(ticket_=k, w=(S, P)) for k in range(10)]          # acc_q − acc_t = 0
        got = score.adjudicate(spec("RR-d"), us)
        self.assertEqual(got["verdict"], "unadjudicable")
        self.assertIn("nothing", " ".join(got["why"]))
        us = [unit(ticket_=k, q=(S, P)) for k in range(10)]          # acc_q − acc_t < 0
        self.assertEqual(score.adjudicate(spec("RR-d"), us)["verdict"], "unadjudicable")
        for row in ("RR-b", "RR-c"):
            with self.subTest(row):
                self.assertNotEqual(score.adjudicate(spec(row), us)["verdict"],
                                    "unadjudicable")

    def test_a_row_with_too_many_invalid_answers_has_no_value(self):
        us = [unit(ticket_=k, w=(None, S) if k < 6 else (S, S)) for k in range(100)]
        self.assertEqual(score.adjudicate(spec("RR-c"), us)["verdict"], "unadjudicable")
        us = [unit(ticket_=k, w=(None, S) if k < 5 else (S, S)) for k in range(100)]
        self.assertNotEqual(score.adjudicate(spec("RR-c"), us)["verdict"], "unadjudicable")
        us = [unit(ticket_=k, t=(P, P), r=(None, S) if k < 6 else (S, S)) for k in range(100)]
        self.assertEqual(score.adjudicate(spec("RR-d"), us)["verdict"], "unadjudicable")
        self.assertNotEqual(score.adjudicate(spec("RR-b"), us)["verdict"], "unadjudicable")

    def test_thin_by_the_error_and_by_one_run(self):
        us = ([unit(run=1, ticket_=k, w=(S, S), t=(P, P)) for k in range(5)]
              + [unit(run=2, ticket_=10 + k, w=(P, P), t=(P, P)) for k in range(20)])
        got = score.adjudicate(spec("RR-b"), us)
        self.assertEqual(got["verdict"], "holds")
        self.assertTrue(got["thin"])
        self.assertEqual(got["thin_because"]["dropping_one_run_flips"], ["L3r1"])
        us = ([unit(run=1, ticket_=k, t=(P, P)) for k in range(5)]
              + [unit(run=2, ticket_=10 + k, t=(P, P), w=(P, P)) for k in range(4)]
              + [unit(run=3, ticket_=20 + k, t=(P, P)) for k in range(20)])
        got = score.adjudicate(spec("RR-d"), us)
        self.assertEqual(got["verdict"], "holds")
        self.assertEqual(got["thin_because"]["dropping_one_run_flips"], [])


class TestTheAnchorByHand(unittest.TestCase):

    def test_its_term_is_plan_queue_alones(self):
        p = qscore.Prompt(id="t:L3:1", ticket=1, today=(Y, Y), before=(Y, W))
        self.assertEqual(qscore.anchor_term(p), 1 - F(2, 4))

    def test_it_reads_the_rule_arm_and_plan_queue_alones_answers_from_the_pinned_provider(self):
        d = population.build()
        a = d.asks_of("t")[0]
        design = SimpleNamespace(asks_of=lambda arm: [a] if arm == "t" else [])
        today = {k: {a.id: {"action": Y, "served_by": plan.PROVIDER_NAME}} for k in (1, 2)}
        before = {1: {a.id: {"action": Y, "served_by": plan.PROVIDER_NAME}},
                  2: {a.id: {"action": W, "served_by": "Relace"}}}
        (p,) = score.anchor_prompts(design, today, before)
        self.assertEqual((p.id, p.today, p.before), (a.id, (Y, Y), (Y,)))

    def test_it_needs_a_hundred_prompts_and_is_thin_only_by_its_error(self):
        few = [qscore.Prompt(id=f"t:L3:{k}", ticket=k, today=(Y, Y), before=(Y,))
               for k in range(99)]
        self.assertEqual(score.adjudicate_anchor(few)["verdict"], "unadjudicable")
        enough = few + [qscore.Prompt(id="t:L3:99", ticket=99, today=(Y, Y), before=(Y,))]
        got = score.adjudicate_anchor(enough)
        self.assertEqual((got["id"], got["verdict"], got["thin"]), ("RR-a", "holds", False))
        self.assertNotIn("dropping_one_run_flips", got["thin_because"])


class TestStageCEndToEnd(unittest.TestCase):
    """Stage C over synthetic passes of every prompt, and synthetic answers of
    the closed plans': the structure, never a figure. The rules a ticket
    matches are stubbed, so that no real ticket is read against the list
    before the signature."""

    def test_score_runs_over_the_whole_design(self):
        d = population.build()
        lab = ascore.labels()
        catch_all = qrules.parse("H29: SI severity gte 1 ENTONCES T1_GENERAL\n")
        payload = {"action": Y, "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                   "beats": ["H29"], "loses_to": [], "note": "x"}

        def rows(k):
            return {"rows": [{"id": i, "arm": a.arm, "action": Y,
                              "served_by": plan.PROVIDER_NAME, "failure": None,
                              "attempts": 1, "retries": [], "seconds": 1.0,
                              "payload": payload if a.arm in ("t", "w") else {"action": Y},
                              "keys": list(payload) if a.arm in ("t", "w") else ["action"],
                              "reasoning": "x" if a.arm in ("w", "r") else None,
                              "call_attempts": [{"provider": plan.PROVIDER_NAME,
                                                 "finish_reason": "stop",
                                                 "completion_tokens": 40,
                                                 "reasoning_tokens": (9 if a.arm in ("w", "r")
                                                                      else 0)}]}
                             for i, a in d.asks.items()]}
        qa = {k: {a.id: {"id": a.id, "action": W, "served_by": plan.PROVIDER_NAME}
                  for a in d.asks_of("t")} for k in (1, 2)}
        fm = {k: {a.id: {"id": a.id, "action": Y, "served_by": plan.PROVIDER_NAME}
                  for arm in ("q", "r") for a in d.asks_of(arm)} for k in (1, 2)}
        with mock.patch.object(qrules, "matching",
                               side_effect=lambda t, rs=None: list(catch_all)), \
             mock.patch.object(qrules, "rules", return_value=catch_all):
            out = score.score(d, {"pass1": rows(1), "pass2": rows(2)}, lab, qa, fm)
        self.assertEqual(list(out["verdicts"]), ["RR-a", "RR-b", "RR-c", "RR-d"])
        for rid, v in out["verdicts"].items():
            with self.subTest(rid):
                self.assertIn(v["verdict"], ("holds", "refuted", "unadjudicable"))
        self.assertEqual(out["verdicts"]["RR-a"]["read"], 171)
        self.assertEqual(out["verdicts"]["RR-b"]["decisions"], 320)
        self.assertEqual(set(out["RR-e"]), {"accuracy", "where_errors_go", "by_governing_rule",
                                            "by_true_queue", "agreement", "beside",
                                            "rules_written", "the_calls"})
        written = out["RR-e"]["rules_written"]
        self.assertEqual(set(written), {"t", "w"})
        self.assertEqual((written["w"]["answers"], written["w"]["validates"],
                          written["w"]["all_right"], written["w"]["action_written_first"]),
                         (342, 342, 342, 342))
        self.assertEqual((written["t"]["same_region_as_a_listed_rule"],
                          written["t"]["cites_identifiers"]), (342, 342))
        calls = out["RR-e"]["the_calls"]["pass1"]
        self.assertEqual(calls["reasoning"], {"recorded": 342, "coded": False})
        self.assertEqual(calls["reasoning_tokens"]["w"]["median"], 9)
        self.assertEqual(set(out["RR-e"]["beside"]),
                         {"queue_alone_rule_arm", "first_match_plain_arm",
                          "first_match_reasoning_arm"})


if __name__ == "__main__":
    unittest.main()
