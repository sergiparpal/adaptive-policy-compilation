"""
`ranked/twins.py` — the POST-RUN reading of one region under two queues. No
figure of the reading.

What is pinned is the instrument:
- the twin pairs read off a record built by hand over the real space: a copy
  of another queue is a pair, a copy of the same queue is counted apart, and
  gate 1 fails on a `copy_of` that is not the first copy or on two regions
  that differ;
- what bore a rule at a case;
- the edge between a pair: the newborn above or its twin, installed, refused,
  or not listed, and gate 3 failing on an edge tried at another birth;
- the region's points by the queue each engine decides there, rung 2's and the
  ranking's, and the region read in a base built by hand;
- the arrivals in the region after the newborn's birth, right, wrong or left;
- gate 1 with teeth on K r2's record;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

from edges.rebuild import Edge
from manual import instrument as MI
from ranked import plan
from ranked import reading as R
from ranked import twins as TW

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SS, BILL, T1 = "SELF_SERVICE_DEFLECT", "BILLING_SPECIALIST", "T1_GENERAL"
BILLING4 = [{"attr": "product", "op": "eq", "value": "billing"},
            {"attr": "severity", "op": "eq", "value": 4}]
BILLING4_IN = [{"attr": "severity", "op": "in", "value": [4]},
               {"attr": "product", "op": "eq", "value": "billing"}]
FREE = [{"attr": "customer_tier", "op": "eq", "value": "free"}]


def rule(rid, action, born_at, conditions):
    return {"rule_id": rid, "action": action, "born_at": born_at, "conditions": conditions}


def esc(idx, rid, copies, kind="ERROR", copy_of="first"):
    return {"idx": idx, "kind": kind, "verdict": "nacida", "rule_id": rid,
            "copy_of": (copies[0] if copies else None) if copy_of == "first" else copy_of,
            "calls": [{"copies": list(copies), "left_out": {}}]}


def record():
    return {"rules": [rule("R1", BILL, 1, BILLING4), rule("R2", SS, 2, BILLING4_IN),
                      rule("R3", BILL, 3, BILLING4), rule("R4", T1, 4, FREE)],
            "escalations": [esc(1, "R1", []), esc(2, "R2", ["R1"]),
                            esc(3, "R3", ["R1", "R2"]), esc(4, "R4", [], kind="IMPASSE"),
                            {"idx": 5, "kind": "ERROR", "verdict": "sin_situar",
                             "calls": [{"copies": ["R4"]}]}]}


class TestTheTwins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()

    def test_pairs_and_copies(self):
        pairs, counts, ok = TW.twins_of(record(), self.space)
        self.assertTrue(ok)
        self.assertEqual([(p["newborn"], p["twin"]) for p in pairs], [("R2", "R1"), ("R3", "R2")])
        self.assertEqual(counts, {"births": 4, "twin_births": 2, "pairs": 2, "copy_births": 1})
        self.assertEqual(pairs[0]["queues"], [SS, BILL])
        self.assertEqual(pairs[0]["points"], self.space.extension(
            [TW.Condition(**c) for c in BILLING4]).bit_count())

    def test_gate_one_has_teeth(self):
        r = record()
        r["escalations"][2]["copy_of"] = "R2"
        self.assertFalse(TW.twins_of(r, self.space)[2])
        r = record()
        r["rules"][1]["conditions"] = FREE
        self.assertFalse(TW.twins_of(r, self.space)[2])

    def test_what_bore_a_rule(self):
        r = record()
        r["records"] = [{"idx": i, "truth_rule": "H12", "truth": SS, "engine_rule": "R1",
                         "engine_action": BILL} for i in range(6)]
        r["reports_handed"] = {"2": SS}
        got = TW.birth_of(r, 2)
        self.assertEqual(got, {"case": 2, "kind": "ERROR", "report": SS, "governing": "H12",
                               "truth": SS, "decided_by": "R1", "decided": BILL})


class TestTheSide(unittest.TestCase):

    PAIR = {"newborn": "R2", "twin": "R1", "born_at": 2}

    def test_each_fate(self):
        by = {2: [Edge(0, 2, "R2", "R1", "ok")]}
        self.assertEqual(TW.edge_fate(by, self.PAIR, {("R2", "R1")})[0], TW.NEWBORN_ABOVE)
        by = {2: [Edge(0, 2, "R1", "R2", "ok")]}
        self.assertEqual(TW.edge_fate(by, self.PAIR, {("R1", "R2")})[0], TW.TWIN_ABOVE)
        by = {2: [Edge(0, 2, "R2", "R1", "cierra_ciclo")]}
        fate, log, at = TW.edge_fate(by, self.PAIR, set())
        self.assertEqual((fate, log, at), (TW.REFUSED, [["R2", "R1", "cierra_ciclo"]], True))
        self.assertEqual(TW.edge_fate({}, self.PAIR, set())[0], TW.NOT_LISTED)

    def test_gate_three_has_teeth(self):
        by = {7: [Edge(0, 7, "R2", "R1", "ok")]}
        self.assertFalse(TW.edge_fate(by, self.PAIR, {("R2", "R1")})[2])


def base(own, queues, ranking=(), conflict=0, right=0):
    return {"own": own, "queues": queues, "ranking": list(ranking),
            "read": {"conflict": conflict}, "right": right}


class TestWhatItDecided(unittest.TestCase):

    def test_by_rung_two(self):
        b = base("rung2", {SS: 0b0111, BILL: 0b0110, T1: 0b1000}, conflict=0b0110)
        got = TW.decided_by_queue(b, 0b1111)
        self.assertEqual(got, {SS: 0b0001, T1: 0b1000})

    def test_by_the_ranking(self):
        b = base("ranked", {SS: 0b0111, BILL: 0b0110, T1: 0b1000}, ranking=(BILL, SS, T1))
        got = TW.decided_by_queue(b, 0b1111)
        self.assertEqual(got, {BILL: 0b0110, SS: 0b0001, T1: 0b1000})

    def test_the_region_read(self):
        truth = {SS: 0b0011, BILL: 0b0100, T1: 0b1000}
        b = base("ranked", {SS: 0b0111, BILL: 0b0110, T1: 0b1000}, ranking=(BILL, SS, T1),
                 right=0b1101)
        pair = {"queues": [SS, BILL]}
        got = TW.region_reading(b, pair, 0b0111, truth)
        self.assertEqual(got, {"points": 3, "truth": {"newborn": 2, "twin": 1, "other": 0},
                               "decided": {"newborn": 1, "twin": 2, "other": 0, "no_queue": 0},
                               "right": 2})


class TestTheArrivals(unittest.TestCase):

    def test_after_the_birth_and_in_the_region(self):
        space, corpus = MI.space(), list(MI.corpus())
        region = R.point_of(corpus[3], space) | R.point_of(corpus[5], space) \
            | R.point_of(corpus[6], space) | R.point_of(corpus[1], space)
        rows = [{"idx": i, "outcome": "ACTION", "cause": None, "truth": SS, "predicted": SS,
                 "engine_action": None} for i in range(8)]
        rows[3]["predicted"] = BILL                       # wrong, by the twin
        rows[5]["outcome"] = "CONFLICT"                   # left
        rows[6]["cause"] = "ERROR"                        # its engine's answer counts
        rows[6]["engine_action"] = T1
        pair = {"born_at": 2, "queues": [SS, BILL]}
        got = TW.arrivals_in({"records": rows}, pair, region, space, corpus)
        in_region = [i for i in range(3, 8) if R.point_of(corpus[i], space) & region]
        self.assertEqual(got["arrivals"], len(in_region))
        self.assertEqual(got["left"], 1)
        self.assertGreaterEqual(got["wrong"], 2)
        self.assertGreaterEqual(got["by_twin"], 1)
        self.assertGreaterEqual(got["by_other"], 1)
        self.assertEqual(got["right"] + got["wrong"] + got["left"], got["arrivals"])


class TestGateOneOnARecord(unittest.TestCase):

    def test_on_k_r2(self):
        rec = json.loads(plan.run_path(plan.RANKED, 2).read_text())
        space = MI.space()
        self.assertTrue(TW.twins_of(rec, space)[2])
        moved = copy.deepcopy(rec)
        e = next(x for x in moved["escalations"]
                 if x["verdict"] == "nacida" and (x["calls"][0] or {}).get("copies"))
        e["copy_of"] = "R9999"
        self.assertFalse(TW.twins_of(moved, space)[2])


def run(births=20, twin_births=1, pairs=2, at_report=1, above=2, flipped=2, wrong=2,
        twin_above=0):
    return {"births": births, "twin_births": twin_births, "pairs": pairs,
            "twin_births_at_a_report": at_report,
            "fates": {TW.NEWBORN_ABOVE: above, TW.TWIN_ABOVE: twin_above},
            "verdicts": {TW.CP.WRONG: wrong}, "flipped": flipped}


def fake(**kw):
    return {"runs": {t: run(**kw) for t in TW.RUNS}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in TW.read_expectation(readings)}


CLAUSES = ["K1", "K2", "K3", "K4", "K5"]


class TestTheExpectation(unittest.TestCase):

    def test_five_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake(births=10, twin_births=2, pairs=2, at_report=1, above=1, flipped=1,
                         wrong=1, twin_above=1))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_one_run_and_the_pool(self):
        r = fake()
        r["runs"]["k_r2"] = run(births=10, twin_births=1)
        self.assertFalse(holds(r)["K5"])
        self.assertTrue(holds(r)["K1"])
        r = fake()
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {c: False for c in CLAUSES})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(twin_births=0, pairs=0, at_report=0, above=0, flipped=0, wrong=0))
        self.assertEqual(got, {"K1": False, "K2": False, "K3": False, "K4": False, "K5": True})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(TW, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                TW.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
