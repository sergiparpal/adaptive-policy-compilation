"""
`PLAN_BLIND.md` — the instrument, no figure.

**No figure of the plan is pinned here**: Stage B has not run, and the figures
§0 declares of what is already paid for belong to their records, which `K-g2`
reproduces in the dry run. What is pinned is what makes the instrument the one
§0, §5 and §10 describe:

  * the constants of §11 and the lines of §0, and the plan's own text for them;
  * v2b is v2e with one paragraph added, its texts hash to the declared
    fingerprint, an impasse shows no rule and a CONFLICT shows v2e's screen;
  * the blind path on small worlds: a draft that overlaps no rule of another
    queue is born on one call, one that does is placed in one round that lists
    exactly those rules, and a placement that changes the rule, leaves a rule
    unplaced or never comes back is refused, as are a copy, a rule that does not
    match its ticket and an order answer on an impasse;
  * with the blind draft off, `PLAN_OVERLAP.md`'s runs replay through the loop;
  * §0's statistics at their edges: keyword rules apart, overlap read on the half
    without the keyword, each older rule counted once, the two comparators, the
    split, and the rules for too few units and for runs without room;
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
from blind import gates, loop, plan, rows, run, score
from blind import protocol as p
from overlap import protocol as v2e
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space
from rung2.proposers2 import MAX_SHOWN

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
SI = "SECURITY_INCIDENT"
BASE_CASE = Case(has_security_keyword=False, severity=3, customer_tier="free",
                 product="billing", channel="email", prior_tickets_30d=1,
                 off_hours=False, language="en")
SPACE = Space()


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
    """A proposer answering from a script keyed by (case, round), with v2b's
    screens."""

    name = "scripted"

    def __init__(self, script: dict):
        self.script = script
        self.asked: list[tuple[int, int]] = []
        self.bases: list[str] = []

    def build_base(self, engine, case, undefeated):
        shown, kind, text = p.build_base(engine, case, undefeated)
        self.bases.append(text)
        return shown, kind, text

    def _answer(self, idx: int, round_: int) -> e.Answer:
        self.asked.append((idx, round_))
        payload = self.script.get((idx, round_))
        if payload is None:
            raise e.ProposalFailed("no answer", "length", 3)
        return e.Answer(payload.get("action"), payload, json.dumps(payload), "stop", 1)

    def first(self, case, base_text, idx):
        return self._answer(idx, 0)

    def repair(self, case, base_text, previous, message, idx):
        self.message = message
        return self._answer(idx, 1)


def world(*rules: Rule2) -> PriorityEngine:
    engine = PriorityEngine(space=SPACE)
    for i, r in enumerate(rules):
        engine.add(r, born_at=-1 - i, keep_id=True)
    return engine


def run_world(engine, cases, script, blind=True):
    proposer = Scripted(script)
    labels = [(T1, "H00")] * len(cases)
    return loop.run_loop(cases, labels, engine, proposer, blind=blind), proposer


class TestTheConstants(unittest.TestCase):

    def test_section_11(self):
        self.assertEqual((plan.N, plan.SEED, plan.MODEL, plan.REASONING, plan.PROMPT),
                         (2000, 17, "deepseek/deepseek-v4-flash", {"effort": "none"},
                          "v2b"))
        self.assertEqual((plan.MAX_SHOWN, plan.PLACEMENT_ROUNDS, plan.LISTING_SEED,
                          plan.REPS, plan.SMOKE_N), (12, 1, 17, 3, 20))
        self.assertEqual(plan.MAX_SHOWN, MAX_SHOWN)

    def test_section_0s_lines_are_the_plans(self):
        self.assertEqual((plan.K_A_MAX_ALONE, plan.K_B_MIN_DIRECTION, plan.K_C_MIN_MARGIN,
                          plan.K_D_MIN_FILL, plan.K_D_MIN_RUNS_WITH_ROOM,
                          plan.K_E_MIN_DIRECTION, plan.MIN_UNITS),
                         (0.50, 0.60, 0.0, 0.50, 2, 0.60, 20))
        text = plan.PLAN.read_text()
        for band in ("**≤ 0.50**", "**≥ 0.60**", "**≥ 0.00**", "**≥ 0.50**",
                     "with fewer than 20 units the row is unadjudicable",
                     "with fewer than two runs with room the row is unadjudicable"):
            with self.subTest(band):
                self.assertIn(band, text)

    def test_the_gate_reads_this_plan_and_counts(self):
        self.assertEqual(plan.PLAN, Path("PLAN_BLIND.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        lines = [l for l in plan.PLAN.read_text().splitlines()
                 if l.startswith("**Signed by Sergi:")]
        self.assertEqual(plan.gate_signature()["found"], len(lines))


class TestTheTexts(unittest.TestCase):

    def test_v2b_is_v2e_with_one_paragraph_added(self):
        self.assertEqual(v2e.SYSTEM_PROMPT_V2E.count(p.BEFORE), 1)
        self.assertEqual(p.SYSTEM_PROMPT_V2B.replace(p.BLIND_PARAGRAPH, ""),
                         v2e.SYSTEM_PROMPT_V2E)

    def test_the_fingerprint_is_the_declared_one(self):
        self.assertEqual(p.fingerprint(), plan.FINGERPRINT)

    def test_an_impasse_shows_no_rule_and_a_conflict_v2es_screen(self):
        engine = world(rule("R0001", T1, product="billing"))
        shown, kind, text = p.build_base(engine, BASE_CASE, [])
        self.assertEqual((shown, kind, text), ([], p.BLIND, p.BLIND_BASE))
        self.assertNotIn("R0001", text)
        shown, kind, text = p.build_base(engine, BASE_CASE, list(engine.rules))
        self.assertEqual(kind, "conflicto")
        self.assertIn(p.ORDER_PARAGRAPH, text)
        self.assertEqual(text, v2e.render_base(shown, kind, engine, BASE_CASE))

    def test_a_placement_sends_the_draft_back_under_v2b(self):
        prev = e.Answer(T1, {}, "RAW", "stop", 1)
        m = p.messages_for(BASE_CASE, p.BLIND_BASE, prev, "LISTA")
        self.assertEqual([x["role"] for x in m], ["system", "user", "assistant", "user"])
        self.assertEqual((m[0]["content"], m[2]["content"], m[3]["content"]),
                         (p.SYSTEM_PROMPT_V2B, "RAW", "LISTA"))
        self.assertIn(p.BLIND_BASE, m[1]["content"])
        self.assertIn("LA MISMA regla", p.PLACEMENT_TEMPLATE)
        self.assertIn("de OTRA cola", p.PLACEMENT_TEMPLATE)


class TestTheSameRule(unittest.TestCase):

    def test_same_queue_and_extension_whatever_the_wording(self):
        a = rule("A", T2, product="billing", customer_tier="free")
        reworded = Rule2(rule_id="B", action=T2, conditions=[
            Condition("customer_tier", "in", ["free"]), Condition("product", "eq", "billing")])
        self.assertTrue(p.same_rule(a, reworded, SPACE))
        self.assertFalse(p.same_rule(a, rule("C", T1, product="billing",
                                             customer_tier="free"), SPACE))
        self.assertFalse(p.same_rule(a, rule("D", T2, product="billing"), SPACE))


class TestTheBlindPath(unittest.TestCase):

    def test_a_draft_that_meets_no_other_queue_is_born_on_one_call(self):
        engine = world(rule("X", T2, product="billing"))
        res, prop = run_world(engine, [case(product="api")], {
            (0, 0): payload_rule(T2, beats=["X"], customer_tier="free")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, prop.asked), (e.BORN, [(0, 0)]))
        self.assertEqual((esc.calls[0]["overlapped"], esc.calls[0]["same_queue"]),
                         ([], ["X"]))
        self.assertEqual(prop.bases, [p.BLIND_BASE])
        self.assertEqual(res.run.records[0].shown_ids, [])
        self.assertEqual(res.run.records[0].edge_reasons, [e.OUTSIDE])
        self.assertEqual(engine.edge_log, [])

    def test_a_draft_that_meets_another_queue_is_placed(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, language="es"),
                       rule("Z", T3, channel="email"))
        draft = payload_rule(T2, customer_tier="business")
        res, prop = run_world(engine, [case(product="api", customer_tier="business",
                                            channel="chat")], {
            (0, 0): draft,
            (0, 1): payload_rule(T2, beats=["Z"], loses_to=["X"],
                                 customer_tier="business")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, sorted(esc.listed), len(esc.calls)),
                         (e.BORN, ["X", "Z"], 2))
        self.assertEqual((esc.calls[0]["overlapped"], esc.calls[0]["same_queue"]),
                         (["X", "Z"], ["Y"]))
        self.assertEqual((esc.calls[1]["unplaced"], esc.calls[0]["listed"]),
                         ([], esc.listed))
        self.assertEqual(esc.listed, p.listing(["X", "Z"], 0, 0))
        self.assertIn("X: SI", prop.message)
        self.assertNotIn("Y: SI", prop.message)
        born = engine.rules[-1]
        self.assertEqual((born.beats, born.loses_to), (["Z"], ["X"]))
        self.assertEqual(res.edge_channels, [e.WRITE, e.WRITE])

    def test_a_placement_that_changes_the_rule_is_refused(self):
        engine = world(rule("X", T1, product="billing"))
        cases = [case(product="api", customer_tier="business")]
        for second in (payload_rule(T3, loses_to=["X"], customer_tier="business"),
                       payload_rule(T2, loses_to=["X"], customer_tier="business",
                                    channel="email")):
            with self.subTest(second=second["action"]):
                engine = world(rule("X", T1, product="billing"))
                res, _ = run_world(engine, cases, {
                    (0, 0): payload_rule(T2, customer_tier="business"), (0, 1): second})
                self.assertEqual(res.escalations[0].verdict, p.CHANGED)
                self.assertEqual((len(engine.rules), engine.edge_log), (1, []))

    def test_a_placement_that_leaves_a_rule_unplaced_is_refused(self):
        engine = world(rule("X", T1, product="billing"), rule("Z", T3, channel="email"))
        res, _ = run_world(engine, [case(product="api", customer_tier="business",
                                         channel="chat")], {
            (0, 0): payload_rule(T2, customer_tier="business"),
            (0, 1): payload_rule(T2, loses_to=["X"], customer_tier="business")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, esc.calls[1]["unplaced"]), (e.UNPLACED, ["Z"]))
        self.assertEqual(len(engine.rules), 2)

    def test_a_placement_that_never_comes_back_is_refused(self):
        engine = world(rule("X", T1, product="billing"))
        res, _ = run_world(engine, [case(product="api", customer_tier="business")], {
            (0, 0): payload_rule(T2, customer_tier="business")})
        esc = res.escalations[0]
        self.assertEqual((esc.verdict, esc.calls[1]["failure"]), (e.UNPLACED, "no answer"))
        self.assertEqual(res.run.records[0].predicted, T2)

    def test_a_failed_draft_a_copy_a_rule_off_its_ticket_and_an_order(self):
        cases = [case(product="api", customer_tier="business")]
        engine = world(rule("X", T1, customer_tier="business"))
        res, _ = run_world(engine, [BASE_CASE], {})
        self.assertEqual(res.escalations[0].verdict, e.FAILED)
        self.assertTrue(res.run.records[0].predicted is None)
        # On an impasse no existing rule matches the ticket, so a copy of one
        # cannot match it either: the path is called directly to reach the check.
        got = loop.propose_blind(world(rule("X", T1, product="billing")), BASE_CASE, 0,
                                 "IMPASSE", [], p.BLIND_BASE,
                                 Scripted({(0, 0): payload_rule(T2, product="billing")}), [])
        self.assertEqual((got["esc"].verdict, got["esc"].copy_of), (e.COPY, "X"))
        res, _ = run_world(world(rule("X", T1, product="billing")), cases,
                           {(0, 0): payload_rule(T2, customer_tier="free")})
        self.assertEqual(res.escalations[0].verdict, e.REJECTED)
        res, _ = run_world(world(rule("X", T1, product="billing")), cases,
                           {(0, 0): {"action": T2, "order": []}})
        self.assertEqual(res.escalations[0].verdict, e.ORDER_WITHOUT_CONFLICT)

    def test_a_conflict_goes_through_v2es_path(self):
        engine = world(rule("X", T1, product="billing"), rule("Y", T2, customer_tier="free"))
        res, prop = run_world(engine, [BASE_CASE, BASE_CASE], {
            (0, 0): {"action": T1, "order": [{"winner": "X", "loser": "Y"}]}})
        self.assertEqual((res.escalations[0].verdict, res.edge_channels),
                         (e.ORDER, [e.ORDER_CHANNEL]))
        self.assertIn(p.ORDER_PARAGRAPH, prop.bases[0])
        self.assertEqual(res.run.records[1].winner_id, "X")

    def test_with_the_blind_draft_off_an_impasse_is_v2es(self):
        class V2EScreens(Scripted):
            def build_base(self, engine, case, undefeated):
                return gates.ReplayV2E({}).build_base(engine, case, undefeated)
        engine = world(rule("X", T1, product="billing"))
        proposer = V2EScreens({(0, 0): payload_rule(T2, loses_to=["X"],
                                                    customer_tier="business")})
        res = loop.run_loop([case(product="api", customer_tier="business")],
                            [(T1, "H00")], engine, proposer, blind=False)
        # v2e shows the neighbourhood, so the first answer can place X itself.
        self.assertEqual((res.escalations[0].verdict, proposer.asked), (e.BORN, [(0, 0)]))
        self.assertEqual(res.run.records[0].shown_ids, ["X"])


class TestOverlapsRunsReplay(unittest.TestCase):

    def test_v2es_runs_replay_through_the_loop(self):
        for path in [plan.V2E_SMOKE] + [plan.v2e_path(k) for k in plan.BASELINE_REPS]:
            with self.subTest(path.name):
                self.assertTrue(gates.parity(gates.load(path), SPACE)["passes"])


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": x} for a, x in conds.items()]}


class TestTheRows(unittest.TestCase):

    def setUp(self):
        self.outside = rows.outside_mask(SPACE)

    def test_the_half_without_the_keyword(self):
        self.assertEqual(self.outside.bit_count() * 2, SPACE.n)
        kw = rows.ext_of(r_("K", 0, SI, has_security_keyword=True), SPACE)
        self.assertTrue(rows.is_keyword(kw, self.outside))
        self.assertFalse(rows.is_keyword(kw, SPACE.full))
        self.assertFalse(rows.is_keyword(rows.ext_of(r_("P", 0, T1, product="api"), SPACE),
                                         self.outside))

    def test_k_a_leaves_keyword_rules_apart_and_reads_the_half_without_it(self):
        rules = [r_("K", 0, SI, has_security_keyword=True),
                 r_("A", 1, T1, product="billing"),
                 r_("B", 2, T2, product="billing", has_security_keyword=True),
                 r_("C", 3, T2, customer_tier="free")]
        # K is a keyword rule; A is alone; B is a keyword rule too; C meets A
        # (another queue) on the half without the keyword.
        b = rows.births_outside(rules, SPACE, self.outside)
        self.assertEqual(b, {"born": 4, "keyword": 2, "outside": 2, "alone_outside": 1})
        self.assertEqual(rows.k_a(rules, SPACE, self.outside), 0.5)
        self.assertEqual(rows.k_a(rules[:1], SPACE, self.outside), 1.0)
        # With the restriction lifted it is O-a's statistic: only K, born first,
        # meets no earlier rule of another queue.
        lifted = rows.births_outside(rules, SPACE, SPACE.full)
        self.assertEqual((lifted["keyword"], lifted["alone_outside"]), (0, 1))

    def test_direction_counts_each_older_rule_once(self):
        def row(older, winner_better, winner="N", queues=(T1, T2)):
            return {"winner": winner, "loser": older if winner == "N" else "N",
                    "older": older, "younger": "N", "channel": e.WRITE,
                    "younger_born_on": rows.IMPASSE, "queues": queues,
                    "same_queue": False, "keyword": False,
                    "space_out": rows.HIT if winner_better else rows.MISS}
        run1 = [row("A", True), row("A", True), row("A", True), row("B", False)]
        run2 = [row("A", False), dict(row("C", True), keyword=True),
                dict(row("D", True), space_out=rows.TIE)]
        d = rows.direction([run1, run2], "space_out")
        # units: (1, A) at 1.0, (1, B) at 0.0, (2, A) at 0.0; C is a keyword
        # edge and D a tie.
        self.assertEqual((d["units"], d["hits"], d["strict"], d["ties"]), (3, 3, 5, 1))
        self.assertAlmostEqual(d["reading"], 1 / 3)
        self.assertAlmostEqual(d["pooled"], 0.6)
        self.assertEqual(d["largest_unit"], 3)

    def test_the_comparators_name_their_own_rule(self):
        base = {"older": "O", "younger": "N", "channel": e.WRITE,
                "younger_born_on": rows.IMPASSE, "same_queue": False, "keyword": False}
        # N, of T1, declared the winner over O, of SECURITY_INCIDENT; O is better.
        r = dict(base, winner="N", loser="O", queues=(T1, SI), space_out=rows.MISS)
        c = rows.comparators([[r]], "space_out")
        self.assertEqual(c["declared"]["hits"], 0)
        self.assertEqual(c["stage_c_ranking"]["hits"], 1)   # SI ranks above T1
        self.assertEqual(c["newborn_wins"]["hits"], 0)

    def test_the_split_reads_a_queue_pair_with_both_better_rules_as_unreachable(self):
        def row(older, w, l, qw, ql, v):
            return {"winner": w, "loser": l, "older": older, "younger": "N",
                    "channel": e.WRITE, "younger_born_on": rows.IMPASSE,
                    "queues": (qw, ql), "same_queue": False, "keyword": False,
                    "space_out": v}
        rs = [row("A", "N", "A", T1, T2, rows.HIT), row("B", "N", "B", T2, T1, rows.HIT),
              row("C", "N", "C", T1, T3, rows.MISS)]
        s = rows.split_by_queue_pair([rs], "space_out")
        self.assertEqual((s["queue_pairs"], s["unreachable_queue_pairs"]), (2, 1))
        self.assertEqual((s["unreachable"]["strict"], s["reachable"]["strict"]), (2, 1))

    def test_the_rule_for_runs_without_room(self):
        self.assertEqual(rows.median_with_room([0.2, 0.6, 0.9], 2)["reading"], 0.6)
        two = rows.median_with_room([1.0, None, 0.5], 2)
        self.assertEqual((two["reading"], two["runs_with_room"], two["left_out"]),
                         (0.75, [1, 3], [2]))
        self.assertTrue(rows.median_with_room([None, None, 0.9], 2)["unadjudicable"])

    def test_the_fill_on_a_small_base(self):
        # A beats B over their shared region; the truth there is A's.
        record = {"rules": [r_("A", 0, T1, product="billing"),
                            r_("B", 1, T2, customer_tier="free")],
                  "edge_log": [("A", "B", EDGE_OK)], "edge_channels": [e.WRITE]}
        ea = rows.ext_of(record["rules"][0], SPACE)
        eb = rows.ext_of(record["rules"][1], SPACE)
        tmask = {T1: ea, T2: eb & ~ea, T3: 0}
        f = rows.fill(record, SPACE, tmask, SPACE.full)
        self.assertEqual((f["bound"], f["e2e"]), ((ea | eb).bit_count() / SPACE.n,) * 2)
        self.assertEqual(f["share"], 1.0)
        none = rows.fill(record, SPACE, tmask, SPACE.full, keep=set())
        self.assertLess(none["e2e"], none["bound"])


class TestStageCsVerdicts(unittest.TestCase):

    def d(self, units, reading, ranking, corpus_units=None, corpus=None):
        def x(u, r):
            return {"units": u, "reading": r, "hits": 0, "strict": 0}
        return {"space": {"declared": x(units, reading), "stage_c_ranking": x(units, ranking)},
                "corpus": {"declared": x(corpus_units or units,
                                         reading if corpus is None else corpus)}}

    def test_the_rows_at_their_lines(self):
        runs = [{"K-a": 0.50, "K-d": 0.50}] * 3
        x = score.verdicts(runs, self.d(20, 0.60, 0.60))
        self.assertEqual([x[k]["holds"] for k in ("K-a", "K-b", "K-c", "K-d", "K-e")],
                         [True] * 5)
        runs = [{"K-a": 0.5001, "K-d": 0.4999}] * 3
        x = score.verdicts(runs, self.d(20, 0.5999, 0.6))
        self.assertEqual([x[k]["holds"] for k in ("K-a", "K-b", "K-c", "K-d", "K-e")],
                         [False] * 5)

    def test_unadjudicable_only_as_section_0_says(self):
        runs = [{"K-a": 0.4, "K-d": None}, {"K-a": 0.4, "K-d": None}, {"K-a": 0.4, "K-d": 0.9}]
        x = score.verdicts(runs, self.d(19, 0.9, 0.1, corpus_units=20, corpus=0.9))
        self.assertEqual([x[k]["unadjudicable"] for k in ("K-a", "K-b", "K-c", "K-d", "K-e")],
                         [False, True, True, True, False])
        self.assertTrue(x["K-e"]["holds"])


class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(p, "ProposerV2B",
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
               "placement_rounds": plan.PLACEMENT_ROUNDS, "fingerprint": plan.FINGERPRINT,
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
        self.assertFalse(self.check(self.record(prompt_version="v2e")))
        self.assertFalse(self.check(self.record(metrics={"n_rules": 0})))
        without_s = {f: None for f in run.CALL_FIELDS} | {"overlapped": []}
        self.assertFalse(self.check(self.record(escalations=[{"calls": [without_s]}])))


if __name__ == "__main__":
    unittest.main()
