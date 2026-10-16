"""
The stage of `PLAN_BOUND.md`: the certificate on every instance, `H-a` to
`H-d`, and the readings of `H-e`. Zero API calls.

It refuses while the plan is unsigned, before it measures, builds or writes
anything. Then it runs `H-g1` to `H-g4` again, all blocking. Only after both
does it pack a cycle on rung 1's rules.

WHAT IT MEASURES (§0 and §7 of the plan), on each instance:

  coverable   the coverage bound, in cases
  attained    the best searched score a record publishes (`instances.published`)
  nu          the cases the certificate shows every order loses
  bound       coverable - nu: the certified bound
  residue     coverable - attained, the gap STATUS.md's first open item asks about
  share       nu / residue: how much of that gap the certificate shows is slack
  met         the certified bound equals the searched score: on the corpus in
              cases, on the space to the four decimals the search is published to

and adjudicates

  H-a   space, pure pool:   share >= 0.50
  H-b   space, hybrid pool: share >= 0.50
  H-c   space: met on neither pool
  H-d   corpus train halves: the median share over the ten (split, pool)
        instances >= 0.75. An instance with no residue counts as share 1.

TWO THINGS STOP IT BEFORE IT WRITES, both of which would mean the instrument is
wrong rather than that a row came out one way or the other: a certificate
`verify` refuses, and a certified bound below a score some order attained.

    python3 -m bound.score --dry-run   # H-g1..H-g4; writes nothing
    python3 -m bound.score             # refuses while PLAN_BOUND.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from typing import Any

from harness.provenance import environment

from . import gates, plan
from .certificate import FINDER_SEED, FINDER_STARTS, certificate, verify


# ---------------------------------------------------------------------------
# One instance
# ---------------------------------------------------------------------------

def measure(inst, attained: int | float, on_space: bool) -> dict[str, Any]:
    """The certificate on one instance, checked twice before it is believed:
    by `verify`, from the masks alone, and against a score an order reached.
    `attained` is a count on the corpus and a four-decimal share on the space."""
    t0 = time.time()
    cert = certificate(inst)
    v = verify(inst, cert)
    if not v["ok"] or v["nu"] != cert["nu"]:
        sys.exit(f"\nREFUSED: the certificate on {inst.name} does not verify: "
                 f"{v['problems'][:3]}. Nothing was written.\n")
    n, cov, nu, bound = inst.n, cert["coverable"], cert["nu"], cert["bound"]
    if on_space:
        half = 0.5 * 10 ** -plan.SPACE_PLACES
        valid = bound / n >= attained - half
        residue = cov / n - attained
        share = (nu / n) / residue if residue > 0 else 1.0
        # the searched score is known to +-half, so the share to this range
        lo_res, hi_res = residue + half, residue - half
        share_range = [(nu / n) / lo_res if lo_res > 0 else 1.0,
                       (nu / n) / hi_res if hi_res > 0 else float("inf")]
        met = round(bound / n, plan.SPACE_PLACES) == attained
        residue_after = bound / n - attained
    else:
        valid = bound >= attained
        residue = cov - attained
        share = nu / residue if residue > 0 else 1.0
        share_range = [share, share]
        met = bound == attained
        residue_after = bound - attained
    if not valid:
        sys.exit(f"\nREFUSED: on {inst.name} the certified bound {bound} is below "
                 f"the searched score {attained}. The certificate is wrong. "
                 "Nothing was written.\n")
    return {
        "instance": inst.name, "n": n, "coverable": cov, "attained": attained,
        "nu": nu, "bound": bound,
        "bound_share": bound / n, "coverable_share": cov / n,
        "residue": residue, "residue_after": residue_after,
        "share_closed": share, "share_range": share_range, "met": met,
        "structure": {k: cert[k] for k in (
            "n_rules", "n_classes", "uncontested", "contested", "n_signatures",
            "n_singleton_signatures", "cases_in_singleton_signatures", "n_nodes",
            "n_cycles", "nu_by_length", "nu_by_start", "best_start")},
        "seconds": round(time.time() - t0, 1),
        "certificate": cert["cycles"],
    }


# ---------------------------------------------------------------------------
# The verdicts
# ---------------------------------------------------------------------------

def verdict_share(share: float, line: float, share_range=None) -> dict:
    """Holds at share >= line. *Thin* when the range the share is known to,
    from the rounding of the searched score, reaches both sides of the line;
    the label does not change the verdict."""
    lo, hi = share_range if share_range is not None else (share, share)
    return {"value": share, "line": line, "range": [lo, hi],
            "verdict": "holds" if share >= line else "refuted",
            "thin": lo < line <= hi}


def verdict_h_c(met: dict[str, bool]) -> dict:
    return {"value": met, "verdict": "holds" if not any(met.values()) else "refuted"}


def verdicts(space: dict, corpus: dict) -> dict:
    shares = [corpus[k]["share_closed"] for k in sorted(corpus)]
    med = statistics.median(shares)
    return {
        "H-a": verdict_share(space["puro"]["share_closed"], plan.H_A_LINE,
                             space["puro"]["share_range"]),
        "H-b": verdict_share(space["hibrido"]["share_closed"], plan.H_B_LINE,
                             space["hibrido"]["share_range"]),
        "H-c": verdict_h_c({p: space[p]["met"] for p in plan.POOLS}),
        "H-d": {**verdict_share(med, plan.H_D_LINE), "shares": shares},
    }


def score(checks: gates.Checks) -> dict[str, Any]:
    pub = checks.pub
    space = {name: measure(inst, pub["space"][name]["attained"], on_space=True)
             for name, inst in checks.space.items()}
    corpus = {key: measure(inst, pub["corpus"][key]["attained"], on_space=False)
              for key, inst in checks.corpus.items()}
    for key in corpus:
        corpus[key]["attained_sources"] = pub["corpus"][key]["sources"]
    return {
        "verdicts": verdicts(space, corpus),
        "space": space,
        "corpus": {f"split {s}/{p}": v for (s, p), v in sorted(corpus.items())},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="PLAN_BOUND.md: the certified bound, H-a to H-d and the "
                    "readings of H-e. Zero API calls.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run H-g1 to H-g4 and stop; nothing packed, nothing written")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("dry run: nothing packed on rung 1's rules, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"bound/score.py writes {plan.SCORE_PATH}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    result = score(checks)
    print()
    for row, v in result["verdicts"].items():
        print(f"  {row}  {v['value']}  (line {v.get('line', '—')})  ->  {v['verdict']}"
              + ("  (thin)" if v.get("thin") else ""))
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "scoring",
        "surface": {
            "H-a": "exhaustive space, pure pool",
            "H-b": "exhaustive space, hybrid pool",
            "H-c": "exhaustive space, both pools",
            "H-d": "corpus, the train half of each of the five splits, both pools",
        },
        "provenance": "PRE-REGISTERED: §0 signed before any of these figures existed",
        "constants": {"finder_seed": FINDER_SEED, "finder_starts": FINDER_STARTS,
                      "space_places": plan.SPACE_PLACES,
                      "lines": {"H-a": plan.H_A_LINE, "H-b": plan.H_B_LINE,
                                "H-d": plan.H_D_LINE}},
        "gates": checks.summary(),
        **result,
    }, indent=2) + "\n")
    print(f"\nwrote {plan.SCORE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
