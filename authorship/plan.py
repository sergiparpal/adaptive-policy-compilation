"""
`PLAN_AUTHORSHIP.md`'s gate, the constants of its §11, and §0's lines.

**The gate reads `PLAN_AUTHORSHIP.md` and no other plan, and counts every
signature line.** The counting is `reuse/plan.py`'s, called and not copied, with
this plan's own minimum: §0 carries one line. A gate that read the wrong file
would be worse than none, because it would be believed (`CLAUDE.md`).

**The constants are fixed before any figure of the plan exists** and pinned by
`tests/test_authorship.py`, so that moving one afterwards shows in a diff.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_AUTHORSHIP.md")
OUT = Path("results_authorship")
MIN_SIGNATURES = 1                 # §0's table; an amendment would add its own

# --- §11: the run -----------------------------------------------------------
N = 2000
SEED = 17
MODEL = "deepseek/deepseek-v4-flash"
REASONING = {"effort": "none"}     # PLAN_REUSE.md's amendment, kept
PROMPT = "v1e"
MAX_SHOWN = 12                     # v1's neighbourhood; a test pins it to rung 2's
REPAIR_ROUNDS = 1                  # §2's K
LISTING_SEED = 17                  # the order of a repair round's list
REPS = 3                           # §2's R
SMOKE_N = 20

# --- §0's lines -------------------------------------------------------------
E_A_MIN_NESTED = 0.05              # E-a holds at nested share >= 0.05
E_B_MAX_SILENT = 0.45              # E-b holds at silent error <= 0.45 ...
E_B_MIN_COVERAGE = 0.90            # ... and coverage >= 0.90, both on the median
E_C_MIN_FILL = 0.50                # E-c holds at a share of the room >= 0.50
E_D_MIN_CONTRADICTIONS = 1         # E-d holds at >= 1 contradice_subsuncion, pooled

# --- The baseline: PLAN_REUSE.md's three runs, and what reads them -----------
BASELINE_REPS = (1, 2, 3)
BASELINE_STRUCTURE = Path("results_reuse/structure.json")
BASELINE_EDGES = Path("results_edges/score.json")
RUNG1 = Path("results/llm_run.json")

# What §0 declares of the baseline, to four decimals. `E-g2` recomputes each from
# the records and refuses if one differs: the drafter's arithmetic is checked,
# not trusted.
DECLARED_DISTINCT_NESTING = (0.0160, 0.0277, 0.0043)
DECLARED_FILL_SPACE = (0.3000, 0.3833, 0.7806)
DECLARED_FILL_CORPUS = (0.2326, 0.3636, 0.4429)

# The v1e texts, frozen. `E-g3` refuses if `protocol.fingerprint()` differs.
FINGERPRINT = "72b611ad60c0278e"


def baseline_path(rep: int) -> Path:
    return reuse_plan.run_path(rep)


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
