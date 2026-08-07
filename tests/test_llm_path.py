"""
La ruta del LLM, de extremo a extremo y sin gastar.

Hasta aqui de esta ruta solo estaba probado el parseo. Lo que no lo estaba es
todo lo que hay alrededor: como se arma la peticion, como se lee la respuesta
del SDK, cuando se reintenta, que llega a la base y que sale en las metricas.
Son las cuatro cosas que solo se ejercitaban pagando una tirada, y son
exactamente donde una tirada de 2000 casos se pierde a mitad.

El doble esta descrito en `doubles.py`: sustituye al CLIENTE del SDK, no al
proponente, asi que el proponente corre entero.

DOS NIVELES, Y HACEN COSAS DISTINTAS

  * las clases de PETICION fijan el contrato con la API: prompt, temperatura,
    `response_format`, reintentos, y que la accion verdadera no viaje jamas.
    Se apoyan en respuestas inventadas, porque lo que miden es la peticion.

  * las clases de REPLAY son snapshots: reproducen la tirada registrada entera
    a partir de las respuestas del propio registro y exigen que salga identica
    —reglas, metricas y los registros crudos caso a caso—. Si alguien toca el
    validador, el arbitraje o el calculo de metricas, esto lo caza sin haber
    llamado a nadie.

Vale para las dos rutas: la del peldano 1 (`results/llm_run.json`, 2000 casos,
632 escalaciones) y la del peldano 2 (`results2/llm_run2_n100.json`, 100 casos,
42 escalaciones, con sus aristas de prioridad).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from harness.domain import generate_corpus
from harness.dsl import RuleEngine
from harness.hidden_policy import true_action
from harness.shadow import run_shadow
from peldano2.engine2 import PriorityEngine
from peldano2.shadow2 import run_shadow2
from tests.fixtures import corpus, space
from tests.doubles import (
    CLAVE_FALSA,
    INTENTOS,
    ClienteAnthropicFalso,
    ClienteOpenAIFalso,
    Desincronizado,
    Guion,
    RespuestasFijas,
    Turno,
    guion_peldano1,
    guion_peldano2,
    registro,
    sdk_falso,
)

REPO = Path(__file__).resolve().parent.parent

REGLA = json.dumps({
    "action": "T2_TECHNICAL",
    "conditions": [{"attr": "severity", "op": "lte", "value": 2}],
    "note": "una regla cualquiera, valida y que casa cualquier caso severo",
})


def un_caso(idx: int = 0):
    return generate_corpus(idx + 1, seed=17)[idx]


def proponente1(guion, **kwargs):
    """`OpenRouterProposer` construido contra el cliente falso."""
    cliente = ClienteOpenAIFalso(guion)
    with sdk_falso(openai=cliente):
        from harness.proposers import OpenRouterProposer

        return OpenRouterProposer(**kwargs), cliente


def proponente2(guion, **kwargs):
    cliente = ClienteOpenAIFalso(guion)
    with sdk_falso(openai=cliente):
        from peldano2.proposers2 import OpenRouterProposer2

        return OpenRouterProposer2(**kwargs), cliente


# ---------------------------------------------------------------------------
# El doble
# ---------------------------------------------------------------------------

class TestElDoble(unittest.TestCase):
    """Infraestructura de prueba: si el doble miente, todo lo de abajo miente."""

    def test_el_guion_detecta_que_se_pregunta_por_otro_caso(self):
        """Es la comprobacion que convierte el replay en snapshot: si la ruta
        escala en otro sitio, falla ahi y no en un total distinto al final.

        Y sale ENTERA a traves del proponente, que envuelve toda `Exception` en
        un `ProposalError`: por eso `Desincronizado` no es una de ellas."""
        guion = Guion([Turno(0, un_caso(0).as_dict(), REGLA)])
        prop, _ = proponente1(guion)
        with self.assertRaises(Desincronizado) as ctx:
            prop.propose(un_caso(1), true_action_hint=None)
        self.assertIn("turno 0", str(ctx.exception))

    def test_el_guion_se_queja_si_se_le_piden_turnos_de_mas(self):
        guion = Guion([Turno(0, un_caso(0).as_dict(), REGLA)])
        prop, _ = proponente1(guion)
        prop.propose(un_caso(0), true_action_hint=None)
        self.assertTrue(guion.agotado)
        with self.assertRaises(Desincronizado):
            prop.propose(un_caso(0), true_action_hint=None)

    def test_el_sdk_inyectado_se_retira_al_salir(self):
        """La suite corre con venv y sin el; el doble no puede dejar rastro."""
        import sys

        previo = sys.modules.get("openai")
        with sdk_falso(openai=ClienteOpenAIFalso(RespuestasFijas(REGLA))):
            self.assertIn("openai", sys.modules)
        self.assertIs(sys.modules.get("openai"), previo)


# ---------------------------------------------------------------------------
# La peticion — peldano 1
# ---------------------------------------------------------------------------

class TestPeticionPeldano1(unittest.TestCase):

    def setUp(self):
        self.caso = un_caso(0)

    def test_la_clave_sale_del_entorno_y_apunta_a_openrouter(self):
        """Regla dura 7: la clave vive en el entorno. Aqui se comprueba que el
        proponente la lee de ahi y no de ningun otro sitio."""
        _, cli = proponente1(RespuestasFijas(REGLA))
        self.assertEqual(cli.construido_con["api_key"], CLAVE_FALSA)
        self.assertEqual(cli.construido_con["base_url"],
                         "https://openrouter.ai/api/v1")

    def test_sin_clave_en_el_entorno_no_se_construye(self):
        from unittest import mock

        cliente = ClienteOpenAIFalso(RespuestasFijas(REGLA))
        with sdk_falso(openai=cliente), \
                mock.patch.dict("os.environ", {}, clear=True):
            from harness.proposers import OpenRouterProposer

            with self.assertRaises(KeyError):
                OpenRouterProposer()

    def test_manda_el_prompt_del_sistema_y_el_ticket(self):
        from harness.proposers import SYSTEM_PROMPT

        prop, cli = proponente1(RespuestasFijas(REGLA))
        prop.propose(self.caso, true_action_hint=None)

        sistema, usuario = cli.peticiones[0]["messages"]
        self.assertEqual(sistema, {"role": "system", "content": SYSTEM_PROMPT})
        self.assertEqual(usuario["role"], "user")
        self.assertIn("TICKET EN IMPASSE:", usuario["content"])
        for attr, valor in self.caso.as_dict().items():
            with self.subTest(attr):
                self.assertIn(json.dumps(valor), usuario["content"])

    def test_temperatura_cero_y_modelo_pedido(self):
        prop, cli = proponente1(RespuestasFijas(REGLA),
                                model="openai/gpt-5.6-luna")
        prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(cli.peticiones[0]["temperature"], 0)
        self.assertEqual(cli.peticiones[0]["model"], "openai/gpt-5.6-luna")
        self.assertEqual(prop.name, "openrouter(openai/gpt-5.6-luna)")

    def test_la_accion_verdadera_no_viaja_en_la_peticion(self):
        """El invariante que separa al LLM de los mocks: el mock recibe la
        accion correcta gratis y el LLM no. `run_shadow` le pasa la verdad como
        `true_action_hint` y el proponente tiene que tirarla."""
        prop, cli = proponente1(RespuestasFijas(REGLA))
        verdad = true_action(self.caso)
        prop.propose(self.caso, true_action_hint=verdad)
        usuario = cli.peticiones[0]["messages"][1]["content"]
        self.assertNotIn(verdad, usuario)

    def test_devuelve_la_accion_del_payload(self):
        prop, _ = proponente1(RespuestasFijas(REGLA))
        accion, payload = prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(accion, "T2_TECHNICAL")
        self.assertEqual(payload["action"], "T2_TECHNICAL")

    def test_atraviesa_la_valla_markdown(self):
        """El parseo tolerante ya esta probado suelto; esto comprueba que
        efectivamente se aplica a lo que devuelve el SDK."""
        prop, _ = proponente1(RespuestasFijas(f"Aqui tienes:\n```json\n{REGLA}\n```"))
        accion, _ = prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(accion, "T2_TECHNICAL")

    def test_una_respuesta_vacia_no_revienta_la_tirada(self):
        """`content: None` es lo que devuelve el SDK cuando el modelo no emite
        nada. Tiene que acabar en ProposalError, que el bucle cuenta y sigue."""
        from harness.proposers import ProposalError

        prop, _ = proponente1(RespuestasFijas(None))
        with self.assertRaises(ProposalError):
            prop.propose(self.caso, true_action_hint=None)

    def test_json_object_solo_en_el_primer_intento(self):
        """Algunos modelos no soportan `response_format`; el reintento lo quita
        y confia en el parser tolerante."""
        from harness.proposers import ProposalError

        prop, cli = proponente1(RespuestasFijas("no es json"))
        with self.assertRaises(ProposalError):
            prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(cli.peticiones[0]["response_format"],
                         {"type": "json_object"})
        for p in cli.peticiones[1:]:
            self.assertNotIn("response_format", p)

    def test_el_reintento_lleva_instruccion_de_reparacion(self):
        prop, cli = proponente1(RespuestasFijas("no es json", REGLA))
        accion, _ = prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(accion, "T2_TECHNICAL")
        self.assertEqual(len(cli.peticiones), 2)
        self.assertEqual(len(cli.peticiones[0]["messages"]), 2)
        mensajes = cli.peticiones[1]["messages"]
        self.assertEqual(len(mensajes), 4)
        self.assertIn("UNICAMENTE con el objeto JSON", mensajes[-1]["content"])

    def test_agota_los_reintentos_y_levanta_ProposalError(self):
        from harness.proposers import ProposalError

        prop, cli = proponente1(RespuestasFijas("no es json"))
        with self.assertRaises(ProposalError) as ctx:
            prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(len(cli.peticiones), INTENTOS)
        self.assertIn("sin objeto JSON", str(ctx.exception))

    def test_la_instruccion_de_reparacion_no_se_duplica(self):
        """Tres intentos, un solo par de mensajes de reparacion."""
        from harness.proposers import ProposalError

        prop, cli = proponente1(RespuestasFijas("no es json"))
        with contextlib.suppress(ProposalError):
            prop.propose(self.caso, true_action_hint=None)
        self.assertEqual([len(p["messages"]) for p in cli.peticiones], [2, 4, 4])


# ---------------------------------------------------------------------------
# La peticion — Anthropic
# ---------------------------------------------------------------------------

class TestPeticionAnthropic(unittest.TestCase):
    """El proveedor alternativo. `run_experiment.py llm --provider anthropic`
    lo ofrece, y hasta ahora no lo habia ejercitado nadie."""

    def setUp(self):
        self.caso = un_caso(0)

    def _proponente(self, guion, **kwargs):
        cliente = ClienteAnthropicFalso(guion)
        with sdk_falso(anthropic=cliente):
            from harness.proposers import AnthropicProposer

            return AnthropicProposer(**kwargs), cliente

    def test_la_clave_sale_del_entorno(self):
        _, cli = self._proponente(RespuestasFijas(REGLA))
        self.assertEqual(cli.construido_con["api_key"], CLAVE_FALSA)

    def test_el_prompt_del_sistema_va_con_cache_control(self):
        """Es lo que abarata la tirada: 2000 casos con el mismo prompt."""
        prop, cli = self._proponente(RespuestasFijas(REGLA))
        prop.propose(self.caso, true_action_hint=None)
        sistema = cli.peticiones[0]["system"]
        self.assertEqual(sistema[0]["cache_control"], {"type": "ephemeral"})

    def test_junta_solo_los_bloques_de_texto(self):
        from tests.doubles import _Bloque

        respuesta = [_Bloque("thinking", "esto no es contenido"),
                     _Bloque("text", REGLA)]
        prop, _ = self._proponente(RespuestasFijas(respuesta))
        accion, _ = prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(accion, "T2_TECHNICAL")

    def test_agota_los_reintentos_y_levanta_ProposalError(self):
        from harness.proposers import ProposalError

        prop, cli = self._proponente(RespuestasFijas("no es json"))
        with self.assertRaises(ProposalError):
            prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(len(cli.peticiones), INTENTOS)


# ---------------------------------------------------------------------------
# La peticion — peldano 2
# ---------------------------------------------------------------------------

class TestPeticionPeldano2(unittest.TestCase):

    def setUp(self):
        self.caso = un_caso(0)
        self.engine = PriorityEngine(space=space())

    def _propone(self, prop):
        _, _, base = prop.build_base(self.engine, self.caso, [])
        return prop.propose(self.caso, base)

    def test_manda_el_vecindario_y_el_ticket(self):
        prop, cli = proponente2(RespuestasFijas(REGLA))
        self._propone(prop)
        usuario = cli.peticiones[0]["messages"][1]["content"]
        self.assertIn("BASE DE REGLAS: vacia", usuario)
        self.assertIn("TICKET EN IMPASSE:", usuario)

    def test_cada_version_manda_su_propio_prompt(self):
        from peldano2.proposers2 import SYSTEM_PROMPT_V1, SYSTEM_PROMPT_V2

        for version, esperado in (("v1", SYSTEM_PROMPT_V1),
                                  ("v2", SYSTEM_PROMPT_V2)):
            with self.subTest(version):
                prop, cli = proponente2(RespuestasFijas(REGLA),
                                        prompt_version=version)
                self._propone(prop)
                self.assertEqual(cli.peticiones[0]["messages"][0]["content"],
                                 esperado)
                self.assertIn(version, prop.name)

    def test_una_version_desconocida_no_llega_a_construirse(self):
        with self.assertRaises(ValueError):
            proponente2(RespuestasFijas(REGLA), prompt_version="v3")

    def test_json_object_solo_en_el_primer_intento(self):
        from peldano2.proposers2 import ProposalError

        prop, cli = proponente2(RespuestasFijas("no es json"))
        with self.assertRaises(ProposalError):
            self._propone(prop)
        self.assertEqual(len(cli.peticiones), INTENTOS)
        self.assertIn("response_format", cli.peticiones[0])
        self.assertNotIn("response_format", cli.peticiones[1])

    def test_las_aristas_declaradas_llegan_al_bucle_con_su_veredicto(self):
        """`beats`/`loses_to` es lo unico que el peldano 2 anade al esquema. Si
        el payload las trae, el bucle las tiene que ver y el motor juzgarlas.

        Los dos primeros casos del corpus llegan por `chat` y por `email`, asi
        que una regla por canal cubre uno cada una y son disjuntas: la arista
        que declara la segunda contra la primera se rechaza con `no_solapan`,
        que es el veredicto que se repite en las ocho tiradas registradas.
        """
        def por_canal(canal, **extra):
            return json.dumps({
                "action": "T2_TECHNICAL",
                "conditions": [{"attr": "channel", "op": "eq", "value": canal}],
                "note": f"todo lo que entra por {canal}", **extra})

        guion = RespuestasFijas(por_canal("chat"),
                                por_canal("email", beats=["R0001"]))
        cliente = ClienteOpenAIFalso(guion)
        with sdk_falso(openai=cliente):
            from peldano2.proposers2 import OpenRouterProposer2

            prop = OpenRouterProposer2()
            res = run_shadow2(generate_corpus(2, seed=17),
                              PriorityEngine(space=space()), prop)

        self.assertEqual(res.metrics["edges_proposed"], 1)
        self.assertEqual(res.metrics["edges_accepted"], 0)
        self.assertEqual(res.records[0].edge_reasons, [])
        self.assertEqual(res.records[1].edge_reasons, ["no_solapan"])
        self.assertEqual(res.rules[1].dropped_edges, ["beats:R0001:no_solapan"])


# ---------------------------------------------------------------------------
# Replay: la tirada registrada, entera, sin llamar a nadie
# ---------------------------------------------------------------------------

class TestReplayPeldano1(unittest.TestCase):
    """Snapshot de `results/llm_run.json`: 2000 casos, 632 escalaciones.

    Las respuestas salen del propio registro (ver `doubles.py`), asi que esto
    comprueba la cadena entera —peticion, parseo, validacion, arbitraje,
    metricas— contra la tirada que produjo las cifras publicadas.
    """

    @classmethod
    def setUpClass(cls):
        cls.reg = registro("results/llm_run.json")
        cls.guion = guion_peldano1(cls.reg)
        cliente = ClienteOpenAIFalso(cls.guion)
        with sdk_falso(openai=cliente):
            from harness.proposers import OpenRouterProposer

            prop = OpenRouterProposer(model=cls.reg["model"])
            cls.res = run_shadow(list(corpus()), RuleEngine(), prop)
        cls.cliente = cliente

    def test_reproduce_las_reglas_una_a_una(self):
        self.assertEqual([r.as_dict() for r in self.res.rules], self.reg["rules"])

    def test_reproduce_las_metricas(self):
        self.assertEqual(self.res.metrics, self.reg["metrics"])

    def test_reproduce_los_registros_crudos_caso_a_caso(self):
        self.assertEqual([vars(r) for r in self.res.records], self.reg["records"])

    def test_escala_exactamente_donde_escalo_la_tirada(self):
        registrado = [r["idx"] for r in self.reg["records"] if r["escalated"]]
        self.assertEqual(self.guion.vistos, registrado)
        self.assertEqual(len(registrado), 632)

    def test_632_escalaciones_costaron_700_llamadas(self):
        """El coste no es una llamada por escalacion: los 34 fallos de parseo se
        reintentan hasta tres veces. La diferencia se paga y no aparece en
        ninguna metrica del registro."""
        self.assertTrue(self.guion.agotado)
        self.assertEqual(len(self.cliente.peticiones), 700)
        self.assertEqual(self.res.metrics["llm_calls"], 632)
        self.assertEqual(self.res.metrics["failed_proposals"], 34)

    def test_los_dos_ejes_de_error_siguen_separados(self):
        """Las dos cifras que CLAUDE.md manda no mezclar."""
        self.assertEqual(self.res.metrics["proposal_action_accuracy"], 0.3877)
        self.assertEqual(self.res.metrics["silent_error_rate"], 0.4839)


class TestReplayPeldano2(unittest.TestCase):
    """Snapshot de `results2/llm_run2_n100.json`: 100 casos, 42 escalaciones.

    Anade lo que el peldano 1 no tiene: el vecindario en la peticion y las
    aristas de prioridad de vuelta, con su veredicto.
    """

    @classmethod
    def setUpClass(cls):
        cls.reg = registro("results2/llm_run2_n100.json")
        cls.guion = guion_peldano2(cls.reg)
        cliente = ClienteOpenAIFalso(cls.guion)
        engine = PriorityEngine(space=space())
        with sdk_falso(openai=cliente):
            from peldano2.proposers2 import OpenRouterProposer2

            prop = OpenRouterProposer2(model=cls.reg["model"],
                                       prompt_version="v1")
            cls.res = run_shadow2(
                generate_corpus(cls.reg["n"], seed=cls.reg["seed"]), engine, prop)
        cls.engine = engine
        cls.cliente = cliente

    def test_reproduce_las_reglas_con_sus_aristas(self):
        self.assertEqual([r.as_dict() for r in self.res.rules], self.reg["rules"])

    def test_reproduce_las_metricas(self):
        self.assertEqual(self.res.metrics, self.reg["metrics"])

    def test_reproduce_los_registros_crudos_caso_a_caso(self):
        self.assertEqual([vars(r) for r in self.res.records], self.reg["records"])

    def test_reproduce_el_veredicto_de_cada_arista(self):
        self.assertEqual([list(e) for e in self.engine.edge_log],
                         self.reg["edge_log"])
        self.assertEqual(self.res.metrics["edges_proposed"], 7)
        self.assertEqual(self.res.metrics["edges_accepted"], 0)

    def test_42_escalaciones_costaron_46_llamadas(self):
        self.assertTrue(self.guion.agotado)
        self.assertEqual(len(self.cliente.peticiones), 46)
        self.assertEqual(self.res.metrics["failed_proposals"], 2)


# ---------------------------------------------------------------------------
# El comando entero
# ---------------------------------------------------------------------------

class TestLaTiradaComoLaLanzaElComando(unittest.TestCase):
    """`run_experiment.py llm` de principio a fin, incluido el volcado.

    Es el comando que cuesta dinero, y es el unico trozo de la ruta que ninguna
    otra prueba toca: el arranque, el proveedor, el progreso y el JSON que
    queda. Con `OUT` desviado a un temporal: la suite no escribe en `results*/`
    y esta prueba comprueba tambien eso.
    """

    N = 50

    @classmethod
    def setUpClass(cls):
        import run_experiment
        from unittest import mock

        cls.reg = registro("results/llm_run.json")
        completo = guion_peldano1(cls.reg)
        cls.guion = Guion([t for t in completo.turnos if t.idx < cls.N])
        cls.antes = cls._huella()

        cls.tmp = tempfile.TemporaryDirectory()
        cliente = ClienteOpenAIFalso(cls.guion)
        args = argparse.Namespace(n=cls.N, seed=17, provider="openrouter",
                                  model=cls.reg["model"])
        with sdk_falso(openai=cliente), \
                mock.patch.object(run_experiment, "OUT", Path(cls.tmp.name)), \
                contextlib.redirect_stdout(io.StringIO()) as salida:
            run_experiment.cmd_llm(args)
        cls.salida = salida.getvalue()
        cls.escrito = json.loads(
            (Path(cls.tmp.name) / "llm_run.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @staticmethod
    def _huella() -> str:
        return hashlib.sha256(
            (REPO / "results" / "llm_run.json").read_bytes()).hexdigest()

    def test_no_ha_tocado_el_registro_publicado(self):
        """`results/llm_run.json` es la entrada de los peldanos 3 y 4
        (regla dura 4). Una prueba que lo pisara seria peor que no tenerla."""
        self.assertEqual(self._huella(), self.antes)

    def test_el_json_lleva_procedencia_y_el_modelo(self):
        self.assertEqual(self.escrito["_env"]["seed"], 17)
        self.assertEqual(self.escrito["_env"]["n"], self.N)
        self.assertEqual(self.escrito["_env"]["provider"], "openrouter")
        self.assertEqual(self.escrito["model"], self.reg["model"])

    def test_el_json_no_filtra_la_clave(self):
        crudo = json.dumps(self.escrito)
        self.assertNotIn(CLAVE_FALSA, crudo)
        self.assertNotIn("API_KEY", crudo)

    def test_guarda_las_reglas_con_su_note_y_los_registros_crudos(self):
        self.assertEqual(len(self.escrito["records"]), self.N)
        self.assertTrue(all(r["note"] for r in self.escrito["rules"]))

    def test_el_prefijo_reproduce_el_prefijo_de_la_tirada_registrada(self):
        """El corpus de n=50 es el prefijo del de n=2000, asi que las reglas y
        las decisiones de esos 50 casos tienen que salir clavadas.

        Los contadores de disparos no: en la tirada larga estas mismas reglas
        siguen disparando durante los 1950 casos que aqui no existen. Es la
        diferencia entre la regla y su historial.
        """
        def sin_contadores(reglas):
            return [{k: v for k, v in r.items()
                     if k not in ("fire_count", "correct_count")} for r in reglas]

        esperadas = [r for r in self.reg["rules"] if r["born_at"] < self.N]
        self.assertEqual(sin_contadores(self.escrito["rules"]),
                         sin_contadores(esperadas))
        self.assertEqual(self.escrito["records"],
                         self.reg["records"][: self.N])

    def test_avisa_de_que_sin_el_paso_0_las_cifras_no_valen(self):
        """El aviso del techo va en la salida de la tirada, no en el README."""
        self.assertIn("harness.ceiling_check", self.salida)
        self.assertIn("58.75%", self.salida)


if __name__ == "__main__":
    unittest.main()
