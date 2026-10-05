"""
PLAN_EDGES.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §8 and the three band lines of §0, so that moving one after
    a figure exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The rebuild of `edges/rebuild.py`, on a scripted run small enough to read.
    Given the declared directions it is the record, and given no installed edge
    it is the replay without edges. Every departure without edges is an ACTION
    that becomes a CONFLICT. Flipping the edges hands their cases to the other
    rule and changes nothing else. Every birth happens in every arm.
  * `W-g2` and `W-g3`'s identities on the three Stage B records. They read no
    label and are silent when they pass.
  * The stage's arithmetic, on numbers small enough to check by hand, and each
    verdict at its edge.

**No test here writes under `results*/`, and none computes a figure of §0 on the
Stage B records.** The scripted run is synthetic, labelled by rung 2's loop as
every record is, and owns nothing.
"""

from __future__ import annotations

import json
import math
import random
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from harness.domain import generate_corpus
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import SYSTEM_PROMPT_V1, neighbourhood, render_base_v1
from rung2.shadow2 import run_shadow2

from edges import gates, plan, readings, score
from edges import rebuild as rb
from reuse import plan as reuse_plan
from tests.fixtures import space

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


# ---------------------------------------------------------------------------
# A scripted run: broad rules that overlap, and on every conflict a rule that
# sides with the first rule shown and declares that it beats the others
# ---------------------------------------------------------------------------

class Scripted:
    """Coverage impasses get broad one-condition rules, in turn on severity, tier
    and product, each with its own queue. A conflict gets a rule on the ticket's
    channel and product, with the action of the first rule shown, beating every
    shown rule whose action differs. That gives installed edges, edges
    redundant with subsumption, and cases decided through an edge."""

    name = "scripted"
    BROAD = (("severity", "T2_TECHNICAL"), ("customer_tier", "ACCOUNT_MANAGER"),
             ("product", "BILLING_SPECIALIST"))

    def __init__(self):
        self.n = 0
        self.shown, self.kind = [], None

    def build_base(self, engine, case, undefeated):
        self.shown, self.kind = neighbourhood(engine, case, undefeated)
        return self.shown, self.kind, render_base_v1(self.shown, self.kind, engine, case)

    def propose(self, case, base_text):
        if self.kind == "conflicto":
            action = self.shown[0].action
            return action, {
                "action": action,
                "conditions": [{"attr": "channel", "op": "eq", "value": case.channel},
                               {"attr": "product", "op": "eq", "value": case.product}],
                "beats": [r.rule_id for r in self.shown if r.action != action],
                "loses_to": [], "note": "scripted"}
        attr, action = self.BROAD[self.n % len(self.BROAD)]
        self.n += 1
        return action, {"action": action,
                        "conditions": [{"attr": attr, "op": "eq",
                                        "value": getattr(case, attr)}],
                        "beats": [], "loses_to": [], "note": "scripted"}


def scripted_record(n: int = 120):
    corpus = generate_corpus(n, seed=17)
    engine = PriorityEngine(space=space())
    res = run_shadow2(corpus, engine, Scripted())
    rec = {"rules": [r.as_dict() for r in res.rules], "edge_log": engine.edge_log,
           "records": [vars(r) for r in res.records], "system_prompt": SYSTEM_PROMPT_V1}
    return json.loads(json.dumps(rec)), corpus


class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_of_section_8(self):
        self.assertEqual((plan.RUNS, plan.N, plan.SEED), ((1, 2, 3), 2000, 17))
        for k in plan.RUNS:
            self.assertEqual(plan.run_path(k), Path(f"results_reuse/run_n2000_r{k}.json"))

    def test_the_null_of_section_8(self):
        self.assertEqual((plan.COIN_DRAWS, plan.COIN_SEED), (2000, 47))
        self.assertEqual(plan.MIN_QUALIFYING_EDGES, 20)

    def test_the_three_lines_of_section_0(self):
        self.assertEqual(plan.W_A_REFUTED_AT_OR_ABOVE, 0.50)
        self.assertEqual(plan.W_B_REFUTED_AT_OR_ABOVE, 0.60)
        self.assertEqual(plan.W_C_MIN_SHARE, 0.05)

    def test_the_published_size_w_g1_checks(self):
        self.assertEqual((plan.SPACE_POINTS, plan.T2, plan.T2_SPACE_POINTS),
                         (134_400, "T2_TECHNICAL", 36_720))

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_EDGES.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        self.assertEqual(plan.SCORE_PATH, Path("results_edges/score.json"))

    def test_one_coin_stream_per_run_and_no_hash_in_it(self):
        a, b = plan.coin_rng(1), plan.coin_rng(1)
        self.assertEqual([a.random() for _ in range(5)], [b.random() for _ in range(5)])
        self.assertNotEqual(plan.coin_rng(1).random(), plan.coin_rng(2).random())


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
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-05)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-05)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


class TestTheRebuildOnAScriptedRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rec, cls.corpus = scripted_record()
        cls.declared = rb.rebuild(cls.rec, cls.corpus, space())
        cls.classes = rb.classify(cls.rec, cls.declared)
        cls.without = rb.replay_without_edges(cls.rec, cls.corpus, space())
        cls.d, cls.kinds = rb.edge_decided(cls.rec, cls.without)
        cls.installed = sorted(cls.declared.installed)

    def arm(self, directions, only=None):
        return rb.rebuild(self.rec, self.corpus, space(), directions=directions,
                          only=only)

    def test_the_run_has_what_the_tests_need(self):
        """Installed edges, edges redundant with subsumption, and cases decided
        through an edge: otherwise the tests below would pass vacuously."""
        self.assertIn("installed", self.classes.values())
        self.assertIn("redundant", self.classes.values())
        self.assertGreater(len(self.d), 0)

    def test_every_logged_edge_is_paired_with_its_birth(self):
        edges = rb.all_edges(self.rec)
        self.assertEqual(len(edges), len(self.rec["edge_log"]))
        self.assertEqual([e.key for e in edges], list(range(len(edges))))
        born = rb.births(self.rec)
        for e in edges:
            self.assertIn(e.birth, born)
            self.assertIn(born[e.birth]["rule_id"], (e.winner, e.loser))

    def test_given_the_declared_directions_it_is_the_record(self):
        none = self.arm(rb.without_installed(self.declared.installed))
        self.assertEqual(gates.identity_problems(self.rec, self.declared, self.classes,
                                                 none, self.without), [])

    def test_a_tampered_record_is_caught(self):
        rec = json.loads(json.dumps(self.rec))
        i = next(r["idx"] for r in rec["records"] if r["outcome"] == "ACTION")
        rec["records"][i]["winner_id"] = "R9999"
        none = self.arm(rb.without_installed(self.declared.installed))
        self.assertNotEqual(gates.identity_problems(rec, self.declared, self.classes,
                                                    none, self.without), [])

    def test_a_log_that_does_not_pair_is_refused(self):
        rec = json.loads(json.dumps(self.rec))
        rec["edge_log"] = rec["edge_log"][:-1]
        with self.assertRaises(rb.RebuildError):
            rb.edges_by_birth(rec)

    def test_without_edges_every_departure_is_an_action_that_becomes_a_conflict(self):
        self.assertEqual(set(self.kinds), {"action_to_conflict"})
        row = {r["idx"]: r for r in self.rec["records"]}
        for i in self.d:
            self.assertEqual(row[i]["outcome"], "ACTION")
            self.assertEqual(self.without[i].outcome, "CONFLICT")

    def test_with_no_installed_edge_it_is_the_replay_without_edges(self):
        none = self.arm(rb.without_installed(self.declared.installed))
        self.assertEqual(none.decisions, self.without)

    def test_flipping_hands_the_cases_to_the_other_rule_and_changes_nothing_else(self):
        flipped = self.arm({k: rb.FLIPPED for k in self.installed})
        moved = [i for i in self.d
                 if flipped.decisions[i].action != self.declared.decisions[i].action]
        self.assertGreater(len(moved), 0)
        d = set(self.d)
        for row in self.rec["records"]:
            if row["outcome"] == "ACTION" and row["idx"] not in d:
                self.assertEqual(flipped.decisions[row["idx"]].action, row["predicted"])

    def test_every_birth_happens_in_every_arm(self):
        ids = [r["rule_id"] for r in self.rec["rules"]]
        for directions in ({}, {k: rb.FLIPPED for k in self.installed},
                           rb.without_installed(self.declared.installed)):
            for only in (None, set(), set(self.d)):
                got = self.arm(directions, only).engine.rules
                self.assertEqual([r.rule_id for r in got], ids)

    def test_only_decides_just_those_cases(self):
        part = self.arm({}, only=set(self.d))
        self.assertEqual(set(part.decisions), set(self.d))
        for i in self.d:
            self.assertEqual(part.decisions[i], self.declared.decisions[i])

    def test_the_coin_is_reproducible(self):
        def draws(seed):
            rng = random.Random(seed)
            return [rb.coin_directions(self.installed, rng) for _ in range(3)]
        self.assertEqual(draws("x"), draws("x"))
        self.assertNotEqual(draws("x"), draws("y"))
        self.assertEqual(set(draws("x")[0]), set(self.installed))

    def test_the_stage_assertion_holds_and_has_teeth(self):
        ys, clusters = score.w_a_rows(1, self.rec, self.d, self.declared)
        self.assertEqual(len(ys), len(self.d))
        self.assertEqual(len(clusters), len(self.d))
        rec = json.loads(json.dumps(self.rec))
        i = self.d[0]
        rec["records"][i]["correct"] = not rec["records"][i]["correct"]
        with self.assertRaises(AssertionError):
            score.w_a_rows(1, rec, self.d, self.declared)

    def test_outside_the_shared_regions_the_edges_change_nothing(self):
        """What `score.static` relies on to decide the space without edges only
        where an edge can matter."""
        final = self.declared.engine
        bare = self.arm(rb.without_installed(self.declared.installed), only=set()).engine
        pairs = [(e.winner, e.loser) for e in rb.all_edges(self.rec)
                 if e.key in self.declared.installed]
        for c in self.corpus:
            a, b = final.decide(c), bare.decide(c)
            if (a[0], a[1] and a[1].action) != (b[0], b[1] and b[1].action):
                ids = {r.rule_id for r in final.rules if r.matches(c)}
                self.assertTrue(any(w in ids and l in ids for w, l in pairs))

    def test_the_census_and_the_split_on_the_scripted_run(self):
        sets = score.matched_sets(self.declared.engine, self.corpus)
        c = score.census(self.rec, self.declared, self.classes, sets)
        self.assertEqual(c["logged"], len(self.rec["edge_log"]))
        self.assertEqual(c["installed"], len(self.installed))
        self.assertEqual(c["installed_newborn_wins"] + c["installed_newborn_loses"],
                         c["installed"])
        s = score.split_errors(self.rec, self.d, self.without)
        self.assertEqual(s["right"] + s["wrong_direction"] + s["wrong_material"], s["n"])
        # An edge only removes rules from the undefeated set, so the action it
        # decides is one of the contenders': a right decision is always one a
        # direction could reach.
        self.assertEqual(s["right"] + s["wrong_direction"],
                         s["any_direction_could_be_right"])

    def test_the_post_run_readings_add_up_on_the_scripted_run(self):
        rules = readings.deciding_rules(self.rec, self.d, self.classes)
        self.assertEqual(sum(r["decided"] for r in rules), len(self.d))
        queues = readings.by_queue(self.rec, self.d)
        self.assertEqual(sum(q["decided"] for q in queues.values()), len(self.d))
        for q in queues.values():
            self.assertEqual(q["decided"] - q["right"],
                             sum(q["true_queue_of_the_wrong"].values()))
        sec = readings.security(self.rec, self.d)
        self.assertLessEqual(sec["of_which_through_an_edge"], sec["right_decisions"])


class TestTheStageBRecords(unittest.TestCase):
    """`W-g2` and `W-g3` on the three records: identities, no label read, silent
    when they pass."""

    @classmethod
    def setUpClass(cls):
        cls.corpus = generate_corpus(plan.N, seed=plan.SEED)
        cls.runs = rb.load_runs()

    def test_each_run_is_its_record_and_without_edges_departs_one_way(self):
        for k, rec in self.runs.items():
            with self.subTest(run=k):
                declared = rb.rebuild(rec, self.corpus, space())
                classes = rb.classify(rec, declared)
                without = rb.replay_without_edges(rec, self.corpus, space())
                none = rb.rebuild(rec, self.corpus, space(),
                                  directions=rb.without_installed(declared.installed))
                self.assertEqual(gates.identity_problems(rec, declared, classes,
                                                         none, without), [])
                d, kinds = rb.edge_decided(rec, without)
                self.assertEqual(set(kinds), {"action_to_conflict"})
                self.assertGreater(len(d), 0)
                self.assertNotIn("duplicate", classes.values())

    def test_the_fingerprint_is_deterministic_in_one_process(self):
        """The cross-seed half is `W-g3`'s, in child processes."""
        self.assertEqual(rb.fingerprint(draws=2), rb.fingerprint(draws=2))


class TestTheArithmetic(unittest.TestCase):

    def test_clustered_share_by_hand(self):
        r = score.clustered_share([1, 0, 1, 1], ["a", "a", "b", "c"])
        self.assertEqual((r["n"], r["right"], r["share"], r["clusters"]), (4, 3, 0.75, 3))
        # residuals summed by cluster: a -0.5, b 0.25, c 0.25
        self.assertAlmostEqual(r["se"], math.sqrt(3 / 2 * 0.375) / 4)

    def test_singleton_clusters_are_the_binomial_with_n_minus_one(self):
        ys = [1, 0, 0, 1, 1, 0, 1, 1]
        r = score.clustered_share(ys, list(range(len(ys))))
        p = sum(ys) / len(ys)
        self.assertAlmostEqual(r["se"], math.sqrt(p * (1 - p) / (len(ys) - 1)))

    def test_one_cluster_has_no_error_and_nothing_has_no_share(self):
        self.assertIsNone(score.clustered_share([1, 0], ["a", "a"])["se"])
        self.assertIsNone(score.clustered_share([], [])["share"])

    def test_binomial_and_thin(self):
        b = score.binomial(3, 4)
        self.assertEqual(b["rate"], 0.75)
        self.assertAlmostEqual(b["se"], math.sqrt(0.75 * 0.25 / 4))
        self.assertIsNone(score.binomial(0, 0)["rate"])
        self.assertTrue(score.thin(0.49, 0.50, 0.02))
        self.assertFalse(score.thin(0.45, 0.50, 0.02))
        self.assertFalse(score.thin(0.49, 0.50, None))

    def test_a_tie_with_the_proposer_counts_against_it(self):
        self.assertEqual(score.coin_share([1, 2, 3, 3, 4], 3), 3 / 5)

    def test_the_direction_rate_leaves_ties_and_neither_outside(self):
        rows = [{"k": "a"}, {"k": "a"}, {"k": "b"}, {"k": "tie"},
                {"k": "neither_ever_right"}]
        r = score.direction_rate(rows, "k")
        self.assertEqual((r["n"], r["hits"], r["toward_loser"], r["tie"],
                          r["neither_ever_right"]), (3, 2, 1, 1, 1))

    def test_the_coin_read_among_resolved_and_net_by_hand(self):
        r = readings.coin_readings([1, 2, 0], [1, 2, 0], 3, 1)
        # the third draw resolves nothing and is left out of the first reading
        self.assertEqual(r["right_among_resolved"]["draws"], 2)
        self.assertEqual(r["right_among_resolved"]["proposer"], 0.75)
        self.assertEqual(r["right_among_resolved"]["mean"], 0.5)
        self.assertEqual(r["right_among_resolved"]["share_at_least_the_proposer"], 0.0)
        self.assertEqual(r["right_minus_wrong"]["proposer"], 2)
        self.assertEqual(r["right_minus_wrong"]["share_at_least_the_proposer"], 0.0)
        self.assertEqual(r["right_minus_wrong"]["mean"], 0.0)

    def test_space_labels_by_case_index_are_msb_first(self):
        self.assertEqual(score.labels_by_index({"A": 0b1010, "B": 0b0101}, 4),
                         ["A", "B", "A", "B"])

    def test_the_split_by_hand(self):
        rec = {"rules": [{"rule_id": "R1", "action": "X"},
                         {"rule_id": "R2", "action": "Y"}],
               "records": [{"idx": 0, "truth": "X", "correct": True},
                           {"idx": 1, "truth": "X", "correct": False},
                           {"idx": 2, "truth": "Z", "correct": False}]}
        without = {i: rb.Decision("CONFLICT", None, None, 2, ("R1", "R2"))
                   for i in range(3)}
        self.assertEqual(score.split_errors(rec, [0, 1, 2], without),
                         {"n": 3, "right": 1, "wrong_direction": 1,
                          "wrong_material": 1, "any_direction_could_be_right": 2})


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def test_w_a(self):
        self.assertEqual(score.verdict_w_a(0.4999, 0.01)["verdict"], "holds")
        self.assertEqual(score.verdict_w_a(0.50, 0.01)["verdict"], "refuted")
        self.assertEqual(score.verdict_w_a(None, None)["verdict"], "unadjudicable")
        self.assertTrue(score.verdict_w_a(0.495, 0.01)["thin"])

    def test_w_b(self):
        self.assertEqual(score.verdict_w_b(0.5999, 0.05, 20)["verdict"], "holds")
        self.assertEqual(score.verdict_w_b(0.60, 0.05, 20)["verdict"], "refuted")
        self.assertEqual(score.verdict_w_b(0.30, 0.05, 19)["verdict"], "unadjudicable")

    def test_w_c(self):
        self.assertEqual(score.verdict_w_c(0.05)["verdict"], "holds")
        self.assertEqual(score.verdict_w_c(0.0499)["verdict"], "refuted")
        v = score.verdict_w_c(0.05)
        self.assertAlmostEqual(v["se"], math.sqrt(0.05 * 0.95 / plan.COIN_DRAWS))
        self.assertTrue(v["thin"])


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

    def test_the_post_run_readings_refuse_before_anything_too(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_all",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                readings.main([])
        checks.assert_not_called()
        read.assert_not_called()
        write.assert_not_called()

    def test_the_stage_reads_this_plan_and_no_other(self):
        self.assertNotEqual(plan.PLAN, reuse_plan.PLAN)


if __name__ == "__main__":
    unittest.main()
