"""
The frozen DSL: conditions, validation and specificity arbitration.

`harness/dsl.py` is frozen specification (hard rule 1). These tests do not ask
it to behave WELL: they ask it to behave THE SAME, because the rung 1 figures
were measured over this exact behaviour. That is why it includes a
characterization test of the defect recorded in CLAUDE.md — that CONFLICT is
returned before reaching the age tie-break — which is a design failure and at
the same time the central fact rung 1 measured.
"""

from __future__ import annotations

import unittest

from harness.domain import Case
from harness.dsl import (OPS, Condition, Rule, RuleEngine, RuleValidationError,
                         validate_rule_payload)


def make_case(**over) -> Case:
    base = dict(has_security_keyword=False, severity=3, customer_tier="free",
                product="dashboard", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


def rule(rid: str, conds, action: str, born_at: int = 0) -> Rule:
    return Rule(rule_id=rid,
                conditions=[Condition(a, o, v) for a, o, v in conds],
                action=action, born_at=born_at)


class TestCondition(unittest.TestCase):

    def test_eq(self):
        c = Condition("severity", "eq", 1)
        self.assertTrue(c.holds(make_case(severity=1)))
        self.assertFalse(c.holds(make_case(severity=2)))

    def test_neq(self):
        c = Condition("customer_tier", "neq", "enterprise")
        self.assertTrue(c.holds(make_case(customer_tier="free")))
        self.assertFalse(c.holds(make_case(customer_tier="enterprise")))

    def test_lte_and_gte_include_the_endpoint(self):
        self.assertTrue(Condition("severity", "lte", 2).holds(make_case(severity=2)))
        self.assertFalse(Condition("severity", "lte", 2).holds(make_case(severity=3)))
        self.assertTrue(Condition("severity", "gte", 2).holds(make_case(severity=2)))
        self.assertFalse(Condition("severity", "gte", 2).holds(make_case(severity=1)))

    def test_in(self):
        c = Condition("customer_tier", "in", ["business", "enterprise"])
        self.assertTrue(c.holds(make_case(customer_tier="business")))
        self.assertFalse(c.holds(make_case(customer_tier="pro")))

    def test_unknown_operator_blows_up(self):
        with self.assertRaises(AssertionError):
            Condition("severity", "between", 2).holds(make_case())

    def test_the_operator_vocabulary_is_the_declared_one(self):
        self.assertEqual(OPS, {"eq", "neq", "lte", "gte", "in"})


class TestValidation(unittest.TestCase):
    """No LLM judgement takes part here: these are mechanical checks."""

    def valid_payload(self, **over):
        p = {"rule_id": "X1", "action": "T2_TECHNICAL",
             "conditions": [{"attr": "severity", "op": "lte", "value": 2}]}
        p.update(over)
        return p

    def test_valid_payload(self):
        r = validate_rule_payload(self.valid_payload())
        self.assertEqual(r.action, "T2_TECHNICAL")
        self.assertEqual(r.specificity, 1)
        self.assertEqual(r.conditions[0].attr, "severity")

    def test_must_match_the_case_that_originated_it(self):
        p = self.valid_payload()
        validate_rule_payload(p, case=make_case(severity=1))
        with self.assertRaises(RuleValidationError):
            validate_rule_payload(p, case=make_case(severity=4))

    def test_the_note_is_truncated_to_280(self):
        r = validate_rule_payload(self.valid_payload(note="x" * 500))
        self.assertEqual(len(r.note), 280)

    def test_default_rule_id(self):
        r = validate_rule_payload(self.valid_payload(rule_id=None))
        self.assertEqual(r.rule_id, "R?")

    def test_rejections(self):
        cases = {
            "payload no es objeto": "no soy un dict",
            "accion inventada": self.valid_payload(action="T9_INVENTADA"),
            "sin accion": self.valid_payload(action=None),
            "conditions no es lista": self.valid_payload(conditions={"a": 1}),
            "conditions vacia": self.valid_payload(conditions=[]),
            "condicion no es objeto": self.valid_payload(conditions=["severity<=2"]),
            "atributo inventado": self.valid_payload(
                conditions=[{"attr": "urgencia", "op": "eq", "value": 1}]),
            "operador inventado": self.valid_payload(
                conditions=[{"attr": "severity", "op": "between", "value": 2}]),
            "condicion duplicada": self.valid_payload(conditions=[
                {"attr": "severity", "op": "eq", "value": 2},
                {"attr": "severity", "op": "eq", "value": 3}]),
            "lte sobre no numerico": self.valid_payload(
                conditions=[{"attr": "product", "op": "lte", "value": "api"}]),
            "lte con valor no entero": self.valid_payload(
                conditions=[{"attr": "severity", "op": "lte", "value": "2"}]),
            "lte con booleano": self.valid_payload(
                conditions=[{"attr": "severity", "op": "lte", "value": True}]),
            "lte fuera de dominio": self.valid_payload(
                conditions=[{"attr": "severity", "op": "lte", "value": 9}]),
            "in con valor no lista": self.valid_payload(
                conditions=[{"attr": "customer_tier", "op": "in", "value": "free"}]),
            "in con lista vacia": self.valid_payload(
                conditions=[{"attr": "customer_tier", "op": "in", "value": []}]),
            "in con miembro fuera de dominio": self.valid_payload(
                conditions=[{"attr": "customer_tier", "op": "in",
                             "value": ["free", "titanium"]}]),
            "eq fuera de dominio": self.valid_payload(
                conditions=[{"attr": "product", "op": "eq", "value": "crm"}]),
        }
        for name, payload in cases.items():
            with self.subTest(name):
                with self.assertRaises(RuleValidationError):
                    validate_rule_payload(payload)

    def test_more_conditions_than_attributes(self):
        conds = [{"attr": "severity", "op": "eq", "value": 1}] * 9
        with self.assertRaises(RuleValidationError):
            validate_rule_payload(self.valid_payload(conditions=conds))

    def test_one_condition_per_attribute_and_a_different_operator_is_allowed(self):
        r = validate_rule_payload(self.valid_payload(conditions=[
            {"attr": "severity", "op": "gte", "value": 2},
            {"attr": "severity", "op": "lte", "value": 3}]))
        self.assertEqual(r.specificity, 2)


class TestRuleEngine(unittest.TestCase):

    def test_add_assigns_a_sequential_id_and_born_at(self):
        e = RuleEngine()
        a = e.add(rule("?", [("severity", "eq", 1)], "T1_GENERAL"), born_at=7)
        b = e.add(rule("?", [("severity", "eq", 2)], "T1_GENERAL"), born_at=9)
        self.assertEqual((a.rule_id, a.born_at), ("R0001", 7))
        self.assertEqual((b.rule_id, b.born_at), ("R0002", 9))

    def test_impasse_when_nothing_matches(self):
        e = RuleEngine()
        e.rules = [rule("A", [("severity", "eq", 1)], "T1_GENERAL")]
        outcome, winner, matched = e.decide(make_case(severity=4))
        self.assertEqual(outcome, "IMPASSE")
        self.assertIsNone(winner)
        self.assertEqual(matched, [])

    def test_the_most_specific_one_wins(self):
        e = RuleEngine()
        e.rules = [
            rule("GENERICA", [("severity", "eq", 3)], "T1_GENERAL", born_at=0),
            rule("ESPECIFICA", [("severity", "eq", 3), ("product", "eq", "dashboard")],
                 "T2_TECHNICAL", born_at=1),
        ]
        outcome, winner, matched = e.decide(make_case())
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "ESPECIFICA")
        self.assertEqual(len(matched), 2)

    def test_at_equal_specificity_and_same_action_the_oldest_wins(self):
        e = RuleEngine()
        e.rules = [
            rule("NUEVA", [("severity", "eq", 3)], "T1_GENERAL", born_at=50),
            rule("VIEJA", [("product", "eq", "dashboard")], "T1_GENERAL", born_at=2),
        ]
        outcome, winner, _ = e.decide(make_case())
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "VIEJA")

    def test_conflict_at_equal_specificity_with_different_actions(self):
        e = RuleEngine()
        e.rules = [
            rule("A", [("severity", "eq", 3)], "T1_GENERAL", born_at=0),
            rule("B", [("product", "eq", "dashboard")], "T2_TECHNICAL", born_at=1),
        ]
        outcome, winner, finalists = e.decide(make_case())
        self.assertEqual(outcome, "CONFLICT")
        self.assertIsNone(winner)
        self.assertEqual({r.rule_id for r in finalists}, {"A", "B"})

    def test_a_less_specific_rule_does_not_enter_the_conflict(self):
        """The finalists are only those of maximum specificity."""
        e = RuleEngine()
        e.rules = [
            rule("GEN", [("severity", "eq", 3)], "SELF_SERVICE_DEFLECT", born_at=0),
            rule("A", [("severity", "eq", 3), ("channel", "eq", "portal")],
                 "T1_GENERAL", born_at=1),
            rule("B", [("severity", "eq", 3), ("product", "eq", "dashboard")],
                 "T2_TECHNICAL", born_at=2),
        ]
        outcome, _, finalists = e.decide(make_case())
        self.assertEqual(outcome, "CONFLICT")
        self.assertEqual({r.rule_id for r in finalists}, {"A", "B"})

    def test_RECORDED_DEFECT_the_conflict_precedes_the_tiebreak(self):
        """CHARACTERIZATION of the defect documented in CLAUDE.md, not approval.

        `decide` returns CONFLICT as soon as the finalists disagree, so the age
        tie-break —which is the correct semantics— is left unreachable exactly
        when it would decide something. It is the defect that yields 505
        CONFLICT and sinks the rung 1 ceiling to 0.5875, and it is pinned here
        because `dsl.py` is a closed record and its figures must reproduce. The
        redesign already exists separately, in `rung2/engine2.py`.
        """
        e = RuleEngine()
        e.rules = [
            rule("VIEJA", [("severity", "eq", 3)], "T1_GENERAL", born_at=0),
            rule("NUEVA", [("product", "eq", "dashboard")], "T2_TECHNICAL", born_at=99),
        ]
        outcome, winner, _ = e.decide(make_case())
        self.assertEqual(outcome, "CONFLICT")
        self.assertIsNone(winner, "si algun dia gana VIEJA, el techo del "
                                  "rung 1 deja de ser 0,5875")


if __name__ == "__main__":
    unittest.main()
