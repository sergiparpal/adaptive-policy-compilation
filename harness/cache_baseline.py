"""
Baseline obligatorio: cache semantica.

No induce reglas. Guarda casos vistos y, ante uno nuevo, recupera el mas
parecido por distancia de Hamming sobre los atributos. Si la distancia es <= d,
reutiliza su accion; si no, escala.

Es la hipotesis nula del proyecto entero: si esto consigue el 80% del ahorro con
una fraccion de la complejidad, las reglas tienen que justificar su existencia.
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
        truth = true_action(case)  # solo para etiquetar el registro
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
            store.append((case, truth))  # el LLM habria dado la accion correcta

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
