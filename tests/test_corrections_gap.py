"""
`corrections/gap.py` — the POST-RUN reading of what the rest of what the declared
ranking lacks is. No figure of the reading.

What is pinned is the instrument:
- the swap exchanges the two queues and nothing else, and the pairs two rankings
  order against each other;
- the policy's eight layers partitioning the space, each the union of its rules'
  regions, and the two queues' points lying in their layers;
- the decomposition's arithmetic, and what an order gains and loses;
- the votes on the pair, each oriented by its side and cast by its newborn's
  answer, a vote of another pair left out; the better rule on the space as the
  policy gives it, and on the corpus as a count case by case over the arrivals
  gives it; the shared region's layers;
- what the four orders decide being the engine's own decision on both surfaces;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import billing as BL
from corrections import gap as G
from corrections import hierarchy as H
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from harness.hidden_policy import true_action
from manual import compile as MC
from manual import instrument as MI
from rung3 import edge_direction as ED
from tests.test_corrections_shape import UNSIGNED, c_, r_

SPACE = MI.space()
TRUTH = MI.space_truth()
F = Fraction
T3, AM, BILL = G.T3, G.AM, "BILLING_SPECIALIST"
DECLARED = ("SECURITY_INCIDENT", "ONCALL_ESCALATION", T3, AM, "T2_TECHNICAL",
            "SELF_SERVICE_DEFLECT", BILL, "T1_GENERAL")
BEST = ("SECURITY_INCIDENT", BILL, "ONCALL_ESCALATION", AM, T3, "T2_TECHNICAL",
        "SELF_SERVICE_DEFLECT", "T1_GENERAL")

# T3_ENGINEERING at severity 1 for business clients and on the api at severity 2 or
# less; ACCOUNT_MANAGER's churn for business and enterprise clients; a billing rule.
HAND = [r_(T3, c_("severity", "eq", 1), c_("customer_tier", "eq", "business")),
        r_(AM, c_("customer_tier", "eq", "business"), c_("prior_tickets_30d", "gte", 8)),
        r_(AM, c_("customer_tier", "eq", "enterprise"), c_("prior_tickets_30d", "gte", 5)),
        r_(T3, c_("product", "eq", "api"), c_("severity", "lte", 2)),
        r_(BILL, c_("product", "eq", "billing"))]


def decl(rule, ref, side, queue, ref_queue, verdict="installed"):
    return {"rule": rule, "ref": ref, "side": side, "why": "ok", "verdict": verdict,
            "queue": queue, "ref_queue": ref_queue}


class Hand:

    def __init__(self):
        self.eng = MC.install(HAND, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.ids = self.rs.ids                      # by birth: HAND's order
        self.rules = {r.rule_id: r for r in self.eng.rules}
        self.sp = BL.surface("space", self.eng.ext, self.rs.action, self.rs.inside, TRUTH,
                             SPACE.n)
        self.co = BL.surface("corpus", BL.corpus_ext(self.eng.rules), self.rs.action,
                             self.rs.inside, BL.corpus_truth(), len(MI.corpus()))


HANDS: list[Hand] = []


def hand() -> Hand:
    if not HANDS:
        HANDS.append(Hand())
    return HANDS[0]


class TestTheOrders(unittest.TestCase):

    def test_the_swap_exchanges_the_two_and_nothing_else(self):
        got = G.swapped(DECLARED)
        self.assertEqual(got, ("SECURITY_INCIDENT", "ONCALL_ESCALATION", AM, T3,
                               "T2_TECHNICAL", "SELF_SERVICE_DEFLECT", BILL, "T1_GENERAL"))
        self.assertEqual(G.swapped(got), DECLARED)
        self.assertEqual(G.swapped(BEST)[3:5], (T3, AM))

    def test_the_pairs_ordered_against(self):
        got = G.inverted(DECLARED, BEST)
        self.assertEqual(sorted(map(tuple, got)),
                         sorted([("ONCALL_ESCALATION", BILL), (T3, BILL), (AM, BILL),
                                 ("T2_TECHNICAL", BILL), ("SELF_SERVICE_DEFLECT", BILL),
                                 (T3, AM)]))
        self.assertEqual(G.inverted(DECLARED, DECLARED), [])

    def test_the_decomposition(self):
        got = G.decomposition({"declared": 10, "swap": 15, "rest": 13, "best": 20})
        self.assertEqual(got, {"lacks": 10, "swap_alone": 5, "rest_alone": 3,
                               "swap_given_rest": 7, "left_to_each_other": 2})
        self.assertEqual(G.decomposition({"declared": 0, "swap": 4, "rest": 6,
                                          "best": 10})["left_to_each_other"], 0)

    def test_what_an_order_gains_and_loses(self):
        sp = hand().sp
        before, after = TRUTH[AM] | TRUTH[T3], TRUTH[AM] | TRUTH["T1_GENERAL"]
        got = G.moved(before, after, sp, G.policy_layers())
        self.assertEqual(got["gained"]["by_queue"], {"T1_GENERAL": TRUTH["T1_GENERAL"].bit_count()})
        self.assertEqual(got["lost"]["by_queue"], {T3: TRUTH[T3].bit_count()})
        for side in ("gained", "lost"):
            self.assertEqual(sum(got[side]["by_layer"].values()), got[side]["points"])


class TestTheLayers(unittest.TestCase):

    def test_they_partition_the_space(self):
        self.assertTrue(G.layers_partition())
        self.assertEqual(len(G.policy_layers()), 8)

    def test_each_is_its_rules_regions(self):
        regions = MI.hidden_regions()
        sev1 = 0
        for k in range(4, 9):
            sev1 |= regions[f"H{k:02d}"]["mask"]
        self.assertEqual(G.policy_layers()["severity_1"], sev1)
        self.assertEqual(G.layer_of("H13"), "churn")
        self.assertEqual(G.layer_of("H29"), "defaults")

    def test_the_two_queues_lie_in_their_layers(self):
        m = G.policy_layers()
        self.assertEqual(TRUTH[AM] & ~(m["billing"] | m["churn"]), 0)
        self.assertEqual(TRUTH[T3] & ~(m["severity_1"] | m["product"]), 0)
        self.assertEqual(m["churn"] & ~TRUTH[AM], 0)


class TestTheVotes(unittest.TestCase):

    def setUp(self):
        self.h = hand()
        t3_sev1, am_business, am_enterprise, t3_api, bill = self.h.ids
        self.decls = [
            decl(t3_sev1, am_business, "beats", T3, AM),          # for T3, its own answer
            decl(am_enterprise, t3_api, "beats", AM, T3),         # for AM, its own answer
            decl(t3_api, am_enterprise, "beats", T3, AM),         # for T3, the worse rule
            decl(am_business, t3_sev1, "loses_to", AM, T3),       # for T3, AM's answer
            decl(bill, t3_api, "beats", BILL, T3),                # another pair
            decl(t3_sev1, "R9999", "beats", T3, None),            # an unknown rule
        ]
        self.rows = G.pair_rows(self.decls, self.h.rs.action, self.h.rs.inside, self.h.sp,
                                self.h.co, G.policy_layers())

    def test_only_the_pair(self):
        self.assertEqual(len(self.rows), 4)

    def test_each_oriented_by_its_side(self):
        t3_sev1, am_business, am_enterprise, t3_api, _ = self.h.ids
        self.assertEqual([(r["winner"], r["loser"]) for r in self.rows],
                         [(t3_sev1, am_business), (am_enterprise, t3_api),
                          (t3_api, am_enterprise), (t3_sev1, am_business)])
        self.assertEqual([r["for"] for r in self.rows], [T3, AM, T3, T3])
        self.assertEqual([r["answer"] for r in self.rows], [T3, AM, T3, AM])

    def test_the_better_rule_by_the_policy(self):
        # At severity 1 for business clients the policy never reaches churn: T3 or on-call.
        # On the api at severity 2 for enterprise churn, churn comes before product routing.
        self.assertEqual([r["space"] for r in self.rows], ["a", "a", "b", "a"])

    def test_the_better_rule_case_by_case_over_the_arrivals(self):
        rules = self.h.rules
        for row in self.rows:
            w, l = rules[row["winner"]], rules[row["loser"]]
            ww = wl = 0
            for case in MI.corpus():
                if w.matches(case) and l.matches(case):
                    y = true_action(case)
                    ww += y == w.action
                    wl += y == l.action
            self.assertEqual(row["corpus"], ED.verdict(ww, wl))

    def test_the_shared_region_by_layer(self):
        first = self.rows[0]
        self.assertEqual(sum(first["layers"].values()), first["shared"])
        self.assertEqual(set(k for k, n in first["layers"].items() if n),
                         {"security", "severity_1"})
        self.assertGreater(self.rows[1]["layers"]["churn"], 0)

    def test_the_sides_read_whole(self):
        got = G.read_votes(self.rows)
        self.assertEqual(got["for_t3"]["votes"], 3)
        self.assertEqual(got["for_am"]["votes"], 1)
        self.assertEqual(got["for_t3"]["by_answer"], {T3: 2, AM: 1})
        self.assertEqual((got["for_t3"]["space"]["strict"], got["for_t3"]["space"]["named"]),
                         (3, 2))


class TestWhatTheOrdersDecide(unittest.TestCase):

    def test_the_engines_own_decision_on_both_surfaces(self):
        h = hand()
        for ranking in (DECLARED, G.swapped(DECLARED), BEST, G.swapped(BEST)):
            o = H.pulled(h.rs, H.rank_of(ranking))
            s, c = BL.right_mask(o, h.sp), BL.right_mask(o, h.co)
            self.assertTrue(BL.installs(o, h.rules, h.rs, SPACE, s.bit_count(), c.bit_count()))
            got = G.read_surface(s, h.sp)
            self.assertEqual(sum(got["by_queue"].values()), got["right"])


def fake(swap=6, lacks=10, own=3, votes=5, named=3, strict=5, sev1=6, layers=10,
         gained=10, churn=6, corpus=1, runs=G.L_RUNS):
    out = {}
    for t in runs:
        out[t] = {"gap": {"space": {"swap_alone": swap, "lacks": lacks},
                          "corpus": {"swap_alone": corpus}},
                  "votes": {"for_t3": {"votes": votes, "by_answer": {T3: own, AM: votes - own},
                                       "space": {"named": named, "strict": strict},
                                       "layers": {"severity_1": sev1, "churn": layers - sev1}}},
                  "the_swap": {"space": {"gained": {"points": gained,
                                                    "by_layer": {"churn": churn}}}}}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in G.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(swap=5, own=2, votes=4, named=2, strict=4, sev1=5, gained=10, churn=5,
                         corpus=0))
        self.assertEqual(got, {f"G{k}": False for k in range(1, 7)})

    def test_every_run(self):
        self.assertEqual(set(holds(fake(runs=("l_r1", "l_r2"))).values()), {False})

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(BL, "declared_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                G.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
