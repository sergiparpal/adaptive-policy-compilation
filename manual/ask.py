"""
Stage B1 of `PLAN_MANUAL.md`: shape C, the manual compiled once. **It spends.**

It asks §5's compile question at each level, once per level in the smoke run
and `ASKS` times per level in the session, in §2.5's order, and keeps every
answer. Nothing here installs or scores an answer: `manual/score.py` does that,
from the record. What the model writes is recorded as written (rule E).

THE CLIENT. OpenRouter's, through the `openai` SDK, as every paid writer here.
The model and reasoning off are `PLAN_REUSE.md`'s, imported through
`manual/plan.py`. The first attempt asks for a JSON object, and a retry asks
again with rung 2's own retry message, as `rung2/proposers2.py` does.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§9 of the plan):

  1. `--dry-run` runs `G-g1` to `G-g3` and stops. It never builds the client and
     never needs the key.
  2. The signature (`G-g4`). While `PLAN_MANUAL.md` carries a blank signature
     line this module exits here, before the checks, the destination or the
     client. No flag skips it.
  3. For the session: a smoke record under this plan's protocol, holding a
     valid ask.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `G-g1` to `G-g3`, blocking. Then Stage A's record must hold the prompts and
     the order the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

EVERY ATTEMPT IS KEPT. `harness/call_record.py`'s recorder is installed on the
client, and each row keeps its question's `call_attempts`: generation id,
provider, model, both finish reasons and the tokens. Each row also keeps the
text of every attempt, because an invalid ask is published with its raw text,
and an answer cut at the token limit is one.

A SESSION THAT DIES KEEPS WHAT IT PAID FOR, with `PLAN_FIDELITY.md`'s machinery
called: `open_partial` resumes from the git-ignored partial file, and a run of
`plan.MAX_CONSECUTIVE_FAILURES` failed calls stops the session without recording
them, because an outage is not answers.

    python3 -m manual.ask --dry-run
    .venv/bin/python -m manual.ask --session smoke
    .venv/bin/python -m manual.ask --session session
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from harness import call_record
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from fidelity import ask as fidelity_ask
from reuse.run import key_check
from rung2.proposers2 import ProposalError, parse_payload

from . import compile as C
from . import gates, plan, prompts

Outage = fidelity_ask.Outage
open_partial = fidelity_ask.open_partial
now = fidelity_ask.now


def protocol() -> dict[str, Any]:
    """As it reads back from JSON, so that a resumed partial file's header and a
    record's fields compare equal to it."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "shape": "C", "model": plan.MODEL,
        "temperature": plan.TEMPERATURE, "max_tokens": plan.COMPILE_MAX_TOKENS,
        "max_retries": plan.COMPILE_MAX_RETRIES, "reasoning": plan.REASONING,
        "order_seed": plan.ORDER_SEED, "asks": plan.ASKS,
        "texts_sha256": dict(plan.DIGESTS),
        "prompts_sha256": prompts.prompt_digests()["compile"]}))


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.sample_path()).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The client
# ---------------------------------------------------------------------------

class Compiler:
    """One compile question at a time. The text of every attempt is returned
    with the payload."""

    def __init__(self, model: str = plan.MODEL,
                 max_retries: int = plan.COMPILE_MAX_RETRIES):
        from openai import OpenAI

        self.name = f"openrouter-compile({model})"
        self.model = model
        self.max_retries = max_retries
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        self.calls = call_record.install(self)

    def request(self, messages: list[dict], attempt: int) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"model": self.model, "messages": messages,
                                  "max_tokens": plan.COMPILE_MAX_TOKENS,
                                  "temperature": plan.TEMPERATURE,
                                  "extra_body": {"reasoning": plan.REASONING}}
        if attempt == 0:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs

    def ask(self, level: int) -> tuple[dict[str, Any], list[str]]:
        """(payload, texts). Raises ProposalError, carrying the texts, if nothing
        parses."""
        messages = prompts.compile_messages(level)
        texts: list[str] = []
        last: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._client.chat.completions.create(
                    **self.request(messages, attempt))
                text = resp.choices[0].message.content or ""
                texts.append(text)
                return parse_payload(text), texts
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content": prompts.RETRY_MSG}]
        err = ProposalError(str(last))
        err.texts = texts
        raise err


# ---------------------------------------------------------------------------
# Step 3: the smoke record. Step 5: Stage A's record is the design rebuilt
# ---------------------------------------------------------------------------

def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.compile_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol().items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {sorted(wrong)}"
    valid = sum(1 for r in rec.get("rows", []) if r.get("valid"))
    if not valid:
        return False, f"{path} holds no valid ask"
    return True, f"{path}: {valid} valid ask(s) of {len(rec.get('rows', []))}"


def sample_matches(path: Path | None = None) -> tuple[bool, str]:
    from .sample import design
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run manual.sample first"
    rec = json.loads(path.read_text())
    now_ = json.loads(json.dumps(design()))
    for k in ("texts", "prompts", "order"):
        if rec["design"].get(k) != now_[k]:
            return False, f"{path}'s {k} differ from the ones rebuilt now"
    return True, f"{path}: the same texts, prompts and order"


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record that survives an interruption
# ---------------------------------------------------------------------------

def ask(session: str, compiler, partial: Path, header: dict,
        clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {(r["pass"], r["level"]) for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    schedule = plan.compile_schedule(session)
    digests = prompts.prompt_digests()["compile"]
    calls = getattr(compiler, "calls", None)

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for position, (pass_no, level) in enumerate(schedule):
            if (pass_no, level) in asked:
                continue
            if calls is not None:
                calls.take()
            t0 = clock()
            try:
                payload, texts = compiler.ask(level)
                failure = None
            except ProposalError as exc:
                payload, texts, failure = None, getattr(exc, "texts", []), str(exc)[:300]
            raw, why = C.rules_of(payload) if failure is None else ([], "no parseo")
            row = {"session": session, "pass": pass_no, "position": position,
                   "level": level, "prompt_sha256": digests[level],
                   "valid": why is None, "why_invalid": why,
                   "rules_in_answer": len(raw), "payload": payload,
                   "raw_answers": texts, "failure": failure,
                   "seconds": round(clock() - t0, 2), "asked_at": now()}
            if calls is not None:
                row["call_attempts"] = calls.take()
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
            print(f"  {len(rows):>3}/{len(schedule)}  pass {pass_no}  level {level}  "
                  f"{'valid' if row['valid'] else 'INVALID'}  {len(raw)} rules")
        for r in pending:
            keep(f, r)
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def record(session: str, compiler, rows: list[dict], resumed_at: list[str],
           started: str, checks: gates.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B1",
        "session": session,
        "compile_user": prompts.COMPILE_USER,
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
        description="Stage B1 of PLAN_MANUAL.md: the manual compiled once (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run G-g1 to G-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.COMPILE_SESSIONS,
                       help="the smoke run first, then the session")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"manual/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = smoke_check()
        if not ok:
            sys.exit(f"\nREFUSED: the session before a smoke run that worked — "
                     f"{why}.\n  Nothing was built, spent or written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: manual/ask.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    ok, why = sample_matches()
    if not ok:
        sys.exit(f"\nREFUSED: {why}. Nothing was spent.\n")
    print(f"Stage A: {why}")

    target = or_exit(refuse_overwrite, plan.compile_path(args.session),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    compiler = Compiler()
    digest = sample_sha256()
    header = {"protocol": protocol(), "session": args.session, "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B1 · session {args.session} with {compiler.name}\n")
    try:
        rows, resumed_at = ask(args.session, compiler, plan.compile_partial(args.session),
                               header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.compile_partial(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, compiler, rows, resumed_at,
                                        started, checks, digest),
                                 indent=2, default=str))
    plan.compile_partial(args.session).unlink()
    valid = sum(1 for r in rows if r["valid"])
    print(f"\n  answers {len(rows)}, valid {valid}, failed "
          f"{sum(1 for r in rows if r['failure'])}")
    print(f"\n-> {target}\n  {describe()}")
    if args.session == "smoke":
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the session may start' if ok else 'FAIL'} "
              f"· {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
