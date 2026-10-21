"""
A compile answer of `PLAN_MANUAL.md`'s shape C, parsed and installed into rung
2's engine.

The answer is a list of rules in an order. **The order stands for the
declaration**, by `rung2/hidden_priority.py`'s own rule, applied to whatever
list the model wrote: for every pair, the earlier rule is declared to beat the
later one iff the two overlap over the exhaustive space, neither contains the
other, and their actions differ. Containment is left to subsumption, which
decides first in rung 2's engine whatever the list says, and agreeing actions
need no winner. That is the derivation that turns the hidden policy's layer
order into its 199 edges, and `G-g1` checks that, applied to the hidden policy
written as an answer, it gives back exactly those edges and a ceiling of 1.0000
on both surfaces.

A rule that fails rung 2's validation is rejected and counted, as the loop
counts the rules it rejects, and the rest of the list is installed in its
order. A cycle the derivation would close is refused by the engine and logged,
as every declared edge's fate is logged in the loop. **What the model wrote is
recorded and never repaired** (§4, rule E).

Nothing here reads the oracle. The answer is installed as a deployment would
install it; scoring it is `manual/instrument.py`'s.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from harness.dsl import RuleValidationError
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space, strictly_below, validate_conditions


@dataclass
class Installed:
    """One answer, installed. `rules` are the ones the engine took, in the
    answer's order; `rejected` says where the others were and why."""
    engine: PriorityEngine
    rules: list[Rule2]
    rejected: list[dict[str, Any]] = field(default_factory=list)
    positions: list[int] = field(default_factory=list)   # answer position of each rule

    @property
    def edges(self) -> list[tuple[str, str, str]]:
        return list(self.engine.edge_log)

    def summary(self) -> dict[str, Any]:
        reasons: dict[str, int] = {}
        for _, _, why in self.engine.edge_log:
            reasons[why] = reasons.get(why, 0) + 1
        return {"rules_in_answer": len(self.rules) + len(self.rejected),
                "rules_installed": len(self.rules),
                "rules_rejected": len(self.rejected),
                "edges_derived": len(self.engine.edge_log),
                "edges_by_verdict": reasons}


def rules_of(payload: Any) -> tuple[list[Any], str | None]:
    """The answer's list of rules, or why it has none. An answer without a
    list is an invalid ask (§0); an empty list is one too."""
    if not isinstance(payload, dict):
        return [], "la respuesta no es un objeto JSON"
    raw = payload.get("rules")
    if not isinstance(raw, list):
        return [], "la respuesta no trae una lista 'rules'"
    if not raw:
        return [], "la lista 'rules' esta vacia"
    return raw, None


def derive_edges(engine: PriorityEngine, rules: list[Rule2]) -> None:
    """`rung2/hidden_priority.py`'s derivation over `rules` in their order."""
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            a, b = rules[i], rules[j]
            ea, eb = engine.ext[a.rule_id], engine.ext[b.rule_id]
            if ea & eb == 0:
                continue                       # they never meet
            if strictly_below(ea, eb) or strictly_below(eb, ea):
                continue                       # subsumption decides
            if a.action == b.action:
                continue                       # nothing to decide
            why = engine.try_edge(a.rule_id, b.rule_id)
            engine.edge_log.append((a.rule_id, b.rule_id, why))
            if why == EDGE_OK:
                a.beats.append(b.rule_id)
                b.loses_to.append(a.rule_id)


def install(raw_rules: list[Any], space: Space | None = None) -> Installed:
    """Validate each rule as rung 2 does, add the valid ones in the answer's
    order, then derive the edges from that order."""
    engine = PriorityEngine(space=space or Space())
    rules: list[Rule2] = []
    rejected: list[dict[str, Any]] = []
    positions: list[int] = []
    for pos, raw in enumerate(raw_rules):
        try:
            rule = validate_conditions(raw if isinstance(raw, dict) else {}, case=None)
        except RuleValidationError as exc:
            rejected.append({"position": pos, "reason": str(exc)})
            continue
        engine.add(rule, born_at=pos)
        rules.append(rule)
        positions.append(pos)
    derive_edges(engine, rules)
    return Installed(engine=engine, rules=rules, rejected=rejected, positions=positions)


def inversions(installed: Installed) -> list[tuple[str, str]]:
    """Pairs where the list puts a rule above one it strictly contains, with a
    different action: there rung 2's engine lets the contained rule win, and a
    first-match reading of the same list would not. Reported, never repaired."""
    eng, rules = installed.engine, installed.rules
    out = []
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            a, b = rules[i], rules[j]
            if a.action != b.action and strictly_below(eng.ext[b.rule_id], eng.ext[a.rule_id]):
                out.append((a.rule_id, b.rule_id))
    return out
