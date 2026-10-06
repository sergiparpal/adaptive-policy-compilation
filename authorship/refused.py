"""
THE DECLARATIONS LEVEL 1 REFUSED. In `PLAN_AUTHORSHIP.md`'s runs the proposer
declared, 8 times, that a rule should beat a rule strictly inside it, and
`try_edge` refused each as `contradice_subsuncion` (`E-d`). Were they right?

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
Level 1 of rung 2's engine makes the narrower of two nested rules win over its
whole extension, and no declaration can override it. Each refused declaration
says the opposite for one pair: the broader rule should decide the narrower
one's region. Where the two carry different queues, the truth over that region
says which of the two was right, and so what the refusal cost or saved there.
It is the question `IDEAS.md` carries under rung 2, subsumption against
declaration, and the one `E-d` left open in `FINDINGS_AUTHORSHIP.md`.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
For each refused declaration, winner W and loser L, with L strictly inside W:

  the pair   their queues and conditions, which of the two was the rule being
             born when the declaration was made, and the case each was born on.
  space      over the shared region, which is L's extension: the points whose
             true queue is W's and those whose true queue is L's, and the
             better rule by `rung3/edge_direction.py`'s `verdict`, as `W-b` of
             `PLAN_EDGES.md` read the installed edges.
  corpus     the same over the arrivals matching both, counted as often as they
             arrive, as `W-d` read them. Each queue is counted on its own:
             `better_over_corpus` credits a pair's shared queue to the rule
             passed first, which would turn a same-queue tie into a direction.

Pooled over the runs, on each surface: how often the declared winner is the
better rule, among the pairs with a strict better rule. Ties and pairs where
neither rule is ever right are counted apart, as `agreement` counts them.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The declarations are the ones `E-d` counted**: per run, the record's
     `contradice_subsuncion` verdicts number what `score.json` gives.
  2. **Each still is one**: both rules are in the final base, and L's extension
     is strictly inside W's.
  3. **The base is the one Stage C scored**: rebuilt with every installed edge,
     its end to end over the space and on the corpus equals `score.json`'s.
  4. **The truth partitions the space**: the masks sum to its 134,400 points.

It refuses to write if any fails, and while the plan is unsigned, like every
writer of the package.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
**By construction, the declared winner is the rule being born.** No CONFLICT
arose in the three runs, so every escalation was an impasse: no earlier rule
matched the ticket, and the rule born on it matches it, so no earlier rule
contains the new one. In a nested pair met at birth the new rule is therefore
the broader one, and each refused declaration is a new rule claiming to beat an
earlier rule inside it. If one is not, this reading of the records is wrong.

**And three bets, the last the weakest:**

  1. **Most of the eight carry different queues, at least five.** Under v1e the
     proposer must place itself against every rule it overlaps, but naming the
     broader rule the winner is a claim about whose queue holds in the narrower
     one's region, and that claim is idle when the queues agree.
  2. **Over the space the declared winner is the better rule in more than half
     of the pairs with a strict better rule, and on the corpus in half or
     fewer.** That is how `W-b` split the 50 edges installed in `PLAN_REUSE.md`'s
     runs, 0.7556 over the space and 0.4118 by the corpus definition, and these
     are declarations by the same proposer, at write time, on the same loop.
  3. **Most of the eight name `SECURITY_INCIDENT` as the winner's queue**, as
     47 of those 50 edges did.

**What the drafter had seen**: the count per run in `score.json`, 2, 6 and 0;
`FINDINGS_AUTHORSHIP.md`, whose line on `E-d` it wrote; and `FINDINGS_EDGES.md`.
Not the eight rules, their queues, their regions or the truth over them.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN**: asked for after `PLAN_AUTHORSHIP.md`'s verdicts existed, with the
expectation above written before the reading and committed before it ran. Not a
signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero API
calls.

Usage:  PYTHONHASHSEED=0 python3 -m authorship.refused
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

from harness.domain import generate_corpus
from harness.provenance import describe, environment
from rung2.engine2 import EDGE_CONTRADICTS, Space, strictly_below
from rung3.edge_direction import better_over_space, verdict
from rung3.order_search_ls import space_truth_masks

from . import gates, plan
from . import protocol as p

READ_PATH = plan.OUT / "refused.json"
SECURITY = "SECURITY_INCIDENT"
WINNER, LOSER, TIE, NEITHER = "a", "b", "tie", "neither_ever_right"
PROVENANCE = (
    "POST-RUN: asked for after PLAN_AUTHORSHIP.md's verdicts existed. The "
    "expectation in the module's docstring was written before the reading and "
    "committed before it ran. Not a signed row; no verdict moves.")


# ---------------------------------------------------------------------------
# The reading
# ---------------------------------------------------------------------------

def refused(record: dict) -> list[tuple[str, str, str]]:
    """The declarations level 1 refused, as (winner, loser, channel)."""
    log = record.get("edge_log") or []
    chans = record.get("edge_channels") or [p.WRITE] * len(log)
    return [(w, l, ch) for (w, l, why), ch in zip(log, chans) if why == EDGE_CONTRADICTS]


def matched_sets(engine, corpus) -> list[set[str]]:
    """Every rule of the final base matching each case, whenever it was born."""
    return [{r.rule_id for r in engine.rules if r.matches(c)} for c in corpus]


def side(wins_w: int, wins_l: int, region: int) -> dict[str, Any]:
    """One surface of one pair, the declared winner passed first."""
    return {"region": region, "truth_is_winner": wins_w, "truth_is_loser": wins_l,
            "better": verdict(wins_w, wins_l)}


def read_pair(w: str, l: str, channel: str, rules: dict[str, dict], ext: dict[str, int],
              tmask: dict[str, int], sets: list[set[str]], truth: list[str]) -> dict[str, Any]:
    row: dict[str, Any] = {"winner": w, "loser": l, "channel": channel,
                           "in_final_base": w in rules and l in rules}
    if not row["in_final_base"]:
        return row
    action = {rid: r["action"] for rid, r in rules.items()}
    born_w, born_l = rules[w]["born_at"], rules[l]["born_at"]
    shared = [i for i, s in enumerate(sets) if w in s and l in s]
    row.update({
        "strictly_inside": strictly_below(ext[l], ext[w]),
        "being_born": "winner" if born_w > born_l else "loser" if born_l > born_w else "neither",
        "born_at": {"winner": born_w, "loser": born_l},
        "queues": {"winner": action[w], "loser": action[l]},
        "same_queue": action[w] == action[l],
        "conditions": {"winner": rules[w]["conditions"], "loser": rules[l]["conditions"]},
        "space": side(*better_over_space(w, l, ext, action, tmask),
                      (ext[w] & ext[l]).bit_count()),
        "corpus": side(sum(1 for i in shared if truth[i] == action[w]),
                       sum(1 for i in shared if truth[i] == action[l]), len(shared)),
    })
    return row


def direction(rows: list[dict], surface: str) -> dict[str, Any]:
    """How often the declared winner is the better rule, among the pairs with a
    strict better rule; ties and pairs neither rule is ever right on, apart."""
    c = Counter(r[surface]["better"] for r in rows if r.get("in_final_base"))
    n = c[WINNER] + c[LOSER]
    return {"winner_better": c[WINNER], "loser_better": c[LOSER],
            "rate": c[WINNER] / n if n else None, "tie": c[TIE],
            "neither_ever_right": c[NEITHER]}


def read_run(record: dict, corpus, space: Space, tmask: dict[str, int]) -> dict[str, Any]:
    engine, problems = gates.rebuild_final(record, space)
    rules = {r["rule_id"]: r for r in record["rules"]}
    truth = [r["truth"] for r in record["records"]]
    sets = matched_sets(engine, corpus)
    rows = [read_pair(w, l, ch, rules, engine.ext, tmask, sets, truth)
            for w, l, ch in refused(record)]
    return {"rows": rows, "reinstall_problems": problems,
            "e2e": {"space": gates.on_space(engine, tmask, space.n)["e2e"],
                    "corpus": gates.on_corpus(engine, corpus,
                                              gates.labels_of(record))["e2e"]}}


# ---------------------------------------------------------------------------
# The gates and the expectation
# ---------------------------------------------------------------------------

def check(score: dict, runs: dict[int, dict], tmask: dict[str, int],
          n_space: int) -> list[dict]:
    by_rep = {r["rep"]: r for r in score["runs"]}
    out = []
    for rep, got in runs.items():
        published = by_rep[rep]
        rows = got["rows"]
        out.append({"gate": 1, "rep": rep, "what": "the refusals E-d counted",
                    "measured": len(rows), "published": published["E-d"],
                    "passes": len(rows) == published["E-d"]})
        out.append({"gate": 2, "rep": rep, "what": "each still contradicts subsumption",
                    "passes": all(r.get("in_final_base") and r["strictly_inside"]
                                  for r in rows)})
        all_edges = published["E-e"]["by_channel"]["all"]
        same = all(round(got["e2e"][s], 6) == round(all_edges[s]["e2e"], 6)
                   for s in ("space", "corpus"))
        out.append({"gate": 3, "rep": rep, "what": "the base Stage C scored",
                    "measured": {s: round(got["e2e"][s], 6) for s in ("space", "corpus")},
                    "published": {s: all_edges[s]["e2e"] for s in ("space", "corpus")},
                    "passes": same and not got["reinstall_problems"]})
    total = sum(m.bit_count() for m in tmask.values())
    out.append({"gate": 4, "what": "the truth partitions the space",
                "measured": total, "published": n_space, "passes": total == n_space})
    return out


def read_expectation(rows: list[dict], space: dict, corpus: dict) -> list[dict]:
    n = len(rows)
    different = sum(1 for r in rows if not r["same_queue"])
    security = sum(1 for r in rows if r["queues"]["winner"] == SECURITY)
    return [
        {"clause": "by construction", "what": "the declared winner is the rule being born",
         "reading": sum(1 for r in rows if r["being_born"] == "winner"), "of": n,
         "holds": all(r["being_born"] == "winner" for r in rows)},
        {"clause": 1, "what": "at least five of the eight carry different queues",
         "reading": different, "of": n, "holds": different >= 5},
        {"clause": "2, space", "what": "the declared winner better in more than half",
         "reading": space["rate"],
         "holds": None if space["rate"] is None else space["rate"] > 0.5},
        {"clause": "2, corpus", "what": "the declared winner better in half or fewer",
         "reading": corpus["rate"],
         "holds": None if corpus["rate"] is None else corpus["rate"] <= 0.5},
        {"clause": 3, "what": "most name SECURITY_INCIDENT as the winner's queue",
         "reading": security, "of": n, "holds": security > n / 2},
    ]


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    if argv:
        print(__doc__)
        return 2
    plan.refuse_unsigned(f"authorship/refused.py writes {READ_PATH}")
    score = json.loads(plan.SCORE_PATH.read_text())
    corpus = generate_corpus(plan.N, seed=plan.SEED)
    space = Space()
    tmask = space_truth_masks(space)
    runs = {rep: read_run(gates.load(plan.run_path(rep)), corpus, space, tmask)
            for rep in range(1, plan.REPS + 1)}
    checked = check(score, runs, tmask, space.n)
    for g in checked:
        print(f"  gate {g['gate']}{' run ' + str(g['rep']) if 'rep' in g else ''}: "
              f"{'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    rows = [dict(r, rep=rep) for rep, got in runs.items() for r in got["rows"]]
    pooled = {"space": direction(rows, "space"), "corpus": direction(rows, "corpus")}
    READ_PATH.write_text(json.dumps({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "provenance": PROVENANCE,
        "source": {"record": str(plan.SCORE_PATH),
                   "its_commit": score["_env"].get("git_commit")},
        "surfaces": {"space": "the exhaustive space, over each pair's shared region",
                     "corpus": "the 2,000 arrivals matching both rules, as they arrive"},
        "gates": checked,
        "declarations": rows,
        "pooled": pooled,
        "expectation": read_expectation(rows, pooled["space"], pooled["corpus"]),
    }, indent=2) + "\n")
    print(f"\n-> {READ_PATH}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
