"""
PLAN_FIDELITY.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §10 and the five band lines of §0, so that moving one after
    a figure exists is visible in a diff.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `fidelity/ask.py` exits before it builds the client.
  * `F-g2`: the replay reproduces the three Stage B records and fails without
    their edges.
  * `F-g3`: the prompts. Above all, every birth prompt rebuilt here is the
    request rung 2's loop actually built. That is checked on the four v1 n=100
    records, which `tests/doubles.py` replays with the loop itself.
  * The draw and the sessions on the real records.
  * Stage C's arithmetic on items small enough to check by hand.
  * Stage B end to end through the SDK double, including resuming and stopping
    on an outage.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double or something that fails the test if it is ever built. No figure of
any row is computed for display. The checks on real inputs are silent when
they pass.
"""

from __future__ import annotations

import inspect
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import generate_corpus
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import render_base_v1
from rung2.shadow2 import run_shadow2

from fidelity import ask, plan, prompts, replay, sample, score
from reuse import plan as reuse_plan
from tests.doubles import FakeOpenAIClient, FixedResponses, fake_sdk, record, script_rung2
from tests.fixtures import space

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {**UNSIGNED, "passes": True, "unsigned": 0}
GOOD = ('{"action": "T2_TECHNICAL", "conditions": '
        '[{"attr": "severity", "op": "lte", "value": 2}], "beats": [], '
        '"loses_to": [], "note": "x"}')


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_protocol_of_section_10(self):
        self.assertEqual((plan.N, plan.SEED, plan.RUNS), (2000, 17, (1, 2, 3)))
        self.assertEqual(plan.MODEL, "deepseek/deepseek-v4-flash")
        self.assertEqual(plan.PROMPT, "v1")
        self.assertEqual(plan.REASONING, {"effort": "none"})
        self.assertEqual((plan.DRAWS, plan.PER_RUN, plan.TICKET_ONLY_PER_RUN,
                          plan.SMOKE_PER_ARM), (2, 600, 100, 5))
        self.assertEqual((plan.SAMPLE_SEED, plan.ORDER_SEED), (41, 43))
        self.assertEqual((plan.MAX_INVALID_SHARE, plan.MIN_SILENT_ERRORS), (0.05, 100))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_five_lines_of_section_0(self):
        self.assertEqual(plan.F_A_MAX_GAP, 0.05)
        self.assertEqual(plan.F_B_MIN_GAP, 0.10)
        self.assertEqual(plan.F_C_REFUTED_AT_OR_BELOW, 0.0)
        self.assertEqual(plan.F_D_MIN_SHARE, 0.60)
        self.assertEqual(plan.F_E_MIN_ONCALL, 1)

    def test_the_breaker_fixed_before_any_call(self):
        self.assertEqual(ask.STOP_AFTER_FAILURES_IN_A_ROW, 5)

    def test_the_inputs_are_the_three_stage_b_records(self):
        for k in plan.RUNS:
            self.assertEqual(plan.run_path(k), Path(f"results_reuse/run_n2000_r{k}.json"))
            self.assertTrue(plan.run_path(k).is_file())

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_FIDELITY.md"))
        self.assertTrue(plan.PLAN.is_file())
        self.assertGreaterEqual(plan.gate_signature()["found"], 1)

    def test_one_stream_per_run_and_per_pass(self):
        draws = [plan.sample_rng(k).random() for k in plan.RUNS]
        self.assertEqual(draws, [plan.sample_rng(k).random() for k in plan.RUNS])
        self.assertEqual(len(set(draws)), 3)
        orders = {(s, p): plan.order_rng(s, p).random()
                  for s in plan.SESSIONS for p in (1, 2)}
        self.assertEqual(len(set(orders.values())), len(orders))

    def test_the_session_names(self):
        self.assertEqual(plan.SESSIONS, ("smoke", "births", "base1", "base2",
                                         "base3", "ticket_only"))
        with self.assertRaises(ValueError):
            plan.ask_path("base4")


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None, gate=plan.gate_signature) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return gate(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_no_signature_line_no_pass(self):
        self.assertFalse(self.gate("# a plan\n")["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ________________________ (date: ______________)**\n"
        )["passes"])

    def test_one_signed_line_passes_this_plan(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-02)**\n")["passes"])

    def test_and_still_not_plan_reuse(self):
        """The minimum is an argument now, and PLAN_REUSE.md's default did not
        move: one line is still its §0 without its amendment."""
        line = "**Signed by Sergi: Sergi Parpal (date: 2026-10-02)**\n"
        self.assertFalse(self.gate(line, reuse_plan.gate_signature)["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-02)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


class TestTheReplay(unittest.TestCase):
    """`F-g2` on the three Stage B records. Silent when it passes."""

    @classmethod
    def setUpClass(cls):
        cls.corpus = generate_corpus(plan.N, seed=plan.SEED)
        cls.runs = sample.load_runs()

    def test_each_run_rebuilds_exactly(self):
        for k, rec in self.runs.items():
            with self.subTest(run=k):
                c = replay.check(rec, self.corpus, space())
                self.assertEqual(c["first_problems"], [])
                self.assertTrue(c["passes"])

    def test_without_its_edges_each_run_departs(self):
        """The check has teeth: every run accepted edges, and the record says
        what they decided."""
        for k, rec in self.runs.items():
            with self.subTest(run=k):
                c = replay.check(rec, self.corpus, space(), with_edges=False)
                self.assertFalse(c["passes"])
                self.assertGreater(c["decisions_departing"], 0)

    def test_a_tampered_record_is_caught(self):
        rec = json.loads(json.dumps(self.runs[2]))
        i = next(r["idx"] for r in rec["records"] if r["outcome"] == "ACTION")
        rec["records"][i]["winner_id"] = "R9999"
        self.assertFalse(replay.check(rec, self.corpus, space())["passes"])

    def test_another_system_prompt_is_caught(self):
        rec = dict(self.runs[3], system_prompt="otro prompt")
        c = replay.check(rec, self.corpus, space())
        self.assertFalse(c["system_prompt_is_v1"])
        self.assertFalse(c["passes"])


V1_N100 = [p for v, _, p in reuse_plan.EIGHT if v == "v1"]


class TestThePrompts(unittest.TestCase):

    def test_the_birth_prompts_are_the_requests_the_loop_built(self):
        """`F-g3`'s birth half. Rung 2's own loop, driven by the SDK double over
        each v1 n=100 record, builds a request at every escalation; the prompt
        this package rebuilds at the same moment must be that request, byte for
        byte. Only first attempts carry `response_format`."""
        from rung2.proposers2 import OpenRouterProposer2
        for path in V1_N100:
            with self.subTest(record=str(path)):
                reg = record(str(path))
                corpus = generate_corpus(reg["n"], seed=reg["seed"])
                client = FakeOpenAIClient(script_rung2(reg))
                with fake_sdk(openai=client):
                    proposer = OpenRouterProposer2(model=reg["model"],
                                                   prompt_version="v1")
                    run_shadow2(corpus, PriorityEngine(space=space()), proposer)
                sent = [k["messages"][1]["content"] for k in client.peticiones
                        if "response_format" in k]
                rebuilt = [prompts.birth(m.engine, m.case, m.undefeated).user
                           for m in replay.Replay(reg, corpus, space()).moments()
                           if m.outcome != "ACTION" and m.row["escalated"]]
                self.assertEqual(len(sent), reg["metrics"]["escalations"])
                self.assertEqual(sent, rebuilt)

    def test_no_builder_takes_a_label(self):
        allowed = {"engine", "case", "undefeated"}
        for fn in (prompts.birth, prompts.hidden, prompts.ticket_only):
            with self.subTest(fn.__name__):
                self.assertLessEqual(set(inspect.signature(fn).parameters), allowed)

    def test_the_headers_are_v1s_own(self):
        self.assertEqual(prompts.COVERAGE_HEADER,
                         "REGLAS PROXIMAS de la base (ninguna casa este ticket; "
                         "se listan las que menos condiciones incumplen):")
        self.assertEqual(prompts.EMPTY_BASE,
                         "BASE DE REGLAS: vacia. Esta es la primera regla.\n")

    def test_a_ticket_only_prompt_is_the_empty_base(self):
        case = generate_corpus(1, seed=17)[0]
        p = prompts.ticket_only(case)
        self.assertEqual(p.base_text, render_base_v1([], "vecindario"))
        self.assertEqual(prompts.check_ticket_only(p), [])

    def test_a_b_screen_on_real_moments(self):
        """Every decided case of run 2: no matching rule and not the deciding one
        on the screen, under v1's coverage header."""
        rec = json.loads(plan.run_path(2).read_text())
        corpus = generate_corpus(plan.N, seed=plan.SEED)
        n = 0
        for m in replay.Replay(rec, corpus, space()).moments():
            if m.outcome == "ACTION":
                p = prompts.hidden(m.engine, m.case)
                self.assertEqual(prompts.check_hidden(p, m.engine, m.winner.rule_id), [])
                n += 1
        self.assertGreater(n, 0)

    def test_check_hidden_catches_a_screen_showing_the_deciding_rule(self):
        rec = json.loads(plan.run_path(1).read_text())
        corpus = generate_corpus(plan.N, seed=plan.SEED)
        m = next(m for m in replay.Replay(rec, corpus, space()).moments()
                 if m.outcome == "ACTION")
        p = prompts.birth(m.engine, m.case, [])        # design A: nothing hidden
        problems = prompts.check_hidden(p, m.engine, m.winner.rule_id)
        self.assertIn("the deciding rule is on the screen", problems)
        self.assertIn("a rule on the screen matches the ticket", problems)

    def test_the_baselines_and_their_tie_break(self):
        case = generate_corpus(1, seed=17)[0]
        p = prompts.Prompt(kind=prompts.HIDDEN, case=case, screen="vecindario",
                           shown_ids=("R1", "R2", "R3", "R4"),
                           shown_actions=("A", "B", "B", "A"), base_text="")
        self.assertEqual(prompts.plurality(p), "A")      # a tie: shown first
        self.assertEqual(prompts.first_shown(p), "A")
        p.shown_actions = ("C", "B", "B", "A")
        self.assertEqual(prompts.plurality(p), "B")
        p.shown_actions = ()
        self.assertIsNone(prompts.plurality(p))


class TestTheDraw(unittest.TestCase):
    """Stage A's checks and design on the real records, without the suite."""

    @classmethod
    def setUpClass(cls):
        cls.checks = sample.run_checks(suite=False)
        cls.d = cls.checks.design

    def test_the_blocking_checks_pass(self):
        self.assertEqual({k: r["problems"] for k, r in self.checks.fg1["records"].items()},
                         {f"run{k}": [] for k in plan.RUNS})
        self.assertTrue(self.checks.fg2["passes"])
        self.assertEqual(self.checks.fg3["first_problems"], [])
        self.assertTrue(self.checks.fg3["passes"])
        self.assertTrue(self.checks.fg3["F-d_population"]["F-d_adjudicable"])

    def test_the_draw_is_deterministic(self):
        again = sample.build_design(self.d.runs, self.d.corpus, self.d.space)
        self.assertEqual(again.draw, self.d.draw)
        self.assertEqual(again.sessions, self.d.sessions)
        self.assertEqual({i: it["digest"] for i, it in again.items.items()},
                         {i: it["digest"] for i, it in self.d.items.items()})

    def test_six_hundred_distinct_decided_cases_per_run(self):
        for k in plan.RUNS:
            uniform = self.d.draw[k]["uniform"]
            rows = self.d.runs[k]["records"]
            self.assertEqual(len(set(uniform)), plan.PER_RUN)
            self.assertTrue(all(rows[i]["outcome"] == "ACTION" for i in uniform))
        self.assertNotEqual(self.d.draw[1]["uniform"], self.d.draw[2]["uniform"])

    def test_every_session_and_its_passes(self):
        s = self.d.sessions
        self.assertEqual(len(s["births"]["items"]),
                         sum(r["metrics"]["escalations"] for r in self.d.runs.values()))
        for name in ("births", "base1", "base2", "base3"):
            with self.subTest(name):
                one, two = s[name]["passes"]
                self.assertEqual(sorted(one), sorted(s[name]["items"]))
                self.assertEqual(sorted(two), sorted(s[name]["items"]))
                self.assertNotEqual(one, two)
        one, two = s["ticket_only"]["passes"]
        self.assertEqual(sorted(one), sorted(s["ticket_only"]["items"]))
        self.assertEqual(len(two), 27)            # 20 SECURITY and 7 ONCALL tickets
        self.assertTrue(all(self.d.items[i]["rare"] for i in two))

    def test_the_census(self):
        for k in plan.RUNS:
            items = [self.d.items[i] for i in self.d.sessions[f"base{k}"]["items"]]
            oncall = [it for it in items if it["census"] == plan.ONCALL]
            self.assertEqual(len(oncall), 7)
            self.assertTrue(all(it["kind"] == prompts.HIDDEN for it in items))

    def test_the_smoke_run(self):
        ids = self.d.sessions["smoke"]["items"]
        kinds = [self.d.items[i]["kind"] for i in ids]
        for kind in prompts.KINDS:
            self.assertEqual(kinds.count(kind), plan.SMOKE_PER_ARM)
        self.assertTrue(any(self.d.items[i]["kind"] == prompts.BIRTH
                            and self.d.items[i]["screen"] == prompts.CONFLICT
                            for i in ids))
        self.assertEqual(len(self.d.sessions["smoke"]["passes"]), 1)

    def test_every_item_carries_the_digest_of_its_prompt(self):
        for i, it in self.d.items.items():
            self.assertEqual(it["digest"], self.d.prompts[i].digest)


def entry(a1, a2, *, r="A", y="A", rule="R1", uniform=True, census=None, idx=0):
    labels = {"truth": y, "rule_action": r, "rule_id": rule, "uniform": uniform,
              "census": census}
    return {"id": f"d1:{idx}", "kind": prompts.HIDDEN, "run": 1, "idx": idx,
            "labels": labels, "answers": {1: a1, 2: a2}, "payloads": {}}


class TestTheArithmetic(unittest.TestCase):
    """Stage C's statistics on items small enough to check by hand."""

    def test_group_and_validity(self):
        rows = [{"id": "x", "kind": "hidden", "run": 1, "idx": 0, "labels": {},
                 "pass": p, "action": a, "valid": v, "payload": None}
                for p, a, v in ((1, "A", True), (2, "Z", False))]
        g = score.group(rows)
        self.assertEqual(g["x"]["answers"], {1: "A", 2: None})
        self.assertIsNone(score.valid_pair(g["x"]))

    def test_agreement_gap(self):
        es = [entry("A", "A", r="A"), entry("B", "B", r="A"), entry("A", "B", r="A")]
        g = score.agreement_gap(es, lambda e: e["labels"]["rule_action"])
        self.assertAlmostEqual(g["S"], 2 / 3)
        self.assertAlmostEqual(g["A"], (1 + 0 + 0.5) / 3)
        self.assertAlmostEqual(g["gap"], 2 / 3 - 0.5)

    def test_exchangeable_answers_put_the_gap_at_zero_in_expectation(self):
        """§2.2's null, enumerated exactly: r, a₁, a₂ independent draws of one
        distribution over three queues."""
        p = {"A": 0.6, "B": 0.3, "C": 0.1}
        es, w = [], []
        for r in p:
            for a1 in p:
                for a2 in p:
                    es.append(entry(a1, a2, r=r))
                    w.append(p[r] * p[a1] * p[a2])
        d = score.agreement_gap(es, lambda e: e["labels"]["rule_action"])["values"]
        self.assertAlmostEqual(sum(x * y for x, y in zip(d, w)), 0.0)

    def test_accuracy_difference_and_own_error_share(self):
        es = [entry("A", "A", r="B", y="A"),   # loss: model right, rule wrong
              entry("B", "B", r="A", y="A"),   # gain: rule right, model wrong
              entry("C", "A", r="B", y="A"),   # rule wrong, model right once
              entry("A", "A", r="A", y="A")]   # both right
        c = score.accuracy_difference(es)
        self.assertAlmostEqual(c["model_accuracy"], (1 + 0 + 0.5 + 1) / 4)
        self.assertAlmostEqual(c["rule_accuracy"], 2 / 4)
        self.assertAlmostEqual(c["difference"], 0.625 - 0.5)
        d = score.own_error_share(es)
        self.assertEqual(d["n"], 2)                    # the rule's two errors
        self.assertAlmostEqual(d["share"], (0 + 0.5) / 2)

    def test_the_four_cells_add_up(self):
        es = [entry("A", "A", r="B", y="A"), entry("B", "C", r="B", y="A")]
        c = score.cells(es)
        self.assertEqual((c["loss"], c["both_wrong_same_queue"],
                          c["both_wrong_other_queues"]), (2, 1, 1))
        self.assertEqual(c["answers"], 4)

    def test_oncall_needs_both_answers(self):
        o = plan.ONCALL
        es = [entry(o, o, census=o), entry(o, "T1_GENERAL", census=o),
              entry(o, None, census=o)]
        self.assertEqual(score.oncall_named(es),
                         {"tickets": 3, "named_by_both": 1, "lacking_a_valid_pair": 1})

    def test_alarm_and_proxy(self):
        es = [entry("B", "B", r="A", y="B", rule="R1"),   # disagree, rule wrong
              entry("A", "A", r="A", y="A", rule="R2")]   # agree, rule right
        a = score.alarm(es)
        self.assertEqual((a["rule_wrong_where_disagreeing"],
                          a["rule_wrong_where_agreeing"]), (1.0, 0.0))
        p = score.proxy_concordance(es, lambda e: e["labels"]["rule_id"] == "R1")
        self.assertEqual((p["answers_on_rule_errors"], p["concordant"]), (2, 0))

    def test_standard_error_and_its_correction(self):
        vals = [0.0, 1.0, 0.0, 1.0]
        plain = score.standard_error(vals)
        self.assertAlmostEqual(plain, (1 / 3) ** 0.5 / 2)
        self.assertAlmostEqual(score.standard_error(vals, 8), plain * 0.5 ** 0.5)
        self.assertIsNone(score.standard_error([1.0]))

    def test_thin(self):
        self.assertTrue(score.thin(0.11, 0.10, 0.02))
        self.assertFalse(score.thin(0.15, 0.10, 0.02))
        self.assertIsNone(score.thin(None, 0.10, 0.02))

    def test_a_run_with_too_many_invalid_pairs_has_no_value(self):
        rec = {"records": [{"idx": i, "outcome": "ACTION", "correct": True}
                           for i in range(20)],
               "rules": [{"rule_id": "R1", "born_at": 99}]}
        rows = []
        for i in range(20):
            for p in (1, 2):
                bad = i == 0 and p == 2               # one item of twenty: 5%
                rows.append({"id": f"d1:{i}", "kind": "hidden", "run": 1, "idx": i,
                             "pass": p, "action": None if bad else "A",
                             "valid": not bad, "payload": None, "failure": None,
                             "seconds": 1.0, "labels": {
                                 "truth": "A", "rule_action": "A", "rule_id": "R1",
                                 "uniform": True, "census": None}})
        with mock.patch.object(score, "births",
                               return_value=({"R1": {"proposal_action_correct": True}}, [])):
            ok = score.score_run(1, rows, rec, generate_corpus(20, seed=17))
            self.assertTrue(ok["validity"]["defined"])
            rows[3]["valid"] = False                  # a second item: 10%
            rows[3]["action"] = None
            bad = score.score_run(1, rows, rec, generate_corpus(20, seed=17))
        self.assertFalse(bad["validity"]["defined"])
        self.assertIsNone(bad["rows"]["F-b"])

    def test_the_median_and_its_standard_error(self):
        runs = [{"rows": {"F-c": v}, "standard_errors": {"F-c": se}}
                for v, se in ((0.01, 0.02), (0.05, 0.01), (None, None))]
        m = score.median_row(runs, "F-c")
        self.assertAlmostEqual(m["median"], 0.03)
        self.assertEqual(m["verdict"], "holds")


class TestTheVerdictsAtTheirEdges(unittest.TestCase):
    """Each band's edge is its own refutation line (§0)."""

    def test_f_a(self):
        self.assertEqual(score.verdict_f_a(0.05), "holds")
        self.assertEqual(score.verdict_f_a(0.0501), "refuted")

    def test_f_b(self):
        self.assertEqual(score.verdict_f_b(0.10), "holds")
        self.assertEqual(score.verdict_f_b(0.0999), "refuted")

    def test_f_c(self):
        self.assertEqual(score.verdict_f_c(1e-9), "holds")
        self.assertEqual(score.verdict_f_c(0.0), "refuted")

    def test_f_d(self):
        self.assertEqual(score.verdict_f_d(0.60), "holds")
        self.assertEqual(score.verdict_f_d(0.5999), "refuted")

    def test_f_e(self):
        self.assertEqual(score.verdict_f_e(1), "holds")
        self.assertEqual(score.verdict_f_e(0), "refuted")

    def test_no_value_no_verdict(self):
        for fn in score.VERDICTS.values():
            self.assertEqual(fn(None), "unadjudicable")


def fake_checks(passes: bool = True) -> sample.Checks:
    ok = {"passes": passes}
    return sample.Checks(fg1={**ok, "records": {}, "suite": {"ran": False}},
                         fg2={**ok, "runs": {}},
                         fg3={**ok, "prompts": {}, "first_problems": [],
                              "F-d_population": {"F-d_adjudicable": True}},
                         fg4=dict(UNSIGNED), design=None)


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
        fetch.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(sample, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(sample, "report"), mock.patch("builtins.print"):
            self.assertEqual(ask.main(["--dry-run"]), 1)
            self.assertEqual(sample.main(["--dry-run"]), 1)


def smoke_record(kinds=prompts.KINDS, **over) -> dict:
    rec = {**ask.protocol(),
           "rows": [{"kind": k, "valid": True} for k in kinds]}
    rec.update(over)
    return rec


API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
MANAGEMENT_KEY = (200, {"data": {"is_management_key": True}})


class TestTheSessionsWaitForASmokeRunThatWorked(unittest.TestCase):

    def check(self, rec: dict | None, kinds) -> tuple[bool, str]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "smoke.json"
            if rec is not None:
                p.write_text(json.dumps(rec))
            return ask.smoke_check(set(kinds), p)

    def test_no_smoke_record_no_session(self):
        self.assertFalse(self.check(None, {"birth"})[0])

    def test_a_smoke_run_under_another_protocol(self):
        self.assertFalse(self.check(smoke_record(model="another/model"), {"birth"})[0])
        self.assertFalse(self.check(smoke_record(reasoning=None), {"birth"})[0])
        rec = smoke_record()
        del rec["reasoning"]
        self.assertFalse(self.check(rec, {"birth"})[0])

    def test_a_smoke_run_without_a_valid_answer_of_the_kind(self):
        ok, why = self.check(smoke_record(kinds=("birth",)), {"hidden"})
        self.assertFalse(ok)
        self.assertIn("hidden", why)
        rec = smoke_record()
        for r in rec["rows"]:
            r["valid"] = False
        self.assertFalse(self.check(rec, {"birth"})[0])

    def test_a_smoke_run_that_worked(self):
        self.assertTrue(self.check(smoke_record(), prompts.KINDS)[0])

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
                    ask.main(["--session", "births"])
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
        self.refused(["--session", "base1"], smoke_record())


class TestASessionThroughTheSDKDouble(unittest.TestCase):
    """Stage B's calls end to end, with the SDK double one rung below the
    proposer: the request it builds, the record rows, resuming, and stopping on
    an outage. Partial records go to a temporary directory."""

    @classmethod
    def setUpClass(cls):
        cls.design = sample.run_checks(suite=False).design

    def proposer(self, script):
        from rung2.proposers2 import OpenRouterProposer2
        client = FakeOpenAIClient(script)
        with fake_sdk(openai=client):
            p = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                    reasoning=plan.REASONING)
        return p, client

    def run_smoke(self, script, partial: Path, header=None):
        p, client = self.proposer(script)
        with mock.patch("builtins.print"):
            rows, resumed = ask.ask("smoke", self.design, p, partial,
                                    header or {"protocol": ask.protocol()})
        return rows, resumed, client

    def test_every_request_is_the_rebuilt_prompt_under_the_signed_setting(self):
        with tempfile.TemporaryDirectory() as d:
            rows, _, client = self.run_smoke(FixedResponses(GOOD), Path(d) / "s.jsonl")
        ids = self.design.sessions["smoke"]["passes"][0]
        self.assertEqual([r["id"] for r in rows], ids)
        self.assertEqual(len(client.peticiones), len(ids))
        for kwargs, iid in zip(client.peticiones, ids):
            p = self.design.prompts[iid]
            self.assertEqual(kwargs["messages"][1]["content"], p.user)
            self.assertEqual(kwargs["extra_body"], {"reasoning": plan.REASONING})
            self.assertEqual(kwargs["temperature"], ask.TEMPERATURE)
            self.assertEqual(kwargs["max_tokens"], ask.MAX_TOKENS)
            self.assertEqual(kwargs["model"], plan.MODEL)
        self.assertTrue(all(r["valid"] and r["action"] == "T2_TECHNICAL" for r in rows))

    def test_the_labels_are_copied_from_the_records(self):
        with tempfile.TemporaryDirectory() as d:
            rows, _, _ = self.run_smoke(FixedResponses(GOOD), Path(d) / "s.jsonl")
        for r in rows:
            if r["kind"] == prompts.HIDDEN:
                row = self.design.runs[r["run"]]["records"][r["idx"]]
                self.assertEqual(r["labels"]["rule_action"], row["predicted"])
                self.assertEqual(r["labels"]["truth"], row["truth"])
            if r["kind"] == prompts.BIRTH:
                row = self.design.runs[r["run"]]["records"][r["idx"]]
                self.assertEqual(r["labels"]["recorded_answer"], row["predicted"])

    def test_a_resumed_session_asks_nothing_twice(self):
        with tempfile.TemporaryDirectory() as d:
            partial = Path(d) / "s.jsonl"
            full, _, _ = self.run_smoke(FixedResponses(GOOD), partial)
            lines = partial.read_text().splitlines()
            partial.write_text("\n".join(lines[:7]) + "\n" + lines[7][:20])  # cut mid-line
            rows, resumed, client = self.run_smoke(FixedResponses(GOOD), partial)
            after = partial.read_text().splitlines()
        # The cut line is gone, so a second interruption could not bury what
        # followed it: every line parses, the header and every answer once.
        self.assertEqual(len(after), 1 + len(full))
        for line in after:
            json.loads(line)
        self.assertEqual(len(client.peticiones), len(full) - 6)
        self.assertEqual(len(resumed), 1)
        self.assertEqual([r["id"] for r in rows], [r["id"] for r in full])

    def test_a_partial_record_under_another_protocol_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            partial = Path(d) / "s.jsonl"
            partial.write_text(json.dumps({"protocol": "another"}) + "\n")
            p, _ = self.proposer(FixedResponses(GOOD))
            with self.assertRaises(SystemExit):
                ask.ask("smoke", self.design, p, partial, {"protocol": ask.protocol()})

    def test_an_outage_stops_the_session_and_records_none_of_it(self):
        with tempfile.TemporaryDirectory() as d:
            partial = Path(d) / "s.jsonl"
            with self.assertRaises(ask.Outage):
                self.run_smoke(FixedResponses(""), partial)
            lines = partial.read_text().splitlines()
        self.assertEqual(len(lines), 1)                   # the header alone

    def test_an_isolated_failure_is_an_answer_and_is_recorded(self):
        texts = ["", "", ""] + [GOOD] * 40                # three tries, then good
        with tempfile.TemporaryDirectory() as d:
            rows, _, _ = self.run_smoke(FixedResponses(*texts), Path(d) / "s.jsonl")
        self.assertEqual(len(rows), len(self.design.sessions["smoke"]["passes"][0]))
        failed = [r for r in rows if r["failure"]]
        self.assertEqual(len(failed), 1)
        self.assertFalse(failed[0]["valid"])

    def test_stage_b_builds_the_proposer_with_the_signed_setting(self):
        source = Path("fidelity/ask.py").read_text()
        self.assertIn("reasoning=plan.REASONING", source)
        self.assertIn("**protocol()", source)


class TestStageCOverRecordsTheDoubleProduced(unittest.TestCase):
    """`fidelity/score.py` end to end, in a temporary directory. Stage A's
    record is written by `sample.payload`. Every session is asked through the
    SDK double, which answers `T2_TECHNICAL` to everything, so no verdict here
    means anything. What is checked is the path: the records are read, checked
    against the protocol and Stage A's digest, scored and written."""

    @classmethod
    def setUpClass(cls):
        from rung2.proposers2 import OpenRouterProposer2
        cls.checks = sample.run_checks(suite=False)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.patches = [mock.patch.object(plan, "OUT", cls.out),
                       mock.patch.object(plan, "SAMPLE_PATH", cls.out / "sample.json"),
                       mock.patch.object(plan, "SCORE_PATH", cls.out / "score.json")]
        for p in cls.patches:
            p.start()
        plan.SAMPLE_PATH.write_text(json.dumps(sample.payload(cls.checks), indent=2))
        digest = ask.sample_sha256()
        for s in ("births", "base1", "base2", "base3", "ticket_only"):
            client = FakeOpenAIClient(FixedResponses(GOOD))
            with fake_sdk(openai=client):
                proposer = OpenRouterProposer2(model=plan.MODEL,
                                               prompt_version=plan.PROMPT,
                                               reasoning=plan.REASONING)
            with mock.patch("builtins.print"):
                rows, _ = ask.ask(s, cls.checks.design, proposer, plan.partial_path(s),
                                  {"protocol": ask.protocol()})
            plan.ask_path(s).write_text(json.dumps(
                {**ask.protocol(), "sample_sha256": digest, "rows": rows}))
        with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch.object(sample, "run_checks", return_value=cls.checks), \
             mock.patch.object(sample, "report"), mock.patch("builtins.print"):
            cls.exit = score.main([])
        cls.score = json.loads(plan.SCORE_PATH.read_text())

    @classmethod
    def tearDownClass(cls):
        for p in cls.patches:
            p.stop()
        cls.tmp.cleanup()

    def test_it_scores_every_row_and_writes_its_record(self):
        self.assertEqual(self.exit, 0)
        self.assertEqual(set(self.score["verdicts"]), {"F-a", "F-b", "F-c", "F-d", "F-e"})
        self.assertEqual(self.score["sample_sha256"], ask.sample_sha256())
        self.assertIsNotNone(self.score["F-f"]["ticket_only"])

    def test_the_arithmetic_on_answers_that_never_vary(self):
        """Every answer is T2_TECHNICAL: the two answers always agree, no
        ONCALL ticket is named, and A is the share of rules that send to T2."""
        for run in self.score["runs"]:
            self.assertEqual(run["beside"]["S"], 1.0)
            self.assertEqual(run["rows"]["F-e"], 0)
        self.assertEqual(self.score["verdicts"]["F-e"]["verdict"], "refuted")
        b = self.score["births"]
        self.assertAlmostEqual(b["value"], b["S"] - b["A"])

    def test_a_record_under_another_protocol_is_refused(self):
        path = plan.ask_path("base2")
        original = path.read_text()
        path.write_text(json.dumps({**json.loads(original), "model": "another/model"}))
        try:
            with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
                 mock.patch.object(sample, "run_checks", return_value=self.checks), \
                 mock.patch.object(sample, "report"), mock.patch("builtins.print"):
                with self.assertRaises(SystemExit):
                    score.main([])
        finally:
            path.write_text(original)


if __name__ == "__main__":
    unittest.main()
