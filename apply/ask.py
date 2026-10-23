"""
Stage B of `PLAN_APPLY.md`: the calls. **The only module of the plan that
spends.**

It asks the model the prompts `apply/prompts.py` rebuilds: each escalation's own
prompt, screen and all, and each ticket alone under its level's system prompt.
The client at each level is the proposer `manual/run.py` builds for it,
`manual.run.build_proposer(level)`: rung 2's `OpenRouterProposer2` with v1,
reasoning off, and the level's system prompt. Its `propose` is called as the
loop called it: temperature 0, 1,200 tokens, `response_format` on the first
attempt, two retries (§1). What the model writes beyond its `action` is recorded
in full and never executed (rule E).

EACH ROW KEEPS WHAT THE CALL SAID ABOUT ITSELF. The proposer's client carries
`harness.call_record`'s recorder, which changes no request: its `take()` before
an ask clears it, and after the ask the row keeps every attempt's provider,
finish reasons and tokens as `call_attempts`.

NO ROW CARRIES A LABEL (rule B). A row says what was asked and what came back.
Stage C joins `truth` and the loop's answer from the loop records. The blocking
checks this module runs before spending read the records offline, and send
nothing.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `X-g1` to `X-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`X-g4`). While `PLAN_APPLY.md` carries a blank signature
     line this module exits here, before the checks, the destination or a
     client. No flag skips it.
  3. What comes before the session: for a pass, the smoke record under this
     protocol with a valid answer from each arm; for pass 2, pass 1's record.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `X-g1` to `X-g3`, blocking. Then Stage A's record must hold the same
     sessions and prompt digests the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The clients, and the calls: sequential (hard rule 3).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR (§5.12), with `PLAN_FIDELITY.md`'s
machinery called: `open_partial` resumes from the git-ignored partial file, and
a run of `plan.MAX_CONSECUTIVE_FAILURES` failed calls stops the session without
recording them, because an outage is not answers. **A pass outlives a background
command of the agent's harness**, so the passes run in Sergi's terminal.

    python3 -m apply.ask --dry-run
    .venv/bin/python -m apply.ask --session smoke
    .venv/bin/python -m apply.ask --session pass1
    .venv/bin/python -m apply.ask --session pass2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable

from harness.call_record import CallRecorder
from harness.domain import ACTIONS
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from fidelity import ask as fidelity_ask
from manual.run import build_proposer
from reuse.run import key_check
from rung2.proposers2 import ProposalError

from . import gates, plan, population, prompts

# What every pass asks, by arm. A smoke record must hold a valid answer of each.
ARMS = set(prompts.ARMS)

# What `OpenRouterProposer2.propose` sends, written into every record so that it
# says what was asked. `tests/test_apply.py` checks these against the request
# the proposer actually builds, so they cannot drift from it in silence.
TEMPERATURE = fidelity_ask.TEMPERATURE
MAX_TOKENS = fidelity_ask.MAX_TOKENS

# `PLAN_FIDELITY.md`'s, called: the partial file and the breaker.
Outage = fidelity_ask.Outage
open_partial = fidelity_ask.open_partial
now = fidelity_ask.now


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL,
            "prompt_version": plan.PROMPT, "reasoning": plan.REASONING,
            "seed": plan.SEED, "n": plan.N}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.sample_path()).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Step 3: what comes before the session
# ---------------------------------------------------------------------------

def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol().items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    valid = {r["arm"] for r in rec.get("rows", []) if r.get("valid")}
    missing = sorted(ARMS - valid)
    if missing:
        return False, f"{path} holds no valid answer from {missing}"
    return True, f"{path}: a valid answer from each arm"


def previous_check(session: str) -> tuple[bool, str]:
    """A pass after the smoke run, and pass 2 after pass 1 (§8)."""
    ok, why = smoke_check()
    if not ok or session != "pass2":
        return ok, why
    path = plan.ask_path("pass1")
    if not path.exists():
        return False, f"no record of pass 1 at {path}; pass 2 comes after it"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol().items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    return True, f"{why}; {path} holds pass 1"


# ---------------------------------------------------------------------------
# Step 5: Stage A's record is the design the checks rebuilt
# ---------------------------------------------------------------------------

def sample_matches(design: population.Design, path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run apply.sample first"
    rec = json.loads(path.read_text()).get("design", {})
    summary = json.loads(json.dumps(design.summary()))
    if rec.get("sessions") != summary["sessions"]:
        return False, f"{path} holds other sessions than the ones rebuilt now"
    stale = [i for i, a in summary["asks"].items()
             if rec.get("asks", {}).get(i, {}).get("digest") != a["digest"]]
    if stale or set(rec.get("asks", {})) != set(summary["asks"]):
        return False, f"{len(stale)} prompts rebuilt now differ from {path}'s"
    if rec.get("decisions") != summary["decisions"]:
        return False, f"{path} holds other decisions than the ones rebuilt now"
    return True, f"{path}: the same sessions, prompts and decisions"


# ---------------------------------------------------------------------------
# Step 7: the clients, the calls, and the partial record
# ---------------------------------------------------------------------------

class Proposers:
    """One proposer per level, built when its level is first asked. The builder
    is `manual.run.build_proposer`, looked up when it is first needed, so that a
    test can stand the SDK double behind it."""

    def __init__(self, build: Callable[[int], Any] | None = None):
        self._build = build
        self.by_level: dict[int, Any] = {}

    def get(self, level: int):
        if level not in self.by_level:
            self.by_level[level] = (self._build or build_proposer)(level)
        return self.by_level[level]


def ask(session: str, design: population.Design, proposers: Proposers, partial: Path,
        header: dict, clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {r["id"] for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    order = design.sessions[session]
    pass_no = plan.pass_of(session)

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for position, aid in enumerate(order):
            if aid in asked:
                continue
            a = design.asks[aid]
            proposer = proposers.get(a.level)
            calls = getattr(proposer, "calls", None)
            if not isinstance(calls, CallRecorder):
                calls = None
            if calls is not None:
                calls.take()
            t0 = clock()
            try:
                action, payload = proposer.propose(a.case, a.base_text)
                failure = None
            except ProposalError as exc:
                action, payload, failure = None, None, str(exc)[:300]
            attempts = calls.take() if calls is not None else []
            row = {"session": session, "pass": pass_no, "position": position,
                   "id": aid, "arm": a.arm, "level": a.level, "digest": a.digest,
                   "shown_ids": list(a.shown_ids), "action": action,
                   "valid": action in ACTIONS, "payload": payload,
                   "failure": failure, "attempts": len(attempts),
                   "call_attempts": attempts,
                   "seconds": round(clock() - t0, 2), "asked_at": now()}
            if failure is not None:
                pending.append(row)
                if len(pending) >= plan.MAX_CONSECUTIVE_FAILURES:
                    raise Outage(f"{len(pending)} calls in a row failed, the last "
                                 f"with: {failure}")
                continue
            for r in pending:
                keep(f, r)
            pending = []
            keep(f, row)
            print(f"  {len(rows):>5}/{len(order)}  {session}  {aid:<16} "
                  f"{action if row['valid'] else 'INVALID'}", end="\r", flush=True)
        for r in pending:
            keep(f, r)
    print()
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def record(session: str, proposers: Proposers, rows: list[dict], resumed_at: list[str],
           started: str, checks: gates.Checks, digest: str) -> dict[str, Any]:
    built = sorted(proposers.by_level)
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "pass": plan.pass_of(session),
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "max_retries": {lv: proposers.by_level[lv].max_retries for lv in built},
        "system_prompts_sha256": {lv: hashlib.sha256(
            proposers.by_level[lv].system_prompt.encode()).hexdigest() for lv in built},
        "sample_record": str(plan.sample_path()),
        "sample_sha256": digest,
        "gates": checks.summary(),
        "started_at": started,
        "resumed_at": resumed_at,
        "finished_at": now(),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_APPLY.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run X-g1 to X-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.SESSIONS,
                       help="one session of §8, in its order")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"apply/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = previous_check(args.session)
        if not ok:
            sys.exit(f"\nREFUSED: session {args.session} out of its turn — {why}.\n"
                     "  Nothing was built, spent or written.\n")
        print(f"turn check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: apply/ask.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    ok, why = sample_matches(checks.design)
    if not ok:
        sys.exit(f"\nREFUSED: {why}. Nothing was spent.\n")
    print(f"Stage A: {why}")

    target = or_exit(refuse_overwrite, plan.ask_path(args.session),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    proposers = Proposers()
    digest = sample_sha256()
    header = {"protocol": protocol(), "session": args.session, "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session}, "
          f"{len(checks.design.sessions[args.session])} asks\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, proposers,
                               plan.partial_path(args.session), header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, proposers, rows, resumed_at,
                                        started, checks, digest),
                                 indent=2, default=str))
    plan.partial_path(args.session).unlink()
    valid = sum(1 for r in rows if r["valid"])
    print(f"\n  answers {len(rows)}, valid {valid}, failed "
          f"{sum(1 for r in rows if r['failure'])}")
    print(f"\n-> {target}\n  {describe()}")
    if args.session == "smoke":
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the passes may start' if ok else 'FAIL'} · {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
