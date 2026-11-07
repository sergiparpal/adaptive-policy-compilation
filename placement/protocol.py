"""
v1c — §5.2 of `PLAN_PLACEMENT.md`: v1b with one change, to the placement round's
list. **On the proposer's path**: nothing here reads a label, a draw or the
policy, and nothing imports the policy in code (rule B of the plan).

THE LIST. At an escalation the draft `D`, of queue `a`, is read on the base as it
stands before the draft is born. `O` is v1b's, `overlap.protocol.split_overlapped`:
every rule of another queue whose extension meets `D`. v1c's list keeps each rule
`R` of `O` for which both hold:

  1. neither extension contains the other strictly. A rule equal to the draft
     stays: containment cannot order two equal extensions, only an edge can;
  2. some point of `R ∩ D` is not governed at listing (§2.2). A point is
     governed at listing when a rule of the base other than `R`, strictly
     inside `D`, matches it, so beats `D` there by containment, the only
     relation a draft has before its answer; and a rule of the base other than
     `D` that beats `R`, by containment or a declared edge, matches it.

**A rule that is defeated still defeats.** The engine reads the edges of every
matched rule, defeated or not, so one third rule beating `R` is not enough: `D`
must be beaten at the point too. That is why both halves are read.

**Why what v1c leaves out decides nothing.** A side against a nested rule is
accepted by `try_edge` as redundant, installing nothing, or refused as against
containment. A point governed at listing stays governed, because no rule and no
edge ever leaves the base, so an edge between `D` and `R` would never change
which rules are undefeated there. `PL-g2` checks both on the hidden policy's path
and the transcriber's runs, over the whole space (`placement.references`).

THE ESCALATION `propose_v1c` is `reasoned_loop.loop.propose_v1b`'s steps, copied,
with the list changed (rule A); `propose_v1b` is not edited. With `nested=False`
and `governed=False` its list is `O`, and it gives back `propose_v1b`'s record but
for the one key it adds to the first call's row, `left_out`, which `PL-g1` holds
it to. A round whose list comes out empty sends no placement call: the draft is
born at once with no declaration, as v1b does when `O` is empty.

THE ASKER is `reasoned_loop.protocol.Asker` with a pin of the caller's choosing
in its request, and nothing else changed: the request is that asker's, called,
with its `provider` replaced. It is built only after the gate, the key check and
the blocking checks have spoken (`placement/run.py`).
"""

from __future__ import annotations

import json
import time
from typing import Any, Callable

from harness.domain import Case

from authorship import loop as eloop
from authorship import protocol as e
from blind.loop import _a_rule, _born, _refused
from reasoned_loop import loop as rl_loop
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine, strictly_below
from rung2.proposers2 import ProposalError

from . import plan

# A listed rule's relation to the draft, by masks.
INSIDE, CONTAINING, EQUAL, CROSSING = "inside", "containing", "equal", "crossing"
# Why v1c leaves a rule of `O` out.
GOVERNED = "governed"
REASONS = (INSIDE, CONTAINING, GOVERNED)
V1C_KEYS = ("left_out",)           # what v1c adds to the first call's row


def relation(ext: int, draft: int) -> str:
    """A rule's extension against the draft's, as `reasoned_loop.unplaced`
    classes them."""
    if ext == draft:
        return EQUAL
    if strictly_below(ext, draft):
        return INSIDE
    if strictly_below(draft, ext):
        return CONTAINING
    return CROSSING


def beaten(engine: PriorityEngine, rid: str) -> int:
    """Where some rule of the base that beats `rid` matches, by containment or
    by a declared edge."""
    out = 0
    for b in engine.beats_me(rid):
        out |= engine.ext[b]
    return out


def listing_of(engine: PriorityEngine, draft: int, action: str, *, nested: bool = True,
               governed: bool = True) -> dict[str, Any]:
    """`O` and `S`, as v1b reads them, the rules of `O` v1c keeps, in base order,
    and each rule it leaves out with its reason. The draft is not in the base."""
    o, s = p.split_overlapped(engine, draft, action)
    inside = [(r.rule_id, engine.ext[r.rule_id]) for r in engine.rules
              if strictly_below(engine.ext[r.rule_id], draft)]
    kept: list[str] = []
    left: dict[str, str] = {}
    for rid in o:
        rel = relation(engine.ext[rid], draft)
        if nested and rel in (INSIDE, CONTAINING):
            left[rid] = rel
            continue
        if governed:
            shared = engine.ext[rid] & draft
            beats_draft = 0
            for other, x in inside:
                if other != rid:
                    beats_draft |= x
            if shared & ~(beats_draft & beaten(engine, rid)) == 0:
                left[rid] = GOVERNED
                continue
        kept.append(rid)
    return {"overlapped": o, "same_queue": s, "kept": kept, "left_out": left}


def propose_v1c(engine: PriorityEngine, case: Case, idx: int, cause: str, proposer,
                channels: list[str], clock=time.monotonic, *, nested: bool = True,
                governed: bool = True) -> dict[str, Any]:
    """One escalation under v1c (§5.2). Returns what the case's record needs, in
    the shape `reasoned_loop.loop.propose_v1b` returns it."""
    esc = eloop.Escalation(idx=idx, kind=cause, verdict=e.FAILED)
    out = {"action": None, "n_prop": 0, "n_acc": 0, "reasons": [],
           "reason": None, "failed": False, "rejected": False, "esc": esc}

    t0 = clock()
    try:
        draft = proposer.first(case, idx=idx)
    except ProposalError as exc:
        rl_loop.call_failed(esc, 0, exc, t0, clock)
        out.update(failed=True, reason=f"proposal_failed: {exc}")
        return out
    esc.calls.append(rl_loop.call_row(0, draft, clock() - t0))
    out["action"] = draft.action
    rule, refused = _a_rule(esc, out, draft, case)
    if refused is not None:
        return refused
    ext = engine.space.extension(rule.conditions)
    copies = e.copies_of(engine, ext)
    if copies:
        esc.copy_of = copies[0]
    got = listing_of(engine, ext, rule.action, nested=nested, governed=governed)
    o, s, kept = got["overlapped"], got["same_queue"], got["kept"]
    esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=list(kept), copies=copies,
                         left_out=got["left_out"])
    if not kept:
        return _born(engine, rule, draft.payload, set(), idx, channels, esc, out)

    esc.listed = p.listing(kept, idx, 0)
    esc.calls[-1].update(listed=list(esc.listed))
    allowed = set(esc.listed)
    t0 = clock()
    try:
        placed = proposer.placement(case, draft, p.placement_message(engine, esc.listed),
                                    idx=idx, listed=list(esc.listed))
    except ProposalError as exc:
        rl_loop.call_failed(esc, 1, exc, t0, clock)
        return _refused(esc, out, e.UNPLACED)    # the placement never came back
    esc.calls.append(rl_loop.call_row(1, placed, clock() - t0))
    out["action"] = placed.action
    second, refused = _a_rule(esc, out, placed, case)
    if refused is not None:
        return refused
    if not p.same_rule(rule, second, engine.space):
        return _refused(esc, out, p.CHANGED)
    missing = e.unplaced(kept, placed.payload, allowed)
    esc.calls[-1].update(overlapped=o, same_queue=s, unplaced=missing)
    if missing:
        return _refused(esc, out, e.UNPLACED)
    return _born(engine, second, placed.payload, allowed, idx, channels, esc, out)


def without_v1c_keys(record: dict[str, Any]) -> dict[str, Any]:
    """A run's record with the key v1c adds to a first call's row taken out, so
    that v1c with both exclusions off can be held to v1b (`PL-g1`)."""
    out = json.loads(json.dumps(record, default=str))
    for esc in out.get("escalations", []):
        for c in esc.get("calls") or []:
            for k in V1C_KEYS:
                c.pop(k, None)
    return out


# ---------------------------------------------------------------------------
# The asker, with a pin
# ---------------------------------------------------------------------------

def request_with(pin: dict, model: str, arm: str, messages: list[dict],
                 attempt: int) -> dict[str, Any]:
    """`reasoned_loop.protocol.Asker`'s request, called, with `pin` in place of
    its provider. A module function, so that `PL-g2` can read the request
    without building a client."""
    holder = type("Holder", (), {"model": model})()
    kwargs = p.Asker.request(holder, arm, messages, attempt)
    kwargs["extra_body"] = {**kwargs["extra_body"], "provider": json.loads(json.dumps(pin))}
    return kwargs


class Asker(p.Asker):
    """`PLAN_REASONED_LOOP.md`'s asker with a pin of the caller's choosing (§1,
    §2.8): this plan's by default, and each provider's own for the bridge. Built
    only after the gate, the key check and the blocking checks have spoken."""

    def __init__(self, pin: dict | None = None, model: str = plan.MODEL,
                 max_retries: int = plan.MAX_RETRIES,
                 sleep: Callable[[float], None] = time.sleep):
        super().__init__(model=model, max_retries=max_retries, sleep=sleep)
        self.pin = json.loads(json.dumps(plan.PROVIDER if pin is None else pin))
        self.name = f"openrouter-placement({model},{self.pin['order'][0]})"

    def request(self, arm: str, messages: list[dict], attempt: int) -> dict[str, Any]:
        return request_with(self.pin, self.model, arm, messages, attempt)
