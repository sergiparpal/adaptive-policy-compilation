"""
The four arms of `PLAN_HALVES.md`: the loop's first call, with one paragraph
changed. **On the proposer's path.**

THE TEXTS (§2.1 of the plan). Two are recorded texts, imported and not retyped.
Two are cut or joined from them here, at v2b's semicolon, so that no word in
either is new:

  e  the empty base, `queue_alone.prompts.EMPTY_BASE`, which is v1's empty base
     (`rung2.proposers2.render_base_v1`), as `PLAN_REASONED_RULE.md`'s arm `w`
     sent it;
  v  v2b's paragraph, `reasoned_loop.protocol.BLIND_BASE`, which is
     `blind.protocol.BLIND_BASE`, as every v1b and v1c first call sent it;
  h  `v` up to its semicolon, with a full stop in the semicolon's place;
  o  `e`'s line with its last full stop made a semicolon, and `v`'s clause on
     the next line.

Every arm's system prompt is the loop's, `reasoned_loop.protocol.SYSTEM_PROMPT`,
which is `manual.prompts.loop_system_prompt(3)`. Every user message is
`rung2.proposers2.user_msg` over the arm's paragraph, as the loop's first call
builds it over v2b's. `HV-g1` holds every claim here to the closed records and
to the loop's own code, and `tests/test_halves.py` pins the four texts byte for
byte.

NOTHING HERE TAKES A LABEL (rule B). A builder receives an arm, a ticket's name,
its case and a repetition, never a record's row. The policy reaches a prompt
only as `manual/levels.py`'s frozen text, through `reasoned_loop.protocol`: this
module imports neither the oracle nor any name that carries the policy in code
(`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from harness.domain import Case

from queue_alone import prompts as qprompts
from reasoned_loop import protocol as p
from rung2.proposers2 import user_msg

EMPTY, V2B, HIDDEN, OVERLAP = "e", "v", "h", "o"
ARMS = (EMPTY, V2B, HIDDEN, OVERLAP)

SYSTEM_PROMPT = p.SYSTEM_PROMPT
EMPTY_BASE = qprompts.EMPTY_BASE
BLIND_BASE = p.BLIND_BASE

# --- §2.1: the two halves, cut and joined at v2b's semicolon ---------------------------
SEMICOLON = "; "
assert BLIND_BASE.count(SEMICOLON) == 1, "v2b's paragraph no longer has its one semicolon"
assert EMPTY_BASE.endswith(".\n"), "the empty base no longer ends on a full stop"
HIDDEN_HEAD, OVERLAP_CLAUSE = BLIND_BASE.split(SEMICOLON)
HIDDEN_HALF = HIDDEN_HEAD + ".\n"
OVERLAP_ON_EMPTY = EMPTY_BASE[:-2] + ";\n" + OVERLAP_CLAUSE

PARAGRAPHS = {EMPTY: EMPTY_BASE, V2B: BLIND_BASE, HIDDEN: HIDDEN_HALF,
              OVERLAP: OVERLAP_ON_EMPTY}


def paragraph(arm: str) -> str:
    if arm not in PARAGRAPHS:
        raise ValueError(f"no arm {arm!r}: {ARMS}")
    return PARAGRAPHS[arm]


def system_prompt(arm: str) -> str:
    """Every arm's system prompt is the loop's."""
    paragraph(arm)
    return SYSTEM_PROMPT


def user_message(arm: str, case: Case) -> str:
    """The loop's first user message, over the arm's paragraph."""
    return user_msg(case, paragraph(arm))


def digest(system: str, user: str) -> str:
    """`PLAN_QUEUE_ALONE.md`'s formula, so that every prompt of `e` carries the
    digest `PLAN_REASONED_RULE.md` recorded for its arm `w`."""
    return qprompts.digest(system, user)


def ask_id(arm: str, ticket: int, rep: int = 0) -> str:
    """`h:710` in the smoke run and the passes; `h:710#3` in the rarest queue's
    session, its third repetition."""
    paragraph(arm)
    return f"{arm}:{ticket}" + (f"#{rep}" if rep else "")


@dataclass(frozen=True)
class Ask:
    """One ask of one arm at one ticket, frozen."""
    id: str
    arm: str
    ticket: int
    case: Case
    rep: int = 0

    @property
    def system(self) -> str:
        return system_prompt(self.arm)

    @property
    def user(self) -> str:
        return user_message(self.arm, self.case)

    @property
    def digest(self) -> str:
        return digest(self.system, self.user)

    @property
    def prompt(self) -> str:
        """The prompt it asks: the same for every repetition."""
        return ask_id(self.arm, self.ticket)

    def messages(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": self.system},
                {"role": "user", "content": self.user}]


def ask(arm: str, ticket: int, case: Case, rep: int = 0) -> Ask:
    return Ask(id=ask_id(arm, ticket, rep), arm=arm, ticket=ticket, case=case, rep=rep)


# --- what a record keeps of the texts -----------------------------------------------------

def texts() -> dict[str, str]:
    return {"system_prompt": SYSTEM_PROMPT,
            **{f"paragraph_{arm}": PARAGRAPHS[arm] for arm in ARMS}}


def digests() -> dict[str, str]:
    return {k: hashlib.sha256(v.encode()).hexdigest()[:16] for k, v in texts().items()}


def fingerprint() -> str:
    body = json.dumps([texts()[k] for k in sorted(texts())], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]
