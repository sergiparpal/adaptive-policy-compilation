"""
Proposers.

A proposer receives a case in impasse and returns (action, rule_payload). The
payload then goes through mechanical validation: the proposer has no access to
the active base and cannot promote anything.

Two families:

  * MockProposer -- calls no LLM. It receives the correct action and generalizes
    with a fixed heuristic. It serves to (a) validate the plumbing without
    spending a single call and (b) trace the reuse / silent-error FRONTIER
    inherent to the DSL, which is the reference the real LLM is judged against
    afterwards.

    Methodological note: giving the mock the correct action is deliberate. It
    isolates the GENERALIZATION axis from the ACTING axis. With the real LLM a
    second source of error appears (the wrong action at proposal time) which is
    measured separately.

  * AnthropicProposer -- a real call. Ready to plug in; not run here.
"""

from __future__ import annotations

import json
import os
import random
from typing import Any, Protocol

from .domain import ACTIONS, ATTRIBUTES, DOMAINS, Case


class ProposalError(Exception):
    """The proposer returned nothing usable. NOT fatal: the loop counts it as an
    escalation without a rule and carries on. With cheap models this happens, and
    losing a 2000-case run at case 1500 over a badly closed JSON would be
    absurd."""


def parse_payload(text: str) -> dict[str, Any]:
    """Tolerant extraction: strips markdown fences, preambles and epilogues."""
    t = text.strip()
    if "```" in t:
        parts = t.split("```")
        for p in parts:
            p = p.strip().removeprefix("json").strip()
            if p.startswith("{"):
                t = p
                break
    i, j = t.find("{"), t.rfind("}")
    if i == -1 or j == -1 or j < i:
        raise ProposalError(f"sin objeto JSON en la respuesta: {text[:200]!r}")
    try:
        return json.loads(t[i : j + 1])
    except json.JSONDecodeError as exc:
        raise ProposalError(f"JSON invalido: {exc}") from exc


class Proposer(Protocol):
    name: str

    def propose(self, case: Case, true_action_hint: str | None) -> tuple[str, dict[str, Any]]:
        ...


# ---------------------------------------------------------------------------
# Mocks: they trace the DSL's frontier
# ---------------------------------------------------------------------------

class KeepKProposer:
    """
    Keeps the first k attributes of the priority order in domain.ATTRIBUTES and
    fixes them with `eq`. A deliberately naive generalizer: it never discovers
    `lte`/`gte`/`in`.

    k = 8 amounts to memorizing the case. k = 1 is maximally general.
    """

    def __init__(self, k: int):
        self.k = k
        self.name = f"keep_k({k})"

    def propose(self, case: Case, true_action_hint: str | None) -> tuple[str, dict[str, Any]]:
        attrs = ATTRIBUTES[: self.k]
        conds = [{"attr": a, "op": "eq", "value": getattr(case, a)} for a in attrs]
        return true_action_hint, {
            "conditions": conds,
            "action": true_action_hint,
            "note": f"mock keep_k k={self.k}",
        }


class RandomKProposer:
    """Same as KeepK but choosing k attributes at random. A lower baseline: it
    isolates how much of the performance comes from choosing the attributes
    WELL."""

    def __init__(self, k: int, seed: int = 0):
        self.k = k
        self.name = f"random_k({k})"
        self._rng = random.Random(seed)

    def propose(self, case: Case, true_action_hint: str | None) -> tuple[str, dict[str, Any]]:
        attrs = self._rng.sample(ATTRIBUTES, self.k)
        conds = [{"attr": a, "op": "eq", "value": getattr(case, a)} for a in attrs]
        return true_action_hint, {
            "conditions": conds,
            "action": true_action_hint,
            "note": f"mock random_k k={self.k}",
        }


# ---------------------------------------------------------------------------
# Real proposer
# ---------------------------------------------------------------------------

# NOTE: the prompt is left in Spanish on purpose. It is the text that produced
# the published records and `tests/doubles.py` replays those runs against it;
# translating it would change the experiment, not the documentation.
SYSTEM_PROMPT = f"""Eres el componente de excepcion de un sistema de triaje de tickets.

El motor simbolico no ha encontrado ninguna regla aplicable a este ticket. Tu tarea:

1. Decidir la cola de destino correcta para ESTE ticket.
2. Escribir UNA regla generalizable que cubra este ticket y casos analogos futuros.

La regla no es una anotacion: se anadira a una base que crece y se ejecutara sin
supervision sobre casos que aun no has visto. Escribela al nivel de abstraccion
que creas correcto. Demasiado especifica y no volvera a dispararse nunca;
demasiado general y pisara casos que deberian resolverse de otra forma.

ATRIBUTOS DISPONIBLES Y SUS DOMINIOS:
{json.dumps(DOMAINS, indent=2, default=str)}

severity: 1 = critica, 4 = baja.

ACCIONES POSIBLES:
{json.dumps(ACTIONS, indent=2)}

OPERADORES: eq, neq, lte, gte, in
  - lte y gte SOLO sobre severity y prior_tickets_30d
  - in requiere una lista de valores del dominio

Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:

{{
  "action": "<accion para este ticket>",
  "conditions": [{{"attr": "...", "op": "...", "value": ...}}],
  "note": "<una frase justificando el nivel de abstraccion elegido>"
}}

La regla DEBE casar el ticket presentado."""


def _user_msg(case: Case) -> str:
    return "TICKET EN IMPASSE:\n" + json.dumps(case.as_dict(), indent=2, default=str)


class AnthropicProposer:
    """Proposer via the Anthropic API. Requires ANTHROPIC_API_KEY."""

    def __init__(self, model: str = "claude-haiku-4-5-20251001", max_retries: int = 2):
        from anthropic import Anthropic  # lazy import

        self.name = f"anthropic({model})"
        self.model = model
        self.max_retries = max_retries
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def propose(self, case: Case, true_action_hint: str | None) -> tuple[str, dict[str, Any]]:
        user = _user_msg(case)
        last: Exception | None = None
        for _ in range(self.max_retries + 1):
            try:
                resp = self._client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=[{
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": user}],
                )
                text = "".join(b.text for b in resp.content if b.type == "text")
                payload = parse_payload(text)
                return payload.get("action"), payload
            except Exception as exc:  # noqa: BLE001
                last = exc
        raise ProposalError(str(last))


class OpenRouterProposer:
    """
    Proposer via OpenRouter. Requires OPENROUTER_API_KEY.

    OpenRouter exposes an OpenAI-compatible API, so the `openai` SDK pointed at
    a different base_url is enough. The model slug is the only change between
    providers: `deepseek/deepseek-v4-flash`, `openai/gpt-5.6-luna`, etc.

    Using a model from another family is methodologically preferable: the
    harness and the hidden policy were written by Claude, and it is better that
    the proposer was not.
    """

    def __init__(
        self,
        model: str = "deepseek/deepseek-v4-flash",
        max_retries: int = 2,
        force_json: bool = True,
    ):
        from openai import OpenAI  # lazy import

        self.name = f"openrouter({model})"
        self.model = model
        self.max_retries = max_retries
        self.force_json = force_json
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def propose(self, case: Case, true_action_hint: str | None) -> tuple[str, dict[str, Any]]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_msg(case)},
        ]

        last: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                kwargs: dict[str, Any] = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0,
                }
                # Some models do not support response_format; if it fails, the
                # retry disables it and relies on the tolerant parser.
                if self.force_json and attempt == 0:
                    kwargs["response_format"] = {"type": "json_object"}

                resp = self._client.chat.completions.create(**kwargs)
                text = resp.choices[0].message.content or ""
                payload = parse_payload(text)
                return payload.get("action"), payload
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    # Retry with an explicit repair instruction.
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content":
                         "Tu respuesta anterior no era JSON valido. Responde "
                         "UNICAMENTE con el objeto JSON, sin texto alrededor."},
                    ]
        raise ProposalError(str(last))


def list_openrouter_models(substring: str = "") -> list[tuple[str, str]]:
    """Queries the OpenRouter catalogue to find the exact slug. Avoids guessing
    names: the marketing ones and the API ones do not match."""
    import urllib.request

    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as r:
        data = json.loads(r.read().decode())
    out = []
    for m in data.get("data", []):
        mid = m.get("id", "")
        if substring.lower() in mid.lower():
            pr = m.get("pricing", {})
            out.append((mid, f"in {pr.get('prompt','?')} / out {pr.get('completion','?')} por token"))
    return sorted(out)
