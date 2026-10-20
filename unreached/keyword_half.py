"""
WHAT THE KEYWORD HOLDS OVER THE SPACE. Four questions the records leave open,
read as one. `FINDINGS_UNREACHED.md`, *What this does not settle*, names three:
why `R0019` leaves 5,900 points, which rules the back move's 1,560 come from,
and which rules the swaps carried up along the curve. `FINDINGS_ESCALATIONS.md`
and `FINDINGS_SPOTCHECK.md` name the fourth: why the space follows
`SECURITY_INCIDENT` at the top. Neither record could say, since neither splits
the space by the keyword. `IDEAS.md` carries all four as free readings.
POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL, AND WHAT IT IMPLIES BEFORE ANY READING
--------------------------------------------------------------------------
**The keyword half** is the 67,200 points of the space with the security
keyword. The hidden policy's first layer decides all of it:
- `SECURITY_INCIDENT` on 50,400 points;
- `T2_TECHNICAL` on the 16,800 of the two lower tiers at severity 3 or 4.

Rung 1's base routes to `SECURITY_INCIDENT` with thirteen rules:
- `R0019`, *the keyword and severity 1*, right on all of its 16,800 points;
- **the keyword rule**, *the keyword* alone, written twelve times, `R0067`
  the earliest.

The twelve copies have one extension, so in an order only the highest decides
anything. Its place is the order's **copy place**. It matches the whole half,
so no rule below it decides a point of the half. On the half an order is right
only where a `SECURITY_INCIDENT` rule decides a point whose truth is that queue,
or a `T2_TECHNICAL` rule one whose truth is that queue.

**Two things follow from the stage's record.**
- In the escalations' order `R0019` decides neither of its two test cases, and
  both are right (`FINDINGS_UNREACHED.md`, the table of the 25). Their truth is
  `SECURITY_INCIDENT`, so a copy of the keyword rule decides them, above
  `R0019`'s place 55. So `R0019` decides no point of the space there. Its 5,900
  are the keyword's severity-1 points that rules above the copy place take with
  another queue.
- At ten labels, draws 0 and 2, the back move costs the order all three of its
  `SECURITY_INCIDENT` test cases, and `R0019` matches two test cases. So a copy
  decides one of them, no label reaches it, and neither draw labels a keyword
  ticket.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Why `R0019` leaves 5,900 points.** In the escalations' order, every rule
     that decides a point of `R0019`'s extension:
     - its place, queue and conditions;
     - the points it decides there, and how many right;
     - the escalations it decides, and how many right.
     The same in the whole train half's order, beside, and in both, every rule
     that decides a point of the keyword half.
  B. **The parts of the back move over the space.** In the escalations' order,
     every rule no escalation reaches:
     - the points it decides;
     - how many are right before the move and after it, on each half;
     - the queues that take them after.
  C. **What the swaps carried up.** The same parts in the twenty orders of the
     curve, on the test split and over the space. Where the back move changes
     an order, its start is rebuilt from the declared seed and searched again
     pass by pass. For every rule no label reaches that decides something, and
     every rule that routes to `SECURITY_INCIDENT`: its place at the start,
     after each pass and at the end.
  D. **The space split by the keyword.** Every order of the escalations stage
     and of the audit stage, with the twenty of random arrivals and the two
     endpoints beside:
     - its right decisions on each half, and on the keyword half by truth;
     - its copy place;
     - the keyword tickets its labels hold.
     The **cells** are twelve: the escalations' seven sets at each budget, and
     the audit's five draws at each arm and budget.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- `results_unreached/score.json`: the two endpoints' orders and the curve's
  twenty, with what the stage measured on them.
- `results_spotcheck/readings.json`: the audit stage's forty orders.
- `results_escalations/score.json`: the escalations stage's labelled sets. That
  record kept no order, so its 29 are searched again by
  `escalations/instrument.py`'s `labelled_order`, called and not copied: the
  28 of the cells, and the one on all 316. This record keeps them.
- `results_spotcheck/score.json`: what the audit stage measured, for gate 1.

The space is `space_pools`' `puro` masks. The halves are `Space`'s masks of the
keyword, and the truth by queue is `space_truth_masks`'. A start is rebuilt
from the record's `best_from`, with `declared_starts` and the record's greedy.
It is replayed with `local_search`, one pass at a time, a move pass then a swap
pass, until a round changes nothing.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The orders are the records'.** Every order scores on the test split and
     over the space what its record says, with its four rare queues. The 29
     searched again give their record's start too. The audit stage's endpoints
     are the unreached stage's orders, and so is the escalations stage's order
     on all 316.
  2. **The masks are one convention.**
     - The keyword half is `R0067`'s extension, 67,200 points.
     - The truth by queue partitions the space. It holds `SECURITY_INCIDENT` on
       50,400 points, all in the half, and `T2_TECHNICAL` on 16,800 of the half.
     - `R0019`'s extension is 16,800 points, all `SECURITY_INCIDENT`.
     - Every rule is right exactly where its extension meets its queue's truth.
     - The keyword rule has twelve copies. With `R0019` they are every rule
       that routes to `SECURITY_INCIDENT`.
  3. **Two routes agree.**
     - Every order's count over the space, walked rule by rule, is
       `score_order`'s. Its two halves sum to it, and every point of the
       keyword half is decided at or above the copy place.
     - `R0019`'s extension, decided rule by rule, gives the stage's front move.
       The stage's own reading of `R0019` is the one the deduction above reads.
     - Every back move, summed rule by rule, gives the stage's figure on each
       surface. It moves no point a reached rule decided.
  4. **The replays end where the records do.** Every rebuilt start, searched
     whole by `local_search` and replayed pass by pass, ends at the record's
     order.

It refuses to write if any fails, and while `PLAN_UNREACHED.md` is unsigned,
like every writer of the package. `--dry-run` runs the four, prints pass or
fail, and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  E1. **`T2_TECHNICAL` is the queue that takes the most of `R0019`'s 5,900
      points** in the escalations' order. The escalations hold 99
      `T2_TECHNICAL` tickets and none whose truth is `SECURITY_INCIDENT`. So
      nothing in them puts the keyword rule above the technical rules the other
      tickets put high. The billing rules are the other candidate: the billing
      product is a fifth of the keyword's severity-1 points.
  E2. **Every rule that takes 500 or more of them decides an escalation in that
      order, and is right on at least three quarters of those it decides.** The
      labels put them there, and put them well for the tickets they show.
  E3. **Deferring `R0506`, the on-call rule's highest copy, loses points over
      the space.** It sits below the copy place, so it decides only points
      without the keyword. Off hours at severity 1, the truth there is
      `ONCALL_ESCALATION` on the two upper tiers, half of the points. No
      escalation is that queue in truth, so the rules the labels placed are not
      right there.
  E4. **The copy place in the escalations' order is above every rule no
      escalation reaches, so the keyword half's part of the back move is
      zero.** The highest of the 25 is `R0459`, at place 35.
  E5. **At ten labels, draws 0 and 2, every rule no label reaches that decides
      one of the order's `SECURITY_INCIDENT` test cases right made its largest
      rise in a swap pass.** `FINDINGS_UNREACHED.md` says *a swap had carried
      it up* without reading it. A move pass never moves such a rule for
      itself, only past the rules it moves, one place each.
  E6. **At the same two orders, the keyword half carries the whole of the back
      move's loss over the space: its part is a loss at least as large as the
      net.** Deferring the rules that route to `SECURITY_INCIDENT` hands the
      half to rules that route elsewhere, wrong on three points in four of it.
  E7. **In at least 9 of the 12 cells, an order with the most points over the
      space also has the most on the keyword half.** That is what *the space
      follows `SECURITY_INCIDENT` at the top* means, if the keyword rule is what
      the shares measure.
  E8. **Pooled over the 12 cells, the keyword half's counts spread more within
      their cells than the other half's**: their squared deviations from the
      cell means sum to more.

The drafter trusts E4 least, then E1. E4 is a bet on where the copy sits, and
the record bounds that only by 55. **Read beside them, and not a clause**: the
share of the cells' spread over the space that the keyword half carries, its
covariance with the whole over the whole's variance, pooled.

**What the drafter had seen**:
- `STATUS.md`, `IDEAS.md` and `FINDINGS_UNREACHED.md` whole, every figure in
  it: the 25's places and front moves in the escalations' order, `R0019`'s
  5,900, the back move's 1,560, the curve's table and its rare queues;
- `FINDINGS_ESCALATIONS.md`'s tables of every set on both surfaces, of the
  sets' make-up at fifty labels and of the rare queues, and its reading of
  `SECURITY_INCIDENT` at the top;
- `FINDINGS_SPOTCHECK.md`'s readings over the space, and its seven cells of
  eight;
- the hidden policy and the domains, from which the half's truth follows;
- rung 1's thirteen rules that route to `SECURITY_INCIDENT`, how many of its
  rules name the keyword by queue, and the conditions of the 25;
- the code of the greedy, which puts the rules no label reaches at the tail in
  birth order, and of the move and swap passes;
- `results3/FINDINGS_ORDERS.md`, part two, as `STATUS.md` cites it:
  `SECURITY_INCIDENT` carries 57.5% of the disagreement between the full
  search's end orders over the space. Those orders share their labels; these
  differ in them.

**Not seen**:
- any order, beyond the places `FINDINGS_UNREACHED.md` publishes;
- which rule decides any point of either half in any order;
- any split of an order's count by the keyword, and any copy place;
- any start or pass of the curve's orders;
- which rules decide the `SECURITY_INCIDENT` test cases at ten labels.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for on 2026-10-20, after `PLAN_UNREACHED.md`'s stage, with
the expectation above written and committed before the first run. Not a signed
row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API calls;
about five minutes, most of them the 29 searches.

Usage:  python3 -m unreached.keyword_half --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m unreached.keyword_half
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from typing import Any, Iterable, Sequence

from escalations import instrument as I
from escalations.selections import escalations
from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung3.budget_and_balance_ls import greedy_from_record
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, build_masks,
                                declared_starts, local_search, score_order)
from rung3.order_search_ls import space_truth_masks

from . import gates, moves, plan

RECORD = plan.OUT / "keyword_half.json"
KEYWORD = "has_security_keyword"
SI, T2 = "SECURITY_INCIDENT", "T2_TECHNICAL"
SUB_RULE = "R0019"       # the keyword and severity 1 -> SECURITY_INCIDENT
FIRST_COPY = "R0067"     # the keyword rule's earliest-born copy
ONCALL = "R0506"         # the on-call rule's highest copy in the escalations' order
SWAP_DRAWS = ("10|0", "10|2")
ESC_SETS = ("random|{b}|0", "random|{b}|1", "random|{b}|2", "random|{b}|3",
            "random|{b}|4", "arrival|{b}", "crowded|{b}")
AUDIT_ARMS = ("mix", "audit")
N_CELLS = 12

# The material, as the drafter derived it from the hidden policy and the base.
# Gate 2 recomputes it.
MATERIAL = {"keyword_half": 67200, "keyword_si": 50400, "keyword_t2": 16800,
            "sub_rule": 16800, "copies": 12, "route_to_si": 13}
# What the deduction reads off the stage's record. Gate 3 reads it again.
DEDUCED_FROM = {"sub_rule_place": 55, "sub_rule_test_cases": 2,
                "sub_rule_front_space": 5900}

# The expectation's lines.
E2_TAKES = 500
E2_SHARE = (3, 4)
E7_CELLS = 9

PROVENANCE = (
    "POST-RUN: asked for on 2026-10-20, after PLAN_UNREACHED.md's stage. The "
    "expectation in the module's docstring was written and committed before the "
    "first run. Not a signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# Orders, read rule by rule
# ---------------------------------------------------------------------------

def fires(order: Sequence[str], M: dict, full: int) -> dict[str, int]:
    """What each rule decides in `order`, first match wins: only the rules
    that decide something."""
    remaining, out = full, {}
    for rid in order:
        f = M[rid] & remaining
        if f:
            out[rid] = f
            remaining ^= f
            if not remaining:
                break
    return out


def first_match(order: Sequence[str], matched, cases) -> dict[int, str | None]:
    rank = {rid: k for k, rid in enumerate(order)}
    return {i: (min(matched[i], key=rank.__getitem__) if matched[i] else None)
            for i in cases}


def copy_place(order: Sequence[str], copies: Iterable[str]) -> int:
    """The place of the highest copy: the number of rules above it."""
    rank = {rid: k for k, rid in enumerate(order)}
    return min(rank[c] for c in copies)


def conditions(rule: dict) -> list[str]:
    return [f"{c['attr']} {c['op']} {c['value']}" for c in rule["conditions"]]


def split(order: Sequence[str], sp: dict, copies: Sequence[str]) -> dict[str, Any]:
    """An order's right decisions over the space: on each half, on the keyword
    half by truth, and what decides the keyword half above the copy place."""
    F = fires(order, sp["M"], sp["full"])
    W, kw = sp["W"], sp["kw"]
    rank = {rid: k for k, rid in enumerate(order)}
    place = copy_place(order, copies)
    out = {"space": 0, "keyword": 0, "other": 0, "keyword_si": 0,
           "keyword_t2": 0, "copy_place": place, "copy_rule": order[place],
           "keyword_above_copy": 0, "keyword_above_copy_right": 0,
           "keyword_by_copy": (F.get(order[place], 0) & kw).bit_count()}
    for rid, f in F.items():
        right = W[rid] & f
        out["space"] += right.bit_count()
        out["keyword"] += (right & kw).bit_count()
        out["other"] += (right & sp["other"]).bit_count()
        out["keyword_si"] += (right & sp["si"]).bit_count()
        out["keyword_t2"] += (right & sp["t2"]).bit_count()
        if rank[rid] < place:
            out["keyword_above_copy"] += (f & kw).bit_count()
            out["keyword_above_copy_right"] += (right & kw).bit_count()
    return out


def takers(order: Sequence[str], sp: dict, region: int, inst,
           labelled: Sequence[int]) -> dict[str, Any]:
    """Every rule that decides a point of `region` in `order`, with what it
    decides there and the labelled cases it decides."""
    F = fires(order, sp["M"], sp["full"])
    W, action, truth = sp["W"], inst["action"], inst["truth"]
    by = {r["rule_id"]: r for r in inst["rules"]}
    rank = {rid: k for k, rid in enumerate(order)}
    lab: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for i, r in first_match(order, inst["matched"], labelled).items():
        if r is not None:
            lab[r][0] += 1
            lab[r][1] += action[r] == truth[i]
    rows = []
    by_queue: dict[str, dict[str, int]] = defaultdict(
        lambda: {"decides": 0, "right": 0, "wrong": 0})
    for rid, f in F.items():
        x = f & region
        if not x:
            continue
        ok = (W[rid] & x).bit_count()
        n_lab, ok_lab = lab.get(rid, (0, 0))
        row = {"rule": rid, "place": rank[rid], "queue": action[rid],
               "conditions": conditions(by[rid]), "decides": x.bit_count(),
               "right": ok, "wrong": x.bit_count() - ok,
               "labelled_decided": n_lab, "labelled_right": ok_lab}
        rows.append(row)
        q = by_queue[action[rid]]
        q["decides"] += row["decides"]
        q["right"] += ok
        q["wrong"] += row["wrong"]
    rows.sort(key=lambda r: r["place"])
    return {"rows": rows,
            "by_queue": dict(sorted(by_queue.items(),
                                    key=lambda kv: (-kv[1]["wrong"], kv[0]))),
            "decides": sum(r["decides"] for r in rows),
            "right": sum(r["right"] for r in rows),
            "wrong": sum(r["wrong"] for r in rows)}


REGIONS = ("keyword", "other", "si")


def back_parts(order: Sequence[str], U: Iterable[str], bundle: dict,
               action: dict) -> dict[str, Any]:
    """The back move rule by rule: what each rule no label reaches decides in
    `order`, and how much of it is right before the move and after it, in all
    and on each region."""
    M, W, full = bundle["M"], bundle["W"], bundle["full"]
    us = set(U)
    after_order = moves.back(order, us)
    F, FB = fires(order, M, full), fires(after_order, M, full)
    rank = {rid: k for k, rid in enumerate(order)}
    D = {u: F[u] for u in order if u in us and u in F}
    union = 0
    for d in D.values():
        union |= d
    premise = (all((F.get(r, 0) & ~FB.get(r, 0)) == 0
                   and (FB.get(r, 0) & ~F.get(r, 0) & ~union) == 0
                   for r in order if r not in us)
               and all((FB.get(u, 0) & ~D.get(u, 0)) == 0 for u in us))
    movers = {r: fb & union for r, fb in FB.items() if fb & union}
    regions = {"all": full} | {k: bundle[k] for k in REGIONS}
    parts = {}
    for u, d in D.items():
        per = {n: {"decides": (d & reg).bit_count(),
                   "before": (W[u] & d & reg).bit_count(), "after": 0}
               for n, reg in regions.items()}
        took: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        for r, m in movers.items():
            x = m & d
            if not x:
                continue
            ok = W[r] & x
            took[action[r]][0] += x.bit_count()
            took[action[r]][1] += ok.bit_count()
            for n, reg in regions.items():
                per[n]["after"] += (ok & reg).bit_count()
        for p in per.values():
            p["delta"] = p["after"] - p["before"]
        parts[u] = ({"queue": action[u], "place": rank[u]} | per["all"]
                    | {"regions": {n: per[n] for n in REGIONS},
                       "taken_by": {q: {"points": v[0], "right": v[1]}
                                    for q, v in sorted(took.items(),
                                                       key=lambda kv: -kv[1][0])}})
    return {"parts": parts,
            "net": sum(p["delta"] for p in parts.values()),
            "regions": {n: sum(p["regions"][n]["delta"] for p in parts.values())
                        for n in REGIONS},
            "premise": premise,
            "score": score_order(order, M, W, full),
            "score_after": score_order(after_order, M, W, full)}


# ---------------------------------------------------------------------------
# Starts and passes
# ---------------------------------------------------------------------------

def rebuilt_start(inst, labelled: Sequence[int], name: str) -> list[str]:
    """The declared start `name` of the search labelled at `labelled`: the
    record's greedy, or one of the seeded random starts."""
    sub = sorted(labelled)
    greedy = greedy_from_record(inst["rules"], inst["matched"], inst["truth"],
                                inst["action"], sub)
    for n, o in declared_starts(inst["ids"], first=greedy):
        if n == name:
            return list(o)
    raise KeyError(name)


def replay(inst, labelled: Sequence[int], start: Sequence[str],
           tracked: Iterable[str]) -> dict[str, Any]:
    """The search from `start`, whole and one pass at a time, with the place of
    every tracked rule after each pass."""
    sub = sorted(labelled)
    M, W, full = build_masks(inst["ids"], inst["matched"], inst["truth"],
                             inst["action"], sub)
    whole, _st = local_search(list(start), M, W, full,
                              neighbourhood=DECLARED_NEIGHBOURHOOD)
    o = list(start)
    tracked = list(tracked)
    rank = {r: k for k, r in enumerate(o)}
    trail = {r: [rank[r]] for r in tracked}
    kinds: list[str] = []
    while True:
        changed = 0
        for kind in ("move", "swap"):
            o, st = local_search(o, M, W, full, neighbourhood=kind, max_rounds=1)
            changed += st["moves"] + st["swaps"]
            kinds.append(kind)
            rank = {r: k for k, r in enumerate(o)}
            for r in tracked:
                trail[r].append(rank[r])
        if not changed:
            break
    return {"end": o, "whole": list(whole), "kinds": kinds, "trail": trail}


def path(trail: Sequence[int], kinds: Sequence[str]) -> dict[str, Any]:
    """A rule's places, read as rises: a rise is a fall in place. The largest
    rise is the earliest on a tie."""
    rises = [trail[k] - trail[k + 1] for k in range(len(kinds))]
    by = {"move": 0, "swap": 0}
    for d, kind in zip(rises, kinds):
        if d > 0:
            by[kind] += d
    big = max(range(len(rises)), key=lambda k: (rises[k], -k)) if rises else None
    largest = rises[big] if big is not None else 0
    return {"start": trail[0], "end": trail[-1], "passes": len(kinds),
            "rise_in_moves": by["move"], "rise_in_swaps": by["swap"],
            "largest_rise": largest,
            "largest_in": kinds[big] if big is not None and largest > 0 else None,
            "swap_passes_that_moved_it": sum(1 for d, kind in zip(rises, kinds)
                                             if kind == "swap" and d != 0)}


# ---------------------------------------------------------------------------
# The cells
# ---------------------------------------------------------------------------

def cell_names() -> dict[str, list[str]]:
    """The twelve cells: the escalations' seven sets at each budget, and the
    audit's five draws at each arm and budget."""
    out = {f"escalations|{b}": [f"esc:{n.format(b=b)}" for n in ESC_SETS]
           for b in plan.BUDGETS}
    for arm in AUDIT_ARMS:
        for b in plan.BUDGETS:
            out[f"{arm}|{b}"] = [f"audit:{arm}|{b}|{d}" for d in range(plan.DRAWS)]
    return out


def beside_names() -> dict[str, list[str]]:
    """The random arrivals' four, read beside the cells."""
    return {f"arrivals|{b}": [f"arrivals:{b}|{d}" for d in range(plan.DRAWS)]
            for b in plan.BUDGETS}


def squares(x: Sequence[int]) -> Fraction:
    m = Fraction(sum(x), len(x))
    return sum(((Fraction(v) - m) ** 2 for v in x), Fraction(0))


def products(x: Sequence[int], y: Sequence[int]) -> Fraction:
    mx, my = Fraction(sum(x), len(x)), Fraction(sum(y), len(y))
    return sum(((Fraction(a) - mx) * (Fraction(b) - my) for a, b in zip(x, y)),
               Fraction(0))


def read_cell(rows: Sequence[dict]) -> dict[str, Any]:
    S = [r["space"] for r in rows]
    K = [r["keyword"] for r in rows]
    N = [r["other"] for r in rows]
    top, top_k = max(S), max(K)
    return {"orders": len(rows),
            "space": [min(S), max(S)], "keyword": [min(K), max(K)],
            "other": [min(N), max(N)],
            "top_has_top_keyword": any(s == top and k == top_k
                                       for s, k in zip(S, K)),
            "ss_keyword": squares(K), "ss_other": squares(N),
            "ss_space": squares(S), "sp_keyword_space": products(K, S)}


def pooled(cells: dict[str, dict]) -> dict[str, Any]:
    ss_k = sum((c["ss_keyword"] for c in cells.values()), Fraction(0))
    ss_n = sum((c["ss_other"] for c in cells.values()), Fraction(0))
    ss_s = sum((c["ss_space"] for c in cells.values()), Fraction(0))
    sp_ks = sum((c["sp_keyword_space"] for c in cells.values()), Fraction(0))
    return {"ss_keyword": ss_k, "ss_other": ss_n, "ss_space": ss_s,
            "keyword_share": (sp_ks / ss_s) if ss_s else None}


def plain(x: Any) -> Any:
    """Fractions as floats, for the record."""
    if isinstance(x, Fraction):
        return round(float(x), 4)
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    if isinstance(x, list):
        return [plain(v) for v in x]
    return x


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(A: dict, B: dict, C: dict, D: dict) -> list[dict[str, Any]]:
    esc = A["escalations"]["sub_rule"]
    q = esc["by_queue"]
    t2 = q.get(T2, {"wrong": 0})["wrong"]
    rest = max((v["wrong"] for k, v in q.items() if k != T2), default=0)
    big = [r for r in esc["rows"] if r["wrong"] >= E2_TAKES]
    e2 = all(r["labelled_decided"] >= 1
             and r["labelled_right"] * E2_SHARE[1] >= E2_SHARE[0] * r["labelled_decided"]
             for r in big)
    oncall = B["parts"].get(ONCALL, {"delta": 0})["delta"]
    e4 = B["copy_place"] < B["unreached_top"] and B["regions"]["keyword"] == 0
    e5, e5_read = True, []
    for key in SWAP_DRAWS:
        c = C[key]
        dec = c["si_deciders"]
        paths = c.get("replay", {}).get("paths", {})
        ok = bool(dec) and all(r in paths and paths[r]["largest_in"] == "swap"
                               for r in dec)
        e5 = e5 and ok
        e5_read.append(f"{key}: " + ", ".join(
            f"{r} {paths[r]['largest_in'] if r in paths else 'unreplayed'}"
            for r in dec))
    e6 = all(C[k]["space"]["net"] < 0
             and C[k]["space"]["regions"]["keyword"] <= C[k]["space"]["net"]
             for k in SWAP_DRAWS)
    cells = D["cells"]
    tops = sum(1 for c in cells.values() if c["top_has_top_keyword"])
    pool = D["pooled"]
    return [
        {"clause": "E1", "holds": t2 > rest,
         "reading": f"of {esc['wrong']} taken with another queue: " + ", ".join(
             f"{k} {v['wrong']}" for k, v in q.items() if v["wrong"])},
        {"clause": "E2", "holds": e2,
         "reading": f"{len(big)} rules take {E2_TAKES} or more: " + ", ".join(
             f"{r['rule']} {r['wrong']} ({r['labelled_right']} of "
             f"{r['labelled_decided']} escalations right)" for r in big)},
        {"clause": "E3", "holds": oncall < 0,
         "reading": f"deferring {ONCALL}: {oncall:+d} over the space"},
        {"clause": "E4", "holds": e4,
         "reading": f"copy place {B['copy_place']}, highest unreached "
                    f"{B['unreached_top']}; the keyword half's part "
                    f"{B['regions']['keyword']:+d}"},
        {"clause": "E5", "holds": e5, "reading": "; ".join(e5_read)},
        {"clause": "E6", "holds": e6,
         "reading": "; ".join(f"{k}: net {C[k]['space']['net']:+d}, keyword half "
                              f"{C[k]['space']['regions']['keyword']:+d}"
                              for k in SWAP_DRAWS)},
        {"clause": "E7", "holds": tops >= E7_CELLS,
         "reading": f"{tops} of {len(cells)} cells"},
        {"clause": "E8", "holds": pool["ss_keyword"] > pool["ss_other"],
         "reading": f"squared deviations: keyword half "
                    f"{float(pool['ss_keyword']):.4g}, other half "
                    f"{float(pool['ss_other']):.4g}"},
    ]


# ---------------------------------------------------------------------------
# The bundles and the orders
# ---------------------------------------------------------------------------

def space_bundle() -> dict[str, Any]:
    M, W, full, n = I.space_masks()
    space = Space()
    kw = space.mask[KEYWORD][True]
    truth = space_truth_masks(space)
    return {"M": M, "W": W, "full": full, "n": n, "kw": kw, "keyword": kw,
            "other": full & ~kw, "si": truth[SI] & kw, "t2": truth[T2] & kw,
            "truth": truth}


def test_bundle(inst) -> dict[str, Any]:
    _tr, te = I.halves(inst)
    M, W, full = I.test_masks()
    corpus, truth = inst["corpus"], inst["truth"]
    kw = sum(1 << k for k, i in enumerate(te) if getattr(corpus[i], KEYWORD))
    si = sum(1 << k for k, i in enumerate(te) if truth[i] == SI)
    return {"M": M, "W": W, "full": full, "keyword": kw, "other": full & ~kw,
            "si": si}


def keyword_copies(inst) -> list[str]:
    by = {r["rule_id"]: r for r in inst["rules"]}
    t = moves.text(by[FIRST_COPY])
    return sorted((rid for rid in inst["ids"] if moves.text(by[rid]) == t),
                  key=lambda r: (inst["born"][r], r))


def collect(inst, rec: dict, tr, escs) -> tuple[dict, dict, dict]:
    """Every order read, its labelled set, and the start of the 29 searched
    again."""
    u, e, s, rd = rec["unreached"], rec["escalations"], rec["spotcheck"], rec["readings"]
    orders: dict[str, list[str]] = {}
    labelled: dict[str, list[int]] = {}
    for name in plan.ENDPOINTS:
        orders[name] = list(u["orders"]["endpoints"][name])
    labelled["escalations"], labelled["full"] = list(escs), list(tr)
    for key, o in u["orders"]["curve"].items():
        k, d = (int(x) for x in key.split("|"))
        orders[f"arrivals:{key}"] = list(o)
        labelled[f"arrivals:{key}"] = list(I.record_draw(inst, k, d))
    for name, o in rd["orders"].items():
        if name not in plan.ENDPOINTS:
            orders[f"audit:{name}"] = list(o)
            labelled[f"audit:{name}"] = list(s["selections"][name]["cases"])
    starts = {}
    for name, sel in e["selections"].items():
        best, st = I.labelled_order(inst, sel["cases"])
        orders[f"esc:{name}"] = list(best)
        labelled[f"esc:{name}"] = list(sel["cases"])
        starts[f"esc:{name}"] = st["best_from"]
        print(f"  searched {name}", flush=True)
    return orders, labelled, starts


def recorded(rec: dict, name: str) -> dict[str, Any]:
    """What the order's own record measured: test, space and the rare queues,
    and the start where the record keeps it."""
    u, e, s = rec["unreached"], rec["escalations"], rec["spotcheck"]
    if name in plan.ENDPOINTS:
        o = u["endpoints"][name]["order"]
        return {"test": o["test"], "space": o["space"], "rare": o["rare"],
                "best_from": u["endpoints"][name]["best_from"]}
    src, key = name.split(":", 1)
    if src == "arrivals":
        row = u["curve"][key]
        return {"test": row["order"]["test"], "space": row["order"]["space"],
                "rare": row["order"]["rare"], "best_from": row["best_from"]}
    r = (e if src == "esc" else s)["results"][key]
    return {"test": r["test"], "space": r["space"],
            "rare": gates.rare(r["per_class"]), "best_from": r["best_from"]}


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("unreached/keyword_half.py writes nothing")
    t0 = time.time()
    rec = {"unreached": json.loads(plan.SCORE_PATH.read_text()),
           "escalations": json.loads(plan.ESCALATIONS.read_text()),
           "spotcheck": json.loads(plan.SPOTCHECK.read_text()),
           "readings": json.loads(plan.READINGS.read_text())}
    inst = I.instance()
    tr, te = I.halves(inst)
    escs = escalations(tr)
    ids, matched, action = inst["ids"], inst["matched"], inst["action"]

    print("=" * 78)
    print("PLAN_UNREACHED.md — WHAT THE KEYWORD HOLDS OVER THE SPACE — POST-RUN")
    print("=" * 78)
    orders, labelled, starts = collect(inst, rec, tr, escs)
    sp, tb = space_bundle(), test_bundle(inst)
    copies = keyword_copies(inst)
    test_m = (tb["M"], tb["W"], tb["full"])
    space_m = (sp["M"], sp["W"], sp["full"])
    off: dict[str, list] = defaultdict(list)

    # Gate 1: the orders are the records'.
    for name, order in orders.items():
        want = recorded(rec, name)
        got = {"test": score_order(order, *test_m),
               "space": score_order(order, *space_m),
               "rare": gates.rare(I.per_class(inst, order, te))}
        if name.startswith("esc:"):
            got["best_from"] = starts[name]
        if any(got[k] != want[k] for k in got):
            off["1"].append(name)
    for name in plan.ENDPOINTS:
        if rec["readings"]["orders"][name] != orders[name]:
            off["1"].append(f"readings:{name}")
    if orders["esc:all"] != orders["escalations"]:
        off["1"].append("esc:all")

    # Gate 2: the masks are one convention.
    kw, truth = sp["kw"], sp["truth"]
    by = {r["rule_id"]: r for r in inst["rules"]}
    route_si = {r for r in ids if action[r] == SI}
    sum_truth = sum(m.bit_count() for m in truth.values())
    union_truth = 0
    for m in truth.values():
        union_truth |= m
    material = {"keyword_half": kw.bit_count(), "keyword_si": sp["si"].bit_count(),
                "keyword_t2": sp["t2"].bit_count(),
                "sub_rule": sp["M"][SUB_RULE].bit_count(), "copies": len(copies),
                "route_to_si": len(route_si)}
    masks_ok = (material == MATERIAL
                and kw == sp["M"][FIRST_COPY]
                and union_truth == sp["full"] and sum_truth == sp["n"]
                and truth[SI] & ~kw == 0
                and sp["M"][SUB_RULE] & ~truth[SI] == 0
                and all(sp["W"][r] == sp["M"][r] & truth[action[r]] for r in ids)
                and route_si == set(copies) | {SUB_RULE}
                and all(moves.text(by[c]) == moves.text(by[FIRST_COPY]) for c in copies))
    if not masks_ok:
        off["2"].append("masks or material")

    # D: every order, split by the keyword.
    rows = {}
    for name, order in orders.items():
        r = split(order, sp, copies)
        lab_kw = Counter(inst["truth"][i] for i in labelled[name]
                         if getattr(inst["corpus"][i], KEYWORD))
        rows[name] = r | {"test": score_order(order, *test_m),
                          "test_si_right": I.per_class(inst, order, te)[SI]["right"],
                          "labels": len(labelled[name]),
                          "labelled_keyword": dict(lab_kw.most_common())}
        if (r["space"] != score_order(order, *space_m)
                or r["keyword"] + r["other"] != r["space"]
                or r["keyword_si"] + r["keyword_t2"] != r["keyword"]
                or r["keyword_above_copy"] + r["keyword_by_copy"] != MATERIAL["keyword_half"]):
            off["3"].append(f"split:{name}")
    cells = {c: read_cell([rows[n] for n in names]) for c, names in cell_names().items()}
    beside = {c: read_cell([rows[n] for n in names])
              for c, names in beside_names().items()}
    D = {"cells": cells, "pooled": pooled(cells), "beside": beside}

    # A: R0019's extension and the keyword half, at both endpoints.
    u_rec = rec["unreached"]
    A = {}
    for name in plan.ENDPOINTS:
        A[name] = {"sub_rule_place": orders[name].index(SUB_RULE),
                   "copy_place": rows[name]["copy_place"],
                   "sub_rule": takers(orders[name], sp, sp["M"][SUB_RULE], inst,
                                      labelled[name]),
                   "keyword": takers(orders[name], sp, kw, inst, labelled[name])}
    esc_r = u_rec["endpoints"]["escalations"]["rules"][SUB_RULE]
    if not (A["escalations"]["sub_rule"]["decides"] == MATERIAL["sub_rule"]
            and A["escalations"]["sub_rule"]["wrong"] == esc_r["delta_space"]
            == DEDUCED_FROM["sub_rule_front_space"]
            and esc_r["rank"] == A["escalations"]["sub_rule_place"]
            == DEDUCED_FROM["sub_rule_place"]
            and esc_r["test_cases"] == DEDUCED_FROM["sub_rule_test_cases"]
            and esc_r["decided_in_order"] == 0
            and esc_r["right_in_order"] == esc_r["right_moved"] == esc_r["test_cases"]):
        off["3"].append("sub_rule")

    # B: the back move's parts over the space, in the escalations' order.
    U_e = moves.unreached(ids, matched, escs)
    b = back_parts(orders["escalations"], U_e, sp, action)
    e_rec = u_rec["endpoints"]["escalations"]
    B = b | {"copy_place": rows["escalations"]["copy_place"],
             "unreached_top": min(orders["escalations"].index(r) for r in U_e)}
    if not (U_e == e_rec["unreached"] and b["premise"]
            and b["net"] == b["score_after"] - b["score"]
            == e_rec["back"]["space"] - e_rec["order"]["space"]
            and b["regions"]["keyword"] + b["regions"]["other"] == b["net"]):
        off["3"].append("back:escalations")

    # C: the curve's twenty, on both surfaces, and the replays.
    C = {}
    for key in u_rec["orders"]["curve"]:
        name = f"arrivals:{key}"
        row = u_rec["curve"][key]
        U = moves.unreached(ids, matched, labelled[name])
        bt = back_parts(orders[name], U, tb, action)
        bs = back_parts(orders[name], U, sp, action)
        C[key] = {"unreached": len(U), "best_from": row["best_from"],
                  "test": bt, "space": bs,
                  "si_deciders": sorted(r for r, p in bt["parts"].items()
                                        if p["regions"]["si"]["before"] > 0)}
        if not (len(U) == row["unreached"] and bt["premise"] and bs["premise"]
                and bt["net"] == bt["score_after"] - bt["score"]
                == row["back"]["test"] - row["order"]["test"]
                and bs["net"] == bs["score_after"] - bs["score"]
                == row["back"]["space"] - row["order"]["space"]
                and bt["regions"]["keyword"] + bt["regions"]["other"] == bt["net"]
                and bs["regions"]["keyword"] + bs["regions"]["other"] == bs["net"]):
            off["3"].append(f"back:{key}")
        if bt["net"] or bs["net"]:
            tracked = sorted(set(bt["parts"]) | set(bs["parts"]) | route_si,
                             key=lambda r: (inst["born"][r], r))
            start = rebuilt_start(inst, labelled[name], row["best_from"])
            rp = replay(inst, labelled[name], start, tracked)
            if not (rp["end"] == rp["whole"] == orders[name]):
                off["4"].append(key)
            C[key]["replay"] = {"start": row["best_from"], "passes": len(rp["kinds"]),
                                "paths": {r: path(rp["trail"][r], rp["kinds"])
                                          for r in tracked}}
            print(f"  replayed {key}", flush=True)

    checked = [{"gate": g, "what": what, "off": off.get(g, []),
                "passes": not off.get(g)}
               for g, what in (("1", "the orders are the records'"),
                               ("2", "the masks are one convention"),
                               ("3", "two routes agree"),
                               ("4", "the replays end where the records do"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off'][:12]}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    expectation = read_expectation(A, B, C, D)
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  {e['reading']}")

    RECORD.write_text(json.dumps({
        "_env": environment(split_seed=plan.SPLIT_SEED, budgets=list(plan.BUDGETS),
                            draws=plan.DRAWS),
        "what": "what the keyword holds over the space: why R0019 leaves its points, "
                "the parts of the back move, what the swaps carried up along the "
                "curve, and every order's count split by the keyword",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "source": {"records": [str(plan.SCORE_PATH), str(plan.READINGS),
                               str(plan.ESCALATIONS), str(plan.SPOTCHECK)],
                   "orders": "the unreached stage's 22 and the audit stage's 40 from "
                             "their records; the escalations stage's 29 searched "
                             "again by escalations/instrument.py's labelled_order"},
        "surface": "the exhaustive space, 134,400 points, split by the security "
                   "keyword, and corpus test split 0, 995 cases; puro pool; every "
                   "count against the truth",
        "material": material,
        "gates": checked,
        "A": A,
        "B": B,
        "C": C,
        "D": plain({"orders": rows} | D),
        "orders": {n: o for n, o in orders.items() if n.startswith("esc:")},
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }, indent=2) + "\n")
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
