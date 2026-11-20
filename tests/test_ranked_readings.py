"""
`ranked/readings.py` — the POST-RUN readings Stage C of `PLAN_RANKED.md` left
free. No figure of the reading.

What is pinned is the instrument:
- a pair between the winner's queue and another: silent, even, against or
  with, and a decision's worst pair;
- why a wrong decision was wrong: absent, then or last;
- the excess, which adds up over the classes, and has no value without a run;
- one run's cases summed: by pair, by class, and the distinct points;
- the points of the space by the set of queues standing there, a partition;
- the abstaining engine over the space, on masks built by hand;
- a draft at a ticket of the exception, classed over the real space;
- the points a pair decides, and the ranking with two queues exchanged;
- a base over a half, by how each point is decided;
- the same draft at one ticket in two runs;
- gates 1 and 2 with teeth, on K r3's record: they pass on it, and a figure
  moved by one fails them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import json
import unittest
from collections import Counter
from fractions import Fraction
from unittest import mock

from manual import instrument as MI
from ranked import plan
from ranked import readings as RD

F = Fraction
SEC, ONC, T2, T3, AM = RD.SEC, RD.ONC, RD.T2, RD.T3, RD.AM
BILL, SS, T1 = RD.BILL, RD.SS, "T1_GENERAL"
LAST = (SEC, ONC, T3, AM, T2, BILL, SS, T1)
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


def fr(x) -> dict:
    return {"fraction": str(F(x)), "value": float(F(x))}


class TestPairs(unittest.TestCase):

    def test_each_class(self):
        votes = Counter({(AM, T3): 2, (T3, AM): 2, (AM, T2): 1, (T2, AM): 3, (AM, BILL): 4})
        self.assertEqual(RD.pair_class(AM, T3, votes), "even")
        self.assertEqual(RD.pair_class(AM, T2, votes), "against")
        self.assertEqual(RD.pair_class(AM, BILL, votes), "with")
        self.assertEqual(RD.pair_class(AM, SS, votes), "silent")

    def test_the_worst_pair(self):
        votes = Counter({(AM, T3): 2, (T3, AM): 2, (AM, T2): 1, (T2, AM): 3, (AM, BILL): 4})
        self.assertEqual(RD.worst(AM, [AM, T3, T2, BILL], votes), "even")
        self.assertEqual(RD.worst(AM, [AM, T2, BILL], votes), "against")
        self.assertEqual(RD.worst(AM, [AM, BILL], votes), "with")
        self.assertEqual(RD.worst(AM, [AM, BILL, SS, T3], votes), "silent")
        self.assertIsNone(RD.worst(AM, [AM], votes))


class TestWrongClass(unittest.TestCase):

    def test_absent_then_last(self):
        self.assertEqual(RD.wrong_class(AM, [T3, T2], LAST), "absent")
        self.assertEqual(RD.wrong_class(AM, [T3, AM], LAST), "last")       # T3 above AM
        self.assertEqual(RD.wrong_class(T3, [AM, T3], LAST), "then")       # the last puts T3 first


def row(right, cls=None, case=0, point=0, queues=(T2, BILL), reported=False, last=True,
        keyword=False, governing="H10", truth=BILL, decision=T2):
    return {"case": case, "point": point, "queues": list(queues), "right": right,
            "class": None if right else cls, "reported": reported, "last_ranking": last,
            "keyword": keyword, "governing": governing, "truth": truth, "decision": decision}


class TestExcess(unittest.TestCase):

    def runs(self):
        return {"k_r1": [row(True)] * 3 + [row(False, "absent")],
                "k_r3": [row(True)] * 4,
                "k_r2": [row(True), row(False, "last"), row(False, "last"), row(False, "then")]}

    def test_it_adds_up(self):
        ex = RD.excess(self.runs())
        self.assertEqual(ex["total"], F(3, 4) - F(1, 8))
        self.assertEqual(ex["by_class"], {"absent": -F(1, 8), "then": F(1, 4), "last": F(1, 2)})
        self.assertEqual(sum(ex["by_class"].values()), ex["total"])

    def test_no_value_without_a_run(self):
        runs = self.runs()
        del runs["k_r3"]
        self.assertIsNone(RD.excess(runs))
        self.assertIsNone(RD.excess({**self.runs(), "k_r2": []}))


class TestOneRunSummed(unittest.TestCase):

    def test_counts(self):
        rows = [row(True, case=10, point=1),
                row(False, "last", case=250, point=7, queues=(BILL, T2)),
                row(False, "last", case=260, point=7),
                row(False, "absent", case=900, point=9, queues=(T3, AM), reported=True)]
        got = RD.read_taken(rows)
        self.assertEqual((got["cases"], got["right"], got["wrong"]), (4, 1, 3))
        self.assertEqual(got["wrong_by_class"], {"absent": 1, "then": 0, "last": 2})
        self.assertEqual(got["by_pair"][f"{BILL} / {T2}"], {"cases": 3, "wrong": 2})
        self.assertEqual(got["by_pair"][f"{AM} / {T3}"], {"cases": 1, "wrong": 1})
        self.assertEqual(got["wrong_points"], {"distinct": 2, "most_repeated": 2})
        self.assertEqual(got["by_tenth"]["1"], {"cases": 2, "wrong": 2})
        self.assertEqual(got["wrong_reported"], 1)


QUEUES = {SEC: 0b000011, T2: 0b000110, AM: 0b011000}
FULL = 0b111111


class TestStandingSets(unittest.TestCase):

    def test_a_partition_by_the_queues_standing(self):
        got = RD.standing_sets({q: QUEUES.get(q, 0) for q in RD.ACTIONS}, FULL)
        self.assertEqual(got, {frozenset({SEC}): 0b000001, frozenset({SEC, T2}): 0b000010,
                               frozenset({T2}): 0b000100, frozenset({AM}): 0b011000,
                               frozenset(): 0b100000})
        union = 0
        for m in got.values():
            self.assertEqual(union & m, 0)
            union |= m
        self.assertEqual(union, FULL)


class TestAbstainingOverTheSpace(unittest.TestCase):

    def test_silent_then_with(self):
        queues = {q: QUEUES.get(q, 0) for q in RD.ACTIONS}
        truth = {SEC: 0b000010, T2: 0b000100}
        got = RD.abstentions_over_space(queues, LAST, Counter(), truth, FULL)
        self.assertEqual(got["ranking_points"], 1)
        self.assertEqual(got["by_worst_pair"]["silent"], {"points": 1, "right": 1})
        self.assertEqual(got["left_in_conflict"], {"points": 1, "right": 1})
        self.assertEqual(got["abstaining_pairs"], {f"{SEC} / {T2}: silent": 1})
        got = RD.abstentions_over_space(queues, LAST, Counter({(SEC, T2): 3, (T2, SEC): 1}),
                                        truth, FULL)
        self.assertEqual(got["left_in_conflict"], {"points": 0, "right": 0})
        self.assertEqual(got["by_worst_pair"]["with"], {"points": 1, "right": 1})


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


class TestDraftsAtTheException(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space, cls.truth = MI.space(), MI.space_truth()
        cls.keyword = cls.space.mask["has_security_keyword"][True]
        cls.regions = {h: MI.hidden_regions()[h]["mask"] for h in (RD.EXCEPTION, RD.TIER_RULE)}

    def classed(self, action, *conds):
        ext = RD.region({"action": action, "conditions": list(conds)}, self.space)
        return RD.draft_class(action, ext, self.keyword, self.truth[SEC],
                              self.regions[RD.EXCEPTION]), ext

    def test_each_class(self):
        kw = cond("has_security_keyword", "eq", True)
        cls, ext = self.classed(T2, kw, cond("severity", "gte", 3))
        self.assertEqual(cls, "reaching")
        self.assertTrue(ext & self.regions[RD.TIER_RULE])       # the tier dropped
        cls, ext = self.classed(T2, kw, cond("customer_tier", "in", ["free", "pro"]),
                                cond("severity", "gte", 3))
        self.assertEqual(cls, "exception")
        self.assertEqual(ext, self.regions[RD.EXCEPTION])       # the policy's own, whole
        self.assertEqual(self.classed(T2, cond("severity", "gte", 3))[0], "beyond")
        self.assertEqual(self.classed(SEC, kw)[0], "other_queue")
        self.assertIsNone(RD.region({"action": T2, "conditions": []}, self.space))
        self.assertEqual(RD.draft_class(T2, None, 0, 0, 0), "invalid")


class TestThePair(unittest.TestCase):

    def test_where_it_decides(self):
        queues = {SEC: 0b0001, T3: 0b0110, AM: 0b1100}
        self.assertEqual(RD.pair_decides(queues, LAST, T3, AM), 0b0100)
        queues[SEC] = 0b0101
        self.assertEqual(RD.pair_decides(queues, LAST, T3, AM), 0)
        # a queue below both does not block
        queues = {T3: 0b0110, AM: 0b1100, T2: 0b0100}
        self.assertEqual(RD.pair_decides(queues, LAST, T3, AM), 0b0100)

    def test_exchanged(self):
        got = RD.swapped(LAST, T3, AM)
        self.assertEqual(got[2:4], (AM, T3))
        self.assertEqual(set(got), set(LAST))


class TestAHalf(unittest.TestCase):

    def test_by_how_each_point_is_decided(self):
        # eight points: 0-1 rung 2 right, 2 rung 2 wrong, 3-4 conflict (3 right by the
        # ranking), 5 undecided, 6-7 outside the half
        read = {"rung2": 0b00000011, "conflict": 0b00011000, "decided": 0b11011111,
                "ranked": 0b00001011}
        truth = {AM: 0b00001001, T3: 0b00000110}
        base = {"read": read, "right": read["ranked"], "own": "ranked"}
        got = RD.half(base, truth, 0b00111111)
        self.assertEqual({k: got[k] for k in ("points", "right", "rung2_right", "ranking_right",
                                              "conflict", "undecided", "decided_wrong")},
                         {"points": 6, "right": 3, "rung2_right": 2, "ranking_right": 1,
                          "conflict": 2, "undecided": 1, "decided_wrong": 1})
        self.assertEqual(got["by_queue"][AM]["ranking_right"], 1)
        got = RD.half({**base, "own": "rung2", "right": read["rung2"]}, truth, 0b00111111)
        self.assertEqual((got["right"], got["ranking_right"]), (2, 0))


class TestTheSameDraft(unittest.TestCase):

    def test_pairs_of_runs_told_the_queue(self):
        def c(esc, ext):
            return {"case": 5, "escalation": esc, "action": T2, "extension": ext,
                    "class": "reaching"}
        calls = {"l_r1": [c("ERROR", 7)], "k_r1": [c("ERROR", 7)], "l_r2": [c("IMPASSE", 7)],
                 "k_r2": [c("ERROR", 3)], "l_r3": [], "k_r3": [c("ERROR", None)]}
        got = RD.same_draft_pairs(calls, {5})
        self.assertEqual((got["pairs"], got["same"]), (6, 1))
        self.assertEqual(got["per_ticket"]["5"]["runs"], ["l_r1", "k_r1", "k_r2", "k_r3"])


class TestGatesWithTeeth(unittest.TestCase):
    """On K r3's record: the gates pass, and one figure moved fails them. Nothing
    of the reading is printed or pinned."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(plan.run_path(plan.RANKED, 3).read_text())
        cls.space, cls.truth = MI.space(), MI.space_truth()
        cls.corpus = list(MI.corpus())

    def test_gate_two(self):
        _, ok = RD.taken(self.record, self.space, self.corpus)
        self.assertTrue(ok)
        logs = self.record["ranked"]["cases"]
        i = next(i for i, c in enumerate(logs) if c["by"] == "ranking")
        logs[i]["votes_for"] += 1
        try:
            self.assertFalse(RD.taken(self.record, self.space, self.corpus)[1])
        finally:
            logs[i]["votes_for"] -= 1
        j = next(i for i, c in enumerate(logs) if c["by"] == "rung2")
        logs[j]["by"] = None
        try:
            self.assertFalse(RD.taken(self.record, self.space, self.corpus)[1])
        finally:
            logs[j]["by"] = "rung2"

    def test_gate_one(self):
        base = RD.base_of(self.record, self.space, self.truth)
        keyword = self.space.mask["has_security_keyword"][True]
        right = base["right"]
        kept = {"space": fr(F(right.bit_count(), self.space.n)),
                "keyword_half": [(right & keyword).bit_count(), (right & ~keyword).bit_count()]}
        self.assertTrue(RD.gate_one(base, kept, keyword, self.space.n))
        kept["keyword_half"][0] += 1
        self.assertFalse(RD.gate_one(base, kept, keyword, self.space.n))


def fake(last=F(1, 2), total=F(3, 4), pair_wrong=11, wrong=20, distinct=11, governing="H03",
         escalation="ERROR", report=T2, h01=1, reaching=3, exception=2, pairs=4, same=3,
         interleaving=6, ranking_right=10, conflict=6, not_right=10, k_right_there=4,
         decides=1343, am=5, t3=4, beside=9, sec_mine=F(1), sec_other=F(9, 10),
         onc_mine=F(1), onc_other=F(9, 10), kw=6, other=5, left_cases=9, left_points=9,
         left_right=5):
    a = {"excess": {"total": fr(total),
                    "by_class": {"absent": fr(0), "then": fr(total - last), "last": fr(last)}},
         "runs": {"k_r2": {"wrong": wrong,
                           "by_pair": {f"{BILL} / {T2}": {"cases": wrong, "wrong": pair_wrong}},
                           "wrong_points": {"distinct": distinct, "most_repeated": 2}}}}
    b = {"nested": {t: ([{"reaches": True, "governing": governing, "escalation": escalation,
                          "report": report, "tier_rule_points": h01}] if t == "k_r2" else [])
                    for t in RD.RUNS},
         "told_the_queue": {"by_class": {"reaching": reaching, "exception": exception}},
         "same_ticket": {"pairs": pairs, "same": same}}
    by_queue = {q: {"ranking_right": interleaving if q == AM else 0} for q in RD.ACTIONS}
    c = {f"r{k}": {"k": {"ranking_right": ranking_right, "by_queue": by_queue},
                   "l": {"conflict": conflict, "points": 100, "right": 100 - not_right},
                   "l_conflict_k_decides_right": {"points": k_right_there}} for k in (1, 2, 3)}
    d = {t: {"pair_decides": {"points": decides, "account_manager": am, "t3_engineering": t3},
             "account_manager": {"t3_beside": beside, "points": 100}} for t in RD.K_RUNS}
    e = {t: {"median_recall": {SEC: fr(sec_mine if t == "k_r2" else sec_other),
                               ONC: fr(onc_mine if t == "k_r2" else onc_other)}}
         for t in RD.RUNS}
    e["k_r2"]["beyond_the_loop"] = {"keyword_half": kw, "other_half": other}
    f = {"arrivals": {t: {"cases": 100, "left_in_conflict": {"cases": left_cases}}
                      for t in RD.K_RUNS},
         "space": {t: {"ranking_points": 100,
                       "left_in_conflict": {"points": left_points, "right": left_right}}
                   for t in RD.K_RUNS}}
    return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in RD.read_expectation(readings)}


CLAUSES = [f"{x}{k}" for x, n in (("A", 3), ("B", 5), ("C", 3), ("D", 3), ("E", 3), ("F", 3))
           for k in range(1, n + 1)]


class TestTheExpectation(unittest.TestCase):

    def test_twenty_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(last=F(3, 8), pair_wrong=10, distinct=10, governing="H01",
                         escalation="IMPASSE", h01=0, reaching=2, pairs=4, same=2,
                         interleaving=5, conflict=5, k_right_there=2, decides=1344, am=4,
                         beside=10, sec_mine=F(9, 10), onc_mine=F(9, 10), kw=5,
                         left_cases=10, left_points=10, left_right=5))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_each_edge_alone(self):
        self.assertFalse(holds(fake(report=BILL))["B2"])
        self.assertTrue(holds(fake(report=BILL))["B1"])
        self.assertFalse(holds(fake(left_points=8, left_right=4))["F3"])
        self.assertTrue(holds(fake(left_points=8, left_right=4))["F2"])

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(RD, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                RD.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
