"""
The gate and the constants of `PLAN_MANUAL.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_MANUAL.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§11 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `manual/ask.py` and
`manual/run.py` call it before they construct a client. No flag skips it. **The
free stages get the gate too**: what it protects is not money but the order of
events (§8 of the plan).

THE CLIENT IS `PLAN_REUSE.md`'S. The model and the reasoning setting are
imported from `reuse.plan`, where §1's amendment of 2026-09-30 put the second:
the hosted model reasons by default, and reasoning tokens count against
`max_tokens`. The loop's own client is `OpenRouterProposer2`, untouched but for
its system prompt.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_manual.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact: each statistic of §0 is a ratio of integer
counts.

THE ORDER. §2.5: one order of the four levels is drawn per shape at
`ORDER_SEED`, from a string seed, and rotated one place per compile pass or per
loop repetition. CPython seeds a string through SHA-512, so no order depends on
`PYTHONHASHSEED`.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from reuse import plan as reuse_plan

from . import levels

PLAN = Path("PLAN_MANUAL.md")
OUT = Path("results_manual")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §11: the client ----------------------------------------------------------
MODEL = reuse_plan.MODEL
REASONING = reuse_plan.REASONING   # PLAN_REUSE.md §1's amendment of 2026-09-30
TEMPERATURE = 0
PROMPT = "v1"                      # the loop's prompt version, with the manual inserted
COMPILE_MAX_TOKENS = 16000
COMPILE_MAX_RETRIES = 2

# --- §5 and §11: the texts, by digest -------------------------------------------
LEVELS = levels.LEVELS
DIGESTS = {
    "catalogue": "95cec2fe42aeacebc77c642a634e5fc8d3024da9d6f133aff22cb09b406edff1",
    "prose": "dc63a2a144271372ec70af6a9102e3f0996960cdcc75751c1549643ca7438330",
    "rules": "bcc9f9818caa18039346e610ad73f30c57b49957dab51f04dfd3b02717c47dcd",
}

# --- §11: the loop, PLAN_REUSE.md's ----------------------------------------------
N = reuse_plan.N
SEED = reuse_plan.SEED
REPS = reuse_plan.REPS
SMOKE_N = reuse_plan.SMOKE_N
LOOP_SMOKE_LEVEL = 3               # the longest prompt

# --- §11: the compile session ------------------------------------------------------
ASKS = 5                           # passes; one ask per level in each
COMPILE_SESSIONS = ("smoke", "session")

# --- §11: the order ------------------------------------------------------------------
ORDER_SEED = 61

# --- §11: the limits -----------------------------------------------------------------
MIN_VALID_ASKS = 3                 # below it, a row reading that level is unadjudicable
MIN_RUNS = 2                       # likewise for the loop's runs
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§9)

# --- §0: the lines, exact --------------------------------------------------------------
G_A_LINE = Fraction(95, 100)       # holds at >= : C_3's median space
G_B_LINE = Fraction(1, 10)         # holds at >= : C_1 - C_0, recall of the two queues
G_C_LINE = Fraction(1, 2)          # holds ABOVE : L_3's median K-a
G_D_LINE = Fraction(1, 10)         # holds at >= : C_3 - L_3, space
G_E_LINE = Fraction(1, 10)         # holds at >= : L_2 - L_0, corpus
G_F_LINE = Fraction(1, 10)         # holds at >= : prop(L_1) - prop(L_0)

# --- §1: the inputs, every one of them read-only ------------------------------------------
REUSE_RUNS = tuple(reuse_plan.run_path(r) for r in range(1, reuse_plan.REPS + 1))
EDGES_SCORE = Path("results_edges/score.json")     # W-d: the final bases, read whole
BLIND_SCORE = Path("results_blind/score.json")     # K-a's baselines

# --- §8-§10: the records ---------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in `results_manual/`.

def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def loop_smoke_path() -> Path:
    return OUT / "loop_smoke.json"


def compile_path(session: str) -> Path:
    if session not in COMPILE_SESSIONS:
        raise ValueError(f"no compile session {session!r}: {COMPILE_SESSIONS}")
    return OUT / f"compile_{session}.json"


def compile_partial(session: str) -> Path:
    """Where a compile session appends its answers as they arrive (§9). Ignored
    by git, and gone once the session's record is written."""
    return OUT / f"compile_{session}.partial.jsonl"


def loop_path(level: int, rep: int) -> Path:
    if level not in LEVELS or rep not in range(1, REPS + 1):
        raise ValueError(f"no loop run L{level} r{rep}")
    return OUT / f"loop_L{level}_r{rep}.json"


# ---------------------------------------------------------------------------
# §2.5: the order of Stage B
# ---------------------------------------------------------------------------

def rotate(order: list[int], k: int) -> list[int]:
    k %= len(order)
    return order[k:] + order[:k]


def base_order(shape: str) -> list[int]:
    """The order of the four levels drawn for one shape."""
    if shape not in ("compile", "loop"):
        raise ValueError(f"no shape {shape!r}")
    order = list(LEVELS)
    random.Random(f"PLAN_MANUAL/{shape}/{ORDER_SEED}").shuffle(order)
    return order


def compile_schedule(session: str) -> list[tuple[int, int]]:
    """(pass, level) in the order they are asked. The smoke asks each level
    once, in the drawn order."""
    base = base_order("compile")
    if session == "smoke":
        return [(1, lv) for lv in base]
    if session != "session":
        raise ValueError(f"no compile session {session!r}")
    return [(p, lv) for p in range(1, ASKS + 1) for lv in rotate(base, p - 1)]


def loop_schedule() -> list[tuple[int, int]]:
    """(rep, level) in the order the twelve runs are made."""
    base = base_order("loop")
    return [(r, lv) for r in range(1, REPS + 1) for lv in rotate(base, r - 1)]


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

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
