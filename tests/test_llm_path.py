"""
The LLM path, end to end and without spending.

Until now only the parsing of this path was tested. What was not is everything
around it: how the request is built, how the SDK response is read, when it
retries, what reaches the base and what comes out in the metrics. Those are the
four things that were only exercised by paying for a run, and they are exactly
where a 2000-case run is lost halfway.

The double is described in `doubles.py`: it replaces the SDK CLIENT, not the
proposer, so the proposer runs in full.

TWO LEVELS, AND THEY DO DIFFERENT THINGS

  * the REQUEST classes pin the contract with the API: prompt, temperature,
    `response_format`, retries, and that the true action never travels. They
    rely on invented responses, because what they measure is the request.

  * the REPLAY classes are snapshots: they reproduce the whole recorded run from
    the record's own responses and require it to come out identical —rules,
    metrics and the raw records case by case. If somebody touches the validator,
    the arbitration or the metric computation, this catches it without having
    called anyone.

It holds for both paths: rung 1's (`results/llm_run.json`, 2000 cases, 632
escalations) and rung 2's (`results2/llm_run2_n100.json`, 100 cases, 42
escalations, with their priority edges).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from harness.domain import generate_corpus
from harness.dsl import RuleEngine
from harness.hidden_policy import true_action
from harness.shadow import run_shadow
from rung2.engine2 import PriorityEngine
from rung2.shadow2 import run_shadow2
from tests.fixtures import corpus, space
from tests.doubles import (
    FAKE_KEY,
    INTENTOS,
    FakeAnthropicClient,
    FakeOpenAIClient,
    OutOfSync,
    Script,
    FixedResponses,
    Turn,
    script_rung1,
    script_rung2,
    record,
    fake_sdk,
)

REPO = Path(__file__).resolve().parent.parent

RULE_PAYLOAD = json.dumps({
    "action": "T2_TECHNICAL",
    "conditions": [{"attr": "severity", "op": "lte", "value": 2}],
    "note": "una regla cualquiera, valida y que casa cualquier caso severo",
})


def one_case(idx: int = 0):
    return generate_corpus(idx + 1, seed=17)[idx]


def proposer1(script, **kwargs):
    """`OpenRouterProposer` built against the fake client."""
    client = FakeOpenAIClient(script)
    with fake_sdk(openai=client):
        from harness.proposers import OpenRouterProposer

        return OpenRouterProposer(**kwargs), client


def proposer2(script, **kwargs):
    client = FakeOpenAIClient(script)
    with fake_sdk(openai=client):
        from rung2.proposers2 import OpenRouterProposer2

        return OpenRouterProposer2(**kwargs), client


# ---------------------------------------------------------------------------
# The double
# ---------------------------------------------------------------------------

class TestTheDouble(unittest.TestCase):
    """Test infrastructure: if the double lies, everything below it lies."""

    def test_the_script_detects_a_question_about_another_case(self):
        """This is the check that turns the replay into a snapshot: if the path
        escalates somewhere else, it fails there and not on a different total at
        the end.

        And it comes out WHOLE through the proposer, which wraps every
        `Exception` in a `ProposalError`: that is why `OutOfSync` is not
        one of them."""
        script = Script([Turn(0, one_case(0).as_dict(), RULE_PAYLOAD)])
        prop, _ = proposer1(script)
        with self.assertRaises(OutOfSync) as ctx:
            prop.propose(one_case(1), true_action_hint=None)
        self.assertIn("turno 0", str(ctx.exception))

    def test_the_script_complains_if_asked_for_extra_turns(self):
        script = Script([Turn(0, one_case(0).as_dict(), RULE_PAYLOAD)])
        prop, _ = proposer1(script)
        prop.propose(one_case(0), true_action_hint=None)
        self.assertTrue(script.agotado)
        with self.assertRaises(OutOfSync):
            prop.propose(one_case(0), true_action_hint=None)

    def test_the_injected_sdk_is_removed_on_exit(self):
        """The suite runs with and without the venv; the double must leave no
        trace."""
        import sys

        prior = sys.modules.get("openai")
        with fake_sdk(openai=FakeOpenAIClient(FixedResponses(RULE_PAYLOAD))):
            self.assertIn("openai", sys.modules)
        self.assertIs(sys.modules.get("openai"), prior)


# ---------------------------------------------------------------------------
# The request — rung 1
# ---------------------------------------------------------------------------

class TestRequestRung1(unittest.TestCase):

    def setUp(self):
        self.case = one_case(0)

    def test_the_key_comes_from_the_environment_and_points_to_openrouter(self):
        """Hard rule 7: the key lives in the environment. Here it is checked that
        the proposer reads it from there and from nowhere else."""
        _, cli = proposer1(FixedResponses(RULE_PAYLOAD))
        self.assertEqual(cli.built_with["api_key"], FAKE_KEY)
        self.assertEqual(cli.built_with["base_url"],
                         "https://openrouter.ai/api/v1")

    def test_without_a_key_in_the_environment_it_is_not_built(self):
        from unittest import mock

        client = FakeOpenAIClient(FixedResponses(RULE_PAYLOAD))
        with fake_sdk(openai=client), \
                mock.patch.dict("os.environ", {}, clear=True):
            from harness.proposers import OpenRouterProposer

            with self.assertRaises(KeyError):
                OpenRouterProposer()

    def test_sends_the_system_prompt_and_the_ticket(self):
        from harness.proposers import SYSTEM_PROMPT

        prop, cli = proposer1(FixedResponses(RULE_PAYLOAD))
        prop.propose(self.case, true_action_hint=None)

        system, user = cli.peticiones[0]["messages"]
        self.assertEqual(system, {"role": "system", "content": SYSTEM_PROMPT})
        self.assertEqual(user["role"], "user")
        self.assertIn("TICKET EN IMPASSE:", user["content"])
        for attr, value in self.case.as_dict().items():
            with self.subTest(attr):
                self.assertIn(json.dumps(value), user["content"])

    def test_zero_temperature_and_requested_model(self):
        prop, cli = proposer1(FixedResponses(RULE_PAYLOAD),
                              model="openai/gpt-5.6-luna")
        prop.propose(self.case, true_action_hint=None)
        self.assertEqual(cli.peticiones[0]["temperature"], 0)
        self.assertEqual(cli.peticiones[0]["model"], "openai/gpt-5.6-luna")
        self.assertEqual(prop.name, "openrouter(openai/gpt-5.6-luna)")

    def test_the_true_action_does_not_travel_in_the_request(self):
        """The invariant that separates the LLM from the mocks: the mock gets
        the correct action for free and the LLM does not. `run_shadow` passes it
        the truth as `true_action_hint` and the proposer has to drop it."""
        prop, cli = proposer1(FixedResponses(RULE_PAYLOAD))
        truth = true_action(self.case)
        prop.propose(self.case, true_action_hint=truth)
        user = cli.peticiones[0]["messages"][1]["content"]
        self.assertNotIn(truth, user)

    def test_returns_the_action_from_the_payload(self):
        prop, _ = proposer1(FixedResponses(RULE_PAYLOAD))
        action_taken, payload = prop.propose(self.case, true_action_hint=None)
        self.assertEqual(action_taken, "T2_TECHNICAL")
        self.assertEqual(payload["action"], "T2_TECHNICAL")

    def test_gets_through_the_markdown_fence(self):
        """The tolerant parsing is already tested on its own; this checks that
        it is actually applied to what the SDK returns."""
        prop, _ = proposer1(FixedResponses(f"Aqui tienes:\n```json\n{RULE_PAYLOAD}\n```"))
        action_taken, _ = prop.propose(self.case, true_action_hint=None)
        self.assertEqual(action_taken, "T2_TECHNICAL")

    def test_an_empty_response_does_not_blow_up_the_run(self):
        """`content: None` is what the SDK returns when the model emits nothing.
        It has to end in ProposalError, which the loop counts and carries on."""
        from harness.proposers import ProposalError

        prop, _ = proposer1(FixedResponses(None))
        with self.assertRaises(ProposalError):
            prop.propose(self.case, true_action_hint=None)

    def test_json_object_only_on_the_first_attempt(self):
        """Some models do not support `response_format`; the retry removes it
        and relies on the tolerant parser."""
        from harness.proposers import ProposalError

        prop, cli = proposer1(FixedResponses("no es json"))
        with self.assertRaises(ProposalError):
            prop.propose(self.case, true_action_hint=None)
        self.assertEqual(cli.peticiones[0]["response_format"],
                         {"type": "json_object"})
        for p in cli.peticiones[1:]:
            self.assertNotIn("response_format", p)

    def test_the_retry_carries_a_repair_instruction(self):
        prop, cli = proposer1(FixedResponses("no es json", RULE_PAYLOAD))
        action_taken, _ = prop.propose(self.case, true_action_hint=None)
        self.assertEqual(action_taken, "T2_TECHNICAL")
        self.assertEqual(len(cli.peticiones), 2)
        self.assertEqual(len(cli.peticiones[0]["messages"]), 2)
        mensajes = cli.peticiones[1]["messages"]
        self.assertEqual(len(mensajes), 4)
        self.assertIn("UNICAMENTE con el objeto JSON", mensajes[-1]["content"])

    def test_exhausts_the_retries_and_raises_ProposalError(self):
        from harness.proposers import ProposalError

        prop, cli = proposer1(FixedResponses("no es json"))
        with self.assertRaises(ProposalError) as ctx:
            prop.propose(self.case, true_action_hint=None)
        self.assertEqual(len(cli.peticiones), INTENTOS)
        self.assertIn("sin objeto JSON", str(ctx.exception))

    def test_the_repair_instruction_is_not_duplicated(self):
        """Three attempts, a single pair of repair messages."""
        from harness.proposers import ProposalError

        prop, cli = proposer1(FixedResponses("no es json"))
        with contextlib.suppress(ProposalError):
            prop.propose(self.case, true_action_hint=None)
        self.assertEqual([len(p["messages"]) for p in cli.peticiones], [2, 4, 4])


# ---------------------------------------------------------------------------
# The request — Anthropic
# ---------------------------------------------------------------------------

class TestAnthropicRequest(unittest.TestCase):
    """The alternative provider. `run_experiment.py llm --provider anthropic`
    offers it, and until now nobody had exercised it."""

    def setUp(self):
        self.case = one_case(0)

    def _proposer(self, script, **kwargs):
        client = FakeAnthropicClient(script)
        with fake_sdk(anthropic=client):
            from harness.proposers import AnthropicProposer

            return AnthropicProposer(**kwargs), client

    def test_the_key_comes_from_the_environment(self):
        _, cli = self._proposer(FixedResponses(RULE_PAYLOAD))
        self.assertEqual(cli.built_with["api_key"], FAKE_KEY)

    def test_the_system_prompt_goes_with_cache_control(self):
        """It is what makes the run cheap: 2000 cases with the same prompt."""
        prop, cli = self._proposer(FixedResponses(RULE_PAYLOAD))
        prop.propose(self.case, true_action_hint=None)
        system = cli.peticiones[0]["system"]
        self.assertEqual(system[0]["cache_control"], {"type": "ephemeral"})

    def test_joins_only_the_text_blocks(self):
        from tests.doubles import _Block

        response = [_Block("thinking", "esto no es contenido"),
                    _Block("text", RULE_PAYLOAD)]
        prop, _ = self._proposer(FixedResponses(response))
        action_taken, _ = prop.propose(self.case, true_action_hint=None)
        self.assertEqual(action_taken, "T2_TECHNICAL")

    def test_exhausts_the_retries_and_raises_ProposalError(self):
        from harness.proposers import ProposalError

        prop, cli = self._proposer(FixedResponses("no es json"))
        with self.assertRaises(ProposalError):
            prop.propose(self.case, true_action_hint=None)
        self.assertEqual(len(cli.peticiones), INTENTOS)


# ---------------------------------------------------------------------------
# The request — rung 2
# ---------------------------------------------------------------------------

class TestRequestRung2(unittest.TestCase):

    def setUp(self):
        self.case = one_case(0)
        self.engine = PriorityEngine(space=space())

    def _propone(self, prop):
        _, _, base = prop.build_base(self.engine, self.case, [])
        return prop.propose(self.case, base)

    def test_sends_the_neighbourhood_and_the_ticket(self):
        prop, cli = proposer2(FixedResponses(RULE_PAYLOAD))
        self._propone(prop)
        user = cli.peticiones[0]["messages"][1]["content"]
        self.assertIn("BASE DE REGLAS: vacia", user)
        self.assertIn("TICKET EN IMPASSE:", user)

    def test_each_version_sends_its_own_prompt(self):
        from rung2.proposers2 import SYSTEM_PROMPT_V1, SYSTEM_PROMPT_V2

        for version, expected in (("v1", SYSTEM_PROMPT_V1),
                                  ("v2", SYSTEM_PROMPT_V2)):
            with self.subTest(version):
                prop, cli = proposer2(FixedResponses(RULE_PAYLOAD),
                                      prompt_version=version)
                self._propone(prop)
                self.assertEqual(cli.peticiones[0]["messages"][0]["content"],
                                 expected)
                self.assertIn(version, prop.name)

    def test_an_unknown_version_never_gets_built(self):
        with self.assertRaises(ValueError):
            proposer2(FixedResponses(RULE_PAYLOAD), prompt_version="v3")

    def test_json_object_only_on_the_first_attempt(self):
        from rung2.proposers2 import ProposalError

        prop, cli = proposer2(FixedResponses("no es json"))
        with self.assertRaises(ProposalError):
            self._propone(prop)
        self.assertEqual(len(cli.peticiones), INTENTOS)
        self.assertIn("response_format", cli.peticiones[0])
        self.assertNotIn("response_format", cli.peticiones[1])

    def test_the_declared_edges_reach_the_loop_with_their_verdict(self):
        """`beats`/`loses_to` is the only thing rung 2 adds to the schema. If
        the payload carries them, the loop has to see them and the engine has to
        judge them.

        The first two cases of the corpus arrive via `chat` and via `email`, so
        one rule per channel covers one each and they are disjoint: the edge the
        second declares against the first is rejected with `no_solapan`, which is
        the verdict repeated across the eight recorded runs.
        """
        def by_channel(channel, **extra):
            return json.dumps({
                "action": "T2_TECHNICAL",
                "conditions": [{"attr": "channel", "op": "eq", "value": channel}],
                "note": f"todo lo que entra por {channel}", **extra})

        script = FixedResponses(by_channel("chat"),
                                by_channel("email", beats=["R0001"]))
        client = FakeOpenAIClient(script)
        with fake_sdk(openai=client):
            from rung2.proposers2 import OpenRouterProposer2

            prop = OpenRouterProposer2()
            res = run_shadow2(generate_corpus(2, seed=17),
                              PriorityEngine(space=space()), prop)

        self.assertEqual(res.metrics["edges_proposed"], 1)
        self.assertEqual(res.metrics["edges_accepted"], 0)
        self.assertEqual(res.records[0].edge_reasons, [])
        self.assertEqual(res.records[1].edge_reasons, ["no_solapan"])
        self.assertEqual(res.rules[1].dropped_edges, ["beats:R0001:no_solapan"])


# ---------------------------------------------------------------------------
# Replay: the recorded run, whole, without calling anyone
# ---------------------------------------------------------------------------

class TestReplayRung1(unittest.TestCase):
    """Snapshot of `results/llm_run.json`: 2000 cases, 632 escalations.

    The responses come from the record itself (see `doubles.py`), so this checks
    the whole chain —request, parsing, validation, arbitration, metrics—
    against the run that produced the published figures.
    """

    @classmethod
    def setUpClass(cls):
        cls.reg = record("results/llm_run.json")
        cls.script = script_rung1(cls.reg)
        client = FakeOpenAIClient(cls.script)
        with fake_sdk(openai=client):
            from harness.proposers import OpenRouterProposer

            prop = OpenRouterProposer(model=cls.reg["model"])
            cls.res = run_shadow(list(corpus()), RuleEngine(), prop)
        cls.client = client

    def test_reproduces_the_rules_one_by_one(self):
        self.assertEqual([r.as_dict() for r in self.res.rules], self.reg["rules"])

    def test_reproduces_the_metrics(self):
        self.assertEqual(self.res.metrics, self.reg["metrics"])

    def test_reproduces_the_raw_records_case_by_case(self):
        self.assertEqual([vars(r) for r in self.res.records], self.reg["records"])

    def test_escalates_exactly_where_the_run_escalated(self):
        recorded = [r["idx"] for r in self.reg["records"] if r["escalated"]]
        self.assertEqual(self.script.seen, recorded)
        self.assertEqual(len(recorded), 632)

    def test_632_escalations_cost_700_calls(self):
        """The cost is not one call per escalation: the 34 parse failures are
        retried up to three times. The difference is paid for and appears in no
        metric of the record."""
        self.assertTrue(self.script.agotado)
        self.assertEqual(len(self.client.peticiones), 700)
        self.assertEqual(self.res.metrics["llm_calls"], 632)
        self.assertEqual(self.res.metrics["failed_proposals"], 34)

    def test_the_two_error_axes_stay_separate(self):
        """The two figures CLAUDE.md orders not to mix."""
        self.assertEqual(self.res.metrics["proposal_action_accuracy"], 0.3877)
        self.assertEqual(self.res.metrics["silent_error_rate"], 0.4839)


class TestReplayRung2(unittest.TestCase):
    """Snapshot of `results2/llm_run2_n100.json`: 100 cases, 42 escalations.

    It adds what rung 1 does not have: the neighbourhood in the request and the
    priority edges coming back, with their verdict.
    """

    @classmethod
    def setUpClass(cls):
        cls.reg = record("results2/llm_run2_n100.json")
        cls.script = script_rung2(cls.reg)
        client = FakeOpenAIClient(cls.script)
        engine = PriorityEngine(space=space())
        with fake_sdk(openai=client):
            from rung2.proposers2 import OpenRouterProposer2

            prop = OpenRouterProposer2(model=cls.reg["model"],
                                       prompt_version="v1")
            cls.res = run_shadow2(
                generate_corpus(cls.reg["n"], seed=cls.reg["seed"]), engine, prop)
        cls.engine = engine
        cls.client = client

    def test_reproduces_the_rules_with_their_edges(self):
        self.assertEqual([r.as_dict() for r in self.res.rules], self.reg["rules"])

    def test_reproduces_the_metrics(self):
        self.assertEqual(self.res.metrics, self.reg["metrics"])

    def test_reproduces_the_raw_records_case_by_case(self):
        self.assertEqual([vars(r) for r in self.res.records], self.reg["records"])

    def test_reproduces_the_verdict_of_each_edge(self):
        self.assertEqual([list(e) for e in self.engine.edge_log],
                         self.reg["edge_log"])
        self.assertEqual(self.res.metrics["edges_proposed"], 7)
        self.assertEqual(self.res.metrics["edges_accepted"], 0)

    def test_42_escalations_cost_46_calls(self):
        self.assertTrue(self.script.agotado)
        self.assertEqual(len(self.client.peticiones), 46)
        self.assertEqual(self.res.metrics["failed_proposals"], 2)


# ---------------------------------------------------------------------------
# The whole command
# ---------------------------------------------------------------------------

class TestTheRunAsTheCommandLaunchesIt(unittest.TestCase):
    """`run_experiment.py llm` from start to finish, including the dump.

    It is the command that costs money, and it is the only piece of the path no
    other test touches: the startup, the provider, the progress and the JSON
    left behind. With `OUT` redirected to a temporary directory: the suite does
    not write to `results*/` and this test checks that too.
    """

    N = 50

    @classmethod
    def setUpClass(cls):
        import run_experiment
        from unittest import mock

        cls.reg = record("results/llm_run.json")
        complete = script_rung1(cls.reg)
        cls.script = Script([t for t in complete.turns if t.idx < cls.N])
        cls.before = cls._fingerprint()

        cls.tmp = tempfile.TemporaryDirectory()
        client = FakeOpenAIClient(cls.script)
        args = argparse.Namespace(n=cls.N, seed=17, provider="openrouter",
                                  model=cls.reg["model"], out=None,
                                  overwrite_record=False)
        with fake_sdk(openai=client), \
                mock.patch.object(run_experiment, "OUT", Path(cls.tmp.name)), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            run_experiment.cmd_llm(args)
        cls.output = output.getvalue()
        # The name carries the n since Aug 8, 2026: the smoke test and the full
        # run used to write the same file. See harness/record_guard.py.
        cls.escrito = json.loads(
            (Path(cls.tmp.name) / f"llm_run_n{cls.N}.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @staticmethod
    def _fingerprint() -> str:
        return hashlib.sha256(
            (REPO / "results" / "llm_run.json").read_bytes()).hexdigest()

    def test_has_not_touched_the_published_record(self):
        """`results/llm_run.json` is the input of rungs 3 and 4 (hard rule 4).
        A test that trampled it would be worse than not having it."""
        self.assertEqual(self._fingerprint(), self.before)

    def test_the_json_carries_provenance_and_the_model(self):
        self.assertEqual(self.escrito["_env"]["seed"], 17)
        self.assertEqual(self.escrito["_env"]["n"], self.N)
        self.assertEqual(self.escrito["_env"]["provider"], "openrouter")
        self.assertEqual(self.escrito["model"], self.reg["model"])

    def test_the_json_does_not_leak_the_key(self):
        raw = json.dumps(self.escrito)
        self.assertNotIn(FAKE_KEY, raw)
        self.assertNotIn("API_KEY", raw)

    def test_keeps_the_rules_with_their_note_and_the_raw_records(self):
        self.assertEqual(len(self.escrito["records"]), self.N)
        self.assertTrue(all(r["note"] for r in self.escrito["rules"]))

    def test_the_prefix_reproduces_the_prefix_of_the_recorded_run(self):
        """The n=50 corpus is the prefix of the n=2000 one, so the rules and the
        decisions for those 50 cases have to come out identical.

        The firing counters do not: in the long run these same rules keep firing
        during the 1950 cases that do not exist here. It is the difference
        between the rule and its history.
        """
        def without_counters(rules):
            return [{k: v for k, v in r.items()
                     if k not in ("fire_count", "correct_count")} for r in rules]

        expected_rates = [r for r in self.reg["rules"] if r["born_at"] < self.N]
        self.assertEqual(without_counters(self.escrito["rules"]),
                         without_counters(expected_rates))
        self.assertEqual(self.escrito["records"],
                         self.reg["records"][: self.N])

    def test_warns_that_without_step_0_the_figures_are_void(self):
        """The ceiling warning goes in the run's output, not in the README."""
        self.assertIn("harness.ceiling_check", self.output)
        self.assertIn("58.75%", self.output)


if __name__ == "__main__":
    unittest.main()
