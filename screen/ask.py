"""
Stage B of `PLAN_SCREEN.md`: the calls. **The only module of the plan that
spends.**

It asks the model prompt v1 on prompts `PLAN_FIDELITY.md`'s own builders make:
the ticket alone, under v1's empty base, and the pilot's B prompts again. The
client is `PLAN_FIDELITY.md`'s, unchanged:
`OpenRouterProposer2(model, prompt_version="v1", reasoning={"effort": "none"})`,
whose `propose` is called exactly as rung 2's loop calls it (§1). What the model
writes beyond its `action` is recorded and never executed (rule E).

ONE THING IS ADDED, AND IT CHANGES NO REQUEST (§1). The proposer's SDK client is
wrapped by `FinishRecorder`, which passes every keyword argument through to the
same client and keeps each attempt's `finish_reason`. `PLAN_FIDELITY.md`'s
records never kept one, so its empty answers have no cause on record; these
records do. `tests/test_screen.py` checks against `tests/doubles.py` that the
requests are the ones the proposer builds without the wrapper. Since
2026-10-16 the client it wraps is already `harness.call_record`'s recorder, and
each row also keeps that recorder's `call_attempts`: the provider among them.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `V-g1` to `V-g3` and stops. It never builds the client and
     never needs the key.
  2. The signature (`V-g4`). While `PLAN_SCREEN.md` carries a blank signature
     line this module exits here, before the checks, the destination or the
     client. No flag skips it.
  3. For every session but the smoke run: a smoke record under this plan's
     protocol, holding a valid answer of each kind of prompt the session asks.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `V-g1` to `V-g3`, blocking. Then Stage A's record must hold the same
     sessions and prompt digests the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR (§5.10), with `PLAN_FIDELITY.md`'s
machinery called: `open_partial` resumes from the git-ignored partial file, and
a run of STOP_AFTER_FAILURES_IN_A_ROW failed calls stops the session without
recording them, because an outage is not answers.

    python3 -m screen.ask --dry-run
    .venv/bin/python -m screen.ask --session smoke
    .venv/bin/python -m screen.ask --session anchor
    .venv/bin/python -m screen.ask --session ticket_only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from harness.call_record import CallRecorder
from harness.domain import ACTIONS
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from fidelity import ask as fidelity_ask
from reuse.run import key_check
from rung2.proposers2 import OpenRouterProposer2, ProposalError

from . import plan, sample

TICKET_ONLY, HIDDEN = sample.TICKET_ONLY, sample.HIDDEN

# What each session asks, by kind of prompt. A smoke record must hold a valid
# answer of every kind a later session will ask.
KINDS = {"smoke": {TICKET_ONLY, HIDDEN},
         "anchor": {HIDDEN},
         "ticket_only": {TICKET_ONLY}}

# `PLAN_FIDELITY.md`'s, called: the same request, the same breaker.
TEMPERATURE = fidelity_ask.TEMPERATURE
MAX_TOKENS = fidelity_ask.MAX_TOKENS
STOP_AFTER_FAILURES_IN_A_ROW = fidelity_ask.STOP_AFTER_FAILURES_IN_A_ROW
Outage = fidelity_ask.Outage
open_partial = fidelity_ask.open_partial
now = fidelity_ask.now


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL,
            "prompt_version": plan.PROMPT, "reasoning": plan.REASONING,
            "seed": plan.SEED, "n": plan.N}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.SAMPLE_PATH).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The client, wrapped: each attempt's finish_reason, and nothing else
# ---------------------------------------------------------------------------

class FinishRecorder:
    """The proposer's SDK client, wrapped so that each attempt's
    `finish_reason` is kept. Every keyword argument reaches the wrapped client
    untouched, and its response comes back untouched: the request is
    `PLAN_FIDELITY.md`'s (§1)."""

    def __init__(self, client: Any):
        self.inner = client
        self.attempts: list[dict[str, Any]] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> Any:
        try:
            resp = self.inner.chat.completions.create(**kwargs)
        except Exception as exc:  # noqa: BLE001 — recorded, then raised as it was
            self.attempts.append({"finish_reason": None, "error": type(exc).__name__})
            raise
        choices = getattr(resp, "choices", None) or []
        self.attempts.append({"finish_reason": getattr(choices[0], "finish_reason", None)
                              if choices else None, "error": None})
        return resp

    def take(self) -> list[dict[str, Any]]:
        """The attempts of the call just made, and a clean slate for the next."""
        out, self.attempts = self.attempts, []
        return out


def wrap(proposer: OpenRouterProposer2) -> FinishRecorder:
    recorder = FinishRecorder(proposer._client)
    proposer._client = recorder
    return recorder


# ---------------------------------------------------------------------------
# Step 3: the smoke record
# ---------------------------------------------------------------------------

def smoke_check(kinds: set[str], path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke record at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    wrong = {k: rec.get(k) for k, v in protocol().items() if rec.get(k) != v}
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    valid = {r["kind"] for r in rec.get("rows", []) if r.get("valid")}
    missing = sorted(set(kinds) - valid)
    if missing:
        return False, f"{path} holds no valid answer for {missing}"
    return True, f"{path}: a valid answer for each of {sorted(kinds)}"


# ---------------------------------------------------------------------------
# Step 5: Stage A's record is the design the checks rebuilt
# ---------------------------------------------------------------------------

def sample_matches(design: sample.Design, path: Path | None = None) -> tuple[bool, str]:
    path = path or plan.SAMPLE_PATH
    if not path.exists():
        return False, f"no Stage A record at {path}; run screen.sample first"
    rec = json.loads(path.read_text())
    if rec.get("sessions") != json.loads(json.dumps(design.sessions)):
        return False, f"{path} holds other sessions than the ones rebuilt now"
    stale = [i for i, it in design.items.items()
             if rec.get("items", {}).get(i, {}).get("digest") != it["digest"]]
    if stale:
        return False, f"{len(stale)} prompts rebuilt now differ from {path}'s"
    if rec.get("decisions") != json.loads(json.dumps(design.decisions)):
        return False, f"{path} holds other decisions than the ones rebuilt now"
    return True, f"{path}: the same sessions, prompts and decisions"


# ---------------------------------------------------------------------------
# The labels, copied from the records and never computed (rule B)
# ---------------------------------------------------------------------------

def labels(design: sample.Design, item: dict) -> dict[str, Any]:
    """Off `PLAN_REUSE.md`'s records, the rows `PLAN_FIDELITY.md` copied its
    labels from. Stage C reads `y` off `PLAN_FIDELITY.md`'s own records and
    checks these against them."""
    runs = design.fidelity.runs
    if item["kind"] == TICKET_ONLY:
        return {"truth": runs[plan.RUNS[0]]["records"][item["idx"]]["truth"],
                "rare": item["rare"],
                "serves": [{"run": k, "idx": i,
                            "population": design.decisions[f"d{k}:{i}"]["population"]}
                           for k, i in item["serves"]]}
    row = runs[item["run"]]["records"][item["idx"]]
    return {"truth": row["truth"], "rule_id": row["winner_id"],
            "rule_action": row["predicted"], "rule_right": row["correct"]}


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record that survives an interruption
# ---------------------------------------------------------------------------

def ask(session: str, design: sample.Design, proposer, recorder: FinishRecorder,
        partial: Path, header: dict, clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {(r["pass"], r["id"]) for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    plan_ = design.sessions[session]
    total = sum(len(p) for p in plan_["passes"])
    # Since 2026-10-16 the proposer's own client carries `harness.call_record`'s
    # recorder, inside `FinishRecorder`: the provider and the rest of what each
    # attempt said, beside the finish reasons this module has always kept.
    calls = getattr(proposer, "calls", None)
    if not isinstance(calls, CallRecorder):
        calls = None

    def keep(f, row: dict) -> None:
        f.write(json.dumps(row) + "\n")
        f.flush()
        rows.append(row)

    with partial.open("a") as f:
        for pass_no, order in enumerate(plan_["passes"], start=1):
            for position, iid in enumerate(order):
                if (pass_no, iid) in asked:
                    continue
                item, p = design.items[iid], design.prompts[iid]
                recorder.take()
                if calls is not None:
                    calls.take()
                t0 = clock()
                try:
                    action, payload = proposer.propose(p.case, p.base_text)
                    failure = None
                except ProposalError as exc:
                    action, payload, failure = None, None, str(exc)[:300]
                attempts = recorder.take()
                row = {"session": session, "pass": pass_no, "position": position,
                       "id": iid, "kind": item["kind"], "run": item["run"],
                       "idx": item["idx"], "digest": p.digest,
                       "shown_ids": list(p.shown_ids), "action": action,
                       "valid": action in ACTIONS, "payload": payload,
                       "failure": failure, "attempts": len(attempts),
                       "finish_reasons": [a["finish_reason"] for a in attempts],
                       "attempt_errors": [a["error"] for a in attempts],
                       "labels": labels(design, item),
                       "seconds": round(clock() - t0, 2), "asked_at": now()}
                if calls is not None:
                    row["call_attempts"] = calls.take()
                if failure is not None:
                    pending.append(row)
                    if len(pending) >= STOP_AFTER_FAILURES_IN_A_ROW:
                        raise Outage(f"{len(pending)} calls in a row failed, the last "
                                     f"with: {failure}")
                    continue
                for r in pending:
                    keep(f, r)
                pending = []
                keep(f, row)
                print(f"  {len(rows):>5}/{total}  pass {pass_no}  {iid:<12} "
                      f"{action if row['valid'] else 'INVALID'}", end="\r", flush=True)
        for r in pending:
            keep(f, r)
    print()
    rows.sort(key=lambda r: (r["pass"], r["position"]))
    return rows, resumed_at


def record(session: str, proposer, rows: list[dict], resumed_at: list[str],
           started: str, checks: sample.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "max_retries": proposer.max_retries,
        "system_prompt": proposer.system_prompt,
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
        description="Stage B of PLAN_SCREEN.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run V-g1 to V-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.SESSIONS,
                       help="one session of §8, in its order")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = sample.run_checks(suite=True)
        sample.report(checks)
        print("\ndry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"screen/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = smoke_check(KINDS[args.session])
        if not ok:
            sys.exit(f"\nREFUSED: session {args.session} before a smoke run that "
                     f"worked — {why}.\n  Nothing was built, spent or written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: screen/ask.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = sample.run_checks(suite=True)
    sample.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    ok, why = sample_matches(checks.design)
    if not ok:
        sys.exit(f"\nREFUSED: {why}. Nothing was spent.\n")
    print(f"Stage A: {why}")

    target = or_exit(refuse_overwrite, plan.ask_path(args.session),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    proposer = OpenRouterProposer2(model=plan.MODEL, prompt_version=plan.PROMPT,
                                   reasoning=plan.REASONING)
    recorder = wrap(proposer)
    digest = sample_sha256()
    header = {"protocol": protocol(), "session": args.session,
              "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session} with {proposer.name}\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, proposer, recorder,
                               plan.partial_path(args.session), header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, proposer, rows, resumed_at,
                                        started, checks, digest),
                                 indent=2, default=str))
    plan.partial_path(args.session).unlink()
    valid = sum(1 for r in rows if r["valid"])
    print(f"\n  answers {len(rows)}, valid {valid}, failed "
          f"{sum(1 for r in rows if r['failure'])}")
    print(f"\n-> {target}\n  {describe()}")
    if args.session == "smoke":
        ok, why = smoke_check(KINDS["smoke"], target)
        print(f"\nsmoke check: {'PASS — the sessions may start' if ok else 'FAIL'} "
              f"· {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
