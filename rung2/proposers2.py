"""
Rung 2 proposer: it sees a BOUNDED neighbourhood of the existing base.

The underlying change relative to rung 1: priority is a relation between rules,
and there the proposer saw no other rule. Here it sees the ones that could
compete with the one it is about to write.

WHAT IT IS SHOWN, AND WHY

  * on CONFLICT: the UNDEFEATED set that disagreed. Those are literally the
    rules it has to position itself against; the engine has already computed
    that no other rule defeats them.
  * on a coverage IMPASSE: the nearest neighbours, ordered by how many of their
    conditions the case fails.

A hard cap of MAX_SHOWN rules, regardless of the size of the base. Priority can
only be needed between rules that OVERLAP: a rule sharing no case with the new
one can never conflict with it, so showing it is noise. The bounded
neighbourhood is exactly the set the new rule might need to order itself
against, and its size does not grow with the base.

`correct_count` is NOT shown. It is a figure derived from the oracle and showing
it would break the separation. Id, conditions, action and already-declared edges
are shown.
"""

from __future__ import annotations

import json
import os
from typing import Any

from harness.domain import ACTIONS, DOMAINS, Case

from .engine2 import Rule2

MAX_SHOWN = 12


class ProposalError(Exception):
    """The proposer returned nothing usable. Not fatal: it is counted and the
    loop carries on."""


def parse_payload(text: str) -> dict[str, Any]:
    t = text.strip()
    if "```" in t:
        for p in t.split("```"):
            p = p.strip().removeprefix("json").strip()
            if p.startswith("{"):
                t = p
                break
    i, j = t.find("{"), t.rfind("}")
    if i == -1 or j == -1 or j < i:
        raise ProposalError(f"sin objeto JSON: {text[:200]!r}")
    try:
        return json.loads(t[i : j + 1])
    except json.JSONDecodeError as exc:
        raise ProposalError(f"JSON invalido: {exc}") from exc


# ---------------------------------------------------------------------------
# Neighbourhood
# ---------------------------------------------------------------------------

def _violated(rule: Rule2, case: Case) -> int:
    return sum(0 if c.holds(case) else 1 for c in rule.conditions)


def neighbourhood(engine, case: Case, undefeated: list[Rule2]) -> tuple[list[Rule2], str]:
    """The rules shown to the proposer, and how they are labelled."""
    shown = list(undefeated)[:MAX_SHOWN]
    if shown:
        return shown, "conflicto"
    rest = sorted(
        (r for r in engine.rules),
        key=lambda r: (_violated(r, case), -r.fire_count, r.born_at),
    )
    return rest[:MAX_SHOWN], "vecindario"


def render_base_v1(shown: list[Rule2], kind: str, engine=None, case=None) -> str:
    if not shown:
        return "BASE DE REGLAS: vacia. Esta es la primera regla.\n"
    if kind == "conflicto":
        head = ("REGLAS EN CONFLICTO sobre este ticket. Todas casan el ticket y "
                "ninguna derrota a las demas, por eso el motor no ha podido "
                "decidir:")
    else:
        head = ("REGLAS PROXIMAS de la base (ninguna casa este ticket; se listan "
                "las que menos condiciones incumplen):")
    return head + "\n" + "\n".join("  " + r.render() for r in shown) + "\n"


def render_base_v2(shown: list[Rule2], kind: str, engine, case: Case) -> str:
    """
    v2: the engine supplies the SET ARITHMETIC the proposer computes badly.

    Under v1 the proposer claimed non-existent overlaps (R0035: "it overlaps at
    business+severity4" between `billing` and `integrations`, which are
    disjoint) and even wrote down the correct fact and drew the opposite
    conclusion (R0036: "off_hours is mutually exclusive" and declared the edge
    anyway).

    Everything marked here is computed over the exhaustive space of 134,400
    combinations. None of these figures is derivable by the proposer from the
    text of the rules.

    The emitted text stays in Spanish: it is what produced the records.
    """
    if not shown:
        return "BASE DE REGLAS: vacia. Esta es la primera regla.\n"

    if kind == "conflicto":
        head = ("REGLAS EN CONFLICTO sobre este ticket. Todas lo casan y ninguna "
                "derrota a las demas, por eso el motor no ha podido decidir:")
    else:
        head = ("REGLAS PROXIMAS de la base, ordenadas por cuantas condiciones "
                "incumple el ticket:")

    lines = [head]
    for r in shown:
        bad = [f"{c.attr} {c.op} {c.value}" for c in r.conditions if not c.holds(case)]
        size = engine.ext[r.rule_id].bit_count()
        tag = ("CASA EL TICKET -> tu regla se solapara con ella con seguridad"
               if not bad else
               "el ticket INCUMPLE: " + "; ".join(bad))
        lines.append(f"  {r.render()}")
        lines.append(f"      [{tag}]  [cubre {size:,} casos del espacio]")

    # exact disjointness among the rules shown
    disj = []
    for i in range(len(shown)):
        for j in range(i + 1, len(shown)):
            a, b = shown[i], shown[j]
            if engine.ext[a.rule_id] & engine.ext[b.rule_id] == 0:
                disj.append(f"{a.rule_id}/{b.rule_id}")
    if disj:
        lines.append("\n  PARES DISJUNTOS entre las de arriba (no comparten ni un "
                     "solo caso posible, calculado por el motor):")
        lines.append("    " + ", ".join(disj))

    lines.append(
        "\n  COMO SABER SI TU REGLA SE SOLAPARA CON UNA DE ESTAS: tu regla tiene "
        "que casar el ticket.\n  Si fijas alguno de los atributos que la regla R "
        "'incumple' arriba, tu regla y R quedaran\n  DISJUNTAS y declarar prioridad "
        "entre ambas no tendra ningun efecto. Solo se solaparan\n  si dejas libres "
        "esos atributos.")
    return "\n".join(lines) + "\n"


RENDERERS = {"v1": render_base_v1, "v2": render_base_v2}


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_V1 = f"""Eres el componente de excepcion de un sistema de triaje de tickets.

El motor simbolico no ha podido decidir este ticket. Tu tarea:

1. Decidir la cola de destino correcta para ESTE ticket.
2. Escribir UNA regla generalizable que lo cubra a el y a casos analogos futuros.
3. Situar esa regla respecto a las reglas que ya existen, cuando haga falta.

COMO ARBITRA EL MOTOR (importante para el punto 3)

El motor aplica dos niveles:

  NIVEL 1, automatico: si el conjunto de casos que cubre una regla esta
  CONTENIDO en el de otra, la mas contenida gana sin que nadie lo declare. Las
  excepciones anidadas dentro de un caso general se ordenan solas.

  NIVEL 2, declarado por ti: cuando dos reglas se solapan pero ninguna contiene
  a la otra, el motor no tiene forma de saber cual debe mandar. Si no lo
  declaras, seguira sin saberlo y escalara cada vez que ambas casen.

Por eso solo necesitas declarar prioridad frente a reglas que se solapan con la
tuya sin que una contenga a la otra. Si tu regla es un caso particular de otra,
no declares nada: el nivel 1 ya lo resuelve.

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
  "beats": ["<id de regla existente a la que la tuya debe ganar>"],
  "loses_to": ["<id de regla existente que debe ganar a la tuya>"],
  "note": "<una frase justificando el nivel de abstraccion y la prioridad elegidos>"
}}

`beats` y `loses_to` solo pueden citar identificadores de reglas que aparezcan
en la lista de arriba. Si no hay ninguna relacion que declarar, dejalos vacios.

La regla DEBE casar el ticket presentado."""


# ---------------------------------------------------------------------------
# v2 — changes two things relative to v1, and only two:
#
#   (a) how overlap is framed. v1 said "you only need to declare priority
#       against rules that overlap yours without one containing the other",
#       which reads as an incentive to AVOID overlap. Measured over 4 runs of
#       n=100 with different corpora: overlap between rules fell from rung 1's
#       17.5% to 0.0-2.9%, with the same number of conditions per rule. The
#       model was not narrowing the rules: it was tiling them. Without overlap
#       there is no conflict and declared priority cannot be measured.
#
#   (b) the inference rule about disjointness, which the engine already marks in
#       the v2 neighbourhood but is worth stating once.
#
# The rest of the text is identical to v1, word for word. Both prompts stay in
# Spanish: they are the text that produced the published records.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_V2 = SYSTEM_PROMPT_V1.replace(
    """Por eso solo necesitas declarar prioridad frente a reglas que se solapan con la
tuya sin que una contenga a la otra. Si tu regla es un caso particular de otra,
no declares nada: el nivel 1 ya lo resuelve.""",
    """El solape entre reglas es NORMAL y es lo que se espera. Una regla que no se
solapa con ninguna otra cubre solo el rincon del que nacio y no generaliza nada.
Escribe la regla al nivel de abstraccion que creas correcto AUNQUE pise a otras,
y usa `beats` / `loses_to` para decir quien manda donde se pisen. No estreches
una regla ni le añadas condiciones para esquivar a otra: eso no resuelve el
conflicto, lo esconde.

Si tu regla es un caso particular de otra (todo caso que casa la tuya casa
tambien la otra), no declares nada: el nivel 1 ya lo resuelve solo.

Cuidado con la aritmetica de conjuntos: dos reglas que mencionan los mismos
atributos pueden no compartir ni un solo caso. El motor te marca abajo, para
cada regla, que condiciones incumple este ticket y que pares son disjuntos.
Esos datos estan calculados sobre el espacio completo de casos: fiate de ellos
antes que de tu propia estimacion.""")

assert SYSTEM_PROMPT_V2 != SYSTEM_PROMPT_V1, "la sustitucion de la v2 no aplico"

PROMPTS = {"v1": SYSTEM_PROMPT_V1, "v2": SYSTEM_PROMPT_V2}


def user_msg(case: Case, base_text: str) -> str:
    return (base_text + "\nTICKET EN IMPASSE:\n"
            + json.dumps(case.as_dict(), indent=2, default=str))


# ---------------------------------------------------------------------------

class OpenRouterProposer2:
    """Identical to rung 1's except that the user message carries the
    neighbourhood of the base. It never receives the true action."""

    def __init__(self, model: str = "deepseek/deepseek-v4-flash", max_retries: int = 2,
                 prompt_version: str = "v1"):
        from openai import OpenAI

        if prompt_version not in PROMPTS:
            raise ValueError(f"version de prompt desconocida: {prompt_version}")
        self.name = f"openrouter2({model},{prompt_version})"
        self.model = model
        self.prompt_version = prompt_version
        self.system_prompt = PROMPTS[prompt_version]
        self.render = RENDERERS[prompt_version]
        self.max_retries = max_retries
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def build_base(self, engine, case: Case, undefeated: list[Rule2]):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, self.render(shown, kind, engine, case)

    def propose(self, case: Case, base_text: str) -> tuple[str, dict[str, Any]]:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_msg(case, base_text)},
        ]
        last: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                kwargs: dict[str, Any] = {
                    "model": self.model, "messages": messages,
                    "max_tokens": 1200, "temperature": 0,
                }
                if attempt == 0:
                    kwargs["response_format"] = {"type": "json_object"}
                resp = self._client.chat.completions.create(**kwargs)
                payload = parse_payload(resp.choices[0].message.content or "")
                return payload.get("action"), payload
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content":
                         "Tu respuesta anterior no era JSON valido. Responde "
                         "UNICAMENTE con el objeto JSON, sin texto alrededor."},
                    ]
        raise ProposalError(str(last))
