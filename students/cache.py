"""
THE CACHE — `harness/cache_baseline.py`'s retrieval, over a store of answers.
`PLAN_STUDENTS.md` §3.3.

The frozen file calls the cache *the null hypothesis of the whole project*, and
it caches the truth *as if the LLM had given it*. Here it holds what the LLM
gave. Its distance is the frozen `_dist`: the number of attributes on which two
tickets differ. Its tie-break is the frozen loop's: the first stored ticket at
the smallest distance wins, and a stored ticket at distance zero ends the scan.

**This is the retrieval, not the protocol.** The online cache stores only what
it escalates and abstains beyond a distance. The student here has a fixed store,
the training tickets in arrival order, and no maximum distance: it always
answers. `online` is the protocol, kept here so that `students/gates.py` can show
that the same distance and tie-break, run through it with the truth, give
`results/frontier.json`'s three cache rows.

Over the space the student is read through masks: for each stored ticket, the
points at each distance from it, from the per-attribute masks of
`rung2.engine2.Space`. A point goes to the first stored ticket, in store order,
at the smallest distance — the scan's answer, for every point at once.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from harness.domain import ATTRIBUTES, Case


def distance(a: Case, b: Case) -> int:
    """The frozen `_dist`, read rather than imported: the file is frozen and
    its helper is private. `students/gates.py` holds the two equal."""
    return sum(1 for at in ATTRIBUTES if getattr(a, at) != getattr(b, at))


@dataclass
class Cache:
    store: list[tuple[Case, str]]

    def nearest(self, case: Case) -> tuple[str | None, int]:
        best, best_d = None, 10 ** 9
        for prev, act in self.store:
            d = distance(case, prev)
            if d < best_d:
                best, best_d = act, d
                if d == 0:
                    break
        return best, best_d

    def predict(self, case: Case) -> str:
        return self.nearest(case)[0]


def fit(cases: Sequence[Case], labels: Sequence[str]) -> Cache:
    """The store: the training tickets, in the order given, which is arrival
    order. Reads the tickets and their labels, nothing else."""
    return Cache(list(zip(cases, labels)))


def online(corpus: Sequence[Case], labels: Sequence[str], max_dist: int) -> dict[str, Any]:
    """The cache's protocol, with `labels` where the frozen loop calls
    `true_action`: what it would have cached had the LLM given those queues.
    The metrics are the frozen function's, field for field."""
    store: list[tuple[Case, str]] = []
    escalations = hits = correct = 0
    n = len(corpus)
    for case, truth in zip(corpus, labels):
        best, best_d = Cache(store).nearest(case)
        if best is not None and best_d <= max_dist:
            hits += 1
            if best == truth:
                correct += 1
        else:
            escalations += 1
            store.append((case, truth))
    return {
        "name": f"cache(d<={max_dist})",
        "n_rules": len(store),
        "escalations": escalations,
        "escalation_rate": round(escalations / n, 4),
        "coverage": round(hits / n, 4),
        "silent_error_rate": round(1 - correct / hits, 4) if hits else None,
        "reuse_rate": None,
        "final_decile_escalation_rate": None,
        "dead_rules": 0,
    }


# ---------------------------------------------------------------------------
# Over the space
# ---------------------------------------------------------------------------

def _add_bit(planes: list[int], bit: int) -> list[int]:
    """Add a one-bit mask to a counter held as bit-planes, least significant
    first, for every point at once."""
    out = []
    carry = bit
    for p in planes:
        out.append(p ^ carry)
        carry = p & carry
    out.append(carry)
    return out


def _equal_to(planes: list[int], k: int, full: int) -> int:
    m = full
    for j, p in enumerate(planes):
        m &= p if (k >> j) & 1 else (full & ~p)
    return m


def space_masks(cache: Cache, space) -> dict[str, int]:
    """`{label: points the student answers it on}`, in `Space`'s convention.
    Distance by distance, each stored ticket in store order takes the points not
    yet taken at that distance from it, which is the scan's tie-break."""
    full = space.full
    agree = []
    for case, _label in cache.store:
        planes: list[int] = []
        for a in ATTRIBUTES:
            planes = _add_bit(planes, space.mask[a][getattr(case, a)])
        agree.append(planes[:4])            # a count of at most 8 needs 4 bits
    taken = 0
    out: dict[str, int] = {}
    n_attr = len(ATTRIBUTES)
    for d in range(n_attr + 1):
        for (case, label), planes in zip(cache.store, agree):
            at = _equal_to(planes, n_attr - d, full) & ~taken
            if at:
                out[label] = out.get(label, 0) | at
                taken |= at
        if taken == full:
            break
    return out
