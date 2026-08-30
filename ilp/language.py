"""
THE HYPOTHESIS LANGUAGE — the 224 conditions of §2, and what the inducer may say.

--------------------------------------------------------------------------
WHY IT IS DECLARED AND ENUMERATED
--------------------------------------------------------------------------
The DSL's condition space is not finite in a usable sense: `in` ranges over
subsets and `prior_tickets_30d` has 21 values, so `in` alone would contribute
2²¹ conditions on that one attribute. §2 of `PLAN_ILP.md` therefore declares the
language rather than inheriting it:

    eq        every attribute, every value                        47
    neq       every attribute, every value                        47
    lte, gte  the two numeric attributes                          50
    in        attributes with at most 5 values, subsets 2..n-1     80
                                                            ---------
                                                                  224

**The `in` restriction is the decision that could have invalidated the plan in
silence.** `customer_tier` has FOUR values — `free`, `pro`, `business`,
`enterprise` — so the hidden policy's `customer_tier in [business, enterprise]`
is **not** `neq free`, which would also admit `pro`. Dropping `in`, or keeping
only complements, would put the target outside the language and make `I-g1`
unreachable for a reason that has nothing to do with induction. `I-g2` checks it
against the 29 rules rather than arguing it here.

--------------------------------------------------------------------------
WHAT THIS MODULE DOES NOT DO
--------------------------------------------------------------------------
**It does not enumerate bodies.** Conjunctions of up to three of these
conditions that cover at least one training case number **839,070** on the real
training set, and one `covers(body, case)` fact per pair would ground to hundreds
of millions of atoms. `induce.py` therefore lets the solver choose conditions per
rule slot, which searches the same space with a grounding linear in the number of
conditions. The count is recorded here because it is the reason for that design
and `results_ilp/induce_check.json` reports it.

It measures nothing and it never sees a label.
"""

from __future__ import annotations

import itertools
from functools import lru_cache

from harness.domain import ATTRIBUTES, DOMAINS, NUMERIC_ATTRS
from harness.dsl import Condition

MAX_IN_DOMAIN = 5          # attributes with more values get no `in`
MAX_CONDITIONS = 3         # the hidden policy's own maximum body size


@lru_cache(maxsize=None)
def language() -> tuple[tuple, ...]:
    """The 224 conditions, as hashable triples in a fixed order.

    Order is deterministic and is the identity the ASP encoding uses, so a
    grounded program is reproducible across runs."""
    out: list[tuple] = []
    for attr in ATTRIBUTES:
        values = DOMAINS[attr]
        for v in values:
            out.append((attr, "eq", v))
        for v in values:
            out.append((attr, "neq", v))
        if attr in NUMERIC_ATTRS:
            for v in values:
                out.append((attr, "lte", v))
            for v in values:
                out.append((attr, "gte", v))
        if len(values) <= MAX_IN_DOMAIN:
            for k in range(2, len(values)):
                for combo in itertools.combinations(values, k):
                    out.append((attr, "in", tuple(combo)))
    return tuple(out)


def as_condition(triple) -> Condition:
    """A language triple as a frozen-DSL `Condition`. `in` carries a list, which
    is what `validate_rule_payload` requires and what `Condition.holds` expects."""
    attr, op, value = triple
    return Condition(attr=attr, op=op,
                     value=list(value) if op == "in" else value)


def render(triple) -> str:
    attr, op, value = triple
    if op == "in":
        return f"{attr} in {list(value)}"
    return f"{attr} {op} {value}"


def holds_matrix(cases) -> list[int]:
    """Per condition, a bitmask over `cases`. Bit `k` is case `k`, LSB-first —
    the opposite convention to `rung2.engine2.Space`, and local to this package
    so that nothing here has to reason about the other one."""
    conds = [as_condition(t) for t in language()]
    out = []
    for cond in conds:
        mask = 0
        for k, case in enumerate(cases):
            if cond.holds(case):
                mask |= 1 << k
        out.append(mask)
    return out


def body_extension(body, holds: list[int], full: int) -> int:
    """A conjunction is the AND of its conditions' masks."""
    acc = full
    for i in body:
        acc &= holds[i]
        if not acc:
            break
    return acc


def count_candidate_bodies(holds: list[int], full: int,
                           max_conditions: int = MAX_CONDITIONS) -> dict:
    """How many conjunctions of up to `max_conditions` conditions, with distinct
    attributes, cover at least one case.

    This is the number that decides the encoding, so it is measured rather than
    asserted, and `induce_check.py` publishes it."""
    lang = language()
    by_attr: dict[str, list[int]] = {}
    for i, triple in enumerate(lang):
        if holds[i]:
            by_attr.setdefault(triple[0], []).append(i)
    attrs = sorted(by_attr)
    per_size = {}
    for k in range(1, max_conditions + 1):
        n = 0
        for combo in itertools.combinations(attrs, k):
            for picks in itertools.product(*(by_attr[a] for a in combo)):
                if body_extension(picks, holds, full):
                    n += 1
        per_size[k] = n
    return {"per_size": per_size, "total": sum(per_size.values()),
            "conditions_covering_a_case": sum(len(v) for v in by_attr.values())}
