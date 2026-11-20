"""
WHY ONE PROMPT DREW DIFFERENT DRAFTS. `FINDINGS_RANKED.md`, *Six things Stage C
left free*, B, found that at the tickets that begot a rule reaching into the
keyword's region, the first calls of two runs that asked the ticket as a
reported error drew the same queue and extension in three pairs of nine. A
ticket's first call is sent the same texts in every run and in both arms, so one
prompt drew different drafts. Its *What it does not settle*, fourth item, says
that each first call's reasoning is in the records, and that no stage codes it.
`IDEAS.md` carries it under *What `PLAN_RANKED.md` opens*. Asked for by Sergi on
2026-11-20, with *Why K r2's conflicts fell where its ranking errs*, which
`ranked/conflicts.py` reads. POST-RUN.

--------------------------------------------------------------------------
THE MATERIAL
--------------------------------------------------------------------------
**The six runs**, `results_ranked/loop_{l,k}_r{1,2,3}.json`. Every escalation
keeps its first call: the draft, the reasoning whole, and what OpenRouter said
of each attempt, among it the provider, the system fingerprint and the tokens.
The requests were sent at temperature 0, with reasoning at high effort, to
DeepInfra's fp8 endpoint alone.

**A first call's prompt** is two messages: level 1's system prompt, and the blind
user message, which is v2b's paragraph and the ticket's eight attributes, with
the report naming the ticket's true queue after the paragraph at a reported
error (`corrections/protocol.messages_for`). Nothing else enters it: not the
arm, the run, the base, nor the case's place among the arrivals. So two first
calls are **sent the same prompt** when their tickets carry the same attributes
and neither carries a report, or both carry reports naming the same queue. An
impasse in either arm and a conflict L asked about send the same prompt.

**A draft** is a first call's queue and its extension over the space. **A pair**
is two first calls sent the same prompt, in two runs or at two cases of one run,
classed:
- `same`: the same queue and the same extension;
- `same_queue`: the same queue and another extension;
- `other_queue`: two queues;
- `invalid`: a draft without a queue, or one that builds no extension.

**Where two reasonings part** is the length of their common prefix, in
characters.

--------------------------------------------------------------------------
THE QUESTIONS
--------------------------------------------------------------------------
  H-a. **How often one prompt draws one draft.** The pairs by class, with a
       report and without; and for each prompt asked several times, how many
       drafts its calls drew.
  H-b. **Where two answers part.** For every pair, where its reasonings part:
       by class, the median and the extremes, how many part within 50, 100,
       200, 500 and 1,000 characters, and how many are the same text.
  H-c. **What differs between two drafts of one queue.** Of the `same_queue`
       pairs, those whose drafts condition on other attributes, and those on the
       same attributes with other values, attribute by attribute.
  H-d. **At the exception's tickets.** Every pair at a ticket of `H03` whose
       report named `T2_TECHNICAL`: both drafts' conditions, where the
       reasonings part, and of each reasoning a window from there and its end,
       kept for reading.
  Beside them: the provider and the system fingerprint of every attempt, and
  the median reasoning of a first call, in tokens and in characters.

--------------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------------
  1. **The texts are the protocol's.** Every run's system prompt, blind
     paragraph and report template are `corrections/protocol.py`'s.
  2. **One attempt, no retry.** Every first call was answered at its first
     attempt, with no retry message and no failure, so what it sent is
     `messages_for`'s.
  3. **One prompt, one count of tokens.** Within each prompt, every first call's
     prompt tokens are the same.
  4. **A report is the ticket's own.** A first call carries a report exactly
     when its escalation is a reported error, and the report names the case's
     true queue.
  5. **A born draft is its rule.** At every birth, the first call's draft has
     the born rule's queue and extension.

It refuses to write if any gate fails, and while the plan is unsigned, like
every writer of the package. `--dry-run` runs the gates and writes nothing.

--------------------------------------------------------------------------
WHAT IS EXPECTED, WRITTEN BEFORE THE READING AND NOT SIGNED
--------------------------------------------------------------------------
  H1. **One prompt, mostly other drafts.** Fewer than half of the pairs drew the
      same queue and extension.
  H2. **The report holds the queue.** Of the pairs whose prompt carries a
      report, more than nine in ten drew the same queue.
  H3. **The answers part at once.** In more than half of the pairs, the
      reasonings part within their first 200 characters.
  H4. **Never one reasoning.** No pair's reasonings are the same text.
  H5. **Other attributes, not other values.** Of the `same_queue` pairs, more
      than half condition on other attributes.
  H6. **Without a report, one queue still.** Of the pairs whose prompt carries
      no report, more than half drew the same queue.

A clause that reads a missing value fails.

**The drafter's account.**
- **H1.** B found three pairs of nine alike at the exception's tickets.
  `FINDINGS_HALVES.md` found that two asks of one prompt shared a class in about
  half the prompts, and an extension is finer than a class.
- **H3 and H4.** Sent at temperature 0, a decoder that took the likeliest token
  every time would give one prompt one reasoning, and two answers could part
  only where two tokens were nearly tied, anywhere in the text. Different drafts
  in two pairs of three say the reasoning is drawn. The drafter expects it
  sampled: the answers part in their first sentences, where a reasoning restates
  the ticket in words of its own choosing, and no two are the same text.
- **H2.** A report names the queue, and B found every first call told
  `T2_TECHNICAL` at the exception's tickets drafting that queue.
- **H5.** At case 238 the drafts differ in an attribute, the tier kept or
  dropped, and at case 529 in a value, severity's bound. A blind first call
  told a label has to guess why, and the drafter expects the guess to choose
  the attribute more often than the bound.
- **H6.** Without a report the queue is the model's own reading of the
  catalogue, which the drafter expects to be steadier than the region it
  draws.

**The bet is H3.** **H2 and H4 are trusted most.** **H5 and H6 are trusted
least.**

**What the drafter had seen**:
- `FINDINGS_RANKED.md` whole, among it B's drafts at cases 529 and 238;
  `FINDINGS_HALVES.md`'s finding on two asks of one prompt; `STATUS.md`'s and
  `IDEAS.md`'s entries on `PLAN_RANKED.md`; `corrections/protocol.py`, which
  builds the first call's messages, and `blind/loop.py`, which refuses a
  placement that changes the draft;
- the records' layouts, by their keys, and their settings: temperature 0,
  reasoning at high effort, 16,000 tokens, DeepInfra's fp8 endpoint;
- one first call of K's smoke run, at case 0: its length, and the first 700
  characters of its reasoning, which restate the ticket and weigh
  `ACCOUNT_MANAGER`;
- the counts by prompt, without a draft or a reasoning: 1,822 first calls in
  the six runs, 1,098 prompts, 411 sent twice or more, 292 of them with a
  report, 1,273 pairs, and 33 prompts sent twice within one run; every first
  call answered at its first attempt, with no retry, by DeepInfra, and no
  attempt with a system fingerprint.

**What the drafter had not seen**: any draft or reasoning of the six runs
beyond what `FINDINGS_RANKED.md` names; any pair's class or where its
reasonings part.

The dry run ran before the expectation was committed, and printed pass or fail
alone.

--------------------------------------------------------------------------
PROVENANCE
--------------------------------------------------------------------------
**POST-RUN.** Asked for by Sergi on 2026-11-20, after `ranked/readings.py`'s
six readings. The expectation above was written and committed before the
reading ran. Not a signed row, not on `STATUS.md`'s scoreboard, not a
calibration event. Zero API calls.

Usage:  python3 -m ranked.drafts --dry-run   # the gates; writes nothing
        PYTHONHASHSEED=0 python3 -m ranked.drafts
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from typing import Any, Sequence

from harness.domain import ATTRIBUTES
from harness.provenance import describe, environment

from corrections import protocol as CRP
from manual import instrument as MI
from reuse import structure as st
from rung2.engine2 import Condition, Space

from . import plan
from . import readings as RD

F = Fraction
T2 = RD.T2
EXCEPTION = RD.EXCEPTION
RUNS = RD.RUNS
CLASSES = ("same", "same_queue", "other_queue", "invalid")
WITHIN = (50, 100, 200, 500, 1000)
AT_ONCE = 200                                   # H3: characters
WINDOW_BEFORE, WINDOW_AFTER, TAIL = 100, 500, 800
PROVENANCE = (
    "POST-RUN: asked for by Sergi on 2026-11-20, after ranked/readings.py's six readings. "
    "The expectation in the module's docstring was written and committed before the reading "
    "ran. Not a signed row; no verdict moves.")

frac, share, plain = RD.frac, RD.share, RD.plain


def median_of(xs: Sequence[int]) -> Fraction | None:
    """The middle value, or the mean of the two middle ones; None over nothing."""
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    return F(ys[n // 2]) if n % 2 else F(ys[n // 2 - 1] + ys[n // 2], 2)


def parted_at(a: str, b: str) -> int:
    """Where two reasonings part: the length of their common prefix."""
    return len(os.path.commonprefix([a, b]))


# ---------------------------------------------------------------------------
# Every first call
# ---------------------------------------------------------------------------

def first_calls(record: dict[str, Any], tag: str, corpus: Sequence,
                space: Space) -> list[dict[str, Any]]:
    """Every escalation's first call in a run, with its prompt and its draft."""
    handed = record.get("reports_handed") or {}
    rows = record["records"]
    out = []
    for esc in record["escalations"]:
        idx = esc["idx"]
        calls = esc.get("calls") or []
        call = calls[0] if calls else {}
        payload = call.get("payload")
        ext = RD.region(payload, space)
        action = payload.get("action") if isinstance(payload, dict) else None
        conds = payload.get("conditions") if isinstance(payload, dict) else None
        att = call.get("call_attempts") or []
        out.append({
            "run": tag, "case": idx, "kind": esc["kind"], "verdict": esc["verdict"],
            "rule_id": esc.get("rule_id"), "report": handed.get(str(idx)),
            "key": list(corpus[idx].key()), "truth": rows[idx]["truth"],
            "governing": rows[idx]["truth_rule"], "round": call.get("round"),
            "action": action, "extension": ext,
            "conditions": RD.conditions_of(conds) if ext is not None else None,
            "attributes": RD.attrs(conds) if ext is not None else None,
            "reasoning": call.get("reasoning") or "",
            "attempts": call.get("attempts"), "retries": call.get("retries"),
            "failure": call.get("failure"),
            "prompt_tokens": [x.get("prompt_tokens") for x in att],
            "reasoning_tokens": [x.get("reasoning_tokens") for x in att],
            "providers": [x.get("provider") for x in att],
            "fingerprints": [x.get("system_fingerprint") for x in att]})
    return out


def prompt_of(call: dict[str, Any]) -> tuple:
    """What a first call was sent depends on the ticket and the report alone."""
    return (tuple(call["key"]), call["report"])


def by_prompt(calls: dict[str, list[dict]]) -> dict[tuple, list[dict]]:
    """Every prompt and the first calls sent it, in §2.5's order of the runs and
    the order of the arrivals."""
    out: dict[tuple, list[dict]] = {}
    for t in RUNS:
        for c in sorted(calls.get(t, []), key=lambda c: c["case"]):
            out.setdefault(prompt_of(c), []).append(c)
    return out


# ---------------------------------------------------------------------------
# The gates
# ---------------------------------------------------------------------------

def texts_are_the_protocols(record: dict[str, Any]) -> bool:
    """Gate 1."""
    return bool(record.get("system_prompt") == CRP.SYSTEM_PROMPT
                and record.get("base_text") == CRP.BLIND_BASE
                and record.get("report_template") == CRP.REPORT)


def one_attempt(calls: Sequence[dict]) -> bool:
    """Gate 2."""
    return bool(calls) and all(
        c["round"] == 0 and c["attempts"] == 1 and c["retries"] == [] and c["failure"] is None
        and len(c["prompt_tokens"]) == 1 for c in calls)


def one_count(groups: dict[tuple, list[dict]]) -> bool:
    """Gate 3."""
    return bool(groups) and all(len({tuple(c["prompt_tokens"]) for c in cs}) == 1
                                for cs in groups.values())


def reports_are_the_tickets(calls: Sequence[dict]) -> bool:
    """Gate 4."""
    return bool(calls) and all(
        (c["report"] is not None) == (c["kind"] == plan.ERROR)
        and (c["report"] is None or c["report"] == c["truth"]) for c in calls)


def born_drafts_are_rules(record: dict[str, Any], calls: Sequence[dict], space: Space) -> bool:
    """Gate 5."""
    rules = {d["rule_id"]: d for d in record["rules"]}
    born = [c for c in calls if c["verdict"] == "nacida"]
    ok = len(born) == len(rules)
    for c in born:
        d = rules.get(c["rule_id"])
        ok &= bool(d and d["born_at"] == c["case"] and d["action"] == c["action"]
                   and space.extension([Condition(**x) for x in d["conditions"]])
                   == c["extension"])
    return bool(ok)


# ---------------------------------------------------------------------------
# H-a, H-b: the pairs, and where their reasonings part
# ---------------------------------------------------------------------------

def pair_class(a: dict[str, Any], b: dict[str, Any]) -> str:
    if a["action"] is None or b["action"] is None or a["extension"] is None \
            or b["extension"] is None:
        return "invalid"
    if a["action"] != b["action"]:
        return "other_queue"
    return "same" if a["extension"] == b["extension"] else "same_queue"


def by_attribute(conditions: Sequence[Sequence]) -> dict[str, list[str]]:
    """A draft's conditions on each attribute, comparable."""
    out: dict[str, list[str]] = {}
    for attr, op, value in conditions or []:
        out.setdefault(attr, []).append(json.dumps([op, value], sort_keys=True))
    return {a: sorted(v) for a, v in out.items()}


def side(c: dict[str, Any]) -> dict[str, Any]:
    return {"run": c["run"], "case": c["case"], "kind": c["kind"], "verdict": c["verdict"],
            "action": c["action"], "conditions": c["conditions"],
            "reasoning_chars": len(c["reasoning"])}


def pairs_of(groups: dict[tuple, list[dict]]) -> list[dict[str, Any]]:
    out = []
    for prompt, cs in groups.items():
        for a, b in combinations(cs, 2):
            cls = pair_class(a, b)
            at = parted_at(a["reasoning"], b["reasoning"])
            out.append({
                "report": prompt[1], "governing": a["governing"], "truth": a["truth"],
                "a": side(a), "b": side(b), "class": cls,
                "parted_at": at, "shorter": min(len(a["reasoning"]), len(b["reasoning"])),
                "same_text": bool(a["reasoning"]) and a["reasoning"] == b["reasoning"],
                "attributes_differ": (cls == "same_queue"
                                      and set(a["attributes"]) != set(b["attributes"]))})
    return out


def classes(pairs: Sequence[dict]) -> dict[str, int]:
    c = Counter(p["class"] for p in pairs)
    return {k: c.get(k, 0) for k in CLASSES}


def where_they_part(pairs: Sequence[dict]) -> dict[str, Any]:
    at = [p["parted_at"] for p in pairs]
    return {"pairs": len(pairs), "median": frac(median_of(at)),
            "least": min(at) if at else None, "most": max(at) if at else None,
            "within": {str(w): sum(1 for x in at if x < w) for w in WITHIN},
            "same_text": sum(p["same_text"] for p in pairs),
            "one_inside_the_other": sum(1 for p in pairs if p["parted_at"] == p["shorter"]),
            "median_share_of_the_shorter": frac(median_of(
                [F(p["parted_at"], p["shorter"]) if p["shorter"] else F(0) for p in pairs]))
            if pairs else None}


def drafts_by_size(groups: dict[tuple, list[dict]]) -> dict[str, dict[str, int]]:
    """For prompts sent twice or more: how many drafts their calls drew, by how
    many calls; an invalid draft counts as one draft."""
    out: dict[str, Counter] = {}
    for cs in groups.values():
        if len(cs) < 2:
            continue
        drawn = {(c["action"], c["extension"]) for c in cs}
        out.setdefault(str(len(cs)), Counter())[str(len(drawn))] += 1
    return {k: dict(sorted(v.items(), key=lambda kv: int(kv[0])))
            for k, v in sorted(out.items(), key=lambda kv: int(kv[0]))}


def read_ab(pairs: Sequence[dict], groups: dict[tuple, list[dict]]) -> dict[str, Any]:
    told = [p for p in pairs if p["report"] is not None]
    untold = [p for p in pairs if p["report"] is None]
    return {
        "prompts": len(groups), "sent_twice_or_more": sum(1 for cs in groups.values()
                                                          if len(cs) > 1),
        "pairs": len(pairs),
        "classes": {"all": classes(pairs), "with_a_report": classes(told),
                    "without": classes(untold)},
        "drafts_by_calls": drafts_by_size(groups),
        "parted": {"all": where_they_part(pairs),
                   **{k: where_they_part([p for p in pairs if p["class"] == k])
                      for k in CLASSES},
                   "with_a_report": where_they_part(told), "without": where_they_part(untold)},
    }


# ---------------------------------------------------------------------------
# H-c: two drafts of one queue
# ---------------------------------------------------------------------------

def read_c(pairs: Sequence[dict]) -> dict[str, Any]:
    mine = [p for p in pairs if p["class"] == "same_queue"]
    one_side, other_values = Counter(), Counter()
    for p in mine:
        x, y = by_attribute(p["a"]["conditions"]), by_attribute(p["b"]["conditions"])
        for attr in ATTRIBUTES:
            if (attr in x) != (attr in y):
                one_side[attr] += 1
            elif attr in x and x[attr] != y[attr]:
                other_values[attr] += 1
    return {"pairs": len(mine),
            "other_attributes": sum(p["attributes_differ"] for p in mine),
            "same_attributes_other_values": sum(not p["attributes_differ"] for p in mine),
            "attribute_in_one_draft_only": {a: one_side.get(a, 0) for a in ATTRIBUTES},
            "attribute_in_both_other_conditions": {a: other_values.get(a, 0) for a in ATTRIBUTES},
            "with_a_report": sum(1 for p in mine if p["report"] is not None)}


# ---------------------------------------------------------------------------
# H-d: the exception's tickets, kept for reading
# ---------------------------------------------------------------------------

def window(text: str, at: int) -> str:
    return text[max(0, at - WINDOW_BEFORE): at + WINDOW_AFTER]


def read_d(groups: dict[tuple, list[dict]]) -> list[dict[str, Any]]:
    out = []
    for prompt, cs in groups.items():
        if prompt[1] != T2 or cs[0]["governing"] != EXCEPTION:
            continue
        for a, b in combinations(cs, 2):
            at = parted_at(a["reasoning"], b["reasoning"])
            out.append({"key": list(prompt[0]), "class": pair_class(a, b), "parted_at": at,
                        "a": dict(side(a), window=window(a["reasoning"], at),
                                  tail=a["reasoning"][-TAIL:]),
                        "b": dict(side(b), window=window(b["reasoning"], at),
                                  tail=b["reasoning"][-TAIL:])})
    return out


# ---------------------------------------------------------------------------
# The expectation
# ---------------------------------------------------------------------------

def read_expectation(readings: dict[str, Any]) -> list[dict[str, Any]]:
    ab = readings.get("pairs") or {}
    c = readings.get("one_queue") or {}
    cl = ab.get("classes") or {}
    every, told, untold = cl.get("all") or {}, cl.get("with_a_report") or {}, \
        cl.get("without") or {}
    n = sum(every.values())
    nt, nu = sum(told.values()), sum(untold.values())
    parted = (ab.get("parted") or {}).get("all") or {}
    within = (parted.get("within") or {}).get(str(AT_ONCE))

    def same_queue(d):
        return d.get("same", 0) + d.get("same_queue", 0)

    h1 = bool(n) and 2 * every.get("same", 0) < n
    h2 = bool(nt) and 10 * same_queue(told) > 9 * nt
    h3 = bool(n) and within is not None and 2 * within > n
    h4 = bool(n) and parted.get("same_text") == 0
    m = c.get("pairs") or 0
    h5 = bool(m) and 2 * c["other_attributes"] > m
    h6 = bool(nu) and 2 * same_queue(untold) > nu

    def out(clause, what, holds, reading):
        return {"clause": clause, "what": what, "reading": reading, "holds": bool(holds)}

    return [
        out("H1", "fewer than half of the pairs drew the same queue and extension", h1,
            {"pairs": n, "same": every.get("same")}),
        out("H2", "of the pairs whose prompt carries a report, more than nine in ten drew the "
                  "same queue", h2, {"pairs": nt, "same_queue": same_queue(told)}),
        out("H3", "in more than half of the pairs, the reasonings part within their first 200 "
                  "characters", h3, {"pairs": n, "within_200": within}),
        out("H4", "no pair's reasonings are the same text", h4,
            {"pairs": n, "same_text": parted.get("same_text")}),
        out("H5", "of the same_queue pairs, more than half condition on other attributes", h5,
            {"pairs": m, "other_attributes": c.get("other_attributes")}),
        out("H6", "of the pairs whose prompt carries no report, more than half drew the same "
                  "queue", h6, {"pairs": nu, "same_queue": same_queue(untold)}),
    ]


# ---------------------------------------------------------------------------
# Everything
# ---------------------------------------------------------------------------

def record_path():
    return plan.OUT / "drafts.json"


def read_inputs() -> dict[str, dict]:
    return {RD.tag_of(a, k): json.loads(plan.run_path(a, k).read_text())
            for a, k in plan.schedule() if plan.run_path(a, k).exists()}


def beside(calls: dict[str, list[dict]]) -> dict[str, Any]:
    every = [c for t in RUNS for c in calls.get(t, [])]
    return {"first_calls": len(every),
            "providers": dict(sorted(Counter(str(p) for c in every
                                             for p in c["providers"]).items())),
            "fingerprints": dict(sorted(Counter(str(f) for c in every
                                                for f in c["fingerprints"]).items())),
            "median_reasoning_tokens": frac(median_of(
                [x for c in every for x in c["reasoning_tokens"] if x is not None])),
            "median_reasoning_chars": frac(median_of([len(c["reasoning"]) for c in every]))}


def read_everything(records: dict[str, dict]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    space = MI.space()
    corpus = list(MI.corpus())
    gates: list[dict[str, Any]] = []
    calls = {}
    for t in RUNS:
        if t not in records:
            continue
        rec = records[t]
        calls[t] = first_calls(rec, t, corpus, space)
        gates.append({"gate": 1, "run": t, "what": "the texts are the protocol's",
                      "passes": texts_are_the_protocols(rec)})
        gates.append({"gate": 2, "run": t, "what": "one attempt, no retry",
                      "passes": one_attempt(calls[t])})
        gates.append({"gate": 4, "run": t, "what": "a report is the ticket's own",
                      "passes": reports_are_the_tickets(calls[t])})
        gates.append({"gate": 5, "run": t, "what": "a born draft is its rule",
                      "passes": born_drafts_are_rules(rec, calls[t], space)})
    groups = by_prompt(calls)
    gates.append({"gate": 3, "run": "all", "what": "one prompt, one count of tokens",
                  "passes": one_count(groups)})
    pairs = pairs_of(groups)
    readings = {"pairs": read_ab(pairs, groups), "one_queue": read_c(pairs),
                "exception": read_d(groups), "beside": beside(calls),
                "every_pair": [{k: v for k, v in p.items()} for p in pairs]}
    return readings, gates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Why one prompt drew different drafts "
                                             "(POST-RUN, free).")
    ap.add_argument("--dry-run", action="store_true", help="run the gates; writes nothing")
    args = ap.parse_args(argv)
    gate = plan.refuse_unsigned(f"ranked/drafts.py writes {record_path()}")
    records = read_inputs()
    readings, gates = read_everything(records)
    for g in gates:
        print(f"  gate {g['gate']} run {g['run']}: {'PASS' if g['passes'] else 'FAIL'}"
              f"  {g['what']}")
    complete = len(records) == len(RUNS)
    if not complete:
        print("  missing records")
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
        "source": {"runs": {t: str(plan.run_path(RD.arm_of(t), RD.rep_of(t))) for t in RUNS}},
        "surface": "every first call of the six runs, grouped by the prompt it was sent; a "
                   "draft's extension is read over the whole space of 134,400 points",
        "constants": {"within": list(WITHIN), "at_once": AT_ONCE,
                      "window": [WINDOW_BEFORE, WINDOW_AFTER], "tail": TAIL},
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
