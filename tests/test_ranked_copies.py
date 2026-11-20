"""
`ranked/copies.py` — the POST-RUN reading of copies of the same queue. No figure
of the reading.

What is pinned is the instrument:
- the copies read off a record built by hand over the real space: a rule of the
  same queue recorded among the first call's `copies` is an original, one of
  another queue is not, and gate 1 fails on an original whose region differs;
- the rule that erred, nested in the copy or not, and none at a conflict;
- what each engine decides at one point, rung 2's and the ranking's;
- each copy at its birth, on a record the walk replays: an original that stood
  or did not, and the copy standing, deciding, or left in conflict;
- each copy in a final base built by hand;
- the replay without the copies: with nothing left out it is the base (gate 3),
  and a copy left out takes its edges with it;
- what the copies cost, read off a replay;
- gate 1 with teeth on K r2's record;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import json
import unittest
from types import SimpleNamespace
from unittest import mock

from manual import instrument as MI
from ranked import copies as CO
from ranked import engine as E
from ranked import plan
from ranked import reading as R
from ranked import readings as RD

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SS, BILL, T1 = "SELF_SERVICE_DEFLECT", "BILLING_SPECIALIST", "T1_GENERAL"
# Tickets 2, 3 and 4 of the corpus are all `mobile`; ticket 3 alone is `pro` and
# of severity 2.
MOBILE = [{"attr": "product", "op": "eq", "value": "mobile"}]
MOBILE_PRO = [{"attr": "product", "op": "eq", "value": "mobile"},
              {"attr": "customer_tier", "op": "eq", "value": "pro"}]
SEV2 = [{"attr": "severity", "op": "eq", "value": 2}]


def rule(rid, action, born_at, conditions, beats=()):
    return {"rule_id": rid, "action": action, "born_at": born_at, "conditions": conditions,
            "beats": list(beats), "loses_to": []}


def esc(idx, rid, copies, kind="ERROR"):
    return {"idx": idx, "kind": kind, "verdict": "nacida", "rule_id": rid,
            "copy_of": copies[0] if copies else None,
            "calls": [{"copies": list(copies), "left_out": {}}]}


def rows(n=8, truth=BILL):
    return [{"idx": i, "truth": truth, "truth_rule": "H12", "engine_rule": None,
             "edge_reasons": []} for i in range(n)]


def nested_record(arm="l"):
    """R2, of another queue, lies strictly inside R1 and R3: it erred at R3's
    ticket and keeps it from both."""
    r = {"arm": arm, "rules": [rule("R1", BILL, 1, MOBILE), rule("R2", SS, 2, MOBILE_PRO),
                               rule("R3", BILL, 3, MOBILE)],
         "escalations": [esc(1, "R1", [], kind="IMPASSE"), esc(2, "R2", [], kind="IMPASSE"),
                         esc(3, "R3", ["R1"])],
         "records": rows(), "edge_log": [], "reports_handed": {"3": BILL}}
    r["records"][3]["engine_rule"] = "R2"
    return r


def conflict_record(arm="l", edge=False):
    """R2, of another queue, crosses R1 and R3 at R3's ticket, a conflict; with
    `edge`, R3's birth installs R3 above R2."""
    r = {"arm": arm, "rules": [rule("R1", BILL, 1, MOBILE), rule("R2", SS, 2, SEV2),
                               rule("R3", BILL, 3, MOBILE, beats=["R2"] if edge else [])],
         "escalations": [esc(1, "R1", [], kind="IMPASSE"), esc(2, "R2", [], kind="IMPASSE"),
                         esc(3, "R3", ["R1"], kind="CONFLICT")],
         "records": rows(), "edge_log": [["R3", "R2", "ok"]] if edge else []}
    if edge:
        r["records"][3]["edge_reasons"] = ["ok"]
    return r


class TestTheCopies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()

    def test_a_copy_and_what_erred(self):
        got, ok = CO.copies_of_run(nested_record(), self.space)
        self.assertTrue(ok)
        self.assertEqual([c["rule_id"] for c in got], ["R3"])
        c = got[0]
        self.assertEqual((c["originals"], c["kind"], c["report"], c["erring"], c["erring_queue"],
                          c["erring_nested"]), (["R1"], "ERROR", BILL, "R2", SS, True))

    def test_another_queue_is_no_original(self):
        r = nested_record()
        r["rules"][2]["action"] = T1
        self.assertEqual(CO.copies_of_run(r, self.space)[0], [])

    def test_no_rule_erred_at_a_conflict(self):
        got, ok = CO.copies_of_run(conflict_record(), self.space)
        self.assertTrue(ok)
        self.assertEqual((got[0]["kind"], got[0]["erring"], got[0]["erring_nested"]),
                         ("CONFLICT", None, False))

    def test_an_erring_rule_not_inside(self):
        r = nested_record()
        r["rules"][1]["conditions"] = SEV2
        self.assertFalse(CO.copies_of_run(r, self.space)[0][0]["erring_nested"])

    def test_gate_one_has_teeth(self):
        r = nested_record()
        r["rules"][0]["conditions"] = SEV2
        self.assertFalse(CO.copies_of_run(r, self.space)[1])


def base(own, queues, ranking=(), und=None):
    return {"own": own, "queues": queues, "ranking": tuple(ranking),
            "walk": SimpleNamespace(und=und or {})}


class TestWhatAnEngineDecides(unittest.TestCase):

    def test_by_rung_two(self):
        self.assertEqual(CO.decision_at(base("rung2", {SS: 0b01, BILL: 0b10}, (BILL, SS)), 0b01),
                         SS)
        self.assertIsNone(CO.decision_at(base("rung2", {SS: 0b11, BILL: 0b01}, (BILL, SS)), 0b01))
        self.assertIsNone(CO.decision_at(base("rung2", {SS: 0b10}, (BILL, SS)), 0b01))

    def test_by_the_ranking(self):
        b = base("ranked", {SS: 0b11, BILL: 0b01, T1: 0b01}, (T1, BILL, SS))
        self.assertEqual(CO.decision_at(b, 0b01), T1)
        self.assertEqual(CO.decision_at(b, 0b10), SS)
        self.assertIsNone(CO.decision_at(b, 0b100))


class TestAtTheirBirth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space, cls.corpus = MI.space(), list(MI.corpus())

    def at(self, record):
        copies, _ = CO.copies_of_run(record, self.space)
        return CO.at_birth(record, copies, self.space, self.corpus)["R3"]

    def test_kept_out_by_a_nested_rule(self):
        self.assertEqual(self.at(nested_record()), {"original_stood": False, "stands": False,
                                                   "decision": SS, "decides": False})

    def test_left_in_conflict(self):
        self.assertEqual(self.at(conflict_record()), {"original_stood": True, "stands": True,
                                                     "decision": None, "decides": False})

    def test_the_ranking_decides_in_k(self):
        first = next(q for q in E.Tally().ranking if q in (BILL, SS))
        got = self.at(conflict_record(arm=plan.RANKED))
        self.assertEqual((got["decision"], got["decides"]), (first, first == BILL))

    def test_its_edge_decides(self):
        self.assertEqual(self.at(conflict_record(edge=True)),
                         {"original_stood": True, "stands": True, "decision": BILL,
                          "decides": True})


class TestInTheFinalBase(unittest.TestCase):

    def test_each_copy(self):
        space, corpus = MI.space(), list(MI.corpus())
        p3, p4 = R.point_of(corpus[3], space), R.point_of(corpus[4], space)
        copies = [{"rule_id": "R3", "queue": BILL, "born_at": 3, "truth": BILL,
                   "originals": ["R1"]},
                  {"rule_id": "R4", "queue": BILL, "born_at": 4, "truth": SS,
                   "originals": ["R1"]}]
        und = {"R1": p4, "R3": p3, "R4": p4, "R2": p4}
        got = CO.in_final(base("rung2", {BILL: p3 | p4, SS: p4}, (BILL, SS), und),
                          copies, space, corpus)
        self.assertEqual(got, [
            {"rule_id": "R3", "decision": BILL, "stands": True, "decides": True,
             "original_stands": False, "right": True},
            {"rule_id": "R4", "decision": None, "stands": True, "decides": False,
             "original_stands": True, "right": False}])
        got = CO.in_final(base("ranked", {BILL: p3 | p4, SS: p4}, (SS, BILL), und),
                          copies, space, corpus)
        self.assertEqual([(x["decision"], x["decides"], x["right"]) for x in got],
                         [(BILL, True, True), (SS, False, True)])


class TestTheReplay(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()
        cls.mobile = cls.space.extension([CO.TW.Condition(**c) for c in MOBILE])
        cls.both = cls.mobile & cls.space.extension([CO.TW.Condition(**c) for c in SEV2])
        cls.truth = {BILL: cls.mobile}

    def test_nothing_left_out_is_the_base(self):
        for r in (nested_record(), conflict_record(), conflict_record(edge=True),
                  conflict_record(arm=plan.RANKED, edge=True)):
            got = CO.replay_without(r, self.space, self.truth, set())
            self.assertEqual(got["right"], RD.base_of(r, self.space, self.truth)["right"])
            self.assertEqual(got["rules"], 3)

    def test_a_copy_takes_its_edges(self):
        r = conflict_record(edge=True)
        self.assertEqual(CO.replay_without(r, self.space, self.truth, set())["right"],
                         self.mobile)
        got = CO.replay_without(r, self.space, self.truth, {"R3"})
        self.assertEqual((got["right"], got["rules"]), (self.mobile & ~self.both, 2))

    def test_everything_left_out(self):
        got = CO.replay_without(conflict_record(), self.space, self.truth, {"R1", "R2", "R3"})
        self.assertEqual(got, {"right": 0, "rules": 0})


class TestTheCost(unittest.TestCase):

    def test_read_off_a_replay(self):
        with mock.patch.object(CO, "replay_without", return_value={"right": 0b1011, "rules": 5}):
            got = CO.cost({}, {"right": 0b0111}, [{"rule_id": "R3"}], None, {}, 0b0011)
        self.assertEqual(got, {"final": {"right": 3, "halves": [2, 1]},
                               "without": {"right": 3, "rules": 5, "halves": [2, 1]},
                               "change": 0, "gained_without": 1, "lost_without": 1})


class TestGateOneOnARecord(unittest.TestCase):

    def test_on_k_r2(self):
        rec = json.loads(plan.run_path(plan.RANKED, 2).read_text())
        space = MI.space()
        got, ok = CO.copies_of_run(rec, space)
        self.assertTrue(ok)
        moved = copy.deepcopy(rec)
        original = got[0]["originals"][0]
        r = next(x for x in moved["rules"] if x["rule_id"] == original)
        r["conditions"] = r["conditions"][:-1] if len(r["conditions"]) > 1 else SEV2
        self.assertFalse(CO.copies_of_run(moved, space)[1])


def run(copies=10, at_report=6, nested=4, decide=4, change=0):
    return {"copies": copies, "at_a_report": at_report, "erring_nested": nested,
            "decide_their_ticket": decide, "cost": {"change": change}}


def fake(**kw):
    return {"runs": {t: run(**kw) for t in CO.RUNS}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in CO.read_expectation(readings)}


CLAUSES = ["L1", "L2", "L3", "L4"]


class TestTheExpectation(unittest.TestCase):

    def test_four_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})
        self.assertTrue(holds(fake(change=-1343))["L4"])

    def test_at_the_lines(self):
        got = holds(fake(copies=12, at_report=6, nested=3, decide=6, change=1344))
        self.assertEqual(got, {c: False for c in CLAUSES})
        self.assertFalse(holds(fake(change=-1344))["L4"])

    def test_one_run_and_the_pool(self):
        r = fake()
        r["runs"]["k_r2"] = run(decide=6, change=2000)
        got = holds(r)
        self.assertEqual(got, {"L1": True, "L2": True, "L3": False, "L4": False})
        r = fake()
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {c: False for c in CLAUSES})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        got = holds(fake(copies=0, at_report=0, nested=0, decide=0))
        self.assertEqual(got, {"L1": False, "L2": False, "L3": False, "L4": True})
        r = fake()
        r["runs"]["l_r3"]["cost"] = {"change": None}
        self.assertFalse(holds(r)["L4"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(CO, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                CO.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
