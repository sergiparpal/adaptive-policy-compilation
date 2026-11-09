"""
`PLAN_WHOLE.md`'s instrument, `whole/`. **No figure of the plan**: no test runs the
loop over the corpus, and every ticket, run and record below is built by hand.
The figures §0 declares are recomputed by `WR-g2`, `WR-g3` and Stage A, never
here; what is pinned here is that `DECLARED` is the plan's text.

What is pinned:

  1. §11's constants, the seed and §0's lines with their sides, `DECLARED`
     against §0's text, the schedule, and the gate, which counts every
     signature line.
  2. v1d's paragraph: its digest, its first sentence, that it names no queue and
     no rule, and that the plan quotes it byte for byte.
  3. v1d's messages: v1c's with that one paragraph replaced, on both calls; v2b's
     text giving v1c's messages back; a first message that is not v1c's refused;
     the texts' digests and fingerprints of both arms.
  4. v1d's proposer: each arm's class sends its own messages through the
     resumable proposer, and a loop on a corpus built by hand gives the same
     record under both, every call one paragraph apart.
  5. The resume, and that a run cannot resume under the other arm or other draws.
  6. Nothing is built, asked or written while the plan is unsigned; the dry runs
     build no client; a run refuses before the key without what must come
     before it; the turn.
  7. The smoke check, with v1d's paragraph.
  8. The request is `PLAN_PLACEMENT.md`'s for both arms.
  9. `whole(r)` on drafts built by hand, by breadth, and Stage C's terms: exact
     lines on every side, medians, the pairs by repetition, thin labels and every
     reason a row has no value.
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
from manual import instrument as MI
from placement import loop as pl_loop
from placement import plan as pl_plan
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import user_msg

from whole import gates, plan, protocol, references, run, sample, score

from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
F = Fraction
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
PLAN_TEXT = (REPO / "PLAN_WHOLE.md").read_text()
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
                  "PROVIDER_NAME", "LEVEL", "SYSTEM_PROMPT_SHA16", "COVERAGE", "N", "SEED"):
            with self.subTest(k):
                self.assertEqual(getattr(plan, k), getattr(pl_plan, k))
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, "DeepInfra")
        self.assertEqual(plan.settings(), pl_plan.settings())

    def test_the_arms_and_the_runs(self):
        self.assertEqual(plan.PROTOCOLS, ("v1c", "v1d"))
        self.assertEqual(plan.ARMS, ("v1c", "v1d"))
        self.assertEqual(plan.COVERAGE, F(1, 2))
        self.assertEqual((plan.REPS, plan.N, plan.SEED), (3, 2000, 17))
        self.assertEqual((plan.SMOKE_N, plan.SMOKE_ARM), (30, "v1d"))
        self.assertEqual((plan.MAX_ESCALATIONS, plan.MAX_CONSECUTIVE_FAILURES), (400, 5))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_seed_is_the_next_prime_after_103_and_no_closed_threads(self):
        def prime(n):
            return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))
        self.assertEqual(plan.ORDER_SEED, next(n for n in range(104, 200) if prime(n)))
        taken = set()
        for path in REPO.glob("*/plan.py"):
            if path.parent.name == "whole":
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, int)
                        and any(isinstance(t, ast.Name) and t.id.endswith("SEED")
                                for t in node.targets)):
                    taken.add(node.value.value)
        self.assertNotIn(plan.ORDER_SEED, taken)

    def test_the_lines_are_section_0s_as_fractions_on_their_sides(self):
        self.assertEqual(plan.LINES, {"WR-a": F(3, 4), "WR-b": F(9, 10), "WR-c": F(3, 2),
                                      "WR-d": F(1, 40), "WR-e": F(9, 10), "WR-f": F(1, 4)})
        self.assertEqual(plan.SIDES, {"WR-a": ">=", "WR-b": ">=", "WR-c": "<=",
                                      "WR-d": "<=", "WR-e": "<", "WR-f": ">="})
        for v in plan.LINES.values():
            self.assertIsInstance(v, Fraction)

    def test_the_plan_states_them(self):
        for text in ("`ORDER_SEED = 107`", "`WR_A_LINE = Fraction(3, 4)`",
                     "`WR_B_LINE = Fraction(9, 10)`", "`WR_C_LINE = Fraction(3, 2)`",
                     "`WR_D_LINE = Fraction(1, 40)`", "`WR_E_LINE = Fraction(9, 10)`",
                     "`WR_F_LINE = Fraction(1, 4)`",
                     "`SMOKE_N = 30`", '`SMOKE_ARM = "v1d"`', "`MAX_ESCALATIONS = 400`",
                     "`MIN_SIGNATURES = 1`", '"deepinfra/fp8"',
                     f"`WHOLE_BASE_SHA16 = \"{plan.WHOLE_BASE_SHA16}\"`"):
            with self.subTest(text):
                self.assertIn(text, PLAN_TEXT)

    def test_declared_transcribes_section_0(self):
        d = plan.DECLARED
        v1c = [d["whole"][f"v1c_r{r}"] for r in (1, 2, 3)]
        v1b = [d["whole"][f"v1b_r{r}"] for r in (1, 2, 3)]
        for runs in (v1c, v1b):
            listed = f"{runs[0][0]} of {runs[0][1]}, {runs[1][0]} of {runs[1][1]} and " \
                     f"{runs[2][0]} of {runs[2][1]}"
            self.assertIn(listed, FLAT)
        self.assertEqual(F(d["whole_median_v1c"]), sorted(F(*x) for x in v1c)[1])
        lists = [d["lists"][f"v1c_r{r}"] for r in (1, 2, 3)]

        def said(key):
            xs = [str(float(F(x["whole_median" if key == "w" else "sent_median"])))
                  .removesuffix(".0") for x in lists]
            return f"{xs[0]}, {xs[1]} and {xs[2]}"
        self.assertIn(f"The median list is {said('w')} rules by run, against {said('s')}",
                      FLAT)
        self.assertIn(", ".join(str(x["whole_max"]) for x in lists[:2])
                      + f" and {lists[2]['whole_max']}", FLAT)
        rare = [row for k in sorted(d["lists_rare"]) for row in d["lists_rare"][k]]
        self.assertIn(f"{min(r[2] for r in rare)} to {max(r[2] for r in rare)} rules", FLAT)
        for k, rows in d["lists_rare"].items():
            for idx, gov, whole, sent in rows:
                with self.subTest(k=k, idx=idx):
                    self.assertRegex(PLAN_TEXT, rf"\| {k[:3]} {k[4:]} \| {idx} \| `{gov}` "
                                                rf"\| {whole} \| {sent} \|")
        t = d["transcriber_oncall"]
        self.assertIn(f"recalls {t['r1']}, {t['r2']} and {t['r3']} of `ONCALL_ESCALATION`",
                      FLAT)
        order = ", ".join(f"{a} r{r}" for a, r in d["schedule"][:-1]) \
            + f" and {d['schedule'][-1][0]} r{d['schedule'][-1][1]}"
        self.assertIn(order, FLAT)
        tr = d["text_relations"]
        self.assertIn(f"{tr['rules_inside_a_lower_rule']} of the 29 rules lie strictly inside "
                      f"a lower rule", FLAT)
        self.assertIn(f"{tr['lower_containing_pairs']} pairs in all", FLAT)
        self.assertIn(f"{tr['lower_crossing_pairs']} crossing pairs", FLAT)
        self.assertIn(f"{tr['rules_crossing_another_queue']} of the 29 cross a lower rule of "
                      f"another queue", FLAT)
        self.assertIn(f"none holds a lower rule inside it", FLAT)
        self.assertEqual(tr["rules_holding_a_lower_rule"], 0)
        for g, (inside, crosses, other) in tr["rare"].items():
            self.assertIn(f"`{g}` lies inside {inside} lower rules and crosses {crosses}, "
                          f"{other} of them of another queue", FLAT)

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        first = random.Random("PLAN_WHOLE/order/107").choice(plan.ARMS)
        self.assertEqual(order[0], (first, 1))
        self.assertEqual([list(x) for x in order], plan.DECLARED["schedule"])
        arms = [a for a, _ in order]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))

    def test_the_schedule_is_the_same_under_any_hash_seed(self):
        code = "import json; from whole import plan; print(json.dumps(plan.schedule()))"
        outs = set()
        for seed in ("0", "1", "4242"):
            env = {**os.environ, "PYTHONHASHSEED": seed}
            outs.add(subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                                    capture_output=True, text=True, check=True).stdout)
        self.assertEqual(len(outs), 1)

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            for path in (plan.sample_path(), plan.score_path(), plan.smoke_path(),
                         plan.run_path("v1d", 1), plan.partial_path("v1c_r2")):
                self.assertEqual(path.parent, d)
        with self.assertRaises(ValueError):
            plan.run_path("v1b", 1)
        with self.assertRaises(ValueError):
            plan.run_path("v1d", 4)

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
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-09)**\n"
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
        self.assertEqual(plan.gate_signature(REPO / "PLAN_WHOLE.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_WHOLE.md"))
        self.assertEqual(plan.gate_signature()["source"], "PLAN_WHOLE.md")


# ---------------------------------------------------------------------------
# 2. The paragraph
# ---------------------------------------------------------------------------

class TestTheParagraph(unittest.TestCase):

    def test_its_digest_and_its_first_sentence(self):
        self.assertEqual(sha16(protocol.WHOLE_BASE), plan.WHOLE_BASE_SHA16)
        self.assertEqual(sha16(p.BLIND_BASE), plan.BLIND_BASE_SHA16)
        for text in (protocol.WHOLE_BASE, p.BLIND_BASE):
            self.assertTrue(text.startswith(protocol.FIRST_SENTENCE))
            self.assertTrue(text.endswith("\n") and text.isascii())
        self.assertEqual(protocol.BASES, {"v1c": p.BLIND_BASE, "v1d": protocol.WHOLE_BASE})

    def test_it_names_no_queue_and_no_rule(self):
        self.assertTrue(protocol.names_nothing(protocol.WHOLE_BASE))
        self.assertTrue(protocol.names_nothing(p.BLIND_BASE))
        for bad in ("gana a H04", "manda a ONCALL_ESCALATION", "cita R0001"):
            with self.subTest(bad):
                self.assertFalse(protocol.names_nothing(protocol.WHOLE_BASE + bad))

    def test_the_plan_quotes_it_byte_for_byte(self):
        path = REPO / "PLAN_WHOLE.md"
        self.assertTrue(gates.quoted_in_the_plan(protocol.WHOLE_BASE, path))
        self.assertFalse(gates.quoted_in_the_plan(protocol.WHOLE_BASE.replace("entera", "toda"),
                                                  path))
        self.assertFalse(gates.quoted_in_the_plan(protocol.WHOLE_BASE.rstrip("\n"), path))


# ---------------------------------------------------------------------------
# 3. The messages
# ---------------------------------------------------------------------------

class TestTheMessages(unittest.TestCase):

    def setUp(self):
        self.case = case(product="api")
        self.draft = answer(payload(*API))

    def test_v2bs_text_gives_v1cs_messages_back(self):
        self.assertEqual(protocol.messages_for(self.case, base=p.BLIND_BASE),
                         p.messages_for(self.case))
        self.assertEqual(protocol.messages_for(self.case, self.draft, "lista", base=p.BLIND_BASE),
                         p.messages_for(self.case, self.draft, "lista"))

    def test_v1d_is_v1c_one_paragraph_apart_on_both_calls(self):
        for prev, msg in ((None, ""), (self.draft, "lista")):
            with self.subTest(placement=prev is not None):
                ours = protocol.messages_for(self.case, prev, msg)
                theirs = p.messages_for(self.case, prev, msg)
                self.assertTrue(protocol.one_paragraph_apart(theirs, ours))
                self.assertEqual(ours[1], {"role": "user",
                                           "content": user_msg(self.case, protocol.WHOLE_BASE)})
                self.assertEqual([m for k, m in enumerate(ours) if k != 1],
                                 [m for k, m in enumerate(theirs) if k != 1])
                self.assertEqual(len(ours), 2 if prev is None else 4)

    def test_one_paragraph_apart_has_teeth(self):
        theirs = p.messages_for(self.case, self.draft, "lista")
        ours = protocol.messages_for(self.case, self.draft, "lista")
        self.assertTrue(protocol.one_paragraph_apart(theirs, ours))
        system = [dict(ours[0], content="otro"), *ours[1:]]
        other_ticket = protocol.messages_for(case(product="billing"), self.draft, "lista")
        other_list = protocol.messages_for(self.case, self.draft, "otra lista")
        not_at_start = [ours[0], {"role": "user", "content": "x" + ours[1]["content"]}, *ours[2:]]
        for name, bad in (("system", system), ("ticket", other_ticket), ("list", other_list),
                          ("start", not_at_start), ("short", ours[:3])):
            with self.subTest(name):
                self.assertFalse(protocol.one_paragraph_apart(theirs, bad))

    def test_a_first_message_that_is_not_v1cs_is_refused(self):
        odd = [{"role": "system", "content": "s"}, {"role": "user", "content": "otra cosa"}]
        with mock.patch.object(p, "messages_for", return_value=odd):
            with self.assertRaises(protocol.NotV1c):
                protocol.messages_for(self.case)

    def test_the_texts_digests_and_fingerprints(self):
        self.assertEqual(protocol.texts("v1c"), p.texts())
        self.assertEqual(protocol.digests("v1c"), p.digests())
        self.assertEqual(protocol.fingerprint("v1c"), p.fingerprint())
        c, d = protocol.digests("v1c"), protocol.digests("v1d")
        self.assertEqual(sorted(d), ["placement_template", "retry_message", "system_prompt",
                                     "whole_base"])
        for k in ("system_prompt", "placement_template", "retry_message"):
            self.assertEqual(d[k], c[k])
        self.assertEqual(d["whole_base"], plan.WHOLE_BASE_SHA16)
        self.assertNotEqual(protocol.fingerprint("v1d"), protocol.fingerprint("v1c"))
        with mock.patch.dict(protocol.BASES, {"v1d": p.BLIND_BASE}):
            self.assertEqual(protocol.fingerprint("v1d"), p.fingerprint())
        with self.assertRaises(ValueError):
            protocol.texts("v1b")


# ---------------------------------------------------------------------------
# 4. The proposer, and a loop on a corpus built by hand
# ---------------------------------------------------------------------------

def corpus() -> list[Case]:
    """Case 0 is an impasse on the empty base, which writes the API rule; case 1
    an impasse no rule matches, whose draft crosses the API rule, so v1c's list
    holds it and a placement round is sent."""
    return [case(product="api"), case(product="dashboard", severity=1)]


LABELS = [(T2, "H16"), (T3, "H06")]
DRAWS = [0.9, 0.9]


def answers() -> list[p.Answer]:
    return [answer(payload(*API)), answer(payload(*SEVERE)),
            answer(payload(*SEVERE, beats=["R0001"]))]


def looped(arm: str, d: Path, base: str | None = None):
    """The loop under v1c's escalation with `arm`'s proposer class over a live
    double serving `answers()` in order."""
    live = LiveScript(*answers())
    path = d / f"{arm}_{base is not None}.partial.jsonl"
    rows, _ = erun.open_partial(path, {"plan": "test", "arm": arm})
    prop = protocol.PROPOSERS[arm](live, path, rows)
    if base is not None:
        prop.base = base
    eng = PriorityEngine(space=MI.space())
    res = pl_loop.run_loop(corpus(), LABELS, eng, prop, F(1, 2), DRAWS,
                           propose=pl_loop.ESCALATIONS["v1c"], clock=lambda: 0.0)
    prop.flush()
    return gates.as_json(pl_loop.record_of(res, eng)), live.sent


class TestTheProposer(unittest.TestCase):

    def test_the_classes(self):
        self.assertIs(protocol.PROPOSERS["v1c"], pl_run.Stamped)
        self.assertTrue(issubclass(protocol.PROPOSERS["v1d"], pl_run.Stamped))
        self.assertEqual(protocol.Stamped.base, protocol.WHOLE_BASE)

    def test_each_arm_sends_its_own_messages(self):
        c, draft = case(product="api"), answer(payload(*API))
        with tempfile.TemporaryDirectory() as d:
            for arm in plan.ARMS:
                with self.subTest(arm):
                    live = LiveScript(answer(payload(*API)), answer(payload(*API)))
                    path = Path(d) / f"{arm}.partial.jsonl"
                    rows, _ = erun.open_partial(path, {"plan": "test"})
                    prop = protocol.PROPOSERS[arm](live, path, rows)
                    prop.first(c, 0)
                    prop.placement(c, draft, "lista", 0)
                    base = protocol.BASES[arm]
                    self.assertEqual(live.sent, [
                        protocol.messages_for(c, base=base),
                        protocol.messages_for(c, draft, "lista", base=base)])

    def test_a_loop_gives_the_same_record_under_both_one_paragraph_apart(self):
        with tempfile.TemporaryDirectory() as d:
            rec_c, sent_c = looped("v1c", Path(d))
            rec_d, sent_d = looped("v1d", Path(d))
            rec_0, sent_0 = looped("v1d", Path(d), base=p.BLIND_BASE)
        self.assertEqual(rec_c, rec_d)
        self.assertEqual(rec_c, rec_0)
        self.assertEqual(sent_0, sent_c)
        self.assertEqual([len(m) for m in sent_c], [2, 2, 4])     # a placement round was sent
        self.assertEqual(len(sent_d), len(sent_c))
        for theirs, ours in zip(sent_c, sent_d):
            self.assertTrue(protocol.one_paragraph_apart(theirs, ours))
        self.assertEqual([r["action"] for r in rec_c["rules"]], [T2, T3])
        self.assertEqual(rec_c["escalations"][1]["listed"], ["R0001"])

    def test_the_proposers_path_names_no_policy(self):
        for rel in ("whole/protocol.py", "whole/run.py"):
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
        for rel in ("whole/run.py", "whole/protocol.py", "whole/plan.py"):
            tree = ast.parse((REPO / rel).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare) and any(
                        isinstance(n, ast.Name) and n.id in ("truth", "trule", "labels")
                        for x in (node.left, *node.comparators) for n in ast.walk(x)):
                    found.append((rel, ast.unparse(node)))
        self.assertEqual(found, [])


# ---------------------------------------------------------------------------
# 5. The resume
# ---------------------------------------------------------------------------

class TestTheResume(unittest.TestCase):

    def test_a_resumed_v1d_record_keeps_each_calls_own_seconds_and_hour(self):
        header = {"plan": "test"}
        corp, labels = [case(product="api"), case()], [(T2, "H01"), (T1, "H29")]
        catch_all = payload(T1, ("severity", "gte", 1))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, header)
            live = protocol.Stamped(LiveScript(e.ProposalFailed("no parse", "stop", 3, []),
                                               answer(catch_all)),
                                    path, rows, clock=iter([0.0, 7.5, 10.0, 52.0]).__next__)
            asked = pl_loop.run_loop(corp, labels, PriorityEngine(space=MI.space()), live,
                                     F(1, 2), [0.1, 0.9], propose=pl_loop.ESCALATIONS["v1c"],
                                     clock=itertools.count(0.0, 5.0).__next__)
            live.flush()
            kept = [json.loads(x) for x in path.read_text().splitlines()[1:]]
            self.assertTrue(all(r.get("kept_at") for r in kept))
            rows, resumed = erun.open_partial(path, header)
            self.assertTrue(resumed)
            served = pl_loop.run_loop(corp, labels, PriorityEngine(space=MI.space()),
                                      protocol.Stamped(LiveScript(), path, rows), F(1, 2),
                                      [0.1, 0.9], propose=pl_loop.ESCALATIONS["v1c"],
                                      clock=itertools.count(0.0, 0.01).__next__)
        for res, seconds in ((asked, [5.0, 5.0]), (served, [7.5, 42.0])):
            with self.subTest(seconds=seconds):
                calls = [esc.calls[0] for esc in res.loop.escalations]
                self.assertEqual([c["seconds"] for c in calls], seconds)

    def test_a_stored_answer_paid_for_under_the_other_arms_request_is_refused(self):
        """A partial file's rows carry their request's digest: v1d cannot be
        served an answer v1c's request paid for."""
        c = case(product="api")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, {"plan": "test"})
            first = pl_run.Stamped(LiveScript(answer(payload(*API))), path, rows)
            first.first(c, 0)
            rows, _ = erun.open_partial(path, {"plan": "test"})
            with self.assertRaises(erun.Desync):
                protocol.Stamped(LiveScript(), path, rows).first(c, 0)

    def test_a_partial_under_the_other_arm_or_other_draws_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            mine = run.protocol_header("v1d", plan.N, "v1d_r1", 1)
            erun.open_partial(path, mine)
            for other in (run.protocol_header("v1c", plan.N, "v1d_r1", 1),
                          run.protocol_header("v1d", plan.N, "v1d_r1", 2)):
                self.assertNotEqual(other, mine)
                with self.assertRaises(SystemExit):
                    erun.open_partial(path, other)

    def test_the_header_names_the_plan_the_pin_the_protocol_and_the_texts(self):
        h = run.protocol_header("v1d", plan.N, "v1d_r2", 2)
        self.assertEqual((h["plan"], h["protocol"], h["provider"]),
                         ("PLAN_WHOLE.md", "v1d", plan.PROVIDER))
        self.assertEqual(h["texts_sha16"], protocol.digests("v1d"))
        self.assertEqual(h["fingerprint"], protocol.fingerprint("v1d"))
        self.assertEqual(h["draws_seed"], "PLAN_CHANNEL/channel/97/r2")
        c = run.protocol_header("v1c", plan.N, "v1c_r2", 2)
        self.assertEqual((c["fingerprint"], c["texts_sha16"]), (p.fingerprint(), p.digests()))
        placement_header = pl_run.protocol_header("v1c", plan.N, "v1c_r2", 2)
        self.assertEqual({k: v for k, v in c.items() if k != "plan"},
                         {k: v for k, v in placement_header.items() if k != "plan"})

    def test_the_loop_does_not_swallow_an_outage(self):
        class Refused:
            name = "refused"

            def first(self, case, idx):
                raise p.RateLimited("refused")

        with self.assertRaises(p.RateLimited):
            pl_loop.run_loop([case()], [(T1, "H29")], PriorityEngine(space=MI.space()),
                             Refused(), F(1, 2), [0.3], propose=pl_loop.ESCALATIONS["v1c"])


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
            for over in ({"schedule": [["v1d", 1]]},
                         {"streams": {"r1": {"seed": "x", "sha16": "y"}}},
                         {"fingerprints": {"v1c": p.fingerprint(), "v1d": "0" * 16}}):
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
           "base_text": protocol.WHOLE_BASE,
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

    def test_a_clean_smoke_run_passes(self):
        ok, why = self.check(smoke_record())
        self.assertTrue(ok, why)
        self.assertIn("1 placements answered", why)

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
        blind = smoke_record(base_text=p.BLIND_BASE)
        unborn = smoke_record(metrics={"n_rules": 0})
        for name, rec in (("elsewhere", bad), ("did not reason", quiet), ("cut", cut),
                          ("no placement", unplaced), ("rows", lost), ("protocol", other),
                          ("v1c's paragraph", blind), ("no rule", unborn)):
            with self.subTest(name):
                self.assertFalse(self.check(rec)[0])


# ---------------------------------------------------------------------------
# 8. The request
# ---------------------------------------------------------------------------

class DeepInfraReasons(OpenRouterShapedClient):
    PROVIDER = "DeepInfra"


class TestTheRequest(unittest.TestCase):

    def test_both_arms_send_plan_placements_request(self):
        msgs = protocol.messages_for(case())
        holder = SimpleNamespace(model=plan.MODEL)
        for attempt in (0, 1):
            got = [pl_protocol.request_with(plan.PROVIDER, plan.MODEL, arm, msgs, attempt)
                   for arm in plan.ARMS]
            self.assertEqual(got[0], got[1])
            theirs = p.Asker.request(holder, "v1b", msgs, attempt)
            self.assertEqual(got[0]["extra_body"]["provider"], plan.PROVIDER)
            got[0]["extra_body"]["provider"] = theirs["extra_body"]["provider"]
            self.assertEqual(got[0], theirs)

    def test_the_asker_sends_v1ds_paragraph_and_the_pin_through_the_sdk(self):
        client = DeepInfraReasons(FixedResponses(json.dumps(payload(*API))))
        with fake_sdk(openai=client):
            live = p.Live(pl_protocol.Asker(sleep=lambda s: None))
            live.ask(protocol.messages_for(case()))
        (req,) = client.peticiones
        self.assertEqual(req["extra_body"]["provider"], plan.PROVIDER)
        self.assertEqual(req["extra_body"]["reasoning"], {"effort": "high"})
        self.assertEqual((req["temperature"], req["max_tokens"]), (0, 16000))
        self.assertEqual(req["response_format"], {"type": "json_object"})
        self.assertTrue(req["messages"][1]["content"].startswith(protocol.WHOLE_BASE))


# ---------------------------------------------------------------------------
# 9. whole(r) and Stage C's terms
# ---------------------------------------------------------------------------

def drafts(*classes) -> list[dict]:
    return [{"class": c, "governing": "H16"} for c in classes]


class TestWhole(unittest.TestCase):

    def test_other_queues_and_no_rule_are_left_out_above_and_below(self):
        got = references.whole_of(drafts("whole", "cut_by_one", "wrong_queue", "no_rule",
                                         "whole", "other"))
        self.assertEqual((got["held"], got["right_queue"], got["drafts"]), (2, 4, 6))
        self.assertEqual((got["wrong_queue"], got["no_rule"]), (1, 1))
        self.assertEqual(got["share"], F(1, 2))

    def test_a_held_part_is_counted_by_the_drafts_breadth(self):
        rows = [{"class": "whole", "governing": "H16", "breadth": b}
                for b in (references.THE_REGION, references.WIDER, references.WIDER,
                          references.WITHIN_OR_ACROSS)]
        got = references.whole_of(rows + drafts("cut_by_one"))
        self.assertEqual(got["held_by_breadth"], {"the_region": 1, "wider": 2,
                                                  "within_or_across": 1})
        self.assertEqual(got["share"], F(4, 5))

    def test_a_run_with_no_right_queue_draft_has_no_share(self):
        self.assertIsNone(references.whole_of(drafts("wrong_queue", "no_rule"))["share"])
        self.assertIsNone(references.whole_of([])["share"])


def runs_of(**arms) -> dict[str, list[dict]]:
    out = {a: [] for a in plan.ARMS}
    for a, rows in arms.items():
        out[a] = [{"space": s, "refused": r, "oncall": o, "whole": w, "rep": k}
                  for k, (s, r, o, w) in enumerate(rows, start=1)]
    return out


class TestStageC(unittest.TestCase):

    def test_the_lines_are_exact_on_every_side(self):
        tiny = F(1, 10 ** 9)
        self.assertTrue(score.holds("WR-a", F(3, 4)))
        self.assertFalse(score.holds("WR-a", F(3, 4) - tiny))
        self.assertTrue(score.holds("WR-b", F(9, 10)))
        self.assertFalse(score.holds("WR-b", F(9, 10) - tiny))
        self.assertTrue(score.holds("WR-c", F(3, 2)))
        self.assertFalse(score.holds("WR-c", F(3, 2) + tiny))
        self.assertTrue(score.holds("WR-d", F(1, 40)))
        self.assertFalse(score.holds("WR-d", F(1, 40) + tiny))
        self.assertFalse(score.holds("WR-e", F(9, 10)))      # strictly below
        self.assertTrue(score.holds("WR-e", F(9, 10) - tiny))
        self.assertTrue(score.holds("WR-f", F(1, 4)))
        self.assertFalse(score.holds("WR-f", F(1, 4) - tiny))

    def test_medians_ratios_and_thin(self):
        runs = runs_of(v1c=[("19/20", "1/10", "2/3", "2/5"), ("1", "1/20", "1/2", "1/3"),
                            ("9/10", "1/5", "1", "1/2")],
                       v1d=[("19/20", "1/10", "1", "4/5"), ("39/40", "1/5", "1", "1"),
                            ("1/2", "3/20", "8/15", "1/2")])
        a = score.row("WR-a", runs)
        self.assertEqual((a["verdict"], F(a["value"]["fraction"])), (score.HOLDS, F(4, 5)))
        self.assertTrue(a["thin"])          # v1d's 1/2 in its median's place
        b = score.row("WR-b", runs)
        self.assertEqual((b["verdict"], b["thin"]), (score.HOLDS, True))
        c = score.row("WR-c", runs)
        self.assertEqual((c["verdict"], F(c["value"]["fraction"])), (score.HOLDS, F(3, 2)))
        self.assertTrue(c["thin"])          # v1d's 1/5 in its median's place reads 2
        d = score.row("WR-d", runs)
        self.assertEqual(F(d["value"]["fraction"]), F(19, 20) - F(19, 20))
        self.assertEqual(d["verdict"], score.HOLDS)
        self.assertTrue(d["thin"])          # v1d's 1/2 in its median's place
        e_ = score.row("WR-e", runs)
        self.assertEqual((e_["verdict"], F(e_["value"]["fraction"])), (score.HOLDS, F(2, 3)))
        self.assertTrue(e_["thin"])         # v1c's 1 in its median's place
        f = score.row("WR-f", runs)         # pairs: 1 - 2/3, 1 - 1/2, 8/15 - 1
        self.assertEqual(f["per_run"]["pairs"], [[1, "1/3"], [2, "1/2"], [3, "-7/15"]])
        self.assertEqual((f["verdict"], F(f["value"]["fraction"])), (score.HOLDS, F(1, 3)))
        self.assertTrue(f["thin"])          # the third pair's -7/15 in the median's place

    def test_the_pairs_are_by_repetition_not_by_position(self):
        runs = runs_of(v1c=[("1", "1/5", "1/2", "1"), ("1", "1/5", "0", "1")],
                       v1d=[("1", "1/5", "1", "1"), ("1", "1/5", "1", "1")])
        runs["v1c"].reverse()               # read out of order: the reps still pair them
        f = score.row("WR-f", runs)
        self.assertEqual(f["per_run"]["pairs"], [[1, "1/2"], [2, "1"]])
        self.assertEqual(F(f["value"]["fraction"]), F(3, 4))
        self.assertFalse(f["thin"])

    def test_every_reason_a_row_has_no_value(self):
        one = runs_of(v1c=[("1", "1/5", "1", "1")], v1d=[("1", "1/5", "1", "1")] * 2)
        for rid in ("WR-c", "WR-d", "WR-e", "WR-f"):
            with self.subTest(rid):
                self.assertEqual(score.row(rid, one)["verdict"], score.NO_VALUE)
        zero = runs_of(v1c=[("1", "0", "1", "1")] * 3, v1d=[("1", "1/5", "1", "1")] * 3)
        self.assertEqual(score.row("WR-c", zero)["verdict"], score.NO_VALUE)
        none = runs_of(v1c=[("1", "1/5", "1", "1")] * 3,
                       v1d=[("1", "1/5", "1", None), ("1", "1/5", "1", None),
                            ("1", "1/5", "1", "1")])
        got = score.row("WR-a", none)
        self.assertEqual(got["verdict"], score.NO_VALUE)
        self.assertEqual(got["per_run"]["v1d"], [None, None, "1"])
        two = runs_of(v1d=[("1", "1/5", "1", None), ("1", "1/5", "1", "1"),
                           ("1", "1/5", "1", "1/2")])
        got = score.row("WR-a", two)            # the two runs with a value, their mean
        self.assertEqual((got["verdict"], F(got["value"]["fraction"])),
                         (score.HOLDS, F(3, 4)))

    def test_the_rows_read_the_arms_section_0_says(self):
        self.assertEqual({rid: (arms, key) for rid, (arms, key, _) in score.ROWS.items()},
                         {"WR-a": (("v1d",), "whole"), "WR-b": (("v1d",), "oncall"),
                          "WR-c": (("v1c", "v1d"), "refused"),
                          "WR-d": (("v1c", "v1d"), "space"), "WR-e": (("v1c",), "oncall")})
        self.assertEqual(score.PAIRED, {"WR-f": "oncall"})
        self.assertEqual(score.ALL_ROWS, ("WR-a", "WR-b", "WR-c", "WR-d", "WR-e", "WR-f"))
        self.assertEqual(set(score.ALL_ROWS), set(plan.LINES))


if __name__ == "__main__":
    unittest.main()
