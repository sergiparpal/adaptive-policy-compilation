"""
Stage B of `PLAN_QUEUE_ALONE.md`: the calls. **The only module of the plan that
spends.**

It asks the model the three arms' prompts, every call pinned to one provider
(§2.3 of the plan):

  t  the rule arm, through the proposer `manual/run.py` builds for the level,
     `manual.run.build_proposer(level)`: rung 2's `OpenRouterProposer2` with
     v1, reasoning off and the level's system prompt. Its `propose` is called
     as `PLAN_APPLY.md` called it, on v1's empty base: temperature 0, 1,200
     tokens, `response_format` on the first attempt, two retries.
  i, q  the impasse and plain arms, through this module's `Asker`: the same
     model, temperature, tokens, reasoning setting and `response_format`, and on
     a failed parse the same two retries with v1's retry message.

THE PIN, AND NOTHING ELSE. `pin` puts OpenRouter's provider routing,
`plan.PROVIDER`, into every request the rule arm's proposer sends, by wrapping
its client: `rung2/proposers2.py` is not edited (rule A). The `Asker` sends it
itself. `tests/test_queue_alone.py` checks, through `tests/doubles.py`'s SDK
double, that each arm's request is the proposer's own with the pin added, and
that nothing else differs. What the model writes beyond its `action` is
recorded in full and never executed (rule E).

EACH ROW KEEPS WHAT THE CALL SAID ABOUT ITSELF. Both clients carry
`harness.call_record`'s recorder, which changes no request. Its `take()` before
an ask clears it, and after the ask the row keeps every attempt's provider,
finish reasons and tokens as `call_attempts`. **The provider that served an
answer is its last attempt's**, kept as `served_by`. An answer is valid only
when its `action` is one of the eight queues and `served_by` is
`plan.PROVIDER_NAME` (rule G): an answer from another provider is recorded,
counted and never read.

NO ROW CARRIES A LABEL (rule B). A row says what was asked and what came back.
Stage C joins the truth from the loop records. The blocking checks this module
runs before spending read labels offline, and send nothing.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `QA-g1` to `QA-g3` and stops. It never builds a client
     and never needs the key.
  2. The signature (`QA-g4`). While `PLAN_QUEUE_ALONE.md` carries a blank
     signature line this module exits here, before the checks, the destination
     or a client. No flag skips it.
  3. What comes before the session: for a pass, the smoke record under this
     protocol, with a valid answer from each arm and every attempt served by
     the pinned provider; for pass 2, pass 1's record.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `QA-g1` to `QA-g3`, blocking. Then Stage A's record must hold the same
     sessions and prompt digests the checks just rebuilt.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The clients, and the calls: sequential (hard rule 3).

A SESSION THAT DIES KEEPS WHAT IT PAID FOR (§5.10), with `PLAN_FIDELITY.md`'s
machinery called: `open_partial` resumes from the git-ignored partial file, and
a run of `plan.MAX_CONSECUTIVE_FAILURES` failed calls stops the session without
recording them, because an outage is not answers. A pinned provider that does
not serve fails every call, and stops a session the same way. **A pass outlives
a background command of the agent's harness**, so the passes run in Sergi's
terminal.

    python3 -m queue_alone.ask --dry-run
    .venv/bin/python -m queue_alone.ask --session smoke
    .venv/bin/python -m queue_alone.ask --session pass1
    .venv/bin/python -m queue_alone.ask --session pass2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

from harness import call_record
from harness.call_record import CallRecorder
from harness.domain import ACTIONS
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from fidelity import ask as fidelity_ask
from manual.run import build_proposer
from reuse.run import key_check
from rung2.proposers2 import ProposalError, parse_payload

from . import gates, plan, population, prompts

# `PLAN_FIDELITY.md`'s, called: the partial file and the breaker.
Outage = fidelity_ask.Outage
open_partial = fidelity_ask.open_partial
now = fidelity_ask.now


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL, "prompt_version": plan.PROMPT,
            "reasoning": plan.REASONING, "provider": plan.PROVIDER,
            "seed": plan.SEED, "n": plan.N}


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.sample_path()).read_bytes()).hexdigest()


def served_by(attempts: list[dict[str, Any]]) -> str | None:
    """The provider of an answer: its last attempt's, the one whose text was
    parsed."""
    return attempts[-1].get("provider") if attempts else None


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
    return True, (f"{path}: a valid answer from each arm, every attempt served by "
                  f"{plan.PROVIDER_NAME}")


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
        return False, f"no Stage A record at {path}; run queue_alone.sample first"
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
# Step 7: the clients
# ---------------------------------------------------------------------------

class Pinned:
    """A client whose every request carries `plan.PROVIDER` in its `extra_body`,
    and is otherwise the request it was handed. It answers to
    `.chat.completions.create`, which is all the proposer uses."""

    def __init__(self, inner: Any):
        self.inner = inner
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> Any:
        body = dict(kwargs.get("extra_body") or {})
        body["provider"] = json.loads(json.dumps(plan.PROVIDER))
        return self.inner.chat.completions.create(**{**kwargs, "extra_body": body})


def pin(proposer: Any) -> Any:
    """The proposer, with the pin wrapped around its recorded client. Its
    recorder stays where `calls` points, so `take()` still sees every attempt."""
    if not isinstance(getattr(proposer, "calls", None), CallRecorder):
        raise ValueError("pin a proposer whose client carries a call recorder")
    if not isinstance(proposer._client, Pinned):
        proposer._client = Pinned(proposer._client)
    return proposer


class Asker:
    """The impasse and plain arms' client: one prompt in, one queue out. It is
    `OpenRouterProposer2.propose`'s loop over this plan's messages, with the pin
    in every request. `rung2/` is not touched."""

    def __init__(self, model: str = plan.MODEL, max_retries: int = plan.MAX_RETRIES):
        from openai import OpenAI

        self.name = f"openrouter-queue-alone({model})"
        self.model = model
        self.max_retries = max_retries
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
        self.calls = call_record.install(self)

    def request(self, messages: list[dict], attempt: int) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model, "messages": messages,
            "max_tokens": plan.MAX_TOKENS, "temperature": plan.TEMPERATURE,
            "extra_body": {"reasoning": plan.REASONING,
                           "provider": json.loads(json.dumps(plan.PROVIDER))}}
        if attempt == 0:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs

    def ask(self, a: prompts.Ask) -> tuple[str | None, dict[str, Any]]:
        messages = a.messages()
        last: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._client.chat.completions.create(**self.request(messages, attempt))
                payload = parse_payload(resp.choices[0].message.content or "")
                return payload.get("action"), payload
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content": prompts.RETRY_MSG}]
        raise ProposalError(str(last))


class Clients:
    """The rule arm's proposer for each level, pinned, and one asker for the
    other two arms, each built when first needed. The builders are looked up
    then, so that a test can stand the SDK double behind them."""

    def __init__(self, build_rule: Callable[[int], Any] | None = None,
                 build_asker: Callable[[], Any] | None = None):
        self._build_rule = build_rule
        self._build_asker = build_asker
        self.rule: dict[int, Any] = {}
        self.asker: Any = None

    def for_rule(self, level: int) -> Any:
        if level not in self.rule:
            self.rule[level] = pin((self._build_rule or build_proposer)(level))
        return self.rule[level]

    def for_question(self) -> Any:
        if self.asker is None:
            self.asker = (self._build_asker or Asker)()
        return self.asker


def answer(a: prompts.Ask, clients: Clients) -> tuple[Any, tuple[str | None, Any]]:
    """The client that asks `a`, and what it answered."""
    if a.arm == prompts.RULE:
        proposer = clients.for_rule(a.level)
        return proposer, proposer.propose(a.case, prompts.EMPTY_BASE)
    asker = clients.for_question()
    return asker, asker.ask(a)


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record
# ---------------------------------------------------------------------------

def ask(session: str, design: population.Design, clients: Clients, partial: Path,
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
            client = (clients.for_rule(a.level) if a.arm == prompts.RULE
                      else clients.for_question())
            calls = getattr(client, "calls", None)
            if not isinstance(calls, CallRecorder):
                calls = None
            if calls is not None:
                calls.take()
            t0 = clock()
            try:
                _, (action, payload) = answer(a, clients)
                failure = None
            except ProposalError as exc:
                action, payload, failure = None, None, str(exc)[:300]
            attempts = calls.take() if calls is not None else []
            by = served_by(attempts)
            row = {"session": session, "pass": pass_no, "position": position,
                   "id": aid, "arm": a.arm, "level": a.level, "ticket": a.ticket,
                   "digest": a.digest, "action": action, "served_by": by,
                   "valid": action in ACTIONS and by == plan.PROVIDER_NAME,
                   "payload": payload, "failure": failure, "attempts": len(attempts),
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
            print(f"  {len(rows):>5}/{len(order)}  {session}  {aid:<14} "
                  f"{action if row['valid'] else 'INVALID'}", end="\r", flush=True)
        for r in pending:
            keep(f, r)
    print()
    rows.sort(key=lambda r: r["position"])
    return rows, resumed_at


def record(session: str, clients: Clients, rows: list[dict], resumed_at: list[str],
           started: str, checks: gates.Checks, digest: str) -> dict[str, Any]:
    return {
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": session,
        "pass": plan.pass_of(session),
        "temperature": plan.TEMPERATURE,
        "max_tokens": plan.MAX_TOKENS,
        "max_retries": plan.MAX_RETRIES,
        "system_prompts_sha256": {
            f"{arm} L{lv}": hashlib.sha256(prompts.system_prompt(arm, lv).encode()).hexdigest()
            for arm in prompts.ARMS for lv in plan.LEVELS},
        "rule_proposers_system_prompts_sha256": {
            lv: hashlib.sha256(p.system_prompt.encode()).hexdigest()
            for lv, p in sorted(clients.rule.items())},
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
        description="Stage B of PLAN_QUEUE_ALONE.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run QA-g1 to QA-g3 and stop; spends nothing")
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

    plan.refuse_unsigned(f"queue_alone/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = previous_check(args.session)
        if not ok:
            sys.exit(f"\nREFUSED: session {args.session} out of its turn — {why}.\n"
                     "  Nothing was built, spent or written.\n")
        print(f"turn check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: queue_alone/ask.py — {why}.\n  Nothing was built, "
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

    clients = Clients()
    digest = sample_sha256()
    header = {"protocol": json.loads(json.dumps(protocol())), "session": args.session,
              "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session}, "
          f"{len(checks.design.sessions[args.session])} asks\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, clients,
                               plan.partial_path(args.session), header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record(args.session, clients, rows, resumed_at,
                                        started, checks, digest),
                                 indent=2, default=str))
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
