"""
THE FLOOR BY POOL — what an order that searches for nothing scores, on both
pools and on all three surfaces.

--------------------------------------------------------------------------
WHY IT EXISTS
--------------------------------------------------------------------------
`results3/order_search_ls.json` carries a `"pool"` field on every row and, under
it, only greedy and local-search scores. So there is a world record for the
`hibrido` pool and no measurement at all of what WALKING scores there — and
`hibrido` is the pool where declared edges live. Anything a declaration produces
has to be scored against the floor of the same machine, and that floor did not
exist. `PLAN_PAIRWISE.md` §3 marks the missing cell explicitly:
`born_at`, `hibrido` pool — NOT MEASURED.

Three of the figures this run produces have never had an owning record either:
`born_at` and the random mean over the FULL corpus, and reversed `born_at` over
the space. They come from the ad hoc probe of `CHAT_SUMMARY.md` §2.1, which
declares its own protocol unofficial, and `ARBITRATION_REPORT.md` §2 cites the
two reversed figures with the only warning of its kind in that document: "the
two figures of the reversed order are the ones left unconfirmed". This run is
where they stop being unconfirmed.

--------------------------------------------------------------------------
THIS RECORD CARRIES NO PREDICTION, AND THAT IS NOT A CHOICE
--------------------------------------------------------------------------
`PLAN_PAIRWISE.md` §0.1: the two rows that predicted these figures, P-a and P-b,
were measured on 2026-08-24 BEFORE anybody signed them — by an audit that ran
this stage's own gate to check that a correct implementation could pass it. A
band defended after its figure is known is not a prediction, and redrafting one
around a number already seen is hard rule 6 wearing a different hat, so they are
recorded there as spent and are not restored here.

What this stage loses is only its status as a test of a prediction. What it
keeps is its whole purpose: giving these figures an owner, a script and an
`_env`. Nothing below may be reported as a band that held.

--------------------------------------------------------------------------
TRAP 1 — THERE ARE TWO RANDOM-ORDER GENERATORS AND THEY DISAGREE
--------------------------------------------------------------------------
`local_search.random_order(ids, seed)` sorts the ids and shuffles once per seed:
fifty independent `random.Random`. `order_search.py:344-350` uses a different
one: a single `random.Random(17)` shuffling the rules' appearance order fifty
times IN SEQUENCE, so draw k depends on the k-1 before it. Different sequences,
different means.

The record's corpus figures came from the second and the record's space figure
from the first. **No single generator reproduces all three**, which is why every
random row below names its generator on the same line as its number, and why the
gate names one per row. A stage that prescribed one generator everywhere would
fail its own corpus gates on a CORRECT implementation.

The rules' appearance order in `results/llm_run.json` happens to equal
`sorted(ids)` — the ids are `R%04d` in birth order — so the two generators differ
in the RNG and in nothing else. That is checked here rather than assumed:
`gate_generators_differ_only_in_the_rng` is in the record.

--------------------------------------------------------------------------
TRAP 2 — THE RECORD'S CORPUS-TEST REFERENCES ARE SPLIT 0, NOT THE MEAN OF FIVE
--------------------------------------------------------------------------
`order_search.py:344` and `order_search_ls.py:266-274` compute `born_at` and the
random mean on `te0` from `split(corpus, truth, seed=17)` alone, while the
searched orders printed in the same table are means over five splits. Two index
sets in one block, unlabelled.

Both are reported here, on separate lines, each labelled. Split 0 is the only one
that reproduces the record; the five-split mean is the more stable statistic.
Neither substitutes for the other, and having the label on the same line as the
number is the whole point of this stage.

--------------------------------------------------------------------------
THE GATE, WHICH RUNS FIRST AND IS BLOCKING
--------------------------------------------------------------------------
Six figures that are not new and must come out. Four gate against a record; two
(G3, G4) gate against the unowned probe, and are here because they are the only
check available on the full-corpus surface and because giving them an owner is
what this stage is for. **A probe that gates is still a probe** and the record
says so per row, in `kind`.

A miss on G2, G4 or G6 is a generator mismatch until proven otherwise. A miss on
any row stops the run: nothing is adjusted to fit (hard rule 6).

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
No search of any kind: no greedy, no local search, no multi-start.
`MULTISTART_SEED`, `MULTISTART_STARTS` and `DECLARED_NEIGHBOURHOOD` are not read
and not touched. `results/llm_run.json` is opened read-only through
`order_search.load`. It writes one new file, `results3/floor_by_pool.json`, and
rewrites none of the records it reads. Zero API calls.

Usage:  PYTHONHASHSEED=0 python3 -m rung3.floor_by_pool
        PYTHONHASHSEED=0 python3 -m rung3.floor_by_pool --checks   (gate only)
"""

from __future__ import annotations

import json
import random
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.local_search import build_masks, random_order, score_order
from rung3.order_search import build_tables, load, split, subsumption_below
from rung3.order_search_ls import space_pools

OUT = Path("results3")
RECORD = "floor_by_pool.json"

N_SPLITS = 5
N_RANDOM = 50
SPLIT_SEED = 17
POOLS = ("puro", "hibrido")

# The two generators of trap 5.5, named so that no figure can be produced
# without one of these strings landing on the same line as it.
GEN_MODULE = "local_search.random_order(ids, seed), seeds 0..49"
GEN_RECORD = "order_search.py:344-350, one random.Random(17) shuffling the "\
             "appearance order 50 times in sequence"

CORPUS_FULL = "corpus_full"
SPACE = "space"


def test_split_name(s: int) -> str:
    return f"corpus_test_split{s}"


# ---------------------------------------------------------------------------
# The two generators, transcribed
# ---------------------------------------------------------------------------

def module_random_orders(ids, n=N_RANDOM):
    """`local_search.random_order`: `sorted(ids)`, one `Random(seed)` per draw.

    This is the generator behind the space figure the `FINDINGS3.md` erratum
    publishes (0.3768).
    """
    return [random_order(ids, seed=k) for k in range(n)]


def record_random_orders(ids, n=N_RANDOM, seed=SPLIT_SEED):
    """
    The generator of `order_search.py:344-350`, transcribed rather than
    imported: there it is four lines inline in `main()` and there is nothing to
    import.

        rng = random.Random(17)
        ids = [r["rule_id"] for r in rules]     # APPEARANCE order
        for _ in range(50):
            o = ids[:]; rng.shuffle(o)

    One generator advanced fifty times, so draw k is conditioned on every draw
    before it. This is the generator behind both corpus figures the record
    publishes (0.4227 test split 0, 0.4172 full corpus).
    """
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        o = list(ids)
        rng.shuffle(o)
        out.append(o)
    return out


# ---------------------------------------------------------------------------
# The order families that search for nothing
# ---------------------------------------------------------------------------

def born_at_order(ids, born):
    return sorted(ids, key=lambda rid: born[rid])


def order_families(ids, born):
    """{name: order}. Two deterministic families; the random ones are 50 draws
    each and are handled apart."""
    asc = born_at_order(ids, born)
    return {"born_at": asc, "born_at_reversed": list(reversed(asc))}


# ---------------------------------------------------------------------------
# Instances: (M, W, full, n) per pool and surface
# ---------------------------------------------------------------------------

def corpus_instances(ids, corpus_pool, truth, action, index_sets):
    """One instance per (surface, pool) over the corpus index sets given."""
    inst = {}
    for surface, idxs in index_sets.items():
        for name in POOLS:
            M, W, full = build_masks(ids, corpus_pool[name], truth, action, idxs)
            inst[(surface, name)] = (M, W, full, len(idxs))
    return inst


def index_sets_of(corpus, truth):
    """The corpus index sets this record measures on, each named.

    `corpus_test_split0` is `split(corpus, truth, seed=17)[1]` — the record's own
    index set, and the only one that reproduces 0.5216 / 0.4227. Splits 1..4 are
    here so that the five-split mean can be reported beside it with its own
    label (trap 5.6).
    """
    sets = {CORPUS_FULL: list(range(len(corpus)))}
    for s in range(N_SPLITS):
        sets[test_split_name(s)] = split(corpus, truth, seed=SPLIT_SEED + s)[1]
    return sets


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def floor(order, instance):
    """Fraction of the instance's cases won with the right action."""
    M, W, full, n = instance
    return score_order(order, M, W, full) / n


def random_floor(orders, instance):
    """Mean and spread over the 50 draws. Both deviations are reported because
    the probe that published `sd 0.0711` is not in the tree and does not say
    which one it used."""
    vals = [floor(o, instance) for o in orders]
    return {
        "mean": statistics.mean(vals),
        "pstdev": statistics.pstdev(vals),
        "stdev": statistics.stdev(vals),
        "min": min(vals), "max": max(vals), "n_draws": len(vals),
    }


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

GATES = [
    {"id": "G1", "pool": "puro", "surface": "corpus_test_split0",
     "order": "born_at", "generator": None,
     "protocol": "split 0 only — NOT the five-split mean (trap 5.6)",
     "target": 0.5216, "tol": 0.0002, "kind": "record",
     "source": "results3/order_search.json::references_split0.born_at_test"},
    {"id": "G2", "pool": "puro", "surface": "corpus_test_split0",
     "order": "random", "generator": GEN_RECORD,
     "protocol": "the order_search.py generator (trap 5.5), split 0 only",
     "target": 0.4227, "tol": 0.002, "kind": "record",
     "sd_target": None,
     "source": "results3/order_search.json::references_split0.random_test_mean"},
    {"id": "G3", "pool": "puro", "surface": CORPUS_FULL,
     "order": "born_at", "generator": None,
     "protocol": "all 2000 indices",
     "target": 0.5115, "tol": 0.0002, "kind": "probe",
     "source": "CHAT_SUMMARY.md §2.1 erratum of 2026-08-12, "
               "cited in ARBITRATION_REPORT.md §2. No record owns it."},
    {"id": "G4", "pool": "puro", "surface": CORPUS_FULL,
     "order": "random", "generator": GEN_RECORD,
     "protocol": "the order_search.py generator (trap 5.5), all 2000 indices",
     "target": 0.4172, "tol": 0.002, "kind": "probe", "sd_target": 0.0711,
     "source": "CHAT_SUMMARY.md §2.1 erratum of 2026-08-12, "
               "cited in ARBITRATION_REPORT.md §2. No record owns it."},
    {"id": "G5", "pool": "puro", "surface": SPACE,
     "order": "born_at", "generator": None,
     "protocol": "space_pools, normalised by n",
     "target": 0.3148, "tol": 0.0002, "kind": "record",
     "source": "results3/FINDINGS3.md erratum of 2026-08-08, and "
               "results3/budget_and_balance_ls.json::references['born_at espacio']"},
    {"id": "G6", "pool": "puro", "surface": SPACE,
     "order": "random", "generator": GEN_MODULE,
     "protocol": "random_order(ids, seed), seeds 0..49 (trap 5.5)",
     "target": 0.3768, "tol": 0.002, "kind": "record", "sd_target": 0.1026,
     "source": "results3/FINDINGS3.md erratum of 2026-08-08"},
]


def gate_rows(instances, families, randoms):
    """
    Every gate row evaluated under the protocol NAMED IN THE ROW.

    `randoms` is {(generator, surface, pool): the summary of its 50 draws}; the
    generator is part of the key precisely because the record's six figures did
    not all come from the same one.
    """
    rows = []
    for g in GATES:
        key = (g["surface"], g["pool"])
        if g["order"] == "random":
            summ = randoms[(g["generator"], g["surface"], g["pool"])]
            got = summ["mean"]
            sd = {"pstdev": summ["pstdev"], "stdev": summ["stdev"]}
        else:
            got = floor(families[g["order"]], instances[key])
            sd = None
        d = abs(got - g["target"])
        row = dict(g)
        row.update({"measured": round(got, 6), "delta": round(d, 6),
                    "passes": d <= g["tol"]})
        if sd is not None:
            row["measured_sd"] = {k: round(v, 6) for k, v in sd.items()}
            row["sd_is_blocking"] = False       # the plan writes it "sd ≈", not "±"
            if g.get("sd_target") is not None:
                row["sd_delta"] = {k: round(abs(v - g["sd_target"]), 6)
                                   for k, v in sd.items()}
        rows.append(row)
    return rows


def gate_generators_differ_only_in_the_rng(ids, rules):
    """
    The record's generator shuffles the APPEARANCE order and the module's sorts
    first. Over this base the two are the same list, so the difference measured
    in trap 5.5 is the RNG and nothing else. Checked, not assumed: on a base
    where it stopped holding, the two generators would differ for a second
    reason and the gate rows would stop isolating the one being described.
    """
    appearance = [r["rule_id"] for r in rules]
    return {
        "what": "the rules' appearance order in results/llm_run.json against "
                "sorted(ids). If they are equal, the only thing separating the "
                "two random generators is how the RNG is advanced.",
        "appearance_equals_sorted": appearance == sorted(ids),
        "n_rules": len(appearance),
    }


# ---------------------------------------------------------------------------
# The floors
# ---------------------------------------------------------------------------

def deterministic_rows(families, instances):
    """One row per (order family, pool, surface). The label is on the line."""
    rows = []
    for fam, order in families.items():
        for (surface, pool), inst in instances.items():
            rows.append({
                "order": fam, "generator": None, "pool": pool,
                "surface": surface, "value": round(floor(order, inst), 6),
                "n_cases": inst[3],
            })
    return rows


def random_rows(randoms):
    rows = []
    for (gen, surface, pool), summ in randoms.items():
        rows.append({
            "order": "random", "generator": gen, "pool": pool,
            "surface": surface, "value": round(summ["mean"], 6),
            "aggregation": f"mean of {summ['n_draws']} draws",
            "pstdev": round(summ["pstdev"], 6),
            "stdev": round(summ["stdev"], 6),
            "min": round(summ["min"], 6), "max": round(summ["max"], 6),
        })
    return rows


def five_split_rows(rows):
    """
    The five-split mean, built from the per-split rows and labelled as the
    DOUBLE aggregation it is for the random families.

    Split 0 is one of the five. It is also the record's index set, and it keeps
    its own row: reporting only the mean would silently drop the only figure
    that reproduces 0.5216 (trap 5.6).
    """
    out = []
    by_key = {}
    for r in rows:
        if not r["surface"].startswith("corpus_test_split"):
            continue
        by_key.setdefault((r["order"], r["generator"], r["pool"]), []).append(r)
    for (order, gen, pool), group in by_key.items():
        group.sort(key=lambda r: r["surface"])
        vals = [r["value"] for r in group]
        agg = (f"mean over {len(vals)} splits of the mean over {N_RANDOM} draws"
               if order == "random" else f"mean over {len(vals)} splits")
        out.append({
            "order": order, "generator": gen, "pool": pool,
            "surface": "corpus_test_5splits",
            "value": round(statistics.mean(vals), 6),
            "aggregation": agg,
            "per_split": [{"split": int(r["surface"][-1]),
                           "seed": SPLIT_SEED + int(r["surface"][-1]),
                           "value": r["value"], "n_cases": r.get("n_cases")}
                          for r in group],
        })
    return out


# ---------------------------------------------------------------------------

def measure():
    """Everything but the printing and the file. Returns (payload, ok)."""
    t_start = time.time()
    corpus, rules, ext, conds = load()
    ids = [r["rule_id"] for r in rules]
    action = {r["rule_id"]: r["action"] for r in rules}
    born = {r["rule_id"]: r["born_at"] for r in rules}
    below = subsumption_below(rules, ext)
    matched, undef, truth = build_tables(corpus, rules, conds, below)
    corpus_pool = {"puro": matched, "hibrido": undef}

    sets = index_sets_of(corpus, truth)
    instances = corpus_instances(ids, corpus_pool, truth, action, sets)
    spools = space_pools(ids, conds, action, below)
    for name in POOLS:
        M, W, full, n = spools[name]
        instances[(SPACE, name)] = (M, W, full, n)
    n_space = spools["puro"][3]

    families = order_families(ids, born)
    draws = {GEN_MODULE: module_random_orders(ids),
             GEN_RECORD: record_random_orders(ids)}
    randoms = {}
    for gen, orders in draws.items():
        for key, inst in instances.items():
            randoms[(gen, *key)] = random_floor(orders, inst)

    g_rows = gate_rows(instances, families, randoms)
    g_ids = gate_generators_differ_only_in_the_rng(ids, rules)
    passes = all(r["passes"] for r in g_rows) and g_ids["appearance_equals_sorted"]

    rows = deterministic_rows(families, instances) + random_rows(randoms)
    rows += five_split_rows(rows)
    rows.sort(key=lambda r: (r["order"], r["generator"] or "", r["pool"],
                             r["surface"]))

    payload = {
        "_env": environment(n_splits=N_SPLITS, n_random=N_RANDOM,
                            split_seed=SPLIT_SEED),
        "what":
            "what an order that searches for NOTHING scores, on both pools and "
            "on all three surfaces. The cell PLAN_PAIRWISE.md §3 marks NOT "
            "MEASURED — born_at over the hibrido pool — is the floor any "
            "declared order has to be scored against, and it did not exist "
            "before this record. Three further figures had no owning record "
            "either: born_at and the random mean over the FULL corpus, and "
            "reversed born_at over the space. No search of any kind; no API "
            "calls; results/llm_run.json is read-only.",
        "carries_no_prediction":
            "PLAN_PAIRWISE.md §0.1. P-a and P-b predicted these figures and "
            "were measured on 2026-08-24 before anybody signed them, so they "
            "are spent and are not restored. Nothing here may be reported as a "
            "band that held. What the stage keeps is giving the figures an "
            "owner, a script and an _env.",
        "surface_note":
            "corpus_full is the 2000 draws of the modelled arrival distribution "
            "at seed 17; corpus_test_split0 is split(corpus, truth, seed=17)[1], "
            "the record's own index set and the only one that reproduces 0.5216 "
            "and 0.4227; corpus_test_5splits is the mean over seeds 17..21 and "
            "is the more stable statistic but reproduces neither; space is the "
            "uniform measure over all 134,400 attribute combinations. Over the "
            "same 2,080 pairs the two surfaces rank at Spearman 0.34: a figure "
            "on one cannot be reweighted into a figure on the other.",
        "pool_note":
            "puro is first-match-wins over a total order with subsumption OFF. "
            "hibrido is subsumption as a non-overridable base level plus a "
            "declared order on top, which is where declared edges live. They "
            "are different machines and their figures never chain.",
        "generator_note":
            "trap 5.5 of PLAN_PAIRWISE.md. Two random-order generators exist in "
            "the tree and they disagree; the record's corpus figures came from "
            "one and its space figure from the other, and no single generator "
            "reproduces all three. Every random row names its generator.",
        "n_rules": len(ids), "n_cases": len(corpus), "n_space": n_space,
        "splits": {test_split_name(s): {"seed": SPLIT_SEED + s,
                                        "n_test": len(sets[test_split_name(s)])}
                   for s in range(N_SPLITS)},
        "gates": {
            "what": "six figures that are NOT new and must come out. Four gate "
                    "against a record and two against an unowned probe; `kind` "
                    "says which per row. A probe that gates is still a probe. "
                    "A miss on G2, G4 or G6 is a generator mismatch until "
                    "proven otherwise.",
            "rows": g_rows,
            "generators_differ_only_in_the_rng": g_ids,
            "passes": passes,
        },
        "floors": rows,
        "seconds": round(time.time() - t_start, 1),
    }
    return payload, passes


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    only_checks = "--checks" in argv

    print("=" * 78)
    print("THE FLOOR BY POOL — what an order that searches for nothing scores")
    print("=" * 78)
    print("  no search, no multi-start, no API calls; results/llm_run.json "
          "read-only")
    print("  PLAN_PAIRWISE.md stage A. It carries NO prediction: P-a and P-b "
          "were")
    print("  spent before signature (§0.1) and are not restored.")
    print(f"  {describe()}")

    payload, passes = measure()

    print()
    print("=" * 78)
    print("REPRODUCTION GATE — runs first, blocking")
    print("=" * 78)
    print(f"  {'':>3}{'pool':<8}{'surface':<22}{'order':<18}"
          f"{'measured':>10}{'target':>9}{'kind':>8}")
    for r in payload["gates"]["rows"]:
        print(f"  {r['id']:<3}{r['pool']:<8}{r['surface']:<22}{r['order']:<18}"
              f"{r['measured']:>10.4f}{r['target']:>9.4f}{r['kind']:>8}"
              f"{'  ok' if r['passes'] else '  NO'}")
        if r.get("measured_sd"):
            tgt = r.get("sd_target")
            print(f"      sd pstdev {r['measured_sd']['pstdev']:.4f} · "
                  f"stdev {r['measured_sd']['stdev']:.4f}"
                  + (f" · published {tgt}" if tgt is not None else "")
                  + "   (reported, not blocking)")
    g_ids = payload["gates"]["generators_differ_only_in_the_rng"]
    print(f"  appearance order == sorted(ids): "
          f"{g_ids['appearance_equals_sorted']}")
    if not passes:
        print()
        print("  STOP. A miss means the pool construction, the index set or the")
        print("  generator differs from the record's, and that has to be "
              "understood")
        print("  before a new figure is added on top. Do not adjust to fit "
              "(hard rule 6).")
        return 1
    print("\n  GATE PASSES, 6/6 rows.")

    if only_checks:
        print(f"\n  gate only. total cost: {payload['seconds']:.0f}s")
        return 0

    print()
    print("=" * 78)
    print("THE FLOORS — every line names its surface, its pool and, for a "
          "random")
    print("baseline, its generator")
    print("=" * 78)
    for surface in (CORPUS_FULL, "corpus_test_split0", "corpus_test_5splits",
                    SPACE):
        print(f"\n  SURFACE {surface}")
        print(f"    {'order':<18}{'generator':<22}{'puro':>9}{'hibrido':>9}")
        seen = {}
        for r in payload["floors"]:
            if r["surface"] != surface:
                continue
            gen = "—" if r["generator"] is None else (
                "random_order" if r["generator"] == GEN_MODULE
                else "order_search.py")
            seen.setdefault((r["order"], gen), {})[r["pool"]] = r["value"]
        for (order, gen), v in sorted(seen.items()):
            print(f"    {order:<18}{gen:<22}"
                  f"{v.get('puro', float('nan')):>9.4f}"
                  f"{v.get('hibrido', float('nan')):>9.4f}")

    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {payload['seconds']:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
