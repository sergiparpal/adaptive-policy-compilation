"""
Stage B2 of `PLAN_MANUAL.md`: shape L, the loop with the manual in its prompt.
**It spends.**

The loop is `reuse/run.py`'s, called and not copied (rule A): a fresh
`PriorityEngine(space=Space())`, `OpenRouterProposer2(model, prompt_version="v1",
reasoning=REASONING)` and `run_shadow2`, over the 2,000 cases of seed 17. **One
thing changes**: the proposer's system prompt is v1 with the level's manual
inserted (`manual/prompts.py`). At level 0 it is v1's to the byte, so `L_0` is
`PLAN_REUSE.md`'s protocol asked again. The user message, the request and the
engine are rung 2's. The record keeps `reuse/run.py`'s layout, plus the level
and the texts' digests, so that the closed threads' readers read it.

THE ORDER OF EVENTS IS THE POINT (§9 of the plan):

  1. `--dry-run` runs `G-g1` to `G-g3` and stops. It never builds the client.
  2. The signature (`G-g4`). No flag skips it.
  3. For a run: the smoke record, under this protocol, with a proposal that
     parsed and a rule born (`reuse.run.smoke_check`'s test); the compile
     session's record; and every run before it in §2.5's order. A run out of
     its turn is refused.
  4. The key, by `reuse.run.key_check`.
  5. `G-g1` to `G-g3`, blocking.
  6. The destination: a paid record is never overwritten.
  7. The client, and the calls — sequential, hard rule 3.

**A run takes from minutes to half an hour**, and the twelve take hours. A
command longer than about half an hour outlives a background command of the
agent's harness, so the runs belong in Sergi's terminal, one after another.

    python3 -m manual.run --dry-run
    .venv/bin/python -m manual.run --smoke
    .venv/bin/python -m manual.run --level 0 --rep 1    # §2.5's order; the module says what is next
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from reuse.run import key_check
from rung2.engine2 import PriorityEngine, Space
from rung2.proposers2 import OpenRouterProposer2
from rung2.shadow2 import run_shadow2

from . import gates, plan, prompts


def build_proposer(level: int) -> OpenRouterProposer2:
    """Rung 2's proposer, as `reuse/run.py` builds it, with the level's system
    prompt. Nothing else of it is touched."""
    p = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                            reasoning=plan.REASONING)
    p.system_prompt = prompts.loop_system_prompt(level)
    p.name = f"openrouter2({plan.MODEL},{plan.PROMPT}+manual{level})"
    return p


def protocol(level: int, n: int) -> dict[str, Any]:
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "shape": "L", "level": level, "model": plan.MODEL,
        "prompt_version": plan.PROMPT, "reasoning": plan.REASONING, "seed": plan.SEED,
        "n": n, "texts_sha256": dict(plan.DIGESTS),
        "prompt_sha256": prompts.prompt_digests()["loop"][level]}))


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """§9: the smoke run checks the client, the key, the longest prompt and the
    shape of the record. `reuse.run.smoke_check`'s test, on this protocol."""
    path = path or plan.loop_smoke_path()
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke first"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol(plan.LOOP_SMOKE_LEVEL, plan.SMOKE_N).items()
             if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {sorted(wrong)}"
    m = rec.get("metrics", {})
    parsed = m.get("escalations", 0) - m.get("failed_proposals", 0)
    if parsed < 1:
        return False, f"none of the proposals in {path} parsed"
    if m.get("n_rules", 0) < 1:
        return False, f"{parsed} proposals in {path} parsed and no rule was born"
    return True, f"{path}: {parsed} proposals parsed, {m['n_rules']} rules born"


def turn_check(level: int, rep: int) -> tuple[bool, str]:
    """§2.5: the compile session first, then the twelve runs in their order."""
    if not plan.compile_path("session").exists():
        return False, "the compile session (manual.ask --session session) comes first"
    for r, lv in plan.loop_schedule():
        if (r, lv) == (rep, level):
            return True, f"run L{level} r{rep} is next in §2.5's order"
        if not plan.loop_path(lv, r).exists():
            return False, f"run L{lv} r{r} comes before L{level} r{rep} in §2.5's order"
    return False, f"no run L{level} r{rep} in the schedule"


def next_run() -> tuple[int, int] | None:
    for r, lv in plan.loop_schedule():
        if not plan.loop_path(lv, r).exists():
            return lv, r
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B2 of PLAN_MANUAL.md: the loop with the manual (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run G-g1 to G-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases at level {plan.LOOP_SMOKE_LEVEL}, first")
    which.add_argument("--level", type=int, choices=plan.LEVELS,
                       help="the level of one run; --rep says which")
    ap.add_argument("--rep", type=int, choices=range(1, plan.REPS + 1))
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        nxt = next_run()
        print(f"\nnext run in §2.5's order: {f'--level {nxt[0]} --rep {nxt[1]}' if nxt else 'none'}")
        print("dry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1
    if args.level is not None and args.rep is None:
        ap.error("--level needs --rep")

    what = "smoke" if args.smoke else f"L{args.level} r{args.rep}"
    plan.refuse_unsigned(f"manual/run.py spends (run {what})")

    if not args.smoke:
        for check in (smoke_check, lambda: turn_check(args.level, args.rep)):
            ok, why = check()
            if not ok:
                sys.exit(f"\nREFUSED: run {what} — {why}.\n  Nothing was built, spent "
                         "or written.\n")
            print(f"check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: manual/run.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")

    level = plan.LOOP_SMOKE_LEVEL if args.smoke else args.level
    n = plan.SMOKE_N if args.smoke else plan.N
    target = or_exit(refuse_overwrite,
                     plan.loop_smoke_path() if args.smoke else plan.loop_path(level, args.rep),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    corpus = generate_corpus(n, seed=plan.SEED)
    engine = PriorityEngine(space=Space())
    proposer = build_proposer(level)
    started = environment()["recorded_at"]
    print(f"\n{plan.PLAN} · stage B2 · run {what}: {n} cases with {proposer.name}")
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
    print("  (the rows are scored by manual/score.py, not read here)")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        "_env": environment(),
        **protocol(level, n),
        "stage": "B2",
        "rep": "smoke" if args.smoke else args.rep,
        "rung": 2,
        "started_at": started,
        "system_prompt": proposer.system_prompt,
        "gates": checks.summary(),
        "metrics": m,
        "rules": [r.as_dict() for r in res.rules],
        "edge_log": engine.edge_log,
        "records": [vars(r) for r in res.records],
        "calls": res.calls,
    }, indent=2, default=str))
    print(f"\n-> {target}\n  {describe()}")
    if args.smoke:
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the runs may start' if ok else 'FAIL'} · {why}")
        return 0 if ok else 1
    nxt = next_run()
    print(f"\nnext run in §2.5's order: {f'--level {nxt[0]} --rep {nxt[1]}' if nxt else 'none: Stage B is complete'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
