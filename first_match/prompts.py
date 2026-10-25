"""
The three arms of `PLAN_FIRST_MATCH.md`. **On the proposer's path.**

  q  the plain arm: `PLAN_QUEUE_ALONE.md`'s plain arm at level 3, its system
     prompt and its user message as `queue_alone.prompts` builds them, called
     and not rebuilt here. So its prompts are that plan's byte for byte, digest
     for digest, and its ids are that plan's too.
  n  the naming arm: the plain arm's prompt with §5.1's line added to the
     answer's template, asking for the identifier of the rule that applies
     before the queue.
  r  the reasoning arm: the plain arm's prompt byte for byte. It differs only
     in the request, which reasons (`first_match.plan.settings`).

THE NEW TEXT IS §5.1's, FROZEN BY THE SIGNATURE (hard rule 5). `NAMING_ANSWER` is
`PLAIN_ANSWER`, `PLAN_QUEUE_ALONE.md`'s answer, with `NAMING_LINE` added before
its one field. Everything above the answer is the plain arm's, and so is the
user message. `FM-g2` checks both claims.

WHICH RULE AN ANSWER NAMES. `named_rule` reads a naming-arm answer's `rule` field
as §0 defines it: one of the identifiers `H01` to `H29` at its start, with no
digit after it. The identifiers are the list's names, not its rules: they say
nothing about what any rule decides. `FM-g1` holds them to level 3's text
through `PLAN_QUEUE_ALONE.md`'s checks.

NOTHING HERE TAKES A LABEL (rule B). A builder receives an arm, a ticket's name
and its case, never a record's row. The policy reaches a prompt only as
`manual/levels.py`'s frozen text, through `queue_alone.prompts` and
`manual.prompts.block`: this module imports neither the oracle nor any name that
carries the policy in code (`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from harness.domain import Case

from queue_alone import prompts as qprompts

PLAIN, NAMING, REASONING = "q", "n", "r"
ARMS = (PLAIN, NAMING, REASONING)
LEVEL = 3

# `PLAN_QUEUE_ALONE.md` §5.1's answer, and §5.1's, verbatim.
PLAIN_ANSWER = qprompts.ANSWER
NAMING_LINE = '  "rule": "<identificador de la regla que se aplica a este ticket>",'
NAMING_ANSWER = ("Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:\n\n"
                 "{\n  \"rule\": \"<identificador de la regla que se aplica a este ticket>\",\n"
                 "  \"action\": \"<accion para este ticket>\"\n}")

# v1's retry, word for word, which `queue_alone.prompts` already carries.
RETRY_MSG = qprompts.RETRY_MSG

# The list's names, `H01` to `H29`, and how an answer's field names one.
IDENTIFIERS = tuple(f"H{k:02d}" for k in range(1, 30))
NAMED = re.compile(r"(H\d{2})(?!\d)")


def system_prompt(arm: str) -> str:
    """An arm's system prompt at level 3. The plain and reasoning arms' is
    `PLAN_QUEUE_ALONE.md`'s plain arm's."""
    plain = qprompts.system_prompt(qprompts.PLAIN, LEVEL)
    if arm in (PLAIN, REASONING):
        return plain
    if arm != NAMING:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    if not plain.endswith(PLAIN_ANSWER):
        raise ValueError("the plain arm's prompt must end with its answer")
    return plain[: -len(PLAIN_ANSWER)] + NAMING_ANSWER


def user_message(arm: str, case: Case) -> str:
    """Every arm's user message is the plain arm's: `TICKET:` and the ticket."""
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    return qprompts.user_message(qprompts.PLAIN, case)


def digest(system: str, user: str) -> str:
    """`PLAN_QUEUE_ALONE.md`'s formula, so that a plain-arm prompt carries the
    digest that plan recorded for it."""
    return qprompts.digest(system, user)


def ask_id(arm: str, ticket: int) -> str:
    """`q:L3:17`, `n:L3:17` and `r:L3:17`. The plain arm's ids are
    `PLAN_QUEUE_ALONE.md`'s plain arm's."""
    return qprompts.ask_id(arm, LEVEL, ticket)


def named_rule(field: Any) -> str | None:
    """The identifier a naming-arm answer names, as §0 defines it, or `None`."""
    if not isinstance(field, str):
        return None
    m = NAMED.match(field.strip())
    return m.group(1) if m and m.group(1) in IDENTIFIERS else None


@dataclass(frozen=True)
class Ask:
    """One prompt of one arm, frozen."""
    id: str
    arm: str
    ticket: int
    case: Case

    @property
    def level(self) -> int:
        return LEVEL

    @property
    def system(self) -> str:
        return system_prompt(self.arm)

    @property
    def user(self) -> str:
        return user_message(self.arm, self.case)

    @property
    def digest(self) -> str:
        return digest(self.system, self.user)

    def messages(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": self.system},
                {"role": "user", "content": self.user}]


def ask(arm: str, ticket: int, case: Case) -> Ask:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    return Ask(id=ask_id(arm, ticket), arm=arm, ticket=ticket, case=case)
