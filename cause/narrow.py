"""
WHY THE MODEL NARROWS A MISSING DEFAULT.
`cause/general.py` found it, POST-RUN. Told that no rule of the base matches its
ticket, the first call reads the governing rule as missing from the base and
writes it back, but at the tickets of `H08`, `H28` and `H29`. There it writes a
narrowing kept to its ticket: the ticket's own combination, inside the default's
region. Two notes say the default is absent, so a specific rule is added. None
says why specific, and the default's breadth, named in most of pass 1's
reasonings there, told nothing apart. `FINDINGS_CAUSE.md`, *Two things Stage C
left free*, *What it does not settle*, item 1, and `IDEAS.md` carry the
question. Asked for by Sergi on 2026-11-26, after the two readings. Free on the
records. POST-RUN.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
For every valid answer of the right queue, in the three sessions, under the
empty base `e`, v2b's paragraph `v` and the impasse notice `i`, it reads its
class, its kind and its governing rule, as `cause/general.py` reads them, and:
- **its governing rule's group**: how many rules of another queue than the
  governing rule's lie whole inside the governing rule's region, the governing
  rule aside. *None*; *few*, one to three; or *many*, four or more. The count
  reads the manual's regions and no truth;
- **what its draft holds** of the rules of another queue, by the same count;
- **its reasoning**, by two codes frozen on pass 1 (below).

--------------------------------------------------------------------------
THE STRUCTURE
--------------------------------------------------------------------------
Of the rules that govern a ticket of the passes, `H08`, `H28` and `H29` are the
only ones whose regions hold four rules of another queue or more: 4, 7 and 26.
They are Stage C's three, which this reading takes as given. `H27` holds 8 and
governs none of the tickets. `H03`, `H12`, `H16` and `H18` hold one to three:
`H01` and `H02`; `H09` to `H11`; `H07` and `H15`; and `H17`. They close the
keyword's, billing's, the api's and the integrations' blocks of the list, as the
three close theirs. Gate 5 holds the groups to the regions.

--------------------------------------------------------------------------
THE CODEBOOK, FROZEN ON PASS 1
--------------------------------------------------------------------------
The reasoning walks the list, finds the governing rule, and then places its
draft against the rules it believes stand. A sentence is a run of text ended by
a full stop, a question or an exclamation mark and a space, or by a line break.
Two codes, each a set of patterns matched case-blind within one sentence:

  INSIDE     a sentence places a draft inside the governing rule: a draft
             (*our rule*, *my rule*, *the new rule*, *esta regla*, and their
             kin) said to be a *subset*, *contained*, *nested*, *more specific
             than* or a *caso particular* of the governing rule, named by its
             identifier; or the governing rule said to *contain*, *include* or
             be a *superset* of the draft;
  CONTAINER  a sentence places the other rules inside the draft, the catch-all
             or the default: *all rules are subsets of the catch-all*, *the
             other rules are contained in ours*; or has the draft, the catch-all
             or the default yield to the more specific rules: *automatically
             loses to them*, *more specific rules will override it*, *reglas
             más específicas la superan*.

And one count, which reads no text:

  HOLDS_NONE the draft's region holds no region of a rule of another queue than
             the governing rule's, the governing rule aside.

**Pass 1 is the development set.** Its right-queue answers, which are the ones
`cause/general.py` read there, were read for the codes. Their counts are
`DEVELOPMENT`, `DEVELOPMENT_ANSWERS` and `DEVELOPMENT_GROUPS`, which gate 4
recomputes. How many carry each code, at the three rules' tickets and at the
others, as whole / not whole:

                   e                   v                   i
                   three    others     three    others     three    others
  answers          19 / 8   76 / 30    3 / 22   40 / 66    8 / 17   88 / 12
  INSIDE           4 / 7    6 / 27     1 / 21   28 / 66    1 / 14   13 / 10
  CONTAINER        5 / 0    2 / 0      2 / 0    2 / 2      5 / 1    1 / 1
  HOLDS_NONE       0 / 8    55 / 30    1 / 22   35 / 66    1 / 16   67 / 12

By the governing rule's group, the answers, as whole / not whole:

                   e          v          i
  none             55 / 14    31 / 38    61 / 7
  few              21 / 16    9 / 28     27 / 5
  many             19 / 8     3 / 22     8 / 17

- **What the drafter read of them**: the classes, drafts and declarations at
  the three rules' tickets, by arm; every note there; the tails of `i`'s
  reasonings there, before their answer, whole and not; the sentences that
  candidate patterns matched, by arm, place and kind; and the counts of the
  candidates. Also the regions of the rules and what each holds, and the three
  rules' parts by attribute value, which read the truth over the space.
- **The split is by session**, as in `cause/general.py`.
- **Under `v` the model takes the governing rule to stand**, and pass 1 had 28
  of its 40 whole answers at the other tickets carrying `INSIDE`: a whole draft
  of the rule's part often lies inside its region. So S2 reads `e` and `i`.
- **Under `e` the groups go another way**: the few were written whole less often
  than the three. S5 reads `i` alone.

**Codes tried on pass 1 and dropped**:
- the draft said not to overlap the other rules, *does not overlap*, *sin
  solaparse*, *avoid conflicts*: in most reasonings of `v` and `i` at the three
  rules' tickets, whole or not;
- caution, likeness, the base unknown and the listing promised later, *to be
  safe*, *similar tickets*, *we don't know the existing rules*, *will be listed*:
  at the three rules' tickets, none of them more frequent in the answers not
  whole than in the whole ones, in any arm;
- the governing rule's existence put in a condition, *if H29 existed*, *si
  existiera*: in most answers of `i`, whole or not. It is the reading of absence
  that `cause/general.py`'s `ABSENT` carries;
- the system prompt's own words cited, *componente de excepción*, *caso
  particular de otra*, *excepciones anidadas*: in most answers of `e`, whole or
  not, and at the three rules' tickets in a minority of `v`'s and `i`'s, whole
  or not;
- `INSIDE` with its consequence, the draft said to win or to need no
  declaration in the same sentence or the next: in 8 of `i`'s 17 answers not
  whole at the three rules' tickets, against `INSIDE`'s 14, and in 1 of its 8
  whole ones. `INSIDE` was kept.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. every answer of the three sessions is valid as §0 reads it, as Stage C
     read it;
  2. the classes of the two passes, recounted by arm, are `score.json`'s `CA-g`
     classes;
  3. every answer keeps its reasoning and its payload;
  4. the codebook gives `DEVELOPMENT`'s counts on pass 1, over the answers
     `cause/general.py` read there;
  5. of the rules that govern the passes' tickets, those whose regions hold
     four or more rules of another queue are the three, and those that hold one
     to three are `H03`, `H12`, `H16` and `H18`.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out answers of the right queue: pass 2 and the
rarest queue's session. The three rules and the few govern none of the rarest
queue's tickets, so the clauses at their tickets read pass 2 alone.

  S1. **At a missing default, the narrowing is a particular case of it.** Under
      `i`, `INSIDE` is in at least 0.60 of the answers not whole at the three
      rules' tickets.
  S2. **It is how the model narrows anywhere.** Under `e` and `i`, over every
      ticket, `INSIDE` is in at least 0.75 of the answers not whole, and in at
      most 0.25 of the whole ones.
  S3. **Writing the default whole takes the other side of level 1.** Under `v`
      and `i`, at the three rules' tickets, `CONTAINER` is in at least 0.40 of
      the whole answers, and in at most 0.15 of those not whole.
  S4. **The narrowing holds none of the rules the default holds.** At the three
      rules' tickets, at least 0.85 of the answers not whole, under `e`, `v` and
      `i` together, carry `HOLDS_NONE`.
  S5. **A missing rule that holds few is written back.** Under `i`, at least
      0.70 of the right-queue answers at the tickets of the few are whole.
  S6. **Under the empty base the narrowing is a particular case of the default
      too.** Under `e`, `INSIDE` is in at least 0.60 of the answers not whole at
      the three rules' tickets.

A share over no answers has no value, and a clause that reads one fails.

**The drafter's account.** The system prompt casts the proposer as the
system's exception component. It tells it that a rule that is a particular case
of another needs no declaration, because level 1 orders it.
- **When the model narrows, it writes such a particular case** (S2). Its
  reasoning places the draft inside the governing rule, and the draft holds no
  rule of another queue (S4).
- **Told that no rule of the base matches**, the model reads the governing rule
  as missing (`cause/general.py`'s D1). Where the rule's region holds few rules
  of other queues, it writes the rule back (S5).
- **At the three rules, whose regions hold many**, it writes a particular case
  of the missing default instead (S1): nested in the default, *if it existed*,
  and holding none of the rules the model believes stand.
- **When it writes the default whole there**, its reasoning has those rules lie
  inside the draft and beat it (S3).
- So the narrowing is the model declining to write a rule under which standing
  rules of other queues nest, and writing one nested in it instead. The
  declarations do not explain it. `H29` holds every rule of another queue, so
  written whole it needs no declaration, and most of its answers were narrowed,
  as the other two's were.
- **S4 is trusted most**, then S2, S1, S5 and S3. S3 reads few whole answers.
- **The bet is S6.** Under the empty base no rule stands, and still pass 1's
  narrowings at the three rules' tickets placed the draft inside the default.
  If S6 holds, the particular case is the model's way of narrowing whatever it
  is told of the base. If it fails, it is the hidden base's.

**What the drafter had seen**:
- `FINDINGS_CAUSE.md` whole: Stage C's classes by arm, pass, queue and
  governing rule and at the rarest queue's tickets, and its two POST-RUN
  readings. Their section B gives pass 2's whole answers by governing rule at
  the three rules' tickets, D1 to D6's readings, six phrasings of the held-out
  notes `GAP` missed, and two held-out notes, at tickets 725 and 1807. So the
  denominators of S1, S3, S4 and S6 were known before the reading, and their
  numerators were not.
- `cause/general.py`, its codebook and its development counts, and
  `tests/test_cause_general.py`.
- **Pass 1's answers**, the development set, as said above.
- The texts of the system prompt and of the four arms.

**What the drafter had not seen**: any draft, note or reasoning of pass 2 or of
the rarest queue's session, answer by answer, beyond what `FINDINGS_CAUSE.md`
quotes; and the answers `general.json` keeps. The reading of `cause/general.py`
read by hand, after its verdicts, the held-out notes `GAP` missed and the
answers D6 read. Of them this drafter has seen what `FINDINGS_CAUSE.md` quotes.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-26, after the two readings of
Stage C. The codebook and the expectation above were written and committed
before the reading ran on the held-out answers. Not a signed row, not on
`STATUS.md`'s scoreboard, not a calibration event. Zero API calls.

Usage:  python3 -m cause.narrow --dry-run   # gates 1 to 5; writes nothing
        PYTHONHASHSEED=0 python3 -m cause.narrow
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

from . import general as G
from . import plan

F = Fraction
ARMS = G.ARMS                           # e, v and i, as cause/general.py reads them
DEVELOPMENT_SESSIONS, HELD_OUT, SESSIONS = G.DEVELOPMENT_SESSIONS, G.HELD_OUT, G.SESSIONS
RIGHT_OUT = G.RIGHT_OUT
THE_THREE = G.THE_THREE                 # Stage C's selection, H08, H28 and H29
THREE, OTHERS = G.THREE, G.OTHERS
WHOLE, NOT_WHOLE = G.WHOLE, G.NOT_WHOLE
NONE, FEW, MANY = "none", "few", "many"
GROUPS = (NONE, FEW, MANY)
FEW_MAX = 3                             # a region that holds one to three rules of another queue
THE_FEW = ("H03", "H12", "H16", "H18")  # gate 5: the few that govern a ticket of the passes

# The codebook, frozen on pass 1 before the reading ran on the held-out answers.
SENTENCE = re.compile(r"(?<=[.?!])\s+|\n+")
DRAFT = (r"(?:our|my|this|the\s+new|the\s+proposed|new|proposed)\s+"
         r"(?:rule|condition|conditions|condition\s+set)"
         r"|\bours\b|esta\s+regla|nuestra\s+regla|la\s+regla\s+propuesta|mi\s+regla")
INSIDE_WORDS = (r"(?:strict\s+)?(?:subset|sub-?set|subconjunto|subcaso|sub-?case|special\s+case|"
                r"particular\s+case|caso\s+particular|specialization|specialisation|refinement|"
                r"contained|contenid[ao]|nested|anidad[ao]|inside|within|more\s+specific\s+than|"
                r"m[aá]s\s+espec[ií]fic[ao]\s+que)")
HOLDS_WORDS = r"(?:contains?|contendr[ií]a|contiene|superset|superconjunto|subsumes?|includes?)"
INSIDE_FORMS = (
    # the draft, then a word of being inside, then the governing rule
    r"(?:{d})[^.?!\n]{{0,80}}?\b{w}\b[^.?!\n]{{0,60}}?\b{g}\b",
    # the governing rule, then a word of holding, then the draft
    r"\b{g}\b[^.?!\n]{{0,60}}?\b{h}\b[^.?!\n]{{0,40}}?(?:{d})",
    # the governing rule said to be a superset
    r"\b{g}\b[^.?!\n]{{0,40}}?\bwould\s+be\s+a\s+superset\b",
    # the governing rule, then the draft said to be inside
    r"\b{g}\b[^.?!\n]{{0,40}}?(?:{d})[^.?!\n]{{0,30}}?\b(?:would\s+be|is|be|ser[ií]a|es)\s+"
    r"(?:a\s+|un[ao]?\s+)?{w}",
    # a rule said to be inside the governing rule
    r"\b(?:it|a\s+rule|the\s+rule)\s+(?:would|will)\s+be\s+(?:a\s+)?{w}\b[^.?!\n]{{0,30}}?\b{g}\b",
)
YIELD_TO = r"(?:them|all|any|every|those|these|the\s+more\s+specific|more\s+specific)"
CONTAINER_FORMS = (
    # the other rules said to lie inside the draft, the catch-all or the default
    rf"\b(?:all|every|the\s+other|other|existing|those|these|they)\b[^.?!\n]{{0,40}}?"
    rf"\b(?:rules?\s+)?(?:are|would\s+be|will\s+be)\s+(?:all\s+)?(?:strict\s+)?"
    rf"(?:subsets|contained|nested|inside)\s+(?:of|in|within)\s+(?:the\s+)?"
    rf"(?:catch-?all|default|it\b|ours|{DRAFT})",
    r"\b(?:all|every)\s+(?:other\s+|existing\s+)?rules\s+are\s+(?:all\s+)?subsets\b",
    # the draft, the catch-all or the default said to yield to the more specific rules
    rf"(?:{DRAFT}|catch-?all|the\s+default)[^.?!\n]{{0,30}}?\b(?:would|will)\s+"
    rf"(?:automatically\s+)?(?:lose|yield|be\s+overridden|be\s+superseded)\s+(?:to|by)\s+"
    rf"(?:{YIELD_TO}|H\d\d\s*[-–]\s*H\d\d)",
    rf"\bautomatically\s+(?:lose|loses|yield|yields)\s+to\s+{YIELD_TO}",
    r"\bmore\s+specific\s+rules\b(?!\s*\(ours\))[^.?!\n]{0,40}?\b(?:will|would)\s+"
    r"(?:automatically\s+)?(?:win|override|beat|take\s+precedence|supersede|prevail)\b",
    r"\breglas\s+m[aá]s\s+espec[ií]ficas\b[^.?!\n]{0,40}?\b(?:la\s+|lo\s+)?"
    r"(?:superen|superan|superar[aá]n|ganan|ganar[aá]n|sobrescrib\w*|prevalec\w*)\b",
    r"\bpierde\s+frente\s+a\s+(?:las\s+)?reglas\s+m[aá]s\s+espec",
)
CODES = ("INSIDE", "CONTAINER")
STRUCTURE = "HOLDS_NONE"                # the draft holds no rule of another queue
COUNTED = CODES + (STRUCTURE,)

# The codebook's counts on pass 1's right-queue answers, by arm, place and kind:
# how many carry each code, and how many drafts hold no rule of another queue.
# Gate 4 recomputes them.
DEVELOPMENT: dict[str, dict[str, dict[str, dict[str, int]]]] = {
    "INSIDE": {"e": {THREE: {WHOLE: 4, NOT_WHOLE: 7}, OTHERS: {WHOLE: 6, NOT_WHOLE: 27}},
               "v": {THREE: {WHOLE: 1, NOT_WHOLE: 21}, OTHERS: {WHOLE: 28, NOT_WHOLE: 66}},
               "i": {THREE: {WHOLE: 1, NOT_WHOLE: 14}, OTHERS: {WHOLE: 13, NOT_WHOLE: 10}}},
    "CONTAINER": {"e": {THREE: {WHOLE: 5, NOT_WHOLE: 0}, OTHERS: {WHOLE: 2, NOT_WHOLE: 0}},
                  "v": {THREE: {WHOLE: 2, NOT_WHOLE: 0}, OTHERS: {WHOLE: 2, NOT_WHOLE: 2}},
                  "i": {THREE: {WHOLE: 5, NOT_WHOLE: 1}, OTHERS: {WHOLE: 1, NOT_WHOLE: 1}}},
    STRUCTURE: {"e": {THREE: {WHOLE: 0, NOT_WHOLE: 8}, OTHERS: {WHOLE: 55, NOT_WHOLE: 30}},
                "v": {THREE: {WHOLE: 1, NOT_WHOLE: 22}, OTHERS: {WHOLE: 35, NOT_WHOLE: 66}},
                "i": {THREE: {WHOLE: 1, NOT_WHOLE: 16}, OTHERS: {WHOLE: 67, NOT_WHOLE: 12}}},
}
DEVELOPMENT_ANSWERS: dict[str, dict[str, dict[str, int]]] = {
    "e": {THREE: {WHOLE: 19, NOT_WHOLE: 8}, OTHERS: {WHOLE: 76, NOT_WHOLE: 30}},
    "v": {THREE: {WHOLE: 3, NOT_WHOLE: 22}, OTHERS: {WHOLE: 40, NOT_WHOLE: 66}},
    "i": {THREE: {WHOLE: 8, NOT_WHOLE: 17}, OTHERS: {WHOLE: 88, NOT_WHOLE: 12}},
}
# Pass 1's right-queue answers by arm and by the group of their governing rule.
DEVELOPMENT_GROUPS: dict[str, dict[str, dict[str, int]]] = {
    "e": {NONE: {WHOLE: 55, NOT_WHOLE: 14}, FEW: {WHOLE: 21, NOT_WHOLE: 16},
          MANY: {WHOLE: 19, NOT_WHOLE: 8}},
    "v": {NONE: {WHOLE: 31, NOT_WHOLE: 38}, FEW: {WHOLE: 9, NOT_WHOLE: 28},
          MANY: {WHOLE: 3, NOT_WHOLE: 22}},
    "i": {NONE: {WHOLE: 61, NOT_WHOLE: 7}, FEW: {WHOLE: 27, NOT_WHOLE: 5},
          MANY: {WHOLE: 8, NOT_WHOLE: 17}},
}

# The expectation's lines.
S1_LINE = F(3, 5)
S2_NOT_WHOLE, S2_WHOLE = F(3, 4), F(1, 4)
S3_WHOLE, S3_NOT_WHOLE = F(2, 5), F(3, 20)
S4_LINE = F(17, 20)
S5_LINE = F(7, 10)
S6_LINE = F(3, 5)

PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-26, after the two readings of Stage C. The codebook "
    "and the expectation in the module's docstring were written and committed before the reading "
    "ran on the held-out answers. Not a signed row; no verdict moves.")

share, frac, jsonable = hhidden.share, hhidden.frac, hhidden.jsonable
of = G.of


def record_path():
    return plan.OUT / "narrow.json"


# ---------------------------------------------------------------------------
# The structure
# ---------------------------------------------------------------------------

def held(region: int, governing: str, regions: dict[str, int],
         queues: dict[str, str]) -> list[str]:
    """The rules of another queue than the governing rule's, the governing rule
    aside, whose regions lie whole inside `region`, in the list's order."""
    q = queues[governing]
    return sorted((h for h, r in regions.items()
                   if h != governing and queues[h] != q and r & region == r),
                  key=lambda h: int(h[1:]))


def group(n: int) -> str:
    return NONE if n == 0 else FEW if n <= FEW_MAX else MANY


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def sentences(text: str | None) -> list[str]:
    return [s for s in SENTENCE.split(text or "") if s]


def inside_sentence(s: str, governing: str) -> bool:
    """A sentence that places a draft inside the governing rule."""
    g = re.escape(governing)
    return any(re.search(f.format(d=DRAFT, w=INSIDE_WORDS, h=HOLDS_WORDS, g=g), s, re.I)
               for f in INSIDE_FORMS)


def container_sentence(s: str) -> bool:
    """A sentence that places other rules inside the draft, or has the draft
    yield to the more specific rules."""
    return any(re.search(f, s, re.I) for f in CONTAINER_FORMS)


def inside(reasoning: str | None, governing: str) -> str | None:
    """The first sentence of the reasoning that places a draft inside the
    governing rule, or None."""
    return next((s for s in sentences(reasoning) if inside_sentence(s, governing)), None)


def container(reasoning: str | None) -> str | None:
    return next((s for s in sentences(reasoning) if container_sentence(s)), None)


# ---------------------------------------------------------------------------
# Each answer
# ---------------------------------------------------------------------------

def answer(r: dict[str, Any], session: str, world: tuple) -> dict[str, Any]:
    """One valid answer of the right queue, read: its class, its governing rule's
    group, what of the rules of another queue its draft holds, and its codes. The
    sentence each code matched is kept, so a reader can check the code against
    the text."""
    space, cases, regions, truth, queues = world
    payload = r.get("payload") or {}
    cls = W.classed(r["ticket"], payload)
    point = gv.point_of(cases[r["ticket"]], space)
    gov = PO.matched(point, regions)[0]
    g = regions[gov]
    ext = PO.draft_ext(payload, space)
    gov_held = held(g, gov, regions, queues)
    draft_held = held(ext, gov, regions, queues) if ext is not None else None
    reasoning = r.get("reasoning") or ""
    spans = {"INSIDE": inside(reasoning, gov), "CONTAINER": container(reasoning)}
    return {"session": session, "arm": r["arm"], "id": r["id"], "ticket": r["ticket"],
            "class": cls, "kind": G.kind(cls), "governing": gov, "governing_queue": queues[gov],
            "place": THREE if gov in THE_THREE else OTHERS,
            "governing_holds": gov_held, "group": group(len(gov_held)),
            "draft_holds": draft_held,
            "inside_the_governing_rule": ext is not None and ext & g == ext,
            "covers_its_ticket": ext is not None and bool(ext & point),
            "codes": {"INSIDE": spans["INSIDE"] is not None,
                      "CONTAINER": spans["CONTAINER"] is not None,
                      STRUCTURE: draft_held == []},
            "spans": spans,
            "note": str(payload.get("note") or ""),
            "reasoning_chars": len(reasoning)}


def read_session(session: str, rows: list[dict], world: tuple) -> list[dict[str, Any]]:
    """Every valid right-queue answer of the three arms in a session, read."""
    out = []
    for r in rows:
        if r["arm"] not in ARMS or not G.valid(r):
            continue
        if W.classed(r["ticket"], r.get("payload")) in RIGHT_OUT:
            continue
        out.append(answer(r, session, world))
    return out


def development(rows: list[dict], world: tuple) -> tuple[dict, dict, dict]:
    """The codebook's counts on pass 1's right-queue answers by arm, place and
    kind; the answers by arm, place and kind; and by arm and group (gate 4)."""
    read = read_session("pass1", rows, world)
    cells = {a: {p: {k: 0 for k in (WHOLE, NOT_WHOLE)} for p in (THREE, OTHERS)} for a in ARMS}
    counts = {c: json.loads(json.dumps(cells)) for c in COUNTED}
    answers = json.loads(json.dumps(cells))
    groups = {a: {gr: {k: 0 for k in (WHOLE, NOT_WHOLE)} for gr in GROUPS} for a in ARMS}
    for x in read:
        answers[x["arm"]][x["place"]][x["kind"]] += 1
        groups[x["arm"]][x["group"]][x["kind"]] += 1
        for c in COUNTED:
            counts[c][x["arm"]][x["place"]][x["kind"]] += x["codes"][c]
    return counts, answers, groups


# ---------------------------------------------------------------------------
# The tallies and the expectation
# ---------------------------------------------------------------------------

def code(c: str):
    return lambda x: x["codes"][c]


def tally(xs: list[dict]) -> dict[str, Any]:
    """By arm, place and kind: the answers, each code's share and the classes; by
    arm and group, and by governing rule at the three rules' and the few's
    tickets, the whole answers."""
    out: dict[str, Any] = {}
    for a in ARMS:
        out[a] = {}
        for p in (THREE, OTHERS):
            out[a][p] = {}
            for k in (WHOLE, NOT_WHOLE):
                ys = of(xs, a, p, k)
                out[a][p][k] = {
                    "answers": len(ys),
                    "codes": {c: share(ys, code(c)) for c in COUNTED},
                    "classes": dict(sorted(Counter(x["class"] for x in ys).items())),
                }
    out["by_group"] = {a: {gr: {"whole": sum(x["kind"] == WHOLE for x in ys), "answers": len(ys)}
                           for gr in GROUPS
                           for ys in ([x for x in of(xs, a) if x["group"] == gr],)}
                       for a in ARMS}
    rules = [r for r in THE_THREE + THE_FEW if any(x["governing"] == r for x in xs)]
    out["by_rule"] = {r: {a: {"whole": sum(x["kind"] == WHOLE for x in ys), "answers": len(ys)}
                          for a in ARMS
                          for ys in ([x for x in of(xs, a) if x["governing"] == r],)}
                      for r in rules}
    return out


def expectation(xs: list[dict]) -> list[dict[str, Any]]:
    """The six clauses, on the held-out answers."""
    i3 = of(xs, "i", THREE, NOT_WHOLE)
    s1 = share(i3, code("INSIDE"))
    ei = [x for x in xs if x["arm"] in ("e", "i")]
    s2n = share([x for x in ei if x["kind"] == NOT_WHOLE], code("INSIDE"))
    s2w = share([x for x in ei if x["kind"] == WHOLE], code("INSIDE"))
    vi3 = [x for x in xs if x["arm"] in ("v", "i") and x["place"] == THREE]
    vi3w = [x for x in vi3 if x["kind"] == WHOLE]
    vi3n = [x for x in vi3 if x["kind"] == NOT_WHOLE]
    s3w, s3n = share(vi3w, code("CONTAINER")), share(vi3n, code("CONTAINER"))
    n3 = of(xs, None, THREE, NOT_WHOLE)
    s4 = share(n3, code(STRUCTURE))
    few = [x for x in of(xs, "i") if x["group"] == FEW]
    s5 = share(few, lambda x: x["kind"] == WHOLE)
    e3 = of(xs, "e", THREE, NOT_WHOLE)
    s6 = share(e3, code("INSIDE"))
    return [
        {"clause": "S1", "what": "under i, INSIDE in at least 0.60 of the answers not whole at "
                                 "the three rules' tickets",
         "reading": {"share": s1, "answers": len(i3)},
         "holds": s1 is not None and s1 >= S1_LINE},
        {"clause": "S2", "what": "under e and i, over every ticket, INSIDE in at least 0.75 of "
                                 "the answers not whole, and in at most 0.25 of the whole ones",
         "reading": {"not_whole": s2n, "whole": s2w},
         "holds": None not in (s2n, s2w) and s2n >= S2_NOT_WHOLE and s2w <= S2_WHOLE},
        {"clause": "S3", "what": "under v and i, at the three rules' tickets, CONTAINER in at "
                                 "least 0.40 of the whole answers, and in at most 0.15 of those "
                                 "not whole",
         "reading": {"whole": s3w, "not_whole": s3n,
                     "answers": {"whole": len(vi3w), "not_whole": len(vi3n)}},
         "holds": None not in (s3w, s3n) and s3w >= S3_WHOLE and s3n <= S3_NOT_WHOLE},
        {"clause": "S4", "what": "at the three rules' tickets, at least 0.85 of the answers not "
                                 "whole, under e, v and i together, hold no rule of another queue",
         "reading": {"share": s4, "answers": len(n3)},
         "holds": s4 is not None and s4 >= S4_LINE},
        {"clause": "S5", "what": "under i, at least 0.70 of the right-queue answers at the "
                                 "tickets of the rules that hold one to three rules of another "
                                 "queue are whole",
         "reading": {"share": s5, "answers": len(few)},
         "holds": s5 is not None and s5 >= S5_LINE},
        {"clause": "S6", "what": "under e, INSIDE in at least 0.60 of the answers not whole at "
                                 "the three rules' tickets",
         "reading": {"share": s6, "answers": len(e3)},
         "holds": s6 is not None and s6 >= S6_LINE},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def structure(rows: list[dict], world: tuple) -> dict[str, list[str]]:
    """The governing rules of the passes' tickets, by group (gate 5)."""
    space, cases, regions, truth, queues = world
    govs = {PO.matched(gv.point_of(cases[r["ticket"]], space), regions)[0] for r in rows}
    out: dict[str, list[str]] = {gr: [] for gr in GROUPS}
    for g in sorted(govs, key=lambda h: int(h[1:])):
        out[group(len(held(regions[g], g, regions, queues)))].append(g)
    return out


def gates(records: dict[str, dict], stage_c: dict, world: tuple) -> list[dict[str, Any]]:
    rows = [(s, r) for s in SESSIONS for r in records[s]["rows"]]
    recount = {a: Counter() for a in plan.ARMS}
    for s, r in rows:
        if s in plan.PASSES and G.valid(r):
            recount[r["arm"]][W.classed(r["ticket"], r.get("payload"))] += 1
    stage_c_classes = stage_c["CA-g"]["classes"]
    dev = development(records["pass1"]["rows"], world)
    found = structure([r for s, r in rows if s in plan.PASSES], world)
    return [
        {"gate": 1, "what": "every answer of the three sessions is valid as §0 reads it",
         "passes": all(G.valid(r) for _, r in rows)},
        {"gate": 2, "what": "the classes of the two passes, recounted by arm, are score.json's "
                            "CA-g classes",
         "passes": all(dict(recount[a]) == stage_c_classes.get(a) for a in plan.ARMS)},
        {"gate": 3, "what": "every answer keeps its reasoning and its payload",
         "passes": all(isinstance(r.get("reasoning"), str) and r["reasoning"]
                       and isinstance(r.get("payload"), dict) for _, r in rows)},
        {"gate": 4, "what": "the codebook gives DEVELOPMENT's counts on pass 1, over the answers "
                            "cause/general.py read there",
         "passes": dev == (DEVELOPMENT, DEVELOPMENT_ANSWERS, DEVELOPMENT_GROUPS)
                   and DEVELOPMENT_ANSWERS == G.DEVELOPMENT_ANSWERS},
        {"gate": 5, "what": "of the rules governing the passes' tickets, those whose regions hold "
                            "four or more rules of another queue are the three, and those holding "
                            "one to three are the few",
         "passes": found[MANY] == list(THE_THREE) and found[FEW] == list(THE_FEW)},
    ]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def record_of(gate: dict, checked: list[dict], dev: list[dict], held_out: list[dict],
              clauses: list[dict]) -> dict[str, Any]:
    """The record: `_env` first, kept out of `jsonable`."""
    return {"_env": environment(), **jsonable({
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "source": {s: str(plan.ask_path(s)) for s in SESSIONS} | {"score": str(plan.score_path())},
        "surface": "the corpus's escalated tickets; each draft's region over the space",
        "development": list(DEVELOPMENT_SESSIONS), "held_out": list(HELD_OUT),
        "the_three_rules": list(THE_THREE), "the_few_rules": list(THE_FEW),
        "codebook": {"sentence": SENTENCE.pattern, "draft": DRAFT,
                     "INSIDE": {"inside_words": INSIDE_WORDS, "holds_words": HOLDS_WORDS,
                                "forms": list(INSIDE_FORMS), "read_in": "reasoning"},
                     "CONTAINER": {"forms": list(CONTAINER_FORMS), "read_in": "reasoning"},
                     STRUCTURE: "the draft's region holds no region of a rule of another queue "
                                "than the governing rule's, the governing rule aside"},
        "constants": {"FEW_MAX": FEW_MAX, "S1_LINE": str(S1_LINE),
                      "S2_NOT_WHOLE": str(S2_NOT_WHOLE), "S2_WHOLE": str(S2_WHOLE),
                      "S3_WHOLE": str(S3_WHOLE), "S3_NOT_WHOLE": str(S3_NOT_WHOLE),
                      "S4_LINE": str(S4_LINE), "S5_LINE": str(S5_LINE), "S6_LINE": str(S6_LINE)},
        "gates": checked,
        "development_tally": tally(dev),
        "held_out_tally": tally(held_out),
        "expectation": clauses,
        "answers": held_out + dev,
    })}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why the model narrows a missing default "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 5 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"cause/narrow.py writes {record_path()}")
    records, stage_c = G.read_all()
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
    held_out = [x for s in HELD_OUT for x in read_session(s, records[s]["rows"], world)]
    clauses = expectation(held_out)
    record_path().write_text(json.dumps(st._rounded(record_of(gate, checked, dev, held_out,
                                                               clauses)),
                                        indent=2, default=str, ensure_ascii=False) + "\n")
    for c in clauses:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
