"""
Stage A of `PLAN_HALVES.md`: the design and the references. Free, and gated: it
writes nothing while the plan is unsigned, because a reference written before
the signature would be a figure that existed before its band (§10 of the plan).

WHAT IT WRITES, `results_halves/sample.json`:

  - **the design**: the 136 tickets, every ask with its digest, and the four
    sessions in their orders; the texts, their digests and the fingerprint;
  - **each ticket's governing rule and its queue**, the first rule of level 3's
    list whose region holds the ticket, read over the space through
    `whole.references`;
  - **the references**, ticket by ticket, classed as `whole/paragraph.py`
    classes an answer:
    - `PLAN_REASONED_RULE.md`'s arm `w`, at the tickets it asked, both passes;
    - each loop group's first calls, at the tickets of `T` it escalated;
    - `HV-a`'s comparator: the first calls of the DeepInfra loops under v2b's
      paragraph, `PLAN_PLACEMENT.md`'s six runs and `PLAN_WHOLE.md`'s three v1c
      runs, pooled;
  - **§0's four figures, recomputed**, and which of them did not come back as
    §0 declares them.

It reads the closed records and level 3's list, and asks nothing.

    python3 -m halves.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m halves.sample
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from typing import Any

from harness.provenance import describe, environment

from placement import oncall as PO
from reasoned_loop import governed as gv
from whole import paragraph as W
from whole import references

from . import gates, plan, prompts

PROVENANCE = ("Stage A of PLAN_HALVES.md, written after §0 was signed. Its four figures "
              "were computed while drafting, from the records as main held them at "
              "41b3ce4, and seen before §0's lines were drawn. Its references, the classes "
              "of the closed answers ticket by ticket, were not.")

# §0's figures as the plan declares them, which `not_back` holds the record to.
DECLARED = {
    "rule_arm_tickets": 171,
    "first_call_tickets": {"reasoned_loop": 216, "channel": 316, "placement": 250,
                           "whole_v1c": 171, "whole_v1d": 108},
    "first_call_tickets_in_all": 545,
    "shared": {"reasoned_loop": 91, "channel": 96, "placement": 88, "whole_v1c": 78,
               "whole_v1d": 60},
    "shared_in_all": 133,
    "shared_under_v2b": 131,
    "oncall": list(plan.ONCALL),
    "oncall_governing": ["H05", "H05", "H04", "H04", "H04", "H05", "H04"],
    "oncall_among_the_rule_arms": [257, 710, 1783, 1951],
    "shared_by_queue": {"T2_TECHNICAL": 48, "T1_GENERAL": 20, "SECURITY_INCIDENT": 19,
                        "SELF_SERVICE_DEFLECT": 15, "ACCOUNT_MANAGER": 11,
                        "T3_ENGINEERING": 11, "BILLING_SPECIALIST": 5,
                        "ONCALL_ESCALATION": 4},
    "security_tickets": 20,
    "security_shared": 19,
    "deepinfra": {"tickets": 102, "escalations": 405, "most_a_ticket": 9},
    "baidu": {"tickets": 117, "escalations": 523},
    "pace": {
        "placement": {"calls": 500, "seconds_median": 77.2, "seconds_mean": 89.4,
                      "reasoning_median": 4881, "completion_median": 5142,
                      "completion_mean": 5630, "prompt": 1762},
        "whole_v1c": {"calls": 244, "seconds_median": 95.1, "seconds_mean": 114.3,
                      "reasoning_median": 5053, "completion_median": 5258,
                      "completion_mean": 5682, "prompt": 1762},
        "whole_v1d": {"calls": 161, "seconds_median": 111.6, "seconds_mean": 130.5,
                      "reasoning_median": 4910, "completion_median": 5200,
                      "completion_mean": 5594, "prompt": 1857},
    },
    "attempts_at_the_budget": 1,
}

DEEPINFRA = plan.HV_A_GROUPS
BAIDU = ("reasoned_loop", "channel")


# ---------------------------------------------------------------------------
# The governing rules
# ---------------------------------------------------------------------------

def governing() -> dict[int, tuple[str, str]]:
    """Every corpus ticket's governing rule and its queue."""
    space, cases, regions, _, queues = references._world()
    out = {}
    for i, c in enumerate(cases):
        g = PO.matched(gv.point_of(c, space), regions)[0]
        out[i] = (g, queues[g])
    return out


# ---------------------------------------------------------------------------
# §0's figures
# ---------------------------------------------------------------------------

def escalated(loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Counter]:
    """By loop group, how many escalations each ticket had."""
    return {g: Counter(e["idx"] for _, rec in runs for e in rec["escalations"])
            for g, runs in loops.items()}


def pace(runs: list[tuple[str, dict]]) -> dict[str, Any]:
    """The first calls' seconds and tokens, over the attempts that came back."""
    secs, reason, compl, prompt, n, capped = [], [], [], [], 0, 0
    for _, rec in runs:
        for e in rec["escalations"]:
            c = (e.get("calls") or [{}])[0]
            if c.get("round") != 0:
                continue
            n += 1
            if c.get("seconds") is not None:
                secs.append(c["seconds"])
            for a in c.get("call_attempts") or []:
                if a.get("error") is None and a.get("completion_tokens") is not None:
                    compl.append(a["completion_tokens"])
                    prompt.append(a["prompt_tokens"])
                    reason.append(a.get("reasoning_tokens") or 0)
                    capped += a["completion_tokens"] >= plan.MAX_TOKENS
    return {"calls": n, "seconds_median": round(statistics.median(secs), 1),
            "seconds_mean": round(statistics.mean(secs), 1),
            "reasoning_median": round(statistics.median(reason)),
            "completion_median": round(statistics.median(compl)),
            "completion_mean": round(statistics.mean(compl)),
            "prompt": round(statistics.median(prompt)), "_capped": capped}


def figures(loops: dict[str, list[tuple[str, dict]]],
            gov: dict[int, tuple[str, str]]) -> dict[str, Any]:
    """§0's four figures, from the closed records. None reads an answer's class."""
    asked = {r["ticket"] for r in W.rule_arm_rows()}
    esc = escalated(loops)
    met = {g: set(c) for g, c in esc.items()}
    shared = {g: len(m & asked) for g, m in met.items()}
    every = set().union(*met.values())
    in_all = asked & every
    v2b = asked & set().union(*(met[g] for g in BAIDU + DEEPINFRA))
    t = set(plan.TICKETS)
    di = Counter()
    for g in DEEPINFRA:
        di.update({i: n for i, n in esc[g].items() if i in t})
    ba = Counter()
    for g in BAIDU:
        ba.update({i: n for i, n in esc[g].items() if i in t})
    paces = {g: pace(loops[g]) for g in ("placement", "whole_v1c", "whole_v1d")}
    security = [i for i, (_, q) in gov.items() if q == "SECURITY_INCIDENT"]
    return {
        "rule_arm_tickets": len(asked),
        "first_call_tickets": {g: len(m) for g, m in met.items()},
        "first_call_tickets_in_all": len(every),
        "shared": shared, "shared_in_all": len(in_all), "shared_under_v2b": len(v2b),
        "oncall": list(plan.ONCALL),
        "oncall_governing": [gov[i][0] for i in plan.ONCALL],
        "oncall_among_the_rule_arms": sorted(set(plan.ONCALL) & asked),
        "shared_by_queue": dict(Counter(gov[i][1] for i in in_all).most_common()),
        "security_tickets": len(security),
        "security_shared": len(set(security) & in_all),
        "deepinfra": {"tickets": len(di), "escalations": sum(di.values()),
                      "most_a_ticket": max(di.values())},
        "baidu": {"tickets": len(ba), "escalations": sum(ba.values())},
        "pace": {g: {k: v for k, v in x.items() if not k.startswith("_")}
                 for g, x in paces.items()},
        "attempts_at_the_budget": sum(paces[g]["_capped"] for g in ("placement",)),
    }


def not_back(got: dict[str, Any]) -> list[str]:
    """The figures §0 declared that did not come back."""
    return sorted(k for k, v in DECLARED.items() if got.get(k) != v)


# ---------------------------------------------------------------------------
# The references
# ---------------------------------------------------------------------------

def references_at(loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    """The closed answers at `T`, classed, ticket by ticket, and `HV-a`'s
    comparator."""
    t = set(plan.TICKETS)
    rule_arm: dict[int, list[str]] = {}
    for r in W.rule_arm_rows():
        if r["ticket"] in t:
            rule_arm.setdefault(r["ticket"], []).append(W.classed(r["ticket"], r.get("payload")))
    groups: dict[str, dict[int, list[str]]] = {}
    for g, runs in loops.items():
        by: dict[int, list[str]] = {}
        for _, rec in runs:
            for d in references.first_drafts(rec):
                if d["idx"] in t:
                    by.setdefault(d["idx"], []).append(d["class"])
        groups[g] = by
    pooled: dict[int, list[str]] = {}
    for g in DEEPINFRA:
        for i, cs in groups[g].items():
            pooled.setdefault(i, []).extend(cs)
    comparator = {i: {"answers": len(cs), "right_queue": sum(c not in W.RIGHT_OUT for c in cs),
                      "whole": sum(c == "whole" for c in cs)} for i, cs in sorted(pooled.items())}
    keyed = lambda d: {str(i): v for i, v in sorted(d.items())}   # noqa: E731
    return {"rule_arm": keyed(rule_arm), "loops": {g: keyed(by) for g, by in groups.items()},
            "hv_a_comparator": keyed(comparator)}


def sample_record(checks: gates.Checks, gate: dict) -> dict[str, Any]:
    loops = gates.loop_records()
    gov = governing()
    got = figures(loops, gov)
    return {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
            "provenance": PROVENANCE, "signature": gate, "gates": checks.summary(),
            "design": checks.design.summary(),
            "texts": prompts.texts(), "texts_sha16": prompts.digests(),
            "fingerprint": prompts.fingerprint(),
            "tickets": {str(i): {"governing": gov[i][0], "queue": gov[i][1]}
                        for i in plan.TICKETS},
            "references": references_at(loops),
            "figures": got, "figures_not_back": not_back(got)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_HALVES.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run HV-g1 to HV-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("halves/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    record = sample_record(checks, gate)
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\nfigures §0 declared that did not come back: "
          f"{record['figures_not_back'] or 'none'}")
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
