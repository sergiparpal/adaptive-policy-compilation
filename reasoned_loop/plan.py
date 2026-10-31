"""
The gate and the constants of `PLAN_REASONED_LOOP.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_REASONED_LOOP.md` that starts `**Signed by Sergi:` must be filled in, and
there must be at least `MIN_SIGNATURES`: two since 2026-10-31, §0's and the
amendment to §5.5's. The counting is `reuse/plan.py`'s, called with this plan's
path and minimum rather than copied (§11 of the plan). The amendment carries its
own line, and `MIN_SIGNATURES` rose with it, so neither can go missing.

Every module of this package that writes a record calls `refuse_unsigned`
before it measures, builds or writes anything, and `reasoned_loop/run.py` calls
it before it constructs a client. No flag skips it. **The free stages get the
gate too**: what it protects is the order of events, not money. A record of
this plan written before the signature would be a figure that existed before
its band (§11 of the plan).

THE CLIENT IS `PLAN_FIRST_MATCH.md`'S REASONING ARM'S, IMPORTED AND NOT RETYPED
(rule A of the plan): the model, temperature 0, reasoning `{"effort": "high"}`,
16,000 tokens, the retries and the pin to Baidu. One setting serves every call,
the draft's and the placement's (§2.4).

A RATE LIMIT IS AN OUTAGE, NOT AN ANSWER (§5.5's amendment, 2026-10-31). The
smoke run met HTTP 429 from the pinned provider on every launch. A call whose
every attempt was refused for the rate is asked again after each wait of
`RATE_LIMIT_WAIT`, and if it is still refused the run stops without recording
it. `RATE_LIMITED` is how `harness/call_record.py` keeps such an attempt: the
class `openai` raises on HTTP 429.

THE LABELS THE ERROR TRIGGER READS are `PLAN_REUSE.md`'s first Stage B
record's, as v2e's and v2b's loops read theirs (rule B): handed in, never the
oracle's. `RL-g1` checks them against level 3's text, case by case.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_reasoned_loop.py` pins every one of them, so that
moving one after a figure exists is visible in a diff. **The lines are
fractions**, and every comparison with them is exact.

`DECLARED` holds the figures §0 lists as computed while drafting, as
`blind/plan.py`'s `DECLARED` holds that plan's. `RL-g2` recomputes the
transcriber's and the hidden policy's and refuses if one departs; Stage A
recomputes the rest and records whether each came back.

THE SEED. §11 fixes `ORDER_SEED = 83`. It draws one thing, which arm runs
first, from a string seed: CPython seeds a string through SHA-512, so the
order depends on no `PYTHONHASHSEED`. The placement round's listing order is
v2b's, `blind.protocol.listing`'s, and keeps its seed.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

from authorship import gates as egates
from first_match import plan as fm_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_REASONED_LOOP.md")
OUT = Path("results_reasoned_loop")
MIN_SIGNATURES = 2                 # §0's line and §5.5's amendment's

# --- §11: the client, PLAN_FIRST_MATCH.md's reasoning arm ----------------------------
MODEL = fm_plan.MODEL
PROMPT = fm_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = fm_plan.TEMPERATURE
REASONING = fm_plan.REASONING_ON   # {"effort": "high"}, on every call (§2.4)
MAX_TOKENS = fm_plan.MAX_TOKENS_REASONING
MAX_RETRIES = fm_plan.MAX_RETRIES
CALL_RETRY_WAIT = fm_plan.CALL_RETRY_WAIT
PROVIDER = fm_plan.PROVIDER
PROVIDER_NAME = fm_plan.PROVIDER_NAME

# --- §5.5's amendment, 2026-10-31: a rate limit is an outage, not an answer ------------
RATE_LIMITED = "RateLimitError"    # the class `openai` raises on HTTP 429, as call_record keeps it
RATE_LIMIT_WAIT = (60, 120, 240, 480, 960)   # seconds before a refused call is asked again

# --- §11: the protocol ----------------------------------------------------------------
PROTOCOL = "v1b"
LEVEL = 3
SYSTEM_PROMPT_SHA16 = "7b883f03a863d647"   # §5.1: PLAN_MANUAL.md's level-3 loop prompt

# --- §11: the arms and their triggers (§5.3) -----------------------------------------
IMPASSE, CONFLICT, ERROR = "IMPASSE", "CONFLICT", "ERROR"
CAUSES = (IMPASSE, CONFLICT, ERROR)
ARMS = ("i", "e")
TRIGGERS = {"i": (IMPASSE, CONFLICT), "e": (IMPASSE, CONFLICT, ERROR)}

# --- §11: the runs -----------------------------------------------------------------------
REPS = 3
N = reuse_plan.N                   # 2,000
SEED = reuse_plan.SEED             # 17
SMOKE_N = 30
SMOKE_ARM = "e"
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.5)
ORDER_SEED = 83

# --- §11: the limits ------------------------------------------------------------------
MIN_ESCALATIONS = 60               # RL-a, pooled
MIN_UNITS = 20                     # RL-e and RL-f
COVER_BEFORE = 200                 # RL-b: within the first tenth of the arrivals

# --- §0: the lines ----------------------------------------------------------------------
RL_A_LINE = Fraction(9, 10)        # holds at >= : right drafts over escalations, pooled
RL_B_LINE = Fraction(2, 3)         # holds at >= : share of i's runs covering before 200
RL_C_LINE = Fraction(1, 10)        # holds at >= : median space(e) − median space(i)
RL_D_LINE = Fraction(9, 10)        # holds at >= : median space(e)
RL_E_LINE = Fraction(9, 10)        # holds at >= : direction by older rule, pooled
RL_F_LINE = Fraction(0)            # holds at >= : direction less the Stage C ranking's
RL_G_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, e

LINES = {"RL-a": RL_A_LINE, "RL-b": RL_B_LINE, "RL-c": RL_C_LINE, "RL-d": RL_D_LINE,
         "RL-e": RL_E_LINE, "RL-f": RL_F_LINE, "RL-g": RL_G_LINE}

# --- §0: what the drafter computed while drafting ----------------------------------------
DECLARED = {
    "h29": {"tickets": 163, "first": [1, 21, 50, 64, 86]},
    "rare": {"ONCALL_ESCALATION": {"tickets": 7,
                                   "at": [257, 710, 954, 982, 1432, 1783, 1951],
                                   "governed": {"H04": 4, "H05": 3}},
             "SECURITY_INCIDENT": {"tickets": 20},
             "ACCOUNT_MANAGER": {"tickets": 109},
             "T3_ENGINEERING": {"tickets": 117}},
    "transcriber": {
        "i": {"escalations": [[0, IMPASSE, "H13"], [1, IMPASSE, "H29"]],
              "rules": ["H13", "H29"], "space_right": 14820, "corpus_right": 298},
        "e": {"escalations": 23, "impasses": 2, "errors": 21, "last": 954,
              "rules": 23, "not_written": ["H21", "H22", "H23", "H25", "H27", "H28"],
              "declarations": 148, "accepted": 148, "space_right": 134380,
              "k_a": "1/20", "crossing": 64, "strict": 59, "units": 15},
    },
    "hidden": {"born": 29, "declarations": 253, "installed": 199},
    # The rules PLAN_REASONED_RULE.md's two rule arms wrote, by governing rule:
    # [answers, the reasoning rule arm's governing region, inside it, the rule
    # arm's governing region], over both passes.
    "rules_written": {"H29": [28, 12, 16, 1], "H28": [16, 10, 6, 0],
                      "H16": [34, 23, 10, 4], "H18": [40, 19, 15, 0],
                      "H12": [16, 9, 7, 0]},
    "catch_all_without_reasoning": {"answers": 6, "of": 342, "under_other_rules": 5},
    # Computed while the package was written, after the draft and before the
    # signature, and declared by the erratum that lands with it: RL-e's and
    # RL-f's statistics on the transcriber's error run, one run, every edge
    # placed by the list's order.
    "transcriber_direction": {"e": {"units": 15, "hits": 55, "strict": 59,
                                    "reading": "71/75", "ranking": "403/450"},
                              "i": {"units": 0}},
}


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin (§1, §2.4): one reasoning setting and one budget."""
    return {"reasoning": json.loads(json.dumps(REASONING)), "max_tokens": MAX_TOKENS}


def schedule() -> list[tuple[str, int]]:
    """§2.6: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_REASONED_LOOP/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the labels the error trigger reads (rule B) -------------------------------------------

def labels_path() -> Path:
    return reuse_plan.run_path(1)


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record."""
    return egates.labels_of(egates.load(labels_path()))


# --- §8 to §10: the records -------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_reasoned_loop/`.

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
    """Where a run appends its answers as they arrive (§5.5). Ignored by git,
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
