"""
The two designs `PLAN_RANKED.md` set aside before its signature (§2.2), kept so
that the figures that set them aside are recomputed and not recalled. **No run
uses them**, and they are not on the proposer's path.

Both order the whole base by the ranking, and read no declared edge:

  A   the first draft's engine. Every citation is a vote; the base is put in
      the ranking's order under `corrections/hierarchy.py`'s pulled
      construction, every rule strictly inside another before it; a case is
      decided by the first rule of that order that matches it. It is
      `corrections/online.py`'s replay, made an engine.
  B   A, with each pair of regions voting once a side, however often an answer
      declares it.

WHAT SET THEM ASIDE (§0 of the plan, figure 2). Under the transcriber, a
proposer that writes the governing rule and places it by the policy's order,
design A's ranking ends with `ACCOUNT_MANAGER` last under every draw, and the
base decides about nine tenths of the space, where rung 2's engine decides
nearly all of it. A rule written again after a reported error casts all its
votes again, and a queue in the middle of the policy loses to more rules than
it beats. Design B mends two draws of three. `RK-g3` recomputes both.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from harness.domain import Case

from corrections import declared as DC
from corrections import hierarchy as H
from fidelity.replay import rule_from
from rung2.engine2 import PriorityEngine, Space

from .engine import Tally, births, cited

EVERY, DISTINCT = "every citation", "each pair of regions once a side"


@dataclass
class Total(PriorityEngine):
    """Designs A and B: the whole base in the ranking's order, pulled, decided
    by first match. It never returns CONFLICT, and reads no declared edge."""

    count: str = EVERY
    tally: Tally = field(default_factory=Tally)
    _counted: int = 0
    _seen: set = field(default_factory=set)
    _position: dict[str, int] = field(default_factory=dict)

    def refresh(self) -> None:
        if self._counted == len(self.rules):
            return
        for r in self.rules[self._counted:]:
            if self.count == EVERY:
                self.tally.born(r)
            else:
                self.tally.queue_of[r.rule_id] = r.action
                self.tally.count(r, self._distinct(r))
        self._counted = len(self.rules)
        order = H.pulled(H.rules_of(self), H.rank_of(self.tally.ranking))
        self._position = {rid: i for i, rid in enumerate(order)}

    def _distinct(self, r) -> Counter:
        """A citation's vote, unless its two regions already voted that way."""
        held = {x.rule_id: x for x in self.rules if x.rule_id in self.tally.queue_of}
        v: Counter = Counter()
        for ref, side, _ in DC.citations(cited(r)):
            o = held.get(ref)
            if o is None or o.action == r.action:
                continue
            w, l = (r, o) if side == "beats" else (o, r)
            key = (self.ext[w.rule_id], w.action, self.ext[l.rule_id], l.action)
            if key not in self._seen:
                self._seen.add(key)
                v[(w.action, l.action)] += 1
        return v

    @property
    def order(self) -> list[str]:
        self.refresh()
        return sorted(self._position, key=self._position.get)

    def decide(self, case: Case):
        self.refresh()
        matched = [r for r in self.rules if r.matches(case)]
        if not matched:
            return "IMPASSE", None, []
        return "ACTION", min(matched, key=lambda r: self._position[r.rule_id]), matched


def right_of(total: Total, truth: dict[str, int]) -> int:
    """The points first match over the base's order decides right."""
    action = {r.rule_id: r.action for r in total.rules}
    taken = right = 0
    for rid in total.order:
        mine = total.ext[rid] & ~taken
        right |= mine & truth.get(action[rid], 0)
        taken |= mine
    return right.bit_count()


def fed(record: dict, space: Space, count: str) -> Total:
    """A finished record's births, fed in order with the citations their
    answers made: the replay of a run under one of the two designs. No declared
    edge is installed, since neither design reads one."""
    total = Total(space=space, count=count)
    for d in births(record):
        rule = rule_from(d)
        for k, v in cited(d).items():
            setattr(rule, k, list(v))
        total.add(rule, born_at=d["born_at"], keep_id=True)
        total.refresh()
    return total
