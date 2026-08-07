"""
Domain: support ticket triage.

Defines the case space, the action space and the sampling distribution
(deliberately long-tailed).

FROZEN. Do not touch without freezing a new version of the experiment.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Attribute space
# ---------------------------------------------------------------------------

# Fixed order. The mock proposers walk this list in this order, which
# represents the priority a reasonable analyst would give to the attributes.
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
    "severity": [1, 2, 3, 4],  # 1 = critical
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
# Sampling distribution (long tail)
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

# prior_tickets_30d: truncated geometric. Most in 0-1, tail out to 20.
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
        """Exact identity of the case, for measuring literal duplicates."""
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
    """Fixed, reproducible corpus. Generated once and never changed."""
    rng = random.Random(seed)
    return [sample_case(rng) for _ in range(n)]
