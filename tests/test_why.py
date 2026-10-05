"""
PLAN_WHY.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §8, the codebook's fingerprint, the development figures §0
    declares and the four band lines, so that moving one after a figure exists
    is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The codebook on sentences written by hand, in the three languages the
    answers came in, and the categorical feature by hand.
  * The rows and §0's statistics on records small enough to check by hand, and
    the whole stage end to end on a synthetic record: the stage cannot be run on
    the held-out answers before §0 is signed, so this is where it runs first.
  * The blocking checks on the real records, a tampered fingerprint and a
    tampered development figure caught, and **every sentence the codebook is
    handed during the checks belonging to the development set**.
  * Each verdict at its edge.

**No test here writes under `results*/`, and none codes a held-out `why`.**
"""

from __future__ import annotations

import ast
import copy
import math
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from edges import plan as edges_plan
from primacy import plan as primacy_plan
from reuse import plan as reuse_plan
from why import codebook as cb
from why import gates, plan, score
from why import rows as R

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


def question(first: str, second: str, act_first: str, act_second: str) -> str:
    return ("LAS DOS REGLAS QUE CASAN EL TICKET:\n"
            f"  A: SI {first} ENTONCES {act_first}\n"
            f"  B: SI {second} ENTONCES {act_second}\n\nTICKET:\n{{}}")


def answer(k, *, a_first=True, declared="a_beats_b", why="", batch="this_run",
           conds_a="severity eq 4 AND product eq api", conds_b="customer_tier eq free",
           ext=(100, 900), actions=("T2_TECHNICAL", "T1_GENERAL")):
    a, b = f"R{k}a", f"R{k}b"
    first, second = (a, b) if a_first else (b, a)
    ca, cb_ = (conds_a, conds_b) if a_first else (conds_b, conds_a)
    acts = (actions[0], actions[1]) if a_first else (actions[1], actions[0])
    return {"index": k, "rule_a": a, "rule_b": b, "action_a": actions[0],
            "action_b": actions[1], "extension_a": ext[0], "extension_b": ext[1],
            "a_shown_as": "A" if a_first else "B", "shown_as": {"A": first, "B": second},
            "declared": declared,
            "answer": {"a_beats_b": actions[0], "b_beats_a": actions[1]}.get(declared),
            "why": why, "answer_from": batch, "question": question(ca, cb_, *acts)}


# ---------------------------------------------------------------------------
# The constants and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_and_the_split(self):
        self.assertEqual(plan.SOURCE, Path("results2/pair_judgement_1600.json"))
        self.assertEqual(plan.STAGE_D, Path("results2/pair_judgement_learned.json"))
        self.assertEqual(plan.HIDDEN, Path("results2/pair_judgement_hidden.json"))
        self.assertEqual(plan.SAMPLE, Path("results2/pair_sample_1600.json"))
        self.assertEqual((plan.DEV_BATCH, plan.TEST_BATCH), ("stage_d", "this_run"))
        self.assertEqual((plan.N_DEV_ANSWERS, plan.N_TEST_ANSWERS, plan.N_HIDDEN),
                         (400, 1200, 170))

    def test_the_codebook_is_the_frozen_one(self):
        self.assertEqual(plan.CODEBOOK_DIGEST, "65e1732a08fd32c0")
        self.assertEqual(cb.digest(), plan.CODEBOOK_DIGEST)

    def test_the_development_figures_of_section_0(self):
        d = plan.DEV["stage_d"]
        self.assertEqual(d["n"], 365)
        self.assertEqual(d["codes"]["spec"], 172)
        self.assertEqual((d["Y-a"], d["Y-b"]), ((92, 172), (37, 147)))
        self.assertEqual(d["Y-c"], ((108, 147), (91, 193)))
        self.assertEqual(d["Y-d"], ((95, 138), (99, 140)))
        self.assertEqual(plan.DEV["stage_c"]["n"], 166)

    def test_the_four_lines_of_section_0(self):
        self.assertEqual(plan.Y_A_BAND, (0.45, 0.62))
        self.assertEqual(plan.Y_B_REFUTED_AT_OR_ABOVE, 0.33)
        self.assertEqual(plan.Y_C_MIN_DIFFERENCE, 0.15)
        self.assertEqual(plan.Y_D_MAX_ABS_DIFFERENCE, 0.06)
        self.assertEqual((plan.MIN_ROWS, plan.QUOTES_PER_CODE), (50, 5))

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_WHY.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        self.assertEqual(plan.SCORE_PATH, Path("results_why/score.json"))
        self.assertNotIn(plan.PLAN, (reuse_plan.PLAN, edges_plan.PLAN,
                                     primacy_plan.PLAN))


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text):
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

    def test_one_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-06)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-06)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


# ---------------------------------------------------------------------------
# The codebook, by hand
# ---------------------------------------------------------------------------

class TestTheCodebook(unittest.TestCase):

    def test_specificity_and_counting(self):
        self.assertTrue({"spec", "count"} <= cb.code(
            "La regla B es más específica (4 condiciones) que la A (2 condiciones)."))
        self.assertTrue({"spec", "count"} <= cb.code(
            "Rule B has more conditions and is more specific."))
        c = cb.code("La regla A especifica producto api, más restrictiva que B.")
        self.assertIn("spec", c)
        self.assertNotIn("count", c)
        self.assertIn("spec", cb.code("冲突时采用条件更多的规则A，因为其更具体。"))

    def test_queue_importance_and_precedence(self):
        self.assertEqual(cb.code("Security keyword present; security incidents take "
                                 "precedence over technical issues."), {"queue", "prio"})
        self.assertEqual(cb.code("安全关键字匹配，安全事件优先级高于技术问题。"),
                         {"queue", "prio"})
        self.assertIn("queue", cb.code("Severity 1 requires immediate escalation."))

    def test_match_and_order(self):
        self.assertIn("match", cb.code("El ticket cumple todas las condiciones de la regla A."))
        self.assertIn("order", cb.code("First matching rule A: product mobile."))
        self.assertIn("order", cb.code("Conflicting rules: assigned to T1_GENERAL as default."))
        self.assertEqual(cb.code("Product is billing, so billing specialist."), frozenset())

    def test_labels_are_case_sensitive(self):
        self.assertEqual(cb.labels("La regla A es más específica que la B."), (True, True))
        self.assertEqual(cb.labels("Rule B has three conditions."), (False, True))
        self.assertEqual(cb.labels("prioriza la atención técnica"), (False, False))

    def test_language(self):
        self.assertEqual(cb.language("La regla A es más específica."), "es")
        self.assertEqual(cb.language("Rule A is more specific than rule B."), "en")
        self.assertEqual(cb.language("规则B更紧急"), "zh")

    def test_conditions_are_read_off_the_question(self):
        q = question("severity eq 4 AND product eq api", "customer_tier eq free",
                     "T2_TECHNICAL", "T1_GENERAL")
        a, b = cb.listed_rules(q)
        self.assertEqual(a, [("severity", "eq", "4"), ("product", "eq", "api")])
        self.assertEqual(b, [("customer_tier", "eq", "free")])
        with self.assertRaises(ValueError):
            cb.conditions("TICKET:")

    def test_the_categorical_edge_by_hand(self):
        prod = [("product", "eq", "api")]
        tier = [("customer_tier", "eq", "free")]
        self.assertTrue(cb.categorical_edge(prod, tier))
        self.assertFalse(cb.categorical_edge(tier, prod))
        self.assertTrue(cb.categorical_edge([("severity", "eq", "4")],
                                            [("severity", "gte", "3")]))
        self.assertTrue(cb.categorical_edge([("severity", "eq", "4"), ("channel", "eq", "web")],
                                            [("severity", "lte", "4")]))
        self.assertFalse(cb.categorical_edge([("severity", "gte", "3")],
                                             [("severity", "eq", "4")]))


# ---------------------------------------------------------------------------
# The rows and the statistics, by hand
# ---------------------------------------------------------------------------

class TestTheRows(unittest.TestCase):

    def test_a_learned_row(self):
        truth = {0: {"better_space": "a", "better_corpus": "tie"}}
        r = answer(0, a_first=False, declared="a_beats_b",
                   why="La regla B es más específica.")
        (row,) = R.learned_rows([r], truth, lambda r: "x")
        self.assertEqual(row["named_label"], "B")
        self.assertTrue(row["narrower"])                 # 100 against 900
        self.assertTrue(row["more_conditions"])          # two against one
        self.assertTrue(row["categorical"])              # product, the other none
        self.assertIs(row["right_space"], True)
        self.assertIsNone(row["right_corpus"])
        self.assertEqual(row["queue_pair"], "T1_GENERAL vs T2_TECHNICAL")

    def test_rows_without_an_edge_or_a_why_are_left_out(self):
        rs = [answer(0, declared="none", why="x"), answer(1, why="")]
        self.assertEqual(R.learned_rows(rs, None, lambda r: "x"), [])

    def test_a_hidden_row(self):
        r = {"index": 3, "outcome": "wrong", "winner_shown_as": "A",
             "why": "Rule B is more specific.", "winner_extension": 50,
             "loser_extension": 10, "winner_action": "SECURITY_INCIDENT",
             "loser_action": "T2_TECHNICAL",
             "question": question("has_security_keyword eq True", "product eq api AND "
                                  "severity eq 1", "SECURITY_INCIDENT", "T2_TECHNICAL")}
        (row,) = R.hidden_rows([r])
        self.assertEqual(row["named_label"], "B")       # wrong, winner first: B named
        self.assertTrue(row["narrower"])                 # the loser, 10 against 50
        self.assertIs(row["right_space"], False)

    def test_section_0_by_hand(self):
        spec = "La regla A es más específica."
        rows = (
            [R._row(batch="x", index=i, named_label="A", why=spec,
                    named_conds=[("product", "eq", "api")], other_conds=[("severity", "gte", "3")],
                    ext_named=1, ext_other=2, right_space=True, right_corpus=True,
                    queue_pair="p") for i in range(3)]
            + [R._row(batch="x", index=3, named_label="A", why=spec,
                      named_conds=[("severity", "gte", "3")],
                      other_conds=[("product", "eq", "api"), ("channel", "eq", "web")],
                      ext_named=5, ext_other=2, right_space=False, right_corpus=None,
                      queue_pair="p")]
            + [R._row(batch="x", index=4 + i, named_label="B", why="Product is api.",
                      named_conds=[("severity", "gte", "3")], other_conds=[("product", "eq", "api")],
                      ext_named=9, ext_other=2, right_space=i == 0, right_corpus=None,
                      queue_pair="p") for i in range(2)])
        s = R.section_0(rows)
        self.assertEqual((s["Y-a"]["hits"], s["Y-a"]["n"]), (3, 4))
        self.assertEqual((s["Y-b"]["hits"], s["Y-b"]["n"]), (0, 4))
        self.assertAlmostEqual(s["Y-c"]["difference"], 3 / 4 - 0 / 2)
        self.assertAlmostEqual(s["Y-d"]["difference"], 3 / 4 - 1 / 2)
        self.assertAlmostEqual(s["Y-a"]["standard_error"], math.sqrt(0.75 * 0.25 / 4))


# ---------------------------------------------------------------------------
# The stage, end to end, on a synthetic record
# ---------------------------------------------------------------------------

def synthetic():
    whys = ["La regla A es más específica (3 condiciones) que la B (1 condición).",
            "Security keyword present, overriding general triage.",
            "El ticket cumple todas las condiciones de la regla A.",
            "Rule B is more specific because it names a product.",
            "First matching rule A."]
    answers = []
    for k in range(240):
        batch = "stage_d" if k < 60 else "this_run"
        answers.append(answer(k, a_first=k % 2 == 0,
                              declared="a_beats_b" if k % 3 else "b_beats_a",
                              why=whys[k % len(whys)], batch=batch,
                              ext=(100 + k, 900 - k)))
    oracle = [{"index": k, "rule_a": f"R{k}a", "rule_b": f"R{k}b",
               "better_space": "ab"[k % 2] if k % 5 else "tie",
               "better_corpus": "a" if k % 4 else "neither_ever_right"}
              for k in range(240)]
    hidden = [{"index": i, "outcome": "correct", "winner_shown_as": "A",
               "why": "Security keyword present.", "winner_extension": 5,
               "loser_extension": 9, "winner_action": "SECURITY_INCIDENT",
               "loser_action": "T2_TECHNICAL",
               "question": question("has_security_keyword eq True", "product eq api",
                                    "SECURITY_INCIDENT", "T2_TECHNICAL")}
              for i in range(10)]
    split = {"space": {"unreachable_queue_pairs": ["T1_GENERAL vs T2_TECHNICAL"]}}
    return SimpleNamespace(src={"answers": answers},
                           sample={"oracle": oracle, "split_for_B_d": split},
                           hidden={"answers": hidden})


class TestTheStageOnASyntheticRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = synthetic()
        cls.result = score.score(cls.c)

    def test_it_reads_only_the_held_out_batch(self):
        self.assertEqual(len(self.result["rows"]), 180)
        self.assertEqual(self.result["Y-e"]["census"]["n"], 180)

    def test_the_verdicts_are_there(self):
        self.assertEqual(set(self.result["verdicts"]), {"Y-a", "Y-b", "Y-c", "Y-d"})
        for v in self.result["verdicts"].values():
            self.assertIn(v["verdict"], ("holds", "refuted", "unadjudicable"))

    def test_y_a_by_hand(self):
        # Specificity is argued by whys 0 and 3, every fifth row each: 72 of 180.
        # Rule a is the narrower (100 + k against 900 - k) for k < 400, so the
        # named rule is narrower exactly when the answer named rule a.
        s = self.result["section_0"]["Y-a"]
        rows = [a for a in self.c.src["answers"][60:] if a["why"] in
                ("La regla A es más específica (3 condiciones) que la B (1 condición).",
                 "Rule B is more specific because it names a product.")]
        self.assertEqual(s["n"], len(rows))
        self.assertEqual(s["hits"], sum(1 for a in rows if a["declared"] == "a_beats_b"))

    def test_the_readings_are_there(self):
        e = self.result["Y-e"]
        self.assertEqual(set(e), {"census", "base_rates", "by_code", "by_b_d_side_space",
                                  "labels_against_the_named_rule", "quotes",
                                  "development"})
        self.assertEqual(len(e["quotes"]["spec"]), plan.QUOTES_PER_CODE)
        self.assertEqual(set(e["development"]), {"stage_d", "stage_c"})
        self.assertEqual(sum(e["labels_against_the_named_rule"].values()), 180)

    def test_the_record_rounds_and_sorts_when_written(self):
        self.assertEqual(score.rounded({"x": [1 / 3], "y": frozenset({"b", "a"})}),
                         {"x": [0.333333], "y": ["a", "b"]})


# ---------------------------------------------------------------------------
# The blocking checks on the real records
# ---------------------------------------------------------------------------

class TestTheBlockingChecksOnTheRecords(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.src, cls.stage_d = gates.load(plan.SOURCE), gates.load(plan.STAGE_D)
        cls.hidden, cls.sample = gates.load(plan.HIDDEN), gates.load(plan.SAMPLE)
        cls.direction = gates.load(plan.DIRECTION)

    def test_y_g1_and_y_g2_pass(self):
        self.assertTrue(gates.gate_yg1(self.src, self.stage_d, self.sample,
                                       self.direction, suite=False)["passes"])
        self.assertTrue(gates.gate_yg2(self.src, self.hidden)["passes"])

    def test_y_g3_reproduces_the_development_figures(self):
        self.assertTrue(gates.gate_yg3(self.src, self.hidden, self.sample)["passes"])

    def test_y_g3_catches_a_changed_codebook_or_figure(self):
        with mock.patch.object(plan, "CODEBOOK_DIGEST", "0" * 16):
            self.assertFalse(gates.gate_yg3(self.src, self.hidden, self.sample)["passes"])
        dev = copy.deepcopy(plan.DEV)
        dev["stage_d"]["codes"]["spec"] += 1
        with mock.patch.object(plan, "DEV", dev):
            self.assertFalse(gates.gate_yg3(self.src, self.hidden, self.sample)["passes"])

    def test_y_g1_catches_a_changed_development_why(self):
        src = copy.deepcopy(self.src)
        r = next(r for r in src["answers"] if r["answer_from"] == plan.DEV_BATCH
                 and r.get("why"))
        r["why"] += " (edited)"
        self.assertTrue(gates.stage_d_is_the_development_batch(src, self.stage_d))

    def test_the_checks_hand_the_codebook_only_development_sentences(self):
        dev_whys = ({r["why"] for r in self.stage_d["answers"]}
                    | {r["why"] for r in self.hidden["answers"]})
        seen = []
        real = cb.code

        def watch(why):
            seen.append(why)
            return real(why)
        with mock.patch.object(cb, "code", side_effect=watch):
            gates.gate_yg1(self.src, self.stage_d, self.sample, self.direction,
                           suite=False)
            gates.gate_yg2(self.src, self.hidden)
            gates.gate_yg3(self.src, self.hidden, self.sample)
        self.assertTrue(seen)
        self.assertTrue(set(seen) <= dev_whys)

    def test_the_checks_never_reach_the_stage(self):
        tree = ast.parse((REPO / "why/gates.py").read_text())
        names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        names |= {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        names |= {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                  for a in n.names}
        for forbidden in ("score", "held_out_rows"):
            self.assertNotIn(forbidden, names)


# ---------------------------------------------------------------------------
# The verdicts at their edges
# ---------------------------------------------------------------------------

def share(v, se=0.02, n=100):
    return {"share": v, "standard_error": se, "n": n, "hits": 0}


def diff(v, se=0.02, n=(100, 100)):
    return {"difference": v, "standard_error": se,
            "first": {"n": n[0]}, "second": {"n": n[1]}}


class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def test_y_a_is_a_band(self):
        self.assertEqual(score.verdict_y_a(share(0.45))["verdict"], "holds")
        self.assertEqual(score.verdict_y_a(share(0.62))["verdict"], "holds")
        self.assertEqual(score.verdict_y_a(share(0.4499))["verdict"], "refuted")
        self.assertEqual(score.verdict_y_a(share(0.6201))["verdict"], "refuted")
        self.assertEqual(score.verdict_y_a(share(0.5, n=49))["verdict"], "unadjudicable")
        self.assertTrue(score.verdict_y_a(share(0.46))["thin"])
        self.assertFalse(score.verdict_y_a(share(0.53))["thin"])

    def test_y_b(self):
        self.assertEqual(score.verdict_y_b(share(0.3299))["verdict"], "holds")
        self.assertEqual(score.verdict_y_b(share(0.33))["verdict"], "refuted")

    def test_y_c(self):
        self.assertEqual(score.verdict_y_c(diff(0.15))["verdict"], "holds")
        self.assertEqual(score.verdict_y_c(diff(0.1499))["verdict"], "refuted")
        self.assertEqual(score.verdict_y_c(diff(0.3, n=(49, 100)))["verdict"],
                         "unadjudicable")

    def test_y_d(self):
        self.assertEqual(score.verdict_y_d(diff(0.0599))["verdict"], "holds")
        self.assertEqual(score.verdict_y_d(diff(-0.0599))["verdict"], "holds")
        self.assertEqual(score.verdict_y_d(diff(-0.06))["verdict"], "refuted")
        self.assertTrue(score.verdict_y_d(diff(0.05))["thin"])


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
