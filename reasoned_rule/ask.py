"""
Stage B of `PLAN_REASONED_RULE.md`: the calls. **The only module of the plan
that spends.**

It asks the model the four arms' prompts, every call pinned to one provider
(§2.4 of the plan), through one `Asker`:

  t, q  the rule and plain arms: the model, temperature 0, 1,200 tokens,
     reasoning off and `response_format` on the first attempt, as
     `PLAN_QUEUE_ALONE.md`'s rule and plain arms were asked;
  w, r  the reasoning rule and reasoning arms: the same request with reasoning
     `{"effort": "high"}` and 16,000 tokens, as `PLAN_FIRST_MATCH.md`'s
     reasoning arm was asked (`plan.settings`).

THE ASKER IS `PLAN_FIRST_MATCH.md`'s, CALLED AND NOT COPIED (rule A). `Asker`
subclasses `first_match.ask.Asker` and replaces its `request` alone, so that each
arm's request carries this plan's settings. Its loop is that plan's, and so is
its retry (rule H):
- **a failed call**, one that raised before any answer came back, is retried
  with the same messages, after `plan.CALL_RETRY_WAIT`'s seconds;
- **a failed parse**, an answer that came back and holds no JSON object, is
  retried with v1's retry message, as v1 does;
- **every row keeps the cause of each retry**, in `retries`.

The request is sent by that asker, which is the call site, and it carries
`harness.call_record`'s recorder. This module makes no call of its own.

EACH ROW KEEPS WHAT THE CALL SAID ABOUT ITSELF. The recorder changes no request.
Its `take()` before an ask clears it, and after the ask the row keeps every
attempt's provider, finish reasons and tokens as `call_attempts`. **The provider
that served an answer is its last attempt's**, kept as `served_by`. An answer is
valid only when its `action` is one of the eight queues and `served_by` is
`plan.PROVIDER_NAME` (rule G): an answer from another provider is recorded,
counted and never read.

WHAT THE MODEL WRITES BEYOND ITS `action` IS RECORDED AND NEVER EXECUTED (rule
E). The row keeps the whole payload, its keys in the order the model wrote them,
the rule arms' rules, edges and notes among it, and the response's `reasoning`
when it carries one. No rule is installed and no edge is tried.

NO ROW CARRIES A LABEL (rule B). A row says what was asked and what came back.
Stage C joins the truth from the loop records. The blocking checks this module
runs before spending read labels offline, and send nothing.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `RR-g1` to `RR-g3` and stops. It never builds a client
     and never needs the key.
  2. The signature (`RR-g4`). While `PLAN_REASONED_RULE.md` carries a blank
     signature line this module exits here, before the checks, the destination
     or a client. No flag skips it.
  3. What comes before the session: for a pass, the smoke record under this
     protocol, with a valid answer from each arm, every attempt served by the
     pinned provider, every attempt of both reasoning arms reasoned and ended
     `stop`, and no attempt of the other two reasoned; for pass 2, pass 1's
     record.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `RR-g1` to `RR-g3`, blocking. Then Stage A's record must hold the same
     sessions and prompt digests the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR (§5.16), with `PLAN_FIDELITY.md`'s
machinery called through `first_match.ask`: `open_partial` resumes from the
git-ignored partial file, and a run of `plan.MAX_CONSECUTIVE_FAILURES` failed
asks stops the session without recording them, because an outage is not
answers. **A pass outlives a background command of the agent's harness**, so
the passes run in Sergi's terminal.

    python3 -m reasoned_rule.ask --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m reasoned_rule.ask --session smoke
    PYTHONHASHSEED=0 .venv/bin/python -m reasoned_rule.ask --session pass1
    PYTHONHASHSEED=0 .venv/bin/python -m reasoned_rule.ask --session pass2
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

from first_match import ask as fm_ask
from reuse.run import key_check
from rung2.proposers2 import ProposalError

from . import gates, plan, population, prompts

# `PLAN_FIRST_MATCH.md`'s, called: the partial file, the breaker, the causes of a
# retry and what a response says about itself.
Outage = fm_ask.Outage
open_partial = fm_ask.open_partial
now = fm_ask.now
AskFailed = fm_ask.AskFailed
CALL, PARSE = fm_ask.CALL, fm_ask.PARSE
served_by = fm_ask.served_by
reasoning_of = fm_ask.reasoning_of
reasoned = fm_ask.reasoned


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
            "settings": {arm: plan.settings(arm) for arm in prompts.ARMS},
            "provider": plan.PROVIDER, "call_retry_wait": list(plan.CALL_RETRY_WAIT),
            "seed": plan.SEED, "n": plan.N}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.sample_path()).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Step 3: what comes before the session
# ---------------------------------------------------------------------------

def under_protocol(rec: dict[str, Any]) -> dict[str, Any]:
    return {k: rec.get(k) for k, v in json.loads(json.dumps(protocol())).items()
            if rec.get(k) != v}


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = under_protocol(rec)
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    rows = rec.get("rows", [])
    valid = {r["arm"] for r in rows if r.get("valid")}
    missing = sorted(set(prompts.ARMS) - valid)
    if missing:
        return False, f"{path} holds no valid answer from {missing}"
    elsewhere = sorted({a.get("provider") or "none" for r in rows
                        for a in r.get("call_attempts") or []} - {plan.PROVIDER_NAME})
    if elsewhere:
        return False, (f"{path} holds attempts served by {elsewhere}, not only by "
                       f"{plan.PROVIDER_NAME}: the pin did not hold")
    for r in rows:
        attempts = r.get("call_attempts") or []
        if r["arm"] in plan.REASONING_ARMS:
            if not attempts or not all(reasoned(a) or r.get("reasoning") for a in attempts):
                return False, f"{r['id']} did not reason, and the reasoning arms must"
            if any(a.get("finish_reason") != "stop" for a in attempts):
                return False, (f"{r['id']} ended {[a.get('finish_reason') for a in attempts]}: "
                               "the reasoning arms' budget must fit (§2.2)")
        elif any(reasoned(a) for a in attempts) or r.get("reasoning"):
            return False, f"{r['id']} reasoned, and only the reasoning arms may"
    return True, (f"{path}: a valid answer from each arm, every attempt served by "
                  f"{plan.PROVIDER_NAME}, both reasoning arms reasoned and fitted their "
                  "budget, neither other arm reasoned")


def previous_check(session: str) -> tuple[bool, str]:
    """A pass after the smoke run, and pass 2 after pass 1 (§8)."""
    ok, why = smoke_check()
    if not ok or session != "pass2":
        return ok, why
    path = plan.ask_path("pass1")
    if not path.exists():
        return False, f"no record of pass 1 at {path}; pass 2 comes after it"
    wrong = under_protocol(json.loads(path.read_text()))
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    return True, f"{why}; {path} holds pass 1"


# ---------------------------------------------------------------------------
# Step 5: Stage A's record is the design the checks rebuilt
# ---------------------------------------------------------------------------

def sample_matches(design: population.Design, path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run reasoned_rule.sample first"
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
# Step 7: the client
# ---------------------------------------------------------------------------

class Asker(fm_ask.Asker):
    """Every arm's client: `PLAN_FIRST_MATCH.md`'s asker, with this plan's
    settings in its request and nothing else changed. Its loop, its retry by
    cause and its recorder are that plan's; `first_match/` is not touched."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = plan.MAX_RETRIES,
                 sleep: Callable[[float], None] = time.sleep):
        super().__init__(model=model, max_retries=max_retries, sleep=sleep)
        self.name = f"openrouter-reasoned-rule({model})"

    def request(self, arm: str, messages: list[dict], attempt: int) -> dict[str, Any]:
        s = plan.settings(arm)
        kwargs: dict[str, Any] = {
            "model": self.model, "messages": messages,
            "max_tokens": s["max_tokens"], "temperature": plan.TEMPERATURE,
            "extra_body": {"reasoning": s["reasoning"],
                           "provider": json.loads(json.dumps(plan.PROVIDER))}}
        if attempt == 0:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record
# ---------------------------------------------------------------------------

def ask(session: str, design: population.Design, asker: Any, partial: Path,
        header: dict, clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {r["id"] for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    order = design.sessions[session]
    pass_no = plan.pass_of(session)
    calls = getattr(asker, "calls", None)
    if not isinstance(calls, CallRecorder):
        calls = None

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for position, aid in enumerate(order):
            if aid in asked:
                continue
            a = design.asks[aid]
            if calls is not None:
                calls.take()
            t0 = clock()
            try:
                got = asker.ask(a)
                failure, causes = None, got["retries"]
            except ProposalError as exc:
                got = {"action": None, "payload": None, "keys": None, "reasoning": None}
                failure, causes = str(exc)[:300], getattr(exc, "causes", [])
            attempts = calls.take() if calls is not None else []
            by = served_by(attempts)
            row = {"session": session, "pass": pass_no, "position": position,
                   "id": aid, "arm": a.arm, "ticket": a.ticket, "digest": a.digest,
                   "action": got["action"], "served_by": by,
                   "valid": got["action"] in ACTIONS and by == plan.PROVIDER_NAME,
                   "payload": got["payload"], "keys": got["keys"],
                   "reasoning": got["reasoning"], "failure": failure,
                   "attempts": len(attempts), "retries": causes,
                   "call_attempts": attempts,
                   "seconds": round(clock() - t0, 2), "asked_at": now()}
            if failure is not None:
                pending.append(row)
                if len(pending) >= plan.MAX_CONSECUTIVE_FAILURES:
                    raise Outage(f"{len(pending)} asks in a row failed, the last "
                                 f"with: {failure}")
                continue
            for r in pending:
                keep(f, r)
            pending = []
            keep(f, row)
            print(f"  {len(rows):>5}/{len(order)}  {session}  {aid:<12} "
                  f"{got['action'] if row['valid'] else 'INVALID'}", end="\r", flush=True)
        for r in pending:
            keep(f, r)
    print()
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def record(session: str, rows: list[dict], resumed_at: list[str], started: str,
           checks: gates.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "pass": plan.pass_of(session),
        "temperature": plan.TEMPERATURE,
        "max_retries": plan.MAX_RETRIES,
        "system_prompts_sha256": {
            arm: hashlib.sha256(prompts.system_prompt(arm).encode()).hexdigest()
            for arm in prompts.ARMS},
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
        description="Stage B of PLAN_REASONED_RULE.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run RR-g1 to RR-g3 and stop; spends nothing")
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

    plan.refuse_unsigned(f"reasoned_rule/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = previous_check(args.session)
        if not ok:
            sys.exit(f"\nREFUSED: session {args.session} out of its turn — {why}.\n"
                     "  Nothing was built, spent or written.\n")
        print(f"turn check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: reasoned_rule/ask.py — {why}.\n  Nothing was built, "
                 "spent or written.\n")
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

    asker = Asker()
    digest = sample_sha256()
    header = {"protocol": json.loads(json.dumps(protocol())), "session": args.session,
              "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session}, "
          f"{len(checks.design.sessions[args.session])} asks\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, asker,
                               plan.partial_path(args.session), header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

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
