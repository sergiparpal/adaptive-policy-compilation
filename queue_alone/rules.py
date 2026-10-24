"""
The 29 rules, read from level 3's frozen text, for §5.6's classes. **Stage C's,
and `QA-g1`'s; never the proposer's.**

WHY THE TEXT AND NOT THE ORACLE. Level 3 hands the model the hidden policy as
text: the 29 rules in order, under *"Se aplica la primera regla de la lista
cuyas condiciones casa el ticket."* (`manual/texts/rules.txt`, pinned by digest
in `PLAN_MANUAL.md` §5). §5.6 classifies an answer against the rules the model
was shown, so it reads them where the model did. That keeps the list of modules
allowed to see the oracle as it is (§4, rule B of the plan). `QA-g1` holds the
reading to the truth: by first match it gives every escalated ticket the queue
its loop record says is true.

THE GRAMMAR is the text's, one rule a line:

    H07: SI severity eq 1 AND product eq api ENTONCES T3_ENGINEERING

A value is `True` or `False`, an integer, a Python list of strings, or a bare
word. The operators are v1's five.

§5.6's CLASSES, for an answer to a ticket:
- **first**: the queue of the first rule the ticket matches, which is its truth;
- **order**: another queue, given by a rule the ticket also matches, lower in
  the list;
- **matching**: a queue no rule the ticket matches gives.
Beside them, the queue of the matching rule with the most conditions, the first
such in the list: how rung 1's engine arbitrated by specificity.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from manual import levels

LINE = re.compile(r"^(H\d{2}): SI (.+) ENTONCES ([A-Z][A-Z0-9_]*)$")
CONDITION = re.compile(r"^(\w+) (eq|neq|lte|gte|in) (.+)$")
CLASSES = ("first", "order", "matching")


@dataclass(frozen=True)
class Rule:
    id: str
    conditions: tuple[tuple[str, str, Any], ...]
    queue: str

    def matches(self, ticket: dict[str, Any]) -> bool:
        return all(holds(ticket[attr], op, value) for attr, op, value in self.conditions)


def value_of(text: str) -> Any:
    if text in ("True", "False"):
        return text == "True"
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if text.startswith("["):
        return tuple(ast.literal_eval(text))
    return text


def holds(x: Any, op: str, v: Any) -> bool:
    if op == "eq":
        return x == v
    if op == "neq":
        return x != v
    if op == "lte":
        return x <= v
    if op == "gte":
        return x >= v
    if op == "in":
        return x in v
    raise ValueError(f"no operator {op!r}")


def parse(text: str) -> tuple[Rule, ...]:
    """Every rule line of the text, in its order. A line that starts like a rule
    and does not parse is an error, never skipped."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("H"):
            continue
        m = LINE.match(line)
        if not m:
            raise ValueError(f"not a rule line: {line!r}")
        conds = []
        for part in m.group(2).split(" AND "):
            c = CONDITION.match(part.strip())
            if not c:
                raise ValueError(f"not a condition: {part!r} in {line!r}")
            conds.append((c.group(1), c.group(2), value_of(c.group(3))))
        out.append(Rule(id=m.group(1), conditions=tuple(conds), queue=m.group(3)))
    return tuple(out)


@lru_cache(maxsize=None)
def rules() -> tuple[Rule, ...]:
    """Level 3's text, as `manual.levels` hands it to the model."""
    return parse(levels.text(3))


def matching(ticket: dict[str, Any], rs: tuple[Rule, ...] | None = None) -> list[Rule]:
    """The rules the ticket matches, in the list's order."""
    return [r for r in (rules() if rs is None else rs) if r.matches(ticket)]


def first_queue(ticket: dict[str, Any], rs: tuple[Rule, ...] | None = None) -> str | None:
    hit = matching(ticket, rs)
    return hit[0].queue if hit else None


def most_conditions_queue(ticket: dict[str, Any],
                          rs: tuple[Rule, ...] | None = None) -> str | None:
    """The queue of the matching rule with the most conditions, the first such
    in the list."""
    hit = matching(ticket, rs)
    if not hit:
        return None
    return max(hit, key=lambda r: (len(r.conditions), -hit.index(r))).queue


def classify(answer: str, ticket: dict[str, Any],
             rs: tuple[Rule, ...] | None = None) -> str:
    """§5.6's class of one answer to one ticket."""
    hit = matching(ticket, rs)
    if hit and answer == hit[0].queue:
        return "first"
    if any(answer == r.queue for r in hit[1:]):
        return "order"
    return "matching"
