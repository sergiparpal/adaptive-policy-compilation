"""
Stage C of `PLAN_PLACEMENT.md`: scoring, and the six adjudications (§10). **Free,
and gated**: it refuses while §0 is unsigned, because what the gate protects is
the order of events, not money (§11 of the plan).

THE ROWS ARE §0's, AND ALL OF THEIR TERMS ARE SETTLED THERE, NOT HERE.

  PL-a  the median over v1c's runs of `refused(r)`, over the median over v1b's;
        holds at or below 3/4. No value when v1b's median is 0.
  PL-b  the median over v1c's runs of `space(B)`; holds at or above 9/10.
  PL-c  the number of v1c's runs whose `space(B)` is at least 9/10; holds at 3.
        A value only with three v1c runs. Thin when moving one run to the other
        side of 9/10 changes the verdict: every hold, and a refutation by one run.
  PL-d  the median over v1b's runs of `space(B)`, less v1c's; holds at or below
        1/20.
  PL-e  the median over v1b's runs of `space(B)`; holds at or above 9/10.
  PL-f  the median over v1c's runs of `recall_ONCALL_ESCALATION(B)` over the
        space; holds at or above 9/10.

Every statistic is a fraction of counts, compared with its line exactly. A row
that reads an arm with fewer than two runs has no value. A verdict on medians is
thin when any one run, put in place of its arm's median, puts the statistic on the
other side of its line. `refused(r)` counts the escalations that ended unplaced
with an answer, over every escalation of the run (§0).

`PL-g` is reported and adjudicates nothing. What a run reads is
`channel.score.read_run`'s, called: its base rebuilt and held to the record, its
`space`, its recall and its calls.

    python3 -m placement.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m placement.score
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from authorship import protocol as e
from blind import rows as brows
from channel import score as ch_score
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reasoned_loop import references as rl_refs
from reasoned_loop import score as rl_score
from rung2.engine2 import EDGE_CYCLE, PriorityEngine
from rung3.edge_direction import better_over_space, verdict as pair_verdict

from . import gates, plan, protocol, references

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
median = rl_score.median
ONCALL = references.ONCALL


def holds(rid: str, x: Fraction) -> bool:
    """§0's side of the line: `PL-a` and `PL-d` hold at or below it, every other
    row at or above."""
    line = plan.LINES[rid]
    return x <= line if rid in plan.HOLDS_AT_OR_BELOW else x >= line


# ---------------------------------------------------------------------------
# One run, read
# ---------------------------------------------------------------------------

def unplaced_with_an_answer(esc: dict) -> bool:
    """An escalation whose placement answer came back, kept the draft's rule and
    left a listed rule without a side (§0's `refused(r)`)."""
    return esc["verdict"] == e.UNPLACED and any(
        c["round"] == 1 and c.get("failure") is None for c in esc.get("calls") or [])


def refused_of(record: dict) -> Fraction | None:
    esc = record["escalations"]
    return F(sum(1 for x in esc if unplaced_with_an_answer(x)), len(esc)) if esc else None


def read_run(record: dict) -> dict[str, Any]:
    """`channel.score.read_run`, and the run's `refused(r)`."""
    got = ch_score.read_run(record)
    got["refused"] = refused_of(record)
    return got


# ---------------------------------------------------------------------------
# The six rows
# ---------------------------------------------------------------------------

def verdict(rid: str, value: Fraction | None, thin: bool, why: str | None,
            **parts) -> dict[str, Any]:
    line = plan.LINES[rid] if rid != "PL-c" else F(plan.PL_C_RUNS)
    at = "<=" if rid in plan.HOLDS_AT_OR_BELOW else ">="
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "holds_at": at, "thin": False, **parts}
    ok = value >= line if rid == "PL-c" else holds(rid, value)
    return {"verdict": HOLDS if ok else REFUTED, "value": frac(value), "line": frac(line),
            "holds_at": at, "thin": thin, "why": None, **parts}


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
    return m["v1c"] / m["v1b"] if m["v1b"] else None


ROWS: dict[str, tuple[tuple[str, ...], str, Callable]] = {
    "PL-a": (("v1b", "v1c"), "refused", ratio),
    "PL-b": (("v1c",), "space", lambda m: m["v1c"]),
    "PL-d": (("v1b", "v1c"), "space", lambda m: m["v1b"] - m["v1c"]),
    "PL-e": (("v1b",), "space", lambda m: m["v1b"]),
    "PL-f": (("v1c",), "oncall", lambda m: m["v1c"]),
}


def row(rid: str, runs: dict[str, list[dict]]) -> dict[str, Any]:
    if rid == "PL-c":
        return count_row(runs)
    arms, key, stat = ROWS[rid]
    vals = {a: [F(r[key]) for r in runs[a]] for a in arms}
    per_run = {a: [str(x) for x in xs] for a, xs in vals.items()}
    why = enough(runs, arms)
    if why:
        return verdict(rid, None, False, why, per_run=per_run)
    v, thin = median_row(rid, vals, stat)
    if v is None:
        return verdict(rid, None, False, "v1b's median refused(r) is 0", per_run=per_run)
    return verdict(rid, v, thin, None, per_run=per_run)


def count_row(runs: dict[str, list[dict]]) -> dict[str, Any]:
    """`PL-c`: how many v1c runs reach `PL_C_LINE`, of three."""
    vals = [F(r["space"]) for r in runs["v1c"]]
    per_run = {"v1c": [str(x) for x in vals]}
    if len(vals) < plan.PL_C_RUNS:
        return verdict("PL-c", None, False, "PL-c has a value only with three v1c runs",
                       per_run=per_run)
    count = sum(1 for v in vals if v >= plan.PL_C_LINE)
    ok = count >= plan.PL_C_RUNS
    thin = ok or len(vals) - count == 1
    return verdict("PL-c", F(count), thin, None, per_run=per_run,
                   per_run_line=frac(plan.PL_C_LINE))


ALL_ROWS = ("PL-a", "PL-b", "PL-c", "PL-d", "PL-e", "PL-f")


# ---------------------------------------------------------------------------
# PL-g, reported
# ---------------------------------------------------------------------------

def calls_of(record: dict) -> dict[str, Any]:
    """`channel.score.calls_of`, with `served_elsewhere` read against this plan's
    pin."""
    out = ch_score.calls_of(record)
    calls = [c for esc in record["escalations"] for c in esc.get("calls") or []]
    out["served_elsewhere"] = sum(1 for c in calls if c.get("failure") is None
                                  and c.get("served_by") != plan.PROVIDER_NAME)
    return out


def rounds_reported(record: dict) -> dict[str, Any]:
    """The placement rounds of a run of either arm, replayed: every rule `O`
    holds by its relation to its draft, every rule v1c left out by its reason,
    and every unplaced answer by the relation of what it left without a side."""
    proto = record["protocol"]
    space = MI.space()
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    births, bi = sorted(born), 0
    listed_by = collections.Counter()
    left_by = collections.Counter()
    unplaced_by = collections.Counter()
    sent = not_sent = 0
    replay_ok = True
    for esc in sorted(record["escalations"], key=lambda x: x["idx"]):
        idx = esc["idx"]
        while bi < len(births) and births[bi] < idx:
            b = births[bi]
            engine.add(rule_from(born[b]), born_at=b, keep_id=True)
            for ed in by_birth.get(b, []):
                engine.try_edge(ed.winner, ed.loser)
            bi += 1
        c0 = (esc.get("calls") or [{}])[0]
        o = c0.get("overlapped") or []
        if not o or c0.get("payload") is None:
            continue
        draft = brows.ext_of({"conditions": c0["payload"]["conditions"]}, space)
        got = protocol.listing_of(engine, draft, c0["payload"]["action"])
        keep = got["kept"] if proto == "v1c" else got["overlapped"]
        replay_ok &= set(got["overlapped"]) == set(o) and set(keep) == set(esc.get("listed") or [])
        if proto == "v1c":
            replay_ok &= got["left_out"] == (c0.get("left_out") or {})
        for rid in o:
            listed_by[protocol.relation(engine.ext[rid], draft)] += rid in keep
        left_by.update(got["left_out"].values() if proto == "v1c" else [])
        sent += bool(esc.get("listed"))
        not_sent += not esc.get("listed")
        if unplaced_with_an_answer(esc):
            c1 = next(c for c in esc["calls"] if c["round"] == 1)
            rels = sorted({protocol.relation(engine.ext[rid], draft)
                           for rid in c1.get("unplaced") or []})
            unplaced_by["+".join(rels) or "none"] += 1
    return {"rounds_sent": sent, "rounds_not_sent": not_sent, "listed_by_relation": dict(listed_by),
            "left_out_by_reason": dict(left_by), "unplaced_by_what_it_left_out": dict(unplaced_by),
            "replay_ok": replay_ok}


def births_left_out(record: dict) -> dict[str, list[int]]:
    """v1c's births whose round left a rule out, by the birth's queue: [births,
    of them with the ticket's queue] (§6.19)."""
    truth = {r["idx"]: r["truth"] for r in record["records"]}
    out: dict[str, list[int]] = {}
    for esc in record["escalations"]:
        c0 = (esc.get("calls") or [{}])[0]
        if esc["verdict"] != e.BORN or not c0.get("left_out"):
            continue
        q = c0["payload"]["action"]
        out.setdefault(q, [0, 0])
        out[q][0] += 1
        out[q][1] += q == truth.get(esc["idx"])
    return dict(sorted(out.items()))


RIGHT, WRONG = "a", "b"            # `rung3.edge_direction.verdict` on (winner, loser)


def cycle_refused(record: dict, eng: PriorityEngine) -> dict[str, Any]:
    """Every edge the engine refused for closing a cycle (§6.11, `PL-g`).

    An edge is *right* when its declared winner is the better rule over the
    pair's shared region, by `rung3/edge_direction.py`'s `verdict`, as `RL-e`
    reads a placed edge: `a` right, `b` wrong, and a tie or a region neither rule
    is ever right on counted apart. It is read on the whole space and on the
    half without the keyword. A pair of one queue has no direction to get
    wrong, and is counted apart too.

    Beside each, the points of the shared region on which the final base
    leaves both rules undefeated: where the refused edge would decide now, and
    of those, where its winner's queue is the truth. The cycle was closed at the
    edge's birth; the final base is read at the run's end."""
    action = {r["rule_id"]: r["action"] for r in record["rules"]}
    born = {r["rule_id"]: r["born_at"] for r in record["rules"]}
    tmask = MI.space_truth()
    t_out = brows.restrict(tmask, MI.outside())
    und = brows.undefeated_masks(eng)
    edges = []
    for (w, l, why), ch in zip(record.get("edge_log") or [], brows.channels_of(record)):
        if why != EDGE_CYCLE or w not in eng.ext or l not in eng.ext:
            continue
        shared = eng.ext[w] & eng.ext[l]
        both = shared & und[w] & und[l]
        row: dict[str, Any] = {"winner": w, "loser": l, "channel": ch,
                               "queues": [action[w], action[l]], "born_at": [born[w], born[l]],
                               "same_queue": action[w] == action[l],
                               "shared": shared.bit_count(), "contested": both.bit_count()}
        if not row["same_queue"]:
            row["space_full"] = pair_verdict(*better_over_space(w, l, eng.ext, action, tmask))
            row["space_out"] = pair_verdict(*better_over_space(w, l, eng.ext, action, t_out))
            row["contested_winner_right"] = (both & tmask[action[w]]).bit_count()
            row["contested_loser_right"] = (both & tmask[action[l]]).bit_count()
        edges.append(row)
    return {"refused": len(edges), "edges": edges, **cycle_summary(edges)}


def cycle_summary(edges: list[dict[str, Any]]) -> dict[str, Any]:
    """`cycle_refused`'s counts, over one run's edges or an arm's."""
    across = [r for r in edges if not r["same_queue"]]
    out: dict[str, Any] = {"same_queue": len(edges) - len(across),
                           "by_verdict": {}, "right": {}}
    for key in ("space_full", "space_out"):
        out["by_verdict"][key] = dict(sorted(collections.Counter(r[key] for r in across).items()))
        right = [r for r in across if r[key] == RIGHT]
        out["right"][key] = {
            "edges": len(right),
            "pairs": len({frozenset((r["winner"], r["loser"])) for r in right}),
            "contested": sum(r["contested"] for r in right),
            "contested_winner_right": sum(r["contested_winner_right"] for r in right)}
    return out


def edges_of(record: dict) -> dict[str, int]:
    return dict(collections.Counter(why for r in record["records"]
                                    for why in r.get("edge_reasons") or []))


def bridge_reported(bridge: dict | None) -> dict[str, Any] | None:
    """§5.5: each provider's first calls against the label, against the governing
    rule's region and against each other, and Baidu's against `PLAN_CHANNEL.md`'s
    recorded drafts of the same tickets."""
    if bridge is None:
        return None
    labels, corpus, space = plan.labels(), MI.corpus(), MI.space()
    region = rl_refs.regions()
    recorded: dict[int, list[dict]] = collections.defaultdict(list)
    for rep in (1, 2, 3):
        rec = references.closed_record("channel", "c", rep)
        for esc in rec["escalations"]:
            pl = (esc.get("calls") or [{}])[0].get("payload")
            if pl:
                recorded[esc["idx"]].append(pl)

    def read(pl: dict | None, idx: int) -> dict[str, Any] | None:
        if not pl or not pl.get("conditions"):
            return None
        try:
            ext = brows.ext_of(pl, space)
        except Exception:
            return None
        return {"queue": pl.get("action"), "queue_right": pl.get("action") == labels[idx][0],
                "ext": ext, "governing_region": ext == region[rl_refs.governing(corpus[idx]).id]}

    by = {(a["idx"], a["provider"]): read(a.get("payload"), a["idx"]) for a in bridge["asks"]}
    out: dict[str, Any] = {"providers": {}, "between": collections.Counter(),
                           "baidu_against_recorded": collections.Counter()}
    for pv in plan.BRIDGE_PROVIDERS:
        mine = [v for (i, q), v in by.items() if q == pv and v is not None]
        out["providers"][pv] = {"answered": len(mine),
                                "queue_right": sum(v["queue_right"] for v in mine),
                                "governing_region": sum(v["governing_region"] for v in mine)}
    for idx in plan.bridge_tickets():
        a, b = by.get((idx, "baidu")), by.get((idx, "deepinfra"))
        if a and b:
            out["between"]["both_answered"] += 1
            out["between"]["same_queue"] += a["queue"] == b["queue"]
            out["between"]["same_rule"] += a["queue"] == b["queue"] and a["ext"] == b["ext"]
        for pl in recorded.get(idx, []):
            old = read(pl, idx)
            if a and old:
                out["baidu_against_recorded"]["pairs"] += 1
                out["baidu_against_recorded"]["same_queue"] += a["queue"] == old["queue"]
                out["baidu_against_recorded"]["same_rule"] += (a["queue"] == old["queue"]
                                                               and a["ext"] == old["ext"])
    out["between"] = dict(out["between"])
    out["baidu_against_recorded"] = dict(out["baidu_against_recorded"])
    return out


def reported(runs: dict[str, list[dict]], records: dict[str, list[dict]],
             sample: dict[str, Any], bridge: dict | None) -> dict[str, Any]:
    out: dict[str, Any] = {"runs": {}}
    refs = sample["references"]
    inside = MI.space().full & ~MI.outside()
    channels = {}
    for rep in range(1, plan.REPS + 1):
        ch = references.closed_record("channel", "c", rep)
        got = ch_score.read_run(ch)
        refused_cycle = cycle_refused(ch, got["engine"])
        channels[rep] = {"space": frac(got["space"]), "oncall": frac(got["oncall"]),
                         "refused": frac(refused_of(ch)), "calls": got["calls"],
                         "cycle_refused": {k: v for k, v in refused_cycle.items() if k != "edges"},
                         "dates": [ch.get("started_at"), ch.get("_env", {}).get("recorded_at")]}
    out["channels_runs"] = {f"c_r{rep}": v for rep, v in channels.items()}
    for a in plan.ARMS:
        for r, rec in zip(runs[a], records[a]):
            eng, rep = r["engine"], rec["rep"]
            co = MI.over_corpus(eng)
            tx = refs["transcriber"][f"{a}_r{rep}"]["figures"]
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
                "v1b": rec["v1b"], "refused": frac(r["refused"]), "drafts": list(r["drafts"]),
                "calls": calls_of(rec), "calls_as_recorded": r["calls_as_recorded"],
                "rounds": rounds_reported(rec), "births_left_out": births_left_out(rec),
                "edges": edges_of(rec), "cycle_refused": cycle_refused(rec, eng),
                "reports": ch_score.reports_of(rec),
                "transcriber": {k: tx[k] for k in ("escalations", "impasses", "conflicts",
                                                   "errors", "calls", "space_right",
                                                   "space_points", "corpus_right",
                                                   "recall_oncall")},
                "verdicts": ch_score.verdicts_with_finish(rec),
                "placements": rl_score.placements_of(rec),
                "births": rl_score.births_against_the_list(rec),
                "rare": rl_score.rare_of(rec, eng),
                "channels_run_under_the_same_draws": f"c_r{rep}",
                "dates": [rec.get("first_kept"), rec.get("started_at"),
                          rec.get("_env", {}).get("recorded_at")]}
    out["cycle_refused"] = {}
    for a in plan.ARMS:
        edges = [x for k, run in out["runs"].items() if k.startswith(f"{a}_")
                 for x in run["cycle_refused"]["edges"]]
        out["cycle_refused"][a] = {"refused": len(edges), **cycle_summary(edges)}
    out["direction"] = {}
    for a in plan.ARMS:
        rows_by_run = [r["edges"] for r in runs[a]]
        got = {"declared": rl_score.direction(rows_by_run),
               "ranking": rl_score.direction(rows_by_run, predict=brows.stage_c_names)}
        for d in got.values():
            d["reading"] = frac(d["reading"]) if d["reading"] is not None else None
        out["direction"][a] = got
    out["bridge"] = bridge_reported(bridge)
    return out


def score(records: dict[str, list[dict]], sample: dict[str, Any],
          bridge: dict | None) -> dict[str, Any]:
    runs = {a: [read_run(rec) for rec in records[a]] for a in plan.ARMS}
    verdicts = {rid: row(rid, runs) for rid in ALL_ROWS}
    return {"verdicts": verdicts, "PL-g": reported(runs, records, sample, bridge),
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
    ap = argparse.ArgumentParser(description="Stage C of PLAN_PLACEMENT.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run PL-g1 to PL-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("placement/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if not plan.sample_path().exists():
        sys.exit("\nREFUSED: no Stage A record; nothing was written.\n")
    sample = json.loads(plan.sample_path().read_text())
    bridge = json.loads(plan.bridge_path().read_text()) if plan.bridge_path().exists() else None
    records, missing = read_records()
    scored = score(records, sample, bridge)
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
