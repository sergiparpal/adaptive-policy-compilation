"""
STEP 0 of the audit of rungs 3 and 4: validate the optimizer BEFORE using it.

--------------------------------------------------------------------------
THE PATTERN, AND WHY IT IS REPEATED
--------------------------------------------------------------------------
`harness.ceiling_check` loads the true policy into the engine and measures what
the engine can do with it. It cost zero API calls and it voided rung 1 before a
single cent had been spent on interpreting it. `peldano2.ceiling_check2` did the
same for the hybrid engine.

This does it for the SEARCH. The local search of `local_search.py` is about to
be asked how much accuracy the greedy left on the table over 577 learned rules.
Before believing any answer, it is run on the one instance whose optimum is
known for a reason rather than by search: the 29 rules of the hidden policy,
where the design order scores 1.0000 by construction.

If the local search cannot recover a known optimum over 29 rules, it is
insufficient, and nothing it says about the 577 means anything.

--------------------------------------------------------------------------
TWO INSTANCES, AND THE SECOND IS THE REAL ONE
--------------------------------------------------------------------------
corpus     the 2000 cases with seed 17, which is the protocol of every rung.
           1.0000 here means "fits the sample": 2000 draws touch 1743 distinct
           cases out of 134,400, so many rules never get to compete.

space      the exhaustive 134,400 combinations. 1.0000 here means the order
           found is POLICY-EQUIVALENT to the true one, which is a strictly
           stronger statement and the one worth reporting.

THE CRITERION IS THE EXHAUSTIVE SPACE, and the first run is why. On the corpus
the pairwise-swap search scores 0.9575 and relocation 0.9995 — one wrong case in
2000 — which reads as "close enough". Over the exhaustive space the same two
searches score 0.9356 and 0.999851, and the swap failure turns into 8,660 wrong
cases. The corpus would have passed an instrument that does not work. It is
still reported, because it is the protocol every rung runs on, but it does not
validate anything.

--------------------------------------------------------------------------
FOUR STARTING POINTS
--------------------------------------------------------------------------
greedy     what PLAN_AUDIT asks for, and what Step 1 will depart from.
design     the optimum itself. It must not move: a search that walks away from
           a global optimum is broken, and this is the cheapest way to see it.
reverse    the design order reversed. Rung 1 measured 12.8% for it on the
           corpus; recovering that number is also a check that this file scores
           the same thing the record scored.
random     restarts, because if the greedy start is already optimal the
           question "can it recover the optimum" would go untested.

--------------------------------------------------------------------------
HISTORY OF THIS FILE — the first run failed, and that is on the record
--------------------------------------------------------------------------
August 8, 2026, single run from the greedy start: pairwise swaps 0.9356 over
the exhaustive space, relocation 0.999851. The residue was ONE inverted
relation, H26 beating H23 against a design order that puts H23 first, in a basin
that no single relocation, no single swap and no permutation of three positions
escapes. Repairing the inversion on its own costs accuracy (−190 cases swapping
the pair, −40 lifting H23), which is what makes it a basin rather than an
oversight.

Sergi authorized changing the instrument. The repair is the one the measurement
pointed at — restarts, declared in `local_search.py` — and NOT a wider
neighbourhood, which is what would have been tuned to the symptom. The failing
single-run figures stay measured and printed below: that swaps fail on 8,660
cases is a result about the method, which is what PLAN_AUDIT asked for, and not
a discard.

Usage:  python3 -m peldano3.optimizer_check
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import ACTIONS, generate_corpus
from harness.dsl import Condition
from harness.hidden_policy import true_action
from harness.provenance import describe, environment
from peldano2.engine2 import Space

from .local_search import (MULTISTART_SEED, MULTISTART_STARTS, NEIGHBOURHOODS,
                           build_masks, coverage_length, declared_starts,
                           greedy_order_from_masks, local_search, multistart,
                           random_order, score_order)

OUT = Path("results3")
N_RANDOM_REF = 200          # rung 1 averaged the random order over 200 samples

# The instance that decides. The corpus is measured too and decides nothing.
INSTANCIA_QUE_VALIDA = "espacio exhaustivo"


# ---------------------------------------------------------------------------
# The instance
# ---------------------------------------------------------------------------

def hidden_rules():
    """The 29 rules, with their conditions and their design order."""
    ids, conds, action, born = [], {}, {}, {}
    for i, (rid, cs, act) in enumerate(HIDDEN_DSL):
        ids.append(rid)
        conds[rid] = [Condition(attr=a, op=o, value=v) for a, o, v in cs]
        action[rid] = act
        born[rid] = i
    return ids, conds, action, born


def masks_over_corpus(ids, conds, action, corpus):
    pool = [[rid for rid in ids if all(c.holds(case) for c in conds[rid])]
            for case in corpus]
    truth = [true_action(case) for case in corpus]
    M, W, full = build_masks(ids, pool, truth, action, list(range(len(corpus))))
    return M, W, full


def masks_over_space(ids, conds, action):
    """Extensions over the exhaustive space, and the truth as one mask per
    action. Same bit convention as `Space`, which is what builds the extensions."""
    space = Space()
    bits = {a: bytearray(space.n) for a in ACTIONS}
    for i, case in enumerate(all_cases()):
        bits[true_action(case)][i] = 1
    tmask = {a: int("".join(map(str, b)), 2) for a, b in bits.items()}
    M = {rid: space.extension(conds[rid]) for rid in ids}
    W = {rid: M[rid] & tmask[action[rid]] for rid in ids}
    return M, W, space.full, space.n


# ---------------------------------------------------------------------------

def tail_key_factory(M, W, born):
    """The tail rule of `order_search.greedy_order`: train precision, then
    born_at."""
    def prec(rid):
        w = W[rid].bit_count()
        miss = (M[rid] ^ W[rid]).bit_count()
        return (w / (w + miss)) if (w + miss) else -1.0
    return lambda rid: (-prec(rid), born[rid])


def run_instance(name, ids, M, W, full, n_cases, born, other=None):
    """`other` is the masks of the other instance, to score there the order
    found here. That is what separates 'fits the sample' from 'recovers the
    policy'."""
    design = sorted(ids, key=lambda r: born[r])
    reverse = list(reversed(design))
    greedy = greedy_order_from_masks(ids, M, W, full,
                                     tail_key=tail_key_factory(M, W, born))

    def frac(o):
        return score_order(o, M, W, full) / n_cases

    def frac_other(o):
        if other is None:
            return None
        oM, oW, ofull, on = other
        return score_order(o, oM, oW, ofull) / on

    print()
    print("=" * 78)
    print(f"INSTANCIA · {name}  ({n_cases:,} casos, 29 reglas)")
    print("=" * 78)
    rnd = [frac(random_order(ids, seed=s)) for s in range(N_RANDOM_REF)]
    refs = {
        "orden de diseno (optimo conocido)": frac(design),
        "orden inverso": frac(reverse),
        f"orden aleatorio (media de {N_RANDOM_REF})": statistics.mean(rnd),
        "orden voraz (punto de partida)": frac(greedy),
    }
    for k, v in refs.items():
        print(f"  {k:<46}{v:>10.4f}")
    print(f"  {'longitud de cobertura del voraz':<46}"
          f"{coverage_length(greedy, M, full):>10d}")

    if abs(refs["orden de diseno (optimo conocido)"] - 1.0) > 1e-12:
        print("\n  EL ORDEN DE DISENO NO DA 1.0000 SOBRE ESTA INSTANCIA.")
        print("  El optimo no es conocido y el paso 0 no mide nada. Se aborta.")
        return None

    # ---- ONE RUN, which is what failed on August 8 and stays measured -------
    singles = []
    print()
    print("  UNA SOLA CORRIDA (lo que pedia el PLAN_AUDIT, y lo que fallo)")
    print(f"  {'partida':<10}{'vecindario':<12}{'inicio':>9}{'final':>10}"
          f"{'fallos':>9}{'optimo':>8}{'pasadas':>9}{'movs':>7}{'perms':>7}")
    for sname, s0 in (("voraz", greedy), ("diseno", design), ("inverso", reverse)):
        for vec in NEIGHBOURHOODS:
            o, st = local_search(s0, M, W, full, neighbourhood=vec)
            hit = st["end"] == n_cases
            singles.append({
                "instance": name, "mode": "single", "start": sname,
                "neighbourhood": vec,
                "start_score": round(st["start"] / n_cases, 6),
                "end_score": round(st["end"] / n_cases, 6),
                "wrong_cases": n_cases - st["end"],
                "reached_optimum": hit,
                "rounds": st["rounds"], "moves": st["moves"],
                "swaps": st["swaps"], "exhausted": st["exhausted"],
                "score_on_other_instance": (
                    None if other is None else round(frac_other(o), 6)),
                "equals_design_order": o == design,
            })
            print(f"  {sname:<10}{vec:<12}{st['start']/n_cases:>9.4f}"
                  f"{st['end']/n_cases:>10.6f}{n_cases - st['end']:>9}"
                  f"{'SI' if hit else 'no':>8}"
                  f"{st['rounds']:>9}{st['moves']:>7}{st['swaps']:>7}")

    # ---- MULTI-START, with the constants declared in local_search.py -------
    print()
    print(f"  MULTI-ARRANQUE  ·  semilla {MULTISTART_SEED} · "
          f"{MULTISTART_STARTS} arranques aleatorios + el voraz en la posicion 0")
    print(f"  {'vecindario':<12}{'mejor':>10}{'fallos':>8}{'optimo':>8}"
          f"{'1er acierto':>18}{'aciertan':>11}{'media':>10}{'peor':>10}")
    multis = {}
    for vec in NEIGHBOURHOODS:
        starts = declared_starts(ids, first=greedy)
        o, st = multistart(starts, M, W, full, neighbourhood=vec,
                           optimum=n_cases)
        sc = [r["end_score"] / n_cases for r in st["rows"]]
        st["instance"] = name
        st["best_fraction"] = round(st["best_score"] / n_cases, 6)
        st["wrong_cases"] = n_cases - st["best_score"]
        st["mean_fraction"] = round(statistics.mean(sc), 6)
        st["worst_fraction"] = round(min(sc), 6)
        st["hit_rate"] = round(st["n_hits"] / st["n_starts"], 4)
        st["equals_design_order"] = o == design
        st["score_on_other_instance"] = (
            None if other is None else round(frac_other(o), 6))
        multis[vec] = st
        primero = ("—" if st["starts_until_first_hit"] is None
                   else f"{st['starts_until_first_hit']} ({st['first_hit_start']})")
        aciertan = f"{st['n_hits']}/{st['n_starts']}"
        print(f"  {vec:<12}{st['best_fraction']:>10.6f}{st['wrong_cases']:>8}"
              f"{'SI' if st['reached_optimum'] else 'NO':>8}{primero:>18}"
              f"{aciertan:>11}"
              f"{st['mean_fraction']:>10.6f}{st['worst_fraction']:>10.6f}")
    return singles, multis


# ---------------------------------------------------------------------------

def main() -> int:
    ids, conds, action, born = hidden_rules()
    corpus = generate_corpus(2000, seed=17)

    print("=" * 78)
    print("PASO 0 DE LA AUDITORIA — TECHO DEL OPTIMIZADOR")
    print("=" * 78)
    print("  La busqueda local corre sobre la politica oculta perfecta, donde el")
    print("  optimo se conoce por construccion y no por buscarlo: 1.0000.")
    print(f"  {describe()}")

    cM, cW, cfull = masks_over_corpus(ids, conds, action, corpus)
    sM, sW, sfull, sn = masks_over_space(ids, conds, action)

    singles, multis = [], {}
    for inst, (M, W, full, n, other) in (
            ("corpus", (cM, cW, cfull, len(corpus), (sM, sW, sfull, sn))),
            (INSTANCIA_QUE_VALIDA, (sM, sW, sfull, sn,
                                    (cM, cW, cfull, len(corpus))))):
        out = run_instance(inst, ids, M, W, full, n, born, other=other)
        if out is None:
            return 1
        singles += out[0]
        multis[inst] = out[1]

    # ------------------------------------------------------------- VERDICT
    print()
    print("=" * 78)
    print("VEREDICTO")
    print("=" * 78)
    print(f"  El criterio es 1.0000 sobre el {INSTANCIA_QUE_VALIDA}. El corpus se")
    print("  mide y no valida: habria dado por bueno el instrumento que fallaba.")
    print()
    print(f"  {'instancia · vecindario':<34}{'una corrida':>13}"
          f"{'multi-arranque':>16}{'1er acierto':>13}{'aciertan':>11}")
    verdict = {}
    for inst in ("corpus", INSTANCIA_QUE_VALIDA):
        for vec in NEIGHBOURHOODS:
            single = next(x for x in singles if x["instance"] == inst
                          and x["neighbourhood"] == vec and x["start"] == "voraz")
            multi = multis[inst][vec]
            verdict[f"{inst} · {vec}"] = {
                "single_from_greedy": single["end_score"],
                "single_reaches_optimum": single["reached_optimum"],
                "single_wrong_cases": single["wrong_cases"],
                "multistart": multi["best_fraction"],
                "multistart_reaches_optimum": multi["reached_optimum"],
                "multistart_wrong_cases": multi["wrong_cases"],
                "starts_until_first_hit": multi["starts_until_first_hit"],
                "n_hits": multi["n_hits"], "n_starts": multi["n_starts"],
                "hit_rate": multi["hit_rate"],
            }
            primero = ("—" if multi["starts_until_first_hit"] is None
                       else str(multi["starts_until_first_hit"]))
            aciertan = f"{multi['n_hits']}/{multi['n_starts']}"
            print(f"  {inst + ' · ' + vec:<34}{single['end_score']:>13.6f}"
                  f"{multi['best_fraction']:>16.6f}{primero:>13}{aciertan:>11}")

    decide = {vec: verdict[f"{INSTANCIA_QUE_VALIDA} · {vec}"]
              for vec in NEIGHBOURHOODS}
    passes = any(v["multistart_reaches_optimum"] for v in decide.values())
    print()
    print(f"  PASO 0: {'PASA' if passes else 'NO PASA'}")
    for vec, v in decide.items():
        if v["multistart_reaches_optimum"]:
            que = "alcanza 1.0000"
            coste = (f"con {v['starts_until_first_hit']} arranques  "
                     f"({v['n_hits']}/{v['n_starts']} aciertan)")
        else:
            que = f"se queda en {v['multistart']:.6f}"
            coste = f"{v['multistart_wrong_cases']} casos mal"
        print(f"    {vec:<12}{que:<24}{coste}")

    OUT.mkdir(exist_ok=True)
    (OUT / "optimizer_check.json").write_text(json.dumps({
        "_env": environment(multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            n_random_ref=N_RANDOM_REF),
        "what": "step 0 of the rung 3/4 audit: local search on the perfect "
                "policy, whose optimum is 1.0000 by construction",
        "criterion": f"1.0000 over the {INSTANCIA_QUE_VALIDA}; the corpus is "
                     "measured and does not validate",
        "passes": passes,
        "n_rules": len(ids),
        "n_cases": {"corpus": len(corpus), INSTANCIA_QUE_VALIDA: sn},
        "single_runs": singles,
        "multistart": {inst: {vec: {k: v for k, v in st.items() if k != "rows"}
                              for vec, st in per.items()}
                       for inst, per in multis.items()},
        "multistart_per_start": {
            inst: {vec: st["rows"] for vec, st in per.items()}
            for inst, per in multis.items()},
        "verdict": verdict,
    }, indent=2))
    print(f"\n-> {OUT/'optimizer_check.json'}")
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
