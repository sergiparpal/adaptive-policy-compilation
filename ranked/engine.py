"""
The engine of arm K — §5.2 of `PLAN_RANKED.md`. **On the proposer's path**: it
reads the rules of the base and the citations of their answers, and nothing of
the truth. Nothing here imports the policy.

WHAT IT IS. Rung 2's engine with one method changed: `decide`, and that only
where rung 2's would return CONFLICT. Everything else is inherited and
untouched: `add`, `try_edge`, containment, the installed edges and the edge log.
So `placement.protocol.propose_v1c` lists and shows in arm K what it would in
arm L on the same base, and every case rung 2's engine decides, this one decides
the same.

WHERE RUNG 2'S ENGINE WOULD RETURN CONFLICT, the undefeated rules carry two
queues or more, and it asks. This engine decides: **the rule whose queue its
ranking puts first wins.** It never returns CONFLICT.

THE RANKING (§2.3, §2.4), taken again after every birth:

  the votes     every citation, in the answer of every rule born so far, of a
                rule of another queue the base held when the answer was given: a
                rule and a side, read as `corrections/declared.py`'s `citations`
                reads them, whatever the engine did with the edge. A `beats` is
                a vote for the newborn's queue over the cited rule's, a
                `loses_to` the other way;
  the ranking   of the 40,320 rankings of the eight queues, those that agree
                with the most votes, and of those the earliest in
                `itertools.permutations(ACTIONS)`. Before any vote that is the
                domain's own order.

The count is `corrections/online.py`'s, and `RK-g1` holds it to that replay's
ranking on every birth of `PLAN_CORRECTIONS.md`'s three L runs.

A VOTE COUNTS A RULE THE BASE HOLDS WHEN THE ANSWER IS GIVEN. An engine cannot
count a citation of a rule not yet born, and never goes back to one. A reading
of a finished record feeds its births in order through `Tally`, this same code,
so it counts what the engine counted.

WHAT IT LOGS, when `keep_log` is set, as a run does:
- after every birth, the ranking it took, its agreement, how many rankings tie
  at it, and the votes so far;
- at every case, who decided: nobody at an impasse, rung 2's engine, or the
  ranking. Where the ranking decided, the queues of the undefeated rules, the
  queue of the best placed other, and the votes between the two.
The log reads no truth.
"""

from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from harness.domain import ACTIONS, Case

from corrections import declared as DC
from rung2.engine2 import PriorityEngine, Rule2

from . import plan

SIDES = ("beats", "loses_to", "dropped_edges")
RUNG2, RANKING = "rung2", "ranking"        # who decided a case


# ---------------------------------------------------------------------------
# The rankings, and which of them put one queue above another
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def rankings() -> tuple[tuple[str, ...], ...]:
    """Every ranking of the eight queues, in `itertools.permutations(ACTIONS)`'s
    order, which breaks every tie."""
    return tuple(itertools.permutations(ACTIONS))


@lru_cache(maxsize=1)
def ahead() -> dict[tuple[str, str], tuple[int, ...]]:
    """For each ordered pair of queues, the rankings that put the first above
    the second, by index."""
    out: dict[tuple[str, str], list[int]] = {(a, b): [] for a in ACTIONS for b in ACTIONS
                                             if a != b}
    for k, perm in enumerate(rankings()):
        for i, a in enumerate(perm):
            for b in perm[i + 1:]:
                out[(a, b)].append(k)
    return {pair: tuple(ks) for pair, ks in out.items()}


# ---------------------------------------------------------------------------
# The votes and the ranking
# ---------------------------------------------------------------------------

def get(rule: Any, key: str) -> Any:
    """A field of a rule, from the engine's rule or from a record's."""
    return rule[key] if isinstance(rule, dict) else getattr(rule, key)


def cited(rule: Any) -> dict[str, list]:
    """A rule's citations, as `corrections.declared.citations` takes them."""
    return {k: (rule.get(k) if isinstance(rule, dict) else getattr(rule, k)) or []
            for k in SIDES}


def votes_of_rule(rule: Any, queue_of: dict[str, str]) -> Counter:
    """One born rule's votes: a citation of a rule of another queue that
    `queue_of` holds, a rule and a side."""
    action = get(rule, "action")
    v: Counter = Counter()
    for ref, side, _ in DC.citations(cited(rule)):
        q = queue_of.get(ref)
        if q is None or q == action:
            continue
        v[(action, q) if side == "beats" else (q, action)] += 1
    return v


class Tally:
    """The votes as births come, and the ranking they choose after each."""

    def __init__(self) -> None:
        self.scores = [0] * plan.N_RANKINGS
        self.votes: Counter = Counter()
        self.state = (0, 0, plan.N_RANKINGS)   # the ranking, its agreement, the rankings tied
        self.log: list[dict[str, Any]] = []
        self.queue_of: dict[str, str] = {}

    def born(self, rule: Any) -> None:
        """Take one birth: the newborn joins the base, then its votes count."""
        self.queue_of[get(rule, "rule_id")] = get(rule, "action")
        self.count(rule, votes_of_rule(rule, self.queue_of))

    def count(self, rule: Any, v: Counter) -> None:
        table = ahead()
        for pair, m in v.items():
            for k in table[pair]:
                self.scores[k] += m
        self.votes.update(v)
        top = max(self.scores)
        self.state = (self.scores.index(top), top, self.scores.count(top))
        self.log.append({"rule_id": get(rule, "rule_id"), "born_at": get(rule, "born_at"),
                         "ranking": self.state[0], "agreeing": top, "tied": self.state[2],
                         "votes": sum(self.votes.values())})

    @property
    def ranking(self) -> tuple[str, ...]:
        return rankings()[self.state[0]]

    def final(self) -> dict[str, Any]:
        """What a record keeps of the ranking a run ends with."""
        k, top, tied = self.state
        return {"ranking": list(rankings()[k]), "index": k, "agreeing": top, "tied": tied,
                "votes": DC.by_pair(self.votes), "n_votes": sum(self.votes.values())}


def births(record: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(record["rules"], key=lambda r: (r["born_at"], r["rule_id"]))


def tally_of(record: dict[str, Any]) -> Tally:
    """A finished record's votes, its births fed in order."""
    t = Tally()
    for d in births(record):
        t.born(d)
    return t


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------

@dataclass
class RankedEngine(PriorityEngine):
    """Rung 2's engine, deciding by the ranking its own votes choose where rung
    2's would return CONFLICT."""

    keep_log: bool = False
    case_log: list[dict[str, Any]] = field(default_factory=list)
    tally: Tally = field(default_factory=Tally)
    _counted: int = 0

    # -- the ranking -----------------------------------------------------------

    def refresh(self) -> None:
        """Take the votes of every rule born since the last time. A birth's
        citations are complete by the time the next case is decided."""
        for r in self.rules[self._counted:]:
            self.tally.born(r)
        self._counted = len(self.rules)

    @property
    def ranking(self) -> tuple[str, ...]:
        self.refresh()
        return self.tally.ranking

    @property
    def ranking_log(self) -> list[dict[str, Any]]:
        self.refresh()
        return self.tally.log

    def final(self) -> dict[str, Any]:
        self.refresh()
        return self.tally.final()

    # -- the decision ----------------------------------------------------------

    def decide(self, case: Case):
        outcome, winner, involved = PriorityEngine.decide(self, case)
        if outcome != "CONFLICT":
            if self.keep_log:
                self.case_log.append({"by": RUNG2 if outcome == "ACTION" else None})
            return outcome, winner, involved
        self.refresh()
        winner = pick(involved, self.tally.ranking)
        if self.keep_log:
            self.case_log.append(self._ranked_row(involved, winner))
        return "ACTION", winner, [r for r in self.rules if r.matches(case)]

    def _ranked_row(self, undefeated: list[Rule2], winner: Rule2) -> dict[str, Any]:
        rank = {q: i for i, q in enumerate(self.tally.ranking)}
        queues = sorted({r.action for r in undefeated}, key=rank.get)
        other = queues[1] if queues[0] == winner.action else queues[0]
        return {"by": RANKING, "ranking": self.tally.state[0], "queues": queues,
                "runner_up": other,
                "votes_for": self.tally.votes[(winner.action, other)],
                "votes_against": self.tally.votes[(other, winner.action)]}


def pick(undefeated: list[Rule2], ranking: tuple[str, ...]) -> Rule2:
    """Of the undefeated rules, the one whose queue `ranking` puts first; of
    several of that queue, the earliest born, which changes no decision."""
    rank = {q: i for i, q in enumerate(ranking)}
    return min(undefeated, key=lambda r: (rank[r.action], r.born_at, r.rule_id))
