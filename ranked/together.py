"""
WHY BILLING'S COPIES DECLARED SIDES THE BASE COULD NOT HOLD TOGETHER.
`FINDINGS_RANKED.md`, *One thing the losses first left free*, P, found that L r2
lost under the copies' losses first through two of billing's copies, `R0143`
and `R0234`. Their answers put them below the keyword's rules and above
deflection's, while deflection's rules already reached rules the copies declared
themselves below. So the base could not hold both kinds of side of either
answer: the record kept the wins and refused the losses, and the replay did the
reverse. Its *What it does not settle*, first item, asks why the copies declared
such sides, and says that their reasoning is in the records. `IDEAS.md` carries
the item under *What `PLAN_RANKED.md` opens*. Asked for by Sergi on 2026-11-21.
POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`: the rules in birth
order, every edge each birth tried with the engine's verdict, and at every
escalation the round's list and the placement answer with its reasoning.
**`copies.json`**, whose rows give every copy with its originals.
**`sides.json`**, whose rows give every refused side of a copy with what closed
its cycle. **`lost.json`**, whose L r2 edges that carry the most lost points
name the two copies.

**A side** is an edge a birth tried. Its rule, **the newborn**, is at one end:
a `win` when the newborn's answer declared it above the other rule, a `loss`
when below.

**A pair** of a birth is one win, the newborn `N` above `D`, and one loss, `U`
above `N`, read in the base right before the birth tried its first edge, with
`N` in it:
- **neither closes a cycle alone**: `D` does not reach `N`, and `N` does not
  reach `U`;
- **`D` reaches `U`**, by what beats what: containment, a rule nested in
  another beating it, and declared edges.

So the base cannot hold both sides: either, installed, closes the other into a
cycle. The loop installs a birth's wins before its losses, so the record
installs the win and refuses the loss (gate 3). **A rule the answer cited on
both sides**, `D` = `U`, is the answer's own contradiction. It is counted apart
and kept out of the pairs.

**Each pair is read in that base**:
- **The sides' verdicts.** The policy's verdict on each side over the points its
  two rules share, `right`, `wrong` or `even`, as `corrections/paths.py`'s
  `verdict` reads one. **Both right** when both are `right`.
- **What holds `D` above `U`.** The steps of the paths from `D` to `U`, each
  `nested` or `declared`, with the policy's verdict on it.
  - **A wrong step carries it** when `D` no longer reaches `U` with every step
    the policy calls wrong taken out.
  - **A wrong declared step carries it** when the same holds with the wrong
    declared steps alone taken out.
- **Where the cycle is.** `somewhere` when some path from `D` to `U` runs
  through rules that all match a point `N`, `D` and `U` all match; `nowhere`
  otherwise, as when `D` and `U` share no point.
- **A door** is a step every path passes through. A declared door comes with
  the birth that installed it.
- **Across the keyword's half** when `D` matches no point of it and `U` matches
  only points of it.
- **What the round showed.** The round lists each rule with its own accepted
  sides, its `beats` and its `loses_to`, and shows nothing of containment.
  - **A step is shown** when it is declared and the list shows it: the upper
    rule listed with the lower among its `beats`, or the lower listed with the
    upper among its `loses_to`.
  - **The pair is shown** when some path from `D` to `U` has every step shown.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  (a) **How many.** In each run, the copies' births that tried a side, those
      that tried a win and a loss, and those with a pair; their pairs, and the
      losses and wins the pairs hold; and the rules cited on both sides. The
      same for the other births. The copies' pairs by the queues of `D` and
      `U`.
  (b) **Were the sides right.** The pairs by the verdict on each side, and
      those with both right.
  (c) **What held `D` above `U`.** The pairs by whether a wrong step carries
      every path, and a wrong declared step; by where the cycle is; by whether
      a door carries every path; and those across the keyword's half. The doors
      that carry the most of the copies' pairs, with their kind, their verdict,
      and the birth that installed a declared one.
  (d) **What the round showed.** The pairs the round showed.
  (e) **The two copies.** `R0143` and `R0234`, in L r2.
      - **Each pair**, with one shortest path from `D` to `U`, and every step's
        kind, verdict and the birth that installed it.
      - **The round they were asked**: the list in its order, each listed rule
        as the round showed it, the answer's sides, its note and its reasoning,
        whole.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The replay is the log.** Every edge the replay tries gets the log's
     verdict, and the replayed base is the run's.
  2. **The copies are `copies.json`'s**, with their originals and the rule that
     erred at their ticket.
  3. **The record's order does what a pair says.** At every pair the log
     installed the win and refused the loss for closing a cycle, and at every
     rule cited on both sides it did the same.
  4. **The losses are `sides.json`'s.** The losses the copies' pairs hold,
     with those of their rules cited on both sides, are exactly the copies'
     refused losses `sides.json` reads as closed by the copy's own answer.
  5. **The two copies are `lost.json`'s.** In L r2 the newborns of the four
     edges that carry the most lost points are `R0143` and `R0234`, and both
     are copies.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  Q1. **Both right.** Pooled over the six runs, at more than half of the
      copies' pairs both sides are right by the policy.
  Q2. **A wrong step between.** Pooled, at more than half of the copies' pairs
      a step wrong by the policy carries every path from `D` to `U`.
  Q3. **Nowhere.** Pooled, the cycle is nowhere at more than half of the
      copies' pairs.
  Q4. **Not shown.** Pooled, the round showed fewer than a tenth of the copies'
      pairs.
  Q5. **The two copies.** In L r2, `R0143` and `R0234` each have a pair, and at
      every pair of theirs both sides are right and a wrong step carries every
      path.

A clause that reads a missing value fails.

**The drafter's account.**
- **What the order settles.** A pair's win and loss cannot both go in, so the
  order of installation chooses which goes: the win in the record, the loss in
  `ranked/losses.py`'s replay with the copies' losses first. That is P's
  lesson. No clause reads it; gate 3 holds the reading to it.
- **What a path must cross, at the two copies.** P read the lower rules of
  their four costliest wins as deflection's rules of severity 4 without the
  keyword, and their kept losses as losses to rules of the keyword's half.
  - **The crossing.** A path from a rule outside the keyword's half to one
    inside it must cross by a declared step, from a rule that does not read the
    keyword to one that requires it. Containment cannot cross: a rule nested in
    a rule of the half lies in the half.
  - **What the policy says there.** On the keyword's half the policy names only
    `SECURITY_INCIDENT` and `T2_TECHNICAL` (`H01` to `H03`). A crossing
    declared above a rule of either by a rule of any other queue is wrong, or
    even.
  - **Where.** `D` and `U` share no point there, so the cycle is nowhere by
    construction.
- **Q5, the bet.** Their losses put the keyword's rules, the policy's layer 0,
  above billing's line, which is layer 2. Their wins put billing's tickets with
  five prior tickets or more, `H11`, above deflection, `H12`. Both are right
  on the points the sides share. The risk is the crossing: a rule of
  `T2_TECHNICAL` that does not read the keyword, declared above a rule of
  `SECURITY_INCIDENT`, can be right on its points.
- **Q1, trusted least.** Most copies are billing's general line, and broader
  than these two. Their wins over deflection's rules take points of `H12`,
  where the policy sends billing's tickets of severity 3 or 4 with fewer than
  three prior tickets, outside enterprise accounts, to deflection. Over the
  points it shares, such a win can be wrong. N found the copies' refused sides
  right at 2,017 of 3,796, and their refused losses at 548 of 908.
- **Q2.** A cycle of steps each right on the points its two rules share can
  exist where no point lies on all of them. So Q2 says the base held a wrong
  order between the two rules, and not only a shape the engine refuses. N
  found the doors that carry the most of L r2's refused sides to be early
  declarations: `R0039`, the two copies' original, above `R0031`, of
  deflection, and `R0031` above `R0018`, a keyword rule of `T2_TECHNICAL`.
- **Q3.** Across the keyword's half the cycle is nowhere by construction.
  Elsewhere a pair's two other rules each cross the copy, and need not meet
  each other. N found most of the copies' refused sides somewhere. There, on a
  win, the rule nested in the copy that a path entered through matched a point
  the two rules share. A pair's cycle enters the copy through no such rule.
- **Q4, trusted most.** The round never shows containment, and shows a declared
  step only where one of its rules is listed with the other among its own
  sides. The drafter expects the paths to run through rules the round does not
  list.
- **How the pairs weigh.** An answer holds one pair for each of its wins and
  losses the base cannot hold together. Each pair counts once, so a broad copy
  with many pairs weighs as many. The record keeps every pair with its birth,
  so a reading by copy is free.

**The bet is Q5.** **Q4 is trusted most.** **Q1 is trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md`'s header, its Stage C, and its sections N, O and P
  whole, and the notes `STATUS.md` and `IDEAS.md` carry for its other readings;
- `harness/hidden_policy.py`'s rules;
- `ranked/sides.py`, `ranked/lost.py` and the helpers of `ranked/refusals.py`
  and `corrections/paths.py` this reading reuses; `rung2/engine2.py`'s
  containment, `try_edge` and `render`; `authorship/loop.py`'s order of
  installation; `placement/protocol.py`'s list;
- the fields of the loop records, of `sides.json`'s rows, of `copies.json`'s
  runs and of `lost.json`'s top edges, and one placement answer of L r2, at
  case 1, a birth that is not a copy's.

**What the drafter had not seen**: any pair, any verdict on a pair's sides, any
path from `D` to `U`, door or where any cycle is, what any round showed, the
lists, answers and reasoning of `R0143` and `R0234`, and any figure of
`sides.json`, `copies.json` or `lost.json` beyond what `FINDINGS_RANKED.md`
states.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-21, after `ranked/lost.py`. The
expectation above was written and committed before the reading ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  python3 -m ranked.together --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.together
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any, Sequence

from harness.provenance import describe, environment

from corrections import paths as CP
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

from . import copies as CO
from . import plan
from . import readings as RD
from . import refusals as RF
from . import sides as SD

RUNS = RD.RUNS
WIN, LOSS = RF.WIN, RF.LOSS
OWN = RF.OWN
SOMEWHERE, NOWHERE = RF.SOMEWHERE, RF.NOWHERE
WHERE = RF.WHERE
VERDICTS = RF.VERDICTS
RIGHT, WRONG = CP.RIGHT_VERDICT, CP.WRONG
NESTED, DECLARED = RF.NESTED, RF.DECLARED
GROUPS = ("copies", "others")
NAMED_RUN = "l_r2"
NAMED = ("R0143", "R0234")
NAMED_EDGES = 4                     # gate 5: lost.json's edges that carry the most
TOP = 12
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-21, after ranked/lost.py. The expectation in "
    "the module's docstring was written and committed before the reading ran. Not a signed "
    "row; no verdict moves.")

plain = RD.plain


# ---------------------------------------------------------------------------
# The pairs of one birth, in the base right before its first edge
# ---------------------------------------------------------------------------

def pairs_at(engine: PriorityEngine, rid: str, edges: Sequence[erb.Edge]
             ) -> tuple[list[tuple[erb.Edge, erb.Edge]], list[tuple[erb.Edge, erb.Edge]]]:
    """Every win and loss of the newborn `rid` the base cannot hold together,
    and every rule its answer cited on both sides, each as (win, loss)."""
    wins = [e for e in edges if e.winner == rid and e.loser != rid]
    losses = [e for e in edges if e.loser == rid and e.winner != rid]
    pairs: list[tuple[erb.Edge, erb.Edge]] = []
    both: list[tuple[erb.Edge, erb.Edge]] = []
    if not wins or not losses:
        return pairs, both
    up = CP.forward(engine, rid)                 # a loss to one of these closes alone
    seen: set[tuple[str, str]] = set()
    for w in wins:
        reach = CP.forward(engine, w.loser)
        if rid in reach:                         # the win closes alone
            continue
        for lo in losses:
            u = lo.winner
            if u in up or (w.loser, u) in seen:  # the loss closes alone, or seen
                continue
            if u == w.loser:
                seen.add((w.loser, u))
                both.append((w, lo))
            elif u in reach:
                seen.add((w.loser, u))
                pairs.append((w, lo))
    return pairs, both


# ---------------------------------------------------------------------------
# What holds D above U
# ---------------------------------------------------------------------------

class Steps:
    """The policy's verdict on a step, kept as the run goes: the rules'
    extensions never change once born."""

    def __init__(self, engine: PriorityEngine, action: dict[str, str], truth: dict[str, int]):
        self.engine, self.action, self.truth = engine, action, truth
        self.kept: dict[tuple[str, str], str] = {}

    def verdict(self, x: str, y: str) -> str:
        k = (x, y)
        if k not in self.kept:
            self.kept[k] = CP.verdict(self.engine, x, y, self.action, self.truth)
        return self.kept[k]


def reaches_without(engine: PriorityEngine, src: str, dst: str, nodes: set[str],
                    keep) -> bool:
    """Whether `src` reaches `dst` through `nodes` by the steps `keep` keeps."""
    seen, stack = {src}, [src]
    while stack:
        x = stack.pop()
        if x == dst:
            return True
        for y in engine.wins_over(x):
            if y in nodes and y not in seen and keep(x, y):
                seen.add(y)
                stack.append(y)
    return False


def doors(engine: PriorityEngine, src: str, dst: str, nodes: set[str]) -> list[tuple[str, str]]:
    """The steps every path from `src` to `dst` passes through. A door lies on
    every path, so on one shortest path: only its steps are tried."""
    path = SD.one_path(engine, src, dst, nodes)
    if not path:
        return []
    out = []
    for x, y in zip(path, path[1:]):
        if not reaches_without(engine, src, dst, nodes, lambda a, b, s=(x, y): (a, b) != s):
            out.append((x, y))
    return out


def shown_steps(beats: dict[str, list[str]], loses: dict[str, list[str]],
                listed: Sequence[str]):
    """The declared steps the round's list shows: a listed rule's own `beats`,
    and a listed rule's own `loses_to`."""
    on = set(listed)

    def shown(engine: PriorityEngine, x: str, y: str) -> bool:
        if RF.step_kind(engine, x, y) != DECLARED:
            return False
        return bool((x in on and y in beats.get(x, ())) or (y in on and x in loses.get(y, ())))
    return shown


def read_pair(engine: PriorityEngine, rid: str, d: str, u: str, steps: Steps,
              shown, installed_at: dict[tuple[str, str], int], keyword: int,
              born: dict[int, dict], copies: set[str]) -> dict[str, Any]:
    """One pair, read in the base right before its birth's first edge."""
    ext, action = engine.ext, steps.action
    nodes = CP.forward(engine, d) & CP.backward(engine, u)
    region = ext[rid] & ext[d] & ext[u]
    door_rows = []
    for x, y in doors(engine, d, u, nodes):
        kind = RF.step_kind(engine, x, y)
        at = installed_at.get((x, y)) if kind == DECLARED else None
        by = born[at]["rule_id"] if at is not None else None
        door_rows.append({"upper": x, "lower": y, "kind": kind, "verdict": steps.verdict(x, y),
                          "installed_at": at, "installed_by": by,
                          "by_a_copy": by in copies if by else None,
                          "queues": [action[x], action[y]]})
    return {
        "newborn": rid, "lower": d, "upper": u,
        "queues": [action[rid], action[d], action[u]],
        "win_verdict": CP.verdict(engine, rid, d, action, steps.truth),
        "loss_verdict": CP.verdict(engine, u, rid, action, steps.truth),
        "carried_wrong": not reaches_without(
            engine, d, u, nodes, lambda x, y: steps.verdict(x, y) != WRONG),
        "carried_wrong_declared": not reaches_without(
            engine, d, u, nodes,
            lambda x, y: RF.step_kind(engine, x, y) != DECLARED or steps.verdict(x, y) != WRONG),
        "where": SOMEWHERE if region and CP.local_reach(engine, d, u, nodes, region)
        else NOWHERE,
        "shown": reaches_without(engine, d, u, nodes, lambda x, y: shown(engine, x, y)),
        "across": bool(ext[d] & keyword == 0 and ext[u] & ~keyword == 0),
        "shortest": CP.shortest(engine, d, u, nodes),
        "path_rule_count": len(nodes - {d, u}),
        "doors": door_rows,
    }


def one_path_read(engine: PriorityEngine, d: str, u: str, steps: Steps,
                  installed_at: dict[tuple[str, str], int], born: dict[int, dict],
                  by_id: dict[str, dict], copies: set[str]) -> list[dict[str, Any]]:
    """(e): one shortest path from `d` to `u`, each rule with its queue and
    birth, and each step with its kind, verdict and installer."""
    nodes = CP.forward(engine, d) & CP.backward(engine, u)
    path = SD.one_path(engine, d, u, nodes) or []
    out = []
    for i, x in enumerate(path):
        r = by_id[x]
        row = {"rule_id": x, "queue": r["action"], "born_at": r["born_at"],
               "conditions": RD.conditions_of(r["conditions"]), "copy": x in copies}
        if i + 1 < len(path):
            y = path[i + 1]
            kind = RF.step_kind(engine, x, y)
            at = installed_at.get((x, y)) if kind == DECLARED else None
            row["step_to_next"] = {"kind": kind, "verdict": steps.verdict(x, y),
                                   "installed_at": at,
                                   "installed_by": born[at]["rule_id"] if at is not None
                                   else None}
        out.append(row)
    return out


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def replay(record: dict[str, Any], space: Space, truth: dict[str, int],
           copies: Sequence[dict], named: Sequence[str] = ()) -> dict[str, Any]:
    """The record's births and edges, in order; every birth's pairs read before
    its first edge. Gates 1 and 3 are kept as it goes."""
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    escs = {e["idx"]: e for e in record["escalations"]}
    by_id = {d["rule_id"]: d for d in record["rules"]}
    beats = {d["rule_id"]: list(d.get("beats") or []) for d in record["rules"]}
    loses = {d["rule_id"]: list(d.get("loses_to") or []) for d in record["rules"]}
    ids = {c["rule_id"] for c in copies}
    keyword = space.mask["has_security_keyword"][True]
    engine = PriorityEngine(space=space)
    action: dict[str, str] = {}
    steps = Steps(engine, action, truth)
    installed_at: dict[tuple[str, str], int] = {}
    rows: list[dict[str, Any]] = []
    own_rows: list[dict[str, Any]] = []
    counts = {g: Counter() for g in GROUPS}
    named_rows: dict[str, dict[str, Any]] = {}
    log_ok = order_ok = True
    for idx in sorted(born):
        d = born[idx]
        rid = d["rule_id"]
        engine.add(rule_from(d), born_at=idx, keep_id=True)
        action[rid] = d["action"]
        edges = by_birth.get(idx, [])
        group = "copies" if rid in ids else "others"
        mine = [e for e in edges if rid in (e.winner, e.loser)]
        if mine:
            counts[group]["tried"] += 1
            if any(e.winner == rid for e in mine) and any(e.loser == rid for e in mine):
                counts[group]["win_and_loss"] += 1
        pairs, both = pairs_at(engine, rid, mine)
        listed = list((escs.get(idx) or {}).get("listed") or [])
        shown = shown_steps(beats, loses, listed)
        here = []
        for w, lo in pairs:
            row = dict(read_pair(engine, rid, w.loser, lo.winner, steps, shown, installed_at,
                                 keyword, born, ids),
                       birth=idx, group=group, win_key=w.key, loss_key=lo.key)
            here.append(row)
            order_ok &= w.verdict == EDGE_OK and lo.verdict == EDGE_CYCLE
        for w, lo in both:
            own_rows.append({"birth": idx, "group": group, "newborn": rid, "cited": w.loser,
                             "queues": [action[rid], action[w.loser]],
                             "win_key": w.key, "loss_key": lo.key})
            order_ok &= w.verdict == EDGE_OK and lo.verdict == EDGE_CYCLE
        rows.extend(here)
        if rid in named:
            named_rows[rid] = named_birth(record, escs.get(idx) or {}, engine, rid, idx, here,
                                          steps, installed_at, born, by_id, ids)
        for e in edges:
            before = e.loser in engine.decl_above.get(e.winner, set())
            why = engine.try_edge(e.winner, e.loser)
            log_ok &= why == e.verdict
            if why == EDGE_OK and not before and e.loser in engine.decl_above[e.winner]:
                installed_at[(e.winner, e.loser)] = idx
    return {"rows": rows, "own": own_rows, "counts": counts, "named": named_rows,
            "log_ok": bool(log_ok), "order_ok": bool(order_ok), "engine": engine,
            "action": action}


def named_birth(record: dict[str, Any], esc: dict[str, Any], engine: PriorityEngine, rid: str,
                idx: int, here: Sequence[dict], steps: Steps,
                installed_at: dict[tuple[str, str], int], born: dict[int, dict],
                by_id: dict[str, dict], copies: set[str]) -> dict[str, Any]:
    """(e): one of the two copies, at its birth: its pairs with one path each,
    and the round it was asked."""
    rules = {r.rule_id: r for r in engine.rules}
    calls = esc.get("calls") or []
    first = calls[0] if calls else {}
    placed = calls[1] if len(calls) > 1 else {}
    payload = placed.get("payload") or {}
    listed = list(esc.get("listed") or [])
    return {
        "rule_id": rid, "born_at": idx, "kind": esc.get("kind"),
        "report": (record.get("reports_handed") or {}).get(str(idx)),
        "conditions": RD.conditions_of(by_id[rid]["conditions"]),
        "pairs": [dict({k: r[k] for k in ("lower", "upper", "queues", "win_verdict",
                                            "loss_verdict", "carried_wrong",
                                            "carried_wrong_declared", "where", "shown",
                                            "across", "shortest", "doors")},
                       path=one_path_read(engine, r["lower"], r["upper"], steps, installed_at,
                                          born, by_id, copies))
                  for r in here],
        "round": {"listed": listed,
                  "shown_as": [rules[x].render() for x in listed if x in rules],
                  "beats": list(payload.get("beats") or []),
                  "loses_to": list(payload.get("loses_to") or []),
                  "note": payload.get("note"),
                  "reasoning": placed.get("reasoning"),
                  "first_note": (first.get("payload") or {}).get("note")},
    }


def summary(rows: Sequence[dict], own: Sequence[dict], counts: Counter) -> dict[str, Any]:
    def tally(key, keys):
        c = Counter(key(r) for r in rows)
        return {k: c.get(k, 0) for k in keys}
    return {"births_that_tried_a_side": counts.get("tried", 0),
            "births_that_tried_a_win_and_a_loss": counts.get("win_and_loss", 0),
            "births_with_a_pair": len({r["birth"] for r in rows}),
            "pairs": len(rows),
            "losses": len({r["loss_key"] for r in rows}),
            "wins": len({r["win_key"] for r in rows}),
            "cited_on_both_sides": len(own),
            "win_verdict": tally(lambda r: r["win_verdict"], VERDICTS),
            "loss_verdict": tally(lambda r: r["loss_verdict"], VERDICTS),
            "both_right": sum(r["win_verdict"] == RIGHT and r["loss_verdict"] == RIGHT
                              for r in rows),
            "carried": {"wrong": sum(r["carried_wrong"] for r in rows),
                        "wrong_declared": sum(r["carried_wrong_declared"] for r in rows)},
            "where": tally(lambda r: r["where"], WHERE),
            "door": sum(bool(r["doors"]) for r in rows),
            "shown": sum(r["shown"] for r in rows),
            "across": sum(r["across"] for r in rows)}


def by_queues(rows: Sequence[dict]) -> list[dict[str, Any]]:
    """(a): the copies' pairs by the queues of `D` and `U`."""
    n = Counter((r["queues"][1], r["queues"][2]) for r in rows)
    return [{"lower_queue": a, "upper_queue": b, "pairs": k}
            for (a, b), k in sorted(n.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]]


def top_doors(rows: Sequence[dict]) -> list[dict[str, Any]]:
    """(c): the doors that carry the most of the copies' pairs."""
    n: Counter = Counter()
    kept: dict[tuple[str, str], dict] = {}
    for r in rows:
        for dr in r["doors"]:
            k = (dr["upper"], dr["lower"])
            n[k] += 1
            kept[k] = dr
    return [dict(kept[k], pairs=c)
            for k, c in sorted(n.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP]]


def slim(row: dict[str, Any]) -> dict[str, Any]:
    """A pair as the record keeps it: its doors counted, not listed."""
    out = {k: v for k, v in row.items() if k != "doors"}
    out["door_count"] = len(row["doors"])
    return out


def read_run(record: dict[str, Any], space: Space, truth: dict[str, int],
             copies: Sequence[dict], named: Sequence[str] = ()) -> tuple[dict, dict]:
    got = replay(record, space, truth, copies, named)
    rows = {g: [r for r in got["rows"] if r["group"] == g] for g in GROUPS}
    own = {g: [r for r in got["own"] if r["group"] == g] for g in GROUPS}
    reading = {g: summary(rows[g], own[g], got["counts"][g]) for g in GROUPS}
    reading.update(by_queues=by_queues(rows["copies"]), doors=top_doors(rows["copies"]),
                   cited_on_both_sides=got["own"],
                   rows=[slim(r) for r in got["rows"] if r["group"] == "copies"])
    if named:
        reading["named"] = {rid: got["named"].get(rid) for rid in named}
    return reading, got


# ---------------------------------------------------------------------------
# The gates that read the other records
# ---------------------------------------------------------------------------

def same_losses(got: dict[str, Any], sides_rows: Sequence[dict]) -> bool:
    """Gate 4: the copies' pairs' losses, with their rules cited on both sides,
    are `sides.json`'s refused losses closed by the copy's own answer."""
    mine = {r["loss_key"] for r in got["rows"] if r["group"] == "copies"}
    mine |= {r["loss_key"] for r in got["own"] if r["group"] == "copies"}
    theirs = {r["key"] for r in sides_rows if r["side"] == LOSS and r["closes"] == OWN}
    return bool(mine == theirs)


def named_are_lost(lost_run: dict[str, Any], copies: Sequence[dict]) -> bool:
    """Gate 5: the newborns of `lost.json`'s four edges that carry the most lost
    points in L r2 are the two copies."""
    top = ((lost_run or {}).get("lost") or {}).get("top") or []
    ids = {c["rule_id"] for c in copies}
    return bool(len(top) >= NAMED_EDGES
                and {t["newborn"] for t in top[:NAMED_EDGES]} == set(NAMED)
                and set(NAMED) <= ids)


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    runs = readings.get("runs") or {}
    have = [runs[t] for t in RUNS if t in runs]
    complete = len(have) == len(RUNS)

    def total(*path) -> int | None:
        n = 0
        for r in have:
            x: Any = r
            for p in path:
                x = x.get(p) if isinstance(x, dict) else None
            if not isinstance(x, int) or isinstance(x, bool):
                return None
            n += x
        return n if complete else None

    pairs, both = total("copies", "pairs"), total("copies", "both_right")
    carried = total("copies", "carried", "wrong")
    nowhere, shown = total("copies", "where", NOWHERE), total("copies", "shown")

    def known(*xs) -> bool:
        return all(isinstance(x, int) for x in xs)

    q1 = known(pairs, both) and pairs > 0 and 2 * both > pairs
    q2 = known(pairs, carried) and pairs > 0 and 2 * carried > pairs
    q3 = known(pairs, nowhere) and pairs > 0 and 2 * nowhere > pairs
    q4 = known(pairs, shown) and pairs > 0 and 10 * shown < pairs

    named = (runs.get(NAMED_RUN) or {}).get("named") or {}
    each = {rid: (named.get(rid) or {}).get("pairs") for rid in NAMED}
    ok_named = [all(p.get("win_verdict") == RIGHT and p.get("loss_verdict") == RIGHT
                    and p.get("carried_wrong") is True for p in ps)
                for ps in each.values() if isinstance(ps, list)]
    q5 = (all(isinstance(ps, list) and ps for ps in each.values())
          and len(ok_named) == len(NAMED) and all(ok_named))

    def out(clause, what, holds, value):
        return {"clause": clause, "what": what, "reading": value, "holds": bool(holds)}

    def per_copy(ps):
        if not isinstance(ps, list):
            return None
        return {"pairs": len(ps),
                "both_right_and_carried": sum(p.get("win_verdict") == RIGHT
                                              and p.get("loss_verdict") == RIGHT
                                              and p.get("carried_wrong") is True for p in ps)}

    return [
        out("Q1", "pooled over the six runs, at more than half of the copies' pairs both sides "
                  "are right by the policy", q1, {"pairs": pairs, "both_right": both}),
        out("Q2", "pooled, at more than half of the copies' pairs a step wrong by the policy "
                  "carries every path from D to U", q2, {"pairs": pairs, "carried": carried}),
        out("Q3", "pooled, the cycle is nowhere at more than half of the copies' pairs", q3,
            {"pairs": pairs, "nowhere": nowhere}),
        out("Q4", "pooled, the round showed fewer than a tenth of the copies' pairs", q4,
            {"pairs": pairs, "shown": shown}),
        out("Q5", "in L r2, R0143 and R0234 each have a pair, and at every pair of theirs both "
                  "sides are right and a wrong step carries every path", q5,
            {rid: per_copy(ps) for rid, ps in each.items()}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "together.json"


def copies_path():
    return plan.OUT / "copies.json"


def sides_path():
    return plan.OUT / "sides.json"


def lost_path():
    return plan.OUT / "lost.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, Any], dict[str, Any], dict[str, Any]]:
    records = {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    return (records, json.loads(copies_path().read_text()),
            json.loads(sides_path().read_text()), json.loads(lost_path().read_text()))


def read_everything(records: dict[str, dict], kept: dict[str, Any], sides: dict[str, Any],
                    lost: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    kept_runs = kept["readings"]["runs"]
    sides_runs = sides["readings"]["runs"]
    gates: list[dict[str, Any]] = []
    runs = {}
    for t in RUNS:
        if t not in records:
            continue
        copies, ok = CO.copies_of_run(records[t], space)
        gates.append({"gate": 2, "run": t, "what": "the copies are copies.json's",
                      "passes": SD.same_copies(copies, kept_runs[t]["rows"], ok)})
        named = NAMED if t == NAMED_RUN else ()
        runs[t], got = read_run(records[t], space, truth, copies, named)
        gates.append({"gate": 1, "run": t, "what": "the replay is the log",
                      "passes": bool(got["log_ok"]
                                     and RF.same_base(got["engine"], records[t], space))})
        gates.append({"gate": 3, "run": t, "what": "the record's order does what a pair says",
                      "passes": got["order_ok"]})
        gates.append({"gate": 4, "run": t, "what": "the losses are sides.json's",
                      "passes": same_losses(got, sides_runs[t]["rows"])})
        if t == NAMED_RUN:
            gates.append({"gate": 5, "run": t, "what": "the two copies are lost.json's",
                          "passes": named_are_lost(lost["readings"]["runs"].get(t), copies)})
    return {"runs": runs}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why billing's copies declared sides the base "
                                             "could not hold together (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/together.py writes {record_path()}")
    records, kept, sides, lost = read_inputs()
    readings, gates = read_everything(records, kept, sides, lost)
    for g in sorted(gates, key=lambda g: (RUNS.index(g["run"]), g["gate"])):
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(RUNS)
    if not complete:
        print("  missing records")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0 if complete and all(g["passes"] for g in gates) else 1
    if not complete or not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(readings)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"copies": str(copies_path()), "copies_from": kept["_env"].get("git_commit"),
                   "sides": str(sides_path()), "sides_from": sides["_env"].get("git_commit"),
                   "lost": str(lost_path()), "lost_from": lost["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "every birth's win and loss the base right before its first edge could not "
                   "hold together, each read in that base; the policy's verdict on a side or a "
                   "step over the points its two rules share",
        "constants": {"named_run": NAMED_RUN, "named": list(NAMED),
                      "named_edges": NAMED_EDGES, "top": TOP},
        "gates": gates,
        "readings": readings,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for cl_ in expectation:
        print(f"  {cl_['clause']}: {'holds' if cl_['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
