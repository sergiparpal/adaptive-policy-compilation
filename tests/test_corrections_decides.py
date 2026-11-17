"""
`corrections/decides.py` — the POST-RUN reading of a count of what each pair
decides. No figure of the reading.

What is pinned is the instrument:
- what a pair decides in an order: computed rule by rule, it is the same; it is
  exactly the points whose deciding rule changes when two neighbours of the
  order are exchanged; a rule and a rule nested in it decide nothing together;
  the rules before both take their points from the pair;
- the votes, one a citation between rules of two queues, oriented by the side
  declared, and their count `corrections/declared.py`'s own;
- the share of a set of votes that agrees with a ranking, and a queue's place;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import billing as BL
from corrections import declared as DC
from corrections import decides as D
from corrections import hierarchy as H
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from manual import compile as MC
from manual import instrument as MI
from tests.test_corrections_shape import UNSIGNED, c_, r_

SPACE = MI.space()
F = Fraction
SEC, T3, AM, BILL = "SECURITY_INCIDENT", D.T3, D.AM, D.BILLING

# The keyword's rule, T3_ENGINEERING at severity 1 for business clients and on the
# api at severity 2 or less, ACCOUNT_MANAGER's churn, a billing rule, and a rule of
# ACCOUNT_MANAGER nested in the billing rule.
HAND = [r_(SEC, c_("has_security_keyword", "eq", True)),
        r_(T3, c_("severity", "eq", 1), c_("customer_tier", "eq", "business")),
        r_(AM, c_("customer_tier", "eq", "business"), c_("prior_tickets_30d", "gte", 8)),
        r_(T3, c_("product", "eq", "api"), c_("severity", "lte", 2)),
        r_(BILL, c_("product", "eq", "billing")),
        r_(AM, c_("product", "eq", "billing"), c_("customer_tier", "eq", "enterprise"))]
RANKING = (SEC, "ONCALL_ESCALATION", T3, AM, "T2_TECHNICAL", "SELF_SERVICE_DEFLECT", BILL,
           "T1_GENERAL")


def decl(rule, ref, side, queue, ref_queue):
    return {"rule": rule, "ref": ref, "side": side, "why": "ok", "verdict": "installed",
            "queue": queue, "ref_queue": ref_queue}


class Hand:

    def __init__(self):
        self.eng = MC.install(HAND, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.ids = self.rs.ids                      # HAND's order
        self.M = S.undefeated(self.eng.ext, self.rs.inside)


HANDS: list[Hand] = []


def hand() -> Hand:
    if not HANDS:
        HANDS.append(Hand())
    return HANDS[0]


def deciders(order, M):
    """Each point's deciding rule, as a mask a rule."""
    remaining, out = (1 << SPACE.n) - 1, {}
    for r in order:
        out[r] = M[r] & remaining
        remaining &= ~M[r]
    return out


class TestWhatAPairDecides(unittest.TestCase):

    def setUp(self):
        self.h = hand()
        sec, t3_sev1, am_churn, t3_api, bill, am_bill = self.h.ids
        self.rows = D.vote_rows([
            decl(t3_sev1, am_churn, "beats", T3, AM),
            decl(am_churn, t3_api, "beats", AM, T3),
            decl(am_bill, bill, "beats", AM, BILL),        # nested: decides nothing
            decl(bill, sec, "loses_to", BILL, SEC),
        ], self.h.rs.action)
        self.order = H.pulled(self.h.rs, H.rank_of(RANKING))

    def test_rule_by_rule_the_same(self):
        got = D.decided(self.rows, self.order, self.h.M)
        pos = {r: i for i, r in enumerate(self.order)}
        for row, n in zip(self.rows, got):
            m = self.h.M[row["winner"]] & self.h.M[row["loser"]]
            for r in self.order[:min(pos[row["winner"]], pos[row["loser"]])]:
                m &= ~self.h.M[r]
            self.assertEqual(n, m.bit_count())

    def test_a_nested_pair_decides_nothing(self):
        self.assertEqual(D.decided(self.rows, self.order, self.h.M)[2], 0)

    def test_rules_before_both_take_their_points(self):
        sec, t3_sev1, am_churn, *_ = self.h.ids
        # the keyword's rule before both covers the keyword's half of what they share
        row = D.vote_rows([decl(t3_sev1, am_churn, "beats", T3, AM)], self.h.rs.action)
        order = [sec] + [r for r in self.order if r != sec]
        shared = self.h.M[t3_sev1] & self.h.M[am_churn]
        self.assertEqual(D.decided(row, order, self.h.M)[0],
                         (shared & ~self.h.M[sec]).bit_count())
        covered = [r for r in order if r not in (t3_sev1, am_churn)] + [t3_sev1, am_churn]
        rest = shared
        for r in covered[:-2]:
            rest &= ~self.h.M[r]
        self.assertEqual(D.decided(row, covered, self.h.M)[0], rest.bit_count())

    def test_it_is_what_exchanging_neighbours_changes(self):
        order = list(self.order)
        for i in range(len(order) - 1):
            a, b = order[i], order[i + 1]
            if self.h.rs.action[a] == self.h.rs.action[b]:
                continue
            row = D.vote_rows([decl(a, b, "beats", self.h.rs.action[a], self.h.rs.action[b])],
                              self.h.rs.action)
            swapped = order[:i] + [b, a] + order[i + 2:]
            before, after = deciders(order, self.h.M), deciders(swapped, self.h.M)
            changed = 0
            for r in order:
                changed |= before[r] ^ after[r]
            self.assertEqual(D.decided(row, order, self.h.M)[0], changed.bit_count())
            self.assertEqual(changed & ~before[a], 0)
            self.assertEqual(changed & ~after[b], 0)


class TestTheVotes(unittest.TestCase):

    def test_oriented_and_counted_as_declared_counts_them(self):
        h = hand()
        sec, t3_sev1, am_churn, t3_api, bill, am_bill = h.ids
        decls = [decl(t3_sev1, am_churn, "beats", T3, AM),
                 decl(am_churn, t3_api, "loses_to", AM, T3),
                 decl(bill, am_bill, "loses_to", BILL, AM),
                 decl(t3_sev1, t3_api, "beats", T3, T3),           # within a queue
                 decl(bill, "R9999", "beats", BILL, None)]         # unknown rule
        rows = D.vote_rows(decls, h.rs.action)
        self.assertEqual([(r["for"], r["against"]) for r in rows], [(T3, AM), (T3, AM), (AM, BILL)])
        self.assertEqual(D.count(rows), DC.votes(decls))

    def test_agreeing_and_places(self):
        rows = [{"for": T3, "against": AM}, {"for": AM, "against": T3}, {"for": SEC, "against": BILL}]
        got = D.agreeing(rows, RANKING)
        self.assertEqual((got["votes"], got["agreeing"]), (3, 2))
        self.assertEqual(F(got["share"]["fraction"]), F(2, 3))
        self.assertIsNone(D.agreeing([], RANKING)["share"])
        self.assertEqual(D.place(RANKING, BILL), 7)
        self.assertTrue(D.above(RANKING, T3, AM))
        self.assertFalse(D.above(RANKING, AM, T3))


def fake(kept_place=5, declared_place=7, kept=F(8, 10), declared=F(7, 10), turned=True,
         at_once=F(75, 100), kept_agree=F(8, 10), left_agree=F(6, 10), kept_corpus=101,
         declared_corpus=100, runs=D.L_RUNS):
    def sh(x):
        return {"fraction": str(x), "value": float(x)}
    out = {}
    for t in runs:
        out[t] = {"kept_count": {"median": {"billing_place": kept_place, "space": {"share": sh(kept)},
                                            "account_manager_above_t3": turned,
                                            "corpus": {"right": kept_corpus}}},
                  "beside": {"declared": {"billing_place": declared_place,
                                          "space": {"share": sh(declared)},
                                          "corpus": {"right": declared_corpus}},
                             "at_once": sh(at_once)},
                  "against_best": {"kept": {"share": sh(kept_agree)},
                                   "left_out": {"share": sh(left_agree)}}}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in D.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(kept_place=7, kept=F(7, 10), turned=False, at_once=F(7, 10),
                         kept_agree=F(6, 10), kept_corpus=100))
        self.assertEqual(got, {f"P{k}": False for k in range(1, 7)})

    def test_the_runs_each_reads(self):
        got = holds(fake(runs=("l_r1", "l_r3")))
        self.assertTrue(got["P1"])
        self.assertFalse(got["P2"] or got["P3"] or got["P4"] or got["P5"] or got["P6"])

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(BL, "declared_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                D.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
