"""
The two questions of `PLAN_MANUAL.md` §5, one per shape, at each level.

**Shape L, the loop.** The system prompt is `rung2.proposers2.SYSTEM_PROMPT_V1`,
imported and not retyped (rule A), with the manual inserted as one block just
before the operators. At level 0 nothing is inserted, so the prompt is v1's to
the byte and the loop is `PLAN_REUSE.md`'s protocol, asked again on the day the
other levels are asked. The user message — the base's neighbourhood and the
ticket — is rung 2's own and is not touched here.

**Shape C, compile once.** One question asks for the whole rule base in one
answer. It reuses v1's blocks word for word where they say the same thing — the
attributes and their domains, the actions, the operators — and describes rung
2's engine with the list's order standing for the declaration: what one rule's
cases contain decides first, and where two rules overlap without containment,
the earlier one in the list wins. That is the engine `manual/compile.py`
installs the answer into, so the model is told the semantics it is scored
under (§6.3 of the plan).

The manual block is the same at every level and in both shapes: one header
line, then the frozen text of `manual/levels.py`. `G-g2` checks that a prompt
with the manual differs from its level-0 prompt by that block and nothing else.

The texts are in Spanish: they are prompt content, as v1's is.
"""

from __future__ import annotations

import hashlib
import json

from harness.domain import ACTIONS, DOMAINS
from rung2.proposers2 import SYSTEM_PROMPT_V1

from . import levels

MANUAL_HEADER = "MANUAL DE ENRUTAMIENTO DE LA EMPRESA (es la politica que hay que seguir):"

# The block goes in just before this line, which appears once in each prompt.
ANCHOR = "\n\nOPERADORES: eq, neq, lte, gte, in"


def block(level: int) -> str:
    """What a manual adds to a prompt: the header and the frozen text."""
    body = levels.text(level)
    if body is None:
        raise ValueError("level 0 has no manual block")
    return MANUAL_HEADER + "\n\n" + body


def insert(prompt: str, level: int) -> str:
    """`prompt` with the manual of `level` inserted before the operators; the
    prompt itself at level 0."""
    if level == 0:
        return prompt
    if prompt.count(ANCHOR) != 1:
        raise ValueError("the anchor must appear exactly once in the prompt")
    return prompt.replace(ANCHOR, "\n\n" + block(level) + ANCHOR, 1)


# ---------------------------------------------------------------------------
# Shape L: the loop
# ---------------------------------------------------------------------------

def loop_system_prompt(level: int) -> str:
    return insert(SYSTEM_PROMPT_V1, level)


# ---------------------------------------------------------------------------
# Shape C: compile once
# ---------------------------------------------------------------------------

COMPILE_PROMPT = f"""Eres el autor de la base de reglas de un sistema de triaje de tickets.

Tu tarea: escribir, de una vez, la base de reglas COMPLETA con la que el motor
simbolico decidira a que cola va cada ticket.

COMO APLICA EL MOTOR TU BASE

El motor aplica dos niveles:

  NIVEL 1, automatico: si el conjunto de casos que cubre una regla esta
  CONTENIDO en el de otra, la mas contenida gana. Las excepciones anidadas
  dentro de un caso general se ordenan solas.

  NIVEL 2, por tu orden: cuando dos reglas se solapan sin que una contenga a la
  otra, gana la que aparece antes en tu lista.

Un ticket que no casa ninguna regla queda sin decidir. Toda regla necesita al
menos una condicion: si quieres una regla por defecto, dale una condicion que
casen todos los tickets.

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
  "rules": [
    {{"conditions": [{{"attr": "...", "op": "...", "value": ...}}],
     "action": "<accion>",
     "note": "<una frase>"}}
  ],
  "note": "<una frase sobre la base en su conjunto>"
}}

Las reglas van en el orden en que el motor debe aplicar el nivel 2."""

COMPILE_USER = "Escribe ahora la base de reglas completa."

# rung 2's proposer's retry, word for word.
RETRY_MSG = ("Tu respuesta anterior no era JSON valido. Responde UNICAMENTE con el "
             "objeto JSON, sin texto alrededor.")


def compile_system_prompt(level: int) -> str:
    return insert(COMPILE_PROMPT, level)


def compile_messages(level: int) -> list[dict[str, str]]:
    return [{"role": "system", "content": compile_system_prompt(level)},
            {"role": "user", "content": COMPILE_USER}]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def prompt_digests() -> dict[str, dict[int, str]]:
    """The digest of every prompt this plan sends, by shape and level."""
    return {"loop": {lv: sha256(loop_system_prompt(lv)) for lv in levels.LEVELS},
            "compile": {lv: sha256(compile_system_prompt(lv)) for lv in levels.LEVELS}}
