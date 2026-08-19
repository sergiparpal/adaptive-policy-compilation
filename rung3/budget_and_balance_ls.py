"""
STEP 3 OF THE AUDIT — `budget_and_balance` with the audited optimizer.

--------------------------------------------------------------------------
WHAT CHANGES AND WHAT DOES NOT
--------------------------------------------------------------------------
Only the optimizer: the decision-list greedy becomes the multi-start local
search declared in `local_search.py` — seed 17, 64 random starts plus the
record's greedy at index 0, neighbourhood `move+swap`.

Everything else is the record's, and phase P3 checks that it is: corpus of 2000
at seed 17, the five splits grouped by case identity and stratified by action,
the pure pool, the fractions, the draw seeds, simple random subsampling — never
stratified, since stratifying needs the labels being rationed — and evaluation
always over the whole test half.

--------------------------------------------------------------------------
WHAT "TRAIN" MEANS HERE
--------------------------------------------------------------------------
The objective sees the LABELLED SUBSET and nothing else, so `*_train` is scored
over that subset, not over the train half. It is the only set on which "the
multi-start is never worse than the greedy" is an invariant rather than a hope:
the greedy is start 0, and start 0 is only optimal-by-construction against the
objective it was built for.

--------------------------------------------------------------------------
WHAT THE STARTS DID, AND WHY IT IS RECORDED
--------------------------------------------------------------------------
With a fixed seed there is no hit rate to estimate, and on the real instance
there is no known optimum to hit. What can still be said is how the 65 starts
spread: how many tie at the best train score (`n_at_best`), where the winner
came from, and how many distinct scores they reached. That is what says whether
64 restarts are comfortable or tight here — one start at the best, out of 65
values all distinct, means the search is riding on a single lucky shuffle.

--------------------------------------------------------------------------
TWO SURFACES, AND §2 NEEDS BOTH
--------------------------------------------------------------------------
Every order is scored on corpus test (primary, comparable with the record) and
over the exhaustive space of 134,400 combinations. §2 additionally reports
MACRO-RECALL on the space for both objectives and both optimizers: the corpus is
the long-tailed arrival distribution and the space is uniform, so it is exactly
where a class-balanced objective and a total one have to diverge, and that
divergence is the question the section asks.

--------------------------------------------------------------------------
THE OLD RECORD IS NOT TOUCHED
--------------------------------------------------------------------------
`results3/budget_and_balance.json` is read-only for this work. It is
deliberately pre-tie-break, so its numbers stay reproducible beside the new
ones, and `python3 -m rung3.budget_and_balance` is NEVER run: it has no
guard and dumps over that record on finishing. Greedy-today comes from
importing `budget_and_balance.greedy` and calling it.

A partial run writes its own file. Every save rewrites the whole document from
the rows of THIS process, so letting `--sections budget` land on the canonical
name would silently drop §2 — the loss `harness/record_guard.py` exists to
prevent, and which nearly happened in `sweep_ls` on 2026-08-08.

Usage:  python3 -m rung3.budget_and_balance_ls
        python3 -m rung3.budget_and_balance_ls --sections budget
        python3 -m rung3.budget_and_balance_ls --checks
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.provenance import describe, environment
from rung3.budget_and_balance import FRACTIONS, N_DRAWS, N_SPLITS
from rung3.budget_and_balance import greedy as greedy_del_registro
from rung3.budget_and_balance import per_class
from rung3.optimizer_check_wt import class_counts
from rung3.order_search import (build_tables, ceiling, greedy_order, load,
                                   split, subsumption_below)
from rung3.order_search_ls import space_pools

from .local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                           MULTISTART_STARTS, build_masks, coverage_length,
                           declared_starts, multistart, score_order,
                           weights_from_counts)

OUT = Path("results3")
POOL = "puro"
GROUPS = ("budget", "balanced")

# The record every P3 check is measured against: `results3/order_search_ls.
# json`, splits[0], pool puro — and the born_at figure of the FINDINGS3 erratum
# of 2026-08-08. They are constants because a check that reads its expectation
# out of the file it is checking is not a check.
ESPERADO = {
    "voraz test": 0.7487,
    "busqueda local test": 0.8472,
    "longitud de cobertura": 559,
    "born_at espacio": 0.3148,
}

# `results3/budget_and_balance.json`, PRE-TIE-BREAK: the record this re-measures.
# `tests/test_budget_ls.py` pins these against that file, so they cannot drift
# from it, and the file itself is never written.
PUBLICADO = {
    1.00: {"labels": 1005, "test_mean": 0.7707, "test_sd": 0.0374,
           "test_min": 0.7425, "test_max": 0.8430},
    0.25: {"labels": 251, "test_mean": 0.7681, "test_sd": 0.0326,
           "test_min": 0.7290, "test_max": 0.8522},
    0.10: {"labels": 100, "test_mean": 0.7488, "test_sd": 0.0352,
           "test_min": 0.6500, "test_max": 0.8053},
    0.05: {"labels": 50, "test_mean": 0.7049, "test_sd": 0.0535,
           "test_min": 0.5596, "test_max": 0.8241},
    0.01: {"labels": 10, "test_mean": 0.5251, "test_sd": 0.0628,
           "test_min": 0.3850, "test_max": 0.6577},
}
PUBLICADO_OBJETIVO = {
    "total": {"e2e_test_mean": 0.7707, "balanced_acc_mean": 0.5241},
    "balanced": {"e2e_test_mean": 0.7150, "balanced_acc_mean": 0.6936},
}

REFERENCIAS = {
    "born_at corpus": 0.5216, "born_at espacio": 0.3148,
    "aleatorio corpus": 0.4227,
    "ls supervision plena, pool puro (order_search_ls)": 0.8530,
    "cota por cobertura, corpus": 0.9010,
    "cota por cobertura, espacio": 0.8784,
}


def record_name(groups) -> str:
    """Where a run writes. A partial run goes to its own file."""
    if set(groups) == set(GROUPS):
        return "budget_and_balance_ls.json"
    return f"budget_and_balance_ls_{'_'.join(groups)}.json"


# ---------------------------------------------------------------------------
# The instance — the record's, and checked to be
# ---------------------------------------------------------------------------

def load_instance():
    """Corpus, rules, pure pool, truth and the five splits, built exactly as
    `budget_and_balance` built them."""
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ids = [r["rule_id"] for r in rules]
    below = subsumption_below(rules, ext)
    matched, _undef, truth = build_tables(corpus, rules, conds, below)
    splits = [split(corpus, truth, seed=17 + s) for s in range(N_SPLITS)]
    return {"corpus": corpus, "rules": rules, "ids": ids, "action": action,
            "born": born, "conds": conds, "below": below, "matched": matched,
            "truth": truth, "splits": splits}


def subsample(tr, frac, s, d):
    """The record's draw, to the seed: simple random sampling of the train
    half. NOT stratified — stratifying would need the labels being rationed,
    which is the resource the experiment is measuring."""
    if frac >= 1.0:
        return tr
    k = max(1, round(frac * len(tr)))
    return sorted(random.Random(1000 * s + d).sample(tr, k))


def balanced_objective(ids, action, truth, label_idx):
    """
    The balanced objective for one labelled subset, in the two forms the run
    needs, both built from ONE count of the classes.

    `budget_and_balance.greedy` takes class -> 1/|class| as floats and the local
    search takes rule -> integer weight. They have to be the SAME objective, and
    the only way to be sure is for both to come out of the same Counter — the
    very one `budget_and_balance` builds, `Counter(truth[i] for i in tr)`. The
    identity is checked below rather than trusted.

    NOT from the masks, and not from any per-class ceiling: over the 577 rules
    the two differ by 98 cases in 1005, and they differ precisely in
    T3_ENGINEERING and ACCOUNT_MANAGER, where two thirds of the cases have no
    correct rule at all. Weighting by a ceiling would multiply the weight of
    exactly the classes this objective exists to protect by about three, and
    would maximize something other than what the record maximized while
    reporting it under the same name.

    Returns (weights, wt, counts, L).
    """
    counts = Counter(truth[i] for i in label_idx)
    weights = {c: 1.0 / counts[c] for c in counts}
    wt, L, n = weights_from_counts(ids, action, counts)
    if n is not counts:
        raise ValueError("los pesos del voraz balanceado y los de la busqueda "
                         "local no salen del mismo recuento de clases")
    return weights, wt, counts, L


def search(ids, greedy, M, W, full, wt=None):
    """D2: start 0 is the record's greedy, tail included, so the multi-start
    can never come back worse on train than the single greedy run, and the
    difference measured is the optimizer and nothing else."""
    return multistart(declared_starts(ids, first=greedy), M, W, full,
                      neighbourhood=DECLARED_NEIGHBOURHOOD, wt=wt)


def start_spread(st):
    """
    What the 65 starts actually did.

    With the seed fixed there is no rate to estimate and no optimum to hit, so
    what is on the record is the shape of the sample: how many reach the best
    train score, which start won, and how many distinct scores came out.
    """
    scores = [r["end_score"] for r in st["rows"]]
    return {
        "n_at_best": sum(1 for x in scores if x == st["best_score"]),
        "best_from_index": st["best_from_index"],
        "best_from": st["best_from"],
        "end_score_min": min(scores),
        "end_score_max": max(scores),
        "end_score_distinct": len(set(scores)),
        "n_starts": len(scores),
    }


# ---------------------------------------------------------------------------
# One configuration
# ---------------------------------------------------------------------------

def run_config(inst, espacio, frac, s, d, test_masks):
    """Greedy and multi-start over one labelled subset, on both surfaces."""
    ids, action, matched = inst["ids"], inst["action"], inst["matched"]
    rules, truth = inst["rules"], inst["truth"]
    tr, te = inst["splits"][s]
    sM, sW, sfull, sn = espacio["masks"]

    sub = subsample(tr, frac, s, d)
    M, W, full = build_masks(ids, matched, truth, action, sub)
    tM, tW, tfull = test_masks

    t0 = time.time()
    greedy = greedy_del_registro(rules, matched, truth, action, sub)
    best, st = search(ids, greedy, M, W, full)
    dt = time.time() - t0

    fila = st["rows"][st["best_from_index"]]
    row = {
        "fraction": frac, "split": s, "draw": d, "labels": len(sub),
        "greedy_train": round(score_order(greedy, M, W, full) / len(sub), 4),
        "greedy_test": round(score_order(greedy, tM, tW, tfull) / len(te), 4),
        "greedy_space": round(score_order(greedy, sM, sW, sfull) / sn, 4),
        "ls_train": round(st["best_score"] / len(sub), 4),
        "ls_test": round(score_order(best, tM, tW, tfull) / len(te), 4),
        "ls_space": round(score_order(best, sM, sW, sfull) / sn, 4),
        "rounds": fila["rounds"],
        "exhausted": any(r["exhausted"] for r in st["rows"]),
        "coverage_length": coverage_length(greedy, M, full),
        "seconds": round(dt, 1),
    }
    row.update(start_spread(st))
    row["delta_test"] = round(row["ls_test"] - row["greedy_test"], 4)
    row["delta_train"] = round(row["ls_train"] - row["greedy_train"], 4)
    return row


def aggregate(rows, frac):
    """Per-fraction aggregate, in the record's shape."""
    sub = [r for r in rows if r["fraction"] == frac]
    out = {"fraction": frac, "labels": sub[0]["labels"], "n_runs": len(sub)}
    for quien in ("greedy", "ls"):
        te = [r[f"{quien}_test"] for r in sub]
        out[quien] = {
            "test_mean": round(statistics.mean(te), 4),
            "test_sd": round(statistics.pstdev(te), 4),
            "test_min": round(min(te), 4), "test_max": round(max(te), 4),
            "train_mean": round(statistics.mean(
                [r[f"{quien}_train"] for r in sub]), 4),
            "space_mean": round(statistics.mean(
                [r[f"{quien}_space"] for r in sub]), 4),
        }
    out["delta_test_mean"] = round(out["ls"]["test_mean"]
                                   - out["greedy"]["test_mean"], 4)
    out["delta_space_mean"] = round(out["ls"]["space_mean"]
                                    - out["greedy"]["space_mean"], 4)
    out["coverage_length_mean"] = round(statistics.mean(
        [r["coverage_length"] for r in sub]), 1)
    out["n_at_best_mean"] = round(statistics.mean(
        [r["n_at_best"] for r in sub]), 2)
    out["end_score_distinct_mean"] = round(statistics.mean(
        [r["end_score_distinct"] for r in sub]), 1)
    out["ls_worse_than_greedy_on_test"] = sum(
        1 for r in sub if r["ls_test"] < r["greedy_test"])
    out["ls_worse_than_greedy_on_train"] = sum(
        1 for r in sub if r["ls_train"] < r["greedy_train"])
    out["exhausted"] = sum(1 for r in sub if r["exhausted"])
    out["seconds"] = round(sum(r["seconds"] for r in sub), 1)
    return out


# ---------------------------------------------------------------------------
# Is 0.8530 converged, or is it "the best of 65"?
# ---------------------------------------------------------------------------

BUDGETS = (64, 128, 256)


def start_budget_check(inst, espacio, budgets=BUDGETS, splits=None):
    """
    A DIAGNOSTIC, NOT A TUNING, and the distinction is the whole point.

    §1 measured that at full supervision exactly ONE start of 65 reaches the
    best train score, in all five configurations. That makes the published
    figure the best of 65 draws rather than a converged value, and on this
    instance no optimum is known, so nothing else can say whether a 66th start
    would beat it. This runs the same configurations with more starts and
    reports whether the best train score moves — and, where it moves, what
    happens on the two evaluation surfaces.

    **`MULTISTART_STARTS` stays 64 because it was DECLARED before the runs that
    used it.** That is the whole reason and it is not contingent on anything
    measured here. Whatever this diagnostic returns — better, worse or
    unchanged on test — reading it back into the constant would be choosing a
    hyperparameter off the evaluation surface, which is rule 6 with its sign
    reversed. What a diagnostic can legitimately produce is a CAVEAT on the
    figure, never a new figure and never a new constant.

    Run over all five splits, because one split and one 65 -> 257 jump is a
    sample of size one and cannot tell an effect from a draw.

    The comparison is nested by construction: `declared_starts` draws its
    shuffles from `random.Random(17)` in sequence, so the first 65 starts of the
    256 run are the 65 of the 64 run, bit for bit. Checked below rather than
    assumed — without it the rows would not be comparable at all.
    """
    ids, action, matched = inst["ids"], inst["action"], inst["matched"]
    rules, truth = inst["rules"], inst["truth"]
    sM, sW, sfull, sn = espacio["masks"]
    splits = list(range(N_SPLITS)) if splits is None else list(splits)

    print()
    print("=" * 78)
    print("SENSIBILIDAD AL PRESUPUESTO DE ARRANQUES  (diagnostico, no ajuste)")
    print("=" * 78)
    print(f"  fraccion 100% · pool {POOL} · particiones {splits}")
    print(f"  MULTISTART_STARTS sigue en {MULTISTART_STARTS} porque estaba")
    print("  DECLARADO antes de las corridas. Lo que salga aqui no es un motivo.")
    print()
    print(f"  {'part':>5}{'arranques':>10}{'train':>9}{'(bruto)':>9}{'test':>9}"
          f"{'espacio':>9}{'en el mejor':>13}{'distintas':>11}{'seg':>7}")

    rows = []
    for s in splits:
        tr, te = inst["splits"][s]
        M, W, full = build_masks(ids, matched, truth, action, tr)
        tM, tW, tfull = build_masks(ids, matched, truth, action, te)
        greedy = greedy_del_registro(rules, matched, truth, action, tr)
        base = declared_starts(ids, first=greedy, n=budgets[0])
        ref = None
        for n in budgets:
            starts = declared_starts(ids, first=greedy, n=n)
            if starts[:len(base)] != base:
                raise ValueError("los arranques no son anidados: las filas no "
                                 "son comparables")
            t0 = time.time()
            best, st = multistart(starts, M, W, full,
                                  neighbourhood=DECLARED_NEIGHBOURHOOD)
            fila = {
                "split": s, "starts": len(starts), "random_starts": n,
                "train_score": st["best_score"],
                "train": round(st["best_score"] / len(tr), 4),
                "test": round(score_order(best, tM, tW, tfull) / len(te), 4),
                "space": round(score_order(best, sM, sW, sfull) / sn, 4),
                "seconds": round(time.time() - t0, 1),
            }
            fila.update(start_spread(st))
            if ref is None:
                ref = fila
            fila["train_score_delta"] = fila["train_score"] - ref["train_score"]
            fila["train_delta"] = round(fila["train"] - ref["train"], 4)
            fila["test_delta"] = round(fila["test"] - ref["test"], 4)
            fila["space_delta"] = round(fila["space"] - ref["space"], 4)
            rows.append(fila)
            print(f"  {s:>5}{fila['starts']:>10}{fila['train']:>9.4f}"
                  f"{fila['train_score']:>9}{fila['test']:>9.4f}"
                  f"{fila['space']:>9.4f}{fila['n_at_best']:>13}"
                  f"{fila['end_score_distinct']:>11}{fila['seconds']:>7.0f}")

    # -------------------------------------------------- does it generalize?
    mayor = max(budgets)
    finales = [r for r in rows if r["random_starts"] == mayor]
    mueven = [r for r in finales if r["train_score_delta"] > 0]
    peor_test = [r for r in mueven if r["test_delta"] < 0]
    peor_esp = [r for r in mueven if r["space_delta"] < 0]

    print()
    print(f"  Al pasar de {budgets[0]} a {mayor} arranques, sobre "
          f"{len(finales)} particiones:")
    print(f"    el mejor train mejora en          {len(mueven)}/{len(finales)}")
    print(f"    de esas, el test EMPEORA en       {len(peor_test)}/{len(mueven) or 1}")
    print(f"    de esas, el espacio EMPEORA en    {len(peor_esp)}/{len(mueven) or 1}")
    if mueven:
        print(f"    media del delta en test           "
              f"{statistics.mean([r['test_delta'] for r in mueven]):+.4f}")
        print(f"    media del delta en espacio        "
              f"{statistics.mean([r['space_delta'] for r in mueven]):+.4f}")
    print()
    if len(mueven) == 0:
        print("  El mejor train NO se mueve en ninguna particion. Es evidencia")
        print("  de convergencia, no prueba: sin optimo conocido sobre esta")
        print("  instancia, nada descarta un arranque 258.")
    elif len(peor_test) == len(mueven) and len(mueven) > 1:
        print("  LA INVERSION SE REPITE: donde el train mejora, el test empeora.")
    elif len(peor_test) > 0:
        print("  LA INVERSION APARECE, pero no en todas: ver la tabla.")
    else:
        print("  El train mejora sin que el test empeore.")
    print()
    print(f"  MULTISTART_STARTS sigue en {MULTISTART_STARTS}, y no por esto:")
    print("  por estar declarado de antemano. Elegirlo leyendo el test seria")
    print("  la regla 6 con el signo cambiado.")

    return {"rows": rows, "budgets": list(budgets), "splits": splits,
            "best_train_moves": len(mueven) > 0,
            "n_splits_train_improves": len(mueven),
            "n_splits_test_worsens": len(peor_test),
            "n_splits_space_worsens": len(peor_esp),
            "mean_test_delta_where_train_improves": (
                round(statistics.mean([r["test_delta"] for r in mueven]), 4)
                if mueven else None),
            "mean_space_delta_where_train_improves": (
                round(statistics.mean([r["space_delta"] for r in mueven]), 4)
                if mueven else None)}


# ---------------------------------------------------------------------------
# P3 — harness parity. No figures.
# ---------------------------------------------------------------------------

def checks(inst, espacio):
    """Three checks against published numbers. If any fails, the instances or
    the surfaces are not the record's and nothing downstream is comparable."""
    ids, action, born = inst["ids"], inst["action"], inst["born"]
    rules, matched, truth = inst["rules"], inst["matched"], inst["truth"]
    tr0, te0 = inst["splits"][0]
    sM, sW, sfull, sn = espacio["masks"]
    verdicts = {}

    print("=" * 78)
    print("P3 · PARIDAD DEL BANCO DE PRUEBAS  (sin cifras nuevas)")
    print("=" * 78)

    a = greedy_del_registro(rules, matched, truth, action, tr0)
    b = greedy_order(rules, matched, truth, action, tr0)
    verdicts["voraz de budget_and_balance == voraz de order_search"] = (a == b)
    print(f"  1. voraz de budget_and_balance == voraz de order_search   "
          f"{'SI' if a == b else 'NO':>6}")

    M, W, full = build_masks(ids, matched, truth, action, tr0)
    tM, tW, tfull = build_masks(ids, matched, truth, action, te0)
    t0 = time.time()
    best, st = search(ids, a, M, W, full)
    obtenido = {
        "voraz test": round(score_order(a, tM, tW, tfull) / len(te0), 4),
        "busqueda local test": round(
            score_order(best, tM, tW, tfull) / len(te0), 4),
        "longitud de cobertura": coverage_length(a, M, full),
    }
    print(f"\n  2. particion 0, fraccion 100%, pool puro   ({time.time()-t0:.0f}s)")
    print(f"     {'magnitud':<26}{'publicado':>11}{'hoy':>11}")
    for k, v in obtenido.items():
        verdicts[k] = (v == ESPERADO[k])
        fmt = "{:>11.4f}" if isinstance(v, float) else "{:>11d}"
        print(f"     {k:<26}" + fmt.format(ESPERADO[k]) + fmt.format(v)
              + f"{'SI' if verdicts[k] else 'NO':>7}")

    born_order = sorted(ids, key=lambda r: born[r])
    verdicts["sorted(ids) es born_at"] = (sorted(ids) == born_order)
    v = round(score_order(born_order, sM, sW, sfull) / sn, 4)
    verdicts["born_at espacio"] = (v == ESPERADO["born_at espacio"])
    print(f"\n  3. banco del espacio exhaustivo ({sn:,} casos)")
    print(f"     {'born_at sobre el espacio':<26}"
          f"{ESPERADO['born_at espacio']:>11.4f}{v:>11.4f}"
          f"{'SI' if verdicts['born_at espacio'] else 'NO':>7}")

    todo = all(verdicts.values())
    print(f"\n  P3: {'PASA' if todo else 'NO PASA'}")
    if not todo:
        print("  Las instancias o las superficies no son las del registro.")
    return todo, verdicts


# ---------------------------------------------------------------------------
# §1 — the label-budget curve
# ---------------------------------------------------------------------------

def seccion_presupuesto(inst, espacio, rows, budget_rows, save):
    print()
    print("=" * 78)
    print("1. PRESUPUESTO DE ETIQUETAS  (muestreo aleatorio simple del train)")
    print("=" * 78)
    print("  tres columnas: publicado (voraz, pre-desempate) · voraz de hoy · "
          "busqueda local")
    print(f"  {'frac':>6}{'etiq':>7}{'PUBLICADO':>11}{'VORAZ HOY':>11}"
          f"{'BL HOY':>10}{'desv BL':>9}{'min BL':>9}{'max BL':>9}"
          f"{'espacio':>9}{'delta':>8}{'seg':>7}")

    test_masks = {}
    for s in range(N_SPLITS):
        _tr, te = inst["splits"][s]
        test_masks[s] = build_masks(inst["ids"], inst["matched"],
                                    inst["truth"], inst["action"], te)

    for frac in FRACTIONS:
        for s in range(N_SPLITS):
            for d in range(1 if frac == 1.0 else N_DRAWS):
                rows.append(run_config(inst, espacio, frac, s, d,
                                       test_masks[s]))
        agg = aggregate(rows, frac)
        budget_rows.append(agg)
        pub = PUBLICADO[round(frac, 2)]
        print(f"  {frac:>5.0%}{agg['labels']:>7}{pub['test_mean']:>11.4f}"
              f"{agg['greedy']['test_mean']:>11.4f}"
              f"{agg['ls']['test_mean']:>10.4f}{agg['ls']['test_sd']:>9.4f}"
              f"{agg['ls']['test_min']:>9.4f}{agg['ls']['test_max']:>9.4f}"
              f"{agg['ls']['space_mean']:>9.4f}"
              f"{agg['delta_test_mean']:>+8.4f}{agg['seconds']:>7.0f}")
        save()
    return test_masks


# ---------------------------------------------------------------------------
# §2 — the balanced objective
# ---------------------------------------------------------------------------

def seccion_balanceado(inst, espacio, obj_rows, per_class_split0, save):
    ids, action, matched = inst["ids"], inst["action"], inst["matched"]
    rules, truth = inst["rules"], inst["truth"]
    sM, sW, sfull, sn = espacio["masks"]
    wt_esp, L_esp, n_esp = espacio["weights"]

    def macro_espacio(order):
        """Macro-recall over the exhaustive space: the weighted score over its
        maximum. The corpus is long-tailed and the space uniform, so this is
        where a balanced objective and a total one have to diverge."""
        return score_order(order, sM, sW, sfull, wt_esp) / (L_esp * len(n_esp))

    print()
    print("=" * 78)
    print("2. OBJETIVO BALANCEADO POR CLASE  (supervision completa del train)")
    print("=" * 78)

    for s in range(N_SPLITS):
        tr, te = inst["splits"][s]
        M, W, full = build_masks(ids, matched, truth, action, tr)
        tM, tW, tfull = build_masks(ids, matched, truth, action, te)
        weights, wt, _counts, _L = balanced_objective(ids, action, truth, tr)

        for objetivo in ("total", "balanced"):
            t0 = time.time()
            w_greedy = None if objetivo == "total" else weights
            w_search = None if objetivo == "total" else wt
            greedy = greedy_del_registro(rules, matched, truth, action, tr,
                                         weights=w_greedy)
            best, st = search(ids, greedy, M, W, full, wt=w_search)
            dt = time.time() - t0

            fila = {"split": s, "objective": objetivo,
                    "labels": len(tr), "seconds": round(dt, 1)}
            for quien, order in (("greedy", greedy), ("ls", best)):
                _t, _ok, _c, bal = per_class(order, matched, truth, action, te)
                fila[f"{quien}_e2e_test"] = round(
                    score_order(order, tM, tW, tfull) / len(te), 4)
                fila[f"{quien}_balanced_acc"] = round(bal, 4)
                fila[f"{quien}_e2e_space"] = round(
                    score_order(order, sM, sW, sfull) / sn, 4)
                fila[f"{quien}_macro_space"] = round(macro_espacio(order), 4)
            fila.update({f"ls_{k}": v for k, v in start_spread(st).items()})
            obj_rows.append(fila)

            if s == 0:
                t, ok, cc, _ = per_class(greedy, matched, truth, action, te)
                _t2, ok2, _c2, _ = per_class(best, matched, truth, action, te)
                for c in t:
                    d = per_class_split0.setdefault(
                        c, {"test": t[c], "ceiling": cc.get(c, 0)})
                    d[f"greedy_{objetivo}"] = ok.get(c, 0)
                    d[f"ls_{objetivo}"] = ok2.get(c, 0)
        save()
        print(f"  particion {s} lista "
              f"({sum(r['seconds'] for r in obj_rows if r['split'] == s):.0f}s)")

    # ------------------------------------------------------------- aggregate
    print()
    print(f"  {'objetivo':<12}{'quien':<8}{'e2e test':>10}{'bal. test':>11}"
          f"{'e2e esp':>10}{'MACRO esp':>11}")
    resumen = {}
    for objetivo in ("total", "balanced"):
        sub = [r for r in obj_rows if r["objective"] == objetivo]
        resumen[objetivo] = {}
        for quien in ("greedy", "ls"):
            d = {k: round(statistics.mean([r[f"{quien}_{k}"] for r in sub]), 4)
                 for k in ("e2e_test", "balanced_acc", "e2e_space",
                           "macro_space")}
            resumen[objetivo][quien] = d
            print(f"  {objetivo:<12}{quien:<8}{d['e2e_test']:>10.4f}"
                  f"{d['balanced_acc']:>11.4f}{d['e2e_space']:>10.4f}"
                  f"{d['macro_space']:>11.4f}")

    for quien in ("greedy", "ls"):
        coste = (resumen["total"][quien]["e2e_test"]
                 - resumen["balanced"][quien]["e2e_test"])
        gana = (resumen["balanced"][quien]["balanced_acc"]
                - resumen["total"][quien]["balanced_acc"])
        gana_esp = (resumen["balanced"][quien]["macro_space"]
                    - resumen["total"][quien]["macro_space"])
        resumen.setdefault("balancing", {})[quien] = {
            "cost_e2e_test": round(coste, 4),
            "gain_balanced_acc_test": round(gana, 4),
            "gain_macro_space": round(gana_esp, 4),
        }
        print(f"\n  {quien}: balancear cuesta {coste:+.4f} en e2e test, "
              f"gana {gana:+.4f} en acierto balanceado")
        print(f"  {' ' * len(quien)}  y {gana_esp:+.4f} en macro-recall sobre "
              f"el espacio exhaustivo")
    print(f"\n  el registro publica: coste -0.0557 · ganancia +0.1695 (voraz)")
    return resumen


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    solo_checks = "--checks" in argv
    solo_arranques = "--start-budget" in argv
    groups = list(GROUPS)
    if "--sections" in argv:
        groups = [g.strip() for g in argv[argv.index("--sections") + 1].split(",")]
        malos = [g for g in groups if g not in GROUPS]
        if malos:
            print(f"secciones desconocidas: {malos}; validas: {list(GROUPS)}")
            return 2
    name = record_name(groups)
    t_start = time.time()

    print("=" * 78)
    print("PASO 3 DE LA AUDITORIA — PRESUPUESTO DE ETIQUETAS Y OBJETIVO "
          "BALANCEADO")
    print("=" * 78)
    print(f"  optimizador: {DECLARED_NEIGHBOURHOOD}, semilla {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} arranques + el voraz")
    print(f"  fracciones {FRACTIONS} · {N_SPLITS} particiones · "
          f"{N_DRAWS} extracciones · pool {POOL}")
    print(f"  secciones: {groups}  ->  {name}")
    print(f"  {describe()}")

    inst = load_instance()
    t0 = time.time()
    spools = space_pools(inst["ids"], inst["conds"], inst["action"],
                         inst["below"])
    espacio = {"masks": spools[POOL],
               "weights": weights_from_counts(inst["ids"], inst["action"],
                                              class_counts(all_cases()))}
    print(f"  mascaras y pesos del espacio en {time.time()-t0:.1f}s")
    print()

    ok, verdicts = checks(inst, espacio)
    if not ok:
        print("\n  Se para: P3 es bloqueante.")
        return 1
    if solo_checks:
        print(f"\n  coste total: {time.time() - t_start:.0f}s")
        return 0

    if solo_arranques:
        d = start_budget_check(inst, espacio)
        OUT.mkdir(exist_ok=True)
        (OUT / "start_budget_check.json").write_text(json.dumps({
            "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                                multistart_seed=MULTISTART_SEED,
                                multistart_starts=MULTISTART_STARTS,
                                budgets=list(BUDGETS)),
            "what": "diagnostic, not a tuning: whether the best train score at "
                    "full supervision moves when the multi-start budget is "
                    "doubled and quadrupled, over all five splits, and what "
                    "happens to the two evaluation surfaces where it does. "
                    "MULTISTART_STARTS is unchanged, because it was declared "
                    "before the runs that used it and for no reason measured "
                    "here.",
            "surfaces": ["corpus test", "espacio exhaustivo"],
            "pool": POOL, "fraction": 1.0,
            "n_rules": len(inst["ids"]), "n_space": espacio["masks"][3],
            **d,
            "seconds_total": round(time.time() - t_start, 1),
        }, indent=2))
        print(f"\n  coste total: {time.time() - t_start:.0f}s")
        print(f"-> {OUT/'start_budget_check.json'}")
        return 0

    rows, budget_rows, obj_rows = [], [], []
    per_class_split0, resumen = {}, {}

    def save():
        OUT.mkdir(exist_ok=True)
        payload = {
            "_env": environment(n_splits=N_SPLITS, n_draws=N_DRAWS,
                                fractions=FRACTIONS,
                                neighbourhood=DECLARED_NEIGHBOURHOOD,
                                multistart_seed=MULTISTART_SEED,
                                multistart_starts=MULTISTART_STARTS),
            "what": "step 3 of the rungs 3/4 audit: the label-budget curve and "
                    "the balanced objective, re-measured with the declared "
                    "multi-start local search",
            "pool": POOL,
            "surfaces": ["corpus test", "espacio exhaustivo"],
            "train_is": "el subconjunto etiquetado, que es lo que ve el objetivo",
            "groups_run": groups_done, "groups_requested": groups,
            "n_rules": len(inst["ids"]), "n_cases": len(inst["corpus"]),
            "n_space": espacio["masks"][3],
            "references": dict(REFERENCIAS,
                               **{"publicado pre-desempate": PUBLICADO,
                                  "publicado objetivos": PUBLICADO_OBJETIVO}),
            "label_budget": budget_rows,
            "label_budget_runs": rows,
            "objective_comparison": resumen,
            "objective_runs": obj_rows,
            "per_class_split0": per_class_split0,
            "checks": checks_out,
            "seconds_total": round(time.time() - t_start, 1),
        }
        (OUT / name).write_text(json.dumps(payload, indent=2))

    groups_done = []
    checks_out = {"P3": verdicts}

    if "budget" in groups:
        seccion_presupuesto(inst, espacio, rows, budget_rows, save)
        groups_done.append("budget")
        save()

    if "balanced" in groups:
        resumen.update(seccion_balanceado(inst, espacio, obj_rows,
                                          per_class_split0, save))
        groups_done.append("balanced")
        save()

    # ------------------------------------------------- P5 identity and P-a
    if "budget" in groups and "balanced" in groups:
        iguales = []
        for r in obj_rows:
            if r["objective"] != "total":
                continue
            m = next((x for x in rows if x["fraction"] == 1.0
                      and x["split"] == r["split"] and x["draw"] == 0), None)
            iguales.append(m is not None
                           and m["greedy_test"] == r["greedy_e2e_test"]
                           and m["ls_test"] == r["ls_e2e_test"])
        checks_out["P5 identidad total == fraccion 1.0"] = all(iguales)
        print(f"\n  identidad §2 total == §1 fraccion 100%: "
              f"{'SI' if all(iguales) else 'NO'}")

    if budget_rows:
        fila = budget_rows[0]
        checks_out["P-a gate"] = {
            "esperado": REFERENCIAS[
                "ls supervision plena, pool puro (order_search_ls)"],
            "obtenido": fila["ls"]["test_mean"],
            "coincide": abs(fila["ls"]["test_mean"] - 0.8530) <= 0.0001,
        }
    save()

    print(f"\n  coste total: {time.time() - t_start:.0f}s")
    print(f"-> {OUT/name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
