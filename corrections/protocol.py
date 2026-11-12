"""
The two arms' messages — §5.1 and §5.2 of `PLAN_CORRECTIONS.md`. **On the
proposer's path.** Nothing here imports the policy in code (§4). The one thing
of the truth that reaches a prompt is a reported ticket's own label, handed to
the proposer by `corrections/loop.py` in arm `l` only, and it enters the prompt
through `report`, nowhere else.

THE SYSTEM PROMPT is level 1's: `manual.prompts.loop_system_prompt(1)`, the
catalogue in v1's loop prompt, as `PLAN_MANUAL.md`'s level-1 loop sent it. v1c
sends level 3's. Level 3 is fixed in `reasoned_loop/plan.py`, and
`reasoned_loop.protocol` builds its system prompt from it at import, so this
module builds its own messages. With level 3's system prompt and no report they
are v1c's, byte for byte, and `CR-g1` holds them to that on every call of
`PLAN_PLACEMENT.md`'s three v1c runs.

THE REPORT (§2.1, R1). At a reported error in arm `l`, the first user message
carries, after v2b's `BLIND_BASE`, the paragraph `REPORT` with the ticket's true
queue in it:

    AVISO DE REVISION: este ticket no es un impasse. El motor lo decidio, y un
    revisor ha marcado esa decision como erronea. La cola correcta de este
    ticket es {queue}.

Everything else is v1c's: v2b's paragraph, the ticket under v1's heading
*TICKET EN IMPASSE*, the draft sent back as the assistant's turn and the
placement message. The placement call repeats the conversation, so it carries
the report too. In arm `n`, and at an impasse or a conflict in arm `l`, there is
no report and the messages are v1c's but for the system prompt.

THE PROPOSER is `placement/run.py`'s `Stamped`, the resumable proposer v1c's runs
were asked through, with its two calls building these messages. `reports` maps a
case to the queue its report names. Only `corrections/loop.py`'s wrapper of arm
`l` writes to it, and only at an escalation caused by a reported error.
Everything else is that class's, called: the partial file, the check that a
stored answer was paid for under the same request, the hour each answer was
kept, the seconds a resumed call keeps, and the outage that stops a run
unrecorded.

THE TEXTS' DIGESTS. Arm `n` sends four texts: level 1's system prompt and v1c's
other three. Arm `l` sends the same four and `REPORT`. The fingerprint hashes an
arm's texts in sorted order, as `reasoned_loop.protocol.fingerprint` does.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS, Case

from manual import prompts as mprompts
from placement import run as pl_run
from reasoned_loop import protocol as p
from rung2.proposers2 import user_msg

from . import plan

SYSTEM_PROMPT = mprompts.loop_system_prompt(plan.LEVEL)
LEVEL3_SYSTEM_PROMPT = p.SYSTEM_PROMPT     # v1c's, which level 1's replaces
BLIND_BASE = p.BLIND_BASE
PLACEMENT_TEMPLATE = p.PLACEMENT_TEMPLATE
RETRY_MSG = p.RETRY_MSG

REPORT = """AVISO DE REVISION: este ticket no es un impasse. El motor lo decidio, y un
revisor ha marcado esa decision como erronea. La cola correcta de este
ticket es {queue}.
"""

RULE_ID = re.compile(r"\b(?:H\d\d|R\d{4})\b")


class NotAQueue(ValueError):
    """A report that would name something other than one of the eight queues.
    Nothing is sent."""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# The report, and the messages
# ---------------------------------------------------------------------------

def report(queue: str) -> str:
    """§2.1's paragraph, naming `queue`, which must be one of the eight."""
    if queue not in ACTIONS:
        raise NotAQueue(f"{queue!r} is not one of the eight queues")
    return REPORT.format(queue=queue)


def base_text(queue: str | None = None) -> str:
    """What stands where the base would be: v2b's paragraph, and after it the
    report when there is one."""
    return BLIND_BASE if queue is None else BLIND_BASE + "\n" + report(queue)


def messages_for(case: Case, previous: Any = None, message: str = "",
                 queue: str | None = None,
                 system: str = SYSTEM_PROMPT) -> list[dict[str, str]]:
    """What a call sends: the system prompt and the blind user message, with
    the report in it when `queue` is given, and for the placement call the
    draft as the assistant's turn and the placement message after it."""
    out = [{"role": "system", "content": system},
           {"role": "user", "content": user_msg(case, base_text(queue))}]
    if previous is not None:
        out += [{"role": "assistant", "content": p.turn(previous)},
                {"role": "user", "content": message}]
    return out


def one_report_apart(without: list[dict[str, str]], with_: list[dict[str, str]],
                     queue: str) -> bool:
    """Whether two calls' messages are the same but for the first user
    message, where the second carries the report naming `queue` right after
    v2b's paragraph, and nothing else changes (`CR-g1`)."""
    if len(without) != len(with_) or len(without) < 2:
        return False
    if any(a != b for k, (a, b) in enumerate(zip(without, with_)) if k != 1):
        return False
    a, b = without[1]["content"], with_[1]["content"]
    insert = "\n" + report(queue)
    return (without[1]["role"] == with_[1]["role"] == "user"
            and a.startswith(BLIND_BASE)
            and b == BLIND_BASE + insert + a[len(BLIND_BASE):])


# ---------------------------------------------------------------------------
# The texts
# ---------------------------------------------------------------------------

def texts(arm: str) -> dict[str, str]:
    """The texts an arm sends: level 1's system prompt and v1c's other three,
    and in arm `l` the report's template."""
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    out = {"system_prompt": SYSTEM_PROMPT, "blind_base": BLIND_BASE,
           "placement_template": PLACEMENT_TEMPLATE, "retry_message": RETRY_MSG}
    if arm == plan.LABELLED:
        out["report"] = REPORT
    return out


def digests(arm: str) -> dict[str, str]:
    return {k: sha256(v)[:16] for k, v in texts(arm).items()}


def fingerprint(arm: str) -> str:
    """`reasoned_loop.protocol.fingerprint`'s hash over the arm's texts, in
    sorted order. So arm `n` with level 3's system prompt would have v1c's."""
    t = texts(arm)
    body = json.dumps([t[k] for k in sorted(t)], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def names_no_rule(text: str) -> bool:
    return not RULE_ID.search(text)


def queues_named(text: str) -> list[str]:
    return [q for q in ACTIONS if q in text]


# ---------------------------------------------------------------------------
# The proposer
# ---------------------------------------------------------------------------

class Reporting(pl_run.Stamped):
    """`placement/run.py`'s resumable proposer, whose two calls send this
    plan's messages: level 1's system prompt, and the report at a case
    `reports` names. `system` is level 1's; `CR-g1` sets it to level 3's to
    hold the class to v1c's."""

    name = f"openrouter-corrections({plan.MODEL})"
    system = SYSTEM_PROMPT

    def __init__(self, live, partial: Path, rows: list[dict], clock=time.monotonic):
        super().__init__(live, partial, rows, clock)
        self.reports: dict[int, str] = {}

    def first(self, case: Case, idx: int) -> p.Answer:
        return self.answer(idx, 0, messages_for(case, queue=self.reports.get(idx),
                                                system=self.system))

    def placement(self, case: Case, draft: Any, message: str, idx: int,
                  listed: list[str] | None = None) -> p.Answer:
        return self.answer(idx, 1, messages_for(case, draft, message,
                                                queue=self.reports.get(idx),
                                                system=self.system))


PROPOSERS = {"n": Reporting, "l": Reporting}
