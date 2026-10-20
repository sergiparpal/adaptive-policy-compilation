"""
The gate and the constants of `PLAN_UNREACHED.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_UNREACHED.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied.
If a blocking check ever forces an amendment, the amendment carries its own
line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §9's, fixed before any figure of the plan existed, and the
lines are §0's. `tests/test_unreached.py` pins every one of them, so that moving
one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_UNREACHED.md")
OUT = Path("results_unreached")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §1: the inputs, every one of them read-only ----------------------------
RUNG1 = Path("results/llm_run.json")                    # who escalated; the rules
BUDGET = Path("results3/budget_and_balance_ls.json")    # the random arrivals
ESCALATIONS = Path("results_escalations/score.json")    # the escalations alone
SPOTCHECK = Path("results_spotcheck/score.json")        # both endpoints' reads
READINGS = Path("results_spotcheck/readings.json")      # both endpoints' orders

SPLIT = 0
SPLIT_SEED = 17                    # split 0 is order_search.split(seed=17)
N_SPACE = 134400
N_TEST = 995
SPACE_PLACES = 4

# --- §2 and §3: the orders, the rule and the moves ---------------------------
ENDPOINTS = ("escalations", "full")
KEY_RULE = "R0545"                 # the rule T3_ENGINEERING turns on
BUDGETS = (10, 50, 100, 251)       # the optimizer audit's random arrivals
DRAWS = 5
COIN_DRAWS = 100
COIN_SEED = 19000                  # placement d is random.Random(COIN_SEED + d)

RARE = ("ACCOUNT_MANAGER", "T3_ENGINEERING", "SECURITY_INCIDENT",
        "ONCALL_ESCALATION")

# §1's material, as the drafter counted it; Z-g1 recomputes it. Matching, the
# halves, rung 1's escalated flag, birth indices, queues and extensions only.
MATERIAL = {
    "rules": 577,
    "born_in_test": 291,
    "born_in_train": 286,
    "match_their_birth_case": 577,
    "born_at_a_train_escalation": 286,
    "escalations": {
        "unreached": 25, "distinct": 22, "born_in_test": 25,
        "by_queue": {"T2_TECHNICAL": 10, "T1_GENERAL": 5, "ONCALL_ESCALATION": 4,
                     "T3_ENGINEERING": 3, "SELF_SERVICE_DEFLECT": 2,
                     "SECURITY_INCIDENT": 1},
        "test_matches": 162, "birth_ticket_matches": 26,
        "test_cases_touched": 90, "test_cases_only_unreached": 0,
        "space_points": 132728,
    },
    "full": {
        "unreached": 5, "distinct": 5, "born_in_test": 5,
        "by_queue": {"T1_GENERAL": 2, "T3_ENGINEERING": 1,
                     "SELF_SERVICE_DEFLECT": 1, "T2_TECHNICAL": 1},
        "test_matches": 10, "birth_ticket_matches": 5,
        "test_cases_touched": 10, "test_cases_only_unreached": 0,
        "space_points": 5882,
    },
}

# §1's table: every rule no escalation reaches, as (queue, birth index,
# conditions, test cases matched, of them on its birth ticket, space points,
# reached by no train case either).
UNREACHED = {
    "R0016": ("T2_TECHNICAL", 35, 3, 10, 1, 10080, False),
    "R0019": ("SECURITY_INCIDENT", 44, 2, 2, 1, 16800, False),
    "R0027": ("T2_TECHNICAL", 71, 4, 2, 1, 840, False),
    "R0062": ("T1_GENERAL", 291, 8, 1, 1, 6, False),
    "R0080": ("SELF_SERVICE_DEFLECT", 426, 5, 9, 1, 120, False),
    "R0087": ("T1_GENERAL", 506, 4, 1, 1, 1050, True),
    "R0114": ("T2_TECHNICAL", 757, 4, 5, 1, 2520, False),
    "R0117": ("T1_GENERAL", 778, 5, 3, 1, 40, True),
    "R0150": ("T1_GENERAL", 937, 6, 3, 1, 160, False),
    "R0158": ("T2_TECHNICAL", 992, 3, 1, 1, 1680, False),
    "R0211": ("T1_GENERAL", 1211, 8, 2, 1, 40, False),
    "R0267": ("T3_ENGINEERING", 1402, 3, 2, 1, 3520, True),
    "R0287": ("ONCALL_ESCALATION", 1439, 2, 19, 1, 16800, False),
    "R0308": ("T2_TECHNICAL", 1517, 4, 3, 1, 2520, False),
    "R0351": ("SELF_SERVICE_DEFLECT", 1586, 7, 2, 1, 12, True),
    "R0357": ("T2_TECHNICAL", 1602, 6, 6, 1, 640, False),
    "R0361": ("T2_TECHNICAL", 1608, 5, 2, 1, 1260, True),
    "R0373": ("ONCALL_ESCALATION", 1628, 2, 19, 1, 16800, False),
    "R0448": ("T2_TECHNICAL", 1778, 3, 9, 1, 6720, False),
    "R0450": ("T2_TECHNICAL", 1784, 4, 2, 1, 2400, False),
    "R0459": ("T2_TECHNICAL", 1795, 2, 5, 1, 6720, False),
    "R0493": ("ONCALL_ESCALATION", 1863, 2, 19, 1, 16800, False),
    "R0506": ("ONCALL_ESCALATION", 1884, 2, 19, 2, 16800, False),
    "R0545": ("T3_ENGINEERING", 1939, 2, 13, 1, 6720, False),
    "R0570": ("T3_ENGINEERING", 1980, 3, 3, 1, 1680, False),
}
# Written the same, conditions and queue: one move, counted once, under the
# earliest-born.
COPIES = ("R0287", "R0373", "R0493", "R0506")

# §1's curve: the rules no label reaches, per draw of the optimizer audit's
# random arrivals on split 0, at each budget.
CURVE_REACH = {
    10: (247, 357, 264, 327, 305),
    50: (98, 117, 115, 107, 133),
    100: (59, 52, 71, 64, 64),
    251: (17, 18, 23, 28, 18),
}

# --- §4: the endpoints and the references -------------------------------------
ARRIVAL = 519                      # arrival order, test split 0, of 995
ARRIVAL_SPACE = 42310
ESC_ALL = {"test": 814, "space": 73020}   # FINDINGS_ESCALATIONS.md's all 316
FULL = {"test": 843, "space": 81089}      # the search on all 1,005 train cases
PUBLISHED_FULL = {"ls_test": 0.8472, "ls_space": 0.6033}
BEST_FROM = {"escalations": "aleatorio 57", "full": "aleatorio 13"}
ESC_ALL_RARE = {"ACCOUNT_MANAGER": 20, "T3_ENGINEERING": 0,
                "SECURITY_INCIDENT": 4, "ONCALL_ESCALATION": 0}
FULL_RARE = {"ACCOUNT_MANAGER": 19, "T3_ENGINEERING": 18,
             "SECURITY_INCIDENT": 5, "ONCALL_ESCALATION": 0}

# --- §0: the lines -----------------------------------------------------------
GAP = FULL["test"] - ESC_ALL["test"]                    # 29
SPACE_GAP = FULL["space"] - ESC_ALL["space"]            # 8,069
Z_A_LINE = 1                       # one rule besides the key rule
Z_B_LINE = (GAP + 1) // 2          # 15
Z_C_LINE = (SPACE_GAP + 1) // 2    # 4,035
Z_D_LINE = ESC_ALL["test"]         # 814
Z_E_LINE = ESC_ALL["space"]        # 73,020

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
