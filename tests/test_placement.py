"""
`PLAN_PLACEMENT.md`'s instrument, `placement/`. **No figure of the plan**: no test
runs the loop over the corpus, and every rule, ticket, engine, run and record
below is built by hand. The figures §0 declares are recomputed by `PL-g2`,
`PL-g3` and Stage A, never here; what is pinned here is that `DECLARED` is the
plan's text.

What is pinned:

  1. §11's constants, the seeds and §0's lines, `DECLARED` against §0's text, the
     schedule, and the gate, which counts every signature line.
  2. v1c's list on bases built by hand: a rule inside the draft and one
     containing it left out, an equal one kept, a wholly governed one left out, a
     partly governed one kept, and a list left empty sending no call.
  3. v1c with both exclusions off is v1b, and this plan's loop under v1b is
     `PLAN_CHANNEL.md`'s, record for record, on a corpus built by hand.
  4. The list reads no label: labels and draws that leave every cause unchanged
     leave every list, every call and the base unchanged; nothing the trigger
     reads is handed to the proposer; and every comparison with the label on the
     proposer's path is listed here.
  5. The resume, the hour each answer was kept, and that a run cannot resume under
     another protocol or other draws.
  6. Nothing is built, asked or written while the plan is unsigned; the dry runs
     build no client; a run refuses before the key without what must come before.
  7. The smoke check, with the trigger's record and a rule left out.
  8. The bridge's tickets and order, from their seed strings, under any hash seed.
  9. The request is `PLAN_REASONED_LOOP.md`'s but for the pin.
 10. Stage C's terms: exact lines on both sides, medians, thin on medians and on
     `PL-c`'s count, every reason a row has no value, and `refused(r)`.
 11. What decides nothing: an omitted edge, read against an engine built by hand.
"""

from __future__ import annotations

import ast
import functools
import inspect
import itertools
import json
import os
import random
import re
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
from channel import loop as ch_loop
from channel import plan as ch_plan
from manual import instrument as MI
from queue_alone import plan as qa_plan
from reasoned_loop import loop as rl_loop
from reasoned_loop import plan as rl_plan
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine, validate_conditions

from placement import gates, loop, plan, protocol, references, run, sample, score

from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk

REPO = Path(__file__).resolve().parent.parent
F = Fraction
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
T1, T2, T3, S = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"
PLAN_TEXT = (REPO / "PLAN_PLACEMENT.md").read_text()


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
        return answer(self.draft(case, idx))

    def placement(self, case, draft, message, idx, listed=None):
        self.asked.append(("placement", idx, case, list(listed or []), message))
        return answer(self.place(case, draft, listed, idx))


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
    rule is born. Under v1b the API rule's round lists the catch-all, which
    contains it; under v1c that round is not sent."""
    return [case(product="dashboard"), case(product="api"), case(product="api", severity=4)]


LABELS = [(T1, "H29"), (T2, "H16"), (T2, "H16")]
DRAWS = [0.9, 0.1, 0.3]


def run_with(propose, labels=LABELS, draws=DRAWS, prop=None, run_loop=None):
    eng = PriorityEngine(space=MI.space())
    prop = prop or proposer()
    if run_loop is None:
        res = loop.run_loop(corpus(), labels, eng, prop, F(1, 2), draws, propose=propose,
                            clock=lambda: 0.0)
    else:
        res = run_loop(corpus(), labels, eng, prop, F(1, 2), draws, clock=lambda: 0.0)
    return res, eng, prop


def record(res, eng) -> dict:
    return gates.as_json(loop.record_of(res, eng))


def base_of(rules) -> PriorityEngine:
    """An engine holding `rules`, each `(action, *conditions)`, born in order."""
    eng = PriorityEngine(space=MI.space())
    for k, (action, *conds) in enumerate(rules):
        eng.add(validate_conditions(payload(action, *conds), None), born_at=k)
    return eng


def ext(*conds) -> int:
    return MI.space().extension(validate_conditions(payload(T3, *conds), None).conditions)


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_reasoned_loops_but_for_the_pin(self):
        for k in ("MODEL", "TEMPERATURE", "REASONING", "MAX_TOKENS", "MAX_RETRIES",
                  "CALL_RETRY_WAIT", "RATE_LIMITED", "RATE_LIMIT_WAIT", "LEVEL",
                  "SYSTEM_PROMPT_SHA16"):
            with self.subTest(k):
                self.assertEqual(getattr(plan, k), getattr(rl_plan, k))
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual(plan.PROVIDER_NAME, "DeepInfra")
        self.assertEqual(plan.BRIDGE_PROVIDERS, ("baidu", "deepinfra"))
        self.assertEqual(plan.BRIDGE_PINS, {"baidu": qa_plan.PROVIDER, "deepinfra": plan.PROVIDER})
        self.assertEqual(plan.BRIDGE_NAMES, {"baidu": "Baidu", "deepinfra": "DeepInfra"})

    def test_the_arms_and_the_runs(self):
        self.assertEqual(plan.PROTOCOLS, ("v1b", "v1c"))
        self.assertEqual(plan.ARMS, ("v1b", "v1c"))
        self.assertEqual(plan.COVERAGE, F(1, 2))
        self.assertEqual(plan.COVERAGE, ch_plan.COVERAGE["c"])
        self.assertEqual((plan.REPS, plan.N, plan.SEED), (3, 2000, 17))
        self.assertEqual((plan.SMOKE_N, plan.SMOKE_ARM), (30, "v1c"))
        self.assertEqual((plan.MAX_ESCALATIONS, plan.MAX_CONSECUTIVE_FAILURES), (400, 5))
        self.assertEqual((plan.BRIDGE_TICKETS, plan.BRIDGE_DRAWN, plan.BRIDGE_ASKS), (40, 13, 1))

    def test_the_seeds_are_the_next_two_primes_after_97_and_no_closed_threads(self):
        def prime(n):
            return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))
        after = [n for n in range(98, 200) if prime(n)][:2]
        self.assertEqual([plan.ORDER_SEED, plan.BRIDGE_SEED], after)
        taken = set()
        for path in REPO.glob("*/plan.py"):
            if path.parent.name == "placement":
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, int)
                        and any(isinstance(t, ast.Name) and t.id.endswith("SEED")
                                for t in node.targets)):
                    taken.add(node.value.value)
        self.assertFalse({plan.ORDER_SEED, plan.BRIDGE_SEED} & taken)

    def test_the_lines_are_section_0s_as_fractions(self):
        self.assertEqual(plan.LINES, {"PL-a": F(3, 4), "PL-b": F(9, 10), "PL-c": F(9, 10),
                                      "PL-d": F(1, 20), "PL-e": F(9, 10), "PL-f": F(9, 10)})
        self.assertEqual(plan.PL_C_RUNS, 3)
        self.assertEqual(plan.HOLDS_AT_OR_BELOW, ("PL-a", "PL-d"))
        for v in plan.LINES.values():
            self.assertIsInstance(v, Fraction)

    def test_the_plan_states_them(self):
        for text in ("`ORDER_SEED = 101`", "`BRIDGE_SEED = 103`", "`PL_A_LINE = Fraction(3, 4)`",
                     "`PL_B_LINE = Fraction(9, 10)`", "`PL_C_RUNS = 3`",
                     "`PL_D_LINE = Fraction(1, 20)`", "`PL_E_LINE = Fraction(9, 10)`",
                     "`PL_F_LINE = Fraction(9, 10)`", "`SMOKE_N = 30`", '`SMOKE_ARM = "v1c"`',
                     "`MAX_ESCALATIONS = 400`", '"deepinfra/fp8"', "`BRIDGE_TICKETS = 40`",
                     "`BRIDGE_DRAWN = 13`", "`MIN_SIGNATURES = 1`"):
            with self.subTest(text):
                self.assertIn(text, PLAN_TEXT)

    def test_declared_transcribes_figure_1(self):
        """Every row of §0's first table is `DECLARED["rounds"]`'s, in order."""
        rows = [re.split(r"\s*\|\s*", line.strip().strip("|").strip())
                for line in PLAN_TEXT.splitlines()
                if re.match(r"^\s*\|\s*(`PLAN_\w+\.md`)?\s*\|\s*[ice] r\d\s*\|", line)]
        self.assertEqual(len(rows), 12)
        for (name, want), got in zip(plan.DECLARED["rounds"].items(), rows):
            arm, rep = name.split("/")[1].split("_r")
            with self.subTest(name):
                self.assertEqual(got[1], f"{arm} r{rep}")
                self.assertEqual([int(x.replace(",", "")) for x in got[2:]], want)
        total = next(line for line in PLAN_TEXT.splitlines() if "| **all** |" in line)
        nums = [int(x.replace(",", "")) for x in re.findall(r"\*\*([\d,]+)\*\*", total)]
        self.assertEqual(nums, plan.DECLARED["rounds_all"])

    def test_declared_transcribes_the_other_figures(self):
        d = plan.DECLARED
        for q, (u, k) in d["by_queue"].items():
            with self.subTest(q):
                self.assertRegex(PLAN_TEXT, rf"\| `{q}` \| {u} \| {k} \|")
        b = d["bridge"]
        for q in ("SECURITY_INCIDENT", "ONCALL_ESCALATION"):
            listed = ", ".join(str(i) for i in b[q][:-1]) + f" and {b[q][-1]}"
            self.assertIn(listed, " ".join(PLAN_TEXT.split()))
        drawn = ", ".join(str(i) for i in b["drawn"][:-1]) + f" and {b['drawn'][-1]}"
        self.assertIn(drawn, " ".join(PLAN_TEXT.split()))
        order = ", ".join(f"{a} r{r}" for a, r in d["schedule"])
        self.assertIn(order, " ".join(PLAN_TEXT.split()))
        h = d["hidden_v1c"]
        self.assertIn(f"{h['installed']} are installed, against v1b's 199",
                      " ".join(PLAN_TEXT.split()))
        self.assertIn(f"v1c lists {h['listed_v1c']} of them", " ".join(PLAN_TEXT.split()))
        self.assertEqual(sum(d["by_queue"][q][0] for q in d["by_queue"]), d["rounds_all"][10])
        self.assertEqual(sum(d["by_queue"][q][1] for q in d["by_queue"]), d["rounds_all"][11])
        for k, col in enumerate(plan.ROUND_KEYS):
            with self.subTest(col):
                self.assertEqual(sum(r[k] for r in d["rounds"].values()), d["rounds_all"][k])

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        first = random.Random("PLAN_PLACEMENT/order/101").choice(plan.ARMS)
        self.assertEqual(order[0], (first, 1))
        self.assertEqual([list(x) for x in order], plan.DECLARED["schedule"])
        arms = [a for a, _ in order]
        self.assertTrue(all(a != b for a, b in zip(arms, arms[1:])))

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            for path in (plan.sample_path(), plan.score_path(), plan.smoke_path(),
                         plan.bridge_path(), plan.run_path("v1c", 1),
                         plan.partial_path("bridge_baidu")):
                self.assertEqual(path.parent, d)
        with self.assertRaises(ValueError):
            plan.run_path("c", 1)
        with self.assertRaises(ValueError):
            plan.run_path("v1b", 4)

    def test_both_arms_read_plan_channels_draws(self):
        for arm in plan.ARMS:
            for rep in (1, 2, 3):
                with self.subTest(arm=arm, rep=rep):
                    ch = plan.channel_of(arm, rep)
                    self.assertEqual(ch["draws_seed"], f"PLAN_CHANNEL/channel/97/r{rep}")
                    self.assertEqual(ch["draws_sha16"], ch_plan.draws_digest(f"r{rep}"))
            self.assertEqual(plan.channel_of(arm, None)["draws_seed"],
                             "PLAN_CHANNEL/channel/97/smoke")


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_every_line_is_counted_and_one_is_needed(self):
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-08)**\n"
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
        self.assertEqual(plan.gate_signature(REPO / "PLAN_PLACEMENT.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_PLACEMENT.md"))
        self.assertEqual(plan.gate_signature()["source"], "PLAN_PLACEMENT.md")


# ---------------------------------------------------------------------------
# 2. v1c's list, on bases built by hand
# ---------------------------------------------------------------------------

class TestTheList(unittest.TestCase):

    def test_nested_rules_are_left_out_either_way_and_an_equal_one_kept(self):
        eng = base_of([API])                               # R0001: api -> T2
        got = protocol.listing_of(eng, ext(("severity", "gte", 1)), T1)
        self.assertEqual(got["left_out"], {"R0001": protocol.INSIDE})
        got = protocol.listing_of(eng, ext(("product", "eq", "api"), ("severity", "lte", 2)), T3)
        self.assertEqual(got["left_out"], {"R0001": protocol.CONTAINING})
        got = protocol.listing_of(eng, ext(("product", "eq", "api")), T3)
        self.assertEqual((got["kept"], got["left_out"]), (["R0001"], {}))

    def test_a_crossing_rule_is_kept_unless_its_conflict_is_decided(self):
        draft = ext(("severity", "lte", 2))
        live = base_of([API])
        self.assertEqual(protocol.listing_of(live, draft, T3)["kept"], ["R0001"])
        # A third rule inside both governs their whole shared region.
        governed = base_of([API, (S, ("product", "eq", "api"), ("severity", "lte", 2))])
        got = protocol.listing_of(governed, draft, T3)
        self.assertEqual(got["left_out"], {"R0001": protocol.GOVERNED, "R0002": protocol.INSIDE})
        self.assertEqual(got["kept"], [])
        # One that governs only part of it leaves the conflict open elsewhere.
        partly = base_of([API, (S, ("product", "eq", "api"), ("severity", "eq", 1))])
        got = protocol.listing_of(partly, draft, T3)
        self.assertEqual(got["kept"], ["R0001"])
        self.assertEqual(got["left_out"], {"R0002": protocol.INSIDE})

    def test_one_third_rule_beating_the_listed_rule_is_not_enough(self):
        """A defeated rule still defeats: the draft must be beaten there too."""
        eng = base_of([API, (S, ("product", "eq", "api"), ("severity", "lte", 3))])
        eng.try_edge("R0002", "R0001")                     # R0002 beats R0001 everywhere they meet
        draft = ext(("severity", "lte", 2), ("channel", "eq", "email"))
        got = protocol.listing_of(eng, draft, T3)
        self.assertIn("R0001", got["kept"])

    def test_the_exclusions_can_be_turned_off(self):
        eng = base_of([API])
        got = protocol.listing_of(eng, ext(("severity", "gte", 1)), T1, nested=False,
                                  governed=False)
        self.assertEqual((got["kept"], got["left_out"]), (["R0001"], {}))
        self.assertEqual(got["kept"], got["overlapped"])

    def test_an_empty_list_sends_no_call_and_the_draft_is_born(self):
        eng = base_of([API])
        prop = Scripted(lambda c, i: payload(*CATCH_ALL),
                        lambda *a: (_ for _ in ()).throw(AssertionError("placement asked")))
        res = protocol.propose_v1c(eng, case(), 5, plan.IMPASSE, prop, [], clock=lambda: 0.0)
        self.assertEqual(res["esc"].verdict, e.BORN)
        self.assertEqual([c["round"] for c in res["esc"].calls], [0])
        self.assertEqual(res["esc"].calls[0]["left_out"], {"R0001": protocol.INSIDE})
        self.assertEqual(res["esc"].listed, [])


# ---------------------------------------------------------------------------
# 3. v1c off is v1b, and the loop under v1b is PLAN_CHANNEL.md's
# ---------------------------------------------------------------------------

class TestTheLoopIsChannels(unittest.TestCase):

    def test_under_v1b_the_loop_is_channels_record_for_record(self):
        ours = record(*run_with(loop.ESCALATIONS["v1b"])[:2])
        theirs = record(*run_with(None, run_loop=ch_loop.run_loop)[:2])
        self.assertEqual(ours, theirs)

    def test_v1c_with_both_exclusions_off_is_v1b(self):
        off = functools.partial(protocol.propose_v1c, nested=False, governed=False)
        a = record(*run_with(loop.ESCALATIONS["v1b"])[:2])
        b = record(*run_with(off)[:2])
        self.assertEqual(protocol.without_v1c_keys(b), a)

    def test_v1c_leaves_the_round_v1b_sends_unsent(self):
        res_b, _, prop_b = run_with(loop.ESCALATIONS["v1b"])
        res_c, eng_c, prop_c = run_with(loop.ESCALATIONS["v1c"])
        self.assertEqual([x[0] for x in prop_b.asked], ["first", "first", "placement"])
        self.assertEqual([x[0] for x in prop_c.asked], ["first", "first"])
        self.assertEqual(res_b.loop.calls - res_c.loop.calls, 1)
        self.assertEqual([r.action for r in eng_c.rules], [T1, T2])

    def test_the_escalations_are_named_by_arm(self):
        self.assertEqual(set(loop.ESCALATIONS), set(plan.ARMS))
        self.assertIs(loop.ESCALATIONS["v1b"], rl_loop.propose_v1b)
        self.assertIs(loop.escalates, ch_loop.escalates)


# ---------------------------------------------------------------------------
# 4. The list reads no label
# ---------------------------------------------------------------------------

class TestTheTriggerIsTheOnlyReader(unittest.TestCase):
    """Run A and run B differ in every label but one and in every draw; both
    escalate case 0 as an impasse and case 1 as a reported error, and let case
    2 stand right."""

    A = ([(T1, "H29"), (T2, "H16"), (T2, "H16")], [0.9, 0.1, 0.3])
    B = ([(T3, "H06"), (S, "H01"), (T2, "H17")], [0.0, 0.49, 0.7])

    def test_the_proposer_the_lists_and_the_base_see_the_same(self):
        for proto in plan.PROTOCOLS:
            with self.subTest(proto):
                ra, ea, pa = run_with(loop.ESCALATIONS[proto], *self.A)
                rb, eb, pb = run_with(loop.ESCALATIONS[proto], *self.B)
                self.assertEqual([c["cause"] for c in ra.causes], [c["cause"] for c in rb.causes])
                self.assertEqual(pa.asked, pb.asked)
                self.assertEqual([x.calls for x in ra.loop.escalations],
                                 [x.calls for x in rb.loop.escalations])
                self.assertEqual([(r.rule_id, r.action, r.beats, r.loses_to) for r in ea.rules],
                                 [(r.rule_id, r.action, r.beats, r.loses_to) for r in eb.rules])

    def calls_in(self, src: str) -> list[ast.Call]:
        out = []
        for node in ast.walk(ast.parse(src)):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            if ((isinstance(fn, ast.Name) and fn.id in ("propose", "propose_v1c"))
                    or (isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
                        and fn.value.id in ("proposer", "prop"))):
                out.append(node)
        return out

    def test_nothing_the_trigger_reads_is_handed_to_the_proposer(self):
        forbidden = {"truth", "trule", "labels", "draw", "draws", "told", "coverage"}
        sources = {rel: (REPO / rel).read_text()
                   for rel in ("placement/loop.py", "placement/run.py")}
        sources["placement.protocol.propose_v1c"] = textwrap.dedent(
            inspect.getsource(protocol.propose_v1c))
        found = 0
        for rel, src in sources.items():
            inner = rel.startswith("placement.protocol")
            for call in self.calls_in(src):
                found += 1
                names = {n.id for a in [*call.args, *[k.value for k in call.keywords]]
                         for n in ast.walk(a) if isinstance(n, ast.Name)}
                with self.subTest(rel=rel, call=ast.unparse(call)):
                    self.assertFalse(names & (forbidden | ({"cause"} if inner else set())))
        self.assertGreaterEqual(found, 3)

    def test_every_comparison_with_the_label_is_listed_here(self):
        found = []
        for rel in ("placement/loop.py", "placement/run.py", "placement/plan.py",
                    "placement/protocol.py"):
            tree = ast.parse((REPO / rel).read_text())
            for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
                for node in ast.walk(fn):
                    if isinstance(node, ast.Compare) and any(
                            isinstance(n, ast.Name) and n.id in ("truth", "trule", "labels")
                            for x in (node.left, *node.comparators) for n in ast.walk(x)):
                        found.append((rel, fn.name, ast.unparse(node)))
        self.assertEqual(sorted(found), sorted([
            ("placement/loop.py", "run_loop", "predicted == truth"),
            ("placement/loop.py", "run_loop", "predicted == truth")]))

    def test_the_proposers_path_names_no_policy(self):
        for rel in ("placement/protocol.py", "placement/loop.py", "placement/run.py"):
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


# ---------------------------------------------------------------------------
# 5. The resume
# ---------------------------------------------------------------------------

class LiveScript:
    """A live model that answers or raises what it is handed, one per call."""

    def __init__(self, *items):
        self.items, self.extra, self.sent = list(items), {}, []

    def ask(self, messages):
        self.sent.append(messages)
        got = self.items.pop(0)
        if isinstance(got, Exception):
            raise got
        self.extra = got.extra()
        return got


class TestTheResume(unittest.TestCase):

    def test_a_resumed_record_keeps_each_calls_own_seconds_and_hour(self):
        header = {"plan": "test"}
        corp, labels = [case(product="api"), case()], [(T2, "H01"), (T1, "H29")]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            rows, _ = erun.open_partial(path, header)
            live = run.Stamped(LiveScript(e.ProposalFailed("no parse", "stop", 3, []),
                                          answer(payload(*CATCH_ALL))),
                               path, rows, clock=iter([0.0, 7.5, 10.0, 52.0]).__next__)
            asked = loop.run_loop(corp, labels, PriorityEngine(space=MI.space()), live,
                                  F(1, 2), [0.1, 0.9], propose=loop.ESCALATIONS["v1c"],
                                  clock=itertools.count(0.0, 5.0).__next__)
            live.flush()
            kept = [json.loads(x) for x in path.read_text().splitlines()[1:]]
            self.assertTrue(all(r.get("kept_at") for r in kept))
            self.assertEqual(run.first_kept(path), min(r["kept_at"] for r in kept))
            rows, resumed = erun.open_partial(path, header)
            self.assertTrue(resumed)
            served = loop.run_loop(corp, labels, PriorityEngine(space=MI.space()),
                                   run.Stamped(LiveScript(), path, rows), F(1, 2), [0.1, 0.9],
                                   propose=loop.ESCALATIONS["v1c"],
                                   clock=itertools.count(0.0, 0.01).__next__)
        for res, seconds in ((asked, [5.0, 5.0]), (served, [7.5, 42.0])):
            with self.subTest(seconds=seconds):
                calls = [esc.calls[0] for esc in res.loop.escalations]
                self.assertEqual([c["seconds"] for c in calls], seconds)

    def test_a_partial_under_another_protocol_or_other_draws_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "x.partial.jsonl"
            mine = run.protocol_header("v1c", plan.N, "v1c_r1", 1)
            erun.open_partial(path, mine)
            for other in (run.protocol_header("v1b", plan.N, "v1c_r1", 1),
                          run.protocol_header("v1c", plan.N, "v1c_r1", 2)):
                self.assertNotEqual(other, mine)
                with self.assertRaises(SystemExit):
                    erun.open_partial(path, other)

    def test_the_header_names_the_pin_and_the_protocol(self):
        h = run.protocol_header("v1b", plan.N, "v1b_r2", 2)
        self.assertEqual((h["protocol"], h["provider"]), ("v1b", plan.PROVIDER))
        self.assertEqual(h["draws_seed"], "PLAN_CHANNEL/channel/97/r2")
        self.assertEqual(run.bridge_header("baidu")["provider"], qa_plan.PROVIDER)
        self.assertEqual(run.bridge_header("deepinfra")["provider"], plan.PROVIDER)

    def test_the_loop_does_not_swallow_an_outage(self):
        class Refused:
            name = "refused"

            def first(self, case, idx):
                raise p.RateLimited("refused")

        with self.assertRaises(p.RateLimited):
            loop.run_loop([case()], [(T1, "H29")], PriorityEngine(space=MI.space()),
                          Refused(), F(1, 2), [0.3], propose=loop.ESCALATIONS["v1c"])


# ---------------------------------------------------------------------------
# 6. Nothing unsigned, and the order of events
# ---------------------------------------------------------------------------

def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(g1=g, g2=g, g3=g, g4=SIGNED)


def stage_a(d: Path, **over) -> None:
    refs = {"fingerprint": p.fingerprint(), "schedule": [list(x) for x in plan.schedule()],
            "streams": {n: {"seed": plan.draw_seed(n), "sha16": plan.draws_digest(n)}
                        for n in plan.STREAMS},
            "bridge": {"tickets": plan.bridge_tickets()}}
    refs.update(over)
    (d / "sample.json").write_text(json.dumps({"references": refs}))


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(protocol, "Asker",
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
        self.refuses(run.main, ["--bridge"])
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
             mock.patch.object(protocol, "Asker",
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
            for argv in (["--smoke"], ["--bridge"], ["--arm", "v1c", "--rep", "1"]):
                with self.subTest(argv), self.assertRaises(SystemExit):
                    run.main(argv)           # no Stage A record
            stage_a(d)
            self.assertTrue(run.sample_check()[0])
            for argv in (["--bridge"], ["--arm", "v1c", "--rep", "1"]):
                with self.subTest(argv), self.assertRaises(SystemExit):
                    run.main(argv)           # no smoke record
        fetch.assert_not_called()
        checks.assert_not_called()

    def test_a_stage_a_record_under_another_schedule_draws_or_bridge_is_refused(self):
        with TempOut() as d:
            for over in ({"schedule": [["v1b", 1]]},
                         {"streams": {"r1": {"seed": "x", "sha16": "y"}}},
                         {"fingerprint": "0" * 16}, {"bridge": {"tickets": [1, 2]}}):
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
    calls = [{"round": 0, "failure": None, "call_attempts": [dict(attempt)],
              "left_out": {"R0001": protocol.INSIDE}},
             {"round": 1, "failure": None, "call_attempts": [dict(attempt)]}]
    rec = {**run.protocol_header(plan.SMOKE_ARM, plan.SMOKE_N, "smoke", None),
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
        self.assertIn("1 rounds leaving a rule out", why)

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
        nothing_left = smoke_record()
        del nothing_left["escalations"][0]["calls"][0]["left_out"]
        lost = smoke_record(records=smoke_rows()[:-1])
        other = smoke_record(protocol="v1b")
        for name, rec in (("elsewhere", bad), ("did not reason", quiet), ("cut", cut),
                          ("no placement", unplaced), ("nothing left out", nothing_left),
                          ("rows", lost), ("protocol", other)):
            with self.subTest(name):
                self.assertFalse(self.check(rec)[0])


# ---------------------------------------------------------------------------
# 8. The bridge
# ---------------------------------------------------------------------------

class TestTheBridge(unittest.TestCase):

    def test_the_draw_is_its_seed_strings(self):
        cands = list(range(0, 400, 3))
        got = plan.bridge_draw(cands)
        want = sorted(random.Random("PLAN_PLACEMENT/bridge/103").sample(sorted(cands), 13))
        self.assertEqual(got, want)
        self.assertEqual(plan.bridge_draw(list(reversed(cands))), got)
        for idx in (18, 1951):
            self.assertEqual(plan.bridge_first(idx), random.Random(
                f"PLAN_PLACEMENT/bridge/103/{idx}").choice(("baidu", "deepinfra")))

    def test_every_ticket_is_asked_of_each_provider_once_the_drawn_first(self):
        asks = plan.bridge_asks()
        tickets = plan.bridge_tickets()
        self.assertEqual(len(tickets), len(set(tickets)), plan.BRIDGE_TICKETS)
        self.assertEqual(tickets, sorted(tickets))
        self.assertEqual(len(asks), 80)
        for k in range(0, len(asks), 2):
            (i, a), (j, b) = asks[k], asks[k + 1]
            self.assertEqual(i, j)
            self.assertEqual(a, plan.bridge_first(i))
            self.assertEqual({a, b}, set(plan.BRIDGE_PROVIDERS))

    def test_the_same_under_any_hash_seed(self):
        code = ("import json; from placement import plan; "
                "print(json.dumps([plan.schedule(), plan.bridge_asks()]))")
        outs = set()
        for seed in ("0", "1", "4242"):
            env = {**os.environ, "PYTHONHASHSEED": seed}
            outs.add(subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                                    capture_output=True, text=True, check=True).stdout)
        self.assertEqual(len(outs), 1)


# ---------------------------------------------------------------------------
# 9. The request
# ---------------------------------------------------------------------------

class DeepInfraReasons(OpenRouterShapedClient):
    PROVIDER = "DeepInfra"


class TestTheRequest(unittest.TestCase):

    def test_it_is_plan_reasoned_loops_but_for_the_pin(self):
        msgs = p.messages_for(case())
        holder = SimpleNamespace(model=plan.MODEL)
        for pin in (plan.PROVIDER, plan.BRIDGE_PINS["baidu"]):
            for attempt in (0, 1):
                ours = protocol.request_with(pin, plan.MODEL, "v1c", msgs, attempt)
                theirs = p.Asker.request(holder, "v1b", msgs, attempt)
                self.assertEqual(ours["extra_body"]["provider"], pin)
                ours["extra_body"]["provider"] = theirs["extra_body"]["provider"]
                self.assertEqual(ours, theirs)

    def test_the_asker_sends_the_pin_through_the_sdk(self):
        text = json.dumps(payload(*CATCH_ALL))
        for pin in (None, plan.BRIDGE_PINS["baidu"]):
            client = DeepInfraReasons(FixedResponses(text))
            with fake_sdk(openai=client):
                live = p.Live(protocol.Asker(pin=pin, sleep=lambda s: None))
                live.ask(p.messages_for(case()))
            (req,) = client.peticiones
            self.assertEqual(req["extra_body"]["provider"], pin or plan.PROVIDER)
            self.assertEqual(req["extra_body"]["reasoning"], {"effort": "high"})
            self.assertEqual((req["temperature"], req["max_tokens"]), (0, 16000))
            self.assertEqual(req["response_format"], {"type": "json_object"})


# ---------------------------------------------------------------------------
# 10. Stage C's terms
# ---------------------------------------------------------------------------

def runs_of(**arms) -> dict[str, list[dict]]:
    out = {a: [] for a in plan.ARMS}
    for a, rows in arms.items():
        out[a] = [{"space": s, "refused": r, "oncall": o} for s, r, o in rows]
    return out


class TestStageC(unittest.TestCase):

    def test_the_lines_are_exact_on_both_sides(self):
        self.assertTrue(score.holds("PL-a", F(3, 4)))
        self.assertFalse(score.holds("PL-a", F(3, 4) + F(1, 10 ** 9)))
        self.assertTrue(score.holds("PL-d", F(1, 20)))
        self.assertFalse(score.holds("PL-d", F(1, 20) + F(1, 10 ** 9)))
        self.assertTrue(score.holds("PL-b", F(9, 10)))
        self.assertFalse(score.holds("PL-b", F(9, 10) - F(1, 10 ** 9)))

    def test_medians_ratios_and_thin(self):
        runs = runs_of(v1b=[("19/20", "1/5", "1"), ("1", "1/4", "1"), ("9/10", "1/10", "1")],
                       v1c=[("19/20", "1/10", "2/3"), ("1", "1/20", "1"), ("1/2", "3/20", "1")])
        a = score.row("PL-a", runs)
        self.assertEqual((a["verdict"], F(a["value"]["fraction"])), (score.HOLDS, F(1, 2)))
        self.assertTrue(a["thin"])          # v1b's 1/10 in its median's place reads 1
        b = score.row("PL-b", runs)
        self.assertEqual((b["verdict"], F(b["value"]["fraction"])), (score.HOLDS, F(19, 20)))
        self.assertTrue(b["thin"])          # v1c's 1/2 in its median's place
        d = score.row("PL-d", runs)
        self.assertEqual(F(d["value"]["fraction"]), F(0))
        f = score.row("PL-f", runs)
        self.assertEqual(f["verdict"], score.HOLDS)
        self.assertTrue(f["thin"])

    def test_pl_c_counts_runs_and_every_hold_is_thin(self):
        for spaces, verdict, thin in ((("1", "19/20", "9/10"), score.HOLDS, True),
                                      (("1", "19/20", "1/2"), score.REFUTED, True),
                                      (("1", "1/2", "1/2"), score.REFUTED, False)):
            with self.subTest(spaces):
                c = score.row("PL-c", runs_of(v1c=[(s, "0", "1") for s in spaces]))
                self.assertEqual((c["verdict"], c["thin"]), (verdict, thin))
        short = score.row("PL-c", runs_of(v1c=[("1", "0", "1"), ("1", "0", "1")]))
        self.assertEqual(short["verdict"], score.NO_VALUE)

    def test_every_reason_a_row_has_no_value(self):
        one = runs_of(v1b=[("1", "1/5", "1")], v1c=[("1", "1/5", "1"), ("1", "1/5", "1")])
        for rid in ("PL-a", "PL-d", "PL-e"):
            with self.subTest(rid):
                self.assertEqual(score.row(rid, one)["verdict"], score.NO_VALUE)
        zero = runs_of(v1b=[("1", "0", "1")] * 3, v1c=[("1", "1/5", "1")] * 3)
        self.assertEqual(score.row("PL-a", zero)["verdict"], score.NO_VALUE)

    def test_refused_counts_unplaced_answers_only(self):
        answered = {"verdict": e.UNPLACED, "calls": [{"round": 0, "failure": None},
                                                     {"round": 1, "failure": None}]}
        lost = {"verdict": e.UNPLACED, "calls": [{"round": 0, "failure": None},
                                                 {"round": 1, "failure": "timeout"}]}
        born = {"verdict": e.BORN, "calls": [{"round": 0, "failure": None}]}
        self.assertEqual(score.refused_of({"escalations": [answered, lost, born, born]}), F(1, 4))
        self.assertIsNone(score.refused_of({"escalations": []}))


# ---------------------------------------------------------------------------
# 11. What decides nothing
# ---------------------------------------------------------------------------

class TestWhatDecidesNothing(unittest.TestCase):

    def test_a_nested_pair_and_a_governed_one_change_nothing_and_a_live_one_does(self):
        nested = base_of([API, CATCH_ALL])                 # R0001 inside R0002
        self.assertFalse(references.would_change(nested, "R0001", "R0002"))
        self.assertFalse(references.would_change(nested, "R0002", "R0001"))
        live = base_of([API, (T3, ("severity", "lte", 2))])
        self.assertTrue(references.would_change(live, "R0001", "R0002")
                        or references.would_change(live, "R0002", "R0001"))
        governed = base_of([API, (T3, ("severity", "lte", 2)),
                            (S, ("product", "eq", "api"), ("severity", "lte", 2))])
        self.assertFalse(references.would_change(governed, "R0001", "R0002"))
        self.assertFalse(references.would_change(governed, "R0002", "R0001"))

    def test_an_edge_that_closes_a_cycle_installs_nothing(self):
        eng = base_of([API, (T3, ("severity", "lte", 2)), (S, ("channel", "eq", "email"))])
        self.assertEqual(eng.try_edge("R0001", "R0002"), "ok")
        self.assertEqual(eng.try_edge("R0002", "R0003"), "ok")
        self.assertFalse(references.would_change(eng, "R0003", "R0001")
                         and eng._reaches("R0001", "R0003") is False)
        self.assertTrue(eng._reaches("R0001", "R0003"))
        self.assertFalse(references.would_change(eng, "R0003", "R0001"))


if __name__ == "__main__":
    unittest.main()
