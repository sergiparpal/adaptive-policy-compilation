"""
Rung 2 shadow loop.

Invariants inherited from rung 1, unchanged:
  * no rule is activated; what WOULD have happened is recorded
  * the hidden policy only labels the record; the engine and the proposer never
    see it
  * the only escalation trigger is a coverage IMPASSE or a CONFLICT, never "the
    answer was incorrect"
  * strictly sequential

What is newly recorded: the fate of every proposed priority edge.
"""

from __future__ import annotations

import collections
import statistics
from dataclasses import dataclass, field
from typing import Any

from harness.domain import Case
from harness.dsl import RuleValidationError
from harness.hidden_policy import HIDDEN_POLICY_SIZE, true_action, true_rule_id

from .engine2 import PriorityEngine, validate_conditions
from .proposers2 import ProposalError, neighbourhood, render_base_v1


@dataclass
class Record2:
    idx: int
    outcome: str
    predicted: str | None
    truth: str
    truth_rule: str
    correct: bool | None
    winner_id: str | None
    n_matched: int
    escalated: bool
    shown_ids: list[str] = field(default_factory=list)
    shown_kind: str | None = None
    proposal_action_correct: bool | None = None
    edges_proposed: int = 0
    edges_accepted: int = 0
    edge_reasons: list[str] = field(default_factory=list)
    rejected_reason: str | None = None


@dataclass
class RunResult2:
    proposer_name: str
    n_cases: int
    records: list[Record2]
    rules: list
    rejected: int
    failed: int = 0
    edge_stats: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)


def run_shadow2(corpus: list[Case], engine: PriorityEngine, proposer,
                on_progress=None) -> RunResult2:
    records: list[Record2] = []
    rejected = failed = 0
    edge_reasons = collections.Counter()

    for idx, case in enumerate(corpus):
        truth = true_action(case)
        trule = true_rule_id(case)

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
            if hasattr(proposer, "build_base"):
                shown, shown_kind, base_text = proposer.build_base(
                    engine, case, undefeated)
            else:                                   # mock proposers used in tests
                shown, shown_kind = neighbourhood(engine, case, undefeated)
                base_text = render_base_v1(shown, shown_kind, engine, case)
            shown_ids = [r.rule_id for r in shown]
            allowed = set(shown_ids)

            try:
                action, payload = proposer.propose(case, base_text)
            except ProposalError as exc:
                failed += 1
                reason = f"proposal_failed: {exc}"
                action, payload = None, None

            if payload is not None:
                predicted = action
                prop_ok = action == truth
                correct = prop_ok
                try:
                    rule = validate_conditions(payload, case=case)
                    engine.add(rule, born_at=idx)

                    # edges: they may only cite rules that were shown
                    for direction in ("beats", "loses_to"):
                        raw = payload.get(direction) or []
                        if isinstance(raw, str):
                            raw = [raw]
                        if not isinstance(raw, list):
                            continue
                        for ref in raw:
                            ref = str(ref).strip()
                            n_prop += 1
                            if ref not in allowed:
                                reasons.append("fuera_del_vecindario")
                                rule.dropped_edges.append(f"{direction}:{ref}")
                                continue
                            w, l = ((rule.rule_id, ref) if direction == "beats"
                                    else (ref, rule.rule_id))
                            why = engine.try_edge(w, l)
                            reasons.append(why)
                            engine.edge_log.append((w, l, why))
                            if why == "ok":
                                n_acc += 1
                                if direction == "beats":
                                    rule.beats.append(ref)
                                else:
                                    rule.loses_to.append(ref)
                            else:
                                rule.dropped_edges.append(f"{direction}:{ref}:{why}")
                except RuleValidationError as exc:
                    rejected += 1
                    reason = str(exc)
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

    res = RunResult2(
        proposer_name=getattr(proposer, "name", "?"),
        n_cases=len(corpus), records=records, rules=engine.rules,
        rejected=rejected, failed=failed, edge_stats=dict(edge_reasons),
    )
    res.metrics = compute_metrics2(res, engine)
    return res


def compute_metrics2(res: RunResult2, engine: PriorityEngine) -> dict[str, Any]:
    recs = res.records
    n = len(recs)
    esc = [r for r in recs if r.escalated]
    cov = [r for r in recs if r.outcome == "ACTION"]
    n_cov = len(cov)
    n_ok = sum(1 for r in cov if r.correct)

    fires = [r.fire_count for r in res.rules]
    n_rules = len(res.rules)
    bucket = max(1, n // 10)
    curve = [round(sum(1 for r in recs[b:b + bucket] if r.escalated)
                   / len(recs[b:b + bucket]), 3)
             for b in range(0, n, bucket) if recs[b:b + bucket]]

    declared = sum(len(r.beats) + len(r.loses_to) for r in res.rules)
    return {
        "n_cases": n,
        "n_rules": n_rules,
        "hidden_policy_size": HIDDEN_POLICY_SIZE,
        "rejected_rules": res.rejected,
        "failed_proposals": res.failed,
        "escalations": len(esc),
        "escalation_rate": round(len(esc) / n, 4),
        "escalation_curve_by_decile": curve,
        "final_decile_escalation_rate": curve[-1] if curve else None,
        "impasses": sum(1 for r in recs if r.outcome == "IMPASSE"),
        "conflicts": sum(1 for r in recs if r.outcome == "CONFLICT"),
        "coverage": round(n_cov / n, 4),
        "shadow_accuracy": round(n_ok / n_cov, 4) if n_cov else None,
        "silent_error_rate": round(1 - n_ok / n_cov, 4) if n_cov else None,
        "silent_errors_abs": n_cov - n_ok,
        "e2e_accuracy": round(n_ok / n, 4),
        "reuse_rate": round(sum(1 for f in fires if f >= 1) / n_rules, 4) if n_rules else None,
        "median_fires_per_rule": statistics.median(fires) if fires else 0,
        "dead_rules": sum(1 for f in fires if f == 0),
        "proposal_action_accuracy": (
            round(sum(1 for r in esc if r.proposal_action_correct) / len(esc), 4)
            if esc else None),
        "llm_calls": len(esc),
        # --- declared priority ----------------------------------------------
        "edges_proposed": sum(r.edges_proposed for r in recs),
        "edges_accepted": declared,
        "edge_reasons": res.edge_stats,
        "subsumption_pairs": sum(len(s) for s in engine.sub_below.values()),
        "rules_with_edges": sum(1 for r in res.rules if r.beats or r.loses_to),
        "escalations_with_base_shown": sum(1 for r in esc if r.shown_ids),
        "escalations_on_conflict": sum(1 for r in esc if r.shown_kind == "conflicto"),
    }
