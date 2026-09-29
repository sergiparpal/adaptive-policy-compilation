"""
The arithmetic of `PLAN_REUSE.md` over one shadow-loop record — pure and free.

A record is what `rung2/run2.py` writes, and `reuse/run.py` writes the same
layout: `metrics`, `rules` — each with `born_at`, `action`, `fire_count` and
`correct_count` — and `records`, one per case, with `outcome`, `escalated`,
`winner_id`, `truth`, `correct`, `predicted` and `proposal_action_correct`.
**Every label used here is read off the record.** No function imports the
oracle; the shadow loop already wrote what it said.

THE TWO AXES (§5.2 of the plan, `CLAUDE.md` Step 5). A silent error is a case a
rule decided wrongly. The *acting* axis is whether the rule was born with the
wrong queue — its birth escalation did not choose the ticket's true queue. The
*scope* axis is whether a rule born with the right queue reaches cases whose
queue is another. `split_silent` attributes every silent error to one axis by
the birth of the rule that made it (`U-c`); `right_born` isolates the rules on
the scope axis, which are the only ones a `keep_k` heuristic handed the right
action can be compared with (`U-b`).

A RULE'S BIRTH (§5.3) is the escalation at its `born_at`. `births` checks what
that assumes — one rule per escalation, an escalation there, a proposal whose
action is the rule's — and reports every exception rather than skipping it: a
record that breaks them cannot be split.

`F` (§5.2) is the `keep_k` frontier at a reuse rate: points
`(reuse_rate, silent_error)`, the lower error where two share a reuse, linear
between the two that bracket, flat beyond the ends. A `keep_k` that decided no
case has no silent error and says nothing about error, so its point is dropped
— at n=2000 that never happens; at n=100 it can, for `keep_k(8)`.
"""

from __future__ import annotations

import collections
import statistics
from typing import Any, Iterable

FAILED = "proposal_failed"


# ---------------------------------------------------------------------------
# U-g2 — a record reproduces its own published metrics
# ---------------------------------------------------------------------------

def curve_by_decile(recs: list[dict]) -> list[float]:
    n = len(recs)
    bucket = max(1, n // 10)
    return [round(sum(1 for r in recs[b:b + bucket] if r["escalated"])
                  / len(recs[b:b + bucket]), 3)
            for b in range(0, n, bucket) if recs[b:b + bucket]]


def recompute_metrics(record: dict) -> dict[str, Any]:
    """Every field of `rung2.shadow2.compute_metrics2` that is a function of
    the record's own `records` and `rules`, with the same rounding. Two fields
    are not and are left out: `hidden_policy_size`, a constant of the oracle,
    and `subsumption_pairs`, which needs the engine."""
    recs, rules = record["records"], record["rules"]
    n = len(recs)
    esc = [r for r in recs if r["escalated"]]
    cov = [r for r in recs if r["outcome"] == "ACTION"]
    n_cov = len(cov)
    n_ok = sum(1 for r in cov if r["correct"])
    fires = [r["fire_count"] for r in rules]
    n_rules = len(rules)
    curve = curve_by_decile(recs)
    reasons: collections.Counter = collections.Counter()
    for r in recs:
        reasons.update(r.get("edge_reasons") or [])
    why = [r.get("rejected_reason") or "" for r in recs]
    return {
        "n_cases": n,
        "n_rules": n_rules,
        "rejected_rules": sum(1 for w in why if w and not w.startswith(FAILED)),
        "failed_proposals": sum(1 for w in why if w.startswith(FAILED)),
        "escalations": len(esc),
        "escalation_rate": round(len(esc) / n, 4),
        "escalation_curve_by_decile": curve,
        "final_decile_escalation_rate": curve[-1] if curve else None,
        "impasses": sum(1 for r in recs if r["outcome"] == "IMPASSE"),
        "conflicts": sum(1 for r in recs if r["outcome"] == "CONFLICT"),
        "coverage": round(n_cov / n, 4),
        "shadow_accuracy": round(n_ok / n_cov, 4) if n_cov else None,
        "silent_error_rate": round(1 - n_ok / n_cov, 4) if n_cov else None,
        "silent_errors_abs": n_cov - n_ok,
        "e2e_accuracy": round(n_ok / n, 4),
        "reuse_rate": (round(sum(1 for f in fires if f >= 1) / n_rules, 4)
                       if n_rules else None),
        "median_fires_per_rule": statistics.median(fires) if fires else 0,
        "dead_rules": sum(1 for f in fires if f == 0),
        "proposal_action_accuracy": (
            round(sum(1 for r in esc if r["proposal_action_correct"]) / len(esc), 4)
            if esc else None),
        "llm_calls": len(esc),
        "edges_proposed": sum(r.get("edges_proposed", 0) for r in recs),
        "edges_accepted": sum(len(r["beats"]) + len(r["loses_to"]) for r in rules),
        "edge_reasons": dict(reasons),
        "rules_with_edges": sum(1 for r in rules if r["beats"] or r["loses_to"]),
        "escalations_with_base_shown": sum(1 for r in esc if r.get("shown_ids")),
        "escalations_on_conflict": sum(1 for r in esc
                                       if r.get("shown_kind") == "conflicto"),
    }


def metric_mismatches(record: dict) -> list[str]:
    """Fields whose recomputed value differs from the published one."""
    got, published = recompute_metrics(record), record["metrics"]
    return [f"{k}: published {published.get(k)!r}, recomputed {v!r}"
            for k, v in got.items() if published.get(k) != v]


def fire_mismatches(record: dict) -> list[str]:
    """Each rule's `fire_count` and `correct_count`, recounted from the cases
    it decided. The two figures every split below rests on."""
    fires: collections.Counter = collections.Counter()
    right: collections.Counter = collections.Counter()
    for r in record["records"]:
        if r["outcome"] == "ACTION":
            fires[r["winner_id"]] += 1
            if r["correct"]:
                right[r["winner_id"]] += 1
    return [f"{rule['rule_id']}: published {rule['fire_count']}/"
            f"{rule['correct_count']}, recounted {fires[rule['rule_id']]}/"
            f"{right[rule['rule_id']]}"
            for rule in record["rules"]
            if (rule["fire_count"], rule["correct_count"])
            != (fires[rule["rule_id"]], right[rule["rule_id"]])]


# ---------------------------------------------------------------------------
# §5.3 — births
# ---------------------------------------------------------------------------

def births(record: dict) -> tuple[dict[str, dict], list[str]]:
    """Each rule's birth escalation, and every way the record breaks §5.3."""
    by_idx = {r["idx"]: r for r in record["records"]}
    shared = collections.Counter(rule["born_at"] for rule in record["rules"])
    out: dict[str, dict] = {}
    problems: list[str] = []
    for rule in record["rules"]:
        rid, idx = rule["rule_id"], rule["born_at"]
        if shared[idx] != 1:
            problems.append(f"{rid}: born_at {idx} is shared by {shared[idx]} rules")
        rec = by_idx.get(idx)
        if rec is None:
            problems.append(f"{rid}: no case at born_at {idx}")
            continue
        if not rec["escalated"]:
            problems.append(f"{rid}: the case at born_at {idx} did not escalate")
        if rec.get("proposal_action_correct") is None:
            problems.append(f"{rid}: its birth carries no proposal_action_correct")
        if rec.get("predicted") != rule["action"]:
            problems.append(f"{rid}: born {rule['action']} from a proposal of "
                            f"{rec.get('predicted')}")
        out[rid] = rec
    return out, problems


def born_right(born: dict[str, dict], rule_id: str) -> bool:
    return bool(born[rule_id]["proposal_action_correct"])


# ---------------------------------------------------------------------------
# U-c — the silent error, split by the birth of the rule that made it
# ---------------------------------------------------------------------------

def split_silent(record: dict, born: dict[str, dict]) -> dict[str, Any]:
    by_wrong = by_right = 0
    for r in record["records"]:
        if r["outcome"] == "ACTION" and not r["correct"]:
            if born_right(born, r["winner_id"]):
                by_right += 1
            else:
                by_wrong += 1
    total = by_wrong + by_right
    return {
        "silent_errors": total,
        "by_rules_born_wrong": by_wrong,
        "by_rules_born_right": by_right,
        "share_born_wrong": by_wrong / total if total else None,
    }


# ---------------------------------------------------------------------------
# U-b — the scope axis alone, against the frontier
# ---------------------------------------------------------------------------

def right_born(record: dict, born: dict[str, dict]) -> dict[str, Any]:
    """The rules whose birth chose the right queue: their reuse and the silent
    error pooled over the cases they decided."""
    s = [rule for rule in record["rules"] if born_right(born, rule["rule_id"])]
    return pooled([{
        "rules": 1,
        "reused": 1 if rule["fire_count"] >= 1 else 0,
        "decided": rule["fire_count"],
        "correct": rule["correct_count"],
    } for rule in s])


def pooled(parts: Iterable[dict]) -> dict[str, Any]:
    """Sum counts and recompute the two rates from the sums."""
    t = {"rules": 0, "reused": 0, "decided": 0, "correct": 0}
    for p in parts:
        for k in t:
            t[k] += p[k]
    t["reuse_rate"] = t["reused"] / t["rules"] if t["rules"] else None
    t["silent_error"] = 1 - t["correct"] / t["decided"] if t["decided"] else None
    return t


def frontier_points(counts_by_k: dict[int, dict]) -> list[tuple[float, float]]:
    """`(reuse_rate, silent_error)` of `keep_k`, dropping a point whose silent
    error is undefined."""
    return [(c["reuse_rate"], c["silent_error"])
            for _, c in sorted(counts_by_k.items())
            if c["reuse_rate"] is not None and c["silent_error"] is not None]


def F(points: list[tuple[float, float]], u: float) -> float:
    """§5.2's frontier at reuse rate `u`."""
    best: dict[float, float] = {}
    for reuse, err in points:
        best[reuse] = min(err, best.get(reuse, err))
    xs = sorted(best)
    if not xs:
        raise ValueError("an empty frontier has no value anywhere")
    if u <= xs[0]:
        return best[xs[0]]
    if u >= xs[-1]:
        return best[xs[-1]]
    for lo, hi in zip(xs, xs[1:]):
        if lo <= u <= hi:
            return best[lo] + (u - lo) / (hi - lo) * (best[hi] - best[lo])
    raise AssertionError("unreachable: u lies between the ends")


def gap(rb: dict, points: list[tuple[float, float]]) -> float | None:
    """`U-b`'s statistic: the right-born silent error minus `F` at their reuse.
    Undefined when those rules decided nothing."""
    if rb["reuse_rate"] is None or rb["silent_error"] is None:
        return None
    return rb["silent_error"] - F(points, rb["reuse_rate"])


# ---------------------------------------------------------------------------
# U-d, U-e and what is recorded beside them
# ---------------------------------------------------------------------------

def escalations_by_truth(record: dict) -> dict[str, int]:
    return dict(collections.Counter(r["truth"] for r in record["records"]
                                    if r["escalated"]))


def class_ledger(record: dict, queue: str) -> dict[str, int]:
    """Counts for one true queue: how often it arrived, escalated, was decided
    by a rule, and was decided rightly. Counts, never rates (§5.6)."""
    recs = [r for r in record["records"] if r["truth"] == queue]
    decided = [r for r in recs if r["outcome"] == "ACTION"]
    return {
        "cases": len(recs),
        "escalated": sum(1 for r in recs if r["escalated"]),
        "decided_by_a_rule": len(decided),
        "decided_rightly": sum(1 for r in decided if r["correct"]),
    }


def conflict_share(record: dict) -> float | None:
    """The share of escalations that were CONFLICT — `U-a`'s reading (§0)."""
    esc = [r for r in record["records"] if r["escalated"]]
    if not esc:
        return None
    return sum(1 for r in esc if r["outcome"] == "CONFLICT") / len(esc)


def fire_distribution(record: dict) -> dict[str, Any]:
    """§5.1: reuse counts rules, not decisions, so the decisions go beside it."""
    fires = sorted((r["fire_count"] for r in record["rules"]), reverse=True)
    total = sum(fires)
    top = fires[:max(1, len(fires) // 10)] if fires else []
    return {
        "median_fires_per_rule": statistics.median(fires) if fires else 0,
        "dead_rules": sum(1 for f in fires if f == 0),
        "top_decile_fire_share": sum(top) / total if total else None,
    }


def median_of(values: Iterable[float | None]) -> float | None:
    """The adjudicating statistic: the median over runs with a defined value."""
    defined = [v for v in values if v is not None]
    return statistics.median(defined) if defined else None
