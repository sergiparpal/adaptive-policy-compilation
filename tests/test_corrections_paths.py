"""
`corrections/paths.py` — the POST-RUN reading of why a rule's wins reach the
rule it should lose to, no figure.

What is pinned is the instrument, on three runs built by hand over the real
space, each with a truth of its own, and each refusing one newborn's right side
for its own reason:
- run A: the newborn beats a rule declared above the keyword's rule, wrongly
  by the policy, and the cycle is real where the three rules meet;
- run B: the newborn beats a rule of another queue nested inside the keyword's
  rule, wrongly by the policy;
- run C: the newborn reaches the keyword's rule through a rule the policy
  rightly puts above it, by a path through a rule that misses every point
  the pair shares.
Also pinned:
- what beats what forward and back, the shortest path, the reach through
  rules that all match a point, and the policy's verdict on a crossing;
- the five gates on those runs, and each failing on its own;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import fall as fl
from corrections import paths as G
from corrections import plan
from edges import rebuild as erb
from fidelity.replay import rule_from
from harness.ceiling_check import all_cases
from harness.domain import Case
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

F = Fraction
SPACE = Space()
CASES = list(all_cases())
N_POINTS = SPACE.n
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BI, AM, SEC = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SECURITY_INCIDENT"
IMP, ERR = plan.IMPASSE, plan.ERROR
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

KW = SPACE.mask["has_security_keyword"][True]
NOKW = SPACE.mask["has_security_keyword"][False]
CHAT = SPACE.mask["channel"]["chat"]
# Runs A and B: the keyword's tickets are SECURITY_INCIDENT's, the rest T1's.
TRUTH_AB = {SEC: KW, T1: NOKW}
# Run C: the keyword's chat tickets are ACCOUNT_MANAGER's.
TRUTH_C = {AM: KW & CHAT, SEC: KW & ~CHAT, T1: NOKW}


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(rid, born, action, conds, beats=(), loses_to=(), refused=()):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to),
            "dropped_edges": [f"loses_to:{x}:{EDGE_CYCLE}" for x in refused]}


KEYWORD = c_("has_security_keyword", "eq", True)
NO_KEYWORD = c_("has_security_keyword", "eq", False)
BILLING = c_("product", "eq", "billing")

RUN_A = {
    "births": [
        (IMP, r_("U", 0, SEC, [KEYWORD])),
        (IMP, r_("T", 1, T1, [NO_KEYWORD])),
        (ERR, r_("W", 2, AM, [c_("channel", "eq", "chat")], beats=["U", "T"])),
        (ERR, r_("N", 3, BI, [BILLING], beats=["W"], refused=["U", "T"])),
    ],
    "edges": [(2, "W", "U"), (2, "W", "T"), (3, "N", "W"), (3, "U", "N", EDGE_CYCLE),
              (3, "T", "N", EDGE_CYCLE)],
    "truth": TRUTH_AB, "final": 80640,
}
RUN_B = {
    "births": [
        (IMP, r_("U", 0, SEC, [KEYWORD])),
        (IMP, r_("T", 1, T1, [NO_KEYWORD])),
        (ERR, r_("X", 2, T3, [KEYWORD, c_("severity", "eq", 1)])),
        (ERR, r_("N", 3, BI, [BILLING], beats=["X"], loses_to=["T"], refused=["U"])),
    ],
    "edges": [(3, "N", "X"), (3, "U", "N", EDGE_CYCLE), (3, "T", "N")],
    "truth": TRUTH_AB, "final": 107520,
}
RUN_C = {
    "births": [
        (IMP, r_("U", 0, SEC, [KEYWORD, c_("severity", "lte", 2)])),
        (IMP, r_("T", 1, T1, [NO_KEYWORD])),
        (ERR, r_("X2", 2, AM, [KEYWORD, c_("channel", "eq", "chat")], beats=["U"])),
        (IMP, r_("X1", 3, T2, [c_("severity", "gte", 3)], beats=["X2"], loses_to=["T"])),
        (ERR, r_("N", 4, BI, [BILLING], beats=["X1"], loses_to=["T"], refused=["U"])),
    ],
    "edges": [(2, "X2", "U"), (3, "X1", "X2"), (3, "T", "X1"), (4, "N", "X1"),
              (4, "U", "N", EDGE_CYCLE), (4, "T", "N")],
    "truth": TRUTH_C, "final": 94080,
}


def ticket():
    return Case(has_security_keyword=False, severity=3, customer_tier="free",
                product="api", channel="portal", prior_tickets_30d=0, off_hours=False,
                language="en")


def record(run, edges=None):
    births = run["births"]
    cases = len(births)
    rows = [{"idx": i, "edge_reasons": []} for i in range(cases)]
    log = []
    for born, w, l, *why in (edges if edges is not None else run["edges"]):
        reason = why[0] if why else EDGE_OK
        rows[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    return {"rules": [rule for _, rule in births], "records": rows, "edge_log": log,
            "escalations": [{"idx": rule["born_at"], "kind": cause, "verdict": "nacida",
                             "rule_id": rule["rule_id"]} for cause, rule in births]}


def fall_run(run, rec=None):
    """`corrections/fall.py`'s reading of the same run, as `fall.json` keeps it."""
    rec = rec or record(run)
    corpus = [ticket() for _ in run["births"]]
    final = erb.rebuild(rec, corpus, SPACE).engine
    return fl.read_run(rec, SPACE, run["truth"], CASES,
                       {"space": {"fraction": str(F(run["final"], N_POINTS))}}, final=final)


def read(run, rec=None, fall=None, final_rec=None):
    rec = rec or record(run)
    corpus = [ticket() for _ in run["births"]]
    final = erb.rebuild(final_rec or rec, corpus, SPACE).engine
    return G.read_run(rec, SPACE, run["truth"], CASES, fall or fall_run(run), final=final)


def gate(got, k):
    return next(g for g in got["gates"] if g["gate"] == k)["passes"]


class TestTheGraph(unittest.TestCase):

    def setUp(self):
        self.engine = PriorityEngine(space=SPACE)
        rec = record(RUN_C)
        born, by_birth = erb.births(rec), erb.edges_by_birth(rec)
        for idx in sorted(born):
            self.engine.add(rule_from(born[idx]), born_at=idx, keep_id=True)
            for e in by_birth.get(idx, []):
                self.engine.try_edge(e.winner, e.loser)

    def test_forward_and_back(self):
        self.assertEqual(G.forward(self.engine, "N"), {"N", "X1", "X2", "U"})
        self.assertEqual(G.forward(self.engine, "N", {("X1", "X2")}), {"N", "X1"})
        self.assertEqual(G.backward(self.engine, "U"), {"U", "X2", "X1", "N", "T"})

    def test_the_shortest_path(self):
        nodes = {"N", "X1", "X2", "U"}
        self.assertEqual(G.shortest(self.engine, "N", "U", nodes), 3)
        self.assertIsNone(G.shortest(self.engine, "N", "U", {"N", "X1", "U"}))

    def test_the_reach_through_rules_that_all_match(self):
        nodes = {"N", "X1", "X2", "U"}
        shared = self.engine.ext["N"] & self.engine.ext["U"]
        self.assertEqual(G.local_reach(self.engine, "N", "U", nodes, shared), 0)
        everywhere = SPACE.full
        self.assertEqual(G.local_reach(self.engine, "N", "X2", nodes, everywhere),
                         self.engine.ext["N"] & self.engine.ext["X1"] & self.engine.ext["X2"])

    def test_the_policy_s_verdict_on_a_crossing(self):
        action = {r.rule_id: r.action for r in self.engine.rules}
        self.assertEqual(G.verdict(self.engine, "X2", "U", action, TRUTH_C), G.RIGHT_VERDICT)
        self.assertEqual(G.verdict(self.engine, "X2", "U", action, TRUTH_AB), G.WRONG)
        even = {AM: KW & CHAT & SPACE.mask["severity"][1], SEC: KW & CHAT & SPACE.mask["severity"][2]}
        self.assertEqual(G.verdict(self.engine, "X2", "U", action, even), G.EVEN)


class TestTheClasses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a, cls.b, cls.c = read(RUN_A), read(RUN_B), read(RUN_C)

    def test_all_five_gates_pass_on_the_three_runs(self):
        for got in (self.a, self.b, self.c):
            self.assertEqual([g["passes"] for g in got["gates"]], [True] * 5)

    def test_run_a_a_rule_declared_wrongly_above(self):
        s = self.a["summary"]
        self.assertEqual((s["pairs"], s["points"]), (2, 20160))
        self.assertEqual(s["by_class"], {G.WRONG_DECLARED: 20160, G.WRONG_NESTED: 0,
                                         G.RIGHT: 0})
        self.assertEqual(s["where"], {G.SOMEWHERE: 20160, G.NOWHERE: 0})
        self.assertEqual(s["crossings"], {"declared:wrong": 2})
        self.assertEqual(s["wrong_declared"], {"distinct": 2, "by_cause": {ERR: 2},
                                               "installed_by_the_newborn": 0})
        self.assertEqual(s["births_by_cause"], {IMP: 2, ERR: 2})
        self.assertEqual(s["by_queue"], {SEC: 10080, T1: 10080})
        for p in self.a["pairs"]:
            self.assertEqual((p["newborn"], p["shortest"], p["path_rules"], p["touched"],
                              p["own_crossing"]), ("N", 2, 1, 0, False))

    def test_run_b_a_rule_nested_wrongly_inside(self):
        s = self.b["summary"]
        self.assertEqual((s["pairs"], s["points"]), (1, 10080))
        self.assertEqual(s["by_class"], {G.WRONG_DECLARED: 0, G.WRONG_NESTED: 10080,
                                         G.RIGHT: 0})
        self.assertEqual(s["where"], {G.SOMEWHERE: 10080, G.NOWHERE: 0})
        self.assertEqual(s["crossings"], {"nested:wrong": 1})
        self.assertEqual(s["wrong_declared"]["distinct"], 0)

    def test_run_c_a_right_crossing_through_a_rule_that_misses(self):
        s = self.c["summary"]
        self.assertEqual((s["pairs"], s["points"]), (1, 5040))
        self.assertEqual(s["by_class"], {G.WRONG_DECLARED: 0, G.WRONG_NESTED: 0,
                                         G.RIGHT: 5040})
        self.assertEqual(s["where"], {G.SOMEWHERE: 0, G.NOWHERE: 5040})
        self.assertEqual(s["shortest"], {"3": 5040})
        self.assertEqual(s["crossings"], {"declared:right": 1})
        p = self.c["pairs"][0]
        self.assertEqual((p["path_rules"], p["touched"]), (2, 0))
        self.assertEqual([(x["upper"], x["lower"], x["installed_at"], x["cause"])
                          for x in p["crossings"]], [("X2", "U", 2, ERR)])

    def test_the_pairs_are_fall_s(self):
        beside = fall_run(RUN_C)["added_after_the_first_run"]["beside"]
        self.assertEqual((beside["pairs"]["below_refused"], beside["points"]), (5040, 6720))


class TestTheGates(unittest.TestCase):

    def test_gate_1_fails_on_another_base(self):
        got = read(RUN_A, final_rec=record(RUN_A, edges=RUN_A["edges"][1:]))
        self.assertFalse(gate(got, 1))
        self.assertTrue(gate(got, 2) and gate(got, 3) and gate(got, 4) and gate(got, 5))

    def test_gate_2_fails_off_fall_s_pairs(self):
        fall = fall_run(RUN_A)
        fall["added_after_the_first_run"]["beside"]["pairs"]["below_refused"] += 1
        self.assertFalse(gate(read(RUN_A, fall=fall), 2))

    def test_gate_3_fails_when_the_log_is_not_the_engine_s(self):
        edges = RUN_A["edges"][:3] + [(3, "U", "N"), (3, "T", "N", EDGE_CYCLE)]
        rec = record(RUN_A, edges=edges)
        got = read(RUN_A, rec=rec, fall=fall_run(RUN_A))
        self.assertFalse(gate(got, 3))

    def test_gate_4_fails_when_a_path_touches_the_points(self):
        with mock.patch.object(G, "local_reach", side_effect=lambda e, s, d, n, region: region):
            got = read(RUN_A)
        self.assertFalse(gate(got, 4))

    def test_gate_5_fails_on_a_class_outside_the_three(self):
        analyse = G.analyse

        def unclassed(*a, **k):
            got = analyse(*a, **k)
            got["class"] = "other"
            return got

        with mock.patch.object(G, "analyse", side_effect=unclassed):
            got = read(RUN_B)
        self.assertFalse(gate(got, 5))
        self.assertTrue(gate(got, 1) and gate(got, 2) and gate(got, 3) and gate(got, 4))


def summary(points=100, declared=25, nested=25, somewhere=50, distinct=10, at_error=5,
            births=20, births_error=10):
    return {"points": points,
            "by_class": {G.WRONG_DECLARED: declared, G.WRONG_NESTED: nested,
                         G.RIGHT: points - declared - nested},
            "where": {G.SOMEWHERE: somewhere, G.NOWHERE: points - somewhere},
            "wrong_declared": {"distinct": distinct, "by_cause": {ERR: at_error}},
            "births_by_cause": {ERR: births_error, IMP: births - births_error}}


def clauses(l_runs, n3=None):
    runs = {plan.tag(plan.LABELLED, k): {"summary": s} for k, s in enumerate(l_runs, start=1)}
    if n3 is not None:
        runs[G.K5_RUN] = {"summary": n3}
    return {c["clause"]: c["holds"] for c in G.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_every_clause_holds_at_its_line(self):
        self.assertEqual(clauses([summary()] * 3, summary()),
                         {k: True for k in ("K1", "K2", "K3", "K4", "K5")})

    def test_k1_k2_and_k4_pool_l_s_runs(self):
        got = clauses([summary(declared=24, somewhere=49), summary(), summary()], summary())
        self.assertEqual((got["K1"], got["K2"], got["K4"]), (False, False, False))
        got = clauses([summary(declared=24, somewhere=49), summary(declared=26, somewhere=51),
                       summary()], summary())
        self.assertEqual((got["K1"], got["K2"], got["K4"]), (True, True, True))

    def test_k3_sets_the_crossings_beside_the_births(self):
        self.assertFalse(clauses([summary(at_error=4)] * 3, summary())["K3"])
        self.assertTrue(clauses([summary(births_error=9)] * 3, summary())["K3"])

    def test_k5_reads_n_r3_alone(self):
        self.assertFalse(clauses([summary()] * 3, summary(declared=24))["K5"])
        self.assertFalse(clauses([summary()] * 3)["K5"])

    def test_a_clause_over_nothing_fails(self):
        nothing = summary(points=0, declared=0, nested=0, somewhere=0, distinct=0,
                          at_error=0, births=0, births_error=0)
        self.assertEqual(clauses([nothing] * 3, nothing),
                         {k: False for k in ("K1", "K2", "K3", "K4", "K5")})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(G, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                G.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
