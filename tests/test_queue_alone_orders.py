"""
`queue_alone/orders.py`, the POST-RUN reading of where `PLAN_QUEUE_ALONE.md`'s
order errors go.

WHAT IS PINNED HERE, AND WHY.
  * The names it reads by: the catch-all, the arms, the expectation's lines and
    its record's path.
  * One answer read against a ticket's matching rules, on rules and tickets
    built by hand: the rule it follows and its rank, the runner-up, the
    catch-all, and the most specific rule.
  * An arm's reading: its classes, ranks, shares and the three governing rules
    that carry most of its order errors.
  * The specificity reading on the decisions where the most-conditions rule
    gives another queue than the first.
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

from queue_alone import orders as O
from queue_alone import plan, rules
from queue_alone import score as S

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
F = Fraction

# Four rules: the first two give A and B, a narrow third gives C, and the last
# matches every ticket and gives D, as `H29` does.
RS = rules.parse("H01: SI severity eq 1 ENTONCES A_Q\n"
                 "H02: SI product eq api ENTONCES B_Q\n"
                 "H03: SI severity eq 1 AND product eq api AND off_hours eq True "
                 "ENTONCES C_Q\n"
                 "H29: SI severity gte 1 ENTONCES D_Q\n")


def ticket(**kw) -> dict:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return {**base, **kw}


ALL = ticket(severity=1, product="api", off_hours=True)     # matches all four


class TestTheNames(unittest.TestCase):

    def test_the_names_it_reads_by(self):
        self.assertEqual(O.CATCH_ALL, "H29")
        self.assertEqual(O.ARMS, ("t", "i", "q"))
        self.assertEqual(O.record_path(), Path("results_queue_alone/orders.json"))
        self.assertEqual((O.O1_RUNNER_UP, O.O2_CATCH_ALL, O.O3_SPECIFIC, O.O4_TOP_THREE,
                          O.O5_GAP), (F(1, 2), F(1, 5), F(1, 2), F(1, 2), F(3, 20)))

    def test_the_catch_all_is_the_lists_last_rule(self):
        self.assertEqual(rules.rules()[-1].id, O.CATCH_ALL)
        self.assertEqual(rules.rules()[-1].conditions, (("severity", "gte", 1),))


class TestOneAnswer(unittest.TestCase):

    def test_the_runner_up_and_the_rank(self):
        hit = rules.matching(ALL, RS)
        self.assertEqual([r.id for r in hit], ["H01", "H02", "H03", "H29"])
        self.assertEqual(O.runner_up(hit).id, "H02")
        self.assertEqual([(k, r.id) for k, r in [O.follows(a, hit) for a in
                                                 ("B_Q", "C_Q", "D_Q")]],
                         [(2, "H02"), (3, "H03"), (4, "H29")])
        self.assertIsNone(O.follows("A_Q", hit))
        self.assertIsNone(O.follows("E_Q", hit))

    def test_what_one_answer_is(self):
        got = O.read_answer("B_Q", ALL, RS)
        self.assertEqual((got["class"], got["governing"], got["rank"], got["follows"],
                          got["runner_up"], got["catch_all"], got["most_specific"]),
                         ("order", "H01", 2, "H02", True, False, False))
        got = O.read_answer("C_Q", ALL, RS)
        self.assertEqual((got["runner_up"], got["catch_all"], got["most_specific"]),
                         (False, False, True))
        got = O.read_answer("D_Q", ALL, RS)
        self.assertEqual((got["rank"], got["catch_all"]), (4, True))
        self.assertNotIn("rank", O.read_answer("A_Q", ALL, RS))
        self.assertEqual(O.read_answer("E_Q", ALL, RS)["class"], "matching")

    def test_no_runner_up_when_every_matching_rule_gives_the_first_queue(self):
        rs = rules.parse("H01: SI severity eq 1 ENTONCES A_Q\nH29: SI severity gte 1 "
                         "ENTONCES A_Q\n")
        self.assertIsNone(O.runner_up(rules.matching(ticket(severity=1), rs)))


class TestAnArm(unittest.TestCase):

    def test_classes_ranks_shares_and_the_top_three(self):
        answers = [("A_Q", ALL, "A_Q"), ("B_Q", ALL, "A_Q"), ("C_Q", ALL, "A_Q"),
                   ("D_Q", ALL, "A_Q"), ("E_Q", ALL, "A_Q"),
                   ("D_Q", ticket(product="api"), "B_Q")]
        got = O.arm_reading(answers, RS)
        self.assertEqual(got["classes"], {"first": 1, "order": 4, "matching": 1})
        self.assertEqual(got["rank"], {"2": 2, "3": 1, "4": 1})
        self.assertEqual(got["runner_up"]["count"], 2)
        self.assertEqual(Fraction(got["catch_all"]["share"]["fraction"]), F(2, 4))
        self.assertEqual(got["most_specific"]["count"], 1)
        self.assertEqual(got["governing"][0], {"rule": "H01", "order_errors": 3, "answers": 5})
        self.assertEqual(got["top_three"]["rules"], ["H01", "H02"])
        self.assertEqual(Fraction(got["top_three"]["share"]["fraction"]), 1)

    def test_an_arm_with_no_order_error_has_no_shares(self):
        got = O.arm_reading([("A_Q", ALL, "A_Q")], RS)
        self.assertEqual(got["order_errors"], 0)
        self.assertIsNone(got["runner_up"]["share"])

    def test_specificity_reads_only_where_the_most_specific_rule_differs(self):
        answers = [("C_Q", ALL, "A_Q"), ("A_Q", ALL, "A_Q"), ("B_Q", ALL, "A_Q"),
                   ("A_Q", ticket(severity=1), "A_Q")]
        got = O.specificity(answers, RS)
        self.assertEqual((got["answers"], got["most_specific"], got["first"], got["other"]),
                         (3, 1, 1, 1))
        self.assertEqual(Fraction(got["most_specific_share"]["fraction"]), F(1, 3))


def arms_at(runner_up=(5, 10), catch_all=(1, 10), top=(5, 10), rule_up=(5, 10)):
    def arm(up, catch, t3):
        return {"order_errors": up[1],
                "runner_up": {"count": up[0], "share": S.frac(F(*up))},
                "catch_all": {"count": catch[0], "share": S.frac(F(*catch))},
                "top_three": {"rules": ["H01", "H02", "H03"], "share": S.frac(F(*t3))}}
    return {"t": arm(rule_up, (0, 10), (5, 10)), "i": arm((0, 10), (0, 10), (0, 10)),
            "q": arm(runner_up, catch_all, top)}


def spec_at(k=5, n=10):
    return {"q": {"answers": n, "most_specific": k, "most_specific_share": S.frac(F(k, n))}}


def holds(arms, spec) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in O.read_expectation(arms, spec)}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_at_its_line(self):
        got = holds(arms_at(), spec_at())
        self.assertEqual(list(got), ["O1", "O2", "O3", "O4", "O5"])
        self.assertTrue(all(got.values()))

    def test_o1_o3_o4_hold_at_a_half_and_fail_below(self):
        self.assertFalse(holds(arms_at(runner_up=(4, 10)), spec_at())["O1"])
        self.assertFalse(holds(arms_at(), spec_at(k=4))["O3"])
        self.assertFalse(holds(arms_at(top=(4, 10)), spec_at())["O4"])

    def test_o2_is_strict(self):
        self.assertFalse(holds(arms_at(catch_all=(2, 10)), spec_at())["O2"])
        self.assertTrue(holds(arms_at(catch_all=(19, 100)), spec_at())["O2"])

    def test_o5_at_its_gap(self):
        self.assertTrue(holds(arms_at(rule_up=(13, 20)), spec_at())["O5"])
        self.assertFalse(holds(arms_at(rule_up=(66, 100)), spec_at())["O5"])


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_reading_a_record(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(S, "read", side_effect=AssertionError("read")) as read, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                O.main([])
        read.assert_not_called()
        write.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(O.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
