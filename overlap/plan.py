"""
`PLAN_OVERLAP.md`'s gate, the constants of its §11, §0's lines, and the
baselines' figures §0 declares.

**The gate reads `PLAN_OVERLAP.md` and no other plan, and counts every signature
line.** The counting is `reuse/plan.py`'s, called and not copied, with this
plan's own minimum: §0 carries one line. A gate that read the wrong file would be
worse than none, because it would be believed (`CLAUDE.md`).

**The constants are fixed before any figure of the plan exists** and pinned by
`tests/test_overlap.py`, so that moving one afterwards shows in a diff.

**The baselines' figures are §0's, transcribed to the digits §0 gives them.**
They were computed while the plan was drafted, and `O-g2` recomputes every one
from the records and refuses if one differs: the drafter's arithmetic is checked,
not trusted.
"""

from __future__ import annotations

import sys
from pathlib import Path

from authorship import plan as authorship_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_OVERLAP.md")
OUT = Path("results_overlap")
MIN_SIGNATURES = 1                 # §0's table; an amendment would add its own

# --- §11: the run -----------------------------------------------------------
N = 2000
SEED = 17
MODEL = "deepseek/deepseek-v4-flash"
REASONING = {"effort": "none"}     # PLAN_REUSE.md's amendment, kept
PROMPT = "v2e"
MAX_SHOWN = 12                     # v2's neighbourhood; a test pins it to rung 2's
REPAIR_ROUNDS = 1                  # §2's K
LISTING_SEED = 17                  # the order of a repair round's list
REPS = 3                           # §2's R
SMOKE_N = 20

# --- §0's lines -------------------------------------------------------------
O_A_MAX_ALONE = 0.50               # O-a holds at a median share <= 0.50
O_B_MIN_FILL = 0.50                # O-b holds at a median share >= 0.50 ...
O_B_MIN_RUNS_WITH_ROOM = 2         # ... over the runs with room, at least two
O_C_MIN_DIRECTION = 0.70           # O-c holds at a pooled rate >= 0.70

# --- The baselines ----------------------------------------------------------
BASELINE_REPS = (1, 2, 3)          # both protocols ran three times
BASELINE_STRUCTURE = Path("results_reuse/structure.json")
BASELINE_EDGES = Path("results_edges/score.json")
BASELINE_V1E_SCORE = Path("results_authorship/score.json")
RUNG1 = Path("results/llm_run.json")
RUNG2_V1 = (Path("results2/llm_run2_n100.json"), Path("results2/llm_run2_n100_seed18.json"),
            Path("results2/llm_run2_n100_seed19.json"), Path("results2/llm_run2_n100_seed20.json"))
RUNG2_V2 = (Path("results2/llm_run2_n100_v2.json"), Path("results2/llm_run2_n100_v2_seed18.json"),
            Path("results2/llm_run2_n100_v2_seed19.json"),
            Path("results2/llm_run2_n100_v2_seed20.json"))


def v1_path(rep: int) -> Path:
    """`PLAN_REUSE.md`'s run `rep`: v1, declaration offered."""
    return reuse_plan.run_path(rep)


def v1e_path(rep: int) -> Path:
    """`PLAN_AUTHORSHIP.md`'s run `rep`: v1e, declaration imposed on every overlap."""
    return authorship_plan.run_path(rep)


# What §0 declares of the baselines. `O-g2` recomputes each and refuses if one
# differs at the digits given here. `None` is a run without room.
DECLARED_O_A = {"v1": (0.3226, 0.4839, 0.3333), "v1e": (0.8049, 0.7917, 0.9667)}
DECLARED_O_A_MEDIAN = {"v1": 0.3333, "v1e": 0.8049}
DECLARED_O_A_N100 = {"v1": (0.85, 1.00, 0.92, 1.00), "v2": (0.83, 0.78, 1.00, 0.96)}
DECLARED_O_B = {"v1": (0.3000, 0.3833, 0.7806), "v1e": (1.0000, 0.5798, None)}
DECLARED_O_B_READING = {"v1": 0.3833, "v1e": 0.7899}
DECLARED_O_B_POOLED = {"v1": 0.5175, "v1e": 0.8107}
DECLARED_O_C = {"v1": (34, 45), "v1e": (58, 84)}          # (hits, strict pairs), pooled
DECLARED_O_C_V1E_RUNS = ((22, 22), (36, 62), (0, 0))
DECLARED_V1E_INSTALLED = (27, 72, 0)
DECLARED_V1E_INSTALLED_SAME_QUEUE = 15
DECLARED_BY_QUEUE = {"v1e": {"all": (83, 239), "not_no_solapan": (27, 113)},
                     "v1": {"all": (6, 75), "accepted": (1, 64)}}
# The hidden policy written under v2e's discipline, O-g1: every rule placed
# against every earlier rule of another queue it overlaps, by layer order.
DECLARED_HIDDEN = {"declarations": 253, "installed": 199, "exempted": 41}

# The v2e texts, frozen. `O-g3` refuses if `protocol.fingerprint()` differs.
FINGERPRINT = "0acc97d11c37d769"


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
