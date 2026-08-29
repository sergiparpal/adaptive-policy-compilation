"""
THE HYBRID CEILING ON THE EXHAUSTIVE SPACE — is the 1.0000 the sample or the
policy?

--------------------------------------------------------------------------
WHOSE IDEA THIS IS, AND WHY IT WAS STILL OPEN
--------------------------------------------------------------------------
Not this module's. `ARBITRATION_REPORT.md` §9.2, limit 2: *"The hybrid engine's
1.0000 is a corpus figure. Over the exhaustive space that engine has not been
measured, and this report has argued in §6 that the two surfaces do not even rank
the same. It is the cheapest pending check of all the ones named here."* It
carried no erratum, so it was still open on 2026-08-29, when
`EXTERNAL_REVIEW.md` reached it again from outside and made it item 3 of its
plan.

`rung2/ceiling_check2.py` already builds the engine and already constructs
`Space()` — it needs the exhaustive space to compute the extensions in the first
place. What was missing was the second index set: it scores over the 2,000
arrivals and never over the 134,400 cases whose masks it just built.

--------------------------------------------------------------------------
WHAT 1.0000 MEANS ON EACH SURFACE, AND WHY THE DIFFERENCE IS THE POINT
--------------------------------------------------------------------------
The distinction is `rung3/optimizer_check.py`'s and it is borrowed whole:

  corpus   2,000 draws touching 1,743 distinct cases out of 134,400. 1.0000 here
           means *"fits the sample"*, and the sample leaves the rest of the
           function unconstrained — an order can be perfect on the corpus and be
           0.9455 as a function (`results3/FINDINGS_AUDIT.md`, Step 0).
  space    all 134,400 combinations, each counted once. 1.0000 here means the
           engine is **policy-equivalent** to the hidden policy: on every case it
           can ever be shown, it decides what first-match-wins decides. Strictly
           stronger, and the one worth reporting.

--------------------------------------------------------------------------
PROVENANCE: POST-RUN, AND ONE PART OF IT COULD HAVE BEEN A BET
--------------------------------------------------------------------------
Written after the figures were seen. No band was drafted, none is claimed, and no
signed row moves. **But unlike item 2's control, this one's figures did not
exist**: §4 of `EXTERNAL_REVIEW.md` says items 4 and 5 are *"the only two whose
figures do not yet exist and which therefore can be pre-registered"*, and about
this item that is wrong. The record says so rather than letting it pass.

The mitigation is partial and it is worth stating exactly. **The ceiling itself
was derivable in advance** from two facts already in the records — see the proof
below — so a band on it would have been a bet on arithmetic. **The rest was
not**: what level 1 alone scores over the space, and how much of the declared
priority the corpus never exercises, were open questions with no derivation
behind them, and they could have carried a signed band.

--------------------------------------------------------------------------
WHY THE ANSWER IS NOT LUCK — the proof, and the three premises it needs
--------------------------------------------------------------------------
Let `A` be the earliest-born rule matching a case, so `action(A)` is the truth
(first-match-wins is the policy's semantics). For any other matching rule `B`,
born later, exactly one of these holds:

  * `ext(B) ⊊ ext(A)` — then subsumption makes B beat A, which **contradicts the
    layer order**. Premise 1 says there are none.
  * `ext(A) ⊊ ext(B)` — subsumption makes A beat B. B is defeated.
  * incomparable, and `action(A) ≠ action(B)` — they overlap (both match this
    case), so `hidden_priority` declares the edge A → B. Premise 2 says the
    validator rejected none; premise 3 says none is missing. B is defeated.
  * incomparable, and `action(A) = action(B)` — B may survive undefeated, and it
    does not matter: it carries the same action.

So the undefeated set always contains `A`, never contains a rule with a different
action, and the engine returns `action(A)` — on **every** case, not on the 1,743
the corpus happens to touch. The premises are not assumed here: all three are
measured, they are blocking, and each is a fact some other record already
publishes.

That is why the interesting figures below are the other three.

--------------------------------------------------------------------------
WHAT THE CORPUS COULD NOT HAVE SAID
--------------------------------------------------------------------------
1. **Level 1 alone**, measured on both surfaces. Rung 1 published subsumption's
   coverage over the corpus and nothing over the space.
2. **What the 199 edges buy**, per surface — the gap between the two levels, which
   is the same thing read as authorship cost.
3. **How much of that authorship the corpus never exercises.** An edge whose two
   endpoints never match the same arriving ticket decides nothing on the corpus,
   whatever it is worth to the policy. Counting them is what turns *"the 199 are
   the authorship cost"* into a claim with a surface attached.

**On removability, precisely.** An edge that is never the SOLE defeater of its
loser on a surface can be deleted, one at a time, without changing a single
decision on that surface: wherever it fires, something else already defeats the
same rule. That does **not** license deleting a set of them at once — two edges
can be individually redundant and jointly necessary — and this module does not
measure joint removability.

Usage:  python3 -m rung2.ceiling_check2_space
"""

from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import generate_corpus
from harness.dsl import Condition
from harness.hidden_policy import true_action
from harness.provenance import describe, environment

from .engine2 import PriorityEngine, Rule2, Space, strictly_below
from .hidden_priority import build_hidden_engine

OUT = Path("results2")
RECORD = "ceiling2_space.json"

N_CORPUS, SEED = 2000, 17

CORPUS = "corpus (n=2000, seed 17)"
SPACE = "exhaustive space (134,400)"

HYBRID = "hybrid (subsumption + 199 declared edges)"
LEVEL1 = "subsumption alone (level 1)"

# Published rows this run is measured beside. They are re-measured here and they
# BLOCK: a ceiling on a second surface is worth nothing if the first has moved.
#   results2/FINDINGS2.md, "Two different claims"      -> the hybrid corpus row
#   results/FINDINGS.md, route 3                       -> level 1 on the corpus
GATE_HYBRID_CORPUS = {"action": 2000, "conflict": 0, "impasse": 0,
                      "e2e": 1.0000, "silent": 0.0000}
GATE_LEVEL1_CORPUS = {"action": 1263, "conflict": 737, "impasse": 0,
                      "e2e": 0.6315, "silent": 0.0000}
GATE_DECLARED_EDGES = 199         # results2/FINDINGS2.md; tests/test_ceilings.py
GATE_SUBSUMPTION_PAIRS = 61       # idem


# ---------------------------------------------------------------------------
# The two engines. The ONLY difference between them is level 2.
# ---------------------------------------------------------------------------

def build_level1_engine(space: Space) -> PriorityEngine:
    """The same 29 rules, loaded the same way, with no declared edge at all.

    The loading loop is `hidden_priority.build_hidden_engine`'s first half on
    purpose: `gate_the_two_engines_differ_only_in_level_2` checks afterwards that
    the extensions and the subsumption relation came out identical, so the
    comparison below isolates the edges and nothing else."""
    engine = PriorityEngine(space=space)
    for i, (rid, conds, action) in enumerate(HIDDEN_DSL):
        engine.add(Rule2(
            rule_id=rid,
            conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds],
            action=action,
            note="transcripcion literal de hidden_policy",
        ), born_at=i, keep_id=True)
    return engine


# ---------------------------------------------------------------------------
# The three premises of the proof, measured rather than assumed
# ---------------------------------------------------------------------------

def check_premises(engine: PriorityEngine, stats: dict) -> dict:
    """1. subsumption never contradicts the layer order,
       2. the validator rejected no declared edge,
       3. no pair that needs an edge is missing one."""
    rules = engine.rules
    contradictions, missing = [], []
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            a, b = rules[i], rules[j]          # i < j: a is from an earlier layer
            ea, eb = engine.ext[a.rule_id], engine.ext[b.rule_id]
            if strictly_below(eb, ea):
                contradictions.append([a.rule_id, b.rule_id])
                continue
            if ea & eb == 0 or strictly_below(ea, eb):
                continue
            if a.action == b.action:
                continue
            if a.rule_id not in engine.decl_below.get(b.rule_id, set()):
                missing.append([a.rule_id, b.rule_id])
    return {
        "subsumption_contradicts_the_layer_order": contradictions,
        "edges_rejected_by_the_validator": [list(e) for e in stats["rejected"]],
        "pairs_that_need_an_edge_and_lack_one": missing,
        "passes": not contradictions and not stats["rejected"] and not missing,
    }


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def measure(engine: PriorityEngine, cases, surface: str, arbitration: str) -> dict:
    out = collections.Counter()
    ok = 0
    for case in cases:
        outcome, winner, _ = engine.decide(case)
        out[outcome] += 1
        if outcome == "ACTION" and winner.action == true_action(case):
            ok += 1
    n, act = len(cases), out["ACTION"]
    return {
        "surface": surface,
        "arbitration": arbitration,
        "n": n,
        "action": act,
        "conflict": out["CONFLICT"],
        "impasse": out["IMPASSE"],
        "coverage": round(act / n, 6),
        "correct": ok,
        "accuracy_end_to_end": round(ok / n, 6),
        "silent_error_rate": round(1 - ok / act, 6) if act else 0.0,
        "silent_errors_abs": act - ok,
    }


def edge_work(engine: PriorityEngine, cases, surface: str) -> dict:
    """What each declared edge actually does on this surface.

      fires  both endpoints match the same case, so the edge is consulted.
      sole   it is the ONLY thing defeating its loser on that case AND the loser
             carries a different action from the truth — so deleting this one
             edge would turn that ACTION into a CONFLICT.

    An edge that never comes out `sole` is individually removable on this surface
    (see the docstring: individually, not jointly)."""
    rules = engine.rules
    action = {r.rule_id: r.action for r in rules}
    fires, sole = collections.Counter(), collections.Counter()
    needs_an_edge = 0
    for case in cases:
        matched = [r for r in rules if r.matches(case)]
        ids = {r.rule_id for r in matched}
        truth = true_action(case)
        needed = False
        for loser in matched:
            lid = loser.rule_id
            by_sub = engine.sub_below[lid] & ids
            by_edge = engine.decl_below[lid] & ids
            for w in by_edge:
                fires[(w, lid)] += 1
            if by_edge and not by_sub and action[lid] != truth:
                needed = True
                if len(by_edge) == 1:
                    sole[(next(iter(by_edge)), lid)] += 1
        if needed:
            needs_an_edge += 1
    return {
        "surface": surface,
        "n": len(cases),
        "cases_whose_decision_needs_a_declared_edge": needs_an_edge,
        "edges_that_ever_fire": len(fires),
        "edges_ever_sole_defeater": len(sole),
        "fires": fires,
        "sole": sole,
    }


# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    space = Space()
    engine, declared, stats = build_hidden_engine(space)
    level1 = build_level1_engine(space)
    corpus = generate_corpus(N_CORPUS, seed=SEED)
    cases = list(all_cases())

    print("=" * 78)
    print("THE HYBRID CEILING ON THE EXHAUSTIVE SPACE — the sample, or the "
          "policy?")
    print("=" * 78)
    print(f"  {len(engine.rules)} rules · {len(declared)} declared edges · "
          f"{space.n:,} cases in the space · zero API calls")
    print("  POST-RUN: no band was drafted and no signed row moves")
    print(f"  {describe()}")

    # ---- GATE 1: the two engines differ only in level 2 --------------------
    same_ext = engine.ext == level1.ext
    same_sub = (engine.sub_below == level1.sub_below
                and engine.sub_above == level1.sub_above)
    no_edges = all(not s for s in level1.decl_below.values())
    gate_engines = same_ext and same_sub and no_edges

    # ---- GATE 2: the published rows -----------------------------------------
    m_hyb_corpus = measure(engine, corpus, CORPUS, HYBRID)
    m_lv1_corpus = measure(level1, corpus, CORPUS, LEVEL1)
    gate_rows = []
    for got, want, name in ((m_hyb_corpus, GATE_HYBRID_CORPUS,
                             "hybrid · corpus · results2/FINDINGS2.md"),
                            (m_lv1_corpus, GATE_LEVEL1_CORPUS,
                             "level 1 · corpus · results/FINDINGS.md route 3")):
        for k in ("action", "conflict", "impasse"):
            gate_rows.append({"row": name, "field": k, "measured": got[k],
                              "published": want[k], "passes": got[k] == want[k]})
        for k, field in (("e2e", "accuracy_end_to_end"),
                         ("silent", "silent_error_rate")):
            m = round(got[field], 4)
            gate_rows.append({"row": name, "field": k, "measured": m,
                              "published": want[k], "passes": m == want[k]})
    gate_rows.append({"row": "structure", "field": "declared edges",
                      "measured": len(declared), "published": GATE_DECLARED_EDGES,
                      "passes": len(declared) == GATE_DECLARED_EDGES})
    sub_pairs = sum(len(s) for s in engine.sub_below.values())
    gate_rows.append({"row": "structure", "field": "subsumption pairs",
                      "measured": sub_pairs, "published": GATE_SUBSUMPTION_PAIRS,
                      "passes": sub_pairs == GATE_SUBSUMPTION_PAIRS})

    # ---- GATE 3: the three premises of the proof ---------------------------
    premises = check_premises(engine, stats)

    print()
    print("=" * 78)
    print("GATES — the published rows, the premises, and that only level 2 "
          "differs")
    print("=" * 78)
    print(f"  {'row':<48}{'field':<18}{'measured':>10}{'published':>11}")
    for g in gate_rows:
        print(f"  {g['row']:<48}{g['field']:<18}{g['measured']:>10}"
              f"{g['published']:>11}" + ("  ok" if g["passes"] else "  NO"))
    print(f"\n  the two engines differ only in level 2: "
          f"{'ok' if gate_engines else 'NO'}"
          f"   (same extensions {same_ext}, same subsumption {same_sub}, "
          f"level 1 has no edges {no_edges})")
    print("\n  PREMISES OF THE PROOF (each one is a fact another record "
          "publishes)")
    print(f"    subsumption contradicting the layer order : "
          f"{len(premises['subsumption_contradicts_the_layer_order'])}")
    print(f"    declared edges rejected by the validator  : "
          f"{len(premises['edges_rejected_by_the_validator'])}")
    print(f"    pairs needing an edge and lacking one     : "
          f"{len(premises['pairs_that_need_an_edge_and_lack_one'])}")

    gates_pass = (all(g["passes"] for g in gate_rows) and gate_engines
                  and premises["passes"])
    if not gates_pass:
        print()
        print("  STOP. Either a published row has moved or a premise of the "
              "proof")
        print("  is false. Both change what the space figure below would mean, "
              "so")
        print("  find out what changed and date the erratum in the FINDINGS "
              "that")
        print("  owns it. Do not adjust to fit (hard rule 6).")
        return 1
    print("\n  GATES PASS. The corpus rows reproduce and the proof's premises "
          "hold.")

    # ---- THE FOUR ROWS -----------------------------------------------------
    rows = [m_hyb_corpus,
            measure(engine, cases, SPACE, HYBRID),
            m_lv1_corpus,
            measure(level1, cases, SPACE, LEVEL1)]

    print()
    print("=" * 78)
    print("THE CEILING, BY LEVEL AND BY SURFACE · perfect policy loaded, no LLM")
    print("=" * 78)
    print(f"  {'surface':<28}{'arbitration':<42}{'coverage':>10}{'e2e':>9}"
          f"{'CONFLICT':>10}{'silent':>8}")
    for r in rows:
        print(f"  {r['surface']:<28}{r['arbitration']:<42}"
              f"{r['coverage']:>10.4f}{r['accuracy_end_to_end']:>9.4f}"
              f"{r['conflict']:>10}{r['silent_errors_abs']:>8}")

    space_row = rows[1]
    passes = (space_row["accuracy_end_to_end"] == 1.0
              and space_row["silent_errors_abs"] == 0
              and space_row["conflict"] == 0 and space_row["impasse"] == 0)
    print()
    print("  STEP 0 ON THE SPACE -> " + ("PASSES" if passes else "DOES NOT PASS"))
    print("  1.0000 over all 134,400 combinations is not `fits the sample`: the")
    print("  engine decides what first-match-wins decides on every case there "
          "is.")

    # ---- WHAT THE EDGES BUY, PER SURFACE -----------------------------------
    print()
    print("=" * 78)
    print("WHAT THE 199 EDGES BUY, AND HOW MUCH OF THEM THE CORPUS EVER SEES")
    print("=" * 78)
    work = {CORPUS: edge_work(engine, corpus, CORPUS),
            SPACE: edge_work(engine, cases, SPACE)}

    buys = {}
    for surface in (CORPUS, SPACE):
        hyb = next(r for r in rows if r["surface"] == surface
                   and r["arbitration"] == HYBRID)
        lv1 = next(r for r in rows if r["surface"] == surface
                   and r["arbitration"] == LEVEL1)
        w = work[surface]
        buys[surface] = {
            "level_1_alone": lv1["accuracy_end_to_end"],
            "hybrid": hyb["accuracy_end_to_end"],
            "bought_by_the_edges": round(hyb["accuracy_end_to_end"]
                                         - lv1["accuracy_end_to_end"], 6),
            "cases_needing_an_edge": w["cases_whose_decision_needs_a_declared_edge"],
            "level_1_conflicts": lv1["conflict"],
            "consistent": (w["cases_whose_decision_needs_a_declared_edge"]
                           == lv1["conflict"]),
            "edges_that_ever_fire": w["edges_that_ever_fire"],
            "edges_never_firing": len(declared) - w["edges_that_ever_fire"],
            "edges_ever_sole_defeater": w["edges_ever_sole_defeater"],
        }
        b = buys[surface]
        print(f"\n  {surface}")
        print(f"    level 1 alone {b['level_1_alone']:.4f}  ->  hybrid "
              f"{b['hybrid']:.4f}   the edges buy {b['bought_by_the_edges']:+.4f}")
        print(f"    cases whose decision needs a declared edge: "
              f"{b['cases_needing_an_edge']:,}"
              f"  ({b['cases_needing_an_edge']/w['n']:.4f})"
              f"   = level 1's conflicts: {'ok' if b['consistent'] else 'NO'}")
        print(f"    edges that ever fire      : {b['edges_that_ever_fire']:>3} "
              f"of {len(declared)}   "
              f"({b['edges_never_firing']} never fire on this surface)")
        print(f"    edges ever sole defeater  : "
              f"{b['edges_ever_sole_defeater']:>3} of {len(declared)}   "
              f"(the rest are individually removable HERE, not jointly)")

    if not all(b["consistent"] for b in buys.values()):
        print()
        print("  STOP. `needs a declared edge` must equal level 1's CONFLICT "
              "count:")
        print("  they are two ways of counting the same cases. They disagree, "
              "so one")
        print("  of the two is wrong and neither figure may be published.")
        return 1

    only_space = sorted(set(work[SPACE]["sole"]) - set(work[CORPUS]["sole"]))
    only_corpus = sorted(set(work[CORPUS]["sole"]) - set(work[SPACE]["sole"]))
    never_corpus = sorted(set(e for e in declared)
                          - set(work[CORPUS]["fires"]))
    print()
    print("  THE ASYMMETRY, WHICH IS THE POINT")
    print(f"    edges the corpus never exercises at all      : "
          f"{len(never_corpus)} of {len(declared)}")
    print(f"    sole defeater on the space, never on corpus  : {len(only_space)}")
    print(f"    sole defeater on the corpus, never on space  : {len(only_corpus)}")
    print("    the corpus's load-bearing set is a subset of the space's, so the")
    print("    authorship cost read off the arrivals is a floor, not the price.")
    print(f"    first ten never exercised: "
          f"{', '.join(f'{a}->{b}' for a, b in never_corpus[:10])}")

    payload = {
        "_env": environment(n_corpus=N_CORPUS, seed=SEED),
        "what": "the rung 2 hybrid ceiling measured over the exhaustive space "
                "as well as the corpus, with level 1 alone on both surfaces and "
                "what the 199 declared edges buy on each",
        "provenance": "POST-RUN. Written after the figures were seen; no band "
                      "was drafted, none is claimed, no signed row moves. Unlike "
                      "item 2's control the figures did not exist beforehand, so "
                      "the ceiling could have been pre-registered — though it was "
                      "derivable from two facts already recorded, which the "
                      "module's proof gives. The level-1 space figure and the "
                      "edge asymmetry were not derivable and could have carried a "
                      "band. EXTERNAL_REVIEW.md §4 says items 4 and 5 are the "
                      "only ones whose figures do not yet exist; about this item "
                      "that is wrong.",
        "closes": "ARBITRATION_REPORT.md §9.2, limit 2 — 'the cheapest pending "
                  "check of all the ones named here'; item 3 of "
                  "EXTERNAL_REVIEW.md's plan",
        "meaning": {
            CORPUS: "1.0000 means it fits the sample: 2,000 draws touch 1,743 "
                    "distinct cases and leave the rest of the function "
                    "unconstrained",
            SPACE: "1.0000 means policy-equivalent: on every case that exists, "
                   "the engine decides what first-match-wins decides",
        },
        "gates": {"rows": gate_rows,
                  "engines_differ_only_in_level_2": gate_engines,
                  "premises": premises,
                  "passes": gates_pass},
        "n_rules": len(engine.rules),
        "declared_edges": len(declared),
        "subsumption_pairs": sub_pairs,
        "rows": rows,
        "step_0_on_the_space": passes,
        "what_the_edges_buy": buys,
        "edge_asymmetry": {
            "edges_never_exercised_by_the_corpus": [list(e) for e in never_corpus],
            "sole_defeater_on_the_space_only": [list(e) for e in only_space],
            "sole_defeater_on_the_corpus_only": [list(e) for e in only_corpus],
        },
        "per_edge": [{
            "winner": w, "loser": l,
            "fires_corpus": work[CORPUS]["fires"].get((w, l), 0),
            "fires_space": work[SPACE]["fires"].get((w, l), 0),
            "sole_corpus": work[CORPUS]["sole"].get((w, l), 0),
            "sole_space": work[SPACE]["sole"].get((w, l), 0),
        } for w, l in declared],
        "seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
