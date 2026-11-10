"""
WHY EVERY v1c BASE LOST A SIXTH OF `SECURITY_INCIDENT`.
Stage C found it. Each of this plan's three v1c bases decides 0.8750 of the
keyword half and recalls 0.8333 of the queue over the space: 8,400 of its 50,400
points are lost in every run. The loss lies under `H02` in v1c r1, and under `H01`
in v1c r2 and v1c r3. No first-call draft of the run held that rule's part.
`PLAN_PLACEMENT.md`'s v1c bases lost almost none of the queue, and v1d's at most
1,260 points. `FINDINGS_WHOLE.md`, *What Stage C does not settle*, item 2, and
`IDEAS.md` carry the question. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For each of this plan's six runs, and beside them `PLAN_PLACEMENT.md`'s three v1c
runs, reported:
- **`channel/lost.py`'s reading of the queue, called and not copied.** It
  gives each way a point is lost (impasse, conflict, unwritten, outranked), the
  rules of other queues undefeated on the lost points, the queue's own rules, the
  curve birth by birth, the queue's escalations by verdict, and what its
  unplaced answers left out.
- **The same ways, split by part.** The queue's points are `H01`'s part, the
  33,600 points `H01` governs, and `H02`'s part, the 16,800 points it governs
  below `H01`. Each part also gets its own curve, and the rules of the queue that
  hold the part whole.
- **Every first call on a ticket of the queue.** It is read with its governing
  rule, its class and breadth by `whole/references.py`, and its verdict. Beside
  them are what it cut its part by and the conditions it adds, by
  `placement/oncall.py`'s reading, called, and its note.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. to 4. `channel/lost.py`'s four, in every run read:
     1. the replay is the base, and the queue's right points are the run's
        Stage C's;
     2. the ways partition the loss;
     3. the curve ends at the base;
     4. the escalations are the record's.
  5. The two parts partition the queue's points.
  6. In every run, each part's ways partition the part's points.
  7. In this plan's runs, every first call's class and verdict are Stage C's.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Clauses S1 to S4 read this plan's three v1c runs, and S5 reads
`PLAN_PLACEMENT.md`'s. *The losing part* of a run is the part where it loses
the queue's points: `H02`'s in v1c r1, and `H01`'s in v1c r2 and v1c r3.

  S1. **Unwritten.** In each v1c run, every lost point of the queue is unwritten:
      another queue decides it, and no rule of the queue matches it.
  S2. **To the keyword's default.** In each v1c run, at least half of the lost
      points go to `T2_TECHNICAL`, `H03`'s queue.
  S3. **Born narrow.** In each v1c run, every first call of the queue's own on a
      ticket the losing part's rule governs ended with its rule born.
  S4. **Never compiled.** In each v1c run, after no birth did the base decide
      the whole of the losing part right.
  S5. **Held whole before.** In each of `PLAN_PLACEMENT.md`'s v1c runs, some
      rule of the queue in the final base holds `H01`'s part whole.

**The drafter's account.** In this period, v1c's first calls at the tickets of
`H01` and `H02` drew rules narrower than the governing region.
- **What they drew.** One tier of `H01`'s two, a severity, or the overlap with a
  lower listed rule. Each was born, and decides its own points.
- **What the rest went to.** No draft reached the rest of the part. It stays with
  the keyword's default: a broad rule of `T2_TECHNICAL`, written for `H03`'s
  tickets, which contains the part and decides it wrongly.
- **Why the channel did not mend it.** It reports a wrong decision only at a
  ticket, and only under its draw. The part's tickets that arrived after the
  default were either not reported, or reported and drafted narrow again.
- **Why v1d did not lose it.** Its first calls wrote `H01`'s region whole at the
  queue's tickets, and left nothing to the default.
- **The bet is S1.** If an edge pointed the wrong way, the lost points would be
  outranked instead, and S1 would fail while S2 held.
- **S2 is trusted most.** Each v1c base decides 0.8750 of the keyword half,
  which is the queue's points less the 8,400 lost, and all 16,800 of `H03`'s. So
  in each run a rule of `T2_TECHNICAL` decides the keyword's default.
- **S5 is trusted least.** A run can tile the queue with narrow rules and still
  recall it whole.

**What the drafter had seen**:
- `FINDINGS_WHOLE.md` whole, with `score.json`'s `WR-g`, which it tables.
  - For each run: what the final base lost under each listed rule, and that
    rule's class by what was drafted for it.
  - The drafts of the queue that held their part, by run.
  - The queue's escalations, drafts and verdicts by run.
  - The recall of the queue over the space and over the corpus.
- **The first POST-RUN reading**, `whole/oncall.py`, and its record. They read
  the tickets of `ONCALL_ESCALATION` and no ticket of this queue.
- `channel/lost.py` and its tests, and what `CLAUDE.md` and `STATUS.md` say of
  its reading of c r1.

**What the drafter had not seen**: any rule, draft, note or placement answer of
this queue in any run of either plan, any point's winner, any curve, and which
rule of another queue decides the lost points.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN: WHERE THE LOST POINTS LIE
--------------------------------------------------------------------------
The first run found the queue's rules narrow by a tier, a severity or a product.
The rest of the losing part went to a broad rule of `T2_TECHNICAL`, drafted at a
ticket of `H03`. So, for every run, this part reads the queue's lost points by
customer tier, by severity and by product. Then where they lie can be read off
the record, not worked out from the rules' conditions.

It was written after the five clauses above had been read: S1, S2, S4 and S5
hold, and S3 fails. It carries no expectation and moves no clause.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-10, after Stage C. The expectation
above was written and committed before the reading ran. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m whole.security --dry-run   # gates 1 to 7; writes nothing
        PYTHONHASHSEED=0 python3 -m whole.security
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from channel import lost as L
from manual import instrument as MI
from placement import oncall as PO
from placement import plan as pl_plan
from reasoned_loop import governed as gv
from reasoned_loop import references as rl_refs
from reuse import structure as st

from . import oncall as W
from . import plan, references

F = Fraction
QUEUE = "SECURITY_INCIDENT"
H01, H02 = "H01", "H02"
PARTS = (H01, H02)
DEFAULT_QUEUE = "T2_TECHNICAL"     # H03's, the keyword's default
S_HALF = F(1, 2)
V1C = tuple(plan.tag("v1c", k) for k in (1, 2, 3))
BESIDE = tuple(f"placement_v1c_r{k}" for k in (1, 2, 3))

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-10, after Stage C. The expectation in the "
    "module's docstring was written and committed before the reading ran. Not a signed row; "
    "no verdict moves.")
ADDED = (
    "Added after the first run, after its five clauses were read: each run's lost points of "
    "the queue by customer tier, by severity and by product. No expectation; no clause moves.")
BY = ("customer_tier", "severity", "product")


def record_path():
    return plan.OUT / "security.json"


def parts(truth: int, regions: dict[str, int]) -> dict[str, int]:
    """The queue's points each of its two listed rules governs."""
    return {H01: truth & regions[H01], H02: truth & regions[H02] & ~regions[H01]}


def partition_of(ps: dict[str, int], truth: int) -> bool:
    """Gate 2."""
    a, b = ps[H01], ps[H02]
    return not a & b and a | b == truth


def holding(engine, part: int) -> list[str]:
    """The rules of the queue whose extension holds the part whole."""
    return [r.rule_id for r in engine.rules
            if r.action == QUEUE and engine.ext[r.rule_id] & part == part]


def by_part(record: dict, engine, space, part: int) -> dict[str, Any]:
    """One part: its ways, its winners, the rules of the queue holding it whole,
    and its curve."""
    w = L.ways(engine, part, QUEUE)
    rep = L.replay(record, space, part, QUEUE)
    curve = rep["curve"]
    top = max(curve, key=lambda c: c["right"]) if curve else None
    return {"points": part.bit_count(), "ways": L.counts(w),
            "partitions": L.partitions(w, part),
            "winners": L.winners(engine, record, w),
            "holding_whole": holding(engine, part),
            "most_right": top["right"] if top else 0,
            "at_birth": top["born_at"] if top else None,
            "moves": [c for c in curve if c["delta"]]}


def first_calls(record: dict, stage_c: dict[int, dict] | None, space, regions: dict[str, int],
                cases: tuple, conds: dict[str, list[dict]]) -> list[dict[str, Any]]:
    """Every first call on a ticket of the queue."""
    rows = {r["idx"]: r for r in record["records"]}
    drafts = {d["idx"]: d for d in references.first_drafts(record)}
    out = []
    for esc in record["escalations"]:
        row = rows.get(esc["idx"], {})
        if row.get("truth") != QUEUE:
            continue
        gov = row.get("truth_rule")
        c0 = (esc.get("calls") or [{}])[0]
        payload = c0.get("payload") or {}
        d = PO.draft_ext(payload, space)
        m = PO.matched(gv.point_of(cases[esc["idx"]], space), regions)
        dr = drafts.get(esc["idx"], {})
        sc = (stage_c or {}).get(esc["idx"])
        out.append({
            "idx": esc["idx"], "governing": gov, "cause": row.get("cause"),
            "base_decided": row.get("engine_action"),
            "action": payload.get("action"), "conditions": payload.get("conditions"),
            "extra_conditions": W.extra_conditions(payload.get("conditions"),
                                                   conds.get(gov) or []),
            "class": dr.get("class"), "breadth": dr.get("breadth"),
            "verdict": esc.get("verdict"), "rule_id": esc.get("rule_id"),
            "first_cutting_match": PO.first_cutting(m, gov, regions),
            "cut_by": PO.cut_by(d, gov, regions),
            "note": payload.get("note"),
            "stage_c": None if sc is None else {"class": sc.get("class"),
                                               "verdict": sc.get("verdict")},
        })
    return out


def stage_c_agrees(calls: list[dict]) -> bool:
    """Gate 4, for this plan's runs."""
    return all(c["stage_c"] is not None and c["stage_c"]["class"] == c["class"]
               and c["stage_c"]["verdict"] == c["verdict"] for c in calls)


def read_one(record: dict, right: int, stage_c_drafts: list[dict] | None, space, truth: int,
             ps: dict[str, int], regions: dict[str, int], cases: tuple,
             conds: dict[str, list[dict]]) -> dict[str, Any]:
    final = MI.final_engine(record)
    run = L.read_run(record, space, truth, regions, right, QUEUE)
    split = {k: by_part(record, final, space, m) for k, m in ps.items()}
    sc = None if stage_c_drafts is None else {d["idx"]: d for d in stage_c_drafts}
    calls = first_calls(record, sc, space, regions, cases, conds)
    run["gates"] = run["gates"] + [
        {"gate": 6, "what": "each part's ways partition the part's points",
         "passes": all(s["partitions"] for s in split.values())}]
    if sc is not None:
        run["gates"].append({"gate": 7, "what": "every first call's class and verdict are "
                                                "Stage C's",
                             "passes": stage_c_agrees(calls)})
    run["parts"] = split
    run["first_calls"] = calls
    run["lost_by_value"] = by_value(L.ways(final, truth, QUEUE)["lost"], space)
    return run


def by_value(mask: int, space) -> dict[str, dict[str, int]]:
    """ADDED AFTER THE FIRST RUN. A mask's points by each value of `BY`'s
    attributes, the values it holds none of left out."""
    return {a: {str(v): (mask & m).bit_count() for v, m in space.mask[a].items() if mask & m}
            for a in BY}


def losing_part(run: dict[str, Any]) -> str:
    return max(PARTS, key=lambda k: run["parts"][k]["ways"]["lost"])


def expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    v1c = {t: runs[t] for t in V1C}
    beside = {t: runs[t] for t in BESIDE}

    def lost(r):
        return r["ways"]["lost"]

    def unwritten(r):
        return r["ways"]["unwritten"]

    def t2(r):
        return r["ways"]["lost_by_queue"].get(DEFAULT_QUEUE, 0)

    def own_calls(r):
        part = losing_part(r)
        return [c for c in r["first_calls"] if c["governing"] == part and c["action"] == QUEUE]

    return [
        {"clause": "S1", "what": "in each v1c run every lost point of the queue is unwritten",
         "reading": {t: {"unwritten": unwritten(r), "of": lost(r)} for t, r in v1c.items()},
         "holds": all(lost(r) > 0 and unwritten(r) == lost(r) for r in v1c.values())},
        {"clause": "S2", "what": "in each v1c run at least half of the lost points go to "
                                 "T2_TECHNICAL",
         "reading": {t: {"to_T2_TECHNICAL": t2(r), "of": lost(r)} for t, r in v1c.items()},
         "holds": all(lost(r) > 0 and F(t2(r), lost(r)) >= S_HALF for r in v1c.values())},
        {"clause": "S3", "what": "in each v1c run every first call of the queue's own on a "
                                 "ticket the losing part's rule governs ended born",
         "reading": {t: {"losing_part": losing_part(r),
                         "verdicts": [c["verdict"] for c in own_calls(r)]}
                     for t, r in v1c.items()},
         "holds": all(own_calls(r) and all(c["verdict"] == "nacida" for c in own_calls(r))
                      for r in v1c.values())},
        {"clause": "S4", "what": "in each v1c run after no birth did the base decide the whole "
                                 "of the losing part right",
         "reading": {t: {"losing_part": losing_part(r),
                         "most_right": r["parts"][losing_part(r)]["most_right"],
                         "of": r["parts"][losing_part(r)]["points"]} for t, r in v1c.items()},
         "holds": all(r["parts"][losing_part(r)]["most_right"]
                      < r["parts"][losing_part(r)]["points"] for r in v1c.values())},
        {"clause": "S5", "what": "in each of PLAN_PLACEMENT.md's v1c runs some rule of the "
                                 "queue in the final base holds H01's part whole",
         "reading": {t: r["parts"][H01]["holding_whole"] for t, r in beside.items()},
         "holds": all(r["parts"][H01]["holding_whole"] for r in beside.values())},
    ]


def read_all() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any]]:
    records = {plan.tag(arm, rep): json.loads(plan.run_path(arm, rep).read_text())
               for arm, rep in plan.schedule()}
    for k in (1, 2, 3):
        records[f"placement_v1c_r{k}"] = json.loads(pl_plan.run_path("v1c", k).read_text())
    return (records, json.loads(plan.score_path().read_text()),
            json.loads(pl_plan.score_path().read_text()))


def read_runs(records: dict[str, dict], stage_c: dict[str, Any],
              placement_c: dict[str, Any]) -> dict[str, dict[str, Any]]:
    space, regions, cases = MI.space(), rl_refs.regions(), MI.corpus()
    truth = MI.space_truth()[QUEUE]
    ps = parts(truth, regions)
    conds = {r.id: rl_refs.payload_of(r)["conditions"] for r in rl_refs.text_rules()}
    out = {}
    for t, rec in records.items():
        if t.startswith("placement_"):
            right = placement_c["PL-g"]["runs"][t.removeprefix("placement_")]["recall_space"][QUEUE][0]
            drafts = None
        else:
            right = stage_c["WR-g"]["runs"][t]["recall_space"][QUEUE][0]
            drafts = stage_c["WR-g"]["runs"][t]["first_drafts"]
        out[t] = read_one(rec, right, drafts, space, truth, ps, regions, cases, conds)
    out["_parts_partition"] = partition_of(ps, truth)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why every v1c base lost a sixth of "
                                             "SECURITY_INCIDENT (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 7 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"whole/security.py writes {record_path()}")
    records, stage_c, placement_c = read_all()
    runs = read_runs(records, stage_c, placement_c)
    parted = runs.pop("_parts_partition")
    checked = [{"run": "all", "gate": 5, "what": "the two parts partition the queue's points",
                "passes": parted}]
    checked += [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    clauses = expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "added_after_the_first_run": ADDED,
        "source": {"score": str(plan.score_path()),
                   "score_from": stage_c["_env"].get("git_commit"),
                   "beside": str(pl_plan.score_path())},
        "surface": "the exhaustive space, 134,400 points",
        "queue": QUEUE,
        "parts": {H01: "the queue's points H01 governs",
                  H02: "the queue's points H02 governs, below H01"},
        "runs_the_expectation_reads": {"S1-S4": list(V1C), "S5": list(BESIDE)},
        "constants": {"S_HALF": str(S_HALF), "DEFAULT_QUEUE": DEFAULT_QUEUE},
        "gates": checked,
        "runs": runs,
        "expectation": clauses,
    }), indent=2, default=str, ensure_ascii=False) + "\n")
    for c in clauses:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
