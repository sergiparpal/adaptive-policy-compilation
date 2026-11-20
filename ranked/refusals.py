"""
WHY THE REFUSALS FELL WHERE THEY DID. `FINDINGS_RANKED.md`, *Two things the six
readings left free*, G, found that every conflict K's ranking took, in every
run, was a pair whose declared edge the engine had refused for closing a cycle.
Its *What it does not settle*, first item, asks which earlier declarations
closed each refused edge's cycle, and whether the paths ran through rules no
contested point sees, as `results_corrections/FINDINGS_CORRECTIONS.md` found
for the closed L runs. `IDEAS.md` carries it under *What `PLAN_RANKED.md`
opens*. Asked for by Sergi on 2026-11-20, with *Why K r2's base decided `H11`'s
tickets wrong with one queue standing*, which `ranked/billing.py` reads.
POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The three K runs**, `results_ranked/loop_k_r{1,2,3}.json`: the rules in birth
order and every edge each birth tried, with the engine's verdict.
**`conflicts.json`**, whose rows give, at every case K's ranking took, the
edges tried and refused between a rule of the winner's queue and one of the
runner-up's. **`readings.json`**, whose A gives each such case's true queue.

**A refusal** is one such edge at one such case: a case and an edge `W` beats
`L` that the engine refused. The same edge at two cases is two refusals, so a
refusal weighs as the cases its pair decided.

**Each edge is read at the moment it was tried**, in the engine replayed birth
by birth, every edge in the log's order: after the edges its birth tried before
it, and before it. Its birth's rule, **the newborn**, is at one end of it.
- **Its side.** A `win` when the newborn is `W`, the newborn's answer
  declaring itself above `L`; a `loss` when the newborn is `L`.
- **Its paths** are the chains of what beats what, by containment and by
  declared edges, from `L` to `W`. The engine refused the edge because one
  exists: `W` beats `L` would close it into a cycle.
- **What closes it at the newborn.** Every path starts or ends at the newborn,
  and its step there is either a containment, a rule nested in the newborn or
  one the newborn is nested in, or a declared edge its own answer installed
  earlier at the same birth. It is `own answer` when no path is left with the
  newborn's own declarations taken out, `containment` when no path is left with
  the containments at the newborn taken out, and `either` when paths of both
  kinds remain.
- **Where the cycle is.** `somewhere` when some path runs through rules that
  all match a point both `W` and `L` match; `nowhere` when every path runs
  through a rule that misses every such point (`corrections/paths.py`'s
  `local_reach`).
- **A door** is a step of the paths that every path passes through: taken out
  alone, it leaves no path. Its kind, and for a declared door the birth that
  installed it.
- **The policy's verdict** on `W` above `L`, over the points both match:
  `right`, `wrong` or `even` (`corrections/paths.py`'s `verdict`).

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **What closed each refusal.** In each K run, the refusals by side, by
      what closes their cycle at the newborn, by where the cycle is, and by
      whether a door carries every path; each by group, as `conflicts.json`
      groups the cases.
  (b) **The doors.** The steps that carry the most refusals, with their kind,
      the birth that installed a declared one, and the rules at both ends.
  (c) **The refused declaration and the ranking.** At each refusal, whether the
      queue the refused edge declared above is the case's truth, beside whether
      the ranking was right, apart for the refusals whose cycle is nowhere.
  Beside them: each distinct refused edge, read once, with its newborn, its
  shortest path and the rules its paths run through.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the log.** In each K run, every edge the replay tries gets
     the verdict the record's log gives it.
  2. **Every refusal is met where it was tried.** Every refused edge of
     `conflicts.json`'s rows is met in the replay at a birth whose rule is at
     one end of it, `L` reaches `W` right before it, and the engine refuses it
     there for closing a cycle.
  3. **The replayed base is the run's.** At the end, the replay's extensions
     and declared edges are those of `ranked/reading.py`'s walk of the record.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  I1. **Nowhere.** In every K run, the cycle is nowhere at more than half of
      the refusals.
  I2. **There before the answer.** In every K run, at more than half of the
      refusals the cycle closes without the newborn's own declarations:
      `containment` or `either`.
  I3. **Through a door.** In every K run, at more than half of the refusals a
      door carries every path.

A clause that reads a missing value fails.

**The drafter's account.**
- **I2.** The loop installs a newborn's wins before its losses
  (`authorship/loop.py`'s `install_declarations`). A win refused while no loss
  of the newborn is installed can only close through a rule nested in the
  newborn: a narrower rule of its region that an earlier declaration had put
  below `L`. K r1's `R0089` declared wins alone, above all 25 rules its round
  listed, and 15 were refused; most of K r1's refusals are its. A refused loss
  can close through the newborn's own wins, as `PLAN_CORRECTIONS.md`'s readings
  found in L. The drafter expects wins to carry most refusals in every run.
- **I1, the bet.** `corrections/paths.py` found almost every cycle of L's
  refused right sides nowhere, through a rule nested in a broad one. A rule
  nested in the newborn and beaten by `L` needs to overlap `L`, but its path to
  `L` may run through rules that miss the points `W` and `L` share. The drafter
  expects the same as the closed runs.
- **I3.** `corrections/doors.py` found the paths of L's refusals running
  through few doors. A refused win whose paths all enter the newborn through
  one nested rule has that step for a door.

**The bet is I1.** **I2 is trusted most**, by the order of installation. **I3 is
trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole and `conflicts.json` whole: the refused pairs at
  every case of the ranking, with the rule each declared above, their verdicts,
  every one for closing a cycle, and the rules standing; `drafts.json`;
- in the run records: `R0089`'s birth in K r1, its 25 rules listed, its 10 wins
  installed and 15 refused; `R0124`'s and `R0126`'s in K r3, the first
  installing 36 wins, the second's listing and its edges installed and refused;
- `corrections/paths.py` and `FINDINGS_CORRECTIONS.md`'s readings of the paths
  and the doors in L; `authorship/loop.py`'s order of installation;
  `rung2/engine2.py`'s containment and `try_edge`; the attributes' domains.

**What the drafter had not seen**: any path from a refused edge's `L` to its
`W`, any door, where any cycle is, or the policy's verdict on any refused edge
beyond the cases' true queues.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/conflicts.py` and
`ranked/drafts.py`. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.refusals --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.refusals
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from corrections import paths as CP
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import plan
from . import readings as RD

K_RUNS = RD.K_RUNS
GROUPS = ("deflection", "billing", "rest")
WIN, LOSS = "win", "loss"
OWN, CONTAINMENT, EITHER = "own answer", "containment", "either"
CLOSES = (OWN, CONTAINMENT, EITHER)
SOMEWHERE, NOWHERE = CP.SOMEWHERE, CP.NOWHERE
WHERE = (SOMEWHERE, NOWHERE)
VERDICTS = (CP.RIGHT_VERDICT, CP.WRONG, CP.EVEN)
NESTED, DECLARED = CP.NESTED, CP.DECLARED
TOP_DOORS = 12
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/conflicts.py and "
    "ranked/drafts.py. The expectation in the module's docstring was written and committed "
    "before the reading ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


# ---------------------------------------------------------------------------
# The refusals, from conflicts.json
# ---------------------------------------------------------------------------

def refusals_of(rows: Sequence[dict]) -> list[dict[str, Any]]:
    """Every refused edge at every case of the ranking: one refusal each."""
    return [{"case": r["case"], "group": r["group"], "right": r["right"],
             "above": e["above"], "below": e["below"]}
            for r in rows for e in r["refused"]]


# ---------------------------------------------------------------------------
# One refused edge, read at the moment it was tried
# ---------------------------------------------------------------------------

def step_kind(engine: PriorityEngine, x: str, y: str) -> str:
    """A step `x` beats `y`: `x` nested in `y`, or a declared edge."""
    return NESTED if y in engine.sub_above[x] else DECLARED


def closes(engine: PriorityEngine, winner: str, loser: str, newborn: str,
           own: set[tuple[str, str]], nodes: set[str]) -> str | None:
    """What closes the cycle at the newborn: its own declarations, the
    containments at it, or either."""
    if newborn == winner:
        at = {(x, newborn) for x in nodes if newborn in engine.sub_above[x]}
    elif newborn == loser:
        at = {(newborn, y) for y in engine.sub_above[newborn] if y in nodes}
    else:
        return None
    if winner not in CP.forward(engine, loser, own):
        return OWN
    if winner not in CP.forward(engine, loser, at):
        return CONTAINMENT
    return EITHER


def doors_of(engine: PriorityEngine, winner: str, loser: str, nodes: set[str],
             installed_at: dict[tuple[str, str], int], idx: int,
             action: dict[str, str]) -> list[dict[str, Any]]:
    """The steps every path from `loser` to `winner` passes through."""
    out = []
    for x in sorted(nodes):
        for y in sorted(engine.wins_over(x)):
            if y not in nodes or winner in CP.forward(engine, loser, {(x, y)}):
                continue
            kind = step_kind(engine, x, y)
            at = installed_at.get((x, y)) if kind == DECLARED else None
            out.append({"upper": x, "lower": y, "kind": kind, "installed_at": at,
                        "at_this_birth": at == idx, "upper_queue": action[x],
                        "lower_queue": action[y]})
    return out


def analyse(engine: PriorityEngine, winner: str, loser: str, newborn: str, idx: int,
            own: set[tuple[str, str]], installed_at: dict[tuple[str, str], int],
            action: dict[str, str], truth: dict[str, int]) -> dict[str, Any]:
    """A refused edge, read before it is tried."""
    nodes = CP.forward(engine, loser) & CP.backward(engine, winner)
    reaches = winner in nodes
    shared = engine.ext[winner] & engine.ext[loser]
    side = WIN if newborn == winner else LOSS if newborn == loser else None
    out = {"above": winner, "below": loser, "born_at": idx, "newborn": newborn, "side": side,
           "queues": [action[winner], action[loser]], "reaches": reaches,
           "verdict": CP.verdict(engine, winner, loser, action, truth),
           "shared_points": shared.bit_count()}
    if not reaches:
        return dict(out, closes=None, where=None, shortest=None, path_rules=[], doors=[])
    return dict(out,
                closes=closes(engine, winner, loser, newborn, own, nodes),
                where=SOMEWHERE if CP.local_reach(engine, loser, winner, nodes, shared)
                else NOWHERE,
                shortest=CP.shortest(engine, loser, winner, nodes),
                path_rules=sorted(nodes - {winner, loser}),
                doors=doors_of(engine, winner, loser, nodes, installed_at, idx, action))


def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           targets: set[tuple[str, str]]) -> dict[str, Any]:
    """The record's births and edges, in order; every target edge read before
    it is tried. Gates 1 and 2 are kept as it goes."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    action: dict[str, str] = {}
    installed_at: dict[tuple[str, str], int] = {}
    found: dict[tuple[str, str], dict[str, Any]] = {}
    log_ok = True
    met_ok = True
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        action[rid] = d["action"]
        own: set[tuple[str, str]] = set()
        for e in by_birth.get(idx, []):
            key = (e.winner, e.loser)
            first = key in targets and key not in found
            if first:
                found[key] = analyse(engine, e.winner, e.loser, rid, idx, own, installed_at,
                                     action, truth)
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            log_ok &= why == e.verdict
            if first:
                met_ok &= bool(why == EDGE_CYCLE and found[key]["reaches"]
                               and found[key]["side"] is not None)
            if why == EDGE_OK and not before and e.loser in engine.decl_above[e.winner]:
                installed_at[key] = idx
                own.add(key)
    met_ok &= set(found) == set(targets)
    return {"found": found, "log_ok": bool(log_ok), "met_ok": bool(met_ok), "engine": engine,
            "action": action}


def same_base(engine: PriorityEngine, record: dict[str, Any], space: Space) -> bool:
    """Gate 3: the replay's extensions and declared edges are the walk's."""
    w = RD.walked(record, space).engine
    return bool(engine.ext == w.ext and engine.decl_above == w.decl_above
                and engine.decl_below == w.decl_below)


# ---------------------------------------------------------------------------
# (a), (b), (c): the refusals of one run
# ---------------------------------------------------------------------------

def tally(units: Sequence[dict], key, keys: Sequence[str]) -> dict[str, int]:
    c = Counter(key(u) for u in units)
    return {k: c.get(k, 0) for k in keys}


def read_run(units: Sequence[dict], found: dict[tuple[str, str], dict],
             truth_of: dict[int, str], action: dict[str, str]) -> dict[str, Any]:
    rows = []
    for u in units:
        a = found[(u["above"], u["below"])]
        rows.append(dict(u, side=a["side"], closes=a["closes"], where=a["where"],
                         door=bool(a["doors"]), verdict=a["verdict"],
                         declared_names_the_truth=action[u["above"]] == truth_of[u["case"]]))

    def summary(rs):
        return {"refusals": len(rs), "cases": len({r["case"] for r in rs}),
                "side": tally(rs, lambda r: r["side"], (WIN, LOSS)),
                "closes": tally(rs, lambda r: r["closes"], CLOSES),
                "where": tally(rs, lambda r: r["where"], WHERE),
                "door": sum(r["door"] for r in rs),
                "verdict": tally(rs, lambda r: r["verdict"], VERDICTS),
                "ranking_right": sum(r["right"] for r in rs),
                "declared_names_the_truth": sum(r["declared_names_the_truth"] for r in rs)}

    nowhere = [r for r in rows if r["where"] == NOWHERE]
    doors = Counter()
    door_rows: dict[tuple[str, str], dict] = {}
    for r in rows:
        for dr in found[(r["above"], r["below"])]["doors"]:
            k = (dr["upper"], dr["lower"])
            doors[k] += 1
            door_rows[k] = dr
    top = sorted(doors.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP_DOORS]
    edges = sorted({(r["above"], r["below"]) for r in rows})
    return {
        "all": summary(rows),
        "by_group": {g: summary([r for r in rows if r["group"] == g]) for g in GROUPS},
        "nowhere": {"refusals": len(nowhere),
                    "ranking_right": sum(r["right"] for r in nowhere),
                    "declared_names_the_truth": sum(r["declared_names_the_truth"]
                                                    for r in nowhere),
                    "both": sum(r["right"] and r["declared_names_the_truth"] for r in nowhere),
                    "neither": sum(not r["right"] and not r["declared_names_the_truth"]
                                   for r in nowhere)},
        "doors": [dict(door_rows[k], refusals=n) for k, n in top],
        "edges": [dict(found[k], refusals=sum(1 for r in rows
                                              if (r["above"], r["below"]) == k))
                  for k in edges],
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}

    def every(test) -> bool:
        return all(t in runs for t in K_RUNS) and all(
            (runs[t].get("all") or {}).get("refusals") and test(runs[t]["all"]) for t in K_RUNS)

    i1 = every(lambda a: 2 * a["where"][NOWHERE] > a["refusals"])
    i2 = every(lambda a: 2 * (a["closes"][CONTAINMENT] + a["closes"][EITHER]) > a["refusals"])
    i3 = every(lambda a: 2 * a["door"] > a["refusals"])

    def reading(keys):
        return {t: {k: (runs[t].get("all") or {}).get(k) for k in ("refusals", *keys)}
                for t in K_RUNS if t in runs}

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("I1", "in every K run, the cycle is nowhere at more than half of the refusals",
            i1, reading(("where",))),
        out("I2", "in every K run, at more than half of the refusals the cycle closes "
                  "without the newborn's own declarations", i2, reading(("closes",))),
        out("I3", "in every K run, at more than half of the refusals a door carries every "
                  "path", i3, reading(("door",))),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "refusals.json"


def conflicts_path():
    return plan.OUT / "conflicts.json"


def readings_path():
    return plan.OUT / "readings.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any]]:
    records = {t: json.loads(plan.run_path(RD.arm_of(t), RD.rep_of(t)).read_text())
               for t in K_RUNS if plan.run_path(RD.arm_of(t), RD.rep_of(t)).exists()}
    return (records, json.loads(conflicts_path().read_text()),
            json.loads(readings_path().read_text()))


def read_everything(records: dict[str, dict], conflicts: dict[str, Any],
                    kept: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    unordered = conflicts["readings"]["added"]["unordered"]
    a_cases = kept["readings"]["A"]["cases"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in K_RUNS:
        if t not in records:
            continue
        units = refusals_of(unordered[t]["rows"])
        targets = {(u["above"], u["below"]) for u in units}
        got = replay(records[t], space, truth, targets)
        gates.append({"gate": 1, "run": t, "what": "the replay is the log",
                      "passes": got["log_ok"]})
        gates.append({"gate": 2, "run": t, "what": "every refusal is met where it was tried",
                      "passes": got["met_ok"]})
        gates.append({"gate": 3, "run": t, "what": "the replayed base is the run's",
                      "passes": same_base(got["engine"], records[t], space)})
        truth_of = {c["case"]: c["truth"] for c in a_cases[t]}
        runs[t] = read_run(units, got["found"], truth_of, got["action"])
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the refusals fell where they did "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/refusals.py writes {record_path()}")
    records, conflicts, kept = read_inputs()
    readings, gates = read_everything(records, conflicts, kept)
    for g in gates:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(K_RUNS)
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
        "source": {"conflicts": str(conflicts_path()),
                   "conflicts_from": conflicts["_env"].get("git_commit"),
                   "readings": str(readings_path()),
                   "readings_from": kept["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in K_RUNS}},
        "surface": "every edge refused between the rules of the winner's and the runner-up's "
                   "queues at a case K's ranking took, read in the base right before it was "
                   "tried; the policy's verdict over the points both its rules match",
        "constants": {"top_doors": TOP_DOORS},
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
