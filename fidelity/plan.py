"""
The gate and the constants of `PLAN_FIDELITY.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_FIDELITY.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). It is the gate that reads every line instead of the first, and
a second copy of it would be one more place for it to drift. If a blocking check
ever forces an amendment, the amendment carries its own line and
`MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `fidelity/ask.py` calls it before it
constructs the client. No flag skips it. **The free stages get the gate too**:
what it protects is not money but the order of events (§10 of the plan).

THE CONSTANTS are §10's, fixed before any figure of the plan existed, and the
five band lines are §0's. `tests/test_fidelity.py` pins every one of them, so
that moving one after a figure exists is visible in a diff.

THE SEEDS. §10 fixes `SAMPLE_SEED = 41` and `ORDER_SEED = 43`. How a seed becomes
one stream per run, or per session and pass, is fixed here, before any draw
existed: one string seed per stream. CPython seeds a string through SHA-512, so
no stream depends on `PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

from reuse import plan as reuse_plan

PLAN = Path("PLAN_FIDELITY.md")
OUT = Path("results_fidelity")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the inputs ---------------------------------------------------------
RUNS = (1, 2, 3)                   # Stage B of PLAN_REUSE.md, one base each
N = 2000
SEED = 17


def run_path(run: int) -> Path:
    """A Stage B record of PLAN_REUSE.md: an input, never an output (rule B)."""
    return Path(f"results_reuse/run_n{N}_r{run}.json")


# --- §10: the client, Stage B's unchanged (§1) --------------------------------
MODEL = "deepseek/deepseek-v4-flash"
PROMPT = "v1"
REASONING = {"effort": "none"}

# --- §10: the sample ---------------------------------------------------------
DRAWS = 2
PER_RUN = 600
TICKET_ONLY_PER_RUN = 100
SMOKE_PER_ARM = 5
SAMPLE_SEED = 41
ORDER_SEED = 43

# --- §10: the limits ---------------------------------------------------------
MAX_INVALID_SHARE = 0.05           # above it, a run's value is undefined (§5.5)
MIN_SILENT_ERRORS = 100            # F-d's population, per run's draw (F-g3)

# --- §0: the five lines ------------------------------------------------------
F_A_MAX_GAP = 0.05                 # F-a holds at S − A <= 0.05
F_B_MIN_GAP = 0.10                 # F-b holds at S − A >= 0.10
F_C_REFUTED_AT_OR_BELOW = 0.0      # F-c holds at > 0, refuted at <= 0
F_D_MIN_SHARE = 0.60               # F-d holds at >= 0.60
F_E_MIN_ONCALL = 1                 # F-e holds at >= 1 ticket

ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"
RARE = (ONCALL, SECURITY)

# --- §8: the sessions, in the order they run ----------------------------------
SESSIONS = ("smoke", "births", "base1", "base2", "base3", "ticket_only")
SAMPLE_PATH = OUT / "sample.json"
SCORE_PATH = OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§5.8). Ignored by
    git, and gone once the session's record is written."""
    return OUT / f"ask_{session}.partial.jsonl"


def sample_rng(run: int) -> random.Random:
    """The uniform draw of run `run` (§2.3): one stream per run."""
    return random.Random(f"PLAN_FIDELITY/sample/{SAMPLE_SEED}/run{run}")


def order_rng(session: str, pass_no: int) -> random.Random:
    """The order of one pass of one session (§2.2)."""
    return random.Random(f"PLAN_FIDELITY/order/{ORDER_SEED}/{session}/pass{pass_no}")


def gate_signature(path: Path = PLAN) -> dict:
    """Every signature line of this plan filled in, and at least one."""
    return reuse_plan.gate_signature(path, minimum=MIN_SIGNATURES)


def refuse_unsigned(what: str, path: Path = PLAN) -> dict:
    """Exit before anything is measured, written or spent while §0 is unsigned."""
    gate = gate_signature(path)
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {what} while {path.name} is unsigned — "
                 f"{gate['found']} signature line(s), {gate['unsigned']} blank.\n"
                 "  A model may draft a band and may not sign one. Nothing was "
                 "written and nothing was spent.\n")
    return gate
