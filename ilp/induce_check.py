"""
`I-g1` TO `I-g4` — the blocking checks of §4, run first and alone.

They carry no band, adjudicate nothing and are excluded from every denominator.
**Each one aborts the run.** It matters more here than anywhere else in this
repository, and §4 says why: **this competitor is one we wrote, and a home-made
baseline that loses proves nothing at all.**

--------------------------------------------------------------------------
WHAT EACH ONE IS FOR
--------------------------------------------------------------------------
`I-g1` · **Step 0 for the inducer.** Given complete labels over all 134,400
cases, it must return a decision list scoring **1.0000** over the space. The
target is representable (`I-g2`) and the labels are complete, so anything less is
the search and not the material. **This is the check that decides whether any row
may be believed, and it is the one that killed the clingo encoding** — kept in
`asp_encoding.py` so that failure reproduces.

`I-g2` · **the target is inside the language.** Each of the 29 hidden rules must
be expressible as a body of the declared 224, and the list of 29 must score
1.0000 executed first-match-wins. Without it `I-g1` could fail for a reason that
is not about induction. It is also where the `in` restriction of §2 is checked
rather than argued: `customer_tier` has four values, so
`in [business, enterprise]` is **not** `neq free`.

`I-g3` · **no leak.** The inducer's input is masks and nothing else — not the
hidden rules, not the layer order, not the test split, not the learned base.
Checked on the signature and the module's imports, the way
`tests/test_oracle_separation.py` checks who may see the oracle.

`I-g4` · **the method is heuristic, and every row is read at two beam widths.**
Sequential covering proves nothing, so the gate is the property that can actually
be checked: a figure that changes between the declared beams is not reported as a
verdict. Here it is checked on `I-g1` itself.

Usage:  python3 -m ilp.induce_check
"""

from __future__ import annotations

import inspect
import json
import sys
import time
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL
from harness.provenance import describe as describe_env, environment

from . import induce as ind
from . import instances as inst
from . import language as lang

OUT = Path("results_ilp")
RECORD = "induce_check.json"

# The clingo encoding's failure, from the run that killed it on 2026-08-30 and
# is recorded in §1's amendment. Reproducible with `asp_encoding.py`; kept here
# as the reason this module's inducer is the one it is.
SUPERSEDED = {
    "encoding": "ilp/asp_encoding.py — conditions chosen per slot, clingo 5.8.2",
    "60_cases_60s": {"train": "60/60", "optimum_proved": False},
    "316_cases_60s": {"train": "173/316 = 0.5475", "hit_the_cap": True,
                      "optimum_proved": False},
    "316_cases_300s": {"train": "205/316 = 0.6487", "hit_the_cap": True,
                       "optimum_proved": False},
    "space_fact_base": 16_128_000,
    "why_it_was_replaced": "it cannot fit its own training set, and I-g1's "
                           "instance is 425x larger than the one it fails on",
}


def i_g2() -> dict:
    """The 29 hidden rules, as bodies of the declared language."""
    index = {t: i for i, t in enumerate(lang.language())}
    bodies, missing = [], []
    for rid, conds, action in HIDDEN_DSL:
        body = []
        for attr, op, value in conds:
            key = (attr, op, tuple(value) if isinstance(value, list) else value)
            if key not in index:
                missing.append({"rule": rid, "condition": list(key)})
            else:
                body.append(index[key])
        bodies.append((tuple(sorted(body)), action))

    ext, truth, n = inst.instance("space")
    target = ind.Induced(rules=bodies, beam=0)
    scored = ind.score(target, ext, truth, n)
    return {
        "conditions_in_the_language": len(index),
        "hidden_conditions_outside_it": missing,
        "the_29_score": round(scored["accuracy_end_to_end"], 6),
        "passes": not missing and scored["accuracy_end_to_end"] == 1.0,
    }


def i_g1(beams=ind.BEAM_WIDTHS) -> dict:
    """Complete labels over the space; the list must score 1.0000. Both beams."""
    ext, truth, n = inst.instance("space")
    rows = []
    for beam in beams:
        got = ind.induce(ext, truth, n, beam=beam)
        scored = ind.score(got, ext, truth, n)
        rows.append({
            "beam": beam,
            "n_rules": got.n_rules,
            "n_conditions": got.n_conditions,
            "left_undecided": got.left_undecided,
            "hit_the_cap": got.hit_the_cap,
            "accuracy_end_to_end": round(scored["accuracy_end_to_end"], 6),
            "seconds": got.seconds,
            "passes": scored["accuracy_end_to_end"] == 1.0,
        })
    return {"instance": "space, complete labels, 134,400 cases",
            "rows": rows, "passes": all(r["passes"] for r in rows)}


def i_g3() -> dict:
    """The inducer's input is masks and nothing else."""
    params = list(inspect.signature(ind.induce).parameters)
    source = Path(ind.__file__).read_text()
    forbidden = ("hidden_policy", "true_action", "true_rule_id", "llm_run",
                 "HIDDEN_DSL", "instances")
    imported = [name for name in forbidden if f"import {name}" in source
                or f"from harness.{name}" in source or f"from .{name}" in source]
    return {
        "signature": params,
        "takes_only_masks": params[:3] == ["ext", "truth", "n"],
        "forbidden_names_imported_by_the_inducer": imported,
        "passes": params[:3] == ["ext", "truth", "n"] and not imported,
    }


def i_g4(g1: dict) -> dict:
    """A figure that changes between the declared beams is not a verdict."""
    values = {r["beam"]: r["accuracy_end_to_end"] for r in g1["rows"]}
    stable = len(set(values.values())) == 1
    return {
        "beams": list(ind.BEAM_WIDTHS),
        "the_method_proves_nothing": True,
        "i_g1_by_beam": values,
        "stable_across_beams": stable,
        "passes": stable,
    }


def main() -> int:
    t0 = time.time()
    print("=" * 78)
    print("I-g1 TO I-g4 — the blocking checks of PLAN_ILP.md §4")
    print("=" * 78)
    print(f"  beams {ind.BEAM_WIDTHS} · language {len(lang.language())} "
          f"conditions · bodies up to {lang.MAX_CONDITIONS} · zero API calls")
    print(f"  {describe_env()}")

    print("\n  THE INSTANCES")
    described = {name: inst.describe(name)
                 for name in ("space", "train_316", "train_632", "test")}
    print(f"  {'instance':<12}{'n':>8}{'classes':>9}   by class")
    for name, d in described.items():
        top = ", ".join(f"{k.split('_')[0].lower()} {v}"
                        for k, v in list(d["by_class"].items())[:4])
        print(f"  {name:<12}{d['n']:>8}{d['classes']:>9}   {top} …")
    print("\n  ONCALL_ESCALATION never escalated: "
          f"{'ONCALL_ESCALATION' not in described['train_632']['by_class']}"
          "   — §1's amendment turns on this")

    g2 = i_g2()
    print("\n  I-g2 · THE TARGET IS INSIDE THE LANGUAGE")
    print(f"    conditions {g2['conditions_in_the_language']}   "
          f"hidden conditions outside it "
          f"{len(g2['hidden_conditions_outside_it'])}   "
          f"the 29 score {g2['the_29_score']:.6f}   "
          f"{'PASSES' if g2['passes'] else 'FAILS'}")

    g1 = i_g1()
    print("\n  I-g1 · STEP 0 — complete labels over the 134,400")
    print(f"    {'beam':>6}{'rules':>7}{'conds':>7}{'undecided':>11}"
          f"{'e2e':>10}{'secs':>7}")
    for r in g1["rows"]:
        print(f"    {r['beam']:>6}{r['n_rules']:>7}{r['n_conditions']:>7}"
              f"{r['left_undecided']:>11}{r['accuracy_end_to_end']:>10.6f}"
              f"{r['seconds']:>7.1f}   {'ok' if r['passes'] else 'NO'}")
    print(f"    I-g1: {'PASSES' if g1['passes'] else 'FAILS'}")

    g3 = i_g3()
    print("\n  I-g3 · NO LEAK")
    print(f"    the inducer's signature: {g3['signature']}")
    print(f"    forbidden names it imports: "
          f"{g3['forbidden_names_imported_by_the_inducer'] or 'none'}   "
          f"{'PASSES' if g3['passes'] else 'FAILS'}")

    g4 = i_g4(g1)
    print("\n  I-g4 · HEURISTIC, AND READ AT TWO BEAMS")
    print(f"    I-g1 by beam: {g4['i_g1_by_beam']}   "
          f"stable {g4['stable_across_beams']}   "
          f"{'PASSES' if g4['passes'] else 'FAILS'}")

    passes = g1["passes"] and g2["passes"] and g3["passes"] and g4["passes"]
    print()
    print("=" * 78)
    for name, ok in (("I-g1", g1["passes"]), ("I-g2", g2["passes"]),
                     ("I-g3", g3["passes"]), ("I-g4", g4["passes"])):
        print(f"  {name}: {'PASSES' if ok else 'FAILS'}")
    print(f"  THE GATE: {'PASSES' if passes else 'ABORTS THE RUN'}")
    print("=" * 78)

    payload = {
        "_env": environment(beams=list(ind.BEAM_WIDTHS),
                            max_conditions=lang.MAX_CONDITIONS,
                            max_rules=ind.MAX_RULES),
        "what": "I-g1 to I-g4 of PLAN_ILP.md §4: the blocking checks on the "
                "inducer, run before any row is read",
        "carries_no_band": "these four adjudicate nothing and are excluded from "
                           "every denominator, per §4",
        "instances": described,
        "superseded_encoding": SUPERSEDED,
        "i_g1": g1, "i_g2": g2, "i_g3": g3, "i_g4": g4,
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
