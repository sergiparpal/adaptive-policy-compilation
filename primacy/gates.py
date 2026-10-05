"""
`L-g1` to `L-g4` of `PLAN_PRIMACY.md` §6: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  L-g1  The inputs. The suite is green. The 1,600-answer record reproduces its
        own counts: the answers by kind, the parse failures, the accepted edges
        and the per-queue-pair counts. The position figures already published
        reproduce from its rows: 801 of 1,479 edges naming the rule listed
        first, and §15's split by where the ranking's favourite was listed, by
        `rung3.answer_asymmetry`'s own functions. Stage C's breakdown by the
        winner's position reproduces from its rows. The truth per pair lines up
        with the answers row by row, and B-d's split reproduces its published
        counts on both definitions.
  L-g2  The deal. Every slot is the seeded deal and nothing else: the 1,200
        answers of this run carry `winner_positions(1200)`, the 400 reused carry
        Stage D's own record, which carries `winner_positions(400)`, and Stage
        C carries `winner_positions(170)`. A shuffle of a balanced list reads no
        rule, and that is the premise of every lower bound the plan reads.
  L-g3  The definitions. Each row's two rules send the ticket to different
        queues. The rule listed first is `shown_as["A"]`, labelled `A`, and its
        queue is the first the question names. Every answer is consistent with
        the edge it declared. `L-a`'s queue pair is the one the selection rule
        of §2.1 picks, with the record's published split. And the favoured
        queue of every queue pair is defined.
  L-g4  The signature (`primacy/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**What a dry run prints is pass or fail and figures that are already
published.** This module never calls `rows.slot_effect` or
`rows.none_by_favoured_slot`, the statistics of §0's rows, and
`tests/test_primacy.py` checks that it does not.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from rung2.engine2 import EDGE_OK
from rung2.pair_judgement import SHOWN_AS, winner_positions
from rung3 import answer_asymmetry
from rung3.edge_dropping import revealed_ranking

from reuse.gates import run_suite

from . import plan
from . import rows as R


@dataclass
class Checks:
    lg1: dict
    lg2: dict
    lg3: dict
    lg4: dict
    src: dict = field(repr=False)
    hidden: dict = field(repr=False)
    sample: dict = field(repr=False)

    @property
    def blocking_pass(self) -> bool:
        return self.lg1["passes"] and self.lg2["passes"] and self.lg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"L-g1": {k: self.lg1[k] for k in ("suite", "published", "passes")},
                "L-g2": {k: self.lg2[k] for k in ("deals", "passes")},
                "L-g3": {k: self.lg3[k] for k in ("l_a_queue_pair", "favoured",
                                                  "passes")},
                "L-g4": self.lg4}


def load(path) -> dict:
    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# L-g1
# ---------------------------------------------------------------------------

def own_counts(src: dict, stage_d: dict) -> list[str]:
    """The 1,600-answer record against the counts it publishes about itself.

    Its `parse_failures` counts the calls that run made, not its rows (§5.8 of
    the plan): the 400 answers it reused carry Stage D's own failures, which
    Stage D's record counts."""
    ans = src["answers"]
    problems = []
    if len(ans) != plan.N_ROWS:
        problems.append(f"{len(ans)} answers, expected {plan.N_ROWS}")
    if dict(Counter(r["declared"] for r in ans)) != src["declared"]:
        problems.append("the answers by kind do not reproduce `declared`")
    for batch, published in (("this_run", src["parse_failures"]),
                             ("stage_d", stage_d["parse_failures"])):
        if sum(1 for r in ans if r.get("parse_failed")
               and r["answer_from"] == batch) != published:
            problems.append(f"the parse failures of {batch} do not reproduce")
    if sum(1 for r in ans if r.get("try_edge_verdict") == EDGE_OK) != src["n_edges_accepted"]:
        problems.append("the accepted edges do not reproduce")
    if R.per_queue_pair(ans) != src["revealed_hierarchy"]["per_queue_pair"]:
        problems.append("the per-queue-pair counts do not reproduce")
    return problems


def published_position(src: dict, direction: dict, asymmetry: dict) -> dict:
    """801 of 1,479, and §15's split, recomputed from the rows."""
    ans = src["answers"]
    dec = R.declared(ans)
    first = sum(1 for r in dec if R.winner(r) == R.first_rule(r))
    pp = direction["presentation_position"]
    edges = [r for r in ans if r["declared"] != R.NONE]
    _order, rank, _c = revealed_ranking(edges)
    pos = answer_asymmetry.position_test(answer_asymmetry.features(edges, rank))
    h4 = asymmetry["H4_position"]
    split = {k: [pos[k]["hits"], pos[k]["n"]]
             for k in ("favoured_shown_first", "favoured_shown_second")}
    want = {k: [h4[k]["hits"], h4[k]["n"]] for k in split}
    return {"first_listed": [first, len(dec)],
            "first_listed_published": [pp["winner_shown_first"], pp["n_edges"]],
            "h4": split, "h4_published": want,
            "passes": ([first, len(dec)] == [pp["winner_shown_first"], pp["n_edges"]]
                       and split == want)}


def stage_c_breakdown(hidden: dict) -> dict:
    """Stage C's counts by the winner's position, recomputed from its rows."""
    got = {"shown_first": Counter(), "shown_second": Counter()}
    for r in hidden["answers"]:
        slot = "shown_first" if r["winner_shown_as"] == "A" else "shown_second"
        got[slot][r["outcome"]] += 1
    pub = hidden["breakdowns"]["by_position_of_the_winner"]
    table = {s: {k: got[s][k] for k in ("correct", "wrong", "neither")} for s in got}
    want = {s: {k: pub[s][k] for k in ("correct", "wrong", "neither")} for s in got}
    return {"counts": table, "passes": table == want}


def truth_lines_up(src: dict, sample: dict, direction: dict) -> list[str]:
    """The truth per pair is the sample's, row for row, and the published
    direction record carries the same verdicts."""
    ans, oracle, dpairs = src["answers"], sample["oracle"], direction["pairs"]
    problems = []
    if not len(ans) == len(oracle) == len(dpairs):
        return [f"{len(ans)} answers, {len(oracle)} truths, {len(dpairs)} directions"]
    for k, (r, o, p) in enumerate(zip(ans, oracle, dpairs)):
        if r["index"] != k or o["index"] != k:
            problems.append(f"row {k}: index {r['index']} / {o['index']}")
        elif (r["rule_a"], r["rule_b"]) != (o["rule_a"], o["rule_b"]) \
                or (r["rule_a"], r["rule_b"]) != (p["rule_a"], p["rule_b"]):
            problems.append(f"row {k}: the pair differs between records")
        elif (o["better_space"], o["better_corpus"]) != (p["better_space"],
                                                         p["better_corpus"]):
            problems.append(f"row {k}: the truth differs between records")
        if len(problems) >= 5:
            break
    return problems


def b_d_split(src: dict, sample: dict, direction: dict) -> dict:
    """B-d's sides, recounted from the rows and the truth: the sample's counts
    on both definitions, and the declared edges on each side on the space."""
    ans, oracle = src["answers"], sample["oracle"]
    out, ok = {}, True
    for surface in ("space", "corpus"):
        split = sample["split_for_B_d"][surface]
        unreachable = set(split["unreachable_queue_pairs"])
        strict = [k for k, o in enumerate(oracle) if o[f"better_{surface}"] in ("a", "b")]
        far = [k for k in strict if R.pair_key(R.queue_pair(ans[k])) in unreachable]
        got = [len(strict), len(strict) - len(far), len(far)]
        want = [split["n_strict"], split["n_reachable"], split["n_unreachable"]]
        out[surface] = {"strict_reachable_unreachable": got, "published": want}
        ok &= got == want
    bd = direction["B_d_direction_by_queue_ranking_side"]["space"]
    unreachable = set(sample["split_for_B_d"]["space"]["unreachable_queue_pairs"])
    sides = Counter()
    for k, o in enumerate(oracle):
        if o["better_space"] in ("a", "b") and R.winner(ans[k]) is not None:
            far = R.pair_key(R.queue_pair(ans[k])) in unreachable
            sides["unreachable" if far else "reachable"] += 1
    got = [sides["reachable"], sides["unreachable"]]
    want = [bd["reachable"]["n"], bd["unreachable"]["n"]]
    out["declared_on_each_side_space"] = {"got": got, "published": want}
    return {"surfaces": out, "passes": ok and got == want}


def gate_lg1(src, stage_d, hidden, sample, direction, asymmetry,
             suite: bool = True) -> dict:
    counts = own_counts(src, stage_d)
    position = published_position(src, direction, asymmetry)
    stage_c = stage_c_breakdown(hidden)
    truth = truth_lines_up(src, sample, direction)
    bd = b_d_split(src, sample, direction)
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {
        "what": ("the suite is green; the record reproduces its own counts and "
                 "the published position figures; Stage C's breakdown "
                 "reproduces; the truth lines up; B-d's split reproduces"),
        "suite": tests,
        "own_counts": counts,
        "published": {"position": position, "stage_c": stage_c, "b_d": bd},
        "truth": truth,
        "passes": (not counts and position["passes"] and stage_c["passes"]
                   and not truth and bd["passes"] and tests["passes"] is not False),
    }


# ---------------------------------------------------------------------------
# L-g2
# ---------------------------------------------------------------------------

def gate_lg2(src: dict, stage_d: dict, hidden: dict) -> dict:
    ans = src["answers"]
    fresh = [SHOWN_AS.index(r["a_shown_as"]) for r in ans if r["answer_from"] == "this_run"]
    reused = [r for r in ans if r["answer_from"] == "stage_d"]
    d_rows = stage_d["answers"]
    d_slots = [SHOWN_AS.index(r["a_shown_as"]) for r in d_rows]
    by_pair = {(r["rule_a"], r["rule_b"]): r for r in d_rows}
    copied = [r for r in reused
              if (r["rule_a"], r["rule_b"]) in by_pair
              and all(r[k] == by_pair[(r["rule_a"], r["rule_b"])][k]
                      for k in ("a_shown_as", "declared", "answer", "question"))]
    h_slots = [SHOWN_AS.index(r["winner_shown_as"]) for r in hidden["answers"]]
    deals = {
        "fresh": {"n": len(fresh), "is_the_deal": fresh == winner_positions(
            len(fresh), seed=plan.POSITION_SEED), "expected_n": plan.N_FRESH},
        "stage_d": {"n": len(d_rows), "is_the_deal": d_slots == winner_positions(
            len(d_rows), seed=plan.POSITION_SEED), "expected_n": plan.N_REUSED},
        "reused_are_stage_d": {"n": len(reused), "copied": len(copied)},
        "stage_c": {"n": len(h_slots), "is_the_deal": h_slots == winner_positions(
            len(h_slots), seed=plan.POSITION_SEED), "expected_n": plan.N_HIDDEN},
    }
    passes = (deals["fresh"]["is_the_deal"] and len(fresh) == plan.N_FRESH
              and deals["stage_d"]["is_the_deal"] and len(d_rows) == plan.N_REUSED
              and len(reused) == len(copied) == plan.N_REUSED
              and deals["stage_c"]["is_the_deal"] and len(h_slots) == plan.N_HIDDEN)
    return {"what": ("every slot is the seeded deal of rung2.pair_judgement."
                     "winner_positions, which shuffles a balanced list and reads "
                     "no rule"),
            "deals": deals, "passes": passes}


# ---------------------------------------------------------------------------
# L-g3
# ---------------------------------------------------------------------------

def row_problems(r: dict) -> list[str]:
    k = r["index"]
    if r["action_a"] == r["action_b"]:
        return [f"row {k}: both rules send the ticket to {r['action_a']}"]
    first = r["rule_a"] if r["a_shown_as"] == "A" else r["rule_b"]
    second = r["rule_b"] if first == r["rule_a"] else r["rule_a"]
    if r["shown_as"] != {"A": first, "B": second}:
        return [f"row {k}: shown_as disagrees with a_shown_as"]
    lines = r["question"].splitlines()
    if not (len(lines) > 2 and lines[1].lstrip().startswith("A:")
            and lines[2].lstrip().startswith("B:")
            and lines[1].rstrip().endswith(R.action(r, first))
            and lines[2].rstrip().endswith(R.action(r, second))):
        return [f"row {k}: the question does not list A then B with their queues"]
    w = R.winner(r)
    if w is not None and r["answer"] != R.action(r, w):
        return [f"row {k}: declared {r['declared']} but answered {r['answer']}"]
    if w is None and r["answer"] in (r["action_a"], r["action_b"]):
        return [f"row {k}: no edge, yet it answered one of the two queues"]
    if (w is None and r["answer"] is None and not r.get("parse_failed")
            and r.get("raw_answer") is not None):
        # A payload that parsed without an action is recorded with no answer
        # and no raw answer (`rung2/pair_judgement.py`); anything else is not.
        return [f"row {k}: no answer, no parse failure, raw {r['raw_answer']!r}"]
    return []


def l_a_selection(src: dict) -> dict:
    """§2.1's rule: the queue pairs with at least 30 declared answers whose
    majority is below 0.60. It must pick exactly `L-a`'s, with the split the
    record publishes."""
    counts = src["revealed_hierarchy"]["per_queue_pair"]
    picked = sorted(k for k, c in counts.items()
                    if sum(c.values()) >= plan.L_A_SELECT_MIN_ROWS
                    and max(c.values()) / sum(c.values()) < plan.L_A_SELECT_BELOW)
    key = R.pair_key(tuple(sorted(plan.L_A_QUEUE_PAIR)))
    return {"picked": picked, "split_published": counts.get(key),
            "passes": picked == [key]}


def gate_lg3(src: dict) -> dict:
    ans = src["answers"]
    problems = []
    for r in ans:
        problems += row_problems(r)
        if len(problems) >= 5:
            break
    selection = l_a_selection(src)
    maj = R.majority(ans)
    ties = sorted(R.pair_key(qp) for qp, q in maj.items() if q is None)
    apart = sum(1 for r in ans if R.favoured_rule(r, maj) is None)
    return {"what": ("each row is two queues, listed A then B as shown_as says, "
                     "and answered consistently; L-a's queue pair is the one "
                     "§2.1's rule picks; every queue pair has a favoured queue"),
            "rows": problems[:5],
            "l_a_queue_pair": selection,
            "favoured": {"ties": ties, "rows_counted_apart": apart},
            "passes": not problems and selection["passes"] and not ties}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_all(suite: bool = True) -> Checks:
    src, stage_d, hidden = load(plan.SOURCE), load(plan.STAGE_D), load(plan.HIDDEN)
    sample, direction = load(plan.SAMPLE), load(plan.DIRECTION)
    asymmetry = load(plan.ASYMMETRY)
    return Checks(lg1=gate_lg1(src, stage_d, hidden, sample, direction, asymmetry,
                               suite=suite),
                  lg2=gate_lg2(src, stage_d, hidden),
                  lg3=gate_lg3(src),
                  lg4=plan.gate_signature(),
                  src=src, hidden=hidden, sample=sample)


def report(c: Checks) -> None:
    mark = {True: "PASS", False: "FAIL", None: "—"}
    print("=" * 78)
    print(f"{plan.PLAN} — blocking checks (§6), zero API calls")
    print("=" * 78)
    g = c.lg1
    t = g["suite"]
    print(f"  L-g1  {mark[g['passes']]}  test suite: " + (
        f"{t['tests']} tests, {t['result']} ({t['seconds']} s)" if t["ran"]
        else "not run here"))
    print("              the record reproduces its own counts: "
          + ("yes" if not g["own_counts"] else "; ".join(g["own_counts"])))
    p = g["published"]["position"]
    print(f"              named the rule listed first: {p['first_listed'][0]} of "
          f"{p['first_listed'][1]} (published {p['first_listed_published'][0]} "
          f"of {p['first_listed_published'][1]})")
    for k, (h, n) in p["h4"].items():
        print(f"              §15 {k}: {h} of {n} (published "
              f"{p['h4_published'][k][0]} of {p['h4_published'][k][1]})")
    sc = g["published"]["stage_c"]
    print(f"              Stage C by the winner's position reproduces: "
          f"{sc['passes']}  {sc['counts']}")
    print("              the truth lines up row by row: "
          + ("yes" if not g["truth"] else "; ".join(g["truth"])))
    for s, v in g["published"]["b_d"]["surfaces"].items():
        print(f"              B-d {s}: {v}")
    g = c.lg2
    print(f"  L-g2  {mark[g['passes']]}  the slots are the seeded deal:")
    for k, v in g["deals"].items():
        print(f"                {k}: {v}")
    g = c.lg3
    print(f"  L-g3  {mark[g['passes']]}  rows well formed: "
          + ("yes" if not g["rows"] else "; ".join(g["rows"])))
    sel = g["l_a_queue_pair"]
    print(f"              §2.1 picks {sel['picked']}, split {sel['split_published']}")
    print(f"              favoured queue defined everywhere: ties {g['favoured']['ties']}"
          f", rows counted apart {g['favoured']['rows_counted_apart']}")
    s = c.lg4
    print(f"  L-g4  {'SIGNED' if s['passes'] else 'UNSIGNED'}  {s['found']} "
          f"signature line(s), {s['unsigned']} blank"
          + ("" if s["passes"] else " — nothing may be scored or written"))
    print(f"\n  blocking checks: {'ALL PASS' if c.blocking_pass else 'FAILED'}")
