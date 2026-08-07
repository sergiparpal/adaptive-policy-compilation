"""
Rule DSL: a typed, restricted intermediate representation.

The proposer (LLM or mock) NEVER emits code. It emits this closed schema, which
a deterministic compiler validates and executes. This is the authoring-surface /
substrate separation agreed on in the design.

Rung 1: the engine is a list of rules with conflict resolution by specificity.
There is no ASP yet; the schema is meant to be lowered to ASP without changes
when rung 3 arrives.
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
    born_at: int = -1          # index of the case that generated it
    fire_count: int = 0        # firings after its creation
    correct_count: int = 0     # of those, how many were right
    note: str = ""             # free-form proposer justification (not executable)

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
# Validation
# ---------------------------------------------------------------------------

def validate_rule_payload(payload: dict[str, Any], case: Case | None = None) -> Rule:
    """
    Validates the payload of a candidate rule.

    Mechanical checks (no LLM judgement takes part here):
      - schema and types
      - attributes and actions inside the closed vocabulary
      - values inside the declared domain
      - numeric operators only over numeric attributes
      - non-empty, no duplicate conditions over the same attribute+op
      - if `case` is passed: the rule must match the case that originated it
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
# Engine
# ---------------------------------------------------------------------------

@dataclass
class RuleEngine:
    """
    Rule engine with three possible outcomes:
      - ACTION   : one rule wins and proposes an action
      - IMPASSE  : no rule matches (coverage impasse)
      - CONFLICT : rules with different actions tie (logical impasse)

    Conflict resolution: the most specific one wins (most conditions); at equal
    specificity and the same action, the oldest wins; at equal specificity and
    different actions -> CONFLICT.
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
