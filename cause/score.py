"""
Stage C of `PLAN_CAUSE.md`: the six adjudications, and `CA-g`. Free, and gated:
it writes nothing while the plan is unsigned.

WHAT IT READS. Stage B's three records, the passes and the rarest queue's
session, and Stage A's record, whose design they must hold and whose `CA-a`
comparator and causes it reads. Every valid answer is classed by
`whole/paragraph.py`'s `classed`, which is `placement/cost.py`'s `draft_class`,
as `PLAN_HALVES.md`'s Stage C classed it, and every right-queue answer is coded
by `halves/hidden.py`'s codebook, called and not edited (§0).

VALIDITY IS §0's, `plan.valid`, the one the asker's flag reads: the call came
back, after its retries, with a payload that parses, from the pinned provider. An
empty object is valid, and classed *no rule*.

THE STATISTICS ARE §0's, and every one is a ratio of integer counts, compared
with its line exactly.

  - `W_x` over a selection of answers is `H_x / R_x`: `R_x` counts arm `x`'s
    valid answers of the right queue that name a valid rule, `H_x` those classed
    *whole*. `B_x` is `K_x / R_x` over the same answers, `K_x` those whose
    reasoning carries the codebook's `BETWEEN`.
  - `CA-b`, `CA-c`, `CA-d` and `CA-f` read both passes at the 136 tickets;
    `CA-e` reads both passes and the rarest queue's session at its seven.
  - `CA-a` is the mean over tickets of `v`'s share at the ticket, both passes,
    less `PLAN_HALVES.md`'s `v` share there, over its two passes.

THE ERROR, *THIN* AND NO VALUE ARE §0's, settled there and not here.

  - **The standard error is clustered by ticket.** For `Σ c_x W_x`, ticket `t`
    contributes `u_t = Σ c_x (h_{x,t} − W_x r_{x,t}) / R_x`, and the variance is
    `C/(C−1) · Σ u_t²` over the row's `C` tickets; `CA-f` reads `B` the same way.
    `halves.score.contrast` computes it, called. `CA-a`'s is its mean's.
  - **A verdict is *thin*** when the statistic lies within one standard error of
    its line, or of the nearer edge of `CA-a`'s band; or when either pass alone
    puts it on the other side; for `CA-e`, when leaving out any one of its
    seven tickets does.
  - **A row has no value** when more than a twentieth of the answers it reads
    are invalid; `CA-a` with fewer than 50 tickets; `CA-c` when `W_e − W_v` is a
    tenth or less; `CA-e` when fewer than five of its tickets carry a right-queue
    answer under both `r` and `v`; `CA-f` when `B_v` is a fifth or less.

    python3 -m cause.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m cause.score
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from halves import hidden as hhidden
from halves import score as hscore
from reasoned_loop import score as rl_score
from whole import paragraph as W

from . import ask as cask
from . import gates, plan, population, prompts

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
WHOLE = "whole"
RIGHT_OUT = W.RIGHT_OUT
PASSES = plan.PASSES
WITH_ONCALL = PASSES + ("oncall",)
RULE_ID = re.compile(r"^H\d\d$")
BETWEEN = "BETWEEN"

# `PLAN_HALVES.md`'s, called: the selection, the tally of W, the share, the
# contrast and its clustered error, the share of invalid answers, the breadths
# and the calls. Each reads the rows it is handed and nothing of that plan.
selected, tally, share, contrast = hscore.selected, hscore.tally, hscore.share, hscore.contrast
invalid_share, ticket_weighted = hscore.invalid_share, hscore.ticket_weighted
breadths, calls = hscore.breadths, hscore.calls

COEFFS: dict[str, dict[str, Fraction]] = {
    "CA-b": {"e": F(1), "v": F(-1)},
    "CA-c": {"i": F(1), "e": F(-1, 2), "v": F(-1, 2)},
    "CA-d": {"i": F(1), "r": F(-1)},
    "CA-e": {"r": F(1), "v": F(-1)},
    "CA-f": {"v": F(1), "i": F(-1)},
}
ON_B = ("CA-f",)                   # the rows that read B and not W


def holds(rid: str, x: Fraction) -> bool:
    """§0's side of the line."""
    line, side = plan.LINES[rid], plan.SIDES[rid]
    if side == ">=":
        return x >= line
    if side == ">":
        return x > line
    if side == "within":
        return -line <= x <= line
    raise ValueError(f"no side {side!r} for {rid}")


def distance(rid: str, x: Fraction) -> Fraction:
    """How far a statistic lies from its line, or from the nearer edge of a band."""
    line = plan.LINES[rid]
    if plan.SIDES[rid] == "within":
        return min(abs(x - line), abs(x + line))
    return abs(x - line)


# ---------------------------------------------------------------------------
# The answers
# ---------------------------------------------------------------------------

def note_of(r: dict[str, Any]) -> str:
    payload = r.get("payload") if isinstance(r.get("payload"), dict) else {}
    return str(payload.get("note") or "")


def classed_rows(records: dict[str, dict]) -> list[dict[str, Any]]:
    """Every answer of the sessions, valid as §0 reads it, with its class when it
    is valid and the codebook's codes when it names the right queue and a valid
    rule. The asker's flag is kept as `valid_as_recorded`."""
    out = []
    for session, rec in records.items():
        for r in rec["rows"]:
            ok = plan.valid(r.get("failure"), r.get("payload"), r.get("served_by"))
            c = W.classed(r["ticket"], r.get("payload")) if ok else None
            codes = (hhidden.codes(r.get("reasoning"), note_of(r))
                     if ok and c not in RIGHT_OUT else None)
            out.append({**r, "session": session, "valid_as_recorded": r.get("valid"),
                        "valid": ok, "class": c, "codes": codes})
    return out


def tally_b(rows: list[dict], arms, tickets, sessions) -> dict[str, dict[int, list[int]]]:
    """`k` and `r` by arm and ticket: the answers `W` reads, and those of them
    whose reasoning carries `BETWEEN`."""
    out = {a: {t: [0, 0] for t in tickets} for a in arms}
    for r in selected(rows, arms, tickets, sessions):
        if r.get("valid") and r["class"] not in RIGHT_OUT:
            out[r["arm"]][r["ticket"]][1] += 1
            out[r["arm"]][r["ticket"]][0] += bool((r.get("codes") or {}).get(BETWEEN))
    return out


def tally_of(rid: str):
    return tally_b if rid in ON_B else tally


# ---------------------------------------------------------------------------
# The rows
# ---------------------------------------------------------------------------

def verdict(rid: str, value: Fraction | None, se: float | None, thin: bool,
            why: str | None, **parts) -> dict[str, Any]:
    line, at = plan.LINES[rid], plan.SIDES[rid]
    if value is None:
        return {"verdict": NO_VALUE, "why": why, "value": None, "line": frac(line),
                "holds_at": at, "se": None, "thin": False, **parts}
    return {"verdict": HOLDS if holds(rid, value) else REFUTED, "value": frac(value),
            "line": frac(line), "holds_at": at, "se": se, "thin": thin, "why": None, **parts}


def contrast_row(rid: str, rows: list[dict]) -> dict[str, Any]:
    """`CA-b` to `CA-f`: a contrast of shares, its error, *thin* and no value."""
    coeffs = COEFFS[rid]
    oncall = rid == "CA-e"
    tickets = plan.ONCALL if oncall else plan.TICKETS
    sessions = WITH_ONCALL if oncall else PASSES
    arms = tuple(coeffs)
    count = tally_of(rid)
    tal = count(rows, arms, tickets, sessions)
    value, se = contrast(coeffs, tal)
    parts: dict[str, Any] = {"shares": {a: frac(share(tal[a])) for a in arms}}
    bad = invalid_share(rows, arms, tickets, sessions)
    parts["invalid_share"] = frac(bad)
    if bad is None or bad > plan.MAX_INVALID_SHARE:
        return verdict(rid, None, None, False, "more than a twentieth of its answers invalid",
                       **parts)
    if rid == "CA-c":
        gap, _ = contrast(COEFFS["CA-b"], tally(rows, ("e", "v"), tickets, sessions))
        parts["gap"] = frac(gap)
        if gap is None or gap <= plan.CA_C_MIN_GAP:
            return verdict(rid, None, None, False, "the gap W_e − W_v is a tenth or less",
                           **parts)
    if oncall:
        both = [t for t in tickets if tal["r"][t][1] and tal["v"][t][1]]
        parts["tickets_with_both"] = len(both)
        if len(both) < plan.CA_E_MIN_TICKETS:
            return verdict(rid, None, None, False,
                           "fewer than five of its tickets carry both arms", **parts)
    if rid == "CA-f":
        b_v = share(tal["v"])
        if b_v is None or b_v <= plan.CA_F_MIN_B:
            return verdict(rid, None, None, False, "B_v is a fifth or less", **parts)
    if value is None:
        return verdict(rid, None, None, False, "an arm has no right-queue answer", **parts)
    thin = se is not None and float(distance(rid, value)) < se
    others: dict[str, Any] = {}
    if oncall:
        for t in tickets:
            rest = tuple(x for x in tickets if x != t)
            v, _ = contrast(coeffs, count(rows, arms, rest, sessions))
            others[str(t)] = frac(v)
            thin |= v is not None and holds(rid, v) != holds(rid, value)
        parts["leaving_one_ticket_out"] = others
    else:
        for s in PASSES:
            v, _ = contrast(coeffs, count(rows, arms, tickets, (s,)))
            others[s] = frac(v)
            thin |= v is not None and holds(rid, v) != holds(rid, value)
        parts["by_pass"] = others
    return verdict(rid, value, se, thin, None, **parts)


def ca_a_value(rows: list[dict], comparator: dict[str, dict], sessions
               ) -> tuple[Fraction | None, float | None, int]:
    tal = tally(rows, ("v",), plan.TICKETS, sessions)["v"]
    diffs = []
    for t in plan.TICKETS:
        h, r = tal[t]
        theirs = comparator.get(str(t))
        if r and theirs and theirs["right_queue"]:
            diffs.append(F(h, r) - F(theirs["whole"], theirs["right_queue"]))
    c = len(diffs)
    if not c:
        return None, None, 0
    mean = sum(diffs, F(0)) / c
    se = math.sqrt(sum(float(d - mean) ** 2 for d in diffs) / (c * (c - 1))) if c > 1 else None
    return mean, se, c


def ca_a(rows: list[dict], comparator: dict[str, dict]) -> dict[str, Any]:
    value, se, c = ca_a_value(rows, comparator, PASSES)
    bad = invalid_share(rows, ("v",), plan.TICKETS, PASSES)
    parts: dict[str, Any] = {"tickets": c, "invalid_share": frac(bad)}
    if bad is None or bad > plan.MAX_INVALID_SHARE:
        return verdict("CA-a", None, None, False, "more than a twentieth of its answers invalid",
                       **parts)
    if c < plan.CA_A_MIN_TICKETS:
        return verdict("CA-a", None, None, False, "fewer than 50 tickets", **parts)
    thin = se is not None and float(distance("CA-a", value)) < se
    by_pass = {}
    for s in PASSES:
        v, _, _ = ca_a_value(rows, comparator, (s,))
        by_pass[s] = frac(v)
        thin |= v is not None and holds("CA-a", v) != holds("CA-a", value)
    return verdict("CA-a", value, se, thin, None, by_pass=by_pass, **parts)


# ---------------------------------------------------------------------------
# CA-g: what the drafter could not band
# ---------------------------------------------------------------------------

def by_key(rows: list[dict], key: Callable[[int], str], arms) -> dict[str, Any]:
    """Each arm's `W` over both passes, by a key of the ticket."""
    out: dict[str, dict[str, list[int]]] = {}
    for r in selected(rows, arms, plan.TICKETS, PASSES):
        if r.get("valid") and r["class"] not in RIGHT_OUT:
            x = out.setdefault(key(r["ticket"]), {}).setdefault(r["arm"], [0, 0])
            x[1] += 1
            x[0] += r["class"] == WHOLE
    return {k: {a: {"whole": h, "right_queue": n, "share": frac(F(h, n))}
                for a, (h, n) in sorted(v.items())} for k, v in sorted(out.items())}


def agreement(rows: list[dict]) -> dict[str, Any]:
    """By arm, how often a prompt's two answers in the passes share a class."""
    got: dict[str, dict[str, dict[str, str]]] = {}
    for r in selected(rows, prompts.ARMS, plan.TICKETS, PASSES):
        if r.get("valid"):
            got.setdefault(r["arm"], {}).setdefault(r["prompt"], {})[r["session"]] = r["class"]
    out = {}
    for arm, by in got.items():
        both = [v for v in by.values() if len(v) == 2]
        same = sum(1 for v in both if v["pass1"] == v["pass2"])
        out[arm] = {"prompts": len(both), "same_class": same,
                    "share": frac(F(same, len(both))) if both else None}
    return out


def declarations(rows: list[dict]) -> dict[str, Any]:
    out = {}
    for arm in prompts.ARMS:
        valid = [r for r in rows if r["arm"] == arm and r.get("valid")]
        sides = [r for r in valid if (r["payload"].get("beats") or r["payload"].get("loses_to"))]
        cites = [r for r in sides if any(RULE_ID.match(str(x)) for x in
                                         (r["payload"].get("beats") or [])
                                         + (r["payload"].get("loses_to") or []))]
        out[arm] = {"valid": len(valid), "declaring": len(sides), "citing_the_manual": len(cites)}
    return out


def codes_by_class(rows: list[dict]) -> dict[str, Any]:
    """By arm and class, how many right-queue answers carry each code, over both
    passes."""
    out: dict[str, dict[str, Counter]] = {}
    for r in selected(rows, prompts.ARMS, plan.TICKETS, PASSES):
        if r.get("valid") and r["class"] not in RIGHT_OUT:
            k = hhidden.kind(r["class"])
            c = out.setdefault(r["arm"], {}).setdefault(k, Counter())
            c["answers"] += 1
            for code, on in (r.get("codes") or {}).items():
                c[code] += bool(on)
    return {a: {k: dict(c) for k, c in sorted(v.items())} for a, v in sorted(out.items())}


def names_a_queue(rows: list[dict]) -> dict[str, Any]:
    """By arm, the valid answers whose action is not one of the eight queues."""
    return {arm: sum(1 for r in rows if r["arm"] == arm and r.get("valid")
                     and not r.get("names_a_queue")) for arm in prompts.ARMS}


def where_the_loops_met(rows: list[dict], causes: dict[str, dict]) -> dict[str, Any]:
    """Each notice at the tickets where the DeepInfra loops met its cause, both
    passes: `i` where they met an impasse, `r` where they met a reported error,
    and `v` at each set, beside it."""
    def met(cause: str) -> list[int]:
        return [t for t in plan.TICKETS
                if any((causes.get(str(t)) or {}).get(g, {}).get(cause)
                       for g in plan.DEEPINFRA_GROUPS)]

    out = {}
    for arm, cause in ((prompts.IMPASSE, "IMPASSE"), (prompts.REVIEW, "ERROR")):
        ts = met(cause)
        tal = tally(rows, (arm, "v", "e"), ts, PASSES)
        out[f"{arm}_where_{cause.lower()}"] = {
            "tickets": len(ts), **{a: frac(share(tal[a])) for a in (arm, "v", "e")}}
    return out


def beside_halves(rows: list[dict], sample: dict) -> dict[str, Any]:
    """`e` and `v` beside `PLAN_HALVES.md`'s, over both passes, pooled and by
    ticket. Reported, never adjudicated."""
    refs = sample["references"]["halves"]
    out = {}
    for arm in (prompts.EMPTY, prompts.V2B):
        tal = tally(rows, (arm,), plan.TICKETS, PASSES)[arm]
        theirs = {t: [x for x in xs if x["session"] in PASSES and x["valid"]
                      and x["class"] not in RIGHT_OUT] for t, xs in refs[arm].items()}
        h = sum(1 for xs in theirs.values() for x in xs if x["class"] == WHOLE)
        n = sum(len(xs) for xs in theirs.values())
        out[arm] = {"today": frac(share(tal)), "halves": frac(F(h, n)) if n else None,
                    "by_ticket": {str(t): {"today": tal[t],
                                           "halves": [sum(1 for x in theirs.get(str(t), [])
                                                          if x["class"] == WHOLE),
                                                      len(theirs.get(str(t), []))]}
                                  for t in plan.TICKETS}}
    return out


def reported(rows: list[dict], records: dict[str, dict], sample: dict) -> dict[str, Any]:
    tal = tally(rows, prompts.ARMS, plan.TICKETS, PASSES)
    tal_b = tally_b(rows, prompts.ARMS, plan.TICKETS, PASSES)
    t7 = tally(rows, prompts.ARMS, plan.ONCALL, WITH_ONCALL)
    w = {a: share(tal[a]) for a in prompts.ARMS}
    gov = sample["tickets"]
    valid = {a: [r for r in rows if r["arm"] == a and r.get("valid")
                 and r["session"] in PASSES] for a in prompts.ARMS}
    at_t7: dict[str, dict[str, dict[str, int]]] = {}
    for r in selected(rows, prompts.ARMS, plan.ONCALL, WITH_ONCALL):
        at_t7.setdefault(str(r["ticket"]), {}).setdefault(r["arm"], Counter())[
            r["class"] if r.get("valid") else "invalid"] += 1
    other_e, _ = contrast({"i": F(1), "v": F(-1)}, t7)
    other_f, _ = contrast({"v": F(1), "r": F(-1)}, tal_b)
    return {
        "W": {a: {"pooled": frac(w[a]), "ticket_weighted": frac(ticket_weighted(tal[a])),
                  "by_pass": {s: frac(share(tally(rows, (a,), plan.TICKETS, (s,))[a]))
                              for s in PASSES},
                  "at_the_seven": frac(share(t7[a]))} for a in prompts.ARMS},
        "B": {a: {"pooled": frac(share(tal_b[a])),
                  "by_pass": {s: frac(share(tally_b(rows, (a,), plan.TICKETS, (s,))[a]))
                              for s in PASSES}} for a in prompts.ARMS},
        "under_the_other_notice": {"W_i7_less_W_v7": frac(other_e),
                                   "B_v_less_B_r": frac(other_f)},
        "where_the_loops_met_the_cause": where_the_loops_met(rows,
                                                             sample["references"]["causes"]),
        "classes": {a: dict(Counter(r["class"] for r in valid[a])) for a in prompts.ARMS},
        "wrong_queue_and_no_rule": {
            a: {"valid": len(valid[a]),
                "wrong_queue": sum(1 for r in valid[a] if r["class"] == "wrong_queue"),
                "no_rule": sum(1 for r in valid[a] if r["class"] == "no_rule")}
            for a in prompts.ARMS},
        "codes_by_class": codes_by_class(rows),
        "by_governing_rule": by_key(rows, lambda t: gov[str(t)]["governing"], prompts.ARMS),
        "by_queue": by_key(rows, lambda t: gov[str(t)]["queue"], prompts.ARMS),
        "agreement_between_the_passes": agreement(rows),
        "the_seven": {t: {a: dict(c) for a, c in sorted(v.items())}
                      for t, v in sorted(at_t7.items(), key=lambda x: int(x[0]))},
        "breadth": breadths(rows),
        "declarations": declarations(rows),
        "valid_answers_naming_no_queue": names_a_queue(rows),
        "beside_halves": beside_halves(rows, sample),
        "calls": calls(records),
    }


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def score(records: dict[str, dict], sample: dict) -> dict[str, Any]:
    rows = classed_rows(records)
    comparator = sample["references"]["ca_a_comparator"]
    verdicts = {"CA-a": ca_a(rows, comparator)}
    for rid in ("CA-b", "CA-c", "CA-d", "CA-e", "CA-f"):
        verdicts[rid] = contrast_row(rid, rows)
    return {"verdicts": verdicts, "CA-g": reported(rows, records, sample)}


def read_records(design: population.Design) -> dict[str, dict]:
    """The passes and the rarest queue's session, each under this protocol and
    holding its session's asks."""
    out = {}
    for s in WITH_ONCALL:
        path = plan.ask_path(s)
        if not path.exists():
            sys.exit(f"\nREFUSED: no record of {s} at {path}; nothing was written.\n")
        rec = json.loads(path.read_text())
        wrong = cask.under_protocol(rec)
        if wrong:
            sys.exit(f"\nREFUSED: {path} was not produced under this protocol: "
                     f"{sorted(wrong)}; nothing was written.\n")
        if sorted(r["id"] for r in rec["rows"]) != sorted(design.sessions[s]):
            sys.exit(f"\nREFUSED: {path} does not hold its session's asks; nothing was "
                     "written.\n")
        out[s] = rec
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_CAUSE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CA-g1 to CA-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("cause/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    ok, why = cask.sample_matches(checks.design)
    if not ok:
        sys.exit(f"\nREFUSED: {why}; nothing was written.\n")
    sample = json.loads(plan.sample_path().read_text())
    records = read_records(checks.design)
    scored = score(records, sample)
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "C",
              "signature": gate, "gates": checks.summary(),
              "sources": {s: str(plan.ask_path(s)) for s in WITH_ONCALL}, **scored}
    plan.score_path().parent.mkdir(parents=True, exist_ok=True)
    plan.score_path().write_text(json.dumps(record, indent=2, default=str))
    for rid, v in scored["verdicts"].items():
        print(f"  {rid}  {v['verdict']}{', thin' if v.get('thin') else ''}")
    print(f"\n-> {plan.score_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
