"""
Stage C of `PLAN_APPLY.md`: scoring, and the six adjudications. **Free, and
gated.**

It reads Stage A's record, the two passes and the twelve loop records, and
writes `results_apply/score.json`:

  * **`X-a` to `X-f`**, each against its line exactly, as a fraction, with its
    standard error clustered by ticket, *thin* and *unadjudicable* as §0
    defines them;
  * **each row's parts and per-run values**, never summed into the verdict;
  * **`X-g` in full**, and the run itself.

THE LABELS ENTER HERE AND NOWHERE ELSE (rule B). `y` is a row's `truth` and `ℓ`
its `predicted`, read off the loop records by `labels`. The answers come from
the passes' rows, which carry neither.

THE NOTATION IS §0's. Per decision: `s₁` and `s₂` are the screen arm's answers
in passes 1 and 2, `t₁` and `t₂` the ticket arm's at the decision's level, `u₁`
and `u₂` the ticket arm's at level 0, and `p` the screen's plurality. An answer
is valid when its `action` is one of the eight queues, and an invalid one is
`None` here. A decision enters a row only with every answer the row reads valid.

    PYTHONHASHSEED=0 python3 -m apply.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m apply.score
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable

from harness.domain import ACTIONS
from harness.provenance import describe, environment
from rung2.engine2 import RuleValidationError, validate_conditions

from manual import instrument as MI

from . import gates, plan, population, prompts

F = Fraction
NARROW = 840      # points off the keyword: manual/after_readings.py's two narrowest bands
RARE = ("ONCALL_ESCALATION", "SECURITY_INCIDENT", "ACCOUNT_MANAGER", "T3_ENGINEERING")


def labels() -> dict[str, dict[str, Any]]:
    """`{escalation id: {"y": truth, "loop": predicted}}`, off the twelve records."""
    out = {}
    for lv in plan.LEVELS:
        for rep in range(1, plan.REPS + 1):
            for row in population.record(lv, rep)["records"]:
                if row["escalated"]:
                    out[population.escalation_id(lv, rep, row["idx"])] = {
                        "y": row["truth"], "loop": row["predicted"]}
    return out


def read(session: str) -> dict[str, Any]:
    return json.loads(plan.ask_path(session).read_text())


def answer(row: dict | None) -> str | None:
    """A row's action if valid, `None` otherwise or if there is no row."""
    if row is None or row.get("action") not in ACTIONS:
        return None
    return row["action"]


# ---------------------------------------------------------------------------
# The decisions, with their answers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Unit:
    id: str
    level: int
    run: int
    ticket: int
    kind: str
    y: str
    loop: str | None
    p: str | None
    first: str | None
    shown: tuple[str, ...]
    s: tuple[str | None, str | None]
    t: tuple[str | None, str | None]
    u: tuple[str | None, str | None]


def units(design: population.Design, by_pass: dict[int, dict[str, dict]],
          lab: dict[str, dict[str, Any]]) -> list[Unit]:
    out = []
    for i, e in sorted(design.decisions.items()):
        sa = design.asks[population.screen_ask_id(i)]
        tid = population.ticket_ask_id(e.level, e.ticket)
        uid = population.ticket_ask_id(0, e.ticket)
        out.append(Unit(
            id=i, level=e.level, run=e.run, ticket=e.ticket, kind=e.prompt.screen,
            y=lab[i]["y"], loop=lab[i]["loop"], p=prompts.plurality(sa),
            first=prompts.first_shown(sa), shown=tuple(sa.shown_actions),
            s=tuple(answer(by_pass[k].get(sa.id)) for k in (1, 2)),
            t=tuple(answer(by_pass[k].get(tid)) for k in (1, 2)),
            u=tuple(answer(by_pass[k].get(uid)) for k in (1, 2))))
    return out


def hits(pair: tuple[str | None, str | None], target: str | None) -> Fraction:
    """`½(1[a₁=target] + 1[a₂=target])`; an invalid answer never hits."""
    if target is None:
        return F(0)
    return F(sum(1 for a in pair if a is not None and a == target), 2)


def valid(*pairs: tuple[str | None, str | None]) -> bool:
    return all(a is not None for pair in pairs for a in pair)


def mean(xs: list[Fraction]) -> Fraction | None:
    return sum(xs, F(0)) / len(xs) if xs else None


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return None if x is None else {"fraction": f"{x.numerator}/{x.denominator}",
                                   "value": float(x)}


def clustered_se(terms: list[tuple[int, Fraction]]) -> float | None:
    """§0: `C/(C−1) · Σ over tickets of (Σ over its decisions of (d − d̄))² / n²`,
    square-rooted. A float: it labels and never decides."""
    n = len(terms)
    if n < 2:
        return None
    dbar = float(sum((d for _, d in terms), F(0))) / n
    sums: dict[int, float] = defaultdict(float)
    for c, d in terms:
        sums[c] += float(d) - dbar
    c = len(sums)
    if c < 2:
        return None
    return math.sqrt(c / (c - 1) * sum(v * v for v in sums.values()) / n ** 2)


# ---------------------------------------------------------------------------
# The six rows
# ---------------------------------------------------------------------------

HOLDS: dict[str, Callable[[Fraction, Fraction], bool]] = {
    "le": lambda v, line: v <= line,
    "gt": lambda v, line: v > line,
    "ge": lambda v, line: v >= line,
}


@dataclass(frozen=True)
class Spec:
    id: str
    levels: tuple[int, ...]
    needs: Callable[[Unit], bool]
    keep: Callable[[Unit], bool]
    term: Callable[[Unit], Fraction]
    line: Fraction
    rule: str
    offset: Fraction = F(0)        # the statistic is the mean of the terms plus this


def statistic(spec: Spec, us: list[Unit]) -> Fraction | None:
    m = mean([spec.term(u) for u in us])
    return None if m is None else m + spec.offset


def x_a_term(u: Unit) -> Fraction:
    return F(int(u.s[0] == u.s[1])) - hits(u.s, u.loop)


def accuracy_gap(arm: str, base: str) -> Callable[[Unit], Fraction]:
    def term(u: Unit) -> Fraction:
        return hits(getattr(u, arm), u.y) - hits(getattr(u, base), u.y)
    return term


def x_c_term(u: Unit) -> Fraction:
    return 2 * hits(u.t, u.y) - hits(u.s, u.y)


def x_d_term(u: Unit) -> Fraction:
    return hits(u.s, u.p) - F(int(u.t[1] == u.p))


SPECS = (
    Spec("X-a", tuple(plan.LEVELS), lambda u: valid(u.s), lambda u: True,
         x_a_term, plan.X_A_MAX_GAP, "le"),
    Spec("X-b", (3,), lambda u: valid(u.s, u.t), lambda u: True,
         accuracy_gap("t", "s"), plan.X_B_LINE, "gt"),
    Spec("X-c", (3,), lambda u: valid(u.s, u.t), lambda u: True,
         x_c_term, F(0), "ge", offset=F(-1)),
    Spec("X-d", (3,), lambda u: valid(u.s, u.t), lambda u: u.t[0] != u.p,
         x_d_term, plan.X_D_LINE, "ge"),
    Spec("X-e", (2,), lambda u: valid(u.s, u.t), lambda u: True,
         accuracy_gap("t", "s"), plan.X_E_LINE, "gt"),
    Spec("X-f", (3,), lambda u: valid(u.t, u.u), lambda u: True,
         accuracy_gap("t", "u"), plan.X_F_LINE, "ge"),
)


def x_c_share(us: list[Unit]) -> Fraction | None:
    """`(acc_t − acc_s) / (1 − acc_s)`, what `X-c` publishes beside the
    comparison it decides by."""
    acc_s, acc_t = mean([hits(u.s, u.y) for u in us]), mean([hits(u.t, u.y) for u in us])
    if acc_s is None or acc_s == 1:
        return None
    return (acc_t - acc_s) / (1 - acc_s)


def adjudicate(spec: Spec, all_units: list[Unit]) -> dict[str, Any]:
    population_ = [u for u in all_units if u.level in spec.levels]
    usable = [u for u in population_ if spec.needs(u)]
    missing = len(population_) - len(usable)
    kept = [u for u in usable if spec.keep(u)]
    out: dict[str, Any] = {"id": spec.id, "levels": list(spec.levels),
                           "decisions": len(population_), "missing": missing,
                           "read": len(kept), "line": frac(spec.line), "holds": spec.rule}
    reasons = []
    if not population_ or F(missing, len(population_)) > plan.MAX_INVALID_SHARE:
        reasons.append("more than 5% of its decisions lack the valid answers it reads")
    if spec.id == "X-d" and len(kept) < plan.MIN_PULL_POPULATION:
        reasons.append(f"fewer than {plan.MIN_PULL_POPULATION} decisions have t1 != p")
    if spec.id == "X-c" and kept and mean([hits(u.s, u.y) for u in kept]) == 1:
        reasons.append("acc_s is 1")
    value = statistic(spec, kept)
    if value is None:
        reasons.append("no decision to read")
    out["value"] = frac(value)
    if spec.id == "X-c":
        # §0: the line is the share's, 1/2, and the row is decided by the same
        # comparison written without the division.
        out["line"] = frac(plan.X_C_LINE)
        out["share"] = frac(x_c_share(kept))
        out["compared_as"] = "2·acc_t − acc_s − 1 against 0"
    out["se"] = clustered_se([(u.ticket, spec.term(u)) for u in kept])
    runs = sorted({(u.level, u.run) for u in kept})
    out["per_run"] = {f"L{lv}r{r}": frac(statistic(spec, [u for u in kept
                                                         if (u.level, u.run) == (lv, r)]))
                      for lv, r in runs}
    if reasons:
        out.update({"verdict": "unadjudicable", "why": reasons, "thin": None})
        return out
    holds = HOLDS[spec.rule](value, spec.line)
    flips = []
    for key in runs:
        rest = statistic(spec, [u for u in kept if (u.level, u.run) != key])
        if rest is not None and HOLDS[spec.rule](rest, spec.line) != holds:
            flips.append(f"L{key[0]}r{key[1]}")
    within = out["se"] is not None and abs(float(value - spec.line)) <= out["se"]
    out.update({"verdict": "holds" if holds else "refuted",
                "thin": within or bool(flips),
                "thin_because": {"within_one_se": within, "dropping_one_run_flips": flips}})
    out["parts"] = parts(spec, kept)
    return out


def parts(spec: Spec, us: list[Unit]) -> dict[str, Any]:
    """The accuracies or agreements a row is made of, side by side."""
    if spec.id == "X-a":
        return {"S": frac(mean([F(int(u.s[0] == u.s[1])) for u in us])),
                "A": frac(mean([hits(u.s, u.loop) for u in us]))}
    if spec.id == "X-d":
        return {"screen_on_p": frac(mean([hits(u.s, u.p) for u in us])),
                "second_ticket_answer_on_p": frac(mean([F(int(u.t[1] == u.p)) for u in us]))}
    out = {"acc_s": frac(mean([hits(u.s, u.y) for u in us])),
           "acc_t": frac(mean([hits(u.t, u.y) for u in us]))}
    if spec.id == "X-f":
        out = {"acc_t": out["acc_t"], "acc_u": frac(mean([hits(u.u, u.y) for u in us]))}
    return out


# ---------------------------------------------------------------------------
# X-g, reported
# ---------------------------------------------------------------------------

def changed(u: Unit, k: int) -> str | None:
    """What the screen changed the answer to in pass `k` (§5.6), where both
    arms answered validly and differently."""
    s, t = u.s[k], u.t[k]
    if s is None or t is None or s == t:
        return None
    if s == u.p:
        return "plurality"
    if s == u.first:
        return "first_shown"
    return "other_shown" if s in u.shown else "not_shown"


def every_row_at(level: int, us: list[Unit]) -> dict[str, Any]:
    here = [u for u in us if u.level == level]
    st = [u for u in here if valid(u.s, u.t)]
    tu = [u for u in here if valid(u.t, u.u)]
    pull = [u for u in st if u.t[0] != u.p]
    sa = [u for u in here if valid(u.s)]
    return {"decisions": len(here),
            "acc_s": frac(mean([hits(u.s, u.y) for u in st])),
            "acc_t": frac(mean([hits(u.t, u.y) for u in st])),
            "acc_u": frac(mean([hits(u.u, u.y) for u in tu])),
            "loop": frac(mean([F(int(u.loop == u.y)) for u in here])),
            "t_minus_s": frac(mean([accuracy_gap("t", "s")(u) for u in st])),
            "share": frac(x_c_share(st)),
            "pull": frac(mean([x_d_term(u) for u in pull])), "pull_read": len(pull),
            "t_minus_u": frac(mean([accuracy_gap("t", "u")(u) for u in tu])),
            "S_minus_A": frac(mean([x_a_term(u) for u in sa])),
            "by_kind": {kind: {"decisions": len(k), "acc_s": frac(mean([hits(u.s, u.y) for u in k])),
                               "acc_t": frac(mean([hits(u.t, u.y) for u in k])),
                               "t_minus_s": frac(mean([accuracy_gap("t", "s")(u) for u in k]))}
                        for kind in (prompts.COVERAGE, prompts.CONFLICT)
                        for k in [[u for u in st if u.kind == kind]]},
            "changed": dict(Counter(c for u in here for k in (0, 1)
                                    if (c := changed(u, k)) is not None))}


def by_queue(us: list[Unit]) -> dict[str, Any]:
    """Counts, so that the rare queues read as counts (§0)."""
    out: dict[str, Any] = {}
    for lv in plan.LEVELS:
        rows: dict[str, Counter] = defaultdict(Counter)
        for u in us:
            if u.level != lv:
                continue
            c = rows[u.y]
            c["decisions"] += 1
            c["loop_right"] += int(u.loop == u.y)
            for arm in ("s", "t", "u"):
                pair = getattr(u, arm)
                c[f"{arm}_answers"] += sum(1 for a in pair if a is not None)
                c[f"{arm}_right"] += sum(1 for a in pair if a is not None and a == u.y)
        out[str(lv)] = {q: dict(c) for q, c in sorted(rows.items())}
    out["rare"] = list(RARE)
    return out


def rules_written(design: population.Design, by_pass: dict[int, dict[str, dict]]
                  ) -> dict[str, Any]:
    """The rule beside each answer: whether it validates against its ticket, and
    its points off the keyword. Reported; no rule is installed (rule E)."""
    space, outside = MI.space(), MI.outside()
    cells: dict[str, dict[str, list]] = defaultdict(lambda: {"answers": [], "breadth": []})
    reasons: dict[str, Counter] = defaultdict(Counter)
    for k in (1, 2):
        for aid, row in by_pass[k].items():
            a = design.asks[aid]
            cell = f"{a.arm} L{a.level}"
            cells[cell]["answers"].append(aid)
            if not isinstance(row.get("payload"), dict):
                reasons[cell]["no payload"] += 1
                continue
            try:
                rule = validate_conditions(row["payload"], a.case)
            except RuleValidationError as exc:
                reasons[cell][str(exc).split(":")[0]] += 1
                continue
            cells[cell]["breadth"].append(
                (space.extension(rule.conditions) & outside).bit_count())
    out = {}
    for cell, c in sorted(cells.items()):
        b = c["breadth"]
        out[cell] = {"answers": len(c["answers"]), "validate": len(b),
                     "rejected": dict(reasons[cell]),
                     "median_points_off_the_keyword": statistics.median(b) if b else None,
                     "narrow": sum(1 for x in b if x <= NARROW)}
    return out


def against_plan_screen(truth: dict[int, str], design: population.Design,
                        by_pass: dict[int, dict[str, dict]]) -> dict[str, Any]:
    """Level 0's ticket arm beside `PLAN_SCREEN.md`'s ticket-only answers of
    2026-10-14, on the tickets both asked: the same prompt on two dates.
    `truth` is every escalated ticket's queue, case 0's included."""
    rec = json.loads(plan.SCREEN_TICKET_ONLY.read_text())
    theirs: dict[int, dict[int, str | None]] = defaultdict(dict)
    for r in rec["rows"]:
        if r.get("idx") is None:
            continue
        t = population.ticket_of(population.corpus()[r["idx"]])
        theirs[t][r["pass"]] = r["action"] if r.get("valid") else None
    rows = []
    for t, old in sorted(theirs.items()):
        aid = population.ticket_ask_id(0, t)
        if aid not in design.asks or t not in truth:
            continue
        new = tuple(answer(by_pass[k].get(aid)) for k in (1, 2))
        old_ = (old.get(1), old.get(2))
        if not (valid(new) and valid(old_)):
            continue
        rows.append((new, old_, truth[t]))
    if not rows:
        return {"tickets": 0}
    return {"tickets": len(rows),
            "S_today": frac(mean([F(int(n[0] == n[1])) for n, _, _ in rows])),
            "S_then": frac(mean([F(int(o[0] == o[1])) for _, o, _ in rows])),
            "A_across": frac(mean([F(sum(int(a == b) for a in n for b in o), 4)
                                   for n, o, _ in rows])),
            "right_today": frac(mean([hits(n, y) for n, _, y in rows])),
            "right_then": frac(mean([hits(o, y) for _, o, y in rows]))}


def the_calls(design: population.Design, recs: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for session, rec in recs.items():
        rows = rec["rows"]
        per_arm: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
        notes = []
        for r in rows:
            arm = design.asks[r["id"]].arm
            for att in r.get("call_attempts") or []:
                per_arm[arm]["providers"][att.get("provider")] += 1
                per_arm[arm]["finish_reasons"][att.get("finish_reason")] += 1
                per_arm[arm]["tokens"]["prompt"] += att.get("prompt_tokens") or 0
                per_arm[arm]["tokens"]["completion"] += att.get("completion_tokens") or 0
                per_arm[arm]["tokens"]["reasoning"] += att.get("reasoning_tokens") or 0
            note = (r.get("payload") or {}).get("note") if isinstance(r.get("payload"), dict) else None
            if note:
                notes.append(len(str(note)))
        seconds = [r["seconds"] for r in rows if r.get("seconds") is not None]
        out[session] = {
            "answers": len(rows), "valid": sum(1 for r in rows if answer(r) is not None),
            "invalid": sum(1 for r in rows if r.get("failure") is None and answer(r) is None),
            "failed": sum(1 for r in rows if r.get("failure") is not None),
            "retried": sum(1 for r in rows if (r.get("attempts") or 0) > 1),
            "median_seconds": statistics.median(seconds) if seconds else None,
            "started_at": rec.get("started_at"), "finished_at": rec.get("finished_at"),
            "by_arm": {arm: {k: dict(v) for k, v in d.items()} for arm, d in per_arm.items()},
            "notes": {"recorded": len(notes),
                      "median_characters": statistics.median(notes) if notes else None,
                      "coded": False},
        }
    return out


def x_g(us: list[Unit], design: population.Design, by_pass: dict[int, dict[str, dict]],
        recs: dict[str, dict], lab: dict[str, dict[str, Any]]) -> dict[str, Any]:
    truth = {e.ticket: lab[i]["y"] for i, e in design.escalations.items()}
    return {"by_level": {str(lv): every_row_at(lv, us) for lv in plan.LEVELS},
            "by_true_queue": by_queue(us),
            "rules_written": rules_written(design, by_pass),
            "against_plan_screen": against_plan_screen(truth, design, by_pass),
            "the_calls": the_calls(design, recs)}


# ---------------------------------------------------------------------------
# Stage C
# ---------------------------------------------------------------------------

def score(design: population.Design, recs: dict[str, dict],
          lab: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]}
               for s, rec in recs.items() if s != "smoke"}
    us = units(design, by_pass, lab)
    verdicts = {spec.id: adjudicate(spec, us) for spec in SPECS}
    return {"verdicts": verdicts, "X-g": x_g(us, design, by_pass, recs, lab)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_APPLY.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run X-g1 to X-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("apply/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    missing = [s for s in plan.SESSIONS[1:] if not plan.ask_path(s).exists()]
    if missing:
        sys.exit(f"\nREFUSED: no record of {missing}; Stage C reads both passes. "
                 "Nothing was written.\n")
    recs = {s: read(s) for s in plan.SESSIONS[1:]}
    out = score(checks.design, recs, labels())
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "lines": {"X-a": frac(plan.X_A_MAX_GAP), "X-b": frac(plan.X_B_LINE),
                        "X-c": frac(plan.X_C_LINE), "X-d": frac(plan.X_D_LINE),
                        "X-e": frac(plan.X_E_LINE), "X-f": frac(plan.X_F_LINE)},
              **out}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in out["verdicts"].items():
        val = v["value"]["value"] if v.get("value") else None
        print(f"  {rid}: {v['verdict']}{', thin' if v.get('thin') else ''} "
              f"({val if val is None else round(val, 4)}, se {v.get('se')})")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
