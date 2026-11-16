"""
`corrections/declared.py` — the POST-RUN reading of whether the loop declared
the ranking it lacks. No figure of the reading.

What is pinned is the instrument:
- a declaration as `corrections/fall.py` reads it, each verdict named, but one
  a rule and side, where `declared` keeps one a rule; one vote for the queue
  declared above, and none within a queue or for a rule the record does not
  hold;
- the votes a ranking agrees with, and the rankings that agree with the most,
  by brute force;
- the record's edge log matched as a set, and a declaration it lacks refused;
- what the chosen rankings decide, on rules built by hand over the real space
  and policy: their orders install, and the pairs the votes leave free;
- the declarations against a ranking, by verdict;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from collections import Counter
from fractions import Fraction
from itertools import permutations
from unittest import mock

from corrections import declared as D
from corrections import hierarchy as H
from corrections import plan
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


# R1 security; R2 billing, declared below R1; R3 T2, declared above R2 and
# below R1, the second refused; R4 T1, citing R9 outside the round and R3 of
# another queue above it; R5 T1, citing R4 of its own queue; R6 billing, citing
# R3 on both sides, above it installed and below it refused, twice on the first.
RECORD = {"rules": [
    rule("R1", SEC, 1),
    rule("R2", BILL, 2, loses_to=["R1"]),
    rule("R3", T2, 3, beats=["R2"], dropped=[f"loses_to:R1:{EDGE_CYCLE}"]),
    rule("R4", T1, 4, loses_to=["R3"], dropped=["beats:R9"]),
    rule("R5", T1, 5, beats=["R4"]),
    rule("R6", BILL, 6, beats=["R3", "R3"], dropped=[f"loses_to:R3:{EDGE_CYCLE}"]),
], "edge_log": [["R1", "R2", EDGE_OK], ["R3", "R2", EDGE_OK], ["R1", "R3", EDGE_CYCLE],
                ["R3", "R4", EDGE_OK], ["R5", "R4", EDGE_OK], ["R6", "R3", EDGE_OK],
                ["R3", "R6", EDGE_CYCLE]]}


class TestTheDeclarations(unittest.TestCase):

    def test_each_declaration_and_its_verdict(self):
        decls = D.declarations(RECORD)
        got = {(d["rule"], d["ref"], d["side"]): (d["verdict"], d["queue"], d["ref_queue"])
               for d in decls}
        self.assertEqual(len(got), len(decls))
        self.assertEqual(got, {
            ("R2", "R1", "loses_to"): (D.INSTALLED, BILL, SEC),
            ("R3", "R2", "beats"): (D.INSTALLED, T2, BILL),
            ("R3", "R1", "loses_to"): (D.REFUSED, T2, SEC),
            ("R4", "R3", "loses_to"): (D.INSTALLED, T1, T2),
            ("R4", "R9", "beats"): (D.OUTSIDE, T1, None),
            ("R5", "R4", "beats"): (D.INSTALLED, T1, T1),
            ("R6", "R3", "beats"): (D.INSTALLED, BILL, T2),
            ("R6", "R3", "loses_to"): (D.REFUSED, BILL, T2)})

    def test_both_sides_are_kept_where_fall_keeps_one(self):
        from corrections import fall as fl
        r6 = RECORD["rules"][5]
        self.assertEqual(len(fl.declared(r6)), 1)
        self.assertEqual(sorted(D.citations(r6)),
                         [("R3", "beats", EDGE_OK), ("R3", "loses_to", EDGE_CYCLE)])

    def test_one_vote_for_the_queue_above(self):
        decls = D.declarations(RECORD)
        self.assertEqual(D.votes(decls), Counter({(SEC, BILL): 1, (T2, BILL): 2, (SEC, T2): 1,
                                                  (T2, T1): 1, (BILL, T2): 1}))
        self.assertEqual(D.votes(decls, (D.INSTALLED,)),
                         Counter({(SEC, BILL): 1, (T2, BILL): 1, (T2, T1): 1, (BILL, T2): 1}))
        self.assertEqual(D.votes(decls, (D.REFUSED,)), Counter({(SEC, T2): 1, (T2, BILL): 1}))

    def test_the_edge_log_is_matched_as_a_set(self):
        decls = D.declarations(RECORD)
        self.assertTrue(D.edge_log_matches(RECORD, decls))
        twice = {**RECORD, "edge_log": RECORD["edge_log"] + [["R1", "R2", EDGE_OK]]}
        self.assertTrue(D.edge_log_matches(twice, decls))
        less = {**RECORD, "edge_log": RECORD["edge_log"][1:]}
        self.assertFalse(D.edge_log_matches(less, decls))
        other = {**RECORD, "edge_log": [e if e[:2] != ["R5", "R4"] else ["R5", "R4", EDGE_CYCLE]
                                        for e in RECORD["edge_log"]]}
        self.assertFalse(D.edge_log_matches(other, decls))
        one_side = {**RECORD, "rules": RECORD["rules"][:5] + [
            rule("R6", BILL, 6, beats=["R3"])]}
        self.assertFalse(D.edge_log_matches(one_side, D.declarations(one_side)))

    def test_by_pair(self):
        rows = D.by_pair(Counter({(SEC, BILL): 2, (BILL, SEC): 1}))
        self.assertEqual(len(rows), 28)
        row = next(x for x in rows if set(x["pair"]) == {SEC, BILL})
        first = row["pair"][0]
        self.assertEqual((row["for_first"], row["for_second"]),
                         (2, 1) if first == SEC else (1, 2))


class TestTheRankingsTheyChoose(unittest.TestCase):

    def test_agreement(self):
        v = Counter({(SEC, BILL): 3, (BILL, SEC): 1, (T2, T1): 2})
        ranking = [SEC, T2, BILL, T1] + [q for q in ACTIONS if q not in (SEC, T2, BILL, T1)]
        self.assertEqual(D.agreement(v, ranking), 5)
        self.assertEqual(D.agreement(v, list(reversed(ranking))), 1)

    def test_the_most_agreeing_by_brute_force(self):
        v = Counter({(SEC, BILL): 3, (BILL, SEC): 1, (T2, T1): 2, (BILL, T2): 1})
        perms = H.rankings()
        top, ks = D.chosen(v, perms)
        want = max(D.agreement(v, p) for p in perms)
        self.assertEqual(top, want)
        self.assertEqual(ks, [k for k, p in enumerate(perms) if D.agreement(v, p) == want])
        for k in ks:
            p = perms[k]
            self.assertLess(p.index(SEC), p.index(BILL))
            self.assertLess(p.index(T2), p.index(T1))
            self.assertLess(p.index(BILL), p.index(T2))

    def test_no_votes_choose_every_ranking(self):
        top, ks = D.chosen(Counter(), H.rankings())
        self.assertEqual((top, len(ks)), (0, H.N_RANKINGS))


# The keyword's rule, a rule nested in it, a crossing billing rule, severity 1
# to the on-call queue, and a catch-all.
HAND = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
        r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
        r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
        r_("ONCALL_ESCALATION", c_("severity", "eq", 1)),
        r_("T1_GENERAL", c_("severity", "gte", 1))]


class TestOnTheSpace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from corrections import shape as S
        cls.eng = MC.install(HAND, SPACE).engine
        cls.rs = H.rules_of(cls.eng)
        cls.rules = {r.rule_id: r for r in cls.eng.rules}
        cls.inst = S.instance(cls.eng.rules, cls.eng.ext, cls.rs.inside, cls.rs.around, TRUTH,
                              SPACE.n)
        cls.perms = H.rankings()

    def test_the_chosen_rankings_read_and_install(self):
        v = Counter({(SEC, BILL): 2, (SEC, "ONCALL_ESCALATION"): 1, (BILL, T1): 1})
        got, ok = D.read_chosen(self.rs, self.inst, self.rules, self.perms, v, SPACE, TRUTH)
        self.assertTrue(ok)
        self.assertEqual(got["votes"], 4)
        self.assertEqual(got["agreeing"], 4)
        self.assertEqual(sum(got["by_place_of_security"].values()), got["rankings"])
        self.assertLessEqual(F(got["orders"]["least"]["share"]["fraction"]),
                             F(got["orders"]["most"]["share"]["fraction"]))
        free = {frozenset(p) for p in got["pairs_left_free"]}
        self.assertNotIn(frozenset({SEC, BILL}), free)
        self.assertNotIn(frozenset({BILL, T1}), free)
        self.assertIn(frozenset({T2, "T3_ENGINEERING"}), free)

    def test_against_a_ranking(self):
        decls = D.declarations(RECORD)
        ranking = [SEC, T2, BILL, T1] + [q for q in ACTIONS if q not in (SEC, T2, BILL, T1)]
        got = D.against_best(decls, ranking)
        self.assertEqual((got["all"]["votes"], got["all"]["agreeing"]), (6, 5))
        self.assertEqual((got[D.INSTALLED]["votes"], got[D.INSTALLED]["agreeing"]), (4, 3))
        self.assertEqual((got[D.REFUSED]["votes"], got[D.REFUSED]["agreeing"]), (2, 2))
        self.assertEqual(got[D.OUTSIDE]["votes"], 0)
        self.assertIsNone(got[D.OUTSIDE]["share"])


def fake(median=F(7, 10), first=3, rankings=3, at_once=F(65, 100), completed=F(55, 100),
         stated=F(6, 10), agree=F(3, 5), installed=F(1, 2), refused=F(3, 5), runs=D.L_RUNS):
    def sh(x):
        return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}
    out, kept, shape = {}, {"runs": {}}, {"runs": {}}
    for t in runs:
        out[t] = {"every_declaration": {"shares": {"median": sh(median)},
                                        "security_first": first, "rankings": rankings},
                  "against_best": {"all": {"share": sh(agree)},
                                   D.INSTALLED: {"share": sh(installed)},
                                   D.REFUSED: {"share": sh(refused)}}}
        kept["runs"][t] = {"loop": {"on_record": {"stated": {"pulled": {"median": sh(stated)}}}}}
        shape["runs"][t] = {"at_once_median": {"record": sh(at_once)},
                            "loop": {"completed": {"share": sh(completed)}}}
    return out, kept, shape


def holds(triple):
    return {c["clause"]: c["holds"] for c in D.read_expectation(*triple)}


class TestTheExpectation(unittest.TestCase):

    def test_just_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(median=F(13, 20), first=2, at_once=F(13, 20), completed=F(13, 20),
                         stated=F(13, 20), agree=F(1, 2), installed=F(3, 5), refused=F(3, 5)))
        self.assertEqual(got, {"W1": False, "W2": False, "W3": False, "W4": False, "W5": False,
                               "W6": False})

    def test_w2_and_w5_read_two_named_runs(self):
        got = holds(fake(runs=("l_r1", "l_r2")))
        self.assertEqual(got, {"W1": False, "W2": True, "W3": False, "W4": False, "W5": True,
                               "W6": False})

    def test_over_nothing(self):
        self.assertEqual(set(holds(({}, {"runs": {}}, {"runs": {}})).values()), {False})
        self.assertFalse(holds(fake(first=0, rankings=0))["W1"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        from corrections import shape as S
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(D, "hierarchy_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                D.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
