"""
The three prompts of `PLAN_FIDELITY.md`, built with rung 2's own functions.

Every prompt is prompt v1 exactly as `rung2/proposers2.py` builds it: its system
prompt, and `user_msg` around `render_base_v1` of a screen that `neighbourhood`
chose. Called, not copied (rule A of the plan). The three differ only in which
rules the screen is chosen from:

  birth        the base at that moment, as the loop chose it: the conflicting
               rules on a CONFLICT, the nearest on a coverage impasse. `F-a`.
  hidden       design B of §2.1: the base at that moment with every rule that
               matches the ticket left out, so the case is the coverage impasse
               it would have been had no rule covered it. `F-b` to `F-e`.
  ticket_only  design C: v1 with an empty base, which is what case 0 saw in
               every run. It depends on the ticket alone. `F-f`.

`check_hidden` and `check_ticket_only` are the prompt half of `F-g3`. On a B
screen no rule matches its ticket, the header is v1's coverage header and the
deciding rule is never shown. A ticket-only prompt is the empty-base rendering.

NOTHING HERE TAKES A LABEL. A builder receives the base and the ticket, never a
record row, because a builder that could see `truth` could leak it (§6, `F-g3`).
The headers below are rendered by v1's own renderer, not retyped.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import SimpleNamespace

from harness.domain import Case
from harness.dsl import Condition

from rung2.engine2 import Rule2
from rung2.proposers2 import SYSTEM_PROMPT_V1, neighbourhood, render_base_v1, user_msg

BIRTH, HIDDEN, TICKET_ONLY = "birth", "hidden", "ticket_only"
KINDS = (BIRTH, HIDDEN, TICKET_ONLY)
COVERAGE, CONFLICT = "vecindario", "conflicto"

_PROBE = Rule2(rule_id="R0000", conditions=[Condition("severity", "eq", 1)],
               action="T1_GENERAL")
COVERAGE_HEADER = render_base_v1([_PROBE], COVERAGE).splitlines()[0]
EMPTY_BASE = render_base_v1([], COVERAGE)


@dataclass
class Prompt:
    """One prompt, frozen at the moment it was built. The rules on its screen
    are kept as ids and actions: the live rules go on changing as the rebuild
    carries on."""
    kind: str
    case: Case
    screen: str
    shown_ids: tuple[str, ...]
    shown_actions: tuple[str, ...]
    base_text: str

    @property
    def user(self) -> str:
        return user_msg(self.case, self.base_text)

    @property
    def chars(self) -> int:
        """System prompt included, as §0 measured it."""
        return len(SYSTEM_PROMPT_V1) + len(self.user)

    @property
    def digest(self) -> str:
        """What a record carries instead of the prompt (§8)."""
        text = SYSTEM_PROMPT_V1 + "\n\x00\n" + self.user
        return hashlib.sha256(text.encode()).hexdigest()[:16]


def _build(kind: str, case: Case, shown: list[Rule2], screen: str) -> Prompt:
    return Prompt(kind=kind, case=case, screen=screen,
                  shown_ids=tuple(r.rule_id for r in shown),
                  shown_actions=tuple(r.action for r in shown),
                  base_text=render_base_v1(shown, screen))


def birth(engine, case: Case, undefeated: list[Rule2]) -> Prompt:
    """The prompt the loop built at an escalation, rebuilt."""
    shown, screen = neighbourhood(engine, case, undefeated)
    return _build(BIRTH, case, shown, screen)


def hidden(engine, case: Case) -> Prompt:
    """Design B: every rule that matches the ticket left out of the base."""
    view = SimpleNamespace(rules=[r for r in engine.rules if not r.matches(case)])
    shown, screen = neighbourhood(view, case, [])
    return _build(HIDDEN, case, shown, screen)


def ticket_only(case: Case) -> Prompt:
    """Design C: v1 with an empty base."""
    return _build(TICKET_ONLY, case, [], COVERAGE)


def check_hidden(prompt: Prompt, engine, deciding_rule_id: str) -> list[str]:
    """The prompt half of `F-g3` for one B prompt."""
    problems = []
    by_id = {r.rule_id: r for r in engine.rules}
    if any(by_id[i].matches(prompt.case) for i in prompt.shown_ids):
        problems.append("a rule on the screen matches the ticket")
    if deciding_rule_id in prompt.shown_ids:
        problems.append("the deciding rule is on the screen")
    if prompt.screen != COVERAGE:
        problems.append(f"the screen is {prompt.screen}, not a coverage screen")
    if not (prompt.base_text.startswith(COVERAGE_HEADER + "\n")
            or prompt.base_text == EMPTY_BASE):
        problems.append("the header is not v1's coverage header")
    return problems


def check_ticket_only(prompt: Prompt) -> list[str]:
    if prompt.shown_ids or prompt.base_text != EMPTY_BASE:
        return ["a ticket-only prompt is not v1's empty-base rendering"]
    return []


def plurality(prompt: Prompt) -> str | None:
    """Stage A's first baseline: the commonest action on the screen, a tie going
    to the action shown first (§7). None on an empty screen."""
    if not prompt.shown_actions:
        return None
    counts: dict[str, int] = {}
    for a in prompt.shown_actions:
        counts[a] = counts.get(a, 0) + 1
    top = max(counts.values())
    return next(a for a in prompt.shown_actions if counts[a] == top)


def first_shown(prompt: Prompt) -> str | None:
    """Stage A's second baseline: the action of the rule shown first."""
    return prompt.shown_actions[0] if prompt.shown_actions else None
