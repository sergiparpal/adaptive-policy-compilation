"""
Las 29 reglas ocultas con sus relaciones de prioridad DECLARADAS.

Aqui si conocemos el orden de capas, asi que las aristas se derivan de el. Pero
se declara el MINIMO, no un orden total: solo los pares que la subsuncion deja
sin resolver y que ademas pueden colisionar de verdad.

Una arista i -> j (capa i gana a capa j) se declara sii las tres cosas:

  1. las extensiones SOLAPAN sobre el espacio exhaustivo (pueden competir),
  2. son INCOMPARABLES por subsuncion (la subsuncion no lo resuelve ya),
  3. las ACCIONES DIFIEREN (si coinciden, da igual quien gane).

Declarar el orden total (406 pares) seria hacer trampa: mediria "¿funciona un
orden total?", cuya respuesta ya se conoce (100%, peldano 1). Lo que se mide
aqui es si subsuncion + el minimo de aristas declaradas basta. El numero de
aristas resultante es, ademas, el coste de autoria de esta politica: cuantas
relaciones tendria que declarar un autor perfecto por encima de lo que la
estructura ya dice sola.
"""

from __future__ import annotations

from harness.ceiling_check import HIDDEN_DSL
from harness.dsl import Condition

from .engine2 import PriorityEngine, Rule2, Space, strictly_below


def build_hidden_engine(space: Space | None = None):
    space = space or Space()
    engine = PriorityEngine(space=space)

    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        rule = Rule2(
            rule_id=rid,
            conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds],
            action=action,
            note="transcripcion literal de hidden_policy",
        )
        engine.add(rule, born_at=i, keep_id=True)

    # --- derivar las aristas minimas del orden de capas ---------------------
    rules = engine.rules
    declared = []
    skipped_disjoint = skipped_subsumed = skipped_same_action = 0
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            a, b = rules[i], rules[j]          # i < j  =>  a es de capa anterior
            ea, eb = engine.ext[a.rule_id], engine.ext[b.rule_id]
            if ea & eb == 0:
                skipped_disjoint += 1
                continue
            if strictly_below(ea, eb) or strictly_below(eb, ea):
                skipped_subsumed += 1
                continue
            if a.action == b.action:
                skipped_same_action += 1
                continue
            reason = engine.try_edge(a.rule_id, b.rule_id)
            engine.edge_log.append((a.rule_id, b.rule_id, reason))
            if reason == "ok":
                a.beats.append(b.rule_id)
                b.loses_to.append(a.rule_id)
                declared.append((a.rule_id, b.rule_id))

    stats = {
        "declared": len(declared),
        "skipped_disjoint": skipped_disjoint,
        "skipped_subsumed_by_structure": skipped_subsumed,
        "skipped_same_action": skipped_same_action,
        "rejected": [e for e in engine.edge_log if e[2] != "ok"],
    }
    return engine, declared, stats
