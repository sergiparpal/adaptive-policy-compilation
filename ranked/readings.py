"""
SIX THINGS STAGE C LEFT FREE ON THE RECORDS. `FINDINGS_RANKED.md`, *What Stage
C does not settle*, names nine things its runs do not settle, and says of six
that the records can answer them without a call: why K r2's ranking decided its
conflicts at half, the tickets that beget a rule nested in the keyword's region,
where K's gain lies outside the keyword half, what the pair `T3_ENGINEERING`,
`ACCOUNT_MANAGER` decides in K's bases, why K r2's at-once answers decided so
much more than its loop, and what an engine that abstains where its votes are
silent would have left in conflict. `IDEAS.md` carries the six under *What
`PLAN_RANKED.md` opens*. Asked for by Sergi on 2026-11-20. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`, each with its
rules in birth order, the edges tried at each birth, every arrival with its
truth and the hidden rule that governs it (`truth_rule`), every escalation with
its calls, and the labels handed. K's records also keep, at every case, who
decided it, and where the ranking did, the queues of the undefeated rules, the
ranking then and the votes between the winner's queue and the next.
**The six at-once sessions of the runs**, `results_ranked/atonce_*.json`.
**Stage C**, `results_ranked/score.json`, which the gates hold the reading to.

**A base's queues at a point** are the queues of its rules undefeated there,
under rung 2's containments and the edges installed. Two queues or more is a
**conflict**. L's engine leaves a conflict undecided, which counts as wrong. K's
engine decides it by the queue its ranking puts first among those standing:
those are **the ranking's points**. A final base is read with the run's last
ranking, as Stage C reads it (`ranked/reading.py`). **The keyword half** is the
67,200 points with the security keyword; **the other half** is the rest.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Why K r2's ranking decided its conflicts at half.** Every case a K run's
     ranking took, read at the base and the votes the engine held then. A wrong
     decision is:
     - `absent`: no rule of the case's queue stands at the ticket, so no
       ranking decides it right;
     - `then`: one stands, and the run's last ranking would have put it first,
       so the ranking in force then erred;
     - `last`: one stands, and the last ranking also puts another queue first.
     Beside them: the winner's and the runner-up's queues, the arrival's tenth,
     whether the ranking in force was the last, the keyword, reported or
     silent, the hidden rule that governs the ticket, and the distinct points.
     **The excess** is K r2's share of wrong decisions among the cases its
     ranking took, less K r1's and K r3's pooled. Split by class it adds up.
  B. **The tickets that beget a rule nested in the keyword's region.** A rule is
     **nested** when its queue is not `SECURITY_INCIDENT` and its extension lies
     inside the keyword half. It **reaches** when it holds points of
     `SECURITY_INCIDENT`'s region, and is an **exception** otherwise, inside
     `H03`'s region, the policy's own exception. For every nested rule of the
     six runs: its birth ticket and the hidden rule governing it, the
     escalation and what its report named, what the engine had decided there
     and by which rule, and the first call's draft. Beside them, every first
     call at a ticket of `H03` in the six runs, classed by its draft:
     `reaching`, `exception` (`whole` when it is `H03`'s region), `beyond` (it
     reaches the other half), `other queue`, or `invalid`. And for each ticket
     that begot a reaching rule in some run, its first calls in every run that
     asked it as a reported error, compared pair by pair.
     **What a first call is told.** v1c's first call is blind: the system
     prompt is level 1's catalogue, the same at every call, and the base
     paragraph is the same too. What varies is the ticket, and at a reported
     error the report, which says the engine decided the ticket, that a
     reviewer marked the decision wrong, and which queue is right. The rule
     that erred is never shown.
  C. **Where K's gain lies outside the keyword half.** Under each draw, K's base
     against L's, over the other half: K's points right by rung 2's decision
     and by its ranking; L's right, decided wrong, left in conflict and
     undecided; each by true queue. **K's gain** is K's right points less L's.
     **Added after the first run**, and read by no clause: the points each base
     decides wrong there, one queue standing, by how the rules that decide them
     were born, at an impasse, at a reported error or at a conflict the loop
     asked about; and of the points L decides wrong and K right, those where a
     rule L wrote at a conflict stands.
  D. **K's ranking and the pair `T3_ENGINEERING`, `ACCOUNT_MANAGER`.** In each
     K base, the points **the pair decides**: rules of both queues stand, and no
     queue the last ranking puts above both does. Their truth. Beside them: the
     same base read with the two queues exchanged in the last ranking, and the
     points of `ACCOUNT_MANAGER`'s region where a rule of `T3_ENGINEERING` stands
     beside one of `ACCOUNT_MANAGER`.
  E. **Why K r2's at-once answers decided so much more than its loop.** Each
     run's three at-once answers at all of its labels, installed as Stage C
     installs them, read over the space by queue and by half. For each queue,
     the median of the three recalls; **the median answer**, the middle one by
     points right, ties by ask; and the labels by queue and by the hidden rule
     governing each. K r2's median answer is set against its loop's final base,
     by half.
  F. **An engine that abstains where its votes are silent**, §13's fifth item.
     Where K's ranking decides, each other queue standing makes a pair with the
     winner's: `silent` if no vote went either way, `even` if as many went each
     way, `against` if more put the other queue above, `with` otherwise. A
     decision takes the worst of its pairs, in that order. **The abstaining
     engine** leaves `silent` and `even` in conflict. Read at the arrivals, with
     the votes the engine held then, and over the space with the last votes.
     The winner and the runner-up alone are read beside it.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The bases are Stage C's.** Each run's final base, rebuilt birth by birth,
     decides on its own engine the share and the halves `score.json` keeps, and
     the masks kept as the births came are the engine's.
  2. **The ranking's cases are the record's.** At every case a K record logs as
     decided by its ranking, the replay finds the same queues in the same
     order, the same ranking, runner-up and votes, and the winner is the
     decision the record keeps. And at no other case does it find a conflict.
  3. **The at-once answers are Stage C's.** Each answer chosen at all of a run's
     labels, installed, decides the share `score.json` keeps for it.
  4. **The nested rules are Stage C's**, with their points, their points of
     `SECURITY_INCIDENT` and those decided wrong.
  5. **A born draft is its rule.** At the birth of every nested rule, the first
     call's draft has the rule's queue and extension.
  6. **The last ranking is the record's**, in every K run.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  A1. **The last ranking is why.** The class `last` carries more than half of
      K r2's excess of wrong decisions over K r1's and K r3's pooled.
  A2. **Billing against the technical queue.** In K r2, the pair
      `BILLING_SPECIALIST` and `T2_TECHNICAL`, as winner and runner-up either
      way, carries more than half of the wrong decisions.
  A3. **Many tickets, not one again and again.** In K r2, the wrong decisions
      fall on more distinct points of the space than half their number.
  B1. **The exception's tickets.** In the six runs, every nested rule that
      reaches was born at a ticket of `H03`.
  B2. **Told the queue.** Every such birth was a reported error whose report
      named `T2_TECHNICAL`.
  B3. **The tier dropped.** Every such rule holds points of `H01`'s region,
      where the tier decides.
  B4. **Mostly so.** Of the first calls at tickets of `H03` told
      `T2_TECHNICAL`, in the six runs, whose drafts lie inside the keyword half,
      more reach than stay inside `H03`'s region.
  B5. **The ticket, not the run.** Over the tickets that begot a reaching rule
      in some run, more than half of the pairs of runs that asked the ticket as
      a reported error drafted the same queue and extension at its first call.
  C1. **The interleaving queues.** In every draw, more than half of the other
      half's points K's ranking decides right are `ACCOUNT_MANAGER`'s,
      `T3_ENGINEERING`'s and `SELF_SERVICE_DEFLECT`'s.
  C2. **L's loss there is conflict.** In every draw, the points L leaves in
      conflict are more than half of those it does not decide right in the
      other half.
  C3. **K decides them.** In every draw, K decides right more than half of the
      other half's points L leaves in conflict.
  D1. **Little to decide.** In every K run, the pair decides fewer than 1,344
      points, a hundredth of the space.
  D2. **And there it is wrong.** In every K run, where the pair decides,
      `ACCOUNT_MANAGER`'s points outnumber `T3_ENGINEERING`'s.
  D3. **They seldom meet on the account manager's points.** In every K run, a
      rule of `T3_ENGINEERING` stands undefeated beside one of
      `ACCOUNT_MANAGER` on fewer than a tenth of `ACCOUNT_MANAGER`'s points.
  E1. **The security queue.** At all of its labels, K r2's median at-once
      recall of `SECURITY_INCIDENT` is above every other run's.
  E2. **In the keyword half.** More than half of what K r2's median answer
      decides right beyond its loop's final base lies in the keyword half.
  E3. **And the rarest queue.** At all of its labels, K r2's median at-once
      recall of `ONCALL_ESCALATION` is above every other run's.
  F1. **Seldom at the arrivals.** In every K run, the abstaining engine would
      have left in conflict fewer than a tenth of the cases the ranking took.
  F2. **Seldom over the space.** In every K run, it would leave in conflict
      fewer than a tenth of the points the ranking decides.
  F3. **And there the ranking is right.** In every K run, the ranking decides
      right more than half of the points it would leave.

A clause that reads a missing value fails.

**The drafter's account.**
- **A.** The three K runs ended on one ranking, so what parts K r2 from the
  others is the base its ranking met, or the rankings it held on the way. K r2's
  base recalls `BILLING_SPECIALIST` at 0.4327, against 0.6579 and 0.6784, and
  every last ranking puts `T2_TECHNICAL` above it. Where a rule of each stands
  at a billing ticket, the ranking sends it to `T2_TECHNICAL`, and billing's
  tickets are common at the arrivals. That is `last`: A1, and A2, the bet. The
  keyword's tickets are 71 of the 2,000 arrivals, so the rule nested at case 529
  can carry few of the 79 cases. A wrong ranking decides the same conflict at
  every arrival that falls there, but billing's tickets spread over many points:
  A3.
- **B.** `H03`'s tickets are 51 of the corpus's 71 keyword tickets, and a
  keyword rule of `SECURITY_INCIDENT` decides them wrong. Level 1's catalogue
  says what each queue is for, and nothing of tier or severity. The system
  prompt says that nested exceptions order themselves. So a blind first call,
  told that a keyword ticket is `T2_TECHNICAL`'s, writes an exception nested in
  the keyword, and has to guess why. Severity reads as impact, and the drafter
  expects it to explain the label by severity and drop the tier: B3, B4. B1 and
  B2 follow if no first call writes `T2_TECHNICAL` inside the keyword
  unprompted. B5 reads whether one prompt gives one draft: a ticket's first call
  is sent the same texts in every run and in both arms.
- **C.** K's bases recall `ACCOUNT_MANAGER`, `T3_ENGINEERING` and
  `SELF_SERVICE_DEFLECT` far above L's in every run, and those queues lie
  mostly in the other half: C1. `FINDINGS_RANKED.md`'s cross-reading already
  bounds the rest of the split. K's ranking decides right 0.1840, 0.1103 and
  0.0503 of the space, and in draw 3 that is less than half of K's gain in the
  other half alone, so K r3's gain there is mostly its rules'. No clause reads
  that split. C2: on the closed runs L lost mostly by right sides refused,
  which leave their regions in conflict. C3 follows if K's ranking orders those
  meetings right, as `RK-e` found it did at the arrivals.
- **D.** Every K ranking puts `T3_ENGINEERING` above `ACCOUNT_MANAGER`, and K's
  bases still recall `ACCOUNT_MANAGER` at 0.8637 to 0.9313. So the pair can
  decide little of its points: D1, D3. Where it decides, the policy puts churn
  before product routing, and `T3_ENGINEERING` wins only at severity 1: D2, as
  `corrections/gap.py` read the closed runs' declared ranking.
- **E.** K r2's labels named `SECURITY_INCIDENT` eight times and
  `ONCALL_ESCALATION` twice, more than any other run's. Compiled at once, the
  model writes what its labels show (`corrections/layer.py`): E1, E3. K r2's
  loop decided half of the keyword half, under the rule nested at case 529: E2.
- **F.** No case K's ranking took was decided on a tie between the winner's
  queue and the next, and most conflicts at the arrivals hold two queues: F1.
  Over the space more points hold three queues or more, and more pairs meet
  seldom, but after thousands of votes few pairs are silent: F2. Silence falls
  between queues that seldom meet, which the ranking places by their other
  pairs, much as the policy's layers do: F3.

**The bet is A2.** **B1, B2 and F1 are trusted most.** **E3, B5 and C2 are
trusted least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole, every figure in it; `PLAN_RANKED.md` §2.2 to
  §2.4, §5.2 to §5.5, §6 and §13; `STATUS.md`'s and `IDEAS.md`'s entries on
  `PLAN_RANKED.md` and `PLAN_CORRECTIONS.md`; and what `PLAN_CORRECTIONS.md`'s
  POST-RUN readings found, as its record states it, among it that case 529
  begot `keyword and severity other than 1` in that plan's L r3;
- the corpus's make-up by true queue and its 71 keyword tickets; level 1's
  catalogue lines for `T2_TECHNICAL` and `SECURITY_INCIDENT`, and the system
  prompt's sentence on nested exceptions;
- the records' layouts, by their keys; one escalation of K r2, case 5: its
  kind, its verdict, its list and the shape of its two calls; how many
  escalations of K r1 and L r1 were born or unplaced, and how many were
  copies; that in the six runs every escalation has one first call and at most
  one placement round, and how many had one, and that every first call came
  back an object; that K's smoke record holds no case its ranking took; the
  formats of the fields of `score.json` the gates compare;
- that a final base rebuilds in about a second, and that the walk's masks are
  the engine's on K r2 and L r1.

**What the drafter had not seen**: any case the ranking took, its queues, truth
or votes; any nested rule's conditions or birth ticket beyond what
`FINDINGS_RANKED.md` names; any first call's draft; any at-once answer's rules
or recall; any vote by pair; any mask of a base by half or by queue beyond
`FINDINGS_RANKED.md`'s tables.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `PLAN_RANKED.md`'s Stage
C. The expectation above was written and committed before the reading ran. Not
a signed row, not on `STATUS.md`'s scoreboard, not a calibration event. Zero
API calls.

**One part was added after the first run**, C's decided-wrong points by birth,
in a commit of its own. The first run had printed every clause's verdict, and
its readings A to F had been read whole. No clause reads the added part, and
no clause was changed.

Usage:  python3 -m ranked.readings --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.readings
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from typing import Any, Sequence

from harness.domain import ACTIONS, ATTRIBUTES
from harness.provenance import describe, environment

from corrections import ask as cr_ask
from corrections import forgotten as fg
from corrections import layer as cl
from manual import compile as MC
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Condition, Space

from . import engine as E
from . import plan
from . import reading as R
from . import score as S

F = Fraction
SEC, ONC = plan.SECURITY, plan.ONCALL
T2, T3, AM = "T2_TECHNICAL", "T3_ENGINEERING", "ACCOUNT_MANAGER"
BILL, SS = "BILLING_SPECIALIST", "SELF_SERVICE_DEFLECT"
EXCEPTION, TIER_RULE = "H03", "H01"           # the policy's exception, and the tier's part
K_RUNS = ("k_r1", "k_r2", "k_r3")
L_RUNS = ("l_r1", "l_r2", "l_r3")
RUNS = ("l_r1", "k_r1", "l_r2", "k_r2", "l_r3", "k_r3")   # §2.5's order
HUNDREDTH = 1344                               # a hundredth of the space's 134,400 points
INTERLEAVING = (AM, T3, SS)
CLASSES = ("absent", "then", "last")
PAIR_ORDER = ("silent", "even", "against", "with")   # worst first
ABSTAINS = ("silent", "even")
DRAFTS = ("reaching", "exception", "beyond", "other_queue", "invalid")
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after PLAN_RANKED.md's Stage C. The "
    "expectation in the module's docstring was written and committed before the reading ran. "
    "Not a signed row; no verdict moves.")

frac, share, plain = fg.frac, fg.share, fg.plain


def tag_of(arm: str, rep: int) -> str:
    return plan.tag(arm, rep)


def arm_of(tag: str) -> str:
    return tag.split("_")[0]


def rep_of(tag: str) -> int:
    return int(tag.split("_r")[1])


def median3(xs: Sequence[Fraction]) -> Fraction | None:
    """The middle of an odd number of values; None over nothing."""
    if not xs:
        return None
    ys = sorted(xs)
    return ys[len(ys) // 2] if len(ys) % 2 else (ys[len(ys) // 2 - 1] + ys[len(ys) // 2]) / 2


# ---------------------------------------------------------------------------
# A run's final base
# ---------------------------------------------------------------------------

def walked(record: dict[str, Any], space: Space) -> R.Walk:
    """A record's births, every one taken."""
    w = R.Walk(record, space)
    for idx in sorted(w.born):
        w.birth(idx)
    return w


def base_of(record: dict[str, Any], space: Space, truth: dict[str, int]) -> dict[str, Any]:
    """A run's final base, read as its own engine decides: the queues standing at
    every point, the ranking its votes chose, and both readings."""
    w = walked(record, space)
    queues = w.queues()
    ranking = tuple(w.tally.ranking)
    got = R.read(queues, ranking, truth)
    own = "ranked" if record.get("arm") == plan.RANKED else "rung2"
    return {"walk": w, "queues": queues, "ranking": ranking, "read": got, "own": own,
            "right": got[own]}


def gate_one(base: dict[str, Any], kept: dict[str, Any], keyword: int, n: int) -> bool:
    right = base["right"]
    return bool(base["walk"].sound()
                and F(right.bit_count(), n) == F(kept["space"]["fraction"])
                and [(right & keyword).bit_count(), (right & ~keyword).bit_count()]
                == list(kept["keyword_half"]))


# ---------------------------------------------------------------------------
# A and F: the cases K's ranking took, as the engine held them
# ---------------------------------------------------------------------------

def pair_class(w: str, q: str, votes: Counter) -> str:
    """Between the winner's queue `w` and another standing queue `q`."""
    for_, against = votes[(w, q)], votes[(q, w)]
    if for_ == against == 0:
        return "silent"
    if for_ == against:
        return "even"
    return "against" if against > for_ else "with"


def worst(w: str, present: Sequence[str], votes: Counter) -> str | None:
    """A decision's class: the worst of its pairs."""
    got = [pair_class(w, q, votes) for q in present if q != w]
    return min(got, key=PAIR_ORDER.index) if got else None


def wrong_class(truth: str, present: Sequence[str], last: Sequence[str]) -> str:
    """Why a wrong decision was wrong: no rule of the truth stood, the ranking in
    force erred where the last would not have, or the last errs too."""
    if truth not in present:
        return "absent"
    first = min(present, key=list(last).index)
    return "then" if first == truth else "last"


def taken(record: dict[str, Any], space: Space, corpus: Sequence) -> tuple[list[dict], bool]:
    """Every case the ranking took, read at the base and the votes the engine held
    then; and gate 2."""
    walk = R.Walk(record, space)
    last = tuple(record["ranked"]["final"]["ranking"])
    rows, logs = record["records"], record["ranked"]["cases"]
    ok = len(rows) == len(logs) and all(r["idx"] == i for i, r in enumerate(rows))
    out = []
    for row, logged in zip(rows, logs):
        idx = row["idx"]
        queues = walk.queues()
        here = R.point_of(corpus[idx], space)
        ranking = walk.tally.ranking
        present = [q for q in ranking if queues[q] & here]
        if logged["by"] == E.RANKING:
            w = present[0] if present else None
            runner = present[1] if len(present) > 1 else None
            votes = walk.tally.votes
            decision = S.engines_decision(row)
            ok &= (present == logged["queues"] and walk.tally.state[0] == logged["ranking"]
                   and runner == logged["runner_up"] and decision == w
                   and votes[(w, runner)] == logged["votes_for"]
                   and votes[(runner, w)] == logged["votes_against"])
            right = decision == row["truth"]
            out.append({
                "case": idx, "point": here.bit_length() - 1, "truth": row["truth"],
                "governing": row["truth_rule"], "decision": decision, "queues": present,
                "right": right, "reported": row["cause"] == plan.ERROR,
                "keyword": bool(corpus[idx].has_security_keyword),
                "ranking": walk.tally.state[0], "last_ranking": tuple(ranking) == last,
                "class": None if right else wrong_class(row["truth"], present, last),
                "pairs": worst(w, present, votes),
                "runner_up_pair": pair_class(w, runner, votes) if runner else None})
        else:
            ok &= len(present) == 1 if logged["by"] == E.RUNG2 else not present
        if idx in walk.born:
            walk.birth(idx)
    return out, bool(ok)


def tally_by(rows: Sequence[dict], key) -> dict[str, dict[str, int]]:
    """Cases and wrong ones, by `key`."""
    out: dict[str, dict[str, int]] = {}
    for r in rows:
        k = str(key(r))
        out.setdefault(k, {"cases": 0, "wrong": 0})
        out[k]["cases"] += 1
        out[k]["wrong"] += not r["right"]
    return dict(sorted(out.items()))


def between(r: dict[str, Any]) -> str:
    """The winner's queue and the runner-up's, unordered."""
    return " / ".join(sorted(r["queues"][:2]))


def read_taken(rows: Sequence[dict]) -> dict[str, Any]:
    """One K run's cases, summed."""
    wrong = [r for r in rows if not r["right"]]
    points = Counter(r["point"] for r in wrong)
    return {
        "cases": len(rows), "right": len(rows) - len(wrong), "wrong": len(wrong),
        "wrong_by_class": {c: sum(1 for r in wrong if r["class"] == c) for c in CLASSES},
        "wrong_reported": sum(1 for r in wrong if r["reported"]),
        "by_pair": tally_by(rows, between),
        "by_tenth": tally_by(rows, lambda r: r["case"] // (plan.N // 10)),
        "by_ranking_in_force": tally_by(rows, lambda r: "the last" if r["last_ranking"]
                                        else "another"),
        "by_keyword": tally_by(rows, lambda r: "keyword" if r["keyword"] else "no keyword"),
        "wrong_by_governing": dict(sorted(Counter(r["governing"] for r in wrong).items())),
        "wrong_by_truth_and_decision": dict(sorted(Counter(
            f"{r['truth']} -> {r['decision']}" for r in wrong).items())),
        "wrong_points": {"distinct": len(points),
                         "most_repeated": max(points.values()) if points else 0},
    }


def excess(per_run: dict[str, list[dict]]) -> dict[str, Any] | None:
    """K r2's share of wrong decisions among the cases its ranking took, less K
    r1's and K r3's pooled, split by class."""
    if any(t not in per_run for t in K_RUNS):
        return None
    pooled = per_run["k_r1"] + per_run["k_r3"]

    def shares(rows):
        n = len(rows)
        if not n:
            return None, None
        c = Counter(r["class"] for r in rows if not r["right"])
        return {k: F(c.get(k, 0), n) for k in CLASSES}, F(sum(c.values()), n)

    s2, w2 = shares(per_run["k_r2"])
    sp, wp = shares(pooled)
    if s2 is None or sp is None:
        return None
    return {"total": w2 - wp, "by_class": {k: s2[k] - sp[k] for k in CLASSES}}


def abstentions(rows: Sequence[dict]) -> dict[str, Any]:
    """F at the arrivals: the cases by the class of their worst pair, right and
    wrong, and those the abstaining engine would have left."""
    by = {c: {"cases": 0, "right": 0} for c in PAIR_ORDER}
    runner = {c: 0 for c in PAIR_ORDER}
    for r in rows:
        by[r["pairs"]]["cases"] += 1
        by[r["pairs"]]["right"] += r["right"]
        runner[r["runner_up_pair"]] += 1
    left = [r for r in rows if r["pairs"] in ABSTAINS]
    return {"cases": len(rows), "by_worst_pair": by, "by_runner_up_pair": runner,
            "left_in_conflict": {"cases": len(left), "right": sum(r["right"] for r in left),
                                 "reported_wrong": sum(1 for r in left if not r["right"]
                                                       and r["reported"])}}


# ---------------------------------------------------------------------------
# F over the space
# ---------------------------------------------------------------------------

def standing_sets(queues: dict[str, int], full: int) -> dict[frozenset, int]:
    """The points of the space by the set of queues standing there."""
    parts: dict[frozenset, int] = {frozenset(): full}
    for q in ACTIONS:
        m = queues.get(q, 0)
        new: dict[frozenset, int] = {}
        for s, mask in parts.items():
            a, b = mask & m, mask & ~m
            if a:
                new[s | {q}] = new.get(s | {q}, 0) | a
            if b:
                new[s] = new.get(s, 0) | b
        parts = new
    return parts


def abstentions_over_space(queues: dict[str, int], ranking: Sequence[str], votes: Counter,
                           truth: dict[str, int], full: int) -> dict[str, Any]:
    """F over the space, with the last ranking and the last votes."""
    by = {c: {"points": 0, "right": 0} for c in PAIR_ORDER}
    pairs: Counter = Counter()
    for s, mask in standing_sets(queues, full).items():
        if len(s) < 2:
            continue
        present = [q for q in ranking if q in s]
        w = present[0]
        c = worst(w, present, votes)
        n = mask.bit_count()
        by[c]["points"] += n
        by[c]["right"] += (mask & truth.get(w, 0)).bit_count()
        for q in present[1:]:
            k = pair_class(w, q, votes)
            if k in ABSTAINS:
                pairs[f"{w} / {q}: {k}"] += n
    left = {k: sum(by[c][k] for c in ABSTAINS) for k in ("points", "right")}
    return {"ranking_points": sum(v["points"] for v in by.values()), "by_worst_pair": by,
            "left_in_conflict": left, "abstaining_pairs": dict(sorted(pairs.items()))}


# ---------------------------------------------------------------------------
# B: the nested rules, and the first calls at the exception's tickets
# ---------------------------------------------------------------------------

def region(payload: Any, space: Space) -> int | None:
    """The points of the space a draft covers, or None if it builds none."""
    if not isinstance(payload, dict) or not isinstance(payload.get("conditions"), list) \
            or not payload["conditions"]:
        return None
    try:
        return space.extension([Condition(**c) for c in payload["conditions"]])
    except (TypeError, ValueError, KeyError):
        return None


def draft_class(action: Any, ext: int | None, keyword: int, sec: int, exception: int) -> str:
    """How a draft at a ticket of the exception lies against it."""
    if ext is None:
        return "invalid"
    if action != T2:
        return "other_queue"
    if ext & ~keyword:
        return "beyond"
    if ext & sec:
        return "reaching"
    return "exception"


def conditions_of(c: Sequence[dict]) -> list[list[Any]]:
    return [[x["attr"], x["op"], x["value"]] for x in c]


def attrs(c: Sequence[dict]) -> list[str]:
    return sorted({x["attr"] for x in c})


def first_call(esc: dict[str, Any]) -> dict[str, Any] | None:
    calls = esc.get("calls") or []
    return calls[0] if calls else None


def nested_rules(record: dict[str, Any], base: dict[str, Any], space: Space,
                 truth: dict[str, int], regions: dict[str, int], corpus: Sequence
                 ) -> tuple[list[dict], bool]:
    """Every nested rule of a run, with its birth; and gate 5."""
    eng = base["walk"].engine
    keyword = space.mask["has_security_keyword"][True]
    sec = truth.get(SEC, 0)
    rows = record["records"]
    by_id = {d["rule_id"]: d for d in record["rules"]}
    escs = {e["idx"]: e for e in record["escalations"]}
    handed = record.get("reports_handed") or {}
    ok = True
    out = []
    for rule in sorted(eng.rules, key=lambda r: (r.born_at, r.rule_id)):
        ext = eng.ext[rule.rule_id]
        if rule.action == SEC or ext & ~keyword:
            continue
        d = by_id[rule.rule_id]
        idx = d["born_at"]
        row, esc = rows[idx], escs.get(idx)
        call = first_call(esc) if esc else None
        payload = call.get("payload") if call else None
        draft_ext = region(payload, space)
        is_rule = (isinstance(payload, dict) and payload.get("action") == rule.action
                   and draft_ext == ext)
        ok &= bool(is_rule)
        erred = by_id.get(row.get("engine_rule") or "")
        inside = ext & sec
        out.append({
            "rule_id": rule.rule_id, "queue": rule.action, "born_at": idx,
            "points": ext.bit_count(), "security_points": inside.bit_count(),
            "security_points_wrong": (inside & ~base["right"]).bit_count(),
            "tier_rule_points": (ext & regions[TIER_RULE]).bit_count(),
            "reaches": bool(inside), "whole_exception": ext == regions[EXCEPTION],
            "conditions": conditions_of(d["conditions"]), "attributes": attrs(d["conditions"]),
            "ticket": {a: getattr(corpus[idx], a) for a in ATTRIBUTES},
            "governing": row["truth_rule"], "truth": row["truth"],
            "escalation": esc["kind"] if esc else None, "report": handed.get(str(idx)),
            "engine_decided": row.get("engine_action"), "by_rule": row.get("engine_rule"),
            "by_rule_conditions": conditions_of(erred["conditions"]) if erred else None,
            "copy_of": esc.get("copy_of") if esc else None, "draft_is_the_rule": bool(is_rule)})
    return out, bool(ok)


def exception_calls(record: dict[str, Any], space: Space, truth: dict[str, int],
                    regions: dict[str, int]) -> list[dict]:
    """Every first call at a ticket the exception governs, its draft classed."""
    keyword = space.mask["has_security_keyword"][True]
    sec, exc = truth.get(SEC, 0), regions[EXCEPTION]
    rows = record["records"]
    handed = record.get("reports_handed") or {}
    out = []
    for esc in record["escalations"]:
        idx = esc["idx"]
        if rows[idx]["truth_rule"] != EXCEPTION:
            continue
        call = first_call(esc)
        payload = call.get("payload") if call else None
        ext = region(payload, space)
        action = payload.get("action") if isinstance(payload, dict) else None
        cls = draft_class(action, ext, keyword, sec, exc)
        conds = payload.get("conditions") if isinstance(payload, dict) else None
        out.append({"case": idx, "escalation": esc["kind"], "report": handed.get(str(idx)),
                    "class": cls, "whole": ext == exc, "action": action,
                    "extension": ext, "born": esc["verdict"] == "nacida",
                    "attributes": attrs(conds) if ext is not None else None,
                    "conditions": conditions_of(conds) if ext is not None else None})
    return out


def same_draft_pairs(calls: dict[str, list[dict]], tickets: set[int]) -> dict[str, Any]:
    """For each ticket, its first calls in the runs that asked it as a reported
    error, compared two by two: the same queue and extension, or not."""
    per_ticket = {}
    pairs = same = 0
    for t in sorted(tickets):
        got = [(run, c) for run in RUNS for c in calls.get(run, [])
               if c["case"] == t and c["escalation"] == plan.ERROR]
        n = s = 0
        for (_, a), (_, b) in combinations(got, 2):
            n += 1
            s += a["action"] == b["action"] and a["extension"] == b["extension"] \
                and a["extension"] is not None
        per_ticket[str(t)] = {"runs": [r for r, _ in got], "pairs": n, "same": s,
                              "classes": [c["class"] for _, c in got]}
        pairs, same = pairs + n, same + s
    return {"pairs": pairs, "same": same, "per_ticket": per_ticket}


def read_b(nested: dict[str, list[dict]], calls: dict[str, list[dict]]) -> dict[str, Any]:
    reaching = [dict(r, run=t) for t in RUNS for r in nested.get(t, []) if r["reaches"]]
    tickets = {r["born_at"] for r in reaching}
    told = [c for t in RUNS for c in calls.get(t, [])
            if c["escalation"] == plan.ERROR and c["report"] == T2]
    by_ticket: dict[str, list[str]] = {}
    for t in RUNS:
        for r in nested.get(t, []):
            by_ticket.setdefault(str(r["born_at"]), []).append(f"{t} {r['rule_id']}")
    return {
        "nested": {t: nested.get(t, []) for t in RUNS},
        "nested_by_ticket": dict(sorted(by_ticket.items(), key=lambda kv: int(kv[0]))),
        "reaching": len(reaching),
        "exception_calls": {t: [{k: v for k, v in c.items() if k != "extension"}
                                for c in calls.get(t, [])] for t in RUNS},
        "told_the_queue": {"calls": len(told),
                           "by_class": {k: sum(1 for c in told if c["class"] == k)
                                        for k in DRAFTS},
                           "whole": sum(1 for c in told if c["whole"]),
                           "reaching_with_the_tier": sum(
                               1 for c in told if c["class"] == "reaching"
                               and "customer_tier" in (c["attributes"] or [])),
                           "exception_with_the_tier": sum(
                               1 for c in told if c["class"] == "exception"
                               and "customer_tier" in (c["attributes"] or []))},
        "not_told": {"calls": sum(1 for t in RUNS for c in calls.get(t, [])
                                  if c["escalation"] != plan.ERROR),
                     "by_class": {k: sum(1 for t in RUNS for c in calls.get(t, [])
                                         if c["escalation"] != plan.ERROR and c["class"] == k)
                                  for k in DRAFTS}},
        "same_ticket": same_draft_pairs(calls, tickets),
    }


# ---------------------------------------------------------------------------
# C: the other half, K against L under the same draw
# ---------------------------------------------------------------------------

def half(base: dict[str, Any], truth: dict[str, int], mask: int) -> dict[str, Any]:
    """A base over the points of `mask`, by how each is decided, and by true queue."""
    rd = base["read"]
    conflict, decided = rd["conflict"] & mask, rd["decided"] & mask
    right = base["right"] & mask
    parts = {"right": right,
             "rung2_right": rd["rung2"] & mask,
             "ranking_right": (rd["ranked"] & rd["conflict"] & mask
                               if base["own"] == "ranked" else 0),
             "conflict": conflict,
             "undecided": mask & ~decided,
             "decided_wrong": decided & ~rd["conflict"] & ~rd["rung2"] & mask}
    out = {k: v.bit_count() for k, v in parts.items()}
    out["points"] = mask.bit_count()
    out["by_queue"] = {q: {k: (v & truth.get(q, 0)).bit_count() for k, v in parts.items()}
                       for q in ACTIONS}
    return out


CAUSES = (plan.IMPASSE, plan.ERROR, plan.CONFLICT)


def by_birth(base: dict[str, Any], record: dict[str, Any], mask: int,
             truth: dict[str, int]) -> dict[str, Any]:
    """Added after the first run. The points of `mask` a base decides wrong, one
    queue standing, by how the rules that decide them were born: at an impasse,
    at a reported error, or at a conflict the loop asked about. A point is
    `conflict` when a rule born at a conflict stands there, and `only_conflict`
    when every rule that stands there was."""
    cause = {e["idx"]: e["kind"] for e in record["escalations"]}
    rd = base["read"]
    wrong = rd["decided"] & ~rd["conflict"] & ~rd["rung2"] & mask
    born = {c: 0 for c in CAUSES}
    for r in base["walk"].engine.rules:
        born[cause[r.born_at]] |= base["walk"].und[r.rule_id] & wrong
    others = born[plan.IMPASSE] | born[plan.ERROR]
    only = born[plan.CONFLICT] & ~others
    return {"wrong": wrong.bit_count(),
            **{c.lower(): born[c].bit_count() for c in CAUSES},
            "only_conflict": only.bit_count(),
            "conflict_by_queue": {q: (born[plan.CONFLICT] & truth.get(q, 0)).bit_count()
                                  for q in ACTIONS},
            "masks": {"conflict": born[plan.CONFLICT], "wrong": wrong}}


def read_c(bases: dict[str, dict], truth: dict[str, int], other: int,
           records: dict[str, dict] | None = None) -> dict[str, Any]:
    out = {}
    for k in range(1, plan.REPS + 1):
        kt, lt = tag_of(plan.RANKED, k), tag_of(plan.CONTROL, k)
        if kt not in bases or lt not in bases:
            continue
        kb, lb = bases[kt], bases[lt]
        kh, lh = half(kb, truth, other), half(lb, truth, other)
        l_conflict = lb["read"]["conflict"] & other
        k_on_it = kb["right"] & l_conflict
        out[f"r{k}"] = {
            "k": kh, "l": lh, "gain": kh["right"] - lh["right"],
            "gain_by_queue": {q: kh["by_queue"][q]["right"] - lh["by_queue"][q]["right"]
                              for q in ACTIONS},
            "l_conflict_k_decides_right": {
                "points": k_on_it.bit_count(),
                "by_ranking": (k_on_it & kb["read"]["conflict"]).bit_count(),
                "by_queue": {q: (k_on_it & truth.get(q, 0)).bit_count() for q in ACTIONS}}}
        if records and lt in records and kt in records:
            # added after the first run: what decides wrong the points L errs on
            lw = by_birth(lb, records[lt], other, truth)
            kw = by_birth(kb, records[kt], other, truth)
            gain_points = lw["masks"]["wrong"] & kb["right"]
            out[f"r{k}"]["decided_wrong_by_birth"] = {
                "l": {x: v for x, v in lw.items() if x != "masks"},
                "k": {x: v for x, v in kw.items() if x != "masks"},
                "l_wrong_k_right": {
                    "points": gain_points.bit_count(),
                    "a_conflict_birth_stands": (gain_points & lw["masks"]["conflict"]).bit_count(),
                    "by_queue": {q: (gain_points & truth.get(q, 0)).bit_count()
                                 for q in ACTIONS}}}
    return out


# ---------------------------------------------------------------------------
# D: the pair in K's bases
# ---------------------------------------------------------------------------

def swapped(ranking: Sequence[str], a: str, b: str) -> tuple[str, ...]:
    r = list(ranking)
    i, j = r.index(a), r.index(b)
    r[i], r[j] = r[j], r[i]
    return tuple(r)


def pair_decides(queues: dict[str, int], ranking: Sequence[str], a: str, b: str) -> int:
    """Where rules of both queues stand and no queue ranked above both does."""
    top = min(list(ranking).index(a), list(ranking).index(b))
    blocked = 0
    for q in list(ranking)[:top]:
        blocked |= queues.get(q, 0)
    return queues.get(a, 0) & queues.get(b, 0) & ~blocked


def read_d(base: dict[str, Any], truth: dict[str, int]) -> dict[str, Any]:
    q, ranking = base["queues"], base["ranking"]
    decides = pair_decides(q, ranking, T3, AM)
    other_way = swapped(ranking, T3, AM)
    then = R.read(q, other_way, truth)["ranked"]
    am = truth.get(AM, 0)
    beside = am & q.get(T3, 0) & q.get(AM, 0)
    return {
        "ranking": list(ranking), "t3_above": ranking.index(T3) < ranking.index(AM),
        "meet": (q.get(T3, 0) & q.get(AM, 0)).bit_count(),
        "pair_decides": {"points": decides.bit_count(),
                         **{k: (decides & truth.get(x, 0)).bit_count()
                            for k, x in (("account_manager", AM), ("t3_engineering", T3))},
                         "other": (decides & ~am & ~truth.get(T3, 0)).bit_count()},
        "exchanged": {"ranking": list(other_way), "right": then.bit_count(),
                      "change": then.bit_count() - base["right"].bit_count(),
                      "account_manager_right": (then & am).bit_count()},
        "account_manager": {"points": am.bit_count(), "right": (base["right"] & am).bit_count(),
                            "t3_beside": beside.bit_count()},
    }


# ---------------------------------------------------------------------------
# E: the at-once answers at all of a run's labels
# ---------------------------------------------------------------------------

def at_all_labels(record: dict[str, Any], session: dict[str, Any]
                  ) -> tuple[int, list[tuple[int, dict]]]:
    pairs = cr_ask.labelled(record)
    j = len(pairs)
    return j, [(k, row) for cj, k, row in cl.chosen(session) if cj == j]


def answer_read(payload: Any, truth: dict[str, int], keyword: int) -> dict[str, Any]:
    inst = MC.install(MC.rules_of(payload)[0], MI.space())
    right = MI.right_mask(inst.engine)
    return {"right": right, "points": right.bit_count(),
            "recall": {q: share((right & truth.get(q, 0)).bit_count(),
                                truth.get(q, 0).bit_count()) for q in ACTIONS},
            "halves": [(right & keyword).bit_count(), (right & ~keyword).bit_count()],
            "rules": len(inst.rules)}


def make_up(record: dict[str, Any]) -> dict[str, Any]:
    """A run's labels by queue, and by the hidden rule governing each ticket."""
    pairs = cr_ask.labelled(record)
    rows = record["records"]
    by_rule: dict[str, Counter] = {}
    for i, q in pairs:
        by_rule.setdefault(q, Counter())[rows[i]["truth_rule"]] += 1
    return {"labels": len(pairs), "by_queue": dict(sorted(Counter(q for _, q in pairs).items())),
            "by_queue_and_rule": {q: dict(sorted(c.items())) for q, c in sorted(by_rule.items())}}


def read_e(records: dict[str, dict], sessions: dict[str, dict], bases: dict[str, dict],
           truth: dict[str, int], keyword: int) -> tuple[dict[str, Any], dict[str, list]]:
    """Each run's answers at all of its labels; their medians; and what gate 3
    compares."""
    out, rights = {}, {}
    for t in RUNS:
        if t not in records or t not in sessions:
            continue
        j, chosen = at_all_labels(records[t], sessions[t])
        reads = [(k, answer_read(row["payload"], truth, keyword)) for k, row in chosen]
        rights[t] = reads
        med = {q: median3([r["recall"][q] for _, r in reads if r["recall"][q] is not None])
               for q in ACTIONS}
        order = sorted(reads, key=lambda kr: (kr[1]["points"], kr[0]))
        mid_k, mid = order[len(order) // 2] if order else (None, None)
        out[t] = {"labels": j, "answers": [{"ask": k, "points": r["points"],
                                            "halves": r["halves"], "rules": r["rules"],
                                            "recall": {q: frac(v) for q, v in r["recall"].items()}}
                                           for k, r in reads],
                  "median_recall": {q: frac(v) for q, v in med.items()},
                  "median_answer": None if mid is None else {"ask": mid_k, "points": mid["points"],
                                                             "halves": mid["halves"]},
                  "make_up": make_up(records[t])}
        if mid is not None and t in bases:
            loop = bases[t]["right"]
            beyond = [((mid["right"] & m).bit_count() - (loop & m).bit_count())
                      for m in (keyword, ~keyword)]
            out[t]["beyond_the_loop"] = {"keyword_half": beyond[0], "other_half": beyond[1],
                                         "loop_halves": [(loop & keyword).bit_count(),
                                                         (loop & ~keyword).bit_count()]}
    return out, rights


def gate_three(e: dict[str, Any], rights: dict[str, list], score: dict[str, Any],
               n: int) -> dict[str, bool]:
    """Each run's answers at all of its labels decide the shares Stage C keeps,
    ask by ask."""
    got = {}
    for t, reads in rights.items():
        kept = [c["at_once"]["asks"] for c in score["RK-g"]["curves"].get(t) or []
                if c["labels"] == e[t]["labels"] and c.get("at_once")]
        got[t] = bool(len(kept) == 1 and len(kept[0]) == len(reads) == 3 and all(
            F(a["space"]["fraction"]) == F(r["points"], n) for a, (_, r) in zip(kept[0], reads)))
    return got


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    A, B, C = readings.get("A") or {}, readings.get("B") or {}, readings.get("C") or {}
    D, Ex, Fr = readings.get("D") or {}, readings.get("E") or {}, readings.get("F") or {}
    runs_a = A.get("runs") or {}

    # A
    ex = A.get("excess")
    total = None if not ex else F(ex["total"]["fraction"])
    a1 = bool(total is not None and total > 0
              and F(ex["by_class"]["last"]["fraction"]) > total / 2)
    k2 = runs_a.get("k_r2")
    pair = " / ".join(sorted((BILL, T2)))
    a2 = bool(k2 and k2["wrong"] and 2 * k2["by_pair"].get(pair, {}).get("wrong", 0) > k2["wrong"])
    a3 = bool(k2 and k2["wrong"] and 2 * k2["wrong_points"]["distinct"] > k2["wrong"])

    # B
    reaching = [r for t in RUNS for r in (B.get("nested") or {}).get(t, []) if r["reaches"]]
    b1 = bool(reaching) and all(r["governing"] == EXCEPTION for r in reaching)
    b2 = bool(reaching) and all(r["escalation"] == plan.ERROR and r["report"] == T2
                                for r in reaching)
    b3 = bool(reaching) and all(r["tier_rule_points"] > 0 for r in reaching)
    told = (B.get("told_the_queue") or {}).get("by_class") or {}
    b4 = told.get("reaching", 0) > told.get("exception", 0)
    same = B.get("same_ticket") or {}
    b5 = bool(same.get("pairs")) and 2 * same["same"] > same["pairs"]

    # C
    def c_each(test) -> bool:
        return len(C) == plan.REPS and all(test(v) for v in C.values())

    c1 = c_each(lambda v: v["k"]["ranking_right"] > 0 and 2 * sum(
        v["k"]["by_queue"][q]["ranking_right"] for q in INTERLEAVING) > v["k"]["ranking_right"])
    c2 = c_each(lambda v: 2 * v["l"]["conflict"] > v["l"]["points"] - v["l"]["right"])
    c3 = c_each(lambda v: v["l"]["conflict"] > 0
                and 2 * v["l_conflict_k_decides_right"]["points"] > v["l"]["conflict"])

    # D
    def d_each(test) -> bool:
        return all(t in D for t in K_RUNS) and all(test(D[t]) for t in K_RUNS)

    d1 = d_each(lambda v: v["pair_decides"]["points"] < HUNDREDTH)
    d2 = d_each(lambda v: v["pair_decides"]["account_manager"] > v["pair_decides"]["t3_engineering"])
    d3 = d_each(lambda v: 10 * v["account_manager"]["t3_beside"] < v["account_manager"]["points"])

    # E
    def med(t, q):
        x = ((Ex.get(t) or {}).get("median_recall") or {}).get(q)
        return None if x is None else F(x["fraction"])

    def above_all(q) -> bool:
        mine = med("k_r2", q)
        others = [med(t, q) for t in RUNS if t != "k_r2"]
        return mine is not None and len(others) == len(RUNS) - 1 and \
            all(o is not None and mine > o for o in others)

    e1 = above_all(SEC)
    bl = (Ex.get("k_r2") or {}).get("beyond_the_loop")
    e2 = bool(bl) and bl["keyword_half"] + bl["other_half"] > 0 and \
        2 * bl["keyword_half"] > bl["keyword_half"] + bl["other_half"]
    e3 = above_all(ONC)

    # F
    arr, spc = Fr.get("arrivals") or {}, Fr.get("space") or {}

    def f_each(d, test) -> bool:
        return all(t in d for t in K_RUNS) and all(test(d[t]) for t in K_RUNS)

    f1 = f_each(arr, lambda v: v["cases"] > 0 and 10 * v["left_in_conflict"]["cases"] < v["cases"])
    f2 = f_each(spc, lambda v: v["ranking_points"] > 0
                and 10 * v["left_in_conflict"]["points"] < v["ranking_points"])
    f3 = f_each(spc, lambda v: v["left_in_conflict"]["points"] > 0
                and 2 * v["left_in_conflict"]["right"] > v["left_in_conflict"]["points"])

    def out(clause, what, holds, reading):
        return {"clause": clause, "what": what, "reading": reading, "holds": bool(holds)}

    return [
        out("A1", "the class `last` carries more than half of K r2's excess of wrong decisions "
                  "over K r1's and K r3's pooled", a1, ex),
        out("A2", "in K r2, the pair BILLING_SPECIALIST and T2_TECHNICAL, as winner and "
                  "runner-up either way, carries more than half of the wrong decisions", a2,
            None if not k2 else {"wrong": k2["wrong"], "pair": k2["by_pair"].get(pair)}),
        out("A3", "in K r2, the wrong decisions fall on more distinct points of the space than "
                  "half their number", a3,
            None if not k2 else {"wrong": k2["wrong"], "points": k2["wrong_points"]}),
        out("B1", "in the six runs, every nested rule that reaches was born at a ticket of H03",
            b1, {"reaching": len(reaching),
                 "governing": dict(Counter(r["governing"] for r in reaching))}),
        out("B2", "every such birth was a reported error whose report named T2_TECHNICAL", b2,
            {"by_escalation_and_report": dict(Counter(f"{r['escalation']} {r['report']}"
                                                      for r in reaching))}),
        out("B3", "every such rule holds points of H01's region", b3,
            {"holding_h01": sum(1 for r in reaching if r["tier_rule_points"] > 0),
             "reaching": len(reaching)}),
        out("B4", "of the first calls at tickets of H03 told T2_TECHNICAL whose drafts lie inside "
                  "the keyword half, more reach than stay inside H03's region", b4, told),
        out("B5", "over the tickets that begot a reaching rule, more than half of the pairs of "
                  "runs that asked the ticket as a reported error drafted the same queue and "
                  "extension at its first call", b5,
            {"pairs": same.get("pairs"), "same": same.get("same")}),
        out("C1", "in every draw, more than half of the other half's points K's ranking decides "
                  "right are ACCOUNT_MANAGER's, T3_ENGINEERING's and SELF_SERVICE_DEFLECT's", c1,
            {d: {"ranking_right": v["k"]["ranking_right"],
                 "interleaving": sum(v["k"]["by_queue"][q]["ranking_right"]
                                     for q in INTERLEAVING)} for d, v in C.items()}),
        out("C2", "in every draw, the points L leaves in conflict are more than half of those it "
                  "does not decide right in the other half", c2,
            {d: {"conflict": v["l"]["conflict"], "not_right": v["l"]["points"] - v["l"]["right"]}
             for d, v in C.items()}),
        out("C3", "in every draw, K decides right more than half of the other half's points L "
                  "leaves in conflict", c3,
            {d: {"l_conflict": v["l"]["conflict"],
                 "k_right_there": v["l_conflict_k_decides_right"]["points"]}
             for d, v in C.items()}),
        out("D1", "in every K run, the pair decides fewer than 1,344 points", d1,
            {t: D[t]["pair_decides"]["points"] for t in K_RUNS if t in D}),
        out("D2", "in every K run, where the pair decides, ACCOUNT_MANAGER's points outnumber "
                  "T3_ENGINEERING's", d2,
            {t: [D[t]["pair_decides"]["account_manager"], D[t]["pair_decides"]["t3_engineering"]]
             for t in K_RUNS if t in D}),
        out("D3", "in every K run, a rule of T3_ENGINEERING stands undefeated beside one of "
                  "ACCOUNT_MANAGER on fewer than a tenth of ACCOUNT_MANAGER's points", d3,
            {t: [D[t]["account_manager"]["t3_beside"], D[t]["account_manager"]["points"]]
             for t in K_RUNS if t in D}),
        out("E1", "at all of its labels, K r2's median at-once recall of SECURITY_INCIDENT is "
                  "above every other run's", e1,
            {t: frac(med(t, SEC)) for t in RUNS if t in Ex}),
        out("E2", "more than half of what K r2's median answer decides right beyond its loop's "
                  "final base lies in the keyword half", e2, bl),
        out("E3", "at all of its labels, K r2's median at-once recall of ONCALL_ESCALATION is "
                  "above every other run's", e3,
            {t: frac(med(t, ONC)) for t in RUNS if t in Ex}),
        out("F1", "in every K run, the abstaining engine would have left in conflict fewer than a "
                  "tenth of the cases the ranking took", f1,
            {t: [arr[t]["left_in_conflict"]["cases"], arr[t]["cases"]] for t in K_RUNS
             if t in arr}),
        out("F2", "in every K run, it would leave in conflict fewer than a tenth of the points the "
                  "ranking decides", f2,
            {t: [spc[t]["left_in_conflict"]["points"], spc[t]["ranking_points"]] for t in K_RUNS
             if t in spc}),
        out("F3", "in every K run, the ranking decides right more than half of the points it "
                  "would leave", f3,
            {t: [spc[t]["left_in_conflict"]["right"], spc[t]["left_in_conflict"]["points"]]
             for t in K_RUNS if t in spc}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "readings.json"


def read_inputs() -> tuple[dict[str, dict], dict[str, dict], dict[str, Any]]:
    records = {tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
               for a, k in plan.schedule() if plan.run_path(a, k).exists()}
    sessions = {t: json.loads(plan.ask_path(t).read_text()) for t in records
                if plan.ask_path(t).exists()}
    score = json.loads(plan.score_path().read_text())
    return records, sessions, score


def read_everything(records: dict[str, dict], sessions: dict[str, dict],
                    score: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space, truth = MI.space(), MI.space_truth()
    corpus = list(MI.corpus())
    n, full = space.n, (1 << space.n) - 1
    keyword = space.mask["has_security_keyword"][True]
    other = full & ~keyword
    regions = {h: MI.hidden_regions()[h]["mask"] for h in (EXCEPTION, TIER_RULE)}
    kept = score["RK-g"]["runs"]
    gates: list[dict[str, Any]] = []
    bases, nested, calls, per_run_taken = {}, {}, {}, {}
    taken_ok, nested_ok, draft_ok, last_ok = {}, {}, {}, {}
    for t in RUNS:
        if t not in records:
            continue
        rec = records[t]
        bases[t] = base_of(rec, space, truth)
        gates.append({"gate": 1, "run": t, "what": "the base is Stage C's",
                      "passes": gate_one(bases[t], kept[t], keyword, n)})
        nested[t], draft_ok[t] = nested_rules(rec, bases[t], space, truth, regions, corpus)
        kept_nested = [{k: x[k] for k in ("rule_id", "queue", "born_at", "points",
                                          "security_points", "security_points_wrong")}
                       for x in kept[t]["nested_in_the_keyword"]]
        mine = [{k: x[k] for k in ("rule_id", "queue", "born_at", "points", "security_points",
                                   "security_points_wrong")} for x in nested[t]]
        nested_ok[t] = sorted(mine, key=lambda x: x["rule_id"]) == \
            sorted(kept_nested, key=lambda x: x["rule_id"])
        gates.append({"gate": 4, "run": t, "what": "the nested rules are Stage C's",
                      "passes": nested_ok[t]})
        gates.append({"gate": 5, "run": t, "what": "a born draft is its rule",
                      "passes": draft_ok[t]})
        calls[t] = exception_calls(rec, space, truth, regions)
        if arm_of(t) == plan.RANKED:
            per_run_taken[t], taken_ok[t] = taken(rec, space, corpus)
            gates.append({"gate": 2, "run": t, "what": "the ranking's cases are the record's",
                          "passes": taken_ok[t]})
            last_ok[t] = (list(bases[t]["ranking"]) == rec["ranked"]["final"]["ranking"]
                          == kept[t]["ranking"]["final"])
            gates.append({"gate": 6, "run": t, "what": "the last ranking is the record's",
                          "passes": last_ok[t]})
    e, rights = read_e(records, sessions, bases, truth, keyword)
    for t, ok in gate_three(e, rights, score, n).items():
        gates.append({"gate": 3, "run": t, "what": "the at-once answers are Stage C's",
                      "passes": ok})
    ex = excess(per_run_taken)
    a = {"runs": {t: read_taken(rows) for t, rows in per_run_taken.items()},
         "cases": {t: rows for t, rows in per_run_taken.items()},
         "excess": None if ex is None else
         {"total": frac(ex["total"]), "by_class": {k: frac(v) for k, v in ex["by_class"].items()}}}
    b = read_b(nested, calls)
    c = read_c(bases, truth, other, records)
    d = {t: read_d(bases[t], truth) for t in K_RUNS if t in bases}
    f = {"arrivals": {t: abstentions(rows) for t, rows in per_run_taken.items()},
         "space": {t: abstentions_over_space(bases[t]["queues"], bases[t]["ranking"],
                                             bases[t]["walk"].tally.votes, truth, full)
                   for t in K_RUNS if t in bases}}
    return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f}, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Six readings Stage C left free (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/readings.py writes {record_path()}")
    records, sessions, score = read_inputs()
    readings, gates = read_everything(records, sessions, score)
    for g in gates:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(RUNS) and len(sessions) == len(RUNS)
    if not complete:
        print("  missing records or sessions")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0 if complete and all(g["passes"] for g in gates) else 1
    if not complete or not all(g["passes"] for g in gates):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    expectation = read_expectation(readings)
    record_path().write_text(json.dumps(st._rounded({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {"score": str(plan.score_path()),
                   "score_from": score["_env"].get("git_commit"),
                   "runs": {t: str(plan.run_path(arm_of(t), rep_of(t))) for t in RUNS},
                   "sessions": {t: str(plan.ask_path(t)) for t in RUNS}},
        "surface": "the arrivals as each K run's engine decided them (A, F), the whole space of "
                   "134,400 points as each run's final base decides it on its own engine, by "
                   "half and by queue (B, C, D, F), and each run's at-once answers at all of "
                   "its labels, installed as Stage C installs them (E)",
        "constants": {"exception": EXCEPTION, "tier_rule": TIER_RULE, "hundredth": HUNDREDTH,
                      "interleaving": list(INTERLEAVING), "abstains": list(ABSTAINS)},
        "gates": gates,
        "readings": readings,
        "expectation": expectation,
    }), indent=2, default=plain) + "\n")
    for cl_ in expectation:
        print(f"  {cl_['clause']}: {'holds' if cl_['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
