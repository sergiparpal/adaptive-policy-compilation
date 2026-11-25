"""
The four arms of `PLAN_CAUSE.md`: the loop's first call, with what stands where
the base would be changed. **On the proposer's path.**

THE TEXTS (§2.1 of the plan). Three are recorded texts, imported and not
retyped; one is new:

  e  the empty base, `PLAN_HALVES.md`'s arm `e`, `halves.prompts.EMPTY_BASE`;
  v  v2b's paragraph, `PLAN_HALVES.md`'s arm `v`, `halves.prompts.BLIND_BASE`,
     the first call every v1b and v1c loop sends;
  i  `v`, a blank line, and the impasse notice, `IMPASSE_NOTICE`, which is new;
  r  `v`, a blank line, and the review notice, `REVIEW_NOTICE`:
     `corrections.protocol.REPORT` up to the sentence that names the right
     queue, with a newline in place of the space before it. That newline is the
     one byte not taken from `REPORT`.

Each notice is set after v2b's paragraph as `corrections.protocol.base_text`
sets its report after it: `BLIND_BASE + "\\n" + notice`.

Every arm's system prompt is `PLAN_HALVES.md`'s, which is the loop's,
`reasoned_loop.protocol.SYSTEM_PROMPT`, which is
`manual.prompts.loop_system_prompt(3)`. Every user message is
`rung2.proposers2.user_msg` over the arm's paragraph, as the loop's first call
builds it over v2b's. `CA-g1` holds every claim here to `PLAN_HALVES.md`'s
records and to `corrections/protocol.py`, and `tests/test_cause.py` pins the
four texts byte for byte.

NOTHING HERE TAKES A LABEL (rule B). A builder receives an arm, a ticket's name,
its case and a repetition, never a record's row. Neither notice names a queue, a
rule or a decision. The policy reaches a prompt only as `manual/levels.py`'s
frozen text, through `reasoned_loop.protocol`: this module imports neither the
oracle nor any name that carries the policy in code
(`tests/test_oracle_separation.py`).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from harness.domain import Case

from corrections import protocol as cprotocol
from halves import prompts as hprompts
from rung2.proposers2 import user_msg

EMPTY, V2B, IMPASSE, REVIEW = "e", "v", "i", "r"
ARMS = (EMPTY, V2B, IMPASSE, REVIEW)

SYSTEM_PROMPT = hprompts.SYSTEM_PROMPT
EMPTY_BASE = hprompts.EMPTY_BASE
BLIND_BASE = hprompts.BLIND_BASE

# --- §2.1: the two notices ---------------------------------------------------------------
SEPARATOR = "\n"                   # a blank line, as corrections.protocol.base_text sets its report
REPORT = cprotocol.REPORT
LABEL_SENTENCE = " La cola correcta"
assert REPORT.count(LABEL_SENTENCE) == 1, "the report no longer has one sentence naming the queue"
REVIEW_NOTICE = REPORT.split(LABEL_SENTENCE)[0] + "\n"
IMPASSE_NOTICE = ("AVISO DEL MOTOR: ninguna regla de la base casa este ticket. Por eso no ha "
                  "podido\ndecidirlo.\n")

PARAGRAPHS = {EMPTY: EMPTY_BASE, V2B: BLIND_BASE,
              IMPASSE: BLIND_BASE + SEPARATOR + IMPASSE_NOTICE,
              REVIEW: BLIND_BASE + SEPARATOR + REVIEW_NOTICE}
NOTICES = {IMPASSE: IMPASSE_NOTICE, REVIEW: REVIEW_NOTICE}


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
    """`PLAN_QUEUE_ALONE.md`'s formula, through `halves.prompts`, so that every
    prompt of `e` and `v` carries the digest `PLAN_HALVES.md` recorded for it."""
    return hprompts.digest(system, user)


def ask_id(arm: str, ticket: int, rep: int = 0) -> str:
    """`i:710` in the smoke run and the passes; `i:710#3` in the rarest queue's
    session, its third repetition. `PLAN_HALVES.md`'s form, so that its `e` and
    `v` asks carry the same names."""
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


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def digests() -> dict[str, str]:
    return {k: sha16(v) for k, v in texts().items()}


def fingerprint() -> str:
    body = json.dumps([texts()[k] for k in sorted(texts())], ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()[:16]
