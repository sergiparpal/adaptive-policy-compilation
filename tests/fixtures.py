"""
Material shared by several tests, built only once.

The canonical corpus and the exhaustive space show up in almost every module and
cost enough (~0.6 s for the space) not to be rebuilt per class.
"""

from __future__ import annotations

from functools import cache

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import Case, generate_corpus
from harness.dsl import Condition
from rung2.engine2 import PriorityEngine, Rule2, Space

# The experiment's corpus. Seed 17 and n=2000 are not parameters: they are part
# of the specification (hard rule 4 of CLAUDE.md).
CORPUS_N = 2000
CORPUS_SEED = 17

# 2*4*4*5*4*21*2*5, the product of the domains.
SPACE_SIZE = 134_400


@cache
def corpus() -> tuple[Case, ...]:
    return tuple(generate_corpus(CORPUS_N, seed=CORPUS_SEED))


@cache
def space() -> Space:
    return Space()


def hidden_rule2s() -> list[Rule2]:
    """The 29 hidden rules as Rule2, with born_at = layer order."""
    return [
        Rule2(rule_id=rid,
              conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds],
              action=action,
              born_at=i)
        for i, (rid, conds, action) in enumerate(HIDDEN_DSL)
    ]


def subsumption_only_engine() -> PriorityEngine:
    """Rung 2 engine WITHOUT any declared edge: level 1 only."""
    engine = PriorityEngine(space=space())
    for rule in hidden_rule2s():
        engine.add(rule, born_at=rule.born_at, keep_id=True)
    return engine
