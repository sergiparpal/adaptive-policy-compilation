"""
The population of `PLAN_APPLY.md` §0, rebuilt from `PLAN_MANUAL.md`'s twelve loop
records and nothing else.

WHAT IS REBUILT. Each record is replayed with `fidelity.replay.Replay`, called
and not copied (rule A): a fresh rung 2 engine decides each case, and every rule
born at an escalation is added under its own id with its edges tried in the
logged order. At every escalation the prompt the loop built is rebuilt by
`fidelity.prompts.birth`, at the moment before the case changes the base.
`X-g1` holds the replay to the record and `X-g2` holds every screen to the
row's `shown_ids` and `shown_kind`.

THE UNITS, as §0 defines them.

  escalation  every escalation of a run, 790 of them, keyed `L{k}r{r}:{idx}`.
  decision    an escalation whose screen is not empty: 778. The twelve with an
              empty screen are case 0 of every run, and enter no row.
  ticket      `Case.key()`, named by the first index of the corpus whose case
              has those attributes, so that a ticket has one name at every
              level.

THE ASKS. One screen-arm ask per decision, `s:L{k}r{r}:{idx}`. One ticket-arm
ask per ticket a level escalated, `t:L{k}:{ticket}`, and at level 0 one per
ticket any level escalated: 676 in all. A ticket ask at level `k` serves the
decisions of level `k` on its ticket as their `t`. At level 0 it also serves
every other level's decisions on its ticket as their `u`.

THE SESSIONS (§1). The smoke run draws, at each level, one decision and one
ticket at `ORDER_SEED`. Each pass asks every ask of both arms once, in its own
seeded order, the arms interleaved (§2.3).

NOTHING HERE READS A LABEL. The replay reads each row's `correct` to keep each
rule's counts, as the loop did, and its `edge_reasons` to replay the edges. No
prompt shows a count, and nothing this module returns carries `truth` or the
loop's answer: Stage C joins those from the records itself (rule B).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from harness.domain import Case, generate_corpus

from fidelity import prompts as fprompts
from fidelity.replay import Replay
from rung2.engine2 import Space

from . import plan, prompts


@lru_cache(maxsize=None)
def corpus() -> tuple[Case, ...]:
    return tuple(generate_corpus(plan.N, seed=plan.SEED))


@lru_cache(maxsize=None)
def space() -> Space:
    return Space()


@lru_cache(maxsize=None)
def ticket_names() -> dict[tuple, int]:
    """`{Case.key(): the first corpus index with that key}`."""
    out: dict[tuple, int] = {}
    for i, c in enumerate(corpus()):
        out.setdefault(c.key(), i)
    return out


def ticket_of(case: Case) -> int:
    return ticket_names()[case.key()]


def record(level: int, rep: int) -> dict[str, Any]:
    """One loop record, read-only (rule B)."""
    return json.loads(plan.loop_record(level, rep).read_text())


def escalation_id(level: int, rep: int, idx: int) -> str:
    return f"L{level}r{rep}:{idx}"


def screen_ask_id(decision_id: str) -> str:
    return f"s:{decision_id}"


def ticket_ask_id(level: int, ticket: int) -> str:
    return f"t:L{level}:{ticket}"


@dataclass(frozen=True)
class Escalation:
    """One escalation, at the moment the loop asked about it. `recorded` is what
    the row says the loop showed: its `shown_ids`, its `shown_kind`, and
    whether it escalated. None of it is a label."""
    id: str
    level: int
    run: int
    idx: int
    ticket: int
    outcome: str
    prompt: fprompts.Prompt
    recorded: tuple[tuple[str, ...], str, bool]

    @property
    def has_screen(self) -> bool:
        return bool(self.prompt.shown_ids)


def escalations_of(level: int, rep: int, rec: dict[str, Any]) -> list[Escalation]:
    """Every escalation of one run, with the prompt the loop built at it."""
    out = []
    rp = Replay(rec, list(corpus()), space())
    for m in rp.moments():
        if m.outcome == "ACTION":
            continue
        p = fprompts.birth(m.engine, m.case, m.undefeated)
        out.append(Escalation(
            id=escalation_id(level, rep, m.idx), level=level, run=rep, idx=m.idx,
            ticket=ticket_of(m.case), outcome=m.outcome, prompt=p,
            recorded=(tuple(m.row["shown_ids"]), m.row["shown_kind"],
                      bool(m.row["escalated"]))))
    return out


@dataclass
class Design:
    escalations: dict[str, Escalation]
    asks: dict[str, prompts.Ask]
    serves: dict[str, dict[str, list[str]]]
    sessions: dict[str, list[str]]

    @property
    def decisions(self) -> dict[str, Escalation]:
        return {i: e for i, e in self.escalations.items() if e.has_screen}

    @property
    def empty(self) -> list[str]:
        return [i for i, e in self.escalations.items() if not e.has_screen]

    def decisions_at(self, level: int) -> list[Escalation]:
        return [e for e in self.decisions.values() if e.level == level]

    def tickets_at(self, level: int) -> set[int]:
        return {e.ticket for e in self.escalations.values() if e.level == level}

    def summary(self) -> dict[str, Any]:
        """What Stage A's record carries, and what `apply/ask.py` checks a
        rebuilt design against before it spends."""
        decisions = {}
        for i, e in self.decisions.items():
            a = self.asks[screen_ask_id(i)]
            decisions[i] = {"level": e.level, "run": e.run, "idx": e.idx,
                            "ticket": e.ticket, "kind": e.prompt.screen,
                            "outcome": e.outcome, "shown_ids": list(a.shown_ids),
                            "plurality": prompts.plurality(a),
                            "first_shown": prompts.first_shown(a)}
        asks = {i: {"arm": a.arm, "level": a.level, "ticket": ticket_of(a.case),
                    "digest": a.digest, "serves": self.serves[i]}
                for i, a in self.asks.items()}
        return {"decisions": decisions, "empty": self.empty, "asks": asks,
                "sessions": self.sessions}


def sessions_for(decisions: dict[str, Escalation], asks: dict[str, prompts.Ask]
                 ) -> dict[str, list[str]]:
    """§1's three sessions: the smoke run's draw, and each pass's order."""
    rng = plan.order_rng("smoke")
    smoke: list[str] = []
    for lv in plan.LEVELS:
        here = sorted(i for i, e in decisions.items() if e.level == lv)
        tickets = sorted(i for i, a in asks.items()
                         if a.arm == prompts.TICKET and a.level == lv)
        for _ in range(plan.SMOKE_PER_ARM_AND_LEVEL):
            smoke.append(screen_ask_id(rng.choice(here)))
            smoke.append(rng.choice(tickets))
    rng.shuffle(smoke)
    out = {"smoke": smoke}
    for session in plan.SESSIONS[1:]:
        order = sorted(asks)
        plan.order_rng(session).shuffle(order)
        out[session] = order
    return out


@lru_cache(maxsize=None)
def build() -> Design:
    """The whole design, from the twelve records. Cached: a replay of the twelve
    takes a few seconds, and nothing it reads may change while it runs."""
    escalations: dict[str, Escalation] = {}
    for lv in plan.LEVELS:
        for rep in range(1, plan.REPS + 1):
            for e in escalations_of(lv, rep, record(lv, rep)):
                escalations[e.id] = e
    decisions = {i: e for i, e in escalations.items() if e.has_screen}

    asks: dict[str, prompts.Ask] = {}
    serves: dict[str, dict[str, list[str]]] = {}
    for i, e in sorted(decisions.items()):
        aid = screen_ask_id(i)
        asks[aid] = prompts.screen_ask(aid, e.level, e.prompt)
        serves[aid] = {"s": [i], "t": [], "u": []}

    cases = {e.ticket: e.prompt.case for e in escalations.values()}
    for lv in plan.LEVELS:
        tickets = (set(cases) if lv == 0
                   else {e.ticket for e in escalations.values() if e.level == lv})
        for t in sorted(tickets):
            aid = ticket_ask_id(lv, t)
            asks[aid] = prompts.ticket_ask(aid, lv, cases[t])
            own = sorted(i for i, e in decisions.items()
                         if e.level == lv and e.ticket == t)
            others = (sorted(i for i, e in decisions.items()
                             if e.level != 0 and e.ticket == t) if lv == 0 else [])
            serves[aid] = {"s": [], "t": own, "u": own + others if lv == 0 else []}

    return Design(escalations=escalations, asks=asks, serves=serves,
                  sessions=sessions_for(decisions, asks))
