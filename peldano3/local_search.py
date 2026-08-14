"""
Local search over the rule order: the optimizer that the audit of rungs 3 and 4
puts on trial.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Rungs 3 and 4 both rest on `order_search.greedy_order`, a decision-list greedy
with no global guarantee. Three independent signs say it is weak:

  * noise IMPROVES its result — 0.7574 -> 0.8337 against the truth with 30% of
    the labels falsified (rung 4), which is impossible as an effect of
    supervision and reads as a random restart;
  * searching the order over the test set ITSELF still leaves 0.1187 under the
    coverage bound (rung 3), so the gap is not a lack of generalization;
  * the tie-break alone moved the result by 0.011 across `PYTHONHASHSEED`.

Fixing the tie-break moved the aggregate by 0.0002. That separates the two
hypotheses: the fragility was VARIANCE, not bias. What is left on trial is the
algorithm, and this module is what tries it.

--------------------------------------------------------------------------
THE OBJECTIVE — identical to the greedy's, on purpose
--------------------------------------------------------------------------
Under first-match-wins the winner of a case is the lowest-ranked rule among
those matching it, and the score counts the cases whose winner carries the
right action. Cases no rule matches count as failures, exactly as
`order_search.evaluate` counts them (it skips them without counting them
correct, and still divides by the number of cases).

The score is an INTEGER count, and every move applied is a STRICT improvement.
That is what guarantees termination, and it is also what keeps the result
independent of the traversal order in the way the old tie-break was not: no move
is ever applied on a tie.

--------------------------------------------------------------------------
WEIGHTS — the balanced objective, on the same machinery
--------------------------------------------------------------------------
`budget_and_balance` also searches a CLASS-BALANCED objective, which weights
each case by 1/|its class| so that the rare classes stop being sacrificed.
Naively that needs per-class masks and about eight times the work.

It does not, because of one lemma: every case in W[r] carries the label
action[r], since W[r] is by construction the subset of M[r] the rule gets
RIGHT. So THE CLASS OF A WIN IS A FUNCTION OF THE RULE, not of the case, and a
class-weighted objective is exactly the machinery below with each rule's hit
count scaled by one integer — `balanced_weights` builds them.

Integer, and that is the point: the score stays a bounded integer, so strict
improvement still guarantees termination and no move is ever applied on a tie.
Both properties would be lost with floating-point 1/n.

`wt=None` is the uniform objective, and it is the path every published figure
runs on. It is kept exactly as it was: the weight never enters its arithmetic,
only a test that it is absent. `tests/test_local_search.py` pins that all-ones
weights return the same order and the same score as `wt=None`.

--------------------------------------------------------------------------
REPRESENTATION — bitmasks, so that a full evaluation is O(#rules)
--------------------------------------------------------------------------
Per rule: M[r] = mask of the evaluated cases it matches, W[r] = the subset of
those whose label its action gets right. Scoring an order is then a sweep of
big-integer ANDs, and it stops as soon as no case is left pending, which in
practice happens long before the end of the order.

That last point matters for reading the result: the rules beyond the position
where the pending mask empties out are INVISIBLE to the objective. They decide
nothing on train and can still decide on test. The local search therefore cannot
improve — nor damage — that tail, exactly as the greedy could not.

--------------------------------------------------------------------------
TWO NEIGHBOURHOODS
--------------------------------------------------------------------------
`swap`   exchange the rules at two positions. This is what PLAN_AUDIT asks for.
         Cost: O(n^2) candidates, each evaluated from a prefix state, so a pass
         is O(L * n * L) with L the coverage length. The expensive one.

`move`   take one rule out and reinsert it at its best position. Cheaper AND
         stronger: for a fixed rule, ALL its insertion positions are evaluated
         in a single sweep, because once the rule is removed the winner of every
         case and its rank are fixed, and inserting the rule at position k means
         precisely that it takes over the cases whose winner sat at rank >= k.
         So a pass costs O(n) sweeps instead of O(n^2).

Neither contains the other: a swap is not one relocation, and a relocation is
not one swap. `move+swap` alternates them until neither improves, which is the
honest reading of "until no improvement".
"""

from __future__ import annotations

import random
from collections import Counter
from math import lcm

# ---------------------------------------------------------------------------
# Masks and scoring
# ---------------------------------------------------------------------------


def build_masks(ids, pool, label, action, idxs):
    """
    M[rid] cases of `idxs` that rid matches; W[rid] those it also gets right.

    `label` is indexed by case index and may be a list (the truth, rung 3) or a
    dict (what the channel reported, rung 4). Nothing else is read from it.
    """
    M = {rid: 0 for rid in ids}
    W = {rid: 0 for rid in ids}
    for k, i in enumerate(idxs):
        bit = 1 << k
        y = label[i]
        for rid in pool[i]:
            M[rid] |= bit
            if action[rid] == y:
                W[rid] |= bit
    return M, W, (1 << len(idxs)) - 1


def balanced_weights(ids, action, label, idxs):
    """
    Integer per-rule weights that turn the objective into macro-recall.

    The lemma is in the module header: every case a rule wins carries that
    rule's action as its label, so weighting a CASE by 1/|its class| is the same
    as weighting the RULE by 1/|its action's class|.

        n[c]  = labelled cases of class c
        L     = lcm{ n[c] }              so that every weight is an integer
        wt[r] = L // n[action[r]]

    The score of an order is then L * sum_c recall_c: macro-recall up to the
    positive constant L * |classes|, which is what `budget_and_balance.per_class`
    reports as balanced accuracy. L being integral is what keeps the score a
    bounded integer, and with it termination and the no-move-on-a-tie rule;
    floating-point 1/n would cost both. L can be large — Python ints.

    A rule whose action is a class absent from the labelled subset gets weight
    0. It can win nothing there (W[r] is empty by construction), so the value
    only has to exist for the lookup, and 0 is the honest one.

    Returns (wt, L, n).
    """
    return weights_from_counts(ids, action, Counter(label[i] for i in idxs))


def weights_from_counts(ids, action, n):
    """
    The same weights when the class counts are already in hand.

    Over the exhaustive space they come off the masks — the cases of class c are
    exactly the union of W[r] over the rules with action c, whenever every case
    is matched by some rule carrying its correct label — and building 134,400
    labels only to count them again would be waste. Returns (wt, L, n).
    """
    L = 1
    for c in n:
        L = lcm(L, n[c])
    wt = {rid: (L // n[action[rid]] if action[rid] in n else 0) for rid in ids}
    return wt, L, n


def greedy_order_from_masks(ids, M, W, full, tail_key):
    """
    `order_search.greedy_order` rewritten over the masks, so that the SAME
    construction can run on instances where building one big integer per case
    index is not affordable — the exhaustive space of 134,400 combinations, for
    one. It is the starting point the audit departs from, so it has to be the
    greedy of the record and not a variant of it: `tests/test_local_search.py`
    checks that both produce the same order.

    `tail_key` orders the rules left over once nothing is pending, which the
    objective cannot see. Rung 3 sorts that tail by train precision and then by
    born_at; rung 4 by born_at alone, so that the absence of feedback degenerates
    to the baseline. It is a parameter because that difference is deliberate.
    """
    remaining = full
    left = set(ids)
    order = []
    while left and remaining:
        best, best_score = None, None
        for rid in sorted(left):          # sorted, never the set: see the 2026-08-06 fix
            hit = (W[rid] & remaining).bit_count()
            miss = ((M[rid] ^ W[rid]) & remaining).bit_count()
            s = hit - miss
            if best_score is None or s > best_score:
                best, best_score = rid, s
        order.append(best)
        left.discard(best)
        remaining &= ~M[best]
    return order + sorted(left, key=tail_key)


def score_order(order, M, W, full, wt=None):
    """Cases won with the right action. `fires` is a subset of `remaining`, so
    the xor is the same as clearing the bits and is cheaper.

    `wt` is the per-rule weight of `balanced_weights`; None is the uniform
    objective and does not pay for the weight, only for a test that it is
    absent."""
    remaining, ok = full, 0
    for rid in order:
        fires = M[rid] & remaining
        if fires:
            if wt is None:
                ok += (W[rid] & fires).bit_count()
            else:
                ok += wt[rid] * (W[rid] & fires).bit_count()
            remaining ^= fires
            if not remaining:
                break
    return ok


def coverage_length(order, M, full):
    """First position at which nothing is left pending. Rules from there on are
    invisible to the objective."""
    remaining = full
    for p, rid in enumerate(order):
        if not remaining:
            return p
        remaining &= ~M[rid]
    return len(order)


# ---------------------------------------------------------------------------
# Neighbourhood `move`: relocate one rule, all positions in one sweep
# ---------------------------------------------------------------------------


def best_insertion(order, k_cur, M, W, full, wt=None):
    """
    Best position for `order[k_cur]` among all the ways of reinserting it into
    the order without it. Returns (position, score).

    With the rule removed, each case has a fixed winner and a fixed rank. Put
    back at position k, the rule takes over exactly the cases it matches whose
    winner sat at rank >= k (including those left with no winner at all). Hence
    three quantities, all obtained in one sweep:

      C     hits among the cases the rule does NOT match — independent of k
      A[k]  hits among the cases it DOES match that are decided before k
      B[k]  cases it matches with rank >= k whose label its action gets right

    and score(k) = C + A[k] + B[k].

    Under weights, C and A are scaled case by case by the weight of whichever
    rule wins the case, while the whole of B belongs to `r` and is scaled by the
    single weight wt[r] — so B is scaled once, after the sweep, and the sweep
    itself stays as cheap as it was.
    """
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
            if wt is None:
                acc += (hits & Mr).bit_count()
                C += (hits & not_Mr).bit_count()
            else:
                w = wt[rest[k]]
                acc += w * (hits & Mr).bit_count()
                C += w * (hits & not_Mr).bit_count()
            remaining ^= fires
        k += 1
        A[k] = acc
    # From k on nothing changes: either the order ran out, or nothing is
    # pending and then no reinsertion of r can win anything.
    tail_B = (Wr & remaining).bit_count()
    for j in range(k, n + 1):
        A[j] = acc
        B[j] = tail_B
    if wt is not None:
        wr = wt[r]
        B = [wr * b for b in B]

    best_k, best = k_cur, C + A[k_cur] + B[k_cur]
    for j in range(n + 1):
        s = C + A[j] + B[j]
        if s > best:                      # strict: a tie never moves anything
            best_k, best = j, s
    return best_k, best


def move_pass(order, M, W, full, wt=None):
    """One sweep relocating every rule. Returns how many it moved."""
    moved = 0
    for rid in list(order):
        k = order.index(rid)
        best_k, best = best_insertion(order, k, M, W, full, wt)
        if best_k != k:
            order.pop(k)
            order.insert(best_k, rid)
            moved += 1
    return moved


# ---------------------------------------------------------------------------
# Neighbourhood `swap`: exchange two positions
# ---------------------------------------------------------------------------


def _prefix_states(order, M, W, full, wt=None):
    """Pending mask and hits accumulated BEFORE each position."""
    n = len(order)
    rem = [0] * (n + 1)
    hit = [0] * (n + 1)
    remaining, ok = full, 0
    for p in range(n):
        rem[p], hit[p] = remaining, ok
        rid = order[p]
        fires = M[rid] & remaining
        if fires:
            if wt is None:
                ok += (W[rid] & fires).bit_count()
            else:
                ok += wt[rid] * (W[rid] & fires).bit_count()
            remaining ^= fires
    rem[n], hit[n] = remaining, ok
    return rem, hit


def _score_after_swap(order, p, q, rem0, ok0, M, W, wt=None):
    """Score of the order with p and q exchanged, resuming from the prefix of
    p. Everything before p is untouched, which is what makes this affordable."""
    n = len(order)
    a, b = order[p], order[q]
    remaining, ok = rem0, ok0
    fires = M[b] & remaining
    if fires:
        if wt is None:
            ok += (W[b] & fires).bit_count()
        else:
            ok += wt[b] * (W[b] & fires).bit_count()
        remaining ^= fires
    for j in range(p + 1, n):
        if not remaining:
            break
        rid = a if j == q else order[j]
        fires = M[rid] & remaining
        if fires:
            if wt is None:
                ok += (W[rid] & fires).bit_count()
            else:
                ok += wt[rid] * (W[rid] & fires).bit_count()
            remaining ^= fires
    return ok


def swap_pass(order, M, W, full, wt=None):
    """
    Sweep of pairs, applying each strict improvement as it is found and
    resuming from the same p. Every application raises an integer bounded
    above, so it terminates. Returns how many it applied.
    """
    n = len(order)
    applied = 0
    rem, hit = _prefix_states(order, M, W, full, wt)
    base = hit[n]
    p = 0
    while p < n:
        rem0, ok0 = rem[p], hit[p]
        if not rem0:                      # nothing pending: the tail decides nothing
            break
        found = False
        for q in range(p + 1, n):
            if not (M[order[p]] & rem0) and not (M[order[q]] & rem0):
                continue                  # neither can fire from here: inert
            s = _score_after_swap(order, p, q, rem0, ok0, M, W, wt)
            if s > base:                  # strict, first improvement
                order[p], order[q] = order[q], order[p]
                applied += 1
                rem, hit = _prefix_states(order, M, W, full, wt)
                base = hit[n]
                found = True
                break
        if not found:
            p += 1
    return applied


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

NEIGHBOURHOODS = ("move", "swap", "move+swap")


def local_search(order, M, W, full, neighbourhood="move+swap", max_rounds=200,
                 wt=None):
    """
    Hill climbing to a local optimum. Returns (order, stats).

    Deterministic: no random tie-break anywhere, and no move is applied on a
    tie. `max_rounds` is a safety net, not a stopping criterion — strict
    improvement over a bounded integer already guarantees termination — and if
    it is ever hit, `stats["exhausted"]` says so instead of it passing silently.
    """
    if neighbourhood not in NEIGHBOURHOODS:
        raise ValueError(f"unknown neighbourhood: {neighbourhood!r}")
    order = list(order)
    start = score_order(order, M, W, full, wt)
    stats = {"start": start, "move_passes": 0, "moves": 0,
             "swap_passes": 0, "swaps": 0, "rounds": 0, "exhausted": False}

    for _ in range(max_rounds):
        stats["rounds"] += 1
        changed = 0
        if neighbourhood in ("move", "move+swap"):
            moved = move_pass(order, M, W, full, wt)
            stats["move_passes"] += 1
            stats["moves"] += moved
            changed += moved
        if neighbourhood in ("swap", "move+swap"):
            swapped = swap_pass(order, M, W, full, wt)
            stats["swap_passes"] += 1
            stats["swaps"] += swapped
            changed += swapped
        if not changed:
            break
    else:
        stats["exhausted"] = True

    stats["end"] = score_order(order, M, W, full, wt)
    stats["gain"] = stats["end"] - start
    return order, stats


def random_order(ids, seed):
    o = sorted(ids)
    random.Random(seed).shuffle(o)
    return o


# ---------------------------------------------------------------------------
# Multi-start
# ---------------------------------------------------------------------------
#
# WHY IT IS HERE. Step 0 of the audit, on August 8, 2026, found that a single
# run from the greedy start does not recover the known optimum of the 29-rule
# hidden policy: pairwise swaps stop at 0.9356 over the exhaustive space and
# relocation at 0.999851, one inverted relation short, in a basin no single
# move and no permutation of three positions escapes. From random starts the
# same search reached 1.0000 in about one attempt in four. Restarting is
# therefore the repair the measurement itself pointed at.
#
# THE CONSTANTS ARE DECLARED, NOT TUNED. At a one-in-four rate, 64 starts miss
# altogether with probability 0.75**64, below 1e-8. The seed is 17, the
# project's, so the sequence of starts is the same in every run and every rung.
# Changing either of them after seeing a result is the Goodhart failure this
# experiment studies; they are constants of the module for that reason.

MULTISTART_SEED = 17
MULTISTART_STARTS = 64

# THE DECLARED NEIGHBOURHOOD, fixed by Sergi on August 8, 2026 after Step 0.
# Reasoning, recorded because the cheaper option was available and refused: the
# two neighbourhoods do not contain each other, and their coming out
# indistinguishable on the 29-rule instance — same optimum, same first hit at
# start 9, same 9/65 — is a sample of size one. The failure Step 0 found is an
# optimum sitting behind a coordinated change of four or more positions, which
# is precisely the case a narrower neighbourhood loses. If `move+swap` turns out
# impractical over 577 rules, that is a measurement about the method and gets
# reported as one; it is not a reason to have narrowed it in advance.
DECLARED_NEIGHBOURHOOD = "move+swap"


def declared_starts(ids, first=None, seed=MULTISTART_SEED, n=MULTISTART_STARTS):
    """
    The ordered list of starting points, fixed by declaration.

    `first` is the greedy where there is one. It goes at position 0, and since
    ties between starts go to the earliest, the multi-start can never return
    something worse than the single run from the greedy that PLAN_AUDIT asked
    for. The comparison stays honest in that direction by construction.
    """
    starts = []
    if first is not None:
        starts.append(("voraz", list(first)))
    rng = random.Random(seed)
    base = sorted(ids)
    for k in range(n):
        o = list(base)
        rng.shuffle(o)
        starts.append((f"aleatorio {k}", o))
    return starts


def multistart(starts, M, W, full, neighbourhood="move+swap", optimum=None,
               wt=None, keep_orders=False):
    """
    Local search from every declared start, keeping the best. Deterministic:
    the starts are fixed, no move is applied on a tie, and a tie between starts
    goes to the earliest.

    `optimum` is REPORTING ONLY — which start first attains it and how many do,
    so that the cost of the restarts is on the record. The search never reads
    it, and it must be left None wherever the optimum is not known independently
    of the search, which is everywhere except this audit's Step 0.

    `keep_orders` adds each start's END ORDER to its row, and changes nothing
    else. Every published figure came out of this function with the orders
    dropped: only the winner survived, scored, and the other 64 permutations
    were discarded at the `for` above. That is why no record in `results*/`
    holds an order from this optimizer, and why the question "do two orders that
    score alike decide alike" has never been askable of a stored artefact
    (`PLAN_ORDER_METRICS.md`, G1). It defaults to False so that the path every
    record ran on is the same path, byte for byte — `tests/test_local_search.py`
    pins the returned stats against what it returned before this argument
    existed. The orders are the expensive thing to hold, not to compute: 65
    permutations of 577 rules, which is why the caller asks for them.
    """
    rows = []
    best_order, best_score, best_at = None, -1, None
    for k, (name, o0) in enumerate(starts):
        o, st = local_search(o0, M, W, full, neighbourhood=neighbourhood, wt=wt)
        row = {"index": k, "start": name, "start_score": st["start"],
               "end_score": st["end"], "rounds": st["rounds"],
               "moves": st["moves"], "swaps": st["swaps"],
               "exhausted": st["exhausted"]}
        if keep_orders:
            row["order"] = list(o)
        rows.append(row)
        if st["end"] > best_score:
            best_order, best_score, best_at = o, st["end"], k

    hits = [r["index"] for r in rows if r["end_score"] == optimum] if optimum else []
    return best_order, {
        "n_starts": len(starts),
        "neighbourhood": neighbourhood,
        "best_score": best_score,
        "best_from_index": best_at,
        "best_from": starts[best_at][0],
        "reached_optimum": bool(optimum) and best_score == optimum,
        "first_hit_index": hits[0] if hits else None,
        "first_hit_start": starts[hits[0]][0] if hits else None,
        "starts_until_first_hit": hits[0] + 1 if hits else None,
        "n_hits": len(hits),
        "rows": rows,
    }
