"""
THE INSTRUMENT — the audit's label-budget search, on a labelled set of cases.
`PLAN_ESCALATIONS.md` §3.

`rung3/budget_and_balance_ls.run_config` searches the order from a random draw
of the train half. This calls the same functions on a set of cases given to it,
and changes nothing else:

  1. masks over the set with the truth, `rung3.local_search.build_masks`, on the
     `puro` pool;
  2. the record's greedy over the set, `rung3.budget_and_balance.greedy`;
  3. the declared multi-start from it, `rung3.budget_and_balance_ls.search`;
  4. the best order scored by `score_order` on split 0's test half and over
     `space_pools`' `puro` masks.

`load_instance` is the audit's own: corpus, rules, pool, truth and splits. The
truth enters through it and through `space_pools`, two modules
`tests/test_oracle_separation.py` already allows. This module imports no oracle.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Sequence

from rung3.budget_and_balance_ls import (POOL, greedy_from_record,
                                          load_instance, search, subsample)
from rung3.local_search import build_masks, score_order
from rung3.order_search_ls import space_pools

from . import plan

RARE = ("ACCOUNT_MANAGER", "T3_ENGINEERING", "SECURITY_INCIDENT",
        "ONCALL_ESCALATION")


@lru_cache(maxsize=None)
def instance() -> dict[str, Any]:
    return load_instance()


def halves(inst) -> tuple[list[int], list[int]]:
    return inst["splits"][plan.SPLIT]


@lru_cache(maxsize=None)
def space_masks():
    inst = instance()
    return space_pools(inst["ids"], inst["conds"], inst["action"],
                       inst["below"])[POOL]


@lru_cache(maxsize=None)
def test_masks():
    inst = instance()
    _tr, te = halves(inst)
    return build_masks(inst["ids"], inst["matched"], inst["truth"],
                       inst["action"], te)


def matching(inst) -> dict[int, int]:
    """How many of the rules match each corpus case."""
    return {i: len(m) for i, m in enumerate(inst["matched"])}


def labelled_order(inst, labelled: Sequence[int]):
    """The audit's search, labelled with the truth of `labelled`."""
    ids, action, matched = inst["ids"], inst["action"], inst["matched"]
    rules, truth = inst["rules"], inst["truth"]
    sub = sorted(labelled)
    M, W, full = build_masks(ids, matched, truth, action, sub)
    greedy = greedy_from_record(rules, matched, truth, action, sub)
    best, st = search(ids, greedy, M, W, full)
    return best, st


def per_class(inst, order, idxs) -> dict[str, dict[str, int]]:
    """Right decisions on the rare classes, first match wins."""
    rank = {rid: k for k, rid in enumerate(order)}
    truth, action, matched = inst["truth"], inst["action"], inst["matched"]
    out = {c: {"right": 0, "of": 0} for c in RARE}
    for i in idxs:
        if truth[i] not in out:
            continue
        out[truth[i]]["of"] += 1
        m = matched[i]
        if m and action[min(m, key=rank.__getitem__)] == truth[i]:
            out[truth[i]]["right"] += 1
    return out


def read(inst, labelled: Sequence[int]) -> dict[str, Any]:
    """An order labelled at `labelled`, scored on both surfaces."""
    best, st = labelled_order(inst, labelled)
    _tr, te = halves(inst)
    sM, sW, sfull, sn = space_masks()
    test = score_order(best, *test_masks())
    space = score_order(best, sM, sW, sfull)
    return {"labels": len(labelled), "test": test,
            "test_share": round(test / len(te), plan.SPACE_PLACES),
            "space": space, "space_share": round(space / sn, plan.SPACE_PLACES),
            "fit": st["best_score"], "best_from": st["best_from"],
            "per_class": per_class(inst, best, te)}


def record_draw(inst, k: int, d: int) -> list[int]:
    """The audit record's own draw of `k` train cases on split 0: the random
    arrivals, rebuilt only for `J-g1`'s check."""
    tr, _te = halves(inst)
    return subsample(tr, plan.FRACTIONS[k], plan.SPLIT, d)
