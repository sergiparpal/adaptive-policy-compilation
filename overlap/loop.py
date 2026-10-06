"""
Rung 2's loop with v2e's proposal path — §5 of `PLAN_OVERLAP.md`, rules A and B.

WHAT IS `PLAN_AUTHORSHIP.md`'S HERE, CALLED AND NOT EDITED. The installation of
a born rule's declarations and of an order answer, the row each call leaves, the
record of an escalation, and, with the discipline off, rung 2's own proposal path
(`authorship.loop.propose_v1`), which `O-g3` holds to rung 2 by replaying its four
v2 records. `authorship/loop.py` is not touched, so that `PLAN_AUTHORSHIP.md`'s
records keep reproducing.

WHAT IS THIS PLAN'S.

  `propose_v2e`  `authorship.loop.propose_v1e` with its one change: `O` is the
                 overlapped rules of another queue, and `S`, those of the same
                 queue, is recorded beside it on the call that computed it; the
                 repair round lists only `O`'s missing rules, under v2e's message.
  `run_loop`     `authorship.loop.run_loop` with that path in place of v1e's. It
                 is a copy because v1e's loop names its own path; `O-g3`'s replay
                 is what holds the copy to rung 2's line by line.

WHERE THE LABELS COME FROM. As in v1e's loop: handed in, read off the baselines'
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
from rung2.engine2 import PriorityEngine, RuleValidationError, validate_conditions
from rung2.proposers2 import ProposalError
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import plan
from . import protocol as v


def propose_v2e(engine: PriorityEngine, case: Case, idx: int, outcome: str,
                shown_ids: list[str], base_text: str, proposer,
                channels: list[str], clock=time.monotonic) -> dict[str, Any]:
    """One escalation under v2e. Returns what the case's record needs."""
    shown = set(shown_ids)
    allowed = set(shown)
    esc = eloop.Escalation(idx=idx, kind=outcome, verdict=e.FAILED)
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [],
           "reason": None, "failed": False, "rejected": False, "esc": esc}
    previous: e.Answer | None = None
    message = ""
    for round_ in range(plan.REPAIR_ROUNDS + 1):
        t0 = clock()
        try:
            answer = (proposer.first(case, base_text, idx=idx) if round_ == 0 else
                      proposer.repair(case, base_text, previous, message, idx=idx))
        except ProposalError as exc:
            esc.calls.append(eloop.call_row(round_, None, failure=str(exc)[:300],
                                            finish=getattr(exc, "finish_reason", None),
                                            attempts=getattr(exc, "attempts", None),
                                            seconds=round(clock() - t0, 2)))
            if round_ == 0:
                out.update(failed=True, reason=f"proposal_failed: {exc}")
                return out
            esc.verdict = e.UNPLACED              # the repair never came back
            out.update(rejected=True, reason=e.UNPLACED)
            return out
        esc.calls.append(eloop.call_row(round_, answer, seconds=round(clock() - t0, 2)))
        out["action"] = answer.action
        payload = answer.payload

        if e.is_order(payload):
            if outcome != "CONFLICT":
                esc.verdict = e.ORDER_WITHOUT_CONFLICT
                out.update(rejected=True, reason=e.ORDER_WITHOUT_CONFLICT)
                return out
            n_prop, n_acc, reasons, pairs = eloop.install_order(engine, payload, shown,
                                                                channels)
            esc.verdict, esc.order = e.ORDER, pairs
            out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
            return out

        try:
            rule = validate_conditions(payload, case=case)
        except RuleValidationError as exc:
            esc.verdict = e.REJECTED
            out.update(rejected=True, reason=str(exc))
            return out
        ext = engine.space.extension(rule.conditions)
        copies = e.copies_of(engine, ext)
        if copies:
            esc.verdict, esc.copy_of = e.COPY, copies[0]
            out.update(rejected=True, reason=f"{e.COPY}: {copies[0]}")
            return out
        o, s = v.split_overlapped(engine, ext, rule.action)
        missing = e.unplaced(o, payload, allowed)
        esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=missing)
        if not missing:
            engine.add(rule, born_at=idx)
            n_prop, n_acc, reasons = eloop.install_declarations(
                engine, rule, payload, allowed, e.WRITE, channels)
            esc.verdict, esc.rule_id = e.BORN, rule.rule_id
            out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
            return out
        if round_ == plan.REPAIR_ROUNDS:
            esc.verdict = e.UNPLACED
            out.update(rejected=True, reason=e.UNPLACED)
            return out
        esc.listed = v.listing(missing, idx, round_)
        esc.calls[-1].update(listed=list(esc.listed))
        allowed |= set(esc.listed)
        message = v.repair_message(engine, esc.listed)
        previous = answer
    return out                                     # unreachable: the last round returns


def run_loop(corpus: list[Case], labels: list[tuple[str, str]],
             engine: PriorityEngine, proposer, *, v2e: bool = True,
             on_progress=None) -> eloop.LoopResult:
    """The loop over `corpus`, case by case and in order: hard rule 3. With
    `v2e=False` the proposal path is rung 2's own, as `O-g3` replays it."""
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
            res = (propose_v2e(engine, case, idx, outcome, shown_ids, base_text,
                               proposer, channels) if v2e else
                   eloop.propose_v1(engine, case, idx, shown_ids, base_text, proposer,
                                    channels))
            if res["esc"] is not None:
                escalations.append(res["esc"])
                calls += len(res["esc"].calls)
            else:
                calls += 1
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
