"""
`PLAN_REASONED_LOOP.md`'s instrument, `reasoned_loop/`. **No figure of the plan**:
no test runs the loop over the corpus, and every rule, ticket, engine, run and
edge below is built by hand. The figures §0 declares are recomputed by `RL-g2`
and Stage A, never here.

What is pinned:

  1. §11's constants and §0's lines, the schedule, and the gate, which counts
     every signature line.
  2. Nothing is built, asked or written while the plan is unsigned, the dry
     runs build no client, and a run refuses before the key without what must
     come before it.
  3. v1b's texts are their sources', and the two calls' messages.
  4. The requests through the SDK double, and `PLAN_FIRST_MATCH.md`'s retry by
     cause.
  5. One escalation, every verdict, on engines built by hand.
  6. Both triggers, `cover`, the cap, and what an error escalation keeps.
  7. The resumable proposer keeps each answer's keys, reasoning, retries and
     provider through a resume.
  8. The smoke check.
  9. Stage C's terms: the exact direction beside `blind.rows`', medians, thin
     labels and every reason a row has no value.
 10. The hidden policy through v1b's path is born whole and decides both
     surfaces right: the instrument on a policy whose answer is known.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import Case

from authorship import protocol as e
from authorship import run as erun
from blind import protocol as v2b
from blind import rows as brows
from first_match import ask as fm_ask
from first_match import plan as fm_plan
from manual import instrument as MI
from manual import prompts as mprompts
from rung2.engine2 import EDGE_OK, PriorityEngine, validate_conditions
from rung2.proposers2 import ProposalError, user_msg

from reasoned_loop import gates, loop, plan, references, run, sample, score
from reasoned_loop import protocol as p
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
F = Fraction
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
T1, T2, T3, S = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"


class BaiduReasons(OpenRouterShapedClient):
    """The double, served by the pinned provider, reasoning on every call."""
    PROVIDER = plan.PROVIDER_NAME
    REASONING = "H29 casa el ticket y ninguna regla anterior lo hace."

    def _create(self, **kwargs):
        resp = super()._create(**kwargs)
        resp.choices[0].message = SimpleNamespace(content=resp.choices[0].message.content,
                                                  reasoning=self.REASONING)
        resp.usage.completion_tokens_details = SimpleNamespace(reasoning_tokens=321)
        return resp


class Raises:
    """A script that raises on the calls it is told to, as an upstream 429 does."""

    def __init__(self, fail: set[int], text: str):
        self.fail, self.text, self.n = fail, text, 0

    def __call__(self, kwargs):
        self.n += 1
        if self.n in self.fail:
            raise RuntimeError("Error code: 429 - temporarily rate-limited upstream")
        return self.text


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


def ticket(**kw) -> dict:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return {**base, **kw}


def case(**kw) -> Case:
    return Case(**ticket(**kw))


def payload(action: str, *conds, beats=(), loses_to=(), **extra) -> dict:
    return {"action": action,
            "conditions": [{"attr": a, "op": o, "value": v} for a, o, v in conds],
            "beats": list(beats), "loses_to": list(loses_to), "note": "una regla", **extra}


def answer(pl: dict) -> p.Answer:
    return p.Answer(pl.get("action"), pl, None, "stop", 1)


CATCH_ALL = (T1, ("severity", "gte", 1))
API = (T2, ("product", "eq", "api"))
KEYWORD = (S, ("has_security_keyword", "eq", True))


def engine_with(*rules) -> PriorityEngine:
    eng = PriorityEngine(space=MI.space())
    for k, (action, *conds) in enumerate(rules):
        eng.add(validate_conditions(payload(action, *conds), None), born_at=k)
    return eng


class Scripted:
    """A proposer double: each draft and placement from a function, every call
    remembered."""
    name = "scripted"

    def __init__(self, draft, place=None):
        self.draft, self.place, self.asked = draft, place, []

    def first(self, case, idx):
        self.asked.append(("first", idx))
        got = self.draft(case, idx)
        if isinstance(got, Exception):
            raise got
        return answer(got)

    def placement(self, case, draft, message, idx, listed=None):
        self.asked.append(("placement", idx, list(listed or []), message))
        got = self.place(case, draft, listed, idx)
        if isinstance(got, Exception):
            raise got
        return answer(got)


def placing(beats=(), loses_to=()):
    """A placement that repeats the draft and places the listed rules."""
    def place(case, draft, listed, idx):
        b = [r for r in listed if r in beats or beats == "all"]
        lo = [r for r in listed if r in loses_to or loses_to == "all"]
        return dict(draft.payload, beats=b, loses_to=lo)
    return place


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_first_matchs_reasoning_arm(self):
        self.assertEqual(plan.MODEL, fm_plan.MODEL)
        self.assertEqual(plan.TEMPERATURE, 0)
        self.assertEqual(plan.REASONING, {"effort": "high"})
        self.assertEqual(plan.REASONING, fm_plan.REASONING_ON)
        self.assertEqual(plan.MAX_TOKENS, 16000)
        self.assertEqual(plan.MAX_TOKENS, fm_plan.MAX_TOKENS_REASONING)
        self.assertEqual((plan.MAX_RETRIES, plan.CALL_RETRY_WAIT), (2, (10, 30)))
        self.assertEqual(plan.PROVIDER, {"order": ["baidu"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, fm_plan.PROVIDER_NAME)
        self.assertEqual(plan.settings(), {"reasoning": {"effort": "high"},
                                           "max_tokens": 16000})

    def test_the_protocol_the_arms_and_the_runs(self):
        self.assertEqual((plan.PROTOCOL, plan.LEVEL), ("v1b", 3))
        self.assertEqual(plan.ARMS, ("i", "e"))
        self.assertEqual(plan.TRIGGERS, {"i": ("IMPASSE", "CONFLICT"),
                                         "e": ("IMPASSE", "CONFLICT", "ERROR")})
        self.assertEqual((plan.REPS, plan.N, plan.SEED), (3, 2000, 17))
        self.assertEqual((plan.SMOKE_N, plan.SMOKE_ARM), (30, "e"))
        self.assertEqual(plan.MAX_ESCALATIONS, 400)
        self.assertEqual(plan.MAX_CONSECUTIVE_FAILURES, erun.STOP_AFTER_FAILURES_IN_A_ROW)
        self.assertEqual((plan.MIN_ESCALATIONS, plan.MIN_UNITS, plan.COVER_BEFORE),
                         (60, 20, 200))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 83)
        self.assertNotIn(plan.ORDER_SEED, {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61, 67,
                                           71, 73, 79})

    def test_the_lines_are_section_0s_as_fractions(self):
        self.assertEqual(plan.LINES, {"RL-a": F(9, 10), "RL-b": F(2, 3), "RL-c": F(1, 10),
                                      "RL-d": F(9, 10), "RL-e": F(9, 10), "RL-f": F(0),
                                      "RL-g": F(9, 10)})
        for v in plan.LINES.values():
            self.assertIsInstance(v, Fraction)

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_REASONED_LOOP.md").read_text()
        for s in ("`ORDER_SEED = 83`", "`MAX_ESCALATIONS = 400`", "`SMOKE_N = 30`",
                  "`MIN_ESCALATIONS = 60`", "`MIN_UNITS = 20`", "`COVER_BEFORE = 200`",
                  "`RL_A_LINE = Fraction(9, 10)`", "`RL_B_LINE = Fraction(2, 3)`",
                  "`RL_C_LINE = Fraction(1, 10)`", "`RL_F_LINE = 0`",
                  plan.SYSTEM_PROMPT_SHA16):
            with self.subTest(s):
                self.assertIn(s, text)

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        self.assertEqual(order, plan.schedule())
        self.assertEqual(len(order), 6)
        arms = [a for a, _ in order]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))
        self.assertEqual([r for _, r in order], [1, 1, 2, 2, 3, 3])
        self.assertEqual(sorted(order), sorted((a, r) for a in plan.ARMS for r in (1, 2, 3)))

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            for path in (plan.sample_path(), plan.score_path(), plan.smoke_path(),
                         plan.run_path("e", 2), plan.partial_path(plan.tag("i", 3))):
                self.assertEqual(path.parent, d)
        self.assertEqual(plan.tag(None, None), "smoke")
        with self.assertRaises(ValueError):
            plan.run_path("x", 1)
        with self.assertRaises(ValueError):
            plan.run_path("e", 4)


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_blank_signed_and_a_blank_second_line(self):
        cases = (("**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-31)**\n", True),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-10-31)**\n"
                  "**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "PLAN.md"
            for text, ok in cases:
                path.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(path)["passes"], ok)

    def test_the_plan_carries_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned: a test
        that pinned the draft's blank line would fail at the signature."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_REASONED_LOOP.md")["found"],
                         plan.MIN_SIGNATURES)


# ---------------------------------------------------------------------------
# 2. Nothing unsigned, and the order of events
# ---------------------------------------------------------------------------

def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(p, "Asker", side_effect=AssertionError("asker built")) as asker, \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        for m in (checks, asker, fetch, write):
            m.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        self.refuses(run.main, ["--smoke"])
        for arm, rep in plan.schedule():
            with self.subTest(arm=arm, rep=rep):
                self.refuses(run.main, ["--arm", arm, "--rep", str(rep)])

    def test_the_free_writers_refuse_too(self):
        self.refuses(sample.main, [])
        self.refuses(score.main, [])

    def test_the_dry_runs_build_no_client_need_no_key_and_write_nothing(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(p, "Asker", side_effect=AssertionError("asker built")) as asker, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (run.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        for m in (fetch, asker, write):
            m.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            for main in (run.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 1)

    def test_a_run_refuses_before_the_key_without_what_comes_before_it(self):
        with TempOut() as d, \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch("builtins.print"):
            for argv in (["--smoke"], ["--arm", "e", "--rep", "1"]):
                with self.subTest(argv), self.assertRaises(SystemExit):
                    run.main(argv)           # no Stage A record
            (d / "sample.json").write_text(json.dumps({"references": {
                "fingerprint": p.fingerprint(),
                "schedule": [list(x) for x in plan.schedule()]}}))
            self.assertTrue(run.sample_check()[0])
            with self.assertRaises(SystemExit):
                run.main(["--arm", "e", "--rep", "1"])   # no smoke record
        fetch.assert_not_called()
        checks.assert_not_called()

    def test_a_stage_a_record_under_another_schedule_is_refused(self):
        with TempOut() as d:
            (d / "sample.json").write_text(json.dumps({"references": {
                "fingerprint": p.fingerprint(), "schedule": [["i", 1]]}}))
            self.assertFalse(run.sample_check()[0])

    def test_the_turn(self):
        with TempOut():
            (first_arm, _), (second_arm, _) = plan.schedule()[:2]
            self.assertTrue(run.turn_check(first_arm, 1)[0])
            self.assertFalse(run.turn_check(second_arm, 1)[0])
            plan.run_path(first_arm, 1).write_text("{}")
            self.assertTrue(run.turn_check(second_arm, 1)[0])
            self.assertEqual(run.next_run(), (second_arm, 1))


# ---------------------------------------------------------------------------
# 3. The texts and the messages
# ---------------------------------------------------------------------------

class TestTheTextsAreTheirSources(unittest.TestCase):

    def test_none_is_new(self):
        self.assertEqual(p.SYSTEM_PROMPT, mprompts.loop_system_prompt(3))
        self.assertEqual(p.sha256(p.SYSTEM_PROMPT)[:16], plan.SYSTEM_PROMPT_SHA16)
        self.assertIs(p.BLIND_BASE, v2b.BLIND_BASE)
        self.assertIs(p.PLACEMENT_TEMPLATE, v2b.PLACEMENT_TEMPLATE)
        self.assertEqual(p.RETRY_MSG, mprompts.RETRY_MSG)

    def test_the_two_calls(self):
        c = case(product="api")
        draft = answer(payload(T2, ("product", "eq", "api"), note="nota"))
        first = p.messages_for(c)
        second = p.messages_for(c, draft, "situala")
        self.assertEqual(first, [{"role": "system", "content": p.SYSTEM_PROMPT},
                                 {"role": "user", "content": user_msg(c, p.BLIND_BASE)}])
        self.assertEqual(second[:2], first)
        self.assertEqual(second[2], {"role": "assistant", "content": p.turn(draft)})
        self.assertEqual(second[3], {"role": "user", "content": "situala"})

    def test_the_turn_is_the_payload_with_its_keys_in_order(self):
        pl = {"note": "ñ", "action": T2, "conditions": [], "beats": [], "loses_to": []}
        self.assertEqual(p.turn(answer(pl)), json.dumps(pl, ensure_ascii=False))
        self.assertEqual(list(json.loads(p.turn(answer(pl)))), list(pl))

    def test_a_changed_character_moves_a_digest_and_the_fingerprint(self):
        base, fp = p.digests(), p.fingerprint()
        with mock.patch.object(p, "BLIND_BASE", p.BLIND_BASE + " "):
            self.assertNotEqual(p.digests()["blind_base"], base["blind_base"])
            self.assertNotEqual(p.fingerprint(), fp)
        self.assertEqual(p.fingerprint(), fp)


# ---------------------------------------------------------------------------
# 4. The requests
# ---------------------------------------------------------------------------

class TestTheRequests(unittest.TestCase):

    def asked(self, messages, client, sleep=None):
        with fake_sdk(openai=client):
            live = p.Live(p.Asker(sleep=sleep or (lambda s: None)))
            got = live.ask(messages)
        return got, client.peticiones

    def test_every_call_carries_the_setting_the_budget_and_the_pin(self):
        msgs = p.messages_for(case())
        text = json.dumps(payload(T1, ("severity", "gte", 1)))
        got, (req,) = self.asked(msgs, BaiduReasons(FixedResponses(text)))
        self.assertEqual(req["model"], plan.MODEL)
        self.assertEqual(req["temperature"], 0)
        self.assertEqual(req["max_tokens"], 16000)
        self.assertEqual(req["response_format"], {"type": "json_object"})
        self.assertEqual(req["extra_body"], {"reasoning": {"effort": "high"},
                                             "provider": plan.PROVIDER})
        self.assertEqual(req["messages"], msgs)
        self.assertEqual(got.action, T1)
        self.assertIsNone(got.raw)
        self.assertEqual(got.keys, list(json.loads(text)))
        self.assertEqual(got.reasoning, BaiduReasons.REASONING)
        self.assertEqual(got.retries, [])
        self.assertEqual(got.served_by, plan.PROVIDER_NAME)
        self.assertEqual(len(got.call_attempts), 1)
        self.assertEqual(got.call_attempts[0]["reasoning_tokens"], 321)

    def test_the_placement_call_sends_the_draft_as_the_assistants_turn(self):
        c = case(product="api")
        draft = answer(payload(T2, ("product", "eq", "api")))
        msgs = p.messages_for(c, draft, "situala")
        _, (req,) = self.asked(msgs, BaiduReasons(FixedResponses(json.dumps(draft.payload))))
        self.assertEqual([m["role"] for m in req["messages"]],
                         ["system", "user", "assistant", "user"])
        self.assertEqual(req["messages"][2]["content"], p.turn(draft))

    def test_a_failed_parse_is_retried_with_v1s_message(self):
        msgs = p.messages_for(case())
        good = json.dumps(payload(T1, ("severity", "gte", 1)))
        got, reqs = self.asked(msgs, BaiduReasons(FixedResponses("no es json", good)))
        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[1]["messages"][-1], {"role": "user", "content": p.RETRY_MSG})
        self.assertNotIn("response_format", reqs[1])
        self.assertEqual(got.retries, [fm_ask.PARSE])

    def test_a_failed_call_is_retried_with_the_same_messages_after_a_wait(self):
        msgs = p.messages_for(case())
        waits = []
        good = json.dumps(payload(T1, ("severity", "gte", 1)))
        got, reqs = self.asked(msgs, BaiduReasons(Raises({1}, good)), sleep=waits.append)
        self.assertEqual(waits, [10])
        self.assertEqual(reqs[1]["messages"], msgs)
        self.assertEqual(got.retries, [fm_ask.CALL])

    def test_every_attempt_failing_is_a_failed_proposal_with_its_attempts(self):
        with fake_sdk(openai=BaiduReasons(Raises({1, 2, 3}, "{}"))):
            live = p.Live(p.Asker(sleep=lambda s: None))
            with self.assertRaises(e.ProposalFailed) as cm:
                live.ask(p.messages_for(case()))
        self.assertEqual(len(cm.exception.call_attempts), 3)
        self.assertIn("call, call, call", str(cm.exception))

    def test_the_asker_is_plan_first_matchs(self):
        self.assertTrue(issubclass(p.Asker, fm_ask.Asker))
        self.assertIs(p.Asker.ask, fm_ask.Asker.ask)


# ---------------------------------------------------------------------------
# 5. One escalation
# ---------------------------------------------------------------------------

class TestOneEscalation(unittest.TestCase):

    def escalate(self, eng, c, proposer, cause="IMPASSE", idx=7):
        channels: list[str] = []
        return loop.propose_v1b(eng, c, idx, cause, proposer, channels), channels

    def test_with_nothing_to_place_the_rule_is_born_and_its_draft_cites_nothing(self):
        eng = engine_with(KEYWORD)
        draft = payload(T2, ("product", "eq", "api"), ("has_security_keyword", "eq", False),
                        beats=["H02"])
        prop = Scripted(lambda c, i: draft)
        res, _ = self.escalate(eng, case(product="api"), prop)
        self.assertEqual(res["esc"].verdict, e.BORN)
        self.assertEqual([a[0] for a in prop.asked], ["first"])
        self.assertEqual(res["reasons"], [e.OUTSIDE])
        self.assertEqual(len(eng.rules), 2)
        self.assertEqual(eng.edge_log, [])

    def test_the_placement_round_lists_o_in_v2bs_order_and_installs_the_edges(self):
        eng = engine_with(KEYWORD, CATCH_ALL)
        prop = Scripted(lambda c, i: payload(*API),
                        placing(beats=["R0002"], loses_to=["R0001"]))
        res, channels = self.escalate(eng, case(product="api"), prop)
        _, idx, listed, message = prop.asked[1]
        self.assertEqual(listed, v2b.listing(["R0001", "R0002"], 7, 0))
        self.assertEqual(message, v2b.placement_message(eng, listed))
        self.assertEqual(res["esc"].verdict, e.BORN)
        self.assertEqual(sorted(res["reasons"]), [EDGE_OK, EDGE_OK])
        new = eng.rules[-1].rule_id
        self.assertIn("R0001", eng.decl_below[new])          # the crossing edge is entered
        self.assertNotIn(new, eng.decl_below["R0002"])        # the nested one is not
        self.assertEqual(res["esc"].calls[0]["overlapped"], ["R0001", "R0002"])

    def test_a_changed_rule_is_refused_and_not_installed(self):
        eng = engine_with(CATCH_ALL)
        prop = Scripted(lambda c, i: payload(*API),
                        lambda c, d, listed, i: payload(T2, ("product", "eq", "api"),
                                                        ("severity", "eq", 3), beats=listed))
        res, _ = self.escalate(eng, case(product="api"), prop)
        self.assertEqual(res["esc"].verdict, p.CHANGED)
        self.assertEqual(len(eng.rules), 1)

    def test_a_listed_rule_placed_by_the_manuals_number_is_unplaced(self):
        eng = engine_with(CATCH_ALL)
        prop = Scripted(lambda c, i: payload(*API),
                        lambda c, d, listed, i: dict(d.payload, beats=["H29"]))
        res, _ = self.escalate(eng, case(product="api"), prop)
        self.assertEqual(res["esc"].verdict, e.UNPLACED)
        self.assertEqual(res["esc"].calls[-1]["unplaced"], ["R0001"])
        self.assertEqual(len(eng.rules), 1)

    def test_an_order_answer_and_a_rule_off_its_ticket_are_refused(self):
        for pl, verdict in (({"action": T2, "order": [{"winner": "R0001", "loser": "R0002"}]},
                             e.ORDER_WITHOUT_CONFLICT),
                            (payload(T2, ("product", "eq", "billing")), e.REJECTED)):
            eng = engine_with(CATCH_ALL)
            res, _ = self.escalate(eng, case(product="api"), Scripted(lambda c, i, pl=pl: pl))
            with self.subTest(verdict):
                self.assertEqual(res["esc"].verdict, verdict)
                self.assertEqual(len(eng.rules), 1)
                self.assertEqual(res["action"], T2)

    def test_a_copy_is_born_and_placed(self):
        eng = engine_with(API)
        prop = Scripted(lambda c, i: payload(T3, ("product", "eq", "api")),
                        placing(beats="all"))
        res, _ = self.escalate(eng, case(product="api"), prop, cause="ERROR")
        self.assertEqual(res["esc"].verdict, e.BORN)
        self.assertEqual(res["esc"].copy_of, "R0001")
        self.assertEqual(res["esc"].calls[0]["copies"], ["R0001"])
        self.assertIn(eng.rules[-1].rule_id, eng.decl_below["R0001"])

    def test_a_failed_draft_and_a_placement_that_never_came_back(self):
        eng = engine_with(CATCH_ALL)
        res, _ = self.escalate(eng, case(), Scripted(lambda c, i: ProposalError("x")))
        self.assertTrue(res["failed"])
        prop = Scripted(lambda c, i: payload(*API), lambda *a: ProposalError("y"))
        res, _ = self.escalate(eng, case(product="api"), prop)
        self.assertEqual(res["esc"].verdict, e.UNPLACED)
        self.assertEqual(len(eng.rules), 1)


# ---------------------------------------------------------------------------
# 6. The triggers, cover and the cap
# ---------------------------------------------------------------------------

class TestTheTriggers(unittest.TestCase):

    def corpus(self):
        return [case(product="dashboard"), case(product="api"), case(product="api")]

    def labels(self):
        return [(T1, "H29"), (T2, "H16"), (T2, "H16")]

    def proposer(self):
        def draft(c, i):
            return payload(*API) if c.product == "api" else payload(*CATCH_ALL)
        return Scripted(draft, placing(beats="all"))

    def test_the_cause(self):
        w = SimpleNamespace(action=T1)
        self.assertEqual(loop.escalates("i", "IMPASSE", None, T2), "IMPASSE")
        self.assertEqual(loop.escalates("e", "CONFLICT", None, T2), "CONFLICT")
        self.assertIsNone(loop.escalates("i", "ACTION", w, T2))
        self.assertEqual(loop.escalates("e", "ACTION", w, T2), "ERROR")
        self.assertIsNone(loop.escalates("e", "ACTION", w, T1))

    def test_the_impasse_arm_never_asks_where_a_rule_decides_wrongly(self):
        eng = PriorityEngine(space=MI.space())
        res = loop.run_loop(self.corpus(), self.labels(), eng, self.proposer(), "i")
        self.assertEqual([c["cause"] for c in res.causes], ["IMPASSE", None, None])
        self.assertEqual(res.cover, 0)
        self.assertEqual(len(eng.rules), 1)
        self.assertEqual(eng.rules[0].fire_count, 2)
        self.assertEqual([r.correct for r in res.loop.run.records], [True, False, False])

    def test_the_error_arm_asks_and_keeps_what_it_overrode(self):
        eng = PriorityEngine(space=MI.space())
        res = loop.run_loop(self.corpus(), self.labels(), eng, self.proposer(), "e")
        self.assertEqual([c["cause"] for c in res.causes], ["IMPASSE", "ERROR", None])
        self.assertEqual(res.causes[1]["engine_action"], T1)
        self.assertEqual(res.causes[1]["engine_rule"], "R0001")
        self.assertEqual(eng.rules[0].fire_count, 0)        # its decision did not stand
        self.assertEqual([r.correct for r in res.loop.run.records], [True, True, True])
        s = res.summary()
        self.assertEqual(s["arm_escalations"], {"IMPASSE": 1, "CONFLICT": 0, "ERROR": 1})
        self.assertEqual((s["decisions_that_stood"], s["silent_errors_among_them"]), (1, 0))
        rec = loop.record_of(res, eng)
        self.assertEqual([r["cause"] for r in rec["records"]], ["IMPASSE", "ERROR", None])

    def test_the_cap_stops_the_run(self):
        eng = PriorityEngine(space=MI.space())
        res = loop.run_loop(self.corpus(), self.labels(), eng, self.proposer(), "e", cap=1)
        self.assertEqual(res.stopped_at, 0)
        self.assertEqual(len(res.loop.run.records), 1)

    def test_an_unknown_arm_is_refused(self):
        with self.assertRaises(ValueError):
            loop.run_loop([], [], PriorityEngine(space=MI.space()), self.proposer(), "x")


# ---------------------------------------------------------------------------
# 7. The resumable proposer
# ---------------------------------------------------------------------------

class LiveDouble:
    def __init__(self, answers):
        self.answers, self.extra, self.asked = list(answers), {}, []

    def ask(self, messages):
        self.asked.append(messages)
        a = self.answers.pop(0)
        self.extra = a.extra()
        return a


class TestTheResumableProposer(unittest.TestCase):

    def test_a_resume_serves_the_answers_with_what_they_kept(self):
        header = {"plan": "test"}
        a = p.Answer(T1, payload(*CATCH_ALL), None, "stop", 1, [{"provider": "Baidu"}],
                     keys=["action", "conditions"], reasoning="porque", retries=["parse"],
                     served_by="Baidu")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, resumed = erun.open_partial(path, header)
            self.assertFalse(resumed)
            got = p.Resumable(LiveDouble([a]), path, rows).first(case(), idx=0)
            self.assertEqual(got.reasoning, "porque")
            rows, resumed = erun.open_partial(path, header)
            self.assertTrue(resumed)
            live = LiveDouble([])
            again = p.Resumable(live, path, rows).first(case(), idx=0)
            self.assertEqual(live.asked, [])
            self.assertEqual(again.extra(), a.extra())
            self.assertEqual(again.payload, a.payload)
            with self.assertRaises(erun.Desync):
                p.Resumable(LiveDouble([]), path, rows).first(case(severity=1), idx=0)


# ---------------------------------------------------------------------------
# 8. The smoke check
# ---------------------------------------------------------------------------

def smoke_record(**over) -> dict:
    attempt = {"provider": plan.PROVIDER_NAME, "reasoning_tokens": 300, "finish_reason": "stop"}
    calls = [{"round": 0, "failure": None, "call_attempts": [dict(attempt)]},
             {"round": 1, "failure": None, "call_attempts": [dict(attempt)]}]
    rec = {**run.protocol(plan.SMOKE_ARM, plan.SMOKE_N, "smoke"),
           "metrics": {"n_rules": 1}, "escalations": [{"calls": calls}]}
    rec.update(over)
    return rec


class TestTheSmokeCheck(unittest.TestCase):

    def check(self, rec) -> bool:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            path.write_text(json.dumps(rec))
            return run.smoke_check(path)[0]

    def test_a_clean_smoke_run_passes(self):
        self.assertTrue(self.check(smoke_record()))

    def test_each_failure(self):
        bad = smoke_record()
        bad["escalations"][0]["calls"][0]["call_attempts"][0]["provider"] = "Elsewhere"
        quiet = smoke_record()
        quiet["escalations"][0]["calls"][1]["call_attempts"][0]["reasoning_tokens"] = 0
        cut = smoke_record()
        cut["escalations"][0]["calls"][0]["call_attempts"][0]["finish_reason"] = "length"
        unplaced = smoke_record()
        unplaced["escalations"][0]["calls"] = unplaced["escalations"][0]["calls"][:1]
        for name, rec in (("provider", bad), ("reasoning", quiet), ("budget", cut),
                          ("placement", unplaced), ("no rule", smoke_record(metrics={})),
                          ("protocol", smoke_record(n=20))):
            with self.subTest(name):
                self.assertFalse(self.check(rec))


# ---------------------------------------------------------------------------
# 9. Stage C's terms
# ---------------------------------------------------------------------------

def edge(winner, loser, verdict_, older=None, same=False, keyword=False, channel=e.WRITE):
    return {"winner": winner, "loser": loser, "older": older or loser, "younger": winner,
            "channel": channel, "same_queue": same, "keyword": keyword,
            "queues": (T2, T1), "space_out": verdict_}


def a_run(space=F(1, 2), oncall=F(1), drafts=(9, 10), cover=None, edges=()):
    return {"space": space, "oncall": oncall, "drafts": drafts, "cover": cover,
            "covers_early": cover is not None and cover < plan.COVER_BEFORE,
            "edges": list(edges)}


class TestStageC(unittest.TestCase):

    def test_the_direction_is_blind_rows_read_exactly_by_older_rule(self):
        rows = [[edge("R2", "R1", brows.HIT), edge("R3", "R1", brows.MISS),
                 edge("R4", "R5", brows.HIT), edge("R6", "R5", brows.TIE),
                 edge("R7", "R8", brows.HIT, keyword=True),
                 edge("R9", "R8", brows.HIT, same=True)],
                [edge("R2", "R1", brows.MISS)]]
        d = score.direction(rows)
        self.assertEqual((d["units"], d["hits"], d["strict"]), (3, 2, 4))
        self.assertEqual(d["reading"], (F(1, 2) + F(1) + F(0)) / 3)
        self.assertAlmostEqual(float(d["reading"]), d["float_reading"], places=12)

    def test_medians_of_three_and_of_two(self):
        self.assertEqual(score.median([F(1), F(3), F(2)]), F(2))
        self.assertEqual(score.median([F(1), F(2)]), F(3, 2))

    def test_rl_b_counts_runs_and_its_thin_label(self):
        def runs(*covers):
            return {"i": [a_run(cover=c) for c in covers], "e": [a_run(), a_run()]}
        two = score.rl_b(runs(1, 150, None))
        self.assertEqual((two["verdict"], two["thin"]), ("holds", True))
        three = score.rl_b(runs(1, 2, 3))
        self.assertEqual((three["verdict"], three["thin"]), ("holds", False))
        one = score.rl_b(runs(1, 200, None))
        self.assertEqual((one["verdict"], one["thin"]), ("refuted", True))

    def test_rl_c_and_rl_d_read_medians_and_their_thin_labels(self):
        runs = {"i": [a_run(F(1, 10)), a_run(F(2, 10)), a_run(F(3, 10))],
                "e": [a_run(F(85, 100)), a_run(F(95, 100)), a_run(F(99, 100))]}
        c = score.rl_c(runs)
        self.assertEqual(c["value"]["fraction"], str(F(95, 100) - F(2, 10)))
        self.assertFalse(c["thin"])
        d = score.rl_d(runs)
        self.assertEqual((d["verdict"], d["thin"]), ("holds", True))   # 0.85 in its place

    def test_rl_a_pools_and_has_no_value_under_its_minimum(self):
        runs = {"i": [a_run(drafts=(9, 10))] * 2, "e": [a_run(drafts=(9, 10))] * 2}
        self.assertEqual(score.rl_a(runs)["verdict"], "unadjudicable")   # 40 escalations
        runs["e"] = [a_run(drafts=(38, 40))] * 2
        got = score.rl_a(runs)
        self.assertEqual(got["value"]["fraction"], str(F(18 + 76, 20 + 80)))
        self.assertEqual(got["verdict"], "holds")

    def test_an_arm_with_one_run_gives_no_value(self):
        runs = {"i": [a_run()], "e": [a_run(), a_run()]}
        for row in (score.rl_b, score.rl_c, score.rl_a):
            with self.subTest(row.__name__):
                self.assertEqual(row(runs)["verdict"], "unadjudicable")

    def test_rl_e_and_rl_f_have_no_value_under_twenty_units(self):
        runs = {a: [a_run(edges=[edge("R2", "R1", brows.HIT)])] * 2 for a in plan.ARMS}
        e_row, f_row = score.rl_e_f(runs)
        self.assertEqual((e_row["verdict"], f_row["verdict"]),
                         ("unadjudicable", "unadjudicable"))
        self.assertEqual(e_row["units"], 4)

    def test_rl_e_and_rl_f_with_material(self):
        rows = [edge(f"W{k}", f"L{k}", brows.HIT) for k in range(12)]
        runs = {a: [a_run(edges=rows)] * 2 for a in plan.ARMS}
        e_row, f_row = score.rl_e_f(runs)
        self.assertEqual(e_row["value"]["fraction"], "1")
        self.assertEqual(e_row["verdict"], "holds")
        # the Stage C ranking names the T2 rule in every pair, the winner here
        self.assertEqual(f_row["value"]["fraction"], str(F(1) - F(f_row["ranking"]["fraction"])))


# ---------------------------------------------------------------------------
# 10. The instrument on a policy whose answer is known
# ---------------------------------------------------------------------------

class TestTheHiddenPolicyThroughThePath(unittest.TestCase):

    def test_it_is_born_whole_and_decides_both_surfaces_right(self):
        got = references.hidden_through_path()
        self.assertEqual(got["born"], len(references.text_rules()))
        self.assertEqual(set(got["verdicts"]), {EDGE_OK})
        self.assertEqual(got["space"]["correct"], got["space"]["n"])
        self.assertEqual(got["corpus"]["correct"], got["corpus"]["n"])


if __name__ == "__main__":
    unittest.main()
