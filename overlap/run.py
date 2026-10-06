"""
Stage B of `PLAN_OVERLAP.md` — rung 2's loop under v2e over the 2,000 cases of
seed 17. **The only module of the plan that spends.**

THE ORDER OF EVENTS IS `authorship/run.py`'s, and nothing that costs is built
before the thing that could forbid it has spoken:

  1. `--dry-run` runs `O-g1` to `O-g3`, prints the signature's state, and stops.
     It never builds the client and never needs the key.
  2. The signature (`O-g4`). While `PLAN_OVERLAP.md` carries a blank signature
     line this module exits here, before the checks, the destination, the corpus
     or the client. No flag skips it.
  2b. For `--rep`, the smoke run: a full run refuses unless a smoke record under
     this protocol shows a proposal that parsed and a rule born, and carries
     every field §5.4 asks each call to record.
  2c. The key, for `--smoke` and `--rep`: OpenRouter's key endpoint must accept
     it and must not call it a management key (`reuse.run.key_check`).
  3. `O-g1` to `O-g3`, blocking.
  4. The destination: a paid record is never overwritten
     (`harness/record_guard.py`), and the flag that would is not typed without
     Sergi asking.
  5. The partial file, and the client, and the calls: sequential, hard rule 3.

A RUN THAT DIES KEEPS WHAT IT PAID FOR, as in `authorship/run.py`, whose partial
file, resumption and outage rule are called here and not copied: every answer is
appended as it arrives, the same command serves each stored answer after
checking that the request is byte for byte the one paid for, and **a run of
failed calls stops the run without recording them**.

A RUN LONGER THAN ABOUT HALF AN HOUR OUTLIVES A BACKGROUND COMMAND of the
agent's harness, which ends it at that limit. Run the full runs in Sergi's
terminal, with the key loaded as rule 7 of `CLAUDE.md` says.

    python3 -m overlap.run --dry-run
    .venv/bin/python -m overlap.run --smoke      # 20 cases, before the first run
    .venv/bin/python -m overlap.run --rep 1      # then 2, then 3, one after another
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from authorship import protocol as e
from authorship import run as erun
from reuse.run import key_check
from rung2.engine2 import PriorityEngine, Space
from rung2.proposers2 import neighbourhood

from . import gates, loop, plan
from . import protocol as v

CALL_FIELDS = erun.CALL_FIELDS
Outage, Desync = erun.Outage, erun.Desync


def destination(args: argparse.Namespace) -> Path:
    return plan.SMOKE_PATH if args.smoke else plan.run_path(args.rep)


def tag(args: argparse.Namespace) -> str:
    return "smoke" if args.smoke else f"r{args.rep}"


def protocol_header(run: str, n: int) -> dict[str, Any]:
    """What a partial file must have been written under to be resumed."""
    return {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
            "fingerprint": v.fingerprint(), "reasoning": plan.REASONING,
            "repair_rounds": plan.REPAIR_ROUNDS, "listing_seed": plan.LISTING_SEED,
            "seed": plan.SEED, "n": n, "run": run}


class Resumable(erun.Resumable):
    """`authorship/run.py`'s resumable proposer, asking with v2e's texts."""

    name = f"openrouter2e({plan.MODEL},{plan.PROMPT})"

    def build_base(self, engine, case, undefeated):
        shown, kind = neighbourhood(engine, case, undefeated)
        return shown, kind, v.render_base(shown, kind, engine, case)

    def first(self, case, base_text, idx: int) -> e.Answer:
        return self.answer(idx, 0, v.messages_for(case, base_text))

    def repair(self, case, base_text, previous: e.Answer, message: str,
               idx: int) -> e.Answer:
        return self.answer(idx, 1, v.messages_for(case, base_text, previous, message))


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """Step 2b: the smoke run under this protocol parsed, bore a rule, and
    recorded every field §5.4 asks of a call, `S` beside every `O`."""
    path = path or plan.SMOKE_PATH
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke first"
    rec = json.loads(path.read_text())
    expected = {"plan": str(plan.PLAN), "model": plan.MODEL,
                "prompt_version": plan.PROMPT, "reasoning": plan.REASONING,
                "seed": plan.SEED, "n": plan.SMOKE_N,
                "repair_rounds": plan.REPAIR_ROUNDS, "fingerprint": plan.FINGERPRINT}
    wrong = {k: rec.get(k) for k, x in expected.items() if rec.get(k) != x}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    calls = [c for esc in rec.get("escalations", []) for c in esc.get("calls", [])]
    if (any(not CALL_FIELDS <= set(c) for c in calls) or "edge_channels" not in rec
            or any(("overlapped" in c) != ("same_queue" in c) for c in calls)):
        return False, f"{path} lacks fields §5.4 asks every call to record"
    parsed = sum(1 for c in calls if c["failure"] is None)
    if parsed < 1:
        return False, (f"none of the {len(calls)} calls in {path} parsed: the client "
                       "or the key is not working")
    if rec.get("metrics", {}).get("n_rules", 0) < 1:
        return False, f"{parsed} calls in {path} parsed and no rule was born"
    return True, (f"{path}: {parsed} of {len(calls)} calls parsed, "
                  f"{rec['metrics']['n_rules']} rules born")


def record(args, n: int, checks: gates.Checks, res, engine: PriorityEngine,
           resumed: bool) -> dict[str, Any]:
    return {
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "B",
        "rep": "smoke" if args.smoke else args.rep,
        "rung": 2,
        "model": plan.MODEL,
        "n": n,
        "seed": plan.SEED,
        "prompt_version": plan.PROMPT,
        "reasoning": plan.REASONING,
        "repair_rounds": plan.REPAIR_ROUNDS,
        "listing_seed": plan.LISTING_SEED,
        "fingerprint": v.fingerprint(),
        "system_prompt": v.SYSTEM_PROMPT_V2E,
        "order_paragraph": v.ORDER_PARAGRAPH,
        "repair_template": v.REPAIR_TEMPLATE,
        "labels_from": str(plan.v1_path(plan.BASELINE_REPS[0])),
        "resumed": resumed,
        "gates": checks.summary(),
        "metrics": res.run.metrics,
        "calls": res.calls,
        "rules": [r.as_dict() for r in res.run.rules],
        "edge_log": engine.edge_log,
        "edge_channels": res.edge_channels,
        "records": [vars(r) for r in res.run.records],
        "escalations": [asdict(x) for x in res.escalations],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_OVERLAP.md: rung 2's loop under v2e (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run O-g1 to O-g3 and stop; spends nothing")
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

    plan.refuse_unsigned("overlap/run.py spends")

    if args.rep is not None:
        ok, why = smoke_check()
        if not ok:
            sys.exit(f"\nREFUSED: overlap/run.py --rep {args.rep} before a smoke run "
                     f"that worked — {why}.\n  Nothing was built, spent or written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: overlap/run.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")

    target = or_exit(refuse_overwrite, destination(args),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    n = plan.SMOKE_N if args.smoke else plan.N
    corpus = generate_corpus(n, seed=plan.SEED)
    labels = gates.labels_of(gates.load(plan.v1_path(plan.BASELINE_REPS[0])))[:n]
    partial = plan.partial_path(tag(args))
    rows, resumed = erun.open_partial(partial, protocol_header(tag(args), n))
    proposer = Resumable(v.ProposerV2E(model=plan.MODEL, reasoning=plan.REASONING),
                         partial, rows)
    engine = PriorityEngine(space=Space())

    print(f"\n{plan.PLAN} · stage B · {'smoke' if args.smoke else f'run {args.rep}'}:"
          f" {n} cases with {proposer.name}"
          + (f" · resuming, {len(rows)} answers already paid for" if resumed else ""))
    print("(only escalations cost a call)\n")

    def progress(idx: int, total: int, n_rules: int, n_esc: int) -> None:
        if idx % 25 == 0 or idx == total - 1:
            print(f"  case {idx + 1:>5}/{total}   rules={n_rules:<5} "
                  f"escalations={n_esc:<5} asked={proposer.asked:<5}",
                  end="\r", flush=True)

    try:
        res = loop.run_loop(corpus, labels, engine, proposer, on_progress=progress)
    except (Outage, Desync) as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before it is kept in "
                 f"{partial}; the same command resumes there.\n")
    proposer.flush()
    print("\n")
    m = res.run.metrics
    for k in ("n_rules", "escalations", "conflicts", "failed_proposals",
              "rejected_rules"):
        print(f"  {k:<24}{m.get(k)}")
    print(f"  {'calls':<24}{res.calls}")
    print("  (the rows are scored by overlap/score.py, not read here)")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args, n, checks, res, engine, resumed),
                                 indent=2, default=str))
    partial.unlink()
    print(f"\n-> {target}\n  {describe()}")
    if args.smoke:
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the full runs may start' if ok else 'FAIL'}"
              f" · {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
