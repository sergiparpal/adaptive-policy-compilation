"""
The certificate of `PLAN_BOUND.md`: cases lost under EVERY order, counted
without a solver.

--------------------------------------------------------------------------
WHAT IS BOUNDED
--------------------------------------------------------------------------
An instance is what `rung3/local_search.py` searches: per rule, M[r] the mask of
the cases whose pool it is in, and W[r] the subset it gets right. Under
first-match-wins over a total order, a case is decided by the first rule of its
pool, and the score counts the cases whose winner is in W. The coverage bound
counts the cases some rule of the pool gets right. It is valid, and no order is
known to reach it: `results3/FINDINGS3.md`, §1 and §4 errata.

This module certifies a number `nu` of coverable cases that every order loses,
so that

    best order  <=  coverage bound - nu.

--------------------------------------------------------------------------
THE ARGUMENT
--------------------------------------------------------------------------
For a case c, let R(c) be the rules of its pool that get it right and X(c) the
ones that get it wrong. Under an order, c is right iff the first rule of R(c)
comes before every rule of X(c).

A CYCLE is a sequence of cases c_1, ..., c_m (m >= 2) with

    R(c_{i+1})  is a subset of  X(c_i)          (indices modulo m).

No order gets all of them right. If c_i is right, the first rule of R(c_i)
precedes every rule of X(c_i), so in particular every rule of R(c_{i+1}), so it
precedes the first rule of R(c_{i+1}). Around the cycle that is a strict order
that returns to its start.

The hard edges `IDEAS.md` names are the case |R(c)| = 1: the one right rule
precedes every wrong rule. Containment is what lets a case with several right
rules join a cycle too, and it reduces to the hard edge when R has one rule.

Cases with the same R and X are decided alike by every order; they form a
SIGNATURE, and the number of its cases is its capacity. A PACKING gives each
cycle a multiplicity y > 0 and asks, for each signature, that the multiplicities
of the cycles it appears in add up to at most its capacity. Then every order
loses at least the sum of the y. Fix an order; each cycle has a signature it
gets wrong, and all of that signature's cases are lost. Charge the cycle's y to
that signature: each lost signature is charged at most its capacity, and its
capacity is cases lost.

So the certificate is a list of cycles with multiplicities. Anyone can check it
from the masks alone, and `verify` does, by a route that shares nothing with
`find` but the masks.

--------------------------------------------------------------------------
THE HYBRID POOL, AND WHY NO SUBSUMPTION EDGE ENTERS
--------------------------------------------------------------------------
`IDEAS.md` says that in the hybrid pool subsumption's edges join the graph and
cannot yield. That describes rung 2's engine, not the code behind rung 3's
`hibrido` figures. `rung3/order_search.build_tables` cuts each case's pool down
to the rules no matching rule strictly subsumes, and the order then decides
among those with no constraint. A rule and one it strictly subsumes are never in
the same pool, so their relative order never changes a score, and an edge that
forced it would close cycles that cost nothing. The certificate therefore takes
the hybrid instance's masks as they are, like the pure ones.

--------------------------------------------------------------------------
HOW THE CYCLES ARE FOUND — a heuristic, and validity does not depend on it
--------------------------------------------------------------------------
Rules with the same M and the same W are interchangeable: every order decides
every case alike whichever of them comes first. They are merged into one class
before anything else, so copies do not turn single-right cases into
several-right ones.

The graph: one node per distinct R among the contested cases. Node A points to
node B through signature k when R(k) = A and B is a subset of X(k); k is the
edge's label. A simple cycle of nodes uses one label per node, so its labels are
distinct signatures, and their cases form a cycle as above.

The packing is greedy, and every choice in it was fixed before any figure of
the plan existed:

  1. Cycle length L = 2, 3, 4, ... For each L, the nodes of every non-trivial
     strongly connected component are taken in the start's order, and while a
     cycle of at most L nodes passes through one, the shortest is packed
     (breadth-first search, neighbours visited in index order).
  2. Each edge of the cycle takes, among its live labels, the one that labels
     the fewest edges, so that a label other cycles could use is spent last;
     then the one with the most capacity left; then the lowest index. The
     cycle's multiplicity is the least capacity among its labels, and that much
     is taken from each. A label with nothing left is dead.
  3. Packing removes capacity and never adds an edge, so a node with no cycle of
     at most L through it has none later in the same pass. When no strongly
     connected component is left, no cycle is left, and the packing stops.
  4. The STARTS: the packing runs once with the nodes in index order and
     `FINDER_STARTS` more times with them shuffled by `random.Random(
     FINDER_SEED)`, and keeps the largest `nu`, the earliest on a tie. Every
     start's packing is a valid certificate, so keeping the largest is not a
     selection that could overstate anything: `verify` checks the one kept.

Both rules in 2 and the starts in 4 were chosen on synthetic data before the
plan existed: on 3,000 random instances small enough to enumerate every order,
the packing reached the exact loss in 2,318 with the most-capacity label and the
index order alone, and in 2,590 with the rule and the starts above. The
synthetic data is described in `PLAN_BOUND.md` §5.7. None of it is rung 1's.

Nodes are indexed by their sorted rules and signatures by their lowest case, so
nothing depends on PYTHONHASHSEED.
"""

from __future__ import annotations

import random
import re
from collections import defaultdict
from dataclasses import dataclass

# The starts of the packing (step 4 of the header), declared before any figure.
FINDER_SEED = 17
FINDER_STARTS = 16

# ---------------------------------------------------------------------------
# Bits
# ---------------------------------------------------------------------------

_ONE = re.compile("1")


def ones(x: int) -> list[int]:
    """Positions of the set bits of `x`, ascending; bit 0 is the least
    significant. One pass over the binary string, so it costs the same for a
    mask of 577 rules and one of 134,400 cases."""
    if not x:
        return []
    s = format(x, "b")[::-1]
    return [m.start() for m in _ONE.finditer(s)]


# ---------------------------------------------------------------------------
# The instance, in classes and signatures
# ---------------------------------------------------------------------------

@dataclass
class Instance:
    """What an order is scored on: `score_order(order, M, W, full)`."""
    name: str
    ids: list
    M: dict
    W: dict
    n: int

    @property
    def full(self) -> int:
        return (1 << self.n) - 1


def classes(inst: Instance) -> list[tuple[tuple, int, int]]:
    """Interchangeable rules merged: one class per distinct (M, W), with its
    members sorted. Rules whose pool is empty decide nothing and are left out.
    Classes are sorted by their first member."""
    groups = defaultdict(list)
    for rid in inst.ids:
        if inst.M[rid]:
            groups[(inst.M[rid], inst.W[rid])].append(rid)
    out = [(tuple(sorted(g)), m, w) for (m, w), g in groups.items()]
    out.sort(key=lambda t: t[0][0])
    return out


@dataclass
class Signatures:
    """The cases split by what every order does with them.

    `keys[k]` is (R, X): the classes that get signature k right and wrong, as
    sorted tuples of class indices. `weight[k]` is its number of cases and
    `rep[k]` its lowest case index. Only contested cases have a signature:
    some class right and some wrong."""
    n_classes: int
    keys: list
    weight: list
    rep: list
    coverable: int      # cases some class gets right: the coverage bound
    uncontested: int    # coverable cases no class gets wrong: won by every order


def signatures(inst: Instance, cls=None) -> Signatures:
    cls = classes(inst) if cls is None else cls
    match = [[] for _ in range(inst.n)]
    right = [[] for _ in range(inst.n)]
    for j, (_, m, w) in enumerate(cls):
        for c in ones(m):
            match[c].append(j)
        for c in ones(w):
            right[c].append(j)
    index: dict = {}
    keys, weight, rep = [], [], []
    coverable = uncontested = 0
    for c in range(inst.n):
        r = right[c]
        if not r:
            continue
        coverable += 1
        p = match[c]
        if len(p) == len(r):
            uncontested += 1
            continue
        rs = set(r)
        key = (tuple(r), tuple(j for j in p if j not in rs))
        k = index.get(key)
        if k is None:
            index[key] = len(keys)
            keys.append(key)
            weight.append(1)
            rep.append(c)
        else:
            weight[k] += 1
    return Signatures(len(cls), keys, weight, rep, coverable, uncontested)


# ---------------------------------------------------------------------------
# The finder
# ---------------------------------------------------------------------------

def _mask(items) -> int:
    m = 0
    for i in items:
        m |= 1 << i
    return m


class _Graph:
    """Nodes, labels and live edges of the packing."""

    def __init__(self, sig: Signatures):
        node_of_r = {}
        for r, _ in sig.keys:
            node_of_r.setdefault(r, None)
        self.node_keys = sorted(node_of_r)
        idx = {r: v for v, r in enumerate(self.node_keys)}
        self.V = len(self.node_keys)
        self.node_mask = [_mask(r) for r in self.node_keys]

        self.cap = list(sig.weight)
        self.node = [idx[r] for r, _ in sig.keys]
        xmask = [_mask(x) for _, x in sig.keys]

        by_low: dict[int, list[int]] = defaultdict(list)
        for v, r in enumerate(self.node_keys):
            by_low[r[0]].append(v)

        # labels[v][u]: the signatures of node v whose X contains node u, in
        # index order; live[v][u]: how many of them have capacity left. A
        # signature's index follows its lowest case, so this is case order.
        self.labels: list[dict[int, list[int]]] = [dict() for _ in range(self.V)]
        self.live: list[dict[int, int]] = [dict() for _ in range(self.V)]
        self.targets: list[list[int]] = []
        for k, (_, x_items) in enumerate(sig.keys):
            x = xmask[k]
            tk = []
            for low in x_items:
                for u in by_low.get(low, ()):
                    if self.node_mask[u] & ~x == 0:
                        tk.append(u)
            tk.sort()
            self.targets.append(tk)
            v = self.node[k]
            for u in tk:
                self.labels[v].setdefault(u, []).append(k)
                self.live[v][u] = self.live[v].get(u, 0) + 1
        self.out = [_mask(self.live[v]) for v in range(self.V)]

    def kill(self, k: int) -> None:
        v = self.node[k]
        for u in self.targets[k]:
            left = self.live[v][u] - 1
            if left:
                self.live[v][u] = left
            else:
                del self.live[v][u]
                self.out[v] &= ~(1 << u)

    def label(self, v: int, u: int) -> int:
        """Step 2 of the header: fewest edges labelled, then most capacity
        left, then lowest index."""
        best, best_key = None, None
        for k in self.labels[v][u]:
            c = self.cap[k]
            if c <= 0:
                continue
            key = (len(self.targets[k]), -c, k)
            if best_key is None or key < best_key:
                best, best_key = k, key
        assert best is not None, "a live edge with no live label"
        return best

    def sccs(self) -> list[list[int]]:
        """Non-trivial strongly connected components of the live graph, each
        sorted, in order of their lowest node. Iterative Tarjan."""
        index = [-1] * self.V
        low = [0] * self.V
        on = [False] * self.V
        stack, comps, counter = [], [], 0
        for root in range(self.V):
            if index[root] != -1 or not self.out[root]:
                continue
            work = [(root, iter(ones(self.out[root])))]
            index[root] = low[root] = counter
            counter += 1
            stack.append(root)
            on[root] = True
            while work:
                v, it = work[-1]
                pushed = False
                for u in it:
                    if index[u] == -1:
                        index[u] = low[u] = counter
                        counter += 1
                        stack.append(u)
                        on[u] = True
                        work.append((u, iter(ones(self.out[u]))))
                        pushed = True
                        break
                    if on[u] and index[u] < low[v]:
                        low[v] = index[u]
                if pushed:
                    continue
                work.pop()
                if work:
                    p = work[-1][0]
                    if low[v] < low[p]:
                        low[p] = low[v]
                if low[v] == index[v]:
                    comp = []
                    while True:
                        u = stack.pop()
                        on[u] = False
                        comp.append(u)
                        if u == v:
                            break
                    if len(comp) > 1:
                        comps.append(sorted(comp))
        comps.sort(key=lambda c: c[0])
        return comps

    def shortest_cycle(self, s: int, within: int, max_len: int) -> list[int] | None:
        """The shortest cycle through `s` of at most `max_len` nodes, inside
        `within`, as its nodes from `s` on; None if there is none."""
        sbit = 1 << s
        visited = sbit
        parent = {}
        frontier = [s]
        for _ in range(2, max_len + 1):
            nxt = []
            for v in frontier:
                new = self.out[v] & within & ~visited
                if new:
                    visited |= new
                    for u in ones(new):
                        parent[u] = v
                        nxt.append(u)
            if not nxt:
                return None
            frontier = nxt
            for v in frontier:
                if self.out[v] & sbit:
                    path = [v]
                    while path[-1] != s:
                        path.append(parent[path[-1]])
                    path.reverse()
                    return path
        return None

    def pack(self, cycle: list[int]) -> tuple[int, list[int]]:
        m = len(cycle)
        labs = [self.label(cycle[i], cycle[(i + 1) % m]) for i in range(m)]
        y = min(self.cap[k] for k in labs)
        for k in labs:
            self.cap[k] -= y
            if self.cap[k] == 0:
                self.kill(k)
        return y, labs


def find(sig: Signatures, rank: list[int] | None = None
         ) -> list[tuple[int, list[int]]]:
    """One greedy packing, steps 1 to 3 of the header. `rank` orders the nodes
    within each component; None is index order. Returns (y, [signature
    indices]) per cycle, in the order the signatures follow each other around
    it."""
    if not sig.keys:
        return []
    g = _Graph(sig)
    cycles = []
    L = 2
    while True:
        comps = g.sccs()
        if not comps:
            break
        for comp in comps:
            within = _mask(comp)
            nodes = comp if rank is None else sorted(comp, key=rank.__getitem__)
            for s in nodes:
                while True:
                    cyc = g.shortest_cycle(s, within, L)
                    if cyc is None:
                        break
                    cycles.append(g.pack(cyc))
        L += 1
    return cycles


def n_nodes(sig: Signatures) -> int:
    return len({r for r, _ in sig.keys})


def best_packing(sig: Signatures, seed: int = FINDER_SEED,
                 starts: int = FINDER_STARTS) -> tuple[list, list[int]]:
    """Step 4 of the header: index order, then `starts` seeded shuffles of the
    nodes; the packing with the largest nu, the earliest on a tie. Returns it
    and every start's nu, in start order."""
    V = n_nodes(sig)
    rng = random.Random(seed)
    ranks: list[list[int] | None] = [None]
    for _ in range(starts):
        perm = list(range(V))
        rng.shuffle(perm)
        rank = [0] * V
        for pos, v in enumerate(perm):
            rank[v] = pos
        ranks.append(rank)
    best, best_nu, nus = [], -1, []
    for rank in ranks:
        cycles = find(sig, rank)
        nu = sum(y for y, _ in cycles)
        nus.append(nu)
        if nu > best_nu:
            best, best_nu = cycles, nu
    return best, nus


# ---------------------------------------------------------------------------
# The certificate and its check
# ---------------------------------------------------------------------------

def certificate(inst: Instance) -> dict:
    """Find a packing and write it in terms of cases: each cycle is its
    multiplicity and one representative case per signature. Nothing in it
    refers to classes or signature indices, so `verify` can rebuild every
    signature from the masks."""
    cls = classes(inst)
    sig = signatures(inst, cls)
    cycles, nus = best_packing(sig)
    nu = sum(y for y, _ in cycles)
    lengths = defaultdict(int)
    for y, labs in cycles:
        lengths[len(labs)] += y
    return {
        "instance": inst.name,
        "n": inst.n,
        "n_rules": len(inst.ids),
        "n_classes": len(cls),
        "coverable": sig.coverable,
        "uncontested": sig.uncontested,
        "contested": sig.coverable - sig.uncontested,
        "n_signatures": len(sig.keys),
        "n_singleton_signatures": sum(1 for r, _ in sig.keys if len(r) == 1),
        "cases_in_singleton_signatures": sum(
            w for (r, _), w in zip(sig.keys, sig.weight) if len(r) == 1),
        "n_nodes": n_nodes(sig),
        "nu": nu,
        "bound": sig.coverable - nu,
        "nu_by_start": nus,
        "best_start": nus.index(nu) if nus else None,
        "n_cycles": len(cycles),
        "nu_by_length": {str(L): v for L, v in sorted(lengths.items())},
        "cycles": [[y, [sig.rep[k] for k in labs]] for y, labs in cycles],
    }


def _pattern(inst: Instance, c: int) -> tuple[frozenset, frozenset]:
    """(R, X) of case c in rule ids, read off the masks one bit at a time."""
    r, x = set(), set()
    for rid in inst.ids:
        if (inst.M[rid] >> c) & 1:
            (r if (inst.W[rid] >> c) & 1 else x).add(rid)
    return frozenset(r), frozenset(x)


def _capacity(inst: Instance, r: frozenset, x: frozenset) -> int:
    """How many cases have exactly this R and this X: an AND over every rule
    of the instance, with no reference to how `find` grouped anything."""
    acc = inst.full
    for rid in inst.ids:
        m, w = inst.M[rid], inst.W[rid]
        if rid in r:
            acc &= w
        elif rid in x:
            acc &= m & ~w
        else:
            acc &= ~m
        if not acc:
            return 0
    return acc.bit_count()


def verify(inst: Instance, cert: dict) -> dict:
    """Check a certificate from the masks alone. Returns {"ok", "nu",
    "coverable", "problems"}; `nu` is the sum of the multiplicities of the
    cycles that pass, and `ok` says every one did."""
    problems: list[str] = []
    coverable = 0
    for rid in inst.ids:
        coverable |= inst.W[rid]
    coverable = coverable.bit_count()
    if cert.get("coverable") != coverable:
        problems.append(f"coverable {cert.get('coverable')} != {coverable}")
    if cert.get("n") != inst.n:
        problems.append(f"n {cert.get('n')} != {inst.n}")

    patterns: dict[int, tuple[frozenset, frozenset]] = {}
    used: dict[tuple[frozenset, frozenset], int] = defaultdict(int)
    nu = 0
    for j, (y, cases) in enumerate(cert["cycles"]):
        bad = None
        if not isinstance(y, int) or y <= 0:
            bad = f"multiplicity {y!r}"
        elif len(cases) < 2:
            bad = "fewer than two cases"
        elif any(not (0 <= c < inst.n) for c in cases):
            bad = "a case outside the instance"
        if bad is None:
            pats = []
            for c in cases:
                if c not in patterns:
                    patterns[c] = _pattern(inst, c)
                pats.append(patterns[c])
            for i, (r, x) in enumerate(pats):
                if not r or not x:
                    bad = f"case {cases[i]} is not contested"
                    break
                if not pats[(i + 1) % len(pats)][0] <= x:
                    bad = f"R of case {cases[(i + 1) % len(cases)]} not inside X of case {cases[i]}"
                    break
        if bad is not None:
            problems.append(f"cycle {j}: {bad}")
            continue
        for p in set(pats):
            used[p] += y
        nu += y

    for (r, x), u in used.items():
        cap = _capacity(inst, r, x)
        if u > cap:
            problems.append(f"signature used {u} times, capacity {cap}")
    if cert.get("nu") != nu:
        problems.append(f"nu {cert.get('nu')} != {nu}")
    return {"ok": not problems, "nu": nu, "coverable": coverable,
            "problems": problems}


# ---------------------------------------------------------------------------
# Exact optimum, for instances small enough to enumerate
# ---------------------------------------------------------------------------

def brute_force(inst: Instance) -> int:
    """The best score over every order of the classes. Interchangeable rules
    are one class, so this is the best over every order of the rules."""
    from itertools import permutations
    cls = classes(inst)
    best = 0
    full = inst.full
    for perm in permutations(range(len(cls))):
        remaining, ok = full, 0
        for j in perm:
            m, w = cls[j][1], cls[j][2]
            fires = m & remaining
            if fires:
                ok += (w & fires).bit_count()
                remaining ^= fires
                if not remaining:
                    break
        best = max(best, ok)
    return best
