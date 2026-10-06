"""
`PLAN_OVERLAP.md` — the instrument, no figure.

**No figure of the plan is pinned here**: Stage B has not run, and the
baselines' figures belong to their records, which `O-g2` reproduces in the dry
run. What is pinned is what makes the instrument the one §0, §5 and §10
describe:

  * the constants of §11 and the lines of §0, and the plan's own text for them;
  * v2e is v2 with one sentence replaced, its texts hash to the declared
    fingerprint, and the order paragraph goes only where a CONFLICT is shown;
  * the exempted split, and the loop on small worlds: an overlap within a queue
    owes nothing, one across queues must be placed, a repair round lists only
    those, and with the discipline off the path is rung 2's;
  * rung 2's four v2 runs replay through the loop with the discipline off;
  * §0's statistics at their edges: O-a's births, O-b's rule for runs without
    room, O-c's pooling and the edges within a queue it leaves apart;
  * every writer refuses while the plan is unsigned, before it builds anything;
  * the smoke check.
"""

from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import Case
from harness.dsl import Condition

from authorship import protocol as e
from overlap import gates, loop, plan, rows, run, score
from overlap import protocol as v
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space
from rung2.proposers2 import MAX_SHOWN, SYSTEM_PROMPT_V2, neighbourhood

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BASE_CASE = Case(has_security_keyword=False, severity=3, customer_tier="free",
                 product="billing", channel="email", prior_tickets_30d=1,
                 off_hours=False, language="en")


def case(**kw) -> Case:
    return dataclasses.replace(BASE_CASE, **kw)


def rule(rid: str, action: str, **conds) -> Rule2:
    return Rule2(rule_id=rid, action=action,
                 conditions=[Condition(a, "eq", x) for a, x in conds.items()])


def payload_rule(action: str, beats=(), loses_to=(), **conds) -> dict:
    return {"action": action,
            "conditions": [{"attr": a, "op": "eq", "value": x} for a, x in conds.items()],
            "beats": list(beats), "loses_to": list(loses_to), "note": "test"}


class Scripted:
    """A proposer answering from a script keyed by (case, round)."""

    name = "scripted"

    def __init__(self, script: dict):
        self.script = script
        self.asked: list[tuple[int, int]] = []

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, v.render_base(shown, kind, engine, case)

    def _answer(self, idx: int, round_: int) -> e.Answer:
        self.asked.append((idx, round_))
        payload = self.script.get((idx, round_))
        if payload is None:
            raise e.ProposalFailed("no answer", "length", 3)
        return e.Answer(payload.get("action"), payload, json.dumps(payload), "stop", 1)

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
                          "v2e"))
        self.assertEqual((plan.MAX_SHOWN, plan.REPAIR_ROUNDS, plan.LISTING_SEED,
                          plan.REPS, plan.SMOKE_N), (12, 1, 17, 3, 20))
        self.assertEqual(plan.MAX_SHOWN, MAX_SHOWN)

    def test_section_0s_lines_are_the_plans(self):
        self.assertEqual((plan.O_A_MAX_ALONE, plan.O_B_MIN_FILL,
                          plan.O_B_MIN_RUNS_WITH_ROOM, plan.O_C_MIN_DIRECTION),
                         (0.50, 0.50, 2, 0.70))
        text = plan.PLAN.read_text()
        for band in ("**≤ 0.50**", "**≥ 0.50**", "**≥ 0.70**",
                     "with fewer than two runs with room the row is unadjudicable"):
            with self.subTest(band):
                self.assertIn(band, text)

    def test_the_gate_reads_this_plan_and_counts(self):
        self.assertEqual(plan.PLAN, Path("PLAN_OVERLAP.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        lines = [l for l in plan.PLAN.read_text().splitlines()
                 if l.startswith("**Signed by Sergi:")]
        self.assertEqual(plan.gate_signature()["found"], len(lines))


class TestTheTexts(unittest.TestCase):

    def test_v2e_is_v2_with_one_sentence_replaced(self):
        self.assertEqual(SYSTEM_PROMPT_V2.count(v.V2_SENTENCE), 1)
        self.assertEqual(v.SYSTEM_PROMPT_V2E.replace(v.V2E_SENTENCE, v.V2_SENTENCE),
                         SYSTEM_PROMPT_V2)

    def test_the_fingerprint_is_the_declared_one(self):
        self.assertEqual(v.fingerprint(), plan.FINGERPRINT)

    def test_the_order_paragraph_is_v1es_and_only_on_a_conflict(self):
        self.assertEqual(v.ORDER_PARAGRAPH, e.ORDER_PARAGRAPH)
        engine = world(rule("R0001", T1, product="billing"))
        shown = list(engine.rules)
        self.assertIn(v.ORDER_PARAGRAPH, v.render_base(shown, "conflicto", engine, BASE_CASE))
        self.assertNotIn(v.ORDER_PARAGRAPH,
                         v.render_base(shown, "vecindario", engine, BASE_CASE))
        self.assertIn("CASA EL TICKET", v.render_base(shown, "vecindario", engine, BASE_CASE))

    def test_a_repair_sends_the_first_answer_back_under_v2e(self):
        prev = e.Answer(T1, {}, "RAW", "stop", 1)
        m = v.messages_for(BASE_CASE, "BASE", prev, "LISTA")
        self.assertEqual([x["role"] for x in m], ["system", "user", "assistant", "user"])
        self.assertEqual((m[0]["content"], m[2]["content"], m[3]["content"]),
                         (v.SYSTEM_PROMPT_V2E, "RAW", "LISTA"))
        self.assertIn("de OTRA cola", v.REPAIR_TEMPLATE)


class TestTheSplit(unittest.TestCase):

    def test_o_is_another_queue_and_s_the_same(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"),
                       rule("Z", T1, channel="email"), rule("W", T3, product="api"))
        ext = engine.space.extension([Condition("severity", "eq", 3)])
        self.assertEqual(v.split_overlapped(engine, ext, T1), (["Y", "W"], ["X", "Z"]))
        ext = engine.space.extension([Condition("product", "eq", "mobile")])
        self.assertEqual(v.split_overlapped(engine, ext, T2), (["Z"], ["Y"]))

    def test_the_listing_is_seeded_and_a_permutation(self):
        ids = ["R0003", "R0001", "R0002", "R0009"]
        a = v.listing(ids, 41, 0)
        self.assertEqual(sorted(a), sorted(ids))
        self.assertEqual(a, v.listing(ids, 41, 0))


class TestTheLoop(unittest.TestCase):

    def test_an_overlap_within_a_queue_owes_nothing(self):
        engine = world(rule("X", T2, product="billing"))
        res, prop = run_world(engine, [case(product="api")], {
            (0, 0): payload_rule(T2, customer_tier="free")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, prop.asked), (e.BORN, [(0, 0)]))
        self.assertEqual((esc.calls[0]["overlapped"], esc.calls[0]["same_queue"]),
                         ([], ["X"]))

    def test_an_overlap_across_queues_must_be_placed(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, language="es"))
        cases = [case(product="api", customer_tier="business")]
        res, prop = run_world(engine, cases, {
            (0, 0): payload_rule(T2, customer_tier="business"),
            (0, 1): payload_rule(T2, loses_to=["X"], customer_tier="business")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, esc.listed, len(esc.calls)), (e.BORN, ["X"], 2))
        self.assertEqual((esc.calls[0]["overlapped"], esc.calls[0]["same_queue"],
                          esc.calls[0]["unplaced"]), (["X"], ["Y"], ["X"]))
        self.assertEqual(engine.rules[-1].loses_to, ["X"])
        self.assertEqual(res.edge_channels, [e.WRITE])

    def test_a_repair_that_does_not_place_is_refused(self):
        engine = world(rule("X", T1, product="billing"))
        res, _ = run_world(engine, [case(product="api", customer_tier="business")], {
            (0, 0): payload_rule(T2, customer_tier="business"),
            (0, 1): payload_rule(T3, customer_tier="business")})
        self.assertEqual(res.escalations[0].verdict, e.UNPLACED)
        self.assertEqual(len(engine.rules), 1)

    def test_a_copy_is_still_refused(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        res, _ = run_world(engine, [BASE_CASE], {
            (0, 0): payload_rule(T2, product="billing")})
        self.assertEqual((res.escalations[0].verdict, res.escalations[0].copy_of),
                         (e.COPY, "X"))

    def test_an_order_answer_on_a_conflict(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        res, _ = run_world(engine, [BASE_CASE, BASE_CASE], {
            (0, 0): {"action": T1, "order": [{"winner": "X", "loser": "Y"}]}})
        self.assertEqual((res.escalations[0].verdict, res.edge_channels),
                         (e.ORDER, [e.ORDER_CHANNEL]))
        self.assertEqual(res.run.records[1].winner_id, "X")

    def test_with_the_discipline_off_the_path_is_rung_2s(self):
        class Plain:
            name = "plain"

            def build_base(self, engine, case, undefeated):
                shown, kind = neighbourhood(engine, case, undefeated)
                return shown, kind, ""

            def propose(self, case, base_text):
                return T2, payload_rule(T2, customer_tier="business")
        engine = world(rule("X", T1, product="billing"))
        res = loop.run_loop([case(product="api", customer_tier="business")],
                            [(T1, "H00")], engine, Plain(), v2e=False)
        self.assertEqual((res.escalations, res.calls, len(engine.rules)), ([], 1, 2))


class TestRung2sV2RunsReplay(unittest.TestCase):

    def test_the_four_v2_runs_replay_through_the_loop(self):
        space = Space()
        for path in plan.RUNG2_V2:
            with self.subTest(path.name):
                self.assertTrue(gates.parity(gates.load(path), space)["passes"])


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": x} for a, x in conds.items()]}


class TestTheRows(unittest.TestCase):

    def test_o_a_reads_births_in_order_and_across_queues(self):
        rules = [r_("R2", 5, T1, customer_tier="free"), r_("R1", 1, T1, product="billing"),
                 r_("R3", 9, T2, product="api"), r_("R4", 12, T2, channel="email")]
        # R1 is alone; R2 meets R1, same queue; R3 meets R2, another queue;
        # R4 meets R1 and R2 of another queue, and R3 of its own.
        b = rows.births(rules, Space())
        self.assertEqual(b, {"born": 4, "alone": 1, "alone_from_other_queues": 2})
        self.assertEqual(rows.o_a(rules, Space()), 0.5)

    def test_o_bs_rule_for_runs_without_room(self):
        self.assertEqual(rows.o_b_reading([0.2, 0.6, 0.9])["reading"], 0.6)
        two = rows.o_b_reading([1.0, None, 0.5])
        self.assertEqual((two["reading"], two["runs_with_room"], two["left_out"]),
                         (0.75, [1, 3], [2]))
        for shares in ([None, None, 0.9], [None, None, None]):
            with self.subTest(shares):
                self.assertTrue(rows.o_b_reading(shares)["unadjudicable"])
                self.assertIsNone(rows.o_b_reading(shares)["reading"])

    def test_the_pooled_fill_is_reported_not_adjudicated(self):
        fills = [{"space": {"room": 0.4, "e2e": 0.3, "alone": 0.1}},
                 {"space": {"room": 0.0, "e2e": 0.2, "alone": 0.2}}]
        self.assertAlmostEqual(rows.pooled_fill(fills), 0.5)
        self.assertIsNone(rows.pooled_fill([fills[1]]))

    def test_o_c_pools_and_leaves_ties_apart(self):
        got = rows.o_c_reading([{"hits": 22, "misses": 0}, {"hits": 36, "misses": 26},
                                {"hits": 0, "misses": 0}])
        self.assertEqual((got["hits"], got["strict"]), (58, 84))
        self.assertIsNone(rows.o_c_reading([{"hits": 0, "misses": 0}])["reading"])

    def test_direction_and_classes_on_a_small_base(self):
        engine = world(rule("A", T1, product="billing"), rule("B", T2, customer_tier="free"),
                       rule("C", T1, channel="email"))
        record = {"rules": [{"rule_id": r.rule_id, "action": r.action} for r in engine.rules],
                  "edge_log": [("A", "B", EDGE_OK), ("A", "C", EDGE_OK),
                               ("B", "C", "no_solapan")]}
        for w, l, _ in record["edge_log"][:2]:
            engine.try_edge(w, l)
        tmask = {T1: engine.ext["A"], T2: engine.ext["B"] & ~engine.ext["A"],
                 T3: 0}
        d = rows.direction(record, engine, tmask)
        self.assertEqual((d["hits"], d["installed"], d["installed_same_queue"]), (1, 2, 1))
        self.assertEqual(rows.by_queue(record, engine),
                         {"installed/different": 1, "installed/same": 1,
                          "no_solapan/different": 1})
        self.assertEqual(rows.same_queue_share(rows.by_queue(record, engine)), (1, 3))


class TestStageCsVerdicts(unittest.TestCase):

    def run_(self, a, b, hits, misses):
        return {"O-a": a, "O-b": b, "O-c": {"hits": hits, "misses": misses}}

    def test_the_rows_at_their_lines(self):
        x = score.verdicts([self.run_(0.50, 0.50, 7, 3)] * 3)
        self.assertEqual([x[k]["holds"] for k in ("O-a", "O-b", "O-c")], [True, True, True])
        x = score.verdicts([self.run_(0.5001, 0.4999, 69, 31)] * 3)
        self.assertEqual([x[k]["holds"] for k in ("O-a", "O-b", "O-c")],
                         [False, False, False])

    def test_unadjudicable_only_as_section_0_says(self):
        x = score.verdicts([self.run_(0.4, None, 0, 0), self.run_(0.4, None, 0, 0),
                            self.run_(0.4, 0.9, 0, 0)])
        self.assertTrue(x["O-b"]["unadjudicable"])
        self.assertTrue(x["O-c"]["unadjudicable"])
        self.assertFalse(x["O-a"]["unadjudicable"])
        x = score.verdicts([self.run_(0.4, None, 1, 0), self.run_(0.4, 0.6, 0, 0),
                            self.run_(0.4, 0.5, 0, 0)])
        self.assertEqual((x["O-b"]["reading"], x["O-b"]["left_out"]), (0.55, [1]))
        self.assertTrue(x["O-b"]["holds"])


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(v, "ProposerV2E",
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
        call = {f: None for f in run.CALL_FIELDS} | {"overlapped": [], "same_queue": []}
        rec = {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
               "reasoning": plan.REASONING, "seed": plan.SEED, "n": plan.SMOKE_N,
               "repair_rounds": plan.REPAIR_ROUNDS, "fingerprint": plan.FINGERPRINT,
               "edge_channels": [], "metrics": {"n_rules": 2},
               "escalations": [{"calls": [call]}]}
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
        self.assertFalse(self.check(self.record(prompt_version="v1e")))
        self.assertFalse(self.check(self.record(metrics={"n_rules": 0})))
        without_s = {f: None for f in run.CALL_FIELDS} | {"overlapped": []}
        self.assertFalse(self.check(self.record(escalations=[{"calls": [without_s]}])))


if __name__ == "__main__":
    unittest.main()
