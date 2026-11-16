"""
`corrections/guard.py` — the POST-RUN reading of the ranking as it went, with a
guard on containment. No figure of the reading.

What is pinned is the instrument:
- the guard sets aside a rule strictly inside a rule of a queue ranked above its
  own, and no other: not one inside a rule of a lower queue or of its own, nor
  one inside nothing;
- what an order of the base the guard keeps decides is the engine's own
  decision and first match's, over the real space and policy, and the mask
  counts what `corrections/online.py` counts;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import guard as G
from corrections import hierarchy as H
from corrections import online as ON
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from manual import compile as MC
from manual import instrument as MI
from rung2.engine2 import EDGE_OK
from tests.test_corrections_shape import UNSIGNED, c_, r_

SPACE = MI.space()
TRUTH = MI.space_truth()
F = Fraction

# The keyword's rule, a rule of another queue nested in it, a crossing billing
# rule, severity 1 to the on-call queue, and a catch-all around them all.
HAND = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
        r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
        r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
        r_("ONCALL_ESCALATION", c_("severity", "eq", 1)),
        r_("T1_GENERAL", c_("severity", "gte", 1))]
SEC_FIRST = ("SECURITY_INCIDENT", "ONCALL_ESCALATION", "BILLING_SPECIALIST", "T3_ENGINEERING",
             "ACCOUNT_MANAGER", "SELF_SERVICE_DEFLECT", "T2_TECHNICAL", "T1_GENERAL")
T2_FIRST = ("T2_TECHNICAL",) + tuple(q for q in SEC_FIRST if q != "T2_TECHNICAL")


class TestTheGuard(unittest.TestCase):

    def setUp(self):
        self.eng = MC.install(HAND, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.by_action = {self.rs.action[r]: r for r in self.rs.ids}

    def test_a_rule_inside_a_higher_queues_is_set_aside(self):
        got = G.set_aside(self.rs, self.rs.ids, H.rank_of(SEC_FIRST))
        self.assertEqual(got, {self.by_action["T2_TECHNICAL"]})

    def test_not_inside_a_lower_queues(self):
        self.assertEqual(G.set_aside(self.rs, self.rs.ids, H.rank_of(T2_FIRST)), set())

    def test_only_among_the_rules_given(self):
        ids = [r for r in self.rs.ids if self.rs.action[r] != "SECURITY_INCIDENT"]
        self.assertEqual(G.set_aside(self.rs, ids, H.rank_of(SEC_FIRST)), set())

    def test_a_rule_inside_one_of_its_own_queue_is_kept(self):
        eng = MC.install([r_("T2_TECHNICAL", c_("severity", "eq", 2)),
                          r_("T2_TECHNICAL", c_("severity", "eq", 2), c_("product", "eq", "api"))],
                         SPACE).engine
        rs = H.rules_of(eng)
        self.assertEqual(G.set_aside(rs, rs.ids, H.rank_of(SEC_FIRST)), set())

    def test_what_the_kept_base_decides_is_the_engines(self):
        rules = {r.rule_id: r for r in self.eng.rules}
        for ranking in (SEC_FIRST, T2_FIRST, tuple(ACTIONS)):
            rank = H.rank_of(ranking)
            aside = G.set_aside(self.rs, self.rs.ids, rank)
            kept = ON.prefix_rules(self.rs, [r for r in self.rs.ids if r not in aside])
            order = H.pulled(kept, rank)
            mask = G.right_mask(order, kept, self.eng.ext, TRUTH, SPACE.n)
            self.assertEqual(mask.bit_count(), ON.right_of(order, kept, self.eng.ext, TRUTH, SPACE.n))
            eng = S.installed_in(order, {r: rules[r] for r in kept.ids}, SPACE)
            self.assertTrue(all(why == EDGE_OK for _, _, why in eng.edge_log))
            self.assertEqual(MI.over_space(eng)["correct"], mask.bit_count())
            self.assertEqual(MI.first_match_over_space([rules[r] for r in order])["correct"],
                             mask.bit_count())

    def test_the_guard_gives_the_container_its_region(self):
        rank = H.rank_of(SEC_FIRST)
        alone = ON.prefix_rules(self.rs, self.rs.ids)
        aside = G.set_aside(self.rs, self.rs.ids, rank)
        kept = ON.prefix_rules(self.rs, [r for r in self.rs.ids if r not in aside])
        with_guard = G.right_mask(H.pulled(kept, rank), kept, self.eng.ext, TRUTH, SPACE.n)
        without = G.right_mask(H.pulled(alone, rank), alone, self.eng.ext, TRUTH, SPACE.n)
        nested = self.eng.ext[self.by_action["T2_TECHNICAL"]]
        self.assertEqual((with_guard ^ without) & ~nested, 0)


def fake(aside2=("R0120",), aside3=("R0104",), both=F(8, 10), at_once=F(7, 10),
         alone=F(75, 100), peak=F(81, 100), final=F(80, 100), record_peak=F(78, 100),
         gained=100, lost=24, runs=G.L_RUNS):
    def sh(x):
        return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}
    out = {}
    for t in runs:
        out[t] = {"checkpoints": [{"both": sh(both), "at_once": sh(at_once),
                                   "ranking_alone": sh(alone)}],
                  "both": {"peak": {"share": sh(peak)}, "final": sh(final)},
                  "record": {"peak": {"share": sh(record_peak)}},
                  "the_guard_at_the_end": {
                      "rules": list(aside2 if t == "l_r2" else aside3 if t == "l_r3" else ()),
                      "gained": {"points": gained}, "lost": {"points": lost}}}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in G.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(aside2=(), both=F(7, 10), alone=F(7, 10), peak=F(8, 10),
                         final=F(779, 1000), record_peak=F(801, 1000), gained=100, lost=25))
        self.assertEqual(got, {"X1": False, "X2": False, "X3": False, "X4": False, "X5": False,
                               "X6": False})
        edge = holds(fake(final=F(79, 100), peak=F(81, 100), record_peak=F(81, 100)))
        self.assertTrue(edge["X3"])
        self.assertTrue(edge["X6"])

    def test_x1_reads_both_runs(self):
        self.assertFalse(holds(fake(aside3=()))["X1"])
        self.assertFalse(holds(fake(runs=("l_r1", "l_r2")))["X1"])

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(G, "online_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                G.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
