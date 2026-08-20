"""
Rung 2 engine: two-level hybrid arbitration.

  LEVEL 1  SUBSUMPTION (derived from the semantics, non-negotiable)
           A ≺ B  iff  ext(A) ⊊ ext(B), over the exhaustive space of 134,400
           combinations. A PARTIAL order: it leaves pairs incomparable.

  LEVEL 2  DECLARED PRIORITY (authored by the proposer, validated)
           Directed edges between specific rules: "A beats B". They only take
           effect where subsumption is silent.

  If after both levels undefeated rules with different actions remain ->
  CONFLICT. Abstaining is correct: in rung 1 subsumption gave a silent error of
  0.0000 precisely because it abstained instead of inventing.

SHAPE OF THE PRIORITY FIELD: referential, not a global integer.

  {"beats": ["R0007"], "loses_to": ["R0021"]}

Justification, with the figures from rung 1:

  * A global integer (layer level) demands a GLOBAL decision from the proposer
    based on a LOCAL observation: it sees a ticket and, at most, a handful of
    rules. It is the same demand that failed in rung 1, under another name.
  * The missing information is small and PARTIAL, not total: over the hidden
    policy, 131 minimal sets covered the whole residue and ~50 targeted
    tie-breaks gave 95% e2e. Those are relations between pairs, which is exactly
    what a reference expresses and an integer does not.
  * A reference is mechanically VERIFIABLE: the cited rule exists, overlaps,
    does not contradict subsumption, does not close a cycle. An integer is
    unfalsifiable: any number passes any validator.
  * A reference COMPOSES with subsumption (it adds edges to the same graph). An
    integer COMPETES with it: if the integer says A>B and subsumption says
    B ≺ A, there is no non-arbitrary way to arbitrate between the two
    arbitrations.

Both directions (`beats` and `loses_to`) are admitted because from a local
observation both are natural: a rule can be born as an exception to an existing
one, or as a default to which an existing one is the exception. They are the
same edge seen from either end.

Subsumption is NOT overridable by declaration. It is the only part of the order
derived from the semantics rather than from the proposer's conjecture, and in
rung 1 it turned out sound (0 contradictions over the hidden policy). Edges that
contradict it are rejected and COUNTED: if that counter comes out high, the
assumption is visibly false and must be revisited, not patched.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case
from harness.dsl import Condition, RuleValidationError

OPS = {"eq", "neq", "lte", "gte", "in"}


# ---------------------------------------------------------------------------
# Extensions: bitmasks over the exhaustive space
# ---------------------------------------------------------------------------

class Space:
    """The complete case space and the masks per (attribute, value). Built
    once; computing a rule's extension is an AND of big integers, not a
    sweep."""

    def __init__(self) -> None:
        cases = list(all_cases())
        self.n = len(cases)
        self.full = (1 << self.n) - 1
        bits: dict[str, dict[Any, bytearray]] = {
            a: {v: bytearray(self.n) for v in DOMAINS[a]} for a in ATTRIBUTES
        }
        for i, c in enumerate(cases):
            for a in ATTRIBUTES:
                bits[a][getattr(c, a)][i] = 1
        self.mask = {
            a: {v: int("".join(map(str, b)), 2) for v, b in d.items()}
            for a, d in bits.items()
        }

    def condition_mask(self, cond: Condition) -> int:
        m = self.mask[cond.attr]
        if cond.op == "eq":
            return m.get(cond.value, 0)
        if cond.op == "neq":
            return self.full & ~m.get(cond.value, 0)
        if cond.op == "in":
            out = 0
            for v in cond.value:
                out |= m.get(v, 0)
            return out
        if cond.op in ("lte", "gte"):
            out = 0
            for v in DOMAINS[cond.attr]:
                if (v <= cond.value) if cond.op == "lte" else (v >= cond.value):
                    out |= m[v]
            return out
        raise AssertionError(cond.op)

    def extension(self, conditions) -> int:
        acc = self.full
        for c in conditions:
            acc &= self.condition_mask(c)
            if acc == 0:
                break
        return acc


def strictly_below(a: int, b: int) -> bool:
    """ext(A) ⊊ ext(B)."""
    return a != b and (a | b) == b


# ---------------------------------------------------------------------------
# Rule
# ---------------------------------------------------------------------------

@dataclass
class Rule2:
    rule_id: str
    conditions: list[Condition]
    action: str
    born_at: int = -1
    fire_count: int = 0
    correct_count: int = 0          # record only; never shown to the proposer
    note: str = ""
    beats: list[str] = field(default_factory=list)       # declared and ACCEPTED
    loses_to: list[str] = field(default_factory=list)
    dropped_edges: list[str] = field(default_factory=list)

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
            "beats": self.beats,
            "loses_to": self.loses_to,
            "dropped_edges": self.dropped_edges,
            "note": self.note,
        }

    def render(self) -> str:
        """How it is shown to the proposer. NO correct_count: that is the oracle's."""
        conds = " AND ".join(f"{c.attr} {c.op} {c.value}" for c in self.conditions)
        s = f"{self.rule_id}: SI {conds} ENTONCES {self.action}"
        if self.beats:
            s += f"  [gana a {', '.join(self.beats)}]"
        if self.loses_to:
            s += f"  [pierde con {', '.join(self.loses_to)}]"
        return s


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_conditions(payload: dict[str, Any], case: Case | None):
    """The same mechanical checks as rung 1."""
    action = payload.get("action")
    if action not in ACTIONS:
        raise RuleValidationError(f"accion invalida: {action!r}")
    raw = payload.get("conditions")
    if not isinstance(raw, list) or not raw:
        raise RuleValidationError("conditions debe ser una lista no vacia")
    if len(raw) > len(ATTRIBUTES):
        raise RuleValidationError("demasiadas condiciones")

    conds: list[Condition] = []
    seen: set[tuple[str, str]] = set()
    for rc in raw:
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
        else:
            if value not in DOMAINS[attr]:
                raise RuleValidationError(f"valor fuera de dominio: {attr}={value!r}")
        conds.append(Condition(attr=attr, op=op, value=value))

    rule = Rule2(rule_id="R?", conditions=conds, action=action,
                 note=str(payload.get("note", ""))[:280])
    if case is not None and not rule.matches(case):
        raise RuleValidationError("la regla no casa el caso que la origino")
    return rule


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

EDGE_OK = "ok"
EDGE_UNKNOWN = "regla_inexistente"
EDGE_DISJOINT = "no_solapan"
EDGE_SELF = "auto_referencia"
EDGE_CONTRADICTS = "contradice_subsuncion"
EDGE_CYCLE = "cierra_ciclo"


@dataclass
class PriorityEngine:
    """
    Three outcomes, as in rung 1: ACTION, IMPASSE, CONFLICT.

    beats(A, B) iff  ext(A) ⊊ ext(B)          [subsumption, non-negotiable]
                 or  declared edge A -> B     [declared priority, validated]

    The UNDEFEATED set wins: the rules no other matching rule defeats. If they
    agree on the action -> ACTION. If they disagree -> CONFLICT. Transitivity
    comes for free: if A beats B and B beats C, B and C are defeated and only A
    remains undefeated, with no closure computed.
    """

    space: Space
    rules: list[Rule2] = field(default_factory=list)
    ext: dict[str, int] = field(default_factory=dict)
    sub_below: dict[str, set[str]] = field(default_factory=dict)   # who subsumes me
    sub_above: dict[str, set[str]] = field(default_factory=dict)   # whom I subsume
    decl_below: dict[str, set[str]] = field(default_factory=dict)  # who beats me, declared
    decl_above: dict[str, set[str]] = field(default_factory=dict)  # whom I beat, declared
    edge_log: list[tuple[str, str, str]] = field(default_factory=list)
    _next_id: int = 1

    # -- construction --------------------------------------------------------

    def add(self, rule: Rule2, born_at: int, keep_id: bool = False) -> Rule2:
        if not keep_id:
            rule.rule_id = f"R{self._next_id:04d}"
            self._next_id += 1
        rule.born_at = born_at
        e = self.space.extension(rule.conditions)
        self.ext[rule.rule_id] = e
        self.sub_below[rule.rule_id] = set()
        self.sub_above[rule.rule_id] = set()
        self.decl_below.setdefault(rule.rule_id, set())
        self.decl_above.setdefault(rule.rule_id, set())
        for other in self.rules:
            oe = self.ext[other.rule_id]
            if strictly_below(oe, e):
                self.sub_below[rule.rule_id].add(other.rule_id)
                self.sub_above[other.rule_id].add(rule.rule_id)
            elif strictly_below(e, oe):
                self.sub_below[other.rule_id].add(rule.rule_id)
                self.sub_above[rule.rule_id].add(other.rule_id)
        self.rules.append(rule)
        return rule

    def beats_me(self, rid: str) -> set[str]:
        return self.sub_below[rid] | self.decl_below[rid]

    def wins_over(self, rid: str) -> set[str]:
        return self.sub_above[rid] | self.decl_above[rid]

    def _reaches(self, src: str, dst: str) -> bool:
        """Does src reach dst following 'beats' edges? (subsumption + declared)"""
        seen, stack = set(), [src]
        while stack:
            cur = stack.pop()
            if cur == dst:
                return True
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self.wins_over(cur))
        return False

    def try_edge(self, winner: str, loser: str) -> str:
        """Installs 'winner beats loser'. Returns the reason if it rejects it."""
        if winner == loser:
            return EDGE_SELF
        if winner not in self.ext or loser not in self.ext:
            return EDGE_UNKNOWN
        ew, item = self.ext[winner], self.ext[loser]
        if ew & item == 0:
            return EDGE_DISJOINT            # they can never compete: inert
        if strictly_below(item, ew):
            return EDGE_CONTRADICTS         # subsumption already says otherwise
        if strictly_below(ew, item):
            return EDGE_OK                  # redundant but consistent; accepted
        if self._reaches(loser, winner):
            return EDGE_CYCLE
        self.decl_below[loser].add(winner)
        self.decl_above[winner].add(loser)
        return EDGE_OK

    # -- decision ------------------------------------------------------------

    def decide(self, case: Case):
        matched = [r for r in self.rules if r.matches(case)]
        if not matched:
            return "IMPASSE", None, []
        ids = {r.rule_id for r in matched}
        undefeated = [r for r in matched if not (self.beats_me(r.rule_id) & ids)]
        if not undefeated:                  # only possible if a cycle slipped in
            return "CONFLICT", None, matched
        if len({r.action for r in undefeated}) == 1:
            return "ACTION", undefeated[0], matched
        return "CONFLICT", None, undefeated
