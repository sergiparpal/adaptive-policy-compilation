"""
PASO A del peldano 3: buscar el orden total que maximiza el acierto sobre el
corpus, con las 577 reglas que el LLM escribio en el peldano 1. Sin LLM.

--------------------------------------------------------------------------
EL TECHO, PRIMERO
--------------------------------------------------------------------------
Bajo primera-que-casa, el ganador de un caso es la regla de menor rango entre
las que lo casan. Luego un caso es GANABLE por algun orden sii alguna regla que
lo casa tiene la accion correcta. Si ninguna la tiene, ningun orden lo salva.
Ese conteo es exacto y no requiere buscar nada; acota todo lo demas.

Se calculan dos techos:
  * puro   : sobre las reglas que CASAN el caso
  * hibrido: sobre las reglas INVICTAS por subsuncion, que son las unicas que
             pueden ganar en el motor del peldano 2. Es <= el puro: la
             subsuncion puede eliminar de la puja a la unica regla correcta.

--------------------------------------------------------------------------
LA PARTICION
--------------------------------------------------------------------------
Agrupada por identidad de caso y estratificada por accion verdadera, 50/50.

  * AGRUPADA porque el 23,1% de los casos del corpus tiene un gemelo exacto.
    Una particion al azar pondria copias del mismo caso a ambos lados y el test
    premiaria memorizar. Todas las copias de un caso caen del mismo lado.
  * ESTRATIFICADA porque ONCALL_ESCALATION son 7 casos de 2000 y
    SECURITY_INCIDENT 20. Sin estratificar, una mitad puede quedarse sin
    ninguno y el test no mediria nada sobre ellos.
  * 50/50 porque con 577 reglas y 2000 casos el conjunto de busqueda ya es
    pequeño; recortarlo mas haria que el orden hallado fuese ruido.

FUGA QUE NINGUNA PARTICION DESHACE, y hay que declararla: las 577 reglas se
aprendieron sobre los 2000 casos (born_at va de 0 a 1998). El test no es datos
no vistos por las REGLAS; es datos no vistos por el ORDEN. Lo que este montaje
mide es el sobreajuste del orden, y solo eso. El gap real de un sistema
completo seria mayor.

--------------------------------------------------------------------------
EL METODO DE BUSQUEDA
--------------------------------------------------------------------------
Voraz de lista de decision: se elige repetidamente la regla que, colocada en la
siguiente posicion, maximiza (casos que gana - casos que pierde) entre los casos
de train aun no decididos; se coloca y se retiran los casos que casa.

Es el voraz clasico de construccion de listas de decision.

  GARANTIZA: optimalidad de cada paso local sobre los casos vivos, y que el
             orden producido es un orden total valido sobre las 577 reglas.
  NO GARANTIZA: nada global. El problema es de tipo minimo conjunto de arcos de
             retroceso; no hay razon de aproximacion conocida para este
             objetivo y no se ha corrido ninguna busqueda local despues.

Cola del orden: cuando ya no queda ningun caso de train por decidir, todas las
reglas restantes puntuan 0. Se ordenan por precision en train y luego por
born_at. Esa cola es arbitraria respecto a train y es una fuente conocida de
gap: en test si puede tocarle decidir.

Se comparan ademas tres ordenes que no buscan nada: born_at (orden de llegada),
precision en train, y aleatorio promediado.
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from harness.domain import generate_corpus
from harness.dsl import Condition
from harness.hidden_policy import true_action
from harness.provenance import environment
from peldano2.engine2 import Space, strictly_below   # reuso, no modificacion

OUT = Path("results3")
N_SPLITS = 5
N_RANDOM = 50


# ---------------------------------------------------------------------------
# Carga y estructura
# ---------------------------------------------------------------------------

def load():
    corpus = generate_corpus(2000, seed=17)
    d = json.loads(Path("results/llm_run.json").read_text())
    rules = d["rules"]
    space = Space()
    ext, conds = {}, {}
    for r in rules:
        cs = [Condition(c["attr"], c["op"], c["value"]) for c in r["conditions"]]
        conds[r["rule_id"]] = cs
        ext[r["rule_id"]] = space.extension(cs)
    return corpus, rules, ext, conds


def subsumption_below(rules, ext):
    """below[A] = {B : ext(B) ⊊ ext(A)}, con poda por popcount."""
    pc = {r["rule_id"]: ext[r["rule_id"]].bit_count() for r in rules}
    order = sorted(rules, key=lambda r: pc[r["rule_id"]])
    below = {r["rule_id"]: set() for r in rules}
    for i, b in enumerate(order):
        eb, pb = ext[b["rule_id"]], pc[b["rule_id"]]
        if eb == 0:
            continue
        for a in order[i + 1:]:
            if pc[a["rule_id"]] == pb:
                continue
            if (eb | ext[a["rule_id"]]) == ext[a["rule_id"]]:
                below[a["rule_id"]].add(b["rule_id"])
    return below


def build_tables(corpus, rules, conds, below):
    """Por caso: reglas que casan, reglas invictas por subsuncion, verdad."""
    matched, undef, truth = [], [], []
    for case in corpus:
        m = [r["rule_id"] for r in rules
             if all(c.holds(case) for c in conds[r["rule_id"]])]
        ids = set(m)
        u = [rid for rid in m if not (below[rid] & ids)]
        matched.append(m)
        undef.append(u)
        truth.append(true_action(case))
    return matched, undef, truth


# ---------------------------------------------------------------------------
# Techo
# ---------------------------------------------------------------------------

def ceiling(pool, truth, action, idxs):
    """Casos ganables por ALGUN orden: alguna regla del pool tiene la accion
    correcta. Exacto, sin busqueda."""
    ok = sum(1 for i in idxs if any(action[r] == truth[i] for r in pool[i]))
    return ok / len(idxs)


# ---------------------------------------------------------------------------
# Busqueda voraz
# ---------------------------------------------------------------------------

def greedy_order(rules, pool, truth, action, train_idx):
    """Voraz de lista de decision sobre `pool` (matched o undefeated)."""
    ids = [r["rule_id"] for r in rules]
    pos = {i: k for k, i in enumerate(train_idx)}
    win = {rid: 0 for rid in ids}
    lose = {rid: 0 for rid in ids}
    for i in train_idx:
        for rid in pool[i]:
            bit = 1 << pos[i]
            if action[rid] == truth[i]:
                win[rid] |= bit
            else:
                lose[rid] |= bit

    remaining = (1 << len(train_idx)) - 1
    left = set(ids)
    order = []
    while left and remaining:
        best, best_score = None, None
        # ARREGLO 2026-08-06: se itera sobre lista ORDENADA, no sobre el set.
        # Antes, el argmax recorria `left` directamente y el desempate quedaba
        # a merced del orden de iteracion de un set de cadenas, que depende de
        # PYTHONHASHSEED: la misma celda daba entre 0,5880 y 0,5991 segun el
        # hash. Ordenar por rule_id es determinista y, como los ids son R%04d
        # asignados por orden de nacimiento, equivale a desempatar por la regla
        # mas antigua. NO se han vuelto a correr los peldanos 3 y 4 con este
        # arreglo: se hara junto con un optimizador serio, para poder distinguir
        # si la fragilidad venia del desempate o del algoritmo.
        for rid in sorted(left):
            s = (win[rid] & remaining).bit_count() - (lose[rid] & remaining).bit_count()
            if best_score is None or s > best_score:
                best, best_score = rid, s
        order.append(best)
        left.discard(best)
        remaining &= ~(win[best] | lose[best])

    # cola: ya no queda nada por decidir en train. Precision en train, luego born_at.
    born = {r["rule_id"]: r["born_at"] for r in rules}
    def prec(rid):
        w, l = win[rid].bit_count(), lose[rid].bit_count()
        return (w / (w + l)) if (w + l) else -1.0
    order += sorted(left, key=lambda rid: (-prec(rid), born[rid]))
    return order


# ---------------------------------------------------------------------------
# Evaluacion
# ---------------------------------------------------------------------------

def evaluate(order, pool, truth, action, idxs):
    rank = {rid: k for k, rid in enumerate(order)}
    ok = 0
    for i in idxs:
        p = pool[i]
        if not p:
            continue
        w = min(p, key=lambda rid: rank[rid])
        if action[w] == truth[i]:
            ok += 1
    return ok / len(idxs)


def eval_specificity(rules, matched, truth, action, idxs):
    ncond = {r["rule_id"]: len(r["conditions"]) for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ok = 0
    for i in idxs:
        m = matched[i]
        if not m:
            continue
        top = max(ncond[r] for r in m)
        fin = [r for r in m if ncond[r] == top]
        if len({action[r] for r in fin}) > 1:
            continue                       # CONFLICT
        if action[min(fin, key=lambda r: born[r])] == truth[i]:
            ok += 1
    return ok / len(idxs)


def eval_subsumption(undef, truth, action, idxs):
    ok = 0
    for i in idxs:
        u = undef[i]
        if not u:
            continue
        if len({action[r] for r in u}) > 1:
            continue                       # CONFLICT
        if action[u[0]] == truth[i]:
            ok += 1
    return ok / len(idxs)


# ---------------------------------------------------------------------------
# Particion
# ---------------------------------------------------------------------------

def split(corpus, truth, seed):
    """Agrupada por identidad de caso, estratificada por accion, 50/50."""
    groups = defaultdict(list)
    for i, c in enumerate(corpus):
        groups[c.key()].append(i)
    by_action = defaultdict(list)
    for key, idxs in groups.items():
        by_action[truth[idxs[0]]].append(idxs)
    rng = random.Random(seed)
    train, test = [], []
    for act, gs in sorted(by_action.items()):
        gs = sorted(gs)
        rng.shuffle(gs)
        for k, g in enumerate(gs):
            (train if k % 2 == 0 else test).extend(g)
    return sorted(train), sorted(test)


# ---------------------------------------------------------------------------

def main() -> int:
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    allidx = list(range(len(corpus)))

    print("=" * 78)
    print("PELDANO 3 · PASO A — ORDEN POR BUSQUEDA SOBRE EL CORPUS")
    print("=" * 78)
    print(f"  reglas: {len(rules)}   casos: {len(corpus)}   semilla del corpus: 17")
    nomatch = sum(1 for i in allidx if not matched[i])
    noundef = sum(1 for i in allidx if not undef[i])
    print(f"  casos sin ninguna regla que los case: {nomatch} ({nomatch/2000:.1%})")

    # ------------------------------------------------------------ TECHO
    print()
    print("=" * 78)
    print("TECHO — maximo alcanzable por CUALQUIER orden (exacto, sin buscar)")
    print("=" * 78)
    ceil_pure = ceiling(matched, truth, action, allidx)
    ceil_hyb = ceiling(undef, truth, action, allidx)
    print(f"  techo PURO    (primera-que-casa)      {ceil_pure:.4f}")
    print(f"  techo HIBRIDO (subsuncion + orden)    {ceil_hyb:.4f}")
    print(f"  perdida por subsuncion                {ceil_pure - ceil_hyb:.4f}")
    print(f"  casos sin regla correcta que los case: "
          f"{round((1-ceil_pure)*2000)} de 2000")

    lost = Counter()
    for i in allidx:
        if not any(action[r] == truth[i] for r in matched[i]):
            lost[truth[i]] += 1
    tot = Counter(truth)
    print("\n  casos irrecuperables por clase (ningun orden los salva):")
    print(f"    {'clase':<24}{'corpus':>8}{'irrecup.':>10}{'%':>8}")
    for cls in sorted(tot, key=lambda k: -tot[k]):
        print(f"    {cls:<24}{tot[cls]:>8}{lost.get(cls,0):>10}"
              f"{100*lost.get(cls,0)/tot[cls]:>7.1f}%")

    # ------------------------------------------------- BUSQUEDA POR PARTICION
    print()
    print("=" * 78)
    print(f"BUSQUEDA CON PARTICION agrupada+estratificada 50/50 · {N_SPLITS} particiones")
    print("=" * 78)

    rows = []
    for s in range(N_SPLITS):
        tr, te = split(corpus, truth, seed=17 + s)
        row = {"split": s, "seed": 17 + s, "n_train": len(tr), "n_test": len(te)}
        for name, pool in (("puro", matched), ("hibrido", undef)):
            order = greedy_order(rules, pool, truth, action, tr)
            row[f"{name}_train"] = evaluate(order, pool, truth, action, tr)
            row[f"{name}_test"] = evaluate(order, pool, truth, action, te)
            row[f"{name}_gap"] = row[f"{name}_train"] - row[f"{name}_test"]
            row[f"{name}_ceil_train"] = ceiling(pool, truth, action, tr)
            row[f"{name}_ceil_test"] = ceiling(pool, truth, action, te)
            if s == 0:
                row[f"{name}_order"] = order
        rows.append(row)

    print(f"  {'part':>5}{'train':>9}{'test':>9}{'GAP':>9}   "
          f"{'train':>9}{'test':>9}{'GAP':>9}")
    print(f"  {'':>5}{'--- primera-que-casa ---':^27}   {'--- hibrido ---':^27}")
    for r in rows:
        print(f"  {r['split']:>5}{r['puro_train']:>9.4f}{r['puro_test']:>9.4f}"
              f"{r['puro_gap']:>9.4f}   {r['hibrido_train']:>9.4f}"
              f"{r['hibrido_test']:>9.4f}{r['hibrido_gap']:>9.4f}")
    for name in ("puro", "hibrido"):
        tr = [r[f"{name}_train"] for r in rows]
        te = [r[f"{name}_test"] for r in rows]
        gp = [r[f"{name}_gap"] for r in rows]
        print(f"\n  {name}:  train {statistics.mean(tr):.4f}±{statistics.pstdev(tr):.4f}"
              f"   test {statistics.mean(te):.4f}±{statistics.pstdev(te):.4f}"
              f"   GAP {statistics.mean(gp):.4f}±{statistics.pstdev(gp):.4f}")

    # --------------------------------------------------------- REFERENCIAS
    print()
    print("=" * 78)
    print("REFERENCIAS sobre la misma base y las mismas particiones")
    print("=" * 78)
    tr0, te0 = split(corpus, truth, seed=17)
    rng = random.Random(17)
    ids = [r["rule_id"] for r in rules]
    rand_test = []
    for _ in range(N_RANDOM):
        o = ids[:]
        rng.shuffle(o)
        rand_test.append(evaluate(o, matched, truth, action, te0))
    born_order = sorted(ids, key=lambda r: born[r])

    print(f"  {'estrategia':<40}{'train':>9}{'test':>9}")
    print(f"  {'orden buscado (voraz), puro':<40}"
          f"{rows[0]['puro_train']:>9.4f}{rows[0]['puro_test']:>9.4f}")
    print(f"  {'orden buscado (voraz), hibrido':<40}"
          f"{rows[0]['hibrido_train']:>9.4f}{rows[0]['hibrido_test']:>9.4f}")
    print(f"  {'orden de llegada (born_at), puro':<40}"
          f"{evaluate(born_order, matched, truth, action, tr0):>9.4f}"
          f"{evaluate(born_order, matched, truth, action, te0):>9.4f}")
    print(f"  {'orden aleatorio, puro (media de 50)':<40}{'—':>9}"
          f"{statistics.mean(rand_test):>9.4f}")
    print(f"  {'arbitraje por especificidad':<40}"
          f"{eval_specificity(rules, matched, truth, action, tr0):>9.4f}"
          f"{eval_specificity(rules, matched, truth, action, te0):>9.4f}")
    print(f"  {'subsuncion sola (conflicto = fallo)':<40}"
          f"{eval_subsumption(undef, truth, action, tr0):>9.4f}"
          f"{eval_subsumption(undef, truth, action, te0):>9.4f}")
    print(f"\n  referencias del peldano 1 sobre los 2000 casos:"
          f" especificidad 0.1825 · subsuncion 0.0375")
    print(f"  techo sobre los 2000: puro {ceil_pure:.4f} · hibrido {ceil_hyb:.4f}")

    OUT.mkdir(exist_ok=True)
    (OUT / "order_search.json").write_text(json.dumps({
        "_env": environment(n_splits=N_SPLITS, n_random=N_RANDOM),
        "n_rules": len(rules), "n_cases": len(corpus),
        "ceiling_pure": round(ceil_pure, 4), "ceiling_hybrid": round(ceil_hyb, 4),
        "cases_without_matching_rule": nomatch,
        "unrecoverable_by_class": dict(lost),
        "splits": [{k: v for k, v in r.items() if not k.endswith("_order")}
                   for r in rows],
        "summary": {name: {
            "train_mean": round(statistics.mean([r[f"{name}_train"] for r in rows]), 4),
            "test_mean": round(statistics.mean([r[f"{name}_test"] for r in rows]), 4),
            "gap_mean": round(statistics.mean([r[f"{name}_gap"] for r in rows]), 4),
            "gap_sd": round(statistics.pstdev([r[f"{name}_gap"] for r in rows]), 4),
        } for name in ("puro", "hibrido")},
        "references_split0": {
            "born_at_train": round(evaluate(born_order, matched, truth, action, tr0), 4),
            "born_at_test": round(evaluate(born_order, matched, truth, action, te0), 4),
            "random_test_mean": round(statistics.mean(rand_test), 4),
            "specificity_test": round(eval_specificity(rules, matched, truth, action, te0), 4),
            "subsumption_test": round(eval_subsumption(undef, truth, action, te0), 4),
        },
        "best_order_split0_pure": rows[0]["puro_order"],
    }, indent=2))
    print(f"\n-> {OUT/'order_search.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
