"""
The gate and the constants of `PLAN_WHY.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_WHY.md` that starts `**Signed by Sergi:` must be filled in, and there must
be at least `MIN_SIGNATURES`: one today, §0's. The counting is `reuse/plan.py`'s,
called with this plan's path and minimum rather than copied (§8 of the plan). If
a blocking check ever forces an amendment, the amendment carries its own line
and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is the order of events,
that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §8's, fixed before any figure of the held-out answers existed,
and the four band lines are §0's. `CODEBOOK_DIGEST` is the codebook's
fingerprint when §0 was drafted, and `DEV` the development figures §0 declares,
which `Y-g3` must reproduce. `tests/test_why.py` pins every one of them, so that
moving one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_WHY.md")
OUT = Path("results_why")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §8: the inputs, every one of them read-only ------------------------------
SOURCE = Path("results2/pair_judgement_1600.json")     # the 1,600 answers
STAGE_D = Path("results2/pair_judgement_learned.json")  # the development batch's own record
HIDDEN = Path("results2/pair_judgement_hidden.json")    # Stage C, development too
SAMPLE = Path("results2/pair_sample_1600.json")         # the truth per pair
DIRECTION = Path("results3/edge_direction_1600.json")   # the truth, as published

# --- §2.1: the split ---------------------------------------------------------
DEV_BATCH = "stage_d"              # answered 2026-08-24, read to build the codebook
TEST_BATCH = "this_run"            # answered 2026-08-25, held out until signature
N_DEV_ANSWERS = 400
N_TEST_ANSWERS = 1200
N_HIDDEN = 170

# --- §8: the codebook, frozen --------------------------------------------------
CODEBOOK_DIGEST = "65e1732a08fd32c0"

# --- §0: the development figures, which Y-g3 reproduces ------------------------
DEV = {
    "stage_d": {
        "n": 365,
        "codes": {"spec": 172, "count": 25, "queue": 130, "prio": 170, "match": 42,
                  "order": 3},
        "Y-a": (92, 172), "Y-b": (37, 147),
        "Y-c": ((108, 147), (91, 193)), "Y-d": ((95, 138), (99, 140)),
    },
    "stage_c": {
        "n": 166,
        "codes": {"spec": 44, "count": 1, "queue": 87, "prio": 78, "match": 10,
                  "order": 1},
        "Y-a": (21, 44), "Y-b": (12, 43),
        "Y-c": ((30, 43), (58, 122)), "Y-d": ((40, 44), (110, 122)),
    },
}

# --- §0: the four lines --------------------------------------------------------
Y_A_BAND = (0.45, 0.62)            # Y-a holds at 0.45 <= share <= 0.62
Y_B_REFUTED_AT_OR_ABOVE = 0.33     # Y-b holds at share < 0.33
Y_C_MIN_DIFFERENCE = 0.15          # Y-c holds at difference >= 0.15
Y_D_MAX_ABS_DIFFERENCE = 0.06      # Y-d holds at |difference| < 0.06

MIN_ROWS = 50                      # below this many rows in a group: unadjudicable

# --- §7: the readings ----------------------------------------------------------
QUOTES_PER_CODE = 5                # the lowest-indexed held-out whys of each code

SCORE_PATH = OUT / "score.json"


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
