"""
WHERE K r2'S CONFLICTS FELL, AND WHICH BIRTHS MADE THEM. `FINDINGS_RANKED.md`,
*Six things Stage C left free*, A, found that no error of any K run was the
ranking in force erring where the last one would not. K r2's ranking took about
as many conflicts in billing's layer as K r1's and K r3's did, and erred at more
of them, and far fewer between deflection and the technical or general queue,
which the last ranking orders right. Its *What it does not settle*, first item,
asks which births made those conflicts, and from which reports. `IDEAS.md`
carries it under *What `PLAN_RANKED.md` opens*. Asked for by Sergi on
2026-11-20, with *Why one prompt drew different drafts*, which
`ranked/drafts.py` reads. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The three K runs**, `results_ranked/loop_k_r{1,2,3}.json`: the rules in birth
order, the edges tried at each birth, every arrival with its truth and the
hidden rule that governs it (`truth_rule`), every escalation with its kind and
the report it handed, and at every case who decided it. **`readings.json`**,
whose A the gates hold this reading to.

**The ranking's cases** are A's: the cases at which K's engine found rules of two
queues or more undefeated at the ticket, and decided by its ranking. **A case's
group** is A's table's, by the winner's queue and the runner-up's, either way:
- `deflection`: `SELF_SERVICE_DEFLECT` and `T2_TECHNICAL` or `T1_GENERAL`;
- `billing`: `ACCOUNT_MANAGER` and `BILLING_SPECIALIST`, or `BILLING_SPECIALIST`
  and `SELF_SERVICE_DEFLECT`;
- `rest`: any other pair.

**The rules standing at a case** are those undefeated at its ticket when it
arrived, before any birth at it, under rung 2's containments and the edges
installed. **The winner's rules** are those of the queue the ranking chose.
**A rule's birth** is the escalation it was born at: an impasse, or a reported
error and the queue its report named; the hidden rule governing that ticket,
and the ticket's true queue. A rule is **right at its birth** when its queue is
that ticket's.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  G-a. **The rules behind each group.** In each K run, for each group: its cases
       and its wrong ones by the hidden rule governing the ticket, and every rule
       standing at its cases, with how many it stands at, how many of those went
       wrong, and its birth.
  G-b. **K r2 at the others' deflection conflicts.** Every case at which K r1's
       or K r3's ranking took a conflict of the deflection group, read in K r2 at
       the same arrival: who decided it there, the ranking, rung 2 with one queue
       standing, or nobody; whether it was right; the queues standing; and
       whether a rule of the queue that won there in K r1 or K r3, and of the
       queue that lost, stood in K r2.
  G-c. **The rules that won the errors.** Every wrong decision of each K run's
       ranking, by group, with the winner's rules and their births.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The ranking's cases are A's.** In each K run, the cases the replay finds
     decided by the ranking, with their queues, decision, truth, governing rule
     and verdict, are `readings.json`'s A, case by case.
  2. **The replay is the engine's log.** At every case of each K run, the
     record's log says the ranking decided where the replay finds two queues or
     more standing, rung 2 where it finds one, and nobody where it finds none;
     and at the ranking's cases the queues are the log's, in its order.
  3. **A rule standing was born of its escalation.** Every rule standing at a
     case of the ranking was born at an escalation of its record whose verdict
     is a birth and whose rule it is.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  G1. **One rule's conflicts.** In K r1 and in K r3, one rule stands at more
      than half of the cases the ranking took in the deflection group.
  G2. **K r2 had one queue there.** At more than half of the cases at which K
      r1's or K r3's ranking took a conflict of the deflection group, K r2's
      engine decided the same arrival by rung 2, with one queue standing.
  G3. **And decided them right.** At more than half of those cases, K r2's
      decision was right.
  G4. **A few rules made K r2's billing errors.** In K r2, at most three rules
      won the ranking's wrong decisions in billing's layer.
  G5. **Each written at a report of its own queue.** Each of those rules was
      born at a reported error whose report named its queue.

A clause that reads a missing value fails.

**The drafter's account.**
- **G1.** A conflict needs two queues' rules undefeated at one ticket, so a
  stream of conflicts in one group needs a pair of regions that overlap and
  that no edge orders. K r1's ranking took 129 cases between deflection and the
  technical or general queue, and erred at none. The drafter expects one broad
  rule, written early, crossing the other queue's rules there, and standing at
  most of them.
- **G2, G3.** K r2's ranking took 33 cases of that group, so most of K r1's and
  K r3's cannot be its ranking's. K r2's base recalls `T1_GENERAL` at 0.8745 and
  `SELF_SERVICE_DEFLECT` at 0.8756 of the space, above K r1's 0.6015 for the
  first. So where the others took a conflict, the drafter expects K r2 to have
  held one queue, and the right one.
- **G4, G5.** A found that 12 of K r2's 20 errors in billing's layer sent
  tickets of `H12` to `BILLING_SPECIALIST`, and 8 sent tickets of `H10` and `H11`
  to `ACCOUNT_MANAGER`. A rule of `BILLING_SPECIALIST` standing at `H12`'s tickets
  reaches past its queue's region, and so does one of `ACCOUNT_MANAGER` at
  `H10`'s and `H11`'s. `PLAN_CORRECTIONS.md`'s readings found that told a queue,
  the blind first call writes that queue's general line from the catalogue: a
  rule of billing's tickets, or of the accounts at risk. One such rule for each
  queue would make every error, with room for one more. Most escalations are
  reported errors, 193 of K r1's 235.

**The bet is G5.** **G2 and G3 are trusted most.** **G1 and G4 are trusted
least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole, every figure in it, among them A's table and its
  account of K r2's errors by the rule governing the ticket, and Stage C's
  recall of each queue by run; `STATUS.md`'s and `IDEAS.md`'s entries on
  `PLAN_RANKED.md` and `PLAN_CORRECTIONS.md`; `ranked/readings.py` and its
  test;
- the hidden policy's 29 rules, and level 1's catalogue as `PLAN_CORRECTIONS.md`'s
  readings describe it;
- the records' layouts, by their keys; in K r1, how many cases each of the
  ranking, rung 2 and nobody decided, how many escalations each cause made,
  and how many were born or unplaced; that in the six runs every first call
  was answered at its first attempt, served by DeepInfra.

**What the drafter had not seen**: any rule standing at any case; any rule's
birth, conditions or extension beyond what `FINDINGS_RANKED.md` names; how K
r2 decided any arrival that K r1 or K r3 took by its ranking.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/readings.py`'s
six readings. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.conflicts --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.conflicts
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Condition, Space

from . import engine as E
from . import plan
from . import reading as R
from . import readings as RD
from . import score as S

SS, T2, BILL, AM = RD.SS, RD.T2, RD.BILL, RD.AM
T1 = "T1_GENERAL"
K_RUNS = RD.K_RUNS
OTHERS = ("k_r1", "k_r3")
GROUPS = ("deflection", "billing", "rest")
DEFLECTION = (frozenset((SS, T2)), frozenset((SS, T1)))
BILLING = (frozenset((AM, BILL)), frozenset((BILL, SS)))
WRONG_RULES_LINE = 3                           # G4: at most this many rules
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/readings.py's six readings. "
    "The expectation in the module's docstring was written and committed before the reading "
    "ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


def group_of(queues: Sequence[str]) -> str:
    """A case's group, by the winner's queue and the runner-up's, either way."""
    pair = frozenset(queues[:2])
    if pair in DEFLECTION:
        return "deflection"
    if pair in BILLING:
        return "billing"
    return "rest"


# ---------------------------------------------------------------------------
# Every case of a K run, as its engine held it
# ---------------------------------------------------------------------------

def cases_of(record: dict[str, Any], space: Space, corpus: Sequence) -> tuple[list[dict], bool]:
    """Every case of a K record: who decided it, the queues standing in the
    ranking's order then, and the rules standing by queue; and gate 2."""
    walk = R.Walk(record, space)
    rows, logs = record["records"], record["ranked"]["cases"]
    ok = len(rows) == len(logs) and all(r["idx"] == i for i, r in enumerate(rows))
    out = []
    for row, logged in zip(rows, logs):
        idx = row["idx"]
        here = R.point_of(corpus[idx], space)
        standing: dict[str, list[str]] = {}
        for rid, m in walk.und.items():
            if m & here:
                standing.setdefault(walk.action[rid], []).append(rid)
        present = [q for q in walk.tally.ranking if q in standing]
        by = logged["by"]
        expected = E.RANKING if len(present) > 1 else E.RUNG2 if present else None
        ok &= by == expected
        if by == E.RANKING:
            ok &= present == logged["queues"]
        decision = S.engines_decision(row) if by else None
        out.append({"case": idx, "by": by, "queues": present,
                    "standing": {q: sorted(standing[q]) for q in present},
                    "truth": row["truth"], "governing": row["truth_rule"],
                    "decision": decision,
                    "right": decision is not None and decision == row["truth"],
                    "reported": row["cause"] == plan.ERROR})
        if idx in walk.born:
            walk.birth(idx)
    return out, bool(ok)


def births_of(record: dict[str, Any], space: Space, truth: dict[str, int]) -> dict[str, dict]:
    """Every rule of a record by its id, with its birth."""
    escs = {e["idx"]: e for e in record["escalations"]}
    handed = record.get("reports_handed") or {}
    rows = record["records"]
    out = {}
    for d in record["rules"]:
        idx, rid, q = d["born_at"], d["rule_id"], d["action"]
        esc = escs.get(idx) or {}
        ext = space.extension([Condition(**c) for c in d["conditions"]])
        out[rid] = {"rule_id": rid, "queue": q, "born_at": idx, "kind": esc.get("kind"),
                    "verdict": esc.get("verdict"), "escalation_rule": esc.get("rule_id"),
                    "report": handed.get(str(idx)), "governing": rows[idx]["truth_rule"],
                    "birth_truth": rows[idx]["truth"], "right_at_birth": q == rows[idx]["truth"],
                    "conditions": RD.conditions_of(d["conditions"]),
                    "attributes": RD.attrs(d["conditions"]),
                    "points": ext.bit_count(), "own_points": (ext & truth.get(q, 0)).bit_count()}
    return out


def born_of_its_escalation(cases: Sequence[dict], births: dict[str, dict]) -> bool:
    """Gate 3: every rule standing at a case of the ranking was born at an
    escalation whose verdict is a birth and whose rule it is."""
    ok = True
    for c in cases:
        if c["by"] != E.RANKING:
            continue
        for rids in c["standing"].values():
            for rid in rids:
                b = births.get(rid)
                ok &= bool(b and b["verdict"] == "nacida" and b["escalation_rule"] == rid)
    return bool(ok)


def as_a(cases: Sequence[dict]) -> list[dict]:
    """The ranking's cases in the shape gate 1 compares with A's."""
    return [{"case": c["case"], "queues": c["queues"], "decision": c["decision"],
             "truth": c["truth"], "governing": c["governing"], "right": c["right"]}
            for c in cases if c["by"] == E.RANKING]


def same_as_a(cases: Sequence[dict], kept: Sequence[dict]) -> bool:
    """Gate 1."""
    mine = as_a(cases)
    theirs = [{k: r[k] for k in ("case", "queues", "decision", "truth", "governing", "right")}
              for r in kept]
    return bool(mine) and mine == theirs


# ---------------------------------------------------------------------------
# G-a: the rules behind each group
# ---------------------------------------------------------------------------

def tally(cases: Sequence[dict], key) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for c in cases:
        k = str(key(c))
        out.setdefault(k, {"cases": 0, "wrong": 0})
        out[k]["cases"] += 1
        out[k]["wrong"] += not c["right"]
    return dict(sorted(out.items()))


def ranked_by_cases(counts: Counter) -> list[tuple[str, int]]:
    """Rules by the cases they stand at, most first, ties by id."""
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def behind(cases: Sequence[dict], births: dict[str, dict], group: str) -> dict[str, Any]:
    """One group of one run: its cases, and every rule standing at them."""
    mine = [c for c in cases if c["by"] == E.RANKING and group_of(c["queues"]) == group]
    stands, wrong, won = Counter(), Counter(), Counter()
    for c in mine:
        for q, rids in c["standing"].items():
            for rid in rids:
                stands[rid] += 1
                wrong[rid] += not c["right"]
                won[rid] += q == c["decision"]
    return {
        "cases": len(mine), "wrong": sum(not c["right"] for c in mine),
        "by_pair": tally(mine, lambda c: " / ".join(sorted(c["queues"][:2]))),
        "by_governing": tally(mine, lambda c: c["governing"]),
        "by_pair_and_governing": tally(
            mine, lambda c: f"{' / '.join(sorted(c['queues'][:2]))} at {c['governing']}"),
        "rules": [dict(births[rid], cases=n, wrong=wrong[rid], won=won[rid])
                  for rid, n in ranked_by_cases(stands)],
    }


# ---------------------------------------------------------------------------
# G-b: K r2 at the others' deflection conflicts
# ---------------------------------------------------------------------------

def at_the_others(per_run: dict[str, list[dict]]) -> dict[str, Any] | None:
    """Every case at which K r1's or K r3's ranking took a deflection conflict,
    read in K r2 at the same arrival."""
    if any(t not in per_run for t in K_RUNS):
        return None
    k2 = {c["case"]: c for c in per_run["k_r2"]}
    others: dict[int, dict[str, dict]] = {}
    for t in OTHERS:
        for c in per_run[t]:
            if c["by"] == E.RANKING and group_of(c["queues"]) == "deflection":
                others.setdefault(c["case"], {})[t] = {"won": c["decision"],
                                                       "lost": c["queues"][1],
                                                       "right": c["right"]}
    rows = []
    for idx in sorted(others):
        c = k2[idx]
        there = set(c["queues"])
        rows.append({"case": idx, "truth": c["truth"], "governing": c["governing"],
                     "others": others[idx],
                     "k_r2": {"by": c["by"], "queues": c["queues"], "decision": c["decision"],
                              "right": c["right"], "reported": c["reported"],
                              "rules": c["standing"]},
                     "winners_queue_stood": any(o["won"] in there for o in others[idx].values()),
                     "losers_queue_stood": any(o["lost"] in there for o in others[idx].values())})
    by = Counter(str(r["k_r2"]["by"]) for r in rows)
    one = [r for r in rows if r["k_r2"]["by"] == E.RUNG2]
    return {
        "cases": len(rows),
        "by": {k: by.get(k, 0) for k in (E.RANKING, E.RUNG2, "None")},
        "right": sum(r["k_r2"]["right"] for r in rows),
        "right_by": {k: sum(r["k_r2"]["right"] for r in rows if str(r["k_r2"]["by"]) == k)
                     for k in (E.RANKING, E.RUNG2, "None")},
        "one_queue_was": dict(sorted(Counter(r["k_r2"]["queues"][0] for r in one).items())),
        "one_queue_by_truth": dict(sorted(Counter(
            f"{r['k_r2']['queues'][0]} at {r['truth']}" for r in one).items())),
        "winners_queue_stood": sum(r["winners_queue_stood"] for r in rows),
        "losers_queue_stood": sum(r["losers_queue_stood"] for r in rows),
        "by_governing": tally([{"governing": r["governing"], "right": r["k_r2"]["right"]}
                               for r in rows], lambda c: c["governing"]),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# G-c: the rules that won the errors
# ---------------------------------------------------------------------------

def errors(cases: Sequence[dict], births: dict[str, dict]) -> dict[str, Any]:
    """One run's wrong decisions of the ranking, by group, with the winner's rules."""
    out = {}
    for g in GROUPS:
        mine = [c for c in cases if c["by"] == E.RANKING and not c["right"]
                and group_of(c["queues"]) == g]
        won = Counter(rid for c in mine for rid in c["standing"].get(c["decision"], []))
        out[g] = {
            "wrong": len(mine),
            "by_truth_and_decision": dict(sorted(Counter(
                f"{c['governing']}: {c['truth']} -> {c['decision']}" for c in mine).items())),
            "winner_rules": [dict(births[rid], wrong=n) for rid, n in ranked_by_cases(won)],
            "cases": [{"case": c["case"], "governing": c["governing"], "truth": c["truth"],
                       "decision": c["decision"], "queues": c["queues"],
                       "reported": c["reported"], "standing": c["standing"]} for c in mine],
        }
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    a = readings.get("behind") or {}
    b = readings.get("k_r2_at_the_others") or {}
    c = readings.get("errors") or {}

    def top(t):
        d = (a.get(t) or {}).get("deflection") or {}
        rules = d.get("rules") or []
        return d.get("cases", 0), (rules[0]["cases"] if rules else 0)

    g1 = all(t in a for t in OTHERS) and all(n > 0 and 2 * m > n for n, m in map(top, OTHERS))
    n = b.get("cases") or 0
    g2 = bool(n) and 2 * b["by"][E.RUNG2] > n
    g3 = bool(n) and 2 * b["right"] > n
    winners = (((c.get("k_r2") or {}).get("billing") or {}).get("winner_rules")) or []
    g4 = 0 < len(winners) <= WRONG_RULES_LINE
    g5 = bool(winners) and all(w["kind"] == plan.ERROR and w["report"] == w["queue"]
                               for w in winners)

    def out(clause, what, holds, reading):
        return {"clause": clause, "what": what, "reading": reading, "holds": bool(holds)}

    return [
        out("G1", "in K r1 and in K r3, one rule stands at more than half of the cases the "
                  "ranking took in the deflection group", g1,
            {t: dict(zip(("cases", "top_rule_stands_at"), top(t))) for t in OTHERS if t in a}),
        out("G2", "at more than half of the cases at which K r1's or K r3's ranking took a "
                  "conflict of the deflection group, K r2's engine decided the same arrival "
                  "by rung 2, with one queue standing", g2,
            None if not n else {"cases": n, "by": b["by"]}),
        out("G3", "at more than half of those cases, K r2's decision was right", g3,
            None if not n else {"cases": n, "right": b["right"]}),
        out("G4", "in K r2, at most three rules won the ranking's wrong decisions in billing's "
                  "layer", g4,
            {"rules": [w["rule_id"] for w in winners]}),
        out("G5", "each of those rules was born at a reported error whose report named its "
                  "queue", g5,
            {w["rule_id"]: {"kind": w["kind"], "report": w["report"], "queue": w["queue"]}
             for w in winners}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "conflicts.json"


def readings_path():
    return plan.OUT / "readings.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {t: json.loads(plan.run_path(RD.arm_of(t), RD.rep_of(t)).read_text())
               for t in K_RUNS if plan.run_path(RD.arm_of(t), RD.rep_of(t)).exists()}
    kept = json.loads(readings_path().read_text())
    return records, kept


def read_everything(records: dict[str, dict], kept: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    corpus = list(MI.corpus())
    a_cases = (kept.get("readings") or {}).get("A", {}).get("cases") or {}
    gates: list[dict[str, Any]] = []
    per_run, births = {}, {}
    for t in K_RUNS:
        if t not in records:
            continue
        per_run[t], logged = cases_of(records[t], space, corpus)
        births[t] = births_of(records[t], space, truth)
        gates.append({"gate": 1, "run": t, "what": "the ranking's cases are A's",
                      "passes": same_as_a(per_run[t], a_cases.get(t) or [])})
        gates.append({"gate": 2, "run": t, "what": "the replay is the engine's log",
                      "passes": logged})
        gates.append({"gate": 3, "run": t, "what": "a rule standing was born of its escalation",
                      "passes": born_of_its_escalation(per_run[t], births[t])})
    readings = {
        "behind": {t: {g: behind(per_run[t], births[t], g) for g in GROUPS} for t in per_run},
        "k_r2_at_the_others": at_the_others(per_run),
        "errors": {t: errors(per_run[t], births[t]) for t in per_run},
    }
    return readings, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Where K r2's conflicts fell, and which births "
                                             "made them (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/conflicts.py writes {record_path()}")
    records, kept = read_inputs()
    readings, gates = read_everything(records, kept)
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
        "source": {"readings": str(readings_path()),
                   "readings_from": kept["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in K_RUNS}},
        "surface": "the arrivals as each K run's engine decided them, with the rules undefeated "
                   "at each ticket when it arrived",
        "constants": {"groups": {"deflection": sorted(" / ".join(sorted(p)) for p in DEFLECTION),
                                 "billing": sorted(" / ".join(sorted(p)) for p in BILLING)},
                      "wrong_rules_line": WRONG_RULES_LINE},
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
