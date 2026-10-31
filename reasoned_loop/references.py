"""
The references of `PLAN_REASONED_LOOP.md` §5.6 and Stage A, all free. **Never on
the proposer's path.**

THE TRANSCRIBER is a double for the proposer. At every escalation it drafts the
rule of level 3's text that governs the ticket, the first one the ticket
matches, and places it by the text's order: a rule earlier in the list wins. It
runs through this package's own loop, `loop.run_loop`, under either trigger, so
what it shows is what each trigger allows a proposer that never errs (§6.17).
It reads the text, as the model does, and the error trigger reads the labels it
is handed; neither reads the oracle (rule B). The base's rules are the text's
regions, so it recognises a listed rule by its extension.

THE HIDDEN POLICY THROUGH v1b's PATH: the 29 rules of the text drafted in order,
each at the lowest point of the space it covers, and each placed by the text's
order. `RL-g2` requires every rule born, every declaration accepted, the 199
edges of `rung2/hidden_priority.py` installed, and the whole space and corpus
decided right, as `PLAN_BLIND.md`'s `K-g1` required of v2b's path.

STAGE A's OTHER READINGS. The `H29` tickets and the rare queues' tickets, off the
labels; the rules `PLAN_REASONED_RULE.md`'s two rule arms wrote, by the rule that
governs their ticket; and `PLAN_MANUAL.md`'s level-3 runs through this plan's
instrument. They are scored with `manual.instrument`, which reads the truth over
the space where the closed threads read it.
"""

from __future__ import annotations

import collections
import json
from fractions import Fraction
from functools import lru_cache
from typing import Any, Callable

from harness.ceiling_check import all_cases
from harness.domain import Case

from authorship import protocol as e
from blind import rows as brows
from blind.gates import witness
from manual import instrument as MI
from manual import plan as mplan
from manual.score import first_full_cover
from queue_alone import rules as qrules
from reasoned_rule import plan as rrplan
from reasoned_rule import shape
from rung2.engine2 import EDGE_OK, PriorityEngine, validate_conditions

from . import loop, plan
from . import protocol as p

RARE = ("ONCALL_ESCALATION", "SECURITY_INCIDENT", "ACCOUNT_MANAGER", "T3_ENGINEERING")


def text_rules() -> tuple[qrules.Rule, ...]:
    """Level 3's text, as `manual.levels` hands it to the model."""
    return qrules.rules()


@lru_cache(maxsize=None)
def regions() -> dict[str, int]:
    """Each listed rule's region over the space, by identifier."""
    return shape.masks(text_rules())[0]


def payload_of(rule: qrules.Rule) -> dict[str, Any]:
    """A listed rule as an answer would write it, its identifier as the note."""
    return {"action": rule.queue,
            "conditions": [{"attr": a, "op": o, "value": list(v) if isinstance(v, tuple) else v}
                           for a, o, v in rule.conditions],
            "beats": [], "loses_to": [], "note": rule.id}


def governing(case: Case) -> qrules.Rule:
    """The first rule of the text the ticket matches."""
    return qrules.matching(case.as_dict())[0]


class Transcriber:
    """A proposer that drafts the governing rule, or the rule `write` names, and
    places it by the text's order. Only for the references and the gates."""

    name = "transcriber"

    def __init__(self, engine: PriorityEngine,
                 write: Callable[[Case], qrules.Rule] | None = None):
        self.engine = engine
        self.write = write or governing
        self.position = {r.id: k for k, r in enumerate(text_rules())}
        self.by_region: dict[int, str] = {}
        for r in text_rules():
            self.by_region.setdefault(regions()[r.id], r.id)

    def first(self, case: Case, idx: int) -> p.Answer:
        rule = self.write(case)
        return p.Answer(rule.queue, payload_of(rule), None, "stop", 1)

    def placement(self, case: Case, draft, message: str, idx: int,
                  listed: list[str] | None = None) -> p.Answer:
        mine = self.position[draft.payload["note"]]
        beats, loses = [], []
        for rid in listed or []:
            theirs = self.position[self.by_region[self.engine.ext[rid]]]
            (beats if mine < theirs else loses).append(rid)
        placed = dict(draft.payload, beats=beats, loses_to=loses)
        return p.Answer(draft.action, placed, None, "stop", 1)


def written(esc) -> str | None:
    """The listed rule an escalation's first call drafted, by its note."""
    calls = esc.calls if hasattr(esc, "calls") else esc["calls"]
    payload = calls[0].get("payload") if calls else None
    return (payload or {}).get("note")


# ---------------------------------------------------------------------------
# The transcriber under each trigger
# ---------------------------------------------------------------------------

def run_transcriber(arm: str):
    """The transcriber through `loop.run_loop` over the 2,000 cases, and the
    record it leaves, in a paid run's shape."""
    engine = PriorityEngine(space=MI.space())
    res = loop.run_loop(list(MI.corpus()), plan.labels(), engine, Transcriber(engine), arm)
    return res, engine, loop.record_of(res, engine)


def transcriber_figures(arm: str) -> dict[str, Any]:
    res, engine, rec = run_transcriber(arm)
    esc = res.loop.escalations
    reasons = collections.Counter(why for r in res.loop.run.records for why in r.edge_reasons)
    sp = MI.over_space(engine)
    co = MI.over_corpus(engine)
    out = {"escalations": [[x.idx, x.kind, written(x)] for x in esc],
           "causes": {k: sum(1 for x in esc if x.kind == k) for k in plan.CAUSES},
           "rules": [r.note for r in engine.rules],
           "verdicts": dict(collections.Counter(x.verdict for x in esc)),
           "declarations": sum(reasons.values()), "accepted": reasons.get(EDGE_OK, 0),
           "edge_verdicts": dict(reasons),
           "space_right": sp["correct"], "space_points": sp["n"],
           "corpus_right": co["correct"], "corpus_cases": co["n"],
           "k_a": str(MI.k_a_exact(rec["rules"])),
           "material": brows.material(rec["rules"], MI.space(), MI.space_truth(), MI.outside()),
           "cover": res.cover, "stopped_at": res.stopped_at}
    return {"figures": out, "result": res, "engine": engine, "record": rec}


def as_declared(arm: str, got: dict[str, Any]) -> dict[str, bool]:
    """Each figure §0 declares for the transcriber under `arm`, against `got`."""
    d = plan.DECLARED["transcriber"][arm]
    if arm == "i":
        return {"escalations": got["escalations"] == d["escalations"],
                "rules": got["rules"] == d["rules"],
                "space_right": got["space_right"] == d["space_right"],
                "corpus_right": got["corpus_right"] == d["corpus_right"]}
    m = got["material"]
    return {"escalations": len(got["escalations"]) == d["escalations"],
            "impasses": got["causes"][plan.IMPASSE] == d["impasses"],
            "errors": got["causes"][plan.ERROR] == d["errors"],
            "last": got["escalations"][-1][0] == d["last"],
            "rules": len(got["rules"]) == d["rules"],
            "not_written": sorted(set(r.id for r in text_rules()) - set(got["rules"]))
            == d["not_written"],
            "declarations": got["declarations"] == d["declarations"],
            "accepted": got["accepted"] == d["accepted"],
            "space_right": got["space_right"] == d["space_right"],
            "k_a": got["k_a"] == d["k_a"],
            "crossing": m["crossing_pairs"] == d["crossing"],
            "strict": m["strict"] == d["strict"], "units": m["units"] == d["units"]}


# ---------------------------------------------------------------------------
# The hidden policy through v1b's path
# ---------------------------------------------------------------------------

def hidden_through_path() -> dict[str, Any]:
    """The text's 29 rules drafted in order and placed by the text's order,
    each at the lowest point of its region."""
    sp = MI.space()
    cases = list(all_cases())
    engine = PriorityEngine(space=sp)
    current: list[qrules.Rule] = []
    author = Transcriber(engine, write=lambda case: current[-1])
    channels: list[str] = []
    verdicts = collections.Counter()
    born = declarations = 0
    for k, r in enumerate(text_rules()):
        current.append(r)
        ext = regions()[r.id]
        o, _ = p.split_overlapped(engine, ext, r.queue)
        declarations += len(o)
        res = loop.propose_v1b(engine, witness(sp, cases, ext), k, plan.IMPASSE, author,
                               channels)
        born += res["esc"].verdict == e.BORN
        verdicts.update(res["reasons"])
    named = {rule.rule_id: rule.note for rule in engine.rules}
    installed = sorted([named[w], named[l]] for l, ws in engine.decl_below.items() for w in ws)
    return {"born": born, "declarations": declarations, "verdicts": dict(verdicts),
            "installed": installed, "space": MI.over_space(engine),
            "corpus": MI.over_corpus(engine), "engine": engine}


# ---------------------------------------------------------------------------
# Stage A's other readings
# ---------------------------------------------------------------------------

def h29_tickets() -> dict[str, Any]:
    at = [i for i, (_, rule) in enumerate(plan.labels()) if rule == "H29"]
    return {"tickets": len(at), "first": at[:5]}


def rare_tickets() -> dict[str, Any]:
    labels = plan.labels()
    out: dict[str, Any] = {}
    for q in RARE:
        at = [i for i, (y, _) in enumerate(labels) if y == q]
        out[q] = {"tickets": len(at)}
        if q == "ONCALL_ESCALATION":
            out[q]["at"] = at
            out[q]["governed"] = dict(sorted(collections.Counter(
                labels[i][1] for i in at).items()))
    return out


def rules_written() -> dict[str, Any]:
    """The rules `PLAN_REASONED_RULE.md`'s rule arms wrote, read against the rule
    that governs their ticket, over both passes' answers."""
    sp = MI.space()
    corpus = MI.corpus()
    region = regions()
    tab: dict[str, dict[str, collections.Counter]] = collections.defaultdict(
        lambda: collections.defaultdict(collections.Counter))
    whole = {"answers": 0, "of": 0, "under_other_rules": 0}
    for session in ("pass1", "pass2"):
        for row in json.loads(rrplan.ask_path(session).read_text())["rows"]:
            if row["arm"] not in ("w", "t") or not row.get("payload"):
                continue
            gov = governing(corpus[row["ticket"]]).id
            try:
                ext = sp.extension(validate_conditions(row["payload"], None).conditions)
            except Exception:          # noqa: BLE001 — counted, never repaired
                tab[row["arm"]][gov]["invalid"] += 1
                continue
            g = region[gov]
            kind = ("governing" if ext == g else
                    "inside" if ext != g and (ext | g) == g else "other")
            tab[row["arm"]][gov][kind] += 1
            if row["arm"] == "t":
                whole["of"] += 1
                if ext == sp.full:
                    whole["answers"] += 1
                    whole["under_other_rules"] += gov != "H29"
    rows = {gov: [sum(tab["w"][gov].values()), tab["w"][gov]["governing"],
                  tab["w"][gov]["inside"], tab["t"][gov]["governing"]]
            for gov in plan.DECLARED["rules_written"]}
    full = {arm: {gov: dict(c) for gov, c in sorted(by.items())} for arm, by in tab.items()}
    return {"rows": rows, "catch_all_without_reasoning": whole, "by_arm": full}


def manual_level_3() -> list[dict[str, Any]]:
    """`PLAN_MANUAL.md`'s three level-3 runs through this plan's instrument."""
    out = []
    for rep in range(1, mplan.REPS + 1):
        rec = json.loads(mplan.loop_path(3, rep).read_text())
        eng = MI.final_engine(rec)
        sp, co = MI.over_space(eng), MI.over_corpus(eng)
        out.append({"rep": rep, "space": str(Fraction(sp["correct"], sp["n"])),
                    "corpus": str(Fraction(co["correct"], co["n"])),
                    "k_a": str(MI.k_a_exact(rec["rules"])),
                    "cover": first_full_cover(rec),
                    "escalations": rec["metrics"]["escalations"],
                    "prop": rec["metrics"]["proposal_action_accuracy"],
                    "recall_oncall": str(Fraction(
                        sp["recall"]["ONCALL_ESCALATION"]["right"],
                        sp["recall"]["ONCALL_ESCALATION"]["of"]))})
    return out
