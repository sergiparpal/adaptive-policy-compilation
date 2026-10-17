"""
Stage B of `PLAN_RANKING.md`: the calls. **The only module of the plan that
spends.**

It asks the model the one question of `ranking/question.py`, in the twelve
presentations of Stage A, twice each, and keeps every answer. The client is rung
2's pairwise judge's, with the judge's settings imported (rule A), and with
reasoning off, `PLAN_REUSE.md`'s setting since its amendment of 2026-09-30
(`ranking/plan.py` says why). What the model writes beyond its ranking is
recorded and never executed (rule E).

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `M-g1` to `M-g3` and stops. It never builds the client and
     never needs the key.
  2. The signature (`M-g4`). While `PLAN_RANKING.md` carries a blank signature
     line this module exits here, before the checks, the destination or the
     client. No flag skips it.
  3. For the session: a smoke record under this plan's protocol, holding a
     valid ranking.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `M-g1` to `M-g3`, blocking. Then Stage A's record must hold the same
     presentations, digests and pass orders the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

EVERY ATTEMPT IS KEPT. `harness/call_record.py`'s recorder is installed on the
client, and each row keeps its question's `call_attempts`: generation id,
provider, model, both finish reasons and the tokens. Each row also keeps the
text of every attempt, because an invalid answer is published with its raw
text (§5.7).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR, with `PLAN_FIDELITY.md`'s machinery
called: `open_partial` resumes from the git-ignored partial file, and a run of
`plan.MAX_CONSECUTIVE_FAILURES` failed calls stops the session without recording
them, because an outage is not answers. An answer that parses into an invalid
ranking is an answer, not a failure: it is recorded and Stage C excludes it.

    python3 -m ranking.ask --dry-run
    .venv/bin/python -m ranking.ask --session smoke
    .venv/bin/python -m ranking.ask --session session
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

from . import gates, plan, question

Outage = fidelity_ask.Outage
open_partial = fidelity_ask.open_partial
now = fidelity_ask.now


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL,
            "temperature": plan.TEMPERATURE, "max_tokens": plan.MAX_TOKENS,
            "max_retries": plan.MAX_RETRIES, "reasoning": plan.REASONING,
            "presentation_seed": plan.PRESENTATION_SEED,
            "presentations": plan.PRESENTATIONS, "passes": plan.PASSES,
            "system_prompt_sha256": hashlib.sha256(
                question.SYSTEM_PROMPT.encode()).hexdigest()}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.SAMPLE_PATH).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The client
# ---------------------------------------------------------------------------

class Asker:
    """Rung 2's pairwise judge, asking this plan's question. `Judge.ask`'s loop,
    with two differences: every request carries reasoning off, and the text of
    every attempt is returned with the payload. `rung2/` is not touched."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = plan.MAX_RETRIES):
        from openai import OpenAI

        self.name = f"openrouter-ranking({model})"
        self.model = model
        self.max_retries = max_retries
        self.system_prompt = question.SYSTEM_PROMPT
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        self.calls = call_record.install(self)

    def request(self, messages: list[dict], attempt: int) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"model": self.model, "messages": messages,
                                  "max_tokens": plan.MAX_TOKENS,
                                  "temperature": plan.TEMPERATURE,
                                  "extra_body": {"reasoning": plan.REASONING}}
        if attempt == 0:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs

    def ask(self, order) -> tuple[dict[str, Any], list[str]]:
        """(payload, texts). Raises ProposalError, carrying the texts, if nothing
        parses."""
        messages = question.messages(order)
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
                        {"role": "user", "content": question.RETRY_MSG}]
        err = ProposalError(str(last))
        err.texts = texts
        raise err


# ---------------------------------------------------------------------------
# Step 3: the smoke record
# ---------------------------------------------------------------------------

def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol().items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    valid = sum(1 for r in rec.get("rows", []) if r.get("valid"))
    if not valid:
        return False, f"{path} holds no valid ranking"
    return True, f"{path}: {valid} valid ranking(s) of {len(rec.get('rows', []))}"


# ---------------------------------------------------------------------------
# Step 5: Stage A's record is the design the checks rebuilt
# ---------------------------------------------------------------------------

def sample_matches(path: Path | None = None) -> tuple[bool, str]:
    from .sample import design
    path = path or plan.SAMPLE_PATH
    if not path.exists():
        return False, f"no Stage A record at {path}; run ranking.sample first"
    rec = json.loads(path.read_text())
    now_ = design()
    for k in ("presentations", "passes", "smoke", "system_prompt_sha256"):
        if rec.get(k) != json.loads(json.dumps(now_[k])):
            return False, f"{path}'s {k} differ from the ones rebuilt now"
    return True, f"{path}: the same presentations, digests and pass orders"


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record that survives an interruption
# ---------------------------------------------------------------------------

def schedule(session: str) -> list[tuple[int, str]]:
    """(pass, presentation) in the order they are asked."""
    pres = question.presentations()
    if session == "smoke":
        return [(1, pid) for pid in question.smoke_order(pres)]
    return [(p, pid) for p, order in enumerate(question.pass_orders(pres), start=1)
            for pid in order]


def ask(session: str, asker, partial: Path, header: dict,
        clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {(r["pass"], r["pid"]) for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    pres = {p.pid: p for p in question.presentations()}
    plan_ = schedule(session)
    calls = getattr(asker, "calls", None)

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for position, (pass_no, pid) in enumerate(plan_):
            if (pass_no, pid) in asked:
                continue
            p = pres[pid]
            if calls is not None:
                calls.take()
            t0 = clock()
            try:
                payload, texts = asker.ask(p.order)
                failure = None
            except ProposalError as exc:
                payload, texts, failure = None, getattr(exc, "texts", []), str(exc)[:300]
            ranking = question.ranking_of(payload)
            row = {"session": session, "pass": pass_no, "position": position,
                   "pid": pid, "order": list(p.order), "digest": p.digest,
                   "ranking": ranking, "valid": ranking is not None,
                   "payload": payload, "raw_answers": texts, "failure": failure,
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
            shown = " > ".join(q.split("_")[0] for q in ranking) if ranking else "INVALID"
            print(f"  {len(rows):>3}/{len(plan_)}  pass {pass_no}  {pid}  {shown}")
        for r in pending:
            keep(f, r)
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def record(session: str, asker, rows: list[dict], resumed_at: list[str],
           started: str, checks: gates.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "system_prompt": asker.system_prompt,
        "sample_record": str(plan.SAMPLE_PATH),
        "sample_sha256": digest,
        "gates": checks.summary(),
        "started_at": started,
        "resumed_at": resumed_at,
        "finished_at": now(),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_RANKING.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run M-g1 to M-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.SESSIONS,
                       help="the smoke run first, then the session")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True, progress=True)
        gates.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"ranking/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = smoke_check()
        if not ok:
            sys.exit(f"\nREFUSED: the session before a smoke run that worked — "
                     f"{why}.\n  Nothing was built, spent or written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: ranking/ask.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_checks(suite=True, progress=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    ok, why = sample_matches()
    if not ok:
        sys.exit(f"\nREFUSED: {why}. Nothing was spent.\n")
    print(f"Stage A: {why}")

    target = or_exit(refuse_overwrite, plan.ask_path(args.session),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    asker = Asker()
    digest = sample_sha256()
    header = {"protocol": protocol(), "session": args.session, "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session} with {asker.name}\n")
    try:
        rows, resumed_at = ask(args.session, asker, plan.partial_path(args.session),
                               header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, asker, rows, resumed_at,
                                        started, checks, digest),
                                 indent=2, default=str))
    plan.partial_path(args.session).unlink()
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
