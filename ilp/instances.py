"""
THE INSTANCES — the four sets of labelled cases the plan names, built once and
built the same way.

`I-g1`'s instance and the two training sets and the test surfaces all have to be
masks over a set of cases, and getting the bit convention wrong once would be a
silent error rather than a loud one. So there is one builder and everything goes
through it.

--------------------------------------------------------------------------
WHAT EACH ONE IS, AND WHY THERE ARE TWO TRAINING SETS
--------------------------------------------------------------------------
`space`          all 134,400 combinations with complete labels. `I-g1`'s
                 instance, and `I-c`'s surface.
`train_316`      the escalations of `results/llm_run.json` whose case falls in
                 rung 3's corpus train half, seed 17. **`I-a`'s banded set.**
`train_632`      every escalation. **`I-b`'s banded set**, and the one that
                 matches what the proposer saw.
`test`           rung 3's corpus test split 0, 995 cases. Where `I-a` and `I-b`
                 are read.

**Two training sets because neither is clean**, and §1's amendment of 2026-08-30
says which is which: `rung3/order_search.py` declares in its own docstring that
the 577 rules were learned over all 2,000 cases, so training on the 316 hands the
inducer *less* material than the proposer had while matching the order's
handicap; training on the 632 matches the material and advantages the order. `I-a`
is banded on the conservative one and both are reported.

**Nothing here is an oracle leak.** `true_action` labels the examples, which is
what the proposer also received per case, and `I-g3` checks that the inducer's own
input is masks and nothing else.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.domain import generate_corpus
from harness.hidden_policy import true_action
from rung3.order_search import split

from .language import as_condition, language

RUN = Path("results/llm_run.json")
N_CORPUS, CORPUS_SEED, SPLIT_SEED = 2000, 17, 17


@lru_cache(maxsize=None)
def corpus():
    return tuple(generate_corpus(N_CORPUS, seed=CORPUS_SEED))


@lru_cache(maxsize=None)
def truths():
    return tuple(true_action(c) for c in corpus())


@lru_cache(maxsize=None)
def splits():
    """Rung 3's own split, imported rather than reimplemented: grouped by case
    identity and stratified by action, so the comparison figures and these
    instances partition the corpus the same way."""
    return split(list(corpus()), list(truths()), SPLIT_SEED)


@lru_cache(maxsize=None)
def escalated() -> tuple[int, ...]:
    """The cases the engine could not resolve and handed to the proposer."""
    records = json.loads(RUN.read_text())["records"]
    return tuple(sorted(r["idx"] for r in records if r.get("escalated")))


def masks(cases, labels):
    """`(ext, truth, n)`: one mask per condition, one per action, LSB-first.

    The convention is local and consistent — `induce.py` never learns which end
    the bits start at, and never has to."""
    n = len(cases)
    conds = [as_condition(t) for t in language()]
    ext = []
    for cond in conds:
        mask = 0
        for k, case in enumerate(cases):
            if cond.holds(case):
                mask |= 1 << k
        ext.append(mask)
    truth: dict[str, int] = {}
    for k, action in enumerate(labels):
        truth[action] = truth.get(action, 0) | (1 << k)
    return ext, truth, n


@lru_cache(maxsize=None)
def instance(name: str):
    """`(ext, truth, n)` for one of the four named instances."""
    if name == "space":
        cases = list(all_cases())
        return masks(cases, [true_action(c) for c in cases])
    idx = _indices(name)
    return masks([corpus()[i] for i in idx], [truths()[i] for i in idx])


@lru_cache(maxsize=None)
def _indices(name: str) -> tuple[int, ...]:
    train, test = splits()
    if name == "train_316":
        return tuple(sorted(set(escalated()) & set(train)))
    if name == "train_632":
        return escalated()
    if name == "test":
        return tuple(sorted(test))
    if name == "corpus":
        return tuple(range(len(corpus())))
    raise AssertionError(name)


def describe(name: str) -> dict:
    """What an instance is made of, for the record. Class counts included,
    because §1's amendment turns on them: `ONCALL_ESCALATION` never escalated."""
    import collections

    if name == "space":
        cases = list(all_cases())
        labels = [true_action(c) for c in cases]
    else:
        idx = _indices(name)
        labels = [truths()[i] for i in idx]
    return {"name": name, "n": len(labels),
            "classes": len(set(labels)),
            "by_class": dict(collections.Counter(labels).most_common())}
