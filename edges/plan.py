"""
The gate and the constants of `PLAN_EDGES.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_EDGES.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§8 of the plan), as `fidelity/plan.py` calls it. If a blocking check ever
forces an amendment, the amendment carries its own line and `MIN_SIGNATURES`
rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §8's, fixed before any figure of the plan existed, and the
three band lines are §0's. `tests/test_edges.py` pins every one of them, so
that moving one after a figure exists is visible in a diff.

THE COIN. §8 fixes `COIN_SEED = 47`. How it becomes streams is fixed here,
before any draw existed: one string seed per run. CPython seeds a string through
SHA-512, so no draw depends on `PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_EDGES.md")
OUT = Path("results_edges")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §8: the inputs ----------------------------------------------------------
RUNS = (1, 2, 3)                   # PLAN_REUSE.md's Stage B runs
N = 2000
SEED = 17


def run_path(run: int) -> Path:
    """A Stage B record of PLAN_REUSE.md: an input, never an output (rule B)."""
    return reuse_plan.run_path(run)


# --- §8: the null ------------------------------------------------------------
COIN_DRAWS = 2000
COIN_SEED = 47

# --- §8: W-b's minimum -------------------------------------------------------
MIN_QUALIFYING_EDGES = 20

# --- §0: the three lines -----------------------------------------------------
W_A_REFUTED_AT_OR_ABOVE = 0.50     # W-a holds at a share right < 0.50
W_B_REFUTED_AT_OR_ABOVE = 0.60     # W-b holds at a rate < 0.60
W_C_MIN_SHARE = 0.05               # W-c holds at a coin share >= 0.05

# --- W-g1: the published size the space labels are checked against ----------
SPACE_POINTS = 134_400
T2 = "T2_TECHNICAL"
T2_SPACE_POINTS = 36_720           # results3/FINDINGS_ORDERS.md, part four

# --- W-g3: the hash seeds the coin is fingerprinted under --------------------
FINGERPRINT_SEEDS = ("0", "1", "2")
FINGERPRINT_DRAWS = 25

SCORE_PATH = OUT / "score.json"


def coin_rng(run: int) -> random.Random:
    """The coin of run `run` (§0, `W-c`): one stream per run."""
    return random.Random(f"PLAN_EDGES/coin/{COIN_SEED}/run{run}")


def gate_signature(path: Path = PLAN) -> dict:
    """Every signature line of this plan filled in, and at least one."""
    return reuse_plan.gate_signature(path, minimum=MIN_SIGNATURES)


def refuse_unsigned(what: str, path: Path = PLAN) -> dict:
    """Exit before anything is measured or written while §0 is unsigned."""
    gate = gate_signature(path)
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {what} while {path.name} is unsigned — "
                 f"{gate['found']} signature line(s), {gate['unsigned']} blank.\n"
                 "  A model may draft a band and may not sign one. Nothing was "
                 "measured and nothing was written.\n")
    return gate
