"""
WHY THE IMPASSE NOTICE CUTS AT `T1_GENERAL`'S TICKETS.
Stage C of `PLAN_CAUSE.md` found it. Told that no rule of the base matches its
ticket, the loop's first call wrote the governing rule's region whole at every
queue's tickets at least as often as under the empty base, but one: at
`T1_GENERAL`'s it wrote it in 9 of 39 right-queue answers, against the empty
base's 27 of 40. By governing rule, it wrote it at the tickets of `H08`, `H28`
and `H29` in 13 of 51, against the empty base's 40 of 55. `FINDINGS_CAUSE.md`,
*What Stage C does not settle*, item 4, and `IDEAS.md` carry the question. Asked
for by Sergi on 2026-11-26, after Stage C. Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For every valid answer of the right queue, in the three sessions, under the
empty base `e`, v2b's paragraph `v` and the impasse notice `i`, it reads:
- **its class**, as Stage C classes it (`whole/paragraph.py`'s `classed`). A
  *cut* is a cut by one listed rule or by two, and *other* is neither whole nor
  a cut;
- **its governing rule**, and whether it is one of *the three rules*, `H08`,
  `H28` and `H29`, where Stage C found the notice writing the region least
  beside the empty base. `H28` and `H29` govern most of `T1_GENERAL`'s tickets,
  and `H23` the rest. The selection is Stage C's, made on both passes, and
  this reading takes it as given;
- **its draft** against the governing rule: whether it lies inside the rule's
  region, covers its ticket, and how much of the rule's part it holds;
- **its note and its reasoning**, by two codes frozen on pass 1 (below).

--------------------------------------------------------------------------
THE CODEBOOK, FROZEN ON PASS 1
--------------------------------------------------------------------------
Under the impasse notice the reasoning walks the manual's list, finds the rule
the ticket matches first, and meets the notice, which says no rule of the base
matches. At the three rules' tickets it says so: *"H29 should apply. But the
motor says 'ninguna regla de la base casa este ticket'. That means H29 is not
present?"* Two codes, each a set of anchored patterns matched case-blind:

  ABSENT  the reasoning says the governing rule is not in the base: the
          governing rule's identifier, followed within 80 characters of one
          sentence by *not present*, *missing*, *absent*, *lacks*, *not in the
          base* and their kin, or one of those followed within 40 characters by
          the identifier;
  GAP     the note says the draft covers what no rule covers: a gap, a
          *vacío*, *not covered*, *no cubierto*, *fills*, *llena*, *no rule
          covers*, *ninguna regla cubre*, *none of the rules*.

**Pass 1 is the development set.** Its right-queue answers were read for the
codes, and their counts are `DEVELOPMENT`, which gate 4 recomputes. Its answers
by arm, place and kind are in `DEVELOPMENT_ANSWERS`. How many carry each code,
at the three rules' tickets and at the others, as whole / not whole:

                   e                   v                   i
                   three    others     three    others     three    others
  answers          19 / 8   76 / 30    3 / 22   40 / 66    8 / 17   88 / 12
  ABSENT           6 / 2    20 / 6     2 / 6    29 / 22    8 / 17   88 / 12
  GAP              1 / 1    0 / 0      1 / 5    1 / 2      3 / 12   6 / 7

- **What the drafter read of them**: the classes by governing rule and arm, with
  each rule's region and part; the drafts and notes of `e` and `i` at the
  tickets of `H28` and `H29`; the windows of `i`'s reasoning at the three rules'
  tickets around `H29`, the catch-all, the notice and the gap, and around the
  words of absence; and the counts of candidate patterns by arm, place and kind.
- **The split is by session**, as in `halves/hidden.py`.

**Codes tried on pass 1 and dropped**:
- the rule said to be broad, *too broad*, *catches everything*: in nearly every
  answer of every arm at the three rules' tickets, whole or not;
- a catch-all or a default named, and the notice said to contradict the
  manual: in nearly every answer of `i`;
- the base said to be a subset of the manual: in most answers of `i`, whole or
  not;
- the governing rule proposed itself, *add H08*, *replicate H28*, *essentially
  adding H28*: in every whole answer of `i` at the three rules' tickets and in
  under a third of the others. It reads the draft the answer then writes, so
  it explains nothing the class does not.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every answer of the three sessions is valid as §0 reads it, as Stage C
     read it;
  2. the classes of the two passes, recounted by arm, are `score.json`'s `CA-g`
     classes;
  3. every answer keeps its reasoning and its payload;
  4. the codebook gives `DEVELOPMENT`'s counts on pass 1.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out answers of the right queue: pass 2 and the
rarest queue's session. The three rules govern none of the rarest queue's
tickets, so the clauses at their tickets read pass 2 alone.

  D1. **The notice is read as the governing rule missing from the base.**
      `ABSENT` is in at least 0.90 of `i`'s answers, and in at most 0.40 of
      `e`'s.
  D2. **At the three rules' tickets, what the notice writes instead of the
      region is a narrowing kept to its ticket.** Under `i`, at least 0.80 of
      the answers not whole there are *other*, inside the governing rule's
      region and covering their ticket.
  D3. **And under v2b's paragraph it was no cut by a listed rule either.**
      Under `v`, at least 0.60 of the answers not whole at the three rules'
      tickets are *other*.
  D4. **The note calls it a gap.** `GAP` is in the notes of at least 0.60 of
      `i`'s answers not whole at the three rules' tickets, and of at most 0.20
      of `i`'s whole answers at the other tickets.
  D5. **The empty base does not call it so.** `GAP` is in the notes of at most
      0.15 of `e`'s answers at the three rules' tickets.
  D6. **The gap is the notice's way of narrowing everywhere.** `GAP` is in the
      notes of at least half of `i`'s answers not whole at the other tickets.

A share over no answers has no value, and a clause that reads one fails.

**The drafter's account.** The impasse notice says no rule of the base matches
the ticket. The model has the manual's list in its system prompt, and the
manual's first match always exists: `H29` matches every ticket.
- **So it reads the notice as the governing rule missing from the base** (D1).
  Everywhere but at the three rules' tickets, it writes the missing rule back.
- **At the three rules' tickets the missing rule is a layer's default**, and
  the rest of the list is read as standing. A default written back would cover
  the regions of the rules above it. So the model writes the gap its ticket
  falls in among the standing rules: the ticket's own combination, inside the
  default's region, and not a cut by any listed rule (D2). Its note calls it a
  gap (D4), as the empty base's notes do not (D5).
- **v2b's paragraph narrowed there the same way** (D3), so the cut at the
  three rules' tickets was never the conflict's cut that the notice took away.
- **D1 is trusted most**, then D2, D5 and D4, then D3.
- **The bet is D6.** Pass 1 held 12 answers of `i` not whole outside the three
  rules. Their notes called 7 of them a gap, and what they narrowed was mostly
  not a default. If the gap is the notice's general way of narrowing, the
  three rules' tickets are only where it narrows most. If it is not, the gap is
  the defaults' alone.

**What the drafter had seen**:
- `FINDINGS_CAUSE.md` whole: Stage C's classes by arm and pass, by queue, by
  governing rule and at the rarest queue's tickets; the codes of
  `halves/hidden.py`; the declarations by arm; the agreement between the passes.
- `score.json`, which carries the same, and its `CA-g` classes by arm.
- **Pass 1's answers**, the development set, as said above.
- **The field names** of an answer and its payload.
- `halves/hidden.py`, its FINDINGS section, and the texts of the four arms.

**What the drafter had not seen**: any draft, note or reasoning of pass 2 or of
the rarest queue's session, answer by answer.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-26, after Stage C. The codebook and
the expectation above were written and committed before the reading ran on the
held-out answers. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m cause.general --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m cause.general
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
ARMS = ("e", "v", "i")
DEVELOPMENT_SESSIONS = ("pass1",)
HELD_OUT = ("pass2", "oncall")
SESSIONS = DEVELOPMENT_SESSIONS + HELD_OUT
RIGHT_OUT = W.RIGHT_OUT                 # wrong queue and no rule: left out, as Stage C leaves them
THE_THREE = ("H08", "H28", "H29")       # Stage C's selection, FINDINGS_CAUSE.md, by governing rule
THREE, OTHERS = "three", "others"
WHOLE, NOT_WHOLE = "whole", "not_whole"
GENERAL = "T1_GENERAL"

# The codebook, frozen on pass 1 before the reading ran on the held-out answers.
ABSENCE = (r"(?:not\s+(?:actually\s+|yet\s+)?(?:in|present\s+in|part\s+of|included\s+in)\s+the\s+"
           r"(?:motor'?s\s+|engine'?s\s+|actual\s+)?(?:base|rule\s*set|ruleset)"
           r"|not\s+(?:actually\s+)?present|missing|absent|lacks?"
           r"|does\s+not\s+(?:have|contain|include)|doesn'?t\s+(?:have|contain|include)"
           r"|no\s+est[aá]\s+en\s+la\s+base|not\s+there)")
AFTER, BEFORE = 80, 40                  # ABSENT: characters from the identifier to the absence, and back
GAP: tuple[str, ...] = (
    r"\bgaps?\b", r"\bvac[ií]os?\b", r"\bhuecos?\b",
    r"\bnot\s+(?:yet\s+|currently\s+|otherwise\s+|already\s+)?(?:covered|handled|addressed|captured|"
    r"matched)\b",
    r"\bno\s+(?:est[aá]n?\s+|estaba\s+)?cubiert[oa]s?\b",
    r"\bno\s+(?:la\s+|lo\s+|los\s+|las\s+|le\s+)?cubren?\b",
    r"\bno\s+contemplad[oa]s?\b",
    r"\buncovered\b", r"\bfill(?:s|ing)?\b", r"\bllen(?:a|ar)\b",
    r"\bninguna\s+regla\s+(?:existente\s+)?(?:cubre|casa|contempla|aplica)\b",
    r"\bno\s+(?:existing\s+)?rule\s+(?:covers|matches|handles|applies)\b",
    r"\bnone\s+of\s+the\s+(?:existing\s+)?rules\b",
)
CODES = ("ABSENT", "GAP")
READ_IN = {"ABSENT": "reasoning", "GAP": "note"}

# The codebook's counts on pass 1's right-queue answers, by arm, place and kind:
# how many carry each code. Gate 4 recomputes them.
DEVELOPMENT: dict[str, dict[str, dict[str, dict[str, int]]]] = {
    "ABSENT": {"e": {THREE: {WHOLE: 6, NOT_WHOLE: 2}, OTHERS: {WHOLE: 20, NOT_WHOLE: 6}},
               "v": {THREE: {WHOLE: 2, NOT_WHOLE: 6}, OTHERS: {WHOLE: 29, NOT_WHOLE: 22}},
               "i": {THREE: {WHOLE: 8, NOT_WHOLE: 17}, OTHERS: {WHOLE: 88, NOT_WHOLE: 12}}},
    "GAP": {"e": {THREE: {WHOLE: 1, NOT_WHOLE: 1}, OTHERS: {WHOLE: 0, NOT_WHOLE: 0}},
            "v": {THREE: {WHOLE: 1, NOT_WHOLE: 5}, OTHERS: {WHOLE: 1, NOT_WHOLE: 2}},
            "i": {THREE: {WHOLE: 3, NOT_WHOLE: 12}, OTHERS: {WHOLE: 6, NOT_WHOLE: 7}}},
}
DEVELOPMENT_ANSWERS: dict[str, dict[str, dict[str, int]]] = {
    "e": {THREE: {WHOLE: 19, NOT_WHOLE: 8}, OTHERS: {WHOLE: 76, NOT_WHOLE: 30}},
    "v": {THREE: {WHOLE: 3, NOT_WHOLE: 22}, OTHERS: {WHOLE: 40, NOT_WHOLE: 66}},
    "i": {THREE: {WHOLE: 8, NOT_WHOLE: 17}, OTHERS: {WHOLE: 88, NOT_WHOLE: 12}},
}

# The expectation's lines.
D1_I, D1_E = F(9, 10), F(2, 5)
D2_LINE = F(4, 5)
D3_LINE = F(3, 5)
D4_THREE, D4_WHOLE_OTHERS = F(3, 5), F(1, 5)
D5_LINE = F(3, 20)
D6_LINE = F(1, 2)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-26, after Stage C. The codebook and the "
    "expectation in the module's docstring were written and committed before the reading ran "
    "on the held-out answers. Not a signed row; no verdict moves.")

share, frac, jsonable = hhidden.share, hhidden.frac, hhidden.jsonable


def record_path():
    return plan.OUT / "general.json"


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def absent(reasoning: str | None, governing: str) -> str | None:
    """The first span where the reasoning says the governing rule is not in the
    base, or None. Each span lies inside one sentence."""
    text = reasoning or ""
    rule = re.escape(governing)
    for pattern in (rf"\b{rule}\b[^.?!\n]{{0,{AFTER}}}?\b{ABSENCE}",
                    rf"\b{ABSENCE}[^.?!\n]{{0,{BEFORE}}}?\b{rule}\b"):
        m = re.search(pattern, text, re.I)
        if m:
            return m.group(0)
    return None


def gap(note: str | None) -> bool:
    return any(re.search(p, note or "", re.I) for p in GAP)


# ---------------------------------------------------------------------------
# Each answer
# ---------------------------------------------------------------------------

def kind(cls: str) -> str:
    return WHOLE if cls == "whole" else NOT_WHOLE


def answer(r: dict[str, Any], session: str, world: tuple) -> dict[str, Any]:
    """One valid answer of the right queue, read: its class, its draft against the
    governing rule, its note and its codes. The span `ABSENT` matched is kept, so
    a reader can check the code against the text."""
    space, cases, regions, truth, queues = world
    payload = r.get("payload") or {}
    cls = W.classed(r["ticket"], payload)
    point = gv.point_of(cases[r["ticket"]], space)
    m = PO.matched(point, regions)
    gov = m[0]
    g = regions[gov]
    part = truth[queues[gov]] & g
    ext = PO.draft_ext(payload, space)
    span = absent(r.get("reasoning"), gov)
    note = str(payload.get("note") or "")
    return {"session": session, "arm": r["arm"], "id": r["id"], "ticket": r["ticket"],
            "class": cls, "kind": kind(cls), "governing": gov, "governing_queue": queues[gov],
            "place": THREE if gov in THE_THREE else OTHERS,
            "inside_the_governing_rule": ext is not None and ext & g == ext,
            "covers_its_ticket": ext is not None and bool(ext & point),
            "draft_points": ext.bit_count() if ext is not None else None,
            "part_points": part.bit_count(),
            "part_held": (ext & part).bit_count() if ext is not None else None,
            "cut_by": (PO.cut_by(ext, gov, regions) if cls.startswith("cut") else None),
            "note": note,
            "codes": {"ABSENT": span is not None, "GAP": gap(note)},
            "absent_span": span,
            "reasoning_chars": len(r.get("reasoning") or "")}


def valid(r: dict[str, Any]) -> bool:
    """§0's validity, the one Stage C read."""
    return plan.valid(r.get("failure"), r.get("payload"), r.get("served_by"))


def read_session(session: str, rows: list[dict], world: tuple) -> list[dict[str, Any]]:
    """Every valid right-queue answer of the three arms in a session, read."""
    out = []
    for r in rows:
        if r["arm"] not in ARMS or not valid(r):
            continue
        if W.classed(r["ticket"], r.get("payload")) in RIGHT_OUT:
            continue
        out.append(answer(r, session, world))
    return out


def development(rows: list[dict], world: tuple) -> tuple[dict, dict]:
    """The codebook's counts on pass 1's right-queue answers, by arm, place and
    kind, and the answers by arm, place and kind (gate 4)."""
    read = read_session("pass1", rows, world)
    cells = {a: {p: {k: 0 for k in (WHOLE, NOT_WHOLE)} for p in (THREE, OTHERS)} for a in ARMS}
    counts = {c: json.loads(json.dumps(cells)) for c in CODES}
    answers = json.loads(json.dumps(cells))
    for x in read:
        answers[x["arm"]][x["place"]][x["kind"]] += 1
        for c in CODES:
            counts[c][x["arm"]][x["place"]][x["kind"]] += x["codes"][c]
    return counts, answers


# ---------------------------------------------------------------------------
# The tallies and the expectation
# ---------------------------------------------------------------------------

def of(xs: list[dict], arm: str | None = None, place: str | None = None,
       k: str | None = None) -> list[dict]:
    return [x for x in xs if (arm is None or x["arm"] == arm)
            and (place is None or x["place"] == place) and (k is None or x["kind"] == k)]


def is_a_narrowing(x: dict) -> bool:
    """D2's narrowing kept to its ticket: other, inside the governing rule's
    region, covering its ticket."""
    return x["class"] == "other" and x["inside_the_governing_rule"] and x["covers_its_ticket"]


def tally(xs: list[dict]) -> dict[str, Any]:
    """By arm, place and kind: the answers, each code's share, the classes and
    the drafts' shape; by governing rule at `T1_GENERAL`'s tickets and the
    three rules'."""
    out: dict[str, Any] = {}
    for a in ARMS:
        out[a] = {}
        for p in (THREE, OTHERS):
            out[a][p] = {}
            for k in (WHOLE, NOT_WHOLE):
                ys = of(xs, a, p, k)
                out[a][p][k] = {
                    "answers": len(ys),
                    "codes": {c: share(ys, lambda x, c=c: x["codes"][c]) for c in CODES},
                    "classes": dict(sorted(Counter(x["class"] for x in ys).items())),
                    "narrowings": share(ys, is_a_narrowing),
                    "part_held": (F(sum(x["part_held"] or 0 for x in ys),
                                    sum(x["part_points"] for x in ys)) if ys else None),
                }
    rules = sorted({x["governing"] for x in xs
                    if x["governing"] in THE_THREE or x["governing_queue"] == GENERAL})
    out["by_rule"] = {g: {a: {"whole": len([x for x in of(xs, a) if x["governing"] == g
                                            and x["kind"] == WHOLE]),
                              "answers": len([x for x in of(xs, a) if x["governing"] == g])}
                          for a in ARMS} for g in rules}
    return out


def diff(a: Fraction | None, b: Fraction | None) -> Fraction | None:
    return None if a is None or b is None else a - b


def expectation(xs: list[dict]) -> list[dict[str, Any]]:
    """The six clauses, on the held-out answers."""
    d1i = share(of(xs, "i"), lambda x: x["codes"]["ABSENT"])
    d1e = share(of(xs, "e"), lambda x: x["codes"]["ABSENT"])
    i3 = of(xs, "i", THREE, NOT_WHOLE)
    d2 = share(i3, is_a_narrowing)
    d3 = share(of(xs, "v", THREE, NOT_WHOLE), lambda x: x["class"] == "other")
    d4a = share(i3, lambda x: x["codes"]["GAP"])
    d4b = share(of(xs, "i", OTHERS, WHOLE), lambda x: x["codes"]["GAP"])
    d5 = share(of(xs, "e", THREE), lambda x: x["codes"]["GAP"])
    d6 = share(of(xs, "i", OTHERS, NOT_WHOLE), lambda x: x["codes"]["GAP"])
    return [
        {"clause": "D1", "what": "ABSENT in at least 0.90 of i's answers, and in at most 0.40 "
                                 "of e's",
         "reading": {"i": d1i, "e": d1e},
         "holds": None not in (d1i, d1e) and d1i >= D1_I and d1e <= D1_E},
        {"clause": "D2", "what": "under i, at least 0.80 of the answers not whole at the three "
                                 "rules' tickets are other, inside the governing rule's region "
                                 "and covering their ticket",
         "reading": {"share": d2, "answers": len(i3)},
         "holds": d2 is not None and d2 >= D2_LINE},
        {"clause": "D3", "what": "under v, at least 0.60 of the answers not whole at the three "
                                 "rules' tickets are other",
         "reading": {"share": d3, "answers": len(of(xs, "v", THREE, NOT_WHOLE))},
         "holds": d3 is not None and d3 >= D3_LINE},
        {"clause": "D4", "what": "GAP in the notes of at least 0.60 of i's answers not whole at "
                                 "the three rules' tickets, and of at most 0.20 of i's whole "
                                 "answers at the other tickets",
         "reading": {"three_not_whole": d4a, "others_whole": d4b},
         "holds": None not in (d4a, d4b) and d4a >= D4_THREE and d4b <= D4_WHOLE_OTHERS},
        {"clause": "D5", "what": "GAP in the notes of at most 0.15 of e's answers at the three "
                                 "rules' tickets",
         "reading": {"share": d5, "answers": len(of(xs, "e", THREE))},
         "holds": d5 is not None and d5 <= D5_LINE},
        {"clause": "D6", "what": "GAP in the notes of at least half of i's answers not whole at "
                                 "the other tickets",
         "reading": {"share": d6, "answers": len(of(xs, "i", OTHERS, NOT_WHOLE))},
         "holds": d6 is not None and d6 >= D6_LINE},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gates(records: dict[str, dict], stage_c: dict, world: tuple) -> list[dict[str, Any]]:
    rows = [(s, r) for s in SESSIONS for r in records[s]["rows"]]
    recount = {a: Counter() for a in plan.ARMS}
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
         "passes": all(dict(recount[a]) == stage_c_classes.get(a) for a in plan.ARMS)},
        {"gate": 3, "what": "every answer keeps its reasoning and its payload",
         "passes": all(isinstance(r.get("reasoning"), str) and r["reasoning"]
                       and isinstance(r.get("payload"), dict) for _, r in rows)},
        {"gate": 4, "what": "the codebook gives DEVELOPMENT's counts on pass 1",
         "passes": dev == (DEVELOPMENT, DEVELOPMENT_ANSWERS)},
    ]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def read_all() -> tuple[dict[str, dict], dict[str, Any]]:
    records = {s: json.loads(plan.ask_path(s).read_text()) for s in SESSIONS}
    return records, json.loads(plan.score_path().read_text())


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
        "the_three_rules": list(THE_THREE),
        "codebook": {"ABSENT": {"absence": ABSENCE, "after": AFTER, "before": BEFORE,
                                "read_in": READ_IN["ABSENT"]},
                     "GAP": {"patterns": list(GAP), "read_in": READ_IN["GAP"]}},
        "constants": {"D1_I": str(D1_I), "D1_E": str(D1_E), "D2_LINE": str(D2_LINE),
                      "D3_LINE": str(D3_LINE), "D4_THREE": str(D4_THREE),
                      "D4_WHOLE_OTHERS": str(D4_WHOLE_OTHERS), "D5_LINE": str(D5_LINE),
                      "D6_LINE": str(D6_LINE)},
        "gates": checked,
        "development_tally": tally(dev),
        "held_out_tally": tally(held),
        "expectation": clauses,
        "answers": held + dev,
    })}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the impasse notice cuts at T1_GENERAL's "
                                             "tickets (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"cause/general.py writes {record_path()}")
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
