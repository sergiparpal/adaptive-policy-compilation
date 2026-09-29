"""
The gate and the constants of `PLAN_REUSE.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_REUSE.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least one. §0's table carries one today; an amendment forced by a
blocking check would carry its own, as both of the last two plans' did. A gate
that stopped at the first line would find §0 signed and report ok over an
unsigned amendment — which is why `CLAUDE.md` says not to copy
`rung2/pair_judgement.py`'s gate into a plan that may carry more than one.

Every module of this package that writes a record calls `refuse_unsigned`
before it writes anything, and `reuse/run.py` calls it before it constructs the
client. No flag skips it. **A free stage gets the gate too**: what it protects is
not money but the order of events — that §0's bands were signed before any
figure that could inform them existed (§10 of the plan).

THE CONSTANTS are §10's, fixed before any figure of the plan existed, and the
five band lines are §0's. `tests/test_reuse.py` pins every one of them, so that
moving one after a figure exists is visible in a diff: editing a line here to
turn a refutation into a hold is hard rule 6 in its purest form.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PLAN = Path("PLAN_REUSE.md")
OUT = Path("results_reuse")

SIGNATURE = "**Signed by Sergi:"
MIN_SIGNATURES = 1                 # §0's table; an amendment adds its own line
BLANKS = re.compile(r"_{3,}")

# --- §10: the protocol, fixed before any figure ------------------------------
N = 2000
SEED = 17
PROMPT = "v1"
MODEL = "deepseek/deepseek-v4-flash"
REPS = 3                           # "unless the signature says otherwise" (§2)
SMOKE_N = 20                       # §8: the smoke run, before the first full one

# --- §0: the five lines ------------------------------------------------------
U_A_MIN_REUSE = 0.30               # U-a holds at reuse_rate >= 0.30
U_B_REFUTED_AT_OR_BELOW = 0.0      # U-b holds at gap > 0, refuted at gap <= 0
U_C_MIN_SHARE = 0.60               # U-c holds at share >= 0.60
U_D_MIN_ONCALL = 1                 # U-d holds at >= 1 ONCALL escalation
U_E_MAX_CONFLICTS = 20             # U-e holds at <= 20 CONFLICTs

# §0's reading of U-a: above this share of escalations being CONFLICT, the
# record carries rung 1's caveat beside U-a. Not a band — the verdict stands.
U_A_CAVEAT_CONFLICT_SHARE = 0.25

# --- §1: the eight n=100 records Stage A reads -------------------------------
N_EIGHT = 100
EIGHT = (
    ("v1", 17, Path("results2/llm_run2_n100.json")),
    ("v1", 18, Path("results2/llm_run2_n100_seed18.json")),
    ("v1", 19, Path("results2/llm_run2_n100_seed19.json")),
    ("v1", 20, Path("results2/llm_run2_n100_seed20.json")),
    ("v2", 17, Path("results2/llm_run2_n100_v2.json")),
    ("v2", 18, Path("results2/llm_run2_n100_v2_seed18.json")),
    ("v2", 19, Path("results2/llm_run2_n100_v2_seed19.json")),
    ("v2", 20, Path("results2/llm_run2_n100_v2_seed20.json")),
)
EIGHT_SEEDS = (17, 18, 19, 20)


def run_path(rep: int) -> Path:
    """Where Stage B's run `rep` lands, and where Stage C reads it."""
    return OUT / f"run_n{N}_r{rep}.json"


SMOKE_PATH = OUT / f"run_n{SMOKE_N}_smoke.json"


def gate_signature(path: Path = PLAN) -> dict:
    """Every signature line in the plan filled in, and at least one of them."""
    lines = ([l.strip() for l in path.read_text().splitlines()
              if l.startswith(SIGNATURE)] if path.exists() else [])
    unsigned = [l for l in lines if BLANKS.search(l)]
    return {
        "what": (f"every line starting `{SIGNATURE}` in {path.name}, of which "
                 f"there must be at least {MIN_SIGNATURES}. A gate that stopped "
                 "at the first would report ok over an unsigned amendment."),
        "source": str(path),
        "found": len(lines),
        "unsigned": len(unsigned),
        "passes": len(lines) >= MIN_SIGNATURES and not unsigned,
    }


def refuse_unsigned(what: str, path: Path = PLAN) -> dict:
    """Exit before anything is written or spent while §0 is unsigned."""
    gate = gate_signature(path)
    if not gate["passes"]:
        sys.exit(f"\nREFUSED: {what} while {path.name} is unsigned — "
                 f"{gate['found']} signature line(s), {gate['unsigned']} blank.\n"
                 "  A model may draft a band and may not sign one. Nothing was "
                 "written and nothing was spent.\n")
    return gate
