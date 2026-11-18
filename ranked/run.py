"""
Stage B of `PLAN_RANKED.md`, its first half: the smoke runs and the six runs.
**It spends.** On the proposer's path: the labels the trigger reads are handed
to the loop off `PLAN_REUSE.md`'s first record and the draws off
`PLAN_CHANNEL.md`'s seed strings. In both arms a reported case's own label
reaches its first call, through `corrections/loop.py` and nowhere else (§4).
Nothing here imports the policy in code.

THE ORDER OF EVENTS IS THE POINT (§9 of the plan), and nothing that costs is
built before the thing that could forbid it has spoken:

  1. `--dry-run` runs `RK-g1` to `RK-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`RK-g4`). While `PLAN_RANKED.md` carries a blank signature
     line this module exits here, before the checks, the destination or a
     client. No flag skips it.
  3. What comes before (§9):
     - for any run, Stage A's record, under these protocols, this schedule and
       these draws;
     - for K's smoke run, L's: §2.9 asks L first;
     - for a run, both smoke runs and the at-once smoke and prior sessions;
     - every run before it in §2.5's order, and the at-once session of each.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `RK-g1` to `RK-g3`, blocking.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

THE LOOP, THE ESCALATION, THE PROPOSER, THE ASKER AND THE RESUME ARE
`PLAN_CORRECTIONS.md`'S ARM L'S, called: `corrections.loop.run_loop` over
`corrections.protocol.Reporting`, over `reasoned_loop.protocol.Live`, over
`placement.protocol.Asker` with its pin, and `authorship/run.py`'s partial file.
Every answer is appended as it arrives, with the hour it was kept, and the same
command serves each stored answer after checking that the request is the one
paid for. Five failed calls in a row stop the run without recording them, and so
does a call refused for the rate through every wait. A call served from the
partial file keeps the seconds the file kept.

WHAT IS THIS PLAN'S is the engine each arm's loop is handed (`ranked/loop.py`).
The partial file's header carries the arm and its engine's rule, so a run cannot
resume under the other arm. **A resumed K run rebuilds its ranking**: the replay
passes the same births with the same citations, and the engine counts them
again.

    python3 -m ranked.run --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m ranked.run --smoke --arm l
    PYTHONHASHSEED=0 .venv/bin/python -m ranked.run --smoke --arm k
    PYTHONHASHSEED=0 .venv/bin/python -m ranked.run --arm l --rep 1   # §2.5's order; the module says what is next
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
from corrections import protocol as cr_protocol
from corrections import run as cr_run
from placement import protocol as pl_protocol
from placement import run as pl_run
from reasoned_loop import protocol as p
from reasoned_loop.run import reasoned
from reuse.run import key_check
from rung2.engine2 import Space

from . import engine as E
from . import gates, loop, plan

Outage, Desync = erun.Outage, erun.Desync
now = pl_run.now
first_kept = pl_run.first_kept


def engine_rule(arm: str) -> dict[str, str] | None:
    """The ranked engine's rule, as a record's header carries it; none in arm
    `l`."""
    if arm != plan.RANKED:
        return None
    return {"vote": plan.VOTE, "tie": plan.TIE, "decides": plan.DECIDES}


def protocol_header(arm: str, n: int, name: str, rep: int | None) -> dict[str, Any]:
    """What a run is written under, and what its partial file must have been
    written under to be resumed: `PLAN_CORRECTIONS.md`'s arm L's header, with
    this plan, the arm and its engine."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "protocol": "v1c", "level": plan.LEVEL,
        "engine": plan.ENGINE[arm], "engine_rule": engine_rule(arm),
        "model": plan.MODEL, "temperature": plan.TEMPERATURE, "settings": plan.settings(),
        "provider": plan.PROVIDER, "call_retry_wait": list(plan.CALL_RETRY_WAIT),
        "rate_limit_wait": list(plan.RATE_LIMIT_WAIT),
        "seed": plan.SEED, "n": n, "arm": arm, "run": name, "cap": plan.MAX_ESCALATIONS,
        "listing_seed": bplan.LISTING_SEED,
        "fingerprint": cr_protocol.fingerprint(plan.TEXTS_OF),
        "texts_sha16": cr_protocol.digests(plan.TEXTS_OF), **plan.channel_of(arm, rep)}))


# ---------------------------------------------------------------------------
# What comes before (step 3)
# ---------------------------------------------------------------------------

def sample_check(path: Path | None = None) -> tuple[bool, str]:
    """Stage A's record, under these protocols, this schedule and these draws."""
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run ranked.sample first"
    refs = json.loads(path.read_text()).get("references", {})
    streams = {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
               for name in plan.STREAMS}
    if (refs.get("fingerprint") != cr_protocol.fingerprint(plan.TEXTS_OF)
            or refs.get("engines") != {a: {"engine": plan.ENGINE[a], "rule": engine_rule(a)}
                                       for a in plan.ARMS}
            or refs.get("schedule") != [list(x) for x in plan.schedule()]
            or refs.get("streams") != streams):
        return False, f"{path} was not written under these protocols, schedule and draws"
    return True, f"{path}: Stage A's record, under these protocols"


def handed_check(rec: dict[str, Any]) -> tuple[bool, str]:
    """§4's route, read off a record of either arm: every escalation caused by a
    reported error was handed its own label, and no other case was."""
    return cr_run.handed_check(rec, plan.TEXTS_OF)


def ranked_check(rec: dict[str, Any]) -> tuple[bool, str]:
    """What arm `k`'s record keeps of its engine is what its own rules give:
    fed the record's births in order, the count takes the rankings the log keeps
    and ends where the record ends. Every case has its row, none was a CONFLICT,
    and the ranking decided only cases the record decided. Arm `l`'s record
    keeps nothing of it."""
    kept = rec.get("ranked")
    if rec.get("arm") != plan.RANKED:
        return (kept is None, "arm l keeps no ranking" if kept is None
                else "arm l's record keeps a ranking")
    if not kept:
        return False, "arm k's record keeps no ranking"
    again = E.tally_of(rec)
    if again.log != kept["log"]:
        return False, "the ranking log is not what the record's births give"
    final = again.final()
    if final != kept["final"]:
        return False, "the final ranking is not what the record's births give"
    rows, cases = rec["records"], kept["cases"]
    if len(cases) != len(rows):
        return False, f"{len(cases)} logged cases for {len(rows)} cases read"
    conflicts = sum(1 for r in rows if r["outcome"] == plan.CONFLICT)
    if conflicts:
        return False, f"{conflicts} cases were a CONFLICT under arm k's engine"
    taken = [r for r, c in zip(rows, cases) if c["by"] == E.RANKING]
    if any(r["outcome"] != "ACTION" for r in taken):
        return False, "the ranking is logged at a case the record did not decide"
    return True, (f"the ranking after each of {len(kept['log'])} births, and the final one, "
                  f"are what the record's births give; {final['n_votes']} votes; the ranking "
                  f"decided {len(taken)} cases")


def smoke_check(arm: str, path: Path | None = None) -> tuple[bool, str]:
    """§2.9: an arm's smoke run was served by the pinned provider, reasoned on
    every attempt that reached the model and fitted its budget, bore a rule,
    answered a placement round, sent the arm's texts, kept the trigger's
    record, and handed labels by §4's route; L's handed at least one. K's cast
    at least one vote, and its record of the engine is what its births give. An
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
    ok, why = handed_check(rec)
    if not ok:
        return False, f"{path}: {why}"
    if arm == plan.CONTROL and not rec.get("reports_handed"):
        return False, f"{path} handed no label: L's smoke run must exercise the route"
    ok, engine_why = ranked_check(rec)
    if not ok:
        return False, f"{path}: {engine_why}"
    if arm == plan.RANKED and rec["ranked"]["final"]["n_votes"] < 1:
        return False, f"{path} cast no vote: K's smoke run must exercise the engine"
    return True, (f"{path}: {len(calls)} calls, every attempt that reached the model "
                  f"served by {plan.PROVIDER_NAME}, reasoned and ended `stop`, "
                  f"{limited} refused for the rate and not read; "
                  f"{rec['metrics']['n_rules']} rules born, {placed} placements answered; "
                  f"{why}; {engine_why}")


def sessions_before(arm: str, rep: int) -> list[str]:
    """The at-once sessions a run comes after: the smoke and prior sessions, and
    the session of every run before it in §2.5's order."""
    out = ["smoke", "prior"]
    for a, r in plan.schedule():
        if (a, r) == (arm, rep):
            break
        out.append(plan.session_of(a, r))
    return out


def turn_check(arm: str, rep: int) -> tuple[bool, str]:
    """§2.5 and §9: the runs in their order, each run's session after it."""
    for s in sessions_before(arm, rep):
        if not plan.ask_path(s).exists():
            return False, f"the at-once session {s} comes before run {arm} r{rep}"
    for a, r in plan.schedule():
        if (a, r) == (arm, rep):
            return True, f"run {arm} r{rep} is next in §2.5's order"
        if not plan.run_path(a, r).exists():
            return False, f"run {a} r{r} comes before {arm} r{rep} in §2.5's order"
    return False, f"no run {arm} r{rep} in the schedule"


def next_step() -> str:
    """What §9's order asks for next."""
    for arm in plan.SMOKE_ARMS:
        if not plan.smoke_path(arm).exists():
            return f"ranked.run --smoke --arm {arm}"
    for s in ("smoke", "prior"):
        if not plan.ask_path(s).exists():
            return f"ranked.ask --session {s}"
    for a, r in plan.schedule():
        if not plan.run_path(a, r).exists():
            return f"ranked.run --arm {a} --rep {r}"
        if not plan.ask_path(plan.session_of(a, r)).exists():
            return f"ranked.ask --session {plan.session_of(a, r)}"
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
        refuse("ranked/run.py", why)
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
    proposer = cr_protocol.PROPOSERS[plan.TEXTS_OF](p.Live(pl_protocol.Asker()), partial, rows)
    space = Space()
    engine = loop.engine_for(arm, space)
    started = now()
    print(f"\n{plan.PLAN} · stage B · run {name}: {n} cases, arm {arm}, engine "
          f"{plan.ENGINE[arm]}, level {plan.LEVEL}, coverage {plan.COVERAGE}, with "
          f"{proposer.name}"
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
    print("  (the rows are scored by ranked/score.py, not read here)")

    record = {"_env": environment(), **header, "stage": "B",
              "rep": "smoke" if args.smoke else rep, "rung": 2,
              "started_at": started, "first_kept": first_kept(partial), "resumed": resumed,
              "labels_from": str(plan.labels_path()),
              "system_prompt": cr_protocol.SYSTEM_PROMPT, "base_text": cr_protocol.BLIND_BASE,
              "report_template": cr_protocol.REPORT,
              "placement_template": cr_protocol.PLACEMENT_TEMPLATE,
              "reports_handed": loop.reports_handed(proposer),
              "ranked": loop.ranked_part(engine),
              "gates": checks.summary(), **loop.record_of(res, engine)}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, default=str))
    partial.unlink()
    print(f"\n-> {target}\n  {describe()}")
    written = json.loads(target.read_text())
    ok, why = handed_check(written)
    print(f"\nthe label's route: {'PASS' if ok else 'FAIL'} · {why}")
    ok1, why1 = ranked_check(written)
    print(f"the engine's record: {'PASS' if ok1 else 'FAIL'} · {why1}")
    ok = ok and ok1
    if args.smoke:
        ok2, why2 = smoke_check(arm, target)
        print(f"smoke check: {'PASS' if ok2 else 'FAIL'} · {why2}")
        ok = ok and ok2
    print(f"\nnext in §9's order: {next_step()}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_RANKED.md: the loops, under rung 2's order and under "
                    "the ranking (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run RK-g1 to RK-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases of one arm, L first; --arm says which")
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
    plan.refuse_unsigned(f"ranked/run.py spends (run {name})")
    if args.smoke:
        checks_before = [sample_check]
        if args.arm != plan.SMOKE_ARMS[0]:
            checks_before.append(lambda: smoke_check(plan.SMOKE_ARMS[0]))
    else:
        checks_before = [sample_check, *(lambda a=a: smoke_check(a) for a in plan.SMOKE_ARMS),
                         lambda: turn_check(args.arm, args.rep)]
    checks = before(f"run {name}", checks_before)
    return a_run(args, checks)


if __name__ == "__main__":
    sys.exit(main())
