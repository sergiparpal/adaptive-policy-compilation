"""
The gate and the constants of `PLAN_PRIMACY.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_PRIMACY.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§8 of the plan), as `edges/plan.py` calls it. If a blocking check ever forces an
amendment, the amendment carries its own line and `MIN_SIGNATURES` rises with
it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §8's, fixed before any figure of the plan existed, and the two
band lines are §0's. `tests/test_primacy.py` pins every one of them, so that
moving one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_PRIMACY.md")
OUT = Path("results_primacy")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §8: the inputs, every one of them read-only (rule B) -------------------
SOURCE = Path("results2/pair_judgement_1600.json")     # the 1,600 answers
STAGE_D = Path("results2/pair_judgement_learned.json")  # the 400 reused, as dealt
HIDDEN = Path("results2/pair_judgement_hidden.json")    # Stage C, the hidden policy
SAMPLE = Path("results2/pair_sample_1600.json")         # the truth, and B-d's split
DIRECTION = Path("results3/edge_direction_1600.json")   # published: 801 of 1,479
ASYMMETRY = Path("results3/answer_asymmetry.json")      # published: §15's H4

N_ROWS = 1600
N_REUSED = 400                     # answered on 2026-08-24, Stage D of PLAN_PAIRWISE
N_FRESH = 1200                     # answered by PLAN_PROPOSER_1600's Stage B
N_HIDDEN = 170
POSITION_SEED = 17                 # rung2/pair_judgement.py's, for every deal

# --- §0: L-a -----------------------------------------------------------------
# §2.1's selection rule: the queue pairs with at least L_A_SELECT_MIN_ROWS
# declared answers whose majority share is below L_A_SELECT_BELOW. In the
# record's own per-queue-pair counts it picks one, 86 against 82, and `L-g3`
# checks that it still picks exactly that one.
L_A_SELECT_MIN_ROWS = 30
L_A_SELECT_BELOW = 0.60
L_A_QUEUE_PAIR = ("SELF_SERVICE_DEFLECT", "T2_TECHNICAL")
L_A_LINE = 0.20                    # L-a holds at d >= 0.20
L_A_MIN_SIDE = 20                  # below this many answers in a slot: unadjudicable

# --- §0: L-b -----------------------------------------------------------------
L_B_LINE = 0.025                   # L-b holds at |difference| < 0.025

# --- §7: the readings --------------------------------------------------------
READING_MIN_ROWS = 30              # queue pairs read one by one in L-c

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
