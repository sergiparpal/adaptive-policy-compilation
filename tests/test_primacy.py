"""
PLAN_PRIMACY.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §8 and the two band lines of §0, so that moving one after
    a figure exists is visible in a diff.
  * The gate: it reads every signature line, and the writer exits on an
    unsigned plan before it measures, builds or writes anything.
  * The definitions of `primacy/rows.py`, on rows small enough to check by
    hand: the slot effect and its symmetry on one queue pair, the favoured
    queue and the rows counted apart, and the share with no edge by the
    favoured rule's slot.
  * The whole stage, end to end, on a synthetic record whose verdicts are
    computed by hand. The stage cannot be run on the real records before §0 is
    signed, so this is where it is run first.
  * The blocking checks on the real records. They reproduce figures already
    published, catch a tampered deal and a tampered row, and read no slot split
    of §0.
  * That `primacy/gates.py`, which the dry run runs, never calls the
    statistics of §0's rows.
  * Each verdict at its edge.

**No test here writes under `results*/`, and none computes a figure of §0 on
the real records.** The rows the statistics are checked on are synthetic.
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

from primacy import gates, plan, score
from primacy import rows as R
from reuse import plan as reuse_plan
from edges import plan as edges_plan

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}

SS, T2, T1, SEC = ("SELF_SERVICE_DEFLECT", "T2_TECHNICAL", "T1_GENERAL",
                   "SECURITY_INCIDENT")


def row(k, a, b, act_a, act_b, first_is_a, declared, *, batch="this_run",
        ext=(10, 5), attempts=1, parse_failed=False):
    """One answer as `rung2/pair_judgement.py` records it, without a ticket."""
    first, second = (a, b) if first_is_a else (b, a)
    answer = {"a_beats_b": act_a, "b_beats_a": act_b}.get(declared)
    act = {a: act_a, b: act_b}
    return {"index": k, "rule_a": a, "rule_b": b, "action_a": act_a, "action_b": act_b,
            "a_shown_as": "A" if first_is_a else "B",
            "shown_as": {"A": first, "B": second},
            "declared": declared, "answer": answer, "raw_answer": answer,
            "parse_failed": parse_failed, "attempts": attempts, "answer_from": batch,
            "extension_a": ext[0], "extension_b": ext[1], "a_is_broader": ext[0] > ext[1],
            "question": ("LAS DOS REGLAS QUE CASAN EL TICKET:\n"
                         f"  A: SI x eq 1 ENTONCES {act[first]}\n"
                         f"  B: SI y eq 2 ENTONCES {act[second]}\n\nTICKET:\n{{}}")}


def synthetic():
    """A record small enough to score by hand.

    On SELF_SERVICE_DEFLECT vs T2_TECHNICAL, 50 declared answers with the
    self-service rule listed first, 35 of them naming it, and 50 with it listed
    second, 20 naming it: L-a's d is 0.70 - 0.40 = 0.30. Six rows on the same
    pair have no edge, four with the self-service rule listed second.
    On SECURITY_INCIDENT vs T1_GENERAL, 40 answers, all naming security, half
    with it listed first. Self-service is the favoured queue of its pair (55
    against 45), so for L-b the favoured rule is listed second on 54 + 20 rows,
    4 of them with no edge, and first on 52 + 20, 2 with no edge:
    4/74 - 2/72.
    """
    rows, k = [], 0

    def add(a, b, act_a, act_b, first_is_a, declared, **kw):
        nonlocal k
        rows.append(row(k, a, b, act_a, act_b, first_is_a, declared, **kw))
        k += 1

    for i in range(50):        # self-service listed first
        add(f"S{i}", f"T{i}", SS, T2, True, "a_beats_b" if i < 35 else "b_beats_a")
    for i in range(50, 100):   # self-service listed second
        add(f"S{i}", f"T{i}", SS, T2, False, "a_beats_b" if i < 70 else "b_beats_a",
            batch="stage_d")
    for i in range(100, 106):  # no edge: two with self-service first, four second
        add(f"S{i}", f"T{i}", SS, T2, i < 102, "none", parse_failed=i % 2 == 0)
    for i in range(106, 146):  # security always named
        add(f"X{i}", f"Y{i}", SEC, T1, i % 2 == 0, "a_beats_b", ext=(3, 9),
            attempts=2 if i < 110 else 1)
    oracle = [{"index": r["index"], "rule_a": r["rule_a"], "rule_b": r["rule_b"],
               "better_space": ("a" if r["index"] % 3 == 0 else
                                "b" if r["index"] % 3 == 1 else "tie"),
               "better_corpus": "a" if r["index"] % 2 == 0 else "neither_ever_right"}
              for r in rows]
    split = {s: {"unreachable_queue_pairs": [f"{SS} vs {T2}"]} for s in ("space", "corpus")}
    hidden = [{"outcome": o, "winner_shown_as": s}
              for o, s in (("correct", "A"), ("correct", "A"), ("wrong", "A"),
                           ("correct", "B"), ("wrong", "B"), ("neither", "B"))]
    return SimpleNamespace(src={"answers": rows},
                           sample={"oracle": oracle, "split_for_B_d": split},
                           hidden={"answers": hidden})


# ---------------------------------------------------------------------------
# The constants and the gate
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheSignedOnes(unittest.TestCase):

    def test_the_inputs_of_section_8(self):
        self.assertEqual(plan.SOURCE, Path("results2/pair_judgement_1600.json"))
        self.assertEqual(plan.STAGE_D, Path("results2/pair_judgement_learned.json"))
        self.assertEqual(plan.HIDDEN, Path("results2/pair_judgement_hidden.json"))
        self.assertEqual(plan.SAMPLE, Path("results2/pair_sample_1600.json"))
        self.assertEqual(plan.DIRECTION, Path("results3/edge_direction_1600.json"))
        self.assertEqual(plan.ASYMMETRY, Path("results3/answer_asymmetry.json"))
        self.assertEqual((plan.N_ROWS, plan.N_REUSED, plan.N_FRESH, plan.N_HIDDEN),
                         (1600, 400, 1200, 170))
        self.assertEqual(plan.POSITION_SEED, 17)

    def test_l_a_of_section_0(self):
        self.assertEqual(plan.L_A_QUEUE_PAIR, (SS, T2))
        self.assertEqual(plan.L_A_LINE, 0.20)
        self.assertEqual(plan.L_A_MIN_SIDE, 20)
        self.assertEqual((plan.L_A_SELECT_MIN_ROWS, plan.L_A_SELECT_BELOW), (30, 0.60))

    def test_l_b_of_section_0_and_the_readings(self):
        self.assertEqual(plan.L_B_LINE, 0.025)
        self.assertEqual(plan.READING_MIN_ROWS, 30)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_PRIMACY.md"))
        self.assertEqual(plan.MIN_SIGNATURES, 1)
        self.assertEqual(plan.SCORE_PATH, Path("results_primacy/score.json"))
        self.assertNotIn(plan.PLAN, (reuse_plan.PLAN, edges_plan.PLAN))


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
# The definitions, by hand
# ---------------------------------------------------------------------------

class TestTheDefinitions(unittest.TestCase):

    def test_what_a_row_is(self):
        r = row(0, "a", "b", SS, T2, False, "b_beats_a")
        self.assertEqual((R.first_rule(r), R.second_rule(r)), ("b", "a"))
        self.assertEqual(R.winner(r), "b")
        self.assertEqual(R.queue_pair(r), (SS, T2))
        self.assertEqual(R.pair_key(R.queue_pair(r)), f"{SS} vs {T2}")
        self.assertIsNone(R.winner(row(1, "a", "b", SS, T2, True, "none")))
        self.assertEqual(R.rule_with_action(r, T2), "b")
        self.assertIsNone(R.rule_with_action(r, T1))

    def test_the_slot_effect_by_hand(self):
        rs = ([row(i, f"s{i}", f"t{i}", SS, T2, True, "a_beats_b") for i in range(3)]
              + [row(3, "s3", "t3", SS, T2, True, "b_beats_a")]
              + [row(4, "s4", "t4", SS, T2, False, "a_beats_b")]
              + [row(i, f"s{i}", f"t{i}", SS, T2, False, "b_beats_a") for i in range(5, 8)]
              + [row(8, "s8", "t8", SS, T2, False, "none")])
        e = R.slot_effect(rs, lambda r: R.rule_with_action(r, SS))
        self.assertEqual((e["hits1"], e["n1"], e["hits2"], e["n2"]), (3, 4, 1, 4))
        self.assertAlmostEqual(e["difference"], 0.5)
        self.assertAlmostEqual(e["standard_error"],
                               math.sqrt(0.75 * 0.25 / 4 + 0.25 * 0.75 / 4))

    def test_on_one_queue_pair_the_reference_does_not_matter(self):
        c = synthetic()
        on = [r for r in c.src["answers"] if R.queue_pair(r) == (SS, T2)]
        by_ss = R.slot_effect(on, lambda r: R.rule_with_action(r, SS))
        by_t2 = R.slot_effect(on, lambda r: R.rule_with_action(r, T2))
        self.assertAlmostEqual(by_ss["difference"], by_t2["difference"])
        self.assertAlmostEqual(by_ss["standard_error"], by_t2["standard_error"])

    def test_rows_without_a_reference_are_left_out(self):
        rs = [row(0, "a", "b", SS, T2, True, "a_beats_b"),
              row(1, "c", "d", SS, T2, False, "a_beats_b")]
        e = R.slot_effect(rs, lambda r: None if r["index"] == 1 else r["rule_a"])
        self.assertEqual((e["n1"], e["n2"]), (1, 0))
        self.assertIsNone(e["difference"])

    def test_the_favoured_queue_and_a_tie(self):
        rs = [row(0, "a", "b", SS, T2, True, "a_beats_b"),
              row(1, "c", "d", SS, T2, True, "a_beats_b"),
              row(2, "e", "f", SS, T2, True, "b_beats_a"),
              row(3, "g", "h", SEC, T1, True, "a_beats_b"),
              row(4, "i", "j", SEC, T1, True, "b_beats_a")]
        maj = R.majority(rs)
        self.assertEqual(maj, {(SS, T2): SS, (SEC, T1): None})
        self.assertEqual(R.favoured_rule(rs[2], maj), "e")
        self.assertIsNone(R.favoured_rule(rs[3], maj))
        self.assertEqual(R.per_queue_pair(rs), {f"{SS} vs {T2}": {SS: 2, T2: 1},
                                                f"{SEC} vs {T1}": {SEC: 1, T1: 1}})

    def test_no_edge_by_the_favoured_slot_by_hand(self):
        c = synthetic()
        ans = c.src["answers"]
        out = R.none_by_favoured_slot(ans, R.majority(ans))
        self.assertEqual((out["hits1"], out["n1"], out["hits2"], out["n2"]),
                         (4, 74, 2, 72))
        self.assertAlmostEqual(out["difference"], 4 / 74 - 2 / 72)
        self.assertEqual(out["counted_apart"], 0)
        self.assertEqual(out["parse_failures"], {"favoured_second": 2, "favoured_first": 1})

    def test_a_row_whose_queue_pair_has_no_favourite_is_counted_apart(self):
        rs = [row(0, "a", "b", SEC, T1, True, "a_beats_b"),
              row(1, "c", "d", SEC, T1, True, "b_beats_a"),
              row(2, "e", "f", SS, T2, True, "none")]
        out = R.none_by_favoured_slot(rs, R.majority(rs))
        self.assertEqual(out["counted_apart"], 3)
        self.assertIsNone(out["difference"])

    def test_the_first_listed_rate_by_hand(self):
        c = synthetic()
        out = R.first_listed_rate(c.src["answers"])
        # 35 + 30 on the pair, and security named whenever listed first: 20.
        self.assertEqual((out["hits"], out["n"]), (85, 140))
        self.assertAlmostEqual(out["twice_minus_one"], 2 * 85 / 140 - 1)
        self.assertAlmostEqual(out["standard_error"], math.sqrt(0.25 / 140))


# ---------------------------------------------------------------------------
# The stage, end to end, on the synthetic record
# ---------------------------------------------------------------------------

class TestTheStageOnASyntheticRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = synthetic()
        cls.result = score.score(cls.c)

    def test_l_a_is_computed_by_hand(self):
        a = self.result["L-a"]
        self.assertEqual((a["hits1"], a["n1"], a["hits2"], a["n2"]), (35, 50, 20, 50))
        self.assertAlmostEqual(a["difference"], 0.30)
        self.assertEqual(a["queue_pair"], f"{SS} vs {T2}")
        v = self.result["verdicts"]["L-a"]
        # |0.30 - 0.20| = 0.10 against a standard error of 0.0949: not thin.
        self.assertEqual((v["verdict"], v["thin"]), ("holds", False))

    def test_l_b_is_computed_by_hand(self):
        b = self.result["L-b"]
        self.assertAlmostEqual(b["difference"], 4 / 74 - 2 / 72)
        self.assertEqual(self.result["verdicts"]["L-b"]["verdict"], "refuted")

    def test_the_readings_are_there_and_add_up(self):
        lc = self.result["L-c"]
        self.assertEqual(set(lc), {"overall", "by_b_d_side", "by_batch", "by_queue_pair",
                                   "by_breadth_of_the_rule_listed_first", "stage_c",
                                   "retries_by_favoured_slot",
                                   "l_a_queue_pair_against_the_truth"})
        self.assertEqual(lc["overall"]["first_listed"]["hits"], 85)
        self.assertEqual(set(lc["by_queue_pair"]), {f"{SS} vs {T2}", f"{SEC} vs {T1}"})
        self.assertEqual(lc["by_batch"]["stage_d"]["first_listed"]["n"], 50)
        sc = lc["stage_c"]
        # Named first: correct with the winner first (2), wrong with it second (1).
        self.assertEqual((sc["first_listed"]["hits"], sc["first_listed"]["n"]), (3, 5))
        e = sc["slot_effect_winner_reference"]
        self.assertEqual((e["hits1"], e["n1"], e["hits2"], e["n2"]), (2, 3, 1, 2))
        r = lc["retries_by_favoured_slot"]
        self.assertEqual(r["hits1"] + r["hits2"], 4)
        b = lc["by_breadth_of_the_rule_listed_first"]
        self.assertEqual(b["equal_extensions_counted_apart"], 0)
        side = lc["by_b_d_side"]["space"]
        self.assertEqual(side["reachable"]["first_listed"]["n"]
                         + side["unreachable"]["first_listed"]["n"]
                         + side["no_strict_better"]["first_listed"]["n"], 140)

    def test_the_record_rounds_only_when_it_is_written(self):
        self.assertEqual(score.rounded({"x": [1 / 3, 2], "y": "z"}),
                         {"x": [0.333333, 2], "y": "z"})


# ---------------------------------------------------------------------------
# The blocking checks on the real records
# ---------------------------------------------------------------------------

class TestTheBlockingChecksOnTheRecords(unittest.TestCase):
    """They reproduce what the records publish and read no slot split of §0."""

    @classmethod
    def setUpClass(cls):
        cls.src, cls.stage_d = gates.load(plan.SOURCE), gates.load(plan.STAGE_D)
        cls.hidden, cls.sample = gates.load(plan.HIDDEN), gates.load(plan.SAMPLE)
        cls.direction, cls.asymmetry = gates.load(plan.DIRECTION), gates.load(plan.ASYMMETRY)

    def test_l_g1_reproduces_what_is_published(self):
        g = gates.gate_lg1(self.src, self.stage_d, self.hidden, self.sample,
                           self.direction, self.asymmetry, suite=False)
        self.assertTrue(g["passes"], g)

    def test_l_g2_the_slots_are_the_seeded_deal(self):
        self.assertTrue(gates.gate_lg2(self.src, self.stage_d, self.hidden)["passes"])

    def test_l_g2_catches_a_tampered_deal(self):
        src = copy.deepcopy(self.src)
        r = next(r for r in src["answers"] if r["answer_from"] == "this_run")
        r["a_shown_as"] = "B" if r["a_shown_as"] == "A" else "A"
        self.assertFalse(gates.gate_lg2(src, self.stage_d, self.hidden)["passes"])

    def test_l_g3_the_definitions_hold(self):
        self.assertTrue(gates.gate_lg3(self.src)["passes"])

    def test_l_g3_catches_a_tampered_row(self):
        src = copy.deepcopy(self.src)
        r = src["answers"][7]
        r["shown_as"] = {"A": r["shown_as"]["B"], "B": r["shown_as"]["A"]}
        self.assertFalse(gates.gate_lg3(src)["passes"])

    def test_the_dry_run_cannot_compute_a_row_of_section_0(self):
        """`gates.py` is what the dry run runs. It must not reach the statistics
        of §0's rows, by any name."""
        tree = ast.parse((REPO / "primacy/gates.py").read_text())
        names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        names |= {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                    for a in n.names}
        for forbidden in ("slot_effect", "none_by_favoured_slot", "score",
                          "verdict_l_a", "verdict_l_b"):
            self.assertNotIn(forbidden, names | imported)


# ---------------------------------------------------------------------------
# The verdicts at their edges
# ---------------------------------------------------------------------------

class TestTheVerdictsAtTheirEdges(unittest.TestCase):

    def test_l_a(self):
        self.assertEqual(score.verdict_l_a(0.20, 0.05, 20, 20)["verdict"], "holds")
        self.assertEqual(score.verdict_l_a(0.1999, 0.05, 20, 20)["verdict"], "refuted")
        self.assertEqual(score.verdict_l_a(0.50, 0.05, 19, 80)["verdict"], "unadjudicable")
        self.assertEqual(score.verdict_l_a(None, None, 0, 0)["verdict"], "unadjudicable")
        self.assertTrue(score.verdict_l_a(0.24, 0.05, 40, 40)["thin"])
        self.assertFalse(score.verdict_l_a(0.26, 0.05, 40, 40)["thin"])

    def test_l_b(self):
        self.assertEqual(score.verdict_l_b(0.0249, 0.01)["verdict"], "holds")
        self.assertEqual(score.verdict_l_b(-0.0249, 0.01)["verdict"], "holds")
        self.assertEqual(score.verdict_l_b(0.025, 0.01)["verdict"], "refuted")
        self.assertEqual(score.verdict_l_b(-0.025, 0.01)["verdict"], "refuted")
        self.assertEqual(score.verdict_l_b(None, None)["verdict"], "unadjudicable")
        self.assertTrue(score.verdict_l_b(0.02, 0.01)["thin"])
        self.assertFalse(score.verdict_l_b(0.0, 0.01)["thin"])


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
