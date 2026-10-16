"""
WHAT EACH CALL SAYS ABOUT ITSELF — `harness/call_record.py`, checked against
the double and against the tree.

Four things are pinned:

  1. What an attempt keeps: every field of a response shaped like OpenRouter's,
     None for every field the bare double lacks, and the class of the exception
     when the request raised. Nothing of the message, ever.
  2. That the recorder changes no request and no response.
  3. That every client a paid writer uses carries it, and that the record paths
     keep what it says: v1e's answers and call rows, the resumable proposer's
     partial file, the pairwise rows. The rung 2 loop's `calls` are checked in
     `tests/test_llm_path.py`, against the replay of a published run; the rows
     of `fidelity/ask.py` and `screen/ask.py` in their own test modules.
  4. That no call site goes unrecorded: the call sites are derived from the tree,
     as `tests/test_writer_lists.py` derives the writers, and each is recorded
     or exempt for a stated reason.
"""

from __future__ import annotations

import importlib
import json
import re
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from harness import call_record
from harness.call_record import FIELDS, CallRecorder
from harness.domain import generate_corpus
from harness.provenance import CODE_ROOTS

from tests.doubles import (INTENTOS, FixedResponses, OpenRouterShapedClient, _Choice,
                           _Completion, _Message, fake_sdk)

REPO = Path(__file__).resolve().parent.parent

GOOD = json.dumps({"action": "T2_TECHNICAL",
                   "conditions": [{"attr": "severity", "op": "lte", "value": 2}],
                   "note": "una regla cualquiera"})
TEXT = "un texto de mensaje que no puede aparecer en ningun intento"
T1 = "T1_GENERAL"


def openrouter_response(text: str = "{}", **over) -> types.SimpleNamespace:
    """A response with every field OpenRouter documents around an answer, and
    the undocumented `provider`."""
    body = {
        "id": "gen-1", "provider": "DeepInfra",
        "model": "deepseek/deepseek-v4-flash", "system_fingerprint": "fp-1",
        "choices": [types.SimpleNamespace(
            finish_reason="length", native_finish_reason="MAX_TOKENS",
            message=types.SimpleNamespace(content=text))],
        "usage": types.SimpleNamespace(
            prompt_tokens=900, completion_tokens=1200,
            completion_tokens_details=types.SimpleNamespace(reasoning_tokens=1100)),
    }
    body.update(over)
    return types.SimpleNamespace(**body)


def client_returning(create) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))


def built(path: str, client):
    """A paid client, built against the double."""
    module, name = path.rsplit(".", 1)
    with fake_sdk(openai=client):
        return getattr(importlib.import_module(module), name)()


def messages() -> list[dict[str, str]]:
    return [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]


# ---------------------------------------------------------------------------
# 1. What an attempt keeps
# ---------------------------------------------------------------------------

class TestWhatAnAttemptKeeps(unittest.TestCase):

    def test_every_field_of_a_response_shaped_like_openrouters(self):
        got = call_record.attempt(openrouter_response())
        self.assertEqual(got, {
            "generation_id": "gen-1", "provider": "DeepInfra",
            "model": "deepseek/deepseek-v4-flash", "system_fingerprint": "fp-1",
            "finish_reason": "length", "native_finish_reason": "MAX_TOKENS",
            "prompt_tokens": 900, "completion_tokens": 1200,
            "reasoning_tokens": 1100, "error": None})
        self.assertEqual(tuple(got), FIELDS)

    def test_a_field_the_response_lacks_is_none_never_guessed(self):
        """The bare double returns the text and nothing around it."""
        got = call_record.attempt(_Completion(choices=[_Choice(_Message("{}"))]))
        self.assertEqual(got, dict.fromkeys(FIELDS))

    def test_no_choices_and_no_usage_leave_their_fields_none(self):
        got = call_record.attempt(types.SimpleNamespace(id="gen-2", choices=[],
                                                        usage=None))
        self.assertEqual((got["generation_id"], got["finish_reason"],
                          got["prompt_tokens"], got["reasoning_tokens"]),
                         ("gen-2", None, None, None))

    def test_a_request_that_raised_keeps_its_class_and_nothing_else(self):
        self.assertEqual(call_record.failed(TimeoutError("slow")),
                         dict.fromkeys(FIELDS) | {"error": "TimeoutError"})

    def test_nothing_of_the_message_is_kept(self):
        got = call_record.attempt(openrouter_response(text=TEXT))
        self.assertNotIn(TEXT, json.dumps(got))

    def test_what_is_kept_is_plain_json(self):
        got = call_record.attempt(openrouter_response(provider=object(),
                                                      model=["not", "a", "name"]))
        json.dumps(got)
        self.assertIsInstance(got["provider"], str)
        self.assertIsInstance(got["model"], str)

    def test_the_sdk_keeps_openrouters_extra_fields_as_attributes(self):
        """What `attempt` relies on: the `openai` SDK keeps the fields its
        schema lacks, `provider` and `native_finish_reason`, as attributes.
        Checked with 2.53.0 on 2026-10-16. The suite runs without the venv, so
        this only runs where the SDK is installed."""
        try:
            from openai.types.chat import ChatCompletion
        except ImportError:
            self.skipTest("the openai SDK is not installed here")
        resp = ChatCompletion.model_validate({
            "id": "gen-3", "provider": "DeepInfra", "model": "m",
            "object": "chat.completion", "created": 1,
            "choices": [{"index": 0, "finish_reason": "stop",
                         "native_finish_reason": "stop",
                         "message": {"role": "assistant", "content": "{}"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2,
                      "completion_tokens_details": {"reasoning_tokens": 0}}})
        got = call_record.attempt(resp)
        self.assertEqual((got["provider"], got["native_finish_reason"],
                          got["reasoning_tokens"]), ("DeepInfra", "stop", 0))


# ---------------------------------------------------------------------------
# 2. The recorder changes nothing
# ---------------------------------------------------------------------------

class TestTheRecorderChangesNothing(unittest.TestCase):

    def test_the_request_reaches_the_client_as_it_was_built(self):
        sent = {"model": "m", "messages": [{"role": "user", "content": TEXT}],
                "max_tokens": 1200, "temperature": 0,
                "response_format": {"type": "json_object"},
                "extra_body": {"reasoning": {"effort": "none"}}}
        inner = OpenRouterShapedClient(FixedResponses("{}"))
        rec = CallRecorder(inner)
        rec.chat.completions.create(**sent)
        self.assertEqual(inner.peticiones, [sent])
        self.assertIs(inner.peticiones[0]["messages"], sent["messages"])
        self.assertNotIn(TEXT, json.dumps(rec.attempts))

    def test_the_response_is_the_clients_own_object(self):
        resp = openrouter_response()
        rec = CallRecorder(client_returning(lambda **kw: resp))
        self.assertIs(rec.chat.completions.create(model="m"), resp)
        self.assertEqual(rec.take(), [call_record.attempt(resp)])

    def test_a_request_that_raises_is_recorded_and_raised_as_it_was(self):
        boom = ConnectionError("down")

        def create(**kwargs):
            raise boom

        rec = CallRecorder(client_returning(create))
        with self.assertRaises(ConnectionError) as ctx:
            rec.chat.completions.create(model="m")
        self.assertIs(ctx.exception, boom)
        self.assertEqual(rec.take(), [call_record.failed(boom)])

    def test_take_returns_the_attempts_since_the_last_take(self):
        rec = CallRecorder(OpenRouterShapedClient(FixedResponses("{}")))
        rec.chat.completions.create(model="m")
        rec.chat.completions.create(model="m")
        self.assertEqual([a["generation_id"] for a in rec.take()],
                         ["gen-double-1", "gen-double-2"])
        self.assertEqual(rec.take(), [])

    def test_installing_twice_does_not_wrap_twice(self):
        holder = types.SimpleNamespace(_client=OpenRouterShapedClient(FixedResponses("{}")))
        first = call_record.install(holder)
        self.assertIs(call_record.install(holder), first)
        self.assertIs(holder._client, first)
        self.assertNotIsInstance(first.inner, CallRecorder)


# ---------------------------------------------------------------------------
# 3. Every paid client carries it, and the record paths keep it
# ---------------------------------------------------------------------------

PAID_CLIENTS = ("rung2.proposers2.OpenRouterProposer2",
                "authorship.protocol.ProposerE",
                "overlap.protocol.ProposerV2E",
                "blind.protocol.ProposerV2B",
                "rung2.pair_judgement.Judge")


class TestEveryPaidClientCarriesIt(unittest.TestCase):

    def test_each_client_is_wrapped_once_around_the_sdks(self):
        for path in PAID_CLIENTS:
            with self.subTest(path):
                client = OpenRouterShapedClient(FixedResponses(GOOD))
                obj = built(path, client)
                self.assertIsInstance(obj._client, CallRecorder)
                self.assertIs(obj.calls, obj._client)
                self.assertIs(obj._client.inner, client)

    def test_a_retried_proposal_leaves_one_attempt_per_request(self):
        client = OpenRouterShapedClient(FixedResponses("no es JSON", GOOD))
        prop = built("rung2.proposers2.OpenRouterProposer2", client)
        prop.propose(generate_corpus(1, seed=17)[0], "BASE")
        got = prop.calls.take()
        self.assertEqual(len(client.peticiones), 2)
        self.assertEqual([a["generation_id"] for a in got],
                         ["gen-double-1", "gen-double-2"])
        self.assertEqual({a["provider"] for a in got},
                         {OpenRouterShapedClient.PROVIDER})
        self.assertEqual({a["finish_reason"] for a in got}, {"stop"})

    def test_the_judge_records_every_attempt_of_a_question(self):
        client = OpenRouterShapedClient(FixedResponses("no", '{"action": "T1_GENERAL"}'))
        judge = built("rung2.pair_judgement.Judge", client)
        judge.ask("question")
        self.assertEqual(len(judge.calls.take()), len(client.peticiones))


class TestV1eAnswersCarryTheirAttempts(unittest.TestCase):

    def test_an_answer_carries_its_own_question_and_no_other(self):
        client = OpenRouterShapedClient(FixedResponses(GOOD))
        prop = built("authorship.protocol.ProposerE", client)
        first, second = prop.ask(messages()), prop.ask(messages())
        self.assertEqual([a["generation_id"] for a in first.call_attempts],
                         ["gen-double-1"])
        self.assertEqual([a["generation_id"] for a in second.call_attempts],
                         ["gen-double-2"])

    def test_an_answer_that_never_parsed_carries_all_its_attempts(self):
        from authorship import protocol as p
        client = OpenRouterShapedClient(FixedResponses("nada"))
        prop = built("authorship.protocol.ProposerE", client)
        with self.assertRaises(p.ProposalFailed) as ctx:
            prop.ask(messages())
        self.assertEqual(len(ctx.exception.call_attempts), INTENTOS)
        self.assertEqual(ctx.exception.attempts, INTENTOS)
        self.assertEqual(ctx.exception.finish_reason, "stop")


class TestTheCallRowsKeepThem(unittest.TestCase):

    def setUp(self):
        self.said = [call_record.attempt(openrouter_response())]

    def test_a_row_has_the_key_exactly_when_attempts_were_recorded(self):
        from authorship import loop
        from authorship import protocol as p
        with_ = loop.call_row(0, p.Answer(T1, {"action": T1}, "{}", "stop", 1, self.said))
        without = loop.call_row(0, p.Answer(T1, {"action": T1}, "{}", "stop", 1))
        self.assertEqual(with_["call_attempts"], self.said)
        self.assertNotIn("call_attempts", without)

    def test_a_failed_call_keeps_what_its_exception_carried(self):
        from authorship import loop
        row = loop.call_row(1, None, failure="no answer", finish="length",
                            attempts=3, call_attempts=self.said * 3)
        self.assertEqual(row["call_attempts"], self.said * 3)

    def test_the_partial_file_keeps_them_and_a_resume_serves_them_back(self):
        from authorship import protocol as p
        from authorship import run
        case = generate_corpus(1, seed=17)[0]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "partial.jsonl"
            header = run.protocol_header("r1", 2000)
            rows, _ = run.open_partial(path, header)
            live = mock.Mock()
            live.ask.side_effect = [
                p.ProposalFailed("no answer", "length", 3, self.said * 3),
                p.Answer(T1, {"action": T1}, "{}", "stop", 1, self.said)]
            r = run.Resumable(live, path, rows)
            with self.assertRaises(p.ProposalFailed):
                r.first(case, "BASE", idx=0)
            r.first(case, "BASE", idx=1)
            stored, again = run.open_partial(path, header)
            self.assertTrue(again)
            self.assertEqual([len(s["call_attempts"]) for s in stored], [3, 1])
            never = mock.Mock(ask=mock.Mock(side_effect=AssertionError("asked")))
            served = run.Resumable(never, path, stored)
            self.assertEqual(served.first(case, "BASE", idx=1).call_attempts, self.said)
            with self.assertRaises(p.ProposalFailed) as ctx:
                served.first(case, "BASE", idx=0)
            self.assertEqual(ctx.exception.call_attempts, self.said * 3)

    def test_a_row_paid_for_before_the_recorder_is_served_without_them(self):
        from authorship import protocol as p
        from authorship import run
        case = generate_corpus(1, seed=17)[0]
        msgs = p.messages_for(case, "BASE")
        row = {"idx": 0, "round": 0, "digest": run.digest(msgs), "raw": "{}",
               "payload": {"action": T1}, "finish_reason": "stop", "attempts": 1,
               "failure": None}
        with tempfile.TemporaryDirectory() as d:
            never = mock.Mock(ask=mock.Mock(side_effect=AssertionError("asked")))
            served = run.Resumable(never, Path(d) / "p.jsonl", [row])
            self.assertEqual(served.first(case, "BASE", idx=0).call_attempts, [])


class TestThePairwiseRowsKeepThem(unittest.TestCase):
    """The two loops of `rung2/pair_judgement.py` run behind their plans'
    signatures and the key, so they are read rather than run: each clears the
    judge's recorder before it asks, and stores what it took after."""

    def test_both_loops_clear_before_asking_and_store_after(self):
        src = (REPO / "rung2" / "pair_judgement.py").read_text()
        self.assertEqual(src.count('r["call_attempts"] = judge.calls.take()'), 2)
        self.assertEqual(src.count("judge.calls.take()\n        try:\n"
                                   "            payload, attempts = judge.ask("), 2)


# ---------------------------------------------------------------------------
# 4. No call site goes unrecorded
# ---------------------------------------------------------------------------

CALLS_THE_API = re.compile(r"chat\.completions\.create\(")

EXEMPT = {
    "harness/proposers.py":
        "rung 1's proposers. Their loop, harness/shadow.py, is frozen (hard rule 1) "
        "and keeps no per-call field, and rung 1 does not run again.",
}


def call_sites() -> set[str]:
    """Every module under `CODE_ROOTS` that calls the API."""
    out: set[str] = set()
    for root in CODE_ROOTS:
        p = REPO / root
        files = [p] if p.is_file() else (sorted(p.rglob("*.py")) if p.is_dir() else [])
        for f in files:
            if "__pycache__" not in f.parts and CALLS_THE_API.search(f.read_text()):
                out.add(f.relative_to(REPO).as_posix())
    return out


class TestNoCallSiteGoesUnrecorded(unittest.TestCase):

    def test_every_call_site_is_recorded_or_exempt_for_a_reason(self):
        for module in sorted(call_sites() - {"harness/call_record.py"} - set(EXEMPT)):
            with self.subTest(module):
                src = (REPO / module).read_text()
                self.assertTrue("call_record" in src or "calls.take()" in src,
                                f"{module} calls the API and records nothing")

    def test_the_call_sites_are_the_ones_classified_here(self):
        """A new call site fails this until somebody decides how it is
        recorded. That decision is the point."""
        self.assertEqual(call_sites(), {"harness/call_record.py",
                                        "harness/proposers.py",
                                        "rung2/proposers2.py",
                                        "rung2/pair_judgement.py",
                                        "authorship/protocol.py",
                                        "screen/ask.py"})

    def test_every_exemption_says_why(self):
        for module, why in EXEMPT.items():
            with self.subTest(module):
                self.assertIn(module, call_sites())
                self.assertGreater(len(why), 40)


if __name__ == "__main__":
    unittest.main()
