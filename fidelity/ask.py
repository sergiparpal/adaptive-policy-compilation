"""
Stage B of `PLAN_FIDELITY.md`: the calls. **The only module of the plan that
spends.**

It asks the model prompt v1 on prompts rebuilt from PLAN_REUSE.md's Stage B
records. The client is Stage B's, unchanged:
`OpenRouterProposer2(model, prompt_version="v1", reasoning={"effort": "none"})`,
whose `propose` is called exactly as rung 2's loop calls it (rule A of the
plan). What the model writes beyond its `action` is recorded and never executed
(rule E). No rule it writes enters any engine.

THE ORDER OF EVENTS IS THE POINT, and nothing that costs is built before the
thing that could forbid it has spoken (§8 of the plan):

  1. `--dry-run` runs `F-g1` to `F-g3` and stops. It never builds the client and
     never needs the key.
  2. The signature (`F-g4`). While `PLAN_FIDELITY.md` carries a blank signature
     line this module exits here, before the checks, the destination or the
     client. No flag skips it.
  3. For every session but the smoke run: a smoke record under this plan's
     protocol (model, prompt, reasoning setting, seed) holding at least one
     valid answer of each kind of prompt the session will ask.
  4. The key, read off OpenRouter's key endpoint by `reuse.run.key_check`,
     called and not copied. A management key answers 200 there and cannot call
     a model.
  5. `F-g1` to `F-g3`, blocking. Then Stage A's record must hold the same draw,
     sessions and prompt digests the checks just rebuilt. A prompt that would
     differ from the one Stage A recorded is never sent.
  6. The destination: a paid record is never overwritten
     (`harness/record_guard.py`). The flag that would is not typed without Sergi
     asking.
  7. The client, and the calls: sequential (hard rule 3), two passes for every
     session but the smoke run.

A SESSION THAT DIES KEEPS WHAT IT PAID FOR (§5.8). Each answer is appended to
`results_fidelity/ask_<session>.partial.jsonl` as it arrives, a file git
ignores. A restart under the same protocol and the same Stage A record
resumes, and the final record says where it was resumed. No prompt already
answered in a pass is asked again in that pass. The partial file goes once the
record is written. **Five failed calls in a row stop the session** without
recording them, because a run of failures is an outage, not answers. See
`STOP_AFTER_FAILURES_IN_A_ROW`.

    python3 -m fidelity.ask --dry-run
    .venv/bin/python -m fidelity.ask --session smoke
    .venv/bin/python -m fidelity.ask --session births
    .venv/bin/python -m fidelity.ask --session base1      # then base2, base3
    .venv/bin/python -m fidelity.ask --session ticket_only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from harness.domain import ACTIONS
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from reuse.run import key_check
from rung2.proposers2 import OpenRouterProposer2, ProposalError

from . import plan, prompts, sample

# What each session asks, by kind of prompt. A smoke record must hold a valid
# answer of every kind a later session will ask.
KINDS = {"smoke": {prompts.BIRTH, prompts.HIDDEN, prompts.TICKET_ONLY},
         "births": {prompts.BIRTH},
         "base1": {prompts.HIDDEN}, "base2": {prompts.HIDDEN},
         "base3": {prompts.HIDDEN},
         "ticket_only": {prompts.TICKET_ONLY}}

# What `OpenRouterProposer2.propose` sends, written into every record so that it
# says what was asked. `tests/test_fidelity.py` checks these against the request
# the proposer actually builds, so they cannot drift from it in silence.
TEMPERATURE = 0
MAX_TOKENS = 1200


def protocol() -> dict[str, Any]:
    return {"plan": str(plan.PLAN), "model": plan.MODEL,
            "prompt_version": plan.PROMPT, "reasoning": plan.REASONING,
            "seed": plan.SEED, "n": plan.N}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sample_sha256(path: Path | None = None) -> str:
    return hashlib.sha256((path or plan.SAMPLE_PATH).read_bytes()).hexdigest()


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
        return False, f"no Stage A record at {path}; run fidelity.sample first"
    rec = json.loads(path.read_text())
    draw = json.loads(json.dumps({f"run{k}": v for k, v in design.draw.items()}))
    if rec.get("draw") != draw:
        return False, f"{path} holds another draw than the one rebuilt now"
    if rec.get("sessions") != json.loads(json.dumps(design.sessions)):
        return False, f"{path} holds other sessions than the ones rebuilt now"
    stale = [i for i, it in design.items.items()
             if rec.get("items", {}).get(i, {}).get("digest") != it["digest"]]
    if stale:
        return False, f"{len(stale)} prompts rebuilt now differ from {path}'s"
    return True, f"{path}: the same draw, sessions and prompts"


# ---------------------------------------------------------------------------
# The labels, copied from the Stage B record and never computed (§8)
# ---------------------------------------------------------------------------

def labels(design: sample.Design, item: dict) -> dict[str, Any]:
    if item["kind"] == prompts.TICKET_ONLY:
        rows = design.runs[plan.RUNS[0]]["records"]
        return {"truth": rows[item["idx"]]["truth"], "rare": item["rare"],
                "sources": [{"run": k, "idx": i,
                             "rule_action": design.runs[k]["records"][i]["predicted"]}
                            for k, i in item["sources"]]}
    row = design.runs[item["run"]]["records"][item["idx"]]
    out = {"truth": row["truth"], "truth_rule": row["truth_rule"]}
    if item["kind"] == prompts.BIRTH:
        out["recorded_answer"] = row["predicted"]
        out["recorded_answer_right"] = row["proposal_action_correct"]
    else:
        out.update(rule_id=row["winner_id"], rule_action=row["predicted"],
                   rule_right=row["correct"], uniform=item["uniform"],
                   census=item["census"])
    return out


# ---------------------------------------------------------------------------
# Step 7: the calls, and the partial record that survives an interruption
# ---------------------------------------------------------------------------

def open_partial(path: Path, header: dict) -> tuple[list[dict], bool]:
    """The answers already paid for in this session, and whether it resumes."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            f.write(json.dumps(header) + "\n")
        return [], False
    lines = path.read_text().splitlines()
    if not lines or json.loads(lines[0]) != header:
        sys.exit(f"\nREFUSED: {path} was left by a session under another protocol "
                 "or another Stage A record. Nothing was spent. Look at it before "
                 "removing it.\n")
    rows = []
    for line in lines[1:]:
        try:
            rows.append(json.loads(line))
        except ValueError:            # a line cut off by the interruption
            break
    # Rewritten without the cut line, so that what is appended next starts on
    # a line of its own and a second interruption cannot bury it.
    with path.open("w") as f:
        f.write("".join(json.dumps(r) + "\n" for r in [header] + rows))
    return rows, True


class Outage(Exception):
    """Too many calls in a row failed: the network, the key or the credit, not
    the model's answers."""


# `propose` raises the same error for an answer that never parsed and for a
# call that never reached the model: a dropped connection, a revoked key, an
# exhausted credit. One failure is an answer the model did not give, and it is
# recorded. A run of them is an outage, and recording it would fill the session
# with failures that are not answers. That is what PLAN_REUSE.md's first smoke
# run did with a rejected key: 20 failures out of 20, and a record. So a run of
# this many stops the session, and those failures are not written: the partial
# record keeps everything before them, and a resume asks them again. Fixed when
# this module was written, before any call of the plan was made. Stage B parsed
# 135 proposals of 135, so five unparsed answers in a row is not the plausible
# reading of five failures in a row.
STOP_AFTER_FAILURES_IN_A_ROW = 5


def ask(session: str, design: sample.Design, proposer, partial: Path,
        header: dict, clock=time.monotonic) -> tuple[list[dict], list[str]]:
    done, resumed = open_partial(partial, header)
    asked = {(r["pass"], r["id"]) for r in done}
    resumed_at = [now()] if resumed else []
    rows = list(done)
    pending: list[dict] = []           # failures not yet known to be isolated
    plan_ = design.sessions[session]
    total = sum(len(p) for p in plan_["passes"])

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
                t0 = clock()
                try:
                    action, payload = proposer.propose(p.case, p.base_text)
                    failure = None
                except ProposalError as exc:
                    action, payload, failure = None, None, str(exc)[:300]
                row = {"session": session, "pass": pass_no, "position": position,
                       "id": iid, "kind": item["kind"], "run": item["run"],
                       "idx": item["idx"], "digest": p.digest,
                       "shown_ids": list(p.shown_ids), "action": action,
                       "valid": action in ACTIONS, "payload": payload,
                       "failure": failure, "labels": labels(design, item),
                       "seconds": round(clock() - t0, 2), "asked_at": now()}
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage B of PLAN_FIDELITY.md: the calls (spends).")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--dry-run", action="store_true",
                       help="run F-g1 to F-g3 and stop; spends nothing")
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

    plan.refuse_unsigned(f"fidelity/ask.py spends (session {args.session})")

    if args.session != "smoke":
        ok, why = smoke_check(KINDS[args.session])
        if not ok:
            sys.exit(f"\nREFUSED: session {args.session} before a smoke run that "
                     f"worked — {why}.\n  Nothing was built, spent or written.\n")
        print(f"smoke check: {why}")

    ok, why = key_check()
    if not ok:
        sys.exit(f"\nREFUSED: fidelity/ask.py — {why}.\n  Nothing was built, spent "
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
    digest = sample_sha256()
    header = {"protocol": protocol(), "session": args.session,
              "sample_sha256": digest}
    started = now()
    print(f"\n{plan.PLAN} · stage B · session {args.session} with {proposer.name}\n")
    try:
        rows, resumed_at = ask(args.session, checks.design, proposer,
                               plan.partial_path(args.session), header)
    except Outage as exc:
        sys.exit(f"\n\nSTOPPED: {exc}.\n  Every answer before them is kept in "
                 f"{plan.partial_path(args.session)}; the same command resumes "
                 "there once the cause is fixed. No record was written.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        "_env": environment(),
        **protocol(),
        "stage": "B",
        "session": args.session,
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
    }, indent=2, default=str))
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
