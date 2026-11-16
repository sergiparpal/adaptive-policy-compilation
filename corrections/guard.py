"""
THE RANKING AS IT WENT, AND A GUARD ON CONTAINMENT.
`corrections/online.py` replayed each L run's births, the base after each
ordered by the ranking its declarations so far choose. It kept what conflicts
cost the loop, and not what containment cost it. In L r2 and L r3 the replay
fell where a rule of another queue was born nested in a security rule, and the
nested rule took `SECURITY_INCIDENT`'s points by containment, which no ranking
undoes. This reading replays the same births with both levers: the same ranking,
and a guard that sets aside every rule strictly inside a rule of a queue the
ranking puts above its own. Proposed by the agent and asked for by Sergi on
2026-11-16, after `corrections/online.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE GUARD
--------------------------------------------------------------------------
After each birth, under the ranking the declarations so far choose, every rule
born so far that lies strictly inside a rule born so far of a queue ranked above
its own is **set aside**. It decides nothing while that holds. The rest are the
base, ordered under `corrections/hierarchy.py`'s pulled construction and read
over the space as `corrections/online.py` reads it. Containment is transitive,
so a rule inside one set aside is inside what set that one aside.

**Neither the guard nor the ranking reads the truth.** A loop could apply both:
re-rank after each birth, and set aside what the ranking says containment
reverses. The guard can cost. The policy sends part of the keyword's region to
`T2_TECHNICAL`: free clients at severity 3 or more. A rule of that queue written
for those tickets, nested in a security rule, is set aside with the rest.

**It is a replay, not the loop that would have run.** Its rules are the ones the
loop wrote, as `corrections/online.py` says of its own.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
For each L run:
- **the curve** with both levers after every birth, beside the ranking alone
  (`online.json`) and the record (`fall.json`);
- **the checkpoints**: at 10, 20, 40, 80 and 160 labels and at all of them,
  beside the ranking alone, the loop's base and at once (`score.json`'s
  `CR-g`);
- **the peak and the final**;
- **the guard at the end**: the rules it sets aside, by queue and the largest
  first; and the points the final base decides right with it and not without
  it, and the other way, by true queue;
- **the drops**: the five largest of the curve with both levers.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **Without the guard it is `online.json`'s replay.** At every birth the
     ranking alone decides the points `online.json`'s curve keeps.
  3. **The record's curve is `fall.json`'s, and the checkpoints `score.json`'s**,
     as `corrections/online.py`'s gate 3 reads them.
  4. **What the replay decides is the engine's.** At each checkpoint, the base
     the guard keeps, installed in the replay's order into a fresh rung 2 engine
     as `CR-d` installs an answer, closes no cycle. The engine and first match
     each decide what the replay reads.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 and 3 and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's runs, each apart. **At all labels** is the last
checkpoint, where at once and the ranking alone are as `score.json` and
`online.json` keep them.

  X1. **The guard catches what fell.** At the end, the guard sets aside `R0120`
      in L r2 and `R0104` in L r3.
  X2. **Above at once.** In every L run, at all labels, the replay with both
      levers decides more of the space than at once.
  X3. **No fall.** In every L run, its final is within 0.02 of the space of its
      own peak.
  X4. **Above the ranking alone.** In every L run, at all labels, it decides
      more of the space than the ranking alone.
  X5. **What the guard costs.** In every L run, the points the final base
      decides right without the guard and not with it are fewer than a quarter
      of those it decides right with it and not without it.
  X6. **The loop's best.** In every L run, its peak is at least the record's.

A clause that reads a missing value fails.

**The drafter's account.**
- **`R0120` and `R0104` are rules of `T2_TECHNICAL` strictly inside a security
  rule**: they hold `SECURITY_INCIDENT`'s points by containment (*Shape or
  order*, section 3). The final ranking puts that queue first in every run:
  X1, trusted most.
- **Containment held 8,400, 16,800 and 33,600 of `SECURITY_INCIDENT`'s points**
  from the loop's rules (*Shape or order*, section 3). Set aside, the rules
  that hold them leave those points to the security rules: X2, the bet, and X4.
  L r1 needs the least of it, since its ranking alone came within 0.0089 of at
  once.
- **The guard also sets aside rules right where they are**, the policy's part
  of the keyword's region for `T2_TECHNICAL` among them, and narrow rules of a
  lower queue inside broad rules of a higher one elsewhere: X5 is trusted
  least.
- **Without containment against the ranking, a later birth nested in a security
  rule takes nothing back**: X3. A later broad rule of a higher queue still
  sets aside what lay inside it.
- **In L r2 the record's peak, 0.7773, was above the ranking alone's, 0.7596**,
  and the guard gives back what containment took: X6.

**The bet is X2.** **X1 is trusted most.** **X5 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the sections *Shape or order* and *The
  ranking the loop declared, as it went* among it, and so `shape.json`'s,
  `online.json`'s, `fall.json`'s and `score.json`'s figures;
- the hidden policy's keyword rules: two of `SECURITY_INCIDENT`, and the rest of
  the region to `T2_TECHNICAL`;
- **the reading's size and cost**, timed before this was written, printing no
  share: the replay of L r1's 282 births with both levers took 2.1 seconds;
- **gates 1 and 3**, which pass on the dry run.

**What the drafter had not seen**: the curve with both levers, what the guard
sets aside, and what it gains or loses.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/online.py`. The expectation above was written and committed before
the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.guard --dry-run   # gates 1 and 3; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.guard
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Sequence

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_OK, Space

from . import forgotten as fg
from . import hierarchy as H
from . import online as ON
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
SECURITY = H.SECURITY
ASIDE_KEPT = 6                      # the rules set aside listed at the end, largest first
DROPS_KEPT = 5
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/online.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

frac = fg.frac


# ---------------------------------------------------------------------------
# The guard
# ---------------------------------------------------------------------------

def set_aside(rs: H.Rules, ids: Sequence[str], rank: dict[str, int]) -> set[str]:
    """The rules of `ids` strictly inside a rule of `ids` of a queue ranked above
    their own."""
    keep = set(ids)
    out = set()
    for r in ids:
        mine = rank[rs.action[r]]
        if any(rank[rs.action[x]] < mine for x in rs.around[r] & keep):
            out.add(r)
    return out


def right_mask(order: Sequence[str], rs: H.Rules, ext: dict[str, int],
               truth: dict[str, int], n: int) -> int:
    """The points an order of the base decides right, as a mask: what
    `corrections/online.py`'s `right_of` counts."""
    remaining, right = (1 << n) - 1, 0
    for r in order:
        dom = 0
        for b in rs.inside[r]:
            dom |= ext[b]
        fires = ext[r] & ~dom & remaining
        if fires:
            right |= fires & truth.get(rs.action[r], 0)
            remaining &= ~fires
    return right


def replay(record: dict[str, Any], perms: Sequence[tuple[str, ...]], space: Space,
           truth: dict[str, int]) -> dict[str, Any]:
    """The run's births in order: after each, the ranking its declarations so far
    choose, the base it orders alone, and the base the guard keeps."""
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    ext = engine.ext
    per_rule = ON.votes_of(record)
    agree = ON.Agreement(perms)
    curve, prefix = [], []
    for rid in rs.ids:
        prefix.append(rid)
        agree.add(per_rule.get(rid, Counter()))
        k, _, _ = agree.chosen()
        rank = H.rank_of(perms[k])
        alone = ON.prefix_rules(rs, prefix)
        aside = set_aside(rs, prefix, rank)
        kept = ON.prefix_rules(rs, [r for r in prefix if r not in aside])
        curve.append({
            "born_at": rs.born[rid][0], "rule_id": rid, "ranking": k,
            "alone": ON.right_of(H.pulled(alone, rank), alone, ext, truth, space.n),
            "right": ON.right_of(H.pulled(kept, rank), kept, ext, truth, space.n),
            "set_aside": len(aside)})
    return {"curve": curve, "rules": rs, "engine": engine}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def online_record() -> dict[str, Any]:
    return json.loads(ON.record_path().read_text())


def read_run(tag: str, kept_fall: dict[str, Any], kept_online: dict[str, Any],
             score: dict[str, Any]) -> dict[str, Any]:
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    n = space.n
    perms = H.rankings()
    got = replay(record, perms, space, truth)
    curve, rs, engine = got["curve"], got["rules"], got["engine"]
    rules = {r.rule_id: r for r in engine.rules}
    on_curve = kept_online["runs"][tag]["curve"]
    rec_curve = kept_fall["runs"][tag]["curve"]
    gate2 = (len(on_curve) == len(curve)
             and all(a["rule_id"] == b["rule_id"] and a["right"] == b["alone"]
                     for a, b in zip(on_curve, curve)))
    gate4 = True
    checkpoints = []
    for c, oc in zip(score["CR-g"]["curves"][tag], kept_online["runs"][tag]["checkpoints"]):
        mine = ON.at_case(curve, c["case"])
        k = curve.index(mine)
        ids = [p["rule_id"] for p in curve[:k + 1]]
        rank = H.rank_of(perms[mine["ranking"]])
        aside = set_aside(rs, ids, rank)
        sub = ON.prefix_rules(rs, [r for r in ids if r not in aside])
        order = H.pulled(sub, rank)
        eng = S.installed_in(order, {r: rules[r] for r in sub.ids}, space)
        gate4 &= (all(why == EDGE_OK for _, _, why in eng.edge_log)
                  and MI.over_space(eng)["correct"] == mine["right"]
                  and MI.first_match_over_space([rules[r] for r in order])["correct"]
                  == mine["right"])
        checkpoints.append({"labels": c["labels"], "case": c["case"],
                            "both": frac(F(mine["right"], n)), "ranking_alone": oc["replay"],
                            "loop": c["loop"], "at_once": c["at_once"].get("space"),
                            "set_aside": mine["set_aside"]})
    # the end
    final_rank = H.rank_of(perms[curve[-1]["ranking"]])
    alone = ON.prefix_rules(rs, rs.ids)
    aside = set_aside(rs, rs.ids, final_rank)
    kept = ON.prefix_rules(rs, [r for r in rs.ids if r not in aside])
    with_guard = right_mask(H.pulled(kept, final_rank), kept, engine.ext, truth, n)
    without = right_mask(H.pulled(alone, final_rank), alone, engine.ext, truth, n)
    gained, lost = with_guard & ~without, without & ~with_guard
    above = {r: sorted((x for x in rs.around[r] if final_rank[rs.action[x]] < final_rank[rs.action[r]]),
                       key=lambda x: rs.born[x])
             for r in aside}
    listed = sorted(aside, key=lambda r: (-engine.ext[r].bit_count(), rs.born[r]))
    peak_at = max(range(len(curve)), key=lambda i: (curve[i]["right"], -i))
    drops = sorted(((curve[i - 1]["right"] - curve[i]["right"], i + 1, curve[i]["rule_id"],
                     curve[i]["born_at"]) for i in range(1, len(curve))), reverse=True)[:DROPS_KEPT]
    return {
        "births": len(curve),
        "curve": [{k: p[k] for k in ("born_at", "rule_id", "right", "alone", "ranking", "set_aside")}
                  for p in curve],
        "both": {"peak": {"birth": peak_at + 1, "born_at": curve[peak_at]["born_at"],
                          "share": frac(F(curve[peak_at]["right"], n))},
                 "final": frac(F(curve[-1]["right"], n))},
        "ranking_alone": {"peak": kept_online["runs"][tag]["replay"]["peak"],
                          "final": kept_online["runs"][tag]["replay"]["final"]},
        "record": {"peak": kept_online["runs"][tag]["record"]["peak"],
                   "final": kept_online["runs"][tag]["record"]["final"]},
        "drops": [{"points": d, "birth": b, "rule_id": r, "born_at": at} for d, b, r, at in drops],
        "the_guard_at_the_end": {
            "set_aside": len(aside),
            "rules": sorted(aside, key=lambda r: rs.born[r]),
            "by_queue": dict(sorted(Counter(rs.action[r] for r in aside).items())),
            "largest": [{"rule": r, "action": rs.action[r], "born_at": rs.born[r][0],
                         "conditions": [[c.attr, c.op, c.value] for c in rules[r].conditions],
                         "points": engine.ext[r].bit_count(), "inside": above[r][:3]}
                        for r in listed[:ASIDE_KEPT]],
            "gained": {"points": gained.bit_count(),
                       "by_queue": {q: (gained & truth.get(q, 0)).bit_count() for q in ACTIONS
                                    if gained & truth.get(q, 0)}},
            "lost": {"points": lost.bit_count(),
                     "by_queue": {q: (lost & truth.get(q, 0)).bit_count() for q in ACTIONS
                                  if lost & truth.get(q, 0)}}},
        "checkpoints": checkpoints,
        "gates": [S.stage_c(tag),
                  {"gate": 2, "what": "without the guard it is online.json's replay",
                   "passes": bool(gate2)},
                  ON.gate_three(tag, kept_fall, score),
                  {"gate": 4, "what": "what the replay decides is the engine's",
                   "passes": bool(gate4)}],
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(x: dict[str, Any] | None) -> Fraction | None:
    return None if x is None else F(x["fraction"])


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    got: dict[str, dict[str, Any]] = {}
    for t in L_RUNS:
        r = runs.get(t)
        if r is None:
            continue
        last = r["checkpoints"][-1] if r["checkpoints"] else {}
        end = r["the_guard_at_the_end"]
        got[t] = {"set_aside": end["rules"],
                  "both": value(last.get("both")), "at_once": value(last.get("at_once")),
                  "ranking_alone": value(last.get("ranking_alone")),
                  "peak": value(r["both"]["peak"]["share"]), "final": value(r["both"]["final"]),
                  "record_peak": value(r["record"]["peak"]["share"]),
                  "gained": end["gained"]["points"], "lost": end["lost"]["points"]}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    def known(*keys):
        return lambda x: all(x[k] is not None for k in keys)

    x1 = ("R0120" in (got.get("l_r2") or {}).get("set_aside", [])
          and "R0104" in (got.get("l_r3") or {}).get("set_aside", []))
    x2 = each(lambda x: known("both", "at_once")(x) and x["both"] > x["at_once"])
    x3 = each(lambda x: known("peak", "final")(x) and x["final"] >= x["peak"] - F(2, 100))
    x4 = each(lambda x: known("both", "ranking_alone")(x) and x["both"] > x["ranking_alone"])
    x5 = each(lambda x: 4 * x["lost"] < x["gained"])
    x6 = each(lambda x: known("peak", "record_peak")(x) and x["peak"] >= x["record_peak"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "X1", "what": "at the end, the guard sets aside R0120 in L r2 and R0104 in L r3",
         "reading": {t: {"R0120": "R0120" in x["set_aside"], "R0104": "R0104" in x["set_aside"]}
                     for t, x in got.items() if t in ("l_r2", "l_r3")},
         "holds": x1},
        {"clause": "X2", "what": "in every L run, at all labels, the replay with both levers "
                                 "decides more of the space than at once",
         "reading": shown(("both", "at_once")), "holds": x2},
        {"clause": "X3", "what": "in every L run, its final is within 0.02 of the space of its own "
                                 "peak",
         "reading": shown(("peak", "final")), "holds": x3},
        {"clause": "X4", "what": "in every L run, at all labels, it decides more of the space than "
                                 "the ranking alone",
         "reading": shown(("both", "ranking_alone")), "holds": x4},
        {"clause": "X5", "what": "in every L run, the points the guard loses at the end are fewer "
                                 "than a quarter of those it gains",
         "reading": shown(("gained", "lost")), "holds": x5},
        {"clause": "X6", "what": "in every L run, its peak is at least the record's",
         "reading": shown(("peak", "record_peak")), "holds": x6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "guard.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="The ranking as it went, and a guard on "
                                             "containment (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 and 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/guard.py writes {record_path()}")
    kept_fall, kept_online = ON.fall_record(), online_record()
    score = json.loads(plan.score_path().read_text())
    if args.dry_run:
        ones = [{"run": t, **g} for t in L_RUNS
                for g in (S.stage_c(t), ON.gate_three(t, kept_fall, score))]
        for g in ones:
            print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
                  f"  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    runs = {t: read_run(t, kept_fall, kept_online, score) for t in L_RUNS}
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(runs)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"online": str(ON.record_path()),
                   "online_from": kept_online["_env"].get("git_commit"),
                   "fall": str(ON.fl.record_path()),
                   "score": str(plan.score_path()),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)}},
        "surface": "the whole space, 134,400 points: each L run's base after every birth, "
                   "ordered by the ranking its declarations so far choose, with every rule "
                   "strictly inside a rule of a queue ranked above its own set aside",
        "constants": {"rankings": H.N_RANKINGS, "construction": "pulled",
                      "tie": "the earliest of the most agreeing, in itertools.permutations(ACTIONS)",
                      "aside_kept": ASIDE_KEPT, "drops_kept": DROPS_KEPT},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        print(f"  {t}: both levers peak {r['both']['peak']['share']['value']:.4f}, final "
              f"{r['both']['final']['value']:.4f}; set aside at the end "
              f"{r['the_guard_at_the_end']['set_aside']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
