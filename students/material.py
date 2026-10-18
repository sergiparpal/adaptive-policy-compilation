"""
THE MATERIAL — the proposer's answers, by set, their reach into the test split,
and the one route the truth takes. `PLAN_STUDENTS.md` §1.

**An answer is a queue the proposer named at an escalation, with its ticket.**
On rung 1's record they are read by `ilp/chosen.py`'s `chosen`, called and not
copied: the escalations whose proposal named a queue, 579 of the 632. On
`PLAN_REUSE.md`'s three runs the same function reads every escalation, since
every proposal there parsed and named one.

THE SETS. Each run gives two: `all`, every answer, which the rows read because
the rules were written from every answer (§2.1 of the plan); and `train`, the
answers whose ticket falls in rung 3's train half of split 0, reported beside.
Both are in arrival order, which is the cache's store order.

THE REACH is the number of test cases whose ticket is identical to a training
ticket, which `CLAUDE.md` asks a baseline set against the proposer to declare. A
train half reaches nothing, because rung 3's split groups cases by identity.

THE TRUTH, and only to score. The students never read it: `answers` returns the
proposer's queues and nothing else, and `T-g3` checks them against the records.
`truth` is `ilp.instances.truths`, a module `tests/test_oracle_separation.py`
already allows to see the oracle. This module imports no oracle.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from harness.domain import Case
from ilp import instances as inst
from ilp.chosen import chosen

from . import plan

RUNS = ("rung1",) + tuple(f"reuse{k}" for k in plan.REUSE_RUNS)
KINDS = ("all", "train")


@dataclass(frozen=True)
class AnswerSet:
    run: str                       # rung1, reuse1, reuse2, reuse3
    kind: str                      # all, train
    idx: tuple[int, ...]           # corpus indices, ascending: arrival order
    labels: tuple[str, ...]        # the proposer's queue for each

    @property
    def name(self) -> str:
        return f"{self.run}/{self.kind}"

    def cases(self) -> list[Case]:
        c = corpus()
        return [c[i] for i in self.idx]


@lru_cache(maxsize=None)
def corpus() -> tuple[Case, ...]:
    return inst.corpus()


@lru_cache(maxsize=None)
def split() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Rung 3's split 0, as `ilp/instances.py` builds it: train, test."""
    train, test = inst.splits()
    return tuple(train), tuple(test)


def truth() -> tuple[str, ...]:
    """The truth of every corpus case. To score, and only to score."""
    return inst.truths()


def record_path(run: str):
    return plan.RUNG1 if run == "rung1" else plan.reuse_path(int(run[-1]))


@lru_cache(maxsize=None)
def record(run: str) -> dict[str, Any]:
    return json.loads(record_path(run).read_text())


@lru_cache(maxsize=None)
def answers(run: str) -> dict[int, str]:
    """`{case index: the queue the proposer named}` at the run's escalations."""
    return chosen(record(run)["records"])


@lru_cache(maxsize=None)
def answer_set(run: str, kind: str) -> AnswerSet:
    named = answers(run)
    idx = sorted(named)
    if kind == "train":
        train = set(split()[0])
        idx = [i for i in idx if i in train]
    elif kind != "all":
        raise AssertionError(kind)
    return AnswerSet(run, kind, tuple(idx), tuple(named[i] for i in idx))


def answer_sets() -> list[AnswerSet]:
    return [answer_set(r, k) for r in RUNS for k in KINDS]


def reached(s: AnswerSet) -> tuple[int, ...]:
    """The test cases whose ticket is identical to one of the set's tickets."""
    c = corpus()
    keys = {c[i].key() for i in s.idx}
    return tuple(i for i in split()[1] if c[i].key() in keys)


def counts(run: str) -> dict[str, int]:
    """The material's counts as §1 of the plan declares them, recomputed."""
    named = answers(run)
    t = truth()
    train, test = (set(x) for x in split())
    return {"answers": len(named),
            "right": sum(1 for i, q in named.items() if q == t[i]),
            "train": sum(1 for i in named if i in train),
            "test": sum(1 for i in named if i in test),
            "reach": len(reached(answer_set(run, "all")))}
