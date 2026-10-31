"""
Stage C of `PLAN_REASONED_LOOP.md`: scoring, and the seven adjudications (§10).
**Free, and gated**: it refuses while §0 is unsigned.

EVERY STATISTIC IS A FRACTION OF COUNTS, compared with its line exactly (§0).

  RL-a  the right drafts over the escalations, pooled over both arms' runs. A
        draft is the queue the first call named; a first call that never came
        back is a draft not right.
  RL-b  the share of the impasse arm's runs whose `cover` falls before case 200.
  RL-c  the error arm's median `space` less the impasse arm's.
  RL-d  the error arm's median `space`.
  RL-e  the direction of the placed edges, beyond the keyword, by older rule,
        pooled over both arms' runs: `blind.rows`' units and verdicts, read
        exactly. `blind.rows.direction` gives the same reading as a float, and
        the record keeps it beside, so the population is visibly its.
  RL-f  RL-e's reading less the Stage C ranking's, on the same pairs and units.
  RL-g  the error arm's median recall of `ONCALL_ESCALATION` over the space.

THE POPULATION OF RL-e AND RL-f is `blind.rows.edge_rows`' edges, accepted and
entered in the graph, declared at a birth (the write channel), between rules of
different queues, neither of them a keyword rule. Unlike `K-b`'s, it is not cut
to births on an impasse: under v1b every escalation drafts blind and places.

*thin* AND *no value* ARE §0's, settled there and applied here as written: a
pooled row is thin when dropping any one run puts it on the other side, a median
row when any one run of either arm put in place of its arm's median does, and
RL-b when one run on the other side does. A row that reads an arm with fewer
than two runs has no value, nor RL-a under 60 escalations, nor RL-e and RL-f
under 20 units.

A RUN'S BASE is `manual.instrument.final_engine`'s rebuild of its record, held
here to the rules and edges the record says the run ended with.

    python3 -m reasoned_loop.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m reasoned_loop.score
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

from authorship import protocol as e
from blind import readings as breadings
from blind import rows as brows
from manual import instrument as MI
from reasoned_rule import shape
from rung2.engine2 import strictly_below

from . import gates, plan, references

F = Fraction
HOLDS, REFUTED, NO_VALUE = "holds", "refuted", "unadjudicable"


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": str(x), "value": float(x)}


def side(x: Fraction, line: Fraction) -> bool:
    """Every line of §0 holds at or above it."""
    return x >= line


def median(xs: list[Fraction]) -> Fraction:
    """The middle of three runs, the mean of two."""
    s = sorted(xs)
    k = len(s)
    return s[k // 2] if k % 2 else (s[k // 2 - 1] + s[k // 2]) / 2


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def placed_edge(row: dict) -> bool:
    """RL-e's population: an edge a birth declared, between two queues, neither
    rule a keyword rule."""
    return row["channel"] == e.WRITE and not row["same_queue"] and not row["keyword"]


def recorded_edges(record: dict, engine) -> set[tuple[str, str]]:
    """The edges the record says the run entered in the graph: every accepted
    citation of its rules, less those nested in containment."""
    out = set()
    for r in record["rules"]:
        for ref in r.get("beats") or []:
            out.add((r["rule_id"], ref))
        for ref in r.get("loses_to") or []:
            out.add((ref, r["rule_id"]))
    return {(w, l) for w, l in out
            if not (strictly_below(engine.ext[w], engine.ext[l])
                    or strictly_below(engine.ext[l], engine.ext[w]))}


def drafts(record: dict) -> tuple[int, int]:
    """(right drafts, escalations)."""
    right = n = 0
    for esc in record["escalations"]:
        n += 1
        calls = esc.get("calls") or []
        first = calls[0] if calls else None
        named = (first.get("payload") or {}).get("action") if first and not first.get(
            "failure") else None
        right += named == record["records"][esc["idx"]]["truth"]
    return right, n


def read_run(record: dict) -> dict[str, Any]:
    eng = MI.final_engine(record)
    graph = {(w, l) for l, ws in eng.decl_below.items() for w in ws}
    rebuilt = ([(r.rule_id, r.born_at, r.action) for r in eng.rules]
               == [(r["rule_id"], r["born_at"], r["action"]) for r in record["rules"]]
               and graph == recorded_edges(record, eng))
    sp = MI.over_space(eng)
    rec = sp["recall"]["ONCALL_ESCALATION"]
    right, n = drafts(record)
    corpus = list(MI.corpus())
    truth = [r["truth"] for r in sorted(record["records"], key=lambda r: r["idx"])]
    cases_out = [i for i in brows.outside_cases(corpus) if i < len(truth)]
    rows = brows.edge_rows(record, eng, MI.space_truth(), MI.outside(),
                           sets=brows.sets_of(record["rules"], corpus[:len(truth)]),
                           truth=truth, cases_out=cases_out)
    cover = record["v1b"]["cover"]
    return {"engine": eng, "rebuilt": rebuilt,
            "space": F(sp["correct"], sp["n"]), "space_scored": sp,
            "oncall": F(rec["right"], rec["of"]),
            "drafts": (right, n), "cover": cover,
            "covers_early": cover is not None and cover < plan.COVER_BEFORE,
            "edges": rows}


# ---------------------------------------------------------------------------
# The direction, exactly
# ---------------------------------------------------------------------------

def direction(rows_by_run: list[list[dict]], key: str = "space_out",
              keep: Callable[[dict], bool] = placed_edge,
              predict: Callable[[dict], str] | None = None) -> dict[str, Any]:
    """`blind.rows.direction`'s reading by older rule, as a fraction: the mean
    over the units of each unit's share of strict pairs whose named rule is the
    better one."""
    units: dict[tuple[int, str], list[bool]] = collections.defaultdict(list)
    for k, rows in enumerate(rows_by_run):
        for row in rows:
            if not keep(row) or row.get(key) in (brows.TIE, brows.NEITHER, None):
                continue
            better = row["winner"] if row[key] == brows.HIT else row["loser"]
            named = row["winner"] if predict is None else predict(row)
            units[(k, row["older"])].append(named == better)
    reading = (sum((F(sum(v), len(v)) for v in units.values()), F(0)) / len(units)
               if units else None)
    return {"units": len(units), "reading": reading,
            "hits": sum(sum(v) for v in units.values()),
            "strict": sum(len(v) for v in units.values()),
            "float_reading": brows.direction(rows_by_run, key, keep=keep,
                                             predict=predict)["reading"]}


# ---------------------------------------------------------------------------
# The seven rows
# ---------------------------------------------------------------------------

def verdict(value: Fraction | None, line: Fraction, thin: bool, why: str | None,
            **parts) -> dict[str, Any]:
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "thin": False, **parts}
    return {"verdict": HOLDS if side(value, line) else REFUTED, "value": frac(value),
            "line": frac(line), "thin": thin, "why": None, **parts}


def enough(runs: dict[str, list[dict]], arms) -> str | None:
    short = [a for a in arms if len(runs[a]) < 2]
    return f"arm(s) {short} with fewer than two runs" if short else None


def rl_a(runs) -> dict[str, Any]:
    line = plan.RL_A_LINE
    per = [r["drafts"] for a in plan.ARMS for r in runs[a]]

    def value(xs):
        n = sum(x[1] for x in xs)
        return F(sum(x[0] for x in xs), n) if n else None
    v = value(per)
    why = enough(runs, plan.ARMS) or (
        f"{sum(x[1] for x in per)} escalations, under {plan.MIN_ESCALATIONS}"
        if sum(x[1] for x in per) < plan.MIN_ESCALATIONS else None)
    if why:
        return verdict(None, line, False, why, per_run=[list(x) for x in per])
    thin = any(side(value(per[:k] + per[k + 1:]), line) != side(v, line)
               for k in range(len(per)) if value(per[:k] + per[k + 1:]) is not None)
    return verdict(v, line, thin, None, per_run=[list(x) for x in per])


def rl_b(runs) -> dict[str, Any]:
    line = plan.RL_B_LINE
    hits = [r["covers_early"] for r in runs["i"]]
    covers = [r["cover"] for r in runs["i"]]
    why = enough(runs, ("i",))
    if why:
        return verdict(None, line, False, why, covers=covers)
    v = F(sum(hits), len(hits))
    thin = any(side(F(sum(hits) + (-1 if h else 1), len(hits)), line) != side(v, line)
               for h in hits)
    return verdict(v, line, thin, None, covers=covers)


def median_row(values: dict[str, list[Fraction]], line: Fraction,
               stat: Callable[[dict[str, Fraction]], Fraction]) -> tuple[Fraction, bool]:
    meds = {a: median(xs) for a, xs in values.items()}
    v = stat(meds)
    thin = any(side(stat({**meds, a: x}), line) != side(v, line)
               for a, xs in values.items() for x in xs)
    return v, thin


def rl_c(runs) -> dict[str, Any]:
    line = plan.RL_C_LINE
    vals = {a: [r["space"] for r in runs[a]] for a in plan.ARMS}
    why = enough(runs, plan.ARMS)
    if why:
        return verdict(None, line, False, why)
    v, thin = median_row(vals, line, lambda m: m["e"] - m["i"])
    return verdict(v, line, thin, None,
                   per_run={a: [str(x) for x in xs] for a, xs in vals.items()})


def rl_d(runs) -> dict[str, Any]:
    line = plan.RL_D_LINE
    vals = {"e": [r["space"] for r in runs["e"]]}
    why = enough(runs, ("e",))
    if why:
        return verdict(None, line, False, why)
    v, thin = median_row(vals, line, lambda m: m["e"])
    return verdict(v, line, thin, None, per_run=[str(x) for x in vals["e"]])


def rl_g(runs) -> dict[str, Any]:
    line = plan.RL_G_LINE
    vals = {"e": [r["oncall"] for r in runs["e"]]}
    why = enough(runs, ("e",))
    if why:
        return verdict(None, line, False, why)
    v, thin = median_row(vals, line, lambda m: m["e"])
    return verdict(v, line, thin, None, per_run=[str(x) for x in vals["e"]])


def rl_e_f(runs) -> tuple[dict[str, Any], dict[str, Any]]:
    rows_by_run = [r["edges"] for a in plan.ARMS for r in runs[a]]
    declared = direction(rows_by_run)
    ranking = direction(rows_by_run, predict=brows.stage_c_names)
    why = enough(runs, plan.ARMS) or (
        f"{declared['units']} units, under {plan.MIN_UNITS}"
        if declared["units"] < plan.MIN_UNITS else None)
    parts_e = {"units": declared["units"], "hits": declared["hits"],
               "strict": declared["strict"], "float_reading": declared["float_reading"]}
    if why:
        return (verdict(None, plan.RL_E_LINE, False, why, **parts_e),
                verdict(None, plan.RL_F_LINE, False, why))

    def dropped(k, predict=None):
        return direction(rows_by_run[:k] + rows_by_run[k + 1:], predict=predict)

    v_e = declared["reading"]
    v_f = declared["reading"] - ranking["reading"]
    thin_e = thin_f = False
    for k in range(len(rows_by_run)):
        d, rk = dropped(k), dropped(k, brows.stage_c_names)
        if d["reading"] is not None:
            thin_e |= side(d["reading"], plan.RL_E_LINE) != side(v_e, plan.RL_E_LINE)
            thin_f |= side(d["reading"] - rk["reading"], plan.RL_F_LINE) != side(
                v_f, plan.RL_F_LINE)
    return (verdict(v_e, plan.RL_E_LINE, thin_e, None, **parts_e),
            verdict(v_f, plan.RL_F_LINE, thin_f, None, ranking=frac(ranking["reading"]),
                    ranking_float=ranking["float_reading"]))


# ---------------------------------------------------------------------------
# RL-h, reported
# ---------------------------------------------------------------------------

def calls_of(record: dict) -> dict[str, Any]:
    calls = [c for esc in record["escalations"] for c in esc.get("calls") or []]
    attempts = [a for c in calls for a in c.get("call_attempts") or []]
    by_round = collections.defaultdict(list)
    for c in calls:
        if c.get("seconds") is not None:
            by_round[c["round"]].append(c["seconds"])
    reasoning = [a.get("reasoning_tokens") or 0 for a in attempts]
    return {"calls": len(calls), "attempts": len(attempts),
            "providers": dict(collections.Counter(a.get("provider") or "none"
                                                  for a in attempts)),
            "finish_reasons": dict(collections.Counter(a.get("finish_reason") or "none"
                                                       for a in attempts)),
            "prompt_tokens": sum(a.get("prompt_tokens") or 0 for a in attempts),
            "completion_tokens": sum(a.get("completion_tokens") or 0 for a in attempts),
            "reasoning_tokens": {"sum": sum(reasoning),
                                 "median": statistics.median(reasoning) if reasoning else None,
                                 "max": max(reasoning, default=None)},
            "seconds_by_round": {str(k): {"median": statistics.median(v), "sum": sum(v)}
                                 for k, v in sorted(by_round.items())},
            "retries": dict(collections.Counter(x for c in calls for x in c.get("retries") or []))}


def placements_of(record: dict) -> dict[str, Any]:
    rounds = [c for esc in record["escalations"] for c in esc.get("calls") or []
              if c["round"] == 1]
    cites = collections.Counter()
    for esc in record["escalations"]:
        for c in esc.get("calls") or []:
            for ref in shape.edges(c.get("payload") or {}):
                cites["manual" if shape.CITED.fullmatch(ref) else "other"] += 1
    return {"rounds": len(rounds),
            "listed": [len(esc.get("listed") or []) for esc in record["escalations"]
                       if esc.get("listed")],
            "citations": dict(cites),
            "verdicts": dict(collections.Counter(esc["verdict"]
                                                 for esc in record["escalations"])),
            "edge_reasons": dict(collections.Counter(
                why for r in record["records"] for why in r.get("edge_reasons") or [])),
            "copies_born": sum(1 for esc in record["escalations"]
                               if esc.get("copy_of") and esc["verdict"] == e.BORN)}


def births_against_the_list(record: dict) -> dict[str, Any]:
    region = references.regions()
    by = {v: k for k, v in sorted(region.items(), reverse=True)}
    corpus = MI.corpus()
    listed = governing = 0
    for r in record["rules"]:
        ext = brows.ext_of(r, MI.space())
        listed += ext in by
        governing += ext == region[references.governing(corpus[r["born_at"]]).id]
    return {"rules": len(record["rules"]), "a_listed_rules_region": listed,
            "the_governing_rules_region": governing}


def rare_of(record: dict, eng) -> dict[str, Any]:
    out = {}
    for q in references.RARE:
        esc = [x for x in record["escalations"]
               if record["records"][x["idx"]]["truth"] == q]
        stood = [r for r in record["records"] if r["truth"] == q and not r["escalated"]]
        out[q] = {"escalations": len(esc),
                  "drafts_right": sum(1 for x in esc if x.get("calls")
                                      and (x["calls"][0].get("payload") or {}).get("action") == q),
                  "decided_by_rules": len(stood),
                  "decided_right": sum(1 for r in stood if r["correct"])}
    return out


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]]) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}}
    inside = MI.space().full & ~MI.outside()
    for a in plan.ARMS:
        for k, (r, rec) in enumerate(zip(runs[a], records[a])):
            eng = r["engine"]
            co = MI.over_corpus(eng)
            out["runs"][f"{a}_r{rec['rep']}"] = {
                "space": frac(r["space"]),
                "space_without_the_keyword": MI.over_space(eng, MI.outside())["e2e"],
                "space_with_the_keyword": MI.over_space(eng, inside)["e2e"],
                "recall_space": {q: v["share"] for q, v in r["space_scored"]["recall"].items()},
                "corpus": co["e2e"], "recall_corpus": {q: v["share"]
                                                       for q, v in co["recall"].items()},
                "k_a": str(MI.k_a_exact(rec["rules"])), "cover": r["cover"],
                "rebuilt_is_the_run": r["rebuilt"],
                "online": {k2: rec["metrics"].get(k2) for k2 in (
                    "n_rules", "escalations", "impasses", "conflicts", "reuse_rate",
                    "e2e_accuracy", "silent_error_rate", "proposal_action_accuracy",
                    "failed_proposals", "rejected_rules", "dead_rules")},
                "v1b": rec["v1b"], "drafts": list(r["drafts"]),
                "placements": placements_of(rec), "births": births_against_the_list(rec),
                "rare": rare_of(rec, eng), "calls": calls_of(rec),
                "fill": breadings.read_run(rec, len(out["runs"]) + 1, MI.space(),
                                           MI.space_truth(), MI.outside(), list(MI.corpus()),
                                           brows.outside_cases(list(MI.corpus()))),
                "dates": [rec.get("started_at"), rec.get("_env", {}).get("recorded_at")]}
    rows_by_run = [r["edges"] for a in plan.ARMS for r in runs[a]]
    out["direction"] = {
        "space_whole": direction(rows_by_run, key="space_full"),
        "corpus_without_the_keyword": direction(rows_by_run, key="corpus_out"),
        "pooled_over_pairs": brows.direction(rows_by_run, "space_out", keep=placed_edge),
        "newborn_wins": direction(rows_by_run, predict=brows.newborn_names),
        "by_queue_pair": brows.split_by_queue_pair(rows_by_run, "space_out", keep=placed_edge)}
    for d in out["direction"].values():
        if isinstance(d, dict) and isinstance(d.get("reading"), Fraction):
            d["reading"] = frac(d["reading"])
    return out


def score(records: dict[str, list[dict]]) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    e_row, f_row = rl_e_f(runs)
    verdicts = {"RL-a": rl_a(runs), "RL-b": rl_b(runs), "RL-c": rl_c(runs),
                "RL-d": rl_d(runs), "RL-e": e_row, "RL-f": f_row, "RL-g": rl_g(runs)}
    return {"verdicts": verdicts, "RL-h": reported(runs, records),
            "rebuilt_is_the_run": all(r["rebuilt"] for a in plan.ARMS for r in runs[a])}


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
    ap = argparse.ArgumentParser(description="Stage C of PLAN_REASONED_LOOP.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run RL-g1 to RL-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("reasoned_loop/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    records, missing = read_records()
    out = score(records)
    if not out["rebuilt_is_the_run"]:
        sys.exit("\nREFUSED: a run's rebuilt base is not the base its record says it "
                 "ended with; nothing was written.\n")
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(), "missing": missing,
              "lines": {k: frac(v) for k, v in plan.LINES.items()}, **out}
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
