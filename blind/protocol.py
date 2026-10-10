"""
v2b — `PLAN_OVERLAP.md`'s v2e with a blind first draft and a forced placement:
§5 of `PLAN_BLIND.md`, and nothing else.

THE TEXTS. v2b is built from `overlap.protocol.SYSTEM_PROMPT_V2E` by adding one
paragraph before v2's paragraph on set arithmetic, the way v2e was built from v2,
and the addition is asserted to have applied. Two texts are new: the line that
stands where the base would be on an impasse, and the placement message. The
order paragraph and the repair message of a CONFLICT are v2e's. `fingerprint()`
hashes the five, and `K-g3` refuses if it is not the one `plan.FINGERPRINT`
declares. **After §0 is signed none of them moves**, hard rule 5.

THE BLIND DRAFT (§5.1). On an impasse the first call shows no rule: where v2e
rendered the neighbourhood, v2b sends `BLIND_BASE`. On a CONFLICT the screen is
v2e's, the rules in conflict and the order paragraph, because an order answer has
to cite them.

THE PLACEMENT (§5.2). After a blind draft, `O` is v2e's: the existing rules whose
extension meets the new rule's and whose queue differs. If it is not empty, one
placement round lists it, in v2e's seeded order, and asks for **the same rule**,
placed against each. `same_rule` is what the validator holds the second answer
to: the same queue and the same extension, whatever the wording.

THE PROPOSER is v2e's `ProposerV2E` with v2b's system prompt and v2b's screens.
Its retries, and the raw text and `finish_reason` it keeps, are v1e's.
"""

from __future__ import annotations

import hashlib
import json
import random
from typing import Any

from harness.domain import Case

from authorship import protocol as e
from overlap import protocol as v2e
from rung2.proposers2 import MAX_SHOWN, neighbourhood, user_msg

from . import plan

# --- §5.1: the paragraph v2b adds, and where ---------------------------------

BEFORE = "Cuidado con la aritmetica de conjuntos:"

BLIND_PARAGRAPH = """CUANDO NINGUNA REGLA CUBRE EL TICKET, escribes la regla SIN VER la base: no se
te muestra ninguna regla existente. Escribela al nivel de abstraccion que creas
correcto para el ticket, con `beats` y `loses_to` vacios. Despues el motor
calcula, sobre el espacio completo de casos, con que reglas existentes de OTRA
cola se solapa la tuya, y te las lista: entonces tienes que situar ESA MISMA
regla frente a cada una, sin cambiarla. Cuando el ticket escala porque varias
reglas existentes chocan, esas reglas si se te muestran.

"""

assert v2e.SYSTEM_PROMPT_V2E.count(BEFORE) == 1, "v2e's arithmetic paragraph moved"
SYSTEM_PROMPT_V2B = v2e.SYSTEM_PROMPT_V2E.replace(BEFORE, BLIND_PARAGRAPH + BEFORE)
assert SYSTEM_PROMPT_V2B != v2e.SYSTEM_PROMPT_V2E, "la adicion de la v2b no aplico"

# What stands where the base would be, on an impasse.
BLIND_BASE = """BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues.
"""

BLIND = "ciego"                     # the screen's kind, beside v2's two

# --- §5.2: the placement round ------------------------------------------------

PLACEMENT_TEMPLATE = """Tu regla se solapa con estas reglas existentes de OTRA cola (calculado por el
motor sobre el espacio completo de casos):
{lista}
Responde de nuevo con el mismo formato y con LA MISMA regla: la misma accion y
las mismas condiciones. Situala frente a cada una de la lista: ponla en `beats`
si tu regla es una EXCEPCION a ella, de modo que la tuya manda donde casen las
dos; en `loses_to` si es un caso GENERAL por debajo de ella, de modo que la otra
manda. No cambies la regla: una regla distinta se rechaza."""

# --- §5.3: a CONFLICT is v2e's --------------------------------------------------

ORDER_PARAGRAPH = v2e.ORDER_PARAGRAPH
REPAIR_TEMPLATE = v2e.REPAIR_TEMPLATE

# The one verdict v2b adds to v1e's, §5.2.
CHANGED = "cambiada"


def fingerprint() -> str:
    """The texts v2b sends, hashed. `K-g3` compares it with `plan.FINGERPRINT`."""
    body = json.dumps([SYSTEM_PROMPT_V2B, BLIND_BASE, PLACEMENT_TEMPLATE,
                       ORDER_PARAGRAPH, REPAIR_TEMPLATE], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def render_base(shown, kind: str, engine=None, case=None) -> str:
    """On a CONFLICT, v2e's screen; on an impasse, no rule at all."""
    if kind == BLIND:
        return BLIND_BASE
    return v2e.render_base(shown, kind, engine, case)


def build_base(engine, case: Case, undefeated) -> tuple[list, str, str]:
    """What the first call shows: the rules in conflict on a CONFLICT, nothing on
    an impasse. The loop passes `undefeated` only on a CONFLICT."""
    if undefeated:
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, render_base(shown, kind, engine, case)
    return [], BLIND, BLIND_BASE


# ---------------------------------------------------------------------------
# The validator's two additions
# ---------------------------------------------------------------------------

split_overlapped = v2e.split_overlapped


def listing(rule_ids: list[str], idx: int, round_: int) -> list[str]:
    """v2e's listing order, seeded by this plan's constant: shuffled by the plan,
    the case and the round, so that a slot effect can be read afterwards and a
    resumed run lists the rules the same way."""
    order = sorted(rule_ids)
    random.Random(f"{plan.LISTING_SEED}/{idx}/{round_}").shuffle(order)
    return order


def same_rule(first, second, space) -> bool:
    """The placement answer's rule is the draft's when it sends the tickets to
    the same queue and covers exactly the same cases of the space."""
    return (first.action == second.action
            and space.extension(first.conditions) == space.extension(second.conditions))


def placement_message(engine, rule_ids: list[str]) -> str:
    by_id = {r.rule_id: r for r in engine.rules}
    return PLACEMENT_TEMPLATE.format(
        lista="\n".join("  " + by_id[rid].render() for rid in rule_ids))


def messages_for(case: Case, base_text: str, previous: "e.Answer | None" = None,
                 message: str = "") -> list[dict[str, str]]:
    """What a call sends: v2b's system prompt and v1's user message, and for a
    second round the first answer as the assistant's turn and the message after
    it. A module function, so that a resumed run can check a stored answer
    against the request without building the client."""
    out = [{"role": "system", "content": SYSTEM_PROMPT_V2B},
           {"role": "user", "content": user_msg(case, base_text)}]
    if previous is not None:
        out += [{"role": "assistant", "content": previous.raw},
                {"role": "user", "content": message}]
    return out


# ---------------------------------------------------------------------------
# The proposer
# ---------------------------------------------------------------------------

class ProposerV2B(v2e.ProposerV2E):
    """v2e's `ProposerV2E` with v2b. Built only after the gate, the key check and
    the blocking checks have spoken (`blind/run.py`)."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = 2,
                 reasoning: dict[str, Any] | None = None):
        super().__init__(model=model, max_retries=max_retries, reasoning=reasoning)
        self.name = f"openrouter2b({model},{plan.PROMPT})"
        self.prompt_version = plan.PROMPT
        self.system_prompt = SYSTEM_PROMPT_V2B

    def build_base(self, engine, case: Case, undefeated):
        return build_base(engine, case, undefeated)

    def first(self, case: Case, base_text: str, idx: int | None = None) -> e.Answer:
        return self.ask(messages_for(case, base_text))

    def repair(self, case: Case, base_text: str, previous: e.Answer, message: str,
               idx: int | None = None) -> e.Answer:
        return self.ask(messages_for(case, base_text, previous, message))


assert MAX_SHOWN == plan.MAX_SHOWN, "v2's neighbourhood is not the plan's"
