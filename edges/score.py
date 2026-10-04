"""
The stage of `PLAN_EDGES.md`: the census, the three adjudications and `W-d`.
Zero API calls.

It refuses while the plan is unsigned, before it measures, builds or writes
anything. Then it runs `W-g1` to `W-g4` again, all blocking. Only after both
does it read a label of `D`.

WHAT IT MEASURES (§0 and §7 of the plan), per run and pooled over the three:

  census  every logged edge by what it did: installed, redundant (§5.1), or
          refused. For each installed one, its birth screen, which end is the
          newborn, and the corpus cases and space points its two rules share.
  W-a     over `D`, the share the record marks correct, with its error
          clustered by `winner_id` (§5.8).
  W-b     over the installed edges, the better rule on the exhaustive space,
          counted as `FINDINGS3.md` §9 counts it, and the share declared towards
          it. Ties and `neither` are counted apart, and under
          `MIN_QUALIFYING_EDGES` the row is unadjudicable.
  W-c     the proposer's right decisions over `D` against `COIN_DRAWS` coin
          draws, each a rebuild with births and edge timing fixed (§5.3). The
          inverted and oracle arms sit beside them.
  W-d     §5.9's split of `W-a`'s errors, `W-b` by the corpus definition, and
          each final base with and without its edges, on the corpus and on the
          space: the final base as a machine, not the run.

THE LABELS. On the corpus, the records' own `truth` and `correct`. On the space,
`rung3.order_search_ls.space_truth_masks`, a module allowed to see the oracle.
No module of this package imports the oracle.

    python3 -m edges.score --dry-run   # W-g1..W-g4; writes nothing
    python3 -m edges.score             # refuses while PLAN_EDGES.md is unsigned
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter
from typing import Any

from harness.ceiling_check import all_cases
from harness.provenance import environment
from rung3.edge_direction import better_over_corpus, better_over_space, verdict
from rung3.order_search_ls import space_truth_masks

from . import gates, plan
from . import rebuild as rb

# `rung3.edge_direction.verdict`'s names, and this module always calls it with
# the declared winner first: "a" is the declared winner, "b" the declared loser.
WINNER, LOSER, TIE, NEITHER = "a", "b", "tie", "neither_ever_right"


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------

def clustered_share(ys: list[int], clusters: list) -> dict[str, Any]:
    """A share and its standard error, clustered (§5.8): the variance of a mean
    with the residuals summed within each cluster, and the G/(G-1)
    correction."""
    n = len(ys)
    if not n:
        return {"n": 0, "right": 0, "share": None, "se": None, "clusters": 0}
    p = sum(ys) / n
    groups: dict = {}
    for y, c in zip(ys, clusters):
        groups[c] = groups.get(c, 0.0) + (y - p)
    g = len(groups)
    se = (math.sqrt(g / (g - 1) * sum(v * v for v in groups.values())) / n
          if g > 1 else None)
    return {"n": n, "right": sum(ys), "share": p, "se": se, "clusters": g}


def binomial(hits: int, n: int) -> dict[str, Any]:
    if not n:
        return {"n": 0, "hits": 0, "rate": None, "se": None}
    p = hits / n
    return {"n": n, "hits": hits, "rate": p, "se": math.sqrt(p * (1 - p) / n)}


def thin(value, line: float, se) -> bool:
    """Within one standard error of its line: labelled beside the verdict, and
    never changing it."""
    return value is not None and se is not None and abs(value - line) < se


def coin_share(draws: list[int], proposer: int) -> float:
    """The share of draws that score at least the proposer's: a tie counts
    against it."""
    return sum(1 for x in draws if x >= proposer) / len(draws)


def summary(xs: list[int]) -> dict[str, Any]:
    s = sorted(xs)
    at = lambda f: s[min(len(s) - 1, int(f * len(s)))]   # noqa: E731
    return {"mean": statistics.fmean(s), "sd": statistics.pstdev(s),
            "min": s[0], "p05": at(0.05), "p50": at(0.50), "p95": at(0.95),
            "max": s[-1]}


def verdict_w_a(share, se) -> dict[str, Any]:
    line = plan.W_A_REFUTED_AT_OR_ABOVE
    if share is None:
        return {"value": None, "se": None, "line": line,
                "verdict": "unadjudicable", "thin": False}
    return {"value": share, "se": se, "line": line,
            "verdict": "holds" if share < line else "refuted",
            "thin": thin(share, line, se)}


def verdict_w_b(rate, se, n: int) -> dict[str, Any]:
    line = plan.W_B_REFUTED_AT_OR_ABOVE
    if rate is None or n < plan.MIN_QUALIFYING_EDGES:
        return {"value": rate, "se": se, "n": n, "line": line,
                "verdict": "unadjudicable", "thin": False}
    return {"value": rate, "se": se, "n": n, "line": line,
            "verdict": "holds" if rate < line else "refuted",
            "thin": thin(rate, line, se)}


def verdict_w_c(share: float, draws: int = plan.COIN_DRAWS) -> dict[str, Any]:
    line = plan.W_C_MIN_SHARE
    se = math.sqrt(share * (1 - share) / draws)
    return {"value": share, "se": se, "line": line, "draws": draws,
            "verdict": "holds" if share >= line else "refuted",
            "thin": thin(share, line, se)}


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------

def matched_sets(engine, corpus) -> list[set[str]]:
    """Every rule of a base matching each corpus case, whenever it was born."""
    return [{r.rule_id for r in engine.rules if r.matches(c)} for c in corpus]


def census(rec: dict, declared: rb.Rebuild, classes: dict[int, str],
           sets: list[set[str]]) -> dict[str, Any]:
    ext = declared.engine.ext
    action = {r["rule_id"]: r["action"] for r in rec["rules"]}
    born = {r["rule_id"]: r["born_at"] for r in rec["rules"]}
    screen = {row["idx"]: row["shown_kind"] for row in rec["records"] if row["escalated"]}
    rows = []
    for e in rb.all_edges(rec):
        r = {"key": e.key, "birth": e.birth, "winner": e.winner, "loser": e.loser,
             "logged": e.verdict, "class": classes[e.key]}
        if r["class"] in ("installed", "redundant"):
            r.update({
                "same_action": action[e.winner] == action[e.loser],
                "birth_screen": screen.get(e.birth),
                "newborn_wins": born[e.winner] == e.birth,
                "shared_cases": sum(1 for s in sets if e.winner in s and e.loser in s),
                "shared_points": (ext[e.winner] & ext[e.loser]).bit_count(),
            })
        rows.append(r)
    inst = [r for r in rows if r["class"] == "installed"]
    return {
        "logged": len(rows),
        "verdicts": dict(Counter(r["logged"] for r in rows)),
        "classes": dict(Counter(r["class"] for r in rows)),
        "installed": len(inst),
        "installed_same_action": sum(1 for r in inst if r["same_action"]),
        "installed_by_birth_screen": dict(Counter(r["birth_screen"] for r in inst)),
        "installed_newborn_wins": sum(1 for r in inst if r["newborn_wins"]),
        "installed_newborn_loses": sum(1 for r in inst if not r["newborn_wins"]),
        "installed_sharing_no_case": sum(1 for r in inst if r["shared_cases"] == 0),
        "installed_sharing_at_most_two_cases": sum(1 for r in inst
                                                   if r["shared_cases"] <= 2),
        "edges": rows,
    }


# ---------------------------------------------------------------------------
# W-a, W-b, W-c and §5.9, per run
# ---------------------------------------------------------------------------

def w_a_rows(k: int, rec: dict, d: list[int], declared: rb.Rebuild):
    """`D`'s labels, read here for the first time, and the stage's assertion:
    on `D` the rebuild decides what the record decided (`W-g3`), so its right
    count is this numerator."""
    row = {r["idx"]: r for r in rec["records"]}
    ys = [1 if row[i]["correct"] else 0 for i in d]
    rebuilt = sum(1 for i in d if declared.decisions[i].outcome == "ACTION"
                  and declared.decisions[i].action == row[i]["truth"])
    if rebuilt != sum(ys):
        raise AssertionError(f"run {k}: the rebuild's right decisions over D, "
                             f"{rebuilt}, are not the record's, {sum(ys)}")
    return ys, [(k, row[i]["winner_id"]) for i in d]


def directions_better(rec: dict, declared: rb.Rebuild, classes: dict[int, str],
                      tmask: dict[str, int], sets: list[set[str]]) -> list[dict]:
    """The better rule of every installed edge, on the space (`W-b`) and on the
    corpus (`W-d`), with the declared winner passed first."""
    ext = declared.engine.ext
    action = {r["rule_id"]: r["action"] for r in rec["rules"]}
    truth = [r["truth"] for r in rec["records"]]
    out = []
    for e in rb.all_edges(rec):
        if classes[e.key] != "installed":
            continue
        out.append({
            "key": e.key,
            "space": verdict(*better_over_space(e.winner, e.loser, ext, action, tmask)),
            "corpus": verdict(*better_over_corpus(e.winner, e.loser, sets, truth,
                                                  action, range(len(truth)))),
        })
    return out


def direction_rate(rows: list[dict], key: str) -> dict[str, Any]:
    c = Counter(r[key] for r in rows)
    return {**binomial(c[WINNER], c[WINNER] + c[LOSER]),
            "toward_loser": c[LOSER], "tie": c[TIE], "neither_ever_right": c[NEITHER]}


def tally(arm: rb.Rebuild, d: list[int], truth: dict[int, str],
          installed: list[int]) -> dict[str, int]:
    right = wrong = unresolved = 0
    for i in d:
        dec = arm.decisions[i]
        if dec.outcome != "ACTION":
            unresolved += 1
        elif dec.action == truth[i]:
            right += 1
        else:
            wrong += 1
    refused = sum(1 for kk in installed if arm.tried.get(kk) != rb.OK)
    return {"right": right, "wrong": wrong, "unresolved": unresolved,
            "refused": refused}


def arms(k: int, rec: dict, corpus, space, declared: rb.Rebuild, d: list[int],
         better: list[dict]) -> dict[str, Any]:
    """`W-c` for one run: the proposer, the coin, and the inverted and oracle
    arms, all over the same `D` with births and edge timing fixed."""
    truth = {r["idx"]: r["truth"] for r in rec["records"]}
    installed = sorted(declared.installed)
    only = set(d)

    def run(directions):
        return tally(rb.rebuild(rec, corpus, space, only=only, directions=directions),
                     d, truth, installed)

    rng = plan.coin_rng(k)
    draws = [run(rb.coin_directions(installed, rng)) for _ in range(plan.COIN_DRAWS)]
    oracle = {b["key"]: (rb.FLIPPED if b["space"] == LOSER else rb.DECLARED)
              for b in better}
    return {
        "installed": len(installed),
        "proposer": tally(declared, d, truth, installed),
        "inverted": run({kk: rb.FLIPPED for kk in installed}),
        "oracle": run(oracle),
        "coin_right": [x["right"] for x in draws],
        "coin_wrong": [x["wrong"] for x in draws],
        "coin_unresolved": [x["unresolved"] for x in draws],
        "coin_refused": [x["refused"] for x in draws],
    }


def split_errors(rec: dict, d: list[int],
                 without: dict[int, rb.Decision]) -> dict[str, int]:
    """§5.9: on each case of `D`, the contending actions are those of the
    undefeated set the rebuild without edges returns."""
    row = {r["idx"]: r for r in rec["records"]}
    action = {r["rule_id"]: r["action"] for r in rec["rules"]}
    out = {"n": len(d), "right": 0, "wrong_direction": 0, "wrong_material": 0,
           "any_direction_could_be_right": 0}
    for i in d:
        acts = {action[r] for r in without[i].contenders}
        t = row[i]["truth"]
        out["any_direction_could_be_right"] += t in acts
        if row[i]["correct"]:
            out["right"] += 1
        elif t in acts:
            out["wrong_direction"] += 1
        else:
            out["wrong_material"] += 1
    return out


# ---------------------------------------------------------------------------
# W-d: the final bases as machines, on both surfaces
# ---------------------------------------------------------------------------

def levels(decided: list[tuple[str, str | None]], truth: list[str]) -> dict[str, Any]:
    n = len(truth)
    right = sum(1 for (o, a), t in zip(decided, truth) if o == "ACTION" and a == t)
    acted = sum(1 for o, _ in decided if o == "ACTION")
    return {"cases": n, "e2e": right / n,
            "silent_error": (acted - right) / acted if acted else None,
            "silent_errors": acted - right,
            "conflicts": sum(1 for o, _ in decided if o == "CONFLICT"),
            "impasses": sum(1 for o, _ in decided if o == "IMPASSE")}


def decide_all(engine, cases) -> list[tuple[str, str | None]]:
    out = []
    for c in cases:
        o, w, _ = engine.decide(c)
        out.append((o, w.action if w else None))
    return out


def resolved(with_e, without_e, truth, idxs) -> dict[str, Any]:
    hit = [i for i in idxs if without_e[i][0] == "CONFLICT" and with_e[i][0] == "ACTION"]
    right = sum(1 for i in hit if with_e[i][1] == truth[i])
    return {"resolved": len(hit), "right": right,
            "share_right": right / len(hit) if hit else None}


def labels_by_index(tmask: dict[str, int], n: int) -> list[str | None]:
    """Each space point's true action, by case index (MSB-first, §5 of
    `PLAN_PAIRWISE.md`)."""
    out: list[str | None] = [None] * n
    for a, m in tmask.items():
        for i, ch in enumerate(format(m, f"0{n}b")):
            if ch == "1":
                out[i] = a
    return out


def static(rec: dict, corpus, space, declared: rb.Rebuild, edges: list[rb.Edge],
           installed: set[int], cases, space_truth) -> dict[str, Any]:
    final = declared.engine
    bare = rb.rebuild(rec, corpus, space, only=set(),
                      directions=rb.without_installed(installed)).engine
    truth = [r["truth"] for r in rec["records"]]
    c_with, c_without = decide_all(final, corpus), decide_all(bare, corpus)
    region = 0
    for e in edges:
        if e.key in installed:
            region |= final.ext[e.winner] & final.ext[e.loser]
    n = space.n
    inside = [i for i, ch in enumerate(format(region, f"0{n}b")) if ch == "1"]
    s_with = decide_all(final, cases)
    s_without = list(s_with)
    for i, dec in zip(inside, decide_all(bare, [cases[i] for i in inside])):
        s_without[i] = dec
    return {
        "corpus": {"with_edges": levels(c_with, truth),
                   "without_edges": levels(c_without, truth),
                   **resolved(c_with, c_without, truth, range(len(truth)))},
        "space": {"with_edges": levels(s_with, space_truth),
                  "without_edges": levels(s_without, space_truth),
                  "points_where_an_edge_can_matter": len(inside),
                  **resolved(s_with, s_without, space_truth, inside)},
    }


# ---------------------------------------------------------------------------
# The stage
# ---------------------------------------------------------------------------

def score(c: gates.Checks) -> dict[str, Any]:
    tmask = space_truth_masks(c.space)
    cases = list(all_cases())
    space_truth = labels_by_index(tmask, c.space.n)
    runs: dict[str, Any] = {}
    ys_all, cl_all, better_all, split_all = [], [], [], Counter()
    proposer_right, coin_pooled = 0, [0] * plan.COIN_DRAWS
    for k, rec in c.runs.items():
        declared, d = c.declared[k], c.d[k]
        sets = matched_sets(declared.engine, c.corpus)
        ys, cl = w_a_rows(k, rec, d, declared)
        better = directions_better(rec, declared, c.classes[k], tmask, sets)
        arm = arms(k, rec, c.corpus, c.space, declared, d, better)
        split = split_errors(rec, d, c.without[k])
        w_a = clustered_share(ys, cl)
        w_b = direction_rate(better, "space")
        share = coin_share(arm["coin_right"], arm["proposer"]["right"])
        runs[f"run{k}"] = {
            "census": census(rec, declared, c.classes[k], sets),
            "d": len(d),
            "W-a": w_a,
            "W-b": {"space": w_b, "corpus": direction_rate(better, "corpus"),
                    "edges": better},
            "W-c": {**arm, "coin_share": share,
                    "coin_right_summary": summary(arm["coin_right"])},
            "split": split,
            "static": static(rec, c.corpus, c.space, declared, rb.all_edges(rec),
                             declared.installed, cases, space_truth),
        }
        ys_all += ys
        cl_all += cl
        better_all += better
        split_all.update(split)
        proposer_right += arm["proposer"]["right"]
        coin_pooled = [a + b for a, b in zip(coin_pooled, arm["coin_right"])]
    w_a = clustered_share(ys_all, cl_all)
    w_b = direction_rate(better_all, "space")
    share = coin_share(coin_pooled, proposer_right)
    pooled = {
        "W-a": w_a,
        "W-b": {"space": w_b, "corpus": direction_rate(better_all, "corpus")},
        "W-c": {"proposer_right": proposer_right, "coin_share": share,
                "coin_right": coin_pooled, "coin_right_summary": summary(coin_pooled),
                **{arm: sum(r["W-c"][arm]["right"] for r in runs.values())
                   for arm in ("inverted", "oracle")}},
        "split": dict(split_all),
    }
    verdicts = {
        "W-a": verdict_w_a(w_a["share"], w_a["se"]),
        "W-b": verdict_w_b(w_b["rate"], w_b["se"], w_b["n"]),
        "W-c": verdict_w_c(share),
    }
    return {"verdicts": verdicts, "pooled": pooled, "runs": runs}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="PLAN_EDGES.md: the census, W-a to W-c, and W-d. Zero API calls.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run W-g1 to W-g4 and stop; nothing scored, nothing written")
    args = ap.parse_args(argv)

    if args.dry_run:
        checks = gates.run_all(suite=True)
        gates.report(checks)
        print("dry run: nothing scored, nothing written")
        return 0 if checks.blocking_pass else 1

    plan.refuse_unsigned(f"edges/score.py writes {plan.SCORE_PATH}")
    checks = gates.run_all(suite=True)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    result = score(checks)
    print()
    for row, v in result["verdicts"].items():
        print(f"  {row}  {v['value']}  ->  {v['verdict']}"
              + ("  (thin)" if v["thin"] else ""))
    plan.OUT.mkdir(exist_ok=True)
    plan.SCORE_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "stage": "scoring",
        "surface": {
            "W-a": "corpus — seed 17, n=2000, in arrival order: D, the cases the "
                   "edges decided in PLAN_REUSE.md's three Stage B runs",
            "W-b": "the exhaustive space, 134,400 points: the shared region of "
                   "each installed edge; the corpus definition is in W-d",
            "W-c": "corpus — D, rebuilt with births and edge timing fixed (§5.3)",
            "static": "both: the final base of each run as a machine, not the run",
        },
        "provenance": "PRE-REGISTERED: §0 signed before any of these figures existed",
        "constants": {"runs": list(plan.RUNS), "n": plan.N, "seed": plan.SEED,
                      "coin_draws": plan.COIN_DRAWS, "coin_seed": plan.COIN_SEED,
                      "min_qualifying_edges": plan.MIN_QUALIFYING_EDGES,
                      "lines": {"W-a": plan.W_A_REFUTED_AT_OR_ABOVE,
                                "W-b": plan.W_B_REFUTED_AT_OR_ABOVE,
                                "W-c": plan.W_C_MIN_SHARE}},
        "gates": checks.summary(),
        **result,
    }, indent=2) + "\n")
    print(f"\nwrote {plan.SCORE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
