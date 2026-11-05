"""
Rung 2's loop under v1b, with a channel's trigger — §5 of `PLAN_CHANNEL.md`. **On
the proposer's path**: the labels and the draws are handed in, and nothing here
imports the policy (rule B of the plan).

WHAT IS `PLAN_REASONED_LOOP.md`'S, CALLED AND NOT EDITED (rule A). One escalation
is `reasoned_loop.loop.propose_v1b`: the draft, blind at every escalation, then
the placement round when the draft overlaps rules of other queues. A run's record
is `reasoned_loop.loop.record_of`, and its result `reasoned_loop.loop.Result`,
which `Result` below extends with the channel's counts.

WHAT IS THIS PLAN'S (§5.2).

  `escalates`  THE TRIGGER, and the only code of the loop that reads a label to
               decide anything the loop does (§5.2). An IMPASSE or a CONFLICT
               escalates in both arms. A case the engine decides with a queue
               other than its label escalates as an `ERROR` when the channel
               reports it, which `plan.reportable` says from the case's draw and
               the coverage: at coverage 1, always, which is
               `PLAN_REASONED_LOOP.md`'s error arm; at 0, never, which is its
               impasse arm (`CH-g1`). The loop's other reads of the label score
               what was decided, into the record, as rung 2's loop always has:
               `correct`, `proposal_action_correct` and a rule's `correct_count`,
               which the engine keeps for the record and never shows the
               proposer. `tests/test_channel.py` pins that by behaviour, not by
               this paragraph: labels that leave the causes unchanged leave the
               proposer's calls and the base unchanged.
  `run_loop`   the loop, case by case and in order (hard rule 3), at a coverage
               and over a run's draws. It is `reasoned_loop.loop.run_loop` with
               this trigger in place of that one: that function refuses any arm
               but its own two, and it is called, never edited. It keeps what
               that loop keeps, and on every case's row the case's draw and
               whether its wrong decision was reported.

WHAT THE PROPOSER IS HANDED is what `PLAN_REASONED_LOOP.md`'s was: the ticket, and
for the placement round the draft and the rules it overlaps. Neither the label,
nor the draw, nor that a decision was wrong reaches it (rule I). The record keeps
the label beside each case, as rung 2's loop always has, for scoring.

A WRONG DECISION THE CHANNEL DOES NOT REPORT STANDS, as any decision does under
the impasse trigger, and its rule is counted as fired. A reported one escalates at
once (§2.2), and its rule is not counted as fired: its decision did not stand.
"""

from __future__ import annotations

import collections
import time
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Sequence

from harness.domain import Case

from authorship import loop as eloop
from authorship import protocol as e
from reasoned_loop import loop as rl_loop
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import plan

propose_v1b = rl_loop.propose_v1b
record_of = rl_loop.record_of


def escalates(coverage: Fraction, outcome: str, winner, truth: str,
              draw: float | None) -> tuple[str | None, bool | None]:
    """The trigger (§5.2): a case's cause of escalation, or None, and whether
    its wrong decision was reported, or None where the engine decided nothing
    or decided right."""
    if outcome in (plan.IMPASSE, plan.CONFLICT):
        return outcome, None
    if winner.action == truth:
        return None, None
    told = plan.reportable(coverage, draw)
    return (plan.ERROR if told else None), told


@dataclass
class Result(rl_loop.Result):
    coverage: Fraction = Fraction(1)

    def summary(self) -> dict[str, Any]:
        """`reasoned_loop.loop.Result`'s, and the channel's counts: the wrong
        decisions the trigger saw, the ones reported, which escalated, and the
        ones not reported, which stood."""
        out = super().summary()
        wrong = [c for c in self.causes if c["reported"] is not None]
        told = sum(1 for c in wrong if c["reported"])
        out["channel"] = {"coverage": str(self.coverage), "wrong_decisions": len(wrong),
                          "reported": told, "unreported": len(wrong) - told}
        return out


def run_loop(corpus: Sequence[Case], labels: Sequence[tuple[str, str]],
             engine: PriorityEngine, proposer, coverage: Fraction,
             draws: Sequence[float] | None = None, *, cap: int = plan.MAX_ESCALATIONS,
             on_progress=None, clock=time.monotonic) -> Result:
    """The loop over `corpus`, case by case and in order: hard rule 3."""
    plan.reportable(coverage, 0.0)               # a coverage from 0 to 1, or refused
    if draws is None and 0 < coverage < 1:
        raise ValueError(f"a channel at coverage {coverage} needs a run's draws")
    if draws is not None and len(draws) < len(corpus):
        raise ValueError(f"{len(draws)} draws for {len(corpus)} cases")
    records: list[Record2] = []
    causes: list[dict[str, Any]] = []
    escalations: list[eloop.Escalation] = []
    channels: list[str] = []
    rejected = failed = calls = 0
    edge_reasons = collections.Counter()
    union, cover, stopped_at = 0, None, None

    for idx, case in enumerate(corpus):
        truth, trule = labels[idx]
        draw = None if draws is None else draws[idx]
        outcome, winner, involved = engine.decide(case)
        cause, told = escalates(coverage, outcome, winner, truth, draw)
        predicted = correct = prop_ok = reason = None
        n_prop = n_acc = 0
        reasons: list[str] = []

        if cause is None:
            predicted = winner.action
            correct = predicted == truth
            winner.fire_count += 1
            if correct:
                winner.correct_count += 1
        else:
            res = propose_v1b(engine, case, idx, cause, proposer, channels, clock=clock)
            escalations.append(res["esc"])
            calls += len(res["esc"].calls)
            failed += res["failed"]
            rejected += res["rejected"]
            reason = res["reason"]
            if not res["failed"]:
                predicted = res["action"]
                prop_ok = predicted == truth
                correct = prop_ok
            n_prop, n_acc, reasons = res["n_prop"], res["n_acc"], res["reasons"]
            edge_reasons.update(reasons)
            if res["esc"].verdict == e.BORN:
                union |= engine.ext[res["esc"].rule_id]
                if cover is None and union == engine.space.full:
                    cover = idx

        records.append(Record2(
            idx=idx, outcome=outcome, predicted=predicted, truth=truth,
            truth_rule=trule, correct=correct,
            winner_id=winner.rule_id if winner else None,
            n_matched=len(involved), escalated=cause is not None,
            shown_ids=[], shown_kind=p.BLIND if cause else None,
            proposal_action_correct=prop_ok,
            edges_proposed=n_prop, edges_accepted=n_acc,
            edge_reasons=reasons, rejected_reason=reason,
        ))
        causes.append({"cause": cause,
                       "engine_action": winner.action if cause == plan.ERROR else None,
                       "engine_rule": winner.rule_id if cause == plan.ERROR else None,
                       "draw": draw, "reported": told})
        if on_progress is not None:
            on_progress(idx, len(corpus), len(engine.rules), len(escalations))
        if len(escalations) >= cap:
            stopped_at = idx
            break

    res2 = RunResult2(proposer_name=getattr(proposer, "name", "?"),
                      n_cases=len(records), records=records, rules=engine.rules,
                      rejected=rejected, failed=failed, edge_stats=dict(edge_reasons))
    res2.metrics = compute_metrics2(res2, engine)
    return Result(eloop.LoopResult(res2, escalations, channels, calls),
                  causes, cover, stopped_at, coverage)
