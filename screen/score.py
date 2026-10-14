"""
Stage C of `PLAN_SCREEN.md`: the four adjudications, from Stage B's records and
`PLAN_FIDELITY.md`'s. Free, and it refuses while the plan is unsigned.

Every Stage B record is checked first: this plan's protocol, and the digest of
the Stage A record the checks rebuild (§8). Then, per held-out decision, `y` is
the true queue and `b₁`, `b₂` the two answers with the screen, all read off
`PLAN_FIDELITY.md`'s records (rule B); `t₁`, `t₂` are the two answers without a
screen on the decision's ticket, pass 1 and pass 2 of this plan's ticket-only
session; and `p` is the screen's plurality action, from Stage A's design.

  V-a  pooled, two clauses, S − A each                         holds at <= 0.05, both
       ticket only: the 301 tickets F-f asked, new against 2026-10-03
       screen:      the 300 pilot B prompts, the anchor's answer against F-f's two
  V-b  per run: ½(1[t₁=y]+1[t₂=y]) − ½(1[b₁=y]+1[b₂=y])             holds at > 0
  V-c  per run, where t₁ ≠ p: ½(1[b₁=p]+1[b₂=p]) − 1[t₂=p]          holds at >= 0.10
  V-d  per run, two cells, each on its own median                  holds at > 0, both
       p = y: ½(1[b₁=y]+1[b₂=y]) − ½(1[t₁=y]+1[t₂=y])
       p ≠ y: the same with the sign reversed

**§0's rule for a run without a value, and for the median, is the scorer's
whole discretion, and it is §0's, not this module's.** A run has no value for
`V-b` to `V-d` if more than MAX_INVALID_SHARE of its held-out decisions lack the
four valid answers; for `V-c` if fewer than MIN_PULL_POPULATION have `t₁ ≠ p`;
for a cell of `V-d` if it holds fewer than MIN_CELL. The median is over the runs
that have a value: the middle one of three, the mean of two, and nothing with
fewer. The standard error that decides *thin* is the median run's, and over two
runs the larger of the two.

**The standard errors.** `V-a`'s are its items' alone, as `F-a`'s were.
`V-b` to `V-d` carry the finite-population correction of the held-out set's
sampling fraction in its run, the held-out decisions over the run's decided
cases. A row over part of the held-out set (`V-c`, each cell of `V-d`) takes
the same fraction: its part of the population is sampled at that rate too.

Recorded beside the rows and never in a denominator (§9):
  * the parts of each row, and the pooled value of every median row;
  * `V-e`: the rare classes in counts; the table by true queue; the pilot read
    on one day; each base's net beside its share p = y and its two cells, which
    compose it exactly; every changed answer classified by what the screen
    changed it to; and `finish_reason` by outcome;
  * the run itself: failures, invalid answers, the tickets serving decisions
    in more than one run, and the pace.

    python3 -m screen.score --dry-run
    python3 -m screen.score               # refuses while PLAN_SCREEN.md is unsigned
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import statistics
import sys
from typing import Any, Iterable

from harness.provenance import describe, environment

from fidelity import score as fidelity_score

from . import ask, plan, sample

HOLDS, REFUTED, NO_VERDICT = "holds", "refuted", "unadjudicable"
REQUIRED = ("anchor", "ticket_only")


# ---------------------------------------------------------------------------
# §0's lines, as functions, so that their edges can be pinned
# ---------------------------------------------------------------------------

def verdict_v_a(gaps: Iterable[float | None]) -> str:
    gaps = list(gaps)
    if not gaps or any(g is None for g in gaps):
        return NO_VERDICT
    return HOLDS if all(g <= plan.V_A_MAX_GAP for g in gaps) else REFUTED


def verdict_v_b(value: float | None) -> str:
    if value is None:
        return NO_VERDICT
    return HOLDS if value > plan.V_B_REFUTED_AT_OR_BELOW else REFUTED


def verdict_v_c(value: float | None) -> str:
    if value is None:
        return NO_VERDICT
    return HOLDS if value >= plan.V_C_MIN_PULL else REFUTED


def verdict_v_d(clause1: float | None, clause2: float | None) -> str:
    if clause1 is None or clause2 is None:
        return NO_VERDICT
    line = plan.V_D_REFUTED_AT_OR_BELOW
    return HOLDS if clause1 > line and clause2 > line else REFUTED


thin = fidelity_score.thin


# ---------------------------------------------------------------------------
# The arithmetic, pure
# ---------------------------------------------------------------------------

def mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def standard_error(values: list[float], fraction: float = 0.0) -> float | None:
    """Of a mean of `values`, with the finite-population correction of a
    sampling `fraction` (0 for none)."""
    if len(values) < 2:
        return None
    return statistics.stdev(values) / math.sqrt(len(values)) * math.sqrt(
        max(0.0, 1 - fraction))


def median_rule(per_run: list[tuple[float | None, float | None]]) -> dict[str, Any]:
    """§0: the median over the runs that have a value — the middle one of three,
    the mean of two — and its standard error for *thin*: the median run's, and
    over two runs the larger of the two. Fewer than two: no median."""
    defined = [(v, s) for v, s in per_run if v is not None]
    if len(defined) < 2:
        return {"median": None, "standard_error": None, "runs_with_a_value": len(defined)}
    if len(defined) == 2:
        (v1, s1), (v2, s2) = defined
        ses = [s for s in (s1, s2) if s is not None]
        return {"median": (v1 + v2) / 2, "standard_error": max(ses) if ses else None,
                "runs_with_a_value": 2}
    v, s = sorted(defined, key=lambda vs: vs[0])[len(defined) // 2]
    return {"median": v, "standard_error": s, "runs_with_a_value": len(defined)}


def pair_of(e: dict | None) -> tuple[str | None, str | None]:
    if e is None:
        return None, None
    return e["answers"].get(1), e["answers"].get(2)


def complete(d: dict) -> bool:
    """The four answers valid, and the label there."""
    return d["y"] is not None and None not in d["b"] and None not in d["t"]


def acc2(pair: tuple, target: str) -> float:
    return ((pair[0] == target) + (pair[1] == target)) / 2


# ---------------------------------------------------------------------------
# V-a
# ---------------------------------------------------------------------------

def ticket_clause(design: sample.Design, new: dict[str, dict],
                  old: dict[str, dict]) -> dict[str, Any]:
    """V-a without a screen: over the tickets F-f asked on 2026-10-03, `S` is
    the share whose two new answers agree and `A` the mean agreement of a new
    answer with an answer of that day."""
    s, a, d = [], [], []
    for t in design.tickets.values():
        if t["asked_by_F_f"] is None:
            continue
        pair = pair_of(new.get(t["id"]))
        before = [x for x in (old.get(t["asked_by_F_f"]) or {"answers": {}})
                  ["answers"].values() if x is not None]
        if None in pair or not before:
            continue
        si = 1.0 if pair[0] == pair[1] else 0.0
        ai = mean([1.0 if n == o else 0.0 for n in pair for o in before])
        s.append(si)
        a.append(ai)
        d.append(si - ai)
    return {"n": len(d), "S": mean(s), "A": mean(a), "gap": mean(d),
            "standard_error": standard_error(d)}


def screen_clause(anchor: dict[str, dict],
                  bases: dict[int, dict[str, dict]]) -> dict[str, Any]:
    """V-a with the screen: over the pilot's B prompts, `S` is the share whose
    two answers of 2026-10-02 or 03 agree and `A` the mean agreement of the
    anchor's answer with each of them."""
    s, a, d = [], [], []
    for iid, e in anchor.items():
        n = e["answers"].get(1)
        old = bases.get(e["run"], {}).get(iid)
        pair = fidelity_score.valid_pair(old) if old is not None else None
        if n is None or pair is None:
            continue
        si = 1.0 if pair[0] == pair[1] else 0.0
        ai = ((n == pair[0]) + (n == pair[1])) / 2
        s.append(si)
        a.append(ai)
        d.append(si - ai)
    return {"n": len(d), "S": mean(s), "A": mean(a), "gap": mean(d),
            "standard_error": standard_error(d)}


def adjudicate_v_a(tickets: dict, screen: dict) -> dict[str, Any]:
    gaps = [tickets["gap"], screen["gap"]]
    thins = [thin(c["gap"], plan.V_A_MAX_GAP, c["standard_error"])
             for c in (tickets, screen)]
    return {"ticket_only": tickets, "screen": screen, "line": plan.V_A_MAX_GAP,
            "verdict": verdict_v_a(gaps),
            "thin": (any(bool(x) for x in thins) if None not in thins else None)}


# ---------------------------------------------------------------------------
# V-b to V-d, per run
# ---------------------------------------------------------------------------

def held_out_entries(design: sample.Design, new: dict[str, dict],
                     bases: dict[int, dict[str, dict]]) -> dict[int, list[dict]]:
    """Every held-out decision with its four answers, its label and its screen."""
    out: dict[int, list[dict]] = {k: [] for k in plan.RUNS}
    for did, d in design.decisions.items():
        if d["population"] != sample.HELD_OUT:
            continue
        b = bases.get(d["run"], {}).get(did)
        out[d["run"]].append({
            "id": did, "run": d["run"], "ticket": d["ticket"],
            "y": b["labels"]["truth"] if b else None,
            "b": pair_of(b), "t": pair_of(new.get(d["ticket"])),
            "p": d["plurality"], "first": d["first_shown"],
            "shown": set(d["shown_actions"])})
    return out


def values_v_b(entries: list[dict]) -> list[float]:
    return [acc2(e["t"], e["y"]) - acc2(e["b"], e["y"]) for e in entries if complete(e)]


def values_v_c(entries: list[dict]) -> list[float]:
    return [acc2(e["b"], e["p"]) - (1.0 if e["t"][1] == e["p"] else 0.0)
            for e in entries if complete(e) and e["t"][0] != e["p"]]


def values_v_d(entries: list[dict]) -> tuple[list[float], list[float]]:
    c1 = [acc2(e["b"], e["y"]) - acc2(e["t"], e["y"])
          for e in entries if complete(e) and e["p"] == e["y"]]
    c2 = [acc2(e["t"], e["y"]) - acc2(e["b"], e["y"])
          for e in entries if complete(e) and e["p"] != e["y"]]
    return c1, c2


def score_run(k: int, entries: list[dict], population: int) -> dict[str, Any]:
    lacking = sum(1 for e in entries if not complete(e))
    defined = bool(entries) and lacking / len(entries) <= plan.MAX_INVALID_SHARE
    fraction = len(entries) / population if population else 0.0
    b, c = values_v_b(entries), values_v_c(entries)
    c1, c2 = values_v_d(entries)

    def value(vals: list[float], minimum: int = 0) -> float | None:
        return mean(vals) if defined and vals and len(vals) >= minimum else None

    rows = {"V-b": value(b), "V-c": value(c, plan.MIN_PULL_POPULATION),
            "V-d.1": value(c1, plan.MIN_CELL), "V-d.2": value(c2, plan.MIN_CELL)}
    ses = {"V-b": standard_error(b, fraction), "V-c": standard_error(c, fraction),
           "V-d.1": standard_error(c1, fraction), "V-d.2": standard_error(c2, fraction)}
    done = [e for e in entries if complete(e)]
    return {
        "run": k,
        "population": {"decided": population, "held_out": len(entries),
                       "sampling_fraction": fraction},
        "validity": {"lacking_the_four_answers": lacking, "defined": defined},
        "n": {"V-b": len(b), "V-c": len(c), "V-d.1": len(c1), "V-d.2": len(c2)},
        "rows": rows,
        "standard_errors": ses,
        "parts": {"without_screen": mean([acc2(e["t"], e["y"]) for e in done]),
                  "with_screen": mean([acc2(e["b"], e["y"]) for e in done]),
                  "plurality_is_the_true_queue": mean(
                      [1.0 if e["p"] == e["y"] else 0.0 for e in done])},
    }


def median_row(per_run: list[dict], row: str) -> dict[str, Any]:
    m = median_rule([(r["rows"][row], r["standard_errors"][row]) for r in per_run])
    return {"per_run": [r["rows"][row] for r in per_run], **m}


def adjudicate(v_a: dict, per_run: list[dict]) -> dict[str, dict]:
    b = median_row(per_run, "V-b")
    c = median_row(per_run, "V-c")
    d1, d2 = median_row(per_run, "V-d.1"), median_row(per_run, "V-d.2")
    thins_d = [thin(m["median"], plan.V_D_REFUTED_AT_OR_BELOW, m["standard_error"])
               for m in (d1, d2)]
    return {
        "V-a": v_a,
        "V-b": {**b, "line": plan.V_B_REFUTED_AT_OR_BELOW,
                "verdict": verdict_v_b(b["median"]),
                "thin": thin(b["median"], plan.V_B_REFUTED_AT_OR_BELOW,
                             b["standard_error"])},
        "V-c": {**c, "line": plan.V_C_MIN_PULL, "verdict": verdict_v_c(c["median"]),
                "thin": thin(c["median"], plan.V_C_MIN_PULL, c["standard_error"])},
        "V-d": {"clause_1_plurality_right": d1, "clause_2_plurality_wrong": d2,
                "line": plan.V_D_REFUTED_AT_OR_BELOW,
                "verdict": verdict_v_d(d1["median"], d2["median"]),
                "thin": (any(bool(x) for x in thins_d) if None not in thins_d else None)},
    }


def pooled(entries: dict[int, list[dict]], design: sample.Design) -> dict[str, Any]:
    """Every median row pooled over the three runs, beside it and adjudicating
    nothing."""
    allof = [e for k in plan.RUNS for e in entries[k]]
    decided = sum(design.fidelity.draw[k]["population"] for k in plan.RUNS)
    fraction = len(allof) / decided if decided else 0.0
    c1, c2 = values_v_d(allof)
    out = {}
    for row, vals in (("V-b", values_v_b(allof)), ("V-c", values_v_c(allof)),
                      ("V-d.1", c1), ("V-d.2", c2)):
        out[row] = {"n": len(vals), "value": mean(vals),
                    "standard_error": standard_error(vals, fraction)}
    return out


# ---------------------------------------------------------------------------
# V-e, beside the rows
# ---------------------------------------------------------------------------

def rare_classes(design: sample.Design, new: dict[str, dict]) -> dict[str, Any]:
    out: dict[str, dict] = {}
    for t in design.tickets.values():
        if t["rare"] is None:
            continue
        q = out.setdefault(t["rare"], {"tickets": 0, "named_by_both_answers": 0,
                                       "answers_by_queue": collections.Counter()})
        q["tickets"] += 1
        pair = pair_of(new.get(t["id"]))
        if pair == (t["rare"], t["rare"]):
            q["named_by_both_answers"] += 1
        for a in pair:
            q["answers_by_queue"][str(a)] += 1
    return {k: {**v, "answers_by_queue": dict(v["answers_by_queue"])}
            for k, v in sorted(out.items())}


def by_true_queue(entries: dict[int, list[dict]]) -> dict[str, Any]:
    groups = collections.defaultdict(list)
    for k in plan.RUNS:
        for e in entries[k]:
            if complete(e):
                groups[e["y"]].append(e)
    return {q: {"decisions": len(es),
                "without_screen": mean([acc2(e["t"], q) for e in es]),
                "with_screen": mean([acc2(e["b"], q) for e in es])}
            for q, es in sorted(groups.items(), key=lambda kv: -len(kv[1]))}


def pilot_one_day(design: sample.Design, new: dict[str, dict],
                  anchor: dict[str, dict]) -> dict[str, Any]:
    """The pilot asked under both arms on one day: the anchor's answer against
    the two new answers without a screen."""
    runs = design.fidelity.runs
    with_, without = [], []
    for iid, e in anchor.items():
        n = e["answers"].get(1)
        pair = pair_of(new.get(design.decisions[iid]["ticket"]))
        if n is None or None in pair:
            continue
        y = runs[e["run"]]["records"][e["idx"]]["truth"]
        with_.append(1.0 if n == y else 0.0)
        without.append(acc2(pair, y))
    return {"decisions": len(with_), "with_screen_one_answer": mean(with_),
            "without_screen_mean_of_two": mean(without),
            "difference": (mean(without) - mean(with_)) if with_ else None}


def decomposition(per_run: list[dict], entries: dict[int, list[dict]]) -> dict[str, Any]:
    """Each base's V-b beside its share p = y and its two cells, which compose
    it exactly over the decisions with four valid answers."""
    out = {}
    for r in per_run:
        es = [e for e in entries[r["run"]] if complete(e)]
        b, (c1, c2) = values_v_b(es), values_v_d(es)
        share = len(c1) / len(es) if es else None
        composed = (None if share is None or not b else
                    -share * (mean(c1) or 0.0) + (1 - share) * (mean(c2) or 0.0))
        out[f"run{r['run']}"] = {
            "V-b_over_complete": mean(b), "share_plurality_right": share,
            "cell_1": mean(c1), "cell_2": mean(c2), "composed": composed,
            "composes_exactly": (None if composed is None
                                 else abs(composed - mean(b)) < 1e-12)}
    return out


def changed_answers(entries: dict[int, list[dict]]) -> dict[str, Any]:
    """§5.4: every pass where the answer with the screen is not the answer
    without it, classified by what the screen changed it to — the plurality, the
    first shown action, another shown action, or an action not shown — over all
    such changes, the ones that cost and the ones that paid."""
    out = {}
    for k in list(plan.RUNS) + ["all"]:
        es = [e for kk in plan.RUNS for e in entries[kk]
              if complete(e) and (k == "all" or kk == k)]
        c = {s: collections.Counter() for s in ("all", "cost", "paid")}
        for e in es:
            for b, t in zip(e["b"], e["t"]):
                if b == t:
                    continue
                kind = ("plurality" if b == e["p"] else
                        "first_shown" if b == e["first"] else
                        "other_shown" if b in e["shown"] else "not_shown")
                c["all"][kind] += 1
                if t == e["y"]:
                    c["cost"][kind] += 1
                elif b == e["y"]:
                    c["paid"][kind] += 1
        out[f"run{k}" if k != "all" else "all"] = {s: dict(v) for s, v in c.items()}
    return out


def finish_reasons(records: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for name, rec in sorted(records.items()):
        c = collections.Counter()
        for r in rec["rows"]:
            outcome = ("failed" if r.get("failure") else
                       "valid" if r.get("valid") else "invalid")
            reasons = r.get("finish_reasons") or [None]
            c[f"{outcome}: {reasons[-1]}"] += 1
            c[f"attempts: {r.get('attempts')}"] += 1
        out[name] = dict(sorted(c.items()))
    return out


def run_itself(design: sample.Design, records: dict[str, dict]) -> dict[str, Any]:
    serving = collections.Counter()
    for t in design.tickets.values():
        runs = {k for k, i in t["serves"]
                if design.decisions[f"d{k}:{i}"]["population"] == sample.HELD_OUT}
        serving[len(runs)] += 1
    out = {"held_out_tickets_by_runs_served": {str(k): v for k, v in sorted(serving.items())}}
    for name, rec in sorted(records.items()):
        rows = rec["rows"]
        out[name] = {"answers": len(rows),
                     "valid": sum(1 for r in rows if r["valid"]),
                     "failed": sum(1 for r in rows if r["failure"]),
                     "invalid_action": sum(1 for r in rows
                                           if not r["valid"] and not r["failure"]),
                     "median_seconds_per_call": (statistics.median(
                         r["seconds"] for r in rows) if rows else None)}
    return out


def labels_agree(design: sample.Design, new_rows: list[dict],
                 bases: dict[int, dict[str, dict]]) -> list[str]:
    """Rule B: the labels a session row carries are the ones
    `PLAN_FIDELITY.md`'s records give the decisions it serves."""
    problems = []
    for r in new_rows:
        if r["kind"] != sample.TICKET_ONLY:
            continue
        for s in r["labels"]["serves"]:
            b = bases.get(s["run"], {}).get(f"d{s['run']}:{s['idx']}")
            if b is not None and b["labels"]["truth"] != r["labels"]["truth"]:
                problems.append(f"{r['id']}: its truth is not F-f's for d{s['run']}:{s['idx']}")
    return problems


# ---------------------------------------------------------------------------

def load_sessions() -> tuple[dict[str, dict], list[str]]:
    found, missing = {}, []
    for s in REQUIRED:
        path = plan.ask_path(s)
        if path.exists():
            found[s] = json.loads(path.read_text())
        else:
            missing.append(str(path))
    return found, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Stage C of PLAN_SCREEN.md: the four adjudications.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the blocking checks and list the records present")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = sample.run_checks(suite=True)
        sample.report(checks)
        found, missing = load_sessions()
        print(f"\n  Stage B records present: {sorted(found)}"
              + (f" — missing {', '.join(missing)}" if missing else ""))
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"screen/score.py writes {plan.SCORE_PATH}")
    checks = sample.run_checks(suite=True)
    sample.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    ok, why = ask.sample_matches(checks.design)
    if not ok:
        sys.exit(f"\nREFUSED: {why}.\n")
    found, missing = load_sessions()
    if missing:
        sys.exit(f"\nREFUSED: Stage B is incomplete — missing {', '.join(missing)}\n")
    digest = ask.sample_sha256()
    for name, rec in found.items():
        wrong = {k: rec.get(k) for k, v in ask.protocol().items() if rec.get(k) != v}
        if wrong or rec.get("sample_sha256") != digest:
            sys.exit(f"\nREFUSED: the {name} record was not produced under this "
                     f"protocol and this Stage A record: {wrong or 'sample digest'}\n")

    d = checks.design
    bases = sample.fidelity_bases(checks.found)
    new = fidelity_score.group(found["ticket_only"]["rows"])
    anchor = fidelity_score.group(found["anchor"]["rows"])
    old = fidelity_score.group(checks.found["ticket_only"]["rows"])
    problems = labels_agree(d, found["ticket_only"]["rows"], bases)
    if problems:
        sys.exit(f"\nREFUSED: {problems[0]} ({len(problems)} in all).\n")

    v_a = adjudicate_v_a(ticket_clause(d, new, old), screen_clause(anchor, bases))
    entries = held_out_entries(d, new, bases)
    per_run = [score_run(k, entries[k], d.fidelity.draw[k]["population"])
               for k in plan.RUNS]
    verdicts = adjudicate(v_a, per_run)
    for row, v in verdicts.items():
        print(f"  {row}  ->  {v['verdict']}" + ("  (thin)" if v.get("thin") else ""))
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(),
        **ask.protocol(),
        "stage": "C",
        "surface": ("corpus — seed 17, n=2000, in arrival order: the held-out "
                    "decisions of PLAN_FIDELITY.md's draw over PLAN_REUSE.md's three "
                    "Stage B runs"),
        "provenance": ("PRE-REGISTERED: §0 signed before any of these figures existed; "
                       "three of its four bands set on a development set, the pilot"),
        "gates": checks.summary(),
        "sample_sha256": digest,
        "verdicts": verdicts,
        "runs": per_run,
        "pooled": pooled(entries, d),
        "V-e": {
            "rare_classes": rare_classes(d, new),
            "by_true_queue": by_true_queue(entries),
            "pilot_on_one_day": pilot_one_day(d, new, anchor),
            "decomposition": decomposition(per_run, entries),
            "changed_answers": changed_answers(entries),
            "finish_reasons": finish_reasons(found),
        },
        "run_itself": run_itself(d, found),
    }, indent=2, default=str))
    print(f"\n-> {plan.SCORE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
