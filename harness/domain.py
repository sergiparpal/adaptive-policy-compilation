"""
Dominio: triaje de tickets de soporte.

Define el espacio de casos, el espacio de acciones y la distribucion de
muestreo (deliberadamente de cola larga).

FROZEN. No tocar sin congelar una version nueva del experimento.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Espacio de atributos
# ---------------------------------------------------------------------------

# Orden fijo. Los proponentes mock recorren esta lista en este orden, que
# representa la prioridad que un analista razonable daria a los atributos.
ATTRIBUTES: list[str] = [
    "has_security_keyword",
    "severity",
    "customer_tier",
    "product",
    "channel",
    "prior_tickets_30d",
    "off_hours",
    "language",
]

DOMAINS: dict[str, Any] = {
    "customer_tier": ["free", "pro", "business", "enterprise"],
    "severity": [1, 2, 3, 4],  # 1 = critica
    "product": ["dashboard", "billing", "api", "mobile", "integrations"],
    "channel": ["portal", "email", "chat", "phone"],
    "off_hours": [False, True],
    "prior_tickets_30d": list(range(0, 21)),
    "has_security_keyword": [False, True],
    "language": ["en", "es", "pt", "de", "fr"],
}

NUMERIC_ATTRS = {"severity", "prior_tickets_30d"}

ACTIONS: list[str] = [
    "T1_GENERAL",
    "T2_TECHNICAL",
    "T3_ENGINEERING",
    "BILLING_SPECIALIST",
    "SECURITY_INCIDENT",
    "ACCOUNT_MANAGER",
    "ONCALL_ESCALATION",
    "SELF_SERVICE_DEFLECT",
]


# ---------------------------------------------------------------------------
# Distribucion de muestreo (cola larga)
# ---------------------------------------------------------------------------

_WEIGHTS: dict[str, list[float]] = {
    "customer_tier": [0.50, 0.30, 0.15, 0.05],
    "severity": [0.05, 0.20, 0.35, 0.40],
    "product": [0.30, 0.25, 0.20, 0.15, 0.10],
    "channel": [0.40, 0.35, 0.20, 0.05],
    "off_hours": [0.72, 0.28],
    "has_security_keyword": [0.97, 0.03],
    "language": [0.60, 0.20, 0.08, 0.07, 0.05],
}

# prior_tickets_30d: geometrica truncada. La mayoria en 0-1, cola hasta 20.
_PRIOR_WEIGHTS = [0.85 ** k for k in range(21)]


@dataclass(frozen=True)
class Case:
    has_security_keyword: bool
    severity: int
    customer_tier: str
    product: str
    channel: str
    prior_tickets_30d: int
    off_hours: bool
    language: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def key(self) -> tuple:
        """Identidad exacta del caso, para medir duplicados literales."""
        return tuple(getattr(self, a) for a in ATTRIBUTES)


def sample_case(rng: random.Random) -> Case:
    values: dict[str, Any] = {}
    for attr in ATTRIBUTES:
        if attr == "prior_tickets_30d":
            values[attr] = rng.choices(DOMAINS[attr], weights=_PRIOR_WEIGHTS, k=1)[0]
        else:
            values[attr] = rng.choices(DOMAINS[attr], weights=_WEIGHTS[attr], k=1)[0]
    return Case(**values)


def generate_corpus(n: int, seed: int) -> list[Case]:
    """Corpus fijo y reproducible. Se genera una vez y no cambia."""
    rng = random.Random(seed)
    return [sample_case(rng) for _ in range(n)]
