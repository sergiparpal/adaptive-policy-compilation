"""
The gate, the constants, the draws and the declared figures of `PLAN_IMPASSE.md`,
in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_IMPASSE.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries its own
line and raises the minimum. The counting is `reuse/plan.py`'s, called with this
plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `impasse/run.py` calls it before it
constructs a client. No flag skips it. **The free stages get the gate too**: what
it protects is the order of events, not money. A record of this plan written
before the signature would be a figure that existed before its band (§11).

THE CLIENT IS `PLAN_PLACEMENT.md`'S, IMPORTED AND NOT RETYPED, PIN INCLUDED (§1,
§2.6, §2.7, rule A): the model, temperature 0, reasoning `{"effort": "high"}`,
16,000 tokens, the retries, the waits a call refused for the rate is waited out
through, and DeepInfra's fp8 endpoint with no fallback. `PROVIDER_NAME` is what
a response's `provider` field is expected to say, and the smoke run holds it to
what it says.

THE ARMS (§0, §5). Both run `PLAN_PLACEMENT.md`'s v1c: `PLAN_CHANNEL.md`'s channel
arm at coverage 1/2 with v1c's placement round. An arm is named by its protocol:
`v1c`, that plan's arm, called and not changed; and `v1n`, v1c with
`PLAN_CAUSE.md`'s arm `i`'s paragraph at the first call of an escalation whose
cause is an IMPASSE (`impasse/protocol.py`).

THE DRAWS (§5.3) are `PLAN_CHANNEL.md`'s, called through `placement.plan` and so
through `channel.plan`: run `k` of both arms reads stream `r<k>`, and the smoke
run reads `smoke`. No new draw seed is drawn, so the pairing of §0 is that plan's
draws case for case, as `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s were.

THE SEED (§11) was fixed by rule before any draw was computed: the next prime
after `PLAN_RANKED.md`'s 113, the last loop plan's. `ORDER_SEED` draws one thing,
which arm runs first, from `ARMS`, so the order of `ARMS` is pinned.

THE DEFAULTS (§0) are the four listed rules whose regions hold four or more rules
of another queue: `cause/narrow.py`'s group *many*, over all 29 rules. `DEFAULTS`
transcribes them, and `IM-g2` holds the set to that module's `held` and `group`.

THE LABELS THE TRIGGER READS are `PLAN_REUSE.md`'s first Stage B record's, as
`PLAN_CHANNEL.md`'s, `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s triggers read
them (rule B): handed in, never the oracle's.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_impasse.py` pins every one of them, so that moving one
after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact. Each row's side is in `SIDES`: `IM-a`,
`IM-c` and `IM-f` hold at or above their lines, `IM-d` and `IM-e` at or below,
and `IM-b` strictly below.

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as §0
numbers them. `IM-g2` and `IM-g3` recompute them and refuse if one departs;
Stage A recomputes all eight and records whether each came back.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from placement import plan as pl_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_IMPASSE.md")
OUT = Path("results_impasse")
MIN_SIGNATURES = 1                 # §0's line

# --- §11: the client, PLAN_PLACEMENT.md's, pin included ----------------------------------
MODEL = pl_plan.MODEL
PROMPT = pl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = pl_plan.TEMPERATURE
REASONING = pl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = pl_plan.MAX_TOKENS
MAX_RETRIES = pl_plan.MAX_RETRIES
CALL_RETRY_WAIT = pl_plan.CALL_RETRY_WAIT
RATE_LIMITED = pl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = pl_plan.RATE_LIMIT_WAIT
PROVIDER = pl_plan.PROVIDER        # {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
PROVIDER_NAME = pl_plan.PROVIDER_NAME

# --- §11: the protocol --------------------------------------------------------------------
PROTOCOLS = ("v1c", "v1n")
LEVEL = pl_plan.LEVEL              # 3
SYSTEM_PROMPT_SHA16 = pl_plan.SYSTEM_PROMPT_SHA16
NOTICE_BASE_SHA16 = "24b1b5c42568dd32"    # PLAN_CAUSE.md's arm i's paragraph, §5.2
BLIND_BASE_SHA16 = "8de0ebf50ce9a54b"     # v2b's, which v1n's paragraph opens with

# --- §11: the arms and the causes (§5) ------------------------------------------------------
IMPASSE, CONFLICT, ERROR = pl_plan.IMPASSE, pl_plan.CONFLICT, pl_plan.ERROR
CAUSES = pl_plan.CAUSES
ARMS = PROTOCOLS                   # an arm is named by its protocol; ORDER_SEED picks from it
COVERAGE = pl_plan.COVERAGE        # 1/2, PLAN_CHANNEL.md's channel arm's

# --- §11: the runs ---------------------------------------------------------------------------
REPS = 3
N = pl_plan.N                      # 2,000
SEED = pl_plan.SEED                # 17
SMOKE_N = 30
SMOKE_ARM = "v1n"
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.4)

# --- §11: the seed -----------------------------------------------------------------------------
ORDER_SEED = 127

# --- §0: the defaults, cause/narrow.py's group "many" over the 29 rules -----------------------
DEFAULTS = ("H08", "H27", "H28", "H29")

# --- §0: the lines ---------------------------------------------------------------------------
IM_A_LINE = Fraction(1, 5)         # holds at >= : median whole_I(r), v1n, less v1c's
IM_B_LINE = Fraction(1, 3)         # holds at <  : whole_D over v1n's runs pooled
IM_C_LINE = Fraction(1, 100)       # holds at >= : median space(B), v1n, less v1c's
IM_D_LINE = Fraction(1, 40)        # holds at <= : median space(B), v1c, less v1n's
IM_E_LINE = Fraction(3, 4)         # holds at <= : median impasses(r), v1n, over v1c's
IM_F_LINE = Fraction(3, 4)         # holds at >= : median born_W(r), v1n
IM_B_MIN = 5                       # the drafts IM-b needs, pooled, to have a value

LINES = {"IM-a": IM_A_LINE, "IM-b": IM_B_LINE, "IM-c": IM_C_LINE, "IM-d": IM_D_LINE,
         "IM-e": IM_E_LINE, "IM-f": IM_F_LINE}
SIDES = {"IM-a": ">=", "IM-b": "<", "IM-c": ">=", "IM-d": "<=", "IM-e": "<=", "IM-f": ">="}

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
# The runs are named by their plan and arm: `pl_v1c_r1` is PLAN_PLACEMENT.md's v1c r1,
# `wh_v1c_r1` and `wh_v1d_r1` PLAN_WHOLE.md's.
DECLARED = {
    # 1. The escalations by cause: [all, impasse, conflict, reported error].
    "escalations": {
        "pl_v1c_r1": [98, 37, 18, 43],
        "pl_v1c_r2": [68, 32, 3, 33],
        "pl_v1c_r3": [87, 28, 6, 53],
        "wh_v1c_r1": [88, 26, 4, 58],
        "wh_v1c_r2": [72, 35, 10, 27],
        "wh_v1c_r3": [84, 39, 4, 41],
        "wh_v1d_r1": [48, 17, 4, 27],
        "wh_v1d_r2": [58, 14, 7, 37],
        "wh_v1d_r3": [55, 17, 2, 36],
    },
    # 2. The share whole by cause: [whole, right-queue drafts naming a valid rule].
    "whole_by_cause": {
        "pl_v1c_r1": {"IMPASSE": [10, 36], "CONFLICT": [7, 17], "ERROR": [18, 39]},
        "pl_v1c_r2": {"IMPASSE": [10, 30], "CONFLICT": [0, 3], "ERROR": [9, 31]},
        "pl_v1c_r3": {"IMPASSE": [13, 27], "CONFLICT": [0, 6], "ERROR": [22, 52]},
        "wh_v1c_r1": {"IMPASSE": [8, 24], "CONFLICT": [1, 4], "ERROR": [35, 57]},
        "wh_v1c_r2": {"IMPASSE": [14, 31], "CONFLICT": [2, 9], "ERROR": [7, 26]},
        "wh_v1c_r3": {"IMPASSE": [11, 36], "CONFLICT": [1, 4], "ERROR": [23, 40]},
        "wh_v1d_r1": {"IMPASSE": [11, 17], "CONFLICT": [3, 4], "ERROR": [13, 26]},
        "wh_v1d_r2": {"IMPASSE": [9, 13], "CONFLICT": [1, 7], "ERROR": [20, 35]},
        "wh_v1d_r3": {"IMPASSE": [10, 16], "CONFLICT": [2, 2], "ERROR": [16, 33]},
    },
    # 3. At the impasses, by the governing rule's group, the same counts; pooled over
    #    v1c's six runs; and the impasse escalations v1c met at each default's tickets.
    "groups": {
        "pl_v1c_r1": {"none": [6, 16], "few": [3, 10], "many": [1, 10]},
        "pl_v1c_r2": {"none": [10, 15], "few": [0, 8], "many": [0, 7]},
        "pl_v1c_r3": {"none": [9, 12], "few": [3, 9], "many": [1, 6]},
        "wh_v1c_r1": {"none": [6, 10], "few": [1, 11], "many": [1, 3]},
        "wh_v1c_r2": {"none": [12, 16], "few": [2, 8], "many": [0, 7]},
        "wh_v1c_r3": {"none": [8, 16], "few": [3, 9], "many": [0, 11]},
        "wh_v1d_r1": {"none": [8, 9], "few": [2, 5], "many": [1, 3]},
        "wh_v1d_r2": {"none": [7, 8], "few": [1, 3], "many": [1, 2]},
        "wh_v1d_r3": {"none": [7, 7], "few": [2, 6], "many": [1, 3]},
    },
    "groups_pooled_v1c": {"none": [51, 85], "few": [12, 55], "many": [3, 44]},
    "impasses_at_defaults_v1c": {"H08": 7, "H27": 0, "H28": 13, "H29": 24},
    # 4. The whole drafts at impasses, and how their escalations ended.
    "born": {
        "pl_v1c_r1": {"whole": 10, "born": 7, "unplaced": 3, "refused": 0},
        "pl_v1c_r2": {"whole": 10, "born": 10, "unplaced": 0, "refused": 0},
        "pl_v1c_r3": {"whole": 13, "born": 10, "unplaced": 3, "refused": 0},
        "wh_v1c_r1": {"whole": 8, "born": 7, "unplaced": 1, "refused": 0},
        "wh_v1c_r2": {"whole": 14, "born": 12, "unplaced": 1, "refused": 1},
        "wh_v1c_r3": {"whole": 11, "born": 10, "unplaced": 1, "refused": 0},
        "wh_v1d_r1": {"whole": 11, "born": 9, "unplaced": 2, "refused": 0},
        "wh_v1d_r2": {"whole": 9, "born": 8, "unplaced": 1, "refused": 0},
        "wh_v1d_r3": {"whole": 10, "born": 7, "unplaced": 3, "refused": 0},
    },
    # 5. Where each v1c base lost its points: [lost, under rules whose tickets met no
    #    impasse, an impasse and another cause, only impasses, no escalation].
    "lost": {
        "pl_v1c_r1": [4375, 4080, 125, 170, 0],
        "pl_v1c_r2": [4260, 2060, 80, 0, 2120],
        "pl_v1c_r3": [6580, 6400, 160, 20, 0],
        "wh_v1c_r1": [10860, 10120, 720, 0, 20],
        "wh_v1c_r2": [11288, 8880, 288, 0, 2120],
        "wh_v1c_r3": [10450, 425, 9920, 105, 0],
    },
    # 6. H01's first ticket, case 44: how it met the base, its draft's class and
    #    verdict, and the first later case whose first call drafted H01's region whole.
    "h01_case_44": {
        "pl_v1c_r1": ["IMPASSE", "cut_by_one", "nacida", 155],
        "pl_v1c_r2": ["ERROR", "cut_by_one", "nacida", 155],
        "pl_v1c_r3": ["IMPASSE", "cut_by_one", "nacida", 1802],
        "wh_v1c_r1": ["decided", None, None, 155],
        "wh_v1c_r2": ["ERROR", "cut_by_one", "rechazada", None],
        "wh_v1c_r3": ["IMPASSE", "cut_by_one", "nacida", None],
        "wh_v1d_r1": ["decided", None, None, 155],
        "wh_v1d_r2": ["ERROR", "whole", "nacida", None],
        "wh_v1d_r3": ["IMPASSE", "whole", "nacida", None],
    },
    # 7. The schedule.
    "schedule": [["v1c", 1], ["v1n", 1], ["v1c", 2], ["v1n", 2], ["v1c", 3], ["v1n", 3]],
    # 8. The groups off the text's 29 regions: four or more rules of another queue
    #    inside, and one to three.
    "groups_of_rules": {"many": ["H08", "H27", "H28", "H29"],
                        "few": ["H03", "H06", "H12", "H16", "H18"]},
}


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_REASONED_LOOP.md`'s one reasoning setting and
    one budget, as `PLAN_PLACEMENT.md` sends them."""
    return pl_plan.settings()


def schedule() -> list[tuple[str, int]]:
    """§2.3: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_IMPASSE/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§5.3): PLAN_CHANNEL.md's, called -----------------------------------------------

STREAMS = pl_plan.STREAMS          # ("r1", "r2", "r3", "smoke")
draw_seed = pl_plan.draw_seed
draws = pl_plan.draws
draws_digest = pl_plan.draws_digest
reportable = pl_plan.reportable


def _arm(arm: str) -> None:
    if arm not in ARMS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")


def stream(arm: str, rep: int | None) -> str:
    """The stream a run reads: `r<rep>` for run `rep` of either arm, the smoke
    run's when `rep` is None."""
    _arm(arm)
    return "smoke" if rep is None else f"r{rep}"


def channel_of(arm: str, rep: int | None) -> dict:
    """What a record says of its channel (rule C): the coverage, and the draws'
    seed string and digest."""
    name = stream(arm, rep)
    return {"channel_coverage": str(COVERAGE), "draws_seed": draw_seed(name),
            "draws_sha16": draws_digest(name), "draws_n": N}


# --- the labels the trigger reads (rule B) ----------------------------------------------------

def labels_path() -> Path:
    return pl_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_CHANNEL.md`'s trigger reads them."""
    return pl_plan.labels()


# --- §8 to §10: the records ----------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_impasse/`.

def _check(arm: str, rep: int) -> None:
    _arm(arm)
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
    """Where a run appends its answers as they arrive (§5.4). Ignored by git,
    and gone once its record is written."""
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
