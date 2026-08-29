"""
THE DEFAULT-RULE CONTROL — how much of rung 1's headline failure is the DSL's
one-condition minimum rather than the priority/specificity thesis it is cited for.

--------------------------------------------------------------------------
PROVENANCE, FIRST, BECAUSE IT IS NOT A PRE-REGISTERED MEASUREMENT
--------------------------------------------------------------------------
POST-RUN. The two corpus rows this module owns were run in memory on 2026-08-29
during the adjudication of `EXTERNAL_REVIEW.md`, and its §3 prints them with the
warning that they were owned by nothing and produced by no module in the tree.
This is that module. **Nothing here is a bet that could have failed**: whoever
wrote it had already seen 0.6880. The record declares `provenance: POST-RUN`, the
convention `edge_direction` and `edge_budget` already use, and no signed row is
touched — item 2 of that plan says so before any of this existed.

What it can be worth is the rest: the pair is now reproducible, owned, labelled
by surface, and pinned by a test.

--------------------------------------------------------------------------
THE ARTIFACT
--------------------------------------------------------------------------
`H29` is the hidden policy's default: `lambda c: True`. It has NO conditions.
`validate_rule_payload` requires at least one, so `ceiling_check.HIDDEN_DSL`
encodes it as `severity gte 1`, which is true over the whole domain — and
`RuleEngine.decide` counts conditions, so the catch-all arrives at arbitration
with specificity 1 and **ties with every single-condition layer rule instead of
yielding to it**. `results/FINDINGS.md`, route 1, names that mechanism. Nothing
in the repository quantified it.

--------------------------------------------------------------------------
WHAT IS MEASURED, AND WHAT IS NOT
--------------------------------------------------------------------------
The same criterion — most conditions wins, ties with different actions are a
CONFLICT — applied to the policy AS WRITTEN instead of to the transcription the
schema forced. A condition is *vacuous* when it holds for every value in its
attribute's declared domain; the effective specificity of a rule is the number of
its conditions that are not vacuous. For 28 of the 29 rules that is exactly the
DSL's count; for `H29` it is 0.

**This is oracle-free and that is what makes it a control.** Vacuity is decided
from `DOMAINS` and the rule itself: no layer order, no `true_action`, nothing the
criterion would not have on a learned base. Handing `H28` — a defaults-layer rule
with a real condition — a lower rank *would* need the layer order, and would be
giving the criterion the answer it is being tested on. That line is the whole
difference between correcting an ENCODING artifact and inventing a priority one,
and it is not crossed here.

**No frozen file is touched** (hard rule 1). The alternative ranking lives in this
module and reuses `Rule.matches()` from the DSL, exactly as `ceiling_check.py`
does for `decide_by_priority`. **The published 0.5875 does not move**: it is
re-measured here through `RuleEngine.decide` and `ceiling_check.measure`, the same
two objects that produced it, and it is a blocking gate rather than a row.

--------------------------------------------------------------------------
TWO SURFACES, BOTH REPORTED
--------------------------------------------------------------------------
`STATUS.md`, *Before reading any figure*: the corpus is the modelled arrival
distribution and the exhaustive space is the uniform measure over 134,400
combinations; they answer different questions and neither is *the* bound. Rung 1
published corpus figures without saying so. This does not continue that — and the
two surfaces disagree about the size of the effect in percentage points while
agreeing exactly about its nature.

--------------------------------------------------------------------------
WHY A CONFLICT THIS CONTROL RESOLVES IS ALWAYS RESOLVED CORRECTLY
--------------------------------------------------------------------------
It is a proof, not a regularity, and it is checked on both surfaces anyway
(`gate_no_action_changes`, `gate_no_resolution_is_wrong`), because a proof about
code that stops being true is worth catching.

A case can only move where the catch-all is a finalist under the published
encoding, which requires the top specificity to be 1. Give `H29` its true rank and
the finalists become the matching single-condition rules. If they disagree the
case stays a CONFLICT. If they agree on action A, then the whole matching set is
those rules plus `H29` — no rule with two or more conditions matched, or the top
would not have been 1 — and `H29` is born last, so **first-match-wins picks one of
them and A is the true action**. Nothing can be lost: cases already decided keep
their action, since removing `H29` from a set of finalists that agreed leaves the
same action, and where it matched alone it still wins.

So the control converts abstentions into correct decisions and can never create a
silent error. The silent-error COUNT is identical in both arbitrations on both
surfaces; only its denominator moves.

--------------------------------------------------------------------------
HOW TO READ THE RESULT, AND NO FURTHER
--------------------------------------------------------------------------
The finding survives: the corrected figure is nowhere near 1.0000, and the
impossibility that falsifies specificity as a criterion — `H01` (2 conditions)
must beat `H03` (1), `H16` (1) must beat `H24` (2) — is untouched by any of this,
because it is internal to the policy and mentions no encoding. What moves is how
much of rung 1's conflict rate may be cited as evidence for the thesis, and the
answer is: not all of it. The residue printed at the foot is what the thesis is
made of — finalists of equal effective specificity, different actions, and a
design order the criterion cannot see.

The per-class table is where the reading gets sharp, and it is the one CLAUDE.md
Step 5 asks for: the whole gain sits in the two commonest classes, and the two
critical rare ones — `SECURITY_INCIDENT`, `ONCALL_ESCALATION` — get nothing.

Usage:  python3 -m harness.default_rule_control
"""

from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

from .ceiling_check import all_cases, build_rules, measure
from .domain import DOMAINS, generate_corpus
from .dsl import Condition, Rule, RuleEngine
from .hidden_policy import true_action
from .provenance import describe, environment

OUT = Path("results")
RECORD = "default_rule_control.json"

CATCHALL = "H29"           # the policy's default: `lambda c: True`
N_CORPUS, SEED = 2000, 17

CORPUS = "corpus (n=2000, seed 17)"
SPACE = "exhaustive space (134,400)"

PUBLISHED = "specificity, as published"
CONTROL = "specificity, catch-all at its true rank"

# The row of `results/FINDINGS.md`, route 1, to the digit it publishes. Blocking:
# if this does not come back, this module is not measuring beside that figure and
# nothing below may be read against it.
PUBLISHED_ROW = {
    "action": 1495, "impasse": 0, "conflict": 505, "silent_errors_abs": 320,
    "coverage": 0.7475, "silent_error_rate": 0.2140, "accuracy_end_to_end": 0.5875,
}

TOP_RESIDUE = 10           # residual conflict finalist sets printed per surface


# ---------------------------------------------------------------------------
# Effective specificity: the conditions that constrain
# ---------------------------------------------------------------------------

def is_vacuous(cond: Condition) -> bool:
    """True when the condition holds for every value in its attribute's declared
    domain, i.e. it costs a condition slot and constrains nothing."""
    return all(cond.holds(SimpleNamespace(**{cond.attr: v}))
               for v in DOMAINS[cond.attr])


def effective_specificity(rule: Rule) -> int:
    return sum(1 for c in rule.conditions if not is_vacuous(c))


def decide_by_effective_specificity(rules: list[Rule], spec: dict[str, int],
                                    case, matched: list[Rule] | None = None):
    """`RuleEngine.decide` with `spec` in place of `Rule.specificity`. Same
    tie-breaks, same three outcomes; reuses `Rule.matches()` from the DSL."""
    if matched is None:
        matched = [r for r in rules if r.matches(case)]
    if not matched:
        return "IMPASSE", None, []
    top = max(spec[r.rule_id] for r in matched)
    finalists = [r for r in matched if spec[r.rule_id] == top]
    if len({r.action for r in finalists}) > 1:
        return "CONFLICT", None, finalists
    return "ACTION", min(finalists, key=lambda r: r.born_at), matched


# ---------------------------------------------------------------------------
# The artifact, described rather than assumed
# ---------------------------------------------------------------------------

def describe_artifact(rules: list[Rule], spec: dict[str, int]) -> dict:
    vacuous = {r.rule_id: [c.as_dict() for c in r.conditions if is_vacuous(c)]
               for r in rules}
    vacuous = {k: v for k, v in vacuous.items() if v}
    catchall = next(r for r in rules if r.rule_id == CATCHALL)
    return {
        "rule": CATCHALL,
        "in_the_policy": "lambda c: True",
        "in_the_dsl": [c.as_dict() for c in catchall.conditions],
        "why": "validate_rule_payload requires at least one condition",
        "specificity_in_the_dsl": catchall.specificity,
        "effective_specificity": spec[CATCHALL],
        "rules_with_a_vacuous_condition": sorted(vacuous),
        "vacuous_conditions": vacuous,
    }


# ---------------------------------------------------------------------------
# One pass per surface: the two arbitrations, case by case
# ---------------------------------------------------------------------------

def compare(cases, rules, engine, spec) -> dict:
    """What the control moves, and the two invariants that say what it cannot
    move. One pass over the surface.

    The published side goes through `RuleEngine.decide` untouched — it recomputes
    its own `matched`, and that is the point: the row it produces has to be the
    frozen engine's, not a reimplementation of it that happens to agree."""
    moved = collections.Counter()
    per_class_resolved = collections.Counter()
    per_class = collections.defaultdict(collections.Counter)
    residue = collections.Counter()
    with_catchall = 0
    action_changes = []          # must stay empty (see the docstring's proof)
    resolutions_wrong = []       # must stay empty

    for case in cases:
        matched = [r for r in rules if r.matches(case)]
        pub_out, pub_win, pub_fin = engine.decide(case)
        ctl_out, ctl_win, ctl_fin = decide_by_effective_specificity(
            rules, spec, case, matched=matched)
        truth = true_action(case)
        per_class[truth][f"pub_{pub_out}"] += 1
        per_class[truth][f"ctl_{ctl_out}"] += 1
        if pub_out == "ACTION" and pub_win.action == truth:
            per_class[truth]["pub_correct"] += 1
        if ctl_out == "ACTION" and ctl_win.action == truth:
            per_class[truth]["ctl_correct"] += 1

        if pub_out == "ACTION":
            if ctl_out != "ACTION" or ctl_win.action != pub_win.action:
                action_changes.append(case)
        elif pub_out == "CONFLICT":
            if CATCHALL in {r.rule_id for r in pub_fin}:
                with_catchall += 1
            if ctl_out == "ACTION":
                moved["resolved"] += 1
                if ctl_win.action == truth:
                    moved["resolved_correct"] += 1
                    per_class_resolved[truth] += 1
                else:
                    moved["resolved_wrong"] += 1
                    resolutions_wrong.append(case)
            else:
                moved["still_conflict"] += 1
        if ctl_out == "CONFLICT":
            residue[tuple(sorted(r.rule_id for r in ctl_fin))] += 1

    born = {r.rule_id: r.born_at for r in rules}
    action = {r.rule_id: r.action for r in rules}
    top = [{
        "finalists": list(ids),
        "actions": [action[i] for i in ids],
        "effective_specificity": spec[ids[0]],
        "first_match_wins": min(ids, key=lambda i: born[i]),
        "cases": n,
    } for ids, n in residue.most_common(TOP_RESIDUE)]

    return {
        "published_conflicts_with_the_catchall_as_finalist": with_catchall,
        "of_those_resolved": moved["resolved"],
        "resolved_correct": moved["resolved_correct"],
        "resolved_wrong": moved["resolved_wrong"],
        "still_conflict": moved["still_conflict"],
        "resolved_by_true_class": dict(per_class_resolved),
        "residual_conflict_sets": len(residue),
        "residual_conflict_sets_with_the_catchall": sum(
            1 for ids in residue if CATCHALL in ids),
        "top_residual_conflicts": top,
        "per_class": {k: dict(v) for k, v in per_class.items()},
        "gate_no_action_changes": not action_changes,
        "gate_no_resolution_is_wrong": not resolutions_wrong,
    }


def row(m: dict, surface: str, arbitration: str) -> dict:
    return {
        "surface": surface,
        "arbitration": arbitration,
        "n": m["n"],
        "action": m["action"],
        "impasse": m["impasse"],
        "conflict": m["conflict"],
        "coverage": round(m["coverage"], 6),
        "silent_errors_abs": m["silent_errors_abs"],
        "silent_error_rate": round(m["silent_error_rate"], 6),
        "accuracy_end_to_end": round(m["accuracy_end_to_end"], 6),
    }


def check_published(m: dict) -> dict:
    """The gate. Integers exactly; the three rates to the four decimals the
    record publishes."""
    checks = {}
    for k in ("action", "impasse", "conflict", "silent_errors_abs"):
        checks[k] = {"measured": m[k], "published": PUBLISHED_ROW[k],
                     "passes": m[k] == PUBLISHED_ROW[k]}
    for k in ("coverage", "silent_error_rate", "accuracy_end_to_end"):
        got = round(m[k], 4)
        checks[k] = {"measured": got, "published": PUBLISHED_ROW[k],
                     "passes": got == PUBLISHED_ROW[k]}
    return checks


# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    rules = build_rules()
    engine = RuleEngine()
    engine.rules = rules
    spec = {r.rule_id: effective_specificity(r) for r in rules}
    corpus = generate_corpus(N_CORPUS, seed=SEED)

    print("=" * 78)
    print("THE DEFAULT-RULE CONTROL — what the DSL's one-condition minimum "
          "costs rung 1")
    print("=" * 78)
    print(f"  {len(rules)} rules, no LLM, no learned rule · zero API calls")
    print("  POST-RUN: it adjudicates nothing and enters no scoreboard")
    print(f"  {describe()}")

    artifact = describe_artifact(rules, spec)
    print()
    print("  THE ARTIFACT")
    print(f"    {CATCHALL} is `{artifact['in_the_policy']}` and has no "
          f"conditions; {artifact['why']},")
    conds = ", ".join(f"{c['attr']} {c['op']} {c['value']}"
                      for c in artifact["in_the_dsl"])
    print(f"    so it is encoded `{conds}`, true over the whole domain.")
    print(f"    conditions counted by the engine {artifact['specificity_in_the_dsl']}"
          f"   ·   conditions that constrain {artifact['effective_specificity']}")
    print(f"    rules with a vacuous condition: "
          f"{len(artifact['rules_with_a_vacuous_condition'])} of {len(rules)} "
          f"({', '.join(artifact['rules_with_a_vacuous_condition'])})")

    # ---- GATE: the published row, through the objects that produced it ------
    m_pub_corpus = measure(corpus, engine.decide, PUBLISHED)
    gate = check_published(m_pub_corpus)
    print()
    print("=" * 78)
    print("GATE — the published row must come back to the digit (FINDINGS.md, "
          "route 1)")
    print("=" * 78)
    print(f"  {'field':<24}{'measured':>12}{'published':>12}")
    for k, v in gate.items():
        mark = "  ok" if v["passes"] else "  NO"
        fmt = ("{:>12.4f}" if isinstance(v["published"], float) else "{:>12}")
        print(f"  {k:<24}" + fmt.format(v["measured"])
              + fmt.format(v["published"]) + mark)
    if not all(v["passes"] for v in gate.values()):
        print()
        print("  STOP. The published figure does not reproduce, so this control")
        print("  is not measuring beside it. Find out what changed and date the")
        print("  erratum in the FINDINGS that owns it. Do not adjust to fit")
        print("  (hard rule 6).")
        return 1
    print("\n  GATE PASSES. 0.5875 does not move; the control sits beside it.")

    # ---- THE FOUR ROWS -----------------------------------------------------
    space = list(all_cases())
    rows = [
        row(m_pub_corpus, CORPUS, PUBLISHED),
        row(measure(corpus, lambda c: decide_by_effective_specificity(
            rules, spec, c), CONTROL), CORPUS, CONTROL),
        row(measure(space, engine.decide, PUBLISHED), SPACE, PUBLISHED),
        row(measure(space, lambda c: decide_by_effective_specificity(
            rules, spec, c), CONTROL), SPACE, CONTROL),
    ]

    print()
    print("=" * 78)
    print("THE PAIR, ON BOTH SURFACES · perfect policy loaded, no LLM")
    print("=" * 78)
    print(f"  {'surface':<28}{'arbitration':<44}{'coverage':>10}{'e2e':>9}"
          f"{'CONFLICT':>10}{'silent':>8}")
    for r in rows:
        print(f"  {r['surface']:<28}{r['arbitration']:<44}"
              f"{r['coverage']:>10.4f}{r['accuracy_end_to_end']:>9.4f}"
              f"{r['conflict']:>10}{r['silent_errors_abs']:>8}")

    # ---- WHAT MOVES, AND WHAT CANNOT ---------------------------------------
    moves = {CORPUS: compare(corpus, rules, engine, spec),
             SPACE: compare(space, rules, engine, spec)}

    print()
    print("=" * 78)
    print("WHAT THE CONTROL MOVES")
    print("=" * 78)
    for surface, mv in moves.items():
        pub = next(r for r in rows if r["surface"] == surface
                   and r["arbitration"] == PUBLISHED)
        ctl = next(r for r in rows if r["surface"] == surface
                   and r["arbitration"] == CONTROL)
        print(f"\n  {surface}")
        print(f"    published conflicts {pub['conflict']:>7}, of which the "
              f"catch-all is a finalist in "
              f"{mv['published_conflicts_with_the_catchall_as_finalist']}")
        print(f"    of those, resolved  {mv['of_those_resolved']:>7}   "
              f"correct {mv['resolved_correct']}   wrong "
              f"{mv['resolved_wrong']}   still in conflict "
              f"{mv['still_conflict']}")
        print(f"    e2e {pub['accuracy_end_to_end']:.4f} -> "
              f"{ctl['accuracy_end_to_end']:.4f}  "
              f"({ctl['accuracy_end_to_end'] - pub['accuracy_end_to_end']:+.4f})"
              f"   ·   conflicts {pub['conflict']} -> {ctl['conflict']}  "
              f"({(pub['conflict'] - ctl['conflict']) / pub['conflict']:.1%} "
              f"of them were the encoding)")
        print(f"    silent errors {pub['silent_errors_abs']} -> "
              f"{ctl['silent_errors_abs']}: the control cannot create one, and "
              f"creates none")
        print(f"    invariants · no ACTION changes: "
              f"{'ok' if mv['gate_no_action_changes'] else 'NO'}"
              f"   ·   no resolution is wrong: "
              f"{'ok' if mv['gate_no_resolution_is_wrong'] else 'NO'}")

    invariants_hold = all(mv["gate_no_action_changes"]
                          and mv["gate_no_resolution_is_wrong"]
                          for mv in moves.values())
    if not invariants_hold:
        print()
        print("  STOP. The control did something it cannot do: either it changed")
        print("  a decision that was already taken, or it resolved a conflict")
        print("  wrongly. The reading in the docstring is a proof, so what")
        print("  failed is the code, and the rows above are not to be published.")
        return 1

    # ---- PER CLASS, which is where the reading gets sharp -------------------
    mv = moves[CORPUS]
    print()
    print("=" * 78)
    print("BY TRUE CLASS, ON THE CORPUS — where the gain is, and where it is not")
    print("=" * 78)
    print(f"  {'class':<24}{'corpus':>8}{'CONFLICT pub':>14}{'CONFLICT ctl':>14}"
          f"{'correct pub':>13}{'correct ctl':>13}")
    per_class = mv["per_class"]
    for cls in sorted(per_class, key=lambda k: -sum(
            per_class[k].get(f"pub_{o}", 0)
            for o in ("ACTION", "CONFLICT", "IMPASSE"))):
        c = per_class[cls]
        total = sum(c.get(f"pub_{o}", 0)
                    for o in ("ACTION", "CONFLICT", "IMPASSE"))
        print(f"  {cls:<24}{total:>8}{c.get('pub_CONFLICT', 0):>14}"
              f"{c.get('ctl_CONFLICT', 0):>14}{c.get('pub_correct', 0):>13}"
              f"{c.get('ctl_correct', 0):>13}")
    print()
    print("  The gain is entirely in the two commonest classes. The two critical")
    print("  rare ones — SECURITY_INCIDENT, ONCALL_ESCALATION — move by zero.")

    # ---- THE RESIDUE, which is what the thesis is made of -------------------
    print()
    print("=" * 78)
    print("WHAT REMAINS IN CONFLICT — equal effective specificity, different "
          "action")
    print("=" * 78)
    for surface, mv in moves.items():
        print(f"\n  {surface}   ({mv['residual_conflict_sets']} distinct "
              f"finalist sets, {mv['residual_conflict_sets_with_the_catchall']} "
              f"of them involving {CATCHALL})")
        print(f"    {'cases':>8}  {'finalists':<26}{'spec':>5}  "
              f"{'first-match-wins would pick':<30}")
        for r in mv["top_residual_conflicts"]:
            ids = " vs ".join(r["finalists"])
            pick = r["first_match_wins"]
            act = r["actions"][r["finalists"].index(pick)]
            print(f"    {r['cases']:>8}  {ids:<26}{r['effective_specificity']:>5}"
                  f"  {pick} -> {act}")
    print()
    print("  None of it is an encoding artifact and none of it is reachable by")
    print("  any criterion monotone in the number of conditions: H01 (2) must")
    print("  beat H03 (1) and H16 (1) must beat H24 (2). FINDINGS.md, route 1.")

    payload = {
        "_env": environment(n_corpus=N_CORPUS, seed=SEED),
        "what": "rung 1's specificity ceiling with the catch-all at its true "
                "rank, beside the published encoding, on both surfaces",
        "provenance": "POST-RUN. The two corpus rows were run in memory on "
                      "2026-08-29 during the adjudication of EXTERNAL_REVIEW.md "
                      "and are printed in its §3; this module is item 2 of that "
                      "plan, written by someone who had already seen 0.6880. "
                      "Nothing here is a bet that could have failed, no signed "
                      "row moves, and it enters no scoreboard.",
        "criterion": "the same specificity arbitration, applied to the policy as "
                     "written instead of to the transcription the schema forced. "
                     "Vacuity is decided from DOMAINS and the rule alone: no "
                     "layer order and no oracle take part in the ranking.",
        "artifact": artifact,
        "gate_published_row": {"checks": gate, "passes": True},
        "rows": rows,
        "what_moves": moves,
        "n_rules": len(rules),
        "n_cases": {CORPUS: len(corpus), SPACE: len(space)},
        "seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
