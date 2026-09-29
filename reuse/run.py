"""
Stage B of `PLAN_REUSE.md` — rung 2's loop over the 2,000 cases of seed 17,
prompt v1. **The only module of the plan that spends.**

The loop is rung 2's, called and not copied (rule A): a fresh
`PriorityEngine(space=Space())`, `OpenRouterProposer2(model, prompt_version="v1")`
and `run_shadow2`, exactly as the four v1 records of 2026-08-07 were produced.
Only the horizon changes, and the number of repetitions. The record keeps
`rung2/run2.py`'s layout, so that Stage C reads the eight old records and these
with the same functions.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken:

  1. `--dry-run` runs `U-g1` to `U-g3`, prints the signature's state, and stops.
     It never builds the client and never needs the key.
  2. The signature (`U-g4`). While `PLAN_REUSE.md` carries a blank signature
     line this module exits here — before the checks, the destination, the
     corpus or the client. No flag skips it.
  3. `U-g1` to `U-g3`, blocking.
  4. The destination: a paid record is never overwritten
     (`harness/record_guard.py`), and the flag that would is not typed without
     Sergi asking.
  5. The client, and the calls — sequential, hard rule 3.

    python3 -m reuse.run --dry-run
    .venv/bin/python -m reuse.run --smoke      # 20 cases, before the first run
    .venv/bin/python -m reuse.run --rep 1      # then 2, then 3, one after another
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from harness.domain import generate_corpus
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from rung2.engine2 import PriorityEngine, Space
from rung2.proposers2 import OpenRouterProposer2
from rung2.shadow2 import run_shadow2

from . import gates, plan


def destination(args: argparse.Namespace) -> Path:
    return plan.SMOKE_PATH if args.smoke else plan.run_path(args.rep)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_REUSE.md: rung 2's loop at n=2000 (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run U-g1 to U-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases under their own name, first")
    which.add_argument("--rep", type=int, choices=range(1, plan.REPS + 1),
                       help=f"which of the {plan.REPS} runs of §2")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned("reuse/run.py spends")

    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")

    target = or_exit(refuse_overwrite, destination(args),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    n = plan.SMOKE_N if args.smoke else plan.N
    corpus = generate_corpus(n, seed=plan.SEED)
    engine = PriorityEngine(space=Space())
    proposer = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT)

    print(f"\n{plan.PLAN} · stage B · {'smoke' if args.smoke else f'run {args.rep}'}:"
          f" {n} cases with {proposer.name}")
    print("(only escalations cost a call)\n")

    def progress(idx: int, total: int, n_rules: int, n_esc: int) -> None:
        if idx % 25 == 0 or idx == total - 1:
            print(f"  case {idx + 1:>5}/{total}   rules={n_rules:<5} "
                  f"calls={n_esc:<5}", end="\r", flush=True)

    res = run_shadow2(corpus, engine, proposer, on_progress=progress)
    print("\n")
    m = res.metrics
    for k in ("n_rules", "escalations", "conflicts", "failed_proposals",
              "rejected_rules", "llm_calls"):
        print(f"  {k:<24}{m.get(k)}")
    print("  (the rows are scored by reuse/score.py, not read here)")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "B",
        "rep": "smoke" if args.smoke else args.rep,
        "rung": 2,
        "model": plan.MODEL,
        "n": n,
        "seed": plan.SEED,
        "prompt_version": plan.PROMPT,
        "system_prompt": proposer.system_prompt,
        "gates": checks.summary(),
        "metrics": m,
        "rules": [r.as_dict() for r in res.rules],
        "edge_log": engine.edge_log,
        "records": [vars(r) for r in res.records],
    }, indent=2, default=str))
    print(f"\n-> {target}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
