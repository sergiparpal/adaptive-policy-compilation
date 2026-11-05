"""
The gate, the constants and the draws of `PLAN_CHANNEL.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_CHANNEL.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries its own
line and raises the minimum. The counting is `reuse/plan.py`'s, called with
this plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `channel/run.py` calls it
before it constructs a client. No flag skips it. **The free stages get the gate
too**: what it protects is the order of events, not money. A record of this
plan written before the signature would be a figure that existed before its
band (§11 of the plan).

THE CLIENT AND THE PROTOCOL ARE `PLAN_REASONED_LOOP.md`'S, IMPORTED AND NOT
RETYPED (§11, rule A): the model, temperature 0, reasoning `{"effort": "high"}`,
16,000 tokens, the retries, the pin to Baidu, the waits a call refused for the
rate is waited out through, v1b and level 3, and so `PLAN_FIRST_MATCH.md`'s.

THE ARMS (§0, §5.2). Both escalate an IMPASSE or a CONFLICT. On a case the engine
decides with a queue other than its label, the error arm, `e`, escalates always,
and the channel arm, `c`, escalates when the case's draw falls below its
coverage, 1/2. `reportable` is that rule, read on a draw alone: coverage 1 is the
error arm and needs no draw, coverage 0 is the impasse arm, and anything between
needs one. The trigger that applies it to a decision is `channel.loop.escalates`.

THE DRAWS (§2.1). Each channel run has its own: `N` floats from
`random.Random(draw_seed(name))`, one per case in arrival order, drawn before the
first case, and the smoke run its own stream. A draw belongs to its case, not to
the decision, so a run's reportable cases are fixed before it starts. A string
seed goes through SHA-512, so the draws depend on no `PYTHONHASHSEED`; they read
no label. Their digest is that of their JSON, whose floats are written in the
shortest form that reads back to the same float.

THE SEEDS (§11) were fixed by rule before any draw was computed: the next two
primes after `PLAN_REASONED_LOOP.md`'s 83. `ORDER_SEED` draws one thing, which
arm runs first, from `ARMS`, so the order of `ARMS` is pinned. The placement
round's listing keeps v2b's `LISTING_SEED`, through `blind.protocol.listing`.

THE LABELS THE TRIGGERS READ are `PLAN_REUSE.md`'s first Stage B record's, as
`PLAN_REASONED_LOOP.md`'s error trigger reads them (rule B): handed in, never the
oracle's. `CH-g1` holds them to `manual.instrument.corpus_truth`.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_channel.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact. `CH-b`'s holds at or below its line, and
every other at or above (`HOLDS_AT_OR_BELOW`).

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as
§0 numbers them. `CH-g2` recomputes the draws', the transcriber's and the
schedule's and refuses if one departs; Stage A recomputes the rest and records
whether each came back.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from reasoned_loop import plan as rl_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_CHANNEL.md")
OUT = Path("results_channel")
MIN_SIGNATURES = 1                 # §0's line

# --- §11: the client, PLAN_REASONED_LOOP.md's, and so PLAN_FIRST_MATCH.md's ---------
MODEL = rl_plan.MODEL
PROMPT = rl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = rl_plan.TEMPERATURE
REASONING = rl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = rl_plan.MAX_TOKENS
MAX_RETRIES = rl_plan.MAX_RETRIES
CALL_RETRY_WAIT = rl_plan.CALL_RETRY_WAIT
PROVIDER = rl_plan.PROVIDER
PROVIDER_NAME = rl_plan.PROVIDER_NAME
RATE_LIMITED = rl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = rl_plan.RATE_LIMIT_WAIT

# --- §11: the protocol, unchanged (§5.1) ------------------------------------------------
PROTOCOL = rl_plan.PROTOCOL        # "v1b"
LEVEL = rl_plan.LEVEL              # 3
SYSTEM_PROMPT_SHA16 = rl_plan.SYSTEM_PROMPT_SHA16

# --- §11: the arms and the causes (§5.2) --------------------------------------------------
IMPASSE, CONFLICT, ERROR = rl_plan.IMPASSE, rl_plan.CONFLICT, rl_plan.ERROR
CAUSES = rl_plan.CAUSES
ARMS = ("c", "e")                  # in this order: ORDER_SEED's draw picks from it
COVERAGE = {"c": Fraction(1, 2), "e": Fraction(1)}

# --- §11: the runs -----------------------------------------------------------------------
REPS = 3
N = reuse_plan.N                   # 2,000
SEED = reuse_plan.SEED             # 17
SMOKE_N = 30
SMOKE_ARM = "c"
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.3)

# --- §11: the seeds -------------------------------------------------------------------------
ORDER_SEED = 89
CHANNEL_SEED = 97

# --- §0: the lines --------------------------------------------------------------------------
CH_A_LINE = Fraction(9, 10)        # holds at >= : median space(B), c
CH_B_LINE = Fraction(1, 20)        # holds at <= : median space(B), e, less c's
CH_C_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, c
CH_D_LINE = Fraction(9, 10)        # holds at >= : median space(B), e
CH_E_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, e
CH_F_LINE = Fraction(3, 4)         # holds at >= : median calls, c, over e's

LINES = {"CH-a": CH_A_LINE, "CH-b": CH_B_LINE, "CH-c": CH_C_LINE, "CH-d": CH_D_LINE,
         "CH-e": CH_E_LINE, "CH-f": CH_F_LINE}
HOLDS_AT_OR_BELOW = ("CH-b",)

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
DECLARED = {
    # 1. The rare queues' tickets.
    "rare": {"ONCALL_ESCALATION": {"tickets": 7,
                                   "at": [257, 710, 954, 982, 1432, 1783, 1951],
                                   "governed": {"H04": 4, "H05": 3}},
             "SECURITY_INCIDENT": {"tickets": 20, "governed": {"H01": 9, "H02": 11}}},
    # 2. The space by true queue.
    "space_by_queue": {"SECURITY_INCIDENT": 50400, "T2_TECHNICAL": 36720,
                       "ACCOUNT_MANAGER": 16440, "T3_ENGINEERING": 8180,
                       "BILLING_SPECIALIST": 6840, "ONCALL_ESCALATION": 6300,
                       "T1_GENERAL": 5220, "SELF_SERVICE_DEFLECT": 4300},
    # 3. The channel's draws, by run.
    "draws": {
        "r1": {"reportable": 1000,
               "ONCALL_ESCALATION": {"at": [257, 1432, 1951], "by_rule": {"H04": 2, "H05": 1}},
               "SECURITY_INCIDENT": {"reportable": 11, "by_rule": {"H01": 5, "H02": 6}}},
        "r2": {"reportable": 1025,
               "ONCALL_ESCALATION": {"at": [954, 1951], "by_rule": {"H04": 2, "H05": 0}},
               "SECURITY_INCIDENT": {"reportable": 12, "by_rule": {"H01": 6, "H02": 6}}},
        "r3": {"reportable": 1015,
               "ONCALL_ESCALATION": {"at": [710, 1432, 1951], "by_rule": {"H04": 2, "H05": 1}},
               "SECURITY_INCIDENT": {"reportable": 12, "by_rule": {"H01": 5, "H02": 7}}},
    },
    # 4. The transcriber under the channel arm, by run; and H05's points.
    "transcriber_channel": {
        "r1": {"escalations": 23, "impasses": 2, "errors": 21, "calls": 45,
               "space_right": 134380, "corpus_right": 1999},
        "r2": {"escalations": 22, "impasses": 2, "errors": 20, "calls": 43,
               "space_right": 132280, "corpus_right": 1996, "recall_oncall": "2/3"},
        "r3": {"escalations": 23, "impasses": 2, "errors": 21, "calls": 45,
               "space_right": 134380, "corpus_right": 1999},
    },
    "h05_points": 2100,
    # 5. The transcriber under the error arm, as PLAN_REASONED_LOOP.md §0 lists it.
    "transcriber_error": {"escalations": 23, "calls": 45, "space_right": 134380},
    # 6. The schedule.
    "schedule": [["e", 1], ["c", 1], ["e", 2], ["c", 2], ["e", 3], ["c", 3]],
    # 8. PLAN_REASONED_LOOP.md's error runs' escalations by governing rule (the
    #    table's rows: the rule's queue, its corpus tickets, the transcriber's error
    #    escalations there and the error runs', r1 to r3); the error escalations
    #    of those runs and of the transcriber; and the range of the wrong decisions
    #    its impasse runs let stand.
    "supply": {
        "rules": {"H04": ["ONCALL_ESCALATION", 4, 1, [2, 4, 3]],
                  "H05": ["ONCALL_ESCALATION", 3, 1, [1, 2, 3]],
                  "H01": ["SECURITY_INCIDENT", 9, 1, [6, 5, 4]],
                  "H02": ["SECURITY_INCIDENT", 11, 1, [6, 1, 6]],
                  "H06": ["T3_ENGINEERING", 8, 1, [5, 2, 1]]},
        "error_escalations": {"error_runs": [62, 80, 100], "transcriber": 21},
        "impasse_wrong_decisions_stood": {"min": 379, "max": 590},
    },
}


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_REASONED_LOOP.md`'s one reasoning setting and
    one budget."""
    return rl_plan.settings()


def schedule() -> list[tuple[str, int]]:
    """§2.3: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_CHANNEL/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§2.1) -----------------------------------------------------------------------

STREAMS = ("r1", "r2", "r3", "smoke")


def draw_seed(name: str) -> str:
    """The string a stream of draws is seeded from: a channel run's, `r1` to
    `r3`, or the smoke run's."""
    if name not in STREAMS:
        raise ValueError(f"no stream of draws {name!r}: {STREAMS}")
    return f"PLAN_CHANNEL/channel/{CHANNEL_SEED}/{name}"


def draws(name: str) -> tuple[float, ...]:
    """`N` draws, one per case in arrival order, drawn before the first case.
    The smoke run reads the first `SMOKE_N` of its own stream."""
    return _stream(draw_seed(name))


@lru_cache(maxsize=None)
def _stream(seed: str) -> tuple[float, ...]:
    """Cached by the seed string itself, so that a stream is never served under
    a seed it was not drawn from."""
    rng = random.Random(seed)
    return tuple(rng.random() for _ in range(N))


def draws_digest(name: str) -> str:
    return hashlib.sha256(json.dumps(list(draws(name))).encode()).hexdigest()[:16]


def stream(arm: str, rep: int | None) -> str | None:
    """The stream a run reads: the channel arm's run `r<rep>`, or the smoke
    run's when `rep` is None. The error arm reads none."""
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    if COVERAGE[arm] >= 1:
        return None
    return "smoke" if rep is None else f"r{rep}"


def reportable(coverage: Fraction, draw: float | None) -> bool:
    """Whether a wrong decision on a case with this draw is reported, at this
    coverage (§2.1, §5.2): exactly, a float against a fraction. Coverage 1
    reports every one and needs no draw; coverage 0 reports none; anything
    between needs the case's draw."""
    if not isinstance(coverage, Fraction) or not 0 <= coverage <= 1:
        raise ValueError(f"a coverage is a fraction from 0 to 1, not {coverage!r}")
    if coverage == 1:
        return True
    if coverage == 0:
        return False
    if draw is None:
        raise ValueError(f"a channel at coverage {coverage} needs every case's draw")
    return draw < coverage


def channel_of(arm: str, rep: int | None) -> dict:
    """What a record says of its channel (rule C): the coverage, and the draws'
    seed string and digest, None for the error arm. The coverage is named the
    channel's, because rung 2's metrics carry a `coverage` of their own: the
    share of the arrivals a rule of the base matches."""
    name = stream(arm, rep)
    return {"channel_coverage": str(COVERAGE[arm]),
            "draws_seed": None if name is None else draw_seed(name),
            "draws_sha16": None if name is None else draws_digest(name),
            "draws_n": None if name is None else N}


# --- the labels the triggers read (rule B) -------------------------------------------------

def labels_path() -> Path:
    return rl_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_REASONED_LOOP.md`'s error trigger reads them."""
    return rl_plan.labels()


# --- §8 to §10: the records -------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_channel/`.

def _check(arm: str, rep: int) -> None:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    if rep not in range(1, REPS + 1):
        raise ValueError(f"no run {rep!r}: 1 to {REPS}")


def sample_path() -> Path:
    return OUT / "sample.json"


def score_path() -> Path:
    return OUT / "score.json"


def smoke_path() -> Path:
    return OUT / "loop_smoke.json"


def run_path(arm: str, rep: int) -> Path:
    _check(arm, rep)
    return OUT / f"loop_{arm}_r{rep}.json"


def tag(arm: str | None, rep: int | None) -> str:
    """A run's name: `smoke`, or the arm and the repetition."""
    if arm is None:
        return "smoke"
    _check(arm, rep)
    return f"{arm}_r{rep}"


def partial_path(name: str) -> Path:
    """Where a run appends its answers as they arrive (§5.3). Ignored by git,
    and gone once the run's record is written."""
    return OUT / f"loop_{name}.partial.jsonl"


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
