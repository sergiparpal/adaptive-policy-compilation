"""
THE LOGISTIC REGRESSION — `PLAN_STUDENTS.md` §3.2.

A multinomial logistic regression over one indicator per value of every
attribute, 47 of them in `DOMAINS` order, and a constant. It is trained on
tickets and labels and nothing else.

--------------------------------------------------------------------------
THE OBJECTIVE, AND WHY THE OPTIMISER IS NOT A CHOICE
--------------------------------------------------------------------------
The mean negative log-likelihood of the softmax plus `(λ/2)·‖W‖²` over every
weight, the constant's included. With `λ > 0` it is strictly convex, so its
minimum is unique: the optimiser decides only how close to it a fit gets, and
`students/gates.py` checks that every fit the dry run makes ends with each
component of its gradient within `GRADIENT_TOL`. The stage records the largest
final gradient of every fit it makes.

The classes are the queues present in the training labels, in `ACTIONS` order,
and every fold uses the same classes, so that a held-out label the fold never
saw still has a finite loss.

--------------------------------------------------------------------------
THE PENALTY, CHOSEN BY THE FOLDS
--------------------------------------------------------------------------
`λ` from `LAMBDAS`, `10^(k/2)` for `k = −8, …, 2`, chosen by the five folds of
`students/tree.py`'s `folds`: the lowest mean held-out log-loss wins, and ties go
to the larger `λ`. Within a fold the grid is walked from the largest `λ` down,
each fit starting from the previous one's weights; that changes how many
iterations a fit takes and nothing else, since each fit's minimum is unique. The
final fit, on every example at the chosen `λ`, starts from zero.

--------------------------------------------------------------------------
THE OPTIMISER
--------------------------------------------------------------------------
L-BFGS with `LBFGS_MEMORY` pairs and Armijo backtracking (`ARMIJO`, halving),
until every component of the gradient is at most `GRADIENT_TOL` or `MAX_ITER`
iterations have run.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Sequence

from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS, Case

from . import plan
from .tree import encode, folds

OFFSETS = []
_o = 0
for _a in ATTRIBUTES:
    OFFSETS.append(_o)
    _o += len(DOMAINS[_a])
N_INDICATORS = _o                  # 47
BIAS = N_INDICATORS                # the constant's index
D = N_INDICATORS + 1


def features(x: Sequence[int]) -> tuple[int, ...]:
    """The active indicators of an encoded ticket, and the constant."""
    return tuple(OFFSETS[a] + v for a, v in enumerate(x)) + (BIAS,)


# ---------------------------------------------------------------------------
# The objective
# ---------------------------------------------------------------------------

def objective(w: list[float], data, C: int, lam: float) -> tuple[float, list[float]]:
    """`(J, ∇J)` at `w`, flat by class then feature. `data` is `[(feats, y)]`."""
    n = len(data)
    grad = [0.0] * (C * D)
    loss = 0.0
    for feats, yi in data:
        z = [0.0] * C
        for c in range(C):
            base = c * D
            s = 0.0
            for f in feats:
                s += w[base + f]
            z[c] = s
        m = max(z)
        e = [math.exp(v - m) for v in z]
        tot = sum(e)
        loss += math.log(tot) + m - z[yi]
        for c in range(C):
            p = e[c] / tot
            if c == yi:
                p -= 1.0
            if p != 0.0:
                base = c * D
                for f in feats:
                    grad[base + f] += p
    inv = 1.0 / n
    loss = loss * inv + 0.5 * lam * sum(v * v for v in w)
    grad = [g * inv + lam * v for g, v in zip(grad, w)]
    return loss, grad


def _dot(a, b) -> float:
    return sum(x * y for x, y in zip(a, b))


@dataclass
class Fit:
    w: list[float]
    loss: float
    grad_max: float
    iterations: int
    converged: bool


def lbfgs(data, C: int, lam: float, w0: list[float] | None = None) -> Fit:
    """Minimise the objective from `w0`, zero by default."""
    w = list(w0) if w0 is not None else [0.0] * (C * D)
    f, g = objective(w, data, C, lam)
    S: list[list[float]] = []
    Y: list[list[float]] = []
    it = 0
    while max(abs(v) for v in g) > plan.GRADIENT_TOL and it < plan.MAX_ITER:
        q = list(g)
        alphas = []
        for s, yv in zip(reversed(S), reversed(Y)):
            rho = 1.0 / _dot(yv, s)
            a = rho * _dot(s, q)
            alphas.append((a, rho, s, yv))
            q = [qi - a * yi for qi, yi in zip(q, yv)]
        if S:
            gamma = _dot(S[-1], Y[-1]) / _dot(Y[-1], Y[-1])
            r = [gamma * qi for qi in q]
        else:
            r = [qi / max(1.0, max(abs(v) for v in g)) for qi in q]
        for a, rho, s, yv in reversed(alphas):
            b = rho * _dot(yv, r)
            r = [ri + (a - b) * si for ri, si in zip(r, s)]
        d = [-ri for ri in r]
        slope = _dot(g, d)
        if slope >= 0:                                  # not a descent: restart
            S, Y = [], []
            d = [-gi for gi in g]
            slope = _dot(g, d)
        t = 1.0
        while True:
            w_new = [wi + t * di for wi, di in zip(w, d)]
            f_new, g_new = objective(w_new, data, C, lam)
            if f_new <= f + plan.ARMIJO * t * slope or t < 1e-20:
                break
            t *= 0.5
        s = [a - b for a, b in zip(w_new, w)]
        yv = [a - b for a, b in zip(g_new, g)]
        if _dot(s, yv) > 1e-16:
            S.append(s)
            Y.append(yv)
            if len(S) > plan.LBFGS_MEMORY:
                S.pop(0)
                Y.pop(0)
        w, f, g = w_new, f_new, g_new
        it += 1
    gmax = max(abs(v) for v in g)
    return Fit(w, f, gmax, it, gmax <= plan.GRADIENT_TOL)


# ---------------------------------------------------------------------------
# The student
# ---------------------------------------------------------------------------

@dataclass
class Fitted:
    classes: list[str]
    lam: float
    fit: Fit
    cv_loss: list[float]
    fold_fits: list[dict[str, Any]]

    def scores(self, x: Sequence[int]) -> list[float]:
        feats = features(x)
        return [sum(self.fit.w[c * D + f] for f in feats)
                for c in range(len(self.classes))]

    def predict_index(self, x: Sequence[int]) -> int:
        """The class of highest score, as an index into `ACTIONS`; ties to
        `ACTIONS` order, which the classes are in."""
        z = self.scores(x)
        best = max(range(len(z)), key=lambda c: (z[c], -c))
        return ACTIONS.index(self.classes[best])

    def predict(self, case: Case) -> str:
        return ACTIONS[self.predict_index(encode(case))]


def _data(X, y_names, classes):
    return [(features(x), classes.index(l)) for x, l in zip(X, y_names)]


def held_out_loss(w, data, C) -> float:
    total = 0.0
    for feats, yi in data:
        z = [sum(w[c * D + f] for f in feats) for c in range(C)]
        m = max(z)
        total += math.log(sum(math.exp(v - m) for v in z)) + m - z[yi]
    return total


def fit(cases: Sequence[Case], labels: Sequence[str]) -> Fitted:
    """The plan's regression: `λ` by the five grouped folds, then one fit on
    every example from zero. Reads the tickets and their labels, nothing else."""
    X = [encode(c) for c in cases]
    classes = [a for a in ACTIONS if a in set(labels)]
    C = len(classes)
    fold = folds(X)
    totals = [0.0] * len(plan.LAMBDAS)
    fold_fits = []
    for v in range(plan.FOLDS):
        tr = [i for i, f in enumerate(fold) if f != v]
        ho = [i for i, f in enumerate(fold) if f == v]
        if not ho:
            continue
        d_tr = _data([X[i] for i in tr], [labels[i] for i in tr], classes)
        d_ho = _data([X[i] for i in ho], [labels[i] for i in ho], classes)
        w = None
        for k in reversed(range(len(plan.LAMBDAS))):
            got = lbfgs(d_tr, C, plan.LAMBDAS[k], w)
            w = got.w
            totals[k] += held_out_loss(w, d_ho, C)
            fold_fits.append({"fold": v, "lambda": plan.LAMBDAS[k],
                              "iterations": got.iterations,
                              "grad_max": got.grad_max,
                              "converged": got.converged})
    n = len(X)
    cv = [t / n for t in totals]
    best = choose(cv)
    final = lbfgs(_data(X, labels, classes), C, plan.LAMBDAS[best])
    return Fitted(classes, plan.LAMBDAS[best], final, cv, fold_fits)


def choose(cv: Sequence[float]) -> int:
    """The `λ` of lowest mean held-out log-loss; ties to the larger `λ`, which
    is the later in `LAMBDAS`."""
    return min(range(len(cv)), key=lambda k: (cv[k], -k))


def describe(f: Fitted) -> dict[str, Any]:
    return {"classes": f.classes, "lambda": f.lam, "iterations": f.fit.iterations,
            "grad_max": f.fit.grad_max, "converged": f.fit.converged,
            "cv_loss": f.cv_loss,
            "fold_grad_max": max((r["grad_max"] for r in f.fold_fits), default=None),
            "fold_fits_converged": all(r["converged"] for r in f.fold_fits)}
