"""
`PLAN_CHANNEL.md`'s instrument, `channel/`. **No figure of the plan**: no test
runs the loop over the corpus, and every rule, ticket, engine, run and record
below is built by hand. The draws are rebuilt from their seed strings and never
counted. The figures §0 declares are recomputed by `CH-g2` and Stage A, never
here.

What is pinned:

  1. §11's constants, the seeds and §0's lines, `DECLARED` against §0's text, the
     schedule, and the gate, which counts every signature line.
  2. The draws: rebuilt from their seed strings, one per case from 0 to 1, no two
     streams alike, nested across coverages, and the same under any
     `PYTHONHASHSEED`; and `reportable`, compared exactly.
  3. The trigger, and the loop on corpora built by hand: coverage 1 is
     `PLAN_REASONED_LOOP.md`'s error arm and coverage 0 its impasse arm, record
     for record; at 1/2 a wrong decision escalates by its draw, and one not
     reported stands and fires.
  4. The trigger is the only code of the loop that reads a label to decide
     anything: labels and draws that leave the causes unchanged leave the
     proposer's calls, its messages and the base unchanged; nothing the trigger
     reads is handed to the proposer; and every comparison with the label in the
     proposer's path is listed here, so that a new one is a decision.
  5. The resume: a resumed record keeps each call's own seconds, and a partial
     file written under other draws is refused.
  6. Nothing is built, asked or written while the plan is unsigned, the dry runs
     build no client, and a run refuses before the key without what must come
     before it.
  7. The smoke check, with the trigger's record.
  8. The gates' instruments on records built by hand: the replay double, the
     record comparison, the trigger's record and a closed verdict's projection.
  9. Stage C's terms: exact lines on both sides, medians, thin labels, every
     reason a row has no value, the calls and the channel's reports.
"""

from __future__ import annotations

import ast
import inspect
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile
import textwrap
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import Case

from authorship import protocol as e
from authorship import run as erun
from manual import instrument as MI
from reasoned_loop import loop as rl_loop
from reasoned_loop import plan as rl_plan
from reasoned_loop import protocol as rl_protocol
from rung2.engine2 import PriorityEngine, validate_conditions
from rung2.proposers2 import ProposalError

from channel import gates, loop, plan, references, run, sample, score

REPO = Path(__file__).resolve().parent.parent
F = Fraction
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
T1, T2, T3, S = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"
p = rl_protocol


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


class Scripted:
    """A proposer double: each draft and placement from a function, every call
    remembered with everything it was handed."""
    name = "scripted"

    def __init__(self, draft, place=None):
        self.draft, self.place, self.asked = draft, place, []

    def first(self, case, idx):
        self.asked.append(("first", idx, case))
        got = self.draft(case, idx)
        if isinstance(got, Exception):
            raise got
        return answer(got)

    def placement(self, case, draft, message, idx, listed=None):
        self.asked.append(("placement", idx, case, list(listed or []), message))
        got = self.place(case, draft, listed, idx)
        if isinstance(got, Exception):
            raise got
        return answer(got)


def placing(beats=(), loses_to=()):
    def place(case, draft, listed, idx):
        b = [r for r in listed if r in beats or beats == "all"]
        lo = [r for r in listed if r in loses_to or loses_to == "all"]
        return dict(draft.payload, beats=b, loses_to=lo)
    return place


def proposer() -> Scripted:
    def draft(c, i):
        return payload(*API) if c.product == "api" else payload(*CATCH_ALL)
    return Scripted(draft, placing(beats="all"))


def corpus() -> list[Case]:
    """Case 0 is an impasse on the empty base, which writes the catch-all; cases
    1 and 2 are API tickets the catch-all sends to the wrong queue until the API
    rule is born."""
    return [case(product="dashboard"), case(product="api"), case(product="api", severity=4)]


LABELS = [(T1, "H29"), (T2, "H16"), (T2, "H16")]


def records_of(res, engine) -> dict:
    return gates.as_json(loop.record_of(res, engine))


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_and_the_protocol_are_plan_reasoned_loops(self):
        for name in ("MODEL", "PROMPT", "TEMPERATURE", "REASONING", "MAX_TOKENS",
                     "MAX_RETRIES", "CALL_RETRY_WAIT", "PROVIDER", "PROVIDER_NAME",
                     "RATE_LIMITED", "RATE_LIMIT_WAIT", "PROTOCOL", "LEVEL",
                     "SYSTEM_PROMPT_SHA16", "IMPASSE", "CONFLICT", "ERROR", "CAUSES"):
            with self.subTest(name):
                self.assertEqual(getattr(plan, name), getattr(rl_plan, name))
        self.assertEqual(plan.settings(), {"reasoning": {"effort": "high"},
                                           "max_tokens": 16000})
        self.assertEqual(plan.PROVIDER, {"order": ["baidu"], "allow_fallbacks": False})
        self.assertEqual((plan.PROTOCOL, plan.LEVEL, plan.SYSTEM_PROMPT_SHA16),
                         ("v1b", 3, "7b883f03a863d647"))
        self.assertEqual(plan.labels_path(), rl_plan.labels_path())

    def test_the_arms_and_the_runs(self):
        self.assertEqual(plan.ARMS, ("c", "e"))
        self.assertEqual(plan.COVERAGE, {"c": F(1, 2), "e": F(1)})
        for v in plan.COVERAGE.values():
            self.assertIsInstance(v, Fraction)
        self.assertEqual((plan.REPS, plan.N, plan.SEED), (3, 2000, 17))
        self.assertEqual((plan.SMOKE_N, plan.SMOKE_ARM), (30, "c"))
        self.assertEqual(plan.MAX_ESCALATIONS, 400)
        self.assertEqual(plan.MAX_CONSECUTIVE_FAILURES, erun.STOP_AFTER_FAILURES_IN_A_ROW)
        self.assertEqual(plan.MAX_CONSECUTIVE_FAILURES, 5)
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_seeds_are_the_next_two_primes_after_83_and_no_closed_threads(self):
        self.assertEqual((plan.ORDER_SEED, plan.CHANNEL_SEED), (89, 97))
        closed = {17, 18, 19, 20, 25, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83}
        self.assertFalse({plan.ORDER_SEED, plan.CHANNEL_SEED} & closed)
        primes = [n for n in range(84, 100) if all(n % d for d in range(2, n))]
        self.assertEqual(primes[:2], [plan.ORDER_SEED, plan.CHANNEL_SEED])

    def test_the_lines_are_section_0s_as_fractions(self):
        self.assertEqual(plan.LINES, {"CH-a": F(9, 10), "CH-b": F(1, 20), "CH-c": F(9, 10),
                                      "CH-d": F(9, 10), "CH-e": F(9, 10), "CH-f": F(3, 4)})
        for v in plan.LINES.values():
            self.assertIsInstance(v, Fraction)
        self.assertEqual(plan.HOLDS_AT_OR_BELOW, ("CH-b",))

    def test_the_plan_states_them(self):
        text = (REPO / "PLAN_CHANNEL.md").read_text()
        for s in ('`ARMS = ("c", "e")`', '`COVERAGE = {"c": Fraction(1, 2), "e": Fraction(1)}`',
                  "`REPS = 3`", "`N = 2000`", "`SEED = 17`", "`SMOKE_N = 30`",
                  '`SMOKE_ARM = "c"`', "`MAX_ESCALATIONS = 400`",
                  "`MAX_CONSECUTIVE_FAILURES = 5`", "`ORDER_SEED = 89`",
                  "`CHANNEL_SEED = 97`", "`MIN_SIGNATURES = 1`",
                  "`CH_A_LINE = Fraction(9, 10)`", "`CH_B_LINE = Fraction(1, 20)`",
                  "`CH_C_LINE = Fraction(9, 10)`", "`CH_D_LINE = Fraction(9, 10)`",
                  "`CH_E_LINE = Fraction(9, 10)`", "`CH_F_LINE = Fraction(3, 4)`",
                  '`SYSTEM_PROMPT_SHA16 = "7b883f03a863d647"`',
                  '`f"PLAN_CHANNEL/order/{ORDER_SEED}"`',
                  '`f"PLAN_CHANNEL/channel/{CHANNEL_SEED}/r{rep}"`'):
            with self.subTest(s):
                self.assertIn(s, text)

    def test_declared_transcribes_section_0(self):
        """Each figure `DECLARED` holds is one §0 states, in §0's words. Whether
        it comes back is `CH-g2`'s and Stage A's, never a test's."""
        text = " ".join((REPO / "PLAN_CHANNEL.md").read_text().split())
        d = plan.DECLARED
        oncall = d["rare"]["ONCALL_ESCALATION"]
        self.assertIn("at cases " + ", ".join(map(str, oncall["at"][:-1]))
                      + f" and {oncall['at'][-1]}", text)
        self.assertIn("`H04` governs 4 of them and `H05` 3", text)
        self.assertIn("`SECURITY_INCIDENT` has 20; `H01` governs 9 and `H02` 11", text)
        for q, n in d["space_by_queue"].items():
            with self.subTest(q):
                self.assertRegex(text, rf"`{q}`'s(?: are)? {n:,}")
        for run_, want in d["draws"].items():
            on, sec = want["ONCALL_ESCALATION"], want["SECURITY_INCIDENT"]
            with self.subTest(run_):
                self.assertIn(f"| `c {run_}` | {want['reportable']:,}", text)
                self.assertIn(", ".join(map(str, on["at"])), text)
                self.assertIn(f"| {sec['reportable']} ", text)
        self.assertIn("23 escalations, 2 impasses and 21 errors; 45 calls; 134,380 points "
                      "of the space, and 1,999 arrivals read whole", text)
        self.assertIn("22 escalations, 2 impasses and 20 errors; 43 calls; 132,280 points, "
                      "and 1,996 arrivals. It recalls 2/3", text)
        self.assertIn("`H05` governs 2,100 of the queue's 6,300 points", text)
        self.assertIn("**The transcriber under the error arm**: 23 escalations, 45 calls and "
                      "134,380 points", text)
        self.assertIn("`e r1`, `c r1`, `e r2`, `c r2`, `e r3`, `c r3`", text)
        for rule, (queue, tickets, tx, runs) in d["supply"]["rules"].items():
            with self.subTest(rule):
                self.assertIn(f"| `{rule}` | `{queue}` | {tickets} | {tx} | "
                              + " / ".join(map(str, runs)) + " |", text)
        self.assertIn("escalated on 62, 80 and 100 errors, against the transcriber's 21", text)
        self.assertIn("each base decided 379 to 590 arrivals wrongly", text)

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        self.assertEqual(order, plan.schedule())
        first = random.Random("PLAN_CHANNEL/order/89").choice(plan.ARMS)
        self.assertEqual(order[0], (first, 1))
        arms = [a for a, _ in order]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))
        self.assertEqual([r for _, r in order], [1, 1, 2, 2, 3, 3])
        self.assertEqual(sorted(order), sorted((a, r) for a in plan.ARMS for r in (1, 2, 3)))

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            for path in (plan.sample_path(), plan.score_path(), plan.smoke_path(),
                         plan.run_path("c", 2), plan.partial_path(plan.tag("e", 3))):
                self.assertEqual(path.parent, d)
        self.assertEqual(plan.tag(None, None), "smoke")
        self.assertEqual(plan.tag("c", 1), "c_r1")
        for bad in (("x", 1), ("e", 4), ("c", 0)):
            with self.subTest(bad), self.assertRaises(ValueError):
                plan.run_path(*bad)


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_every_line_is_counted_and_one_is_needed(self):
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-05)**\n"
        blank = "**Signed by Sergi: ________ (date: ________)**\n"
        cases = ((blank, False), (signed, True), (signed + blank, False),
                 (signed * 2, True), (blank + signed, False),
                 ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "PLAN.md"
            for text, ok in cases:
                path.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(path)["passes"], ok)
            self.assertFalse(plan.gate_signature(Path(d) / "absent.md")["passes"])

    def test_the_plan_carries_its_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned: a test
        that pinned a draft's blank line would fail at the signature."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_CHANNEL.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_CHANNEL.md"))
        self.assertEqual(plan.gate_signature()["source"], "PLAN_CHANNEL.md")


# ---------------------------------------------------------------------------
# 2. The draws
# ---------------------------------------------------------------------------

class TestTheDraws(unittest.TestCase):

    def test_each_stream_is_rebuilt_from_its_seed_string(self):
        self.assertEqual(plan.STREAMS, ("r1", "r2", "r3", "smoke"))
        for name in plan.STREAMS:
            with self.subTest(name):
                seed = f"PLAN_CHANNEL/channel/97/{name}"
                self.assertEqual(plan.draw_seed(name), seed)
                rng = random.Random(seed)
                self.assertEqual(plan.draws(name), tuple(rng.random() for _ in range(2000)))
        with self.assertRaises(ValueError):
            plan.draw_seed("r4")

    def test_one_per_case_from_0_to_1_and_no_two_streams_alike(self):
        for name in plan.STREAMS:
            got = plan.draws(name)
            self.assertEqual(len(got), plan.N)
            self.assertTrue(all(0 <= u < 1 for u in got))
        self.assertEqual(len({plan.draws(n) for n in plan.STREAMS}), len(plan.STREAMS))
        self.assertEqual(len({plan.draws_digest(n) for n in plan.STREAMS}), len(plan.STREAMS))

    def test_a_stream_follows_its_seed_and_nothing_cached_under_another(self):
        before = plan.draws("r1")
        with mock.patch.object(plan, "CHANNEL_SEED", 98):
            self.assertNotEqual(plan.draws("r1"), before)
            self.assertEqual(plan.draw_seed("r1"), "PLAN_CHANNEL/channel/98/r1")
        self.assertEqual(plan.draws("r1"), before)

    def test_the_same_under_any_hash_seed(self):
        """A string seed goes through SHA-512: the draws, and the schedule, depend
        on no `PYTHONHASHSEED`."""
        code = ("from channel import plan; print([plan.draws_digest(n) for n in plan.STREAMS], "
                "plan.schedule())")
        here = f"{[plan.draws_digest(n) for n in plan.STREAMS]} {plan.schedule()}"
        for seed in ("0", "1", "4242"):
            with self.subTest(seed):
                got = subprocess.run([sys.executable, "-c", code], cwd=REPO, text=True,
                                     capture_output=True, check=True,
                                     env={**os.environ, "PYTHONHASHSEED": seed})
                self.assertEqual(got.stdout.strip(), here)

    def test_the_stream_each_run_reads(self):
        self.assertEqual(plan.stream("c", 2), "r2")
        self.assertEqual(plan.stream("c", None), "smoke")
        self.assertIsNone(plan.stream("e", 1))
        with self.assertRaises(ValueError):
            plan.stream("i", 1)

    def test_what_a_record_says_of_its_channel(self):
        c = plan.channel_of("c", 3)
        self.assertEqual(c, {"channel_coverage": "1/2",
                             "draws_seed": "PLAN_CHANNEL/channel/97/r3",
                             "draws_sha16": plan.draws_digest("r3"), "draws_n": 2000})
        self.assertEqual(plan.channel_of("c", None)["draws_seed"], "PLAN_CHANNEL/channel/97/smoke")
        self.assertEqual(plan.channel_of("e", 1), {"channel_coverage": "1", "draws_seed": None,
                                                   "draws_sha16": None, "draws_n": None})

    def test_reportable_is_exact(self):
        half = F(1, 2)
        below = 0.49999999999999994                      # the float just under 1/2
        self.assertTrue(plan.reportable(half, below))
        self.assertFalse(plan.reportable(half, 0.5))
        self.assertTrue(plan.reportable(half, 0.0))
        self.assertTrue(plan.reportable(F(1), None))
        self.assertTrue(plan.reportable(F(1), 0.999))
        self.assertFalse(plan.reportable(F(0), 0.0))
        self.assertFalse(plan.reportable(F(0), None))
        self.assertTrue(plan.reportable(F(1, 3), 0.3333333333333333))   # below 1/3 exactly
        for bad in ((half, None), (0.5, 0.1), (F(3, 2), 0.1), (F(-1, 2), 0.1)):
            with self.subTest(bad), self.assertRaises(ValueError):
                plan.reportable(*bad)

    def test_the_draws_are_nested_across_coverages(self):
        """A case reported at 1/4 would be reported at 1/2 (§2.1)."""
        for name in plan.STREAMS:
            at = {c: {t for t, u in enumerate(plan.draws(name)) if plan.reportable(c, u)}
                  for c in (F(1, 4), F(1, 2), F(1))}
            self.assertLessEqual(at[F(1, 4)], at[F(1, 2)])
            self.assertLessEqual(at[F(1, 2)], at[F(1)])
            self.assertEqual(at[F(1)], set(range(plan.N)))


# ---------------------------------------------------------------------------
# 3. The trigger, and the loop on corpora built by hand
# ---------------------------------------------------------------------------

class TestTheTrigger(unittest.TestCase):

    def test_the_cause_and_the_report(self):
        w = SimpleNamespace(action=T1)
        for cov in (F(0), F(1, 2), F(1)):
            with self.subTest(cov):
                self.assertEqual(loop.escalates(cov, "IMPASSE", None, T2, None), ("IMPASSE", None))
                self.assertEqual(loop.escalates(cov, "CONFLICT", None, T2, 0.9),
                                 ("CONFLICT", None))
                self.assertEqual(loop.escalates(cov, "ACTION", w, T1, None), (None, None))
        self.assertEqual(loop.escalates(F(1), "ACTION", w, T2, None), ("ERROR", True))
        self.assertEqual(loop.escalates(F(0), "ACTION", w, T2, 0.0), (None, False))
        self.assertEqual(loop.escalates(F(1, 2), "ACTION", w, T2, 0.25), ("ERROR", True))
        self.assertEqual(loop.escalates(F(1, 2), "ACTION", w, T2, 0.5), (None, False))
        with self.assertRaises(ValueError):
            loop.escalates(F(1, 2), "ACTION", w, T2, None)

    def test_the_escalation_and_the_record_are_plan_reasoned_loops(self):
        self.assertIs(loop.propose_v1b, rl_loop.propose_v1b)
        self.assertIs(loop.record_of, rl_loop.record_of)
        self.assertTrue(issubclass(loop.Result, rl_loop.Result))
        self.assertIs(run.p, rl_protocol)

    def both(self, coverage, arm, draws=None):
        a, b = PriorityEngine(space=MI.space()), PriorityEngine(space=MI.space())
        ours = loop.run_loop(corpus(), LABELS, a, proposer(), coverage, draws,
                             clock=lambda: 0.0)
        theirs = rl_loop.run_loop(corpus(), LABELS, b, proposer(), arm, clock=lambda: 0.0)
        return records_of(ours, a), records_of(theirs, b), ours

    def test_coverage_1_is_the_error_arm_record_for_record(self):
        ours, theirs, res = self.both(F(1), "e")
        self.assertEqual(set(gates.same_record(ours, theirs).values()), {True})
        self.assertTrue(gates.trigger_kept(ours, F(1)))
        self.assertEqual([r["cause"] for r in ours["records"]], ["IMPASSE", "ERROR", None])
        self.assertEqual([r["reported"] for r in ours["records"]], [None, True, None])
        self.assertEqual(res.summary()["channel"], {"coverage": "1", "wrong_decisions": 1,
                                                    "reported": 1, "unreported": 0})

    def test_coverage_0_is_the_impasse_arm_record_for_record(self):
        ours, theirs, res = self.both(F(0), "i")
        self.assertEqual(set(gates.same_record(ours, theirs).values()), {True})
        self.assertTrue(gates.trigger_kept(ours, F(0)))
        self.assertEqual([r["reported"] for r in ours["records"]], [None, False, False])
        self.assertEqual(res.summary()["channel"]["unreported"], 2)
        self.assertEqual(res.summary()["silent_errors_among_them"], 2)

    def test_at_one_half_the_draw_decides_and_an_unreported_error_stands(self):
        eng = PriorityEngine(space=MI.space())
        draws = [0.9, 0.7, 0.2]
        res = loop.run_loop(corpus(), LABELS, eng, proposer(), F(1, 2), draws)
        rec = records_of(res, eng)
        self.assertEqual([r["cause"] for r in rec["records"]], ["IMPASSE", None, "ERROR"])
        self.assertEqual([r["reported"] for r in rec["records"]], [None, False, True])
        self.assertEqual([r["draw"] for r in rec["records"]], draws)
        self.assertEqual([r["correct"] for r in rec["records"]], [True, False, True])
        self.assertEqual(rec["records"][2]["engine_action"], T1)
        self.assertEqual(eng.rules[0].fire_count, 1)           # case 1's decision stood
        self.assertEqual(res.summary()["channel"], {"coverage": "1/2", "wrong_decisions": 2,
                                                    "reported": 1, "unreported": 1})
        self.assertTrue(gates.trigger_kept(rec, F(1, 2), draws))
        flipped = json.loads(json.dumps(rec))
        flipped["records"][1]["reported"] = True
        self.assertFalse(gates.trigger_kept(flipped, F(1, 2), draws))
        self.assertFalse(gates.trigger_kept(rec, F(1, 2), [0.9, 0.7, 0.21]))

    def test_the_loop_refuses_a_channel_it_cannot_read(self):
        for coverage, draws in ((F(1, 2), None), (F(1, 2), [0.1, 0.2]), (0.5, [0.1] * 3),
                                (F(2), None)):
            with self.subTest(coverage=coverage, draws=draws), self.assertRaises(ValueError):
                loop.run_loop(corpus(), LABELS, PriorityEngine(space=MI.space()), proposer(),
                              coverage, draws)

    def test_the_cap_stops_the_run(self):
        eng = PriorityEngine(space=MI.space())
        res = loop.run_loop(corpus(), LABELS, eng, proposer(), F(1), cap=1)
        self.assertEqual(res.stopped_at, 0)
        self.assertEqual(len(res.loop.run.records), 1)


# ---------------------------------------------------------------------------
# 4. Nothing the trigger reads reaches the proposer
# ---------------------------------------------------------------------------

class LiveScript:
    """A live model that answers or raises what it is handed, one per call,
    keeping every message list it was sent."""

    def __init__(self, *items):
        self.items, self.extra, self.sent = list(items), {}, []

    def ask(self, messages):
        self.sent.append(messages)
        got = self.items.pop(0)
        if isinstance(got, Exception):
            raise got
        self.extra = got.extra()
        return got


def answers():
    return (answer(payload(*CATCH_ALL)), answer(payload(*API)),
            answer(payload(*API, beats=["R0001"])))


class TestTheTriggerIsTheOnlyReader(unittest.TestCase):
    """Labels and draws that leave every cause as it was leave everything the
    proposer is handed as it was: run A and run B below differ in every label
    but one and in every draw, and both escalate case 0 as an impasse and case 1
    as a reported error, and let case 2 stand right."""

    A = ([(T1, "H29"), (T2, "H16"), (T2, "H16")], [0.9, 0.1, 0.3])
    B = ([(T3, "H06"), (S, "H01"), (T2, "H17")], [0.0, 0.49, 0.7])

    def run_with(self, labels, draws, prop):
        eng = PriorityEngine(space=MI.space())
        res = loop.run_loop(corpus(), labels, eng, prop, F(1, 2), draws, clock=lambda: 0.0)
        return res, eng

    def test_the_proposer_and_the_base_see_the_same(self):
        pa, pb = proposer(), proposer()
        ra, ea = self.run_with(*self.A, pa)
        rb, eb = self.run_with(*self.B, pb)
        self.assertEqual([c["cause"] for c in ra.causes], [c["cause"] for c in rb.causes])
        self.assertEqual(pa.asked, pb.asked)

        def base(eng):
            return [(r.rule_id, r.action, r.born_at, [c.as_dict() for c in r.conditions],
                     r.beats, r.loses_to, r.fire_count) for r in eng.rules]
        self.assertEqual(base(ea), base(eb))
        self.assertEqual(ea.edge_log, eb.edge_log)
        scoring = {"truth", "truth_rule", "correct", "proposal_action_correct", "draw",
                   "reported"}
        a, b = records_of(ra, ea)["records"], records_of(rb, eb)["records"]
        for x, y in zip(a, b):
            self.assertLessEqual({k for k in x if x[k] != y[k]}, scoring)

    def test_the_messages_are_the_tickets(self):
        """Through `PLAN_REASONED_LOOP.md`'s resumable proposer: every message
        list either run sends is the same, and the first call's is the ticket's
        and nothing else."""
        sent = []
        for labels, draws in (self.A, self.B):
            live = LiveScript(*answers())
            with tempfile.TemporaryDirectory() as d:
                path = Path(d) / "x.partial.jsonl"
                rows, _ = erun.open_partial(path, {"plan": "test"})
                self.run_with(labels, draws, p.Resumable(live, path, rows))
            sent.append(live.sent)
        self.assertEqual(sent[0], sent[1])
        self.assertEqual(sent[0][0], p.messages_for(corpus()[0]))
        self.assertEqual(sent[0][1], p.messages_for(corpus()[1]))
        self.assertEqual(len(sent[0]), 3)

    def calls_in(self, src: str) -> list[ast.Call]:
        tree = ast.parse(src)
        out = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            if ((isinstance(fn, ast.Name) and fn.id == "propose_v1b")
                    or (isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
                        and fn.value.id in ("proposer", "prop"))):
                out.append(node)
        return out

    def test_nothing_the_trigger_reads_is_handed_to_the_proposer(self):
        """In this package's loop and run, no call to the escalation or to the
        proposer is handed the label, the draw, the report or the coverage; and
        inside `PLAN_REASONED_LOOP.md`'s escalation, called, the proposer is
        handed neither those nor the cause, so it is never told the base erred."""
        forbidden = {"truth", "trule", "labels", "draw", "draws", "told", "coverage"}
        sources = {rel: (REPO / rel).read_text() for rel in ("channel/loop.py", "channel/run.py")}
        sources["reasoned_loop.loop.propose_v1b"] = textwrap.dedent(
            inspect.getsource(rl_loop.propose_v1b))
        found = 0
        for rel, src in sources.items():
            inner = rel.startswith("reasoned_loop")
            for call in self.calls_in(src):
                if inner and call.func.__class__ is ast.Name:
                    continue                 # propose_v1b is not called inside itself
                found += 1
                names = {n.id for a in [*call.args, *[k.value for k in call.keywords]]
                         for n in ast.walk(a) if isinstance(n, ast.Name)}
                with self.subTest(rel=rel, call=ast.unparse(call)):
                    self.assertFalse(names & (forbidden | ({"cause"} if inner else set())))
        self.assertGreaterEqual(found, 3)

    def test_every_comparison_with_the_label_is_listed_here(self):
        """The trigger compares the engine's decision with the label, and decides
        what the loop asks. The loop compares the decision that stood, or the
        proposer's answer, with it once each, for the record's `correct` and
        `proposal_action_correct`. Nothing else on the proposer's path compares
        anything with a label: a new comparison fails here until somebody
        decides what it is."""
        found = []
        for rel in ("channel/loop.py", "channel/run.py", "channel/plan.py"):
            tree = ast.parse((REPO / rel).read_text())
            for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
                for node in ast.walk(fn):
                    if isinstance(node, ast.Compare) and any(
                            isinstance(n, ast.Name) and n.id in ("truth", "trule", "labels")
                            for x in (node.left, *node.comparators) for n in ast.walk(x)):
                        found.append((rel, fn.name, ast.unparse(node)))
        self.assertEqual(sorted(found), sorted([
            ("channel/loop.py", "escalates", "winner.action == truth"),
            ("channel/loop.py", "run_loop", "predicted == truth"),
            ("channel/loop.py", "run_loop", "predicted == truth")]))


# ---------------------------------------------------------------------------
# 5. The resume
# ---------------------------------------------------------------------------

class TestTheResume(unittest.TestCase):

    def test_a_resumed_record_keeps_each_calls_own_seconds(self):
        """`PLAN_REASONED_LOOP.md` §5.5's second amendment, through this plan's
        loop: an answer and a failure served from the partial file keep the
        seconds the file kept, and a run that is not resumed keeps the loop's."""
        header = {"plan": "test"}
        corp, labels = [case(product="api"), case()], [(T2, "H01"), (T1, "H29")]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, header)
            live = p.Resumable(LiveScript(e.ProposalFailed("no parse", "stop", 3, []),
                                          answer(payload(*CATCH_ALL))),
                               path, rows, clock=iter([0.0, 7.5, 10.0, 52.0]).__next__)
            asked = loop.run_loop(corp, labels, PriorityEngine(space=MI.space()), live,
                                  F(1, 2), [0.1, 0.9], clock=itertools.count(0.0, 5.0).__next__)
            live.flush()
            rows, resumed = erun.open_partial(path, header)
            self.assertTrue(resumed)
            served = loop.run_loop(corp, labels, PriorityEngine(space=MI.space()),
                                   p.Resumable(LiveScript(), path, rows), F(1, 2), [0.1, 0.9],
                                   clock=itertools.count(0.0, 0.01).__next__)
        for res, seconds in ((asked, [5.0, 5.0]), (served, [7.5, 42.0])):
            with self.subTest(seconds=seconds):
                calls = [esc.calls[0] for esc in res.loop.escalations]
                self.assertEqual([c["seconds"] for c in calls], seconds)
                self.assertEqual([c["failure"] is None for c in calls], [False, True])

    def test_a_partial_written_under_other_draws_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            erun.open_partial(path, run.protocol("c", plan.N, "c_r1", 1))
            with mock.patch.object(plan, "CHANNEL_SEED", 98):
                other = run.protocol("c", plan.N, "c_r1", 1)
            self.assertNotEqual(other, run.protocol("c", plan.N, "c_r1", 1))
            with self.assertRaises(SystemExit):
                erun.open_partial(path, other)

    def test_the_loop_does_not_swallow_an_outage(self):
        class Refused:
            name = "refused"

            def first(self, case, idx):
                raise p.RateLimited("refused")

        with self.assertRaises(p.RateLimited):
            loop.run_loop([case()], [(T1, "H29")], PriorityEngine(space=MI.space()),
                          Refused(), F(1, 2), [0.3])


# ---------------------------------------------------------------------------
# 6. Nothing unsigned, and the order of events
# ---------------------------------------------------------------------------

def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED)


def stage_a(d: Path, **over) -> None:
    refs = {"fingerprint": p.fingerprint(), "schedule": [list(x) for x in plan.schedule()],
            "draws": {"streams": {n: {"seed": plan.draw_seed(n), "sha16": plan.draws_digest(n)}
                                  for n in plan.STREAMS}}}
    refs.update(over)
    (d / "sample.json").write_text(json.dumps({"references": refs}))


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
        with mock.patch.dict(os.environ), TempOut(), \
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
        with TempOut(), mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
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
            stage_a(d)
            self.assertTrue(run.sample_check()[0])
            with self.assertRaises(SystemExit):
                run.main(["--arm", "e", "--rep", "1"])   # no smoke record
        fetch.assert_not_called()
        checks.assert_not_called()

    def test_a_stage_a_record_under_another_schedule_or_other_draws_is_refused(self):
        with TempOut() as d:
            stage_a(d, schedule=[["c", 1]])
            self.assertFalse(run.sample_check()[0])
            stage_a(d, draws={"streams": {"r1": {"seed": "x", "sha16": "y"}}})
            self.assertFalse(run.sample_check()[0])
            stage_a(d, fingerprint="0" * 16)
            self.assertFalse(run.sample_check()[0])

    def test_the_turn(self):
        with TempOut():
            (first_arm, _), (second_arm, _) = plan.schedule()[:2]
            self.assertTrue(run.turn_check(first_arm, 1)[0])
            self.assertFalse(run.turn_check(second_arm, 1)[0])
            plan.run_path(first_arm, 1).write_text("{}")
            self.assertTrue(run.turn_check(second_arm, 1)[0])
            self.assertEqual(run.next_run(), (second_arm, 1))

    def test_score_refuses_without_stage_a(self):
        with TempOut(), mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                score.main([])
        write.assert_not_called()


# ---------------------------------------------------------------------------
# 7. The smoke check
# ---------------------------------------------------------------------------

REFUSED = {"provider": None, "reasoning_tokens": None, "finish_reason": None,
           "error": plan.RATE_LIMITED}
SMOKE_DRAWS = plan.draws("smoke")[:plan.SMOKE_N]


def smoke_rows() -> list[dict]:
    """Thirty rows the trigger kept: an impasse, then decisions that stood
    right, and one wrong decision on the first case whose draw reports it and
    one on the first whose draw does not."""
    rows = [{"idx": i, "outcome": "ACTION", "cause": None, "reported": None,
             "draw": SMOKE_DRAWS[i], "predicted": T1, "truth": T1, "engine_action": None}
            for i in range(plan.SMOKE_N)]
    rows[0].update(outcome="IMPASSE", cause="IMPASSE")
    told = next(i for i in range(1, plan.SMOKE_N) if SMOKE_DRAWS[i] < 0.5)
    quiet = next(i for i in range(1, plan.SMOKE_N) if SMOKE_DRAWS[i] >= 0.5)
    rows[told].update(cause="ERROR", reported=True, engine_action=T1, predicted=T2, truth=T2)
    rows[quiet].update(reported=False, truth=T2)
    return rows


def smoke_record(**over) -> dict:
    attempt = {"provider": plan.PROVIDER_NAME, "reasoning_tokens": 300, "finish_reason": "stop"}
    calls = [{"round": 0, "failure": None, "call_attempts": [dict(attempt)]},
             {"round": 1, "failure": None, "call_attempts": [dict(attempt)]}]
    rec = {**run.protocol(plan.SMOKE_ARM, plan.SMOKE_N, "smoke", None),
           "metrics": {"n_rules": 1}, "escalations": [{"calls": calls}],
           "records": smoke_rows()}
    rec.update(over)
    return rec


class TestTheSmokeCheck(unittest.TestCase):

    def check(self, rec) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            path.write_text(json.dumps(rec))
            return run.smoke_check(path)

    def test_a_clean_smoke_run_passes_and_says_what_the_trigger_did(self):
        ok, why = self.check(smoke_record())
        self.assertTrue(ok, why)
        self.assertIn("2 wrong decisions, 1 reported and escalated", why)

    def test_the_smoke_run_reads_its_own_draws(self):
        self.assertEqual(run.protocol(plan.SMOKE_ARM, plan.SMOKE_N, "smoke", None)["draws_seed"],
                         "PLAN_CHANNEL/channel/97/smoke")

    def test_attempts_refused_for_the_rate_are_counted_and_not_read(self):
        rec = smoke_record()
        rec["escalations"][0]["calls"][0]["call_attempts"][:0] = [REFUSED, REFUSED]
        ok, why = self.check(rec)
        self.assertTrue(ok)
        self.assertIn("2 refused for the rate", why)

    def test_each_failure(self):
        bad = smoke_record()
        bad["escalations"][0]["calls"][0]["call_attempts"][0]["provider"] = "Elsewhere"
        quiet = smoke_record()
        quiet["escalations"][0]["calls"][1]["call_attempts"][0]["reasoning_tokens"] = 0
        cut = smoke_record()
        cut["escalations"][0]["calls"][0]["call_attempts"][0]["finish_reason"] = "length"
        unplaced = smoke_record()
        unplaced["escalations"][0]["calls"] = unplaced["escalations"][0]["calls"][:1]
        unreached = smoke_record()
        for c in unreached["escalations"][0]["calls"]:
            c["call_attempts"] = [dict(REFUSED)]
        flipped = smoke_record()
        k = next(r["idx"] for r in flipped["records"] if r["reported"] is True)
        flipped["records"][k]["reported"] = False
        undrawn = smoke_record()
        undrawn["records"][3]["draw"] = None
        short = smoke_record()
        short["records"] = short["records"][:-1]
        missed = smoke_record()
        k = next(i for i, r in enumerate(missed["records"])
                 if r["outcome"] == "ACTION" and r["reported"] is None)
        missed["records"][k]["truth"] = T3          # a wrong decision the trigger did not see
        for name, rec in (("provider", bad), ("reasoning", quiet), ("budget", cut),
                          ("placement", unplaced), ("no rule", smoke_record(metrics={})),
                          ("protocol", smoke_record(n=20)),
                          ("another channel", smoke_record(draws_seed="x")),
                          ("nothing reached", unreached),
                          ("the waits", smoke_record(rate_limit_wait=[60])),
                          ("a report flipped", flipped), ("a draw missing", undrawn),
                          ("a case missing", short), ("a wrong decision unseen", missed)):
            with self.subTest(name):
                self.assertFalse(self.check(rec)[0])


# ---------------------------------------------------------------------------
# 8. The gates' instruments, on records built by hand
# ---------------------------------------------------------------------------

def paid_record() -> dict:
    """A paid run's record as far as the replay reads it: case 0's draft, case
    1's draft and placement, and case 2's failed draft."""
    def call(round_, pl=None, failure=None):
        return {"round": round_, "payload": pl, "raw": None, "finish_reason": "stop",
                "attempts": 1, "failure": failure, "call_attempts": [{"provider": "Baidu"}],
                "keys": None if pl is None else list(pl), "reasoning": "porque",
                "retries": [], "served_by": "Baidu"}
    return {"escalations": [
        {"idx": 0, "calls": [call(0, payload(*CATCH_ALL))]},
        {"idx": 1, "calls": [call(0, payload(*API)), call(1, payload(*API, beats=["R0001"]))]},
        {"idx": 2, "calls": [call(0, failure="sin objeto JSON")]}]}


class TestTheGatesInstruments(unittest.TestCase):

    def test_the_replay_serves_each_call_where_it_was_made(self):
        replay = gates.Replay(paid_record())
        got = replay.placement(case(), None, "m", idx=1)
        self.assertEqual(got.payload["beats"], ["R0001"])
        self.assertEqual((got.reasoning, got.served_by), ("porque", "Baidu"))
        self.assertEqual(replay.first(case(), idx=0).action, T1)
        with self.assertRaises(e.ProposalFailed):
            replay.first(case(), idx=2)
        with self.assertRaises(gates.ReplayDesync) as cm:
            replay.first(case(), idx=3)
        self.assertNotIsInstance(cm.exception, ProposalError)
        self.assertEqual(replay.asked, [(1, 1), (0, 0), (2, 0), (3, 0)])

    def test_the_replay_through_both_loops_gives_one_record(self):
        def run_(fn):
            eng = PriorityEngine(space=MI.space())
            return records_of(fn(eng, gates.Replay(paid_record())), eng)
        ours = run_(lambda eng, prop: loop.run_loop(corpus(), LABELS, eng, prop, F(1),
                                                    clock=lambda: 0.0))
        theirs = run_(lambda eng, prop: rl_loop.run_loop(corpus(), LABELS, eng, prop, "e",
                                                         clock=lambda: 0.0))
        self.assertEqual(set(gates.same_record(ours, theirs).values()), {True})
        self.assertEqual([r["cause"] for r in ours["records"]], ["IMPASSE", "ERROR", None])

    def test_the_record_comparison_has_teeth(self):
        eng = PriorityEngine(space=MI.space())
        rec = records_of(loop.run_loop(corpus(), LABELS, eng, proposer(), F(1),
                                       clock=lambda: 0.0), eng)
        theirs = json.loads(json.dumps(rec))
        for r in theirs["records"]:
            for k in gates.CHANNEL_KEYS:
                del r[k]
        del theirs["v1b"]["channel"]
        self.assertEqual(set(gates.same_record(rec, theirs).values()), {True})
        theirs["records"][1]["predicted"] = T3
        theirs["rules"][0]["fire_count"] += 1
        got = gates.same_record(rec, theirs)
        self.assertFalse(got["records"])
        self.assertFalse(got["rules"])
        self.assertTrue(got["edge_log"])

    def test_a_closed_verdict_is_read_without_its_floats(self):
        row = {"verdict": "holds", "value": {"fraction": "1613/1680", "value": 0.96},
               "line": {"fraction": "9/10", "value": 0.9}, "thin": True,
               "float_reading": 0.123, "per_run": ["1/2", "2/3"], "why": None}
        self.assertEqual(gates.projection(row), {"verdict": "holds", "value": "1613/1680",
                                                 "line": "9/10", "thin": True,
                                                 "per_run": ["1/2", "2/3"], "why": None})
        self.assertEqual(gates.projection(row), gates.projection({**row, "float_reading": 0.5}))
        self.assertNotEqual(gates.projection(row), gates.projection({**row, "thin": False}))

    def test_stage_a_says_which_declared_figures_did_not_come_back(self):
        refs = {"rare": {"as_declared": True}, "space_by_queue": {"as_declared": False},
                "h05_points": {"as_declared": True},
                "draws": {"as_declared": {"r1": True, "r2": False}},
                "supply": {"as_declared": {"rules": True, "error_escalations": False}},
                "transcriber": {"c_r1": {"as_declared": {"calls": False}},
                                "smoke": {"as_declared": None}},
                "schedule_as_declared": True}
        self.assertEqual(sample.not_back(refs), ["space_by_queue", "draws r2",
                                                 "supply error_escalations",
                                                 "transcriber c_r1"])

    def test_the_declared_transcriber_figures_are_read_by_run(self):
        got = {"escalations": 22, "impasses": 2, "errors": 20, "calls": 43,
               "space_right": 132280, "corpus_right": 1996, "recall_oncall": "2/3"}
        self.assertEqual(set(references.as_declared("c_r2", got).values()), {True})
        self.assertEqual(set(references.as_declared("e", {"escalations": 23, "calls": 45,
                                                          "space_right": 1}).values()),
                         {True, False})


# ---------------------------------------------------------------------------
# 9. Stage C's terms
# ---------------------------------------------------------------------------

def a_run(space=F(1, 2), oncall=F(1), calls=100) -> dict:
    return {"space": space, "oncall": oncall, "calls": calls}


def runs(c=(), e=()) -> dict[str, list[dict]]:
    return {"c": [a_run(**x) for x in c], "e": [a_run(**x) for x in e]}


class TestStageC(unittest.TestCase):

    def test_the_rows_are_section_0s(self):
        self.assertEqual(set(score.ROWS), set(plan.LINES))

    def test_every_line_is_compared_exactly_on_its_own_side(self):
        self.assertTrue(score.holds("CH-a", F(9, 10)))
        self.assertFalse(score.holds("CH-a", F(9, 10) - F(1, 10 ** 12)))
        self.assertTrue(score.holds("CH-b", F(1, 20)))
        self.assertFalse(score.holds("CH-b", F(1, 20) + F(1, 10 ** 12)))
        self.assertTrue(score.holds("CH-b", F(-1, 10)))
        self.assertTrue(score.holds("CH-f", F(3, 4)))
        self.assertFalse(score.holds("CH-f", F(74, 100)))

    def test_ch_a_and_ch_d_read_their_arms_median_and_its_thin_label(self):
        r = runs(c=[{"space": F(95, 100)}, {"space": F(85, 100)}, {"space": F(92, 100)}],
                 e=[{"space": F(99, 100)}, {"space": F(98, 100)}, {"space": F(97, 100)}])
        a, d = score.row("CH-a", r), score.row("CH-d", r)
        self.assertEqual((a["verdict"], a["value"]["fraction"], a["thin"]),
                         ("holds", "23/25", True))           # 0.85 in its place
        self.assertEqual((d["verdict"], d["value"]["fraction"], d["thin"]),
                         ("holds", "49/50", False))
        self.assertEqual(a["per_run"], {"c": ["19/20", "17/20", "23/25"]})
        self.assertEqual(a["holds_at"], ">=")

    def test_ch_b_is_the_difference_of_the_medians_and_holds_at_or_below(self):
        r = runs(c=[{"space": F(90, 100)}, {"space": F(92, 100)}, {"space": F(80, 100)}],
                 e=[{"space": F(96, 100)}, {"space": F(95, 100)}, {"space": F(89, 100)}])
        b = score.row("CH-b", r)
        self.assertEqual(b["value"]["fraction"], str(F(95, 100) - F(90, 100)))
        self.assertEqual((b["verdict"], b["holds_at"]), ("holds", "<="))
        self.assertTrue(b["thin"])           # c's 0.80 in its place gives 0.15

    def test_ch_c_and_ch_e_read_the_recall(self):
        r = runs(c=[{"oncall": F(2, 3)}, {"oncall": F(1)}, {"oncall": F(1)}],
                 e=[{"oncall": F(14, 15)}, {"oncall": F(1)}, {"oncall": F(11, 15)}])
        c, e_ = score.row("CH-c", r), score.row("CH-e", r)
        self.assertEqual((c["verdict"], c["value"]["fraction"], c["thin"]), ("holds", "1", True))
        self.assertEqual((e_["verdict"], e_["value"]["fraction"], e_["thin"]),
                         ("holds", "14/15", True))

    def test_ch_f_is_a_ratio_of_medians_of_calls(self):
        r = runs(c=[{"calls": 150}, {"calls": 160}, {"calls": 90}],
                 e=[{"calls": 200}, {"calls": 189}, {"calls": 233}])
        f = score.row("CH-f", r)
        self.assertEqual(f["value"]["fraction"], str(F(150, 200)))
        self.assertEqual(f["verdict"], "holds")              # exactly 3/4
        self.assertTrue(f["thin"])
        none = score.row("CH-f", runs(c=[{"calls": 3}] * 2, e=[{"calls": 0}] * 2))
        self.assertEqual(none["verdict"], "unadjudicable")

    def test_medians_of_three_and_of_two(self):
        self.assertEqual(score.median([F(1), F(3), F(2)]), F(2))
        self.assertEqual(score.median([F(1), F(2)]), F(3, 2))
        r = runs(c=[{"space": F(89, 100)}, {"space": F(91, 100)}], e=[{}, {}])
        self.assertEqual(score.row("CH-a", r)["value"]["fraction"], "9/10")

    def test_an_arm_with_one_run_gives_no_value_to_every_row_that_reads_it(self):
        r = runs(c=[{}], e=[{}, {}])
        for rid in score.ROWS:
            got = score.row(rid, r)
            reads_c = "c" in score.ROWS[rid][0]
            with self.subTest(rid):
                self.assertEqual(got["verdict"] == "unadjudicable", reads_c)

    def test_the_calls_are_counted_and_the_refused_attempts_not_read(self):
        answered = {"provider": plan.PROVIDER_NAME, "reasoning_tokens": 10,
                    "finish_reason": "stop", "error": None, "prompt_tokens": 5,
                    "completion_tokens": 7}
        rec = {"escalations": [{"calls": [
            {"round": 0, "seconds": 20.0, "call_attempts": [dict(answered)], "retries": [],
             "failure": None, "served_by": plan.PROVIDER_NAME},
            {"round": 0, "seconds": 400.0, "call_attempts": [dict(REFUSED), dict(answered)],
             "retries": ["call"], "failure": None, "served_by": plan.PROVIDER_NAME},
            {"round": 1, "seconds": 30.0,
             "call_attempts": [{**answered, "provider": "Elsewhere"}], "retries": [],
             "failure": None, "served_by": "Elsewhere"},
            {"round": 0, "seconds": 3.0, "call_attempts": [], "retries": [],
             "failure": "sin objeto JSON", "served_by": None}]}]}
        got = score.calls_of(rec)
        self.assertEqual((got["calls"], got["failed"], got["served_elsewhere"]), (4, 1, 1))
        self.assertEqual((got["attempts"], got["rate_limited"]), (4, 1))
        self.assertEqual(got["providers"], {plan.PROVIDER_NAME: 2, "Elsewhere": 1})
        self.assertEqual(got["reasoning_tokens"]["median"], 10)
        self.assertEqual(got["seconds_by_round"]["0"], {"calls": 3, "median": 20.0, "sum": 423.0})
        self.assertEqual(got["seconds_by_round_unlimited"]["0"],
                         {"calls": 2, "median": 11.5, "sum": 23.0})
        self.assertEqual(got["retries"], {"call": 1})
        self.assertEqual(score.calls_made(rec), 4)

    def test_the_channels_reports_by_queue_rule_and_time(self):
        rows = [{"idx": 0, "reported": None, "cause": "IMPASSE", "truth": T1, "truth_rule": "H29"},
                {"idx": 5, "reported": True, "cause": "ERROR", "truth": T2, "truth_rule": "H16"},
                {"idx": 250, "reported": False, "cause": None, "truth": T2, "truth_rule": "H16"},
                {"idx": 260, "reported": True, "cause": "ERROR", "truth": S, "truth_rule": "H01"}]
        got = score.reports_of({"records": rows})
        self.assertEqual(got["all"], [3, 2, 2])
        self.assertEqual(got["by_queue"], {T2: [2, 1, 1], S: [1, 1, 1]})
        self.assertEqual(got["by_rule"], {"H01": [1, 1, 1], "H16": [2, 1, 1]})
        self.assertEqual(got["over_time"], {"0": [1, 1, 1], "200": [2, 1, 1]})

    def test_the_error_escalations_beside_the_supply(self):
        rec = {"records": [{"cause": "ERROR", "truth_rule": "H04"},
                           {"cause": None, "truth_rule": "H04"},
                           {"cause": "ERROR", "truth_rule": "H05"}]}
        supply = {"rules": {"H04": {"tickets": 4, "reportable": [2, 2, 2]},
                            "H05": {"tickets": 3, "reportable": [1, 0, 1]}}}
        self.assertEqual(score.errors_by_rule(rec, "c", 2, supply)["rules"],
                         {"H04": [1, 4, 2], "H05": [1, 3, 0]})
        self.assertEqual(score.errors_by_rule(rec, "e", 2, supply)["rules"],
                         {"H04": [1, 4, 4], "H05": [1, 3, 3]})


if __name__ == "__main__":
    unittest.main()
