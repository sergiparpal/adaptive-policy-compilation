"""
The prompts of `PLAN_REASONED_RULE.md`, from `PLAN_QUEUE_ALONE.md`'s population
and nothing else.

WHAT IS REBUILT. `queue_alone.population.build` rebuilds `PLAN_APPLY.md`'s design,
which replays `PLAN_MANUAL.md`'s twelve loop records, called and not copied
(rule A). At level 3 it holds 171 rule prompts and 171 plain prompts, one of each
per escalated ticket of level 3's three runs. Each rule prompt becomes two here,
the rule arm's and the reasoning rule arm's, and each plain prompt two, the
plain arm's and the reasoning arm's, on the same ticket.

WHAT EACH PROMPT SERVES is the closed plan's prompt's own decisions at level 3:
the escalations of level 3 with a screen whose ticket it is. Every arm's prompt
on a ticket serves the same decisions.

THE SESSIONS (§1). The smoke run draws two tickets in each arm at
`ORDER_SEED`. Each pass asks every prompt of the four arms once, in its own
seeded order, the arms interleaved (§2.5).

NOTHING HERE READS A LABEL. `queue_alone.population` builds on
`apply.population`, which reads each row's `correct` to keep each rule's counts,
as the loop did. Nothing this module returns carries `truth` or the loop's
answer: Stage C joins those from the records itself (rule B).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from apply import population as apop
from queue_alone import population as qpop

from . import plan, prompts


@dataclass
class Design:
    queue_alone: qpop.Design
    asks: dict[str, prompts.Ask]
    serves: dict[str, list[str]]
    sessions: dict[str, list[str]]

    @property
    def decisions(self) -> dict[str, apop.Escalation]:
        """Level 3's decisions, the only ones this plan reads."""
        return {i: e for i, e in self.queue_alone.decisions.items() if e.level == plan.LEVEL}

    def asks_of(self, arm: str) -> list[prompts.Ask]:
        return [a for a in self.asks.values() if a.arm == arm]

    def summary(self) -> dict[str, Any]:
        """What Stage A's record carries, and what `reasoned_rule/ask.py` checks a
        rebuilt design against before it spends."""
        decisions = {i: {"level": e.level, "run": e.run, "idx": e.idx, "ticket": e.ticket}
                     for i, e in sorted(self.decisions.items())}
        asks = {i: {"arm": a.arm, "level": a.level, "ticket": a.ticket,
                    "digest": a.digest, "serves": self.serves[i]}
                for i, a in sorted(self.asks.items())}
        return {"decisions": decisions, "asks": asks, "sessions": self.sessions}


def sessions_for(asks: dict[str, prompts.Ask]) -> dict[str, list[str]]:
    """§1's three sessions: the smoke run's draw, and each pass's order."""
    rng = plan.order_rng("smoke")
    smoke: list[str] = []
    for arm in prompts.ARMS:
        here = sorted(i for i, a in asks.items() if a.arm == arm)
        smoke.extend(rng.sample(here, plan.SMOKE_PER_ARM))
    rng.shuffle(smoke)
    out = {"smoke": smoke}
    for session in plan.SESSIONS[1:]:
        order = sorted(asks)
        plan.order_rng(session).shuffle(order)
        out[session] = order
    return out


@lru_cache(maxsize=None)
def build() -> Design:
    """The whole design, from `PLAN_QUEUE_ALONE.md`'s. Cached, as that one is."""
    design = qpop.build()
    asks: dict[str, prompts.Ask] = {}
    serves: dict[str, list[str]] = {}
    for aid, a in sorted(design.asks.items()):
        if a.level != plan.LEVEL:
            continue
        for arm in prompts.ARMS:
            if prompts.asked_as(arm) != a.arm:
                continue
            x = prompts.ask(arm, a.ticket, a.case)
            asks[x.id] = x
            serves[x.id] = list(design.serves[aid]["own"])
    return Design(queue_alone=design, asks=asks, serves=serves, sessions=sessions_for(asks))
