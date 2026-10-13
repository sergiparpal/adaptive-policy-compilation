"""
`blind/yielding.py` — the POST-RUN reading of which edge of a cycle should
yield, no figure of the runs.

What is pinned is the instrument, on small worlds worked by hand: the log given
back to the escalations that wrote it, the order each arm installs the
declarations in, which edge of a cycle yields under arrival and under recency,
the ranking's and the oracle's groups, the coin seeded, every arm acyclic and
full, what changes against the arrival arm under rung 2's engine and through the
closure, the corpus counted as it arrives, the coin's summaries and the pool,
the hidden policy kept whole under every order, the expectation's clauses at
their edges, and that the writer refuses unsigned before it reads or writes.
Added after the first run: the two halves of the space adding up to the whole,
and pooled as the whole is. Added after the second run: the coin's draws split by
whether they refused a declaration the keyword's queue wins.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from harness.domain import Case

from blind import closure, plan, rows, yielding
from rung2.engine2 import (EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK, PriorityEngine, Space,
                           validate_conditions)

SPACE = Space()
T1, T2, T3, SEC = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING", "SECURITY_INCIDENT"
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


def decl(k, case, w, l, why, channel="write"):
    return {"k": k, "case": case, "winner": w, "loser": l, "verdict": why,
            "channel": channel}


class TheCycle(unittest.TestCase):
    """W (T2: email, api, severity 1) is nested in N (T3: email). X (T1: api,
    free) was declared above W at case 10. At case 20 N was declared above X,
    which closes N > X > W > N, since W beats N by subsumption. A third
    declaration, between rules that never meet, was refused as disjoint."""

    def setUp(self):
        self.bare = engine_with(rule(T2, channel="email", product="api", severity=1),
                                rule(T1, product="api", customer_tier="free"),
                                rule(T3, channel="email"),
                                rule(T1, channel="chat"))
        self.older = decl(0, 10, "R0002", "R0001", EDGE_OK)
        self.newer = decl(1, 20, "R0003", "R0002", EDGE_CYCLE)
        self.idle = decl(2, 20, "R0001", "R0004", EDGE_DISJOINT)
        self.decls = [self.older, self.newer, self.idle]
        self.action = {r.rule_id: r.action for r in self.bare.rules}
        ext = self.bare.ext
        self.contested = ext["R0003"] & ext["R0002"] & ~ext["R0001"]
        self.inner = ext["R0001"] & ext["R0002"]
        self.assertTrue(self.contested and self.inner)

    def tmask(self, contested, inner):
        rest = SPACE.full & ~self.contested & ~self.inner
        out = {T1: 0, T2: 0, T3: 0, SEC: rest}
        out[contested] |= self.contested
        out[inner] |= self.inner
        return out

    def graph(self, arm, tmask=None):
        order = yielding.priority(arm, self.decls, self.action, self.bare.ext,
                                  tmask or self.tmask(T3, T1))
        return yielding.install(self.bare, order)


class TestWhichEdgeYields(TheCycle):

    def test_only_the_accepted_and_the_cyclic_are_ordered(self):
        self.assertEqual(yielding.ordered(self.decls), [self.older, self.newer])

    def test_under_arrival_the_newest_yields(self):
        eng, refused = self.graph("arrival")
        self.assertEqual(refused, [self.newer])
        self.assertEqual(yielding.edges_of(eng), {("R0002", "R0001")})

    def test_under_recency_the_oldest_yields(self):
        eng, refused = self.graph("recency")
        self.assertEqual(refused, [self.older])
        self.assertEqual(yielding.edges_of(eng), {("R0003", "R0002")})

    def test_recency_keeps_an_escalations_own_order(self):
        ds = [decl(0, 5, "a", "b", EDGE_OK), decl(1, 9, "c", "d", EDGE_OK),
              decl(2, 9, "e", "f", EDGE_CYCLE), decl(3, 7, "g", "h", EDGE_OK)]
        got = yielding.priority("recency", ds, {}, {}, {})
        self.assertEqual([d["k"] for d in got], [1, 2, 3, 0])

    def test_the_ranking_keeps_what_agrees_with_it(self):
        # T3 ranks above T1 and T1 below T2: N over X agrees, X over W does not.
        eng, refused = self.graph("ranking")
        self.assertEqual(refused, [self.older])
        ds = [decl(0, 1, "R0002", "R0004", EDGE_OK), decl(1, 2, "R0002", "R0001", EDGE_OK),
              decl(2, 3, "R0003", "R0002", EDGE_OK)]
        got = yielding.priority("ranking", ds, self.action, {}, {})
        self.assertEqual([d["k"] for d in got], [2, 0, 1])     # agrees, one queue, against

    def test_the_oracle_follows_the_truth_over_the_shared_region(self):
        # N's queue true where N and X meet outside W: N over X is the better.
        _, refused = self.graph("oracle", self.tmask(T3, T3))
        self.assertEqual(refused, [self.older])
        # X's queue true there and on W: X over W is the better, N over X the worse.
        _, refused = self.graph("oracle", self.tmask(T1, T1))
        self.assertEqual(refused, [self.newer])

    def test_the_coin_is_a_function_of_its_seed(self):
        many = [decl(k, k, f"w{k}", f"l{k}", EDGE_OK) for k in range(30)]
        a = yielding.coin_order(many, ("v2b", 1), 0)
        self.assertEqual(a, yielding.coin_order(many, ("v2b", 1), 0))
        self.assertNotEqual(a, yielding.coin_order(many, ("v2b", 1), 1))
        self.assertNotEqual(a, yielding.coin_order(many, ("v2b", 3), 0))
        self.assertEqual(sorted(d["k"] for d in a), list(range(30)))

    def test_every_arm_is_acyclic_and_full(self):
        for arm in yielding.ARMS:
            with self.subTest(arm=arm):
                self.assertTrue(yielding.acyclic_and_full(*self.graph(arm)))
        eng, _ = self.graph("arrival")
        self.assertFalse(yielding.acyclic_and_full(eng, [self.idle]))


class TestWhatChanges(TheCycle):

    def readings(self, tmask, mult=None):
        m = {a: yielding.masks(self.graph(a, tmask)[0], tmask) for a in ("arrival", "recency")}
        return {e: yielding.against(m["recency"][e], m["arrival"][e], mult)
                for e in yielding.ENGINES}, m

    def test_under_rung_2s_engine_recency_resolves_and_flips(self):
        got, _ = self.readings(self.tmask(T3, T1))
        d = got["direct"]
        c, i = self.contested.bit_count(), self.inner.bit_count()
        self.assertEqual((d["resolved_right"], d["resolved_wrong"]), (c, 0))
        self.assertEqual((d["flipped_arrival_right"], d["flipped_arm_right"],
                          d["flipped_neither"]), (i, 0, 0))
        self.assertEqual((d["gained"], d["lost"]), (c, i))
        self.assertEqual((d["unresolved_was_right"], d["unresolved_was_wrong"]), (0, 0))
        self.assertEqual(d["gained"], d["resolved_right"] + d["flipped_arm_right"])
        self.assertEqual(d["lost"], d["unresolved_was_right"] + d["flipped_arrival_right"])

    def test_through_the_closure_both_resolve_and_only_the_direction_differs(self):
        got, m = self.readings(self.tmask(T3, T1))
        cl = got["closure"]
        c, i = self.contested.bit_count(), self.inner.bit_count()
        self.assertEqual((m["arrival"]["closure"]["conflict"], m["recency"]["closure"]["conflict"]),
                         (0, 0))
        self.assertEqual(m["arrival"]["direct"]["conflict"], self.contested)
        self.assertEqual((cl["resolved_right"], cl["unresolved_was_right"]), (0, 0))
        self.assertEqual((cl["flipped_arm_right"], cl["flipped_arrival_right"]), (c, i))
        # Letting N over X stand leaves no CONFLICT even under rung 2's engine here.
        self.assertEqual(m["recency"]["direct"]["conflict"], 0)

    def test_neither_side_right(self):
        # A third queue is true where N and X meet: whoever decides there is wrong.
        got, _ = self.readings(self.tmask(T2, T3))
        d = got["direct"]
        c, i = self.contested.bit_count(), self.inner.bit_count()
        self.assertEqual((d["resolved_right"], d["resolved_wrong"]), (0, c))
        self.assertEqual((d["flipped_arm_right"], d["flipped_arrival_right"],
                          d["flipped_neither"]), (0, 0, i))
        self.assertEqual((d["gained"], d["lost"]), (0, 0))

    def test_on_corpus_cases_as_they_arrive(self):
        bits = [closure.point_of(SPACE, c) for c in (
            case(severity=2), case(severity=2), case(severity=3),
            case(severity=1), case(channel="chat"))]
        mult = yielding.multiplicity(bits)
        self.assertEqual(sorted(mult), [1, 2])
        self.assertEqual(yielding.weigh(bits[0] | bits[2], mult), 3)
        got, _ = self.readings(self.tmask(T3, T1), mult)
        d = got["direct"]
        self.assertEqual((d["resolved_right"], d["flipped_arrival_right"]), (3, 1))


class TestTheTwoHalves(TheCycle):
    """Added after the first run: every count on the half of the space without
    the keyword and on the half with it."""

    def test_the_halves_add_up_to_the_whole(self):
        tmask = self.tmask(T3, T1)
        m = {a: yielding.masks(self.graph(a, tmask)[0], tmask) for a in ("arrival", "recency")}
        bits = [closure.point_of(SPACE, c) for c in (
            case(severity=2), case(severity=2, has_security_keyword=True), case(severity=1))]
        mult = yielding.multiplicity(bits)
        outside = rows.outside_mask(SPACE)
        whole = yielding.reading(m["recency"], m["arrival"], mult)
        halves = yielding.by_half(m["recency"], m["arrival"], mult, outside, SPACE.full)
        for e in yielding.ENGINES:
            for s in yielding.SURFACES:
                for c in yielding.COUNTS:
                    with self.subTest(engine=e, surface=s, count=c):
                        self.assertEqual(whole[e][s][c], halves[e]["outside"][s][c]
                                         + halves[e]["keyword"][s][c])
        d = halves["direct"]
        self.assertEqual((d["outside"]["corpus"]["resolved_right"],
                          d["keyword"]["corpus"]["resolved_right"]), (1, 1))
        self.assertEqual(d["outside"]["space"]["resolved_right"],
                         (self.contested & outside).bit_count())

    def test_the_halves_pool_the_bases_with_a_cycle(self):
        counts = {c: 1 for c in yielding.COUNTS}
        arms = {a: {e: {h: {s: dict(counts) for s in yielding.SURFACES}
                        for h in yielding.HALVES} for e in yielding.ENGINES}
                for a in yielding.ARMS}
        draw = {e: {h: {s: {c: 2 for c in yielding.DRAWN} for s in yielding.SURFACES}
                    for h in yielding.HALVES} for e in yielding.ENGINES}
        cyc = {"cycle": True, "_halves": arms, "_draws_halves": [draw] * yielding.N_COIN}
        got = yielding.halves_of({("v2e", 1): cyc, ("v2b", 1): cyc,
                                  ("v1", 1): {"cycle": False, "_halves": arms}})
        self.assertEqual(sorted(got["bases"]), ["v1 1", "v2b 1", "v2e 1"])
        self.assertNotIn("coin", got["bases"]["v1 1"])
        self.assertEqual(got["pooled"]["arms"]["recency"]["closure"]["keyword"]["space"]["lost"], 2)
        coin = got["pooled"]["coin"]["outside"]["closure"]["space"]
        self.assertEqual((coin["right"]["mean"], coin["at_least"]["oracle"]), (4, 1.0))


class TestTheCoinsDrawsByWhatTheyRefused(unittest.TestCase):
    """Added after the second run: the draws that refused a declaration the
    keyword's queue wins, apart from the rest."""

    def test_counting_and_splitting(self):
        action = {"K": SEC, "A": T1, "B": T2}
        refused = [decl(0, 1, "K", "A", EDGE_CYCLE), decl(1, 2, "A", "K", EDGE_CYCLE),
                   decl(2, 3, "B", "A", EDGE_CYCLE)]
        self.assertEqual(yielding.keyword_winners(refused, action), 1)
        draws = [{"closure": {h: {"space": {"right": x + (h == "keyword")}}
                              for h in yielding.HALVES}} for x in (10, 20, 30, 40)]
        got = yielding.split_by_keyword(draws, {"draws": [0, 2, 0, 1], "arms": {"arrival": 1}})
        self.assertEqual(got["arms_refused"], {"arrival": 1})
        self.assertEqual((got["refusing_one"]["draws"], got["refusing_none"]["draws"]), (2, 2))
        self.assertEqual(got["refusing_one"]["outside"]["mean"], 30)
        self.assertEqual(got["refusing_none"]["keyword"]["mean"], 21)
        none = yielding.split_by_keyword(draws, {"draws": [0, 0, 0, 0], "arms": {}})
        self.assertIsNone(none["refusing_one"]["outside"])


class TestTheLog(unittest.TestCase):

    def record(self, reasons, log):
        return {"edge_log": log, "edge_channels": ["write"] * len(log),
                "records": [{"idx": i, "edge_reasons": r} for i, r in enumerate(reasons)]}

    def test_each_entry_goes_to_the_case_that_wrote_it(self):
        log = [["R1", "R2", EDGE_OK], ["R3", "R1", EDGE_CYCLE], ["R3", "R2", EDGE_DISJOINT]]
        rec = self.record([[], [EDGE_OK], [], ["fuera_del_vecindario", EDGE_CYCLE,
                                                EDGE_DISJOINT]], log)
        got, ok = yielding.attribute(rec)
        self.assertTrue(ok)
        self.assertEqual([(d["k"], d["case"], d["verdict"]) for d in got],
                         [(0, 1, EDGE_OK), (1, 3, EDGE_CYCLE), (2, 3, EDGE_DISJOINT)])

    def test_a_verdict_out_of_place_or_an_entry_left_over_fails(self):
        log = [["R1", "R2", EDGE_OK], ["R3", "R1", EDGE_CYCLE]]
        self.assertFalse(yielding.attribute(self.record([[EDGE_CYCLE], [EDGE_OK]], log))[1])
        self.assertFalse(yielding.attribute(self.record([[EDGE_OK]], log))[1])

    def test_a_record_without_channels_is_the_write_channels(self):
        rec = {"edge_log": [["R1", "R2", EDGE_OK]],
               "records": [{"idx": 0, "edge_reasons": [EDGE_OK]}]}
        got, ok = yielding.attribute(rec)
        self.assertTrue(ok)
        self.assertEqual(got[0]["channel"], "write")


class TestTheCoinsSummaries(unittest.TestCase):

    def draws(self, rights):
        out = []
        for x in rights:
            counts = {c: 0 for c in yielding.DRAWN} | {"right": x}
            out.append({e: {s: dict(counts) for s in yielding.SURFACES}
                        for e in yielding.ENGINES})
        return out

    def test_central_ninety(self):
        self.assertEqual(yielding.central(list(range(200))), [10, 189])

    def test_summary_and_at_least(self):
        arms = {a: {e: {s: {"right": 150} for s in yielding.SURFACES} for e in yielding.ENGINES}
                for a in yielding.ARMS}
        got = yielding.summary(self.draws(range(200)), arms)
        s = got["closure"]["space"]
        self.assertEqual((got["draws"], s["right"]["mean"], s["right"]["central"]),
                         (200, 99.5, [10, 189]))
        self.assertEqual(s["at_least"]["recency"], 0.25)

    def test_pooled_sums_the_bases_with_a_cycle_draw_by_draw(self):
        counts = {c: 1 for c in yielding.COUNTS}
        arms = {a: {e: {s: dict(counts) for s in yielding.SURFACES} for e in yielding.ENGINES}
                for a in yielding.ARMS}
        cyc = {"cycle": True, "arms": arms, "_draws": self.draws(range(yielding.N_COIN))}
        bases = {("v2e", 1): cyc, ("v2b", 1): cyc, ("v1", 1): {"cycle": False, "arms": arms}}
        got = yielding.pooled(bases)
        self.assertEqual(got["bases"], ["v2e 1", "v2b 1"])
        self.assertEqual(got["arms"]["oracle"]["direct"]["corpus"]["lost"], 2)
        self.assertEqual(got["coin_right_by_draw"]["closure"][:3], [0, 2, 4])


class TestStopZero(unittest.TestCase):

    def test_the_hidden_policy_keeps_every_edge_under_every_order(self):
        from rung3.order_search_ls import space_truth_masks
        got = yielding.stop_zero(SPACE, space_truth_masks(SPACE))
        self.assertEqual(set(got), {"reversed", "shuffled"})
        for name, x in got.items():
            with self.subTest(name):
                self.assertTrue(x["passes"])
                self.assertEqual(x["refused"], 0)
                self.assertEqual(x["right"], {"direct": SPACE.n, "closure": SPACE.n})


class TestTheExpectation(unittest.TestCase):

    def arms(self, direct, closure_right, wrong=0):
        """`direct` and `closure_right`: {arm: right}, over the space."""
        out = {}
        for a in yielding.ARMS:
            counts = {c: 0 for c in yielding.COUNTS}
            out[a] = {"direct": {s: counts | {"right": direct[a], "wrong": wrong if a == "recency"
                                               else 0} for s in yielding.SURFACES},
                      "closure": {s: counts | {"right": closure_right[a]}
                                  for s in yielding.SURFACES}}
        return out

    def world(self, gains, per_base, pooled_right, coin_mean, central):
        right = {"arrival": 10, "recency": 10 + gains, "ranking": 0, "oracle": 0}
        bases = {yielding.GAINS: {"arms": self.arms(right, right, wrong=gains)}}
        for key, d in zip(yielding.FEWER, per_base):
            r = {"arrival": 10, "recency": 10 + d, "ranking": 0, "oracle": 0}
            bases[key] = {"arms": self.arms(r, r)}
        pool = {"arms": self.arms(pooled_right, pooled_right),
                "coin": {"closure": {"space": {"right": {"mean": coin_mean,
                                                          "central": central}}}}}
        return bases, pool

    def test_clause_by_clause(self):
        good = {"arrival": 100, "recency": 110, "ranking": 120, "oracle": 130}
        x = yielding.read_expectation(*self.world(5, (-1, -1), good, 105, [90, 115]))
        self.assertEqual([c["holds"] for c in x], [True, True, True, True, True])
        bad = {"arrival": 100, "recency": 100, "ranking": 100, "oracle": 100}
        x = yielding.read_expectation(*self.world(0, (0, 1), bad, 101, [101, 102]))
        self.assertEqual([c["holds"] for c in x], [False, False, False, False, False])

    def test_the_fifth_clause_counts_the_coins_mean(self):
        good = {"arrival": 100, "recency": 110, "ranking": 120, "oracle": 130}
        x = yielding.read_expectation(*self.world(5, (-1, -1), good, 131, [90, 115]))
        self.assertEqual(x[4]["holds"], False)


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                yielding.main([])
        read.assert_not_called()
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
