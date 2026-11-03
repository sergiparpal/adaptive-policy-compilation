"""
WHERE THE UNPLACED ANSWERS COME FROM. `FINDINGS_REASONED_LOOP.md`, *What Stage C
does not settle*, leaves this open. 95 of the 408 escalations ended unplaced, 38
of them in e r3, and every attempt ended `stop`, so the 95 are answers, not lost
calls. The reasoning is recorded whole on every attempt, and no stage codes it.
`IDEAS.md` carries the reading as free: a codebook frozen on part of the
reasoning would say why a listed rule was left out. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The placement rounds of the six runs.** Under v1b a draft that overlaps rules
of other queues over the space is sent back with those rules listed, `O`. The
answer must cite each of them in `beats` or `loses_to` (§5.2 of the plan). A
listed rule the answer does not cite is *missing*. An escalation with a missing
rule ends unplaced, and its rule is not born.

**Two texts the proposer reads disagree.**
- The system prompt, level 3's: *"Si tu regla es un caso particular de otra, no
  declares nada: el nivel 1 ya lo resuelve."*
- The placement message, v2b's: *"Situala frente a cada una de la lista."*
- `O` holds every rule of another queue that meets the draft. So it holds rules
  nested with the draft, which subsumption already orders.

**The reasoning of each placement call** is recorded whole. It is in Spanish,
English and Chinese, often more than one of them in a call.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  A. **By masks, reading no text.** Each listed rule's relation to the draft
     over the space: inside it, containing it, equal to it, or crossing it. The
     first three are *nested*. How often each relation is left out.
  B. **By the codebook.** What the reasoning says about each listed rule: that
     it is nested, that it is not, or that the two do not overlap or the rule
     does not apply. Or it says nothing the codes read, or never names the rule.

Each missing rule gets one cause:
  nested_said_nested    nested over the space, and the reasoning says nested;
  nested_not_said       nested, and the reasoning does not say so;
  crossing_said_apart   crossing, and the reasoning says the two do not overlap
                        or the rule does not apply;
  crossing_said_nested  crossing, not said apart, and the reasoning says nested;
  crossing_unmentioned  crossing, and the reasoning never names it;
  crossing_no_claim     crossing, named, with neither claim.
The rules the same answers placed are read the same way beside them.

--------------------------------------------------------------------------
THE CODEBOOK
--------------------------------------------------------------------------
**Development and held-out.**
- The codebook was written while reading the placement reasoning of the first
  run of each arm. That reading covered the text around every rule left out at
  their 24 unplaced escalations, and samples of what the drafts coded for rules
  placed.
- It was frozen before any reasoning of a second or third run was read. Those
  runs hold 71 unplaced escalations.
- The split is by run, as `manual/notes.py`'s is, because the proposer repeats
  its phrasing inside a run.
- **Every clause below reads the held-out runs.** The development figures sit
  beside them.

**A listed rule's text** is the sentences of the placement call's reasoning
that name its identifier. Each comes with the next sentence, when that one
names no rule (`FOLLOW`). A sentence ends at a line break, at `.`, `!`, `?` or
`;` before a space, and at their Chinese forms.

**Three codes**, each a set of patterns, matched ignoring case. A question
claims nothing.
  nested      a containment term with no negation in the `NEAR` characters
              before it: contenida, contiene, subconjunto, caso particular,
              caso especial, nivel 1; contained, contains, subset, special case,
              particular case, level 1; 包含, 子集, 特例.
  not_nested  the same terms with a negation in those characters: no, ni,
              sin, tampoco, ninguna; not, neither, nor, non, n't; 不, 非, 无, 没.
              A negation further back belongs to another clause: *"No incluimos
              R0025 porque está contenida"* says nested.
  apart       no aplica, no se solapa, no hay solapamiento, no casa,
              excluyentes, disjuntos; no overlap, doesn't overlap, does not
              apply, mutually exclusive, disjoint; 无重叠, 不重叠, 互斥, 不适用.

A text can carry any number of codes. **Every count of a code is
approximate**: a code can match a sentence about another rule, and miss a claim
made in words the patterns lack. What is read is the comparison between the
rules left out and the rules placed, under one codebook. `CODEBOOK_DIGEST`
fingerprints the patterns, and the tests pin it.

--------------------------------------------------------------------------
WHAT IT READS
--------------------------------------------------------------------------
- The six run records, read-only, and `score.json` for gate 1.
- Every escalation whose placement answer kept the draft's rule: those that
  ended born, and those that ended unplaced. Answers that changed the rule or
  failed the validator are counted apart.
- By set, by arm and pooled:
  - the census;
  - the omission rate by relation;
  - the causes of the missing rules;
  - each code's share among the missing and among the placed, by relation;
  - the unplaced escalations every one of whose missing rules has a stated
    cause.
- In every run, the unplaced escalations that left out a rule whose region is
  the whole space.
- Quotations: for each cause, the coded sentences of the first held-out rules
  with it, in run order.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The census is the record's.** Each run's verdicts are `score.json`'s.
     Every unplaced escalation's missing rules are its loop's own list: not
     empty, all of them listed, and none of them cited by the answer.
  2. **The draft is the draft.** Every answer read covers exactly the draft's
     cases over the space. So each relation is read against the rule the
     proposer kept.
  3. **The codebook is the one committed**, and the sets split the runs by
     repetition: the first is development, the second and third held-out.
  4. **The reasoning is the record's.** Every placement call read carries its
     reasoning, and every attempt of it that reached the model ended `stop`.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates, prints pass or fail,
and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
Every clause reads the held-out runs, r2 and r3 of both arms.

  U1. **A nested rule is left out at least four times as often as a crossing
      one**, each over the listed rules of its relation.
  U2. **At least three quarters of the missing nested rules are said nested.**
  U3. **At least half of the missing crossing rules are said apart or said
      nested.**
  U4. **Saying apart singles a crossing rule out.** Among the crossing rules,
      the share said apart is at least four times as high among the missing as
      among the placed.
  U5. **e r3's default.** e r3 wrote a rule whose region is the whole space at
      case 1. At least half of its unplaced escalations left out a rule whose
      region is the whole space.

So the drafter expects the unplaced answers to come mostly from the protocol's
two texts. The proposer leaves out the rules nested with its draft, as the
system prompt tells it to, and the placement round lists them. The crossing
rules it leaves out, it mostly takes for nested or for apart. The drafter trusts
U2 most and U5 least, then U3.

**What the drafter had seen**:
- `FINDINGS_REASONED_LOOP.md` whole, with every figure in it, and `STATUS.md`'s
  and `IDEAS.md`'s entries on the plan;
- the level-3 system prompt's paragraphs on the engine's two levels and on
  `beats` and `loses_to`, and v2b's placement message;
- in the development runs: the structure of every unplaced answer, the relation
  of every listed rule to its draft and whether it matches the escalated ticket,
  the reasoning around every rule left out, one placement reasoning whole, and
  samples of the sentences each draft code matched for rules placed;
- four drafts of the codebook's counts on the development runs, with samples
  of the rules each code marked among the rules placed;
- each run's verdicts and number of placement rounds, which read no text.

**What the drafter had not seen**: any reasoning of a second or third run, any
relation or code in them, or which rules their unplaced escalations left out.
The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for on 2026-11-03, after `PLAN_REASONED_LOOP.md` closed and
after `reasoned_loop/decided.py`. The codebook was frozen on the first run of
each arm, and the expectation above was written and committed before any
held-out reasoning was read. Not a signed row, not on `STATUS.md`'s scoreboard,
not a calibration event. Zero API calls.

Usage:  python3 -m reasoned_loop.unplaced --dry-run   # gates 1 to 4; writes nothing
        PYTHONHASHSEED=0 python3 -m reasoned_loop.unplaced
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from typing import Any, Iterable

from harness.provenance import describe, environment

from authorship import protocol as e
from blind import rows as brows
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Space, strictly_below

from . import plan, score

F = Fraction

# The codebook, frozen on the development runs. The patterns keep the reasoning's
# three languages.
NESTED = (r"contenid[ao]s?", r"\bcontiene\b", r"\bsubconjunto\b",
          r"\bcaso (?:particular|especial)\b", r"\bnivel 1\b", r"\bcontain(?:s|ed)?\b",
          r"\bsubset\b", r"\b(?:special|particular) case\b", r"\blevel 1\b",
          r"包含", r"子集", r"特例")
APART = (r"\bno aplica\b", r"\bno se solapa", r"\bno (?:hay|existe) solapamiento\b",
         r"\bno casa\b", r"\bexcluyentes?\b", r"\bdisjunt[ao]s?\b", r"\bno overlap\b",
         r"\bdo(?:es)?n'?t overlap\b", r"\bdo(?:es)? not overlap\b",
         r"\bdo(?:es)? not apply\b", r"\bdo(?:es)?n'?t apply\b", r"\bmutually exclusive\b",
         r"\bdisjoint\b", r"无重叠", r"不重叠", r"互斥", r"不适用")
NEGATION = r"\b(?:not|no|neither|nor|non|sin|ni|tampoco|ninguna?)\b|n't|[不非无没]"
NEAR = 25                          # characters before a containment term a negation reaches
QUESTION = r"[?？]\s*$"
SPLIT = r"(?<=[.!?;])\s+|(?<=[。！？；])\s*|\n+"
RULE_ID = r"\bR\d{4}\b"
FOLLOW = 1                         # sentences after one that names the rule
CODEBOOK_DIGEST = "ccd5d3d68e09c8dc"

P_NESTED = [re.compile(p, re.IGNORECASE) for p in NESTED]
P_APART = [re.compile(p, re.IGNORECASE) for p in APART]
P_NEGATION = re.compile(NEGATION, re.IGNORECASE)
P_QUESTION = re.compile(QUESTION)
P_SPLIT = re.compile(SPLIT)
P_RULE_ID = re.compile(RULE_ID)

SETS = {"development": (1,), "held_out": (2, 3), "all": (1, 2, 3)}
NESTED_RELATIONS = ("inside_draft", "contains_draft", "equal")
CAUSES = ("nested_said_nested", "nested_not_said", "crossing_said_apart",
          "crossing_said_nested", "crossing_unmentioned", "crossing_no_claim")
STATED = {"nested_said_nested", "crossing_said_apart", "crossing_said_nested"}
READ = (e.BORN, e.UNPLACED)        # the answers that kept the draft's rule
QUOTES = 2                         # held-out rules quoted per cause
QUOTE_CHARS = 300

# The expectation's lines.
U1_RATIO = 4
U2_SHARE = F(3, 4)
U3_SHARE = F(1, 2)
U4_RATIO = 4
U5_SHARE = F(1, 2)
DEFAULT_RUN = "e_r3"

PROVENANCE = (
    "POST-RUN: asked for on 2026-11-03, after PLAN_REASONED_LOOP.md closed. The "
    "codebook was frozen on the first run of each arm, and the expectation in the "
    "module's docstring was written and committed before any held-out reasoning "
    "was read. Not a signed row; no verdict moves.")


def record_path():
    return plan.OUT / "unplaced.json"


def digest() -> str:
    body = json.dumps([NESTED, APART, NEGATION, NEAR, QUESTION, SPLIT, RULE_ID, FOLLOW],
                      ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def frac(x: Fraction | None) -> dict[str, Any] | None:
    return score.frac(x)


def set_of(rep: int) -> str:
    return "development" if rep in SETS["development"] else "held_out"


# ---------------------------------------------------------------------------
# The codebook
# ---------------------------------------------------------------------------

def sentences(text: str | None) -> list[str]:
    return [s.strip() for s in P_SPLIT.split(text or "") if s and s.strip()]


def text_of(rule_id: str, sents: list[str]) -> list[str]:
    """The sentences that name `rule_id`, each with the `FOLLOW` sentences after
    it that name no rule."""
    out = []
    for i, s in enumerate(sents):
        if rule_id in P_RULE_ID.findall(s):
            out.append(s)
            for t in sents[i + 1:i + 1 + FOLLOW]:
                if P_RULE_ID.search(t):
                    break
                out.append(t)
    return out


def codes_of(sentence: str) -> set[str]:
    """A sentence's codes. A containment term is negated when a negation lies in
    the `NEAR` characters before it, and a question claims nothing."""
    out = set()
    if any(p.search(sentence) for p in P_APART):
        out.add("apart")
    if P_QUESTION.search(sentence):
        return out
    for p in P_NESTED:
        for m in p.finditer(sentence):
            before = sentence[max(0, m.start() - NEAR):m.start()]
            out.add("not_nested" if P_NEGATION.search(before) else "nested")
    return out


def code(text: Iterable[str]) -> frozenset[str]:
    out: set[str] = set()
    for s in text:
        out |= codes_of(s)
    return frozenset(out)


# ---------------------------------------------------------------------------
# The rules listed at a placement round
# ---------------------------------------------------------------------------

def relation(ext: int, draft: int) -> str:
    if ext == draft:
        return "equal"
    if strictly_below(ext, draft):
        return "inside_draft"
    if strictly_below(draft, ext):
        return "contains_draft"
    return "crossing"


def nested(rel: str) -> bool:
    return rel in NESTED_RELATIONS


def cause(rel: str, codes: frozenset[str], mentioned: bool) -> str:
    if nested(rel):
        return "nested_said_nested" if "nested" in codes else "nested_not_said"
    if "apart" in codes:
        return "crossing_said_apart"
    if "nested" in codes:
        return "crossing_said_nested"
    return "crossing_no_claim" if mentioned else "crossing_unmentioned"


def placement(esc: dict) -> dict | None:
    calls = [c for c in esc.get("calls") or [] if c["round"] == 1]
    return calls[0] if calls else None


def cited(payload: dict) -> set[str]:
    return set(e.citations(payload, "beats")) | set(e.citations(payload, "loses_to"))


def rows_of(record: dict, space: Space) -> tuple[list[dict], list[dict]]:
    """Every listed rule of every placement answer that kept the draft's rule,
    and every placement escalation, each with what this module reads of it."""
    ext = {r["rule_id"]: brows.ext_of(r, space) for r in record["rules"]}
    tag = plan.tag(record["arm"], record["rep"])
    rows, escalations = [], []
    for esc in record["escalations"]:
        c1 = placement(esc)
        if c1 is None or not esc.get("listed"):
            continue
        listed = list(esc["listed"])
        missing = list(c1.get("unplaced") or [])
        draft = brows.ext_of({"conditions": esc["calls"][0]["payload"]["conditions"]}, space)
        entry = {"run": tag, "idx": esc["idx"], "cause": esc["kind"],
                 "verdict": esc["verdict"], "listed": len(listed), "missing": len(missing)}
        escalations.append(entry)
        if esc["verdict"] not in READ:
            continue
        sents = sentences(c1.get("reasoning"))
        for rid in listed:
            mine = text_of(rid, sents)
            codes = code(mine)
            rel = relation(ext[rid], draft)
            rows.append({"run": tag, "arm": record["arm"], "rep": record["rep"],
                         "idx": esc["idx"], "rule": rid, "verdict": esc["verdict"],
                         "missing": rid in missing, "listed": len(listed), "relation": rel,
                         "whole_space": ext[rid] == space.full,
                         "mentions": sum(rid in P_RULE_ID.findall(s) for s in sents),
                         "codes": sorted(codes), "cause": cause(rel, codes, bool(mine)),
                         "coded_sentences": [s for s in mine if codes_of(s)]})
    return rows, escalations


# ---------------------------------------------------------------------------
# The readings
# ---------------------------------------------------------------------------

def share(part: int, whole: int) -> Fraction | None:
    return F(part, whole) if whole else None


def omission(rows: list[dict]) -> dict[str, Any]:
    out = {}
    groups = {"nested": lambda r: nested(r["relation"]),
              "crossing": lambda r: r["relation"] == "crossing",
              **{rel: (lambda rel: lambda r: r["relation"] == rel)(rel)
                 for rel in NESTED_RELATIONS}}
    for name, keep in groups.items():
        rs = [r for r in rows if keep(r)]
        m = sum(r["missing"] for r in rs)
        out[name] = {"listed": len(rs), "missing": m, "rate": frac(share(m, len(rs))),
                     "rate_exact": share(m, len(rs))}
    return out


def code_shares(rows: list[dict]) -> dict[str, Any]:
    """Each code's share, and the share never named, among the rules left out and
    among the rules placed, by relation."""
    out: dict[str, Any] = {}
    for side, missing in (("missing", True), ("placed", False)):
        for rel_name, keep in (("nested", lambda r: nested(r["relation"])),
                               ("crossing", lambda r: r["relation"] == "crossing")):
            rs = [r for r in rows if r["missing"] == missing and keep(r)]
            cell = {"rules": len(rs)}
            for c in ("nested", "not_nested", "apart"):
                n = sum(c in r["codes"] for r in rs)
                cell[c] = {"count": n, "share": frac(share(n, len(rs))),
                           "share_exact": share(n, len(rs))}
            n = sum(r["mentions"] == 0 for r in rs)
            cell["unmentioned"] = {"count": n, "share": frac(share(n, len(rs))),
                                   "share_exact": share(n, len(rs))}
            out[f"{side}_{rel_name}"] = cell
    return out


def causes(rows: list[dict]) -> dict[str, int]:
    c = Counter(r["cause"] for r in rows if r["missing"])
    return {k: c.get(k, 0) for k in CAUSES}


def stated_escalations(rows: list[dict]) -> dict[str, int]:
    by: dict[tuple[str, int], list[str]] = {}
    for r in rows:
        if r["missing"]:
            by.setdefault((r["run"], r["idx"]), []).append(r["cause"])
    return {"unplaced": len(by),
            "every_missing_rule_stated": sum(all(c in STATED for c in cs) for cs in by.values()),
            "every_missing_rule_nested": sum(all(c.startswith("nested") for c in cs)
                                             for cs in by.values())}


def whole_space(rows: list[dict]) -> dict[str, Any]:
    """By run: the unplaced escalations, and those that left out a rule whose
    region is the whole space."""
    out: dict[str, Any] = {}
    for r in rows:
        if r["verdict"] != e.UNPLACED:
            continue
        cell = out.setdefault(r["run"], {"unplaced": set(), "left_out_the_whole_space": set(),
                                         "listed_the_whole_space": set()})
        cell["unplaced"].add(r["idx"])
        if r["whole_space"]:
            cell["listed_the_whole_space"].add(r["idx"])
            if r["missing"]:
                cell["left_out_the_whole_space"].add(r["idx"])
    return {t: {k: len(v) for k, v in c.items()} for t, c in sorted(out.items())}


def reading(rows: list[dict]) -> dict[str, Any]:
    return {"listed_rules": len(rows), "missing_rules": sum(r["missing"] for r in rows),
            "unplaced_escalations": len({(r["run"], r["idx"]) for r in rows
                                         if r["verdict"] == e.UNPLACED}),
            "omission": omission(rows), "causes": causes(rows),
            "codes": code_shares(rows), "escalations": stated_escalations(rows)}


def readings(rows: list[dict]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, reps in SETS.items():
        rs = [r for r in rows if r["rep"] in reps]
        out[name] = {"pooled": reading(rs),
                     **{a: reading([r for r in rs if r["arm"] == a]) for a in plan.ARMS}}
    return out


def quotes(rows: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {k: [] for k in CAUSES}
    for r in rows:
        if r["missing"] and set_of(r["rep"]) == "held_out" and len(out[r["cause"]]) < QUOTES:
            out[r["cause"]].append({"run": r["run"], "idx": r["idx"], "rule": r["rule"],
                                    "relation": r["relation"],
                                    "sentences": [s[:QUOTE_CHARS]
                                                  for s in r["coded_sentences"][:3]]})
    return out


def read_expectation(held_out: dict[str, Any], by_run: dict[str, Any]) -> list[dict[str, Any]]:
    om, co = held_out["omission"], held_out["codes"]
    rn, rc = om["nested"]["rate_exact"], om["crossing"]["rate_exact"]
    miss_n, miss_c = co["missing_nested"], co["missing_crossing"]
    said_nested = held_out["causes"]["nested_said_nested"]
    stated_c = held_out["causes"]["crossing_said_apart"] + held_out["causes"]["crossing_said_nested"]
    apart_m = miss_c["apart"]["share_exact"]
    apart_p = co["placed_crossing"]["apart"]["share_exact"]
    d = by_run.get(DEFAULT_RUN, {"unplaced": 0, "left_out_the_whole_space": 0})
    u2 = share(said_nested, miss_n["rules"])
    u3 = share(stated_c, miss_c["rules"])
    u5 = share(d["left_out_the_whole_space"], d["unplaced"])
    return [
        {"clause": "U1", "what": "a nested rule is left out at least four times as often as a "
                                 "crossing one",
         "reading": {"nested": frac(rn), "crossing": frac(rc)},
         "holds": rn is not None and rc is not None and rn >= U1_RATIO * rc},
        {"clause": "U2", "what": "at least three quarters of the missing nested rules are said "
                                 "nested",
         "reading": {"said_nested": said_nested, "of": miss_n["rules"], "share": frac(u2)},
         "holds": u2 is not None and u2 >= U2_SHARE},
        {"clause": "U3", "what": "at least half of the missing crossing rules are said apart or "
                                 "said nested",
         "reading": {"stated": stated_c, "of": miss_c["rules"], "share": frac(u3)},
         "holds": u3 is not None and u3 >= U3_SHARE},
        {"clause": "U4", "what": "among crossing rules, the share said apart is at least four "
                                 "times as high among the missing as among the placed",
         "reading": {"missing": frac(apart_m), "placed": frac(apart_p)},
         "holds": apart_m is not None and apart_p is not None and apart_m >= U4_RATIO * apart_p},
        {"clause": "U5", "what": "at least half of e r3's unplaced escalations left out a rule "
                                 "whose region is the whole space",
         "reading": {"left_out": d["left_out_the_whole_space"], "of": d["unplaced"],
                     "share": frac(u5)},
         "holds": u5 is not None and u5 >= U5_SHARE},
    ]


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def census_gate(record: dict, published: dict) -> bool:
    tag = plan.tag(record["arm"], record["rep"])
    verdicts = Counter(esc["verdict"] for esc in record["escalations"])
    if dict(verdicts) != published["RL-h"]["runs"][tag]["placements"]["verdicts"]:
        return False
    for esc in record["escalations"]:
        if esc["verdict"] != e.UNPLACED:
            continue
        c1 = placement(esc)
        if c1 is None or not c1.get("payload"):
            return False
        missing = c1.get("unplaced") or []
        if not missing or not set(missing) <= set(esc.get("listed") or []):
            return False
        if set(missing) & cited(c1["payload"]):
            return False
    return True


def draft_gate(record: dict, space: Space) -> bool:
    for esc in record["escalations"]:
        c1 = placement(esc)
        if c1 is None or esc["verdict"] not in READ or not esc.get("listed"):
            continue
        first = brows.ext_of({"conditions": esc["calls"][0]["payload"]["conditions"]}, space)
        second = brows.ext_of({"conditions": c1["payload"]["conditions"]}, space)
        if first != second or esc["calls"][0]["payload"]["action"] != c1["payload"]["action"]:
            return False
    return True


def reasoning_gate(record: dict) -> bool:
    for esc in record["escalations"]:
        c1 = placement(esc)
        if c1 is None or esc["verdict"] not in READ or not esc.get("listed"):
            continue
        if not c1.get("reasoning"):
            return False
        reached = [a for a in c1.get("call_attempts") or [] if a.get("provider")]
        if not reached or any(a.get("finish_reason") != "stop" for a in reached):
            return False
    return True


def check(records: dict[str, dict], published: dict, space: Space) -> list[dict[str, Any]]:
    out = []
    for t, rec in records.items():
        out.append({"gate": 1, "run": t, "what": "the census is the record's",
                    "passes": census_gate(rec, published)})
        out.append({"gate": 2, "run": t, "what": "the draft is the draft",
                    "passes": draft_gate(rec, space)})
        out.append({"gate": 4, "run": t, "what": "the reasoning is the record's",
                    "passes": reasoning_gate(rec)})
    reps = sorted({rec["rep"] for rec in records.values()})
    out.append({"gate": 3, "run": "pooled", "what": "the codebook is the one committed, and "
                                                    "the sets split the runs by repetition",
                "passes": (digest() == CODEBOOK_DIGEST and reps == list(SETS["all"])
                           and [set_of(r) for r in reps]
                           == ["development", "held_out", "held_out"])})
    return out


# ---------------------------------------------------------------------------
# The writer
# ---------------------------------------------------------------------------

def plain(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items() if not k.endswith("_exact")}
    if isinstance(x, list):
        return [plain(v) for v in x]
    return x


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Where the unplaced answers come from "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true",
                    help="run gates 1 to 4 and stop; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"reasoned_loop/unplaced.py writes {record_path()}")
    published = json.loads(plan.score_path().read_text())
    by_arm, missing_runs = score.read_records()
    if missing_runs:
        sys.exit(f"\nREFUSED: runs missing: {missing_runs}; nothing was written.\n")
    records = {plan.tag(a, rec["rep"]): rec for a in plan.ARMS for rec in by_arm[a]}
    space = MI.space()
    checked = check(records, published, space)
    for g in sorted(checked, key=lambda g: (g["gate"], str(g["run"]))):
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    if not all(g["passes"] for g in checked):
        sys.exit("\nREFUSED: a gate failed; nothing was written.\n")
    if args.dry_run:
        print("\ndry run: nothing written")
        return 0
    rows, escalations = [], []
    for t in sorted(records, key=lambda t: (records[t]["rep"], t)):
        rs, es = rows_of(records[t], space)
        rows += rs
        escalations += es
    by_set = readings(rows)
    by_run = whole_space(rows)
    expectation = read_expectation(by_set["held_out"]["pooled"], by_run)
    record_path().write_text(json.dumps(st._rounded(plain({
        "_env": environment(),
        "plan": str(plan.PLAN),
        "signature": gate,
        "provenance": PROVENANCE,
        "codebook": {"digest": CODEBOOK_DIGEST, "nested": NESTED, "apart": APART,
                     "negation": NEGATION, "question": QUESTION, "split": SPLIT,
                     "rule_id": RULE_ID, "follow": FOLLOW},
        "sets": {k: list(v) for k, v in SETS.items()},
        "constants": {"QUOTES": QUOTES, "QUOTE_CHARS": QUOTE_CHARS},
        "gates": checked,
        "verdicts_apart": dict(Counter(es["verdict"] for es in escalations
                                       if es["verdict"] not in READ)),
        "readings": by_set,
        "whole_space_by_run": by_run,
        "expectation": expectation,
        "quotes": quotes(rows),
        "escalations": escalations,
        "rows": [{k: v for k, v in r.items() if k != "coded_sentences"} for r in rows],
    })), indent=2, ensure_ascii=False, default=str) + "\n")
    for c in expectation:
        print(f"  {c['clause']}: {'holds' if c['holds'] else 'fails'}")
    print(f"\n-> {record_path()}\n  {describe()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
