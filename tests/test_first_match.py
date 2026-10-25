"""
PLAN_FIRST_MATCH.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the client and the pin are
    `PLAN_QUEUE_ALONE.md`'s, imported rather than retyped (rule A), and that
    each arm's reasoning setting and budget are §1's.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `first_match/ask.py` exits before it builds a client.
  * The design: `PLAN_QUEUE_ALONE.md`'s plain prompts at level 3, three arms
    each, the plain arm's ids and digests that plan's, the reasoning arm's texts
    the plain arm's, what each prompt serves, the schedule, and nothing in the
    design that carries a label.
  * §5.1's text, verbatim, and the claim §5.1 makes about it: one line added to
    the answer, and nothing else that parts the naming arm from the plain one.
    The rule an answer's field names, as §0 defines it.
  * The requests, through the SDK double: every arm's carries the model, the
    temperature, the pin and `response_format` first, with its own reasoning
    setting and budget; the plain arm's is `PLAN_QUEUE_ALONE.md`'s plain arm's,
    request for request. A failed call is retried with the same messages after
    a wait, and a failed parse with v1's message (rule H).
  * Stage B end to end through the double: the attempts, the provider, the
    reasoning and the keys' order kept, an answer from another provider
    invalid, a session resumed, an outage stopping without recording, the
    turns, and the smoke check's pin, reasoning and named rules.
  * Stage C by hand: every term of §0, the named rules' classes, `FM-c`'s share
    and its conditions, the anchor, every reason a row has no value, *thin*
    both ways, and the whole stage over synthetic passes.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double, or something that fails the test if it is ever built. Every record
a test writes lands in a temporary directory that `plan.OUT` is pointed at.
**No figure of the plan is computed, and no reference Stage A computes after
the signature**: the only answers ever scored are the double's or synthetic
ones, and the rules a ticket matches are read on tickets built by hand, or
stubbed where the whole design is scored.
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

from apply import score as ascore
from queue_alone import ask as qask
from queue_alone import plan as qa_plan
from queue_alone import population as qpop
from queue_alone import prompts as qprompts
from queue_alone import rules as qrules
from queue_alone import score as qscore
from rung2.proposers2 import ProposalError

from first_match import ask, gates, plan, population, prompts, sample, score
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


def answer_json(action: str = P, rule: str | None = None) -> str:
    return json.dumps({"rule": rule, "action": action} if rule else {"action": action})


def by_arm(kwargs: dict) -> str:
    """The double's answer: a rule and a queue to the naming arm, a queue to the
    others."""
    system = kwargs["messages"][0]["content"]
    return answer_json(rule="H03") if prompts.NAMING_LINE in system else answer_json()


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


def small(design: population.Design, k: int = 9) -> population.Design:
    """The design with each pass cut to the first `k` prompts of pass 1's order,
    so that a test asks a few prompts of each arm and not 513."""
    head = design.sessions["pass1"][:k]
    return dataclasses.replace(design, sessions={"smoke": design.sessions["smoke"],
                                                 "pass1": head,
                                                 "pass2": list(reversed(head))})


def ticket(**kw) -> dict:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return {**base, **kw}


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_queue_alones(self):
        self.assertEqual(plan.MODEL, qa_plan.MODEL)
        self.assertEqual(plan.MODEL, "deepseek/deepseek-v4-flash")
        self.assertIs(plan.REASONING_OFF, qa_plan.REASONING)
        self.assertEqual(plan.REASONING_OFF, {"effort": "none"})
        self.assertEqual((plan.PROMPT, plan.TEMPERATURE), ("v1", 0))
        self.assertEqual((plan.MAX_TOKENS, plan.MAX_RETRIES), (1200, 2))
        self.assertEqual(plan.MAX_TOKENS, qa_plan.MAX_TOKENS)
        self.assertEqual(plan.CALL_RETRY_WAIT, (10, 30))

    def test_the_reasoning_arm_is_section_2_2s(self):
        self.assertEqual(plan.REASONING_ON, {"effort": "high"})
        self.assertEqual(plan.MAX_TOKENS_REASONING, 16000)
        from manual import plan as manual_plan
        self.assertEqual(plan.MAX_TOKENS_REASONING, manual_plan.COMPILE_MAX_TOKENS)
        self.assertEqual(plan.settings("r"), {"reasoning": {"effort": "high"},
                                              "max_tokens": 16000})
        for arm in ("q", "n"):
            with self.subTest(arm):
                self.assertEqual(plan.settings(arm), {"reasoning": {"effort": "none"},
                                                      "max_tokens": 1200})
        plan.settings("r")["reasoning"]["effort"] = "low"
        self.assertEqual(plan.REASONING_ON, {"effort": "high"})
        with self.assertRaises(ValueError):
            plan.settings("t")

    def test_the_pin_is_plan_queue_alones(self):
        self.assertEqual(plan.PROVIDER, {"order": ["baidu"], "allow_fallbacks": False})
        self.assertIs(plan.PROVIDER, qa_plan.PROVIDER)
        self.assertEqual(plan.PROVIDER_NAME, "Baidu")

    def test_the_inputs_and_the_population(self):
        self.assertEqual((plan.LEVEL, plan.REPS, plan.N, plan.SEED), (3, 3, 2000, 17))
        self.assertEqual((plan.TICKET_PROMPTS, plan.DECISIONS), (171, 320))
        self.assertEqual(plan.TICKET_PROMPTS, qa_plan.TICKET_PROMPTS[3])
        self.assertEqual(plan.DECISIONS, qa_plan.DECISIONS[3])
        self.assertEqual(plan.queue_alone_sample(), Path("results_queue_alone/sample.json"))
        self.assertEqual(plan.queue_alone_ask("pass2"),
                         Path("results_queue_alone/ask_pass2.json"))
        self.assertEqual(plan.queue_alone_score(), Path("results_queue_alone/score.json"))
        self.assertEqual(plan.queue_alone_orders(), Path("results_queue_alone/orders.json"))

    def test_the_sessions_and_the_limits(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "pass1", "pass2"))
        self.assertEqual((plan.PASSES, plan.SMOKE_PER_ARM), (2, 2))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MAX_CONSECUTIVE_FAILURES,
                          plan.MIN_ANCHOR_PROMPTS, plan.MIN_NAMED_ORDER_ERRORS),
                         (1, 5, 100, 20))
        self.assertEqual((plan.MAX_INVALID_SHARE, plan.MAX_UNNAMED_SHARE),
                         (F(1, 20), F(1, 20)))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 73)
        self.assertNotIn(plan.ORDER_SEED,
                         {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61, 67, 71})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_lines_are_section_0s_as_fractions(self):
        lines = {"FM_A_MAX_GAP": F(1, 20), "FM_B_LINE": F(0), "FM_C_LINE": F(1, 2),
                 "FM_D_LINE": F(0), "FM_E_LINE": F(9, 10), "FM_F_LINE": F(0)}
        for name, value in lines.items():
            with self.subTest(name):
                self.assertIsInstance(getattr(plan, name), Fraction)
                self.assertEqual(getattr(plan, name), value)

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_FIRST_MATCH.md").read_text()
        for needle in ("`ORDER_SEED = 73`", "`TICKET_PROMPTS = 171`", "`DECISIONS = 320`",
                       '`REASONING_ON = {"effort": "high"}`',
                       "`MAX_TOKENS_REASONING = 16000`", "`CALL_RETRY_WAIT = (10, 30)`",
                       '`ARMS = ("q", "n", "r")`', "`SMOKE_PER_ARM = 2`",
                       "`FM_C_LINE = Fraction(1, 2)`", "`FM_E_LINE = Fraction(9, 10)`",
                       "`MIN_NAMED_ORDER_ERRORS = 20`", "`MIN_ANCHOR_PROMPTS = 100`"):
            with self.subTest(needle):
                self.assertIn(needle, text)

    def test_the_gate_reads_this_plan_and_the_records_land_in_their_directory(self):
        self.assertEqual(plan.PLAN, Path("PLAN_FIRST_MATCH.md"))
        self.assertEqual(plan.ask_path("pass1"), Path("results_first_match/ask_pass1.json"))
        self.assertEqual(plan.partial_path("smoke"),
                         Path("results_first_match/ask_smoke.partial.jsonl"))
        self.assertEqual((plan.sample_path(), plan.score_path()),
                         (Path("results_first_match/sample.json"),
                          Path("results_first_match/score.json")))
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
        self.assertEqual(plan.gate_signature(REPO / "PLAN_FIRST_MATCH.md")["found"],
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

class TestTheDesignIsPlanQueueAlonesLevel3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.d = population.build()
        cls.qa = qpop.build()

    def test_three_arms_on_every_level_3_ticket(self):
        self.assertEqual(prompts.ARMS, ("q", "n", "r"))
        for arm in prompts.ARMS:
            with self.subTest(arm):
                self.assertEqual(len(self.d.asks_of(arm)), plan.TICKET_PROMPTS)
        self.assertEqual(len(self.d.asks), 3 * 171)
        self.assertEqual(len(self.d.decisions), plan.DECISIONS)
        self.assertEqual({e.level for e in self.d.decisions.values()}, {3})

    def test_the_plain_arm_is_plan_queue_alones(self):
        theirs = {i: a for i, a in self.qa.asks.items()
                  if a.arm == qprompts.PLAIN and a.level == 3}
        mine = {i: a for i, a in self.d.asks.items() if a.arm == prompts.PLAIN}
        self.assertEqual(set(mine), set(theirs))
        for i in sorted(mine)[::20]:
            with self.subTest(i):
                self.assertEqual((mine[i].system, mine[i].user, mine[i].digest),
                                 (theirs[i].system, theirs[i].user, theirs[i].digest))

    def test_the_reasoning_arm_is_the_plain_arm_text_for_text(self):
        for a in self.d.asks_of(prompts.REASONING)[::20]:
            q = self.d.asks[prompts.ask_id(prompts.PLAIN, a.ticket)]
            with self.subTest(a.id):
                self.assertEqual((a.system, a.user, a.digest), (q.system, q.user, q.digest))
                self.assertEqual(a.messages(), q.messages())

    def test_each_prompt_serves_what_the_plain_prompt_served(self):
        for i, a in list(self.d.asks.items())[::17]:
            qid = qprompts.ask_id(qprompts.PLAIN, 3, a.ticket)
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
                         ["n", "n", "q", "q", "r", "r"])
        for s in ("pass1", "pass2"):
            self.assertEqual(sorted(self.d.sessions[s]), sorted(self.d.asks))
        self.assertNotEqual(self.d.sessions["pass1"], self.d.sessions["pass2"])

    def test_the_four_gates_pass_without_the_suite(self):
        checks = gates.run_checks(suite=False)
        self.assertTrue(checks.g1["passes"], checks.g1)
        self.assertTrue(checks.g2["passes"], checks.g2)
        self.assertTrue(checks.g3["passes"], checks.g3)
        self.assertTrue(checks.blocking_pass)

    def test_the_checks_drop_every_float(self):
        self.assertEqual(gates.exact({"v": {"fraction": "1/3", "value": 1 / 3}, "se": 0.1,
                                      "n": 3, "xs": [0.5, {"fraction": "1/2", "value": 0.5}]}),
                         {"v": "1/3", "n": 3, "xs": ["1/2"]})


# ---------------------------------------------------------------------------
# The texts
# ---------------------------------------------------------------------------

class TestTheTextIsSection5_1s(unittest.TestCase):

    def test_the_line_and_the_answer_verbatim(self):
        self.assertEqual(prompts.NAMING_LINE,
                         '  "rule": "<identificador de la regla que se aplica a este ticket>",')
        self.assertEqual(prompts.NAMING_ANSWER,
                         "Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:"
                         "\n\n{\n"
                         '  "rule": "<identificador de la regla que se aplica a este ticket>",\n'
                         '  "action": "<accion para este ticket>"\n}')
        self.assertEqual(prompts.PLAIN_ANSWER, qprompts.ANSWER)
        plan_text = (REPO / "PLAN_FIRST_MATCH.md").read_text()
        self.assertIn("```\n" + prompts.NAMING_ANSWER + "\n```", plan_text)
        self.assertIn("```\n" + prompts.PLAIN_ANSWER + "\n```", plan_text)

    def test_the_naming_prompt_is_the_plain_one_with_the_line(self):
        plain, naming = prompts.system_prompt("q"), prompts.system_prompt("n")
        self.assertEqual(plain, qprompts.system_prompt(qprompts.PLAIN, 3))
        self.assertEqual(naming.replace(prompts.NAMING_LINE + "\n", "", 1), plain)
        self.assertEqual(len(naming.splitlines()), len(plain.splitlines()) + 1)
        self.assertEqual(gates.changed_lines(plain, naming),
                         [("insert", [], [prompts.NAMING_LINE])])
        self.assertEqual(prompts.system_prompt("r"), plain)
        self.assertIn(qprompts.v1_block(), naming)
        self.assertNotIn("primera regla", prompts.NAMING_ANSWER)

    def test_every_arm_sends_the_plain_arms_user_message(self):
        case = population.build().asks_of("q")[0].case
        self.assertEqual({prompts.user_message(arm, case) for arm in prompts.ARMS},
                         {qprompts.user_message(qprompts.PLAIN, case)})
        self.assertTrue(prompts.user_message("n", case).startswith("TICKET:\n"))

    def test_an_unknown_arm_is_refused(self):
        case = population.build().asks_of("q")[0].case
        for bad in ("t", "i", "z"):
            with self.subTest(bad):
                with self.assertRaises(ValueError):
                    prompts.system_prompt(bad)
                with self.assertRaises(ValueError):
                    prompts.user_message(bad, case)
                with self.assertRaises(ValueError):
                    prompts.ask(bad, 1, case)

    def test_the_rule_an_answer_names(self):
        cases = (("H03", "H03"), (" H03 ", "H03"), ("H03: SI has_security_keyword eq True",
                                                   "H03"),
                 ("H29", "H29"), ("H030", None), ("H30", None), ("H00", None),
                 ("h03", None), ("regla H03", None), ("", None), (None, None), (3, None))
        for field, expected in cases:
            with self.subTest(field=field):
                self.assertEqual(prompts.named_rule(field), expected)
        self.assertEqual(prompts.IDENTIFIERS, tuple(r.id for r in qrules.rules()))


# ---------------------------------------------------------------------------
# The requests, through the SDK double
# ---------------------------------------------------------------------------

class TestTheRequests(unittest.TestCase):

    def asked(self, a: prompts.Ask, client, sleep=None) -> tuple[dict, list[dict]]:
        with fake_sdk(openai=client):
            asker = ask.Asker(sleep=sleep or (lambda s: None))
            got = asker.ask(a)
        return got, client.peticiones

    def test_each_arm_sends_its_settings_with_the_pin(self):
        d = population.build()
        for arm in prompts.ARMS:
            a = d.asks_of(arm)[0]
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

    def test_the_plain_arm_is_plan_queue_alones_request(self):
        a = population.build().asks_of("q")[0]
        theirs_client = BaiduShaped(FixedResponses(answer_json()))
        with fake_sdk(openai=theirs_client):
            qask.Asker().ask(a)
        _, (mine,) = self.asked(a, BaiduShaped(FixedResponses(answer_json())))
        (theirs,) = theirs_client.peticiones
        self.assertEqual(mine, theirs)

    def test_the_reasoning_arm_differs_from_the_plain_one_in_its_settings_alone(self):
        d = population.build()
        q = d.asks_of("q")[0]
        r = d.asks[prompts.ask_id("r", q.ticket)]
        _, (rq,) = self.asked(q, BaiduShaped(FixedResponses(answer_json())))
        _, (rr,) = self.asked(r, BaiduShaped(FixedResponses(answer_json())))
        self.assertEqual({k: v for k, v in rq.items() if k not in ("max_tokens", "extra_body")},
                         {k: v for k, v in rr.items() if k not in ("max_tokens", "extra_body")})
        self.assertEqual(rr["extra_body"]["provider"], rq["extra_body"]["provider"])
        self.assertEqual((rr["max_tokens"], rr["extra_body"]["reasoning"]),
                         (16000, {"effort": "high"}))

    def test_the_answer_keeps_its_keys_in_order_and_the_reasoning(self):
        d = population.build()
        n = d.asks_of("n")[0]
        got, _ = self.asked(n, Reasons(by_arm))
        self.assertEqual((got["action"], got["payload"]["rule"], got["keys"]),
                         (P, "H03", ["rule", "action"]))
        self.assertIsNone(got["reasoning"])
        r = d.asks_of("r")[0]
        got, _ = self.asked(r, Reasons(by_arm))
        self.assertEqual(got["reasoning"], Reasons.REASONING)

    def test_a_failed_parse_is_retried_with_v1s_message(self):
        a = population.build().asks_of("q")[0]
        waits = []
        got, reqs = self.asked(a, BaiduShaped(FixedResponses("no es json", answer_json())),
                               sleep=waits.append)
        self.assertEqual(len(reqs), 2)
        self.assertNotIn("response_format", reqs[1])
        self.assertEqual(reqs[1]["messages"][-1],
                         {"role": "user", "content": prompts.RETRY_MSG})
        self.assertEqual(reqs[1]["extra_body"]["provider"], plan.PROVIDER)
        self.assertEqual((got["retries"], waits), (["parse"], []))

    def test_a_failed_call_is_retried_with_the_same_messages_after_a_wait(self):
        a = population.build().asks_of("r")[0]
        waits = []
        got, reqs = self.asked(a, BaiduShaped(Raises({1, 2}, answer_json())),
                               sleep=waits.append)
        self.assertEqual(len(reqs), 3)
        for req in reqs:
            self.assertEqual(req["messages"], a.messages())
            self.assertNotIn(prompts.RETRY_MSG, json.dumps(req["messages"]))
        self.assertEqual(got["retries"], ["call", "call"])
        self.assertEqual(waits, list(plan.CALL_RETRY_WAIT))
        self.assertEqual(got["action"], P)

    def test_a_call_then_a_parse_then_an_answer(self):
        a = population.build().asks_of("n")[0]
        n = {"calls": 0}

        def texts(kwargs):
            n["calls"] += 1
            if n["calls"] == 1:
                raise RuntimeError("Error code: 429 - temporarily rate-limited upstream")
            return "no es json" if n["calls"] == 2 else answer_json(rule="H02", action=S)
        waits = []
        got, reqs = self.asked(a, BaiduShaped(texts), sleep=waits.append)
        self.assertEqual(got["retries"], ["call", "parse"])
        self.assertEqual(waits, [plan.CALL_RETRY_WAIT[0]])
        self.assertEqual(reqs[1]["messages"], a.messages())
        self.assertEqual(reqs[2]["messages"][-1]["content"], prompts.RETRY_MSG)

    def test_every_attempt_failing_says_why_each_did(self):
        a = population.build().asks_of("q")[0]
        with fake_sdk(openai=BaiduShaped(Raises({1, 2, 3}, answer_json()))):
            asker = ask.Asker(sleep=lambda s: None)
            with self.assertRaises(ask.AskFailed) as caught:
                asker.ask(a)
        self.assertEqual(caught.exception.causes, ["call", "call", "call"])
        self.assertIsInstance(caught.exception, ProposalError)


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
        self.assertEqual({r["arm"] for r in rows}, set(prompts.ARMS))
        for r in rows:
            with self.subTest(r["id"]):
                self.assertTrue(r["valid"])
                self.assertEqual(r["served_by"], plan.PROVIDER_NAME)
                self.assertEqual(r["digest"], self.design.asks[r["id"]].digest)
                self.assertEqual(r["call_attempts"][-1]["provider"], plan.PROVIDER_NAME)
                self.assertEqual(r["retries"], [])
                self.assertFalse({"truth", "labels", "predicted", "y"} & set(r))
                if r["arm"] == "r":
                    self.assertEqual(r["reasoning"], Reasons.REASONING)
                    self.assertEqual(r["call_attempts"][-1]["reasoning_tokens"], 321)
                else:
                    self.assertIsNone(r["reasoning"])
                if r["arm"] == "n":
                    self.assertEqual(r["keys"], ["rule", "action"])

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
            self.assertEqual(len(rec["rows"]), 6)
            self.assertEqual(rec["provider"], plan.PROVIDER)
            self.assertEqual(rec["settings"]["r"], {"reasoning": {"effort": "high"},
                                                    "max_tokens": 16000})
            self.assertIn("_env", rec)
            ok, why = ask.previous_check("pass2")
            self.assertFalse(ok)
            self.assertIn("pass 1", why)
            self.assertTrue(ask.previous_check("pass1")[0])
            with self.assertRaises(SystemExit):
                ask.main(["--session", "pass2"])
            with self.assertRaises(SystemExit):           # a paid record is never overwritten
                ask.main(["--session", "smoke"])

    def test_the_smoke_check_wants_the_pin_the_reasoning_and_the_named_rules(self):
        def row(arm, rule="H03", tokens=None, finish="stop", reasoning=None, provider=None):
            return {"id": f"{arm}:L3:1", "arm": arm, "valid": True,
                    "payload": {"rule": rule, "action": P} if arm == "n" else {"action": P},
                    "reasoning": reasoning,
                    "call_attempts": [{"provider": provider or plan.PROVIDER_NAME,
                                       "finish_reason": finish,
                                       "reasoning_tokens": tokens}]}

        def check(rows):
            rec = {**json.loads(json.dumps(ask.protocol())), "rows": rows}
            plan.ask_path("smoke").write_text(json.dumps(rec))
            return ask.smoke_check()

        with TempOut():
            good = [row("q", tokens=0), row("n", tokens=0), row("r", tokens=321)]
            self.assertTrue(check(good)[0])
            self.assertTrue(check([row("q"), row("n"), row("r", reasoning="pienso")])[0])
            cases = {"did not reason": [row("q"), row("n"), row("r", tokens=0)],
                     "budget": [row("q"), row("n"), row("r", tokens=321, finish="length")],
                     "only the reasoning arm": [row("q", tokens=5), row("n"),
                                                row("r", tokens=321)],
                     "names no rule": [row("q"), row("n", rule="la tercera"),
                                       row("r", tokens=321)],
                     "Relace": [row("q"), row("n", provider="Relace"), row("r", tokens=321)],
                     "no valid answer": [row("q"), row("r", tokens=321)]}
            for why, rows in cases.items():
                with self.subTest(why):
                    ok, said = check(rows)
                    self.assertFalse(ok)
                    self.assertIn(why, said)
            rec = {**json.loads(json.dumps(ask.protocol())), "rows": good}
            rec["settings"]["r"]["reasoning"] = {"effort": "medium"}
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

    def test_reasoning_is_read_from_the_field_or_the_sdks_extras(self):
        self.assertEqual(ask.reasoning_of(SimpleNamespace(reasoning="x")), "x")
        self.assertEqual(ask.reasoning_of(SimpleNamespace(reasoning=None,
                                                          model_extra={"reasoning": "y"})), "y")
        self.assertIsNone(ask.reasoning_of(SimpleNamespace(reasoning="")))
        self.assertIsNone(ask.reasoning_of(SimpleNamespace()))


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
        asks = {"q:L3:1": SimpleNamespace(id="q:L3:1", arm="q")}
        design = SimpleNamespace(decisions=decisions,
                                 asks_of=lambda arm: [a for a in asks.values() if a.arm == arm])
        before = {1: {"q:L3:1": {"action": "A_Q", "served_by": "Baidu"}}, 2: {}}
        with mock.patch.object(qrules, "rules", return_value=rs):
            got = sample.references(design, before)
        self.assertEqual(got["matches"]["L3r1:1"], {"ticket": 1,
                                                    "matching": ["H01", "H02", "H03"],
                                                    "runner_up": "H02"})
        self.assertEqual(got["matches"]["L3r1:2"], {"ticket": 2, "matching": ["H02", "H03"],
                                                    "runner_up": "H03"})
        self.assertEqual(got["queue_alone_plain"]["q:L3:1"],
                         [{"pass": 1, "action": "A_Q", "served_by": "Baidu"},
                          {"pass": 2, "action": None, "served_by": None}])


# ---------------------------------------------------------------------------
# Stage C by hand
# ---------------------------------------------------------------------------

HIT = ("H02", "H03", "H29")        # an exception, its general rule, the catch-all
QUEUES = (S, P, Y)


def unit(run=1, ticket_=1, y=S, q=(S, S), n=(S, S), rho=("H02", "H02"), r=(S, S),
         hit=HIT, queues=QUEUES, uid=None) -> score.Unit:
    return score.Unit(id=uid or f"L3r{run}:{ticket_}", run=run, ticket=ticket_, y=y,
                      hit=tuple(hit), queues=tuple(queues), q=tuple(q), n=tuple(n),
                      rho=tuple(rho), r=tuple(r))


def spec(row: str) -> score.Spec:
    return next(s for s in score.SPECS if s.id == row)


class TestTheTermsByHand(unittest.TestCase):

    def test_an_answer_is_valid_only_from_the_pinned_provider(self):
        row = {"action": P, "served_by": plan.PROVIDER_NAME}
        self.assertEqual(score.answer(row), P)
        self.assertIsNone(score.answer({**row, "served_by": "Relace"}))
        self.assertIsNone(score.answer({**row, "action": "NOT_A_QUEUE"}))
        self.assertIsNone(score.answer(None))

    def test_a_rule_is_named_only_by_a_valid_answer(self):
        row = {"action": P, "served_by": plan.PROVIDER_NAME, "payload": {"rule": "H03"}}
        self.assertEqual(score.named(row), "H03")
        self.assertIsNone(score.named({**row, "served_by": "Relace"}))
        self.assertIsNone(score.named({**row, "payload": {"rule": "la H03"}}))
        self.assertIsNone(score.named({**row, "payload": None}))

    def test_the_classes(self):
        u = unit()
        self.assertEqual([score.klass(a, u) for a in (S, P, Y, W)],
                         ["first", "order", "order", "matching"])
        self.assertEqual([score.rule_class(x, u) for x in ("H02", "H03", "H29", "H07", None)],
                         ["first", "lower", "lower", "unmatched", "none"])

    def test_the_units_from_rows(self):
        rs = qrules.parse(HAND)
        case = SimpleNamespace(as_dict=lambda: ticket(severity=1, product="api"))
        decisions = {"L3r2:5": SimpleNamespace(level=3, run=2, ticket=5,
                                               prompt=SimpleNamespace(case=case))}
        design = SimpleNamespace(decisions=decisions)
        ok = {"served_by": plan.PROVIDER_NAME}
        by_pass = {1: {"q:L3:5": {**ok, "action": W}, "n:L3:5": {**ok, "action": P,
                                                                 "payload": {"rule": "H02"}},
                       "r:L3:5": {**ok, "action": S}},
                   2: {"q:L3:5": {"action": W, "served_by": "Relace"},
                       "n:L3:5": {**ok, "action": P, "payload": {"rule": "dos"}}}}
        with mock.patch.object(qrules, "rules", return_value=rs):
            (u,) = score.units(design, by_pass, {"L3r2:5": {"y": "A_Q"}})
        self.assertEqual((u.run, u.ticket, u.y, u.hit, u.queues),
                         (2, 5, "A_Q", ("H01", "H02", "H03"), ("A_Q", "B_Q", "A_Q")))
        self.assertEqual((u.q, u.n, u.rho, u.r), ((W, None), (P, P), ("H02", None), (S, None)))

    def test_the_terms(self):
        u = unit(q=(P, S), n=(S, S), r=(S, Y))
        self.assertEqual(spec("FM-b").term(u), 1 - F(1, 2))
        self.assertEqual(spec("FM-d").term(u), F(1, 2) - F(1, 2))
        self.assertEqual(spec("FM-e").term(u), F(1, 2))
        self.assertEqual(spec("FM-f").term(u), F(1, 2) - 1)

    def test_the_clustered_error_is_plan_applys(self):
        self.assertIs(score.clustered_se, ascore.clustered_se)
        self.assertIs(score.hits, ascore.hits)
        self.assertIs(score.labels, ascore.labels)


def errors(lower: int, first: int, run: int = 1, start: int = 0) -> list[score.Unit]:
    """Decisions whose naming answers are order errors: `lower` answers naming
    the general rule below the exception, `first` naming the exception itself.
    Two answers a decision, one ticket each."""
    names = ["H03"] * lower + ["H02"] * first
    out = []
    for k in range(0, len(names), 2):
        chunk = names[k:k + 2]
        if len(chunk) == 2:
            out.append(unit(run=run, ticket_=start + k, n=(P, P), rho=tuple(chunk)))
        else:                       # the odd one out, beside a right answer
            out.append(unit(run=run, ticket_=start + k, n=(P, S), rho=(chunk[0], "H02")))
    return out


class TestTheVerdictsByHand(unittest.TestCase):

    def test_each_line_is_exact_at_its_edge(self):
        # FM-e at exactly 9/10: nine right of ten tickets holds.
        us = [unit(ticket_=k, r=(S, S) if k < 9 else (P, P)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("FM-e"), us)["verdict"], "holds")
        us[0] = unit(ticket_=0, r=(S, P))
        self.assertEqual(score.adjudicate(spec("FM-e"), us)["verdict"], "refuted")
        # FM-b, FM-d and FM-f at exactly 0 are refuted: their lines are held above.
        us = [unit(ticket_=k) for k in range(10)]
        for row in ("FM-b", "FM-d", "FM-f"):
            with self.subTest(row):
                self.assertEqual(score.adjudicate(spec(row), us)["verdict"], "refuted")
        us = [unit(ticket_=k, q=(P, P)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("FM-d"), us)["verdict"], "holds")

    def test_fm_c_at_its_edge(self):
        self.assertEqual(score.adjudicate_naming(errors(10, 10))["verdict"], "holds")
        self.assertEqual(score.adjudicate_naming(errors(9, 11))["verdict"], "refuted")
        got = score.adjudicate_naming(errors(14, 6))
        self.assertEqual((got["named_order_errors"], got["lower"], got["value"]["fraction"]),
                         (20, 14, "7/10"))

    def test_fm_c_reads_only_order_errors_that_name_a_rule(self):
        us = errors(12, 8)
        us += [unit(ticket_=100 + k, n=(S, S), rho=("H03", "H03")) for k in range(5)]
        us += [unit(ticket_=200, n=(W, P), rho=("H07", "H02"))]
        got = score.adjudicate_naming(us)
        self.assertEqual((got["named_order_errors"], got["lower"]), (21, 12))

    def test_fm_c_needs_twenty_named_order_errors(self):
        got = score.adjudicate_naming(errors(10, 9))
        self.assertEqual(got["verdict"], "unadjudicable")
        self.assertIn("fewer than 20", " ".join(got["why"]))

    def test_fm_c_has_no_value_when_too_many_answers_name_no_rule(self):
        base = errors(20, 10)                                   # 30 answers, 15 decisions
        right = [unit(ticket_=300 + k) for k in range(80)]      # 160 answers, all named
        unnamed = [unit(ticket_=500 + k, rho=(None, None)) for k in range(5)]
        got = score.adjudicate_naming(base + right + unnamed)   # 10 of 200 name none
        self.assertEqual(got["unnamed"], 10)
        self.assertNotEqual(got["verdict"], "unadjudicable")
        unnamed.append(unit(ticket_=600, rho=(None, "H02")))     # 11 of 202
        got = score.adjudicate_naming(base + right + unnamed)
        self.assertEqual(got["verdict"], "unadjudicable")

    def test_a_row_with_too_many_invalid_answers_has_no_value(self):
        us = [unit(ticket_=k, r=(None, S) if k < 6 else (S, S)) for k in range(100)]
        self.assertEqual(score.adjudicate(spec("FM-e"), us)["verdict"], "unadjudicable")
        us = [unit(ticket_=k, r=(None, S) if k < 5 else (S, S)) for k in range(100)]
        self.assertNotEqual(score.adjudicate(spec("FM-e"), us)["verdict"], "unadjudicable")
        us = errors(30, 0) + [unit(ticket_=900 + k, n=(None, S)) for k in range(2)]
        self.assertEqual(score.adjudicate_naming(us)["verdict"], "unadjudicable")

    def test_thin_by_the_error_and_by_one_run(self):
        us = ([unit(run=1, ticket_=k, n=(S, S), q=(P, P)) for k in range(5)]
              + [unit(run=2, ticket_=10 + k, n=(P, P), q=(P, P)) for k in range(20)])
        got = score.adjudicate(spec("FM-b"), us)
        self.assertEqual(got["verdict"], "holds")
        self.assertTrue(got["thin"])
        self.assertEqual(got["thin_because"]["dropping_one_run_flips"], ["L3r1"])
        us = errors(16, 0, run=1) + errors(6, 18, run=2, start=1000)
        got = score.adjudicate_naming(us)
        self.assertEqual(got["verdict"], "holds")
        self.assertEqual(got["thin_because"]["dropping_one_run_flips"], ["L3r1"])


class TestTheAnchorByHand(unittest.TestCase):

    def test_its_term_is_plan_queue_alones(self):
        p = qscore.Prompt(id="q:L3:1", ticket=1, today=(Y, Y), before=(Y, W))
        self.assertEqual(qscore.anchor_term(p), 1 - F(2, 4))

    def test_it_reads_plan_queue_alones_answers_from_the_pinned_provider(self):
        a = population.build().asks_of("q")[0]
        design = SimpleNamespace(asks_of=lambda arm: [a])
        today = {k: {a.id: {"action": Y, "served_by": plan.PROVIDER_NAME}} for k in (1, 2)}
        before = {1: {a.id: {"action": Y, "served_by": plan.PROVIDER_NAME}},
                  2: {a.id: {"action": W, "served_by": "Relace"}}}
        (p,) = score.anchor_prompts(design, today, before)
        self.assertEqual((p.today, p.before), ((Y, Y), (Y,)))

    def test_it_needs_a_hundred_prompts_and_is_thin_only_by_its_error(self):
        few = [qscore.Prompt(id=f"q:L3:{k}", ticket=k, today=(Y, Y), before=(Y,))
               for k in range(99)]
        self.assertEqual(score.adjudicate_anchor(few)["verdict"], "unadjudicable")
        enough = few + [qscore.Prompt(id="q:L3:99", ticket=99, today=(Y, Y), before=(Y,))]
        got = score.adjudicate_anchor(enough)
        self.assertEqual((got["id"], got["verdict"], got["thin"]), ("FM-a", "holds", False))
        self.assertNotIn("dropping_one_run_flips", got["thin_because"])


class TestStageCEndToEnd(unittest.TestCase):
    """Stage C over synthetic passes of every prompt, and synthetic answers of
    `PLAN_QUEUE_ALONE.md`'s: the structure, never a figure. The rules a ticket
    matches are stubbed, so that no real ticket is read against the list
    before the signature."""

    def test_score_runs_over_the_whole_design(self):
        d = population.build()
        lab = ascore.labels()
        catch_all = qrules.parse("H29: SI severity gte 1 ENTONCES T1_GENERAL\n")

        def rows(k):
            return {"rows": [{"id": i, "arm": a.arm, "action": Y,
                              "served_by": plan.PROVIDER_NAME, "failure": None,
                              "attempts": 1, "retries": [], "seconds": 1.0,
                              "payload": ({"rule": "H29", "action": Y} if a.arm == "n"
                                          else {"action": Y}),
                              "keys": ["rule", "action"] if a.arm == "n" else ["action"],
                              "reasoning": "x" if a.arm == "r" else None,
                              "call_attempts": [{"provider": plan.PROVIDER_NAME,
                                                 "finish_reason": "stop",
                                                 "reasoning_tokens": 9 if a.arm == "r" else 0}]}
                             for i, a in d.asks.items()]}
        before = {k: {a.id: {"id": a.id, "action": W, "served_by": plan.PROVIDER_NAME}
                      for a in d.asks_of("q")} for k in (1, 2)}
        with mock.patch.object(qrules, "matching", side_effect=lambda t, rs=None: list(catch_all)), \
             mock.patch.object(qrules, "rules", return_value=catch_all):
            out = score.score(d, {"pass1": rows(1), "pass2": rows(2)}, lab, before)
        self.assertEqual(list(out["verdicts"]), ["FM-a", "FM-b", "FM-c", "FM-d", "FM-e", "FM-f"])
        for rid, v in out["verdicts"].items():
            with self.subTest(rid):
                self.assertIn(v["verdict"], ("holds", "refuted", "unadjudicable"))
        self.assertEqual(out["verdicts"]["FM-a"]["read"], 171)
        self.assertEqual(out["verdicts"]["FM-b"]["decisions"], 320)
        self.assertEqual(set(out["FM-g"]), {"accuracy", "where_errors_go", "naming", "paired",
                                            "by_governing_rule", "by_true_queue", "agreement",
                                            "queue_alone_beside", "the_calls"})
        calls = out["FM-g"]["the_calls"]["pass1"]
        self.assertEqual(calls["reasoning"], {"recorded": 171, "coded": False})
        self.assertEqual(out["FM-g"]["naming"]["rule_written_first"], 342)


if __name__ == "__main__":
    unittest.main()
