"""
The loop of `PLAN_RANKED.md` §5: `PLAN_CORRECTIONS.md`'s arm L's, called, on the
engine of each arm. **On the proposer's path.** Nothing here reads a label: the
one route by which a reported ticket's own label reaches its first call is
`corrections/loop.py`'s, called and not copied (§4).

WHAT IS `PLAN_CORRECTIONS.md`'S, CALLED AND NOT EDITED. The loop is
`corrections.loop.run_loop` in that plan's arm `l`, in both of this plan's arms:
`placement.loop.run_loop` under the channel at coverage 1/2, with
`placement.protocol.propose_v1c` wrapped so that a reported error hands its
case's label to the proposer. The trigger is `channel.loop.escalates`, and the
record `reasoned_loop.loop.record_of`.

WHAT IS THIS PLAN'S. The engine the loop is handed:

  * arm `l`: `rung2.engine2.PriorityEngine`, as every run before this plan;
  * arm `k`: `ranked.engine.RankedEngine`, which decides as rung 2's does, and
    where rung 2's would return CONFLICT, by the ranking its own votes choose.
    So in arm `k` a case escalates on an impasse or on a reported error, and on
    nothing else.

`ranked_part` is what arm `k`'s record keeps beyond arm `l`'s: the ranking the
engine ended with, its ranking after every birth, and who decided every case.
It reads no truth.
"""

from __future__ import annotations

import time
from typing import Any, Sequence

from harness.domain import Case

from corrections import loop as cr_loop
from rung2.engine2 import PriorityEngine, Space

from . import plan
from .engine import RankedEngine, rankings

record_of = cr_loop.record_of
reports_handed = cr_loop.reports_handed
Result = cr_loop.Result


def engine_for(arm: str, space: Space) -> PriorityEngine:
    """A fresh engine of an arm: rung 2's, or arm K's, logging."""
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    if arm == plan.RANKED:
        return RankedEngine(space=space, keep_log=True)
    return PriorityEngine(space=space)


def run_loop(corpus: Sequence[Case], labels: Sequence[tuple[str, str]],
             engine: PriorityEngine, proposer, arm: str, draws: Sequence[float], *,
             cap: int = plan.MAX_ESCALATIONS, on_progress=None,
             clock=time.monotonic) -> Result:
    """`corrections.loop.run_loop` in that plan's arm `l`, on this arm's engine:
    case by case and in order, hard rule 3."""
    plan.stream(arm, None)
    if (arm == plan.RANKED) != isinstance(engine, RankedEngine):
        raise ValueError(f"arm {arm!r} was handed {type(engine).__name__}")
    return cr_loop.run_loop(corpus, labels, engine, proposer, plan.TEXTS_OF, draws,
                            cap=cap, on_progress=on_progress, clock=clock)


def ranked_part(engine: PriorityEngine) -> dict[str, Any] | None:
    """What arm `k`'s record keeps of its engine; nothing in arm `l`."""
    if not isinstance(engine, RankedEngine):
        return None
    final = engine.final()
    used = sorted({final["index"], *(x["ranking"] for x in engine.ranking_log),
                   *(x["ranking"] for x in engine.case_log if "ranking" in x)})
    return {"vote": plan.VOTE, "tie": plan.TIE, "decides": plan.DECIDES, "final": final,
            "rankings": {str(k): list(rankings()[k]) for k in used},
            "log": list(engine.ranking_log), "cases": list(engine.case_log)}
