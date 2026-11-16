"""
WHETHER THE LOOP DECLARED THE RANKING IT LACKS.
`corrections/hierarchy.py` found that in L r1 and L r2 one ranking of the eight
queues orders the loop's own rules above at once, and that neither the run's
labels nor the model's stated rankings find it. This reading asks whether the
loop had declared it. At every birth, the placement round's answer declared the
newborn above or below rules of other queues, and the records keep every
declaration, those the engine refused among them. Gathered by pair of queues,
the declarations choose rankings, and those rankings order the loop's rules as
`corrections/hierarchy.py` orders them. If they reach the best ranking, the loop
knew the order and lost it installing its declarations one at a time. If they
do not, its preferences were wrong too. Proposed by the agent and asked for by
Sergi on 2026-11-16, after `corrections/hierarchy.py`. Free on the records.
POST-RUN.

--------------------------------------------------------------------------
THE DECLARATIONS
--------------------------------------------------------------------------
Each born rule's answer is read from its `beats`, `loses_to` and
`dropped_edges`, as `corrections/fall.py`'s `declared` reads them: each rule it
cited, the side it declared, and what the engine did with it. The engine
**installed** it, **refused** it for closing a cycle, or never ruled on it,
because the round had not shown that rule (**outside**). `declared` keeps one
citation a rule, and an answer can cite a rule on both sides, so this reading
keeps one citation a rule and side. A citation of a rule of the newborn's own
queue says nothing of a ranking, and is left out. Every other citation is one
vote: for the newborn's queue over the cited rule's where it declared itself
above, and the other way where below. A rule an answer cites twice on one side
is one vote.

--------------------------------------------------------------------------
THE RANKINGS THEY CHOOSE
--------------------------------------------------------------------------
A vote for one queue over another agrees with a ranking that puts the first
above the second. Every ranking of the eight queues, 40,320, is scored by the
votes it agrees with, and **the rankings the declarations choose** are those
that agree with the most. Pairs the votes leave even, or never meet, leave the
choice free, so the set is read whole, as `corrections/hierarchy.py` reads the
rankings the labels choose: its size, the places it gives `SECURITY_INCIDENT`,
and the least, the median and the most of the space its rankings decide. The
three are read as orders, each installed.

Each ranking orders the loop's final base under `corrections/hierarchy.py`'s
pulled construction: each rule as early as its queue's rank and containment
allow, the rules strictly inside it just before it.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
For each L run:
- **the votes**, by pair of queues, and by what the engine did with them;
- **the rankings every declaration chooses**, as above;
- **the rankings the installed declarations alone choose**: what the engine
  kept, gathered the same way;
- **the declarations against the best ranking**: of the votes, the share that
  agrees with `hierarchy.json`'s best ranking of the run, over all of them and
  by what the engine did.

Set beside each run's figures in `results_corrections/hierarchy.json`, the best
ranking, Stage C's, and the medians of the stated rankings and of those its
labels choose; and in `results_corrections/shape.json`, at once and the base
completed.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **The instances are `shape.json`'s**, as `corrections/hierarchy.py`'s gate
     2 reads them.
  3. **The declarations are the record's.** Every declaration the engine ruled
     on is in the run's `edge_log`, with the verdict read, and every edge of the
     log is one of them.
  4. **The orders are `hierarchy.json`'s.** The run's best ranking there, read
     on this reading's instance, decides what `hierarchy.json` keeps. Every
     ranking is scored once, 40,320.
  5. **Every order read installs.** It keeps containment, installs into a fresh
     rung 2 engine and closes no cycle, and the engine and first match each give
     it the share read. No ranking the declarations choose decides more than the
     rules' bound.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 to 3 and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's runs, each apart, and every ranking under pulled. In run
`r`, **at once** and **completed** are as `shape.json` keeps them, and **the
best ranking** and **the stated rankings** as `hierarchy.json` keeps them. **The
rankings its declarations choose** are those every declaration chooses.

  W1. **Security first.** In every L run, every ranking its declarations choose
      puts `SECURITY_INCIDENT` first.
  W2. **The loop knew the order.** In L r1 and in L r2, the rankings its
      declarations choose decide, at their median, more of the space than at
      once.
  W3. **Better than its base.** In every L run, they decide, at their median,
      more of the space than the loop's base completed.
  W4. **Mostly right.** In every L run, more than half of its votes agree with
      the best ranking.
  W5. **The refused were right.** In L r1 and in L r2, the votes the engine
      refused agree with the best ranking more often than those it installed.
  W6. **In context.** In every L run, the rankings its declarations choose
      decide, at their median, more of the space than the model's stated
      rankings at theirs.

A clause that reads a missing value fails.

**The drafter's account.**
- **The answers place the security rules as one block above their newborn**
  (`corrections/above.py`), and read a keyword rule of another queue as a
  security rule (`corrections/byqueue.py`). So most of the votes that meet
  `SECURITY_INCIDENT` go its way: W1, and W4 with them.
- **The engine refused right sides in the keyword half.** Where a born rule's
  wins already reached the rule it should lose to, the loss closed a cycle and
  was refused (`corrections/fall.py`, `corrections/paths.py`). Gathered into a
  ranking, every vote counts, refused or not: W5, and W3.
- **Gathered whole, the declarations carry the fact the best ranking turns
  on**: `SECURITY_INCIDENT` above every queue whose rules cross the keyword's.
  And each was written beside the rules it orders, where the stated rankings
  were given with the queues' names alone. So they may give what neither the
  labels nor the stated rankings gave: W2, the bet, and W6.
- **But some answers climb.** They put their newborn above every rule of their
  list, the security rules among them (`corrections/above.py`,
  `corrections/conditions.py`). Their votes could leave a pair with
  `SECURITY_INCIDENT` even, or turn it: W1 is trusted least.

**The bet is W2.** **W4 is trusted most.** **W1 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the sections *Shape or order* and *A
  ranking of the queues as the order* among it. So `shape.json`'s and
  `hierarchy.json`'s figures for each run: at once, the base completed, the best
  ranking, Stage C's, and the rankings stated and chosen by the labels;
- the readings of the answers' declarations, through their sections:
  `corrections/fall.py`, `paths.py`, `gateway.py`, `doors.py`, `byqueue.py`,
  `above.py` and `conditions.py`;
- **the record's form.** Each born rule keeps `beats`, `loses_to` and
  `dropped_edges`, which `corrections/fall.py`'s `declared` reads. L r1's edge
  log holds 5,405 edges installed and 1,849 refused. Gate 3, first written
  through `declared`, failed on L r1 and L r2. In each, one answer had cited a
  rule on both sides: above it, installed, and below it, refused for the cycle
  the first side had closed. `declared` kept the second. Read a citation a rule
  and side, the gate holds in all three runs;
- **the reading's size and cost**, timed before this was written, printing no
  vote, no ranking and no share. Reading the three runs' declarations took 0.3
  seconds, and scoring the 40,320 rankings against synthetic votes 0.1. One
  ranking's order took 0.7 ms on L r1's base;
- `corrections/hierarchy.py`, which this reading calls and does not edit.

**What the drafter had not seen**: any run's votes, the rankings they choose,
what those decide, or how the votes stand against the best ranking.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/hierarchy.py`. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.declared --dry-run   # gates 1 to 3; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.declared
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
from reasoned_loop import score as rl_score
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import fall as fl
from . import forgotten as fg
from . import hierarchy as H
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
SECURITY = H.SECURITY
INSTALLED, REFUSED, OUTSIDE = "installed", "refused", "outside"
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/hierarchy.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

median = rl_score.median
frac = fg.frac


# ---------------------------------------------------------------------------
# The declarations, as votes
# ---------------------------------------------------------------------------

def verdict_of(why: str) -> str:
    if why == EDGE_OK:
        return INSTALLED
    if why == EDGE_CYCLE:
        return REFUSED
    if why == fl.OUTSIDE:
        return OUTSIDE
    return why


def citations(rule: dict[str, Any]) -> list[tuple[str, str, str]]:
    """`(rule cited, side, verdict)` for a born rule's answer, read from its
    `beats`, `loses_to` and `dropped_edges` as `corrections/fall.py`'s
    `declared` reads them, but one a rule and side: `declared` keeps one a rule,
    and an answer can cite a rule on both sides. On one rule and side,
    `dropped_edges` wins, as in `declared`."""
    out: dict[tuple[str, str], str] = {}
    for ref in rule.get("beats") or []:
        out[(ref, "beats")] = EDGE_OK
    for ref in rule.get("loses_to") or []:
        out[(ref, "loses_to")] = EDGE_OK
    for x in rule.get("dropped_edges") or []:
        parts = x.split(":")
        out[(parts[1], parts[0])] = parts[2] if len(parts) > 2 else fl.OUTSIDE
    return [(ref, side, why) for (ref, side), why in out.items()]


def declarations(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Every citation of every born rule's answer, in birth order: the newborn,
    the rule it cited, the side, the engine's verdict, and the two queues."""
    rules = {r["rule_id"]: r for r in record["rules"]}
    out = []
    for r in sorted(record["rules"], key=lambda x: (x["born_at"], x["rule_id"])):
        for ref, side, why in citations(r):
            x = rules.get(ref)
            out.append({"rule": r["rule_id"], "ref": ref, "side": side, "why": why,
                        "verdict": verdict_of(why), "queue": r["action"],
                        "ref_queue": None if x is None else x["action"]})
    return out


def votes(decls: Sequence[dict[str, Any]], verdicts: Sequence[str] | None = None
          ) -> Counter:
    """`(a, b)` counts the declarations for queue `a` over queue `b`; those
    between two rules of one queue, or citing a rule the record does not hold,
    say nothing of a ranking."""
    out: Counter = Counter()
    for d in decls:
        if d["ref_queue"] is None or d["ref_queue"] == d["queue"]:
            continue
        if verdicts is not None and d["verdict"] not in verdicts:
            continue
        a, b = ((d["queue"], d["ref_queue"]) if d["side"] == "beats"
                else (d["ref_queue"], d["queue"]))
        out[(a, b)] += 1
    return out


def agreement(v: Counter, ranking: Sequence[str]) -> int:
    """The votes a ranking agrees with."""
    rank = H.rank_of(ranking)
    return sum(n for (a, b), n in v.items() if rank[a] < rank[b])


def chosen(v: Counter, perms: Sequence[tuple[str, ...]]) -> tuple[int, list[int]]:
    """The rankings that agree with the most votes, by index."""
    scores = [agreement(v, p) for p in perms]
    top = max(scores) if scores else 0
    return top, [k for k, s in enumerate(scores) if s == top]


def edge_log_matches(record: dict[str, Any], decls: Sequence[dict[str, Any]]) -> bool:
    """Gate 3: every declaration the engine ruled on is in the run's edge log,
    with its verdict, and every edge of the log is one of them."""
    ruled = {((d["rule"], d["ref"]) if d["side"] == "beats" else (d["ref"], d["rule"]))
             + (d["why"],) for d in decls if d["verdict"] != OUTSIDE}
    return ruled == {tuple(e) for e in record.get("edge_log") or []}


def by_pair(v: Counter) -> list[dict[str, Any]]:
    """The votes by unordered pair of queues, in the domain's order."""
    out = []
    for i, a in enumerate(ACTIONS):
        for b in ACTIONS[i + 1:]:
            out.append({"pair": [a, b], "for_first": v.get((a, b), 0),
                        "for_second": v.get((b, a), 0)})
    return out


# ---------------------------------------------------------------------------
# What the chosen rankings decide
# ---------------------------------------------------------------------------

def read_chosen(rs: H.Rules, inst: S.Instance, rules, perms: Sequence[tuple[str, ...]],
                v: Counter, space: Space, truth: dict[str, int]) -> tuple[dict[str, Any], bool]:
    """The rankings the votes `v` choose, read whole: their size, the places
    they give `SECURITY_INCIDENT`, the pairs they leave free, the least, median
    and most of the space they decide, and those three read as orders, each
    installed. Also whether none decides more than the bound."""
    top, ks = chosen(v, perms)
    right = {k: inst.score(inst.searched(H.pulled(rs, H.rank_of(perms[k])))) for k in ks}
    vals = sorted((right[k], k) for k in ks)
    picks = {"least": vals[0][1], "median": vals[(len(vals) - 1) // 2][1], "most": vals[-1][1]}
    ok = max(right.values()) <= S.coverage(inst)
    reads = {}
    for name, k in picks.items():
        row, good = H.read_order(rs, inst, perms[k], "pulled", rules, space, truth)
        ok &= good
        reads[name] = {**row, "index": k}
    free = [[a, b] for i, a in enumerate(ACTIONS) for b in ACTIONS[i + 1:]
            if len({(perms[k].index(a) < perms[k].index(b)) for k in ks}) > 1]
    return {"votes": sum(v.values()), "agreeing": top, "rankings": len(ks),
            "shares": H.spread([r for r, _ in vals], space.n),
            "security_first": sum(perms[k][0] == SECURITY for k in ks),
            "by_place_of_security": {str(p): sum(perms[k].index(SECURITY) + 1 == p for k in ks)
                                     for p in range(1, 9)},
            "pairs_left_free": free,
            "orders": reads}, bool(ok)


def against_best(decls: Sequence[dict[str, Any]], best: Sequence[str]) -> dict[str, Any]:
    """Of the votes, those that agree with the run's best ranking: over all, and
    by what the engine did."""
    out = {}
    for name, verdicts in (("all", None), (INSTALLED, (INSTALLED,)), (REFUSED, (REFUSED,)),
                           (OUTSIDE, (OUTSIDE,))):
        v = votes(decls, verdicts)
        n = sum(v.values())
        out[name] = {"votes": n, "agreeing": agreement(v, best),
                     "share": frac(F(agreement(v, best), n)) if n else None}
    return out


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def hierarchy_record() -> dict[str, Any]:
    return json.loads(H.record_path().read_text())


def read_run(tag: str, kept: dict[str, Any]) -> dict[str, Any]:
    """One L run: its declarations, the rankings they choose, and gates 1 to 5."""
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    perms = H.rankings()
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    rules = {r.rule_id: r for r in engine.rules}
    inst = S.instance(engine.rules, engine.ext, rs.inside, rs.around, truth, space.n)
    decls = declarations(record)
    every = votes(decls)
    held = votes(decls, (INSTALLED,))
    best = kept["runs"][tag]["loop"]["pulled"]["best"]
    best_right = inst.score(inst.searched(H.pulled(rs, H.rank_of(best["ranking"]))))
    all_read, ok_all = read_chosen(rs, inst, rules, perms, every, space, truth)
    held_read, ok_held = read_chosen(rs, inst, rules, perms, held, space, truth)
    counts = Counter(d["verdict"] for d in decls)
    same = sum(1 for d in decls if d["ref_queue"] == d["queue"])
    gates = [S.stage_c(tag), H.gate_two(tag),
             {"gate": 3, "what": "the declarations are the record's",
              "passes": edge_log_matches(record, decls)},
             {"gate": 4, "what": "the orders are hierarchy.json's",
              "passes": best_right == best["right"] and len(perms) == H.N_RANKINGS},
             {"gate": 5, "what": "every order read installs, and the bound bounds",
              "passes": ok_all and ok_held}]
    return {"declarations": {"of": len(decls), "by_verdict": dict(sorted(counts.items())),
                             "within_a_queue": same,
                             "unknown_rule": sum(1 for d in decls if d["ref_queue"] is None)},
            "votes": {"all": by_pair(every), INSTALLED: by_pair(held)},
            "every_declaration": all_read,
            "installed_alone": held_read,
            "against_best": {"best": list(best["ranking"]), **against_best(decls, best["ranking"])},
            "gates": gates}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(x: dict[str, Any] | None) -> Fraction | None:
    return None if x is None else F(x["fraction"])


def read_expectation(runs: dict[str, dict[str, Any]], kept: dict[str, Any],
                     shape: dict[str, Any]) -> list[dict[str, Any]]:
    got: dict[str, dict[str, Any]] = {}
    for t in L_RUNS:
        r, hk, sh = runs.get(t), kept["runs"].get(t), shape["runs"].get(t)
        if r is None or hk is None or sh is None:
            continue
        ev, ab = r["every_declaration"], r["against_best"]
        got[t] = {"chosen_median": value(ev["shares"]["median"]),
                  "security_first": ev["security_first"], "rankings": ev["rankings"],
                  "at_once": value(sh["at_once_median"]["record"]),
                  "completed": value(sh["loop"]["completed"]["share"]),
                  "stated_median": value(hk["loop"]["on_record"]["stated"]["pulled"]["median"]),
                  "agree_all": value(ab["all"]["share"]),
                  "agree_installed": value(ab[INSTALLED]["share"]),
                  "agree_refused": value(ab[REFUSED]["share"])}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    def both(test) -> bool:
        return all(t in got and test(got[t]) for t in ("l_r1", "l_r2"))

    def known(*keys):
        return lambda x: all(x[k] is not None for k in keys)

    w1 = each(lambda x: x["rankings"] > 0 and x["security_first"] == x["rankings"])
    w2 = both(lambda x: known("chosen_median", "at_once")(x) and x["chosen_median"] > x["at_once"])
    w3 = each(lambda x: known("chosen_median", "completed")(x)
              and x["chosen_median"] > x["completed"])
    w4 = each(lambda x: known("agree_all")(x) and x["agree_all"] > F(1, 2))
    w5 = both(lambda x: known("agree_refused", "agree_installed")(x)
              and x["agree_refused"] > x["agree_installed"])
    w6 = each(lambda x: known("chosen_median", "stated_median")(x)
              and x["chosen_median"] > x["stated_median"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "W1", "what": "in every L run, every ranking its declarations choose puts "
                                 "SECURITY_INCIDENT first",
         "reading": shown(("security_first", "rankings")), "holds": w1},
        {"clause": "W2", "what": "in L r1 and in L r2, the rankings its declarations choose decide, "
                                 "at their median, more of the space than at once",
         "reading": shown(("chosen_median", "at_once")), "holds": w2},
        {"clause": "W3", "what": "in every L run, the rankings its declarations choose decide, at "
                                 "their median, more of the space than the loop's base completed",
         "reading": shown(("chosen_median", "completed")), "holds": w3},
        {"clause": "W4", "what": "in every L run, more than half of its votes agree with the best "
                                 "ranking",
         "reading": shown(("agree_all",)), "holds": w4},
        {"clause": "W5", "what": "in L r1 and in L r2, the votes the engine refused agree with the "
                                 "best ranking more often than those it installed",
         "reading": shown(("agree_refused", "agree_installed")), "holds": w5},
        {"clause": "W6", "what": "in every L run, the rankings its declarations choose decide, at "
                                 "their median, more of the space than the model's stated rankings "
                                 "at theirs",
         "reading": shown(("chosen_median", "stated_median")), "holds": w6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "declared.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether the loop declared the ranking it lacks "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/declared.py writes {record_path()}")
    kept, shape = hierarchy_record(), H.shape_record()
    if args.dry_run:
        ones = []
        for t in L_RUNS:
            record, _, _ = S.inputs(t)
            ones += [{"run": t, **S.stage_c(t)}, {"run": t, **H.gate_two(t, shape)},
                     {"run": t, "gate": 3, "what": "the declarations are the record's",
                      "passes": edge_log_matches(record, declarations(record))}]
        for g in ones:
            print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
                  f"  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    runs = {t: read_run(t, kept) for t in L_RUNS}
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(runs, kept, shape)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"hierarchy": str(H.record_path()),
                   "hierarchy_from": kept["_env"].get("git_commit"),
                   "shape": str(S.record_path()),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)}},
        "surface": "the whole space, 134,400 points: each L run's final base, ordered by the "
                   "rankings of the eight queues that its own placement declarations choose, "
                   "under corrections/hierarchy.py's pulled construction",
        "constants": {"rankings": H.N_RANKINGS, "construction": "pulled"},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        ev = r["every_declaration"]
        print(f"  {t}: {ev['votes']} votes; {ev['rankings']} rankings chosen, median "
              f"{ev['shares']['median']['value']:.4f}, security first in {ev['security_first']}; "
              f"agreeing with the best ranking {r['against_best']['all']['share']['value']:.4f}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
