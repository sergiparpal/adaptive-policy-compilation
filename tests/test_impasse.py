"""
`PLAN_IMPASSE.md`'s instrument, `impasse/`. **No figure of the plan**: no test runs
the loop over the corpus, and every ticket, run and record below is built by
hand. The figures §0 declares are recomputed by `IM-g2`, `IM-g3` and Stage A,
never here; what is pinned here is that `DECLARED` is the plan's text.

What is pinned:

  1. §11's constants, the seed, `DEFAULTS` and §0's lines with their sides,
     `DECLARED` against §0's text, the schedule, and the gate, which counts every
     signature line, never whether the plan is signed.
  2. The notice's paragraph: its digest, that it is `PLAN_CAUSE.md`'s arm `i`'s,
     v2b's paragraph and the notice, that it names no queue and no rule, and that
     the plan quotes it byte for byte.
  3. v1n's messages: v1c's at no impasse, and v1c's with the one paragraph
     replaced at an impasse, on both calls; a first message that is not v1c's
     refused; the texts' digests and fingerprints of both arms.
  4. v1n's proposer and escalation: the flag set from the cause alone, false at a
     conflict and at an error, and cleared after every escalation, even one that
     raised; each arm's class sending its own messages; a loop on a corpus built by
     hand giving the same record under both arms, with the notice sent at its
     impasses and nowhere else.
  5. The resume, and that a run cannot resume under the other arm or other draws.
  6. Nothing is built, asked or written while the plan is unsigned; the dry runs
     build no client; a run refuses before the key without what must come before
     it; the turn.
  7. The smoke check, with the notice at the impasses alone.
  8. The request is `PLAN_PLACEMENT.md`'s for both arms, and the SDK double
     receives the notice and the pin.
  9. The statistics on drafts built by hand, and Stage C's terms: exact lines on
     every side, medians, `IM-b`'s pooled share and its thin, every reason a row
     has no value, and the word for a row of no value the prose test reads.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import Case

from authorship import protocol as e
from authorship import run as erun
from cause import prompts as cprompts
from manual import instrument as MI
from placement import loop as pl_loop
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import ProposalError, user_msg

from impasse import gates, plan, protocol, references, run, sample, score

from tests import test_prose_tables as prose
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
F = Fraction
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
PLAN_TEXT = (REPO / "PLAN_IMPASSE.md").read_text()
FLAT = " ".join(PLAN_TEXT.split())


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


API = (T2, ("product", "eq", "api"))
API_LOW = (T3, ("product", "eq", "api"), ("severity", "gte", 3))
SEVERE = (T3, ("severity", "lte", 2))


class LiveScript:
    """A live model that answers or raises what it is handed, one per call, and
    keeps every message list it was sent."""

    def __init__(self, *items):
        self.items, self.extra, self.sent = list(items), {}, []

    def ask(self, messages):
        self.sent.append(messages)
        got = self.items.pop(0)
        if isinstance(got, Exception):
            raise got
        self.extra = got.extra()
        return got


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_and_the_pin_are_plan_placements(self):
        for k in ("MODEL", "PROMPT", "TEMPERATURE", "REASONING", "MAX_TOKENS", "MAX_RETRIES",
                  "CALL_RETRY_WAIT", "RATE_LIMITED", "RATE_LIMIT_WAIT", "PROVIDER",
                  "PROVIDER_NAME", "LEVEL", "SYSTEM_PROMPT_SHA16", "COVERAGE", "N", "SEED",
                  "IMPASSE", "CONFLICT", "ERROR", "CAUSES"):
            with self.subTest(k):
                self.assertEqual(getattr(plan, k), getattr(pl_plan, k))
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, "DeepInfra")
        self.assertEqual(plan.settings(), pl_plan.settings())

    def test_the_arms_and_the_runs(self):
        self.assertEqual(plan.PROTOCOLS, ("v1c", "v1n"))
        self.assertEqual(plan.ARMS, ("v1c", "v1n"))
        self.assertEqual(plan.COVERAGE, F(1, 2))
        self.assertEqual((plan.REPS, plan.N, plan.SEED), (3, 2000, 17))
        self.assertEqual((plan.SMOKE_N, plan.SMOKE_ARM), (30, "v1n"))
        self.assertEqual((plan.MAX_ESCALATIONS, plan.MAX_CONSECUTIVE_FAILURES), (400, 5))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        self.assertEqual(plan.DEFAULTS, ("H08", "H27", "H28", "H29"))

    def test_the_seed_is_the_next_prime_after_113_and_no_closed_threads(self):
        def prime(n):
            return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))
        self.assertEqual(plan.ORDER_SEED, next(n for n in range(114, 200) if prime(n)))
        taken = set()
        for path in REPO.glob("*/plan.py"):
            if path.parent.name == "impasse":
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, int)
                        and any(isinstance(t, ast.Name) and t.id.endswith("SEED")
                                for t in node.targets)):
                    taken.add(node.value.value)
        self.assertNotIn(plan.ORDER_SEED, taken)
        self.assertIn(113, taken)

    def test_the_lines_are_section_0s_as_fractions_on_their_sides(self):
        self.assertEqual(plan.LINES, {"IM-a": F(1, 5), "IM-b": F(1, 3), "IM-c": F(1, 100),
                                      "IM-d": F(1, 40), "IM-e": F(3, 4), "IM-f": F(3, 4)})
        self.assertEqual(plan.SIDES, {"IM-a": ">=", "IM-b": "<", "IM-c": ">=",
                                      "IM-d": "<=", "IM-e": "<=", "IM-f": ">="})
        self.assertEqual(plan.IM_B_MIN, 5)
        for v in plan.LINES.values():
            self.assertIsInstance(v, Fraction)

    def test_the_plan_states_them(self):
        for text in ("`ORDER_SEED = 127`", "`IM_A_LINE = Fraction(1, 5)`",
                     "`IM_B_LINE = Fraction(1, 3)`", "`IM_C_LINE = Fraction(1, 100)`",
                     "`IM_D_LINE = Fraction(1, 40)`", "`IM_E_LINE = Fraction(3, 4)`",
                     "`IM_F_LINE = Fraction(3, 4)`", "`IM_B_MIN = 5`",
                     "`SMOKE_N = 30`", '`SMOKE_ARM = "v1n"`', "`MAX_ESCALATIONS = 400`",
                     "`MIN_SIGNATURES = 1`", '"deepinfra/fp8"',
                     '`DEFAULTS = ("H08", "H27", "H28", "H29")`',
                     f"`NOTICE_BASE_SHA16 = \"{plan.NOTICE_BASE_SHA16}\"`",
                     f"`BLIND_BASE_SHA16 = \"{plan.BLIND_BASE_SHA16}\"`"):
            with self.subTest(text):
                self.assertIn(text, PLAN_TEXT)

    def test_declared_transcribes_section_0(self):
        d = plan.DECLARED
        names = {"pl_v1c": "`PLAN_PLACEMENT.md`'s v1c", "wh_v1c": "`PLAN_WHOLE.md`'s v1c",
                 "wh_v1d": "`PLAN_WHOLE.md`'s v1d"}

        def run_name(key):
            return f"{names[key[:6]]} r{key[-1]}"
        for key, (n, imp, con, err) in d["escalations"].items():
            with self.subTest(figure=1, run=key):
                self.assertIn(f"| {run_name(key)} | {n} | {imp} | {con} | {err} |", PLAN_TEXT)
        for key, by in d["whole_by_cause"].items():
            cells = " | ".join(f"{by[c][0]} of {by[c][1]}" for c in ("IMPASSE", "CONFLICT",
                                                                     "ERROR"))
            with self.subTest(figure=2, run=key):
                self.assertIn(f"| {run_name(key)} | {cells} |", PLAN_TEXT)
        for key, by in d["groups"].items():
            if key.startswith("wh_v1d"):
                continue
            cells = " | ".join(f"{by[g][0]} of {by[g][1]}" for g in ("none", "few", "many"))
            with self.subTest(figure=3, run=key):
                self.assertIn(f"| {run_name(key)} | {cells} |", PLAN_TEXT)
        pooled = d["groups_pooled_v1c"]
        self.assertIn("| v1c, pooled | " + " | ".join(
            f"{pooled[g][0]} of {pooled[g][1]}" for g in ("none", "few", "many")) + " |",
            PLAN_TEXT)
        met = d["impasses_at_defaults_v1c"]
        self.assertIn(f"met `H29`'s tickets {met['H29']} times, `H28`'s {met['H28']} and "
                      f"`H08`'s {met['H08']}, and `H27`'s none", FLAT)
        self.assertEqual(met["H27"], 0)
        for key, b in d["born"].items():
            with self.subTest(figure=4, run=key):
                self.assertIn(f"| {run_name(key)} | {b['whole']} | {b['born']} | "
                              f"{b['unplaced']} | {b['refused']} |", PLAN_TEXT)
        for key, row in d["lost"].items():
            cells = " | ".join(f"{x:,}" for x in row)
            with self.subTest(figure=5, run=key):
                self.assertIn(f"| {run_name(key)} | {cells} |", PLAN_TEXT)
        words = {"IMPASSE": "an impasse", "ERROR": "a reported error",
                 "decided": "decided, not escalated"}
        cls = {"cut_by_one": "cut by one rule", "whole": "whole", None: "—"}
        verdicts = {"nacida": "born", "rechazada": "refused", None: "—"}
        for key, (how, c, v, later) in d["h01_case_44"].items():
            with self.subTest(figure=6, run=key):
                self.assertIn(f"| {run_name(key)} | {words[how]} | {cls[c]} | {verdicts[v]} |",
                              PLAN_TEXT)
        order = ", ".join(f"{a} r{r}" for a, r in d["schedule"][:-1]) \
            + f" and {d['schedule'][-1][0]} r{d['schedule'][-1][1]}"
        self.assertIn(order, FLAT)
        g = d["groups_of_rules"]
        self.assertEqual(g["many"], list(plan.DEFAULTS))
        self.assertIn("**Few, one to three**: " + ", ".join(f"`{r}`" for r in g["few"][:-1])
                      + f" and `{g['few'][-1]}`", FLAT)

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        first = random.Random("PLAN_IMPASSE/order/127").choice(plan.ARMS)
        self.assertEqual(order[0], (first, 1))
        self.assertEqual([list(x) for x in order], plan.DECLARED["schedule"])
        arms = [a for a, _ in order]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))

    def test_the_schedule_is_the_same_under_any_hash_seed(self):
        code = "import json; from impasse import plan; print(json.dumps(plan.schedule()))"
        outs = set()
        for seed in ("0", "1", "4242"):
            env = {**os.environ, "PYTHONHASHSEED": seed}
            outs.add(subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                                    capture_output=True, text=True, check=True).stdout)
        self.assertEqual(len(outs), 1)

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            for path in (plan.sample_path(), plan.score_path(), plan.smoke_path(),
                         plan.run_path("v1n", 1), plan.partial_path("v1c_r2")):
                self.assertEqual(path.parent, d)
        with self.assertRaises(ValueError):
            plan.run_path("v1d", 1)
        with self.assertRaises(ValueError):
            plan.run_path("v1n", 4)

    def test_both_arms_read_plan_placements_draws(self):
        for arm in plan.ARMS:
            for rep in (1, 2, 3):
                with self.subTest(arm=arm, rep=rep):
                    self.assertEqual(plan.channel_of(arm, rep), pl_plan.channel_of("v1c", rep))
                    self.assertEqual(plan.channel_of(arm, rep)["draws_seed"],
                                     f"PLAN_CHANNEL/channel/97/r{rep}")
            self.assertEqual(plan.channel_of(arm, None)["draws_seed"],
                             "PLAN_CHANNEL/channel/97/smoke")


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_every_line_is_counted_and_one_is_needed(self):
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-28)**\n"
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
        self.assertEqual(plan.gate_signature(REPO / "PLAN_IMPASSE.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_IMPASSE.md"))
        self.assertEqual(plan.gate_signature()["source"], "PLAN_IMPASSE.md")


# ---------------------------------------------------------------------------
# 2. The notice's paragraph
# ---------------------------------------------------------------------------

class TestTheNotice(unittest.TestCase):

    def test_it_is_plan_causes_arm_i_byte_for_byte(self):
        self.assertEqual(protocol.NOTICE_BASE, cprompts.PARAGRAPHS["i"])
        self.assertEqual(protocol.NOTICE_BASE, p.BLIND_BASE + "\n" + protocol.NOTICE)
        self.assertEqual(protocol.NOTICE,
                         "AVISO DEL MOTOR: ninguna regla de la base casa este ticket. Por "
                         "eso no ha podido\ndecidirlo.\n")
        self.assertEqual(sha16(protocol.NOTICE_BASE), plan.NOTICE_BASE_SHA16)
        self.assertEqual(sha16(p.BLIND_BASE), plan.BLIND_BASE_SHA16)
        self.assertTrue(protocol.NOTICE_BASE.isascii() and protocol.NOTICE_BASE.endswith("\n"))

    def test_it_names_no_queue_and_no_rule(self):
        self.assertTrue(protocol.names_nothing(protocol.NOTICE_BASE))
        for bad in ("gana a H04", "manda a ONCALL_ESCALATION", "cita R0001"):
            with self.subTest(bad):
                self.assertFalse(protocol.names_nothing(protocol.NOTICE_BASE + bad))

    def test_the_plan_quotes_it_byte_for_byte(self):
        path = REPO / "PLAN_IMPASSE.md"
        self.assertTrue(gates.quoted_in_the_plan(protocol.NOTICE_BASE, path))
        self.assertFalse(gates.quoted_in_the_plan(
            protocol.NOTICE_BASE.replace("ninguna", "una"), path))
        self.assertFalse(gates.quoted_in_the_plan(protocol.NOTICE_BASE.rstrip("\n"), path))


# ---------------------------------------------------------------------------
# 3. The messages
# ---------------------------------------------------------------------------

class TestTheMessages(unittest.TestCase):

    def setUp(self):
        self.case = case(product="api")
        self.draft = answer(payload(*API))

    def test_no_impasse_gives_v1cs_messages_back(self):
        self.assertEqual(protocol.messages_for(self.case), p.messages_for(self.case))
        self.assertEqual(protocol.messages_for(self.case, self.draft, "lista"),
                         p.messages_for(self.case, self.draft, "lista"))

    def test_an_impasse_is_v1c_one_paragraph_apart_on_both_calls(self):
        for prev, msg in ((None, ""), (self.draft, "lista")):
            with self.subTest(placement=prev is not None):
                ours = protocol.messages_for(self.case, prev, msg, impasse=True)
                theirs = p.messages_for(self.case, prev, msg)
                self.assertTrue(protocol.apart_by_the_notice(theirs, ours))
                self.assertEqual(ours[1], {"role": "user",
                                           "content": user_msg(self.case, protocol.NOTICE_BASE)})
                self.assertEqual([m for k, m in enumerate(ours) if k != 1],
                                 [m for k, m in enumerate(theirs) if k != 1])

    def test_apart_by_the_notice_has_teeth(self):
        theirs = p.messages_for(self.case, self.draft, "lista")
        ours = protocol.messages_for(self.case, self.draft, "lista", impasse=True)
        self.assertTrue(protocol.apart_by_the_notice(theirs, ours))
        system = [dict(ours[0], content="otro"), *ours[1:]]
        other = protocol.messages_for(case(product="billing"), self.draft, "lista",
                                      impasse=True)
        same = protocol.messages_for(self.case, self.draft, "lista")
        for name, bad in (("system", system), ("ticket", other), ("no notice", same),
                          ("short", ours[:3])):
            with self.subTest(name):
                self.assertFalse(protocol.apart_by_the_notice(theirs, bad))

    def test_a_first_message_that_is_not_v1cs_is_refused(self):
        odd = [{"role": "system", "content": "s"}, {"role": "user", "content": "otra cosa"}]
        with mock.patch.object(p, "messages_for", return_value=odd):
            for impasse in (False, True):
                with self.subTest(impasse=impasse), self.assertRaises(protocol.NotV1c):
                    protocol.messages_for(self.case, impasse=impasse)

    def test_the_texts_digests_and_fingerprints(self):
        self.assertEqual(protocol.texts("v1c"), p.texts())
        self.assertEqual(protocol.digests("v1c"), p.digests())
        self.assertEqual(protocol.fingerprint("v1c"), p.fingerprint())
        c, n = protocol.digests("v1c"), protocol.digests("v1n")
        self.assertEqual(sorted(n), sorted([*c, "notice_base"]))
        for k in c:
            self.assertEqual(n[k], c[k])
        self.assertEqual(n["notice_base"], plan.NOTICE_BASE_SHA16)
        self.assertNotEqual(protocol.fingerprint("v1n"), protocol.fingerprint("v1c"))
        with self.assertRaises(ValueError):
            protocol.texts("v1d")


# ---------------------------------------------------------------------------
# 4. The proposer, the escalation, and a loop on a corpus built by hand
# ---------------------------------------------------------------------------

def corpus() -> list[Case]:
    """Case 0 is an impasse on the empty base, which writes the API rule. Case 1
    is an api ticket the API rule decides wrongly, reported under its draw: an
    error escalation, whose draft lies inside the API rule, so no round is sent.
    Case 2 is an impasse whose draft crosses the API rule, so v1c's list holds it
    and a placement round is sent."""
    return [case(product="api"), case(product="api", severity=4),
            case(product="dashboard", severity=1)]


LABELS = [(T2, "H16"), (T3, "H15"), (T3, "H06")]
DRAWS = [0.9, 0.1, 0.9]


def answers() -> list[p.Answer]:
    return [answer(payload(*API)), answer(payload(*API_LOW)), answer(payload(*SEVERE)),
            answer(payload(*SEVERE, beats=["R0001"]))]


def looped(arm: str, d: Path, notice: bool = True):
    """The loop under `arm`'s escalation with `arm`'s proposer class over a live
    double serving `answers()` in order."""
    live = LiveScript(*answers())
    path = d / f"{arm}_{notice}.partial.jsonl"
    rows, _ = erun.open_partial(path, {"plan": "test", "arm": arm})
    prop = protocol.PROPOSERS[arm](live, path, rows)
    if not notice:
        prop.notice = False
    eng = PriorityEngine(space=MI.space())
    res = pl_loop.run_loop(corpus(), LABELS, eng, prop, F(1, 2), DRAWS,
                           propose=protocol.ESCALATIONS[arm], clock=lambda: 0.0)
    prop.flush()
    return gates.as_json(pl_loop.record_of(res, eng)), live.sent, prop


class TestTheProposer(unittest.TestCase):

    def test_the_classes_and_the_escalations(self):
        self.assertIs(protocol.PROPOSERS["v1c"], pl_run.Stamped)
        self.assertTrue(issubclass(protocol.PROPOSERS["v1n"], pl_run.Stamped))
        self.assertIs(protocol.ESCALATIONS["v1c"], pl_loop.ESCALATIONS["v1c"])
        self.assertIs(protocol.ESCALATIONS["v1n"], protocol.propose_v1n)

    def test_the_flag_reads_the_cause_alone_and_is_cleared(self):
        seen = []

        def fake(engine, case_, idx, cause, proposer, channels, clock=None):
            seen.append((cause, proposer.impasse))
            if cause == "BOOM":
                raise RuntimeError("boom")
            return {}
        prop = SimpleNamespace(impasse=False)
        with mock.patch.object(pl_protocol, "propose_v1c", side_effect=fake):
            for cause in (plan.IMPASSE, plan.CONFLICT, plan.ERROR):
                protocol.propose_v1n(None, case(), 0, cause, prop, [])
                self.assertFalse(prop.impasse)
            with self.assertRaises(RuntimeError):
                protocol.propose_v1n(None, case(), 0, "BOOM", prop, [])
            self.assertFalse(prop.impasse)
        self.assertEqual(seen, [(plan.IMPASSE, True), (plan.CONFLICT, False),
                                (plan.ERROR, False), ("BOOM", False)])

    def test_each_arm_sends_its_own_messages(self):
        c, draft = case(product="api"), answer(payload(*API))
        with tempfile.TemporaryDirectory() as d:
            for arm, impasse in (("v1c", True), ("v1n", True), ("v1n", False)):
                with self.subTest(arm=arm, impasse=impasse):
                    live = LiveScript(answer(payload(*API)), answer(payload(*API)))
                    path = Path(d) / f"{arm}_{impasse}.partial.jsonl"
                    rows, _ = erun.open_partial(path, {"plan": "test"})
                    prop = protocol.PROPOSERS[arm](live, path, rows)
                    prop.impasse = impasse
                    prop.first(c, 0)
                    prop.placement(c, draft, "lista", 0)
                    told = arm == "v1n" and impasse
                    self.assertEqual(live.sent, [
                        protocol.messages_for(c, impasse=told),
                        protocol.messages_for(c, draft, "lista", impasse=told)])
                    if arm == "v1n":
                        self.assertEqual(prop.notice_at, [0] if told else [])

    def test_a_loop_gives_the_same_record_with_the_notice_at_its_impasses_alone(self):
        with tempfile.TemporaryDirectory() as d:
            rec_c, sent_c, _ = looped("v1c", Path(d))
            rec_n, sent_n, prop_n = looped("v1n", Path(d))
            rec_0, sent_0, prop_0 = looped("v1n", Path(d), notice=False)
        self.assertEqual(rec_c, rec_n)
        self.assertEqual(rec_c, rec_0)
        self.assertEqual(sent_0, sent_c)
        self.assertEqual(prop_0.notice_at, [])
        self.assertEqual([x["kind"] for x in rec_c["escalations"]],
                         [plan.IMPASSE, plan.ERROR, plan.IMPASSE])
        self.assertEqual([len(m) for m in sent_c], [2, 2, 2, 4])   # a round at case 2 alone
        self.assertEqual(prop_n.notice_at, [0, 2])
        told = [True, False, True, True]             # the calls of cases 0, 1, 2 and 2
        for theirs, ours, t in zip(sent_c, sent_n, told):
            if t:
                self.assertTrue(protocol.apart_by_the_notice(theirs, ours))
            else:
                self.assertEqual(theirs, ours)
        self.assertEqual([r["action"] for r in rec_c["rules"]], [T2, T3, T3])
        self.assertEqual(rec_c["escalations"][2]["listed"], ["R0001"])

    def test_the_proposers_path_names_no_policy(self):
        for rel in ("impasse/protocol.py", "impasse/run.py"):
            tree = ast.parse((REPO / rel).read_text())
            names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names |= {a.name for a in node.names}
                elif isinstance(node, ast.ImportFrom):
                    names |= {node.module or ""} | {a.name for a in node.names}
            with self.subTest(rel):
                self.assertFalse({n for n in names for bad in (
                    "hidden_policy", "HIDDEN_DSL", "ceiling_check", "hidden_priority",
                    "rung4") if bad in n})

    def test_no_comparison_with_the_label_on_the_proposers_path(self):
        found = []
        for rel in ("impasse/run.py", "impasse/protocol.py", "impasse/plan.py"):
            tree = ast.parse((REPO / rel).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare) and any(
                        isinstance(n, ast.Name) and n.id in ("truth", "trule", "labels")
                        for x in (node.left, *node.comparators) for n in ast.walk(x)):
                    found.append((rel, ast.unparse(node)))
        self.assertEqual(found, [])
        self.assertTrue(gates.no_label_on_the_proposers_path()["passes"])


# ---------------------------------------------------------------------------
# 5. The resume
# ---------------------------------------------------------------------------

class TestTheResume(unittest.TestCase):

    def test_a_resumed_v1n_record_keeps_each_calls_own_seconds_and_hour(self):
        header = {"plan": "test"}
        corp, labels = [case(product="api"), case()], [(T2, "H16"), (T1, "H29")]
        catch_all = payload(T1, ("severity", "gte", 1))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, header)
            live = protocol.Stamped(LiveScript(e.ProposalFailed("no parse", "stop", 3, []),
                                               answer(catch_all)),
                                    path, rows, clock=iter([0.0, 7.5, 10.0, 52.0]).__next__)
            asked = pl_loop.run_loop(corp, labels, PriorityEngine(space=MI.space()), live,
                                     F(1, 2), [0.1, 0.9], propose=protocol.propose_v1n,
                                     clock=itertools.count(0.0, 5.0).__next__)
            live.flush()
            kept = [json.loads(x) for x in path.read_text().splitlines()[1:]]
            self.assertTrue(all(r.get("kept_at") for r in kept))
            rows, resumed = erun.open_partial(path, header)
            self.assertTrue(resumed)
            again = protocol.Stamped(LiveScript(), path, rows)
            served = pl_loop.run_loop(corp, labels, PriorityEngine(space=MI.space()), again,
                                      F(1, 2), [0.1, 0.9], propose=protocol.propose_v1n,
                                      clock=itertools.count(0.0, 0.01).__next__)
        for res, seconds in ((asked, [5.0, 5.0]), (served, [7.5, 42.0])):
            with self.subTest(seconds=seconds):
                calls = [esc.calls[0] for esc in res.loop.escalations]
                self.assertEqual([c["seconds"] for c in calls], seconds)
        self.assertEqual(live.notice_at, again.notice_at)
        self.assertEqual(again.notice_at, [0, 1])

    def test_a_stored_answer_paid_for_under_the_other_arms_request_is_refused(self):
        """A partial file's rows carry their request's digest: v1n at an impasse
        cannot be served an answer v1c's request paid for."""
        c = case(product="api")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, {"plan": "test"})
            pl_run.Stamped(LiveScript(answer(payload(*API))), path, rows).first(c, 0)
            rows, _ = erun.open_partial(path, {"plan": "test"})
            prop = protocol.Stamped(LiveScript(), path, rows)
            prop.impasse = True
            with self.assertRaises(erun.Desync):
                prop.first(c, 0)

    def test_a_partial_under_the_other_arm_or_other_draws_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            mine = run.protocol_header("v1n", plan.N, "v1n_r1", 1)
            erun.open_partial(path, mine)
            for other in (run.protocol_header("v1c", plan.N, "v1n_r1", 1),
                          run.protocol_header("v1n", plan.N, "v1n_r1", 2)):
                self.assertNotEqual(other, mine)
                with self.assertRaises(SystemExit):
                    erun.open_partial(path, other)

    def test_the_header_names_the_plan_the_pin_the_protocol_and_the_texts(self):
        h = run.protocol_header("v1n", plan.N, "v1n_r2", 2)
        self.assertEqual((h["plan"], h["protocol"], h["provider"]),
                         ("PLAN_IMPASSE.md", "v1n", plan.PROVIDER))
        self.assertEqual(h["texts_sha16"], protocol.digests("v1n"))
        self.assertEqual(h["fingerprint"], protocol.fingerprint("v1n"))
        self.assertEqual(h["draws_seed"], "PLAN_CHANNEL/channel/97/r2")
        c = run.protocol_header("v1c", plan.N, "v1c_r2", 2)
        self.assertEqual((c["fingerprint"], c["texts_sha16"]), (p.fingerprint(), p.digests()))
        placement_header = pl_run.protocol_header("v1c", plan.N, "v1c_r2", 2)
        self.assertEqual({k: v for k, v in c.items() if k != "plan"},
                         {k: v for k, v in placement_header.items() if k != "plan"})
        self.assertEqual(run.notice_text("v1n"), protocol.NOTICE_BASE)
        self.assertIsNone(run.notice_text("v1c"))

    def test_the_loop_does_not_swallow_an_outage(self):
        class Refused:
            name = "refused"
            impasse = False

            def first(self, case, idx):
                raise p.RateLimited("refused")

        with self.assertRaises(p.RateLimited):
            pl_loop.run_loop([case()], [(T1, "H29")], PriorityEngine(space=MI.space()),
                             Refused(), F(1, 2), [0.3], propose=protocol.propose_v1n)


# ---------------------------------------------------------------------------
# 6. Nothing unsigned, and the order of events
# ---------------------------------------------------------------------------

def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED)


def stage_a(d: Path, **over) -> None:
    refs = {"fingerprints": {a: protocol.fingerprint(a) for a in plan.ARMS},
            "schedule": [list(x) for x in plan.schedule()],
            "streams": {n: {"seed": plan.draw_seed(n), "sha16": plan.draws_digest(n)}
                        for n in plan.STREAMS}}
    refs.update(over)
    (d / "sample.json").write_text(json.dumps({"references": refs}))


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(pl_protocol, "Asker",
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
             mock.patch.object(pl_protocol, "Asker",
                               side_effect=AssertionError("asker built")) as asker, \
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
            for argv in (["--smoke"], ["--arm", "v1c", "--rep", "1"]):
                with self.subTest(argv), self.assertRaises(SystemExit):
                    run.main(argv)           # no Stage A record
            stage_a(d)
            self.assertTrue(run.sample_check()[0])
            with self.assertRaises(SystemExit):
                run.main(["--arm", "v1c", "--rep", "1"])      # no smoke record
        fetch.assert_not_called()
        checks.assert_not_called()

    def test_a_stage_a_record_under_another_schedule_draws_or_texts_is_refused(self):
        with TempOut() as d:
            for over in ({"schedule": [["v1n", 1]]},
                         {"streams": {"r1": {"seed": "x", "sha16": "y"}}},
                         {"fingerprints": {"v1c": p.fingerprint(), "v1n": "0" * 16}}):
                stage_a(d, **over)
                with self.subTest(over=list(over)):
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
# 7. The smoke check
# ---------------------------------------------------------------------------

REFUSED = {"provider": None, "reasoning_tokens": None, "finish_reason": None,
           "error": plan.RATE_LIMITED}
SMOKE_DRAWS = plan.draws("smoke")[:plan.SMOKE_N]


def smoke_rows() -> list[dict]:
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
    rec = {**run.protocol_header(plan.SMOKE_ARM, plan.SMOKE_N, "smoke", None),
           "base_text": p.BLIND_BASE, "notice_text": protocol.NOTICE_BASE, "notice_at": [0],
           "metrics": {"n_rules": 1},
           "escalations": [{"idx": 0, "kind": "IMPASSE", "calls": calls},
                           {"idx": 5, "kind": "ERROR",
                            "calls": [{"round": 0, "failure": None,
                                       "call_attempts": [dict(attempt)]}]}],
           "records": smoke_rows()}
    rec.update(over)
    return rec


class TestTheSmokeCheck(unittest.TestCase):

    def check(self, rec) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            path.write_text(json.dumps(rec))
            return run.smoke_check(path)

    def test_a_clean_smoke_run_passes(self):
        ok, why = self.check(smoke_record())
        self.assertTrue(ok, why)
        self.assertIn("1 placements answered", why)
        self.assertIn("the notice sent at the 1 impasses alone", why)

    def test_attempts_refused_for_the_rate_are_counted_and_not_read(self):
        rec = smoke_record()
        rec["escalations"][0]["calls"][0]["call_attempts"][:0] = [REFUSED, REFUSED]
        ok, why = self.check(rec)
        self.assertTrue(ok)
        self.assertIn("2 refused for the rate", why)

    def test_each_failure(self):
        bad = smoke_record()
        bad["escalations"][0]["calls"][0]["call_attempts"][0]["provider"] = "Baidu"
        quiet = smoke_record()
        quiet["escalations"][0]["calls"][1]["call_attempts"][0]["reasoning_tokens"] = 0
        cut = smoke_record()
        cut["escalations"][0]["calls"][0]["call_attempts"][0]["finish_reason"] = "length"
        unplaced = smoke_record()
        unplaced["escalations"][0]["calls"] = unplaced["escalations"][0]["calls"][:1]
        lost = smoke_record(records=smoke_rows()[:-1])
        other = smoke_record(protocol="v1c")
        no_notice = smoke_record(notice_text=None)
        wrong_base = smoke_record(base_text=protocol.NOTICE_BASE)
        everywhere = smoke_record(notice_at=[0, 5])
        nowhere = smoke_record(notice_at=[])
        no_impasse = smoke_record(notice_at=[])
        no_impasse["escalations"][0]["kind"] = "CONFLICT"
        unborn = smoke_record(metrics={"n_rules": 0})
        for name, rec in (("elsewhere", bad), ("did not reason", quiet), ("cut", cut),
                          ("no placement", unplaced), ("rows", lost), ("protocol", other),
                          ("no notice text", no_notice), ("base text", wrong_base),
                          ("notice at an error", everywhere), ("notice missing", nowhere),
                          ("no impasse", no_impasse), ("no rule", unborn)):
            with self.subTest(name):
                self.assertFalse(self.check(rec)[0])


# ---------------------------------------------------------------------------
# 8. The request
# ---------------------------------------------------------------------------

class DeepInfraReasons(OpenRouterShapedClient):
    PROVIDER = "DeepInfra"


class TestTheRequest(unittest.TestCase):

    def test_both_arms_send_plan_placements_request(self):
        msgs = protocol.messages_for(case(), impasse=True)
        holder = SimpleNamespace(model=plan.MODEL)
        for attempt in (0, 1):
            got = [pl_protocol.request_with(plan.PROVIDER, plan.MODEL, arm, msgs, attempt)
                   for arm in plan.ARMS]
            self.assertEqual(got[0], got[1])
            theirs = p.Asker.request(holder, "v1b", msgs, attempt)
            self.assertEqual(got[0]["extra_body"]["provider"], plan.PROVIDER)
            got[0]["extra_body"]["provider"] = theirs["extra_body"]["provider"]
            self.assertEqual(got[0], theirs)
        self.assertTrue(gates.requests()["passes"])

    def test_the_asker_sends_the_notice_and_the_pin_through_the_sdk(self):
        client = DeepInfraReasons(FixedResponses(json.dumps(payload(*API))))
        with fake_sdk(openai=client):
            live = p.Live(pl_protocol.Asker(sleep=lambda s: None))
            live.ask(protocol.messages_for(case(), impasse=True))
        (req,) = client.peticiones
        self.assertEqual(req["extra_body"]["provider"], plan.PROVIDER)
        self.assertEqual(req["extra_body"]["reasoning"], {"effort": "high"})
        self.assertEqual((req["temperature"], req["max_tokens"]), (0, 16000))
        self.assertEqual(req["response_format"], {"type": "json_object"})
        self.assertTrue(req["messages"][1]["content"].startswith(protocol.NOTICE_BASE))


# ---------------------------------------------------------------------------
# 9. The statistics, and Stage C's terms
# ---------------------------------------------------------------------------

def drafts(*rows) -> list[dict]:
    """Drafts built by hand: (cause, governing, class, verdict)."""
    return [{"idx": i, "cause": c, "governing": g, "group": references.group_of(g),
             "class": k, "verdict": v} for i, (c, g, k, v) in enumerate(rows)]


I, C, E = plan.IMPASSE, plan.CONFLICT, plan.ERROR


class TestTheStatistics(unittest.TestCase):

    def setUp(self):
        self.ds = drafts((I, "H16", "whole", e.BORN), (I, "H29", "other", e.BORN),
                         (I, "H08", "whole", e.UNPLACED), (I, "H16", "wrong_queue", e.BORN),
                         (I, "H28", "no_rule", e.REJECTED), (C, "H16", "whole", e.BORN),
                         (E, "H01", "cut_by_one", e.BORN), (I, "H03", "whole", e.REJECTED))

    def test_other_queues_and_no_rule_are_left_out_above_and_below(self):
        imp = references.at(self.ds, I)
        self.assertEqual(references.counted(imp), [3, 4])
        self.assertEqual(references.share(references.counted(imp)), F(3, 4))
        self.assertIsNone(references.share([0, 0]))

    def test_by_cause_and_by_group(self):
        self.assertEqual(references.by_cause(self.ds),
                         {I: [3, 4], C: [1, 1], E: [0, 1]})
        self.assertEqual(references.by_group(self.ds),
                         {"none": [0, 0], "few": [2, 2], "many": [1, 2]})

    def test_the_defaults_read_the_impasses_alone(self):
        self.assertEqual(references.at_the_defaults(self.ds), [1, 2])
        self.assertEqual(references.defaults_met(self.ds),
                         {"H08": 1, "H27": 0, "H28": 1, "H29": 1})

    def test_born_w_reads_the_whole_drafts_at_impasses(self):
        self.assertEqual(references.born_of(self.ds),
                         {"whole": 3, "born": 1, "unplaced": 1, "refused": 1})
        self.assertEqual(references.born_w(self.ds), F(1, 3))
        self.assertIsNone(references.born_w(drafts((I, "H16", "other", e.BORN))))

    def test_impasses_count_the_records_causes(self):
        rec = {"escalations": [{"kind": I}, {"kind": E}, {"kind": I}, {"kind": C}]}
        self.assertEqual(references.impasses(rec), 2)


def runs_of(**arms) -> dict[str, list[dict]]:
    """Runs built by hand: (space, whole_I, impasses, born_W, whole_D counts)."""
    out = {a: [] for a in plan.ARMS}
    for a, rows in arms.items():
        out[a] = [{"space": s, "whole_I": w, "impasses": n, "born_W": b,
                   "whole_D_counts": dcounts, "rep": k}
                  for k, (s, w, n, b, dcounts) in enumerate(rows, start=1)]
    return out


class TestStageC(unittest.TestCase):

    def test_the_lines_are_exact_on_every_side(self):
        tiny = F(1, 10 ** 9)
        self.assertTrue(score.holds("IM-a", F(1, 5)))
        self.assertFalse(score.holds("IM-a", F(1, 5) - tiny))
        self.assertFalse(score.holds("IM-b", F(1, 3)))       # strictly below
        self.assertTrue(score.holds("IM-b", F(1, 3) - tiny))
        self.assertTrue(score.holds("IM-c", F(1, 100)))
        self.assertFalse(score.holds("IM-c", F(1, 100) - tiny))
        self.assertTrue(score.holds("IM-d", F(1, 40)))
        self.assertFalse(score.holds("IM-d", F(1, 40) + tiny))
        self.assertTrue(score.holds("IM-e", F(3, 4)))
        self.assertFalse(score.holds("IM-e", F(3, 4) + tiny))
        self.assertTrue(score.holds("IM-f", F(3, 4)))
        self.assertFalse(score.holds("IM-f", F(3, 4) - tiny))

    def test_medians_ratios_and_thin(self):
        runs = runs_of(v1c=[("9/10", "1/3", 30, "4/5", [0, 7]),
                            ("19/20", "2/5", 36, "1", [1, 6]),
                            ("23/25", "3/10", 28, "7/10", [0, 5])],
                       v1n=[("47/50", "3/4", 16, "4/5", [1, 6]),
                            ("93/100", "7/10", 20, "3/4", [2, 7]),
                            ("49/50", "1/2", 22, "9/10", [3, 5])])
        a = score.row("IM-a", runs)            # 7/10 - 1/3
        self.assertEqual((a["verdict"], F(a["value"]["fraction"])),
                         (score.HOLDS, F(7, 10) - F(1, 3)))
        self.assertTrue(a["thin"])             # v1n's 1/2 in its median's place reads 1/6
        c = score.row("IM-c", runs)            # 47/50 - 23/25
        self.assertEqual(F(c["value"]["fraction"]), F(47, 50) - F(23, 25))
        self.assertEqual(c["verdict"], score.HOLDS)
        self.assertTrue(c["thin"])             # v1c's 19/20 in its median's place
        d = score.row("IM-d", runs)
        self.assertEqual(F(d["value"]["fraction"]), F(23, 25) - F(47, 50))
        self.assertEqual(d["verdict"], score.HOLDS)
        e_ = score.row("IM-e", runs)           # 20/30
        self.assertEqual((e_["verdict"], F(e_["value"]["fraction"])), (score.HOLDS, F(2, 3)))
        self.assertFalse(e_["thin"])
        f = score.row("IM-f", runs)
        self.assertEqual((f["verdict"], F(f["value"]["fraction"])), (score.HOLDS, F(4, 5)))
        self.assertFalse(f["thin"])            # v1n's 3/4 in its median's place still holds
        b = score.row("IM-b", runs)            # 6/18
        self.assertEqual(b["pooled"], [6, 18])
        self.assertEqual((b["verdict"], F(b["value"]["fraction"])), (score.REFUTED, F(1, 3)))
        self.assertTrue(b["thin"])             # without run 3, 3/13 holds

    def test_im_f_is_thin_only_where_a_run_crosses_the_line(self):
        runs = runs_of(v1n=[("1", "1", 10, "4/5", [0, 5]), ("1", "1", 10, "9/10", [0, 5]),
                            ("1", "1", 10, "1", [0, 5])])
        f = score.row("IM-f", runs)
        self.assertEqual((f["verdict"], f["thin"]), (score.HOLDS, False))

    def test_every_reason_a_row_has_no_value(self):
        one = runs_of(v1c=[("1", "1/3", 30, "1", [0, 9])],
                      v1n=[("1", "1/2", 20, "1", [0, 9])] * 2)
        for rid in ("IM-a", "IM-c", "IM-d", "IM-e"):
            with self.subTest(rid):
                self.assertEqual(score.row(rid, one)["verdict"], score.NO_VALUE)
        zero = runs_of(v1c=[("1", "1/3", 0, "1", [0, 9])] * 3,
                       v1n=[("1", "1/2", 20, "1", [0, 9])] * 3)
        self.assertEqual(score.row("IM-e", zero)["verdict"], score.NO_VALUE)
        none = runs_of(v1c=[("1", "1/3", 30, "1", [0, 9])] * 3,
                       v1n=[("1", None, 20, None, [0, 1]), ("1", None, 20, None, [0, 1]),
                            ("1", "1/2", 20, "1", [0, 2])])
        for rid in ("IM-a", "IM-f"):
            with self.subTest(rid):
                got = score.row(rid, none)
                self.assertEqual(got["verdict"], score.NO_VALUE)
        b = score.row("IM-b", none)            # 4 drafts at the defaults, fewer than 5
        self.assertEqual((b["verdict"], b["pooled"]), (score.NO_VALUE, [0, 4]))
        two = runs_of(v1n=[("1", None, 20, None, [0, 5]), ("1", "1/2", 20, "1", [0, 5]),
                           ("1", "1/2", 20, "1/2", [0, 5])])
        got = score.row("IM-f", two)           # the two runs with a value, their mean
        self.assertEqual((got["verdict"], F(got["value"]["fraction"])),
                         (score.HOLDS, F(3, 4)))

    def test_the_rows_read_the_arms_section_0_says(self):
        self.assertEqual({rid: (arms, key) for rid, (arms, key, _) in score.ROWS.items()},
                         {"IM-a": (("v1c", "v1n"), "whole_I"),
                          "IM-c": (("v1c", "v1n"), "space"),
                          "IM-d": (("v1c", "v1n"), "space"),
                          "IM-e": (("v1c", "v1n"), "impasses"),
                          "IM-f": (("v1n",), "born_W")})
        self.assertEqual(score.POOLED, {"IM-b": ("v1n", "whole_D_counts")})
        self.assertEqual(score.ALL_ROWS, ("IM-a", "IM-b", "IM-c", "IM-d", "IM-e", "IM-f"))
        self.assertEqual(set(score.ALL_ROWS), set(plan.LINES))

    def test_a_row_of_no_value_reads_as_none_in_the_prose_test(self):
        """`PLAN_CAUSE.md`'s lesson: a scorer's word for no value must be one the
        prose test reads. A record built by hand with a row of no value."""
        rec = {"verdicts": {"IM-b": score.verdict("IM-b", None, False, "too few")}}
        self.assertEqual(rec["verdicts"]["IM-b"]["verdict"], "unadjudicable")
        self.assertEqual(prose.verdict(rec["verdicts"]["IM-b"]), prose.NONE)
        self.assertEqual(prose.verdict(score.verdict("IM-a", F(1, 2), False, None)),
                         prose.HOLDS)
        self.assertEqual(prose.verdict(score.verdict("IM-a", F(0), False, None)),
                         prose.REFUTED)


if __name__ == "__main__":
    unittest.main()
