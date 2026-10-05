"""
The definitions §0 of `PLAN_PRIMACY.md` names, and the statistics its rows read.
Pure functions over answer rows: nothing here opens a file.

A ROW is one answer of `results2/pair_judgement_1600.json`: two rules of the
learned base, `rule_a` born before `rule_b`, listed to the proposer as `A` and
then `B`, and the queue it answered. The two rules of a row always send its
ticket to different queues, which `L-g3` checks.

  first_rule     the rule listed first, `shown_as["A"]`. It is also the rule
                 labelled `A`, and its queue is the first queue the question
                 names (§5.1 of the plan): the three never come apart.
  queue_pair     the row's two queues, sorted.
  winner         the rule the answer named, or None when it named neither: a
                 parse failure, or a queue that is neither rule's.
  slot_effect    for a reference rule chosen without looking at the slot, the
                 share of answers naming it when it is listed first, minus the
                 share naming it when it is listed second. The slot was dealt
                 at random (`L-g2`), so the difference is the share of answers
                 the slot pulled towards the first rule minus the share it
                 pulled towards the second: a LOWER BOUND on the share it
                 decided, not that share (§5.4). On one queue pair it does not
                 depend on which of the two queues is the reference.
  majority       a queue pair's favoured queue, the one named more often among
                 its declared answers; None on a tie.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Callable, Iterable

NONE = "none"


# ---------------------------------------------------------------------------
# What a row is
# ---------------------------------------------------------------------------

def first_rule(r: dict) -> str:
    return r["shown_as"]["A"]


def second_rule(r: dict) -> str:
    return r["shown_as"]["B"]


def action(r: dict, rule: str) -> str:
    return r["action_a"] if rule == r["rule_a"] else r["action_b"]


def queue_pair(r: dict) -> tuple[str, str]:
    return tuple(sorted((r["action_a"], r["action_b"])))


def pair_key(qp: tuple[str, str]) -> str:
    """The record's own spelling of a queue pair, `X vs Y` with X < Y."""
    return f"{qp[0]} vs {qp[1]}"


def winner(r: dict) -> str | None:
    if r["declared"] == "a_beats_b":
        return r["rule_a"]
    if r["declared"] == "b_beats_a":
        return r["rule_b"]
    return None


def declared(rows: Iterable[dict]) -> list[dict]:
    return [r for r in rows if winner(r) is not None]


def rule_with_action(r: dict, queue: str) -> str | None:
    if r["action_a"] == queue:
        return r["rule_a"]
    if r["action_b"] == queue:
        return r["rule_b"]
    return None


# ---------------------------------------------------------------------------
# Counts the record publishes, and the favoured queue
# ---------------------------------------------------------------------------

def per_queue_pair(rows: Iterable[dict]) -> dict[str, dict[str, int]]:
    """How often each queue was named winner, by queue pair: the record's
    `revealed_hierarchy.per_queue_pair`, recomputed."""
    out: dict[str, Counter] = defaultdict(Counter)
    for r in declared(rows):
        out[pair_key(queue_pair(r))][action(r, winner(r))] += 1
    return {k: dict(v) for k, v in out.items()}


def majority(rows: Iterable[dict]) -> dict[tuple[str, str], str | None]:
    """Each queue pair's favoured queue among its declared answers."""
    counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for r in declared(rows):
        counts[queue_pair(r)][action(r, winner(r))] += 1
    out = {}
    for qp, c in counts.items():
        (q1, n1), *rest = c.most_common()
        out[qp] = None if rest and rest[0][1] == n1 else q1
    return out


def favoured_rule(r: dict, maj: dict) -> str | None:
    q = maj.get(queue_pair(r))
    return None if q is None else rule_with_action(r, q)


# ---------------------------------------------------------------------------
# The statistics
# ---------------------------------------------------------------------------

def _share(hits: int, n: int) -> float | None:
    return hits / n if n else None


def two_sample(h1: int, n1: int, h2: int, n2: int) -> dict:
    """A difference of two shares, the first minus the second, with the
    unpooled standard error. Unrounded: a verdict is read on these values, and
    the record rounds only when it is written."""
    p1, p2 = _share(h1, n1), _share(h2, n2)
    if p1 is None or p2 is None:
        return {"n1": n1, "hits1": h1, "p1": p1, "n2": n2, "hits2": h2, "p2": p2,
                "difference": None, "standard_error": None}
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {"n1": n1, "hits1": h1, "p1": p1, "n2": n2, "hits2": h2, "p2": p2,
            "difference": p1 - p2, "standard_error": se}


def slot_effect(rows: Iterable[dict], ref: Callable[[dict], str | None]) -> dict:
    """Over the declared rows with a reference rule: the share naming the
    reference when it is listed first, minus the share when listed second."""
    n1 = h1 = n2 = h2 = 0
    for r in declared(rows):
        x = ref(r)
        if x is None:
            continue
        hit = winner(r) == x
        if first_rule(r) == x:
            n1, h1 = n1 + 1, h1 + hit
        else:
            n2, h2 = n2 + 1, h2 + hit
    out = two_sample(h1, n1, h2, n2)
    out["what"] = ("share naming the reference rule when it is listed first, "
                   "minus the share when it is listed second; a lower bound on "
                   "the share of answers the slot decided")
    return out


def first_listed_rate(rows: Iterable[dict]) -> dict:
    """The share of declared answers naming the rule listed first, against a
    coin: §15's `names_first_shown`, on any subset."""
    d = declared(rows)
    n = len(d)
    hits = sum(1 for r in d if winner(r) == first_rule(r))
    rate = _share(hits, n)
    se = math.sqrt(0.25 / n) if n else None
    return {"n": n, "hits": hits, "rate": rate,
            "twice_minus_one": 2 * rate - 1 if rate is not None else None,
            "standard_error": se,
            "deviations_from_a_coin": (rate - 0.5) / se if se else None}


def none_by_favoured_slot(rows: Iterable[dict], maj: dict) -> dict:
    """`L-b`: the share of rows with no edge when the favoured rule is listed
    second, minus the share when it is listed first. A row whose queue pair has
    no favoured queue is counted apart."""
    n = {"first": 0, "second": 0}
    none = {"first": 0, "second": 0}
    parse = {"first": 0, "second": 0}
    apart = 0
    for r in rows:
        f = favoured_rule(r, maj)
        if f is None:
            apart += 1
            continue
        slot = "first" if first_rule(r) == f else "second"
        n[slot] += 1
        if r["declared"] == NONE:
            none[slot] += 1
            parse[slot] += bool(r.get("parse_failed"))
    out = two_sample(none["second"], n["second"], none["first"], n["first"])
    out.update({"what": ("share of rows with no edge when the favoured rule is "
                         "listed second, minus the share when it is listed first"),
                "counted_apart": apart,
                "parse_failures": {"favoured_second": parse["second"],
                                   "favoured_first": parse["first"]},
                "no_edge_without_a_parse_failure": {
                    "favoured_second": none["second"] - parse["second"],
                    "favoured_first": none["first"] - parse["first"]}})
    return out
