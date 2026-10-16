"""
WHAT EACH CALL SAYS ABOUT ITSELF, kept per attempt for every paid run to come.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Two loose ends had one cause: the records kept the answer and not the call.

  * `PLAN_SCREEN.md`'s `V-a`. Asked without a screen, the model's answers moved
    between 2026-10-03 and 2026-10-14, in which wrong queue it picks. OpenRouter
    routes a model's name to several providers, and no record kept which one
    answered, so the drift cannot be split between the model and the route.
  * The pairwise parse failures reopened on 2026-10-05 (`FINDINGS3.md` §11's
    erratum). They are more frequent on the learned base's pairs than on the
    hidden policy's, and nothing says why, because those records keep no
    `finish_reason`.

`screen/ask.py` already wrapped its client to keep each attempt's
`finish_reason`. This module generalizes that wrapper and installs it where
every paid call goes through: the clients of `rung2/proposers2.py`,
`authorship/protocol.py` (which inherits it) and `rung2/pair_judgement.py`.
Rung 1's `harness/proposers.py` is left out: its loop, `harness/shadow.py`, is
frozen and keeps no per-call field.

--------------------------------------------------------------------------
WHAT IS KEPT, PER ATTEMPT
--------------------------------------------------------------------------
An attempt is one request. A question the proposer retries makes several, and
each is kept: the failed ones are what a parse failure is about.

  generation_id         `id`, OpenRouter's generation id. Documented. Its
                        `/api/v1/generation?id=` endpoint returns, among other
                        fields, `provider_name`, `finish_reason` and
                        `native_finish_reason` for that generation, for as long
                        as OpenRouter keeps it. Its reference does not say how
                        long.
  provider              `provider`, the provider OpenRouter routed the request
                        to. It arrives in the response body, but OpenRouter's API
                        reference does not document it (read on 2026-10-16), so
                        it may come back None. `generation_id` is the documented
                        route to the same fact.
  model                 `model`, the model that served the request. The reference
                        says it may differ from the one requested.
  system_fingerprint    when the provider sends one.
  finish_reason         `choices[0].finish_reason`, which OpenRouter normalizes to
                        stop, length, content_filter, tool_calls or error.
  native_finish_reason  `choices[0].native_finish_reason`, the provider's raw
                        value.
  prompt_tokens         from `usage`.
  completion_tokens     from `usage`.
  reasoning_tokens      `usage.completion_tokens_details.reasoning_tokens`.
                        Reasoning is what spent the answer's budget on 2026-09-30
                        (the amendment to §1 of `PLAN_REUSE.md`).
  error                 the exception's class name when the request itself
                        raised. Every other field is then None. An answer that
                        arrives and does not parse is not an error here: it has
                        its `finish_reason`, which is the point.

A field the response lacks is None, never guessed. `tests/doubles.py` returns
none of them, so a record written through the double says nothing about a
provider, and it should not.

--------------------------------------------------------------------------
WHAT IT NEVER DOES
--------------------------------------------------------------------------
It changes no request and no response. Every keyword argument reaches the
wrapped client untouched, and the response comes back as it came;
`tests/test_call_record.py` checks both against the double. It keeps no
message text and never sees the key. It makes no request of its own: looking a
generation id up is a separate act, for whoever needs it.

A WRITER THAT SPENDS stores, beside each question it asks, the list `take()`
returns, under the key `call_attempts`. The rung 2 loop keeps one entry per
escalation, `{"idx": ..., "call_attempts": [...]}`, in the record's `calls`,
because its per-case records are pinned by the replay of the published runs.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

FIELDS = ("generation_id", "provider", "model", "system_fingerprint",
          "finish_reason", "native_finish_reason",
          "prompt_tokens", "completion_tokens", "reasoning_tokens", "error")


def _plain(value: Any) -> Any:
    """What a record can hold: a JSON scalar, or its text."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def attempt(resp: Any) -> dict[str, Any]:
    """What a response says about the request that produced it."""
    choices = getattr(resp, "choices", None) or []
    choice = choices[0] if choices else None
    usage = getattr(resp, "usage", None)
    details = getattr(usage, "completion_tokens_details", None)
    return {
        "generation_id": _plain(getattr(resp, "id", None)),
        "provider": _plain(getattr(resp, "provider", None)),
        "model": _plain(getattr(resp, "model", None)),
        "system_fingerprint": _plain(getattr(resp, "system_fingerprint", None)),
        "finish_reason": _plain(getattr(choice, "finish_reason", None)),
        "native_finish_reason": _plain(getattr(choice, "native_finish_reason", None)),
        "prompt_tokens": _plain(getattr(usage, "prompt_tokens", None)),
        "completion_tokens": _plain(getattr(usage, "completion_tokens", None)),
        "reasoning_tokens": _plain(getattr(details, "reasoning_tokens", None)),
        "error": None,
    }


def failed(exc: BaseException) -> dict[str, Any]:
    """A request that raised before any response came back."""
    out: dict[str, Any] = dict.fromkeys(FIELDS)
    out["error"] = type(exc).__name__
    return out


class CallRecorder:
    """An SDK client, wrapped so that every request leaves an attempt behind.
    It answers to `.chat.completions.create`, which is all any caller here
    uses."""

    def __init__(self, client: Any):
        self.inner = client
        self.attempts: list[dict[str, Any]] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> Any:
        try:
            resp = self.inner.chat.completions.create(**kwargs)
        except Exception as exc:  # noqa: BLE001 — recorded, then raised as it was
            self.attempts.append(failed(exc))
            raise
        self.attempts.append(attempt(resp))
        return resp

    def take(self) -> list[dict[str, Any]]:
        """The attempts since the last take, and a clean slate for the next."""
        out, self.attempts = self.attempts, []
        return out


def install(holder: Any) -> CallRecorder:
    """Wrap `holder._client` in place and return the recorder. Installing twice
    returns the recorder already there instead of wrapping it again."""
    client = holder._client
    if isinstance(client, CallRecorder):
        return client
    recorder = CallRecorder(client)
    holder._client = recorder
    return recorder
