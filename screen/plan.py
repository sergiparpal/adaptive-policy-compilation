"""
The gate and the constants of `PLAN_SCREEN.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_SCREEN.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment, the amendment
carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `screen/ask.py` calls it
before it constructs the client. No flag skips it. **The free stages get the
gate too**: what it protects is not money but the order of events. Stage A's
share of held-out decisions whose screen's plurality is the true queue is
exactly what would inform `V-b`'s and `V-d`'s bands (§10 of the plan).

THE INPUTS AND THE CLIENT ARE `PLAN_FIDELITY.md`'s, IMPORTED AND NOT RETYPED
(rule A of the plan). A second copy of the model name or of the reasoning
setting could drift from the one that produced the answers this plan compares
with, and nothing downstream would say so.

THE CONSTANTS are §10's, and the band lines are §0's, fixed before any figure
of the plan existed. `tests/test_screen.py` pins every one of them, so that
moving one after a figure exists is visible in a diff. The three population
sizes are §0's own counts: the checks of `V-g3` rebuild them from the records
and refuse if they differ.

THE SEED. §10 fixes `ORDER_SEED = 53`. How it becomes one stream per session
and pass is fixed here, before any order existed: one string seed per stream.
CPython seeds a string through SHA-512, so no stream depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from fidelity import plan as fidelity_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_SCREEN.md")
OUT = Path("results_screen")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the inputs, PLAN_FIDELITY.md's ----------------------------------------
RUNS = fidelity_plan.RUNS
N = fidelity_plan.N
SEED = fidelity_plan.SEED
FIDELITY_SAMPLE = fidelity_plan.SAMPLE_PATH
FIDELITY_SCORE = fidelity_plan.SCORE_PATH
FIDELITY_TICKET_ONLY = fidelity_plan.ask_path("ticket_only")


def fidelity_base(run: int) -> Path:
    """`PLAN_FIDELITY.md`'s answers with the screen, for one base: an input,
    never an output (rule B)."""
    return fidelity_plan.ask_path(f"base{run}")


# --- §10: the client, PLAN_FIDELITY.md's unchanged (§1) ---------------------------
MODEL = fidelity_plan.MODEL
PROMPT = fidelity_plan.PROMPT
REASONING = fidelity_plan.REASONING

# --- §10: the populations (§0) -------------------------------------------------
PILOT_PER_RUN = fidelity_plan.TICKET_ONLY_PER_RUN     # the decisions F-f paired
HELD_OUT_SIZES = {1: 429, 2: 405, 3: 425}             # positions 100..599, less F-f's tickets
TICKETS = 1184                                        # the draw and census, by Case.key()
ASKED_BY_F_F = 301                                    # F-f's ticket-only session, 2026-10-03

# --- §10: the sessions ---------------------------------------------------------
TICKET_ONLY_DRAWS = 2
ANCHOR_DRAWS = 1
SMOKE_PER_ARM = 5
ORDER_SEED = 53

# --- §10: the limits -----------------------------------------------------------
MAX_INVALID_SHARE = 0.05           # above it, a run has no value (§0)
MIN_PULL_POPULATION = 100          # V-c's decisions with t1 != p, per run
MIN_CELL = 50                      # each cell of V-d, per run

# --- §0: the lines ---------------------------------------------------------------
V_A_MAX_GAP = 0.05                 # V-a holds at S − A <= 0.05, in both clauses
V_B_REFUTED_AT_OR_BELOW = 0.0      # V-b holds at > 0
V_C_MIN_PULL = 0.10                # V-c holds at >= 0.10
V_D_REFUTED_AT_OR_BELOW = 0.0      # each clause of V-d holds at > 0

ONCALL, SECURITY, RARE = fidelity_plan.ONCALL, fidelity_plan.SECURITY, fidelity_plan.RARE

# --- §8: the sessions, in the order they run --------------------------------------
SESSIONS = ("smoke", "anchor", "ticket_only")
SAMPLE_PATH = OUT / "sample.json"
SCORE_PATH = OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.10). Ignored by
    git, and gone once the session's record is written."""
    return OUT / f"ask_{session}.partial.jsonl"


def order_rng(session: str, pass_no: int) -> random.Random:
    """The order of one pass of one session."""
    return random.Random(f"PLAN_SCREEN/order/{ORDER_SEED}/{session}/pass{pass_no}")


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
