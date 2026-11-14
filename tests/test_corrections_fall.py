"""
`corrections/fall.py` — the POST-RUN reading of why the loop's share of the
space peaked and fell, no figure.

What is pinned is the instrument, on a run built by hand over the real space,
with a truth by product: `api` to `T2_TECHNICAL`, `billing` to
`BILLING_SPECIALIST`, and the other three products to `T1_GENERAL`. Nine
births and two declared edges. Three broad rules make the peak, and after it
each kind of loss falls on a region chosen for it:
- a rule nested inside the `api` rule takes a quarter of it by containment;
- a rule of `chat` is declared above the `billing` rule, and takes its `chat`
  tickets by an edge;
- the same rule crosses the `mobile` rule with no edge, a conflict;
- a later rule gains points the peak did not hold;
- a point lost, won back, and lost again is read at its last loss.
Also pinned:
- the masks' decision, its points right, its outcome at a point, and the ends
  of a mask;
- the space's enumeration, case `k` at bit `n - 1 - k`;
- the four gates on that run, and each failing on its own;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import fall as G
from corrections import plan
from edges import rebuild as erb
from harness.ceiling_check import all_cases
from harness.domain import ATTRIBUTES, Case
from rung2.engine2 import EDGE_OK, Space

F = Fraction
SPACE = Space()
CASES = list(all_cases())
N_POINTS = SPACE.n
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BI, AM = "BILLING_SPECIALIST", "ACCOUNT_MANAGER"
IMP, ERR, CON = plan.IMPASSE, plan.ERROR, plan.CONFLICT
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

PRODUCT = SPACE.mask["product"]
TRUTH = {T2: PRODUCT["api"], BI: PRODUCT["billing"],
         T1: PRODUCT["dashboard"] | PRODUCT["mobile"] | PRODUCT["integrations"]}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


def ticket(**over):
    base = dict(has_security_keyword=False, severity=3, customer_tier="free",
                product="api", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


# Each birth: the cause of its escalation and its rule. A product holds 26,880
# points of the space, and a product with a channel or a severity 6,720.
BIRTHS = [
    (IMP, r_("R1", 0, T2, product="api")),                       # right on 26,880
    (IMP, r_("R2", 1, BI, product="billing")),                   # right on 26,880
    (IMP, r_("R3", 2, T1, product="mobile")),                    # right on 26,880: the peak
    (ERR, r_("R4", 3, T3, product="api", severity=1)),           # nested in R1: 6,720 lost
    (ERR, r_("R5", 4, AM, channel="chat")),                      # above R2, crossing R3
    (IMP, r_("R6", 5, T1, product="integrations", channel="email")),   # 6,720 gained
    (CON, r_("R7", 6, BI, product="api", channel="portal")),     # nested in R1: 5,040 lost
    (ERR, r_("R8", 7, T2, product="api", channel="portal", severity=2)),   # 1,680 won back
    (IMP, r_("R9", 8, AM, product="api", channel="portal", severity=2, language="en")),
]
# At R5's birth: R5 above R2, and R1 above R5. R3 and R5 get no edge.
EDGES = [(4, "R5", "R2"), (4, "R1", "R5")]
# Case 9: a reported error whose answer was left unplaced; nothing is born.
UNBORN = [(9, ERR)]
CORPUS = [ticket() for _ in range(10)]


def record(edges=EDGES):
    rows = [{"idx": i, "edge_reasons": []} for i in range(len(CORPUS))]
    rules, escalations, log = [], [], []
    for cause, rule in BIRTHS:
        rules.append(rule)
        escalations.append({"idx": rule["born_at"], "kind": cause, "verdict": "nacida",
                            "rule_id": rule["rule_id"]})
    for idx, cause in UNBORN:
        escalations.append({"idx": idx, "kind": cause, "verdict": "sin_situar",
                            "rule_id": None})
    for born, w, l in edges:
        rows[born]["edge_reasons"].append(EDGE_OK)
        log.append([w, l, EDGE_OK])
    escalations.sort(key=lambda e: e["idx"])
    return {"rules": rules, "records": rows, "edge_log": log, "escalations": escalations}


def fraction(k):
    return {"fraction": str(F(k, N_POINTS))}


# Right after each birth, by hand.
RIGHT = [26880, 53760, 80640, 73920, 60480, 67200, 62160, 63840, 63504]
STAGE_C = {"space": fraction(63504),
           "curve": [{"case": 1, "loop": fraction(53760)},
                     {"case": 4, "loop": fraction(60480)},
                     {"case": 9, "loop": fraction(63504)}]}


def read(rec=None, stage_c=STAGE_C, final_rec=None):
    rec = rec or record()
    final = erb.rebuild(final_rec or rec, CORPUS, SPACE).engine
    return G.read_run(rec, SPACE, TRUTH, CASES, stage_c, final=final)


def gate(run, k):
    return next(g for g in run["gates"] if g["gate"] == k)["passes"]


class TestTheMasks(unittest.TestCase):

    def test_the_decision_and_its_points_right(self):
        a, b = PRODUCT["api"], SPACE.mask["channel"]["chat"]
        dec = G.decision({"A": a, "B": b}, {"A": T2, "B": AM})
        self.assertEqual(dec["two"], a & b)
        self.assertEqual(dec["one"], a | b)
        self.assertEqual(G.right_of(dec, TRUTH), a & ~b)

    def test_the_reading_at_a_point(self):
        a, b = PRODUCT["api"], SPACE.mask["channel"]["chat"]
        dec = G.decision({"A": a, "B": b}, {"A": T2, "B": AM})
        j = ((a & ~b) & -(a & ~b)).bit_length() - 1
        self.assertEqual(G.reading_at(dec, j), (G.ACTION, T2))
        k = ((a & b) & -(a & b)).bit_length() - 1
        self.assertEqual(G.reading_at(dec, k), (G.CONFLICT_OUTCOME, None))
        none = SPACE.full & ~(a | b)
        self.assertEqual(G.reading_at(dec, none.bit_length() - 1), (G.IMPASSE, None))

    def test_the_ends_of_a_mask(self):
        self.assertEqual(G.ends(0), [])
        self.assertEqual(G.ends(0b1000), [3])
        self.assertEqual(G.ends(0b101000), [3, 5])

    def test_case_k_is_bit_n_minus_one_minus_k(self):
        for k in (0, 12345, N_POINTS - 1):
            m = SPACE.full
            for a in ATTRIBUTES:
                m &= SPACE.mask[a][getattr(CASES[k], a)]
            self.assertEqual(m, 1 << (N_POINTS - 1 - k))


class TestTheCurve(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.got = read()
        cls.s = cls.got["summary"]

    def test_the_points_right_after_every_birth(self):
        self.assertEqual([c["right"] for c in self.got["curve"]], RIGHT)

    def test_each_birth_counts_the_reported_errors_up_to_it(self):
        self.assertEqual([c["errors"] for c in self.got["curve"]], [0, 0, 0, 1, 2, 2, 2, 3, 3])
        self.assertEqual([c["cause"] for c in self.got["curve"]][3:5], [ERR, ERR])

    def test_the_peak_is_the_first_birth_with_the_most_right(self):
        p = self.s["peak"]
        self.assertEqual((p["birth"], p["born_at"], p["rule_id"], p["right"]),
                         (3, 2, "R3", 80640))
        self.assertEqual(self.s["births"], 9)

    def test_the_fall_is_what_was_lost_less_what_was_gained(self):
        self.assertEqual(self.s["fall_points"], 80640 - 63504)
        self.assertEqual(self.s["lost"]["points"] - self.s["gained"]["points"],
                         self.s["fall_points"])
        self.assertEqual(self.s["fall"]["fraction"], str(F(80640 - 63504, N_POINTS)))
        self.assertEqual(self.s["final"]["right"], 63504)

    def test_the_points_lost_and_gained_by_true_queue(self):
        self.assertEqual(self.s["lost"]["points"], 23856)
        self.assertEqual(self.s["lost"]["by_true_queue"], {T2: 10416, BI: 6720, T1: 6720})
        self.assertEqual(self.s["gained"], {"points": 6720, "by_true_queue": {T1: 6720}})
        self.assertEqual(self.s["lost"]["keyword"], 23856 // 2)

    def test_each_kind_of_loss_falls_where_it_was_placed(self):
        self.assertEqual(self.s["lost"]["by_kind"],
                         {G.BY_CONTAINMENT: 6720 + 3360 + 336, G.BY_EDGE: 6720,
                          G.CONFLICT: 6720})

    def test_the_takers_at_their_last_losses(self):
        got = [(t["rule_id"], t["cause"], t["action"], t["points"], t["by_kind"])
               for t in self.got["takers"]]
        none = {G.BY_CONTAINMENT: 0, G.BY_EDGE: 0, G.CONFLICT: 0}
        self.assertEqual(got, [
            ("R4", ERR, T3, 6720, {**none, G.BY_CONTAINMENT: 6720}),
            ("R5", ERR, AM, 13440, {**none, G.BY_EDGE: 6720, G.CONFLICT: 6720}),
            ("R7", CON, BI, 3360, {**none, G.BY_CONTAINMENT: 3360}),
            ("R9", IMP, AM, 336, {**none, G.BY_CONTAINMENT: 336}),
        ])

    def test_a_point_won_back_and_lost_again_is_read_at_its_last_loss(self):
        """R7 took `api` with `portal` and severity 2 from R1, R8 won it back,
        and R9 took its `en` tickets: those are R9's, and the rest is nobody's."""
        r7 = next(t for t in self.got["takers"] if t["rule_id"] == "R7")
        r9 = next(t for t in self.got["takers"] if t["rule_id"] == "R9")
        self.assertEqual((r7["points"], r9["points"]), (5040 - 1680, 336))
        self.assertNotIn("R8", [t["rule_id"] for t in self.got["takers"]])

    def test_the_losses_by_cause_and_by_the_newborns_queue(self):
        self.assertEqual(self.s["lost"]["by_cause"], {ERR: 20160, CON: 3360, IMP: 336})
        self.assertEqual(self.s["lost"]["by_newborn_queue"], {T3: 6720, AM: 13776, BI: 3360})
        self.assertEqual(self.s["lost"]["security_by_newborn_queue"], {})
        self.assertEqual((self.s["lost"]["takers"], self.s["lost"]["top"]), (4, 23856))

    def test_the_points_lost_in_the_final_base(self):
        self.assertEqual(self.s["lost"]["in_the_final_base"],
                         {"decided_by": {T3: 5040, AM: 7056, BI: 3360},
                          "conflict": 1680 + 6720, "impasse": 0})

    def test_what_the_births_after_the_peak_did_in_all(self):
        self.assertEqual(self.s["after_the_peak"],
                         {"births": 6, "by_cause": {ERR: 3, IMP: 2, CON: 1},
                          "lost": 6720 + 13440 + 5040 + 336, "gained": 6720 + 1680,
                          "lost_by_kind": {G.BY_CONTAINMENT: 6720 + 5040 + 336,
                                           G.BY_EDGE: 6720, G.CONFLICT: 6720}})


class TestTheGates(unittest.TestCase):

    def test_all_four_pass_on_the_run(self):
        got = read()
        self.assertEqual([g["passes"] for g in got["gates"]], [True] * 4)
        self.assertTrue(all(got["checks"].values()))

    def test_gate_1_fails_on_another_base(self):
        got = read(final_rec=record(edges=EDGES[1:]))
        self.assertFalse(gate(got, 1))
        self.assertTrue(gate(got, 3))

    def test_gate_2_fails_off_a_checkpoint_or_off_the_final_share(self):
        off = {**STAGE_C, "curve": [{"case": 4, "loop": fraction(60481)}]}
        self.assertFalse(gate(read(stage_c=off), 2))
        self.assertFalse(gate(read(stage_c={**STAGE_C, "space": fraction(63503)}), 2))
        self.assertTrue(gate(read(stage_c={"space": fraction(63504)}), 2))

    def test_gate_3_fails_on_an_edge_between_two_older_rules(self):
        """R3 placed above R5 at R7's birth: an edge without the newborn. The
        masks kept birth by birth miss it, and the final base's do not."""
        rec = record(edges=EDGES + [(6, "R3", "R5")])
        got = read(rec=rec, stage_c={"space": fraction(63504 + 6720)})
        self.assertFalse(gate(got, 3))
        self.assertFalse(got["checks"]["newborn_at_each_end"])
        self.assertFalse(got["checks"]["masks"])
        self.assertFalse(got["checks"]["decide"])

    def test_gate_3_fails_when_a_reading_is_not_the_engines(self):
        with mock.patch.object(G, "is_the_engines", return_value=False):
            got = read()
        self.assertFalse(gate(got, 3))
        self.assertTrue(gate(got, 1) and gate(got, 2) and gate(got, 4))

    def test_gate_4_fails_when_a_loss_goes_unread(self):
        replay = G.replay

        def without_r5s_losses(*a, **k):
            rep = replay(*a, **k)
            for s in rep["steps"]:
                if s["rule_id"] == "R5":
                    s["lost"] = 0
            return rep

        with mock.patch.object(G, "replay", side_effect=without_r5s_losses):
            got = read()
        self.assertFalse(gate(got, 4))
        self.assertTrue(gate(got, 1) and gate(got, 2) and gate(got, 3))


def summary(points=100, sec=50, alone=50, error=50, births=10, births_error=5,
            sec_t2=25, top=50, fall=10):
    return {"lost": {"points": points, "by_true_queue": {G.SEC: sec},
                     "by_kind": {G.BY_CONTAINMENT: alone, G.BY_EDGE: 0,
                                 G.CONFLICT: points - alone},
                     "by_cause": {ERR: error}, "security_by_newborn_queue": {G.T2: sec_t2},
                     "top": top},
            "after_the_peak": {"births": births, "by_cause": {ERR: births_error}},
            "fall_points": fall, "fall": G.frac(F(fall, N_POINTS))}


def runs_of(l_runs, n_runs):
    out = {}
    for k, (l, n) in enumerate(zip(l_runs, n_runs), start=1):
        out[plan.tag(plan.LABELLED, k)] = {"summary": l}
        out[plan.tag(G.UNLABELLED, k)] = {"summary": n}
    return out


def clauses(l_runs, n_runs=None):
    n_runs = n_runs or [summary(fall=9)] * 3
    return {c["clause"]: c["holds"] for c in G.read_expectation(runs_of(l_runs, n_runs))}


class TestTheExpectation(unittest.TestCase):

    def test_every_clause_holds_at_its_line(self):
        self.assertEqual(clauses([summary()] * 3),
                         {q: True for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")})

    def test_q1_and_q5_read_each_run(self):
        got = clauses([summary(), summary(), summary(sec=49, top=49)])
        self.assertFalse(got["Q1"])
        self.assertFalse(got["Q5"])
        self.assertTrue(got["Q2"] and got["Q4"])

    def test_q2_q3_and_q4_pool_the_runs(self):
        got = clauses([summary(alone=49, error=49, sec_t2=24), summary(), summary()])
        self.assertEqual((got["Q2"], got["Q3"], got["Q4"]), (False, False, False))
        got = clauses([summary(alone=49, error=49, sec_t2=24), summary(alone=51, error=51,
                                                                       sec_t2=26), summary()])
        self.assertEqual((got["Q2"], got["Q3"], got["Q4"]), (True, True, True))

    def test_q3_reads_the_births_after_the_peaks(self):
        self.assertFalse(clauses([summary(births_error=6), summary(), summary()])["Q3"])
        self.assertTrue(clauses([summary(births_error=4), summary(), summary()])["Q3"])

    def test_q6_reads_each_pair(self):
        self.assertFalse(clauses([summary()] * 3, [summary(fall=9), summary(fall=10),
                                                   summary(fall=9)])["Q6"])
        self.assertTrue(clauses([summary()] * 3, [summary(fall=0)] * 3)["Q6"])

    def test_a_clause_over_nothing_fails(self):
        nothing = summary(points=0, sec=0, alone=0, error=0, births=0, births_error=0,
                          sec_t2=0, top=0)
        got = clauses([nothing] * 3)
        self.assertEqual({q: got[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")},
                         {q: False for q in ("Q1", "Q2", "Q3", "Q4", "Q5")})
        self.assertFalse({c["clause"]: c["holds"] for c in G.read_expectation({})}["Q6"])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(G, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                G.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
