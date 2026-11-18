"""
Stage C of `PLAN_RANKED.md`: scoring, and the six adjudications (§10). **Free,
and gated**: it refuses while §0 is unsigned, because what the gate protects is
the order of events, not money (§11 of the plan).

THE ROWS ARE §0's, AND ALL OF THEIR TERMS ARE SETTLED THERE, NOT HERE.

  RK-a  every complete K run's ranking puts `SECURITY_INCIDENT` first. It reads
        a count of runs, so it is never thin.
  RK-b  the median over K's runs of `space(B)`, less the median over L's; holds
        at or above 1/10.
  RK-c  the median over K's runs of `recall_SECURITY_INCIDENT(B)` over the
        space; holds at or above 1/2.
  RK-d  the median over K's runs of `space(B)` less `space(A(r))`; holds at or
        above 0. A run without a valid at-once ask at all of its labels has no
        value.
  RK-e  the median over K's runs of `taken(r)`, the share decided right of the
        cases the ranking decided; holds at or above 1/2. A run in which the
        ranking decided no case has no value.
  RK-f  the median over K's runs of `recall_ONCALL_ESCALATION(B)` over the
        space; holds at or above 9/10.

`space(B)` and the recalls are read as the run's own engine decides: rung 2's in
arm `l`, and in arm `k` rung 2's with the ranking at every CONFLICT
(`ranked/reading.py`). Every statistic is a fraction of counts, compared with
its line exactly. A row that reads an arm with fewer than two runs with a value
has no value. A verdict on medians is thin when any one run, put in place of its
arm's median, puts the statistic on the other side of its line; for `RK-d`, any
one run's difference put in place of the median.

`RK-g` is reported and adjudicates nothing.

    python3 -m ranked.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m ranked.score
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from typing import Any, Callable

from harness.domain import ACTIONS
from harness.provenance import describe, environment

from corrections import ask as cr_ask
from corrections import learners
from corrections import plan as cr_plan
from corrections import run as cr_run
from corrections import score as cr_score
from manual import instrument as MI
from placement import score as pl_score
from reasoned_loop import score as rl_score

from . import engine as E
from . import gates, plan
from . import reading as R
from . import run as rrun

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median
LAYER_BELOW_ONCALL = ("H06", "H07", "H08")


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def engines_decision(row: dict[str, Any]) -> str | None:
    """What the engine decided at a case: at a reported error the record keeps
    it apart, because the row's own answer is then the proposer's."""
    return row["engine_action"] if row["cause"] == plan.ERROR else row["predicted"]


def taken_by_the_ranking(record: dict[str, Any]) -> dict[str, int] | None:
    """Of arm K's cases, those its ranking decided: how many, how many right,
    and what became of the wrong ones. None in arm L."""
    kept = record.get("ranked")
    if not kept:
        return None
    out = {"cases": 0, "right": 0, "wrong_reported": 0, "wrong_silent": 0, "on_a_tie": 0}
    for row, case in zip(record["records"], kept["cases"]):
        if case["by"] != E.RANKING:
            continue
        out["cases"] += 1
        out["on_a_tie"] += case["votes_for"] == case["votes_against"]
        if engines_decision(row) == row["truth"]:
            out["right"] += 1
        elif row["cause"] == plan.ERROR:
            out["wrong_reported"] += 1
        else:
            out["wrong_silent"] += 1
    return out


def read_run(record: dict[str, Any]) -> dict[str, Any]:
    """`placement.score.read_run`, and this plan's statistics: the base read as
    its own engine decides, after every birth and at the end."""
    got = pl_score.read_run(record)
    space, truth = MI.space(), MI.space_truth()
    n = space.n
    went = R.as_it_went(record, space, truth)
    final = went["final"]
    arm = record.get("arm")
    own = "ranked" if arm == plan.RANKED else "rung2"
    recall = R.recall_of(final[own], truth)
    taken = taken_by_the_ranking(record)
    got.update(
        arm=arm, rep=record.get("rep"), own=own, went=went,
        rung2=F(final["rung2"].bit_count(), n), ranked=F(final["ranked"].bit_count(), n),
        recall={q: F(*recall[q]) for q in ACTIONS}, ranking=list(went["tally"].ranking),
        handed=cr_run.handed_check(record, cr_plan.LABELLED),
        engine_record=rrun.ranked_check(record), taken_counts=taken,
        taken=(F(taken["right"], taken["cases"]) if taken and taken["cases"] else None),
        # The reading after every birth ends where `placement.score` reads the base.
        sound=went["sound"] and F(final["rung2"].bit_count(), n) == got["space"])
    got["space"] = got[own]
    got["security"], got["oncall"] = got["recall"][plan.SECURITY], got["recall"][plan.ONCALL]
    return got


# ---------------------------------------------------------------------------
# The six rows
# ---------------------------------------------------------------------------

def verdict(rid: str, value: Fraction | None, thin: bool, why: str | None,
            **parts) -> dict[str, Any]:
    line = plan.LINES[rid]
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "holds_at": ">=", "thin": False, **parts}
    return {"verdict": HOLDS if value >= line else REFUTED, "value": frac(value),
            "line": frac(line), "holds_at": ">=", "thin": thin, "why": None, **parts}


def median_row(rid: str, values: dict[str, list[Fraction]],
               stat: Callable[[dict[str, Fraction]], Fraction]) -> tuple[Fraction, bool]:
    """The statistic over the arms' medians, and whether any one run put in
    place of its arm's median puts it on the other side of the line."""
    line = plan.LINES[rid]
    meds = {a: median(xs) for a, xs in values.items()}
    v = stat(meds)
    thin = any((stat({**meds, a: x}) >= line) != (v >= line)
               for a, xs in values.items() for x in xs)
    return v, thin


MEDIANS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "RK-b": (("k", "l"), "space", lambda m: m["k"] - m["l"]),
    "RK-c": (("k",), "security", lambda m: m["k"]),
    "RK-e": (("k",), "taken", lambda m: m["k"]),
    "RK-f": (("k",), "oncall", lambda m: m["k"]),
}


def rk_a(runs: dict[str, list[dict]]) -> dict[str, Any]:
    """Every complete K run's ranking puts `SECURITY_INCIDENT` first."""
    firsts = {str(r["rep"]): r["ranking"][0] for r in runs[plan.RANKED]}
    if len(firsts) < 2:
        return {"verdict": NO_VALUE, "why": "fewer than two complete K runs", "value": None,
                "line": "every complete K run", "thin": False, "per_run": firsts}
    put = sum(1 for q in firsts.values() if q == plan.SECURITY)
    return {"verdict": HOLDS if put == len(firsts) else REFUTED, "value": [put, len(firsts)],
            "line": "every complete K run", "thin": False, "why": None, "per_run": firsts}


def rk_d(runs: dict[str, list[dict]], extra: dict[str, dict]) -> dict[str, Any]:
    diffs, per_run = [], {}
    for r in runs[plan.RANKED]:
        other = extra.get(plan.tag(plan.RANKED, r["rep"]), {}).get("at_once_all")
        if other is None:
            per_run[str(r["rep"])] = None
            continue
        diffs.append(r["space"] - other)
        per_run[str(r["rep"])] = str(r["space"] - other)
    if len(diffs) < 2:
        return verdict("RK-d", None, False, "fewer than two of K's runs with a value",
                       per_run=per_run)
    v = median(diffs)
    line = plan.LINES["RK-d"]
    thin = any((d >= line) != (v >= line) for d in diffs)
    return verdict("RK-d", v, thin, None, per_run=per_run)


def row(rid: str, runs: dict[str, list[dict]], extra: dict[str, dict]) -> dict[str, Any]:
    if rid == "RK-a":
        return rk_a(runs)
    if rid == "RK-d":
        return rk_d(runs, extra)
    arms, key, stat = MEDIANS[rid]
    vals = {a: [F(r[key]) for r in runs[a] if r[key] is not None] for a in arms}
    per_run = {a: [None if r[key] is None else str(F(r[key])) for r in runs[a]] for a in arms}
    short = [a for a in arms if len(vals[a]) < 2]
    if short:
        return verdict(rid, None, False, f"arm(s) {short} with fewer than two runs with a "
                                         f"value of {key}", per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    return verdict(rid, v, thin, None, per_run=per_run)


# ---------------------------------------------------------------------------
# RK-g, reported
# ---------------------------------------------------------------------------

def ranking_reported(r: dict[str, Any]) -> dict[str, Any]:
    """The ranking a run's votes chose as its births came: arm K's engine's, and
    in arm L what its votes would have chosen."""
    curve = r["went"]["curve"]
    final = curve[-1]["ranking"] if curve else 0
    return {"final": r["ranking"], "votes": r["went"]["tally"].final()["votes"],
            "n_votes": sum(r["went"]["tally"].votes.values()),
            "changes": sum(1 for a, b in zip(curve, curve[1:]) if a["ranking"] != b["ranking"]),
            "security_first_from": settled(curve, lambda p: E.rankings()[p["ranking"]][0]
                                           == plan.SECURITY),
            "final_from": settled(curve, lambda p: p["ranking"] == final)}


def settled(curve: list[dict[str, Any]], test) -> int | None:
    """The first birth, by its place in the curve from 1, from which `test` holds
    for good."""
    out = None
    for i, p in enumerate(curve, start=1):
        if test(p):
            out = i if out is None else out
        else:
            out = None
    return out


def reports_reported(record: dict[str, Any]) -> dict[str, Any]:
    """The reported errors by decile of the arrivals and by true queue."""
    truth = {r["idx"]: r["truth"] for r in record["records"]}
    errors = [e["idx"] for e in record["escalations"] if e["kind"] == plan.ERROR]
    by_queue: dict[str, int] = {}
    for i in errors:
        by_queue[truth[i]] = by_queue.get(truth[i], 0) + 1
    width = plan.N // 10
    return {"by_decile": [sum(1 for i in errors if i // width == d) for d in range(10)],
            "by_queue": by_queue}


def nested_in_the_keyword(r: dict[str, Any]) -> list[dict[str, Any]]:
    """The rules of other queues wholly inside the keyword's region, and the
    points of `SECURITY_INCIDENT` inside each that the base decides wrongly."""
    eng = r["engine"]
    space, truth = MI.space(), MI.space_truth()
    keyword = space.mask["has_security_keyword"][True]
    right = r["went"]["final"][r["own"]]
    out = []
    for rule in eng.rules:
        ext = eng.ext[rule.rule_id]
        if rule.action == plan.SECURITY or ext & ~keyword:
            continue
        inside = ext & truth.get(plan.SECURITY, 0)
        out.append({"rule_id": rule.rule_id, "queue": rule.action, "born_at": rule.born_at,
                    "points": ext.bit_count(), "security_points": inside.bit_count(),
                    "security_points_wrong": (inside & ~right).bit_count()})
    return out


def layer_below_oncall(r: dict[str, Any]) -> list[int]:
    """The points of the policy's layer below the rarest queue that the base
    decides right, and the layer's points."""
    regions = MI.hidden_regions()
    layer = 0
    for h in LAYER_BELOW_ONCALL:
        layer |= regions[h]["mask"]
    return [(r["went"]["final"][r["own"]] & layer).bit_count(), layer.bit_count()]


def run_reported(r: dict[str, Any], record: dict[str, Any], closed: dict[str, Any] | None,
                 zero: dict[str, Any] | None) -> dict[str, Any]:
    n = MI.space().n
    keyword = MI.space().mask["has_security_keyword"][True]
    right = r["went"]["final"][r["own"]]
    curve = r["went"]["curve"]
    causes: dict[str, int] = {}
    for esc in record["escalations"]:
        causes[esc["kind"]] = causes.get(esc["kind"], 0) + 1
    engine = (R.engine_of(r["engine"], record) if r["arm"] == plan.RANKED else r["engine"])
    num, den = cr_score.followed(record)
    asked = None
    if r["arm"] == plan.CONTROL:
        cases = list(R.asked_conflicts(record, list(MI.corpus()), MI.space()))
        asked = {"cases": len(cases),
                 "ranking_right": sum(1 for c in cases if c["decided"] == c["truth"]),
                 "first_call_right": gates.first_call_right(record)}
    return {
        "arm": r["arm"], "engine": plan.ENGINE[r["arm"]], "space": frac(r["space"]),
        "under_rung2": frac(r["rung2"]), "under_the_ranking": frac(r["ranked"]),
        "keyword_half": [(right & keyword).bit_count(), (right & ~keyword).bit_count()],
        "recall": {q: frac(r["recall"][q]) for q in ACTIONS},
        "ranking": ranking_reported(r),
        "curve": {"births": len(curve), "points": n,
                  "rung2": R.summary(curve, "rung2"), "ranked": R.summary(curve, "ranked")},
        "taken_by_the_ranking": r["taken_counts"], "asked_conflicts": asked,
        "corpus": cr_score.corpus_split(record, engine),
        "escalations": causes, "stopped_at_the_cap": record.get("v1b", {}).get("stopped_at"),
        "empty_objects": sum(1 for esc in record["escalations"] for c in esc.get("calls") or []
                             if c.get("payload") == {}),
        "labels": len(record.get("reports_handed") or {}), "handed": r["handed"][1],
        "engine_record": r["engine_record"][1], "followed": [num, den],
        "refused": frac(r["refused"]), "calls": r["calls"],
        "reports": reports_reported(record),
        "layer_below_oncall": layer_below_oncall(r),
        "nested_in_the_keyword": nested_in_the_keyword(r),
        "rounds": pl_score.rounds_reported(record), "edges": pl_score.edges_of(record),
        "calls_made": pl_score.calls_of(record),
        "closed_l_under_the_same_draws": closed, "transcriber_under_the_same_draws": zero,
    }


def at_checkpoints(r: dict[str, Any], record: dict[str, Any],
                   asked: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    """At every checkpoint: the base as its own engine read it after the same
    label, and the at-once asks on the labels up to it."""
    n = MI.space().n
    pairs = cr_ask.labelled(record)
    out = []
    for j in plan.checkpoints(len(pairs)):
        idx = pairs[j - 1][0]
        then = R.at_case(r["went"]["curve"], idx)
        out.append({"labels": j, "case": idx,
                    "loop": None if then is None else frac(F(then[r["own"]], n)),
                    "at_once": None if j not in asked else
                    {**asked[j], "space": frac(asked[j]["space"])}})
    return out


def closed_l() -> dict[str, dict[str, Any]]:
    """`PLAN_CORRECTIONS.md`'s L runs, as its Stage C keeps them: another period,
    set beside the runs under the same draws and adjudicating nothing."""
    path = cr_plan.score_path()
    if not path.exists():
        return {}
    kept = json.loads(path.read_text())["CR-g"]["runs"]
    return {str(k): {"space": kept[f"l_r{k}"]["space"],
                     "security": kept[f"l_r{k}"]["recall"][plan.SECURITY],
                     "oncall": kept[f"l_r{k}"]["recall"][plan.ONCALL],
                     "escalations": kept[f"l_r{k}"]["escalations"]}
            for k in range(1, cr_plan.REPS + 1) if f"l_r{k}" in kept}


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sessions: dict[str, dict], extra: dict[str, dict],
             sample: dict[str, Any] | None) -> dict[str, Any]:
    closed = closed_l()
    zero = ((sample or {}).get("references") or {}).get("step_zero") or {}
    out: dict[str, Any] = {"runs": {}, "curves": {}, "learners": {}, "prior": None}
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            tag = plan.tag(a, r["rep"])
            out["runs"][tag] = run_reported(r, rec, closed.get(str(r["rep"])),
                                            zero.get(f"r{r['rep']}"))
            out["curves"][tag] = extra[tag]["curve"]
            out["learners"][tag] = extra[tag]["learners"]
    if "prior" in sessions:
        out["prior"] = {str(j): {**v, "space": frac(v["space"])}
                        for j, v in cr_score.at_once(sessions["prior"]).items()}
    return out


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def score(records: dict[str, list[dict]], sessions: dict[str, dict],
          sample: dict[str, Any] | None = None, with_learners: bool = True) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    extra: dict[str, dict] = {}
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            tag = plan.tag(a, r["rep"])
            session = sessions.get(plan.session_of(a, r["rep"]))
            pairs = cr_ask.labelled(rec)
            asked = cr_score.at_once(session) if session else {}
            trained = learners.trained(pairs) if with_learners and pairs else None
            b = learners.best(trained) if trained else None
            extra[tag] = {"at_once_all": (asked.get(len(pairs)) or {}).get("space"),
                          "curve": at_checkpoints(r, rec, asked),
                          "learners": {"trained": trained,
                                       "best": None if b is None
                                       else frac(F(b, cr_score.SPACE_N))}}
    verdicts = {rid: row(rid, runs, extra) for rid in plan.ROWS}
    every = [r for a in plan.ARMS for r in runs[a]]
    return {"verdicts": verdicts, "RK-g": reported(runs, records, sessions, extra, sample),
            "rebuilt_is_the_run": all(r["rebuilt"] and r["sound"] for r in every),
            "calls_as_recorded": all(r["calls_as_recorded"] for r in every),
            "labels_by_their_route": all(r["handed"][0] for r in every),
            "engines_as_recorded": all(r["engine_record"][0] for r in every)}


def read_records() -> tuple[dict[str, list[dict]], dict[str, dict], list[str]]:
    out: dict[str, list[dict]] = {a: [] for a in plan.ARMS}
    missing = []
    for a, rep in plan.schedule():
        path = plan.run_path(a, rep)
        if path.exists():
            out[a].append(json.loads(path.read_text()))
        else:
            missing.append(f"{a} r{rep}")
    sessions = {s: json.loads(plan.ask_path(s).read_text()) for s in plan.sessions()
                if plan.ask_path(s).exists()}
    missing += [f"session {s}" for s in plan.sessions() if s not in sessions]
    return out, sessions, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_RANKED.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run RK-g1 to RK-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("ranked/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if not plan.sample_path().exists():
        sys.exit("\nREFUSED: no Stage A record; nothing was written.\n")
    records, sessions, missing = read_records()
    sample = json.loads(plan.sample_path().read_text())
    scored = score(records, sessions, sample)
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
