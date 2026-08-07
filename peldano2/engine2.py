"""
Motor del peldano 2: arbitraje hibrido en dos niveles.

  NIVEL 1  SUBSUNCION (derivado de la semantica, no negociable)
           A ≺ B  sii  ext(A) ⊊ ext(B), sobre el espacio exhaustivo de 134.400
           combinaciones. Orden PARCIAL: deja pares incomparables.

  NIVEL 2  PRIORIDAD DECLARADA (autoria del proponente, validada)
           Aristas dirigidas entre reglas concretas: "A gana a B". Solo tienen
           efecto donde la subsuncion calla.

  Si tras ambos niveles quedan reglas invictas con acciones distintas -> CONFLICT.
  Abstenerse es correcto: en el peldano 1 la subsuncion dio error silencioso
  0,0000 precisamente porque se abstenia en vez de inventar.

FORMA DEL CAMPO DE PRIORIDAD: referencial, no entero global.

  {"beats": ["R0007"], "loses_to": ["R0021"]}

Justificacion, con las cifras del peldano 1:

  * Un entero global (nivel de capa) exige al proponente una decision GLOBAL a
    partir de una observacion LOCAL: ve un ticket y, como mucho, un puñado de
    reglas. Es la misma demanda que fallo en el peldano 1, con otro nombre.
  * La informacion que falta es pequeña y es PARCIAL, no total: sobre la politica
    oculta, 131 conjuntos minimales cubrian todo el residuo y ~50 desempates
    dirigidos daban 95% de e2e. Eso son relaciones entre pares, que es
    exactamente lo que una referencia expresa y un entero no.
  * Una referencia es VERIFICABLE mecanicamente: la regla citada existe, solapa,
    no contradice la subsuncion, no cierra un ciclo. Un entero es invalidable:
    cualquier numero pasa cualquier validador.
  * Una referencia COMPONE con la subsuncion (añade aristas al mismo grafo). Un
    entero COMPITE con ella: si el entero dice A>B y la subsuncion dice B ≺ A,
    no hay forma no arbitraria de arbitrar entre los dos arbitrajes.

Se admiten las dos direcciones (`beats` y `loses_to`) porque desde una
observacion local ambas son naturales: una regla puede nacer como excepcion de
una existente, o como defecto del que una existente es la excepcion. Son la
misma arista vista desde los dos extremos.

La subsuncion NO es sobreescribible por declaracion. Es la unica parte del orden
derivada de la semantica y no de la conjetura del proponente, y en el peldano 1
resulto sound (0 contradicciones sobre la politica oculta). Las aristas que la
contradicen se rechazan y se CUENTAN: si ese contador sale alto, la suposicion
es visiblemente falsa y hay que revisarla, no parchearla.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case
from harness.dsl import Condition, RuleValidationError

OPS = {"eq", "neq", "lte", "gte", "in"}


# ---------------------------------------------------------------------------
# Extensiones: mascaras de bits sobre el espacio exhaustivo
# ---------------------------------------------------------------------------

class Space:
    """El espacio completo de casos y las mascaras por (atributo, valor).
    Se construye una vez; calcular la extension de una regla es un AND de
    enteros grandes, no un barrido."""

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
# Regla
# ---------------------------------------------------------------------------

@dataclass
class Rule2:
    rule_id: str
    conditions: list[Condition]
    action: str
    born_at: int = -1
    fire_count: int = 0
    correct_count: int = 0          # solo registro; nunca se muestra al proponente
    note: str = ""
    beats: list[str] = field(default_factory=list)       # declaradas y ACEPTADAS
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
        """Como se le enseña al proponente. SIN correct_count: es del oraculo."""
        conds = " AND ".join(f"{c.attr} {c.op} {c.value}" for c in self.conditions)
        s = f"{self.rule_id}: SI {conds} ENTONCES {self.action}"
        if self.beats:
            s += f"  [gana a {', '.join(self.beats)}]"
        if self.loses_to:
            s += f"  [pierde con {', '.join(self.loses_to)}]"
        return s


# ---------------------------------------------------------------------------
# Validacion
# ---------------------------------------------------------------------------

def validate_conditions(payload: dict[str, Any], case: Case | None):
    """Mismas comprobaciones mecanicas que el peldano 1."""
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
# Motor
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
    Tres resultados, como el peldano 1: ACTION, IMPASSE, CONFLICT.

    beats(A, B) sii  ext(A) ⊊ ext(B)          [subsuncion, no negociable]
                 o   arista declarada A -> B  [prioridad declarada, validada]

    Gana el conjunto INVICTO: las reglas que ninguna otra que case derrota. Si
    coinciden en accion -> ACTION. Si discrepan -> CONFLICT. La transitividad
    sale gratis: si A gana a B y B gana a C, B y C quedan derrotadas y solo A
    queda invicta, sin calcular clausura.
    """

    space: Space
    rules: list[Rule2] = field(default_factory=list)
    ext: dict[str, int] = field(default_factory=dict)
    sub_below: dict[str, set[str]] = field(default_factory=dict)   # quien me subsume
    sub_above: dict[str, set[str]] = field(default_factory=dict)   # a quien subsumo
    decl_below: dict[str, set[str]] = field(default_factory=dict)  # quien me gana declarado
    decl_above: dict[str, set[str]] = field(default_factory=dict)  # a quien gano declarado
    edge_log: list[tuple[str, str, str]] = field(default_factory=list)
    _next_id: int = 1

    # -- construccion --------------------------------------------------------

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
        """¿src alcanza dst siguiendo aristas 'gana a'? (subsuncion + declaradas)"""
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
        """Instala 'winner gana a loser'. Devuelve el motivo si la rechaza."""
        if winner == loser:
            return EDGE_SELF
        if winner not in self.ext or loser not in self.ext:
            return EDGE_UNKNOWN
        ew, el = self.ext[winner], self.ext[loser]
        if ew & el == 0:
            return EDGE_DISJOINT            # no pueden competir jamas: inerte
        if strictly_below(el, ew):
            return EDGE_CONTRADICTS         # la subsuncion ya dice lo contrario
        if strictly_below(ew, el):
            return EDGE_OK                  # redundante pero consistente; se acepta
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
        if not undefeated:                  # solo posible con un ciclo colado
            return "CONFLICT", None, matched
        if len({r.action for r in undefeated}) == 1:
            return "ACTION", undefeated[0], matched
        return "CONFLICT", None, undefeated
