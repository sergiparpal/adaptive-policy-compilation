"""
THE EVALUATION PATH — specificity arbitration scored against a policy's own truth,
on either surface, under either encoding.

--------------------------------------------------------------------------
WHY THIS IS A SEPARATE MODULE
--------------------------------------------------------------------------
§7 of `PLAN_SENSITIVITY.md` proposes three files and says the naming is Sergi's to
overrule. This is a fourth, and the reason is a dependency direction: `A-g3` — the
parity check that says this path returns what `harness.ceiling_check` returns —
lives in `generator_check.py`, which gates `sweep.py`. If the scoring lived in the
sweep, the gate would import the thing it gates.

--------------------------------------------------------------------------
THE ARITHMETIC, AND WHY IT IS NOT A REIMPLEMENTATION
--------------------------------------------------------------------------
`RuleEngine.decide` takes the matching rules, keeps those with the most
conditions, and returns their common action or CONFLICT. Done per case that is
29 matches per case per policy; done on bitmasks it is a handful of big-integer
operations for the whole surface, because the rules that match a case are exactly
the extensions containing that case.

For each specificity level `s`, with `M_s` the union of the extensions of the
rules at that level and `A_{s,a}` the union of those whose action is `a`:

    T_s          = M_s minus every M_t with t > s        cases whose top level is s
    agree_{s,a}  = T_s & A_{s,a} & ~(union of A_{s,b}, b != a)
    conflict_s   = T_s minus every agree_{s,a}

A case in `agree_{s,a}` has all its finalists carrying `a`, which is exactly when
`decide` returns ACTION with that action; the age tie-break only chooses between
finalists that already agree, so it cannot move the action. **`A-g3` checks this
against the frozen engine rather than arguing it**, on the one policy whose
figures are published: 0.5875 / 505 / 0.2140.

--------------------------------------------------------------------------
TWO ENCODINGS, AS §1 REQUIRES AT EVERY POINT
--------------------------------------------------------------------------
`published` counts conditions the way the DSL forces them, so the catch-all —
`severity gte 1`, true over the whole domain — arrives with specificity 1 and ties
with every one-condition rule. `corrected` gives it the rank the policy actually
gives it, 0, which is `harness/default_rule_control.py`'s control applied across
the family; `A-e` is the difference between the two curves.

The corrected ranking is oracle-free, and this module reuses that module's own
`is_vacuous` rather than special-casing the catch-all, so a synthetic rule that
happened to be vacuous would be caught by the same rule. `A-g4` asserts that none
is.

--------------------------------------------------------------------------
TWO SURFACES
--------------------------------------------------------------------------
`rung2.engine2.Space` is the exhaustive one, 134,400 cases each counted once.
`CorpusUniverse` is the same interface over the 2,000 draws of seed 17, **one bit
per draw** rather than per distinct case — the corpus is a distribution and its
duplicates are part of it. Everything below is written against the interface, so
neither surface gets a code path of its own.
"""

from __future__ import annotations

from dataclasses import dataclass

from harness.default_rule_control import is_vacuous
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, generate_corpus
from harness.dsl import Condition

N_CORPUS, CORPUS_SEED = 2000, 17


class CorpusUniverse:
    """`Space`'s interface over the 2,000 corpus draws, duplicates included."""

    def __init__(self, n: int = N_CORPUS, seed: int = CORPUS_SEED) -> None:
        cases = list(generate_corpus(n, seed=seed))
        self.n = len(cases)
        self.full = (1 << self.n) - 1
        bits = {a: {v: bytearray(self.n) for v in DOMAINS[a]} for a in ATTRIBUTES}
        for i, c in enumerate(cases):
            for a in ATTRIBUTES:
                bits[a][getattr(c, a)][i] = 1
        self.mask = {a: {v: int("".join(map(str, b)), 2) for v, b in d.items()}
                     for a, d in bits.items()}

    # The two methods below are `Space`'s, and deliberately identical: a second
    # implementation of the operator semantics is a second place to get them
    # wrong. `tests/test_sensitivity_measure.py` pins that the two agree.
    def condition_mask(self, cond: Condition) -> int:
        m = self.mask[cond.attr]
        if cond.op == "eq":
            return m.get(cond.value, 0)
        if cond.op == "neq":
            return self.full & ~m.get(cond.value, 0)
        if cond.op == "in":
            out = 0
            for v in cond.value:
                out |= m.get(v, 0)
            return out
        if cond.op in ("lte", "gte"):
            out = 0
            for v in DOMAINS[cond.attr]:
                if (v <= cond.value) if cond.op == "lte" else (v >= cond.value):
                    out |= m[v]
            return out
        raise AssertionError(cond.op)

    def extension(self, conditions) -> int:
        acc = self.full
        for c in conditions:
            acc &= self.condition_mask(c)
            if acc == 0:
                break
        return acc


PUBLISHED = "published"
CORRECTED = "corrected"
ENCODINGS = (PUBLISHED, CORRECTED)


def specificities(policy, encoding: str) -> list[int]:
    """Conditions counted as the engine counts them, or as the policy means them.

    `corrected` counts only the conditions that constrain — vacuity read off
    `DOMAINS` and the rule alone, no oracle — which for these policies means the
    catch-all drops from 1 to 0 and nothing else moves."""
    if encoding == PUBLISHED:
        return [r.n_conditions for r in policy.rules]
    if encoding == CORRECTED:
        return [sum(1 for c in r.conditions if not is_vacuous(c))
                for r in policy.rules]
    raise AssertionError(encoding)


@dataclass(frozen=True)
class Verdict:
    """What specificity arbitration decides over a whole surface."""

    action: dict[str, int]          # per action, the cases it is returned on
    conflict: int                   # finalists disagreed
    impasse: int                    # nothing matched


def verdict(policy, ext: list[int], spec: list[int], full: int) -> Verdict:
    levels = sorted({s for s in spec}, reverse=True)
    covered_above = 0
    out_action = {a: 0 for a in ACTIONS}
    out_conflict = 0
    matched_any = 0
    for s in levels:
        by_action: dict[str, int] = {}
        level_mask = 0
        for rule, e, rs in zip(policy.rules, ext, spec):
            if rs == s:
                by_action[rule.action] = by_action.get(rule.action, 0) | e
                level_mask |= e
        matched_any |= level_mask
        top = level_mask & ~covered_above
        covered_above |= level_mask
        if not top:
            continue
        others = {a: 0 for a in by_action}
        for a in by_action:
            for b, m in by_action.items():
                if b != a:
                    others[a] |= m
        agreed = 0
        for a, m in by_action.items():
            only = top & m & ~others[a]
            if only:
                out_action[a] |= only
                agreed |= only
        out_conflict |= top & ~agreed
    return Verdict(action={a: m for a, m in out_action.items() if m},
                   conflict=out_conflict, impasse=full & ~matched_any)


def score(v: Verdict, truth: dict[str, int], n: int) -> dict:
    """Coverage, silent error and e2e, counted the way `harness.ceiling_check`
    counts them, so the two are comparable digit for digit."""
    correct = sum((m & truth.get(a, 0)).bit_count() for a, m in v.action.items())
    acted = sum(m.bit_count() for m in v.action.values())
    conflict = v.conflict.bit_count()
    impasse = v.impasse.bit_count()
    return {
        "n": n,
        "action": acted,
        "conflict": conflict,
        "impasse": impasse,
        "correct": correct,
        "coverage": acted / n,
        "accuracy_end_to_end": correct / n,
        "silent_errors_abs": acted - correct,
        "silent_error_rate": (1 - correct / acted) if acted else 0.0,
    }


def required_inequalities(policy, ext: list[int]) -> dict:
    """`A-d`'s structural quantity, and no engine takes part.

    For every ordered pair `(i, j)` with `i` in an earlier layer than `j`, whose
    extensions overlap and whose actions differ, specificity can only get the pair
    right if `count(i) > count(j)`. Collect those requirements and count the
    violations. **Zero violations means some monotone function of specificity
    could execute the policy; one or more means none can** — it is
    `results/FINDINGS.md`'s impossibility proof turned into a counter."""
    from .generator import POSITION_LAYER

    required = violated = 0
    for i in range(len(policy.rules)):
        for j in range(i + 1, len(policy.rules)):
            if POSITION_LAYER[i] == POSITION_LAYER[j]:
                continue                       # same layer: not a layer relation
            if not (ext[i] & ext[j]):
                continue                       # cannot compete
            if policy.rules[i].action == policy.rules[j].action:
                continue                       # it does not matter who wins
            required += 1
            if policy.rules[i].n_conditions <= policy.rules[j].n_conditions:
                violated += 1
    return {"required": required, "violated": violated,
            "any_violation": violated > 0}
