"""
`apply/providers.py`, the POST-RUN reading of each `PLAN_APPLY.md` row within one
provider's answers.

WHAT IS PINNED HERE, AND WHY.
  * The names it reads by: the floor, which is the plan's own for `X-d`, the
    reference provider and the two it is set against, what each row reads, the
    expectation's lines, and its record's path.
  * The provider of an answer as its last attempt's, which is what a retried
    answer was parsed from.
  * An arm cut to one provider's answers as `hits` reads it: two kept, one read
    twice so that `hits` gives it alone, none dropping the decision, and every
    provider keeping the pair.
  * Each row's cut on units built by hand: `X-a` needs both screen answers and
    the loop's, `X-d` keeps Stage C's selector whoever gave it, and every
    provider gives the unit back. Reading B's filter takes `X-d`'s `t₁` too.
  * A cut cell read through `apply/score.py`'s `adjudicate`, which a provider's
    two answers and one answer read twice reach alike.
  * The asks two answers at a time: who is right more often, on the asks one
    provider answered in one pass and another in the other, and agreement by
    whether one provider gave both.
  * Each clause of the expectation at its edge.
  * The writer refusing unsigned before it reads a record, and an argument
    printing the docstring.

**No figure of the reading is pinned here**, and no test reads a record.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from apply import plan, prompts
from apply import providers as PR
from apply import score

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
Y, W, P = "T1_GENERAL", "BILLING_SPECIALIST", "T2_TECHNICAL"
B, G, R = "Baidu", "GMICloud", "Relace"


def unit(level=3, run=1, ticket=1, y=Y, loop=Y, p=P, s=(Y, Y), t=(Y, Y), u=(Y, Y),
         uid=None) -> score.Unit:
    return score.Unit(id=uid or f"L{level}r{run}:{ticket}", level=level, run=run,
                      ticket=ticket, kind=prompts.COVERAGE, y=y, loop=loop, p=p,
                      first=p, shown=(p,), s=tuple(s), t=tuple(t), u=tuple(u))


def who(s=(B, B), t=(B, B), u=(B, B), loop=B) -> PR.Who:
    return PR.Who(s=tuple(s), t=tuple(t), u=tuple(u), loop=loop)


def spec(row: str) -> score.Spec:
    return next(x for x in score.SPECS if x.id == row)


class TestTheNames(unittest.TestCase):

    def test_the_names_it_reads_by(self):
        self.assertEqual(PR.FLOOR, plan.MIN_PULL_POPULATION)
        self.assertEqual(PR.FLOOR, 100)
        self.assertIsNone(PR.EVERY)
        self.assertEqual((PR.REFERENCE, PR.AGAINST), (B, (G, R)))
        self.assertEqual(PR.record_path(), Path("results_apply/providers.json"))
        self.assertEqual(set(PR.READS), {x.id for x in score.SPECS})
        self.assertEqual(PR.READS["X-a"], ("s", "loop"))
        self.assertEqual(PR.READS["X-f"], ("t", "u"))

    def test_the_expectations_lines(self):
        self.assertEqual((PR.NEAR, PR.MOVE, PR.ALIKE),
                         (Fraction(1, 20), Fraction(3, 100), Fraction(1, 20)))


class TestWhoAnswered(unittest.TestCase):

    def test_the_provider_of_an_answer_is_its_last_attempts(self):
        row = {"call_attempts": [{"provider": G, "finish_reason": "length"},
                                 {"provider": R, "finish_reason": "stop"}]}
        self.assertEqual(PR.provider_of(row), R)
        self.assertIsNone(PR.provider_of({"call_attempts": []}))
        self.assertIsNone(PR.provider_of({}))

    def test_the_passes_by_ask(self):
        recs = {"pass1": {"rows": [{"id": "s:x", "call_attempts": [{"provider": B}]}]},
                "pass2": {"rows": [{"id": "s:x", "call_attempts": [{"provider": G}]}]}}
        self.assertEqual(PR.served(recs), {(1, "s:x"): B, (2, "s:x"): G})


class TestTheCut(unittest.TestCase):

    def test_an_arm_cut_to_one_providers_answers(self):
        self.assertEqual(PR.own((Y, W), (B, B), B), (Y, W))
        self.assertEqual(PR.own((Y, W), (G, B), B), (W, W))
        self.assertEqual(PR.own((Y, W), (B, G), B), (Y, Y))
        self.assertIsNone(PR.own((Y, W), (G, R), B))
        self.assertEqual(PR.own((Y, W), (G, R), PR.EVERY), (Y, W))

    def test_one_answer_read_twice_is_that_answer_alone(self):
        """`hits` halves a pair: an answer read twice counts whole."""
        self.assertEqual(score.hits(PR.own((Y, W), (B, G), B), Y), 1)
        self.assertEqual(score.hits(PR.own((Y, W), (G, B), B), Y), 0)
        self.assertEqual(score.hits(PR.own((Y, W), (B, B), B), Y), Fraction(1, 2))

    def test_every_provider_gives_the_unit_back(self):
        u = unit(s=(Y, W))
        for row in PR.READS:
            self.assertIs(PR.on_answers(row, u, None, PR.EVERY), u)

    def test_the_rows_that_compare_two_arms(self):
        u = unit(s=(Y, W), t=(W, Y), u=(P, Y))
        cut = PR.on_answers("X-b", u, who(s=(B, G), t=(G, B)), B)
        self.assertEqual((cut.s, cut.t, cut.u), ((Y, Y), (Y, Y), (P, Y)))
        cut = PR.on_answers("X-f", u, who(t=(B, G), u=(G, B)), B)
        self.assertEqual((cut.s, cut.t, cut.u), ((Y, W), (W, W), (Y, Y)))
        self.assertIsNone(PR.on_answers("X-e", u, who(s=(G, G)), B))
        self.assertIsNone(PR.on_answers("X-f", u, who(u=(G, R)), B))

    def test_x_d_keeps_its_selector_whoever_gave_it(self):
        u = unit(s=(P, W), t=(W, Y))
        cut = PR.on_answers("X-d", u, who(s=(G, B), t=(G, B)), B)
        self.assertEqual((cut.s, cut.t), ((W, W), (W, Y)))
        self.assertIsNone(PR.on_answers("X-d", u, who(t=(B, G)), B))
        self.assertIsNone(PR.on_answers("X-d", u, who(s=(G, G)), B))

    def test_x_a_needs_both_screen_answers_and_the_loops(self):
        u = unit(s=(Y, W))
        self.assertIs(PR.on_answers("X-a", u, who(), B), u)
        self.assertIsNone(PR.on_answers("X-a", u, who(s=(B, G)), B))
        self.assertIsNone(PR.on_answers("X-a", u, who(loop=G), B))

    def test_reading_b_takes_every_answer_x_d_s_selector_included(self):
        self.assertTrue(PR.whole("X-d", who(u=(G, G), loop=G), B))
        self.assertFalse(PR.whole("X-d", who(t=(G, B)), B))
        self.assertFalse(PR.whole("X-b", who(s=(B, G)), B))
        self.assertTrue(PR.whole("X-f", who(s=(G, G), loop=G), B))
        self.assertFalse(PR.whole("X-a", who(loop=G), B))

    def test_usable_is_stage_cs_population(self):
        units = [unit(level=3), unit(level=3, t=(Y, None), uid="L3r1:9"), unit(level=2)]
        self.assertEqual([u.id for u in PR.usable(spec("X-b"), units)], ["L3r1:1"])


class TestACell(unittest.TestCase):

    def test_a_cell_is_adjudicate_with_its_verdict_renamed(self):
        us = [unit(ticket=i, s=(W, W), t=(Y, Y)) for i in range(4)]
        c = PR.cell(spec("X-b"), us)
        self.assertNotIn("verdict", c)
        self.assertIs(c["meets_the_line"], True)
        self.assertEqual(PR.value(c), 1)
        self.assertIs(PR.cell(spec("X-b"), [])["meets_the_line"], None)

    def test_two_answers_and_one_read_twice_reach_alike(self):
        """A decision whose provider gave both screen answers, and one whose
        provider gave one, enter the mean as the provider's share right."""
        a = PR.on_answers("X-b", unit(ticket=1, s=(Y, W), t=(Y, Y)), who(), B)
        b = PR.on_answers("X-b", unit(ticket=2, s=(Y, W), t=(Y, Y)), who(s=(G, B)), B)
        self.assertEqual(PR.value(PR.cell(spec("X-b"), [a, b])),
                         ((1 - Fraction(1, 2)) + (1 - 0)) / 2)


def asked(by, a=(Y, Y), y=Y, arm="screen", ticket=1) -> PR.Asked:
    return PR.Asked(id=f"x:{ticket}", arm=arm, level=3, ticket=ticket, y=y,
                    a=tuple(a), by=tuple(by))


class TestTheAsks(unittest.TestCase):

    def test_who_is_right_more_often_on_one_ask(self):
        qs = [asked((B, G), a=(Y, W), ticket=1), asked((G, B), a=(Y, W), ticket=2),
              asked((B, B), a=(Y, W), ticket=3), asked((B, R), a=(W, Y), ticket=4)]
        got = PR.against(qs, B, lambda p: p == G)
        self.assertEqual(got["asks"], 2)
        self.assertEqual(Fraction(got["difference"]["fraction"]), 0)
        self.assertEqual((got["right"]["one"]["value"], got["right"]["other"]["value"]),
                         (0.5, 0.5))
        every = PR.against(qs, B, lambda p: p != B)
        self.assertEqual((every["asks"], Fraction(every["difference"]["fraction"])),
                         (3, Fraction(-1, 3)))

    def test_agreement_by_whether_one_provider_gave_both(self):
        qs = [asked((B, B), a=(Y, Y)), asked((B, B), a=(Y, W)), asked((G, G), a=(W, W)),
              asked((B, G), a=(Y, W)), asked((B, G), a=(Y, W), arm="ticket")]
        got = PR.agreement(qs)["screen"]
        self.assertEqual((got["one_provider"]["asks"],
                          Fraction(got["one_provider"]["agree"]["fraction"])),
                         (3, Fraction(2, 3)))
        self.assertEqual(Fraction(got["two_providers"]["agree"]["fraction"]), 0)
        self.assertEqual(got["both_reference"]["asks"], 2)
        self.assertEqual(got["reference_and_another"]["asks"], 1)


def frac(x: Fraction) -> dict:
    return {"fraction": f"{x.numerator}/{x.denominator}", "value": float(x)}


def as_expected() -> tuple[dict, dict, dict, dict]:
    """Cells on which every clause holds, each a step inside its line."""
    stage_c = {"X-a": Fraction(-1, 100), "X-b": Fraction(11, 100), "X-c": Fraction(-18, 100),
               "X-d": Fraction(19, 100), "X-e": Fraction(2, 100), "X-f": Fraction(23, 100)}
    A = {}
    for row, v in stage_c.items():
        own_ = {"value": frac(v), "read": 200}
        if row == "X-c":
            own_["share"] = frac(Fraction(27, 100))
        A[row] = {B: {"above_floor": True, "own": own_,
                      "every_answer": {"value": frac(v), "read": 200}}}
    Bc = {row: {B: {"value": frac(v), "read": 90}} for row, v in stage_c.items()}
    acc = {k: {"asks": 150, "difference": frac(Fraction(1, 100))}
           for k in (G, R, "every_other")}
    agree = {arm: {"one_provider": {"agree": frac(Fraction(9, 10))},
                   "two_providers": {"agree": frac(Fraction(8, 10))}}
             for arm in ("screen", "ticket")}
    return A, Bc, {"accuracy": acc, "agreement": agree}, stage_c


def holds(A, Bc, C, stage_c) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in PR.read_expectation(A, Bc, C, stage_c)}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_holds_inside_its_lines(self):
        got = holds(*as_expected())
        self.assertEqual(list(got), ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "B1",
                                     "C1", "C2"])
        self.assertTrue(all(got.values()))

    def set_own(self, A, row, v):
        A[row][B]["own"]["value"] = frac(v)

    def test_a1_and_a4_at_their_distance_from_stage_c(self):
        for row, clause in (("X-b", "A1"), ("X-e", "A4")):
            A, Bc, C, sc = as_expected()
            self.set_own(A, row, sc[row] + PR.NEAR)
            A[row][B]["every_answer"]["value"] = frac(sc[row] + PR.NEAR)
            self.assertTrue(holds(A, Bc, C, sc)[clause])
            self.set_own(A, row, sc[row] - PR.NEAR - Fraction(1, 10_000))
            self.assertFalse(holds(A, Bc, C, sc)[clause])

    def test_a1_needs_the_row_above_its_line(self):
        A, Bc, C, sc = as_expected()
        sc["X-b"] = Fraction(1, 100)
        self.set_own(A, "X-b", Fraction(0))
        self.assertFalse(holds(A, Bc, C, sc)["A1"])

    def test_a_cell_below_the_floor_is_not_read(self):
        A, Bc, C, sc = as_expected()
        A["X-f"][B]["above_floor"] = False
        self.assertFalse(holds(A, Bc, C, sc)["A5"])

    def test_a3_needs_a_hundred_decisions(self):
        A, Bc, C, sc = as_expected()
        A["X-d"][B]["own"]["read"] = 99
        self.assertFalse(holds(A, Bc, C, sc)["A3"])
        A["X-d"][B]["own"]["read"] = 100
        self.set_own(A, "X-d", plan.X_D_LINE)
        self.assertTrue(holds(A, Bc, C, sc)["A3"])

    def test_a2_a5_a6_at_the_rows_lines(self):
        A, Bc, C, sc = as_expected()
        self.set_own(A, "X-c", Fraction(0))
        self.set_own(A, "X-f", plan.X_F_LINE)
        self.set_own(A, "X-a", plan.X_A_MAX_GAP)
        got = holds(A, Bc, C, sc)
        self.assertEqual((got["A2"], got["A5"], got["A6"]), (False, True, True))

    def test_a7_at_its_move(self):
        A, Bc, C, sc = as_expected()
        A["X-d"][B]["every_answer"]["value"] = frac(sc["X-d"] + PR.MOVE)
        self.assertTrue(holds(A, Bc, C, sc)["A7"])
        A["X-d"][B]["every_answer"]["value"] = frac(sc["X-d"] - PR.MOVE - Fraction(1, 10_000))
        self.assertFalse(holds(A, Bc, C, sc)["A7"])

    def test_b1_reads_the_sides_stage_c_found(self):
        A, Bc, C, sc = as_expected()
        Bc["X-c"][B]["value"] = frac(Fraction(0))
        self.assertFalse(holds(A, Bc, C, sc)["B1"])
        A, Bc, C, sc = as_expected()
        del Bc["X-f"][B]
        self.assertFalse(holds(A, Bc, C, sc)["B1"])

    def test_c1_at_its_gap_and_its_floor(self):
        A, Bc, C, sc = as_expected()
        C["accuracy"][R]["difference"] = frac(-PR.ALIKE)
        self.assertTrue(holds(A, Bc, C, sc)["C1"])
        C["accuracy"][R]["difference"] = frac(-PR.ALIKE - Fraction(1, 10_000))
        self.assertFalse(holds(A, Bc, C, sc)["C1"])
        A, Bc, C, sc = as_expected()
        C["accuracy"]["every_other"]["asks"] = 99
        self.assertFalse(holds(A, Bc, C, sc)["C1"])

    def test_c2_is_strict_in_each_arm(self):
        A, Bc, C, sc = as_expected()
        C["agreement"]["ticket"]["two_providers"]["agree"] = frac(Fraction(9, 10))
        self.assertFalse(holds(A, Bc, C, sc)["C2"])


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_reading_a_record(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(score, "read", side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                PR.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(PR.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
