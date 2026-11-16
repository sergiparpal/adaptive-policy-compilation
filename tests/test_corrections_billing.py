"""
`corrections/billing.py` — the POST-RUN reading of why the declarations put
`BILLING_SPECIALIST` low. No figure of the reading.

What is pinned is the instrument:
- the votes on billing's pairs, each oriented by its side, against or for the
  queue, cast by billing's own answer or the other queue's, nested or not; a
  citation within a queue, or of a rule the record does not hold, is no vote;
- the better rule of a vote on both surfaces, against the policy read by hand
  and against a count case by case over the arrivals;
- what an order decides on each surface, the engine's own decision, first
  match's on the space, and what `corrections/online.py` counts;
- the policy's three layers partitioning the space;
- the queue moved through its places, the best place and the path to it;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import billing as B
from corrections import hierarchy as H
from corrections import online as ON
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from harness.hidden_policy import true_action
from manual import compile as MC
from manual import instrument as MI
from rung2.engine2 import EDGE_OK
from rung3 import edge_direction as ED
from tests.test_corrections_shape import UNSIGNED, c_, r_

SPACE = MI.space()
TRUTH = MI.space_truth()
F = Fraction
BILL, ONC, SS, T2, T1 = ("BILLING_SPECIALIST", "ONCALL_ESCALATION", "SELF_SERVICE_DEFLECT",
                         "T2_TECHNICAL", "T1_GENERAL")

# A broad billing rule, on-call at severity 1, self-service for free clients, a
# rule of T2_TECHNICAL nested in the first two, and a catch-all of T1_GENERAL.
HAND = [r_(BILL, c_("product", "eq", "billing")),
        r_(ONC, c_("severity", "eq", 1)),
        r_(SS, c_("customer_tier", "eq", "free")),
        r_(T2, c_("product", "eq", "billing"), c_("severity", "eq", 1)),
        r_(T1, c_("severity", "gte", 1))]
DECLARED = ("SECURITY_INCIDENT", ONC, "T3_ENGINEERING", "ACCOUNT_MANAGER", T2, SS, BILL, T1)


def decl(rule, ref, side, queue, ref_queue, verdict="installed"):
    return {"rule": rule, "ref": ref, "side": side, "why": "ok", "verdict": verdict,
            "queue": queue, "ref_queue": ref_queue}


class Hand:
    """The hand base, installed over the real space, with both surfaces."""

    def __init__(self):
        self.eng = MC.install(HAND, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.id = {self.rs.action[r]: r for r in self.rs.ids}
        self.rules = {r.rule_id: r for r in self.eng.rules}
        self.sp = B.surface("space", self.eng.ext, self.rs.action, self.rs.inside, TRUTH, SPACE.n)
        self.co = B.surface("corpus", B.corpus_ext(self.eng.rules), self.rs.action,
                            self.rs.inside, B.corpus_truth(), len(MI.corpus()))

    def rows(self, decls):
        return B.vote_rows(decls, self.rs.action, self.rs.inside, self.sp, self.co,
                           B.layer_masks())


HANDS: list[Hand] = []


def hand() -> Hand:
    if not HANDS:
        HANDS.append(Hand())
    return HANDS[0]


class TestTheVotes(unittest.TestCase):

    def setUp(self):
        self.h = hand()
        i = self.h.id
        self.decls = [
            decl(i[ONC], i[BILL], "beats", ONC, BILL),        # against, the other's answer
            decl(i[BILL], i[SS], "loses_to", BILL, SS),       # against, billing's own
            decl(i[BILL], i[T1], "beats", BILL, T1),          # for, billing's own
            decl(i[T2], i[BILL], "beats", T2, BILL),          # against, nested
            decl(i[ONC], i[SS], "beats", ONC, SS),            # not billing's pair
            decl(i[BILL], i[BILL], "beats", BILL, BILL),      # within a queue: no vote
            decl(i[BILL], "R9999", "beats", BILL, None),      # unknown rule: no vote
        ]
        self.rows = self.h.rows(self.decls)

    def test_only_votes_between_two_queues(self):
        self.assertEqual(len(self.rows), 5)
        self.assertEqual([r["billing"] for r in self.rows], [True, True, True, True, False])

    def test_each_oriented_by_its_side(self):
        i = self.h.id
        on_billing = [r for r in self.rows if r["billing"]]
        self.assertEqual([(r["winner"], r["loser"]) for r in on_billing],
                         [(i[ONC], i[BILL]), (i[SS], i[BILL]), (i[BILL], i[T1]),
                          (i[T2], i[BILL])])
        self.assertEqual([r["against"] for r in on_billing], [True, True, False, True])
        self.assertEqual([r["own_answer"] for r in on_billing], [False, True, True, False])
        self.assertEqual([r["other_queue"] for r in on_billing], [ONC, SS, T1, T2])
        # the catch-all holds billing's rule, and billing's rule the nested one
        self.assertEqual([r["nested"] for r in on_billing], [False, False, True, True])
        # billing's rule, a fifth of the space, against a quarter, a quarter, the whole
        # space, and a twentieth inside it
        self.assertEqual([r["billing_larger"] for r in on_billing], [False, False, False, True])

    def test_the_better_rule_by_the_policy(self):
        # On billing at severity 1 the policy never sends a ticket to billing: on-call is
        # the better rule there. On billing for free clients, the specialist's two rules
        # take more than the residue self-service keeps: billing is the better rule.
        a, b = self.rows[0], self.rows[1]
        self.assertEqual(a["space"], B.HIT)
        self.assertEqual(b["space"], B.MISS)

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

    def test_the_shared_region_and_its_layers(self):
        for row in self.rows:
            shared = self.h.sp.ext[row["winner"]] & self.h.sp.ext[row["loser"]]
            self.assertEqual(row["shared"], shared.bit_count())
            self.assertEqual(sum(row["layers"].values()), row["shared"])

    def test_the_sides_read_whole(self):
        got = B.read_votes(self.rows)
        self.assertEqual(got["against"]["votes"], 3)
        self.assertEqual(got["for"]["votes"], 1)
        self.assertEqual(got["against"]["by_answer"], {"the_other_queues": 2, "its_own": 1})
        self.assertEqual(got["against"]["nested"], 1)
        self.assertEqual(got["by_queue"][ONC]["against"]["votes"], 1)
        self.assertEqual(got["by_queue"][T1]["for"]["votes"], 1)
        self.assertEqual(got["elsewhere"]["votes"], 1)
        self.assertNotIn(BILL, got["by_queue"])


class TestTheTally(unittest.TestCase):

    def test_strict_named_tie_and_neither(self):
        rows = [{"space": B.HIT}, {"space": B.HIT}, {"space": B.MISS}, {"space": B.TIE},
                {"space": B.NEITHER}]
        got = B.tally(rows, "space")
        self.assertEqual((got["votes"], got["strict"], got["named"], got["tie"], got["neither"]),
                         (5, 3, 2, 1, 1))
        self.assertEqual(F(got["share"]["fraction"]), F(2, 3))
        self.assertIsNone(B.tally([], "space")["share"])

    def test_the_median_of_an_even_count(self):
        self.assertEqual(B.median_of([4, 1, 3, 10]), F(7, 2))
        self.assertIsNone(B.median_of([]))


class TestTheSurfaces(unittest.TestCase):

    def test_layers_partition_the_space(self):
        m = B.layer_masks()
        self.assertEqual(m["above"] | m["billing"] | m["below"], (1 << SPACE.n) - 1)
        self.assertFalse(m["above"] & m["billing"] or m["above"] & m["below"]
                         or m["billing"] & m["below"])

    def test_what_an_order_decides_is_the_engines(self):
        h = hand()
        for ranking in (DECLARED, B.moved(DECLARED, 1), tuple(ACTIONS)):
            o = H.pulled(h.rs, H.rank_of(ranking))
            s, c = B.right_mask(o, h.sp), B.right_mask(o, h.co)
            self.assertEqual(s.bit_count(), ON.right_of(o, h.rs, h.eng.ext, TRUTH, SPACE.n))
            eng = S.installed_in(o, h.rules, SPACE)
            self.assertTrue(all(why == EDGE_OK for _, _, why in eng.edge_log))
            self.assertEqual(MI.over_space(eng)["correct"], s.bit_count())
            self.assertEqual(MI.over_corpus(eng)["correct"], c.bit_count())
            self.assertTrue(B.installs(o, h.rules, h.rs, SPACE, s.bit_count(), c.bit_count()))
            self.assertFalse(B.installs(o, h.rules, h.rs, SPACE, s.bit_count() + 1,
                                        c.bit_count()))


class TestThePlace(unittest.TestCase):

    def test_moved_through_its_places(self):
        others = [q for q in DECLARED if q != BILL]
        for p in range(1, 9):
            got = B.moved(DECLARED, p)
            self.assertEqual(got.index(BILL), p - 1)
            self.assertEqual([q for q in got if q != BILL], others)
        self.assertEqual(B.moved(DECLARED, 7), DECLARED)

    @staticmethod
    def places(rights):
        return {p: {"space": {"right": r, "by_queue": {q: 0 for q in ACTIONS}},
                    "corpus": {"right": 10 * r}} for p, r in rights.items()}

    def test_the_best_place(self):
        pl = self.places({1: 5, 2: 9, 3: 9, 4: 1, 5: 2, 6: 3, 7: 4, 8: 9})
        self.assertEqual(B.best_place(pl, 7), 8)
        self.assertEqual(B.best_place(pl, 5), 3)
        pl = self.places({1: 9, 2: 1, 3: 1, 4: 1, 5: 9, 6: 1, 7: 1, 8: 1})
        self.assertEqual(B.best_place(pl, 3), 1)
        self.assertEqual(B.best_place(pl, 5), 5)

    def test_the_path_passes_one_queue_a_step(self):
        pl = self.places({p: p * p for p in range(1, 9)})
        up = B.path(pl, DECLARED, 7, 4)
        self.assertEqual([s["passes"] for s in up], [SS, T2, "ACCOUNT_MANAGER"])
        self.assertEqual([(s["from"], s["to"]) for s in up], [(7, 6), (6, 5), (5, 4)])
        self.assertEqual([s["space"] for s in up], [36 - 49, 25 - 36, 16 - 25])
        self.assertEqual([s["corpus"] for s in up], [-130, -110, -90])
        self.assertTrue(all(s["up"] for s in up))
        down = B.path(pl, DECLARED, 7, 8)
        self.assertEqual([s["passes"] for s in down], [T1])
        self.assertFalse(down[0]["up"])
        self.assertEqual(B.path(pl, DECLARED, 7, 7), [])


def fake(others=6, against=10, named=3, strict=5, gain=6, lacks=10, step=4, pair=(5, 2, 3, 5),
         corpus=(100, 101), medians=(1, 2), runs=B.READ):
    def sh(x):
        return {"fraction": str(F(x)), "value": float(x)}
    a, f, n, s = pair
    out = {}
    for t in runs:
        out[t] = {
            "votes": {"against": {"votes": against, "by_answer": {"the_other_queues": others},
                                  "space": {"named": named, "strict": strict},
                                  "shared_median": sh(medians[0])},
                      "for": {"shared_median": sh(medians[1])},
                      "by_queue": {SS: {"against": {"votes": a, "space": {"named": n, "strict": s}},
                                        "for": {"votes": f}}}},
            "place": {"declared": 7, "best": 6, "gain": {"points": gain},
                      "lacks": {"points": lacks},
                      "places": {"7": {"corpus": {"right": corpus[0]}},
                                 "6": {"corpus": {"right": corpus[1]}}},
                      "path": [{"up": True, "passes": SS, "space": step}]}}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in B.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(others=5, named=5, strict=10, gain=5, step=0, corpus=(100, 100),
                         medians=(2, 2)))
        self.assertEqual(got, {f"V{k}": False for k in range(1, 7)})

    def test_v4_reads_the_pair(self):
        self.assertFalse(holds(fake(pair=(2, 2, 3, 5)))["V4"])
        self.assertFalse(holds(fake(pair=(5, 2, 2, 4)))["V4"])
        self.assertTrue(holds(fake(pair=(5, 2, 3, 5)))["V4"])

    def test_both_runs(self):
        self.assertEqual(set(holds(fake(runs=("l_r1",))).values()), {False})

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(B, "declared_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                B.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
