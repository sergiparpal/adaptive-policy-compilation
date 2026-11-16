"""
THE RANKING THE LOOP DECLARED, AS IT WENT.
`corrections/declared.py` gathered each L run's placement declarations, all of
them, after the run. They choose one ranking of the eight queues, and that
ranking orders the run's final rules above at once in L r2, and just below it
in L r1. A loop that ranked its base by its own declarations while it ran would
need no labels, no operator and no new question, and it is calls and a plan.
Before it is paid for, this reading replays each L run's births in their order,
and after every birth orders the base so far by the ranking the declarations so
far choose. Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/citations.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE REPLAY
--------------------------------------------------------------------------
The base after a birth is every rule born up to it, as the record bore them.
Its declarations are those of the answers born up to it, read as
`corrections/declared.py` reads them: one vote a citation of another queue's
rule, a citation a rule and side, whatever the engine did with it. Of the
40,320 rankings, the ones that agree with the most of those votes are chosen,
and the replay takes **the earliest of them** in `itertools.permutations(ACTIONS)`
order: a loop must take one, and that rule reads no truth. The base is ordered
by it under `corrections/hierarchy.py`'s pulled construction, and read over the
space by first match among the rules undefeated by containment, as rung 2's
engine decides an order that keeps containment.

**It is a replay, not the loop that would have run.** Its rules are the ones the
loop wrote. A loop that ranked as it went would have decided other cases on the
way, escalated others and written other rules, as `corrections/fall.py`'s and
`corrections/carry.py`'s replays say of theirs.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
For each L run:
- **the curve**: the points the replay decides right after every birth, beside
  the record's, as `fall.json` keeps it;
- **the checkpoints**: at 10, 20, 40, 80 and 160 labels and at all of them, the
  replay beside the loop's base and at once, as `score.json`'s `CR-g` keeps
  them;
- **the peak and the final**, the replay's and the record's;
- **the ranking**: how often it changes, the birth from which it puts
  `SECURITY_INCIDENT` first for good, and the birth from which it is the final
  ranking for good.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **The end is `declared.json`'s.** After the last birth the votes are its
     votes, pair by pair, the ranking chosen is its ranking, and the replay
     decides what it decides.
  3. **The record's curve is `fall.json`'s, and the checkpoints `score.json`'s.**
     At each checkpoint, the record's curve after the last birth up to the
     checkpoint's case gives the loop's share `score.json` keeps.
  4. **What the replay decides is the engine's.** At each checkpoint, the base
     installed in the replay's order into a fresh rung 2 engine, as `CR-d`
     installs an answer, closes no cycle. The engine and first match each decide
     what the replay reads.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 and 3 and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's runs, each apart. **The record's peak** is its curve's
highest point, as `fall.json` keeps it; a birth is counted by its place in the
curve, from 1.

  U1. **Security first, early.** In every L run, the replay's ranking puts
      `SECURITY_INCIDENT` first for good by the record's peak birth.
  U2. **Above the loop from its peak.** In every L run, at every birth from the
      record's peak on, the replay decides at least as much of the space as the
      record.
  U3. **No fall.** In every L run, the replay's final is within 0.02 of the
      space of its own peak.
  U4. **Above at once.** In L r2, at every checkpoint from 40 labels on, the
      replay decides more of the space than at once.
  U5. **Settled by the peak.** In every L run, the replay's ranking at the
      record's peak birth is its final ranking.
  U6. **The loop's best.** In every L run, the replay's peak is at least the
      record's.

A clause that reads a missing value fails.

**The drafter's account.**
- **Every newborn whose region crosses a security rule votes on it**, and
  nearly every vote goes its way: 11, 24 and 34 of more than a thousand went
  against it (`declared.json`). Once a security rule is born they pile up:
  U1, trusted most.
- **What the record lost after its peak was mostly `SECURITY_INCIDENT`'s
  region**, left in conflicts by right sides the engine refused
  (`corrections/fall.py`). The replay ranks that queue first and refuses
  nothing: U2 and U3.
- **At the end the declared ranking beats at once in L r2**, and at 40 and 80
  labels at once decided little there (Stage C's table). At 160 labels it
  decided more: U4, the bet, rests there.
- **The ranking's lower places rest on fewer votes**, between queues whose
  rules meet later: U5 is trusted least.
- **The record's own order decided most at its peak.** In L r2 that is more
  than the final ranking decides at the end. U6 bets a ranking reaches it.

**The bet is U4.** **U1 is trusted most.** **U5 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole: Stage C's table of the loop and at once at
  every checkpoint, *Why the loop's share of the space peaked and fell* with
  each run's peak and fall, and *The ranking the loop declared*;
- `fall.json`'s, `score.json`'s and `declared.json`'s figures;
- **the reading's size and cost**, timed before this was written, printing no
  share: the replay of L r1's 282 births took 3.2 seconds;
- **gates 1 and 3**, which pass on the dry run.

**What the drafter had not seen**: the replay's curve, its rankings, and what it
decides at any checkpoint.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/citations.py`. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.online --dry-run   # gates 1 and 3; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.online
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

from . import declared as DC
from . import fall as fl
from . import forgotten as fg
from . import hierarchy as H
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
SECURITY = H.SECURITY
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/citations.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

frac = fg.frac


# ---------------------------------------------------------------------------
# The votes, as the births come
# ---------------------------------------------------------------------------

def votes_of(record: dict[str, Any]) -> dict[str, Counter]:
    """Each born rule's votes, as `corrections/declared.py` reads them: one a
    citation of another queue's rule, a citation a rule and side."""
    out: dict[str, Counter] = {}
    queue = {r["rule_id"]: r["action"] for r in record["rules"]}
    for r in record["rules"]:
        v: Counter = Counter()
        for ref, side, _ in DC.citations(r):
            q = queue.get(ref)
            if q is None or q == r["action"]:
                continue
            v[(r["action"], q) if side == "beats" else (q, r["action"])] += 1
        out[r["rule_id"]] = v
    return out


class Agreement:
    """Every ranking's agreement with the votes so far, kept as votes come: a
    vote for `a` over `b` adds to every ranking that puts `a` above `b`."""

    def __init__(self, perms: Sequence[tuple[str, ...]]):
        self.perms = perms
        self.scores = [0] * len(perms)
        self.ahead: dict[tuple[str, str], list[int]] = {
            (a, b): [k for k, p in enumerate(perms) if p.index(a) < p.index(b)]
            for a in ACTIONS for b in ACTIONS if a != b}

    def add(self, v: Counter) -> None:
        for pair, n in v.items():
            for k in self.ahead[pair]:
                self.scores[k] += n

    def chosen(self) -> tuple[int, int, int]:
        """The earliest ranking of the most agreement, that agreement, and how
        many rankings share it."""
        top = max(self.scores)
        first = self.scores.index(top)
        return first, top, self.scores.count(top)


# ---------------------------------------------------------------------------
# The base so far, ordered and read
# ---------------------------------------------------------------------------

def prefix_rules(rs: H.Rules, ids: Sequence[str]) -> H.Rules:
    keep = frozenset(ids)
    return H.Rules(ids=list(ids), action={r: rs.action[r] for r in ids},
                   born={r: rs.born[r] for r in ids},
                   inside={r: rs.inside[r] & keep for r in ids},
                   around={r: rs.around[r] & keep for r in ids})


def right_of(order: Sequence[str], rs: H.Rules, ext: dict[str, int],
             truth: dict[str, int], n: int) -> int:
    """The points an order of the base decides right, by first match among the
    rules undefeated by containment: what rung 2's engine decides of an order
    that keeps containment."""
    remaining, right = (1 << n) - 1, 0
    for r in order:
        dom = 0
        for b in rs.inside[r]:
            dom |= ext[b]
        fires = ext[r] & ~dom & remaining
        if fires:
            right |= fires & truth.get(rs.action[r], 0)
            remaining &= ~fires
    return right.bit_count()


def replay(record: dict[str, Any], perms: Sequence[tuple[str, ...]], space: Space,
           truth: dict[str, int]) -> dict[str, Any]:
    """The run's births in order, the base after each ordered by the ranking its
    declarations so far choose."""
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    ext = engine.ext
    per_rule = votes_of(record)
    agree = Agreement(perms)
    so_far: Counter = Counter()
    curve, prefix = [], []
    for rid in rs.ids:
        prefix.append(rid)
        agree.add(per_rule.get(rid, Counter()))
        so_far.update(per_rule.get(rid, Counter()))
        k, top, ties = agree.chosen()
        sub = prefix_rules(rs, prefix)
        order = H.pulled(sub, H.rank_of(perms[k]))
        curve.append({"born_at": rs.born[rid][0], "rule_id": rid, "ranking": k, "agreeing": top,
                      "votes": sum(so_far.values()), "tied": ties,
                      "right": right_of(order, sub, ext, truth, space.n)})
    return {"curve": curve, "votes": so_far, "ids": list(rs.ids), "rules": rs, "engine": engine}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def fall_record() -> dict[str, Any]:
    return json.loads(fl.record_path().read_text())


def declared_record() -> dict[str, Any]:
    return json.loads(DC.record_path().read_text())


def at_case(curve: Sequence[dict[str, Any]], case: int) -> dict[str, Any] | None:
    """The curve's point after the last birth up to `case`."""
    before = [p for p in curve if p["born_at"] <= case]
    return before[-1] if before else None


def settled(curve: Sequence[dict[str, Any]], test) -> int | None:
    """The first birth, by its place in the curve from 1, from which `test` holds
    for good."""
    out = None
    for i, p in enumerate(curve, start=1):
        if test(p):
            out = i if out is None else out
        else:
            out = None
    return out


def read_run(tag: str, kept_fall: dict[str, Any], kept_declared: dict[str, Any],
             score: dict[str, Any]) -> dict[str, Any]:
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    perms = H.rankings()
    got = replay(record, perms, space, truth)
    curve, rs, engine = got["curve"], got["rules"], got["engine"]
    n = space.n
    rec_curve = kept_fall["runs"][tag]["curve"]
    final_rank = perms[curve[-1]["ranking"]]
    peak_at = max(range(len(curve)), key=lambda i: (curve[i]["right"], -i))
    rec_peak_at = max(range(len(rec_curve)), key=lambda i: (rec_curve[i]["right"], -i))
    checkpoints = []
    gate3 = len(rec_curve) == len(curve) and all(
        a["rule_id"] == b["rule_id"] for a, b in zip(rec_curve, curve))
    gate4 = True
    rules = {r.rule_id: r for r in engine.rules}
    for c in score["CR-g"]["curves"][tag]:
        mine, theirs = at_case(curve, c["case"]), at_case(rec_curve, c["case"])
        gate3 &= theirs is not None and F(theirs["right"], n) == F(c["loop"]["fraction"])
        k = curve.index(mine)
        ids = [p["rule_id"] for p in curve[:k + 1]]
        sub = prefix_rules(rs, ids)
        order = H.pulled(sub, H.rank_of(perms[mine["ranking"]]))
        eng = S.installed_in(order, {r: rules[r] for r in ids}, space)
        gate4 &= (all(why == EDGE_OK for _, _, why in eng.edge_log)
                  and MI.over_space(eng)["correct"] == mine["right"]
                  and MI.first_match_over_space([rules[r] for r in order])["correct"]
                  == mine["right"])
        at_once = c["at_once"].get("space")
        checkpoints.append({"labels": c["labels"], "case": c["case"],
                            "replay": frac(F(mine["right"], n)), "loop": c["loop"],
                            "at_once": at_once, "ranking": list(perms[mine["ranking"]])})
    kd = kept_declared["runs"][tag]
    want_votes = {tuple(x["pair"]): (x["for_first"], x["for_second"]) for x in kd["votes"]["all"]}
    have = got["votes"]
    gate2 = (all((have.get((a, b), 0), have.get((b, a), 0)) == v for (a, b), v in want_votes.items())
             and list(final_rank) == kd["every_declaration"]["orders"]["median"]["ranking"]
             and curve[-1]["right"] == kd["every_declaration"]["orders"]["median"]["right"])
    changes = sum(1 for a, b in zip(curve, curve[1:]) if a["ranking"] != b["ranking"])
    return {
        "births": len(curve),
        "curve": [{k: p[k] for k in ("born_at", "rule_id", "right", "ranking", "tied")}
                  for p in curve],
        "rankings": {str(k): list(perms[k]) for k in sorted({p["ranking"] for p in curve})},
        "replay": {"peak": {"birth": peak_at + 1, "born_at": curve[peak_at]["born_at"],
                            "share": frac(F(curve[peak_at]["right"], n))},
                   "final": frac(F(curve[-1]["right"], n))},
        "record": {"peak": {"birth": rec_peak_at + 1, "born_at": rec_curve[rec_peak_at]["born_at"],
                            "share": frac(F(rec_curve[rec_peak_at]["right"], n))},
                   "final": frac(F(rec_curve[-1]["right"], n))},
        "ranking": {"changes": changes,
                    "security_first_from": settled(curve, lambda p: perms[p["ranking"]][0] == SECURITY),
                    "final_from": settled(curve, lambda p: perms[p["ranking"]] == final_rank),
                    "final": list(final_rank)},
        "against_the_record": {
            "from_its_peak": all(curve[i]["right"] >= rec_curve[i]["right"]
                                 for i in range(rec_peak_at, len(curve))),
            "births_below_from_its_peak": sum(1 for i in range(rec_peak_at, len(curve))
                                              if curve[i]["right"] < rec_curve[i]["right"]),
            "ranking_at_its_peak": list(perms[curve[rec_peak_at]["ranking"]])},
        "checkpoints": checkpoints,
        "gates": [S.stage_c(tag),
                  {"gate": 2, "what": "the end is declared.json's", "passes": bool(gate2)},
                  {"gate": 3, "what": "the record's curve is fall.json's, and the checkpoints "
                                      "score.json's", "passes": bool(gate3)},
                  {"gate": 4, "what": "what the replay decides is the engine's",
                   "passes": bool(gate4)}],
    }


def gate_three(tag: str, kept_fall: dict[str, Any], score: dict[str, Any]) -> dict[str, Any]:
    """Gate 3 alone, for the dry run: it reads no replay."""
    n = MI.space().n
    rec_curve = kept_fall["runs"][tag]["curve"]
    ok = all(at_case(rec_curve, c["case"]) is not None
             and F(at_case(rec_curve, c["case"])["right"], n) == F(c["loop"]["fraction"])
             for c in score["CR-g"]["curves"][tag])
    return {"gate": 3, "what": "the record's curve is fall.json's, and the checkpoints "
                               "score.json's", "passes": bool(ok)}


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
        got[t] = {"security_first_from": r["ranking"]["security_first_from"],
                  "record_peak_birth": r["record"]["peak"]["birth"],
                  "above_from_its_peak": r["against_the_record"]["from_its_peak"],
                  "births_below": r["against_the_record"]["births_below_from_its_peak"],
                  "peak": value(r["replay"]["peak"]["share"]),
                  "final": value(r["replay"]["final"]),
                  "record_peak": value(r["record"]["peak"]["share"]),
                  "settled_by_the_peak": (r["against_the_record"]["ranking_at_its_peak"]
                                          == r["ranking"]["final"]),
                  "checkpoints": [(c["labels"], value(c["replay"]), value(c["at_once"]))
                                  for c in r["checkpoints"]]}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    u1 = each(lambda x: x["security_first_from"] is not None
              and x["security_first_from"] <= x["record_peak_birth"])
    u2 = each(lambda x: x["above_from_its_peak"])
    u3 = each(lambda x: x["peak"] is not None and x["final"] is not None
              and x["final"] >= x["peak"] - F(2, 100))
    l2 = [c for c in (got.get("l_r2") or {}).get("checkpoints", []) if c[0] >= 40]
    u4 = bool(l2) and all(rep is not None and ao is not None and rep > ao for _, rep, ao in l2)
    u5 = each(lambda x: x["settled_by_the_peak"])
    u6 = each(lambda x: x["peak"] is not None and x["record_peak"] is not None
              and x["peak"] >= x["record_peak"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "U1", "what": "in every L run, the replay's ranking puts SECURITY_INCIDENT first "
                                 "for good by the record's peak birth",
         "reading": shown(("security_first_from", "record_peak_birth")), "holds": u1},
        {"clause": "U2", "what": "in every L run, at every birth from the record's peak on, the "
                                 "replay decides at least as much of the space as the record",
         "reading": shown(("above_from_its_peak", "births_below")), "holds": u2},
        {"clause": "U3", "what": "in every L run, the replay's final is within 0.02 of the space "
                                 "of its own peak",
         "reading": shown(("peak", "final")), "holds": u3},
        {"clause": "U4", "what": "in L r2, at every checkpoint from 40 labels on, the replay decides "
                                 "more of the space than at once",
         "reading": [{"labels": lab, "replay": frac(rep) if rep is not None else None,
                      "at_once": frac(ao) if ao is not None else None} for lab, rep, ao in l2],
         "holds": u4},
        {"clause": "U5", "what": "in every L run, the replay's ranking at the record's peak birth is "
                                 "its final ranking",
         "reading": shown(("settled_by_the_peak",)), "holds": u5},
        {"clause": "U6", "what": "in every L run, the replay's peak is at least the record's",
         "reading": shown(("peak", "record_peak")), "holds": u6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "online.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="The ranking the loop declared, as it went "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 and 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/online.py writes {record_path()}")
    kept_fall, kept_declared = fall_record(), declared_record()
    score = json.loads(plan.score_path().read_text())
    if args.dry_run:
        ones = [{"run": t, **g} for t in L_RUNS for g in (S.stage_c(t), gate_three(t, kept_fall, score))]
        for g in ones:
            print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
                  f"  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    runs = {t: read_run(t, kept_fall, kept_declared, score) for t in L_RUNS}
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
        "source": {"fall": str(fl.record_path()),
                   "fall_from": kept_fall["_env"].get("git_commit"),
                   "declared": str(DC.record_path()),
                   "declared_from": kept_declared["_env"].get("git_commit"),
                   "score": str(plan.score_path()),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)}},
        "surface": "the whole space, 134,400 points: each L run's base after every birth, "
                   "ordered by the ranking its declarations so far choose, the earliest of "
                   "the most agreeing, under corrections/hierarchy.py's pulled construction",
        "constants": {"rankings": H.N_RANKINGS, "construction": "pulled",
                      "tie": "the earliest of the most agreeing, in itertools.permutations(ACTIONS)"},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        print(f"  {t}: replay peak {r['replay']['peak']['share']['value']:.4f} at birth "
              f"{r['replay']['peak']['birth']}, final {r['replay']['final']['value']:.4f}; "
              f"record peak {r['record']['peak']['share']['value']:.4f}, final "
              f"{r['record']['final']['value']:.4f}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
