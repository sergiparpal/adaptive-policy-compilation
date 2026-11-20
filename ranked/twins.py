"""
ONE REGION UNDER TWO QUEUES. `FINDINGS_RANKED.md`, *Two things the last two
readings left free*, J, found that the edge at the most of K r2's losses of
`H11`'s tickets was `R0118` above `R0117`: billing at severity 4, the same region
written twice, as `SELF_SERVICE_DEFLECT`'s and as `BILLING_SPECIALIST`'s, at
consecutive cases. Its *What it does not settle*, third item, asks how often the
loop wrote one region as two queues' rules, and what the side declared between
them decided. `IDEAS.md` carries it under *What `PLAN_RANKED.md` opens*. Asked
for by Sergi on 2026-11-20. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`: the rules in birth
order, every edge each birth tried, every arrival with its truth, the hidden
rule that governs it and the engine's outcome. v1c records a draft that covers
exactly the tickets an earlier rule covers, in its first call's `copies` and the
escalation's `copy_of`, and lets it be born (`placement/protocol.py`).
**`score.json`**, whose bases the gates hold this reading to.

**A twin pair** is a born rule, the newborn `N`, and an earlier rule `E` of
another queue that covers exactly the same tickets, its **region**. A newborn
with an earlier rule of its own queue covering the same tickets is a **copy**,
counted beside. **The edge between them** is whatever `N`'s birth tried between
the two: the side its answer declared, `N` above or `E` above, and whether the
engine installed it or refused it. When no edge was tried, `E` was not listed,
and the first call's record says why.

**What the side decided**, read three ways:
- **the policy's verdict** on the side installed, over the region
  (`corrections/paths.py`'s `verdict`): `right`, `wrong` or `even`;
- **the run's final base**, as its own engine decides it, as Stage C reads it:
  the region's points decided by `N`'s queue, by `E`'s, by another queue, or
  left to no queue, and how many are right;
- **the arrivals** in the region after `N`'s birth, as the engine decided them:
  right, wrong, or left in conflict, and by which queue.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **How often.** In each run, the births, those that twin an earlier rule of
      another queue, the twin pairs, and the copies of the same queue.
  (b) **How the newborn was born.** Each twin's birth: an impasse or a reported
      error and the queue its report named, the hidden rule governing its ticket,
      and the rule that had decided that ticket; beside it, its twin's birth.
  (c) **The side between them.** The pairs by the edge's fate: `N` above,
      installed; `E` above, installed; refused; or not listed, and why.
  (d) **What it decided.** For each pair, the policy's verdict on the side
      installed, the region in the final base, and the arrivals in it after the
      newborn's birth.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The twins are the record's.** Every pair's newborn recorded its twin
     among its first call's `copies`, the escalation's `copy_of` is the first of
     them, and the two rules' conditions cover exactly the same points.
  2. **The bases are Stage C's.** Each run's final base, rebuilt birth by birth,
     decides on its own engine the share and the halves `score.json` keeps.
  3. **Every edge is the log's, at the newborn's birth.** The edges between a
     pair are paired with the births that tried them as the log and the rows
     have them, and each was tried at the newborn's birth.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  K1. **Born at reported errors.** In the six runs pooled, more than half of the
      births that twin an earlier rule of another queue were born at a reported
      error.
  K2. **Declared above its twin.** Of the twin pairs pooled, at more than half
      the newborn was declared above its twin and the engine installed the edge.
  K3. **The region flips.** Of the twin pairs pooled, at more than half the
      newborn's queue decides more of the region than its twin's, in the run's
      final base.
  K4. **Wrong by the policy.** Of the twin pairs whose edge was installed,
      pooled, at more than half the side installed is wrong by the policy's
      verdict over the region.
  K5. **Rare.** In every run, fewer than one birth in ten twins an earlier rule
      of another queue.

A clause that reads a missing value fails.

**The drafter's account.**
- **K5.** A twin of another queue needs a first call to draw exactly the region
  of an earlier rule, under another queue. That happens where the catalogue's
  line and the ticket's salient attributes coincide, as billing at severity 4
  did. Most births draw regions of their own.
- **K1.** Most escalations are reported errors, and a report that names another
  queue at a ticket inside an earlier rule's region invites that region again
  under the reported queue. `R0118` was born so, though the rule that had
  decided its ticket was not its twin but `R0059`, of `T1_GENERAL`.
- **K2.** A newborn's answer declares itself above the rules its round lists, as
  `R0089` did above 25 and `R0124` above 36, and `R0118` above `R0117`. A twin is
  listed, since neither contains the other, unless its region is wholly
  governed. The edge is refused only if the twin already reaches the newborn.
- **K3.** Installed above its twin, the newborn takes the region wherever no
  third rule beats it.
- **K4, the bet.** The region is drawn from one ticket, and spans the layers
  that share it, as `H11` and `H12` share billing's tickets and part on prior
  tickets. The newborn's queue is right for its ticket's layer, and over the
  space the other layer is often the larger: billing at severity 4 is mostly
  `H11`'s, and `R0118` put `SELF_SERVICE_DEFLECT` above it.

**The bet is K4.** **K1 and K5 are trusted most.** **K3 and K4 are trusted
least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole, and `billing.json`'s edges, among them `R0118`
  above `R0117`: their conditions, their births at cases 585 and 584, the side
  declared and its verdict;
- `R0118`'s escalation in K r2's record: its `copy_of`, its first call's
  `copies` and `left_out`, its 18 rules listed, and the rule that had decided
  its ticket; the outcomes and causes an L record keeps;
- `placement/protocol.py`'s handling of a copy, `authorship/protocol.py`'s
  `copies_of`, and `rung3/copy_births.py` with `FINDINGS3.md`'s §18 and §19
  headings on rung 1's copies.

**What the drafter had not seen**: any other twin or copy of the six runs, how
many there are, any edge between a pair but `R0118`'s, or what any region
holds in a final base or at the arrivals.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/refusals.py` and
`ranked/billing.py`. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.twins --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.twins
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
from rung2.engine2 import Condition, Space

from . import plan
from . import reading as R
from . import readings as RD
from . import score as S

RUNS = RD.RUNS
NEWBORN_ABOVE, TWIN_ABOVE = "newborn above", "twin above"
REFUSED, NOT_LISTED = "refused", "not listed"
FATES = (NEWBORN_ABOVE, TWIN_ABOVE, REFUSED, NOT_LISTED)
VERDICTS = (CP.RIGHT_VERDICT, CP.WRONG, CP.EVEN)
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/refusals.py and "
    "ranked/billing.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


def extension(space: Space, conditions: Sequence[dict]) -> int:
    return space.extension([Condition(**c) for c in conditions])


# ---------------------------------------------------------------------------
# (a), (b): the twins and the copies
# ---------------------------------------------------------------------------

def twins_of(record: dict[str, Any], space: Space) -> tuple[list[dict], dict[str, int], bool]:
    """Every twin pair of a run, the counts of (a), and gate 1."""
    rules = {d["rule_id"]: d for d in record["rules"]}
    ok = True
    pairs, births, twin_births, copy_births = [], 0, 0, 0
    for esc in record["escalations"]:
        if esc["verdict"] != "nacida":
            continue
        births += 1
        n = rules[esc["rule_id"]]
        copies = list((esc["calls"][0] or {}).get("copies") or [])
        ok &= esc.get("copy_of") == (copies[0] if copies else None)
        ext = extension(space, n["conditions"])
        other = [e for e in copies if rules[e]["action"] != n["action"]]
        twin_births += bool(other)
        copy_births += any(rules[e]["action"] == n["action"] for e in copies)
        for e in copies:
            ok &= extension(space, rules[e]["conditions"]) == ext
        for e in other:
            pairs.append({"newborn": n["rule_id"], "twin": e, "born_at": n["born_at"],
                          "twin_born_at": rules[e]["born_at"],
                          "queues": [n["action"], rules[e]["action"]],
                          "conditions": RD.conditions_of(n["conditions"]),
                          "twin_conditions": RD.conditions_of(rules[e]["conditions"]),
                          "points": ext.bit_count(),
                          "left_out": ((esc["calls"][0] or {}).get("left_out") or {}).get(e)})
    counts = {"births": births, "twin_births": twin_births, "pairs": len(pairs),
              "copy_births": copy_births}
    return pairs, counts, bool(ok)


def birth_of(record: dict[str, Any], idx: int) -> dict[str, Any]:
    """What bore a rule at a case: the escalation, its report, and the ticket."""
    row = record["records"][idx]
    esc = next(e for e in record["escalations"] if e["idx"] == idx)
    return {"case": idx, "kind": esc["kind"],
            "report": (record.get("reports_handed") or {}).get(str(idx)),
            "governing": row["truth_rule"], "truth": row["truth"],
            "decided_by": row.get("engine_rule"), "decided": row.get("engine_action")}


# ---------------------------------------------------------------------------
# (c): the side between them
# ---------------------------------------------------------------------------

def edge_fate(by_birth: dict[int, list], pair: dict[str, Any],
              installed: set[tuple[str, str]]) -> tuple[str, list[list[str]], bool]:
    """The edge between a pair, as the newborn's birth tried it; and gate 3."""
    n, e = pair["newborn"], pair["twin"]
    tried = [x for idx, es in by_birth.items() for x in es if {x.winner, x.loser} == {n, e}]
    at_birth = all(x.birth == pair["born_at"] for x in tried)
    log = [[x.winner, x.loser, x.verdict] for x in tried]
    if not tried:
        return NOT_LISTED, log, at_birth
    if any((x.winner, x.loser) in installed for x in tried):
        winner = next(x.winner for x in tried if (x.winner, x.loser) in installed)
        return (NEWBORN_ABOVE if winner == n else TWIN_ABOVE), log, at_birth
    return REFUSED, log, at_birth


# ---------------------------------------------------------------------------
# (d): what it decided
# ---------------------------------------------------------------------------

def decided_by_queue(base: dict[str, Any], region: int) -> dict[str, int]:
    """The region's points by the queue the base's own engine decides there:
    one queue standing; in arm K, at a conflict, the ranking's first."""
    queues = base["queues"]
    out: dict[str, int] = {}
    if base["own"] == "ranked":
        taken = 0
        for q in base["ranking"]:
            m = queues.get(q, 0) & region & ~taken
            if m:
                out[q] = m
            taken |= queues.get(q, 0) & region
        return out
    conflict = base["read"]["conflict"]
    for q, m in queues.items():
        got = m & region & ~conflict
        if got:
            out[q] = got
    return out


def region_reading(base: dict[str, Any], pair: dict[str, Any], region: int,
                   truth: dict[str, int]) -> dict[str, Any]:
    qn, qe = pair["queues"]
    by = decided_by_queue(base, region)
    decided = 0
    for m in by.values():
        decided |= m
    other = 0
    for q, m in by.items():
        if q not in (qn, qe):
            other |= m
    return {"points": region.bit_count(),
            "truth": {"newborn": (region & truth.get(qn, 0)).bit_count(),
                      "twin": (region & truth.get(qe, 0)).bit_count(),
                      "other": (region & ~truth.get(qn, 0) & ~truth.get(qe, 0)).bit_count()},
            "decided": {"newborn": by.get(qn, 0).bit_count(), "twin": by.get(qe, 0).bit_count(),
                        "other": other.bit_count(),
                        "no_queue": (region & ~decided).bit_count()},
            "right": (base["right"] & region).bit_count()}


def arrivals_in(record: dict[str, Any], pair: dict[str, Any], region: int, space: Space,
                corpus: Sequence) -> dict[str, Any]:
    """The arrivals in the region after the newborn's birth, as the engine
    decided them."""
    qn, qe = pair["queues"]
    out = Counter()
    for row in record["records"]:
        idx = row["idx"]
        if idx <= pair["born_at"] or not (R.point_of(corpus[idx], space) & region):
            continue
        out["arrivals"] += 1
        if row["outcome"] != "ACTION":
            out["left"] += 1
            continue
        d = S.engines_decision(row)
        out["right" if d == row["truth"] else "wrong"] += 1
        out["by_newborn" if d == qn else "by_twin" if d == qe else "by_other"] += 1
    return {k: out.get(k, 0) for k in ("arrivals", "right", "wrong", "left", "by_newborn",
                                       "by_twin", "by_other")}


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int], corpus: Sequence,
             base: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bool]]:
    pairs, counts, twins_ok = twins_of(record, space)
    by_birth = erb.edges_by_birth(record)
    eng = base["walk"].engine
    installed = {(w, l) for w, ls in eng.decl_above.items() for l in ls}
    action = {d["rule_id"]: d["action"] for d in record["rules"]}
    edges_ok = True
    rows = []
    for p in pairs:
        fate, log, at_birth = edge_fate(by_birth, p, installed)
        edges_ok &= at_birth
        region = extension(space, [dict(attr=a, op=o, value=v) for a, o, v in p["conditions"]])
        upper = p["newborn"] if fate == NEWBORN_ABOVE else p["twin"] if fate == TWIN_ABOVE \
            else None
        lower = p["twin"] if upper == p["newborn"] else p["newborn"] if upper else None
        rows.append(dict(p, fate=fate, log=log,
                         verdict=CP.verdict(eng, upper, lower, action, truth) if upper else None,
                         newborn_birth=birth_of(record, p["born_at"]),
                         twin_birth=birth_of(record, p["twin_born_at"]),
                         final=region_reading(base, p, region, truth),
                         arrivals=arrivals_in(record, p, region, space, corpus)))
    fates = Counter(r["fate"] for r in rows)
    verdicts = Counter(r["verdict"] for r in rows if r["verdict"])
    return ({**counts,
             "twin_births_at_a_report": len({r["newborn"] for r in rows
                                             if r["newborn_birth"]["kind"] == plan.ERROR}),
             "fates": {k: fates.get(k, 0) for k in FATES},
             "verdicts": {k: verdicts.get(k, 0) for k in VERDICTS},
             "flipped": sum(1 for r in rows
                            if r["final"]["decided"]["newborn"] > r["final"]["decided"]["twin"]),
             "pairs_list": rows},
            {"twins": twins_ok, "edges": bool(edges_ok)})


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    have = [runs[t] for t in RUNS if t in runs]
    complete = len(have) == len(RUNS)

    def total(key):
        return sum(r.get(key) or 0 for r in have)

    twin_births, pairs = total("twin_births"), total("pairs")
    at_report = total("twin_births_at_a_report")
    above = sum((r.get("fates") or {}).get(NEWBORN_ABOVE, 0) for r in have)
    installed = sum((r.get("fates") or {}).get(k, 0) for r in have
                    for k in (NEWBORN_ABOVE, TWIN_ABOVE))
    wrong = sum((r.get("verdicts") or {}).get(CP.WRONG, 0) for r in have)
    flipped = total("flipped")
    k1 = complete and bool(twin_births) and 2 * at_report > twin_births
    k2 = complete and bool(pairs) and 2 * above > pairs
    k3 = complete and bool(pairs) and 2 * flipped > pairs
    k4 = complete and bool(installed) and 2 * wrong > installed
    k5 = complete and all((r.get("births") or 0) > 0
                          and 10 * (r.get("twin_births") or 0) < r["births"] for r in have)

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    return [
        out("K1", "in the six runs pooled, more than half of the births that twin an earlier "
                  "rule of another queue were born at a reported error", k1,
            {"twin_births": twin_births, "at_a_report": at_report}),
        out("K2", "of the twin pairs pooled, at more than half the newborn was declared above its "
                  "twin and the engine installed the edge", k2,
            {"pairs": pairs, "newborn_above": above}),
        out("K3", "of the twin pairs pooled, at more than half the newborn's queue decides more "
                  "of the region than its twin's, in the run's final base", k3,
            {"pairs": pairs, "flipped": flipped}),
        out("K4", "of the twin pairs whose edge was installed, pooled, at more than half the side "
                  "installed is wrong by the policy's verdict over the region", k4,
            {"installed": installed, "wrong": wrong}),
        out("K5", "in every run, fewer than one birth in ten twins an earlier rule of another "
                  "queue", k5,
            {t: [runs[t].get("twin_births"), runs[t].get("births")] for t in RUNS if t in runs}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "twins.json"


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
        runs[t], ok = read_run(records[t], space, truth, corpus, base)
        gates.append({"gate": 1, "run": t, "what": "the twins are the record's",
                      "passes": ok["twins"]})
        gates.append({"gate": 3, "run": t, "what": "every edge is the log's, at the newborn's "
                                                   "birth", "passes": ok["edges"]})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="One region under two queues (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/twins.py writes {record_path()}")
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
                   "rule of another queue covers; its region read over the whole space of "
                   "134,400 points in the run's final base, on its own engine, and at the "
                   "arrivals after its birth",
        "constants": {"fates": list(FATES)},
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
