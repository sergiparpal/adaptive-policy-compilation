"""
El doble del proponente: un cliente de SDK que devuelve respuestas grabadas.

POR QUE EXISTE. De la ruta del LLM solo estaba probado el parseo, que es la
parte pura. Todo lo demas —construir la peticion, leerla del objeto que devuelve
el SDK, reintentar, validar, meter la regla en la base y calcular las metricas—
solo se ejercitaba pagando una tirada. Es la deuda que `IDEAS.md` dejaba escrita
asi: "un doble del proponente que devolviera respuestas grabadas cubriria el
resto sin gastar".

DONDE SE PINCHA. El doble NO sustituye al proponente: sustituye al CLIENTE del
SDK, un escalon mas abajo. `OpenRouterProposer` y `OpenRouterProposer2` corren
enteros, con su prompt, sus reintentos y su parseo; lo unico que no ocurre es la
peticion HTTP. Sustituir el proponente entero habria dejado sin probar
justamente el codigo que cuesta dinero ejercitar.

Como el SDK `openai` no esta instalado sin venv, `sdk_falso` inyecta un modulo
en `sys.modules` antes de construir el proponente, y lo retira al salir.

DE DONDE SALEN LAS RESPUESTAS. No hay archivo de guion: se derivan del registro
publicado (`results/llm_run.json`, `results2/llm_run2_n100.json`), asi que por
construccion son las de la tirada que produjo esas cifras. El texto crudo nunca
se guardo, de modo que la reconstruccion es exacta en el CONTENIDO y normalizada
en la forma. Turno a turno, del registro del peldano 1:

  577  regla aceptada       accion, condiciones y `note` verbatim del registro;
                            el formato (sangria, ausencia de valla markdown) se
                            normaliza porque no consta.
   32  respuesta vacia      verbatim: el motivo registrado lleva el `repr` de lo
                            que llego —"sin objeto JSON en la respuesta: ''"— y
                            lo que llego era la cadena vacia.
    2  JSON mal cerrado     el texto NO es recuperable. Se sintetiza uno que
                            falla en la misma linea, columna y offset que el
                            registro (ver `_json_roto`). Reconstruye el modo de
                            fallo, no el texto.
   19  payload sin `action` las condiciones no constan; un payload sin `action`
                            reproduce el desenlace registrado, que es lo unico
                            que el registro fija.
    2  regla que no casa    accion verbatim del registro, mas una condicion
                            deliberadamente falsa sobre el caso.

Las cinco reconstrucciones salen de `records[].idx`, `records[].predicted`,
`records[].rejected_reason` y `rules[]`. Ninguna lee `records[].truth`: el doble
no ve el oraculo, igual que no lo veia el modelo.

CUANTAS LLAMADAS CONSUME UN TURNO. Una si el texto parsea; `INTENTOS` si no,
porque el proponente reintenta. El guion lo expande de antemano y comprueba caso
por caso a quien se le esta preguntando, asi que si la ruta se desincroniza
—otra politica de reintento, otro orden de escalacion— la prueba falla senalando
el turno exacto en vez de dar un numero distinto al final.
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

# Nunca es una clave: el proponente lee la de verdad del entorno (regla dura 7)
# y las pruebas comprueban precisamente que la lee de ahi.
CLAVE_FALSA = "sk-doble-de-pruebas-esto-no-es-una-clave"

# max_retries=2 en los dos proponentes -> tres llamadas antes de rendirse.
INTENTOS = 3

MARCA_TICKET = "TICKET EN IMPASSE:"


class Desincronizado(BaseException):
    """El guion no reconoce el caso por el que se le pregunta.

    Hereda de BaseException, no de Exception, A PROPOSITO: los dos proponentes
    envuelven cualquier `Exception` en un reintento y acaban convirtiendola en
    `ProposalError`, que el bucle cuenta y se traga. Un fallo del guion se
    veria entonces como "el modelo contesto mal" y el replay seguiria adelante
    hasta dar una cifra distinta al final, sin decir donde. Asi sale entero.
    """


# Cada peldano tiene su propio parseador y su propio mensaje de error. El guion
# necesita el prefijo exacto para recuperar de el la respuesta que llego.
SIN_JSON = {1: "sin objeto JSON en la respuesta:", 2: "sin objeto JSON:"}


# ---------------------------------------------------------------------------
# Los objetos que devuelven los SDK
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
    """Bloque de contenido de Anthropic. `type` puede no ser 'text': el
    proponente debe quedarse solo con los que lo son."""
    type: str
    text: str = ""


@dataclass
class _RespuestaAnthropic:
    content: list[_Bloque]


# ---------------------------------------------------------------------------
# Los clientes falsos
# ---------------------------------------------------------------------------

class ClienteOpenAIFalso:
    """Compatible con lo que usa el proponente: `.chat.completions.create`."""

    def __init__(self, guion: Callable[[dict], Any]):
        self.construido_con: dict[str, Any] = {}    # base_url y api_key
        self.peticiones: list[dict] = []
        self._guion = guion
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> _Completion:
        self.peticiones.append(kwargs)
        return _Completion(choices=[_Opcion(_Mensaje(self._guion(kwargs)))])


class ClienteAnthropicFalso:
    """Compatible con lo que usa el proponente: `.messages.create`."""

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
    """Lo que el proponente llama como `OpenAI(...)` o `Anthropic(...)`."""
    def crear(**kwargs: Any):
        cliente.construido_con = kwargs
        return cliente
    return crear


@contextmanager
def sdk_falso(openai: ClienteOpenAIFalso | None = None,
              anthropic: ClienteAnthropicFalso | None = None):
    """Inyecta los SDK y una clave falsa mientras dure el bloque.

    Se inyecta el MODULO, no el proponente: `from openai import OpenAI` dentro
    de `__init__` resuelve contra esto. Al salir se restaura lo que hubiera,
    instalado o no, para que la suite corra igual con venv y sin el.
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
# Guiones
# ---------------------------------------------------------------------------

class RespuestasFijas:
    """Devuelve textos en orden, y repite el ultimo si se lo piden de mas."""

    def __init__(self, *textos: Any):
        self.textos = list(textos)
        self.n = 0

    def __call__(self, kwargs: dict) -> Any:
        texto = self.textos[min(self.n, len(self.textos) - 1)]
        self.n += 1
        return texto


def ticket_de(kwargs: dict) -> dict:
    """El caso que viaja en la peticion.

    Se busca en TODOS los mensajes de usuario porque en el reintento el ultimo
    es la instruccion de reparacion, no el ticket.
    """
    for m in kwargs["messages"]:
        if m["role"] == "user" and MARCA_TICKET in m["content"]:
            return json.loads(m["content"].split(MARCA_TICKET, 1)[1])
    raise AssertionError("la peticion no lleva ningun ticket")


@dataclass
class Turno:
    """Una escalacion del registro y lo que el modelo contesto."""
    idx: int
    caso: dict
    texto: Any
    llamadas: int = 1                       # 1, o INTENTOS si el texto no parsea


@dataclass
class Guion:
    """Reproduce los turnos y comprueba por quien se pregunta en cada uno."""
    turnos: list[Turno]
    extraer: Callable[[dict], dict] = ticket_de
    _t: int = 0                             # turno en curso
    _c: int = 0                             # llamadas consumidas del turno
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
# Reconstruccion del guion a partir de un registro publicado
# ---------------------------------------------------------------------------

POSICION = re.compile(r"line (\d+) column (\d+) \(char (\d+)\)")


def _json_roto(lineno: int, colno: int, pos: int) -> str:
    """Un texto que `json.loads` rechaza en EXACTAMENTE esa posicion.

    El texto crudo de las respuestas mal cerradas no se guardo; lo que si consta
    es donde fallaron. Se sintetiza un objeto cuyo ultimo valor va seguido de
    otra cadena sin coma —el error "Expecting ',' delimiter"— cuadrando el
    relleno para que linea, columna y offset coincidan con el registro.
    """
    if lineno < 3 or colno < 11:
        raise NotImplementedError(f"posicion no reconstruible: {lineno}:{colno}")
    inicio = pos - (colno - 1)              # indice donde empieza la linea mala
    lineas = [f'"k{i}": "",' for i in range(1, lineno - 1)]
    sobra = inicio - (2 + sum(len(x) + 1 for x in lineas))
    if sobra < 0:
        raise NotImplementedError(f"cabecera imposible para char {pos}")
    lineas[0] = f'"k1": "{"a" * sobra}",'
    cabecera = "{\n" + "".join(x + "\n" for x in lineas)
    assert len(cabecera) == inicio, "el relleno de la cabecera no cuadra"
    return cabecera + '"note": "' + "b" * (colno - 11) + '""y": 1}'


def _texto_de_fallo(rec: dict, caso: dict, sin_json: str) -> str:
    """Reconstruye la respuesta a partir del motivo registrado.

    Cada rama es un modo de fallo distinto, de los enumerados arriba. Un motivo
    desconocido revienta: mejor eso que un guion que reproduce otra cosa y una
    prueba verde que no significa nada.
    """
    razon: str = rec["rejected_reason"]

    if razon.startswith(f"proposal_failed: {sin_json}"):
        # El motivo lleva el repr de lo que llego (200 primeros caracteres).
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
        # La accion consta; las condiciones no. Una sola condicion falsa sobre
        # el caso basta para reproducir el rechazo.
        otra = 1 if caso["severity"] != 1 else 2
        return json.dumps({
            "action": rec["predicted"],
            "conditions": [{"attr": "severity", "op": "eq", "value": otra}],
            "note": "no casa el caso",
        })

    raise NotImplementedError(f"motivo no reconstruible: {razon!r}")


def _llamadas(texto: Any, parse) -> int:
    """Un turno consume una llamada si el texto parsea, e `INTENTOS` si no."""
    try:
        parse(texto)
    except Exception:                                            # noqa: BLE001
        return INTENTOS
    return 1


def _cuerpo_p1(regla: dict) -> dict:
    return {"action": regla["action"], "conditions": regla["conditions"],
            "note": regla["note"]}


def _cuerpo_p2(regla: dict) -> dict:
    """Como el del peldano 1, mas las aristas de prioridad que se propusieron.

    Las aceptadas estan en `beats`/`loses_to` y las descartadas en
    `dropped_edges`, con la forma `direccion:regla[:motivo]`. El orden RELATIVO
    entre unas y otras no consta; se reconstruye aceptadas primero. Da igual
    mientras no coincidan los dos tipos en una misma regla, que es el caso de
    las ocho tiradas registradas: cero aristas aceptadas.
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
    """Un registro publicado, leido del repo."""
    return json.loads((REPO / nombre).read_text())


def guion_peldano1(reg: dict) -> Guion:
    from harness.proposers import parse_payload

    corpus = generate_corpus(reg["metrics"]["n_cases"], seed=17)
    return Guion(_turnos(reg, corpus, parse_payload, _cuerpo_p1, SIN_JSON[1]))


def guion_peldano2(reg: dict) -> Guion:
    from peldano2.proposers2 import parse_payload

    corpus = generate_corpus(reg["n"], seed=reg["seed"])
    return Guion(_turnos(reg, corpus, parse_payload, _cuerpo_p2, SIN_JSON[2]))
