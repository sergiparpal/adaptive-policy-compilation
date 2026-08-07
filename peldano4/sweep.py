"""
PASO A del peldano 4: repetir la busqueda de orden del peldano 3 sobre las
mismas 577 reglas y las mismas particiones, sustituyendo el oraculo por el canal
de feedback. Cero llamadas al LLM.

PROTOCOLO
---------
1. Una politica de referencia pi0 decide sobre los casos de train. Por defecto
   es el ORDEN DE LLEGADA (born_at), que es lo que hace la base sin ninguna
   prioridad aprendida y que en test saca 0,5216. Es tambien el baseline a batir.
2. El canal observa esas decisiones y emite {caso -> accion reportada} segun sus
   cuatro parametros.
3. El voraz del peldano 3 busca un orden usando SOLO lo que emitio el canal.
   Donde antes leia `true_action[i]`, ahora lee `reported[i]`.
4. El orden se evalua sobre el test entero contra la verdad. Eso es medicion.

La pregunta: a partir de que combinacion de cobertura, retardo, ruido y asimetria
el orden aprendido deja de superar a born_at (0,5216 en test).

DEGENERACION CONTROLADA: si el canal no emite nada, el voraz no tiene con que
puntuar y su cola ordena por born_at. Es decir, sin feedback el metodo colapsa
exactamente al baseline. Que una celda del barrido quede POR DEBAJO de 0,5216
significa entonces algo concreto: el feedback recibido fue peor que ninguno.

Uso:  python3 -m peldano4.sweep
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

# Nota 2026-08-06: este modulo NO importa `true_action`. Lo hacia, sin usarlo, y
# eso contradecia literalmente la afirmacion de FINDINGS4 de que feedback.py era
# el unico que lo importaba. Las verdades que maneja llegan por `build_tables` y
# se usan solo para EVALUAR el orden resultante y para calcular la tasa de error
# de pi0 que se reporta; nunca se le pasan al aprendiz, que es
# `greedy_from_reports` y solo recibe `reported`.
from peldano3.order_search import (build_tables, ceiling, evaluate, load, split,
                                   subsumption_below)

from .feedback import Channel

OUT = Path("results4")
N_SPLITS = 3
N_DRAWS = 3

REF = {"oraculo completo": 0.7707, "5% de etiquetas": 0.7049,
       "1% de etiquetas": 0.5251, "born_at": 0.5216,
       "aleatorio": 0.4227, "techo": 0.8995}


def greedy_from_reports(rules, pool, reported, action, born):
    """
    Voraz de lista de decision sobre los casos con accion reportada.
    Identico al del peldano 3 salvo que la etiqueta viene del canal.
    Cola: born_at, para que la ausencia de feedback degenere en el baseline.
    """
    ids = [r["rule_id"] for r in rules]
    idxs = sorted(reported)
    if not idxs:
        return sorted(ids, key=lambda r: born[r])

    pos = {i: k for k, i in enumerate(idxs)}
    win = {rid: 0 for rid in ids}
    lose = {rid: 0 for rid in ids}
    for i in idxs:
        bit = 1 << pos[i]
        lab = reported[i]
        for rid in pool[i]:
            if action[rid] == lab:
                win[rid] |= bit
            else:
                lose[rid] |= bit

    remaining = (1 << len(idxs)) - 1
    left = set(ids)
    order = []
    while left and remaining:
        best, bs = None, None
        for rid in sorted(left):     # ARREGLO 2026-08-06, ver order_search.py
            s = (win[rid] & remaining).bit_count() - (lose[rid] & remaining).bit_count()
            if bs is None or s > bs:
                best, bs = rid, s
        order.append(best)
        left.discard(best)
        remaining &= ~(win[best] | lose[best])
    order += sorted(left, key=lambda rid: born[rid])
    return order


def pi0_decisions(pool, order_ids, action, idxs):
    rank = {rid: k for k, rid in enumerate(order_ids)}
    out = {}
    for i in idxs:
        if pool[i]:
            out[i] = action[min(pool[i], key=lambda r: rank[r])]
    return out


def main() -> int:
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    ids = [r["rule_id"] for r in rules]
    born_order = sorted(ids, key=lambda r: born[r])
    splits = [split(corpus, truth, seed=17 + s) for s in range(N_SPLITS)]

    print("=" * 78)
    print("PELDANO 4 · PASO A — ORDEN APRENDIDO DE UN CANAL DE FEEDBACK")
    print("=" * 78)
    print(f"  reglas 577 · corpus 2000 · semilla 17 · {N_SPLITS} particiones"
          f" x {N_DRAWS} sorteos")
    print("  pi0 (politica observada) = orden de llegada (born_at)")
    print("  el canal es el unico componente que toca true_action;")
    print("  el aprendiz solo ve {caso -> accion reportada}")
    print(f"\n  referencias en test: " +
          " · ".join(f"{k} {v}" for k, v in REF.items()))

    def run(ch_kwargs) -> tuple[float, float, float]:
        scores, yields = [], []
        for s, (tr, te) in enumerate(splits):
            dec = pi0_decisions(matched, born_order, action, tr)
            for d in range(N_DRAWS):
                ch = Channel(seed=1000 * s + d, **ch_kwargs)
                rep = ch.observe(corpus, tr, dec, window_end=max(tr))
                o = greedy_from_reports(rules, matched, rep, action, born)
                scores.append(evaluate(o, matched, truth, action, te))
                yields.append(len(rep))
        return (statistics.mean(scores), statistics.pstdev(scores),
                statistics.mean(yields))

    rows = []

    # ---------------------------------------------------------- barrido 1D
    print()
    print("=" * 78)
    print("BARRIDO POR PARAMETRO  (los demas en su valor mas favorable)")
    print("=" * 78)
    base = dict(coverage=1.0, asymmetry=1.0, delay=0, noise=0.0)
    sweeps = {
        "coverage": [1.0, 0.5, 0.25, 0.10, 0.05, 0.02],
        "asymmetry": [1.0, 0.5, 0.25, 0.10, 0.0],
        "delay": [0, 50, 100, 200, 400],
        "noise": [0.0, 0.05, 0.10, 0.20, 0.30, 0.50],
    }
    for param, values in sweeps.items():
        print(f"\n  {param}:")
        print(f"    {'valor':>8}{'etiquetas':>11}{'test e2e':>11}{'desv':>8}"
              f"{'vs born_at':>12}")
        for v in values:
            kw = dict(base); kw[param] = v
            m, sd, y = run(kw)
            rows.append({"sweep": param, "value": v, **kw,
                         "labels": round(y, 1), "test": round(m, 4),
                         "sd": round(sd, 4)})
            flag = "" if m >= REF["born_at"] else "   <- por debajo"
            print(f"    {v:>8}{y:>11.0f}{m:>11.4f}{sd:>8.4f}"
                  f"{m - REF['born_at']:>+12.4f}{flag}")

    # ------------------------------------------------------ rejilla realista
    print()
    print("=" * 78)
    print("REJILLA · asimetria 0 (solo se observan errores), que es el caso real")
    print("=" * 78)
    print(f"  {'cobertura':>10}{'retardo':>9}{'ruido':>7}{'etiq.':>8}"
          f"{'test e2e':>11}{'desv':>8}{'vs born_at':>12}")
    for cov in (1.0, 0.5, 0.25, 0.10):
        for dly in (0, 100):
            for noi in (0.0, 0.1, 0.3):
                kw = dict(coverage=cov, asymmetry=0.0, delay=dly, noise=noi)
                m, sd, y = run(kw)
                rows.append({"sweep": "grid_a0", "value": None, **kw,
                             "labels": round(y, 1), "test": round(m, 4),
                             "sd": round(sd, 4)})
                flag = "" if m >= REF["born_at"] else "   <-"
                print(f"  {cov:>10}{dly:>9}{noi:>7}{y:>8.0f}{m:>11.4f}"
                      f"{sd:>8.4f}{m - REF['born_at']:>+12.4f}{flag}")

    # ------------------------------------------------------- eleccion de pi0
    print()
    print("=" * 78)
    print("SENSIBILIDAD A pi0  (c=0.5, a=0, d=0, e=0.1)")
    print("=" * 78)
    ncond = {r["rule_id"]: len(r["conditions"]) for r in rules}
    spec_order = sorted(ids, key=lambda r: (-ncond[r], born[r]))
    pi0s = {"born_at (0.5216 en test)": born_order,
            "especificidad aprox (0.1829)": spec_order}
    print(f"  {'pi0':<32}{'errores de pi0':>16}{'etiq.':>8}{'test e2e':>11}")
    for name, o0 in pi0s.items():
        scores, yields, errs = [], [], []
        for s, (tr, te) in enumerate(splits):
            dec = pi0_decisions(matched, o0, action, tr)
            errs.append(sum(1 for i in tr if dec.get(i) != truth[i]) / len(tr))
            for d in range(N_DRAWS):
                ch = Channel(coverage=0.5, asymmetry=0.0, delay=0, noise=0.1,
                             seed=1000 * s + d)
                rep = ch.observe(corpus, tr, dec, window_end=max(tr))
                o = greedy_from_reports(rules, matched, rep, action, born)
                scores.append(evaluate(o, matched, truth, action, te))
                yields.append(len(rep))
        print(f"  {name:<32}{statistics.mean(errs):>15.1%}"
              f"{statistics.mean(yields):>8.0f}{statistics.mean(scores):>11.4f}")
        rows.append({"sweep": "pi0", "value": name, "coverage": 0.5,
                     "asymmetry": 0.0, "delay": 0, "noise": 0.1,
                     "labels": round(statistics.mean(yields), 1),
                     "test": round(statistics.mean(scores), 4),
                     "sd": round(statistics.pstdev(scores), 4)})

    OUT.mkdir(exist_ok=True)
    (OUT / "sweep.json").write_text(json.dumps(
        {"references": REF, "n_splits": N_SPLITS, "n_draws": N_DRAWS,
         "pi0": "born_at", "rows": rows}, indent=2))
    print(f"\n-> {OUT/'sweep.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
