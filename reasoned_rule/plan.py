"""
The gate and the constants of `PLAN_REASONED_RULE.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_REASONED_RULE.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `reasoned_rule/ask.py` calls
it before it constructs a client. No flag skips it. **The free stages get the
gate too**: what it protects is the order of events, not money. A record of
this plan written before the signature would be a figure that existed before
its band (§10 of the plan).

THE CLIENT AND THE INPUTS ARE THE CLOSED THREADS', IMPORTED AND NOT RETYPED (rule
A of the plan). The model, the prompt version, the temperature, the pin, both
reasoning settings and both token budgets come from `first_match.plan`, which
takes the first four from `queue_alone.plan`. The population is
`PLAN_QUEUE_ALONE.md`'s at level 3, rebuilt by `queue_alone.population`, and the
closed plans' records are read where their own `plan` modules put them.

THE ARMS CROSS TWO FACTORS (§0): the rule arm `t` and the plain arm `q` ask with
reasoning off, as `PLAN_QUEUE_ALONE.md` asked them; the reasoning rule arm `w`
and the reasoning arm `r` ask the same two prompts with reasoning on, as
`PLAN_FIRST_MATCH.md` asked its reasoning arm. `settings` says what each arm's
request carries.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_reasoned_rule.py` pins every one of them, so that
moving one after a figure exists is visible in a diff. **The lines are
fractions**, and every comparison with them is exact.

THE SEED. §10 fixes `ORDER_SEED = 79`. It becomes one stream per session, from a
string seed. CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from first_match import plan as fm_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_REASONED_RULE.md")
OUT = Path("results_reasoned_rule")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the client, PLAN_FIRST_MATCH.md's ---------------------------------------
MODEL = fm_plan.MODEL
PROMPT = fm_plan.PROMPT
TEMPERATURE = fm_plan.TEMPERATURE
REASONING_OFF = fm_plan.REASONING_OFF  # PLAN_REUSE.md §1's amendment: reasoning off
MAX_TOKENS = fm_plan.MAX_TOKENS        # the rule and plain arms', the proposer's own
REASONING_ON = fm_plan.REASONING_ON    # PLAN_FIRST_MATCH.md §2.2's
MAX_TOKENS_REASONING = fm_plan.MAX_TOKENS_REASONING
MAX_RETRIES = fm_plan.MAX_RETRIES
CALL_RETRY_WAIT = fm_plan.CALL_RETRY_WAIT  # seconds before a failed call's two retries

# --- §2.4: one provider, pinned, with fallbacks off -------------------------------------
PROVIDER = fm_plan.PROVIDER
PROVIDER_NAME = fm_plan.PROVIDER_NAME

# --- §10: the inputs, every one of them read-only ---------------------------------------
LEVEL = 3
REPS = fm_plan.REPS
N = fm_plan.N
SEED = fm_plan.SEED

# --- §10: the arms, and which of them reason ---------------------------------------------
REASONING_ARMS = ("w", "r")        # the reasoning rule arm and the reasoning arm
QUIET_ARMS = ("t", "q")            # the rule arm and the plain arm

# --- §10: the population (§0) ---------------------------------------------------------------
TICKET_PROMPTS = 171               # an arm's prompts, level 3's tickets
DECISIONS = 320                    # level 3's, PLAN_QUEUE_ALONE.md's

# --- §10: the sessions ----------------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2")
PASSES = 2
SMOKE_PER_ARM = 2
ORDER_SEED = 79

# --- §10: the limits ------------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.16)
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value (§0)
MIN_ANCHOR_PROMPTS = 100           # RR-a's prompts, at the least

# --- §0: the lines --------------------------------------------------------------------------
RR_A_MAX_GAP = Fraction(1, 20)     # holds at <= : S − A over the rule prompts
RR_B_LINE = Fraction(0)            # holds ABOVE : acc_w − acc_t
RR_C_LINE = Fraction(9, 10)        # holds at >= : acc_w
RR_D_LINE = Fraction(0)            # holds BELOW : (acc_r − acc_w) − (acc_q − acc_t)


def settings(arm: str) -> dict[str, Any]:
    """What an arm's request carries beyond the model, the temperature, the
    messages and the pin: its reasoning setting and its token budget (§1). The
    reasoning rule arm and the reasoning arm reason as `PLAN_FIRST_MATCH.md`'s
    reasoning arm did; the rule and plain arms as the proposer does, not at
    all."""
    if arm not in QUIET_ARMS + REASONING_ARMS:
        raise ValueError(f"no arm {arm!r}")
    if arm in REASONING_ARMS:
        return {"reasoning": json.loads(json.dumps(REASONING_ON)),
                "max_tokens": MAX_TOKENS_REASONING}
    return {"reasoning": json.loads(json.dumps(REASONING_OFF)), "max_tokens": MAX_TOKENS}


# --- the closed plans' records, read where those plans put them --------------------------

def queue_alone_sample() -> Path:
    return fm_plan.queue_alone_sample()


def queue_alone_ask(session: str) -> Path:
    return fm_plan.queue_alone_ask(session)


def first_match_sample() -> Path:
    return fm_plan.sample_path()


def first_match_ask(session: str) -> Path:
    return fm_plan.ask_path(session)


def first_match_score() -> Path:
    return fm_plan.score_path()


# --- §8 and §9: the records ------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_reasoned_rule/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.16). Ignored by
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
    return random.Random(f"PLAN_REASONED_RULE/order/{ORDER_SEED}/{session}")


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
