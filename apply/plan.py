"""
The gate and the constants of `PLAN_APPLY.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_APPLY.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `apply/ask.py` calls it
before it constructs a client. No flag skips it. **The free stages get the gate
too**: what it protects is not money but the order of events. Stage A counts
how often a decision's plurality is the true queue and how often it is the
loop's answer, which is exactly what would inform `X-b`'s and `X-d`'s bands
(§10 of the plan).

THE CLIENT AND THE INPUTS ARE `PLAN_MANUAL.md`'S, IMPORTED AND NOT RETYPED (rule
A of the plan). The model and reasoning off come from `manual.plan`, which takes
them from `reuse.plan`. The loop records are read where `manual.plan.loop_path`
puts them. A second copy of any of them could drift from what produced the
answers this plan asks again, and nothing downstream would say so.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_apply.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact: each statistic of §0 is a ratio of integer
counts. The population sizes are §0's own counts; `X-g3` rebuilds them from the
records and refuses if they differ.

THE SEED. §10 fixes `ORDER_SEED = 67`. It becomes one stream per session, from a
string seed. CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from manual import plan as manual_plan
from reuse import plan as reuse_plan
from screen import plan as screen_plan

PLAN = Path("PLAN_APPLY.md")
OUT = Path("results_apply")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the client, PLAN_MANUAL.md's loop proposer ---------------------------------
MODEL = manual_plan.MODEL
PROMPT = manual_plan.PROMPT
REASONING = manual_plan.REASONING  # PLAN_REUSE.md §1's amendment: reasoning off
TEMPERATURE = manual_plan.TEMPERATURE

# --- §10: the inputs, every one of them read-only -----------------------------------
LEVELS = manual_plan.LEVELS
REPS = manual_plan.REPS
N = manual_plan.N
SEED = manual_plan.SEED


def loop_record(level: int, rep: int) -> Path:
    """One of `PLAN_MANUAL.md`'s twelve loop runs: an input, never an output
    (rule B)."""
    return manual_plan.loop_path(level, rep)


def manual_sample() -> Path:
    """`PLAN_MANUAL.md`'s Stage A: each level's system prompt and its digest."""
    return manual_plan.sample_path()


def manual_score() -> Path:
    """`PLAN_MANUAL.md`'s Stage C: the loop's choice of queue by level, `G-g`."""
    return manual_plan.score_path()


# `PLAN_SCREEN.md`'s ticket-only answers of 2026-10-14, which `X-g` sets beside
# level 0's ticket arm where a ticket is shared.
SCREEN_TICKET_ONLY = screen_plan.ask_path("ticket_only")

# --- §10: the populations (§0) -------------------------------------------------------
DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}          # escalations with a screen
CONFLICT_DECISIONS = {0: 11, 1: 37, 2: 75, 3: 70}
EMPTY_SCREENS = 12                                     # case 0 of every run
TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}       # level 0 on every ticket
SHARED_WITH_SCREEN = 183                               # level-0 prompts PLAN_SCREEN.md asked

# --- §10: the sessions -----------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2")
PASSES = 2
SMOKE_PER_ARM_AND_LEVEL = 1
ORDER_SEED = 67

# --- §10: the limits -------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.12)
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value (§0)
MIN_PULL_POPULATION = 100          # X-d's decisions with t1 != p

# --- §0: the lines ---------------------------------------------------------------------
X_A_MAX_GAP = Fraction(1, 20)      # holds at <= : S − A, every level pooled
X_B_LINE = Fraction(0)             # holds ABOVE : acc_t − acc_s at L3
X_C_LINE = Fraction(1, 2)          # holds at >= : (acc_t − acc_s) / (1 − acc_s) at L3
X_D_LINE = Fraction(1, 10)         # holds at >= : the pull at L3
X_E_LINE = Fraction(0)             # holds ABOVE : acc_t − acc_s at L2
X_F_LINE = Fraction(1, 10)         # holds at >= : acc_t − acc_u at L3

# --- §8 and §9: the records ----------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in `results_apply/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.12). Ignored by
    git, and gone once the session's record is written."""
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.partial.jsonl"


def pass_of(session: str) -> int:
    """The pass a session's answers belong to: 0 for the smoke run, whose
    answers enter no row."""
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return SESSIONS.index(session)


def order_rng(session: str) -> random.Random:
    """The order of one session, or the smoke run's draw."""
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return random.Random(f"PLAN_APPLY/order/{ORDER_SEED}/{session}")


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
