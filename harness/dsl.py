"""
DSL de reglas: representacion intermedia tipada y restringida.

El proponente (LLM o mock) NUNCA emite codigo. Emite este esquema cerrado, que
un compilador determinista valida y ejecuta. Es la separacion
superficie-de-autoria / sustrato acordada en el diseno.

Peldano 1: el motor es una lista de reglas con resolucion de conflictos por
especificidad. No hay ASP todavia; el esquema esta pensado para bajarse a ASP
sin cambios cuando llegue el peldano 3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .domain import ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case

OPS = {"eq", "neq", "lte", "gte", "in"}


class RuleValidationError(Exception):
    pass


@dataclass
class Condition:
    attr: str
    op: str
    value: Any

    def holds(self, case: Case) -> bool:
        v = getattr(case, self.attr)
        if self.op == "eq":
            return v == self.value
        if self.op == "neq":
            return v != self.value
        if self.op == "lte":
            return v <= self.value
        if self.op == "gte":
            return v >= self.value
        if self.op == "in":
            return v in self.value
        raise AssertionError(f"op desconocido: {self.op}")

    def as_dict(self) -> dict[str, Any]:
        return {"attr": self.attr, "op": self.op, "value": self.value}


@dataclass
class Rule:
    rule_id: str
    conditions: list[Condition]
    action: str
    born_at: int = -1          # indice del caso que la genero
    fire_count: int = 0        # disparos posteriores a su creacion
    correct_count: int = 0     # de esos, cuantos acertaron
    note: str = ""             # justificacion libre del proponente (no ejecutable)

    @property
    def specificity(self) -> int:
        return len(self.conditions)

    def matches(self, case: Case) -> bool:
        return all(c.holds(case) for c in self.conditions)

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "conditions": [c.as_dict() for c in self.conditions],
            "action": self.action,
            "born_at": self.born_at,
            "fire_count": self.fire_count,
            "correct_count": self.correct_count,
            "note": self.note,
        }


# ---------------------------------------------------------------------------
# Validacion
# ---------------------------------------------------------------------------

def validate_rule_payload(payload: dict[str, Any], case: Case | None = None) -> Rule:
    """
    Valida el payload de una regla candidata.

    Comprobaciones mecanicas (ningun juicio de LLM interviene aqui):
      - esquema y tipos
      - atributos y acciones dentro del vocabulario cerrado
      - valores dentro del dominio declarado
      - operadores numericos solo sobre atributos numericos
      - no vacia, sin condiciones duplicadas sobre el mismo atributo+op
      - si se pasa `case`: la regla debe casar el caso que la origino
    """
    if not isinstance(payload, dict):
        raise RuleValidationError("payload no es un objeto")

    action = payload.get("action")
    if action not in ACTIONS:
        raise RuleValidationError(f"accion invalida: {action!r}")

    raw_conds = payload.get("conditions")
    if not isinstance(raw_conds, list) or not raw_conds:
        raise RuleValidationError("conditions debe ser una lista no vacia")
    if len(raw_conds) > len(ATTRIBUTES):
        raise RuleValidationError("demasiadas condiciones")

    conds: list[Condition] = []
    seen: set[tuple[str, str]] = set()
    for rc in raw_conds:
        if not isinstance(rc, dict):
            raise RuleValidationError("condicion no es un objeto")
        attr, op, value = rc.get("attr"), rc.get("op"), rc.get("value")

        if attr not in ATTRIBUTES:
            raise RuleValidationError(f"atributo invalido: {attr!r}")
        if op not in OPS:
            raise RuleValidationError(f"operador invalido: {op!r}")
        if (attr, op) in seen:
            raise RuleValidationError(f"condicion duplicada: {attr}/{op}")
        seen.add((attr, op))

        if op in ("lte", "gte"):
            if attr not in NUMERIC_ATTRS:
                raise RuleValidationError(f"{op} sobre atributo no numerico: {attr}")
            if not isinstance(value, int) or isinstance(value, bool):
                raise RuleValidationError(f"valor no entero para {op}: {value!r}")
            if value not in DOMAINS[attr]:
                raise RuleValidationError(f"valor fuera de dominio: {attr}={value!r}")
        elif op == "in":
            if not isinstance(value, list) or not value:
                raise RuleValidationError("valor de 'in' debe ser lista no vacia")
            for v in value:
                if v not in DOMAINS[attr]:
                    raise RuleValidationError(f"valor fuera de dominio: {attr}={v!r}")
        else:  # eq / neq
            if value not in DOMAINS[attr]:
                raise RuleValidationError(f"valor fuera de dominio: {attr}={value!r}")

        conds.append(Condition(attr=attr, op=op, value=value))

    rule = Rule(
        rule_id=str(payload.get("rule_id") or "R?"),
        conditions=conds,
        action=action,
        note=str(payload.get("note", ""))[:280],
    )

    if case is not None and not rule.matches(case):
        raise RuleValidationError("la regla no casa el caso que la origino")

    return rule


# ---------------------------------------------------------------------------
# Motor
# ---------------------------------------------------------------------------

@dataclass
class RuleEngine:
    """
    Motor de reglas con tres resultados posibles:
      - ACTION   : una regla gana y propone accion
      - IMPASSE  : ninguna regla casa (impasse de cobertura)
      - CONFLICT : empatan reglas con acciones distintas (impasse logico)

    Resolucion de conflictos: gana la mas especifica (mas condiciones);
    a igual especificidad y misma accion, gana la mas antigua; a igual
    especificidad y acciones distintas -> CONFLICT.
    """

    rules: list[Rule] = field(default_factory=list)
    _next_id: int = 1

    def add(self, rule: Rule, born_at: int) -> Rule:
        rule.rule_id = f"R{self._next_id:04d}"
        rule.born_at = born_at
        self._next_id += 1
        self.rules.append(rule)
        return rule

    def decide(self, case: Case) -> tuple[str, Rule | None, list[Rule]]:
        matched = [r for r in self.rules if r.matches(case)]
        if not matched:
            return "IMPASSE", None, []

        top = max(r.specificity for r in matched)
        finalists = [r for r in matched if r.specificity == top]
        actions = {r.action for r in finalists}
        if len(actions) > 1:
            return "CONFLICT", None, finalists

        winner = min(finalists, key=lambda r: r.born_at)
        return "ACTION", winner, matched
