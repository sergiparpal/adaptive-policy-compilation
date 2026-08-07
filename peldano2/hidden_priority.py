"""
The 29 hidden rules with their DECLARED priority relations.

Here we do know the layer order, so the edges are derived from it. But the
MINIMUM is declared, not a total order: only the pairs subsumption leaves
unresolved and that can genuinely collide.

An edge i -> j (layer i beats layer j) is declared iff all three hold:

  1. the extensions OVERLAP over the exhaustive space (they can compete),
  2. they are INCOMPARABLE by subsumption (subsumption does not resolve it),
  3. the ACTIONS DIFFER (if they agree, it does not matter who wins).

Declaring the total order (406 pairs) would be cheating: it would measure "does
a total order work?", whose answer is already known (100%, rung 1). What is
measured here is whether subsumption + the minimum of declared edges suffices.
The resulting number of edges is, in addition, the authorship cost of this
policy: how many relations a perfect author would have to declare beyond what
the structure already says on its own.
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

    # --- derive the minimal edges from the layer order ----------------------
    rules = engine.rules
    declared = []
    skipped_disjoint = skipped_subsumed = skipped_same_action = 0
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            a, b = rules[i], rules[j]          # i < j  =>  a is from an earlier layer
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
