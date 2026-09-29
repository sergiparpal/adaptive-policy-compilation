"""
The `keep_k` frontier through the frozen loop — `U-g3`, and Stage A's reference.

`keep_k` (`harness/proposers.py`) writes one rule per escalation: `k` equality
conditions over the first `k` attributes of `harness/domain.ATTRIBUTES`, and the
ticket's true action, handed to it. It was built to trace *"the reference the
real LLM is judged against afterwards"*, and `CLAUDE.md` Step 1 declared that
reference invalid while the engine could not execute the policy. `PLAN_REUSE.md`
uses it under rung 2's engine, and this module is where the plan checks that the
reference carries over instead of assuming it.

WHY IT SHOULD CARRY OVER. Two `keep_k` rules share their attributes, so they are
either identical or disjoint, and an identical second rule is never born — the
first would have decided its ticket. So no case is ever matched by two of its
rules, and an engine that never has to arbitrate cannot matter: specificity and
subsumption alike. **`U-g3` checks it rather than arguing it**: over the n=2000
corpus the eight runs reproduce `results/frontier.json` exactly, and in no run —
there, or at n=100 over the corpora of seeds 17 to 20 — is any case matched by
more than one rule.

Everything runs through the frozen `harness.shadow.run_shadow` with the frozen
`harness.dsl.RuleEngine`, exactly as `run_experiment.py frontier` does. This
module imports no oracle: the labels are in the records the frozen loop writes.

    python3 -m reuse.frontier --dry-run   # U-g3 alone, writes nothing
    python3 -m reuse.frontier             # refuses while PLAN_REUSE.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from harness.domain import generate_corpus
from harness.dsl import RuleEngine
from harness.proposers import KeepKProposer
from harness.provenance import describe, environment
from harness.shadow import RunResult, run_shadow

from . import analysis, plan

KS = tuple(range(1, 9))
PUBLISHED = Path("results/frontier.json")
RECORD = plan.OUT / "frontier.json"


def keep_k_runs(n: int, seed: int) -> dict[int, RunResult]:
    corpus = generate_corpus(n, seed=seed)
    return {k: run_shadow(corpus, RuleEngine(), KeepKProposer(k)) for k in KS}


def counts(res: RunResult) -> dict[str, Any]:
    """The counts `analysis.pooled` works on, off one frozen-loop run."""
    return analysis.pooled([{
        "rules": len(res.rules),
        "reused": sum(1 for r in res.rules if r.fire_count >= 1),
        "decided": sum(1 for r in res.records if r.outcome == "ACTION"),
        "correct": sum(1 for r in res.records
                       if r.outcome == "ACTION" and r.correct),
    }])


def truth_sequence(res: RunResult) -> list[tuple[str, str]]:
    """What the frozen loop labelled each case of the corpus, in order."""
    return [(r.truth, r.truth_rule) for r in res.records]


def published_metrics() -> dict[int, dict]:
    results = json.loads(PUBLISHED.read_text())["results"]
    return {k: results[f"keep_k_{k}"] for k in KS}


def published_points() -> list[tuple[float, float]]:
    """`F`'s points at n=2000, off the record that owns them. `U-g3` is what
    licenses reading them under rung 2's engine."""
    return analysis.frontier_points({
        k: {"reuse_rate": m["reuse_rate"], "silent_error": m["silent_error_rate"]}
        for k, m in published_metrics().items()})


def max_matched(runs: dict[int, RunResult]) -> int:
    return max(r.n_matched for res in runs.values() for r in res.records)


def gate_ug3(runs_n: dict[int, RunResult],
             runs_100: dict[int, dict[int, RunResult]]) -> dict[str, Any]:
    published = published_metrics()
    mismatched = [k for k in KS if runs_n[k].metrics != published[k]]
    most = max([max_matched(runs_n)] + [max_matched(r) for r in runs_100.values()])
    return {
        "what": ("keep_k(1..8) over the n=2000 corpus reproduces "
                 "results/frontier.json exactly, and no case of any run — n=2000, "
                 "or n=100 over seeds 17 to 20 — is matched by more than one rule"),
        "reproduces_published": not mismatched,
        "k_not_reproduced": mismatched,
        "most_rules_matching_one_case": most,
        "passes": not mismatched and most <= 1,
    }


def payload(runs_n: dict[int, RunResult],
            runs_100: dict[int, dict[int, RunResult]], ug3: dict) -> dict:
    per_seed = {seed: {k: counts(res) for k, res in runs.items()}
                for seed, runs in runs_100.items()}
    return {
        "_env": environment(seed=plan.SEED),
        "plan": str(plan.PLAN),
        "stage": "A",
        "surface": "corpus",
        "provenance": ("PRE-REGISTERED plan, REPORTED row: U-f carries no band "
                       "(§0), and these are its reference points"),
        "U-g3": ug3,
        f"n{plan.N}_seed{plan.SEED}": {k: counts(res) for k, res in runs_n.items()},
        f"n{plan.N_EIGHT}": per_seed,
        f"n{plan.N_EIGHT}_pooled_over_seeds": {
            k: analysis.pooled(per_seed[s][k] for s in per_seed) for k in KS},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="The keep_k frontier of PLAN_REUSE.md, through the frozen loop.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run U-g3 and write nothing")
    args = ap.parse_args(argv)

    if not args.dry_run:
        plan.refuse_unsigned(f"reuse/frontier.py writes {RECORD}")
        from . import gates                   # the full set, before any write
        checks = gates.run_all(suite=True)
        gates.report(checks)
        if not checks.blocking_pass:
            sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
        runs_n, runs_100, ug3 = checks.runs_n, checks.runs_100, checks.ug3
    else:
        runs_n = keep_k_runs(plan.N, plan.SEED)
        runs_100 = {s: keep_k_runs(plan.N_EIGHT, s) for s in plan.EIGHT_SEEDS}
        ug3 = gate_ug3(runs_n, runs_100)
        print(f"U-g3  {'PASS' if ug3['passes'] else 'FAIL'} — reproduces "
              f"results/frontier.json: {ug3['reproduces_published']}; most rules "
              f"matching one case: {ug3['most_rules_matching_one_case']}")
        print("dry run: nothing written")
        return 0 if ug3["passes"] else 1

    plan.OUT.mkdir(exist_ok=True)
    RECORD.write_text(json.dumps(payload(runs_n, runs_100, ug3), indent=2))
    print(f"\n-> {RECORD}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
