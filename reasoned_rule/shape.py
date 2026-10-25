"""
The rules the two rule arms of `PLAN_REASONED_RULE.md` write, read against the
29 rules over the space. **Stage C's, for `RR-e`, which is reported; never the
proposer's, and never a row's.**

WHAT IS READ, for each valid answer of a rule arm (§0, `RR-e`):
- **whether its rule validates** under rung 2's validator,
  `rung2.engine2.validate_conditions`, called without the ticket, and the reason
  when it does not, cut as `apply/score.py` cuts it;
- **whether it matches its ticket**, which v1 requires of it;
- **its conditions**, counted;
- **its region over the space**: its points, and how many of them the list's
  first match sends to the rule's queue. A rule gets *all of it* when every
  point does;
- **whether its region is one of the 29 rules'**, and whether that rule is the
  one that governs its ticket, `m₁`;
- **its edges**: whether it declares `beats` or `loses_to`, and whether those
  cite the list's identifiers, `H01` to `H29`.

A RULE READ ALONE IS NOT A RULE COMPILED (§5.10 of the plan). Each rule is read as
the first rule of an empty base, which is what v1 tells the model it is. Nothing
here installs it, tries an edge, or says what it would decide among other rules
(rule E). **A narrower rule gets its region right more easily**, so its share is
never read without its points beside it.

THE LIST IS READ FROM LEVEL 3'S FROZEN TEXT, by `queue_alone.rules`, never from
the oracle (rule B). `RR-g1` holds its first match over the space to the policy,
through `rung3.order_search_ls.space_truth_masks`, a module already allowed to
see the oracle. The space is `manual.instrument`'s, built once.
"""

from __future__ import annotations

import re
import statistics
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from typing import Any

from harness.domain import Case
from harness.dsl import Condition, RuleValidationError
from rung2.engine2 import Space, validate_conditions

from apply import score as ascore
from manual import instrument as MI
from queue_alone import rules as qrules

F = Fraction
CITED = re.compile(r"(?<![A-Za-z0-9])(H\d{2})(?!\d)")


def space() -> Space:
    """The 134,400 points, `manual.instrument`'s, built once."""
    return MI.space()


@lru_cache(maxsize=None)
def masks(rs: tuple[qrules.Rule, ...]) -> tuple[dict[str, int], dict[str, int]]:
    """Each listed rule's region over the space, by identifier, and the list's
    first match as one region per queue."""
    sp = space()
    regions = {r.id: sp.extension([Condition(attr=a, op=o, value=v)
                                   for a, o, v in r.conditions]) for r in rs}
    by_queue: dict[str, int] = {}
    left = sp.full
    for r in rs:
        took = regions[r.id] & left
        by_queue[r.queue] = by_queue.get(r.queue, 0) | took
        left &= ~regions[r.id]
    return regions, by_queue


def first_match_masks(rs: tuple[qrules.Rule, ...] | None = None) -> dict[str, int]:
    """`{queue: the points the list's first match sends there}`."""
    return masks(qrules.rules() if rs is None else tuple(rs))[1]


def edges(payload: dict[str, Any]) -> list[str]:
    """What an answer declares in `beats` and `loses_to`, as strings."""
    out: list[str] = []
    for key in ("beats", "loses_to"):
        v = payload.get(key)
        items = v if isinstance(v, list) else ([v] if isinstance(v, str) and v else [])
        out.extend(str(x) for x in items)
    return out


def cites(items: list[str], ids: set[str]) -> bool:
    return any(m in ids for x in items for m in CITED.findall(x))


def read(payload: Any, case: Case, rs: tuple[qrules.Rule, ...] | None = None
         ) -> dict[str, Any]:
    """One answer's rule, read as the module's docstring says."""
    rs = qrules.rules() if rs is None else tuple(rs)
    if not isinstance(payload, dict):
        return {"validates": False, "why": "no payload"}
    try:
        rule = validate_conditions(payload, None)
    except RuleValidationError as exc:
        return {"validates": False, "why": str(exc).split(":")[0]}
    regions, by_queue = masks(rs)
    region = space().extension(rule.conditions)
    points = region.bit_count()
    right = (region & by_queue.get(rule.action, 0)).bit_count()
    hit = qrules.matching(case.as_dict(), rs)
    governing = hit[0].id if hit else None
    same = sorted(rid for rid, m in regions.items() if m == region)
    declared = edges(payload)
    return {"validates": True, "why": None, "matches_ticket": rule.matches(case),
            "conditions": len(rule.conditions), "points": points, "right": right,
            "all_right": points > 0 and right == points, "same_region_as": same,
            "governing": governing, "is_governing": governing in same,
            "declares": bool(declared), "cites": cites(declared, {r.id for r in rs})}


def summary(readings: list[dict[str, Any]]) -> dict[str, Any]:
    """An arm's readings, counted. The share of a region a rule gets right is
    always set beside its points (§5.10)."""
    ok = [r for r in readings if r["validates"]]
    points = [r["points"] for r in ok]
    shares = [F(r["right"], r["points"]) for r in ok if r["points"]]
    total = sum(points)
    listed = Counter(r["same_region_as"][0] for r in ok if r["same_region_as"])
    return {
        "answers": len(readings), "validates": len(ok),
        "why_not": dict(sorted(Counter(r["why"] for r in readings
                                       if not r["validates"]).items())),
        "matches_ticket": sum(1 for r in ok if r["matches_ticket"]),
        "conditions": {str(k): v for k, v in
                       sorted(Counter(r["conditions"] for r in ok).items())},
        "points": {"min": min(points) if points else None,
                   "median": statistics.median(points) if points else None,
                   "max": max(points) if points else None},
        "right_share_pooled": ascore.frac(F(sum(r["right"] for r in ok), total)
                                          if total else None),
        "right_share_median": ascore.frac(F(statistics.median(shares))
                                          if shares else None),
        "all_right": sum(1 for r in ok if r["all_right"]),
        "same_region_as_a_listed_rule": sum(1 for r in ok if r["same_region_as"]),
        "as_the_governing_rule": sum(1 for r in ok if r["is_governing"]),
        "listed_rules_written": dict(listed.most_common()),
        "declares": sum(1 for r in ok if r["declares"]),
        "cites_identifiers": sum(1 for r in ok if r["cites"]),
    }
