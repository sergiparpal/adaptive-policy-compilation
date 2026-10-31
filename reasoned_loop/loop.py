"""
Rung 2's loop under v1b, with either trigger — §5 of `PLAN_REASONED_LOOP.md`.
**On the proposer's path**: the labels are handed in, and nothing here imports
the policy (rule B of the plan).

WHAT IS `PLAN_BLIND.md`'S, CALLED AND NOT EDITED. The draft is read by
`blind.loop`'s `_a_rule`: an answer carrying `order` is refused, and a rule must
pass rung 2's validator and match its ticket. A birth goes through `_born`,
which installs the rule and its citations through
`authorship.loop.install_declarations`; a refusal through `_refused`; a call
that never came back through `_failed_call`. `O`, the listing, the placement
message and the check that the second answer is the draft's rule are
`blind.protocol`'s.

WHAT IS THIS PLAN'S (§5.2, §5.3).

  `escalates`   the trigger. Both arms escalate an IMPASSE or a CONFLICT; the
                error arm also escalates a case the engine decided with a
                queue other than its label.
  `propose_v1b` one escalation: the draft, blind at every escalation, then the
                placement round when `O` is not empty. **There is no copy
                check** (§2.3): a rule whose extension equals an existing one's
                is born and placed like any other, and the call records which
                rules it copies.
  `run_loop`    the loop, case by case and in order (hard rule 3). It keeps each
                escalation's cause, the queue and rule an error escalation
                overrode, `cover`, the case after which every point of the space
                matches a rule of the base, and stops at `plan.MAX_ESCALATIONS`.
  `record_of`   what a run's record holds, so that the gates read a run of the
                transcriber in the same shape as a paid run.

AN ERROR ESCALATION'S RULE IS NOT COUNTED AS FIRED. Its decision did not stand:
the proposer's answer replaced it, as at any escalation. `fire_count` counts the
decisions that stood, so rung 2's reuse figures mean under the error arm what
they mean under the impasse arm.
"""

from __future__ import annotations

import collections
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from harness.domain import Case

from authorship import loop as eloop
from authorship import protocol as e
from blind.loop import _a_rule, _born, _failed_call, _refused
from rung2.engine2 import PriorityEngine
from rung2.proposers2 import ProposalError
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import plan
from . import protocol as p


def escalates(arm: str, outcome: str, winner, truth: str) -> str | None:
    """The cause of a case's escalation under `arm`, or None (§5.3)."""
    if outcome in (plan.IMPASSE, plan.CONFLICT):
        return outcome
    if plan.ERROR in plan.TRIGGERS[arm] and winner.action != truth:
        return plan.ERROR
    return None


def call_row(round_: int, answer, seconds: float) -> dict[str, Any]:
    """`authorship.loop.call_row`, and what this package keeps beside it."""
    row = eloop.call_row(round_, answer, seconds=round(seconds, 2))
    row.update({k: getattr(answer, k, None) for k in p.EXTRA})
    return row


def propose_v1b(engine: PriorityEngine, case: Case, idx: int, cause: str, proposer,
                channels: list[str], clock=time.monotonic) -> dict[str, Any]:
    """One escalation under v1b (§5.2). Returns what the case's record needs, in
    the shape `blind.loop.propose_blind` returns it."""
    esc = eloop.Escalation(idx=idx, kind=cause, verdict=e.FAILED)
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [],
           "reason": None, "failed": False, "rejected": False, "esc": esc}

    t0 = clock()
    try:
        draft = proposer.first(case, idx=idx)
    except ProposalError as exc:
        _failed_call(esc, 0, exc, t0, clock)
        out.update(failed=True, reason=f"proposal_failed: {exc}")
        return out
    esc.calls.append(call_row(0, draft, clock() - t0))
    out["action"] = draft.action
    rule, refused = _a_rule(esc, out, draft, case)
    if refused is not None:
        return refused
    ext = engine.space.extension(rule.conditions)
    copies = e.copies_of(engine, ext)
    if copies:
        esc.copy_of = copies[0]
    o, s = p.split_overlapped(engine, ext, rule.action)
    esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=list(o), copies=copies)
    if not o:
        return _born(engine, rule, draft.payload, set(), idx, channels, esc, out)

    esc.listed = p.listing(o, idx, 0)
    esc.calls[-1].update(listed=list(esc.listed))
    allowed = set(esc.listed)
    t0 = clock()
    try:
        placed = proposer.placement(case, draft, p.placement_message(engine, esc.listed),
                                    idx=idx, listed=list(esc.listed))
    except ProposalError as exc:
        _failed_call(esc, 1, exc, t0, clock)
        return _refused(esc, out, e.UNPLACED)    # the placement never came back
    esc.calls.append(call_row(1, placed, clock() - t0))
    out["action"] = placed.action
    second, refused = _a_rule(esc, out, placed, case)
    if refused is not None:
        return refused
    if not p.same_rule(rule, second, engine.space):
        return _refused(esc, out, p.CHANGED)
    missing = e.unplaced(o, placed.payload, allowed)
    esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=missing)
    if missing:
        return _refused(esc, out, e.UNPLACED)
    return _born(engine, second, placed.payload, allowed, idx, channels, esc, out)


@dataclass
class Result:
    loop: eloop.LoopResult
    causes: list[dict[str, Any]] = field(default_factory=list)
    cover: int | None = None
    stopped_at: int | None = None

    def summary(self) -> dict[str, Any]:
        by = collections.Counter(c["cause"] for c in self.causes if c["cause"])
        stood = [r for r, c in zip(self.loop.run.records, self.causes)
                 if not c["cause"] and r.outcome == "ACTION"]
        wrong = sum(1 for r in stood if not r.correct)
        return {"arm_escalations": {k: by.get(k, 0) for k in plan.CAUSES},
                "cover": self.cover, "stopped_at": self.stopped_at,
                "cases_read": len(self.loop.run.records),
                "decisions_that_stood": len(stood),
                "silent_errors_among_them": wrong}


def run_loop(corpus: list[Case], labels: list[tuple[str, str]], engine: PriorityEngine,
             proposer, arm: str, *, cap: int = plan.MAX_ESCALATIONS,
             on_progress=None, clock=time.monotonic) -> Result:
    """The loop over `corpus`, case by case and in order: hard rule 3."""
    if arm not in plan.ARMS:
        raise ValueError(f"no arm {arm!r}: {plan.ARMS}")
    records: list[Record2] = []
    causes: list[dict[str, Any]] = []
    escalations: list[eloop.Escalation] = []
    channels: list[str] = []
    rejected = failed = calls = 0
    edge_reasons = collections.Counter()
    union, cover, stopped_at = 0, None, None

    for idx, case in enumerate(corpus):
        truth, trule = labels[idx]
        outcome, winner, involved = engine.decide(case)
        cause = escalates(arm, outcome, winner, truth)
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
                       "engine_rule": winner.rule_id if cause == plan.ERROR else None})
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
                  causes, cover, stopped_at)


def record_of(res: Result, engine: PriorityEngine) -> dict[str, Any]:
    """The part of a run's record the run itself produces. A paid run adds its
    header, `_env` and the checks it ran behind (`reasoned_loop/run.py`)."""
    return {
        "metrics": res.loop.run.metrics,
        "v1b": res.summary(),
        "calls": res.loop.calls,
        "rules": [r.as_dict() for r in res.loop.run.rules],
        "edge_log": engine.edge_log,
        "edge_channels": res.loop.edge_channels,
        "records": [{**vars(r), **c} for r, c in zip(res.loop.run.records, res.causes)],
        "escalations": [asdict(x) for x in res.loop.escalations],
    }
