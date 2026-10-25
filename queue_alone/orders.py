"""
WHERE THE ORDER ERRORS GO. `FINDINGS_QUEUE_ALONE.md`, read beside the verdicts,
found that asked for the queue alone the model almost never names a queue no
matching rule gives, and still names a lower matching rule's queue on more than
a fifth of its answers at level 3. `IDEAS.md` carries the next question under
*What `PLAN_QUEUE_ALONE.md` opens*: which lower rule those answers follow, and
whether they lean to the more specific rule. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**Every valid answer of the three arms at level 3**, two per decision, from the
two passes, under §0's rule G: an answer counts when its `action` is one of the
eight queues and Baidu served it. They are read against **the 29 rules from
level 3's frozen text**, through `queue_alone/rules.py`, which is how §5.6 read
them. No oracle is read.

For a decision's ticket, its matching rules in the list's order are `r₁, r₂,
…`. `r₁` gives the truth. An **order error** is an answer that is not `r₁`'s
queue and is the queue of some lower matching rule.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Which lower rule an order error follows.** The rule it follows is the
     highest matching rule below `r₁` that gives its queue. Read three ways:
     - its rank among the ticket's matching rules: second, third, and so on;
     - whether it is **the runner-up**, the first matching rule that gives
       another queue than `r₁`'s;
     - whether it is **the catch-all**, `H29`, which matches every ticket, so
       that no rule above it gives that queue.
  B. **Specificity.** Whether an order error names the queue of the matching
     rule with the most conditions, as rung 1's engine arbitrated. And on the
     decisions where that rule's queue is not `r₁`'s, how often each arm names
     it, `r₁`'s, or another.
  C. **Which rule is skipped.** The order errors by `r₁`, the rule that governs
     the ticket and was passed over, beside each arm's answers on the tickets
     that rule governs.

Every question is read for the three arms. The rule and plain arms are set side
by side: the plain question removed nearly all the matching errors, and this
asks whether it moved where the order errors go.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The classes come back.** Counted again here, each arm's first, order and
     matching answers at level 3 are `score.json`'s `classes_at_L3`.
  2. **The copiers come back.** The most-conditions copier and the commonest-
     queue copier are right on the decisions `sample.json` records.
  3. **The catch-all is total, and the first match is the truth.** `H29`
     matches every level-3 ticket, and `r₁` gives every decision its truth.
  4. **The order errors partition.** Every order error has a lower matching
     rule that gives its queue, and a runner-up; first, order and matching add
     up to each arm's answers.

It refuses to write if any fails, and while `PLAN_QUEUE_ALONE.md` is unsigned.
`--dry-run` runs the four, prints pass or fail, and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  O1. **At least half of the plain arm's order errors name the runner-up's
      queue.** The model stops one rule late more often than it lands anywhere
      lower.
  O2. **Fewer than one plain-arm order error in five follows the catch-all.**
      The errors are not a fall to the default.
  O3. **On the decisions where the most-conditions rule gives another queue
      than `r₁`'s, the plain arm names the most-conditions queue on at least
      half of its answers there.** It reads the rule that names more of the
      ticket.
  O4. **The three governing rules with the most plain-arm order errors carry at
      least half of them.** The errors sit on a few rules, not across the list.
  O5. **The rule and plain arms send their order errors to the runner-up at
      shares within 0.15 of each other.** The plain question removed the
      matching errors without changing where the order errors go.

So the drafter expects the order errors to be one rule late, on a few rules,
leaning to the more specific rule, and the same in both arms. The drafter
trusts O2 most and O3 least: a specificity reading is right on most decisions
(Stage A), and the model is right less often than it, so the model is not
simply reading by specificity.

**What the drafter had seen**:
- `FINDINGS_QUEUE_ALONE.md` whole, `score.json`'s verdicts and `QA-g`, and
  `sample.json`'s references: §5.6's classes by arm, the two copiers, the
  number of matching rules per decision, the rank of each decision's first
  match, and the rare queues by arm;
- the 29 rules, and `harness/ceiling_check.py`'s comments on their layers.

**What the drafter had not seen**:
- which lower rule any order error follows, its rank, or whether it is the
  runner-up, the catch-all or the most specific;
- which governing rule any order error passes over;
- any arm's answers on the decisions where the most-conditions rule gives
  another queue.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-10-25, after `PLAN_QUEUE_ALONE.md`
closed. The expectation above was written and committed before any figure of
the reading was computed. Not a signed row, not on `STATUS.md`'s scoreboard,
and no verdict moves. Zero API calls.

Usage:  python3 -m queue_alone.orders --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m queue_alone.orders
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

from harness.provenance import describe, environment

from . import plan, population, rules
from . import score as S

F = Fraction
ARMS = ("t", "i", "q")
CATCH_ALL = "H29"                  # `severity gte 1`: every ticket matches it

# The expectation's lines.
O1_RUNNER_UP = F(1, 2)
O2_CATCH_ALL = F(1, 5)
O3_SPECIFIC = F(1, 2)
O4_TOP_THREE = F(1, 2)
O5_GAP = F(3, 20)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-10-25, after PLAN_QUEUE_ALONE.md "
    "closed. The expectation in the module's docstring was written and committed "
    "before any figure of the reading was computed. Not a signed row; no verdict "
    "moves.")


def record_path() -> Path:
    return plan.OUT / "orders.json"


# ---------------------------------------------------------------------------
# One answer, read against the ticket's matching rules
# ---------------------------------------------------------------------------

def runner_up(hit: Sequence[rules.Rule]) -> rules.Rule | None:
    """The first matching rule that gives another queue than the first's."""
    return next((r for r in hit[1:] if r.queue != hit[0].queue), None)


def follows(answer: str, hit: Sequence[rules.Rule]) -> tuple[int, rules.Rule] | None:
    """The highest matching rule below the first that gives `answer`, with its
    rank among the matching rules, counted from 1; `None` for no such rule."""
    for k, r in enumerate(hit[1:], start=2):
        if r.queue == answer and answer != hit[0].queue:
            return k, r
    return None


def read_answer(answer: str, ticket: dict[str, Any], rs: Sequence[rules.Rule]) -> dict[str, Any]:
    """Everything this reading asks of one answer."""
    hit = rules.matching(ticket, tuple(rs))
    out: dict[str, Any] = {"class": rules.classify(answer, ticket, tuple(rs)),
                           "governing": hit[0].id if hit else None,
                           "most_specific": answer == rules.most_conditions_queue(ticket, tuple(rs))}
    f = follows(answer, hit)
    if f is not None:
        rank, r = f
        up = runner_up(hit)
        out.update({"rank": rank, "follows": r.id, "runner_up": up is not None and r is up,
                    "catch_all": r.id == CATCH_ALL})
    return out


# ---------------------------------------------------------------------------
# The three questions, over an arm's answers
# ---------------------------------------------------------------------------

def share(k: int, n: int) -> Fraction | None:
    return F(k, n) if n else None


def arm_reading(answers: list[tuple[str, dict[str, Any], str]],
                rs: Sequence[rules.Rule]) -> dict[str, Any]:
    """`answers` holds (answer, ticket, truth) for one arm at level 3."""
    classes: Counter = Counter()
    rank: Counter = Counter()
    follow: Counter = Counter()
    governing_errors: Counter = Counter()
    governing_answers: Counter = Counter()
    up = catch = specific = 0
    for a, ticket, _ in answers:
        got = read_answer(a, ticket, rs)
        classes[got["class"]] += 1
        governing_answers[got["governing"]] += 1
        if got["class"] != "order":
            continue
        rank[got["rank"]] += 1
        follow[got["follows"]] += 1
        governing_errors[got["governing"]] += 1
        up += got["runner_up"]
        catch += got["catch_all"]
        specific += got["most_specific"]
    n = classes["order"]
    top = governing_errors.most_common()
    return {
        "answers": len(answers), "classes": dict(classes), "order_errors": n,
        "rank": {str(k): v for k, v in sorted(rank.items())},
        "runner_up": {"count": up, "share": S.frac(share(up, n))},
        "catch_all": {"count": catch, "share": S.frac(share(catch, n))},
        "most_specific": {"count": specific, "share": S.frac(share(specific, n))},
        "follows": dict(follow.most_common()),
        "governing": [{"rule": g, "order_errors": c, "answers": governing_answers[g]}
                      for g, c in top],
        "top_three": {"rules": [g for g, _ in top[:3]],
                      "share": S.frac(share(sum(c for _, c in top[:3]), n))},
    }


def specificity(answers: list[tuple[str, dict[str, Any], str]],
                rs: Sequence[rules.Rule]) -> dict[str, Any]:
    """On the decisions where the most-conditions rule's queue is not the
    first's: how often the arm names it, the first's, or another."""
    c: Counter = Counter()
    for a, ticket, y in answers:
        mc = rules.most_conditions_queue(ticket, tuple(rs))
        if mc == y:
            continue
        c["answers"] += 1
        c["most_specific" if a == mc else "first" if a == y else "other"] += 1
    n = c["answers"]
    return {**dict(c), "most_specific_share": S.frac(share(c["most_specific"], n))}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(d: dict | None) -> Fraction | None:
    return Fraction(d["fraction"]) if d else None


def read_expectation(arms: dict[str, dict], spec: dict[str, dict]) -> list[dict[str, Any]]:
    out = []

    def clause(c: str, holds: Any, reading: str) -> None:
        out.append({"clause": c, "holds": bool(holds), "reading": reading})

    q, t = arms["q"], arms["t"]

    def fmt(x: Fraction | None) -> str:
        return "none" if x is None else f"{float(x):.4f}"

    v = value(q["runner_up"]["share"])
    clause("O1", v is not None and v >= O1_RUNNER_UP,
           f"{q['runner_up']['count']} of {q['order_errors']} plain-arm order errors "
           f"name the runner-up's queue, {fmt(v)}")
    v = value(q["catch_all"]["share"])
    clause("O2", v is not None and v < O2_CATCH_ALL,
           f"{q['catch_all']['count']} of {q['order_errors']} follow the catch-all, {fmt(v)}")
    v = value(spec["q"]["most_specific_share"])
    clause("O3", v is not None and v >= O3_SPECIFIC,
           f"{spec['q'].get('most_specific', 0)} of {spec['q'].get('answers', 0)} plain-arm "
           f"answers name the most-conditions queue where it is not the first's, {fmt(v)}")
    v = value(q["top_three"]["share"])
    clause("O4", v is not None and v >= O4_TOP_THREE,
           f"{', '.join(q['top_three']['rules'])} carry {fmt(v)} of the plain arm's "
           f"order errors")
    a, b = value(t["runner_up"]["share"]), value(q["runner_up"]["share"])
    clause("O5", a is not None and b is not None and abs(a - b) <= O5_GAP,
           f"runner-up shares: rule arm {fmt(a)}, plain arm {fmt(b)}")
    return out


# ---------------------------------------------------------------------------

def level3_answers(units: list[S.Unit], design: population.Design
                   ) -> dict[str, list[tuple[str, dict[str, Any], str]]]:
    out: dict[str, list] = {arm: [] for arm in ARMS}
    for u in units:
        if u.level != 3:
            continue
        ticket = design.decisions[u.id].prompt.case.as_dict()
        for arm in ARMS:
            for a in getattr(u, arm):
                if a is not None:
                    out[arm].append((a, ticket, u.y))
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("queue_alone/orders.py writes its reading")
    t0 = time.time()
    scored = json.loads(plan.score_path().read_text())
    staged = json.loads(plan.sample_path().read_text())
    recs = {s: S.read(s) for s in plan.SESSIONS[1:]}
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]} for s, rec in recs.items()}
    design = population.build()
    lab = S.labels()
    units = S.units(design, by_pass, lab)
    rs = rules.rules()
    answers = level3_answers(units, design)
    off: dict[str, list[str]] = defaultdict(list)

    print("=" * 78)
    print("PLAN_QUEUE_ALONE.md — WHERE THE ORDER ERRORS GO — POST-RUN")
    print("=" * 78)

    # Gate 1: the classes come back.
    recorded = scored["QA-g"]["classes_at_L3"]
    for arm in ARMS:
        c = Counter(rules.classify(a, ticket, rs) for a, ticket, _ in answers[arm])
        mine = {**dict(c), "answers": len(answers[arm])}
        theirs = {k: recorded[arm].get(k, 0) for k in ("first", "order", "matching", "answers")}
        if {k: mine.get(k, 0) for k in theirs} != theirs:
            off["1"].append(arm)

    # Gate 2: the copiers come back.
    l3 = [(i, e) for i, e in sorted(design.decisions.items()) if e.level == 3]
    most = sum(rules.most_conditions_queue(e.prompt.case.as_dict(), rs) == lab[i]["y"]
               for i, e in l3)
    copiers = staged["references"]["copiers"]
    if F(most, len(l3)) != Fraction(copiers["most_conditions"]["fraction"]):
        off["2"].append("most_conditions")

    # Gate 3: the catch-all is total, and the first match is the truth.
    for i, e in l3:
        ticket = e.prompt.case.as_dict()
        hit = rules.matching(ticket, rs)
        if not hit or hit[-1].id != CATCH_ALL or hit[0].queue != lab[i]["y"]:
            off["3"].append(i)

    # Gate 4: the order errors partition.
    for arm in ARMS:
        n = Counter()
        for a, ticket, _ in answers[arm]:
            got = read_answer(a, ticket, rs)
            n[got["class"]] += 1
            if got["class"] == "order" and ("follows" not in got
                                            or runner_up(rules.matching(ticket, rs)) is None):
                off["4"].append(arm)
        if sum(n.values()) != len(answers[arm]):
            off["4"].append(f"{arm}: classes do not add up")

    checked = [{"gate": g, "what": what, "off": off.get(g, [])[:12], "passes": not off.get(g)}
               for g, what in (("1", "the classes come back"),
                               ("2", "the copiers come back"),
                               ("3", "the catch-all is total, and the first match is the truth"),
                               ("4", "the order errors partition"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off']}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    arms = {arm: arm_reading(answers[arm], rs) for arm in ARMS}
    spec = {arm: specificity(answers[arm], rs) for arm in ARMS}
    expectation = read_expectation(arms, spec)
    for arm in ARMS:
        a = arms[arm]
        print(f"  {arm}: {a['order_errors']} order errors; runner-up "
              f"{a['runner_up']['count']}, catch-all {a['catch_all']['count']}, most "
              f"specific {a['most_specific']['count']}; ranks {a['rank']}; top three "
              f"{a['top_three']['rules']}")
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'fails'}  {e['reading']}")

    record_path().write_text(json.dumps({
        "_env": environment(),
        "what": "where PLAN_QUEUE_ALONE.md's order errors go at level 3: which lower "
                "rule they follow, whether they lean to the more specific rule, and "
                "which governing rule they pass over",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "follows": str(plan.score_path()),
        "surface": "the corpus: the valid answers of the three arms at level 3, two per "
                   "decision, read against the 29 rules of level 3's frozen text",
        "gates": checked,
        "arms": arms,
        "specificity": spec,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }, indent=2, default=str) + "\n")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
