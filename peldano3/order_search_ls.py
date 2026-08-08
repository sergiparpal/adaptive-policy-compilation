"""
STEP 1 of the audit: rung 3's order search, run with the declared optimizer.

--------------------------------------------------------------------------
WHAT CHANGES AND WHAT DOES NOT
--------------------------------------------------------------------------
Only the search changes. Corpus of 2000 with seed 17, the same five splits
(grouped by case identity, stratified by action, 50/50), the same two pools —
first-match-wins and subsumption-undefeated — and the same objective, so that
every number here is comparable with `results3/order_search.json`.

What replaces the decision-list greedy is the multi-start local search declared
in `local_search.py`: seed 17, 64 random starts plus the greedy at position 0,
neighbourhood `move+swap`. The greedy is still computed and still reported,
because the point of the audit is the difference between the two.

--------------------------------------------------------------------------
TWO INSTANCES, AND WHY THE SECOND ONE IS HERE
--------------------------------------------------------------------------
Step 0 found that the corpus cannot certify an optimum: orders scoring a
perfect 1.0000 over its 2000 cases scored 0.9455 and 0.9299 over the exhaustive
space of 134,400. Rungs 3 and 4 were measured on the corpus, so anything the
exhaustive space can say about these 577 rules is worth more than the corpus
figure.

Three things it can say, and they cost very different amounts:

  bound        what fraction of the WHOLE case space some matching rule gets
               right. It is the honest version of rung 3's 0.9010, which was
               computed over a 2000-draw sample of a skewed distribution.
  transfer     the orders searched on corpus train, scored over the whole
               space. Cheap, and it measures whether the order recovers the
               POLICY or only the sample.
  direct       searching the order over the whole space. This is the analogue
               of rung 3's "search over the test set itself" diagnostic, which
               is what separates search weakness from failure to generalize.
               It costs ~3 h against ~2 min for everything else, so it lives
               behind --full-space-search and its own record.

Usage:  python3 -m peldano3.order_search_ls
        python3 -m peldano3.order_search_ls --full-space-search
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

from harness.ceiling_check import all_cases
from harness.domain import ACTIONS
from harness.hidden_policy import true_action
from harness.provenance import describe, environment
from peldano2.engine2 import Space
from peldano3.order_search import (build_tables, load, split, subsumption_below)

from .local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                           MULTISTART_STARTS, build_masks, coverage_length,
                           declared_starts, greedy_order_from_masks,
                           multistart, random_order, score_order)

OUT = Path("results3")
N_SPLITS = 5
N_RANDOM = 50
POOLS = ("puro", "hibrido")

# The record this is measured against (`results3/FINDINGS3.md`, pre-tie-break).
REF = {"voraz test (post arreglo del desempate)": 0.7713,
       "cota por cobertura, corpus": 0.9010,
       "born_at": 0.5216, "aleatorio": 0.4227}


# ---------------------------------------------------------------------------
# Pools as masks
# ---------------------------------------------------------------------------

def space_pools(ids, conds, action, below):
    """
    The two pools over the exhaustive space, as bitmasks.

    The undefeated pool comes out without touching a single case one at a time:
    rule A survives on case c iff c is in ext(A) and in no ext(B) for the B that
    subsumption puts strictly below A. `tests/test_local_search.py` checks this
    against `order_search.build_tables`, which is what computed the record.
    """
    space = Space()
    bits = {a: bytearray(space.n) for a in ACTIONS}
    for i, case in enumerate(all_cases()):
        bits[true_action(case)][i] = 1
    tmask = {a: int("".join(map(str, b)), 2) for a, b in bits.items()}

    ext = {rid: space.extension(conds[rid]) for rid in ids}
    pools = {}
    for name in POOLS:
        if name == "puro":
            M = dict(ext)
        else:
            M = {}
            for rid in ids:
                dominated = 0
                for b in below[rid]:
                    dominated |= ext[b]
                M[rid] = ext[rid] & ~dominated
        W = {rid: M[rid] & tmask[action[rid]] for rid in ids}
        pools[name] = (M, W, space.full, space.n)
    return pools


def bound_of(M, W, full, n):
    """Cases some rule in the pool gets right: the exact upper bound of any
    order. Not a demonstrated optimum — see the erratum of 2026-08-06."""
    reach = 0
    for rid in W:
        reach |= W[rid]
    covered = 0
    for rid in M:
        covered |= M[rid]
    return reach.bit_count() / n, (n - covered.bit_count())


def tail_key_factory(M, W, born):
    def prec(rid):
        w = W[rid].bit_count()
        miss = (M[rid] ^ W[rid]).bit_count()
        return (w / (w + miss)) if (w + miss) else -1.0
    return lambda rid: (-prec(rid), born[rid])


def search(ids, M, W, full, born):
    """Greedy, then the declared multi-start from it. Returns both."""
    greedy = greedy_order_from_masks(ids, M, W, full,
                                     tail_key=tail_key_factory(M, W, born))
    best, st = multistart(declared_starts(ids, first=greedy), M, W, full,
                          neighbourhood=DECLARED_NEIGHBOURHOOD)
    return greedy, best, st


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    full_space_search = "--full-space-search" in argv

    t_start = time.time()
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ids = [r["rule_id"] for r in rules]
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    corpus_pool = {"puro": matched, "hibrido": undef}

    print("=" * 78)
    print("PASO 1 DE LA AUDITORIA — LAS 577 REGLAS CON EL OPTIMIZADOR DECLARADO")
    print("=" * 78)
    print(f"  reglas {len(ids)} · corpus {len(corpus)} · semilla 17 · "
          f"{N_SPLITS} particiones")
    print(f"  optimizador: {DECLARED_NEIGHBOURHOOD}, semilla {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} arranques + el voraz")
    print(f"  {describe()}")

    spools = space_pools(ids, conds, action, below)
    sn = spools["puro"][3]

    print()
    print("=" * 78)
    print("COTAS POR COBERTURA — corpus contra espacio exhaustivo")
    print("=" * 78)
    bounds = {}
    print(f"  {'pool':<10}{'cota corpus':>14}{'cota espacio':>15}"
          f"{'sin regla, esp.':>18}")
    for name in POOLS:
        cM, cW, cfull = build_masks(ids, corpus_pool[name], truth, action,
                                    list(range(len(corpus))))
        bc, _ = bound_of(cM, cW, cfull, len(corpus))
        bs, nomatch = bound_of(*spools[name])
        bounds[name] = {"corpus": round(bc, 4), "espacio": round(bs, 4),
                        "espacio_sin_regla": nomatch}
        print(f"  {name:<10}{bc:>14.4f}{bs:>15.4f}{nomatch:>18,}")
    print("\n  el registro publica 0.9010 para el pool puro sobre el corpus")

    # ------------------------------------------------------- SEARCH PER SPLIT
    print()
    print("=" * 78)
    print("BUSQUEDA POR PARTICION — el voraz del registro contra el optimizador")
    print("=" * 78)
    rows = []
    for s in range(N_SPLITS):
        tr, te = split(corpus, truth, seed=17 + s)
        for name in POOLS:
            pool = corpus_pool[name]
            M, W, full = build_masks(ids, pool, truth, action, tr)
            tM, tW, tfull = build_masks(ids, pool, truth, action, te)
            t0 = time.time()
            greedy, best, st = search(ids, M, W, full, born)
            dt = time.time() - t0
            sM, sW, sfull, _ = spools[name]
            row = {
                "split": s, "seed": 17 + s, "pool": name,
                "n_train": len(tr), "n_test": len(te),
                "greedy_train": round(score_order(greedy, M, W, full) / len(tr), 4),
                "greedy_test": round(score_order(greedy, tM, tW, tfull) / len(te), 4),
                "greedy_space": round(score_order(greedy, sM, sW, sfull) / sn, 4),
                "ls_train": round(st["best_score"] / len(tr), 4),
                "ls_test": round(score_order(best, tM, tW, tfull) / len(te), 4),
                "ls_space": round(score_order(best, sM, sW, sfull) / sn, 4),
                "best_from": st["best_from"],
                "best_from_index": st["best_from_index"],
                "coverage_length": coverage_length(greedy, M, full),
                "seconds": round(dt, 1),
            }
            row["greedy_gap"] = round(row["greedy_train"] - row["greedy_test"], 4)
            row["ls_gap"] = round(row["ls_train"] - row["ls_test"], 4)
            rows.append(row)
        print(f"  particion {s} lista ({sum(r['seconds'] for r in rows if r['split']==s):.0f}s)")

    for name in POOLS:
        sub = [r for r in rows if r["pool"] == name]
        print()
        print(f"  POOL {name.upper()}")
        print(f"    {'part':>5}{'voraz tr':>10}{'voraz te':>10}{'  |':>3}"
              f"{'BL tr':>9}{'BL te':>9}{'BL gap':>9}{'  |':>3}"
              f"{'voraz esp':>11}{'BL esp':>9}{'desde':>13}")
        for r in sub:
            print(f"    {r['split']:>5}{r['greedy_train']:>10.4f}"
                  f"{r['greedy_test']:>10.4f}{'  |':>3}{r['ls_train']:>9.4f}"
                  f"{r['ls_test']:>9.4f}{r['ls_gap']:>9.4f}{'  |':>3}"
                  f"{r['greedy_space']:>11.4f}{r['ls_space']:>9.4f}"
                  f"{r['best_from']:>13}")
        for k in ("greedy_train", "greedy_test", "ls_train", "ls_test",
                  "ls_gap", "greedy_space", "ls_space"):
            v = [r[k] for r in sub]
            print(f"    {k:<16}{statistics.mean(v):>9.4f} ± "
                  f"{statistics.pstdev(v):.4f}")

    # ------------------------------------------------------------ REFERENCES
    print()
    print("=" * 78)
    print("CONTRA LAS REFERENCIAS DEL REGISTRO (test, pool puro)")
    print("=" * 78)
    pure = [r for r in rows if r["pool"] == "puro"]
    g_test = statistics.mean([r["greedy_test"] for r in pure])
    l_test = statistics.mean([r["ls_test"] for r in pure])
    tr0, te0 = split(corpus, truth, seed=17)
    tM, tW, tfull = build_masks(ids, matched, truth, action, te0)
    born_order = sorted(ids, key=lambda r: born[r])
    rnd = [score_order(random_order(ids, seed=k), tM, tW, tfull) / len(te0)
           for k in range(N_RANDOM)]
    print(f"  {'orden aleatorio (media de 50)':<44}{statistics.mean(rnd):>9.4f}")
    print(f"  {'orden de llegada (born_at)':<44}"
          f"{score_order(born_order, tM, tW, tfull)/len(te0):>9.4f}")
    print(f"  {'voraz del registro (post arreglo)':<44}{g_test:>9.4f}")
    print(f"  {'BUSQUEDA LOCAL MULTI-ARRANQUE':<44}{l_test:>9.4f}")
    print(f"  {'cota por cobertura, corpus':<44}{bounds['puro']['corpus']:>9.4f}")
    print(f"  {'cota por cobertura, espacio exhaustivo':<44}"
          f"{bounds['puro']['espacio']:>9.4f}")
    gap_total = bounds["puro"]["corpus"] - REF["voraz test (post arreglo del desempate)"]
    recovered = l_test - REF["voraz test (post arreglo del desempate)"]
    print(f"\n  hueco del registro (0.9010 - 0.7713) = {gap_total:.4f}")
    print(f"  recuperado por el optimizador          = {recovered:+.4f}"
          f"  ({recovered/gap_total:.0%} del hueco)")

    payload = {
        "_env": environment(n_splits=N_SPLITS, n_random=N_RANDOM,
                            neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS),
        "what": "step 1 of the rung 3/4 audit: the 577 rules with the declared "
                "multi-start local search, same protocol as order_search.py",
        "n_rules": len(ids), "n_cases": len(corpus), "n_space": sn,
        "bounds": bounds, "references": REF,
        "splits": rows,
        "summary": {name: {k: round(statistics.mean(
            [r[k] for r in rows if r["pool"] == name]), 4)
            for k in ("greedy_train", "greedy_test", "greedy_space",
                      "ls_train", "ls_test", "ls_space", "ls_gap")}
            for name in POOLS},
        "gap_recovered_pure_test": round(recovered, 4),
        "seconds_total": round(time.time() - t_start, 1),
    }

    # ------------------------------------------- DIRECT SEARCH OVER THE SPACE
    if full_space_search:
        print()
        print("=" * 78)
        print("BUSQUEDA DIRECTA SOBRE EL ESPACIO EXHAUSTIVO (sin particion)")
        print("=" * 78)
        print("  Es el analogo de 'buscar sobre el propio test' del peldano 3:")
        print("  separa debilidad de la busqueda de fallo de generalizacion.")
        direct = {}
        for name in POOLS:
            M, W, full, n = spools[name]
            t0 = time.time()
            greedy, best, st = search(ids, M, W, full, born)
            dt = time.time() - t0
            direct[name] = {
                "greedy": round(score_order(greedy, M, W, full) / n, 4),
                "local_search": round(st["best_score"] / n, 4),
                "bound": bounds[name]["espacio"],
                "best_from": st["best_from"],
                "best_from_index": st["best_from_index"],
                "seconds": round(dt, 1),
            }
            d = direct[name]
            print(f"  {name:<10}voraz {d['greedy']:.4f}   "
                  f"busqueda local {d['local_search']:.4f}   "
                  f"cota {d['bound']:.4f}   "
                  f"resto {d['bound']-d['local_search']:.4f}   "
                  f"({d['seconds']:.0f}s)")
        payload["full_space_direct"] = direct
        OUT.mkdir(exist_ok=True)
        (OUT / "order_search_ls_fullspace.json").write_text(
            json.dumps(payload, indent=2))
        print(f"\n-> {OUT/'order_search_ls_fullspace.json'}")
        return 0

    OUT.mkdir(exist_ok=True)
    (OUT / "order_search_ls.json").write_text(json.dumps(payload, indent=2))
    print(f"\n  coste total: {payload['seconds_total']:.0f}s")
    print(f"-> {OUT/'order_search_ls.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
