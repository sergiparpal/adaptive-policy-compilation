"""
WHERE THE 30x SPREAD COMES FROM, AT THE RULE LEVEL — D-a TO D-d.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Part four of `FINDINGS_ORDERS.md` closed the CENTRE of the corpus/space gap:
98.6% of it is which points arrive, not how often each is drawn. It explicitly
did not close the SPREAD: `touched/space` still runs 0.0544 to 1.6284 across the
2,080 pairs of `split0_starts65`, a factor of 30, and 89% of R-c's spread on a
log scale is already present at that step.

Class composition cannot produce it, and that was settled from figures on disk
before this run existed: a pair's ratio under a pure class-composition model is
a weighted average of the eight class ratios, which run 0.1952 to 2.4069, and
478 of the 2,080 pairs fall BELOW that floor.

The level below the class is the rule. An order is an order over 577 rules;
beneath a rule there is only its conditions on attributes, and the arrival skew
of those attributes is a declared property of the corpus generator. So the chain
under test is: a pair's ratio <- the arrival concentration of the rules whose
territories change hands <- the attribute marginals <- the generator.

--------------------------------------------------------------------------
THE QUANTITY, AND THE RESTRICTION THAT IS THE WHOLE DESIGN
--------------------------------------------------------------------------
For each rule r, its arrival concentration over the pure pool:

    kappa_r = (|M_r & T| / 1743) / (|M_r| / 134400)

For an order o, the TERRITORY of r is the set of cases r wins under o. For a
pair (i, j), with D_ij the cases the two orders decide differently:

    rho_hat(i, j) = mean over c in D_ij of (kappa_{r_i(c)} + kappa_{r_j(c)}) / 2

**The predictor may read `T` only through the aggregate `kappa_r`, never for an
individual case.** With per-case access the row is a tautology and nothing is
measured: the measured ratio of a pair IS the arrival density of its
disagreement set, `(|D & T| / 1743) / (|D| / 134400)`, so a predictor allowed to
intersect `D` with `T` returns the answer it is being scored against. That
quantity is computed here under the name `rho_tilde` and reported, so that the
trap is visible rather than described: it equals the measured ratio to the last
bit, over all 2,080 pairs.

What `rho_hat` must lose is the heterogeneity INSIDE a territory. How much it
loses is the finding.

--------------------------------------------------------------------------
THE PROOF THAT IT DOES NOT PEEK, WHICH IS A TEST AND NOT A PROMISE
--------------------------------------------------------------------------
`IDEAS.md` requires it: permuting `T` within each rule's extension must leave
`rho_hat` unchanged for every pair. It is executed here in two forms, because
the literal one passes for a reason that does not distinguish the two
predictors, and saying so is cheaper than being asked.

  PERM-1, the literal form.  The permutations of the space that preserve every
  rule's extension setwise are exactly the permutations that act inside the
  ATOMS of the 577 extensions — the classes of points matched by the same set of
  rules. One is drawn with seed 17 and applied to `T`. kappa is unchanged by
  construction and is checked rule by rule; `rho_hat` must come back identical
  for all 2,080 pairs.
  **What it cannot catch, stated rather than left implicit**: a winner under
  first-match-wins is constant on an atom, so `D_ij` is a union of atoms and
  `|D_ij & T|` is invariant under PERM-1 too. The tautology passes this test as
  cleanly as the predictor does.

  PERM-2, the form with teeth.  A reshuffle of `T` that preserves |M_r & T| for
  all 577 rules EXACTLY while moving mass between atoms, so that kappa is
  identical and the per-case quantity is not. It is built from pairs of moves
  that cancel: a touched point from atom A to atom B where B is matched by
  exactly A's rules plus r, and another from C to D where C is matched by
  exactly D's rules plus r. Each such pair leaves every rule's count where it
  was. Under it `rho_hat` must again be identical, and `rho_tilde` must move —
  and the run reports how many pairs it moves, because a test nothing can fail
  is not a test.

Both run BEFORE any verdict is computed, and either failing stops the run.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No new search: the orders come out of `run_full_supervision` and `run_band_1pct`
of `order_metrics_run.py`, imported and called unchanged, and the 31-row parity
gate is what says they are the published ones. `MULTISTART_SEED`,
`MULTISTART_STARTS` and `DECLARED_NEIGHBOURHOOD` are untouched and nothing here
is an argument about any of them. The 2,080 measured ratios are READ from
`order_metrics_touched.json` and reproduced, never re-measured. It runs no
`budget_and_balance_ls`, `order_search_ls`, `budget_and_balance` or `sweep*`:
those dump JSON over published records, so their functions are imported and
called instead. It writes one new file, `results3/order_metrics_rules.json`, and
rewrites none of the records it reads. Zero API calls.

Usage:  python3 -m rung3.order_metrics_rules
        python3 -m rung3.order_metrics_rules --checks   (gates only)
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS)
from rung3.order_metrics import winners
from rung3.order_metrics_run import (BUDGETS, SPLITS_FULL, build_instance,
                                        parity_band, parity_full_supervision,
                                        resumen, run_band_1pct,
                                        run_full_supervision, spearman)
from rung3.order_metrics_touched import TOUCHED_PUBLISHED, touched_mask

OUT = Path("results3")
RECORD = "order_metrics_rules.json"
SPACE_RECORD = "order_metrics.json"
TOUCHED_RECORD = "order_metrics_touched.json"
POOL = "puro"
SURFACE = ("espacio exhaustivo, pool puro, y sus 1.743 puntos tocados: kappa y "
           "el cociente medido son concentraciones de uno sobre el otro")

SET = "split0_starts65"
N_ORDERS = 65
N_PAIRS = N_ORDERS * (N_ORDERS - 1) // 2          # 2,080

# The five-number summary `IDEAS.md` declares it derived for kappa over the 577
# rules, before this module existed. It pins the POOL and the mask together: a
# different pool, a different corpus or the hybrid masks move it. Copied here
# with its source named, as the touched run copied the 1,743 and the corpus run
# copied the G2 census.
KAPPA_DECLARED = {"min": 0.0229, "p25": 0.8105, "median": 1.6265,
                  "p75": 3.3046, "max": 30.8434}
KAPPA_DECLARED_SOURCE = ("IDEAS.md, the entry 'Where the 30x spread comes from, "
                         "at the level the order actually operates on', under "
                         "'What the drafter had already seen'")

# The floor of the eight class ratios `touched(c)/all(c)`, and the count of
# pairs below it. Both are declared by the entry as derived from figures on
# disk; both are recomputed here from the published records and compared.
CLASS_FLOOR_DECLARED = 0.1952
PAIRS_BELOW_FLOOR_DECLARED = 478

# The permutation test. The seed is the project's, fixed before the test ran;
# PERM_SWAPS caps how many count-preserving move pairs PERM-2 applies, and is a
# cap on the SIZE of a perturbation whose effect on kappa is exactly zero by
# construction, not a tuning knob for any figure.
PERM_SEED = 17
PERM_SWAPS = 200


# ---------------------------------------------------------------------------
# The arrangement of the 577 extensions
# ---------------------------------------------------------------------------
#
# Two points matched by exactly the same rules are indistinguishable to every
# order: under first-match-wins the winner is the first rule of the order that
# matches, so it depends on the MATCHING SET and on nothing else. The classes of
# that relation are the atoms, and they are what makes both halves of this file
# affordable — a pair's disagreement is a union of atoms, so it is summed over
# 4,121 of them instead of 134,400 cases, and the permutation test has a group
# to permute inside.

BITS_OF_BYTE = [[k for k in range(8) if b >> (7 - k) & 1] for b in range(256)]


def bytes_of_mask(m, n):
    """
    A space mask as bytes, case 0 in the top bit of the first one.

    `Space` puts case i at bit n-1-i, so the mask is left-aligned to a byte
    boundary before it is walked and case i lands at byte i//8, bit i%8 from the
    top. n = 134,400 is a whole number of bytes and the shift is zero there; it
    is written anyway because a helper that is silently wrong for any other n is
    the kind of thing that ends up in a test with a hand-written answer.
    """
    nbytes = (n + 7) // 8
    return (m << (nbytes * 8 - n)).to_bytes(nbytes, "big")


def arrangement(ids, M, n):
    """
    The atoms of the 577 extensions, in `Space`'s bit convention.

    {patterns, rules, points, sizes, atom_of_point, index_of_pattern}: the
    pattern is a bitmask over RULE INDEX (position in `ids`), `points` are case
    indices i of the `all_cases()` enumeration, which is bit n-1-i of every
    space mask in this repository.

    Built by walking each rule's mask once as bytes, which costs one pass over
    the sum of the extensions — 5.1M point-rule incidences — instead of 577
    tests per case.
    """
    pattern_of_point = [0] * n
    for k, rid in enumerate(ids):
        m = M[rid]
        if not m:
            continue
        bit = 1 << k
        for bi, byte in enumerate(bytes_of_mask(m, n)):
            if byte:
                base = bi * 8
                for off in BITS_OF_BYTE[byte]:
                    pattern_of_point[base + off] |= bit

    index_of_pattern = {}
    patterns, points = [], []
    atom_of_point = [0] * n
    for i, p in enumerate(pattern_of_point):
        a = index_of_pattern.get(p)
        if a is None:
            a = index_of_pattern[p] = len(patterns)
            patterns.append(p)
            points.append([])
        points[a].append(i)
        atom_of_point[i] = a
    return {
        "patterns": patterns,
        "rules": [tuple(k for k in range(len(ids)) if p >> k & 1)
                  for p in patterns],
        "points": points,
        "sizes": [len(p) for p in points],
        "atom_of_point": atom_of_point,
        "index_of_pattern": index_of_pattern,
    }


def atom_census(atoms, n):
    tam = resumen(sorted(atoms["sizes"]))
    return {
        "n_atoms": len(atoms["patterns"]),
        "n_space": n,
        "sizes": tam,
        "atoms_matched_by_no_rule": sum(1 for p in atoms["patterns"] if not p),
        "note": "an atom is a class of cases matched by exactly the same set of "
                "rules. Under first-match-wins the winner is constant on an "
                "atom, so every territory and every disagreement set is a union "
                "of atoms.",
    }


def touch_by_atom(atoms, touched_points):
    """|A & T| per atom, from the case indices T contains."""
    cnt = [0] * len(atoms["patterns"])
    ap = atoms["atom_of_point"]
    for i in touched_points:
        cnt[ap[i]] += 1
    return cnt


def mask_from_points(puntos, n):
    """A space mask from case indices, in `Space`'s convention. Through a
    bytearray because 134,400 shifts of a 134,400-bit integer is not the same
    price as 134,400 byte writes."""
    nbytes = (n + 7) // 8
    ba = bytearray(nbytes)
    for i in puntos:
        ba[i >> 3] |= 128 >> (i & 7)
    return int.from_bytes(bytes(ba), "big") >> (nbytes * 8 - n)


def points_of_mask(m, n):
    """The case indices a space mask holds, the inverse of `mask_from_points`
    and by the same byte walk."""
    fuera = []
    for bi, byte in enumerate(bytes_of_mask(m, n)):
        if byte:
            base = bi * 8
            fuera.extend(base + off for off in BITS_OF_BYTE[byte])
    return fuera


# ---------------------------------------------------------------------------
# kappa, and the territories it is read through
# ---------------------------------------------------------------------------

def kappa_over_rules(ids, M, touched, n_touched, n_space):
    """
    {rule: its arrival concentration}, exactly as `IDEAS.md` defines it.

    A rule matched by a fair share of the touched points scores 1; the entry's
    own summary says the 577 span three orders of magnitude around that.
    Rules with an empty extension would have no concentration and get None
    rather than a made-up 1.0 — there are none in this pool, and the record says
    how many there were.
    """
    out = {}
    for rid in ids:
        m = M[rid]
        size = m.bit_count()
        out[rid] = (((m & touched).bit_count() / n_touched) / (size / n_space)
                    if size else None)
    return out


def gate_kappa(kappa):
    """The five numbers the entry declared, against the ones this pool gives."""
    vals = sorted(v for v in kappa.values() if v is not None)
    res = resumen([round(v, 4) for v in vals])
    filas = {k: {"recomputed": res[k], "declared": v, "reproduces": res[k] == v}
             for k, v in KAPPA_DECLARED.items()}
    return {
        "what": "kappa over the 577 rules of the pure pool, against the "
                "five-number summary the prediction declares it derived",
        "source": KAPPA_DECLARED_SOURCE,
        "n_rules": len(kappa),
        "n_with_extension": len(vals),
        "n_without_extension": sum(1 for v in kappa.values() if v is None),
        "summary_rounded_4": res,
        "comparison": filas,
        "range_factor": round(res["max"] / res["min"], 1) if res["min"] else None,
        "passes": all(f["reproduces"] for f in filas.values()),
    }


def winners_by_atom(orden, ids, atoms):
    """
    The winning rule index of every atom under one order: first-match-wins, read
    off the atom's matching set instead of the case.

    Every atom has a winner here because the pure pool covers the space; an atom
    matched by nothing gets None, and the territory gate below counts it as an
    undecided case rather than letting it pass.
    """
    idx = {rid: k for k, rid in enumerate(ids)}
    pos = [0] * len(ids)
    for k, rid in enumerate(orden):
        pos[idx[rid]] = k
    fuera = []
    for reglas in atoms["rules"]:
        fuera.append(min(reglas, key=pos.__getitem__) if reglas else None)
    return fuera


def gate_territories(orden, ids, M, sfull, n, atoms, win_atom):
    """
    The territories of one order, by two independent routes.

    The mask route is `order_metrics.winners`, the sweep every figure in this
    thread is built on. The atom route is the one this file computes with. They
    must give the same mask for every rule, and the union must be the whole
    space with no overlap — which is the invariant `IDEAS.md` names: disjoint,
    and covering every decided case.
    """
    terr, undecided = winners(orden, M, sfull)
    por_regla = {}
    for a, k in enumerate(win_atom):
        if k is not None:
            por_regla.setdefault(ids[k], []).append(a)

    reconstruido = {rid: mask_from_points(
        (i for a in aa for i in atoms["points"][a]), n)
        for rid, aa in por_regla.items()}

    union = 0
    solapan = 0
    for m in terr.values():
        solapan |= union & m
        union |= m
    return {
        "n_rules_with_territory": len(terr),
        "undecided": undecided.bit_count(),
        "disjoint": solapan == 0,
        "covers_the_space": union == sfull,
        "sum_of_territories": sum(m.bit_count() for m in terr.values()),
        "atoms_without_a_winner": sum(1 for k in win_atom if k is None),
        "atom_route_equals_mask_route": reconstruido == terr,
        "passes": (solapan == 0 and union == sfull and undecided == 0
                   and reconstruido == terr
                   and sum(m.bit_count() for m in terr.values()) == n),
    }


# ---------------------------------------------------------------------------
# The pairwise sweep: one pass over the atoms per pair
# ---------------------------------------------------------------------------

def pair_scan(act_i, act_j, kap_i, kap_j, sizes, touch):
    """
    (|D|, |D & T|, rho_hat) for one pair, summed over atoms.

    `rho_hat` is the case-weighted mean of (kappa_i + kappa_j)/2 over the
    disagreement set — case-weighted because the mean the entry writes is over
    CASES, and an atom stands for `sizes[a]` of them. `touch` is passed so that
    the tautology can be reported beside it; it enters no term of `rho_hat`,
    which is the point of the whole file.
    """
    dis = hit = 0
    s = 0.0
    for x, y, p, q, w, t in zip(act_i, act_j, kap_i, kap_j, sizes, touch):
        if x != y:
            dis += w
            hit += t
            s += w * (p + q)
    return dis, hit, (s / (2 * dis) if dis else None)


def sweep_pairs(acts, kaps, sizes, touch):
    """The 2,080 pairs of the 65 end orders, in index order i < j."""
    fuera = []
    for i in range(len(acts)):
        for j in range(i + 1, len(acts)):
            dis, hit, rho = pair_scan(acts[i], acts[j], kaps[i], kaps[j],
                                      sizes, touch)
            fuera.append({"i": i, "j": j, "disagree_space": dis,
                          "disagree_touched": hit, "rho_hat": rho})
    return fuera


def kappa_by_atom(win_atom, ids, kappa):
    """The winner's kappa per atom, which is what the sweep consumes."""
    return [kappa[ids[k]] if k is not None else 0.0 for k in win_atom]


def actions_by_atom(win_atom, ids, action):
    return [action[ids[k]] if k is not None else None for k in win_atom]


# ---------------------------------------------------------------------------
# The permutation test — blocking, and run before any verdict
# ---------------------------------------------------------------------------

def permute_within_atoms(atoms, touch, seed):
    """
    PERM-1: T', a permutation of T inside the atoms.

    The permutations of the space that preserve every rule's extension setwise
    are exactly those that act inside the atoms, so this is the literal form of
    *permuting T within each rule's extension* and not an approximation of it.
    """
    rng = random.Random(seed)
    puntos = []
    for pts, k in zip(atoms["points"], touch):
        if k:
            puntos.extend(rng.sample(pts, k) if k < len(pts) else pts)
    return sorted(puntos)


def count_preserving_reshuffle(atoms, touch, n_swaps):
    """
    PERM-2: T'', which preserves |M_r & T| for every one of the 577 rules and
    still moves points between atoms.

    Built from cancelling pairs of moves. Let `v_A` be the set of rules matching
    atom A. If `v_B = v_A + {r}`, moving a touched point from A to B raises
    rule r's count by one and leaves every other rule's alone; if `v_C = v_D +
    {r}`, moving one from C to D lowers it by one. Doing both leaves all 577
    counts exactly where they were, and the four atoms are four different
    matching sets, so the arrangement of T over the atoms has changed — which is
    what PERM-1 cannot do and what the tautology is sensitive to.

    Returns the moves and a census of the links found, never a mask: turning
    them into T'' is `apply_moves`, so that what is perturbed stays visible at
    the call site.
    """
    patrones = atoms["patterns"]
    tam = atoms["sizes"]
    idx = atoms["index_of_pattern"]
    n_rules = max((p.bit_length() for p in patrones), default=0)

    arriba, abajo = {}, {}                       # rule -> [(source, sink)]
    for a, p in enumerate(patrones):
        if not touch[a]:
            continue
        for r in range(n_rules):
            bit = 1 << r
            if p & bit:
                b = idx.get(p & ~bit)
                if b is not None and touch[b] < tam[b]:
                    abajo.setdefault(r, []).append((a, b))
            else:
                b = idx.get(p | bit)
                if b is not None and touch[b] < tam[b]:
                    arriba.setdefault(r, []).append((a, b))

    usados = set()
    movimientos = []
    for r in sorted(set(arriba) & set(abajo)):
        for (a, b) in arriba[r]:
            if len(movimientos) >= n_swaps:
                break
            if {a, b} & usados:
                continue
            for (c, d) in abajo[r]:
                if {c, d} & usados or {a, b} & {c, d}:
                    continue
                usados |= {a, b, c, d}
                movimientos.append({"rule_index": r, "up": [a, b],
                                    "down": [c, d]})
                break
        if len(movimientos) >= n_swaps:
            break
    return movimientos, {"n_rules_with_an_up_link": len(arriba),
                         "n_rules_with_a_down_link": len(abajo),
                         "n_rules_with_both": len(set(arriba) & set(abajo)),
                         "n_atoms_used": len(usados)}


def apply_moves(atoms, touched_points, movimientos):
    """T'' as case indices: each move takes a touched point out of one atom and
    puts an untouched one into another."""
    en_t = set(touched_points)
    fuera = set(touched_points)
    detalle = []
    for mv in movimientos:
        for origen, destino in (mv["up"], mv["down"]):
            sale = next(i for i in atoms["points"][origen] if i in en_t)
            entra = next(i for i in atoms["points"][destino] if i not in en_t)
            fuera.discard(sale)
            fuera.add(entra)
            en_t.discard(sale)
            en_t.add(entra)
            detalle.append({"from_atom": origen, "to_atom": destino,
                            "point_out": sale, "point_in": entra})
    return sorted(fuera), detalle


def permutation_test(nombre, descripcion, kappa, kappa2, pares, pares2,
                     touched, touched2, catches):
    """One arm of the test, reported as a row: kappa identical, rho_hat
    identical, and what the per-case quantity did."""
    k_dif = [rid for rid in kappa if kappa[rid] != kappa2[rid]]
    r_dif = [[p["i"], p["j"]] for p, q in zip(pares, pares2)
             if p["rho_hat"] != q["rho_hat"]]
    t_dif = [(p, q) for p, q in zip(pares, pares2)
             if p["disagree_touched"] != q["disagree_touched"]]
    d_dif = [1 for p, q in zip(pares, pares2)
             if p["disagree_space"] != q["disagree_space"]]
    return {
        "what": nombre,
        "how": descripcion,
        "bits_of_T_moved": (touched ^ touched2).bit_count(),
        "T_size_preserved": touched.bit_count() == touched2.bit_count(),
        "kappa_identical": not k_dif,
        "n_rules_whose_kappa_moved": len(k_dif),
        "rho_hat_identical": not r_dif,
        "n_pairs_whose_rho_hat_moved": len(r_dif),
        "pairs_that_moved": r_dif[:20],
        "disagreement_sets_untouched": not d_dif,
        "n_pairs_whose_per_case_quantity_moved": len(t_dif),
        "per_case_quantity_max_absolute_move": max(
            (abs(p["disagree_touched"] - q["disagree_touched"])
             for p, q in t_dif), default=0),
        "catches_a_predictor_reading_T_per_case": catches,
        "passes": (not k_dif and not r_dif and not d_dif
                   and touched.bit_count() == touched2.bit_count()),
    }


# ---------------------------------------------------------------------------
# The last link: does kappa come from the attribute marginals (D-d)
# ---------------------------------------------------------------------------

def condition_concentrations(space, conds, touched, n_touched, n_space):
    """
    The same concentration, computed for a single condition instead of a rule.

    `c(cond)` is what kappa would be for a one-condition rule, so a rule whose
    attributes were independent under both measures would have exactly
    kappa_r = prod c(cond). The gap between the two is the last link of the
    chain, and it is REPORTED: D-d says so, and it says why — both sides are
    computable from data already on disk, so no honest band could be written for
    it now.
    """
    fuera = {}
    for cs in conds.values():
        for c in cs:
            clave = (c.attr, c.op,
                     tuple(c.value) if isinstance(c.value, (list, set, tuple))
                     else c.value)
            if clave in fuera:
                continue
            m = space.condition_mask(c)
            size = m.bit_count()
            fuera[clave] = {
                "attr": c.attr, "op": c.op, "value": str(c.value),
                "space_share": round(size / n_space, 6),
                "touched_share": round((m & touched).bit_count() / n_touched, 6),
                "concentration": (((m & touched).bit_count() / n_touched)
                                  / (size / n_space)) if size else None,
            }
    return fuera


def marginal_prediction(ids, conds, cc):
    """prod of the per-condition concentrations, per rule."""
    fuera = {}
    for rid in ids:
        v = 1.0
        ok = True
        for c in conds[rid]:
            clave = (c.attr, c.op,
                     tuple(c.value) if isinstance(c.value, (list, set, tuple))
                     else c.value)
            k = cc[clave]["concentration"]
            if k is None:
                ok = False
                break
            v *= k
        fuera[rid] = v if ok else None
    return fuera


# ---------------------------------------------------------------------------
# D-a to D-d, adjudicated exactly as they are written
# ---------------------------------------------------------------------------
#
# NOT re-specified, before or after seeing a number. None of these rows has a
# dead zone, and that is deliberate on the entry's part: every band's edges are
# its refutation lines. D-d is REPORTED and carries no verdict, as its own row
# says.

def adjudicate(rho_spearman, residual, debajo, floor):
    q = {}

    q["D-a"] = {
        "claim": "Spearman between rho_hat and the measured ratio, over the "
                 "2,080 pairs of split0_starts65, lands between 0.75 and 0.97. "
                 "Refuted below 0.75 or above 0.97. Below is the informative "
                 "side: it would mean the heterogeneity inside a rule's "
                 "territory dominates the differences between rules, and the "
                 "explanation lives beneath the rule level, in the attributes "
                 "directly.",
        "band": [0.75, 0.97], "no_dead_zone": True,
        "spearman": rho_spearman,
        "verdict": ("HOLDS" if rho_spearman is not None
                    and 0.75 <= rho_spearman <= 0.97 else "REFUTED"),
    }

    p75_p25 = residual["p75_over_p25"]
    q["D-b"] = {
        "claim": "the residual rho / rho_hat still spans p75/p25 above 1.20. "
                 "Refuted at or below 1.20, which would say the rule level "
                 "closes the spread completely and nothing is left inside the "
                 "territories. D-a and D-b are a single position taken in two "
                 "halves — rules explain most of it and not all of it — and the "
                 "entry is wrong if either half fails.",
        "threshold": 1.20, "no_dead_zone": True,
        "p75_over_p25": p75_p25,
        "residual": residual,
        "verdict": ("HOLDS" if p75_p25 is not None and p75_p25 > 1.20
                    else "REFUTED"),
    }

    frac = (debajo["n_rho_hat_below"] / debajo["n_measured_below"]
            if debajo["n_measured_below"] else None)
    q["D-c"] = {
        "claim": "of the 478 pairs that fall below the 0.1952 class floor, at "
                 "least three quarters have rho_hat below that floor too. "
                 "Refuted below three quarters. This is the row that ties the "
                 "mechanism to the specific anomaly the C entry left behind, "
                 "rather than to the spread in general.",
        "threshold": 0.75, "no_dead_zone": True,
        "floor": floor,
        "floor_declared": CLASS_FLOOR_DECLARED,
        "n_pairs_below_the_floor": debajo["n_measured_below"],
        "n_pairs_below_declared": PAIRS_BELOW_FLOOR_DECLARED,
        "n_of_those_with_rho_hat_below": debajo["n_rho_hat_below"],
        "fraction": round(frac, 6) if frac is not None else None,
        "verdict": ("HOLDS" if frac is not None and frac >= 0.75
                    else "REFUTED"),
    }
    return q


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    solo_checks = "--checks" in argv
    t_start = time.time()

    print("=" * 78)
    print("D-a..D-d — THE 30x SPREAD AT THE RULE LEVEL")
    print("=" * 78)
    print(f"  optimizer: {DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} declared starts + the greedy (untouched)")
    print(f"  set {SET} · {N_PAIRS} pairs · pool {POOL} · no new search, "
          f"no API calls")
    print(f"  {describe()}")

    inst = build_instance()
    sM, _sW, sfull, sn = inst["space"]
    ids = inst["ids"]
    print(f"  instance ready in {inst['seconds_setup']}s: {len(ids)} rules, "
          f"{len(inst['corpus'])} corpus cases, {sn:,} space cases")

    tocado = json.loads((OUT / TOUCHED_RECORD).read_text())

    # ------------------------------------------------------------- the mask
    touched, censo = touched_mask(inst["corpus"])
    n_touched = touched.bit_count()
    g_mask = {
        "what": "the touched mask, the same object part four built",
        "n_bits": n_touched, "published_n_bits": TOUCHED_PUBLISHED,
        "census": censo,
        "inside_the_space": touched & ~sfull == 0,
        "passes": n_touched == TOUCHED_PUBLISHED and touched & ~sfull == 0,
    }
    print()
    print(f"MASK GATE — {censo['n_corpus_draws']:,} draws on {n_touched:,} "
          f"distinct points, published {TOUCHED_PUBLISHED:,}"
          f"{'  ok' if g_mask['passes'] else '  NO'}")
    if not g_mask["passes"]:
        print("  STOP: the mask is not the one the record publishes.")
        return 1

    # -------------------------------------------------------------- kappa
    t0 = time.time()
    kappa = kappa_over_rules(ids, sM, touched, n_touched, sn)
    g_kappa = gate_kappa(kappa)
    print()
    print("KAPPA GATE — the five numbers the prediction declares it derived")
    for k in ("min", "p25", "median", "p75", "max"):
        f = g_kappa["comparison"][k]
        print(f"  {k:<8}{f['recomputed']:>10}   declared {f['declared']:>10}"
              f"{'  ok' if f['reproduces'] else '  NO'}")
    print(f"  range {g_kappa['range_factor']}x over {g_kappa['n_with_extension']} "
          f"rules ({time.time() - t0:.0f}s)")
    if not g_kappa["passes"]:
        print("  STOP: this is not the pool the prediction was written about.")
        return 1

    # ------------------------------------------------------------- the atoms
    t0 = time.time()
    atoms = arrangement(ids, sM, sn)
    censo_atomos = atom_census(atoms, sn)
    puntos_t = points_of_mask(touched, sn)
    touch_atom = touch_by_atom(atoms, puntos_t)
    print()
    print(f"ARRANGEMENT — {censo_atomos['n_atoms']:,} atoms of the 577 "
          f"extensions, sizes {censo_atomos['sizes']['min']}–"
          f"{censo_atomos['sizes']['max']} ({time.time() - t0:.0f}s)")

    # ------------------------------------------------------------ regeneration
    print()
    print("REGENERATING, keeping every end order (the P4 path, unmodified)")
    runs = {}
    for s in SPLITS_FULL:
        runs[s] = run_full_supervision(inst, s)
        print(f"  split {s}: {max(BUDGETS)} starts in {runs[s]['seconds']}s")

    par_a = parity_full_supervision(inst, [runs[s] for s in SPLITS_FULL])
    print()
    print("PARITY GATE — against results3/start_budget_check.json")
    print(f"  {'split':>6}{'starts':>8}{'train_score':>13}{'train':>9}"
          f"{'test':>9}{'space':>9}{'':>4}")
    for f in par_a:
        c = f["comparison"]
        print(f"  {f['split']:>6}{f['starts']:>8}{c['train_score'][0]:>13}"
              f"{c['train'][0]:>9.4f}{c['test'][0]:>9.4f}{c['space'][0]:>9.4f}"
              f"{'  ok' if f['passes'] else '  NO':>4}")
        if not f["passes"]:
            for m, (mio, pub, ok) in c.items():
                if not ok:
                    print(f"        {m}: regenerated {mio} vs published {pub}")

    band = run_band_1pct(inst)
    par_b = parity_band(inst, band)
    malas = [f for f in par_b if not f["passes"]]
    print()
    print("PARITY GATE — the 1% band against "
          "results3/budget_and_balance_ls.json")
    print(f"  {len(par_b) - len(malas)}/{len(par_b)} cells reproduce exactly")
    for f in malas:
        print(f"    split {f['split']} draw {f['draw']}: "
              + ", ".join(f"{m} regenerated {v[0]} vs published {v[1]}"
                          for m, v in f["comparison"].items() if not v[2]))
    n_filas = len(par_a) + len(par_b)
    if malas or not all(f["passes"] for f in par_a):
        print("\n  STOP: a parity failure means the regenerated orders are not "
              "the measured ones, and nothing below would be about them.")
        return 1
    print(f"\n  PARITY: PASSES, {n_filas}/{n_filas} rows. The regenerated "
          f"orders are the published ones.")

    # ---------------------------------------------------- the 65 orders and D
    s0 = SPLITS_FULL[0]
    orders = [r["order"] for r in runs[s0]["stats"]["rows"][:N_ORDERS]]

    t0 = time.time()
    win_atom = [winners_by_atom(o, ids, atoms) for o in orders]
    acts = [actions_by_atom(w, ids, inst["action"]) for w in win_atom]
    kaps = [kappa_by_atom(w, ids, kappa) for w in win_atom]
    print(f"\n  territories of the {N_ORDERS} end orders in "
          f"{time.time() - t0:.0f}s")

    t0 = time.time()
    g_terr = {"per_order": [], "passes": True}
    for k, o in enumerate(orders):
        fila = gate_territories(o, ids, sM, sfull, sn, atoms, win_atom[k])
        fila["order"] = k
        g_terr["per_order"].append(fila)
        g_terr["passes"] &= fila["passes"]
    g_terr["what"] = ("every case has exactly one winner under each of the 65 "
                      "orders: the territories are pairwise disjoint, they "
                      "cover the space, nothing is left undecided, and the atom "
                      "route gives the same mask per rule as the sweep every "
                      "other figure in this thread is built on")
    g_terr["n_orders"] = len(orders)
    g_terr["n_orders_passing"] = sum(1 for f in g_terr["per_order"]
                                     if f["passes"])
    print("TERRITORY GATE — disjoint, covering, and equal by two routes")
    print(f"  {g_terr['n_orders_passing']}/{g_terr['n_orders']} orders pass; "
          f"undecided cases "
          f"{max(f['undecided'] for f in g_terr['per_order'])}; "
          f"rules with a territory "
          f"{min(f['n_rules_with_territory'] for f in g_terr['per_order'])}–"
          f"{max(f['n_rules_with_territory'] for f in g_terr['per_order'])}"
          f"  ({time.time() - t0:.0f}s)")
    if not g_terr["passes"]:
        print("  STOP: the territories are not a partition of the space.")
        return 1

    # ------------------------------------------------------- the pairwise sweep
    t0 = time.time()
    pares = sweep_pairs(acts, kaps, atoms["sizes"], touch_atom)
    print(f"  {len(pares):,} pairs swept over the atoms in "
          f"{time.time() - t0:.0f}s")

    # ----------------------------------------- the measured ratios, READ
    filas_pub = {(p["i"], p["j"]): p
                 for p in tocado[f"pairs_{SET}_touched"]}
    medidos = {}
    for p in pares:
        pub = filas_pub.get((p["i"], p["j"]))
        if pub:
            medidos[(p["i"], p["j"])] = pub["rate_touched"] / pub["rate_space"]
    razon_pub = tocado["predictions"]["C-d"]["ratios"]["touched_over_space"]
    res_medidos = resumen(sorted(medidos.values()))
    reproduce = {
        k: (res_medidos[k], razon_pub["resumen"][k],
            res_medidos[k] == razon_pub["resumen"][k])
        for k in ("n", "min", "p25", "median", "mean", "p75", "max")}
    reproduce["p75_over_p25"] = (
        round(res_medidos["p75"] / res_medidos["p25"], 6),
        razon_pub["p75_over_p25"],
        round(res_medidos["p75"] / res_medidos["p25"], 6)
        == razon_pub["p75_over_p25"])
    reproduce["max_over_min"] = (
        round(res_medidos["max"] / res_medidos["min"], 6),
        razon_pub["max_over_min"],
        round(res_medidos["max"] / res_medidos["min"], 6)
        == razon_pub["max_over_min"])
    difieren = [[p["i"], p["j"]] for p in pares
                if (p["i"], p["j"]) not in filas_pub
                or p["disagree_space"] != filas_pub[(p["i"], p["j"])]["disagree_space"]
                or p["disagree_touched"] != filas_pub[(p["i"], p["j"])]["disagree_touched"]]
    g_matrix = {
        "what": "the 2,080 measured ratios are READ from the touched record and "
                "reproduced, never re-measured: their summary comes back "
                "identical to the one that record publishes, and the two counts "
                "each ratio is built from — |D| over the space and |D & T| — "
                "come back identical from the regenerated orders, which is what "
                "says the read rows are about these orders",
        "source": f"{TOUCHED_RECORD}::pairs_{SET}_touched and "
                  f"::predictions.C-d.ratios.touched_over_space",
        "n_read": len(medidos), "n_expected": N_PAIRS,
        "key_sets_identical": set(medidos) == set(filas_pub),
        "summary_reproduces": reproduce,
        "n_pairs_whose_counts_differ": len(difieren),
        "pairs_that_differ": difieren[:20],
        "passes": (len(medidos) == N_PAIRS and not difieren
                   and all(v[2] for v in reproduce.values())),
    }
    print()
    print(f"MATRIX GATE — the 2,080 measured ratios, read from {TOUCHED_RECORD}")
    print(f"  read {g_matrix['n_read']:,}, counts differing on "
          f"{g_matrix['n_pairs_whose_counts_differ']} pairs, summary "
          f"reproduces "
          f"{all(v[2] for v in reproduce.values())}"
          f"{'  ok' if g_matrix['passes'] else '  NO'}")
    if not g_matrix["passes"]:
        print("  STOP: the read ratios are not the published ones, or not "
              "about these orders.")
        return 1

    # --------------------------------------------------- THE PERMUTATION TEST
    print()
    print("PERMUTATION TEST — before any verdict is computed")
    t0 = time.time()
    p1_puntos = permute_within_atoms(atoms, touch_atom, PERM_SEED)
    t1 = mask_from_points(p1_puntos, sn)
    k1 = kappa_over_rules(ids, sM, t1, t1.bit_count(), sn)
    tp1 = touch_by_atom(atoms, p1_puntos)
    kaps1 = [[k1[ids[k]] if k is not None else 0.0 for k in w] for w in win_atom]
    pares1 = sweep_pairs(acts, kaps1, atoms["sizes"], tp1)
    perm1 = permutation_test(
        "PERM-1, the literal form",
        "a permutation of T inside the atoms of the 577 extensions, seed "
        f"{PERM_SEED}. The permutations of the space that preserve every rule's "
        "extension setwise are exactly these, so it is the literal form of "
        "IDEAS.md's 'permuting T within each rule's extension' rather than an "
        "approximation of it.",
        kappa, k1, pares, pares1, touched, t1,
        catches=False)
    perm1["cannot_catch"] = (
        "a winner is constant on an atom, so D_ij is a union of atoms and "
        "|D_ij & T| is invariant under this permutation too: the tautology "
        "passes this arm as cleanly as the predictor does. That is why PERM-2 "
        "exists, and it is stated here rather than left for a reader to notice.")

    movimientos, censo_enlaces = count_preserving_reshuffle(
        atoms, touch_atom, PERM_SWAPS)
    p2_puntos, detalle = apply_moves(atoms, puntos_t, movimientos)
    t2 = mask_from_points(p2_puntos, sn)
    k2 = kappa_over_rules(ids, sM, t2, t2.bit_count(), sn)
    tp2 = touch_by_atom(atoms, p2_puntos)
    kaps2 = [[k2[ids[k]] if k is not None else 0.0 for k in w] for w in win_atom]
    pares2 = sweep_pairs(acts, kaps2, atoms["sizes"], tp2)
    perm2 = permutation_test(
        "PERM-2, the form with teeth",
        f"{len(movimientos)} cancelling pairs of moves between atoms, each pair "
        "raising and lowering one rule's count by one so that all 577 counts "
        "are preserved exactly while T changes which atoms it sits in. kappa "
        "cannot move; a predictor reading T per case must.",
        kappa, k2, pares, pares2, touched, t2,
        catches=True)
    perm2["n_move_pairs"] = len(movimientos)
    perm2["moves"] = detalle[:8]
    perm2["cap"] = PERM_SWAPS
    perm2["links"] = censo_enlaces

    for arm in (perm1, perm2):
        print(f"  {arm['what']}: {arm['bits_of_T_moved']} bits of T moved, "
              f"kappa identical {arm['kappa_identical']}, rho_hat identical "
              f"{arm['rho_hat_identical']}, per-case quantity moved on "
              f"{arm['n_pairs_whose_per_case_quantity_moved']} pairs"
              f"{'  ok' if arm['passes'] else '  NO'}")
    g_perm = {
        "what": "IDEAS.md: 'permuting T within each rule's extension must leave "
                "rho_hat unchanged for every pair. If it moves, the predictor "
                "is reading T per case and D-a is a tautology.'",
        "seed": PERM_SEED,
        "arms": [perm1, perm2],
        "seconds": round(time.time() - t0, 1),
        "passes": perm1["passes"] and perm2["passes"]
                  and perm2["n_pairs_whose_per_case_quantity_moved"] > 0,
    }
    if not g_perm["passes"]:
        print("\n  STOP: rho_hat moved when only the arrangement of T did. The "
              "predictor is reading T per case and D-a would be a tautology.")
        return 1
    print(f"  PERMUTATION: PASSES ({g_perm['seconds']}s)")

    if solo_checks:
        print(f"\n  ALL SIX GATES PASS. total cost: {time.time() - t_start:.0f}s")
        return 0

    # ------------------------------------------------------ the tautology, named
    tauto = {}
    for p in pares:
        r = ((p["disagree_touched"] / n_touched)
             / (p["disagree_space"] / sn)) if p["disagree_space"] else None
        tauto[(p["i"], p["j"])] = r
    dif_tauto = max(abs(round(tauto[k], 6) - round(medidos[k], 6))
                    for k in medidos)
    control = {
        "what": "rho_tilde, the predictor the restriction exists to forbid: the "
                "arrival density of the disagreement set itself, computed with "
                "per-case access to T",
        "spearman_against_the_measured_ratio": spearman(
            [tauto[k] for k in sorted(medidos)],
            [medidos[k] for k in sorted(medidos)]),
        "max_absolute_difference_from_the_measured_ratio_at_6_dp": dif_tauto,
        "note": "it is not merely correlated with the measured ratio, it IS the "
                "measured ratio: the two agree to the resolution the published "
                "rates carry. A predictor with per-case access to T scores 1 by "
                "construction and measures nothing, which is why rho_hat may "
                "read T only through kappa and why the permutation test above "
                "is blocking.",
    }

    # -------------------------------------------------------------- D-a to D-c
    xs = [p["rho_hat"] for p in pares]
    ys = [medidos[(p["i"], p["j"])] for p in pares]
    rho_spearman = spearman(xs, ys)

    residuo = [{"i": p["i"], "j": p["j"],
                "r": medidos[(p["i"], p["j"])] / p["rho_hat"]}
               for p in pares if p["rho_hat"]]
    res_residuo = resumen(sorted(r["r"] for r in residuo))
    residual = {
        "n": len(residuo),
        "n_dropped_zero_denominator": len(pares) - len(residuo),
        "resumen": res_residuo,
        "p75_over_p25": round(res_residuo["p75"] / res_residuo["p25"], 6)
                        if res_residuo["p25"] else None,
        "max_over_min": round(res_residuo["max"] / res_residuo["min"], 6)
                        if res_residuo["min"] else None,
    }

    tasas_clase = tocado["rates_by_class"]
    razones_clase = {c: v["touched"] / v["all"] for c, v in tasas_clase.items()}
    floor = min(razones_clase.values())
    techo = max(razones_clase.values())
    bajo_medido = [p for p in pares if medidos[(p["i"], p["j"])] < floor]
    debajo = {
        "n_measured_below": len(bajo_medido),
        "n_rho_hat_below": sum(1 for p in bajo_medido if p["rho_hat"] < floor),
        "n_measured_below_declared_floor": sum(
            1 for p in pares if medidos[(p["i"], p["j"])] < CLASS_FLOOR_DECLARED),
        "n_measured_above_the_ceiling": sum(
            1 for p in pares if medidos[(p["i"], p["j"])] > techo),
        "n_rho_hat_below_over_all_pairs": sum(1 for p in pares
                                              if p["rho_hat"] < floor),
    }

    q = adjudicate(rho_spearman, residual, debajo, floor)

    # ---------------------------------------------------------------- D-d
    t0 = time.time()
    space = Space()
    cc = condition_concentrations(space, inst["conds"], touched, n_touched, sn)
    pred = marginal_prediction(ids, inst["conds"], cc)
    comunes = [rid for rid in ids
               if pred[rid] is not None and kappa[rid] is not None]
    razon_marg = sorted(kappa[rid] / pred[rid] for rid in comunes if pred[rid])
    res_marg = resumen(razon_marg)
    por_atributo = {}
    for v in cc.values():
        if v["concentration"] is not None:
            por_atributo.setdefault(v["attr"], []).append(v["concentration"])
    q["D-d"] = {
        "claim": "reported, and it cannot be a prediction: whether kappa_r "
                 "tracks the arrival marginals of the attributes in r's "
                 "conditions. Reported and not adjudicated because both sides "
                 "are computable from data already on disk, so no honest band "
                 "could be written for it now. It is here because the chain is "
                 "only closed if someone looks.",
        "adjudicates": False,
        "model": "kappa_hat(r) = prod over r's conditions of c(cond), where "
                 "c(cond) is the same concentration computed for a "
                 "one-condition rule. It is what kappa would be if the "
                 "attributes were independent under both measures.",
        "n_rules": len(comunes),
        "n_conditions_distinct": len(cc),
        "spearman_kappa_vs_marginal_prediction": spearman(
            [kappa[rid] for rid in comunes], [pred[rid] for rid in comunes]),
        "ratio_kappa_over_prediction": res_marg,
        "ratio_p75_over_p25": (round(res_marg["p75"] / res_marg["p25"], 6)
                               if res_marg and res_marg["p25"] else None),
        "by_condition": {
            f"{k[0]}|{k[1]}|{k[2]}": v for k, v in
            sorted(cc.items(),
                   key=lambda kv: (kv[1]["concentration"] is None,
                                   kv[1]["concentration"] or 0.0))},
        "by_attribute": {a: {"n_conditions": len(v),
                             "min": round(min(v), 6), "max": round(max(v), 6)}
                         for a, v in sorted(por_atributo.items())},
        "seconds": round(time.time() - t0, 1),
    }

    # ----------------------------------------------------------------- output
    print()
    print("=" * 78)
    print("D-a..D-d, AS WRITTEN")
    print("=" * 78)
    print(f"  D-a  Spearman(rho_hat, measured) = {q['D-a']['spearman']}   "
          f"band [0.75, 0.97]   {q['D-a']['verdict']}")
    print(f"  D-b  residual p75/p25 = {q['D-b']['p75_over_p25']}   "
          f"above 1.20   {q['D-b']['verdict']}")
    print(f"  D-c  {q['D-c']['n_of_those_with_rho_hat_below']} of "
          f"{q['D-c']['n_pairs_below_the_floor']} = {q['D-c']['fraction']}   "
          f"at least 0.75   {q['D-c']['verdict']}")
    print(f"  D-d  reported: Spearman(kappa, marginals) = "
          f"{q['D-d']['spearman_kappa_vs_marginal_prediction']}, "
          f"kappa/prediction p75/p25 = {q['D-d']['ratio_p75_over_p25']}")
    print()
    print(f"  the control: rho_tilde, with per-case access to T, correlates "
          f"{control['spearman_against_the_measured_ratio']} with the measured "
          f"ratio")

    payload = {
        "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            budgets=list(BUDGETS), set_measured=SET,
                            n_pairs=N_PAIRS, n_orders=N_ORDERS,
                            permutation_seed=PERM_SEED),
        "what":
            "D-a to D-d of IDEAS.md, adjudicated. The same 65 end orders of "
            "split 0 and the same 2,080 pairs as order_metrics.json, "
            "order_metrics_corpus.json and order_metrics_touched.json. It asks "
            "whether the factor-of-30 spread in the per-pair ratio "
            "touched/space is the arrival concentration of the RULES whose "
            "territories change hands: kappa_r = (|M_r & T| / 1743) / (|M_r| / "
            "134400) per rule, and rho_hat(i,j) = the mean over D_ij of the two "
            "winners' kappa. The predictor reads T only through kappa, never "
            "per case — the permutation test in gates.permutation is what makes "
            "that a fact rather than a claim, and the tautology it forbids is "
            "computed and reported as rho_tilde. No new search: the orders come "
            "out of run_full_supervision and run_band_1pct of "
            "order_metrics_run.py, imported and called unchanged, and the "
            "31-row parity gate is what says they are the published ones. The "
            "2,080 measured ratios are read from order_metrics_touched.json and "
            "reproduced, not re-measured. No record it reads is rewritten. Zero "
            "API calls.",
        "prediction":
            "IDEAS.md, the entry 'Where the 30x spread comes from, at the level "
            "the order actually operates on', drafted, signed and committed "
            "before the territories existed",
        "surface": SURFACE,
        "surface_note":
            "kappa and rho_hat are over the EXHAUSTIVE SPACE, pure pool, with "
            "the 1,743 touched points entering only as a mask and only through "
            "the per-rule aggregate. The measured ratio each pair is scored "
            "against is touched/space, published by part four of "
            "FINDINGS_ORDERS.md. The train, test and space figures of the "
            "parity gate are the surfaces of the records being reproduced.",
        "pool": POOL,
        "n_rules": len(ids),
        "n_space": sn,
        "n_touched": n_touched,
        "n_corpus": len(inst["corpus"]),
        "splits": list(SPLITS_FULL),
        "budgets": list(BUDGETS),
        "gates": {
            "mask": g_mask,
            "kappa": g_kappa,
            "parity_rows": n_filas,
            "parity_full_supervision": par_a,
            "parity_band_1pct": par_b,
            "matrix": g_matrix,
            "territories": g_terr,
            "permutation": g_perm,
        },
        "no_new_search":
            "every order measured here comes out of run_full_supervision and "
            "run_band_1pct of order_metrics_run.py, imported and called "
            "unchanged. The prefix shortcut is not revalidated: it was checked "
            "against an independent 65-start run when it was introduced. "
            "MULTISTART_SEED, MULTISTART_STARTS and DECLARED_NEIGHBOURHOOD are "
            "untouched and no figure here is an argument about any of them.",
        "atoms": censo_atomos,
        "kappa_summary": g_kappa["summary_rounded_4"],
        "kappa_by_rule": {rid: (round(v, 6) if v is not None else None)
                          for rid, v in kappa.items()},
        "class_ratios_touched_over_all": {c: round(v, 6)
                                          for c, v in sorted(razones_clase.items())},
        "class_floor": floor,
        "class_ceiling": techo,
        "pairs_below_the_class_floor": debajo,
        "control_rho_tilde": control,
        "residual": residual,
        "pairs_split0_starts65_rules": [
            {"i": p["i"], "j": p["j"],
             "rho_hat": round(p["rho_hat"], 6) if p["rho_hat"] else None,
             "ratio_measured": round(medidos[(p["i"], p["j"])], 6),
             "disagree_space": p["disagree_space"],
             "disagree_touched": p["disagree_touched"]}
            for p in pares],
        "pairs_stored":
            "the full 2,080-row triangle: each pair's rho_hat, the measured "
            "ratio read from the touched record, and the two counts the gate "
            "matched them by, so that D-a to D-c can be recomputed from this "
            "file alone",
        "predictions": q,
        "seconds": {
            "setup": inst["seconds_setup"],
            "search_full_supervision": {s: runs[s]["seconds"]
                                        for s in SPLITS_FULL},
            "search_band_1pct": round(sum(f["seconds"] for f in band), 1),
            "permutation_test": g_perm["seconds"],
            "total": round(time.time() - t_start, 1),
        },
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
