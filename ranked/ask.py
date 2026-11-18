"""
Stage B of `PLAN_RANKED.md`, its second half: the at-once asks (§2.6). **It
spends.** On the proposer's path in the sense `tests/test_oracle_separation.py`
watches: it sends level 1's catalogue, and the labels a run's proposer was
handed, read off that run's own record. Nothing here imports the policy in code
(§4).

THE ASKS ARE `PLAN_CORRECTIONS.md` §2.4's, called and not retyped: the compile
prompt, the header, the lines, the request with its budget, the validity of an
answer, the re-asks, the ask pool with its four workers and its breaker, and the
client, `corrections.ask.AtOnceAsker` behind `reasoned_loop.protocol.Live`.

WHAT IS THIS PLAN'S is the list of sessions, each a record of its own, in this
order (§9):

  smoke        two asks: one with no label, one on L's smoke run's labels;
  prior        five asks with no label, right after the smoke session;
  <arm>_r<k>   after run `k` of an arm and before the next run: three asks at
               each checkpoint the run reaches, and three at all of its labels.

Every run of either arm has a session. `RK-d` reads K's; L's are reported.

THE ORDER OF EVENTS, as `ranked/run.py`'s: the signature, what comes before, the
key, the blocking checks, the destination, and only then the client.

    python3 -m ranked.ask --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m ranked.ask --session smoke
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from harness import ask_pool
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from authorship import run as erun
from corrections import ask as cr_ask
from corrections import prompts as cr_prompts
from reuse.run import key_check

from . import gates, plan

Ask = cr_ask.Ask
ask_id = cr_ask.ask_id
labelled = cr_ask.labelled
NotHanded = cr_ask.NotHanded
reasks = cr_ask.reasks
ask_one = cr_ask.ask_one
make_worker = cr_ask.make_worker
file_sha256 = cr_ask.file_sha256
first_kept = cr_ask.first_kept
refusals_in = cr_ask.refusals_in
Outage, STOPS = cr_ask.Outage, cr_ask.STOPS
now = cr_ask.now


# ---------------------------------------------------------------------------
# The design of a session
# ---------------------------------------------------------------------------

def source_of(session: str) -> Path | None:
    """The record a session reads its labels off: L's smoke run for `smoke`,
    none for `prior`, and its own run for a run's session."""
    if session not in plan.sessions():
        raise ValueError(f"no session {session!r}: {plan.sessions()}")
    if session == "smoke":
        return plan.smoke_path(plan.CONTROL)
    if session == "prior":
        return None
    arm, rep = session.split("_r")
    return plan.run_path(arm, int(rep))


def design(session: str, record: dict[str, Any] | None = None) -> list[Ask]:
    """The first pass of a session's asks, in order (§2.6)."""
    if session not in plan.sessions():
        raise ValueError(f"no session {session!r}: {plan.sessions()}")
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
        "source_sha256": source_sha256, "texts_sha16": cr_prompts.digests()}))


def run_session(session: str, record: dict[str, Any] | None, live_factory, partial: Path,
                header: dict[str, Any], workers: int = plan.WORKERS) -> tuple[list, list, list]:
    """Every pass of a session: the first, then up to `plan.MAX_REASKS` passes
    of the asks still without a valid answer. Returns the asks, the rows and
    the hours it resumed at. `corrections.ask.run_session`, over this plan's
    sessions."""
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


# ---------------------------------------------------------------------------
# What comes before a session
# ---------------------------------------------------------------------------

def workers_for(session: str) -> int:
    """§2.6: `plan.WORKERS` at a time, unless the smoke session met a refusal
    for the rate at that concurrency; then one ask at a time."""
    if session == "smoke":
        return plan.WORKERS
    smoke = plan.ask_path("smoke")
    return 1 if smoke.exists() and refusals_in(smoke) else plan.WORKERS


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """The smoke session, read as `corrections.ask.smoke_check` reads its own."""
    return cr_ask.smoke_check(path or plan.ask_path("smoke"))


def turn_check(session: str) -> tuple[bool, str]:
    """§9's order: the loops' smoke runs, then the smoke session, then `prior`,
    and each run's session after that run."""
    from . import run as rrun      # the loops' checks; run.py does not import this module

    if session == "smoke":
        for arm in plan.SMOKE_ARMS:
            ok, why = rrun.smoke_check(arm)
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
        description="Stage B of PLAN_RANKED.md: the at-once asks (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run RK-g1 to RK-g3 and stop; spends nothing")
    which.add_argument("--session", choices=plan.sessions(), help="one session, in its turn")
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("dry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1

    session = args.session
    plan.refuse_unsigned(f"ranked/ask.py spends (session {session})")
    ok, why = turn_check(session)
    if not ok:
        refuse(f"session {session}", why)
    print(f"check: {why}")
    ok, why = key_check()
    if not ok:
        refuse("ranked/ask.py", why)
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
           "system_prompt": cr_prompts.SYSTEM_PROMPT, "header_text": cr_prompts.HEADER,
           "compile_user": cr_prompts.COMPILE_USER,
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
