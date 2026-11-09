"""
v1d — §5.2 of `PLAN_WHOLE.md`: `PLAN_PLACEMENT.md`'s v1c with one change, to the
first call's user message. **On the proposer's path**: nothing here reads a
label, a draw or the policy, and nothing imports the policy in code (rule B of
the plan). The text names neither a queue nor a rule.

THE TEXT (§2.1, T1). v1c's first call carries v2b's `BLIND_BASE` where the base
would be:

    BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
    ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues.

v1d carries `WHOLE_BASE` in its place, and nothing else changes. Its first
sentence is `BLIND_BASE`'s, and so is its last clause's promise of a list. In
between it asks for the region of the listed rule that governs the ticket, the
first of the list whose conditions the ticket matches, and says what a rule
narrowed to fall inside a lower rule of the list wins and loses.

THE MESSAGES. `messages_for` is `reasoned_loop.protocol.messages_for`, called,
with its first user message rebuilt over `WHOLE_BASE`. That message must be the
one v1c sends, `rung2.proposers2.user_msg` over `BLIND_BASE`, or nothing is sent:
so the system prompt, the ticket, the draft sent back as the assistant's turn and
the placement message are v1c's, byte for byte. The placement call repeats the
conversation, so it carries the same paragraph. With `base=BLIND_BASE` the
function gives back v1c's messages exactly, and `WR-g1` holds it to that on
every call of `PLAN_PLACEMENT.md`'s three v1c runs.

THE PROPOSER is `placement/run.py`'s `Stamped`, the resumable proposer v1c's runs
were asked through, with its two calls building v1d's messages. Everything else
is that class's, called: the partial file, the check that a stored answer was
paid for under the same request, the hour each answer was kept, the seconds a
resumed call keeps, and the outage that stops a run unrecorded. `PROPOSERS`
names each arm's class; v1c's is `placement.run.Stamped` itself.

THE TEXTS' DIGESTS. v1c's are `reasoned_loop.protocol`'s, as `PLAN_PLACEMENT.md`'s
records carry them. v1d's are the same four with `WHOLE_BASE` under its own key,
`whole_base`, in place of `blind_base`; `WR-g2` holds the other three to v1c's.
The fingerprint hashes the four in v1c's order, the paragraph in v2b's place, so
that it differs from v1c's by the paragraph alone.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from harness.domain import ACTIONS, Case

from placement import run as pl_run
from reasoned_loop import protocol as p
from rung2.proposers2 import user_msg

from . import plan

WHOLE_BASE = """BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
ticket con la region entera de la regla de la lista que lo gobierna: la
primera de la lista cuyas condiciones casa el ticket. No le anadas
condiciones para que quede dentro de una regla de mas abajo de la lista:
una regla dentro de otra solo le gana a esa otra, y el resto de su region se
queda con reglas de otras colas. Si tu regla se solapa con reglas existentes
de OTRA cola, se te listaran despues para que la situes.
"""

BASES = {"v1c": p.BLIND_BASE, "v1d": WHOLE_BASE}
BASE_KEYS = {"v1c": "blind_base", "v1d": "whole_base"}
FIRST_SENTENCE = "BASE DE REGLAS: no se te muestra en este paso."
RULE_ID = re.compile(r"\b(?:H\d\d|R\d{4})\b")


class NotV1c(ValueError):
    """The first user message is not the one v1c sends, so v1d would not be v1c
    with one paragraph replaced. Nothing is sent."""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# The messages
# ---------------------------------------------------------------------------

def messages_for(case: Case, previous: Any = None, message: str = "",
                 base: str = WHOLE_BASE) -> list[dict[str, str]]:
    """v1c's messages for the call, with the first user message rebuilt over
    `base` (§5.2)."""
    out = p.messages_for(case, previous, message)
    if out[1] != {"role": "user", "content": user_msg(case, p.BLIND_BASE)}:
        raise NotV1c("v1c's first user message is not the one v1d replaces")
    out[1] = {"role": "user", "content": user_msg(case, base)}
    return out


def one_paragraph_apart(v1c: list[dict[str, str]], v1d: list[dict[str, str]],
                        base: str = WHOLE_BASE) -> bool:
    """Whether two calls' messages are the same but for the first user message,
    where v1c's paragraph stands in one and `base` in the other, once and at
    the start (`WR-g1`)."""
    if len(v1c) != len(v1d) or len(v1c) < 2:
        return False
    if any(a != b for k, (a, b) in enumerate(zip(v1c, v1d)) if k != 1):
        return False
    a, b = v1c[1]["content"], v1d[1]["content"]
    return (v1c[1]["role"] == v1d[1]["role"] == "user"
            and a.startswith(p.BLIND_BASE) and b.startswith(base)
            and a[len(p.BLIND_BASE):] == b[len(base):])


# ---------------------------------------------------------------------------
# The texts
# ---------------------------------------------------------------------------

def texts(arm: str) -> dict[str, str]:
    """The four texts an arm sends: v1c's are `reasoned_loop.protocol`'s."""
    if arm == "v1c":
        return p.texts()
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    return {"system_prompt": p.SYSTEM_PROMPT, BASE_KEYS[arm]: BASES[arm],
            "placement_template": p.PLACEMENT_TEMPLATE, "retry_message": p.RETRY_MSG}


def digests(arm: str) -> dict[str, str]:
    return {k: sha256(v)[:16] for k, v in texts(arm).items()}


def fingerprint(arm: str) -> str:
    """`reasoned_loop.protocol.fingerprint`'s hash over the arm's four texts, in
    v1c's order, with the arm's paragraph in the place of v2b's. So v1d given
    v2b's paragraph has v1c's fingerprint, and v1c's is that function's own."""
    if arm == "v1c":
        return p.fingerprint()
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    t = {**p.texts(), BASE_KEYS["v1c"]: BASES[arm]}
    body = json.dumps([t[k] for k in sorted(t)], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def names_nothing(text: str) -> bool:
    """Whether a text names neither a queue nor a rule (§2.1)."""
    return not RULE_ID.search(text) and not any(q in text for q in ACTIONS)


# ---------------------------------------------------------------------------
# The proposer
# ---------------------------------------------------------------------------

class Stamped(pl_run.Stamped):
    """`placement/run.py`'s resumable proposer, whose two calls send v1d's
    messages. `base` is v1d's paragraph; `WR-g1` sets it to v2b's to hold the
    class to v1c's."""

    name = f"openrouter-v1d({plan.MODEL})"
    base = WHOLE_BASE

    def first(self, case: Case, idx: int) -> p.Answer:
        return self.answer(idx, 0, messages_for(case, base=self.base))

    def placement(self, case: Case, draft: Any, message: str, idx: int,
                  listed: list[str] | None = None) -> p.Answer:
        return self.answer(idx, 1, messages_for(case, draft, message, base=self.base))


PROPOSERS = {"v1c": pl_run.Stamped, "v1d": Stamped}
