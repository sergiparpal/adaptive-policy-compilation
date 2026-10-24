"""
The prompts of `PLAN_QUEUE_ALONE.md`, from `PLAN_APPLY.md`'s population and
nothing else.

WHAT IS REBUILT. `apply.population.build` replays `PLAN_MANUAL.md`'s twelve loop
records, called and not copied (rule A). Its design holds the decisions, the
tickets, and the ticket arm's 676 prompts: 275 at level 0, on every escalated
ticket, and each level's own tickets at levels 1 to 3. Each of those prompts
becomes three here, one per arm, on the same level and ticket.

WHAT EACH PROMPT SERVES is `PLAN_APPLY.md`'s ticket arm's:
- **`own`**: the decisions of its level on its ticket, which read it as their
  `t`, `i` or `q`;
- **`zero`**: at level 0, every decision of any level on its ticket, which read
  it as their `t⁰`, `i⁰` or `q⁰`.

THE SESSIONS (§1). The smoke run draws, at each level, one ticket in each arm at
`ORDER_SEED`. Each pass asks every prompt of the three arms once, in its own
seeded order, the arms interleaved (§2.4).

NOTHING HERE READS A LABEL. `apply.population` reads each row's `correct` to
keep each rule's counts, as the loop did, and nothing this module returns
carries `truth` or the loop's answer: Stage C joins those from the records
itself (rule B).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from apply import population as apop
from apply import prompts as aprompts

from . import plan, prompts


@dataclass
class Design:
    apply: apop.Design
    asks: dict[str, prompts.Ask]
    serves: dict[str, dict[str, list[str]]]
    sessions: dict[str, list[str]]

    @property
    def decisions(self) -> dict[str, apop.Escalation]:
        return self.apply.decisions

    def asks_of(self, arm: str, level: int) -> list[prompts.Ask]:
        return [a for a in self.asks.values() if a.arm == arm and a.level == level]

    def summary(self) -> dict[str, Any]:
        """What Stage A's record carries, and what `queue_alone/ask.py` checks a
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
    for lv in plan.LEVELS:
        for arm in prompts.ARMS:
            here = sorted(i for i, a in asks.items() if a.arm == arm and a.level == lv)
            for _ in range(plan.SMOKE_PER_ARM_AND_LEVEL):
                smoke.append(rng.choice(here))
    rng.shuffle(smoke)
    out = {"smoke": smoke}
    for session in plan.SESSIONS[1:]:
        order = sorted(asks)
        plan.order_rng(session).shuffle(order)
        out[session] = order
    return out


@lru_cache(maxsize=None)
def build() -> Design:
    """The whole design, from `PLAN_APPLY.md`'s. Cached, as that one is."""
    design = apop.build()
    asks: dict[str, prompts.Ask] = {}
    serves: dict[str, dict[str, list[str]]] = {}
    for aid, a in sorted(design.asks.items()):
        if a.arm != aprompts.TICKET:
            continue
        ticket = apop.ticket_of(a.case)
        for arm in prompts.ARMS:
            x = prompts.ask(arm, a.level, ticket, a.case)
            asks[x.id] = x
            serves[x.id] = {"own": list(design.serves[aid]["t"]),
                            "zero": list(design.serves[aid]["u"])}
    return Design(apply=design, asks=asks, serves=serves, sessions=sessions_for(asks))
