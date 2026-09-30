"""
Stage B of `PLAN_REUSE.md` — rung 2's loop over the 2,000 cases of seed 17,
prompt v1. **The only module of the plan that spends.**

The loop is rung 2's, called and not copied (rule A): a fresh
`PriorityEngine(space=Space())`, `OpenRouterProposer2(model, prompt_version="v1")`
and `run_shadow2`, as the four v1 records of 2026-08-07 were produced. Only the
horizon changes, the number of repetitions, and — by §1's amendment of
2026-09-30, signed separately — one client parameter: every call carries
`reasoning: {"effort": "none"}`, because the hosted model now reasons by default
and its reasoning spent the 1,200-token budget on a third of the third smoke
run's answers. The record keeps `rung2/run2.py`'s layout plus that setting, so
that Stage C reads the eight old records and these with the same functions.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken:

  1. `--dry-run` runs `U-g1` to `U-g3`, prints the signature's state, and stops.
     It never builds the client and never needs the key.
  2. The signature (`U-g4`). While `PLAN_REUSE.md` carries a blank signature
     line this module exits here — before the checks, the destination, the
     corpus or the client. No flag skips it.
  2b. For `--rep`, the smoke run (§8). A full run refuses unless a smoke record
     exists under this plan's protocol and shows at least one proposal that
     parsed and one rule born. Added 2026-09-30, after the first smoke run met
     a key OpenRouter rejected on all 20 calls and still wrote a record: the
     loop counts a failed proposal and carries on, so a full run with that key
     would have spent hours on a record with no model output in it.
  2c. The key, for `--smoke` and `--rep`: OpenRouter's key endpoint, free, must
     accept it and must not call it a management key. Added the same day, after
     the second smoke run met a management key — which that endpoint accepts,
     and which reads the account's credits and cannot call a model. The smoke
     run took twelve minutes to fail on it; this takes a second.
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
import os
import sys
import urllib.error
import urllib.request
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


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """§8: the smoke run checks the client, the key and the shape of the record.
    This is that check made mechanical — step 2b of the module docstring."""
    path = path or plan.SMOKE_PATH
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke first"
    rec = json.loads(path.read_text())
    expected = {"plan": str(plan.PLAN), "model": plan.MODEL,
                "prompt_version": plan.PROMPT, "reasoning": plan.REASONING,
                "seed": plan.SEED, "n": plan.SMOKE_N}
    wrong = {k: rec.get(k) for k, v in expected.items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    m = rec.get("metrics", {})
    escalations = m.get("escalations", 0)
    parsed = escalations - m.get("failed_proposals", 0)
    if parsed < 1:
        return False, (f"none of the {escalations} proposals in {path} parsed: "
                       "the client or the key is not working")
    if m.get("n_rules", 0) < 1:
        return False, f"{parsed} proposals in {path} parsed and no rule was born"
    return True, (f"{path}: {parsed} of {escalations} proposals parsed, "
                  f"{m['n_rules']} rules born")


KEY_INFO_URL = "https://openrouter.ai/api/v1/key"


def fetch_key_info(key: str) -> tuple[int, dict]:
    """GET OpenRouter's key endpoint. Free: it reads, and calls no model."""
    request = urllib.request.Request(KEY_INFO_URL,
                                     headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except ValueError:
            return e.code, {}


def key_check(fetch=None) -> tuple[bool, str]:
    """Step 2c of the module docstring. Nothing it prints or returns carries the
    key or its label."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return False, "OPENROUTER_API_KEY is not in the environment (hard rule 7)"
    try:
        status, body = (fetch or fetch_key_info)(key)
    except Exception as exc:  # noqa: BLE001 — the network, not the key
        return False, (f"OpenRouter's key endpoint could not be reached "
                       f"({type(exc).__name__})")
    if status != 200:
        return False, f"OpenRouter does not accept the key: HTTP {status}"
    data = body.get("data") or {}
    if data.get("is_management_key") or data.get("is_provisioning_key"):
        return False, ("the key is a management key: it reads the key's metadata "
                       "and the account's credits, and cannot call a model")
    return True, "an API key OpenRouter accepts, and not a management key"


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

    if args.rep is not None:
        ok, why = smoke_check()
        if not ok:
            sys.exit(f"\nREFUSED: reuse/run.py --rep {args.rep} before a smoke run "
                     f"that worked — {why}.\n  Nothing was built, spent or "
                     "written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: reuse/run.py — {why}.\n  Nothing was built, spent "
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
    engine = PriorityEngine(space=Space())
    proposer = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                   reasoning=plan.REASONING)

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
        "reasoning": plan.REASONING,
        "system_prompt": proposer.system_prompt,
        "gates": checks.summary(),
        "metrics": m,
        "rules": [r.as_dict() for r in res.rules],
        "edge_log": engine.edge_log,
        "records": [vars(r) for r in res.records],
    }, indent=2, default=str))
    print(f"\n-> {target}\n  {describe()}")
    if args.smoke:
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the full runs may start' if ok else 'FAIL'}"
              f" · {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
