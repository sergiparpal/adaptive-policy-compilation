"""
Stage C of `PLAN_HALVES.md`: the six adjudications, and `HV-g`. Free, and
gated: it writes nothing while the plan is unsigned.

WHAT IT READS. Stage B's three records, the passes and the rarest queue's
session, and Stage A's record, whose design they must hold and whose `HV-a`
comparator it reads. Every valid answer is classed by `whole/paragraph.py`'s
`classed`, which is `placement/cost.py`'s `draft_class`, as `PLAN_WHOLE.md`'s
Stage C classed a first-call draft (§0).

**[Corrected before Stage C, 2026-11-10.] Validity is §0's.** An answer is valid
when the call came back, after its retries, with a payload that parses, from the
pinned provider. The asker's own flag, `valid` in each row, also asks for an
action among the eight queues, which §0 does not, so an empty object came back
flagged invalid: four of pass 1's first 126 answers were one. The scorer reads
§0's definition, classes an empty object *no rule*, and keeps the asker's flag
as `valid_as_recorded`; `HV-g` counts where the two differ. No figure of Stage C
existed when this was corrected, and no answer was classed to find it.

THE STATISTICS ARE §0's, and every one is a ratio of integer counts, compared
with its line exactly.

  - `W_x` over a selection of answers is `H_x / R_x`: `R_x` counts arm `x`'s
    valid answers of the right queue that name a valid rule, `H_x` those classed
    *whole*.
  - `HV-b` to `HV-e` read both passes at the 136 tickets; `HV-f` reads both
    passes and the rarest queue's session at its seven.
  - `HV-a` is the mean over tickets of `v`'s share at the ticket, both passes,
    less the DeepInfra loops' first calls' share there.

THE ERROR, *THIN* AND NO VALUE ARE §0's, settled there and not here.

  - **The standard error is clustered by ticket.** For `Σ c_x W_x`, ticket `t`
    contributes `u_t = Σ c_x (h_{x,t} − W_x r_{x,t}) / R_x`, and the variance is
    `C/(C−1) · Σ u_t²` over the row's `C` tickets. `HV-a`'s is its mean's.
  - **A verdict is *thin*** when the statistic lies within one standard error of
    its line, or of the nearer edge of `HV-a`'s band; or when either pass alone
    puts it on the other side; for `HV-f`, when leaving out any one of its
    seven tickets does.
  - **A row has no value** when more than a twentieth of the answers it reads
    are invalid; `HV-a` with fewer than 50 tickets; `HV-c` when `W_e − W_v` is a
    tenth or less; `HV-f` when fewer than five of its tickets carry a
    right-queue answer under both `h` and `v`.

    python3 -m halves.score --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m halves.score
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Callable

from harness.provenance import describe, environment

from reasoned_loop import score as rl_score
from whole import paragraph as W
from whole import references

from . import ask as hask
from . import gates, plan, population, prompts

F = Fraction
HOLDS, REFUTED, NO_VALUE = rl_score.HOLDS, rl_score.REFUTED, rl_score.NO_VALUE
frac = rl_score.frac
WHOLE = "whole"
RIGHT_OUT = W.RIGHT_OUT
PASSES = plan.PASSES
WITH_ONCALL = PASSES + ("oncall",)
RULE_ID = re.compile(r"^H\d\d$")

COEFFS: dict[str, dict[str, Fraction]] = {
    "HV-b": {"e": F(1), "v": F(-1)},
    "HV-c": {"h": F(1), "e": F(-1, 2), "v": F(-1, 2)},
    "HV-d": {"e": F(1), "h": F(-1)},
    "HV-e": {"e": F(1), "o": F(-1)},
    "HV-f": {"h": F(1), "v": F(-1)},
}


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

def valid(r: dict[str, Any]) -> bool:
    """§0's validity: the call came back, after its retries, with a payload that
    parses, from the pinned provider. An empty object is such a payload, and its
    class is *no rule*. The asker's flag also asks for an action among the eight
    queues, which §0 does not (the correction above)."""
    return (r.get("failure") is None and isinstance(r.get("payload"), dict)
            and r.get("served_by") == plan.PROVIDER_NAME)


def classed_rows(records: dict[str, dict]) -> list[dict[str, Any]]:
    """Every answer of the sessions, valid as §0 reads it, with its class when it
    is valid. The asker's flag is kept as `valid_as_recorded`."""
    out = []
    for session, rec in records.items():
        for r in rec["rows"]:
            ok = valid(r)
            c = W.classed(r["ticket"], r.get("payload")) if ok else None
            out.append({**r, "session": session, "valid_as_recorded": r.get("valid"),
                        "valid": ok, "class": c})
    return out


def selected(rows: list[dict], arms, tickets, sessions) -> list[dict]:
    arms, tickets, sessions = set(arms), set(tickets), set(sessions)
    return [r for r in rows if r["arm"] in arms and r["ticket"] in tickets
            and r["session"] in sessions]


def tally(rows: list[dict], arms, tickets, sessions) -> dict[str, dict[int, list[int]]]:
    """`h` and `r` by arm and ticket, over the valid answers the selection reads."""
    out = {a: {t: [0, 0] for t in tickets} for a in arms}
    for r in selected(rows, arms, tickets, sessions):
        if r.get("valid") and r["class"] not in RIGHT_OUT:
            out[r["arm"]][r["ticket"]][1] += 1
            out[r["arm"]][r["ticket"]][0] += r["class"] == WHOLE
    return out


def share(by_ticket: dict[int, list[int]]) -> Fraction | None:
    h = sum(x[0] for x in by_ticket.values())
    r = sum(x[1] for x in by_ticket.values())
    return F(h, r) if r else None


def contrast(coeffs: dict[str, Fraction], tal: dict[str, dict[int, list[int]]]
             ) -> tuple[Fraction | None, float | None]:
    """`Σ c_x W_x`, and its standard error clustered by ticket (§0)."""
    ws = {a: share(tal[a]) for a in coeffs}
    if any(w is None for w in ws.values()):
        return None, None
    value = sum((c * ws[a] for a, c in coeffs.items()), F(0))
    rs = {a: sum(x[1] for x in tal[a].values()) for a in coeffs}
    tickets = sorted(next(iter(tal.values())))
    if len(tickets) < 2:
        return value, None
    u = [sum(float(c) * (tal[a][t][0] - float(ws[a]) * tal[a][t][1]) / rs[a]
             for a, c in coeffs.items()) for t in tickets]
    c = len(tickets)
    return value, math.sqrt(c / (c - 1) * sum(x * x for x in u))


def invalid_share(rows: list[dict], arms, tickets, sessions) -> Fraction | None:
    sel = selected(rows, arms, tickets, sessions)
    return F(sum(1 for r in sel if not r.get("valid")), len(sel)) if sel else None


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
    """`HV-b` to `HV-f`: a contrast of shares, its error, *thin* and no value."""
    coeffs = COEFFS[rid]
    oncall = rid == "HV-f"
    tickets = plan.ONCALL if oncall else plan.TICKETS
    sessions = WITH_ONCALL if oncall else PASSES
    arms = tuple(coeffs)
    tal = tally(rows, arms, tickets, sessions)
    value, se = contrast(coeffs, tal)
    parts: dict[str, Any] = {"shares": {a: frac(share(tal[a])) for a in arms}}
    bad = invalid_share(rows, arms, tickets, sessions)
    parts["invalid_share"] = frac(bad)
    if bad is None or bad > plan.MAX_INVALID_SHARE:
        return verdict(rid, None, None, False, "more than a twentieth of its answers invalid",
                       **parts)
    if rid == "HV-c":
        gap, _ = contrast(COEFFS["HV-b"], tally(rows, ("e", "v"), tickets, sessions))
        parts["gap"] = frac(gap)
        if gap is None or gap <= plan.HV_C_MIN_GAP:
            return verdict(rid, None, None, False, "the gap W_e − W_v is a tenth or less",
                           **parts)
    if oncall:
        both = [t for t in tickets if tal["h"][t][1] and tal["v"][t][1]]
        parts["tickets_with_both"] = len(both)
        if len(both) < plan.HV_F_MIN_TICKETS:
            return verdict(rid, None, None, False,
                           "fewer than five of its tickets carry both arms", **parts)
    if value is None:
        return verdict(rid, None, None, False, "an arm has no right-queue answer", **parts)
    thin = se is not None and float(distance(rid, value)) < se
    others: dict[str, Any] = {}
    if oncall:
        for t in tickets:
            rest = tuple(x for x in tickets if x != t)
            v, _ = contrast(coeffs, tally(rows, arms, rest, sessions))
            others[str(t)] = frac(v)
            thin |= v is not None and holds(rid, v) != holds(rid, value)
        parts["leaving_one_ticket_out"] = others
    else:
        for s in PASSES:
            v, _ = contrast(coeffs, tally(rows, arms, tickets, (s,)))
            others[s] = frac(v)
            thin |= v is not None and holds(rid, v) != holds(rid, value)
        parts["by_pass"] = others
    return verdict(rid, value, se, thin, None, **parts)


def hv_a_value(rows: list[dict], comparator: dict[str, dict], sessions
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


def hv_a(rows: list[dict], comparator: dict[str, dict]) -> dict[str, Any]:
    value, se, c = hv_a_value(rows, comparator, PASSES)
    bad = invalid_share(rows, ("v",), plan.TICKETS, PASSES)
    parts: dict[str, Any] = {"tickets": c, "invalid_share": frac(bad)}
    if bad is None or bad > plan.MAX_INVALID_SHARE:
        return verdict("HV-a", None, None, False, "more than a twentieth of its answers invalid",
                       **parts)
    if c < plan.HV_A_MIN_TICKETS:
        return verdict("HV-a", None, None, False, "fewer than 50 tickets", **parts)
    thin = se is not None and float(distance("HV-a", value)) < se
    by_pass = {}
    for s in PASSES:
        v, _, _ = hv_a_value(rows, comparator, (s,))
        by_pass[s] = frac(v)
        thin |= v is not None and holds("HV-a", v) != holds("HV-a", value)
    return verdict("HV-a", value, se, thin, None, by_pass=by_pass, **parts)


# ---------------------------------------------------------------------------
# HV-g: what the drafter could not band
# ---------------------------------------------------------------------------

def ticket_weighted(by_ticket: dict[int, list[int]]) -> Fraction | None:
    shares = [F(h, r) for h, r in by_ticket.values() if r]
    return sum(shares, F(0)) / len(shares) if shares else None


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


def askers_flag(rows: list[dict]) -> dict[str, Any]:
    """By arm, the answers the asker flagged invalid that §0 reads as valid, and
    their classes."""
    out = {}
    for arm in prompts.ARMS:
        differ = [r for r in rows if r["arm"] == arm and r["valid"]
                  and not r.get("valid_as_recorded")]
        out[arm] = {"answers": len(differ), "classes": dict(Counter(r["class"] for r in differ))}
    return out


def breadths(rows: list[dict]) -> dict[str, Any]:
    _, cases, _, _, _ = references._world()
    out: dict[str, Counter] = {}
    for r in rows:
        if r.get("valid") and r["class"] not in RIGHT_OUT:
            b = references.breadth({"calls": [{"payload": r["payload"]}]}, cases[r["ticket"]])
            out.setdefault(r["arm"], Counter())[f"{r['class']}|{b}"] += 1
    return {a: dict(sorted(c.items())) for a, c in sorted(out.items())}


def calls(records: dict[str, dict]) -> dict[str, Any]:
    out = {}
    for session, rec in records.items():
        rows = rec["rows"]
        attempts = [a for r in rows for a in r.get("call_attempts") or []]
        came = [a for a in attempts if a.get("error") is None
                and a.get("completion_tokens") is not None]
        secs = [r["seconds"] for r in rows if r.get("seconds") is not None]
        med = lambda xs: statistics.median(xs) if xs else None   # noqa: E731
        out[session] = {
            "asks": len(rows), "valid": sum(1 for r in rows if r.get("valid")),
            "failed": sum(1 for r in rows if r.get("failure")),
            "providers": dict(Counter(str(a.get("provider")) for a in attempts)),
            "finish_reasons": dict(Counter(str(a.get("finish_reason")) for a in attempts)),
            "prompt_tokens_median": med([a["prompt_tokens"] for a in came]),
            "completion_tokens_median": med([a["completion_tokens"] for a in came]),
            "reasoning_tokens_median": med([a.get("reasoning_tokens") or 0 for a in came]),
            "seconds_median": med(secs),
            "seconds_mean": statistics.mean(secs) if secs else None,
            "retries": dict(Counter(c for r in rows for c in (r.get("retries") or []))),
        }
    return out


def beside_the_references(rows: list[dict], sample: dict) -> dict[str, Any]:
    """`e` beside the rule arm at its tickets, and `v` beside each loop group at
    its, across dates and providers. Reported, never adjudicated."""
    refs = sample["references"]

    def pooled(by: dict[str, list[str]]) -> dict[str, Any]:
        cs = [c for v in by.values() for c in v]
        right = [c for c in cs if c not in RIGHT_OUT]
        held = sum(1 for c in right if c == WHOLE)
        return {"answers": len(cs), "right_queue": len(right), "whole": held,
                "share": frac(F(held, len(right))) if right else None}

    def today(arm: str, tickets) -> dict[str, Any]:
        tal = tally(rows, (arm,), [int(t) for t in tickets], PASSES)[arm]
        h, r = sum(x[0] for x in tal.values()), sum(x[1] for x in tal.values())
        return {"whole": h, "right_queue": r, "share": frac(F(h, r)) if r else None}

    out = {"e_and_the_rule_arm": {"tickets": len(refs["rule_arm"]),
                                  "today": today("e", refs["rule_arm"]),
                                  "the_rule_arm": pooled(refs["rule_arm"])}}
    for g, by in refs["loops"].items():
        out[f"v_and_{g}"] = {"tickets": len(by), "today": today("v", by),
                             "the_loop": pooled(by)}
    return out


def reported(rows: list[dict], records: dict[str, dict], sample: dict) -> dict[str, Any]:
    tal = tally(rows, prompts.ARMS, plan.TICKETS, PASSES)
    t7 = tally(rows, prompts.ARMS, plan.ONCALL, WITH_ONCALL)
    w = {a: share(tal[a]) for a in prompts.ARMS}
    gov = sample["tickets"]
    inter = (w["h"] - w["v"]) - (w["e"] - w["o"]) if None not in w.values() else None
    valid = {a: [r for r in rows if r["arm"] == a and r.get("valid")
                 and r["session"] in PASSES] for a in prompts.ARMS}
    at_t7: dict[str, dict[str, dict[str, int]]] = {}
    for r in selected(rows, prompts.ARMS, plan.ONCALL, WITH_ONCALL):
        at_t7.setdefault(str(r["ticket"]), {}).setdefault(r["arm"], Counter())[
            r["class"] if r.get("valid") else "invalid"] += 1
    return {
        "W": {a: {"pooled": frac(w[a]), "ticket_weighted": frac(ticket_weighted(tal[a])),
                  "by_pass": {s: frac(share(tally(rows, (a,), plan.TICKETS, (s,))[a]))
                              for s in PASSES},
                  "at_the_seven": frac(share(t7[a]))} for a in prompts.ARMS},
        "interaction": frac(inter),
        "classes": {a: dict(Counter(r["class"] for r in valid[a])) for a in prompts.ARMS},
        "wrong_queue_and_no_rule": {
            a: {"valid": len(valid[a]),
                "wrong_queue": sum(1 for r in valid[a] if r["class"] == "wrong_queue"),
                "no_rule": sum(1 for r in valid[a] if r["class"] == "no_rule")}
            for a in prompts.ARMS},
        "by_governing_rule": by_key(rows, lambda t: gov[str(t)]["governing"], prompts.ARMS),
        "by_queue": by_key(rows, lambda t: gov[str(t)]["queue"], prompts.ARMS),
        "agreement_between_the_passes": agreement(rows),
        "the_seven": {t: {a: dict(c) for a, c in sorted(v.items())}
                      for t, v in sorted(at_t7.items(), key=lambda x: int(x[0]))},
        "breadth": breadths(rows),
        "declarations": declarations(rows),
        "the_askers_flag": askers_flag(rows),
        "beside_the_references": beside_the_references(rows, sample),
        "calls": calls(records),
    }


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def score(records: dict[str, dict], sample: dict) -> dict[str, Any]:
    rows = classed_rows(records)
    comparator = sample["references"]["hv_a_comparator"]
    verdicts = {"HV-a": hv_a(rows, comparator)}
    for rid in ("HV-b", "HV-c", "HV-d", "HV-e", "HV-f"):
        verdicts[rid] = contrast_row(rid, rows)
    return {"verdicts": verdicts, "HV-g": reported(rows, records, sample)}


def read_records(design: population.Design) -> dict[str, dict]:
    """The passes and the rarest queue's session, each under this protocol and
    holding its session's asks."""
    out = {}
    for s in WITH_ONCALL:
        path = plan.ask_path(s)
        if not path.exists():
            sys.exit(f"\nREFUSED: no record of {s} at {path}; nothing was written.\n")
        rec = json.loads(path.read_text())
        wrong = hask.under_protocol(rec)
        if wrong:
            sys.exit(f"\nREFUSED: {path} was not produced under this protocol: "
                     f"{sorted(wrong)}; nothing was written.\n")
        if sorted(r["id"] for r in rec["rows"]) != sorted(design.sessions[s]):
            sys.exit(f"\nREFUSED: {path} does not hold its session's asks; nothing was "
                     "written.\n")
        out[s] = rec
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage C of PLAN_HALVES.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run HV-g1 to HV-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("halves/score.py writes Stage C")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    ok, why = hask.sample_matches(checks.design)
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
