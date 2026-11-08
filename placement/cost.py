"""
WHAT THE CUTS COST.
`placement/births.py` found the loop writing its narrow rules mostly as cuts:
where a cut is possible, about seven narrow births in ten are their governing
rule's region cut by one listed rule. v1c's bases decide 0.9510 to 0.9683 of the
space right. `FINDINGS_PLACEMENT.md` and `IDEAS.md` carry the question: how much
of what the bases still lose lies where the run drafted only cuts of the rule
that governs it. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For each run, every point of the space the final base does not decide right is
set against the listed rule that governs it: the first of the list whose region
holds it. Each governing rule is classed by the first-call drafts at the run's
escalations on tickets it governs. Each draft is classed as `placement/births.py`
classes a birth, born or not:
  no escalation     no ticket it governs escalated;
  whole born        some draft of the right queue that holds its part was born;
  whole not born    some such draft, and none of them born;
  cuts only         its right-queue drafts are all cuts, by one listed rule or by
                    two;
  narrow other      it has right-queue drafts, none whole, not all cuts;
  no right draft    every draft names another queue, or no rule.

The lost points are summed by class, by the governing rule's queue and by run.

**Beside them, reported**: the same reading of `PLAN_CHANNEL.md`'s six runs and
`PLAN_REASONED_LOOP.md`'s six, on Baidu, under v1b.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. each run's final base decides right exactly the points its plan's Stage C
     counts;
  2. the listed rules' regions, each less the earlier ones', partition the
     space;
  3. each escalation's ticket is governed as the record's row says.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads this plan's runs, over the space. *Lost* is a point a run's
final base does not decide right. K1 leaves out the points `H04` and `H05`
govern, the rarest queue's: from `FINDINGS_PLACEMENT.md`'s tables the drafter
could derive that they are most of what v1c's bases lose, and that their drafts
were cuts in every run but at case 257.

  K1. **The cuts' share, beyond the rarest queue.** Outside `H04`'s and `H05`'s
      points, at least half of what v1c's three bases lose lies under governing
      rules whose drafts were cuts only.
  K2. **A whole birth holds.** Under governing rules with a whole draft born,
      v1c's three bases lose at most a tenth of the points.
  K3. **A cut leaves the rest.** Under governing rules whose drafts were cuts
      only, v1c's three bases lose at least a fifth of the points.
  K4. **v1b's refusals.** Under governing rules with a whole draft and none
      born, v1b's three bases lose more points than v1c's three.

**The drafter's account.** What v1c's bases still lose is where the first call
never wrote the governing rule's region whole. v1c took away most of the
refusals (`PL-a`), so a whole draft is mostly born and decides its region. A
cut decides only its own points, and the rest of the part stays with rules of
other queues. Under v1b the round also refused whole drafts, and their regions
were lost too.
- **Why it expects that.** At the rarest queue's tickets every loss traced
  back to cuts, refused or born. Elsewhere about seven narrow births in ten are
  cuts.
- **The bet is K1.** It is the clause the drafter cannot derive.
- **K2 is trusted most.** A whole birth decides its region unless an edge or a
  narrower rule takes part of it.
- **K1 is trusted least.** Losses outside the rarest queue may lie under rules
  whose tickets never escalated, where no draft exists.

**What the drafter had seen**:
- `FINDINGS_PLACEMENT.md` whole, with each base's space and each queue's recall
  over the space;
- `oncall.json`, `provider.json` and `births.json`, with every birth's class, and
  from `births.json` the governing rules of the whole births and of the narrow
  births that are no cut, counted by rule;
- each Stage C's space by run.

**What the drafter had not seen**: any run's lost points by governing rule, or
the class of any draft that was not born, outside the rarest queue's tickets.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-08, after `placement/births.py`'s
reading. The expectation above was written and committed before the reading ran.
Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero
API calls.

Usage:  python3 -m placement.cost --dry-run   # gates 1 to 3; writes nothing
        PYTHONHASHSEED=0 python3 -m placement.cost
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
from reasoned_loop import governed as gv
from reasoned_loop import references as rl_refs
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space

from . import births as BI
from . import oncall as PO
from . import plan

F = Fraction
CLASSES = ("no_escalation", "whole_born", "whole_not_born", "cuts_only", "narrow_other",
           "no_right_draft")
RARE_RULES = ("H04", "H05")        # the rarest queue's two listed rules
POINTS = 134_400                   # the space

# The expectation's lines.
K_HALF = F(1, 2)
K_TENTH = F(1, 10)
K_FIFTH = F(1, 5)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-08, after placement/births.py's reading. "
    "The expectation in the module's docstring was written and committed before the "
    "reading ran. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "cost.json"


# ---------------------------------------------------------------------------
# The space, by governing rule, and what a base decides right
# ---------------------------------------------------------------------------

def governed_masks(regions: dict[str, int]) -> dict[str, int]:
    """Each listed rule's points: its region less every earlier rule's."""
    out, seen = {}, 0
    for x in sorted(regions):
        out[x] = regions[x] & ~seen
        seen |= regions[x]
    return out


def partitions(masks: dict[str, int], full: int) -> bool:
    """Gate 2."""
    union = 0
    for m in masks.values():
        union |= m
    return union == full and sum(m.bit_count() for m in masks.values()) == full.bit_count()


def right_mask(engine: PriorityEngine, truth: dict[str, int]) -> int:
    """The points a base decides right: one queue alone undefeated, and the
    truth's."""
    _, by_queue, _ = L.by_action(engine)
    out = 0
    for q, pts in L.decided_alone(by_queue).items():
        out |= pts & truth.get(q, 0)
    return out


# ---------------------------------------------------------------------------
# The drafts, and each governing rule's class
# ---------------------------------------------------------------------------

def draft_class(esc: dict, case, space: Space, regions: dict[str, int],
                truth: dict[str, int], queues: dict[str, str]) -> dict[str, Any]:
    """An escalation's first-call draft, classed as `placement/births.py` classes
    a birth, with its verdict. A draft naming no valid rule is `no_rule`."""
    payload = ((esc.get("calls") or [{}])[0].get("payload")) or {}
    m = PO.matched(gv.point_of(case, space), regions)
    base = {"idx": esc["idx"], "governing": m[0], "action": payload.get("action"),
            "verdict": esc.get("verdict"), "born": esc.get("verdict") == L.BORN}
    if not payload.get("conditions") or PO.draft_ext(payload, space) is None:
        return {**base, "class": "no_rule"}
    rule = {"rule_id": None, "born_at": esc["idx"], "action": payload.get("action"),
            "conditions": payload["conditions"]}
    return {**base, "class": BI.classify(rule, case, space, regions, truth, queues)["class"]}


def rule_class(drafts: list[dict[str, Any]]) -> str:
    """A governing rule's class in a run, by the drafts at its tickets."""
    if not drafts:
        return "no_escalation"
    right = [d for d in drafts if d["class"] not in ("wrong_queue", "no_rule")]
    if any(d["class"] == "whole" and d["born"] for d in right):
        return "whole_born"
    if any(d["class"] == "whole" for d in right):
        return "whole_not_born"
    if not right:
        return "no_right_draft"
    if all(d["class"] in ("cut_by_one", "cut_by_two") for d in right):
        return "cuts_only"
    return "narrow_other"


def read_run(record: dict, space: Space, regions: dict[str, int], masks: dict[str, int],
             truth: dict[str, int], queues: dict[str, str], cases) -> dict[str, Any]:
    right = right_mask(MI.final_engine(record), truth)
    drafts: dict[str, list[dict[str, Any]]] = {}
    for esc in record["escalations"]:
        d = draft_class(esc, cases[esc["idx"]], space, regions, truth, queues)
        drafts.setdefault(d["governing"], []).append(d)
    rules = {}
    for g in sorted(regions):
        ds = drafts.get(g, [])
        rules[g] = {"queue": queues[g], "points": masks[g].bit_count(),
                    "lost": (masks[g] & ~right).bit_count(), "class": rule_class(ds),
                    "drafts": ds}
    return {"right": right.bit_count(), "rules": rules}


def governed_as_the_record_says(record: dict, run: dict[str, Any]) -> bool:
    """Gate 3."""
    rows = {r["idx"]: r for r in record["records"]}
    return all(rows.get(d["idx"], {}).get("truth_rule") == g
               for g, r in run["rules"].items() for d in r["drafts"])


def as_stage_c(run: dict[str, Any], space_fraction: str) -> bool:
    """Gate 1."""
    return F(run["right"], POINTS) == F(space_fraction)


# ---------------------------------------------------------------------------
# Totals
# ---------------------------------------------------------------------------

def totals(runs: dict[str, dict[str, Any]], tags, leave_out=()) -> dict[str, Any]:
    """Points and lost points by class, over the given runs."""
    out = {c: {"points": 0, "lost": 0, "rules": 0} for c in CLASSES}
    for t in tags:
        for g, r in runs[t]["rules"].items():
            if g in leave_out:
                continue
            out[r["class"]]["points"] += r["points"]
            out[r["class"]]["lost"] += r["lost"]
            out[r["class"]]["rules"] += 1
    out["lost"] = sum(out[c]["lost"] for c in CLASSES)
    return out


def by_queue(runs: dict[str, dict[str, Any]], tags) -> dict[str, dict[str, int]]:
    """Lost points by the governing rule's queue and class, over the given runs."""
    out: dict[str, dict[str, int]] = {}
    for t in tags:
        for r in runs[t]["rules"].values():
            if r["lost"]:
                q = out.setdefault(r["queue"], {})
                q[r["class"]] = q.get(r["class"], 0) + r["lost"]
    return dict(sorted(out.items()))


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def arm_tags(arm: str) -> list[str]:
    return [plan.tag(arm, r) for r in range(1, plan.REPS + 1)]


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    c_out = totals(runs, arm_tags("v1c"), RARE_RULES)
    c_all = totals(runs, arm_tags("v1c"))
    b_all = totals(runs, arm_tags("v1b"))
    k1 = share(c_out["cuts_only"]["lost"], c_out["lost"])
    k2 = share(c_all["whole_born"]["lost"], c_all["whole_born"]["points"])
    k3 = share(c_all["cuts_only"]["lost"], c_all["cuts_only"]["points"])
    return [
        {"clause": "K1", "what": "outside H04's and H05's points, at least half of what "
                                 "v1c's bases lose lies under rules whose drafts were cuts "
                                 "only",
         "reading": {"lost_under_cuts_only": c_out["cuts_only"]["lost"],
                     "of": c_out["lost"], "share": frac(k1)},
         "holds": k1 is not None and k1 >= K_HALF},
        {"clause": "K2", "what": "under rules with a whole draft born, v1c's bases lose "
                                 "at most a tenth of the points",
         "reading": {"lost": c_all["whole_born"]["lost"],
                     "of": c_all["whole_born"]["points"], "share": frac(k2)},
         "holds": k2 is not None and k2 <= K_TENTH},
        {"clause": "K3", "what": "under rules whose drafts were cuts only, v1c's bases lose "
                                 "at least a fifth of the points",
         "reading": {"lost": c_all["cuts_only"]["lost"],
                     "of": c_all["cuts_only"]["points"], "share": frac(k3)},
         "holds": k3 is not None and k3 >= K_FIFTH},
        {"clause": "K4", "what": "under rules with a whole draft and none born, v1b's bases "
                                 "lose more points than v1c's",
         "reading": {"v1b": b_all["whole_not_born"]["lost"],
                     "v1c": c_all["whole_not_born"]["lost"]},
         "holds": b_all["whole_not_born"]["lost"] > c_all["whole_not_born"]["lost"]},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What the cuts cost (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"placement/cost.py writes {record_path()}")
    records, stage_c = BI.read_all()
    space, cases = MI.space(), MI.corpus()
    regions, truth, queues = rl_refs.regions(), MI.space_truth(), BI.listed_queues()
    masks = governed_masks(regions)
    runs: dict[str, dict[str, dict[str, Any]]] = {}
    gates = [{"gate": 2, "plan": None, "run": None,
              "what": "the listed rules' governed regions partition the space",
              "passes": partitions(masks, space.full)}]
    for name, (_, key) in BI.PLANS.items():
        runs[name] = {}
        for t, rec in records[name].items():
            r = read_run(rec, space, regions, masks, truth, queues, cases)
            runs[name][t] = r
            gates += [
                {"gate": 1, "plan": name, "run": t,
                 "what": "the final base decides right the points Stage C counts",
                 "passes": as_stage_c(r, stage_c[name][key]["runs"][t]["space"]["fraction"])},
                {"gate": 3, "plan": name, "run": t,
                 "what": "each escalation's ticket is governed as the record's row says",
                 "passes": governed_as_the_record_says(rec, r)}]
    for g in gates:
        where = f" {g['plan']} {g['run']}" if g["plan"] else ""
        print(f"  gate {g['gate']}{where}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs["placement"])
    summary = {}
    for name, rs in runs.items():
        tags = list(rs)
        summary[name] = {"runs": {t: totals(rs, [t]) for t in tags},
                         "pooled": totals(rs, tags),
                         "pooled_outside_the_rarest_queue": totals(rs, tags, RARE_RULES),
                         "lost_by_queue": by_queue(rs, tags)}
    summary["placement"]["by_arm"] = {a: {"all": totals(runs["placement"], arm_tags(a)),
                                          "outside_the_rarest_queue":
                                              totals(runs["placement"], arm_tags(a),
                                                     RARE_RULES),
                                          "lost_by_queue": by_queue(runs["placement"],
                                                                    arm_tags(a))}
                                      for a in plan.ARMS}
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {name: {"score": str(p.score_path()),
                          "score_from": stage_c[name]["_env"].get("git_commit")}
                   for name, (p, _) in BI.PLANS.items()},
        "surface": "the exhaustive space, 134,400 points",
        "constants": {"K_HALF": str(K_HALF), "K_TENTH": str(K_TENTH),
                      "K_FIFTH": str(K_FIFTH), "RARE_RULES": list(RARE_RULES)},
        "gates": gates,
        "summary": summary,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
