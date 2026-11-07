"""
The references of `PLAN_PLACEMENT.md` §5.6 and Stage A, all free. **Never on the
proposer's path.**

THE DRAFTING READING, §0's figures 1 to 4. Each of the twelve loop records of
`PLAN_REASONED_LOOP.md` and `PLAN_CHANNEL.md`, read-only, is replayed in birth
order: each rule is added at the case it was born at, and its edges tried after it
in `edge_log` order, as `edges/rebuild.py` pairs them. At every placement round the
rebuilt base's `O` must be the recorded one. Each listed rule is then classed
against its draft by masks, through this package's own `protocol.listing_of`, and
the recorded answer is set against the list v1c would have sent. It reads the
proposer's answers those plans paid for, and no answer this plan buys.

THE TRANSCRIBER is `PLAN_REASONED_LOOP.md`'s double for the proposer,
`reasoned_loop.references.Transcriber`, called (rule A). Run through this plan's
loop under each protocol, with each of `PLAN_CHANNEL.md`'s draws, it shows what
each protocol and each draw allow a proposer that never errs (§6.13). It bounds
nothing about the model.

THE HIDDEN POLICY THROUGH A PATH is `reasoned_loop.references.hidden_through_path`
with the escalation handed in: the text's 29 rules drafted in order and placed by
the text's order, each at the lowest point of its region. Through v1b's path it
must give back that function's figures; through v1c's, §0's figure 5.

WHAT v1c LEAVES OUT DECIDES NOTHING (§5.2, `PL-g2`). For every rule a v1c round
left out of a draft that was born, both edges between the two are tried against
the final base without touching it. An edge `try_edge` would refuse, or would
accept as redundant, installs nothing. One it would install changes which rules
are undefeated at a point exactly where both rules match and the loser is not
already beaten there; so an omitted edge decides nothing when the loser is beaten
at every point of the pair's shared region. Undefeated sets that do not move are
decisions that do not move, at every point of the space.

THE BRIDGE'S TICKETS, §0's figure 8: the 27 tickets of the two rarest queues, off
the labels the trigger reads, and 13 drawn by `BRIDGE_SEED` from the other
distinct tickets `PLAN_CHANNEL.md`'s channel runs escalated, a ticket being its
eight attributes.
"""

from __future__ import annotations

import collections
import json
from fractions import Fraction
from functools import lru_cache
from typing import Any, Callable

from harness.ceiling_check import all_cases

from authorship import protocol as e
from blind import rows as brows
from blind.gates import witness
from channel import plan as ch_plan
from edges import rebuild as erb
from fidelity.replay import rule_from
from manual import instrument as MI
from reasoned_loop import plan as rl_plan
from reasoned_loop import protocol as p
from reasoned_loop import references as rl_refs
from rung2.engine2 import PriorityEngine, strictly_below

from . import loop, plan, protocol

ONCALL, SECURITY = "ONCALL_ESCALATION", "SECURITY_INCIDENT"
CLOSED = tuple([("reasoned_loop", a, r) for a in ("i", "e") for r in (1, 2, 3)]
               + [("channel", a, r) for a in ("e", "c") for r in (1, 2, 3)])


def F(x: str | int | Fraction) -> Fraction:
    return Fraction(x)


def median(xs: list[Fraction]) -> Fraction | None:
    """The middle of three, the mean of two (§0)."""
    xs = sorted(xs)
    if not xs:
        return None
    if len(xs) % 2:
        return xs[len(xs) // 2]
    return (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2


# ---------------------------------------------------------------------------
# The closed records, read-only
# ---------------------------------------------------------------------------

def closed_name(thread: str, arm: str, rep: int) -> str:
    return f"{thread}/{arm}_r{rep}"


@lru_cache(maxsize=None)
def _closed_text(thread: str, arm: str, rep: int) -> str:
    owner = rl_plan if thread == "reasoned_loop" else ch_plan
    return owner.run_path(arm, rep).read_text()


def closed_record(thread: str, arm: str, rep: int) -> dict[str, Any]:
    return json.loads(_closed_text(thread, arm, rep))


# ---------------------------------------------------------------------------
# §0's figures 1 to 4: the drafting reading
# ---------------------------------------------------------------------------

def rounds_of(record: dict[str, Any]) -> dict[str, Any]:
    """Figure 1's row for one recorded run, and what figures 2 to 4 read of it."""
    space, corpus, region = MI.space(), MI.corpus(), rl_refs.regions()
    born, by_birth = erb.births(record), erb.edges_by_birth(record)
    engine = PriorityEngine(space=space)
    births, bi = sorted(born), 0
    c: collections.Counter = collections.Counter()
    by_queue: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    rare: dict[str, dict[str, list[int]]] = {q: {"taken": [], "left": []}
                                              for q in (SECURITY, ONCALL)}
    still_missing: dict[int, list[str]] = {}
    replay_ok = True
    for esc in sorted(record["escalations"], key=lambda x: x["idx"]):
        idx = esc["idx"]
        while bi < len(births) and births[bi] < idx:
            b = births[bi]
            engine.add(rule_from(born[b]), born_at=b, keep_id=True)
            for ed in by_birth.get(b, []):
                engine.try_edge(ed.winner, ed.loser)
            bi += 1
        c["escalations"] += 1
        listed = esc.get("listed") or []
        if not listed:
            continue
        c0 = esc["calls"][0]
        draft = brows.ext_of({"conditions": c0["payload"]["conditions"]}, space)
        action = c0["payload"]["action"]
        got = protocol.listing_of(engine, draft, action)
        nested_only = protocol.listing_of(engine, draft, action, governed=False)
        if not set(got["overlapped"]) == set(c0.get("overlapped") or []) == set(listed):
            replay_ok = False
        c["rounds"] += 1
        c["listed"] += len(listed)
        for rid in listed:
            c[protocol.relation(engine.ext[rid], draft)] += 1
        c["wholly_governed"] += sum(1 for v in got["left_out"].values() if v == protocol.GOVERNED)
        c["v1c_list"] += len(got["kept"])
        c["not_sent"] += not got["kept"]
        c["not_sent_nested"] += not nested_only["kept"]
        broad = draft == region[rl_refs.governing(corpus[idx]).id]
        c["rounds_broad"] += broad
        c1 = next((x for x in esc["calls"] if x["round"] == 1), None)
        answered = c1 is not None and c1.get("payload") is not None
        if esc["verdict"] == e.UNPLACED and answered:
            missing = list(c1.get("unplaced") or [])
            still = [rid for rid in missing if rid in got["kept"]]
            complete = not still
            c["unplaced"] += 1
            c["complete"] += complete
            c["complete_nested"] += not any(rid in nested_only["kept"] for rid in missing)
            c["broad_unplaced"] += broad
            c["broad_complete"] += broad and complete
            by_queue[action][0] += 1
            by_queue[action][1] += complete
            if action in rare:
                rare[action]["taken" if complete else "left"].append(idx)
            still_missing[idx] = still
        elif esc["verdict"] == e.UNPLACED:
            c["unplaced_unanswered"] += 1
        if esc["verdict"] == e.BORN:
            c["born_after_round"] += 1
            c["born_broad"] += broad
    return {"row": [c[k] for k in plan.ROUND_KEYS], "counts": dict(c),
            "by_queue": dict(by_queue), "rare": rare, "still_missing": still_missing,
            "replay_ok": replay_ok}


@lru_cache(maxsize=None)
def _drafting_reading() -> str:
    runs = {closed_name(*k): rounds_of(closed_record(*k)) for k in CLOSED}
    total: collections.Counter = collections.Counter()
    by_queue: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for got in runs.values():
        total.update(got["counts"])
        for q, (u, k) in got["by_queue"].items():
            by_queue[q][0] += u
            by_queue[q][1] += k
    channel = [runs[closed_name("channel", "c", r)]["counts"] for r in (1, 2, 3)]
    refused = [Fraction(x["unplaced"], x["escalations"]) for x in channel]
    left = [Fraction(x["unplaced"] - x["complete"], x["escalations"]) for x in channel]
    out = {
        "rounds": {name: got["row"] for name, got in runs.items()},
        "rounds_all": [total[k] for k in plan.ROUND_KEYS],
        "answered": total["unplaced"], "unanswered": total["unplaced_unanswered"],
        "nested_alone": {"complete": total["complete_nested"],
                         "not_sent": total["not_sent_nested"]},
        "pl_a_reading": {"refused": [str(x) for x in refused], "median": str(median(refused)),
                         "left": [str(x) for x in left], "median_left": str(median(left)),
                         "ratio": str(median(left) / median(refused))},
        "by_queue": {q: list(v) for q, v in sorted(by_queue.items())},
        "rare_in_channel": {f"c_r{r}": runs[closed_name("channel", "c", r)]["rare"]
                            for r in (1, 2, 3)},
        "c_r2_1951_left_out": runs[closed_name("channel", "c", 2)]["still_missing"].get(1951),
        "breadth": {"rounds_broad": total["rounds_broad"],
                    "broad_unplaced": total["broad_unplaced"],
                    "rounds_other": total["rounds"] - total["rounds_broad"],
                    "other_unplaced": total["unplaced"] - total["broad_unplaced"],
                    "born_after_round": total["born_after_round"],
                    "born_broad": total["born_broad"],
                    "broad_refusals_taken": total["broad_complete"]},
        "replay_ok": all(got["replay_ok"] for got in runs.values()),
    }
    return json.dumps(out)


def drafting_reading() -> dict[str, Any]:
    """§0's figures 1 to 4, recomputed from the twelve records."""
    return json.loads(_drafting_reading())


def same_fractions(a: list[str], b: list[str]) -> bool:
    return len(a) == len(b) and all(F(x) == F(y) for x, y in zip(a, b))


def drafting_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    """Each of §0's figures 1 to 4 against `got`. The fractions §0 writes are
    compared by value."""
    d = plan.DECLARED
    pa, want = got["pl_a_reading"], d["pl_a_reading"]
    return {
        "replay": got["replay_ok"],
        "rounds": got["rounds"] == d["rounds"],
        "rounds_all": got["rounds_all"] == d["rounds_all"],
        "answered": got["answered"] == d["answered"] and got["unanswered"] == 0,
        "nested_alone": got["nested_alone"] == d["nested_alone"],
        "pl_a_reading": (same_fractions(pa["refused"], want["refused"])
                         and same_fractions(pa["left"], want["left"])
                         and all(F(pa[k]) == F(want[k])
                                 for k in ("median", "median_left", "ratio"))),
        "by_queue": got["by_queue"] == {q: list(v) for q, v in sorted(d["by_queue"].items())},
        "rare_in_channel": got["rare_in_channel"] == d["rare_in_channel"],
        "c_r2_1951_left_out": got["c_r2_1951_left_out"] == d["c_r2_1951_left_out"],
        "breadth": got["breadth"] == d["breadth"],
    }


# ---------------------------------------------------------------------------
# The transcriber through both paths (§0's figure 6)
# ---------------------------------------------------------------------------

def run_transcriber(proto: str, draws, n: int = plan.N):
    """The transcriber through this plan's loop under `proto`, over the first `n`
    cases, and the record it leaves, in a paid run's shape."""
    engine = PriorityEngine(space=MI.space())
    res = loop.run_loop(list(MI.corpus())[:n], plan.labels()[:n], engine,
                        rl_refs.Transcriber(engine), plan.COVERAGE, draws[:n],
                        propose=loop.ESCALATIONS[proto])
    return res, engine, loop.record_of(res, engine)


def round_counts(escalations) -> dict[str, Any]:
    """What a run's placement rounds listed: the rounds with `O`, `O`'s sizes,
    v1c's lists and the rounds not sent, and every rule left out by reason."""
    out = collections.Counter()
    reasons = collections.Counter()
    for esc in escalations:
        calls = esc.calls if hasattr(esc, "calls") else esc["calls"]
        c0 = calls[0] if calls else {}
        o = c0.get("overlapped") or []
        if not o:
            continue
        left = c0.get("left_out") or {}
        out["rounds"] += 1
        out["listed_v1b"] += len(o)
        out["listed_v1c"] += len(o) - len(left)
        out["not_sent"] += len(left) == len(o)
        reasons.update(left.values())
    return {**dict(out), "left_out": dict(reasons)}


def figures(res, engine) -> dict[str, Any]:
    esc = res.loop.escalations
    causes = collections.Counter(x.kind for x in esc)
    sp, co = MI.over_space(engine), MI.over_corpus(engine)
    oncall = sp["recall"][ONCALL]
    return {"escalations": len(esc), "impasses": causes.get(plan.IMPASSE, 0),
            "conflicts": causes.get(plan.CONFLICT, 0), "errors": causes.get(plan.ERROR, 0),
            "calls": res.loop.calls, "rules": [r.note for r in engine.rules],
            "space_right": sp["correct"], "space_points": sp["n"],
            "corpus_right": co["correct"], "corpus_cases": co["n"],
            "recall_oncall": str(Fraction(oncall["right"], oncall["of"])),
            "recall_space": {q: [v["right"], v["of"]] for q, v in sp["recall"].items()},
            "cover": res.cover, "stopped_at": res.stopped_at, **round_counts(esc)}


@lru_cache(maxsize=None)
def transcriber(proto: str, rep: int | None) -> dict[str, Any]:
    """The transcriber under `proto` with run `rep`'s draws, or with the smoke
    run's over the smoke run's cases when `rep` is None."""
    name = plan.stream(proto, rep)
    n = plan.SMOKE_N if rep is None else plan.N
    res, engine, rec = run_transcriber(proto, plan.draws(name), n)
    return {"figures": figures(res, engine), "result": res, "engine": engine,
            "record": rec, "stream": name, "n": n}


def transcribed() -> dict[str, dict[str, Any]]:
    """The transcriber under both protocols and every draw, by run name."""
    return {f"{proto}_{plan.stream(proto, rep)}": transcriber(proto, rep)
            for proto in plan.PROTOCOLS for rep in (1, 2, 3, None)}


def transcriber_as_declared(name: str, got: dict[str, Any]) -> dict[str, bool]:
    proto, stream = name.split("_", 1)
    want = plan.DECLARED["transcriber"][proto][stream]
    return {k: got.get(k) == v for k, v in want.items()}


# ---------------------------------------------------------------------------
# The hidden policy through a path (§0's figure 5)
# ---------------------------------------------------------------------------

def hidden_through(propose: Callable[..., dict[str, Any]]) -> dict[str, Any]:
    """`reasoned_loop.references.hidden_through_path`, with the escalation handed
    in, and what its rounds listed and left out."""
    sp = MI.space()
    cases = list(all_cases())
    engine = PriorityEngine(space=sp)
    current: list = []
    author = rl_refs.Transcriber(engine, write=lambda case: current[-1])
    channels: list[str] = []
    verdicts = collections.Counter()
    born = declarations = 0
    escalations, pairs = [], []
    for k, r in enumerate(rl_refs.text_rules()):
        current.append(r)
        ext = rl_refs.regions()[r.id]
        o, _ = p.split_overlapped(engine, ext, r.queue)
        declarations += len(o)
        res = propose(engine, witness(sp, cases, ext), k, plan.IMPASSE, author, channels)
        esc = res["esc"]
        escalations.append(esc)
        born += esc.verdict == e.BORN
        verdicts.update(res["reasons"])
        if esc.verdict == e.BORN:
            left = (esc.calls[0].get("left_out") or {}) if esc.calls else {}
            pairs += [(esc.rule_id, rid, why) for rid, why in left.items()]
    named = {rule.rule_id: rule.note for rule in engine.rules}
    installed = sorted([named[w], named[l]] for l, ws in engine.decl_below.items() for w in ws)
    return {"born": born, "declarations": declarations, "verdicts": dict(verdicts),
            "installed": installed, "space": MI.over_space(engine),
            "corpus": MI.over_corpus(engine), "engine": engine,
            "rounds": round_counts(escalations), "pairs": pairs}


@lru_cache(maxsize=None)
def hidden(proto: str) -> dict[str, Any]:
    return hidden_through(loop.ESCALATIONS[proto])


def hidden_v1c_figures(got: dict[str, Any]) -> dict[str, Any]:
    """§0's figure 5's numbers, off the hidden policy through v1c's path."""
    rc, left = got["rounds"], got["rounds"]["left_out"]
    sp, co = got["space"], got["corpus"]
    return {"born": got["born"], "rounds": rc["rounds"], "listed_v1b": rc["listed_v1b"],
            "listed_v1c": rc["listed_v1c"],
            "inside_or_containing": left.get(protocol.INSIDE, 0) + left.get(protocol.CONTAINING, 0),
            "governed": left.get(protocol.GOVERNED, 0), "not_sent": rc["not_sent"],
            "installed": len(got["installed"]), "space": [sp["correct"], sp["n"]],
            "corpus": [co["correct"], co["n"]]}


def v1b_path_is_reasoned_loops() -> dict[str, Any]:
    """Through v1b's path, this module's copy gives back
    `reasoned_loop.references.hidden_through_path`'s figures."""
    ours, theirs = hidden("v1b"), rl_refs.hidden_through_path()
    keys = ("born", "declarations", "verdicts", "installed")
    same = {k: ours[k] == theirs[k] for k in keys}
    same["space"] = ours["space"]["correct"] == theirs["space"]["correct"]
    same["corpus"] = ours["corpus"]["correct"] == theirs["corpus"]["correct"]
    return {"same": same, "passes": all(same.values())}


# ---------------------------------------------------------------------------
# What v1c leaves out decides nothing (§5.2, PL-g2)
# ---------------------------------------------------------------------------

def would_change(engine: PriorityEngine, w: str, l: str) -> bool:
    """Whether installing `w` over `l` on `engine`, where `try_edge` would take
    it, would change which rules are undefeated at some point. It reads the
    engine and does not touch it."""
    if w == l or w not in engine.ext or l not in engine.ext:
        return False
    ew, el = engine.ext[w], engine.ext[l]
    if not ew & el:
        return False                     # disjoint: refused
    if strictly_below(el, ew):
        return False                     # against containment: refused
    if strictly_below(ew, el):
        return False                     # redundant with containment: installs nothing
    if engine._reaches(l, w):
        return False                     # it would close a cycle: refused
    return bool(ew & el & ~protocol.beaten(engine, l))


def left_out_pairs() -> list[tuple[str, PriorityEngine, str, str, str]]:
    """Every (source, final engine, draft, rule left out, reason) of the hidden
    policy's v1c path and of the transcriber's v1c runs, for drafts born."""
    out = []
    h = hidden("v1c")
    out += [("hidden", h["engine"], d, r, why) for d, r, why in h["pairs"]]
    for rep in (1, 2, 3, None):
        t = transcriber("v1c", rep)
        for esc in t["result"].loop.escalations:
            if esc.verdict != e.BORN or not esc.calls:
                continue
            for rid, why in (esc.calls[0].get("left_out") or {}).items():
                out.append((f"v1c_{t['stream']}", t["engine"], esc.rule_id, rid, why))
    return out


def left_out_decides_nothing() -> dict[str, Any]:
    pairs = left_out_pairs()
    changing, misclassed = [], []
    by = collections.Counter()
    for source, engine, d, r, why in pairs:
        by[(source, why)] += 1
        rel = protocol.relation(engine.ext[r], engine.ext[d])
        if (why in (protocol.INSIDE, protocol.CONTAINING) and rel != why) or (
                why == protocol.GOVERNED and rel not in (protocol.EQUAL, protocol.CROSSING)):
            misclassed.append([source, d, r, why, rel])
        for w, l in ((d, r), (r, d)):
            if would_change(engine, w, l):
                changing.append([source, w, l, why])
    return {"pairs": len(pairs),
            "by_source_and_reason": {f"{s} {w}": n for (s, w), n in sorted(by.items())},
            "changing": changing[:20], "misclassed": misclassed[:20],
            "passes": bool(pairs) and not changing and not misclassed}


# ---------------------------------------------------------------------------
# The bridge's tickets (§0's figure 8)
# ---------------------------------------------------------------------------

def ticket_key(case) -> tuple:
    return tuple(sorted(case.as_dict().items()))


def bridge_reading() -> dict[str, Any]:
    labels, corpus = plan.labels(), MI.corpus()
    rare = {q: [i for i, (y, _) in enumerate(labels) if y == q] for q in plan.BRIDGE_RARE}
    rare_all = sorted(i for q in plan.BRIDGE_RARE for i in rare[q])
    escalated: set[int] = set()
    for rep in (1, 2, 3):
        escalated |= {esc["idx"] for esc in closed_record("channel", "c", rep)["escalations"]}
    seen = {ticket_key(corpus[i]) for i in rare_all}
    candidates = []
    for i in sorted(escalated):
        if i in rare_all or ticket_key(corpus[i]) in seen:
            continue
        seen.add(ticket_key(corpus[i]))
        candidates.append(i)
    drawn = plan.bridge_draw(candidates)
    first = collections.Counter(plan.bridge_first(i) for i in sorted(rare_all + drawn))
    return {SECURITY: rare[SECURITY], ONCALL: rare[ONCALL],
            "rare_escalated": sum(1 for i in rare_all if i in escalated),
            "candidates": len(candidates), "drawn": drawn,
            "first": dict(sorted(first.items())),
            "distinct": len({ticket_key(corpus[i]) for i in rare_all + drawn}) == len(rare_all + drawn)}


def bridge_as_declared(got: dict[str, Any]) -> dict[str, bool]:
    want = plan.DECLARED["bridge"]
    out = {k: got[k] == v for k, v in want.items()}
    out["distinct"] = got["distinct"]
    out["tickets"] = sorted(got[SECURITY] + got[ONCALL] + got["drawn"]) == plan.bridge_tickets()
    out["forty"] = len(plan.bridge_tickets()) == plan.BRIDGE_TICKETS
    return out
