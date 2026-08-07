"""
Material compartido por varias pruebas, construido una sola vez.

El corpus canonico y el espacio exhaustivo salen en casi todos los modulos y
cuestan lo suficiente (~0,6 s el espacio) como para no rehacerlos por clase.
"""

from __future__ import annotations

from functools import cache

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import Case, generate_corpus
from harness.dsl import Condition
from peldano2.engine2 import PriorityEngine, Rule2, Space

# El corpus del experimento. Semilla 17 y n=2000 no son parametros: son parte
# de la especificacion (regla dura 4 de CLAUDE.md).
CORPUS_N = 2000
CORPUS_SEED = 17

# 2*4*4*5*4*21*2*5, el producto de los dominios.
SPACE_SIZE = 134_400


@cache
def corpus() -> tuple[Case, ...]:
    return tuple(generate_corpus(CORPUS_N, seed=CORPUS_SEED))


@cache
def space() -> Space:
    return Space()


def hidden_rule2s() -> list[Rule2]:
    """Las 29 reglas ocultas como Rule2, con born_at = orden de capa."""
    return [
        Rule2(rule_id=rid,
              conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds],
              action=action,
              born_at=i)
        for i, (rid, conds, action) in enumerate(HIDDEN_DSL)
    ]


def subsumption_only_engine() -> PriorityEngine:
    """Motor del peldano 2 SIN ninguna arista declarada: solo el nivel 1."""
    engine = PriorityEngine(space=space())
    for rule in hidden_rule2s():
        engine.add(rule, born_at=rule.born_at, keep_id=True)
    return engine
