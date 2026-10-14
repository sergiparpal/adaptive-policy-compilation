"""
PLAN_SCREEN.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. And that the inputs and the client are
    `PLAN_FIDELITY.md`'s, imported rather than retyped (rule A).
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `screen/ask.py` exits before it builds the client.
  * `V-g1` to `V-g3` on the real records: the populations §0 states, the
    tickets counted by their attributes, the prompts against F-f's digests, and
    `PLAN_FIDELITY.md`'s Stage C given back in memory. And their teeth: a
    changed screen moves a digest, and a tampered record is caught.
  * The request: through the SDK double, the wrapped client sends exactly what
    the bare one sends, and keeps each attempt's `finish_reason`.
  * Stage C's arithmetic on entries small enough to check by hand, §0's rule for
    a run without a value and for the median, and each verdict at its edge.
  * Stage B end to end through the double, including resuming and stopping on
    an outage, and Stage C over the records the double produced.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double or something that fails the test if it is ever built. **No figure of
the held-out decisions is computed, not even silently**: Stage A's readout is
replaced by a stub wherever a test writes a Stage A record, because the share of
held-out screens whose plurality is right is what §10 keeps behind the gate.
"""

from __future__ import annotations

import dataclasses
import functools
import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from fidelity import plan as fidelity_plan
from fidelity import prompts
from rung2.proposers2 import ProposalError, render_base_v1

from screen import ask, plan, sample, score
from tests.doubles import FakeOpenAIClient, FixedResponses, fake_sdk

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {**UNSIGNED, "passes": True, "unsigned": 0}
GOOD = ('{"action": "T2_TECHNICAL", "conditions": '
        '[{"attr": "severity", "op": "lte", "value": 2}], "beats": [], '
        '"loses_to": [], "note": "x"}')
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
MANAGEMENT_KEY = (200, {"data": {"is_management_key": True}})


@functools.lru_cache(maxsize=1)
def real_checks() -> sample.Checks:
    """The checks on the real records, without the suite, built once."""
    return sample.run_checks(suite=False)


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_lines_of_section_0(self):
        self.assertEqual((plan.V_A_MAX_GAP, plan.V_B_REFUTED_AT_OR_BELOW,
                          plan.V_C_MIN_PULL, plan.V_D_REFUTED_AT_OR_BELOW),
                         (0.05, 0.0, 0.10, 0.0))

    def test_the_constants_of_section_10(self):
        self.assertEqual(plan.PILOT_PER_RUN, 100)
        self.assertEqual(plan.PILOT_PER_RUN, fidelity_plan.TICKET_ONLY_PER_RUN)
        self.assertEqual(plan.HELD_OUT_SIZES, {1: 429, 2: 405, 3: 425})
        self.assertEqual((plan.TICKETS, plan.ASKED_BY_F_F), (1184, 301))
        self.assertEqual((plan.TICKET_ONLY_DRAWS, plan.ANCHOR_DRAWS,
                          plan.SMOKE_PER_ARM), (2, 1, 5))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MAX_INVALID_SHARE,
                          plan.MIN_PULL_POPULATION, plan.MIN_CELL), (1, 0.05, 100, 50))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 53)
        self.assertNotIn(plan.ORDER_SEED, {17, 18, 19, 20, 25, 41, 43, 47})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_inputs_and_the_client_are_fidelitys_imported(self):
        for name in ("RUNS", "N", "SEED", "MODEL", "PROMPT", "REASONING", "RARE"):
            with self.subTest(name):
                self.assertEqual(getattr(plan, name), getattr(fidelity_plan, name))
        source = Path("screen/plan.py").read_text()
        self.assertNotIn("deepseek", source)
        self.assertNotIn('"effort"', source)
        self.assertEqual(plan.FIDELITY_SAMPLE, fidelity_plan.SAMPLE_PATH)
        self.assertEqual(plan.fidelity_base(2), fidelity_plan.ask_path("base2"))

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_SCREEN.md"))
        self.assertEqual(plan.OUT, Path("results_screen"))

    def test_one_stream_per_session_and_pass(self):
        a = [plan.order_rng("ticket_only", 1).random() for _ in range(3)]
        self.assertEqual(a, [plan.order_rng("ticket_only", 1).random() for _ in range(3)])
        self.assertNotEqual(a, [plan.order_rng("ticket_only", 2).random() for _ in range(3)])
        self.assertNotEqual(a, [fidelity_plan.order_rng("ticket_only", 1).random()
                                for _ in range(3)])

    def test_the_sessions_and_where_they_land(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "anchor", "ticket_only"))
        self.assertEqual(plan.ask_path("anchor"), Path("results_screen/ask_anchor.json"))
        with self.assertRaises(ValueError):
            plan.ask_path("births")
        self.assertIn("results_screen/*.partial.jsonl", Path(".gitignore").read_text())


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ________________________ (date: ______________)**\n"
        )["passes"])

    def test_one_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-15)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-15)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


class TestThePopulationsAndTheTickets(unittest.TestCase):
    """`V-g2` and `V-g3` on the real records. Silent when they pass."""

    @classmethod
    def setUpClass(cls):
        cls.checks = real_checks()
        cls.d = cls.checks.design

    def test_the_blocking_checks_pass(self):
        for g in (self.checks.vg1, self.checks.vg2, self.checks.vg3):
            self.assertEqual(g["first_problems"], [])
            self.assertTrue(g["passes"])

    def test_the_held_out_sizes_are_section_0s(self):
        self.assertEqual({k: len(v) for k, v in self.d.held_out.items()},
                         plan.HELD_OUT_SIZES)

    def test_the_pilot_is_the_first_hundred_and_f_f_asked_its_tickets(self):
        fid = self.d.fidelity
        for k in plan.RUNS:
            self.assertEqual(self.d.pilot[k], fid.draw[k]["uniform"][:100])
            for i in self.d.pilot[k]:
                self.assertIsNotNone(
                    self.d.tickets[self.d.ticket_of(k, i)]["asked_by_F_f"])

    def test_no_held_out_decision_is_on_a_ticket_f_f_asked(self):
        for k in plan.RUNS:
            for i in self.d.held_out[k]:
                self.assertIsNone(self.d.tickets[self.d.ticket_of(k, i)]["asked_by_F_f"])

    def test_a_ticket_is_its_attributes(self):
        corpus = self.d.fidelity.corpus
        keys = set()
        for t in self.d.tickets.values():
            ks = {corpus[i].key() for i in t["cases"]}
            self.assertEqual(len(ks), 1)
            self.assertEqual(t["idx"], min(t["cases"]))
            keys |= ks
        self.assertEqual(len(keys), len(self.d.tickets))
        self.assertEqual(len(self.d.tickets), plan.TICKETS)
        asked = [t for t in self.d.tickets.values() if t["asked_by_F_f"]]
        self.assertEqual(len(asked), plan.ASKED_BY_F_F)
        self.assertEqual(sum(1 for t in self.d.tickets.values() if t["rare"]), 27)

    def test_every_decision_has_a_screen_and_its_plurality(self):
        for did, x in self.d.decisions.items():
            p = self.d.fidelity.prompts[did]
            self.assertEqual(x["plurality"], prompts.plurality(p))
            self.assertEqual(x["first_shown"], prompts.first_shown(p))
            if x["population"] == sample.HELD_OUT:
                self.assertTrue(x["shown_ids"])

    def test_the_prompts_are_the_ones_f_f_recorded(self):
        recorded = json.loads(plan.FIDELITY_SAMPLE.read_text())["items"]
        for t in self.d.tickets.values():
            self.assertEqual(self.d.prompts[t["id"]].base_text, prompts.EMPTY_BASE)
            if t["asked_by_F_f"]:
                self.assertEqual(recorded[t["asked_by_F_f"]]["digest"], t["digest"])
        for k in plan.RUNS:
            for i in self.d.pilot[k]:
                self.assertEqual(recorded[f"d{k}:{i}"]["digest"],
                                 self.d.prompts[f"d{k}:{i}"].digest)

    def test_a_changed_screen_moves_the_digest(self):
        """The teeth of `V-g2`: one more rule on a screen is another prompt."""
        did = f"d1:{self.d.pilot[1][0]}"
        p = self.d.prompts[did]
        probe = prompts._PROBE
        changed = dataclasses.replace(p, base_text=render_base_v1([probe], prompts.COVERAGE))
        self.assertNotEqual(changed.digest, p.digest)

    def test_the_sessions(self):
        s = self.d.sessions
        self.assertEqual(len(s["ticket_only"]["passes"]), 2)
        for order in s["ticket_only"]["passes"]:
            self.assertEqual(sorted(order), sorted(self.d.tickets))
        self.assertNotEqual(s["ticket_only"]["passes"][0], s["ticket_only"]["passes"][1])
        self.assertEqual(sorted(s["anchor"]["passes"][0]),
                         sorted(f"d{k}:{i}" for k in plan.RUNS for i in self.d.pilot[k]))
        self.assertEqual(len(s["anchor"]["passes"]), 1)
        kinds = [self.d.items[i]["kind"] for i in s["smoke"]["items"]]
        self.assertEqual(kinds.count(prompts.TICKET_ONLY), 5)
        self.assertEqual(kinds.count(prompts.HIDDEN), 5)

    def test_the_design_is_deterministic(self):
        again = sample.build_design(self.d.fidelity)
        self.assertEqual(again.sessions, self.d.sessions)
        self.assertEqual(again.decisions, self.d.decisions)


class TestTheInputsReproduceThemselves(unittest.TestCase):
    """`V-g1`'s halves on the real records, and their teeth."""

    @classmethod
    def setUpClass(cls):
        cls.checks = real_checks()

    def test_f_f_stage_c_is_given_back(self):
        self.assertEqual(sample.fidelity_stage_c(self.checks.design.fidelity,
                                                 self.checks.found), [])

    def test_a_tampered_score_is_caught(self):
        stored = json.loads(plan.FIDELITY_SCORE.read_text())
        stored["verdicts"]["F-c"]["verdict"] = "holds"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "score.json"
            p.write_text(json.dumps(stored))
            with mock.patch.object(plan, "FIDELITY_SCORE", p):
                problems = sample.fidelity_stage_c(self.checks.design.fidelity,
                                                   self.checks.found)
        self.assertEqual(len(problems), 1)
        self.assertIn("verdicts", problems[0])

    def test_the_records_are_under_f_fs_protocol(self):
        self.assertEqual(sample.fidelity_records(self.checks.found), [])
        found = {"base1": {**self.checks.found["base1"], "model": "another/model"}}
        self.assertTrue(sample.fidelity_records(found))


class TestTheRequestIsUnchanged(unittest.TestCase):
    """§1: the wrapper keeps `finish_reason` and changes no request."""

    def proposer(self, client, wrapped: bool):
        from rung2.proposers2 import OpenRouterProposer2
        with fake_sdk(openai=client):
            p = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                    reasoning=plan.REASONING)
        return p, (ask.wrap(p) if wrapped else None)

    def test_the_wrapper_passes_every_request_through(self):
        d = real_checks().design
        ids = d.sessions["smoke"]["items"]
        bare, wrapped = FakeOpenAIClient(FixedResponses(GOOD)), FakeOpenAIClient(
            FixedResponses(GOOD))
        p0, _ = self.proposer(bare, False)
        p1, rec = self.proposer(wrapped, True)
        for iid in ids:
            pr = d.prompts[iid]
            self.assertEqual(p0.propose(pr.case, pr.base_text),
                             p1.propose(pr.case, pr.base_text))
            self.assertEqual(rec.take(), [{"finish_reason": None, "error": None}])
        self.assertEqual(bare.peticiones, wrapped.peticiones)
        self.assertEqual(len(wrapped.peticiones), len(ids))

    def test_each_attempt_is_kept(self):
        answers = iter([("{not json", "length"), (GOOD, "stop")])

        def create(**kwargs):
            text, why = next(answers)
            return SimpleNamespace(choices=[SimpleNamespace(
                message=SimpleNamespace(content=text), finish_reason=why)])

        client = SimpleNamespace(chat=SimpleNamespace(
            completions=SimpleNamespace(create=create)))
        p, rec = self.proposer(client, True)
        case = real_checks().design.prompts[next(iter(real_checks().design.tickets))]
        action, _ = p.propose(case.case, case.base_text)
        self.assertEqual(action, "T2_TECHNICAL")
        self.assertEqual(rec.take(), [{"finish_reason": "length", "error": None},
                                      {"finish_reason": "stop", "error": None}])
        self.assertEqual(rec.take(), [])

    def test_an_error_is_kept_and_raised_as_it_was(self):
        def create(**kwargs):
            raise ConnectionError("down")

        client = SimpleNamespace(chat=SimpleNamespace(
            completions=SimpleNamespace(create=create)))
        p, rec = self.proposer(client, True)
        pr = real_checks().design.prompts[next(iter(real_checks().design.tickets))]
        with self.assertRaises(ProposalError):
            p.propose(pr.case, pr.base_text)
        self.assertEqual(rec.take(), [{"finish_reason": None, "error": "ConnectionError"}] * 3)


def entry(t, b, y="A", p="A", first=None, shown=("A", "B")):
    return {"y": y, "t": tuple(t), "b": tuple(b), "p": p,
            "first": first or p, "shown": set(shown)}


class TestTheArithmetic(unittest.TestCase):

    def test_complete_needs_the_four_answers_and_the_label(self):
        self.assertTrue(score.complete(entry("AA", "AA")))
        self.assertFalse(score.complete(entry(("A", None), "AA")))
        self.assertFalse(score.complete(entry("AA", (None, "A"))))
        self.assertFalse(score.complete({**entry("AA", "AA"), "y": None}))

    def test_v_b(self):
        es = [entry("AA", "BB"), entry("AB", "AA"), entry(("A", None), "BB")]
        self.assertEqual(score.values_v_b(es), [1.0, -0.5])

    def test_v_c_reads_t1_for_the_population_and_t2_for_the_baseline(self):
        es = [entry("BB", "AA", p="A"),      # t1 != p: b on p 1.0, t2 on p 0 -> 1.0
              entry("BA", "BB", p="A"),      # t1 != p: b on p 0.0, t2 on p 1 -> -1.0
              entry("AB", "AA", p="A")]      # t1 == p: not in V-c
        self.assertEqual(score.values_v_c(es), [1.0, -1.0])

    def test_v_d_splits_by_whether_the_plurality_is_right(self):
        es = [entry("BB", "AA", y="A", p="A"),     # cell 1: b 1.0 − t 0.0
              entry("AA", "BB", y="A", p="B"),     # cell 2: t 1.0 − b 0.0
              entry("AB", "AB", y="A", p="B")]     # cell 2: 0
        c1, c2 = score.values_v_d(es)
        self.assertEqual((c1, c2), ([1.0], [1.0, 0.0]))

    def test_a_run_without_a_value(self):
        good = [entry("AB", "BB")] * 133
        lacking = [entry(("A", None), "BB")]
        r = score.score_run(1, good + lacking * 7, 2000)       # 7 of 140: exactly 5%
        self.assertTrue(r["validity"]["defined"])
        r = score.score_run(1, good + lacking * 8, 2000)       # 8 of 141: above it
        self.assertEqual(r["validity"]["lacking_the_four_answers"], 8)
        self.assertFalse(r["validity"]["defined"])
        self.assertEqual(set(r["rows"].values()), {None})

    def test_v_c_and_v_d_need_their_populations(self):
        few = [entry("BB", "AA", p="A")] * 99 + [entry("AA", "AA", p="A")] * 60
        r = score.score_run(1, few, 2000)
        self.assertIsNone(r["rows"]["V-c"])           # 99 < 100
        self.assertIsNotNone(r["rows"]["V-d.1"])      # 159 with p = y
        self.assertIsNone(r["rows"]["V-d.2"])         # none with p != y
        r = score.score_run(1, few + [entry("BB", "AA", p="A")], 2000)
        self.assertIsNotNone(r["rows"]["V-c"])

    def test_the_standard_error_and_its_correction(self):
        vals = [0.0, 1.0] * 50
        bare = score.standard_error(vals)
        self.assertAlmostEqual(score.standard_error(vals, 0.75), bare * 0.5)
        self.assertIsNone(score.standard_error([1.0]))

    def test_the_median_rule_of_section_0(self):
        m = score.median_rule([(0.3, 0.01), (0.1, 0.02), (0.2, 0.03)])
        self.assertEqual((m["median"], m["standard_error"]), (0.2, 0.03))
        m = score.median_rule([(0.3, 0.01), (None, None), (0.1, 0.04)])
        self.assertAlmostEqual(m["median"], 0.2)
        self.assertEqual(m["standard_error"], 0.04)          # the larger of two
        m = score.median_rule([(0.3, 0.01), (None, None), (None, None)])
        self.assertIsNone(m["median"])

    def test_v_a_by_hand(self):
        d = SimpleNamespace(tickets={
            "t:1": {"id": "t:1", "asked_by_F_f": "t:9"},
            "t:2": {"id": "t:2", "asked_by_F_f": None}})
        new = {"t:1": {"answers": {1: "A", 2: "A"}}, "t:2": {"answers": {1: "A", 2: "B"}}}
        old = {"t:9": {"answers": {1: "A", 2: "B"}}}
        c = score.ticket_clause(d, new, old)
        self.assertEqual((c["n"], c["S"], c["A"], c["gap"]), (1, 1.0, 0.5, 0.5))
        anchor = {"d1:5": {"run": 1, "answers": {1: "A"}}}
        bases = {1: {"d1:5": {"answers": {1: "A", 2: "A"}}}}
        c = score.screen_clause(anchor, bases)
        self.assertEqual((c["n"], c["S"], c["A"], c["gap"]), (1, 1.0, 1.0, 0.0))

    def test_the_verdicts_at_their_edges(self):
        self.assertEqual(score.verdict_v_a([0.05, 0.0]), score.HOLDS)
        self.assertEqual(score.verdict_v_a([0.05, 0.0501]), score.REFUTED)
        self.assertEqual(score.verdict_v_a([0.0, None]), score.NO_VERDICT)
        self.assertEqual(score.verdict_v_b(0.0), score.REFUTED)
        self.assertEqual(score.verdict_v_b(1e-9), score.HOLDS)
        self.assertEqual(score.verdict_v_c(0.10), score.HOLDS)
        self.assertEqual(score.verdict_v_c(0.0999), score.REFUTED)
        self.assertEqual(score.verdict_v_d(0.01, 0.01), score.HOLDS)
        self.assertEqual(score.verdict_v_d(0.01, 0.0), score.REFUTED)
        self.assertEqual(score.verdict_v_d(None, 0.3), score.NO_VERDICT)
        for f in (score.verdict_v_b, score.verdict_v_c):
            self.assertEqual(f(None), score.NO_VERDICT)

    def test_the_net_is_composed_exactly_of_the_two_cells(self):
        rng = random.Random(7)
        qs = "ABC"
        es = [entry([rng.choice(qs) for _ in "12"], [rng.choice(qs) for _ in "12"],
                    y=rng.choice(qs), p=rng.choice(qs)) for _ in range(500)]
        per_run = [{"run": 1}]
        out = score.decomposition(per_run, {1: es})["run1"]
        self.assertTrue(out["composes_exactly"])

    def test_exchangeable_answers_put_v_c_at_zero_in_expectation(self):
        """If the screen did nothing, an answer with it and a second answer
        without it would be draws of one distribution: §5.5's null."""
        rng = random.Random(11)
        es = []
        for _ in range(40000):
            weights = [rng.random() for _ in range(3)]
            draw = lambda: rng.choices("ABC", weights)[0]   # noqa: E731
            es.append(entry([draw(), draw()], [draw(), draw()], p=rng.choice("ABC")))
        vals = score.values_v_c(es)
        self.assertLess(abs(sum(vals) / len(vals)), 0.02)


def fake_checks(passes: bool = True) -> sample.Checks:
    ok = {"passes": passes, "first_problems": []}
    return sample.Checks(vg1={**ok, "suite": {"ran": False}, "fidelity_checks": {}},
                         vg2={**ok, "prompts": {}, "tickets_asked_by_F_f": 0},
                         vg3={**ok, "per_run": {}, "tickets": 0,
                              "tickets_asked_by_F_f": 0},
                         vg4=dict(UNSIGNED), design=None)


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):
    """The signature comes first, in every writer: before the checks, the
    destination or the client."""

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(sample, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "OpenRouterProposer2",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        for s in plan.SESSIONS:
            with self.subTest(s):
                self.refuses(ask.main, ["--session", s])

    def test_the_free_writers_refuse_too(self):
        self.refuses(sample.main, [])
        self.refuses(score.main, [])

    def test_the_dry_run_builds_no_client_needs_no_key_and_writes_nothing(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(sample, "run_checks", return_value=fake_checks()), \
             mock.patch.object(sample, "report"), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(ask, "OpenRouterProposer2",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            self.assertEqual(ask.main(["--dry-run"]), 0)
            self.assertEqual(sample.main(["--dry-run"]), 0)
            self.assertEqual(score.main(["--dry-run"]), 0)
        fetch.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(sample, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(sample, "report"), mock.patch("builtins.print"):
            self.assertEqual(ask.main(["--dry-run"]), 1)
            self.assertEqual(sample.main(["--dry-run"]), 1)
            self.assertEqual(score.main(["--dry-run"]), 1)


def smoke_record(kinds=(prompts.TICKET_ONLY, prompts.HIDDEN), **over) -> dict:
    rec = {**ask.protocol(), "rows": [{"kind": k, "valid": True} for k in kinds]}
    rec.update(over)
    return rec


class TestTheSessionsWaitForASmokeRunThatWorked(unittest.TestCase):

    def check(self, rec: dict | None, kinds) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "smoke.json"
            if rec is not None:
                p.write_text(json.dumps(rec))
            return ask.smoke_check(set(kinds), p)

    def test_no_smoke_record_no_session(self):
        self.assertFalse(self.check(None, {prompts.HIDDEN})[0])

    def test_a_smoke_run_under_another_protocol(self):
        self.assertFalse(self.check(smoke_record(model="another/model"),
                                    {prompts.HIDDEN})[0])
        self.assertFalse(self.check(smoke_record(plan="PLAN_FIDELITY.md"),
                                    {prompts.HIDDEN})[0])
        rec = smoke_record()
        del rec["reasoning"]
        self.assertFalse(self.check(rec, {prompts.HIDDEN})[0])

    def test_a_smoke_run_without_a_valid_answer_of_the_kind(self):
        ok, why = self.check(smoke_record(kinds=(prompts.HIDDEN,)), {prompts.TICKET_ONLY})
        self.assertFalse(ok)
        self.assertIn(prompts.TICKET_ONLY, why)

    def test_a_smoke_run_that_worked(self):
        self.assertTrue(self.check(smoke_record(), ask.KINDS["smoke"])[0])

    def test_a_session_refuses_before_the_key_the_checks_or_the_client(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(plan, "OUT", Path(d)), \
                 mock.patch("reuse.run.fetch_key_info",
                            side_effect=AssertionError("asked")) as fetch, \
                 mock.patch.object(sample, "run_checks",
                                   side_effect=AssertionError("checks ran")) as checks, \
                 mock.patch.object(ask, "OpenRouterProposer2",
                                   side_effect=AssertionError("client built")) as client:
                with self.assertRaises(SystemExit):
                    ask.main(["--session", "anchor"])
        fetch.assert_not_called()
        checks.assert_not_called()
        client.assert_not_called()


class TestTheKeyIsCheckedBeforeAnythingIsCalled(unittest.TestCase):
    """Step 4 of §8, `reuse.run.key_check` called and not copied. **No test here
    reaches the network**: the endpoint is always replaced."""

    def refused(self, argv: list[str], smoke: dict | None) -> None:
        with tempfile.TemporaryDirectory() as d:
            if smoke is not None:
                (Path(d) / "ask_smoke.json").write_text(json.dumps(smoke))
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(plan, "OUT", Path(d)), \
                 mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}), \
                 mock.patch("reuse.run.fetch_key_info", return_value=MANAGEMENT_KEY), \
                 mock.patch.object(sample, "run_checks",
                                   side_effect=AssertionError("checks ran")) as checks, \
                 mock.patch.object(ask, "OpenRouterProposer2",
                                   side_effect=AssertionError("client built")) as client, \
                 mock.patch("builtins.print"):
                with self.assertRaises(SystemExit):
                    ask.main(argv)
        checks.assert_not_called()
        client.assert_not_called()

    def test_the_smoke_run_refuses_a_management_key(self):
        self.refused(["--session", "smoke"], None)

    def test_a_session_refuses_one_even_after_a_smoke_run_that_worked(self):
        self.refused(["--session", "ticket_only"], smoke_record())


class TestASessionThroughTheSDKDouble(unittest.TestCase):
    """Stage B's calls end to end, with the SDK double one rung below the
    proposer. Partial records go to a temporary directory."""

    @classmethod
    def setUpClass(cls):
        cls.design = real_checks().design

    def proposer(self, script):
        from rung2.proposers2 import OpenRouterProposer2
        client = FakeOpenAIClient(script)
        with fake_sdk(openai=client):
            p = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                    reasoning=plan.REASONING)
        return p, ask.wrap(p), client

    def run_smoke(self, script, partial: Path, header=None):
        p, rec, client = self.proposer(script)
        with mock.patch("builtins.print"):
            rows, resumed = ask.ask("smoke", self.design, p, rec, partial,
                                    header or {"protocol": ask.protocol()})
        return rows, resumed, client

    def test_every_request_is_the_prompt_under_the_signed_setting(self):
        with tempfile.TemporaryDirectory() as d:
            rows, _, client = self.run_smoke(FixedResponses(GOOD), Path(d) / "s.jsonl")
        ids = self.design.sessions["smoke"]["passes"][0]
        self.assertEqual([r["id"] for r in rows], ids)
        for kwargs, iid in zip(client.peticiones, ids):
            p = self.design.prompts[iid]
            self.assertEqual(kwargs["messages"][1]["content"], p.user)
            self.assertEqual(kwargs["extra_body"], {"reasoning": plan.REASONING})
            self.assertEqual(kwargs["temperature"], ask.TEMPERATURE)
            self.assertEqual(kwargs["max_tokens"], ask.MAX_TOKENS)
            self.assertEqual(kwargs["model"], plan.MODEL)
        for r in rows:
            self.assertTrue(r["valid"])
            self.assertEqual((r["attempts"], r["finish_reasons"]), (1, [None]))

    def test_the_labels_are_copied_from_the_records(self):
        with tempfile.TemporaryDirectory() as d:
            rows, _, _ = self.run_smoke(FixedResponses(GOOD), Path(d) / "s.jsonl")
        runs = self.design.fidelity.runs
        for r in rows:
            if r["kind"] == prompts.HIDDEN:
                row = runs[r["run"]]["records"][r["idx"]]
                self.assertEqual(r["labels"]["rule_action"], row["predicted"])
                self.assertEqual(r["labels"]["truth"], row["truth"])
            else:
                self.assertEqual(r["labels"]["truth"],
                                 runs[1]["records"][r["idx"]]["truth"])

    def test_a_resumed_session_asks_nothing_twice(self):
        with tempfile.TemporaryDirectory() as d:
            partial = Path(d) / "s.jsonl"
            full, _, _ = self.run_smoke(FixedResponses(GOOD), partial)
            lines = partial.read_text().splitlines()
            partial.write_text("\n".join(lines[:7]) + "\n" + lines[7][:20])
            rows, resumed, client = self.run_smoke(FixedResponses(GOOD), partial)
        self.assertEqual(len(client.peticiones), len(full) - 6)
        self.assertEqual(len(resumed), 1)
        self.assertEqual([r["id"] for r in rows], [r["id"] for r in full])

    def test_an_outage_stops_the_session_and_records_none_of_it(self):
        with tempfile.TemporaryDirectory() as d:
            partial = Path(d) / "s.jsonl"
            with self.assertRaises(ask.Outage):
                self.run_smoke(FixedResponses(""), partial)
            self.assertEqual(len(partial.read_text().splitlines()), 1)

    def test_an_isolated_failure_is_an_answer_and_is_recorded(self):
        texts = ["", "", ""] + [GOOD] * 40
        with tempfile.TemporaryDirectory() as d:
            rows, _, _ = self.run_smoke(FixedResponses(*texts), Path(d) / "s.jsonl")
        failed = [r for r in rows if r["failure"]]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["attempts"], 3)
        self.assertFalse(failed[0]["valid"])

    def test_stage_b_builds_the_proposer_with_the_signed_setting(self):
        source = Path("screen/ask.py").read_text()
        self.assertIn("reasoning=plan.REASONING", source)
        self.assertIn("recorder = wrap(proposer)", source)


def masked(real):
    """`score.held_out_entries` with every held-out label replaced by one queue,
    so that Stage C runs its whole path without computing a single figure of the
    held-out decisions' labels before the signature."""
    def entries(*args, **kwargs):
        out = real(*args, **kwargs)
        for es in out.values():
            for e in es:
                if e["y"] is not None:
                    e["y"] = "T1_GENERAL"
        return out
    return entries


class TestStageCOverRecordsTheDoubleProduced(unittest.TestCase):
    """`screen/score.py` end to end, in a temporary directory. Stage A's record
    is written by `sample.payload` with its readout stubbed, and Stage C reads
    the held-out decisions with their labels masked, so that no figure of them
    exists. Both paid sessions are asked through the SDK double, which answers
    `T2_TECHNICAL` to everything, so no verdict here means anything. What is
    checked is the path."""

    @classmethod
    def setUpClass(cls):
        from rung2.proposers2 import OpenRouterProposer2
        cls.checks = real_checks()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.patches = [mock.patch.object(plan, "OUT", cls.out),
                       mock.patch.object(plan, "SAMPLE_PATH", cls.out / "sample.json"),
                       mock.patch.object(plan, "SCORE_PATH", cls.out / "score.json")]
        for p in cls.patches:
            p.start()
        with mock.patch.object(sample, "readout", return_value={"stub": True}):
            plan.SAMPLE_PATH.write_text(json.dumps(sample.payload(cls.checks)))
        digest = ask.sample_sha256()
        for s in ("anchor", "ticket_only"):
            client = FakeOpenAIClient(FixedResponses(GOOD))
            with fake_sdk(openai=client):
                prop = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                           reasoning=plan.REASONING)
            rec = ask.wrap(prop)
            with mock.patch("builtins.print"):
                rows, resumed = ask.ask(s, cls.checks.design, prop, rec,
                                        plan.partial_path(s), {"protocol": ask.protocol()})
            plan.ask_path(s).write_text(json.dumps(
                ask.record(s, prop, rows, resumed, "start", cls.checks, digest)))
        cls.mask = mock.patch.object(score, "held_out_entries",
                                     side_effect=masked(score.held_out_entries))
        cls.mask.start()
        with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch.object(sample, "run_checks", return_value=cls.checks), \
             mock.patch("builtins.print"):
            cls.code = score.main([])
        cls.record = json.loads(plan.SCORE_PATH.read_text())

    @classmethod
    def tearDownClass(cls):
        cls.mask.stop()
        for p in cls.patches:
            p.stop()
        cls.tmp.cleanup()

    def test_it_scores_every_row_and_writes_its_record(self):
        self.assertEqual(self.code, 0)
        self.assertEqual(set(self.record["verdicts"]), {"V-a", "V-b", "V-c", "V-d"})
        self.assertEqual(len(self.record["runs"]), 3)
        for r in self.record["runs"]:
            self.assertEqual(r["population"]["held_out"], plan.HELD_OUT_SIZES[r["run"]])

    def test_its_record_carries_the_protocol_it_scored(self):
        for k, v in ask.protocol().items():
            self.assertEqual(self.record[k], v)
        self.assertEqual(self.record["stage"], "C")

    def test_the_arithmetic_on_answers_that_never_vary(self):
        """Every answer without a screen is T2_TECHNICAL: two of them always
        agree, and none ever lands on a plurality that is not T2_TECHNICAL, so
        no decision in V-c can count against the screen."""
        self.assertEqual(self.record["verdicts"]["V-a"]["ticket_only"]["S"], 1.0)
        for r in self.record["runs"]:
            if r["rows"]["V-c"] is not None:
                self.assertGreaterEqual(r["rows"]["V-c"], 0.0)
        self.assertTrue(all(v["composes_exactly"] for v in
                            self.record["V-e"]["decomposition"].values()))

    def test_a_record_under_another_protocol_is_refused(self):
        path = plan.ask_path("anchor")
        kept = path.read_text()
        try:
            path.write_text(json.dumps({**json.loads(kept), "model": "another/model"}))
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(sample, "run_checks", return_value=self.checks), \
                 mock.patch("builtins.print"):
                with self.assertRaises(SystemExit):
                    score.main([])
        finally:
            path.write_text(kept)


if __name__ == "__main__":
    unittest.main()
