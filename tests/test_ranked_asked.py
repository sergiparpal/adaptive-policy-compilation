"""
`ranked/asked.py` — the POST-RUN reading of why L's twins are born at the
conflicts it asks about. No figure of the reading.

What is pinned is the instrument:
- the conflict twins read off a record built by hand over the real space: a
  twin born at a conflict is one, with every twin it has, while a twin born at
  a reported error and a copy of the same queue are not;
- the rules standing at a ticket when it arrived, before the birth there;
- which queue the newborn named against what stood;
- each conflict twin read at its ticket: a twin that stood, the newborn's queue
  another standing or not, right or wrong, and the reasoning's end kept;
- gates 2 and 3 with teeth: one queue standing, a row that was no conflict, a
  draft of another queue or region;
- the conditions of the births, by group, and their median;
- `twins.json`'s pairs born at a conflict;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import unittest
from fractions import Fraction
from unittest import mock

from manual import instrument as MI
from ranked import asked as AS
from ranked import plan

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SS, BILL, T1 = "SELF_SERVICE_DEFLECT", "BILLING_SPECIALIST", "T1_GENERAL"
# Tickets 2, 3 and 4 of the corpus are all `mobile`; ticket 3 alone is of
# severity 2.
MOBILE = [{"attr": "product", "op": "eq", "value": "mobile"}]
MOBILE_EVERY_TIER = [{"attr": "product", "op": "eq", "value": "mobile"},
                     {"attr": "customer_tier", "op": "in",
                      "value": ["free", "pro", "business", "enterprise"]}]
SEV2 = [{"attr": "severity", "op": "eq", "value": 2}]


def rule(rid, action, born_at, conditions):
    return {"rule_id": rid, "action": action, "born_at": born_at, "conditions": conditions,
            "beats": [], "loses_to": []}


def esc(idx, rid, copies, kind, action, conditions, reasoning=""):
    return {"idx": idx, "kind": kind, "verdict": "nacida", "rule_id": rid,
            "copy_of": copies[0] if copies else None,
            "calls": [{"copies": list(copies), "left_out": {}, "reasoning": reasoning,
                       "payload": {"action": action, "conditions": conditions}}]}


def record():
    """R3 twins R1 at a conflict; R4 twins R1 and R3 at another; R5 copies R1;
    R6 twins R2 at a reported error."""
    rules = [rule("R1", BILL, 1, MOBILE), rule("R2", SS, 2, SEV2), rule("R3", SS, 3, MOBILE),
             rule("R4", T1, 4, MOBILE_EVERY_TIER), rule("R5", BILL, 5, MOBILE),
             rule("R6", T1, 6, SEV2)]
    escs = [esc(1, "R1", [], "IMPASSE", BILL, MOBILE),
            esc(2, "R2", [], "IMPASSE", SS, SEV2),
            esc(3, "R3", ["R1"], plan.CONFLICT, SS, MOBILE, reasoning="x" * 1000),
            esc(4, "R4", ["R1", "R3"], plan.CONFLICT, T1, MOBILE, reasoning="the end"),
            esc(5, "R5", ["R1"], "ERROR", BILL, MOBILE),
            esc(6, "R6", ["R2"], "ERROR", T1, SEV2)]
    rows = [{"idx": i, "outcome": "ACTION", "truth": BILL, "truth_rule": "H12",
             "edge_reasons": []} for i in range(8)]
    rows[3]["outcome"] = rows[4]["outcome"] = plan.CONFLICT
    rows[4]["truth"] = T1
    return {"arm": "l", "rules": rules, "escalations": escs, "records": rows, "edge_log": []}


class TestTheConflictTwins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space = MI.space()

    def test_born_at_a_conflict(self):
        got = AS.conflict_twins(record(), self.space)
        self.assertEqual(list(got), ["R3", "R4"])
        self.assertEqual([p["twin"] for p in got["R3"]], ["R1"])
        self.assertEqual([p["twin"] for p in got["R4"]], ["R1", "R3"])

    def test_the_conditions_by_group(self):
        got = AS.conditions_beside(record(), self.space)
        self.assertEqual(got, {"conflict_twins": [1, 2], "other_twins": [1],
                               "no_twin": [1, 1, 1]})

    def test_the_median(self):
        self.assertEqual(AS.median_of([3, 1, 2]), Fraction(2))
        self.assertEqual(AS.median_of([1, 2, 3, 4]), Fraction(5, 2))
        self.assertIsNone(AS.median_of([]))


class TestWhatStood(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space, cls.corpus = MI.space(), list(MI.corpus())

    def test_before_each_birth(self):
        got = AS.standing_at(record(), {1, 2, 3, 4}, self.space, self.corpus)
        self.assertEqual(got, {1: {}, 2: {BILL: ["R1"]}, 3: {BILL: ["R1"], SS: ["R2"]},
                               4: {BILL: ["R1"], SS: ["R3"]}})

    def test_the_queue_named(self):
        here = {BILL: ["R1"], SS: ["R2"]}
        self.assertEqual(AS.named(SS, here), AS.ANOTHER)
        self.assertEqual(AS.named(T1, here), AS.NOT_STANDING)


class TestEachConflictTwin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space, cls.corpus = MI.space(), list(MI.corpus())

    def read(self, r, standing=None):
        births = AS.conflict_twins(r, self.space)
        standing = standing or AS.standing_at(r, {3, 4}, self.space, self.corpus)
        return AS.read_births(r, births, standing, self.space)

    def test_read_at_its_ticket(self):
        rows, was_conflict, drafts_ok = self.read(record())
        self.assertTrue(was_conflict)
        self.assertTrue(drafts_ok)
        r3, r4 = rows
        self.assertEqual((r3["queue"], r3["twin_stood"], r3["named"], r3["newborn_right"],
                          r3["twin_right"], r3["conditions"]),
                         (SS, True, AS.ANOTHER, False, True, 1))
        self.assertEqual((r3["reasoning_chars"], len(r3["tail"])), (1000, AS.TAIL))
        self.assertEqual((r4["queue"], r4["twin_stood"], r4["named"], r4["newborn_right"],
                          r4["twin_right"], r4["conditions"], r4["tail"]),
                         (T1, True, AS.NOT_STANDING, True, False, 2, "the end"))
        self.assertEqual([(t["rule"], t["stood"]) for t in r4["twins"]],
                         [("R1", True), ("R3", True)])

    def test_a_twin_that_did_not_stand(self):
        rows, _, _ = self.read(record(), standing={3: {BILL: ["R9"], SS: ["R2"]},
                                                   4: {BILL: ["R1"], SS: ["R2"]}})
        self.assertFalse(rows[0]["twin_stood"])
        self.assertEqual([t["stood"] for t in rows[1]["twins"]], [True, False])
        self.assertTrue(rows[1]["twin_stood"])

    def test_gate_two_has_teeth(self):
        r = record()
        self.assertFalse(self.read(r, standing={3: {BILL: ["R1"]},
                                                4: {BILL: ["R1"], SS: ["R3"]}})[1])
        r["records"][4]["outcome"] = "ACTION"
        self.assertFalse(self.read(r)[1])

    def test_gate_three_has_teeth(self):
        r = record()
        r["escalations"][2]["calls"][0]["payload"]["action"] = T1
        self.assertFalse(self.read(r)[2])
        r = record()
        r["escalations"][3]["calls"][0]["payload"]["conditions"] = SEV2
        self.assertFalse(self.read(r)[2])
        r = record()
        r["escalations"][3]["calls"][0]["payload"] = None
        self.assertFalse(self.read(r)[2])


class TestTheKeptPairs(unittest.TestCase):

    def test_born_at_a_conflict(self):
        def p(n, t, kind):
            return {"newborn": n, "twin": t, "newborn_birth": {"kind": kind}}
        twins = {"readings": {"runs": {"l_r1": {"pairs_list": [
            p("R4", "R3", plan.CONFLICT), p("R3", "R1", plan.CONFLICT), p("R6", "R2", "ERROR"),
            p("R4", "R1", plan.CONFLICT)]}}}}
        self.assertEqual(AS.pairs_kept(twins, "l_r1"),
                         [("R3", "R1"), ("R4", "R1"), ("R4", "R3")])


def birth(stood=True, named=AS.ANOTHER, right=False):
    return {"twin_stood": stood, "named": named, "newborn_right": right}


def fake(births=None, conflict=1, no_twin=2):
    births = births if births is not None else [birth(), birth(), birth(False, AS.NOT_STANDING,
                                                                        True)]
    f = AS.frac
    return {"runs": {t: {"births": copy.deepcopy(births)} for t in AS.L_RUNS},
            "conditions": {"conflict_twins_median": f(Fraction(conflict)) if conflict else None,
                           "no_twin_median": f(Fraction(no_twin)) if no_twin else None}}


def holds(readings) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in AS.read_expectation(readings)}


CLAUSES = ["M1", "M2", "M3", "M4"]


class TestTheExpectation(unittest.TestCase):

    def test_four_clauses(self):
        self.assertEqual(list(holds(fake())), CLAUSES)

    def test_inside_the_lines(self):
        self.assertEqual(holds(fake()), {c: True for c in CLAUSES})

    def test_at_the_lines(self):
        got = holds(fake([birth(True, AS.ANOTHER, True), birth(False, AS.NOT_STANDING, False)],
                         conflict=2, no_twin=2))
        self.assertEqual(got, {c: False for c in CLAUSES})

    def test_pooled(self):
        r = fake()
        r["runs"]["l_r2"]["births"] = [birth(False, AS.NOT_STANDING, True)]
        self.assertEqual(holds(r), {c: True for c in CLAUSES})
        r = fake()
        del r["runs"]["l_r1"]
        self.assertEqual(holds(r), {c: False for c in CLAUSES})

    def test_over_nothing(self):
        self.assertEqual(holds({}), {c: False for c in CLAUSES})
        self.assertEqual(holds(fake([])), {"M1": False, "M2": False, "M3": False, "M4": True})
        self.assertFalse(holds(fake(conflict=None))["M4"])
        self.assertFalse(holds(fake(no_twin=None))["M4"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(AS, "read_inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                AS.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
