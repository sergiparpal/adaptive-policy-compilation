"""
COPIES OF THE SAME QUEUE. `FINDINGS_RANKED.md`, *One thing the last two readings
left free*, K, found that 461 of the six runs' 1,519 births cover exactly the
tickets an earlier rule of their own queue covers, far more than the twins of
another queue it read. Its *What it does not settle*, first item, asks what the
copies cost the base, and whether they are mostly the queue's general line
written again at reported errors, as `PLAN_CORRECTIONS.md`'s readings found.
`IDEAS.md` carries it under *What `PLAN_RANKED.md` opens*. Asked for by Sergi on
2026-11-20, with *Why L's twins are born at the conflicts it asks about*, which
`ranked/asked.py` reads. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`: the rules in birth
order, every edge each birth tried, every arrival with its truth, the hidden
rule that governs it and the rule that decided it, and each escalation's first
call with its `copies`. **`score.json`**, whose bases the gates hold this
reading to.

**A copy** is a born rule whose first call recorded, among its `copies`, an
earlier rule of its own queue: a rule that covers exactly the same tickets and
sends them to the same queue. That earlier rule is **its original**.
- **Its birth** is an escalation at a ticket inside its original's region, so
  never an impasse: a reported error, or in arm L a conflict the loop asked
  about.
- **The rule that erred**, at a birth at a reported error, is the rule that had
  decided the ticket wrongly. It is **nested in the copy** when its region lies
  strictly inside the copy's: then it beats the copy there by containment, as
  it beat the original, and no declaration can turn that.
- **A copy decides its ticket** in a base when it stands undefeated at its
  birth ticket and its queue is what the base's own engine decides there. It
  is read in the base right after its birth, and in the run's final base.
- **The base without its copies** is the run's births replayed in order with
  every copy left out and every edge with a copy at one end left out. Every
  other edge is tried again, as the engine takes it, and in arm K the votes of
  the copies, and the votes cast about them, are left uncounted. It is not the
  loop that would have run: without them other cases would have escalated.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **How often, and how born.** In each run, the copies; by the kind of their
      birth, the hidden rule governing the ticket, and the queue the report
      named; at a reported error, whether the rule that erred is nested in the
      copy, and whether an original stood at the ticket when it arrived.
  (b) **What they do.** Whether each copy decides its own ticket right after
      its birth and in the final base, and whether an original stands there.
  (c) **What they cost.** The points of the space the base without its copies
      decides right, beside the run's final base, by half.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The copies are the record's.** Every copy's first call recorded its
     original among its `copies`, and the two rules' conditions cover exactly
     the same points.
  2. **The bases are Stage C's.** Each run's final base, rebuilt birth by birth,
     decides on its own engine the share and the halves `score.json` keeps.
  3. **The replay that leaves rules out leaves out nothing else.** Replayed with
     nothing left out, it decides exactly the points the run's final base
     decides right.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  L1. **At reported errors.** In the six runs pooled, more than half of the
      copies were born at a reported error.
  L2. **Below the rule that erred.** Of the copies born at a reported error,
      pooled, at more than half the rule that erred is nested in the copy.
  L3. **Kept out of their ticket.** In every run, more than half of the
      copies do not decide their own ticket in the final base.
  L4. **Little to cost.** In every run, what the base without its copies
      decides right differs from what the run's final base decides right by
      fewer than 1,344 points, a hundredth of the space.

A clause that reads a missing value fails.

**The drafter's account.**
- **L1.** A copy cannot be born at an impasse, since its original matches its
  ticket. Most escalations are reported errors, and arm K asks about no
  conflict.
- **L2 and L3.** `corrections/forgotten.py` found most of L's corrections born
  and never deciding their own ticket: a rule nested inside the correction,
  mostly the one that had erred there, kept it by containment. A copy covers
  what its original covers, so the rule that kept the original from deciding
  the ticket keeps the copy too, when it is nested. A blind first call, told
  the queue, writes the queue's general line again
  (`corrections/broad.py`), and it is the line the base already held.
- **L4.** A copy adds nothing its original does not cover. It changes the base
  only through the edges its answer declares and, in K, its votes. The drafter
  expects those to move little.

**The bet is L3.** **L1 is trusted most.** **L4 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole and `twins.json` whole, among it each run's count
  of copies, by run, and nothing else of them;
- Stage C's count of each run's escalations by kind, and L r1's rows by
  outcome and cause;
- `corrections/forgotten.py`'s and `corrections/broad.py`'s findings, as
  `FINDINGS_CORRECTIONS.md` states them;
- `placement/protocol.py`'s handling of a copy, `authorship/protocol.py`'s
  `copies_of`, `rung2/engine2.py`'s containment and `try_edge`, and
  `ranked/engine.py`'s tally of votes.

**What the drafter had not seen**: any copy's birth, its original, the rule
that erred at its ticket, whether it decides anything, or what the base
without the copies decides.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/twins.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m ranked.copies --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.copies
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from blind import rows as brows
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space, strictly_below

from . import engine as E
from . import plan
from . import reading as R
from . import readings as RD
from . import twins as TW

RUNS = RD.RUNS
HUNDREDTH = RD.HUNDREDTH
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/twins.py. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


# ---------------------------------------------------------------------------
# (a): the copies, and how they were born
# ---------------------------------------------------------------------------

def copies_of_run(record: dict[str, Any], space: Space) -> tuple[list[dict], bool]:
    """Every copy of a run, with its birth; and gate 1."""
    rules = {d["rule_id"]: d for d in record["rules"]}
    rows = record["records"]
    handed = record.get("reports_handed") or {}
    out, ok = [], True
    for esc in record["escalations"]:
        if esc["verdict"] != "nacida":
            continue
        n = rules[esc["rule_id"]]
        copies = list((esc["calls"][0] or {}).get("copies") or [])
        originals = [e for e in copies if rules[e]["action"] == n["action"]]
        if not originals:
            continue
        ext = TW.extension(space, n["conditions"])
        ok &= all(TW.extension(space, rules[e]["conditions"]) == ext for e in originals)
        idx = n["born_at"]
        row = rows[idx]
        erring = row.get("engine_rule") if esc["kind"] == plan.ERROR else None
        nested = bool(erring in rules and strictly_below(
            TW.extension(space, rules[erring]["conditions"]), ext))
        out.append({"rule_id": n["rule_id"], "queue": n["action"], "born_at": idx,
                    "kind": esc["kind"], "report": handed.get(str(idx)),
                    "governing": row["truth_rule"], "truth": row["truth"],
                    "originals": originals, "erring": erring,
                    "erring_queue": rules[erring]["action"] if erring in rules else None,
                    "erring_nested": nested, "points": ext.bit_count(),
                    "conditions": RD.conditions_of(n["conditions"])})
    return out, bool(ok)


def at_birth(record: dict[str, Any], copies: Sequence[dict], space: Space,
             corpus: Sequence) -> dict[str, dict[str, Any]]:
    """At each copy's ticket: whether an original stood there when the case
    arrived, and whether the copy decides it right after its birth, on the
    run's own engine with the votes counted so far."""
    at = {c["born_at"]: c for c in copies}
    own = "ranked" if record.get("arm") == plan.RANKED else "rung2"
    walk = R.Walk(record, space)
    out = {}
    for idx in sorted(walk.born):
        c = at.get(idx)
        here = R.point_of(corpus[idx], space) if c else 0
        stood = bool(c) and any(walk.und.get(e, 0) & here for e in c["originals"])
        walk.birth(idx)
        if c:
            now = {"queues": walk.queues(), "ranking": tuple(walk.tally.ranking), "own": own}
            d = decision_at(now, here)
            stands = bool(walk.und.get(c["rule_id"], 0) & here)
            out[c["rule_id"]] = {"original_stood": stood, "stands": stands, "decision": d,
                                 "decides": stands and d == c["queue"]}
    return out


# ---------------------------------------------------------------------------
# (b): what the copies do in the final base
# ---------------------------------------------------------------------------

def decision_at(base: dict[str, Any], here: int) -> str | None:
    """What the base's own engine decides at one point: one queue standing, or
    in arm K the ranking's first among those standing; None at a conflict of
    arm L or where nothing stands."""
    present = [q for q in base["ranking"] if base["queues"].get(q, 0) & here]
    if base["own"] == "ranked":
        return present[0] if present else None
    return present[0] if len(present) == 1 else None


def in_final(base: dict[str, Any], copies: Sequence[dict], space: Space,
             corpus: Sequence) -> list[dict[str, Any]]:
    und = base["walk"].und
    out = []
    for c in copies:
        here = R.point_of(corpus[c["born_at"]], space)
        d = decision_at(base, here)
        stands = bool(und.get(c["rule_id"], 0) & here)
        original = any(und.get(e, 0) & here for e in c["originals"])
        out.append({"rule_id": c["rule_id"], "decision": d, "stands": stands,
                    "decides": stands and d == c["queue"], "original_stands": original,
                    "right": d == c["truth"]})
    return out


# ---------------------------------------------------------------------------
# (c): the base without its copies
# ---------------------------------------------------------------------------

def replay_without(record: dict[str, Any], space: Space, truth: dict[str, int],
                   drop: set[str]) -> dict[str, Any]:
    """The run's births in order, the rules in `drop` left out with every edge
    that has one at an end, and in arm K their votes uncounted; read on the
    run's own engine, as Stage C reads a base."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    eng = PriorityEngine(space=space)
    action: dict[str, str] = {}
    tally = E.Tally()
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        if rid in drop:
            continue
        eng.add(rule_from(d), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            if e.winner in drop or e.loser in drop:
                continue
            eng.try_edge(e.winner, e.loser)
        action[rid] = d["action"]
        tally.born(d)
    queues = R.by_queue(brows.undefeated_masks(eng), action)
    got = R.read(queues, tally.ranking, truth)
    own = "ranked" if record.get("arm") == plan.RANKED else "rung2"
    return {"right": got[own], "rules": len(eng.rules)}


def cost(record: dict[str, Any], base: dict[str, Any], copies: Sequence[dict], space: Space,
         truth: dict[str, int], keyword: int) -> dict[str, Any]:
    without = replay_without(record, space, truth, {c["rule_id"] for c in copies})
    w, f = without["right"], base["right"]
    return {"final": {"right": f.bit_count(), "halves": [(f & keyword).bit_count(),
                                                         (f & ~keyword).bit_count()]},
            "without": {"right": w.bit_count(), "rules": without["rules"],
                        "halves": [(w & keyword).bit_count(), (w & ~keyword).bit_count()]},
            "change": w.bit_count() - f.bit_count(),
            "gained_without": (w & ~f).bit_count(), "lost_without": (f & ~w).bit_count()}


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def read_run(record: dict[str, Any], base: dict[str, Any], space: Space,
             truth: dict[str, int], corpus: Sequence, keyword: int) -> tuple[dict, bool]:
    copies, ok = copies_of_run(record, space)
    born = at_birth(record, copies, space, corpus)
    final = {x["rule_id"]: x for x in in_final(base, copies, space, corpus)}
    rows = [dict(c, at_birth=born[c["rule_id"]], final=final[c["rule_id"]]) for c in copies]
    reported = [c for c in rows if c["kind"] == plan.ERROR]
    births = sum(1 for e in record["escalations"] if e["verdict"] == "nacida")
    return ({"births": births, "copies": len(rows),
             "by_kind": dict(sorted(Counter(c["kind"] for c in rows).items())),
             "by_governing": dict(sorted(Counter(c["governing"] for c in rows).items())),
             "by_queue": dict(sorted(Counter(c["queue"] for c in rows).items())),
             "at_a_report": len(reported),
             "report_names_its_queue": sum(c["report"] == c["queue"] for c in reported),
             "erring_nested": sum(c["erring_nested"] for c in reported),
             "original_stood_at_birth": sum(c["at_birth"]["original_stood"] for c in rows),
             "decide_their_ticket_at_birth": sum(c["at_birth"]["decides"] for c in rows),
             "decide_their_ticket": sum(c["final"]["decides"] for c in rows),
             "stand_at_their_ticket": sum(c["final"]["stands"] for c in rows),
             "an_original_stands_there": sum(c["final"]["original_stands"] for c in rows),
             "ticket_right_in_the_final_base": sum(c["final"]["right"] for c in rows),
             "cost": cost(record, base, copies, space, truth, keyword),
             "rows": rows}, ok)


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    have = [runs[t] for t in RUNS if t in runs]
    complete = len(have) == len(RUNS)
    n = sum(r.get("copies") or 0 for r in have)
    rep = sum(r.get("at_a_report") or 0 for r in have)
    nested = sum(r.get("erring_nested") or 0 for r in have)
    l1 = complete and bool(n) and 2 * rep > n
    l2 = complete and bool(rep) and 2 * nested > rep
    l3 = complete and all((r.get("copies") or 0) > 0
                          and 2 * (r["copies"] - (r.get("decide_their_ticket") or 0)) > r["copies"]
                          for r in have)
    l4 = complete and all(abs(((r.get("cost") or {}).get("change"))
                              if (r.get("cost") or {}).get("change") is not None
                              else HUNDREDTH) < HUNDREDTH for r in have)

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("L1", "in the six runs pooled, more than half of the copies were born at a reported "
                  "error", l1, {"copies": n, "at_a_report": rep}),
        out("L2", "of the copies born at a reported error, pooled, at more than half the rule "
                  "that erred is nested in the copy", l2, {"at_a_report": rep, "nested": nested}),
        out("L3", "in every run, more than half of the copies do not decide their own ticket in "
                  "the final base", l3,
            {t: [runs[t].get("decide_their_ticket"), runs[t].get("copies")]
             for t in RUNS if t in runs}),
        out("L4", "in every run, what the base without its copies decides right differs from "
                  "what the run's final base decides right by fewer than 1,344 points", l4,
            {t: ((runs[t].get("cost") or {}).get("change")) for t in RUNS if t in runs}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "copies.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    return records, json.loads(plan.score_path().read_text())


def read_everything(records: dict[str, dict], score: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    corpus = list(MI.corpus())
    keyword = space.mask["has_security_keyword"][True]
    kept = score["RK-g"]["runs"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in RUNS:
        if t not in records:
            continue
        base = RD.base_of(records[t], space, truth)
        gates.append({"gate": 2, "run": t, "what": "the base is Stage C's",
                      "passes": RD.gate_one(base, kept[t], keyword, space.n)})
        same = replay_without(records[t], space, truth, set())["right"] == base["right"]
        gates.append({"gate": 3, "run": t, "what": "the replay that leaves rules out leaves out "
                                                   "nothing else", "passes": bool(same)})
        runs[t], ok = read_run(records[t], base, space, truth, corpus, keyword)
        gates.append({"gate": 1, "run": t, "what": "the copies are the record's", "passes": ok})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Copies of the same queue (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/copies.py writes {record_path()}")
    records, score = read_inputs()
    readings, gates = read_everything(records, score)
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
        "source": {"score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "every born rule of the six runs that covers exactly the tickets an earlier "
                   "rule of its own queue covers; its ticket read at its birth and in the run's "
                   "final base, and the base replayed without the copies over the whole space "
                   "of 134,400 points, on the run's own engine",
        "constants": {"hundredth": HUNDREDTH},
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
