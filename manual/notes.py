"""
WHAT THE PROPOSER WROTE BESIDE EACH RULE. `FINDINGS_MANUAL.md`, *What these
readings do not settle*, leaves two questions to the notes the proposer wrote
beside its rules in `PLAN_MANUAL.md`'s twelve loop runs. Why does the list of
rules make it write narrower rules than the prose does? And why does the
catalogue make it exclude the keyword when the prose does not? `IDEAS.md`
carries both under *What `PLAN_MANUAL.md` opens*, as a codebook's work, with
its patterns anchored. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The twelve loop runs**, `results_manual/loop_L{k}_r{r}.json`. Every rule a run
installed keeps the `note` the proposer wrote beside it. v1's schema asks for it
as *"una frase justificando el nivel de abstraccion y la prioridad elegidos"*.
There are 764 notes:
- 119 under the names;
- 102 under the catalogue;
- 222 under the prose;
- 321 under the rules.
They are in Spanish, and a few are in English.

**A note is its first 280 characters.** `rung2/engine2.py` cuts it there when it
builds the rule. No record keeps the rest: a loop record keeps each call's
provider, tokens and finish reasons, not its text. 674 of the 764 notes are 280
characters long. So a code missing from a note may lie past the cut, and
**every count of a code is a floor** on what the proposer wrote.

**`PLAN_MANUAL.md` §4, rule E, says a note is recorded and never coded.** That
rule bound the plan's stages, so that no row would read what the proposer said.
This reading codes the notes after the plan closed, and no row reads it either.

--------------------------------------------------------------------------
THE CODEBOOK
--------------------------------------------------------------------------
**Development and held-out.**
- The codebook was written while reading the notes of the first run at each
  level, 231 of them.
- It was frozen before any note of the second or third runs was read, 533 of
  them.
- The split is by run, because the proposer repeats its phrasing inside a run.
  A split inside runs would hand the held-out notes the development notes'
  idiom.
- **Every clause below is read on the held-out runs.** The development
  figures sit beside them.

**Ten codes**, each a set of literal patterns anchored at word boundaries.
Anchoring matters: `PLAN_WHY.md`'s codebook matched `m[aá]s condiciones` inside
*"mismas condiciones"*. `hidden` is matched case-sensitively, the others not.
A note can carry any number of codes. The count orients, and the quotations the
record keeps are the evidence.

  hidden      it cites a rule of the manual by its identifier, `H01` to `H29`.
              Only level 3's prompt carries them.
  policy      it appeals to the manual by name (*la política*, *el manual*) or
              to a numbered section of the prose (*punto 4*).
  inside      it frames a rule as a particular case of another: *caso
              particular*, *subcaso*, *subconjunto*.
  spec        it argues comparative specificity: *más específica*.
  narrow      it says the rule is written for the case: *se crea una regla
              específica*, *perfil exacto*.
  widen       it says the rule generalises: *generaliza*, *se abstrae*, *regla
              general para*, *cualquier cliente*, *casos análogos*.
  gap         it frames the ticket as uncovered by the base: *ninguna regla*,
              *no hay regla*, *hueco*, *complementaria*.
  analogy     it argues from a rule of the base: *por analogía*, *siguiendo el
              patrón*, *coherente con*.
  precedence  it says one thing outranks another: *tiene prioridad*,
              *prevalecer*, *prioriza*, *antes que*, *por encima de*. The
              boilerplate *no necesita declarar prioridad* does not count.
  keyword     it mentions security or the keyword: *seguridad*, *security*,
              *keyword*, *palabra clave*.

`CODEBOOK_DIGEST` fingerprints the patterns, and the tests pin it. An edit to a
pattern after the commit that fixed it shows in a diff.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **Why the list makes the proposer write narrower rules.** The births read
     are the ones `K-a` reads, taken as `manual/readings.py` takes them. A birth
     is *narrow* when it spans at most 840 points off the keyword: the two
     narrowest bands of `manual/after_readings.py`, cut at the quartiles of L₂'s
     and L₃'s births pooled. For each level and set it reads:
     - each code's births beside the births without it: how many there are, how
       many are narrow, and their median points off the keyword;
     - **the gap** in the narrow share between L₂ and L₃, split by each code's
       mix as `manual/after_readings.py` splits `K-a`'s gap, with each level's
       rates read on the other level's mix;
     - the same split by **the tickets' mix**, the true queue of the ticket
       each birth was born on. When one level has births on a queue's tickets
       and the other has none, those births leave both sides. The split reads
       the common support, and counts the births it drops.
     For the births whose note cites hidden rules, it reads three things:
     - whether the birth lies inside a rule it cites, over the space and as
       written;
     - whether it cites the hidden rule that governs its ticket;
     - whether it names that rule's queue.
  B. **Why the catalogue makes the proposer exclude the keyword and the prose
     does not.** Every rule is read, and sorted three ways:
     - a *keyword rule* is one whose extension lies inside the keyword's half;
     - a rule *excludes* the keyword when its extension lies in the half without
       it;
     - an *ordinary* rule is neither a keyword rule nor born on a ticket that
       carried the keyword.
     For each level and set it reads:
     - the ordinary rules, by whether they exclude the keyword and whether their
       note mentions it;
     - the rules that exclude it, by whether their note mentions it;
     - the keyword rules, by whether their note states a precedence or mentions
       the keyword, and whether the rule declared an edge at its birth;
     - every rule, by whether a rule shown at its escalation excluded the
       keyword, and whether it excludes the keyword itself.
     It quotes four sets of notes:
     - the first rule of every run;
     - every held-out ordinary rule at L₂ and L₃ whose note mentions the
       keyword;
     - every held-out keyword rule at L₂;
     - every held-out rule at L₁ that excludes the keyword when no rule shown
       at its escalation did.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- The twelve loop records, read-only, and the corpus their tickets come from.
- `results_manual/readings.json` and `results_manual/after_readings.json`, for
  gate 1.
- `HIDDEN_DSL`, through `manual/readings.py`'s `hidden_rules`.
Every function that already exists is called, not copied:
- the births are `manual/readings.py`'s `births_read`;
- the bands, the split and the mix split are `manual/after_readings.py`'s, read
  on the narrow rate where that module reads crossing;
- the exclusion is its `excludes_keyword`, and a keyword rule is
  `blind.rows.is_keyword`.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The births and the bands are the readings'.** Every run's births, by
     rule, crossing and class, are `readings.json`'s. The cuts are
     `after_readings.json`'s.
  2. **The notes are the records'.** Every rule of every run carries a note of
     at most 280 characters. Every rule shown at a birth was born before it.
     The sets split the runs by repetition: the first is development, the
     second and third held-out.
  3. **Two routes give the keyword and the nesting.**
     - A rule excludes the keyword exactly when its extension lies in the half
       without it.
     - A rule is a keyword rule exactly when one of its conditions admits only
       `True` for the keyword.
     - For every birth and every hidden rule its note cites, the birth lies
       inside the cited rule over the space exactly when it does so off the
       keyword.
  4. **The codebook is the one committed, and the identifiers are the
     policy's.** The patterns give `CODEBOOK_DIGEST`. Every identifier a note
     cites names a rule of `HIDDEN_DSL`, and no note outside level 3 cites one.

It refuses to write if any gate fails, and while `PLAN_MANUAL.md` is unsigned,
like every writer of the package. `--dry-run` runs the four gates, prints pass
or fail, and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out runs, r2 and r3.

  A1. **L₃'s notes frame the new rule as a particular case of another rule at
      least twice as often as L₂'s.** This is the `inside` code, among the
      births.
  A2. **At L₃, the births whose note frames them that way are narrow more
      often than the births whose note does not.** A proposer writing a
      subcase of a rule adds the ticket's attributes to it.
  A3. **At L₃, at least two thirds of the births coded `inside` that cite a
      hidden rule lie inside a rule they cite**, as written, over the space.
  A4. **The tickets' mix carries less than half of the gap in the narrow share
      between L₂ and L₃, under both readings, on the common support.** That
      gap is positive. On the same tickets the two levels write differently.
  A5. **At L₂, the births whose note appeals to the manual are narrow less
      often than the others.** A rule written from the prose paraphrases one of
      its sentences, and a sentence is broad.
  B1. **At L₁, at least three quarters of the rules that exclude the keyword
      mention it in their note.**
  B2. **At L₂, fewer than one in ten ordinary rules mention the keyword in
      their note.** None of them excludes it.
  B3. **At L₂, at least half of the keyword rules' notes state a precedence.**
      The prose's precedence is stated where the class's rules are born.
  B4. **At L₃, fewer than one in ten ordinary rules mention the keyword in
      their note.**
  B5. **At L₁, at least half of the ordinary rules mention it.**
  B6. **At L₁, a birth excludes the keyword more often when a rule shown at
      its escalation excludes it than when none does.** The exclusion is copied
      from the rules shown.

So the drafter expects the notes to say four things:
- The list narrows the rules because the proposer writes subcases of the
  manual's rules as if those rules were in the base.
- The prose broadens them because the proposer paraphrases its sentences.
- Under the prose and the rules, the keyword is out of view when an ordinary
  rule is written. The precedence is stated only where the class's own rules
  are born.
- Under the catalogue, the exclusion spreads from the first rules to the rest.

`IDEAS.md` asks whether the proposer leaves the keyword to a precedence it was
told. **The drafter expects no**: the proposer does not think of the keyword at
all when it writes an ordinary rule. The drafter trusts A4 least, then A3 and
B6.

**What the drafter had seen**:
- `FINDINGS_MANUAL.md` whole, every figure in it, including the per-run counts
  of keyword rules and the pooled counts of rules that exclude the keyword;
- `STATUS.md`'s and `IDEAS.md`'s entries on `PLAN_MANUAL.md`;
- `PLAN_MANUAL.md`'s §2, §4 and §5, the three texts among them;
- `manual/readings.py` and `manual/after_readings.py`;
- every note of the four development runs, with five things beside it: its
  rule's conditions and queue, the truth and the governing rule of the ticket
  it was born on, and whether the rule excludes the keyword (231 rules);
- three drafts of the codebook's counts by level on the development notes,
  each draft code's matches with their context, and the development notes no
  draft code matched;
- the length of every note in the twelve runs, and the number of rules in each
  run.

**What the drafter had not seen**:
- any note of a second or third run;
- the points off the keyword of any birth, in any run;
- any count of a code on the held-out runs;
- any code beside breadth, nesting, a ticket's queue, the rules shown at an
  escalation, or a declared edge, in any run;
- which rules of a second or third run exclude the keyword or are keyword
  rules, beyond the counts `FINDINGS_MANUAL.md` publishes.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for on 2026-10-23, after `manual/readings.py` and
`manual/after_readings.py`. The codebook was frozen on the development runs, and
the expectation above was written and committed before any held-out note was
read. Not a signed row, not on `STATUS.md`'s scoreboard, not a calibration
event. Zero API calls.

Usage:  python3 -m manual.notes --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m manual.notes
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

from harness.provenance import describe, environment

from blind import rows as brows
from edges.rebuild import rebuild

from . import after_readings as AR
from . import instrument as I
from . import plan
from . import readings as R
from .score import plain

# The codebook, frozen on the development runs. The patterns stay in Spanish:
# the notes they match are in Spanish, with the English forms the development
# notes showed.
CODES: dict[str, tuple[str, ...]] = {
    "hidden": (r"\bH(?:0[1-9]|1[0-9]|2[0-9])\b",),
    "policy": (r"\bpol[ií]tica\b", r"\bmanual\b", r"\bpolicy\b", r"\bpunto\s+[1-8]\b",
               r"\bsecci[oó]n\s+[1-8]\b"),
    "inside": (r"\bcaso particular\b", r"\bsub-?casos?\b", r"\bsubconjunto\b",
               r"\bsubcase\b", r"\b(?:particular|special) case\b",
               r"\bspecific case of\b"),
    "spec": (r"\bm[aá]s espec[ií]fic\w*", r"\bmore specific\b"),
    "narrow": (r"\bse crea una regla (?:m[aá]s )?espec[ií]fica\b",
               r"^\s*regla espec[ií]fica\b", r"\bperfil exacto\b",
               r"\bspecific rule for\b"),
    "widen": (r"\bgeneraliz\w*", r"\babstraer?\b", r"\bregla general para\b",
              r"\b(?:captura|cubre) el caso general\b",
              r"\bcualquier (?:cliente|tier|ticket|producto)\b",
              r"\b(?:casos?|otros) an[aá]logos\b"),
    "gap": (r"\bninguna regla\b", r"\bno (?:hay|existen?) (?:una |ninguna )?reglas?\b",
            r"\bno encajan? en (?:las |ninguna )?reglas?\b",
            r"\bno (?:est[aá]n? |quedan? )?cubiert\w*", r"\bhuecos?\b", r"\bsin regla\b",
            r"\bninguna casa\b", r"\bno cubren\b", r"\bcomplementari[ao]\b",
            r"\bno existing rules?\b", r"\bno rules?\b"),
    "analogy": (r"\bpor analog[ií]a\b", r"\ban[aá]log[ao] a\b",
                r"\bsiguiendo el patr[oó]n\b", r"\bcoherente con\b", r"\bsimilar a R\d",
                r"\bby analogy\b", r"\banalogous to\b"),
    "precedence": (r"\bprioridad (?:absoluta|sobre)\b", r"\btiene prioridad\b",
                   r"\bla prioridad es\b", r"\bes prioritari[ao]\b", r"\bprioriza\w*",
                   r"\bprevalec\w*", r"\bprecedencia\b", r"\bantes que\b",
                   r"\bpor encima de\b", r"\bimponerse\b", r"\bse impone\b",
                   r"\bprima sobre\b", r"\bjerarqu[ií]a\b",
                   r"\b(?:aplicarse|ir|va|van) primero\b", r"\btakes? precedence\b",
                   r"\bpriority over\b", r"\boverrid\w*"),
    "keyword": (r"\bseguridad\b", r"\bsecurity", r"security_keyword", r"\bkeyword\b",
                r"\bpalabra clave\b"),
}
CODEBOOK_DIGEST = "bea660598e6499b7"

SETS = {"development": (1,), "held_out": (2, 3), "all": (1, 2, 3)}
NOTE_CUT = 280                     # rung2/engine2.py cuts every note there
NARROW_BANDS = ("b1", "b2")        # manual/after_readings.py's two narrowest
LOW, HIGH = 2, 3                   # the gap is L3's narrow share less L2's
QUOTES = 3                         # quotations per code, level and set

# The expectation's lines.
A1_RATIO = 2
A3_NESTED = Fraction(2, 3)
A4_MIX = Fraction(1, 2)
B1_MENTION = Fraction(3, 4)
B2_MENTION = Fraction(1, 10)
B3_PRECEDENCE = Fraction(1, 2)
B4_MENTION = Fraction(1, 10)
B5_MENTION = Fraction(1, 2)

PROVENANCE = (
    "POST-RUN: asked for on 2026-10-23, after manual/readings.py and "
    "manual/after_readings.py. The codebook was frozen on the first run of each "
    "level, and the expectation in the module's docstring was written and "
    "committed before any note of a second or third run was read. Not a signed "
    "row; no verdict moves.")

_RX = {k: re.compile("|".join(v), 0 if k == "hidden" else re.IGNORECASE)
       for k, v in CODES.items()}


def record_path() -> Path:
    return plan.OUT / "notes.json"


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def digest() -> str:
    """The codebook's fingerprint: any edit to a pattern shows up here."""
    blob = json.dumps(CODES, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def code(note: str) -> frozenset[str]:
    return frozenset(k for k, rx in _RX.items() if rx.search(note or ""))


def cited(note: str) -> tuple[str, ...]:
    """The hidden rules a note names, each once, in the order it first names them."""
    out: list[str] = []
    for m in _RX["hidden"].finditer(note or ""):
        if m.group(0) not in out:
            out.append(m.group(0))
    return tuple(out)


def set_of(rep: int) -> str:
    return "development" if rep in SETS["development"] else "held_out"


# ---------------------------------------------------------------------------
# A: breadth
# ---------------------------------------------------------------------------

def narrow(points: int, cuts: Sequence[float]) -> bool:
    return AR.band(points, cuts) in NARROW_BANDS


def births_coded(births: Sequence[dict], notes: dict[str, str], ext: dict[str, int],
                 hidden: dict, cuts: Sequence[float]) -> list[dict]:
    """Every birth `K-a` reads, with its note's codes, the hidden rules it cites,
    and whether it lies inside one of them, over the space, as written."""
    out = []
    for b in births:
        note, E = notes[b["rule_id"]], ext[b["rule_id"]]
        cites = cited(note)
        out.append({
            "rule_id": b["rule_id"], "born_at": b["born_at"], "queue": b["queue"],
            "truth": b["truth"], "ticket_rule": b["ticket_rule"],
            "right_queue": b["right_queue"], "crosses": b["crosses"],
            "points_outside": b["points_outside"],
            "narrow": narrow(b["points_outside"], cuts),
            "codes": sorted(code(note)), "cited": list(cites),
            "nested_in_cited": any(R.contains(hidden[h]["ext"], E) for h in cites),
            "cites_ticket_rule": b["ticket_rule"] in cites,
        })
    return out


def narrow_split(items: Sequence[tuple[dict, str]], keys: Sequence[str]) -> dict[str, Any]:
    """`manual/after_readings.py`'s split, read on the narrow rate. That split
    counts a birth *alone* when it crosses nothing. Here a birth stands in it as
    crossing when it is not narrow, so its `alone` counts the narrow births and
    its `k_a` is the narrow share."""
    return AR.split([({"crosses": not b["narrow"]}, part) for b, part in items], keys)


def shown_split(s: dict[str, Any]) -> dict[str, Any]:
    """A split under the names this reading uses."""
    return {"births": s["births"], "narrow": s["alone"], "narrow_share": s["k_a"],
            "parts": {k: {"births": v["births"], "narrow": v["births"] - v["cross"]}
                      for k, v in s["parts"].items()}}


def median_points(bs: Sequence[dict]) -> float | None:
    return statistics.median(b["points_outside"] for b in bs) if bs else None


def side(bs: Sequence[dict]) -> dict[str, Any]:
    k = sum(b["narrow"] for b in bs)
    return {"births": len(bs), "narrow": k, "narrow_share": R.share(k, len(bs)),
            "points_median": median_points(bs)}


def by_code(bs: Sequence[dict]) -> dict[str, Any]:
    """Each code's births beside the births without it."""
    return {c: {"with": side([b for b in bs if c in b["codes"]]),
                "without": side([b for b in bs if c not in b["codes"]])}
            for c in CODES}


def code_mix(low: Sequence[dict], high: Sequence[dict], c: str) -> dict[str, Any]:
    """The gap in the narrow share between two levels, split by one code's mix."""
    keys = ("with", "without")
    part = lambda b: "with" if c in b["codes"] else "without"  # noqa: E731
    lo = narrow_split([(b, part(b)) for b in low], keys)
    hi = narrow_split([(b, part(b)) for b in high], keys)
    return AR.mix_split(lo, hi, keys)


def ticket_mix(low: Sequence[dict], high: Sequence[dict]) -> dict[str, Any]:
    """The same gap split by the tickets' true queues, on their common support."""
    keys = sorted({b["truth"] for b in low} & {b["truth"] for b in high})
    lo_c = [b for b in low if b["truth"] in keys]
    hi_c = [b for b in high if b["truth"] in keys]
    lo = narrow_split([(b, b["truth"]) for b in lo_c], keys)
    hi = narrow_split([(b, b["truth"]) for b in hi_c], keys)
    return {"queues": keys, "dropped": {"low": len(low) - len(lo_c),
                                        "high": len(high) - len(hi_c)},
            "low": shown_split(lo), "high": shown_split(hi),
            **AR.mix_split(lo, hi, keys)}


def citations(bs: Sequence[dict]) -> dict[str, Any]:
    """The births whose note cites hidden rules, against the rules they cite."""
    c = [b for b in bs if b["cited"]]
    inside = [b for b in c if "inside" in b["codes"]]
    own = [b for b in c if b["cites_ticket_rule"]]
    other = [b for b in c if not b["cites_ticket_rule"]]
    return {"births": len(bs), "citing": len(c),
            "nested_in_cited": sum(b["nested_in_cited"] for b in c),
            "inside_citing": len(inside),
            "inside_nested": sum(b["nested_in_cited"] for b in inside),
            "cites_ticket_rule": len(own),
            "right_queue": {"cites_ticket_rule": [sum(b["right_queue"] for b in own), len(own)],
                            "does_not": [sum(b["right_queue"] for b in other), len(other)]},
            "most_cited": Counter(h for b in c for h in b["cited"]).most_common(10)}


def level_a(bs: Sequence[dict]) -> dict[str, Any]:
    out = side(bs)
    out.update({"codes": by_code(bs), "citations": citations(bs)})
    return out


# ---------------------------------------------------------------------------
# B: the keyword
# ---------------------------------------------------------------------------

def admits_only_true(cond: dict) -> bool:
    """A condition on the keyword that lets only tickets with it through."""
    if cond["attr"] != brows.KW:
        return False
    op, v = cond["op"], cond["value"]
    return ((op == "eq" and v is True) or (op == "neq" and v is False)
            or (op == "in" and list(v) == [True]))


def rules_read(record: dict, ext: dict[str, int], outside: int,
               corpus: Sequence) -> list[dict]:
    """Every rule of a run, in birth order, with its note's codes, its kind, its
    ticket's keyword, and the rules shown at its escalation."""
    by_id = {r["rule_id"]: r for r in record["rules"]}
    rows = {r["idx"]: r for r in record["records"]}
    out = []
    for r in sorted(record["rules"], key=lambda r: (r["born_at"], r["rule_id"])):
        shown = rows[r["born_at"]]["shown_ids"]
        out.append({
            "rule_id": r["rule_id"], "born_at": r["born_at"], "queue": r["action"],
            "codes": sorted(code(r["note"])),
            "keyword_rule": brows.is_keyword(ext[r["rule_id"]], outside),
            "excludes": AR.excludes_keyword(r),
            "ticket_keyword": bool(corpus[r["born_at"]].has_security_keyword),
            "shown": list(shown),
            "shown_excluding": any(AR.excludes_keyword(by_id[s]) for s in shown),
            "declared": bool(r["beats"] or r["loses_to"] or r["dropped_edges"]),
        })
    return out


def ordinary(r: dict) -> bool:
    return not r["keyword_rule"] and not r["ticket_keyword"]


def mentions(rs: Sequence[dict]) -> dict[str, int]:
    return {"rules": len(rs), "mention": sum("keyword" in r["codes"] for r in rs)}


def level_b(rs: Sequence[dict]) -> dict[str, Any]:
    ords = [r for r in rs if ordinary(r)]
    kw = [r for r in rs if r["keyword_rule"]]
    shown = [r for r in rs if r["shown_excluding"]]
    unshown = [r for r in rs if not r["shown_excluding"]]
    return {
        "rules": len(rs), "excludes": sum(r["excludes"] for r in rs),
        "keyword_rules": len(kw),
        "ordinary": {**mentions(ords),
                     "excludes": mentions([r for r in ords if r["excludes"]]),
                     "does_not": mentions([r for r in ords if not r["excludes"]])},
        "excluding": mentions([r for r in rs if r["excludes"]]),
        "keyword_rule_notes": {"rules": len(kw),
                               "precedence": sum("precedence" in r["codes"] for r in kw),
                               "mention": sum("keyword" in r["codes"] for r in kw),
                               "declared": sum(r["declared"] for r in kw)},
        "imitation": {"shown_excluding": {"rules": len(shown),
                                          "excludes": sum(r["excludes"] for r in shown)},
                      "none_shown_excluding": {"rules": len(unshown),
                                               "excludes": sum(r["excludes"]
                                                               for r in unshown)}},
    }


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(A: dict, B: dict) -> list[dict[str, Any]]:
    """Every clause, read on the held-out sets `A` and `B`."""
    lv, kb = A["levels"], B["levels"]
    out = []

    def clause(c: str, holds: Any, reading: str) -> None:
        out.append({"clause": c, "holds": bool(holds), "reading": reading})

    def ratio(d: dict, part: str) -> Fraction | None:
        return R.share(d[part], d["rules"])

    s2 = R.share(lv["2"]["codes"]["inside"]["with"]["births"], lv["2"]["births"])
    s3 = R.share(lv["3"]["codes"]["inside"]["with"]["births"], lv["3"]["births"])
    clause("A1", s2 is not None and s3 is not None and s3 > 0 and s3 >= A1_RATIO * s2,
           f"inside: L3 {R.fmt(s3)} against L2 {R.fmt(s2)}")
    c3 = lv["3"]["codes"]["inside"]
    w, wo = c3["with"]["narrow_share"], c3["without"]["narrow_share"]
    clause("A2", R.less(wo, w), f"L3 narrow: with inside {R.fmt(w)}, without {R.fmt(wo)}")
    cit = lv["3"]["citations"]
    n, k = cit["inside_citing"], cit["inside_nested"]
    clause("A3", n and Fraction(k, n) >= A3_NESTED,
           f"{k} of {n} L3 births coded inside that cite a hidden rule lie inside one")
    m = A["ticket_mix"]
    lo, hi = m["mix_share_low_rates"], m["mix_share_high_rates"]
    clause("A4", m["gap"] is not None and m["gap"] > 0 and lo is not None
           and hi is not None and lo < A4_MIX and hi < A4_MIX,
           f"gap {R.fmt(m['gap'])} on the common support; the tickets' mix carries "
           f"{R.fmt(lo)} on L2's rates and {R.fmt(hi)} on L3's")
    p2 = lv["2"]["codes"]["policy"]
    w, wo = p2["with"]["narrow_share"], p2["without"]["narrow_share"]
    clause("A5", R.less(w, wo), f"L2 narrow: with policy {R.fmt(w)}, without {R.fmt(wo)}")

    e1 = kb["1"]["excluding"]
    r = ratio(e1, "mention")
    clause("B1", r is not None and r >= B1_MENTION,
           f"{e1['mention']} of {e1['rules']} L1 rules that exclude the keyword mention it")
    o2 = kb["2"]["ordinary"]
    r = ratio(o2, "mention")
    clause("B2", r is not None and r < B2_MENTION,
           f"{o2['mention']} of {o2['rules']} L2 ordinary rules mention the keyword")
    k2 = kb["2"]["keyword_rule_notes"]
    r = ratio(k2, "precedence")
    clause("B3", r is not None and r >= B3_PRECEDENCE,
           f"{k2['precedence']} of {k2['rules']} L2 keyword rules state a precedence")
    o3 = kb["3"]["ordinary"]
    r = ratio(o3, "mention")
    clause("B4", r is not None and r < B4_MENTION,
           f"{o3['mention']} of {o3['rules']} L3 ordinary rules mention the keyword")
    o1 = kb["1"]["ordinary"]
    r = ratio(o1, "mention")
    clause("B5", r is not None and r >= B5_MENTION,
           f"{o1['mention']} of {o1['rules']} L1 ordinary rules mention the keyword")
    im = kb["1"]["imitation"]
    a = R.share(im["shown_excluding"]["excludes"], im["shown_excluding"]["rules"])
    b = R.share(im["none_shown_excluding"]["excludes"], im["none_shown_excluding"]["rules"])
    clause("B6", R.less(b, a),
           f"L1 excludes: {R.fmt(a)} with an excluding rule shown, {R.fmt(b)} without")
    return out


# ---------------------------------------------------------------------------

def same_cuts(a: Sequence[float], b: Sequence[float]) -> bool:
    """Cuts recomputed here against a record's: floats, so with a tolerance."""
    return len(a) == len(b) and all(math.isclose(x, y, rel_tol=1e-12) for x, y in zip(a, b))


def quote(run: tuple[int, int], r: dict, note: str, **extra: Any) -> dict[str, Any]:
    return {"run": R.name(run), "rule_id": r["rule_id"], "born_at": r["born_at"],
            "queue": r["queue"], **extra, "note": note}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if [a for a in argv if a != "--dry-run"]:
        print(__doc__)
        return 2
    gate = plan.refuse_unsigned("manual/notes.py writes nothing")
    t0 = time.time()
    first = json.loads(R.record_path().read_text())
    after = json.loads(AR.record_path().read_text())
    recs, hidden = R.load_runs(), R.hidden_rules()
    sp, corpus, outside = I.space(), list(I.corpus()), I.outside()
    off: dict[str, list] = defaultdict(list)

    print("=" * 78)
    print("PLAN_MANUAL.md — WHAT THE PROPOSER WROTE BESIDE EACH RULE — POST-RUN")
    print("=" * 78)

    built = {run: rebuild(rec, corpus, sp) for run, rec in recs.items()}
    notes = {run: {r["rule_id"]: r["note"] for r in rec["rules"]} for run, rec in recs.items()}
    births = {}
    for run, rec in recs.items():
        rows = {r["idx"]: r for r in rec["records"]}
        births[run] = R.births_read(rec["rules"], rows, hidden,
                                    dict(built[run].engine.ext), outside)

    # Gate 1: the births and the bands are the readings'.
    for run in recs:
        theirs = first["A"]["births"][R.name(run)]
        if [(b["rule_id"], b["crosses"], b["class"]) for b in births[run]] != \
                [(b["rule_id"], b["crosses"], b["class"]) for b in theirs]:
            off["1"].append(f"{R.name(run)}:births")
    cuts = AR.edges_of([b["points_outside"] for run in recs if run[0] in (LOW, HIGH)
                        for b in births[run]])
    if not same_cuts(cuts, after["A"]["bands"]["cuts"]):
        off["1"].append("the cuts")

    # Gate 2: the notes are the records'.
    for run, rec in recs.items():
        born = {r["rule_id"]: r["born_at"] for r in rec["rules"]}
        rows = {r["idx"]: r for r in rec["records"]}
        for r in rec["rules"]:
            if not isinstance(r.get("note"), str) or len(r["note"]) > NOTE_CUT:
                off["2"].append(f"{R.name(run)}:{r['rule_id']}:note")
            for s in rows[r["born_at"]]["shown_ids"]:
                if s not in born or born[s] >= r["born_at"]:
                    off["2"].append(f"{R.name(run)}:{r['rule_id']}:shown {s}")
    if (set(SETS["development"]) & set(SETS["held_out"])
            or sorted(SETS["development"] + SETS["held_out"]) != list(range(1, plan.REPS + 1))
            or sorted(SETS["all"]) != list(range(1, plan.REPS + 1))):
        off["2"].append("the sets")

    # Gate 3: two routes give the keyword and the nesting.
    for run, rec in recs.items():
        ext = built[run].engine.ext
        for r in rec["rules"]:
            E = ext[r["rule_id"]]
            if AR.excludes_keyword(r) != (E & ~outside == 0):
                off["3"].append(f"{R.name(run)}:{r['rule_id']}:excludes")
            if brows.is_keyword(E, outside) != any(admits_only_true(c)
                                                   for c in r["conditions"]):
                off["3"].append(f"{R.name(run)}:{r['rule_id']}:keyword rule")
        for b in births[run]:
            E = ext[b["rule_id"]]
            for h in cited(notes[run][b["rule_id"]]):
                if h in hidden and (R.contains(hidden[h]["ext"], E)
                                    != R.contains(hidden[h]["ext"] & outside, E & outside)):
                    off["3"].append(f"{R.name(run)}:{b['rule_id']}:{h}")

    # Gate 4: the codebook is the one committed, and the identifiers the policy's.
    if digest() != CODEBOOK_DIGEST:
        off["4"].append("the digest")
    for run, rec in recs.items():
        for r in rec["rules"]:
            for h in cited(r["note"]):
                if h not in hidden or run[0] != 3:
                    off["4"].append(f"{R.name(run)}:{r['rule_id']}:{h}")

    checked = [{"gate": g, "what": what, "off": off.get(g, []), "passes": not off.get(g)}
               for g, what in (("1", "the births and the bands are the readings'"),
                               ("2", "the notes are the records'"),
                               ("3", "two routes give the keyword and the nesting"),
                               ("4", "the codebook is the one committed, and the "
                                     "identifiers the policy's"))]
    for g in checked:
        print(f"  gate {g['gate']}: {'PASS' if g['passes'] else 'FAIL'}  {g['what']}"
              + ("" if g["passes"] else f"  off: {g['off'][:12]}"))
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if dry:
        print(f"\n  --dry-run: the gates ran and nothing was written "
              f"({time.time() - t0:.0f} s).")
        return 0

    coded = {run: births_coded(births[run], notes[run], dict(built[run].engine.ext),
                               hidden, cuts) for run in recs}
    rules = {run: rules_read(rec, dict(built[run].engine.ext), outside, corpus)
             for run, rec in recs.items()}

    def pooled(by_run: dict, lv: int, reps: Sequence[int]) -> list[dict]:
        return [x for run in recs if run[0] == lv and run[1] in reps for x in by_run[run]]

    A: dict[str, Any] = {"cuts": cuts, "narrow_at_most": cuts[1]}
    B: dict[str, Any] = {}
    for s, reps in SETS.items():
        A[s] = {"levels": {str(lv): level_a(pooled(coded, lv, reps)) for lv in plan.LEVELS}}
        low, high = pooled(coded, LOW, reps), pooled(coded, HIGH, reps)
        A[s]["code_mix"] = {c: code_mix(low, high, c) for c in CODES}
        A[s]["ticket_mix"] = ticket_mix(low, high)
        B[s] = {"levels": {str(lv): level_b(pooled(rules, lv, reps)) for lv in plan.LEVELS}}

    # The census of the notes, and the quotations.
    census = {}
    for s, reps in SETS.items():
        census[s] = {}
        for lv in plan.LEVELS:
            rs = pooled(rules, lv, reps)
            census[s][str(lv)] = {
                "notes": len(rs),
                "at_the_cut": sum(len(notes[run][r["rule_id"]]) == NOTE_CUT
                                  for run in recs if run[0] == lv and run[1] in reps
                                  for r in rules[run]),
                "codes": {c: sum(c in r["codes"] for r in rs) for c in CODES},
                "uncoded": sum(not r["codes"] for r in rs)}
    held = [run for run in recs if run[1] in SETS["held_out"]]
    q: dict[str, Any] = {"by_code": {}, "uncoded": {}}
    for lv in plan.LEVELS:
        mine = [(run, r) for run in held if run[0] == lv for r in rules[run]]
        q["by_code"][str(lv)] = {c: [quote(run, r, notes[run][r["rule_id"]])
                                     for run, r in mine if c in r["codes"]][:QUOTES]
                                 for c in CODES}
        q["uncoded"][str(lv)] = [quote(run, r, notes[run][r["rule_id"]])
                                 for run, r in mine if not r["codes"]][:5]
    render = {run: {x.rule_id: x.render() for x in built[run].engine.rules} for run in recs}
    q["first_rules"] = [quote(run, rules[run][0], notes[run][rules[run][0]["rule_id"]],
                              rule=render[run][rules[run][0]["rule_id"]],
                              excludes=rules[run][0]["excludes"]) for run in recs]
    q["ordinary_mentioning_keyword"] = [
        quote(run, r, notes[run][r["rule_id"]], rule=render[run][r["rule_id"]])
        for run in held if run[0] in (LOW, HIGH) for r in rules[run]
        if ordinary(r) and "keyword" in r["codes"]]
    q["keyword_rules_l2"] = [
        quote(run, r, notes[run][r["rule_id"]], rule=render[run][r["rule_id"]],
              declared=r["declared"])
        for run in held if run[0] == LOW for r in rules[run] if r["keyword_rule"]]
    q["l1_exclusion_unshown"] = [
        quote(run, r, notes[run][r["rule_id"]], rule=render[run][r["rule_id"]],
              shown=r["shown"])
        for run in held if run[0] == 1 for r in rules[run]
        if r["excludes"] and not r["shown_excluding"]]

    expectation = read_expectation(A["held_out"], B["held_out"])
    for lv in plan.LEVELS:
        c = census["held_out"][str(lv)]
        print(f"  L{lv} held-out: {c['notes']} notes, "
              + ", ".join(f"{k} {v}" for k, v in c["codes"].items())
              + f", uncoded {c['uncoded']}")
    for e in expectation:
        print(f"  {e['clause']}: {'holds' if e['holds'] else 'FAILS'}  {e['reading']}")

    record_path().write_text(json.dumps(plain({
        "_env": environment(),
        "what": "the notes the proposer wrote beside its rules in PLAN_MANUAL.md's "
                "twelve loop runs, coded: why the list makes it write narrower rules, "
                "and why the catalogue makes it exclude the keyword",
        "plan": str(plan.PLAN),
        "gate": gate,
        "provenance": PROVENANCE,
        "follows": [str(R.record_path()), str(AR.record_path())],
        "source": {"records": [str(plan.loop_path(lv, rep)) for (lv, rep) in recs],
                   "policy": "HIDDEN_DSL, through manual/readings.py's hidden_rules"},
        "surface": "A reads the births K-a reads, by their points off the keyword, and "
                   "nests them in the rules their notes cite over the exhaustive space; "
                   "B reads every rule's extension against the keyword's half, and "
                   "each rule's birth ticket in the corpus",
        "codebook": {"codes": CODES, "digest": digest(), "sets": SETS,
                     "note_cut": NOTE_CUT},
        "gates": checked,
        "census": census,
        "A": A,
        "B": B,
        "rows": {R.name(run): [{"rule_id": r["rule_id"], "codes": r["codes"],
                                "cited": list(cited(notes[run][r["rule_id"]]))}
                               for r in rules[run]] for run in recs},
        "quotations": q,
        "expectation": expectation,
        "seconds": round(time.time() - t0, 1),
    }), indent=2, default=str, ensure_ascii=False) + "\n")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
