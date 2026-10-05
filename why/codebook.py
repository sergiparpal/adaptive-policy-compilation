"""
The codebook of `PLAN_WHY.md`, frozen on the development set before §0 was
signed. Pure functions: nothing here opens a file.

A `why` is the one sentence the proposer was asked for beside each answer,
*"una frase, como maximo 30 palabras"*. The prompt is Spanish; the answers come
back in Spanish, English and, now and then, Chinese, so every pattern below
carries the Spanish and English forms, and the Chinese ones the development set
showed.

THE CODES, each a set of literal patterns, deliberately so, as
`rung2/note_audit.py`'s are: the count orients and the quotation is the
evidence, which is why the stage quotes as well as counts.

  spec    the sentence argues SPECIFICITY: more specific, more restrictive, more
          concrete, more conditions. It is read as a claim about the rule the
          answer named: in the development set every one of the 172 claims was.
  count   a sub-code of `spec`: the sentence COUNTS conditions explicitly.
  queue   it argues the IMPORTANCE of a queue or of the ticket: security,
          urgency, criticality, escalation, risk.
  prio    it uses a verb of PRECEDENCE: priority, precedence, override,
          prevails. A conclusion more than a reason; reported only.
  match   it argues an EXACT or COMPLETE match.
  order   it argues ORDER or a DEFAULT: first, by default, no defined priority.

THE LABELS, matched case-sensitively, apart from the codes: whether the sentence
names rule `A`, rule `B`, both or neither.

THE CONDITIONS of a rule are read off the question the proposer saw, one
`attr op value` per condition, so every feature below is a property of what was
shown and of nothing else.
"""

from __future__ import annotations

import hashlib
import json
import re

CODES: dict[str, tuple[str, ...]] = {
    "spec": (r"espec[ií]fic", r"\bspecific", r"restrict", r"concret",
             r"m[aá]s condiciones", r"more conditions", r"condiciones adicionales",
             r"additional condition", r"具体", r"条件更多", r"更多条件"),
    "count": (r"\d+\s*condici", r"\b(dos|tres|cuatro|cinco|seis|siete|ocho)\s+condici",
              r"\b(two|three|four|five|six|seven|eight)\s+conditions",
              r"\d+\s*conditions", r"m[aá]s condiciones", r"more conditions",
              r"\d+\s*vs\.?\s*\d+", r"条件更多", r"更多条件", r"[两三四五六]个条件"),
    "queue": (r"segur", r"security", r"安全", r"urgen", r"inmediat", r"immediate",
              r"cr[ií]tic", r"critical", r"escal", r"riesgo", r"\brisk", r"amenaza",
              r"threat", r"紧急", r"升级"),
    "prio": (r"priori", r"precedence", r"overrid", r"prevalec", r"\bprima\b", r"trump",
             r"supera", r"por encima", r"优先", r"higher priority"),
    "match": (r"exactamente", r"\bexactly", r"todas las condiciones",
              r"all (its |the )?conditions", r"directamente", r"\bdirectly",
              r"completamente", r"\bcompletely", r"perfect", r"cumple todo"),
    "order": (r"primer[ao]? en el manual", r"\bfirst\b", r"default", r"por defecto",
              r"\borden\b", r"prioridad definida"),
}
LABEL_A = r"\b(?:[Rr]egla|[Rr]ule|la)\s+A\b|\bA\s+(?:es|is)\b|规则A"
LABEL_B = r"\b(?:[Rr]egla|[Rr]ule|la)\s+B\b|\bB\s+(?:es|is)\b|规则B"

_RX = {k: re.compile("|".join(v), re.IGNORECASE) for k, v in CODES.items()}
_A, _B = re.compile(LABEL_A), re.compile(LABEL_B)
_CJK = re.compile(r"[一-鿿]")
_ES = re.compile(r"[áéíóúñ]|\b(?:el|la|los|las|que|regla|ambas|por|con|del|sobre|es)\b",
                 re.IGNORECASE)
_EN = re.compile(r"\b(?:the|rule|rules|is|and|with|over|both|so|for|of)\b", re.IGNORECASE)
_RULE = re.compile(r"SI (.*) ENTONCES")


def digest() -> str:
    """The codebook's fingerprint, pinned in §8 of the plan: any edit to a
    pattern after the signature shows up here."""
    blob = json.dumps({"codes": CODES, "label_a": LABEL_A, "label_b": LABEL_B},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def code(why: str) -> frozenset[str]:
    return frozenset(k for k, rx in _RX.items() if rx.search(why or ""))


def labels(why: str) -> tuple[bool, bool]:
    """Whether the sentence names rule A, and whether it names rule B."""
    return bool(_A.search(why or "")), bool(_B.search(why or ""))


def language(why: str) -> str:
    if _CJK.search(why):
        return "zh"
    return "es" if len(_ES.findall(why)) >= len(_EN.findall(why)) else "en"


def conditions(question_line: str) -> list[tuple[str, str, str]]:
    """The conditions of one listed rule, as `(attr, op, value)`."""
    m = _RULE.search(question_line)
    if not m:
        raise ValueError(f"not a rule line: {question_line!r}")
    out = []
    for c in m.group(1).split(" AND "):
        attr, op, value = c.strip().split(" ", 2)
        out.append((attr, op, value))
    return out


def listed_rules(question: str) -> tuple[list, list]:
    """The conditions of the rule listed first, `A`, and second, `B`."""
    lines = question.splitlines()
    return conditions(lines[1]), conditions(lines[2])


def categorical_edge(named: list, other: list) -> bool:
    """§0's `Y-c` feature: the named rule carries a categorical or exact
    condition the other lacks. Any one of three: a condition on `product` the
    other does not have; an exact severity where the other has a range; more
    `eq` conditions than the other."""
    def has(cs, attr, ops=None):
        return any(a == attr and (ops is None or op in ops) for a, op, _ in cs)
    eqs = lambda cs: sum(1 for _, op, _ in cs if op == "eq")
    return ((has(named, "product") and not has(other, "product"))
            or (has(named, "severity", ("eq",))
                and has(other, "severity", ("gte", "lte")))
            or eqs(named) > eqs(other))
