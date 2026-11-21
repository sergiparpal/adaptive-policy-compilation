"""
WHY THE COPIES' DECLARED SIDES CLOSED CYCLES. `FINDINGS_RANKED.md`, *Two things
the last reading left free*, L, found that a copy enters its original's region
with its own answer's sides, and not with the order its original had been
given. In L r2 `R0258`'s declared win over `R0252`, and in L r3 `R0275`'s
declared losses to the keyword's security rules, were refused for closing
cycles, and each copy stands beside rules its original had lost to. Its *What
it does not settle*, second item, asks through which rules those cycles closed,
and whether they are older rules nested in the copy's region, as
`ranked/refusals.py` found in K. `IDEAS.md` carries it under *What
`PLAN_RANKED.md` opens*. Asked for by Sergi on 2026-11-21. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`: the rules in birth
order, every edge each birth tried with the engine's verdict, and every arrival
with the rule that decided it. **`copies.json`**, whose rows give every copy
with its originals and the rule that erred at its ticket, and whose `alone`
names each run's copy whose leaving out alone gains most.

**A side** is an edge a birth tried. Its rule, **the newborn**, is at one end of
it: a `win` when the newborn is declared above the other rule, a `loss` when
below. **A copy's side** is a side tried at a copy's birth, and **a refused
side** one the engine refused for closing a cycle. Each is one entry of the
run's log.

**Each refused side of a copy is read at the moment it was tried**, in the
engine replayed birth by birth, every edge in the log's order: after the edges
its birth tried before it, and before it. As `ranked/refusals.py` reads a
refusal:
- **Its paths** are the chains of what beats what, by containment and by
  declared edges, from the lower rule to the upper. The engine refused the side
  because one exists.
- **What closes it at the copy.** `own answer` when no path is left with the
  copy's declarations installed earlier at its birth taken out; `containment`
  when none is left with the containments at the copy taken out; `either` when
  paths of both kinds remain.
- **The rules at the copy** are those the paths step through by containment at
  the copy: nested in it, on a win; holding it, on a loss.
- **Where the cycle is.** `somewhere` when some path runs through rules that
  all match a point both rules match; `nowhere` otherwise.
- **A door** is a step every path passes through.
- **The policy's verdict** on the refused side, over the points both its rules
  match: `right`, `wrong` or `even`.
- **Its original's order.** Whether, by what beats what in that base, an
  original of the copy already stood on the side of the other rule the copy
  declared, `repeats`; on the other side, `contradicts`; on both, `both`; or on
  neither, `unordered`.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **How often.** In each run, the sides the copies' births tried, by the
      engine's verdict, beside the sides the other births tried.
  (b) **What closed each refused side.** In each run, the copies' refused
      sides by side; by what closes their cycle at the copy, by where the
      cycle is, and by whether a door carries every path; by the policy's
      verdict; and by the original's order. Each also apart for the wins and
      the losses.
  (c) **Through which rules.** At each refused side, whether its rules at the
      copy include one of another queue than the copy's, one wrong at its
      birth, the rule that erred at the copy's ticket, or a copy. The rules at
      the copy that carry the most refused sides, and the doors that carry the
      most, with the births of their rules.
  (d) **The copy that costs most.** In each run, the copy whose leaving out
      alone gains most, if leaving it out gains, as `copies.json` reads it:
      each of its refused sides with one shortest path, and the queue and
      birth of every rule on it.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the log.** In each run, every edge the replay tries gets
     the verdict the record's log gives it.
  2. **The copies are `copies.json`'s.** The copies read off each run, with
     their originals and the rule that erred at their ticket, are its rows,
     and each covers exactly its originals' points.
  3. **Every refused side is met where it was tried.** At its copy's birth,
     the lower rule reaches the upper right before it, and the engine refuses
     it there for closing a cycle.
  4. **The replayed base is the run's.** At the end, the replay's extensions
     and declared edges are those of `ranked/reading.py`'s walk of the record.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  N1. **Refused more often.** Pooled over the six runs, the engine refused for
      closing a cycle a larger share of the copies' sides than of the other
      births' sides.
  N2. **Wins.** Pooled, more than half of the copies' refused sides are wins.
  N3. **Losses through its own wins.** Of the copies' refused losses, pooled,
      at more than half the cycle closes through the copy's own wins:
      `own answer` or `either`.
  N4. **Nowhere.** Pooled, the cycle is nowhere at more than half of the
      copies' refused sides.

A clause that reads a missing value fails.

**The drafter's account.**
- **What the order of installation settles.** The loop installs a birth's wins
  before its losses (`authorship/loop.py`'s `install_declarations`), and at a
  birth only the newborn's answer declares.
  - **A refused win.** While a copy's wins are tried no rule is declared above
    it, so a refused win can only enter the copy through a rule nested in it:
    it closes through containment. That rule lies inside the original too,
    since the two cover the same points, and beats it too. So the other rule
    already stood above the original, and a refused win contradicts its
    original's order.
  - **A refused loss** leaves the copy through its own wins installed before
    it, or through a rule holding it, which holds the original too.
  - **No clause reads what this settles.**
- **N1.** A copy enters a region the base had already ordered. Its original was
  born there. The rules nested in the region, among them at a reported error
  the rule that erred, beat the copy as they beat the original, and carry
  whatever order earlier births gave them. v1c lists only what is not wholly
  governed when the round is listed, which works the other way.
- **N2.** Wins are tried first, and 377 of the 461 copies are broad, with one
  or two conditions: a broad region holds many older rules. The refusals
  reading found the newborn's wins carrying most refusals in every K run.
- **N3, the bet.** `corrections/fall.py` found most of what two of
  `PLAN_CORRECTIONS.md`'s L runs lost after their peak lost where a newborn's
  loss was refused: a win the same answer had installed first already reached
  the rule the newborn should lose to. Few rules hold a broad region, so a
  refused loss's path leaves a copy mostly through its own wins. `R0275`'s
  answer declared it below the four security rules its original had lost to,
  and all four were refused.
- **N4.** `corrections/paths.py` found the cycles of L's refused right sides
  mostly nowhere the pair shares. The refusals reading found most nowhere in K
  r1 and K r3, and most somewhere in K r2. A rule nested in a broad copy may lie
  anywhere in its region, away from what the copy shares with the rule it
  claims to beat.

**The bet is N3.** **N2 is trusted most**, by the order of installation and the
copies' breadth. **N4 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole, and `copies.json` whole: every copy with its
  birth, its originals and the rule that erred at its ticket. For the copies
  whose leaving out alone moves most, the edges of their answer the engine
  refused that name a rule standing where they cost, among them `R0258`'s win
  over `R0252` and `R0275`'s losses to `R0027`, `R0181`, `R0234` and `R0238`;
- `refusals.json` as `FINDINGS_RANKED.md`'s I states it;
- `corrections/fall.py`'s and `corrections/paths.py`'s findings, as
  `FINDINGS_CORRECTIONS.md` states them;
- `authorship/loop.py`'s order of installation, `rung2/engine2.py`'s
  containment and `try_edge`, and `ranked/refusals.py`, whose reading of an
  edge this one reuses.

**What the drafter had not seen**: how many sides any birth tried or the engine
refused beyond those, any path, door or rule at a copy, where any cycle is, the
policy's verdict on any refused side, or the original's order at any of them.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-21, after `ranked/copies.py` and
`ranked/asked.py`. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.sides --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.sides
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
from rung2.engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK, EDGE_SELF,
                           EDGE_UNKNOWN, PriorityEngine, Space)

from . import conflicts as CF
from . import copies as CO
from . import plan
from . import readings as RD
from . import refusals as RF

RUNS = RD.RUNS
WIN, LOSS = RF.WIN, RF.LOSS
SIDES = (WIN, LOSS)
OWN, CONTAINMENT, EITHER = RF.OWN, RF.CONTAINMENT, RF.EITHER
CLOSES = RF.CLOSES
SOMEWHERE, NOWHERE = RF.SOMEWHERE, RF.NOWHERE
WHERE = RF.WHERE
VERDICTS = RF.VERDICTS
TRIED = (EDGE_OK, EDGE_CYCLE, EDGE_CONTRADICTS, EDGE_DISJOINT, EDGE_SELF, EDGE_UNKNOWN)
REPEATS, CONTRADICTS, BOTH, UNORDERED = "repeats", "contradicts", "both", "unordered"
ORDERS = (REPEATS, CONTRADICTS, BOTH, UNORDERED)
THROUGH = ("another_queue", "wrong_at_its_birth", "the_rule_that_erred", "a_copy")
TOP = 12
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-21, after ranked/copies.py and ranked/asked.py. "
    "The expectation in the module's docstring was written and committed before the reading "
    "ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


# ---------------------------------------------------------------------------
# One refused side, read at the moment it was tried
# ---------------------------------------------------------------------------

def one_path(engine: PriorityEngine, src: str, dst: str, nodes: set[str]) -> list[str] | None:
    """One shortest path from `src` to `dst` through `nodes`, its rules in
    order, the lowest-numbered step taken first."""
    parent: dict[str, str | None] = {src: None}
    level = [src]
    while level and dst not in parent:
        nxt = []
        for x in level:
            for y in sorted(engine.wins_over(x)):
                if y in nodes and y not in parent:
                    parent[y] = x
                    nxt.append(y)
        level = nxt
    if dst not in parent:
        return None
    out: list[str] = []
    at: str | None = dst
    while at is not None:
        out.append(at)
        at = parent[at]
    return out[::-1]


def original_order(engine: PriorityEngine, winner: str, loser: str, newborn: str,
                   originals: Sequence[str]) -> str:
    """Where the copy's originals stood, in this base, against the other rule:
    on the side the copy declared, on the other, on both, or on neither."""
    other = loser if newborn == winner else winner
    reach = CP.forward(engine, other)
    above = {o for o in originals if other in CP.forward(engine, o)}
    below = {o for o in originals if o in reach}
    same, against = (above, below) if newborn == winner else (below, above)
    if same and against:
        return BOTH
    return REPEATS if same else CONTRADICTS if against else UNORDERED


def read_side(engine: PriorityEngine, e: erb.Edge, copy: dict[str, Any], idx: int,
              own: set[tuple[str, str]], installed_at: dict[tuple[str, str], int],
              action: dict[str, str], truth: dict[str, int]) -> dict[str, Any]:
    """A copy's refused side, read before it is tried."""
    rid = copy["rule_id"]
    a = RF.analyse(engine, e.winner, e.loser, rid, idx, own, installed_at, action, truth)
    nodes = CP.forward(engine, e.loser) & CP.backward(engine, e.winner)
    return dict(a, key=e.key, copy=rid, other=e.loser if e.winner == rid else e.winner,
                original=original_order(engine, e.winner, e.loser, rid, copy["originals"]),
                path=one_path(engine, e.loser, e.winner, nodes) if a["reaches"] else None)


def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           copies: Sequence[dict]) -> dict[str, Any]:
    """The record's births and edges, in order: every refused side of a copy
    read before it is tried, and every side tallied by its verdict. Gates 1 and
    3 are kept as it goes."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    of = {c["rule_id"]: c for c in copies}
    engine = PriorityEngine(space=space)
    action: dict[str, str] = {}
    installed_at: dict[tuple[str, str], int] = {}
    found: dict[int, dict[str, Any]] = {}
    tried = {"copies": Counter(), "others": Counter()}
    elsewhere = 0
    log_ok = met_ok = True
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        action[rid] = d["action"]
        c = of.get(rid)
        own: set[tuple[str, str]] = set()
        for e in by_birth.get(idx, []):
            key = (e.winner, e.loser)
            here = rid in key
            target = c is not None and here and e.verdict == EDGE_CYCLE
            if target:
                found[e.key] = read_side(engine, e, c, idx, own, installed_at, action, truth)
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            log_ok &= why == e.verdict
            if here:
                tried["copies" if c else "others"][why] += 1
            else:
                elsewhere += 1
            if target:
                met_ok &= bool(why == EDGE_CYCLE and found[e.key]["reaches"])
            if why == EDGE_OK and not before and e.loser in engine.decl_above[e.winner]:
                installed_at[key] = idx
                own.add(key)
    return {"found": found,
            "tried": {k: {v: n.get(v, 0) for v in TRIED} for k, n in tried.items()},
            "elsewhere": elsewhere, "log_ok": bool(log_ok), "met_ok": bool(met_ok),
            "engine": engine, "action": action}


def same_copies(copies: Sequence[dict], kept: Sequence[dict], ok: bool) -> bool:
    """Gate 2: the copies read off the run are `copies.json`'s rows, with their
    originals and the rule that erred, and each covers its originals' points."""
    def keyed(rows):
        return [(r["rule_id"], list(r["originals"]), r["erring"]) for r in rows]
    return bool(ok and keyed(copies) == keyed(kept))


# ---------------------------------------------------------------------------
# (b), (c), (d): the refused sides of one run
# ---------------------------------------------------------------------------

def tally(rows: Sequence[dict], key, keys: Sequence[str]) -> dict[str, int]:
    c = Counter(key(r) for r in rows)
    return {k: c.get(k, 0) for k in keys}


def through(side: dict[str, Any], births: dict[str, dict], copy: dict[str, Any],
            ids: set[str]) -> dict[str, bool]:
    """(c): what the rules at the copy include."""
    rs = side["nested_at_newborn"]
    return {"another_queue": any(births[r]["queue"] != copy["queue"] for r in rs),
            "wrong_at_its_birth": any(not births[r]["right_at_birth"] for r in rs),
            "the_rule_that_erred": copy.get("erring") in rs,
            "a_copy": any(r in ids for r in rs)}


def summary(rows: Sequence[dict]) -> dict[str, Any]:
    return {"sides": len(rows), "copies": len({r["copy"] for r in rows}),
            "side": tally(rows, lambda r: r["side"], SIDES),
            "closes": tally(rows, lambda r: r["closes"], CLOSES),
            "where": tally(rows, lambda r: r["where"], WHERE),
            "door": sum(bool(r["doors"]) for r in rows),
            "verdict": tally(rows, lambda r: r["verdict"], VERDICTS),
            "original": tally(rows, lambda r: r["original"], ORDERS),
            "through": {k: sum(r["through"][k] for r in rows) for k in THROUGH}}


BIRTH_KEYS = ("queue", "born_at", "kind", "report", "governing", "right_at_birth", "conditions")


def at_the_copy(rows: Sequence[dict], births: dict[str, dict]) -> list[dict[str, Any]]:
    """(c): the rules at the copy that carry the most refused sides."""
    n = Counter(r for row in rows for r in row["nested_at_newborn"])
    return [dict({k: births[r][k] for k in BIRTH_KEYS}, rule_id=r, sides=k)
            for r, k in sorted(n.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]]


def doors(rows: Sequence[dict], births: dict[str, dict]) -> list[dict[str, Any]]:
    """(c): the doors that carry the most refused sides, with the births of the
    rules at both ends."""
    n: Counter = Counter()
    kept: dict[tuple[str, str], dict] = {}
    for row in rows:
        for d in row["doors"]:
            k = (d["upper"], d["lower"])
            n[k] += 1
            kept[k] = d
    return [dict(kept[k], sides=c, upper_born_at=births[k[0]]["born_at"],
                 lower_born_at=births[k[1]]["born_at"])
            for k, c in sorted(n.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]]


def costs_most(rows: Sequence[dict], kept_run: dict[str, Any],
               births: dict[str, dict]) -> dict[str, Any] | None:
    """(d): the copy whose leaving out alone gains most, if leaving it out
    gains, as `copies.json` reads it; each of its refused sides with one
    shortest path, and every rule on it with its queue and birth."""
    hi = (kept_run.get("alone") or {}).get("most_gained")
    if not hi or hi["change"] <= 0:
        return None
    keys = ("queue", "born_at", "kind", "right_at_birth", "conditions")
    return {"rule_id": hi["rule_id"], "change": hi["change"], "keyword": hi["keyword"],
            "sides": [{"above": r["above"], "below": r["below"], "side": r["side"],
                       "closes": r["closes"], "where": r["where"], "verdict": r["verdict"],
                       "original": r["original"], "nested_at_newborn": r["nested_at_newborn"],
                       "doors": r["doors"],
                       "path": [dict({k: births[x][k] for k in keys}, rule_id=x)
                                for x in r["path"] or []]}
                      for r in rows if r["copy"] == hi["rule_id"]]}


def slim(row: dict[str, Any]) -> dict[str, Any]:
    """A refused side as the record keeps it: the rules its paths run through
    counted, not listed."""
    out = {k: v for k, v in row.items() if k != "path_rules"}
    out["path_rule_count"] = len(row["path_rules"])
    return out


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int],
             copies: Sequence[dict], kept_run: dict[str, Any]) -> tuple[dict, dict]:
    got = replay(record, space, truth, copies)
    births = CF.births_of(record, space, truth)
    of = {c["rule_id"]: c for c in copies}
    rows = []
    for key in sorted(got["found"]):
        s = got["found"][key]
        c = of[s["copy"]]
        rows.append(dict(s, queue=c["queue"], copy_born_at=c["born_at"], kind=c["kind"],
                         erring=c["erring"], erring_nested=c["erring_nested"],
                         through=through(s, births, c, set(of))))
    return ({"copies": len(copies), "tried": got["tried"], "elsewhere": got["elsewhere"],
             "refused": {"all": summary(rows),
                         WIN: summary([r for r in rows if r["side"] == WIN]),
                         LOSS: summary([r for r in rows if r["side"] == LOSS])},
             "at_the_copy": at_the_copy(rows, births),
             "doors": doors(rows, births),
             "costs_most": costs_most(rows, kept_run, births),
             "rows": [slim(r) for r in rows]}, got)


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    have = [runs[t] for t in RUNS if t in runs]
    complete = len(have) == len(RUNS)

    def total(*path) -> int | None:
        n = 0
        for r in have:
            x: Any = r
            for p in path:
                x = x.get(p) if isinstance(x, dict) else None
            if not isinstance(x, int):
                return None
            n += x
        return n

    def tried(who) -> int | None:
        n = 0
        for r in have:
            v = (r.get("tried") or {}).get(who)
            if not isinstance(v, dict) or not all(isinstance(x, int) for x in v.values()):
                return None
            n += sum(v.values())
        return n

    tc, to = tried("copies"), tried("others")
    rc, ro = total("tried", "copies", EDGE_CYCLE), total("tried", "others", EDGE_CYCLE)
    sides, wins = total("refused", "all", "sides"), total("refused", "all", "side", WIN)
    losses = total("refused", LOSS, "sides")
    own, either = total("refused", LOSS, "closes", OWN), total("refused", LOSS, "closes", EITHER)
    nowhere = total("refused", "all", "where", NOWHERE)

    def known(*xs) -> bool:
        return complete and all(x is not None for x in xs)

    n1 = known(tc, to, rc, ro) and tc > 0 and to > 0 and rc * to > ro * tc
    n2 = known(sides, wins) and sides > 0 and 2 * wins > sides
    n3 = known(losses, own, either) and losses > 0 and 2 * (own + either) > losses
    n4 = known(sides, nowhere) and sides > 0 and 2 * nowhere > sides

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("N1", "pooled over the six runs, the engine refused for closing a cycle a larger "
                  "share of the copies' sides than of the other births' sides", n1,
            {"copies": [rc, tc], "others": [ro, to]}),
        out("N2", "pooled, more than half of the copies' refused sides are wins", n2,
            {"sides": sides, "wins": wins}),
        out("N3", "of the copies' refused losses, pooled, at more than half the cycle closes "
                  "through the copy's own wins", n3,
            {"losses": losses, "own answer": own, "either": either}),
        out("N4", "pooled, the cycle is nowhere at more than half of the copies' refused sides",
            n4, {"sides": sides, "nowhere": nowhere}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "sides.json"


def copies_path():
    return plan.OUT / "copies.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    return records, json.loads(copies_path().read_text())


def read_everything(records: dict[str, dict], kept: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    kept_runs = kept["readings"]["runs"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in RUNS:
        if t not in records:
            continue
        copies, ok = CO.copies_of_run(records[t], space)
        gates.append({"gate": 2, "run": t, "what": "the copies are copies.json's",
                      "passes": same_copies(copies, kept_runs[t]["rows"], ok)})
        runs[t], got = read_run(records[t], space, truth, copies, kept_runs[t])
        gates.append({"gate": 1, "run": t, "what": "the replay is the log",
                      "passes": got["log_ok"]})
        gates.append({"gate": 3, "run": t, "what": "every refused side is met where it was "
                                                   "tried", "passes": got["met_ok"]})
        gates.append({"gate": 4, "run": t, "what": "the replayed base is the run's",
                      "passes": RF.same_base(got["engine"], records[t], space)})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the copies' declared sides closed cycles "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/sides.py writes {record_path()}")
    records, kept = read_inputs()
    readings, gates = read_everything(records, kept)
    for g in sorted(gates, key=lambda g: (RUNS.index(g["run"]), g["gate"])):
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(RUNS)
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
        "source": {"copies": str(copies_path()),
                   "copies_from": kept["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "every edge a copy's birth tried with the copy at one end, by the engine's "
                   "verdict, beside every other birth's; each refused for closing a cycle read "
                   "in the base right before it was tried; the policy's verdict over the "
                   "points both its rules match",
        "constants": {"top": TOP},
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
