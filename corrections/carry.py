"""
HOW MUCH OF THE FALL THE DOORS CARRY.
`corrections/gateway.py` found the rules above each run's gateway reaching it
through few doors, and `corrections/doors.py` found why the doors declared
themselves above it. `corrections/paths.py` had found the refused right sides'
paths entering `SECURITY_INCIDENT`'s rule through the gateway.
`FINDINGS_CORRECTIONS.md`, *Why so many rules sit above the gateway*, *What it
does not settle*, item 2, and `IDEAS.md` leave how much of what L lost rests on
the doors. Asked for by Sergi on 2026-11-15, after `corrections/doors.py`. Free
on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
**The same births and declarations are installed in the record's order**, as
`corrections/fall.py`'s `order_replay` installs them, with some declared edges
left out. Three kinds of replay are read:
  doors   the doors' edges left out: every edge `gateway.json` gives as
          door_win, a door's declared win over a gateway, installed at the
          door's birth;
  climbs  every declared win over a gateway left out: the doors' edges, and the
          climbs the engine refused, every edge a newborn's answer declared
          above a gateway born before it;
  door    each door's edges alone left out, one replay per door.
A door nested inside a gateway beats it by containment, which is no edge, and
stays in every replay.

**Each replay is read as `fall.json` reads the record's order**: the base's right
points over the space after every birth, its peak, its final share, its fall,
`SECURITY_INCIDENT`'s recall, its conflict points and its refusals for a cycle.
- **What a replay keeps** is its final share less the record's.
- **What it carries of the fall** is what it keeps over the record's fall, the
  record's peak less its final.

**Also read, for each replay against the record's order**, the edges whose
verdict differs:
- the edges the record refused for a cycle and this replay installs, and among
  them the newborns' losses to a rule of SECURITY_INCIDENT, the right sides
  `fall.py` found refused;
- the edges the record installed and this replay refuses;
- the climbs the record refused that this replay installs: new doors.

**It is not the loop that would have run.** A base without those edges decides
the arrivals otherwise, and would have escalated other cases. What it shows is
what the same births and the rest of the same declarations decide.

**Arm N is read the same way.** Only N r3 has a gateway. N r1 and N r2 leave
nothing out.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay that leaves nothing out is `fall.json`'s record order**: its
     curve is `fall.json`'s at every birth, and so are its final, its recall,
     its conflict points and its refusals for a cycle.
  2. **The edges left out are the records'.** Each door's edge is a door_win
     edge of `gateway.json`, tried at the door's birth and installed by the
     record's order. Each climb is a declared win over a gateway, and the climbs
     are `doors.json`'s.
  3. **Each replay is the record's order until it leaves an edge out**: its
     curve equals the record's at every birth before the first.
  4. **Every replay's masks are its engine's.**
  5. **A run without a gateway leaves nothing out.**

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the doors replay, or one door's.

  C1. **L r1 keeps half.** Without its door's edge, L r1 keeps at least half of
      its fall.
  C2. **L r2 keeps half.** Without its doors' edges, L r2 keeps at least half of
      its fall.
  C3. **L r3 keeps little.** Without its doors' edges, L r3 keeps at most a
      quarter of its fall.
  C4. **L keeps half.** Without their doors' edges, the three L runs keep at
      least half of their falls, summed.
  C5. **One door carries L r2's.** Without `R0051`'s edge alone, L r2 keeps at
      least half of what it keeps without all its doors' edges.
  C6. **N alike.** Without its door's edge, N r3 keeps at least a quarter of its
      fall.

A share over nothing has no value, and a clause that reads one fails. What a
run keeps can be less than nothing.

**The drafter's account.**
- **In L r1 one edge carries every path from above.** Every rule above `R0061`
  reaches it only through `R0062` (`gateway.json`). 70,270 of L r1's 79,155
  refused right sides' pair-points run through `R0061` (`paths.json`).
  - **Without that edge**, no newborn's wins reach `R0061`, so none reaches the
    keyword's rule through it.
  - **So the engine installs the newborns' losses to that rule**, and the
    conflicts the fall left close in `SECURITY_INCIDENT`'s favour (C1).
- **In L r2 too** (C2): 131,060 of its 136,505 pair-points run through its two
  gateways. `R0051`, born before the peak, carries 101 of the 102 rules above a
  gateway, and 63 of them reach one only through it (C5).
  - **Its nested door `R0265`** keeps a path once it is born, near the run's end.
    The drafter expects most refusals to have come before it.
- **In L r3 the fall was taken by containment** (C3). A correction nested in the
  keyword's rule took most of it, and no edge left out changes containment.
  `fall.py`'s losses first and `paths.py`'s engine barely moved it.
- **So L keeps half** (C4), on L r1's and L r2's falls.
- **In N r3 one door carries every path too** (C6). All five rules above `R0175`
  reach it only through `R0213`, and 98,240 of its 99,205 pair-points run through
  `R0175`. That door is right by the policy on the 440 points it shares with the
  gateway: leaving it out loses those, and keeps more.
- **A climb the record refused may be installed** once the doors' edges are out,
  and become a door. The climbs replay leaves those out too.

**The bet is C4.** It says the doors carry most of L's fall. **C1 is trusted
most**: one edge, and nearly every pair-point through its gateway. **C5 is
trusted least**: `gateway.json`'s count of the rules that reach a gateway only
through `R0051` is the final base's. At the births that refused the right sides,
other doors and rules may have carried the paths.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and `fall.json`, `paths.json`, `gateway.json`
  and `doors.json` whole: every run's curve, peak, final and fall; the losses
  first and the engine that refuses only where the cycle is; the pairs through
  each gateway; the doors, what each carries, and how they declared themselves;
- one replay of L r1 in the record's order, timed, which gave `fall.json`'s
  final right points and refusals;
- `corrections/fall.py`'s `order_replay`, `settle` and `decision`, and
  `rung2/engine2.py`'s `try_edge`.

**What the drafter had not seen**: any replay with an edge left out.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-15, after `corrections/doors.py`.
The expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m corrections.carry --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.carry
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import doors as dr
from . import fall as fl
from . import forgotten as fg
from . import gateway as gw
from . import plan

F = Fraction
SEC = fl.SEC
UNLABELLED = fl.UNLABELLED

# The replays.
RECORD, DOORS, CLIMBS = "record", "doors", "climbs"

# The expectation's lines.
C1_SHARE = F(1, 2)
C2_SHARE = F(1, 2)
C3_SHARE = F(1, 4)
C4_SHARE = F(1, 2)
C5_SHARE = F(1, 2)
C5_RUN, C5_DOOR = plan.tag(plan.LABELLED, 2), "R0051"
C6_SHARE = F(1, 4)
C6_RUN = plan.tag(UNLABELLED, 3)
L_RUNS = tuple(plan.tag(plan.LABELLED, k) for k in range(1, plan.REPS + 1))

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-15, after corrections/doors.py. The expectation "
    "in the module's docstring was written and committed before the reading ran. Not a "
    "signed row; no verdict moves.")

share, frac = fg.share, fg.frac


def record_path():
    return plan.OUT / "carry.json"


# ---------------------------------------------------------------------------
# The replay
# ---------------------------------------------------------------------------

def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           skip: frozenset[tuple[str, str]] = frozenset()) -> dict[str, Any]:
    """`corrections/fall.py`'s `order_replay` in the record's order, the edges in
    `skip` left out, with each edge it tries and what the engine did with it."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    und: dict[str, int] = {}
    action: dict[str, str] = {}
    curve: list[int] = []
    tried: list[dict[str, Any]] = []
    first_skip = None
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            if (e.winner, e.loser) in skip:
                first_skip = idx if first_skip is None else first_skip
                continue
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            tried.append({"born_at": idx, "newborn": rid, "winner": e.winner, "loser": e.loser,
                          "verdict": why,
                          "installed": (why == EDGE_OK and not before
                                        and e.loser in engine.decl_above[e.winner])})
        fl.settle(engine, und, action, rid, d["action"])
        curve.append(fl.right_of(fl.decision(und, action), truth).bit_count())
    dec = fl.decision(und, action)
    right = fl.right_of(dec, truth)
    return {"engine": engine, "action": action, "curve": curve, "tried": tried,
            "first_skip": first_skip, "right": right.bit_count(),
            "security": (right & truth.get(SEC, 0)).bit_count(),
            "conflict": dec["two"].bit_count(),
            "cycles": sum(1 for t in tried if t["verdict"] == EDGE_CYCLE),
            "masks_ok": und == brows.undefeated_masks(engine)}


def summary(got: dict[str, Any], truth: dict[str, int], n: int) -> dict[str, Any]:
    """`fall.py`'s `order_summary` of a replay."""
    return fl.order_summary(got, truth, n)


def against(base: dict[str, Any], got: dict[str, Any], gates: set[str]) -> dict[str, Any]:
    """The edges whose verdict differs between the record's order and a replay:
    refused for a cycle there and installed here, and the reverse; the newborns'
    losses to a rule of SECURITY_INCIDENT among the first; and the climbs over a
    gateway the record refused that the replay installs."""
    key = lambda t: (t["born_at"], t["winner"], t["loser"])
    there = {key(t): t for t in base["tried"]}
    action = base["action"]
    now_in, now_out, right_sides, new_doors = [], [], [], []
    for t in got["tried"]:
        b = there.get(key(t))
        if b is None:
            continue
        if b["verdict"] == EDGE_CYCLE and t["installed"]:
            now_in.append(t)
            if t["loser"] == t["newborn"] and action.get(t["winner"]) == SEC:
                right_sides.append(t)
            if t["winner"] == t["newborn"] and t["loser"] in gates:
                new_doors.append([t["winner"], t["loser"]])
        elif b["installed"] and t["verdict"] == EDGE_CYCLE:
            now_out.append(t)
    return {"refused_there_installed_here": len(now_in),
            "installed_there_refused_here": len(now_out),
            "right_sides_installed": len(right_sides),
            "new_doors": new_doors}


# ---------------------------------------------------------------------------
# What is left out
# ---------------------------------------------------------------------------

def door_edges(gateway_run: dict[str, Any]) -> list[tuple[str, str]]:
    """`gateway.json`'s door_win edges of a run, door then gateway."""
    return sorted((d["door"], d["gateway"]) for d in gateway_run.get("doors") or []
                  if d["kind"] == gw.DOOR_WIN)


def climb_edges(record: dict[str, Any], gates: dict[str, int]) -> list[tuple[str, str]]:
    """Every edge a newborn's answer declared above a gateway born before it, as
    the record tried it."""
    out = set()
    born = erb.births(record)
    for idx, edges in erb.edges_by_birth(record).items():
        rid = born[idx]["rule_id"]
        for e in edges:
            if e.winner == rid and e.loser in gates and gates[e.loser] < idx:
                out.add((e.winner, e.loser))
    return sorted(out)


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], space: Space, truth: dict[str, int],
             gateway_run: dict[str, Any], doors_run: dict[str, Any],
             fall_run: dict[str, Any]) -> dict[str, Any]:
    """One run's record order, its doors and climbs replays, one replay per door,
    and the gates. The three runs are its entries in `gateway.json`,
    `doors.json` and `fall.json`."""
    n = space.n
    gates = {g["rule_id"]: g["born_at"] for g in gateway_run.get("gateways") or []}
    base = replay(record, space, truth)
    peak = max(base["curve"]) if base["curve"] else 0
    fall_points = peak - base["right"]
    doors = door_edges(gateway_run)
    climbs = climb_edges(record, gates)
    arms: dict[str, frozenset] = {DOORS: frozenset(doors), CLIMBS: frozenset(climbs)}
    per_door = {d: frozenset(e for e in doors if e[0] == d) for d in sorted({e[0] for e in doors})}

    def read(skip: frozenset) -> tuple[dict[str, Any], dict[str, Any]]:
        got = replay(record, space, truth, skip) if skip else base
        kept = got["right"] - base["right"]
        return got, {**summary(got, truth, n),
                     "left_out": [list(e) for e in sorted(skip)],
                     "kept": {"points": kept, "share": frac(F(kept, n))},
                     "of_the_fall": frac(share(kept, fall_points)),
                     **against(base, got, set(gates))}

    replays = {}
    out_arms, out_doors = {}, {}
    for name, skip in arms.items():
        replays[name], out_arms[name] = read(skip)
    for d, skip in per_door.items():
        replays[d], out_doors[d] = read(skip)

    rec_summary = summary(base, truth, n)
    stored = st._rounded(rec_summary)
    declared = (fall_run.get("added_after_the_first_run") or {}).get("orders", {}).get("declared", {})
    fall_curve = [c["right"] for c in fall_run.get("curve") or []]
    tried = {(t["born_at"], t["winner"], t["loser"]): t for t in base["tried"]}
    born_at = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    doors_climbs = sorted({(l["newborn"], l["gateway"]) for l in doors_run.get("listings") or []
                           if l["side"] == dr.CLIMB})

    def same_prefix(got: dict[str, Any]) -> bool:
        if got["first_skip"] is None:
            return got["curve"] == base["curve"]
        k = sorted(erb.births(record)).index(got["first_skip"])
        return got["curve"][:k] == base["curve"][:k]

    gates_out = [
        {"gate": 1, "what": "the replay that leaves nothing out is fall.json's record order",
         "passes": (base["curve"] == fall_curve and base["masks_ok"]
                    and all(stored[k] == declared.get(k)
                            for k in ("final", "peak", "security_recall", "conflict",
                                      "refused_for_a_cycle")))},
        {"gate": 2, "what": "the edges left out are the records'",
         "passes": (all((born_at[dd], dd, g) in tried and tried[(born_at[dd], dd, g)]["installed"]
                        for dd, g in doors)
                    and climbs == doors_climbs and set(doors) <= set(climbs))},
        {"gate": 3, "what": "each replay is the record's order until it leaves an edge out",
         "passes": all(same_prefix(g_) for g_ in replays.values())},
        {"gate": 4, "what": "every replay's masks are its engine's",
         "passes": all(g_["masks_ok"] for g_ in replays.values()) and base["masks_ok"]},
        {"gate": 5, "what": "a run without a gateway leaves nothing out",
         "passes": bool(gates) or (not doors and not climbs)},
    ]
    return {"summary": {"gateways": sorted(gates, key=gates.get), "births": len(base["curve"]),
                        "record": {**rec_summary,
                                   "fall_points": fall_points}},
            "replays": out_arms, "doors": out_doors, "gates": gates_out}


def read_all_runs(records: dict[str, dict], gateway_record: dict[str, Any],
                  doors_record: dict[str, Any], fall_record: dict[str, Any], space: Space,
                  truth: dict[str, int]) -> dict[str, dict]:
    return {tag: read_run(rec, space, truth, gateway_record["runs"][tag],
                          doors_record["runs"][tag], fall_record["runs"][tag])
            for tag, rec in records.items()}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def kept_of(run: dict[str, Any], door: str | None = None) -> int:
    got = run["doors"][door] if door else run["replays"][DOORS]
    return got["kept"]["points"]


def fall_of(run: dict[str, Any]) -> int:
    return run["summary"]["record"]["fall_points"]


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    def at_least(kept: int, of: int, line: Fraction) -> bool:
        return of > 0 and F(kept, of) >= line

    def run_clause(cid, what, tag, line, most=False):
        r = runs.get(tag)
        kept, of = (kept_of(r), fall_of(r)) if r else (0, 0)
        holds = (of > 0 and F(kept, of) <= line) if most else at_least(kept, of, line)
        return {"clause": cid, "what": what,
                "reading": {"kept": kept, "fall": of, "share": frac(share(kept, of))},
                "holds": holds}

    pooled = [runs[t] for t in L_RUNS if t in runs]
    kept_l = sum(kept_of(r) for r in pooled)
    fall_l = sum(fall_of(r) for r in pooled)
    r5 = runs.get(C5_RUN)
    one = kept_of(r5, C5_DOOR) if r5 and C5_DOOR in r5["doors"] else 0
    every = kept_of(r5) if r5 else 0
    return [
        run_clause("C1", "without its door's edge, L r1 keeps at least half of its fall",
                   L_RUNS[0], C1_SHARE),
        run_clause("C2", "without its doors' edges, L r2 keeps at least half of its fall",
                   L_RUNS[1], C2_SHARE),
        run_clause("C3", "without its doors' edges, L r3 keeps at most a quarter of its fall",
                   L_RUNS[2], C3_SHARE, most=True),
        {"clause": "C4", "what": "without their doors' edges, the three L runs keep at least "
                                 "half of their falls, summed",
         "reading": {"kept": kept_l, "fall": fall_l, "share": frac(share(kept_l, fall_l))},
         "holds": at_least(kept_l, fall_l, C4_SHARE)},
        {"clause": "C5", "what": f"without {C5_DOOR}'s edge alone, L r2 keeps at least half of "
                                 "what it keeps without all its doors' edges",
         "reading": {"kept": one, "of": every, "share": frac(share(one, every))},
         "holds": at_least(one, every, C5_SHARE)},
        run_clause("C6", "without its door's edge, N r3 keeps at least a quarter of its fall",
                   C6_RUN, C6_SHARE),
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any], dict[str, Any]]:
    records = {plan.tag(a, k): json.loads(plan.run_path(a, k).read_text())
               for a in (plan.LABELLED, UNLABELLED) for k in range(1, plan.REPS + 1)}
    return (records, json.loads(gw.record_path().read_text()),
            json.loads(dr.record_path().read_text()), json.loads(fl.record_path().read_text()))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="How much of the fall the doors carry "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/carry.py writes {record_path()}")
    records, gateway_record, doors_record, fall_record = read_all()
    runs = read_all_runs(records, gateway_record, doors_record, fall_record, MI.space(),
                         MI.space_truth())
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
        "source": {"gateway": str(gw.record_path()), "doors": str(dr.record_path()),
                   "fall": str(fl.record_path()),
                   "gateway_from": gateway_record["_env"].get("git_commit"),
                   "doors_from": doors_record["_env"].get("git_commit"),
                   "fall_from": fall_record["_env"].get("git_commit")},
        "surface": "each run's base over the whole space after every birth, in the record's "
                   "order, with the doors' edges, every declared win over a gateway, or each "
                   "door's edges left out",
        "constants": {"C1_SHARE": str(C1_SHARE), "C2_SHARE": str(C2_SHARE),
                      "C3_SHARE": str(C3_SHARE), "C4_SHARE": str(C4_SHARE),
                      "C5_SHARE": str(C5_SHARE), "C5_RUN": C5_RUN, "C5_DOOR": C5_DOOR,
                      "C6_SHARE": str(C6_SHARE), "C6_RUN": C6_RUN},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        s = r["summary"]["record"]
        a = r["replays"]
        print(f"  {t}: record final {s['final']['share']['value']}, fall "
              f"{s['fall']['value'] if s['fall'] else None}; doors final "
              f"{a[DOORS]['final']['share']['value']}, climbs final "
              f"{a[CLIMBS]['final']['share']['value']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
