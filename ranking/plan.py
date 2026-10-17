"""
The gate and the constants of `PLAN_RANKING.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_RANKING.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. The counting is
`reuse/plan.py`'s, called with this plan's path and minimum rather than copied
(§10 of the plan). If a blocking check ever forces an amendment after the
signature, the amendment carries its own line and `MIN_SIGNATURES` rises with it.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `ranking/ask.py` calls it
before it constructs the client. No flag skips it. **The free stages get the
gate too**: what it protects is not money but the order of events. Stage A's
revealed rankings and their scores are the closest thing to `M-b`'s answer that
exists without paying, and knowing them would inform `M-b`'s and `M-c`'s lines
(§7 of the plan).

THE CLIENT IS RUNG 2'S PAIRWISE JUDGE'S, IMPORTED AND NOT RETYPED (rule A),
with one setting the judge never sent: reasoning off, `PLAN_REUSE.md`'s
`REASONING`, imported from where its amendment of 2026-09-30 put it. The hosted
model has reasoned by default since then, and reasoning tokens count against
`max_tokens`; the judge's 400 would be spent before the answer. The pairwise
answers `M-d` reads were given in August without it.

THE CONSTANTS are §10's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_ranking.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **Three of the five lines are not
here**: `M-b`'s, `M-c`'s and `M-e`'s are read from the records that own them
(`signed_lines`), so that no figure of this project gets a second home in
Python. What is here is where to read them.

THE SEED. §10 fixes `PRESENTATION_SEED = 59` and two streams from it, one
string seed each: one draws the eleven presentations after the first, the other
orders each pass. CPython seeds a string through SHA-512, so no stream depends
on `PYTHONHASHSEED`.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS
from reuse import plan as reuse_plan
from rung2 import pair_judgement
from rung3 import queue_hierarchy_floor as qhf

PLAN = Path("PLAN_RANKING.md")
OUT = Path("results_ranking")
MIN_SIGNATURES = 1                 # §0's line; an amendment would add one

# --- §10: the client, rung 2's pairwise judge's, imported (rule A) -------------
MODEL = pair_judgement.MODEL
TEMPERATURE = pair_judgement.TEMPERATURE
MAX_TOKENS = pair_judgement.MAX_TOKENS
MAX_RETRIES = pair_judgement.MAX_RETRIES
REASONING = reuse_plan.REASONING   # PLAN_REUSE.md §1's amendment of 2026-09-30

# --- §10: the queues, the domain's own, in its own order ------------------------
QUEUES = tuple(ACTIONS)

# --- §10: the session ---------------------------------------------------------
PRESENTATIONS = 12                 # presentation 1 is QUEUES; eleven drawn
PASSES = 2
SMOKE_ASKS = 2                     # presentations 1 and 2, once each
PRESENTATION_SEED = 59

# --- §10: the limits ------------------------------------------------------------
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§8)
MIN_VALID_SHARE = 0.90             # M-a's validity clause, and its edge
MIN_VALID_ASKS = 4                 # below it, M-b to M-e are unadjudicable

# --- §0: the two lines that are the claims' own edges -----------------------------
M_A_MAX_SLOT_GAP = 0.05            # M-a's slot clause holds at W - A <= 0.05
M_D_MIN_GAP = 0.0                  # M-d holds at >= 0.00

# --- §0: where the other three lines are read from (rule D) ------------------------
HIERARCHY_RECORD = qhf.OUT / qhf.RECORD           # results3/queue_hierarchy_floor.json
FLOOR_RECORD = qhf.FLOOR_RECORD                   # results3/floor_by_pool.json
BLIND_SCORE = Path("results_blind/score.json")
SIGNED_CELL = ("hibrido", "corpus_test_split0")   # (pool, surface) of M-b and M-c
P_D_MARGIN = qhf.P_D_MARGIN                       # P-d's margin, as signed
LINE_PLACES = 6                                   # the precision those records publish

# --- §1: the inputs, every one of them read-only ------------------------------------
RULES = Path("results/llm_run.json")
PAIRWISE_LEARNED = Path("results2/pair_judgement_1600.json")
PAIRWISE_HIDDEN = Path("results2/pair_judgement_hidden.json")
EDGE_DROPPING = Path("results3/edge_dropping.json")   # FINDINGS3 §14: the revealed ranking

# --- §8: the sessions, in the order they run ------------------------------------------
SESSIONS = ("smoke", "session")
SAMPLE_PATH = OUT / "sample.json"
SCORE_PATH = OUT / "score.json"


def ask_path(session: str) -> Path:
    if session not in SESSIONS:
        raise ValueError(f"no session {session!r}: {SESSIONS}")
    return OUT / f"ask_{session}.json"


def partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive (§8). Ignored by git,
    and gone once the session's record is written."""
    return OUT / f"ask_{session}.partial.jsonl"


def presentation_rng() -> random.Random:
    """The stream that draws presentations 2 to 12."""
    return random.Random(f"PLAN_RANKING/presentations/{PRESENTATION_SEED}")


def order_rng(pass_no: int) -> random.Random:
    """The stream that orders one pass of the session."""
    return random.Random(f"PLAN_RANKING/order/{PRESENTATION_SEED}/pass{pass_no}")


# ---------------------------------------------------------------------------
# The three lines §0 reads rather than states
# ---------------------------------------------------------------------------

def at_record_precision(x: float) -> float:
    """A reading compared with a line read from a record is compared at the
    precision that record publishes. On the signed cell one case is 1/995,
    about a thousand units of the sixth place; on `K-b`'s units the readings
    are means of 65 shares. So the rounding decides nothing, except that a reading equal to the
    line it is compared with stays equal."""
    return round(x, LINE_PLACES)


def signed_lines(hierarchy: Path | None = None, blind_score: Path | None = None
                 ) -> dict[str, Any]:
    """`M-b`'s, `M-c`'s and `M-e`'s lines, read from the records that own them,
    with where each came from. A record that is missing or lacks the cell is a
    failure of the instrument, and the caller stops."""
    hierarchy = hierarchy or HIERARCHY_RECORD
    blind_score = blind_score or BLIND_SCORE
    pool, surface = SIGNED_CELL
    rec = json.loads(hierarchy.read_text())
    row = next(r for r in rec["rows"] if r.get("tiebreak") == "born_at"
               and r["pool"] == pool and r["surface"] == surface)
    blind = json.loads(blind_score.read_text())
    k_b = blind["verdicts"]["K-b"]
    return {
        "M-b": {"line": at_record_precision(row["born_at_floor"] + P_D_MARGIN),
                "floor": row["born_at_floor"], "margin": P_D_MARGIN,
                "source": f"{hierarchy}::rows[born_at, {pool}, {surface}].born_at_floor "
                          "+ rung3.queue_hierarchy_floor.P_D_MARGIN",
                "holds_when": "median > line"},
        "M-c": {"line": row["stage_c"],
                "source": f"{hierarchy}::rows[born_at, {pool}, {surface}].stage_c",
                "holds_when": "median >= line"},
        "M-e": {"line": k_b["reading"], "units": k_b["units"],
                "source": f"{blind_score}::verdicts.K-b.reading",
                "holds_when": "median > line"},
    }


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
