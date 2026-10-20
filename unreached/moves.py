"""
REACH AND THE MOVES — `PLAN_UNREACHED.md` §3. Nothing here reads the truth.

**Reach.** A rule is reached by a labelled set when it matches one of the set's
cases in the `puro` pool, the pool the search's masks are built on. The search
counts the labelled cases decided right, first match wins, so a rule no labelled
case matches never changes its objective. The local search applies no move on a
tie, so such a rule is never moved for itself: it stays where the start put it,
and moves only when a swap carries it.

**The moves**, each a permutation of a searched order:

  front(order, rid)          the rule first, every other rule as it was;
  back(order, unreached)     every rule a label reaches, in the order's order,
                             then the unreached, in the order's order;
  coin(order, unreached, d)  the rules a label reaches in the order's order,
                             and the unreached at random places among them,
                             seeded by `COIN_SEED + d`.

**Copies.** Rules written the same, conditions and queue, make the same move, so
`distinct` keeps the earliest-born of each.

It reads matching, rule ids, conditions, queues, birth indices and ticket keys.
`tests/test_unreached.py` walks its syntax tree to say that it names no truth,
in a name or in a string literal, and `Z-g2` does so again before any record.
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Iterable, Sequence

from . import plan


def reached(matched, cases: Iterable[int]) -> set[str]:
    """Every rule that matches one of `cases`."""
    out: set[str] = set()
    for i in cases:
        out.update(matched[i])
    return out


def unreached(ids: Sequence[str], matched, cases: Iterable[int]) -> list[str]:
    """The rules no case of `cases` matches, in the base's order."""
    hit = reached(matched, cases)
    return [rid for rid in ids if rid not in hit]


def front(order: Sequence[str], rid: str) -> list[str]:
    """`rid` first, every other rule as it was."""
    if rid not in order:
        raise ValueError(f"{rid} is not in the order")
    return [rid] + [r for r in order if r != rid]


def back(order: Sequence[str], unreached_rules: Iterable[str]) -> list[str]:
    """The reached rules in the order's order, then the unreached in theirs."""
    u = set(unreached_rules)
    return [r for r in order if r not in u] + [r for r in order if r in u]


def coin(order: Sequence[str], unreached_rules: Iterable[str], d: int) -> list[str]:
    """The reached rules in the order's order, the unreached at seeded random
    places among them, in a seeded random order of their own."""
    u = set(unreached_rules)
    rest = [r for r in order if r not in u]
    moved = [r for r in order if r in u]
    rng = random.Random(plan.COIN_SEED + d)
    rng.shuffle(moved)
    slots = set(rng.sample(range(len(order)), len(moved)))
    a, b = iter(rest), iter(moved)
    return [next(b) if k in slots else next(a) for k in range(len(order))]


def text(rule: dict) -> tuple:
    """What a rule says: its conditions, in a canonical order, and its queue."""
    conds = tuple(sorted((c["attr"], c["op"], str(c["value"]))
                         for c in rule["conditions"]))
    return conds, rule["action"]


def copies(rules: Sequence[dict], rids: Iterable[str]) -> list[list[str]]:
    """The groups of `rids` written the same, each earliest-born first; only
    groups of two or more."""
    by = {r["rule_id"]: r for r in rules}
    groups: dict[tuple, list[str]] = defaultdict(list)
    for rid in rids:
        groups[text(by[rid])].append(rid)
    out = [sorted(g, key=lambda r: (by[r]["born_at"], r)) for g in groups.values()]
    return sorted((g for g in out if len(g) > 1), key=lambda g: g[0])


def distinct(rules: Sequence[dict], rids: Iterable[str]) -> list[str]:
    """One rule per text among `rids`, the earliest-born, in birth order."""
    by = {r["rule_id"]: r for r in rules}
    groups: dict[tuple, list[str]] = defaultdict(list)
    for rid in rids:
        groups[text(by[rid])].append(rid)
    first = [min(g, key=lambda r: (by[r]["born_at"], r)) for g in groups.values()]
    return sorted(first, key=lambda r: (by[r]["born_at"], r))


def birth_ticket(corpus, born_at: int, cases: Iterable[int]) -> set[int]:
    """The cases of `cases` whose ticket is the one the rule was written at."""
    key = corpus[born_at].key()
    return {i for i in cases if corpus[i].key() == key}
