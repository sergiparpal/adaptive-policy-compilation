"""
The gate, the constants, the draws and the bridge's tickets of
`PLAN_PLACEMENT.md`, in one place.

THE GATE READS THIS PLAN AND NO OTHER, AND IT COUNTS SIGNATURES. Every line of
`PLAN_PLACEMENT.md` that starts `**Signed by Sergi:` must be filled in, and there
must be at least `MIN_SIGNATURES`: one today, §0's. An amendment carries its own
line and raises the minimum. The counting is `reuse/plan.py`'s, called with this
plan's path and minimum rather than copied (§11 of the plan).

Every module of this package that writes a record calls `refuse_unsigned` before
it measures, builds or writes anything, and `placement/run.py` calls it before it
constructs a client. No flag skips it. **The free stages get the gate too**: what
it protects is the order of events, not money. A record of this plan written
before the signature would be a figure that existed before its band (§11).

THE CLIENT IS `PLAN_REASONED_LOOP.md`'S, IMPORTED AND NOT RETYPED, BUT FOR THE PIN
(§1, §2.8, rule A): the model, temperature 0, reasoning `{"effort": "high"}`,
16,000 tokens, the retries and the waits a call refused for the rate is waited
out through. The pin is this plan's, DeepInfra's fp8 endpoint, by the rule
agreed on 2026-11-06. `PROVIDER_NAME` is what a response's `provider` field is
expected to say, and the smoke run holds it to what it says (§2.5). The bridge
pins each of its two providers: Baidu by `PLAN_QUEUE_ALONE.md`'s pin, imported.

THE ARMS (§0, §5). Both run `PLAN_CHANNEL.md`'s channel arm at coverage 1/2, and
an arm is named by its protocol: `v1b`, that plan's channel arm, and `v1c`, which
changes only the placement round's list (`placement/protocol.py`).

THE DRAWS (§5.3) are `PLAN_CHANNEL.md`'s, called through `channel.plan`: run `k`
of both arms reads stream `r<k>`, and the smoke run reads `smoke`. No new draw
seed is drawn, so the pairing of §0 is that plan's draws case for case.

THE SEEDS (§11) were fixed by rule before any draw was computed: the next two
primes after `PLAN_CHANNEL.md`'s 97. `ORDER_SEED` draws one thing, which arm runs
first, from `ARMS`, so the order of `ARMS` is pinned. `BRIDGE_SEED` draws two:
the bridge's 13 tickets, and at each ticket the provider asked first, from
`BRIDGE_PROVIDERS`, whose order is pinned too. The placement listing keeps v2b's
`LISTING_SEED`, through `blind.protocol.listing`.

THE LABELS THE TRIGGER READS are `PLAN_REUSE.md`'s first Stage B record's, as
`PLAN_CHANNEL.md`'s trigger reads them (rule B): handed in, never the oracle's.

THE CONSTANTS are §11's and the lines are §0's, fixed before any figure of the
plan existed. `tests/test_placement.py` pins every one of them, so that moving
one after a figure exists is visible in a diff. **The lines are fractions**, and
every comparison with them is exact. `PL-a`'s and `PL-d`'s hold at or below
their lines, and every other at or above (`HOLDS_AT_OR_BELOW`).

`DECLARED` holds the figures §0 lists as computed while drafting, numbered as §0
numbers them. `PL-g2` and `PL-g3` recompute figures 1 to 3 and 5 to 8 and refuse
if one departs; Stage A recomputes all eight and records whether each came back.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from channel import plan as ch_plan
from queue_alone import plan as qa_plan
from reasoned_loop import plan as rl_plan
from reuse import plan as reuse_plan

PLAN = Path("PLAN_PLACEMENT.md")
OUT = Path("results_placement")
MIN_SIGNATURES = 1                 # §0's line

# --- §11: the client, PLAN_REASONED_LOOP.md's, and so PLAN_FIRST_MATCH.md's -----------
MODEL = rl_plan.MODEL
PROMPT = rl_plan.PROMPT            # v1, the system prompt's base
TEMPERATURE = rl_plan.TEMPERATURE
REASONING = rl_plan.REASONING      # {"effort": "high"}, on every call
MAX_TOKENS = rl_plan.MAX_TOKENS
MAX_RETRIES = rl_plan.MAX_RETRIES
CALL_RETRY_WAIT = rl_plan.CALL_RETRY_WAIT
RATE_LIMITED = rl_plan.RATE_LIMITED
RATE_LIMIT_WAIT = rl_plan.RATE_LIMIT_WAIT

# --- §11, §2.8: the pins ------------------------------------------------------------------
PROVIDER = {"order": ["deepinfra/fp8"], "allow_fallbacks": False}
PROVIDER_NAME = "DeepInfra"        # held to the smoke run's `provider` field (§2.5)
BRIDGE_PROVIDERS = ("baidu", "deepinfra")      # in this order: BRIDGE_SEED's draw picks from it
BRIDGE_PINS = {"baidu": qa_plan.PROVIDER, "deepinfra": PROVIDER}
BRIDGE_NAMES = {"baidu": qa_plan.PROVIDER_NAME, "deepinfra": PROVIDER_NAME}

# --- §11: the protocol --------------------------------------------------------------------
PROTOCOLS = ("v1b", "v1c")
LEVEL = rl_plan.LEVEL              # 3
SYSTEM_PROMPT_SHA16 = rl_plan.SYSTEM_PROMPT_SHA16

# --- §11: the arms and the causes (§5) ------------------------------------------------------
IMPASSE, CONFLICT, ERROR = ch_plan.IMPASSE, ch_plan.CONFLICT, ch_plan.ERROR
CAUSES = ch_plan.CAUSES
ARMS = PROTOCOLS                   # an arm is named by its protocol; ORDER_SEED picks from it
COVERAGE = ch_plan.COVERAGE["c"]   # 1/2, PLAN_CHANNEL.md's channel arm's

# --- §11: the runs ---------------------------------------------------------------------------
REPS = 3
N = reuse_plan.N                   # 2,000
SEED = reuse_plan.SEED             # 17
SMOKE_N = 30
SMOKE_ARM = "v1c"
MAX_ESCALATIONS = 400              # §1's cap
MAX_CONSECUTIVE_FAILURES = 5       # an outage, not answers (§5.4)

# --- §11: the seeds ----------------------------------------------------------------------------
ORDER_SEED = 101
BRIDGE_SEED = 103

# --- §11, §2.6: the bridge -------------------------------------------------------------------
BRIDGE_TICKETS = 40
BRIDGE_DRAWN = 13
BRIDGE_ASKS = 1                    # to each provider
BRIDGE_RARE = ("SECURITY_INCIDENT", "ONCALL_ESCALATION")

# --- §0: the lines ---------------------------------------------------------------------------
PL_A_LINE = Fraction(3, 4)         # holds at <= : median refused(r), v1c, over v1b's
PL_B_LINE = Fraction(9, 10)        # holds at >= : median space(B), v1c
PL_C_LINE = Fraction(9, 10)        # each v1c run's space(B) at >= it ...
PL_C_RUNS = 3                      # ... and PL-c holds when this many do
PL_D_LINE = Fraction(1, 20)        # holds at <= : median space(B), v1b, less v1c's
PL_E_LINE = Fraction(9, 10)        # holds at >= : median space(B), v1b
PL_F_LINE = Fraction(9, 10)        # holds at >= : median recall of ONCALL_ESCALATION, v1c

LINES = {"PL-a": PL_A_LINE, "PL-b": PL_B_LINE, "PL-c": PL_C_LINE, "PL-d": PL_D_LINE,
         "PL-e": PL_E_LINE, "PL-f": PL_F_LINE}
HOLDS_AT_OR_BELOW = ("PL-a", "PL-d")

# --- §0: what the drafter computed while drafting, numbered as §0 numbers it ------------------
# Figure 1's columns, in §0's table's order after the run's name.
ROUND_KEYS = ("escalations", "rounds", "listed", "inside", "containing", "equal", "crossing",
              "wholly_governed", "v1c_list", "not_sent", "unplaced", "complete")

DECLARED = {
    # 1. The new round's list on v1b's recorded rounds, by run, and its apportionment.
    "rounds": {
        "reasoned_loop/i_r1": [41, 29, 113, 11, 0, 0, 102, 13, 89, 2, 3, 1],
        "reasoned_loop/i_r2": [28, 17, 48, 4, 0, 0, 44, 4, 40, 2, 3, 0],
        "reasoned_loop/i_r3": [18, 17, 34, 0, 0, 0, 34, 0, 34, 0, 2, 0],
        "reasoned_loop/e_r1": [99, 90, 1026, 24, 69, 8, 925, 169, 764, 2, 21, 14],
        "reasoned_loop/e_r2": [120, 113, 1392, 127, 87, 21, 1157, 243, 935, 6, 28, 15],
        "reasoned_loop/e_r3": [102, 100, 848, 40, 160, 7, 641, 96, 552, 13, 38, 28],
        "channel/e_r1": [90, 81, 735, 55, 41, 0, 639, 92, 547, 5, 22, 15],
        "channel/e_r2": [95, 87, 799, 61, 48, 10, 680, 162, 528, 4, 14, 8],
        "channel/e_r3": [106, 102, 940, 40, 84, 15, 801, 78, 738, 3, 18, 8],
        "channel/c_r1": [79, 68, 502, 9, 53, 3, 437, 29, 411, 4, 16, 12],
        "channel/c_r2": [131, 119, 1271, 82, 106, 83, 1000, 207, 876, 1, 34, 20],
        "channel/c_r3": [62, 55, 478, 27, 46, 1, 404, 60, 345, 3, 9, 3],
    },
    "rounds_all": [971, 878, 8186, 480, 694, 148, 6864, 1153, 5859, 45, 208, 124],
    "answered": 208,                                   # every unplaced answer came back
    "nested_alone": {"complete": 122, "not_sent": 42},
    # As §0 writes them; compared by value, as fractions.
    "pl_a_reading": {"refused": ["16/79", "34/131", "9/62"], "median": "16/79",
                     "left": ["4/79", "14/131", "6/62"], "median_left": "6/62",
                     "ratio": "474/992"},
    # 2. By the draft's queue: unplaced, and complete against v1c's list.
    "by_queue": {"SECURITY_INCIDENT": [26, 17], "ONCALL_ESCALATION": [14, 3],
                 "ACCOUNT_MANAGER": [18, 14], "T3_ENGINEERING": [28, 19],
                 "T2_TECHNICAL": [63, 36], "SELF_SERVICE_DEFLECT": [32, 18],
                 "T1_GENERAL": [19, 12], "BILLING_SPECIALIST": [8, 5]},
    # 3. The two rarest queues' unplaced answers in PLAN_CHANNEL.md's channel runs:
    #    the cases v1c's lists would have taken, and those they would not.
    "rare_in_channel": {
        "c_r1": {"SECURITY_INCIDENT": {"taken": [599, 770, 1063, 1264, 1871, 1961],
                                       "left": [448, 580, 751]},
                 "ONCALL_ESCALATION": {"taken": [257], "left": []}},
        "c_r2": {"SECURITY_INCIDENT": {"taken": [580], "left": [155]},
                 "ONCALL_ESCALATION": {"taken": [], "left": [1951]}},
        "c_r3": {"SECURITY_INCIDENT": {"taken": [], "left": [402]},
                 "ONCALL_ESCALATION": {"taken": [], "left": [954, 1432]}},
    },
    "c_r2_1951_left_out": ["R0022"],
    # 4. The breadth of drafts and births.
    "breadth": {"rounds_broad": 247, "broad_unplaced": 54, "rounds_other": 631,
                "other_unplaced": 154, "born_after_round": 664, "born_broad": 193,
                "broad_refusals_taken": 37},
    # 5. The hidden policy through v1c's path.
    "hidden_v1c": {"born": 29, "rounds": 27, "listed_v1b": 253, "listed_v1c": 192,
                   "inside_or_containing": 54, "governed": 7, "not_sent": 2,
                   "installed": 192, "space": [134400, 134400], "corpus": [2000, 2000]},
    # 6. The transcriber through both paths, under each of PLAN_CHANNEL.md's draws.
    "transcriber": {
        "v1b": {"r1": {"escalations": 23, "calls": 45, "space_right": 134380, "corpus_right": 1999},
                "r2": {"escalations": 22, "calls": 43, "space_right": 132280, "corpus_right": 1996},
                "r3": {"escalations": 23, "calls": 45, "space_right": 134380, "corpus_right": 1999},
                "smoke": {"escalations": 9, "calls": 17, "space_right": 49420}},
        "v1c": {"r1": {"escalations": 23, "calls": 42, "space_right": 134380, "corpus_right": 1999},
                "r2": {"escalations": 22, "calls": 40, "space_right": 132280, "corpus_right": 1996},
                "r3": {"escalations": 23, "calls": 42, "space_right": 134380, "corpus_right": 1999},
                "smoke": {"escalations": 9, "calls": 16, "space_right": 49420,
                          "rounds": 8, "listed_v1b": 20, "listed_v1c": 10, "not_sent": 1}},
    },
    # 7. The schedule.
    "schedule": [["v1c", 1], ["v1b", 1], ["v1c", 2], ["v1b", 2], ["v1c", 3], ["v1b", 3]],
    # 8. The bridge's tickets.
    "bridge": {
        "SECURITY_INCIDENT": [44, 155, 342, 402, 448, 580, 599, 676, 739, 751, 770, 1063,
                              1235, 1264, 1514, 1704, 1802, 1871, 1961, 1998],
        "ONCALL_ESCALATION": [257, 710, 954, 982, 1432, 1783, 1951],
        "rare_escalated": 20, "candidates": 175,
        "drawn": [18, 19, 29, 42, 55, 65, 265, 449, 513, 529, 658, 794, 881],
        "first": {"baidu": 18, "deepinfra": 22},
    },
}


def settings() -> dict:
    """What every request carries beyond the model, the temperature, the
    messages and the pin: `PLAN_REASONED_LOOP.md`'s one reasoning setting and
    one budget."""
    return rl_plan.settings()


def schedule() -> list[tuple[str, int]]:
    """§2.4: the six runs in order. `ORDER_SEED` draws which arm runs first;
    then the arms alternate, one run of each in every repetition."""
    first = random.Random(f"PLAN_PLACEMENT/order/{ORDER_SEED}").choice(ARMS)
    second = ARMS[1 - ARMS.index(first)]
    return [(arm, rep) for rep in range(1, REPS + 1) for arm in (first, second)]


# --- the draws (§5.3): PLAN_CHANNEL.md's, called ---------------------------------------------

STREAMS = ch_plan.STREAMS          # ("r1", "r2", "r3", "smoke")
draw_seed = ch_plan.draw_seed
draws = ch_plan.draws
draws_digest = ch_plan.draws_digest
reportable = ch_plan.reportable


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
    return ch_plan.labels_path()


def labels() -> list[tuple[str, str]]:
    """`(truth, truth_rule)` for every corpus case, off `PLAN_REUSE.md`'s first
    Stage B record, as `PLAN_CHANNEL.md`'s trigger reads them."""
    return ch_plan.labels()


# --- the bridge (§2.6, §5.5) -------------------------------------------------------------------

def bridge_draw(candidates: list[int]) -> list[int]:
    """The 13 tickets `BRIDGE_SEED` draws from the other distinct tickets
    `PLAN_CHANNEL.md`'s channel runs escalated, in case order."""
    rng = random.Random(f"PLAN_PLACEMENT/bridge/{BRIDGE_SEED}")
    return sorted(rng.sample(sorted(candidates), BRIDGE_DRAWN))


def bridge_first(idx: int) -> str:
    """The provider asked first at ticket `idx`."""
    return random.Random(f"PLAN_PLACEMENT/bridge/{BRIDGE_SEED}/{idx}").choice(BRIDGE_PROVIDERS)


def bridge_tickets() -> list[int]:
    """§0's figure 8: the 40 tickets, in case order. `PL-g3` rebuilds them from
    the records and the seed before any of them is asked."""
    b = DECLARED["bridge"]
    return sorted(b["SECURITY_INCIDENT"] + b["ONCALL_ESCALATION"] + b["drawn"])


def bridge_asks() -> list[tuple[int, str]]:
    """Every ask of the bridge, in order: ticket by ticket, the provider drawn
    first, then the other."""
    out = []
    for idx in bridge_tickets():
        first = bridge_first(idx)
        out += [(idx, first), (idx, BRIDGE_PROVIDERS[1 - BRIDGE_PROVIDERS.index(first)])]
    return out


# --- §8 to §10: the records ----------------------------------------------------------------------
# Functions, not constants, so that every path follows `OUT` wherever it points:
# the tests point it at a temporary directory and must never land in
# `results_placement/`.

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


def bridge_path() -> Path:
    return OUT / "bridge.json"


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
    """Where a run, or a half of the bridge, appends its answers as they arrive
    (§5.4). Ignored by git, and gone once its record is written."""
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
