"""
WHETHER THE ORDER THE LOOP LACKS IS A RANKING OF THE QUEUES.
`corrections/shape.py` read each L run's final base in the best order rung 2's
engine can install. In L r1 and L r2 an order of the loop's own rules, found
with the truth, decides more of the space than at once: there the loop lost by
its order. Neither completing the base by birth nor searching it on its own
labels found that order. `IDEAS.md` leaves the levers to calls, the model asked
to order the loop's rules among them. Before any is paid for, this reading asks
whether the order the loop lacks is a ranking of the eight queues: one fixed
order between them, which an operator could give once, a few labels could fit,
or a model has already stated. There are 40,320, so every one is read.
Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/shape.py`. Free on the records. POST-RUN.

--------------------------------------------------------------------------
A RANKING, AS AN ORDER RUNG 2'S ENGINE CAN INSTALL
--------------------------------------------------------------------------
`rung3/queue_hierarchy_floor.py` sorts rules by their queue's rank, which rung
3's hybrid pool allows and rung 2's engine does not. There a rule strictly
inside another beats it wherever both match, so an order the engine installs
puts every such rule before the rule around it (`corrections/shape.py`). Where a
rule of a lower-ranked queue lies strictly inside one of a higher-ranked queue,
no such order keeps both the ranking and containment, and one of the two rules
leaves its rank's place. Two constructions place the pair, and both are read:
- **pulled**, the one the clauses read: each rule as early as its queue's rank
  and containment allow. The rules strictly inside it come just before it, in
  its rank's place. It is built from the back: the last place goes to the rule
  of the lowest-ranked queue that no unplaced rule lies around, ties to the
  latest born;
- **waiting**: each rule at its own queue's rank. A rule waits for every rule
  strictly inside it, and comes when it is the available rule of the highest
  rank. Kahn's algorithm, ties to the earliest born.
Where containment is silent both are `queue_hierarchy_floor`'s order, by rank
and then by birth, as `tests/test_corrections_hierarchy.py` pins. Pulled keeps
a broad rule's rank over its region, but for the rules nested in it. Waiting
keeps a nested rule's rank on its own region, and drags the broad rule down to
it.

Inside a queue the ties go by birth. Where containment is silent a tie-break
cannot change what the order decides, as `queue_hierarchy_floor` proves. Where
containment pulls a rule of one queue into another's place it can, and that is
not read.

Each order is read over the space by `corrections/shape.py`'s instance. The
points whose undefeated rules carry one queue are decided the same in every such
order, and the rest are read under first match.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
**Each L run's final base**, in the order of every ranking of the eight queues
under both constructions:
- **the best ranking**: the one that decides most of the space, the earliest in
  `itertools.permutations(ACTIONS)` on a tie. It is chosen with the truth, as
  `queue_hierarchy_floor`'s best is, and nothing without it can pick it;
- **the blind rankings**: the 40,320 as a distribution, and by the place each
  gives `SECURITY_INCIDENT`;
- **the rankings its labels choose**, under pulled: those that decide the most
  of the run's labels right, the reported errors with their true queues. It is
  what a loop that fitted a ranking to the labels it had would choose among.
  The set is read whole: its size, and the least, the median and the most of
  the space its rankings decide;
- **the rankings on record**, none of them read on these bases before:
  - **stated**: the 24 the model gave in `PLAN_RANKING.md`'s session, asked for
    the order that decides which queue wins a contested ticket, shown the
    queues' names alone; and their Borda count, which that plan's Stage C kept;
  - **revealed**: Copeland over the model's own pairwise answers about rung 1's
    learned base, as `PLAN_RANKING.md`'s Stage A kept it;
  - **Stage C's**: the ranking that best fits the answer key of the hidden
    policy's 170 labelled pairs, `rung3/queue_hierarchy_floor.py`'s. It reads
    the policy, on another object.

Set beside each run's figures in `results_corrections/shape.json`: the record,
completed, by its labels, with the truth, the bound, and at once.

**Each L run's three at-once answers at all labels**, under every ranking and
both constructions: each answer's best ranking, and the median of its 40,320.
A median over a run's answers is over its three.

**The hidden policy's own rules**, written as an answer as `G-g1` writes it,
under every ranking and both constructions: how far the policy itself lies from
a ranking, and what the rankings on record make of it.

Each order reported is read for its share of the space, its right points in the
keyword half and outside it, and every queue's recall.

**The three runs are read in three processes**, one each, and the hidden
policy's rules in the parent. Every reading is deterministic, and the record is
the one a single process writes, which `--processes 1` does.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's**, as `corrections/shape.py`'s gate 1 reads them.
  2. **The instances are `shape.json`'s.** For each L run's final base and each
     of its answers, the record's right points, the bound, and the order with
     the truth that `shape.json` keeps give, read on this reading's instance, the
     figures `shape.json` keeps.
  3. **Every order is one the engine installs.** Every order of every ranking,
     under both constructions, puts every rule strictly inside another before
     it. Every order reported, installed into a fresh rung 2 engine as `CR-d`
     installs an answer, closes no cycle, and the engine and first match each
     give it the share read.
  4. **The bound bounds.** No ranking's order decides more than its rules'
     bound.
  5. **Every ranking once.** Each set of rules is read under the 40,320
     distinct rankings of the eight queues, under each construction, and every
     ranking on record is one of them.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1 and 2, prints pass or
fail, and writes nothing. Gates 3 to 5 read the rankings, so they run with the
reading.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's runs, each apart, and every clause but Y6 reads pulled
alone. In run `r`, **at once**
is the median of its three answers' shares, `CR-d`'s `space(A(r))`, and
**with the truth** and **completed** are the loop's, all as `shape.json` keeps
them. **The best ranking** is the loop's base under its best ranking.

  Y1. **Room.** In every L run, the best ranking of the loop's rules decides
      less of the space than its rules with the truth.
  Y2. **A ranking is enough.** In L r1 and in L r2, the best ranking of the
      loop's rules decides more of the space than at once.
  Y3. **Security first.** In every L run, the best ranking of the loop's rules
      puts `SECURITY_INCIDENT` first.
  Y4. **The labels do not choose it.** In every L run, the rankings its labels
      choose decide, at their median, less of the space than at once.
  Y5. **The model's stated rankings.** In every L run, they decide, at their
      median, more of the space than the loop's base completed.
  Y6. **Pulled.** In L r1 and in L r2, the best ranking pulled decides more of
      the space than the best ranking waiting.

A clause that reads a missing value fails.

**The drafter's account.**
- **The policy is no ranking.** Its rules order some pairs of queues one way in
  one region and the other way in another, and the loop's 280-odd rules a run
  copy pieces of it. So one ranking falls short of an order chosen rule by
  rule: Y1.
- **What the order with the truth gains lies mostly in one region.** In L r1
  and L r2 it is mostly `SECURITY_INCIDENT`'s, in the keyword half
  (`shape.json`'s S5). One fact decides it: that queue above every queue whose
  rules cross the keyword's. A ranking carries that fact whole: Y3, and Y2
  where the loop's rules leave room. In L r3 they leave none, since no order of
  them reaches at once, so Y2 reads L r1 and L r2.
- **Outside the keyword half a ranking replaces the loop's own declarations**,
  where the policy's orders are the ones no ranking keeps. What a ranking gains
  in the keyword half it may lose outside it: Y2 is the bet.
- **The labels are tickets of the corpus**, and few lie in the keyword half.
  So they say little of where `SECURITY_INCIDENT` goes, and the rankings they
  choose spread over its places: Y4. In L r3 it cannot fail, for the reason
  above.
- **The model's stated rankings put `SECURITY_INCIDENT` first**, all 24. All
  but two put `T1_GENERAL` above `BILLING_SPECIALIST` and `ACCOUNT_MANAGER`,
  where the policy sends billing tickets before its general rules. And
  `PLAN_RANKING.md` found the stated order worth less than a blind one on rung
  1's rules, on the corpus. What they gain in the keyword half they may give
  back outside: Y5.
- **The loop nests rules of other queues in `SECURITY_INCIDENT`'s region**
  (`FINDINGS_CORRECTIONS.md`, *Shape or order*, section 3). Under waiting the
  queue's rule waits for each of them, behind the rules of the queues ranked
  between. Pulled keeps it in its place: Y6, in the runs where the loop lost by
  its order.

**The bet is Y2.** **Y1 is trusted most.** **Y5 is trusted least**: one
ranking for the whole space, given without a rule in sight.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the section *Shape or order* among it, and
  so `shape.json`'s figures for each run: at once, the record, completed, by
  its labels, with the truth and the bound, and where each bound falls short;
- **the hidden policy's rules**, written as an answer. No ranking keeps them
  all: `ACCOUNT_MANAGER` comes before `BILLING_SPECIALIST` at the billing
  tickets of enterprise clients and after it at those of business clients with
  eight prior tickets or more (rules 8, 9 and 13, from 0). The same holds of
  `T3_ENGINEERING` and `ACCOUNT_MANAGER` (5, 12, 13 and 14), and of
  `T2_TECHNICAL` and `SELF_SERVICE_DEFLECT` (20, 24 and 26);
- **the rankings on record**, which are this reading's inputs. There are six
  distinct stated rankings. Fourteen asks gave the one that is also their
  Borda count: `SECURITY_INCIDENT`, `ONCALL_ESCALATION`, `T3_ENGINEERING`,
  `T2_TECHNICAL`, `T1_GENERAL`, `BILLING_SPECIALIST`, `ACCOUNT_MANAGER`,
  `SELF_SERVICE_DEFLECT`. The revealed ranking puts `ONCALL_ESCALATION` first
  and `SECURITY_INCIDENT` second. Stage C's puts `SECURITY_INCIDENT` first and
  `T1_GENERAL` last;
- **the labels in the keyword half**: 4, 5 and 13 of L r1's, L r2's and L r3's,
  counted when `corrections/shape.py` was read and kept in no record;
- **the reading's size and cost**, timed before this was written, printing no
  share and no score:
  - L r1's final base has 282 rules, 235 of them searched, and 2,812 pairs of
    rules one strictly inside the other;
  - one ranking, under both constructions, with the labels and the check of
    gate 3, took about 4 ms there, so the 40,320 take about three minutes;
  - an at-once answer of 48 rules, and the policy's 29, took about 0.4 ms a
    ranking. One install of gate 3 took 0.3 seconds;
- `rung3/queue_hierarchy_floor.py`, `ranking/plan.py`, and the records the
  rankings are read from.

**What the drafter had not seen**: any ranking's order read on any of these
rules or on the policy's, so no share, no best ranking, and no ranking chosen by
the labels.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/shape.py`. The expectation above was written and committed before
the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.hierarchy --dry-run   # gates 1 and 2; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.hierarchy
"""

from __future__ import annotations

import argparse
import heapq
import itertools
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from multiprocessing import get_context
from typing import Any, Callable, Sequence

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from manual import compile as MC
from manual import gates as MG
from manual import instrument as MI
from ranking import plan as RP
from reasoned_loop import score as rl_score
from reuse import structure as st
from rung2.engine2 import PriorityEngine, Space
from rung3 import local_search as LS
from rung3.queue_hierarchy_floor import STAGE_C_HIERARCHY

from . import ask
from . import forgotten as fg
from . import layer as LY
from . import plan
from . import shape as S

F = Fraction
L_RUNS = LY.L_RUNS
SECURITY = "SECURITY_INCIDENT"
PROCESSES = 3
N_RANKINGS = 40320                 # 8!
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/shape.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

median = rl_score.median
frac = fg.frac


# ---------------------------------------------------------------------------
# A ranking, as an order rung 2's engine can install
# ---------------------------------------------------------------------------

@dataclass
class Rules:
    """A set of rules as the constructions read them: every rule by birth, its
    queue, its birth, and containment as rung 2's engine computed it."""
    ids: list[str]
    action: dict[str, str]
    born: dict[str, tuple[int, str]]
    inside: dict[str, frozenset]
    around: dict[str, frozenset]


def rules_of(engine: PriorityEngine) -> Rules:
    inside, around = S.containment(engine)
    ordered = sorted(engine.rules, key=lambda r: (r.born_at, r.rule_id))
    return Rules(ids=[r.rule_id for r in ordered],
                 action={r.rule_id: r.action for r in ordered},
                 born={r.rule_id: (r.born_at, r.rule_id) for r in ordered},
                 inside=inside, around=around)


def rank_of(ranking: Sequence[str]) -> dict[str, int]:
    if sorted(ranking) != sorted(ACTIONS):
        raise ValueError(f"not a ranking of the eight queues: {list(ranking)}")
    return {q: i for i, q in enumerate(ranking)}


def pulled(rs: Rules, rank: dict[str, int]) -> list[str]:
    """Each rule as early as its queue's rank and containment allow, the rules
    strictly inside it just before it. Built from the back: the last place goes
    to the rule of the lowest-ranked queue that no unplaced rule lies around,
    ties to the latest born. Where containment is silent, by rank and then by
    birth."""
    late = sorted(rs.ids, key=lambda r: (rank[rs.action[r]], rs.born[r]))
    pos = {r: i for i, r in enumerate(late)}
    left = {r: len(rs.around[r]) for r in rs.ids}
    heap = [(-pos[r], r) for r in rs.ids if left[r] == 0]
    heapq.heapify(heap)
    back: list[str] = []
    while heap:
        _, r = heapq.heappop(heap)
        back.append(r)
        for b in rs.inside[r]:
            left[b] -= 1
            if left[b] == 0:
                heapq.heappush(heap, (-pos[b], b))
    if len(back) != len(rs.ids):
        raise ValueError("containment has a cycle: no order of these rules respects it")
    back.reverse()
    return back


def waiting(rs: Rules, rank: dict[str, int]) -> list[str]:
    """Each rule at its own queue's rank: Kahn's algorithm over containment, the
    available rule of the highest-ranked queue first, ties to the earliest born.
    A rule waits for every rule strictly inside it."""
    return S.topological(rs.ids, rs.inside, {r: (rank[rs.action[r]], rs.born[r]) for r in rs.ids})


BUILD: dict[str, Callable[[Rules, dict[str, int]], list[str]]] = {
    "pulled": pulled, "waiting": waiting}
CONSTRUCTIONS = tuple(BUILD)


def rankings() -> list[tuple[str, ...]]:
    """Every ranking of the eight queues, in `itertools.permutations(ACTIONS)`'s
    order, which breaks every tie in this reading."""
    return list(itertools.permutations(ACTIONS))


def scores_of(rs: Rules, inst: S.Instance, perms: Sequence[tuple[str, ...]],
              labels: tuple[dict[str, int], dict[str, int], int] | None = None
              ) -> dict[str, Any]:
    """Each ranking's order under each construction, its right points over the
    space, and, under pulled and where labels are given, its right labels. Also
    whether every order puts every rule strictly inside another before it."""
    out: dict[str, Any] = {c: [] for c in CONSTRUCTIONS}
    right_labels: list[int] = []
    linear = True
    for perm in perms:
        rank = rank_of(perm)
        for c, build in BUILD.items():
            o = build(rs, rank)
            linear = linear and S.is_linear_extension(o, rs.inside)
            out[c].append(inst.score(inst.searched(o)))
            if c == "pulled" and labels is not None:
                right_labels.append(LS.score_order(o, *labels))
    out["labels"] = right_labels if labels is not None else None
    out["linear"] = linear
    return out


# ---------------------------------------------------------------------------
# What the rankings decide, summed up
# ---------------------------------------------------------------------------

def share_of(right: int, n: int) -> dict[str, Any]:
    return frac(F(right, n))


def spread(values: Sequence[int], n: int) -> dict[str, Any]:
    """The least, a quarter, the median, three quarters, the most and the mean
    of a set of right points, as shares of the space. The quarters are the
    sorted values at `len // 4` and `3 * len // 4`."""
    s = sorted(values)
    m = len(s)
    return {"of": m, "least": share_of(s[0], n), "quarter": share_of(s[m // 4], n),
            "median": frac(F(s[(m - 1) // 2] + s[m // 2], 2 * n)),
            "three_quarters": share_of(s[(3 * m) // 4], n), "most": share_of(s[-1], n),
            "mean": frac(F(sum(s), m * n))}


def best_index(values: Sequence[int]) -> int:
    """The earliest ranking of the most right points."""
    top = max(values)
    return next(k for k, v in enumerate(values) if v == top)


def by_place(values: Sequence[int], perms: Sequence[tuple[str, ...]], n: int,
             queue: str = SECURITY) -> dict[str, Any]:
    """The rankings grouped by the place they give `queue`, first to eighth."""
    groups: dict[int, list[int]] = {}
    for v, perm in zip(values, perms):
        groups.setdefault(perm.index(queue) + 1, []).append(v)
    return {str(p): {"median": spread(vs, n)["median"], "most": share_of(max(vs), n)}
            for p, vs in sorted(groups.items())}


def read_order(rs: Rules, inst: S.Instance, ranking: Sequence[str], construction: str,
               rules, space: Space, truth: dict[str, int]) -> tuple[dict[str, Any], bool]:
    """One ranking's order, read for its share, halves and recall, and gate 3's
    install for it."""
    o = BUILD[construction](rs, rank_of(ranking))
    got = S.reading(inst.right(inst.searched(o)), space, truth)
    ok = S.installs(o, rules, inst, space)
    return {"ranking": list(ranking), "construction": construction, **got}, ok


def on_record() -> dict[str, Any]:
    """The rankings `PLAN_RANKING.md` and rung 3 keep: the model's 24 stated
    rankings, in its session's order, and their Borda count; its revealed
    ranking; and Stage C's."""
    session = json.loads(RP.ask_path("session").read_text())
    sample = json.loads(RP.SAMPLE_PATH.read_text())
    score = json.loads(RP.SCORE_PATH.read_text())
    stated = [{"pid": r["pid"], "pass": r["pass"], "ranking": tuple(r["ranking"])}
              for r in session["rows"] if r["valid"]]
    return {"stated": stated,
            "borda": tuple(score["M-f"]["borda"]["order"]),
            "revealed": tuple(sample["revealed"]["learned"]["order"]),
            "stage_c": tuple(STAGE_C_HIERARCHY),
            "stage_c_as_sample_keeps_it": tuple(sample["stage_c"]["order"])}


def named_rankings(record: dict[str, Any]) -> dict[str, tuple[str, ...]]:
    """Each distinct ranking on record, by name: the stated ones by first ask."""
    out: dict[str, tuple[str, ...]] = {}
    for x in record["stated"]:
        if x["ranking"] not in out.values():
            out[f"stated {x['pid']} pass {x['pass']}"] = x["ranking"]
    for k in ("borda", "revealed", "stage_c"):
        out[k] = record[k]
    return out


def read_rules(engine: PriorityEngine, space: Space, truth: dict[str, int],
               record: dict[str, Any], perms: Sequence[tuple[str, ...]],
               labels: Sequence[tuple[int, str]] | None = None,
               named: bool = True) -> dict[str, Any]:
    """One set of rules under every ranking: the best under each construction,
    the blind rankings, the rankings on record where `named`, and the rankings
    its labels choose where it has labels; gates 3 to 5 for it."""
    rs = rules_of(engine)
    rules = {r.rule_id: r for r in engine.rules}
    inst = S.instance(engine.rules, engine.ext, rs.inside, rs.around, truth, space.n)
    n = space.n
    lab = S.label_masks(engine, labels, rs.inside) if labels is not None else None
    got = scores_of(rs, inst, perms, lab)
    index = {p: k for k, p in enumerate(perms)}
    bound = S.coverage(inst)
    installs = True
    out: dict[str, Any] = {"rules": len(rs.ids), "searched": len(inst.ids),
                           "contested": inst.full.bit_count(), "fixed_right": inst.fixed,
                           "bound": {"share": share_of(bound, n), "right": bound}}
    for c in CONSTRUCTIONS:
        vals = got[c]
        k = best_index(vals)
        best, ok = read_order(rs, inst, perms[k], c, rules, space, truth)
        installs &= ok
        out[c] = {"best": {**best, "index": k,
                           "rankings_at_it": sum(v == vals[k] for v in vals)},
                  "blind": spread(vals, n),
                  "by_place_of_security": by_place(vals, perms, n)}
    if named:
        rows = {}
        for name, ranking in named_rankings(record).items():
            k = index[ranking]
            row, ok = read_order(rs, inst, ranking, "pulled", rules, space, truth)
            installs &= ok
            rows[name] = {**row, "waiting": share_of(got["waiting"][k], n)}
        stated = [{"pid": x["pid"], "pass": x["pass"],
                   **{c: share_of(got[c][index[x["ranking"]]], n) for c in CONSTRUCTIONS}}
                  for x in record["stated"]]
        out["on_record"] = {
            "rankings": rows,
            "stated": {"asks": stated, **{c: spread([got[c][index[x["ranking"]]]
                                                     for x in record["stated"]], n)
                                           for c in CONSTRUCTIONS},
                       "distinct": len({x["ranking"] for x in record["stated"]})}}
    if labels is not None:
        lv = got["labels"]
        top = max(lv)
        chosen = [k for k, v in enumerate(lv) if v == top]
        vals = sorted(((got["pulled"][k], k) for k in chosen))
        picks = {"least": vals[0][1], "median": vals[(len(vals) - 1) // 2][1],
                 "most": vals[-1][1]}
        reads = {}
        for name, k in picks.items():
            row, ok = read_order(rs, inst, perms[k], "pulled", rules, space, truth)
            installs &= ok
            reads[name] = {**row, "index": k}
        out["by_its_labels"] = {
            "labels": {"of": len(labels), "right": top},
            "rankings": len(chosen),
            "shares": spread([v for v, _ in vals], n),
            "security_first": sum(perms[k][0] == SECURITY for k in chosen),
            "by_place_of_security": {str(p): sum(perms[k].index(SECURITY) + 1 == p for k in chosen)
                                     for p in range(1, 9)},
            "orders": reads}
    out["gates"] = {
        "installs": bool(got["linear"] and installs),
        "bound_bounds": all(max(got[c]) <= bound for c in CONSTRUCTIONS),
        "every_ranking_once": (len(perms) == N_RANKINGS == len(set(perms))
                               and all(len(got[c]) == N_RANKINGS for c in CONSTRUCTIONS))}
    return out


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def shape_record() -> dict[str, Any]:
    return json.loads(S.record_path().read_text())


def same_as_shape(engine: PriorityEngine, kept: dict[str, Any], space: Space,
                  truth: dict[str, int]) -> bool:
    """Gate 2, for one set of rules: its record's right points, its bound, and
    the order with the truth `shape.json` keeps, read on this instance."""
    inside, around = S.containment(engine)
    inst = S.instance(engine.rules, engine.ext, inside, around, truth, space.n)
    order = kept["orders"]["with_the_truth"]
    return (MI.right_mask(engine).bit_count() == kept["record"]["right"]
            and S.coverage(inst) == kept["bound"]["right"]
            and sorted(order) == sorted(r.rule_id for r in engine.rules)
            and inst.score(inst.searched(order)) == kept["with_the_truth"]["right"])


def gate_two(tag: str, shape: dict[str, Any] | None = None) -> dict[str, Any]:
    shape = shape_record() if shape is None else shape
    record, session, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    kept = shape["runs"][tag]
    ok = same_as_shape(MI.final_engine(record), kept["loop"], space, truth)
    answers = S.answers_at_all(session, len(ask.labelled(record)))
    ok &= len(answers) == len(kept["at_once"])
    for (k, row), a in zip(answers, kept["at_once"]):
        ok &= k == a["k"] and same_as_shape(LY.installed(row["payload"]).engine, a, space, truth)
    return {"gate": 2, "what": "the instances are shape.json's", "passes": bool(ok)}


def read_run(tag: str) -> dict[str, Any]:
    """One L run: its final base and its three at-once answers at all labels,
    each read under every ranking, with gates 1 to 5. It runs in a process of
    its own."""
    record, session, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    perms = rankings()
    kept = on_record()
    labels = ask.labelled(record)
    loop = read_rules(MI.final_engine(record), space, truth, kept, perms, labels=labels)
    answers = S.answers_at_all(session, len(labels))
    asks = [{"k": k, **read_rules(LY.installed(row["payload"]).engine, space, truth, kept, perms,
                                  named=False)} for k, row in answers]
    g = {"installs": True, "bound_bounds": True, "every_ranking_once": True}
    for x in [loop, *asks]:
        for key in g:
            g[key] &= x["gates"][key]
    on_list = all(r in set(perms) for r in named_rankings(kept).values())
    gates = [S.stage_c(tag), gate_two(tag),
             {"gate": 3, "what": "every order is one the engine installs", "passes": g["installs"]},
             {"gate": 4, "what": "the bound bounds", "passes": g["bound_bounds"]},
             {"gate": 5, "what": "every ranking once, and every ranking on record among them",
              "passes": g["every_ranking_once"] and on_list
              and kept["stage_c"] == kept["stage_c_as_sample_keeps_it"]}]

    def med(get) -> dict[str, Any] | None:
        return frac(median([F(get(a)["fraction"]) for a in asks])) if asks else None

    return {"labels": len(labels), "loop": loop, "at_once": asks,
            "at_once_median": {
                "best_pulled": med(lambda a: a["pulled"]["best"]["share"]),
                "best_waiting": med(lambda a: a["waiting"]["best"]["share"]),
                "blind_pulled": med(lambda a: a["pulled"]["blind"]["median"])},
            "gates": gates}


def read_policy(space: Space, truth: dict[str, int]) -> dict[str, Any]:
    """The hidden policy's own rules, written as an answer as `G-g1` writes it,
    under every ranking."""
    engine = MC.install(MG.hidden_answer(), space).engine
    return read_rules(engine, space, truth, on_record(), rankings())


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(x: dict[str, Any] | None) -> Fraction | None:
    return None if x is None else F(x["fraction"])


def read_expectation(runs: dict[str, dict[str, Any]], shape: dict[str, Any]
                     ) -> list[dict[str, Any]]:
    got: dict[str, dict[str, Any]] = {}
    for t in L_RUNS:
        r, sh = runs.get(t), shape["runs"].get(t)
        if r is None or sh is None:
            continue
        lp, sl = r["loop"], sh["loop"]
        got[t] = {"at_once": value(sh["at_once_median"]["record"]),
                  "completed": value(sl["completed"]["share"]),
                  "with_the_truth": value(sl["with_the_truth"]["share"]),
                  "best": value(lp["pulled"]["best"]["share"]),
                  "best_waiting": value(lp["waiting"]["best"]["share"]),
                  "best_first": lp["pulled"]["best"]["ranking"][0],
                  "labels_median": value(lp["by_its_labels"]["shares"]["median"]),
                  "stated_median": value(lp["on_record"]["stated"]["pulled"]["median"])}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    def both(test) -> bool:
        return all(t in got and test(got[t]) for t in ("l_r1", "l_r2"))

    def known(*keys):
        return lambda x: all(x[k] is not None for k in keys)

    y1 = each(lambda x: known("best", "with_the_truth")(x) and x["best"] < x["with_the_truth"])
    y2 = both(lambda x: known("best", "at_once")(x) and x["best"] > x["at_once"])
    y3 = each(lambda x: x["best_first"] == SECURITY)
    y4 = each(lambda x: known("labels_median", "at_once")(x) and x["labels_median"] < x["at_once"])
    y5 = each(lambda x: known("stated_median", "completed")(x)
              and x["stated_median"] > x["completed"])
    y6 = both(lambda x: known("best", "best_waiting")(x) and x["best"] > x["best_waiting"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "Y1", "what": "in every L run, the best ranking of the loop's rules decides less "
                                 "of the space than its rules with the truth",
         "reading": shown(("best", "with_the_truth")), "holds": y1},
        {"clause": "Y2", "what": "in L r1 and in L r2, the best ranking of the loop's rules decides "
                                 "more of the space than at once",
         "reading": shown(("best", "at_once")), "holds": y2},
        {"clause": "Y3", "what": "in every L run, the best ranking of the loop's rules puts "
                                 "SECURITY_INCIDENT first",
         "reading": shown(("best_first",)), "holds": y3},
        {"clause": "Y4", "what": "in every L run, the rankings its labels choose decide, at their "
                                 "median, less of the space than at once",
         "reading": shown(("labels_median", "at_once")), "holds": y4},
        {"clause": "Y5", "what": "in every L run, the model's stated rankings decide, at their "
                                 "median, more of the space than the loop's base completed",
         "reading": shown(("stated_median", "completed")), "holds": y5},
        {"clause": "Y6", "what": "in L r1 and in L r2, the best ranking pulled decides more of the "
                                 "space than the best waiting",
         "reading": shown(("best", "best_waiting")), "holds": y6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "hierarchy.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Whether the order the loop lacks is a ranking of "
                                             "the queues (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 and 2 and stop; writes nothing")
    ap.add_argument("--processes", type=int, default=PROCESSES,
                    help="processes to read the runs in, one run each; 1 reads them in this "
                         "one. The record is the same")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/hierarchy.py writes {record_path()}")
    shape = shape_record()
    if args.dry_run:
        ones = [{"run": t, **g} for t in L_RUNS for g in (S.stage_c(t), gate_two(t, shape))]
        for g in ones:
            print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
                  f"  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    space, truth = MI.space(), MI.space_truth()
    if args.processes > 1:
        with get_context("fork").Pool(min(args.processes, len(L_RUNS))) as pool:
            pending = pool.map_async(read_run, L_RUNS)
            policy = read_policy(space, truth)
            runs = dict(zip(L_RUNS, pending.get()))
    else:
        runs = {t: read_run(t) for t in L_RUNS}
        policy = read_policy(space, truth)
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]] + [
        {"gate": g, "run": "the hidden policy", "what": w, "passes": policy["gates"][k]}
        for g, k, w in ((3, "installs", "every order is one the engine installs"),
                        (4, "bound_bounds", "the bound bounds"),
                        (5, "every_ranking_once", "every ranking once"))]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(runs, shape)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"shape": str(S.record_path()),
                   "shape_from": shape["_env"].get("git_commit"),
                   "score": str(plan.score_path()),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)},
                   "sessions": {t: str(LY.session_path(t)) for t in L_RUNS},
                   "rankings": {"stated": str(RP.ask_path("session")),
                                "borda": f"{RP.SCORE_PATH} :: M-f.borda.order",
                                "revealed": f"{RP.SAMPLE_PATH} :: revealed.learned.order",
                                "stage_c": "rung3/queue_hierarchy_floor.py :: STAGE_C_HIERARCHY"}},
        "surface": "the whole space, 134,400 points: each L run's final base and its three "
                   "at-once answers at all labels, as CR-d reads them, and the hidden policy's "
                   "own rules, each in the order of every ranking of the eight queues that "
                   "rung 2's engine can install, under two constructions",
        "constants": {"rankings": N_RANKINGS, "constructions": list(CONSTRUCTIONS),
                      "processes": args.processes},
        "gates": checked,
        "runs": runs,
        "policy": policy,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        lp = r["loop"]
        print(f"  {t}: best ranking pulled {lp['pulled']['best']['share']['value']:.4f}, "
              f"waiting {lp['waiting']['best']['share']['value']:.4f}; blind median "
              f"{lp['pulled']['blind']['median']['value']:.4f}; by its labels, median "
              f"{lp['by_its_labels']['shares']['median']['value']:.4f}; stated, median "
              f"{lp['on_record']['stated']['pulled']['median']['value']:.4f}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
