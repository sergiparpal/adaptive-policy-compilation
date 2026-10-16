"""
The gate and the constants of `PLAN_BOUND.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_BOUND.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied,
as `primacy/plan.py` calls it. If a blocking check ever forces an amendment, the
amendment carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §8's, fixed before any figure of the plan existed, and the
lines are §0's. `tests/test_bound.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. The finder's own constants,
`FINDER_SEED` and `FINDER_STARTS`, live beside the code they drive in
`bound/certificate.py` and are pinned by the same test.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_BOUND.md")
OUT = Path("results_bound")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §1: the inputs, every one of them read-only ----------------------------
RULES = Path("results/llm_run.json")                   # rung 1's 577 rules
FULLSPACE = Path("results3/order_search_ls_fullspace.json")  # the direct search
SPLITS = Path("results3/order_search_ls.json")         # the search per split
BUDGET = Path("results3/start_budget_check.json")      # 64, 128, 256 starts, pure
CEILINGS = Path("results3/order_search.json")          # per-split train ceilings

POOLS = ("puro", "hibrido")
N_SPLITS = 5
SPLIT_SEED = 17                    # split s is order_search.split(seed=17 + s)
N_SPACE = 134400

# --- §0: the lines -----------------------------------------------------------
# H-a and H-b: the share of the space's residue the certificate closes, per pool.
H_A_LINE = 0.50                    # H-a holds at share >= 0.50 (pure)
H_B_LINE = 0.50                    # H-b holds at share >= 0.50 (hybrid)
# H-c: met on neither pool of the space, at the published precision.
SPACE_PLACES = 4                   # the direct search is published to 4 decimals
# H-d: the median share over the ten (split, pool) train instances of the corpus.
H_D_LINE = 0.75                    # H-d holds at median >= 0.75

# --- §6: the blocking checks -------------------------------------------------
PLUMBING_SEED = 17                 # the random orders H-g1 scores both ways
PLUMBING_ORDERS = 3
BRUTE_SEED = 17                    # H-g3's synthetic instances
BRUTE_INSTANCES = 2000
BRUTE_MAX_RULES = 7                # every order enumerated: at most 7! = 5,040

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
