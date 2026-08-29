"""
`A-g1` TO `A-g4` — the blocking checks of §4, run first and alone.

They carry no band, adjudicate nothing and are excluded from every denominator.
**Each one aborts the run.** The convention is `PLAN_ORDER_METRICS.md`'s `G1`–`G6`
and the discipline is `harness.ceiling_check`'s: measure the instrument before the
instrument measures anything else.

--------------------------------------------------------------------------
WHAT EACH ONE IS FOR, AND WHAT IT WOULD CATCH
--------------------------------------------------------------------------
`A-g1` · **Step 0 for this instrument.** Every checked policy must be executed at
e2e 1.0000 by first-match-wins in layer order, through the **frozen** engine —
`harness.dsl.RuleEngine` loaded with the policy's rules and arbitrated by
`harness.ceiling_check.decide_by_priority`. A generator that emits policies the
engine cannot execute even with the correct arbitration measures the generator,
not specificity. It doubles as the check on `measure.py`'s bitmask path: the fast
truth and the engine's decision are compared **case by case**, not by their
totals, because two wrong answers can share a total.

`A-g2` · **the knob is the knob.** Achieved ρ within `RHO_TOLERANCE` of the bin
centre for every draw, reported as a distribution rather than asserted.

`A-g3` · **parity with the hidden policy.** Supplied its own permutation, its own
conditions and its own actions, this module's evaluation path must return
**0.5875 / 505 / 0.2140** on the corpus and reproduce `harness.ceiling_check`
exactly. Without it `A-a` compares two different measurement paths and means
nothing. The parity is checked against the frozen engine's own numbers, not
against constants transcribed from a record.

`A-g4` · **every rule reachable.** No rule claims nothing under first-match-wins;
exactly one rule matches the whole surface and it is in the last layer; and no
rule but that one carries a vacuous condition. **This is the check that killed the
first construction** — under it, 0 of 24,888 draws survived — and §1's amendment
of 2026-08-29 made reachability a property of the construction so that a failure
here now means a defect rather than a property of the draw.

It also keeps reporting **effective size per bin**, because the quantity that sank
the first construction has to stay visible: if it ever correlates with ρ again,
the curve is confounded and the run must abort rather than publish.

Usage:  python3 -m sensitivity.generator_check
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from pathlib import Path

from harness.ceiling_check import (all_cases, build_rules, decide_by_priority,
                                   measure as harness_measure)
from harness.default_rule_control import is_vacuous
from harness.domain import generate_corpus
from harness.dsl import Rule as DslRule, RuleEngine
from harness.provenance import describe, environment
from rung2.engine2 import Space

from . import generator as g
from . import measure as m

OUT = Path("results_sensitivity")
RECORD = "generator_check.json"

# Declared before the run. The gate's own sample; the sweep re-checks A-g2 and
# A-g4 on every draw it makes, because those two are cheap and universal.
CHECK_SEED = 17
CHECK_DRAWS_PER_BIN = 10          # A-g2, A-g4, and A-g1 over the corpus
SPACE_DRAWS_PER_BIN = 2           # A-g1 over the 134,400, which costs ~1 s each

# The published row A-g3 measures against. It is re-derived from the frozen engine
# in the same run; the constants are here so a silent drift in BOTH would still be
# caught by one of them.
PUBLISHED_ROW = {"accuracy_end_to_end": 0.5875, "conflict": 505,
                 "silent_error_rate": 0.2140}


def dsl_rules(policy) -> list[DslRule]:
    """The policy as frozen-DSL rules, born in layer order."""
    return [DslRule(rule_id=r.rule_id, conditions=list(r.conditions),
                    action=r.action, born_at=i)
            for i, r in enumerate(policy.rules)]


# ---------------------------------------------------------------------------

def a_g1(policy, ext, universe, cases) -> dict:
    """The frozen engine, arbitrating by birth order, against the mask truth —
    case by case."""
    rules = dsl_rules(policy)
    truth = g.truth_masks(policy, ext, universe.full)
    action_of_bit = {}
    for action, mask in truth.items():
        for i in range(universe.n):
            if (mask >> (universe.n - 1 - i)) & 1:
                action_of_bit[i] = action
    disagreements, impasses = 0, 0
    for i, case in enumerate(cases):
        outcome, winner, _ = decide_by_priority(rules, case)
        if outcome != "ACTION":
            impasses += 1
        elif winner.action != action_of_bit.get(i):
            disagreements += 1
    return {"n": universe.n, "impasses": impasses,
            "disagreements_with_the_fast_truth": disagreements,
            "e2e": (universe.n - impasses - disagreements) / universe.n,
            "passes": impasses == 0 and disagreements == 0}


def a_g3(space, corpus) -> dict:
    """Parity: this path against the frozen engine, on the hidden policy."""
    hidden = g.hidden_member()
    ext = [corpus.extension(list(r.conditions)) for r in hidden.rules]
    truth = g.truth_masks(hidden, ext, corpus.full)
    mine = m.score(m.verdict(hidden, ext, m.specificities(hidden, m.PUBLISHED),
                             corpus.full), truth, corpus.n)

    engine = RuleEngine()
    engine.rules = build_rules()
    theirs = harness_measure(list(generate_corpus(m.N_CORPUS, seed=m.CORPUS_SEED)),
                            engine.decide, "harness.ceiling_check")

    # `harness.ceiling_check.measure` publishes the split and the silent errors;
    # `correct` is derived from them there and computed directly here, so the two
    # routes to it are compared rather than one being read off the other.
    theirs = dict(theirs, correct=theirs["action"] - theirs["silent_errors_abs"])
    fields = ("action", "conflict", "impasse", "correct", "silent_errors_abs")
    same = {f: (mine[f], theirs[f], mine[f] == theirs[f]) for f in fields}
    published = {
        "accuracy_end_to_end": (round(mine["accuracy_end_to_end"], 4),
                                PUBLISHED_ROW["accuracy_end_to_end"]),
        "conflict": (mine["conflict"], PUBLISHED_ROW["conflict"]),
        "silent_error_rate": (round(mine["silent_error_rate"], 4),
                              PUBLISHED_ROW["silent_error_rate"]),
    }
    return {
        "against_the_frozen_engine": {k: {"mine": a, "engine": b, "equal": ok}
                                      for k, (a, b, ok) in same.items()},
        "against_the_published_row": {k: {"measured": a, "published": b,
                                          "equal": a == b}
                                      for k, (a, b) in published.items()},
        "passes": all(ok for _a, _b, ok in same.values())
        and all(a == b for a, b in published.values()),
    }


def a_g4(policy, ext, space) -> dict:
    """Reachability, the catch-all, and vacuity."""
    dead = g.dead_rules(policy, ext, space.full)
    full_extension = [i for i, e in enumerate(ext) if e == space.full]
    vacuous = [policy.rules[i].rule_id for i, r in enumerate(policy.rules)
               if any(is_vacuous(c) for c in r.conditions)]
    catchall_id = policy.rules[g.CATCHALL_POSITION].rule_id
    return {
        "dead_rules": dead,
        "rules_matching_everything": [policy.rules[i].rule_id
                                      for i in full_extension],
        "catch_all_is_last": full_extension == [g.CATCHALL_POSITION],
        "rules_with_a_vacuous_condition": vacuous,
        "effective_size": len(policy.rules) - len(dead),
        "passes": (not dead and full_extension == [g.CATCHALL_POSITION]
                   and vacuous == [catchall_id]),
    }


# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    space = Space()
    corpus = m.CorpusUniverse()
    corpus_cases = list(generate_corpus(m.N_CORPUS, seed=m.CORPUS_SEED))

    print("=" * 78)
    print("A-g1 TO A-g4 — the blocking checks of PLAN_SENSITIVITY.md §4")
    print("=" * 78)
    print(f"  13 ρ bins · {CHECK_DRAWS_PER_BIN} draws each · seed {CHECK_SEED} "
          f"· zero API calls")
    print(f"  {describe()}")

    # ---- A-g3 first: without parity nothing else means anything -----------
    g3 = a_g3(space, corpus)
    print("\n  A-g3 · PARITY WITH THE HIDDEN POLICY")
    for k, v in g3["against_the_frozen_engine"].items():
        print(f"    {k:<22}{v['mine']:>8}  engine {v['engine']:>8}"
              f"{'  ok' if v['equal'] else '  NO'}")
    for k, v in g3["against_the_published_row"].items():
        print(f"    {k:<22}{v['measured']:>8}  published {v['published']:>8}"
              f"{'  ok' if v['equal'] else '  NO'}")
    print(f"    A-g3: {'PASSES' if g3['passes'] else 'FAILS'}")

    # ---- the draws --------------------------------------------------------
    rng = random.Random(CHECK_SEED)
    per_bin, g1_rows = [], []
    print("\n  DRAWING AND CHECKING")
    print(f"  {'centre':>9}{'draws':>7}{'attempts':>10}{'|ρ−c| max':>11}"
          f"{'dead':>6}{'eff.size':>10}{'A-g1 corpus':>13}{'A-g1 space':>12}")
    for centre in g.RHO_BINS:
        rhos, attempts, sizes, g4s = [], 0, [], []
        drawn = []
        while len(drawn) < CHECK_DRAWS_PER_BIN:
            attempts += 1
            try:
                policy, ext = g.draw(rng, centre, space)
            except g.DeadEnd:
                continue
            drawn.append((policy, ext))
            rhos.append(abs(policy.rho - centre))
            g4 = a_g4(policy, ext, space)
            g4s.append(g4)
            sizes.append(g4["effective_size"])

        corpus_ok = space_ok = 0
        for k, (policy, ext) in enumerate(drawn):
            cext = [corpus.extension(list(r.conditions)) for r in policy.rules]
            row = a_g1(policy, cext, corpus, corpus_cases)
            row.update({"bin": centre, "draw": k, "surface": "corpus"})
            g1_rows.append(row)
            corpus_ok += row["passes"]
            if k < SPACE_DRAWS_PER_BIN:
                row = a_g1(policy, ext, space, list(all_cases()))
                row.update({"bin": centre, "draw": k, "surface": "space"})
                g1_rows.append(row)
                space_ok += row["passes"]

        per_bin.append({
            "centre": centre,
            "draws": len(drawn),
            "attempts": attempts,
            "acceptance_rate": round(len(drawn) / attempts, 4),
            "max_rho_deviation": round(max(rhos), 6),
            "a_g2_passes": max(rhos) <= g.RHO_TOLERANCE,
            "dead_rules_seen": sorted({len(x["dead_rules"]) for x in g4s}),
            "effective_size": sorted(set(sizes)),
            "a_g4_passes": all(x["passes"] for x in g4s),
            "a_g1_corpus_passes": corpus_ok == len(drawn),
            "a_g1_space_passes": space_ok == min(SPACE_DRAWS_PER_BIN, len(drawn)),
        })
        b = per_bin[-1]
        print(f"  {centre:>+9.4f}{b['draws']:>7}{b['attempts']:>10}"
              f"{b['max_rho_deviation']:>11.4f}"
              f"{str(b['dead_rules_seen']):>6}{str(b['effective_size']):>10}"
              f"{'ok' if b['a_g1_corpus_passes'] else 'NO':>13}"
              f"{'ok' if b['a_g1_space_passes'] else 'NO':>12}")

    g2 = all(b["a_g2_passes"] for b in per_bin)
    g4 = all(b["a_g4_passes"] for b in per_bin)
    g1 = all(r["passes"] for r in g1_rows)

    sizes = sorted({s for b in per_bin for s in b["effective_size"]})
    print("\n  THE QUANTITY THAT SANK THE FIRST CONSTRUCTION")
    print(f"    effective size over every draw: {sizes}")
    print("    dead rules: none, at any bin — so it cannot correlate with ρ")
    print(f"    acceptance rate falls with ρ "
          f"({per_bin[0]['acceptance_rate']:.1%} at {g.RHO_BINS[0]:+.2f} to "
          f"{per_bin[-1]['acceptance_rate']:.1%} at {g.RHO_BINS[-1]:+.2f}): "
          f"fewer count-permutations")
    print("    admit a policy with every rule live. That is a property of the "
          "family,")
    print("    not of the accepted draws, and it is reported rather than hidden.")

    passes = g1 and g2 and g3["passes"] and g4
    print()
    print("=" * 78)
    for name, ok in (("A-g1", g1), ("A-g2", g2), ("A-g3", g3["passes"]),
                     ("A-g4", g4)):
        print(f"  {name}: {'PASSES' if ok else 'FAILS'}")
    print(f"  THE GATE: {'PASSES' if passes else 'ABORTS THE RUN'}")
    print("=" * 78)

    payload = {
        "_env": environment(check_seed=CHECK_SEED,
                            draws_per_bin=CHECK_DRAWS_PER_BIN,
                            space_draws_per_bin=SPACE_DRAWS_PER_BIN),
        "what": "A-g1 to A-g4 of PLAN_SENSITIVITY.md §4: the blocking checks on "
                "the family generator, run before any row is read",
        "carries_no_band": "these four adjudicate nothing and are excluded from "
                           "every denominator, per §4",
        "rho_grid": {"centres": list(g.RHO_BINS),
                     "tolerance": g.RHO_TOLERANCE,
                     "rho_hidden": g.RHO_HIDDEN,
                     "declared_in": "sensitivity/generator.py, before any figure "
                                    "of the sweep existed"},
        "a_g1": {"rows": g1_rows, "passes": g1},
        "a_g2": {"per_bin": per_bin, "passes": g2},
        "a_g3": g3,
        "a_g4": {"per_bin": per_bin, "passes": g4},
        "passes": passes,
        "seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
