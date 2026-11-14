"""
Stage C of `PLAN_CORRECTIONS.md`: scoring, and the six adjudications (§10).
**Free, and gated**: it refuses while §0 is unsigned, because what the gate
protects is the order of events, not money (§11 of the plan).

THE ROWS ARE §0's, AND ALL OF THEIR TERMS ARE SETTLED THERE, NOT HERE.

  CR-a  the median over L's runs of `followed(r)`; holds at or above 19/20. A
        run with no first call at a reported ticket that names a queue has no
        `followed(r)`.
  CR-b  the median over L's runs of `space(B)`, less the median over N's;
        holds at or above 1/10.
  CR-c  the same with `pair(B)`, the mean recall of `ACCOUNT_MANAGER` and
        `T3_ENGINEERING` over the space; holds at or above 1/4.
  CR-d  the median over L's runs of `space(A(r))` less `space(B)`; holds at or
        above 0. A run without a valid at-once ask at all of its labels has no
        value.
  CR-e  the median over L's runs of `space(B)` less `best(r)`; holds strictly
        above 0.
  CR-f  the median over L's runs of `recall_ONCALL_ESCALATION(B)` over the
        space; holds at or above 9/10.

Every statistic is a fraction of counts, compared with its line exactly. A row
that reads an arm with fewer than two runs with a value has no value. A verdict
on medians is thin when any one run, put in place of its arm's median, puts the
statistic on the other side of its line; for `CR-d` and `CR-e`, any one run's
difference put in place of the median. `space(B)`, the recall and `refused(r)`
are `placement/score.py`'s, called.

`CR-g` is reported and adjudicates nothing.

    python3 -m corrections.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m corrections.score
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any, Callable

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from edges.rebuild import rebuild
from manual import compile as C
from manual import instrument as MI
from placement import score as pl_score
from reasoned_loop import score as rl_score

from . import ask, gates, learners, plan, run

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median
SPACE_N = 134400
PAIR = ("ACCOUNT_MANAGER", "T3_ENGINEERING")
ONCALL = "ONCALL_ESCALATION"


def holds(rid: str, x: Fraction) -> bool:
    """§0's side of the line, as `plan.SIDES` gives it."""
    line, side = plan.LINES[rid], plan.SIDES[rid]
    if side == ">=":
        return x >= line
    if side == ">":
        return x > line
    raise ValueError(f"no side {side!r} for {rid}")


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def followed(record: dict[str, Any]) -> tuple[int, int]:
    """Of the first calls at reported tickets whose answer names one of the
    eight queues, how many name the ticket's true queue."""
    truth = {r["idx"]: r["truth"] for r in record["records"]}
    num = den = 0
    for esc in record["escalations"]:
        if esc["kind"] != plan.ERROR:
            continue
        call = (esc.get("calls") or [None])[0] or {}
        payload = call.get("payload")
        action = payload.get("action") if isinstance(payload, dict) else None
        if action in ACTIONS:
            den += 1
            num += action == truth[esc["idx"]]
    return num, den


def recall(scored: dict[str, Any], q: str) -> Fraction:
    r = scored["recall"][q]
    return F(r["right"], r["of"])


def read_run(record: dict[str, Any]) -> dict[str, Any]:
    """`placement.score.read_run`, and this plan's statistics."""
    got = pl_score.read_run(record)
    sp = got["space_scored"]
    got["pair"] = sum((recall(sp, q) for q in PAIR), F(0)) / len(PAIR)
    got["rep"], got["arm"] = record.get("rep"), record.get("arm")
    num, den = followed(record)
    got["followed"] = F(num, den) if den else None
    got["followed_counts"] = [num, den]
    got["handed"] = run.handed_check(record, record.get("arm"))
    return got


# ---------------------------------------------------------------------------
# The at-once asks, and the learners
# ---------------------------------------------------------------------------

def answer_space(payload: Any) -> dict[str, Any]:
    """An at-once answer installed as §5.4 reads it, and its share of the
    space; the first-match reading beside it."""
    raw, _ = C.rules_of(payload)
    inst = C.install(raw, MI.space())
    sp = MI.over_space(inst.engine)
    return {"space": F(sp["correct"], sp["n"]), "installed": inst.summary(),
            "first_match": MI.first_match_over_space(inst.rules)["e2e"]}


def at_once(session: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Each checkpoint's asks: for each ask, its first valid answer in re-ask
    order, read; and the median of their `space`."""
    rows = sorted(session["rows"], key=lambda r: (r["reask"], r["position"]))
    chosen: dict[tuple[int, int], dict] = {}
    for r in rows:
        if r["valid"] and (r["checkpoint"], r["k"]) not in chosen:
            chosen[(r["checkpoint"], r["k"])] = r
    out: dict[int, dict[str, Any]] = {}
    for j in sorted({r["checkpoint"] for r in rows}):
        read = [answer_space(chosen[(j, k)]["payload"])
                for (cj, k) in sorted(chosen) if cj == j]
        spaces = [x["space"] for x in read]
        out[j] = {"valid_asks": len(read), "space": median(spaces) if spaces else None,
                  "asks": [{"space": frac(x["space"]), "first_match": x["first_match"],
                            "installed": x["installed"]} for x in read]}
    return out


def base_after(record: dict[str, Any], idx: int) -> Fraction:
    """The loop's base as it stood right after case `idx`'s escalation."""
    eng = rebuild(record, list(MI.corpus())[:idx + 1], MI.space(), only=set()).engine
    sp = MI.over_space(eng)
    return F(sp["correct"], sp["n"])


def curve(record: dict[str, Any], session: dict[str, Any] | None) -> list[dict[str, Any]]:
    """At every checkpoint: the loop's base after the same label, the at-once
    asks and every learner."""
    pairs = ask.labelled(record)
    asked = at_once(session) if session else {}
    out = []
    for j in plan.checkpoints(len(pairs)):
        idx = pairs[j - 1][0]
        trained = learners.trained(pairs[:j])
        b = learners.best(trained)
        out.append({"labels": j, "case": idx, "loop": frac(base_after(record, idx)),
                    "at_once": None if j not in asked else
                    {**asked[j], "space": frac(asked[j]["space"])},
                    "learners": trained,
                    "best": None if b is None else frac(F(b, SPACE_N))})
    return out


# ---------------------------------------------------------------------------
# The six rows
# ---------------------------------------------------------------------------

def verdict(rid: str, value: Fraction | None, thin: bool, why: str | None,
            **parts) -> dict[str, Any]:
    line, at = plan.LINES[rid], plan.SIDES[rid]
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "holds_at": at, "thin": False, **parts}
    return {"verdict": HOLDS if holds(rid, value) else REFUTED, "value": frac(value),
            "line": frac(line), "holds_at": at, "thin": thin, "why": None, **parts}


def median_row(rid: str, values: dict[str, list[Fraction]],
               stat: Callable[[dict[str, Fraction]], Fraction]) -> tuple[Fraction, bool]:
    """The statistic over the arms' medians, and whether any one run put in
    place of its arm's median puts it on the other side of the line."""
    meds = {a: median(xs) for a, xs in values.items()}
    v = stat(meds)
    thin = any(holds(rid, stat({**meds, a: x})) != holds(rid, v)
               for a, xs in values.items() for x in xs)
    return v, thin


ROWS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "CR-a": (("l",), "followed", lambda m: m["l"]),
    "CR-b": (("l", "n"), "space", lambda m: m["l"] - m["n"]),
    "CR-c": (("l", "n"), "pair", lambda m: m["l"] - m["n"]),
    "CR-f": (("l",), "oncall", lambda m: m["l"]),
}
DIFFERENCES = ("CR-d", "CR-e")
ALL_ROWS = ("CR-a", "CR-b", "CR-c", "CR-d", "CR-e", "CR-f")


def median_of_differences(rid: str, diffs: list[Fraction], per_run: dict) -> dict[str, Any]:
    if len(diffs) < 2:
        return verdict(rid, None, False, "fewer than two of L's runs with a value",
                       per_run=per_run)
    v = median(diffs)
    thin = any(holds(rid, d) != holds(rid, v) for d in diffs)
    return verdict(rid, v, thin, None, per_run=per_run)


def row(rid: str, runs: dict[str, list[dict]], extra: dict[int, dict]) -> dict[str, Any]:
    if rid in DIFFERENCES:
        diffs, per_run = [], {}
        for r in runs["l"]:
            e = extra.get(r["rep"], {})
            other = e.get("at_once_all") if rid == "CR-d" else e.get("best_all")
            if other is None:
                per_run[r["rep"]] = None
                continue
            d = other - r["space"] if rid == "CR-d" else r["space"] - other
            diffs.append(d)
            per_run[r["rep"]] = str(d)
        return median_of_differences(rid, diffs, per_run)
    arms, key, stat = ROWS[rid]
    vals = {a: [F(r[key]) for r in runs[a] if r[key] is not None] for a in arms}
    per_run = {a: [None if r[key] is None else str(F(r[key])) for r in runs[a]] for a in arms}
    short = [a for a in arms if len(vals[a]) < 2]
    if short:
        return verdict(rid, None, False, f"arm(s) {short} with fewer than two runs with a "
                                         f"value of {key}", per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    return verdict(rid, v, thin, None, per_run=per_run)


# ---------------------------------------------------------------------------
# CR-g, reported
# ---------------------------------------------------------------------------

def corpus_split(record: dict[str, Any], eng) -> dict[str, Any]:
    """The final base on the arrivals, split into the tickets labelled, with
    their repeats, and the rest; and the online figure, each decision as it was
    taken.

    **The truth of every arrival is the corpus label**, `plan.labels()`, the one
    the trigger reads, and not the record's. A run that stops at the cap keeps a
    row only for the cases it read. Its final base still decides all 2,000
    arrivals, and the online figure covers the cases it read, which
    `online_cases_read` gives. Corrected on 2026-11-14, after Stage C's first
    launch stopped here on N r1, which the cap stopped at case 1,276, before
    anything was written or printed."""
    cases = list(MI.corpus())
    truth = [t for t, _ in plan.labels()]
    keys = {cases[int(i)].key() for i in record.get("reports_handed") or {}}
    out = {"labelled": [0, 0], "rest": [0, 0]}
    for i, case in enumerate(cases):
        outcome, winner, _ = eng.decide(case)
        right = winner is not None and outcome != "CONFLICT" and winner.action == truth[i]
        part = "labelled" if case.key() in keys else "rest"
        out[part][0] += right
        out[part][1] += 1
    rows = record["records"]
    out["online"] = [sum(1 for r in rows if r["correct"] is True), len(rows)]
    out["online_cases_read"] = len(rows)
    return out


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sessions: dict[str, dict], extra: dict[int, dict]) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}, "curves": {}, "prior": None, "own_answers": {}}
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            sp = r["space_scored"]
            causes: dict[str, int] = {}
            for esc in rec["escalations"]:
                causes[esc["kind"]] = causes.get(esc["kind"], 0) + 1
            empties = sum(1 for esc in rec["escalations"] for c in esc.get("calls") or []
                          if c.get("payload") == {})
            out["runs"][f"{a}_r{r['rep']}"] = {
                "space": frac(r["space"]), "pair": frac(r["pair"]),
                "oncall": frac(r["oncall"]),
                "recall": {q: frac(recall(sp, q)) for q in ACTIONS},
                "followed": r["followed_counts"], "refused": frac(r["refused"]),
                "calls": r["calls"], "escalations": causes,
                "stopped_at_the_cap": rec.get("v1b", {}).get("stopped_at"),
                "empty_objects": empties, "labels": len(rec.get("reports_handed") or {}),
                "handed": r["handed"][1],
                "corpus": corpus_split(rec, r["engine"])}
    for k, e in extra.items():
        out["curves"][f"l_r{k}"] = e["curve"]
        out["own_answers"][f"l_r{k}"] = e["own_answers"]
    if "prior" in sessions:
        out["prior"] = {str(j): {**v, "space": frac(v["space"])}
                        for j, v in at_once(sessions["prior"]).items()}
    return out


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def score(records: dict[str, list[dict]], sessions: dict[str, dict]) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    extra: dict[int, dict] = {}
    for r, rec in zip(runs["l"], records["l"]):
        k = r["rep"]
        session = sessions.get(plan.session_of(k))
        pairs = ask.labelled(rec)
        asked = at_once(session) if session else {}
        all_j = len(pairs)
        trained = learners.trained(pairs)
        b = learners.best(trained)
        own = learners.trained(learners.own_answers(rec, rec.get("reports_handed") or {}))
        extra[k] = {"at_once_all": (asked.get(all_j) or {}).get("space"),
                    "best_all": None if b is None else F(b, SPACE_N),
                    "curve": curve(rec, session), "own_answers": own}
    verdicts = {rid: row(rid, runs, extra) for rid in ALL_ROWS}
    return {"verdicts": verdicts, "CR-g": reported(runs, records, sessions, extra),
            "rebuilt_is_the_run": all(r["rebuilt"] for a in plan.ARMS for r in runs[a]),
            "calls_as_recorded": all(r["calls_as_recorded"] for a in plan.ARMS
                                     for r in runs[a]),
            "labels_by_their_route": all(r["handed"][0] for a in plan.ARMS for r in runs[a])}


def read_records() -> tuple[dict[str, list[dict]], dict[str, dict], list[str]]:
    out: dict[str, list[dict]] = {a: [] for a in plan.ARMS}
    missing = []
    for a, rep in plan.schedule():
        path = plan.run_path(a, rep)
        if path.exists():
            out[a].append(json.loads(path.read_text()))
        else:
            missing.append(f"{a} r{rep}")
    sessions = {s: json.loads(plan.ask_path(s).read_text()) for s in plan.SESSIONS
                if plan.ask_path(s).exists()}
    missing += [f"session {s}" for s in plan.SESSIONS if s not in sessions]
    return out, sessions, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_CORRECTIONS.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CR-g1 to CR-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("corrections/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if not plan.sample_path().exists():
        sys.exit("\nREFUSED: no Stage A record; nothing was written.\n")
    records, sessions, missing = read_records()
    scored = score(records, sessions)
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(), "missing": missing, **scored}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in scored["verdicts"].items():
        print(f"  {rid}  {v['verdict']}{', thin' if v.get('thin') else ''}")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
