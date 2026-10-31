"""
v1b — §5 of `PLAN_REASONED_LOOP.md`: v1 with level 3's manual, v2b's blind
draft and v2b's placement round, asked with reasoning on. **On the proposer's
path**: nothing here reads a label, and nothing imports the policy in code
(rule B of the plan).

THE TEXTS (§5.1). None is new, and none is retyped:

  system prompt     `manual.prompts.loop_system_prompt(3)`, which
                    `PLAN_MANUAL.md`'s level-3 loop and `PLAN_REASONED_RULE.md`'s
                    two rule arms sent
  user message      `rung2.proposers2.user_msg` over v2b's `BLIND_BASE`
  placement message v2b's `PLACEMENT_TEMPLATE`, filled by
                    `blind.protocol.placement_message`
  retry message     v1's, as `first_match.prompts.RETRY_MSG` carries it

`fingerprint()` hashes the four, and `RL-g2` holds each to its source.

THE ASSISTANT'S TURN. A placement call sends the draft back as the assistant's
turn, as v2b's does. v2b sent the raw text. The asker here is
`PLAN_FIRST_MATCH.md`'s, called and not copied (rule A), and it keeps the
payload it parsed and not the text it parsed it from. So the turn is that
payload serialized, its keys in the order the model wrote them, and every call
row records `raw` as None rather than a text nobody kept.

THE ASKER is `first_match.ask.Asker` with this plan's request: one reasoning
setting and one budget for every call, the pin, temperature 0 and
`response_format` on the first attempt. Its retry is that plan's (rule H): a
failed call is retried with the same messages after a wait, and a failed parse
with v1's message, which that asker appends to a two-message request only. It
is the call site, with the recorder; this module makes no call of its own.

A RATE LIMIT IS AN OUTAGE, NOT AN ANSWER (§5.5's amendment, 2026-10-31). Every
launch of the smoke run met HTTP 429 from the pinned provider, and the text as
signed kept a call refused on all its attempts as a failed proposal whenever
the next call was answered: an escalation without a rule because the provider
was saturated. `Live` asks such a call again after each wait of
`plan.RATE_LIMIT_WAIT`, and raises `RateLimited` once every wait is spent: an
`Outage`, which nothing records. A call any of whose attempts reached the model
keeps §5.5's rule as signed, and is never asked again.

THE PROPOSER THE LOOP TALKS TO is `authorship/run.py`'s `Resumable`, called:
the answers already paid for first, each checked against the request it would
send, then the model, every answer appended to the partial file as it arrives.
This module adds what that proposer does not keep: each answer's keys in order,
its reasoning, its retries by cause and the provider that served it.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from harness.domain import Case

from authorship import protocol as e
from authorship import run as erun
from blind import protocol as v2b
from first_match import ask as fm_ask
from first_match import prompts as fm_prompts
from manual import prompts as mprompts
from rung2.proposers2 import user_msg

from . import plan

SYSTEM_PROMPT = mprompts.loop_system_prompt(plan.LEVEL)
BLIND_BASE = v2b.BLIND_BASE
PLACEMENT_TEMPLATE = v2b.PLACEMENT_TEMPLATE
RETRY_MSG = fm_prompts.RETRY_MSG
BLIND = v2b.BLIND                   # the screen's kind: no rule is shown

# v2b's validator parts, called (rule A).
split_overlapped = v2b.split_overlapped
listing = v2b.listing
same_rule = v2b.same_rule
placement_message = v2b.placement_message
CHANGED = v2b.CHANGED

# What this package keeps of an answer beyond `authorship.protocol.Answer`.
EXTRA = ("keys", "reasoning", "retries", "served_by")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def texts() -> dict[str, str]:
    return {"system_prompt": SYSTEM_PROMPT, "blind_base": BLIND_BASE,
            "placement_template": PLACEMENT_TEMPLATE, "retry_message": RETRY_MSG}


def digests() -> dict[str, str]:
    return {k: sha256(v)[:16] for k, v in texts().items()}


def fingerprint() -> str:
    body = json.dumps([texts()[k] for k in sorted(texts())], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The messages
# ---------------------------------------------------------------------------

def turn(answer: Any) -> str:
    """The draft as the assistant's turn: its payload, keys in order."""
    return json.dumps(answer.payload, ensure_ascii=False)


def messages_for(case: Case, previous: Any = None, message: str = "") -> list[dict[str, str]]:
    """What a call sends: the system prompt and the blind user message, and for
    the placement call the draft as the assistant's turn and the placement
    message after it (§5.2)."""
    out = [{"role": "system", "content": SYSTEM_PROMPT},
           {"role": "user", "content": user_msg(case, BLIND_BASE)}]
    if previous is not None:
        out += [{"role": "assistant", "content": turn(previous)},
                {"role": "user", "content": message}]
    return out


# ---------------------------------------------------------------------------
# The answer, and the asker
# ---------------------------------------------------------------------------

@dataclass
class Answer(e.Answer):
    keys: list | None = None
    reasoning: str | None = None
    retries: list = field(default_factory=list)
    served_by: str | None = None

    def extra(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in EXTRA}


@dataclass
class Request:
    """What `first_match.ask.Asker.ask` is handed: the messages, and an arm its
    request ignores."""
    turns: list[dict[str, str]]
    arm: str = plan.PROTOCOL

    def messages(self) -> list[dict[str, str]]:
        return [dict(m) for m in self.turns]


class Asker(fm_ask.Asker):
    """`PLAN_FIRST_MATCH.md`'s asker with this plan's request (§1). Built only
    after the gate, the key check and the blocking checks have spoken."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = plan.MAX_RETRIES,
                 sleep: Callable[[float], None] = time.sleep):
        super().__init__(model=model, max_retries=max_retries, sleep=sleep)
        self.name = f"openrouter-v1b({model})"

    def request(self, arm: str, messages: list[dict], attempt: int) -> dict[str, Any]:
        s = plan.settings()
        kwargs: dict[str, Any] = {
            "model": self.model, "messages": messages,
            "max_tokens": s["max_tokens"], "temperature": plan.TEMPERATURE,
            "extra_body": {"reasoning": s["reasoning"],
                           "provider": json.loads(json.dumps(plan.PROVIDER))}}
        if attempt == 0:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs


class RateLimited(erun.Outage):
    """A call refused for the rate on every attempt, through every wait of
    `plan.RATE_LIMIT_WAIT`: the provider's capacity, not the model's answer
    (§5.5's amendment). An `Outage`, so `Resumable` keeps nothing of it and the
    run stops where it was; the same command resumes there."""


def rate_limited(attempts: list[dict[str, Any]]) -> bool:
    """Whether no attempt of an ask reached the model: every one was refused
    for the rate, and none came back with a response."""
    return bool(attempts) and all(a.get("error") == plan.RATE_LIMITED for a in attempts)


class Live:
    """The model, behind the asker: one call in, one `Answer` out, with what
    each attempt said about itself. `ask(messages)` is all
    `authorship.run.Resumable` needs of it.

    An ask refused for the rate on every attempt is asked again after each wait
    of `plan.RATE_LIMIT_WAIT`, through the asker's own sleep, and the asker
    starts again each time, its retries and `response_format` included. The
    answer keeps every attempt and every retry of the call."""

    def __init__(self, asker: Asker):
        self.asker = asker
        self.extra: dict[str, Any] = {}

    def ask(self, messages: list[dict[str, str]]) -> Answer:
        recorder = self.asker.calls
        recorder.take()                    # only this call's attempts count
        said: list[dict[str, Any]] = []
        causes: list[str] = []
        for wait in (0, *plan.RATE_LIMIT_WAIT):
            if wait:
                self.asker.sleep(wait)
            try:
                got = self.asker.ask(Request(messages))
            except fm_ask.AskFailed as exc:
                now = recorder.take()
                said, causes = said + now, causes + list(exc.causes)
                if rate_limited(now):
                    continue               # nothing reached the model: wait it out
                self.extra = {}
                raise e.ProposalFailed(f"{exc} (retries: {', '.join(causes)})",
                                       said[-1].get("finish_reason") if said else None,
                                       len(causes), said) from exc
            said, causes = said + recorder.take(), causes + list(got["retries"])
            self.extra = {"keys": got["keys"], "reasoning": got["reasoning"],
                          "retries": causes, "served_by": fm_ask.served_by(said)}
            return Answer(got["action"], got["payload"], None,
                          said[-1].get("finish_reason") if said else None,
                          len(causes) + 1, said, **self.extra)
        self.extra = {}
        raise RateLimited(f"a call was refused for the rate on all {len(said)} of its "
                          f"attempts, through waits of {sum(plan.RATE_LIMIT_WAIT)} s")


class Resumable(erun.Resumable):
    """`authorship/run.py`'s resumable proposer with v1b's two calls, keeping
    each answer's keys, reasoning, retries and provider in the partial file and
    giving them back on a resume."""

    name = f"openrouter-v1b({plan.MODEL})"

    def first(self, case: Case, idx: int) -> Answer:
        return self.answer(idx, 0, messages_for(case))

    def placement(self, case: Case, draft: Any, message: str, idx: int,
                  listed: list[str] | None = None) -> Answer:
        return self.answer(idx, 1, messages_for(case, draft, message))

    def keep(self, row: dict) -> None:
        if row.get("failure") is None:
            row = {**row, **{k: getattr(self.live, "extra", {}).get(k) for k in EXTRA}}
        super().keep(row)

    def answer(self, idx: int, round_: int, messages) -> Answer:
        stored = self.stored.get((idx, round_))
        got = super().answer(idx, round_, messages)
        source = stored if stored is not None else getattr(self.live, "extra", {})
        return Answer(got.action, got.payload, got.raw, got.finish_reason, got.attempts,
                      list(got.call_attempts or []), **{k: source.get(k) for k in EXTRA})
