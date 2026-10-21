"""
Stage A of `PLAN_MANUAL.md`: the design and the references. **Free, and gated.**

It writes `results_manual/sample.json`:

  * `G-g1` to `G-g3`, the blocking checks, run first;
  * **the design**: the three texts and their digests, every prompt this plan
    sends by shape and level with its digest, and the order of Stage B (§2.5);
  * **the references, through this plan's instrument**: `PLAN_REUSE.md`'s three
    final bases on every cell §0 names, and the hidden policy written as an
    answer;
  * **§5.3's masses**: what each hidden rule decides on both surfaces, how the
    prose states it, and what each of `PLAN_REUSE.md`'s bases decides right of
    each rule's region. They are `G-g`'s reference columns.

Every figure here was seen while drafting (§0 of the plan says which). **The
gate binds this stage anyway**, because what it protects is the order of events:
a figure that informs a band must exist only after the signature, and these
acquire here the record that owns them.

    PYTHONHASHSEED=0 python3 -m manual.sample --dry-run   # the checks; writes nothing
    PYTHONHASHSEED=0 python3 -m manual.sample
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from harness.provenance import describe, environment

from overlap.rows import o_a

from . import compile as C
from . import gates, levels, plan, prompts
from . import instrument as I

# §5.3, as the plan states it. Stage A carries it so that G-g can read the
# masses by how the prose states each rule.
PROSE = {
    "H01": "exact", "H02": "vague", "H03": "vague", "H04": "exact", "H05": "exact",
    "H06": "exact", "H07": "exact", "H08": "exact", "H09": "exact", "H10": "vague",
    "H11": "vague", "H12": "exact", "H13": "vague", "H14": "vague", "H15": "vague",
    "H16": "exact", "H17": "vague", "H18": "exact", "H19": "ambiguous", "H20": "vague",
    "H21": "omitted", "H22": "exact", "H23": "exact", "H24": "vague", "H25": "omitted",
    "H26": "exact", "H27": "omitted", "H28": "merged", "H29": "merged",
}


def design() -> dict[str, Any]:
    return {
        "texts": {name: {"sha256": levels.digest(name), "text": levels.part(name)}
                  for name in levels.FILES},
        "levels": {lv: list(levels.PARTS[lv]) for lv in plan.LEVELS},
        "prompts": {shape: {lv: {"sha256": d,
                                 "text": (prompts.loop_system_prompt(lv) if shape == "loop"
                                          else prompts.compile_system_prompt(lv))}
                            for lv, d in by_level.items()}
                    for shape, by_level in prompts.prompt_digests().items()},
        "compile_user": prompts.COMPILE_USER,
        "order": {"seed": plan.ORDER_SEED,
                  "compile_smoke": plan.compile_schedule("smoke"),
                  "compile_session": plan.compile_schedule("session"),
                  "loop": plan.loop_schedule()},
    }


def cells(engine) -> dict[str, Any]:
    """Every cell §0 names, for one base."""
    keyword = ((1 << I.space().n) - 1) & ~I.outside()
    sp = I.over_space(engine)
    return {"space": sp, "space_outside": I.over_space(engine, I.outside()),
            "space_keyword": I.over_space(engine, keyword),
            "corpus": I.over_corpus(engine)}


def base_reading(engine, rules: list[dict]) -> dict[str, Any]:
    return {"cells": cells(engine), "k_a": str(I.k_a_exact(rules)),
            "o_a": o_a(rules, I.space()), "rules": len(rules),
            "reproduces": I.reproduces(engine), "by_region": I.by_region(engine)}


def references() -> dict[str, Any]:
    out: dict[str, Any] = {"plan_reuse": []}
    for k, rec in enumerate(I.reuse_records(), start=1):
        eng = I.final_engine(rec)
        row = base_reading(eng, rec["rules"])
        row["run"] = k
        row["prop"] = I.proposals(rec)
        out["plan_reuse"].append(row)
    hid = C.install(gates.hidden_answer(), I.space())
    out["hidden_policy"] = base_reading(hid.engine, [r.as_dict() for r in hid.rules])
    return out


def masses() -> dict[str, Any]:
    rows = []
    for rid, reg in I.hidden_regions().items():
        rows.append({"rule": rid, "queue": reg["queue"], "prose": PROSE[rid],
                     "space": reg["mask"].bit_count(), "corpus": len(reg["cases"])})
    by: dict[str, list[int]] = {}
    for r in rows:
        acc = by.setdefault(r["prose"], [0, 0, 0])
        acc[0] += 1
        acc[1] += r["space"]
        acc[2] += r["corpus"]
    return {"rules": rows,
            "by_how_the_prose_states_it": {k: {"rules": a, "space": b, "corpus": c}
                                           for k, (a, b, c) in by.items()}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Stage A of PLAN_MANUAL.md (free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run G-g1 to G-g3 and stop; writes nothing")
    args = ap.parse_args(argv)
    if args.dry_run:
        checks = gates.run_checks(suite=True)
        gates.report(checks)
        print("\ndry run: nothing written")
        return 0 if checks.blocking_pass else 1
    gate = plan.refuse_unsigned("manual/sample.py writes Stage A")
    checks = gates.run_checks(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    record = {"_env": environment(), "plan": str(plan.PLAN), "stage": "A",
              "signature": gate, "gates": checks.summary(), "design": design(),
              "references": references(), "masses": masses()}
    plan.sample_path().parent.mkdir(parents=True, exist_ok=True)
    plan.sample_path().write_text(json.dumps(record, indent=2, default=str))
    print(f"\n-> {plan.sample_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
