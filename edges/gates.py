"""
`W-g1` to `W-g4` of `PLAN_EDGES.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  W-g1  The inputs. The suite is green. The hybrid engine executes the hidden
        policy at 1.0000 on the corpus and on the space, measured in memory with
        `reuse.gates.gate_ug1`, so no published record is rewritten. Each Stage
        B record reproduces its own metrics, fire counts, births and corpus
        labels, by `fidelity.sample.gate_fg1`. The space labels partition the
        134,400 points and give `T2_TECHNICAL` its published 36,720.
  W-g2  The rebuild, with and without the edges. With them, each run rebuilds
        exactly, by `fidelity.replay.check`. Without them, every departure is an
        ACTION that becomes a CONFLICT, which is §5.2's premise and `D`'s.
  W-g3  The counterfactual rebuild (`edges/rebuild.py`) is the identity where it
        should be. Given the declared directions, it decides every case as the
        record did and tries every edge to its logged verdict, and every edge
        accepted is either installed or consistent with subsumption. Given no
        installed edge, it decides every case as `W-g2`'s rebuild without edges
        does. And the coin's first draws decide `D` identically under three
        values of `PYTHONHASHSEED`, while a witness that does depend on the hash
        changes between them.
  W-g4  The signature (`edges/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures that are already
published**: the engine's 1.0000, counts of records that reproduce, the
departures `FINDINGS_FIDELITY.md` publishes and the 36,720. It computes no
figure from the labels of `D`.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

from harness.domain import generate_corpus
from rung2.engine2 import Space
from rung3.order_search_ls import space_truth_masks

from fidelity import replay
from fidelity import sample as fidelity_sample
from reuse import gates as reuse_gates

from . import plan
from . import rebuild as rb


@dataclass
class Checks:
    wg1: dict
    wg2: dict
    wg3: dict
    wg4: dict
    runs: dict[int, dict] = field(repr=False)
    corpus: list = field(repr=False)
    space: Space = field(repr=False)
    declared: dict[int, rb.Rebuild] = field(repr=False)       # declared directions
    without: dict[int, dict[int, rb.Decision]] = field(repr=False)   # W-g2's rebuild
    d: dict[int, list[int]] = field(repr=False)               # D_r
    classes: dict[int, dict[int, str]] = field(repr=False)    # each edge's class

    @property
    def blocking_pass(self) -> bool:
        return self.wg1["passes"] and self.wg2["passes"] and self.wg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"W-g1": {k: self.wg1[k] for k in ("ceilings", "suite", "space_labels",
                                                  "passes")},
                "W-g2": {"departures": {r: v["departures"]
                                        for r, v in self.wg2["runs"].items()},
                         "passes": self.wg2["passes"]},
                "W-g3": {"runs": {r: v["passes"] for r, v in self.wg3["runs"].items()},
                         "hash_seeds": self.wg3["hash_seeds"],
                         "passes": self.wg3["passes"]},
                "W-g4": self.wg4}


# ---------------------------------------------------------------------------
# W-g1
# ---------------------------------------------------------------------------

def space_labels(space: Space) -> dict[str, Any]:
    """The labels `W-b` reads, through the one module allowed to compute them:
    they must partition the space, and give `T2_TECHNICAL` its published
    size."""
    tmask = space_truth_masks(space)
    union = 0
    total = 0
    for m in tmask.values():
        union |= m
        total += m.bit_count()
    t2 = tmask.get(plan.T2, 0).bit_count()
    return {"points": space.n, "t2_points": t2,
            "passes": (space.n == plan.SPACE_POINTS and union == space.full
                       and total == space.n and t2 == plan.T2_SPACE_POINTS)}


def gate_wg1(runs: dict[int, dict], corpus, space: Space,
             suite: bool = True) -> dict[str, Any]:
    ug1 = reuse_gates.gate_ug1(suite=suite)
    fg1 = fidelity_sample.gate_fg1(runs, fidelity_sample.truth_labels(corpus),
                                   suite=False)
    labels = space_labels(space)
    return {
        "what": ("the suite is green; the hidden policy executed at 1.0000 on "
                 "corpus and space; each Stage B record reproduces itself; the "
                 "space labels partition the space"),
        "ceilings": ug1["surfaces"],
        "suite": ug1["suite"],
        "records": fg1["records"],
        "space_labels": labels,
        "passes": ug1["passes"] and fg1["passes"] and labels["passes"],
    }


# ---------------------------------------------------------------------------
# W-g2
# ---------------------------------------------------------------------------

def gate_wg2(runs: dict[int, dict], corpus, space: Space):
    rows, without, d = {}, {}, {}
    for k, rec in runs.items():
        exact = replay.check(rec, corpus, space)
        none = rb.replay_without_edges(rec, corpus, space)
        dk, kinds = rb.edge_decided(rec, none)
        only_that_kind = set(kinds) <= {"action_to_conflict"}
        rows[f"run{k}"] = {
            "replay_exact": exact["passes"],
            "first_problems": exact["first_problems"][:5],
            "departures": kinds,
            "passes": exact["passes"] and only_that_kind,
        }
        without[k], d[k] = none, dk
    return ({"what": ("each run rebuilds exactly with its edges; without them "
                      "every departure is an ACTION that becomes a CONFLICT"),
             "runs": rows, "passes": all(r["passes"] for r in rows.values())},
            without, d)


# ---------------------------------------------------------------------------
# W-g3
# ---------------------------------------------------------------------------

def identity_problems(rec: dict, declared: rb.Rebuild, classes: dict[int, str],
                      none: rb.Rebuild, without: dict[int, rb.Decision]) -> list[str]:
    problems = []
    for row in rec["records"]:
        got = declared.decisions[row["idx"]]
        want = (row["outcome"], row["winner_id"], row["n_matched"])
        if (got.outcome, got.winner_id, got.n_matched) != want:
            problems.append(f"case {row['idx']}: rebuilt {got[:2]}, recorded {want[:2]}")
        elif row["outcome"] == "ACTION" and got.action != row["predicted"]:
            problems.append(f"case {row['idx']}: rebuilt action {got.action}, "
                            f"recorded {row['predicted']}")
    for e in rb.all_edges(rec):
        if declared.tried.get(e.key) != e.verdict:
            problems.append(f"edge {e.key}: tried {declared.tried.get(e.key)}, "
                            f"logged {e.verdict}")
    duplicates = sum(1 for c in classes.values() if c == "duplicate")
    if duplicates:
        problems.append(f"{duplicates} accepted edge(s) over a pair already installed")
    departing = [i for i, dec in none.decisions.items() if dec != without[i]]
    if departing:
        problems.append(f"without its installed edges the rebuild departs from "
                        f"W-g2's on {len(departing)} cases, the first {departing[0]}")
    return problems


def fingerprints() -> dict[str, Any]:
    """`tests/hashseed_child.py`'s method: a child per hash seed, compared."""
    rows = {}
    for s in plan.FINGERPRINT_SEEDS:
        p = subprocess.run([sys.executable, "-m", "edges.rebuild", "--fingerprint"],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONHASHSEED": s})
        lines = p.stdout.strip().splitlines()
        rows[s] = (json.loads(lines[-1]) if p.returncode == 0 and lines
                   else {"error": p.stderr.strip()[-300:]})
    failed = [s for s, r in rows.items() if "error" in r]
    draws = {r.get("draws") for r in rows.values()}
    witness = {r.get("witness") for r in rows.values()}
    return {"seeds": list(rows), "failed": failed,
            "draws_identical": not failed and len(draws) == 1,
            "witness_varies": not failed and len(witness) == len(rows),
            "passes": not failed and len(draws) == 1 and len(witness) == len(rows)}


def gate_wg3(runs: dict[int, dict], corpus, space: Space,
             without: dict[int, dict[int, rb.Decision]], seeds: bool = True):
    rows, declared, classes = {}, {}, {}
    for k, rec in runs.items():
        dec = rb.rebuild(rec, corpus, space)
        cls = rb.classify(rec, dec)
        none = rb.rebuild(rec, corpus, space,
                          directions=rb.without_installed(dec.installed))
        problems = identity_problems(rec, dec, cls, none, without[k])
        rows[f"run{k}"] = {"problems": problems[:5], "passes": not problems}
        declared[k], classes[k] = dec, cls
    hs = fingerprints() if seeds else {"passes": None}
    return ({"what": ("given the declared directions the rebuild is the record; "
                      "given none it is W-g2's rebuild; the coin does not depend "
                      "on the hash seed"),
             "runs": rows, "hash_seeds": hs,
             "passes": all(r["passes"] for r in rows.values())
                       and hs["passes"] is not False},
            declared, classes)


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_all(suite: bool = True, seeds: bool = True) -> Checks:
    runs = rb.load_runs()
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    wg1 = gate_wg1(runs, corpus, space, suite=suite)
    wg2, without, d = gate_wg2(runs, corpus, space)
    wg3, declared, classes = gate_wg3(runs, corpus, space, without, seeds=seeds)
    return Checks(wg1=wg1, wg2=wg2, wg3=wg3, wg4=plan.gate_signature(),
                  runs=runs, corpus=corpus, space=space, declared=declared,
                  without=without, d=d, classes=classes)


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    s = c.wg1["ceilings"]
    print(f"  W-g1  {mark[c.wg1['passes']]}  hybrid engine, hidden policy: "
          f"corpus e2e {s['corpus']['e2e']:.4f}, space e2e {s['space']['e2e']:.4f}")
    t = c.wg1["suite"]
    print("              test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    ok = sum(1 for r in c.wg1["records"].values() if r["passes"])
    print(f"              Stage B records reproduce themselves: {ok} of "
          f"{len(c.wg1['records'])}")
    for name, r in c.wg1["records"].items():
        for p in r["problems"][:3]:
            print(f"                {name}: {p}")
    lab = c.wg1["space_labels"]
    print(f"              space labels partition {lab['points']:,} points; "
          f"{plan.T2} {lab['t2_points']:,}")
    print(f"  W-g2  {mark[c.wg2['passes']]}  rebuilt with edges, exact: "
          f"{sum(1 for r in c.wg2['runs'].values() if r['replay_exact'])} of "
          f"{len(c.wg2['runs'])}; without them, departures by kind:")
    for name, r in c.wg2["runs"].items():
        print(f"                {name}: {r['departures']}")
        for p in r["first_problems"][:3]:
            print(f"                {name}: {p}")
    print(f"  W-g3  {mark[c.wg3['passes']]}  the counterfactual rebuild is the "
          f"identity: {sum(1 for r in c.wg3['runs'].values() if r['passes'])} of "
          f"{len(c.wg3['runs'])}")
    for name, r in c.wg3["runs"].items():
        for p in r["problems"][:3]:
            print(f"                {name}: {p}")
    hs = c.wg3["hash_seeds"]
    if hs["passes"] is None:
        print("              hash seeds: not run here")
    else:
        print(f"              hash seeds {', '.join(hs['seeds'])}: coin identical "
              f"{hs['draws_identical']}, witness varies {hs['witness_varies']}"
              + (f", failed {hs['failed']}" if hs["failed"] else ""))
    g = c.wg4
    print(f"  W-g4  {'SIGNED' if g['passes'] else 'UNSIGNED'}  {g['found']} "
          f"signature line(s), {g['unsigned']} blank"
          + ("" if g["passes"] else " — nothing may be scored or written"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")
