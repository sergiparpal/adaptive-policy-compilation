"""
STEP 1 of the audit, rung 4 half: does the asymmetry regime change survive a
serious optimizer?

--------------------------------------------------------------------------
THE CLAIM UNDER TEST
--------------------------------------------------------------------------
`results4/FINDINGS4.md` reports that with symmetric feedback the learned order
beats born_at by +0.235, and with the asymmetric kind — the only sort a real
system produces — by +0.067. That is the ONLY claim rung 4 contributes, and it
rests on the same greedy the audit has now shown to be weak. If a serious
optimizer extracts much more from scarce, asymmetric labels, the figure rises
and the regime change softens.

--------------------------------------------------------------------------
WHAT CHANGES AND WHAT DOES NOT
--------------------------------------------------------------------------
Only the learner. Same channel (`feedback.py`, untouched), same pi0 (born_at),
same three splits with seed 17, same corpus. Where `sweep.greedy_from_reports`
ran a decision-list greedy over the reported labels, this runs the declared
multi-start local search over exactly the same labels.

ORACLE SEPARATION IS UNCHANGED AND IS THE POINT. The learner receives
`reported` and nothing else: the masks it optimizes are built from the channel's
output, never from `truth`. The truth appears only in the evaluation, which is
measurement and not supervision. This module handles truths for that evaluation
and never passes them to the search, exactly as `sweep.py` does — and unlike
`sweep.py` before 2026-08-06, it does not import the oracle at all.

--------------------------------------------------------------------------
THE CELLS, ORDERED BY HOW MUCH THEY DECIDE
--------------------------------------------------------------------------
anchors    c=1 d=0 e=0 with a=1 and a=0. The channel's OUTPUT is deterministic
           in both — at a=1 every case reports the truth, at a=0 exactly the
           cases pi0 got wrong do — so one draw is not a reduction, it is the
           whole cell. This pair alone is the +0.235 against +0.067.
asymmetry  a in 0.5, 0.25, 0.1: the shape of the transition between the two.
noise      the sweep that made noise look beneficial. If restarts were what the
           noise was supplying, it should stop helping now.

Each group is written to the record as it finishes, so that a run cut short
leaves the groups it completed rather than nothing, and the report can say
exactly which ones those are.

Usage:  python3 -m rung4.sweep_ls [--groups anchors,asymmetry,noise]
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS, build_masks,
                                   declared_starts, greedy_order_from_masks,
                                   multistart, score_order)
from rung3.order_search import (build_tables, load, split, subsumption_below)
from rung3.order_search_ls import space_pools

from .feedback import Channel
from .sweep import pi0_decisions

OUT = Path("results4")
N_SPLITS = 3
N_DRAWS = 3

# From `results4/FINDINGS4.md`, produced by the greedy this replaces.
REF = {"born_at": 0.5216, "oraculo completo": 0.7707, "aleatorio": 0.4227,
       "ancla simetrica (a=1)": 0.7564, "ancla asimetrica (a=0)": 0.5887}

GROUPS = ("anchors", "asymmetry", "noise")


def record_name(groups) -> str:
    """
    Where a run writes. A partial run goes to its own file.

    Every save rewrites the whole document from the rows of THIS process, so
    letting `--groups noise` land on the canonical name would silently drop the
    anchors that carry the finding. That is the class of loss
    `harness/record_guard.py` exists to prevent, and it nearly happened here on
    2026-08-08.
    """
    if set(groups) == set(GROUPS):
        return "sweep_ls.json"
    return f"sweep_ls_{'_'.join(groups)}.json"


def learn(ids, pool, reported, action, born):
    """
    The learner. Sees `reported` and nothing else.

    Degenerates to born_at when the channel emitted nothing, so that the
    absence of feedback collapses to the baseline exactly as rung 4 intended.
    """
    order_born = sorted(ids, key=lambda r: born[r])
    idxs = sorted(reported)
    if not idxs:
        return order_born, {"best_score": 0, "best_from": "sin etiquetas",
                            "best_from_index": None, "n_starts": 0}
    M, W, full = build_masks(ids, pool, reported, action, idxs)
    greedy = greedy_order_from_masks(ids, M, W, full,
                                     tail_key=lambda rid: born[rid])
    best, st = multistart(declared_starts(ids, first=greedy), M, W, full,
                          neighbourhood=DECLARED_NEIGHBOURHOOD)
    return best, st


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    groups = list(GROUPS)
    for i, a in enumerate(argv):
        if a == "--groups" and i + 1 < len(argv):
            groups = [g for g in argv[i + 1].split(",") if g in GROUPS]

    t_start = time.time()
    corpus, rules, ext, conds = load()
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    ids = [r["rule_id"] for r in rules]
    below = subsumption_below(rules, ext)
    matched, _undef, truth = build_tables(corpus, rules, conds, below)
    born_order = sorted(ids, key=lambda r: born[r])
    splits = [split(corpus, truth, seed=17 + s) for s in range(N_SPLITS)]
    sM, sW, sfull, sn = space_pools(ids, conds, action, below)["puro"]

    print("=" * 78)
    print("PASO 1 · RUNG 4 — ¿SOBREVIVE EL CAMBIO DE REGIMEN POR ASIMETRIA?")
    print("=" * 78)
    print(f"  reglas {len(ids)} · corpus {len(corpus)} · {N_SPLITS} particiones")
    print(f"  aprendiz: {DECLARED_NEIGHBOURHOOD}, semilla {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} arranques + el voraz")
    print("  pi0 = born_at · el canal es el de feedback.py, sin tocar")
    print("  referencias del registro: " +
          " · ".join(f"{k} {v}" for k, v in REF.items()))
    print(f"  {describe()}")

    rows = []

    def run_cell(label, kwargs, draws):
        """One channel configuration. Returns test e2e, its spread and the
        score over the exhaustive space."""
        scores, spaces, yields = [], [], []
        t0 = time.time()
        for s, (tr, te) in enumerate(splits):
            dec = pi0_decisions(matched, born_order, action, tr)
            tM, tW, tfull = build_masks(ids, matched, truth, action, te)
            for d in range(draws):
                ch = Channel(seed=1000 * s + d, **kwargs)
                rep = ch.observe(corpus, tr, dec, window_end=max(tr))
                order, _st = learn(ids, matched, rep, action, born)
                scores.append(score_order(order, tM, tW, tfull) / len(te))
                spaces.append(score_order(order, sM, sW, sfull) / sn)
                yields.append(len(rep))
        row = {"label": label, **kwargs, "draws": draws,
               "labels": round(statistics.mean(yields), 1),
               "test": round(statistics.mean(scores), 4),
               "sd": round(statistics.pstdev(scores), 4),
               "space": round(statistics.mean(spaces), 4),
               "vs_born_at": round(statistics.mean(scores) - REF["born_at"], 4),
               "seconds": round(time.time() - t0, 1)}
        rows.append(row)
        print(f"  {label:<26}{row['labels']:>8.0f}{row['test']:>10.4f}"
              f"{row['sd']:>8.4f}{row['vs_born_at']:>+11.4f}"
              f"{row['space']:>10.4f}{row['seconds']:>9.0f}s")
        return row

    name = record_name(groups)

    def save():
        OUT.mkdir(exist_ok=True)
        (OUT / name).write_text(json.dumps({
            "_env": environment(n_splits=N_SPLITS, n_draws=N_DRAWS,
                                neighbourhood=DECLARED_NEIGHBOURHOOD,
                                multistart_seed=MULTISTART_SEED,
                                multistart_starts=MULTISTART_STARTS),
            "what": "step 1 of the audit, rung 4 half: the asymmetry regime "
                    "change re-measured with the declared optimizer",
            "groups_run": groups_done, "groups_requested": groups,
            "references": REF, "pi0": "born_at",
            "n_rules": len(ids), "n_space": sn,
            "rows": rows,
            "seconds_total": round(time.time() - t_start, 1),
        }, indent=2))

    groups_done = []
    hdr = (f"  {'celda':<26}{'etiq.':>8}{'test e2e':>10}{'desv':>8}"
           f"{'vs born_at':>11}{'espacio':>10}{'coste':>10}")

    if "anchors" in groups:
        print()
        print("=" * 78)
        print("ANCLAS — salida del canal determinista, un sorteo ES la celda")
        print("=" * 78)
        print(hdr)
        run_cell("simetrica  a=1", dict(coverage=1.0, asymmetry=1.0,
                                        delay=0, noise=0.0), draws=1)
        run_cell("asimetrica a=0", dict(coverage=1.0, asymmetry=0.0,
                                        delay=0, noise=0.0), draws=1)
        groups_done.append("anchors")
        save()

    if "asymmetry" in groups:
        print()
        print("=" * 78)
        print("FORMA DE LA TRANSICION")
        print("=" * 78)
        print(hdr)
        for a in (0.5, 0.25, 0.1):
            run_cell(f"asimetria a={a}", dict(coverage=1.0, asymmetry=a,
                                              delay=0, noise=0.0), draws=N_DRAWS)
        groups_done.append("asymmetry")
        save()

    if "noise" in groups:
        print()
        print("=" * 78)
        print("RUIDO — ¿sigue ayudando, ahora que los reinicios estan puestos?")
        print("=" * 78)
        print(hdr)
        for e in (0.0, 0.1, 0.3, 0.5):
            run_cell(f"ruido e={e}", dict(coverage=1.0, asymmetry=1.0,
                                          delay=0, noise=e), draws=N_DRAWS)
        groups_done.append("noise")
        save()

    print()
    print("=" * 78)
    print("LECTURA")
    print("=" * 78)
    anc = {r["label"]: r for r in rows if r["label"].startswith(("simetrica",
                                                                "asimetrica"))}
    if len(anc) == 2:
        sim = anc["simetrica  a=1"]
        asi = anc["asimetrica a=0"]
        print(f"  simetrica  a=1 : {sim['test']:.4f}  ({sim['vs_born_at']:+.4f} "
              f"vs born_at)   el registro daba +0.2348")
        print(f"  asimetrica a=0 : {asi['test']:.4f}  ({asi['vs_born_at']:+.4f} "
              f"vs born_at)   el registro daba +0.0671")
        print(f"  razon simetrica/asimetrica: "
              f"{sim['vs_born_at']/asi['vs_born_at']:.1f}x"
              if asi["vs_born_at"] else "")
    save()
    print(f"\n  coste total: {time.time()-t_start:.0f}s")
    print(f"-> {OUT/name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
