"""
`rung3/copy_births.py` — why rung 1's loop wrote the same rule again, no figure.

**No count is pinned here.** The figures live in `results3/copy_births.json` and
in `results3/FINDINGS3.md` §19. What is pinned is the instrument, on a small run
worked by hand:

  * the replay gives a run back, and gate 1 catches a record it does not give
    back; gate 2 catches a rule off its case and a case that bore two;
  * a later copy born in its group's own tie, with a finalist outside the group
    or with every finalist inside it, and one born in someone else's tie;
  * whether a tie recurs, what each group's CONFLICTs bore, what it decided;
  * the summary's counts, and the expectation's clauses at their edges;
  * added after the first run: each rule born on a CONFLICT placed above, at
    or below the tie that bore it.
"""

from __future__ import annotations

import copy
import unittest

from harness.domain import Case

from rung3 import copy_births as cb
from rung3.identical_rules import groups, written

T1, T2, BILL = "T1_GENERAL", "T2_TECHNICAL", "BILLING_SPECIALIST"


def case(**over) -> Case:
    base = dict(has_security_keyword=False, severity=2, customer_tier="pro",
                product="api", channel="email", prior_tickets_30d=0, off_hours=False,
                language="en")
    return Case(**(base | over))


def cond(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


BILLING = [cond("product", "eq", "billing")]

# The run, case by case: what the engine decides with the base as it stands,
# and the rule the escalation bore. Worked by hand from rung 1's arbitration.
CORPUS = [
    case(customer_tier="free"),                          # 0 IMPASSE -> B
    case(product="billing"),                             # 1 IMPASSE -> A
    case(customer_tier="free", product="billing"),       # 2 A vs B -> A2, own, outside
    case(customer_tier="free", product="billing"),       # 3 A, A2 vs B -> A3, own, outside
    case(product="billing"),                             # 4 A, A2 vs A3 -> A5, own, inside
    case(product="billing", severity=4),                 # 5 the group's tie -> C
    case(product="billing", severity=4),                 # 6 C decides, more specific
    case(severity=4),                                    # 7 IMPASSE -> D
    case(product="billing", severity=4),                 # 8 C vs D -> A4, other's tie
    case(customer_tier="free"),                          # 9 B decides
]
RULES = [   # rule_id, conditions, action, born_at, fire_count, correct_count
    ("R0001", [cond("customer_tier", "eq", "free")], T1, 0, 1, 1),
    ("R0002", BILLING, BILL, 1, 0, 0),
    ("R0003", BILLING, BILL, 2, 0, 0),
    ("R0004", BILLING, T1, 3, 0, 0),
    ("R0005", BILLING, BILL, 4, 0, 0),
    ("R0006", [cond("product", "eq", "billing"), cond("severity", "eq", 4)], T2, 5, 1, 1),
    ("R0007", [cond("customer_tier", "eq", "pro"), cond("severity", "eq", 4)], T1, 7, 0, 0),
    ("R0008", BILLING, BILL, 8, 0, 0),
]
DECISIONS = [   # outcome, winner, n_matched (the finalists, on a CONFLICT), truth
    ("IMPASSE", None, 0, T1), ("IMPASSE", None, 0, BILL), ("CONFLICT", None, 2, T1),
    ("CONFLICT", None, 3, T1), ("CONFLICT", None, 3, BILL), ("CONFLICT", None, 4, T2),
    ("ACTION", "R0006", 5, T2), ("IMPASSE", None, 0, T1), ("CONFLICT", None, 2, T2),
    ("ACTION", "R0001", 1, T1),
]


def the_record() -> dict:
    return {
        "rules": [{"rule_id": r, "conditions": c, "action": a, "born_at": b,
                   "fire_count": f, "correct_count": k, "note": ""}
                  for r, c, a, b, f, k in RULES],
        "records": [{"idx": i, "outcome": o, "winner_id": w, "n_matched": n, "truth": t}
                    for i, (o, w, n, t) in enumerate(DECISIONS)],
    }


class TheRun(unittest.TestCase):

    def setUp(self):
        self.record = the_record()
        self.engine, self.cases, self.problems = cb.replay(self.record, CORPUS)
        self.spec = {r.rule_id: r.specificity for r in self.engine.rules}
        self.gs = groups({d["rule_id"]: written(d["conditions"]) for d in self.record["rules"]})


class TestTheReplay(TheRun):

    def test_it_gives_the_run_back(self):
        self.assertEqual(self.problems, [])
        self.assertTrue(cb.same_as_record(self.record, self.engine, self.cases)["passes"])
        self.assertEqual(self.cases[2]["finalists"], ["R0001", "R0002"])
        self.assertEqual(self.cases[8]["finalists"], ["R0006", "R0007"])
        self.assertEqual([c["born"] for c in self.cases],
                         ["R0001", "R0002", "R0003", "R0004", "R0005", "R0006", None,
                          "R0007", "R0008", None])

    def test_gate_1_catches_a_record_it_does_not_give_back(self):
        for tamper in (lambda r: r["records"][6].update(winner_id="R0002"),
                       lambda r: r["records"][4].update(n_matched=2),
                       lambda r: r["rules"][0].update(correct_count=0)):
            record = copy.deepcopy(self.record)
            tamper(record)
            engine, cases, _ = cb.replay(record, CORPUS)
            with self.subTest(tamper=tamper):
                self.assertFalse(cb.same_as_record(record, engine, cases)["passes"])

    def test_gate_2_catches_a_rule_off_its_case_and_a_case_that_bore_two(self):
        record = copy.deepcopy(self.record)
        record["rules"][1]["born_at"] = 0              # A does not match case 0
        _, _, problems = cb.replay(record, CORPUS)
        self.assertTrue(any(p.startswith("R0002") for p in problems))
        record = copy.deepcopy(self.record)
        record["rules"][2]["born_at"] = 3              # two rules at case 3
        _, _, problems = cb.replay(record, CORPUS)
        self.assertTrue(any("bore" in p for p in problems))

    def test_the_gates(self):
        gates = cb.check(self.record, self.engine, self.cases, self.problems, self.gs,
                         [["R0002", "R0003", "R0004", "R0005", "R0008"]], self.spec)
        self.assertEqual([g["passes"] for g in gates], [True, True, True, True])
        gates = cb.check(self.record, self.engine, self.cases, self.problems, self.gs,
                         [["R0002", "R0003"]], self.spec)
        self.assertFalse(gates[2]["passes"])


class TestWhatBoreEachRule(TheRun):

    def rows(self):
        return {r["rule"]: r for r in cb.births(self.record, self.cases, self.gs, self.spec)}

    def test_alone_first_and_later(self):
        rows = self.rows()
        self.assertEqual([(rows[r]["trigger"], rows[r]["status"]) for r in sorted(rows)],
                         [("IMPASSE", "alone"), ("IMPASSE", "first"), ("CONFLICT", "later"),
                          ("CONFLICT", "later"), ("CONFLICT", "later"), ("CONFLICT", "alone"),
                          ("IMPASSE", "alone"), ("CONFLICT", "later")])

    def test_own_tie_outside_and_inside_and_others_tie(self):
        rows = self.rows()
        self.assertEqual((rows["R0003"]["own"], rows["R0003"]["outside"]), (True, True))
        self.assertEqual((rows["R0004"]["own"], rows["R0004"]["outside"]), (True, True))
        self.assertEqual((rows["R0005"]["own"], rows["R0005"]["outside"]), (True, False))
        self.assertEqual((rows["R0008"]["own"], rows["R0008"]["outside"]), (False, None))
        self.assertEqual(rows["R0008"]["finalists"], [["R0006", T2, 2], ["R0007", T1, 2]])

    def test_a_tie_recurs(self):
        rows = self.rows()
        self.assertEqual([rows[r]["recurs"] for r in ("R0003", "R0004", "R0005", "R0008")],
                         [True, True, True, None])
        self.assertFalse(cb.recurs(self.cases[6:], {"R0002"}))

    def test_what_the_groups_conflicts_bore(self):
        (g,) = cb.per_group(self.gs, self.cases, self.record, self.spec)
        self.assertEqual((g["queues"], g["specificity"], g["conflicts"], g["bore_a_copy"],
                          g["bore_another_rule"], g["bore_nothing"], g["decided"]),
                         ([BILL, T1], 1, 4, 3, 1, 0, 0))

    def test_the_summary_and_the_expectation_at_its_edges(self):
        s = cb.summary(cb.births(self.record, self.cases, self.gs, self.spec), self.engine)
        self.assertEqual((s["later_copies"], s["on_a_conflict"], s["own_tie"],
                          s["own_tie_outside"], s["own_tie_inside"], s["others_tie"],
                          s["own_tie_recurs"], s["later_copies_that_fired"]),
                         (4, 4, 3, 2, 1, 1, 3, 0))
        self.assertEqual((s["dead_rules"], s["dead_later_copies"]), (6, 4))
        x = cb.read_expectation(s)
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])
        self.assertEqual(x[1]["reading"], 0.75)            # clause 2 at its line
        worse = s | {"on_a_conflict": 3, "own_tie": 2, "own_tie_outside": 0,
                     "own_tie_recurs": 1, "later_copies_that_fired": 1}
        self.assertEqual([c["holds"] for c in cb.read_expectation(worse)],
                         [False, False, False, False, False])
        none = s | {"later_copies": 0, "own_tie": 0}
        self.assertEqual([c["holds"] for c in cb.read_expectation(none)][1:4],
                         [None, None, None])


class TestAgainstTheTie(TheRun):
    """Added after the first run: each rule born on a CONFLICT placed against
    the finalists that bore it."""

    def test_above_at_and_below(self):
        rows = cb.births(self.record, self.cases, self.gs, self.spec)
        places = {r["rule"]: cb.place(r) for r in rows}
        self.assertEqual(places, {"R0001": None, "R0002": None, "R0003": "at",
                                  "R0004": "at", "R0005": "at", "R0006": "above",
                                  "R0007": None, "R0008": "below"})
        a = cb.against_the_tie(rows)
        self.assertEqual((a["born_on_a_conflict"], a["by_place"]),
                         (5, {"above": 1, "at": 3, "below": 1}))
        self.assertEqual(a["by_status_and_place"]["later"], {"above": 0, "at": 3, "below": 1})
        self.assertEqual(a["by_status_and_place"]["alone"], {"above": 1, "at": 0, "below": 0})
        self.assertEqual(a["later_copies_below"],
                         {"rules": 1, "conditions_short": {"1": 1},
                          "their_queue_is_a_tied_queue": 0})
        self.assertEqual(a["queue_true_at_birth"],
                         {"alone": [3, 3], "first": [1, 1], "later": [2, 4]})


if __name__ == "__main__":
    unittest.main()
