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

Since the `openai` SDK is not installed without the venv, `sdk_falso` injects a
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
                            record (see `_json_roto`). It reconstructs the
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
CLAVE_FALSA = "sk-doble-de-pruebas-esto-no-es-una-clave"

# max_retries=2 in both proposers -> three calls before giving up.
INTENTOS = 3

MARCA_TICKET = "TICKET EN IMPASSE:"


class Desincronizado(BaseException):
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
SIN_JSON = {1: "sin objeto JSON en la respuesta:", 2: "sin objeto JSON:"}


# ---------------------------------------------------------------------------
# The objects the SDKs return
# ---------------------------------------------------------------------------

@dataclass
class _Mensaje:
    content: str | None


@dataclass
class _Opcion:
    message: _Mensaje


@dataclass
class _Completion:
    choices: list[_Opcion]


@dataclass
class _Bloque:
    """An Anthropic content block. `type` may not be 'text': the proposer must
    keep only those that are."""
    type: str
    text: str = ""


@dataclass
class _RespuestaAnthropic:
    content: list[_Bloque]


# ---------------------------------------------------------------------------
# The fake clients
# ---------------------------------------------------------------------------

class ClienteOpenAIFalso:
    """Compatible with what the proposer uses: `.chat.completions.create`."""

    def __init__(self, guion: Callable[[dict], Any]):
        self.construido_con: dict[str, Any] = {}    # base_url and api_key
        self.peticiones: list[dict] = []
        self._guion = guion
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> _Completion:
        self.peticiones.append(kwargs)
        return _Completion(choices=[_Opcion(_Mensaje(self._guion(kwargs)))])


class ClienteAnthropicFalso:
    """Compatible with what the proposer uses: `.messages.create`."""

    def __init__(self, guion: Callable[[dict], Any]):
        self.construido_con: dict[str, Any] = {}
        self.peticiones: list[dict] = []
        self._guion = guion
        self.messages = types.SimpleNamespace(create=self._create)

    def _create(self, **kwargs: Any) -> _RespuestaAnthropic:
        self.peticiones.append(kwargs)
        salida = self._guion(kwargs)
        bloques = ([_Bloque("text", salida)] if isinstance(salida, str)
                   else list(salida))
        return _RespuestaAnthropic(content=bloques)


def _fabrica(cliente):
    """What the proposer calls as `OpenAI(...)` or `Anthropic(...)`."""
    def crear(**kwargs: Any):
        cliente.construido_con = kwargs
        return cliente
    return crear


@contextmanager
def sdk_falso(openai: ClienteOpenAIFalso | None = None,
              anthropic: ClienteAnthropicFalso | None = None):
    """Injects the SDKs and a fake key for the duration of the block.

    The MODULE is injected, not the proposer: `from openai import OpenAI` inside
    `__init__` resolves against this. On exit whatever was there is restored,
    installed or not, so that the suite runs the same with and without the venv.
    """
    previos = {n: sys.modules.get(n) for n in ("openai", "anthropic")}
    if openai is not None:
        sys.modules["openai"] = types.SimpleNamespace(OpenAI=_fabrica(openai))
    if anthropic is not None:
        sys.modules["anthropic"] = types.SimpleNamespace(
            Anthropic=_fabrica(anthropic))
    entorno = {"OPENROUTER_API_KEY": CLAVE_FALSA, "ANTHROPIC_API_KEY": CLAVE_FALSA}
    try:
        with mock.patch.dict("os.environ", entorno):
            yield
    finally:
        for nombre, modulo in previos.items():
            if modulo is None:
                sys.modules.pop(nombre, None)
            else:
                sys.modules[nombre] = modulo


# ---------------------------------------------------------------------------
# Scripts
# ---------------------------------------------------------------------------

class RespuestasFijas:
    """Returns texts in order, repeating the last if asked for more."""

    def __init__(self, *textos: Any):
        self.textos = list(textos)
        self.n = 0

    def __call__(self, kwargs: dict) -> Any:
        texto = self.textos[min(self.n, len(self.textos) - 1)]
        self.n += 1
        return texto


def ticket_de(kwargs: dict) -> dict:
    """The case travelling in the request.

    It is looked for in ALL user messages because on the retry the last one is
    the repair instruction, not the ticket.
    """
    for m in kwargs["messages"]:
        if m["role"] == "user" and MARCA_TICKET in m["content"]:
            return json.loads(m["content"].split(MARCA_TICKET, 1)[1])
    raise AssertionError("la peticion no lleva ningun ticket")


@dataclass
class Turno:
    """One escalation from the record and what the model answered."""
    idx: int
    caso: dict
    texto: Any
    llamadas: int = 1                       # 1, or INTENTOS if the text fails to parse


@dataclass
class Guion:
    """Replays the turns and checks who is being asked about in each one."""
    turnos: list[Turno]
    extraer: Callable[[dict], dict] = ticket_de
    _t: int = 0                             # current turn
    _c: int = 0                             # calls consumed from the turn
    vistos: list[int] = field(default_factory=list)

    def __call__(self, kwargs: dict) -> Any:
        if self._t >= len(self.turnos):
            raise Desincronizado(
                f"el guion tiene {len(self.turnos)} turnos y se pide uno mas: "
                "la ruta escala mas veces que la tirada registrada")
        turno = self.turnos[self._t]
        pedido = self.extraer(kwargs)
        if pedido != turno.caso:
            raise Desincronizado(
                f"turno {self._t} (caso {turno.idx}): se esperaba {turno.caso} "
                f"y se pregunta por {pedido}")
        self._c += 1
        if self._c == 1:
            self.vistos.append(turno.idx)
        if self._c >= turno.llamadas:
            self._t += 1
            self._c = 0
        return turno.texto

    @property
    def agotado(self) -> bool:
        return self._t == len(self.turnos) and self._c == 0

    @property
    def llamadas_previstas(self) -> int:
        return sum(t.llamadas for t in self.turnos)


# ---------------------------------------------------------------------------
# Reconstruction of the script from a published record
# ---------------------------------------------------------------------------

POSICION = re.compile(r"line (\d+) column (\d+) \(char (\d+)\)")


def _json_roto(lineno: int, colno: int, pos: int) -> str:
    """A text that `json.loads` rejects at EXACTLY that position.

    The raw text of the badly closed responses was not stored; what is recorded
    is where they failed. An object is synthesized whose last value is followed
    by another string with no comma —the "Expecting ',' delimiter" error—
    adjusting the padding so that line, column and offset match the record.
    """
    if lineno < 3 or colno < 11:
        raise NotImplementedError(f"posicion no reconstruible: {lineno}:{colno}")
    inicio = pos - (colno - 1)              # index where the bad line starts
    lineas = [f'"k{i}": "",' for i in range(1, lineno - 1)]
    sobra = inicio - (2 + sum(len(x) + 1 for x in lineas))
    if sobra < 0:
        raise NotImplementedError(f"cabecera imposible para char {pos}")
    lineas[0] = f'"k1": "{"a" * sobra}",'
    cabecera = "{\n" + "".join(x + "\n" for x in lineas)
    assert len(cabecera) == inicio, "el relleno de la cabecera no cuadra"
    return cabecera + '"note": "' + "b" * (colno - 11) + '""y": 1}'


def _texto_de_fallo(rec: dict, caso: dict, sin_json: str) -> str:
    """Reconstructs the response from the recorded reason.

    Each branch is a different failure mode, from those enumerated above. An
    unknown reason blows up: better that than a script reproducing something
    else and a green test that means nothing.
    """
    razon: str = rec["rejected_reason"]

    if razon.startswith(f"proposal_failed: {sin_json}"):
        # The reason carries the repr of what arrived (first 200 characters).
        return ast.literal_eval(razon.split(sin_json, 1)[1].strip())

    if razon.startswith("proposal_failed: JSON invalido"):
        if "Expecting ',' delimiter" not in razon:
            raise NotImplementedError(f"error de JSON no reconstruible: {razon}")
        m = POSICION.search(razon)
        return _json_roto(*(int(g) for g in m.groups()))

    if razon.startswith("accion invalida"):
        valor = ast.literal_eval(razon.split(":", 1)[1].strip())
        cuerpo: dict[str, Any] = {"conditions": [], "note": "sin accion"}
        if valor is not None:
            cuerpo["action"] = valor
        return json.dumps(cuerpo)

    if razon == "la regla no casa el caso que la origino":
        # The action is recorded; the conditions are not. A single condition
        # false about the case is enough to reproduce the rejection.
        otra = 1 if caso["severity"] != 1 else 2
        return json.dumps({
            "action": rec["predicted"],
            "conditions": [{"attr": "severity", "op": "eq", "value": otra}],
            "note": "no casa el caso",
        })

    raise NotImplementedError(f"motivo no reconstruible: {razon!r}")


def _llamadas(texto: Any, parse) -> int:
    """A turn consumes one call if the text parses, and `INTENTOS` if not."""
    try:
        parse(texto)
    except Exception:                                            # noqa: BLE001
        return INTENTOS
    return 1


def _cuerpo_p1(regla: dict) -> dict:
    return {"action": regla["action"], "conditions": regla["conditions"],
            "note": regla["note"]}


def _cuerpo_p2(regla: dict) -> dict:
    """Like rung 1's, plus the priority edges that were proposed.

    The accepted ones are in `beats`/`loses_to` and the discarded ones in
    `dropped_edges`, with the shape `direction:rule[:reason]`. The RELATIVE
    order between them is not recorded; it is reconstructed with the accepted
    ones first. It does not matter as long as both kinds do not coincide on the
    same rule, which is the case in the eight recorded runs: zero accepted
    edges.
    """
    cuerpo = _cuerpo_p1(regla)
    beats, loses = list(regla["beats"]), list(regla["loses_to"])
    for arista in regla["dropped_edges"]:
        direccion, ref = arista.split(":")[:2]
        (beats if direccion == "beats" else loses).append(ref)
    cuerpo["beats"], cuerpo["loses_to"] = beats, loses
    return cuerpo


def _turnos(reg: dict, corpus, parse, cuerpo, sin_json: str) -> list[Turno]:
    reglas = {r["born_at"]: r for r in reg["rules"]}
    turnos = []
    for rec in reg["records"]:
        if not rec["escalated"]:
            continue
        caso = corpus[rec["idx"]].as_dict()
        regla = reglas.get(rec["idx"])
        texto = (json.dumps(cuerpo(regla), ensure_ascii=False, indent=2)
                 if regla is not None else _texto_de_fallo(rec, caso, sin_json))
        turnos.append(Turno(rec["idx"], caso, texto, _llamadas(texto, parse)))
    return turnos


def registro(nombre: str) -> dict:
    """A published record, read from the repo."""
    return json.loads((REPO / nombre).read_text())


def guion_rung1(reg: dict) -> Guion:
    from harness.proposers import parse_payload

    corpus = generate_corpus(reg["metrics"]["n_cases"], seed=17)
    return Guion(_turnos(reg, corpus, parse_payload, _cuerpo_p1, SIN_JSON[1]))


def guion_rung2(reg: dict) -> Guion:
    from rung2.proposers2 import parse_payload

    corpus = generate_corpus(reg["n"], seed=reg["seed"])
    return Guion(_turnos(reg, corpus, parse_payload, _cuerpo_p2, SIN_JSON[2]))
