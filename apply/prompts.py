"""
The two arms of `PLAN_APPLY.md`, built with the functions that built the loop's
prompts. **On the proposer's path.**

Every prompt is what `PLAN_MANUAL.md`'s loop sent at some moment:
- **its system prompt** is `manual.prompts.loop_system_prompt` of the level,
  which is v1 with the level's manual inserted, and v1 to the byte at level 0;
- **its user message** is `rung2.proposers2.user_msg` around v1's rendering of a
  screen.

They are called, not copied (rule A of the plan). The arms differ only in that
screen:

  screen  the escalation's own: `fidelity.prompts.birth` at its moment, the
          conflicting rules on a CONFLICT and the nearest on a coverage
          impasse, exactly as the loop chose them.
  ticket  the ticket alone: v1's empty-base rendering, which is what case 0
          saw in every run (`fidelity.prompts.ticket_only`).

NOTHING HERE TAKES A LABEL (rule B). A builder receives a frozen prompt or a
ticket, never a record's row, and no prompt shows a count. The policy reaches a
prompt only as `manual/levels.py`'s frozen text, through
`manual.prompts.loop_system_prompt`: this module imports neither the oracle nor
any name that carries the policy in code (`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from harness.domain import Case

from fidelity import prompts as fprompts
from manual import prompts as mprompts
from rung2.proposers2 import user_msg

SCREEN, TICKET = "screen", "ticket"
ARMS = (SCREEN, TICKET)
COVERAGE, CONFLICT = fprompts.COVERAGE, fprompts.CONFLICT
EMPTY_BASE = fprompts.EMPTY_BASE


def system_prompt(level: int) -> str:
    """The loop's system prompt at `level`, `PLAN_MANUAL.md` §5.5's."""
    return mprompts.loop_system_prompt(level)


def digest(level: int, user: str) -> str:
    """What a record carries instead of the prompt: the system prompt and the
    user message, as `fidelity.prompts.Prompt.digest` joins them. At level 0 the
    two digests are the same string."""
    text = system_prompt(level) + "\n\x00\n" + user
    return hashlib.sha256(text.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class Ask:
    """One prompt of one arm, frozen. The rules a screen shows are kept as ids
    and actions; the live rules go on changing as the replay carries on."""
    id: str
    arm: str
    level: int
    case: Case
    screen: str
    shown_ids: tuple[str, ...]
    shown_actions: tuple[str, ...]
    base_text: str

    @property
    def system(self) -> str:
        return system_prompt(self.level)

    @property
    def user(self) -> str:
        return user_msg(self.case, self.base_text)

    @property
    def digest(self) -> str:
        return digest(self.level, self.user)


def screen_ask(ask_id: str, level: int, prompt: fprompts.Prompt) -> Ask:
    """The screen arm: an escalation's prompt as `fidelity.prompts.birth` rebuilt
    it at its moment, under the level's system prompt."""
    if prompt.kind != fprompts.BIRTH:
        raise ValueError(f"{ask_id}: a screen-arm prompt is a birth prompt, "
                         f"not {prompt.kind!r}")
    return Ask(id=ask_id, arm=SCREEN, level=level, case=prompt.case,
               screen=prompt.screen, shown_ids=prompt.shown_ids,
               shown_actions=prompt.shown_actions, base_text=prompt.base_text)


def ticket_ask(ask_id: str, level: int, case: Case) -> Ask:
    """The ticket arm: the ticket alone, under the level's system prompt."""
    p = fprompts.ticket_only(case)
    return Ask(id=ask_id, arm=TICKET, level=level, case=case, screen=p.screen,
               shown_ids=p.shown_ids, shown_actions=p.shown_actions,
               base_text=p.base_text)


def plurality(ask: Ask) -> str | None:
    """The screen's commonest action, a tie going to the action shown first:
    `fidelity.prompts.plurality`, called on the shown actions."""
    return fprompts.plurality(ask)


def first_shown(ask: Ask) -> str | None:
    return fprompts.first_shown(ask)
