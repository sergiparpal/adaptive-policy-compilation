"""
Stage A of `PLAN_REUSE.md` — the eight n=100 records, read for the founding
question for the first time. Free, and `U-f`: reported, not adjudicated.

For each of the eight: the split of its silent errors by the birth action of
the rule that made each one (the two axes, §5.2), the reuse and silent error of
the rules born with the right queue, and their gap against the `keep_k` frontier
on that record's own corpus at n=100 (§5.2's `F`). Then the same, pooled by
prompt. Beside it, each run's escalations by true queue, and the memorization
floor at n=100 — `keep_k(8)`'s reuse on that corpus — because the 0.1176 of
n=2000 is not the floor at a twentieth of the horizon.

**It runs only after §0 is signed**, and that is not a formality for a free
stage: these are exactly the figures that would inform `U-b`'s and `U-c`'s bands,
and without the gate the only thing between them is commit order. Until then
`--dry-run` runs the blocking checks and writes and prints nothing of `U-f`.

    python3 -m reuse.readout --dry-run
    python3 -m reuse.readout             # refuses while PLAN_REUSE.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from . import analysis, frontier, gates, plan

RECORD = plan.OUT / f"readout_n{plan.N_EIGHT}.json"
ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"


def read_run(prompt: str, seed: int, rec: dict, keep_k: dict[int, dict]) -> dict:
    born, _ = analysis.births(rec)
    rb = analysis.right_born(rec, born)
    points = analysis.frontier_points(keep_k)
    m = rec["metrics"]
    return {
        "prompt": prompt, "seed": seed, "n": rec["n"],
        "rules": m["n_rules"],
        "reuse_rate": m["reuse_rate"],
        "silent_error_rate": m["silent_error_rate"],
        "proposal_action_accuracy": m["proposal_action_accuracy"],
        "e2e_accuracy": m["e2e_accuracy"],
        "split": analysis.split_silent(rec, born),
        "right_born": rb,
        "F_at_their_reuse": (analysis.F(points, rb["reuse_rate"])
                             if rb["reuse_rate"] is not None else None),
        "gap": analysis.gap(rb, points),
        "memorization_floor": keep_k[8]["reuse_rate"],
        "escalations_by_truth": analysis.escalations_by_truth(rec),
        ONCALL: analysis.class_ledger(rec, ONCALL),
        SECURITY: analysis.class_ledger(rec, SECURITY),
        "fires": analysis.fire_distribution(rec),
        "conflict_share_of_escalations": analysis.conflict_share(rec),
    }


def pool_prompt(runs: list[dict], keep_k_by_seed: dict[int, dict[int, dict]]) -> dict:
    """One prompt's four runs, pooled: counts summed and rates recomputed, and
    the frontier pooled the same way over the same four corpora."""
    rb = analysis.pooled(r["right_born"] for r in runs)
    points = analysis.frontier_points({
        k: analysis.pooled(keep_k_by_seed[r["seed"]][k] for r in runs)
        for k in frontier.KS})
    wrong = sum(r["split"]["by_rules_born_wrong"] for r in runs)
    total = sum(r["split"]["silent_errors"] for r in runs)
    return {
        "runs": len(runs),
        "silent_errors": total,
        "share_born_wrong": wrong / total if total else None,
        "right_born": rb,
        "F_at_their_reuse": (analysis.F(points, rb["reuse_rate"])
                             if rb["reuse_rate"] is not None else None),
        "gap": analysis.gap(rb, points),
    }


def readout(checks: gates.Checks) -> dict[str, Any]:
    keep_k_by_seed = {seed: {k: frontier.counts(res) for k, res in runs.items()}
                      for seed, runs in checks.runs_100.items()}
    runs = [read_run(prompt, seed, json.loads(path.read_text()),
                     keep_k_by_seed[seed])
            for prompt, seed, path in plan.EIGHT]
    return {
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "A",
        "row": "U-f",
        "provenance": ("REPORTED, NOT ADJUDICATED: its inputs have been on disk "
                       "since 2026-08-07 and the drafter had read their metrics "
                       "blocks (§0)"),
        "surface": "corpus — each run's own, n=100, in arrival order",
        "gates": checks.summary(),
        "records": [str(p) for _, _, p in plan.EIGHT],
        "runs": runs,
        "pooled_by_prompt": {p: pool_prompt([r for r in runs if r["prompt"] == p],
                                            keep_k_by_seed)
                             for p in ("v1", "v2")},
    }


def show(out: dict) -> None:
    fmt = lambda x: "—" if x is None else f"{x:.4f}"
    print(f"\n{'prompt':<7}{'seed':>5}{'reuse':>8}{'silent':>8}"
          f"{'born wrong':>12}{'rb reuse':>10}{'rb silent':>11}{'F':>8}{'gap':>9}")
    for r in out["runs"]:
        print(f"{r['prompt']:<7}{r['seed']:>5}{fmt(r['reuse_rate']):>8}"
              f"{fmt(r['silent_error_rate']):>8}"
              f"{fmt(r['split']['share_born_wrong']):>12}"
              f"{fmt(r['right_born']['reuse_rate']):>10}"
              f"{fmt(r['right_born']['silent_error']):>11}"
              f"{fmt(r['F_at_their_reuse']):>8}{fmt(r['gap']):>9}")
    for p, q in out["pooled_by_prompt"].items():
        print(f"{p + ' pooled':<12}{'':>8}{'':>8}{fmt(q['share_born_wrong']):>12}"
              f"{fmt(q['right_born']['reuse_rate']):>10}"
              f"{fmt(q['right_born']['silent_error']):>11}"
              f"{fmt(q['F_at_their_reuse']):>8}{fmt(q['gap']):>9}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage A of PLAN_REUSE.md: the eight n=100 records (U-f).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the blocking checks; write and print nothing of U-f")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written, and nothing of U-f computed for display")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"reuse/readout.py writes {RECORD}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    out = readout(checks)
    show(out)
    plan.OUT.mkdir(exist_ok=True)
    RECORD.write_text(json.dumps(out, indent=2))
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
