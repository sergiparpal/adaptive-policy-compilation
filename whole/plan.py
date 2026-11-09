"""
The gate, the constants, the draws and the declared figures of `PLAN_WHOLE.md`,
in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_WHOLE.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries its own
line and raises the minimum. The counting is `reuse/plan.py`'s, called with this
plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `whole/run.py` calls it before it
constructs a client. No flag skips it. **The free stages get the gate too**: what
it protects is the order of events, not money. A record of this plan written
before the signature would be a figure that existed before its band (§11).

THE CLIENT IS `PLAN_PLACEMENT.md`'S, IMPORTED AND NOT RETYPED, PIN INCLUDED (§1,
§2.6, §2.7, rule A): the model, temperature 0, reasoning `{"effort": "high"}`,
16,000 tokens, the retries, the waits a call refused for the rate is waited out
through, and DeepInfra's fp8 endpoint with no fallback. `PROVIDER_NAME` is what
a response's `provider` field is expected to say, and the smoke run holds it to
what it says.

THE ARMS (§0, §5). Both run `PLAN_PLACEMENT.md`'s v1c: `PLAN_CHANNEL.md`'s channel
arm at coverage 1/2 with v1c's placement round. An arm is named by its protocol:
`v1c`, that plan's arm, called and not changed; and `v1d`, v1c with one
paragraph of the first call's user message replaced (`whole/protocol.py`).

THE DRAWS (§5.3) are `PLAN_CHANNEL.md`'s, called through `placement.plan` and so
through `channel.plan`: run `k` of both arms reads stream `r<k>`, and the smoke
run reads `smoke`. No new draw seed is drawn, so the pairing of §0 is that plan's
draws case for case, as `PLAN_PLACEMENT.md`'s was.

THE SEED (§11) was fixed by rule before any draw was computed: the next prime
after `PLAN_PLACEMENT.md`'s 103. `ORDER_SEED` draws one thing, which arm runs
first, from `ARMS`, so the order of `ARMS` is pinned.

THE LABELS THE TRIGGER READS are `PLAN_REUSE.md`'s first Stage B record's, as
`PLAN_CHANNEL.md`'s and `PLAN_PLACEMENT.md`'s triggers read them (rule B):
handed in, never the oracle's.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_whole.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact. Each row's side is in `SIDES`: `WR-a`,
`WR-b` and `WR-f` hold at or above their lines, `WR-c` and `WR-d` at or below,
and `WR-e` strictly below.

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as §0
numbers them. `WR-g2` and `WR-g3` recompute figures 1 to 5 and refuse if one
departs; Stage A recomputes all five and records whether each came back.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from placement import plan as pl_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_WHOLE.md")
OUT = Path("results_whole")
MIN_SIGNATURES = 1                 # §0's line

# --- §11: the client, PLAN_PLACEMENT.md's, pin included ----------------------------------
MODEL = pl_plan.MODEL
PROMPT = pl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = pl_plan.TEMPERATURE
REASONING = pl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = pl_plan.MAX_TOKENS
MAX_RETRIES = pl_plan.MAX_RETRIES
CALL_RETRY_WAIT = pl_plan.CALL_RETRY_WAIT
RATE_LIMITED = pl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = pl_plan.RATE_LIMIT_WAIT
PROVIDER = pl_plan.PROVIDER        # {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
PROVIDER_NAME = pl_plan.PROVIDER_NAME

# --- §11: the protocol --------------------------------------------------------------------
PROTOCOLS = ("v1c", "v1d")
LEVEL = pl_plan.LEVEL              # 3
SYSTEM_PROMPT_SHA16 = pl_plan.SYSTEM_PROMPT_SHA16
WHOLE_BASE_SHA16 = "1e054d7554c5c4f4"     # §2.1's T1, as §5.2 gives it
BLIND_BASE_SHA16 = "8de0ebf50ce9a54b"     # v2b's, which v1d replaces

# --- §11: the arms and the causes (§5) ------------------------------------------------------
IMPASSE, CONFLICT, ERROR = pl_plan.IMPASSE, pl_plan.CONFLICT, pl_plan.ERROR
CAUSES = pl_plan.CAUSES
ARMS = PROTOCOLS                   # an arm is named by its protocol; ORDER_SEED picks from it
COVERAGE = pl_plan.COVERAGE        # 1/2, PLAN_CHANNEL.md's channel arm's

# --- §11: the runs ---------------------------------------------------------------------------
REPS = 3
N = pl_plan.N                      # 2,000
SEED = pl_plan.SEED                # 17
SMOKE_N = 30
SMOKE_ARM = "v1d"
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.4)

# --- §11: the seed -----------------------------------------------------------------------------
ORDER_SEED = 107

# --- §0: the lines ---------------------------------------------------------------------------
WR_A_LINE = Fraction(3, 4)         # holds at >= : median whole(r), v1d
WR_B_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, v1d
WR_C_LINE = Fraction(3, 2)         # holds at <= : median refused(r), v1d, over v1c's
WR_D_LINE = Fraction(1, 40)        # holds at <= : median space(B), v1c, less v1d's
WR_E_LINE = Fraction(9, 10)        # holds at <  : median recall of ONCALL_ESCALATION, v1c
WR_F_LINE = Fraction(1, 4)         # holds at >= : median over k of v1d r k's recall less v1c r k's

LINES = {"WR-a": WR_A_LINE, "WR-b": WR_B_LINE, "WR-c": WR_C_LINE, "WR-d": WR_D_LINE,
         "WR-e": WR_E_LINE, "WR-f": WR_F_LINE}
SIDES = {"WR-a": ">=", "WR-b": ">=", "WR-c": "<=", "WR-d": "<=", "WR-e": "<", "WR-f": ">="}

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
DECLARED = {
    # 1. whole(r) on PLAN_PLACEMENT.md's runs: [held, of the right-queue first-call drafts].
    "whole": {"v1c_r1": [35, 92], "v1c_r2": [19, 64], "v1c_r3": [35, 85],
              "v1b_r1": [38, 79], "v1b_r2": [39, 82], "v1b_r3": [27, 73]},
    "whole_median_v1c": "35/92",
    # 2. The lists v1c would have sent a draft of the governing rule's region whole, on
    #    v1c's three bases rebuilt before each recorded escalation, beside the lists sent.
    "lists": {"v1c_r1": {"escalations": 98, "whole_median": "9", "sent_median": "5",
                         "whole_max": 35},
              "v1c_r2": {"escalations": 68, "whole_median": "11/2", "sent_median": "4",
                         "whole_max": 23},
              "v1c_r3": {"escalations": 87, "whole_median": "6", "sent_median": "5",
                         "whole_max": 43}},
    #    At the rarest queue's escalations: [case, governing rule, whole list, list sent].
    "lists_rare": {"v1c_r1": [[257, "H05", 14, 14], [1432, "H04", 29, 7],
                              [1951, "H04", 17, 6]],
                   "v1c_r2": [[954, "H04", 20, 19], [1951, "H04", 19, 4]],
                   "v1c_r3": [[710, "H05", 20, 3], [1432, "H04", 26, 4],
                              [1951, "H04", 30, 29]]},
    # 3. The transcriber's recall of ONCALL_ESCALATION over the space, under v1c and each
    #    of PLAN_CHANNEL.md's draws (PLAN_PLACEMENT.md's Stage A).
    "transcriber_oncall": {"r1": "1", "r2": "2/3", "r3": "1"},
    # 4. The schedule.
    "schedule": [["v1c", 1], ["v1d", 1], ["v1c", 2], ["v1d", 2], ["v1c", 3], ["v1d", 3]],
    # 5. Off the text's 29 regions alone: the lower rules that contain each listed rule,
    #    and those it crosses. For H04 and H05: [contained by, crosses, crosses of
    #    another queue].
    "text_relations": {"lower_containing_pairs": 61, "lower_crossing_pairs": 233,
                       "rules_inside_a_lower_rule": 28, "rules_holding_a_lower_rule": 0,
                       "rules_crossing_another_queue": 26,
                       "rare": {"H04": [4, 12, 12], "H05": [5, 12, 12]}},
}


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_REASONED_LOOP.md`'s one reasoning setting and
    one budget, as `PLAN_PLACEMENT.md` sends them."""
    return pl_plan.settings()


def schedule() -> list[tuple[str, int]]:
    """§2.3: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_WHOLE/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§5.3): PLAN_CHANNEL.md's, called -----------------------------------------------

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
    run's when `rep` is None."""
    _arm(arm)
    return "smoke" if rep is None else f"r{rep}"


def channel_of(arm: str, rep: int | None) -> dict:
    """What a record says of its channel (rule C): the coverage, and the draws'
    seed string and digest."""
    name = stream(arm, rep)
    return {"channel_coverage": str(COVERAGE), "draws_seed": draw_seed(name),
            "draws_sha16": draws_digest(name), "draws_n": N}


# --- the labels the trigger reads (rule B) ----------------------------------------------------

def labels_path() -> Path:
    return pl_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_CHANNEL.md`'s trigger reads them."""
    return pl_plan.labels()


# --- §8 to §10: the records ----------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_whole/`.

def _check(arm: str, rep: int) -> None:
    _arm(arm)
    if rep not in range(1, REPS + 1):
        raise ValueError(f"no run {rep!r}: 1 to {REPS}")


def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def smoke_path() -> Path:
    return OUT / "loop_smoke.json"


def run_path(arm: str, rep: int) -> Path:
    _check(arm, rep)
    return OUT / f"loop_{arm}_r{rep}.json"


def tag(arm: str | None, rep: int | None) -> str:
    """A run's name: `smoke`, or the arm and the repetition."""
    if arm is None:
        return "smoke"
    _check(arm, rep)
    return f"{arm}_r{rep}"


def partial_path(name: str) -> Path:
    """Where a run appends its answers as they arrive (§5.4). Ignored by git,
    and gone once its record is written."""
    return OUT / f"loop_{name}.partial.jsonl"


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
