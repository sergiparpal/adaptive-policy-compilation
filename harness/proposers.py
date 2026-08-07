"""
Proponentes.

Un proponente recibe un caso en impasse y devuelve (accion, payload_de_regla).
El payload pasa despues por validacion mecanica: el proponente no tiene acceso
a la base activa ni puede promocionar nada.

Dos familias:

  * MockProposer -- no llama a ningun LLM. Recibe la accion correcta y
    generaliza con una heuristica fija. Sirve para (a) validar las tuberias sin
    gastar una sola llamada y (b) trazar la FRONTERA reutilizacion / error
    silencioso propia del DSL, que es la referencia contra la que se juzga
    despues al LLM real.

    Nota metodologica: darle la accion correcta al mock es deliberado. Aisla el
    eje de GENERALIZACION del eje de ACTUACION. Con el LLM real aparece una
    segunda fuente de error (accion equivocada en el momento de proponer) que se
    mide por separado.

  * AnthropicProposer -- llamada real. Listo para enchufar; no se ejecuta aqui.
"""

from __future__ import annotations

import json
import os
import random
from typing import Any, Protocol

from .domain import ACTIONS, ATTRIBUTES, DOMAINS, Case


class ProposalError(Exception):
    """El proponente no devolvio nada usable. NO es fatal: el bucle lo cuenta
    como escalacion sin regla y sigue. Con modelos baratos esto pasa, y perder
    una tirada de 2000 casos en el caso 1500 por un JSON mal cerrado seria
    absurdo."""


def parse_payload(text: str) -> dict[str, Any]:
    """Extraccion tolerante: quita vallas markdown, preambulos y epilogos."""
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
# Mocks: trazan la frontera del DSL
# ---------------------------------------------------------------------------

class KeepKProposer:
    """
    Conserva los primeros k atributos del orden de prioridad de domain.ATTRIBUTES
    y los fija con `eq`. Generalizador deliberadamente ingenuo: nunca descubre
    `lte`/`gte`/`in`.

    k = 8 equivale a memorizar el caso. k = 1 es maximamente general.
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
    """Igual que KeepK pero eligiendo k atributos al azar. Baseline inferior:
    aisla cuanto del rendimiento viene de elegir BIEN los atributos."""

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
# Proponente real
# ---------------------------------------------------------------------------

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
    """Proponente via API de Anthropic. Requiere ANTHROPIC_API_KEY."""

    def __init__(self, model: str = "claude-haiku-4-5-20251001", max_retries: int = 2):
        from anthropic import Anthropic  # import perezoso

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
    Proponente via OpenRouter. Requiere OPENROUTER_API_KEY.

    OpenRouter expone una API compatible con OpenAI, asi que basta con el SDK
    `openai` apuntando a otra base_url. El slug del modelo es el unico cambio
    entre proveedores: `deepseek/deepseek-v4-flash`, `openai/gpt-5.6-luna`, etc.

    Usar un modelo de otra familia es metodologicamente preferible: el arnes y
    la politica oculta los escribio Claude, y conviene que el proponente no.
    """

    def __init__(
        self,
        model: str = "deepseek/deepseek-v4-flash",
        max_retries: int = 2,
        force_json: bool = True,
    ):
        from openai import OpenAI  # import perezoso

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
                # Algunos modelos no soportan response_format; si falla, el
                # reintento lo desactiva y confia en el parser tolerante.
                if self.force_json and attempt == 0:
                    kwargs["response_format"] = {"type": "json_object"}

                resp = self._client.chat.completions.create(**kwargs)
                text = resp.choices[0].message.content or ""
                payload = parse_payload(text)
                return payload.get("action"), payload
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    # Reintento con instruccion de reparacion explicita.
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content":
                         "Tu respuesta anterior no era JSON valido. Responde "
                         "UNICAMENTE con el objeto JSON, sin texto alrededor."},
                    ]
        raise ProposalError(str(last))


def list_openrouter_models(substring: str = "") -> list[tuple[str, str]]:
    """Consulta el catalogo de OpenRouter para encontrar el slug exacto.
    Evita adivinar nombres: los comerciales y los de API no coinciden."""
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
