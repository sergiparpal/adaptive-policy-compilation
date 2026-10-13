"""
`blind/cycles.py` — the POST-RUN reading of why run 1 closed cycles, no figure.

What is pinned is the instrument, on small worlds worked by hand: the fork, the
side each listed rule is placed on, the ordered and inverted pairs, why an edge
closes a cycle in each of the four ways a birth can close one, the slot
statistic and its permutation null, the slices of the log each escalation
wrote, the expectation's clauses at their edges, the smoke run replayed with its
forks, and that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from harness.domain import generate_corpus

from authorship import protocol as e
from blind import cycles, plan
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space, validate_conditions

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def rule(action, **conds):
    return validate_conditions(
        {"action": action,
         "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]},
        case=None)


def engine_with(*rules) -> PriorityEngine:
    eng = PriorityEngine(space=SPACE)
    for i, r in enumerate(rules):
        eng.add(r, born_at=i)
    return eng


class TestTheFork(unittest.TestCase):

    def test_a_fork_does_not_write_the_engine(self):
        eng = engine_with(rule(T1, product="billing"), rule(T2, customer_tier="free"))
        f = cycles.fork(eng)
        f.add(rule(T3, channel="email"), born_at=2)
        self.assertEqual(f.try_edge("R0003", "R0001"), EDGE_OK)
        self.assertEqual([r.rule_id for r in eng.rules], ["R0001", "R0002"])
        self.assertEqual((eng._next_id, eng.decl_above["R0001"]), (3, set()))
        self.assertNotIn("R0003", eng.ext)
        self.assertEqual(f.rules[2].rule_id, "R0003")


class TestSides(unittest.TestCase):

    def test_each_listed_rule_on_its_side(self):
        payload = {"beats": ["A", " B ", "Z"], "loses_to": "C"}
        self.assertEqual(cycles.sides(payload, ["C", "A", "B", "D"]),
                         {"C": cycles.ABOVE, "A": cycles.BELOW, "B": cycles.BELOW})
        both = {"beats": ["A"], "loses_to": ["A", "B"]}
        self.assertEqual(cycles.sides(both, ["A", "B"]),
                         {"A": cycles.BOTH, "B": cycles.ABOVE})


class TestWhyAnEdgeClosesACycle(unittest.TestCase):
    """A is T1 on billing, B is T2 on the free tier, and A is declared above B.
    N, T3 on email, crosses both and nests in neither."""

    def setUp(self):
        self.eng = engine_with(rule(T1, product="billing"), rule(T2, customer_tier="free"))
        self.assertEqual(self.eng.try_edge("R0001", "R0002"), EDGE_OK)
        self.f = cycles.fork(self.eng)
        self.f.add(rule(T3, channel="email"), born_at=2)

    def test_an_inverted_pair(self):
        side = {"R0001": cycles.BELOW, "R0002": cycles.ABOVE}
        pairs = cycles.ordered_pairs(self.f, ["R0002", "R0001"], side)
        self.assertEqual(pairs, [("R0001", "R0002")])
        self.assertEqual(cycles.inverted(pairs, side), [("R0001", "R0002")])
        refusals, same = cycles.reinstall(
            self.f, [("R0003", "R0001", EDGE_OK), ("R0002", "R0003", EDGE_CYCLE)],
            [e.WRITE, e.WRITE], "R0003")
        self.assertTrue(same)
        self.assertEqual(len(refusals), 1)
        r = refusals[0]
        self.assertEqual((r["edge"], r["side"], r["kind"], r["through"]),
                         (["R0002", "R0003"], cycles.ABOVE, "pair", ["R0001"]))
        self.assertEqual(r["path"], [["R0003", "R0001", "decl"], ["R0001", "R0002", "decl"]])

    def test_a_consistent_placement_is_not_inverted(self):
        side = {"R0001": cycles.ABOVE, "R0002": cycles.BELOW}
        pairs = cycles.ordered_pairs(self.f, ["R0001", "R0002"], side)
        self.assertEqual(cycles.inverted(pairs, side), [])

    def test_one_rule_on_both_sides(self):
        refusals, same = cycles.reinstall(
            self.f, [("R0003", "R0001", EDGE_OK), ("R0001", "R0003", EDGE_CYCLE)],
            [e.WRITE, e.WRITE], "R0003")
        self.assertTrue(same)
        self.assertEqual((refusals[0]["kind"], refusals[0]["through"]), ("both", ["R0001"]))

    def test_a_wrong_logged_verdict_is_caught(self):
        _, same = cycles.reinstall(self.f, [("R0002", "R0003", EDGE_CYCLE)],
                                   [e.WRITE], "R0003")
        self.assertFalse(same)

    def test_an_order_edge(self):
        refusals, same = cycles.reinstall(cycles.fork(self.eng), [("R0002", "R0001", EDGE_CYCLE)],
                                          [e.ORDER_CHANNEL], None)
        self.assertTrue(same)
        self.assertEqual((refusals[0]["kind"], refusals[0]["side"]), ("order", None))

    def test_the_new_rule_inside_a_rule_above_the_one_it_loses_to(self):
        # Z (T2) holds the half without the keyword and is declared above Y
        # (T1, billing); N (T3, email, no keyword) is nested in Z.
        eng = engine_with(rule(T2, has_security_keyword=False), rule(T1, product="billing"))
        self.assertEqual(eng.try_edge("R0001", "R0002"), EDGE_OK)
        f = cycles.fork(eng)
        f.add(rule(T3, channel="email", has_security_keyword=False), born_at=2)
        refusals, same = cycles.reinstall(f, [("R0002", "R0003", EDGE_CYCLE)],
                                          [e.WRITE], "R0003")
        self.assertTrue(same)
        self.assertEqual((refusals[0]["kind"], refusals[0]["through"]),
                         ("inside", ["R0001"]))
        self.assertEqual(refusals[0]["path"][0], ["R0003", "R0001", "sub"])

    def test_the_new_rule_around_a_rule_below_the_one_it_beats(self):
        # W (T2, email and api) is nested in N (T3, email); X (T1, api, free)
        # is declared above W; N beats X closes X -> W -> N.
        eng = engine_with(rule(T2, channel="email", product="api"),
                          rule(T1, product="api", customer_tier="free"))
        self.assertEqual(eng.try_edge("R0002", "R0001"), EDGE_OK)
        f = cycles.fork(eng)
        f.add(rule(T3, channel="email"), born_at=2)
        refusals, same = cycles.reinstall(f, [("R0003", "R0002", EDGE_CYCLE)],
                                          [e.WRITE], "R0003")
        self.assertTrue(same)
        self.assertEqual((refusals[0]["kind"], refusals[0]["side"], refusals[0]["through"]),
                         ("contains", cycles.BELOW, ["R0001"]))


class TestTheSlot(unittest.TestCase):

    def placement(self, listed, inverted=()):
        return {"listed": [list(x) for x in listed], "inverted": [list(x) for x in inverted]}

    def test_the_pairs_each_statistic_counts(self):
        r = self.placement([("Y", cycles.ABOVE), ("X", cycles.BELOW), ("C", cycles.ABOVE)],
                           inverted=[("X", "Y")])
        got = cycles.slot_pairs(r)
        self.assertEqual(got["mixed"], [(0, 1), (2, 1)])
        self.assertEqual(got["inverted"], [(0, 1)])
        self.assertEqual(cycles.statistic(got["mixed"], [0, 1, 2]), 0)
        self.assertEqual(cycles.statistic(got["mixed"], [0, 2, 1]), 2)
        self.assertEqual(cycles.statistic(got["inverted"], [1, 0, 2]), -1)

    def test_one_pair_is_as_extreme_as_any_permutation(self):
        rounds = {1: [self.placement([("A", cycles.ABOVE), ("B", cycles.BELOW)])]}
        t = cycles.slot_test(rounds, 200, 17)
        self.assertEqual(t["mixed"]["1"]["statistic"], 1)
        self.assertEqual((t["mixed"]["pooled"]["as_extreme"], t["mixed"]["pooled"]["p"]),
                         (200, 1.0))
        self.assertEqual(t["inverted"]["pooled"]["pairs"], 0)

    def test_a_slot_that_decides_is_found_and_the_draws_are_seeded(self):
        rounds = {1: [self.placement([("A", cycles.ABOVE), ("B", cycles.BELOW)])] * 12,
                  2: [self.placement([("A", cycles.ABOVE), ("B", cycles.BELOW)])] * 12}
        t = cycles.slot_test(rounds, 200, 17)
        self.assertEqual(t["mixed"]["pooled"]["statistic"], 24)
        self.assertEqual(t["mixed"]["pooled"]["per_pair"], 1.0)
        self.assertLess(t["mixed"]["pooled"]["p"], 0.01)
        self.assertEqual(t, cycles.slot_test(rounds, 200, 17))

    def test_by_slot(self):
        rounds = [self.placement([("A", cycles.ABOVE), ("B", cycles.BELOW), ("C", cycles.BOTH)]),
                  self.placement([("D", cycles.BELOW)])]
        self.assertEqual(cycles.by_slot(rounds),
                         {"first": {cycles.ABOVE: 1}, "between": {cycles.BELOW: 1},
                          "last": {cycles.BOTH: 1}})


class TestTheSegments(unittest.TestCase):

    def test_each_escalation_gets_the_fork_of_its_last_call_and_its_slice(self):
        record = {"escalations": [{"idx": 3, "calls": [{"round": 0}, {"round": 1}]},
                                  {"idx": 7, "calls": [{"round": 0}]}],
                  "edge_log": [["a", "b", EDGE_OK], ["c", "d", EDGE_OK], ["e", "f", EDGE_OK]]}
        forks = {(3, 0): ("F30", 0), (3, 1): ("F31", 0), (7, 0): ("F70", 2)}
        got = cycles.segments(record, forks)
        self.assertEqual([(s["fork"], s["last"], s["start"], s["end"]) for s in got],
                         [("F31", 1, 0, 2), ("F70", 0, 2, 3)])


class TestTheExpectation(unittest.TestCase):

    def runs(self, ordered, inverted, births, repeats):
        return {str(k): {"ordered_pairs": o, "inverted_pairs": i,
                         "inverted_share": i / o if o else None,
                         "write_refusals": {"births_with_a_cycle": births},
                         "order_refusals": {"repeating_a_write_refusal": repeats}}
                for k, o, i in zip((1, 2, 3), ordered, inverted)}

    def readings(self, p_mixed, p_inverted):
        return {"mixed": {"pooled": {"p": p_mixed}},
                "inverted": {"pooled": {"p": p_inverted}}}

    def test_clause_by_clause(self):
        x = cycles.read_expectation(self.readings(0.05, 0.5),
                                    self.runs((10, 10, 10), (2, 1, 0), 6, 9))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])
        x = cycles.read_expectation(self.readings(0.049, 0.01),
                                    self.runs((10, 10, 10), (1, 2, 0), 7, 8))
        self.assertEqual([c["holds"] for c in x], [False, False, False, False, False])

    def test_no_ordered_pair_in_runs_2_and_3_leaves_clause_4_unread(self):
        x = cycles.read_expectation(self.readings(0.5, 0.5), self.runs((10, 0, 0), (2, 0, 0), 1, 9))
        self.assertIsNone(x[3]["holds"])


class TestTheSmokeRun(unittest.TestCase):
    """The replay, its forks and its slices on the smoke run's 20 cases: what the
    gates ask of the full runs, on the one record small enough for the suite."""

    def test_the_replay_is_the_run_and_the_forks_are_the_engine(self):
        record = json.loads(plan.SMOKE_PATH.read_text())
        corpus = generate_corpus(record["n"], seed=record["seed"])
        proposer, parity = cycles.replay(record, SPACE, corpus)
        self.assertEqual(parity, {k: True for k in parity})
        action = {r["rule_id"]: r["action"] for r in record["rules"]}
        segs = [cycles.read_segment(s, record, corpus, action)
                for s in cycles.segments(record, proposer.forks)]
        self.assertEqual(sum(s["logged"] for s in segs), len(record["edge_log"]))
        for s in segs:
            with self.subTest(idx=s["idx"]):
                self.assertTrue(s["verdicts_ok"] and s["id_ok"] and s["quiet_ok"])
        placements = [s for s in segs if s["placement"] is not None]
        self.assertTrue(placements)
        for s in placements:
            self.assertEqual([rid for rid, _ in s["placement"]["listed"]],
                             next(x["listed"] for x in record["escalations"]
                                  if x["idx"] == s["idx"]))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                cycles.main([])
        read.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
