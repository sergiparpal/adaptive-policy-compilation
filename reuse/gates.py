"""
`U-g1` to `U-g4` of `PLAN_REUSE.md` §6 — the blocking checks, all free.

They run before any record of the plan is written and before any call is made,
and **any failure stops the plan before a figure exists**. Both of the last two
plans had their declared method killed by a check like these; running them
first is how a design error becomes a fix to the draft instead of a signed
amendment.

  U-g1  STOP 0 for this engine, again: the hybrid engine executes the hidden
        policy — 1.0000, no silent error, no CONFLICT, no IMPASSE — on the
        corpus and on the exhaustive space, measured in memory with
        `rung2.ceiling_check2_space.measure` so that no published record is
        rewritten; and the test suite is green.
  U-g2  The eight n=100 records reproduce themselves: their published metrics
        and each rule's fire counts recompute from their own cases, every rule
        has one birth escalation (§5.3), and the corpus redrawn at each seed is
        labelled the same way case by case — read off the frozen loop's records,
        so no module of the plan imports the oracle.
  U-g3  The `keep_k` frontier does not depend on the engine (`reuse/frontier.py`).
  U-g4  The signature (`reuse/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write and every call.

**What a dry run prints is pass or fail and figures that are already
published** — the engine's 1.0000, counts of records that reproduce. It never
prints anything Stage A would report: those figures wait for the signature.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from harness.ceiling_check import all_cases
from harness.domain import generate_corpus
from harness.shadow import RunResult

from rung2.ceiling_check2_space import measure
from rung2.engine2 import Space
from rung2.hidden_priority import build_hidden_engine

from . import analysis, frontier, plan


@dataclass
class Checks:
    ug1: dict
    ug2: dict
    ug3: dict
    ug4: dict
    runs_n: dict[int, RunResult] = field(repr=False)
    runs_100: dict[int, dict[int, RunResult]] = field(repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.ug1["passes"] and self.ug2["passes"] and self.ug3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"U-g1": self.ug1, "U-g2": {"passes": self.ug2["passes"],
                                          "records": len(self.ug2["rows"])},
                "U-g3": self.ug3, "U-g4": self.ug4}


# ---------------------------------------------------------------------------
# U-g1
# ---------------------------------------------------------------------------

def run_suite() -> dict[str, Any]:
    t0 = time.time()
    p = subprocess.run([sys.executable, "-m", "unittest", "discover"],
                       capture_output=True, text=True)
    ran = re.search(r"Ran (\d+) tests?", p.stderr)
    lines = [l for l in p.stderr.strip().splitlines() if l.strip()]
    return {"ran": True, "tests": int(ran.group(1)) if ran else None,
            "result": lines[-1] if lines else "",
            "seconds": round(time.time() - t0, 1), "passes": p.returncode == 0}


def gate_ug1(suite: bool = True) -> dict[str, Any]:
    engine, _, _ = build_hidden_engine(Space())
    surfaces = {}
    for name, cases in (("corpus", generate_corpus(plan.N, seed=plan.SEED)),
                        ("space", list(all_cases()))):
        m = measure(engine, cases, name, "hybrid")
        surfaces[name] = {
            "e2e": m["accuracy_end_to_end"], "silent_errors": m["silent_errors_abs"],
            "conflict": m["conflict"], "impasse": m["impasse"],
            "passes": (m["accuracy_end_to_end"] == 1.0 and m["silent_errors_abs"] == 0
                       and m["conflict"] == 0 and m["impasse"] == 0),
        }
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {
        "what": "the hidden policy executed at 1.0000 on corpus and space; the suite green",
        "surfaces": surfaces,
        "suite": tests,
        "passes": all(s["passes"] for s in surfaces.values())
                  and tests["passes"] is not False,
    }


# ---------------------------------------------------------------------------
# U-g2
# ---------------------------------------------------------------------------

def check_record(rec: dict, *, n: int, seed: int, prompt: str,
                 truth: list[tuple[str, str]]) -> list[str]:
    """Every way a shadow-loop record fails to reproduce itself. Stage C runs
    the same function over the records Stage B writes (§5.3)."""
    problems = []
    if rec.get("n") != n or rec.get("seed") != seed:
        problems.append(f"n={rec.get('n')}, seed={rec.get('seed')}: "
                        f"expected n={n}, seed={seed}")
    if rec.get("prompt_version", prompt) != prompt:
        problems.append(f"prompt {rec.get('prompt_version')}: expected {prompt}")
    problems += analysis.metric_mismatches(rec)
    problems += analysis.fire_mismatches(rec)
    problems += analysis.births(rec)[1]
    labels = [(r["truth"], r["truth_rule"]) for r in rec["records"]]
    if labels != truth:
        first = next((i for i, (a, b) in enumerate(zip(labels, truth)) if a != b),
                     min(len(labels), len(truth)))
        problems.append(f"the corpus redrawn at seed {seed} is labelled "
                        f"differently from case {first} on")
    return problems


def gate_ug2(runs_100: dict[int, dict[int, RunResult]]) -> dict[str, Any]:
    rows = []
    for prompt, seed, path in plan.EIGHT:
        rec = json.loads(path.read_text())
        problems = check_record(rec, n=plan.N_EIGHT, seed=seed, prompt=prompt,
                                truth=frontier.truth_sequence(runs_100[seed][1]))
        rows.append({"record": str(path), "prompt": prompt, "seed": seed,
                     "problems": problems, "passes": not problems})
    return {"what": "the eight n=100 records reproduce their own published "
                    "metrics, fire counts, births and corpus",
            "rows": rows, "passes": all(r["passes"] for r in rows)}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_all(suite: bool = True) -> Checks:
    runs_n = frontier.keep_k_runs(plan.N, plan.SEED)
    runs_100 = {s: frontier.keep_k_runs(plan.N_EIGHT, s) for s in plan.EIGHT_SEEDS}
    return Checks(ug1=gate_ug1(suite=suite), ug2=gate_ug2(runs_100),
                  ug3=frontier.gate_ug3(runs_n, runs_100),
                  ug4=plan.gate_signature(), runs_n=runs_n, runs_100=runs_100)


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    s = c.ug1["surfaces"]
    print(f"  U-g1  {mark[c.ug1['passes']]}  hybrid engine, hidden policy: "
          f"corpus e2e {s['corpus']['e2e']:.4f}, space e2e {s['space']['e2e']:.4f}, "
          f"silent {s['corpus']['silent_errors'] + s['space']['silent_errors']}, "
          f"CONFLICT {s['corpus']['conflict'] + s['space']['conflict']}, "
          f"IMPASSE {s['corpus']['impasse'] + s['space']['impasse']}")
    t = c.ug1["suite"]
    print(f"              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    ok = sum(1 for r in c.ug2["rows"] if r["passes"])
    print(f"  U-g2  {mark[c.ug2['passes']]}  the eight n=100 records reproduce "
          f"themselves: {ok} of {len(c.ug2['rows'])}")
    for r in c.ug2["rows"]:
        for p in r["problems"][:5]:
            print(f"              {r['record']}: {p}")
    print(f"  U-g3  {mark[c.ug3['passes']]}  keep_k reproduces results/frontier.json: "
          f"{c.ug3['reproduces_published']}; most rules matching one case: "
          f"{c.ug3['most_rules_matching_one_case']}")
    g = c.ug4
    print(f"  U-g4  {'SIGNED' if g['passes'] else 'UNSIGNED'}  {g['found']} "
          f"signature line(s), {g['unsigned']} blank"
          + ("" if g["passes"] else " — nothing may be written or spent"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")
