"""
`corrections/online.py` — the POST-RUN reading of the ranking the loop declared,
as it went. No figure of the reading.

What is pinned is the instrument:
- each born rule's votes, as `corrections/declared.py` reads them, a citation a
  rule and side;
- the agreement kept as votes come equals every ranking's agreement read
  afresh, and the ranking chosen is the earliest of the most agreeing;
- the base so far: containment cut to the rules born, and what an order decides
  is the engine's own decision and first match's;
- the curve's helpers: the point at a checkpoint's case, and the birth from
  which a test holds for good;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import random
import unittest
from collections import Counter
from fractions import Fraction
from unittest import mock

from corrections import declared as DC
from corrections import hierarchy as H
from corrections import online as ON
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from manual import compile as MC
from manual import instrument as MI
from rung2.engine2 import EDGE_CYCLE, EDGE_OK
from tests.test_corrections_shape import UNSIGNED, c_, r_

SPACE = MI.space()
TRUTH = MI.space_truth()
F = Fraction
SEC, T2, BILL, T1 = "SECURITY_INCIDENT", "T2_TECHNICAL", "BILLING_SPECIALIST", "T1_GENERAL"


def rule(rid, action, born, beats=(), loses_to=(), dropped=()):
    return {"rule_id": rid, "action": action, "born_at": born, "beats": list(beats),
            "loses_to": list(loses_to), "dropped_edges": list(dropped)}


RECORD = {"rules": [
    rule("R1", SEC, 1),
    rule("R2", BILL, 2, loses_to=["R1"]),
    rule("R3", T2, 3, beats=["R2"], dropped=[f"loses_to:R1:{EDGE_CYCLE}"]),
    rule("R4", T1, 4, beats=["R3", "R3"], dropped=[f"loses_to:R3:{EDGE_CYCLE}"]),
]}


class TestTheVotes(unittest.TestCase):

    def test_each_born_rules_votes(self):
        got = ON.votes_of(RECORD)
        self.assertEqual(got["R1"], Counter())
        self.assertEqual(got["R2"], Counter({(SEC, BILL): 1}))
        self.assertEqual(got["R3"], Counter({(T2, BILL): 1, (SEC, T2): 1}))
        self.assertEqual(got["R4"], Counter({(T1, T2): 1, (T2, T1): 1}))
        total = sum(got.values(), Counter())
        self.assertEqual(total, DC.votes(DC.declarations(RECORD)))


class TestTheAgreement(unittest.TestCase):

    def test_kept_as_votes_come_equals_read_afresh(self):
        perms = H.rankings()
        rng = random.Random(23)
        agree = ON.Agreement(perms)
        so_far = Counter()
        for _ in range(5):
            v = Counter({(a, b): rng.randrange(1, 4) for a in ACTIONS for b in ACTIONS
                         if a != b and rng.random() < 0.1})
            agree.add(v)
            so_far.update(v)
            for k in range(0, len(perms), 4999):
                self.assertEqual(agree.scores[k], DC.agreement(so_far, perms[k]))
            first, top, ties = agree.chosen()
            want_top, want = DC.chosen(so_far, perms)
            self.assertEqual((first, top, ties), (want[0], want_top, len(want)))

    def test_no_votes_choose_the_first_ranking(self):
        agree = ON.Agreement(H.rankings())
        self.assertEqual(agree.chosen(), (0, 0, H.N_RANKINGS))


# The keyword's rule, a rule nested in it, a crossing billing rule, severity 1
# to the on-call queue, and a catch-all.
HAND = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
        r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
        r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
        r_("ONCALL_ESCALATION", c_("severity", "eq", 1)),
        r_("T1_GENERAL", c_("severity", "gte", 1))]


class TestTheBaseSoFar(unittest.TestCase):

    def setUp(self):
        self.eng = MC.install(HAND, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.rules = {r.rule_id: r for r in self.eng.rules}

    def test_containment_cut_to_the_rules_born(self):
        sub = ON.prefix_rules(self.rs, self.rs.ids[:3])
        keep = set(self.rs.ids[:3])
        for r in sub.ids:
            self.assertLessEqual(set(sub.inside[r]), keep)
            self.assertLessEqual(set(sub.around[r]), keep)
            self.assertEqual(sub.inside[r], self.rs.inside[r] & keep)

    def test_what_an_order_decides_is_the_engines(self):
        perms = H.rankings()
        for k in range(1, len(self.rs.ids) + 1):
            sub = ON.prefix_rules(self.rs, self.rs.ids[:k])
            for p in perms[::9973]:
                order = H.pulled(sub, H.rank_of(p))
                got = ON.right_of(order, sub, self.eng.ext, TRUTH, SPACE.n)
                eng = S.installed_in(order, {r: self.rules[r] for r in sub.ids}, SPACE)
                self.assertTrue(all(why == EDGE_OK for _, _, why in eng.edge_log))
                self.assertEqual(MI.over_space(eng)["correct"], got)
                self.assertEqual(MI.first_match_over_space([self.rules[r] for r in order])["correct"],
                                 got)


class TestTheCurve(unittest.TestCase):

    def test_at_case(self):
        curve = [{"born_at": 3}, {"born_at": 7}, {"born_at": 12}]
        self.assertIsNone(ON.at_case(curve, 2))
        self.assertEqual(ON.at_case(curve, 7), {"born_at": 7})
        self.assertEqual(ON.at_case(curve, 11), {"born_at": 7})
        self.assertEqual(ON.at_case(curve, 99), {"born_at": 12})

    def test_settled(self):
        pts = [{"x": v} for v in (0, 1, 1, 0, 1, 1, 1)]
        self.assertEqual(ON.settled(pts, lambda p: p["x"] == 1), 5)
        self.assertIsNone(ON.settled(pts + [{"x": 0}], lambda p: p["x"] == 1))
        self.assertEqual(ON.settled([{"x": 1}], lambda p: p["x"] == 1), 1)


def fake(sec_from=40, peak_birth=80, above=True, below=0, peak=F(7, 10), final=F(69, 100),
         record_peak=F(68, 100), settled_ranking=True, l2=((40, F(6, 10), F(5, 10)),
                                                         (160, F(7, 10), F(62, 100))),
         runs=ON.L_RUNS):
    def sh(x):
        return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}
    final_rank = list(ACTIONS)
    out = {}
    for t in runs:
        out[t] = {"ranking": {"security_first_from": sec_from, "final": final_rank},
                  "record": {"peak": {"birth": peak_birth, "share": sh(record_peak)}},
                  "replay": {"peak": {"share": sh(peak)}, "final": sh(final)},
                  "against_the_record": {"from_its_peak": above, "births_below_from_its_peak": below,
                                         "ranking_at_its_peak": final_rank if settled_ranking
                                         else list(reversed(final_rank))},
                  "checkpoints": [{"labels": lab, "replay": sh(rep), "at_once": sh(ao)}
                                  for lab, rep, ao in l2] if t == "l_r2" else []}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in ON.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_and_past_the_lines(self):
        got = holds(fake(sec_from=81, peak_birth=80, above=False, below=3, peak=F(7, 10),
                         final=F(679, 1000), record_peak=F(701, 1000), settled_ranking=False,
                         l2=((40, F(6, 10), F(5, 10)), (160, F(62, 100), F(62, 100)))))
        self.assertEqual(got, {"U1": False, "U2": False, "U3": False, "U4": False, "U5": False,
                               "U6": False})
        edges = holds(fake(sec_from=80, peak_birth=80, final=F(68, 100), peak=F(7, 10),
                           record_peak=F(7, 10)))
        self.assertTrue(edges["U1"])
        self.assertTrue(edges["U3"])
        self.assertTrue(edges["U6"])

    def test_u4_reads_l_r2_from_40_labels(self):
        got = holds(fake(l2=((10, F(1, 10), F(9, 10)), (40, F(6, 10), F(5, 10)))))
        self.assertTrue(got["U4"])
        self.assertFalse(holds(fake(l2=((10, F(9, 10), F(1, 10)),)))["U4"])
        self.assertFalse(holds(fake(runs=("l_r1", "l_r3")))["U4"])

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})
        self.assertFalse(holds(fake(sec_from=None))["U1"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(ON, "fall_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                ON.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
