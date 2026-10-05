"""
Rung 2's loop with v1e's proposal path — §5 of `PLAN_AUTHORSHIP.md`, rule B.

WHAT IS RUNG 2'S HERE, AND WHAT IS NOT. The engine is `rung2.engine2`, called:
`decide`, `add`, `try_edge`, `edge_log`. The decision of a case, the fire counts
and the record of each case are `rung2/shadow2.py`'s, field for field, and
`compute_metrics2` reads them. **Only the proposal path differs**, and with
`v1e=False` it is v1's, line for line: `E-g3` replays a recorded v1 run through
it and requires every record, rule and verdict back.

WHERE THE LABELS COME FROM. `rung2/shadow2.py` labels its records by importing
the oracle, and a proposer path may not (`tests/test_oracle_separation.py`). So
the loop is handed each case's `(truth, truth_rule)`, read by `authorship/run.py`
off `PLAN_REUSE.md`'s records of the same corpus, which `E-g3` checks against one
another and against rung 1's. The proposer never sees them.

V1E'S PATH, §5.2 and §5.3, for one escalation:

  1. The first answer. An order answer on a CONFLICT orders the rules shown, on
     an IMPASSE it is refused; a rule must match the ticket, must not copy an
     existing rule, and must place every rule of `O`.
  2. If it leaves rules of `O` unplaced, one repair round lists them, and the
     second answer is validated from the start.
  3. A rule that still leaves one unplaced is refused, `sin_situar`. A refused
     rule is not installed and the case keeps the proposer's answer as its
     decision, as v1 does with a rule it rejects.

Every edge the engine is asked about is logged in order, `(winner, loser,
verdict)` as v1 logs it, with its channel beside it in `edge_channels`. **An edge
of the order channel is not written into any rule's `beats` or `loses_to`**:
those keep, as in v1, the edges accepted at the rule's birth, which is what
`fidelity/replay.py` and `edges/rebuild.py` assume.
"""

from __future__ import annotations

import collections
import time
from dataclasses import dataclass, field
from typing import Any

from harness.domain import Case

from rung2.engine2 import EDGE_OK, PriorityEngine, RuleValidationError, validate_conditions
from rung2.proposers2 import ProposalError
from rung2.shadow2 import Record2, RunResult2, compute_metrics2

from . import plan
from . import protocol as p


@dataclass
class Escalation:
    """What v1e adds to a case's record: every call, and how it ended."""
    idx: int
    kind: str
    verdict: str
    calls: list[dict[str, Any]] = field(default_factory=list)
    rule_id: str | None = None
    copy_of: str | None = None
    listed: list[str] = field(default_factory=list)
    order: list[list[str]] = field(default_factory=list)


@dataclass
class LoopResult:
    run: RunResult2
    escalations: list[Escalation]
    edge_channels: list[str]
    calls: int


def install_declarations(engine: PriorityEngine, rule, payload: dict,
                         allowed: set[str], channel: str,
                         channels: list[str]) -> tuple[int, int, list[str]]:
    """v1's installation of a born rule's edges: `beats` then `loses_to`, a
    citation outside `allowed` dropped before `try_edge`, every verdict logged.
    Returns (proposed, accepted, reasons)."""
    n_prop = n_acc = 0
    reasons: list[str] = []
    for direction in ("beats", "loses_to"):
        for ref in p.citations(payload, direction):
            n_prop += 1
            if ref not in allowed:
                reasons.append(p.OUTSIDE)
                rule.dropped_edges.append(f"{direction}:{ref}")
                continue
            w, l = ((rule.rule_id, ref) if direction == "beats"
                    else (ref, rule.rule_id))
            why = engine.try_edge(w, l)
            reasons.append(why)
            engine.edge_log.append((w, l, why))
            channels.append(channel)
            if why == EDGE_OK:
                n_acc += 1
                if direction == "beats":
                    rule.beats.append(ref)
                else:
                    rule.loses_to.append(ref)
            else:
                rule.dropped_edges.append(f"{direction}:{ref}:{why}")
    return n_prop, n_acc, reasons


def install_order(engine: PriorityEngine, payload: dict, shown: set[str],
                  channels: list[str]) -> tuple[int, int, list[str], list[list[str]]]:
    """§5.3: each pair of an order answer through `try_edge`, citing only the
    rules shown. Nothing is written into a rule."""
    n_prop = n_acc = 0
    reasons: list[str] = []
    pairs: list[list[str]] = []
    for pair in p.order_pairs(payload):
        n_prop += 1
        if pair is None:
            reasons.append(p.MALFORMED_PAIR)
            continue
        w, l = pair
        if w not in shown or l not in shown:
            reasons.append(p.OUTSIDE)
            pairs.append([w, l, p.OUTSIDE])
            continue
        why = engine.try_edge(w, l)
        reasons.append(why)
        engine.edge_log.append((w, l, why))
        channels.append(p.ORDER_CHANNEL)
        pairs.append([w, l, why])
        if why == EDGE_OK:
            n_acc += 1
    return n_prop, n_acc, reasons, pairs


def call_row(round_: int, answer: p.Answer | None, failure: str | None = None,
             finish: str | None = None, attempts: int | None = None,
             seconds: float | None = None) -> dict[str, Any]:
    return {"round": round_,
            "form": (None if answer is None else
                     "order" if p.is_order(answer.payload) else "rule"),
            "finish_reason": answer.finish_reason if answer else finish,
            "attempts": answer.attempts if answer else attempts,
            "raw": answer.raw if answer else None,
            "payload": answer.payload if answer else None,
            "failure": failure,
            "seconds": seconds}


def propose_v1e(engine: PriorityEngine, case: Case, idx: int, outcome: str,
                shown_ids: list[str], base_text: str, proposer,
                channels: list[str], clock=time.monotonic) -> dict[str, Any]:
    """One escalation under v1e. Returns what the case's record needs."""
    shown = set(shown_ids)
    allowed = set(shown)
    esc = Escalation(idx=idx, kind=outcome, verdict=p.FAILED)
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [],
           "reason": None, "failed": False, "rejected": False, "esc": esc}
    previous: p.Answer | None = None
    message = ""
    for round_ in range(plan.REPAIR_ROUNDS + 1):
        t0 = clock()
        try:
            answer = (proposer.first(case, base_text, idx=idx) if round_ == 0 else
                      proposer.repair(case, base_text, previous, message, idx=idx))
        except ProposalError as exc:
            esc.calls.append(call_row(round_, None, failure=str(exc)[:300],
                                      finish=getattr(exc, "finish_reason", None),
                                      attempts=getattr(exc, "attempts", None),
                                      seconds=round(clock() - t0, 2)))
            if round_ == 0:
                out.update(failed=True, reason=f"proposal_failed: {exc}")
                return out
            esc.verdict = p.UNPLACED              # the repair never came back
            out.update(rejected=True, reason=p.UNPLACED)
            return out
        esc.calls.append(call_row(round_, answer, seconds=round(clock() - t0, 2)))
        out["action"] = answer.action
        payload = answer.payload

        if p.is_order(payload):
            if outcome != "CONFLICT":
                esc.verdict = p.ORDER_WITHOUT_CONFLICT
                out.update(rejected=True, reason=p.ORDER_WITHOUT_CONFLICT)
                return out
            n_prop, n_acc, reasons, pairs = install_order(engine, payload, shown,
                                                          channels)
            esc.verdict, esc.order = p.ORDER, pairs
            out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
            return out

        try:
            rule = validate_conditions(payload, case=case)
        except RuleValidationError as exc:
            esc.verdict = p.REJECTED
            out.update(rejected=True, reason=str(exc))
            return out
        ext = engine.space.extension(rule.conditions)
        copies = p.copies_of(engine, ext)
        if copies:
            esc.verdict, esc.copy_of = p.COPY, copies[0]
            out.update(rejected=True, reason=f"{p.COPY}: {copies[0]}")
            return out
        o = p.overlapped(engine, ext)
        missing = p.unplaced(o, payload, allowed)
        esc.calls[-1].update(overlapped=o, unplaced=missing)
        if not missing:
            engine.add(rule, born_at=idx)
            n_prop, n_acc, reasons = install_declarations(
                engine, rule, payload, allowed, p.WRITE, channels)
            esc.verdict, esc.rule_id = p.BORN, rule.rule_id
            out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
            return out
        if round_ == plan.REPAIR_ROUNDS:
            esc.verdict = p.UNPLACED
            out.update(rejected=True, reason=p.UNPLACED)
            return out
        esc.listed = p.listing(missing, idx, round_)
        esc.calls[-1].update(listed=list(esc.listed))
        allowed |= set(esc.listed)
        message = p.repair_message(engine, esc.listed)
        previous = answer
    return out                                     # unreachable: the last round returns


def propose_v1(engine: PriorityEngine, case: Case, idx: int, shown_ids: list[str],
               base_text: str, proposer, channels: list[str]) -> dict[str, Any]:
    """`rung2/shadow2.py`'s proposal path, as it produced the baseline."""
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [], "reason": None,
           "failed": False, "rejected": False, "esc": None}
    try:
        action, payload = proposer.propose(case, base_text)
    except ProposalError as exc:
        out.update(failed=True, reason=f"proposal_failed: {exc}")
        return out
    out["action"] = action
    try:
        rule = validate_conditions(payload, case=case)
        engine.add(rule, born_at=idx)
        n_prop, n_acc, reasons = install_declarations(
            engine, rule, payload, set(shown_ids), p.WRITE, channels)
        out.update(n_prop=n_prop, n_acc=n_acc, reasons=reasons)
    except RuleValidationError as exc:
        out.update(rejected=True, reason=str(exc))
    return out


def run_loop(corpus: list[Case], labels: list[tuple[str, str]],
             engine: PriorityEngine, proposer, *, v1e: bool = True,
             on_progress=None) -> LoopResult:
    """The loop over `corpus`, case by case and in order: hard rule 3."""
    records: list[Record2] = []
    escalations: list[Escalation] = []
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
            res = (propose_v1e(engine, case, idx, outcome, shown_ids, base_text,
                               proposer, channels) if v1e else
                   propose_v1(engine, case, idx, shown_ids, base_text, proposer,
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
    return LoopResult(res2, escalations, channels, calls)
