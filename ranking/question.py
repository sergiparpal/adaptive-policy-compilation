"""
The question of `PLAN_RANKING.md`, its twelve presentations, and what makes an
answer valid. And `M-g2`: the question reads nothing but the eight names.

THE QUESTION IS THE PAIRWISE ONE, ASKED ONCE IN GENERAL (§2.1). `rung2/
pair_judgement.py` asked which queue a ticket goes to when two rules of the
manual match it, send it to different queues and neither contains the other.
This asks for the fixed order between the queues that would answer every such
pair at once, which is exactly what `rung3/queue_hierarchy_floor.py` applies:
of two queues, the one earlier in the order wins. The wording follows the
judge's system prompt, in Spanish and without accents, as that prompt is.

WHAT THE MODEL SEES, AND NOTHING ELSE. The system prompt is a constant and
names no queue. The user message is a header and the eight names, one per line,
in the presentation's order. So each name appears exactly once in the whole
request, and the only thing a presentation varies is the order the names are
offered in (§5.2). No ticket, no rule, no condition, no label and no description
of any queue reaches the model: a ticket or a rule cannot be rendered without
an attribute name, and `M-g2` checks the whole request for every one of them.

**The attribute VALUES are not checked as tokens, and that is deliberate.**
Three of them are two-letter language codes, `en`, `es` and `de`, which are
also Spanish words; a check on them would fail on the question's own grammar.
`PLAN_WHY.md` learned the same thing the other way round, when `m[aá]s
condiciones` matched inside *mismas condiciones*. The values a rendered ticket
would carry come with their attribute names, and those are checked.

THE PRESENTATIONS (§2.2). Presentation 1 is `harness.domain.ACTIONS`'s own
order, the one every prompt in the tree has used. Presentations 2 to 12 are
drawn from `plan.presentation_rng()`, each a permutation distinct from every
other and from the first. They are a function of the seed alone.

WHAT MAKES AN ANSWER VALID (§0). Its `ranking` is a list of exactly the eight
queue names, each once, with no other entry. Surrounding whitespace is stripped
and nothing else is forgiven: a lower-cased name, a tie, an omission, a
repetition or an invented queue is invalid, and an invalid answer is recorded
and excluded, never repaired. What the model writes beyond its ranking is
recorded and never executed (rule E).
"""

from __future__ import annotations

import hashlib
import inspect
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from harness.domain import ATTRIBUTES, DOMAINS

from . import plan

SYSTEM_PROMPT = """Eres el arbitro de un sistema de triaje de tickets.

A veces dos reglas del manual casan el mismo ticket y lo mandan a colas
DISTINTAS, y ninguna de las dos esta contenida en la otra, asi que la estructura
no decide: hace falta un criterio.

El criterio que se te pide es un orden fijo entre las colas, el mismo para
cualquier ticket y cualquier par de reglas: de dos colas, gana la que va antes
en el orden.

Tu unica tarea es dar ese orden, desde la cola que gana a todas las demas hasta
la que pierde con todas.

NO escribas reglas. NO propongas cambios en el manual. NO expliques como deberia
arbitrar el motor. Solo el orden.

Responde UNICAMENTE con un objeto JSON, sin texto alrededor:

  {"ranking": ["<COLA>", "<COLA>", ...], "why": "<una frase, como maximo 30 palabras>"}

`ranking` tiene que contener exactamente las colas de la lista, cada una una
sola vez y sin empates.
"""

HEADER = "LAS COLAS:"
RETRY_MSG = ("Tu respuesta anterior no era JSON valido. Responde UNICAMENTE "
             "con el objeto JSON, sin texto alrededor.")

# A queue-shaped token: upper case with at least one underscore. Every queue is
# one, and no other word of the question is.
QUEUE_SHAPED = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
# The rule ids of both bases: rung 1's R0001..R0577 and the hidden policy's
# H01..H29 as the pairwise thread showed them.
RULE_SHAPED = re.compile(r"\b(?:R\d{4}|H\d{2})\b")


def user_message(order: Sequence[str]) -> str:
    """The user message: the header and the names, one per line. It takes the
    order and nothing else, which `M-g2` checks on its signature."""
    return "\n".join([HEADER] + [f"  {q}" for q in order])


def messages(order: Sequence[str]) -> list[dict[str, str]]:
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message(order)}]


def digest(order: Sequence[str]) -> str:
    """The request's content, hashed: both messages, as sent."""
    return hashlib.sha256(json.dumps(messages(order), sort_keys=True)
                          .encode()).hexdigest()


# ---------------------------------------------------------------------------
# The presentations, and the order of each pass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Presentation:
    pid: str                 # "p01" .. "p12"
    order: tuple[str, ...]
    digest: str


def presentations() -> list[Presentation]:
    """Presentation 1 is the domain's order; the rest are drawn without
    repetition from the plan's stream."""
    first = tuple(plan.QUEUES)
    orders = [first]
    seen = {first}
    rng = plan.presentation_rng()
    while len(orders) < plan.PRESENTATIONS:
        o = list(first)
        rng.shuffle(o)
        t = tuple(o)
        if t not in seen:
            seen.add(t)
            orders.append(t)
    return [Presentation(f"p{k:02d}", o, digest(o)) for k, o in enumerate(orders, 1)]


def pass_orders(pres: list[Presentation]) -> list[list[str]]:
    """The order of each pass of the session, one stream per pass."""
    out = []
    for p in range(1, plan.PASSES + 1):
        ids = [x.pid for x in pres]
        plan.order_rng(p).shuffle(ids)
        out.append(ids)
    return out


def smoke_order(pres: list[Presentation]) -> list[str]:
    """The smoke run asks presentations 1 and 2, once each, in that order."""
    return [x.pid for x in pres[:plan.SMOKE_ASKS]]


# ---------------------------------------------------------------------------
# What makes an answer valid
# ---------------------------------------------------------------------------

def ranking_of(payload: Any) -> list[str] | None:
    """The answer's ranking if it is valid, None otherwise. Whitespace around a
    name is stripped and nothing else is forgiven."""
    if not isinstance(payload, dict):
        return None
    r = payload.get("ranking")
    if not isinstance(r, list) or len(r) != len(plan.QUEUES):
        return None
    if not all(isinstance(q, str) for q in r):
        return None
    names = [q.strip() for q in r]
    if sorted(names) != sorted(plan.QUEUES):
        return None
    return names


# ---------------------------------------------------------------------------
# M-g2 — the question reads nothing but the eight names
# ---------------------------------------------------------------------------

def _tokens(pattern: re.Pattern, text: str) -> list[str]:
    return pattern.findall(text)


def leaks(order: Sequence[str], rule_ids: set[str]) -> list[str]:
    """Everything the request for `order` carries beyond the eight names."""
    problems = []
    whole = SYSTEM_PROMPT + "\n" + user_message(order)
    for q in plan.QUEUES:
        n = len(re.findall(rf"\b{re.escape(q)}\b", whole))
        if n != 1:
            problems.append(f"{q} appears {n} times")
    extra = sorted(set(_tokens(QUEUE_SHAPED, whole)) - set(plan.QUEUES))
    if extra:
        problems.append(f"queue-shaped tokens that are no queue: {extra}")
    for attr in ATTRIBUTES:
        if re.search(rf"\b{re.escape(attr)}\b", whole):
            problems.append(f"attribute name {attr}")
    long_values = {v for vals in DOMAINS.values() for v in vals
                   if isinstance(v, str) and len(v) >= 3}
    for v in sorted(long_values):
        if re.search(rf"\b{re.escape(v)}\b", whole):
            problems.append(f"attribute value {v}")
    ids = set(_tokens(RULE_SHAPED, whole)) | {r for r in rule_ids
                                              if re.search(rf"\b{re.escape(r)}\b", whole)}
    if ids:
        problems.append(f"rule ids {sorted(ids)}")
    if user_message(order).splitlines() != [HEADER] + [f"  {q}" for q in order]:
        problems.append("the user message is not the header and the names")
    return problems


def rule_ids(path: Path | None = None) -> set[str]:
    rec = json.loads((path or plan.RULES).read_text())
    return {r["rule_id"] for r in rec["rules"]}


def gate_mg2(pres: list[Presentation] | None = None,
             ids: set[str] | None = None) -> dict[str, Any]:
    pres = presentations() if pres is None else pres
    ids = rule_ids() if ids is None else ids
    problems: list[str] = []
    for p in pres:
        problems += [f"{p.pid}: {x}" for x in leaks(p.order, ids)]
        if sorted(p.order) != sorted(plan.QUEUES):
            problems.append(f"{p.pid}: not a permutation of the eight queues")
        if p.digest != digest(p.order):
            problems.append(f"{p.pid}: its digest is not its request's")
    if len(pres) != plan.PRESENTATIONS:
        problems.append(f"{len(pres)} presentations, not {plan.PRESENTATIONS}")
    if pres and pres[0].order != tuple(plan.QUEUES):
        problems.append("presentation 1 is not the domain's own order")
    if len({p.order for p in pres}) != len(pres):
        problems.append("two presentations share an order")
    if len({p.digest for p in pres}) != len(pres):
        problems.append("two presentations share a digest")
    if [(p.pid, p.order) for p in presentations()] != [(p.pid, p.order) for p in pres]:
        problems.append("the presentations are not the seed's")
    # Teeth: the first two names of presentation 1 swapped must move its digest.
    o = list(plan.QUEUES)
    o[0], o[1] = o[1], o[0]
    teeth = digest(o) != digest(plan.QUEUES)
    if not teeth:
        problems.append("a changed order does not move the digest")
    takes = list(inspect.signature(user_message).parameters)
    if takes != ["order"]:
        problems.append(f"the user message takes {takes}, not the order alone")
    for p in pres:
        if any(m["role"] == "system" and m["content"] != SYSTEM_PROMPT
               for m in messages(p.order)):
            problems.append(f"{p.pid}: another system prompt")
    return {
        "what": "every request carries the eight queue names, each exactly once, "
                "and nothing else of the policy: no ticket, no rule, no attribute "
                "name, no label and no description; the presentations are the "
                "seed's, distinct, and a changed order moves the digest",
        "presentations": len(pres),
        "digests": {p.pid: p.digest for p in pres},
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "teeth": teeth,
        "problems": problems,
        "passes": not problems,
    }
