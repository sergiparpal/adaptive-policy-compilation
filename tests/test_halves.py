"""
`PLAN_HALVES.md`'s package, pinned before the signature.

  * The constants and the lines are the drafted ones, and the four texts are
    §2.1's, byte for byte.
  * The gate reads every signature line, and every writer of the package
    refuses while the plan is unsigned, before it builds, asks or writes.
  * The design: 136 tickets, 544 prompts, the passes, the rarest queue's
    session and the smoke run, rebuilt from their seeds.
  * The request is the loop's first call's with DeepInfra's pin, as the SDK
    double receives it.
  * Stage B keeps every attempt, the provider and the reasoning, never a label;
    it resumes where it stopped, and an outage or a rate limit through every
    wait stops it unrecorded.
  * Stage C's statistics, errors, *thin* and no-value rules, on rows built by
    hand.

**No answer of the model is read here, and none is scored before the
signature**: the only answers are the double's or written by hand.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from authorship import protocol as aprotocol
from authorship import run as erun
from halves import ask, gates, plan, population, prompts, sample, score
from reasoned_loop import protocol as p
from tests.doubles import OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
F = Fraction
RULE = {"action": "T2_TECHNICAL", "conditions": [{"attr": "severity", "op": "eq", "value": 1}],
        "beats": [], "loses_to": [], "note": "una regla"}

E_TEXT = "BASE DE REGLAS: vacia. Esta es la primera regla.\n"
V_TEXT = ("BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este\n"
          "ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues.\n")
H_TEXT = ("BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este\n"
          "ticket.\n")
O_TEXT = ("BASE DE REGLAS: vacia. Esta es la primera regla;\n"
          "si se solapa con reglas existentes de OTRA cola, se te listaran despues.\n")


class DeepInfraShaped(OpenRouterShapedClient):
    """The double, served by the pinned provider, reasoning on every call."""
    PROVIDER = plan.PROVIDER_NAME
    REASONING = "H04 casa el ticket y es la primera; su region entera."

    def _create(self, **kwargs):
        resp = super()._create(**kwargs)
        resp.choices[0].message = SimpleNamespace(content=resp.choices[0].message.content,
                                                  reasoning=self.REASONING)
        resp.usage.completion_tokens_details = SimpleNamespace(reasoning_tokens=321)
        return resp


class RateLimitError(Exception):
    """What `openai` raises on an HTTP 429, by its class name."""


def answers(kwargs) -> str:
    return json.dumps(RULE)


def fake_checks(passes: bool = True, design=None) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED, design=design or population.build())


def small(design: population.Design, k: int = 8) -> population.Design:
    """The design with each session cut to its first `k` asks."""
    return dataclasses.replace(design, sessions={s: v[:k] for s, v in design.sessions.items()})


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


def live(sleep=lambda s: None) -> p.Live:
    return ask.build_live(sleep=sleep)


# ---------------------------------------------------------------------------
# The constants and the texts
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_lines_and_their_sides(self):
        self.assertEqual(plan.LINES, {"HV-a": F(1, 10), "HV-b": F(1, 5), "HV-c": F(0),
                                      "HV-d": F(1, 10), "HV-e": F(1, 10), "HV-f": F(1, 5)})
        self.assertEqual(plan.SIDES, {"HV-a": "within", "HV-b": ">=", "HV-c": ">",
                                      "HV-d": ">=", "HV-e": ">=", "HV-f": ">="})

    def test_the_limits(self):
        self.assertEqual(plan.MAX_INVALID_SHARE, F(1, 20))
        self.assertEqual(plan.HV_A_MIN_TICKETS, 50)
        self.assertEqual(plan.HV_C_MIN_GAP, F(1, 10))
        self.assertEqual(plan.HV_F_MIN_TICKETS, 5)
        self.assertEqual(plan.MAX_CONSECUTIVE_FAILURES, 5)
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_sessions_and_the_seed(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "pass1", "pass2", "oncall"))
        self.assertEqual(plan.PASSES, ("pass1", "pass2"))
        self.assertEqual((plan.SMOKE_PER_ARM, plan.ONCALL_REPEATS, plan.ORDER_SEED), (2, 4, 83))

    def test_the_tickets(self):
        self.assertEqual(len(plan.TICKETS), plan.N_TICKETS)
        self.assertEqual(plan.N_TICKETS, 136)
        self.assertEqual(list(plan.TICKETS), sorted(set(plan.TICKETS)))
        self.assertEqual(hashlib.sha256(json.dumps(list(plan.TICKETS)).encode())
                         .hexdigest()[:16], "0fe4b09ac90e3ec2")
        self.assertEqual(plan.ONCALL, (257, 710, 954, 982, 1432, 1783, 1951))
        self.assertEqual(plan.ADDED, (954, 982, 1432))
        self.assertTrue(set(plan.ONCALL) <= set(plan.TICKETS))
        self.assertEqual((plan.RULE_ARM_TICKETS, plan.SHARED), (171, 133))

    def test_the_request_is_the_loops_with_deepinfras_pin(self):
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, "DeepInfra")
        self.assertEqual(plan.MODEL, "deepseek/deepseek-v4-flash")
        self.assertEqual(plan.TEMPERATURE, 0)
        self.assertEqual(plan.settings(), {"reasoning": {"effort": "high"}, "max_tokens": 16000})
        self.assertEqual((plan.N, plan.SEED, plan.LEVEL), (2000, 17, 3))

    def test_the_paths_follow_out(self):
        with TempOut() as d:
            self.assertEqual(plan.ask_path("oncall"), d / "ask_oncall.json")
            self.assertEqual(plan.partial_path("pass1"), d / "ask_pass1.partial.jsonl")
            self.assertEqual(plan.sample_path(), d / "sample.json")
        with self.assertRaises(ValueError):
            plan.ask_path("pass3")


class TestTheFourTexts(unittest.TestCase):

    def test_byte_for_byte(self):
        self.assertEqual(prompts.PARAGRAPHS, {"e": E_TEXT, "v": V_TEXT, "h": H_TEXT,
                                              "o": O_TEXT})

    def test_cut_and_joined_at_the_semicolon(self):
        head, clause = V_TEXT.split("; ")
        self.assertEqual(H_TEXT, head + ".\n")
        self.assertEqual(O_TEXT, E_TEXT[:-2] + ";\n" + clause)

    def test_they_name_no_queue_and_no_rule(self):
        self.assertTrue(gates.the_halves()["passes"])

    def test_every_arm_sends_the_loops_system_prompt_and_its_paragraph(self):
        case = population.build().asks["v:710"].case
        for arm in prompts.ARMS:
            with self.subTest(arm):
                self.assertEqual(prompts.system_prompt(arm), p.SYSTEM_PROMPT)
                self.assertTrue(prompts.user_message(arm, case)
                                .startswith(prompts.PARAGRAPHS[arm] + "\nTICKET EN IMPASSE:\n"))
        self.assertEqual(prompts.ask("v", 710, case).messages(), p.messages_for(case))

    def test_a_repetition_asks_its_prompt(self):
        a = prompts.ask("h", 710, population.build().asks["h:710"].case, 3)
        self.assertEqual((a.id, a.prompt), ("h:710#3", "h:710"))
        with self.assertRaises(ValueError):
            prompts.ask_id("x", 1)


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_blank_signed_and_a_blank_second_line(self):
        cases = (("**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-11-10)**\n", True),
                 ("**Signed by Sergi: Sergi Parpal (date: 2026-11-10)**\n"
                  "**Signed by Sergi: ____ (date: ____)**\n", False),
                 ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "PLAN.md"
            for text, ok in cases:
                path.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(path)["passes"], ok)

    def test_the_plan_carries_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned here: a
        test that pinned the draft's blank line would fail at the signature,
        as two of `PLAN_APPLY.md`'s did on 2026-10-23."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_HALVES.md")["found"],
                         plan.MIN_SIGNATURES)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "build_live",
                               side_effect=AssertionError("asker built")) as built, \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        for m in (checks, built, fetch, write):
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
             mock.patch.object(ask, "build_live",
                               side_effect=AssertionError("asker built")) as built, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        for m in (fetch, built, write):
            m.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            for main in (ask.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 1)

    def test_a_session_out_of_its_turn_refuses_before_the_key(self):
        with TempOut(), \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks:
            for s in ("pass1", "pass2", "oncall"):
                with self.subTest(s), self.assertRaises(SystemExit):
                    ask.main(["--session", s])
        fetch.assert_not_called()
        checks.assert_not_called()


# ---------------------------------------------------------------------------
# The design
# ---------------------------------------------------------------------------

class TestTheDesign(unittest.TestCase):

    def setUp(self):
        self.design = population.build()

    def test_the_counts(self):
        base = [a for a in self.design.asks.values() if a.rep == 0]
        reps = [a for a in self.design.asks.values() if a.rep]
        self.assertEqual(len(base), 544)
        self.assertEqual(len(reps), 112)
        for arm in prompts.ARMS:
            with self.subTest(arm):
                self.assertEqual(len(self.design.prompts_of(arm)), 136)
        self.assertEqual({s: len(v) for s, v in self.design.sessions.items()},
                         {"smoke": 8, "pass1": 544, "pass2": 544, "oncall": 112})

    def test_the_sessions(self):
        self.assertTrue(gates.asks_and_sessions(self.design)["passes"])

    def test_the_orders_come_back_from_the_seed(self):
        self.assertEqual(population.sessions_for(plan.TICKETS), self.design.sessions)

    def test_the_texts_check(self):
        self.assertTrue(gates.one_paragraph_apart(self.design)["passes"])
        self.assertTrue(gates.builders()["passes"])
        self.assertTrue(gates.digests(self.design)["passes"])

    def test_the_asker_path_names_no_label(self):
        self.assertTrue(gates.no_label_on_the_asker_path()["passes"])

    def test_the_guard(self):
        self.assertTrue(gates.the_guard()["passes"])


# ---------------------------------------------------------------------------
# The request, and Stage B
# ---------------------------------------------------------------------------

class TestTheRequest(unittest.TestCase):

    def test_what_the_sdk_receives(self):
        a = population.build().asks["h:710"]
        client = DeepInfraShaped(answers)
        with fake_sdk(openai=client):
            got = live().ask(a.messages())
        self.assertEqual(got.payload, RULE)
        sent = client.peticiones[0]
        self.assertEqual(sent["model"], plan.MODEL)
        self.assertEqual(sent["messages"], a.messages())
        self.assertEqual(sent["temperature"], plan.TEMPERATURE)
        self.assertEqual(sent["max_tokens"], plan.MAX_TOKENS)
        self.assertEqual(sent["extra_body"], {"reasoning": plan.REASONING,
                                              "provider": plan.PROVIDER})
        self.assertEqual(sent["response_format"], {"type": "json_object"})


class Interrupting:
    """A `Live` that raises after `n` asks, as a ^C does."""

    def __init__(self, inner, n: int):
        self.inner, self.n, self.k = inner, n, 0

    def ask(self, messages):
        self.k += 1
        if self.k == self.n:
            raise KeyboardInterrupt
        return self.inner.ask(messages)


class Failing:
    def ask(self, messages):
        raise aprotocol.ProposalFailed("failed", None, 3, [])


class TestStageB(unittest.TestCase):

    def setUp(self):
        self.design = small(population.build())

    def run_session(self, out: Path, session: str, asker) -> tuple[list, list]:
        header = {"protocol": json.loads(json.dumps(ask.protocol())), "session": session,
                  "sample_sha256": "x"}
        return ask.ask(session, self.design, asker, out / f"{session}.jsonl", header)

    def test_a_pass_keeps_the_attempts_the_provider_the_reasoning_and_no_label(self):
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=DeepInfraShaped(answers)), \
             mock.patch("builtins.print"):
            rows, resumed = self.run_session(Path(d), "pass1", live())
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(resumed, [])
        for r in rows:
            with self.subTest(r["id"]):
                self.assertTrue(r["valid"])
                self.assertEqual(r["served_by"], plan.PROVIDER_NAME)
                self.assertEqual(r["digest"], self.design.asks[r["id"]].digest)
                self.assertEqual(r["payload"], RULE)
                self.assertEqual(r["reasoning"], DeepInfraShaped.REASONING)
                self.assertEqual(r["call_attempts"][-1]["reasoning_tokens"], 321)
                self.assertFalse({"truth", "truth_rule", "correct", "class"} & set(r))

    def test_an_answer_from_another_provider_is_invalid(self):
        with tempfile.TemporaryDirectory() as d, \
             fake_sdk(openai=OpenRouterShapedClient(answers)), mock.patch("builtins.print"):
            rows, _ = self.run_session(Path(d), "pass1", live())
        self.assertTrue(rows)
        self.assertFalse(any(r["valid"] for r in rows))

    def test_an_interrupted_session_resumes_where_it_stopped(self):
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=DeepInfraShaped(answers)), \
             mock.patch("builtins.print"):
            with self.assertRaises(KeyboardInterrupt):
                self.run_session(Path(d), "pass1", Interrupting(live(), 4))
            rows, resumed = self.run_session(Path(d), "pass1", live())
        self.assertEqual([r["id"] for r in rows], self.design.sessions["pass1"])
        self.assertEqual(len(resumed), 1)

    def test_an_outage_stops_the_session_without_recording_it(self):
        with tempfile.TemporaryDirectory() as d, mock.patch("builtins.print"):
            with self.assertRaises(ask.Outage):
                self.run_session(Path(d), "pass1", Failing())
            lines = (Path(d) / "pass1.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)          # the header, and no failure

    def test_a_rate_limit_through_every_wait_stops_it_unrecorded(self):
        def refused(kwargs):
            raise RateLimitError("Error code: 429")

        waits = []
        with tempfile.TemporaryDirectory() as d, fake_sdk(openai=DeepInfraShaped(refused)), \
             mock.patch("builtins.print"):
            with self.assertRaises(erun.Outage):
                self.run_session(Path(d), "pass1", live(sleep=waits.append))
            lines = (Path(d) / "pass1.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)
        for w in plan.RATE_LIMIT_WAIT:
            self.assertIn(w, waits)

    def test_the_smoke_run_end_to_end_and_the_turns(self):
        with TempOut(), fake_sdk(openai=DeepInfraShaped(answers)), \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info", return_value=API_KEY), \
             mock.patch.object(gates, "run_checks",
                               return_value=fake_checks(design=self.design)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(ask, "sample_matches", return_value=(True, "the design")), \
             mock.patch.object(ask, "sample_sha256", return_value="x"), \
             mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-double"}), \
             mock.patch("builtins.print"):
            self.assertEqual(ask.main(["--session", "smoke"]), 0)
            ok, why = ask.smoke_check()
            self.assertTrue(ok, why)
            self.assertTrue(ask.turn_check("pass1")[0])
            self.assertFalse(ask.turn_check("pass2")[0])
            self.assertFalse(ask.turn_check("oncall")[0])
            rec = json.loads(plan.ask_path("smoke").read_text())
            self.assertEqual(rec["paragraphs"], prompts.PARAGRAPHS)
            self.assertEqual(rec["provider"], plan.PROVIDER)
            self.assertFalse(plan.partial_path("smoke").exists())
            with self.assertRaises(SystemExit):     # never over a paid record
                ask.main(["--session", "smoke"])


class TestTheSmokeCheck(unittest.TestCase):

    def record(self, **row) -> dict:
        base = {"arm": "e", "valid": True,
                "call_attempts": [{"provider": plan.PROVIDER_NAME, "finish_reason": "stop",
                                   "reasoning_tokens": 9, "error": None}]}
        rows = [{**base, "arm": a} for a in prompts.ARMS]
        rows[0] = {**rows[0], **row}
        return {**json.loads(json.dumps(ask.protocol())), "rows": rows}

    def check(self, rec: dict) -> bool:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            path.write_text(json.dumps(rec))
            return ask.smoke_check(path)[0]

    def test_it_passes_and_fails_where_it_should(self):
        self.assertTrue(self.check(self.record()))
        self.assertFalse(self.check(self.record(valid=False)))
        attempt = {"provider": plan.PROVIDER_NAME, "finish_reason": "stop", "error": None}
        self.assertFalse(self.check(self.record(call_attempts=[{**attempt, "reasoning_tokens": 0}])))
        self.assertFalse(self.check(self.record(call_attempts=[
            {**attempt, "reasoning_tokens": 9, "finish_reason": "length"}])))
        self.assertFalse(self.check(self.record(call_attempts=[
            {**attempt, "reasoning_tokens": 9, "provider": "Baidu"}])))
        # an attempt refused for the rate never reached the model, and is not read
        self.assertTrue(self.check(self.record(call_attempts=[
            {"provider": None, "error": plan.RATE_LIMITED},
            {**attempt, "reasoning_tokens": 9}])))
        rec = self.record()
        rec["provider"] = {"order": ["baidu"], "allow_fallbacks": False}
        self.assertFalse(self.check(rec))


# ---------------------------------------------------------------------------
# Stage C, on rows built by hand
# ---------------------------------------------------------------------------

def row(arm: str, ticket: int, cls: str | None, session: str = "pass1", valid: bool = True,
        rep: int = 0) -> dict:
    return {"arm": arm, "ticket": ticket, "session": session, "valid": valid and cls is not None,
            "class": cls if valid else None, "prompt": f"{arm}:{ticket}", "rep": rep,
            "payload": dict(RULE)}


def rows_for(shares: dict[str, list[str]], tickets, sessions=("pass1", "pass2")) -> list[dict]:
    """Each arm's classes at every ticket, in every session."""
    return [row(a, t, c, s) for a, cs in shares.items() for t, c in zip(tickets, cs)
            for s in sessions]


class TestStageC(unittest.TestCase):

    def setUp(self):
        self.T = list(plan.TICKETS)

    def classes(self, whole: int, n: int = 136) -> list[str]:
        return ["whole"] * whole + ["cut_by_one"] * (n - whole)

    def test_holds_reads_each_side(self):
        self.assertTrue(score.holds("HV-b", F(1, 5)))
        self.assertFalse(score.holds("HV-b", F(1, 5) - F(1, 1000)))
        self.assertFalse(score.holds("HV-c", F(0)))
        self.assertTrue(score.holds("HV-c", F(1, 1000)))
        self.assertTrue(score.holds("HV-a", F(1, 10)) and score.holds("HV-a", F(-1, 10)))
        self.assertFalse(score.holds("HV-a", F(11, 100)))

    def test_a_contrast_is_exact_and_its_error_is_the_clustered_one(self):
        rows = rows_for({"e": self.classes(110), "v": self.classes(50)}, self.T)
        tal = score.tally(rows, ("e", "v"), self.T, plan.PASSES)
        value, se = score.contrast(score.COEFFS["HV-b"], tal)
        self.assertEqual(value, F(110, 136) - F(50, 136))
        # by hand: u_t = (h_e − W_e r_e)/R_e − (h_v − W_v r_v)/R_v, two answers a ticket
        we, wv, re_, rv = F(110, 136), F(50, 136), 272, 272
        u = [(2 * (i < 110) - float(we) * 2) / re_ - (2 * (i < 50) - float(wv) * 2) / rv
             for i in range(136)]
        self.assertAlmostEqual(se, math.sqrt(136 / 135 * sum(x * x for x in u)), places=12)

    def test_hv_b_holds_and_is_not_thin_far_from_its_line(self):
        rows = rows_for({"e": self.classes(110), "v": self.classes(50)}, self.T)
        v = score.contrast_row("HV-b", rows)
        self.assertEqual(v["verdict"], score.HOLDS)
        self.assertFalse(v["thin"])
        self.assertEqual(v["value"]["fraction"], str(F(60, 136)))

    def test_a_pass_alone_on_the_other_side_makes_it_thin(self):
        rows = (rows_for({"e": self.classes(110), "v": self.classes(50)}, self.T, ("pass1",))
                + rows_for({"e": self.classes(60), "v": self.classes(50)}, self.T, ("pass2",)))
        v = score.contrast_row("HV-b", rows)
        self.assertEqual(v["verdict"], score.HOLDS)     # 35/136 pooled, over a fifth
        self.assertTrue(v["thin"])

    def test_too_many_invalid_answers_leave_no_value(self):
        rows = rows_for({"e": self.classes(110), "v": self.classes(50)}, self.T)
        for r in rows[:28]:                              # 28 of 544, over a twentieth
            r["valid"], r["class"] = False, None
        self.assertEqual(score.contrast_row("HV-b", rows)["verdict"], score.NO_VALUE)
        for r in rows[:27]:
            r["valid"], r["class"] = True, "whole"
        self.assertNotEqual(score.contrast_row("HV-b", rows)["verdict"], score.NO_VALUE)

    def test_hv_c_needs_a_gap_to_divide(self):
        small_gap = rows_for({"e": self.classes(100), "v": self.classes(90),
                              "h": self.classes(99)}, self.T)
        self.assertEqual(score.contrast_row("HV-c", small_gap)["verdict"], score.NO_VALUE)
        gap = rows_for({"e": self.classes(110), "v": self.classes(50),
                        "h": self.classes(100)}, self.T)
        v = score.contrast_row("HV-c", gap)
        self.assertEqual(v["verdict"], score.HOLDS)
        self.assertEqual(v["value"]["fraction"], str(F(100, 136) - F(80, 136)))

    def test_hv_f_reads_the_seven_with_the_session_and_leaves_one_out(self):
        seven = list(plan.ONCALL)
        sessions = ("pass1", "pass2", "oncall")
        rows = rows_for({"h": ["whole"] * 6 + ["cut_by_one"], "v": ["cut_by_one"] * 7},
                        seven, sessions)
        v = score.contrast_row("HV-f", rows)
        self.assertEqual(v["verdict"], score.HOLDS)
        self.assertEqual(v["value"]["fraction"], "6/7")
        self.assertEqual(set(v["leaving_one_ticket_out"]), {str(t) for t in seven})
        few = rows_for({"h": ["whole"] * 4 + [None] * 3, "v": ["cut_by_one"] * 7},
                       seven, sessions)
        self.assertEqual(score.contrast_row("HV-f", few)["verdict"], score.NO_VALUE)

    def test_hv_a_reads_ticket_by_ticket_and_needs_fifty(self):
        comparator = {str(t): {"answers": 2, "right_queue": 2, "whole": 1} for t in self.T[:60]}
        rows = rows_for({"v": ["whole"] * 136}, self.T)
        v = score.hv_a(rows, comparator)
        self.assertEqual(v["verdict"], score.REFUTED)    # 1 − 1/2 at every ticket
        self.assertEqual(v["value"]["fraction"], "1/2")
        self.assertEqual(v["tickets"], 60)
        few = {k: comparator[k] for k in list(comparator)[:49]}
        self.assertEqual(score.hv_a(rows, few)["verdict"], score.NO_VALUE)
        level = rows_for({"v": ["whole", "cut_by_one"] * 68}, self.T)
        half = {str(t): {"answers": 2, "right_queue": 2, "whole": 2 if i % 2 == 0 else 0}
                for i, t in enumerate(self.T[:60])}
        self.assertEqual(score.hv_a(level, half)["verdict"], score.HOLDS)

    def test_the_scorer_end_to_end_on_a_hand_written_rule(self):
        """Every session's every ask answered with one rule written by hand, and
        a Stage A record whose references are invented: the scorer runs through,
        and every row and the reported block come out with a verdict or a
        reason."""
        design = population.build()
        records = {}
        for s in score.WITH_ONCALL:
            rows = []
            for k, aid in enumerate(design.sessions[s]):
                a = design.asks[aid]
                rows.append({"session": s, "position": k, "id": aid, "prompt": a.prompt,
                             "arm": a.arm, "ticket": a.ticket, "rep": a.rep,
                             "valid": True, "payload": dict(RULE), "served_by": plan.PROVIDER_NAME,
                             "call_attempts": [{"provider": plan.PROVIDER_NAME,
                                                "finish_reason": "stop", "error": None,
                                                "prompt_tokens": 1762, "completion_tokens": 5000,
                                                "reasoning_tokens": 4800}],
                             "retries": [], "seconds": 90.0, "failure": None})
            records[s] = {"rows": rows}
        refs = {str(t): {"answers": 2, "right_queue": 2, "whole": 1} for t in plan.TICKETS}
        sample_rec = {"references": {"hv_a_comparator": refs,
                                     "rule_arm": {str(t): ["whole"] for t in plan.TICKETS[:5]},
                                     "loops": {g: {str(t): ["cut_by_one"] for t in plan.TICKETS[:5]}
                                               for g in plan.LOOP_GROUPS}},
                      "tickets": {str(t): {"governing": "H00", "queue": "Q"}
                                  for t in plan.TICKETS}}
        got = score.score(records, sample_rec)
        self.assertEqual(set(got["verdicts"]), set(plan.ROWS))
        for rid, v in got["verdicts"].items():
            with self.subTest(rid):
                self.assertIn(v["verdict"], (score.HOLDS, score.REFUTED, score.NO_VALUE))
        self.assertEqual(set(got["HV-g"]["calls"]), set(score.WITH_ONCALL))
        json.dumps(got, default=str)

    def test_validity_is_section_zeros(self):
        """An empty object from the pinned provider is valid, and its class is no
        rule; a failed call and another provider's answer are not valid. The
        asker's flag is kept beside §0's."""
        t = plan.TICKETS[0]
        base = {"ticket": t, "arm": "e", "prompt": f"e:{t}", "rep": 0,
                "served_by": plan.PROVIDER_NAME, "failure": None}
        rows = [{**base, "id": "empty", "payload": {}, "action": None, "valid": False},
                {**base, "id": "rule", "payload": dict(RULE), "action": RULE["action"],
                 "valid": True},
                {**base, "id": "failed", "payload": None, "action": None, "valid": False,
                 "failure": "RuntimeError: 429"},
                {**base, "id": "elsewhere", "payload": dict(RULE), "action": RULE["action"],
                 "valid": False, "served_by": "Baidu"}]
        got = {r["id"]: r for r in score.classed_rows({"pass1": {"rows": rows}})}
        self.assertTrue(got["empty"]["valid"])
        self.assertEqual(got["empty"]["class"], "no_rule")
        self.assertFalse(got["empty"]["valid_as_recorded"])
        self.assertTrue(got["rule"]["valid"])
        self.assertIsNotNone(got["rule"]["class"])
        for rid in ("failed", "elsewhere"):
            with self.subTest(rid):
                self.assertFalse(got[rid]["valid"])
                self.assertIsNone(got[rid]["class"])
        flag = score.askers_flag(list(got.values()))
        self.assertEqual(flag["e"], {"answers": 1, "classes": {"no_rule": 1}})
        # an empty object is not invalid, so it does not count toward no value
        self.assertEqual(score.invalid_share(list(got.values()), ("e",), [t], ("pass1",)),
                         F(2, 4))

    def test_wrong_queue_and_no_rule_leave_the_share(self):
        rows = [row("e", 1, "whole"), row("e", 2, "wrong_queue"), row("e", 3, "no_rule"),
                row("e", 4, "other")]
        tal = score.tally(rows, ("e",), [1, 2, 3, 4], ("pass1",))
        self.assertEqual(score.share(tal["e"]), F(1, 2))


if __name__ == "__main__":
    unittest.main()
