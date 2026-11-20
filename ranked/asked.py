"""
WHY L'S TWINS ARE BORN AT THE CONFLICTS IT ASKS ABOUT. `FINDINGS_RANKED.md`,
*One thing the last two readings left free*, K, found that 35 of arm L's 53
twins, births that cover exactly an earlier rule's region under another queue,
were born at a conflict the loop asked about. Its *What it does not settle*,
second item, asks why: at those conflicts the first call drew exactly an
earlier rule's region under another queue. `IDEAS.md` carries it under *What
`PLAN_RANKED.md` opens*. Asked for by Sergi on 2026-11-20, with *Copies of the
same queue*, which `ranked/copies.py` reads. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**Arm L's three runs**, `results_ranked/loop_l_r{1,2,3}.json`: the rules in
birth order, every edge each birth tried, every arrival with its truth, and
each escalation's first call, its draft, its `copies` and its reasoning.
**`twins.json`**, whose pairs the gates hold this reading to.

**A conflict twin** is a birth of arm L that twins an earlier rule of another
queue, born at a conflict L asked about: when its ticket arrived, rules of two
queues or more stood undefeated there, and the loop escalated it. **Its twins**
are the earlier rules of another queue whose region it covers exactly: one, or
several in a few births. The unit of every clause below is the birth. The first
call is blind, as at every escalation: it is told the engine could not decide
the ticket, and it is shown no rule.
- **The rules standing** are those undefeated at the ticket when it arrived,
  before the birth, and their queues.
- **A twin stood** when one of the birth's twins is among them.
- **The newborn's queue** is another of the queues standing there, or a queue
  that did not stand. It cannot be a twin's queue.
- **A region's conditions** are the conditions its rule was written with.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **What the conflict held.** At every conflict twin: the rules and queues
      standing, whether a twin stood, which queue the newborn named against
      them, and whether it is the ticket's true queue, and a twin's.
  (b) **The region drawn.** The conditions of the conflict twins' regions,
      beside those of arm L's other twins and of its births that twin no rule
      of another queue.
  (c) **The reasoning.** For each conflict twin, the end of its first call's
      reasoning, kept for reading.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The pairs are `twins.json`'s.** The conflict twins found here, each
     newborn with each of its twins, are the pairs of that record whose newborn
     was born at a conflict, in each L run.
  2. **Each was a conflict.** At every conflict twin's ticket, the replay finds
     rules of two queues or more standing when it arrived, and the record's
     row says the engine returned a conflict there.
  3. **A born draft is its rule.** At every conflict twin's birth, the first
     call's draft has the newborn's queue and region.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  M1. **A twin stood there.** Of the conflict twins pooled, at more than half
      one of the birth's twins was among the rules standing at the ticket.
  M2. **The newborn named the other side.** Of them, at more than half the
      newborn's queue was another queue standing there.
  M3. **And not the truth, mostly.** Of them, at fewer than half the newborn's
      queue is the ticket's true queue.
  M4. **A coarse region.** The conflict twins were written with fewer
      conditions than L's other births: their median number of conditions is
      below the median of L's births that twin no rule of another queue.

A clause that reads a missing value fails.

**The drafter's account.**
- **M1.** A conflict is a ticket inside the regions of rules of two queues. A
  blind first call that draws a natural region for the ticket can land on the
  region one of them was drawn with, at a ticket like this one.
- **M2.** The call does not see the conflict, but it is asked about a ticket
  whose queue is in dispute. The drafter expects it to name a queue that stood
  there, the twin's rival, which is how its draft becomes the twin's region
  under another queue.
- **M3.** At the conflicts it asked about, L's first call named the true queue
  at 60 of 137, 36 of 119 and 73 of 163 (Stage C). The drafter expects the
  twins no better.
- **M4.** Two blind calls land on one region where the region is one the
  catalogue's line and the ticket's salient attributes draw at once: coarse
  ones, such as billing at severity 4.

**The bet is M2.** **M1 is trusted most.** **M4 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole and `twins.json` whole, among it every twin
  pair's region, birth, fate and verdict. That is 10, 6 and 19 conflict twins
  in L's three runs, with 10, 8 and 39 pairs, and two of L r1's in full:
  `R0144`, of `T2_TECHNICAL`, born at a conflict at a ticket of `H15` with
  `R0084`'s region, and `R0146`, of `T2_TECHNICAL`, at a ticket of `H14` with
  `R0116`'s;
- Stage C's counts of the conflicts L asked about, of its first calls that
  named the true queue, and of those the ranking would have decided right; the
  first call's texts, `corrections/protocol.py`.

**What the drafter had not seen**: which rules stood at any conflict twin's
ticket, which queue any newborn named against them, any first call's reasoning
at those births, or the conditions of L's births that twin no rule of another
queue.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/twins.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m ranked.asked --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.asked
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.provenance import describe, environment

from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Space

from . import plan
from . import reading as R
from . import readings as RD
from . import twins as TW

F = Fraction
L_RUNS = RD.L_RUNS
TAIL = 800                       # the characters of a reasoning's end kept for reading
ANOTHER = "another queue standing"
NOT_STANDING = "a queue not standing"
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/twins.py. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")

frac, plain = RD.frac, RD.plain


def median_of(xs: Sequence[int]) -> Fraction | None:
    if not xs:
        return None
    ys = sorted(xs)
    k = len(ys)
    return F(ys[k // 2]) if k % 2 else F(ys[k // 2 - 1] + ys[k // 2], 2)


# ---------------------------------------------------------------------------
# (a): what each conflict held
# ---------------------------------------------------------------------------

def conflict_twins(record: dict[str, Any], space: Space) -> dict[str, list[dict[str, Any]]]:
    """The run's births that twin a rule of another queue and were born at a
    conflict, each with its pairs, in birth order."""
    pairs, _, _ = TW.twins_of(record, space)
    kind = {e["idx"]: e["kind"] for e in record["escalations"]}
    out: dict[str, list[dict[str, Any]]] = {}
    for p in pairs:
        if kind.get(p["born_at"]) == plan.CONFLICT:
            out.setdefault(p["newborn"], []).append(p)
    return dict(sorted(out.items(), key=lambda kv: kv[1][0]["born_at"]))


def standing_at(record: dict[str, Any], idxs: set[int], space: Space,
                corpus: Sequence) -> dict[int, dict[str, list[str]]]:
    """At each case of `idxs`, the rules standing at its ticket when it arrived,
    by queue."""
    walk = R.Walk(record, space)
    out = {}
    for idx in sorted(set(walk.born) | idxs):
        if idx in idxs:
            here = R.point_of(corpus[idx], space)
            got: dict[str, list[str]] = {}
            for rid, m in walk.und.items():
                if m & here:
                    got.setdefault(walk.action[rid], []).append(rid)
            out[idx] = {q: sorted(v) for q, v in sorted(got.items())}
        if idx in walk.born:
            walk.birth(idx)
    return out


def named(queue: str, standing: dict[str, list[str]]) -> str:
    """Which queue the newborn named, against what stood."""
    return ANOTHER if queue in standing else NOT_STANDING


def read_births(record: dict[str, Any], births: dict[str, list[dict]],
                standing: dict[int, dict[str, list[str]]], space: Space
                ) -> tuple[list[dict[str, Any]], bool, bool]:
    """Each conflict twin, read; and gates 2 and 3."""
    rows = record["records"]
    rules = {d["rule_id"]: d for d in record["rules"]}
    escs = {e["idx"]: e for e in record["escalations"]}
    was_conflict = drafts_ok = True
    out = []
    for rid, pairs in births.items():
        n = rules[rid]
        idx = n["born_at"]
        here = standing[idx]
        row = rows[idx]
        was_conflict &= len(here) > 1 and row["outcome"] == plan.CONFLICT
        call = escs[idx]["calls"][0] or {}
        payload = call.get("payload")
        drafts_ok &= bool(isinstance(payload, dict) and payload.get("action") == n["action"]
                          and RD.region(payload, space) == TW.extension(space, n["conditions"]))
        twins = [{"rule": p["twin"], "queue": p["queues"][1],
                  "born_at": p["twin_born_at"],
                  "stood": p["twin"] in here.get(p["queues"][1], []),
                  "conditions": len(rules[p["twin"]]["conditions"])} for p in pairs]
        reasoning = call.get("reasoning") or ""
        out.append({"newborn": rid, "case": idx, "queue": n["action"],
                    "truth": row["truth"], "governing": row["truth_rule"],
                    "standing": here, "twins": twins,
                    "twin_stood": any(t["stood"] for t in twins),
                    "named": named(n["action"], here),
                    "newborn_right": n["action"] == row["truth"],
                    "twin_right": any(t["queue"] == row["truth"] for t in twins),
                    "conditions": len(n["conditions"]),
                    "region": RD.conditions_of(n["conditions"]),
                    "points": TW.extension(space, n["conditions"]).bit_count(),
                    "reasoning_chars": len(reasoning),
                    "tail": reasoning[-TAIL:]})
    return out, bool(was_conflict), bool(drafts_ok)


# ---------------------------------------------------------------------------
# (b): the regions drawn
# ---------------------------------------------------------------------------

def conditions_beside(record: dict[str, Any], space: Space) -> dict[str, list[int]]:
    """The number of conditions of the run's births: the conflict twins, the
    other twins, and the births that twin no rule of another queue."""
    pairs, _, _ = TW.twins_of(record, space)
    kind = {e["idx"]: e["kind"] for e in record["escalations"]}
    twins = {p["newborn"] for p in pairs}
    at_conflict = {p["newborn"] for p in pairs if kind.get(p["born_at"]) == plan.CONFLICT}
    born = {e["rule_id"] for e in record["escalations"] if e["verdict"] == "nacida"}
    rules = {d["rule_id"]: d for d in record["rules"]}
    out: dict[str, list[int]] = {"conflict_twins": [], "other_twins": [], "no_twin": []}
    for rid in sorted(born):
        k = len(rules[rid]["conditions"])
        out["conflict_twins" if rid in at_conflict else "other_twins" if rid in twins
            else "no_twin"].append(k)
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    complete = all(t in runs for t in L_RUNS)
    rows = [r for t in L_RUNS for r in (runs.get(t) or {}).get("births") or []]
    n = len(rows)
    stood = sum(r["twin_stood"] for r in rows)
    other = sum(r["named"] == ANOTHER for r in rows)
    right = sum(r["newborn_right"] for r in rows)
    pooled = readings.get("conditions") or {}
    mc, mo = pooled.get("conflict_twins_median"), pooled.get("no_twin_median")
    m1 = complete and bool(n) and 2 * stood > n
    m2 = complete and bool(n) and 2 * other > n
    m3 = complete and bool(n) and 2 * right < n
    m4 = complete and mc is not None and mo is not None and F(mc["fraction"]) < F(mo["fraction"])

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("M1", "of the conflict twins pooled, at more than half one of the birth's twins was "
                  "among the rules standing at the ticket", m1,
            {"births": n, "twin_stood": stood}),
        out("M2", "of them, at more than half the newborn's queue was another queue standing "
                  "there", m2, {"births": n, "another_queue_standing": other}),
        out("M3", "of them, at fewer than half the newborn's queue is the ticket's true queue",
            m3, {"births": n, "newborn_right": right}),
        out("M4", "the conflict twins' median number of conditions is below the median of L's "
                  "births that twin no rule of another queue", m4,
            {"conflict_twins": mc, "no_twin": mo}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "asked.json"


def twins_path():
    return plan.OUT / "twins.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {t: json.loads(plan.run_path(RD.arm_of(t), RD.rep_of(t)).read_text())
               for t in L_RUNS if plan.run_path(RD.arm_of(t), RD.rep_of(t)).exists()}
    return records, json.loads(twins_path().read_text())


def pairs_kept(twins: dict[str, Any], tag: str) -> list[tuple[str, str]]:
    """`twins.json`'s pairs of a run whose newborn was born at a conflict."""
    return sorted((p["newborn"], p["twin"]) for p in twins["readings"]["runs"][tag]["pairs_list"]
                  if p["newborn_birth"]["kind"] == plan.CONFLICT)


def read_everything(records: dict[str, dict], twins: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space = MI.space()
    corpus = list(MI.corpus())
    gates: list[dict[str, Any]] = []
    runs, conditions = {}, {"conflict_twins": [], "other_twins": [], "no_twin": []}
    for t in L_RUNS:
        if t not in records:
            continue
        rec = records[t]
        births = conflict_twins(rec, space)
        found = sorted((p["newborn"], p["twin"]) for ps in births.values() for p in ps)
        theirs = pairs_kept(twins, t)
        gates.append({"gate": 1, "run": t, "what": "the pairs are twins.json's",
                      "passes": bool(theirs) and found == theirs})
        standing = standing_at(rec, {ps[0]["born_at"] for ps in births.values()}, space, corpus)
        rows, was_conflict, drafts_ok = read_births(rec, births, standing, space)
        gates.append({"gate": 2, "run": t, "what": "each was a conflict", "passes": was_conflict})
        gates.append({"gate": 3, "run": t, "what": "a born draft is its rule",
                      "passes": drafts_ok})
        beside = conditions_beside(rec, space)
        for k, v in beside.items():
            conditions[k].extend(v)
        runs[t] = {"births": rows,
                   "conflict_twins": len(rows),
                   "pairs": len(found),
                   "twin_stood": sum(r["twin_stood"] for r in rows),
                   "named": dict(sorted(Counter(r["named"] for r in rows).items())),
                   "newborn_right": sum(r["newborn_right"] for r in rows),
                   "twin_right": sum(r["twin_right"] for r in rows),
                   "queues": dict(sorted(Counter(r["queue"] for r in rows).items())),
                   "standing_queues": dict(sorted(Counter(len(r["standing"])
                                                          for r in rows).items())),
                   "conditions": {k: dict(sorted(Counter(v).items())) for k, v in beside.items()}}
    summary: dict[str, Any] = {f"{k}_median": frac(median_of(v)) for k, v in conditions.items()}
    summary.update({f"{k}_births": len(v) for k, v in conditions.items()})
    return {"runs": runs, "conditions": summary}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why L's twins are born at the conflicts it asks "
                                             "about (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/asked.py writes {record_path()}")
    records, twins = read_inputs()
    readings, gates = read_everything(records, twins)
    for g in sorted(gates, key=lambda g: (L_RUNS.index(g["run"]), g["gate"])):
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(L_RUNS)
    if not complete:
        print("  missing records")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0 if complete and all(g["passes"] for g in gates) else 1
    if not complete or not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(readings)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"twins": str(twins_path()),
                   "twins_from": twins["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in L_RUNS}},
        "surface": "the births of arm L's three runs that twin a rule of another queue and were "
                   "born at a conflict the loop asked about, each read at its ticket as the "
                   "engine held it when the case arrived, and the conditions of arm L's births",
        "constants": {"tail": TAIL},
        "gates": gates,
        "readings": readings,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for cl_ in expectation:
        print(f"  {cl_['clause']}: {'holds' if cl_['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
