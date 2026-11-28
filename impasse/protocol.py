"""
v1n — §5.2 of `PLAN_IMPASSE.md`: `PLAN_PLACEMENT.md`'s v1c with one change, to
the first call's user message at an escalation whose cause is an IMPASSE. **On
the proposer's path**: nothing here reads a label, a draw or the policy, and
nothing imports the policy in code (rule B of the plan). The notice names neither
a queue nor a rule.

THE TEXT (§2.1, N1). v1c's first call carries v2b's `BLIND_BASE` where the base
would be. At an impasse, v1n carries `PLAN_CAUSE.md`'s arm `i`'s paragraph in its
place, `cause.prompts.PARAGRAPHS["i"]`, imported and not retyped: `BLIND_BASE`, a
blank line, and the impasse notice,

    AVISO DEL MOTOR: ninguna regla de la base casa este ticket. Por eso no ha podido
    decidirlo.

At a CONFLICT and at a reported ERROR, v1n's two calls send v1c's messages, byte
for byte.

THE CAUSE, AND WHAT OF IT THE PROPOSER IS TOLD. `propose_v1n` is
`placement.protocol.propose_v1c`, called, with the proposer told before its first
call whether the escalation's cause is an IMPASSE, and told nothing else. The flag
is read off the cause `channel.loop.escalates` returned, which is the engine's own
outcome where it is an IMPASSE: no rule of the base matches the ticket. It is
false at a CONFLICT and at an ERROR alike, so a reported error reaches the
proposer as a conflict does, as nothing (rule I). It is cleared after the
escalation, whatever happened in it.

THE MESSAGES. `messages_for` is `whole.protocol.messages_for`, called, with the
first user message rebuilt over the notice's paragraph at an impasse and over v2b's
everywhere else. That function checks that the message it replaces is the one v1c
sends, `rung2.proposers2.user_msg` over `BLIND_BASE`, or nothing is sent; given
`BLIND_BASE` it gives back v1c's messages exactly. The placement call repeats the
conversation, so at an impasse it carries the notice too.

THE PROPOSER is `placement/run.py`'s `Stamped`, the resumable proposer v1c's runs
were asked through, with its two calls building v1n's messages, and the cases at
which it sent the notice kept as `notice_at`. Everything else is that class's,
called: the partial file, the check that a stored answer was paid for under the
same request, the hour each answer was kept, the seconds a resumed call keeps,
and the outage that stops a run unrecorded. `notice = False` holds the class to
v1c: `IM-g1` sets it so on the closed runs' replays. `PROPOSERS` names each arm's
class, and `ESCALATIONS` each arm's escalation; v1c's are `placement`'s.

THE TEXTS' DIGESTS. v1c's are `reasoned_loop.protocol`'s, as `PLAN_PLACEMENT.md`'s
and `PLAN_WHOLE.md`'s records carry them. v1n's are the same four and the notice's
paragraph under its own key, `notice_base`; `IM-g2` holds the four to v1c's. The
fingerprint hashes the five in the order of their keys, so that it differs from
v1c's by the paragraph alone.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

from harness.domain import Case

from cause import prompts as cprompts
from placement import loop as pl_loop
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from whole import protocol as wprotocol

from . import plan

NOTICE = cprompts.IMPASSE_NOTICE
NOTICE_BASE = cprompts.PARAGRAPHS[cprompts.IMPASSE]
SEPARATOR = cprompts.SEPARATOR
NOTICE_KEY = "notice_base"
names_nothing = wprotocol.names_nothing
NotV1c = wprotocol.NotV1c

if NOTICE_BASE != p.BLIND_BASE + SEPARATOR + NOTICE:
    raise ImportError("PLAN_CAUSE.md's arm i is no longer v2b's paragraph and the notice")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# The messages
# ---------------------------------------------------------------------------

def base_for(impasse: bool) -> str:
    """The paragraph a call carries where the base would be (§5.2)."""
    return NOTICE_BASE if impasse else p.BLIND_BASE


def messages_for(case: Case, previous: Any = None, message: str = "",
                 impasse: bool = False) -> list[dict[str, str]]:
    """v1c's messages for the call, with the first user message rebuilt over the
    notice's paragraph at an impasse (§5.2)."""
    return wprotocol.messages_for(case, previous, message, base=base_for(impasse))


def apart_by_the_notice(v1c: list[dict[str, str]], v1n: list[dict[str, str]]) -> bool:
    """Whether two calls' messages are the same but for the first user message,
    where v2b's paragraph stands in one and the notice's in the other, once and
    at the start (`IM-g1`)."""
    return wprotocol.one_paragraph_apart(v1c, v1n, base=NOTICE_BASE)


# ---------------------------------------------------------------------------
# The texts
# ---------------------------------------------------------------------------

def texts(arm: str) -> dict[str, str]:
    """The texts an arm sends: v1c's four are `reasoned_loop.protocol`'s; v1n's
    are those four and the notice's paragraph."""
    if arm == "v1c":
        return p.texts()
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    return {**p.texts(), NOTICE_KEY: NOTICE_BASE}


def digests(arm: str) -> dict[str, str]:
    return {k: sha256(v)[:16] for k, v in texts(arm).items()}


def fingerprint(arm: str) -> str:
    """`reasoned_loop.protocol.fingerprint`'s hash over the arm's texts, in the
    order of their keys. v1c's is that function's own."""
    if arm == "v1c":
        return p.fingerprint()
    t = texts(arm)
    body = json.dumps([t[k] for k in sorted(t)], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The proposer, and the escalation
# ---------------------------------------------------------------------------

class Stamped(pl_run.Stamped):
    """`placement/run.py`'s resumable proposer, whose two calls send v1n's
    messages: at an impasse, over the notice's paragraph. `impasse` is set by
    `propose_v1n` for one escalation; `notice = False` holds the class to v1c."""

    name = f"openrouter-v1n({plan.MODEL})"
    notice = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.impasse = False
        self.notice_at: list[int] = []

    def sends_the_notice(self) -> bool:
        return bool(self.notice and self.impasse)

    def first(self, case: Case, idx: int) -> p.Answer:
        told = self.sends_the_notice()
        if told:
            self.notice_at.append(idx)
        return self.answer(idx, 0, messages_for(case, impasse=told))

    def placement(self, case: Case, draft: Any, message: str, idx: int,
                  listed: list[str] | None = None) -> p.Answer:
        return self.answer(idx, 1, messages_for(case, draft, message,
                                                impasse=self.sends_the_notice()))


def propose_v1n(engine, case: Case, idx: int, cause: str, proposer, channels: list[str],
                clock=time.monotonic) -> dict[str, Any]:
    """One escalation under v1n (§5.2): v1c's, with the proposer told whether the
    cause is an IMPASSE and nothing else, and the flag cleared after it."""
    proposer.impasse = cause == plan.IMPASSE
    try:
        return pl_protocol.propose_v1c(engine, case, idx, cause, proposer, channels,
                                       clock=clock)
    finally:
        proposer.impasse = False


PROPOSERS = {"v1c": pl_run.Stamped, "v1n": Stamped}
ESCALATIONS = {"v1c": pl_loop.ESCALATIONS["v1c"], "v1n": propose_v1n}
