"""
THE CITATIONS ON BOTH SIDES: WHAT THE READINGS THAT KEPT ONE MOVE.
`corrections/declared.py` found that `corrections/fall.py`'s `declared` keeps
one citation a rule. In L r1 and L r2 one answer each cited a rule on both
sides: above it, installed, and below it, refused for the cycle the first side
had closed. `declared` keeps the second. Six readings read the answers'
declarations through it: `fall.py`, `gateway.py`, `doors.py`, `byqueue.py`,
`above.py` and `conditions.py`. Three more read their records: `paths.py` reads
`fall.json`; `carry.py` reads `fall.json`, `gateway.json` and `doors.json`; and
`oncall.py` reads `fall.json`, `paths.json`, `carry.json` and `gateway.json`.
This audit asks which of their figures move when the side `declared` drops is
the one kept. Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/declared.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE CITATIONS ON BOTH SIDES
--------------------------------------------------------------------------
Every answer of every run, L's and N's, is read a citation a rule and side, as
`corrections/declared.py`'s `citations` reads it. Every rule an answer cites on
both sides is listed, with each side's verdict and the side `declared` keeps.

--------------------------------------------------------------------------
THE TWO PASSES
--------------------------------------------------------------------------
The nine readings are run in this process, in the order their records feed one
another: `fall`, `paths`, `gateway`, `doors`, `byqueue`, `above`, `conditions`,
`carry` and `oncall`. Each writes its record to a temporary directory, never
over its own, and reads the records of the same pass where it reads another
reading's.
- **As committed**: the runs as they are. Each record must equal its committed
  record but for `_env` and `source`, which name the records a reading read
  and the commit each was written from.
- **The other side**: the same runs, read from copies in which every answer
  that cites a rule on both sides cites it only on the side `declared` drops.
  The kept side's citation leaves the rule's lists and its placement call's
  answer, so `declared` and every reading of the answer agree on the side.
  `above.py`'s gate 1 holds `declared` to the answer, and both keep the second
  side, so changing `declared` alone would make it refuse. Nothing else
  changes: the edge log keeps both edges, as the engine tried them.
Every leaf where the two passes' records differ is read, with its path and its
value in each. So is every clause of a record's expectation whose verdict
differs. A reading that refuses to write under the other side, or cannot run, is
read as refused, with what it said.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The citations are the records'.** In every run, every citation the
     engine ruled on is in the run's edge log with its verdict, and every edge
     of the log is one of them, as `corrections/declared.py`'s gate 3 reads it.
  2. **The copies change only the citations on both sides.** In every run, the
     copy differs from the record only in the lists of the rules that cite a
     rule on both sides and in their placement calls' answers. There
     `declared` gives the side it dropped, and everywhere else what it gave.
  3. **Every reading reproduces its record.** As committed, each of the nine
     records equals the committed one but for `_env` and `source`.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 and 2 and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
A reading **moves** when a leaf of its record differs between the two passes.

  Z1. **Two answers.** In the six runs, the rules an answer cites on both sides
      are two: `R0021`, cited by L r1's `R0159`, and `R0176`, cited by L r2's
      `R0198`.
  Z2. **Where an answer's sides are counted.** Under the other side,
      `gateway.json` and `above.json` move.
  Z3. **The conflicts.** `fall.json` does not move.
  Z4. **The gateways, the doors and the security rules.** `paths.json`,
      `doors.json`, `byqueue.json`, `conditions.json`, `carry.json` and
      `oncall.json` do not move.
  Z5. **No verdict.** No clause of the nine readings' expectations changes its
      verdict.
  Z6. **Nothing refuses.** Every reading writes under the other side.

A clause that reads a missing value fails, and a reading that refuses moves
nothing it can be read for.

**The drafter's account.**
- **The two were found in L's runs**, by `corrections/declared.py`'s gate 3,
  and N's were never read for it. The same round asked N's answers for their
  sides: Z1 is trusted least.
- **Both lie outside the keyword half**, between queues none of which is
  `SECURITY_INCIDENT`: `T1_GENERAL` against `SELF_SERVICE_DEFLECT`, and
  `SELF_SERVICE_DEFLECT` against `T2_TECHNICAL`. The readings of gateways,
  doors and security rules read rounds that list a keyword rule, and neither
  round can: Z4, and `paths.json` with `fall.json`.
- **`gateway.py` counts every answer's sides**, and `above.py` reads every
  placement of a listed rule by its side. Read on the other side, each of the
  two answers declares one win more and one loss fewer: Z2, the bet.
- **`fall.py` reads the declarations of the births at conflicts**, pair by pair
  beside the newborn: Z3 bets neither of the two is such a pair.
- **Every clause of the nine reads a rate over many rounds, or the keyword
  half**: one answer moves none: Z5, trusted most.
- **The copy changes the answer as it changes the rule**, so every gate that
  holds one to the other reads the copy as the record: Z6.

**The bet is Z2.** **Z5 is trusted most.** **Z1 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the section *The ranking the loop declared*
  among it, which found the two citations;
- **the two answers' rules.** `R0159`, of `T1_GENERAL` at severity 4,
  dashboard and the portal without the keyword, cites 23 rules above it. It
  cites 5 below it, `R0021` among them, all refused for closing a cycle.
  `R0021` is of `SELF_SERVICE_DEFLECT`. `R0198`, of
  `SELF_SERVICE_DEFLECT` at severity 4 off hours on the portal, cites 109 above,
  1 below and 87 dropped. `R0176` is of `T2_TECHNICAL`, without the keyword;
- **the keys `gateway.json` and `above.json` keep**, and not their values for
  these answers;
- **`above.py`'s gate 1 and its `payload_sides`**, which keep the second side,
  as `declared` does;
- **the reproduction.** Run as committed, all nine give their records but for
  `_env` and `source`. Without that, the seven that read another reading's
  record differ in the commit they name. One pass took about four and a half
  minutes: `oncall.py` two, `paths.py` one;
- **gates 1 and 2**, which pass on the dry run.

**What the drafter had not seen**: which answers of N's runs cite a rule on both
sides, and any reading's record under the other side.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: PAST THE PINS
--------------------------------------------------------------------------
On the first run, under the other side, `doors.py` and `above.py` refused at
their gate 5. It holds the counts of their development set, written in their
code before their expectation, to what the reading computes, and in L r1 those
counts moved. The four readings that read their records, `byqueue.py`,
`conditions.py`, `carry.py` and `oncall.py`, could not run. So the audit adds a
third pass:
- **past the pins**: the other side's copies, with each reading's
  `DEVELOPMENT` compared, recorded and let through, so the reading writes.
  Every other gate holds as it is. `doors.py`, `byqueue.py`, `above.py` and
  `conditions.py` keep such a pin.
Its leaves and clauses are read against the first pass, as the second's are,
with which pins it let through. A refusal now names the gates that failed. It
was tried in a scratch script first. It carries no expectation and moves no
clause: the clauses read the second pass, as written.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/declared.py`. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.citations --dry-run   # gates 1 and 2; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.citations
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import importlib
import io
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from harness.provenance import describe, environment

from reuse import structure as st

from . import byqueue as bq
from . import declared as DC
from . import fall as fl
from . import forgotten as fg
from . import plan

ORDER = ("fall", "paths", "gateway", "doors", "byqueue", "above", "conditions", "carry",
         "oncall")
DIRECT = ("fall", "gateway", "doors", "byqueue", "above", "conditions")
PASSES = ("as_committed", "other_side", "past_the_pins")
PINNED = ("doors", "byqueue", "above", "conditions")
KEPT_LEAVES = 400                   # the leaves kept a reading, in path order
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/declared.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")
ADDED = (
    "Added after the first run, after its six clauses were read: a third pass, past the pins, "
    "on the other side's copies with each reading's DEVELOPMENT compared, recorded and let "
    "through; and the gates a refusal names. Tried in a scratch script first. No expectation; "
    "no clause moves.")

# ---------------------------------------------------------------------------
# The citations on both sides
# ---------------------------------------------------------------------------

def records() -> dict[str, dict[str, Any]]:
    """Every run of both arms, by tag."""
    return {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
            for a in plan.ARMS for k in range(1, plan.REPS + 1)}


def both_sides(rule: dict[str, Any]) -> dict[str, list[tuple[str, str]]]:
    """The rules a born rule's answer cites on both sides, each with its sides and
    their verdicts, as `corrections/declared.py`'s `citations` reads them."""
    by_ref: dict[str, list[tuple[str, str]]] = {}
    for ref, side, why in DC.citations(rule):
        by_ref.setdefault(ref, []).append((side, why))
    return {ref: sorted(s) for ref, s in by_ref.items() if len({x for x, _ in s}) > 1}


def other_side(record: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """A copy of a run's record in which every answer that cites a rule on both
    sides cites it only on the side `declared` drops: the kept side's citation
    leaves the rule's lists and its placement call's answer. Also where."""
    rec = copy.deepcopy(record)
    escs = fg.escalation_at(rec)
    where = []
    for i, r in enumerate(rec["rules"]):
        for ref in both_sides(r):
            kept = fl.declared(r)[ref][0]
            dropped = [x for x in r.get("dropped_edges") or []
                       if x.split(":")[:2] == [kept, ref]]
            if dropped:
                r["dropped_edges"] = [x for x in r["dropped_edges"] if x not in dropped]
                at = "dropped_edges"
            else:
                r[kept] = [x for x in r.get(kept) or [] if x != ref]
                at = kept
            esc = escs.get(r["born_at"]) or {}
            call = bq.placement_call(esc)
            payload = (call or {}).get("payload")
            if isinstance(payload, dict):
                payload[kept] = [x for x in payload.get(kept) or [] if x != ref]
            where.append({"rule_index": i, "rule": r["rule_id"], "ref": ref, "kept": kept,
                          "list": at, "answer": isinstance(payload, dict),
                          "escalation_index": next((j for j, e in enumerate(rec["escalations"])
                                                    if e is esc), None),
                          "call_index": next((j for j, c in enumerate(esc.get("calls") or [])
                                              if c is call), None)})
    return rec, where


def listed(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Every rule an answer cites on both sides, in every run."""
    out = []
    for tag, record in runs.items():
        queue = {r["rule_id"]: r["action"] for r in record["rules"]}
        for r in sorted(record["rules"], key=lambda x: (x["born_at"], x["rule_id"])):
            for ref, sides in both_sides(r).items():
                out.append({"run": tag, "rule": r["rule_id"], "born_at": r["born_at"],
                            "queue": r["action"], "ref": ref, "ref_queue": queue.get(ref),
                            "sides": [{"side": s, "verdict": w} for s, w in sides],
                            "declared_keeps": fl.declared(r)[ref][0]})
    return out


def gate_one(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ok = {tag: DC.edge_log_matches(record, DC.declarations(record))
          for tag, record in runs.items()}
    return {"gate": 1, "what": "the citations are the records'", "passes": all(ok.values()),
            "by_run": ok}


def allowed(where: list[dict[str, Any]]) -> set[str]:
    """The paths a copy may differ at: the lists changed, and the answers'."""
    out = set()
    for w in where:
        out.add(f"rules[{w['rule_index']}].{w['list']}")
        if w["answer"]:
            out.add(f"escalations[{w['escalation_index']}].calls[{w['call_index']}]"
                    f".payload.{w['kept']}")
    return out


def gate_two(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ok = True
    for record in runs.values():
        copy_, where = other_side(record)
        ok &= {d["path"] for d in leaves(record, copy_)} <= allowed(where)
        for r, c in zip(record["rules"], copy_["rules"]):
            a, b = fl.declared(r), fl.declared(c)
            moved = {ref for ref in set(a) | set(b) if a.get(ref) != b.get(ref)}
            ok &= moved == set(both_sides(r))
            ok &= all(b[ref][0] != a[ref][0] for ref in moved)
    return {"gate": 2, "what": "the copies change only the citations on both sides",
            "passes": bool(ok)}


# ---------------------------------------------------------------------------
# The two passes
# ---------------------------------------------------------------------------

class Through(dict):
    """A pinned count let through: equal to whatever it is compared with, and a
    record of whether it differed. Added after the first run."""
    __hash__ = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.differed: list[bool] = []

    def __eq__(self, other):
        self.differed.append(not dict.__eq__(self, other))
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class ThroughByRun(dict):
    """`DEVELOPMENT` kept by run, each run's counts let through. Added after the
    first run."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lets: dict[str, Through] = {}

    def get(self, key, default=None):
        if key not in self.lets:
            self.lets[key] = Through(super().get(key, default) or {})
        return self.lets[key]


def let_through(pin: dict[str, Any]) -> dict[str, Any]:
    """A reading's `DEVELOPMENT`, let through: one run's counts, or counts by run."""
    if pin and all(isinstance(v, dict) for v in pin.values()):
        return ThroughByRun(pin)
    return Through(pin)


def differed(pin: dict[str, Any]) -> dict[str, Any]:
    """Whether a pin let through was compared, and whether it differed."""
    if isinstance(pin, ThroughByRun):
        return {tag: {"compared": len(t.differed), "differed": any(t.differed)}
                for tag, t in pin.lets.items()}
    if isinstance(pin, Through):
        return {"compared": len(pin.differed), "differed": any(pin.differed)}
    return {}


def run_pass(name: str, out_dir: Path, runs: dict[str, dict[str, Any]]
             ) -> dict[str, dict[str, Any]]:
    """The nine readings, in order, each writing to `out_dir`; on the copies of
    the runs where `name` says so. What each said, and its seconds."""
    mods = {m: importlib.import_module(f"corrections.{m}") for m in ORDER}
    paths = {m: mods[m].record_path for m in ORDER}
    run_path = plan.run_path
    pins = {m: mods[m].DEVELOPMENT for m in PINNED
            if m in mods and hasattr(mods[m], "DEVELOPMENT")}
    copies = {}
    if name in ("other_side", "past_the_pins"):
        for tag, record in runs.items():
            copy_, where = other_side(record)
            if where:
                copies[tag] = out_dir / f"loop_{tag}.json"
                copies[tag].write_text(json.dumps(copy_))
    committed = {m: str(paths[m]()) for m in ORDER}

    def load(p: Path) -> dict[str, Any]:
        """A record of the pass, the pass's paths written as the committed ones,
        where a reading names the record it read."""
        text = p.read_text()
        for m in ORDER:
            text = text.replace(str(out_dir / f"{m}.json"), committed[m])
        return json.loads(text)

    out: dict[str, dict[str, Any]] = {}
    try:
        for m in ORDER:
            mods[m].record_path = (lambda p=out_dir / f"{m}.json": p)
        plan.run_path = (lambda arm, rep: copies.get(plan.tag(arm, rep)) or run_path(arm, rep))
        if name == "past_the_pins":
            for m, pin in pins.items():
                mods[m].DEVELOPMENT = let_through(pin)
        for m in ORDER:
            t = time.time()
            said = io.StringIO()
            refused = None
            try:
                with contextlib.redirect_stdout(said):
                    mods[m].main([])
            except SystemExit as e:
                failed = [x.strip() for x in said.getvalue().splitlines() if ": FAIL" in x]
                refused = "; ".join([str(e).strip() or f"exit {e.code}"] + failed)
            except Exception as e:            # a reading that cannot run is read as refused
                refused = f"{type(e).__name__}: {e}"
            p = out_dir / f"{m}.json"
            out[m] = {"record": load(p) if refused is None and p.exists() else None,
                      "refused": refused, "seconds": round(time.time() - t, 1),
                      "pin": differed(mods[m].DEVELOPMENT) if m in pins else None}
    finally:
        plan.run_path = run_path
        for m, pin in pins.items():
            mods[m].DEVELOPMENT = pin
        for m in ORDER:
            mods[m].record_path = paths[m]
    return out


def leaves(a: Any, b: Any, path: str = "") -> list[dict[str, Any]]:
    """Every leaf where `a` and `b` differ, by path."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b), key=str):
            p = f"{path}.{k}" if path else str(k)
            if k not in a or k not in b:
                out.append({"path": p, "as_committed": a.get(k), "other_side": b.get(k)})
            else:
                out += leaves(a[k], b[k], p)
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += leaves(x, y, f"{path}[{i}]")
        return out
    return [] if a == b else [{"path": path, "as_committed": a, "other_side": b}]


def without_env(record: dict[str, Any] | None) -> dict[str, Any] | None:
    """A record but for `_env` and `source`: what it read and when, not what it
    found."""
    return None if record is None else {k: v for k, v in record.items()
                                        if k not in ("_env", "source")}


def verdicts(record: dict[str, Any] | None) -> dict[str, bool]:
    return {c["clause"]: c["holds"] for c in (record or {}).get("expectation") or []
            if "clause" in c and "holds" in c}


def compare(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    """One reading's two passes: whether it refused, the leaves that differ, and
    the clauses whose verdict differs."""
    if second["refused"] is not None:
        return {"refused": second["refused"], "moved": None, "leaves": [], "clauses": []}
    diff = leaves(without_env(first["record"]), without_env(second["record"]))
    a, b = verdicts(first["record"]), verdicts(second["record"])
    return {"refused": None, "moved": len(diff), "leaves": diff[:KEPT_LEAVES],
            "clauses": [{"clause": c, "as_committed": a.get(c), "other_side": b.get(c)}
                        for c in sorted(set(a) | set(b)) if a.get(c) != b.get(c)]}


def reproduces(first: dict[str, Any], committed: Path) -> bool:
    return (first["refused"] is None
            and without_env(first["record"]) == without_env(json.loads(committed.read_text())))


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

TWO = {("l_r1", "R0159", "R0021"), ("l_r2", "R0198", "R0176")}
SIDES_COUNTED = ("gateway", "above")
STILL = ("paths", "doors", "byqueue", "conditions", "carry", "oncall")


def read_expectation(found: list[dict[str, Any]], readings: dict[str, dict[str, Any]]
                     ) -> list[dict[str, Any]]:
    def moved(m: str) -> int | None:
        r = readings.get(m)
        return None if r is None or r["refused"] is not None else r["moved"]

    pairs = {(f["run"], f["rule"], f["ref"]) for f in found}
    z1 = pairs == TWO
    z2 = all((moved(m) or 0) > 0 for m in SIDES_COUNTED)
    z3 = moved("fall") == 0
    z4 = all(moved(m) == 0 for m in STILL)
    z5 = (len(readings) == len(ORDER)
          and all(r["refused"] is None and not r["clauses"] for r in readings.values()))
    z6 = len(readings) == len(ORDER) and all(r["refused"] is None for r in readings.values())
    return [
        {"clause": "Z1", "what": "the rules an answer cites on both sides are R0021, cited by L "
                                 "r1's R0159, and R0176, cited by L r2's R0198",
         "reading": sorted(list(x) for x in pairs), "holds": z1},
        {"clause": "Z2", "what": "under the other side, gateway.json and above.json move",
         "reading": {m: moved(m) for m in SIDES_COUNTED}, "holds": z2},
        {"clause": "Z3", "what": "fall.json does not move",
         "reading": {"fall": moved("fall")}, "holds": z3},
        {"clause": "Z4", "what": "paths, doors, byqueue, conditions, carry and oncall do not move",
         "reading": {m: moved(m) for m in STILL}, "holds": z4},
        {"clause": "Z5", "what": "no clause of the nine readings changes its verdict",
         "reading": {m: [c["clause"] for c in r["clauses"]] for m, r in readings.items()},
         "holds": z5},
        {"clause": "Z6", "what": "every reading writes under the other side",
         "reading": {m: r["refused"] for m, r in readings.items()}, "holds": z6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "citations.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="The citations on both sides: what the readings "
                                             "that kept one move (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 and 2 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/citations.py writes {record_path()}")
    runs = records()
    first_gates = [gate_one(runs), gate_two(runs)]
    if args.dry_run:
        for g in first_gates:
            print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in first_gates) else 1
    found = listed(runs)
    committed = {m: importlib.import_module(f"corrections.{m}").record_path() for m in ORDER}
    with tempfile.TemporaryDirectory() as tmp:
        passes = {}
        for name in PASSES:
            d = Path(tmp) / name
            d.mkdir()
            passes[name] = run_pass(name, d, runs)
    same = {m: reproduces(passes["as_committed"][m], committed[m]) for m in ORDER}
    gates = first_gates + [{"gate": 3, "what": "every reading reproduces its record",
                            "passes": all(same.values()), "by_reading": same}]
    for g in gates:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    readings = {m: {"seconds": {p: passes[p][m]["seconds"] for p in PASSES[:2]},
                    **compare(passes["as_committed"][m], passes["other_side"][m])}
                for m in ORDER}
    past = {m: {"seconds": passes["past_the_pins"][m]["seconds"],
                "pin": passes["past_the_pins"][m]["pin"],
                **compare(passes["as_committed"][m], passes["past_the_pins"][m])}
            for m in ORDER}
    expectation = read_expectation(found, readings)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "added_after_the_first_run": ADDED,
        "source": {"runs": {plan.tag(a, k): str(plan.run_path(a, k))
                            for a in plan.ARMS for k in range(1, plan.REPS + 1)},
                   "readings": {m: str(committed[m]) for m in ORDER}},
        "surface": "the nine readings that read the answers' declarations through "
                   "corrections/fall.py's declared, or read the records of those that do, each "
                   "run twice: as committed, and keeping the side declared drops for a rule an "
                   "answer cites on both sides; and, added after the first run, a third time on "
                   "the second's copies, past the pins of the development counts",
        "constants": {"order": list(ORDER), "direct": list(DIRECT), "kept_leaves": KEPT_LEAVES,
                      "pinned": list(PINNED)},
        "gates": gates,
        "both_sides": found,
        "readings": readings,
        "past_the_pins": past,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for label, rd in (("other side", readings), ("past the pins", past)):
        for m, r in rd.items():
            state = "refused" if r["refused"] is not None else f"{r['moved']} leaves move"
            print(f"  {label}, {m}: {state}; clauses that flip: "
                  f"{[c['clause'] for c in r['clauses']]}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
