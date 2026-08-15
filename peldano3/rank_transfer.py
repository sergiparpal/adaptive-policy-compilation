"""
DOES THE SPACE *RANK* TWO ORDERS WHEN IT CANNOT *RATE* THEM?

--------------------------------------------------------------------------
WHAT THIS IS
--------------------------------------------------------------------------
`results3/order_metrics.json` and `results3/order_metrics_corpus.json` measure
the same 2,080 pairs of the same 65 end orders on two surfaces. The corpus part
settled that the LEVEL does not transfer (5.75% against 20.35%) and that WHERE
the disagreement falls does not transfer either (S-c refuted). Neither says
whether the ORDERING of the pairs survives, and neither implies it: a rank is
invariant to any monotone transformation, so a level that falls by 3.5x is
compatible with an ordering preserved exactly.

That is what `IDEAS.md` predicts as R-a to R-d, drafted, signed and committed
before any of these figures existed, and this is the run that adjudicates it.

--------------------------------------------------------------------------
IT IS A JOIN, NOT A RUN
--------------------------------------------------------------------------
No search, no regeneration, no new instrument, no API call, and nothing here
touches an order: the two records already hold every distance this needs. Both
are opened READ ONLY and neither is rewritten. If anything in this file ever
calls `multistart`, it has stopped being what it says it is.

The three matrices, 2,080 rows each over the same 65 end orders of split 0:

    order_metrics.json        :: pairs_split0_starts65            (the space)
    order_metrics_corpus.json :: pairs_split0_starts65_corpus_full
    order_metrics_corpus.json :: pairs_split0_starts65_corpus_test

They are joined on `(i, j)` and NEVER on position in the list. Position would
work today and would break silently the day a matrix is written in another
order, and the failure would look like a finding.

--------------------------------------------------------------------------
THE TWO FUNCTIONS THAT ARE IMPORTED AND NOT REWRITTEN
--------------------------------------------------------------------------
`order_metrics_run.spearman` — average ranks for ties, and it is the function
that produced Q-d's number. Writing another would change instrument halfway
through a record.

`order_metrics_run.resumen` — quantile BY INDEX, `v[len(v) // 4]`, not an
interpolated percentile. The gate below compares against summaries that
function produced; an interpolating percentile would never reproduce them.

Importing them pulls `order_metrics_run`'s own imports in behind them, the
search modules included. Nothing here calls into any of it, and importing costs
what it costs to define functions — but it is worth saying out loud, because
"no search" is a claim about what runs and not about what the import graph
happens to reach.

--------------------------------------------------------------------------
THE GATE, WHICH IS THIS QUESTION'S PARITY GATE
--------------------------------------------------------------------------
Blocking, and it is what makes the join about the right rows:

  a. the three `(i, j)` key sets are identical, 2,080 keys, no duplicates,
     indices in 0..64;
  b. `resumen()` over each matrix's own stored rates reproduces EXACTLY the
     summary that matrix's own record already publishes for the set.

It was first run on 2026-08-15 BEFORE the prediction was committed, and that
does not contaminate anything: it reproduces summaries already published and
computes no quantity R-a to R-d adjudicates on — no Spearman, no decile overlap,
no ratio quantile, no argmin. It is re-run here, and the record carries the
result of THIS run.

Usage:  python3 -m peldano3.rank_transfer
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from harness.provenance import describe, environment
from peldano3.order_metrics_run import resumen, spearman

OUT = Path("results3")
RECORD = "rank_transfer.json"
SPACE_RECORD = "order_metrics.json"
CORPUS_RECORD = "order_metrics_corpus.json"

SET = "split0_starts65"
N_ORDERS = 65
N_PAIRS = N_ORDERS * (N_ORDERS - 1) // 2          # 2,080
DECILE = N_PAIRS // 10                            # 208, exactly a tenth

SURFACES = ("space", "corpus_full", "corpus_test")
ADJUDICATES = "corpus_full"

# Already published, quoted here as the yardsticks the entry names rather than
# recomputed: the pooled rates of this very set on the two surfaces, and what
# the class-reweighting model predicted for their quotient.
POOLED = {"space": 0.203451, "corpus_full": 0.057472}
REWEIGHTING_MODEL = 0.116685


# ---------------------------------------------------------------------------
# Reading the two records
# ---------------------------------------------------------------------------

def load():
    """The three matrices and the three summaries they must reproduce. Read
    only: neither record is opened for writing anywhere in this module."""
    esp = json.loads((OUT / SPACE_RECORD).read_text())
    cor = json.loads((OUT / CORPUS_RECORD).read_text())
    return {
        "space": {
            "rows": esp[f"pairs_{SET}"],
            "published": esp["sets"][SET]["disagreement_rate"],
            "from": f"{SPACE_RECORD}::pairs_{SET}",
            "n_surface": esp["n_space"],
        },
        "corpus_full": {
            "rows": cor[f"pairs_{SET}_corpus_full"],
            "published": cor["sets"]["corpus_full"][SET]["disagreement_rate"],
            "from": f"{CORPUS_RECORD}::pairs_{SET}_corpus_full",
            "n_surface": cor["n_corpus"],
        },
        "corpus_test": {
            "rows": cor[f"pairs_{SET}_corpus_test"],
            "published": cor["sets"]["corpus_test"][SET]["disagreement_rate"],
            "from": f"{CORPUS_RECORD}::pairs_{SET}_corpus_test",
            "n_surface": cor["surfaces"]["corpus_test"]["n"]["0"],
        },
    }


def keyed(rows):
    """{(i, j): rate}. The join key, and the only one used."""
    return {(r["i"], r["j"]): r["rate"] for r in rows}


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def gate(mats):
    """Blocking. Returns the report and whether it passes."""
    claves, filas = {}, {}
    for s in SURFACES:
        rows = mats[s]["rows"]
        k = [(r["i"], r["j"]) for r in rows]
        idx = {x for p in k for x in p}
        claves[s] = set(k)
        filas[s] = {
            "source": mats[s]["from"],
            "rows": len(rows),
            "distinct_keys": len(claves[s]),
            "duplicates": len(k) - len(claves[s]),
            "index_min": min(idx), "index_max": max(idx),
            "i_lt_j_always": all(a < b for a, b in k),
            "n_is_65_choose_2": len(claves[s]) == N_PAIRS,
        }
    identicas = claves["space"] == claves["corpus_full"] == claves["corpus_test"]

    resumenes = {}
    for s in SURFACES:
        mio = resumen([round(r["rate"], 6) for r in mats[s]["rows"]])
        pub = mats[s]["published"]
        resumenes[s] = {
            "recomputed": mio, "published": pub, "reproduces": mio == pub,
            "differs_in": [f for f in sorted(set(mio) | set(pub))
                           if mio.get(f) != pub.get(f)],
        }

    pasa = (identicas
            and all(f["duplicates"] == 0 and f["i_lt_j_always"]
                    and f["n_is_65_choose_2"] and f["index_min"] == 0
                    and f["index_max"] == N_ORDERS - 1 for f in filas.values())
            and all(r["reproduces"] for r in resumenes.values()))
    return {
        "what": "this question's parity gate: the three matrices are the same "
                "2,080 pairs, and each reproduces the summary its own record "
                "publishes for the set",
        "key_sets": filas,
        "key_sets_identical": identicas,
        "summaries": resumenes,
        "first_verified": "2026-08-15, before the prediction was committed. It "
                          "reproduces already-published summaries and computes "
                          "no quantity R-a..R-d adjudicates on, so it could not "
                          "carry information about an answer; this record "
                          "carries the result of the run that produced the "
                          "figures below.",
        "passes": pasa,
    }


# ---------------------------------------------------------------------------
# Ties, which is what a rank statistic can be capped by
# ---------------------------------------------------------------------------

def tie_profile(valores):
    """How much of the ordering is decided by nothing: distinct values, the
    largest group sharing one, and the mean group size."""
    c = Counter(valores)
    return {"n": len(valores), "distinct_values": len(c),
            "largest_tie_group": max(c.values()),
            "mean_group_size": round(len(valores) / len(c), 4),
            "values_appearing_once": sum(1 for v in c.values() if v == 1)}


def tie_ceiling(a, b):
    """
    The largest Spearman these two tie structures allow, and the attenuation
    that follows from it.

    Sorting both and pairing k-th smallest with k-th smallest is the comonotone
    coupling: no arrangement of the same two multisets correlates higher. So the
    ceiling is what a perfect monotone relation would score GIVEN the ties, and
    1 - ceiling is the correction the entry says it checked and found
    negligible. Computed with the same `spearman`, not with a formula written
    for the occasion.

    THE RESOLUTION IS THE INSTRUMENT'S. `spearman` rounds to four decimals, so a
    ceiling that comes back 1.0 means >= 0.99995 and an attenuation below 5e-5,
    not zero. That is reported as the bound it is. Resolving it finer would take
    a second rank correlation, which is exactly the instrument change this
    record declines to make halfway through — and it is unnecessary: the bound
    is already three orders of magnitude away from anything that could move a
    verdict.
    """
    techo = spearman(sorted(a), sorted(b))
    if techo is None:
        return {"max_attainable_spearman": None}
    return {
        "max_attainable_spearman": techo,
        "attenuation_upper_bound": round(1 - techo + 5e-5, 8),
        "resolution_note": "spearman rounds to 4 dp; 1.0 means >= 0.99995, so "
                           "the bound carries that half-ulp rather than "
                           "claiming an exact zero",
    }


# ---------------------------------------------------------------------------
# R-b's decile, and how much of it the tie-break decides
# ---------------------------------------------------------------------------

def closest(rates, k):
    """
    The k pairs of lowest rate, ties broken by `(i, j)` ascending as declared.

    The boundary matters as much as the set: if many pairs share the k-th value,
    which of them got in was decided by the tie-break and not by the
    measurement. `core` is the unambiguous part — everything strictly below the
    boundary — and `boundary_*` says how wide the arbitrary band is.
    """
    orden = sorted(rates, key=lambda kk: (rates[kk], kk))
    dentro = orden[:k]
    frontera = rates[dentro[-1]]
    en_frontera = [kk for kk in rates if rates[kk] == frontera]
    nucleo = {kk for kk in rates if rates[kk] < frontera}
    return {
        "set": set(dentro),
        "core": nucleo,
        "boundary_rate": frontera,
        "boundary_ties_total": len(en_frontera),
        "boundary_ties_inside": sum(1 for kk in dentro
                                    if rates[kk] == frontera),
        "core_size": len(nucleo),
        "decided_by_tie_break": len(en_frontera) - sum(
            1 for kk in dentro if rates[kk] == frontera) > 0,
    }


# ---------------------------------------------------------------------------
# R-d, and the draw-noise arithmetic the entry reasons from
# ---------------------------------------------------------------------------

def veredicto_b_pura(x):
    """R-b's rule, as written, kept in one place so the verdict and the
    tie-break sensitivity around it cannot come from two readings of it."""
    if x < 0.20 or x > 0.80:
        return "REFUTED"
    return "HOLDS" if 0.35 <= x <= 0.70 else "NEITHER"


def rank_of(clave, rates):
    """1-based position under the declared order, plus the tie-robust reading:
    how many pairs are strictly below it."""
    orden = sorted(rates, key=lambda kk: (rates[kk], kk))
    return {"rank": orden.index(clave) + 1,
            "n_strictly_below": sum(1 for v in rates.values()
                                    if v < rates[clave]),
            "n_sharing_its_rate": sum(1 for v in rates.values()
                                      if v == rates[clave])}


def extremes(keys, rates, otra, nombre_otra):
    """Every pair attaining the minimum here, and where each ranks there."""
    minimo = min(rates[k] for k in keys)
    fuera = []
    for k in sorted(keys, key=lambda kk: (rates[kk], kk)):
        if rates[k] != minimo:
            break
        fuera.append({
            "pair": list(k), "rate_here": rates[k],
            f"rate_on_{nombre_otra}": otra[k],
            "rank_here": rank_of(k, rates),
            f"rank_on_{nombre_otra}": rank_of(k, otra),
        })
    return {"minimum_rate": minimo, "n_pairs_attaining": len(fuera),
            "pairs": fuera}


def draw_noise(p, n):
    """
    Relative standard deviation of a rate estimated from `n` draws at rate `p`:
    sqrt((1-p) / (n p)). It is closed form, not a measurement, and it is the
    first half of the 9%-against-42% arithmetic the entry reasons from.
    """
    return round(((1 - p) / (n * p)) ** 0.5, 6)


def spread(pub):
    """Interquartile range over the median, from a published summary. The
    second half of the same arithmetic."""
    return round((pub["p75"] - pub["p25"]) / pub["median"], 6)


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    t_start = time.time()

    print("=" * 78)
    print("R-a..R-d — DOES THE SPACE RANK WHAT IT CANNOT RATE?")
    print("=" * 78)
    print(f"  a join of two published records · set {SET} · {N_PAIRS} pairs · "
          f"{N_ORDERS} end orders")
    print("  no search, no regeneration, no new instrument, zero API calls")
    print(f"  {describe()}")

    mats = load()
    for s in SURFACES:
        print(f"  {s:<12} {mats[s]['from']}  ({mats[s]['n_surface']:,} cases)")

    # ------------------------------------------------------------------ gate
    g = gate(mats)
    print()
    print("GATE — the same 2,080 pairs, and each record's own summary")
    for s in SURFACES:
        f, r = g["key_sets"][s], g["summaries"][s]
        print(f"  {s:<12} rows {f['rows']:>5}  keys {f['distinct_keys']:>5}  "
              f"dups {f['duplicates']}  idx {f['index_min']}..{f['index_max']}  "
              f"summary {'reproduces' if r['reproduces'] else 'DOES NOT'}")
        if not r["reproduces"]:
            for campo in r["differs_in"]:
                print(f"      {campo}: recomputed "
                      f"{r['recomputed'].get(campo)} vs published "
                      f"{r['published'].get(campo)}")
    print(f"  key sets identical across the three: {g['key_sets_identical']}")
    if not g["passes"]:
        print("\n  STOP: the join is not over the rows it claims to be over. "
              "Nothing below would be about them.")
        return 1
    print("\n  GATE: PASSES.")

    # --------------------------------------------------------------- the join
    tasas = {s: keyed(mats[s]["rows"]) for s in SURFACES}
    claves = sorted(tasas["space"])
    listas = {s: [tasas[s][k] for k in claves] for s in SURFACES}
    if any(v <= 0 for s in SURFACES for v in listas[s]):
        print("\n  STOP: a rate is zero or negative, and R-c divides by the "
              "space rate. The entry declares none is; that would be the "
              "finding.")
        return 1

    # ---------------------------------------------------------------- R-a
    rho = {s: spearman(listas[s], listas["space"])
           for s in ("corpus_full", "corpus_test")}
    perfiles = {s: tie_profile(listas[s]) for s in SURFACES}
    techos = {s: tie_ceiling(listas[s], listas["space"])
              for s in ("corpus_full", "corpus_test")}

    def veredicto_a(x):
        if x < 0.55 or x > 0.97:
            return "REFUTED"
        return "HOLDS" if 0.70 <= x <= 0.93 else "NEITHER"

    r_a = {
        "claim": "Spearman between the corpus-full rate and the space rate, "
                 "over the 2,080 pairs of split0_starts65, lands between 0.70 "
                 "and 0.93. Refuted below 0.55 or above 0.97.",
        "adjudicates_on": ADJUDICATES,
        "band": [0.70, 0.93], "refuted_outside": [0.55, 0.97],
        "spearman": rho,
        "verdict_by_surface": {s: veredicto_a(rho[s]) for s in rho},
        "verdict": veredicto_a(rho[ADJUDICATES]),
        "tie_diagnostics": {
            "note": "reported beside rho and adjudicating nothing. The entry "
                    "declares the drafter checked the tie load and concluded it "
                    "does not cap the band; this is that claim made checkable.",
            "profiles": perfiles,
            "ceilings": techos,
        },
    }

    # ---------------------------------------------------------------- R-b
    cercanos = {s: closest(tasas[s], DECILE) for s in SURFACES}
    solape = {}
    for s in ("corpus_full", "corpus_test"):
        comun = cercanos["space"]["set"] & cercanos[s]["set"]
        nucleo = cercanos["space"]["core"] & cercanos[s]["core"]
        # How much of the answer the tie-break decides. The space side's
        # boundary is unambiguous, so only the corpus side can vary: its core is
        # forced, and the remaining slots are filled from the pairs sharing the
        # boundary rate. Best and worst case over every way of filling them.
        frontera = {k for k, v in tasas[s].items()
                    if v == cercanos[s]["boundary_rate"]}
        huecos = DECILE - cercanos[s]["core_size"]
        en_ambos = len(cercanos["space"]["set"] & frontera)
        solape[s] = {
            "overlap": len(comun),
            "fraction": round(len(comun) / DECILE, 6),
            "core_overlap": len(nucleo),
            "core_sizes": [cercanos["space"]["core_size"],
                           cercanos[s]["core_size"]],
            "tie_break_sensitivity": {
                "slots_filled_from_the_boundary": huecos,
                "boundary_pairs_also_in_the_space_208": en_ambos,
                "overlap_min": len(nucleo) + max(
                    0, huecos - (len(frontera) - en_ambos)),
                "overlap_max": len(nucleo) + min(huecos, en_ambos),
                "space_boundary_is_unambiguous":
                    cercanos["space"]["boundary_ties_total"] == 1,
            },
        }
        sens = solape[s]["tie_break_sensitivity"]
        sens["fraction_min"] = round(sens["overlap_min"] / DECILE, 6)
        sens["fraction_max"] = round(sens["overlap_max"] / DECILE, 6)
        sens["verdict_is_robust_to_the_tie_break"] = (
            veredicto_b_pura(sens["fraction_min"])
            == veredicto_b_pura(sens["fraction_max"]))

    veredicto_b = veredicto_b_pura

    r_b = {
        "claim": "of the 208 pairs closest on the space, between 35% and 70% "
                 "are among the 208 closest on the corpus. Refuted below 20% "
                 "or above 80%.",
        "adjudicates_on": ADJUDICATES,
        "k": DECILE, "band": [0.35, 0.70], "refuted_outside": [0.20, 0.80],
        "overlap": solape,
        "boundary": {s: {k: v for k, v in cercanos[s].items()
                         if k not in ("set", "core")} for s in SURFACES},
        "tie_break": "lowest rate first, ties by (i, j) ascending, as declared "
                     "before the numbers existed",
        "verdict_by_surface": {s: veredicto_b(solape[s]["fraction"])
                               for s in solape},
        "verdict": veredicto_b(solape[ADJUDICATES]["fraction"]),
    }

    # ---------------------------------------------------------------- R-c
    razones = {}
    for s in ("corpus_full", "corpus_test"):
        r = [tasas[s][k] / tasas["space"][k] for k in claves]
        res = resumen(r)
        razones[s] = {
            "resumen": res,
            "p75_over_p25": round(res["p75"] / res["p25"], 6),
            "max_over_min": round(res["max"] / res["min"], 6),
        }

    def veredicto_c(x):
        if x < 1.15:
            return "REFUTED"
        return "HOLDS" if x > 1.30 else "NEITHER"

    r_c = {
        "claim": "the per-pair ratio corpus/space is not a common factor: its "
                 "p75 over its p25 exceeds 1.30. Refuted below 1.15.",
        "adjudicates_on": ADJUDICATES,
        "threshold": 1.30, "refuted_below": 1.15,
        "note": "the ratio is per pair, and p75 and p25 come from resumen() "
                "over the list of ratios — not from dividing one surface's p75 "
                "by the other's, which is a different quantity.",
        "ratios": razones,
        "pooled_ratio_for_context": round(POOLED["corpus_full"]
                                          / POOLED["space"], 6),
        "reweighting_model_for_context": round(REWEIGHTING_MODEL
                                               / POOLED["space"], 6),
        "verdict_by_surface": {s: veredicto_c(razones[s]["p75_over_p25"])
                               for s in razones},
        "verdict": veredicto_c(razones[ADJUDICATES]["p75_over_p25"]),
    }

    # ---------------------------------------------------------------- R-d
    r_d = {
        "claim": "reported, not adjudicated: which pair attains the space "
                 "minimum inside this set and where it ranks on the corpus, "
                 "and the converse.",
        "adjudicates": False,
        "space_minimum": extremes(claves, tasas["space"], tasas["corpus_full"],
                                  "corpus_full"),
        "corpus_full_minimum": extremes(claves, tasas["corpus_full"],
                                        tasas["space"], "space"),
        "corpus_test_minimum": extremes(claves, tasas["corpus_test"],
                                        tasas["space"], "space"),
    }

    # ------------------------------- the arithmetic the entry reasons from
    ruido = draw_noise(POOLED["corpus_full"], mats["corpus_full"]["n_surface"])
    dispersion = {s: spread(mats[s]["published"]) for s in SURFACES}
    reparto = {
        "what": "the entry argues that which particular cases were drawn "
                "contributes about 9% relative, against a spread between pairs "
                "of about 42%, so idiosyncratic draw cannot be what lowers the "
                "correlation. Both halves are checked here.",
        "draw_noise_relative_sd": ruido,
        "draw_noise_is": "closed form, sqrt((1-p)/(n p)) at the published "
                         "pooled corpus rate over 2,000 draws. Not a "
                         "measurement.",
        "iqr_over_median_by_surface": dispersion,
        "entry_says": {"draw": 0.09, "spread": 0.42},
    }

    print()
    print("=" * 78)
    print("R-a..R-d, AS WRITTEN")
    print("=" * 78)
    print(f"  R-a  Spearman corpus_full vs space   {rho['corpus_full']:>8.4f}"
          f"   band [0.70, 0.93]   {r_a['verdict']}")
    print(f"       corpus_test beside               {rho['corpus_test']:>8.4f}"
          f"   (does not adjudicate)")
    print(f"       tie ceiling on corpus_full       "
          f"{techos['corpus_full']['max_attainable_spearman']:>8.5f}"
          f"   attenuation at most "
          f"{techos['corpus_full']['attenuation_upper_bound']:.1e}")
    print(f"  R-b  decile overlap                  "
          f"{solape['corpus_full']['fraction']:>8.4f}"
          f"   band [0.35, 0.70]   {r_b['verdict']}")
    print(f"       {solape['corpus_full']['overlap']} of {DECILE} shared; "
          f"boundary ties space {cercanos['space']['boundary_ties_total']}, "
          f"corpus {cercanos['corpus_full']['boundary_ties_total']}")
    print(f"  R-c  ratio p75/p25                   "
          f"{razones['corpus_full']['p75_over_p25']:>8.4f}"
          f"   > 1.30 holds        {r_c['verdict']}")
    print(f"  R-d  reported: space minimum "
          f"{r_d['space_minimum']['pairs'][0]['pair']} ranks "
          f"{r_d['space_minimum']['pairs'][0]['rank_on_corpus_full']['rank']} "
          f"of {N_PAIRS} on the corpus")

    payload = {
        "_env": environment(set_measured=SET, n_pairs=N_PAIRS,
                            n_orders=N_ORDERS, decile=DECILE),
        "what":
            "R-a to R-d of IDEAS.md, adjudicated. A JOIN of two records already "
            "published — order_metrics.json for the exhaustive space and "
            "order_metrics_corpus.json for the two corpus surfaces — over the "
            "2,080 pairs of the 65 end orders of split 0, matched by (i, j). No "
            "search, no regeneration of orders, no new instrument, zero API "
            "calls; both records are read only and neither is rewritten. The "
            "question is whether the ORDERING of pairs transfers between "
            "surfaces, which the corpus record settled nothing about: it "
            "measured that the level does not transfer and that the per-class "
            "composition does not, and a rank is invariant to any monotone "
            "transformation, so neither implies this one either way.",
        "prediction": "IDEAS.md, the entry 'Whether the space can RANK two "
                      "orders when it cannot rate them', committed alone and "
                      "without code before any of these figures existed",
        "surfaces": {s: {"source": mats[s]["from"],
                         "n_cases": mats[s]["n_surface"]} for s in SURFACES},
        "adjudicating_surface": ADJUDICATES,
        "corpus_test_note":
            "measured and published beside every figure, adjudicating nothing, "
            "as the entry fixes: it is 995 cases, half the resolution, and rank "
            "noise rises as the surface shrinks.",
        "n_pairs": N_PAIRS, "n_orders": N_ORDERS,
        "gate": g,
        "predictions": {"R-a": r_a, "R-b": r_b, "R-c": r_c, "R-d": r_d},
        "drafters_arithmetic": reparto,
        "seconds_total": round(time.time() - t_start, 2),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {payload['seconds_total']:.2f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
