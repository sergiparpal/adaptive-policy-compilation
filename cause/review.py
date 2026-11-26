"""
WHICH QUEUE THE REVIEW NOTICE NAMES, AND WHY.
Stage C of `PLAN_CAUSE.md` found it. Told that a reviewer had marked the
engine's decision on its ticket wrong, and nothing of that decision, the loop's
first call named a queue other than the governing rule's in 259 of its 272
answers at the 136 tickets (`CA-d` refuted, thin; `CA-e` unadjudicable).
`FINDINGS_CAUSE.md`, *What Stage C does not settle*, item 1, and `IDEAS.md`
carry the question, with the account it calls obvious and untested: the model
takes the engine's decision to be the manual's first match, and names the next
rule's queue. Asked for by Sergi on 2026-11-26, after Stage C. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For every valid answer of the review notice, arm `r`, in the three sessions, it
reads:
- **the listed rules its ticket matches**, in the list's order, and their
  queues. The *runner-up* is the first matched rule whose queue is not the
  governing rule's, and its queue is the *runner-up's queue*. `H29` matches
  every ticket, so every ticket of a queue other than `T1_GENERAL` has one;
- **the place of the queue it names** among the matched rules' queues, each
  counted once in the list's order: the governing rule's, the runner-up's, a
  later one's, or none of theirs;
- **its draft**: whether its region lies inside the governing rule's region,
  and inside the region of the first matched rule of the queue it names;
- **its declarations**, `beats` and `loses_to`;
- **its reasoning**, by one code frozen on pass 1 (below).

The *support ladder* is `T1_GENERAL`, `T2_TECHNICAL`, `T3_ENGINEERING`. The
tier above a queue on it is its next one; `T3_ENGINEERING` and the queues off
the ladder have none.

--------------------------------------------------------------------------
THE CODE, FROZEN ON PASS 1
--------------------------------------------------------------------------
The reasoning is long: a median of about 15,400 characters in pass 1, and up to
35,000. It is mostly in English, with the prompt quoted in Spanish. It walks the
list, finds the rule the ticket matches first, says where that rule sends the
ticket, and sets the reviewer's mark against it. One code, matched case-blind:

  MARK  the reasoning sets the reviewer's mark against the governing rule.
        Within the 400 characters before a word of the mark (reviewer,
        revisor, marked, erroneous, errónea or erronea, wrong, incorrect), the
        governing rule's identifier, or its queue's name.

It is read in every arm's answers. The other three arms carry no reviewer, so
their hits are the code's own noise: a *wrong* or an *incorrect* near the rule
the reasoning has just walked to.

**Pass 1 is the development set.** Every answer of every arm was read for the
code, and its counts are `DEVELOPMENT`, which gate 4 recomputes. The answers of
`r` by place are in `DEVELOPMENT_PLACES`, which gate 4 reads too:

              e     v     i     r
  answers     136   136   136   136
  MARK        5     9     26    136

  r, by the place of the queue it names: the governing rule's 5, the
  runner-up's 89, a later one's 14, none of theirs 28.

- **What the drafter read of them**: `r`'s counts by place and governing queue;
  the drafts' regions against the governing rule's and the named queue's rule;
  the windows around the engine and the reviewer in four answers of `r`, and
  their notes; the counts of candidate patterns by arm and place.
- **The split is by session**, because the proposer repeats its phrasing inside
  one (`CLAUDE.md`, `PLAN_MANUAL.md`'s lesson). Each prompt is asked once in
  each pass, in its own order, on another day.

**Codes tried on pass 1 and dropped**:
- the engine named beside the governing rule's queue in one sentence: in
  nearly every answer of `r`, `v` and `i`. Every arm's reasoning walks the list
  and says where the engine would send the ticket, so it told the notice from
  nothing;
- the next rule said to apply: *should have matched*, *instead*, *fallback*,
  *the next rule*. It was in about three in four of the answers that name the
  runner-up's queue, and in half of those that name a queue none of the
  matched rules has;
- escalation and technical support, in most answers of every place.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every answer of the three sessions is valid as §0 reads it, as Stage C
     read it;
  2. the classes of the two passes, recounted by arm, are `score.json`'s `CA-g`
     classes;
  3. every answer keeps its reasoning and its payload;
  4. the code gives `DEVELOPMENT`'s counts on pass 1, and `r`'s places give
     `DEVELOPMENT_PLACES`.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out answers: pass 2 and the rarest queue's session.
A *wrong-queue answer* names a queue other than the governing rule's.

  V1. **It names the runner-up's queue.** Among `r`'s wrong-queue answers at
      tickets with a runner-up, at least 0.70 name the runner-up's queue.
  V2. **Its draft is nested in the governing rule.** At least 0.80 of `r`'s
      wrong-queue answers draft a region inside the governing rule's region.
  V3. **And inside the rule of the queue it names.** Among `r`'s wrong-queue
      answers that name the queue of a rule the ticket matches, at least 0.80
      draft a region inside the first such rule's region.
  V4. **Where no matched rule has the queue it names, it names the next tier.**
      Among `r`'s wrong-queue answers that name a queue none of the matched
      rules has, at least 0.70 name the tier above the governing rule's queue
      on the support ladder.
  V5. **The reasoning sets the mark against the governing rule.** `MARK` is in
      at least 0.90 of `r`'s answers, and in at most 0.25 of the other three
      arms' answers, pooled.
  V6. **At the rarest queue's tickets too.** At the seven tickets of `T₇`, at
      least half of `r`'s wrong-queue answers name the runner-up's queue.

A share over no answers has no value, and a clause that reads one fails.

**The drafter's account.** The notice says the engine decided the ticket and a
reviewer marked that decision wrong. It does not say what the engine decided.
- **So the model supposes the engine applied the manual.** It walks the list,
  finds the first rule the ticket matches, and takes that rule's queue for the
  decision the reviewer marked (V5).
- **Then the governing rule's queue is the one answer it rules out**, and it
  reads the list on for the next rule that matches with another queue (V1).
- **It writes that rule's queue as an exception to the governing rule**: a
  region nested inside the governing rule's, which wins there by containment
  with no side declared (level 1 of the system prompt), and inside the rule
  whose queue it takes (V2, V3). It is the region `v`'s cuts draw, or a part
  of it, under the other rule's queue.
- **Where no matched rule has another queue**, at `T1_GENERAL`'s tickets, the
  list offers nothing, and the model climbs the support ladder (V4).
- **V1 is trusted most**, then V5 and V2, then V3 and V4.
- **The bet is V6.** At the rarest queue's tickets the runner-up's queue is
  `T3_ENGINEERING` at four of the seven and `T2_TECHNICAL` at three. In pass 1
  the model named it at three of the four where it is `T3_ENGINEERING`, and at
  none of the three where it is `T2_TECHNICAL`: there it named
  `T3_ENGINEERING`, `ACCOUNT_MANAGER` and `BILLING_SPECIALIST`. A severity-1
  ticket of an enterprise customer may not read as a matter for general
  technical support, whatever the list says. Or pass 1's three were few.

**What the drafter had seen**:
- `FINDINGS_CAUSE.md` whole: Stage C's classes by arm and pass, by queue, by
  governing rule and at the rarest queue's tickets; the codes of
  `halves/hidden.py`; the declarations by arm; the agreement between the passes.
- `score.json`, which carries the same, and its `CA-g` classes by arm.
- **Pass 1's answers**, the development set, as said above.
- **The field names** of an answer and its payload.
- `halves/hidden.py`, its FINDINGS section, and the texts of the four arms.

**What the drafter had not seen**: any queue, draft, note, declaration or
reasoning of pass 2 or of the rarest queue's session, answer by answer, nor
which queue the review notice named there.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-26, after Stage C. The code and the
expectation above were written and committed before the reading ran on the
held-out answers. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m cause.review --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m cause.review
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from typing import Any

from harness.provenance import describe, environment

from halves import hidden as hhidden
from placement import oncall as PO
from reasoned_loop import governed as gv
from reuse import structure as st
from whole import paragraph as W
from whole import references

from . import plan

F = Fraction
ARMS = plan.ARMS                        # e, v, i, r
REVIEW = "r"
OTHERS = tuple(a for a in ARMS if a != REVIEW)
DEVELOPMENT_SESSIONS = ("pass1",)
HELD_OUT = ("pass2", "oncall")
SESSIONS = DEVELOPMENT_SESSIONS + HELD_OUT

GOVERNING, RUNNER_UP, LATER, UNMATCHED = "governing", "runner_up", "later", "unmatched"
PLACES = (GOVERNING, RUNNER_UP, LATER, UNMATCHED)
LADDER = ("T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING")

# The code, frozen on pass 1 before the reading ran on the held-out answers.
MARK_WORDS = r"\b(?:reviewer|revisor|marked|erroneous|err[oó]ne[ao]|wrong|incorrect)\b"
BEFORE = 400                            # the characters before a word of the mark that MARK reads

# The code's counts on pass 1's answers, by arm, and r's answers by place. Gate 4
# recomputes them.
DEVELOPMENT: dict[str, dict[str, int]] = {
    "answers": {"e": 136, "v": 136, "i": 136, "r": 136},
    "MARK": {"e": 5, "v": 9, "i": 26, "r": 136},
}
DEVELOPMENT_PLACES: dict[str, int] = {GOVERNING: 5, RUNNER_UP: 89, LATER: 14, UNMATCHED: 28}

# The expectation's lines.
V1_LINE = F(7, 10)
V2_LINE = F(4, 5)
V3_LINE = F(4, 5)
V4_LINE = F(7, 10)
V5_R, V5_OTHERS = F(9, 10), F(1, 4)
V6_LINE = F(1, 2)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-26, after Stage C. The code and the expectation "
    "in the module's docstring were written and committed before the reading ran on the "
    "held-out answers. Not a signed row; no verdict moves.")

share, frac, jsonable = hhidden.share, hhidden.frac, hhidden.jsonable


def record_path():
    return plan.OUT / "review.json"


# ---------------------------------------------------------------------------
# The code
# ---------------------------------------------------------------------------

def mark(reasoning: str | None, governing: str, queue: str) -> str | None:
    """The window before the first word of the mark whose 400 characters name
    the governing rule or its queue; None if no word of the mark has one."""
    text = reasoning or ""
    rule = re.compile(rf"\b{re.escape(governing)}\b")
    name = re.compile(rf"\b{re.escape(queue)}\b")
    for m in re.finditer(MARK_WORDS, text, re.I):
        before = text[max(0, m.start() - BEFORE):m.start()]
        if rule.search(before) or name.search(before):
            return text[max(0, m.start() - BEFORE):m.end()]
    return None


# ---------------------------------------------------------------------------
# Each answer
# ---------------------------------------------------------------------------

def queues_in_order(m: list[str], queues: dict[str, str]) -> list[str]:
    """The queues of the matched rules, each once, in the list's order."""
    out: list[str] = []
    for x in m:
        if queues[x] not in out:
            out.append(queues[x])
    return out


def place(named: str | None, order: list[str]) -> str:
    """Where the named queue stands among the matched rules' queues."""
    if named not in order:
        return UNMATCHED
    k = order.index(named)
    return GOVERNING if k == 0 else RUNNER_UP if k == 1 else LATER


def tier_above(queue: str) -> str | None:
    """The next queue up the support ladder, or None."""
    if queue not in LADDER or queue == LADDER[-1]:
        return None
    return LADDER[LADDER.index(queue) + 1]


def inside(a: int | None, b: int | None) -> bool | None:
    return None if a is None or b is None else a & b == a


def answer(r: dict[str, Any], session: str, world: tuple) -> dict[str, Any]:
    """One valid answer, read: where the queue it names stands in its ticket's
    list, its draft against the governing rule and the named queue's rule, its
    declarations and its code. The window `MARK` matched is kept, so a reader can
    check the code against the text."""
    space, cases, regions, queues = world[0], world[1], world[2], world[4]
    payload = r.get("payload") or {}
    point = gv.point_of(cases[r["ticket"]], space)
    m = PO.matched(point, regions)
    gov = m[0]
    gq = queues[gov]
    order = queues_in_order(m, queues)
    named = payload.get("action")
    runner = next((x for x in m if queues[x] != gq), None)
    of_named = next((x for x in m if queues[x] == named), None)
    ext = PO.draft_ext(payload, space)
    window = mark(r.get("reasoning"), gov, gq)
    sides = [str(x) for x in (payload.get("beats") or []) + (payload.get("loses_to") or [])]
    return {"session": session, "arm": r["arm"], "id": r["id"], "ticket": r["ticket"],
            "class": W.classed(r["ticket"], payload),
            "governing": gov, "governing_queue": gq, "matched": m, "queues_in_order": order,
            "named": named, "wrong_queue": named != gq, "place": place(named, order),
            "runner_up": runner, "runner_up_queue": queues[runner] if runner else None,
            "first_of_the_named_queue": of_named,
            "tier_above": tier_above(gq), "names_the_tier_above": named == tier_above(gq),
            "draft_points": ext.bit_count() if ext is not None else None,
            "covers_its_ticket": None if ext is None else bool(ext & point),
            "inside_the_governing_rule": inside(ext, regions[gov]),
            "inside_the_named_queue_rule": (inside(ext, regions[of_named])
                                            if of_named is not None else None),
            "is_their_intersection": (None if ext is None or of_named is None
                                      else ext == regions[gov] & regions[of_named]),
            "beats": payload.get("beats"), "loses_to": payload.get("loses_to"),
            "declares": bool(sides), "beats_the_governing_rule": gov in (payload.get("beats") or []),
            "note": str(payload.get("note") or ""),
            "MARK": window is not None, "mark_window": window,
            "reasoning_chars": len(r.get("reasoning") or "")}


def valid(r: dict[str, Any]) -> bool:
    """§0's validity, the one Stage C read."""
    return plan.valid(r.get("failure"), r.get("payload"), r.get("served_by"))


def read_session(session: str, rows: list[dict], world: tuple,
                 arms: tuple[str, ...] = ARMS) -> list[dict[str, Any]]:
    """Every valid answer of a session's arms, read."""
    return [answer(r, session, world) for r in rows if valid(r) and r["arm"] in arms]


def development(rows: list[dict], world: tuple) -> tuple[dict, dict]:
    """The code's counts on pass 1, by arm, and r's answers by place (gate 4)."""
    read = read_session("pass1", rows, world)
    counts = {"answers": {a: 0 for a in ARMS}, "MARK": {a: 0 for a in ARMS}}
    places = {p: 0 for p in PLACES}
    for x in read:
        counts["answers"][x["arm"]] += 1
        counts["MARK"][x["arm"]] += x["MARK"]
        if x["arm"] == REVIEW:
            places[x["place"]] += 1
    return counts, places


# ---------------------------------------------------------------------------
# The tallies and the expectation
# ---------------------------------------------------------------------------

def of(xs: list[dict], arm: str | None = None, **eq) -> list[dict]:
    return [x for x in xs if (arm is None or x["arm"] == arm)
            and all(x[k] == v for k, v in eq.items())]


def tally(xs: list[dict]) -> dict[str, Any]:
    """`r`'s answers by place and by governing queue, its drafts by place, and the
    code by arm."""
    r = of(xs, REVIEW)
    wrong = of(xs, REVIEW, wrong_queue=True)
    out: dict[str, Any] = {
        "answers": {a: len(of(xs, a)) for a in ARMS},
        "MARK": {a: share(of(xs, a), lambda x: x["MARK"]) for a in ARMS},
        "MARK_by_place": {p: share(of(xs, REVIEW, place=p), lambda x: x["MARK"]) for p in PLACES},
        "places": {p: len(of(xs, REVIEW, place=p)) for p in PLACES},
        "named_by_governing_queue": {},
        "drafts_by_place": {},
        "declares": share(wrong, lambda x: x["declares"]),
        "beats_the_governing_rule": share(wrong, lambda x: x["beats_the_governing_rule"]),
        "wrong_queue": len(wrong), "right_queue": len(r) - len(wrong),
    }
    for gq in sorted({x["governing_queue"] for x in r}):
        out["named_by_governing_queue"][gq] = dict(sorted(Counter(
            f"{x['named']} ({x['place']})" for x in r if x["governing_queue"] == gq).items()))
    for p in PLACES:
        ys = of(xs, REVIEW, place=p, wrong_queue=True)
        out["drafts_by_place"][p] = {
            "answers": len(ys),
            "inside_the_governing_rule": share(ys, lambda x: x["inside_the_governing_rule"]),
            "inside_the_named_queue_rule": share(ys, lambda x: x["inside_the_named_queue_rule"]),
            "is_their_intersection": share(ys, lambda x: x["is_their_intersection"]),
            "covers_its_ticket": share(ys, lambda x: x["covers_its_ticket"]),
            "names_the_tier_above": share(ys, lambda x: x["names_the_tier_above"]),
        }
    seven = [x for x in r if x["ticket"] in plan.ONCALL]
    out["the_seven"] = {
        "answers": len(seven),
        "places": {p: len([x for x in seven if x["place"] == p]) for p in PLACES},
        "named": dict(sorted(Counter(x["named"] for x in seven).items())),
        "runner_up_queues": dict(sorted(Counter(x["runner_up_queue"] for x in seven).items())),
    }
    return out


def expectation(xs: list[dict]) -> list[dict[str, Any]]:
    """The six clauses, on the held-out answers."""
    wrong = of(xs, REVIEW, wrong_queue=True)
    with_runner = [x for x in wrong if x["runner_up"] is not None]
    v1 = share(with_runner, lambda x: x["place"] == RUNNER_UP)
    v2 = share(wrong, lambda x: x["inside_the_governing_rule"])
    matched = [x for x in wrong if x["first_of_the_named_queue"] is not None]
    v3 = share(matched, lambda x: x["inside_the_named_queue_rule"])
    unmatched = [x for x in wrong if x["place"] == UNMATCHED]
    v4 = share(unmatched, lambda x: x["names_the_tier_above"])
    v5r = share(of(xs, REVIEW), lambda x: x["MARK"])
    v5o = share([x for x in xs if x["arm"] in OTHERS], lambda x: x["MARK"])
    seven = [x for x in with_runner if x["ticket"] in plan.ONCALL]
    v6 = share(seven, lambda x: x["place"] == RUNNER_UP)
    return [
        {"clause": "V1", "what": "among r's wrong-queue answers at tickets with a runner-up, at "
                                 "least 0.70 name the runner-up's queue",
         "reading": {"share": v1, "answers": len(with_runner)},
         "holds": v1 is not None and v1 >= V1_LINE},
        {"clause": "V2", "what": "at least 0.80 of r's wrong-queue answers draft a region inside "
                                 "the governing rule's region",
         "reading": {"share": v2, "answers": len(wrong)},
         "holds": v2 is not None and v2 >= V2_LINE},
        {"clause": "V3", "what": "among r's wrong-queue answers naming a matched rule's queue, at "
                                 "least 0.80 draft inside the first such rule's region",
         "reading": {"share": v3, "answers": len(matched)},
         "holds": v3 is not None and v3 >= V3_LINE},
        {"clause": "V4", "what": "among r's wrong-queue answers naming a queue no matched rule "
                                 "has, at least 0.70 name the tier above the governing rule's "
                                 "queue on the support ladder",
         "reading": {"share": v4, "answers": len(unmatched)},
         "holds": v4 is not None and v4 >= V4_LINE},
        {"clause": "V5", "what": "MARK in at least 0.90 of r's answers, and in at most 0.25 of "
                                 "the other three arms' answers, pooled",
         "reading": {"r": v5r, "others": v5o},
         "holds": None not in (v5r, v5o) and v5r >= V5_R and v5o <= V5_OTHERS},
        {"clause": "V6", "what": "at T7's tickets, at least half of r's wrong-queue answers name "
                                 "the runner-up's queue",
         "reading": {"share": v6, "answers": len(seven)},
         "holds": v6 is not None and v6 >= V6_LINE},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gates(records: dict[str, dict], stage_c: dict, world: tuple) -> list[dict[str, Any]]:
    rows = [(s, r) for s in SESSIONS for r in records[s]["rows"]]
    recount = {a: Counter() for a in ARMS}
    for s, r in rows:
        if s in plan.PASSES and valid(r):
            recount[r["arm"]][W.classed(r["ticket"], r.get("payload"))] += 1
    stage_c_classes = stage_c["CA-g"]["classes"]
    dev = development(records["pass1"]["rows"], world)
    return [
        {"gate": 1, "what": "every answer of the three sessions is valid as §0 reads it",
         "passes": all(valid(r) for _, r in rows)},
        {"gate": 2, "what": "the classes of the two passes, recounted by arm, are score.json's "
                            "CA-g classes",
         "passes": all(dict(recount[a]) == stage_c_classes.get(a) for a in ARMS)},
        {"gate": 3, "what": "every answer keeps its reasoning and its payload",
         "passes": all(isinstance(r.get("reasoning"), str) and r["reasoning"]
                       and isinstance(r.get("payload"), dict) for _, r in rows)},
        {"gate": 4, "what": "the code gives DEVELOPMENT's counts on pass 1, and r's places "
                            "DEVELOPMENT_PLACES",
         "passes": dev == (DEVELOPMENT, DEVELOPMENT_PLACES)},
    ]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {s: json.loads(plan.ask_path(s).read_text()) for s in SESSIONS}
    return records, json.loads(plan.score_path().read_text())


def kept(xs: list[dict]) -> list[dict]:
    """Every answer of `r` as read, and of the other arms only the code."""
    return [x if x["arm"] == REVIEW else
            {k: x[k] for k in ("session", "arm", "id", "ticket", "governing", "MARK",
                               "mark_window")} for x in xs]


def record_of(gate: dict, checked: list[dict], dev: list[dict], held: list[dict],
              clauses: list[dict]) -> dict[str, Any]:
    """The record: `_env` first, kept out of `jsonable`."""
    return {"_env": environment(), **jsonable({
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {s: str(plan.ask_path(s)) for s in SESSIONS} | {"score": str(plan.score_path())},
        "surface": "the corpus's escalated tickets; each draft's region over the space",
        "development": list(DEVELOPMENT_SESSIONS), "held_out": list(HELD_OUT),
        "code": {"MARK": {"words": MARK_WORDS, "before": BEFORE,
                          "names": "the governing rule's identifier or its queue's name"}},
        "ladder": list(LADDER),
        "constants": {"V1_LINE": str(V1_LINE), "V2_LINE": str(V2_LINE), "V3_LINE": str(V3_LINE),
                      "V4_LINE": str(V4_LINE), "V5_R": str(V5_R), "V5_OTHERS": str(V5_OTHERS),
                      "V6_LINE": str(V6_LINE)},
        "gates": checked,
        "development_tally": tally(dev),
        "held_out_tally": tally(held),
        "expectation": clauses,
        "answers": kept(held) + kept(dev),
    })}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Which queue the review notice names, and why "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"cause/review.py writes {record_path()}")
    records, stage_c = read_all()
    world = references._world()
    checked = gates(records, stage_c, world)
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    dev = read_session("pass1", records["pass1"]["rows"], world)
    held = [x for s in HELD_OUT for x in read_session(s, records[s]["rows"], world)]
    clauses = expectation(held)
    record_path().write_text(json.dumps(st._rounded(record_of(gate, checked, dev, held, clauses)),
                                        indent=2, default=str, ensure_ascii=False) + "\n")
    for c in clauses:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
