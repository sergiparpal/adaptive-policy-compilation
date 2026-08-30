"""
THE FOUR ROWS — `I-a` to `I-d` of `PLAN_ILP.md` §0.

--------------------------------------------------------------------------
THE GATE
--------------------------------------------------------------------------
§8: this plan spends nothing and still gets a gate, because what the gate protects
is not money — it is that the bands were signed before the figures existed.

**It reads `PLAN_ILP.md` and no other plan**, and it counts the signatures rather
than stopping at the first: §0's table and §1's amendment of 2026-08-30 each carry
one, and a gate that read only the first would find §0 signed and report `ok` over
an unsigned amendment. `--dry-run` runs everything and writes nothing.

--------------------------------------------------------------------------
WHAT IS READ WHERE, AFTER §1'S AMENDMENT
--------------------------------------------------------------------------
`I-a`  trained on **train_316**, scored on corpus test split 0. The conservative
       set: the proposer's rules saw all 632, so 316 hands the inducer less
       material while matching the order's handicap. The 632 figure is reported
       beside it and is not what the band reads.
`I-b`  trained on **train_632**, the matched set — the inducer gets the 6
       `T3_ENGINEERING` and 29 `ACCOUNT_MANAGER` examples the proposer got.
`I-c`  `I-a`'s list, scored over the 134,400.
`I-d`  `I-a`'s list, counted.

**Every row is read at both declared beam widths** and a row whose verdict differs
between them is reported as unstable rather than as a verdict — `I-g4`.

Usage:  python3 -m ilp.compare [--dry-run]
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from harness.provenance import describe as describe_env, environment

from . import induce as ind
from . import instances as inst

PLAN = Path("PLAN_ILP.md")
OUT = Path("results_ilp")
RECORD = "compare.json"

SIGNATURE = "**Signed by Sergi:"
MIN_SIGNATURES = 2                 # §0's table and §1's amendment
BLANKS = re.compile(r"_{3,}")

# --- the four signed bands, transcribed from §0 ------------------------------
# Sergi's, signed 2026-08-30 before any figure of this plan existed. Named
# constants and pinned by `tests/test_ilp.py` for the reason §7 gives: so that
# moving a band after seeing a figure is visible in a diff.
I_A_MIN = 0.8530                   # the searched order over the 577 LLM rules
I_B_CEILING = {"T3_ENGINEERING": 39 / 117, "ACCOUNT_MANAGER": 39 / 109}
I_C_MIN = 0.50                     # e2e over the exhaustive space
I_D_MAX = 58                       # rules, against 29 for the manual and 577

SPLIT_SEED = 17


def gate_signature(path: Path = PLAN) -> dict:
    lines = [l.strip() for l in path.read_text().splitlines()
             if l.startswith(SIGNATURE)] if path.exists() else []
    unsigned = [l for l in lines if BLANKS.search(l)]
    return {
        "what": f"every line starting `{SIGNATURE}` in {path.name}, of which "
                f"there must be at least {MIN_SIGNATURES}: §0's table and §1's "
                "amendment of 2026-08-30",
        "source": str(path), "found": len(lines), "lines": lines,
        "unsigned": unsigned,
        "passes": len(lines) >= MIN_SIGNATURES and not unsigned,
    }


def run(train: str, beam: int) -> dict:
    """Induce on one training set, score everywhere a row is read."""
    ext, truth, n = inst.instance(train)
    got = ind.induce(ext, truth, n, beam=beam)
    out = {
        "train": train, "beam": beam,
        "n_rules": got.n_rules, "n_conditions": got.n_conditions,
        "hit_the_cap": got.hit_the_cap,
        "left_undecided_on_train": got.left_undecided,
        "seconds": got.seconds,
        "train_score": ind.score(got, ext, truth, n),
    }
    for surface in ("test", "space", "corpus"):
        s_ext, s_truth, s_n = inst.instance(surface)
        out[surface] = ind.score(got, s_ext, s_truth, s_n)
    out["rules"] = ind.as_dsl(got)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry_run = "--dry-run" in argv
    t0 = time.time()

    gate = gate_signature()
    print("=" * 78)
    print("I-a TO I-d — the four rows of PLAN_ILP.md §0")
    print("=" * 78)
    print(f"  beams {ind.BEAM_WIDTHS} · zero API calls · the inducer runs on the "
          f"standard library")
    print(f"  {describe_env()}")
    print(f"\n  GATE · signatures found {gate['found']} "
          f"(at least {MIN_SIGNATURES}), unsigned {len(gate['unsigned'])}  ->  "
          f"{'ok' if gate['passes'] else 'REFUSES TO WRITE'}")
    if not gate["passes"] and not dry_run:
        print("\n  STOP. The plan is not signed, so no record is written. There "
              "is no\n  flag that skips this; `--dry-run` writes nothing anyway.")
        return 1

    runs = {(train, beam): run(train, beam)
            for train in ("train_316", "train_632")
            for beam in ind.BEAM_WIDTHS}

    print("\n  THE INDUCED LISTS")
    print(f"  {'train':<11}{'beam':>6}{'rules':>7}{'conds':>7}{'train e2e':>11}"
          f"{'test e2e':>10}{'space e2e':>11}{'secs':>7}")
    for (train, beam), r in runs.items():
        print(f"  {train:<11}{beam:>6}{r['n_rules']:>7}{r['n_conditions']:>7}"
              f"{r['train_score']['accuracy_end_to_end']:>11.4f}"
              f"{r['test']['accuracy_end_to_end']:>10.4f}"
              f"{r['space']['accuracy_end_to_end']:>11.4f}{r['seconds']:>7.1f}")

    def by_beam(train, field):
        return {b: field(runs[(train, b)]) for b in ind.BEAM_WIDTHS}

    # ---- I-a --------------------------------------------------------------
    a_vals = by_beam("train_316", lambda r: r["test"]["accuracy_end_to_end"])
    a_verdicts = {b: ("HOLDS" if v > I_A_MIN else "REFUTED")
                  for b, v in a_vals.items()}
    i_a = {"row": "I-a", "band": f"> {I_A_MIN}", "refuted_by": f"<= {I_A_MIN}",
           "trained_on": "train_316", "surface": "corpus test split 0, puro",
           "by_beam": {str(b): round(v, 6) for b, v in a_vals.items()},
           "verdict_by_beam": {str(b): v for b, v in a_verdicts.items()},
           "stable": len(set(a_verdicts.values())) == 1,
           "reported_beside": {
               "train_632": {str(b): round(v, 6) for b, v in by_beam(
                   "train_632",
                   lambda r: r["test"]["accuracy_end_to_end"]).items()}}}
    i_a["verdict"] = (list(a_verdicts.values())[0] if i_a["stable"]
                      else "UNSTABLE ACROSS BEAMS — not a verdict")

    # ---- I-b --------------------------------------------------------------
    b_rows, b_verdicts = {}, {}
    for beam in ind.BEAM_WIDTHS:
        per = runs[("train_632", beam)]["test"]["per_class"]
        got = {c: per.get(c, {"accuracy": 0.0, "n": 0, "correct": 0})
               for c in I_B_CEILING}
        above = {c: got[c]["accuracy"] > I_B_CEILING[c] for c in I_B_CEILING}
        b_rows[str(beam)] = {c: {"accuracy": round(got[c]["accuracy"], 6),
                                 "correct": got[c]["correct"], "n": got[c]["n"],
                                 "ceiling": round(I_B_CEILING[c], 6),
                                 "above": above[c]} for c in I_B_CEILING}
        b_verdicts[str(beam)] = "HOLDS" if all(above.values()) else "REFUTED"
    i_b = {"row": "I-b", "band": "above the ceiling in both classes",
           "refuted_by": "at or below it in either", "trained_on": "train_632",
           "surface": "corpus test split 0", "by_beam": b_rows,
           "verdict_by_beam": b_verdicts,
           "stable": len(set(b_verdicts.values())) == 1,
           "warning": "PLAN_ILP.md §1's amendment: T3_ENGINEERING has 6 training "
                      "examples and ACCOUNT_MANAGER 29 in this set. The row can "
                      "be refuted by scarcity rather than by induction."}
    i_b["verdict"] = (list(b_verdicts.values())[0] if i_b["stable"]
                      else "UNSTABLE ACROSS BEAMS — not a verdict")

    # ---- I-c and I-d ------------------------------------------------------
    c_vals = by_beam("train_316", lambda r: r["space"]["accuracy_end_to_end"])
    c_verdicts = {b: ("HOLDS" if v >= I_C_MIN else "REFUTED")
                  for b, v in c_vals.items()}
    i_c = {"row": "I-c", "band": f">= {I_C_MIN}", "refuted_by": f"< {I_C_MIN}",
           "trained_on": "train_316", "surface": "exhaustive space, 134,400",
           "by_beam": {str(b): round(v, 6) for b, v in c_vals.items()},
           "verdict_by_beam": {str(b): v for b, v in c_verdicts.items()},
           "stable": len(set(c_verdicts.values())) == 1}
    i_c["verdict"] = (list(c_verdicts.values())[0] if i_c["stable"]
                      else "UNSTABLE ACROSS BEAMS — not a verdict")

    d_vals = by_beam("train_316", lambda r: r["n_rules"])
    d_verdicts = {b: ("HOLDS" if v <= I_D_MAX else "REFUTED")
                  for b, v in d_vals.items()}
    i_d = {"row": "I-d", "band": f"<= {I_D_MAX}", "refuted_by": f"> {I_D_MAX}",
           "trained_on": "train_316", "against": {"hidden_policy": 29,
                                                  "learned_base": 577},
           "by_beam": {str(b): v for b, v in d_vals.items()},
           "verdict_by_beam": {str(b): v for b, v in d_verdicts.items()},
           "stable": len(set(d_verdicts.values())) == 1}
    i_d["verdict"] = (list(d_verdicts.values())[0] if i_d["stable"]
                      else "UNSTABLE ACROSS BEAMS — not a verdict")

    rows = [i_a, i_b, i_c, i_d]
    print("\n" + "=" * 78)
    print("THE FOUR ROWS")
    print("=" * 78)
    print(f"  {'row':<6}{'band':<22}{'beam 40':>12}{'beam 120':>12}"
          f"{'verdict':>14}")
    print(f"  {'I-a':<6}{i_a['band']:<22}"
          f"{a_vals[40]:>12.4f}{a_vals[120]:>12.4f}{i_a['verdict']:>14}")
    for c in I_B_CEILING:
        print(f"  {'I-b':<6}{c.lower():<22}"
              f"{b_rows['40'][c]['accuracy']:>12.4f}"
              f"{b_rows['120'][c]['accuracy']:>12.4f}"
              f"{'(ceiling ' + format(I_B_CEILING[c], '.4f') + ')':>14}")
    print(f"  {'':<6}{'both above?':<22}{'':>12}{'':>12}{i_b['verdict']:>14}")
    print(f"  {'I-c':<6}{i_c['band']:<22}"
          f"{c_vals[40]:>12.4f}{c_vals[120]:>12.4f}{i_c['verdict']:>14}")
    print(f"  {'I-d':<6}{i_d['band']:<22}"
          f"{d_vals[40]:>12}{d_vals[120]:>12}{i_d['verdict']:>14}")

    print("\n  REPORTED BESIDE, NOT BANDED — the matched training set for I-a")
    print(f"    train_632, test e2e: {i_a['reported_beside']['train_632']}")

    payload = {
        "_env": environment(beams=list(ind.BEAM_WIDTHS), split_seed=SPLIT_SEED),
        "what": "I-a to I-d of PLAN_ILP.md: a symbolic inducer as a competitor "
                "to the LLM proposer, on the material the proposer saw",
        "plan": {"file": str(PLAN), "signatures": gate["lines"]},
        "bands": {"I_A_MIN": I_A_MIN, "I_B_CEILING": I_B_CEILING,
                  "I_C_MIN": I_C_MIN, "I_D_MAX": I_D_MAX},
        "gate": gate,
        "instances": {n: inst.describe(n)
                      for n in ("train_316", "train_632", "test", "space")},
        "runs": {f"{t}|{b}": r for (t, b), r in runs.items()},
        "rows": {r["row"]: r for r in rows},
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
