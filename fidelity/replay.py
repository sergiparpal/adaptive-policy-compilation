"""
A Stage B record of `PLAN_REUSE.md`, rebuilt case by case from the record alone.
This is `F-g2` of `PLAN_FIDELITY.md` §6, and it supplies the moments every
prompt of the plan is built at.

WHAT IS REBUILT, AND FROM WHAT. The record holds every rule with its birth and
the edges it declared there, the whole `edge_log` in the order `try_edge` met it,
and one row per case. Rebuilding it means deciding each case with a fresh rung 2
engine. On a decided case, the decision counts toward the winner, as the loop
counts it. On an escalation, the rule born there is added under its own id and
its edges are tried in the logged order. Nothing is asked of a model, and the
one label used, `correct` for the counts, comes off the record. No oracle.

WHY IT IS A CHECK AND NOT A CONVENIENCE. Every prompt the plan pays for is built
on a rebuilt base. A rebuild that drifted would put the wrong screen in front of
the model, and nothing downstream could tell. So `check` compares the rebuild
with everything the record says happened:

  * every outcome, winner and number of matched rules;
  * every escalation's neighbourhood, ids and kind, which exercises v1's
    tie-break on fire counts (§5.7 of the plan);
  * every edge verdict, in `edge_log` order;
  * every rule's final fire and correct counts;
  * the system prompt, which must be v1's, byte for byte.

**And it has teeth**: rebuilt without the edges, each Stage B run diverges, and
`tests/test_fidelity.py` pins that it does.

`Replay.moments` yields each case's moment BEFORE the case changes the base. A
decided case has not yet been counted toward its rule, and an escalation's rule
is not yet born. That is the moment a prompt about that case is built at.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from harness.domain import Case
from harness.dsl import Condition

from rung2.engine2 import PriorityEngine, Rule2, Space
from rung2.proposers2 import SYSTEM_PROMPT_V1, neighbourhood

# An edge citing a rule the proposer was not shown: dropped before `try_edge`,
# so it is in the row's `edge_reasons` and not in the `edge_log`.
OUTSIDE = "fuera_del_vecindario"


def rule_from(d: dict) -> Rule2:
    """A rule as the record stores it, `Rule2.as_dict()`, back into a rule. Its
    edges are the ones accepted at its birth: the loop never adds one later."""
    return Rule2(rule_id=d["rule_id"],
                 conditions=[Condition(**c) for c in d["conditions"]],
                 action=d["action"], note=d.get("note", ""),
                 beats=list(d.get("beats") or []),
                 loses_to=list(d.get("loses_to") or []),
                 dropped_edges=list(d.get("dropped_edges") or []))


@dataclass
class Moment:
    """One case, at the moment it arrives: the base as it stood, and what the
    engine decided over it. `row` is the record's row for the case."""
    idx: int
    case: Case
    row: dict
    engine: PriorityEngine
    outcome: str
    winner: Rule2 | None
    involved: list[Rule2]

    @property
    def undefeated(self) -> list[Rule2]:
        """What the loop shows on a CONFLICT; on an impasse, nothing."""
        return self.involved if self.outcome == "CONFLICT" else []


@dataclass
class Replay:
    record: dict
    corpus: list[Case]
    space: Space
    with_edges: bool = True
    edge_problems: list[str] = field(default_factory=list)
    engine: PriorityEngine | None = None

    def moments(self) -> Iterator[Moment]:
        born = {r["born_at"]: r for r in self.record["rules"]}
        log = list(self.record.get("edge_log") or [])
        engine = self.engine = PriorityEngine(space=self.space)
        for idx, case in enumerate(self.corpus):
            row = self.record["records"][idx]
            outcome, winner, involved = engine.decide(case)
            yield Moment(idx, case, row, engine, outcome, winner, involved)
            if outcome == "ACTION":
                winner.fire_count += 1
                if row.get("correct"):
                    winner.correct_count += 1
                continue
            d = born.get(idx)
            if d is None:
                continue
            engine.add(rule_from(d), born_at=idx, keep_id=True)
            for why in row.get("edge_reasons") or []:
                if why == OUTSIDE:
                    continue
                if not log:
                    self.edge_problems.append(f"case {idx}: the edge_log ran out")
                    break
                winner_id, loser_id, logged = log.pop(0)
                if logged != why:
                    self.edge_problems.append(
                        f"case {idx}: the row says {why}, the log says {logged}")
                if self.with_edges:
                    got = engine.try_edge(winner_id, loser_id)
                    if got != logged:
                        self.edge_problems.append(
                            f"case {idx}: {winner_id} over {loser_id} rebuilt "
                            f"{got}, logged {logged}")
        if log:
            self.edge_problems.append(f"{len(log)} edge_log entries never replayed")


def check(record: dict, corpus: list[Case], space: Space, *,
          with_edges: bool = True) -> dict[str, Any]:
    """`F-g2` for one record: every way the rebuild departs from it."""
    rp = Replay(record, corpus, space, with_edges=with_edges)
    decisions: list[str] = []
    screens: list[str] = []
    for m in rp.moments():
        got = (m.outcome, m.winner.rule_id if m.winner else None, len(m.involved))
        want = (m.row["outcome"], m.row["winner_id"], m.row["n_matched"])
        if got != want:
            decisions.append(f"case {m.idx}: rebuilt {got}, recorded {want}")
        elif m.outcome != "ACTION":
            shown, kind = neighbourhood(m.engine, m.case, m.undefeated)
            if ([r.rule_id for r in shown], kind) != (m.row["shown_ids"],
                                                     m.row["shown_kind"]):
                screens.append(f"case {m.idx}: its screen rebuilt differently")
    by_id = {r.rule_id: r for r in rp.engine.rules}
    counts: list[str] = []
    for d in record["rules"]:
        r = by_id.get(d["rule_id"])
        if r is None:
            counts.append(f"{d['rule_id']}: never rebuilt")
        elif (r.fire_count, r.correct_count) != (d["fire_count"], d["correct_count"]):
            counts.append(f"{d['rule_id']}: rebuilt {r.fire_count}/{r.correct_count}, "
                          f"recorded {d['fire_count']}/{d['correct_count']}")
    prompt_is_v1 = record.get("system_prompt") == SYSTEM_PROMPT_V1
    problems = (decisions + screens + rp.edge_problems + counts
                + ([] if prompt_is_v1 else ["the system prompt is not v1's"]))
    return {
        "decisions_departing": len(decisions),
        "screens_departing": len(screens),
        "edge_problems": len(rp.edge_problems),
        "rules_whose_counts_depart": len(counts),
        "system_prompt_is_v1": prompt_is_v1,
        "first_problems": problems[:10],
        "passes": not problems,
    }
