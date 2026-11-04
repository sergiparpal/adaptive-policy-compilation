"""
`reasoned_loop/governed.py` — the POST-RUN reading of why the error arm's edges
sit on regions third rules govern, no figure.

What is pinned is the instrument, on a base worked by hand: a ticket's point of
the space, a pair's shared region split into what was governed at listing, by
the draft's own answer, later and never, a later point given to the birth that
completed it with a repair told from another error and from an impasse,
governance that never goes back, the replay's final graph the engine's, the
readings on rows built by hand, the expectation's clauses at their edges, and
that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from authorship import gates as egates
from authorship import protocol as e
from blind import rows as brows
from harness.domain import Case
from reasoned_loop import decided, governed as G, plan
from rung2.engine2 import EDGE_OK, Space

SPACE = Space()
T1, T2, T3, SI = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"
HIT, MISS, NEITHER = brows.HIT, brows.MISS, brows.NEITHER
UNSIGNED = {"passes": False, "found": 3, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


def ticket(**over):
    base = dict(has_security_keyword=False, severity=3, customer_tier="pro",
                product="dashboard", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


A = r_("A", 0, T1, product="billing")
C = r_("C", 1, T3, product="billing", customer_tier="free", channel="email")
D = r_("D", 2, SI, product="billing", channel="chat")
B = r_("B", 3, T2, customer_tier="free")
E = r_("E", 4, SI, product="billing", customer_tier="free", channel="phone")


def record(later_cause="ERROR", engine_rule="A", later_ticket=None):
    """A over B and D over B, both declared at B's birth. C lies inside A and B
    before B is born; D lies inside A and B places itself below D; E, born after,
    lies inside both."""
    rows = [{"idx": 0, "cause": "IMPASSE", "edge_reasons": []},
            {"idx": 1, "cause": "IMPASSE", "edge_reasons": []},
            {"idx": 2, "cause": "IMPASSE", "edge_reasons": []},
            {"idx": 3, "cause": "IMPASSE", "edge_reasons": ["ok", "ok"]},
            {"idx": 4, "cause": later_cause, "edge_reasons": [],
             "engine_rule": engine_rule if later_cause == "ERROR" else None}]
    corpus = [ticket(product="billing"), ticket(product="billing", customer_tier="free"),
              ticket(product="billing", channel="chat"), ticket(customer_tier="free"),
              later_ticket or ticket(product="billing", customer_tier="free", channel="phone")]
    return ({"rules": [A, C, D, B, E], "records": rows,
             "edge_log": [("A", "B", EDGE_OK), ("D", "B", EDGE_OK)],
             "edge_channels": [e.WRITE, e.WRITE]}, corpus)


def ext(rule):
    return brows.ext_of(rule, SPACE)


SHARED = ext(A) & ext(B)


class TestTheReplay(unittest.TestCase):

    def run_(self, **kw):
        rec, corpus = record(**kw)
        out = G.replay(rec, {("A", "B")}, SPACE, SPACE.full, corpus)
        rows = G.pair_rows([{"winner": "A", "loser": "B", "older": "A", "pair": MISS,
                             "point": NEITHER, "rl_e": True}], out["state"])
        return rec, out, rows[0]

    def test_a_ticket_is_one_point(self):
        p = G.point_of(ticket(product="billing", customer_tier="free"), SPACE)
        self.assertEqual(p.bit_count(), 1)
        self.assertTrue(p & SHARED)

    def test_the_four_parts(self):
        _, out, row = self.run_()
        email = (SHARED & ext(C)).bit_count()
        chat = (SHARED & ext(D)).bit_count()
        phone = (SHARED & ext(E)).bit_count()
        self.assertEqual(row["shared"], SHARED.bit_count())
        self.assertEqual((row["at_listing"], row["by_answer"], row["later"]),
                         (email, chat, phone))
        self.assertEqual(row["never"], SHARED.bit_count() - email - chat - phone)
        self.assertEqual(row["birth"], 3)
        self.assertFalse(out["went_back"])
        self.assertTrue(out["tickets_ok"])

    def test_a_later_point_goes_to_the_birth_that_completed_it(self):
        phone = (SHARED & ext(E)).bit_count()
        _, _, row = self.run_()
        self.assertEqual(row["later_by_cause"], {"IMPASSE": 0, "CONFLICT": 0, "ERROR": 0,
                                                 "REPAIR": phone})
        _, _, row = self.run_(engine_rule="B")
        self.assertEqual(row["later_by_cause"]["ERROR"], phone)
        _, _, row = self.run_(later_ticket=ticket(product="api"))
        self.assertEqual(row["later_by_cause"]["ERROR"], phone)
        _, _, row = self.run_(later_cause="IMPASSE")
        self.assertEqual(row["later_by_cause"]["IMPASSE"], phone)

    def test_the_replay_is_the_engine(self):
        rec, out, _ = self.run_()
        final, problems = egates.rebuild_final(rec, SPACE)
        self.assertEqual(problems, [])
        self.assertEqual(decided.graph_edges(out["engine"]), decided.graph_edges(final))

    def test_an_error_birth_whose_deciding_rule_is_not_in_the_base(self):
        rec, corpus = record(engine_rule="Z")
        out = G.replay(rec, {("A", "B")}, SPACE, SPACE.full, corpus)
        self.assertFalse(out["tickets_ok"])


def prow(pair, shared, listing, answer, later, never, repair=0, error=0):
    return {"pair": pair, "shared": shared, "at_listing": listing, "by_answer": answer,
            "later": later, "never": never, "governed_end": listing + answer + later,
            "later_by_cause": {"IMPASSE": later - repair - error, "CONFLICT": 0,
                               "ERROR": error, "REPAIR": repair}}


class TestTheReadings(unittest.TestCase):

    def test_sums_and_shares(self):
        rows = [prow(MISS, 10, 1, 1, 6, 2, repair=3, error=2),
                prow(MISS, 10, 10, 0, 0, 0), prow(HIT, 8, 0, 0, 0, 8)]
        got = G.arm_reading(rows)
        b = got["b"]
        self.assertEqual((b["pairs"], b["shared"], b["later"], b["governed_end"]), (2, 20, 6, 18))
        self.assertEqual(b["of_governed"]["later"], {"fraction": "1/3", "value": 1 / 3})
        self.assertEqual((b["pairs_with_a_repair"], b["pairs_governed_later"],
                          b["pairs_wholly_governed_at_listing"]), (1, 1, 1))
        self.assertEqual(got["a"]["never"], 8)
        self.assertEqual(got["strict"]["pairs"], 3)


class TestTheExpectation(unittest.TestCase):

    def arm(self, b, a):
        return G.arm_reading([b, a])

    def test_clause_by_clause_at_their_edges(self):
        # Missing: governed 12, later 6 (half), errors 3 of 6, repairs 2 of 6.
        b = prow(MISS, 20, 3, 3, 6, 8, repair=2, error=1)
        a = prow(HIT, 20, 1, 1, 1, 17)
        x = G.read_expectation(self.arm(b, a))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, False])
        b = prow(MISS, 20, 4, 3, 5, 8, repair=1, error=1)
        a = prow(HIT, 20, 2, 2, 5, 11)
        x = G.read_expectation(self.arm(b, a))
        self.assertEqual([c["holds"] for c in x], [False, False, False, False, False])
        b = prow(MISS, 20, 1, 0, 9, 10, repair=3, error=2)
        a = prow(HIT, 20, 0, 0, 1, 19)
        x = G.read_expectation(self.arm(b, a))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])

    def test_a_reading_without_value_does_not_hold(self):
        x = G.read_expectation(G.arm_reading([]))
        self.assertEqual([c["holds"] for c in x], [False] * 5)


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
                    G.main(argv)
                read.assert_not_called()
                write.assert_not_called()

    def test_the_lines(self):
        self.assertEqual((G.G1_SHARE, G.G2_SHARE, G.G3_SHARE),
                         (Fraction(1, 2), Fraction(1, 2), Fraction(1, 3)))


if __name__ == "__main__":
    unittest.main()
