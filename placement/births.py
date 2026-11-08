"""
WHETHER THE CUT IS WHY THE LOOP'S BIRTHS ARE NARROW.
`PL-g` counts 70 of v1c's 213 births and 68 of v1b's 178 as their governing
rule's region. `placement/oncall.py` read the rarest queue's drafts, and found
11 of its 15 to be their governing rule's region cut by exactly the first lower
listed rule the ticket matches that a cut changes. `placement/provider.py` found
both providers making that cut. `FINDINGS_PLACEMENT.md` and `IDEAS.md` carry the
question: whether the loop's other narrow births are such cuts. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Every birth of this plan's six runs, set against the listed rule that governs
the ticket it was born at, `reasoned_loop/references.governing`'s, as `PL-g`
sets it. A birth's *part* is the points of the governing rule's region whose
true queue is the governing rule's. Each birth falls in exactly one class:
  wrong queue   its queue is not its ticket's;
  whole         it holds its part whole;
  cut by one    it does not, and it is the governing rule's region cut by one
                listed rule, `placement/oncall.py`'s `cut_by`;
  cut by two    neither, and it is that region cut by two listed rules the
                ticket matches;
  other         none of these.

For each birth it also reads the listed rules its ticket matches, the first of
them after the governing one that a cut would change, and the queue of the rule
it is cut by. The cutting rule read is the first in the list's order among those
that give the same cut.

**Beside them, reported**: the same reading of `PLAN_CHANNEL.md`'s six runs and
`PLAN_REASONED_LOOP.md`'s six, on Baidu, under v1b.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every birth's ticket is governed, by the list, by the rule the record's
     row names, and lies first in that rule's region;
  2. in every run of the three plans, the births and those that are their
     governing rule's region come back as that plan's Stage C counts them;
  3. the classes partition every run's births.

It refuses to write if any gate fails, and while the plan is unsigned, like every
writer of the package. `--dry-run` runs the gates, prints pass or fail, and
writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads this plan's six runs, the births of the right queue that do
not hold their part: *narrow births*. Each clause is read pooled over the runs
it names.

  N1. **Cuts are most of the narrow births where a cut is possible.** Of the
      narrow births at tickets that match a lower listed rule a cut would
      change, at least half are cut by one listed rule.
  N2. **In each arm.** N1's share is at least half in v1b's three runs, and in
      v1c's three.
  N3. **By the first a cut changes.** Of the births cut by one listed rule, at
      least three in four are cut by the first matched rule a cut changes.
  N4. **By another queue's rule.** Of the births cut by one listed rule, at
      least three in four are cut by a rule of another queue than theirs.

**The drafter's account.** The first call writes the governing rule's region
cut by the first lower listed rule the ticket matches that crosses it, so that
containment orders the birth above that rule without a declared side. The notes
at the rarest queue's tickets say so: *being a subset of both, it wins
automatically*. So where the ticket matches such a rule, the narrow birth is
mostly the cut. The rule it cuts by is one the ticket would otherwise go to, of
another queue.
- **Why it expects that.** 11 of the rarest queue's 15 drafts were such a cut,
  and both providers made it on the bridge.
- **The bet is N1.**
- **N2 is trusted least.** It needs both arms, and v1c's list changes what a
  first call meets only after the draft.
- **N4 is trusted most.** A cut by a rule of the birth's own queue would buy it
  nothing against a conflict.

**What the drafter had seen**:
- `FINDINGS_PLACEMENT.md` whole, `oncall.json` and `provider.json`: the rarest
  queue's drafts and the bridge's answers at its tickets;
- in `oncall.json`, the rules of other queues undefeated on that queue's lost
  points in v1c r3 and v1b r3, seventeen births, with their conditions and the
  governing rules of their tickets;
- each Stage C's births counts by run: the births, those that are a listed
  rule's region, and those that are their governing rule's;
- `reasoned_loop/score.py`'s `births_against_the_list`, and the field names of
  a record's rules and rows.

**What the drafter had not seen**: any other birth's extension or class, in any
run of the three plans.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-08, after `placement/provider.py`'s
reading. The expectation above was written and committed before the reading ran.
Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero
API calls.

Usage:  python3 -m placement.births --dry-run   # gates 1 to 3; writes nothing
        PYTHONHASHSEED=0 python3 -m placement.births
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from itertools import combinations
from typing import Any

from harness.provenance import describe, environment

from blind import rows as brows
from channel import plan as ch_plan
from manual import instrument as MI
from reasoned_loop import governed as gv
from reasoned_loop import plan as rl_plan
from reasoned_loop import references as rl_refs
from reuse import structure as st
from rung2.engine2 import Space

from . import oncall as PO
from . import plan

F = Fraction
CLASSES = ("wrong_queue", "whole", "cut_by_one", "cut_by_two", "other")

# The expectation's lines.
N_HALF = F(1, 2)
N_MOST = F(3, 4)

# The three plans' runs, and the key each one's Stage C keeps its runs under.
PLANS = {
    "placement": (plan, "PL-g"),
    "channel": (ch_plan, "CH-g"),
    "reasoned_loop": (rl_plan, "RL-h"),
}

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-08, after placement/provider.py's reading. "
    "The expectation in the module's docstring was written and committed before the "
    "reading ran. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "births.json"


def listed_queues() -> dict[str, str]:
    """Each listed rule's queue, by identifier."""
    return {r.id: r.queue for r in rl_refs.text_rules()}


# ---------------------------------------------------------------------------
# One birth
# ---------------------------------------------------------------------------

def cut_by_two(ext: int, gov: str, m: list[str], regions: dict[str, int]) -> list[list[str]]:
    """The pairs of matched rules, neither containing the governing rule's
    region, whose regions cut it to the birth exactly."""
    g = regions[gov]
    cands = [x for x in m if x != gov and g & regions[x] != g]
    return [[x, y] for x, y in combinations(cands, 2) if g & regions[x] & regions[y] == ext]


def classify(rule: dict, case, space: Space, regions: dict[str, int],
             truth: dict[str, int], queues: dict[str, str]) -> dict[str, Any]:
    """A birth against the listed rule that governs its ticket: the first the
    ticket matches, in the list's order, as `reasoned_loop/references.governing`
    finds it. Gate 1 holds the two to the record's row."""
    ext = brows.ext_of(rule, space)
    point = gv.point_of(case, space)
    m = PO.matched(point, regions)
    gov = m[0]
    queue = queues[gov]
    g = regions[gov]
    part = truth[queue] & g
    first = PO.first_cutting(m, gov, regions)
    one = two = None
    if rule["action"] != queue:
        cls = "wrong_queue"
    elif ext & part == part:
        cls = "whole"
    else:
        one = PO.cut_by(ext, gov, regions)
        if one:
            cls = "cut_by_one"
        else:
            two = cut_by_two(ext, gov, m, regions)
            cls = "cut_by_two" if two else "other"
    return {"rule_id": rule["rule_id"], "born_at": rule["born_at"], "action": rule["action"],
            "governing": gov, "governing_queue": queue, "class": cls,
            "is_the_region": ext == g, "covers_its_ticket": bool(ext & point),
            "points": ext.bit_count(), "part_points": part.bit_count(),
            "part_points_held": (ext & part).bit_count(),
            "matched": m, "first_cutting_match": first,
            "cut_by_one": one, "cut_by_two": two,
            "cut_by_the_first_cutting_match": bool(one) and first in one,
            "cutting_queue": queues[one[0]] if one else None}


def read_run(record: dict, space: Space, regions: dict[str, int], truth: dict[str, int],
             queues: dict[str, str], cases) -> list[dict[str, Any]]:
    return [classify(r, cases[r["born_at"]], space, regions, truth, queues)
            for r in sorted(record["rules"], key=lambda r: r["born_at"])]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def governed_as_the_record_says(record: dict, births: list[dict[str, Any]]) -> bool:
    """Gate 1: each birth's ticket is governed by the rule its row names, and lies
    first in that rule's region."""
    rows = {r["idx"]: r for r in record["records"]}
    return all(rows.get(b["born_at"], {}).get("truth_rule") == b["governing"]
               and b["matched"] and b["matched"][0] == b["governing"] for b in births)


def as_stage_c_counts(births: list[dict[str, Any]], counted: dict[str, Any]) -> bool:
    """Gate 2: the births, and those that are their governing rule's region."""
    return (len(births) == counted["rules"]
            and sum(b["is_the_region"] for b in births) == counted["the_governing_rules_region"])


def partition(births: list[dict[str, Any]], counts: dict[str, int]) -> bool:
    """Gate 3."""
    return (sum(counts.values()) == len(births)
            and all(b["class"] in CLASSES for b in births))


# ---------------------------------------------------------------------------
# Counts
# ---------------------------------------------------------------------------

def counts(births: list[dict[str, Any]]) -> dict[str, Any]:
    by = {c: sum(1 for b in births if b["class"] == c) for c in CLASSES}
    narrow = [b for b in births if b["class"] in ("cut_by_one", "cut_by_two", "other")]
    possible = [b for b in narrow if b["first_cutting_match"]]
    one = [b for b in births if b["class"] == "cut_by_one"]
    return {"births": len(births), "by_class": by, "narrow": len(narrow),
            "narrow_where_a_cut_is_possible": len(possible),
            "of_them_cut_by_one": sum(1 for b in possible if b["class"] == "cut_by_one"),
            "cut_by_one": len(one),
            "cut_by_the_first_cutting_match": sum(b["cut_by_the_first_cutting_match"]
                                                  for b in one),
            "cut_by_another_queue": sum(1 for b in one if b["cutting_queue"] != b["action"])}


def pooled(runs: dict[str, list[dict[str, Any]]], tags) -> dict[str, Any]:
    return counts([b for t in tags for b in runs[t]])


def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    arms = {a: [plan.tag(a, r) for r in range(1, plan.REPS + 1)] for a in plan.ARMS}
    every = [t for a in plan.ARMS for t in arms[a]]
    c = pooled(runs, every)
    per = {a: pooled(runs, arms[a]) for a in plan.ARMS}

    def cut_share(x):
        return share(x["of_them_cut_by_one"], x["narrow_where_a_cut_is_possible"])

    def at_least(x, line):
        return x is not None and x >= line

    first = share(c["cut_by_the_first_cutting_match"], c["cut_by_one"])
    other = share(c["cut_by_another_queue"], c["cut_by_one"])
    return [
        {"clause": "N1", "what": "of the narrow births where a cut is possible, at least "
                                 "half are cut by one listed rule",
         "reading": {"cut_by_one": c["of_them_cut_by_one"],
                     "of": c["narrow_where_a_cut_is_possible"], "share": frac(cut_share(c))},
         "holds": at_least(cut_share(c), N_HALF)},
        {"clause": "N2", "what": "N1's share is at least half in each arm",
         "reading": {a: {"cut_by_one": per[a]["of_them_cut_by_one"],
                         "of": per[a]["narrow_where_a_cut_is_possible"],
                         "share": frac(cut_share(per[a]))} for a in plan.ARMS},
         "holds": all(at_least(cut_share(per[a]), N_HALF) for a in plan.ARMS)},
        {"clause": "N3", "what": "of the births cut by one listed rule, at least three in "
                                 "four are cut by the first matched rule a cut changes",
         "reading": {"by_the_first": c["cut_by_the_first_cutting_match"],
                     "of": c["cut_by_one"], "share": frac(first)},
         "holds": at_least(first, N_MOST)},
        {"clause": "N4", "what": "of the births cut by one listed rule, at least three in "
                                 "four are cut by a rule of another queue",
         "reading": {"by_another_queue": c["cut_by_another_queue"], "of": c["cut_by_one"],
                     "share": frac(other)},
         "holds": at_least(other, N_MOST)},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict[str, dict]], dict[str, dict]]:
    records: dict[str, dict[str, dict]] = {}
    stage_c: dict[str, dict] = {}
    for name, (p, _) in PLANS.items():
        records[name] = {p.tag(arm, rep): json.loads(p.run_path(arm, rep).read_text())
                         for arm, rep in p.schedule()}
        stage_c[name] = json.loads(p.score_path().read_text())
    return records, stage_c


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether the cut is why the loop's births "
                                             "are narrow (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"placement/births.py writes {record_path()}")
    records, stage_c = read_all()
    space, cases = MI.space(), MI.corpus()
    regions, truth, queues = rl_refs.regions(), MI.space_truth(), listed_queues()
    runs: dict[str, dict[str, list[dict[str, Any]]]] = {}
    gates = []
    for name, (p, key) in PLANS.items():
        runs[name] = {}
        for t, rec in records[name].items():
            bs = read_run(rec, space, regions, truth, queues, cases)
            runs[name][t] = bs
            gates += [
                {"gate": 1, "plan": name, "run": t,
                 "what": "each birth's ticket is governed as the record's row says",
                 "passes": governed_as_the_record_says(rec, bs)},
                {"gate": 2, "plan": name, "run": t,
                 "what": "the births and those that are the governing rule's region are "
                         "Stage C's",
                 "passes": as_stage_c_counts(bs, stage_c[name][key]["runs"][t]["births"])},
                {"gate": 3, "plan": name, "run": t, "what": "the classes partition the births",
                 "passes": partition(bs, counts(bs)["by_class"])}]
    for g in gates:
        print(f"  gate {g['gate']} {g['plan']} {g['run']}: "
              f"{'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    expectation = read_expectation(runs["placement"])
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {name: {"score": str(p.score_path()),
                          "score_from": stage_c[name]["_env"].get("git_commit")}
                   for name, (p, _) in PLANS.items()},
        "surface": "the exhaustive space, 134,400 points, for each birth's extension",
        "constants": {"N_HALF": str(N_HALF), "N_MOST": str(N_MOST)},
        "gates": gates,
        "counts": {name: {"runs": {t: counts(bs) for t, bs in rs.items()},
                          "pooled": counts([b for bs in rs.values() for b in bs])}
                   for name, rs in runs.items()},
        "by_arm": {a: pooled(runs["placement"],
                             [plan.tag(a, r) for r in range(1, plan.REPS + 1)])
                   for a in plan.ARMS},
        "births": runs,
        "expectation": expectation,
    }), indent=2, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
