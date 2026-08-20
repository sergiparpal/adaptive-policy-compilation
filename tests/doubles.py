"""
The proposer double: an SDK client that returns recorded responses.

WHY IT EXISTS. Of the LLM path only the parsing was tested, which is the pure
part. Everything else —building the request, reading it from the object the SDK
returns, retrying, validating, inserting the rule into the base and computing
the metrics— was only exercised by paying for a run. It is the debt `IDEAS.md`
put in writing thus: "a proposer double returning recorded responses would cover
the rest without spending".

WHERE IT TAPS IN. The double does NOT replace the proposer: it replaces the SDK
CLIENT, one rung lower. `OpenRouterProposer` and `OpenRouterProposer2` run in
full, with their prompt, their retries and their parsing; the only thing that
does not happen is the HTTP request. Replacing the whole proposer would have
left untested precisely the code that costs money to exercise.

Since the `openai` SDK is not installed without the venv, `fake_sdk` injects a
module into `sys.modules` before building the proposer, and removes it on exit.

WHERE THE RESPONSES COME FROM. There is no script file: they are derived from
the published record (`results/llm_run.json`, `results2/llm_run2_n100.json`), so
by construction they are those of the run that produced those figures. The raw
text was never stored, so the reconstruction is exact in CONTENT and normalized
in form. Turn by turn, from the rung 1 record:

  577  accepted rule        action, conditions and `note` verbatim from the
                            record; the formatting (indentation, absence of a
                            markdown fence) is normalized because it is not
                            recorded.
   32  empty response       verbatim: the recorded reason carries the `repr` of
                            what arrived —"sin objeto JSON en la respuesta: ''"—
                            and what arrived was the empty string.
    2  badly closed JSON    the text is NOT recoverable. One is synthesized that
                            fails at the same line, column and offset as the
                            record (see `_broken_json`). It reconstructs the
                            failure mode, not the text.
   19  payload with no      the conditions are not recorded; a payload without
        `action`            `action` reproduces the recorded outcome, which is
                            all the record pins down.
    2  non-matching rule    action verbatim from the record, plus a condition
                            deliberately false about the case.

The five reconstructions come from `records[].idx`, `records[].predicted`,
`records[].rejected_reason` and `rules[]`. None reads `records[].truth`: the
double does not see the oracle, just as the model did not.

HOW MANY CALLS A TURN CONSUMES. One if the text parses; `INTENTOS` if not,
because the proposer retries. The script expands that in advance and checks case
by case who is being asked about, so if the path goes out of sync —a different
retry policy, a different escalation order— the test fails pointing at the exact
turn instead of giving a different number at the end.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import types
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from unittest import mock

from harness.domain import generate_corpus

REPO = Path(__file__).resolve().parent.parent

# Never a real key: the proposer reads the real one from the environment (hard
# rule 7) and the tests check precisely that it reads it from there.
FAKE_KEY = "sk-doble-de-pruebas-esto-no-es-una-clave"

# max_retries=2 in both proposers -> three calls before giving up.
INTENTOS = 3

TICKET_MARKER = "TICKET EN IMPASSE:"


class OutOfSync(BaseException):
    """The script does not recognize the case it is being asked about.

    It inherits from BaseException, not from Exception, ON PURPOSE: both
    proposers wrap any `Exception` in a retry and end up turning it into
    `ProposalError`, which the loop counts and swallows. A script failure would
    then look like "the model answered badly" and the replay would carry on to a
    different figure at the end, without saying where. This way it comes out
    whole.
    """


# Each rung has its own parser and its own error message. The script needs the
# exact prefix to recover from it the response that arrived.
NO_JSON = {1: "sin objeto JSON en la respuesta:", 2: "sin objeto JSON:"}


# ---------------------------------------------------------------------------
# The objects the SDKs return
# ---------------------------------------------------------------------------

@dataclass
class _Message:
    content: str | None


@dataclass
class _Choice:
    message: _Message


@dataclass
class _Completion:
    choices: list[_Choice]


@dataclass
class _Block:
    """An Anthropic content block. `type` may not be 'text': the proposer must
    keep only those that are."""
    type: str
    text: str = ""


@dataclass
class _AnthropicResponse:
    content: list[_Block]


# ---------------------------------------------------------------------------
# The fake clients
# ---------------------------------------------------------------------------

class FakeOpenAIClient:
    """Compatible with what the proposer uses: `.chat.completions.create`."""

    def __init__(self, script: Callable[[dict], Any]):
        self.built_with: dict[str, Any] = {}    # base_url and api_key
        self.peticiones: list[dict] = []
        self._script = script
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> _Completion:
        self.peticiones.append(kwargs)
        return _Completion(choices=[_Choice(_Message(self._script(kwargs)))])


class FakeAnthropicClient:
    """Compatible with what the proposer uses: `.messages.create`."""

    def __init__(self, script: Callable[[dict], Any]):
        self.built_with: dict[str, Any] = {}
        self.peticiones: list[dict] = []
        self._script = script
        self.messages = types.SimpleNamespace(create=self._create)

    def _create(self, **kwargs: Any) -> _AnthropicResponse:
        self.peticiones.append(kwargs)
        output = self._script(kwargs)
        blocks = ([_Block("text", output)] if isinstance(output, str)
                  else list(output))
        return _AnthropicResponse(content=blocks)


def _fabrica(client):
    """What the proposer calls as `OpenAI(...)` or `Anthropic(...)`."""
    def create(**kwargs: Any):
        client.built_with = kwargs
        return client
    return create


@contextmanager
def fake_sdk(openai: FakeOpenAIClient | None = None,
             anthropic: FakeAnthropicClient | None = None):
    """Injects the SDKs and a fake key for the duration of the block.

    The MODULE is injected, not the proposer: `from openai import OpenAI` inside
    `__init__` resolves against this. On exit whatever was there is restored,
    installed or not, so that the suite runs the same with and without the venv.
    """
    priors = {n: sys.modules.get(n) for n in ("openai", "anthropic")}
    if openai is not None:
        sys.modules["openai"] = types.SimpleNamespace(OpenAI=_fabrica(openai))
    if anthropic is not None:
        sys.modules["anthropic"] = types.SimpleNamespace(
            Anthropic=_fabrica(anthropic))
    env = {"OPENROUTER_API_KEY": FAKE_KEY, "ANTHROPIC_API_KEY": FAKE_KEY}
    try:
        with mock.patch.dict("os.environ", env):
            yield
    finally:
        for name, module in priors.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


# ---------------------------------------------------------------------------
# Scripts
# ---------------------------------------------------------------------------

class FixedResponses:
    """Returns texts in order, repeating the last if asked for more."""

    def __init__(self, *textos: Any):
        self.textos = list(textos)
        self.n = 0

    def __call__(self, kwargs: dict) -> Any:
        text = self.textos[min(self.n, len(self.textos) - 1)]
        self.n += 1
        return text


def ticket_of(kwargs: dict) -> dict:
    """The case travelling in the request.

    It is looked for in ALL user messages because on the retry the last one is
    the repair instruction, not the ticket.
    """
    for m in kwargs["messages"]:
        if m["role"] == "user" and TICKET_MARKER in m["content"]:
            return json.loads(m["content"].split(TICKET_MARKER, 1)[1])
    raise AssertionError("la peticion no lleva ningun ticket")


@dataclass
class Turn:
    """One escalation from the record and what the model answered."""
    idx: int
    case: dict
    text: Any
    calls: int = 1                       # 1, or INTENTOS if the text fails to parse


@dataclass
class Script:
    """Replays the turns and checks who is being asked about in each one."""
    turns: list[Turn]
    extraer: Callable[[dict], dict] = ticket_of
    _t: int = 0                             # current turn
    _c: int = 0                             # calls consumed from the turn
    seen: list[int] = field(default_factory=list)

    def __call__(self, kwargs: dict) -> Any:
        if self._t >= len(self.turns):
            raise OutOfSync(
                f"el guion tiene {len(self.turns)} turnos y se pide uno mas: "
                "la ruta escala mas veces que la tirada registrada")
        turn = self.turns[self._t]
        requested = self.extraer(kwargs)
        if requested != turn.case:
            raise OutOfSync(
                f"turno {self._t} (caso {turn.idx}): se esperaba {turn.case} "
                f"y se pregunta por {requested}")
        self._c += 1
        if self._c == 1:
            self.seen.append(turn.idx)
        if self._c >= turn.calls:
            self._t += 1
            self._c = 0
        return turn.text

    @property
    def agotado(self) -> bool:
        return self._t == len(self.turns) and self._c == 0

    @property
    def calls_expected(self) -> int:
        return sum(t.calls for t in self.turns)


# ---------------------------------------------------------------------------
# Reconstruction of the script from a published record
# ---------------------------------------------------------------------------

POSITION = re.compile(r"line (\d+) column (\d+) \(char (\d+)\)")


def _broken_json(lineno: int, colno: int, pos: int) -> str:
    """A text that `json.loads` rejects at EXACTLY that position.

    The raw text of the badly closed responses was not stored; what is recorded
    is where they failed. An object is synthesized whose last value is followed
    by another string with no comma —the "Expecting ',' delimiter" error—
    adjusting the padding so that line, column and offset match the record.
    """
    if lineno < 3 or colno < 11:
        raise NotImplementedError(f"posicion no reconstruible: {lineno}:{colno}")
    start = pos - (colno - 1)              # index where the bad line starts
    lineas = [f'"k{i}": "",' for i in range(1, lineno - 1)]
    left_over = start - (2 + sum(len(x) + 1 for x in lineas))
    if left_over < 0:
        raise NotImplementedError(f"cabecera imposible para char {pos}")
    lineas[0] = f'"k1": "{"a" * left_over}",'
    header = "{\n" + "".join(x + "\n" for x in lineas)
    assert len(header) == start, "el relleno de la cabecera no cuadra"
    return header + '"note": "' + "b" * (colno - 11) + '""y": 1}'


def _failure_text(rec: dict, case: dict, without_json: str) -> str:
    """Reconstructs the response from the recorded reason.

    Each branch is a different failure mode, from those enumerated above. An
    unknown reason blows up: better that than a script reproducing something
    else and a green test that means nothing.
    """
    reason: str = rec["rejected_reason"]

    if reason.startswith(f"proposal_failed: {without_json}"):
        # The reason carries the repr of what arrived (first 200 characters).
        return ast.literal_eval(reason.split(without_json, 1)[1].strip())

    if reason.startswith("proposal_failed: JSON invalido"):
        if "Expecting ',' delimiter" not in reason:
            raise NotImplementedError(f"error de JSON no reconstruible: {reason}")
        m = POSITION.search(reason)
        return _broken_json(*(int(g) for g in m.groups()))

    if reason.startswith("accion invalida"):
        value = ast.literal_eval(reason.split(":", 1)[1].strip())
        body: dict[str, Any] = {"conditions": [], "note": "sin accion"}
        if value is not None:
            body["action"] = value
        return json.dumps(body)

    if reason == "la regla no casa el caso que la origino":
        # The action is recorded; the conditions are not. A single condition
        # false about the case is enough to reproduce the rejection.
        another = 1 if case["severity"] != 1 else 2
        return json.dumps({
            "action": rec["predicted"],
            "conditions": [{"attr": "severity", "op": "eq", "value": another}],
            "note": "no casa el caso",
        })

    raise NotImplementedError(f"motivo no reconstruible: {reason!r}")


def _calls(text: Any, parse) -> int:
    """A turn consumes one call if the text parses, and `INTENTOS` if not."""
    try:
        parse(text)
    except Exception:                                            # noqa: BLE001
        return INTENTOS
    return 1


def _body_p1(rule: dict) -> dict:
    return {"action": rule["action"], "conditions": rule["conditions"],
            "note": rule["note"]}


def _body_p2(rule: dict) -> dict:
    """Like rung 1's, plus the priority edges that were proposed.

    The accepted ones are in `beats`/`loses_to` and the discarded ones in
    `dropped_edges`, with the shape `direction:rule[:reason]`. The RELATIVE
    order between them is not recorded; it is reconstructed with the accepted
    ones first. It does not matter as long as both kinds do not coincide on the
    same rule, which is the case in the eight recorded runs: zero accepted
    edges.
    """
    body = _body_p1(rule)
    beats, loses = list(rule["beats"]), list(rule["loses_to"])
    for edge in rule["dropped_edges"]:
        direction, ref = edge.split(":")[:2]
        (beats if direction == "beats" else loses).append(ref)
    body["beats"], body["loses_to"] = beats, loses
    return body


def _turns(reg: dict, corpus, parse, body, without_json: str) -> list[Turn]:
    rules = {r["born_at"]: r for r in reg["rules"]}
    turns = []
    for rec in reg["records"]:
        if not rec["escalated"]:
            continue
        case = corpus[rec["idx"]].as_dict()
        rule = rules.get(rec["idx"])
        text = (json.dumps(body(rule), ensure_ascii=False, indent=2)
                if rule is not None else _failure_text(rec, case, without_json))
        turns.append(Turn(rec["idx"], case, text, _calls(text, parse)))
    return turns


def record(name: str) -> dict:
    """A published record, read from the repo."""
    return json.loads((REPO / name).read_text())


def script_rung1(reg: dict) -> Script:
    from harness.proposers import parse_payload

    corpus = generate_corpus(reg["metrics"]["n_cases"], seed=17)
    return Script(_turns(reg, corpus, parse_payload, _body_p1, NO_JSON[1]))


def script_rung2(reg: dict) -> Script:
    from rung2.proposers2 import parse_payload

    corpus = generate_corpus(reg["n"], seed=reg["seed"])
    return Script(_turns(reg, corpus, parse_payload, _body_p2, NO_JSON[2]))
