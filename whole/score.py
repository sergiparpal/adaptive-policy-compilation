"""
Stage C of `PLAN_WHOLE.md`: scoring, and the six adjudications (§10). **Free, and
gated**: it refuses while §0 is unsigned, because what the gate protects is the
order of events, not money (§11 of the plan).

THE ROWS ARE §0's, AND ALL OF THEIR TERMS ARE SETTLED THERE, NOT HERE.

  WR-a  the median over v1d's runs of `whole(r)`; holds at or above 3/4. A run
        with no first-call draft of the right queue has no `whole(r)`, and the row
        reads the v1d runs that have one.
  WR-b  the median over v1d's runs of `recall_ONCALL_ESCALATION(B)` over the
        space; holds at or above 9/10.
  WR-c  the median over v1d's runs of `refused(r)`, over the median over v1c's;
        holds at or below 3/2. No value when v1c's median is 0.
  WR-d  the median over v1c's runs of `space(B)`, less the median over v1d's;
        holds at or below 1/40.
  WR-e  the median over v1c's runs of `recall_ONCALL_ESCALATION(B)` over the
        space; holds strictly below 9/10.
  WR-f  run `k` of v1d's recall of the queue less run `k` of v1c's, paired by
        the draws both read; the median over the pairs; holds at or above 1/4.
        Thin when any one pair's difference, put in place of the median, falls
        on the other side of the line. No value with fewer than two pairs.

Every statistic is a fraction of counts, compared with its line exactly. A row
that reads an arm with fewer than two runs with a value has no value. A verdict on
medians is thin when any one run, put in place of its arm's median, puts the
statistic on the other side of its line. `refused(r)`, `space(B)` and the recall
are `placement/score.py`'s, called; `whole(r)` is `whole/references.py`'s.

`WR-g` is reported and adjudicates nothing. What a run reads is
`placement.score.read_run`'s, called: its base rebuilt and held to the record,
its `space`, its recall, its calls and its `refused(r)`.

    python3 -m whole.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m whole.score
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from blind import rows as brows
from channel import score as ch_score
from manual import instrument as MI
from placement import plan as pl_plan
from placement import score as pl_score
from reasoned_loop import score as rl_score

from . import gates, plan, references

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median
ONCALL = references.ONCALL


def holds(rid: str, x: Fraction) -> bool:
    """§0's side of the line, as `plan.SIDES` gives it."""
    line, side = plan.LINES[rid], plan.SIDES[rid]
    if side == ">=":
        return x >= line
    if side == "<=":
        return x <= line
    if side == "<":
        return x < line
    raise ValueError(f"no side {side!r} for {rid}")


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def read_run(record: dict) -> dict[str, Any]:
    """`placement.score.read_run`, the run's `whole(r)`, and its repetition,
    which pairs it with the other arm's run under the same draws."""
    got = pl_score.read_run(record)
    w = references.whole_share(record)
    got["whole"] = w["share"]
    got["whole_counts"] = w
    got["rep"] = record.get("rep")
    return got


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
    return m["v1d"] / m["v1c"] if m["v1c"] else None


ROWS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "WR-a": (("v1d",), "whole", lambda m: m["v1d"]),
    "WR-b": (("v1d",), "oncall", lambda m: m["v1d"]),
    "WR-c": (("v1c", "v1d"), "refused", ratio),
    "WR-d": (("v1c", "v1d"), "space", lambda m: m["v1c"] - m["v1d"]),
    "WR-e": (("v1c",), "oncall", lambda m: m["v1c"]),
}
PAIRED: dict[str, str] = {"WR-f": "oncall"}
ALL_ROWS = (*ROWS, *PAIRED)


def paired_row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    """`WR-f`: run `k` of v1d less run `k` of v1c, the median over the pairs."""
    key = PAIRED[rid]
    by = {a: {r["rep"]: r for r in runs[a]} for a in ("v1c", "v1d")}
    reps = sorted(set(by["v1c"]) & set(by["v1d"]))
    diffs = [F(by["v1d"][k][key]) - F(by["v1c"][k][key]) for k in reps]
    per_run = {"pairs": [[k, str(d)] for k, d in zip(reps, diffs)]}
    if len(diffs) < 2:
        return verdict(rid, None, False, "fewer than two pairs of runs", per_run=per_run)
    v = median(diffs)
    thin = any(holds(rid, d) != holds(rid, v) for d in diffs)
    return verdict(rid, v, thin, None, per_run=per_run)


def row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    if rid in PAIRED:
        return paired_row(rid, runs)
    arms, key, stat = ROWS[rid]
    vals = {a: [F(r[key]) for r in runs[a] if r[key] is not None] for a in arms}
    per_run = {a: [None if r[key] is None else str(F(r[key])) for r in runs[a]] for a in arms}
    short = [a for a in arms if len(vals[a]) < 2]
    if short:
        return verdict(rid, None, False, f"arm(s) {short} with fewer than two runs with a "
                                         f"value of {key}", per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    if v is None:
        return verdict(rid, None, False, "v1c's median refused(r) is 0", per_run=per_run)
    return verdict(rid, v, thin, None, per_run=per_run)


# ---------------------------------------------------------------------------
# WR-g, reported
# ---------------------------------------------------------------------------

def list_sizes(record: dict) -> dict[str, Any]:
    """The size of every list a placement round was sent, by the draft's
    queue, their median, and every round's size with its verdict, so that
    refusals can be read by the length of the list (§13)."""
    sizes: dict[str, list[int]] = {}
    rounds = []
    for esc in record["escalations"]:
        if esc.get("listed"):
            q = ((esc.get("calls") or [{}])[0].get("payload") or {}).get("action")
            sizes.setdefault(str(q), []).append(len(esc["listed"]))
            rounds.append([len(esc["listed"]), esc["verdict"],
                           pl_score.unplaced_with_an_answer(esc)])
    every = sorted(n for xs in sizes.values() for n in xs)
    return {"rounds": len(every), "median": str(median([F(n) for n in every])) if every else None,
            "max": max(every, default=None),
            "by_queue": {q: sorted(xs) for q, xs in sorted(sizes.items())},
            "size_verdict_unplaced": sorted(rounds)}


def beside_placement(rep: int) -> dict[str, Any]:
    """`PLAN_PLACEMENT.md`'s run `v1c r<rep>`, under the same draws, read as this
    plan's runs are read."""
    rec = json.loads(pl_plan.run_path("v1c", rep).read_text())
    got = read_run(rec)
    return {"space": frac(got["space"]), "oncall": frac(got["oncall"]),
            "refused": frac(got["refused"]), "whole": frac(got["whole"]),
            "calls": got["calls"],
            "dates": [rec.get("first_kept"), rec.get("started_at"),
                      rec.get("_env", {}).get("recorded_at")]}


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sample: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}}
    refs = sample["references"]
    inside = MI.space().full & ~MI.outside()
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            eng, rep = r["engine"], rec["rep"]
            co = MI.over_corpus(eng)
            tx = refs["transcriber"][f"v1c_r{rep}"]
            w = r["whole_counts"]
            out["runs"][f"{a}_r{rep}"] = {
                "space": frac(r["space"]),
                "space_without_the_keyword": ch_score.exact(MI.over_space(eng, MI.outside())),
                "space_with_the_keyword": ch_score.exact(MI.over_space(eng, inside)),
                "recall_space": {q: [v["right"], v["of"]]
                                 for q, v in r["space_scored"]["recall"].items()},
                "corpus": [co["correct"], co["n"]],
                "recall_corpus": {q: [v["right"], v["of"]] for q, v in co["recall"].items()},
                "k_a": str(MI.k_a_exact(rec["rules"])), "cover": r["cover"],
                "rebuilt_is_the_run": r["rebuilt"],
                "online": {k: rec["metrics"].get(k) for k in ch_score.ONLINE},
                "refused": frac(r["refused"]),
                "whole": {k: w[k] for k in ("drafts", "right_queue", "held", "wrong_queue",
                                            "no_rule", "by_class", "by_queue",
                                            "held_by_breadth")},
                "whole_share": frac(w["share"]),
                "first_drafts": [{k: d[k] for k in ("idx", "governing", "action", "class",
                                                    "breadth", "verdict", "born")}
                                 for d in w["rows"]],
                "inside_whole_births": references.inside_whole_births(rec),
                "births": references.births_of(rec),
                "lost": references.lost_of(rec),
                "calls": pl_score.calls_of(rec), "calls_as_recorded": r["calls_as_recorded"],
                "rounds": pl_score.rounds_reported({**rec, "protocol": "v1c"}),
                "list_sizes": list_sizes(rec),
                "births_left_out": pl_score.births_left_out(rec),
                "edges": pl_score.edges_of(rec), "cycle_refused": pl_score.cycle_refused(rec, eng),
                "reports": ch_score.reports_of(rec),
                "transcriber": {k: tx[k] for k in ("escalations", "impasses", "conflicts",
                                                   "errors", "calls", "space_right",
                                                   "space_points", "corpus_right",
                                                   "recall_oncall")},
                "verdicts": ch_score.verdicts_with_finish(rec),
                "placements": rl_score.placements_of(rec),
                "births_against_the_list": rl_score.births_against_the_list(rec),
                "rare": rl_score.rare_of(rec, eng),
                "placements_run_under_the_same_draws": f"v1c_r{rep}",
                "dates": [rec.get("first_kept"), rec.get("started_at"),
                          rec.get("_env", {}).get("recorded_at")]}
    out["cycle_refused"] = {}
    for a in plan.ARMS:
        edges = [x for k, run in out["runs"].items() if k.startswith(f"{a}_")
                 for x in run["cycle_refused"]["edges"]]
        out["cycle_refused"][a] = {"refused": len(edges), **pl_score.cycle_summary(edges)}
    out["direction"] = {}
    for a in plan.ARMS:
        rows_by_run = [r["edges"] for r in runs[a]]
        got = {"declared": rl_score.direction(rows_by_run),
               "ranking": rl_score.direction(rows_by_run, predict=brows.stage_c_names)}
        for d in got.values():
            d["reading"] = frac(d["reading"]) if d["reading"] is not None else None
        out["direction"][a] = got
    out["placements_v1c_runs"] = {f"v1c_r{rep}": beside_placement(rep)
                                  for rep in range(1, pl_plan.REPS + 1)}
    return out


def score(records: dict[str, list[dict]], sample: dict[str, Any]) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    verdicts = {rid: row(rid, runs) for rid in ALL_ROWS}
    return {"verdicts": verdicts, "WR-g": reported(runs, records, sample),
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
    ap = argparse.ArgumentParser(description="Stage C of PLAN_WHOLE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run WR-g1 to WR-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("whole/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if not plan.sample_path().exists():
        sys.exit("\nREFUSED: no Stage A record; nothing was written.\n")
    sample = json.loads(plan.sample_path().read_text())
    records, missing = read_records()
    scored = score(records, sample)
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(), "missing_runs": missing,
              **scored}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in scored["verdicts"].items():
        print(f"  {rid}  {v['verdict']}{', thin' if v.get('thin') else ''}")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
