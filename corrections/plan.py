"""
The gate, the constants, the draws and the declared figures of
`PLAN_CORRECTIONS.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_CORRECTIONS.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries
its own line and raises the minimum. The counting is `reuse/plan.py`'s, called
with this plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `corrections/run.py` and
`corrections/ask.py` call it before they construct a client. No flag skips it.
**The free stages get the gate too**: what it protects is the order of events,
not money (§11).

THE CLIENT IS `PLAN_PLACEMENT.md`'S, IMPORTED AND NOT RETYPED, PIN INCLUDED (§1,
§2.9, §2.10): the model, temperature 0, reasoning `{"effort": "high"}`, 16,000
tokens, the retries, the waits a call refused for the rate is waited out
through, and DeepInfra's fp8 endpoint with no fallback. The at-once asks send
the same request with one change, their budget, `AT_ONCE_MAX_TOKENS` (§2.4).

THE ARMS (§0, §5). Both run `PLAN_PLACEMENT.md`'s v1c at level 1:
`PLAN_CHANNEL.md`'s channel arm at coverage 1/2 with v1c's placement round.
`n` is v1c with level 1's system prompt; `l` is `n` with the report paragraph
at a reported error (`corrections/protocol.py`). "Level 1" is the manual's
level 1, the catalogue, and nothing else here.

THE DRAWS (§5) are `PLAN_CHANNEL.md`'s, called through `placement.plan` and so
through `channel.plan`: run `k` of both arms reads stream `r<k>`, and the smoke
runs read `smoke`. No new draw seed is drawn.

THE SEED (§2.3) was fixed by rule before any draw was computed: the next prime
after `PLAN_WHOLE.md`'s 107. `ORDER_SEED` draws one thing, which arm runs first,
from `ARMS`, so the order of `ARMS` is pinned.

THE LABELS are `PLAN_REUSE.md`'s first Stage B record's, as `PLAN_CHANNEL.md`'s
trigger reads them: handed in, never the oracle's. The trigger reads them, and
in arm `l` a reported ticket's own label reaches its first call (§4).

THE CONSTANTS are §2's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_corrections.py` pins every one of them. **The lines
are fractions**, and every comparison with them is exact. `CR-e` holds strictly
above its line, every other row at or above it.

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as
§0 numbers them. `CR-g2` recomputes them and refuses if one departs; Stage A
records them.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from placement import plan as pl_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_CORRECTIONS.md")
OUT = Path("results_corrections")
MIN_SIGNATURES = 1                 # §0's line

# --- §2.10: the client, PLAN_PLACEMENT.md's, pin included --------------------------------
MODEL = pl_plan.MODEL
PROMPT = pl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = pl_plan.TEMPERATURE
REASONING = pl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = pl_plan.MAX_TOKENS    # 16,000, the loop's
MAX_RETRIES = pl_plan.MAX_RETRIES
CALL_RETRY_WAIT = pl_plan.CALL_RETRY_WAIT
RATE_LIMITED = pl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = pl_plan.RATE_LIMIT_WAIT
PROVIDER = pl_plan.PROVIDER        # {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
PROVIDER_NAME = pl_plan.PROVIDER_NAME

# --- §5: the protocol --------------------------------------------------------------------
LEVEL = 1                          # the manual's level 1: the catalogue
SYSTEM_PROMPT_SHA16 = "fb72980e84c9aa16"     # manual.prompts.loop_system_prompt(1)
COMPILE_PROMPT_SHA16 = "fb6af1748467d1eb"    # manual.prompts.compile_system_prompt(1)
LEVEL3_SYSTEM_PROMPT_SHA16 = pl_plan.SYSTEM_PROMPT_SHA16   # v1c's, which level 1's replaces
REPORT_SHA16 = "89809fb99b3aee4b"            # §2.1's R1, as §5.2 quotes it
AT_ONCE_HEADER_SHA16 = "034afad4aaaee649"    # §2.4's header, as §5.3 quotes it

# --- §5: the arms and the causes ------------------------------------------------------------
IMPASSE, CONFLICT, ERROR = pl_plan.IMPASSE, pl_plan.CONFLICT, pl_plan.ERROR
CAUSES = pl_plan.CAUSES
ARMS = ("n", "l")                  # without the label, with it; ORDER_SEED picks from it
LABELLED = "l"                     # the one arm whose reported tickets carry their label
COVERAGE = pl_plan.COVERAGE        # 1/2, PLAN_CHANNEL.md's channel arm's

# --- §2.3: the runs --------------------------------------------------------------------------
REPS = 3
N = pl_plan.N                      # 2,000
SEED = pl_plan.SEED                # 17
SMOKE_N = 30
SMOKE_ARMS = ("n", "l")            # §2.7: N, then L
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers

# --- §2.3: the seed ----------------------------------------------------------------------------
ORDER_SEED = 109

# --- §2.4: the at-once asks ----------------------------------------------------------------------
CHECKPOINTS = (10, 20, 40, 80, 160, 320)   # labels, where a run reaches them; and all of them
ASKS_PER_CHECKPOINT = 3
PRIOR_ASKS = 5                     # with no label, right after the smoke runs
SMOKE_ASKS = 2                     # one with no label, one on L's smoke labels
WORKERS = 4                        # harness/ask_pool.py, asks only
MAX_REASKS = 2                     # an ask with no valid base is asked again, at most twice
AT_ONCE_MAX_TOKENS = 32000         # twice the loop's: they write a whole base
SESSIONS = ("smoke", "prior", "l_r1", "l_r2", "l_r3")

# --- §0: the lines ---------------------------------------------------------------------------
CR_A_LINE = Fraction(19, 20)       # holds at >= : median followed(r), L
CR_B_LINE = Fraction(1, 10)        # holds at >= : median space(B), L, less N's
CR_C_LINE = Fraction(1, 4)         # holds at >= : median pair(B), L, less N's
CR_D_LINE = Fraction(0)            # holds at >= : median over L's runs of space(A(r)) - space(B)
CR_E_LINE = Fraction(0)            # holds at >  : median over L's runs of space(B) - best(r)
CR_F_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, L

LINES = {"CR-a": CR_A_LINE, "CR-b": CR_B_LINE, "CR-c": CR_C_LINE, "CR-d": CR_D_LINE,
         "CR-e": CR_E_LINE, "CR-f": CR_F_LINE}
SIDES = {"CR-a": ">=", "CR-b": ">=", "CR-c": ">=", "CR-d": ">=", "CR-e": ">", "CR-f": ">="}

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
DECLARED = {
    # 1. In the six level-3 v1c runs, at the escalations caused by a reported error:
    #    [those whose first call named the case's true queue, all of them].
    "first_calls_true_queue": {"placement_v1c_r1": [39, 43], "placement_v1c_r2": [31, 33],
                               "placement_v1c_r3": [52, 53], "whole_v1c_r1": [57, 58],
                               "whole_v1c_r2": [26, 27], "whole_v1c_r3": [40, 41]},
    # 2. The same runs: [escalations, of them caused by a reported error, calls].
    "escalations_reports_calls": {"placement_v1c_r1": [98, 43, 186],
                                  "placement_v1c_r2": [68, 33, 126],
                                  "placement_v1c_r3": [87, 53, 167],
                                  "whole_v1c_r1": [88, 58, 168],
                                  "whole_v1c_r2": [72, 27, 132],
                                  "whole_v1c_r3": [84, 41, 157]},
    # 3. The arrivals that repeat an earlier ticket, of the corpus's 2,000.
    "repeated_arrivals": 257,
    # 4. The schedule.
    "schedule": [["l", 1], ["n", 1], ["l", 2], ["n", 2], ["l", 3], ["n", 3]],
}


def settings() -> dict:
    """What every loop request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_PLACEMENT.md`'s one reasoning setting and one
    budget."""
    return pl_plan.settings()


def at_once_settings() -> dict:
    """The at-once asks' request: the loop's, with their own budget (§2.4)."""
    return {**settings(), "max_tokens": AT_ONCE_MAX_TOKENS}


def schedule() -> list[tuple[str, int]]:
    """§2.3: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_CORRECTIONS/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§5): PLAN_CHANNEL.md's, called -------------------------------------------------

STREAMS = pl_plan.STREAMS          # ("r1", "r2", "r3", "smoke")
draw_seed = pl_plan.draw_seed
draws = pl_plan.draws
draws_digest = pl_plan.draws_digest
reportable = pl_plan.reportable


def _arm(arm: str) -> None:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")


def stream(arm: str, rep: int | None) -> str:
    """The stream a run reads: `r<rep>` for run `rep` of either arm, the smoke
    runs' when `rep` is None."""
    _arm(arm)
    return "smoke" if rep is None else f"r{rep}"


def channel_of(arm: str, rep: int | None) -> dict:
    """What a record says of its channel: the coverage, and the draws' seed
    string and digest."""
    name = stream(arm, rep)
    return {"channel_coverage": str(COVERAGE), "draws_seed": draw_seed(name),
            "draws_sha16": draws_digest(name), "draws_n": N}


# --- the labels (§4) -----------------------------------------------------------------------------

def labels_path() -> Path:
    return pl_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_CHANNEL.md`'s trigger reads them."""
    return pl_plan.labels()


# --- §2.4: the checkpoints -------------------------------------------------------------------------

def checkpoints(n_labels: int) -> list[int]:
    """The checkpoints a run with `n_labels` labels reaches, and all of its
    labels last. A run with no label has none."""
    out = [j for j in CHECKPOINTS if j <= n_labels]
    if n_labels and (not out or out[-1] != n_labels):
        out.append(n_labels)
    return out


# --- §8 to §10: the records ----------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_corrections/`.

def _check(arm: str, rep: int) -> None:
    _arm(arm)
    if rep not in range(1, REPS + 1):
        raise ValueError(f"no run {rep!r}: 1 to {REPS}")


def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def smoke_path(arm: str) -> Path:
    _arm(arm)
    return OUT / f"loop_smoke_{arm}.json"


def run_path(arm: str, rep: int) -> Path:
    _check(arm, rep)
    return OUT / f"loop_{arm}_r{rep}.json"


def tag(arm: str, rep: int | None) -> str:
    """A run's name: `smoke_<arm>`, or the arm and the repetition."""
    if rep is None:
        _arm(arm)
        return f"smoke_{arm}"
    _check(arm, rep)
    return f"{arm}_r{rep}"


def partial_path(name: str) -> Path:
    """Where a run appends its answers as they arrive. Ignored by git, and gone
    once its record is written."""
    return OUT / f"loop_{name}.partial.jsonl"


def session_of(rep: int) -> str:
    """The at-once session of L's run `rep`."""
    _check(LABELLED, rep)
    return f"{LABELLED}_r{rep}"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"atonce_{session}.json"


def ask_partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive. Ignored by git, and
    gone once its record is written."""
    ask_path(session)                          # refuses a session the plan does not have
    return OUT / f"atonce_{session}.partial.jsonl"


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def gate_signature(path: Path = PLAN) -> dict:
    """Every signature line of this plan filled in, and at least one."""
    return reuse_plan.gate_signature(path, minimum=MIN_SIGNATURES)


def refuse_unsigned(what: str, path: Path = PLAN) -> dict:
    """Exit before anything is measured, written or spent while §0 is unsigned."""
    gate = gate_signature(path)
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {what} while {path.name} is unsigned — "
                 f"{gate['found']} signature line(s), {gate['unsigned']} blank.\n"
                 "  A model may draft a band and may not sign one. Nothing was "
                 "written and nothing was spent.\n")
    return gate
