"""
`PLAN_BLIND.md`'s gate, the constants of its §11, §0's lines, and the figures §0
declares of what is already paid for.

**The gate reads `PLAN_BLIND.md` and no other plan, and counts every signature
line.** The counting is `reuse/plan.py`'s, called and not copied, with this
plan's own minimum: §0 carries one line. A gate that read the wrong file would be
worse than none, because it would be believed (`CLAUDE.md`).

**The constants are fixed before any figure of the plan exists** and pinned by
`tests/test_blind.py`, so that moving one afterwards shows in a diff.

**The declared figures are §0's, transcribed to the digits §0 gives them.** They
were computed while the plan was drafted, and `K-g2` recomputes every one from
the records and refuses if one differs: the drafter's arithmetic is checked, not
trusted.
"""

from __future__ import annotations

import sys
from pathlib import Path

from overlap import plan as overlap_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_BLIND.md")
OUT = Path("results_blind")
MIN_SIGNATURES = 1                 # §0's table; an amendment would add its own

# --- §11: the run -----------------------------------------------------------
N = 2000
SEED = 17
MODEL = "deepseek/deepseek-v4-flash"
REASONING = {"effort": "none"}     # PLAN_REUSE.md's amendment, kept
PROMPT = "v2b"
MAX_SHOWN = 12                     # v2's neighbourhood, on a CONFLICT only
PLACEMENT_ROUNDS = 1               # §2's K, after a blind draft
LISTING_SEED = 17                  # the order of a placement round's list
REPS = 3                           # §2's R
SMOKE_N = 20

# --- §0's lines -------------------------------------------------------------
K_A_MAX_ALONE = 0.50               # K-a holds at a median share <= 0.50
K_B_MIN_DIRECTION = 0.60           # K-b holds at a reading >= 0.60
K_C_MIN_MARGIN = 0.0               # K-c holds at declared minus ranking >= 0
K_D_MIN_FILL = 0.50                # K-d holds at a median share >= 0.50 ...
K_D_MIN_RUNS_WITH_ROOM = 2         # ... over the runs with room, at least two
K_E_MIN_DIRECTION = 0.60           # K-e holds at a reading >= 0.60
MIN_UNITS = 20                     # K-b, K-c and K-e need this many older rules

# --- What is already paid for -----------------------------------------------
BASELINE_REPS = (1, 2, 3)          # the three protocols ran three times each
RUNG1 = Path("results/llm_run.json")
PAIRWISE = Path("results2/pair_judgement_1600.json")
OVERLAP_SCORE = Path("results_overlap/score.json")
V2E_SMOKE = overlap_plan.SMOKE_PATH


def v1_path(rep: int) -> Path:
    """`PLAN_REUSE.md`'s run `rep`: v1, declaration offered."""
    return reuse_plan.run_path(rep)


def v1e_path(rep: int) -> Path:
    """`PLAN_AUTHORSHIP.md`'s run `rep`: v1e, declaration imposed on every overlap."""
    return overlap_plan.v1e_path(rep)


def v2e_path(rep: int) -> Path:
    """`PLAN_OVERLAP.md`'s run `rep`: v2e, imposed where the queues differ."""
    return overlap_plan.run_path(rep)


BASELINES = {"v1": v1_path, "v1e": v1e_path, "v2e": v2e_path}

# What §0 declares. `K-g2` recomputes each and refuses if one differs at the
# digits given here. `None` is a run without room, or a reading without units.
# A direction reading is (units, reading by older rule, hits, strict pairs).
DECLARED: dict = {
    "outside": {"space": 67200, "corpus": 1929},
    "baselines": {
        "v1": {"k_a": (1.0, 1.0, 0.8125), "k_a_median": 1.0,
               "k_b": (0, None, 0, 0), "k_b_stage_c": (0, None, 0, 0),
               "k_d": (None, None, 0.6667), "k_e": (0, None, 0, 0),
               "across_queues_and_keyword": ((17, 17), (6, 6), (27, 24))},
        "v1e": {"k_a": (1.0, 0.9655, 0.9667), "k_a_median": 0.9667,
                "k_b": (2, 0.5, 2, 3), "k_b_stage_c": (2, 0.5, 2, 3),
                "k_d": (None, 0.5714, None), "k_e": (2, 0.5, 2, 3),
                "across_queues_and_keyword": ((22, 22), (62, 59), (0, 0))},
        "v2e": {"k_a": (0.8704, 1.0, 1.0), "k_a_median": 1.0,
                "k_b": (2, 0.25, 1, 3), "k_b_stage_c": (2, 0.75, 2, 3),
                "k_d": (0.0345, None, None), "k_e": (2, 0.0, 0, 3),
                "across_queues_and_keyword": ((58, 51), (21, 21), (0, 0))},
    },
    "rung1_blind_births": {
        "20": {"k_a": 0.7368, "on_an_impasse": 20},
        "50": {"k_a": 0.3061, "on_an_impasse": 34},
        "100": {"k_a": 0.1649, "on_an_impasse": 37},
        "impasse_born": {"rules": 37, "k_a": 0.4444, "crossing_pairs": 72,
                         "strict": 60, "units": 25},
    },
    "pairwise": {
        "answers_with_a_pair": 1479, "keyword_pairs": 290,
        "space": {"declared": (325, 0.6618, 610, 891),
                  "stage_c_ranking": (325, 0.7194, 686, 891),
                  "newborn_wins": (325, 0.5525, 504, 891)},
        "corpus": {"declared": (320, 0.6455, 603, 898),
                   "stage_c_ranking": (320, 0.6966, 667, 898),
                   "newborn_wins": (320, 0.5342, 495, 898)},
        "split": {"unreachable_queue_pairs": 6, "queue_pairs": 18,
                  "reachable": (171, 0.8277, 308, 366),
                  "unreachable": (253, 0.5801, 302, 525)},
    },
    # The hidden policy written through v2b's path, K-g1.
    "hidden": {"born": 29, "declarations": 253, "installed": 199, "exempted": 41},
}

# The v2b texts, frozen. `K-g3` refuses if `protocol.fingerprint()` differs.
FINGERPRINT = "311d774209da570a"


def run_path(rep: int) -> Path:
    """Where Stage B's run `rep` lands, and where Stage C reads it."""
    return OUT / f"run_n{N}_r{rep}.json"


SMOKE_PATH = OUT / f"run_n{SMOKE_N}_smoke.json"
SCORE_PATH = OUT / "score.json"


def partial_path(tag: str) -> Path:
    """The answers of a run in progress, kept so that an interruption loses
    nothing paid for. Git-ignored; it goes once the run's record is written."""
    return OUT / f"run_{tag}.partial.jsonl"


def gate_signature(path: Path = PLAN, minimum: int = MIN_SIGNATURES) -> dict:
    return reuse_plan.gate_signature(path, minimum)


def refuse_unsigned(what: str, path: Path = PLAN) -> dict:
    """Exit before anything is written or spent while §0 is unsigned."""
    gate = gate_signature(path)
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {what} while {path.name} is unsigned — "
                 f"{gate['found']} signature line(s), {gate['unsigned']} blank.\n"
                 "  A model may draft a band and may not sign one. Nothing was "
                 "written and nothing was spent.\n")
    return gate
