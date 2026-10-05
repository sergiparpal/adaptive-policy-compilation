"""
THE THREE BASES, READ FOR WHAT STAGE E WOULD CHANGE. A POST-RUN reading of
`PLAN_REUSE.md`'s Stage B records: the structure the proposer left in each final
base. Zero API calls.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Stage E, §11 of `PLAN_PAIRWISE.md`, specified and not authorised, would make the
proposer declare, for each rule a new one overlaps, whether it is an exception
to it or a default under it. It predicts two things, both written in August
against rung 1's base: that subsumption's silent error over a base written that
way falls well below rung 1's at comparable or greater coverage, and that the
gap between the hybrid and the pure coverage bounds narrows.

A plan that ran it would sit on the loop `PLAN_REUSE.md` ran, so its baseline is
that loop's three bases, and not rung 1's. Nothing had measured those quantities
on them. This module does, beside the two bases whose figures are published,
which are its references and its gates.

--------------------------------------------------------------------------
WHAT IT MEASURES
--------------------------------------------------------------------------
For each base, loaded whole from case 0, as `harness/learned_subsumption.py`
loaded rung 1's:

  pairs        how many overlap, how many are nested, one strictly inside the
               other, and the population that could carry a declared edge:
               overlapping, not nested, different queues.
  subsumption  the arbiter alone: a case is decided when the minimal matching
               rules agree on the queue. On the full corpus and over the
               exhaustive space: decided, conflicts, impasses, coverage, silent
               error and end to end.
  bounds       the coverage bounds of the pure and the hybrid pool, on the full
               corpus and over the space, and the gap between them.
  copies       `rung3/identical_rules.py`'s census: rules written the same and
               rules covering the same, by whether the queues agree.

--------------------------------------------------------------------------
THE GATES. No base of the three is profiled before all of them pass.
--------------------------------------------------------------------------
  1. **The hand-written policy reproduces**: 61 nested pairs of 406; subsumption
     decides 1,263 corpus cases, all right, and 35,102 points of the space, all
     right; its population is the 199 declared edges.
  2. **Rung 1's base reproduces**: 8,599 nested pairs of 166,176; subsumption
     decides 160 corpus cases, 75 of them right; its population is 31,850; its
     bounds are `order_search_ls.json`'s; its copies are `identical_rules.json`'s.
  3. **The three bases are the records' own**: each run's rule count is the
     `n_rules` its record publishes.
  4. **`PLAN_REUSE.md` is signed**, as for every writer in `reuse/`.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE RUN AND NOT SIGNED
--------------------------------------------------------------------------
For each of the three bases:

  1. It nests less than the hand-written policy: its share of nested pairs is
     below that policy's.
  2. Subsumption alone decides more of the corpus than on rung 1's base: its
     coverage is above rung 1's.
  3. Its silent error on the corpus sits nearer rung 1's than the hand-written
     policy's: above half of rung 1's.
  4. No two of its rules are written the same, with the same queue or another.
  5. The gap between its pure and hybrid bounds on the corpus is below rung 1's.

The reasons. Rung 2's proposer, shown the base, writes mostly disjoint rules,
so there is little nesting for subsumption to prune and few conflicts for it to
leave open. Most of the rules' errors are born with them, so leaving an error to
subsumption does not remove it. And a rule born on an impasse cannot copy one
that already covers its ticket. `EXPECTED` carries the five clauses in a form
the module reads mechanically, with lines taken from the two gated references.

**What the drafter had seen**: the published figures of the two references, and
of `PLAN_REUSE.md`'s three runs their records' metrics and what
`FINDINGS_REUSE.md` and `FINDINGS_EDGES.md` publish: 62, 31 and 42 escalations,
a median of 12 CONFLICTs with 30 in run 1, 30, 6 and 28 accepted edges of which
50 were installed, and the rule count of run 1. And `FINDINGS2.md`'s overlap at
n=100: 17.5% of pairs without the base shown, 1.60% with it. No pair of rules of
any of the three bases had been compared.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN with an expectation written before the run**, in this module and in
its record, and committed before it ran. A baseline for a plan not yet drafted;
not a signed row, not on `STATUS.md`'s scoreboard, not a calibration event.

--------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN, AND LABELLED SO
--------------------------------------------------------------------------
The first run found clause 4 refuted on every base: hundreds of pairs written the
same, all with the same queue. `vehicles` says what those copies are: for each
group of rules written the same in a run, which was born first, and for every
later copy the outcome of the escalation it was born on, the edges the engine
accepted at that escalation, and how many cases the copy decided. It was written
after the readings above existed, reads only the run records, and changes none
of them. The section of `FINDINGS_REUSE.md` that reads it says whether the run
from the commit that added it reproduced the first run's figures.

    python3 -m reuse.structure --dry-run   # the gates on the references; writes nothing
    python3 -m reuse.structure             # refuses while PLAN_REUSE.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import generate_corpus
from harness.dsl import Condition
from harness.provenance import describe, environment
from rung2.engine2 import Space, strictly_below
from rung2.pair_judgement import GATE_POPULATION, N_DECLARED
from rung3.identical_rules import groups, pairs_of, written
from rung3.local_search import build_masks
from rung3.order_search import build_tables, subsumption_below
from rung3.order_search_ls import bound_of, space_pools, space_truth_masks

from . import plan

RECORD = plan.OUT / "structure.json"
RUNG1 = Path("results/llm_run.json")
PUBLISHED_HIDDEN = Path("results/subsumption.json")
PUBLISHED_HIDDEN_SPACE = Path("results2/ceiling2_space.json")
PUBLISHED_RUNG1 = Path("results/learned_subsumption.json")
PUBLISHED_BOUNDS = Path("results3/order_search_ls.json")
PUBLISHED_COPIES = Path("results3/identical_rules.json")

REFERENCES = ("hand_written", "rung1")
BASES = tuple(f"reuse_r{rep}" for rep in range(1, plan.REPS + 1))

PROVENANCE = (
    "POST-RUN with an expectation written before the run, in the module and in "
    "this record, and committed before it ran. A baseline for a plan not yet "
    "drafted: Stage E of PLAN_PAIRWISE.md §11. Not a signed row, not on "
    "STATUS.md's scoreboard, not a calibration event. Zero API calls.")

EXPECTATION = (
    "Written before the run and committed before it ran. For each of the three "
    "bases: (1) it nests less than the hand-written policy; (2) subsumption alone "
    "decides more of the corpus than on rung 1's base; (3) its silent error on the "
    "corpus is above half of rung 1's; (4) no two of its rules are written the "
    "same, with the same queue or another; (5) the gap between its pure and "
    "hybrid bounds on the corpus is below rung 1's. The reasons: rung 2's "
    "proposer, shown the base, writes mostly disjoint rules, so there is little "
    "nesting to prune and few conflicts to leave open; most of the rules' errors "
    "are born with them; and a rule born on an impasse cannot copy one that "
    "already covers its ticket.")

SEEN = (
    "The published figures of the two references. Of PLAN_REUSE.md's three runs, "
    "their records' metrics and what FINDINGS_REUSE.md and FINDINGS_EDGES.md "
    "publish: 62, 31 and 42 escalations, a median of 12 CONFLICTs with 30 in run "
    "1, 30, 6 and 28 accepted edges of which 50 were installed, and run 1's rule "
    "count. FINDINGS2.md's overlap at n=100: 17.5% of pairs without the base "
    "shown, 1.60% with it. No pair of rules of any of the three bases had been "
    "compared.")

# The five clauses, as (clause, what, how to read a profile, line from the two
# gated references, the test of the reading against the line).
EXPECTED = (
    ("1", "nested share below the hand-written policy's",
     lambda p: p["pairs"]["nested_share"],
     lambda ref: ref["hand_written"]["pairs"]["nested_share"], lambda v, l: v < l),
    ("2", "corpus coverage of subsumption above rung 1's",
     lambda p: p["subsumption"]["corpus"]["coverage"],
     lambda ref: ref["rung1"]["subsumption"]["corpus"]["coverage"], lambda v, l: v > l),
    ("3", "corpus silent error of subsumption above half of rung 1's",
     lambda p: p["subsumption"]["corpus"]["silent_error"],
     lambda ref: ref["rung1"]["subsumption"]["corpus"]["silent_error"] / 2,
     lambda v, l: v > l),
    ("4", "pairs written the same, same queue or another, equal to none",
     lambda p: sum(p["copies"]["written"]["pairs"].values()),
     lambda ref: 0, lambda v, l: v == l),
    ("5", "corpus gap between the pure and hybrid bounds below rung 1's",
     lambda p: p["bounds"]["gap"]["corpus"],
     lambda ref: ref["rung1"]["bounds"]["gap"]["corpus"], lambda v, l: v < l),
)


# ---------------------------------------------------------------------------
# The bases, as rule dicts
# ---------------------------------------------------------------------------

def hand_written() -> list[dict]:
    """The hidden policy's 29 rules as `harness/ceiling_check.py` transcribes
    them, `born_at` their position, as `build_rules` sets it."""
    return [{"rule_id": rid, "action": action, "born_at": i,
             "conditions": [{"attr": a, "op": o, "value": v} for a, o, v in conds]}
            for i, (rid, conds, action) in enumerate(HIDDEN_DSL)]


def from_record(path: Path) -> list[dict]:
    return [{k: r[k] for k in ("rule_id", "conditions", "action", "born_at")}
            for r in json.loads(path.read_text())["rules"]]


# ---------------------------------------------------------------------------
# The four readings, pure
# ---------------------------------------------------------------------------

def pair_census(ids, ext, below, action) -> dict:
    """Overlapping, nested and the population, as `learned_population` draws it:
    overlapping, neither strictly inside the other, different queues."""
    n = len(ids)
    possible = n * (n - 1) // 2
    nested = sum(len(below[r]) for r in ids)
    overlapping = population = 0
    degree = Counter({r: 0 for r in ids})
    for i, a in enumerate(ids):
        ea = ext[a]
        for b in ids[i + 1:]:
            eb = ext[b]
            if not ea & eb:
                continue
            overlapping += 1
            degree[a] += 1
            degree[b] += 1
            if not (strictly_below(ea, eb) or strictly_below(eb, ea)) \
                    and action[a] != action[b]:
                population += 1
    return {"possible": possible, "overlapping": overlapping, "nested": nested,
            "population": population,
            "overlapping_share": overlapping / possible if possible else None,
            "nested_share": nested / possible if possible else None,
            "overlap_degree": {"mean": sum(degree.values()) / n if n else None,
                               "max": max(degree.values(), default=0)}}


def arbitration(counts: Counter, correct: int, n: int) -> dict:
    act = counts["action"]
    return {"n": n, "action": act, "conflict": counts["conflict"],
            "impasse": counts["impasse"], "correct": correct,
            "coverage": act / n, "silent_error": (act - correct) / act if act else None,
            "e2e": correct / n}


def subsumption_on_corpus(matched, undef, truth, action) -> dict:
    """`learned_subsumption.decide_subsumption`, case by case: an impasse when
    no rule matches, a decision when the minimal rules agree on the queue."""
    c, correct = Counter(), 0
    for m, u, y in zip(matched, undef, truth):
        if not m:
            c["impasse"] += 1
        elif len({action[r] for r in u}) == 1:
            c["action"] += 1
            correct += action[u[0]] == y
        else:
            c["conflict"] += 1
    return arbitration(c, correct, len(truth))


def subsumption_on_space(undefeated, action, tmask, n) -> dict:
    """The same arbiter over the space, by masks. A rule is minimal at a point
    exactly where it is undefeated, so a point is decided when the undefeated
    rules there all carry one queue."""
    by_queue: dict[str, int] = {}
    for rid, m in undefeated.items():
        by_queue[action[rid]] = by_queue.get(action[rid], 0) | m
    one = two = 0
    for m in by_queue.values():
        two |= one & m
        one |= m
    only = one & ~two
    correct = sum((m & only & tmask[q]).bit_count() for q, m in by_queue.items())
    c = Counter(action=only.bit_count(), conflict=two.bit_count(),
                impasse=n - one.bit_count())
    return arbitration(c, correct, n)


def bounds(ids, pools_corpus, truth, action, pools_space) -> dict:
    """`order_search_ls`'s coverage bounds, on the full corpus and the space."""
    out = {}
    for name, pool in pools_corpus.items():
        M, W, full = build_masks(ids, pool, truth, action, list(range(len(truth))))
        out[name] = {"corpus": bound_of(M, W, full, len(truth))[0],
                     "space": bound_of(*pools_space[name])[0]}
    out["gap"] = {s: out["puro"][s] - out["hibrido"][s] for s in ("corpus", "space")}
    return out


def copies(rules, ext, action, listed: bool) -> dict:
    """`rung3/identical_rules.py`'s two definitions, counted."""
    out = {}
    for name, key in (("written", {r["rule_id"]: written(r["conditions"]) for r in rules}),
                      ("covering", {rid: e for rid, e in ext.items() if e})):
        gs = groups(key)
        p = pairs_of(gs, action)
        out[name] = {"groups": len(gs), "rules_in_groups": sum(len(g) for g in gs),
                     "pairs": {k: len(v) for k, v in p.items()}}
        if listed:
            out[name]["different_queue_pairs"] = [list(x) for x in p["different_queue"]]
    return out


def vehicles(path: Path) -> dict:
    """
    The copies of a run, read off its record: for each group of rules written
    the same, the first-born, and for each later copy the escalation it was born
    on, the edges accepted there, and the cases it decided. Added after the first
    run; see the module's last section.
    """
    d = json.loads(path.read_text())
    byid = {r["rule_id"]: r for r in d["rules"]}
    at = {r["idx"]: r for r in d["records"]}
    later = []
    for g in groups({r["rule_id"]: written(r["conditions"]) for r in d["rules"]}):
        first, *rest = sorted(g, key=lambda r: (byid[r]["born_at"], r))
        for rid in rest:
            b = byid[rid]["born_at"]
            later.append({"rule_id": rid, "copy_of": first, "born_at": b,
                          "born_on": at[b]["outcome"],
                          "edges_accepted_at_birth": at[b]["edges_accepted"],
                          "cases_decided": byid[rid]["fire_count"]})
    return {"later_copies": len(later),
            "born_on": dict(Counter(c["born_on"] for c in later)),
            "edges_accepted_at_their_births": sum(c["edges_accepted_at_birth"]
                                                  for c in later),
            "edges_accepted_in_the_run": sum(r["edges_accepted"] for r in d["records"]),
            "cases_they_decided": sum(c["cases_decided"] for c in later),
            "rows": later}


def profile(rules, corpus, space, tmask, listed: bool = True) -> dict:
    ids = [r["rule_id"] for r in rules]
    action = {r["rule_id"]: r["action"] for r in rules}
    conds = {r["rule_id"]: [Condition(c["attr"], c["op"], c["value"])
                            for c in r["conditions"]] for r in rules}
    ext = {rid: space.extension(conds[rid]) for rid in ids}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    pools = space_pools(ids, conds, action, below)
    return {
        "rules": len(ids),
        "empty_extension": sum(1 for rid in ids if not ext[rid]),
        "pairs": pair_census(ids, ext, below, action),
        "subsumption": {
            "corpus": subsumption_on_corpus(matched, undef, truth, action),
            "space": subsumption_on_space(pools["hibrido"][0], action, tmask,
                                          pools["hibrido"][3])},
        "bounds": bounds(ids, {"puro": matched, "hibrido": undef}, truth, action, pools),
        "copies": copies(rules, ext, action, listed),
    }


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def row(what, measured, published, owner) -> dict:
    return {"what": what, "measured": measured, "published": published,
            "owner": str(owner), "passes": measured == published}


def gate_hand_written(p: dict) -> list[dict]:
    pub = json.loads(PUBLISHED_HIDDEN.read_text())
    sub = pub["arbitration"]["subsumption"]
    space = [r for r in json.loads(PUBLISHED_HIDDEN_SPACE.read_text())["rows"]
             if r["surface"].startswith("exhaustive space")
             and r["arbitration"].startswith("subsumption alone")]
    if len(space) != 1:
        raise ValueError(f"{PUBLISHED_HIDDEN_SPACE}: the subsumption row over the "
                         "space is not where this gate reads it")
    space = space[0]
    c, s = p["subsumption"]["corpus"], p["subsumption"]["space"]
    return [
        row("nested pairs, of possible", [p["pairs"]["nested"], p["pairs"]["possible"]],
            [pub["order"]["ordered_pairs"], pub["order"]["possible_pairs"]], PUBLISHED_HIDDEN),
        row("subsumption on the corpus: decided, conflicts, right",
            [c["action"], c["conflict"], c["correct"]],
            [sub["action"], sub["conflict"], sub["correct"]], PUBLISHED_HIDDEN),
        row("subsumption over the space: decided, conflicts, impasses, right",
            [s["action"], s["conflict"], s["impasse"], s["correct"]],
            [space["action"], space["conflict"], space["impasse"], space["correct"]],
            PUBLISHED_HIDDEN_SPACE),
        row("the population: the declared edges", p["pairs"]["population"], N_DECLARED,
            "rung2/pair_judgement.py, N_DECLARED"),
    ]


def gate_rung1(p: dict) -> list[dict]:
    pub = json.loads(PUBLISHED_RUNG1.read_text())
    sub = pub["subsumption"]
    bnd = json.loads(PUBLISHED_BOUNDS.read_text())["bounds"]
    cop = json.loads(PUBLISHED_COPIES.read_text())
    c = p["subsumption"]["corpus"]
    mine_b = {k: [round(p["bounds"][k]["corpus"], 4), round(p["bounds"][k]["space"], 4)]
              for k in ("puro", "hibrido")}
    pub_b = {k: [bnd[k]["corpus"], bnd[k]["espacio"]] for k in ("puro", "hibrido")}
    mine_c = {k: [p["copies"][k]["groups"], p["copies"][k]["rules_in_groups"],
                  p["copies"][k]["pairs"]] for k in ("written", "covering")}
    pub_c = {k: [cop[k]["groups"], cop[k]["rules_in_groups"], cop[k]["pairs"]]
             for k in ("written", "covering")}
    return [
        row("nested pairs, of possible", [p["pairs"]["nested"], p["pairs"]["possible"]],
            [pub["ordered_pairs"], pub["possible_pairs"]], PUBLISHED_RUNG1),
        row("subsumption on the corpus: decided, conflicts, impasses, right",
            [c["action"], c["conflict"], c["impasse"], c["correct"]],
            [sub["action"], sub["conflict"], sub["impasse"], sub["correct"]],
            PUBLISHED_RUNG1),
        row("the population", p["pairs"]["population"], GATE_POPULATION,
            "rung2/pair_judgement.py, GATE_POPULATION"),
        row("coverage bounds, corpus and space, both pools", mine_b, pub_b,
            PUBLISHED_BOUNDS),
        row("copies, both definitions", mine_c, pub_c, PUBLISHED_COPIES),
    ]


def gate_records(bases: dict) -> list[dict]:
    return [row(f"{name}: its rules, against its record's n_rules", len(rules),
                json.loads(plan.run_path(rep).read_text())["metrics"]["n_rules"],
                plan.run_path(rep))
            for rep, (name, rules) in enumerate(bases.items(), start=1)]


def read_expectation(profiles: dict) -> list[dict]:
    out = []
    for clause, what, read, line, test in EXPECTED:
        lv = line(profiles)
        for name in BASES:
            v = read(profiles[name])
            out.append({"clause": clause, "base": name, "what": what,
                        "reading": v, "line": lv,
                        "holds": None if v is None else bool(test(v, lv))})
    return out


# ---------------------------------------------------------------------------

def measure(dry_run: bool = False):
    """The references and their gates, then, only if every gate passed and the
    run is not dry, the three bases."""
    t_start = time.time()
    corpus = generate_corpus(2000, seed=17)
    space = Space()
    tmask = space_truth_masks(space)
    profiles = {"hand_written": profile(hand_written(), corpus, space, tmask),
                "rung1": profile(from_record(RUNG1), corpus, space, tmask, listed=False)}
    gates = {"hand_written": gate_hand_written(profiles["hand_written"]),
             "rung1": gate_rung1(profiles["rung1"])}
    bases = {name: from_record(plan.run_path(rep))
             for rep, name in enumerate(BASES, start=1)}
    gates["records"] = gate_records(bases)
    passes = all(r["passes"] for rows in gates.values() for r in rows)
    if dry_run or not passes:
        return None, gates, passes
    for name, rules in bases.items():
        profiles[name] = profile(rules, corpus, space, tmask)
    payload = {
        "_env": environment(),
        "plan": str(plan.PLAN),
        "what": "the structure of PLAN_REUSE.md's three final bases, loaded whole "
                "from case 0, beside the hand-written policy and rung 1's base: "
                "pairs, subsumption alone, the coverage bounds and copies. The "
                "baseline for Stage E of PLAN_PAIRWISE.md §11. Zero API calls.",
        "provenance": PROVENANCE,
        "expectation_written_before_the_run": EXPECTATION,
        "what_the_drafter_had_seen": SEEN,
        "adjudicates_nothing": "no row of any plan is read here and none moves.",
        "surfaces": {"corpus": "the full corpus, 2,000 cases, seed 17",
                     "space": "the exhaustive space, 134,400 points, each once"},
        "loaded_whole": "every rule of a base present from case 0, as "
                        "harness/learned_subsumption.py loaded rung 1's. Not what "
                        "the loop decided as the base grew: FINDINGS_REUSE.md "
                        "owns that.",
        "gates": gates,
        "profiles": profiles,
        "expectation_read": read_expectation(profiles),
        "post_run": {
            "what": "the later copies of each run: the escalation each was born on, "
                    "the edges accepted there, and the cases it decided",
            "provenance": "ADDED AFTER THE FIRST RUN, which refuted clause 4 on "
                          "every base, to say what the copies are. It reads only "
                          "the run records and moves no reading above.",
            "vehicles": {name: vehicles(plan.run_path(rep))
                         for rep, name in enumerate(BASES, start=1)}},
        "seconds": round(time.time() - t_start, 1),
    }
    return _rounded(payload), gates, passes


def report(gates: dict, passes: bool) -> None:
    print("=" * 78)
    print("THE THREE BASES, READ FOR WHAT STAGE E WOULD CHANGE")
    print("=" * 78)
    print(f"  {describe()}")
    for group, rows in gates.items():
        for r in rows:
            print(f"  {'ok  ' if r['passes'] else 'FAIL'} {group:<13} {r['what']}")
            if not r["passes"]:
                print(f"         measured {r['measured']}\n         published {r['published']}")
    print(f"  gates: {'PASS' if passes else 'FAIL'}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true",
                    help="the gates only; profiles no base of the three, writes nothing")
    args = ap.parse_args(argv)
    if not args.dry_run:
        plan.refuse_unsigned(f"reuse/structure.py writes {RECORD}")
    payload, gates, passes = measure(dry_run=args.dry_run)
    report(gates, passes)
    if args.dry_run:
        return 0 if passes else 1
    if not passes:
        print("\nREFUSED: a gate failed; nothing of the three bases was read or written.")
        return 1

    print(f"\n  {'base':<14}{'rules':>6}{'nested':>9}{'overlap':>9}{'popul.':>8}"
          f"{'sub cov':>9}{'sub err':>9}{'pure':>8}{'hybrid':>8}{'gap':>8}{'copies':>8}")
    for name, p in payload["profiles"].items():
        c = p["subsumption"]["corpus"]
        err = "—" if c["silent_error"] is None else f"{c['silent_error']:.4f}"
        print(f"  {name:<14}{p['rules']:>6}{p['pairs']['nested_share']:>9.4f}"
              f"{p['pairs']['overlapping_share']:>9.4f}{p['pairs']['population']:>8}"
              f"{c['coverage']:>9.4f}{err:>9}{p['bounds']['puro']['corpus']:>8.4f}"
              f"{p['bounds']['hibrido']['corpus']:>8.4f}{p['bounds']['gap']['corpus']:>8.4f}"
              f"{sum(p['copies']['written']['pairs'].values()):>8}")
    print("  (corpus columns; the space is in the record)")

    print("\n  the expectation, written before the run:")
    for e in payload["expectation_read"]:
        mark = {True: "holds", False: "does not hold", None: "unreadable"}[e["holds"]]
        print(f"    ({e['clause']}) {e['base']:<9} {e['reading']!s:<10} against "
              f"{e['line']!s:<8} {mark}")

    print("\n  post-run: the later copies, the escalations they were born on, "
          "the edges accepted there:")
    for name, v in payload["post_run"]["vehicles"].items():
        print(f"    {name:<9} {v['later_copies']:>3} copies, born on {v['born_on']}, "
              f"{v['edges_accepted_at_their_births']} of the run's "
              f"{v['edges_accepted_in_the_run']} accepted edges, "
              f"{v['cases_they_decided']} cases decided")

    RECORD.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {RECORD}")
    return 0


def _rounded(x, places: int = 6):
    if isinstance(x, float):
        return round(x, places)
    if isinstance(x, dict):
        return {k: _rounded(v, places) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_rounded(v, places) for v in x]
    return x


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
