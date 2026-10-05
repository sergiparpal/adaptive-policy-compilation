"""
`Y-g1` to `Y-g4` of `PLAN_WHY.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  Y-g1  The inputs. The suite is green. The 1,600 record reproduces its own
        counts, by `primacy.gates.own_counts`. Stage D's own record is the
        1,600 record's development batch, row for row, `why` included. The
        truth lines up with the answers row by row, by
        `primacy.gates.truth_lines_up`.
  Y-g2  The split. The development set is Stage D's 400 answers and Stage C's
        170; the held-out set is the 1,200 answered the next day. The two
        batches share no pair. It counts the answers with a `why` in each part
        and reads none of the held-out ones.
  Y-g3  The codebook. Its fingerprint is the one §8 pins, and on the development
        set it reproduces every development figure §0 declares. **It never codes
        a held-out `why`**: this module builds rows from the development set
        only, and `tests/test_why.py` checks that by watching every sentence the
        codebook is handed during the checks.
  Y-g4  The signature (`why/plan.py`). It does not block a dry run, which writes
        nothing; it blocks every write.

**What a dry run prints is pass or fail and figures already declared**: the
counts the records publish and the development figures §0 states.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from primacy import gates as primacy_gates
from reuse.gates import run_suite

from . import codebook as cb
from . import plan
from . import rows as R


@dataclass
class Checks:
    yg1: dict
    yg2: dict
    yg3: dict
    yg4: dict
    src: dict = field(repr=False)
    hidden: dict = field(repr=False)
    sample: dict = field(repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.yg1["passes"] and self.yg2["passes"] and self.yg3["passes"]

    def summary(self) -> dict[str, Any]:
        return {"Y-g1": {k: self.yg1[k] for k in ("suite", "passes")},
                "Y-g2": {k: self.yg2[k] for k in ("parts", "shared_pairs", "passes")},
                "Y-g3": {k: self.yg3[k] for k in ("digest", "passes")},
                "Y-g4": self.yg4}


def load(path) -> dict:
    return json.loads(path.read_text())


def truth_by_index(sample: dict) -> dict[int, dict]:
    return {o["index"]: o for o in sample["oracle"]}


def part(src: dict, batch: str) -> list[dict]:
    return [r for r in src["answers"] if r["answer_from"] == batch]


# ---------------------------------------------------------------------------
# Y-g1
# ---------------------------------------------------------------------------

def stage_d_is_the_development_batch(src: dict, stage_d: dict) -> list[str]:
    own = {(r["rule_a"], r["rule_b"]): r for r in stage_d["answers"]}
    problems = []
    for r in part(src, plan.DEV_BATCH):
        o = own.get((r["rule_a"], r["rule_b"]))
        if o is None:
            problems.append(f"row {r['index']}: not in Stage D's record")
        elif any(r[k] != o[k] for k in ("a_shown_as", "declared", "answer",
                                        "question", "why")):
            problems.append(f"row {r['index']}: differs from Stage D's record")
        if len(problems) >= 5:
            break
    return problems


def gate_yg1(src, stage_d, sample, direction, suite: bool = True) -> dict:
    counts = primacy_gates.own_counts(src, stage_d)
    same = stage_d_is_the_development_batch(src, stage_d)
    truth = primacy_gates.truth_lines_up(src, sample, direction)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": ("the suite is green; the record reproduces its own counts; "
                     "Stage D's record is the development batch, why included; "
                     "the truth lines up"),
            "suite": tests, "own_counts": counts, "stage_d": same, "truth": truth,
            "passes": (not counts and not same and not truth
                       and tests["passes"] is not False)}


# ---------------------------------------------------------------------------
# Y-g2
# ---------------------------------------------------------------------------

def gate_yg2(src: dict, hidden: dict) -> dict:
    dev, test = part(src, plan.DEV_BATCH), part(src, plan.TEST_BATCH)
    shared = ({(r["rule_a"], r["rule_b"]) for r in dev}
              & {(r["rule_a"], r["rule_b"]) for r in test})

    def with_why(rows):
        return sum(1 for r in rows if r["declared"] != "none" and r.get("why"))
    parts = {
        "development_stage_d": {"answers": len(dev), "declared_with_a_why": with_why(dev)},
        "development_stage_c": {"answers": len(hidden["answers"]),
                                "two_way_with_a_why": sum(
                                    1 for r in hidden["answers"]
                                    if r["outcome"] in ("correct", "wrong") and r.get("why"))},
        "held_out": {"answers": len(test), "declared_with_a_why": with_why(test)},
    }
    passes = (len(dev) == plan.N_DEV_ANSWERS and len(test) == plan.N_TEST_ANSWERS
              and len(hidden["answers"]) == plan.N_HIDDEN and not shared
              and len(dev) + len(test) == len(src["answers"]))
    return {"what": ("the development batch and the held-out batch partition the "
                     "1,600 answers and share no pair"),
            "parts": parts, "shared_pairs": len(shared), "passes": passes}


# ---------------------------------------------------------------------------
# Y-g3
# ---------------------------------------------------------------------------

def development_figures(rows: list[dict]) -> dict:
    """The shape of `plan.DEV`, measured."""
    c, s = R.census(rows), R.section_0(rows)

    def hn(x):
        return (x["hits"], x["n"])
    return {"n": c["n"], "codes": c["codes"],
            "Y-a": hn(s["Y-a"]), "Y-b": hn(s["Y-b"]),
            "Y-c": (hn(s["Y-c"]["first"]), hn(s["Y-c"]["second"])),
            "Y-d": (hn(s["Y-d"]["first"]), hn(s["Y-d"]["second"]))}


def development_rows(src: dict, hidden: dict, sample: dict) -> dict[str, list[dict]]:
    """The development set's rows, and only them."""
    truth = truth_by_index(sample)
    return {"stage_d": R.learned_rows(part(src, plan.DEV_BATCH), truth,
                                      lambda r: plan.DEV_BATCH),
            "stage_c": R.hidden_rows(hidden["answers"])}


def gate_yg3(src: dict, hidden: dict, sample: dict) -> dict:
    digest = cb.digest()
    rows = development_rows(src, hidden, sample)
    got = {k: development_figures(v) for k, v in rows.items()}
    want = {k: {kk: (tuple(map(tuple, vv)) if kk in ("Y-c", "Y-d") else
                     tuple(vv) if kk in ("Y-a", "Y-b") else vv)
                for kk, vv in v.items()} for k, v in plan.DEV.items()}
    mismatches = [f"{k}.{kk}: measured {got[k][kk]}, declared {want[k][kk]}"
                  for k in want for kk in want[k] if got[k][kk] != want[k][kk]]
    return {"what": ("the codebook is the one §8 pins, and on the development set it "
                     "reproduces every development figure §0 declares"),
            "digest": {"measured": digest, "pinned": plan.CODEBOOK_DIGEST},
            "development": got, "mismatches": mismatches,
            "passes": digest == plan.CODEBOOK_DIGEST and not mismatches}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_all(suite: bool = True) -> Checks:
    src, stage_d, hidden = load(plan.SOURCE), load(plan.STAGE_D), load(plan.HIDDEN)
    sample, direction = load(plan.SAMPLE), load(plan.DIRECTION)
    return Checks(yg1=gate_yg1(src, stage_d, sample, direction, suite=suite),
                  yg2=gate_yg2(src, hidden),
                  yg3=gate_yg3(src, hidden, sample),
                  yg4=plan.gate_signature(),
                  src=src, hidden=hidden, sample=sample)


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    g = c.yg1
    t = g["suite"]
    print(f"  Y-g1  {mark[g['passes']]}  test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    for name, probs in (("the record reproduces its own counts", g["own_counts"]),
                        ("Stage D's record is the development batch", g["stage_d"]),
                        ("the truth lines up row by row", g["truth"])):
        print(f"              {name}: " + ("yes" if not probs else "; ".join(probs)))
    g = c.yg2
    print(f"  Y-g2  {mark[g['passes']]}  the split, {g['shared_pairs']} pair(s) shared:")
    for k, v in g["parts"].items():
        print(f"                {k}: {v}")
    g = c.yg3
    print(f"  Y-g3  {mark[g['passes']]}  codebook {g['digest']['measured']} "
          f"(pinned {g['digest']['pinned']})")
    for k, v in g["development"].items():
        print(f"                {k}: {v}")
    for m in g["mismatches"]:
        print(f"                MISMATCH {m}")
    s = c.yg4
    print(f"  Y-g4  {'SIGNED' if s['passes'] else 'UNSIGNED'}  {s['found']} "
          f"signature line(s), {s['unsigned']} blank"
          + ("" if s["passes"] else " — nothing may be scored or written"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")
