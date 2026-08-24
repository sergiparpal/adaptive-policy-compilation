"""
THE LABELLED PAIR BENCHMARK — pairs whose correct winner is known by
construction.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Rung 2's finding is that the mechanism works and the material never arrives:
subsumption plus 199 declared edges executes a perfect author's declaration at
e2e 1.0000, and across eight runs the proposer generated 2 conflicts, 14
proposed edges and 0 accepted — all 14 rejected for the same reason,
`no_solapan`, the cited rule does not overlap.

`PLAN_PAIRWISE.md` changes the question put to the model: instead of "write a
rule", "here are two rules that both match this ticket — which queue does it go
to?". Before a euro is spent asking that of the learned base, it has to be asked
where the answer is already known. This module builds that population.

**It is a benchmark, not a measurement of anything.** It spends no API call,
makes no decision and scores no model. What it produces is a set of pairs, each
with a witness ticket and the queue the hidden policy sends that ticket to.

--------------------------------------------------------------------------
THE SUBSTRATE ALREADY EXISTS AND IS NOT TOUCHED
--------------------------------------------------------------------------
`hidden_priority.build_hidden_engine` derives the minimal edge set from the
hidden policy's layer order: an edge is declared iff the two extensions OVERLAP,
are INCOMPARABLE by subsumption, and the ACTIONS DIFFER. Over the 29 rules that
partitions the 406 pairs into 112 disjoint, 61 already ordered by subsumption, 34
same-action and **199 declared edges with a known winner**. That module is
imported and called unchanged; so is `engine2`. Nothing in `rung2/` is modified.

--------------------------------------------------------------------------
THE WITNESS, WHICH IS THE WHOLE POINT
--------------------------------------------------------------------------
For a declared edge the witness is a case drawn from `ext(winner) & ext(loser)`,
the region where the two rules actually compete. The answer to "which queue does
this ticket go to?" *is* the edge, and checking it costs an `&` of two integers.

**But not any case in the intersection will do.** A third rule from an even
earlier layer may also match there, and then the hidden policy's true action is
neither rule's — the ticket would have a correct answer that is not on the menu.
So the intersection is restricted to the cases whose truth is the winner's
action, and the witness is the lowest-indexed of those. Deterministic: no
sampling, no seed.

Pairs with at least one clean witness are the benchmark and its denominator.
Pairs with none are recorded, counted **separately and outside the
denominator**, with the reason. Their count is a result of this run.

**Read those as a bias and not only as a loss.** They are precisely the pairs
where the layer order is invisible on the surface of the two rules shown, so the
survivors are the easier half by construction, and any rate measured on them is
an **upper** estimate of what a proposer would do on all 199. That is not a
caveat; it is what the denominator means.

--------------------------------------------------------------------------
TRAP — THE BIT ORDER IS MSB-FIRST AND GETTING IT WRONG FAILS SILENTLY
--------------------------------------------------------------------------
`engine2.Space` builds masks with `int("".join(...), 2)`, so case index `i` lives
at bit position `n - 1 - i` and the **lowest-indexed** case in a mask is its
**highest** set bit. An implementation that assumes LSB-first draws witnesses
from the wrong cases and every figure downstream is quietly wrong. Hence
`lowest_case_index`, and hence the two assertions below, which would both fail
loudly on that mistake:

  1. both rules of the pair match the witness case;
  2. `true_action(witness) == action[winner]`.

They are checked for every emitted witness, and a failure stops the run.

--------------------------------------------------------------------------
WHY THIS MODULE MAY SEE THE ORACLE
--------------------------------------------------------------------------
It imports `true_action` and `true_rule_id`, and it is therefore added
deliberately to the allowlist in `tests/test_oracle_separation.py`, whose own
docstring says growing that list must be a decision rather than an oversight.
The decision: this measures OFFLINE against a known key and decides nothing. No
component of the online loop imports it, and the benchmark it writes carries the
key openly — that is what makes it a benchmark.

Usage:  PYTHONHASHSEED=0 python3 -m rung2.pair_benchmark
        PYTHONHASHSEED=0 python3 -m rung2.pair_benchmark --checks
        PYTHONHASHSEED=0 python3 -m rung2.pair_benchmark --digest
"""

from __future__ import annotations

import hashlib
import json
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.hidden_policy import true_action, true_rule_id
from harness.provenance import describe, environment

from .engine2 import Space
from .hidden_priority import build_hidden_engine

OUT = Path("results2")
RECORD = "pair_benchmark.json"

N_RULES = 29
N_PAIRS = N_RULES * (N_RULES - 1) // 2          # 406

# The two counts PLAN_PAIRWISE.md §7 measured on 2026-08-24 and made a gate on
# this stage, in the same sense the six figures of §6 are a gate on stage A.
# They are not figures of this record: they are what says this run built the
# population the plan budgeted for.
GATE_CLEAN = 170
GATE_UNCLEAN = 29


# ---------------------------------------------------------------------------
# The bit convention, in one place
# ---------------------------------------------------------------------------

def lowest_case_index(mask: int, n: int):
    """
    The lowest CASE index a `Space` mask holds, or None if it holds none.

    MSB-first: case `i` is bit `n - 1 - i`, so the lowest-indexed case is the
    HIGHEST set bit and `bit_length` finds it in one step. Every witness in this
    record comes through here.
    """
    return None if mask == 0 else n - mask.bit_length()


def case_indices(mask: int, n: int):
    """Every case index a mask holds, ascending. Used for the diagnosis of the
    pairs with no clean witness, never for the witness itself."""
    out = []
    while mask:
        b = mask.bit_length()
        out.append(n - b)
        mask &= (1 << (b - 1)) - 1
    return out


# ---------------------------------------------------------------------------
# The key, over the whole space
# ---------------------------------------------------------------------------

def oracle_masks(cases, n):
    """
    Two families of masks over the exhaustive space:

      truth[action]  the cases whose TRUE label is that action
      owner[rid]     the cases the hidden rule `rid` WINS under first-match-wins

    Both partition the space — every case has exactly one true action and
    exactly one winning rule — and the second is what diagnoses a pair with no
    clean witness: it names the rule that owns the intersection instead of
    asserting that some rule does.
    """
    tbits = {a: bytearray(n) for a in ACTIONS}
    obits: dict[str, bytearray] = {}
    for i, case in enumerate(cases):
        tbits[true_action(case)][i] = 1
        rid = true_rule_id(case)
        if rid not in obits:
            obits[rid] = bytearray(n)
        obits[rid][i] = 1
    to_int = lambda b: int("".join(map(str, b)), 2)      # noqa: E731
    return ({a: to_int(b) for a, b in tbits.items()},
            {r: to_int(b) for r, b in obits.items()})


# ---------------------------------------------------------------------------
# The benchmark
# ---------------------------------------------------------------------------

def pair_row(engine, cases, truth, owner, action, layer, winner, loser, n):
    """
    One declared edge, with its witness if it has a clean one.

    The two assertions of the module header are checked here and raise, so a
    wrong bit convention or a wrong key stops the run at the first pair instead
    of producing a plausible-looking record.
    """
    inter = engine.ext[winner] & engine.ext[loser]
    clean_mask = inter & truth[action[winner]]
    idx = lowest_case_index(clean_mask, n)

    row = {
        "winner": winner, "loser": loser,
        "winner_action": action[winner], "loser_action": action[loser],
        "winner_layer_index": layer[winner], "loser_layer_index": layer[loser],
        "overlap_cases": inter.bit_count(),
        "clean_cases": clean_mask.bit_count(),
        "clean": idx is not None,
        "witness_index": idx,
        "witness": None,
    }
    if idx is None:
        # Nobody's competition: name the rules that actually own the region.
        held = [((owner[r] & inter).bit_count(), r) for r in owner
                if owner[r] & inter]
        row["owned_by"] = [{"rule_id": r, "cases": c} for c, r in
                           sorted(held, key=lambda t: (-t[0], t[1]))]
        row["true_actions_over_the_overlap"] = dict(sorted(Counter(
            true_action(cases[i]) for i in case_indices(inter, n)).items()))
        return row

    case = cases[idx]
    by_id = {r.rule_id: r for r in engine.rules}
    if not by_id[winner].matches(case) or not by_id[loser].matches(case):
        raise AssertionError(
            f"witness {idx} of {winner}>{loser} is not matched by both rules: "
            f"the bit convention is wrong (see the module header)")
    if true_action(case) != action[winner]:
        raise AssertionError(
            f"witness {idx} of {winner}>{loser} has truth {true_action(case)} "
            f"and the winner's action is {action[winner]}")
    row["witness"] = case.as_dict()
    return row


def build(space: Space | None = None):
    """
    The whole benchmark, from nothing but the frozen modules. Deterministic:
    no sampling and no seed anywhere in it.
    """
    engine, declared, stats = build_hidden_engine(space)
    n = engine.space.n
    cases = list(all_cases())
    truth, owner = oracle_masks(cases, n)
    action = {r.rule_id: r.action for r in engine.rules}
    layer = {r.rule_id: k for k, r in enumerate(engine.rules)}
    rows = [pair_row(engine, cases, truth, owner, action, layer, w, lo, n)
            for w, lo in declared]
    return rows, stats, n


def digest(rows) -> str:
    """A fingerprint of the emitted witnesses, for the determinism gate. It
    covers the pair, the witness index and the witness itself, which is
    everything a consumer of this record reads."""
    h = hashlib.sha256()
    for r in rows:
        h.update(json.dumps(
            [r["winner"], r["loser"], r["witness_index"], r["witness"]],
            sort_keys=True).encode())
        h.update(b"\0")
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gate_partition(stats):
    """
    The four boxes must partition the 406 pairs of the 29 rules, and each must
    be the count `hidden_priority` has always produced. The record checks
    itself: 112 + 61 + 34 + 199 == 406.
    """
    boxes = {
        "skipped_disjoint": stats["skipped_disjoint"],
        "skipped_subsumed_by_structure": stats["skipped_subsumed_by_structure"],
        "skipped_same_action": stats["skipped_same_action"],
        "declared": stats["declared"],
    }
    total = sum(boxes.values())
    return {
        "what": "the four boxes hidden_priority.py sorts the 406 pairs of the "
                "29 hidden rules into. It is a property of the frozen policy, "
                "not a figure of this run.",
        "boxes": boxes,
        "expected": {"skipped_disjoint": 112,
                     "skipped_subsumed_by_structure": 61,
                     "skipped_same_action": 34, "declared": 199},
        "total": total, "n_pairs": N_PAIRS,
        "rejected_edges": len(stats["rejected"]),
        "passes": (total == N_PAIRS
                   and boxes == {"skipped_disjoint": 112,
                                 "skipped_subsumed_by_structure": 61,
                                 "skipped_same_action": 34, "declared": 199}
                   and not stats["rejected"]),
    }


def gate_witnesses(rows):
    """The two counts PLAN_PAIRWISE.md §7 budgeted the next stage on."""
    clean = sum(1 for r in rows if r["clean"])
    return {
        "what": "how many of the 199 declared pairs have a clean witness. "
                "PLAN_PAIRWISE.md §7 measured 170 and 29 on 2026-08-24 and made "
                "them a gate on this stage: they are what says this run built "
                "the population the next stage was budgeted for.",
        "clean": clean, "unclean": len(rows) - clean,
        "expected_clean": GATE_CLEAN, "expected_unclean": GATE_UNCLEAN,
        "n_declared": len(rows),
        "passes": clean == GATE_CLEAN and len(rows) - clean == GATE_UNCLEAN,
    }


def gate_determinism(a, b):
    """
    Two independent builds, from two independent `Space` objects, must emit
    byte-identical witnesses. `tests/test_pair_benchmark.py` runs the same check
    across three `PYTHONHASHSEED` values, which is the one that counts: rung 4
    already recorded a same-process determinism test returning a false zero.
    """
    da, db = digest(a), digest(b)
    return {
        "what": "two builds from scratch, in the same process, emit the same "
                "witnesses. The cross-process check over three PYTHONHASHSEED "
                "values is in tests/test_pair_benchmark.py.",
        "digest": da, "digest_second_build": db, "passes": da == db,
    }


# ---------------------------------------------------------------------------
# Description of the population
# ---------------------------------------------------------------------------

def describe_population(rows):
    overlaps = sorted(r["overlap_cases"] for r in rows)
    unclean = [r for r in rows if not r["clean"]]
    clean = [r for r in rows if r["clean"]]
    return {
        "overlap_over_the_declared_pairs": {
            "n": len(overlaps), "min": overlaps[0],
            "median": statistics.median(overlaps), "max": overlaps[-1],
            "note": "cases of the exhaustive space in ext(winner) & ext(loser). "
                    "None of the 199 is empty: overlap is the condition that "
                    "made the edge declarable in the first place.",
        },
        "unclean_pairs": {
            "n": len(unclean),
            "winners": dict(sorted(Counter(r["winner"] for r in unclean).items())),
            "losers": dict(sorted(Counter(r["loser"] for r in unclean).items())),
            "note": "no case of the overlap has the winner's action as its "
                    "truth: an earlier layer owns the whole region, so the "
                    "correct queue for every ticket there is neither rule's. "
                    "`owned_by` names the rules and the case counts.",
        },
        "clean_pairs": {
            "n": len(clean),
            "winner_actions": dict(sorted(Counter(
                r["winner_action"] for r in clean).items())),
            "loser_actions": dict(sorted(Counter(
                r["loser_action"] for r in clean).items())),
            "clean_cases": {
                "min": min(r["clean_cases"] for r in clean),
                "median": statistics.median(r["clean_cases"] for r in clean),
                "max": max(r["clean_cases"] for r in clean),
            },
        },
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    only_checks = "--checks" in argv
    only_digest = "--digest" in argv
    t_start = time.time()

    rows, stats, n = build()
    if only_digest:
        # The determinism child. It prints a WITNESS alongside the digest: the
        # iteration order of a set of the rule ids, which MUST change between
        # PYTHONHASHSEED values. Without it a cross-seed test could pass by
        # proving only that hashing is no longer randomized in this Python —
        # the precedent is `tests/hashseed_child.py`, written after rung 4's
        # same-process determinism test returned a false zero.
        print(json.dumps({
            "digest": digest(rows),
            "set_iteration": hashlib.sha256(
                "\0".join(set(r["winner"] for r in rows)).encode()
            ).hexdigest()[:16],
            "n_declared": len(rows),
            "n_clean": sum(1 for r in rows if r["clean"]),
        }))
        return 0

    print("=" * 78)
    print("THE LABELLED PAIR BENCHMARK — pairs whose winner is known")
    print("=" * 78)
    print(f"  {N_RULES} hidden rules · {N_PAIRS} pairs · {n:,} cases in the "
          f"space · zero API calls")
    print("  the substrate is hidden_priority.build_hidden_engine, imported and "
          "called unchanged")
    print(f"  {describe()}")

    g_part = gate_partition(stats)
    print()
    print("PARTITION GATE — the four boxes of the 406 pairs")
    for k, v in g_part["boxes"].items():
        exp = g_part["expected"][k]
        print(f"  {k:<32}{v:>6}   expected {exp:>6}"
              f"{'  ok' if v == exp else '  NO'}")
    print(f"  {'total':<32}{g_part['total']:>6}   expected {N_PAIRS:>6}"
          f"   rejected {g_part['rejected_edges']}")
    if not g_part["passes"]:
        print("  STOP: this is not the edge set rung 2 published.")
        return 1

    g_wit = gate_witnesses(rows)
    print()
    print("WITNESS GATE — how many of the 199 have a clean witness")
    print(f"  {'clean':<32}{g_wit['clean']:>6}   expected "
          f"{GATE_CLEAN:>6}"
          f"{'  ok' if g_wit['clean'] == GATE_CLEAN else '  NO'}")
    print(f"  {'no clean witness':<32}{g_wit['unclean']:>6}   expected "
          f"{GATE_UNCLEAN:>6}"
          f"{'  ok' if g_wit['unclean'] == GATE_UNCLEAN else '  NO'}")
    if not g_wit["passes"]:
        print("  STOP: this is not the population the next stage was budgeted "
              "for. Do not adjust to fit (hard rule 6).")
        return 1

    rows_b, _stats_b, _n_b = build()
    g_det = gate_determinism(rows, rows_b)
    print()
    print("DETERMINISM GATE — two builds from scratch")
    print(f"  digest {g_det['digest']} · second build "
          f"{g_det['digest_second_build']}"
          f"{'  ok' if g_det['passes'] else '  NO'}")
    if not g_det["passes"]:
        print("  STOP: the witnesses are not reproducible.")
        return 1

    pop = describe_population(rows)
    o = pop["overlap_over_the_declared_pairs"]
    u = pop["unclean_pairs"]
    print()
    print("=" * 78)
    print("THE POPULATION")
    print("=" * 78)
    print(f"  overlap over the 199 declared pairs: min {o['min']}, median "
          f"{o['median']:.0f}, max {o['max']:,} cases")
    print(f"  {g_wit['clean']} pairs carry a clean witness — the benchmark and "
          f"its denominator")
    print(f"  {u['n']} do not, and they are outside it. Their winners: "
          + ", ".join(f"{k}x{v}" for k, v in u["winners"].items()))
    print("  those are the pairs where the layer order is invisible on the "
          "surface of")
    print("  the two rules shown, so the survivors are the easier half by "
          "construction")

    if only_checks:
        print(f"\n  gates only, all pass. total cost: "
              f"{time.time() - t_start:.0f}s")
        return 0

    payload = {
        "_env": environment(n_rules=N_RULES, n_pairs=N_PAIRS),
        "what":
            "the pairs of the hidden policy whose correct winner is known by "
            "construction, each with a witness ticket drawn from the region "
            "where the two rules compete. Built so that the pairwise question "
            "can be asked where the answer is already known, before a euro is "
            "spent asking it of the learned base. It is a benchmark: it spends "
            "no API call, decides nothing and scores no model.",
        "substrate":
            "rung2/hidden_priority.py::build_hidden_engine, imported and called "
            "unchanged, and rung2/engine2.py. Nothing in rung2/ is modified. "
            "The edge set is the minimal one derived from the layer order: "
            "extensions overlap, subsumption-incomparable, actions differ.",
        "why_it_may_see_the_oracle":
            "it imports true_action and true_rule_id and is on the allowlist of "
            "tests/test_oracle_separation.py, added deliberately: it measures "
            "offline against a known key and decides nothing. The key is in the "
            "record openly, which is what makes it a benchmark.",
        "witness_rule":
            "the lowest-indexed case of ext(winner) & ext(loser) whose TRUE "
            "action is the winner's. Deterministic: no sampling, no seed. The "
            "restriction is not cosmetic — a third rule from an earlier layer "
            "may own part of the overlap, and there the correct queue is "
            "neither rule's.",
        "denominator_note":
            "the pairs with no clean witness are outside the denominator, and "
            "they are precisely the pairs where the layer order is invisible on "
            "the surface of the two rules shown. The survivors are therefore "
            "the easier half BY CONSTRUCTION, and any rate measured on them is "
            "an UPPER estimate of what a proposer would do on all 199. That is "
            "not a caveat; it is what the denominator means.",
        "bit_convention":
            "engine2.Space is MSB-first: case index i is bit n-1-i, so the "
            "lowest-indexed case of a mask is its HIGHEST set bit. Every "
            "witness passes the two assertions of pair_row — both rules match "
            "it, and its true action is the winner's — which is what would fail "
            "loudly on the opposite convention.",
        "n_rules": N_RULES, "n_pairs": N_PAIRS, "n_space": n,
        "gates": {"partition": g_part, "witnesses": g_wit,
                  "determinism": g_det,
                  "passes": all(g["passes"] for g in
                                (g_part, g_wit, g_det))},
        "population": pop,
        "pairs": rows,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
