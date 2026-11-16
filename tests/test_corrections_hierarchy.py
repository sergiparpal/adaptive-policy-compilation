"""
`corrections/hierarchy.py` — the POST-RUN reading of whether the order the loop
lacks is a ranking of the queues. No figure of the reading.

What is pinned is the instrument:
- where containment is silent, both constructions are
  `rung3/queue_hierarchy_floor.py`'s order, by rank and then by birth;
- where it is not, both keep containment, by brute force over every order that
  does: pulled puts the rule ranked first as early as it can go, then the next,
  and waiting gives the least sequence of ranks;
- the two on a rule nested in one of a higher-ranked queue, by hand, over the
  real space;
- rules built by hand over the real space and policy: what a ranking's order
  decides is the engine's own decision and first match's, under both
  constructions, and its right labels are the engine's;
- the summaries: the spread, the earliest best, the places;
- the rankings on record, as the records keep them;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import random
import unittest
from fractions import Fraction
from itertools import permutations
from unittest import mock

from corrections import hierarchy as H
from corrections import plan
from corrections import shape as S
from harness.domain import ACTIONS
from manual import compile as MC
from manual import instrument as MI
from rung3 import local_search as LS
from rung3 import queue_hierarchy_floor as QHF
from tests.test_corrections_shape import UNSIGNED, c_, r_, random_containment

SPACE = MI.space()
TRUTH = MI.space_truth()
F = Fraction


def random_rules(rng: random.Random, n: int, p: float) -> H.Rules:
    ids = [f"r{i}" for i in range(n)]
    inside, around = random_containment(rng, ids, p)
    return H.Rules(ids=ids, action={r: rng.choice(ACTIONS) for r in ids},
                   born={r: (i, r) for i, r in enumerate(ids)}, inside=inside, around=around)


def random_rank(rng: random.Random) -> dict[str, int]:
    perm = list(ACTIONS)
    rng.shuffle(perm)
    return H.rank_of(perm)


def linear_extensions(rs: H.Rules):
    for p in permutations(rs.ids):
        if S.is_linear_extension(p, rs.inside):
            yield list(p)


class TestWhereContainmentIsSilent(unittest.TestCase):
    """Both constructions are rung 3's hierarchy order."""

    def test_both_are_queue_hierarchy_floors_order(self):
        rng = random.Random(11)
        for _ in range(40):
            rs = random_rules(rng, 9, 0.0)
            rank = random_rank(rng)
            want = QHF.hierarchy_order(rs.ids, rs.action, {r: rs.born[r][0] for r in rs.ids}, rank)
            self.assertEqual(H.pulled(rs, rank), want)
            self.assertEqual(H.waiting(rs, rank), want)


class TestWhereItIsNot(unittest.TestCase):
    """By brute force over every order that keeps containment."""

    def test_both_keep_containment(self):
        rng = random.Random(13)
        for _ in range(60):
            rs = random_rules(rng, 8, 0.35)
            rank = random_rank(rng)
            for build in H.BUILD.values():
                o = build(rs, rank)
                self.assertEqual(sorted(o), sorted(rs.ids))
                self.assertTrue(S.is_linear_extension(o, rs.inside))

    def test_pulled_puts_each_rule_as_early_as_its_rank_allows(self):
        rng = random.Random(17)
        for _ in range(40):
            rs = random_rules(rng, 6, 0.35)
            rank = random_rank(rng)
            first = sorted(rs.ids, key=lambda r: (rank[rs.action[r]], rs.born[r]))
            want = min(linear_extensions(rs),
                       key=lambda o: tuple(o.index(r) for r in first))
            self.assertEqual(H.pulled(rs, rank), want)

    def test_waiting_gives_the_least_sequence_of_ranks(self):
        rng = random.Random(19)
        for _ in range(40):
            rs = random_rules(rng, 6, 0.35)
            rank = random_rank(rng)
            want = min(linear_extensions(rs),
                       key=lambda o: tuple((rank[rs.action[r]], rs.born[r]) for r in o))
            self.assertEqual(H.waiting(rs, rank), want)

    def test_a_cycle_is_refused(self):
        rs = H.Rules(ids=["a", "b"], action={"a": ACTIONS[0], "b": ACTIONS[1]},
                     born={"a": (0, "a"), "b": (1, "b")},
                     inside={"a": frozenset({"b"}), "b": frozenset({"a"})},
                     around={"a": frozenset({"b"}), "b": frozenset({"a"})})
        rank = H.rank_of(ACTIONS)
        for build in H.BUILD.values():
            with self.assertRaises(ValueError):
                build(rs, rank)

    def test_a_ranking_is_of_the_eight_queues(self):
        with self.assertRaises(ValueError):
            H.rank_of(ACTIONS[:7])
        with self.assertRaises(ValueError):
            H.rank_of(list(ACTIONS[:7]) + [ACTIONS[0]])


# The keyword's rule, a rule of a lower-ranked queue nested in it, a billing rule
# that crosses both, and a catch-all around them all.
NESTED = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
          r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
          r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
          r_("T1_GENERAL", c_("severity", "gte", 1))]
RANKING = ("SECURITY_INCIDENT", "BILLING_SPECIALIST", "ONCALL_ESCALATION", "T3_ENGINEERING",
           "ACCOUNT_MANAGER", "SELF_SERVICE_DEFLECT", "T2_TECHNICAL", "T1_GENERAL")


class TestTheNestedRule(unittest.TestCase):
    """Pulled brings the nested rule up to its container's place; waiting drags
    the container down to the nested rule's."""

    def setUp(self):
        self.eng = MC.install(NESTED, SPACE).engine
        self.rs = H.rules_of(self.eng)
        self.by_action = {self.rs.action[r]: r for r in self.rs.ids}

    def names(self, order):
        return [self.rs.action[r] for r in order]

    def test_the_two_constructions(self):
        rank = H.rank_of(RANKING)
        self.assertEqual(self.names(H.pulled(self.rs, rank)),
                         ["T2_TECHNICAL", "SECURITY_INCIDENT", "BILLING_SPECIALIST", "T1_GENERAL"])
        self.assertEqual(self.names(H.waiting(self.rs, rank)),
                         ["BILLING_SPECIALIST", "T2_TECHNICAL", "SECURITY_INCIDENT", "T1_GENERAL"])

    def test_both_install_and_decide_as_read(self):
        rules = {r.rule_id: r for r in self.eng.rules}
        inst = S.instance(self.eng.rules, self.eng.ext, self.rs.inside, self.rs.around, TRUTH,
                          SPACE.n)
        for c in H.CONSTRUCTIONS:
            row, ok = H.read_order(self.rs, inst, RANKING, c, rules, SPACE, TRUTH)
            self.assertTrue(ok)
            o = H.BUILD[c](self.rs, H.rank_of(RANKING))
            self.assertEqual(row["right"], inst.score(inst.searched(o)))
            self.assertEqual(row["ranking"], list(RANKING))


# Rules built by hand over the real space: the keyword's rule, a rule nested in
# it, a crossing billing rule, severity 1 to the on-call queue, and a catch-all.
HAND = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
        r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
        r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
        r_("ONCALL_ESCALATION", c_("severity", "eq", 1)),
        r_("T1_GENERAL", c_("severity", "gte", 1))]


class TestOnTheSpace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.eng = MC.install(HAND, SPACE).engine
        cls.rs = H.rules_of(cls.eng)
        cls.rules = {r.rule_id: r for r in cls.eng.rules}
        cls.inst = S.instance(cls.eng.rules, cls.eng.ext, cls.rs.inside, cls.rs.around, TRUTH,
                              SPACE.n)
        cls.labels = [(i, MI.corpus_truth()[i]) for i in range(60)]
        cls.perms = H.rankings()
        cls.got = H.read_rules(cls.eng, SPACE, TRUTH, H.on_record(), cls.perms, labels=cls.labels)

    def test_every_ranking_once(self):
        self.assertEqual(len(self.perms), H.N_RANKINGS)
        self.assertEqual(len(set(self.perms)), H.N_RANKINGS)
        self.assertEqual(self.perms[0], tuple(ACTIONS))

    def test_what_an_order_decides_is_the_engines_and_first_matchs(self):
        for perm in self.perms[::4999]:
            for c in H.CONSTRUCTIONS:
                o = H.BUILD[c](self.rs, H.rank_of(perm))
                self.assertTrue(S.installs(o, self.rules, self.inst, SPACE))

    def test_the_labels_are_the_engines(self):
        M, W, full = S.label_masks(self.eng, self.labels, self.rs.inside)
        corpus = MI.corpus()
        for perm in self.perms[::6007]:
            o = H.pulled(self.rs, H.rank_of(perm))
            e2 = S.installed_in(o, self.rules, SPACE)
            want = 0
            for idx, q in self.labels:
                outcome, winner, _ = e2.decide(corpus[idx])
                want += outcome == "ACTION" and winner.action == q
            self.assertEqual(LS.score_order(o, M, W, full), want)

    def test_read_rules(self):
        got = self.got
        self.assertTrue(all(got["gates"].values()))
        for c in H.CONSTRUCTIONS:
            best = got[c]["best"]
            self.assertLessEqual(best["right"], got["bound"]["right"])
            self.assertEqual(best["halves"]["keyword"] + best["halves"]["outside"], best["right"])
            self.assertGreaterEqual(best["rankings_at_it"], 1)
            self.assertEqual(sum(1 for _ in got[c]["by_place_of_security"]), 8)
            self.assertEqual(got[c]["blind"]["of"], H.N_RANKINGS)
            self.assertEqual(got[c]["blind"]["most"], best["share"])
        lab = got["by_its_labels"]
        self.assertEqual(lab["labels"]["of"], 60)
        self.assertEqual(sum(lab["by_place_of_security"].values()), lab["rankings"])
        self.assertLessEqual(F(lab["orders"]["least"]["share"]["fraction"]),
                             F(lab["orders"]["most"]["share"]["fraction"]))
        rec = got["on_record"]
        self.assertEqual(len(rec["stated"]["asks"]), 24)
        self.assertEqual(rec["stated"]["distinct"], 6)
        self.assertEqual(set(rec["rankings"]) >= {"borda", "revealed", "stage_c"}, True)

    def test_a_subset_is_not_every_ranking(self):
        got = H.read_rules(self.eng, SPACE, TRUTH, H.on_record(), self.perms[:24], named=False)
        self.assertFalse(got["gates"]["every_ranking_once"])
        self.assertTrue(got["gates"]["installs"])
        self.assertTrue(got["gates"]["bound_bounds"])


class TestTheSummaries(unittest.TestCase):

    def test_spread(self):
        got = H.spread([4, 1, 3, 2], 10)
        self.assertEqual(F(got["median"]["fraction"]), F(5, 20))
        self.assertEqual(F(got["least"]["fraction"]), F(1, 10))
        self.assertEqual(F(got["most"]["fraction"]), F(4, 10))
        self.assertEqual(F(got["quarter"]["fraction"]), F(2, 10))
        self.assertEqual(F(got["three_quarters"]["fraction"]), F(4, 10))
        self.assertEqual(F(got["mean"]["fraction"]), F(10, 40))
        self.assertEqual(F(H.spread([3, 1, 2], 10)["median"]["fraction"]), F(2, 10))

    def test_the_earliest_best(self):
        self.assertEqual(H.best_index([1, 3, 2, 3]), 1)

    def test_by_place(self):
        perms = H.rankings()
        got = H.by_place(list(range(len(perms))), perms, len(perms))
        self.assertEqual(list(got), [str(p) for p in range(1, 9)])
        first = [k for k, p in enumerate(perms) if p[0] == H.SECURITY]
        self.assertEqual(F(got["1"]["most"]["fraction"]), F(max(first), len(perms)))


class TestTheRankingsOnRecord(unittest.TestCase):

    def test_as_the_records_keep_them(self):
        got = H.on_record()
        self.assertEqual(len(got["stated"]), 24)
        self.assertEqual(got["stage_c"], got["stage_c_as_sample_keeps_it"])
        names = H.named_rankings(got)
        self.assertEqual(len(names), 9)
        for ranking in names.values():
            self.assertEqual(sorted(ranking), sorted(ACTIONS))


def fake(best=F(7, 10), waiting=F(6, 10), first=H.SECURITY, labels=F(1, 2), stated=F(6, 10),
         truth=F(8, 10), at_once=F(65, 100), completed=F(55, 100), runs=H.L_RUNS):
    def sh(x):
        return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}
    rest = [q for q in ACTIONS if q != first]
    out, shape = {}, {"runs": {}}
    for t in runs:
        out[t] = {"loop": {"pulled": {"best": {"share": sh(best), "ranking": [first, *rest]}},
                           "waiting": {"best": {"share": sh(waiting)}},
                           "by_its_labels": {"shares": {"median": sh(labels)}},
                           "on_record": {"stated": {"pulled": {"median": sh(stated)}}}}}
        shape["runs"][t] = {"at_once_median": {"record": sh(at_once)},
                            "loop": {"completed": {"share": sh(completed)},
                                     "with_the_truth": {"share": sh(truth)}}}
    return out, shape


def holds(pair):
    return {c["clause"]: c["holds"] for c in H.read_expectation(*pair)}


class TestTheExpectation(unittest.TestCase):

    def test_just_inside_the_lines(self):
        self.assertEqual(set(holds(fake()).values()), {True})

    def test_at_the_lines(self):
        got = holds(fake(best=F(7, 10), waiting=F(7, 10), first="ONCALL_ESCALATION",
                         labels=F(7, 10), stated=F(55, 100), truth=F(7, 10), at_once=F(7, 10)))
        self.assertEqual(got, {"Y1": False, "Y2": False, "Y3": False, "Y4": False, "Y5": False,
                               "Y6": False})

    def test_y2_and_y6_read_two_named_runs(self):
        got = holds(fake(runs=("l_r1", "l_r2")))
        self.assertEqual(got, {"Y1": False, "Y2": True, "Y3": False, "Y4": False, "Y5": False,
                               "Y6": True})
        self.assertFalse(holds(fake(runs=("l_r1", "l_r3")))["Y2"])

    def test_over_nothing(self):
        self.assertEqual(set(holds(({}, {"runs": {}})).values()), {False})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(H, "shape_record", side_effect=AssertionError("read")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                H.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
