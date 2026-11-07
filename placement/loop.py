"""
Rung 2's loop under `PLAN_CHANNEL.md`'s channel, with the escalation as an
argument — §5 of `PLAN_PLACEMENT.md`. **On the proposer's path**: the labels and
the draws are handed in, and nothing here imports the policy (rule B of the plan).

WHAT IS `PLAN_CHANNEL.md`'S, CALLED AND NOT EDITED (rule A). The trigger is
`channel.loop.escalates`: an IMPASSE or a CONFLICT escalates; a case the engine
decides with a queue other than its label escalates as an `ERROR` when its draw
falls below the coverage. A run's result is `channel.loop.Result`, and its record
`reasoned_loop.loop.record_of`.

WHAT IS THIS PLAN'S. `run_loop` is `channel.loop.run_loop` with the escalation
handed in, because that function names its own, `propose_v1b`. It is a copy, and
`PL-g1` holds it to the original: under v1b, served `PLAN_CHANNEL.md`'s run
`c r1`'s answers, both give the same record case for case. `ESCALATIONS` names
each arm's escalation: v1b's is `reasoned_loop.loop.propose_v1b`, called; v1c's
is `placement.protocol.propose_v1c`.

WHAT THE PROPOSER IS HANDED is what `PLAN_CHANNEL.md`'s was: the ticket, and for
the placement round the draft and the rules listed. Neither the label, nor the
draw, nor that a decision was wrong reaches it (rule I). The record keeps the
label beside each case, as rung 2's loop always has, for scoring.
"""

from __future__ import annotations

import collections
import time
from fractions import Fraction
from typing import Any, Callable, Sequence

from harness.domain import Case

from authorship import loop as eloop
from authorship import protocol as e
from channel import loop as ch_loop
from reasoned_loop import loop as rl_loop
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import plan, protocol

escalates = ch_loop.escalates
record_of = rl_loop.record_of
Result = ch_loop.Result

ESCALATIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "v1b": rl_loop.propose_v1b,
    "v1c": protocol.propose_v1c,
}


def run_loop(corpus: Sequence[Case], labels: Sequence[tuple[str, str]],
             engine: PriorityEngine, proposer, coverage: Fraction,
             draws: Sequence[float] | None = None, *,
             propose: Callable[..., dict[str, Any]],
             cap: int = plan.MAX_ESCALATIONS, on_progress=None,
             clock=time.monotonic) -> Result:
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
            res = propose(engine, case, idx, cause, proposer, channels, clock=clock)
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
