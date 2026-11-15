"""
SHAPE OR ORDER: WHAT THE LOOP'S OWN RULES COULD DECIDE, ORDERED.
Compiled at once, L's labels give a base far better than the loop's at all of a
run's labels (`CR-d` holds). Two accounts fit:
- **shape.** The loop writes one rule at one ticket, and its rules are worse
  than an answer written whole;
- **order.** Its rules are as good, and the loop orders them worse. Its order is
  containment, the edges it declared one birth at a time, and what the engine
  refused for closing a cycle.
For the rarest queue `corrections/layer.py` found information, not shape. For
the rest of the space no reading separates the two: the replays of
`corrections/fall.py` and `corrections/carry.py` keep the loop's own
declarations. `STATUS.md` and `IDEAS.md` carry the question, *Shape or order*.
Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/layer.py`. Free on the records. POST-RUN.

`IDEAS.md` proposed installing each base in the other's order. The two bases are
different rules, as its note of 2026-11-14 says, so that is not defined. This
reading asks instead what each set of rules decides in the best order rung 2's
engine can install, and how close each base came to it.

--------------------------------------------------------------------------
THE ORDERS RUNG 2'S ENGINE CAN INSTALL
--------------------------------------------------------------------------
Rung 2's engine lets a rule strictly inside another beat it wherever both match,
whatever was declared. So it can install an order of a set of rules as written
when every rule strictly inside another comes before it. Installed as `CR-d`
installs an answer, each earlier rule declared to beat every later one it
crosses, such an order closes no cycle. The engine then decides each point by
the order's first rule that matches it. **No base of the same rules decides
right more than the best such order does**: an order that completes a base's
own graph decides every point the base decides, and its conflicts too.

**Searching those orders.** Rung 3's declared optimizer, `rung3/local_search.py`,
searches orders under first match: moves and swaps, strict improvement only, and
64 random starts of seed 17. Here every move and every swap that would put a
rule after one strictly around it is skipped, and each random start is first
repaired into such an order. Nothing else changes. Where containment is silent
it is rung 3's search, move for move, as `tests/test_corrections_shape.py` pins.
The constants are rung 3's, not tuned. The search reads:
- **the contested points**: where the rules undefeated by containment carry one
  action, every such order decides the same, so only the other points are
  searched;
- **the rules undefeated at one of them**.

**Before it measures anything, the search is measured.** The hidden policy
written as an answer decides the whole space, as `G-g1` proves. On it, the 64
declared random starts alone, never its own order, must find an order that
decides all 134,400 points right. Like `rung3.optimizer_check`, the reading
stops if they do not.

--------------------------------------------------------------------------
WHAT IS READ
--------------------------------------------------------------------------
**Each L run's final base**, as Stage C rebuilds it, read five ways over the
space:
- **the record**: the base as it stands, `CR-d`'s `space(B)`;
- **completed**: its own graph, containment and the edges it accepted, completed
  into one order. Each rule comes after every rule that beats it, and otherwise
  by birth, the earliest first, so its conflicts go to the rule born first;
- **by its labels**: the completed order, searched from there alone on the
  run's labels, the reported errors with their true queues. It is what a loop
  that reordered its own base on the labels it had would keep. A rule no label
  reaches stays where its start put it;
- **with the truth**: the best order the search finds over the whole space,
  the completed order first among its starts;
- **the bound**: the points some rule undefeated by containment gets right. No
  order decides more.

**Each L run's three at-once answers at all labels**, the ones `CR-d` reads, are
installed as it installs them, and read four ways: the record, completed in
their own list's order, with the truth, and the bound. A median is over a run's
three answers.

Each order is read for its share of the space, every queue's recall, and its
right points in the keyword half and outside it.

**The three runs are searched in three processes**, one each. Every search is
deterministic, and the record is the one a single process writes, which
`--processes 1` does.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's.** Each L run's final base decides the share of
     the space `score.json` keeps. Its three at-once answers at all labels,
     installed, give the shares and the installation summaries `score.json`
     keeps, in order.
  2. **Every order is one the engine installs.** Each order read, of the loop
     and of every answer, puts every rule strictly inside another before it.
     Installed into a fresh rung 2 engine as `CR-d` installs an answer, it
     closes no cycle, and the engine's share of the space is the order's. First
     match over the same list gives it too.
  3. **Completing loses nothing.** Every point a base decides right, its
     completed order decides right.
  4. **The bound bounds.** No order read decides more than its rules' bound.
  5. **The search finds the known optimum**, on the hidden policy, as above. It
     runs first, and nothing else runs if it fails.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs gates 5 and 1, which need no
search of the records, prints pass or fail, and writes nothing. Gates 2 to 4
read the orders the search finds, so they run with the reading.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads L's three runs, each apart. In run `r`, **at once** is the
median of its three answers' shares, `CR-d`'s `space(A(r))`. **The gap** is
`CR-d`'s difference for the run: at once less the loop's base.

  S1. **Room.** In every L run, the loop's bound is at least at once.
  S2. **Order, with the truth.** In every L run, the loop's rules with the
      truth decide at least as much of the space as at once.
  S3. **The conflicts.** In at least two of L's runs, completing the loop's
      base gives back at least half of the gap.
  S4. **The labels do not reach at once.** In every L run, the loop's base by
      its labels decides less of the space than at once.
  S5. **Where the order gains.** In L r1 and in L r2, the points the loop's rules
      with the truth decide right, less those the record does, are more in the
      keyword half than outside it.
  S6. **At once nearer its own best.** In every L run, the median of the three
      answers' gains with the truth over their record is smaller than the
      loop's gain with the truth over its record.

A clause that reads a missing value fails.

**The drafter's account.**
- **The loop's rules are many.** About 280 a run, against a few dozen in an
  answer, and most of the space is contested among them. With the truth there
  is room for at once: S1.
- **It ordered them badly.** Most of what the loop lost after its peak was
  `SECURITY_INCIDENT`'s, left in conflicts by right sides the engine refused
  (`corrections/fall.py`). Its doors carried most of that fall in L r1 and L r2
  (`corrections/carry.py`). Installed losses first, the same declarations came
  close to at once in L r1 and L r2. An order chosen with the truth, free of the
  loop's declarations, should do better than any of them: S2, and S5 where the
  fall was conflicts.
- **Completing by birth gives a conflict to the older rule.** In the keyword
  half that is mostly the security rule the later rules climbed over, or were
  refused under: S3, in L r1 and L r2. L r3's fall was mostly containment,
  which no order changes.
- **The labels are tickets of the corpus**, and the corpus has few of the
  keyword half, where the gap lies: S4.
- **An answer is written whole**, its list chosen at once. The loop's order was
  declared one birth at a time: S6.

**The bet is S2.** **S1 is trusted most.** **S3 is trusted least**: where a
correction conflicts with the rule it corrects, the older rule is the wrong one.

**What the drafter had seen**:
- `FINDINGS_CORRECTIONS.md` whole. That includes Stage C's tables: the loop's
  and at once's share of the space at every checkpoint, `CR-d` by run, and
  every queue's recall. It also includes every POST-RUN reading's findings,
  `fall.json`'s and `carry.json`'s among them;
- **the search's ceiling** on the hidden policy, gate 5: all 134,400 points,
  first at start 4, by 11 of the 64 starts;
- **the search's size and cost**, timed before this was written, printing no
  share and no score:
  - L r1's final base has 282 rules, 235 of them undefeated at some contested
    point, and 114,850 contested points. One start took 6 to 11 seconds;
  - L r1's first at-once answer at all labels has 48 rules, all searched, and
    104,760 contested points. Five starts took half a second;
- `rung2/engine2.py`, `manual/compile.py`, `rung3/local_search.py`, and
  `corrections/score.py`'s `at_once` and `base_after`.

**What the drafter had not seen**: any order's share of the space, any bound,
any completed base, and anything the search finds, by the labels or with the
truth.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Proposed by the agent and asked for by Sergi on 2026-11-16, after
`corrections/layer.py`. The expectation above was written and committed before
the reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m corrections.shape --dry-run   # gates 5 and 1; writes nothing
        PYTHONHASHSEED=0 python3 -m corrections.shape
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from multiprocessing import get_context
from typing import Any, Sequence

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from manual import compile as MC
from manual import instrument as MI
from reasoned_loop import score as rl_score
from reuse import structure as st
from rung2.engine2 import EDGE_OK, PriorityEngine, Rule2, Space
from rung3 import local_search as LS

from . import ask
from . import forgotten as fg
from . import layer as LY
from . import plan

F = Fraction
L_RUNS = LY.L_RUNS
KEYWORD = "has_security_keyword"
PROCESSES = 3
PROVENANCE = (
    "POST-RUN: proposed by the agent and asked for by Sergi on 2026-11-16, after "
    "corrections/layer.py. The expectation in the module's docstring was written and "
    "committed before the reading ran. Not a signed row; no verdict moves.")

median = rl_score.median
share, frac = fg.share, fg.frac


# ---------------------------------------------------------------------------
# The orders rung 2's engine can install
# ---------------------------------------------------------------------------

def containment(engine: PriorityEngine) -> tuple[dict[str, frozenset], dict[str, frozenset]]:
    """`inside[r]`: the rules strictly inside `r`, which rung 2's engine lets beat
    it wherever both match; `around[r]`: the rules strictly around it. Read off
    the engine, which computed them with `strictly_below` when each rule was
    added."""
    inside = {r.rule_id: frozenset(engine.sub_below[r.rule_id]) for r in engine.rules}
    around = {r.rule_id: frozenset(engine.sub_above[r.rule_id]) for r in engine.rules}
    return inside, around


def restricted(rel: dict[str, frozenset], ids: Sequence[str]) -> dict[str, frozenset]:
    keep = frozenset(ids)
    return {r: rel[r] & keep for r in ids}


def is_linear_extension(order: Sequence[str], inside: dict[str, frozenset]) -> bool:
    """Every rule strictly inside another comes before it, and no rule twice."""
    pos = {r: i for i, r in enumerate(order)}
    if len(pos) != len(order):
        return False
    return all(pos[b] < pos[r] for r in order for b in inside[r] if b in pos)


def topological(ids: Sequence[str], beaten_by: dict[str, frozenset],
                key: dict[str, Any]) -> list[str]:
    """The order in which each rule comes after every rule that beats it, taking
    at each step the available rule of least `key`. Kahn's algorithm: it never
    reorders two rules the graph leaves free unless the graph forces it."""
    ids = list(ids)
    keep = set(ids)
    beats: dict[str, list[str]] = {r: [] for r in ids}
    waiting = {}
    for r in ids:
        bs = [b for b in beaten_by[r] if b in keep]
        waiting[r] = len(bs)
        for b in bs:
            beats[b].append(r)
    heap = [(key[r], r) for r in ids if waiting[r] == 0]
    heapq.heapify(heap)
    out: list[str] = []
    while heap:
        _, r = heapq.heappop(heap)
        out.append(r)
        for x in beats[r]:
            waiting[x] -= 1
            if waiting[x] == 0:
                heapq.heappush(heap, (key[x], x))
    if len(out) != len(ids):
        raise ValueError("the graph has a cycle: no order of these rules respects it")
    return out


def repaired(order: Sequence[str], inside: dict[str, frozenset]) -> list[str]:
    """The linear extension of containment that keeps `order` wherever containment
    allows: at each step, the earliest rule of `order` whose inside rules are all
    placed. On an order that already is one, the identity."""
    return topological(order, inside, {r: i for i, r in enumerate(order)})


def completed(engine: PriorityEngine) -> list[str]:
    """The engine's own graph, containment and the declared edges it accepted,
    completed into one order: each rule after every rule that beats it, and
    otherwise by birth, the earliest first. Every point the engine decides is
    decided the same by this order, and the conflicts it leaves go to the rule
    born first."""
    beaten_by = {r.rule_id: frozenset(engine.beats_me(r.rule_id)) for r in engine.rules}
    key = {r.rule_id: (r.born_at, r.rule_id) for r in engine.rules}
    return topological([r.rule_id for r in engine.rules], beaten_by, key)


def merged(searched: Sequence[str], others: Sequence[str],
           inside: dict[str, frozenset]) -> list[str]:
    """Every rule in one linear extension of containment that keeps `searched`'s
    order exactly: each rule of `others` is placed, in `others`' order, as soon
    as every rule strictly inside it is. `searched` must already be a linear
    extension of the containment among its own rules."""
    first = {r: i for i, r in enumerate(others)}
    placed: set[str] = set()
    waiting = {x: len(inside[x]) for x in others}
    out: list[str] = []
    ready = [(first[x], x) for x in others if waiting[x] == 0]
    heapq.heapify(ready)
    around_of: dict[str, list[str]] = {}
    for x in others:
        for b in inside[x]:
            around_of.setdefault(b, []).append(x)

    def place(r: str) -> None:
        out.append(r)
        placed.add(r)
        for x in around_of.get(r, ()):
            waiting[x] -= 1
            if waiting[x] == 0:
                heapq.heappush(ready, (first[x], x))

    def flush() -> None:
        while ready:
            _, x = heapq.heappop(ready)
            place(x)

    for r in searched:
        flush()
        if not inside[r] <= placed:
            raise ValueError(f"{r} comes before a rule strictly inside it")
        place(r)
    flush()
    if len(out) != len(searched) + len(others):
        raise ValueError("a rule of `others` was never placed")
    return out


# ---------------------------------------------------------------------------
# An instance: what an order decides
# ---------------------------------------------------------------------------

@dataclass
class Instance:
    """A set of rules over a set of points, as rung 3's optimizer reads it.

    `M[r]` is where `r` is undefeated by containment: it matches and no rule
    strictly inside it does. `W[r]` is where it is also right. Under an order that
    puts every rule strictly inside another before it, the first rule whose `M`
    holds a point is the first rule that matches it, and rung 2's engine decides
    the point by it. So such an order decides `fixed` plus `score_order` of the
    contested points, and nothing else depends on the order.

    The points whose undefeated rules all carry one action are decided the same
    in every such order, and `fixed` counts those decided right. Only the rest,
    `full`, are searched, and only the rules undefeated at one of them, `ids`."""
    ids: list[str]
    M: dict[str, int]
    W: dict[str, int]
    full: int
    fixed: int
    fixed_right: int                  # the mask
    inside: dict[str, frozenset]      # restricted to `ids`
    around: dict[str, frozenset]
    n: int
    every: list[str]                  # every rule, by birth
    inside_all: dict[str, frozenset]

    def score(self, order: Sequence[str]) -> int:
        return self.fixed + LS.score_order(list(order), self.M, self.W, self.full)

    def right(self, order: Sequence[str]) -> int:
        """The points the order decides right, as a mask."""
        remaining, right = self.full, self.fixed_right
        for r in order:
            fires = self.M[r] & remaining
            if fires:
                right |= self.W[r] & fires
                remaining ^= fires
                if not remaining:
                    break
        return right

    def searched(self, order: Sequence[str]) -> list[str]:
        """An order of every rule, restricted to the searched ones."""
        keep = set(self.ids)
        return [r for r in order if r in keep]

    def whole(self, order: Sequence[str]) -> list[str]:
        """A searched order with every other rule merged in, by birth."""
        keep = set(self.ids)
        return merged(list(order), [r for r in self.every if r not in keep], self.inside_all)


def undefeated(ext: dict[str, int], inside: dict[str, frozenset]) -> dict[str, int]:
    """Where each rule matches and no rule strictly inside it does:
    `rung3.order_search_ls.space_pools`'s hibrido pool, over these rules."""
    out = {}
    for r, e in ext.items():
        dom = 0
        for b in inside[r]:
            dom |= ext[b]
        out[r] = e & ~dom
    return out


def instance(rules: Sequence[Rule2], ext: dict[str, int], inside: dict[str, frozenset],
             around: dict[str, frozenset], truth: dict[str, int], n: int,
             points: int | None = None) -> Instance:
    """The instance of `rules` over `points` (every point of the space by
    default), split into the fixed points and the contested ones."""
    points = (1 << n) - 1 if points is None else points
    action = {r.rule_id: r.action for r in rules}
    und = {r: m & points for r, m in undefeated(ext, inside).items()}
    by_action: dict[str, int] = {}
    for r, m in und.items():
        by_action[action[r]] = by_action.get(action[r], 0) | m
    one = two = 0
    for m in by_action.values():
        two |= one & m
        one |= m
    single = one & ~two
    fixed_right = 0
    for q, m in by_action.items():
        fixed_right |= m & single & truth.get(q, 0)
    M = {r: m & two for r, m in und.items()}
    W = {r: m & truth.get(action[r], 0) for r, m in M.items()}
    ids = [r.rule_id for r in rules if M[r.rule_id]]
    return Instance(ids=ids, M={r: M[r] for r in ids}, W={r: W[r] for r in ids}, full=two,
                    fixed=fixed_right.bit_count(), fixed_right=fixed_right,
                    inside=restricted(inside, ids), around=restricted(around, ids),
                    n=n, every=[r.rule_id for r in rules], inside_all=inside)


def coverage(inst: Instance) -> int:
    """The points some undefeated rule gets right: no order decides more.
    `rung3.order_search_ls.bound_of`'s reach, over these rules."""
    reach = inst.fixed_right
    for w in inst.W.values():
        reach |= w
    return reach.bit_count()


# ---------------------------------------------------------------------------
# The search: rung 3's declared optimizer, kept to those orders
# ---------------------------------------------------------------------------

def insertion_scores(order: list[str], k_cur: int, M, W, full) -> list[int]:
    """`rung3.local_search.best_insertion`'s sweep, every position's score kept:
    position `j` puts `order[k_cur]` back before the `j`-th rule of the order
    without it. The uniform objective only."""
    r = order[k_cur]
    rest = order[:k_cur] + order[k_cur + 1:]
    Mr, Wr = M[r], W[r]
    not_Mr = full & ~Mr
    n = len(rest)
    A = [0] * (n + 1)
    B = [0] * (n + 1)
    C = 0
    remaining, acc, k = full, 0, 0
    while k < n and remaining:
        B[k] = (Wr & remaining).bit_count()
        fires = M[rest[k]] & remaining
        if fires:
            hits = W[rest[k]] & fires
            acc += (hits & Mr).bit_count()
            C += (hits & not_Mr).bit_count()
            remaining ^= fires
        k += 1
        A[k] = acc
    tail_B = (Wr & remaining).bit_count()
    for j in range(k, n + 1):
        A[j] = acc
        B[j] = tail_B
    return [C + A[j] + B[j] for j in range(n + 1)]


def window(rest: Sequence[str], r: str, inside, around) -> tuple[int, int]:
    """The positions of `rest` at which `r` may go back: after every rule
    strictly inside it, before every rule strictly around it."""
    lo, hi = 0, len(rest)
    for j, x in enumerate(rest):
        if x in inside[r]:
            lo = j + 1
        elif x in around[r] and hi == len(rest):
            hi = j
    return lo, hi


def best_valid_insertion(order: list[str], k_cur: int, M, W, full, inside,
                         around) -> tuple[int, int]:
    """`best_insertion`, among the positions that keep containment: strict
    improvement only, scanned in the same order."""
    scores = insertion_scores(order, k_cur, M, W, full)
    rest = order[:k_cur] + order[k_cur + 1:]
    lo, hi = window(rest, order[k_cur], inside, around)
    best_k, best = k_cur, scores[k_cur]
    for j in range(lo, hi + 1):
        if scores[j] > best:
            best_k, best = j, scores[j]
    return best_k, best


def move_pass(order: list[str], M, W, full, inside, around) -> int:
    """`rung3.local_search.move_pass`, every relocation kept to the window."""
    moved = 0
    for rid in list(order):
        k = order.index(rid)
        best_k, _ = best_valid_insertion(order, k, M, W, full, inside, around)
        if best_k != k:
            order.pop(k)
            order.insert(best_k, rid)
            moved += 1
    return moved


def swap_keeps(order: Sequence[str], p: int, q: int, inside, around) -> bool:
    """Whether exchanging positions `p < q` keeps every rule strictly inside
    another before it."""
    a, b = order[p], order[q]
    if a in inside[b]:
        return False
    for x in order[p + 1:q]:
        if x in inside[b] or x in around[a]:
            return False
    return True


def swap_pass(order: list[str], M, W, full, inside, around) -> int:
    """`rung3.local_search.swap_pass`, every exchange that would break
    containment skipped before it is scored."""
    n = len(order)
    applied = 0
    rem, hit = LS._prefix_states(order, M, W, full)
    base = hit[n]
    p = 0
    while p < n:
        rem0, ok0 = rem[p], hit[p]
        if not rem0:
            break
        found = False
        for q in range(p + 1, n):
            if not (M[order[p]] & rem0) and not (M[order[q]] & rem0):
                continue
            if not swap_keeps(order, p, q, inside, around):
                continue
            s = LS._score_after_swap(order, p, q, rem0, ok0, M, W)
            if s > base:
                order[p], order[q] = order[q], order[p]
                applied += 1
                rem, hit = LS._prefix_states(order, M, W, full)
                base = hit[n]
                found = True
                break
        if not found:
            p += 1
    return applied


def local_search(order: Sequence[str], M, W, full, inside, around,
                 neighbourhood: str = LS.DECLARED_NEIGHBOURHOOD,
                 max_rounds: int = 200) -> tuple[list[str], dict[str, Any]]:
    """`rung3.local_search.local_search`, over the orders that keep containment.
    It starts from one and every move it applies keeps it one."""
    if neighbourhood not in LS.NEIGHBOURHOODS:
        raise ValueError(f"unknown neighbourhood: {neighbourhood!r}")
    order = list(order)
    if not is_linear_extension(order, inside):
        raise ValueError("the start puts a rule before one strictly inside it")
    start = LS.score_order(order, M, W, full)
    stats = {"start": start, "move_passes": 0, "moves": 0,
             "swap_passes": 0, "swaps": 0, "rounds": 0, "exhausted": False}
    for _ in range(max_rounds):
        stats["rounds"] += 1
        changed = 0
        if neighbourhood in ("move", "move+swap"):
            moved = move_pass(order, M, W, full, inside, around)
            stats["move_passes"] += 1
            stats["moves"] += moved
            changed += moved
        if neighbourhood in ("swap", "move+swap"):
            swapped = swap_pass(order, M, W, full, inside, around)
            stats["swap_passes"] += 1
            stats["swaps"] += swapped
            changed += swapped
        if not changed:
            break
    else:
        stats["exhausted"] = True
    stats["end"] = LS.score_order(order, M, W, full)
    stats["gain"] = stats["end"] - start
    return order, stats


OWN = "own order"


def declared_starts(ids: Sequence[str], inside, first: Sequence[str] | None = None
                    ) -> list[tuple[str, list[str]]]:
    """`rung3.local_search.declared_starts`'s 64 starts, seed 17, each repaired
    into an order that keeps containment. `first`, the rules' own order, goes
    first where it is given, as the greedy does there; it must keep containment
    already."""
    starts = [(name, repaired(o, inside)) for name, o in LS.declared_starts(ids)]
    if first is None:
        return starts
    first = list(first)
    if sorted(first) != sorted(ids) or not is_linear_extension(first, inside):
        raise ValueError("the first start is not an order of these rules that keeps containment")
    return [(OWN, first)] + starts


def multistart(starts, M, W, full, inside, around,
               neighbourhood: str = LS.DECLARED_NEIGHBOURHOOD) -> tuple[list[str], dict[str, Any]]:
    """`rung3.local_search.multistart`, over the orders that keep containment.
    A tie between starts goes to the earliest."""
    rows = []
    best_order, best_score, best_at = None, -1, None
    for k, (name, o0) in enumerate(starts):
        o, st = local_search(o0, M, W, full, inside, around, neighbourhood=neighbourhood)
        rows.append({"index": k, "start": name, "start_score": st["start"],
                     "end_score": st["end"], "rounds": st["rounds"], "moves": st["moves"],
                     "swaps": st["swaps"], "exhausted": st["exhausted"]})
        if st["end"] > best_score:
            best_order, best_score, best_at = o, st["end"], k
    return best_order, {"n_starts": len(starts), "neighbourhood": neighbourhood,
                        "best_score": best_score, "best_from_index": best_at,
                        "best_from": starts[best_at][0], "rows": rows}


# ---------------------------------------------------------------------------
# The instrument's ceiling: the hidden policy, whose optimum is known
# ---------------------------------------------------------------------------

def hidden_ceiling(space: Space, truth: dict[str, int]) -> dict[str, Any]:
    """The hidden policy written as an answer and installed as `CR-d` installs
    one, which `G-g1` proves decides the whole space right. From the 64 declared
    random starts alone, never its own order, the search must find an order that
    decides every point right. Like `rung3.optimizer_check`, it measures the
    instrument before the instrument measures anything."""
    from manual import compile as MC
    from manual import gates as MG
    eng = MC.install(MG.hidden_answer(), space).engine
    inside, around = containment(eng)
    inst = instance(eng.rules, eng.ext, inside, around, truth, space.n)
    starts = declared_starts(inst.ids, inst.inside)
    best, st = multistart(starts, inst.M, inst.W, inst.full, inst.inside, inst.around)
    got = inst.score(best)
    hits = [r["index"] for r in st["rows"] if inst.fixed + r["end_score"] == space.n]
    return {"rules": len(eng.rules), "searched": len(inst.ids),
            "contested": inst.full.bit_count(), "best": got, "n": space.n,
            "passes": got == space.n and is_linear_extension(best, inst.inside),
            "first_hit_index": hits[0] if hits else None, "n_hits": len(hits),
            "n_starts": st["n_starts"]}


# ---------------------------------------------------------------------------
# An order, installed and read
# ---------------------------------------------------------------------------

def installed_in(order: Sequence[str], rules: dict[str, Rule2], space: Space) -> PriorityEngine:
    """The rules in `order`, installed into a fresh rung 2 engine as `CR-d`
    installs an answer: added in that order, each earlier rule then declared to
    beat every later one it crosses with another queue."""
    eng = PriorityEngine(space=space)
    fresh = []
    for rid in order:
        r = rules[rid]
        nr = Rule2(rule_id=rid, conditions=list(r.conditions), action=r.action)
        eng.add(nr, born_at=r.born_at, keep_id=True)
        fresh.append(nr)
    MC.derive_edges(eng, fresh)
    return eng


def installs(order: Sequence[str], rules: dict[str, Rule2], inst: Instance,
             space: Space) -> bool:
    """Gate 2, for one order of every rule."""
    if sorted(order) != sorted(rules) or not is_linear_extension(order, inst.inside_all):
        return False
    eng = installed_in(order, rules, space)
    if any(why != EDGE_OK for _, _, why in eng.edge_log):
        return False
    s = inst.searched(order)
    got = inst.score(s)
    return (inst.right(s).bit_count() == got
            and MI.over_space(eng)["correct"] == got
            and MI.first_match_over_space([rules[r] for r in order])["correct"] == got)


def reading(right: int, space: Space, truth: dict[str, int]) -> dict[str, Any]:
    """What an order decides right: its share of the space, its right points in
    the keyword half and outside it, and every queue's recall."""
    kw = space.mask[KEYWORD][True]
    return {"share": frac(F(right.bit_count(), space.n)), "right": right.bit_count(),
            "halves": {"keyword": (right & kw).bit_count(),
                       "outside": (right & ~kw).bit_count()},
            "recall": {q: frac(share((right & truth.get(q, 0)).bit_count(),
                                     truth.get(q, 0).bit_count())) for q in ACTIONS}}


def label_masks(engine: PriorityEngine, labels: Sequence[tuple[int, str]],
                inside: dict[str, frozenset]) -> tuple[dict[str, int], dict[str, int], int]:
    """The run's labels as an instance of every rule: bit `j` is the `j`-th
    label's ticket, set in `M[r]` where `r` is undefeated by containment there,
    and in `W[r]` where its queue is also the label's."""
    corpus = MI.corpus()
    M = {r.rule_id: 0 for r in engine.rules}
    W = dict(M)
    action = {r.rule_id: r.action for r in engine.rules}
    for j, (idx, queue) in enumerate(labels):
        case = corpus[idx]
        hit = {r.rule_id for r in engine.rules if r.matches(case)}
        for rid in hit:
            if not (inside[rid] & hit):
                M[rid] |= 1 << j
                if action[rid] == queue:
                    W[rid] |= 1 << j
    return M, W, (1 << len(labels)) - 1


def by_its_labels(engine: PriorityEngine, own: list[str], labels: Sequence[tuple[int, str]],
                  inside: dict[str, frozenset], around: dict[str, frozenset]) -> dict[str, Any]:
    """The completed order, searched from there alone on the labels."""
    M, W, full = label_masks(engine, labels, inside)
    order, stats = local_search(own, M, W, full, inside, around)
    corpus = MI.corpus()
    record = 0
    for idx, queue in labels:
        outcome, winner, _ = engine.decide(corpus[idx])
        record += outcome == "ACTION" and winner.action == queue
    return {"order": order,
            "labels": {"of": len(labels), "record": record,
                       "completed": LS.score_order(own, M, W, full),
                       "searched": LS.score_order(order, M, W, full)},
            "search": {k: stats[k] for k in ("rounds", "moves", "swaps", "exhausted")}}


def read_rules(engine: PriorityEngine, space: Space, truth: dict[str, int],
               labels: Sequence[tuple[int, str]] | None = None) -> dict[str, Any]:
    """One base: the record, completed, by its labels where it has labels, with
    the truth, and the bound; and gates 2 to 4 for it."""
    rules = {r.rule_id: r for r in engine.rules}
    inside, around = containment(engine)
    inst = instance(engine.rules, engine.ext, inside, around, truth, space.n)
    rec = MI.right_mask(engine)
    own = completed(engine)
    orders: dict[str, list[str]] = {"completed": own}
    out: dict[str, Any] = {"rules": len(rules), "searched": len(inst.ids),
                           "contested": inst.full.bit_count(), "fixed_right": inst.fixed,
                           "record": reading(rec, space, truth)}
    if labels is not None:
        lab = by_its_labels(engine, own, labels, inside, around)
        orders["by_its_labels"] = lab["order"]
    best, ms = multistart(declared_starts(inst.ids, inst.inside, first=inst.searched(own)),
                          inst.M, inst.W, inst.full, inst.inside, inst.around)
    orders["with_the_truth"] = inst.whole(best)
    for name, order in orders.items():
        out[name] = reading(inst.right(inst.searched(order)), space, truth)
    if labels is not None:
        out["by_its_labels"].update(labels=lab["labels"], search=lab["search"])
    out["with_the_truth"]["search"] = {
        **{k: v for k, v in ms.items() if k != "rows"},
        "fixed": inst.fixed,
        "rows": [{k: r[k] for k in ("start", "start_score", "end_score", "rounds", "moves",
                                    "swaps", "exhausted")} for r in ms["rows"]]}
    bound = coverage(inst)
    out["bound"] = {"share": frac(F(bound, space.n)), "right": bound}
    out["orders"] = {k: list(v) for k, v in orders.items() if k != "completed"}
    out["gates"] = {
        "installs": all(installs(o, rules, inst, space) for o in orders.values()),
        "completing_loses_nothing": rec & ~inst.right(inst.searched(own)) == 0,
        "bound_bounds": all(out[k]["right"] <= bound for k in ("record", *orders))}
    return out


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "shape.json"


def inputs(tag: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    k = L_RUNS.index(tag) + 1
    return (json.loads(plan.run_path(plan.LABELLED, k).read_text()),
            json.loads(LY.session_path(tag).read_text()),
            json.loads(plan.score_path().read_text()))


def answers_at_all(session: dict[str, Any], labels: int) -> list[tuple[int, dict[str, Any]]]:
    """The at-once answers `CR-d` reads: each ask's first valid answer in re-ask
    order, at all of the run's labels."""
    return [(k, row) for j, k, row in LY.chosen(session) if j == labels]


def stage_c(tag: str) -> dict[str, Any]:
    """Gate 1: the loop's final base and the three answers are Stage C's."""
    record, session, score = inputs(tag)
    labels = len(ask.labelled(record))
    loop = MI.over_space(MI.final_engine(record))
    kept_loop = F(score["CR-g"]["runs"][tag]["space"]["fraction"])
    curve = score["CR-g"]["curves"][tag]
    kept = next(c for c in curve if c["labels"] == labels)["at_once"]["asks"]
    answers = answers_at_all(session, labels)
    ok = F(loop["correct"], loop["n"]) == kept_loop and len(kept) == len(answers) == 3
    for (_, row), s in zip(answers, kept):
        inst = LY.installed(row["payload"])
        sp = MI.over_space(inst.engine)
        ok &= F(s["space"]["fraction"]) == F(sp["correct"], sp["n"])
        ok &= s["installed"] == inst.summary()
    return {"gate": 1, "what": "the bases are Stage C's", "passes": bool(ok)}


def read_run(tag: str) -> dict[str, Any]:
    """One L run: its final base and its three at-once answers at all labels,
    each read, with gates 1 to 4. It runs in a process of its own."""
    record, session, _ = inputs(tag)
    space, truth = MI.space(), MI.space_truth()
    labels = ask.labelled(record)
    loop = read_rules(MI.final_engine(record), space, truth, labels=labels)
    asks = [{"k": k, **read_rules(LY.installed(row["payload"]).engine, space, truth)}
            for k, row in answers_at_all(session, len(labels))]
    g = {"installs": True, "completing_loses_nothing": True, "bound_bounds": True}
    for x in [loop, *asks]:
        for key in g:
            g[key] &= x["gates"][key]
    gates = [stage_c(tag),
             {"gate": 2, "what": "every order is one the engine installs", "passes": g["installs"]},
             {"gate": 3, "what": "completing loses nothing", "passes": g["completing_loses_nothing"]},
             {"gate": 4, "what": "the bound bounds", "passes": g["bound_bounds"]}]

    def med(key: str) -> dict[str, Any] | None:
        return frac(median([F(a[key]["share"]["fraction"]) for a in asks])) if asks else None

    gains = [F(a["with_the_truth"]["share"]["fraction"]) - F(a["record"]["share"]["fraction"])
             for a in asks]
    return {"labels": len(labels), "loop": loop, "at_once": asks,
            "at_once_median": {k: med(k) for k in ("record", "completed", "with_the_truth", "bound")}
            | {"gain_with_the_truth": frac(median(gains)) if gains else None},
            "gates": gates}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(runs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    def value(x: dict[str, Any] | None) -> Fraction | None:
        return None if x is None else F(x["fraction"])

    got: dict[str, dict[str, Any]] = {}
    for t in L_RUNS:
        r = runs.get(t)
        if r is None:
            continue
        lp = r["loop"]
        at = value(r["at_once_median"]["record"])
        rec = value(lp["record"]["share"])
        got[t] = {"at_once": at, "record": rec, "gap": None if at is None else at - rec,
                  "bound": value(lp["bound"]["share"]),
                  "completed": value(lp["completed"]["share"]),
                  "by_its_labels": value(lp["by_its_labels"]["share"]),
                  "with_the_truth": value(lp["with_the_truth"]["share"]),
                  "keyword_gain": lp["with_the_truth"]["halves"]["keyword"]
                  - lp["record"]["halves"]["keyword"],
                  "outside_gain": lp["with_the_truth"]["halves"]["outside"]
                  - lp["record"]["halves"]["outside"],
                  "answers_gain": value(r["at_once_median"]["gain_with_the_truth"])}
    every = bool(got) and len(got) == len(L_RUNS)

    def each(test) -> bool:
        return every and all(test(x) for x in got.values())

    def known(*keys):
        return lambda x: all(x[k] is not None for k in keys)

    s1 = each(lambda x: known("bound", "at_once")(x) and x["bound"] >= x["at_once"])
    s2 = each(lambda x: known("with_the_truth", "at_once")(x) and x["with_the_truth"] >= x["at_once"])
    s3_runs = [t for t, x in got.items() if known("completed", "record", "gap")(x)
               and x["completed"] - x["record"] >= x["gap"] / 2]
    s4 = each(lambda x: known("by_its_labels", "at_once")(x) and x["by_its_labels"] < x["at_once"])
    s5_runs = ("l_r1", "l_r2")
    s5 = all(t in got and got[t]["keyword_gain"] > got[t]["outside_gain"] for t in s5_runs)
    s6 = each(lambda x: known("answers_gain", "with_the_truth", "record")(x)
              and x["answers_gain"] < x["with_the_truth"] - x["record"])

    def shown(keys):
        return {t: {k: (frac(x[k]) if isinstance(x[k], Fraction) else x[k]) for k in keys}
                for t, x in got.items()}

    return [
        {"clause": "S1", "what": "in every L run, the loop's bound is at least at once",
         "reading": shown(("bound", "at_once")), "holds": s1},
        {"clause": "S2", "what": "in every L run, the loop's rules with the truth decide at least "
                                 "as much of the space as at once",
         "reading": shown(("with_the_truth", "at_once")), "holds": s2},
        {"clause": "S3", "what": "in at least two of L's runs, completing the loop's base gives "
                                 "back at least half of the gap",
         "reading": {**shown(("completed", "record", "gap")), "runs": s3_runs},
         "holds": len(s3_runs) >= 2},
        {"clause": "S4", "what": "in every L run, the loop's base by its labels decides less of "
                                 "the space than at once",
         "reading": shown(("by_its_labels", "at_once")), "holds": s4},
        {"clause": "S5", "what": "in L r1 and in L r2, the points the loop's rules with the truth "
                                 "decide right, less the record's, are more in the keyword half "
                                 "than outside it",
         "reading": shown(("keyword_gain", "outside_gain")), "holds": s5},
        {"clause": "S6", "what": "in every L run, the median answer's gain with the truth over its "
                                 "record is smaller than the loop's",
         "reading": shown(("answers_gain", "with_the_truth", "record")), "holds": s6},
    ]


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Shape or order: what the loop's own rules could "
                                             "decide, ordered (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 5 and 1 and stop; writes nothing")
    ap.add_argument("--processes", type=int, default=PROCESSES,
                    help="processes to search the runs in, one run each; 1 searches them in "
                         "this one. The record is the same")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"corrections/shape.py writes {record_path()}")
    space, truth = MI.space(), MI.space_truth()
    ceiling = hidden_ceiling(space, truth)
    print(f"  gate 5: {'PASS' if ceiling['passes'] else 'FAIL'}  the search finds the hidden "
          f"policy's optimum from the declared random starts ({ceiling['n_hits']} of "
          f"{ceiling['n_starts']}, first at {ceiling['first_hit_index']})")
    if not ceiling["passes"]:
        sys.exit("\nREFUSED: the search does not find a known optimum; nothing was written.\n")
    if args.dry_run:
        ones = [{"run": t, **stage_c(t)} for t in L_RUNS]
        for g in ones:
            print(f"  gate 1 run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
        print("\ndry run: nothing written")
        return 0 if all(g["passes"] for g in ones) else 1
    if args.processes > 1:
        with get_context("fork").Pool(min(args.processes, len(L_RUNS))) as pool:
            runs = dict(zip(L_RUNS, pool.map(read_run, L_RUNS)))
    else:
        runs = {t: read_run(t) for t in L_RUNS}
    checked = [{"run": t, **g} for t, r in runs.items() for g in r["gates"]] + [
        {"gate": 5, "run": None, "what": "the search finds the known optimum",
         "passes": ceiling["passes"]}]
    for g in checked:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(runs)
    _, _, score = inputs(L_RUNS[0])
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(plan.LABELLED, k))
                            for k, t in enumerate(L_RUNS, start=1)},
                   "sessions": {t: str(LY.session_path(t)) for t in L_RUNS}},
        "surface": "the whole space, 134,400 points: each L run's final base and its three "
                   "at-once answers at all labels, as CR-d reads them, each read in the orders "
                   "rung 2's engine can install",
        "constants": {"MULTISTART_SEED": LS.MULTISTART_SEED,
                      "MULTISTART_STARTS": LS.MULTISTART_STARTS,
                      "DECLARED_NEIGHBOURHOOD": LS.DECLARED_NEIGHBOURHOOD,
                      "processes": args.processes},
        "ceiling": ceiling,
        "gates": checked,
        "runs": runs,
        "expectation": expectation,
    }), indent=2, default=fg.plain) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    for t, r in runs.items():
        lp, am = r["loop"], r["at_once_median"]
        print(f"  {t}: at once {am['record']['value']:.4f}; the loop's record "
              f"{lp['record']['share']['value']:.4f}, completed {lp['completed']['share']['value']:.4f}, "
              f"by its labels {lp['by_its_labels']['share']['value']:.4f}, with the truth "
              f"{lp['with_the_truth']['share']['value']:.4f}, bound {lp['bound']['share']['value']:.4f}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
