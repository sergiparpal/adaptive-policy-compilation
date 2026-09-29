"""
Stage C of `PLAN_REUSE.md` — the five adjudications, from Stage B's records.
Free, and it refuses while the plan is unsigned.

Each run is first checked the way `U-g2` checked the eight old records (§5.3):
its metrics and fire counts recompute from its own cases, every rule has one
birth, and its corpus is the one seed 17 draws. Then, per run:

  U-a  reuse_rate                                   holds at >= 0.30
  U-b  right-born silent error − F(their reuse)     holds at > 0
  U-c  silent errors by rules born wrong / all      holds at >= 0.60
  U-d  escalations whose true queue is ONCALL       holds at >= 1
  U-e  CONFLICT outcomes over the 2,000             holds at <= 20

**The median over the runs adjudicates** and each run's value is published
beside it (§0). `F` at n=2000 is read off `results/frontier.json`, the record
that owns it; `U-g3` is what licenses reading it under rung 2's engine.

Recorded beside the rows and never in a denominator: the distribution of fires,
e2e, silent error and the proposer's accuracy side by side, the escalation curve
and the share of escalations that were CONFLICT — above one in four `U-a` carries
rung 1's caveat — `SECURITY_INCIDENT` and `ONCALL_ESCALATION` counted, and every
`try_edge` verdict, `contradice_subsuncion` included: it has never fired in a
real run.

    python3 -m reuse.score --dry-run
    python3 -m reuse.score               # refuses while PLAN_REUSE.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from . import analysis, frontier, gates, plan

RECORD = plan.OUT / "score.json"
ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"
HOLDS, REFUTED, NO_VERDICT = "holds", "refuted", "unadjudicable"


# ---------------------------------------------------------------------------
# The five lines of §0, as functions, so that their edges can be pinned
# ---------------------------------------------------------------------------

def verdict_u_a(reuse: float | None) -> str:
    if reuse is None:
        return NO_VERDICT
    return HOLDS if reuse >= plan.U_A_MIN_REUSE else REFUTED


def verdict_u_b(gap: float | None) -> str:
    if gap is None:
        return NO_VERDICT
    return HOLDS if gap > plan.U_B_REFUTED_AT_OR_BELOW else REFUTED


def verdict_u_c(share: float | None) -> str:
    if share is None:
        return NO_VERDICT
    return HOLDS if share >= plan.U_C_MIN_SHARE else REFUTED


def verdict_u_d(oncall_escalations: float | None) -> str:
    if oncall_escalations is None:
        return NO_VERDICT
    return HOLDS if oncall_escalations >= plan.U_D_MIN_ONCALL else REFUTED


def verdict_u_e(conflicts: float | None) -> str:
    if conflicts is None:
        return NO_VERDICT
    return HOLDS if conflicts <= plan.U_E_MAX_CONFLICTS else REFUTED


VERDICTS = {"U-a": verdict_u_a, "U-b": verdict_u_b, "U-c": verdict_u_c,
            "U-d": verdict_u_d, "U-e": verdict_u_e}


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------

def score_run(rec: dict, points: list[tuple[float, float]],
              truth: list[tuple[str, str]]) -> dict[str, Any]:
    problems = gates.check_record(rec, n=plan.N, seed=plan.SEED,
                                  prompt=plan.PROMPT, truth=truth)
    born, _ = analysis.births(rec)
    split = analysis.split_silent(rec, born)
    rb = analysis.right_born(rec, born)
    m = analysis.recompute_metrics(rec)
    share = analysis.conflict_share(rec)
    reasons = m["edge_reasons"]
    return {
        "rep": rec.get("rep"),
        "problems": problems,
        "rows": {
            "U-a": m["reuse_rate"],
            "U-b": analysis.gap(rb, points),
            "U-c": split["share_born_wrong"],
            "U-d": analysis.escalations_by_truth(rec).get(ONCALL, 0),
            "U-e": m["conflicts"],
        },
        "beside": {
            "right_born": rb,
            "F_at_their_reuse": (analysis.F(points, rb["reuse_rate"])
                                 if rb["reuse_rate"] is not None else None),
            "split": split,
            "fires": analysis.fire_distribution(rec),
            "n_rules": m["n_rules"],
            "e2e_accuracy": m["e2e_accuracy"],
            "silent_error_rate": m["silent_error_rate"],
            "proposal_action_accuracy": m["proposal_action_accuracy"],
            "escalations": m["escalations"],
            "escalation_curve_by_decile": m["escalation_curve_by_decile"],
            "conflict_share_of_escalations": share,
            "U-a_carries_rung_1_caveat": (share is not None and
                                          share > plan.U_A_CAVEAT_CONFLICT_SHARE),
            ONCALL: analysis.class_ledger(rec, ONCALL),
            SECURITY: analysis.class_ledger(rec, SECURITY),
            "edges_proposed": m["edges_proposed"],
            "edges_accepted": m["edges_accepted"],
            "edge_verdicts": reasons,
            "contradice_subsuncion": reasons.get("contradice_subsuncion", 0),
        },
    }


def adjudicate(runs: list[dict]) -> dict[str, dict]:
    out = {}
    for row, verdict in VERDICTS.items():
        values = [r["rows"][row] for r in runs]
        median = analysis.median_of(values)
        out[row] = {"per_run": values, "median": median, "verdict": verdict(median)}
    return out


def load_runs() -> tuple[list[dict], list[str]]:
    found, missing = [], []
    for rep in range(1, plan.REPS + 1):
        path = plan.run_path(rep)
        if path.exists():
            found.append(json.loads(path.read_text()))
        else:
            missing.append(str(path))
    return found, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage C of PLAN_REUSE.md: the five adjudications.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the blocking checks and list the runs present")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        found, missing = load_runs()
        print(f"\n  Stage B records present: {len(found)} of {plan.REPS}"
              + (f" — missing {', '.join(missing)}" if missing else ""))
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"reuse/score.py writes {RECORD}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    found, missing = load_runs()
    if missing:
        sys.exit(f"\nREFUSED: Stage B is incomplete — missing {', '.join(missing)}\n")

    points = frontier.published_points()
    truth = frontier.truth_sequence(checks.runs_n[1])
    runs = [score_run(rec, points, truth) for rec in found]
    bad = [(r["rep"], p) for r in runs for p in r["problems"]]
    if bad:
        for rep, p in bad[:20]:
            print(f"  run {rep}: {p}")
        sys.exit("\nREFUSED: a Stage B record does not reproduce itself (§5.3).\n")

    verdicts = adjudicate(runs)
    for row, v in verdicts.items():
        print(f"  {row}  median {v['median']}  ->  {v['verdict']}   "
              f"per run {v['per_run']}")
    plan.OUT.mkdir(exist_ok=True)
    RECORD.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "C",
        "surface": f"corpus — n={plan.N}, seed {plan.SEED}, in arrival order",
        "provenance": "PRE-REGISTERED: §0 signed before any of these figures existed",
        "gates": checks.summary(),
        "frontier_points": points,
        "verdicts": verdicts,
        "runs": runs,
    }, indent=2))
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
