"""
THE ESCALATIONS AND THE THREE RULES — `PLAN_ESCALATIONS.md` §2.6 and §3.

**The escalations** are rung 1's cases that escalated and fall in the train half
of split 0, in arrival order. A reviewer labels the ticket whatever the proposer
did with it, so a failed proposal counts like any other.

**The rules choose which of them to label at a budget `k`**, and none reads the
truth:

  random   `k` of them drawn by `random.Random(DRAW_SEED + d)`, `d` in 0 to 4,
           without replacement, sorted;
  arrival  the first `k`, what a reviewer labelling as tickets come and stopping
           at `k` would label;
  crowded  the `k` the most rules of the final base match, the earlier case
           first on a tie.

They read case indices, arrival order and how many rules match each case, and
nothing else. `tests/test_escalations.py` walks this module's syntax tree to say
that it never names the truth.
"""

from __future__ import annotations

import json
import random
from typing import Sequence

from . import plan


def escalations(train: Sequence[int], record_path=plan.RUNG1) -> tuple[int, ...]:
    """The cases of `train` that rung 1's loop escalated, in arrival order."""
    records = json.loads(record_path.read_text())["records"]
    half = set(train)
    return tuple(sorted(r["idx"] for r in records
                        if r["escalated"] and r["idx"] in half))


def random_draw(escs: Sequence[int], k: int, d: int) -> list[int]:
    return sorted(random.Random(plan.DRAW_SEED + d).sample(list(escs), k))


def arrival(escs: Sequence[int], k: int) -> list[int]:
    return list(escs[:k])


def crowded(escs: Sequence[int], k: int, matching: dict[int, int]) -> list[int]:
    """The `k` escalations the most rules match, the earlier first on a tie."""
    ranked = sorted(escs, key=lambda i: (-matching[i], i))
    return sorted(ranked[:k])


def selections(escs: Sequence[int], matching: dict[int, int]) -> dict[str, list[int]]:
    """Every labelled set the stage reads, by name: `random|k|d`,
    `arrival|k`, `crowded|k`, and `all`."""
    out: dict[str, list[int]] = {}
    for k in plan.BUDGETS:
        for d in range(plan.DRAWS):
            out[f"random|{k}|{d}"] = random_draw(escs, k, d)
        out[f"arrival|{k}"] = arrival(escs, k)
        out[f"crowded|{k}"] = crowded(escs, k, matching)
    out["all"] = list(escs)
    return out
