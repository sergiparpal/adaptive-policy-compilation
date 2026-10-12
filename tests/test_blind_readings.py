"""
`blind/readings.py` — the POST-RUN reading of `K-d`, no figure.

What is pinned is the instrument, on small worlds worked by hand: how each arm
points an edge, that an edge within a queue keeps its direction, what an arm
resolves and gets right in the room, the coin's draws and their summary, the
expectation's clauses at their edges, and that the writer refuses unsigned
before it reads or writes.
"""

from __future__ import annotations

import random
import unittest
from pathlib import Path
from unittest import mock

from authorship import protocol as e
from blind import plan, readings, rows
from reuse import structure as st
from rung2.engine2 import EDGE_OK, Space

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
SI = "SECURITY_INCIDENT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": x} for a, x in conds.items()]}


def record(rules, log):
    return {"rules": rules, "edge_log": [(w, l, EDGE_OK) for w, l in log],
            "edge_channels": [e.WRITE] * len(log)}


class TestTheArms(unittest.TestCase):

    def setUp(self):
        # A (T1, billing) and B (T2, free) cross; C (T1, api) is of A's queue.
        self.rec = record([r_("A", 0, T1, product="billing"),
                           r_("B", 1, T2, customer_tier="free"),
                           r_("C", 2, T1, customer_tier="free", channel="email")],
                          [("A", "B"), ("C", "A")])
        self.ext = {r["rule_id"]: rows.ext_of(r, SPACE) for r in self.rec["rules"]}
        # The truth on A and B's shared region is B's queue.
        self.tmask = {T1: self.ext["A"] & ~self.ext["B"], T2: self.ext["B"], T3: 0, SI: 0}

    def test_how_each_arm_points_an_edge(self):
        p = readings.pointers(self.rec, self.ext, self.tmask)
        self.assertEqual(p["declared"]("A", "B"), ("A", "B"))
        self.assertEqual(p["ranking"]("A", "B"), ("B", "A"))   # T2 ranks above T1
        self.assertEqual(p["newborn"]("A", "B"), ("B", "A"))   # B is born later
        self.assertEqual(p["oracle"]("A", "B"), ("B", "A"))    # B is right there
        for name in ("ranking", "newborn", "oracle"):
            with self.subTest(name):
                self.assertEqual(p[name]("C", "A"), ("C", "A"))   # one queue: as declared

    def test_the_coin_is_seeded_and_leaves_a_queue_alone(self):
        def draw():
            p = readings.pointers(self.rec, self.ext, self.tmask, random.Random("17/1/0"))
            return [p["coin"]("A", "B") for _ in range(20)] + [p["coin"]("C", "A")]
        self.assertEqual(draw(), draw())
        self.assertEqual(draw()[-1], ("C", "A"))
        self.assertEqual({x for x in draw()[:-1]}, {("A", "B"), ("B", "A")})

    def test_decided_and_right_is_the_scorer_s_count(self):
        engine, verdicts = readings.install(self.rec, SPACE, lambda w, l: (w, l))
        self.assertEqual(verdicts, {EDGE_OK: 2})
        decided, right = readings.decided_and_right(engine, self.tmask, SPACE.full)
        action = {r.rule_id: r.action for r in engine.rules}
        counts = st.subsumption_on_space(rows.undefeated_masks(engine), action,
                                         self.tmask, SPACE.n)
        self.assertEqual((decided.bit_count(), right.bit_count()),
                         (counts["action"], counts["correct"]))

    def test_the_room_and_what_an_arm_resolves_in_it(self):
        # Two rules alone: subsumption leaves A and B in conflict on their shared
        # region, where B is right, and decides the rest of each right.
        rec = record(self.rec["rules"][:2], [("A", "B")])
        base = readings.base_of(rec, SPACE, self.tmask, SPACE.full)
        shared = self.ext["A"] & self.ext["B"]
        self.assertEqual(base["room_points"], shared.bit_count())
        right_way, v = readings.install(rec, SPACE, lambda w, l: (l, w))
        wrong_way, _ = readings.install(rec, SPACE, lambda w, l: (w, l))
        good = readings.arm_reading(right_way, base, self.tmask, SPACE.full, v)
        bad = readings.arm_reading(wrong_way, base, self.tmask, SPACE.full, v)
        self.assertEqual((good["share"], good["resolved_of_room"], good["right_of_resolved"]),
                         (1.0, 1.0, 1.0))
        self.assertEqual((bad["share"], bad["resolved_of_room"], bad["right_of_resolved"]),
                         (0.0, 1.0, 0.0))
        self.assertEqual(good["refused"], {})


class TestTheDraws(unittest.TestCase):

    def test_the_summary_of_the_draws(self):
        draws = [{"share": s, "resolved_of_room": 1.0, "right_of_resolved": s,
                  "right_of_room": s, "refused": {"cierra_ciclo": i % 2}}
                 for i, s in enumerate([x / 100 for x in range(100)])]
        declared = {"share": 0.9, "resolved_of_room": 1.0, "right_of_resolved": 0.9,
                    "right_of_room": 0.9}
        s = readings.summary_of_draws(draws, declared)
        self.assertAlmostEqual(s["share"]["mean"], 0.495)
        self.assertEqual(s["share"]["central"], [0.05, 0.94])
        self.assertAlmostEqual(s["share"]["at_least_declared"], 0.10)
        self.assertEqual((s["draws_with_a_refusal"], s["refused_mean"]), (50, 0.5))


class TestTheExpectation(unittest.TestCase):

    def runs(self, declared, coin_mean, central, resolved, coin_resolved, ranking, oracle):
        return {r: {"declared": {"share": declared, "resolved_of_room": resolved},
                    "coin": {"share": {"mean": coin_mean, "central": central},
                             "resolved_of_room": {"mean": coin_resolved}},
                    "ranking": {"share": ranking}, "oracle": {"share": oracle}}
                for r in (1, 2, 3)}

    def test_clause_by_clause(self):
        x = readings.read_expectation(self.runs(0.5, 0.45, [0.3, 0.6], 1.0, 0.9, 0.7, 0.9))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])
        x = readings.read_expectation(self.runs(0.7, 0.61, [0.3, 0.6], 0.9, 0.9, 0.7, 0.84))
        self.assertEqual([c["holds"] for c in x], [False, False, False, False, False])


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                readings.main([])
        read.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
