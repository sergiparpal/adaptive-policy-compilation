"""
An instrument that measures ORDERS, not scores.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
Four rungs have compared permutations of 577 rules by looking at a scalar. Two
orders that score alike are then reported as if they were the same answer, and
nothing in the repository can say whether they are: the only complete order ever
stored is the superseded rung-3 greedy, and the audited optimizer's orders were
scored and dropped inside `multistart` (`PLAN_ORDER_METRICS.md`, G1).

The reason a scalar is a bad summary here is arithmetic, not philosophical.
Under first-match-wins the relative order of two rules can change a decision
only if BOTH match some common case AND they prescribe different actions. Most
pairs do neither, so most of a 577-element permutation is free: two orders can
differ in hundreds of positions and be the same machine. A rank statistic over
all pairs spends most of its mass on the part that cannot matter.

So the measure here is not a rank statistic at all. It is: ON HOW MANY CASES DO
TWO ORDERS DECIDE DIFFERENTLY — exact, computed with one bitmask sweep per
order. `tau` is kept because a rank correlation is what a reader expects, and
because restricting it to the conflicting pairs is a falsifiable claim about
whether such a statistic can be made to track behaviour at all.

--------------------------------------------------------------------------
WHAT IT IS AND IS NOT
--------------------------------------------------------------------------
Pure functions over orders and masks. This module does not consult the oracle,
does not read the corpus, writes no JSON and knows nothing about optimizers:
everything it needs arrives as an argument, which is what lets the same code
measure the exhaustive space, the corpus, or a three-rule instance whose answer
is written out by hand in a test.

The masks are the ones `local_search.build_masks` and
`order_search_ls.space_pools` already build. Nothing here ever maps a bit back
to a case — every operation is an AND, an OR and a `bit_count` — so the bit
convention is the caller's business, and the two in the repository differ:
`build_masks` puts case k in bit k, `Space` puts it in bit n-1-k. What a caller
must not do is mix masks from two of them in one comparison. `truth`, where a
function takes it, is
{class: mask of the cases whose true label is that class}, and it comes from a
module allowed to see the oracle — never from the masks, which give the per-class
CEILING and not the class size (the defect recorded as F10 of the optimizer
audit).

--------------------------------------------------------------------------
AGREEMENT IS ON THE ACTION, NEVER ON THE RULE
--------------------------------------------------------------------------
Two rules with different identity and the same action decide a case the same
way. A caller that measured agreement by which rule fired would report a
difference where a deployed system would show none. `winners` and
`attribution_agreement` compute the rule-level quantity separately, because it
is interesting for explainability, and it is deliberately not what
`behavioural_distance` returns.
"""

from __future__ import annotations

import statistics
from itertools import combinations

# ---------------------------------------------------------------------------
# What an order decides
# ---------------------------------------------------------------------------


def decisions(order, M, action, full):
    """
    ({action: mask of the cases it decides}, mask of the cases nobody matched).

    One sweep, the same one `score_order` runs, except that it records WHAT was
    decided instead of whether it was right — so this needs no labels and can be
    run over an instance whose truth nobody has. Actions that decide nothing do
    not appear as keys; the two masks of a returned dict never overlap, and
    together with the undecided mask they partition `full`.
    """
    out = {}
    remaining = full
    for rid in order:
        if not remaining:
            break
        fires = M[rid] & remaining
        if fires:
            a = action[rid]
            out[a] = out.get(a, 0) | fires
            remaining ^= fires
    return out, remaining


def winners(order, M, full):
    """
    ({rule: mask of the cases it wins}, mask of the cases nobody matched).

    The attribution, not the decision: which rule fired, regardless of what it
    said. Secondary on purpose — see the module header.
    """
    out = {}
    remaining = full
    for rid in order:
        if not remaining:
            break
        fires = M[rid] & remaining
        if fires:
            out[rid] = fires
            remaining ^= fires
    return out, remaining


def signature(d, undecided):
    """
    A hashable canonical form of what an order decides: everything that
    determines its behaviour and nothing else.

    Two orders share a signature exactly when they decide every case
    identically, which is what makes counting distinct signatures a count of
    distinct MACHINES rather than of distinct permutations (G3). Exact, not a
    digest: the masks go in whole, and a caller that wants something short for a
    record hashes this.
    """
    return (tuple(sorted((a, m) for a, m in d.items() if m)), undecided)


# ---------------------------------------------------------------------------
# How far apart two orders are, behaviourally
# ---------------------------------------------------------------------------


def agreement_masks(dA, dB, full):
    """
    (agree, disagree, undecided_either), as masks.

    A case is in `undecided_either` when at least one of the two orders leaves
    it undecided — a third category rather than a disagreement, because "no rule
    matched" and "a rule matched and said something else" are different events
    and averaging them hides which one is happening. The three partition `full`.
    """
    agree = 0
    for a, m in dA.items():
        other = dB.get(a)
        if other:
            agree |= m & other
    decided = _decided(dA) & _decided(dB)
    return agree, decided & ~agree, full & ~decided


def behavioural_distance(dA, dB, full):
    """
    (agree, disagree, undecided_either), as counts of cases.

    THE measure of this module. `disagree` is the number of cases on which the
    two orders, both having decided, decide differently.
    """
    return tuple(m.bit_count() for m in agreement_masks(dA, dB, full))


def attribution_agreement(wA, wB, restrict_to=None):
    """
    Cases where the SAME RULE fires in both orders, optionally restricted to a
    mask — a class's cases, say, or a region a finding is about.

    It is always at most the behavioural agreement, and restricting it to the
    agreement mask is a no-op: a case won by the same rule in both orders is
    decided by the same action in both, by definition. So the interesting
    quantity is the SHORTFALL — cases the two orders decide alike for different
    reasons — which is `agree - attribution_agreement`, and it is what makes
    this an explainability figure rather than a second measure of behaviour.
    """
    same = 0
    for rid, m in wA.items():
        other = wB.get(rid)
        if other:
            same |= m & other
    if restrict_to is not None:
        same &= restrict_to
    return same.bit_count()


def per_class_disagreement(dA, dB, truth):
    """
    {class: {n, disagree, rate, undecided_either}} over the true class.

    `truth` is {class: mask}, from a module allowed to see the oracle. `rate` is
    over the whole class, undecided cases included in the denominator: a class
    the orders leave undecided is not a class they agree on, and dividing by the
    decided part only would flatter exactly the classes with the least material
    — which are the classes this is asked about (Q-f).
    """
    decided_both = _decided(dA) & _decided(dB)
    agree, _dis, _und = agreement_masks(dA, dB, decided_both)
    out = {}
    for c, m in truth.items():
        n = m.bit_count()
        dis = (m & decided_both & ~agree).bit_count()
        out[c] = {
            "n": n,
            "disagree": dis,
            "rate": (dis / n) if n else None,
            "undecided_either": (m & ~decided_both).bit_count(),
        }
    return out


def _decided(d):
    dec = 0
    for m in d.values():
        dec |= m
    return dec


# ---------------------------------------------------------------------------
# Which pairs can matter at all
# ---------------------------------------------------------------------------


def conflicting_pairs(ids, M, action):
    """
    The pairs whose relative order can change a decision: they co-match at least
    one case and prescribe different actions.

    Everything else is free — swapping such a pair leaves every decision
    untouched, which `tests/test_order_metrics.py` pins on a toy and P3 pins on
    the 29 hidden rules. Canonical tuples (a, b) with a < b, so a caller can use
    them as a set.

    Cost: one big-int AND per pair. Over the exhaustive space and 577 rules that
    is 166,176 ANDs of 134,400 bits, about 0.3 s.
    """
    orden = sorted(ids)
    return {(a, b) for a, b in combinations(orden, 2)
            if action[a] != action[b] and M[a] & M[b]}


def pair_census(ids, M, action):
    """
    {pairs, co_match, conflicting, same_action}: how much of a permutation can
    matter at all, on this surface and this pool.

    Separate from `conflicting_pairs` because the co-matching count is the
    denominator the conflicting one has to be read against, and because the
    census is what gets reported per surface (G2) while the set is what `tau`
    consumes.
    """
    orden = sorted(ids)
    co = conf = 0
    for a, b in combinations(orden, 2):
        if M[a] & M[b]:
            co += 1
            if action[a] != action[b]:
                conf += 1
    n = len(orden)
    return {"pairs": n * (n - 1) // 2, "co_match": co, "conflicting": conf,
            "same_action": co - conf}


# ---------------------------------------------------------------------------
# The positional statistics, kept honest about what they are
# ---------------------------------------------------------------------------


def tau(a, b, pairs=None):
    """
    Kendall tau-a between two orders, over all pairs or over a given set.

    No ties are possible — both arguments are permutations of the same rules —
    so tau is (concordant - discordant) / pairs, and with `pairs` given it is
    that same ratio restricted to those pairs. The restricted form is the point:
    a statistic over all 166,176 pairs spends four fifths of its mass on pairs
    whose relative order cannot change a decision, and Q-d bets that restricting
    it to the conflicting ones makes it track behaviour.

    Returns nan when there is nothing to correlate — fewer than two elements, or
    an empty pair set. That is a real answer to an empty question and it
    propagates, where a 0.0 or a 1.0 would be a made-up one.

    Over all pairs the count is O(n log n) by inversions rather than the O(n^2)
    double loop, which is what makes a 65 x 65 matrix affordable.
    """
    ra = {x: k for k, x in enumerate(a)}
    rb = {x: k for k, x in enumerate(b)}
    if len(ra) != len(a) or len(rb) != len(b) or set(ra) != set(rb):
        raise ValueError("tau compares two permutations of the same elements")

    if pairs is None:
        n = len(a)
        total = n * (n - 1) // 2
        if not total:
            return float("nan")
        disc = _inversions([ra[x] for x in b])
    else:
        total = disc = 0
        for x, y in pairs:
            total += 1
            if (ra[x] < ra[y]) != (rb[x] < rb[y]):
                disc += 1
        if not total:
            return float("nan")
    return (total - 2 * disc) / total


def _inversions(seq):
    """Pairs out of order in `seq`, counted with a Fenwick tree over the values,
    which are a permutation of range(len(seq))."""
    n = len(seq)
    tree = [0] * (n + 1)
    inv = 0
    for k, v in enumerate(seq):
        i = v + 1
        seen = 0
        while i > 0:
            seen += tree[i]
            i -= i & -i
        inv += k - seen
        i = v + 1
        while i <= n:
            tree[i] += 1
            i += i & -i
    return inv


def positions_moved(a, b):
    """
    How much of the permutation moved, and by how far.

    {n, moved, fraction_moved, max, mean, median, total, displacement} where
    `displacement` is the signed change of index per rule, b's index minus a's,
    and the summary figures are over its absolute value.

    Reported next to a behavioural distance and never instead of it: churn is
    the quantity that overstates functional difference, and Q-e is the bet that
    it overstates it grossly.
    """
    ra = {x: k for k, x in enumerate(a)}
    rb = {x: k for k, x in enumerate(b)}
    if len(ra) != len(a) or len(rb) != len(b) or set(ra) != set(rb):
        raise ValueError("positions_moved compares two permutations of the "
                         "same elements")
    disp = {x: rb[x] - ra[x] for x in ra}
    abs_disp = [abs(v) for v in disp.values()]
    moved = sum(1 for v in abs_disp if v)
    return {
        "n": len(a),
        "moved": moved,
        "fraction_moved": (moved / len(a)) if a else float("nan"),
        "max": max(abs_disp) if abs_disp else 0,
        "mean": statistics.mean(abs_disp) if abs_disp else float("nan"),
        "median": statistics.median(abs_disp) if abs_disp else float("nan"),
        "total": sum(abs_disp),
        "displacement": disp,
    }
