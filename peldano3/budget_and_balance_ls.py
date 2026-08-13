"""
STEP 3 OF THE AUDIT — `budget_and_balance` with the audited optimizer.

--------------------------------------------------------------------------
WHAT IS IN THIS FILE TODAY, AND WHAT IS NOT
--------------------------------------------------------------------------
Phase P3 of `PLAN_BUDGET_LS.md`: the harness, and the parity checks that say
the harness is the record's. The label-budget curve (P4) and the balanced
objective (P5) are NOT here yet — §0 of the plan is the prediction, it carries
no signature, and hard rule 2 of `CLAUDE.md` makes predictions Sergi's.

The harness lives here rather than in a scratch script on purpose: P3 exists to
validate the harness P4 will use, and a parity check run against different code
would measure nothing. It is the same reason `optimizer_check` validates the
optimizer that `order_search_ls` then runs.

--------------------------------------------------------------------------
WHAT CHANGES AND WHAT DOES NOT
--------------------------------------------------------------------------
Only the optimizer: the decision-list greedy becomes the multi-start local
search declared in `local_search.py` — seed 17, 64 random starts plus the
record's greedy at index 0, neighbourhood `move+swap`.

Everything else is the record's and is checked to be: corpus of 2000 at seed
17, the five splits grouped by case identity and stratified by action, the pure
pool, the fractions, the draw seeds, simple random subsampling — never
stratified, since stratifying needs the labels being rationed — and evaluation
always over the whole test half.

--------------------------------------------------------------------------
THE OLD RECORD IS NOT TOUCHED
--------------------------------------------------------------------------
`results3/budget_and_balance.json` is read-only for this work. It is
deliberately pre-tie-break, so its numbers stay reproducible beside the new
ones, and `python3 -m peldano3.budget_and_balance` is NEVER run: it has no
guard and dumps over that record on finishing. Greedy-today is obtained by
importing `budget_and_balance.greedy` and calling it, which is the discipline
the test suite already follows.

Usage:  python3 -m peldano3.budget_and_balance_ls --checks
"""

from __future__ import annotations

import random
import statistics
import sys
import time
from collections import Counter

from peldano3.budget_and_balance import FRACTIONS, N_DRAWS, N_SPLITS
from peldano3.budget_and_balance import greedy as greedy_del_registro
from peldano3.order_search import (build_tables, greedy_order, load, split,
                                   subsumption_below)
from peldano3.order_search_ls import space_pools

from .local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                           MULTISTART_STARTS, build_masks, coverage_length,
                           declared_starts, multistart, score_order,
                           weights_from_counts)

POOL = "puro"

# The record every check below is measured against: `results3/order_search_ls.
# json`, splits[0], pool puro — and the born_at figure of the FINDINGS3 erratum
# of 2026-08-08. They are constants because a check that reads its expectation
# out of the file it is checking is not a check.
ESPERADO = {
    "voraz test": 0.7487,
    "busqueda local test": 0.8472,
    "longitud de cobertura": 559,
    "born_at espacio": 0.3148,
}


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

    NOT from the masks. Over the 577 rules the masks give the per-class CEILING
    and not the class size: on split 0's train the union of the correct masks
    falls 98 cases short of 1005, and it falls short precisely in
    T3_ENGINEERING and ACCOUNT_MANAGER, where two thirds of the cases have no
    correct rule at all. Weighting by that would multiply the weight of exactly
    the classes the balanced objective exists to protect by about three, and
    would maximize something other than what the record maximized, while
    reporting it under the same name. `optimizer_check_wt.
    class_counts_from_masks` now refuses when its precondition fails, and this
    is the function that replaces it here.

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


# ---------------------------------------------------------------------------
# P3 — harness parity. No figures.
# ---------------------------------------------------------------------------

def checks(inst, spools):
    """
    Three checks against published numbers. If any fails, the instances or the
    surfaces are not the record's and nothing downstream would be comparable.
    """
    ids, action, born = inst["ids"], inst["action"], inst["born"]
    rules, matched, truth = inst["rules"], inst["matched"], inst["truth"]
    tr0, te0 = inst["splits"][0]
    verdicts = {}

    print("=" * 78)
    print("P3 · PARIDAD DEL BANCO DE PRUEBAS  (sin cifras nuevas)")
    print("=" * 78)

    # -- 1. two implementations of one algorithm must give one order ---------
    t0 = time.time()
    a = greedy_del_registro(rules, matched, truth, action, tr0)
    b = greedy_order(rules, matched, truth, action, tr0)
    igual = a == b
    verdicts["greedy_de_budget_and_balance_igual_a_order_search"] = igual
    print(f"  1. voraz de budget_and_balance == voraz de order_search   "
          f"{'SI' if igual else 'NO':>6}   ({time.time()-t0:.0f}s)")
    if not igual:
        d = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), None)
        print(f"     primera divergencia en la posicion {d}: {a[d]} vs {b[d]}")

    # -- 2. one configuration reproduced, digit for digit -------------------
    t0 = time.time()
    M, W, full = build_masks(ids, matched, truth, action, tr0)
    tM, tW, tfull = build_masks(ids, matched, truth, action, te0)
    _best, st = search(ids, a, M, W, full)
    obtenido = {
        "voraz test": round(score_order(a, tM, tW, tfull) / len(te0), 4),
        "busqueda local test": round(
            score_order(_best, tM, tW, tfull) / len(te0), 4),
        "longitud de cobertura": coverage_length(a, M, full),
    }
    print(f"\n  2. particion 0, fraccion 100%, pool puro                   "
          f"({time.time()-t0:.0f}s)")
    print(f"     {'magnitud':<26}{'publicado':>11}{'hoy':>11}{'':>7}")
    for k, v in obtenido.items():
        ok = v == ESPERADO[k]
        verdicts[k] = ok
        fmt = "{:>11.4f}" if isinstance(v, float) else "{:>11d}"
        print(f"     {k:<26}" + fmt.format(ESPERADO[k]) + fmt.format(v)
              + f"{'SI' if ok else 'NO':>7}")
    print(f"     mejor arranque: {st['best_from']} (indice "
          f"{st['best_from_index']})")

    # -- 3. the other surface, on its own reference -------------------------
    t0 = time.time()
    sM, sW, sfull, sn = spools[POOL]
    born_order = sorted(ids, key=lambda r: born[r])
    verdicts["sorted_ids_es_el_orden_born_at"] = sorted(ids) == born_order
    v = round(score_order(born_order, sM, sW, sfull) / sn, 4)
    ok = v == ESPERADO["born_at espacio"]
    verdicts["born_at espacio"] = ok
    print(f"\n  3. banco del espacio exhaustivo ({sn:,} casos)             "
          f"({time.time()-t0:.0f}s)")
    print(f"     {'born_at sobre el espacio':<26}"
          f"{ESPERADO['born_at espacio']:>11.4f}{v:>11.4f}"
          f"{'SI' if ok else 'NO':>7}")
    print(f"     {'sorted(ids) es born_at':<26}{'':>11}"
          f"{'SI' if verdicts['sorted_ids_es_el_orden_born_at'] else 'NO':>11}")

    todo = all(verdicts.values())
    print()
    print(f"  P3: {'PASA' if todo else 'NO PASA'}")
    if not todo:
        print("  Las instancias o las superficies no son las del registro.")
        print("  Nada aguas abajo seria comparable. Se para.")
    return todo, verdicts


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    t_start = time.time()

    print("=" * 78)
    print("PASO 3 DE LA AUDITORIA — PRESUPUESTO DE ETIQUETAS Y OBJETIVO "
          "BALANCEADO")
    print("=" * 78)
    print(f"  optimizador: {DECLARED_NEIGHBOURHOOD}, semilla {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} arranques + el voraz")
    print(f"  fracciones {FRACTIONS} · {N_SPLITS} particiones · "
          f"{N_DRAWS} extracciones · pool {POOL}")

    inst = load_instance()
    t0 = time.time()
    spools = space_pools(inst["ids"], inst["conds"], inst["action"],
                         inst["below"])
    print(f"  mascaras del espacio construidas en {time.time()-t0:.1f}s")
    print()

    ok, _verdicts = checks(inst, spools)
    print(f"\n  coste total: {time.time() - t_start:.0f}s")
    if not ok:
        return 1

    if "--checks" not in argv:
        print()
        print("  P4 (la curva) y P5 (el objetivo balanceado) no estan en este")
        print("  fichero todavia: la §0 del plan no lleva firma.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
