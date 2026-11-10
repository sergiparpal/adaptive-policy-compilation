"""
The gate and the constants of `PLAN_HALVES.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_HALVES.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `halves/ask.py` calls it
before it constructs a client. No flag skips it. **The free stages get the gate
too**: what it protects is the order of events, not money. A record of this plan
written before the signature would be a figure that existed before its band.

THE REQUEST IS THE LOOP'S FIRST CALL'S, IMPORTED AND NOT RETYPED (§2.7). The
model, the temperature, the reasoning setting, the budget, the retries, the
waits and the pin come from `placement.plan`, which takes all but the pin from
`reasoned_loop.plan`. The pin is DeepInfra's fp8 endpoint, which
`PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s runs carried (§2.6).

THE TICKETS ARE FIXED HERE (§0, §2.2), and `HV-g3` rebuilds them from the closed
records: the tickets of `PLAN_REASONED_RULE.md`'s arm `w` that a first call of
one of the five loop groups `whole/paragraph.py` reads met, and the tickets of
the rarest queue that arm did not ask. Nothing on the asker's path opens a
record.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_halves.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact.

THE SEED. `ORDER_SEED = 83` becomes one stream per session, from a string seed.
CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from placement import plan as pl_plan
from reasoned_rule import plan as rr_plan
from reuse import plan as reuse_plan
from whole import plan as wh_plan

PLAN = Path("PLAN_HALVES.md")
OUT = Path("results_halves")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §2.7: the request, the loop's first call's --------------------------------------------
MODEL = pl_plan.MODEL
PROMPT = pl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = pl_plan.TEMPERATURE
REASONING = pl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = pl_plan.MAX_TOKENS
MAX_RETRIES = pl_plan.MAX_RETRIES
CALL_RETRY_WAIT = pl_plan.CALL_RETRY_WAIT
RATE_LIMITED = pl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = pl_plan.RATE_LIMIT_WAIT

# --- §2.6: the pin --------------------------------------------------------------------------
PROVIDER = pl_plan.PROVIDER        # DeepInfra's fp8 endpoint, fallbacks off
PROVIDER_NAME = pl_plan.PROVIDER_NAME

# --- the inputs, every one of them read-only ------------------------------------------------
LEVEL = pl_plan.LEVEL              # 3
N = pl_plan.N                      # 2,000
SEED = pl_plan.SEED                # 17

# --- §0: the arms ---------------------------------------------------------------------------
ARMS = ("e", "v", "h", "o")        # the empty base, v2b's paragraph, its two halves crossed

# --- §0, §2.2: the tickets ------------------------------------------------------------------
TICKETS = (
    0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26,
    28, 29, 33, 34, 35, 38, 42, 44, 45, 46, 49, 50, 55, 57, 58, 64, 68, 69, 75,
    77, 78, 80, 86, 91, 92, 96, 102, 103, 105, 106, 107, 111, 120, 123, 131,
    135, 138, 141, 147, 148, 155, 158, 162, 163, 168, 172, 180, 192, 199, 227,
    228, 238, 245, 257, 260, 265, 271, 278, 282, 294, 301, 316, 338, 339, 342,
    346, 367, 369, 388, 401, 402, 448, 456, 467, 476, 511, 530, 564, 566, 567,
    580, 587, 599, 642, 658, 676, 688, 710, 725, 739, 751, 761, 762, 770, 805,
    816, 855, 954, 982, 1063, 1160, 1229, 1234, 1235, 1264, 1318, 1432, 1514,
    1704, 1783, 1802, 1807, 1871, 1951, 1998,
)
N_TICKETS = 136
RULE_ARM_TICKETS = 171             # the tickets PLAN_REASONED_RULE.md's arm w asked
SHARED = 133                       # of them, the ones a reasoning loop's first call met
ONCALL = (257, 710, 954, 982, 1432, 1783, 1951)   # T₇, the rarest queue's seven
ADDED = (954, 982, 1432)           # T₇'s tickets the rule arm did not ask
LOOP_GROUPS = ("reasoned_loop", "channel", "placement", "whole_v1c", "whole_v1d")
HV_A_GROUPS = ("placement", "whole_v1c")   # the DeepInfra loops under v2b's paragraph

# --- §2.3: the sessions ---------------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2", "oncall")
PASSES = ("pass1", "pass2")
SMOKE_PER_ARM = 2
ONCALL_REPEATS = 4
ORDER_SEED = 83

# --- §0: the limits -------------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value
HV_A_MIN_TICKETS = 50
HV_C_MIN_GAP = Fraction(1, 10)     # at or below it, HV-c has no value
HV_F_MIN_TICKETS = 5

# --- §0: the lines --------------------------------------------------------------------------
LINES = {
    "HV-a": Fraction(1, 10),       # holds WITHIN ±: the mean by ticket of v's share less the loops'
    "HV-b": Fraction(1, 5),        # holds at >= : W_e − W_v
    "HV-c": Fraction(0),           # holds ABOVE : W_h − (W_e + W_v)/2
    "HV-d": Fraction(1, 10),       # holds at >= : W_e − W_h
    "HV-e": Fraction(1, 10),       # holds at >= : W_e − W_o
    "HV-f": Fraction(1, 5),        # holds at >= : W_h⁷ − W_v⁷
}
SIDES = {"HV-a": "within", "HV-b": ">=", "HV-c": ">", "HV-d": ">=", "HV-e": ">=",
         "HV-f": ">="}
ROWS = tuple(LINES)


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: the loop's one reasoning setting and one budget."""
    return pl_plan.settings()


# --- the closed records, read where their own plans put them --------------------------------

def rule_arm_ask(session: str) -> Path:
    """`PLAN_REASONED_RULE.md`'s pass records, whose arm `w` is `e`."""
    return rr_plan.ask_path(session)


def paragraph_record() -> Path:
    """`whole/paragraph.py`'s record, which `HV-g2` holds the classes to."""
    return wh_plan.OUT / "paragraph.json"


# --- §7 to §9: the records --------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_halves/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive. Ignored by git, and
    gone once the session's record is written."""
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.partial.jsonl"


def order_rng(session: str) -> random.Random:
    """The order of one session, or the smoke run's draw."""
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return random.Random(f"PLAN_HALVES/order/{ORDER_SEED}/{session}")


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
