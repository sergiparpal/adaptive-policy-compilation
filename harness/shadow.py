"""
Bucle en sombra + metricas.

PROPIEDAD CENTRAL: ninguna regla se activa jamas. Se registra lo que HABRIA
pasado. Como los tickets son independientes (sin estado compartido), la decision
registrada no influye en el resto del corpus: la sombra es exacta, no una
aproximacion.

SEPARACION DEL ORACULO: la politica oculta se consulta solo para etiquetar el
registro. El motor y el proponente nunca la ven. El unico disparador de
escalacion es el impasse de cobertura o de conflicto -- nunca "la respuesta era
incorrecta". Esa es justamente la condicion que hace medible el error silencioso.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import Any

from .domain import Case
from .dsl import Rule, RuleEngine, RuleValidationError, validate_rule_payload
from .proposers import ProposalError
from .hidden_policy import HIDDEN_POLICY_SIZE, true_action, true_rule_id


@dataclass
class Record:
    idx: int
    outcome: str                 # ACTION | IMPASSE | CONFLICT
    predicted: str | None
    truth: str
    truth_rule: str
    correct: bool | None
    winner_id: str | None
    n_matched: int
    escalated: bool
    proposal_action_correct: bool | None = None
    rejected_reason: str | None = None


@dataclass
class RunResult:
    proposer_name: str
    n_cases: int
    records: list[Record]
    rules: list[Rule]
    rejected: int
    failed: int = 0
    metrics: dict[str, Any] = field(default_factory=dict)


def run_shadow(
    corpus: list[Case],
    engine: RuleEngine,
    proposer,
    escalate_on_conflict: bool = True,
    on_progress=None,
) -> RunResult:
    records: list[Record] = []
    rejected = 0
    failed = 0

    for idx, case in enumerate(corpus):
        truth = true_action(case)          # solo para el registro
        trule = true_rule_id(case)

        outcome, winner, matched = engine.decide(case)

        escalated = False
        predicted: str | None = None
        correct: bool | None = None
        prop_ok: bool | None = None
        reason: str | None = None

        if outcome == "ACTION":
            predicted = winner.action
            correct = predicted == truth
            winner.fire_count += 1
            if correct:
                winner.correct_count += 1
        else:
            # IMPASSE de cobertura, o CONFLICT logico
            if outcome == "CONFLICT" and not escalate_on_conflict:
                pass
            else:
                escalated = True
                try:
                    action, payload = proposer.propose(case, true_action_hint=truth)
                except ProposalError as exc:
                    # El proponente no devolvio nada usable. Se cuenta y se sigue:
                    # una tirada larga no puede morir por un JSON mal cerrado.
                    failed += 1
                    reason = f"proposal_failed: {exc}"
                    action, payload = None, None

                if payload is not None:
                    predicted = action
                    prop_ok = action == truth
                    correct = prop_ok
                    try:
                        rule = validate_rule_payload(payload, case=case)
                        engine.add(rule, born_at=idx)
                    except RuleValidationError as exc:
                        rejected += 1
                        reason = str(exc)

        records.append(
            Record(
                idx=idx,
                outcome=outcome,
                predicted=predicted,
                truth=truth,
                truth_rule=trule,
                correct=correct,
                winner_id=winner.rule_id if winner else None,
                n_matched=len(matched),
                escalated=escalated,
                proposal_action_correct=prop_ok,
                rejected_reason=reason,
            )
        )

        if on_progress is not None:
            on_progress(idx, len(corpus), len(engine.rules), sum(1 for r in records if r.escalated))

    res = RunResult(
        proposer_name=getattr(proposer, "name", "?"),
        n_cases=len(corpus),
        records=records,
        rules=engine.rules,
        rejected=rejected,
        failed=failed,
    )
    res.metrics = compute_metrics(res)
    return res


# ---------------------------------------------------------------------------
# Metricas
# ---------------------------------------------------------------------------

def compute_metrics(res: RunResult) -> dict[str, Any]:
    recs = res.records
    n = len(recs)

    escalations = [r for r in recs if r.escalated]
    covered = [r for r in recs if r.outcome == "ACTION"]
    conflicts = [r for r in recs if r.outcome == "CONFLICT"]

    n_cov = len(covered)
    n_correct_cov = sum(1 for r in covered if r.correct)

    # --- reutilizacion ----------------------------------------------------
    fires = [r.fire_count for r in res.rules]
    reused = [f for f in fires if f >= 1]
    n_rules = len(res.rules)

    # cuota del decil superior de reglas sobre el total de disparos
    total_fires = sum(fires) or 1
    top_decile_n = max(1, n_rules // 10)
    top_decile_share = sum(sorted(fires, reverse=True)[:top_decile_n]) / total_fires

    # --- curva de escalacion por decil ------------------------------------
    bucket = max(1, n // 10)
    curve = []
    for b in range(0, n, bucket):
        chunk = recs[b : b + bucket]
        if chunk:
            curve.append(round(sum(1 for r in chunk if r.escalated) / len(chunk), 3))

    # --- exactitud por regla ----------------------------------------------
    per_rule_acc = [
        r.correct_count / r.fire_count for r in res.rules if r.fire_count >= 3
    ]

    return {
        "n_cases": n,
        "n_rules": n_rules,
        "hidden_policy_size": HIDDEN_POLICY_SIZE,
        "compression_ratio": round(n_rules / HIDDEN_POLICY_SIZE, 2),
        "rejected_rules": res.rejected,
        "failed_proposals": res.failed,

        "escalations": len(escalations),
        "escalation_rate": round(len(escalations) / n, 4),
        "escalation_curve_by_decile": curve,
        "final_decile_escalation_rate": curve[-1] if curve else None,

        "coverage": round(n_cov / n, 4),
        "conflicts": len(conflicts),

        # LA metrica de error silencioso: casos donde una regla disparo con
        # total confianza y estaba equivocada. El sistema no puede detectarlos.
        "shadow_accuracy": round(n_correct_cov / n_cov, 4) if n_cov else None,
        "silent_error_rate": round(1 - n_correct_cov / n_cov, 4) if n_cov else None,
        "silent_errors_abs": n_cov - n_correct_cov,

        # LA metrica que decide si la arquitectura tiene sentido
        "reuse_rate": round(len(reused) / n_rules, 4) if n_rules else None,
        "median_fires_per_rule": statistics.median(fires) if fires else 0,
        "mean_fires_per_rule": round(statistics.mean(fires), 2) if fires else 0,
        "top_decile_fire_share": round(top_decile_share, 3),
        "dead_rules": sum(1 for f in fires if f == 0),

        "median_rule_accuracy": (
            round(statistics.median(per_rule_acc), 3) if per_rule_acc else None
        ),
        "proposal_action_accuracy": (
            round(sum(1 for r in escalations if r.proposal_action_correct) / len(escalations), 4)
            if escalations and escalations[0].proposal_action_correct is not None
            else None
        ),

        # coste proxy: 1 llamada de LLM por escalacion
        "llm_calls": len(escalations),
        "llm_calls_per_100_cases_final_decile": (
            round(curve[-1] * 100, 1) if curve else None
        ),
    }
