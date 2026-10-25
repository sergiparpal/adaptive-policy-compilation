"""
The four arms of `PLAN_REASONED_RULE.md`. **On the proposer's path.**

No prompt here is new (§5.1 of the plan). Each arm sends a closed plan's prompt
at level 3, built by `queue_alone.prompts`, called and not rebuilt here:

  t  the rule arm: `PLAN_QUEUE_ALONE.md`'s rule arm, which is `PLAN_APPLY.md`'s
     ticket arm: v1 with the manual's block, and v1's empty base around the
     ticket. Its ids and digests are that plan's.
  w  the reasoning rule arm: the rule arm's prompt byte for byte. It differs
     only in the request, which reasons (`reasoned_rule.plan.settings`).
  q  the plain arm: `PLAN_QUEUE_ALONE.md`'s plain arm, which is
     `PLAN_FIRST_MATCH.md`'s. Its ids and digests are both plans'.
  r  the reasoning arm: the plain arm's prompt byte for byte, with reasoning
     on, which is `PLAN_FIRST_MATCH.md`'s reasoning arm, ids included.

`asked_as` says which of `PLAN_QUEUE_ALONE.md`'s arms each one sends the prompt
of. `RR-g2` checks every claim above against the closed plans' records.

NOTHING HERE TAKES A LABEL (rule B). A builder receives an arm, a ticket's name
and its case, never a record's row. The policy reaches a prompt only as
`manual/levels.py`'s frozen text, through `queue_alone.prompts`, which reaches it
through `apply.prompts` and `manual.prompts.block`: this module imports neither
the oracle nor any name that carries the policy in code
(`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

from dataclasses import dataclass

from harness.domain import Case

from queue_alone import prompts as qprompts

RULE, REASONING_RULE, PLAIN, REASONING = "t", "w", "q", "r"
ARMS = (RULE, REASONING_RULE, PLAIN, REASONING)
RULE_ARMS = (RULE, REASONING_RULE)
LEVEL = 3

# v1's retry, word for word, which `queue_alone.prompts` already carries.
RETRY_MSG = qprompts.RETRY_MSG


def asked_as(arm: str) -> str:
    """The arm of `PLAN_QUEUE_ALONE.md` whose prompt `arm` sends."""
    if arm in RULE_ARMS:
        return qprompts.RULE
    if arm in (PLAIN, REASONING):
        return qprompts.PLAIN
    raise ValueError(f"no arm {arm!r}: {ARMS}")


def system_prompt(arm: str) -> str:
    """An arm's system prompt at level 3: `PLAN_QUEUE_ALONE.md`'s rule arm's for
    the two rule arms, its plain arm's for the other two."""
    return qprompts.system_prompt(asked_as(arm), LEVEL)


def user_message(arm: str, case: Case) -> str:
    """An arm's user message: the rule arm's for the two rule arms, v1's empty
    base around the ticket, and the plain arm's for the other two."""
    return qprompts.user_message(asked_as(arm), case)


def digest(system: str, user: str) -> str:
    """`PLAN_QUEUE_ALONE.md`'s formula, so that each prompt carries the digest
    that plan recorded for it."""
    return qprompts.digest(system, user)


def ask_id(arm: str, ticket: int) -> str:
    """`t:L3:17`, `w:L3:17`, `q:L3:17` and `r:L3:17`. The rule and plain arms'
    ids are `PLAN_QUEUE_ALONE.md`'s, and the plain and reasoning arms' are
    `PLAN_FIRST_MATCH.md`'s."""
    return qprompts.ask_id(arm, LEVEL, ticket)


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
