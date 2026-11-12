"""
The loop of `PLAN_CORRECTIONS.md` §5: `PLAN_PLACEMENT.md`'s, called, with the
escalation chosen by arm. **On the proposer's path**, and the one module where
the truth is handed to the proposer, on purpose and by one route (§4).

WHAT IS `PLAN_PLACEMENT.md`'S, CALLED AND NOT EDITED. The loop is
`placement.loop.run_loop`, its trigger `channel.loop.escalates`, its escalation
`placement.protocol.propose_v1c`, and its record `reasoned_loop.loop.record_of`.
None of them hands the proposer a label, and `tests/test_placement.py` and
`tests/test_channel.py` keep them so.

WHAT IS THIS PLAN'S. `run_loop` passes `placement.loop.run_loop` an escalation
chosen by arm:

  * arm `n`: `propose_v1c` itself. The proposer is handed the ticket, and for the
    placement round the draft and the rules listed, as in every channel run.
  * arm `l`: `propose_v1c`, wrapped. At an escalation caused by a reported error,
    the wrapper writes that case's label into the proposer's `reports` before the
    first call, and `corrections/protocol.py` puts it in the first user message.
    At an impasse or a conflict it writes nothing.

The label is `labels[idx][0]`: the corpus label `PLAN_REUSE.md`'s first Stage B
record holds for that case, which is also what the trigger compared the
engine's decision with. No other case's label is written, and none is written
in arm `n`.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Sequence

from harness.domain import Case

from placement import loop as pl_loop
from placement import protocol as pl_protocol
from rung2.engine2 import PriorityEngine

from . import plan

record_of = pl_loop.record_of
Result = pl_loop.Result


def propose_for(arm: str, labels: Sequence[tuple[str, str]]) -> Callable[..., dict[str, Any]]:
    """The escalation of an arm: `propose_v1c`, and in arm `l` the same with the
    reported case's label handed to the proposer first."""
    plan.stream(arm, None)                     # refuses an arm the plan does not have
    if arm != plan.LABELLED:
        return pl_protocol.propose_v1c

    def propose_reported(engine: PriorityEngine, case: Case, idx: int, cause: str,
                         proposer, channels: list[str],
                         clock=time.monotonic) -> dict[str, Any]:
        if cause == plan.ERROR:
            proposer.reports[idx] = labels[idx][0]
        return pl_protocol.propose_v1c(engine, case, idx, cause, proposer, channels,
                                       clock=clock)

    return propose_reported


def run_loop(corpus: Sequence[Case], labels: Sequence[tuple[str, str]],
             engine: PriorityEngine, proposer, arm: str, draws: Sequence[float], *,
             cap: int = plan.MAX_ESCALATIONS, on_progress=None,
             clock=time.monotonic) -> Result:
    """`placement.loop.run_loop` under the channel at coverage 1/2, with the
    arm's escalation: case by case and in order, hard rule 3."""
    return pl_loop.run_loop(corpus, labels, engine, proposer, plan.COVERAGE, draws,
                            propose=propose_for(arm, labels), cap=cap,
                            on_progress=on_progress, clock=clock)


def reports_handed(proposer) -> dict[str, str]:
    """What the proposer was handed, case by case, for the record: in arm `n`,
    nothing."""
    return {str(idx): q for idx, q in sorted(getattr(proposer, "reports", {}).items())}
