"""
The three arms of `PLAN_QUEUE_ALONE.md`. **On the proposer's path.**

  t  the rule arm: `PLAN_APPLY.md`'s ticket arm, its system prompt and its user
     message as `apply.prompts` builds them, called and not rebuilt here. So
     its prompts are that plan's byte for byte, digest for digest.
  i  the impasse arm: §5.1's text with the impasse framing, asking for the
     queue alone.
  q  the plain arm: §5.1's text, asking for the queue alone, with no impasse.

THE NEW TEXTS ARE §5.1's, FROZEN BY THE SIGNATURE (hard rule 5). They are built
from v1's own blocks, word for word where they say the same thing:
- **`v1_block`** is cut out of `rung2.proposers2.SYSTEM_PROMPT_V1`, from its
  attributes to its actions, so it cannot drift from v1;
- **the manual's block** is `manual.prompts.block`'s, at levels 1 to 3;
- **the task** is v1's first item, *"decidir la cola de destino correcta para
  ESTE ticket"*;
- **the answer** is v1's answer cut to its first field, `action`.

The plain and impasse arms differ in two sentences of the system prompt and the
first line of the user message, and in nothing else. The impasse arm's user
message is the rule arm's without its empty-base line. `QA-g2` checks all three
claims. The texts are in Spanish, as v1's are, because they are prompt content.

NOTHING HERE TAKES A LABEL (rule B). A builder receives an arm, a level, a
ticket's name and its case, never a record's row. The policy reaches a prompt
only as `manual/levels.py`'s frozen text, through `manual.prompts.block` and
`apply.prompts.system_prompt`: this module imports neither the oracle nor any
name that carries the policy in code (`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from harness.domain import Case

from apply import prompts as aprompts
from manual import prompts as mprompts
from rung2.proposers2 import SYSTEM_PROMPT_V1, user_msg

RULE, IMPASSE, PLAIN = "t", "i", "q"
ARMS = (RULE, IMPASSE, PLAIN)
EMPTY_BASE = aprompts.EMPTY_BASE

# v1's attributes and actions, from the first line of the one to the last of
# the other: where v1's operators begin, the block ends.
V1_FROM = "ATRIBUTOS DISPONIBLES Y SUS DOMINIOS:"
V1_TO = "\n\nOPERADORES:"

# §5.1, verbatim.
PLAIN_HEAD = ("Eres el componente de enrutamiento de un sistema de triaje de tickets.\n\n"
              "Tu tarea: decidir la cola de destino correcta para ESTE ticket.")
IMPASSE_HEAD = ("Eres el componente de excepcion de un sistema de triaje de tickets.\n\n"
                "El motor simbolico no ha podido decidir este ticket. Tu tarea: decidir "
                "la cola de destino correcta para ESTE ticket.")
ANSWER = ("Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:\n\n"
          "{\n  \"action\": \"<accion para este ticket>\"\n}")
PLAIN_HEADER = "TICKET:\n"
IMPASSE_HEADER = "TICKET EN IMPASSE:\n"

# v1's retry, word for word, which `manual.prompts` already carries.
RETRY_MSG = mprompts.RETRY_MSG


def v1_block() -> str:
    """v1's attributes and actions, cut out of v1 itself."""
    s = SYSTEM_PROMPT_V1
    if s.count(V1_FROM) != 1 or s.count(V1_TO) != 1:
        raise ValueError("v1's block must be bounded exactly once")
    return s[s.index(V1_FROM):s.index(V1_TO)]


def system_prompt(arm: str, level: int) -> str:
    """An arm's system prompt at `level`. The rule arm's is `PLAN_APPLY.md`'s."""
    if arm == RULE:
        return aprompts.system_prompt(level)
    if arm not in (IMPASSE, PLAIN):
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    parts = [PLAIN_HEAD if arm == PLAIN else IMPASSE_HEAD, v1_block()]
    if level:
        parts.append(mprompts.block(level))
    parts.append(ANSWER)
    return "\n\n".join(parts)


def ticket_text(case: Case) -> str:
    """The ticket as v1 renders it in its user message."""
    return json.dumps(case.as_dict(), indent=2, default=str)


def user_message(arm: str, case: Case) -> str:
    """An arm's user message. The rule arm's is `PLAN_APPLY.md`'s: rung 2's
    message around v1's empty base."""
    if arm == RULE:
        return user_msg(case, EMPTY_BASE)
    if arm not in (IMPASSE, PLAIN):
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    return (PLAIN_HEADER if arm == PLAIN else IMPASSE_HEADER) + ticket_text(case)


def digest(system: str, user: str) -> str:
    """`apply.prompts.digest`'s formula over any system prompt, so that a rule-arm
    prompt carries the digest `PLAN_APPLY.md` recorded for it."""
    return hashlib.sha256((system + "\n\x00\n" + user).encode()).hexdigest()[:16]


def ask_id(arm: str, level: int, ticket: int) -> str:
    """`t:L3:17`, `i:L3:17` and `q:L3:17`. The rule arm's ids are
    `PLAN_APPLY.md`'s ticket arm's."""
    return f"{arm}:L{level}:{ticket}"


@dataclass(frozen=True)
class Ask:
    """One prompt of one arm, frozen."""
    id: str
    arm: str
    level: int
    ticket: int
    case: Case

    @property
    def system(self) -> str:
        return system_prompt(self.arm, self.level)

    @property
    def user(self) -> str:
        return user_message(self.arm, self.case)

    @property
    def digest(self) -> str:
        return digest(self.system, self.user)

    def messages(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": self.system},
                {"role": "user", "content": self.user}]


def ask(arm: str, level: int, ticket: int, case: Case) -> Ask:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    return Ask(id=ask_id(arm, level, ticket), arm=arm, level=level, ticket=ticket,
               case=case)
