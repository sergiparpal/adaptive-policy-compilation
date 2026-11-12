"""
Stage B of `PLAN_CORRECTIONS.md`, its second half: the at-once asks (§2.4, §5.3).
**It spends.** On the proposer's path in the sense `tests/test_oracle_separation.py`
watches: it sends level 1's catalogue, and the labels arm `l`'s proposer was
handed, read off that arm's own record. Nothing here imports the policy in code
(§4).

WHAT AN ASK IS. Under level 1's compile prompt, `PLAN_MANUAL.md`'s shape C,
`manual.prompts.compile_system_prompt(1)`, the model is handed the labelled
tickets of one L run up to a checkpoint, and asked for the whole base in one
answer. The user message is §2.4's header, one line per labelled ticket in
arrival order, and `PLAN_MANUAL.md`'s request, byte for byte:

    CORRECCIONES DE REVISORES: el sistema decidio mal cada uno de estos
    tickets, y un revisor le dio su cola correcta.
    {"ticket": {...}, "cola_correcta": "..."}
    ...

    Escribe ahora la base de reglas completa.

With no label, the user message is `PLAN_MANUAL.md`'s request alone, and the
messages are its level-1 compile messages exactly.

THE SESSIONS (§2.4, §9), each a record of its own, in this order:

  smoke   two asks: one with no label, one on L's smoke run's labels;
  prior   five asks with no label, right after the smoke;
  l_r<k>  after L's run k and before the next run: three asks at each
          checkpoint the run reaches, 10, 20, 40, 80, 160 and 320 labels, and
          three at all of its labels.

An ask whose answer is not valid is asked again, at most twice, as a new ask
with the same messages. **Valid** is §0's: an answer the pinned provider served,
that ended `stop`, and whose payload holds a non-empty list `rules`, as
`manual.compile.rules_of` reads it. What the model wrote is kept whole, its
reasoning included, and never repaired.

THE CLIENT is `placement.protocol.Asker` with DeepInfra's pin, behind
`reasoned_loop.protocol.Live`, with one change to its request: the budget is
`plan.AT_ONCE_MAX_TOKENS`, twice the loop's. A failed parse is retried with v1's
retry message, as that asker retries every two-message request.

THE ASKS GO THROUGH `harness/ask_pool.py`, at most `plan.WORKERS` at a time.
They are asks: nothing an answer says is installed, executed or shown to a later
ask. As that module asks of any plan that uses it, the record keeps the workers,
the seconds are read at that concurrency, the smoke session measures the pace
and the refusals for the rate, and a refusal there means running the sessions
one ask at a time. The breaker stops a session after
`plan.MAX_CONSECUTIVE_FAILURES` failed asks in a row, read in the order the asks
come back.

THE ORDER OF EVENTS, as `corrections/run.py`'s: the signature, what comes
before, the key, the blocking checks, the destination, and only then the client.

    python3 -m corrections.ask --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m corrections.ask --session smoke
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from harness import ask_pool
from harness.domain import generate_corpus
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from authorship import run as erun
from first_match import ask as fm_ask
from manual import compile as C
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from reuse.run import key_check
from rung2.proposers2 import ProposalError

from . import gates, plan, prompts

Outage = fm_ask.Outage
STOPS = (fm_ask.Outage, erun.Outage)    # the breaker, or the rate through every wait
now = pl_run.now


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


@lru_cache(maxsize=1)
def corpus() -> tuple:
    return tuple(generate_corpus(plan.N, seed=plan.SEED))


# ---------------------------------------------------------------------------
# The labels an L run handed its proposer
# ---------------------------------------------------------------------------

class NotHanded(ValueError):
    """An L record whose reports are not its reported errors' labels: an
    instrument failure. Nothing is asked."""


def labelled(record: dict[str, Any]) -> list[tuple[int, str]]:
    """`(case, queue)` for every escalation of an L record caused by a reported
    error, in arrival order, with the queue its proposer was handed. Refused
    unless every such escalation was handed its own label and no other case
    was handed one."""
    handed = record.get("reports_handed") or {}
    truth = {r["idx"]: r["truth"] for r in record["records"]}
    out = [(esc["idx"], handed.get(str(esc["idx"])))
           for esc in record["escalations"] if esc["kind"] == plan.ERROR]
    bad = [i for i, q in out if q is None or q != truth[i]]
    extra = sorted(set(handed) - {str(i) for i, _ in out})
    if bad or extra:
        raise NotHanded(f"reports that are not the reported cases' labels: {bad[:5]}, "
                        f"and reports at other cases: {extra[:5]}")
    return out


# ---------------------------------------------------------------------------
# The design of a session
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Ask:
    id: str
    session: str
    checkpoint: int                    # labels handed in; 0 for none
    k: int                             # the ask's number at its checkpoint
    labelled: tuple                    # ((case, queue), ...) up to the checkpoint
    reask: int = 0

    def messages(self) -> list[dict[str, str]]:
        cases = corpus()
        return prompts.messages([(cases[i], q) for i, q in self.labelled])

    def digest(self) -> str:
        return sha256(json.dumps(self.messages(), ensure_ascii=False))[:16]


def ask_id(session: str, checkpoint: int, k: int, reask: int = 0) -> str:
    return f"{session}:{checkpoint}:{k}" + (f":re{reask}" if reask else "")


def source_of(session: str) -> Path | None:
    """The L record a session reads its labels off: none for `prior`."""
    if session == "smoke":
        return plan.smoke_path(plan.LABELLED)
    if session == "prior":
        return None
    return plan.run_path(plan.LABELLED, int(session.rsplit("r", 1)[1]))


def design(session: str, record: dict[str, Any] | None = None) -> list[Ask]:
    """The first pass of a session's asks, in order (§2.4)."""
    if session not in plan.SESSIONS:
        raise ValueError(f"no session {session!r}: {plan.SESSIONS}")
    if session == "prior":
        return [Ask(ask_id(session, 0, k), session, 0, k, ()) for k in
                range(1, plan.PRIOR_ASKS + 1)]
    got = tuple(labelled(record))
    if session == "smoke":
        if not got:
            raise NotHanded("L's smoke run handed its proposer no label: the smoke "
                            "session has nothing to ask on")
        return [Ask(ask_id(session, 0, 1), session, 0, 1, ()),
                Ask(ask_id(session, len(got), 1), session, len(got), 1, got)]
    return [Ask(ask_id(session, j, k), session, j, k, got[:j])
            for j in plan.checkpoints(len(got)) for k in range(1, plan.ASKS_PER_CHECKPOINT + 1)]


def reasks(asks: list[Ask], rows: list[dict[str, Any]], reask: int) -> list[Ask]:
    """The asks of pass `reask`: every ask of the pass before whose answer was
    not valid, asked again with the same messages."""
    valid = {r["id"] for r in rows if r.get("valid")}
    before = [a for a in asks if a.reask == reask - 1]
    return [Ask(ask_id(a.session, a.checkpoint, a.k, reask), a.session, a.checkpoint, a.k,
                a.labelled, reask) for a in before if a.id not in valid]


# ---------------------------------------------------------------------------
# One ask
# ---------------------------------------------------------------------------

def validity(failure: str | None, payload: Any, finish: str | None,
             served: str | None) -> str | None:
    """Why an answer is not valid (§0), or None."""
    if failure is not None:
        return f"the call failed: {failure[:120]}"
    if served != plan.PROVIDER_NAME:
        return f"served by {served}, not {plan.PROVIDER_NAME}"
    if finish != "stop":
        return f"ended {finish!r}, not 'stop'"
    _, why = C.rules_of(payload)
    return why


def row_of(a: Ask, position: int, got: Any, failure: str | None, attempts: list[dict],
           seconds: float) -> dict[str, Any]:
    payload = getattr(got, "payload", None)
    finish = getattr(got, "finish_reason", None)
    served = fm_ask.served_by(attempts)
    why = validity(failure, payload, finish, served)
    return {"session": a.session, "position": position, "id": a.id,
            "checkpoint": a.checkpoint, "k": a.k, "reask": a.reask,
            "labelled": [list(x) for x in a.labelled], "digest": a.digest(),
            "served_by": served, "valid": why is None, "why_invalid": why,
            "payload": payload, "keys": getattr(got, "keys", None),
            "reasoning": getattr(got, "reasoning", None), "finish_reason": finish,
            "failure": failure, "attempts": len(attempts),
            "retries": getattr(got, "retries", None), "call_attempts": attempts,
            "seconds": round(seconds, 2), "asked_at": now()}


def ask_one(live, position: int, a: Ask, clock=time.monotonic) -> dict[str, Any]:
    t0 = clock()
    try:
        got = live.ask(a.messages())
        failure, attempts = None, list(got.call_attempts or [])
    except STOPS:
        raise
    except ProposalError as exc:
        got, failure = exc, str(exc)[:300]
        attempts = list(getattr(exc, "call_attempts", []) or [])
    return row_of(a, position, None if failure else got, failure, attempts, clock() - t0)


# ---------------------------------------------------------------------------
# The client
# ---------------------------------------------------------------------------

class AtOnceAsker(pl_protocol.Asker):
    """`placement.protocol.Asker` with DeepInfra's pin and the at-once budget.
    Built only after the gate, the key check and the blocking checks."""

    def __init__(self, pin: dict | None = None, sleep=time.sleep):
        super().__init__(pin=pin, sleep=sleep)
        self.name = f"openrouter-at-once({self.model},{self.pin['order'][0]})"

    def request(self, arm: str, messages_: list[dict], attempt: int) -> dict[str, Any]:
        return prompts.request(self.pin, self.model, arm, messages_, attempt)


def make_worker(sleep) -> p.Live:
    return p.Live(AtOnceAsker(pin=plan.PROVIDER, sleep=sleep))


# ---------------------------------------------------------------------------
# A session
# ---------------------------------------------------------------------------

def protocol_header(session: str, source_sha256: str | None,
                    workers: int = plan.WORKERS) -> dict[str, Any]:
    """What a session is asked under, and what its partial file must have been
    written under to be resumed."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "shape": "at once", "level": plan.LEVEL,
        "model": plan.MODEL, "temperature": plan.TEMPERATURE,
        "settings": plan.at_once_settings(), "provider": plan.PROVIDER,
        "call_retry_wait": list(plan.CALL_RETRY_WAIT),
        "rate_limit_wait": list(plan.RATE_LIMIT_WAIT), "seed": plan.SEED, "n": plan.N,
        "workers": workers, "max_reasks": plan.MAX_REASKS, "session": session,
        "source_sha256": source_sha256, "texts_sha16": prompts.digests()}))


def file_sha256(path: Path | None) -> str | None:
    return None if path is None else hashlib.sha256(path.read_bytes()).hexdigest()


def run_session(session: str, record: dict[str, Any] | None, live_factory, partial: Path,
                header: dict[str, Any], workers: int = plan.WORKERS) -> tuple[list, list, list]:
    """Every pass of a session: the first, then up to `plan.MAX_REASKS` passes
    of the asks still without a valid answer. Returns the asks, the rows and
    the hours it resumed at."""
    done, resumed = erun.open_partial(partial, header)
    resumed_at = [now()] if resumed else []
    asks = design(session, record)
    rows = list(done)

    def keep(row: dict[str, Any]) -> None:
        with partial.open("a") as f:
            f.write(json.dumps(row) + "\n")
            f.flush()

    for reask in range(0, plan.MAX_REASKS + 1):
        this = [a for a in asks if a.reask == reask] if reask == 0 else reasks(asks, rows,
                                                                                reask)
        if reask:
            asks += this
        if not this:
            break
        by_id = {a.id: a for a in this}
        rows = ask_pool.run([a.id for a in this], rows,
                            lambda w, pos, aid: ask_one(w, pos, by_id[aid]),
                            live_factory, keep, workers=workers,
                            max_failures=plan.MAX_CONSECUTIVE_FAILURES, outage=Outage)
    rows.sort(key=lambda r: (r["reask"], r["position"]))
    return asks, rows, resumed_at


def first_kept(rows: list[dict]) -> str | None:
    hours = sorted(r["asked_at"] for r in rows if r.get("asked_at"))
    return hours[0] if hours else None


# ---------------------------------------------------------------------------
# What comes before a session
# ---------------------------------------------------------------------------

def refusals_in(path: Path) -> int:
    """The attempts of a session refused for the rate."""
    rec = json.loads(path.read_text())
    return sum(1 for r in rec.get("rows", []) for a in r.get("call_attempts") or []
               if a.get("error") == plan.RATE_LIMITED)


def workers_for(session: str) -> int:
    """§2.4: `plan.WORKERS` at a time, unless the smoke session met a refusal
    for the rate at that concurrency; then one ask at a time."""
    if session == "smoke":
        return plan.WORKERS
    smoke = plan.ask_path("smoke")
    return 1 if smoke.exists() and refusals_in(smoke) else plan.WORKERS


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """The smoke session: both asks valid, every attempt that reached the model
    served by the pinned provider and reasoned. A refusal for the rate is
    counted and not read, and sends the later sessions to one ask at a time."""
    path = path or plan.ask_path("smoke")
    if not path.exists():
        return False, f"no smoke session at {path}; run --session smoke first"
    rec = json.loads(path.read_text())
    rows = rec.get("rows", [])
    firsts = {(r["checkpoint"], r["k"]) for r in rows if r.get("valid")}
    if len(firsts) < plan.SMOKE_ASKS:
        return False, f"{path} holds {len(firsts)} valid asks of {plan.SMOKE_ASKS}"
    attempts = [a for r in rows for a in r.get("call_attempts") or []]
    limited = sum(1 for a in attempts if a.get("error") == plan.RATE_LIMITED)
    reached = [a for a in attempts if a.get("error") != plan.RATE_LIMITED]
    elsewhere = sorted({a.get("provider") or "none" for a in reached} - {plan.PROVIDER_NAME})
    if elsewhere:
        return False, f"{path} holds attempts served by {elsewhere}: the pin did not hold"
    if not all(fm_ask.reasoned(a) for a in reached):
        return False, f"{path} holds an attempt that did not reason, and every one must"
    later = (f"{limited} refusals for the rate at {plan.WORKERS} workers: the later "
             "sessions run one ask at a time" if limited else "no refusal for the rate")
    return True, f"{path}: both asks valid, served by {plan.PROVIDER_NAME}, reasoned; {later}"


def turn_check(session: str) -> tuple[bool, str]:
    """§9's order: the loops' smoke runs, then the smoke session, then `prior`,
    and each L run's session after that run."""
    from . import run as crun      # the loops' checks; run.py does not import this module

    if session == "smoke":
        for arm in plan.SMOKE_ARMS:
            ok, why = crun.smoke_check(arm)
            if not ok:
                return False, why
        return True, "both smoke runs passed; the smoke session comes next"
    ok, why = smoke_check()
    if not ok:
        return False, why
    if session == "prior":
        return True, f"{why}; prior comes next"
    if not plan.ask_path("prior").exists():
        return False, "the prior session comes before any run's"
    src = source_of(session)
    if not src.exists():
        return False, f"no record at {src}; {session} comes after its run"
    return True, f"{src} exists; {session} comes next"


def refuse(what: str, why: str) -> None:
    sys.exit(f"\nREFUSED: {what} — {why}.\n  Nothing was built, spent or written.\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_CORRECTIONS.md: the at-once asks (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run CR-g1 to CR-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.SESSIONS, help="one session, in its turn")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("dry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    session = args.session
    plan.refuse_unsigned(f"corrections/ask.py spends (session {session})")
    ok, why = turn_check(session)
    if not ok:
        refuse(f"session {session}", why)
    print(f"check: {why}")
    ok, why = key_check()
    if not ok:
        refuse("corrections/ask.py", why)
    print(f"key check: {why}")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    target = or_exit(refuse_overwrite, plan.ask_path(session),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))
    src = source_of(session)
    record = None if src is None else json.loads(src.read_text())
    workers = workers_for(session)
    header = protocol_header(session, file_sha256(src), workers)
    partial = plan.ask_partial_path(session)
    started = now()
    print(f"\n{plan.PLAN} · stage B · at-once session {session}: "
          f"{len(design(session, record))} asks, up to {workers} at a time")
    try:
        asks, rows, resumed_at = run_session(session, record, make_worker, partial, header,
                                             workers=workers)
    except STOPS as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before it is kept in "
                 f"{partial}; the same command resumes there.\n")
    out = {"_env": environment(), **header, "stage": "B",
           "system_prompt": prompts.SYSTEM_PROMPT, "header_text": prompts.HEADER,
           "compile_user": prompts.COMPILE_USER,
           "source_record": None if src is None else str(src),
           "labelled": [] if record is None else [list(x) for x in labelled(record)],
           "checkpoints": sorted({a.checkpoint for a in asks}),
           "gates": checks.summary(), "started_at": started,
           "first_kept": first_kept(rows), "resumed_at": resumed_at,
           "finished_at": now(), "rows": rows}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2, default=str))
    partial.unlink()
    valid = sum(1 for r in rows if r["valid"])
    print(f"\n-> {target}\n  {len(rows)} asks, {valid} valid\n  {describe()}")
    if session == "smoke":
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS' if ok else 'FAIL'} · {why}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
