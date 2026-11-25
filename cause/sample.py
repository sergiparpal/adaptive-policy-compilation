"""
Stage A of `PLAN_CAUSE.md`: the design and the references. Free, and gated: it
writes nothing while the plan is unsigned, because a reference written before
the signature would be a figure that existed before its band (§10 of the plan).

WHAT IT WRITES, `results_cause/sample.json`:

  - **the design**: the 136 tickets, every ask with its digest, and the four
    sessions in their orders; the texts, their digests and the fingerprint;
  - **each ticket's governing rule and its queue**, the first rule of level 3's
    list whose region holds the ticket, read over the space through
    `halves.sample.governing`, called;
  - **the references**, ticket by ticket:
    - `PLAN_HALVES.md`'s arms `e` and `v`, every answer of its two passes and its
      rarest queue's session, valid as that plan's §0 reads it, classed as its
      Stage C classed it and coded by `halves/hidden.py`'s codebook;
    - `CA-a`'s comparator: that plan's `v` over its two passes, by ticket;
    - the causes the reasoning loops met at each ticket, by loop group;
  - **§0's three figures, recomputed**, and which of them did not come back as
    §0 declares them.

It reads the closed records and level 3's list, and asks nothing.

    python3 -m cause.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m cause.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any

from harness.provenance import describe, environment

from halves import hidden as hhidden
from halves import sample as hsample
from halves import score as hscore
from whole import paragraph as W

from . import gates, plan, prompts

PROVENANCE = ("Stage A of PLAN_CAUSE.md, written after §0 was signed. Its three figures were "
              "computed while drafting, from the records as main held them at f0c7c29, and "
              "seen before §0's lines were drawn. Its references, PLAN_HALVES.md's answers "
              "classed and coded ticket by ticket, were not.")

# §0's figures as the plan declares them, which `not_back` holds the record to.
DECLARED = {
    "tickets": 136,
    "oncall": list(plan.ONCALL),
    "oncall_governing": ["H05", "H05", "H04", "H04", "H04", "H05", "H04"],
    "runs": {"reasoned_loop": 6, "channel": 6, "placement": 6, "whole_v1c": 3, "whole_v1d": 3},
    "escalations_at_T": {
        "reasoned_loop": {"IMPASSE": 135, "CONFLICT": 1, "ERROR": 112},
        "channel": {"IMPASSE": 134, "CONFLICT": 7, "ERROR": 134},
        "placement": {"IMPASSE": 149, "CONFLICT": 6, "ERROR": 109},
        "whole_v1c": {"IMPASSE": 86, "CONFLICT": 6, "ERROR": 49},
        "whole_v1d": {"IMPASSE": 47, "CONFLICT": 4, "ERROR": 54},
    },
    "tickets_by_cause": {"escalated": 136, "IMPASSE": 63, "ERROR": 108, "CONFLICT": 17},
    "tickets_by_cause_deepinfra": {"escalated": 105, "IMPASSE": 54, "ERROR": 63,
                                   "CONFLICT": 12},
    "deepinfra_cause_sets": {"IMPASSE": 38, "ERROR": 39, "ERROR+IMPASSE": 16,
                             "CONFLICT+ERROR": 8, "CONFLICT": 4},
    "oncall_causes": {"257": {"ERROR": 11}, "710": {"CONFLICT": 1, "ERROR": 8},
                      "954": {"CONFLICT": 1, "ERROR": 11}, "982": {"ERROR": 3},
                      "1432": {"ERROR": 12}, "1783": {"ERROR": 1}, "1951": {"ERROR": 16}},
}
CAUSES = ("IMPASSE", "CONFLICT", "ERROR")


# ---------------------------------------------------------------------------
# §0's figures
# ---------------------------------------------------------------------------

def causes_by_group(loops: dict[str, list[tuple[str, dict]]]) -> dict[str, dict[int, Counter]]:
    """By loop group and ticket of `T`, the causes of its escalations."""
    return {g: gates.causes_at({g: runs}, plan.TICKETS) for g, runs in loops.items()}


def pooled(by_group: dict[str, dict[int, Counter]], groups) -> dict[int, Counter]:
    out: dict[int, Counter] = {t: Counter() for t in plan.TICKETS}
    for g in groups:
        for t, c in by_group[g].items():
            out[t].update(c)
    return out


def figures(loops: dict[str, list[tuple[str, dict]]],
            gov: dict[int, tuple[str, str]]) -> dict[str, Any]:
    """§0's three figures, from the closed records. None reads an answer's class."""
    by_group = causes_by_group(loops)
    every = pooled(by_group, loops)
    di = pooled(by_group, plan.DEEPINFRA_GROUPS)

    def by_cause(c: dict[int, Counter]) -> dict[str, int]:
        return {"escalated": sum(1 for t in plan.TICKETS if c[t]),
                **{k: sum(1 for t in plan.TICKETS if c[t][k]) for k in CAUSES}}

    sets = Counter("+".join(sorted(c)) for c in di.values() if c)
    return {
        "tickets": len(plan.TICKETS),
        "oncall": list(plan.ONCALL),
        "oncall_governing": [gov[i][0] for i in plan.ONCALL],
        "runs": {g: len(runs) for g, runs in loops.items()},
        "escalations_at_T": {g: {k: sum(c[t][k] for t in plan.TICKETS) for k in CAUSES}
                             for g, c in by_group.items()},
        "tickets_by_cause": by_cause(every),
        "tickets_by_cause_deepinfra": by_cause(di),
        "deepinfra_cause_sets": dict(sets),
        "oncall_causes": {str(t): dict(sorted(every[t].items())) for t in plan.ONCALL},
    }


def not_back(got: dict[str, Any]) -> list[str]:
    """The figures §0 declared that did not come back."""
    return sorted(k for k, v in DECLARED.items() if got.get(k) != v)


# ---------------------------------------------------------------------------
# The references
# ---------------------------------------------------------------------------

def halves_answers(sessions: dict[str, dict]) -> dict[str, dict[str, list[dict]]]:
    """`PLAN_HALVES.md`'s `e` and `v` at `T`, by arm and ticket: every answer, valid
    as that plan's §0 reads it, its class, and the codebook's codes when it names
    the right queue and a valid rule."""
    out: dict[str, dict[str, list[dict]]] = {a: {} for a in gates.OURS}
    for r in hscore.classed_rows(sessions):
        if r["arm"] not in gates.OURS:
            continue
        codes = None
        if r["valid"] and r["class"] not in W.RIGHT_OUT:
            payload = r.get("payload") or {}
            codes = hhidden.codes(r.get("reasoning"), str(payload.get("note") or ""))
        out[r["arm"]].setdefault(str(r["ticket"]), []).append(
            {"session": r["session"], "valid": r["valid"], "class": r["class"], "codes": codes})
    return {a: dict(sorted(by.items(), key=lambda x: int(x[0]))) for a, by in out.items()}


def comparator(answers: dict[str, list[dict]]) -> dict[str, dict[str, int]]:
    """`CA-a`'s: `PLAN_HALVES.md`'s `v` at each ticket, over its two passes."""
    out = {}
    for t, xs in answers.items():
        passes = [x for x in xs if x["session"] in plan.PASSES and x["valid"]]
        right = [x for x in passes if x["class"] not in W.RIGHT_OUT]
        out[t] = {"answers": len(passes), "right_queue": len(right),
                  "whole": sum(1 for x in right if x["class"] == "whole")}
    return out


def references_at(sessions: dict[str, dict],
                  loops: dict[str, list[tuple[str, dict]]]) -> dict[str, Any]:
    answers = halves_answers(sessions)
    by_group = causes_by_group(loops)
    causes = {str(t): {g: dict(sorted(by_group[g][t].items())) for g in loops
                       if by_group[g][t]} for t in plan.TICKETS}
    return {"halves": answers, "ca_a_comparator": comparator(answers[prompts.V2B]),
            "causes": causes}


def sample_record(checks: gates.Checks, gate: dict) -> dict[str, Any]:
    _, sessions = gates.halves_records()
    loops = gates.loop_records()
    gov = hsample.governing()
    got = figures(loops, gov)
    return {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
            "provenance": PROVENANCE, "signature": gate, "gates": checks.summary(),
            "design": checks.design.summary(),
            "texts": prompts.texts(), "texts_sha16": prompts.digests(),
            "fingerprint": prompts.fingerprint(),
            "tickets": {str(i): {"governing": gov[i][0], "queue": gov[i][1]}
                        for i in plan.TICKETS},
            "references": references_at(sessions, loops),
            "figures": got, "figures_not_back": not_back(got)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_CAUSE.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run CA-g1 to CA-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1

    gate = plan.refuse_unsigned("cause/sample.py writes Stage A")
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
