"""
WHY THE DECLARATIONS PUT BILLING_SPECIALIST LOW.
`corrections/declared.py` found that each L run's placement declarations,
gathered by pair of queues, choose one ranking, and that it orders the loop's
rules better than the base the loop installed. What it lacks is mostly the
queues of the billing tickets. It puts `BILLING_SPECIALIST` seventh of eight in
L r1 and L r3, where the best ranking of each run's rules, chosen with the
truth, puts it second and fifth. In L r2 both put it fifth. This reading asks
why. Either the answers that put the queue below another were wrong about the
two rules each placed, or they were right about them and wrong as a ranking,
which gives one direction to every pair of rules of two queues. Proposed by
the agent after `corrections/guard.py`, and asked for by Sergi on 2026-11-16.
Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE VOTES ON BILLING'S PAIRS
--------------------------------------------------------------------------
The votes are `corrections/declared.py`'s: each citation of a rule of another
queue, one a rule and side, is one vote, whatever the engine did with it. This
reading keeps those between `BILLING_SPECIALIST` and another queue. A vote **against**
the queue puts the other queue above it, and a vote **for** it puts it above.
Each vote is read for:
- **whose answer cast it**: the newborn's. It is billing's own where the
  newborn is a rule of billing, and the other queue's where it is not;
- **its two rules**, the one declared above and the one below, and whether one
  lies strictly inside the other. There rung 2's engine decides by containment,
  and the vote decides nothing;
- **their shared region** on the space, and its size;
- **the better rule**, as `rung3/edge_direction.py` reads it. Over the shared
  region, it counts the points whose true queue is each rule's queue, and the
  rule with more is the better. A vote names it or not. A region with as many
  of each, or none of either, has no better rule. It is read on the space, and
  on the corpus, where each of the 2,000 arrivals counts once;
- **where its shared region lies in the policy**. The policy's rules' regions
  are read under first match, as `manual/instrument.py`'s `hidden_regions`
  reads them. Three layers are counted:
  - **above billing's**: its security and severity-1 rules, `H01` to `H08`;
  - **billing's own**: `H09` to `H12`;
  - **below it**: `H13` to `H29`.
The votes between two other queues are read the same way, for comparison.

--------------------------------------------------------------------------
ITS PLACE
--------------------------------------------------------------------------
Each run's **declared ranking** is the one its declarations choose, as
`declared.json` keeps it. The queue is moved through its eight places, and the
other seven queues keep their declared order. Each ranking orders the run's
final base under `corrections/hierarchy.py`'s pulled construction.
- **Each order is read on the space**: the points it decides right, by true
  queue, and `BILLING_SPECIALIST`'s recall.
- **And on the corpus**, the same. Each arrival is decided by the first rule of
  the order that matches it and has no rule strictly inside it that does.
- **Its best place** is the place whose order decides the most of the space.
  Among places that tie, it is the one nearest its declared place, and the
  higher of two as near.
- **The path** to it passes one queue at each step. Each step is read for what
  it gains or loses on both surfaces, by true queue.
- **What the declared ranking lacks** is what the run's best ranking, as
  `hierarchy.json` keeps it, decides of the space, less what the declared
  ranking decides.

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
  5. **Every order read installs, on both surfaces.** It keeps containment,
     installs into a fresh rung 2 engine and closes no cycle. On the space, the
     engine and first match each decide what this reading reads. On the corpus,
     the engine decides what this reading reads.
  6. **The truth is the policy's.** The regions of the policy's rules partition
     the space, and each queue's points are the union of its rules' regions.
     Every arrival lies in one rule's region, and its label is that rule's
     queue.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 1, 2, 3 and 6 and writes
nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L r1 and L r3, each apart. These are the two runs where the
declared ranking puts `BILLING_SPECIALIST` seventh and the best ranking puts it
higher. **Against it** and **for it** are the votes on its pairs, as above.
**Strict** votes are those whose shared region has a better rule on the space.

  V1. **By the others.** Most votes against it were cast by the answers of
      other queues' newborns.
  V2. **Right where cast.** Of the strict votes against it, most name the
      better rule.
  V3. **Its place costs.** At its best place, the ranking decides more of the
      space than at its declared place, by more than half of what the declared
      ranking lacks.
  V4. **Right pair by pair, wrong as a ranking.** On the path to its best
      place, at least one step moves it above a queue and gains points of the
      space, though more of that pair's votes put the other queue above it than
      below it, and most of the pair's strict votes against it name the better
      rule.
  V5. **On the tickets too.** At its best place, the ranking decides more of
      the corpus than at its declared place.
  V6. **On small regions.** The votes against it stand, at their median, on a
      smaller shared region than the votes for it.

A clause that reads a missing value fails.

**The drafter's account.**
- **The policy puts two layers above billing's, and two exceptions inside it.**
  Security and severity 1 come first. In billing's own layer, enterprise
  clients go to `ACCOUNT_MANAGER`, and what is left after the specialist's two
  rules goes to `SELF_SERVICE_DEFLECT`. So on a broad billing rule, most other
  queues have a slice where the policy puts them above billing.
- **The answers put their newborn above the rules that hold its ticket**
  (`corrections/above.py`). In L every newborn is born at a ticket the base did
  not decide or decided wrongly. A broad billing rule, the queue's general line
  (`corrections/broad.py`), holds tickets of other queues, and the rules born
  there climb over it. So V1, trusted most, and V2.
- **The climbs stand on slices**: the billing tickets of severity 1, of
  enterprise clients, of the residue. The votes for it stand on the broad rules
  of the queues below billing's layer that held billing's tickets. So V6.
- **Billing's layer sits above most of the policy**: churn, product routing,
  deflection and the defaults. On the space each tier is a quarter of the
  points, and prior tickets run evenly from 0 to 20, so those regions are
  large. A ranking gives one direction to every pair of rules of two queues,
  and the votes, counted one a citation, give it to the slices. So the
  declared place costs, and a step the space pays for can pass a queue whose
  votes were right: V4, the bet.
- **V3 rests in L r3 on more than billing's own points.** There the best
  ranking's recall of the queue, 0.2866 against 0.1374, is 1,020 points of the
  space, and half of what the declared ranking lacks is 1,250. A move of the
  queue reaches past that only by what it does to the rules nested in billing's
  rules, or to other queues' points.
- **On the corpus**, severity 1, enterprise clients and the keyword are rare.
  A billing ticket of severity 3 or more with few prior tickets goes to
  self-service more often than on the space. V5 argues that what the space pays
  for carries to the arrivals. The standing note in `IDEAS.md` reads such an
  argument as evidence that the bet is too high: V5 is trusted least.

**The bet is V4.** **V1 is trusted most.** **V5 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole, the sections *A ranking of the queues as the
  order* and *The ranking the loop declared* among it. So `hierarchy.json`'s
  and `declared.json`'s figures: each run's declared and best ranking, what
  each decides, and the queues' recall under them;
- **`declared.json`'s votes by pair of queues**, read when its section was
  written: how many votes each pair cast each way, in every run. The item this
  reading answers says that in L r1 most votes on billing's pairs with
  `ONCALL_ESCALATION`, `ACCOUNT_MANAGER` and `SELF_SERVICE_DEFLECT` go against
  it;
- the hidden policy's rules, and the domain's grid and its sampling weights;
  and, computed for the account, `BILLING_SPECIALIST`'s 6,840 points of the
  space;
- **the record's form**: a born rule's answer, as `corrections/declared.py`
  reads it;
- **the reading's size and cost**, timed before this was written, printing no
  vote, no share and no place: L r1 read whole took 5.6 seconds, and its six
  gates passed;
- **gates 1, 2, 3 and 6**, which pass on the dry run.

**What the drafter had not seen**: whose answers cast the votes, which rules
they stand on, their shared regions, whether they name the better rule on
either surface, where they lie in the policy, and what any place of the queue
decides.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent after `corrections/guard.py`, and asked for
by Sergi on 2026-11-16. The expectation above was written and committed before
the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.billing --dry-run   # gates 1, 2, 3 and 6; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.billing
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Any, Sequence

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from manual import instrument as MI
from reasoned_loop import score as rl_score
from reuse import structure as st
from rung2.engine2 import EDGE_OK, Space
from rung3 import edge_direction as ED

from . import declared as DC
from . import forgotten as fg
from . import hierarchy as H
from . import plan
from . import shape as S

F = Fraction
L_RUNS = H.L_RUNS
READ = ("l_r1", "l_r3")            # the runs the clauses read
BILLING = "BILLING_SPECIALIST"
HIT, MISS, TIE, NEITHER = "a", "b", "tie", "neither_ever_right"   # rung3/edge_direction.py
LAYERS = ("above", "billing", "below")
ABOVE_LAST, BILLING_LAST = 8, 12   # H01..H08 above billing's layer, H09..H12 billing's own
PROVENANCE = (
    "POST-RUN: proposed by the agent after corrections/guard.py, and asked for by Sergi on "
    "2026-11-16. The expectation in the module's docstring was written and committed before "
    "the reading ran. Not a signed row; no verdict moves.")

frac = fg.frac
share = fg.share


# ---------------------------------------------------------------------------
# The two surfaces
# ---------------------------------------------------------------------------

@dataclass
class Surface:
    """A set of rules over a set of points: `ext[r]`, where `r` matches; `M[r]`,
    where it also has no rule strictly inside it that matches; `W[r]`, where it
    is also right; and each queue's points."""
    name: str
    n: int
    ext: dict[str, int]
    M: dict[str, int]
    W: dict[str, int]
    truth: dict[str, int]


def surface(name: str, ext: dict[str, int], action: dict[str, str],
            inside: dict[str, frozenset], truth: dict[str, int], n: int) -> Surface:
    M = S.undefeated(ext, inside)
    W = {r: m & truth.get(action[r], 0) for r, m in M.items()}
    return Surface(name=name, n=n, ext=dict(ext), M=M, W=W, truth=dict(truth))


def corpus_ext(rules: Sequence[Any]) -> dict[str, int]:
    """Each rule's arrivals, as a mask: bit `i` for the corpus's case `i`."""
    out = {r.rule_id: 0 for r in rules}
    for i, case in enumerate(MI.corpus()):
        bit = 1 << i
        for r in rules:
            if r.matches(case):
                out[r.rule_id] |= bit
    return out


def corpus_truth() -> dict[str, int]:
    out: dict[str, int] = {}
    for i, q in enumerate(MI.corpus_truth()):
        out[q] = out.get(q, 0) | (1 << i)
    return out


def right_mask(order: Sequence[str], sf: Surface) -> int:
    """The points an order decides right on a surface: each point by the first
    rule of the order whose `M` holds it. Under an order that keeps containment
    this is rung 2's engine's decision."""
    remaining, right = (1 << sf.n) - 1, 0
    for r in order:
        fires = sf.M[r] & remaining
        if fires:
            right |= sf.W[r] & fires
            remaining ^= fires
            if not remaining:
                break
    return right


@lru_cache(maxsize=None)
def layer_masks() -> dict[str, int]:
    """The policy's three layers over the space, from its rules' regions under
    first match."""
    out = {k: 0 for k in LAYERS}
    for rid, reg in MI.hidden_regions().items():
        k = int(rid[1:])
        out["above" if k <= ABOVE_LAST else "billing" if k <= BILLING_LAST else "below"] |= \
            reg["mask"]
    return out


# ---------------------------------------------------------------------------
# The votes, rule by rule
# ---------------------------------------------------------------------------

def vote_rows(decls: Sequence[dict[str, Any]], action: dict[str, str],
              inside: dict[str, frozenset], sp: Surface, co: Surface,
              layers: dict[str, int]) -> list[dict[str, Any]]:
    """Every vote between rules of two queues, read rule by rule: its rules, the
    side, whose answer, its shared region and the better rule on each
    surface."""
    out = []
    for d in decls:
        if d["ref_queue"] is None or d["ref_queue"] == d["queue"]:
            continue
        w, l = (d["rule"], d["ref"]) if d["side"] == "beats" else (d["ref"], d["rule"])
        wq, lq = action[w], action[l]
        shared, cshared = sp.ext[w] & sp.ext[l], co.ext[w] & co.ext[l]
        on_billing = BILLING in (wq, lq)
        mine = w if wq == BILLING else l
        other = l if mine == w else w
        out.append({
            "newborn": d["rule"], "cited": d["ref"], "side": d["side"], "verdict": d["verdict"],
            "winner": w, "loser": l, "billing": on_billing,
            "against": on_billing and wq != BILLING,
            "other_queue": action[other] if on_billing else None,
            "own_answer": d["queue"] == BILLING,
            "nested": w in inside[l] or l in inside[w],
            "shared": shared.bit_count(),
            "billing_larger": (on_billing
                               and sp.ext[mine].bit_count() > sp.ext[other].bit_count()),
            "space": ED.verdict((shared & sp.truth.get(wq, 0)).bit_count(),
                                (shared & sp.truth.get(lq, 0)).bit_count()),
            "corpus": ED.verdict((cshared & co.truth.get(wq, 0)).bit_count(),
                                 (cshared & co.truth.get(lq, 0)).bit_count()),
            "layers": {k: (shared & m).bit_count() for k, m in layers.items()},
        })
    return out


def tally(rows: Sequence[dict[str, Any]], key: str) -> dict[str, Any]:
    """Of `rows`, those whose shared region has a better rule on the surface
    `key`, and of those, how many name it."""
    strict = [r for r in rows if r[key] in (HIT, MISS)]
    named = sum(r[key] == HIT for r in strict)
    return {"votes": len(rows), "strict": len(strict), "named": named,
            "tie": sum(r[key] == TIE for r in rows),
            "neither": sum(r[key] == NEITHER for r in rows),
            "share": frac(share(named, len(strict)))}


def median_of(xs: Sequence[int]) -> Fraction | None:
    return rl_score.median([F(x) for x in xs]) if xs else None


def side(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """One side of billing's votes, read whole."""
    by_answer = Counter(r["newborn"] for r in rows)
    top = by_answer.most_common(1)
    return {"votes": len(rows),
            "by_answer": {"the_other_queues": sum(not r["own_answer"] for r in rows),
                          "its_own": sum(r["own_answer"] for r in rows)},
            "by_verdict": dict(sorted(Counter(r["verdict"] for r in rows).items())),
            "answers": len(by_answer),
            "largest_answer": {"newborn": top[0][0], "votes": top[0][1]} if top else None,
            "nested": sum(r["nested"] for r in rows),
            "billing_rule_larger": sum(r["billing_larger"] for r in rows),
            "shared_median": frac(median_of([r["shared"] for r in rows])),
            "space": tally(rows, "space"), "corpus": tally(rows, "corpus"),
            "layers": {k: sum(r["layers"][k] for r in rows) for k in LAYERS}}


def read_votes(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Billing's votes against it and for it, by the other queue, and the votes
    between two other queues beside them."""
    mine = [r for r in rows if r["billing"]]
    rest = [r for r in rows if not r["billing"]]
    by_queue = {}
    for q in ACTIONS:
        if q == BILLING:
            continue
        pair = [r for r in mine if r["other_queue"] == q]
        by_queue[q] = {"against": side([r for r in pair if r["against"]]),
                       "for": side([r for r in pair if not r["against"]])}
    return {"against": side([r for r in mine if r["against"]]),
            "for": side([r for r in mine if not r["against"]]),
            "by_queue": by_queue,
            "elsewhere": {"votes": len(rest), "space": tally(rest, "space"),
                          "corpus": tally(rest, "corpus")}}


# ---------------------------------------------------------------------------
# Its place
# ---------------------------------------------------------------------------

def moved(ranking: Sequence[str], place: int) -> tuple[str, ...]:
    """The ranking with billing at `place`, first to eighth, the other queues
    in their order."""
    others = [q for q in ranking if q != BILLING]
    return tuple(others[:place - 1] + [BILLING] + others[place - 1:])


def read_surface(right: int, sf: Surface) -> dict[str, Any]:
    of = sf.truth.get(BILLING, 0)
    return {"right": right.bit_count(), "share": frac(F(right.bit_count(), sf.n)),
            "by_queue": {q: (right & sf.truth.get(q, 0)).bit_count() for q in ACTIONS},
            "billing_recall": frac(share((right & of).bit_count(), of.bit_count()))}


def installs(order: Sequence[str], rules: dict[str, Any], rs: H.Rules, space: Space,
             on_space: int, on_corpus: int) -> bool:
    """Gate 5, for one order of every rule."""
    if sorted(order) != sorted(rules) or not S.is_linear_extension(order, rs.inside):
        return False
    eng = S.installed_in(order, rules, space)
    if any(why != EDGE_OK for _, _, why in eng.edge_log):
        return False
    return (MI.over_space(eng)["correct"] == on_space
            and MI.first_match_over_space([rules[r] for r in order])["correct"] == on_space
            and MI.over_corpus(eng)["correct"] == on_corpus)


def read_places(rs: H.Rules, ranking: Sequence[str], sp: Surface, co: Surface,
                rules: dict[str, Any], space: Space) -> tuple[dict[int, dict[str, Any]], bool]:
    """The queue at each of its eight places: each ranking's order read on both
    surfaces, and gate 5 for each."""
    out, ok = {}, True
    for p in range(1, len(ACTIONS) + 1):
        rk = moved(ranking, p)
        o = H.pulled(rs, H.rank_of(rk))
        s, c = right_mask(o, sp), right_mask(o, co)
        ok &= installs(o, rules, rs, space, s.bit_count(), c.bit_count())
        out[p] = {"ranking": list(rk), "space": read_surface(s, sp), "corpus": read_surface(c, co)}
    return out, bool(ok)


def best_place(places: dict[int, dict[str, Any]], declared: int) -> int:
    """The place of the most right points of the space, the nearest to the
    declared place among those that tie, and the higher of two as near."""
    top = max(x["space"]["right"] for x in places.values())
    return min((p for p, x in places.items() if x["space"]["right"] == top),
               key=lambda p: (abs(p - declared), p))


def path(places: dict[int, dict[str, Any]], ranking: Sequence[str], start: int,
         end: int) -> list[dict[str, Any]]:
    """The steps from `start` to `end`, one queue passed at each, and what each
    gains or loses on both surfaces."""
    others = [q for q in ranking if q != BILLING]
    out, p = [], start
    while p != end:
        up = end < p
        q = p - 1 if up else p + 1
        a, b = places[p], places[q]
        out.append({"from": p, "to": q, "passes": others[p - 2] if up else others[p - 1],
                    "up": up,
                    "space": b["space"]["right"] - a["space"]["right"],
                    "corpus": b["corpus"]["right"] - a["corpus"]["right"],
                    "by_queue": {k: b["space"]["by_queue"][k] - a["space"]["by_queue"][k]
                                 for k in ACTIONS
                                 if b["space"]["by_queue"][k] != a["space"]["by_queue"][k]}})
        p = q
    return out


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def truth_is_the_policy() -> bool:
    """Gate 6."""
    sp = MI.space()
    union, disjoint, by_queue = 0, True, {}
    label: dict[int, str] = {}
    once = True
    for reg in MI.hidden_regions().values():
        disjoint &= not (union & reg["mask"])
        union |= reg["mask"]
        by_queue[reg["queue"]] = by_queue.get(reg["queue"], 0) | reg["mask"]
        for i in reg["cases"]:
            once &= i not in label
            label[i] = reg["queue"]
    truth, ctruth = MI.space_truth(), MI.corpus_truth()
    return bool(disjoint and once and union == (1 << sp.n) - 1
                and all(by_queue.get(q, 0) == truth.get(q, 0) for q in ACTIONS)
                and len(label) == len(ctruth) == len(MI.corpus())
                and all(label[i] == y for i, y in enumerate(ctruth)))


def gate_six() -> dict[str, Any]:
    return {"gate": 6, "what": "the truth is the policy's", "passes": truth_is_the_policy()}


def chosen_median(rs: H.Rules, sp: Surface, perms: Sequence[tuple[str, ...]],
                  ks: Sequence[int]) -> tuple[str, ...]:
    """The median of the chosen rankings by what they decide, as
    `corrections/declared.py` picks it."""
    vals = sorted((right_mask(H.pulled(rs, H.rank_of(perms[k])), sp).bit_count(), k) for k in ks)
    return perms[vals[(len(vals) - 1) // 2][1]]


def read_run(tag: str, kept_declared: dict[str, Any], kept_hier: dict[str, Any],
             shape: dict[str, Any]) -> dict[str, Any]:
    record, _, _ = S.inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    engine = MI.final_engine(record)
    rs = H.rules_of(engine)
    rules = {r.rule_id: r for r in engine.rules}
    action = rs.action
    sp = surface("space", engine.ext, action, rs.inside, truth, space.n)
    co = surface("corpus", corpus_ext(engine.rules), action, rs.inside, corpus_truth(),
                 len(MI.corpus()))
    decls = DC.declarations(record)
    rows = vote_rows(decls, action, rs.inside, sp, co, layer_masks())
    # the rankings
    perms = H.rankings()
    _, ks = DC.chosen(DC.votes(decls), perms)
    ev = kept_declared["runs"][tag]["every_declaration"]
    declared = tuple(ev["orders"]["median"]["ranking"])
    best = kept_hier["runs"][tag]["loop"]["pulled"]["best"]
    declared_right = right_mask(H.pulled(rs, H.rank_of(declared)), sp).bit_count()
    best_right = right_mask(H.pulled(rs, H.rank_of(best["ranking"])), sp).bit_count()
    gate4 = (len(ks) == ev["rankings"] and chosen_median(rs, sp, perms, ks) == declared
             and declared_right == ev["orders"]["median"]["right"]
             and best_right == best["right"])
    # its place
    places, gate5 = read_places(rs, declared, sp, co, rules, space)
    p0 = declared.index(BILLING) + 1
    pstar = best_place(places, p0)
    steps = path(places, declared, p0, pstar)
    gap = best_right - declared_right
    gain = places[pstar]["space"]["right"] - places[p0]["space"]["right"]
    return {
        "votes": read_votes(rows),
        "place": {"declared_ranking": list(declared), "declared": p0, "best": pstar,
                  "best_ranking": list(best["ranking"]),
                  "best_ranking_place": list(best["ranking"]).index(BILLING) + 1,
                  "lacks": {"points": gap, "share": frac(F(gap, space.n))},
                  "gain": {"points": gain, "share": frac(F(gain, space.n)),
                           "of_what_it_lacks": frac(share(gain, gap))},
                  "corpus_gain": (places[pstar]["corpus"]["right"]
                                  - places[p0]["corpus"]["right"]),
                  "places": {str(p): x for p, x in places.items()},
                  "path": steps},
        "gates": [S.stage_c(tag), H.gate_two(tag, shape),
                  {"gate": 3, "what": "the declarations are the record's",
                   "passes": DC.edge_log_matches(record, decls)},
                  {"gate": 4, "what": "the rankings are the records'", "passes": bool(gate4)},
                  {"gate": 5, "what": "every order read installs, on both surfaces",
                   "passes": gate5},
                  gate_six()],
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(x: dict[str, Any] | None) -> Fraction | None:
    return None if x is None else F(x["fraction"])


def pair_votes(by_queue: dict[str, Any], q: str) -> tuple[int, int, int, int]:
    """For the pair of billing and `q`: votes against billing, for it, and of
    the strict votes against it, those naming the better rule and all."""
    x = by_queue[q]
    return (x["against"]["votes"], x["for"]["votes"],
            x["against"]["space"]["named"], x["against"]["space"]["strict"])


def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    got: dict[str, dict[str, Any]] = {}
    for t in READ:
        r = runs.get(t)
        if r is None:
            continue
        v, pl = r["votes"], r["place"]
        places = pl["places"]
        p0, ps = str(pl["declared"]), str(pl["best"])
        right_steps = []
        for s in pl["path"]:
            if not s["up"]:
                continue
            against, for_, named, strict = pair_votes(v["by_queue"], s["passes"])
            if s["space"] > 0 and against > for_ and 2 * named > strict:
                right_steps.append(s["passes"])
        got[t] = {"against": v["against"]["votes"],
                  "by_the_others": v["against"]["by_answer"]["the_other_queues"],
                  "named": v["against"]["space"]["named"],
                  "strict": v["against"]["space"]["strict"],
                  "gain": pl["gain"]["points"], "lacks": pl["lacks"]["points"],
                  "right_steps": right_steps,
                  "corpus_declared": places[p0]["corpus"]["right"],
                  "corpus_best": places[ps]["corpus"]["right"],
                  "median_against": value(v["against"]["shared_median"]),
                  "median_for": value(v["for"]["shared_median"])}
    every = bool(got) and len(got) == len(READ)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    v1 = each(lambda x: x["against"] > 0 and 2 * x["by_the_others"] > x["against"])
    v2 = each(lambda x: x["strict"] > 0 and 2 * x["named"] > x["strict"])
    v3 = each(lambda x: x["gain"] > 0 and 2 * x["gain"] > x["lacks"])
    v4 = each(lambda x: bool(x["right_steps"]))
    v5 = each(lambda x: x["corpus_best"] > x["corpus_declared"])
    v6 = each(lambda x: x["median_against"] is not None and x["median_for"] is not None
              and x["median_against"] < x["median_for"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "V1", "what": "in L r1 and in L r3, most votes against BILLING_SPECIALIST were "
                                 "cast by the answers of other queues' newborns",
         "reading": shown(("by_the_others", "against")), "holds": v1},
        {"clause": "V2", "what": "in L r1 and in L r3, of the strict votes against it, most name "
                                 "the better rule",
         "reading": shown(("named", "strict")), "holds": v2},
        {"clause": "V3", "what": "in L r1 and in L r3, at its best place the ranking decides more "
                                 "of the space than at its declared place, by more than half of "
                                 "what the declared ranking lacks",
         "reading": shown(("gain", "lacks")), "holds": v3},
        {"clause": "V4", "what": "in L r1 and in L r3, on the path to its best place, a step moves "
                                 "it above a queue and gains points of the space, though more of "
                                 "that pair's votes put the other queue above it, and most of the "
                                 "pair's strict votes against it name the better rule",
         "reading": shown(("right_steps",)), "holds": v4},
        {"clause": "V5", "what": "in L r1 and in L r3, at its best place the ranking decides more "
                                 "of the corpus than at its declared place",
         "reading": shown(("corpus_best", "corpus_declared")), "holds": v5},
        {"clause": "V6", "what": "in L r1 and in L r3, the votes against it stand, at their median, "
                                 "on a smaller shared region than the votes for it",
         "reading": shown(("median_against", "median_for")), "holds": v6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "billing.json"


def declared_record() -> dict[str, Any]:
    return json.loads(DC.record_path().read_text())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the declarations put BILLING_SPECIALIST low "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1, 2, 3 and 6 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/billing.py writes {record_path()}")
    kept_declared, kept_hier, shape = declared_record(), DC.hierarchy_record(), H.shape_record()
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
                   "run's placement declarations on BILLING_SPECIALIST's pairs read rule by "
                   "rule, and its final base ordered by its declared ranking with that queue "
                   "at each of its eight places, under corrections/hierarchy.py's pulled "
                   "construction",
        "constants": {"construction": "pulled", "read": list(READ),
                      "layers": {"above": "H01-H08", "billing": "H09-H12", "below": "H13-H29"},
                      "best_place": "the most right points of the space; among ties the "
                                    "nearest to the declared place, then the higher"},
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        v, pl = r["votes"], r["place"]
        print(f"  {t}: {v['against']['votes']} votes against, {v['for']['votes']} for; "
              f"declared place {pl['declared']}, best {pl['best']}, gaining "
              f"{pl['gain']['points']} of the {pl['lacks']['points']} points the declared "
              f"ranking lacks")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
