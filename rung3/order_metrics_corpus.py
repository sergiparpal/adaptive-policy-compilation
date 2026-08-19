"""
THE SAME ORDERS AND THE SAME INSTRUMENT, ON THE CORPUS SURFACE.

--------------------------------------------------------------------------
WHAT THIS IS
--------------------------------------------------------------------------
`results3/order_metrics.json` measures the end orders of the audited multi-start
over the EXHAUSTIVE SPACE: 134,400 combinations, uniform. That is not the
distribution a deployed system meets. `IDEAS.md` opened the question as its own
entry and wrote a prediction, S-a to S-f, signed and committed before any of the
figures below existed; this run is what adjudicates it.

Nothing new is searched. The orders are regenerated down the SAME deterministic
path P4 already used — `order_metrics_run.run_full_supervision` and
`run_band_1pct`, imported rather than copied — and then measured with
`order_metrics`, which is pure and takes masks as arguments, so the change of
surface is a change of argument and of nothing else. `MULTISTART_SEED`,
`MULTISTART_STARTS` and `DECLARED_NEIGHBOURHOOD` are untouched, and no figure
here is an argument about any of them.

--------------------------------------------------------------------------
THE CORPUS IS TWO SURFACES, AND THEY ARE NAMED SEPARATELY
--------------------------------------------------------------------------
  corpus, all 2000 cases   the modelled arrival distribution, whole. It is what
                           "the corpus" means in the entry and in G2's census,
                           and it is the surface these predictions adjudicate
                           on. The search saw the train half of it, so a
                           disagreement measured here is measured partly over
                           cases the orders were fitted to.
  corpus test half         the same distribution with the fitted half removed:
                           995 cases for split 0, 1002 for split 4. Free of
                           that contamination and half the size.

Every figure below carries which of the two it is. Where they disagree about a
verdict, both are reported and neither is quietly preferred.

--------------------------------------------------------------------------
THE GATES, AND WHY THERE ARE TWO
--------------------------------------------------------------------------
PARITY, blocking and inherited: the same 31 rows of P4 — six budget rows against
`start_budget_check.json` and the whole 1% band against
`budget_and_balance_ls.json` — must reproduce exactly, or the regenerated orders
are not the published ones and nothing here is about them. The prefix shortcut
is NOT revalidated: it was checked against an independent 65-start run when it
was introduced, `tests/test_order_metrics_run.py` pins the tie-break it rests
on, and re-running it would cost 34 s to answer a question already answered.

CENSUS, reported: `pair_census` over the corpus pool must give the row
`FINDINGS_ORDERS.md` already publishes for it — 166,176 pairs, 51,499
co-matching, 33,631 conflicting. It is the one published figure that pins the
corpus MASKS rather than the orders, which is exactly what changes here.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It writes one new file, `results3/order_metrics_corpus.json`. It does not touch
`order_metrics.json` — that record is the space, this one is the corpus, and
their being two files is part of the answer. It runs no `budget_and_balance_ls`,
`order_search_ls`, `budget_and_balance` or `sweep*`: those dump JSON over
published records, so their functions are imported and called instead.

It does not consult the oracle. The truth by class over the corpus is
`inst["truth"]`, the label list `build_masks` already consumes, sliced into one
mask per class; over the space it is `order_search_ls.space_truth_masks`, as in
P4.

No Kendall tau is computed. Q-d refuted it as a stand-in for the exact
comparison on the space, tau is by far the dominant cost of P4, and none of
S-a..S-f asks for it. Where a named pair is reported in full, `pair_report`
computes it anyway, over that surface's own conflicting set.

--------------------------------------------------------------------------
THE AMENDMENT MODE, AND WHY IT IS ALLOWED TO RE-RUN
--------------------------------------------------------------------------
`--s-e-argmin` regenerates down the same path, passes the same two gates, and
then does one thing the full run did not: it says WHICH pairs attain S-e's
minimum. The full run stored the minimum and not the pair, because the
257-order matrices are summarized rather than kept, so the identity is a lookup
into a set already measured and not a new quantity. It was authorized
explicitly, after the six verdicts existed, and on the condition that nothing
already published may move; the mode compares every set summary it recomputes
against the record and refuses to write if one differs. See `AUTHORIZATION`.

Usage:  python3 -m rung3.order_metrics_corpus
        python3 -m rung3.order_metrics_corpus --checks   (gates only)
        python3 -m rung3.order_metrics_corpus --s-e-argmin
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung3.local_search import (DECLARED_NEIGHBOURHOOD, MULTISTART_SEED,
                                   MULTISTART_STARTS)
from rung3.order_metrics import (agreement_masks, behavioural_distance,
                                    conflicting_pairs, pair_census)
from rung3.order_metrics_run import (BUDGETS, DRAW_B, FRACTION_B, SPLIT_B,
                                        SPLITS_FULL, band_context,
                                        build_instance,
                                        decisions_and_signatures, masks_for,
                                        pair_report, pairwise, parity_band,
                                        parity_full_supervision,
                                        per_class_over_pairs, prefix_winner,
                                        run_band_1pct, run_full_supervision,
                                        slice_pairs, summarize)

OUT = Path("results3")
RECORD = "order_metrics_corpus.json"
POOL = "puro"

SURFACES = ("corpus_full", "corpus_test")
LABELS = {"corpus_full": "corpus, all 2000 cases",
          "corpus_test": "corpus test half"}

# `FINDINGS_ORDERS.md`, G2, the row it publishes for the corpus pure pool over
# the 2000 cases. It lives in prose and nowhere else, which is why it is copied
# here with its source named: it is the only published figure that pins the
# corpus MASKS, and the masks are what this run changes.
CENSUS_PUBLISHED = {"pairs": 166176, "co_match": 51499, "conflicting": 33631}

# The classes S-c restricts itself to are chosen by their CORPUS size, and the
# same set is used on both surfaces so that the two columns compare.
S_C_MIN_CORPUS_CASES = 100

# ---------------------------------------------------------------------------
# What the record says about itself. Constants rather than literals inside the
# payload because the committed record was annotated with these same strings by
# hand, after the run, and the only way to be sure the two agree is for there to
# be one copy.
# ---------------------------------------------------------------------------

TRUTH_PROVENANCE = (
    "the per-class truth of every corpus figure in this record is "
    "inst['truth'] — the label list order_search.build_tables produced once "
    "for the 2000 cases — sliced into one mask per class over the indices "
    "ACTUALLY MEASURED, in build_masks' convention: case idxs[k] is bit k. It "
    "is NOT order_search_ls.space_truth_masks, which is the truth over the "
    "134,400 cases of the exhaustive space in Space's convention, case k at "
    "bit n-1-k; that one is used here for nothing, and using it on a corpus "
    "surface would have turned every per-class figure into noise of the right "
    "shape, since the totals would still add up. The G2 census gate does not "
    "cover this: it pins the rule masks M by reproducing a published pair "
    "count, and a pair count never looks at a label. What covers it is "
    "tests/test_order_metrics_corpus.py — the class masks partition each of "
    "the three measured surfaces, and W[r] == M[r] & truth[action[r]] holds "
    "over all 577 rules on each, which the reversed convention fails.")

POST_HOC = (
    "competition_census IS POST HOC and is not one of the adjudicated "
    "figures. The six verdicts were produced first, by a run of this module "
    "that did not contain `competition` at all (2026-08-15T14:08:24Z, "
    "code_digest 3bb4662a607fc9a0). The census was then written and "
    "instrumented BECAUSE S-b had failed and S-b states a mechanism, and the "
    "module was re-run whole (14:17:16Z, code_digest 99184aa53d866fac), "
    "reproducing the six verdicts exactly and adding it. So this record's own "
    "code_digest covers code written after the verdicts existed. That earlier "
    "record was overwritten by this one and is not on the record, so what a "
    "reader can check is the code in this commit, not that run. The two "
    "figures are kept because they separate 'the premise was false' from 'the "
    "premise was true and the effect does not appear', which is the finding; "
    "they are marked because a quantity chosen after seeing a refutation is a "
    "different kind of quantity from one named before it.")

COMPETITION_IS_POST_HOC = (
    "the figures under 'competition' were chosen and measured AFTER this "
    "verdict existed, because it was a refutation with a stated mechanism; see "
    "the record's 'post_hoc' field. They are evidence about the mechanism and "
    "no part of the adjudication, which is the pooled rate against 15.2% and "
    "nothing else.")

RECORD_ANNOTATIONS = (
    "annotations added BY HAND to the committed record on 2026-08-15, after "
    "the run that produced it and after the six verdicts existed: "
    "truth_provenance, post_hoc, sets_measured, this field, and inside "
    "predictions, S-b's competition_is_post_hoc, S-d's clause_verbatim and "
    "readings, and a rewrite of S-d's refutation_note, which paraphrased a "
    "clause that had to be quoted. Every one of them is a string; no measured "
    "value was touched, "
    "and the diff against the commit that landed this record shows those "
    "additions and nothing else. The module holds them as constants and emits "
    "them, so a fresh run reproduces this text — what a fresh run would not "
    "reproduce is code_digest 99184aa53d866fac, which identifies the code as "
    "it stood when these numbers were computed.")

# The row of IDEAS.md, copied rather than summarized: its refutation condition
# is not a number, and paraphrasing it is how it would quietly become one.
S_D_CLAUSE = (
    "S-d — *Calibration.* SECURITY_INCIDENT's share of the total disagreement "
    "falls from **57.5% to under 3%**. *Refuted* by anything far from that, "
    "which would mean the per-class rates do not carry across and S-c will "
    "already have fired.")

SETS_MEASURED = {
    "surfaces": [
        "corpus_full: all 2000 corpus cases",
        "corpus_test: the test half of the split whose orders are measured — "
        "995 cases for split 0, 1002 for split 4",
        "exhaustive space, 134,400 cases: measured here only for S-e's first "
        "clause, which compares the two surfaces pair by pair",
    ],
    "adjudicating": [
        "split0_starts65 on corpus_full — S-a, S-b, S-c and S-d, all four "
        "pooled over its 2,080 pairs; corpus_test reported beside",
        "split0_starts257 on corpus_full, against the same 32,896 pairs on the "
        "exhaustive space — S-e, whose first clause needs both surfaces; "
        "corpus_test reported beside",
        "b_tied_split0_draw0 on corpus_full, the 40 orders tying at the best "
        "train score at 1% — S-f; corpus_test reported beside",
    ],
    "additional": [
        "split0_starts129 on both corpus surfaces: adjudicates nothing, and is "
        "measured because the budgets are nested and slicing the matrix is "
        "free",
        "split4_starts65 / 129 / 257 on both corpus surfaces: the other split "
        "start_budget_check saw the train score move on. It adjudicates "
        "nothing — every prediction names split 0 — and is reported so that no "
        "figure rests on one split",
        "b_all65_split0_draw0 on both corpus surfaces: all 65 end orders of "
        "the 1% cell, tied or not, as the containing set of S-f's 40",
        "band_1pct_context_corpus_full: the tied set of each of the 25 cells "
        "of the 1% band, context for S-f and for nothing else",
        "cited_pairs: the winner at 65 against the winner at 257 on each "
        "split, reported in full on each corpus surface",
        "competition_census: post hoc, see the 'post_hoc' field",
    ],
    "pair_matrices": [
        "5 matrices of 32,896 pairs: (split 0, corpus_full), "
        "(split 0, corpus_test), (split 4, corpus_full), "
        "(split 4, corpus_test), (split 0, exhaustive space)",
        "plus the 2,080-pair and 780-pair triangles of the 1% cell on each "
        "corpus surface, and the tied set of each band cell on corpus_full",
    ],
}


AUTHORIZATION = (
    "the re-run behind `minimum_pairs` was authorized by Sergi on 2026-08-15, "
    "EXPLICITLY AND AFTER THE SIX VERDICTS EXISTED, and for one thing only: to "
    "recover the identity of the pairs attaining S-e's minimum, which this "
    "record measured and did not store because the 257-order matrices are "
    "summarized. It is a lookup, not a measurement. What it returns is an "
    "INDEX into a set already measured — which two of the 257 end orders reach "
    "a distance already published, and where. No quantity that adjudicates "
    "anything is computed for the first time here: S-e rests on the minimum "
    "being 2 cases of 2000, and that number is re-verified rather than "
    "re-derived. That is why an argmin is not a new figure and cannot move a "
    "verdict — the only way this pass could have changed one is by failing to "
    "reproduce, and a failure to reproduce would have been a finding about "
    "determinism, reported as such and with nothing overwritten. Both gates "
    "were re-run and both passed: parity 31/31 and the G2 census. Every "
    "already-published value it recomputes was compared against this file "
    "before anything was written to it.")


def s_d_readings(share_full, share_test):
    """
    S-d has two lines in it and they do not agree; both are published.

    The row states a point value — *under 3%* — and a refutation condition that
    is not a number, *anything far from that*. 4.57% fails the first and
    arguably satisfies the second, since it arrives from 57.5%. What decides
    between them here is not which is kinder: it is that the point value is the
    only half a reader can check mechanically, and that the clause's own rider
    — *which would mean the per-class rates do not carry across and S-c will
    already have fired* — names a condition that DID occur. S-c fired, on four
    of its six eligible classes. The row's own logic therefore points where its
    stated value points.
    """
    return {
        "on_the_stated_value": {
            "line": "under 3%",
            "measured": {"corpus_full": share_full, "corpus_test": share_test},
            "verdict": "REFUTED",
        },
        "on_the_refutation_clause_as_written": {
            "line": "anything far from that",
            "verdict": "NOT DECIDABLE FROM THE ROW",
            "why": "4.57% arrives from 57.5%, a fall of 12.6x, and lands 1.6 "
                   "points above a 3% line. Whether that is 'far from' 3% is "
                   "not a quantity this record can evaluate, and reading it "
                   "charitably after seeing the number is adjudication by "
                   "charity.",
        },
        "applied": "on_the_stated_value",
        "why_applied":
            "the point value is the only half of the row that can be checked "
            "mechanically, and the clause's own rider — that a refutation "
            "would mean the per-class rates do not carry across and S-c would "
            "already have fired — describes exactly what happened: S-c is "
            "refuted on four of its six eligible classes. Both halves of the "
            "row therefore agree, and the verdict is not doing the work of an "
            "argument.",
    }


# ---------------------------------------------------------------------------
# The corpus as a surface
# ---------------------------------------------------------------------------

def truth_masks(inst, idxs):
    """
    {class: mask of the cases of `idxs` whose label is that class}, in
    `build_masks`' convention — case `idxs[k]` is bit k.

    From `inst["truth"]`, which is the corpus label list the masks are already
    built against, and not from the oracle: `order_search.build_tables` labelled
    the corpus once, and this is that labelling sliced by class. Deriving it
    from the masks instead would give the per-class CEILING, which is the defect
    the optimizer audit recorded as F10.
    """
    out = {}
    for k, i in enumerate(idxs):
        c = inst["truth"][i]
        out[c] = out.get(c, 0) | (1 << k)
    return out


def surface(inst, idxs, name, label):
    """A surface, in the shape the P4 measuring functions read it."""
    M, W, full = masks_for(inst, idxs)
    return {"name": name, "label": label, "idxs": idxs, "n": len(idxs),
            "masks": (M, W, full, len(idxs)), "truth": truth_masks(inst, idxs),
            "census": pair_census(inst["ids"], M, inst["action"]),
            "conflicting": conflicting_pairs(inst["ids"], M, inst["action"])}


def competition(ids, M, conflicting, n):
    """
    How much competition the typical case of a surface carries: how many rules
    match it, and how many CONFLICTING pairs are live on it.

    S-b's stated reason for betting the corpus rate UP is that the 577 rules
    were written looking at the corpus, so the typical arriving case carries
    more rules over it and more pairs competing than the typical point of the
    uniform space. That is not an assumption, it is a quantity, and it comes off
    the same masks the rest of this run uses.

    **POST HOC, and marked as such wherever it appears**: this function was
    written on 2026-08-15 AFTER the six verdicts already existed and BECAUSE
    S-b had failed. It is evidence about a mechanism, not part of any
    adjudication, and the record's `post_hoc` field carries the full account
    with the two runs and their digests. Nothing about the verdicts changed
    when it was added: the re-run reproduced all six.

    `conflicting_pairs_per_case_mean` is the honest denominator of the two: a
    pair can only change a decision on a case both its rules match, so summing
    that intersection over the conflicting pairs and dividing by the surface
    counts how much CONTESTED material the average case sits on.
    """
    incidences = sum(M[r].bit_count() for r in ids)
    live = sum((M[a] & M[b]).bit_count() for a, b in conflicting)
    return {"n": n,
            "n_conflicting_pairs": len(conflicting),
            "rules_per_case_mean": round(incidences / n, 4),
            "conflicting_pairs_per_case_mean": round(live / n, 4)}


def view(inst, surf):
    """
    `inst` with its surface replaced, so that P4's measuring functions —
    `pairwise`, `per_class_over_pairs`, `pair_report`, `band_context` — measure
    the corpus without being modified or copied.

    The key stays named `space` because that is what those functions read. It
    holds the corpus masks here, which is the whole point: they never map a bit
    back to a case, so a surface is exactly the four things below.
    """
    return dict(inst, space=surf["masks"], truth_space=surf["truth"],
                conflicting=surf["conflicting"])


def surfaces_for_split(inst, s):
    """The two corpus surfaces a split's orders are measured on."""
    _tr, te = inst["splits"][s]
    return {
        "corpus_full": surface(inst, list(range(len(inst["corpus"]))),
                               "corpus_full", LABELS["corpus_full"]),
        "corpus_test": surface(inst, te, "corpus_test",
                               f"{LABELS['corpus_test']}, split {s}"),
    }


# ---------------------------------------------------------------------------
# Invariants — if these fail the prediction was not tested at all
# ---------------------------------------------------------------------------

def identity_is_zero(dec, masks):
    """d(a, a) = 0 for every order of a set, on this surface."""
    _M, _W, full, n = masks
    return all(behavioural_distance(d, d, full) == (n, 0, 0) for d, _u in dec)


# ---------------------------------------------------------------------------
# The predictions of IDEAS.md, adjudicated as written
# ---------------------------------------------------------------------------
#
# NOT re-specified, before or after seeing a number. Two of them are decided by
# a yardstick the entry states as a number — S-b's 15.2% and S-d's 57.5% — and
# where a yardstick does not reconstruct, what gets reported is the failure to
# reconstruct, next to the verdict against the number AS WRITTEN. Moving the
# line to the reconstruction would be the Goodhart failure this project studies.

def share_of_disagreement(per_class):
    """Each class's share of the TOTAL disagreements, pooled over the pairs.

    `per_class_over_pairs` returns rates over class sizes; the share is
    rate_c * n_c over the sum of that, which is what S-d bets on and what
    `FINDINGS_ORDERS.md` reports as SECURITY_INCIDENT's 57.5% on the space.
    """
    w = {c: v["rate"] * v["n_per_pair"]
         for c, v in per_class["by_class"].items()}
    total = sum(w.values())
    return {c: (round(x / total, 6) if total else None) for c, x in w.items()}


def adjudicate(measured, space):
    """S-a to S-f, verbatim, with the verdict on each corpus surface."""
    q = {}

    # ---- S-a: the pooled rate of the 2,080 pairs, 65 starts, split 0
    def v_a(r):
        if r is None:
            return None
        if r < 0.10 or r > 0.22:
            return "REFUTED"
        return "HOLDS" if 0.12 <= r <= 0.20 else "NEITHER"

    q["S-a"] = {
        "claim": "the disagreement over the 2,080 pairs of the 65-start set, "
                 "measured on the corpus, falls between 12% and 20%; refuted "
                 "below 10% or above 22%. The quantity that adjudicates is the "
                 "POOLED rate — total disagreements over total cases, summed "
                 "across the pairs. The per-pair median is reported beside it "
                 "and does not adjudicate.",
        "adjudicates_on": "corpus_full",
        "band": [0.12, 0.20], "refuted_outside": [0.10, 0.22],
        "pooled": {s: measured[s]["pooled_split0_65"]["overall_rate"]
                   for s in SURFACES},
        "median_per_pair_not_adjudicating": {
            s: measured[s]["sets"]["split0_starts65"]["disagreement_rate"]["median"]
            for s in SURFACES},
        "space_pooled": space["per_class"]["pooled_split0_65"]["overall_rate"],
        "verdict_by_surface": {
            s: v_a(measured[s]["pooled_split0_65"]["overall_rate"])
            for s in SURFACES},
    }
    q["S-a"]["verdict"] = q["S-a"]["verdict_by_surface"]["corpus_full"]

    # ---- S-b: the bet. That same pooled rate against 15.2%
    def v_b(r):
        if r is None:
            return None
        return "HOLDS" if r > 0.152 else "REFUTED" if r < 0.152 else "NEITHER"

    q["S-b"] = {
        "claim": "that same pooled rate comes out above the 15.2% that "
                 "reweighting the space's per-class rates by the arrival "
                 "distribution gives; refuted below 15.2%.",
        "adjudicates_on": "corpus_full",
        "threshold_as_written": 0.152,
        "pooled": q["S-a"]["pooled"],
        "reconstructed_yardstick": measured["reweighted_space_rate"],
        "reconstruction_note":
            "sum over classes of (corpus frequency) x (space per-class rate of "
            "the same 2,080 pairs). It does NOT come out at the 15.2% the "
            "prediction names, and the adjudication is against 15.2% as "
            "written regardless.",
        "stated_mechanism":
            "'the 577 rules were written looking at the corpus, so the typical "
            "arriving case carries more rules over it and more pairs competing, "
            "and that pushes up against a reweighting that pushes down'. The "
            "premise is measured in `competition_census`, not assumed.",
        "competition": measured["competition"],
        "verdict_by_surface": {s: v_b(q["S-a"]["pooled"][s])
                               for s in SURFACES},
        "verdict_against_reconstruction": {
            s: ("above" if q["S-a"]["pooled"][s]
                > measured["reweighted_space_rate"] else "below")
            for s in SURFACES},
    }
    q["S-b"]["verdict"] = q["S-b"]["verdict_by_surface"]["corpus_full"]
    q["S-b"]["competition_is_post_hoc"] = COMPETITION_IS_POST_HOC

    # ---- S-c: per-class rates preserved to +/-30% relative
    def rows_c(s):
        out = {}
        for c, v in measured[s]["pooled_split0_65"]["by_class"].items():
            if measured["corpus_class_sizes"][c] < S_C_MIN_CORPUS_CASES:
                continue
            e = space["per_class"]["pooled_split0_65"]["by_class"][c]["rate"]
            out[c] = {"corpus_rate": v["rate"], "space_rate": e,
                      "corpus_n": measured[s]["class_sizes"][c],
                      "relative_change": round(v["rate"] / e - 1, 4) if e else None,
                      "within_30pct": abs(v["rate"] / e - 1) <= 0.30 if e else None}
        return out

    filas_c = {s: rows_c(s) for s in SURFACES}
    q["S-c"] = {
        "claim": "the per-class rates are preserved across surfaces to within "
                 "+/-30% relative, for the classes with 100 or more corpus "
                 "cases; refuted otherwise.",
        "adjudicates_on": "corpus_full",
        "classes": sorted(filas_c["corpus_full"]),
        "by_class": filas_c,
        "verdict_by_surface": {
            s: ("HOLDS" if all(v["within_30pct"] for v in filas_c[s].values())
                else "REFUTED") for s in SURFACES},
    }
    q["S-c"]["verdict"] = q["S-c"]["verdict_by_surface"]["corpus_full"]

    # ---- S-d: SECURITY_INCIDENT's share of the total disagreement
    q["S-d"] = {
        "claim": "SECURITY_INCIDENT's share of the total disagreement falls "
                 "from 57.5% to under 3%; refuted by anything far from that.",
        "adjudicates_on": "corpus_full",
        "threshold": 0.03,
        "refutation_note":
            "this row has two lines in it and they do not agree. The clause is "
            "quoted verbatim under `clause_verbatim` rather than paraphrased, "
            "and both readings of it, with the one applied and why, are under "
            "`readings`.",
        "space_share": measured["space_share_security"],
        "reweighted_share":
            measured["reweighted_space_share_security"],
        "reweighted_share_note":
            "what pure reweighting predicts for this share — the space's "
            "per-class rates carried over unchanged and weighted by the corpus "
            "class sizes. It is where the 'under 3%' line comes from, and the "
            "gap between it and the measured share is exactly what S-c's "
            "refutation is made of.",
        "share": {s: measured[s]["shares"]["SECURITY_INCIDENT"]
                  for s in SURFACES},
        "all_shares": {s: measured[s]["shares"] for s in SURFACES},
        "verdict_by_surface": {
            s: ("HOLDS" if measured[s]["shares"]["SECURITY_INCIDENT"] < 0.03
                else "REFUTED") for s in SURFACES},
    }
    q["S-d"]["verdict"] = q["S-d"]["verdict_by_surface"]["corpus_full"]
    q["S-d"]["clause_verbatim"] = S_D_CLAUSE
    q["S-d"]["readings"] = s_d_readings(
        measured["corpus_full"]["shares"]["SECURITY_INCIDENT"],
        measured["corpus_test"]["shares"]["SECURITY_INCIDENT"])

    # ---- S-e: the 32,896 pairs of the 257-start set
    def v_e(s):
        d = measured[s]["s_e"]
        if d["pairs_zero_on_corpus_positive_on_space"] > 0:
            return "REFUTED"
        return "HOLDS" if d["min_rate"] < 0.01 else "PARTIAL"

    q["S-e"] = {
        "claim": "over the 32,896 pairs of the 257-start set: pairs at "
                 "distance 0 on the corpus with distance > 0 on the space stay "
                 "at zero, while the pairwise minimum falls from 1.9% of the "
                 "space — 2,615 cases — to under 1% of the corpus. Refuted if "
                 "any such pair appears.",
        "adjudicates_on": "corpus_full",
        "threshold_min_rate": 0.01,
        "space_min": space["sets"]["split0_starts257"]["disagreement"]["min"],
        "space_min_rate":
            space["sets"]["split0_starts257"]["disagreement_rate"]["min"],
        "measured": {s: measured[s]["s_e"] for s in SURFACES},
        "verdict_by_surface": {s: v_e(s) for s in SURFACES},
    }
    q["S-e"]["verdict"] = q["S-e"]["verdict_by_surface"]["corpus_full"]

    # ---- S-f: the tied set at 1%
    def v_f(r):
        if r is None:
            return None
        return "HOLDS" if r > 0.20 else "REFUTED" if r < 0.10 else "NEITHER"

    mediana = {s: measured[s]["sets"]["b_tied_split0_draw0"]
               ["disagreement_rate"]["median"] for s in SURFACES}
    q["S-f"] = {
        "claim": "the tied set at 1%, which disagrees a median 39.2% over the "
                 "space, stays above 20% over the corpus; refuted below 10%.",
        "adjudicates_on": "corpus_full",
        "threshold": 0.20, "refuted_below": 0.10,
        "space_median":
            space["sets"]["b_tied_split0_draw0"]["disagreement_rate"]["median"],
        "median_rate": mediana,
        "median_cases": {s: measured[s]["sets"]["b_tied_split0_draw0"]
                         ["disagreement"]["median"] for s in SURFACES},
        "understatement_note":
            "the tied set was fitted to 10 labelled cases of split 0's train "
            "half, so the full corpus contains what the search saw and the "
            "test half does not. Measuring on what the search fitted "
            "understates this by construction, which is why both surfaces are "
            "published.",
        "verdict_by_surface": {s: v_f(mediana[s]) for s in SURFACES},
    }
    q["S-f"]["verdict"] = q["S-f"]["verdict_by_surface"]["corpus_full"]
    return q


# ---------------------------------------------------------------------------
# The amendment: which pairs reach S-e's minimum
# ---------------------------------------------------------------------------
#
# WHY IT IS A MODE AND NOT A SCRIPT. It has to regenerate down the same path and
# pass the same two gates before it may say anything about these orders, and
# that path is `main` above. So it branches after the gates and reuses every
# line of them; what it adds is an argmin and a comparison.

def _lookup(pares):
    return {(p["i"], p["j"]): p for p in pares}


def minimum_pairs(inst, surf, dec, pares, en_espacio):
    """
    Every pair attaining the minimum behavioural distance on `surf`, with what
    the same pair does over the space, and — the question the findings raise —
    whether the corpus cases they differ on are distinct tickets or one ticket
    drawn twice.

    The minimum is plural on purpose: nothing says one pair attains it, and
    reporting `the` closest pair when three tie would be inventing a
    uniqueness the measurement does not have.
    """
    minimo = min(p["disagree"] for p in pares)
    corpus, idxs = inst["corpus"], surf["idxs"]
    fuera = []
    for p in (q for q in pares if q["disagree"] == minimo):
        dA, dB = dec[p["i"]][0], dec[p["j"]][0]
        _ag, dis, _un = agreement_masks(dA, dB, surf["masks"][2])
        casos = []
        for k in range(surf["n"]):
            if dis >> k & 1:
                i_corpus = idxs[k]
                casos.append({
                    "corpus_index": i_corpus,
                    "true_class": inst["truth"][i_corpus],
                    "key": corpus[i_corpus].key(),
                    "decided_by_i": next(a for a, m in dA.items() if m >> k & 1),
                    "decided_by_j": next(a for a, m in dB.items() if m >> k & 1),
                })
        llaves = [c["key"] for c in casos]
        fuera.append({
            "i": p["i"], "j": p["j"],
            "disagree_here": p["disagree"],
            "disagree_on_the_space": en_espacio[(p["i"], p["j"])]["disagree"],
            "moved_fraction": p["moved_fraction"],
            "cases": casos,
            "distinct_tickets": len(set(llaves)),
            "same_ticket_drawn_twice": len(llaves) > 1 and len(set(llaves)) == 1,
        })
    return {"min_cases": minimo, "n_pairs_at_minimum": len(fuera),
            "pairs": fuera}


def amend_minimum_pairs(inst, surfs, runs, band, t_start):
    """Measure the 257-order sets again, check that nothing published moved, and
    write the identities into the record. Blocking on both counts."""
    registro = OUT / RECORD
    if not registro.is_file():
        print(f"  STOP: {registro} is not there. This amends a record; it does "
              f"not create one.")
        return 1
    d = json.loads(registro.read_text())

    print()
    print("MEASURING AGAIN — the 257-order sets, to locate a minimum already "
          "published")
    dec_c, pares_c = {}, {}
    for s in SPLITS_FULL:
        orders = [r["order"] for r in runs[s]["stats"]["rows"]]
        for name in SURFACES:
            surf = surfs[s][name]
            v = view(inst, surf)
            dec, dig = decisions_and_signatures(v, orders)
            pares = pairwise(v, orders, dec, with_taus=False)
            dec_c[(s, name)], pares_c[(s, name)] = dec, pares
            for k in BUDGETS:
                nuevo = summarize(
                    f"split {s}, fraction 1.0, {k} starts, {surf['label']}",
                    dig, slice_pairs(pares, k), k)
                viejo = d["sets"][name][f"split{s}_starts{k}"]
                distintos = [c for c in viejo if viejo[c] != nuevo.get(c)]
                if distintos:
                    print(f"\n  STOP: split{s}_starts{k} on {name} no longer "
                          f"reproduces. Fields that moved: {distintos}")
                    print("  Nothing is written. A published value changing is "
                          "the finding, and it is reported, not repaired.")
                    return 1
    orders0 = [r["order"] for r in runs[SPLITS_FULL[0]]["stats"]["rows"]]
    dec_s, _dig = decisions_and_signatures(inst, orders0)
    en_espacio = _lookup(pairwise(inst, orders0, dec_s, with_taus=False))
    print(f"  every one of the {len(SPLITS_FULL) * len(SURFACES) * len(BUDGETS)}"
          f" published set summaries reproduces exactly")

    # ---- the argmins, one per corpus surface: they need not be the same pair
    s0 = SPLITS_FULL[0]
    fuera = {}
    for name in SURFACES:
        surf = surfs[s0][name]
        m = minimum_pairs(inst, surf, dec_c[(s0, name)], pares_c[(s0, name)],
                          en_espacio)
        publicado = d["s_e_cross_surface"][name]
        if m["min_cases"] != publicado["min_cases"]:
            print(f"\n  STOP: the minimum on {name} is {m['min_cases']} and "
                  f"the record publishes {publicado['min_cases']}.")
            print("  Nothing is written. That is the finding.")
            return 1
        fuera[name] = m
        print(f"\n  {surf['label']}: minimum {m['min_cases']} cases, reached by "
              f"{m['n_pairs_at_minimum']} pair(s) of {len(pares_c[(s0, name)]):,}")
        for p in m["pairs"]:
            print(f"    orders {p['i']} and {p['j']}: {p['disagree_here']} "
                  f"case(s) here, {p['disagree_on_the_space']:,} over the "
                  f"space, {p['distinct_tickets']} distinct ticket(s)")
            for c in p["cases"]:
                print(f"      corpus case {c['corpus_index']} "
                      f"({c['true_class']}): {c['decided_by_i']} against "
                      f"{c['decided_by_j']}")

    # ---- into the record, beside the value they locate
    for name in SURFACES:
        d["s_e_cross_surface"][name]["minimum_pairs"] = fuera[name]
        d["s_e_cross_surface"][name]["minimum_pairs_note"] = (
            "the pairs attaining `min_cases`, recovered by the authorized "
            "re-run of 2026-08-15; see `authorization`. They are NOT in "
            "`example`, which is the slot for an instance of the case S-e "
            "calls its refutation — a pair at distance 0 here and above 0 on "
            "the space — and whose being null is itself a published fact, "
            "carried also by pairs_zero_on_corpus_positive_on_space: 0.")
        for p in fuera[name]["pairs"]:
            d["cited_pairs"][f"s_e_minimum_split{s0}_{name}_{p['i']}_{p['j']}"] = \
                pair_report(view(inst, surfs[s0][name]),
                            orders0[p["i"]], orders0[p["j"]],
                            f"split {s0}: end orders {p['i']} and {p['j']}, "
                            f"which attain the minimum distance over "
                            f"{surfs[s0][name]['label']}")
    d["authorization"] = AUTHORIZATION
    d["_env_amendment"] = environment(
        what="the authorized re-run that recovered S-e's minimum pairs",
        neighbourhood=DECLARED_NEIGHBOURHOOD, multistart_seed=MULTISTART_SEED,
        multistart_starts=MULTISTART_STARTS, budgets=list(BUDGETS),
        seconds=round(time.time() - t_start, 1))
    registro.write_text(json.dumps(d, indent=2))
    print(f"\n  nothing published moved. total cost: {time.time() - t_start:.0f}s")
    print(f"-> {registro}")
    return 0


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    solo_checks = "--checks" in argv
    solo_argmin = "--s-e-argmin" in argv
    t_start = time.time()

    print("=" * 78)
    print("S-a..S-f — THE SAME ORDERS, MEASURED OVER THE CORPUS")
    print("=" * 78)
    print(f"  optimizer: {DECLARED_NEIGHBOURHOOD}, seed {MULTISTART_SEED}, "
          f"{MULTISTART_STARTS} declared starts + the greedy (untouched)")
    print(f"  budgets {list(BUDGETS)} starts · splits {list(SPLITS_FULL)} · "
          f"pool {POOL} · no new search, no API calls")
    print(f"  {describe()}")

    inst = build_instance()
    _sM, _sW, _sfull, sn = inst["space"]
    print(f"  instance ready in {inst['seconds_setup']}s: "
          f"{len(inst['ids'])} rules, {len(inst['corpus'])} corpus cases, "
          f"{sn:,} space cases")

    # ---------------------------------------------------------------- surfaces
    t0 = time.time()
    surfs = {s: surfaces_for_split(inst, s) for s in SPLITS_FULL}
    corpus_full = surfs[SPLITS_FULL[0]]["corpus_full"]
    print(f"\n  corpus surfaces built in {time.time() - t0:.0f}s: "
          + " · ".join(f"{surfs[s][k]['label']} ({surfs[s][k]['n']})"
                       for s in SPLITS_FULL for k in SURFACES
                       if not (k == "corpus_full" and s != SPLITS_FULL[0])))

    censo = {"published": CENSUS_PUBLISHED,
             "corpus_full": corpus_full["census"],
             "passes": all(corpus_full["census"][k] == v
                           for k, v in CENSUS_PUBLISHED.items()),
             "corpus_test_by_split": {s: surfs[s]["corpus_test"]["census"]
                                      for s in SPLITS_FULL}}
    print("\nCENSUS — the corpus pure pool against FINDINGS_ORDERS.md, G2")
    print(f"  published  {CENSUS_PUBLISHED['pairs']:,} pairs, "
          f"{CENSUS_PUBLISHED['co_match']:,} co-match, "
          f"{CENSUS_PUBLISHED['conflicting']:,} conflict")
    print(f"  measured   {corpus_full['census']['pairs']:,} pairs, "
          f"{corpus_full['census']['co_match']:,} co-match, "
          f"{corpus_full['census']['conflicting']:,} conflict"
          f"{'  ok' if censo['passes'] else '  NO'}")
    if not censo["passes"]:
        print("  STOP: the corpus masks are not the ones that census was "
              "measured on.")
        return 1

    # ------------------------------------------------------------ regeneration
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
        print(f"\n  STOP: a parity failure means the regenerated orders are "
              f"not the measured ones, and nothing below would be about them.")
        return 1
    print(f"\n  PARITY: PASSES, {n_filas}/{n_filas} rows. The regenerated "
          f"orders are the published ones.")
    if solo_checks:
        print(f"\n  total cost: {time.time() - t_start:.0f}s")
        return 0
    if solo_argmin:
        return amend_minimum_pairs(inst, surfs, runs, band, t_start)

    # ----------------------------------------------------------- the measuring
    print()
    print("MEASURING — the same instrument, one surface at a time")
    medido = {s: {"sets": {}, "class_sizes": {}} for s in SURFACES}
    guardados = {}
    invariantes = {"d(a,a) = 0": {}, "undecided_either_max": {}}

    # the 257 end orders of each split, on both corpus surfaces
    dec_corpus, pares_corpus = {}, {}
    for s in SPLITS_FULL:
        orders = [r["order"] for r in runs[s]["stats"]["rows"]]
        for name in SURFACES:
            surf = surfs[s][name]
            v = view(inst, surf)
            t0 = time.time()
            dec, dig = decisions_and_signatures(v, orders)
            invariantes["d(a,a) = 0"][f"{name}_split{s}"] = identity_is_zero(
                dec, surf["masks"])
            pares = pairwise(v, orders, dec, with_taus=False)
            dec_corpus[(s, name)] = dec
            pares_corpus[(s, name)] = pares
            for k in BUDGETS:
                medido[name]["sets"][f"split{s}_starts{k}"] = summarize(
                    f"split {s}, fraction 1.0, {k} starts, {surf['label']}",
                    dig, slice_pairs(pares, k), k)
            resumen_k = medido[name]["sets"][f"split{s}_starts{max(BUDGETS)}"]
            invariantes["undecided_either_max"][f"{name}_split{s}"] = \
                resumen_k["undecided_either_max"]
            print(f"  {surf['label']:<28} split {s}: {len(pares):,} pairs in "
                  f"{time.time() - t0:.0f}s, "
                  f"{resumen_k['n_distinct_signatures']} distinct signatures "
                  f"of {max(BUDGETS)}")

    # the same orders over the space, for S-e's cross-surface clause
    t0 = time.time()
    orders0 = [r["order"] for r in runs[SPLITS_FULL[0]]["stats"]["rows"]]
    dec_space, _dig_space = decisions_and_signatures(inst, orders0)
    pares_space = pairwise(inst, orders0, dec_space, with_taus=False)
    invariantes["d(a,a) = 0"]["space_split0"] = identity_is_zero(
        dec_space, inst["space"])
    print(f"  {'exhaustive space':<28} split {SPLITS_FULL[0]}: "
          f"{len(pares_space):,} pairs in {time.time() - t0:.0f}s "
          f"(for S-e only)")

    # the 1% cell S-f names, and its tied set
    f_b = next(f for f in band if f["split"] == SPLIT_B and f["draw"] == DRAW_B)
    rows_b = f_b["stats"]["rows"]
    orders_b = [r["order"] for r in rows_b]
    mejor_b = max(r["end_score"] for r in rows_b)
    empatados = sorted(r["index"] for r in rows_b
                       if r["end_score"] == mejor_b)
    idx = set(empatados)
    for name in SURFACES:
        surf = surfs[SPLIT_B][name]
        v = view(inst, surf)
        dec_b, dig_b = decisions_and_signatures(v, orders_b)
        pares_b = pairwise(v, orders_b, dec_b, with_taus=False)
        pares_emp = [p for p in pares_b if p["i"] in idx and p["j"] in idx]
        medido[name]["sets"]["b_all65_split0_draw0"] = summarize(
            f"split {SPLIT_B}, fraction 0.01, draw {DRAW_B}, all 65 end "
            f"orders, {surf['label']}", dig_b, pares_b, len(orders_b))
        medido[name]["sets"]["b_tied_split0_draw0"] = summarize(
            f"split {SPLIT_B}, fraction 0.01, draw {DRAW_B}, the "
            f"{len(empatados)} orders tying at the best train score, "
            f"{surf['label']}", [dig_b[i] for i in empatados], pares_emp,
            len(empatados))
        medido[name]["sets"]["b_tied_split0_draw0"]["tied_indices"] = empatados
        medido[name]["pooled_b_tied"] = per_class_over_pairs(v, dec_b,
                                                             pares_emp)
        guardados[f"pairs_b_tied_{name}"] = pares_emp
        invariantes["d(a,a) = 0"][f"{name}_band"] = identity_is_zero(
            dec_b, surf["masks"])
    print(f"  1% cell (split {SPLIT_B}, draw {DRAW_B}): {len(empatados)} tied "
          f"orders, {len(empatados) * (len(empatados) - 1) // 2} pairs, on "
          f"both corpus surfaces")

    # the whole band, as context for S-f and for nothing else
    t0 = time.time()
    contexto = band_context(view(inst, corpus_full), band)
    print(f"  the whole 1% band on {corpus_full['label']} in "
          f"{time.time() - t0:.0f}s (context for S-f)")

    # ------------------------------------------- the pooled per-class figures
    for s in SURFACES:
        s0 = SPLITS_FULL[0]
        medido[s]["pooled_split0_65"] = per_class_over_pairs(
            view(inst, surfs[s0][s]), dec_corpus[(s0, s)],
            slice_pairs(pares_corpus[(s0, s)], 65))
        medido[s]["shares"] = share_of_disagreement(medido[s]["pooled_split0_65"])
        medido[s]["class_sizes"] = {
            c: m.bit_count() for c, m in surfs[s0][s]["truth"].items()}
        guardados[f"pairs_split0_starts65_{s}"] = slice_pairs(
            pares_corpus[(s0, s)], 65)

    espacio = json.loads((OUT / "order_metrics.json").read_text())
    esp_por_clase = espacio["per_class"]["pooled_split0_65"]["by_class"]
    medido["corpus_class_sizes"] = medido["corpus_full"]["class_sizes"]
    medido["space_share_security"] = share_of_disagreement(
        espacio["per_class"]["pooled_split0_65"])["SECURITY_INCIDENT"]
    medido["reweighted_space_rate"] = round(sum(
        medido["corpus_class_sizes"][c] / len(inst["corpus"]) * v["rate"]
        for c, v in esp_por_clase.items()), 6)
    # the same reweighting, read as a share of the total instead of as a rate:
    # the model S-d's "under 3%" comes from.
    peso = {c: v["rate"] * medido["corpus_class_sizes"][c]
            for c, v in esp_por_clase.items()}
    medido["reweighted_space_share_security"] = round(
        peso["SECURITY_INCIDENT"] / sum(peso.values()), 6)

    # ------------------------------------------- how much competition a case
    t0 = time.time()
    medido["competition"] = {
        "space": competition(inst["ids"], inst["space"][0],
                             inst["conflicting"], sn),
        "corpus_full": competition(inst["ids"], corpus_full["masks"][0],
                                   corpus_full["conflicting"],
                                   corpus_full["n"]),
        "corpus_test": {s: competition(inst["ids"],
                                       surfs[s]["corpus_test"]["masks"][0],
                                       surfs[s]["corpus_test"]["conflicting"],
                                       surfs[s]["corpus_test"]["n"])
                        for s in SPLITS_FULL},
    }
    print(f"\n  competition census in {time.time() - t0:.0f}s — rules over the "
          f"average case: "
          f"{medido['competition']['space']['rules_per_case_mean']} on the "
          f"space, {medido['competition']['corpus_full']['rules_per_case_mean']}"
          f" on the corpus; conflicting pairs live on it: "
          f"{medido['competition']['space']['conflicting_pairs_per_case_mean']}"
          f" against "
          f"{medido['competition']['corpus_full']['conflicting_pairs_per_case_mean']}")

    # ------------------------------------------------------------------- S-e
    for name in SURFACES:
        pares = pares_corpus[(SPLITS_FULL[0], name)]
        n_surf = surfs[SPLITS_FULL[0]][name]["n"]
        cruce = [(a, b) for a, b in zip(pares, pares_space)
                 if a["disagree"] == 0 and b["disagree"] > 0]
        if any(a["i"] != b["i"] or a["j"] != b["j"]
               for a, b in zip(pares, pares_space)):
            raise ValueError("the two pair matrices are not aligned")
        minimo = min(p["disagree"] for p in pares)
        medido[name]["s_e"] = {
            "n_pairs": len(pares),
            "pairs_zero_on_corpus_positive_on_space": len(cruce),
            "pairs_zero_on_corpus": sum(1 for p in pares
                                        if p["disagree"] == 0),
            "min_cases": minimo,
            "min_rate": round(minimo / n_surf, 6),
            "n_surface": n_surf,
            "example": (cruce[0][0] if cruce else None),
        }

    # ------------------------------------------------------- the cited pairs
    cited = {}
    for s in SPLITS_FULL:
        rows = runs[s]["stats"]["rows"]
        w65 = prefix_winner(rows, 65)
        w257 = prefix_winner(rows, max(BUDGETS))
        for name in SURFACES:
            cited[f"qa_split{s}_{name}"] = pair_report(
                view(inst, surfs[s][name]), w65["order"], w257["order"],
                f"split {s}: the winner at 65 starts against the winner at "
                f"257, over {surfs[s][name]['label']}")

    q = adjudicate(medido, espacio)

    print()
    print("=" * 78)
    print("S-a..S-f, AS WRITTEN")
    print("=" * 78)
    print(f"  {'':>5}{'corpus 2000':>14}{'corpus test':>14}   decided by")
    for k in sorted(q):
        v = q[k]["verdict_by_surface"]
        print(f"  {k:>5}{v['corpus_full']:>14}{v['corpus_test']:>14}   "
              f"{q[k]['adjudicates_on']}")

    # ------------------------------------------------------------- the record
    payload = {
        "_env": environment(neighbourhood=DECLARED_NEIGHBOURHOOD,
                            multistart_seed=MULTISTART_SEED,
                            multistart_starts=MULTISTART_STARTS,
                            budgets=list(BUDGETS)),
        "what":
            "the end orders of the audited multi-start, regenerated down the "
            "same deterministic path as results3/order_metrics.json and "
            "measured over the CORPUS instead of the exhaustive space. It "
            "adjudicates S-a..S-f of IDEAS.md, written and committed before "
            "any of these figures existed. No new search: the orders are the "
            "published ones, and the 31-row parity gate against "
            "start_budget_check.json and budget_and_balance_ls.json is what "
            "says so. order_metrics.json is NOT rewritten — it owns the space "
            "figures, this one owns the corpus figures, and their being two "
            "records is part of the answer. Zero API calls.",
        "surface": "corpus",
        "surface_note":
            "TWO corpus surfaces, named separately in every figure. 'corpus "
            "full' is all 2000 cases, the modelled arrival distribution and "
            "what the entry means by 'the corpus'; the search saw the train "
            "half of it, so figures there are measured partly over cases the "
            "orders were fitted to. 'corpus test' is that split's test half — "
            "995 cases for split 0, 1002 for split 4 — free of that "
            "contamination and half the size. The predictions adjudicate on "
            "corpus full; the test half is reported beside every one of them.",
        "pool": POOL,
        "n_rules": len(inst["ids"]),
        "n_corpus": len(inst["corpus"]),
        "n_space": sn,
        "surfaces": {name: {"label": (surfs[SPLITS_FULL[0]][name]["label"]
                                      if name == "corpus_full" else
                                      {s: surfs[s][name]["label"]
                                       for s in SPLITS_FULL}),
                            "n": (surfs[SPLITS_FULL[0]][name]["n"]
                                  if name == "corpus_full" else
                                  {s: surfs[s][name]["n"]
                                   for s in SPLITS_FULL}),
                            "census": (corpus_full["census"] if name == "corpus_full"
                                       else {s: surfs[s][name]["census"]
                                             for s in SPLITS_FULL})}
                     for name in SURFACES},
        "budgets": list(BUDGETS),
        "splits": list(SPLITS_FULL),
        "fraction": FRACTION_B,
        "census_gate": censo,
        "parity_full_supervision": par_a,
        "parity_band_1pct": par_b,
        "parity_rows": n_filas,
        "invariants": invariantes,
        "no_new_search":
            "every order measured here comes out of run_full_supervision and "
            "run_band_1pct of order_metrics_run.py, imported and called "
            "unchanged. The prefix shortcut is not revalidated: it was checked "
            "against an independent 65-start run when it was introduced, and "
            "tests/test_order_metrics_run.py pins the tie-break it rests on.",
        "sets": {name: medido[name]["sets"] for name in SURFACES},
        "per_class": {name: {"pooled_split0_65": medido[name]["pooled_split0_65"],
                             "pooled_b_tied": medido[name]["pooled_b_tied"],
                             "shares_of_total_disagreement": medido[name]["shares"],
                             "class_sizes": medido[name]["class_sizes"]}
                      for name in SURFACES},
        "s_e_cross_surface": {name: medido[name]["s_e"] for name in SURFACES},
        "competition_census": medido["competition"],
        "reweighted_space_rate": medido["reweighted_space_rate"],
        "reweighted_space_share_security":
            medido["reweighted_space_share_security"],
        "space_share_security": medido["space_share_security"],
        "band_1pct_context_corpus_full": contexto,
        "cited_pairs": cited,
        "pairs_stored":
            "the full triangle for the 65-order set of split 0 and for the "
            "tied set of the 1% cell, on each corpus surface; for the "
            "257-order sets only the summaries. No taus: Q-d refuted them as a "
            "stand-in on the space, they were the dominant cost of the space "
            "run, and none of S-a..S-f asks for one.",
        "pairs_split0_starts65_corpus_full":
            guardados["pairs_split0_starts65_corpus_full"],
        "pairs_split0_starts65_corpus_test":
            guardados["pairs_split0_starts65_corpus_test"],
        "pairs_b_tied_corpus_full": guardados["pairs_b_tied_corpus_full"],
        "pairs_b_tied_corpus_test": guardados["pairs_b_tied_corpus_test"],
        "predictions": q,
        "seconds": {
            "setup": inst["seconds_setup"],
            "search_full_supervision": {s: runs[s]["seconds"]
                                        for s in SPLITS_FULL},
            "search_band_1pct": round(sum(f["seconds"] for f in band), 1),
            "total": round(time.time() - t_start, 1),
        },
        "truth_provenance": TRUTH_PROVENANCE,
        "post_hoc": POST_HOC,
        "sets_measured": SETS_MEASURED,
        "record_annotations": RECORD_ANNOTATIONS,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"\n  total cost: {time.time() - t_start:.0f}s, zero API calls")
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
