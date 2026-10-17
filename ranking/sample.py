"""
Stage A of `PLAN_RANKING.md`: the questions and the free readout. Zero API
calls.

It refuses while the plan is unsigned, before it measures, builds or writes
anything (§10). Then it runs `M-g1` to `M-g3`, all blocking, and only after both
does it compute the one thing that makes this stage worth gating: **what the
model's revealed ranking scores as a lookup**, on every cell. No record computes
it. `FINDINGS3.md` §14 attributes 0.4824 to it, and that figure is Stage C's
hierarchy's (`rung3/edge_dropping.py`, `QUEUE_RANKING_REFERENCE`, "stage_c row").
Its value is the closest thing to `M-b`'s answer that exists without paying,
which is why nobody computes it before §0 is signed.

WHAT IT WRITES (§7), to `results_ranking/sample.json`:

  presentations  the twelve, with their digests; the order of each pass; the
                 smoke run's two; the system prompt and its digest
  lines          §0's five: three read from the records that own them, two the
                 claims' own edges
  revealed       the revealed ranking of the learned base — `edge_dropping.py`'s
                 Copeland over the 1,479 declared answers, recomputed — and the
                 same Copeland over the hidden policy's 166 two-way answers;
                 each with its queue pairs, what it predicts of its own answers,
                 its readings on `K-b`'s pairs, and its scores on every cell
  stage_c        what Stage C's ranking predicts of both sets of answers, which
                 is `M-d`'s baseline, beside its published scores and readings
  references     the born_at floor and the family's best, mean and worst on
                 every cell, from `M-g1`'s measurement of the record

    python3 -m ranking.sample --dry-run              # M-g1..M-g4; writes nothing
    PYTHONHASHSEED=0 python3 -m ranking.sample       # refuses while unsigned
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from . import gates
from . import instrument as I
from . import plan, question


def lines() -> dict[str, Any]:
    out = plan.signed_lines()
    out["M-a"] = {"validity": plan.MIN_VALID_SHARE, "slot_gap": plan.M_A_MAX_SLOT_GAP,
                  "source": "the claim's own edges, §0",
                  "holds_when": "validity >= 0.90 and W - A <= 0.05"}
    out["M-d"] = {"line": plan.M_D_MIN_GAP, "source": "the claim's own edge, §0",
                  "holds_when": "median >= line"}
    return out


def design() -> dict[str, Any]:
    pres = question.presentations()
    return {
        "presentations": [{"pid": p.pid, "order": list(p.order), "digest": p.digest}
                          for p in pres],
        "passes": question.pass_orders(pres),
        "smoke": question.smoke_order(pres),
        "system_prompt": question.SYSTEM_PROMPT,
        "system_prompt_sha256": hashlib.sha256(
            question.SYSTEM_PROMPT.encode()).hexdigest(),
    }


def ranking_block(inst: I.Instrument, order: list[str], answers: dict[str, list],
                  er: list[list[dict]]) -> dict[str, Any]:
    """Everything a ranking is read for, beside every ask's in Stage C."""
    return {
        "order": list(order),
        "predicts": {name: list(I.predicts(order, a)) for name, a in answers.items()},
        "k_b_pairs": {key: I.blind_reading(order, er, key)
                      for key in ("space_out", "corpus_out")},
        "scores": I.scores(inst, order),
    }


def readout(checks: gates.Checks) -> dict[str, Any]:
    inst = checks.instrument
    la, ha = I.learned_answers(), I.hidden_answers()
    answers = {"learned": la, "hidden": ha}
    er = I.blind_edge_rows()
    learned_order, learned_copeland = I.revealed_learned()
    hidden_order, hidden_copeland = I.revealed_of(ha)
    refs = {}
    for r in checks.mg1["rows"]:
        if r["tiebreak"] == "born_at":
            refs[I.cell_name(r["pool"], r["surface"])] = {
                k: r[k] for k in ("born_at", "best", "mean", "median", "sd", "worst",
                                  "stage_c")}
    return {
        "revealed": {
            "learned": {**ranking_block(inst, learned_order, answers, er),
                        "copeland": learned_copeland,
                        "derived_from": f"{plan.PAIRWISE_LEARNED}: the {len(la)} "
                                        "declared answers, by rung3.edge_dropping."
                                        "revealed_ranking",
                        "by_queue_pair": I.by_queue_pair(la)},
            "hidden": {**ranking_block(inst, hidden_order, answers, er),
                       "copeland": hidden_copeland,
                       "derived_from": f"{plan.PAIRWISE_HIDDEN}: the {len(ha)} "
                                       "two-way answers, by the same Copeland",
                       "by_queue_pair": I.by_queue_pair(ha)},
        },
        "stage_c": {**ranking_block(inst, list(I.STAGE_C), answers, er),
                    "fitted_on": "the hidden policy's 170 pairs, with their answer key"},
        "declarations": {key: I.blind_reading(None, er, key)
                         for key in ("space_out", "corpus_out")},
        "references": refs,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_RANKING.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run M-g1 to M-g4 and stop; writes nothing")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_checks(suite=True, progress=True)
        gates.report(checks)
        print("\ndry run: nothing measured beyond the checks, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"ranking/sample.py writes {plan.SAMPLE_PATH}")
    checks = gates.run_checks(suite=True, progress=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")

    record = {
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "A",
        "gates": checks.summary(),
        **design(),
        "lines": lines(),
        **readout(checks),
    }
    plan.OUT.mkdir(exist_ok=True)
    plan.SAMPLE_PATH.write_text(json.dumps(record, indent=2, default=str))
    print(f"\n-> {plan.SAMPLE_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
