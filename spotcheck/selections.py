"""
THE DECISIONS AND THE DRAWS — `PLAN_SPOTCHECK.md` §2 and §3.

**The decisions** are rung 1's cases that did not escalate and fall in the train
half of split 0, in arrival order: the cases its engine decided itself. A
reviewer who audits the system checks them whatever was decided.

**The draws are nested.** Draw `d` shuffles the decisions once, with
`random.Random(AUDIT_SEED + d)`, and the audited decisions at a budget `k` are
the first `k` of that shuffle, sorted. A larger audit holds every smaller one,
as a reviewer who keeps auditing would.

**The two arms at `k`, draw `d`:**

  mix    the escalations, every one, with the `k` audited decisions;
  audit  the `k` audited decisions alone.

They read case indices, arrival order and rung 1's `escalated` flag, and
nothing else. `tests/test_spotcheck.py` walks this module's syntax tree to say
that it never names the truth, in a name or in a string.
"""

from __future__ import annotations

import json
import random
from typing import Sequence

from . import plan


def decisions(train: Sequence[int], record_path=plan.RUNG1) -> tuple[int, ...]:
    """The cases of `train` that rung 1's loop did not escalate, in arrival
    order."""
    records = json.loads(record_path.read_text())["records"]
    half = set(train)
    return tuple(sorted(r["idx"] for r in records
                        if not r["escalated"] and r["idx"] in half))


def shuffle(decs: Sequence[int], d: int) -> list[int]:
    """Draw `d`'s one shuffle of the decisions."""
    perm = list(decs)
    random.Random(plan.AUDIT_SEED + d).shuffle(perm)
    return perm


def audited(decs: Sequence[int], k: int, d: int) -> list[int]:
    """The first `k` decisions of draw `d`, sorted."""
    return sorted(shuffle(decs, d)[:k])


def selections(escs: Sequence[int], decs: Sequence[int]) -> dict[str, list[int]]:
    """Every labelled set the stage reads, by name: `mix|k|d` and
    `audit|k|d`."""
    out: dict[str, list[int]] = {}
    for k in plan.BUDGETS:
        for d in range(plan.DRAWS):
            a = audited(decs, k, d)
            out[f"mix|{k}|{d}"] = sorted(set(escs) | set(a))
            out[f"audit|{k}|{d}"] = a
    return out
