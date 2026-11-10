"""
Stage B of `PLAN_HALVES.md`: the asks. **The only module of the plan that
spends.** On the proposer's path: no row carries a label, and nothing here
imports the policy (rule B).

It asks the four arms' prompts, every call pinned to DeepInfra's fp8 endpoint
(§2.6 of the plan), through the loop's own first call (§2.7):

  - **the request** is `placement.protocol.Asker`'s, called: `PLAN_REASONED_LOOP.md`'s
    request, with the model, temperature 0, reasoning `{"effort": "high"}`, 16,000
    tokens and `response_format` on the first attempt, and `placement.plan`'s pin;
  - **the asker** is `reasoned_loop.protocol.Live` over it, called: `PLAN_FIRST_MATCH.md`'s
    retry by cause, a failed call retried with the same messages after a wait and
    a failed parse with v1's retry message, and a call refused for the rate waited
    out through `plan.RATE_LIMIT_WAIT` and then an outage.

This module makes no call of its own. The asker carries `harness.call_record`'s
recorder, and every row keeps what each attempt said about itself.

AN ANSWER IS VALID (§0) when the call came back, after its retries, with a
payload that parses and an `action` among the eight queues, from the pinned
provider. A failed call and an answer from another provider are recorded,
counted and never classed.

WHAT THE MODEL WRITES IS RECORDED AND NEVER EXECUTED. The row keeps the whole
payload, its keys in the order the model wrote them, and the reasoning. No rule
is installed and no edge is tried.

THE ORDER OF EVENTS IS THE POINT (§8 of the plan), and nothing that costs is
built before the thing that could forbid it has spoken:

  1. `--dry-run` runs `HV-g1` to `HV-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`HV-g4`). While `PLAN_HALVES.md` carries a blank signature
     line this module exits here, before the checks, the destination or a
     client. No flag skips it.
  3. The turn: a pass after the smoke record, whose every arm holds a valid answer
     and whose every attempt that reached the model was served by the pinned
     provider, reasoned and ended `stop`; pass 2 after pass 1; the rarest queue's
     session after pass 2.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`, called
     and not copied. A management key answers 200 there and cannot call a model.
  5. `HV-g1` to `HV-g3`, blocking. Then Stage A's record must hold the same
     sessions and prompt digests the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: one at a time (hard rule 3).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR, through `PLAN_FIDELITY.md`'s partial
file, called through `first_match.ask`: every row is appended as it arrives,
whole, with its own seconds, and the same command resumes there. A run of
`plan.MAX_CONSECUTIVE_FAILURES` failed asks stops the session without recording
them, and so does a call refused for the rate through every wait: an outage is
not answers. **A pass outlives a background command of the agent's harness**, so
the sessions run in Sergi's terminal or under a supervisor detached from the
harness (§2.5).

    python3 -m halves.ask --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session smoke
    PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session pass1
    PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session pass2
    PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session oncall
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from authorship import run as erun
from first_match import ask as fm_ask
from placement import protocol as pl_protocol
from reasoned_loop import protocol as p
from reuse.run import key_check
from rung2.proposers2 import ProposalError

from . import gates, plan, population, prompts

# `PLAN_FIDELITY.md`'s, through `PLAN_FIRST_MATCH.md`'s, called: the partial file,
# the breaker, the hour, and what a response says about itself.
Outage = fm_ask.Outage
open_partial = fm_ask.open_partial
now = fm_ask.now
served_by = fm_ask.served_by
reasoned = fm_ask.reasoned
STOPS = (fm_ask.Outage, erun.Outage)   # five failures in a row, or the rate through every wait

# What comes before each session (§8).
BEFORE = {"pass1": "smoke", "pass2": "pass1", "oncall": "pass2"}


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
            "temperature": plan.TEMPERATURE, "settings": plan.settings(),
            "provider": plan.PROVIDER, "call_retry_wait": list(plan.CALL_RETRY_WAIT),
            "rate_limit_wait": list(plan.RATE_LIMIT_WAIT), "seed": plan.SEED, "n": plan.N,
            "texts_sha16": prompts.digests(), "fingerprint": prompts.fingerprint()}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.sample_path()).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Step 3: the turn
# ---------------------------------------------------------------------------

def under_protocol(rec: dict[str, Any]) -> dict[str, Any]:
    return {k: rec.get(k) for k, v in json.loads(json.dumps(protocol())).items()
            if rec.get(k) != v}


def reached_the_model(attempt: dict[str, Any]) -> bool:
    return attempt.get("error") != plan.RATE_LIMITED


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = under_protocol(rec)
    if wrong:
        return False, f"{path} was not produced under this protocol: {sorted(wrong)}"
    rows = rec.get("rows", [])
    missing = sorted(set(prompts.ARMS) - {r["arm"] for r in rows if r.get("valid")})
    if missing:
        return False, f"{path} holds no valid answer from {missing}"
    attempts = [a for r in rows for a in r.get("call_attempts") or []
                if reached_the_model(a)]
    elsewhere = sorted({a.get("provider") or "none" for a in attempts} - {plan.PROVIDER_NAME})
    if elsewhere:
        return False, f"{path} holds attempts served by {elsewhere}: the pin did not hold"
    if not all(reasoned(a) for a in attempts):
        return False, f"{path} holds an attempt that did not reason, and every one must"
    ended = sorted({a.get("finish_reason") for a in attempts} - {"stop"})
    if ended:
        return False, f"{path} holds attempts that ended {ended}: the budget must fit"
    return True, (f"{path}: a valid answer from each arm, every attempt that reached "
                  f"the model served by {plan.PROVIDER_NAME}, reasoned and ended `stop`")


def turn_check(session: str) -> tuple[bool, str]:
    """The smoke run first, then pass 1, pass 2 and the rarest queue's session."""
    if session == "smoke":
        return True, "the smoke run comes first"
    ok, why = smoke_check()
    if not ok:
        return False, why
    previous = BEFORE[session]
    path = plan.ask_path(previous)
    if previous != "smoke":
        if not path.exists():
            return False, f"no record of {previous} at {path}; {session} comes after it"
        wrong = under_protocol(json.loads(path.read_text()))
        if wrong:
            return False, f"{path} was not produced under this protocol: {sorted(wrong)}"
    return True, f"{why}; {session} comes after {previous}"


# ---------------------------------------------------------------------------
# Step 5: Stage A's record is the design the checks rebuilt
# ---------------------------------------------------------------------------

def sample_matches(design: population.Design, path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run halves.sample first"
    rec = json.loads(path.read_text()).get("design", {})
    summary = json.loads(json.dumps(design.summary()))
    for key in ("tickets", "sessions", "asks"):
        if rec.get(key) != summary[key]:
            return False, f"{path} holds other {key} than the ones rebuilt now"
    return True, f"{path}: the same tickets, asks, digests and sessions"


# ---------------------------------------------------------------------------
# Step 7: the client, and the calls
# ---------------------------------------------------------------------------

def build_live(sleep=time.sleep) -> p.Live:
    """The loop's first call: `placement.protocol.Asker` with DeepInfra's pin,
    behind `reasoned_loop.protocol.Live`. Built only after steps 2 to 6."""
    return p.Live(pl_protocol.Asker(pin=plan.PROVIDER, sleep=sleep))


def row_of(session: str, position: int, a: prompts.Ask, got: Any, failure: str | None,
           attempts: list[dict], seconds: float) -> dict[str, Any]:
    payload = getattr(got, "payload", None)
    action = getattr(got, "action", None)
    by = served_by(attempts)
    return {"session": session, "position": position, "id": a.id, "prompt": a.prompt,
            "arm": a.arm, "ticket": a.ticket, "rep": a.rep, "digest": a.digest,
            "action": action, "served_by": by,
            "valid": (failure is None and isinstance(payload, dict) and action in ACTIONS
                      and by == plan.PROVIDER_NAME),
            "payload": payload, "keys": getattr(got, "keys", None),
            "reasoning": getattr(got, "reasoning", None),
            "finish_reason": getattr(got, "finish_reason", None),
            "failure": failure, "attempts": len(attempts),
            "retries": getattr(got, "retries", None), "call_attempts": attempts,
            "seconds": round(seconds, 2), "asked_at": now()}


def ask(session: str, design: population.Design, live: Any, partial: Path, header: dict,
        clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {r["id"] for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    order = design.sessions[session]

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for position, aid in enumerate(order):
            if aid in asked:
                continue
            a = design.asks[aid]
            t0 = clock()
            try:
                got = live.ask(a.messages())
                failure, attempts = None, list(got.call_attempts or [])
            except STOPS:
                raise
            except ProposalError as exc:
                got = exc
                failure = str(exc)[:300]
                attempts = list(getattr(exc, "call_attempts", []) or [])
            row = row_of(session, position, a, None if failure else got, failure, attempts,
                         clock() - t0)
            if failure is not None:
                row["finish_reason"] = getattr(got, "finish_reason", None)
                pending.append(row)
                if len(pending) >= plan.MAX_CONSECUTIVE_FAILURES:
                    raise Outage(f"{len(pending)} asks in a row failed, the last with: "
                                 f"{failure}")
                continue
            for r in pending:
                keep(f, r)
            pending = []
            keep(f, row)
            print(f"  {len(rows):>5}/{len(order)}  {session}  {aid:<10} "
                  f"{row['action'] if row['valid'] else 'INVALID'}", end="\r", flush=True)
        for r in pending:
            keep(f, r)
    print()
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def first_kept(rows: list[dict]) -> str | None:
    """The hour of the first answer the session kept, so that a resumed
    session's span is taken from its first launch."""
    hours = sorted(r["asked_at"] for r in rows if r.get("asked_at"))
    return hours[0] if hours else None


def record(session: str, rows: list[dict], resumed_at: list[str], started: str,
           checks: gates.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "system_prompt": prompts.SYSTEM_PROMPT,
        "paragraphs": dict(prompts.PARAGRAPHS),
        "sample_record": str(plan.sample_path()),
        "sample_sha256": digest,
        "gates": checks.summary(),
        "started_at": started,
        "first_kept": first_kept(rows),
        "resumed_at": resumed_at,
        "finished_at": now(),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage B of PLAN_HALVES.md: the asks (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run HV-g1 to HV-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.SESSIONS,
                       help="one session of §8, in its turn")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"halves/ask.py spends (session {args.session})")

    ok, why = turn_check(args.session)
    if not ok:
        sys.exit(f"\nREFUSED: session {args.session} out of its turn — {why}.\n"
                 "  Nothing was built, spent or written.\n")
    print(f"turn check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: halves/ask.py — {why}.\n  Nothing was built, spent or "
                 "written.\n")
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

    live = build_live()
    digest = sample_sha256()
    header = {"protocol": json.loads(json.dumps(protocol())), "session": args.session,
              "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session}, "
          f"{len(checks.design.sessions[args.session])} asks\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, live,
                               plan.partial_path(args.session), header)
    except STOPS as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before it is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes there "
                 "once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, rows, resumed_at, started, checks,
                                        digest), indent=2, default=str))
    plan.partial_path(args.session).unlink()
    valid = sum(1 for r in rows if r["valid"])
    elsewhere = sum(1 for r in rows if r["served_by"] not in (None, plan.PROVIDER_NAME))
    print(f"\n  answers {len(rows)}, valid {valid}, failed "
          f"{sum(1 for r in rows if r['failure'])}, served elsewhere {elsewhere}")
    print(f"\n-> {target}\n  {describe()}")
    if args.session == "smoke":
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the passes may start' if ok else 'FAIL'} · {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
