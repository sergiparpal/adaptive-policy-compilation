"""
The gate and the constants of `PLAN_ESCALATIONS.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_ESCALATIONS.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied.
If a blocking check ever forces an amendment, the amendment carries its own
line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §9's, fixed before any figure of the plan existed, and the
lines are §0's. `tests/test_escalations.py` pins every one of them, so that
moving one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_ESCALATIONS.md")
OUT = Path("results_escalations")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §1: the inputs, every one of them read-only ----------------------------
RUNG1 = Path("results/llm_run.json")                    # who escalated
BUDGET = Path("results3/budget_and_balance_ls.json")    # the random arrivals
STUDENTS = Path("results_students/score.json")          # the 286 named, 814
FLOORS = Path("results3/floor_by_pool.json")            # arrival order

SPLIT = 0
SPLIT_SEED = 17                    # split 0 is order_search.split(seed=17)
N_SPACE = 134400

# --- §2.4 to §2.6: the selections -------------------------------------------
BUDGETS = (10, 50, 100, 251)
FRACTIONS = {10: 0.01, 50: 0.05, 100: 0.10, 251: 0.25}  # the record's own
N_ESCALATIONS = 316
DRAWS = 5
DRAW_SEED = 17000                  # draw d is random.Random(DRAW_SEED + d)
RULES = ("random", "arrival", "crowded")

# --- §1: the material, as the drafter counted it and J-g1 recomputes it -------
MATERIAL = {
    "escalations": 316, "conflict": 300, "impasse": 16, "distinct_tickets": 294,
    "keyword": 8,
    "by_truth": {"SELF_SERVICE_DEFLECT": 114, "T2_TECHNICAL": 99,
                 "T1_GENERAL": 53, "BILLING_SPECIALIST": 35,
                 "ACCOUNT_MANAGER": 12, "T3_ENGINEERING": 3},
    "queues_matching": {1: 1, 2: 58, 3: 157, 4: 99, 5: 1},
    "rules_matching": {"min": 14, "median": 57, "max": 150},
}

# --- §0: the lines -----------------------------------------------------------
ARRIVAL = 519                      # arrival order, test split 0, of 995
ARRIVAL_SPACE = 42310
FULL = 843                         # the search on all 1,005 train cases
J_A_LINE = ARRIVAL + (FULL - ARRIVAL + 1) // 2   # 519 + 162 = 681
J_B_LINE = 717                     # random arrivals at 50, the median
J_C_LINE = 820                     # random arrivals at 251, the median
J_E_LINE = 0.3993                  # random arrivals at 50 over the space
SPACE_PLACES = 4
NAMED_286 = {"test": 814, "space": 73420}   # PLAN_STUDENTS.md's truth_order_286
PUBLISHED_FULL = {"ls_test": 0.8472, "ls_space": 0.6033}

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
