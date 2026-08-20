"""
P4 AND P5 OF `PLAN_ORDER_METRICS.md` — the orders behind figures already
published, measured as orders.

--------------------------------------------------------------------------
WHY THIS FILE EXISTS AND WHY IT REGENERATES INSTEAD OF READING
--------------------------------------------------------------------------
No record in `results*/` holds an order produced by the audited optimizer. The
only complete order the repository has ever stored is the superseded rung-3
greedy in `order_search.json` (G1). `multistart` scored 65 permutations per
configuration and returned one; the rest died inside its loop. So the orders
this measures cannot be read off disk — they have to be produced again, from
the same seed, the same starts and the same instance, and then SHOWN to be the
same objects.

That last step is the parity gate below, and it is blocking: every regenerated
`train_score`, `test` and `space` must equal the published value exactly. What
makes a regenerated order the published order is those three numbers agreeing,
NOT the provenance digest — `code_digest` necessarily differs from the one in
the records, because `local_search.py` gained `keep_orders` and
`order_search_ls.py` gained `space_truth_masks` after they were written.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It does not run `budget_and_balance_ls`, `order_search_ls`, `budget_and_balance`
or any `sweep*`: all of them dump JSON over published records. It imports their
functions and calls them, which is the same arithmetic with none of the
writing. The only file it writes is `results3/order_metrics.json`, which is new.

It does not consult the oracle. The truth by class comes from
`order_search_ls.space_truth_masks`, in a module the pinned list already allows.

It does not tune anything. `MULTISTART_SEED`, `MULTISTART_STARTS` and
`DECLARED_NEIGHBOURHOOD` are untouched; the 257-start rows are a DIAGNOSTIC, in
exactly the sense `start_budget_check` declared, and nothing measured here is an
argument for moving a constant.

--------------------------------------------------------------------------
THE NESTED-PREFIX SHORTCUT, AND WHY IT IS CHECKED BEFORE IT IS USED
--------------------------------------------------------------------------
`declared_starts` draws its shuffles from `random.Random(17)` in sequence, so
the first 65 starts of a 257-start run ARE the 65 of a 65-start run. Running
257 once per split and reading the smaller budgets off its prefix therefore
gives the same answer as three separate runs, at 136 s instead of 237 s — with
the tie-break to the lowest index, which is what `multistart` applies.

"Therefore" is not good enough for something three figures rest on, so
`validate_prefix_shortcut` runs an independent 65-start search on one split and
requires the same winner, the same end score and the same order, rule for rule.

Usage:  python3 -m rung3.order_metrics_run
        python3 -m rung3.order_metrics_run --checks   (parity gate only)
"""

from __future__ import annotations

import hashlib
import json
import statistics
import sys
import time
from itertools import combinations
from pathlib import Path

from harness.provenance import describe, environment
from rung3.budget_and_balance import greedy as greedy_from_record
from rung3.budget_and_balance_ls import load_instance, start_spread, subsample
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS, build_masks,
                                   declared_starts, multistart, score_order)
from rung3.order_metrics import (behavioural_distance, conflicting_pairs,
                                    decisions, pair_census,
                                    per_class_disagreement, positions_moved,
                                    signature, tau, winners,
                                    attribution_agreement)
from rung3.order_search_ls import space_pools, space_truth_masks

OUT = Path("results3")
RECORD = "order_metrics.json"
POOL = "puro"
SURFACE = "espacio exhaustivo"

# The budgets, in STARTS: `declared_starts(n=64|128|256)` plus the greedy at
# index 0. The record names them 65 / 129 / 257 and so does this.
BUDGETS = (65, 129, 257)
BIGGEST = max(BUDGETS)

# A and C: the two splits where `start_budget_check` saw the best train score
# move, so Q-a is not answered on one split.
SPLITS_FULL = (0, 4)

# B: the whole 1% band, five splits by five draws. Q-b is evaluated on
# (split 0, draw 0) — the cell §0 names — where 40 of 65 starts tie, not the
# 56.44 that is the band's mean.
FRACTION_B = 0.01
SPLIT_B, DRAW_B = 0, 0

PUBLISHED_A = OUT / "start_budget_check.json"
PUBLISHED_B = OUT / "budget_and_balance_ls.json"

# The classes §0 bets on, and the one every reversed order collapses to.
SCARCE_CLASSES = ("ACCOUNT_MANAGER", "T3_ENGINEERING")


# ---------------------------------------------------------------------------
# The instance: the record's, plus the space it is measured on
# ---------------------------------------------------------------------------

def build_instance():
    t0 = time.time()
    inst = load_instance()
    spools = space_pools(inst["ids"], inst["conds"], inst["action"],
                         inst["below"])
    sM, sW, sfull, sn = spools[POOL]
    inst.update({
        "space": (sM, sW, sfull, sn),
        "truth_space": space_truth_masks(),
        "conflicting": conflicting_pairs(inst["ids"], sM, inst["action"]),
        "census": pair_census(inst["ids"], sM, inst["action"]),
        "seconds_setup": round(time.time() - t0, 1),
    })
    return inst


def masks_for(inst, idxs):
    return build_masks(inst["ids"], inst["matched"], inst["truth"],
                       inst["action"], idxs)


def scores_of(inst, order, train_masks, n_train, test_masks, n_test):
    """The three numbers the parity gate compares, computed the way
    `start_budget_check` and `run_config` compute them."""
    sM, sW, sfull, sn = inst["space"]
    tM, tW, tfull = test_masks
    M, W, full = train_masks
    return {
        "train_score": score_order(order, M, W, full),
        "train": round(score_order(order, M, W, full) / n_train, 4),
        "test": round(score_order(order, tM, tW, tfull) / n_test, 4),
        "space": round(score_order(order, sM, sW, sfull) / sn, 4),
    }


# ---------------------------------------------------------------------------
# Regeneration
# ---------------------------------------------------------------------------

def run_full_supervision(inst, s):
    """One 257-start search on split `s` at full supervision, keeping every end
    order. The 65 and 129 budgets come off its prefix."""
    tr, te = inst["splits"][s]
    train_masks = masks_for(inst, tr)
    test_masks = masks_for(inst, te)
    greedy = greedy_from_record(inst["rules"], inst["matched"], inst["truth"],
                                inst["action"], tr)
    starts = declared_starts(inst["ids"], first=greedy, n=BIGGEST - 1)
    if len(starts) != BIGGEST:
        raise ValueError("el presupuesto declarado no cuadra con los arranques")
    t0 = time.time()
    _best, st = multistart(starts, *train_masks,
                           neighbourhood=DECLARED_NEIGHBOURHOOD,
                           keep_orders=True)
    return {"split": s, "stats": st, "greedy": greedy, "n_train": len(tr),
            "n_test": len(te), "train_masks": train_masks,
            "test_masks": test_masks, "seconds": round(time.time() - t0, 1)}


def prefix_winner(rows, k):
    """The winner among the first `k` starts, with `multistart`'s tie-break:
    strictly greater wins, so a tie goes to the lowest index."""
    best = None
    for row in rows[:k]:
        if best is None or row["end_score"] > best["end_score"]:
            best = row
    return best


def validate_prefix_shortcut(inst, run):
    """An independent 65-start search must give the prefix's answer exactly."""
    s = run["split"]
    tr, _te = inst["splits"][s]
    starts = declared_starts(inst["ids"], first=run["greedy"])
    t0 = time.time()
    best, st = multistart(starts, *run["train_masks"],
                          neighbourhood=DECLARED_NEIGHBOURHOOD)
    row = prefix_winner(run["stats"]["rows"], MULTISTART_STARTS + 1)
    output = {
        "split": s,
        "starts": len(starts),
        "independent_best_score": st["best_score"],
        "prefix_best_score": row["end_score"],
        "independent_best_index": st["best_from_index"],
        "prefix_best_index": row["index"],
        "same_order": best == row["order"],
        "same_rows": [r["end_score"] for r in st["rows"]] ==
                     [r["end_score"] for r in run["stats"]["rows"][:len(starts)]],
        "seconds": round(time.time() - t0, 1),
    }
    output["passes"] = (output["independent_best_score"] == output["prefix_best_score"]
                        and output["independent_best_index"] == output["prefix_best_index"]
                        and output["same_order"] and output["same_rows"])
    return output


def run_band_1pct(inst):
    """The whole 1% band: five splits by five draws, keeping every end order.
    Regenerated whole because a single cell cannot say whether it is typical."""
    rows = []
    for s in range(len(inst["splits"])):
        tr, te = inst["splits"][s]
        test_masks = masks_for(inst, te)
        for d in range(5):
            sub = subsample(tr, FRACTION_B, s, d)
            train_masks = masks_for(inst, sub)
            greedy = greedy_from_record(inst["rules"], inst["matched"],
                                        inst["truth"], inst["action"], sub)
            t0 = time.time()
            best, st = multistart(declared_starts(inst["ids"], first=greedy),
                                  *train_masks,
                                  neighbourhood=DECLARED_NEIGHBOURHOOD,
                                  keep_orders=True)
            sc = scores_of(inst, best, train_masks, len(sub), test_masks, len(te))
            rows.append({
                "split": s, "draw": d, "labels": len(sub), "stats": st,
                "ls_train": round(st["best_score"] / len(sub), 4),
                "ls_test": sc["test"], "ls_space": sc["space"],
                "spread": start_spread(st),
                "seconds": round(time.time() - t0, 1),
            })
    return rows


# ---------------------------------------------------------------------------
# The parity gate — blocking
# ---------------------------------------------------------------------------

def parity_full_supervision(inst, runs):
    """Every budget of every regenerated split against
    `start_budget_check.json`. Read from the file, never from a constant here:
    a gate that carries its own expectation is not a gate."""
    pub = json.loads(PUBLISHED_A.read_text())
    rows = []
    for run in runs:
        for k in BUDGETS:
            row = prefix_winner(run["stats"]["rows"], k)
            sc = scores_of(inst, row["order"], run["train_masks"],
                           run["n_train"], run["test_masks"], run["n_test"])
            expected = next(r for r in pub["rows"]
                            if r["split"] == run["split"] and r["starts"] == k)
            comp = {m: (sc[m], expected[m], sc[m] == expected[m])
                    for m in ("train_score", "train", "test", "space")}
            rows.append({
                "split": run["split"], "starts": k,
                "best_from_index": row["index"], "best_from": row["start"],
                "n_at_best": sum(1 for r in run["stats"]["rows"][:k]
                                 if r["end_score"] == row["end_score"]),
                "published_n_at_best": expected["n_at_best"],
                "end_score_distinct": len({r["end_score"]
                                           for r in run["stats"]["rows"][:k]}),
                "published_end_score_distinct": expected["end_score_distinct"],
                "comparison": comp,
                "passes": all(v[2] for v in comp.values()),
            })
    return rows


def parity_band(inst, rows):
    """The 1% band against `budget_and_balance_ls.json::label_budget_runs`."""
    pub = json.loads(PUBLISHED_B.read_text())
    output = []
    for f in rows:
        expected = next(r for r in pub["label_budget_runs"]
                        if r["fraction"] == FRACTION_B
                        and r["split"] == f["split"] and r["draw"] == f["draw"])
        comp = {m: (f[m], expected[m], f[m] == expected[m])
                for m in ("ls_train", "ls_test", "ls_space")}
        comp["n_at_best"] = (f["spread"]["n_at_best"], expected["n_at_best"],
                             f["spread"]["n_at_best"] == expected["n_at_best"])
        output.append({"split": f["split"], "draw": f["draw"],
                       "comparison": comp,
                       "passes": all(v[2] for v in comp.values())})
    return output


# ---------------------------------------------------------------------------
# Measuring a set of orders
# ---------------------------------------------------------------------------

def digest(sig):
    """A short, stable name for a behavioural signature. The signature itself is
    exact — the masks whole — and this is what a record can carry."""
    h = hashlib.sha1()
    for a, m in sig[0]:
        h.update(a.encode())
        h.update(m.to_bytes((m.bit_length() + 7) // 8 or 1, "big"))
    h.update(b"|undecided|")
    u = sig[1]
    h.update(u.to_bytes((u.bit_length() + 7) // 8 or 1, "big"))
    return h.hexdigest()[:12]


def summary(values):
    if not values:
        return None
    v = sorted(values)
    return {"n": len(v), "min": v[0], "p25": v[len(v) // 4],
            "median": statistics.median(v), "mean": round(statistics.mean(v), 6),
            "p75": v[(3 * len(v)) // 4], "max": v[-1]}


def spearman(xs, ys):
    """Rank correlation, with average ranks for ties. Stdlib only, and written
    out because the whole of Q-d is one number that comes from it."""
    if len(xs) < 2:
        return None

    def rangos(vs):
        rank_idx = sorted(range(len(vs)), key=lambda i: vs[i])
        r = [0.0] * len(vs)
        i = 0
        while i < len(rank_idx):
            j = i
            while j + 1 < len(rank_idx) and vs[rank_idx[j + 1]] == vs[rank_idx[i]]:
                j += 1
            middle = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[rank_idx[k]] = middle
            i = j + 1
        return r

    rx, ry = rangos(xs), rangos(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx)
    dy = sum((b - my) ** 2 for b in ry)
    return round(num / (dx * dy) ** 0.5, 4) if dx and dy else None


def decisions_and_signatures(inst, orders):
    """One sweep per order over the space, and the name of what it decides."""
    sM, _sW, sfull, _sn = inst["space"]
    dec = [decisions(o, sM, inst["action"], sfull) for o in orders]
    return dec, [digest(signature(d, u)) for d, u in dec]


def pairwise(inst, orders, dec, with_taus=True):
    """
    Every pair of a set of end orders: behavioural distance, positional churn
    and the two taus.

    Computed ONCE on the largest set and sliced by index for the smaller
    budgets, because the budgets are nested — the 65 orders of a 65-start run
    are the first 65 rows of the 257-start run — and the restricted tau costs
    4 ms a pair, which over 32,896 pairs is the dominant cost of this file.
    """
    _sM, _sW, sfull, sn = inst["space"]
    pairs = []
    for i, j in combinations(range(len(orders)), 2):
        _agree, dis, undecided = behavioural_distance(dec[i][0], dec[j][0], sfull)
        churn = positions_moved(orders[i], orders[j])
        row = {"i": i, "j": j, "disagree": dis, "undecided_either": undecided,
               "rate": round(dis / sn, 6),
               "moved": churn["moved"],
               "moved_fraction": round(churn["fraction_moved"], 4),
               "displacement_median": churn["median"]}
        if with_taus:
            row["tau"] = round(tau(orders[i], orders[j]), 4)
            row["tau_conflicting"] = round(
                tau(orders[i], orders[j], inst["conflicting"]), 4)
        pairs.append(row)
    return pairs


def slice_pairs(pairs, k):
    """The sub-matrix of the first `k` orders."""
    return [p for p in pairs if p["i"] < k and p["j"] < k]


def summarize(labels, digests, pairs, n_orders):
    """What the record carries about a set: the summaries, never the orders."""
    rates = [p["rate"] for p in pairs]
    out = {
        "labels": labels,
        "n_orders": n_orders,
        "n_pairs": len(pairs),
        "n_distinct_signatures": len(set(digests[:n_orders])),
        "signatures": digests[:n_orders],
        "undecided_either_max": max((p["undecided_either"] for p in pairs),
                                    default=0),
        "disagreement": summary([p["disagree"] for p in pairs]),
        "disagreement_rate": summary([round(t, 6) for t in rates]),
        "moved_fraction": summary([p["moved_fraction"] for p in pairs]),
        "pairs_identical_behaviour": sum(1 for p in pairs if p["disagree"] == 0),
        "pairs_identical_behaviour_but_moved": sum(
            1 for p in pairs if p["disagree"] == 0 and p["moved"] > 0),
    }
    if pairs and "tau" in pairs[0]:
        out["tau"] = summary([p["tau"] for p in pairs])
        out["tau_conflicting"] = summary([p["tau_conflicting"] for p in pairs])
        out["spearman_tau_vs_disagreement"] = spearman(
            [p["tau"] for p in pairs], rates)
        out["spearman_tau_conflicting_vs_disagreement"] = spearman(
            [p["tau_conflicting"] for p in pairs], rates)
    return out


def per_class_over_pairs(inst, dec, pairs, cuantos=None):
    """
    Per-class disagreement pooled over pairs: total disagreements of the class
    over total cases of the class, summed across pairs.

    Pooled rather than averaged, so that the denominator is the same object the
    overall rate divides by, and the comparison Q-f asks for — class rate
    against overall rate — is between two quantities built the same way.
    """
    _sM, _sW, _sfull, sn = inst["space"]
    truth = inst["truth_space"]
    acc = {c: 0 for c in truth}
    tot = {c: 0 for c in truth}
    used_names = pairs if cuantos is None else pairs[:cuantos]
    for p in used_names:
        share = per_class_disagreement(dec[p["i"]][0], dec[p["j"]][0], truth)
        for c, v in share.items():
            acc[c] += v["disagree"]
            tot[c] += v["n"]
    overall = sum(acc.values()) / sum(tot.values()) if used_names else None
    return {
        "n_pairs": len(used_names),
        "overall_rate": round(overall, 6) if overall is not None else None,
        "by_class": {c: {"n_per_pair": truth[c].bit_count(),
                         "rate": round(acc[c] / tot[c], 6),
                         "ratio_to_overall": round((acc[c] / tot[c]) / overall, 3)
                         if overall else None}
                     for c in sorted(truth)},
    }


def pair_report(inst, a, b, name):
    """Everything about one named pair, which is what a finding cites."""
    sM, _sW, sfull, sn = inst["space"]
    action = inst["action"]
    dA, uA = decisions(a, sM, action, sfull)
    dB, uB = decisions(b, sM, action, sfull)
    agree, dis, undecided = behavioural_distance(dA, dB, sfull)
    wA, _ = winners(a, sM, sfull)
    wB, _ = winners(b, sM, sfull)
    same = attribution_agreement(wA, wB)
    churn = positions_moved(a, b)
    share = per_class_disagreement(dA, dB, inst["truth_space"])
    return {
        "what": name,
        "agree": agree, "disagree": dis, "undecided_either": undecided,
        "disagreement_rate": round(dis / sn, 6),
        "same_signature": signature(dA, uA) == signature(dB, uB),
        "same_rule_where_they_agree": same,
        "agree_for_different_reasons": agree - same,
        "moved": churn["moved"],
        "moved_fraction": round(churn["fraction_moved"], 4),
        "displacement_max": churn["max"],
        "displacement_median": churn["median"],
        "tau": round(tau(a, b), 4),
        "tau_conflicting": round(tau(a, b, inst["conflicting"]), 4),
        "per_class": {c: {"n": v["n"], "disagree": v["disagree"],
                          "rate": round(v["rate"], 6)}
                      for c, v in sorted(share.items())},
    }


# ---------------------------------------------------------------------------
# The predictions of §0, evaluated exactly as they are written
# ---------------------------------------------------------------------------
#
# NOT re-specified after seeing the numbers. P3 recorded that being a
# conflicting pair is necessary and not sufficient — some conflicting pairs are
# inert in a given order because they co-match nowhere still pending — which
# weakens the premise Q-d rests on. That nuance goes in the report and in the
# findings; it does not go in the formula. Changing the measure after seeing the
# premise limp is what §0 exists to prevent.

def evaluate_predictions(inst, sets, pairs, band, cited, per_class):
    _sM, _sW, _sfull, sn = inst["space"]
    q = {}

    # ---- Q-a: the winner at 65 against the winner at 257, split 0
    pair = cited["qa_split0"]
    q["Q-a"] = {
        "claim": "the winner at 65 starts and the winner at 257 disagree on "
                 ">= 6,910 cases of the space (5.1%); below 3,455 the harness "
                 "is wrong, not the prediction",
        "measured": pair["disagree"],
        "rate": pair["disagreement_rate"],
        "floor_arithmetic": 3455, "threshold": 6910,
        "verdict": ("HARNESS SUSPECT" if pair["disagree"] < 3455
                    else "HOLDS" if pair["disagree"] >= 6910 else "REFUTED"),
        "second_split": cited["qa_split4"]["disagree"],
        "second_split_rate": cited["qa_split4"]["disagreement_rate"],
    }

    # ---- Q-b: the tied set at 1%, split 0 draw 0
    b = sets["b_tied_split0_draw0"]
    mediana = b["disagreement"]["median"]
    q["Q-b"] = {
        "claim": "among the orders tying at the best train score at 1% "
                 "(split 0, draw 0), the median pairwise disagreement over the "
                 "space is above 20% (26,880 cases); a median below 5% refutes",
        "n_tied": b["n_orders"], "n_pairs": b["n_pairs"],
        "median": mediana, "median_rate": round(mediana / sn, 6),
        "threshold": 26880, "refutation_below": 6720,
        "verdict": ("HOLDS" if mediana > 26880
                    else "REFUTED" if mediana < 6720 else "NEITHER"),
        "band_context": band,
    }

    # ---- Q-c: 65 distinct signatures, and best against runner-up
    c = sets["split0_starts65"]
    ru = cited["qc_split0"]
    q["Q-c"] = {
        "claim": "at full supervision the 65 end orders give 65 distinct "
                 "behavioural signatures, and the best against the runner-up "
                 "disagree on more than 2% of the space (2,688) while <= 2 "
                 "train cases apart",
        "n_distinct_signatures": c["n_distinct_signatures"],
        "n_orders": c["n_orders"],
        "best_vs_runner_up": ru["disagree"],
        "best_vs_runner_up_rate": ru["disagreement_rate"],
        "train_gap_cases": cited["qc_train_gap"],
        "verdict": ("REFUTED" if c["n_distinct_signatures"] < c["n_orders"]
                    or ru["disagreement_rate"] < 0.005
                    else "HOLDS" if ru["disagreement_rate"] > 0.02
                    else "NEITHER"),
    }

    # ---- Q-d: does a rank statistic track behaviour, and does restricting help
    d = sets["split0_starts257"]
    g = abs(d["spearman_tau_vs_disagreement"])
    r = abs(d["spearman_tau_conflicting_vs_disagreement"])
    q["Q-d"] = {
        "claim": "|Spearman| of global tau against behavioural distance < 0.5, "
                 "and of tau restricted to the 35,457 conflicting pairs > 0.8; "
                 "the restricted metric failing to beat the global one refutes "
                 "the design premise",
        "measured_pairs": d["n_pairs"],
        "spearman_global": d["spearman_tau_vs_disagreement"],
        "spearman_conflicting": d["spearman_tau_conflicting_vs_disagreement"],
        "abs_global": round(g, 4), "abs_conflicting": round(r, 4),
        "restricted_beats_global": r > g,
        "verdict": ("REFUTED" if r <= g
                    else "HOLDS" if (g < 0.5 and r > 0.8) else "PARTIAL"),
        "second_split": {
            "spearman_global": sets["split4_starts257"]["spearman_tau_vs_disagreement"],
            "spearman_conflicting": sets["split4_starts257"][
                "spearman_tau_conflicting_vs_disagreement"]},
    }

    # ---- Q-e: churn overstates functional difference
    p257 = pairs["split0"]
    both = sum(1 for p in p257
               if p["moved_fraction"] > 0.6 and p["rate"] < 0.30)
    q["Q-e"] = {
        "claim": "more than 60% of rules sit at a different index between two "
                 "end orders while behavioural disagreement stays below 30%; "
                 "churn and disagreement of comparable size refutes",
        "median_moved_fraction": d["moved_fraction"]["median"],
        "median_disagreement_rate": d["disagreement_rate"]["median"],
        "pairs_over_60_churn_under_30_disagreement": both,
        "n_pairs": len(p257),
        "fraction_of_pairs": round(both / len(p257), 4),
        "verdict": ("HOLDS" if (d["moved_fraction"]["median"] > 0.6
                                and d["disagreement_rate"]["median"] < 0.30)
                    else "REFUTED"),
    }

    # ---- Q-f: disagreement concentrates where material is scarce
    ratios = {c_: per_class["pooled_split0_65"]["by_class"][c_]["ratio_to_overall"]
              for c_ in SCARCE_CLASSES}
    pair_ratios = {c_: round(pair["per_class"][c_]["rate"]
                             / (pair["disagreement_rate"] or 1), 3)
                   for c_ in SCARCE_CLASSES}
    q["Q-f"] = {
        "claim": "the per-class disagreement rate for ACCOUNT_MANAGER and "
                 "T3_ENGINEERING is at least twice the overall rate; either "
                 "class at or below the overall rate refutes",
        "pooled_over_pairs": {
            "n_pairs": per_class["pooled_split0_65"]["n_pairs"],
            "overall_rate": per_class["pooled_split0_65"]["overall_rate"],
            "by_class": {c_: per_class["pooled_split0_65"]["by_class"][c_]
                         for c_ in sorted(inst["truth_space"])}},
        "ratios_pooled": ratios,
        "ratios_on_the_Q_a_pair": pair_ratios,
        "verdict": ("REFUTED" if any(v <= 1.0 for v in ratios.values())
                    else "HOLDS" if all(v >= 2.0 for v in ratios.values())
                    else "PARTIAL"),
    }
    return q


def band_context(inst, band):
    """The rest of the 1% band, as context for Q-b and for nothing else: how
    many orders tie in each cell and how far apart the tied ones are."""
    out = []
    for f in band:
        rows = f["stats"]["rows"]
        best = max(r["end_score"] for r in rows)
        tied = [r["order"] for r in rows if r["end_score"] == best]
        dec, dig = decisions_and_signatures(inst, tied)
        pairs = pairwise(inst, tied, dec, with_taus=False)
        out.append({
            "split": f["split"], "draw": f["draw"],
            "n_tied": len(tied),
            "n_distinct_signatures": len(set(dig)),
            "median_disagreement": (summary([p["disagree"] for p in pairs])
                                    ["median"] if pairs else None),
            "median_rate": (round(summary([p["rate"] for p in pairs])["median"], 6)
                            if pairs else None),
        })
    return out


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    only_checks = "--checks" in argv
    t_start = time.time()

    print("=" * 78)
    print("P4 — THE ORDERS BEHIND THE FIGURES, MEASURED AS ORDERS")
    print("=" * 78)
    print(f"  optimizer: {DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} declared starts + the greedy (untouched)")
    print(f"  budgets {list(BUDGETS)} starts · splits {list(SPLITS_FULL)} · "
          f"pool {POOL} · surface {SURFACE}")
    print(f"  {describe()}")

    inst = build_instance()
    _sM, _sW, _sfull, sn = inst["space"]
    print(f"  instance ready in {inst['seconds_setup']}s: "
          f"{len(inst['ids'])} rules, {sn:,} cases")
    print(f"  pair census on the space: {inst['census']['pairs']:,} pairs, "
          f"{inst['census']['co_match']:,} co-match, "
          f"{inst['census']['conflicting']:,} conflict "
          f"({100 * inst['census']['conflicting'] / inst['census']['pairs']:.1f}%)")

    # ---------------------------------------------------------------- A and C
    print()
    print("REGENERATING, keeping every end order")
    runs = {}
    for s in SPLITS_FULL:
        runs[s] = run_full_supervision(inst, s)
        print(f"  split {s}: {BIGGEST} starts in {runs[s]['seconds']}s")

    shortcut = validate_prefix_shortcut(inst, runs[SPLITS_FULL[0]])
    print(f"\n  prefix shortcut, split {shortcut['split']}: an independent "
          f"{shortcut['starts']}-start run ({shortcut['seconds']}s)")
    print(f"    same best score {shortcut['independent_best_score']} == "
          f"{shortcut['prefix_best_score']}, same index "
          f"{shortcut['independent_best_index']} == {shortcut['prefix_best_index']}, "
          f"same order {shortcut['same_order']}, all 65 rows {shortcut['same_rows']}")
    if not shortcut["passes"]:
        print("\n  STOP: the prefix is not the independent run. The budgets "
              "derived from it would not be the measured ones.")
        return 1

    # ------------------------------------------------------------ parity gate
    pair_a = parity_full_supervision(inst, [runs[s] for s in SPLITS_FULL])
    print()
    print("PARITY GATE — against results3/start_budget_check.json")
    print(f"  {'split':>6}{'starts':>8}{'train_score':>13}{'train':>9}"
          f"{'test':>9}{'space':>9}{'n_at_best':>11}{'':>4}")
    for f in pair_a:
        c = f["comparison"]
        print(f"  {f['split']:>6}{f['starts']:>8}{c['train_score'][0]:>13}"
              f"{c['train'][0]:>9.4f}{c['test'][0]:>9.4f}{c['space'][0]:>9.4f}"
              f"{f['n_at_best']:>11}"
              f"{'  ok' if f['passes'] else '  NO':>4}")
        if not f["passes"]:
            for m, (mio, pub, ok) in c.items():
                if not ok:
                    print(f"        {m}: regenerated {mio} vs published {pub}")

    band = run_band_1pct(inst)
    pair_b = parity_band(inst, band)
    print()
    print("PARITY GATE — the 1% band against "
          "results3/budget_and_balance_ls.json")
    bad_ones = [f for f in pair_b if not f["passes"]]
    print(f"  {len(pair_b) - len(bad_ones)}/{len(pair_b)} cells reproduce exactly")
    for f in bad_ones:
        print(f"    split {f['split']} draw {f['draw']}: "
              + ", ".join(f"{m} regenerated {v[0]} vs published {v[1]}"
                          for m, v in f["comparison"].items() if not v[2]))
    cell = next(f for f in pair_b
                if f["split"] == SPLIT_B and f["draw"] == DRAW_B)
    print(f"  the cell Q-b names, split {SPLIT_B} draw {DRAW_B}: "
          f"{'reproduces' if cell['passes'] else 'DOES NOT REPRODUCE'}")

    if bad_ones or not all(f["passes"] for f in pair_a):
        print("\n  STOP: a parity failure means the regenerated orders are not "
              "the measured ones, and nothing below would be about them. "
              "Reported as G6.")
        return 1
    print("\n  PARITY: PASSES. The regenerated orders are the published ones.")
    if only_checks:
        print(f"\n  total cost: {time.time() - t_start:.0f}s")
        return 0

    # ----------------------------------------------------------- the measuring
    print()
    print("MEASURING")
    sets, pairs_by_split, dec_by_split = {}, {}, {}
    for s in SPLITS_FULL:
        t0 = time.time()
        orders = [r["order"] for r in runs[s]["stats"]["rows"]]
        dec, dig = decisions_and_signatures(inst, orders)
        pairs = pairwise(inst, orders, dec, with_taus=True)
        dec_by_split[s], pairs_by_split[f"split{s}"] = dec, pairs
        for k in BUDGETS:
            sets[f"split{s}_starts{k}"] = summarize(
                f"split {s}, fraction 1.0, {k} starts",
                dig, slice_pairs(pairs, k), k)
        print(f"  split {s}: {len(pairs):,} pairs in {time.time() - t0:.0f}s, "
              f"{sets[f'split{s}_starts257']['n_distinct_signatures']} distinct "
              f"signatures of {BIGGEST}")

    # the 1% cell Q-b names, and its tied set
    f_b = next(f for f in band if f["split"] == SPLIT_B and f["draw"] == DRAW_B)
    rows_b = f_b["stats"]["rows"]
    orders_b = [r["order"] for r in rows_b]
    dec_b, dig_b = decisions_and_signatures(inst, orders_b)
    pairs_b = pairwise(inst, orders_b, dec_b, with_taus=True)
    best_b = max(r["end_score"] for r in rows_b)
    tied = [r["index"] for r in rows_b if r["end_score"] == best_b]
    sets["b_all65_split0_draw0"] = summarize(
        f"split {SPLIT_B}, fraction 0.01, draw {DRAW_B}, all 65 end orders",
        dig_b, pairs_b, len(orders_b))
    idx = set(tied)
    pairs_tied = [p for p in pairs_b if p["i"] in idx and p["j"] in idx]
    sets["b_tied_split0_draw0"] = summarize(
        f"split {SPLIT_B}, fraction 0.01, draw {DRAW_B}, the {len(tied)} "
        f"orders tying at the best train score",
        [dig_b[i] for i in sorted(idx)], pairs_tied, len(tied))
    sets["b_tied_split0_draw0"]["tied_indices"] = sorted(idx)
    print(f"  1% cell (split {SPLIT_B}, draw {DRAW_B}): {len(tied)} tied "
          f"orders, {len(pairs_tied)} pairs, "
          f"{sets['b_tied_split0_draw0']['n_distinct_signatures']} distinct "
          f"signatures")

    context = band_context(inst, band)

    # ------------------------------------------------------ the cited pairs
    cited = {}
    for s in SPLITS_FULL:
        rows = runs[s]["stats"]["rows"]
        w65 = prefix_winner(rows, 65)
        w257 = prefix_winner(rows, 257)
        cited[f"qa_split{s}"] = pair_report(
            inst, w65["order"], w257["order"],
            f"split {s}: the winner at 65 starts against the winner at 257")
        cited[f"qa_split{s}"]["train_score_65"] = w65["end_score"]
        cited[f"qa_split{s}"]["train_score_257"] = w257["end_score"]
        cited[f"qa_split{s}"]["from_index_65"] = w65["index"]
        cited[f"qa_split{s}"]["from_index_257"] = w257["index"]

    rows0 = runs[SPLITS_FULL[0]]["stats"]["rows"][:65]
    sorted_ids = sorted(rows0, key=lambda r: (-r["end_score"], r["index"]))
    cited["qc_split0"] = pair_report(
        inst, sorted_ids[0]["order"], sorted_ids[1]["order"],
        "split 0, 65 starts: the best against the runner-up")
    cited["qc_train_gap"] = sorted_ids[0]["end_score"] - sorted_ids[1]["end_score"]

    # G5: where the greedy start's end order sits
    g5 = {}
    for s in SPLITS_FULL:
        pairs = pairs_by_split[f"split{s}"]
        from_greedy = [p["disagree"] for p in slice_pairs(pairs, 65)
                       if p["i"] == 0]
        resto = [p["disagree"] for p in slice_pairs(pairs, 65)
                 if p["i"] != 0]
        g5[f"split{s}"] = {
            "greedy_end_order_vs_others": summary(from_greedy),
            "all_other_pairs": summary(resto),
            "greedy_is_an_outlier": (
                summary(from_greedy)["median"] > summary(resto)["p75"]),
        }

    # G4: identical behaviour with a different order, on the real instance
    g4 = {}
    for name, pairs in list(pairs_by_split.items()) + [("b_all65", pairs_b)]:
        equal_ones = [p for p in pairs if p["disagree"] == 0 and p["moved"] > 0]
        g4[name] = {
            "pairs_identical_behaviour_but_moved": len(equal_ones),
            "example": (max(equal_ones, key=lambda p: p["moved"])
                        if equal_ones else None),
        }

    per_class = {
        "pooled_split0_65": per_class_over_pairs(
            inst, dec_by_split[SPLITS_FULL[0]],
            slice_pairs(pairs_by_split["split0"], 65)),
        "pooled_b_tied": per_class_over_pairs(inst, dec_b, pairs_tied),
    }

    q = evaluate_predictions(inst, sets, pairs_by_split, context, cited,
                             per_class)

    print()
    print("=" * 78)
    print("THE PREDICTIONS OF §0, AS WRITTEN")
    print("=" * 78)
    for k in sorted(q):
        print(f"  {k}: {q[k]['verdict']}")

    # ------------------------------------------------------------- the record
    payload = {
        "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            budgets=list(BUDGETS)),
        "what":
            "P4/P5 of PLAN_ORDER_METRICS.md: the end orders of the audited "
            "multi-start, regenerated and measured AS ORDERS rather than "
            "scored. Regenerated rows: full supervision on splits 0 and 4, "
            "budgets 65/129/257 starts, from results3/start_budget_check.json; "
            "and the WHOLE 1% band, 5 splits x 5 draws, from "
            "results3/budget_and_balance_ls.json::label_budget_runs. Q-b is "
            "evaluated on (split 0, draw 0), the cell §0 names, where 40 of 65 "
            "starts tie at the best train score — not the band mean of 56.44. "
            "The 65 and 129 budgets are read off the nested prefix of one "
            "257-start run per split, which is checked against an independent "
            "65-start run before it is used. The parity gate below is what "
            "makes a regenerated order the published order: every train_score, "
            "test and space equals the published value exactly. The _env "
            "code_digest DOES differ from the digest in those records, and "
            "must: local_search.py gained keep_orders and order_search_ls.py "
            "gained space_truth_masks after they were written. Identity of the "
            "orders is established by the three figures agreeing, not by the "
            "digest. The 257-start rows are a diagnostic in the same sense "
            "start_budget_check declared; MULTISTART_STARTS stays 64 because it "
            "was declared before the runs that used it, and nothing here is an "
            "argument about it.",
        "surface": SURFACE,
        "surface_note":
            "every distance, signature and per-class rate is over the "
            "exhaustive space of 134,400 cases, pure pool. The train, test and "
            "space figures of the parity gate are the record's own surfaces: "
            "the labelled subset, corpus test, and the same space.",
        "pool": POOL,
        "n_rules": len(inst["ids"]),
        "n_space": sn,
        "n_conflicting_pairs": inst["census"]["conflicting"],
        "pair_census_space_pure": inst["census"],
        "budgets": list(BUDGETS),
        "splits": list(SPLITS_FULL),
        "fraction": FRACTION_B,
        "prefix_shortcut": shortcut,
        "parity_full_supervision": pair_a,
        "parity_band_1pct": pair_b,
        "sets": sets,
        "pairs_stored":
            "the full triangle is stored for the 65-order set of split 0 and "
            "for the tied set of the 1% cell; for the 257-order sets only the "
            "summaries, because 32,896 rows per split is a record nobody reads",
        "pairs_split0_starts65": slice_pairs(pairs_by_split["split0"], 65),
        "pairs_b_tied": pairs_tied,
        "band_1pct_context": context,
        "per_class": per_class,
        "cited_pairs": cited,
        "greedy_in_the_cloud": g5,
        "identical_behaviour_different_order": g4,
        "predictions": q,
        "cited_orders": {
            "split0_winner_65_starts": prefix_winner(
                runs[0]["stats"]["rows"], 65)["order"],
            "split0_winner_257_starts": prefix_winner(
                runs[0]["stats"]["rows"], 257)["order"],
            "split0_greedy_end_order": runs[0]["stats"]["rows"][0]["order"],
            "split4_winner_65_starts": prefix_winner(
                runs[4]["stats"]["rows"], 65)["order"],
            "split4_winner_257_starts": prefix_winner(
                runs[4]["stats"]["rows"], 257)["order"],
        },
        "seconds": {
            "setup": inst["seconds_setup"],
            "search_full_supervision": {s: runs[s]["seconds"]
                                        for s in SPLITS_FULL},
            "search_band_1pct": round(sum(f["seconds"] for f in band), 1),
            "shortcut_validation": shortcut["seconds"],
            "total": round(time.time() - t_start, 1),
        },
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
