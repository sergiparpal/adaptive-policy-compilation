"""
PLAN_QUEUE_ALONE.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the client is `PLAN_MANUAL.md`'s loop
    proposer, imported rather than retyped (rule A), and that the pin is §2.3's.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `queue_alone/ask.py` exits before it builds a client.
  * The design: `PLAN_APPLY.md`'s ticket prompts, three arms each, the rule
    arm's ids and digests that plan's, what each prompt serves, the schedule,
    and nothing in the design that carries a label.
  * §5.1's texts, verbatim, and the claims §5.1 makes about them: v1's block cut
    from v1, the two sentences and the one line that part the plain arm from
    the impasse arm, the empty-base line that parts the impasse arm from the
    rule arm, the manual's block at levels 1 to 3 and only there.
  * The requests, through the SDK double: each arm's is the proposer's own,
    with the pin added and nothing else changed; the retry is v1's.
  * Stage B end to end through the double: the attempts and the provider kept,
    an answer from another provider invalid, a session resumed, an outage
    stopping without recording, the turns and the smoke check's pin.
  * The 29 rules read from text, and §5.6's classes, on tickets built by hand.
  * Stage C by hand: every term of §0, the share and its comparison, the
    anchor, every reason a row has no value, *thin* both ways, and the whole
    stage over synthetic passes.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double, or something that fails the test if it is ever built. Every record
a test writes lands in a temporary directory that `plan.OUT` is pointed at.
**No figure of the plan is computed, and no reference Stage A computes after
the signature**: the only answers ever scored are the double's or synthetic
ones, and §5.6's classes are read on tickets built by hand.
"""

from __future__ import annotations

import dataclasses
import inspect
import json
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import ACTIONS, DOMAINS
from manual import plan as manual_plan
from manual import prompts as mprompts
from manual.run import build_proposer
from rung2.proposers2 import SYSTEM_PROMPT_V1, OpenRouterProposer2, ProposalError

from apply import population as apop
from apply import prompts as aprompts
from apply import score as ascore
from queue_alone import ask, gates, plan, population, prompts, rules, sample, score
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
F = Fraction


class BaiduShaped(OpenRouterShapedClient):
    """The double, served by the provider the plan pins."""
    PROVIDER = plan.PROVIDER_NAME


def answer_json(action: str = "T2_TECHNICAL") -> str:
    return json.dumps({"action": action,
                       "conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                       "beats": [], "loses_to": [], "note": "una nota"})


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
    so that a test asks a few prompts of each arm and not 2,028."""
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
        self.assertEqual((plan.MAX_TOKENS, plan.MAX_RETRIES), (1200, 2))
        default = inspect.signature(OpenRouterProposer2.__init__).parameters["max_retries"]
        self.assertEqual(default.default, plan.MAX_RETRIES)

    def test_the_pin_is_section_2_3s(self):
        self.assertEqual(plan.PROVIDER, {"order": ["baidu"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, "Baidu")

    def test_the_inputs_and_the_populations(self):
        self.assertEqual((plan.LEVELS, plan.REPS, plan.N, plan.SEED),
                         ((0, 1, 2, 3), 3, 2000, 17))
        self.assertEqual(plan.TICKET_PROMPTS, {0: 275, 1: 81, 2: 149, 3: 171})
        self.assertEqual(plan.DECISIONS, {0: 116, 1: 100, 2: 242, 3: 320})
        self.assertEqual(sum(plan.TICKET_PROMPTS.values()), 676)
        self.assertEqual(plan.apply_sample(), Path("results_apply/sample.json"))
        self.assertEqual(plan.apply_ask("pass2"), Path("results_apply/ask_pass2.json"))
        self.assertEqual(plan.apply_score(), Path("results_apply/score.json"))

    def test_the_sessions_and_the_limits(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "pass1", "pass2"))
        self.assertEqual((plan.PASSES, plan.SMOKE_PER_ARM_AND_LEVEL), (2, 1))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MAX_CONSECUTIVE_FAILURES,
                          plan.MIN_ANCHOR_PROMPTS), (1, 5, 100))
        self.assertEqual(plan.MAX_INVALID_SHARE, F(1, 20))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 71)
        self.assertNotIn(plan.ORDER_SEED,
                         {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61, 67})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_lines_are_section_0s_as_fractions(self):
        lines = {"QA_A_MAX_GAP": F(1, 20), "QA_B_LINE": F(0), "QA_C_LINE": F(1, 2),
                 "QA_D_LINE": F(0), "QA_E_LINE": F(9, 10), "QA_F_LINE": F(0)}
        for name, value in lines.items():
            with self.subTest(name):
                self.assertIsInstance(getattr(plan, name), Fraction)
                self.assertEqual(getattr(plan, name), value)

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_QUEUE_ALONE.md").read_text()
        for needle in ("`ORDER_SEED = 71`", "`TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}`",
                       "`DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}`",
                       '`PROVIDER = {"order": ["baidu"], "allow_fallbacks": False}`',
                       "`QA_C_LINE = Fraction(1, 2)`", "`QA_E_LINE = Fraction(9, 10)`",
                       "`MIN_ANCHOR_PROMPTS = 100`"):
            with self.subTest(needle):
                self.assertIn(needle, text)

    def test_the_gate_reads_this_plan_and_the_records_land_in_their_directory(self):
        self.assertEqual(plan.PLAN, Path("PLAN_QUEUE_ALONE.md"))
        self.assertEqual(plan.ask_path("pass1"), Path("results_queue_alone/ask_pass1.json"))
        self.assertEqual(plan.partial_path("smoke"),
                         Path("results_queue_alone/ask_smoke.partial.jsonl"))
        self.assertEqual((plan.sample_path(), plan.score_path()),
                         (Path("results_queue_alone/sample.json"),
                          Path("results_queue_alone/score.json")))
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
        as one of `PLAN_APPLY.md`'s did on 2026-10-23."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_QUEUE_ALONE.md")["found"],
                         plan.MIN_SIGNATURES)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch.object(ask, "Asker",
                               side_effect=AssertionError("asker built")) as asker, \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        for m in (checks, proposer, asker, fetch, write):
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
             mock.patch.object(ask, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        for m in (fetch, proposer, write):
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

class TestTheDesignIsPlanApplysTickets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.d = population.build()
        cls.a = apop.build()

    def test_three_arms_on_every_ticket_prompt(self):
        for arm in prompts.ARMS:
            for lv in plan.LEVELS:
                with self.subTest(arm=arm, level=lv):
                    self.assertEqual(len(self.d.asks_of(arm, lv)), plan.TICKET_PROMPTS[lv])
        self.assertEqual(len(self.d.asks), 3 * 676)
        self.assertEqual(prompts.ARMS, ("t", "i", "q"))

    def test_the_rule_arm_is_plan_applys_ticket_arm(self):
        theirs = {i: a for i, a in self.a.asks.items() if a.arm == aprompts.TICKET}
        mine = {i: a for i, a in self.d.asks.items() if a.arm == prompts.RULE}
        self.assertEqual(set(mine), set(theirs))
        for i in sorted(mine)[::40]:
            with self.subTest(i):
                self.assertEqual((mine[i].system, mine[i].user, mine[i].digest),
                                 (theirs[i].system, theirs[i].user, theirs[i].digest))

    def test_each_prompt_serves_what_plan_applys_served(self):
        for i, a in list(self.d.asks.items())[::25]:
            rid = prompts.ask_id(prompts.RULE, a.level, a.ticket)
            with self.subTest(i):
                self.assertEqual(self.d.serves[i], {"own": self.a.serves[rid]["t"],
                                                    "zero": self.a.serves[rid]["u"]})

    def test_nothing_in_the_design_carries_a_label(self):
        text = json.dumps(self.d.summary())
        for word in ("truth", "predicted", "correct", '"y"', "loop"):
            with self.subTest(word):
                self.assertNotIn(word, text)

    def test_the_schedule(self):
        self.assertEqual(population.sessions_for(self.d.asks), self.d.sessions)
        smoke = self.d.sessions["smoke"]
        self.assertEqual(len(smoke), 12)
        self.assertEqual({(self.d.asks[i].arm, self.d.asks[i].level) for i in smoke},
                         {(arm, lv) for arm in prompts.ARMS for lv in plan.LEVELS})
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
# The texts
# ---------------------------------------------------------------------------

class TestTheTextsAreSection5_1s(unittest.TestCase):

    def test_the_new_sentences_verbatim(self):
        self.assertEqual(prompts.PLAIN_HEAD,
                         "Eres el componente de enrutamiento de un sistema de triaje de "
                         "tickets.\n\nTu tarea: decidir la cola de destino correcta para "
                         "ESTE ticket.")
        self.assertEqual(prompts.IMPASSE_HEAD,
                         "Eres el componente de excepcion de un sistema de triaje de "
                         "tickets.\n\nEl motor simbolico no ha podido decidir este ticket. "
                         "Tu tarea: decidir la cola de destino correcta para ESTE ticket.")
        self.assertEqual(prompts.ANSWER,
                         'Responde UNICAMENTE con un objeto JSON, sin markdown, sin '
                         'preambulo:\n\n{\n  "action": "<accion para este ticket>"\n}')
        self.assertEqual((prompts.PLAIN_HEADER, prompts.IMPASSE_HEADER),
                         ("TICKET:\n", "TICKET EN IMPASSE:\n"))
        self.assertEqual(prompts.RETRY_MSG, mprompts.RETRY_MSG)

    def test_the_task_is_v1s_first_item(self):
        self.assertIn("Decidir la cola de destino correcta para ESTE ticket.",
                      SYSTEM_PROMPT_V1)

    def test_v1s_block_is_cut_from_v1_and_is_its_rendering(self):
        block = prompts.v1_block()
        self.assertEqual(SYSTEM_PROMPT_V1.count(block), 1)
        self.assertEqual(block,
                         f"ATRIBUTOS DISPONIBLES Y SUS DOMINIOS:\n"
                         f"{json.dumps(DOMAINS, indent=2, default=str)}\n\n"
                         f"severity: 1 = critica, 4 = baja.\n\nACCIONES POSIBLES:\n"
                         f"{json.dumps(ACTIONS, indent=2)}")

    def test_the_plain_prompt_whole_at_level_0(self):
        self.assertEqual(prompts.system_prompt(prompts.PLAIN, 0),
                         prompts.PLAIN_HEAD + "\n\n" + prompts.v1_block() + "\n\n"
                         + prompts.ANSWER)

    def test_the_manual_at_levels_1_to_3_and_only_there(self):
        for lv in plan.LEVELS:
            for arm in (prompts.PLAIN, prompts.IMPASSE):
                text = prompts.system_prompt(arm, lv)
                with self.subTest(arm=arm, level=lv):
                    if lv:
                        self.assertEqual(text.count(mprompts.block(lv)), 1)
                        self.assertLess(text.index("ACCIONES POSIBLES"),
                                        text.index(mprompts.MANUAL_HEADER))
                    else:
                        self.assertNotIn(mprompts.MANUAL_HEADER, text)

    def test_plain_and_impasse_differ_in_two_sentences_and_a_line(self):
        case = population.build().asks[next(iter(population.build().asks))].case
        for lv in plan.LEVELS:
            q, i = (prompts.system_prompt(a, lv) for a in (prompts.PLAIN, prompts.IMPASSE))
            with self.subTest(level=lv):
                self.assertEqual(gates.changed_lines(q, i), [0, 2])
                self.assertEqual(q.replace(prompts.PLAIN_HEAD, prompts.IMPASSE_HEAD), i)
        q, i = (prompts.user_message(a, case) for a in (prompts.PLAIN, prompts.IMPASSE))
        self.assertEqual(gates.changed_lines(q, i), [0])

    def test_the_rule_arms_message_is_the_impasse_arms_under_the_empty_base(self):
        case = population.build().asks[next(iter(population.build().asks))].case
        self.assertEqual(prompts.user_message(prompts.RULE, case),
                         prompts.EMPTY_BASE + "\n"
                         + prompts.user_message(prompts.IMPASSE, case))
        self.assertEqual(prompts.EMPTY_BASE,
                         "BASE DE REGLAS: vacia. Esta es la primera regla.\n")

    def test_an_unknown_arm_is_refused(self):
        case = population.build().asks[next(iter(population.build().asks))].case
        for f, args in ((prompts.system_prompt, ("x", 0)),
                        (prompts.user_message, ("x", case)), (prompts.ask, ("x", 0, 1, case))):
            with self.subTest(f.__name__), self.assertRaises(ValueError):
                f(*args)


# ---------------------------------------------------------------------------
# The requests, through the double
# ---------------------------------------------------------------------------

class TestTheRequests(unittest.TestCase):

    def send(self, a: prompts.Ask, client) -> dict:
        with fake_sdk(openai=client):
            clients = ask.Clients()
            _, (action, _) = ask.answer(a, clients)
        self.assertEqual(action, "T2_TECHNICAL")
        return client.peticiones

    def test_each_arm_sends_the_proposers_request_with_the_pin(self):
        d = population.build()
        for lv in plan.LEVELS:
            for arm in prompts.ARMS:
                a = d.asks_of(arm, lv)[0]
                (req,) = self.send(a, BaiduShaped(FixedResponses(answer_json())))
                with self.subTest(level=lv, arm=arm):
                    self.assertEqual(req["model"], plan.MODEL)
                    self.assertEqual(req["temperature"], 0)
                    self.assertEqual(req["max_tokens"], 1200)
                    self.assertEqual(req["response_format"], {"type": "json_object"})
                    self.assertEqual(req["extra_body"], {"reasoning": plan.REASONING,
                                                         "provider": plan.PROVIDER})
                    self.assertEqual(req["messages"], a.messages())

    def test_the_rule_arm_is_the_unpinned_request_plus_the_pin(self):
        a = population.build().asks_of(prompts.RULE, 3)[0]
        unpinned = BaiduShaped(FixedResponses(answer_json()))
        with fake_sdk(openai=unpinned):
            build_proposer(3).propose(a.case, prompts.EMPTY_BASE)
        (pinned,) = self.send(a, BaiduShaped(FixedResponses(answer_json())))
        (plain,) = unpinned.peticiones
        self.assertEqual({k: v for k, v in pinned.items() if k != "extra_body"},
                         {k: v for k, v in plain.items() if k != "extra_body"})
        self.assertEqual(pinned["extra_body"], {**plain["extra_body"],
                                                "provider": plan.PROVIDER})

    def test_the_new_arms_send_what_the_rule_arm_sends_but_the_messages(self):
        d = population.build()
        reqs = {arm: self.send(d.asks_of(arm, 3)[0],
                               BaiduShaped(FixedResponses(answer_json())))[0]
                for arm in prompts.ARMS}
        for arm in (prompts.IMPASSE, prompts.PLAIN):
            with self.subTest(arm):
                self.assertEqual({k: v for k, v in reqs[arm].items() if k != "messages"},
                                 {k: v for k, v in reqs[prompts.RULE].items()
                                  if k != "messages"})

    def test_a_failed_parse_is_retried_with_v1s_message(self):
        a = population.build().asks_of(prompts.PLAIN, 3)[0]
        reqs = self.send(a, BaiduShaped(FixedResponses("no es json", answer_json())))
        self.assertEqual(len(reqs), 2)
        self.assertNotIn("response_format", reqs[1])
        self.assertEqual(reqs[1]["messages"][-1],
                         {"role": "user", "content": prompts.RETRY_MSG})
        self.assertEqual(reqs[1]["extra_body"]["provider"], plan.PROVIDER)

    def test_the_pin_leaves_the_callers_body_alone_and_wraps_once(self):
        inner = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
            create=lambda **kw: kw)))
        body = {"reasoning": {"effort": "none"}}
        got = ask.Pinned(inner)._create(model="m", extra_body=body)
        self.assertEqual(body, {"reasoning": {"effort": "none"}})
        self.assertEqual(got["extra_body"]["provider"], plan.PROVIDER)
        with fake_sdk(openai=BaiduShaped(FixedResponses(answer_json()))):
            p = ask.pin(build_proposer(0))
            self.assertIs(ask.pin(p)._client, p._client)
        with self.assertRaises(ValueError):
            ask.pin(SimpleNamespace(calls=None, _client=None))


# ---------------------------------------------------------------------------
# Stage B, through the double
# ---------------------------------------------------------------------------

class Failing:
    """A client that fails, as a dropped connection or a pinned provider down."""
    max_retries = 2
    system_prompt = ""

    def propose(self, case, base_text):
        raise ProposalError("sin objeto JSON: ''")

    def ask(self, a):
        raise ProposalError("sin objeto JSON: ''")


class TestStageB(unittest.TestCase):

    def setUp(self):
        self.design = small(population.build())

    def run_session(self, out: Path, session: str, clients=None, **kw):
        header = {"protocol": json.loads(json.dumps(ask.protocol())), "session": session,
                  "sample_sha256": "x"}
        return ask.ask(session, self.design, clients or ask.Clients(),
                       out / f"{session}.jsonl", header, **kw)

    def test_a_pass_keeps_the_attempts_the_provider_and_no_label(self):
        with tempfile.TemporaryDirectory() as d, \
             fake_sdk(openai=BaiduShaped(FixedResponses(answer_json()))), \
             mock.patch("builtins.print"):
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(resumed, [])
        self.assertEqual({r["arm"] for r in rows}, set(prompts.ARMS))
        for r in rows:
            self.assertTrue(r["valid"])
            self.assertEqual(r["served_by"], plan.PROVIDER_NAME)
            self.assertEqual(r["digest"], self.design.asks[r["id"]].digest)
            self.assertEqual(r["call_attempts"][-1]["provider"], plan.PROVIDER_NAME)
            self.assertFalse({"truth", "labels", "predicted", "y"} & set(r))

    def test_an_answer_from_another_provider_is_invalid(self):
        with tempfile.TemporaryDirectory() as d, \
             fake_sdk(openai=OpenRouterShapedClient(FixedResponses(answer_json()))), \
             mock.patch("builtins.print"):
            rows, _ = self.run_session(Path(d), "pass1")
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(r["action"], "T2_TECHNICAL")
            self.assertEqual(r["served_by"], OpenRouterShapedClient.PROVIDER)
            self.assertFalse(r["valid"])
            self.assertIsNone(score.answer(r))

    def test_an_interrupted_session_resumes_where_it_stopped(self):
        with tempfile.TemporaryDirectory() as d, \
             fake_sdk(openai=BaiduShaped(FixedResponses(answer_json()))), \
             mock.patch("builtins.print"):
            n = {"calls": 0}
            real = ask.answer

            def interrupting(a, clients):
                n["calls"] += 1
                if n["calls"] == 5:
                    raise KeyboardInterrupt
                return real(a, clients)

            with mock.patch.object(ask, "answer", side_effect=interrupting), \
                 self.assertRaises(KeyboardInterrupt):
                self.run_session(Path(d), "pass1")
            rows, resumed = self.run_session(Path(d), "pass1")
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(len(resumed), 1)

    def test_an_outage_stops_the_session_without_recording_it(self):
        clients = ask.Clients(build_rule=lambda lv: Failing(), build_asker=Failing)
        with tempfile.TemporaryDirectory() as d, mock.patch("builtins.print"), \
             mock.patch.object(ask, "pin", side_effect=lambda p: p):
            with self.assertRaises(ask.Outage):
                self.run_session(Path(d), "pass1", clients=clients)
            lines = (Path(d) / "pass1.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)          # the header, and no failure

    def test_the_smoke_run_end_to_end_and_the_turns(self):
        design = self.design
        with TempOut(), fake_sdk(openai=BaiduShaped(FixedResponses(answer_json()))), \
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
            self.assertEqual(len(rec["rows"]), 12)
            self.assertEqual(rec["provider"], plan.PROVIDER)
            self.assertIn("_env", rec)
            ok, why = ask.previous_check("pass2")
            self.assertFalse(ok)
            self.assertIn("pass 1", why)
            self.assertTrue(ask.previous_check("pass1")[0])
            with self.assertRaises(SystemExit):
                ask.main(["--session", "pass2"])
            with self.assertRaises(SystemExit):           # a paid record is never overwritten
                ask.main(["--session", "smoke"])

    def test_the_smoke_check_wants_every_attempt_from_the_pinned_provider(self):
        with TempOut():
            rows = [{"arm": arm, "valid": True,
                     "call_attempts": [{"provider": plan.PROVIDER_NAME}]}
                    for arm in prompts.ARMS]
            rec = {**json.loads(json.dumps(ask.protocol())), "rows": rows}
            plan.ask_path("smoke").write_text(json.dumps(rec))
            self.assertTrue(ask.smoke_check()[0])
            rows[1]["call_attempts"].insert(0, {"provider": "Relace"})
            plan.ask_path("smoke").write_text(json.dumps(rec))
            ok, why = ask.smoke_check()
            self.assertFalse(ok)
            self.assertIn("Relace", why)
            rec["provider"] = {"order": ["relace"], "allow_fallbacks": False}
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
# The 29 rules, and §5.6's classes, on tickets built by hand
# ---------------------------------------------------------------------------

def ticket(**kw) -> dict:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return {**base, **kw}


class TestTheRulesFromText(unittest.TestCase):

    def test_the_text_parses_to_29_rules_in_order(self):
        rs = rules.rules()
        self.assertEqual([r.id for r in rs], [f"H{k:02d}" for k in range(1, 30)])
        self.assertEqual(rs[0].conditions, (("has_security_keyword", "eq", True),
                                            ("customer_tier", "in", ("business", "enterprise"))))
        self.assertEqual(rs[0].queue, "SECURITY_INCIDENT")
        self.assertEqual(rs[-1].conditions, (("severity", "gte", 1),))

    def test_values_and_operators(self):
        self.assertEqual([rules.value_of(x) for x in ("True", "False", "3", "api", "['a', 'b']")],
                         [True, False, 3, "api", ("a", "b")])
        self.assertTrue(rules.holds(2, "lte", 2) and rules.holds("a", "in", ("a",)))
        self.assertTrue(rules.holds("pro", "neq", "free") and not rules.holds(1, "gte", 2))
        with self.assertRaises(ValueError):
            rules.holds(1, "lt", 2)

    def test_a_line_that_does_not_parse_is_an_error(self):
        with self.assertRaises(ValueError):
            rules.parse("H01: SI severity es 1 ENTONCES T1_GENERAL")
        self.assertEqual(rules.parse("LAS REGLAS\n\nSe aplica la primera regla.\n"), ())

    def test_first_match_on_tickets_built_by_hand(self):
        cases = ((ticket(has_security_keyword=True, customer_tier="enterprise"),
                  "SECURITY_INCIDENT"),
                 (ticket(severity=1, customer_tier="enterprise"), "ONCALL_ESCALATION"),
                 (ticket(severity=1, product="api"), "T3_ENGINEERING"),
                 (ticket(product="billing", customer_tier="enterprise"), "ACCOUNT_MANAGER"),
                 (ticket(severity=3, customer_tier="free"), "SELF_SERVICE_DEFLECT"),
                 (ticket(), "T1_GENERAL"))
        for t, queue in cases:
            with self.subTest(queue):
                self.assertEqual(rules.first_queue(t), queue)

    def test_the_classes(self):
        rs = rules.parse("H01: SI severity eq 1 ENTONCES A_Q\n"
                         "H02: SI product eq api ENTONCES B_Q\n"
                         "H03: SI severity eq 1 AND product eq api AND off_hours eq True "
                         "ENTONCES C_Q\n"
                         "H04: SI severity gte 1 ENTONCES D_Q\n")
        t = ticket(severity=1, product="api", off_hours=True)
        self.assertEqual([rules.classify(a, t, rs) for a in ("A_Q", "B_Q", "D_Q", "E_Q")],
                         ["first", "order", "order", "matching"])
        self.assertEqual(rules.most_conditions_queue(t, rs), "C_Q")
        self.assertEqual(rules.most_conditions_queue(ticket(severity=2), rs), "D_Q")
        self.assertEqual(rules.classify("C_Q", ticket(severity=1), rs), "matching")
        self.assertEqual(rules.CLASSES, ("first", "order", "matching"))


class TestStageAsReferencesOnAHandBuiltDesign(unittest.TestCase):

    def test_the_references(self):
        rs = rules.parse("H01: SI severity eq 1 ENTONCES A_Q\n"
                         "H02: SI product eq api ENTONCES B_Q\n"
                         "H03: SI severity gte 1 ENTONCES A_Q\n")
        cases = {"L3r1:1": ticket(severity=1, product="api"),
                 "L3r1:2": ticket(severity=2, product="api"),
                 "L2r1:3": ticket(severity=1)}
        decisions = {i: SimpleNamespace(level=int(i[1]), prompt=SimpleNamespace(
            case=SimpleNamespace(as_dict=lambda c=c: c))) for i, c in cases.items()}
        design = SimpleNamespace(decisions=decisions)
        lab = {"L3r1:1": {"y": "A_Q"}, "L3r1:2": {"y": "B_Q"}, "L2r1:3": {"y": "A_Q"}}
        before = {"apply_ticket": {"L3r1:1": ("B_Q", "A_Q"), "L3r1:2": ("Z_Q", None)}}
        with mock.patch.object(rules, "rules", return_value=rs):
            got = sample.references(design, lab, before)
        self.assertEqual(got["decisions_at_L3"], 2)
        self.assertEqual(got["matching_rules"], {"2": 1, "3": 1})
        self.assertEqual(got["first_match_at"], {"1": 1, "2": 1})
        self.assertEqual(got["a_lower_match_gives_another_queue"], 2)
        self.assertEqual(got["plan_apply_classes"]["apply_ticket"],
                         {"order": 1, "first": 1, "matching": 1})
        # Every rule here has one condition, so the most-conditions copier takes
        # the first match; the commonest queue breaks its tie toward the first.
        self.assertEqual(got["copiers"]["most_conditions"]["value"], 1.0)
        self.assertEqual(got["copiers"]["commonest_queue"]["value"], 1.0)


# ---------------------------------------------------------------------------
# Stage C by hand
# ---------------------------------------------------------------------------

Y, W, P = "T1_GENERAL", "BILLING_SPECIALIST", "T2_TECHNICAL"


def unit(level=3, run=1, ticket_=1, y=Y, t=(Y, Y), i=(Y, Y), q=(Y, Y), t0=(Y, Y),
         i0=(Y, Y), q0=(Y, Y), uid=None) -> score.Unit:
    return score.Unit(id=uid or f"L{level}r{run}:{ticket_}", level=level, run=run,
                      ticket=ticket_, y=y, t=tuple(t), i=tuple(i), q=tuple(q),
                      t0=tuple(t0), i0=tuple(i0), q0=tuple(q0))


def spec(row: str) -> score.Spec:
    return next(s for s in score.SPECS if s.id == row)


class TestTheTermsByHand(unittest.TestCase):

    def test_an_answer_is_valid_only_from_the_pinned_provider(self):
        row = {"action": P, "served_by": plan.PROVIDER_NAME}
        self.assertEqual(score.answer(row), P)
        self.assertIsNone(score.answer({**row, "served_by": "Relace"}))
        self.assertIsNone(score.answer({**row, "action": "NOT_A_QUEUE"}))
        self.assertIsNone(score.answer(None))

    def test_the_terms(self):
        u = unit(t=(W, Y), i=(Y, W), q=(Y, Y), t0=(W, W), q0=(Y, W))
        self.assertEqual(spec("QA-b").term(u), 1 - F(1, 2))
        self.assertEqual(spec("QA-c").term(u), 2 - F(1, 2))
        self.assertEqual(spec("QA-d").term(u), 1 - 2 * F(1, 2) + F(1, 2))
        self.assertEqual(spec("QA-e").term(u), 1)
        self.assertEqual(spec("QA-f").term(u), (1 - F(1, 2)) - (F(1, 2) - 0))

    def test_the_share_and_its_comparison_agree(self):
        for q, t in (((Y, Y), (W, W)), ((Y, W), (W, W)), ((W, W), (Y, W)), ((Y, W), (Y, W))):
            us = [unit(ticket_=k, q=q, t=t) for k in range(3)]
            v = score.statistic(spec("QA-c"), us)
            share = score.share(us)
            with self.subTest(q=q, t=t):
                self.assertEqual(v >= 0, share >= plan.QA_C_LINE)

    def test_the_clustered_error_is_plan_applys(self):
        self.assertIs(score.clustered_se, ascore.clustered_se)
        self.assertIs(score.hits, ascore.hits)


class TestTheVerdictsByHand(unittest.TestCase):

    def test_each_line_is_exact_at_its_edge(self):
        # QA-e at exactly 9/10: nine right of ten tickets holds.
        us = [unit(ticket_=k, q=(Y, Y) if k < 9 else (W, W)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("QA-e"), us)["verdict"], "holds")
        us[0] = unit(ticket_=0, q=(Y, W))
        self.assertEqual(score.adjudicate(spec("QA-e"), us)["verdict"], "refuted")
        # QA-b at exactly 0 is refuted: the line is held above.
        us = [unit(ticket_=k) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("QA-b"), us)["verdict"], "refuted")

    def test_a_row_with_too_many_invalid_answers_has_no_value(self):
        us = [unit(ticket_=k, q=(None, Y) if k < 6 else (Y, Y)) for k in range(100)]
        self.assertEqual(score.adjudicate(spec("QA-e"), us)["verdict"], "unadjudicable")
        us = [unit(ticket_=k, q=(None, Y) if k < 5 else (Y, Y)) for k in range(100)]
        self.assertNotEqual(score.adjudicate(spec("QA-e"), us)["verdict"], "unadjudicable")

    def test_qa_c_has_no_value_when_the_rule_arm_is_always_right(self):
        us = [unit(ticket_=k) for k in range(10)]
        got = score.adjudicate(spec("QA-c"), us)
        self.assertEqual(got["verdict"], "unadjudicable")
        self.assertEqual(got["line"], score.frac(plan.QA_C_LINE))

    def test_qa_d_has_no_value_without_a_gain(self):
        us = [unit(ticket_=k, t=(Y, Y), i=(W, W), q=(Y, Y)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("QA-d"), us)["verdict"], "unadjudicable")
        us = [unit(ticket_=k, t=(W, W), i=(W, W), q=(Y, Y)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("QA-d"), us)["verdict"], "holds")
        us = [unit(ticket_=k, t=(W, W), i=(Y, Y), q=(Y, Y)) for k in range(10)]
        self.assertEqual(score.adjudicate(spec("QA-d"), us)["verdict"], "refuted")

    def test_thin_by_the_error_and_by_one_run(self):
        us = ([unit(run=1, ticket_=k, q=(Y, Y), t=(W, W)) for k in range(5)]
              + [unit(run=2, ticket_=10 + k, q=(W, W), t=(W, W)) for k in range(20)])
        got = score.adjudicate(spec("QA-b"), us)
        self.assertEqual(got["verdict"], "holds")
        self.assertTrue(got["thin"])
        self.assertEqual(got["thin_because"]["dropping_one_run_flips"], ["L3r1"])

    def test_only_level_3_is_read(self):
        us = [unit(level=2, ticket_=k, q=(W, W)) for k in range(5)] + \
             [unit(level=3, ticket_=10 + k) for k in range(5)]
        self.assertEqual(score.adjudicate(spec("QA-e"), us)["read"], 5)


class TestTheAnchorByHand(unittest.TestCase):

    def test_its_term(self):
        p = score.Prompt(id="t:L3:1", ticket=1, today=(Y, Y), before=(Y, W))
        self.assertEqual(score.anchor_term(p), 1 - F(2, 4))
        p = score.Prompt(id="t:L3:1", ticket=1, today=(Y, W), before=(W,))
        self.assertEqual(score.anchor_term(p), 0 - F(1, 2))

    def test_plan_applys_answers_count_only_from_the_pinned_provider(self):
        row = {"action": Y, "call_attempts": [{"provider": "Relace"},
                                              {"provider": plan.PROVIDER_NAME}]}
        self.assertEqual(score.apply_answer(row), Y)
        self.assertIsNone(score.apply_answer({**row, "call_attempts": [{"provider": "GMICloud"}]}))
        self.assertIsNone(score.apply_answer({"action": Y}))

    def test_it_needs_a_hundred_prompts_and_is_thin_only_by_its_error(self):
        few = [score.Prompt(id=f"t:L3:{k}", ticket=k, today=(Y, Y), before=(Y,))
               for k in range(99)]
        self.assertEqual(score.adjudicate_anchor(few)["verdict"], "unadjudicable")
        enough = few + [score.Prompt(id="t:L3:99", ticket=99, today=(Y, Y), before=(Y,))]
        got = score.adjudicate_anchor(enough)
        self.assertEqual((got["verdict"], got["thin"]), ("holds", False))
        self.assertNotIn("dropping_one_run_flips", got["thin_because"])
        none_before = [score.Prompt(id=f"t:L3:{k}", ticket=k, today=(Y, Y), before=())
                       for k in range(200)]
        self.assertEqual(score.adjudicate_anchor(none_before)["read"], 0)


class TestStageCEndToEnd(unittest.TestCase):
    """Stage C over synthetic passes of every prompt, and synthetic answers of
    `PLAN_APPLY.md`'s: the structure, never a figure. §5.6's classes are stubbed,
    so that no real ticket is classified before the signature."""

    def test_score_runs_over_the_whole_design(self):
        d = population.build()
        lab = ascore.labels()

        def rows(k):
            return {"rows": [{"id": i, "arm": a.arm, "level": a.level, "action": Y,
                              "served_by": plan.PROVIDER_NAME, "failure": None,
                              "attempts": 1, "payload": {"action": Y},
                              "call_attempts": [{"provider": plan.PROVIDER_NAME}]}
                             for i, a in d.asks.items()]}
        apply_by_pass = {k: {i: {"id": i, "action": W,
                                 "call_attempts": [{"provider": plan.PROVIDER_NAME}]}
                             for i in d.apply.asks} for k in (1, 2)}
        with mock.patch.object(score, "classes", return_value={}):
            out = score.score(d, {"pass1": rows(1), "pass2": rows(2)}, lab, apply_by_pass)
        self.assertEqual(sorted(out["verdicts"]),
                         ["QA-a", "QA-b", "QA-c", "QA-d", "QA-e", "QA-f"])
        for rid, v in out["verdicts"].items():
            with self.subTest(rid):
                self.assertIn(v["verdict"], ("holds", "refuted", "unadjudicable"))
        self.assertEqual(out["verdicts"]["QA-a"]["read"], 676)
        self.assertEqual(out["verdicts"]["QA-b"]["decisions"], 320)
        self.assertEqual(set(out["QA-g"]), {"by_level", "by_ticket", "by_true_queue",
                                            "classes_at_L3", "agreement", "apply_beside",
                                            "the_calls"})


if __name__ == "__main__":
    unittest.main()
