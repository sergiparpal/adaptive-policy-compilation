"""
`corrections/shape.py` — the POST-RUN reading of shape or order: what the loop's
own rules could decide in the orders rung 2's engine can install. No figure of
the reading.

What is pinned is the instrument:
- where containment is silent, the search is rung 3's declared optimizer, move
  for move: the same insertion, the same passes, the same local optimum, the
  same starts and the same multi-start;
- where it is not, every relocation is the best of the positions that keep
  containment, by brute force, and the search stops at a local optimum of the
  moves and swaps that keep it;
- the repairs, the completion of an engine's graph and the merge;
- rules built by hand over the real space and policy: what an order decides is
  the engine's own decision and first match's, its bound bounds every order,
  completing loses nothing, and an order that breaks containment does not
  install;
- the labels as an instance, and the search from the completed order;
- the instrument's ceiling on the hidden policy;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run: where a base's bound falls short, its three ways
partitioning what the bound leaves, the rules that hold the points lost to
containment, what an answer decides among them, and the median answer.
"""

from __future__ import annotations

import random
import unittest
from fractions import Fraction
from itertools import permutations
from unittest import mock

from corrections import plan
from corrections import shape as S
from manual import compile as MC
from manual import instrument as MI
from rung3 import local_search as LS

SPACE = MI.space()
TRUTH = MI.space_truth()
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
F = Fraction


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(action, *conds):
    return {"action": action, "conditions": list(conds)}


def random_instance(rng: random.Random, n_rules: int = 8, n_cases: int = 40):
    ids = [f"r{i}" for i in range(n_rules)]
    M, W = {}, {}
    for r in ids:
        m = rng.getrandbits(n_cases)
        M[r] = m
        W[r] = m & rng.getrandbits(n_cases)
    return ids, M, W, (1 << n_cases) - 1


def random_containment(rng: random.Random, ids, p: float = 0.3):
    """A strict partial order over `ids`, transitively closed: `inside[r]` must
    come before `r`."""
    hidden = list(ids)
    rng.shuffle(hidden)
    inside = {r: set() for r in ids}
    for i, a in enumerate(hidden):
        for b in hidden[i + 1:]:
            if rng.random() < p:
                inside[b].add(a)
    changed = True
    while changed:
        changed = False
        for r in ids:
            more = set().union(*(inside[b] for b in inside[r])) - inside[r]
            if more:
                inside[r] |= more
                changed = True
    around = {r: {x for x in ids if r in inside[x]} for r in ids}
    return ({r: frozenset(v) for r, v in inside.items()},
            {r: frozenset(v) for r, v in around.items()})


NONE = None


def silent(ids):
    e = {r: frozenset() for r in ids}
    return e, e


class TestWhereContainmentIsSilent(unittest.TestCase):
    """The search is rung 3's, move for move."""

    def test_the_same_insertion(self):
        rng = random.Random(3)
        for _ in range(30):
            ids, M, W, full = random_instance(rng)
            order = LS.random_order(ids, rng.randrange(10 ** 6))
            inside, around = silent(ids)
            for k in range(len(order)):
                self.assertEqual(S.best_valid_insertion(order, k, M, W, full, inside, around),
                                 LS.best_insertion(order, k, M, W, full))

    def test_the_same_passes_and_local_optimum(self):
        rng = random.Random(5)
        for _ in range(20):
            ids, M, W, full = random_instance(rng)
            inside, around = silent(ids)
            o = LS.random_order(ids, rng.randrange(10 ** 6))
            a, b = list(o), list(o)
            self.assertEqual(S.move_pass(a, M, W, full, inside, around), LS.move_pass(b, M, W, full))
            self.assertEqual(a, b)
            self.assertEqual(S.swap_pass(a, M, W, full, inside, around), LS.swap_pass(b, M, W, full))
            self.assertEqual(a, b)
            for nb in LS.NEIGHBOURHOODS:
                got = S.local_search(o, M, W, full, inside, around, neighbourhood=nb)
                want = LS.local_search(o, M, W, full, neighbourhood=nb)
                self.assertEqual(got, want)

    def test_the_same_starts_and_multistart(self):
        rng = random.Random(7)
        ids, M, W, full = random_instance(rng, n_rules=7)
        inside, around = silent(ids)
        starts = S.declared_starts(ids, inside)
        self.assertEqual(starts, LS.declared_starts(ids))
        got, gst = S.multistart(starts, M, W, full, inside, around)
        want, wst = LS.multistart(starts, M, W, full)
        self.assertEqual(got, want)
        self.assertEqual(gst["best_score"], wst["best_score"])
        self.assertEqual(gst["best_from_index"], wst["best_from_index"])
        self.assertEqual([r["end_score"] for r in gst["rows"]], [r["end_score"] for r in wst["rows"]])

    def test_the_declared_constants_are_rung_3s(self):
        self.assertEqual((LS.MULTISTART_SEED, LS.MULTISTART_STARTS, LS.DECLARED_NEIGHBOURHOOD),
                         (17, 64, "move+swap"))
        self.assertEqual(len(S.declared_starts([f"r{i}" for i in range(5)],
                                               silent([f"r{i}" for i in range(5)])[0])), 64)


class TestWhereItIsNot(unittest.TestCase):

    def test_every_insertion_is_the_best_that_keeps_containment(self):
        rng = random.Random(11)
        for _ in range(40):
            ids, M, W, full = random_instance(rng, n_rules=7)
            inside, around = random_containment(rng, ids)
            order = S.repaired(LS.random_order(ids, rng.randrange(10 ** 6)), inside)
            for k in range(len(order)):
                r = order[k]
                rest = order[:k] + order[k + 1:]
                best_k, best = k, LS.score_order(order, M, W, full)
                for j in range(len(rest) + 1):
                    cand = rest[:j] + [r] + rest[j:]
                    if not S.is_linear_extension(cand, inside):
                        continue
                    s = LS.score_order(cand, M, W, full)
                    if s > best:
                        best_k, best = j, s
                self.assertEqual(S.best_valid_insertion(order, k, M, W, full, inside, around),
                                 (best_k, best))

    def test_the_search_stops_at_a_local_optimum_that_keeps_containment(self):
        rng = random.Random(13)
        for _ in range(25):
            ids, M, W, full = random_instance(rng, n_rules=7)
            inside, around = random_containment(rng, ids)
            o0 = S.repaired(LS.random_order(ids, rng.randrange(10 ** 6)), inside)
            o, st = S.local_search(o0, M, W, full, inside, around)
            self.assertTrue(S.is_linear_extension(o, inside))
            s = LS.score_order(o, M, W, full)
            self.assertEqual(st["end"], s)
            self.assertGreaterEqual(s, st["start"])
            for k in range(len(o)):
                rest = o[:k] + o[k + 1:]
                for j in range(len(rest) + 1):
                    cand = rest[:j] + [o[k]] + rest[j:]
                    if S.is_linear_extension(cand, inside):
                        self.assertLessEqual(LS.score_order(cand, M, W, full), s)
            for p in range(len(o)):
                for q in range(p + 1, len(o)):
                    cand = list(o)
                    cand[p], cand[q] = cand[q], cand[p]
                    self.assertEqual(S.swap_keeps(o, p, q, inside, around),
                                     S.is_linear_extension(cand, inside))
                    if S.is_linear_extension(cand, inside):
                        self.assertLessEqual(LS.score_order(cand, M, W, full), s)

    def test_a_start_that_breaks_containment_is_refused(self):
        inside = {"a": frozenset(), "b": frozenset({"a"})}
        around = {"a": frozenset({"b"}), "b": frozenset()}
        M = {"a": 1, "b": 1}
        with self.assertRaises(ValueError):
            S.local_search(["b", "a"], M, M, 1, inside, around)
        with self.assertRaises(ValueError):
            S.declared_starts(["a", "b"], inside, first=["b", "a"])

    def test_the_multistart_ties_go_to_the_earliest(self):
        ids = ["a", "b"]
        inside, around = silent(ids)
        M = {"a": 0b11, "b": 0b11}
        W = {"a": 0b11, "b": 0b11}
        best, st = S.multistart([("x", ["b", "a"]), ("y", ["a", "b"])], M, W, 0b11, inside, around)
        self.assertEqual((best, st["best_from"]), (["b", "a"], "x"))


class TestTheOrders(unittest.TestCase):

    def test_repaired(self):
        rng = random.Random(17)
        for _ in range(30):
            ids = [f"r{i}" for i in range(8)]
            inside, _ = random_containment(rng, ids)
            o = LS.random_order(ids, rng.randrange(10 ** 6))
            got = S.repaired(o, inside)
            self.assertTrue(S.is_linear_extension(got, inside))
            self.assertEqual(sorted(got), sorted(ids))
            self.assertEqual(S.repaired(got, inside), got)

    def test_topological_refuses_a_cycle(self):
        with self.assertRaises(ValueError):
            S.topological(["a", "b"], {"a": frozenset({"b"}), "b": frozenset({"a"})},
                          {"a": 0, "b": 1})

    def test_merged_keeps_the_searched_order(self):
        rng = random.Random(19)
        for _ in range(30):
            ids = [f"r{i}" for i in range(9)]
            inside, _ = random_containment(rng, ids)
            keep = rng.sample(ids, 5)
            searched = S.repaired(keep, S.restricted(inside, keep))
            others = [r for r in ids if r not in keep]
            got = S.merged(searched, others, inside)
            self.assertTrue(S.is_linear_extension(got, inside))
            self.assertEqual([r for r in got if r in keep], searched)
            self.assertEqual(sorted(got), sorted(ids))


# Rules built by hand over the real space: the keyword's rule, a rule nested in
# it, a crossing billing rule, severity 1 to the on-call queue, and a catch-all.
HAND = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
        r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("customer_tier", "eq", "free")),
        r_("BILLING_SPECIALIST", c_("product", "eq", "billing")),
        r_("ONCALL_ESCALATION", c_("severity", "eq", 1)),
        r_("T1_GENERAL", c_("severity", "gte", 1))]


def hand_engine(order=(3, 2, 0, 1, 4)):
    return MC.install([HAND[i] for i in order], SPACE).engine


class TestOnTheSpace(unittest.TestCase):

    def setUp(self):
        self.eng = hand_engine()
        self.rules = {r.rule_id: r for r in self.eng.rules}
        self.inside, self.around = S.containment(self.eng)
        self.inst = S.instance(self.eng.rules, self.eng.ext, self.inside, self.around, TRUTH,
                               SPACE.n)

    def orders(self):
        ids = sorted(self.rules)
        return {tuple(S.repaired(list(p), self.inside)) for p in permutations(ids)}

    def test_containment_is_the_engines(self):
        from rung2.engine2 import strictly_below
        for a in self.rules:
            for b in self.rules:
                self.assertEqual(b in self.inside[a],
                                 a != b and strictly_below(self.eng.ext[b], self.eng.ext[a]))
                self.assertEqual(b in self.around[a], a in self.inside[b])

    def test_what_an_order_decides_is_the_engines_and_first_matchs(self):
        for o in self.orders():
            self.assertTrue(S.installs(list(o), self.rules, self.inst, SPACE))

    def test_an_order_that_breaks_containment_does_not_install(self):
        catch_all = next(r for r, x in self.rules.items() if x.action == "T1_GENERAL")
        bad = [catch_all] + [r for r in sorted(self.rules) if r != catch_all]
        self.assertFalse(S.installs(bad, self.rules, self.inst, SPACE))

    def test_the_bound_bounds_and_is_the_right_undefeated(self):
        bound = S.coverage(self.inst)
        und = S.undefeated(self.eng.ext, self.inside)
        want = 0
        for r, m in und.items():
            want |= m & TRUTH.get(self.rules[r].action, 0)
        self.assertEqual(bound, want.bit_count())
        for o in self.orders():
            self.assertLessEqual(self.inst.score(self.inst.searched(o)), bound)

    def test_completing_loses_nothing(self):
        own = S.completed(self.eng)
        beaten_by = {r: self.eng.beats_me(r) for r in self.rules}
        pos = {r: i for i, r in enumerate(own)}
        self.assertTrue(all(pos[b] < pos[r] for r in own for b in beaten_by[r]))
        right = self.inst.right(self.inst.searched(own))
        self.assertEqual(MI.right_mask(self.eng) & ~right, 0)

    def test_read_rules_with_and_without_labels(self):
        labels = [(i, MI.corpus_truth()[i]) for i in range(40)]
        for got in (S.read_rules(self.eng, SPACE, TRUTH),
                    S.read_rules(self.eng, SPACE, TRUTH, labels=labels)):
            self.assertTrue(all(got["gates"].values()))
            self.assertGreaterEqual(got["with_the_truth"]["right"], got["completed"]["right"])
            self.assertGreaterEqual(got["completed"]["right"], got["record"]["right"])
            self.assertLessEqual(got["with_the_truth"]["right"], got["bound"]["right"])
            self.assertEqual(got["with_the_truth"]["search"]["n_starts"], 65)
            self.assertEqual(got["with_the_truth"]["search"]["best_from_index"] is not None, True)
            r = got["record"]
            self.assertEqual(r["halves"]["keyword"] + r["halves"]["outside"], r["right"])
        self.assertIn("by_its_labels", got)
        self.assertGreaterEqual(got["by_its_labels"]["labels"]["searched"],
                                got["by_its_labels"]["labels"]["completed"])


class TestTheLabels(unittest.TestCase):

    def test_the_labels_decide_as_the_engine_does(self):
        eng = hand_engine()
        inside, around = S.containment(eng)
        rules = {r.rule_id: r for r in eng.rules}
        labels = [(i, MI.corpus_truth()[i]) for i in range(60)]
        M, W, full = S.label_masks(eng, labels, inside)
        corpus = MI.corpus()
        inst = S.instance(eng.rules, eng.ext, inside, around, TRUTH, SPACE.n)
        for p in list(permutations(sorted(rules)))[::7]:
            o = S.repaired(list(p), inside)
            e2 = S.installed_in(o, rules, SPACE)
            want = 0
            for idx, q in labels:
                outcome, winner, _ = e2.decide(corpus[idx])
                want += outcome == "ACTION" and winner.action == q
            self.assertEqual(LS.score_order(o, M, W, full), want)
            self.assertTrue(S.installs(o, rules, inst, SPACE))

    def test_the_search_starts_from_the_completed_order(self):
        eng = hand_engine()
        inside, around = S.containment(eng)
        own = S.completed(eng)
        labels = [(i, MI.corpus_truth()[i]) for i in range(60)]
        got = S.by_its_labels(eng, own, labels, inside, around)
        self.assertTrue(S.is_linear_extension(got["order"], inside))
        self.assertGreaterEqual(got["labels"]["searched"], got["labels"]["completed"])
        self.assertGreaterEqual(got["labels"]["completed"], got["labels"]["record"])
        self.assertEqual(got["labels"]["of"], 60)


class TestWhereTheBoundFallsShort(unittest.TestCase):
    """Added after the first run."""

    def setUp(self):
        # The keyword's rule, a rule of another queue nested in it, and a rule that
        # carries a queue billing tickets rarely have; no catch-all.
        raw = [r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True)),
               r_("T2_TECHNICAL", c_("has_security_keyword", "eq", True), c_("severity", "gte", 3)),
               r_("T1_GENERAL", c_("product", "eq", "billing"))]
        self.eng = MC.install(raw, SPACE).engine
        self.ids = [r.rule_id for r in self.eng.rules]

    def test_the_ways_partition_what_the_bound_leaves(self):
        ways = S.short_of(self.eng, TRUTH, SPACE.n)
        inside, around = S.containment(self.eng)
        inst = S.instance(self.eng.rules, self.eng.ext, inside, around, TRUTH, SPACE.n)
        self.assertEqual(ways["short"].bit_count(), SPACE.n - S.coverage(inst))
        parts = [ways[k] for k in ("impasse", "unwritten", "contained")]
        self.assertTrue(all(p for p in parts))
        self.assertEqual(parts[0] | parts[1] | parts[2], ways["short"])
        self.assertEqual(sum(p.bit_count() for p in parts), ways["short"].bit_count())
        covered = 0
        for e in self.eng.ext.values():
            covered |= e
        self.assertEqual(ways["impasse"], ways["short"] & ~covered)
        kw = SPACE.mask["has_security_keyword"][True]
        self.assertEqual(ways["contained"] & ~kw, 0)

    def test_the_nested_rule_holds_the_keywords_points(self):
        got, ok = S.read_short(self.eng, SPACE, TRUTH, answer_right=None)
        self.assertTrue(ok)
        self.assertEqual(got["held_by"][0]["rule"], self.ids[1])
        self.assertEqual(got["held_by"][0]["action"], "T2_TECHNICAL")
        self.assertIn("SECURITY_INCIDENT", got["contained_by_queue"])
        self.assertEqual(got["contained"]["keyword"], got["contained"]["points"])
        self.assertNotIn("the_median_answer_right", got)

    def test_what_an_answer_decides_among_them(self):
        ways = S.short_of(self.eng, TRUTH, SPACE.n)
        right = MC.install([r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True))],
                           SPACE).engine
        mask = MI.right_mask(right)
        got, _ = S.read_short(self.eng, SPACE, TRUTH, answer_right=mask)
        self.assertEqual(got["the_median_answer_right"]["points"],
                         (mask & ways["short"]).bit_count())
        self.assertGreater(got["the_median_answer_right"]["by_queue"]["SECURITY_INCIDENT"], 0)

    def test_the_median_answer(self):
        def row(*rules):
            return {"payload": {"rules": list(rules)}}
        sec = r_("SECURITY_INCIDENT", c_("has_security_keyword", "eq", True))
        bil = r_("BILLING_SPECIALIST", c_("product", "eq", "billing"))
        t1 = r_("T1_GENERAL", c_("severity", "gte", 1))
        rows = [(1, row(sec, bil, t1)), (2, row(sec)), (3, row(sec, bil))]
        rights = sorted(MI.right_mask(MC.install(r["payload"]["rules"], SPACE).engine).bit_count()
                        for _, r in rows)
        got = S.median_answer_right(rows)
        self.assertEqual(got.bit_count(), rights[1])
        self.assertIsNone(S.median_answer_right([]))


class TestTheCeiling(unittest.TestCase):

    def test_the_search_finds_the_hidden_policys_optimum(self):
        got = S.hidden_ceiling(SPACE, TRUTH)
        self.assertTrue(got["passes"])
        self.assertEqual((got["best"], got["n"]), (SPACE.n, SPACE.n))
        self.assertEqual(got["n_starts"], 64)


def fake_runs(at=F(3, 5), rec=F(2, 5), bound=F(4, 5), comp=F(1, 2), lab=F(1, 2),
              truth=F(3, 5), kw=(10, 5), gain=F(1, 10), runs=S.L_RUNS):
    def fr(x):
        return {"fraction": str(x), "value": float(x)}
    out = {}
    for t in runs:
        out[t] = {"loop": {"record": {"share": fr(rec), "halves": {"keyword": 0, "outside": 0}},
                           "bound": {"share": fr(bound)}, "completed": {"share": fr(comp)},
                           "by_its_labels": {"share": fr(lab)},
                           "with_the_truth": {"share": fr(truth),
                                              "halves": {"keyword": kw[0], "outside": kw[1]}}},
                  "at_once_median": {"record": fr(at), "gain_with_the_truth": fr(gain)}}
    return out


def holds(runs):
    return {c["clause"]: c["holds"] for c in S.read_expectation(runs)}


class TestTheExpectation(unittest.TestCase):

    def test_at_the_lines(self):
        # gap 1/5: completing gives back exactly half of it.
        got = holds(fake_runs(bound=F(3, 5), truth=F(3, 5), comp=F(1, 2), lab=F(59, 100),
                              kw=(6, 5), gain=F(1, 10)))
        self.assertEqual(got, {"S1": True, "S2": True, "S3": True, "S4": True, "S5": True,
                               "S6": True})

    def test_just_past_the_lines(self):
        got = holds(fake_runs(bound=F(59, 100), truth=F(59, 100), comp=F(49, 100), lab=F(3, 5),
                              kw=(5, 5), gain=F(19, 100)))
        self.assertEqual(got, {"S1": False, "S2": False, "S3": False, "S4": False, "S5": False,
                               "S6": False})

    def test_s3_reads_two_runs_and_s5_two_named(self):
        runs = fake_runs()
        runs["l_r3"]["loop"]["completed"]["share"] = {"fraction": "2/5", "value": 0.4}
        runs["l_r3"]["loop"]["with_the_truth"]["halves"] = {"keyword": 0, "outside": 9}
        got = holds(runs)
        self.assertTrue(got["S3"])
        self.assertTrue(got["S5"])
        runs["l_r2"]["loop"]["completed"]["share"] = {"fraction": "2/5", "value": 0.4}
        self.assertFalse(holds(runs)["S3"])

    def test_over_nothing(self):
        self.assertEqual(set(holds({}).values()), {False})
        self.assertEqual(set(holds(fake_runs(runs=S.L_RUNS[:2])).values()) - {False}, {True})
        short = holds(fake_runs(runs=S.L_RUNS[:2]))
        for c in ("S1", "S2", "S4", "S6"):
            self.assertFalse(short[c])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(S, "hidden_ceiling", side_effect=AssertionError("searched")), \
                mock.patch.object(S, "inputs", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                S.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
