"""
WHY THE HIDDEN HALF CUTS.
Stage C of `PLAN_HALVES.md` found it. Told only that the base is not shown and
asked for a rule for its ticket, the loop's first call wrote its ticket's
governing region about as rarely as under v2b's whole paragraph. Told that the
base is empty, it wrote it about three times in four (`HV-c` refuted, `HV-d`
holds). `FINDINGS_HALVES.md`, *What Stage C does not settle*, item 2, and
`IDEAS.md` carry the question. Asked for by Sergi on 2026-11-12, after Stage C.
Free on the records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For every valid answer of the right queue, in the three sessions and under the
four arms, it reads:
- **its class**, as Stage C classes it (`whole/paragraph.py`'s `classed`). A
  *cut* is a cut by one listed rule or by two;
- **for a cut, the listed rules it is cut by**, by `placement/oncall.py`'s
  reading, called and not copied, and whether the first crossing rule the ticket
  matches is among them;
- **its note**: whether it cites a crossing rule the ticket matches, and two
  codes;
- **its declarations**, `beats` and `loses_to`;
- **its reasoning**, read by a codebook of anchored patterns frozen on pass 1
  (below).

A *crossing rule* is a listed rule after the governing one that the ticket
matches and whose region does not contain the governing rule's. A cut by it
would change the draft.

--------------------------------------------------------------------------
THE CODEBOOK, FROZEN ON PASS 1
--------------------------------------------------------------------------
The reasoning is long: a median of about 17,000 characters in pass 1, and up to
52,000. It is mostly in English, with the prompt quoted in Spanish. It quotes
the impasse frame and asks why the engine could not decide the ticket. It walks
the list, and composes the answer at its end. Each code is a set of anchored
patterns, matched case-blind:

  CONFLICT  the reasoning reads the impasse as a conflict. Within the 600
            characters after a mention of the impasse, a word of conflict or
            overlap, both rules matching, neither containing the other, or
            deciding between rules;
  BETWEEN   it names a conflict between two listed rules: "between H.. and
            H..", or "entre H.. y H..";
  EMPTY     it takes the base as empty: no rules, no existing or other rules,
            an empty base, or "since this is the first rule";
  HIDDEN    it reads the hidden-base sentence: "no se te muestra", "not
            shown", "hidden", "oculta";
  INSIDE    the note says the draft lies inside another rule: a particular case,
            a subcase, contained, inside, a subset, an intersection, a
            specialisation;
  RESOLVES  the note says the draft resolves a conflict: conflict, resolves,
            ambiguity.

**Pass 1 is the development set.** Its right-queue answers were read for the
codes, and their counts are `DEVELOPMENT`, which gate 4 recomputes. Its answers
by arm and class are in `DEVELOPMENT_ANSWERS`. How many carry each code, by arm,
as whole / cut / other:

              e               v               h               o
  answers     100 / 14 / 14   41 / 38 / 48    41 / 41 / 46    86 / 23 / 19
  CONFLICT    52 / 13 / 6     39 / 37 / 46    40 / 41 / 46    74 / 22 / 15
  BETWEEN     9 / 9 / 4       31 / 32 / 29    33 / 30 / 24    29 / 19 / 11
  EMPTY       99 / 13 / 12    1 / 2 / 3       0 / 2 / 5       80 / 11 / 14
  HIDDEN      0 / 0 / 0       27 / 5 / 26     25 / 6 / 16     2 / 0 / 0
  INSIDE      10 / 11 / 3     16 / 27 / 31    22 / 31 / 28    8 / 22 / 11
  RESOLVES    26 / 7 / 7      11 / 20 / 19    14 / 21 / 17    14 / 12 / 9

**The cuts there were one operation.** Of the 116 cuts over the four arms, 106
were cut by the first crossing rule the ticket matches, and 108 carried a note
citing a crossing rule. Of the whole answers, 36 of 268 did.
- **What the drafter read of them**: the counts of candidate patterns by arm and
  class; the windows around the hidden-base sentence in six answers of `h`;
  the windows around the impasse in five answers of `e` and `o`; and their
  notes.
- **The split is by session**, because the proposer repeats its phrasing inside
  one (`CLAUDE.md`, `PLAN_MANUAL.md`'s lesson). Each prompt is asked once in
  each pass, in its own order, on another day.

**Codes tried on pass 1 and dropped, because nothing told them apart**:
- the existing rules, overlap, conflict anywhere in the reasoning, level 1, a
  particular case, specificity, generality, "this ticket" and the two
  declarations. Each is in nearly every reasoning of every arm and class, most
  because the system prompt carries the words;
- an empty base read naively, which the system prompt's "la primera regla de la
  lista" matches everywhere;
- the listed rules said to be the engine's, which went one way in `e` and the
  other in `h` and `v`;
- "no conflict", which went no way.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every answer of the three sessions is valid as §0 reads it, as Stage C
     read it;
  2. the classes of the two passes, recounted by arm, are `score.json`'s `HV-g`
     classes;
  3. every answer keeps its reasoning and its payload;
  4. the codebook gives `DEVELOPMENT`'s counts on pass 1.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out answers: every valid answer of the right queue
in pass 2 and the rarest queue's session.

  Q1. **The cut is the conflict's intersection, in every arm.** Pooled over the
      four arms, at least 0.85 of the cuts are cut by the first crossing rule
      the ticket matches. At least 0.85 carry a note that cites a crossing rule
      the ticket matches.
  Q2. **The hidden half reads the impasse as a conflict.** `CONFLICT` is in at
      least 0.90 of `h`'s answers, and in a share of `e`'s at least 0.25 lower.
  Q3. **Under the empty base, a named conflict goes with the cut.** Among `e`'s
      answers, the share of cuts is at least 0.10 higher where the reasoning
      names a conflict between two rules (`BETWEEN`) than where it does not.
  Q4. **The empty base is taken at its word, and the hidden half is not.**
      `EMPTY` is in at least 0.80 of `e`'s answers, and in at most 0.15 of
      `h`'s.
  Q5. **Beside the empty base, the overlap half makes the cuts doubt it.**
      Under `o`, `EMPTY` is in the whole answers' reasoning in a share at least
      0.25 higher than in the cuts'.
  Q6. **Under the hidden half, reading the hidden-base sentence goes with the
      whole answer.** Under `h`, `HIDDEN` is in the whole answers' reasoning in
      a share at least 0.25 higher than in the cuts'.

A share over no answers has no value, and a clause that reads one fails.

**The drafter's account.** Every arm's first call is told the engine could not
decide its ticket, and asks why.
- **Under the empty base** it mostly answers that the base holds no rule yet. It
  writes the governing rule's region, as a first rule needs no side.
- **Under the hidden half** it cannot answer so. The base is not shown, so it
  supposes the engine holds rules like the manual's. It finds the ticket matches
  the governing rule and a crossing rule of another queue, and reads the impasse
  as a conflict between the two.
- **Two answers settle such a conflict.** One is the governing rule with sides
  declared. The other is its region cut by the crossing rule, which lies inside
  both and wins by containment, with no side declared (level 1). The cut is the
  second.
- **So the hidden half cuts because it takes away the empty base's explanation
  of the impasse, and leaves the conflict.** Where the empty base's own
  answers name a conflict between two rules, they cut too (Q3).
- **And the overlap half beside the empty base** speaks of existing rules of
  another queue. Where the model believes it over the empty base, it reads a
  conflict and cuts (Q5).
- **Q1 is trusted most**: the cut is one operation in every arm. Then Q4 and Q2,
  then Q5 and Q3, whose development sets held 23 and 14 cuts.
- **The bet is Q6.** It is the one pattern of the development set the account
  does not explain. A reasoning that weighs the hidden-base sentence may
  conclude that it cannot know the engine's rules, and write the rule the
  manual gives the ticket. Or the pattern may not generalise.

**What the drafter had seen**:
- `FINDINGS_HALVES.md` whole: Stage C's classes by arm and pass, by queue, by
  governing rule and at the rarest queue's tickets; the declarations by arm;
  the agreement between the passes; the breadth.
- `score.json`, which carries the same.
- **Pass 1's answers**, the development set, as said above.
- **The field names** of an answer and its payload.
- `whole/oncall.py` and `whole/paragraph.py`, with their FINDINGS sections.

**What the drafter had not seen**: any reasoning, note or declaration of pass 2
or of the rarest queue's session, answer by answer.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-12, after Stage C. The codebook and
the expectation above were written and committed before the reading ran on the
held-out answers. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m halves.hidden --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m halves.hidden
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

from placement import oncall as PO
from reasoned_loop import governed as gv
from reuse import structure as st
from whole import paragraph as W
from whole import references

from . import plan, score

F = Fraction
ARMS = ("e", "v", "h", "o")
DEVELOPMENT_SESSIONS = ("pass1",)
HELD_OUT = ("pass2", "oncall")
SESSIONS = DEVELOPMENT_SESSIONS + HELD_OUT
CLASSES = ("whole", "cut", "other")
RIGHT_OUT = W.RIGHT_OUT                 # wrong queue and no rule: left out, as W leaves them

ID = r"H(?:0[1-9]|1[0-9]|2[0-9])"
IMPASSE = r"\bimpasse\b"
WINDOW = 600                            # the characters after an impasse that CONFLICT reads

# The codebook, frozen on pass 1 before the reading ran on the held-out answers.
CODEBOOK: dict[str, tuple[str, ...]] = {
    "CONFLICT": (r"\bconflict\w*", r"\bconflicto\b", r"\boverlap\w*", r"\bsolap\w*",
                 r"\bboth\b[^.]{0,40}\bmatch", r"\bambas\b", r"\bneither\b[^.]{0,30}\bcontain",
                 r"\bdecide\s+between\b"),
    "BETWEEN": (rf"\b(?:between|entre)\s+{ID}\s+(?:and|y|&)\s+{ID}\b",),
    "EMPTY": (r"\bno\s+(?:existing\s+|other\s+|prior\s+)?rules\b",
              r"\bthere\s+are\s+no\s+(?:existing\s+|other\s+)?rules\b",
              r"\bno\s+hay\s+(?:otras\s+)?reglas\b", r"\bsin\s+reglas\b",
              r"\bbase\s+(?:is|est[aá])\s+(?:empty|vac[ií]a)\b", r"\bempty\s+base\b",
              r"\bbase\s+vac[ií]a\b", r"\bal\s+ser\s+la\s+primera\s+regla\b",
              r"\bsince\s+(?:it'?s|this\s+is)\s+the\s+first\s+rule\b"),
    "HIDDEN": (r"\bno\s+se\s+(?:te|me|nos)\s+muestra\b", r"\bnot\s+shown\b", r"\bhidden\b",
               r"\boculta\b"),
    "INSIDE": (r"\bcaso\s+particular\b", r"\bsubcaso\b", r"\bcontenid[ao]s?\b",
               r"\bdentro\s+de\b", r"\bsubconjunto\b", r"\bintersecci[oó]n\b", r"\bsubset\b",
               r"\bcontained\b", r"\binside\b", r"\bintersection\b", r"\bspeciali[sz]\w*",
               r"\bsub-?case\b", r"\bparticular\s+case\b"),
    "RESOLVES": (r"\bconflict\w*", r"\bconflicto\b", r"\bresolv\w*", r"\bresuelv\w*",
                 r"\bambig\w*"),
}
READ_IN = {"CONFLICT": "the impasse's windows", "BETWEEN": "reasoning", "EMPTY": "reasoning",
           "HIDDEN": "reasoning", "INSIDE": "note", "RESOLVES": "note"}
CODES = tuple(CODEBOOK)

# The codebook's counts on pass 1's right-queue answers, by arm and class: how many
# carry each code. Gate 4 recomputes them.
DEVELOPMENT: dict[str, dict[str, dict[str, int]]] = {
    "CONFLICT": {"e": {"whole": 52, "cut": 13, "other": 6},
                 "v": {"whole": 39, "cut": 37, "other": 46},
                 "h": {"whole": 40, "cut": 41, "other": 46},
                 "o": {"whole": 74, "cut": 22, "other": 15}},
    "BETWEEN": {"e": {"whole": 9, "cut": 9, "other": 4},
                "v": {"whole": 31, "cut": 32, "other": 29},
                "h": {"whole": 33, "cut": 30, "other": 24},
                "o": {"whole": 29, "cut": 19, "other": 11}},
    "EMPTY": {"e": {"whole": 99, "cut": 13, "other": 12},
              "v": {"whole": 1, "cut": 2, "other": 3},
              "h": {"whole": 0, "cut": 2, "other": 5},
              "o": {"whole": 80, "cut": 11, "other": 14}},
    "HIDDEN": {"e": {"whole": 0, "cut": 0, "other": 0},
               "v": {"whole": 27, "cut": 5, "other": 26},
               "h": {"whole": 25, "cut": 6, "other": 16},
               "o": {"whole": 2, "cut": 0, "other": 0}},
    "INSIDE": {"e": {"whole": 10, "cut": 11, "other": 3},
               "v": {"whole": 16, "cut": 27, "other": 31},
               "h": {"whole": 22, "cut": 31, "other": 28},
               "o": {"whole": 8, "cut": 22, "other": 11}},
    "RESOLVES": {"e": {"whole": 26, "cut": 7, "other": 7},
                 "v": {"whole": 11, "cut": 20, "other": 19},
                 "h": {"whole": 14, "cut": 21, "other": 17},
                 "o": {"whole": 14, "cut": 12, "other": 9}},
}
DEVELOPMENT_ANSWERS: dict[str, dict[str, int]] = {
    "e": {"whole": 100, "cut": 14, "other": 14},
    "v": {"whole": 41, "cut": 38, "other": 48},
    "h": {"whole": 41, "cut": 41, "other": 46},
    "o": {"whole": 86, "cut": 23, "other": 19},
}

# The expectation's lines.
Q1_LINE = F(85, 100)
Q2_H, Q2_GAP = F(9, 10), F(1, 4)
Q3_GAP = F(1, 10)
Q4_E, Q4_H = F(4, 5), F(3, 20)
Q5_GAP = F(1, 4)
Q6_GAP = F(1, 4)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-12, after Stage C. The codebook and the "
    "expectation in the module's docstring were written and committed before the reading "
    "ran on the held-out answers. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "hidden.json"


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def count(code: str, text: str | None) -> int:
    """How many times a code's patterns match a text, case-blind."""
    return sum(len(re.findall(p, text or "", re.I)) for p in CODEBOOK[code])


def windows(reasoning: str | None) -> list[str]:
    """The `WINDOW` characters after each mention of the impasse."""
    text = reasoning or ""
    return [text[m.end():m.end() + WINDOW] for m in re.finditer(IMPASSE, text, re.I)]


def codes(reasoning: str | None, note: str | None) -> dict[str, bool]:
    """Whether an answer carries each code, each read where `READ_IN` says."""
    return {"CONFLICT": any(count("CONFLICT", w) for w in windows(reasoning)),
            "BETWEEN": count("BETWEEN", reasoning) > 0,
            "EMPTY": count("EMPTY", reasoning) > 0,
            "HIDDEN": count("HIDDEN", reasoning) > 0,
            "INSIDE": count("INSIDE", note) > 0,
            "RESOLVES": count("RESOLVES", note) > 0}


# ---------------------------------------------------------------------------
# Each answer
# ---------------------------------------------------------------------------

def kind(cls: str) -> str:
    """A class as the reading groups it: a cut by one rule or by two is a cut."""
    return "cut" if cls.startswith("cut") else cls


def crossing(m: list[str], gov: str, regions: dict[str, int]) -> list[str]:
    """The matched rules after the governing one whose region does not contain
    the governing rule's: a cut by any of them would change the draft."""
    g = regions[gov]
    return [x for x in m[m.index(gov) + 1:] if g & regions[x] != g]


def answer(r: dict[str, Any], session: str, world: tuple) -> dict[str, Any]:
    """One valid answer, read: its class, what a cut is cut by, its note, its
    declarations and its codes. The window after its first impasse is kept, so
    a reader can check `CONFLICT` against the text."""
    space, cases, regions = world[0], world[1], world[2]
    payload = r.get("payload") or {}
    cls = W.classed(r["ticket"], payload)
    m = PO.matched(gv.point_of(cases[r["ticket"]], space), regions)
    gov = m[0]
    cross = crossing(m, gov, regions)
    first = PO.first_cutting(m, gov, regions)
    cut = PO.cut_by(PO.draft_ext(payload, space), gov, regions) if kind(cls) == "cut" else None
    note = str(payload.get("note") or "")
    cites = sorted(set(PO.CITED.findall(note)))
    sides = [str(x) for x in (payload.get("beats") or []) + (payload.get("loses_to") or [])]
    reasoning = r.get("reasoning") or ""
    win = windows(reasoning)
    return {"session": session, "arm": r["arm"], "id": r["id"], "ticket": r["ticket"],
            "class": cls, "kind": kind(cls), "governing": gov, "crossing": cross,
            "first_crossing": first, "cut_by": cut,
            "cut_by_the_first_crossing": bool(cut) and first in cut,
            "note": note, "note_cites": cites,
            "note_cites_a_crossing_rule": bool(set(cites) & set(cross)),
            "beats": payload.get("beats"), "loses_to": payload.get("loses_to"),
            "declares": bool(sides), "declares_against_the_governing_rule": gov in sides,
            "declares_against_a_crossing_rule": bool(set(sides) & set(cross)),
            "codes": codes(reasoning, note),
            "first_impasse_window": win[0] if win else None,
            "reasoning_chars": len(reasoning)}


def read_session(session: str, rows: list[dict], world: tuple) -> list[dict[str, Any]]:
    """Every valid right-queue answer of a session, read."""
    out = []
    for r in rows:
        if not score.valid(r):
            continue
        if W.classed(r["ticket"], r.get("payload")) in RIGHT_OUT:
            continue
        out.append(answer(r, session, world))
    return out


def development(rows: list[dict], world: tuple) -> tuple[dict, dict]:
    """The codebook's counts on pass 1's right-queue answers, by arm and class,
    and the answers by arm and class (gate 4)."""
    read = read_session("pass1", rows, world)
    counts = {c: {a: {k: 0 for k in CLASSES} for a in ARMS} for c in CODES}
    answers = {a: {k: 0 for k in CLASSES} for a in ARMS}
    for x in read:
        answers[x["arm"]][x["kind"]] += 1
        for c in CODES:
            counts[c][x["arm"]][x["kind"]] += x["codes"][c]
    return counts, answers


# ---------------------------------------------------------------------------
# The tallies and the expectation
# ---------------------------------------------------------------------------

def share(xs: list[dict], test) -> Fraction | None:
    return F(sum(1 for x in xs if test(x)), len(xs)) if xs else None


def of(xs: list[dict], arm: str | None = None, k: str | None = None) -> list[dict]:
    return [x for x in xs if (arm is None or x["arm"] == arm) and (k is None or x["kind"] == k)]


def tally(xs: list[dict]) -> dict[str, Any]:
    """By arm and class: the answers, each code's share, and the structure of
    the cuts and the declarations."""
    out: dict[str, Any] = {}
    for a in ARMS:
        out[a] = {}
        for k in CLASSES:
            ys = of(xs, a, k)
            out[a][k] = {
                "answers": len(ys),
                "codes": {c: share(ys, lambda x, c=c: x["codes"][c]) for c in CODES},
                "note_cites_a_crossing_rule": share(ys, lambda x: x["note_cites_a_crossing_rule"]),
                "declares": share(ys, lambda x: x["declares"]),
                "declares_against_a_crossing_rule":
                    share(ys, lambda x: x["declares_against_a_crossing_rule"]),
                "declares_against_the_governing_rule":
                    share(ys, lambda x: x["declares_against_the_governing_rule"]),
            }
        cuts = of(xs, a, "cut")
        out[a]["cut_by_the_first_crossing"] = share(cuts, lambda x: x["cut_by_the_first_crossing"])
        out[a]["cuts_where_between"] = share([x for x in of(xs, a) if x["codes"]["BETWEEN"]],
                                             lambda x: x["kind"] == "cut")
        out[a]["cuts_where_not_between"] = share([x for x in of(xs, a)
                                                  if not x["codes"]["BETWEEN"]],
                                                 lambda x: x["kind"] == "cut")
    return out


def diff(a: Fraction | None, b: Fraction | None) -> Fraction | None:
    return None if a is None or b is None else a - b


def expectation(xs: list[dict]) -> list[dict[str, Any]]:
    """The six clauses, on the held-out answers."""
    cuts = of(xs, k="cut")
    q1a = share(cuts, lambda x: x["cut_by_the_first_crossing"])
    q1b = share(cuts, lambda x: x["note_cites_a_crossing_rule"])
    conflict = {a: share(of(xs, a), lambda x: x["codes"]["CONFLICT"]) for a in ("e", "h")}
    e = of(xs, "e")
    q3 = diff(share([x for x in e if x["codes"]["BETWEEN"]], lambda x: x["kind"] == "cut"),
              share([x for x in e if not x["codes"]["BETWEEN"]], lambda x: x["kind"] == "cut"))
    empty = {a: share(of(xs, a), lambda x: x["codes"]["EMPTY"]) for a in ("e", "h")}
    q5 = diff(share(of(xs, "o", "whole"), lambda x: x["codes"]["EMPTY"]),
              share(of(xs, "o", "cut"), lambda x: x["codes"]["EMPTY"]))
    q6 = diff(share(of(xs, "h", "whole"), lambda x: x["codes"]["HIDDEN"]),
              share(of(xs, "h", "cut"), lambda x: x["codes"]["HIDDEN"]))
    q2gap = diff(conflict["h"], conflict["e"])
    return [
        {"clause": "Q1", "what": "pooled over the four arms, at least 0.85 of the cuts are cut "
                                 "by the first crossing rule, and at least 0.85 carry a note "
                                 "citing a crossing rule",
         "reading": {"cut_by_the_first_crossing": q1a, "note_cites_a_crossing_rule": q1b,
                     "cuts": len(cuts)},
         "holds": None not in (q1a, q1b) and q1a >= Q1_LINE and q1b >= Q1_LINE},
        {"clause": "Q2", "what": "CONFLICT in at least 0.90 of h's answers, and in a share of "
                                 "e's at least 0.25 lower",
         "reading": {"h": conflict["h"], "e": conflict["e"], "gap": q2gap},
         "holds": q2gap is not None and conflict["h"] >= Q2_H and q2gap >= Q2_GAP},
        {"clause": "Q3", "what": "among e's answers, the share of cuts is at least 0.10 higher "
                                 "where the reasoning names a conflict between two rules",
         "reading": {"gap": q3},
         "holds": q3 is not None and q3 >= Q3_GAP},
        {"clause": "Q4", "what": "EMPTY in at least 0.80 of e's answers and at most 0.15 of h's",
         "reading": {"e": empty["e"], "h": empty["h"]},
         "holds": None not in empty.values() and empty["e"] >= Q4_E and empty["h"] <= Q4_H},
        {"clause": "Q5", "what": "under o, EMPTY in the whole answers' reasoning in a share at "
                                 "least 0.25 higher than in the cuts'",
         "reading": {"gap": q5},
         "holds": q5 is not None and q5 >= Q5_GAP},
        {"clause": "Q6", "what": "under h, HIDDEN in the whole answers' reasoning in a share at "
                                 "least 0.25 higher than in the cuts'",
         "reading": {"gap": q6},
         "holds": q6 is not None and q6 >= Q6_GAP},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def gates(records: dict[str, dict], stage_c: dict, world: tuple) -> list[dict[str, Any]]:
    rows = [(s, r) for s in SESSIONS for r in records[s]["rows"]]
    recount = {a: Counter() for a in ARMS}
    for s, r in rows:
        if s in plan.PASSES and score.valid(r):
            recount[r["arm"]][W.classed(r["ticket"], r.get("payload"))] += 1
    stage_c_classes = stage_c["HV-g"]["classes"]
    dev = development(records["pass1"]["rows"], world)
    return [
        {"gate": 1, "what": "every answer of the three sessions is valid as §0 reads it",
         "passes": all(score.valid(r) for _, r in rows)},
        {"gate": 2, "what": "the classes of the two passes, recounted by arm, are score.json's "
                            "HV-g classes",
         "passes": all(dict(recount[a]) == stage_c_classes.get(a) for a in ARMS)},
        {"gate": 3, "what": "every answer keeps its reasoning and its payload",
         "passes": all(isinstance(r.get("reasoning"), str) and r["reasoning"]
                       and isinstance(r.get("payload"), dict) for _, r in rows)},
        {"gate": 4, "what": "the codebook gives DEVELOPMENT's counts on pass 1",
         "passes": dev == (DEVELOPMENT, DEVELOPMENT_ANSWERS)},
    ]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def frac(x):
    return None if x is None else {"fraction": str(x), "value": float(x)}


def jsonable(obj):
    if isinstance(obj, Fraction):
        return frac(obj)
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items() if not str(k).startswith("_")}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    return obj


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
        "surface": "the corpus's escalated tickets, each answer's region over the space",
        "development": list(DEVELOPMENT_SESSIONS), "held_out": list(HELD_OUT),
        "codebook": {c: {"patterns": list(CODEBOOK[c]), "read_in": READ_IN[c]} for c in CODES},
        "window": WINDOW,
        "constants": {"Q1_LINE": str(Q1_LINE), "Q2_H": str(Q2_H), "Q2_GAP": str(Q2_GAP),
                      "Q3_GAP": str(Q3_GAP), "Q4_E": str(Q4_E), "Q4_H": str(Q4_H),
                      "Q5_GAP": str(Q5_GAP), "Q6_GAP": str(Q6_GAP)},
        "gates": checked,
        "development_tally": tally(dev),
        "held_out_tally": tally(held),
        "expectation": clauses,
        "answers": held + dev,
    })}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the hidden half cuts (POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"halves/hidden.py writes {record_path()}")
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
