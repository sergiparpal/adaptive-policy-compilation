"""
Stage C of `PLAN_CHANNEL.md`: scoring, and the six adjudications (§10). **Free,
and gated**: it refuses while §0 is unsigned.

EVERY STATISTIC IS A FRACTION OF COUNTS, compared with its line exactly (§0).

  CH-a  the median over the channel arm's runs of `space(B)`.
  CH-b  the median over the error arm's runs of `space(B)`, less the channel
        arm's. It holds at or below its line; every other row at or above.
  CH-c  the median over the channel arm's runs of the recall of
        `ONCALL_ESCALATION` over the space.
  CH-d  the median over the error arm's runs of `space(B)`.
  CH-e  the median over the error arm's runs of the recall of
        `ONCALL_ESCALATION` over the space.
  CH-f  the median over the channel arm's runs of `calls(r)`, over the error
        arm's: one call per escalation and one per placement round sent, failed
        ones included, and an attempt retried inside a call not another call.

*thin* AND *no value* ARE §0's, settled there and applied here as written: a row
is thin when any one run of an arm it reads, put in place of that arm's median,
puts the statistic on the other side of its line. A row that reads an arm with
fewer than two runs has no value, and so has `CH-f` if the error arm's median
makes no call. The median of three runs is the middle one, of two their mean.

A RUN'S BASE is `manual.instrument.final_engine`'s rebuild of its record, held to
the rules and edges the record says the run ended with: `reasoned_loop.score`'s
`read_run`, called (rule A).

CH-g IS REPORTED, NEVER ADJUDICATED: every run on both surfaces, its online
figures, the channel's reports by queue, by governing rule and over time, each
run beside the transcriber under its own draws or trigger (read off Stage A's
record, which owns those figures), the error escalations by governing rule beside
the supply, every escalation's verdict with its finish reasons, the placement
rounds, `RL-e`'s direction and the Stage C ranking's by arm, the error runs beside
`PLAN_REASONED_LOOP.md`'s across dates (read off that plan's Stage C record), and
the calls. The pace is read over every call: this plan's runs record each call's
own seconds from their first launch (that plan's §5.5, second amendment).

    python3 -m channel.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m channel.score
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from blind import rows as brows
from manual import instrument as MI
from reasoned_loop import plan as rl_plan
from reasoned_loop import score as rl_score

from . import gates, plan

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median
ONLINE = ("n_rules", "escalations", "impasses", "conflicts", "coverage", "reuse_rate",
          "e2e_accuracy", "silent_error_rate", "proposal_action_accuracy",
          "failed_proposals", "rejected_rules", "dead_rules")
BLOCK = 200                        # "over time": the arrivals in blocks of a tenth


def holds(rid: str, x: Fraction) -> bool:
    """§0's side of the line: `CH-b` holds at or below it, every other row at or
    above."""
    line = plan.LINES[rid]
    return x <= line if rid in plan.HOLDS_AT_OR_BELOW else x >= line


def calls_made(record: dict) -> int:
    """`calls(r)`: every call an escalation's record keeps, failed ones too."""
    return sum(len(esc.get("calls") or []) for esc in record["escalations"])


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(record: dict) -> dict[str, Any]:
    """`reasoned_loop.score.read_run`, and the run's calls."""
    got = rl_score.read_run(record)
    n = calls_made(record)
    got.update(calls=n, calls_as_recorded=n == record.get("calls"))
    return got


# ---------------------------------------------------------------------------
# The six rows
# ---------------------------------------------------------------------------

def verdict(rid: str, value: Fraction | None, thin: bool, why: str | None,
            **parts) -> dict[str, Any]:
    line = plan.LINES[rid]
    at = "<=" if rid in plan.HOLDS_AT_OR_BELOW else ">="
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "holds_at": at, "thin": False, **parts}
    return {"verdict": HOLDS if holds(rid, value) else REFUTED, "value": frac(value),
            "line": frac(line), "holds_at": at, "thin": thin, "why": None, **parts}


def enough(runs: dict[str, list[dict]], arms) -> str | None:
    short = [a for a in arms if len(runs[a]) < 2]
    return f"arm(s) {short} with fewer than two runs" if short else None


def median_row(rid: str, values: dict[str, list[Fraction]],
               stat: Callable[[dict[str, Fraction]], Fraction | None]
               ) -> tuple[Fraction | None, bool]:
    """The statistic over the arms' medians, and whether any one run put in
    place of its arm's median puts it on the other side of the line."""
    meds = {a: median(xs) for a, xs in values.items()}
    v = stat(meds)
    if v is None:
        return None, False
    thin = False
    for a, xs in values.items():
        for x in xs:
            w = stat({**meds, a: x})
            thin |= w is not None and holds(rid, w) != holds(rid, v)
    return v, thin


def ratio(m: dict[str, Fraction]) -> Fraction | None:
    return m["c"] / m["e"] if m["e"] else None


ROWS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "CH-a": (("c",), "space", lambda m: m["c"]),
    "CH-b": (("c", "e"), "space", lambda m: m["e"] - m["c"]),
    "CH-c": (("c",), "oncall", lambda m: m["c"]),
    "CH-d": (("e",), "space", lambda m: m["e"]),
    "CH-e": (("e",), "oncall", lambda m: m["e"]),
    "CH-f": (("c", "e"), "calls", ratio),
}


def row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    arms, key, stat = ROWS[rid]
    vals = {a: [F(r[key]) for r in runs[a]] for a in arms}
    per_run = {a: [str(x) for x in xs] for a, xs in vals.items()}
    why = enough(runs, arms)
    if why:
        return verdict(rid, None, False, why, per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    if v is None:
        return verdict(rid, None, False, "the error arm's median run made no call",
                       per_run=per_run)
    return verdict(rid, v, thin, None, per_run=per_run)


# ---------------------------------------------------------------------------
# CH-g, reported
# ---------------------------------------------------------------------------

def calls_of(record: dict) -> dict[str, Any]:
    """What a run's calls cost and how they came back (§10). An attempt refused
    for the rate reached no model: it is counted, and the providers, the finish
    reasons and the tokens are read over the attempts that did. A call any of
    whose attempts was refused waited before it was answered, so the pace is
    read over every call and over the calls none of whose attempts was."""
    calls = [c for esc in record["escalations"] for c in esc.get("calls") or []]
    attempts = [a for c in calls for a in c.get("call_attempts") or []]
    reached = [a for a in attempts if a.get("error") != plan.RATE_LIMITED]
    by_round = collections.defaultdict(list)
    unlimited = collections.defaultdict(list)
    for c in calls:
        if c.get("seconds") is None:
            continue
        by_round[c["round"]].append(c["seconds"])
        if not any(a.get("error") == plan.RATE_LIMITED for a in c.get("call_attempts") or []):
            unlimited[c["round"]].append(c["seconds"])
    reasoning = [a.get("reasoning_tokens") or 0 for a in reached]

    def pace(d):
        return {str(k): {"calls": len(v), "median": statistics.median(v), "sum": sum(v)}
                for k, v in sorted(d.items())}
    return {"calls": len(calls),
            "failed": sum(1 for c in calls if c.get("failure") is not None),
            "served_elsewhere": sum(1 for c in calls if c.get("failure") is None
                                    and c.get("served_by") != plan.PROVIDER_NAME),
            "attempts": len(attempts), "rate_limited": len(attempts) - len(reached),
            "providers": dict(collections.Counter(a.get("provider") or "none" for a in reached)),
            "finish_reasons": dict(collections.Counter(a.get("finish_reason") or "none"
                                                       for a in reached)),
            "prompt_tokens": sum(a.get("prompt_tokens") or 0 for a in reached),
            "completion_tokens": sum(a.get("completion_tokens") or 0 for a in reached),
            "reasoning_tokens": {"sum": sum(reasoning),
                                 "median": statistics.median(reasoning) if reasoning else None,
                                 "max": max(reasoning, default=None)},
            "seconds_by_round": pace(by_round),
            "seconds_by_round_unlimited": pace(unlimited),
            "retries": dict(collections.Counter(x for c in calls for x in c.get("retries") or []))}


def verdicts_with_finish(record: dict) -> dict[str, int]:
    """Every escalation's verdict, with the finish reasons of its calls."""
    return dict(collections.Counter(
        f"{esc['verdict']}: {'/'.join(str(c.get('finish_reason')) for c in esc.get('calls') or [])}"
        for esc in record["escalations"]))


def reports_of(record: dict) -> dict[str, Any]:
    """The wrong decisions the trigger saw, whether the channel reported them
    and whether the reported ones escalated: in all, by queue, by governing rule
    and over time, in blocks of `BLOCK` arrivals."""
    wrong = [r for r in record["records"] if r["reported"] is not None]

    def tally(key) -> dict[str, list[int]]:
        out: dict[str, list[int]] = {}
        for r in wrong:
            k = str(key(r))
            out.setdefault(k, [0, 0, 0])
            out[k][0] += 1
            out[k][1] += bool(r["reported"])
            out[k][2] += bool(r["reported"]) and r["cause"] == plan.ERROR
        return dict(sorted(out.items(), key=lambda kv: (len(kv[0]), kv[0])))
    return {"columns": ["wrong", "reported", "reported and escalated"],
            "all": [len(wrong), sum(1 for r in wrong if r["reported"]),
                    sum(1 for r in wrong if r["reported"] and r["cause"] == plan.ERROR)],
            "by_queue": tally(lambda r: r["truth"]),
            "by_rule": tally(lambda r: r["truth_rule"]),
            "over_time": tally(lambda r: r["idx"] // BLOCK * BLOCK)}


def errors_by_rule(record: dict, arm: str, rep: int, supply: dict[str, Any]) -> dict[str, list]:
    """The error escalations by governing rule, beside the rule's corpus tickets
    and the ones the run's draws make reportable: every ticket, for the error
    arm. Read off Stage A's supply."""
    esc = collections.Counter(r["truth_rule"] for r in record["records"]
                              if r["cause"] == plan.ERROR)
    out = {}
    for rule, s in supply["rules"].items():
        reportable = s["tickets"] if plan.stream(arm, rep) is None else s["reportable"][rep - 1]
        out[rule] = [esc.get(rule, 0), s["tickets"], reportable]
    return {"columns": ["error escalations", "corpus tickets", "reportable"], "rules": out}


def exact(scored: dict[str, Any]) -> dict[str, Any]:
    return frac(F(scored["correct"], scored["n"]))


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sample: dict[str, Any], closed: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}}
    refs = sample["references"]
    inside = MI.space().full & ~MI.outside()
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            eng, rep = r["engine"], rec["rep"]
            co = MI.over_corpus(eng)
            tx = refs["transcriber"]["e" if plan.stream(a, rep) is None else f"c_r{rep}"]
            out["runs"][f"{a}_r{rep}"] = {
                "space": frac(r["space"]),
                "space_without_the_keyword": exact(MI.over_space(eng, MI.outside())),
                "space_with_the_keyword": exact(MI.over_space(eng, inside)),
                "recall_space": {q: [v["right"], v["of"]]
                                 for q, v in r["space_scored"]["recall"].items()},
                "corpus": [co["correct"], co["n"]],
                "recall_corpus": {q: [v["right"], v["of"]] for q, v in co["recall"].items()},
                "k_a": str(MI.k_a_exact(rec["rules"])), "cover": r["cover"],
                "rebuilt_is_the_run": r["rebuilt"],
                "online": {k: rec["metrics"].get(k) for k in ONLINE},
                "v1b": rec["v1b"], "drafts": list(r["drafts"]),
                "calls": calls_of(rec), "calls_as_recorded": r["calls_as_recorded"],
                "reports": reports_of(rec),
                "errors_by_rule": errors_by_rule(rec, a, rep, refs["supply"]),
                "transcriber": {k: tx["figures"][k] for k in (
                    "escalations", "impasses", "conflicts", "errors", "calls",
                    "space_right", "space_points", "corpus_right", "recall_oncall")},
                "verdicts": verdicts_with_finish(rec),
                "placements": rl_score.placements_of(rec),
                "births": rl_score.births_against_the_list(rec),
                "rare": rl_score.rare_of(rec, eng),
                "dates": [rec.get("started_at"), rec.get("_env", {}).get("recorded_at")]}
    out["direction"] = {}
    for a in plan.ARMS:
        rows_by_run = [r["edges"] for r in runs[a]]
        got = {"declared": rl_score.direction(rows_by_run),
               "ranking": rl_score.direction(rows_by_run, predict=brows.stage_c_names)}
        for d in got.values():
            d["reading"] = frac(d["reading"]) if d["reading"] is not None else None
        out["direction"][a] = got
    theirs = closed.get("RL-h", {}).get("runs", {})
    out["across_dates"] = {
        f"r{rep}": {"this_plan": {k: out["runs"][f"e_r{rep}"][k] for k in (
                        "space", "space_without_the_keyword", "space_with_the_keyword",
                        "recall_space", "corpus", "k_a", "cover", "online", "dates")}
                    if f"e_r{rep}" in out["runs"] else None,
                    "reasoned_loop": {k: theirs.get(f"e_r{rep}", {}).get(k) for k in (
                        "space", "space_without_the_keyword", "space_with_the_keyword",
                        "recall_space", "corpus", "k_a", "cover", "online", "dates")}}
        for rep in range(1, plan.REPS + 1)}
    return out


def score(records: dict[str, list[dict]], sample: dict[str, Any],
          closed: dict[str, Any]) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    verdicts = {rid: row(rid, runs) for rid in ROWS}
    return {"verdicts": verdicts, "CH-g": reported(runs, records, sample, closed),
            "rebuilt_is_the_run": all(r["rebuilt"] for a in plan.ARMS for r in runs[a]),
            "calls_as_recorded": all(r["calls_as_recorded"] for a in plan.ARMS
                                     for r in runs[a])}


def read_records() -> tuple[dict[str, list[dict]], list[str]]:
    out: dict[str, list[dict]] = {a: [] for a in plan.ARMS}
    missing = []
    for a, rep in plan.schedule():
        path = plan.run_path(a, rep)
        if path.exists():
            out[a].append(json.loads(path.read_text()))
        else:
            missing.append(f"{a} r{rep}")
    return out, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_CHANNEL.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CH-g1 to CH-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("channel/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if not plan.sample_path().exists():
        sys.exit(f"\nREFUSED: no Stage A record at {plan.sample_path()}; nothing was "
                 "written.\n")
    sample = json.loads(plan.sample_path().read_text())
    closed = json.loads(rl_plan.score_path().read_text())
    records, missing = read_records()
    out = score(records, sample, closed)
    if not out["rebuilt_is_the_run"] or not out["calls_as_recorded"]:
        sys.exit("\nREFUSED: a run's rebuilt base, or its calls, are not what its record "
                 "says it ended with; nothing was written.\n")
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(), "missing": missing,
              "lines": {k: {**frac(v), "holds_at": "<=" if k in plan.HOLDS_AT_OR_BELOW
                            else ">="} for k, v in plan.LINES.items()}, **out}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in out["verdicts"].items():
        val = v["value"]["value"] if v.get("value") else None
        print(f"  {rid}: {v['verdict']}{', thin' if v.get('thin') else ''} "
              f"({'—' if val is None else round(val, 4)})")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
