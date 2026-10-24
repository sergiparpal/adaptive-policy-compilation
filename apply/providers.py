"""
EACH ROW WITHIN ONE PROVIDER'S ANSWERS. `FINDINGS_APPLY.md`, *What Stage C does
not settle*, leaves the providers open. Each pass interleaved the two arms in
one order, and §5.9 of `PLAN_APPLY.md` expected that to give both arms the same
providers. In pass 1 it did not, so every row compares arms whose providers
partly differ. `IDEAS.md` carries the reading under *What `PLAN_APPLY.md`
opens*, free on the records. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The two passes**, `results_apply/ask_pass{1,2}.json`. Every one of the 1,454
asks was asked once in each pass, and every answer keeps its `call_attempts`.
**The provider of an answer is the provider of its last attempt**, the one whose
text was parsed. One answer of pass 1 took two attempts, both served by one
provider.

**Ten providers answered the two passes under one model name, and only Baidu
answered enough of every row's decisions to read it.** Counted before the
expectation from the routing alone, which reads no answer, its cells under
reading A below hold:
- 379 of `X-a`'s 778 decisions;
- 246 of the 320 at level 3 for `X-b` and `X-c`, and 209 for `X-d` before its
  selector;
- 187 of `X-e`'s 242;
- 282 of `X-f`'s 320.

GMICloud and Relace hold at most 40 decisions of any row, and every other
provider fewer.

**The loop's own answer has a provider too.** Each loop record keeps one call
per escalation, with its attempts, and `X-a` reads that answer.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Each row on one provider's answers.** For each row and each provider:
     on the decisions Stage C read for the row, each arm is read on the
     answers that provider gave.
     - An arm with two of its answers reads both, as Stage C does. An arm with
       one reads that one alone, and an arm with none drops the decision.
     - `X-b`, `X-c` and `X-e` cut `s` and `t`, and `X-f` cuts `t` and `u`.
     - `X-d` cuts `s`, and needs `t₂` to be the provider's. Its selector,
       `t₁ ≠ p`, is Stage C's, whoever gave `t₁`.
     - `X-a` needs `s₁`, `s₂` and the loop's own answer all to be the
       provider's, since `S` compares the two answers of one decision.
     The statistic, its standard error clustered by ticket and its thin label
     are then Stage C's own: `apply/score.py`'s `adjudicate`, called and not
     copied, on the cut decisions. **Beside each cell, the same decisions read
     with every answer**, as Stage C reads them, so that the provider's cut is
     told apart from the change of decisions. **A cell is read from 100
     decisions up**, the plan's floor for `X-d`. Below it, its counts and value
     are recorded and not read.
  B. **Each row on the decisions one provider answered whole.** The row
     exactly as Stage C computes it, on the decisions where every answer it
     reads is the provider's, `X-d`'s `t₁` included. These are fewer decisions,
     read with Stage C's own estimator. Read for each provider whose cell in A
     is read.
  C. **Whether the providers answer one prompt alike.** Every ask has two
     answers, one per pass, read with the truth of its ticket.
     - **Accuracy.** On the asks Baidu answered in one pass and another
       provider in the other, how much more often Baidu is right. This is read
       against GMICloud, against Relace, and against every other provider
       pooled, each on 100 asks or more.
     - **Agreement.** How often the two answers agree, in each arm, when one
       provider gave both and when two did.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- `results_apply/score.json`, for gate 1;
- the two passes, through `apply/score.py`'s `read`;
- the twelve loop records: the truth and the loop's answer through
  `apply/score.py`'s `labels`, and each escalation's call with its provider;
- the design, rebuilt by `apply/population.py`'s `build`.
Every function `apply/score.py` has is called, not copied: the decisions are
its `units` and every cell its `adjudicate`. What is new is the cut to one
provider's answers, and the asks read two answers at a time.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **Stage C comes back, and so does the reading with every provider.**
     Every row's value, runs, decisions read, verdict and thin label are
     `score.json`'s. That holds for `adjudicate` on the decisions, and for the
     same rows read through this module's cut with every provider admitted.
  2. **Every answer has one provider.** Both passes hold every ask of the
     design once. Every answer has an attempt, and its last attempt names a
     provider.
  3. **A ticket has one truth.** Every escalation on a ticket carries the same
     truth, and every ask's ticket has one, so an ask is read against it.
  4. **The loop's answer has one call.** Every decision's run keeps exactly one
     call at its index, and its last attempt names a provider.

It refuses to write if any fails, and while `PLAN_APPLY.md` is unsigned.
`--dry-run` runs the four, prints pass or fail, and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause of A and B reads Baidu.

  A1. **`X-b` stays above its line, within 0.05 of Stage C's value.**
  A2. **`X-c`'s share stays below 1/2.**
  A3. **`X-d` stays at or above its line, on 100 decisions or more.**
  A4. **`X-e` stays within 0.05 of Stage C's value.** No bet on its sign.
  A5. **`X-f` stays at or above its line.**
  A6. **`X-a` stays at or below its line.**
  A7. **The cut moves `X-b`, `X-d`, `X-e` and `X-f` by at most 0.03 each**,
      against the same decisions read with every answer.
  B1. **On the decisions Baidu answered whole, `X-b`, `X-c` and `X-f` fall on
      the side of their lines where Stage C found them.**
  C1. **Baidu is right as often as GMICloud, as Relace, and as every other
      provider pooled, within 0.05 each.**
  C2. **In each arm, two answers to one ask agree more often when one provider
      gave both than when two did.**

So the drafter expects the routing to have moved the arms' providers without
moving the rows:
- the model under one name answers one prompt about as well wherever it is
  served;
- a provider's share of an arm is too small a lever to move a row by more than
  a few points, even if it did not.

It expects the providers to differ in which answer they give on a close
ticket, which is C2, and not in how often they are right, which is C1. The
drafter trusts C1 least, since no record here has read a provider's answers
before. Then A4, whose row lies within one standard error of its line, then
A7.

**What the drafter had seen**:
- `FINDINGS_APPLY.md` whole, every figure in it, the table of providers by
  pass and arm among them;
- `results_apply/score.json`;
- `PLAN_APPLY.md`'s banner, §0's rows, §5.9 and §12;
- `apply/score.py` and `apply/population.py`;
- `STATUS.md`'s and `IDEAS.md`'s entries on `PLAN_APPLY.md`;
- from the routing alone, which reads no answer:
  - the provider of every answer, by pass, arm, level and kind of screen;
  - the providers that answered each ask in the two passes;
  - the loop's provider at every decision;
  - how many decisions each provider would hold for each row under A and B,
    `X-d`'s before its selector.

**What the drafter had not seen**:
- what any answer of any provider named, or whether it was right;
- any row's value, or any part of one, on any provider's answers;
- how often two answers to one ask agree, by provider.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-10-24, after Stage C closed the plan.
The expectation above was written and committed before any figure by provider
was computed. Not a signed row, not on `STATUS.md`'s scoreboard, and no verdict
moves. Zero API calls.

Usage:  python3 -m apply.providers --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m apply.providers
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from harness.provenance import describe, environment

from . import plan, population
from . import score as S

F = Fraction
FLOOR = plan.MIN_PULL_POPULATION   # a cell is read from this many decisions up
EVERY = None                       # the provider that admits every provider
REFERENCE = "Baidu"                # the one provider with a cell on every row
AGAINST = ("GMICloud", "Relace")   # C1's providers, beside every other pooled

# What each row reads besides the truth: `X-a` the loop's answer, `X-d` its
# selector `t₁` and its `t₂`.
READS = {"X-a": ("s", "loop"), "X-b": ("s", "t"), "X-c": ("s", "t"),
         "X-d": ("s", "t"), "X-e": ("s", "t"), "X-f": ("t", "u")}

# The expectation's lines.
NEAR = F(1, 20)                    # A1, A4: this close to Stage C's value
MOVE = F(3, 100)                   # A7: the cut moves a row at most this far
ALIKE = F(1, 20)                   # C1: two providers right as often, within this

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-10-24, after Stage C closed "
    "PLAN_APPLY.md. The expectation in the module's docstring was written and "
    "committed before any figure by provider was computed. Not a signed row; no "
    "verdict moves.")


def record_path() -> Path:
    return plan.OUT / "providers.json"


# ---------------------------------------------------------------------------
# Who answered
# ---------------------------------------------------------------------------

def provider_of(row: dict) -> str | None:
    """The provider of an answer: its last attempt's, the one whose text was
    parsed. A loop call reads the same way."""
    attempts = row.get("call_attempts") or []
    return attempts[-1].get("provider") if attempts else None


def served(recs: dict[str, dict]) -> dict[tuple[int, str], str | None]:
    """`{(pass, ask id): provider}`, over both passes."""
    return {(plan.pass_of(s), r["id"]): provider_of(r)
            for s, rec in recs.items() for r in rec["rows"]}


def loop_calls() -> dict[str, list[str | None]]:
    """`{escalation id: the provider of each call the loop made at it}`."""
    out: dict[str, list[str | None]] = defaultdict(list)
    for lv in plan.LEVELS:
        for rep in range(1, plan.REPS + 1):
            for c in population.record(lv, rep)["calls"]:
                out[population.escalation_id(lv, rep, c["idx"])].append(provider_of(c))
    return dict(out)


@dataclass(frozen=True)
class Who:
    """Who gave each answer a decision reads, in Stage C's notation."""
    s: tuple[str | None, str | None]
    t: tuple[str | None, str | None]
    u: tuple[str | None, str | None]
    loop: str | None


def who(u: S.Unit, by: dict[tuple[int, str], str | None],
        loop: dict[str, list[str | None]]) -> Who:
    sa = population.screen_ask_id(u.id)
    ta = population.ticket_ask_id(u.level, u.ticket)
    ua = population.ticket_ask_id(0, u.ticket)
    return Who(s=(by[(1, sa)], by[(2, sa)]), t=(by[(1, ta)], by[(2, ta)]),
               u=(by[(1, ua)], by[(2, ua)]), loop=loop[u.id][-1])


# ---------------------------------------------------------------------------
# A and B: the rows
# ---------------------------------------------------------------------------

def own(pair: tuple, by: tuple, provider: str | None) -> tuple | None:
    """The answers of an arm that `provider` gave, as `hits` reads an arm: two
    kept in order, one read twice so that `hits` gives it alone, none `None`.
    Every provider keeps the pair."""
    if provider is EVERY:
        return pair
    kept = tuple(a for a, p in zip(pair, by) if p == provider)
    if not kept:
        return None
    return kept if len(kept) == 2 else kept * 2


def on_answers(row: str, u: S.Unit, w: Who | None, provider: str | None) -> S.Unit | None:
    """Reading A: the decision with each arm the row compares cut to the
    answers `provider` gave, or `None` where it gave none to one of them."""
    if provider is EVERY:
        return u
    if row == "X-a":
        return u if w.s == (provider, provider) and w.loop == provider else None
    if row == "X-d":
        s = own(u.s, w.s, provider)
        return replace(u, s=s) if s is not None and w.t[1] == provider else None
    a, b = READS[row]
    x, y = own(getattr(u, a), getattr(w, a), provider), own(getattr(u, b), getattr(w, b), provider)
    return replace(u, **{a: x, b: y}) if x is not None and y is not None else None


def whole(row: str, w: Who, provider: str) -> bool:
    """Reading B: every answer the row reads is `provider`'s, `X-d`'s selector
    included."""
    return all(w.loop == provider if arm == "loop"
               else all(p == provider for p in getattr(w, arm))
               for arm in READS[row])


def usable(spec: S.Spec, units: list[S.Unit]) -> list[S.Unit]:
    """The decisions Stage C reads for a row: at its levels, with every answer
    it reads valid."""
    return [u for u in units if u.level in spec.levels and spec.needs(u)]


def cell(spec: S.Spec, us: list[S.Unit]) -> dict[str, Any]:
    """`apply/score.py`'s `adjudicate`, called and not copied. A cell is not
    adjudicated, so its verdict is renamed for what it says here: whether the
    cell meets the row's line."""
    out = S.adjudicate(spec, us)
    said = out.pop("verdict")
    out["meets_the_line"] = None if said == "unadjudicable" else said == "holds"
    return out


def reading_a(units: list[S.Unit], whos: dict[str, Who],
              providers: list[str]) -> dict[str, dict[str, Any]]:
    """Every provider with a decision on a row, its cell on its own answers and
    the same decisions on every answer."""
    out: dict[str, dict[str, Any]] = {}
    for spec in S.SPECS:
        cells = {}
        for p in providers:
            pairs = [(u, cut) for u in usable(spec, units)
                     if (cut := on_answers(spec.id, u, whos[u.id], p)) is not None]
            if not pairs:
                continue
            mine = cell(spec, [cut for _, cut in pairs])
            cells[p] = {"above_floor": mine["read"] >= FLOOR, "own": mine,
                        "every_answer": cell(spec, [u for u, _ in pairs])}
        out[spec.id] = cells
    return out


def reading_b(units: list[S.Unit], whos: dict[str, Who],
              a: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Each row on the decisions a provider answered whole, for every provider
    whose cell in A is read."""
    out: dict[str, dict[str, Any]] = {}
    for spec in S.SPECS:
        out[spec.id] = {p: cell(spec, [u for u in usable(spec, units)
                                       if whole(spec.id, whos[u.id], p)])
                        for p, c in a[spec.id].items() if c["above_floor"]}
    return out


# ---------------------------------------------------------------------------
# C: the asks, two answers at a time
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Asked:
    """One ask with a valid answer in each pass, and who gave each."""
    id: str
    arm: str
    level: int
    ticket: int
    y: str
    a: tuple[str, str]
    by: tuple[str | None, str | None]


def asked(design: population.Design, by_pass: dict[int, dict[str, dict]],
          by: dict[tuple[int, str], str | None], truth: dict[int, str]) -> list[Asked]:
    out = []
    for aid, ask in sorted(design.asks.items()):
        a = tuple(S.answer(by_pass[k].get(aid)) for k in (1, 2))
        if not S.valid(a):
            continue
        t = population.ticket_of(ask.case)
        out.append(Asked(id=aid, arm=ask.arm, level=ask.level, ticket=t, y=truth[t],
                         a=a, by=(by[(1, aid)], by[(2, aid)])))
    return out


def against(asks: list[Asked], one: str, other: Callable[[str | None], bool]
            ) -> dict[str, Any]:
    """On the asks `one` answered in one pass and a provider `other` admits in
    the other: how much more often `one` is right."""
    terms, mine, theirs = [], [], []
    for q in asks:
        for k in (0, 1):
            if q.by[k] == one and q.by[1 - k] != one and other(q.by[1 - k]):
                r_one, r_other = int(q.a[k] == q.y), int(q.a[1 - k] == q.y)
                terms.append((q.ticket, F(r_one - r_other)))
                mine.append(F(r_one))
                theirs.append(F(r_other))
                break
    return {"asks": len(terms),
            "right": {"one": S.frac(S.mean(mine)), "other": S.frac(S.mean(theirs))},
            "difference": S.frac(S.mean([d for _, d in terms])),
            "se": S.clustered_se(terms)}


def agreement(asks: list[Asked]) -> dict[str, Any]:
    """How often an ask's two answers agree, by arm and by whether one provider
    gave both. Beside it, Baidu's own pairs against Baidu's with another."""
    def agree(qs: list[Asked]) -> dict[str, Any]:
        return {"asks": len(qs), "agree": S.frac(S.mean([F(int(q.a[0] == q.a[1]))
                                                         for q in qs]))}
    out: dict[str, Any] = {}
    for arm in ("screen", "ticket"):
        here = [q for q in asks if q.arm == arm]
        out[arm] = {
            "one_provider": agree([q for q in here if q.by[0] == q.by[1]]),
            "two_providers": agree([q for q in here if q.by[0] != q.by[1]]),
            "both_reference": agree([q for q in here if q.by == (REFERENCE, REFERENCE)]),
            "reference_and_another": agree([q for q in here if q.by[0] != q.by[1]
                                            and REFERENCE in q.by])}
    return out


def reading_c(asks: list[Asked]) -> dict[str, Any]:
    acc = {name: against(asks, REFERENCE, lambda p, name=name: p == name)
           for name in AGAINST}
    acc["every_other"] = against(asks, REFERENCE, lambda p: p != REFERENCE)
    for arm in ("screen", "ticket"):
        acc[f"every_other_{arm}"] = against([q for q in asks if q.arm == arm],
                                            REFERENCE, lambda p: p != REFERENCE)
    return {"asks": len(asks), "accuracy": acc, "agreement": agreement(asks)}


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def value(c: dict[str, Any] | None) -> Fraction | None:
    """A cell's statistic, exactly."""
    if not c or not c.get("value"):
        return None
    return Fraction(c["value"]["fraction"])


def read_expectation(A: dict, B: dict, C: dict, stage_c: dict[str, Fraction]
                     ) -> list[dict[str, Any]]:
    """Every clause, read on Baidu's cells and on the asks."""
    out = []

    def clause(c: str, holds: Any, reading: str) -> None:
        out.append({"clause": c, "holds": bool(holds), "reading": reading})

    def mine(row: str, part: str = "own") -> Fraction | None:
        c = A[row].get(REFERENCE)
        return value(c[part]) if c and c["above_floor"] else None

    def near(v: Fraction | None, row: str, by: Fraction) -> bool:
        return v is not None and abs(v - stage_c[row]) <= by

    def fmt(v: Fraction | None) -> str:
        return "none" if v is None else f"{float(v):+.4f}"

    v = mine("X-b")
    clause("A1", v is not None and v > plan.X_B_LINE and near(v, "X-b", NEAR),
           f"X-b {fmt(v)} against Stage C's {fmt(stage_c['X-b'])}")
    v = mine("X-c")
    share = A["X-c"][REFERENCE]["own"].get("share") if REFERENCE in A["X-c"] else None
    clause("A2", v is not None and v < 0,
           f"X-c's share {share['value'] if share else None}, compared as {fmt(v)} against 0")
    c = A["X-d"].get(REFERENCE)
    v = mine("X-d")
    clause("A3", v is not None and c["own"]["read"] >= FLOOR and v >= plan.X_D_LINE,
           f"X-d {fmt(v)} on {c['own']['read'] if c else 0} decisions")
    v = mine("X-e")
    clause("A4", near(v, "X-e", NEAR), f"X-e {fmt(v)} against Stage C's {fmt(stage_c['X-e'])}")
    v = mine("X-f")
    clause("A5", v is not None and v >= plan.X_F_LINE, f"X-f {fmt(v)}")
    v = mine("X-a")
    clause("A6", v is not None and v <= plan.X_A_MAX_GAP, f"X-a {fmt(v)}")
    moves = {row: (mine(row), mine(row, "every_answer")) for row in ("X-b", "X-d", "X-e", "X-f")}
    clause("A7", all(o is not None and e is not None and abs(o - e) <= MOVE
                     for o, e in moves.values()),
           "; ".join(f"{row} {fmt(o)} on its own answers, {fmt(e)} on every answer"
                     for row, (o, e) in moves.items()))

    sides = {"X-b": lambda x: x > plan.X_B_LINE, "X-c": lambda x: x < 0,
             "X-f": lambda x: x >= plan.X_F_LINE}
    got = {row: value(B[row].get(REFERENCE)) for row in sides}
    clause("B1", all(x is not None and sides[row](x) for row, x in got.items()),
           "; ".join(f"{row} {fmt(x)} on "
                     f"{B[row][REFERENCE]['read'] if REFERENCE in B[row] else 0} decisions"
                     for row, x in got.items()))

    acc = C["accuracy"]
    keys = (*AGAINST, "every_other")
    diffs = {k: Fraction(acc[k]["difference"]["fraction"]) if acc[k]["difference"] else None
             for k in keys}
    clause("C1", all(acc[k]["asks"] >= FLOOR and diffs[k] is not None
                     and abs(diffs[k]) <= ALIKE for k in keys),
           "; ".join(f"against {k}: {fmt(diffs[k])} on {acc[k]['asks']} asks" for k in keys))
    ag = C["agreement"]

    def share_of(d: dict) -> Fraction | None:
        return Fraction(d["agree"]["fraction"]) if d["agree"] else None
    pairs = {arm: (share_of(ag[arm]["one_provider"]), share_of(ag[arm]["two_providers"]))
             for arm in ("screen", "ticket")}
    clause("C2", all(o is not None and t is not None and o > t for o, t in pairs.values()),
           "; ".join(f"{arm}: {fmt(o)} with one provider, {fmt(t)} with two"
                     for arm, (o, t) in pairs.items()))
    return out


# ---------------------------------------------------------------------------

def same_row(got: dict[str, Any], theirs: dict[str, Any]) -> bool:
    """A row as Stage C recorded it: its value and runs exactly, the decisions
    it read, its verdict and its thin label. The standard error is a float and
    labels only, so it is left to `thin`."""
    def fr(d: dict | None) -> str | None:
        return d["fraction"] if d else None
    return (fr(got.get("value")) == fr(theirs.get("value"))
            and {k: fr(v) for k, v in got.get("per_run", {}).items()}
            == {k: fr(v) for k, v in theirs.get("per_run", {}).items()}
            and got.get("read") == theirs.get("read")
            and got.get("verdict") == theirs.get("verdict")
            and got.get("thin") == theirs.get("thin"))


def routing(by: dict[tuple[int, str], str | None], design: population.Design,
            loop: dict[str, list[str | None]]) -> dict[str, Any]:
    """Who answered, counted by pass and arm, and the loop's provider at the
    decisions."""
    out: dict[str, Any] = {}
    for (k, aid), p in sorted(by.items(), key=lambda x: (x[0][0], x[0][1])):
        arm = design.asks[aid].arm
        out.setdefault(f"pass{k}", {}).setdefault(arm, Counter())[p] += 1
    out = {k: {arm: dict(c.most_common()) for arm, c in v.items()} for k, v in out.items()}
    out["loop_at_the_decisions"] = dict(Counter(loop[i][-1] for i in design.decisions)
                                        .most_common())
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("apply/providers.py writes its reading")
    t0 = time.time()
    before = json.loads(plan.score_path().read_text())
    recs = {s: S.read(s) for s in plan.SESSIONS[1:]}
    by_pass = {plan.pass_of(s): {r["id"]: r for r in rec["rows"]} for s, rec in recs.items()}
    design = population.build()
    lab = S.labels()
    units = S.units(design, by_pass, lab)
    by = served(recs)
    loop = loop_calls()
    off: dict[str, list[str]] = defaultdict(list)

    print("=" * 78)
    print("PLAN_APPLY.md — EACH ROW WITHIN ONE PROVIDER'S ANSWERS — POST-RUN")
    print("=" * 78)

    # Gate 1: Stage C comes back, and so does the reading with every provider.
    for spec in S.SPECS:
        theirs = before["verdicts"][spec.id]
        again = S.adjudicate(spec, units)
        through = S.adjudicate(spec, [on_answers(spec.id, u, None, EVERY)
                                      for u in usable(spec, units)])
        for name, got in (("adjudicate", again), ("the cut", through)):
            if not same_row(got, theirs):
                off["1"].append(f"{spec.id}:{name}")

    # Gate 2: every answer has one provider.
    for s, rec in recs.items():
        ids = [r["id"] for r in rec["rows"]]
        if sorted(ids) != sorted(design.asks):
            off["2"].append(f"{s}: not the design's asks, once each")
        off["2"].extend(f"{s}:{r['id']}" for r in rec["rows"] if not provider_of(r))
    retried = [{"session": s, "id": r["id"],
                "providers": [a.get("provider") for a in r["call_attempts"]]}
               for s, rec in recs.items() for r in rec["rows"]
               if len(r.get("call_attempts") or []) > 1]

    # Gate 3: a ticket has one truth.
    truth: dict[int, str] = {}
    for eid, e in sorted(design.escalations.items()):
        y = lab[eid]["y"]
        if truth.setdefault(e.ticket, y) != y:
            off["3"].append(f"ticket {e.ticket}")
    off["3"].extend(aid for aid, a in design.asks.items()
                    if population.ticket_of(a.case) not in truth)

    # Gate 4: the loop's answer has one call.
    for i in sorted(design.decisions):
        calls = loop.get(i, [])
        if len(calls) != 1 or not calls[0]:
            off["4"].append(i)

    checked = [{"gate": g, "what": what, "off": off.get(g, []), "passes": not off.get(g)}
               for g, what in (("1", "Stage C comes back, and so does the reading with "
                                     "every provider"),
                               ("2", "every answer has one provider"),
                               ("3", "a ticket has one truth"),
                               ("4", "the loop's answer has one call"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off'][:12]}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    whos = {u.id: who(u, by, loop) for u in units}
    providers = sorted({p for p in by.values() if p} | {w.loop for w in whos.values() if w.loop})
    A = reading_a(units, whos, providers)
    B = reading_b(units, whos, A)
    C = reading_c(asked(design, by_pass, by, truth))
    stage_c = {row: Fraction(v["value"]["fraction"]) for row, v in before["verdicts"].items()}
    expectation = read_expectation(A, B, C, stage_c)

    def shown(c: dict | None) -> str:
        v = value(c)
        return f"{'none' if v is None else f'{float(v):+.4f}'} on {c['read'] if c else 0}"
    for spec in S.SPECS:
        c = A[spec.id].get(REFERENCE) or {}
        print(f"  {spec.id}: Stage C {float(stage_c[spec.id]):+.4f}; {REFERENCE} "
              f"{shown(c.get('own'))}, every answer {shown(c.get('every_answer'))}; "
              f"whole {shown(B[spec.id].get(REFERENCE))}")
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'fails'}  {e['reading']}")

    record_path().write_text(json.dumps({
        "_env": environment(),
        "what": "each row of PLAN_APPLY.md read within one provider's answers, and "
                "whether the providers answer one prompt alike",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "follows": str(plan.score_path()),
        "surface": "the corpus: the escalations of PLAN_MANUAL.md's twelve loop runs "
                   "with a screen, as Stage C reads them, and every ask of both passes",
        "gates": checked,
        "retried": retried,
        "routing": routing(by, design, loop),
        "floor": FLOOR,
        "reference": REFERENCE,
        "stage_c": {row: S.frac(v) for row, v in stage_c.items()},
        "A": A,
        "B": B,
        "C": C,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }, indent=2, default=str) + "\n")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
