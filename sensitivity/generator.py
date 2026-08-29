"""
THE FAMILY — policies built from this manual's own atoms, with its counts and its
actions.

--------------------------------------------------------------------------
WHAT A MEMBER IS, PER §1 AS AMENDED ON 2026-08-29
--------------------------------------------------------------------------
Four steps, in this order, and the order matters:

  1. **Permute the multiset of condition counts** across the fixed layer
     structure — 8 layers of sizes 3-5-4-2-6-3-3-3, 29 positions — and reject
     until ρ lands within `RHO_TOLERANCE` of the target bin centre. ρ is the
     Spearman rank correlation between a rule's **layer index** and its number of
     conditions.
  2. **Pin the catch-all to the last position.** It matches every case, so
     anywhere else it deletes everything below it.
  3. **Synthesise a body for each remaining rule**, walking the order from the
     top: a rule of assigned count `k` draws `k` conditions from the hidden
     policy's own vocabulary — 23 distinct conditions, the catch-all's excluded —
     without replacement and with distinct attributes, and is redrawn until its
     extension contains at least one case no earlier rule has claimed.
  4. **Assign actions by permuting the hidden policy's own action multiset**, so
     that how often two matching rules disagree is not a second thing riding on
     the knob.

**Why bodies are synthesised at all** is the amendment's whole subject, and it is
not a preference. The first construction re-assigned the 29 hidden rules
themselves, and `A-g4` killed it: 0 of 24,888 ρ-accepted permutations had zero
dead rules, the hidden policy itself has three, and mean dead rules ran 5.39 at
ρ = −0.6 to 16.38 at ρ = +0.5 — Spearman(ρ, dead) = 1.0. The curve would have
confounded *alignment helps* with *the policy got smaller*, at correlation 1 with
the knob. Step 3 makes reachability a property of the construction instead.

**Why the vocabulary and not the whole DSL.** Drawing conditions from the manual's
own 23 keeps the atoms and their breadth the ones a person chose; only the
combination is drawn. It is also what keeps the hidden policy inside the family:
its counts, its actions and its bodies are all in what the generator draws from,
so supplying its own permutation reproduces it exactly — which is what `A-g3`
pins.

--------------------------------------------------------------------------
THE ρ GRID, WHICH THE PLAN LEFT TO THE EXECUTOR
--------------------------------------------------------------------------
§5 fixes **13 bins** and §8 fixes `SWEEP_SEED` and `SWEEP_DRAWS`. The bin
**centres** are not in the plan and three signed rows depend on them, so they are
declared here and pinned by a test rather than chosen while looking at a curve.
Four constraints, and the grid below is the widest one meeting all four:

  1. **0.0 must be a centre** — `A-d` is read at the ρ = 0 bin.
  2. **ρ of the hidden policy must be a centre.** `A-a` compares it against *the
     bin containing it*; on a round grid it falls 0.047 from the nearest centre
     against a tolerance of 0.02, i.e. into no bin at all.
  3. **Every centre must be reachable**, measured and not assumed: over 1,000,000
     sampled count-permutations the achievable range is [−0.78, +0.61], and the
     rarest centre kept, +0.5, is hit by 0.017% — about 578,000 trials for 100
     draws, which is seconds.
  4. **No two bins may overlap.** The closest pair is 0.047 apart against a total
     tolerance of 0.04.

**ρ of the hidden policy is −0.1532, not the −0.18 in circulation.** −0.18 is the
same statistic against the **rule** index; §1 defines the **layer** one.
`EXTERNAL_REVIEW.md` §1.5, which published the −0.18, owns it nowhere.

This module measures nothing and writes nothing. `generator_check.py` gates it and
`sweep.py` uses it.
"""

from __future__ import annotations

import itertools
import random
import statistics
from dataclasses import dataclass
from functools import lru_cache

from harness.ceiling_check import HIDDEN_DSL
from harness.dsl import Condition
from rung2.engine2 import Space

# --- the fixed structure, from the hidden policy -----------------------------
LAYER_SIZES = (3, 5, 4, 2, 6, 3, 3, 3)
N_RULES = sum(LAYER_SIZES)
POSITION_LAYER = tuple(l for l, n in enumerate(LAYER_SIZES) for _ in range(n))

CATCHALL_CONDITION = ("severity", "gte", 1)     # `lambda c: True`, as the DSL forces it
CATCHALL_POSITION = N_RULES - 1                 # the last slot of the defaults layer

# --- the grid, declared before any figure of the sweep exists ---------------
RHO_HIDDEN = -0.153206
RHO_TOLERANCE = 0.02
RHO_BINS = (-0.6, -0.5, -0.4, -0.3, -0.2, RHO_HIDDEN, -0.1,
            0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
assert len(RHO_BINS) == 13

# Rejection caps. Their only job is to fail loudly rather than spin: the measured
# worst case is ~578,000 count-permutations for a draw at +0.5, and a body redraw
# has never needed more than a handful.
MAX_ORDER_TRIES = 4_000_000


class DeadEnd(RuntimeError):
    """A position no body in the vocabulary can fill: everything a rule of that
    size could match is already claimed. It is a property of the draw, not a
    failure of the search — `bodies()` is enumerated, not sampled."""


# ---------------------------------------------------------------------------
# The material the family is drawn from
# ---------------------------------------------------------------------------

def _as_condition(triple) -> Condition:
    attr, op, value = triple
    return Condition(attr=attr, op=op, value=list(value) if op == "in" else value)


def _vocabulary() -> tuple[tuple, ...]:
    """The distinct conditions of the hidden policy, the catch-all's excluded.
    Hashable triples; `in` values are tuples so they compare and deduplicate."""
    seen: dict[tuple, None] = {}
    for _rid, conds, _act in HIDDEN_DSL:
        for attr, op, value in conds:
            key = (attr, op, tuple(value) if isinstance(value, list) else value)
            if key != CATCHALL_CONDITION:
                seen.setdefault(key, None)
    return tuple(seen)


VOCABULARY = _vocabulary()
COUNTS = tuple(len(cs) for _r, cs, _a in HIDDEN_DSL)
ACTIONS = tuple(act for _r, _c, act in HIDDEN_DSL)
CATCHALL_COUNT = COUNTS[CATCHALL_POSITION]


# ---------------------------------------------------------------------------
# ρ
# ---------------------------------------------------------------------------

def _ranks(values) -> list[float]:
    """Average ranks — the tie correction Spearman needs here, where both vectors
    are heavily tied: 8 layers over 29 positions, counts in {1, 2, 3}."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(a, b) -> float:
    ra, rb = _ranks(a), _ranks(b)
    ma, mb = statistics.fmean(ra), statistics.fmean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    return num / (da * db)


def rho_of_counts(counts) -> float:
    """ρ for a policy whose position `p` carries `counts[p]` conditions."""
    return spearman(list(POSITION_LAYER), list(counts))


# ---------------------------------------------------------------------------
# A member
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Rule:
    rule_id: str
    conditions: tuple[Condition, ...]
    action: str

    @property
    def n_conditions(self) -> int:
        return len(self.conditions)


@dataclass(frozen=True)
class Policy:
    """The 29 rules in order. Position `p` sits in layer `POSITION_LAYER[p]`, and
    first-match-wins down this list is the policy's semantics — its own truth."""

    rules: tuple[Rule, ...]
    rho: float
    bin_centre: float | None = None
    order_tries: int = 0
    body_tries: int = 0

    @property
    def counts(self) -> tuple[int, ...]:
        return tuple(r.n_conditions for r in self.rules)

    @property
    def actions(self) -> tuple[str, ...]:
        return tuple(r.action for r in self.rules)


def hidden_member() -> Policy:
    """The hidden policy in the family's own shape, for `A-g3`'s parity check.

    Named `hidden_member` and not `hidden_policy` on purpose:
    `tests/test_oracle_separation.py` matches imported NAMES against
    `{hidden_policy, true_action, true_rule_id}`, so a module doing
    `from .generator import hidden_policy` would trip the oracle check while
    importing nothing of the sort."""
    rules = tuple(
        Rule(rule_id=rid,
             conditions=tuple(_as_condition(c) for c in conds),
             action=act)
        for rid, conds, act in HIDDEN_DSL)
    return Policy(rules=rules, rho=rho_of_counts(COUNTS))


# ---------------------------------------------------------------------------
# Extensions, reachability and the policy's own truth
# ---------------------------------------------------------------------------

def extensions(space: Space, policy: Policy) -> list[int]:
    return [space.extension(list(r.conditions)) for r in policy.rules]


def claimed(ext: list[int], full: int) -> list[int]:
    """What each rule actually wins under first-match-wins: its extension minus
    everything the rules above it already took."""
    remaining = full
    out = []
    for e in ext:
        hit = remaining & e
        out.append(hit)
        remaining &= ~hit
    return out


def dead_rules(policy: Policy, ext: list[int], full: int) -> list[str]:
    """`A-g4`: rules that claim nothing. Under step 3 this must be empty, and a
    non-empty answer is a defect in the construction rather than a property of the
    draw — which is what makes it worth gating on."""
    return [policy.rules[i].rule_id
            for i, hit in enumerate(claimed(ext, full)) if hit == 0]


def truth_masks(policy: Policy, ext: list[int], full: int) -> dict[str, int]:
    """The policy's own truth as one bitmask per action: first-match-wins.

    This is the fast path; `A-g1` checks it against the frozen engine's priority
    arbitration rather than trusting it."""
    out: dict[str, int] = {}
    for rule, hit in zip(policy.rules, claimed(ext, full)):
        if hit:
            out[rule.action] = out.get(rule.action, 0) | hit
    return out


# ---------------------------------------------------------------------------
# Drawing a member
# ---------------------------------------------------------------------------

def _draw_counts(rng: random.Random, centre: float, tolerance: float):
    """Step 1 and 2: a permutation of the count multiset with the catch-all's slot
    pinned, whose ρ lands in the bin."""
    rest = [c for i, c in enumerate(COUNTS) if i != CATCHALL_POSITION]
    for tries in range(1, MAX_ORDER_TRIES + 1):
        rng.shuffle(rest)
        counts = rest[:CATCHALL_POSITION] + [CATCHALL_COUNT] + rest[CATCHALL_POSITION:]
        r = rho_of_counts(counts)
        if abs(r - centre) <= tolerance:
            return tuple(counts), r, tries
    raise RuntimeError(
        f"no count permutation within {tolerance} of {centre} in "
        f"{MAX_ORDER_TRIES} tries; the grid claims an unreachable centre")


@lru_cache(maxsize=None)
def bodies(k: int) -> tuple[tuple[tuple, ...], ...]:
    """Every body of `k` conditions: `k` distinct attributes, one condition each,
    drawn from the vocabulary. 23, 217 and 1,083 for k = 1, 2, 3.

    Enumerated rather than sampled. Step 3 says *redrawn until it claims an
    unclaimed case*, and rejection sampling implements that only when the valid
    set is a decent fraction of the whole; deep in a policy it can be a handful of
    the 217, and a retry cap then reports "impossible" for what is merely rare.
    Choosing uniformly among the valid bodies is the same distribution computed
    exactly, and it makes an empty set mean what it says."""
    by_attr: dict[str, list[tuple]] = {}
    for triple in VOCABULARY:
        by_attr.setdefault(triple[0], []).append(triple)
    out = []
    for attrs in itertools.combinations(sorted(by_attr), k):
        for combo in itertools.product(*(by_attr[a] for a in attrs)):
            out.append(combo)
    return tuple(out)


@lru_cache(maxsize=None)
def _body_extensions(k: int, space_id: int) -> tuple[int, ...]:
    """Extensions of every body of size `k`, computed once per space. Keyed by
    `id(space)` because `Space` is not hashable and there is only ever one."""
    space = _SPACES[space_id]
    return tuple(space.extension([_as_condition(t) for t in body])
                 for body in bodies(k))


_SPACES: dict[int, Space] = {}


def _draw_body(rng: random.Random, k: int, space: Space, remaining: int):
    """Step 3: `k` conditions from the vocabulary, distinct attributes, and the
    rule must claim a case no earlier rule has claimed. Uniform over the bodies
    that qualify; an empty set is a real dead end and says so."""
    _SPACES[id(space)] = space
    ext_all = _body_extensions(k, id(space))
    valid = [i for i, e in enumerate(ext_all) if e & remaining]
    if not valid:
        raise DeadEnd(f"no body of {k} conditions claims an unclaimed case "
                      f"({len(ext_all)} were available)")
    i = rng.choice(valid)
    return (tuple(_as_condition(t) for t in bodies(k)[i]), ext_all[i],
            len(valid))


def draw(rng: random.Random, centre: float, space: Space,
         tolerance: float = RHO_TOLERANCE) -> tuple[Policy, list[int]]:
    """One member, and its extensions. Returns both because every caller needs
    them and recomputing them is the expensive part."""
    counts, rho, order_tries = _draw_counts(rng, centre, tolerance)
    actions = list(ACTIONS)
    rng.shuffle(actions)

    rules, ext, body_tries = [], [], 0
    remaining = space.full
    for p in range(N_RULES):
        if p == CATCHALL_POSITION:
            # The catch-all is under step 3's requirement like every other rule:
            # if the 28 above it have covered the space there is nothing left for
            # it to claim, and a policy whose default rule is dead is exactly what
            # `A-g4` refuses. It is a dead end, not a special case.
            if remaining == 0:
                raise DeadEnd("the 28 rules above the catch-all cover the space; "
                              "the default rule would claim nothing")
            conds = (_as_condition(CATCHALL_CONDITION),)
            e = space.full
            tries = 1
        else:
            conds, e, tries = _draw_body(rng, counts[p], space, remaining)
        body_tries += tries          # bodies that qualified at this position
        rules.append(Rule(rule_id=f"S{p + 1:02d}", conditions=conds,
                          action=actions[p]))
        ext.append(e)
        remaining &= ~e

    return Policy(rules=tuple(rules), rho=rho, bin_centre=centre,
                  order_tries=order_tries, body_tries=body_tries), ext
