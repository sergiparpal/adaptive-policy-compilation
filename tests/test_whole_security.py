"""
`whole/security.py` — the POST-RUN reading of why every v1c base lost a sixth of
`SECURITY_INCIDENT`, no figure of the reading.

What is pinned is what this module adds to `channel/lost.py`'s reading, which
`tests/test_channel_lost.py` pins:
- the queue's two parts, `H01`'s and `H02`'s, partitioning its points, and a
  pair that does not;
- the rules of the queue that hold a part whole, on a base built by hand;
- one part read on that base: its ways partitioning it, and its curve;
- every first call on a ticket of the queue, with its class read off the drafts,
  the conditions it adds, and a ticket of another queue left out;
- gate 7 failing on a class or a verdict that is not Stage C's;
- the losing part, and the expectation's clauses at their edges;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from blind import rows as brows
from channel import lost as L
from harness.domain import Case
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from rung2.engine2 import Space
from whole import plan
from whole import references
from whole import security as S

SPACE = Space()
SI, T2 = "SECURITY_INCIDENT", "T2_TECHNICAL"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def cond_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def rule_(rid, born, action, *conds):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds)}


KEY = cond_("has_security_keyword", "eq", True)
# S1 holds H01's region whole; S2 is one tier of it; T is the keyword's default.
S1 = rule_("S1", 0, SI, KEY, cond_("customer_tier", "in", ["business", "enterprise"]))
S2 = rule_("S2", 1, SI, KEY, cond_("customer_tier", "eq", "enterprise"))
T = rule_("T", 2, T2, KEY)


def record(rules, escalations=(), rows=None):
    rows = rows or [{"idx": r["born_at"], "cause": "ERROR", "truth": SI, "truth_rule": "H01",
                     "escalated": True, "edge_reasons": []} for r in rules]
    return {"rules": list(rules), "records": rows, "edge_log": [],
            "escalations": list(escalations)}


def ticket(**over):
    base = dict(has_security_keyword=True, severity=3, customer_tier="enterprise",
                product="api", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


class TestTheParts(unittest.TestCase):

    def setUp(self):
        self.truth = MI.space_truth()[SI]
        self.regions = rl_refs.regions()
        self.ps = S.parts(self.truth, self.regions)

    def test_the_two_parts_partition_the_queue(self):
        self.assertEqual(set(self.ps), {"H01", "H02"})
        self.assertTrue(S.partition_of(self.ps, self.truth))
        self.assertFalse(S.partition_of({"H01": self.ps["H01"], "H02": self.ps["H01"]},
                                        self.truth))
        self.assertFalse(S.partition_of({"H01": self.ps["H01"], "H02": 0}, self.truth))

    def test_h02s_part_lies_below_h01(self):
        self.assertFalse(self.ps["H02"] & self.regions["H01"])
        self.assertEqual(self.ps["H01"], self.truth & self.regions["H01"])

    def test_the_rules_that_hold_a_part_whole(self):
        engine = MI.final_engine(record([S1, S2, T]))
        self.assertEqual(S.holding(engine, self.ps["H01"]), ["S1"])
        self.assertEqual(S.holding(MI.final_engine(record([S2, T])), self.ps["H01"]), [])

    def test_where_the_lost_points_lie_added_after_the_first_run(self):
        rec = record([S2, T])
        lost = L.ways(MI.final_engine(rec), self.ps["H01"], SI)["lost"]
        got = S.by_value(lost, SPACE)
        self.assertEqual(set(got), set(S.BY))
        self.assertEqual(set(got["customer_tier"]), {"business"})
        self.assertEqual(sum(got["severity"].values()), lost.bit_count())
        self.assertEqual(sum(got["product"].values()), lost.bit_count())
        self.assertEqual(S.by_value(0, SPACE), {a: {} for a in S.BY})
        self.assertIn("after the first run", S.ADDED)

    def test_one_part_read(self):
        rec = record([S2, T])
        got = S.by_part(rec, MI.final_engine(rec), SPACE, self.ps["H01"])
        self.assertTrue(got["partitions"])
        self.assertEqual(got["points"], self.ps["H01"].bit_count())
        self.assertEqual(got["holding_whole"], [])
        self.assertLess(got["most_right"], got["points"])
        self.assertGreater(got["ways"]["unwritten"], 0)
        self.assertEqual(set(got["ways"]["lost_by_queue"]), {T2})
        self.assertEqual([w["rule_id"] for w in got["winners"]], ["T"])


def esc_(idx, verdict, *conds):
    return {"idx": idx, "verdict": verdict, "rule_id": None,
            "calls": [{"round": 0, "payload": {"action": SI, "conditions": list(conds),
                                               "note": "n"}}]}


class TestTheFirstCalls(unittest.TestCase):

    def setUp(self):
        self.regions = rl_refs.regions()
        self.conds = {r.id: rl_refs.payload_of(r)["conditions"] for r in rl_refs.text_rules()}
        self.rec = {"records": [{"idx": 0, "truth": SI, "truth_rule": "H01", "cause": "ERROR",
                                 "engine_action": T2},
                                {"idx": 1, "truth": T2, "truth_rule": "H03"}],
                    "escalations": [esc_(0, "nacida", KEY, cond_("customer_tier", "eq",
                                                                  "enterprise")),
                                    esc_(1, "nacida", KEY)]}
        self.cases = (ticket(), ticket(customer_tier="pro"))
        self.drafts = [{"idx": 0, "class": "other", "breadth": "within_or_across",
                        "verdict": "nacida"}]

    def calls(self, stage_c):
        with mock.patch.object(references, "first_drafts", return_value=self.drafts):
            return S.first_calls(self.rec, stage_c, SPACE, self.regions, self.cases, self.conds)

    def test_only_the_queues_tickets_are_read(self):
        got = self.calls(None)
        self.assertEqual([c["idx"] for c in got], [0])
        c = got[0]
        self.assertEqual((c["governing"], c["cause"], c["base_decided"], c["class"]),
                         ("H01", "ERROR", T2, "other"))
        self.assertEqual(c["extra_conditions"], [cond_("customer_tier", "eq", "enterprise")])
        self.assertIsNone(c["stage_c"])

    def test_gate_7(self):
        ok = self.calls({0: {"class": "other", "verdict": "nacida"}})
        self.assertTrue(S.stage_c_agrees(ok))
        for wrong in ({"class": "whole", "verdict": "nacida"},
                      {"class": "other", "verdict": "sin_situar"}):
            with self.subTest(wrong=wrong):
                self.assertFalse(S.stage_c_agrees(self.calls({0: wrong})))
        self.assertFalse(S.stage_c_agrees(self.calls({})))


def run_(lost=8, unwritten=8, t2=8, part="H01", own=("nacida",), most=10, points=16,
         holding=("R1",)):
    other = "H02" if part == "H01" else "H01"
    calls = [{"governing": part, "action": SI, "verdict": v} for v in own] + \
            [{"governing": other, "action": SI, "verdict": "sin_situar"}]
    return {"ways": {"lost": lost, "unwritten": unwritten,
                     "lost_by_queue": {T2: t2} if t2 else {}},
            "parts": {part: {"ways": {"lost": lost}, "most_right": most, "points": points,
                             "holding_whole": list(holding)},
                      other: {"ways": {"lost": 0}, "most_right": 4, "points": 4,
                              "holding_whole": list(holding)}},
            "first_calls": calls}


class TestTheExpectation(unittest.TestCase):

    def holds(self, v1c, beside):
        runs = {**{t: v1c for t in S.V1C}, **{t: beside for t in S.BESIDE}}
        return [c["holds"] for c in S.expectation(runs)]

    def test_the_losing_part(self):
        self.assertEqual(S.losing_part(run_(part="H02")), "H02")
        self.assertEqual(S.losing_part(run_(part="H01")), "H01")

    def test_every_clause_holding(self):
        self.assertEqual(self.holds(run_(), run_()), [True] * 5)

    def test_every_clause_failing(self):
        self.assertEqual(self.holds(run_(unwritten=7, t2=3, own=("nacida", "sin_situar"),
                                         most=16), run_(holding=())),
                         [False] * 5)

    def test_the_edges(self):
        """S2 at half the lost points; a run that lost nothing holds neither S1
        nor S2; S3 with no call of its own does not hold."""
        self.assertEqual(self.holds(run_(t2=4), run_())[1], True)
        self.assertEqual(self.holds(run_(t2=3), run_())[1], False)
        self.assertEqual(self.holds(run_(lost=0, unwritten=0, t2=0), run_())[:2],
                         [False, False])
        self.assertFalse(self.holds(run_(own=()), run_())[2])

    def test_the_lines(self):
        self.assertEqual((S.QUEUE, S.PARTS, S.DEFAULT_QUEUE, S.S_HALF),
                         (SI, ("H01", "H02"), T2, Fraction(1, 2)))
        self.assertEqual(S.V1C, ("v1c_r1", "v1c_r2", "v1c_r3"))
        self.assertEqual(S.BESIDE, ("placement_v1c_r1", "placement_v1c_r2",
                                    "placement_v1c_r3"))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    S.main(argv)
                read.assert_not_called()
                write.assert_not_called()

    def test_it_is_post_run(self):
        self.assertIn("POST-RUN", S.PROVENANCE)
        self.assertIn("before the reading ran", S.PROVENANCE)
        self.assertEqual(S.record_path(), plan.OUT / "security.json")


if __name__ == "__main__":
    unittest.main()
