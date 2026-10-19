"""
The gate and the constants of `PLAN_SPOTCHECK.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_SPOTCHECK.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied.
If a blocking check ever forces an amendment, the amendment carries its own
line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §9's, fixed before any figure of the plan existed, and the
lines are §0's. `tests/test_spotcheck.py` pins every one of them, so that moving
one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_SPOTCHECK.md")
OUT = Path("results_spotcheck")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §1: the inputs, every one of them read-only ----------------------------
RUNG1 = Path("results/llm_run.json")                    # who escalated
BUDGET = Path("results3/budget_and_balance_ls.json")    # the random arrivals
ESCALATIONS = Path("results_escalations/score.json")    # the escalations alone

SPLIT = 0
SPLIT_SEED = 17                    # split 0 is order_search.split(seed=17)
N_SPACE = 134400

# --- §2 and §3: the sets ---------------------------------------------------
BUDGETS = (10, 50, 100, 251)       # audited decisions; the record's budgets
N_ESCALATIONS = 316
N_DECISIONS = 689                  # the train half's cases rung 1 decided itself
DRAWS = 5
AUDIT_SEED = 18000                 # draw d shuffles with Random(AUDIT_SEED + d)
ARMS = ("mix", "audit")            # with the escalations, and the audit alone

RARE = ("ACCOUNT_MANAGER", "T3_ENGINEERING", "SECURITY_INCIDENT",
        "ONCALL_ESCALATION")

# §1's material, as the drafter counted it; N-g1 recomputes it.
MATERIAL = {
    "decisions": 689,
    "outcome": {"ACTION": 689},
    "decided_right": 360,
    "distinct_tickets": 616,
    "keyword": 29,
    "by_truth": {"T2_TECHNICAL": 263, "SELF_SERVICE_DEFLECT": 139,
                 "BILLING_SPECIALIST": 100, "T1_GENERAL": 74,
                 "T3_ENGINEERING": 57, "ACCOUNT_MANAGER": 42,
                 "SECURITY_INCIDENT": 10, "ONCALL_ESCALATION": 4},
    "decided": {"T2_TECHNICAL": 388, "BILLING_SPECIALIST": 119,
                "SELF_SERVICE_DEFLECT": 94, "T1_GENERAL": 88},
    "queues_matching": {1: 27, 2: 208, 3: 325, 4: 124, 5: 2, 6: 3},
    "rules_matching": {"min": 8, "median": 37, "max": 145},
}

# §1's table of the five draws: at each budget, the T3_ENGINEERING,
# SECURITY_INCIDENT and keyword tickets, and the decisions rung 1 got wrong.
DRAW_MAKE_UP = {
    0: {10: (0, 0, 0, 3), 50: (3, 0, 3, 17), 100: (9, 3, 6, 47), 251: (18, 5, 13, 118)},
    1: {10: (1, 1, 1, 5), 50: (3, 1, 2, 20), 100: (13, 1, 4, 47), 251: (22, 2, 8, 114)},
    2: {10: (1, 0, 0, 5), 50: (2, 0, 0, 21), 100: (10, 0, 2, 42), 251: (32, 3, 9, 119)},
    3: {10: (1, 0, 1, 4), 50: (4, 0, 2, 25), 100: (6, 0, 3, 47), 251: (16, 3, 13, 123)},
    4: {10: (1, 0, 0, 4), 50: (2, 0, 0, 21), 100: (8, 0, 2, 41), 251: (20, 2, 9, 115)},
}

# --- §4: the endpoints and the comparators ---------------------------------
ARRIVAL = 519                      # arrival order, test split 0, of 995
ARRIVAL_SPACE = 42310
FULL = 843                         # the search on all 1,005 train cases
PUBLISHED_FULL = {"ls_test": 0.8472, "ls_space": 0.6033}
FULL_RARE = {"ACCOUNT_MANAGER": 19, "T3_ENGINEERING": 18,
             "SECURITY_INCIDENT": 5, "ONCALL_ESCALATION": 0}
ESC_ALL = {"test": 814, "space": 73020}   # FINDINGS_ESCALATIONS.md's all 316
ESC_ALL_RARE = {"ACCOUNT_MANAGER": 20, "T3_ENGINEERING": 0,
                "SECURITY_INCIDENT": 4, "ONCALL_ESCALATION": 0}
RARE_OF = {"ACCOUNT_MANAGER": 55, "T3_ENGINEERING": 57,
           "SECURITY_INCIDENT": 10, "ONCALL_ESCALATION": 3}

# --- §0: the lines -----------------------------------------------------------
N_A_LINE = ESC_ALL["test"]                                          # 814
N_B_LINE = ESC_ALL["test"] + (FULL - ESC_ALL["test"] + 1) // 2      # 814 + 15 = 829
N_C_LINE = FULL_RARE["T3_ENGINEERING"] // 2                         # 9
N_D_LINE = ESC_ALL["space"]                                         # 73,020
N_E_LINE = N_B_LINE                                                 # 829

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
