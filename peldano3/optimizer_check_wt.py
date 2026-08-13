"""
STEP 0 FOR THE WEIGHTED INSTRUMENT — phase P2 of `PLAN_BUDGET_LS.md`.

--------------------------------------------------------------------------
WHY THIS EXISTS AND WHY IT BLOCKS
--------------------------------------------------------------------------
`peldano3.optimizer_check` validated the UNWEIGHTED local search against an
instance whose optimum is known for a reason rather than by search, and it
failed the first time: the neighbourhood the audit had declared could not
recover it. That failure is why the multi-start exists.

Step 3 of the audit adds a second objective — the class-balanced one, which
weights each case by 1/|its class| — and an objective is part of the
instrument. So the same gate runs again, on the same instance, before any
balanced figure is believed.

--------------------------------------------------------------------------
THE OPTIMUM IS KNOWN BY CONSTRUCTION, AGAIN
--------------------------------------------------------------------------
The 29 rules of the hidden policy in design order get EVERY case right. So they
maximize every objective with non-negative weights at once, the balanced one
included: every class reaches recall 1, and no order can beat that in any
class. With the integer weights of `local_search.balanced_weights`,

    optimum = L * (number of classes present)

which is arithmetic, not a search result. Anything short of it is the
instrument failing, not the instance being hard. Divided by that optimum, the
score IS macro-recall — balanced accuracy — so the tables below read in [0, 1].

--------------------------------------------------------------------------
TWO INSTANCES, AND THE SECOND IS STILL THE ONE THAT VALIDATES
--------------------------------------------------------------------------
The corpus is measured and decides nothing, for the reason Step 0 recorded: it
certified an instrument that did not work. The criterion here is the exhaustive
space of 134,400 combinations under the DECLARED neighbourhood — `move+swap` is
what phases P4 and P5 will run, so it is what has to pass.

The class counts come off the masks, not off the oracle: the cases of class c
are exactly the union of W[r] over the rules whose action is c, since W[r] is by
construction the subset of M[r] that r gets right, and every case of this
instance is matched by a rule carrying its correct label. So this module never
imports `true_action`; it reuses the mask builders of `optimizer_check`, which
is also what keeps the two gates measuring the same instance.

Usage:  python3 -m peldano3.optimizer_check_wt
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from collections import Counter
from math import comb
from pathlib import Path

from harness.domain import generate_corpus
from harness.provenance import describe, environment

from .local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                           MULTISTART_STARTS, NEIGHBOURHOODS, coverage_length,
                           declared_starts, greedy_order_from_masks,
                           local_search, multistart, score_order,
                           weights_from_counts)
from .optimizer_check import (hidden_rules, masks_over_corpus, masks_over_space,
                              tail_key_factory)

OUT = Path("results3")

# The instance that decides. The corpus is measured and does not validate.
INSTANCIA_QUE_VALIDA = "espacio exhaustivo"


def class_counts_from_masks(ids, action, W, full):
    """
    Cases per class, read off the masks — ONLY where every case is winnable.

    Every bit of W[r] belongs to a case of class action[r], so the union over
    the rules of each action counts the cases of that class THAT SOME CORRECT
    RULE MATCHES. That is the per-class CEILING, and it coincides with the class
    size exactly when every case has a correct rule covering it.

    On the hidden policy it does: every case is covered by its own rule. On the
    577 learned rules it does NOT — two thirds of T3_ENGINEERING and of
    ACCOUNT_MANAGER have no correct rule at all — and there the union falls 98
    cases short of the 1005 of split 0's train. Weighting by a ceiling instead
    of by a class size would inflate exactly the classes the balanced objective
    exists to protect, by a factor of three, and would silently maximize
    something other than what the record maximized.

    So the precondition is CHECKED rather than documented, and the function
    raises instead of returning a ceiling that a caller would read as a count.
    The balanced objective of P5 comes from `Counter(truth)` —
    `budget_and_balance_ls.balanced_objective` — and never from here.
    """
    porclase = {}
    for rid in ids:
        porclase[action[rid]] = porclase.get(action[rid], 0) | W[rid]
    ganables = 0
    for m in porclase.values():
        ganables |= m
    if ganables != full:
        faltan = (full & ~ganables).bit_count()
        raise ValueError(
            f"{faltan} casos no tienen ninguna regla correcta que los case: el "
            "recuento por mascaras seria el techo por clase y no el tamano de "
            "la clase")
    return Counter({c: m.bit_count() for c, m in porclase.items() if m})


# ---------------------------------------------------------------------------
# What the restarts are really worth
# ---------------------------------------------------------------------------

def _binom_cdf(k, n, p):
    """P(X <= k) for X ~ Bin(n, p), with exact integer binomials."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return sum(comb(n, i) * p ** i * (1.0 - p) ** (n - i) for i in range(k + 1))


def _root(f, lo, hi, iters=200):
    """Bisection on a monotone f with a sign change in [lo, hi]."""
    flo = f(lo)
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2.0


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval. Standard library only, like everything here."""
    lo = 0.0 if k == 0 else _root(
        lambda p: (1.0 - _binom_cdf(k - 1, n, p)) - alpha / 2.0, 0.0, 1.0)
    hi = 1.0 if k == n else _root(
        lambda p: _binom_cdf(k, n, p) - alpha / 2.0, 0.0, 1.0)
    return lo, hi


def restart_budget(n_hits, n_random=MULTISTART_STARTS):
    """
    What `MULTISTART_STARTS` buys AT THE MEASURED RATE, which is not the rate
    the constant was declared against.

    `local_search.py` justifies 64 starts thus: "At a one-in-four rate, 64
    starts miss altogether with probability 0.75**64, below 1e-8." That 1-in-4
    was measured UNWEIGHTED, in Step 0. Under weights the rate is lower, so the
    inherited figure does not apply and is recomputed here.

    The constant is NOT touched. It was declared before the runs that used it
    and changing it after seeing a result is the failure this project studies;
    what is recomputed is the claim made ABOUT it.

    Read it as: the probability that a FRESH set of `n_random` starts misses
    entirely, estimated from these ones. The point estimate reuses the same
    draws that produced the rate, so the interval is the honest part.
    """
    p = n_hits / n_random
    lo, hi = clopper_pearson(n_hits, n_random)
    return {
        "hits_of_random_starts": n_hits,
        "random_starts": n_random,
        "hit_rate": round(p, 6),
        "hit_rate_ci95": [round(lo, 6), round(hi, 6)],
        "miss_probability": (1.0 - p) ** n_random,
        # ordered low to high: the high hit rate gives the low miss probability
        "miss_probability_ci95": [(1.0 - hi) ** n_random,
                                  (1.0 - lo) ** n_random],
        "inherited_claim": {
            "hit_rate": 0.25, "miss_probability": 0.75 ** n_random,
            "source": "local_search.py, medido sin pesos en el paso 0",
        },
    }


def run_instance(name, ids, M, W, full, n_cases, action, born):
    """The weighted gate over one instance. Returns None if the optimum is not
    known here, which aborts the whole check."""
    n = class_counts_from_masks(ids, action, W, full)
    wt, L, _ = weights_from_counts(ids, action, n)
    optimo = L * len(n)

    design = sorted(ids, key=lambda r: born[r])
    greedy = greedy_order_from_masks(ids, M, W, full,
                                     tail_key=tail_key_factory(M, W, born))

    def bal(o):
        """Weighted score as a fraction of the optimum: macro-recall."""
        return score_order(o, M, W, full, wt) / optimo

    def e2e(o):
        return score_order(o, M, W, full) / n_cases

    print()
    print("=" * 78)
    print(f"INSTANCIA · {name}  ({n_cases:,} casos, {len(ids)} reglas, "
          f"{len(n)} clases)")
    print("=" * 78)
    print(f"  optimo ponderado = L x clases = {L} x {len(n)} = {optimo}")
    print(f"  casos por clase: "
          + " · ".join(f"{c} {v}" for c, v in sorted(n.items())))
    print()
    print(f"  {'orden':<40}{'balanceado':>12}{'e2e':>10}")
    for etiqueta, o in (("orden de diseno (optimo conocido)", design),
                        ("orden inverso", list(reversed(design))),
                        ("orden voraz sin pesos (partida)", greedy)):
        print(f"  {etiqueta:<40}{bal(o):>12.6f}{e2e(o):>10.4f}")
    print(f"  {'longitud de cobertura del voraz':<40}"
          f"{coverage_length(greedy, M, full):>12d}")

    if score_order(design, M, W, full, wt) != optimo:
        print("\n  EL ORDEN DE DISENO NO ALCANZA EL OPTIMO PONDERADO.")
        print("  El optimo no es conocido y el paso 0 no mide nada. Se aborta.")
        return None

    # ---- IS THE OPTIMUM A FIXED POINT? -------------------------------------
    # No move is applied without STRICT improvement, so a search started at a
    # global optimum must return it untouched. If it does not, the objective
    # being maximized is not the one declared.
    print()
    print("  DESDE EL OPTIMO — un buscador que se aleja de el esta roto")
    print(f"  {'vecindario':<12}{'sale de el':>12}{'balanceado':>12}"
          f"{'movs':>7}{'perms':>7}")
    fijo = {}
    for vec in NEIGHBOURHOODS:
        o, st = local_search(design, M, W, full, neighbourhood=vec, wt=wt)
        fijo[vec] = {"es_punto_fijo": o == design,
                     "start_score": st["start"], "end_score": st["end"],
                     "moves": st["moves"], "swaps": st["swaps"]}
        print(f"  {vec:<12}{'no' if o == design else 'SI':>12}"
              f"{st['end']/optimo:>12.6f}{st['moves']:>7}{st['swaps']:>7}")

    # ---- MULTI-START, with the declared constants ---------------------------
    print()
    print(f"  MULTI-ARRANQUE PONDERADO  ·  semilla {MULTISTART_SEED} · "
          f"{MULTISTART_STARTS} arranques + el voraz en la posicion 0")
    print(f"  {'vecindario':<12}{'mejor':>11}{'optimo':>8}{'1er acierto':>18}"
          f"{'aciertan':>11}{'media':>10}{'peor':>10}{'seg':>8}")
    multis = {}
    for vec in NEIGHBOURHOODS:
        t0 = time.time()
        starts = declared_starts(ids, first=greedy)
        o, st = multistart(starts, M, W, full, neighbourhood=vec,
                           optimum=optimo, wt=wt)
        sc = [r["end_score"] / optimo for r in st["rows"]]
        st["instance"] = name
        st["best_balanced"] = round(st["best_score"] / optimo, 6)
        st["best_e2e"] = round(e2e(o), 6)
        st["mean_balanced"] = round(statistics.mean(sc), 6)
        st["worst_balanced"] = round(min(sc), 6)
        st["hit_rate"] = round(st["n_hits"] / st["n_starts"], 4)
        st["equals_design_order"] = o == design
        st["exhausted_any"] = any(r["exhausted"] for r in st["rows"])
        st["seconds"] = round(time.time() - t0, 1)
        # The greedy occupies index 0 and is not one of the restarts, so the
        # rate the budget depends on counts hits among the random starts only.
        st["greedy_hits"] = st["rows"][0]["end_score"] == optimo
        st["restart_budget"] = restart_budget(
            sum(1 for r in st["rows"][1:] if r["end_score"] == optimo))
        multis[vec] = st
        primero = ("—" if st["starts_until_first_hit"] is None
                   else f"{st['starts_until_first_hit']} ({st['first_hit_start']})")
        aciertan = f"{st['n_hits']}/{st['n_starts']}"
        print(f"  {vec:<12}{st['best_balanced']:>11.6f}"
              f"{'SI' if st['reached_optimum'] else 'NO':>8}{primero:>18}"
              f"{aciertan:>11}"
              f"{st['mean_balanced']:>10.6f}{st['worst_balanced']:>10.6f}"
              f"{st['seconds']:>8.0f}")
    return {"L": L, "n_classes": len(n), "optimum": optimo,
            "cases_per_class": dict(sorted(n.items())),
            "design_balanced": round(bal(design), 6),
            "reverse_balanced": round(bal(list(reversed(design))), 6),
            "greedy_balanced": round(bal(greedy), 6),
            "greedy_e2e": round(e2e(greedy), 6),
            "desde_el_optimo": fijo, "multiarranque": multis}


def main() -> int:
    t_start = time.time()
    ids, conds, action, born = hidden_rules()
    corpus = generate_corpus(2000, seed=17)

    print("=" * 78)
    print("PASO 0 PONDERADO — TECHO DEL OPTIMIZADOR CON EL OBJETIVO BALANCEADO")
    print("=" * 78)
    print("  La busqueda local ponderada corre sobre la politica oculta perfecta,")
    print("  donde el optimo se conoce por construccion y no por buscarlo:")
    print("  L x (numero de clases), porque la politica acierta todos los casos")
    print("  y por tanto llega a recall 1 en todas las clases a la vez.")
    print(f"  {describe()}")

    cM, cW, cfull = masks_over_corpus(ids, conds, action, corpus)
    sM, sW, sfull, sn = masks_over_space(ids, conds, action)

    per = {}
    for inst, (M, W, full, ncas) in (
            ("corpus", (cM, cW, cfull, len(corpus))),
            (INSTANCIA_QUE_VALIDA, (sM, sW, sfull, sn))):
        out = run_instance(inst, ids, M, W, full, ncas, action, born)
        if out is None:
            return 1
        per[inst] = out

    # ------------------------------------------------------------- VERDICT
    print()
    print("=" * 78)
    print("VEREDICTO")
    print("=" * 78)
    print(f"  El criterio es alcanzar el optimo sobre el {INSTANCIA_QUE_VALIDA}")
    print(f"  con el vecindario declarado ({DECLARED_NEIGHBOURHOOD}), que es el")
    print("  que van a usar las fases P4 y P5. El corpus se mide y no valida.")
    print()
    print(f"  {'instancia · vecindario':<34}{'balanceado':>12}{'optimo':>8}"
          f"{'1er acierto':>13}{'aciertan':>11}{'punto fijo':>12}")
    verdict = {}
    for inst in ("corpus", INSTANCIA_QUE_VALIDA):
        for vec in NEIGHBOURHOODS:
            m = per[inst]["multiarranque"][vec]
            f = per[inst]["desde_el_optimo"][vec]
            verdict[f"{inst} · {vec}"] = {
                "best_balanced": m["best_balanced"],
                "reaches_optimum": m["reached_optimum"],
                "starts_until_first_hit": m["starts_until_first_hit"],
                "n_hits": m["n_hits"], "n_starts": m["n_starts"],
                "hit_rate": m["hit_rate"],
                "optimum_is_fixed_point": f["es_punto_fijo"],
                "exhausted_any": m["exhausted_any"],
                "greedy_hits": m["greedy_hits"],
                "restart_budget": m["restart_budget"],
                "seconds": m["seconds"],
            }
            primero = ("—" if m["starts_until_first_hit"] is None
                       else str(m["starts_until_first_hit"]))
            aciertan = f"{m['n_hits']}/{m['n_starts']}"
            print(f"  {inst + ' · ' + vec:<34}{m['best_balanced']:>12.6f}"
                  f"{'SI' if m['reached_optimum'] else 'NO':>8}{primero:>13}"
                  f"{aciertan:>11}"
                  f"{'SI' if f['es_punto_fijo'] else 'NO':>12}")

    decide = verdict[f"{INSTANCIA_QUE_VALIDA} · {DECLARED_NEIGHBOURHOOD}"]
    passes = decide["reaches_optimum"] and decide["optimum_is_fixed_point"]
    print()
    print(f"  PASO 0 PONDERADO: {'PASA' if passes else 'NO PASA'}")
    if decide["reaches_optimum"]:
        print(f"    {DECLARED_NEIGHBOURHOOD}: alcanza el optimo con "
              f"{decide['starts_until_first_hit']} arranques "
              f"({decide['n_hits']}/{decide['n_starts']} aciertan)")
    else:
        print(f"    {DECLARED_NEIGHBOURHOOD}: se queda en "
              f"{decide['best_balanced']:.6f} de acierto balanceado")
    if not decide["optimum_is_fixed_point"]:
        print("    y ADEMAS se aleja del optimo cuando arranca en el")

    # ---- WHAT THE 64 RESTARTS ARE REALLY WORTH, AT THE MEASURED RATE -------
    print()
    print("=" * 78)
    print("PRESUPUESTO DE REINICIOS — recalculado a la tasa medida CON PESOS")
    print("=" * 78)
    print(f"  local_search.py declara {MULTISTART_STARTS} arranques con este")
    print("  argumento: a una tasa de 1 de cada 4, fallar del todo tiene")
    print(f"  probabilidad 0.75**{MULTISTART_STARTS} = "
          f"{0.75 ** MULTISTART_STARTS:.2e}. Ese 1-de-4 se midio SIN PESOS.")
    print("  La constante no se toca; lo que se recalcula es la afirmacion.")
    print()
    print(f"  {'instancia · vecindario':<34}{'aciertos':>10}{'tasa':>9}"
          f"{'IC95 tasa':>18}{'fallo':>11}{'IC95 fallo':>24}")
    for inst in ("corpus", INSTANCIA_QUE_VALIDA):
        for vec in NEIGHBOURHOODS:
            b = per[inst]["multiarranque"][vec]["restart_budget"]
            lo, hi = b["hit_rate_ci95"]
            flo, fhi = b["miss_probability_ci95"]
            print(f"  {inst + ' · ' + vec:<34}"
                  f"{b['hits_of_random_starts']}/{b['random_starts']:<7}"
                  f"{b['hit_rate']:>9.4f}"
                  f"{f'[{lo:.4f}, {hi:.4f}]':>18}"
                  f"{b['miss_probability']:>11.2e}"
                  f"{f'[{flo:.1e}, {fhi:.1e}]':>24}")
    print()
    print("  Es la probabilidad de que un conjunto NUEVO de 64 arranques falle")
    print("  entero. El estimador puntual reutiliza las mismas tiradas que dan")
    print("  la tasa, asi que la parte honesta es el intervalo.")
    print("  Y esto se mide sobre 29 reglas: sobre las 577 de P4 y P5 la tasa")
    print("  no tiene por que ser esta.")

    OUT.mkdir(exist_ok=True)
    (OUT / "optimizer_check_wt.json").write_text(json.dumps({
        "_env": environment(multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            neighbourhood=DECLARED_NEIGHBOURHOOD),
        "what": "phase P2 of step 3 of the audit: the class-weighted local "
                "search on the perfect policy, whose weighted optimum is "
                "L x (number of classes) by construction",
        "criterion": f"the weighted optimum over the {INSTANCIA_QUE_VALIDA} "
                     f"with the declared neighbourhood "
                     f"({DECLARED_NEIGHBOURHOOD}); the corpus is measured and "
                     "does not validate",
        "passes": passes,
        "n_rules": len(ids),
        "n_cases": {"corpus": len(corpus), INSTANCIA_QUE_VALIDA: sn},
        "instances": {inst: {k: v for k, v in d.items() if k != "multiarranque"}
                      for inst, d in per.items()},
        "multistart": {
            inst: {vec: {k: v for k, v in st.items() if k != "rows"}
                   for vec, st in d["multiarranque"].items()}
            for inst, d in per.items()},
        "multistart_per_start": {
            inst: {vec: st["rows"] for vec, st in d["multiarranque"].items()}
            for inst, d in per.items()},
        "verdict": verdict,
        "seconds_total": round(time.time() - t_start, 1),
    }, indent=2))
    print(f"\n  coste total: {time.time() - t_start:.0f}s")
    print(f"-> {OUT/'optimizer_check_wt.json'}")
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
