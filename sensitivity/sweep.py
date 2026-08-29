"""
THE SWEEP — `A-a` to `A-e` of `PLAN_SENSITIVITY.md` §0.

--------------------------------------------------------------------------
THE GATE, AND WHY A FREE RUN GETS ONE
--------------------------------------------------------------------------
§8: this plan spends nothing and still gets a gate, because what the gate protects
is not money — it is that the bands were signed before the figures existed. On a
free run the only thing between a draft and a post-hoc band is the commit order,
and a commit order is an honour system.

**It reads `PLAN_SENSITIVITY.md` and no other plan**, and since 2026-08-29 it
counts the signatures rather than stopping at the first. §1's amendment carries
its own, because it changes what a *policy* is and §0's signature does not
silently carry that; `rung2/pair_judgement.py::gate_signature` stops at the first
match, which here would find §0 signed and report `ok` over an unsigned §1 — the
same failure as reading the wrong file, one file in.

No flag skips it. `--dry-run` draws every policy, re-runs `A-g2` and `A-g4` on
each, prints every row and **writes nothing**.

--------------------------------------------------------------------------
WHAT IS MEASURED, PER §2
--------------------------------------------------------------------------
Per policy, **on both surfaces and under both encodings**: coverage, CONFLICT
rate, silent error and e2e — the four `harness.ceiling_check` prints, computed the
same way and checked against it by `A-g3`. Plus the structural quantity that needs
no engine, which is `A-d`'s: how many of the precedence inequalities specificity
would need are violated by the condition counts.

**The bands are read on the space and on the published encoding**, which the plan
fixes for `A-a` explicitly and which `A-e` implies for `A-b` by comparing the two
encodings' curves. Every figure is reported on both surfaces and both encodings
regardless, so no reading depends on that choice being the right one.

**The central 90% of a bin**, which is `A-a`'s band, is `[sorted[5], sorted[94]]`
over 100 draws — five draws excluded below and five above — and *inside* is
inclusive of both ends. Declared here because a percentile convention chosen after
seeing where the hidden policy lands is a band chosen after the fact.

Usage:  python3 -m sensitivity.sweep [--dry-run]
"""

from __future__ import annotations

import json
import random
import re
import statistics
import sys
import time
from pathlib import Path

from harness.provenance import describe, environment
from rung2.engine2 import Space

from . import generator as g
from . import measure as m

PLAN = Path("PLAN_SENSITIVITY.md")
OUT = Path("results_sensitivity")
RECORD = "sweep.json"

# §8 fixes these two, before any figure of this plan existed, and they are not to
# be tuned afterwards.
SWEEP_SEED = 17
SWEEP_DRAWS = 100

SIGNATURE = "**Signed by Sergi:"
MIN_SIGNATURES = 2                 # §0's table and §1's amendment
BLANKS = re.compile(r"_{3,}")

SPACE, CORPUS = "space", "corpus"
BAND_SURFACE, BAND_ENCODING = SPACE, m.PUBLISHED

# --- the five signed bands, transcribed from §0 ------------------------------
# These are Sergi's, signed on 2026-08-29 before any figure of this plan existed;
# `A-b` and `A-d` carry the lines he tightened at signature time. They are named
# constants and pinned by `tests/test_sensitivity.py` for the reason §7 gives:
# **so that moving a band after seeing a figure is visible in a diff.** Editing
# one turns a refutation into a hold by editing a line of Python, which is hard
# rule 6 in its purest form.
A_A_CENTRAL = 0.90                 # inside the central 90% of its own bin
A_B_MIN_SPEARMAN = 0.85            # Spearman(ρ, median e2e) >= 0.85
A_C_MAX_MEDIAN = 0.95              # median e2e at the top bin <= 0.95
A_D_MIN_FRACTION = 0.60            # >= 0.60 of the ρ=0 draws carry a violation
A_E_MAX_DIFFERENCE = 0.15          # |Spearman published − corrected| <= 0.15

CENTRAL = A_A_CENTRAL


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def gate_signature(path: Path = PLAN) -> dict:
    """Every signature line in the plan must be filled in, and there must be at
    least two of them. A model may draft a band and may not sign one."""
    lines = [l.strip() for l in path.read_text().splitlines()
             if l.startswith(SIGNATURE)] if path.exists() else []
    unsigned = [l for l in lines if BLANKS.search(l)]
    return {
        "what": f"every line starting `{SIGNATURE}` in {path.name}, of which "
                f"there must be at least {MIN_SIGNATURES}: §0's table and §1's "
                "amendment. A gate that stops at the first would read §0, find it "
                "signed and report ok over an unsigned §1.",
        "source": str(path),
        "found": len(lines),
        "lines": lines,
        "unsigned": unsigned,
        "passes": len(lines) >= MIN_SIGNATURES and not unsigned,
    }


# ---------------------------------------------------------------------------
# One policy
# ---------------------------------------------------------------------------

def evaluate(policy, space, corpus) -> dict:
    """Both surfaces, both encodings, plus A-d's structural counter."""
    out = {}
    space_ext = None
    for name, universe in ((SPACE, space), (CORPUS, corpus)):
        ext = [universe.extension(list(r.conditions)) for r in policy.rules]
        if name == SPACE:
            space_ext = ext
        truth = g.truth_masks(policy, ext, universe.full)
        for enc in m.ENCODINGS:
            v = m.verdict(policy, ext, m.specificities(policy, enc), universe.full)
            out[(name, enc)] = m.score(v, truth, universe.n)
    out["violations"] = m.required_inequalities(policy, space_ext)
    out["dead_rules"] = g.dead_rules(policy, space_ext, space.full)
    return out


def central_band(values: list[float], central: float = CENTRAL):
    """`[sorted[k], sorted[n-1-k]]` with `k` draws excluded at each end."""
    s = sorted(values)
    k = int(round(len(s) * (1 - central) / 2))
    return s[k], s[len(s) - 1 - k], k


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry_run = "--dry-run" in argv
    t0 = time.time()

    gate = gate_signature()
    print("=" * 78)
    print("THE SENSITIVITY SWEEP — A-a to A-e of PLAN_SENSITIVITY.md §0")
    print("=" * 78)
    print(f"  13 ρ bins · {SWEEP_DRAWS} draws · seed {SWEEP_SEED} · "
          f"2 surfaces × 2 encodings · zero API calls")
    print(f"  {describe()}")
    print(f"\n  GATE · signatures found {gate['found']} "
          f"(at least {MIN_SIGNATURES} required), unsigned {len(gate['unsigned'])}"
          f"  ->  {'ok' if gate['passes'] else 'REFUSES TO WRITE'}")
    if not gate["passes"] and not dry_run:
        print("\n  STOP. The plan is not signed, so no record is written. There "
              "is no")
        print("  flag that skips this: the way past it is to sign the plan, which "
              "is")
        print("  the whole point. `--dry-run` runs everything and writes nothing.")
        return 1

    space = Space()
    corpus = m.CorpusUniverse()
    rng = random.Random(SWEEP_SEED)

    print("\n  DRAWING")
    print(f"  {'centre':>9}{'draws':>7}{'attempts':>10}{'rate':>8}"
          f"{'e2e median':>12}{'viol. any':>11}{'secs':>7}")
    per_bin, rows = [], []
    for centre in g.RHO_BINS:
        t = time.time()
        drawn, attempts = [], 0
        while len(drawn) < SWEEP_DRAWS:
            attempts += 1
            try:
                policy, _ext = g.draw(rng, centre, space)
            except g.DeadEnd:
                continue
            drawn.append(policy)

        bin_rows = []
        for k, policy in enumerate(drawn):
            ev = evaluate(policy, space, corpus)
            # A-g2 and A-g4 again, on every draw the sweep itself makes.
            assert abs(policy.rho - centre) <= g.RHO_TOLERANCE, "A-g2"
            assert not ev["dead_rules"], "A-g4"
            row = {
                "bin": centre, "draw": k, "rho": round(policy.rho, 6),
                "violations": ev["violations"],
            }
            for surface in (SPACE, CORPUS):
                for enc in m.ENCODINGS:
                    row[f"{surface}_{enc}"] = {
                        k2: (round(v, 6) if isinstance(v, float) else v)
                        for k2, v in ev[(surface, enc)].items()}
            bin_rows.append(row)
            rows.append(row)

        e2e = {(s, e): [r[f"{s}_{e}"]["accuracy_end_to_end"] for r in bin_rows]
               for s in (SPACE, CORPUS) for e in m.ENCODINGS}
        any_viol = [r["violations"]["any_violation"] for r in bin_rows]
        lo, hi, excluded = central_band(e2e[(BAND_SURFACE, BAND_ENCODING)])
        per_bin.append({
            "centre": centre,
            "draws": len(drawn),
            "attempts": attempts,
            "acceptance_rate": round(len(drawn) / attempts, 4),
            "rho_mean": round(statistics.fmean(r["rho"] for r in bin_rows), 6),
            "e2e_median": {f"{s}_{e}": round(statistics.median(v), 6)
                           for (s, e), v in e2e.items()},
            "e2e_mean": {f"{s}_{e}": round(statistics.fmean(v), 6)
                         for (s, e), v in e2e.items()},
            "central_band_band_surface": {"low": round(lo, 6), "high": round(hi, 6),
                                          "excluded_each_end": excluded},
            "conflict_rate_median": {
                f"{s}_{e}": round(statistics.median(
                    r[f"{s}_{e}"]["conflict"] / r[f"{s}_{e}"]["n"]
                    for r in bin_rows), 6)
                for s in (SPACE, CORPUS) for e in m.ENCODINGS},
            "silent_error_median": {
                f"{s}_{e}": round(statistics.median(
                    r[f"{s}_{e}"]["silent_error_rate"] for r in bin_rows), 6)
                for s in (SPACE, CORPUS) for e in m.ENCODINGS},
            "violations_required_median": statistics.median(
                r["violations"]["required"] for r in bin_rows),
            "violations_median": statistics.median(
                r["violations"]["violated"] for r in bin_rows),
            "fraction_with_a_violation": round(sum(any_viol) / len(any_viol), 6),
        })
        b = per_bin[-1]
        print(f"  {centre:>+9.4f}{b['draws']:>7}{b['attempts']:>10}"
              f"{b['acceptance_rate']:>8.1%}"
              f"{b['e2e_median'][f'{BAND_SURFACE}_{BAND_ENCODING}']:>12.4f}"
              f"{b['fraction_with_a_violation']:>11.2f}{time.time()-t:>7.1f}")

    # ---- the hidden policy, measured through the same path ----------------
    hidden = g.hidden_member()
    hid = evaluate(hidden, space, corpus)
    hidden_row = {f"{s}_{e}": hid[(s, e)] for s in (SPACE, CORPUS)
                  for e in m.ENCODINGS}
    hidden_row["violations"] = hid["violations"]
    hidden_row["rho"] = round(hidden.rho, 6)

    print("\n  THE HIDDEN POLICY, THROUGH THE SAME PATH")
    for s in (SPACE, CORPUS):
        for e in m.ENCODINGS:
            r = hid[(s, e)]
            print(f"    {s:<7}{e:<11}cov {r['coverage']:.4f}  "
                  f"e2e {r['accuracy_end_to_end']:.4f}  "
                  f"CONFLICT {r['conflict']:>6}  "
                  f"silent {r['silent_error_rate']:.4f}")
    print(f"    ρ {hidden.rho:+.4f}   required inequalities "
          f"{hid['violations']['required']}, violated "
          f"{hid['violations']['violated']}")

    # ---- the five rows ----------------------------------------------------
    by_centre = {b["centre"]: b for b in per_bin}
    key = f"{BAND_SURFACE}_{BAND_ENCODING}"

    hidden_bin = by_centre[g.RHO_HIDDEN]
    hidden_e2e = hid[(BAND_SURFACE, BAND_ENCODING)]["accuracy_end_to_end"]
    lo = hidden_bin["central_band_band_surface"]["low"]
    hi = hidden_bin["central_band_band_surface"]["high"]
    a_a = {"row": "A-a", "band": f"inside the central {CENTRAL:.0%} of its own bin",
           "refuted_by": "outside it",
           "hidden_e2e": round(hidden_e2e, 6), "bin_low": lo, "bin_high": hi,
           "inside": lo <= hidden_e2e <= hi}
    a_a["verdict"] = "HOLDS" if a_a["inside"] else "REFUTED"

    centres = [b["centre"] for b in per_bin]
    medians = {e: [b["e2e_median"][f"{BAND_SURFACE}_{e}"] for b in per_bin]
               for e in m.ENCODINGS}
    rho_pub = g.spearman(centres, medians[m.PUBLISHED])
    rho_cor = g.spearman(centres, medians[m.CORRECTED])
    a_b = {"row": "A-b", "band": f">= {A_B_MIN_SPEARMAN}",
           "refuted_by": f"< {A_B_MIN_SPEARMAN}",
           "spearman": round(rho_pub, 6)}
    a_b["verdict"] = ("HOLDS" if a_b["spearman"] >= A_B_MIN_SPEARMAN
                      else "REFUTED")

    top = per_bin[-1]
    a_c = {"row": "A-c", "band": f"<= {A_C_MAX_MEDIAN}",
           "refuted_by": f"> {A_C_MAX_MEDIAN}",
           "top_bin": top["centre"], "median_e2e": top["e2e_median"][key]}
    a_c["verdict"] = ("HOLDS" if a_c["median_e2e"] <= A_C_MAX_MEDIAN
                      else "REFUTED")

    zero = by_centre[0.0]
    a_d = {"row": "A-d", "band": f">= {A_D_MIN_FRACTION}",
           "refuted_by": f"< {A_D_MIN_FRACTION}",
           "fraction_with_a_violation": zero["fraction_with_a_violation"],
           "required_median": zero["violations_required_median"],
           "violated_median": zero["violations_median"]}
    a_d["verdict"] = ("HOLDS"
                      if a_d["fraction_with_a_violation"] >= A_D_MIN_FRACTION
                      else "REFUTED")

    a_e = {"row": "A-e", "band": f"<= {A_E_MAX_DIFFERENCE}",
           "refuted_by": f"> {A_E_MAX_DIFFERENCE}",
           "spearman_published": round(rho_pub, 6),
           "spearman_corrected": round(rho_cor, 6),
           "difference": round(abs(rho_pub - rho_cor), 6)}
    a_e["verdict"] = ("HOLDS" if a_e["difference"] <= A_E_MAX_DIFFERENCE
                      else "REFUTED")

    verdicts = [a_a, a_b, a_c, a_d, a_e]
    print("\n" + "=" * 78)
    print(f"THE FIVE ROWS · read on the {BAND_SURFACE}, {BAND_ENCODING} encoding")
    print("=" * 78)
    print(f"  {'row':<6}{'band':<14}{'measured':>34}{'verdict':>12}")
    measured = {
        "A-a": f"{a_a['hidden_e2e']:.4f} against [{lo:.4f}, {hi:.4f}]",
        "A-b": f"Spearman {a_b['spearman']:.4f} over 13 bins",
        "A-c": f"median {a_c['median_e2e']:.4f} at ρ {top['centre']:+.2f}",
        "A-d": f"{a_d['fraction_with_a_violation']:.2f} of the ρ=0 draws",
        "A-e": f"|{rho_pub:.4f} − {rho_cor:.4f}| = {a_e['difference']:.4f}",
    }
    for v in verdicts:
        print(f"  {v['row']:<6}{v['band']:<14}{measured[v['row']]:>34}"
              f"{v['verdict']:>12}")

    print("\n  THE CURVE, both encodings, medians on the space")
    print(f"  {'ρ':>9}{'published':>12}{'corrected':>12}{'lift':>8}"
          f"{'CONFLICT pub':>14}{'viol. any':>11}")
    for b in per_bin:
        p = b["e2e_median"][f"{SPACE}_{m.PUBLISHED}"]
        c = b["e2e_median"][f"{SPACE}_{m.CORRECTED}"]
        print(f"  {b['centre']:>+9.4f}{p:>12.4f}{c:>12.4f}{c - p:>8.4f}"
              f"{b['conflict_rate_median'][f'{SPACE}_{m.PUBLISHED}']:>14.4f}"
              f"{b['fraction_with_a_violation']:>11.2f}")

    payload = {
        "_env": environment(sweep_seed=SWEEP_SEED, sweep_draws=SWEEP_DRAWS),
        "what": "the sensitivity sweep of PLAN_SENSITIVITY.md: 13 ρ bins × 100 "
                "draws × 2 surfaces × 2 encodings, and the five signed rows",
        "plan": {"file": str(PLAN), "signatures": gate["lines"],
                 "bands_read_on": {"surface": BAND_SURFACE,
                                   "encoding": BAND_ENCODING,
                                   "why": "§0 fixes the space and the published "
                                          "encoding for A-a, and A-e implies the "
                                          "published curve for A-b by comparing "
                                          "the two"}},
        "grid": {"centres": list(g.RHO_BINS), "tolerance": g.RHO_TOLERANCE,
                 "rho_hidden": g.RHO_HIDDEN},
        "central_band_convention": {
            "central": CENTRAL,
            "definition": "[sorted[k], sorted[n-1-k]] with k = round(n(1-c)/2); "
                          "inside is inclusive",
            "declared_before": "any figure of the sweep existed"},
        "gate": gate,
        "per_bin": per_bin,
        "hidden_policy": hidden_row,
        "rows": {v["row"]: v for v in verdicts},
        "draws": rows,
        "seconds": round(time.time() - t0, 1),
    }
    print(f"\n  {payload['seconds']:.0f}s, zero API calls")
    if dry_run:
        print("  --dry-run: nothing written.")
        return 0
    OUT.mkdir(exist_ok=True)
    (OUT / RECORD).write_text(json.dumps(payload, indent=2))
    print(f"-> {OUT / RECORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
