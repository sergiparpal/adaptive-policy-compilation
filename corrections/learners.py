"""
The learners of `PLAN_CORRECTIONS.md` §2.5 and §5.5, trained on the labels arm
`l`'s proposer was handed. **Free, offline, and not on the proposer's path**: it
reads the space's truth to score, as `ilp/` and `students/` always have.

WHAT EACH LEARNER IS HANDED: the labelled tickets of one L run up to a
checkpoint, `(case, queue)` in arrival order, and nothing else. Not the
catalogue, and no other truth. `CLAUDE.md` asks four things of a baseline set
against the proposer, and §0 answers them: which side had the label (both), how
far the examples reach (at most a run's escalations, as points of the space),
and the control on the proposer's own answers, `own_answers`.

  ilp_40, ilp_120  `PLAN_ILP.md`'s inducer at its two beams, on an instance built
                   over the labelled tickets as `ilp/chosen.py` builds one, and
                   scored by first match over the space.
  tree, logistic,  `PLAN_STUDENTS.md`'s three, by `fit(cases, labels)`, scored
  cache            over the space by that plan's masks.
  table            the floor: a labelled ticket decides its own point and
                   nothing else; every other point is undecided.

Each is read as its own record reads it, and a point a learner leaves undecided
is not right, as `space(B)` counts it for the loop's base. A learner that fails
to fit is recorded with its error, and `best(r)` reads the ones that fitted.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Sequence

from harness.ceiling_check import all_cases

from ilp import chosen as ilp_chosen
from ilp import induce as ind
from ilp import instances as inst
from students import rules as st_rules
from students import score as st_score

LEARNERS = ("ilp_40", "ilp_120", "tree", "logistic", "cache")
FLOOR = "table"


@lru_cache(maxsize=1)
def space_instance():
    return inst.instance("space")


@lru_cache(maxsize=1)
def space_cases() -> list:
    return list(all_cases())


def corpus() -> list:
    return list(inst.corpus())


def ilp_right(pairs: Sequence[tuple[int, str]], beam: int) -> int:
    idx = [i for i, _ in pairs]
    ext, truth, n = ilp_chosen.instance_of(idx, dict(pairs))
    got = ind.induce(ext, truth, n, beam=beam)
    return ind.score(got, *space_instance())["correct"]


def student_right(name: str, pairs: Sequence[tuple[int, str]]) -> int:
    cases = corpus()
    fitted = st_score.STUDENTS[name]([cases[i] for i, _ in pairs], [q for _, q in pairs])
    return st_rules.right_over_space(st_score.student_space(name, fitted, space_cases()))


def table_right(pairs: Sequence[tuple[int, str]]) -> int:
    """The points the table decides right: one per distinct labelled ticket,
    since each label is that ticket's truth (`ask.labelled` refuses otherwise)."""
    cases = corpus()
    return len({cases[i].key() for i, _ in pairs})


def trained(pairs: Sequence[tuple[int, str]]) -> dict[str, Any]:
    """Every learner and the table on `pairs`: the points of the space each
    decides right, of 134,400, or the error it failed with."""
    out: dict[str, Any] = {"labels": len(pairs),
                           "distinct_tickets": len({corpus()[i].key() for i, _ in pairs})}
    fits = {"ilp_40": lambda: ilp_right(pairs, 40), "ilp_120": lambda: ilp_right(pairs, 120),
            "tree": lambda: student_right("tree", pairs),
            "logistic": lambda: student_right("logistic", pairs),
            "cache": lambda: student_right("cache", pairs),
            FLOOR: lambda: table_right(pairs)}
    for name, fit in fits.items():
        try:
            out[name] = {"right": fit(), "error": None}
        except Exception as exc:  # noqa: BLE001 — recorded, and left out of best(r)
            out[name] = {"right": None, "error": f"{type(exc).__name__}: {exc}"[:200]}
    return out


def best(scored: dict[str, Any]) -> int | None:
    """`best(r)`'s numerator: the most points any learner that fitted decides
    right. The table is the floor, not a learner."""
    got = [scored[name]["right"] for name in LEARNERS if scored[name]["right"] is not None]
    return max(got) if got else None


def own_answers(record: dict[str, Any], handed: dict[str, str]) -> list[tuple[int, str]]:
    """The control on the proposer's own answers: every escalation of an L run
    whose first call named a queue, with the label where its report carried one
    and the proposer's queue elsewhere, in arrival order."""
    named = ilp_chosen.chosen(record["records"])
    return [(i, handed.get(str(i), q)) for i, q in sorted(named.items())]
