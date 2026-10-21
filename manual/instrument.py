"""
The scorers of `PLAN_MANUAL.md`: what a base decides, over the space and over
the corpus, and the loop's own figures. **Offline**: it reads labels, and the
proposer's path never imports it.

Every scorer here is called, not copied (rule A):

  * the truth over the space is `rung3.order_search_ls.space_truth_masks`, the
    one place rung 3's figures, `students/` and `bound/` take it from; the
    truth over the corpus is read off `PLAN_REUSE.md`'s three Stage B records,
    which label every case, and `G-g1` checks that the three agree;
  * a loop's final base is `edges.rebuild.rebuild`'s engine, the replay of a
    Stage B record that `PLAN_EDGES.md`'s gates proved against the record;
  * a base's decisions over the space are `blind.rows.undefeated_masks` read by
    `reuse.structure.subsumption_on_space`, rung 2's arbiter by masks;
  * the partition statistic is `blind.rows.k_a`, `PLAN_BLIND.md`'s `K-a`.

What is added here is only what no module computes: the per-queue recall; a
first-match reading of a compile answer's list, which §0 reports and never
adjudicates; `K-a` as an exact fraction, which `blind.rows.births_outside`'s
counts give; and the regions of the hidden rules, which `G-g` reads a base on.
The regions are first match over `harness.ceiling_check.HIDDEN_DSL`, the
encoding `harness.ceiling_check` proves equal to the hidden policy.
"""

from __future__ import annotations

import json
import statistics
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import ACTIONS, generate_corpus
from harness.dsl import Condition

from blind import rows as brows
from edges.rebuild import rebuild
from reuse import plan as reuse_plan
from reuse.structure import subsumption_on_space
from rung2.engine2 import PriorityEngine, Rule2, Space
from rung3.order_search_ls import space_truth_masks

RARE = ("ACCOUNT_MANAGER", "T3_ENGINEERING")     # G-b's two queues


# ---------------------------------------------------------------------------
# The two surfaces and their labels
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def space() -> Space:
    return Space()


@lru_cache(maxsize=None)
def space_truth() -> dict[str, int]:
    """`{queue: points of the space whose true queue it is}`."""
    return space_truth_masks(space())


@lru_cache(maxsize=None)
def outside() -> int:
    """The half of the space without the security keyword."""
    return brows.outside_mask(space())


@lru_cache(maxsize=None)
def corpus() -> tuple:
    return tuple(generate_corpus(reuse_plan.N, seed=reuse_plan.SEED))


def reuse_records() -> list[dict]:
    return [json.loads(reuse_plan.run_path(r).read_text()) for r in range(1, reuse_plan.REPS + 1)]


@lru_cache(maxsize=None)
def corpus_truth() -> tuple[str, ...]:
    """The true queue of every corpus case, as `PLAN_REUSE.md`'s first Stage B
    record labels it. `G-g1` checks the other two records say the same."""
    rec = json.loads(reuse_plan.run_path(1).read_text())
    rows = sorted(rec["records"], key=lambda r: r["idx"])
    return tuple(r["truth"] for r in rows)


# ---------------------------------------------------------------------------
# A base, decided
# ---------------------------------------------------------------------------

def over_space(engine: PriorityEngine, mask: int | None = None) -> dict[str, Any]:
    """Rung 2's arbiter over the points of `mask` (the whole space by default):
    the counts of `reuse.structure.arbitration`, and the recall of every queue
    — the share of the points whose true queue it is that the base sends
    there. A CONFLICT or an IMPASSE is a point not decided right."""
    sp = space()
    mask = (1 << sp.n) - 1 if mask is None else mask
    und = {rid: m & mask for rid, m in brows.undefeated_masks(engine).items()}
    action = {r.rule_id: r.action for r in engine.rules}
    truth = {q: m & mask for q, m in space_truth().items()}
    out = subsumption_on_space(und, action, truth, mask.bit_count())
    out["recall"] = {}
    for q in ACTIONS:
        size = truth.get(q, 0).bit_count()
        only_q = {k: (v if k == q else 0) for k, v in truth.items()}
        right = subsumption_on_space(und, action, only_q, mask.bit_count())["correct"]
        out["recall"][q] = {"right": right, "of": size,
                            "share": right / size if size else None}
    return out


def over_corpus(engine: PriorityEngine) -> dict[str, Any]:
    """The same base, case by case over the 2,000 arrivals, read whole: what it
    decides once every rule is in, not what the loop decided as it ran."""
    truth = corpus_truth()
    counts = {"action": 0, "conflict": 0, "impasse": 0}
    right = 0
    by_queue = {q: [0, 0] for q in ACTIONS}
    for case, y in zip(corpus(), truth):
        outcome, winner, _ = engine.decide(case)
        counts[outcome.lower()] += 1
        ok = outcome == "ACTION" and winner.action == y
        right += ok
        by_queue[y][0] += ok
        by_queue[y][1] += 1
    n = len(truth)
    return {"n": n, **counts, "correct": right, "e2e": right / n,
            "silent_error": (counts["action"] - right) / counts["action"]
            if counts["action"] else None,
            "recall": {q: {"right": r, "of": t, "share": r / t if t else None}
                       for q, (r, t) in by_queue.items()}}


def macro_recall(scored: dict[str, Any], queues=RARE) -> Fraction:
    """The mean of the recalls of `queues`, exactly: G-b's statistic."""
    return sum((Fraction(scored["recall"][q]["right"], scored["recall"][q]["of"])
                for q in queues), Fraction(0)) / len(queues)


def exact(scored: dict[str, Any]) -> Fraction:
    """A surface's e2e as the fraction of counts it is."""
    return Fraction(scored["correct"], scored["n"])


def right_mask(engine: PriorityEngine) -> int:
    """The points of the space the base decides right."""
    und = brows.undefeated_masks(engine)
    action = {r.rule_id: r.action for r in engine.rules}
    by_queue: dict[str, int] = {}
    for rid, m in und.items():
        by_queue[action[rid]] = by_queue.get(action[rid], 0) | m
    one = two = 0
    for m in by_queue.values():
        two |= one & m
        one |= m
    only = one & ~two
    right = 0
    for q, m in by_queue.items():
        right |= m & only & space_truth().get(q, 0)
    return right


@lru_cache(maxsize=None)
def hidden_regions() -> dict[str, dict[str, Any]]:
    """Each hidden rule's region under first match: its points of the space as
    a mask, and its corpus cases by index."""
    sp = space()
    taken = 0
    out: dict[str, dict[str, Any]] = {}
    conds = {rid: [Condition(a, o, v) for a, o, v in cs] for rid, cs, _ in HIDDEN_DSL}
    for rid, _, action in HIDDEN_DSL:
        ext = sp.extension(conds[rid])
        out[rid] = {"queue": action, "mask": ext & ~taken, "cases": []}
        taken |= ext
    for i, case in enumerate(corpus()):
        for rid, _, _ in HIDDEN_DSL:
            if all(c.holds(case) for c in conds[rid]):
                out[rid]["cases"].append(i)
                break
    return out


def by_region(engine: PriorityEngine) -> dict[str, dict[str, Any]]:
    """How much of each hidden rule's region the base decides right, on both
    surfaces: where a manual's reading was lost, rule by rule (§5.3)."""
    right = right_mask(engine)
    truth = corpus_truth()
    out = {}
    for rid, reg in hidden_regions().items():
        cases = reg["cases"]
        ok = 0
        for i in cases:
            outcome, winner, _ = engine.decide(corpus()[i])
            ok += outcome == "ACTION" and winner.action == truth[i]
        out[rid] = {"space": [(right & reg["mask"]).bit_count(), reg["mask"].bit_count()],
                    "corpus": [ok, len(cases)]}
    return out


def k_a_exact(rules: list[dict]) -> Fraction:
    """`K-a` as the fraction `blind.rows.births_outside` counts; 1 for a base with
    no rule beyond the keyword, as `blind.rows.k_a` reads it."""
    b = brows.births_outside(rules, space(), outside())
    return Fraction(b["alone_outside"], b["outside"]) if b["outside"] else Fraction(1)


def reproduces(engine: PriorityEngine) -> list[str]:
    """The hidden rules some rule of the base equals, extension and queue."""
    sp = space()
    have = {(engine.ext[r.rule_id], r.action) for r in engine.rules}
    return [rid for rid, cs, action in HIDDEN_DSL
            if (sp.extension([Condition(a, o, v) for a, o, v in cs]), action) in have]


def first_match_over_space(rules: list[Rule2]) -> dict[str, Any]:
    """A compile answer's list read as first match, the reading the manual's
    level 3 states. Reported beside the engine's reading, never adjudicated."""
    sp, truth = space(), space_truth()
    taken = 0
    right = 0
    for r in rules:
        ext = sp.extension(r.conditions)
        mine = ext & ~taken
        right += (mine & truth.get(r.action, 0)).bit_count()
        taken |= ext
    return {"n": sp.n, "decided": taken.bit_count(), "correct": right,
            "e2e": right / sp.n}


# ---------------------------------------------------------------------------
# A loop run, read
# ---------------------------------------------------------------------------

def final_engine(record: dict) -> PriorityEngine:
    """A Stage B run's final base: `edges.rebuild`'s replay of its births and
    the timing of its edges, as recorded."""
    return rebuild(record, list(corpus()), space()).engine


def partition(rules: list[dict]) -> float:
    """`K-a`'s statistic over a base's rules in birth order."""
    return brows.k_a(rules, space(), outside())


def proposals(record: dict) -> dict[str, Any]:
    """The proposer's choice of queue at the escalations, as
    `rung2.shadow2.compute_metrics2` counts `proposal_action_accuracy`: right
    over every escalation, a failed proposal counting as not right. By true
    queue beside it."""
    esc = [r for r in record["records"] if r["escalated"]]
    by_queue: dict[str, list[int]] = {}
    for r in esc:
        by_queue.setdefault(r["truth"], [0, 0])
        by_queue[r["truth"]][0] += bool(r.get("proposal_action_correct"))
        by_queue[r["truth"]][1] += 1
    right = sum(1 for r in esc if r.get("proposal_action_correct"))
    return {"escalations": len(esc), "right": right,
            "rate": right / len(esc) if esc else None,
            "failed": sum(1 for r in esc if r.get("proposal_action_correct") is None),
            "by_queue": {q: {"right": a, "of": b} for q, (a, b) in sorted(by_queue.items())}}
