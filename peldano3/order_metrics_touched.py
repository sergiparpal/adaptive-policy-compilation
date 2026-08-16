"""
WHICH POINTS ARRIVE, OR HOW OFTEN — C-a TO C-d.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Two orders disagree on 20.35% of the exhaustive space and 5.75% of the corpus,
the same 2,080 pairs of the same 65 end orders. Class reweighting — carry each
class's space rate over unchanged and weight it by how often the class arrives —
predicts 11.67%, and misses by 2.03x. `R-c` reported that the centre of that
miss is stable across pairs, and `IDEAS.md` decomposed it by class: it is not
spread at all, **T2_TECHNICAL carries 98.5% of it**.

Reweighting corrects for how often a class arrives and assumes the rate WITHIN a
class transfers. It does not. That failure splits in two, and only one half has
ever been measured:

  which points get touched   the 2,000 draws land on 1,743 of the 134,400
                             points, 1.3% of the space, concentrated on common
                             attribute combinations. If disagreement lives in
                             the rare corners, this alone would produce the
                             overestimate.  **UNMEASURED — this is the run.**
  how often each is touched  the multiplicity of those 1,743 points under the
                             arrival distribution. Already measured: it is the
                             difference between `touched` and `arrivals` below.

--------------------------------------------------------------------------
EVERY MEASUREMENT IS ON THE SPACE SIDE, AND THAT IS THE POINT
--------------------------------------------------------------------------
The corpus contributes a MASK and nothing else: which of the 134,400 points it
reaches. Every rate below is computed over `Space`'s bit convention, from
`order_search_ls.space_truth_masks` and the space pools, and no mask is ever
joined across the two conventions in this repository (`build_masks` puts case
`idxs[k]` at bit k; `Space` puts case k at bit n-1-k). That is what makes this
question safer than the corpus one, where the whole per-class apparatus had to be
rebuilt in the other convention — and it is why `arrivals(c)` is READ from the
published record rather than recomputed here. Three rates per class:

  all(c)        over every space point of the class.  PUBLISHED, and the second
                gate is that it reproduces exactly
                (`order_metrics.json::per_class.pooled_split0_65.by_class`).
  touched(c)    over only the points the corpus reaches, WITHOUT multiplicity.
                The one new quantity in this file.
  arrivals(c)   over the 2,000 draws, with multiplicity.  PUBLISHED
                (`order_metrics_corpus.json::per_class.corpus_full`).

`touched(c)` is `all(c)` with the class's truth mask ANDed with the touched
mask, handed to the same `per_class_over_pairs` that produced the published
figure. Same instrument, same pairs, same orders: only the denominator moves.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
PARITY, blocking and inherited: the same 31 rows — six budget rows against
`start_budget_check.json` and the whole 1% band against
`budget_and_balance_ls.json` — reproduce exactly, or the regenerated orders are
not the published ones and nothing here is about them.

THE PUBLISHED `all(c)`, blocking: the eight per-class rates and the overall rate
of `pooled_split0_65` come back identical from the regenerated orders. Parity
compares four scores per row; this compares the per-class behaviour the question
is actually about.

THE MATRIX, blocking: all 2,080 per-pair `disagree` and `rate` values reproduce
`order_metrics.json::pairs_split0_starts65` exactly. It is what makes the
per-pair half of C-d a re-weighting of the published matrix rather than a
second, unrelated one.

THE MASK, blocking: exactly 1,743 bits, the figure `FINDINGS_ORDERS.md` already
publishes for the distinct cases the 2,000 draws touch; every corpus case maps
into the space; and the class masks partition both the space and the touched
mask.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No new search: the orders come out of `run_full_supervision` and `run_band_1pct`
of `order_metrics_run.py`, imported and called unchanged.
`MULTISTART_SEED`, `MULTISTART_STARTS` and `DECLARED_NEIGHBOURHOOD` are
untouched and nothing here is an argument about any of them. It runs no
`budget_and_balance_ls`, `order_search_ls`, `budget_and_balance` or `sweep*`:
those dump JSON over published records, so their functions are imported and
called instead. It writes one new file, `results3/order_metrics_touched.json`,
and rewrites neither of the two records it reads. Zero API calls.

Usage:  python3 -m peldano3.order_metrics_touched
        python3 -m peldano3.order_metrics_touched --checks   (gates only)
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.provenance import describe, environment
from peldano2.engine2 import Space
from peldano3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS)
from peldano3.order_metrics import agreement_masks
from peldano3.order_metrics_run import (BUDGETS, SPLITS_FULL, build_instance,
                                        decisions_and_signatures, pairwise,
                                        parity_band, parity_full_supervision,
                                        per_class_over_pairs, resumen,
                                        run_band_1pct, run_full_supervision)

OUT = Path("results3")
RECORD = "order_metrics_touched.json"
SPACE_RECORD = "order_metrics.json"
CORPUS_RECORD = "order_metrics_corpus.json"
POOL = "puro"
SURFACE = "espacio exhaustivo, restringido a los puntos que el corpus toca"

SET = "split0_starts65"
N_ORDERS = 65
N_PAIRS = N_ORDERS * (N_ORDERS - 1) // 2          # 2,080

# `FINDINGS_ORDERS.md`, part two, S-e: "the 2000 draws touch 1,743 distinct
# cases". It is the one published figure that pins the MASK this run builds, so
# it is copied here with its source named, in the same way the corpus run copied
# the G2 census.
TOUCHED_PUBLISHED = 1743

# The class the decomposition puts 98.5% of the gap on, and the one C-a names.
CLASE_C_A = "T2_TECHNICAL"

# ---------------------------------------------------------------------------
# What the record says about itself, as constants so that the committed text and
# the module cannot drift apart.
# ---------------------------------------------------------------------------

TRUTH_PROVENANCE = (
    "every rate in this record is over the EXHAUSTIVE SPACE in Space's bit "
    "convention, case k at bit n-1-k. The per-class truth is "
    "order_search_ls.space_truth_masks, which for this surface is the correct "
    "source and is the one order_metrics.json used for the figures the second "
    "gate reproduces. The corpus contributes exactly one object, `touched`: the "
    "mask of the points its 2,000 draws land on, built by mapping each corpus "
    "case to its index in the all_cases() enumeration and setting bit n-1-i. "
    "inst['truth'] and local_search.build_masks — the corpus label list and the "
    "corpus convention, case idxs[k] at bit k — are used for NOTHING here "
    "except the parity gate's own train/test scores, which are the record's own "
    "surfaces and are compared only against themselves. arrivals(c) is READ "
    "from order_metrics_corpus.json rather than recomputed, so no corpus mask "
    "is ever built in this file and the two conventions never meet.")

STOPPING_CONDITION = (
    "The stopping condition for this thread. If C-a, C-b and C-c all hold, the "
    "audit thread closes and the next entries go back to the domain. Any other "
    "outcome — a refutation, or a row landing between its band and its "
    "refutation line — permits one successor entry and no more, and that "
    "successor carries no stopping condition of its own because this one is it.")

STOPPING_NOTE = (
    "quoted from IDEAS.md verbatim, beside the three verdicts that activate it. "
    "This record does not apply it and takes no decision from it: what follows "
    "from it is Sergi's to decide.")


# ---------------------------------------------------------------------------
# The corpus as a mask over the space
# ---------------------------------------------------------------------------

def touched_mask(corpus, space=None):
    """
    (mask, census). The points of the exhaustive space the corpus draws land on,
    in `Space`'s bit convention, WITHOUT multiplicity.

    A `Case` is mapped by `key()` — the tuple over `ATTRIBUTES` — against the
    `all_cases()` enumeration `Space` itself was built from, so bit n-1-i of the
    mask is the same case as bit n-1-i of every space mask in this repository.
    A corpus case outside the enumeration would be a broken domain and raises
    rather than being dropped silently.

    The census is the multiplicity information, which is the OTHER half of the
    decomposition and is reported for context: this mask deliberately forgets it.
    """
    space = Space() if space is None else space
    indice = {c.key(): i for i, c in enumerate(all_cases())}
    faltan = [k for k in {c.key() for c in corpus} if k not in indice]
    if faltan:
        raise ValueError(f"{len(faltan)} corpus cases are not in the case space")
    golpes = Counter(indice[c.key()] for c in corpus)
    m = 0
    for i in golpes:
        m |= 1 << (space.n - 1 - i)
    reparto = Counter(golpes.values())
    return m, {
        "n_corpus_draws": len(corpus),
        "n_distinct_points": len(golpes),
        "n_space": space.n,
        "fraction_of_space": round(len(golpes) / space.n, 6),
        "max_draws_on_one_point": max(golpes.values()),
        "mean_draws_per_touched_point": round(len(corpus) / len(golpes), 4),
        "points_by_multiplicity": {str(k): reparto[k]
                                   for k in sorted(reparto)},
    }


def restrict(truth, mask):
    """{class: its cases among the touched points}. The only thing that changes
    between `all(c)` and `touched(c)`."""
    return {c: m & mask for c, m in truth.items()}


def partitions(masks, full):
    """Pairwise disjoint, union exactly `full`, bit counts summing to its size."""
    union = 0
    total = 0
    for m in masks.values():
        if union & m:
            return False
        union |= m
        total += m.bit_count()
    return union == full and total == full.bit_count()


# ---------------------------------------------------------------------------
# The gates that are this question's own
# ---------------------------------------------------------------------------

def gate_published_rates(medido, publicado):
    """The eight `all(c)` and the overall rate, against `order_metrics.json`.

    Read from the file, never from a constant here: a gate carrying its own
    expectation is not a gate.
    """
    filas = {}
    for c, v in sorted(publicado["by_class"].items()):
        mio = medido["by_class"].get(c)
        filas[c] = {
            "recomputed": mio and mio["rate"], "published": v["rate"],
            "n_recomputed": mio and mio["n_per_pair"],
            "n_published": v["n_per_pair"],
            "reproduces": bool(mio) and mio["rate"] == v["rate"]
                          and mio["n_per_pair"] == v["n_per_pair"],
        }
    return {
        "what": "the published per-class rates over the whole space, from the "
                "regenerated orders. Parity compares four scores per row; this "
                "compares the per-class behaviour the question is about.",
        "source": f"{SPACE_RECORD}::per_class.pooled_split0_65",
        "overall": {"recomputed": medido["overall_rate"],
                    "published": publicado["overall_rate"],
                    "reproduces":
                        medido["overall_rate"] == publicado["overall_rate"]},
        "n_pairs": {"recomputed": medido["n_pairs"],
                    "published": publicado["n_pairs"]},
        "by_class": filas,
        "passes": all(f["reproduces"] for f in filas.values())
                  and medido["overall_rate"] == publicado["overall_rate"]
                  and medido["n_pairs"] == publicado["n_pairs"],
    }


def gate_matrix(pares, publicados):
    """All 2,080 per-pair distances against the published matrix, keyed by
    `(i, j)` and never by position."""
    mio = {(p["i"], p["j"]): p for p in pares}
    pub = {(p["i"], p["j"]): p for p in publicados}
    difieren = [list(k) for k in sorted(set(mio) | set(pub))
                if k not in mio or k not in pub
                or mio[k]["disagree"] != pub[k]["disagree"]
                or mio[k]["rate"] != pub[k]["rate"]]
    return {
        "what": "the 2,080 per-pair space distances, so that the per-pair half "
                "of C-d is a re-weighting of the published matrix and not a "
                "second one",
        "source": f"{SPACE_RECORD}::pairs_{SET}",
        "n_recomputed": len(mio), "n_published": len(pub),
        "key_sets_identical": set(mio) == set(pub),
        "pairs_that_differ": difieren[:20],
        "n_pairs_that_differ": len(difieren),
        "passes": not difieren and len(mio) == N_PAIRS,
    }


def gate_mask(censo, truth_space, truth_touched, touched, sfull):
    """The mask itself: its size, and that the class masks partition both the
    space and it."""
    return {
        "what": "the touched mask and the class masks over it",
        "n_bits": touched.bit_count(),
        "published_n_bits": TOUCHED_PUBLISHED,
        "published_source": "FINDINGS_ORDERS.md, part two, S-e: 'the 2000 draws "
                            "touch 1,743 distinct cases'",
        "bits_match_published": touched.bit_count() == TOUCHED_PUBLISHED,
        "census": censo,
        "class_masks_partition_the_space": partitions(truth_space, sfull),
        "class_masks_partition_the_touched_mask": partitions(truth_touched,
                                                             touched),
        "touched_is_inside_the_space": touched & ~sfull == 0,
        "passes": (touched.bit_count() == TOUCHED_PUBLISHED
                   and partitions(truth_space, sfull)
                   and partitions(truth_touched, touched)
                   and touched & ~sfull == 0),
    }


# ---------------------------------------------------------------------------
# The per-pair half, which is C-d
# ---------------------------------------------------------------------------

def per_pair_rates(dec, pares, sfull, touched, n_touched):
    """
    Each pair's disagreement restricted to the touched points, beside its rate
    over the whole space.

    The touched rate divides by 1,743 and the space rate by 134,400, which is
    the same normalization `all` and `touched` use: each is a rate over the
    surface it is measured on.
    """
    fuera = []
    for p in pares:
        _ag, dis, _un = agreement_masks(dec[p["i"]][0], dec[p["j"]][0], sfull)
        t = (dis & touched).bit_count()
        fuera.append({
            "i": p["i"], "j": p["j"],
            "disagree_touched": t,
            "rate_touched": round(t / n_touched, 6),
            "disagree_space": p["disagree"],
            "rate_space": p["rate"],
        })
    return fuera


def ratio_summary(pares, num, den):
    """`resumen()` over a per-pair ratio, with the quantile quotient R-c
    reports. The same `resumen` — quantile by index, not interpolated — that
    produced the 1.880 this is compared against."""
    r = [p[num] / p[den] for p in pares if p[den]]
    res = resumen(r)
    return {
        "n": len(r), "n_dropped_zero_denominator": len(pares) - len(r),
        "resumen": res,
        "p75_over_p25": round(res["p75"] / res["p25"], 6) if res["p25"] else None,
        "max_over_min": round(res["max"] / res["min"], 6) if res["min"] else None,
    }


# ---------------------------------------------------------------------------
# C-a to C-d, adjudicated exactly as they are written
# ---------------------------------------------------------------------------
#
# NOT re-specified, before or after seeing a number. C-d is REPORTED and carries
# no verdict, as its own row says.

def signo(x):
    return 0 if x == 0 else (1 if x > 0 else -1)


def adjudicate(tasas, p_corpus, razones):
    q = {}

    # ---- C-a: the fraction of T2_TECHNICAL's fall carried by WHICH points
    def f_de(c):
        t = tasas[c]
        den = t["all"] - t["arrivals"]
        return None if den == 0 else round((t["all"] - t["touched"]) / den, 6)

    efes = {c: f_de(c) for c in sorted(tasas)}
    f = efes[CLASE_C_A]

    def v_a(x):
        if x is None:
            return None
        if x < 0.40 or x > 1.10:
            return "REFUTED"
        return "HOLDS" if 0.60 <= x <= 0.95 else "NEITHER"

    q["C-a"] = {
        "claim": "write f(c) = (all - touched) / (all - arrivals): the fraction "
                 "of a class's fall carried by WHICH points arrive rather than "
                 "HOW OFTEN. f(T2_TECHNICAL) lands between 0.60 and 0.95. "
                 "Refuted below 0.40 or above 1.10. Nothing forces touched to "
                 "sit between the other two, so f outside [0, 1] is possible "
                 "and is a result, not an error.",
        "class": CLASE_C_A,
        "band": [0.60, 0.95], "refuted_outside": [0.40, 1.10],
        "f": f,
        "components": tasas[CLASE_C_A],
        "f_by_class": efes,
        "f_outside_unit_interval": {c: v for c, v in efes.items()
                                    if v is not None and not 0.0 <= v <= 1.0},
        "verdict": v_a(f),
    }

    # ---- C-b: the mechanism is general, not a fact about one class
    filas_b = {}
    for c in sorted(tasas):
        t = tasas[c]
        s_t, s_a = signo(t["touched"] - t["all"]), signo(t["arrivals"] - t["all"])
        filas_b[c] = {
            "touched_minus_all": round(t["touched"] - t["all"], 6),
            "arrivals_minus_all": round(t["arrivals"] - t["all"], 6),
            "sign_touched": s_t, "sign_arrivals": s_a,
            "signs_match": s_t == s_a,
        }
    n_match = sum(1 for v in filas_b.values() if v["signs_match"])

    q["C-b"] = {
        "claim": "the sign of touched(c) - all(c) matches the sign of "
                 "arrivals(c) - all(c) in at least 6 of the 8 classes. Refuted "
                 "at 4 or fewer. This is the row that keeps C-a from being a "
                 "tautology: BILLING_SPECIALIST at 2.652 and "
                 "SELF_SERVICE_DEFLECT at 1.103 must go UP, not down, or the "
                 "story is not about which points arrive at all.",
        "threshold": 6, "refuted_at_or_below": 4,
        "n_classes": len(filas_b), "n_matching": n_match,
        "by_class": filas_b,
        "the_two_classes_the_row_names": {
            c: filas_b[c] for c in ("BILLING_SPECIALIST", "SELF_SERVICE_DEFLECT")
            if c in filas_b},
        "verdict": ("HOLDS" if n_match >= 6
                    else "REFUTED" if n_match <= 4 else "NEITHER"),
    }

    # ---- C-c: the reconstruction
    valor = round(sum(p_corpus[c] * tasas[c]["touched"] for c in tasas), 6)
    original = round(sum(p_corpus[c] * tasas[c]["all"] for c in tasas), 6)
    medido_corpus = round(sum(p_corpus[c] * tasas[c]["arrivals"] for c in tasas), 6)

    def v_c(x):
        if x < 0.035 or x > 0.090:
            return "REFUTED"
        return "HOLDS" if 0.043 <= x <= 0.072 else "NEITHER"

    q["C-c"] = {
        "claim": "reweighting rebuilt with touched(c) in place of all(c) — "
                 "sum of p_corpus(c) x touched(c) — lands between 0.043 and "
                 "0.072, within +/-25% of the measured 0.0575, against the "
                 "0.1167 the original reweighting gave. Refuted outside "
                 "0.035-0.090.",
        "band": [0.043, 0.072], "refuted_outside": [0.035, 0.090],
        "value": valor,
        "original_reweighting_recomputed": original,
        "original_reweighting_published": 0.116685,
        "corpus_pooled_rate_published": 0.057472,
        "reweighting_of_arrivals_as_a_check": medido_corpus,
        "reweighting_of_arrivals_note":
            "the same weights applied to arrivals(c) must give back the pooled "
            "corpus rate up to rounding, because the corpus class sizes ARE the "
            "denominators arrivals(c) pools over. It is an identity, not a "
            "finding, and it is here so that the weights can be seen to be the "
            "right ones.",
        "weights": {c: round(p_corpus[c], 6) for c in sorted(p_corpus)},
        "verdict": v_c(valor),
    }

    # ---- C-d: reported, not adjudicated
    q["C-d"] = {
        "claim": "reported, not adjudicated: the per-pair ratio recomputed on "
                 "touched points, and whether its p75/p25 of 1.880 shrinks. If "
                 "the same explanation covers the spread, R-c's other half "
                 "closes too; if not, the spread is a separate fact and stays "
                 "open. One measurement either way, and no threshold on it.",
        "adjudicates": False,
        "r_c_published_p75_over_p25": 1.880,
        "ratios": razones,
        "note":
            "three ratios, because the decomposition has two steps and R-c "
            "measured the composition of both. touched/space is the WHICH "
            "POINTS step, arrivals/space is R-c's own quantity reproduced from "
            "the published matrices, and arrivals/touched is the HOW OFTEN "
            "step. No threshold is applied to any of them.",
    }
    return q


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    solo_checks = "--checks" in argv
    t_start = time.time()

    print("=" * 78)
    print("C-a..C-d — WHICH POINTS ARRIVE, OR HOW OFTEN")
    print("=" * 78)
    print(f"  optimizer: {DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} declared starts + the greedy (untouched)")
    print(f"  set {SET} · {N_PAIRS} pairs · pool {POOL} · no new search, "
          f"no API calls")
    print(f"  {describe()}")

    inst = build_instance()
    _sM, _sW, sfull, sn = inst["space"]
    print(f"  instance ready in {inst['seconds_setup']}s: "
          f"{len(inst['ids'])} rules, {len(inst['corpus'])} corpus cases, "
          f"{sn:,} space cases")

    espacio = json.loads((OUT / SPACE_RECORD).read_text())
    corpus_rec = json.loads((OUT / CORPUS_RECORD).read_text())

    # ------------------------------------------------------------- the mask
    t0 = time.time()
    touched, censo = touched_mask(inst["corpus"])
    truth_space = inst["truth_space"]
    truth_touched = restrict(truth_space, touched)
    n_touched = touched.bit_count()
    g_mask = gate_mask(censo, truth_space, truth_touched, touched, sfull)
    print()
    print("MASK GATE — the points the corpus touches")
    print(f"  {censo['n_corpus_draws']:,} draws land on {n_touched:,} distinct "
          f"points of {sn:,} ({100 * censo['fraction_of_space']:.2f}%), "
          f"published {TOUCHED_PUBLISHED:,}"
          f"{'  ok' if g_mask['bits_match_published'] else '  NO'}")
    print(f"  class masks partition the space "
          f"{g_mask['class_masks_partition_the_space']}, and the touched mask "
          f"{g_mask['class_masks_partition_the_touched_mask']} "
          f"({time.time() - t0:.0f}s)")
    if not g_mask["passes"]:
        print("  STOP: the mask is not the one the record publishes, or the "
              "class masks do not partition. Nothing below would be about the "
              "right points.")
        return 1

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

    # ------------------------------------------------- the 65 orders of split 0
    s0 = SPLITS_FULL[0]
    t0 = time.time()
    orders = [r["order"] for r in runs[s0]["stats"]["rows"][:N_ORDERS]]
    dec, dig = decisions_and_signatures(inst, orders)
    pares = pairwise(inst, orders, dec, with_taus=False)
    print(f"\n  split {s0}: {len(pares):,} pairs of {N_ORDERS} end orders over "
          f"the space in {time.time() - t0:.0f}s")

    g_matrix = gate_matrix(pares, espacio[f"pairs_{SET}"])
    print()
    print("MATRIX GATE — the 2,080 per-pair distances against "
          f"{SPACE_RECORD}")
    print(f"  {g_matrix['n_recomputed']:,} recomputed against "
          f"{g_matrix['n_published']:,} published, key sets identical "
          f"{g_matrix['key_sets_identical']}, "
          f"{g_matrix['n_pairs_that_differ']} differ"
          f"{'  ok' if g_matrix['passes'] else '  NO'}")
    if not g_matrix["passes"]:
        print("  STOP: the regenerated pairs are not the published ones.")
        return 1

    # ------------------------------------------------- all(c) and touched(c)
    t0 = time.time()
    pooled_all = per_class_over_pairs(inst, dec, pares)
    g_rates = gate_published_rates(
        pooled_all, espacio["per_class"]["pooled_split0_65"])
    print()
    print(f"RATE GATE — the eight published all(c) against {SPACE_RECORD}")
    for c, f in g_rates["by_class"].items():
        print(f"  {c:<22}{f['recomputed']:>10}  published {f['published']:>10}"
              f"{'  ok' if f['reproduces'] else '  NO'}")
    print(f"  {'overall':<22}{g_rates['overall']['recomputed']:>10}  published "
          f"{g_rates['overall']['published']:>10}"
          f"{'  ok' if g_rates['overall']['reproduces'] else '  NO'}"
          f"   ({time.time() - t0:.0f}s)")
    if not g_rates["passes"]:
        print("  STOP: the published per-class rates do not reproduce.")
        return 1
    if solo_checks:
        print(f"\n  ALL FOUR GATES PASS. total cost: {time.time() - t_start:.0f}s")
        return 0

    t0 = time.time()
    pooled_touched = per_class_over_pairs(
        dict(inst, truth_space=truth_touched), dec, pares)
    print(f"\n  touched(c) over the same {len(pares):,} pairs in "
          f"{time.time() - t0:.0f}s")

    # arrivals(c): READ, not recomputed. See TRUTH_PROVENANCE.
    llegadas = corpus_rec["per_class"]["corpus_full"]["pooled_split0_65"]
    tam_corpus = corpus_rec["per_class"]["corpus_full"]["class_sizes"]
    n_corpus = corpus_rec["n_corpus"]

    tasas = {}
    for c in sorted(truth_space):
        tasas[c] = {
            "all": pooled_all["by_class"][c]["rate"],
            "touched": pooled_touched["by_class"][c]["rate"],
            "arrivals": llegadas["by_class"][c]["rate"],
            "n_all": pooled_all["by_class"][c]["n_per_pair"],
            "n_touched": pooled_touched["by_class"][c]["n_per_pair"],
            "n_arrivals": llegadas["by_class"][c]["n_per_pair"],
        }
    p_corpus = {c: tam_corpus[c] / n_corpus for c in tasas}

    # ------------------------------------------------------------------- C-d
    t0 = time.time()
    por_par = per_pair_rates(dec, pares, sfull, touched, n_touched)
    pub_corpus = {(p["i"], p["j"]): p["rate"]
                  for p in corpus_rec[f"pairs_{SET}_corpus_full"]}
    for p in por_par:
        p["rate_arrivals"] = pub_corpus[(p["i"], p["j"])]
    razones = {
        "touched_over_space": ratio_summary(por_par, "rate_touched",
                                            "rate_space"),
        "arrivals_over_space": ratio_summary(por_par, "rate_arrivals",
                                             "rate_space"),
        "arrivals_over_touched": ratio_summary(por_par, "rate_arrivals",
                                               "rate_touched"),
    }
    razones["arrivals_over_space"]["note"] = (
        "R-c's own quantity, reproduced here from the two published matrices "
        "joined on (i, j). It must give back 1.880; it is the check that this "
        "file's ratio instrument is the one that produced that figure.")
    print(f"  the three per-pair ratios in {time.time() - t0:.0f}s")

    # ------------------------------------------------------- the pooled context
    dis_touched = sum(p["disagree_touched"] for p in por_par)
    contexto = {
        "labels": f"split {s0}, fraction 1.0, {N_ORDERS} starts, the "
                  f"{n_touched} touched points of the space",
        "n_orders": N_ORDERS, "n_pairs": len(por_par),
        "n_distinct_signatures_over_the_space": len(set(dig)),
        "pooled_rate_over_touched_points": round(
            dis_touched / (len(por_par) * n_touched), 6),
        "disagreement_touched": resumen([p["disagree_touched"]
                                         for p in por_par]),
        "disagreement_rate_touched": resumen([p["rate_touched"]
                                              for p in por_par]),
        "pairs_identical_on_the_touched_points": sum(
            1 for p in por_par if p["disagree_touched"] == 0),
        "note":
            "the pooled rate here is UNWEIGHTED over the 1,743 touched points "
            "and is not any of the three per-class rates reweighted: it is what "
            "the overall figure would be if every touched point counted once. "
            "It adjudicates nothing. `pairs_identical_on_the_touched_points` is "
            "S-e's question asked of this surface — the corpus answered zero.",
    }

    q = adjudicate(tasas, p_corpus, razones)

    print()
    print("=" * 78)
    print("THE THREE RATES, BY CLASS")
    print("=" * 78)
    print(f"  {'class':<22}{'all(c)':>10}{'touched(c)':>12}{'arrivals(c)':>13}"
          f"{'f(c)':>9}{'signs':>8}")
    for c in sorted(tasas):
        t = tasas[c]
        f_c = q["C-a"]["f_by_class"][c]
        ok = "match" if q["C-b"]["by_class"][c]["signs_match"] else "-"
        print(f"  {c:<22}{t['all']:>10.4f}{t['touched']:>12.4f}"
              f"{t['arrivals']:>13.4f}"
              f"{(f'{f_c:.3f}' if f_c is not None else 'n/a'):>9}{ok:>8}")

    print()
    print("=" * 78)
    print("C-a..C-d, AS WRITTEN")
    print("=" * 78)
    print(f"  C-a  f({CLASE_C_A}) = {q['C-a']['f']}   band [0.60, 0.95]   "
          f"{q['C-a']['verdict']}")
    print(f"  C-b  signs match in {q['C-b']['n_matching']} of "
          f"{q['C-b']['n_classes']}   at least 6   {q['C-b']['verdict']}")
    print(f"  C-c  reweighting on touched = {q['C-c']['value']}   "
          f"band [0.043, 0.072]   {q['C-c']['verdict']}")
    print(f"  C-d  reported: p75/p25 touched/space "
          f"{razones['touched_over_space']['p75_over_p25']}, "
          f"arrivals/space {razones['arrivals_over_space']['p75_over_p25']}, "
          f"arrivals/touched "
          f"{razones['arrivals_over_touched']['p75_over_p25']}")

    # ------------------------------------------------------------- the record
    payload = {
        "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            budgets=list(BUDGETS), set_measured=SET,
                            n_pairs=N_PAIRS, n_orders=N_ORDERS),
        "what":
            "C-a to C-d of IDEAS.md, adjudicated. The same 65 end orders of "
            "split 0 and the same 2,080 pairs as order_metrics.json and "
            "order_metrics_corpus.json, measured over the EXHAUSTIVE SPACE "
            "RESTRICTED TO THE POINTS THE CORPUS TOUCHES. It splits each "
            "class's fall from all(c) to arrivals(c) into two steps — WHICH "
            "points the corpus reaches and HOW OFTEN it reaches each — of which "
            "only the first was unmeasured. The corpus contributes a mask and "
            "nothing else, so every figure stays in Space's bit convention and "
            "no mask is joined across the two conventions. No new search: the "
            "orders come out of run_full_supervision and run_band_1pct of "
            "order_metrics_run.py, imported and called unchanged, and the "
            "31-row parity gate is what says they are the published ones. "
            "Neither record it reads is rewritten. Zero API calls.",
        "prediction":
            "IDEAS.md, the entry 'The whole 2.03x gap is one class, and the "
            "question is why its arrivals are cleaner', drafted and committed "
            "before touched(c) existed for any class",
        "surface": SURFACE,
        "surface_note":
            "three surfaces, all named: all(c) is over the 134,400 points of "
            "the exhaustive space; touched(c) is over the 1,743 of them the "
            "corpus reaches, each counted once; arrivals(c) is over the 2,000 "
            "draws with multiplicity and is READ from order_metrics_corpus.json "
            "rather than recomputed. The train, test and space figures of the "
            "parity gate are the surfaces of the records being reproduced.",
        "pool": POOL,
        "n_rules": len(inst["ids"]),
        "n_space": sn,
        "n_touched": n_touched,
        "n_corpus": len(inst["corpus"]),
        "splits": list(SPLITS_FULL),
        "budgets": list(BUDGETS),
        "touched_census": censo,
        "gates": {
            "mask": g_mask,
            "parity_rows": n_filas,
            "parity_full_supervision": par_a,
            "parity_band_1pct": par_b,
            "matrix": g_matrix,
            "published_rates": g_rates,
        },
        "no_new_search":
            "every order measured here comes out of run_full_supervision and "
            "run_band_1pct of order_metrics_run.py, imported and called "
            "unchanged. The prefix shortcut is not revalidated: it was checked "
            "against an independent 65-start run when it was introduced, and "
            "tests/test_order_metrics_run.py pins the tie-break it rests on. "
            "MULTISTART_SEED, MULTISTART_STARTS and DECLARED_NEIGHBOURHOOD are "
            "untouched and no figure here is an argument about any of them.",
        "rates_by_class": tasas,
        "pooled_all": pooled_all,
        "pooled_touched": pooled_touched,
        "pooled_arrivals_read_from_the_corpus_record": llegadas,
        "corpus_class_sizes": tam_corpus,
        "set_summary_over_the_space_published": espacio["sets"][SET],
        "set_summary_over_the_touched_points": contexto,
        "pairs_split0_starts65_touched": por_par,
        "pairs_stored":
            "the full 2,080-row triangle, each row carrying its distance over "
            "the space, over the touched points, and its published rate over "
            "arrivals, so that C-d can be recomputed from this file alone.",
        "predictions": q,
        "truth_provenance": TRUTH_PROVENANCE,
        "stopping_condition": STOPPING_CONDITION,
        "stopping_condition_note": STOPPING_NOTE,
        "seconds": {
            "setup": inst["seconds_setup"],
            "search_full_supervision": {s: runs[s]["seconds"]
                                        for s in SPLITS_FULL},
            "search_band_1pct": round(sum(f["seconds"] for f in band), 1),
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
