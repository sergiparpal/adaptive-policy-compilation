"""
WHY THE ERROR ARM'S EDGES SIT ON REGIONS THIRD RULES GOVERN.
`reasoned_loop/decided.py` found the pattern: in the error arm, third rules
govern most of the shared region of the pairs `RL-e` counts against the
proposer, and half of the others'. On those points an edge decides nothing,
whichever way it points. `IDEAS.md` carries the question of why, free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Two routes could put a pair's shared region under third rules:
- **At listing.** The placement round lists every rule of another queue the
  draft meets over the space, whether or not the base already settles their
  shared region. The proposer is then asked for a side on a conflict that third
  rules have already decided.
- **Later.** Rules born after the pair come to govern its region. Under the
  error trigger, a ticket the pair's winner decides wrongly escalates, and the
  rule born there may be placed above both.
A third lies between them: **the answer itself**. The draft may place itself
below a rule that already beats the older rule of the pair.

--------------------------------------------------------------------------
WHAT IT READS, per run, over the half of the space without the keyword
--------------------------------------------------------------------------
**The base, replayed in birth order.** Each rule is added at the case it was
born at, and its edges are tried after it in `edge_log` order, as
`edges/rebuild.py` pairs them with the births.

**The pairs** are `RL-e`'s population, `reasoned_loop/decided.py`'s rows. A
point of a pair's shared region is *governed* when a rule other than the two
beats each of them there. Each pair's shared region is split by when its points
became governed:
  at_listing   governed when the draft has been added and none of its edges
               yet: by subsumption and by the base's edges;
  by_answer    governed once the draft's own edges are in, and not before;
  later        governed at the end and not at the pair's birth;
  never        not governed at the end.

**Each later point** goes to the birth that completed its governance, by the
cause of its escalation: impasse, conflict or error. An error birth is a
*repair* of the pair when its ticket lies in the pair's shared region and the
rule that decided the ticket wrongly was the pair's winner.

**The readings**, by arm and pair verdict, over the strict pairs:
- the points in each part, and each part's share of the governed points;
- the later points by cause;
- the pairs with a repair.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the base.** Its final rules and graph are the final
     engine's, as `reasoned_loop/decided.py` reads it.
  2. **The end is `decided.py`'s.** Every row's shared points, and its points
     governed at the end of the replay, are the row's `shared` and `governed`.
  3. **The parts add up, and governance never goes back.** A point governed at
     one birth is governed at every later one, and the four parts sum to the
     shared region.
  4. **The tickets are the record's.** Every birth's case is one point of the
     space, and every error birth's deciding rule stood in the base before the
     birth.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the error arm's strict pairs, pooled over its three runs.
*Missing* means a pair whose pair verdict is `b`, as `decided.py` uses it.

  G1. **The missing pairs were governed later.** At least half of the points
      third rules govern at the end, on the missing pairs' shared regions,
      became governed after the pair's birth.
  G2. **By the error trigger.** At least half of the missing pairs' later points
      were completed by births at error escalations.
  G3. **By repair.** At least a third of the missing pairs' later points were
      completed by repairs: births at an error escalation on a ticket of the
      pair's region that the pair's winner had decided.
  G4. **The missing pairs more than the others.** The share of the shared
      region that became governed later is higher for the missing pairs than
      for the pairs whose verdict is `a`.
  G5. **Later more than at listing.** Over all strict pairs, more points became
      governed later than were governed at listing and by the answer together.

So the drafter expects the error trigger to repair a wrong edge by covering it
rather than by turning it, and the placement round's listing to account for
less. **G2 sits near its base rate**: most of the error arm's births are at
error escalations, so it holds unless the other births do most of the
governing. The bet is G3, which the drafter trusts least, then G1.

**What the drafter had seen**:
- `FINDINGS_REASONED_LOOP.md` whole, `decided.json` and `unplaced.json` whole,
  with the governed shares at the end by pair verdict;
- the escalations by cause in each run, from Stage C;
- two rows of e r1's error escalations, for their fields;
- every run's edges by channel, all of them on the write channel;
- `edges/rebuild.py` and `fidelity/replay.py`.

**What the drafter had not seen**: any pair's governance at listing or at its
birth, any later point's birth, or any repair.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for on 2026-11-04, after `reasoned_loop/decided.py` and
`reasoned_loop/unplaced.py`. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not
a calibration event. Zero API calls.

Usage:  python3 -m reasoned_loop.governed --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m reasoned_loop.governed
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any

from harness.domain import ATTRIBUTES
from harness.provenance import describe, environment

from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import decided, plan, score

F = Fraction
HIT, MISS = decided.HIT, decided.MISS
IMPASSE, CONFLICT, ERROR = plan.IMPASSE, plan.CONFLICT, plan.ERROR
REPAIR = "REPAIR"
CAUSES = (IMPASSE, CONFLICT, ERROR, REPAIR)
PARTS = ("at_listing", "by_answer", "later", "never")

# The expectation's lines.
G1_SHARE = F(1, 2)
G2_SHARE = F(1, 2)
G3_SHARE = F(1, 3)

PROVENANCE = (
    "POST-RUN: asked for on 2026-11-04, after reasoned_loop/decided.py and "
    "reasoned_loop/unplaced.py. The expectation in the module's docstring was "
    "written and committed before the reading ran. Not a signed row; no verdict "
    "moves.")


def record_path():
    return plan.OUT / "governed.json"


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return score.frac(x)


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


# ---------------------------------------------------------------------------
# The replay
# ---------------------------------------------------------------------------

def point_of(case, space: Space) -> int:
    """A case's point of the space, as a mask."""
    m = space.full
    for a in ATTRIBUTES:
        m &= space.mask[a][getattr(case, a)]
    return m


def governed(engine: PriorityEngine, w: str, l: str, shared: int) -> int:
    """The points of `shared` where a rule other than the pair beats each of
    `w` and `l`."""
    return shared & decided.defeaters(engine, w) & decided.defeaters(engine, l, without=w)


def births_of_edges(record: dict) -> dict[tuple[str, str], int]:
    """The case whose birth tried each edge, first if an edge was tried twice."""
    out: dict[tuple[str, str], int] = {}
    by_birth = erb.edges_by_birth(record)
    for idx in sorted(by_birth):
        for e in by_birth[idx]:
            out.setdefault((e.winner, e.loser), idx)
    return out


def replay(record: dict, pairs: set[tuple[str, str]], space: Space, mask: int,
           corpus) -> dict[str, Any]:
    """The base in birth order, and every pair's shared region split by when its
    points became governed."""
    born = erb.births(record)
    by_birth = erb.edges_by_birth(record)
    birth_of = births_of_edges(record)
    rows = {r["idx"]: r for r in record["records"]}
    engine = PriorityEngine(space=space)
    state: dict[tuple[str, str], dict[str, Any]] = {}
    went_back = False
    tickets_ok = True
    for idx in sorted(born):
        row = rows.get(idx, {})
        point = point_of(corpus[idx], space)
        if point.bit_count() != 1:
            tickets_ok = False
        if row.get("cause") == ERROR and row.get("engine_rule") not in engine.ext:
            tickets_ok = False
        engine.add(rule_from(born[idx]), born_at=idx, keep_id=True)
        for k in sorted(p for p in pairs if birth_of.get(p) == idx):
            w, l = k
            shared = engine.ext[w] & engine.ext[l] & mask
            state[k] = {"birth": idx, "shared": shared,
                        "at_listing": governed(engine, w, l, shared),
                        "later": Counter()}
        for e in by_birth.get(idx, []):
            engine.try_edge(e.winner, e.loser)
        for k, s in state.items():
            w, l = k
            g = governed(engine, w, l, s["shared"])
            if s["birth"] == idx:
                s["by_answer"] = g & ~s["at_listing"]
                s["now"] = g
                continue
            went_back |= bool(s["now"] & ~g)
            new = g & ~s["now"]
            if new:
                cause = row.get("cause")
                if cause == ERROR and row.get("engine_rule") == w and point & s["shared"]:
                    cause = REPAIR
                s["later"][cause] += new.bit_count()
            s["now"] = g
    return {"engine": engine, "state": state, "went_back": went_back,
            "tickets_ok": tickets_ok}


def pair_rows(rows: list[dict], state: dict) -> list[dict[str, Any]]:
    """`decided.py`'s rows of `RL-e`'s population, each with its parts."""
    out = []
    for r in rows:
        if not r["rl_e"]:
            continue
        s = state[(r["winner"], r["loser"])]
        later = sum(s["later"].values())
        out.append({"winner": r["winner"], "loser": r["loser"], "older": r["older"],
                    "pair": r["pair"], "point": r["point"], "birth": s["birth"],
                    "shared": s["shared"].bit_count(),
                    "at_listing": s["at_listing"].bit_count(),
                    "by_answer": s["by_answer"].bit_count(), "later": later,
                    "never": (s["shared"] & ~s["now"]).bit_count(),
                    "governed_end": s["now"].bit_count(),
                    "later_by_cause": {c: s["later"].get(c, 0) for c in CAUSES}})
    return out


# ---------------------------------------------------------------------------
# The readings
# ---------------------------------------------------------------------------

def sums(rows: list[dict]) -> dict[str, Any]:
    out: dict[str, Any] = {"pairs": len(rows), "shared": sum(r["shared"] for r in rows)}
    for p in PARTS:
        out[p] = sum(r[p] for r in rows)
    out["later_by_cause"] = {c: sum(r["later_by_cause"][c] for r in rows) for c in CAUSES}
    gov = out["at_listing"] + out["by_answer"] + out["later"]
    out["governed_end"] = gov
    out["of_governed"] = {p: frac(share(out[p], gov)) for p in ("at_listing", "by_answer", "later")}
    out["of_shared"] = {p: frac(share(out[p], out["shared"])) for p in PARTS}
    out["pairs_with_a_repair"] = sum(1 for r in rows if r["later_by_cause"][REPAIR])
    out["pairs_governed_later"] = sum(1 for r in rows if r["later"])
    out["pairs_wholly_governed_at_listing"] = sum(
        1 for r in rows if r["shared"] and r["at_listing"] == r["shared"])
    return out


def arm_reading(rows: list[dict]) -> dict[str, Any]:
    strict = [r for r in rows if r["pair"] in (HIT, MISS)]
    return {"a": sums([r for r in strict if r["pair"] == HIT]),
            "b": sums([r for r in strict if r["pair"] == MISS]),
            "strict": sums(strict)}


def read_expectation(e: dict[str, Any]) -> list[dict[str, Any]]:
    b, a, s = e["b"], e["a"], e["strict"]
    gov_b = b["at_listing"] + b["by_answer"] + b["later"]
    g1 = share(b["later"], gov_b)
    errors_b = b["later_by_cause"][ERROR] + b["later_by_cause"][REPAIR]
    g2 = share(errors_b, b["later"])
    g3 = share(b["later_by_cause"][REPAIR], b["later"])
    later_b, later_a = share(b["later"], b["shared"]), share(a["later"], a["shared"])
    return [
        {"clause": "G1", "what": "at least half of the missing pairs' governed points became "
                                 "governed after the pair's birth",
         "reading": {"later": b["later"], "of": gov_b, "share": frac(g1)},
         "holds": g1 is not None and g1 >= G1_SHARE},
        {"clause": "G2", "what": "at least half of the missing pairs' later points were "
                                 "completed by births at error escalations",
         "reading": {"by_errors": errors_b, "of": b["later"], "share": frac(g2)},
         "holds": g2 is not None and g2 >= G2_SHARE},
        {"clause": "G3", "what": "at least a third of the missing pairs' later points were "
                                 "completed by repairs",
         "reading": {"by_repairs": b["later_by_cause"][REPAIR], "of": b["later"],
                     "share": frac(g3)},
         "holds": g3 is not None and g3 >= G3_SHARE},
        {"clause": "G4", "what": "the share of the shared region governed later is higher "
                                 "for the missing pairs than for the pairs with verdict a",
         "reading": {"b": frac(later_b), "a": frac(later_a)},
         "holds": later_b is not None and later_a is not None and later_b > later_a},
        {"clause": "G5", "what": "over all strict pairs, more points became governed later "
                                 "than at listing and by the answer together",
         "reading": {"later": s["later"], "at_listing_and_by_answer":
                     s["at_listing"] + s["by_answer"]},
         "holds": s["later"] > s["at_listing"] + s["by_answer"]},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def check(runs: dict[str, dict], replays: dict[str, dict],
          rows: dict[str, list[dict]]) -> list[dict[str, Any]]:
    out = []
    for t, run in runs.items():
        final, mine = run["engine"], replays[t]["engine"]
        same_graph = (decided.graph_edges(final) == decided.graph_edges(mine)
                      and [(r.rule_id, r.action) for r in final.rules]
                      == [(r.rule_id, r.action) for r in mine.rules]
                      and all(final.ext[r.rule_id] == mine.ext[r.rule_id] for r in final.rules))
        out.append({"gate": 1, "run": t, "what": "the replay is the base", "passes": same_graph})
        by_key = {(r["winner"], r["loser"]): r for r in run["rows"] if r["rl_e"]}
        end_ok = all(by_key[(r["winner"], r["loser"])]["shared"] == r["shared"]
                     and by_key[(r["winner"], r["loser"])]["governed"] == r["governed_end"]
                     for r in rows[t])
        out.append({"gate": 2, "run": t, "what": "the end is decided.py's", "passes": end_ok})
        adds_up = (not replays[t]["went_back"]
                   and all(sum(r[p] for p in PARTS) == r["shared"] for r in rows[t]))
        out.append({"gate": 3, "run": t, "what": "the parts add up, and governance never "
                                                 "goes back", "passes": adds_up})
        out.append({"gate": 4, "run": t, "what": "the tickets are the record's",
                    "passes": replays[t]["tickets_ok"]})
    return out


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def plain(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items() if not k.endswith("_exact")}
    if isinstance(x, list):
        return [plain(v) for v in x]
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the error arm's edges sit on regions third "
                                             "rules govern (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"reasoned_loop/governed.py writes {record_path()}")
    records, _stage_c, runs = decided.read_all()
    space, _tmask, mask = decided.world()
    corpus = list(MI.corpus())
    replays, rows = {}, {}
    for t, rec in records.items():
        pairs = {(r["winner"], r["loser"]) for r in runs[t]["rows"] if r["rl_e"]}
        replays[t] = replay(rec, pairs, space, mask, corpus)
        rows[t] = pair_rows(runs[t]["rows"], replays[t]["state"])
    checked = check(runs, replays, rows)
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    tags = {a: [t for t in runs if t.startswith(f"{a}_")] for a in plan.ARMS}
    arms = {a: arm_reading([r for t in tags[a] for r in rows[t]]) for a in plan.ARMS}
    arms["pooled"] = arm_reading([r for t in runs for r in rows[t]])
    expectation = read_expectation(arms["e"])
    record_path().write_text(json.dumps(st._rounded(plain({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"record": str(decided.record_path()),
                   "decided_from": json.loads(decided.record_path().read_text())
                   ["_env"].get("git_commit")},
        "surface": "the half of the space without the keyword, 67,200 points",
        "constants": {"G1_SHARE": str(G1_SHARE), "G2_SHARE": str(G2_SHARE),
                      "G3_SHARE": str(G3_SHARE)},
        "gates": checked,
        "arms": arms,
        "runs": {t: {"readings": arm_reading(rows[t]), "pairs": rows[t]} for t in runs},
        "expectation": expectation,
    })), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
