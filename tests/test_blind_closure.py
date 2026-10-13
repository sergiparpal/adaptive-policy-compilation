"""
`blind/closure.py` — the POST-RUN reading of what the base's transitive order
would decide, no figure of the runs.

What is pinned is the instrument, on small worlds worked by hand: the
ancestors a chain gives, the undefeated masks with and without the closure, a
CONFLICT the closure resolves and one it cannot, who is right on what it
resolves, the coin's and the ranking's counts, the same on corpus cases, the
case-by-case closure against the masks, the hidden policy still executed through
the closure, the expectation's clauses at their edges, and that the writer
refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from harness.domain import Case

from blind import closure, plan
from rung2.engine2 import EDGE_OK, PriorityEngine, Space, validate_conditions
from rung2.hidden_priority import build_hidden_engine
from rung3.order_search_ls import space_truth_masks

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def rule(action, **conds):
    return validate_conditions(
        {"action": action,
         "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]},
        case=None)


def engine_with(*rules) -> PriorityEngine:
    eng = PriorityEngine(space=SPACE)
    for i, r in enumerate(rules):
        eng.add(r, born_at=i)
    return eng


def case(**over) -> Case:
    base = dict(has_security_keyword=False, severity=2, customer_tier="free",
                product="api", channel="email", prior_tickets_30d=0, off_hours=False,
                language="en")
    return Case(**(base | over))


class TheChain(unittest.TestCase):
    """W (T2: email, api, severity 1) is nested in N (T3: email). X (T1: api,
    free) is declared above W. So X reaches N through W, and on email, api and
    free tickets of severity 2 to 4, where W does not match, rung 2's engine
    leaves X and N in CONFLICT."""

    def setUp(self):
        self.eng = engine_with(rule(T2, channel="email", product="api", severity=1),
                               rule(T1, product="api", customer_tier="free"),
                               rule(T3, channel="email"))
        self.assertEqual(self.eng.try_edge("R0002", "R0001"), EDGE_OK)
        ext = self.eng.ext
        self.region = ext["R0003"] & ext["R0002"] & ~ext["R0001"]
        self.assertTrue(self.region)


class TestTheTwoEngines(TheChain):

    def test_ancestors_follow_the_chain(self):
        anc = closure.ancestors(self.eng)
        self.assertEqual(anc["R0003"], {"R0001", "R0002"})
        self.assertEqual(self.eng.beats_me("R0003"), {"R0001"})
        self.assertEqual((anc["R0001"], anc["R0002"]), ({"R0002"}, set()))

    def test_the_closure_resolves_the_region_and_changes_nothing_else(self):
        q = closure.engines(self.eng)
        one_d, two_d = closure.cover(q["direct"])
        one_c, two_c = closure.cover(q["closure"])
        self.assertEqual(two_d, self.region)
        self.assertEqual(two_c, 0)
        self.assertEqual(one_c, one_d)
        self.assertEqual(q["closure"][T1] & self.region, self.region)
        self.assertEqual(q["closure"].get(T3, 0) & self.region, 0)
        for a, m in q["direct"].items():
            decided = m & one_d & ~two_d
            self.assertEqual(decided & ~q["closure"][a], 0)

    def test_the_case_by_case_closure_is_the_masks(self):
        q = closure.engines(self.eng)
        anc = closure.ancestors(self.eng)
        for c, want in ((case(severity=2), (T1,)), (case(severity=1), (T1,)),
                        (case(product="billing"), (T3,)), (case(channel="chat"), (T1,))):
            with self.subTest(c=c):
                bit = closure.point_of(SPACE, c)
                self.assertEqual(bit.bit_count(), 1)
                outcome, queues = closure.decide_closure(self.eng, anc, c)
                self.assertEqual((outcome, queues), ("ACTION", set(want)))
                self.assertEqual(closure.queues_at(q["closure"], bit), set(want))
        self.assertEqual(self.eng.decide(case(severity=2))[0], "CONFLICT")
        self.assertEqual(closure.decide_closure(self.eng, anc, case(channel="chat",
                                                                    product="mobile")),
                         ("IMPASSE", set()))


class TestWhoIsRight(TheChain):

    def tmask(self, region_queue):
        rest = SPACE.full & ~self.region
        out = {T1: 0, T2: 0, T3: 0, "SECURITY_INCIDENT": rest}
        out[region_queue] |= self.region
        return out

    def test_the_closure_right(self):
        q = closure.engines(self.eng)
        got = closure.read_space(q, self.tmask(T1), SPACE.n, 0)
        n = self.region.bit_count()
        self.assertEqual((got["conflicts"], got["resolved"], got["closure"],
                          got["overruled"], got["neither"]), (n, n, n, 0, 0))
        self.assertEqual(got["coin"], n / 2)
        self.assertEqual(got["ranking"], 0)      # T3 ranks above T1
        self.assertEqual(got["closure_correct"] - got["direct_correct"], n)

    def test_the_side_it_overrules_right(self):
        q = closure.engines(self.eng)
        got = closure.read_space(q, self.tmask(T3), SPACE.n, self.region)
        n = self.region.bit_count()
        self.assertEqual((got["closure"], got["overruled"], got["neither"], got["ranking"],
                          got["in_refused_regions"]), (0, n, 0, n, n))

    def test_neither_right(self):
        q = closure.engines(self.eng)
        got = closure.read_space(q, self.tmask(T2), SPACE.n, 0)
        n = self.region.bit_count()
        self.assertEqual((got["closure"], got["overruled"], got["neither"], got["coin"]),
                         (0, 0, n, 0))

    def test_on_corpus_cases(self):
        q = closure.engines(self.eng)
        cases = [case(severity=2), case(severity=3), case(severity=1), case(channel="chat")]
        bits = [closure.point_of(SPACE, c) for c in cases]
        got = closure.read_corpus(q, bits, [T3, T1, T2, T1], self.region)
        self.assertEqual((got["n"], got["conflicts"], got["resolved"], got["closure"],
                          got["overruled"], got["ranking"], got["in_refused_regions"]),
                         (4, 2, 2, 1, 1, 1, 2))
        self.assertEqual((got["coin"], got["direct_correct"], got["closure_correct"]),
                         (1.0, 1, 2))
        s = closure.shares(got)
        self.assertEqual((s["closure"], s["resolved_of_conflicts"], s["gain"]),
                         (0.5, 1.0, 0.25))


class TestACONFLICTNoChainOrders(unittest.TestCase):

    def test_two_crossing_rules_without_an_edge_stay_in_conflict(self):
        eng = engine_with(rule(T1, product="billing"), rule(T2, customer_tier="free"))
        q = closure.engines(eng)
        self.assertEqual(closure.cover(q["closure"])[1], closure.cover(q["direct"])[1])
        got = closure.read_space(q, {T1: SPACE.full, T2: 0}, SPACE.n, 0)
        self.assertGreater(got["conflicts"], 0)
        self.assertEqual(got["resolved"], 0)
        self.assertIsNone(closure.shares(got)["closure"])


class TestCounting(unittest.TestCase):

    def test_at_least_and_exactly(self):
        k = closure.at_least({"a": 0b0011, "b": 0b0110, "c": 0b0100})
        self.assertEqual((k[1], k[2], k[3]), (0b0111, 0b0110, 0))
        self.assertEqual((closure.exactly(k, 1), closure.exactly(k, 2)), (0b0001, 0b0110))

    def test_pooled_sums_the_counts(self):
        r = {k: 1 for k in closure.COUNTS} | {"coin": 0.5, "n": 10, "conflicts": 2}
        got = closure.pooled([r, r])
        self.assertEqual((got["counts"]["resolved"], got["counts"]["coin"],
                          got["counts"]["n"]), (2, 1.0, 20))
        self.assertEqual(got["shares"]["resolved_of_conflicts"], 0.5)


class TestStopZero(unittest.TestCase):

    def test_the_hidden_policy_through_the_closure(self):
        hidden, _, _ = build_hidden_engine(SPACE)
        q = closure.engines(hidden)
        got = closure.read_space(q, space_truth_masks(SPACE), SPACE.n, 0)
        self.assertEqual((got["conflicts"], got["resolved"]), (0, 0))
        self.assertEqual(got["closure_correct"], SPACE.n)


class TestTheExpectation(unittest.TestCase):

    def bases(self, forced, v1, closure_right, coin, ranking, gain):
        out = {}
        for p in closure.PROTOCOLS:
            for r in plan.BASELINE_REPS:
                conflicts, resolved = 10, (forced if p != "v1" else v1)
                counts = {k: 0 for k in closure.COUNTS} | {
                    "n": 100, "conflicts": conflicts, "resolved": resolved,
                    "closure": closure_right, "coin": coin, "ranking": ranking}
                out[(p, r)] = {"space": {"counts": counts, "shares": {"gain": gain}}}
        return out

    def test_clause_by_clause(self):
        x = closure.read_expectation(self.bases(10, 4, 5, 5.5, 6, 0.009))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])
        x = closure.read_expectation(self.bases(9, 5, 9, 5, 9, 0.01))
        self.assertEqual([c["holds"] for c in x], [False, False, False, False, False])

    def test_no_resolved_point_leaves_clauses_3_and_4_unread(self):
        x = closure.read_expectation(self.bases(0, 0, 0, 0, 0, 0.0))
        self.assertEqual((x[2]["holds"], x[3]["holds"]), (None, None))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                closure.main([])
        read.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
