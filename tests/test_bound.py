"""
PLAN_BOUND.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §8, the finder's two, and the lines of §0, so that moving
    one after a figure exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The argument, on instances small enough to check by hand: a two-case cycle,
    a three-case cycle, a cycle through a case with two right rules, the same
    shape without the containment, copies merged into one class, and the
    hybrid pool's own counterexample to an edge from subsumption.
  * `verify`: it accepts what `find` produces and refuses each way a
    certificate can be wrong, and it reaches none of `find`'s machinery.
  * Validity against the exact optimum on random instances, and the same
    certificate under three values of PYTHONHASHSEED.
  * The blocking checks on the real records, a tampered bound caught, and that
    `bound/gates.py`, which the dry run runs, never packs a cycle on rung 1's
    rules.
  * The stage end to end on synthetic instances whose verdicts are worked by
    hand, its two refusals, and each verdict at its edge.

**No test here writes under `results*/`, and none packs a cycle on the 577
rules.** The rules the certificate is run on are synthetic or the hidden
policy's.
"""

from __future__ import annotations

import ast
import copy
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from bound import certificate as C
from bound import gates, plan, score
from bound import instances as I
from reuse import plan as reuse_plan
from primacy import plan as primacy_plan

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


def inst(rules: dict[str, tuple[set[int], set[int]]], n: int, name="t") -> C.Instance:
    """An instance from {rule: (cases it is in the pool of, cases it gets right)}."""
    ids = sorted(rules)
    M = {r: sum(1 << c for c in rules[r][0]) for r in ids}
    W = {r: sum(1 << c for c in rules[r][1]) for r in ids}
    for r in ids:
        assert rules[r][1] <= rules[r][0]
    return C.Instance(name, ids, M, W, n)


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_of_section_8(self):
        self.assertEqual(plan.PLAN, Path("PLAN_BOUND.md"))
        self.assertEqual(plan.OUT, Path("results_bound"))
        self.assertEqual(plan.SCORE_PATH, Path("results_bound/score.json"))
        self.assertEqual(plan.RULES, Path("results/llm_run.json"))
        self.assertEqual(plan.FULLSPACE, Path("results3/order_search_ls_fullspace.json"))
        self.assertEqual(plan.SPLITS, Path("results3/order_search_ls.json"))
        self.assertEqual(plan.BUDGET, Path("results3/start_budget_check.json"))
        self.assertEqual(plan.CEILINGS, Path("results3/order_search.json"))
        self.assertEqual(plan.POOLS, ("puro", "hibrido"))
        self.assertEqual((plan.N_SPLITS, plan.SPLIT_SEED, plan.N_SPACE), (5, 17, 134400))

    def test_the_lines_of_section_0(self):
        self.assertEqual(plan.H_A_LINE, 0.50)
        self.assertEqual(plan.H_B_LINE, 0.50)
        self.assertEqual(plan.SPACE_PLACES, 4)
        self.assertEqual(plan.H_D_LINE, 0.75)

    def test_the_checks_and_the_finder(self):
        self.assertEqual((plan.PLUMBING_SEED, plan.PLUMBING_ORDERS), (17, 3))
        self.assertEqual((plan.BRUTE_SEED, plan.BRUTE_INSTANCES, plan.BRUTE_MAX_RULES),
                         (17, 2000, 7))
        self.assertEqual((C.FINDER_SEED, C.FINDER_STARTS), (17, 16))

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        self.assertNotIn(plan.PLAN, (reuse_plan.PLAN, primacy_plan.PLAN))


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ________________________ (date: ______________)**\n"
        )["passes"])

    def test_one_signed_line_passes_this_plan(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-16)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-16)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


# ---------------------------------------------------------------------------
# The argument, by hand
# ---------------------------------------------------------------------------

class TestTheArgumentByHand(unittest.TestCase):

    def check(self, i: C.Instance, nu: int, opt: int) -> dict:
        cert = C.certificate(i)
        self.assertEqual(cert["nu"], nu)
        self.assertEqual(C.brute_force(i), opt)
        self.assertTrue(C.verify(i, cert)["ok"])
        self.assertGreaterEqual(cert["bound"], opt)
        return cert

    def test_two_rules_that_split_one_territory(self):
        """a and b match the same three cases; a gets two right, b one. No
        order gives each a part, so one case is lost whatever comes first."""
        i = inst({"a": ({0, 1, 2}, {0, 1}), "b": ({0, 1, 2}, {2})}, 3)
        cert = self.check(i, nu=1, opt=2)
        self.assertEqual(cert["nu_by_length"], {"2": 1})
        self.assertEqual(cert["coverable"], 3)

    def test_three_rules_in_a_ring(self):
        """Each case is matched by two rules and right for the first of them:
        a before b, b before c, c before a. One case is lost."""
        i = inst({"a": ({0, 2}, {0}), "b": ({0, 1}, {1}), "c": ({1, 2}, {2})}, 3)
        cert = self.check(i, nu=1, opt=2)
        self.assertEqual(cert["nu_by_length"], {"3": 1})

    def test_a_case_with_two_right_rules_closes_a_cycle_by_containment(self):
        """Case 0 is right for a1 and a2, which are not copies, and wrong for b;
        case 1 is right for b and wrong for both a's. Each R is inside the
        other's X, so one of the two is lost. Case 2 is a1's alone."""
        i = inst({"a1": ({0, 1, 2}, {0, 2}), "a2": ({0, 1}, {0}),
                  "b": ({0, 1}, {1})}, 3)
        cert = self.check(i, nu=1, opt=2)
        self.assertEqual(cert["n_classes"], 3)
        self.assertEqual(cert["n_singleton_signatures"], 1)

    def test_without_the_containment_there_is_no_cycle(self):
        """The same, except that a2 does not match case 1: then a2, b, a1 wins
        all three, and the certificate must claim nothing."""
        i = inst({"a1": ({0, 1, 2}, {0, 2}), "a2": ({0}, {0}),
                  "b": ({0, 1}, {1})}, 3)
        self.check(i, nu=0, opt=3)
        j = inst({"a1": ({0, 1}, {0}), "a2": ({0}, {0}), "b": ({0, 1}, {1}),
                  "x": ({0}, set())}, 2)
        self.check(j, nu=0, opt=2)

    def test_copies_are_one_class(self):
        i = inst({"a": ({0, 1}, {0}), "a_copy": ({0, 1}, {0}), "b": ({0, 1}, {1})}, 2)
        cls = C.classes(i)
        self.assertEqual([m for m, _, _ in cls], [("a", "a_copy"), ("b",)])
        self.check(i, nu=1, opt=1)

    def test_no_edge_from_subsumption_in_the_hybrid_pool(self):
        """`IDEAS.md`'s entry adds subsumption's edges; rung 3's hybrid pool
        does not. D is strictly inside A; on case 0 the pool is {A, C} and only
        A is right; on case 1 it is {C, D} and only C is right. With an edge
        D before A the three would close a ring, and yet the order A, C, D wins
        both. The certificate must claim nothing."""
        i = inst({"A": ({0}, {0}), "C": ({0, 1}, {1}), "D": ({1}, set())}, 2)
        self.check(i, nu=0, opt=2)

    def test_uncontested_and_uncoverable_cases(self):
        i = inst({"a": ({0, 1}, {0}), "b": ({1, 2}, set())}, 4)
        sig = C.signatures(i)
        self.assertEqual((sig.coverable, sig.uncontested, len(sig.keys)), (1, 1, 0))
        self.check(i, nu=0, opt=1)

    def test_multiplicities_follow_the_capacities(self):
        """Three cases on a's side, two on b's: two of b's are a pair with a's,
        so the loss is two and one cycle carries both."""
        i = inst({"a": (set(range(5)), {0, 1, 2}), "b": (set(range(5)), {3, 4})}, 5)
        cert = self.check(i, nu=2, opt=3)
        self.assertEqual([y for y, _ in cert["cycles"]], [2])


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

class TestVerifyRefusesEveryWayToBeWrong(unittest.TestCase):

    def setUp(self):
        self.i = inst({"a": ({0, 2}, {0}), "b": ({0, 1}, {1}), "c": ({1, 2}, {2}),
                       "d": ({0, 1, 2, 3}, {3})}, 4)
        self.cert = C.certificate(self.i)
        self.assertTrue(C.verify(self.i, self.cert)["ok"])
        self.assertEqual(self.cert["nu"], 1)

    def bad(self, change) -> dict:
        c = copy.deepcopy(self.cert)
        change(c)
        return C.verify(self.i, c)

    def test_an_inflated_multiplicity(self):
        def f(c):
            c["cycles"][0][0] += 1
            c["nu"] += 1
        self.assertFalse(self.bad(f)["ok"])

    def test_a_broken_containment(self):
        def f(c):
            c["cycles"][0][1].reverse()
        self.assertFalse(self.bad(f)["ok"])

    def test_a_case_that_is_not_contested(self):
        def f(c):
            c["cycles"][0][1][0] = 3   # only d matches it, and d is right
        self.assertFalse(self.bad(f)["ok"])

    def test_a_cycle_of_one_case_and_a_zero_multiplicity(self):
        self.assertFalse(self.bad(lambda c: c["cycles"][0].__setitem__(1, [0]))["ok"])
        self.assertFalse(self.bad(lambda c: c["cycles"][0].__setitem__(0, 0))["ok"])

    def test_a_wrong_total_or_a_wrong_bound(self):
        self.assertFalse(self.bad(lambda c: c.__setitem__("nu", 2))["ok"])
        self.assertFalse(self.bad(lambda c: c.__setitem__("coverable", 5))["ok"])

    def test_verify_reaches_none_of_finds_machinery(self):
        """It rebuilds every pattern and capacity from the masks; a shared bug
        between finding and checking would otherwise pass unseen."""
        tree = ast.parse((REPO / "bound/certificate.py").read_text())
        fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        reached = set()
        todo = ["verify"]
        while todo:
            f = todo.pop()
            if f in reached or f not in fns:
                continue
            reached.add(f)
            todo += [n.func.id for n in ast.walk(fns[f])
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
        self.assertEqual(reached, {"verify", "_pattern", "_capacity"})


# ---------------------------------------------------------------------------
# Validity, and determinism
# ---------------------------------------------------------------------------

class TestValidityAgainstTheExactOptimum(unittest.TestCase):

    def test_never_below_the_optimum_and_always_verified(self):
        rng = random.Random(2026)
        tight = 0
        for _ in range(300):
            i = gates.random_instance(rng, rng.randint(2, 6), rng.randint(3, 25),
                                      rng.choice((0.3, 0.5, 0.7)), rng.choice((2, 3)))
            cert = C.certificate(i)
            opt = C.brute_force(i)
            self.assertGreaterEqual(cert["bound"], opt)
            self.assertTrue(C.verify(i, cert)["ok"])
            tight += cert["bound"] == opt
        self.assertGreater(tight, 200)

    def test_every_start_is_valid_and_the_largest_is_kept(self):
        rng = random.Random(5)
        for _ in range(50):
            i = gates.random_instance(rng, 6, 25, 0.6, 3)
            sig = C.signatures(i)
            best, nus = C.best_packing(sig)
            self.assertEqual(len(nus), C.FINDER_STARTS + 1)
            self.assertEqual(sum(y for y, _ in best), max(nus))
            self.assertLessEqual(max(nus), sig.coverable - C.brute_force(i))

    def test_the_packing_stops_only_when_no_cycle_is_left(self):
        """Step 3 of the header. Rebuilt by hand from what `find` returns: the
        capacity left per signature, the containment graph over what is left,
        and a plain depth-first search for a cycle in it. A strongly connected
        component the finder missed would leave one."""
        rng = random.Random(11)
        for _ in range(200):
            i = gates.random_instance(rng, rng.randint(3, 8), rng.randint(5, 40), 0.6, 3)
            sig = C.signatures(i)
            V = C.n_nodes(sig)
            shuffled = list(range(V))
            rng.shuffle(shuffled)
            for rank in (None, shuffled):
                cycles = C.find(sig, rank)
                left = list(sig.weight)
                for y, labs in cycles:
                    for k in labs:
                        left[k] -= y
                self.assertTrue(all(c >= 0 for c in left))
                live = [k for k in range(len(sig.keys)) if left[k] > 0]
                nodes = sorted({sig.keys[k][0] for k in live})
                succ = {a: set() for a in nodes}
                for k in live:
                    a, x = sig.keys[k]
                    for b in nodes:
                        if set(b) <= set(x):
                            succ[a].add(b)
                state = {}

                def cyclic(a):
                    state[a] = 1
                    for b in succ[a]:
                        if state.get(b) == 1 or (b not in state and cyclic(b)):
                            return True
                    state[a] = 2
                    return False
                self.assertFalse(any(a not in state and cyclic(a) for a in nodes))

    def test_the_signatures_score_orders_as_score_order_does(self):
        rng = random.Random(9)
        from rung3.local_search import random_order, score_order
        for k in range(100):
            i = gates.random_instance(rng, rng.randint(2, 8), rng.randint(3, 30), 0.5, 3)
            o = random_order(i.ids, seed=k)
            self.assertEqual(gates.score_by_signatures(i, o),
                             score_order(o, i.M, i.W, i.full))


CHILD = """
import json, random
from bound import gates
from bound.certificate import certificate
rng = random.Random(31)
out = []
for _ in range(20):
    i = gates.random_instance(rng, 7, 40, 0.5, 3, copy=0.4)
    c = certificate(i)
    out.append([c["nu"], c["cycles"], c["nu_by_start"]])
print(json.dumps(out))
"""


class TestTheSameCertificateUnderAnyHashSeed(unittest.TestCase):
    """Rule ids are strings, and a set of strings iterates by hash. Only another
    process with another PYTHONHASHSEED exercises that."""

    def test_three_hash_seeds(self):
        outs = []
        for seed in ("0", "1", "4242"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            p = subprocess.run([sys.executable, "-c", CHILD], capture_output=True,
                               text=True, env=env, cwd=REPO)
            self.assertEqual(p.returncode, 0, p.stderr)
            outs.append(json.loads(p.stdout))
        self.assertEqual(outs[0], outs[1])
        self.assertEqual(outs[0], outs[2])
        self.assertTrue(any(o[0] for o in outs[0]))


# ---------------------------------------------------------------------------
# The blocking checks on the real records
# ---------------------------------------------------------------------------

class TestTheBlockingChecksOnTheRecords(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base = I.learned()
        cls.space = I.space_instances(cls.base)
        cls.corpus = I.corpus_instances(cls.base)
        cls.pub = I.published()

    def test_h_g1_reproduces_what_is_published(self):
        g = gates.gate_hg1(self.base, self.space, self.corpus, self.pub, suite=False)
        self.assertTrue(g["passes"], g["problems"])
        self.assertEqual(len(g["instances"]), 2 + 2 * plan.N_SPLITS)

    def test_h_g1_catches_a_tampered_bound(self):
        """The plumbing is held passing here, so that only the tampering can
        fail the check; `test_h_g1_reproduces_what_is_published` runs it."""
        with mock.patch.object(gates, "plumbing", return_value=True):
            pub = copy.deepcopy(self.pub)
            pub["space"]["puro"]["bound"] = 0.8785
            self.assertFalse(gates.gate_hg1(self.base, self.space, self.corpus,
                                            pub, suite=False)["passes"])
            pub = copy.deepcopy(self.pub)
            pub["corpus"][(2, "hibrido")]["attained"] += 10 ** 4
            self.assertFalse(gates.gate_hg1(self.base, self.space, self.corpus,
                                            pub, suite=False)["passes"])
            self.assertTrue(gates.gate_hg1(self.base, self.space, self.corpus,
                                           self.pub, suite=False)["passes"])

    def test_the_published_scores(self):
        self.assertEqual(self.pub["space"]["puro"]["attained"], 0.7905)
        self.assertEqual(self.pub["space"]["hibrido"]["attained"], 0.7557)
        for key, p in self.pub["corpus"].items():
            with self.subTest(key):
                self.assertTrue(all(v is not None for v in p["sources"].values()))
                self.assertEqual(p["attained"], max(p["sources"].values()))

    def test_four_decimals_name_one_count_or_none(self):
        self.assertEqual(I.count_from(0.8786, 1005), 883)
        self.assertIsNone(I.count_from(0.7905, 134400))

    def test_h_g2_and_h_g3_pass(self):
        self.assertTrue(gates.gate_hg2()["passes"])
        self.assertTrue(gates.gate_hg3()["passes"])

    def test_the_dry_run_never_packs_a_cycle_on_the_rules(self):
        """`gates.py` is what the dry run runs. Only H-g2 and H-g3 may build a
        certificate, and they are handed the hidden policy and synthetic
        instances; nothing else in the module may reach the finder."""
        tree = ast.parse((REPO / "bound/gates.py").read_text())
        imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                    for a in n.names}
        for forbidden in ("find", "best_packing", "measure", "score", "_Graph"):
            self.assertNotIn(forbidden, imported)
        for fn in (n for n in tree.body if isinstance(n, ast.FunctionDef)):
            calls = {c.func.id for c in ast.walk(fn)
                     if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
            if fn.name in ("gate_hg2", "gate_hg3"):
                continue
            with self.subTest(fn.name):
                self.assertNotIn("certificate", calls)
        run_all = next(n for n in tree.body
                       if isinstance(n, ast.FunctionDef) and n.name == "run_all")
        hg_calls = [c for c in ast.walk(run_all) if isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Name) and c.func.id in ("gate_hg2", "gate_hg3")]
        self.assertTrue(all(not c.args and not c.keywords for c in hg_calls))


# ---------------------------------------------------------------------------
# The stage, on synthetic instances worked by hand
# ---------------------------------------------------------------------------

def synthetic_checks():
    """Two 'space' instances and ten 'corpus' ones, small, with published
    scores chosen so the verdicts can be worked by hand."""
    pair = inst({"a": (set(range(10)), set(range(6))), "b": (set(range(10)), {6, 7, 8})}, 10)
    # coverable 9, nu 3, bound 6. Published: the space reads 0.6000 (met) for
    # the pure pool and 0.5000 for the hybrid one (not met).
    space = {"puro": pair, "hibrido": pair}
    pub_space = {"puro": {"attained": 0.6}, "hibrido": {"attained": 0.5}}
    corpus, pub_corpus = {}, {}
    for s in range(plan.N_SPLITS):
        for p in plan.POOLS:
            corpus[(s, p)] = pair
            # residue 9 - a; share 3 / (9 - a)
            a = {0: 6, 1: 5, 2: 4, 3: 3, 4: 6}[s] if p == "puro" else 5
            pub_corpus[(s, p)] = {"attained": a, "sources": {"x": a}}
    return SimpleNamespace(space=space, corpus=corpus,
                           pub={"space": pub_space, "corpus": pub_corpus})


class TestTheStageOnSyntheticInstances(unittest.TestCase):

    def test_the_verdicts_by_hand(self):
        r = score.score(synthetic_checks())
        sp = r["space"]
        self.assertEqual((sp["puro"]["coverable"], sp["puro"]["nu"], sp["puro"]["bound"]),
                         (9, 3, 6))
        # puro: residue 0.9 - 0.6 = 0.3, share 0.3 / 0.3 = 1, met
        self.assertAlmostEqual(sp["puro"]["share_closed"], 1.0)
        self.assertTrue(sp["puro"]["met"])
        # hibrido: residue 0.4, share 0.75, not met
        self.assertAlmostEqual(sp["hibrido"]["share_closed"], 0.75)
        self.assertFalse(sp["hibrido"]["met"])
        v = r["verdicts"]
        self.assertEqual(v["H-a"]["verdict"], "holds")
        self.assertEqual(v["H-b"]["verdict"], "holds")
        self.assertEqual(v["H-c"]["verdict"], "refuted")
        # corpus shares: puro 3/3, 3/4, 3/5, 3/6, 3/3; hibrido 3/4 five times.
        # Sorted: .5 .6 .75 .75 .75 .75 .75 .75 1 1 -> median .75
        self.assertAlmostEqual(v["H-d"]["value"], 0.75)
        self.assertEqual(v["H-d"]["verdict"], "holds")

    def test_a_bound_below_a_searched_score_stops_the_stage(self):
        c = synthetic_checks()
        c.pub["corpus"][(0, "puro")]["attained"] = 7
        with mock.patch("builtins.print"), self.assertRaises(SystemExit):
            score.score(c)

    def test_a_certificate_that_does_not_verify_stops_the_stage(self):
        with mock.patch.object(score, "verify",
                               return_value={"ok": False, "nu": 0, "problems": ["x"]}), \
             self.assertRaises(SystemExit):
            score.score(synthetic_checks())

    def test_no_residue_counts_as_share_one(self):
        alone = inst({"a": ({0}, {0}), "b": ({1}, set())}, 2)
        m = score.measure(alone, 1, on_space=False)
        self.assertEqual((m["residue"], m["share_closed"], m["met"]), (0, 1.0, True))
        pair = inst({"a": ({0, 1}, {0}), "b": ({0, 1}, {1})}, 2)
        m = score.measure(pair, 1, on_space=False)
        self.assertEqual((m["residue"], m["share_closed"], m["met"]), (1, 1.0, True))


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def test_the_shares(self):
        self.assertEqual(score.verdict_share(0.50, 0.50)["verdict"], "holds")
        self.assertEqual(score.verdict_share(0.4999, 0.50)["verdict"], "refuted")
        self.assertEqual(score.verdict_share(0.75, 0.75)["verdict"], "holds")
        self.assertFalse(score.verdict_share(0.75, 0.75)["thin"])

    def test_thin_is_the_rounding_reaching_across_the_line(self):
        v = score.verdict_share(0.4995, 0.50, (0.4990, 0.5001))
        self.assertEqual((v["verdict"], v["thin"]), ("refuted", True))
        v = score.verdict_share(0.5004, 0.50, (0.5001, 0.5008))
        self.assertEqual((v["verdict"], v["thin"]), ("holds", False))

    def test_the_space_share_range_brackets_the_share(self):
        pair = inst({"a": (set(range(10)), set(range(6))),
                     "b": (set(range(10)), {6, 7, 8})}, 10)
        m = score.measure(pair, 0.5, on_space=True)
        lo, hi = m["share_range"]
        self.assertLess(lo, m["share_closed"])
        self.assertLess(m["share_closed"], hi)

    def test_h_c(self):
        self.assertEqual(score.verdict_h_c({"puro": False, "hibrido": False})["verdict"],
                         "holds")
        self.assertEqual(score.verdict_h_c({"puro": True, "hibrido": False})["verdict"],
                         "refuted")


# ---------------------------------------------------------------------------
# Nothing is measured or written while §0 is unsigned
# ---------------------------------------------------------------------------

class TestNothingIsMeasuredOrWrittenUnsigned(unittest.TestCase):

    def test_the_stage_refuses_before_anything(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                score.main([])
        checks.assert_not_called()
        write.assert_not_called()

    def test_the_dry_run_writes_nothing_and_answers_for_the_checks(self):
        for passes, code in ((True, 0), (False, 1)):
            with self.subTest(passes=passes), \
                 mock.patch.object(gates, "run_all",
                                   return_value=SimpleNamespace(blocking_pass=passes)), \
                 mock.patch.object(gates, "report"), \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write, \
                 mock.patch("builtins.print"):
                self.assertEqual(score.main(["--dry-run"]), code)
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
