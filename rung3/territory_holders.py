"""
WHICH RULES HOLD TERRITORY, AND WHETHER THE CEILING OF kappa IS ONE OF THEM.

--------------------------------------------------------------------------
PROVENANCE, FIRST, BECAUSE IT IS NOT WHAT THE TWO COMMITS BEFORE IT WERE
--------------------------------------------------------------------------
This is an AUDIT FINDING FOUND AFTER THE RUN, not a pre-registered measurement.
The fact came first — read off `order_metrics_rules.json` once it was published —
and this instrument was written afterwards, by someone who already knew what it
would say. The two commits of PR #29 had the opposite property: the prediction
was signed and committed before any of its figures existed, and the log shows it.
This one cannot claim that and does not. The record it writes says so in its own
`provenance` field, and the erratum in `FINDINGS_ORDERS.md` says it again.

What that costs a reader: nothing here is a bet that could have failed, so the
only thing this can be worth is the primitive being exact and the gates being
blocking. Both are below.

--------------------------------------------------------------------------
WHAT IS BEING CORRECTED
--------------------------------------------------------------------------
Part five of `FINDINGS_ORDERS.md` reports `kappa`'s range over the 577 rules as
the illustration that the mechanism D-a proposed was AVAILABLE — the entry it
adjudicates argues that a range of that size could cover a 30x spread in the
pairs, where the class ratios could not. The range is real. What nobody checked
is whether the rule at its ceiling is a rule that ever decides anything: under
first-match-wins, a rule with an enormous arrival concentration and no territory
enters `rho_hat` exactly nowhere.

So the primitive this run publishes is the one the earlier record did not keep:
for each of the 65 end orders of split 0, WHICH rules hold territory, by id. The
counts were already gated there; the identities were not, and everything the
erratum needs is a lookup away from them.

--------------------------------------------------------------------------
THE PRIMITIVE, AND WHY THE DERIVED BLOCK IS NOT A SECOND RECORD
--------------------------------------------------------------------------
`rules_with_territory` is the whole measurement: 65 sorted lists of rule ids.
Every figure in `derived` is a lookup of `kappa_by_rule` — already published in
`order_metrics_rules.json` — against those lists, so a reader with the two files
recomputes the derived block without running anything. It is emitted for
convenience and it is not a second home for a number: the record that owns
`kappa` is the other one, and this file reads it rather than recomputing it.

--------------------------------------------------------------------------
THREE GATES, ALL BLOCKING
--------------------------------------------------------------------------
PARITY, 31 rows: the same gate as parts one, two, four and five — six budget rows
against `start_budget_check.json` and the whole 1% band against
`budget_and_balance_ls.json`. If it fails, the regenerated orders are not the
published ones and the territories would be somebody else's.

KAPPA READ, not recomputed blindly: the per-rule values come from
`order_metrics_rules.json`, and the gate is that they still reproduce the
five-number summary that record publishes. Recomputing kappa from the masks here
would create a second source for a figure that already has an owner.

THE COUNTS: `n_rules_with_territory` for each of the 65 orders must equal
`gates.territories.per_order` of that same record, order by order. It is what
says these are the same territories, computed by the same sweep, and not a second
population that happens to be about the same size.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No new search: the orders come out of `run_full_supervision` and `run_band_1pct`
of `order_metrics_run.py`, imported and called unchanged. `MULTISTART_SEED`,
`MULTISTART_STARTS` and `DECLARED_NEIGHBOURHOOD` are untouched. No API call. It
writes one new file, `results3/territory_holders.json`, and rewrites none of the
records it reads — least of all `order_metrics_rules.json`, whose figures this
corrects the READING of and not the values.

Usage:  python3 -m rung3.territory_holders
        python3 -m rung3.territory_holders --checks   (gates only)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS)
from rung3.order_metrics import winners
from rung3.order_metrics_run import (BUDGETS, SPLITS_FULL, build_instance,
                                        parity_band, parity_full_supervision,
                                        resumen, run_band_1pct,
                                        run_full_supervision)

OUT = Path("results3")
RECORD = "territory_holders.json"
RULES_RECORD = "order_metrics_rules.json"
POOL = "puro"
SURFACE = "espacio exhaustivo, pool puro"

SET = "split0_starts65"
N_ORDERS = 65

PROVENANCE = (
    "POST-RUN AUDIT FINDING, not a pre-registered measurement. The fact was "
    "found by reading results3/order_metrics_rules.json after PR #29 published "
    "it, and this instrument was written afterwards knowing what it would say. "
    "The two commits of PR #29 had the opposite property — the prediction was "
    "signed and committed before any figure existed, which the log shows — and "
    "this run cannot claim it. Nothing here is a bet that could have failed; "
    "what it can be worth is that the primitive is exact and the three gates are "
    "blocking.")

RECOMPUTE = (
    "everything under `derived` is a lookup of "
    "order_metrics_rules.json::kappa_by_rule against `rules_with_territory` "
    "below. A reader holding the two files recomputes the whole block without "
    "running anything, which is why the primitive is what this record exists to "
    "carry and the derived block is a convenience rather than a second owner of "
    "any figure.")


# ---------------------------------------------------------------------------
# The primitive
# ---------------------------------------------------------------------------

def holders(orden, M, full):
    """
    The ids of the rules that win at least one case under `orden`, sorted.

    `order_metrics.winners` is the same sweep every figure in this thread rests
    on, and it returns {rule: mask of the cases it wins} — a rule absent from
    that dict wins nothing, which is exactly the property in question. The mask
    itself is dropped here: what this record carries is identity, and the sizes
    are already published as `sum_of_territories` and the per-class rates.
    """
    terr, undecided = winners(orden, M, full)
    return sorted(rid for rid, m in terr.items() if m), undecided.bit_count()


def territory_table(orders, M, full):
    filas = []
    for k, o in enumerate(orders):
        ids, undecided = holders(o, M, full)
        filas.append({"order": k, "n_rules_with_territory": len(ids),
                      "undecided": undecided, "rule_ids": ids})
    return filas


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gate_kappa_read(rec):
    """
    kappa comes from the published record, and the gate is that it still
    reproduces the five-number summary published beside it.

    Read, never recomputed from the masks: `order_metrics_rules.json` owns that
    figure, and a second computation of it here would be a second source for a
    number with one home. The rounding is the one that record applied — four
    decimals — so the comparison is against the object it actually publishes.
    """
    kappa = {r: v for r, v in rec["kappa_by_rule"].items() if v is not None}
    publicado = rec["kappa_summary"]
    recomputado = resumen([round(v, 4) for v in kappa.values()])
    filas = {k: (recomputado.get(k), v, recomputado.get(k) == v)
             for k, v in publicado.items()}
    return kappa, {
        "what": "the five-number summary of kappa, recomputed from the per-rule "
                "values this run READS, against the summary published beside "
                "them",
        "source": f"{RULES_RECORD}::kappa_by_rule and ::kappa_summary",
        "n_rules": len(kappa),
        "comparison": filas,
        "passes": all(v[2] for v in filas.values()),
    }


def gate_counts(filas, rec):
    """`n_rules_with_territory` per order against the territory gate of
    `order_metrics_rules.json`, order by order."""
    pub = {f["order"]: f["n_rules_with_territory"]
           for f in rec["gates"]["territories"]["per_order"]}
    difieren = [{"order": f["order"], "recomputed": f["n_rules_with_territory"],
                 "published": pub.get(f["order"])}
                for f in filas if pub.get(f["order"]) != f["n_rules_with_territory"]]
    return {
        "what": "the number of rules holding territory under each of the 65 end "
                "orders, against the gate the earlier record already passed. It "
                "is what says these are the same territories and not a second "
                "population of about the same size.",
        "source": f"{RULES_RECORD}::gates.territories.per_order",
        "n_orders": len(filas),
        "n_published": len(pub),
        "orders_that_differ": difieren,
        "passes": not difieren and len(filas) == N_ORDERS
                  and len(pub) >= N_ORDERS,
    }


# ---------------------------------------------------------------------------
# The derived block, every line of it a lookup
# ---------------------------------------------------------------------------

def derive(filas, kappa, publicado_max):
    union = sorted({r for f in filas for r in f["rule_ids"]})
    k_union = sorted(kappa[r] for r in union if r in kappa)

    por_orden = []
    for f in filas:
        ks = [kappa[r] for r in f["rule_ids"] if r in kappa]
        lo, hi = (min(ks), max(ks)) if ks else (None, None)
        por_orden.append({
            "order": f["order"],
            "n_rules": f["n_rules_with_territory"],
            "kappa_min": lo, "kappa_max": hi,
            "range": (hi / lo) if (ks and lo) else None,
        })
    rangos = sorted(v["range"] for v in por_orden if v["range"] is not None)

    tope = max(kappa, key=kappa.get)
    donde = [f["order"] for f in filas if tope in f["rule_ids"]]

    return {
        "union_over_the_65_orders": {
            "n_rules": len(union),
            "n_rules_in_the_pool": len(kappa),
            "fraction_of_the_pool": round(len(union) / len(kappa), 6)
                                    if kappa else None,
            "rule_ids": union,
        },
        "kappa_over_the_union": {
            "n": len(k_union),
            "min": k_union[0] if k_union else None,
            "median": resumen(k_union)["median"] if k_union else None,
            "max": k_union[-1] if k_union else None,
            "min_rule": min(union, key=lambda r: kappa[r]) if union else None,
            "max_rule": max(union, key=lambda r: kappa[r]) if union else None,
        },
        "kappa_range_within_an_order": {
            "what": "max over min of kappa among the rules that hold territory "
                    "under ONE order: the spread rho_hat actually has available "
                    "inside a single machine, as opposed to across the pool",
            "per_order": por_orden,
            "median": resumen(rangos)["median"] if rangos else None,
            "min": rangos[0] if rangos else None,
            "max": rangos[-1] if rangos else None,
        },
        "argmax_kappa_holds_territory": {
            "rule_id": tope,
            "kappa": kappa[tope],
            "published_max": publicado_max,
            "matches_published_max": round(kappa[tope], 4) == publicado_max,
            "holds_territory": bool(donde),
            "n_orders_where_it_holds": len(donde),
            "orders_where_it_holds": donde[:20],
            "scope": "the 65 end orders of split 0 at full supervision, the set "
                     "every matrix in FINDINGS_ORDERS.md holds. It says nothing "
                     "about any other order over these rules.",
        },
        "n_rules_with_territory": resumen(
            sorted(f["n_rules_with_territory"] for f in filas)),
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    solo_checks = "--checks" in argv
    t_start = time.time()

    print("=" * 78)
    print("WHO HOLDS TERRITORY — an audit note on part five")
    print("=" * 78)
    print(f"  optimizer: {DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} declared starts + the greedy (untouched)")
    print(f"  set {SET} · {N_ORDERS} end orders · pool {POOL} · no new search, "
          f"no API calls")
    print("  POST-RUN AUDIT FINDING: the fact was known before this instrument "
          "was written")
    print(f"  {describe()}")

    rec = json.loads((OUT / RULES_RECORD).read_text())

    kappa, g_kappa = gate_kappa_read(rec)
    print()
    print(f"KAPPA GATE — read from {RULES_RECORD}, not recomputed")
    for k in ("min", "p25", "median", "p75", "max"):
        mio, pub, ok = g_kappa["comparison"][k]
        print(f"  {k:<8}{mio:>10}   published {pub:>10}"
              f"{'  ok' if ok else '  NO'}")
    if not g_kappa["passes"]:
        print("  STOP: the values read do not reproduce the summary published "
              "beside them.")
        return 1

    inst = build_instance()
    sM, _sW, sfull, sn = inst["space"]
    print(f"\n  instance ready in {inst['seconds_setup']}s: "
          f"{len(inst['ids'])} rules, {sn:,} space cases")

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

    # ------------------------------------------------------------ the primitive
    s0 = SPLITS_FULL[0]
    t0 = time.time()
    orders = [r["order"] for r in runs[s0]["stats"]["rows"][:N_ORDERS]]
    filas = territory_table(orders, sM, sfull)
    print(f"\n  who holds territory under each of the {N_ORDERS} orders, in "
          f"{time.time() - t0:.0f}s")

    g_counts = gate_counts(filas, rec)
    print()
    print(f"COUNT GATE — against {RULES_RECORD}::gates.territories.per_order")
    print(f"  {g_counts['n_orders']} orders, "
          f"{len(g_counts['orders_that_differ'])} differ"
          f"{'  ok' if g_counts['passes'] else '  NO'}")
    for f in g_counts["orders_that_differ"][:10]:
        print(f"    order {f['order']}: recomputed {f['recomputed']} vs "
              f"published {f['published']}")
    if not g_counts["passes"]:
        print("  STOP: these are not the territories the earlier record gated.")
        return 1

    if solo_checks:
        print(f"\n  ALL THREE GATES PASS. total cost: "
              f"{time.time() - t_start:.0f}s")
        return 0

    derived = derive(filas, kappa, rec["kappa_summary"]["max"])

    a = derived["argmax_kappa_holds_territory"]
    u = derived["union_over_the_65_orders"]
    ku = derived["kappa_over_the_union"]
    rg = derived["kappa_range_within_an_order"]
    print()
    print("=" * 78)
    print("WHAT THE PRIMITIVE SAYS")
    print("=" * 78)
    print(f"  the union of the 65 sets is {u['n_rules']} rules of "
          f"{u['n_rules_in_the_pool']} ({100 * u['fraction_of_the_pool']:.1f}%)")
    print(f"  kappa over that union: {ku['min']:.4f} ({ku['min_rule']}) .. "
          f"{ku['max']:.4f} ({ku['max_rule']}), median {ku['median']:.4f}")
    print(f"  kappa range INSIDE one order: median {rg['median']:.1f}x, "
          f"min {rg['min']:.1f}x, max {rg['max']:.1f}x")
    print(f"  the rule at kappa's ceiling is {a['rule_id']} "
          f"(kappa {a['kappa']:.4f}, published max {a['published_max']}): "
          f"holds territory {a['holds_territory']}"
          f" in {a['n_orders_where_it_holds']} of {N_ORDERS} orders")

    payload = {
        "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            budgets=list(BUDGETS), set_measured=SET,
                            n_orders=N_ORDERS),
        "what":
            "which rules hold territory under each of the 65 end orders of "
            "split 0, by id. The counts were gated by "
            "order_metrics_rules.json; the identities were not stored anywhere, "
            "and they are what says whether the rule at kappa's ceiling — the "
            "figure part five of FINDINGS_ORDERS.md uses to illustrate that the "
            "mechanism D-a proposed was AVAILABLE — is a rule that ever decides "
            "a case. No new search: the orders come out of run_full_supervision "
            "and run_band_1pct of order_metrics_run.py, imported and called "
            "unchanged, and the 31-row parity gate is what says they are the "
            "published ones. kappa is READ from order_metrics_rules.json and "
            "never recomputed. No record is rewritten. Zero API calls.",
        "provenance": PROVENANCE,
        "corrects": {
            "record": "results3/FINDINGS_ORDERS.md, part five (the rule level, "
                      "D-a to D-d), and its erratum of 2026-08-16",
            "what": "the READING of kappa's range as the spread available to "
                    "rho_hat. The values in order_metrics_rules.json are "
                    "untouched and none of them moves; no verdict moves either.",
            "scope": "the 65 end orders of split 0 at full supervision. Not a "
                     "statement about every possible order over these rules.",
        },
        "surface": SURFACE,
        "surface_note":
            "territories are over the exhaustive space of 134,400 cases, pure "
            "pool, the surface part five measures on. kappa is the arrival "
            "concentration published there, which carries the touched mask "
            "inside it. The train, test and space figures of the parity gate are "
            "the surfaces of the records being reproduced.",
        "pool": POOL,
        "set": SET,
        "n_rules": len(inst["ids"]),
        "n_space": sn,
        "n_orders": N_ORDERS,
        "splits": list(SPLITS_FULL),
        "budgets": list(BUDGETS),
        "gates": {
            "kappa_read": g_kappa,
            "parity_rows": n_filas,
            "parity_full_supervision": par_a,
            "parity_band_1pct": par_b,
            "counts": g_counts,
        },
        "no_new_search":
            "every order measured here comes out of run_full_supervision and "
            "run_band_1pct of order_metrics_run.py, imported and called "
            "unchanged. MULTISTART_SEED, MULTISTART_STARTS and "
            "DECLARED_NEIGHBOURHOOD are untouched and no figure here is an "
            "argument about any of them.",
        "rules_with_territory": filas,
        "derived": derived,
        "how_to_recompute_the_derived_block": RECOMPUTE,
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
