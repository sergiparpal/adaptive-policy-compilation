"""
WHAT MAKES AN ANSWER READ THE LIST BY ITS CONDITIONS.
`corrections/above.py` found that the answers place the rules of
SECURITY_INCIDENT as one block, nearly always below their newborn. The few above
it read every rule by its conditions, or are their queue's general rule read as
a domain, and the same draft goes both ways. `FINDINGS_CORRECTIONS.md`, *Why
some answers put their newborn above every rule of their list*, *What it does
not settle*, item 1, and `IDEAS.md` leave what makes one answer read the list by
its conditions and another by its queues. They ask whether the list's order
moves it. Asked for by Sergi on 2026-11-15, after that reading. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**A round** is a born rule whose round listed a rule of SECURITY_INCIDENT,
newborn not of it, as `corrections/above.py` reads them. Its **side** is what its
answer did with those rules: a *climb* put its newborn above every one, a *cede*
below every one. For each round the reading takes what the round gave the
answer, and what the answer spent:
- **the order**: whether v1c's seeded shuffle opened the list with a security
  rule, and where the first one stands. The shuffle draws the slot, so a slot
  that moved the side would be the presentation's;
- **the precedent**: the listed rules the list shows ceding to a listed security
  rule, `[pierde con` it`]`, and climbing over one, `[gana a` it`]`, as each
  rule's own accepted declarations render;
- **the reasoning**: the placement call's reasoning tokens. They are set against
  the cedes' lower median at the same length of list, binned 1-3, 4-8, 9-20,
  21-50, and 51 or more;
- **the account**: the lines of the placement call's reasoning that name a
  listed security rule, each with the two lines after it, coded for priority and
  for conditions.

Also read, with no clause: the climb rate by the length of list and the
precedent, by a rule shown climbing over a security rule, and by cause; and each
climb's reasoning tokens beside its length's median.

--------------------------------------------------------------------------
THE DEVELOPMENT SET
--------------------------------------------------------------------------
**L r1 and N r3 are the development set**, as for `corrections/above.py`. C1 to
C4 pool the other four runs, L r2, L r3, N r1 and N r2. `above.json` found the
climbs as rare in each arm, and too few in either alone. C5 reads each arm
apart. What the drafter read of L r1 and N r3, before writing anything below:
- **every round**: its side, its list's length and block, what the list showed
  of the security rules, its opening and the slot of its first security rule,
  the number of placement calls, and its reasoning tokens;
- **the reasoning**: the eight climbs' whole, and the passages about the
  security rules of every round, counted for the codes below and for others
  dropped;
- **the first call's note** of every round.

**Its counts**, `DEVELOPMENT`, which gate 5 recomputes. Each pair gives L r1
first and N r3 second.
- **The rounds**: 170 and 217. Of these, 3 and 5 climb, and the rest cede.
- **The order.**
  - **The climbs.** 0 and 2 of their lists opened with a security rule, where
    the shuffle gives 0.63 and 2.17.
  - **The cedes.** 35 and 95 of theirs did, where it gives 40.85 and 87.94.
- **The reasoning.** 2 of the 3 and 5 of the 5 climbs spent fewer reasoning
  tokens than their run's cedes at the same length of list.
- **The account.**
  - **Conditions, and never priority.** The passages of 2 of the 3 and 3 of the
    5 climbs speak so, and those of 9 of the 167 and 9 of the 212 cedes.
  - **Priority.** 1 and 2 climbs' passages name it, and 155 and 199 cedes'.

**What the passages say**, read in the development set:
- **The cedes weigh the queue.** "The security rule is a specific exception
  (security incidents) that should take precedence. So our rule should lose to
  R0014". "Security incidents are critical and should override. So we should
  lose to R0022".
- **The climbs count conditions.** "R0022 solo requiere security_keyword true.
  Claramente R0022 es más general, y mi regla es más específica".
- **Three climbs' passages name priority**, for the task or for their own rule.
  "We need to declare priority: if our rule is a special case (i.e., more
  specific) of an existing rule, we put it in beats"; "debe prevalecer".

**Leads tried on the development set and dropped**:
- a rule shown climbing over a listed security rule: 1 of the 32 rounds with one
  climbed, and 7 of the 355 without;
- the precedent of rules shown ceding: within each length of list it told the
  sides apart by nothing;
- the slot of the first security rule, set against the shuffle;
- the first call's note reading conditions: 1 of the 8 climbs, 55 of the 379
  cedes;
- the reasoning's opening, whether it starts from the round's definition of
  `beats` or from the queues;
- a second placement call: every born rule had one.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The rounds and their sides against security are `above.json`'s.**
  2. **Every list is the seeded shuffle v1c showed.**
  3. **Every placement call carries its reasoning and its reasoning tokens.**
  4. **Every precedent is installed.** Every listed rule shown ceding to a listed
     security rule had that edge installed at its own birth.
  5. **The development set gives `DEVELOPMENT`'s counts.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
C1 to C4 pool L r2, L r3, N r1 and N r2. C5 reads L r2 and L r3, and N r1 and
N r2, apart.

  C1. **The order does not move it.** Of the climbs, the number whose list
      opened with a security rule is at least half what the shuffle gives.
  C2. **The climbs reason less.** At least two thirds of the climbs spent fewer
      reasoning tokens than the lower median of the cedes at the same length of
      list.
  C3. **The climbs count conditions.** Of the climbs, at least half have
      passages that speak of conditions and never of priority.
  C4. **The cedes weigh the queue.** Of the cedes, at most one in ten do.
  C5. **Both arms alike.** C2's statement, in L r2 and L r3, and in N r1 and
      N r2, each.

**Edge cases.**
- A share over nothing has no value, and a clause that reads one fails.
- A climb whose length of list has no cede is left out of C2.

**The drafter's account**, from L r1 and N r3.
- **The answers read the block of security rules one of two ways.**
  - **Nearly all weigh the queue.** Security incidents come first, so their
    newborn goes below every one (C4).
  - **The few that climb count conditions.** A rule of one condition is more
    general than theirs, and the round's `beats` is an exception, so they go
    above it (C3).
- **What the round showed does not set it.** v1c's shuffle opened the climbs'
  lists with a security rule as often as chance would (C1). A rule shown ceding
  to security, or climbing over it, did not tell the sides apart at a given
  length of list.
- **What the answer spent does.** The climbs reasoned less than the cedes of
  lists as long (C2), in either arm (C5). Counting conditions is the shorter
  reading. Weighing the queue takes the answer through what each queue is for,
  and the cheaper reading skips it.

**The bet is C2.** It says the reading by conditions is the cheap one: an answer
that reasons less applies the round's definition of `beats`. **C4 is trusted
most**, at 18 of 379. **C5 is trusted least**: each arm holds a handful of
climbs, and L r1 met the line exactly, at 2 of 3.

**What the drafter had seen**:
- **`FINDINGS_CORRECTIONS.md` whole, and `above.json` whole.** For every round of
  every run, that gives:
  - its side against the security rules, its list's length and block;
  - its draft's conditions, its cause, and its note's codes.
  The notes of the climbs of all six runs had been read for that reading.
- **`doors.json` and `byqueue.json` whole.** `byqueue.json` gives the reasoning
  tokens per listed rule of every listing of a gateway in L r1, L r2, L r3 and
  N r3, and their medians by side of the gateway.
- **L r1 and N r3**, as the development set above.

**What the drafter had not seen**: in L r2, L r3, N r1 and N r2, beyond those
records:
- any round's reasoning, or its passages about the security rules;
- any round's opening, slot, or precedent;
- any climb's reasoning tokens against the cedes'.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/above.py`.
L r1 and N r3 were read as the development set before the expectation above was
written, and the expectation was committed before the reading ran on the other
runs. Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration
event. Zero API calls.

Usage:  python3 -m corrections.conditions --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.conditions
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.provenance import describe, environment

from edges import rebuild as erb
from reasoned_loop import protocol as rp
from reuse import structure as st
from rung2.engine2 import EDGE_OK

from . import above as ab
from . import byqueue as bq
from . import doors as dr
from . import fall as fl
from . import forgotten as fg
from . import plan

F = Fraction
SEC = fl.SEC
UNLABELLED = fl.UNLABELLED
ABOVE, BELOW, MIXED = dr.ABOVE, dr.BELOW, dr.MIXED
CLIMB, CEDE, OTHER = "climb", "cede", "mixed"

DEVELOPMENT_RUNS = (plan.tag(plan.LABELLED, 1), plan.tag(UNLABELLED, 3))
HELD_L = tuple(plan.tag(plan.LABELLED, k) for k in range(2, plan.REPS + 1))
HELD_N = tuple(plan.tag(UNLABELLED, k) for k in range(1, plan.REPS))
HELD_OUT = HELD_L + HELD_N

# A list's length, in the bins the reasoning is set against.
BINS = ((1, 3), (4, 8), (9, 20), (21, 50), (51, None))

# The expectation's lines.
C1_SHARE = F(1, 2)
C2_SHARE = F(2, 3)
C3_SHARE = F(1, 2)
C4_SHARE = F(1, 10)
C5_SHARE = F(2, 3)

# Codes over the passages of the placement reasoning that name a listed rule of
# SECURITY_INCIDENT, frozen on the development set.
PRIORITY = re.compile(r"prioridad|priorit|preval|preced|cr[ií]tic|grave|importan|urgen"
                      r"|siempre|always|override|antes que|by default|por defecto", re.I)
CONDITIONS = re.compile(r"espec[ií]fic|specific|subconjunto|subset|\ba[ñn]ad|\badds?\b"
                        r"|\bm[aá]s condiciones|\bmore conditions|\bm[aá]s general|\bmore general"
                        r"|excepci|exception", re.I)
AFTER = 2       # the lines after each line that names a security rule

# The development set's counts, as the docstring gives them; gate 5 recomputes them.
DEVELOPMENT: dict[str, dict[str, Any]] = {
    DEVELOPMENT_RUNS[0]: {
        "rounds": 170, "sides": {CLIMB: 3, CEDE: 167, OTHER: 0},
        "climbs_open": [0, 0.6317], "cedes_open": [35, 40.8468],
        "climbs_below_median": [2, 3],
        "climbs_conditions_no_priority": [2, 3], "cedes_conditions_no_priority": [9, 167],
        "climbs_priority": [1, 3], "cedes_priority": [155, 167]},
    DEVELOPMENT_RUNS[1]: {
        "rounds": 217, "sides": {CLIMB: 5, CEDE: 212, OTHER: 0},
        "climbs_open": [2, 2.1719], "cedes_open": [95, 87.9352],
        "climbs_below_median": [5, 5],
        "climbs_conditions_no_priority": [3, 5], "cedes_conditions_no_priority": [9, 212],
        "climbs_priority": [2, 5], "cedes_priority": [199, 212]},
}

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/above.py. L r1 and N r3 "
    "are the development set, read before the expectation in the module's docstring was "
    "written; the expectation was committed before the reading ran on the other runs. Not a "
    "signed row; no verdict moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "conditions.json"


# ---------------------------------------------------------------------------
# One round
# ---------------------------------------------------------------------------

def length_bin(n: int) -> str:
    for lo, hi in BINS:
        if n >= lo and (hi is None or n <= hi):
            return f"{lo}-{hi}" if hi is not None else f"{lo}+"
    raise ValueError(n)


def passages(text: str, ids: Sequence[str]) -> str:
    """The lines of `text` that name one of `ids`, each with the `AFTER` lines
    after it."""
    lines = text.split("\n")
    pats = [re.compile(rf"\b{re.escape(x)}\b") for x in ids]
    out = []
    for i, line in enumerate(lines):
        if any(p.search(line) for p in pats):
            out.append("\n".join(lines[i:i + AFTER + 1]))
    return "\n".join(out)


def side_of(toward: str) -> str:
    return CLIMB if toward == ABOVE else CEDE if toward == BELOW else OTHER


def rounds(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Every round whose list holds a rule of SECURITY_INCIDENT, newborn not of
    it: its side against those rules, what its list showed, how much its
    placement call reasoned, and what its passages about them say."""
    born = erb.births(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    out = []
    for idx in sorted(born):
        r = born[idx]
        esc = escs.get(idx) or {}
        listed = list(esc.get("listed") or [])
        secs = [x for x in listed if rules[x]["action"] == SEC]
        if not secs or r["action"] == SEC:
            continue
        said = fl.declared(r)
        s = set(secs)
        call = bq.placement_call(esc) or {}
        text = call.get("reasoning") or ""
        p = passages(text, secs)
        prio, cond = bool(PRIORITY.search(p)), bool(CONDITIONS.search(p))
        first = min(listed.index(x) for x in secs)
        out.append({
            "born_at": idx, "newborn": r["rule_id"], "queue": r["action"], "cause": esc.get("kind"),
            "conditions": len(r["conditions"]),
            "side": side_of(dr.toward(said, secs)),
            "listed": len(listed), "security": len(secs), "bin": length_bin(len(listed)),
            "opens": first == 0, "first_slot": first,
            "opens_expected": F(len(secs), len(listed)),
            "ceding_shown": sum(1 for x in listed if x not in s
                                and s & set(rules[x].get("loses_to") or [])),
            "climbing_shown": sum(1 for x in listed if x not in s
                                  and s & set(rules[x].get("beats") or [])),
            "reasoning_tokens": bq.reasoning_tokens(call),
            "has_reasoning": bool(text),
            "passage": bool(p), "priority": prio, "conditions_code": cond,
            "conditions_no_priority": cond and not prio,
        })
    return out


# ---------------------------------------------------------------------------
# What the rounds give
# ---------------------------------------------------------------------------

def by_side(rows: list[dict[str, Any]], side: str) -> list[dict[str, Any]]:
    return [r for r in rows if r["side"] == side]


def opening(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """How many rounds' lists open with a security rule, against what v1c's
    shuffle gives."""
    exp = sum((F(r["opens_expected"]) for r in rows), F(0))
    return {"rounds": len(rows), "opens": sum(r["opens"] for r in rows), "expected": frac(exp)}


def medians(rows: list[dict[str, Any]]) -> dict[str, int]:
    """The lower median of the cedes' reasoning tokens, by list length."""
    out: dict[str, list[int]] = {}
    for r in by_side(rows, CEDE):
        if r["reasoning_tokens"] is not None:
            out.setdefault(r["bin"], []).append(r["reasoning_tokens"])
    return {b: sorted(v)[(len(v) - 1) // 2] for b, v in sorted(out.items())}


def below_median(rows: list[dict[str, Any]]) -> tuple[int, int]:
    """Of the climbs whose list length has cedes in the same rows, how many spent
    fewer reasoning tokens than those cedes' lower median."""
    med = medians(rows)
    climbs = [r for r in by_side(rows, CLIMB)
              if r["bin"] in med and r["reasoning_tokens"] is not None]
    return sum(r["reasoning_tokens"] < med[r["bin"]] for r in climbs), len(climbs)


def coded(rows: list[dict[str, Any]], side: str, key: str) -> tuple[int, int]:
    g = by_side(rows, side)
    return sum(bool(r[key]) for r in g), len(g)


def summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    sides = {s: by_side(rows, s) for s in (CLIMB, CEDE, OTHER)}
    pr = lambda t: {"part": t[0], "of": t[1], "share": frac(share(*t))}
    return {
        "rounds": len(rows),
        "sides": {s: len(v) for s, v in sides.items()},
        "opening": {s: opening(v) for s, v in sides.items() if v},
        "cede_medians": medians(rows),
        "climbs_below_median": pr(below_median(rows)),
        "codes": {s: {k: pr(coded(rows, s, k))
                      for k in ("passage", "priority", "conditions_code", "conditions_no_priority")}
                  for s in (CLIMB, CEDE)},
    }


def also(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Read with no clause: the climb rate by list length and the precedent shown,
    by whether a rule shown climbing over a security rule is listed, and by cause;
    and each climb's reasoning tokens against its length's median."""
    def rate(g):
        return {"climbs": sum(r["side"] == CLIMB for r in g), "of": len(g)}

    def by(key):
        out: dict[str, list] = {}
        for r in rows:
            out.setdefault(str(key(r)), []).append(r)
        return {k: rate(v) for k, v in sorted(out.items())}

    def precedent(r):
        c = F(r["ceding_shown"], r["listed"])
        return "none" if not r["ceding_shown"] else "under_a_third" if c < F(1, 3) else "a_third_or_more"

    med = medians(rows)
    return {
        "by_length_and_precedent": by(lambda r: f"{r['bin']}/{precedent(r)}"),
        "by_climbing_shown": by(lambda r: "some" if r["climbing_shown"] else "none"),
        "by_cause": by(lambda r: r["cause"]),
        "climbs": [{"born_at": r["born_at"], "newborn": r["newborn"], "queue": r["queue"],
                    "conditions": r["conditions"], "bin": r["bin"],
                    "reasoning_tokens": r["reasoning_tokens"], "cede_median": med.get(r["bin"]),
                    "priority": r["priority"], "conditions_code": r["conditions_code"]}
                   for r in by_side(rows, CLIMB)],
    }


def development(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The counts the docstring gives of a run of the development set."""
    o = opening(by_side(rows, CLIMB))
    oc = opening(by_side(rows, CEDE))
    return {
        "rounds": len(rows),
        "sides": {s: len(by_side(rows, s)) for s in (CLIMB, CEDE, OTHER)},
        "climbs_open": [o["opens"], round(o["expected"]["value"], 4)],
        "cedes_open": [oc["opens"], round(oc["expected"]["value"], 4)],
        "climbs_below_median": list(below_median(rows)),
        "climbs_conditions_no_priority": list(coded(rows, CLIMB, "conditions_no_priority")),
        "cedes_conditions_no_priority": list(coded(rows, CEDE, "conditions_no_priority")),
        "climbs_priority": list(coded(rows, CLIMB, "priority")),
        "cedes_priority": list(coded(rows, CEDE, "priority")),
    }


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], above_run: dict[str, Any],
             tag: str | None = None) -> dict[str, Any]:
    """One run's rounds against security, and the gates. `above_run` is the run's
    entry in `above.json`."""
    rows = rounds(record)
    rules = {r["rule_id"]: r for r in record["rules"]}
    escs = fg.escalation_at(record)
    by_birth = erb.edges_by_birth(record)
    born_at = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    want = sorted((r["born_at"], r["newborn"], r["security"], side_of(r["security_toward"]))
                  for r in above_run.get("rounds") or []
                  if r["queue"] != SEC and r["security"])
    got = sorted((r["born_at"], r["newborn"], r["security"], r["side"]) for r in rows)

    def shown(idx: int) -> bool:
        esc = escs[idx]
        listed = list(esc.get("listed") or [])
        first = (esc.get("calls") or [{}])[0].get("listed")
        return rp.listing(sorted(listed), idx, 0) == listed and first == listed

    def installed(winner: str, loser: str) -> bool:
        return any(e.winner == winner and e.loser == loser and e.verdict == EDGE_OK
                   for e in by_birth.get(born_at[loser], []))

    def ceding_installed(idx: int) -> bool:
        listed = list(escs[idx].get("listed") or [])
        s = {x for x in listed if rules[x]["action"] == SEC}
        return all(installed(w, x) for x in listed if x not in s
                   for w in s & set(rules[x].get("loses_to") or []))

    idxs = [r["born_at"] for r in rows]
    gates_out = [
        {"gate": 1, "what": "the rounds and their sides against security are above.json's",
         "passes": got == want},
        {"gate": 2, "what": "every list is the seeded shuffle v1c showed",
         "passes": all(shown(i) for i in idxs)},
        {"gate": 3, "what": "every placement call carries its reasoning and its reasoning tokens",
         "passes": all(r["has_reasoning"] and r["reasoning_tokens"] is not None for r in rows)},
        {"gate": 4, "what": "every listed rule shown ceding to a listed security rule had that "
                            "edge installed at its own birth",
         "passes": all(ceding_installed(i) for i in idxs)},
    ]
    run = {"summary": summary(rows), "also_read": also(rows),
           "rounds": [{**r, "opens_expected": str(r["opens_expected"])} for r in rows],
           "gates": gates_out}
    if tag in DEVELOPMENT_RUNS:
        run["development"] = development(rows)
        gates_out.append({"gate": 5, "what": "the development set gives DEVELOPMENT's counts",
                          "passes": run["development"] == DEVELOPMENT.get(tag)})
    return run


def read_all_runs(records: dict[str, dict], above_record: dict[str, Any]) -> dict[str, dict]:
    return {tag: read_run(rec, above_record["runs"][tag], tag=tag) for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def pooled(runs: dict[str, dict[str, Any]], tags: Sequence[str]) -> list[dict[str, Any]]:
    return [r for t in tags if t in runs for r in runs[t]["rounds"]]


def share_clause(cid: str, what: str, got: tuple[int, int], line: Fraction,
                 at_most: bool = False) -> dict[str, Any]:
    part, whole = got
    s = share(part, whole)
    holds = s is not None and (s <= line if at_most else s >= line)
    return {"clause": cid, "what": what,
            "reading": {"part": part, "of": whole, "share": frac(s)}, "holds": holds}


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    held = pooled(runs, HELD_OUT)
    climbs = by_side(held, CLIMB)
    o = opening(climbs)
    exp = sum((F(r["opens_expected"]) for r in climbs), F(0))
    arms = {"L": below_median(pooled(runs, HELD_L)), "N": below_median(pooled(runs, HELD_N))}
    return [
        {"clause": "C1", "what": "of the climbs, the number whose list opened with a security "
                                 "rule is at least half what the shuffle gives",
         "reading": {"opens": o["opens"], "of": o["rounds"], "expected": frac(exp) if climbs else None},
         "holds": bool(climbs) and exp > 0 and o["opens"] >= C1_SHARE * exp},
        share_clause("C2", "at least two thirds of the climbs spent fewer reasoning tokens than "
                           "the lower median of the cedes at the same length of list",
                     below_median(held), C2_SHARE),
        share_clause("C3", "of the climbs, at least half have passages that speak of conditions "
                           "and never of priority",
                     coded(held, CLIMB, "conditions_no_priority"), C3_SHARE),
        share_clause("C4", "of the cedes, at most one in ten have passages that speak of "
                           "conditions and never of priority",
                     coded(held, CEDE, "conditions_no_priority"), C4_SHARE, at_most=True),
        {"clause": "C5", "what": "C2's statement, in L r2 and L r3, and in N r1 and N r2, each",
         "reading": {k: {"part": p, "of": w, "share": frac(share(p, w))}
                     for k, (p, w) in arms.items()},
         "holds": all(w > 0 and F(p, w) >= C5_SHARE for p, w in arms.values())},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return records, json.loads(ab.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What makes an answer read the list by its "
                                             "conditions (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/conditions.py writes {record_path()}")
    records, above_record = read_all()
    runs = read_all_runs(records, above_record)
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"above": str(ab.record_path()),
                   "above_from": above_record["_env"].get("git_commit")},
        "surface": "every born rule of each run whose round listed a rule of SECURITY_INCIDENT, "
                   "newborn not of it, by its side against those rules; what its list showed, "
                   "its placement call's reasoning tokens, and its passages about them",
        "constants": {"BINS": [list(b) for b in BINS], "AFTER": AFTER,
                      "C1_SHARE": str(C1_SHARE), "C2_SHARE": str(C2_SHARE),
                      "C3_SHARE": str(C3_SHARE), "C4_SHARE": str(C4_SHARE),
                      "C5_SHARE": str(C5_SHARE),
                      "PRIORITY": PRIORITY.pattern, "CONDITIONS": CONDITIONS.pattern,
                      "DEVELOPMENT_RUNS": list(DEVELOPMENT_RUNS), "HELD_OUT": list(HELD_OUT),
                      "DEVELOPMENT": DEVELOPMENT},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]
        print(f"  {t}: {s['rounds']} rounds, sides {s['sides']}; climbs below the median "
              f"{s['climbs_below_median']['part']} of {s['climbs_below_median']['of']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
