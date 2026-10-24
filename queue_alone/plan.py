"""
The gate and the constants of `PLAN_QUEUE_ALONE.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_QUEUE_ALONE.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `queue_alone/ask.py` calls
it before it constructs a client. No flag skips it. **The free stages get the
gate too**: what it protects is not money but the order of events. Stage A
counts where each level-3 ticket's first match lies and how `PLAN_APPLY.md`'s
answers fall in §5.6's classes, which is exactly what would inform `QA-c`'s and
`QA-e`'s bands (§10 of the plan).

THE CLIENT AND THE INPUTS ARE THE CLOSED THREADS', IMPORTED AND NOT RETYPED (rule
A of the plan). The model, the prompt version, reasoning off and the
temperature come from `manual.plan`, which takes them from `reuse.plan`. The
population is `PLAN_APPLY.md`'s, rebuilt by `apply.population`, and that plan's
records are read where `apply.plan` puts them.

THE PIN. Every request carries `PROVIDER`, OpenRouter's provider routing with
fallbacks off, in the form its documentation gives (read on 2026-10-24, §2.3 of
the plan). `PROVIDER_NAME` is what a response's `provider` field says when
Baidu served it, as `PLAN_APPLY.md`'s records show.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_queue_alone.py` pins every one of them, so that
moving one after a figure exists is visible in a diff. **The lines are
fractions**, and every comparison with them is exact.

THE SEED. §10 fixes `ORDER_SEED = 71`. It becomes one stream per session, from a
string seed. CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from apply import plan as apply_plan
from manual import plan as manual_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_QUEUE_ALONE.md")
OUT = Path("results_queue_alone")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the client, PLAN_MANUAL.md's loop proposer -------------------------------
MODEL = manual_plan.MODEL
PROMPT = manual_plan.PROMPT
REASONING = manual_plan.REASONING  # PLAN_REUSE.md §1's amendment: reasoning off
TEMPERATURE = manual_plan.TEMPERATURE
MAX_TOKENS = 1200                  # the proposer's own
MAX_RETRIES = 2                    # the proposer's own

# --- §2.3: one provider, pinned, with fallbacks off --------------------------------
PROVIDER = {"order": ["baidu"], "allow_fallbacks": False}
PROVIDER_NAME = "Baidu"

# --- §10: the inputs, every one of them read-only -----------------------------------
LEVELS = manual_plan.LEVELS
REPS = manual_plan.REPS
N = manual_plan.N
SEED = manual_plan.SEED

# --- §10: the populations (§0) -------------------------------------------------------
TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}       # an arm's prompts, by level
DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}          # PLAN_APPLY.md's

# --- §10: the sessions -----------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2")
PASSES = 2
SMOKE_PER_ARM_AND_LEVEL = 1
ORDER_SEED = 71

# --- §10: the limits -------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.10)
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value (§0)
MIN_ANCHOR_PROMPTS = 100           # QA-a's prompts, at the least

# --- §0: the lines ---------------------------------------------------------------------
QA_A_MAX_GAP = Fraction(1, 20)     # holds at <= : S − A over the prompts
QA_B_LINE = Fraction(0)            # holds ABOVE : acc_q − acc_t at L3
QA_C_LINE = Fraction(1, 2)         # holds at >= : (acc_q − acc_t) / (1 − acc_t) at L3
QA_D_LINE = Fraction(0)            # holds at >= : (acc_q − acc_i) − (acc_i − acc_t) at L3
QA_E_LINE = Fraction(9, 10)        # holds at >= : acc_q at L3
QA_F_LINE = Fraction(0)            # holds ABOVE : (acc_q − acc_t) − (acc_q⁰ − acc_t⁰) at L3

# --- PLAN_APPLY.md's records, read where that plan puts them ---------------------------

def apply_sample() -> Path:
    return apply_plan.sample_path()


def apply_ask(session: str) -> Path:
    return apply_plan.ask_path(session)


def apply_score() -> Path:
    return apply_plan.score_path()


# --- §8 and §9: the records ----------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_queue_alone/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.10). Ignored by
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
    return random.Random(f"PLAN_QUEUE_ALONE/order/{ORDER_SEED}/{session}")


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
