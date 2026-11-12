"""
The at-once asks' messages — §2.4 and §5.3 of `PLAN_CORRECTIONS.md`. **On the
proposer's path**: it builds prompts that carry labels, the ones arm `l`'s
proposer was handed and no others. Nothing here imports the policy in code (§4).

THE SYSTEM PROMPT is `PLAN_MANUAL.md`'s shape C at level 1:
`manual.prompts.compile_system_prompt(1)`, the catalogue in the compile prompt.

THE USER MESSAGE is the header, one line per labelled ticket in arrival order,
and `PLAN_MANUAL.md`'s request, `manual.prompts.COMPILE_USER`, byte for byte.
With no label it is that request alone, and the messages are
`manual.prompts.compile_messages(1)` exactly. A line is the ticket's fields as
the loop shows them, on one line, and its queue under `cola_correcta`.

THE REQUEST is the loop's, `placement.protocol.request_with` with DeepInfra's
pin, with one change: the budget, `plan.AT_ONCE_MAX_TOKENS`.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from harness.domain import ACTIONS

from manual import prompts as mprompts
from placement import protocol as pl_protocol

from . import plan

SYSTEM_PROMPT = mprompts.compile_system_prompt(plan.LEVEL)
COMPILE_USER = mprompts.COMPILE_USER
HEADER = """CORRECCIONES DE REVISORES: el sistema decidio mal cada uno de estos
tickets, y un revisor le dio su cola correcta.
"""


class NotAQueue(ValueError):
    """A line that would name something other than one of the eight queues."""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def ticket_line(case, queue: str) -> str:
    """One labelled ticket: its fields as the loop shows them, on one line,
    and its queue."""
    if queue not in ACTIONS:
        raise NotAQueue(f"{queue!r} is not one of the eight queues")
    return json.dumps({"ticket": case.as_dict(), "cola_correcta": queue},
                      ensure_ascii=False, default=str)


def user_message(labelled: list[tuple[Any, str]]) -> str:
    """§2.4's user message over `(case, queue)` pairs in arrival order; with
    none, `PLAN_MANUAL.md`'s request alone."""
    if not labelled:
        return COMPILE_USER
    lines = "\n".join(ticket_line(c, q) for c, q in labelled)
    return f"{HEADER}{lines}\n\n{COMPILE_USER}"


def messages(labelled: list[tuple[Any, str]]) -> list[dict[str, str]]:
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message(labelled)}]


def texts() -> dict[str, str]:
    return {"system_prompt": SYSTEM_PROMPT, "header": HEADER, "compile_user": COMPILE_USER}


def digests() -> dict[str, str]:
    return {k: sha256(v)[:16] for k, v in texts().items()}


def request(pin: dict, model: str, arm: str, messages_: list[dict],
            attempt: int) -> dict[str, Any]:
    """`placement.protocol.request_with`'s request, with the at-once budget. A
    module function, so that `CR-g2` can read it without building a client."""
    kwargs = pl_protocol.request_with(pin, model, arm, messages_, attempt)
    kwargs["max_tokens"] = plan.AT_ONCE_MAX_TOKENS
    return kwargs
