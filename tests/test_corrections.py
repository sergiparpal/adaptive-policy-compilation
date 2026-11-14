"""
The `PLAN_CORRECTIONS.md` instrument, before any of its figures exists.

What is pinned:

* §2's constants, with the client and the pin imported from `PLAN_PLACEMENT.md`;
  level 1; the seed the next prime after 107; §0's lines as exact fractions on
  their own sides; `DECLARED`; the schedule; the checkpoints; and the gate
  counting every signature line, without pinning whether the plan is signed.
* The report: its digest, the one queue it names, quoted in the plan.
* The messages: with level 3's system prompt and no report, v1c's; with the
  report, v1c's but for the paragraph; at level 1, v1c's but for the system
  prompt.
* **The label's route.** On a corpus built by hand, arm `l`'s proposer is handed
  the reported case's label at that case's two calls and nowhere else. Arm `n`'s
  is handed none, and the two arms' records are the same.
* The at-once asks: with no label, `PLAN_MANUAL.md`'s level-1 compile messages;
  the labels read off an L record and refused when they are not its reported
  errors'; the design, the re-asks and the validity flag, on an empty object
  first.
* The learners' plumbing; Stage C's exact lines, medians, thin labels and every
  reason a row has no value; nothing built, asked or written unsigned.

**No figure of the plan.** The learners are run on labels made up here, not on
any run's, and no row is read on a record of the plan.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from harness.domain import ACTIONS, Case, generate_corpus

from authorship import run as erun
from manual import instrument as MI
from manual import prompts as mprompts
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import user_msg

from corrections import ask, gates, learners, loop, plan, prompts, protocol, run, score

REPO = Path(__file__).resolve().parent.parent
F = Fraction
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


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


class LiveScript:
    """A live model that answers what it is handed, one per call, and keeps
    every message list it was sent."""

    def __init__(self, *items):
        self.items, self.extra, self.sent = list(items), {}, []

    def ask(self, messages):
        self.sent.append(messages)
        got = self.items.pop(0)
        if isinstance(got, Exception):
            raise got
        self.extra = got.extra()
        return got


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstants(unittest.TestCase):

    def test_the_client_and_the_pin_are_plan_placements(self):
        for name in ("MODEL", "PROMPT", "TEMPERATURE", "REASONING", "MAX_TOKENS",
                     "MAX_RETRIES", "CALL_RETRY_WAIT", "RATE_LIMITED", "RATE_LIMIT_WAIT",
                     "PROVIDER", "PROVIDER_NAME", "COVERAGE", "N", "SEED"):
            with self.subTest(name):
                self.assertEqual(getattr(plan, name), getattr(pl_plan, name))
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual(plan.settings(), pl_plan.settings())
        self.assertEqual(plan.at_once_settings(),
                         {**pl_plan.settings(), "max_tokens": 32000})

    def test_level_one_and_the_arms(self):
        self.assertEqual(plan.LEVEL, 1)
        self.assertEqual(plan.ARMS, ("n", "l"))
        self.assertEqual(plan.LABELLED, "l")
        self.assertEqual((plan.REPS, plan.SMOKE_N, plan.SMOKE_ARMS, plan.MAX_ESCALATIONS),
                         (3, 30, ("n", "l"), 400))
        self.assertEqual(plan.SYSTEM_PROMPT_SHA16, sha16(mprompts.loop_system_prompt(1)))
        self.assertEqual(plan.COMPILE_PROMPT_SHA16, sha16(mprompts.compile_system_prompt(1)))

    def test_the_seed_is_the_next_prime_after_107_and_no_other_threads(self):
        self.assertEqual(plan.ORDER_SEED, 109)
        used = []
        for f in REPO.glob("*/plan.py"):
            if f.parent.name == "corrections":
                continue
            if "= 109\n" in f.read_text() or "= 109 " in f.read_text():
                used.append(str(f))
        self.assertEqual(used, [])

    def test_the_lines_are_section_0s_as_fractions_on_their_sides(self):
        self.assertEqual(plan.LINES, {"CR-a": F(19, 20), "CR-b": F(1, 10), "CR-c": F(1, 4),
                                      "CR-d": F(0), "CR-e": F(0), "CR-f": F(9, 10)})
        self.assertEqual(plan.SIDES, {"CR-a": ">=", "CR-b": ">=", "CR-c": ">=",
                                      "CR-d": ">=", "CR-e": ">", "CR-f": ">="})
        self.assertTrue(all(isinstance(v, Fraction) for v in plan.LINES.values()))

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        self.assertEqual([list(x) for x in plan.schedule()], plan.DECLARED["schedule"])
        arms = [a for a, _ in plan.schedule()]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))

    def test_the_at_once_constants(self):
        self.assertEqual(plan.CHECKPOINTS, (10, 20, 40, 80, 160, 320))
        self.assertEqual((plan.ASKS_PER_CHECKPOINT, plan.PRIOR_ASKS, plan.SMOKE_ASKS,
                          plan.WORKERS, plan.MAX_REASKS, plan.AT_ONCE_MAX_TOKENS),
                         (3, 5, 2, 4, 2, 32000))

    def test_the_checkpoints_a_run_reaches(self):
        self.assertEqual(plan.checkpoints(0), [])
        self.assertEqual(plan.checkpoints(7), [7])
        self.assertEqual(plan.checkpoints(10), [10])
        self.assertEqual(plan.checkpoints(45), [10, 20, 40, 45])
        self.assertEqual(plan.checkpoints(320), [10, 20, 40, 80, 160, 320])
        self.assertEqual(plan.checkpoints(400), [10, 20, 40, 80, 160, 320, 400])

    def test_both_arms_read_plan_placements_draws(self):
        for arm, rep in plan.schedule():
            self.assertEqual(plan.channel_of(arm, rep), pl_plan.channel_of("v1c", rep))
        self.assertEqual(plan.stream("l", None), "smoke")

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            self.assertEqual(plan.run_path("l", 2), d / "loop_l_r2.json")
            self.assertEqual(plan.smoke_path("n"), d / "loop_smoke_n.json")
            self.assertEqual(plan.ask_path("l_r3"), d / "atonce_l_r3.json")
            self.assertEqual(plan.ask_partial_path("prior"), d / "atonce_prior.partial.jsonl")
            self.assertEqual(plan.session_of(1), "l_r1")
            with self.assertRaises(ValueError):
                plan.ask_path("n_r1")
            with self.assertRaises(ValueError):
                plan.run_path("v1c", 1)


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_every_line_is_counted_and_one_is_needed(self):
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-13)**\n"
        blank = "**Signed by Sergi: ________ (date: ________)**\n"
        cases = ((blank, False), (signed, True), (signed + blank, False),
                 (signed * 2, True), ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "PLAN.md"
            for text, ok in cases:
                path.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(path)["passes"], ok)

    def test_the_plan_carries_its_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_CORRECTIONS.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_CORRECTIONS.md"))


# ---------------------------------------------------------------------------
# 2. The report and the messages
# ---------------------------------------------------------------------------

class TestTheReport(unittest.TestCase):

    def test_its_digest_and_the_one_queue_it_names(self):
        self.assertEqual(sha16(protocol.REPORT), plan.REPORT_SHA16)
        self.assertTrue(protocol.REPORT.isascii() and protocol.REPORT.endswith("\n"))
        self.assertEqual(protocol.queues_named(protocol.REPORT), [])
        self.assertTrue(protocol.names_no_rule(protocol.REPORT))
        for q in ACTIONS:
            with self.subTest(q):
                self.assertEqual(protocol.queues_named(protocol.report(q)), [q])
        with self.assertRaises(protocol.NotAQueue):
            protocol.report("H07")

    def test_the_plan_quotes_it_and_the_header_byte_for_byte(self):
        self.assertTrue(gates.quoted_in_the_plan(protocol.REPORT))
        self.assertTrue(gates.quoted_in_the_plan(prompts.HEADER))


class TestTheMessages(unittest.TestCase):

    def setUp(self):
        self.c, self.draft = case(product="api"), answer(payload(T2, ("product", "eq", "api")))

    def test_level_3_and_no_report_give_v1cs_messages_back(self):
        self.assertEqual(protocol.messages_for(self.c, system=p.SYSTEM_PROMPT),
                         p.messages_for(self.c))
        self.assertEqual(protocol.messages_for(self.c, self.draft, "lista",
                                               system=p.SYSTEM_PROMPT),
                         p.messages_for(self.c, self.draft, "lista"))

    def test_the_report_stands_right_after_v2bs_paragraph(self):
        without = protocol.messages_for(self.c, self.draft, "lista")
        with_ = protocol.messages_for(self.c, self.draft, "lista", queue=T3)
        self.assertTrue(protocol.one_report_apart(without, with_, T3))
        self.assertFalse(protocol.one_report_apart(without, with_, T1))
        self.assertFalse(protocol.one_report_apart(without, without, T3))
        self.assertEqual(with_[1]["content"],
                         user_msg(self.c, p.BLIND_BASE + "\n" + protocol.report(T3)))

    def test_level_1_changes_the_system_prompt_alone(self):
        at1 = protocol.messages_for(self.c, self.draft, "lista")
        at3 = protocol.messages_for(self.c, self.draft, "lista", system=p.SYSTEM_PROMPT)
        self.assertEqual(at1[1:], at3[1:])
        self.assertEqual(at1[0]["content"], mprompts.loop_system_prompt(1))

    def test_the_texts_digests_and_fingerprints(self):
        n, l = protocol.digests("n"), protocol.digests("l")
        self.assertEqual(sorted(l), sorted([*n, "report"]))
        self.assertEqual({k: v for k, v in l.items() if k != "report"}, n)
        for k in ("blind_base", "placement_template", "retry_message"):
            self.assertEqual(n[k], p.digests()[k])
        self.assertNotEqual(protocol.fingerprint("n"), protocol.fingerprint("l"))
        with self.assertRaises(ValueError):
            protocol.texts("v1c")


# ---------------------------------------------------------------------------
# 3. The label's route
# ---------------------------------------------------------------------------

API = (T2, ("product", "eq", "api"))
SEVERE = (T3, ("severity", "lte", 2))


def corpus() -> list[Case]:
    """Case 0 is an impasse on the empty base, which writes the API rule. Case
    1 is decided by it, wrongly, and its draw makes it reportable, so it
    escalates as a reported error; its draft crosses the API rule, so v1c's
    list holds it and a placement round is sent."""
    return [case(product="api"), case(product="api", severity=1)]


LABELS = [(T2, "H16"), (T3, "H07")]
DRAWS = [0.9, 0.1]


def looped(arm: str, d: Path):
    live = LiveScript(answer(payload(*API)), answer(payload(*SEVERE)),
                      answer(payload(*SEVERE, beats=["R0001"])))
    path = d / f"{arm}.partial.jsonl"
    rows, _ = erun.open_partial(path, {"plan": "test", "arm": arm})
    prop = protocol.PROPOSERS[arm](live, path, rows)
    eng = PriorityEngine(space=MI.space())
    res = loop.run_loop(corpus(), LABELS, eng, prop, arm, DRAWS, clock=lambda: 0.0)
    prop.flush()
    return gates.as_json(loop.record_of(res, eng)), live.sent, prop


class TestTheLabelsRoute(unittest.TestCase):

    def test_the_label_reaches_the_reported_case_alone_and_only_in_arm_l(self):
        with tempfile.TemporaryDirectory() as d:
            rec_n, sent_n, prop_n = looped("n", Path(d))
            rec_l, sent_l, prop_l = looped("l", Path(d))
        self.assertEqual(rec_n, rec_l)
        self.assertEqual([esc["kind"] for esc in rec_l["escalations"]], ["IMPASSE", "ERROR"])
        self.assertEqual(loop.reports_handed(prop_n), {})
        self.assertEqual(loop.reports_handed(prop_l), {"1": T3})
        self.assertEqual([len(m) for m in sent_l], [2, 2, 4])
        self.assertEqual(sent_l[0], sent_n[0])
        for k in (1, 2):
            self.assertTrue(protocol.one_report_apart(sent_n[k], sent_l[k], T3))
        for m in sent_n:
            self.assertNotIn("AVISO DE REVISION", json.dumps(m))

    def test_the_label_is_the_cases_own(self):
        """The wrapper writes `labels[idx][0]`, the label the trigger read."""
        seen = []

        def fake_v1c(engine, case_, idx, cause, proposer, channels, clock=None):
            seen.append(dict(proposer.reports))
            return {}

        with mock.patch.object(pl_protocol, "propose_v1c", fake_v1c):
            prop = type("P", (), {"reports": {}})()
            propose = loop.propose_for("l", [(T1, "H29"), (T3, "H07"), (T2, "H16")])
            propose(None, None, 0, plan.IMPASSE, prop, [])
            propose(None, None, 1, plan.ERROR, prop, [])
            propose(None, None, 2, plan.CONFLICT, prop, [])
        self.assertEqual(seen, [{}, {1: T3}, {1: T3}])
        self.assertIs(loop.propose_for("n", LABELS), pl_protocol.propose_v1c)

    def test_the_handed_check(self):
        rec = {"records": [{"idx": 0, "truth": T2}, {"idx": 1, "truth": T3}],
               "escalations": [{"idx": 0, "kind": "IMPASSE"}, {"idx": 1, "kind": "ERROR"}],
               "reports_handed": {"1": T3}}
        self.assertTrue(run.handed_check(rec, "l")[0])
        self.assertFalse(run.handed_check(rec, "n")[0])
        self.assertFalse(run.handed_check({**rec, "reports_handed": {"1": T1}}, "l")[0])
        self.assertFalse(run.handed_check({**rec, "reports_handed": {"0": T2, "1": T3}},
                                          "l")[0])
        self.assertTrue(run.handed_check({**rec, "reports_handed": {}}, "n")[0])


# ---------------------------------------------------------------------------
# 4. The at-once asks
# ---------------------------------------------------------------------------

def l_record(n_labels: int) -> dict:
    cases = generate_corpus(plan.N, seed=plan.SEED)
    idx = list(range(5, 5 + n_labels))
    return {"records": [{"idx": i, "truth": T2 if i % 2 else T3} for i in range(len(cases))],
            "escalations": [{"idx": 0, "kind": "IMPASSE"}]
                           + [{"idx": i, "kind": "ERROR"} for i in idx],
            "reports_handed": {str(i): (T2 if i % 2 else T3) for i in idx}}


class TestTheAtOnceAsks(unittest.TestCase):

    def test_with_no_label_they_are_plan_manuals_level_1_compile_messages(self):
        self.assertEqual(prompts.messages([]), mprompts.compile_messages(1))
        self.assertEqual(sha16(prompts.HEADER), plan.AT_ONCE_HEADER_SHA16)

    def test_the_user_message_over_labels(self):
        c = case(product="api")
        msg = prompts.user_message([(c, T3), (c, T2)])
        self.assertTrue(msg.startswith(prompts.HEADER))
        self.assertTrue(msg.endswith("\n\n" + mprompts.COMPILE_USER))
        lines = msg[len(prompts.HEADER):-len("\n\n" + mprompts.COMPILE_USER)].split("\n")
        self.assertEqual([json.loads(x)["cola_correcta"] for x in lines], [T3, T2])
        self.assertEqual(json.loads(lines[0])["ticket"], c.as_dict())
        with self.assertRaises(prompts.NotAQueue):
            prompts.ticket_line(c, "H07")

    def test_the_labels_read_off_an_l_record(self):
        rec = l_record(3)
        self.assertEqual(ask.labelled(rec), [(5, T2 if 5 % 2 else T3), (6, T3), (7, T2)])
        with self.assertRaises(ask.NotHanded):
            ask.labelled({**rec, "reports_handed": {**rec["reports_handed"], "6": T1}})
        with self.assertRaises(ask.NotHanded):
            ask.labelled({**rec, "reports_handed": {**rec["reports_handed"], "0": T3}})

    def test_the_design_of_each_session(self):
        prior = ask.design("prior")
        self.assertEqual([a.id for a in prior], [f"prior:0:{k}" for k in range(1, 6)])
        self.assertTrue(all(a.labelled == () for a in prior))
        asks = ask.design("l_r1", l_record(45))
        self.assertEqual(sorted({a.checkpoint for a in asks}), [10, 20, 40, 45])
        self.assertEqual(len(asks), 4 * plan.ASKS_PER_CHECKPOINT)
        self.assertTrue(all(len(a.labelled) == a.checkpoint for a in asks))
        smoke = ask.design("smoke", l_record(4))
        self.assertEqual([(a.checkpoint, a.k) for a in smoke], [(0, 1), (4, 1)])
        with self.assertRaises(ask.NotHanded):
            ask.design("smoke", l_record(0))

    def test_the_validity_flag_on_an_empty_object_first(self):
        ok = {"rules": [{"conditions": [], "action": T1}]}
        self.assertIsNotNone(ask.validity(None, {}, "stop", plan.PROVIDER_NAME))
        self.assertIsNotNone(ask.validity(None, {"rules": []}, "stop", plan.PROVIDER_NAME))
        self.assertIsNone(ask.validity(None, ok, "stop", plan.PROVIDER_NAME))
        self.assertIsNotNone(ask.validity(None, ok, "length", plan.PROVIDER_NAME))
        self.assertIsNotNone(ask.validity(None, ok, "stop", "Baidu"))
        self.assertIsNotNone(ask.validity("boom", None, None, None))

    def test_the_reasks_and_the_session(self):
        """An answer that is not valid is asked again, at most twice."""
        rec = l_record(10)
        good = {"rules": [{"conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                           "action": T1}]}
        calls = []

        class FakeLive:
            def ask(self, messages):
                calls.append(messages)
                attempts = [{"provider": plan.PROVIDER_NAME, "finish_reason": "stop"}]
                pl = {} if len(calls) <= 4 else good
                return p.Answer(None, pl, None, "stop", 1, attempts)

        with TempOut():
            partial = plan.ask_partial_path("l_r1")
            asks, rows, _ = ask.run_session("l_r1", rec, lambda sleep: FakeLive(), partial,
                                            {"plan": "test"}, workers=1)
        firsts = [r for r in rows if r["reask"] == 0]
        self.assertEqual(len(firsts), plan.ASKS_PER_CHECKPOINT)
        self.assertTrue(all(not r["valid"] for r in firsts))
        again = [r for r in rows if r["reask"] == 1]
        self.assertEqual(len(again), 3)
        self.assertEqual(sum(r["valid"] for r in again), 2)
        third = [r for r in rows if r["reask"] == 2]
        self.assertEqual([r["valid"] for r in third], [True])

    def test_the_request_is_placements_with_the_budget(self):
        msgs = [{"role": "user", "content": "u"}]
        for attempt in (0, 1):
            ours = prompts.request(plan.PROVIDER, plan.MODEL, "x", msgs, attempt)
            theirs = pl_protocol.request_with(plan.PROVIDER, plan.MODEL, "x", msgs, attempt)
            self.assertEqual({**ours, "max_tokens": 0}, {**theirs, "max_tokens": 0})
            self.assertEqual(ours["max_tokens"], 32000)


# ---------------------------------------------------------------------------
# 5. The learners' plumbing
# ---------------------------------------------------------------------------

class TestTheLearners(unittest.TestCase):

    def test_best_reads_the_learners_that_fitted_and_not_the_table(self):
        with mock.patch.object(learners, "ilp_right", side_effect=[5, 7]), \
                mock.patch.object(learners, "student_right",
                                  side_effect=[3, RuntimeError("no fit"), 4]), \
                mock.patch.object(learners, "table_right", return_value=99):
            got = learners.trained([(0, T1), (1, T2)])
        self.assertEqual(got["tree"]["right"], 3)
        self.assertIsNone(got["logistic"]["right"])
        self.assertIn("no fit", got["logistic"]["error"])
        self.assertEqual(learners.best(got), 7)

    def test_the_table_decides_its_distinct_tickets(self):
        cases = learners.corpus()
        seen: dict = {}
        for i, c in enumerate(cases):
            if c.key() in seen:
                first, repeat = seen[c.key()], i
                break
            seen[c.key()] = i
        other = next(i for i, c in enumerate(cases) if c.key() != cases[first].key())
        self.assertEqual(learners.table_right([(first, T1), (repeat, T1)]), 1)
        self.assertEqual(learners.table_right([(first, T1), (repeat, T1), (other, T2)]), 2)

    def test_the_control_on_the_proposers_own_answers(self):
        rec = {"records": [
            {"idx": 0, "escalated": True, "proposal_action_correct": False, "predicted": T1},
            {"idx": 1, "escalated": True, "proposal_action_correct": True, "predicted": T3},
            {"idx": 2, "escalated": False, "proposal_action_correct": None, "predicted": T2}]}
        self.assertEqual(learners.own_answers(rec, {"1": T2}), [(0, T1), (1, T2)])


# ---------------------------------------------------------------------------
# 6. Stage C's rows
# ---------------------------------------------------------------------------

def run_row(rep: int, space=None, pair=None, oncall=None, followed=None) -> dict:
    return {"rep": rep, "space": space, "pair": pair, "oncall": oncall, "followed": followed}


class TestStageC(unittest.TestCase):

    def test_the_median_rows_on_their_sides_with_thin_labels(self):
        runs = {"l": [run_row(1, F(8, 10), F(7, 10), F(1), F(1)),
                      run_row(2, F(9, 10), F(8, 10), F(1), F(19, 20)),
                      run_row(3, F(7, 10), F(6, 10), F(1, 3), F(9, 10))],
                "n": [run_row(1, F(6, 10), F(4, 10)), run_row(2, F(65, 100), F(4, 10)),
                      run_row(3, F(5, 10), F(3, 10))]}
        b = score.row("CR-b", runs, {})
        self.assertEqual((b["verdict"], b["value"]["fraction"]), (score.HOLDS, "1/5"))
        self.assertFalse(b["thin"])
        c = score.row("CR-c", runs, {})
        self.assertEqual((c["verdict"], c["value"]["fraction"]), (score.HOLDS, "3/10"))
        a = score.row("CR-a", runs, {})
        self.assertEqual(a["verdict"], score.HOLDS)
        self.assertTrue(a["thin"])                       # 9/10 in place of the median refutes
        f = score.row("CR-f", runs, {})
        self.assertEqual(f["verdict"], score.HOLDS)
        self.assertTrue(f["thin"])

    def test_the_differences_and_their_reasons_for_no_value(self):
        runs = {"l": [run_row(1, F(8, 10)), run_row(2, F(9, 10)), run_row(3, F(7, 10))],
                "n": []}
        extra = {1: {"at_once_all": F(85, 100), "best_all": F(5, 10)},
                 2: {"at_once_all": F(88, 100), "best_all": F(95, 100)},
                 3: {"at_once_all": None, "best_all": F(6, 10)}}
        d = score.row("CR-d", runs, extra)               # 5/100 and -2/100: median 3/200
        self.assertEqual((d["verdict"], d["value"]["fraction"]), (score.HOLDS, "3/200"))
        self.assertTrue(d["thin"])                       # -2/100 in its place refutes
        e = score.row("CR-e", runs, extra)
        self.assertEqual(e["verdict"], score.HOLDS)
        self.assertTrue(e["thin"])
        none = score.row("CR-d", runs, {1: {"at_once_all": F(1)}})
        self.assertEqual(none["verdict"], score.NO_VALUE)
        short = score.row("CR-b", {"l": runs["l"], "n": [run_row(1, F(1, 2))]}, {})
        self.assertEqual(short["verdict"], score.NO_VALUE)

    def test_followed_reads_the_first_calls_at_reported_tickets(self):
        rec = {"records": [{"idx": 0, "truth": T2}, {"idx": 1, "truth": T3},
                           {"idx": 2, "truth": T1}],
               "escalations": [
                   {"idx": 0, "kind": "IMPASSE", "calls": [{"payload": {"action": T1}}]},
                   {"idx": 1, "kind": "ERROR", "calls": [{"payload": {"action": T3}}]},
                   {"idx": 2, "kind": "ERROR", "calls": [{"payload": {}}]}]}
        self.assertEqual(score.followed(rec), (1, 1))

    def test_the_arrivals_of_a_run_the_cap_stopped(self):
        """A run that stops at the cap keeps rows only for the cases it read,
        and its final base still decides all 2,000 arrivals, read against the
        corpus labels (2026-11-14: Stage C's first launch stopped on N r1)."""
        rows = [{"idx": i, "truth": t, "correct": i == 0}
                for i, (t, _) in enumerate(plan.labels()[:3])]
        rec = {"records": rows, "reports_handed": {}}
        got = score.corpus_split(rec, PriorityEngine(space=MI.space()))
        self.assertEqual(got["labelled"], [0, 0])
        self.assertEqual(got["rest"], [0, plan.N])
        self.assertEqual(got["online"], [1, 3])
        self.assertEqual(got["online_cases_read"], 3)


# ---------------------------------------------------------------------------
# 7. Nothing is built, asked or written unsigned
# ---------------------------------------------------------------------------

class TestNothingUnsigned(unittest.TestCase):

    def test_every_writer_refuses_unsigned(self):
        with TempOut() as d, mock.patch.object(plan, "gate_signature", return_value=UNSIGNED):
            for argv, main in ((["--smoke", "--arm", "n"], run.main),
                               (["--rep", "1", "--arm", "l"], run.main),
                               (["--session", "prior"], ask.main),
                               ([], score.main)):
                with self.subTest(argv=argv, main=main.__module__):
                    with mock.patch.object(gates, "run_checks") as checks:
                        with self.assertRaises(SystemExit):
                            main(argv)
                        checks.assert_not_called()
            self.assertEqual(list(d.iterdir()), [])

    def test_the_turn(self):
        with TempOut():
            self.assertEqual(run.next_step(), "corrections.run --smoke --arm n")
            self.assertEqual(run.sessions_before("n", 2), ["smoke", "prior", "l_r1", "l_r2"])
            self.assertFalse(run.turn_check("l", 1)[0])


class TestTheGates(unittest.TestCase):

    def test_the_cheap_checks_pass(self):
        self.assertTrue(gates.texts()["passes"], gates.texts())
        self.assertTrue(gates.requests()["passes"])
        self.assertTrue(gates.drafting()["passes"])
        self.assertTrue(gates.the_pool_is_for_asks())


if __name__ == "__main__":
    unittest.main()
