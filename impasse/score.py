"""
Stage C of `PLAN_IMPASSE.md`: scoring, and the six adjudications (§10). **Free,
and gated**: it refuses while §0 is unsigned, because what the gate protects is
the order of events, not money (§11 of the plan).

THE ROWS ARE §0's, AND ALL OF THEIR TERMS ARE SETTLED THERE, NOT HERE.

  IM-a  the median over v1n's runs of `whole_I(r)`, less the median over v1c's;
        holds at or above 1/5. A run with no right-queue first-call draft at an
        impasse has no `whole_I(r)`, and the row reads the runs that have one.
  IM-b  `whole_D` over v1n's runs pooled; holds strictly below 1/3. No value with
        fewer than `plan.IM_B_MIN` right-queue drafts at the defaults' impasses.
        Thin when leaving any one of v1n's runs out puts the share on the other
        side of the line.
  IM-c  the median over v1n's runs of `space(B)`, less the median over v1c's;
        holds at or above 1/100.
  IM-d  the median over v1c's runs of `space(B)`, less the median over v1n's;
        holds at or below 1/40.
  IM-e  the median over v1n's runs of `impasses(r)`, over the median over v1c's;
        holds at or below 3/4. No value when v1c's median is 0.
  IM-f  the median over v1n's runs of `born_W(r)`; holds at or above 3/4. A run
        with no whole first-call draft at an impasse has none, and the row reads
        the runs that have one.

Every statistic is a fraction of counts, compared with its line exactly. A row
that reads an arm with fewer than two runs with a value has no value. A verdict on
medians is thin when any one run, put in place of its arm's median, puts the
statistic on the other side of its line. `space(B)`, the recall and `refused(r)`
are `placement/score.py`'s, called; `whole_I`, `whole_D`, `born_W` and
`impasses` are `impasse/references.py`'s.

`IM-g` is reported and adjudicates nothing.

    python3 -m impasse.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m impasse.score
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
from whole import plan as wh_plan
from whole import references as W
from whole import score as wh_score

from . import gates, plan, references as R

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median


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
    """`placement.score.read_run`, and this plan's statistics of the run."""
    got = pl_score.read_run(record)
    drafts = R.drafts_of(record)
    imp = R.counted(R.at(drafts, plan.IMPASSE))
    got.update({"drafts": drafts, "whole_I_counts": imp, "whole_I": R.share(imp),
                "whole_D_counts": R.at_the_defaults(drafts),
                "born_counts": R.born_of(drafts), "born_W": R.born_w(drafts),
                "impasses": R.impasses(record), "rep": record.get("rep")})
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
    return m["v1n"] / m["v1c"] if m["v1c"] else None


ROWS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "IM-a": (("v1c", "v1n"), "whole_I", lambda m: m["v1n"] - m["v1c"]),
    "IM-c": (("v1c", "v1n"), "space", lambda m: m["v1n"] - m["v1c"]),
    "IM-d": (("v1c", "v1n"), "space", lambda m: m["v1c"] - m["v1n"]),
    "IM-e": (("v1c", "v1n"), "impasses", ratio),
    "IM-f": (("v1n",), "born_W", lambda m: m["v1n"]),
}
POOLED: dict[str, tuple[str, str]] = {"IM-b": ("v1n", "whole_D_counts")}
ALL_ROWS = ("IM-a", "IM-b", "IM-c", "IM-d", "IM-e", "IM-f")


def pooled_row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    """`IM-b`: the share pooled over the arm's runs, thin when leaving any one
    run out puts it on the other side of the line."""
    arm, key = POOLED[rid]
    counts = [list(r[key]) for r in runs[arm]]
    per_run = {arm: [[r["rep"], c] for r, c in zip(runs[arm], counts)]}
    held, of = sum(c[0] for c in counts), sum(c[1] for c in counts)
    if len(counts) < 2:
        return verdict(rid, None, False, f"arm {arm} with fewer than two runs",
                       per_run=per_run, pooled=[held, of])
    if of < plan.IM_B_MIN:
        return verdict(rid, None, False, f"{of} right-queue drafts at the defaults' impasses, "
                                         f"fewer than {plan.IM_B_MIN}",
                       per_run=per_run, pooled=[held, of])
    v = F(held, of)
    thin = any(of - c[1] and holds(rid, F(held - c[0], of - c[1])) != holds(rid, v)
               for c in counts)
    return verdict(rid, v, thin, None, per_run=per_run, pooled=[held, of])


def row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    if rid in POOLED:
        return pooled_row(rid, runs)
    arms, key, stat = ROWS[rid]
    vals = {a: [F(r[key]) for r in runs[a] if r[key] is not None] for a in arms}
    per_run = {a: [None if r[key] is None else str(F(r[key])) for r in runs[a]] for a in arms}
    short = [a for a in arms if len(vals[a]) < 2]
    if short:
        return verdict(rid, None, False, f"arm(s) {short} with fewer than two runs with a "
                                         f"value of {key}", per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    if v is None:
        return verdict(rid, None, False, "v1c's median impasses(r) is 0", per_run=per_run)
    return verdict(rid, v, thin, None, per_run=per_run)


# ---------------------------------------------------------------------------
# IM-g, reported
# ---------------------------------------------------------------------------

def firsts_by_queue(drafts: list[dict]) -> dict[str, dict[str, Any]]:
    """Each queue's first escalated ticket in the run, with its cause and its
    draft."""
    _, _, _, _, queues = R._world()
    out: dict[str, dict[str, Any]] = {}
    for d in sorted(drafts, key=lambda x: x["idx"]):
        q = queues[d["governing"]]
        if q not in out:
            out[q] = {k: d[k] for k in ("idx", "governing", "cause", "class", "verdict")}
    return dict(sorted(out.items()))


def paired(runs: dict[str, list[dict]], key: str, op: Callable) -> list[list[Any]]:
    """Run `k` of v1n against run `k` of v1c, under the draws both read."""
    by = {a: {r["rep"]: r for r in runs[a]} for a in plan.ARMS}
    out = []
    for k in sorted(set(by["v1c"]) & set(by["v1n"])):
        a, b = by["v1n"][k][key], by["v1c"][k][key]
        out.append([k, None if a is None or b is None or op(F(a), F(b)) is None
                    else str(op(F(a), F(b)))])
    return out


def beside_earlier(rep: int) -> dict[str, Any]:
    """`PLAN_PLACEMENT.md`'s v1c run, and `PLAN_WHOLE.md`'s v1c and v1d runs, of
    the same draws, read as this plan's runs are read."""
    out = {}
    for name, path in ((f"placement_v1c_r{rep}", pl_plan.run_path("v1c", rep)),
                       (f"whole_v1c_r{rep}", wh_plan.run_path("v1c", rep)),
                       (f"whole_v1d_r{rep}", wh_plan.run_path("v1d", rep))):
        rec = json.loads(path.read_text())
        got = read_run(rec)
        out[name] = {"space": frac(got["space"]), "oncall": frac(got["oncall"]),
                     "refused": frac(got["refused"]), "whole_I": frac(got["whole_I"]),
                     "born_W": frac(got["born_W"]), "impasses": got["impasses"],
                     "whole_D_counts": got["whole_D_counts"], "calls": got["calls"]}
    return out


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sample: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}}
    refs = sample["references"]
    inside = MI.space().full & ~MI.outside()
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            eng, rep, ds = r["engine"], rec["rep"], r["drafts"]
            co = MI.over_corpus(eng)
            tx = refs["transcriber"][f"v1c_r{rep}"]
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
                "impasses": r["impasses"],
                "escalations_by_cause": {c: sum(1 for x in rec["escalations"] if x["kind"] == c)
                                         for c in plan.CAUSES},
                "whole_I_counts": r["whole_I_counts"], "whole_I": frac(r["whole_I"]),
                "whole_by_cause": R.by_cause(ds), "whole_by_group": R.by_group(ds),
                "whole_D_counts": r["whole_D_counts"], "defaults_met": R.defaults_met(ds),
                "born": r["born_counts"], "born_W": frac(r["born_W"]),
                "notice_at": len(rec.get("notice_at") or []),
                "first_drafts": [{k: d[k] for k in ("idx", "governing", "group", "cause",
                                                    "action", "class", "breadth", "verdict",
                                                    "born")} for d in ds],
                "firsts_by_queue": firsts_by_queue(ds),
                "h01_case_44": R.h01_case_44(rec, ds),
                "inside_whole_births": W.inside_whole_births(rec),
                "births": W.births_of(rec),
                "lost": R.lost_by_causes(rec),
                "calls": pl_score.calls_of(rec), "calls_as_recorded": r["calls_as_recorded"],
                "rounds": pl_score.rounds_reported({**rec, "protocol": "v1c"}),
                "list_sizes": wh_score.list_sizes(rec),
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
    out["paired"] = {"whole_I": paired(runs, "whole_I", lambda x, y: x - y),
                     "space": paired(runs, "space", lambda x, y: x - y),
                     "impasses": paired(runs, "impasses", lambda x, y: x / y if y else None),
                     "born_W": paired(runs, "born_W", lambda x, y: x - y)}
    out["whole_D_v1c"] = R.counted([d for r in runs["v1c"] for d in R.at(r["drafts"],
                                                                         plan.IMPASSE)
                                    if d["governing"] in plan.DEFAULTS])
    out["beside_earlier"] = {f"r{rep}": beside_earlier(rep) for rep in range(1, plan.REPS + 1)}
    return out


def score(records: dict[str, list[dict]], sample: dict[str, Any]) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    verdicts = {rid: row(rid, runs) for rid in ALL_ROWS}
    return {"verdicts": verdicts, "IM-g": reported(runs, records, sample),
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
    ap = argparse.ArgumentParser(description="Stage C of PLAN_IMPASSE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run IM-g1 to IM-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("impasse/score.py writes Stage C")
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
