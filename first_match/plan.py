"""
The gate and the constants of `PLAN_FIRST_MATCH.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_FIRST_MATCH.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `first_match/ask.py` calls
it before it constructs a client. No flag skips it. **The free stages get the
gate too**: what it protects is the order of events, not money. A record of
this plan written before the signature would be a figure that existed before
its band (§10 of the plan).

THE CLIENT AND THE INPUTS ARE THE CLOSED THREADS', IMPORTED AND NOT RETYPED (rule
A of the plan). The model, the prompt version, reasoning off, the temperature,
the plain arm's token budget and the pin come from `queue_alone.plan`, which
takes them from `manual.plan` and `reuse.plan`. The population is
`PLAN_QUEUE_ALONE.md`'s at level 3, rebuilt by `queue_alone.population`, and
that plan's records are read where `queue_alone.plan` puts them.

THE REASONING ARM'S SETTING IS THIS PLAN'S OWN (§2.2): `{"effort": "high"}` with
16,000 tokens, the budget `PLAN_MANUAL.md` gave its compiled answer. `settings`
says what each arm's request carries.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_first_match.py` pins every one of them, so that
moving one after a figure exists is visible in a diff. **The lines are
fractions**, and every comparison with them is exact.

THE SEED. §10 fixes `ORDER_SEED = 73`. It becomes one stream per session, from a
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

from queue_alone import plan as qa_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_FIRST_MATCH.md")
OUT = Path("results_first_match")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the client, PLAN_QUEUE_ALONE.md's plain arm --------------------------------
MODEL = qa_plan.MODEL
PROMPT = qa_plan.PROMPT
TEMPERATURE = qa_plan.TEMPERATURE
REASONING_OFF = qa_plan.REASONING  # PLAN_REUSE.md §1's amendment: reasoning off
MAX_TOKENS = qa_plan.MAX_TOKENS    # the plain arm's, the proposer's own
MAX_RETRIES = 2                    # the proposer's own
CALL_RETRY_WAIT = (10, 30)         # seconds before a failed call's two retries (§1)

# --- §2.2: the reasoning arm ---------------------------------------------------------
REASONING_ON = {"effort": "high"}
MAX_TOKENS_REASONING = 16000       # PLAN_MANUAL.md's COMPILE_MAX_TOKENS

# --- §2.4: one provider, pinned, with fallbacks off -----------------------------------
PROVIDER = qa_plan.PROVIDER
PROVIDER_NAME = qa_plan.PROVIDER_NAME

# --- §10: the inputs, every one of them read-only --------------------------------------
LEVEL = 3
REPS = qa_plan.REPS
N = qa_plan.N
SEED = qa_plan.SEED

# --- §10: the population (§0) -------------------------------------------------------------
TICKET_PROMPTS = 171               # an arm's prompts, level 3's tickets
DECISIONS = 320                    # level 3's, PLAN_QUEUE_ALONE.md's

# --- §10: the sessions --------------------------------------------------------------------
SESSIONS = ("smoke", "pass1", "pass2")
PASSES = 2
SMOKE_PER_ARM = 2
ORDER_SEED = 73

# --- §10: the limits ----------------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.13)
MAX_INVALID_SHARE = Fraction(1, 20)  # above it, a row has no value (§0)
MIN_ANCHOR_PROMPTS = 100           # FM-a's prompts, at the least
MIN_NAMED_ORDER_ERRORS = 20        # FM-c's order errors that name a rule, at the least
MAX_UNNAMED_SHARE = Fraction(1, 20)  # above it, FM-c has no value

# --- §0: the lines ------------------------------------------------------------------------
FM_A_MAX_GAP = Fraction(1, 20)     # holds at <= : S − A over the plain prompts
FM_B_LINE = Fraction(0)            # holds ABOVE : acc_n − acc_q
FM_C_LINE = Fraction(1, 2)         # holds at >= : lower / named, over the naming arm's order errors
FM_D_LINE = Fraction(0)            # holds ABOVE : acc_r − acc_q
FM_E_LINE = Fraction(9, 10)        # holds at >= : acc_r
FM_F_LINE = Fraction(0)            # holds ABOVE : acc_r − acc_n


def settings(arm: str) -> dict[str, Any]:
    """What an arm's request carries beyond the model, the temperature, the
    messages and the pin: its reasoning setting and its token budget (§1). The
    reasoning arm is `"r"`; the plain and naming arms reason as the proposer
    does, not at all."""
    if arm not in ("q", "n", "r"):
        raise ValueError(f"no arm {arm!r}")
    if arm == "r":
        return {"reasoning": json.loads(json.dumps(REASONING_ON)),
                "max_tokens": MAX_TOKENS_REASONING}
    return {"reasoning": json.loads(json.dumps(REASONING_OFF)), "max_tokens": MAX_TOKENS}


# --- PLAN_QUEUE_ALONE.md's records, read where that plan puts them -------------------------

def queue_alone_sample() -> Path:
    return qa_plan.sample_path()


def queue_alone_ask(session: str) -> Path:
    return qa_plan.ask_path(session)


def queue_alone_score() -> Path:
    return qa_plan.score_path()


def queue_alone_orders() -> Path:
    return qa_plan.OUT / "orders.json"


# --- §8 and §9: the records ------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_first_match/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.13). Ignored by
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
    return random.Random(f"PLAN_FIRST_MATCH/order/{ORDER_SEED}/{session}")


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
