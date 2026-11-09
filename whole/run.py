"""
Stage B of `PLAN_WHOLE.md`: the smoke run and the six runs. **The only module of
the plan that spends.** On the proposer's path: the labels the trigger reads are
handed to the loop off `PLAN_REUSE.md`'s first record, the draws off
`PLAN_CHANNEL.md`'s seed strings, and nothing here imports the policy (rule B of
the plan).

THE ORDER OF EVENTS IS THE POINT (§9 of the plan), and nothing that costs is
built before the thing that could forbid it has spoken:

  1. `--dry-run` runs `WR-g1` to `WR-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`WR-g4`). While `PLAN_WHOLE.md` carries a blank signature
     line this module exits here, before the checks, the destination or a
     client. No flag skips it.
  3. What comes before: Stage A's record, under these protocols, this schedule
     and these draws; for a run, the smoke record, with every attempt that
     reached the model served by the pinned provider, reasoned and ended `stop`,
     a rule born, a placement round answered, v1d's texts sent and the
     trigger's record kept (§2.4); and every run before it in §2.3's order.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `WR-g1` to `WR-g3`, blocking.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

THE LOOP, THE ESCALATION, THE ASKER AND THE RESUME ARE `PLAN_PLACEMENT.md`'S v1c
(§5, rule A), called: `placement.loop.run_loop` with `propose_v1c`, over
`reasoned_loop.protocol.Live`, over `placement.protocol.Asker` with its pin, and
`authorship/run.py`'s partial file. The proposer is `whole.protocol.PROPOSERS`'s:
`placement.run.Stamped` for v1c, and its subclass for v1d, whose two calls send
v1d's messages. Every answer is appended as it arrives, with the hour it was
kept, and the same command serves each stored answer after checking that the
request is the one paid for. Five failed calls in a row stop the run without
recording them, because an outage is not answers, and so does a call refused for
the rate through every wait. A call served from the partial file keeps the
seconds the file kept. The partial file's header carries the protocol, the
texts' digests and the draws, so a run cannot resume under another arm or other
draws. A record keeps the hour of the first answer the run kept, so that a
resumed run's span is taken from its first launch.

    python3 -m whole.run --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m whole.run --smoke
    PYTHONHASHSEED=0 .venv/bin/python -m whole.run --arm v1c --rep 1   # §2.3's order; the module says what is next
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from authorship import run as erun
from blind import plan as bplan
from channel import gates as ch_gates
from placement import loop as pl_loop
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from reasoned_loop.run import reasoned
from reuse.run import key_check
from rung2.engine2 import PriorityEngine, Space

from . import gates, plan, protocol

Outage, Desync = erun.Outage, erun.Desync
now = pl_run.now
first_kept = pl_run.first_kept


def protocol_header(arm: str, n: int, name: str, rep: int | None) -> dict[str, Any]:
    """What a run is written under, and what its partial file must have been
    written under to be resumed: `PLAN_PLACEMENT.md`'s header, with this plan,
    the arm's protocol and its texts (rule C)."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "protocol": arm, "level": plan.LEVEL,
        "model": plan.MODEL, "temperature": plan.TEMPERATURE, "settings": plan.settings(),
        "provider": plan.PROVIDER, "call_retry_wait": list(plan.CALL_RETRY_WAIT),
        "rate_limit_wait": list(plan.RATE_LIMIT_WAIT),
        "seed": plan.SEED, "n": n, "arm": arm, "run": name, "cap": plan.MAX_ESCALATIONS,
        "listing_seed": bplan.LISTING_SEED, "fingerprint": protocol.fingerprint(arm),
        "texts_sha16": protocol.digests(arm), **plan.channel_of(arm, rep)}))


# ---------------------------------------------------------------------------
# What comes before (step 3)
# ---------------------------------------------------------------------------

def sample_check(path: Path | None = None) -> tuple[bool, str]:
    """Stage A's record, under these protocols, this schedule and these draws."""
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run whole.sample first"
    refs = json.loads(path.read_text()).get("references", {})
    streams = {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
               for name in plan.STREAMS}
    fingerprints = {arm: protocol.fingerprint(arm) for arm in plan.ARMS}
    if (refs.get("fingerprints") != fingerprints
            or refs.get("schedule") != [list(x) for x in plan.schedule()]
            or refs.get("streams") != streams):
        return False, f"{path} was not written under these protocols, schedule and draws"
    return True, f"{path}: Stage A's record, under these protocols"


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """§2.4: the smoke run under v1d was served by the pinned provider, reasoned
    on every attempt that reached the model and fitted its budget, bore a rule,
    answered a placement round, sent v1d's texts, and kept the trigger's record.
    An attempt refused for the rate reached nothing: it is counted, and not
    read."""
    path = path or plan.smoke_path()
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke first"
    rec = json.loads(path.read_text())
    want = protocol_header(plan.SMOKE_ARM, plan.SMOKE_N, plan.tag(None, None), None)
    wrong = sorted(k for k, v in want.items() if rec.get(k) != v)
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
    if rec.get("base_text") != protocol.BASES[plan.SMOKE_ARM]:
        return False, f"{path} did not send v1d's paragraph"
    calls = [c for esc in rec.get("escalations", []) for c in esc.get("calls", [])]
    pairs = [(a, c) for c in calls for a in c.get("call_attempts") or []]
    limited = sum(1 for a, _ in pairs if a.get("error") == plan.RATE_LIMITED)
    pairs = [(a, c) for a, c in pairs if a.get("error") != plan.RATE_LIMITED]
    if not pairs:
        return False, f"{path} recorded no attempt that reached the model"
    elsewhere = sorted({a.get("provider") or "none" for a, _ in pairs} - {plan.PROVIDER_NAME})
    if elsewhere:
        return False, f"{path} has attempts served by {elsewhere}, not {plan.PROVIDER_NAME}"
    if not all(reasoned(a, c) for a, c in pairs):
        return False, f"an attempt in {path} did not reason, and every call must"
    if any(a.get("finish_reason") != "stop" for a, _ in pairs):
        return False, f"an attempt in {path} did not end `stop`: the budget must fit"
    if rec.get("metrics", {}).get("n_rules", 0) < 1:
        return False, f"no rule was born in {path}"
    placed = sum(1 for c in calls if c["round"] == 1 and c["failure"] is None)
    if placed < 1:
        return False, f"no placement round was answered in {path}"
    rows = rec.get("records") or []
    draws = plan.draws(plan.stream(plan.SMOKE_ARM, None))
    if len(rows) != plan.SMOKE_N or not ch_gates.trigger_kept(rec, plan.COVERAGE, draws):
        return False, f"{path} did not keep the trigger's record for every case"
    return True, (f"{path}: {len(calls)} calls, every attempt that reached the model "
                  f"served by {plan.PROVIDER_NAME}, reasoned and ended `stop`, "
                  f"{limited} refused for the rate and not read; "
                  f"{rec['metrics']['n_rules']} rules born, {placed} placements answered")


def turn_check(arm: str, rep: int) -> tuple[bool, str]:
    """§2.3 and rule F: the runs in their order."""
    for a, r in plan.schedule():
        if (a, r) == (arm, rep):
            return True, f"run {arm} r{rep} is next in §2.3's order"
        if not plan.run_path(a, r).exists():
            return False, f"run {a} r{r} comes before {arm} r{rep} in §2.3's order"
    return False, f"no run {arm} r{rep} in the schedule"


def next_run() -> tuple[str, int] | None:
    for a, r in plan.schedule():
        if not plan.run_path(a, r).exists():
            return a, r
    return None


def refuse(what: str, why: str) -> None:
    sys.exit(f"\nREFUSED: {what} — {why}.\n  Nothing was built, spent or written.\n")


def before(what: str, checks_before) -> gates.Checks:
    """Steps 3 to 5: what comes before, the key and the blocking checks."""
    for check in checks_before:
        ok, why = check()
        if not ok:
            refuse(what, why)
        print(f"check: {why}")
    ok, why = key_check()
    if not ok:
        refuse("whole/run.py", why)
    print(f"key check: {why}")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")
    return checks


# ---------------------------------------------------------------------------
# A run (§9)
# ---------------------------------------------------------------------------

def a_run(args, checks: gates.Checks) -> int:
    arm = plan.SMOKE_ARM if args.smoke else args.arm
    rep = None if args.smoke else args.rep
    name = plan.tag(None, None) if args.smoke else plan.tag(args.arm, args.rep)
    target = or_exit(refuse_overwrite,
                     plan.smoke_path() if args.smoke else plan.run_path(args.arm, args.rep),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))
    n = plan.SMOKE_N if args.smoke else plan.N
    corpus = generate_corpus(n, seed=plan.SEED)
    labels = plan.labels()[:n]
    draws = plan.draws(plan.stream(arm, rep))[:n]
    header = protocol_header(arm, n, name, rep)
    partial = plan.partial_path(name)
    rows, resumed = erun.open_partial(partial, header)
    proposer = protocol.PROPOSERS[arm](p.Live(pl_protocol.Asker()), partial, rows)
    engine = PriorityEngine(space=Space())
    started = now()
    print(f"\n{plan.PLAN} · stage B · run {name}: {n} cases, protocol {arm}, coverage "
          f"{plan.COVERAGE}, with {proposer.name}"
          + (f" · resuming, {len(rows)} answers already paid for" if resumed else ""))
    print("(only escalations cost a call)\n")

    def progress(idx: int, total: int, n_rules: int, n_esc: int) -> None:
        if idx % 25 == 0 or idx == total - 1:
            print(f"  case {idx + 1:>5}/{total}   rules={n_rules:<5} "
                  f"escalations={n_esc:<5} asked={proposer.asked:<5}", end="\r", flush=True)

    try:
        res = pl_loop.run_loop(corpus, labels, engine, proposer, plan.COVERAGE, draws,
                               propose=pl_loop.ESCALATIONS["v1c"], on_progress=progress)
    except (Outage, Desync) as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before it is kept in "
                 f"{partial}; the same command resumes there.\n")
    proposer.flush()
    print("\n")
    m, v = res.loop.run.metrics, res.summary()
    for k in ("n_rules", "escalations", "conflicts", "failed_proposals", "rejected_rules"):
        print(f"  {k:<24}{m.get(k)}")
    print(f"  {'calls':<24}{res.loop.calls}")
    print(f"  {'stopped at the cap':<24}{v['stopped_at']}")
    print("  (the rows are scored by whole/score.py, not read here)")

    record = {"_env": environment(), **header, "stage": "B",
              "rep": "smoke" if args.smoke else args.rep, "rung": 2,
              "started_at": started, "first_kept": first_kept(partial), "resumed": resumed,
              "labels_from": str(plan.labels_path()),
              "system_prompt": p.SYSTEM_PROMPT, "base_text": protocol.BASES[arm],
              "placement_template": p.PLACEMENT_TEMPLATE,
              "gates": checks.summary(), **pl_loop.record_of(res, engine)}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, default=str))
    partial.unlink()
    print(f"\n-> {target}\n  {describe()}")
    if args.smoke:
        ok, why = smoke_check(target)
        print(f"\nsmoke check: {'PASS — the runs may start' if ok else 'FAIL'} · {why}")
        return 0 if ok else 1
    nxt = next_run()
    print(f"\nnext run in §2.3's order: "
          f"{f'--arm {nxt[0]} --rep {nxt[1]}' if nxt else 'none: the runs are complete'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_WHOLE.md: the first call asked for the region whole "
                    "(spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run WR-g1 to WR-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases under {plan.SMOKE_ARM}, first")
    which.add_argument("--arm", choices=plan.ARMS, help="the arm of one run; --rep says which")
    ap.add_argument("--rep", type=int, choices=range(1, plan.REPS + 1))
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        nxt = next_run()
        print(f"\nnext run in §2.3's order: {f'--arm {nxt[0]} --rep {nxt[1]}' if nxt else 'none'}")
        print("dry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1
    if args.arm is not None and args.rep is None:
        ap.error("--arm needs --rep")

    name = plan.tag(None, None) if args.smoke else plan.tag(args.arm, args.rep)
    plan.refuse_unsigned(f"whole/run.py spends (run {name})")
    checks_before = [sample_check] if args.smoke else [
        sample_check, smoke_check, lambda: turn_check(args.arm, args.rep)]
    checks = before(f"run {name}", checks_before)
    return a_run(args, checks)


if __name__ == "__main__":
    sys.exit(main())
