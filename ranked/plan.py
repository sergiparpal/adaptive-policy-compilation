"""
The gate, the constants, the schedule and the declared figures of
`PLAN_RANKED.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_RANKED.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries its own
line and raises the minimum. The counting is `reuse/plan.py`'s, called with this
plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `ranked/run.py` and `ranked/ask.py`
call it before they construct a client. No flag skips it. **The free stages get
the gate too**: what it protects is the order of events, not money (§11).

THE CLIENT, THE LEVEL, THE TEXTS, THE DRAWS AND THE AT-ONCE ASKS ARE
`PLAN_CORRECTIONS.md`'S ARM L'S, IMPORTED AND NOT RETYPED (§2.12, §2.6): the
model, temperature 0, reasoning `{"effort": "high"}`, 16,000 tokens, the retries
and the waits, DeepInfra's fp8 endpoint with no fallback, level 1's catalogue,
report R1, the channel at coverage 1/2 over `PLAN_CHANNEL.md`'s draws, and the
checkpoints, the budget and the workers of the at-once asks.

THE ARMS (§5). Both are that plan's arm L. `l` is it, called and not changed, on
rung 2's engine. `k` is the same loop on `ranked/engine.py`'s engine, which is
rung 2's but for one thing: where rung 2's would return CONFLICT, it decides by
the ranking its own votes choose. Everything the proposer is handed is `l`'s in
both.

THE ENGINE'S RULE (§2.2 to §2.4) is fixed here and nowhere else: every citation
a vote, the earliest of the rankings that agree with the most votes, and the
ranking deciding only what rung 2's engine would leave in CONFLICT.
`tests/test_ranked.py` pins it.

THE SEED (§2.5) was fixed by rule before any draw was computed: the next prime
after `PLAN_CORRECTIONS.md`'s 109. `ORDER_SEED` draws one thing, which arm runs
first, from `ARMS`, so the order of `ARMS` is pinned.

THE LINES are §0's, fixed before any figure of the plan existed. **They are
fractions, or counts of runs**, and every comparison with them is exact.

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as
§0 numbers them. `RK-g2` recomputes them and refuses if one departs; Stage A
records them.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from corrections import plan as cr_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_RANKED.md")
OUT = Path("results_ranked")
MIN_SIGNATURES = 1                 # §0's line

# --- §2.12: the client, PLAN_CORRECTIONS.md's, pin included ------------------------------
MODEL = cr_plan.MODEL
TEMPERATURE = cr_plan.TEMPERATURE
REASONING = cr_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = cr_plan.MAX_TOKENS    # 16,000, the loop's
MAX_RETRIES = cr_plan.MAX_RETRIES
CALL_RETRY_WAIT = cr_plan.CALL_RETRY_WAIT
RATE_LIMITED = cr_plan.RATE_LIMITED
RATE_LIMIT_WAIT = cr_plan.RATE_LIMIT_WAIT
PROVIDER = cr_plan.PROVIDER        # {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
PROVIDER_NAME = cr_plan.PROVIDER_NAME

# --- §5: the protocol, PLAN_CORRECTIONS.md's arm L's -------------------------------------
LEVEL = cr_plan.LEVEL              # the manual's level 1: the catalogue
TEXTS_OF = cr_plan.LABELLED        # both arms send that plan's arm L's texts, report included
IMPASSE, CONFLICT, ERROR = cr_plan.IMPASSE, cr_plan.CONFLICT, cr_plan.ERROR
COVERAGE = cr_plan.COVERAGE        # 1/2, PLAN_CHANNEL.md's channel arm's

# --- §5: the arms ---------------------------------------------------------------------------
ARMS = ("l", "k")                  # the control, then the ranked arm; ORDER_SEED picks from it
CONTROL = "l"                      # PLAN_CORRECTIONS.md's arm L, on rung 2's engine
RANKED = "k"                       # the same loop on the ranked engine
ENGINE = {"l": "rung2", "k": "ranked"}

# --- §2.2 to §2.4: the ranked engine's rule --------------------------------------------------
VOTE = "every citation of a born rule's answer, a rule and a side, counted alike"
TIE = "the earliest of the most agreeing, in itertools.permutations(ACTIONS)"
DECIDES = "only where rung 2's engine would return CONFLICT"
N_RANKINGS = 40320                 # 8!
SECURITY = "SECURITY_INCIDENT"
ONCALL = "ONCALL_ESCALATION"

# --- §2.5: the runs --------------------------------------------------------------------------
REPS = 3
N = cr_plan.N                      # 2,000
SEED = cr_plan.SEED                # 17
SMOKE_N = 30
SMOKE_ARMS = ("l", "k")            # §2.9: L, then K
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = cr_plan.MAX_CONSECUTIVE_FAILURES   # an outage, not answers

# --- §2.5: the seed ----------------------------------------------------------------------------
ORDER_SEED = 113

# --- §2.6: the at-once asks, PLAN_CORRECTIONS.md §2.4's ------------------------------------------
CHECKPOINTS = cr_plan.CHECKPOINTS          # 10, 20, 40, 80, 160 and 320 labels, and all of them
ASKS_PER_CHECKPOINT = cr_plan.ASKS_PER_CHECKPOINT
PRIOR_ASKS = cr_plan.PRIOR_ASKS            # with no label, right after the smoke session
SMOKE_ASKS = cr_plan.SMOKE_ASKS            # one with no label, one on L's smoke labels
WORKERS = cr_plan.WORKERS                  # harness/ask_pool.py, asks only
MAX_REASKS = cr_plan.MAX_REASKS
AT_ONCE_MAX_TOKENS = cr_plan.AT_ONCE_MAX_TOKENS

# --- §0: the lines ---------------------------------------------------------------------------
RK_B_LINE = Fraction(1, 10)        # holds at >= : median space(B), K, less L's
RK_C_LINE = Fraction(1, 2)         # holds at >= : median recall of SECURITY_INCIDENT, K
RK_D_LINE = Fraction(0)            # holds at >= : median over K's runs of space(B) - space(A(r))
RK_E_LINE = Fraction(1, 2)         # holds at >= : median share right of the cases the ranking took
RK_F_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, K

LINES = {"RK-b": RK_B_LINE, "RK-c": RK_C_LINE, "RK-d": RK_D_LINE, "RK-e": RK_E_LINE,
         "RK-f": RK_F_LINE}
ROWS = ("RK-a", "RK-b", "RK-c", "RK-d", "RK-e", "RK-f")
# RK-a reads a count of runs: every complete K run puts SECURITY_INCIDENT first.

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
# Every list is by run or by draw: r1, r2, r3. Points are of the space's 134,400.
DECLARED = {
    # 2. The two designs set aside, under the transcriber and each draw: the points the
    #    final base decides right, the escalations, and the queue the ranking ends with
    #    last. Beside them, rung 2's engine under the same proposer.
    "set_aside": {
        "every citation": {"right": [120720, 118620, 120720], "escalations": [47, 51, 63],
                           "last": ["ACCOUNT_MANAGER"] * 3},
        "each pair of regions once a side": {
            "right": [129680, 127580, 120720], "escalations": [39, 39, 64],
            "last": ["SELF_SERVICE_DEFLECT", "SELF_SERVICE_DEFLECT", "ACCOUNT_MANAGER"]},
        "rung 2": {"right": [134380, 132280, 134380], "escalations": [23, 22, 23]}},
    # 3. The closed L runs' final bases, replayed under each design: the points decided
    #    right. `as recorded` is rung 2's engine, the run itself.
    "final_bases": {"as recorded": [75900, 56725, 75509],
                    "every citation": [100735, 92210, 80470],
                    "each pair of regions once a side": [101310, 88450, 80430],
                    "arm K's engine": [105215, 93545, 81822]},
    # 4. Arm K's engine on the closed L runs, after every birth: its peak, the birth it
    #    comes at, and the recall of two queues at the end, as fractions.
    "as_it_went": {"peak": [109560, 106835, 95273], "peak_birth": [219, 77, 81],
                   "SECURITY_INCIDENT": ["5/6", "2/3", "13/42"],
                   "ONCALL_ESCALATION": ["2/3", "3/5", "103/140"]},
    # 5. The cases the closed L runs escalated as a CONFLICT: how many, how many the
    #    ranking of the votes so far decides right, and at how many the proposer's first
    #    call named the true queue.
    "asked_conflicts": {"cases": [125, 118, 74], "ranking_right": [74, 64, 55],
                        "first_call_right": [36, 49, 39]},
    # 6. On the corpus, with the truth: [arrivals, reportable under the draws of r1, r2
    #    and r3]. Counted for the first draft's RK-e, which no row reads now.
    "pair_arrivals": {
        # churn tickets, governed by H13 or H14, that H15 or H17 also matches
        "churn_that_t3_routing_matches": [5, [4, 1, 2]],
        # severity-1 tickets of T3_ENGINEERING, governed by H06 or H07, that H13 or H14 matches
        "severity_1_t3_that_churn_matches": [4, [2, 4, 2]]},
    # 7. The schedule.
    "schedule": [["l", 1], ["k", 1], ["l", 2], ["k", 2], ["l", 3], ["k", 3]],
}


def settings() -> dict:
    """What every loop request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_CORRECTIONS.md`'s, which is `PLAN_PLACEMENT.md`'s."""
    return cr_plan.settings()


def at_once_settings() -> dict:
    """The at-once asks' request: the loop's, with their own budget (§2.6)."""
    return cr_plan.at_once_settings()


def schedule() -> list[tuple[str, int]]:
    """§2.5: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_RANKED/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§5): PLAN_CHANNEL.md's, called -------------------------------------------------

STREAMS = cr_plan.STREAMS          # ("r1", "r2", "r3", "smoke")
draw_seed = cr_plan.draw_seed
draws = cr_plan.draws
draws_digest = cr_plan.draws_digest
reportable = cr_plan.reportable


def _arm(arm: str) -> None:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")


def stream(arm: str, rep: int | None) -> str:
    """The stream a run reads: `r<rep>` for run `rep` of either arm, the smoke
    runs' when `rep` is None."""
    _arm(arm)
    return "smoke" if rep is None else f"r{rep}"


def channel_of(arm: str, rep: int | None) -> dict:
    """What a record says of its channel: the coverage, and the draws' seed
    string and digest."""
    name = stream(arm, rep)
    return {"channel_coverage": str(COVERAGE), "draws_seed": draw_seed(name),
            "draws_sha16": draws_digest(name), "draws_n": N}


# --- the labels (§4) -----------------------------------------------------------------------------

def labels_path() -> Path:
    return cr_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_CHANNEL.md`'s trigger reads them."""
    return cr_plan.labels()


# --- §2.6: the checkpoints -------------------------------------------------------------------------

checkpoints = cr_plan.checkpoints


# --- §8 to §10: the records ----------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_ranked/`.

def _check(arm: str, rep: int) -> None:
    _arm(arm)
    if rep not in range(1, REPS + 1):
        raise ValueError(f"no run {rep!r}: 1 to {REPS}")


def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def smoke_path(arm: str) -> Path:
    _arm(arm)
    return OUT / f"loop_smoke_{arm}.json"


def run_path(arm: str, rep: int) -> Path:
    _check(arm, rep)
    return OUT / f"loop_{arm}_r{rep}.json"


def tag(arm: str, rep: int | None) -> str:
    """A run's name: `smoke_<arm>`, or the arm and the repetition."""
    if rep is None:
        _arm(arm)
        return f"smoke_{arm}"
    _check(arm, rep)
    return f"{arm}_r{rep}"


def partial_path(name: str) -> Path:
    """Where a run appends its answers as they arrive. Ignored by git, and gone
    once its record is written."""
    return OUT / f"loop_{name}.partial.jsonl"


def session_of(arm: str, rep: int) -> str:
    """The at-once session of a run: every run of either arm has one (§2.6)."""
    return tag(arm, rep)


def sessions() -> tuple[str, ...]:
    """Every at-once session, in §9's order: the smoke session, the asks with no
    label, and each run's session after its run."""
    return ("smoke", "prior", *(session_of(a, r) for a, r in schedule()))


def ask_path(session: str) -> Path:
    if session not in sessions():
        raise ValueError(f"no session {session!r}: {sessions()}")
    return OUT / f"atonce_{session}.json"


def ask_partial_path(session: str) -> Path:
    """Where a session appends its answers as they arrive. Ignored by git, and
    gone once its record is written."""
    ask_path(session)                          # refuses a session the plan does not have
    return OUT / f"atonce_{session}.partial.jsonl"


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
