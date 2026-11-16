"""
WHAT THE REST OF WHAT THE DECLARED RANKING LACKS IS.
`corrections/billing.py` found that `BILLING_SPECIALIST`'s place carries a
minority of what each L run's declared ranking lacks against the best ranking of
its rules: at its best place the queue gets the best ranking's recall, and the
ranking still lacks most of what it lacked. Every declared ranking puts
`T3_ENGINEERING` above `ACCOUNT_MANAGER`, and every best ranking puts it below.
This reading asks whether that pair's order carries the rest, where the pair
decides, and why the declarations order it as they do. Proposed by the agent
after `corrections/billing.py`, and asked for by Sergi on 2026-11-16. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE FOUR ORDERS
--------------------------------------------------------------------------
Each L run's final base is ordered by four rankings, each under
`corrections/hierarchy.py`'s pulled construction:
- **the declared ranking**, the one its declarations choose, as
  `declared.json` keeps it;
- **the swap**: the declared ranking with `ACCOUNT_MANAGER` and
  `T3_ENGINEERING` exchanged, every other queue in its place;
- **the best ranking**, as `hierarchy.json` keeps it;
- **the rest**: the best ranking with the two exchanged back. It makes the best
  ranking's other moves and not the swap.
Each order is read on the space and on the corpus, for the points it decides
right, by true queue. From them:
- **the swap alone** is what the swap decides less what the declared ranking
  decides;
- **the rest alone** is what the rest decides less what the declared ranking
  decides;
- **the swap given the rest** is what the best ranking decides less what the
  rest decides;
- **what they leave to each other** is the best ranking less the swap, less the
  rest, plus the declared ranking. It is zero where the two add;
- **what the swap moves**: the points right under the swap and not under the
  declared ranking, and the other way, by true queue and by the policy's layer.
**What the declared ranking lacks** is what the best ranking decides of the
space less what the declared ranking decides.

--------------------------------------------------------------------------
THE POLICY'S LAYERS
--------------------------------------------------------------------------
The eight its file names: security (`H01` to `H03`), severity 1 (`H04` to
`H08`), billing (`H09` to `H12`), churn (`H13`, `H14`), product routing (`H15` to
`H20`), language and staffing (`H21` to `H23`), deflection (`H24` to `H26`) and
the defaults (`H27` to `H29`). Each rule's region is read under first match, as
`manual/instrument.py`'s `hidden_regions` reads it. `ACCOUNT_MANAGER`'s points
lie in the billing and churn layers, and `T3_ENGINEERING`'s in the severity-1
and product-routing layers.

--------------------------------------------------------------------------
THE VOTES ON THE PAIR
--------------------------------------------------------------------------
The votes are `corrections/declared.py`'s, read as `corrections/billing.py`
reads billing's: each citation between a rule of `T3_ENGINEERING` and a rule of
`ACCOUNT_MANAGER`, one a rule and side. A vote **for** a queue puts it above the
other. Each is read for whose answer cast it, the newborn's; its two rules,
nested or not; their shared region on the space and its size; the better rule,
as `rung3/edge_direction.py` reads it, on the space and on the corpus; and where
the shared region lies among the policy's layers.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **The instances are `shape.json`'s**, as `corrections/hierarchy.py`'s gate
     2 reads them.
  3. **The declarations are the record's**, as `corrections/declared.py`'s gate
     3 reads them.
  4. **The rankings are the records'.** The votes choose the rankings
     `declared.json` keeps, and the declared ranking decides what it keeps.
     The best ranking decides what `hierarchy.json` keeps.
  5. **Every order read installs, on both surfaces**, as
     `corrections/billing.py`'s gate 5 reads it.
  6. **The truth is the policy's**, as `corrections/billing.py`'s gate 6 reads
     it; and the eight layers partition the space.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1, 2, 3 and 6 and writes
nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's three runs, each apart. **The votes for
`T3_ENGINEERING`** are those that put it above `ACCOUNT_MANAGER`, and the
**strict** ones those whose shared region has a better rule on the space.

  G1. **The swap carries most of the gap.** In every L run, the swap alone
      gains more than half of what the declared ranking lacks.
  G2. **Cast by its own newborns.** In every L run, most votes for
      `T3_ENGINEERING` were cast by the answers of its own newborns.
  G3. **Right pair by pair.** In every L run, of the strict votes for
      `T3_ENGINEERING`, most name the better rule.
  G4. **About severity 1.** In every L run, most of the points of the shared
      regions of the votes for `T3_ENGINEERING`, counted once a vote, lie in the
      policy's severity-1 layer.
  G5. **The pair decides in the churn layer.** In every L run, most of the
      points the swap gains lie in the policy's churn layer.
  G6. **On the tickets too.** In every L run, the swap decides more of the
      corpus than the declared ranking.

A clause that reads a missing value fails.

**The drafter's account.**
- **The best ranking's other moves pass neither queue in L r2 and L r3.** In
  L r2 it raises `SELF_SERVICE_DEFLECT` above `T2_TECHNICAL`, and in L r3
  billing above two queues below `ACCOUNT_MANAGER`. Under it
  `ACCOUNT_MANAGER` gains 3,240 and 1,840 points of the space, and
  `T3_ENGINEERING` loses 340 and 240. That is 2,900 and 1,600 together, of the
  3,095 and 2,500 the declared ranking lacks.
- **In L r1 billing's move passes `ACCOUNT_MANAGER`** and costs it 1,680 points
  (`corrections/billing.py`). The queue still gains 1,800 under the best
  ranking, so the swap alone should gain it more than that, against 4,045 the
  declared ranking lacks. If the moves add, G1 holds in every run: it is
  trusted most.
- **The policy orders the pair both ways.** Severity 1 comes before churn, and
  churn before product routing. On the space `ACCOUNT_MANAGER`'s churn points
  are 13,920 of its 16,440, and `T3_ENGINEERING`'s severity-1 points 3,780 of
  its 8,180. A ranking gives the pair one direction, and on the space the churn
  layer weighs more: G5.
- **L's reports named the layer below on-call** (`corrections/oncall.py`), and
  its corrections were slices of severity 1 by product, some of them
  `T3_ENGINEERING`'s. A newborn climbs over the rules that held its ticket
  (`corrections/above.py`), and at severity 1 the policy puts the queue above
  `ACCOUNT_MANAGER`'s churn. So its votes are cast by its own newborns, stand on
  severity 1, and are right there: G2, G4, and G3, the bet. That is
  `corrections/billing.py`'s finding again: right pair by pair, wrong as a
  ranking.
- **The votes on the pair are few**: 112, 94 and 64 in the three runs, read
  from `declared.json`. The queue's rules not born at severity 1 vote too, and
  where they meet `ACCOUNT_MANAGER`'s churn they are wrong, so G3 and G4 can fail
  on a few dozen votes.
- **On the corpus**, severity 1 and enterprise clients are rare, and prior
  tickets fall off geometrically, so the churn layer is a much smaller share of
  the arrivals than of the space. G6 argues that what the space pays for
  carries to the arrivals, and the standing note in `IDEAS.md` reads such an
  argument as evidence that the bet is too high. `corrections/billing.py`'s V5,
  the same argument, held by 8 and 14 arrivals of 2,000. G6 is trusted least.

**The bet is G3.** **G1 is trusted most.** **G6 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the sections *A ranking of the queues as the
  order*, *The ranking the loop declared* and *Why the declarations put
  `BILLING_SPECIALIST` low* among it. So `hierarchy.json`'s, `declared.json`'s
  and `billing.json`'s figures, the last its own reading's;
- **`declared.json`'s votes by pair of queues**, those on this pair read again
  before this was written: 68 for `T3_ENGINEERING` and 44 for
  `ACCOUNT_MANAGER` in L r1, 79 and 15 in L r2, and 40 and 24 in L r3;
- **each queue's points under the declared and the best ranking**, computed
  from those records' recalls for the account above;
- the hidden policy's rules, the domain's grid and its sampling weights; and,
  computed for the account, the two queues' points of the space by layer;
- **the reading's size and cost**, timed before this was written, printing no
  vote, no share and no gain: L r1 read whole took 4.2 seconds, and its six
  gates passed;
- **gates 1, 2, 3 and 6**, which pass on the dry run.

**What the drafter had not seen**: what the swap or the rest decides on either
surface, what they leave to each other, what the swap moves and where, and the
votes on the pair rule by rule: whose answers cast them, where they stand, and
whether they name the better rule.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent after `corrections/billing.py`, and asked
for by Sergi on 2026-11-16. The expectation above was written and committed
before the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.gap --dry-run   # gates 1, 2, 3 and 6; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.gap
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from typing import Any, Sequence

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Space
from rung3 import edge_direction as ED

from . import billing as BL
from . import declared as DC
from . import forgotten as fg
from . import hierarchy as H
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
T3, AM = "T3_ENGINEERING", "ACCOUNT_MANAGER"
PAIR = (T3, AM)
LAYERS = (("security", 1, 3), ("severity_1", 4, 8), ("billing", 9, 12), ("churn", 13, 14),
          ("product", 15, 20), ("staffing", 21, 23), ("deflection", 24, 26), ("defaults", 27, 29))
LAYER_NAMES = tuple(name for name, _, _ in LAYERS)
ORDERS = ("declared", "swap", "rest", "best")
PROVENANCE = (
    "POST-RUN: proposed by the agent after corrections/billing.py, and asked for by Sergi on "
    "2026-11-16. The expectation in the module's docstring was written and committed before "
    "the reading ran. Not a signed row; no verdict moves.")

frac = fg.frac
share = fg.share


# ---------------------------------------------------------------------------
# The policy's layers
# ---------------------------------------------------------------------------

def layer_of(rid: str) -> str:
    k = int(rid[1:])
    return next(name for name, lo, hi in LAYERS if lo <= k <= hi)


@lru_cache(maxsize=None)
def policy_layers() -> dict[str, int]:
    """The policy's eight layers over the space, each the union of its rules'
    regions under first match."""
    out = {name: 0 for name in LAYER_NAMES}
    for rid, reg in MI.hidden_regions().items():
        out[layer_of(rid)] |= reg["mask"]
    return out


def by_layer(mask: int, layers: dict[str, int]) -> dict[str, int]:
    return {k: (mask & m).bit_count() for k, m in layers.items()}


def layers_partition() -> bool:
    """Gate 6's second half: the eight layers partition the space."""
    union, disjoint = 0, True
    for m in policy_layers().values():
        disjoint &= not (union & m)
        union |= m
    return bool(disjoint and union == (1 << MI.space().n) - 1)


# ---------------------------------------------------------------------------
# The four orders
# ---------------------------------------------------------------------------

def swapped(ranking: Sequence[str], a: str = T3, b: str = AM) -> tuple[str, ...]:
    """The ranking with `a` and `b` exchanged, every other queue in its place."""
    r = list(ranking)
    i, j = r.index(a), r.index(b)
    r[i], r[j] = r[j], r[i]
    return tuple(r)


def inverted(first: Sequence[str], second: Sequence[str]) -> list[list[str]]:
    """The pairs of queues `first` orders against `second`, the one `first`
    puts above first."""
    pos = {q: i for i, q in enumerate(second)}
    return [[a, b] for i, a in enumerate(first) for b in first[i + 1:] if pos[a] > pos[b]]


def read_surface(right: int, sf: BL.Surface) -> dict[str, Any]:
    return {"right": right.bit_count(), "share": frac(F(right.bit_count(), sf.n)),
            "by_queue": {q: (right & sf.truth.get(q, 0)).bit_count() for q in ACTIONS},
            "recall": {q: frac(share((right & sf.truth.get(q, 0)).bit_count(),
                                     sf.truth.get(q, 0).bit_count())) for q in PAIR}}


def moved(before: int, after: int, sf: BL.Surface,
          layers: dict[str, int] | None = None) -> dict[str, Any]:
    """The points right after and not before, and the other way, by true queue
    and, where layers are given, by layer."""
    out = {}
    for name, m in (("gained", after & ~before), ("lost", before & ~after)):
        out[name] = {"points": m.bit_count(),
                     "by_queue": {q: n for q in ACTIONS
                                  if (n := (m & sf.truth.get(q, 0)).bit_count())}}
        if layers is not None:
            out[name]["by_layer"] = by_layer(m, layers)
    return out


def decomposition(right: dict[str, int]) -> dict[str, int]:
    """What the declared ranking lacks, and the swap's and the rest's parts of it."""
    return {"lacks": right["best"] - right["declared"],
            "swap_alone": right["swap"] - right["declared"],
            "rest_alone": right["rest"] - right["declared"],
            "swap_given_rest": right["best"] - right["rest"],
            "left_to_each_other": (right["best"] - right["swap"] - right["rest"]
                                   + right["declared"])}


# ---------------------------------------------------------------------------
# The votes on the pair
# ---------------------------------------------------------------------------

def pair_rows(decls: Sequence[dict[str, Any]], action: dict[str, str],
              inside: dict[str, frozenset], sp: BL.Surface, co: BL.Surface,
              layers: dict[str, int], pair: tuple[str, str] = PAIR) -> list[dict[str, Any]]:
    """Every vote between a rule of one queue of `pair` and a rule of the other,
    read rule by rule."""
    out = []
    for d in decls:
        if d["ref_queue"] is None or {d["queue"], d["ref_queue"]} != set(pair):
            continue
        w, l = (d["rule"], d["ref"]) if d["side"] == "beats" else (d["ref"], d["rule"])
        wq, lq = action[w], action[l]
        shared, cshared = sp.ext[w] & sp.ext[l], co.ext[w] & co.ext[l]
        out.append({
            "newborn": d["rule"], "cited": d["ref"], "side": d["side"], "verdict": d["verdict"],
            "winner": w, "loser": l, "for": wq, "answer": d["queue"],
            "nested": w in inside[l] or l in inside[w],
            "shared": shared.bit_count(),
            "space": ED.verdict((shared & sp.truth.get(wq, 0)).bit_count(),
                                (shared & sp.truth.get(lq, 0)).bit_count()),
            "corpus": ED.verdict((cshared & co.truth.get(wq, 0)).bit_count(),
                                 (cshared & co.truth.get(lq, 0)).bit_count()),
            "layers": by_layer(shared, layers),
        })
    return out


def side(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    by_answer = Counter(r["newborn"] for r in rows)
    top = by_answer.most_common(1)
    return {"votes": len(rows),
            "by_answer": {q: sum(r["answer"] == q for r in rows) for q in PAIR},
            "by_verdict": dict(sorted(Counter(r["verdict"] for r in rows).items())),
            "answers": len(by_answer),
            "largest_answer": {"newborn": top[0][0], "votes": top[0][1]} if top else None,
            "nested": sum(r["nested"] for r in rows),
            "shared_median": frac(BL.median_of([r["shared"] for r in rows])),
            "space": BL.tally(rows, "space"), "corpus": BL.tally(rows, "corpus"),
            "layers": {k: sum(r["layers"][k] for r in rows) for k in LAYER_NAMES}}


def read_votes(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {f"for_{'t3' if q == T3 else 'am'}": side([r for r in rows if r["for"] == q])
            for q in PAIR}


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def gate_six() -> dict[str, Any]:
    return {"gate": 6, "what": "the truth is the policy's, and its layers partition the space",
            "passes": bool(BL.truth_is_the_policy() and layers_partition())}


def read_run(tag: str, kept_declared: dict[str, Any], kept_hier: dict[str, Any],
             shape: dict[str, Any]) -> dict[str, Any]:
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    rules = {r.rule_id: r for r in engine.rules}
    sp = BL.surface("space", engine.ext, rs.action, rs.inside, truth, space.n)
    co = BL.surface("corpus", BL.corpus_ext(engine.rules), rs.action, rs.inside,
                    BL.corpus_truth(), len(MI.corpus()))
    layers = policy_layers()
    decls = DC.declarations(record)
    rows = pair_rows(decls, rs.action, rs.inside, sp, co, layers)
    perms = H.rankings()
    _, ks = DC.chosen(DC.votes(decls), perms)
    ev = kept_declared["runs"][tag]["every_declaration"]
    best = kept_hier["runs"][tag]["loop"]["pulled"]["best"]
    declared, best_ranking = tuple(ev["orders"]["median"]["ranking"]), tuple(best["ranking"])
    rankings = {"declared": declared, "swap": swapped(declared),
                "rest": swapped(best_ranking), "best": best_ranking}
    reads, masks, gate5 = {}, {}, True
    for name in ORDERS:
        o = H.pulled(rs, H.rank_of(rankings[name]))
        s, c = BL.right_mask(o, sp), BL.right_mask(o, co)
        gate5 &= BL.installs(o, rules, rs, space, s.bit_count(), c.bit_count())
        masks[name] = (s, c)
        reads[name] = {"ranking": list(rankings[name]), "space": read_surface(s, sp),
                       "corpus": read_surface(c, co)}
    gate4 = (len(ks) == ev["rankings"] and BL.chosen_median(rs, sp, perms, ks) == declared
             and reads["declared"]["space"]["right"] == ev["orders"]["median"]["right"]
             and reads["best"]["space"]["right"] == best["right"])
    return {
        "orders": reads,
        "inverted": inverted(declared, best_ranking),
        "gap": {"space": decomposition({k: v["space"]["right"] for k, v in reads.items()}),
                "corpus": decomposition({k: v["corpus"]["right"] for k, v in reads.items()})},
        "the_swap": {"space": moved(masks["declared"][0], masks["swap"][0], sp, layers),
                     "corpus": moved(masks["declared"][1], masks["swap"][1], co)},
        "votes": read_votes(rows),
        "gates": [S.stage_c(tag), H.gate_two(tag, shape),
                  {"gate": 3, "what": "the declarations are the record's",
                   "passes": DC.edge_log_matches(record, decls)},
                  {"gate": 4, "what": "the rankings are the records'", "passes": bool(gate4)},
                  {"gate": 5, "what": "every order read installs, on both surfaces",
                   "passes": bool(gate5)},
                  gate_six()],
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    got: dict[str, dict[str, Any]] = {}
    for t in L_RUNS:
        r = runs.get(t)
        if r is None:
            continue
        g, v, sw = r["gap"], r["votes"]["for_t3"], r["the_swap"]["space"]
        got[t] = {"swap_alone": g["space"]["swap_alone"], "lacks": g["space"]["lacks"],
                  "by_its_own": v["by_answer"][T3], "votes": v["votes"],
                  "named": v["space"]["named"], "strict": v["space"]["strict"],
                  "severity_1": v["layers"]["severity_1"],
                  "all_layers": sum(v["layers"].values()),
                  "gained": sw["gained"]["points"],
                  "gained_in_churn": sw["gained"]["by_layer"]["churn"],
                  "corpus_swap_alone": g["corpus"]["swap_alone"]}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    g1 = each(lambda x: x["lacks"] > 0 and 2 * x["swap_alone"] > x["lacks"])
    g2 = each(lambda x: x["votes"] > 0 and 2 * x["by_its_own"] > x["votes"])
    g3 = each(lambda x: x["strict"] > 0 and 2 * x["named"] > x["strict"])
    g4 = each(lambda x: x["all_layers"] > 0 and 2 * x["severity_1"] > x["all_layers"])
    g5 = each(lambda x: x["gained"] > 0 and 2 * x["gained_in_churn"] > x["gained"])
    g6 = each(lambda x: x["corpus_swap_alone"] > 0)

    def shown(keys):
        return {t: {k: x[k] for k in keys} for t, x in got.items()}

    return [
        {"clause": "G1", "what": "in every L run, the swap alone gains more than half of what the "
                                 "declared ranking lacks",
         "reading": shown(("swap_alone", "lacks")), "holds": g1},
        {"clause": "G2", "what": "in every L run, most votes for T3_ENGINEERING were cast by the "
                                 "answers of its own newborns",
         "reading": shown(("by_its_own", "votes")), "holds": g2},
        {"clause": "G3", "what": "in every L run, of the strict votes for T3_ENGINEERING, most name "
                                 "the better rule",
         "reading": shown(("named", "strict")), "holds": g3},
        {"clause": "G4", "what": "in every L run, most of the points of the shared regions of the "
                                 "votes for T3_ENGINEERING, counted once a vote, lie in the "
                                 "policy's severity-1 layer",
         "reading": shown(("severity_1", "all_layers")), "holds": g4},
        {"clause": "G5", "what": "in every L run, most of the points the swap gains lie in the "
                                 "policy's churn layer",
         "reading": shown(("gained_in_churn", "gained")), "holds": g5},
        {"clause": "G6", "what": "in every L run, the swap decides more of the corpus than the "
                                 "declared ranking",
         "reading": shown(("corpus_swap_alone",)), "holds": g6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "gap.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="What the rest of what the declared ranking lacks "
                                             "is (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1, 2, 3 and 6 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/gap.py writes {record_path()}")
    kept_declared, kept_hier, shape = (BL.declared_record(), DC.hierarchy_record(),
                                       H.shape_record())
    if args.dry_run:
        ones = []
        for t in L_RUNS:
            record, _, _ = S.inputs(t)
            ones += [{"run": t, **S.stage_c(t)}, {"run": t, **H.gate_two(t, shape)},
                     {"run": t, "gate": 3, "what": "the declarations are the record's",
                      "passes": DC.edge_log_matches(record, DC.declarations(record))},
                     {"run": t, **gate_six()}]
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
                   "run's final base ordered by its declared ranking, by that ranking with "
                   "ACCOUNT_MANAGER and T3_ENGINEERING exchanged, by its best ranking, and by "
                   "that ranking with the two exchanged back, under corrections/hierarchy.py's "
                   "pulled construction; and the run's placement declarations on that pair read "
                   "rule by rule",
        "constants": {"construction": "pulled", "pair": list(PAIR),
                      "layers": {name: f"H{lo:02d}-H{hi:02d}" for name, lo, hi in LAYERS}},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        g = r["gap"]["space"]
        print(f"  {t}: lacks {g['lacks']}; the swap alone {g['swap_alone']}, the rest alone "
              f"{g['rest_alone']}, the swap given the rest {g['swap_given_rest']}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
