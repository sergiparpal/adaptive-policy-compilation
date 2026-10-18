"""
`ranking/yielding.py` — the POST-RUN reading of which edge of a cycle yields
under the model's own rankings, no figure of the runs.

What is pinned is the instrument, on small worlds worked by hand: the ranking
arm with the ranking as an argument, which is `blind/yielding.py`'s under Stage
C's hierarchy and lets another edge yield under another; the stated rankings
gathered from a session, and the median over the asks; the coin's share at or
above an arm; the pools; the comparison with a record and its teeth; the
expectation's clauses at their edges; and that the writer refuses unsigned
before it reads or writes.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from blind import yielding as by
from rung2.engine2 import (EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK, PriorityEngine, Space,
                           validate_conditions)
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from ranking import plan
from ranking import yielding as ry

SPACE = Space()
T1, T2, T3, SEC = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


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


def decl(k, case, w, l, why, channel="write"):
    return {"k": k, "case": case, "winner": w, "loser": l, "verdict": why,
            "channel": channel}


class TheCycle(unittest.TestCase):
    """`tests/test_blind_yielding.py`'s world. W (T2: email, api, severity 1) is
    nested in N (T3: email). X (T1: api, free) was declared above W at case 10.
    At case 20 N was declared above X, which closes N > X > W > N, since W beats
    N by subsumption. A third declaration was refused as disjoint."""

    def setUp(self):
        self.bare = engine_with(rule(T2, channel="email", product="api", severity=1),
                                rule(T1, product="api", customer_tier="free"),
                                rule(T3, channel="email"),
                                rule(T1, channel="chat"))
        self.older = decl(0, 10, "R0002", "R0001", EDGE_OK)
        self.newer = decl(1, 20, "R0003", "R0002", EDGE_CYCLE)
        self.idle = decl(2, 20, "R0001", "R0004", EDGE_DISJOINT)
        self.decls = [self.older, self.newer, self.idle]
        self.action = {r.rule_id: r.action for r in self.bare.rules}

    def refused(self, hierarchy):
        return by.install(self.bare, ry.by_ranking(self.decls, self.action, hierarchy))[1]


class TestTheRankingArm(TheCycle):

    def test_under_stage_c_it_is_blinds_ranking_arm(self):
        mine = ry.by_ranking(self.decls, self.action, STAGE_C_HIERARCHY)
        theirs = by.priority("ranking", self.decls, self.action, self.bare.ext, {})
        self.assertEqual(mine, theirs)
        # T3 over T1 agrees with Stage C and T1 over T2 does not: the older yields.
        self.assertEqual(self.refused(STAGE_C_HIERARCHY), [self.older])

    def test_another_ranking_lets_another_edge_yield(self):
        # T1 above T3 and T2: X over W agrees, N over X does not, so N over X yields.
        upside = [T1, T3, T2] + [q for q in STAGE_C_HIERARCHY if q not in (T1, T2, T3)]
        self.assertEqual(self.refused(upside), [self.newer])

    def test_the_groups_and_arrival_within_them(self):
        action = {"a": T3, "b": T1, "c": T1, "d": T2}
        ds = [decl(0, 1, "b", "a", EDGE_OK),      # T1 over T3: against
              decl(1, 2, "b", "c", EDGE_OK),      # within one queue
              decl(2, 3, "a", "d", EDGE_CYCLE),   # T3 over T2: agrees
              decl(3, 4, "c", "d", EDGE_OK),      # T1 over T2: against
              decl(4, 5, "d", "b", EDGE_DISJOINT)]
        got = ry.by_ranking(ds, action, STAGE_C_HIERARCHY)
        self.assertEqual([d["k"] for d in got], [2, 1, 0, 3])

    def test_the_same_decisions_as_blinds_on_many_orders(self):
        queues = [T1, T2, T3, SEC]
        action = {f"r{i}": queues[i % 4] for i in range(12)}
        ds = [decl(k, k // 2, f"r{k % 12}", f"r{(k * 5 + 1) % 12}",
                   EDGE_OK if k % 3 else EDGE_CYCLE) for k in range(30)]
        self.assertEqual(ry.by_ranking(ds, action, STAGE_C_HIERARCHY),
                         by.priority("ranking", ds, action, {}, {}))


class TestTheStatedRankings(unittest.TestCase):

    def session(self, asks):
        return {"rows": [{"pid": f"p{i // 2:02d}", "pass": i % 2 + 1, "valid": v,
                          "ranking": r} for i, (v, r) in enumerate(asks)]}

    def test_distinct_most_asked_first_ties_by_first_ask(self):
        a, b, c = [T1, T2], [T2, T1], [T1, T3]
        got = ry.stated_rankings(self.session(
            [(True, b), (True, a), (False, None), (True, a), (True, c), (True, b)]))
        self.assertEqual([s["order"] for s in got], [b, a, c])
        self.assertEqual([s["name"] for s in got], ["stated_1", "stated_2", "stated_3"])
        self.assertEqual([s["n"] for s in got], [2, 2, 1])
        self.assertEqual(got[0]["asks"], [["p00", 1], ["p02", 2]])

    def test_the_median_ask(self):
        stated = [{"name": "a", "n": 14}, {"name": "b", "n": 5}, {"name": "c", "n": 5}]
        # A ranking given by 14 asks of 24 is the median wherever its value falls.
        for va in (0, 50, 100):
            self.assertEqual(ry.median_ask({"a": va, "b": 10, "c": 90}, stated), va)
        even = [{"name": "a", "n": 2}, {"name": "b", "n": 2}]
        self.assertEqual(ry.median_ask({"a": 1, "b": 4}, even), 2.5)


class TestTheCoinAndThePools(unittest.TestCase):

    def test_at_least(self):
        self.assertEqual(ry.at_least([1, 2, 3, 4], 3), 0.5)
        self.assertEqual(ry.at_least([1, 2, 3, 4], 5), 0.0)
        self.assertEqual(ry.at_least([1, 2, 3, 4], 1), 1.0)

    def arm(self, right):
        counts = {c: 0 for c in by.COUNTS} | {"right": right}
        return {**{e: {s: dict(counts) for s in by.SURFACES} for e in by.ENGINES},
                "halves": {e: {h: {s: dict(counts) for s in by.SURFACES} for h in by.HALVES}
                           for e in by.ENGINES}}

    def test_the_pool_sums_the_bases_with_a_cycle(self):
        per_base = {("v2e", 1): {"cycle": True, "arms": {"x": self.arm(3)}},
                    ("v2b", 1): {"cycle": True, "arms": {"x": self.arm(4)}},
                    ("v1", 1): {"cycle": False, "arms": {"x": self.arm(100)}}}
        got = ry.pool_rankings(per_base, ["x"])
        self.assertEqual(got["bases"], ["v2e 1", "v2b 1"])
        self.assertEqual(got["whole"]["x"]["closure"]["space"]["right"], 7)
        self.assertEqual(got["halves"]["x"]["direct"]["outside"]["corpus"]["right"], 7)

    def test_the_stated_median_and_the_shares(self):
        per_base = {("v2b", 1): {"cycle": True, "arms": {"stated_1": self.arm(10),
                                                         "stated_2": self.arm(40)}}}
        pooled = ry.pool_rankings(per_base, ["stated_1", "stated_2"])
        stated = [{"name": "stated_1", "n": 3}, {"name": "stated_2", "n": 1}]
        got = ry.stated_median(pooled, stated)
        self.assertEqual(got["halves"]["closure"]["outside"]["space"]["right"], 10)
        coin = {"whole": {e: {s: [5, 10, 20, 40] for s in by.SURFACES} for e in by.ENGINES},
                "halves": {e: {h: {s: [5, 10, 20, 40] for s in by.SURFACES}
                               for h in by.HALVES} for e in by.ENGINES}}
        sh = ry.shares(pooled, coin, ["stated_1", "stated_2"])
        self.assertEqual(sh["stated_1"]["halves"]["closure"]["outside"]["space"], 0.75)
        self.assertEqual(sh["stated_2"]["whole"]["direct"]["corpus"], 0.25)


class TestTheComparisonWithTheRecord(unittest.TestCase):

    def test_agrees_to_the_records_precision(self):
        self.assertTrue(ry.agrees({"a": [1, 0.5]}, {"a": [1, 0.5000015]}))
        self.assertFalse(ry.agrees({"a": [1, 0.5]}, {"a": [1, 0.50001]}))
        self.assertFalse(ry.agrees({"a": [1, 0.5]}, {"a": [2, 0.5]}))
        self.assertFalse(ry.agrees({"a": 1}, {"a": 1, "b": 2}))
        self.assertFalse(ry.agrees([1, 2], [1, 2, 3]))
        self.assertFalse(ry.agrees(True, 1))
        self.assertTrue(ry.agrees(None, None))

    def test_the_roundtrip_is_the_records_rounding(self):
        x = {"t": (1, 2), "f": 0.1234567891, "n": None}
        self.assertEqual(ry.roundtrip(x), {"t": [1, 2], "f": 0.123457, "n": None})

    def test_the_published_view_drops_what_blind_does_not_write(self):
        bases = {("v2b", 1): {"rules": 3, "_draws": [1], "_halves": {}, "arms": {}}}
        self.assertEqual(ry.published_view(bases), {"v2b 1": {"rules": 3, "arms": {}}})

    def test_same_as_blinds_has_teeth(self):
        reading = {e: {s: {"right": 1} for s in by.SURFACES} for e in by.ENGINES}
        halves = {"h": 1}
        theirs = {"kept": 2, "refused": [{"k": 4}], **reading}
        mine = {"kept": 2, "refused": [{"k": 4, "queues": [T1, T2]}], **reading,
                "halves": halves}
        self.assertTrue(ry.same_as_blinds(mine, theirs, halves))
        self.assertFalse(ry.same_as_blinds(mine | {"kept": 3}, theirs, halves))
        self.assertFalse(ry.same_as_blinds(mine | {"refused": [{"k": 5}]}, theirs, halves))
        self.assertFalse(ry.same_as_blinds(mine, theirs, {"h": 2}))


class TestTheExpectation(unittest.TestCase):

    STATED = [{"name": "stated_1", "n": 14}, {"name": "stated_2", "n": 10}]

    def world(self, revealed, stated, stage_c=100, central=(90, 110), small=True,
              keyword=0):
        def refused(*ks):
            return [{"k": k} for k in ks]

        def arms_right(**rights):
            return {n: {"closure": {ry.HALF: {"space": {"right": v}}}}
                    for n, v in rights.items()}

        bases = {("v2e", 1): {"arms": {"arrival": {"refused": refused(1)},
                                       "recency": {"refused": refused(2)},
                                       "ranking": {"refused": refused(3)}}},
                 ("v2b", 3): {"arms": {"arrival": {"refused": refused(4, 5)},
                                       "recency": {"refused": refused(6)},
                                       "ranking": {"refused": refused(6)}}}}
        want = {("v2e", 1): {"revealed": (3,), "stated": (2,)},
                ("v2b", 3): {"revealed": (4, 5), "stated": (6,)}}
        per_base = {}
        for key, w in want.items():
            rev = w["revealed"] if small else (9,)
            per_base[key] = {"arms": {
                "revealed": {"refused": refused(*rev), "keyword_refused": keyword},
                **{s["name"]: {"refused": refused(*w["stated"]), "keyword_refused": 0}
                   for s in self.STATED}}}
        per_base[("v2b", 1)] = {"arms": {"revealed": {"refused": [], "keyword_refused": 0}}}
        halves = {"pooled": {"arms": arms_right(ranking=stage_c),
                             "coin": {ry.HALF: {"closure": {"space": {"right": {
                                 "central": list(central)}}}}}}}
        pooled = {"halves": arms_right(revealed=revealed, stated_1=stated, stated_2=0)}
        return per_base, bases, halves, pooled, self.STATED

    def holds(self, *a, **k):
        return [c["holds"] for c in ry.read_expectation(*self.world(*a, **k))]

    def test_every_clause_holds(self):
        self.assertEqual(self.holds(95, 99), [True] * 5)

    def test_every_clause_fails(self):
        self.assertEqual(self.holds(120, 80, small=False, keyword=1), [False] * 5)

    def test_the_edges(self):
        # Clause 2 is strict, against the Stage C arm.
        self.assertFalse(self.holds(95, 100)[1])
        self.assertFalse(self.holds(100, 99)[1])
        # Clause 3 is inclusive at both ends of the coin's central 90%.
        self.assertTrue(self.holds(90, 99)[2])
        self.assertTrue(self.holds(95, 110, stage_c=200)[2])
        self.assertFalse(self.holds(89, 99)[2])
        # Clause 4 is strict.
        self.assertFalse(self.holds(95, 95)[3])
        self.assertTrue(self.holds(95, 96)[3])

    def test_the_stated_arm_is_the_median_ask(self):
        # stated_1 is 14 asks of 24: its value is the median, stated_2's is not read.
        x = ry.read_expectation(*self.world(95, 99))
        self.assertEqual(x[1]["reading"]["stated"], 99)


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                ry.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_the_path(self):
        self.assertEqual(ry.READ_PATH, Path("results_ranking/yielding.json"))


if __name__ == "__main__":
    unittest.main()
