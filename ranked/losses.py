"""
WHETHER A COPY'S LOSSES, INSTALLED BEFORE ITS WINS, WOULD HAVE BEEN KEPT.
`FINDINGS_RANKED.md`, *One thing the last reading left free*, N, found that the
loop installs a birth's wins before its losses, and that most of the copies'
refused losses closed through a win the same answer had installed first. Its
*What it does not settle*, first item, asks whether those losses, tried first,
would have been kept. `corrections/fall.py` replayed `PLAN_CORRECTIONS.md`'s L
runs with each birth's losses first, and the same declarations kept most of
what the base had lost. `IDEAS.md` carries the item under *What
`PLAN_RANKED.md` opens*. Asked for by Sergi on 2026-11-21. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`: the rules in birth
order, and every edge each birth tried with the engine's verdict.
**`copies.json`**, whose rows give every copy, and whose `alone` names each
run's copy whose leaving out alone gains most. **`sides.json`**, whose rows give
every side of a copy the engine refused for closing a cycle. **`score.json`**,
whose bases the gates hold this reading to.

**A replay** is the run's births in order, each with its rule and every edge its
birth tried. It is read on the run's own engine: rung 2's in L, and in K the
ranking its votes choose. That ranking reads every citation of a born rule's
answer, installed or not, so it is the same in every replay. There are three:
- **the record's order**, every birth's edges in the log's order;
- **the copies' losses first**: at a copy's birth, the edges that put another
  rule above the copy are tried before those that put the copy above another,
  each kind in the log's order; every other birth's in the log's order;
- **every birth's losses first**, the same at every birth, as
  `corrections/fall.py`'s replay does.

A replay is not the loop that would have run. A base installed in another
order decides the arrivals otherwise, and would have escalated other cases.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **What the copies' losses first keep, and what they cost.** In each run:
      of the copies' losses the record refused for a cycle, how many the
      replay installs; of the copies' wins the record installed, how many it
      refuses; and the same at the other births, where the base it meets has
      changed.
  (b) **What it decides.** In each run, the points of the space each replay
      decides right, beside the record's, by half; and the points the copies'
      losses first gain and lose, by their true queue.
  (c) **Every birth's losses first.** The same for the third replay.
  (d) **The copy that costs most.** In each run, the copy whose leaving out
      alone gains most, if leaving it out gains, as `copies.json` reads it.
      Each of its losses the record refused, and whether the copies' losses
      first install it; each of its wins the record installed that they
      refuse.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The record's order is the run.** Replayed in the record's order, every
     edge gets the log's verdict, and the base decides exactly the points the
     run's final base decides right, which is Stage C's.
  2. **The copies are `copies.json`'s.** The copies read off each run are its
     rows, each covering exactly its originals' points.
  3. **The refused losses are `sides.json`'s.** The copies' losses the log
     refused for a cycle are `sides.json`'s refused losses.
  4. **A replay moves only the order.** Each replay tries every edge of the log
     once, at the birth that tried it.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  O1. **Kept.** Pooled over the six runs, the replay with the copies' losses
      first installs more than half of the copies' losses the record refused
      for a cycle.
  O2. **For fewer wins.** Pooled, that replay refuses fewer of the copies'
      wins the record installed than it installs of the copies' losses the
      record refused.
  O3. **Decides more in L.** In every L run, the base with the copies' losses
      first decides right more points of the space than the record's.
  O4. **Every birth's, more still.** Pooled over the six runs, the base with
      every birth's losses first decides right more points than the base with
      the copies' losses first.

A clause that reads a missing value fails.

**The drafter's account.**
- **O1, trusted most.** N found 541 of the 908 refused losses closed only
  through the copy's own wins, installed first.
  - **Tried before them**, such a loss meets no win of the copy: the copy can
    reach the rule above it only through a rule holding it.
  - **A loss N found closing through containment**, or either way, still
    closes so.
  - **By then the base differs a little from the record's**, since earlier
    copies' edges went in another order.
- **O2.** A loss kept by going first can block the win it used to be refused
  through, since that win's rule already reached the rule now above the copy.
  - **What favours the clause.** `R0275`'s six losses were refused through
    one win, over `R0263`: tried first, the six would block that one win. One
    win blocking many losses favours the clause.
  - **What works against it.** A broad copy's many wins, each reaching a rule
    above it, work the other way.
- **O3, the bet.** In L a refused loss leaves a conflict the engine gets
  wrong, whichever side is right.
  - **What a kept loss does.** A right loss decides its points right, and a
    wrong one decides them wrong, as the conflict did. A win refused instead
    does the reverse.
  - **What the records say.** N found 548 of the 908 refused losses right by
    the policy. `corrections/fall.py` found the losses first keeping most of
    what two of `PLAN_CORRECTIONS.md`'s L runs lost.
  - **Where the bet can lose.** L r3's refused losses were more often wrong
    than right, 76 and 55.
  - **K is read by no clause.** In K the ranking decides a conflict, so a kept
    loss changes a point only where the ranking would have sided otherwise.
- **O4, trusted least.** The other births refused losses too, and
  `corrections/fall.py`'s replay moved every birth. A lever that keeps losses
  for the copies should keep them for the rest. But what every birth's losses
  first does to the wins of the births that are not copies, none of N's figures
  say.

**The bet is O3.** **O1 is trusted most.** **O4 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole;
- `sides.json` whole: every refused side of every copy, with what closed it,
  where its cycle is and the policy's verdict;
- `copies.json` whole;
- `corrections/fall.py`'s replay with the losses first, and its findings, as
  `FINDINGS_CORRECTIONS.md` states them;
- `authorship/loop.py`'s order of installation, `rung2/engine2.py`'s
  containment and `try_edge`, and `ranked/engine.py`'s tally, which reads every
  citation.

**What the drafter had not seen**: any replay of these runs with the losses
first, which losses it installs, which wins it refuses, or what any of its
bases decides.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-21, after `ranked/sides.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m ranked.losses --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.losses
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from harness.provenance import describe, environment

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import copies as CO
from . import engine as E
from . import plan
from . import reading as R
from . import readings as RD
from . import sides as SD

RUNS, L_RUNS, K_RUNS = RD.RUNS, RD.L_RUNS, RD.K_RUNS
WIN, LOSS = SD.WIN, SD.LOSS
RECORD, COPIES_FIRST, EVERY_FIRST = "record", "copies_first", "every_first"
EVERY = "every birth"
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-21, after ranked/sides.py. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")

plain = RD.plain


# ---------------------------------------------------------------------------
# The replays
# ---------------------------------------------------------------------------

def ordered(edges: Sequence[erb.Edge], rid: str, first) -> list[erb.Edge]:
    """A birth's edges in the order a replay tries them: the log's, or, when its
    rule goes losses first, those that put another rule above it before those
    that put it above another, each kind in the log's order."""
    if first == EVERY or (first and rid in first):
        return [e for e in edges if e.loser == rid] + [e for e in edges if e.loser != rid]
    return list(edges)


def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           first) -> dict[str, Any]:
    """The run's births in order, every edge the log tried, at its birth, in the
    order `ordered` gives: `first` is None for the record's order, a set of rule
    ids whose losses go first, or `EVERY`. Read on the run's own engine: what it
    decides right, and every edge's verdict."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    eng = PriorityEngine(space=space)
    action: dict[str, str] = {}
    tally = E.Tally()
    verdict: dict[int, str] = {}
    tried_at: dict[int, int] = {}
    tries = 0
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        eng.add(rule_from(d), born_at=idx, keep_id=True)
        for e in ordered(by_birth.get(idx, []), rid, first):
            verdict[e.key] = eng.try_edge(e.winner, e.loser)
            tried_at[e.key] = idx
            tries += 1
        action[rid] = d["action"]
        tally.born(d)
    und = brows.undefeated_masks(eng)
    got = R.read(R.by_queue(und, action), tally.ranking, truth)
    own = "ranked" if record.get("arm") == plan.RANKED else "rung2"
    return {"right": got[own], "verdict": verdict, "tried_at": tried_at, "tries": tries,
            "engine": eng}


def sides_of(record: dict[str, Any], copies: set[str]) -> list[dict[str, Any]]:
    """Every edge the log tried, with its birth's rule, whether that rule is a
    copy, the rule's side, and the log's verdict."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    out = []
    for idx in sorted(by_birth):
        rid = born[idx]["rule_id"]
        for e in by_birth[idx]:
            out.append({"key": e.key, "birth": idx, "rule_id": rid, "copy": rid in copies,
                        "side": LOSS if e.loser == rid else WIN if e.winner == rid else None,
                        "logged": e.verdict})
    return out


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def is_the_record(record: dict[str, Any], got: dict[str, Any], base: dict[str, Any]) -> bool:
    """Gate 1, the replay's half: every edge gets the log's verdict, and the
    base decides exactly what the run's final base decides right."""
    logged = {e.key: e.verdict for es in erb.edges_by_birth(record).values() for e in es}
    return bool(got["verdict"] == logged and got["right"] == base["right"])


def same_refused_losses(sides: Sequence[dict], kept_rows: Sequence[dict]) -> bool:
    """Gate 3: the copies' losses the log refused for a cycle are `sides.json`'s
    refused losses."""
    mine = {s["key"] for s in sides
            if s["copy"] and s["side"] == LOSS and s["logged"] == EDGE_CYCLE}
    return bool(mine == {r["key"] for r in kept_rows if r["side"] == LOSS})


def only_the_order(record: dict[str, Any], got: dict[str, Any]) -> bool:
    """Gate 4: the replay tried every edge of the log once, at its birth."""
    edges = [e for es in erb.edges_by_birth(record).values() for e in es]
    return bool(got["tries"] == len(edges)
                and got["tried_at"] == {e.key: e.birth for e in edges})


# ---------------------------------------------------------------------------
# (a) to (d): one run
# ---------------------------------------------------------------------------

def changed(sides: Sequence[dict], before: dict[int, str], after: dict[int, str],
            copies: bool) -> dict[str, dict[str, int]]:
    """Of the copies' sides, or the other births', by side: how many were tried;
    of those the record refused for a cycle, how many the replay installs; of
    those it installed, how many the replay refuses."""
    out = {}
    for side in (WIN, LOSS):
        ss = [s for s in sides if s["copy"] == copies and s["side"] == side]
        refused = [s for s in ss if before[s["key"]] == EDGE_CYCLE]
        installed = [s for s in ss if before[s["key"]] == EDGE_OK]
        out[side] = {"tried": len(ss),
                     "refused_in_the_record": len(refused),
                     "installed_now": sum(after[s["key"]] == EDGE_OK for s in refused),
                     "installed_in_the_record": len(installed),
                     "refused_now": sum(after[s["key"]] == EDGE_CYCLE for s in installed)}
    return out


def by_queue(mask: int, truth: dict[str, int]) -> dict[str, int]:
    return {q: (mask & m).bit_count() for q, m in sorted(truth.items()) if mask & m}


def decides(got: dict[str, Any], keyword: int) -> dict[str, Any]:
    r = got["right"]
    return {"right": r.bit_count(), "halves": [(r & keyword).bit_count(),
                                               (r & ~keyword).bit_count()]}


def against(got: dict[str, Any], rec: dict[str, Any], sides: Sequence[dict],
            truth: dict[str, int], keyword: int) -> dict[str, Any]:
    """(a) to (c): a replay beside the record's order."""
    gained, lost = got["right"] & ~rec["right"], rec["right"] & ~got["right"]
    return dict(decides(got, keyword),
                change=got["right"].bit_count() - rec["right"].bit_count(),
                gained=gained.bit_count(), lost=lost.bit_count(),
                gained_by_queue=by_queue(gained, truth), lost_by_queue=by_queue(lost, truth),
                copies=changed(sides, rec["verdict"], got["verdict"], True),
                others=changed(sides, rec["verdict"], got["verdict"], False))


def costs_most(record: dict[str, Any], kept_run: dict[str, Any], sides: Sequence[dict],
               rec: dict[str, Any], got: dict[str, Any]) -> dict[str, Any] | None:
    """(d): the copy whose leaving out alone gains most, if leaving it out
    gains: its losses the record refused, with the replay's verdict on each;
    and its wins the record installed that the replay refuses."""
    hi = (kept_run.get("alone") or {}).get("most_gained")
    if not hi or hi["change"] <= 0:
        return None
    log = record["edge_log"]

    def edge(s):
        w, l, _ = log[s["key"]]
        return {"above": w, "below": l, "side": s["side"], "record": rec["verdict"][s["key"]],
                "copies_first": got["verdict"][s["key"]]}

    mine = [s for s in sides if s["rule_id"] == hi["rule_id"]]
    return {"rule_id": hi["rule_id"], "change": hi["change"],
            "refused_losses": [edge(s) for s in mine
                               if s["side"] == LOSS and rec["verdict"][s["key"]] == EDGE_CYCLE],
            "wins_refused_now": [edge(s) for s in mine
                                 if s["side"] == WIN and rec["verdict"][s["key"]] == EDGE_OK
                                 and got["verdict"][s["key"]] == EDGE_CYCLE]}


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int],
             copies: Sequence[dict], keyword: int, kept_run: dict[str, Any]
             ) -> tuple[dict[str, Any], dict[str, Any]]:
    """One run's three replays, read; and what the gates need."""
    ids = {c["rule_id"] for c in copies}
    rec = replay(record, space, truth, None)
    cf = replay(record, space, truth, ids)
    ef = replay(record, space, truth, EVERY)
    sides = sides_of(record, ids)
    return ({"copies": len(copies), RECORD: decides(rec, keyword),
             COPIES_FIRST: against(cf, rec, sides, truth, keyword),
             EVERY_FIRST: against(ef, rec, sides, truth, keyword),
             "costs_most": costs_most(record, kept_run, sides, rec, cf)},
            {"record": rec, "copies_first": cf, "every_first": ef, "sides": sides})


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

    def known(*xs) -> bool:
        return complete and all(x is not None for x in xs)

    refused = total(COPIES_FIRST, "copies", LOSS, "refused_in_the_record")
    kept = total(COPIES_FIRST, "copies", LOSS, "installed_now")
    wins = total(COPIES_FIRST, "copies", WIN, "refused_now")
    every, first = total(EVERY_FIRST, "right"), total(COPIES_FIRST, "right")
    in_l = [(runs.get(t) or {}).get(COPIES_FIRST) for t in L_RUNS]
    changes = [x.get("change") if isinstance(x, dict) else None for x in in_l]

    o1 = known(refused, kept) and refused > 0 and 2 * kept > refused
    o2 = known(kept, wins) and kept > 0 and wins < kept
    o3 = complete and all(isinstance(c, int) and c > 0 for c in changes)
    o4 = known(every, first) and every > first

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("O1", "pooled over the six runs, the replay with the copies' losses first installs "
                  "more than half of the copies' losses the record refused for a cycle", o1,
            {"refused_in_the_record": refused, "installed_now": kept}),
        out("O2", "pooled, that replay refuses fewer of the copies' wins the record installed "
                  "than it installs of the copies' losses the record refused", o2,
            {"wins_refused_now": wins, "losses_installed_now": kept}),
        out("O3", "in every L run, the base with the copies' losses first decides right more "
                  "points of the space than the record's", o3, dict(zip(L_RUNS, changes))),
        out("O4", "pooled over the six runs, the base with every birth's losses first decides "
                  "right more points than the base with the copies' losses first", o4,
            {"every_first": every, "copies_first": first}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "losses.json"


def copies_path():
    return plan.OUT / "copies.json"


def sides_path():
    return plan.OUT / "sides.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any], dict[str, Any]]:
    records = {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    return (records, json.loads(copies_path().read_text()),
            json.loads(sides_path().read_text()), json.loads(plan.score_path().read_text()))


def read_everything(records: dict[str, dict], kept: dict[str, Any], sides: dict[str, Any],
                    score: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    keyword = space.mask["has_security_keyword"][True]
    stage_c = score["RK-g"]["runs"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in RUNS:
        if t not in records:
            continue
        copies, ok = CO.copies_of_run(records[t], space)
        gates.append({"gate": 2, "run": t, "what": "the copies are copies.json's",
                      "passes": SD.same_copies(copies, kept["readings"]["runs"][t]["rows"], ok)})
        base = RD.base_of(records[t], space, truth)
        runs[t], got = read_run(records[t], space, truth, copies, keyword,
                                kept["readings"]["runs"][t])
        gates.append({"gate": 1, "run": t, "what": "the record's order is the run",
                      "passes": bool(is_the_record(records[t], got["record"], base)
                                     and RD.gate_one(base, stage_c[t], keyword, space.n))})
        gates.append({"gate": 3, "run": t, "what": "the refused losses are sides.json's",
                      "passes": same_refused_losses(got["sides"],
                                                    sides["readings"]["runs"][t]["rows"])})
        gates.append({"gate": 4, "run": t, "what": "a replay moves only the order",
                      "passes": all(only_the_order(records[t], got[k])
                                    for k in ("record", "copies_first", "every_first"))})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether a copy's losses, installed before its "
                                             "wins, would have been kept (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/losses.py writes {record_path()}")
    records, kept, sides, score = read_inputs()
    readings, gates = read_everything(records, kept, sides, score)
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
        "source": {"copies": str(copies_path()), "copies_from": kept["_env"].get("git_commit"),
                   "sides": str(sides_path()), "sides_from": sides["_env"].get("git_commit"),
                   "score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "the whole space of 134,400 points, on each run's own engine, for three "
                   "replays of the run's births and edges: the record's order, the copies' "
                   "losses first, and every birth's losses first",
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
