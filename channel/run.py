"""
Stage B of `PLAN_CHANNEL.md`: the runs. **The only module of the plan that
spends.** On the proposer's path: the labels the triggers read are handed to the
loop off `PLAN_REUSE.md`'s first record, the channel arm's draws off their seed
strings, and nothing here imports the policy (rule B of the plan).

THE ORDER OF EVENTS IS THE POINT (§9 of the plan), and nothing that costs is
built before the thing that could forbid it has spoken:

  1. `--dry-run` runs `CH-g1` to `CH-g3` and stops. It never builds a client and
     never needs the key.
  2. The signature (`CH-g4`). While `PLAN_CHANNEL.md` carries a blank signature
     line this module exits here, before the checks, the destination or a
     client. No flag skips it.
  3. What comes before the run: Stage A's record, under this protocol, schedule
     and draws; for a run, the smoke record, with every attempt that reached the
     model served by the pinned provider, reasoned and ended `stop`, a rule born,
     a placement round answered and the trigger's record kept (§2.4); and every
     run before this one in §2.3's order.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`, called
     and not copied. A management key answers 200 there and cannot call a model.
  5. `CH-g1` to `CH-g3`, blocking.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3).

THE PROPOSER, THE ASKER AND THE RESUME ARE `PLAN_REASONED_LOOP.md`'S (§5.3,
rule A): `reasoned_loop.protocol`'s `Resumable` over `Live` over `Asker`, and
`authorship/run.py`'s partial file, called. Every answer is appended as it
arrives, and the same command serves each stored answer after checking that the
request is the one paid for. Five failed calls in a row stop the run without
recording them, because an outage is not answers, and so does a call refused for
the rate through every wait of `plan.RATE_LIMIT_WAIT`. A call served from the
partial file keeps the seconds the file kept (that plan's §5.5 and its two
amendments). The partial file's header carries the channel's draws, so a run
cannot resume under other draws.

    python3 -m channel.run --dry-run
    PYTHONHASHSEED=0 .venv/bin/python -m channel.run --smoke
    PYTHONHASHSEED=0 .venv/bin/python -m channel.run --arm e --rep 1   # §2.3's order; the module says what is next
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
from reasoned_loop import protocol as p
from reasoned_loop.run import reasoned
from reuse.run import key_check
from rung2.engine2 import PriorityEngine, Space

from . import gates, loop, plan, score

Outage, Desync = erun.Outage, erun.Desync


def protocol(arm: str, n: int, name: str, rep: int | None) -> dict[str, Any]:
    """What a run is written under, and what its partial file must have been
    written under to be resumed: `PLAN_REASONED_LOOP.md`'s header, this plan's
    arm, and its channel (rule C)."""
    return json.loads(json.dumps({
        "plan": str(plan.PLAN), "protocol": plan.PROTOCOL, "level": plan.LEVEL,
        "model": plan.MODEL, "temperature": plan.TEMPERATURE, "settings": plan.settings(),
        "provider": plan.PROVIDER, "call_retry_wait": list(plan.CALL_RETRY_WAIT),
        "rate_limit_wait": list(plan.RATE_LIMIT_WAIT),
        "seed": plan.SEED, "n": n, "arm": arm, "run": name, "cap": plan.MAX_ESCALATIONS,
        "listing_seed": bplan.LISTING_SEED, "fingerprint": p.fingerprint(),
        "texts_sha16": p.digests(), **plan.channel_of(arm, rep)}))


def sample_check(path: Path | None = None) -> tuple[bool, str]:
    """Step 3: Stage A's record, under this protocol, this schedule and these
    draws."""
    path = path or plan.sample_path()
    if not path.exists():
        return False, f"no Stage A record at {path}; run channel.sample first"
    refs = json.loads(path.read_text()).get("references", {})
    streams = {name: {"seed": plan.draw_seed(name), "sha16": plan.draws_digest(name)}
               for name in plan.STREAMS}
    if (refs.get("fingerprint") != p.fingerprint()
            or refs.get("schedule") != [list(x) for x in plan.schedule()]
            or (refs.get("draws") or {}).get("streams") != streams):
        return False, f"{path} was not written under this protocol, schedule and draws"
    return True, f"{path}: Stage A's record, under this protocol"


def smoke_check(path: Path | None = None) -> tuple[bool, str]:
    """Step 3, for a run (§2.4): the smoke run under this protocol was served by
    the pinned provider, reasoned on every attempt that reached the model and
    fitted its budget, bore a rule, answered a placement round, and kept the
    trigger's record: every case's draw, and for every wrong decision whether it
    was reported and escalated. An attempt refused for the rate reached nothing:
    it is counted, and not read."""
    path = path or plan.smoke_path()
    if not path.exists():
        return False, f"no smoke record at {path}; run --smoke first"
    rec = json.loads(path.read_text())
    want = protocol(plan.SMOKE_ARM, plan.SMOKE_N, plan.tag(None, None), None)
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
    rows = rec.get("records") or []
    draws = plan.draws(plan.stream(plan.SMOKE_ARM, None))
    if len(rows) != plan.SMOKE_N or not gates.trigger_kept(
            rec, plan.COVERAGE[plan.SMOKE_ARM], draws):
        return False, f"{path} did not keep the trigger's record for every case"
    wrong_decisions = sum(1 for r in rows if r.get("reported") is not None)
    told = sum(1 for r in rows if r.get("reported"))
    return True, (f"{path}: {len(calls)} calls, every attempt that reached the model "
                  f"served by {plan.PROVIDER_NAME}, reasoned and ended `stop`, "
                  f"{limited} refused for the rate and not read; "
                  f"{rec['metrics']['n_rules']} rules born, {placed} placements answered; "
                  f"{wrong_decisions} wrong decisions, {told} reported and escalated")


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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_CHANNEL.md: the loop under a channel (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run CH-g1 to CH-g3 and stop; spends nothing")
    which.add_argument("--smoke", action="store_true",
                       help=f"{plan.SMOKE_N} cases under arm {plan.SMOKE_ARM}, first")
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

    arm = plan.SMOKE_ARM if args.smoke else args.arm
    rep = None if args.smoke else args.rep
    name = plan.tag(None, None) if args.smoke else plan.tag(args.arm, args.rep)
    plan.refuse_unsigned(f"channel/run.py spends (run {name})")

    checks_before = [sample_check] if args.smoke else [
        sample_check, smoke_check, lambda: turn_check(args.arm, args.rep)]
    for check in checks_before:
        ok, why = check()
        if not ok:
            sys.exit(f"\nREFUSED: run {name} — {why}.\n  Nothing was built, spent "
                     "or written.\n")
        print(f"check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: channel/run.py — {why}.\n  Nothing was built, spent "
                 "or written.\n")
    print(f"key check: {why}")

    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was spent.\n")

    target = or_exit(refuse_overwrite,
                     plan.smoke_path() if args.smoke else plan.run_path(args.arm, args.rep),
                     overwrite=args.overwrite_record,
                     exits=(f"{FLAG}    overwrite it — only if Sergi asked for it",))

    n = plan.SMOKE_N if args.smoke else plan.N
    corpus = generate_corpus(n, seed=plan.SEED)
    labels = plan.labels()[:n]
    stream = plan.stream(arm, rep)
    draws = None if stream is None else plan.draws(stream)[:n]
    coverage = plan.COVERAGE[arm]
    header = protocol(arm, n, name, rep)
    partial = plan.partial_path(name)
    rows, resumed = erun.open_partial(partial, header)
    proposer = p.Resumable(p.Live(p.Asker()), partial, rows)
    engine = PriorityEngine(space=Space())
    started = environment()["recorded_at"]
    print(f"\n{plan.PLAN} · stage B · run {name}: {n} cases, arm {arm}, coverage {coverage}, "
          f"with {proposer.name}"
          + (f" · resuming, {len(rows)} answers already paid for" if resumed else ""))
    print("(only escalations cost a call)\n")

    def progress(idx: int, total: int, n_rules: int, n_esc: int) -> None:
        if idx % 25 == 0 or idx == total - 1:
            print(f"  case {idx + 1:>5}/{total}   rules={n_rules:<5} "
                  f"escalations={n_esc:<5} asked={proposer.asked:<5}", end="\r", flush=True)

    try:
        res = loop.run_loop(corpus, labels, engine, proposer, coverage, draws,
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
    print("  (the rows are scored by channel/score.py, not read here)")

    record = {"_env": environment(), **header, "stage": "B",
              "rep": "smoke" if args.smoke else args.rep, "rung": 2,
              "started_at": started, "resumed": resumed,
              "labels_from": str(plan.labels_path()),
              "system_prompt": p.SYSTEM_PROMPT, "blind_base": p.BLIND_BASE,
              "placement_template": p.PLACEMENT_TEMPLATE,
              "gates": checks.summary(), **loop.record_of(res, engine)}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, default=str))
    partial.unlink()
    print(f"\n-> {target}\n  {describe()}")
    if args.smoke:
        ok, why = smoke_check(target)
        pace = score.calls_of(json.loads(target.read_text()))
        print(f"\nsmoke check: {'PASS — the runs may start' if ok else 'FAIL'} · {why}")
        print(f"the pace, by round (§9): {pace['seconds_by_round']}; without the calls "
              f"refused for the rate: {pace['seconds_by_round_unlimited']}")
        return 0 if ok else 1
    nxt = next_run()
    print(f"\nnext run in §2.3's order: "
          f"{f'--arm {nxt[0]} --rep {nxt[1]}' if nxt else 'none: Stage B is complete'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
