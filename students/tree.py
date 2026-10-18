"""
THE TREE — a pruned decision tree, `PLAN_STUDENTS.md` §3.1.

It is trained on tickets and labels and on nothing else. Every choice is the
plan's, fixed before any figure: binary splits over the attributes in
`ATTRIBUTES` order, the lowest weighted Gini impurity computed exactly in
rationals, plurality leaves, and minimal cost-complexity pruning (Breiman et
al., 1984) with the cost chosen by five folds grouped by ticket.

--------------------------------------------------------------------------
THE SPLITS
--------------------------------------------------------------------------
`attr lte t` for the two numeric attributes, at every value of the domain but
the last; `attr eq True` for the two booleans; `attr eq v` for every value of
the other four. The left branch is where the condition holds. A split must
leave both branches non-empty. Ties in impurity go to the first split in that
order, and a split that lowers nothing is still taken while the node is impure:
growth stops at purity, or where every ticket at the node is the same ticket.

Impurity is compared exactly. Splitting `n` labels into `L` and `R`, the
weighted Gini impurity is `n − (S_L/n_L + S_R/n_R)`, with `S` the sum of the
squared class counts, so the split chosen is the one with the largest
`S_L/n_L + S_R/n_R`, as a `Fraction`. No float decides a split, which is what
keeps the tree the same under 3.10 and 3.12.

--------------------------------------------------------------------------
THE PRUNING
--------------------------------------------------------------------------
`R(t)` is the number of training labels misclassified at `t` were it a leaf.
Weakest-link pruning collapses, at each step, every internal node whose
`g(t) = (R(t) − R(T_t)) / (|T_t| − 1)` is the smallest, which gives the
sequence of subtrees and its costs `α₀ = 0 < α₁ < … < α_K`. The first subtree
is the smallest of the full tree's with its training error.

The cost is chosen by the folds of `folds`. Each fold grows and prunes its own
tree on the other four, and the full tree's `k` is scored by the held-out
labels the fold's subtree at `β_k = √(α_k·α_{k+1})` misclassifies, with
`β_K = ∞`. The fold's subtree at `β` is the last of its sequence whose cost is
at most `β`, compared on squares so that no square root is taken. **The `k`
with the fewest misclassified wins, and ties go to the larger `k`**, the smaller
tree.

--------------------------------------------------------------------------
THE TREE IS A RULE BASE
--------------------------------------------------------------------------
`rules` writes every leaf as one rule of `harness.dsl`, merging the conditions
on its path to at most one per attribute, so that no rule passes the frozen
validator's limit of eight. A numeric range bounded on both sides is one `in`. The leaves are disjoint
and cover the space, so every engine in the repository decides them alike.
`students/gates.py` checks that the frozen `harness.dsl.RuleEngine` executes
them as the tree predicts.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Iterable, Sequence

from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, NUMERIC_ATTRS, Case
from harness.dsl import validate_rule_payload

from . import plan

A = len(ATTRIBUTES)
CATCH_ALL = {"attr": "severity", "op": "gte", "value": 1}


# ---------------------------------------------------------------------------
# Encoding, splits and folds
# ---------------------------------------------------------------------------

def encode(case: Case) -> tuple[int, ...]:
    """A ticket as the index of each of its values in its domain."""
    return tuple(DOMAINS[a].index(getattr(case, a)) for a in ATTRIBUTES)


def candidate_splits() -> list[tuple[int, str, int]]:
    """`(attribute, kind, value index)` in the plan's order. `lte` holds where
    the value's index is at most the split's; `eq` where it equals it."""
    out = []
    for a, attr in enumerate(ATTRIBUTES):
        dom = DOMAINS[attr]
        if attr in NUMERIC_ATTRS:
            out.extend((a, "lte", v) for v in range(len(dom) - 1))
        elif dom == [False, True]:
            out.append((a, "eq", 1))
        else:
            out.extend((a, "eq", v) for v in range(len(dom)))
    return out


SPLITS = candidate_splits()


def holds(split: tuple[int, str, int], x: Sequence[int]) -> bool:
    a, kind, v = split
    return x[a] <= v if kind == "lte" else x[a] == v


def folds(tickets: Sequence[tuple], k: int = plan.FOLDS,
          seed: int = plan.FOLD_SEED) -> list[int]:
    """The fold of every example: the distinct tickets, sorted, shuffled by
    `random.Random(seed)` and dealt in turn, so that copies of a ticket never sit
    on both sides of a fold. Shared by the tree and the regression."""
    keys = sorted(set(tickets))
    rng = random.Random(seed)
    rng.shuffle(keys)
    of = {key: j % k for j, key in enumerate(keys)}
    return [of[t] for t in tickets]


# ---------------------------------------------------------------------------
# Growth
# ---------------------------------------------------------------------------

@dataclass
class Node:
    counts: tuple[int, ...]               # training labels by class index
    label: int                            # the plurality, tie-broken
    split: tuple[int, str, int] | None = None
    left: int | None = None               # node ids
    right: int | None = None

    @property
    def n(self) -> int:
        return sum(self.counts)

    @property
    def errors(self) -> int:
        """`R(t)`: labels misclassified here, were this node a leaf."""
        return self.n - self.counts[self.label]


@dataclass
class Tree:
    nodes: list[Node]
    collapsed: frozenset = field(default_factory=frozenset)

    def is_leaf(self, t: int) -> bool:
        return self.nodes[t].split is None or t in self.collapsed

    def leaf_of(self, x: Sequence[int]) -> int:
        t = 0
        while not self.is_leaf(t):
            node = self.nodes[t]
            t = node.left if holds(node.split, x) else node.right
        return t

    def predict_index(self, x: Sequence[int]) -> int:
        return self.nodes[self.leaf_of(x)].label

    def predict(self, case: Case) -> str:
        return ACTIONS[self.predict_index(encode(case))]

    def leaves(self) -> list[int]:
        out, stack = [], [0]
        while stack:
            t = stack.pop()
            if self.is_leaf(t):
                out.append(t)
            else:
                stack.extend((self.nodes[t].right, self.nodes[t].left))
        return out

    def subtree(self, collapsed: frozenset) -> "Tree":
        return Tree(self.nodes, collapsed)


def plurality(counts: Sequence[int], prior: Sequence[int]) -> int:
    """The class with most labels; ties to the class more common in the whole
    training set, then to `ACTIONS` order."""
    return max(range(len(counts)), key=lambda c: (counts[c], prior[c], -c))


def grow(X: Sequence[Sequence[int]], y: Sequence[int]) -> Tree:
    """The full tree over `X` (encoded tickets) and `y` (class indices)."""
    C = len(ACTIONS)
    prior = [0] * C
    for c in y:
        prior[c] += 1
    cols = [[x[a] for x in X] for a in range(A)]
    nodes: list[Node] = []
    work: list[tuple[int, list[int]]] = []

    def make(idx: list[int]) -> int:
        counts = [0] * C
        for i in idx:
            counts[y[i]] += 1
        nodes.append(Node(tuple(counts), plurality(counts, prior)))
        work.append((len(nodes) - 1, idx))
        return len(nodes) - 1

    make(list(range(len(y))))
    while work:
        t, idx = work.pop()
        node = nodes[t]
        if max(node.counts) == node.n:
            continue                                  # pure
        best = best_split(idx, cols, y, node.counts)
        if best is None:
            continue                                  # one ticket, many labels
        a, kind, v = best
        col = cols[a]
        if kind == "lte":
            left = [i for i in idx if col[i] <= v]
            right = [i for i in idx if col[i] > v]
        else:
            left = [i for i in idx if col[i] == v]
            right = [i for i in idx if col[i] != v]
        node.split = best
        node.left = make(left)
        node.right = make(right)
    return Tree(nodes)


def _sum_sq(counts: Iterable[int]) -> int:
    return sum(c * c for c in counts)


def best_split(idx: list[int], cols, y, counts) -> tuple[int, str, int] | None:
    """The split of the plan's order with the largest `S_L/n_L + S_R/n_R`, both
    sides non-empty; `None` if no split separates the node."""
    n = len(idx)
    total = list(counts)
    yy = [y[i] for i in idx]
    by_attr = []
    for a in range(A):
        col = cols[a]
        by_attr.append(Counter(zip([col[i] for i in idx], yy)))
    best, best_val = None, None
    C = len(total)
    for split in SPLITS:
        a, kind, v = split
        cnt = by_attr[a]
        if kind == "eq":
            left = [cnt.get((v, c), 0) for c in range(C)]
        else:
            left = [sum(cnt.get((u, c), 0) for u in range(v + 1)) for c in range(C)]
        n_l = sum(left)
        if n_l == 0 or n_l == n:
            continue
        right = [total[c] - left[c] for c in range(C)]
        val = Fraction(_sum_sq(left), n_l) + Fraction(_sum_sq(right), n - n_l)
        if best_val is None or val > best_val:
            best, best_val = split, val
    return best


# ---------------------------------------------------------------------------
# Pruning
# ---------------------------------------------------------------------------

def _stats(tree: Tree) -> dict[int, tuple[int, int]]:
    """`(R(T_t), |T_t|)` for every node of the current subtree, in one post-order
    pass: what a step of weakest-link pruning needs."""
    out: dict[int, tuple[int, int]] = {}
    stack = [(0, False)]
    while stack:
        t, done = stack.pop()
        if tree.is_leaf(t):
            out[t] = (tree.nodes[t].errors, 1)
        elif done:
            node = tree.nodes[t]
            el, ll = out[node.left]
            er, lr = out[node.right]
            out[t] = (el + er, ll + lr)
        else:
            node = tree.nodes[t]
            stack.extend(((t, True), (node.right, False), (node.left, False)))
    return out


def _costs(tree: Tree) -> dict[int, Fraction]:
    """`g(t)` for every internal node of the current subtree."""
    stats = _stats(tree)
    return {t: Fraction(tree.nodes[t].errors - r, leaves - 1)
            for t, (r, leaves) in stats.items() if not tree.is_leaf(t)}


def prune_sequence(tree: Tree) -> list[tuple[Fraction, frozenset]]:
    """`[(α_k, collapsed_k)]`, from the smallest subtree with the full tree's
    training error, at `α₀ = 0`, to the root. Every node at the step's smallest
    `g` is collapsed at once, and a cost reached twice keeps the smaller tree."""
    collapsed: set[int] = set()
    while True:                                   # T(0): what costs nothing
        zero = [t for t, g in _costs(tree.subtree(frozenset(collapsed))).items()
                if g == 0]
        if not zero:
            break
        collapsed |= set(zero)
    seq = [(Fraction(0), frozenset(collapsed))]
    while True:
        gs = _costs(tree.subtree(frozenset(collapsed)))
        if not gs:
            break
        alpha = min(gs.values())
        collapsed |= {t for t, g in gs.items() if g == alpha}
        if alpha == seq[-1][0]:
            seq[-1] = (alpha, frozenset(collapsed))
        else:
            seq.append((alpha, frozenset(collapsed)))
    return seq


def _held_out_counts(tree: Tree, X, y, idx) -> list[list[int]]:
    """Held-out labels by class at every node they pass through."""
    C = len(ACTIONS)
    h = [[0] * C for _ in tree.nodes]
    for i in idx:
        x, c = X[i], y[i]
        t = 0
        while True:
            h[t][c] += 1
            node = tree.nodes[t]
            if node.split is None:
                break
            t = node.left if holds(node.split, x) else node.right
    return h


def _held_out_errors(tree: Tree, collapsed: frozenset, h) -> int:
    sub = tree.subtree(collapsed)
    errs = 0
    for t in sub.leaves():
        errs += sum(h[t]) - h[t][tree.nodes[t].label]
    return errs


def _at(seq, alpha_sq_bound) -> frozenset:
    """The fold's subtree at `β`: the last whose `α² ≤ β²`; `None` is `β = ∞`."""
    chosen = seq[0][1]
    for alpha, coll in seq:
        if alpha_sq_bound is None or alpha * alpha <= alpha_sq_bound:
            chosen = coll
        else:
            break
    return chosen


@dataclass
class Fitted:
    tree: Tree
    sequence: list[tuple[Fraction, frozenset]]
    chosen_k: int
    cv_errors: list[int]
    full_leaves: int

    @property
    def alpha(self) -> Fraction:
        return self.sequence[self.chosen_k][0]

    def predict(self, case: Case) -> str:
        return self.tree.predict(case)


def fit(cases: Sequence[Case], labels: Sequence[str]) -> Fitted:
    """The plan's tree: grown on every example, pruned at the cost the five
    grouped folds choose. Reads the tickets and their labels, nothing else."""
    X = [encode(c) for c in cases]
    y = [ACTIONS.index(l) for l in labels]
    full = grow(X, y)
    seq = prune_sequence(full)
    fold = folds(X)
    K = len(seq) - 1
    bounds = [seq[k][0] * seq[k + 1][0] for k in range(K)] + [None]
    cv = [0] * (K + 1)
    for v in range(plan.FOLDS):
        tr = [i for i, f in enumerate(fold) if f != v]
        ho = [i for i, f in enumerate(fold) if f == v]
        if not ho:
            continue
        sub = grow([X[i] for i in tr], [y[i] for i in tr])
        sub_seq = prune_sequence(sub)
        h = _held_out_counts(sub, X, y, ho)
        cache: dict[frozenset, int] = {}
        for k, b in enumerate(bounds):
            coll = _at(sub_seq, b)
            if coll not in cache:
                cache[coll] = _held_out_errors(sub, coll, h)
            cv[k] += cache[coll]
    best = choose(cv)
    return Fitted(full.subtree(seq[best][1]), seq, best, cv, len(full.leaves()))


def choose(cv: Sequence[int]) -> int:
    """The `k` with the fewest held-out errors; ties to the larger `k`, the
    smaller tree."""
    return min(range(len(cv)), key=lambda k: (cv[k], -k))


# ---------------------------------------------------------------------------
# The tree as a rule base
# ---------------------------------------------------------------------------

def _paths(tree: Tree) -> list[tuple[int, list[tuple[tuple[int, str, int], bool]]]]:
    out, stack = [], [(0, [])]
    while stack:
        t, path = stack.pop()
        if tree.is_leaf(t):
            out.append((t, path))
            continue
        node = tree.nodes[t]
        stack.append((node.right, path + [(node.split, False)]))
        stack.append((node.left, path + [(node.split, True)]))
    out.sort(key=lambda p: p[0])
    return out


def conditions_of(path) -> list[dict[str, Any]]:
    """A path's conditions, merged to at most one per attribute: `eq` for one
    value; `lte` or `gte` for a numeric range open on one side and `in` for one
    bounded on both; for a categorical attribute, `neq` for one value left out
    and `in` for several."""
    out: list[dict[str, Any]] = []
    for a, attr in enumerate(ATTRIBUTES):
        dom = DOMAINS[attr]
        steps = [(kind, v, side) for (aa, kind, v), side in path if aa == a]
        if not steps:
            continue
        if attr in NUMERIC_ATTRS:
            lo, hi = 0, len(dom) - 1
            for _kind, v, side in steps:
                if side:
                    hi = min(hi, v)
                else:
                    lo = max(lo, v + 1)
            if lo == hi:
                out.append({"attr": attr, "op": "eq", "value": dom[lo]})
            elif lo > 0 and hi < len(dom) - 1:
                out.append({"attr": attr, "op": "in", "value": dom[lo:hi + 1]})
            elif lo > 0:
                out.append({"attr": attr, "op": "gte", "value": dom[lo]})
            else:
                out.append({"attr": attr, "op": "lte", "value": dom[hi]})
            continue
        if dom == [False, True]:
            _kind, _v, side = steps[0]
            out.append({"attr": attr, "op": "eq", "value": bool(side)})
            continue
        eq = [v for _k, v, side in steps if side]
        neq = sorted({v for _k, v, side in steps if not side})
        if eq:
            out.append({"attr": attr, "op": "eq", "value": dom[eq[0]]})
        elif len(neq) == 1:
            out.append({"attr": attr, "op": "neq", "value": dom[neq[0]]})
        else:
            left = [dom[v] for v in range(len(dom)) if v not in neq]
            if len(left) == 1:
                out.append({"attr": attr, "op": "eq", "value": left[0]})
            else:
                out.append({"attr": attr, "op": "in", "value": left})
    return out


def rules(tree: Tree) -> list[dict[str, Any]]:
    """Every leaf as a DSL payload, validated by the frozen validator: its
    conditions, its queue and its training counts."""
    out = []
    for k, (t, path) in enumerate(_paths(tree)):
        conds = conditions_of(path) or [dict(CATCH_ALL)]
        node = tree.nodes[t]
        payload = {"rule_id": f"L{k + 1:03d}", "conditions": conds,
                   "action": ACTIONS[node.label]}
        validate_rule_payload(payload)
        out.append(payload | {"node": t, "training_labels": node.n,
                              "training_right": node.counts[node.label]})
    return out


def describe(f: Fitted) -> dict[str, Any]:
    return {"leaves": len(f.tree.leaves()), "full_leaves": f.full_leaves,
            "subtrees": len(f.sequence), "chosen_k": f.chosen_k,
            "alpha": str(f.alpha), "cv_errors": f.cv_errors}
