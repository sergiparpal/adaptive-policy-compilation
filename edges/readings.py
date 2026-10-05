"""
POST-RUN readings of `PLAN_EDGES.md`'s stage: what reading `W-a` to `W-c`
needed once their verdicts existed. Zero API calls.

**Nothing here is a bet that could have failed, and no verdict moves.** Every
figure was chosen after `results_edges/score.json` existed, by someone who had
read it, and the record says so in its `provenance` field. That is how
`rung3/edge_direction.py` was written after `P-d` and `P-e`.

WHAT IT RECORDS, per run and pooled.

  coin        `W-c`'s draws, read the way the verdict could not: each draw's
              share right among the cases it resolves, and its right decisions
              minus its wrong ones, each against the proposer's. Read off
              `score.json`, which stores every draw.
  deciding    the rules that decided `D`. A decided case goes to the oldest
              rule left undefeated, so it is often not the rule that declared
              the edge. Also what each decided, how often it was right, and
              which edges it won.
  queues      `D` by the queue it was sent to, with the true queues of the
              wrong ones.
  keyword     the installed edges, by the winner's action, the loser's action,
              whether their shared region lies inside
              `has_security_keyword = True`, and `W-b`'s verdict on the space.
  surfaces    the keyword tickets by true queue on both surfaces: the corpus's,
              off the records, and the space's, off `space_truth_masks`.
  security    `SECURITY_INCIDENT`, the rules' right decisions on it, and how
              many of them came through an edge.

It refuses while the plan is unsigned, like every writer of the package, and it
rebuilds `D` behind the same checks. The suite and the hash seeds are left to
the stage's own run, whose record this module reads.

    python3 -m edges.readings     # writes results_edges/readings.json
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from typing import Any

from harness.provenance import environment
from rung3.order_search_ls import space_truth_masks

from . import gates, plan
from . import rebuild as rb

READINGS_PATH = plan.OUT / "readings.json"
KEYWORD = "has_security_keyword"
SECURITY = "SECURITY_INCIDENT"
PROVENANCE = (
    "POST-RUN: written after W-a to W-c were adjudicated, by someone who had read "
    "results_edges/score.json. Nothing here is a bet that could have failed, and "
    "no verdict moves.")


# ---------------------------------------------------------------------------
# The coin, read otherwise
# ---------------------------------------------------------------------------

def against_draws(draws: list[float], proposer: float) -> dict[str, Any]:
    return {"proposer": proposer, "mean": statistics.fmean(draws),
            "sd": statistics.pstdev(draws), "draws": len(draws),
            "share_at_least_the_proposer": sum(1 for x in draws if x >= proposer)
                                           / len(draws)}


def coin_readings(right: list[int], wrong: list[int], p_right: int,
                  p_wrong: int) -> dict[str, Any]:
    """The share right among the cases each draw resolves, over the draws that
    resolve any; and right minus wrong, over every draw."""
    among = [r / (r + w) for r, w in zip(right, wrong) if r + w]
    return {
        "right_among_resolved": against_draws(among, p_right / (p_right + p_wrong)),
        "right_minus_wrong": against_draws([r - w for r, w in zip(right, wrong)],
                                           p_right - p_wrong),
    }


# ---------------------------------------------------------------------------
# D, by rule and by queue
# ---------------------------------------------------------------------------

def deciding_rules(rec: dict, d: list[int], classes: dict[int, str]) -> list[dict]:
    row = {r["idx"]: r for r in rec["records"]}
    rules = {r["rule_id"]: r for r in rec["rules"]}
    installed = [e for e in rb.all_edges(rec) if classes[e.key] == "installed"]
    count: Counter = Counter()
    right: Counter = Counter()
    for i in d:
        count[row[i]["winner_id"]] += 1
        right[row[i]["winner_id"]] += bool(row[i]["correct"])
    out = []
    for rid, n in count.most_common():
        rule = rules[rid]
        won = [e for e in installed if e.winner == rid]
        out.append({
            "rule_id": rid,
            "conditions": rule["conditions"],
            "action": rule["action"],
            "born_at": rule["born_at"],
            "birth_screen": row[rule["born_at"]]["shown_kind"],
            "decided": n,
            "right": right[rid],
            "installed_edges_won": len(won),
            "of_which_declared_at_its_birth": sum(1 for e in won if e.birth == rule["born_at"]),
            "installed_edges_lost": sum(1 for e in installed if e.loser == rid),
        })
    return out


def by_queue(rec: dict, d: list[int]) -> dict[str, Any]:
    row = {r["idx"]: r for r in rec["records"]}
    out: dict[str, Any] = {}
    for i in d:
        q = out.setdefault(row[i]["predicted"], {"decided": 0, "right": 0,
                                                 "true_queue_of_the_wrong": Counter()})
        q["decided"] += 1
        if row[i]["correct"]:
            q["right"] += 1
        else:
            q["true_queue_of_the_wrong"][row[i]["truth"]] += 1
    return {a: {**q, "true_queue_of_the_wrong": dict(q["true_queue_of_the_wrong"])}
            for a, q in out.items()}


# ---------------------------------------------------------------------------
# The installed edges, and the keyword
# ---------------------------------------------------------------------------

def keyword_groups(rec: dict, declared: rb.Rebuild, classes: dict[int, str],
                   verdicts: dict[int, str], kw: int) -> list[dict]:
    ext = declared.engine.ext
    action = {r["rule_id"]: r["action"] for r in rec["rules"]}
    groups: Counter = Counter()
    for e in rb.all_edges(rec):
        if classes[e.key] != "installed":
            continue
        shared = ext[e.winner] & ext[e.loser]
        groups[(action[e.winner], action[e.loser], (shared & ~kw) == 0,
                verdicts[e.key])] += 1
    return [{"winner_action": w, "loser_action": l, "inside_the_keyword": inside,
             "space_verdict": v, "edges": n}
            for (w, l, inside, v), n in sorted(groups.items(), key=lambda x: -x[1])]


def keyword_surfaces(rec: dict, corpus, space, tmask: dict[str, int]) -> dict[str, Any]:
    kw = space.mask[KEYWORD][True]
    on_space = {a: (m & kw).bit_count() for a, m in tmask.items() if m & kw}
    on_corpus = Counter(rec["records"][i]["truth"] for i, c in enumerate(corpus)
                        if getattr(c, KEYWORD))
    return {"corpus": {"tickets": sum(on_corpus.values()), "true_queue": dict(on_corpus)},
            "space": {"points": kw.bit_count(), "true_queue": on_space}}


def security(rec: dict, d: list[int]) -> dict[str, int]:
    """The rules' right decisions on `SECURITY_INCIDENT`, and those that came
    through an edge."""
    dset = set(d)
    right = [r["idx"] for r in rec["records"] if r["outcome"] == "ACTION"
             and r["truth"] == SECURITY and r["correct"]]
    return {"right_decisions": len(right),
            "of_which_through_an_edge": sum(1 for i in right if i in dset)}


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def read(c: gates.Checks, score: dict) -> dict[str, Any]:
    tmask = space_truth_masks(c.space)
    kw = c.space.mask[KEYWORD][True]
    runs: dict[str, Any] = {}
    pooled_right = [0] * plan.COIN_DRAWS
    pooled_wrong = [0] * plan.COIN_DRAWS
    p_right = p_wrong = 0
    groups: Counter = Counter()
    for k, rec in c.runs.items():
        s = score["runs"][f"run{k}"]
        wc = s["W-c"]
        verdicts = {b["key"]: b["space"] for b in s["W-b"]["edges"]}
        kg = keyword_groups(rec, c.declared[k], c.classes[k], verdicts, kw)
        for g in kg:
            groups[(g["winner_action"], g["loser_action"], g["inside_the_keyword"],
                    g["space_verdict"])] += g["edges"]
        runs[f"run{k}"] = {
            "d": c.d[k],
            "coin": coin_readings(wc["coin_right"], wc["coin_wrong"],
                                  wc["proposer"]["right"], wc["proposer"]["wrong"]),
            "deciding_rules": deciding_rules(rec, c.d[k], c.classes[k]),
            "queues": by_queue(rec, c.d[k]),
            "keyword_groups": kg,
            "security": security(rec, c.d[k]),
        }
        pooled_right = [a + b for a, b in zip(pooled_right, wc["coin_right"])]
        pooled_wrong = [a + b for a, b in zip(pooled_wrong, wc["coin_wrong"])]
        p_right += wc["proposer"]["right"]
        p_wrong += wc["proposer"]["wrong"]
    first = next(iter(c.runs.values()))
    return {
        "runs": runs,
        "pooled": {
            "coin": coin_readings(pooled_right, pooled_wrong, p_right, p_wrong),
            "keyword_groups": [
                {"winner_action": w, "loser_action": l, "inside_the_keyword": inside,
                 "space_verdict": v, "edges": n}
                for (w, l, inside, v), n in sorted(groups.items(), key=lambda x: -x[1])],
        },
        # The corpus and the labels are the same in all three records (W-g1).
        "keyword_surfaces": keyword_surfaces(first, c.corpus, c.space, tmask),
    }


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"edges/readings.py writes {READINGS_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    checks = gates.run_all(suite=False, seeds=False)
    gates.report(checks)
    if not checks.blocking_pass:
        sys.exit("\nREFUSED: a blocking check failed; nothing was written.\n")
    if {k: len(v) for k, v in checks.d.items()} != {
            k: score["runs"][f"run{k}"]["d"] for k in plan.RUNS}:
        sys.exit("\nREFUSED: D rebuilt here is not the D the stage scored.\n")
    READINGS_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "its_commit": score["_env"].get("git_commit")},
        "surface": {"coin, deciding, queues, security": "corpus, D",
                    "keyword": "the space, over each installed edge's shared region",
                    "keyword_surfaces": "both"},
        "gates": checks.summary(),
        **read(checks, score),
    }, indent=2) + "\n")
    print(f"\nwrote {READINGS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
