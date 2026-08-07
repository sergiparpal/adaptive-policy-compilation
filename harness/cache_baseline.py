"""
Mandatory baseline: semantic cache.

It induces no rules. It stores seen cases and, faced with a new one, retrieves
the most similar by Hamming distance over the attributes. If the distance is
<= d, it reuses its action; otherwise it escalates.

It is the null hypothesis of the whole project: if this achieves 80% of the
saving at a fraction of the complexity, the rules have to justify their
existence.
"""

from __future__ import annotations

from typing import Any

from .domain import ATTRIBUTES, Case
from .hidden_policy import true_action


def _dist(a: Case, b: Case) -> int:
    return sum(1 for at in ATTRIBUTES if getattr(a, at) != getattr(b, at))


def run_cache_baseline(corpus: list[Case], max_dist: int) -> dict[str, Any]:
    store: list[tuple[Case, str]] = []
    escalations = 0
    hits = 0
    correct = 0
    n = len(corpus)

    for case in corpus:
        truth = true_action(case)  # only to label the record
        best, best_d = None, 10**9
        for prev, act in store:
            d = _dist(case, prev)
            if d < best_d:
                best, best_d = act, d
                if d == 0:
                    break

        if best is not None and best_d <= max_dist:
            hits += 1
            if best == truth:
                correct += 1
        else:
            escalations += 1
            store.append((case, truth))  # the LLM would have given the right action

    return {
        "name": f"cache(d<={max_dist})",
        "n_rules": len(store),
        "escalations": escalations,
        "escalation_rate": round(escalations / n, 4),
        "coverage": round(hits / n, 4),
        "silent_error_rate": round(1 - correct / hits, 4) if hits else None,
        "reuse_rate": None,
        "final_decile_escalation_rate": None,
        "dead_rules": 0,
    }
