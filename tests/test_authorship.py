"""
`PLAN_AUTHORSHIP.md` — the instrument, no figure.

**No figure of the plan is pinned here**: Stage B has not run, and the baseline's
figures belong to `results_reuse/structure.json` and `results_edges/score.json`,
which `E-g2` reproduces in the dry run. What is pinned is what makes the
instrument the one §5 and §10 describe:

  * the constants of §11 and the lines of §0, and the plan's own text for them;
  * v1e is v1 with one paragraph replaced, its texts hash to the declared
    fingerprint, and the order paragraph goes only where a CONFLICT is shown;
  * the validator's pure parts, and the loop on small worlds: a born rule, a
    repair round that places, one that does not, a copy, an order answer on a
    CONFLICT and one on an IMPASSE, a failed call, and the channel of each edge;
  * with v1e off the loop is v1's, on a real run of the baseline;
  * a resumed run serves what was paid for, refuses a desynchronised answer,
    and stops on an outage without keeping it;
  * every writer refuses while the plan is unsigned, before it builds anything;
  * the smoke check, and Stage C's arithmetic at its lines.
"""

from __future__ import annotations

import dataclasses
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import Case
from harness.dsl import Condition

from authorship import gates, loop, plan, run, score
from authorship import protocol as p
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space
from rung2.proposers2 import MAX_SHOWN, SYSTEM_PROMPT_V1, ProposalError, neighbourhood

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BASE_CASE = Case(has_security_keyword=False, severity=3, customer_tier="free",
                 product="billing", channel="email", prior_tickets_30d=1,
                 off_hours=False, language="en")


def case(**kw) -> Case:
    return dataclasses.replace(BASE_CASE, **kw)


def rule(rid: str, action: str, **conds) -> Rule2:
    return Rule2(rule_id=rid, action=action,
                 conditions=[Condition(a, "eq", v) for a, v in conds.items()])


def payload_rule(action: str, beats=(), loses_to=(), **conds) -> dict:
    return {"action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()],
            "beats": list(beats), "loses_to": list(loses_to), "note": "test"}


class Scripted:
    """A proposer answering from a script keyed by (case, round)."""

    name = "scripted"

    def __init__(self, script: dict):
        self.script = script
        self.asked: list[tuple[int, int]] = []

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, p.render_base(shown, kind, engine, case)

    def _answer(self, idx: int, round_: int) -> p.Answer:
        self.asked.append((idx, round_))
        payload = self.script.get((idx, round_))
        if payload is None:
            raise p.ProposalFailed("no answer", "length", 3)
        return p.Answer(payload.get("action"), payload, json.dumps(payload), "stop", 1)

    def first(self, case, base_text, idx):
        return self._answer(idx, 0)

    def repair(self, case, base_text, previous, message, idx):
        return self._answer(idx, 1)


def world(*rules: Rule2) -> PriorityEngine:
    engine = PriorityEngine(space=Space())
    for i, r in enumerate(rules):
        engine.add(r, born_at=-1 - i, keep_id=True)
    return engine


def run_world(engine, cases, script):
    proposer = Scripted(script)
    labels = [(T1, "H00")] * len(cases)
    return loop.run_loop(cases, labels, engine, proposer), proposer


class TestTheConstants(unittest.TestCase):

    def test_section_11(self):
        self.assertEqual((plan.N, plan.SEED, plan.MODEL, plan.REASONING, plan.PROMPT),
                         (2000, 17, "deepseek/deepseek-v4-flash", {"effort": "none"},
                          "v1e"))
        self.assertEqual((plan.MAX_SHOWN, plan.REPAIR_ROUNDS, plan.LISTING_SEED,
                          plan.REPS, plan.SMOKE_N), (12, 1, 17, 3, 20))
        self.assertEqual(plan.MAX_SHOWN, MAX_SHOWN)

    def test_section_0s_lines_are_the_plans(self):
        self.assertEqual((plan.E_A_MIN_NESTED, plan.E_B_MAX_SILENT, plan.E_B_MIN_COVERAGE,
                          plan.E_C_MIN_FILL, plan.E_D_MIN_CONTRADICTIONS),
                         (0.05, 0.45, 0.90, 0.50, 1))
        text = plan.PLAN.read_text()
        for band in ("**≥ 0.05**", "**silent error ≤ 0.45 and coverage ≥ 0.90**",
                     "**≥ 0.50**", "**≥ 1**"):
            with self.subTest(band):
                self.assertIn(band, text)

    def test_the_gate_reads_this_plan_and_counts(self):
        self.assertEqual(plan.PLAN, Path("PLAN_AUTHORSHIP.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        lines = [l for l in plan.PLAN.read_text().splitlines()
                 if l.startswith("**Signed by Sergi:")]
        self.assertEqual(plan.gate_signature()["found"], len(lines))


class TestTheTexts(unittest.TestCase):

    def test_v1e_is_v1_with_one_paragraph_replaced(self):
        self.assertEqual(p.SYSTEM_PROMPT_V1E.replace(p.V1E_PARAGRAPH, p.V1_PARAGRAPH),
                         SYSTEM_PROMPT_V1)
        self.assertEqual(SYSTEM_PROMPT_V1.count(p.V1_PARAGRAPH), 1)

    def test_the_fingerprint_is_the_declared_one(self):
        self.assertEqual(p.fingerprint(), plan.FINGERPRINT)

    def test_the_order_paragraph_goes_only_where_a_conflict_is_shown(self):
        r = rule("R0001", T1, product="billing")
        self.assertIn(p.ORDER_PARAGRAPH, p.render_base([r], "conflicto"))
        self.assertNotIn(p.ORDER_PARAGRAPH, p.render_base([r], "vecindario"))

    def test_a_repair_sends_the_first_answer_back(self):
        prev = p.Answer(T1, {}, "RAW", "stop", 1)
        m = p.messages_for(BASE_CASE, "BASE", prev, "LISTA")
        self.assertEqual([x["role"] for x in m], ["system", "user", "assistant", "user"])
        self.assertEqual((m[0]["content"], m[2]["content"], m[3]["content"]),
                         (p.SYSTEM_PROMPT_V1E, "RAW", "LISTA"))


class TestTheValidator(unittest.TestCase):

    def setUp(self):
        self.engine = world(rule("X", T1, product="billing"),
                            rule("Y", T2, customer_tier="free"),
                            rule("Z", T3, product="api"))

    def ext(self, **conds) -> int:
        return self.engine.space.extension([Condition(a, "eq", v) for a, v in conds.items()])

    def test_copies_and_overlaps(self):
        self.assertEqual(p.copies_of(self.engine, self.ext(product="billing")), ["X"])
        self.assertEqual(p.copies_of(self.engine, self.ext(product="mobile")), [])
        self.assertEqual(p.overlapped(self.engine, self.ext(severity=1)), ["X", "Y", "Z"])
        self.assertEqual(p.overlapped(self.engine, self.ext(product="mobile")), ["Y"])

    def test_placed_means_cited_and_allowed(self):
        payload = {"beats": "X", "loses_to": ["Y", "Z"]}
        self.assertEqual(p.unplaced(["X", "Y", "Z"], payload, {"X", "Y"}), ["Z"])
        self.assertEqual(p.citations({"beats": 7}, "beats"), [])

    def test_the_listing_is_seeded_and_a_permutation(self):
        ids = ["R0003", "R0001", "R0002", "R0009"]
        a = p.listing(ids, 41, 0)
        self.assertEqual(sorted(a), sorted(ids))
        self.assertEqual(a, p.listing(ids, 41, 0))

    def test_order_pairs(self):
        self.assertEqual(p.order_pairs({"order": [{"winner": "A", "loser": "B"}, 3]}),
                         [("A", "B"), None])
        self.assertEqual(p.order_pairs({"order": "A>B"}), [None])
        self.assertTrue(p.is_order({"order": []}))
        self.assertFalse(p.is_order({"conditions": []}))


class TestTheLoop(unittest.TestCase):

    def test_an_order_answer_on_a_conflict(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        res, _ = run_world(engine, [BASE_CASE, BASE_CASE], {
            (0, 0): {"action": T1, "order": [{"winner": "X", "loser": "Y"}]}})
        esc = res.escalations[0]
        self.assertEqual((esc.kind, esc.verdict, esc.order), ("CONFLICT", p.ORDER,
                                                              [["X", "Y", EDGE_OK]]))
        self.assertEqual(res.edge_channels, [p.ORDER_CHANNEL])
        self.assertEqual(res.run.records[1].outcome, "ACTION")
        self.assertEqual(res.run.records[1].winner_id, "X")
        self.assertEqual(engine.rules[0].beats, [])          # never written into a rule

    def test_an_order_answer_on_an_impasse_is_refused(self):
        engine = world(rule("X", T1, product="billing"))
        res, _ = run_world(engine, [case(product="api")], {
            (0, 0): {"action": T1, "order": [{"winner": "X", "loser": "X"}]}})
        self.assertEqual(res.escalations[0].verdict, p.ORDER_WITHOUT_CONFLICT)
        self.assertEqual(res.run.records[0].predicted, T1)
        self.assertEqual(len(engine.rules), 1)

    def test_a_copy_is_refused_and_names_what_it_copies(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        res, _ = run_world(engine, [BASE_CASE], {
            (0, 0): payload_rule(T1, beats=["Y"], product="billing")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, esc.copy_of), (p.COPY, "X"))
        self.assertEqual(len(engine.rules), 2)

    def test_a_repair_round_that_places(self):
        engine = world(rule("X", T1, product="billing"))
        cases = [case(product="api", customer_tier="business")]
        res, prop = run_world(engine, cases, {
            (0, 0): payload_rule(T2, customer_tier="business"),
            (0, 1): payload_rule(T2, loses_to=["X"], customer_tier="business")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, esc.listed, len(esc.calls)), (p.BORN, ["X"], 2))
        self.assertEqual(prop.asked, [(0, 0), (0, 1)])
        self.assertEqual(esc.calls[0]["unplaced"], ["X"])
        self.assertEqual(res.edge_channels, [p.WRITE])
        self.assertEqual(engine.rules[-1].loses_to, ["X"])
        self.assertEqual(res.calls, 2)

    def test_a_repair_round_that_does_not(self):
        engine = world(rule("X", T1, product="billing"))
        res, _ = run_world(engine, [case(product="api", customer_tier="business")], {
            (0, 0): payload_rule(T2, customer_tier="business"),
            (0, 1): payload_rule(T3, customer_tier="business")})
        self.assertEqual(res.escalations[0].verdict, p.UNPLACED)
        self.assertEqual(res.run.records[0].predicted, T3)
        self.assertEqual(len(engine.rules), 1)

    def test_a_rule_overlapping_nothing_is_born_at_once(self):
        engine = world(rule("X", T1, product="billing"))
        res, prop = run_world(engine, [case(product="api")], {
            (0, 0): payload_rule(T2, product="api")})
        self.assertEqual((res.escalations[0].verdict, prop.asked), (p.BORN, [(0, 0)]))

    def test_a_failed_call(self):
        engine = world()
        res, _ = run_world(engine, [BASE_CASE], {})
        self.assertEqual(res.escalations[0].verdict, p.FAILED)
        self.assertIsNone(res.run.records[0].predicted)
        self.assertEqual(res.run.metrics["failed_proposals"], 1)
        self.assertEqual(res.escalations[0].calls[0]["finish_reason"], "length")


class TestV1IsV1(unittest.TestCase):

    def test_the_smallest_baseline_run_replays_through_the_loop(self):
        record = gates.load(plan.baseline_path(2))
        from harness.domain import generate_corpus
        got = gates.parity(record, generate_corpus(plan.N, seed=plan.SEED), Space())
        self.assertTrue(got["passes"], got)


class TestTheResume(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "run.partial.jsonl"

    def tearDown(self):
        self.dir.cleanup()

    def test_a_stored_answer_is_served_and_a_changed_request_refused(self):
        msgs = p.messages_for(BASE_CASE, "BASE")
        row = {"idx": 0, "round": 0, "digest": run.digest(msgs), "raw": "{}",
               "payload": {"action": T1}, "finish_reason": "stop", "attempts": 1,
               "failure": None}
        live = mock.Mock(side_effect=AssertionError("asked the model"))
        r = run.Resumable(mock.Mock(ask=live), self.path, [row])
        self.assertEqual(r.first(BASE_CASE, "BASE", idx=0).action, T1)
        with self.assertRaises(run.Desync):
            r.first(BASE_CASE, "OTHER BASE", idx=0)

    def test_failures_wait_and_an_outage_stops_without_keeping_them(self):
        header = run.protocol_header("r1", 2000)
        rows, resumed = run.open_partial(self.path, header)
        self.assertEqual((rows, resumed), ([], False))
        live = mock.Mock()
        live.ask.side_effect = ProposalError("down")
        r = run.Resumable(live, self.path, rows)
        for idx in range(run.STOP_AFTER_FAILURES_IN_A_ROW - 1):
            with self.assertRaises(ProposalError):
                r.first(BASE_CASE, "BASE", idx=idx)
        with self.assertRaises(run.Outage):
            r.first(BASE_CASE, "BASE", idx=99)
        self.assertEqual(self.path.read_text().splitlines(), [json.dumps(header)])

    def test_a_success_keeps_the_isolated_failures_before_it(self):
        header = run.protocol_header("r1", 2000)
        rows, _ = run.open_partial(self.path, header)
        live = mock.Mock()
        live.ask.side_effect = [ProposalError("once"),
                                p.Answer(T1, {"action": T1}, "{}", "stop", 1)]
        r = run.Resumable(live, self.path, rows)
        with self.assertRaises(ProposalError):
            r.first(BASE_CASE, "BASE", idx=0)
        r.first(BASE_CASE, "BASE", idx=1)
        kept = [json.loads(l) for l in self.path.read_text().splitlines()[1:]]
        self.assertEqual([(k["idx"], k["failure"] is None) for k in kept],
                         [(0, False), (1, True)])
        resumed, again = run.open_partial(self.path, header)
        self.assertTrue(again)
        self.assertEqual(len(resumed), 2)

    def test_a_partial_under_another_protocol_is_not_resumed(self):
        run.open_partial(self.path, run.protocol_header("r1", 2000))
        with self.assertRaises(SystemExit):
            run.open_partial(self.path, run.protocol_header("r2", 2000))


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(p, "ProposerE",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        write.assert_not_called()

    def test_stage_b(self):
        self.refuses(run.main, ["--smoke"])
        self.refuses(run.main, ["--rep", "1"])

    def test_stage_c(self):
        self.refuses(score.main, [])


class TestTheSmokeCheck(unittest.TestCase):

    def record(self, **over) -> dict:
        rec = {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
               "reasoning": plan.REASONING, "seed": plan.SEED, "n": plan.SMOKE_N,
               "repair_rounds": plan.REPAIR_ROUNDS, "fingerprint": plan.FINGERPRINT,
               "edge_channels": [], "metrics": {"n_rules": 2},
               "escalations": [{"calls": [{f: None for f in run.CALL_FIELDS}]}]}
        rec.update(over)
        return rec

    def check(self, rec) -> bool:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "smoke.json"
            path.write_text(json.dumps(rec))
            return run.smoke_check(path)[0]

    def test_it_passes_its_own_protocol_and_nothing_else(self):
        self.assertTrue(self.check(self.record()))
        self.assertFalse(self.check(self.record(fingerprint="other")))
        self.assertFalse(self.check(self.record(metrics={"n_rules": 0})))
        self.assertFalse(self.check(self.record(escalations=[{"calls": [{"round": 0}]}])))
        failed = {f: None for f in run.CALL_FIELDS} | {"failure": "down"}
        self.assertFalse(self.check(self.record(escalations=[{"calls": [failed]}])))


class TestStageCsArithmetic(unittest.TestCase):

    def test_the_share(self):
        self.assertAlmostEqual(gates.share(0.3, 0.2, 0.4), 0.5)
        self.assertIsNone(gates.share(0.3, 0.4, 0.4))

    def run_(self, a, err, cov, c, d):
        return {"E-a": a, "E-b": {"silent_error": err, "coverage": cov}, "E-c": c, "E-d": d}

    def test_the_rows_at_their_lines(self):
        v = score.verdicts([self.run_(0.05, 0.45, 0.90, 0.50, 0)] * 3)
        self.assertEqual([v[k]["holds"] for k in ("E-a", "E-b", "E-c", "E-d")],
                         [True, True, True, False])
        v = score.verdicts([self.run_(0.0499, 0.4501, 0.95, 0.4999, 1)] * 3)
        self.assertEqual([v[k]["holds"] for k in ("E-a", "E-b", "E-c", "E-d")],
                         [False, False, False, True])
        v = score.verdicts([self.run_(0.1, 0.1, 0.89, 0.6, 0)] * 3)
        self.assertFalse(v["E-b"]["holds"])

    def test_born_overlapping_nothing_is_read_in_birth_order(self):
        def r(rid, born, **conds):
            return {"rule_id": rid, "born_at": born,
                    "conditions": [{"attr": a, "op": "eq", "value": v}
                                   for a, v in conds.items()]}
        rules = [r("R2", 5, customer_tier="free"), r("R1", 1, product="billing"),
                 r("R3", 9, product="api")]
        # R1 meets nothing before it; R2 meets R1 (billing & free); R3 meets R2.
        self.assertEqual(score.born_overlapping_nothing(rules, Space()), 1)

    def test_the_baseline_beside_e_e(self):
        got = score.baseline_e(gates.load(plan.baseline_path(2)), Space())
        self.assertEqual(set(got), {"rep", "online", "escalations", "born",
                                    "born_overlapping_nothing", "distinct_overlap",
                                    "declarations", score.ONCALL, score.SECURITY})
        self.assertTrue(all(k.startswith("write:") for k in got["declarations"]))

    def test_an_undefined_share_in_any_run_is_unadjudicable(self):
        runs = [self.run_(0.1, 0.4, 0.95, 0.6, 1)] * 2 + [self.run_(0.1, 0.4, 0.95, None, 0)]
        self.assertTrue(score.verdicts(runs)["E-c"]["unadjudicable"])

    def test_a_run_scored_end_to_end_on_a_small_world(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        cases = [BASE_CASE, BASE_CASE, case(product="api", customer_tier="business")]
        res, _ = run_world(engine, cases, {
            (0, 0): {"action": T1, "order": [{"winner": "X", "loser": "Y"}]},
            (2, 0): payload_rule(T3, loses_to=["Y"], product="api")})
        rec = {"rep": 0, "rules": [r.as_dict() for r in engine.rules],
               "edge_log": engine.edge_log, "edge_channels": res.edge_channels,
               "records": [vars(r) for r in res.run.records],
               "escalations": [dataclasses.asdict(e) for e in res.escalations],
               "metrics": res.run.metrics}
        from rung3.order_search_ls import space_truth_masks
        space = Space()
        got = score.score_run(rec, cases, space, space_truth_masks(space))
        self.assertEqual(got["E-d"], 0)
        self.assertEqual(got["E-e"]["verdicts"], {p.ORDER: 1, p.BORN: 1})
        self.assertIsNotNone(got["E-e"]["by_channel"]["order"]["space"]["e2e"])


if __name__ == "__main__":
    unittest.main()
