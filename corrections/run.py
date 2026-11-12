"""
Stage B of `PLAN_CORRECTIONS.md`, its first half: the smoke runs and the six
runs. **It spends.** On the proposer's path: the labels the trigger reads are
handed to the loop off `PLAN_REUSE.md`'s first record and the draws off
`PLAN_CHANNEL.md`'s seed strings. In arm `l` a reported case's own label reaches
its first call, through `corrections/loop.py` and nowhere else (§4). Nothing here
imports the policy in code.

THE ORDER OF EVENTS IS THE POINT (§9 of the plan), and nothing that costs is
built before the thing that could forbid it has spoken:

  1. `--dry-run` runs `CR-g1` to `CR-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`CR-g4`). While `PLAN_CORRECTIONS.md` carries a blank
     signature line this module exits here, before the checks, the destination
     or a client. No flag skips it.
  3. What comes before (§9):
     - for any run, Stage A's record, under these protocols, this schedule and
       these draws;
     - for L's smoke run, N's: §2.7 asks N first;
     - for a run, both smoke runs and the at-once smoke and prior sessions;
     - every run before it in §2.3's order;
     - the at-once session of every L run before it.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `CR-g1` to `CR-g3`, blocking.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

THE LOOP, THE ESCALATION, THE ASKER AND THE RESUME ARE `PLAN_PLACEMENT.md`'S v1c,
called: `placement.loop.run_loop` with `propose_v1c`, wrapped in arm `l`, over
`reasoned_loop.protocol.Live`, over `placement.protocol.Asker` with its pin, and
`authorship/run.py`'s partial file. The proposer is
`corrections.protocol.Reporting`. Every answer is appended as it arrives, with the
hour it was kept, and the same command serves each stored answer after checking
that the request is the one paid for. Five failed calls in a row stop the run
without recording them, because an outage is not answers, and so does a call
refused for the rate through every wait. A call served from the partial file
keeps the seconds the file kept. The partial file's header carries the arm, the
texts' digests and the draws, so a run cannot resume under another arm or other
draws. A resumed run's report rebuilds itself: the wrapper writes each label
again as the replay reaches its case.

    python3 -m corrections.run --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m corrections.run --smoke --arm n
    PYTHONHASHSEED=0 .venv/bin/python -m corrections.run --smoke --arm l
    PYTHONHASHSEED=0 .venv/bin/python -m corrections.run --arm l --rep 1   # §2.3's order; the module says what is next
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
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from reasoned_loop.run import reasoned
from reuse.run import key_check
from rung2.engine2 import PriorityEngine, Space

from . import gates, loop, plan, protocol

Outage, Desync = erun.Outage, erun.Desync
now = pl_run.now
first_kept = pl_run.first_kept


def protocol_header(arm: str, n: int, name: str, rep: int | None) -> dict[str, Any]:
    """What a run is written under, and what its partial file must have been
    written under to be resumed: `PLAN_PLACEMENT.md`'s header, with this plan,
    level 1, the arm and its texts."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "protocol": "v1c", "level": plan.LEVEL,
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
        return False, f"no Stage A record at {path}; run corrections.sample first"
    refs = json.loads(path.read_text()).get("references", {})
    streams = {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
               for name in plan.STREAMS}
    fingerprints = {arm: protocol.fingerprint(arm) for arm in plan.ARMS}
    if (refs.get("fingerprints") != fingerprints
            or refs.get("schedule") != [list(x) for x in plan.schedule()]
            or refs.get("streams") != streams):
        return False, f"{path} was not written under these protocols, schedule and draws"
    return True, f"{path}: Stage A's record, under these protocols"


def handed_check(rec: dict[str, Any], arm: str) -> tuple[bool, str]:
    """§4's route, read off a record: in arm `l` every escalation caused by a
    reported error was handed its own label, and no other case was; in arm `n`
    no case was handed one."""
    handed = rec.get("reports_handed") or {}
    truth = {r["idx"]: r["truth"] for r in rec["records"]}
    errors = {esc["idx"] for esc in rec["escalations"] if esc["kind"] == plan.ERROR}
    if arm != plan.LABELLED:
        return (not handed, "no case handed a label" if not handed
                else f"{len(handed)} cases handed a label in arm {arm}")
    keys = {int(k) for k in handed}
    if keys != errors:
        return False, (f"labels handed at {len(keys)} cases, and {len(errors)} escalations "
                       "were caused by a reported error")
    wrong = sorted(k for k in keys if handed[str(k)] != truth[k])
    if wrong:
        return False, f"labels that are not their case's at {wrong[:5]}"
    return True, f"each of {len(errors)} reported errors handed its own label"


def smoke_check(arm: str, path: Path | None = None) -> tuple[bool, str]:
    """§2.7: an arm's smoke run was served by the pinned provider, reasoned on
    every attempt that reached the model and fitted its budget, bore a rule,
    answered a placement round, sent the arm's texts, kept the trigger's
    record, and handed labels by §4's route; L's handed at least one. An
    attempt refused for the rate reached nothing: it is counted, and not
    read."""
    path = path or plan.smoke_path(arm)
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke --arm {arm} first"
    rec = json.loads(path.read_text())
    want = protocol_header(arm, plan.SMOKE_N, plan.tag(arm, None), None)
    wrong = sorted(k for k, v in want.items() if rec.get(k) != v)
    if wrong:
        return False, f"{path} was not produced under this protocol: {wrong}"
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
    draws = plan.draws(plan.stream(arm, None))
    if (len(rec.get("records") or []) != plan.SMOKE_N
            or not ch_gates.trigger_kept(rec, plan.COVERAGE, draws)):
        return False, f"{path} did not keep the trigger's record for every case"
    ok, why = handed_check(rec, arm)
    if not ok:
        return False, f"{path}: {why}"
    if arm == plan.LABELLED and not rec.get("reports_handed"):
        return False, f"{path} handed no label: L's smoke run must exercise the route"
    return True, (f"{path}: {len(calls)} calls, every attempt that reached the model "
                  f"served by {plan.PROVIDER_NAME}, reasoned and ended `stop`, "
                  f"{limited} refused for the rate and not read; "
                  f"{rec['metrics']['n_rules']} rules born, {placed} placements answered; "
                  f"{why}")


def sessions_before(arm: str, rep: int) -> list[str]:
    """The at-once sessions a run comes after: the smoke and prior sessions, and
    the session of every L run before it in §2.3's order."""
    out = ["smoke", "prior"]
    for a, r in plan.schedule():
        if (a, r) == (arm, rep):
            break
        if a == plan.LABELLED:
            out.append(plan.session_of(r))
    return out


def turn_check(arm: str, rep: int) -> tuple[bool, str]:
    """§2.3 and §9: the runs in their order, each L run's session after it."""
    for s in sessions_before(arm, rep):
        if not plan.ask_path(s).exists():
            return False, f"the at-once session {s} comes before run {arm} r{rep}"
    for a, r in plan.schedule():
        if (a, r) == (arm, rep):
            return True, f"run {arm} r{rep} is next in §2.3's order"
        if not plan.run_path(a, r).exists():
            return False, f"run {a} r{r} comes before {arm} r{rep} in §2.3's order"
    return False, f"no run {arm} r{rep} in the schedule"


def next_step() -> str:
    """What §9's order asks for next."""
    for arm in plan.SMOKE_ARMS:
        if not plan.smoke_path(arm).exists():
            return f"corrections.run --smoke --arm {arm}"
    for s in ("smoke", "prior"):
        if not plan.ask_path(s).exists():
            return f"corrections.ask --session {s}"
    for a, r in plan.schedule():
        if not plan.run_path(a, r).exists():
            return f"corrections.run --arm {a} --rep {r}"
        if a == plan.LABELLED and not plan.ask_path(plan.session_of(r)).exists():
            return f"corrections.ask --session {plan.session_of(r)}"
    return "none: the runs and the asks are complete; Stage C next"


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
        refuse("corrections/run.py", why)
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
    arm, rep = args.arm, (None if args.smoke else args.rep)
    name = plan.tag(arm, rep)
    target = or_exit(refuse_overwrite,
                     plan.smoke_path(arm) if args.smoke else plan.run_path(arm, rep),
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
    print(f"\n{plan.PLAN} · stage B · run {name}: {n} cases, arm {arm}, level {plan.LEVEL}, "
          f"coverage {plan.COVERAGE}, with {proposer.name}"
          + (f" · resuming, {len(rows)} answers already paid for" if resumed else ""))
    print("(only escalations cost a call)\n")

    def progress(idx: int, total: int, n_rules: int, n_esc: int) -> None:
        if idx % 25 == 0 or idx == total - 1:
            print(f"  case {idx + 1:>5}/{total}   rules={n_rules:<5} "
                  f"escalations={n_esc:<5} asked={proposer.asked:<5}", end="\r", flush=True)

    try:
        res = loop.run_loop(corpus, labels, engine, proposer, arm, draws,
                            on_progress=progress)
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
    print("  (the rows are scored by corrections/score.py, not read here)")

    record = {"_env": environment(), **header, "stage": "B",
              "rep": "smoke" if args.smoke else rep, "rung": 2,
              "started_at": started, "first_kept": first_kept(partial), "resumed": resumed,
              "labels_from": str(plan.labels_path()),
              "system_prompt": protocol.SYSTEM_PROMPT, "base_text": protocol.BLIND_BASE,
              "report_template": protocol.REPORT if arm == plan.LABELLED else None,
              "placement_template": protocol.PLACEMENT_TEMPLATE,
              "reports_handed": loop.reports_handed(proposer),
              "gates": checks.summary(), **loop.record_of(res, engine)}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, default=str))
    partial.unlink()
    print(f"\n-> {target}\n  {describe()}")
    ok, why = handed_check(json.loads(target.read_text()), arm)
    print(f"\nthe label's route: {'PASS' if ok else 'FAIL'} · {why}")
    if args.smoke:
        ok2, why2 = smoke_check(arm, target)
        print(f"smoke check: {'PASS' if ok2 else 'FAIL'} · {why2}")
        ok = ok and ok2
    print(f"\nnext in §9's order: {next_step()}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_CORRECTIONS.md: the loops, with and without the label "
                    "(spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run CR-g1 to CR-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases of one arm, N first; --arm says which")
    which.add_argument("--rep", type=int, choices=range(1, plan.REPS + 1),
                       help="the repetition of one run; --arm says which arm")
    ap.add_argument("--arm", choices=plan.ARMS)
    ap.add_argument(FLAG, dest="overwrite_record", action="store_true",
                    help="overwrite a paid record — only if Sergi asked for it")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print(f"\nnext in §9's order: {next_step()}")
        print("dry run: no client built, no call made, nothing written")
        return 0 if checks.blocking_pass else 1
    if args.arm is None:
        ap.error("--smoke and --rep need --arm")

    name = plan.tag(args.arm, None if args.smoke else args.rep)
    plan.refuse_unsigned(f"corrections/run.py spends (run {name})")
    if args.smoke:
        checks_before = [sample_check]
        if args.arm == plan.LABELLED:
            checks_before.append(lambda: smoke_check(plan.SMOKE_ARMS[0]))
    else:
        checks_before = [sample_check, *(lambda a=a: smoke_check(a) for a in plan.SMOKE_ARMS),
                         lambda: turn_check(args.arm, args.rep)]
    checks = before(f"run {name}", checks_before)
    return a_run(args, checks)


if __name__ == "__main__":
    sys.exit(main())
