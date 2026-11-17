"""
A COUNT OF WHAT EACH PAIR DECIDES.
`corrections/billing.py` and `corrections/gap.py` found two ways the count of the
loop's declarations fails. For billing, right votes about points the pair does
not decide outweighed the rest. For `T3_ENGINEERING` and `ACCOUNT_MANAGER`, wrong
votes outnumbered right ones. A count that reads no truth can leave out the
first kind. This reading asks whether doing so places the queues better, and
whether it reaches the pair that carries most of what the declared ranking
lacks. Proposed by the agent after `corrections/gap.py`, and asked for by Sergi
on 2026-11-17. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE COUNT
--------------------------------------------------------------------------
The votes are `corrections/declared.py`'s: each citation of a rule of another
queue, one a rule and side, is one vote for the queue declared above.
- **The first pass** is the declared ranking, the one every vote chooses, as
  `declared.json` keeps it. It orders the run's final base under
  `corrections/hierarchy.py`'s pulled construction.
- **What a pair decides in an order** is the points of the space where both of
  its rules match and have no rule strictly inside them that matches, and no
  rule placed before both does either. There the pair's own order decides the
  point. Rung 2's engine reads the same masks, and so could a loop: it reads the
  rules and the space, and no truth.
- **The kept votes** are those whose pair decides at least one point in the
  declared ranking's order. A vote whose pair decides nothing there says nothing
  a ranking can use. **The count kept** is theirs, one a vote. It chooses
  rankings as `corrections/declared.py`'s count does: those that agree with the
  most votes, read whole, their median by what it decides of the space.
- **One variant is read.** A count weighted by the points each pair decides was
  set aside before the reading ran, so that no choice between variants is made
  after it.
- **Stability.** The kept votes are read again in the order of the median
  ranking they choose, and the reading says whether that changes the ranking.
  It is reported, and no clause reads it.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
For each L run:
- **the votes**: how many, how many kept, and by pair of queues, all and kept;
- **the rankings the kept count chooses**: how many, their shares of the space,
  and the least, the median and the most read as orders, each installed. Beside
  them: where the median puts `BILLING_SPECIALIST`, and whether it puts
  `ACCOUNT_MANAGER` above `T3_ENGINEERING`. Its order is also read on the
  corpus;
- **the kept votes against the best ranking**: of the kept votes and of those
  left out, the share that agrees with the run's best ranking;
- **beside them**: the declared ranking and the best ranking as their records
  keep them, and at once as `shape.json` keeps it.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **The instances are `shape.json`'s**, as `corrections/hierarchy.py`'s gate
     2 reads them.
  3. **The declarations are the record's**, as `corrections/declared.py`'s gate
     3 reads them.
  4. **The rankings are the records'.** Every vote chooses the rankings
     `declared.json` keeps, and the declared ranking decides what it keeps.
     The best ranking decides what `hierarchy.json` keeps.
  5. **Every order read installs, on both surfaces.** The three orders of the
     kept count's rankings install as `corrections/declared.py`'s gate 5 reads
     them, and none decides more than the rules' bound. The median also
     installs as `corrections/billing.py`'s gate 5 reads it, on the corpus too.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 to 3 and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
**The kept ranking** is the median of the rankings the kept count chooses. **The
declared ranking**, **the best ranking** and **at once** are as their records
keep them.

  P1. **Billing rises.** In L r1 and in L r3, the kept ranking puts
      `BILLING_SPECIALIST` higher than the declared ranking does.
  P2. **Better than the count of all.** In every L run, the kept ranking
      decides more of the space than the declared ranking.
  P3. **The pair turns.** In every L run, the kept ranking puts
      `ACCOUNT_MANAGER` above `T3_ENGINEERING`.
  P4. **Above at once.** In L r1 and in L r2, the kept ranking decides more of
      the space than at once.
  P5. **The kept are the righter.** In every L run, the kept votes agree with
      the best ranking more often than the votes left out.
  P6. **On the tickets too.** In every L run, the kept ranking decides more of
      the corpus than the declared ranking.

A clause that reads a missing value fails.

**The drafter's account.**
- **The votes about the layers above billing's decide little in the declared
  ranking's order.** There the security and on-call rules come before both
  rules of most of billing's pairs, and decide the keyword's tickets and
  severity 1 before them. In L r3 `T2_TECHNICAL`'s votes against billing stand
  almost wholly on those points, and in L r1 its pair with billing was 167 votes
  to 166 (`corrections/billing.py`). Left out, they let billing past it: P1,
  trusted most.
- **The votes about the security layer come out on both sides of the pair.**
  Counted once a vote, those for `T3_ENGINEERING` stand mostly on the security
  and severity-1 layers, and those for `ACCOUNT_MANAGER` more on churn
  (`corrections/gap.py`). But a vote is kept if its pair decides any point, and
  a region that reaches churn decides there. So the kept count may still give
  the pair to `T3_ENGINEERING`: P3 is the bet, and not a confident one.
- **P4 rests on P3 in L r1.** There billing's move alone stays short of at once,
  and turning the pair alone beats it. In L r2 the declared ranking is already
  above at once.
- **P2 follows P1 where billing rises past queues the space puts below it.**
  The kept count can also move pairs the reading above did not read.
- **P5 reads whether leaving votes out removes more wrong votes than right
  ones.** For billing it should; for the pair, the votes about severity 1 left
  out are mostly `T3_ENGINEERING`'s, which disagree with the best ranking.
- **On the corpus**, the arrivals weigh severity 1 and the keyword far less than
  the space, and churn less too. P6 argues that what the space pays for carries
  to the arrivals. `corrections/billing.py`'s V5 and `corrections/gap.py`'s G6
  held on that argument, by a handful of arrivals. P6 is trusted least.

**The bet is P3.** **P1 is trusted most.** **P6 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, and so the figures of `hierarchy.json`,
  `declared.json`, `billing.json` and `gap.json`, the last two its own
  readings', among them where the votes on billing's pairs and on
  `T3_ENGINEERING` and `ACCOUNT_MANAGER` stand among the policy's layers;
- `declared.json`'s votes by pair of queues;
- **the reading's size and cost**, timed before this was written, printing no
  vote, no ranking and no share: L r1 read whole took 8.8 seconds, and its
  five gates passed;
- **gates 1, 2 and 3**, which pass on the dry run.

**What the drafter had not seen**: which votes the pairs decide nothing for,
how many are kept, the rankings the kept count chooses, what they decide on
either surface, and how the kept votes stand against the best ranking.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent after `corrections/gap.py`, and asked for by
Sergi on 2026-11-17. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.decides --dry-run   # gates 1 to 3; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.decides
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

from . import billing as BL
from . import declared as DC
from . import forgotten as fg
from . import hierarchy as H
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
BILLING, T3, AM = "BILLING_SPECIALIST", "T3_ENGINEERING", "ACCOUNT_MANAGER"
PROVENANCE = (
    "POST-RUN: proposed by the agent after corrections/gap.py, and asked for by Sergi on "
    "2026-11-17. The expectation in the module's docstring was written and committed before "
    "the reading ran. Not a signed row; no verdict moves.")

frac = fg.frac
share = fg.share


# ---------------------------------------------------------------------------
# What a pair decides in an order
# ---------------------------------------------------------------------------

def vote_rows(decls: Sequence[dict[str, Any]], action: dict[str, str]) -> list[dict[str, Any]]:
    """Every vote between rules of two queues: its winner and loser, by the side
    declared."""
    out = []
    for d in decls:
        if d["ref_queue"] is None or d["ref_queue"] == d["queue"]:
            continue
        w, l = (d["rule"], d["ref"]) if d["side"] == "beats" else (d["ref"], d["rule"])
        out.append({"winner": w, "loser": l, "for": action[w], "against": action[l],
                    "verdict": d["verdict"]})
    return out


def prefixes(order: Sequence[str], M: dict[str, int]) -> tuple[dict[str, int], list[int]]:
    """Each rule's place in the order, and the points some rule before each
    place matches undefeated: `before[i]` for the rules ahead of place `i`."""
    pos = {r: i for i, r in enumerate(order)}
    before, acc = [], 0
    for r in order:
        before.append(acc)
        acc |= M[r]
    return pos, before


def decided(rows: Sequence[dict[str, Any]], order: Sequence[str],
            M: dict[str, int]) -> list[int]:
    """For each vote, how many points its pair decides in `order`: both rules
    match undefeated, and no rule before both does."""
    pos, before = prefixes(order, M)
    return [(M[r["winner"]] & M[r["loser"]] & ~before[min(pos[r["winner"]], pos[r["loser"]])]
             ).bit_count() for r in rows]


def count(rows: Sequence[dict[str, Any]]) -> Counter:
    """One vote a row, for the queue declared above over the other."""
    out: Counter = Counter()
    for r in rows:
        out[(r["for"], r["against"])] += 1
    return out


def agreeing(rows: Sequence[dict[str, Any]], ranking: Sequence[str]) -> dict[str, Any]:
    """Of `rows`, those that agree with `ranking`."""
    rank = H.rank_of(ranking)
    n = sum(rank[r["for"]] < rank[r["against"]] for r in rows)
    return {"votes": len(rows), "agreeing": n, "share": frac(share(n, len(rows)))}


def place(ranking: Sequence[str], queue: str) -> int:
    return list(ranking).index(queue) + 1


def above(ranking: Sequence[str], a: str, b: str) -> bool:
    return place(ranking, a) < place(ranking, b)


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(tag: str, kept_declared: dict[str, Any], kept_hier: dict[str, Any],
             shape: dict[str, Any]) -> dict[str, Any]:
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    rules = {r.rule_id: r for r in engine.rules}
    inst = S.instance(engine.rules, engine.ext, rs.inside, rs.around, truth, space.n)
    M = S.undefeated(engine.ext, rs.inside)
    sp = BL.surface("space", engine.ext, rs.action, rs.inside, truth, space.n)
    co = BL.surface("corpus", BL.corpus_ext(engine.rules), rs.action, rs.inside,
                    BL.corpus_truth(), len(MI.corpus()))
    decls = DC.declarations(record)
    rows = vote_rows(decls, rs.action)
    perms = H.rankings()
    # the first pass: the declared ranking, as every vote chooses it
    ev = kept_declared["runs"][tag]["every_declaration"]
    declared = tuple(ev["orders"]["median"]["ranking"])
    best = kept_hier["runs"][tag]["loop"]["pulled"]["best"]
    _, ks = DC.chosen(DC.votes(decls), perms)
    first = H.pulled(rs, H.rank_of(declared))
    declared_right = BL.right_mask(first, sp).bit_count()
    gate4 = (len(ks) == ev["rankings"] and BL.chosen_median(rs, sp, perms, ks) == declared
             and declared_right == ev["orders"]["median"]["right"]
             and BL.right_mask(H.pulled(rs, H.rank_of(best["ranking"])), sp).bit_count()
             == best["right"]
             and count(rows) == DC.votes(decls))
    # the kept votes, and the rankings they choose
    points = decided(rows, first, M)
    kept = [r for r, n in zip(rows, points) if n]
    out_ = [r for r, n in zip(rows, points) if not n]
    chosen, ok = DC.read_chosen(rs, inst, rules, perms, count(kept), space, truth)
    median_ranking = tuple(chosen["orders"]["median"]["ranking"])
    o = H.pulled(rs, H.rank_of(median_ranking))
    s, c = BL.right_mask(o, sp), BL.right_mask(o, co)
    ok &= BL.installs(o, rules, rs, space, s.bit_count(), c.bit_count())
    # stability: the kept votes again, in the median's order
    again = [r for r, n in zip(rows, decided(rows, o, M)) if n]
    _, ks2 = DC.chosen(count(again), perms)
    by_pair = []
    for i, a in enumerate(ACTIONS):
        for b in ACTIONS[i + 1:]:
            pair = {"pair": [a, b]}
            for name, rs_ in (("all", rows), ("kept", kept)):
                v = count(rs_)
                pair[name] = {"for_first": v.get((a, b), 0), "for_second": v.get((b, a), 0)}
            by_pair.append(pair)
    corpus_declared = BL.right_mask(first, co).bit_count()
    return {
        "votes": {"all": len(rows), "kept": len(kept), "left_out": len(out_),
                  "by_pair": by_pair},
        "kept_count": {**chosen,
                       "median": {"ranking": list(median_ranking),
                                  "billing_place": place(median_ranking, BILLING),
                                  "account_manager_above_t3": above(median_ranking, AM, T3),
                                  "space": {"right": s.bit_count(),
                                            "share": frac(F(s.bit_count(), space.n))},
                                  "corpus": {"right": c.bit_count()}},
                       "stable": {"same_median": any(perms[k] == median_ranking for k in ks2),
                                  "rankings_again": len(ks2), "kept_again": len(again)}},
        "against_best": {"best": list(best["ranking"]),
                         "kept": agreeing(kept, best["ranking"]),
                         "left_out": agreeing(out_, best["ranking"])},
        "beside": {"declared": {"ranking": list(declared),
                                "billing_place": place(declared, BILLING),
                                "account_manager_above_t3": above(declared, AM, T3),
                                "space": {"right": declared_right,
                                          "share": frac(F(declared_right, space.n))},
                                "corpus": {"right": corpus_declared}},
                   "best": {"ranking": list(best["ranking"]), "share": best["share"]},
                   "at_once": shape["runs"][tag]["at_once_median"]["record"]},
        "gates": [S.stage_c(tag), H.gate_two(tag, shape),
                  {"gate": 3, "what": "the declarations are the record's",
                   "passes": DC.edge_log_matches(record, decls)},
                  {"gate": 4, "what": "the rankings are the records'", "passes": bool(gate4)},
                  {"gate": 5, "what": "every order read installs, on both surfaces",
                   "passes": bool(ok)}],
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
        m, d, ab = r["kept_count"]["median"], r["beside"]["declared"], r["against_best"]
        got[t] = {"kept_billing_place": m["billing_place"],
                  "declared_billing_place": d["billing_place"],
                  "kept_share": value(m["space"]["share"]),
                  "declared_share": value(d["space"]["share"]),
                  "account_manager_above_t3": m["account_manager_above_t3"],
                  "at_once": value(r["beside"]["at_once"]),
                  "kept_agree": value(ab["kept"]["share"]),
                  "left_out_agree": value(ab["left_out"]["share"]),
                  "kept_corpus": m["corpus"]["right"], "declared_corpus": d["corpus"]["right"]}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    def runs_of(names, test) -> bool:
        return all(t in got and test(got[t]) for t in names)

    def known(*keys):
        return lambda x: all(x[k] is not None for k in keys)

    p1 = runs_of(("l_r1", "l_r3"), lambda x: x["kept_billing_place"] < x["declared_billing_place"])
    p2 = each(lambda x: known("kept_share", "declared_share")(x)
              and x["kept_share"] > x["declared_share"])
    p3 = each(lambda x: x["account_manager_above_t3"])
    p4 = runs_of(("l_r1", "l_r2"), lambda x: known("kept_share", "at_once")(x)
                 and x["kept_share"] > x["at_once"])
    p5 = each(lambda x: known("kept_agree", "left_out_agree")(x)
              and x["kept_agree"] > x["left_out_agree"])
    p6 = each(lambda x: x["kept_corpus"] > x["declared_corpus"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "P1", "what": "in L r1 and in L r3, the kept ranking puts BILLING_SPECIALIST "
                                 "higher than the declared ranking does",
         "reading": shown(("kept_billing_place", "declared_billing_place")), "holds": p1},
        {"clause": "P2", "what": "in every L run, the kept ranking decides more of the space than "
                                 "the declared ranking",
         "reading": shown(("kept_share", "declared_share")), "holds": p2},
        {"clause": "P3", "what": "in every L run, the kept ranking puts ACCOUNT_MANAGER above "
                                 "T3_ENGINEERING",
         "reading": shown(("account_manager_above_t3",)), "holds": p3},
        {"clause": "P4", "what": "in L r1 and in L r2, the kept ranking decides more of the space "
                                 "than at once",
         "reading": shown(("kept_share", "at_once")), "holds": p4},
        {"clause": "P5", "what": "in every L run, the kept votes agree with the best ranking more "
                                 "often than the votes left out",
         "reading": shown(("kept_agree", "left_out_agree")), "holds": p5},
        {"clause": "P6", "what": "in every L run, the kept ranking decides more of the corpus than "
                                 "the declared ranking",
         "reading": shown(("kept_corpus", "declared_corpus")), "holds": p6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "decides.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="A count of what each pair decides "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 3 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/decides.py writes {record_path()}")
    kept_declared, kept_hier, shape = (BL.declared_record(), DC.hierarchy_record(),
                                       H.shape_record())
    if args.dry_run:
        ones = []
        for t in L_RUNS:
            record, _, _ = S.inputs(t)
            ones += [{"run": t, **S.stage_c(t)}, {"run": t, **H.gate_two(t, shape)},
                     {"run": t, "gate": 3, "what": "the declarations are the record's",
                      "passes": DC.edge_log_matches(record, DC.declarations(record))}]
        for g in ones:
            print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
                  f"  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    runs = {t: read_run(t, kept_declared, kept_hier, shape) for t in L_RUNS}
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
        "source": {"declared": str(DC.record_path()),
                   "declared_from": kept_declared["_env"].get("git_commit"),
                   "hierarchy": str(H.record_path()),
                   "hierarchy_from": kept_hier["_env"].get("git_commit"),
                   "shape": str(S.record_path()),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)}},
        "surface": "the whole space, 134,400 points, and the corpus, 2,000 arrivals: each L "
                   "run's final base ordered by the rankings the votes whose pair decides a "
                   "point in the declared ranking's order choose, under "
                   "corrections/hierarchy.py's pulled construction",
        "constants": {"construction": "pulled", "count": "one a kept vote",
                      "first_pass": "the declared ranking, as declared.json keeps it"},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        m = r["kept_count"]["median"]
        print(f"  {t}: {r['votes']['kept']} of {r['votes']['all']} votes kept; the kept ranking "
              f"decides {m['space']['share']['value']:.4f}, billing at {m['billing_place']}, "
              f"ACCOUNT_MANAGER above T3_ENGINEERING: {m['account_manager_above_t3']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
