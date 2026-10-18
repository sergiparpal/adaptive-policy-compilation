"""
PLAN_STUDENTS.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §3 and §10 and the lines of §0, so that moving one after a
    figure exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The tree by hand: its splits and their order, growth, the plurality's
    tie-break, the folds grouped by ticket, the pruning sequence, the choice of
    `k`, and the tree written as rules of the frozen DSL that the frozen engine
    executes as the tree predicts.
  * The regression: its features, its gradient against finite differences, its
    optimum, its determinism and its choice of `λ`.
  * The cache: the frozen distance and tie-break, its online protocol against
    the frozen file, and its masks.
  * The material and the comparators on the real records, and a tampered figure
    caught.
  * That `students/gates.py`, which the dry run runs, trains no student on the
    proposer's answers and searches no order on them.
  * The stage's verdicts at their edges, on rows built by hand, and its two
    refusals.
  * The same students under three values of PYTHONHASHSEED.

**No test here writes under `results*/`, and none trains a student on the
proposer's answers or scores one against the truth.** Every student fitted
here is fitted on synthetic labels, or on the truth of the whole space, whose
answer is known.
"""

from __future__ import annotations

import ast
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

from harness.cache_baseline import _dist, run_cache_baseline
from harness.ceiling_check import all_cases
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, Case, generate_corpus
from harness.dsl import validate_rule_payload
from rung2.engine2 import Space

from students import cache, gates, logistic, material, plan, rules, score, tree

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def ticket(**kw) -> Case:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "free",
            "product": "dashboard", "channel": "portal", "prior_tickets_30d": 0,
            "off_hours": False, "language": "en"}
    return Case(**(base | kw))


def random_tickets(n: int, seed: int) -> list[Case]:
    rng = random.Random(seed)
    return [Case(**{a: rng.choice(DOMAINS[a]) for a in ATTRIBUTES}) for _ in range(n)]


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs(self):
        self.assertEqual(plan.PLAN, Path("PLAN_STUDENTS.md"))
        self.assertEqual(plan.OUT, Path("results_students"))
        self.assertEqual((plan.N_CORPUS, plan.CORPUS_SEED, plan.SPLIT_SEED,
                          plan.N_SPACE), (2000, 17, 17, 134400))
        self.assertEqual(plan.REUSE_RUNS, (1, 2, 3))
        self.assertEqual(plan.MIN_SIGNATURES, 1)

    def test_the_material_as_section_1_declares_it(self):
        self.assertEqual(plan.MATERIAL, {
            "rung1": {"answers": 579, "right": 245, "train": 286, "test": 293, "reach": 347},
            "reuse1": {"answers": 62, "right": 30, "train": 33, "test": 29, "reach": 32},
            "reuse2": {"answers": 31, "right": 15, "train": 12, "test": 19, "reach": 22},
            "reuse3": {"answers": 42, "right": 23, "train": 21, "test": 21, "reach": 25},
        })

    def test_the_students(self):
        self.assertEqual((plan.FOLDS, plan.FOLD_SEED), (5, 17))
        self.assertEqual(len(plan.LAMBDAS), 11)
        self.assertAlmostEqual(plan.LAMBDAS[0], 1e-4)
        self.assertAlmostEqual(plan.LAMBDAS[-1], 10.0)
        self.assertEqual(list(plan.LAMBDAS), sorted(plan.LAMBDAS))
        self.assertEqual((plan.LBFGS_MEMORY, plan.ARMIJO, plan.GRADIENT_TOL,
                          plan.MAX_ITER), (10, 1e-4, 1e-7, 5000))

    def test_the_checks(self):
        self.assertEqual((plan.MASK_CHECK_SEED, plan.MASK_CHECK_POINTS,
                          plan.SYNTHETIC_SEED, plan.CACHE_DISTANCES),
                         (17, 2000, 17, (0, 1, 2)))

    def test_the_lines_of_section_0(self):
        self.assertEqual((plan.T_A_LINE, plan.T_B_LINE, plan.T_C_LINE,
                          plan.T_D_LINE, plan.T_E_LINE, plan.THIN_SE),
                         (519, 519, 42310, 519, 0, 2))
        self.assertEqual((plan.ARRIVAL_TEST, plan.ARRIVAL_SPACE), (519, 42310))

    def test_the_published_figures(self):
        self.assertEqual(plan.PUBLISHED, {
            "arrival_test": 0.521608, "arrival_space": 0.314807,
            "reversed_test": 0.546734, "reversed_space": 0.566815,
            "specificity_test": 0.1829,
            "searched": {"ls_train": 0.8786, "ls_test": 0.8472, "ls_space": 0.6033},
        })


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
            "**Signed by Sergi: ____________________ (date: __________)**\n")["passes"])

    def test_one_signed_line_passes_this_plan(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-18)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-18)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)

    def test_the_plan_on_disk_is_drafted_with_one_line(self):
        g = plan.gate_signature()
        self.assertEqual(g["found"], 1)


class TestTheThinLabel(unittest.TestCase):

    def test_at_its_edge(self):
        # (b - c)^2 < 4 (b + c)
        self.assertFalse(plan.thin(12, 4))      # 64 < 64 is false
        self.assertTrue(plan.thin(11, 4))       # 49 < 60
        self.assertFalse(plan.thin(0, 0))       # two artefacts that never disagree
        self.assertFalse(plan.thin(10, 0))      # 100 < 40 is false
        self.assertTrue(plan.thin(5, 5))


# ---------------------------------------------------------------------------
# The tree
# ---------------------------------------------------------------------------

class TestTheTreeByHand(unittest.TestCase):

    def test_the_splits_and_their_order(self):
        s = tree.SPLITS
        # keyword 1, severity 3, tier 4, product 5, channel 4, prior 20, off 1, language 5
        self.assertEqual(len(s), 1 + 3 + 4 + 5 + 4 + 20 + 1 + 5)
        self.assertEqual(s[0], (0, "eq", 1))
        self.assertEqual(s[1:4], [(1, "lte", 0), (1, "lte", 1), (1, "lte", 2)])
        self.assertEqual(s[4], (2, "eq", 0))
        self.assertEqual(s[-1], (7, "eq", 4))
        self.assertTrue(tree.holds((1, "lte", 1), tree.encode(ticket(severity=2))))
        self.assertFalse(tree.holds((1, "lte", 1), tree.encode(ticket(severity=3))))

    def test_the_root_split_is_the_purest(self):
        cases = [ticket(product=p, channel=c) for p in DOMAINS["product"]
                 for c in DOMAINS["channel"]]
        labels = ["BILLING_SPECIALIST" if c.product == "billing" else "T2_TECHNICAL"
                  for c in cases]
        full = tree.grow([tree.encode(c) for c in cases],
                         [ACTIONS.index(l) for l in labels])
        self.assertEqual(full.nodes[0].split, (3, "eq", 1))      # product eq billing
        self.assertEqual(len(full.leaves()), 2)
        self.assertTrue(all(full.predict(c) == l for c, l in zip(cases, labels)))

    def test_the_plurality_breaks_ties_by_the_whole_set_then_by_actions(self):
        self.assertEqual(tree.plurality([2, 2, 0], [1, 5, 0]), 1)
        self.assertEqual(tree.plurality([2, 2, 0], [3, 3, 0]), 0)

    def test_an_unpruned_tree_fits_distinct_tickets_exactly(self):
        cases = list(dict.fromkeys(generate_corpus(400, seed=17)))
        rng = random.Random(3)
        labels = [rng.choice(ACTIONS) for _ in cases]
        full = tree.grow([tree.encode(c) for c in cases],
                         [ACTIONS.index(l) for l in labels])
        self.assertTrue(all(full.predict(c) == l for c, l in zip(cases, labels)))

    def test_the_folds_group_copies_and_are_seeded(self):
        X = [(1,), (2,), (1,), (3,), (2,), (4,), (5,), (6,)]
        f = tree.folds(X)
        self.assertEqual(f[0], f[2])
        self.assertEqual(f[1], f[4])
        self.assertEqual(f, tree.folds(X))
        self.assertTrue(all(0 <= v < plan.FOLDS for v in f))

    def test_the_pruning_sequence(self):
        cases = random_tickets(300, 11)
        labels = gates.synthetic(cases, 11)
        full = tree.grow([tree.encode(c) for c in cases],
                         [ACTIONS.index(l) for l in labels])
        seq = tree.prune_sequence(full)
        alphas = [a for a, _ in seq]
        self.assertEqual(alphas[0], 0)
        self.assertEqual(alphas, sorted(set(alphas)))
        last = full.subtree(seq[-1][1])
        self.assertEqual(last.leaves(), [0])
        X = [tree.encode(c) for c in cases]
        y = [ACTIONS.index(l) for l in labels]
        errs = [sum(full.subtree(coll).predict_index(x) != yy for x, yy in zip(X, y))
                for _a, coll in seq]
        self.assertEqual(errs, sorted(errs))
        self.assertEqual(errs[0], sum(full.predict_index(x) != yy for x, yy in zip(X, y)))

    def test_the_choice_of_k(self):
        self.assertEqual(tree.choose([5, 3, 3, 4]), 2)     # ties to the larger k
        self.assertEqual(tree.choose([1, 3, 3, 4]), 0)

    def test_the_fold_subtree_at_beta(self):
        from fractions import Fraction as F
        seq = [(F(0), "a"), (F(1, 2), "b"), (F(2), "c")]
        self.assertEqual(tree._at(seq, F(0)), "a")
        self.assertEqual(tree._at(seq, F(1, 4)), "b")      # (1/2)^2 <= 1/4
        self.assertEqual(tree._at(seq, F(1, 5)), "a")
        self.assertEqual(tree._at(seq, None), "c")


class TestTheTreeIsARuleBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cases = random_tickets(400, 21)
        cls.labels = gates.synthetic(cls.cases, 21)
        cls.fitted = tree.fit(cls.cases, cls.labels)
        cls.space = Space()

    def test_every_leaf_is_a_valid_rule(self):
        for p in tree.rules(self.fitted.tree):
            with self.subTest(p["rule_id"]):
                validate_rule_payload({k: p[k] for k in ("rule_id", "conditions", "action")})

    def test_the_leaves_are_disjoint_and_cover_the_space(self):
        self.assertEqual(gates.partition_problems(gates.leaf_masks(self.fitted.tree),
                                                  self.space.full), [])

    def test_the_frozen_engine_executes_them_as_the_tree_predicts(self):
        sample = random_tickets(500, 22) + self.cases[:100]
        self.assertEqual(gates.engine_problems(self.fitted.tree, sample), 0)

    def test_no_rule_has_more_than_one_condition_per_attribute(self):
        for p in tree.rules(self.fitted.tree):
            attrs = [c["attr"] for c in p["conditions"]]
            self.assertEqual(len(attrs), len(set(attrs)))
            self.assertLessEqual(len(attrs), len(ATTRIBUTES))

    def test_conditions_merge_to_one_per_attribute(self):
        tier, sev, kw = (ATTRIBUTES.index(a) for a in
                         ("customer_tier", "severity", "has_security_keyword"))
        path = [((tier, "eq", 0), False), ((tier, "eq", 1), False),
                ((sev, "lte", 2), True), ((sev, "lte", 0), False), ((kw, "eq", 1), False)]
        self.assertEqual(tree.conditions_of(path), [
            {"attr": "has_security_keyword", "op": "eq", "value": False},
            {"attr": "severity", "op": "in", "value": [2, 3]},
            {"attr": "customer_tier", "op": "in", "value": ["business", "enterprise"]},
        ])
        self.assertEqual(tree.conditions_of([((sev, "lte", 2), True)]),
                         [{"attr": "severity", "op": "lte", "value": 3}])
        self.assertEqual(tree.conditions_of([((sev, "lte", 0), False)]),
                         [{"attr": "severity", "op": "gte", "value": 2}])
        self.assertEqual(tree.conditions_of([((sev, "lte", 1), True), ((sev, "lte", 0), False)]),
                         [{"attr": "severity", "op": "eq", "value": 2}])
        self.assertEqual(tree.conditions_of([((tier, "eq", 0), False), ((tier, "eq", 1), False),
                                             ((tier, "eq", 2), False)]),
                         [{"attr": "customer_tier", "op": "eq", "value": "enterprise"}])

    def test_a_root_alone_is_the_catch_all(self):
        cases = random_tickets(20, 5)
        f = tree.fit(cases, ["T1_GENERAL"] * len(cases))
        r = tree.rules(f.tree)
        self.assertEqual([p["conditions"] for p in r], [[tree.CATCH_ALL]])
        self.assertEqual(r[0]["action"], "T1_GENERAL")

    def test_the_tree_reads_tickets_and_labels_only(self):
        import inspect
        self.assertEqual(list(inspect.signature(tree.fit).parameters), ["cases", "labels"])


# ---------------------------------------------------------------------------
# The regression
# ---------------------------------------------------------------------------

class TestTheRegression(unittest.TestCase):

    def test_the_features(self):
        self.assertEqual(logistic.N_INDICATORS, 47)
        self.assertEqual(logistic.D, 48)
        f = logistic.features(tree.encode(ticket()))
        self.assertEqual(len(f), len(ATTRIBUTES) + 1)
        self.assertEqual(f[-1], logistic.BIAS)
        self.assertEqual(len(set(f)), len(f))

    def test_the_gradient_against_finite_differences(self):
        self.assertLess(gates._fd_check(31), 1e-5)

    def test_a_fit_reaches_its_optimum_and_repeats(self):
        cases = random_tickets(150, 41)
        labels = gates.synthetic(cases, 41)
        a = logistic.fit(cases, labels)
        b = logistic.fit(cases, labels)
        self.assertTrue(a.fit.converged)
        self.assertTrue(logistic.describe(a)["fold_fits_converged"])
        self.assertEqual(a.fit.w, b.fit.w)
        self.assertIn(a.lam, plan.LAMBDAS)
        self.assertTrue(set(a.predict(c) for c in cases) <= set(labels))

    def test_the_classes_are_the_labels_present(self):
        cases = random_tickets(40, 43)
        labels = ["T1_GENERAL" if c.severity > 2 else "SECURITY_INCIDENT" for c in cases]
        f = logistic.fit(cases, labels)
        self.assertEqual(f.classes, ["T1_GENERAL", "SECURITY_INCIDENT"])

    def test_the_choice_of_lambda(self):
        self.assertEqual(logistic.choose([0.5, 0.3, 0.3, 0.9]), 2)
        self.assertEqual(logistic.choose([0.1, 0.3]), 0)


# ---------------------------------------------------------------------------
# The cache
# ---------------------------------------------------------------------------

class TestTheCache(unittest.TestCase):

    def test_the_distance_is_the_frozen_one(self):
        cs = random_tickets(200, 51)
        for a, b in zip(cs, reversed(cs)):
            self.assertEqual(cache.distance(a, b), _dist(a, b))

    def test_the_first_stored_at_the_smallest_distance_wins(self):
        a, b = ticket(severity=1), ticket(severity=2)
        c = cache.fit([a, b, ticket(severity=1)], ["X", "Y", "Z"])
        self.assertEqual(c.predict(ticket(severity=1)), "X")
        self.assertEqual(c.predict(ticket(severity=3)), "X")          # both at 1
        self.assertEqual(c.predict(ticket(severity=2)), "Y")

    def test_its_protocol_is_the_frozen_files(self):
        corpus = generate_corpus(300, seed=17)
        truth = [material.truth()[i] for i in range(300)]
        for d in plan.CACHE_DISTANCES:
            with self.subTest(d=d):
                self.assertEqual(cache.online(corpus, truth, d),
                                 run_cache_baseline(corpus, d))

    def test_its_masks_answer_as_it_does(self):
        sp = Space()
        stored = random_tickets(60, 53)
        c = cache.fit(stored, gates.synthetic(stored, 53))
        masks = cache.space_masks(c, sp)
        cases = list(all_cases())
        for i in random.Random(54).sample(range(sp.n), 400):
            self.assertEqual(gates._decided_at(masks, i, sp.n), c.predict(cases[i]))
        total = 0
        for m in masks.values():
            total += m.bit_count()
        self.assertEqual(total, sp.n)


# ---------------------------------------------------------------------------
# The material and the rules' side, on the real records
# ---------------------------------------------------------------------------

class TestTheMaterialIsTheRecords(unittest.TestCase):

    def test_the_counts_of_section_1(self):
        for run in material.RUNS:
            with self.subTest(run):
                self.assertEqual(material.counts(run), plan.MATERIAL[run])

    def test_the_train_halves_reach_nothing(self):
        for run in material.RUNS:
            self.assertEqual(material.reached(material.answer_set(run, "train")), ())

    def test_the_labels_are_the_records_predicted(self):
        for s in material.answer_sets():
            rec = {r["idx"]: r for r in material.record(s.run)["records"]}
            with self.subTest(s.name):
                self.assertEqual(s.labels, tuple(rec[i]["predicted"] for i in s.idx))
                self.assertEqual(list(s.idx), sorted(s.idx))

    def test_t_g3_passes(self):
        self.assertTrue(gates.gate_tg3()["passes"])


class TestTheSpaceConvention(unittest.TestCase):

    def test_space_index_is_all_cases_order(self):
        cases = list(all_cases())
        for i in random.Random(61).sample(range(len(cases)), 300):
            self.assertEqual(rules.space_index(cases[i]), i)

    def test_a_mask_from_points_is_spaces_bit_convention(self):
        sp = Space()
        cases = list(all_cases())
        m = sp.mask["product"]["billing"]
        pts = [i for i in random.Random(62).sample(range(sp.n), 300)
               if cases[i].product == "billing"]
        built = rules.mask_from_points(pts, sp.n)
        self.assertEqual(built & ~m, 0)
        self.assertTrue(all(rules.bit(built, i, sp.n) for i in pts))


class TestTheRulesSideIsTheRecords(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base = rules.rung1()

    def test_arrival_order_on_the_test_split(self):
        self.assertEqual(rules.scored(self.base.arrival(), self.base.test_masks()),
                         plan.ARRIVAL_TEST)

    def test_rung_1s_engine_on_the_test_split(self):
        self.assertEqual(round(rules.specificity_test(self.base), 4),
                         plan.PUBLISHED["specificity_test"])

    def test_one_reuse_base_rebuilds_and_its_regions_are_decide(self):
        run = "reuse2"
        self.assertEqual(rules.rebuild_mismatches(run), [])
        engine = rules.reuse_base(run).engine
        reg = rules.regions(engine)
        for c in list(material.corpus())[:400]:
            self.assertEqual(gates._decided_at(reg, rules.space_index(c), plan.N_SPACE),
                             rules.decide_action(engine, c))

    def test_the_records_publish_what_the_plan_quotes(self):
        self.assertEqual(gates.published_problems(gates._published()), [])

    def test_a_tampered_figure_is_caught(self):
        pub = gates._published()
        for key, value in (("arrival_test", 0.5), ("specificity_test", 0.2)):
            with self.subTest(key):
                self.assertTrue(gates.published_problems(dict(pub, **{key: value})))
        searched = dict(pub["searched"], ls_test=0.9)
        self.assertTrue(gates.published_problems(dict(pub, searched=searched)))


class TestTheStagesSecondRoutesAgreeOnDecisions(unittest.TestCase):
    """Rule G's second routes, checked on decisions alone: nothing here is
    scored against the truth."""

    @classmethod
    def setUpClass(cls):
        cls.base = rules.rung1()
        cls.ncond = {r["rule_id"]: len(r["conditions"]) for r in cls.base.rules}
        cls.cases = list(all_cases())
        cls.points = random.Random(81).sample(range(plan.N_SPACE), 150)

    def test_rung_1s_engine_point_by_point_is_its_corpus_reading(self):
        corpus = material.corpus()
        for i in range(0, 2000, 7):
            self.assertEqual(score.specificity_point(self.base, corpus[i], self.ncond),
                             gates._specificity_case(self.base, i, self.ncond))

    def test_rung_1s_engine_over_the_space_is_its_point_by_point_reading(self):
        masks = rules.specificity_space(self.base)
        for i in self.points:
            self.assertEqual(gates._decided_at(masks, i, plan.N_SPACE),
                             score.specificity_point(self.base, self.cases[i], self.ncond))

    def test_a_bases_regions_are_decide_off_the_corpus_too(self):
        engine = rules.reuse_base("reuse3").engine
        reg = rules.regions(engine)
        for i in self.points:
            self.assertEqual(gates._decided_at(reg, i, plan.N_SPACE),
                             rules.decide_action(engine, self.cases[i]))


class TestTheStudentsGlueOnASyntheticSet(unittest.TestCase):
    """`read_students` end to end, on real tickets with synthetic labels and a
    synthetic truth: what it reads off a set, and that its second routes run."""

    def test_one_synthetic_set(self):
        corpus = material.corpus()
        idx = tuple(range(0, 2000, 25))
        labels = tuple(gates.synthetic([corpus[i] for i in idx], 91))
        s = material.AnswerSet("synthetic", "all", idx, labels)
        truth = gates.synthetic(list(corpus), 92)
        test = tuple(range(1, 2000, 9))
        rows, fitted = score.read_students([s], lambda x: list(x.labels), truth, test,
                                           list(all_cases()), gates.sample_points(200),
                                           lambda x: set(test[:20]))
        r = rows["synthetic/all"]
        self.assertEqual(set(r), {"tree", "logistic", "cache"})
        for name, row in r.items():
            with self.subTest(name):
                self.assertEqual(row["of"], len(test))
                self.assertEqual(row["abstained"], 0)
                self.assertEqual(row["right"], sum(1 for i in test
                                                   if fitted["synthetic/all"][name].predict(corpus[i]) == truth[i]))
                self.assertEqual(row["reached"]["of"] + row["not_reached"]["of"], len(test))
                self.assertEqual(row["space"]["of"], plan.N_SPACE)


# ---------------------------------------------------------------------------
# The dry run trains nothing on the answers
# ---------------------------------------------------------------------------

class TestTheDryRunTrainsNothingOnTheAnswers(unittest.TestCase):
    """`gates.py` is what the dry run runs. Every fit in it is handed the truth
    of the whole space or synthetic labels, and every search the truth, which
    reproduces a published row. The stage's own functions never appear in it."""

    @classmethod
    def setUpClass(cls):
        cls.tree_ = ast.parse((REPO / "students/gates.py").read_text())

    def test_the_stage_is_not_imported(self):
        names = {a.name for n in ast.walk(self.tree_)
                 if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
        self.assertNotIn("score", names)
        for forbidden in ("read_students", "read_rules", "read_reuse_bases",
                          "verdicts", "fit_students", "majority_floor", "on_test"):
            self.assertNotIn(forbidden, ast.dump(self.tree_))

    def test_every_fit_is_handed_the_space_or_synthetic_labels(self):
        fits = [c for c in ast.walk(self.tree_) if isinstance(c, ast.Call)
                and isinstance(c.func, ast.Attribute) and c.func.attr == "fit"]
        self.assertTrue(fits)
        for c in fits:
            with self.subTest(ast.dump(c.func)):
                self.assertIsInstance(c.args[1], ast.Name)
                self.assertIn(c.args[1].id, ("labels", "syn_labels"))
        sources = {}
        for n in ast.walk(self.tree_):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                    and isinstance(n.targets[0], ast.Name) \
                    and n.targets[0].id in ("labels", "syn_labels"):
                sources.setdefault(n.targets[0].id, set()).add(
                    n.value.func.id if isinstance(n.value, ast.Call)
                    and isinstance(n.value.func, ast.Name) else ast.dump(n.value))
        self.assertEqual(sources, {"labels": {"_space_labels"},
                                   "syn_labels": {"synthetic"}})

    def test_every_search_is_handed_the_truth(self):
        searches = [c for c in ast.walk(self.tree_) if isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute) and c.func.attr == "search_order"]
        self.assertEqual(len(searches), 1)
        arg = searches[0].args[1]
        self.assertEqual((type(arg), getattr(arg, "attr", None)), (ast.Attribute, "truth"))


# ---------------------------------------------------------------------------
# The stage
# ---------------------------------------------------------------------------

def row(right: set[int], decided: dict | None = None, space: int = 0) -> dict:
    return {"right": len(right), "_right": right, "_decided": decided or {},
            "space": {"right": space}}


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def rows(self, tree_n, log_n, cache_n, order_n, space_n, reuse_diffs):
        arrival = row(set(range(519)))
        students = {"rung1/all": {"tree": row(set(range(tree_n)), space=space_n),
                                  "logistic": row(set(range(log_n))),
                                  "cache": row(set(range(cache_n)))}}
        reuse = {}
        for k, d in zip(material.RUNS[1:], reuse_diffs):
            students[f"{k}/all"] = {"tree": row(set(range(400 + d)))}
            reuse[k] = {"base": row(set(range(400)))}
        rules_side = {"arrival": arrival, "answers_order_286": row(set(range(order_n)))}
        return {r["row"]: r for r in score.verdicts(students, rules_side, reuse)}

    def test_at_the_lines(self):
        v = self.rows(519, 500, 400, 519, 42310, (0, 0, 0))
        self.assertEqual([v[k]["holds"] for k in ("T-a", "T-b", "T-c", "T-d", "T-e")],
                         [False, False, False, False, False])

    def test_one_step_inside(self):
        v = self.rows(518, 500, 400, 520, 42311, (-1, -1, 3))
        self.assertEqual([v[k]["holds"] for k in ("T-a", "T-b", "T-c", "T-d", "T-e")],
                         [True, True, True, True, True])

    def test_the_best_student_decides_t_b(self):
        v = self.rows(500, 530, 400, 520, 42311, (-1, -1, -1))
        self.assertTrue(v["T-a"]["holds"])
        self.assertFalse(v["T-b"]["holds"])
        self.assertEqual(v["T-b"]["best"], "logistic")

    def test_t_e_reads_the_median_run(self):
        v = self.rows(500, 500, 400, 520, 42311, (5, -2, -1))
        self.assertEqual(v["T-e"]["value"], -1)
        self.assertTrue(v["T-e"]["holds"])
        self.assertEqual(v["T-e"]["median_run"], "reuse3")

    def test_the_discordance(self):
        a, b = row({1, 2, 3, 4}), row({3, 4, 5})
        self.assertEqual(score.discordance(a, b), {"b": 2, "c": 1, "thin": True})


class TestOnTest(unittest.TestCase):

    def test_counts_abstentions_classes_and_reach(self):
        truth = ["T1_GENERAL", "ACCOUNT_MANAGER", "ACCOUNT_MANAGER", "T2_TECHNICAL"]
        decide = {0: "T1_GENERAL", 1: "ACCOUNT_MANAGER", 2: None, 3: "T1_GENERAL"}.get
        r = score.on_test(decide, [0, 1, 2, 3], truth, reached={0, 2})
        self.assertEqual((r["right"], r["of"], r["abstained"]), (2, 4, 1))
        self.assertEqual(r["per_class"]["ACCOUNT_MANAGER"], {"right": 1, "of": 2})
        self.assertEqual(r["reached"], {"right": 1, "of": 2})
        self.assertEqual(r["not_reached"], {"right": 1, "of": 2})


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
        with mock.patch.object(gates, "run_all",
                               return_value=SimpleNamespace(blocking_pass=True)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            self.assertEqual(score.main(["--dry-run"]), 0)
            write.assert_not_called()
        with mock.patch.object(gates, "run_all",
                               return_value=SimpleNamespace(blocking_pass=False)), \
             mock.patch.object(gates, "report"), \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            with self.assertRaises(SystemExit):
                score.main(["--dry-run"])
            write.assert_not_called()


# ---------------------------------------------------------------------------
# The same students under any hash seed
# ---------------------------------------------------------------------------

CHILD = r"""
import json
from students import cache, gates, logistic, tree
from tests.test_students import random_tickets
cases = random_tickets(160, 71)
labels = gates.synthetic(cases, 71)
probe = random_tickets(200, 72)
t = tree.fit(cases, labels)
l = logistic.fit(cases, labels)
c = cache.fit(cases, labels)
print(json.dumps([[t.predict(x) for x in probe], [l.predict(x) for x in probe],
                  [c.predict(x) for x in probe], tree.rules(t.tree), l.lam]))
"""


class TestTheSameStudentsUnderAnyHashSeed(unittest.TestCase):
    """Labels are strings, and a set of strings iterates by hash. Only another
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


if __name__ == "__main__":
    unittest.main()
