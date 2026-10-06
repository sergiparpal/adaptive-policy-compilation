"""
v2e — rung 2's prompt v2 with v1e's discipline, asked only where the queues
differ: §5 of `PLAN_OVERLAP.md`, and nothing else.

THE TEXTS. v2e is built from `rung2.proposers2.SYSTEM_PROMPT_V2` by replacing one
sentence, the way v2 and v1e were built from v1, and the replacement is asserted
to have applied. The paragraph a CONFLICT escalation adds is v1e's, called from
`authorship/protocol.py`. The repair message is v1e's with the missing rules
named as rules of another queue. `fingerprint()` hashes the three, and `O-g3`
refuses if it is not the one `plan.FINGERPRINT` declares. **After §0 is signed
none of them moves**, hard rule 5.

THE VALIDATOR'S ONE CHANGE (§5.2). `O` is every existing rule whose extension
meets the new rule's **and whose queue differs from the new rule's**. `S`, the
overlapped rules of the same queue, is recorded and owes nothing. Every other
part of the validator is v1e's, called from `authorship/protocol.py`: the copy
check, what counts as placed, and the citations.

THE PROPOSER is v1e's `ProposerE` with v2e's system prompt, v2's rendering of
the base with the engine's set arithmetic, and on a CONFLICT the order paragraph
after it. Its retries, and the raw text and `finish_reason` it keeps, are v1e's.
"""

from __future__ import annotations

import hashlib
import json
import random
from typing import Any

from harness.domain import Case

from authorship import protocol as e
from rung2.proposers2 import MAX_SHOWN, SYSTEM_PROMPT_V2, neighbourhood, render_base_v2, user_msg

from . import plan

# --- §5.1: the sentence of v2 that v2e replaces, and what replaces it --------

V2_SENTENCE = """Si tu regla es un caso particular de otra (todo caso que casa la tuya casa
tambien la otra), no declares nada: el nivel 1 ya lo resuelve solo."""

V2E_SENTENCE = """Tienes que situar tu regla frente a TODA regla existente con la que se solape y
que mande los tickets a OTRA cola, la contenga o no: si tu regla es una EXCEPCION
a ella, de modo que la tuya manda donde casen las dos, ponla en `beats`; si es un
caso GENERAL por debajo de ella, de modo que la otra manda, ponla en `loses_to`.
Si una de las dos contiene a la otra, el nivel 1 ya hace ganar a la mas
contenida: declararlo lo confirma, declarar lo contrario lo contradice, y el motor
lo registrara. Frente a una regla de tu MISMA cola no declares nada: donde se
pisan deciden lo mismo. Una regla que se solape con otra de distinta cola sin
situarse frente a ella se te devolvera con la lista de las que faltan."""

SYSTEM_PROMPT_V2E = SYSTEM_PROMPT_V2.replace(V2_SENTENCE, V2E_SENTENCE)
assert SYSTEM_PROMPT_V2E != SYSTEM_PROMPT_V2, "la sustitucion de la v2e no aplico"

# --- §5.3: what a CONFLICT escalation adds, v1e's ------------------------------

ORDER_PARAGRAPH = e.ORDER_PARAGRAPH

# --- §5.2: the repair round ------------------------------------------------------

REPAIR_TEMPLATE = """Tu regla se solapa con estas reglas existentes de OTRA cola, frente a las que no
te has situado:
{lista}
Responde de nuevo con el mismo formato y cita cada una en `beats` o `loses_to`,
o cambia la regla."""


def fingerprint() -> str:
    """The three texts v2e adds to v2, hashed. `O-g3` compares it with
    `plan.FINGERPRINT`."""
    body = json.dumps([SYSTEM_PROMPT_V2E, ORDER_PARAGRAPH, REPAIR_TEMPLATE],
                      ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def render_base(shown, kind: str, engine=None, case=None) -> str:
    """v2's rendering, the engine's set arithmetic included, and on a CONFLICT
    the paragraph of §5.3 after it."""
    text = render_base_v2(shown, kind, engine, case)
    return text + "\n" + ORDER_PARAGRAPH + "\n" if kind == "conflicto" else text


# ---------------------------------------------------------------------------
# The validator's one change
# ---------------------------------------------------------------------------

def split_overlapped(engine, ext: int, action: Any) -> tuple[list[str], list[str]]:
    """`O` and `S`: the existing rules whose extension meets `ext`, those of
    another queue and those of `action`'s, each in base order."""
    o, s = [], []
    for r in engine.rules:
        if engine.ext[r.rule_id] & ext:
            (s if r.action == action else o).append(r.rule_id)
    return o, s


def listing(rule_ids: list[str], idx: int, round_: int) -> list[str]:
    """v1e's listing order, seeded by this plan's constant: shuffled by the plan,
    the case and the round, so that a slot effect can be read afterwards and a
    resumed run lists the rules the same way."""
    order = sorted(rule_ids)
    random.Random(f"{plan.LISTING_SEED}/{idx}/{round_}").shuffle(order)
    return order


def repair_message(engine, rule_ids: list[str]) -> str:
    by_id = {r.rule_id: r for r in engine.rules}
    return REPAIR_TEMPLATE.format(
        lista="\n".join("  " + by_id[rid].render() for rid in rule_ids))


def messages_for(case: Case, base_text: str, previous: "e.Answer | None" = None,
                 message: str = "") -> list[dict[str, str]]:
    """What a call sends: v2e's system prompt and v1's user message, and for a
    repair round the first answer as the assistant's turn and the repair message
    after it. A module function, so that a resumed run can check a stored answer
    against the request without building the client."""
    out = [{"role": "system", "content": SYSTEM_PROMPT_V2E},
           {"role": "user", "content": user_msg(case, base_text)}]
    if previous is not None:
        out += [{"role": "assistant", "content": previous.raw},
                {"role": "user", "content": message}]
    return out


# ---------------------------------------------------------------------------
# The proposer
# ---------------------------------------------------------------------------

class ProposerV2E(e.ProposerE):
    """v1e's `ProposerE` with v2e. Built only after the gate, the key check and
    the blocking checks have spoken (`overlap/run.py`)."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = 2,
                 reasoning: dict[str, Any] | None = None):
        super().__init__(model=model, max_retries=max_retries, reasoning=reasoning)
        self.name = f"openrouter2e({model},{plan.PROMPT})"
        self.prompt_version = plan.PROMPT
        self.system_prompt = SYSTEM_PROMPT_V2E

    def build_base(self, engine, case: Case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, render_base(shown, kind, engine, case)

    def first(self, case: Case, base_text: str, idx: int | None = None) -> e.Answer:
        return self.ask(messages_for(case, base_text))

    def repair(self, case: Case, base_text: str, previous: e.Answer, message: str,
               idx: int | None = None) -> e.Answer:
        return self.ask(messages_for(case, base_text, previous, message))


assert MAX_SHOWN == plan.MAX_SHOWN, "v2's neighbourhood is not the plan's"
