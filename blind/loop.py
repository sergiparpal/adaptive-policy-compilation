"""
Rung 2's loop with v2b's proposal path — §5 of `PLAN_BLIND.md`, rules A and B.

WHAT IS `PLAN_OVERLAP.md`'S HERE, CALLED AND NOT EDITED. A CONFLICT goes through
`overlap.loop.propose_v2e`, v2e's path, line for line: its screen shows the rules
in conflict, so it is not blind, and an order answer can cite them. With
`blind=False` an impasse is v2e's too, and the loop is `overlap.loop.run_loop`:
`K-g3` replays `PLAN_OVERLAP.md`'s runs through it and requires every record,
rule, edge and call back. `overlap/` and `authorship/` are not touched, so that
their records keep reproducing.

WHAT IS THIS PLAN'S. `propose_blind`, for an impasse, §5.1 and §5.2:

  1. The draft, with no rule shown. An order answer is refused, as on any
     impasse; a rule must match the ticket and must not copy an existing rule.
  2. `O`, the existing rules of another queue the draft overlaps, and `S`, those
     of its own queue, recorded on the call. With `O` empty the rule is born and
     nothing is declared.
  3. Otherwise one placement round lists `O` in the seeded order and asks for the
     same rule placed against each. The second answer must be a rule, match the
     ticket, be the draft's rule (`protocol.same_rule`), and place every rule of
     `O`; each failure has its verdict, and a refused rule is not installed. The
     case keeps the proposer's last answer as its decision, as v2e does.

`run_loop` is `overlap.loop.run_loop` with that path on an impasse. It is a copy
because v2e's loop names its own path; `K-g3`'s replay holds the copy to v2e's.

WHERE THE LABELS COME FROM. As in v2e's loop: handed in, read off the baselines'
records of the same corpus, so that no proposer path imports the oracle
(`tests/test_oracle_separation.py`). The proposer never sees them.
"""

from __future__ import annotations

import collections
import time
from typing import Any

from harness.domain import Case

from authorship import loop as eloop
from authorship import protocol as e
from overlap import loop as loop2e
from rung2.engine2 import PriorityEngine, RuleValidationError, validate_conditions
from rung2.proposers2 import ProposalError
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import protocol as p


def _failed_call(esc, round_: int, exc: Exception, t0: float, clock) -> None:
    esc.calls.append(eloop.call_row(round_, None, failure=str(exc)[:300],
                                    finish=getattr(exc, "finish_reason", None),
                                    attempts=getattr(exc, "attempts", None),
                                    seconds=round(clock() - t0, 2)))


def _refused(esc, out: dict, verdict: str, reason: str | None = None) -> dict[str, Any]:
    esc.verdict = verdict
    out.update(rejected=True, reason=reason or verdict)
    return out


def _born(engine: PriorityEngine, rule, payload: dict, allowed: set[str], idx: int,
          channels: list[str], esc, out: dict) -> dict[str, Any]:
    engine.add(rule, born_at=idx)
    n_prop, n_acc, reasons = eloop.install_declarations(engine, rule, payload, allowed,
                                                        e.WRITE, channels)
    esc.verdict, esc.rule_id = e.BORN, rule.rule_id
    out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
    return out


def _a_rule(esc, out: dict, answer: e.Answer, case: Case):
    """The answer's rule, or the verdict that refuses it: an order answer on an
    impasse, or a rule that does not validate."""
    if e.is_order(answer.payload):
        return None, _refused(esc, out, e.ORDER_WITHOUT_CONFLICT)
    try:
        return validate_conditions(answer.payload, case=case), None
    except RuleValidationError as exc:
        return None, _refused(esc, out, e.REJECTED, str(exc))


def propose_blind(engine: PriorityEngine, case: Case, idx: int, outcome: str,
                  shown_ids: list[str], base_text: str, proposer,
                  channels: list[str], clock=time.monotonic) -> dict[str, Any]:
    """One escalation on an impasse under v2b. Returns what the case's record
    needs, in the shape `overlap.loop.propose_v2e` returns it."""
    esc = eloop.Escalation(idx=idx, kind=outcome, verdict=e.FAILED)
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [],
           "reason": None, "failed": False, "rejected": False, "esc": esc}

    t0 = clock()
    try:
        draft = proposer.first(case, base_text, idx=idx)
    except ProposalError as exc:
        _failed_call(esc, 0, exc, t0, clock)
        out.update(failed=True, reason=f"proposal_failed: {exc}")
        return out
    esc.calls.append(eloop.call_row(0, draft, seconds=round(clock() - t0, 2)))
    out["action"] = draft.action
    rule, refused = _a_rule(esc, out, draft, case)
    if refused is not None:
        return refused
    ext = engine.space.extension(rule.conditions)
    copies = e.copies_of(engine, ext)
    if copies:
        esc.copy_of = copies[0]
        return _refused(esc, out, e.COPY, f"{e.COPY}: {copies[0]}")
    o, s = p.split_overlapped(engine, ext, rule.action)
    esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=list(o))
    if not o:
        return _born(engine, rule, draft.payload, set(), idx, channels, esc, out)

    esc.listed = p.listing(o, idx, 0)
    esc.calls[-1].update(listed=list(esc.listed))
    allowed = set(esc.listed)
    t0 = clock()
    try:
        placed = proposer.repair(case, base_text, draft,
                                 p.placement_message(engine, esc.listed), idx=idx)
    except ProposalError as exc:
        _failed_call(esc, 1, exc, t0, clock)
        return _refused(esc, out, e.UNPLACED)    # the placement never came back
    esc.calls.append(eloop.call_row(1, placed, seconds=round(clock() - t0, 2)))
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


def run_loop(corpus: list[Case], labels: list[tuple[str, str]],
             engine: PriorityEngine, proposer, *, blind: bool = True,
             on_progress=None, clock=time.monotonic) -> eloop.LoopResult:
    """The loop over `corpus`, case by case and in order: hard rule 3. A CONFLICT
    goes through v2e's path; an impasse through v2b's, or v2e's with
    `blind=False`, as `K-g3` replays it."""
    records: list[Record2] = []
    escalations: list[eloop.Escalation] = []
    channels: list[str] = []
    rejected = failed = calls = 0
    edge_reasons = collections.Counter()

    for idx, case in enumerate(corpus):
        truth, trule = labels[idx]
        outcome, winner, involved = engine.decide(case)
        escalated = False
        predicted = correct = prop_ok = reason = None
        shown_ids: list[str] = []
        shown_kind = None
        n_prop = n_acc = 0
        reasons: list[str] = []

        if outcome == "ACTION":
            predicted = winner.action
            correct = predicted == truth
            winner.fire_count += 1
            if correct:
                winner.correct_count += 1
        else:
            escalated = True
            undefeated = involved if outcome == "CONFLICT" else []
            shown, shown_kind, base_text = proposer.build_base(engine, case, undefeated)
            shown_ids = [r.rule_id for r in shown]
            path = (propose_blind if blind and outcome != "CONFLICT"
                    else loop2e.propose_v2e)
            res = path(engine, case, idx, outcome, shown_ids, base_text, proposer,
                       channels, clock=clock)
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

        records.append(Record2(
            idx=idx, outcome=outcome, predicted=predicted, truth=truth,
            truth_rule=trule, correct=correct,
            winner_id=winner.rule_id if winner else None,
            n_matched=len(involved), escalated=escalated,
            shown_ids=shown_ids, shown_kind=shown_kind,
            proposal_action_correct=prop_ok,
            edges_proposed=n_prop, edges_accepted=n_acc,
            edge_reasons=reasons, rejected_reason=reason,
        ))
        if on_progress is not None:
            on_progress(idx, len(corpus), len(engine.rules),
                        sum(1 for r in records if r.escalated))

    res2 = RunResult2(proposer_name=getattr(proposer, "name", "?"),
                      n_cases=len(corpus), records=records, rules=engine.rules,
                      rejected=rejected, failed=failed, edge_stats=dict(edge_reasons))
    res2.metrics = compute_metrics2(res2, engine)
    return eloop.LoopResult(res2, escalations, channels, calls)
