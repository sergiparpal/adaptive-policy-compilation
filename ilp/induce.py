"""
THE INDUCER — sequential covering, precision-first, over the declared language.

--------------------------------------------------------------------------
WHY THIS METHOD AND NOT THE ONE §1 FIRST DECLARED
--------------------------------------------------------------------------
`PLAN_ILP.md` §1 originally declared the objective *"expressed as clingo
optimisation priorities"*. That encoding was built — it is still here, in
`asp_encoding.py`, so its failure reproduces — and `I-g1` killed it: on the real
316-case training set it fits **205 of 316** in 300 seconds, cap-bound and with
nothing proved, and `I-g1`'s instance is 134,400 cases whose fact base alone is
16,128,000 atoms.

This method passes `I-g1` **as signed**: complete labels over all 134,400 cases,
a **28-rule** list, **1.000000**, in under eight seconds. The hidden policy is 29
rules. §1's amendment of 2026-08-30 records the change and Sergi signed it; the
gate that authorises touching the instrument is the one that failed, which is the
only thing that makes it legitimate.

--------------------------------------------------------------------------
THE METHOD, EXACTLY AS §1 NOW DECLARES IT
--------------------------------------------------------------------------
Build the list one rule at a time. At each step, over the cases **not yet
decided**:

  * consider bodies of at most three conditions with distinct attributes, drawn
    from the 224 of `language.py`;
  * score a body by **precision** on the undecided cases it covers — the share
    belonging to its own majority action — breaking ties by **coverage**;
  * take the best, give it that majority action, and remove what it covers;
  * stop when nothing is left to decide.

**The search over bodies is a beam**, because the space of conjunctions is
839,070 on the real training set. Two beam widths are declared, and `I-g4` reads
every row at both: **a row whose verdict changes between them is not reported as
a verdict.** Sequential covering proves nothing, and pretending otherwise would
be worse than saying so.

--------------------------------------------------------------------------
CONVENTIONS
--------------------------------------------------------------------------
This module never sees a `Case`. It takes bitmasks — one per condition, one per
action — and the bit convention is the caller's, provided it is the same for
both. `I-g3` checks that this is the whole of its input: no hidden rules, no
layer order, no test split, no learned base.

It runs on the standard library. `clingo` is needed only to reproduce the
superseded encoding.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from .language import MAX_CONDITIONS, language

# Declared before any row's figure exists. `I-g4` reads every row at both.
BEAM_WIDTHS = (40, 120)
MAX_RULES = 200            # a stop, not a target; whether it binds is reported


@dataclass
class Induced:
    """An ordered decision list: `(body, action)`, first match wins."""

    rules: list[tuple[tuple[int, ...], str]] = field(default_factory=list)
    beam: int = 0
    hit_the_cap: bool = False
    left_undecided: int = 0
    seconds: float = 0.0

    @property
    def n_rules(self) -> int:
        return len(self.rules)

    @property
    def n_conditions(self) -> int:
        return sum(len(body) for body, _a in self.rules)


def _best_rule(remaining: int, ext: list[int], attr: list[str],
               truth: dict[str, int], full: int, beam: int, max_conditions: int):
    """The highest-precision body over the undecided cases, ties by coverage."""
    best_body = best_action = None
    best_key = (-1.0, -1)
    frontier: list[tuple[tuple[int, ...], int]] = [((), full)]
    for _depth in range(max_conditions):
        scored = []
        for body, mask in frontier:
            start = body[-1] + 1 if body else 0
            for j in range(start, len(ext)):
                if any(attr[j] == attr[b] for b in body):
                    continue
                extended = mask & ext[j]
                if not extended:
                    continue
                covered = extended & remaining
                if not covered:
                    continue
                total = covered.bit_count()
                action = max(truth, key=lambda a: (covered & truth[a]).bit_count())
                good = (covered & truth[action]).bit_count()
                scored.append(((good / total, total), body + (j,), extended,
                               action))
        if not scored:
            break
        scored.sort(key=lambda x: (-x[0][0], -x[0][1]))
        key, body, _mask, action = scored[0]
        if key > best_key:
            best_key, best_body, best_action = key, body, action
        frontier = [(b, m) for _k, b, m, _a in scored[:beam]]
    return best_body, best_action


def induce(ext: list[int], truth: dict[str, int], n: int, beam: int,
           max_conditions: int = MAX_CONDITIONS,
           max_rules: int = MAX_RULES) -> Induced:
    """Sequential covering over labelled cases given as masks.

    `ext[t]` is the set of cases condition `t` holds on; `truth[a]` the set whose
    true action is `a`. **That is the entire input.**"""
    t0 = time.time()
    full = (1 << n) - 1
    attr = [t[0] for t in language()]
    remaining = full
    rules: list[tuple[tuple[int, ...], str]] = []
    while remaining and len(rules) < max_rules:
        body, action = _best_rule(remaining, ext, attr, truth, full, beam,
                                  max_conditions)
        if body is None:
            break
        covered = full
        for j in body:
            covered &= ext[j]
        rules.append((body, action))
        remaining &= ~covered
    return Induced(rules=rules, beam=beam,
                   hit_the_cap=len(rules) == max_rules,
                   left_undecided=remaining.bit_count(),
                   seconds=round(time.time() - t0, 2))


def score(induced: Induced, ext: list[int], truth: dict[str, int],
          n: int) -> dict:
    """First-match-wins over the list, on any set of cases given as masks.

    Training and every surface a row is read on go through this one function, so
    the figures are produced by the same code."""
    full = (1 << n) - 1
    remaining = full
    decided_by_action: dict[str, int] = {}
    for body, action in induced.rules:
        covered = full
        for j in body:
            covered &= ext[j]
        hit = covered & remaining
        if hit:
            decided_by_action[action] = decided_by_action.get(action, 0) | hit
            remaining &= ~hit

    correct = sum((m & truth.get(a, 0)).bit_count()
                  for a, m in decided_by_action.items())
    decided = sum(m.bit_count() for m in decided_by_action.values())
    per_class = {}
    for a, tmask in truth.items():
        total = tmask.bit_count()
        if not total:
            continue
        right = sum((m & tmask).bit_count() for act, m in decided_by_action.items()
                    if act == a)
        per_class[a] = {"n": total, "correct": right, "accuracy": right / total}
    return {
        "n": n,
        "decided": decided,
        "undecided": n - decided,
        "correct": correct,
        "accuracy_end_to_end": correct / n if n else 0.0,
        "per_class": per_class,
    }


def as_dsl(induced: Induced) -> list[dict]:
    """The list in the frozen DSL's payload shape, so the record carries rules
    `validate_rule_payload` would accept."""
    lang = language()
    return [{
        "rule_id": f"L{i + 1:02d}",
        "conditions": [
            {"attr": lang[t][0], "op": lang[t][1],
             "value": list(lang[t][2]) if lang[t][1] == "in" else lang[t][2]}
            for t in body],
        "action": action,
    } for i, (body, action) in enumerate(induced.rules)]
