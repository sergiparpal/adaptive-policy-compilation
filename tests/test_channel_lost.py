"""
`channel/lost.py` — the POST-RUN reading of why c r1 lost `SECURITY_INCIDENT`,
no figure.

What is pinned is the instrument, on a base worked by hand:
- every way a point of the queue is lost, each on a ticket chosen for it: an
  impasse, a conflict contested or not, unwritten, and outranked by an edge or
  by containment;
- the ways partitioning the queue's points;
- an edge between two rules of the queue not counted as an edge against it;
- the winners and the queue's rules with their births;
- the replay's final base the rebuild's, and its curve ending at the base;
- the escalations' verdicts and gate 4;
- the expectation's clauses at their edges;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from blind import rows as brows
from channel import lost as L
from channel import plan
from harness.domain import ATTRIBUTES, Case
from manual import instrument as MI
from rung2.engine2 import EDGE_OK, Space

SPACE = Space()
SI, T2, T3, AM = "SECURITY_INCIDENT", "T2_TECHNICAL", "T3_ENGINEERING", "ACCOUNT_MANAGER"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


def ticket(**over):
    base = dict(has_security_keyword=True, severity=3, customer_tier="enterprise",
                product="api", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


def point(case):
    m = SPACE.full
    for a in ATTRIBUTES:
        m &= SPACE.mask[a][getattr(case, a)]
    return m


def ext(rule):
    return brows.ext_of(rule, SPACE)


# The queue's rules: S1 for keyword enterprise tickets, S2 for keyword severity-2
# ones. Against them: a broad keyword rule of T2, a rule of AM that beats S1 by an
# edge, and a rule of T3 nested inside S1.
S1 = r_("S1", 0, SI, has_security_keyword=True, customer_tier="enterprise")
T = r_("T", 1, T2, has_security_keyword=True)
A = r_("A", 2, AM, customer_tier="enterprise", product="billing")
X = r_("X", 3, T3, has_security_keyword=True, customer_tier="enterprise", severity=1)
S2 = r_("S2", 4, SI, has_security_keyword=True, severity=2)
S3 = r_("S3", 5, SI, has_security_keyword=True, customer_tier="enterprise",
        product="billing", channel="phone")

# The queue's true points in this base: keyword enterprise or business tickets,
# and the non-keyword pro mobile ones, which no rule reaches.
TRUTH = (ext(r_("", 0, SI, has_security_keyword=True, customer_tier="enterprise"))
         | ext(r_("", 0, SI, has_security_keyword=True, customer_tier="business"))
         | ext(r_("", 0, SI, has_security_keyword=False, customer_tier="pro",
                  product="mobile")))


def record(edges=(("A", "S1", EDGE_OK),), extra_rules=(), escalations=()):
    rules = [S1, T, A, X, S2, *extra_rules]
    rows = [{"idx": r["born_at"], "cause": "ERROR", "truth": SI, "truth_rule": "H01",
             "escalated": True, "edge_reasons": []} for r in rules]
    for w, l, why in edges:
        born = max(int(r["born_at"]) for r in rules if r["rule_id"] in (w, l))
        next(row for row in rows if row["idx"] == born)["edge_reasons"].append(why)
    rows.sort(key=lambda row: row["idx"])
    return {"rules": rules, "records": rows, "edge_log": [list(e) for e in edges],
            "escalations": list(escalations)}


def engine_of(rec):
    return L.replay(rec, SPACE, TRUTH)["engine"]


class TestTheWays(unittest.TestCase):

    def setUp(self):
        self.rec = record()
        self.w = L.ways(engine_of(self.rec), TRUTH)

    def where(self, **over):
        p = point(ticket(**over))
        return [k for k in ("right",) + L.WAYS + ("contested", "by_edge", "by_containment")
                if self.w[k] & p]

    def test_each_way_on_its_ticket(self):
        self.assertEqual(self.where(), ["right"])
        self.assertEqual(self.where(product="billing"), ["outranked", "by_edge"])
        self.assertEqual(self.where(severity=1), ["outranked", "by_containment"])
        self.assertEqual(self.where(customer_tier="business"), ["unwritten"])
        self.assertEqual(self.where(has_security_keyword=False, customer_tier="pro",
                                    product="mobile"), ["impasse"])
        self.assertEqual(self.where(product="billing", severity=2), ["conflict", "contested"])
        self.assertEqual(self.where(product="billing", severity=1), ["conflict"])

    def test_a_point_off_the_queue_is_in_no_way(self):
        self.assertEqual(self.where(customer_tier="free"), [])

    def test_the_ways_partition_the_queue(self):
        self.assertTrue(L.partitions(self.w, TRUTH))
        broken = dict(self.w, unwritten=0)
        self.assertFalse(L.partitions(broken, TRUTH))

    def test_the_wrong_queues(self):
        self.assertEqual(sorted(self.w["wrong"]), sorted([T2, T3, AM]))
        c = L.counts(self.w)
        self.assertEqual(c["lost"], TRUTH.bit_count() - c["right"])
        self.assertEqual(sum(c[k] for k in L.WAYS), c["lost"])
        self.assertEqual(c["by_edge"] + c["by_containment"], c["outranked"])

    def test_an_edge_inside_the_queue_is_not_an_edge_against_it(self):
        w = L.ways(engine_of(record(edges=(("A", "S1", EDGE_OK), ("S3", "S2", EDGE_OK)),
                                    extra_rules=(S3,))), TRUTH)
        self.assertEqual(L.edge_beaten(engine_of(record()), SI),
                         L.edge_beaten(engine_of(record(edges=(("A", "S1", EDGE_OK),
                                                              ("S3", "S2", EDGE_OK)),
                                                       extra_rules=(S3,))), SI))
        self.assertTrue(L.partitions(w, TRUTH))

    def test_without_the_edge_the_billing_ticket_is_contested(self):
        w = L.ways(engine_of(record(edges=())), TRUTH)
        p = point(ticket(product="billing"))
        self.assertTrue(w["contested"] & p)
        self.assertFalse(w["by_edge"])


class TestTheRules(unittest.TestCase):

    def test_winners_and_the_queues_rules(self):
        rec = record()
        eng = engine_of(rec)
        w = L.ways(eng, TRUTH)
        win = {x["rule_id"]: x for x in L.winners(eng, rec, w)}
        self.assertEqual(sorted(win), ["A", "T", "X"])
        self.assertEqual(win["T"]["unwritten"], win["T"]["lost_points"])
        self.assertEqual(win["A"]["cause"], "ERROR")
        qr = L.queue_rules(eng, rec, w, TRUTH, {"H01": ext(S1)})
        self.assertEqual([q["rule_id"] for q in qr], ["S1", "S2"])
        self.assertEqual(qr[0]["is_listed_region"], "H01")
        self.assertIsNone(qr[1]["is_listed_region"])
        self.assertEqual(qr[0]["queue_points"], (ext(S1) & TRUTH).bit_count())


class TestTheReplay(unittest.TestCase):

    def test_the_replay_is_the_rebuild_and_the_curve_ends_at_the_base(self):
        rec = record()
        rep = L.replay(rec, SPACE, TRUTH)
        self.assertTrue(L.same_base(rep["engine"], MI.final_engine(rec)))
        final = L.ways(rep["engine"], TRUTH)["right"].bit_count()
        self.assertEqual(rep["curve"][-1]["right"], final)
        self.assertEqual(sum(c["delta"] for c in rep["curve"]), final)
        self.assertEqual([c["born_at"] for c in rep["curve"]], [0, 1, 2, 3, 4])
        # S1 alone decides its points; A's edge then takes the billing ones.
        self.assertEqual(rep["curve"][0]["right"], (ext(S1) & TRUTH).bit_count())
        self.assertLess(rep["curve"][2]["delta"], 0)

    def test_a_different_graph_is_not_the_base(self):
        a = engine_of(record())
        b = engine_of(record(edges=()))
        self.assertFalse(L.same_base(a, b))


class TestTheEscalations(unittest.TestCase):

    def esc(self, idx, verdict, rule_id, conds=None):
        payload = {"action": SI, "conditions": conds if conds is not None else
                   [{"attr": "has_security_keyword", "op": "eq", "value": True}]}
        return {"idx": idx, "verdict": verdict, "rule_id": rule_id,
                "calls": [{"payload": payload}], "listed": ["T", "A"]}

    def test_the_verdicts_and_the_drafts(self):
        rec = record(escalations=[self.esc(0, L.BORN, "S1"),
                                  self.esc(4, L.UNPLACED, None),
                                  self.esc(2, L.BORN, "A", conds=[{"attr": "nope"}])])
        eng = engine_of(rec)
        got = L.escalations(rec, eng, SPACE, TRUTH)
        self.assertEqual([e["verdict"] for e in got], [L.BORN, L.UNPLACED, L.BORN])
        self.assertEqual(got[0]["draft_queue_points"],
                         (ext(r_("", 0, SI, has_security_keyword=True)) & TRUTH).bit_count())
        self.assertIsNone(got[2]["draft_queue_points"])
        self.assertEqual(got[0]["listed"], 2)
        self.assertTrue(L.escalations_are_the_record(got))

    def test_gate_4_fails(self):
        rec = record(escalations=[self.esc(0, L.BORN, "R9999")])
        self.assertFalse(L.escalations_are_the_record(
            L.escalations(rec, engine_of(rec), SPACE, TRUTH)))
        rec = record(escalations=[self.esc(0, "otra", "S1")])
        self.assertFalse(L.escalations_are_the_record(
            L.escalations(rec, engine_of(rec), SPACE, TRUTH)))
        rec = record(escalations=[self.esc(0, L.BORN, "S1")])
        rec["records"][0]["escalated"] = False
        self.assertFalse(L.escalations_are_the_record(
            L.escalations(rec, engine_of(rec), SPACE, TRUTH)))

    def test_a_ticket_of_another_queue_is_not_read(self):
        rec = record(escalations=[self.esc(0, L.BORN, "S1")])
        rec["records"][0]["truth"] = T2
        self.assertEqual(L.escalations(rec, engine_of(rec), SPACE, TRUTH), [])


def run_(lost=100, unwritten=50, t2=50, widest=49, born=10, most=49, n=100):
    return {"queue_points": n,
            "ways": {"lost": lost, "unwritten": unwritten,
                     "lost_by_queue": {T2: t2}},
            "queue_rules": [{"queue_points": widest}],
            "escalation_verdicts": {L.BORN: born}, "escalations": [{}] * 13,
            "curve": {"most_right": most, "at_birth": 7}}


class TestTheExpectation(unittest.TestCase):

    def holds(self, mine, others):
        runs = {"c_r1": mine, **{f"o{i}": o for i, o in enumerate(others)}}
        return [c["holds"] for c in L.read_expectation(runs, "c_r1")]

    def test_clause_by_clause_at_their_edges(self):
        broad = run_(widest=50)
        self.assertEqual(self.holds(run_(), [broad] * 5), [True] * 6)
        self.assertEqual(self.holds(run_(unwritten=49, t2=49, widest=50, born=9, most=50),
                                    [broad] * 4 + [run_(widest=49)]), [False] * 6)

    def test_a_run_that_lost_nothing_holds_neither_l1_nor_l2(self):
        x = self.holds(run_(lost=0, unwritten=0, t2=0), [run_(widest=50)])
        self.assertEqual(x[:2], [False, False])

    def test_the_lines(self):
        self.assertEqual((L.L_HALF, L.L4_BORN, L.QUEUE, L.RUN),
                         (Fraction(1, 2), 10, SI, ("c", 1)))


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
                    L.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
