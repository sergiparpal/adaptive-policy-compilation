"""
The rung 2 hybrid engine: extensions, subsumption and declared priority.

Two different things to test here:

  * that the BITMASKS say the same as `Condition.holds`. All of subsumption is
    computed with big integers instead of sweeping cases; if that equivalence
    breaks, the partial order that comes out belongs to another problem.
  * that the EDGE VALIDATOR rejects what it says it rejects. It is what makes a
    reference mechanically verifiable and an integer not, which is the entire
    argument for the level 2 design.
"""

from __future__ import annotations

import unittest

from harness.ceiling_check import all_cases
from harness.domain import Case
from harness.dsl import Condition, RuleValidationError
from rung2.engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT,
                              EDGE_OK, EDGE_SELF, EDGE_UNKNOWN, PriorityEngine,
                              Rule2, strictly_below, validate_conditions)

from .fixtures import SPACE_SIZE, space


def make_case(**over) -> Case:
    base = dict(has_security_keyword=False, severity=3, customer_tier="free",
                product="dashboard", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


def r2(rid: str, conds, action: str, born_at: int = 0) -> Rule2:
    return Rule2(rule_id=rid,
                 conditions=[Condition(a, o, v) for a, o, v in conds],
                 action=action, born_at=born_at)


class TestSpace(unittest.TestCase):

    def test_tamano_y_mascara_llena(self):
        s = space()
        self.assertEqual(s.n, SPACE_SIZE)
        self.assertEqual(s.full.bit_count(), SPACE_SIZE)

    def test_las_mascaras_coinciden_con_Condition_holds(self):
        """One pass over the complete space comparing the two routes."""
        conds = [
            Condition("severity", "eq", 1),
            Condition("customer_tier", "neq", "enterprise"),
            Condition("severity", "lte", 2),
            Condition("prior_tickets_30d", "gte", 5),
            Condition("customer_tier", "in", ["business", "enterprise"]),
            Condition("has_security_keyword", "eq", True),
        ]
        esperado = [0] * len(conds)
        for case in all_cases():
            for k, c in enumerate(conds):
                if c.holds(case):
                    esperado[k] += 1
        for k, c in enumerate(conds):
            with self.subTest(str(c.as_dict())):
                self.assertEqual(space().condition_mask(c).bit_count(), esperado[k])

    def test_la_extension_es_la_interseccion(self):
        s = space()
        a = Condition("severity", "eq", 1)
        b = Condition("product", "eq", "api")
        self.assertEqual(s.extension([a, b]),
                         s.condition_mask(a) & s.condition_mask(b))

    def test_extension_vacia(self):
        s = space()
        self.assertEqual(s.extension([Condition("severity", "lte", 1),
                                      Condition("severity", "gte", 2)]), 0)

    def test_sin_condiciones_es_todo_el_espacio(self):
        self.assertEqual(space().extension([]), space().full)


class TestStrictlyBelow(unittest.TestCase):

    def test_subconjunto_estricto(self):
        self.assertTrue(strictly_below(0b0110, 0b1110))

    def test_iguales_no_cuenta(self):
        self.assertFalse(strictly_below(0b1110, 0b1110))

    def test_incomparables(self):
        self.assertFalse(strictly_below(0b0011, 0b0110))
        self.assertFalse(strictly_below(0b0110, 0b0011))


class TestSubsuncion(unittest.TestCase):

    def setUp(self):
        self.e = PriorityEngine(space=space())

    def test_anadir_una_condicion_baja_en_el_orden(self):
        general = self.e.add(r2("GEN", [("product", "eq", "api")], "T2_TECHNICAL"), 0, True)
        especial = self.e.add(r2("ESP", [("product", "eq", "api"),
                                         ("severity", "lte", 2)], "T3_ENGINEERING"), 1, True)
        self.assertIn(especial.rule_id, self.e.sub_below[general.rule_id])
        self.assertIn(general.rule_id, self.e.sub_above[especial.rule_id])

    def test_la_mas_especifica_gana_sin_declarar_nada(self):
        self.e.add(r2("GEN", [("product", "eq", "api")], "T2_TECHNICAL"), 0, True)
        self.e.add(r2("ESP", [("product", "eq", "api"),
                              ("severity", "lte", 2)], "T3_ENGINEERING"), 1, True)
        outcome, winner, _ = self.e.decide(make_case(product="api", severity=1))
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "ESP")

    def test_impasse_sin_reglas_que_casen(self):
        self.e.add(r2("A", [("severity", "eq", 1)], "T2_TECHNICAL"), 0, True)
        self.assertEqual(self.e.decide(make_case(severity=4))[0], "IMPASSE")

    def test_conflicto_entre_incomparables_con_acciones_distintas(self):
        self.e.add(r2("A", [("severity", "eq", 3)], "T1_GENERAL"), 0, True)
        self.e.add(r2("B", [("product", "eq", "dashboard")], "T2_TECHNICAL"), 1, True)
        outcome, winner, invictas = self.e.decide(make_case())
        self.assertEqual(outcome, "CONFLICT")
        self.assertIsNone(winner)
        self.assertEqual({x.rule_id for x in invictas}, {"A", "B"})

    def test_incomparables_que_coinciden_en_accion_no_son_conflicto(self):
        self.e.add(r2("A", [("severity", "eq", 3)], "T1_GENERAL"), 0, True)
        self.e.add(r2("B", [("product", "eq", "dashboard")], "T1_GENERAL"), 1, True)
        self.assertEqual(self.e.decide(make_case())[0], "ACTION")

    def test_la_transitividad_sale_gratis(self):
        """A beats B and B beats C: only A stays undefeated, with no closure
        computed. Three rules nested by subsumption."""
        self.e.add(r2("C", [("product", "eq", "api")], "T1_GENERAL"), 0, True)
        self.e.add(r2("B", [("product", "eq", "api"),
                            ("severity", "lte", 2)], "T2_TECHNICAL"), 1, True)
        self.e.add(r2("A", [("product", "eq", "api"), ("severity", "lte", 2),
                            ("customer_tier", "eq", "free")], "T3_ENGINEERING"), 2, True)
        outcome, winner, _ = self.e.decide(
            make_case(product="api", severity=1, customer_tier="free"))
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "A")


class TestValidadorDeAristas(unittest.TestCase):
    """The six verdicts of `try_edge`."""

    def setUp(self):
        self.e = PriorityEngine(space=space())
        self.e.add(r2("A", [("severity", "eq", 3)], "T1_GENERAL"), 0, True)
        self.e.add(r2("B", [("product", "eq", "dashboard")], "T2_TECHNICAL"), 1, True)
        self.e.add(r2("LEJOS", [("severity", "eq", 1)], "ONCALL_ESCALATION"), 2, True)
        self.e.add(r2("SUB", [("severity", "eq", 3),
                              ("product", "eq", "dashboard")], "T3_ENGINEERING"), 3, True)

    def test_ok_entre_incomparables_que_solapan(self):
        self.assertEqual(self.e.try_edge("A", "B"), EDGE_OK)
        self.assertIn("A", self.e.decl_below["B"])
        self.assertIn("B", self.e.decl_above["A"])

    def test_auto_referencia(self):
        self.assertEqual(self.e.try_edge("A", "A"), EDGE_SELF)

    def test_regla_inexistente(self):
        self.assertEqual(self.e.try_edge("A", "R9999"), EDGE_UNKNOWN)
        self.assertEqual(self.e.try_edge("R9999", "A"), EDGE_UNKNOWN)

    def test_extensiones_disjuntas_son_inertes(self):
        """severity==3 and severity==1 can never compete."""
        self.assertEqual(self.e.try_edge("A", "LEJOS"), EDGE_DISJOINT)

    def test_contradecir_la_subsuncion_se_rechaza(self):
        """Subsumption is NOT overridable by declaration: it is the only part of
        the order derived from the semantics and not from conjecture."""
        self.assertEqual(self.e.try_edge("A", "SUB"), EDGE_CONTRADICTS)
        self.assertNotIn("A", self.e.decl_below["SUB"])

    def test_redundante_con_la_subsuncion_se_acepta(self):
        """Declaring what the structure already says is consistent, not an
        error."""
        self.assertEqual(self.e.try_edge("SUB", "A"), EDGE_OK)

    def test_cierre_de_ciclo(self):
        self.assertEqual(self.e.try_edge("A", "B"), EDGE_OK)
        self.assertEqual(self.e.try_edge("B", "A"), EDGE_CYCLE)

    def test_ciclo_de_tres_pasando_por_subsuncion(self):
        """`_reaches` follows edges from BOTH levels, not only declared ones.

        C beats A by subsumption (C = A plus one condition). With B -> C
        declared, the path B -> C -> A exists; declaring A -> B would then close
        a cycle that is only visible if the search crosses level 1.
        """
        self.e.add(r2("C", [("severity", "eq", 3),
                            ("channel", "eq", "portal")], "T3_ENGINEERING"), 4, True)
        self.assertIn("C", self.e.sub_below["A"])                # C ⊊ A
        self.assertEqual(self.e.try_edge("B", "C"), EDGE_OK)
        self.assertEqual(self.e.try_edge("A", "B"), EDGE_CYCLE)

    def test_una_arista_declarada_decide_el_conflicto(self):
        """Without SUB in the way, A and B are incomparable and disagree: it is
        the residue level 1 leaves and level 2 exists to resolve."""
        e = PriorityEngine(space=space())
        e.add(r2("A", [("severity", "eq", 3)], "T1_GENERAL"), 0, True)
        e.add(r2("B", [("product", "eq", "dashboard")], "T2_TECHNICAL"), 1, True)
        self.assertEqual(e.decide(make_case())[0], "CONFLICT")
        self.assertEqual(e.try_edge("A", "B"), EDGE_OK)
        outcome, winner, _ = e.decide(make_case())
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "A")

    def test_la_regla_mas_especifica_zanja_el_conflicto_sin_declarar_nada(self):
        """With SUB loaded, the case matching A, B and SUB is not a conflict:
        SUB subsumes both and is left undefeated on its own."""
        outcome, winner, _ = self.e.decide(make_case())
        self.assertEqual(outcome, "ACTION")
        self.assertEqual(winner.rule_id, "SUB")


class TestValidacionDeCondiciones(unittest.TestCase):
    """Rung 2 revalidates with the same mechanical rules as rung 1."""

    def test_payload_valido(self):
        rule = validate_conditions(
            {"action": "T2_TECHNICAL",
             "conditions": [{"attr": "severity", "op": "lte", "value": 2}]}, None)
        self.assertEqual(rule.action, "T2_TECHNICAL")
        self.assertEqual(rule.rule_id, "R?")

    def test_debe_casar_el_caso_que_la_origino(self):
        payload = {"action": "T2_TECHNICAL",
                   "conditions": [{"attr": "severity", "op": "eq", "value": 1}]}
        with self.assertRaises(RuleValidationError):
            validate_conditions(payload, make_case(severity=3))

    def test_rechazos(self):
        casos = {
            "accion inventada": {"action": "T9", "conditions": [
                {"attr": "severity", "op": "eq", "value": 1}]},
            "sin condiciones": {"action": "T1_GENERAL", "conditions": []},
            "atributo inventado": {"action": "T1_GENERAL", "conditions": [
                {"attr": "urgencia", "op": "eq", "value": 1}]},
            "operador inventado": {"action": "T1_GENERAL", "conditions": [
                {"attr": "severity", "op": "between", "value": 1}]},
            "gte sobre no numerico": {"action": "T1_GENERAL", "conditions": [
                {"attr": "product", "op": "gte", "value": "api"}]},
            "valor fuera de dominio": {"action": "T1_GENERAL", "conditions": [
                {"attr": "product", "op": "eq", "value": "crm"}]},
        }
        for nombre, payload in casos.items():
            with self.subTest(nombre):
                with self.assertRaises(RuleValidationError):
                    validate_conditions(payload, None)


class TestRender(unittest.TestCase):
    """What the proposer sees of a rule. `correct_count` comes from the oracle
    and can never appear."""

    def test_no_filtra_el_acierto(self):
        rule = r2("R0001", [("severity", "eq", 1)], "T2_TECHNICAL")
        rule.fire_count, rule.correct_count = 10, 3
        texto = rule.render()
        self.assertNotIn("3", texto)
        self.assertIn("R0001", texto)
        self.assertIn("T2_TECHNICAL", texto)

    def test_muestra_las_aristas_aceptadas(self):
        rule = r2("R0001", [("severity", "eq", 1)], "T2_TECHNICAL")
        rule.beats, rule.loses_to = ["R0007"], ["R0021"]
        texto = rule.render()
        self.assertIn("gana a R0007", texto)
        self.assertIn("pierde con R0021", texto)


if __name__ == "__main__":
    unittest.main()
