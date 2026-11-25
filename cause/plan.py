"""
The gate and the constants of `PLAN_CAUSE.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_CAUSE.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `cause/ask.py` calls it
before it constructs a client. No flag skips it. **The free stages get the gate
too**: what it protects is the order of events, not money. A record of this plan
written before the signature would be a figure that existed before its band.

THE REQUEST IS `PLAN_HALVES.md`'S, IMPORTED AND NOT RETYPED (§2.7), which is the
loop's first call's. `halves.plan` takes the model, the temperature, the
reasoning setting, the budget, the retries, the waits and the pin from
`placement.plan`, which takes all but the pin from `reasoned_loop.plan`. The pin
is DeepInfra's fp8 endpoint (§2.6).

THE TICKETS ARE `PLAN_HALVES.md`'S (§0, §2.2), imported from `halves.plan`, and
`CA-g3` holds them to that plan's Stage A record. Nothing on the asker's path
opens a record.

§0'S VALIDITY IS HERE, ONCE. An answer is valid when the call came back, after
its retries, with a payload that parses, from the pinned provider. An empty
object parses: it is valid, and Stage C classes it *no rule*. The asker's flag
and the scorer both call `valid`, so they cannot part as `PLAN_HALVES.md`'s did
(that plan's lesson, §5).

THE CONSTANTS are §2's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_cause.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact.

THE SEED. `ORDER_SEED = 89` becomes one stream per session, from a string seed.
CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from halves import plan as hplan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_CAUSE.md")
OUT = Path("results_cause")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §2.7: the request, PLAN_HALVES.md's, which is the loop's first call's -----------------
MODEL = hplan.MODEL
PROMPT = hplan.PROMPT              # v1, the system prompt's base
TEMPERATURE = hplan.TEMPERATURE
REASONING = hplan.REASONING        # {"effort": "high"}, on every call
MAX_TOKENS = hplan.MAX_TOKENS
MAX_RETRIES = hplan.MAX_RETRIES
CALL_RETRY_WAIT = hplan.CALL_RETRY_WAIT
RATE_LIMITED = hplan.RATE_LIMITED
RATE_LIMIT_WAIT = hplan.RATE_LIMIT_WAIT

# --- §2.6: the pin --------------------------------------------------------------------------
PROVIDER = hplan.PROVIDER          # DeepInfra's fp8 endpoint, fallbacks off
PROVIDER_NAME = hplan.PROVIDER_NAME

# --- the inputs, every one of them read-only ------------------------------------------------
LEVEL = hplan.LEVEL                # 3
N = hplan.N                        # 2,000
SEED = hplan.SEED                  # 17

# --- §0: the arms ---------------------------------------------------------------------------
ARMS = ("e", "v", "i", "r")        # the empty base, v2b's paragraph, and v2b's with each notice

# --- §0, §2.2: the tickets, PLAN_HALVES.md's ------------------------------------------------
TICKETS = hplan.TICKETS
N_TICKETS = 136
ONCALL = hplan.ONCALL              # T₇, the rarest queue's seven
LOOP_GROUPS = hplan.LOOP_GROUPS    # the reasoning loops whose causes §0's figures count
DEEPINFRA_GROUPS = ("placement", "whole_v1c", "whole_v1d")   # the twelve DeepInfra runs

# --- §2.3: the sessions ---------------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2", "oncall")
PASSES = ("pass1", "pass2")
SMOKE_PER_ARM = 2
ONCALL_REPEATS = 4
ORDER_SEED = 89

# --- §0: the limits -------------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value
CA_A_MIN_TICKETS = 50
CA_C_MIN_GAP = Fraction(1, 10)     # at or below it, CA-c has no value
CA_E_MIN_TICKETS = 5
CA_F_MIN_B = Fraction(1, 5)        # B_v at or below it, CA-f has no value

# --- §0: the lines --------------------------------------------------------------------------
LINES = {
    "CA-a": Fraction(1, 10),       # holds WITHIN ±: the mean by ticket of today's v less PLAN_HALVES.md's
    "CA-b": Fraction(1, 5),        # holds at >= : W_e − W_v
    "CA-c": Fraction(0),           # holds at >= : W_i − (W_e + W_v)/2
    "CA-d": Fraction(1, 10),       # holds at >= : W_i − W_r
    "CA-e": Fraction(1, 5),        # holds at >= : W_r⁷ − W_v⁷
    "CA-f": Fraction(1, 5),        # holds at >= : B_v − B_i
}
SIDES = {"CA-a": "within", "CA-b": ">=", "CA-c": ">=", "CA-d": ">=", "CA-e": ">=",
         "CA-f": ">="}
ROWS = tuple(LINES)


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: the loop's one reasoning setting and one budget."""
    return hplan.settings()


def valid(failure: str | None, payload: Any, served_by: str | None) -> bool:
    """§0's validity, the one both the asker's flag and the scorer read."""
    return failure is None and isinstance(payload, dict) and served_by == PROVIDER_NAME


# --- the closed records, read where their own plan puts them --------------------------------

def halves_sample() -> Path:
    """`PLAN_HALVES.md`'s Stage A record: the design whose `v` and `e` prompts are
    this plan's."""
    return hplan.sample_path()


def halves_ask(session: str) -> Path:
    """`PLAN_HALVES.md`'s session records, whose arms `v` and `e` are this plan's."""
    return hplan.ask_path(session)


def halves_score() -> Path:
    """`PLAN_HALVES.md`'s Stage C record, which `CA-g2` holds the classes to."""
    return hplan.score_path()


# --- §7 to §9: the records --------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_cause/`.

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
    return random.Random(f"PLAN_CAUSE/order/{ORDER_SEED}/{session}")


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
