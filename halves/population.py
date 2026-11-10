"""
The design of `PLAN_HALVES.md`: its asks and its sessions. **On the proposer's
path**, and it opens no record. The tickets are `plan.TICKETS`, fixed before any
figure of the plan existed, and `HV-g3` rebuilds them from the closed records.

  - **A prompt is an arm at a ticket**: 4 × 136 = 544, each asked once in each
    pass.
  - **The rarest queue's session** asks each of the 28 prompts at `plan.ONCALL`'s
    seven tickets `plan.ONCALL_REPEATS` times, each repetition its own ask.
  - **The smoke run** asks two prompts of each arm, at tickets outside the
    seven, drawn at `plan.order_rng("smoke")`.

Every session's order is a shuffle of its asks at its own seeded stream, so the
arms are interleaved in every session (§2.3).

NOTHING HERE READS A LABEL (rule B). A case is the corpus's, which carries the
ticket's attributes and nothing else.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from harness.domain import generate_corpus

from . import plan, prompts


@dataclass
class Design:
    tickets: tuple[int, ...]
    asks: dict[str, prompts.Ask]       # every ask of every session, by id
    sessions: dict[str, list[str]]

    def prompts_of(self, arm: str) -> list[prompts.Ask]:
        """An arm's prompts: its asks of the passes, one a ticket."""
        return [a for a in self.asks.values() if a.arm == arm and a.rep == 0]

    def summary(self) -> dict[str, Any]:
        """What Stage A's record carries, and what `halves/ask.py` checks a
        rebuilt design against before it spends."""
        return {"tickets": list(self.tickets),
                "asks": {i: {"arm": a.arm, "ticket": a.ticket, "rep": a.rep,
                             "digest": a.digest}
                         for i, a in sorted(self.asks.items())},
                "sessions": self.sessions}


def base_ids(tickets: tuple[int, ...]) -> list[str]:
    return [prompts.ask_id(arm, t) for t in tickets for arm in prompts.ARMS]


def oncall_ids() -> list[str]:
    return [prompts.ask_id(arm, t, k) for t in plan.ONCALL for arm in prompts.ARMS
            for k in range(1, plan.ONCALL_REPEATS + 1)]


def sessions_for(tickets: tuple[int, ...]) -> dict[str, list[str]]:
    """§2.3's four sessions: the smoke run's draw, each pass's order, and the
    rarest queue's session's order."""
    rng = plan.order_rng("smoke")
    outside = sorted(t for t in tickets if t not in plan.ONCALL)
    smoke: list[str] = []
    for arm in prompts.ARMS:
        smoke.extend(prompts.ask_id(arm, t) for t in rng.sample(outside, plan.SMOKE_PER_ARM))
    rng.shuffle(smoke)
    out = {"smoke": smoke}
    for session in plan.PASSES:
        order = sorted(base_ids(tickets))
        plan.order_rng(session).shuffle(order)
        out[session] = order
    order = sorted(oncall_ids())
    plan.order_rng("oncall").shuffle(order)
    out["oncall"] = order
    return out


@lru_cache(maxsize=None)
def build() -> Design:
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    asks: dict[str, prompts.Ask] = {}
    for t in plan.TICKETS:
        for arm in prompts.ARMS:
            a = prompts.ask(arm, t, corpus[t])
            asks[a.id] = a
    for t in plan.ONCALL:
        for arm in prompts.ARMS:
            for k in range(1, plan.ONCALL_REPEATS + 1):
                a = prompts.ask(arm, t, corpus[t], k)
                asks[a.id] = a
    return Design(tickets=plan.TICKETS, asks=asks, sessions=sessions_for(plan.TICKETS))
