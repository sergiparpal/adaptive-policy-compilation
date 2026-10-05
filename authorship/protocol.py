"""
v1e — rung 2's prompt v1 and the four changes of §5 of `PLAN_AUTHORSHIP.md`,
and nothing else.

THE TEXTS. v1e is built from `rung2.proposers2.SYSTEM_PROMPT_V1` by replacing
one paragraph, the way v2 was built, and the replacement is asserted to have
applied. Two more texts go with it: the paragraph a CONFLICT escalation adds,
which offers the order answer and warns against copies (§5.3), and the repair
message (§5.2). `fingerprint()` hashes the three, and `E-g3` refuses if it is
not the one `plan.FINGERPRINT` declares. **After §0 is signed none of them
moves**, hard rule 5.

THE VALIDATOR'S PURE PARTS (§5.2): a copy is a rule whose extension equals an
existing rule's; `O` is every existing rule whose extension meets the new
rule's; a rule of `O` is placed when `beats` or `loses_to` cites it and the
citation is allowed, shown or listed; a repair round lists what is missing in an
order shuffled by a fixed seed. The loop applies them; they decide nothing on
their own.

THE PROPOSER is rung 2's `OpenRouterProposer2` with v1e's system prompt, v1e's
rendering of a CONFLICT, and two things v1 never kept: each answer's raw text,
which a repair round sends back as the assistant's turn, and its
`finish_reason`, which §5.4 records on every call. Its retries are v1's.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

from harness.domain import Case

from rung2.proposers2 import (MAX_SHOWN, SYSTEM_PROMPT_V1, OpenRouterProposer2,
                              ProposalError, neighbourhood, parse_payload,
                              render_base_v1, user_msg)

from . import plan

# --- §5.1: the paragraph v1e replaces, and what replaces it ------------------

V1_PARAGRAPH = """Por eso solo necesitas declarar prioridad frente a reglas que se solapan con la
tuya sin que una contenga a la otra. Si tu regla es un caso particular de otra,
no declares nada: el nivel 1 ya lo resuelve."""

V1E_PARAGRAPH = """Tienes que situar tu regla frente a TODA regla existente con la que se solape,
la contenga o no: si tu regla es una EXCEPCION a ella, de modo que la tuya manda
donde casen las dos, ponla en `beats`; si es un caso GENERAL por debajo de ella,
de modo que la otra manda, ponla en `loses_to`. Si tu regla esta contenida en
otra, el nivel 1 ya la hace ganar: declararla excepcion lo confirma, y
declararla caso general lo contradice, y el motor lo registrara. Una regla que
se solape con otra sin situarse frente a ella se te devolvera con la lista de
las que faltan."""

SYSTEM_PROMPT_V1E = SYSTEM_PROMPT_V1.replace(V1_PARAGRAPH, V1E_PARAGRAPH)
assert SYSTEM_PROMPT_V1E != SYSTEM_PROMPT_V1, "la sustitucion de la v1e no aplico"

# --- §5.3: what a CONFLICT escalation adds -------------------------------------

ORDER_PARAGRAPH = """Si este ticket ha escalado porque varias reglas existentes chocan, puedes, en
lugar de escribir una regla nueva, ordenarlas entre si. Responde entonces
{"action": "<cola para este ticket>", "order": [{"winner": "<id>", "loser":
"<id>"}], "note": "<una frase>"}, citando solo reglas de la lista. No escribas
una copia de una regla existente: una regla que cubre exactamente los mismos
casos que otra se rechaza."""

# --- §5.2: the repair round -----------------------------------------------------

REPAIR_TEMPLATE = """Tu regla se solapa con estas reglas existentes, frente a las que no te has
situado:
{lista}
Responde de nuevo con el mismo formato y cita cada una en `beats` o `loses_to`,
o cambia la regla."""

# The verdicts an escalation can end in, §5.
BORN = "nacida"
COPY = "copia"
UNPLACED = "sin_situar"
ORDER = "orden"
ORDER_WITHOUT_CONFLICT = "orden_sin_conflicto"
REJECTED = "rechazada"
FAILED = "fallida"
OUTSIDE = "fuera_del_vecindario"
MALFORMED_PAIR = "par_mal_formado"

# The two channels an installed edge can come through, §5.3.
WRITE = "write"
ORDER_CHANNEL = "order"


def fingerprint() -> str:
    """The three texts v1e adds to v1, hashed. `E-g3` compares it with
    `plan.FINGERPRINT`."""
    body = json.dumps([SYSTEM_PROMPT_V1E, ORDER_PARAGRAPH, REPAIR_TEMPLATE],
                      ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def render_base(shown, kind: str, engine=None, case=None) -> str:
    """v1's rendering, and on a CONFLICT the paragraph of §5.3 after it."""
    text = render_base_v1(shown, kind, engine, case)
    return text + "\n" + ORDER_PARAGRAPH + "\n" if kind == "conflicto" else text


# ---------------------------------------------------------------------------
# The validator's pure parts
# ---------------------------------------------------------------------------

def copies_of(engine, ext: int) -> list[str]:
    """Existing rules covering exactly the tickets `ext` covers, in base order."""
    return [r.rule_id for r in engine.rules if engine.ext[r.rule_id] == ext]


def overlapped(engine, ext: int) -> list[str]:
    """`O`: every existing rule whose extension meets `ext`, in base order."""
    return [r.rule_id for r in engine.rules if engine.ext[r.rule_id] & ext]


def citations(payload: dict, direction: str) -> list[str]:
    """`beats` or `loses_to` as the loop reads them: a string is one citation,
    anything but a list is none, and every citation is a stripped string."""
    raw = payload.get(direction) or []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    return [str(ref).strip() for ref in raw]


def unplaced(o: list[str], payload: dict, allowed: set[str]) -> list[str]:
    """The rules of `O` the answer does not place: not cited, or cited without
    having been shown or listed."""
    placed = {ref for d in ("beats", "loses_to") for ref in citations(payload, d)
              if ref in allowed}
    return [rid for rid in o if rid not in placed]


def listing(rule_ids: list[str], idx: int, round_: int) -> list[str]:
    """The order a repair round lists its rules in: shuffled with a seed fixed
    by the plan, the case and the round, so that a slot effect can be read
    afterwards (§6.5) and a resumed run lists them the same way."""
    order = sorted(rule_ids)
    random.Random(f"{plan.LISTING_SEED}/{idx}/{round_}").shuffle(order)
    return order


def repair_message(engine, rule_ids: list[str]) -> str:
    by_id = {r.rule_id: r for r in engine.rules}
    return REPAIR_TEMPLATE.format(
        lista="\n".join("  " + by_id[rid].render() for rid in rule_ids))


def messages_for(case: Case, base_text: str, previous: "Answer | None" = None,
                 message: str = "") -> list[dict[str, str]]:
    """What a call sends: v1e's system prompt and v1's user message, and for a
    repair round the first answer as the assistant's turn and the repair message
    after it. A module function, so that a resumed run can check a stored
    answer against the request without building the client."""
    out = [{"role": "system", "content": SYSTEM_PROMPT_V1E},
           {"role": "user", "content": user_msg(case, base_text)}]
    if previous is not None:
        out += [{"role": "assistant", "content": previous.raw},
                {"role": "user", "content": message}]
    return out


def is_order(payload: dict) -> bool:
    """An answer carrying `order` is an order answer, whatever else it carries."""
    return "order" in payload


def order_pairs(payload: dict) -> list[tuple[str, str] | None]:
    """`order` as a list of (winner, loser); `None` stands for an entry that is
    not a pair, which the loop counts and refuses."""
    raw = payload.get("order")
    if not isinstance(raw, list):
        return [None]
    out: list[tuple[str, str] | None] = []
    for item in raw:
        if (isinstance(item, dict) and isinstance(item.get("winner"), str)
                and isinstance(item.get("loser"), str)):
            out.append((item["winner"].strip(), item["loser"].strip()))
        else:
            out.append(None)
    return out


# ---------------------------------------------------------------------------
# The proposer
# ---------------------------------------------------------------------------

@dataclass
class Answer:
    action: Any
    payload: dict
    raw: str
    finish_reason: str | None
    attempts: int


class ProposalFailed(ProposalError):
    """An answer that never parsed, with the `finish_reason` of its last try."""

    def __init__(self, message: str, finish_reason: str | None, attempts: int):
        super().__init__(message)
        self.finish_reason = finish_reason
        self.attempts = attempts


class ProposerE(OpenRouterProposer2):
    """`OpenRouterProposer2` with v1e. Built only after the gate, the key check
    and the blocking checks have spoken (`authorship/run.py`)."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = 2,
                 reasoning: dict[str, Any] | None = None):
        super().__init__(model=model, max_retries=max_retries,
                         prompt_version="v1", reasoning=reasoning)
        self.name = f"openrouter2e({model},{plan.PROMPT})"
        self.prompt_version = plan.PROMPT
        self.system_prompt = SYSTEM_PROMPT_V1E

    def build_base(self, engine, case: Case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, render_base(shown, kind, engine, case)

    def first(self, case: Case, base_text: str, idx: int | None = None) -> Answer:
        return self.ask(messages_for(case, base_text))

    def repair(self, case: Case, base_text: str, previous: Answer, message: str,
               idx: int | None = None) -> Answer:
        return self.ask(messages_for(case, base_text, previous, message))

    def ask(self, messages: list[dict[str, str]]) -> Answer:
        """v1's retries: JSON mode on the first try, and after a failure one
        nudge to answer with the object alone."""
        last: Exception | None = None
        finish: str | None = None
        for attempt in range(self.max_retries + 1):
            try:
                kwargs: dict[str, Any] = {
                    "model": self.model, "messages": messages,
                    "max_tokens": 1200, "temperature": 0,
                }
                if attempt == 0:
                    kwargs["response_format"] = {"type": "json_object"}
                if self.reasoning is not None:
                    kwargs["extra_body"] = {"reasoning": self.reasoning}
                resp = self._client.chat.completions.create(**kwargs)
                choice = resp.choices[0]
                finish = getattr(choice, "finish_reason", None)
                raw = choice.message.content or ""
                payload = parse_payload(raw)
                return Answer(payload.get("action"), payload, raw, finish, attempt + 1)
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0:
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content":
                         "Tu respuesta anterior no era JSON valido. Responde "
                         "UNICAMENTE con el objeto JSON, sin texto alrededor."},
                    ]
        raise ProposalFailed(str(last), finish, self.max_retries + 1)


assert MAX_SHOWN == plan.MAX_SHOWN, "v1's neighbourhood is not the plan's"
