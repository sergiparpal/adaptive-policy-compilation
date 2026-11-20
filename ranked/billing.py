"""
WHY K r2'S BASE DECIDED `H11`'S TICKETS WRONG WITH ONE QUEUE STANDING.
`FINDINGS_RANKED.md`, *Two things the six readings left free*, G, found that K
r2's largest loss in billing's layer was `H11`'s tickets, billing at severity 3
or 4 with three prior tickets or more, which the policy sends to
`BILLING_SPECIALIST`: most of them were decided wrong with one queue standing,
which no conflict and no ranking met. Its *What it does not settle*, second
item, asks why. `IDEAS.md` carries it under *What `PLAN_RANKED.md` opens*.
Asked for by Sergi on 2026-11-20, with *Why the refusals fell where they did*,
which `ranked/refusals.py` reads. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The three K runs**, `results_ranked/loop_k_r{1,2,3}.json`: the rules in birth
order, every edge each birth tried, and every arrival with its truth, the
hidden rule that governs it and who decided it. **`conflicts.json`**, whose
count of `H11`'s arrivals decided wrong with one queue standing the gates hold
this reading to.

**A loss** is an arrival of `H11` that a K run's engine decided with one queue
standing, and wrong: the queue standing is not `BILLING_SPECIALIST`. Each is
read in the base the engine held when the case arrived.
- **The rules standing** there, of that one queue, with their births: the case
  each was born at, an impasse or a reported error and the queue its report
  named, and the hidden rule governing that ticket.
- **Billing's rules there**: the rules of `BILLING_SPECIALIST` that match the
  ticket. None stands. A loss is `none matched` when there is none; otherwise
  each is kept out by the rules that beat it and match the ticket, declared
  above it, nested in it, or both. The loss is `declared` when a declared edge
  keeps every one out, `containment` when only rules nested in them do, and
  `mixed` otherwise.
- **Who declared the edge.** Each declared edge that keeps a rule of billing
  out was installed at a birth, by the answer of the rule born there: the rule
  above, declaring a win, or billing's rule, declaring a loss. A `declared`
  loss is `by the rule above` when every such edge was declared at the birth of
  the rule above, `by billing's rule` when every one at billing's rule's, and
  `both` otherwise.
- **The policy's verdict** on each such edge, over the points both its rules
  match (`corrections/paths.py`'s `verdict`). A `declared` loss is `wrong` when
  every such edge is wrong.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **What took `H11`'s tickets.** In each K run, the losses by the queue
      standing, by the rules standing and their births, and by tenth of the
      arrivals.
  (b) **What kept billing's rules out.** The losses by class; the `declared`
      ones by who declared the edge and by the policy's verdict; and the
      declared edges that keep billing's rules out at the most losses, with
      their rules and births.
  (c) **Beside them**, K r1 and K r3 read the same way.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The losses are `conflicts.json`'s.** In each K run, the replay finds as
     many losses as that record's count of `H11`'s arrivals decided wrong with
     one queue standing, and at every case the record's log of who decided it
     is what the replay finds standing.
  2. **Billing stands at none.** At every loss, no rule of `BILLING_SPECIALIST`
     stands, one queue does, and each rule of billing that matches the ticket is
     beaten there by a rule that matches it.
  3. **Every declared edge is the log's.** Each declared edge that keeps a rule
     of billing out was installed at a birth whose rule is at one end of it, as
     the record's log has it.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  J1. **A billing rule matched.** In K r2, at more than half of the losses a
      rule of `BILLING_SPECIALIST` matched the ticket.
  J2. **A declaration kept it out.** In K r2, more than half of the losses where
      one matched are `declared`.
  J3. **Declared by the rule above.** In K r2, more than half of the `declared`
      losses are `by the rule above`.
  J4. **Wrong by the policy.** In K r2, more than half of the `declared` losses
      are `wrong`.
  J5. **K r1 and K r3 alike.** In K r1 and in K r3, more than half of the losses
      where a rule of `BILLING_SPECIALIST` matched are `declared`.

A clause that reads a missing value fails.

**The drafter's account.**
- **J1.** From case 110 on, K r2 held `R0046`, billing's whole product without
  the keyword, and later `R0102`, billing at severity 2 or more. Few of `H11`'s
  186 arrivals come before.
- **J2, the bet.** One queue stands, and it is not billing's, so something
  beats billing's rules at the ticket. Rules of other queues cross billing's:
  deflection's rules of free accounts at severity 3 or more, the general
  queue's of pro accounts at severity 4, the account manager's of business
  accounts with prior tickets. v1c's round asks a side of every crossing pair
  it lists, and the engine installs it. The drafter expects those sides, not
  rules nested in billing's, to keep billing's rules out.
- **J3.** A newborn of another queue declares itself above the rules its round
  lists: `R0089` above all 25, `R0124` above all 36. The drafter expects the
  wins of other queues' newborns, not billing's declared losses.
- **J4.** Over the space, the points such a rule shares with billing's are
  mostly `H11`'s: prior tickets run from 0 to 20, and `H12`'s are 0 to 2. So
  another queue above billing's rule there is wrong by the policy's verdict,
  whatever the arrivals say.
- **J5.** The mechanism is the loop's, not K r2's: K r1 lost 90 of `H11`'s
  arrivals so and K r3 59.

**The bet is J2.** **J1 and J4 are trusted most.** **J3 and J5 are trusted
least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole and `conflicts.json` whole: each K run's arrivals
  by the rule governing them and who decided them, the rules standing at every
  case of the ranking with their births, among them K r2's rules of billing's
  layer, and what kept the losing queue out of K r2 at the arrivals of the
  deflection conflicts;
- the hidden policy, the attributes' domains, `rung2/engine2.py`'s containment
  and `try_edge`, and `authorship/loop.py`'s order of installation.

**What the drafter had not seen**: any rule standing at a loss, which queue
stands at any, or what keeps billing's rules out at any.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/conflicts.py` and
`ranked/drafts.py`. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.billing --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.billing
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
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_OK, Space

from . import conflicts as CF
from . import engine as E
from . import plan
from . import reading as R
from . import readings as RD
from . import score as S

BILL = RD.BILL
RULE = "H11"
K_RUNS = RD.K_RUNS
NONE, DECLARED, CONTAINMENT, MIXED = "none matched", "declared", "containment", "mixed"
KEPT = (DECLARED, CONTAINMENT, MIXED, NONE)
ABOVE, BILLINGS, BOTH = "by the rule above", "by billing's rule", "both"
BY = (ABOVE, BILLINGS, BOTH)
TOP = 12
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/conflicts.py and "
    "ranked/drafts.py. The expectation in the module's docstring was written and committed "
    "before the reading ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


# ---------------------------------------------------------------------------
# Who installed each declared edge
# ---------------------------------------------------------------------------

def installers(record: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Every edge the log accepted, by the birth that first accepted it and the
    rule born there."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for idx in sorted(by_birth):
        for e in by_birth[idx]:
            if e.verdict == EDGE_OK and (e.winner, e.loser) not in out:
                out[(e.winner, e.loser)] = {"born_at": idx, "newborn": born[idx]["rule_id"]}
    return out


# ---------------------------------------------------------------------------
# The losses of one run
# ---------------------------------------------------------------------------

def kept_class(kinds: Sequence[str]) -> str:
    """A loss's class, from what keeps each matching rule of billing out."""
    if not kinds:
        return NONE
    if all(k in ("declared", "both") for k in kinds):
        return DECLARED
    if all(k == "containment" for k in kinds):
        return CONTAINMENT
    return MIXED


def by_class(sides: Sequence[str]) -> str | None:
    """Who declared every edge that keeps billing's rules out at a loss."""
    if not sides:
        return None
    if all(s == ABOVE for s in sides):
        return ABOVE
    if all(s == BILLINGS for s in sides):
        return BILLINGS
    return BOTH


def losses_of(record: dict[str, Any], space: Space, corpus: Sequence,
              installed: dict[tuple[str, str], dict[str, Any]], truth: dict[str, int]
              ) -> tuple[list[dict[str, Any]], bool, bool]:
    """Every loss of a run, read in the base the engine held when it arrived;
    and gates 1 and 2."""
    walk = R.Walk(record, space)
    rows, logs = record["records"], record["ranked"]["cases"]
    log_ok = len(rows) == len(logs) and all(r["idx"] == i for i, r in enumerate(rows))
    stand_ok = True
    out = []
    for row, logged in zip(rows, logs):
        idx = row["idx"]
        here = R.point_of(corpus[idx], space)
        eng = walk.engine
        standing = sorted(rid for rid, m in walk.und.items() if m & here)
        queues = sorted({walk.action[r] for r in standing})
        expected = E.RANKING if len(queues) > 1 else E.RUNG2 if queues else None
        log_ok &= logged["by"] == expected
        if (row["truth_rule"] == RULE and logged["by"] == E.RUNG2
                and S.engines_decision(row) != row["truth"]):
            bills = sorted(rid for rid, m in eng.ext.items()
                           if m & here and walk.action[rid] == BILL)
            kept = []
            for b in bills:
                beaters = sorted(x for x in eng.beats_me(b) if eng.ext[x] & here)
                declared = [x for x in beaters if x in eng.decl_below[b]]
                nested = [x for x in beaters if x in eng.sub_below[b]]
                stand_ok &= bool(beaters)
                kind = CF.defeat(eng, b, here)
                kept.append({"rule": b, "kind": kind, "declared": [
                    {"above": x, "above_queue": walk.action[x],
                     "installed_at": (installed.get((x, b)) or {}).get("born_at"),
                     "by": (ABOVE if (installed.get((x, b)) or {}).get("newborn") == x
                            else BILLINGS if (installed.get((x, b)) or {}).get("newborn") == b
                            else None),
                     "verdict": CP.verdict(eng, x, b, walk.action, truth)}
                    for x in declared], "nested": nested})
            stand_ok &= len(queues) == 1 and BILL not in queues
            out.append({"case": idx, "queue": queues[0] if queues else None,
                        "decision": S.engines_decision(row), "reported": row["cause"] == plan.ERROR,
                        "standing": standing, "billing": kept,
                        "class": kept_class([k["kind"] for k in kept])})
        if idx in walk.born:
            walk.birth(idx)
    return out, bool(log_ok), bool(stand_ok)


def declared_side(loss: dict[str, Any]) -> tuple[str | None, str | None]:
    """A declared loss's class by who declared, and its verdict."""
    edges = [d for k in loss["billing"] for d in k["declared"]]
    if loss["class"] != DECLARED or not edges:
        return None, None
    verdict = "wrong" if all(d["verdict"] == CP.WRONG for d in edges) else "not all wrong"
    return by_class([d["by"] for d in edges]), verdict


def read_run(losses: Sequence[dict], births: dict[str, dict]) -> dict[str, Any]:
    declared = [x for x in losses if x["class"] == DECLARED]
    sides = [declared_side(x) for x in declared]
    edge_counts: Counter = Counter()
    edge_rows: dict[tuple[str, str], dict] = {}
    for x in losses:
        for k in x["billing"]:
            for d in k["declared"]:
                key = (d["above"], k["rule"])
                edge_counts[key] += 1
                edge_rows[key] = {"above": d["above"], "above_queue": d["above_queue"],
                                  "below": k["rule"], "installed_at": d["installed_at"],
                                  "by": d["by"], "verdict": d["verdict"],
                                  "above_birth": births.get(d["above"]),
                                  "below_birth": births.get(k["rule"])}
    standing: Counter = Counter(r for x in losses for r in x["standing"])
    return {
        "losses": len(losses),
        "by_queue": dict(sorted(Counter(x["queue"] for x in losses).items())),
        "by_tenth": dict(sorted(Counter(str(x["case"] // (plan.N // 10)) for x in losses).items(),
                                key=lambda kv: int(kv[0]))),
        "matched": sum(1 for x in losses if x["class"] != NONE),
        "by_class": {k: sum(1 for x in losses if x["class"] == k) for k in KEPT},
        "declared_by": {k: sum(1 for s, _ in sides if s == k) for k in BY},
        "declared_wrong": sum(1 for _, v in sides if v == "wrong"),
        "standing_rules": [dict(births[r], losses=n) for r, n in
                           sorted(standing.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]],
        "edges": [dict(edge_rows[k], losses=n) for k, n in
                  sorted(edge_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]],
        "rows": list(losses),
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    k2 = runs.get("k_r2") or {}
    n, matched = k2.get("losses") or 0, k2.get("matched") or 0
    cls, by = k2.get("by_class") or {}, k2.get("declared_by") or {}
    declared = cls.get(DECLARED, 0)
    j1 = bool(n) and 2 * matched > n
    j2 = bool(matched) and 2 * declared > matched
    j3 = bool(declared) and 2 * by.get(ABOVE, 0) > declared
    j4 = bool(declared) and 2 * (k2.get("declared_wrong") or 0) > declared

    def declared_share(t):
        r = runs.get(t) or {}
        m = r.get("matched") or 0
        return bool(m) and 2 * (r.get("by_class") or {}).get(DECLARED, 0) > m

    j5 = all(t in runs for t in ("k_r1", "k_r3")) and all(declared_share(t)
                                                         for t in ("k_r1", "k_r3"))

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("J1", "in K r2, at more than half of the losses a rule of BILLING_SPECIALIST "
                  "matched the ticket", j1, {"losses": n, "matched": matched}),
        out("J2", "in K r2, more than half of the losses where one matched are declared", j2,
            {"matched": matched, "declared": declared}),
        out("J3", "in K r2, more than half of the declared losses are by the rule above", j3,
            {"declared": declared, "declared_by": by}),
        out("J4", "in K r2, more than half of the declared losses are wrong", j4,
            {"declared": declared, "wrong": k2.get("declared_wrong")}),
        out("J5", "in K r1 and in K r3, more than half of the losses where a rule of "
                  "BILLING_SPECIALIST matched are declared", j5,
            {t: {"matched": (runs.get(t) or {}).get("matched"),
                 "declared": ((runs.get(t) or {}).get("by_class") or {}).get(DECLARED)}
             for t in ("k_r1", "k_r3") if t in runs}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "billing.json"


def conflicts_path():
    return plan.OUT / "conflicts.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {t: json.loads(plan.run_path(RD.arm_of(t), RD.rep_of(t)).read_text())
               for t in K_RUNS if plan.run_path(RD.arm_of(t), RD.rep_of(t)).exists()}
    return records, json.loads(conflicts_path().read_text())


def read_everything(records: dict[str, dict], conflicts: dict[str, Any]
                    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    corpus = list(MI.corpus())
    by_rule = conflicts["readings"]["added"]["arrivals_by_rule"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in K_RUNS:
        if t not in records:
            continue
        installed = installers(records[t])
        losses, log_ok, stand_ok = losses_of(records[t], space, corpus, installed, truth)
        kept = (by_rule.get(t) or {}).get(RULE) or {}
        gates.append({"gate": 1, "run": t, "what": "the losses are conflicts.json's",
                      "passes": bool(log_ok and len(losses) == kept.get("rung2_wrong"))})
        gates.append({"gate": 2, "run": t, "what": "billing stands at none",
                      "passes": stand_ok})
        edges_ok = all(d["by"] is not None for x in losses for k in x["billing"]
                       for d in k["declared"])
        gates.append({"gate": 3, "run": t, "what": "every declared edge is the log's",
                      "passes": bool(edges_ok)})
        births = CF.births_of(records[t], space, truth)
        runs[t] = read_run(losses, births)
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why K r2's base decided H11's tickets wrong "
                                             "with one queue standing (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/billing.py writes {record_path()}")
    records, conflicts = read_inputs()
    readings, gates = read_everything(records, conflicts)
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
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in K_RUNS}},
        "surface": "the arrivals of H11 each K run's engine decided wrong with one queue "
                   "standing, read in the base it held then; the policy's verdict on a "
                   "declared edge over the points both its rules match",
        "constants": {"rule": RULE, "top": TOP},
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
