"""
The gate and the constants of `PLAN_STUDENTS.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_STUDENTS.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied,
as `bound/plan.py` calls it. If a blocking check ever forces an amendment, the
amendment carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything. No flag skips it. **Nothing here
spends, and the gate binds anyway**: what it protects is not money but the order
of events, that §0 was signed before any figure that could inform it existed.

THE CONSTANTS are §3's and §10's, fixed before any figure of the plan existed,
and the lines are §0's. `tests/test_students.py` pins every one of them, so that
moving one after a figure exists is visible in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_STUDENTS.md")
OUT = Path("results_students")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §1: the inputs, every one of them read-only ----------------------------
RUNG1 = Path("results/llm_run.json")                    # rung 1's answers and rules
REUSE_RUNS = (1, 2, 3)                                  # PLAN_REUSE.md's Stage B


def reuse_path(run: int) -> Path:
    return Path(f"results_reuse/run_n2000_r{run}.json")


LABELS = Path("results_ilp/labels.json")                # the answers, counted
CHOSEN = Path("results_ilp/chosen.json")                # the inducer on the answers
COMPARE = Path("results_ilp/compare.json")              # the inducer on the truth
FLOORS = Path("results3/floor_by_pool.json")            # arrival order, both surfaces
SPLITS = Path("results3/order_search_ls.json")          # the searched order, split 0
REFERENCES = Path("results3/order_search.json")         # rung 1's own engine
FRONTIER = Path("results/frontier.json")                # the cache's three rows
SCREEN = Path("results_screen/score.json")              # the model, ticket alone

N_CORPUS = 2000
CORPUS_SEED = 17
SPLIT_SEED = 17                    # split 0 is order_search.split(seed=17)
N_SPACE = 134400

# --- §1: the material, as the drafter counted it and T-g1 recomputes it ------
MATERIAL = {
    "rung1": {"answers": 579, "right": 245, "train": 286, "test": 293, "reach": 347},
    "reuse1": {"answers": 62, "right": 30, "train": 33, "test": 29, "reach": 32},
    "reuse2": {"answers": 31, "right": 15, "train": 12, "test": 19, "reach": 22},
    "reuse3": {"answers": 42, "right": 23, "train": 21, "test": 21, "reach": 25},
}

# --- §3: the students --------------------------------------------------------
FOLDS = 5
FOLD_SEED = 17
LAMBDAS = tuple(10 ** (k / 2) for k in range(-8, 3))    # 1e-4 ... 10, eleven
LBFGS_MEMORY = 10
ARMIJO = 1e-4
GRADIENT_TOL = 1e-7
MAX_ITER = 5000

# --- §8: the blocking checks -------------------------------------------------
MASK_CHECK_SEED = 17               # the points every mask route is checked on
MASK_CHECK_POINTS = 2000
SYNTHETIC_SEED = 17                # the regression's synthetic instances
CACHE_DISTANCES = (0, 1, 2)        # results/frontier.json's three cache rows

# --- §0: the lines -----------------------------------------------------------
ARRIVAL_TEST = 519                 # rung 1's rules in arrival order, of 995
ARRIVAL_SPACE = 42310              # the same, of 134,400
T_A_LINE = ARRIVAL_TEST            # T-a holds at tree < 519
T_B_LINE = ARRIVAL_TEST            # T-b holds at best < 519
T_C_LINE = ARRIVAL_SPACE           # T-c holds at tree > 42,310
T_D_LINE = ARRIVAL_TEST            # T-d holds at order > 519
T_E_LINE = 0                       # T-e holds at median(tree - base) < 0
THIN_SE = 2                        # thin: |b - c| < 2 sqrt(b + c)

# The published figures the gate reproduces, as published.
PUBLISHED = {
    "arrival_test": 0.521608, "arrival_space": 0.314807,
    "reversed_test": 0.546734, "reversed_space": 0.566815,
    "specificity_test": 0.1829,
    "searched": {"ls_train": 0.8786, "ls_test": 0.8472, "ls_space": 0.6033},
}

SCORE_PATH = OUT / "score.json"


def thin(b: int, c: int) -> bool:
    """§0's label: a paired difference within two standard errors. Exact: the
    comparison is done on squares, so no float decides it."""
    return (b - c) ** 2 < THIN_SE ** 2 * (b + c)


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

