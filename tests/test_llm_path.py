"""
The LLM path, end to end and without spending.

Until now only the parsing of this path was tested. What was not is everything
around it: how the request is built, how the SDK response is read, when it
retries, what reaches the base and what comes out in the metrics. Those are the
four things that were only exercised by paying for a run, and they are exactly
where a 2000-case run is lost halfway.

The double is described in `doubles.py`: it replaces the SDK CLIENT, not the
proposer, so the proposer runs in full.

TWO LEVELS, AND THEY DO DIFFERENT THINGS

  * the REQUEST classes pin the contract with the API: prompt, temperature,
    `response_format`, retries, and that the true action never travels. They
    rely on invented responses, because what they measure is the request.

  * the REPLAY classes are snapshots: they reproduce the whole recorded run from
    the record's own responses and require it to come out identical —rules,
    metrics and the raw records case by case. If somebody touches the validator,
    the arbitration or the metric computation, this catches it without having
    called anyone.

It holds for both paths: rung 1's (`results/llm_run.json`, 2000 cases, 632
escalations) and rung 2's (`results2/llm_run2_n100.json`, 100 cases, 42
escalations, with their priority edges).
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
    """`OpenRouterProposer` built against the fake client."""
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
# The double
# ---------------------------------------------------------------------------

class TestElDoble(unittest.TestCase):
    """Test infrastructure: if the double lies, everything below it lies."""

    def test_el_guion_detecta_que_se_pregunta_por_otro_caso(self):
        """This is the check that turns the replay into a snapshot: if the path
        escalates somewhere else, it fails there and not on a different total at
        the end.

        And it comes out WHOLE through the proposer, which wraps every
        `Exception` in a `ProposalError`: that is why `Desincronizado` is not
        one of them."""
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
        """The suite runs with and without the venv; the double must leave no
        trace."""
        import sys

        previo = sys.modules.get("openai")
        with sdk_falso(openai=ClienteOpenAIFalso(RespuestasFijas(REGLA))):
            self.assertIn("openai", sys.modules)
        self.assertIs(sys.modules.get("openai"), previo)


# ---------------------------------------------------------------------------
# The request — rung 1
# ---------------------------------------------------------------------------

class TestPeticionPeldano1(unittest.TestCase):

    def setUp(self):
        self.caso = un_caso(0)

    def test_la_clave_sale_del_entorno_y_apunta_a_openrouter(self):
        """Hard rule 7: the key lives in the environment. Here it is checked that
        the proposer reads it from there and from nowhere else."""
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
        """The invariant that separates the LLM from the mocks: the mock gets
        the correct action for free and the LLM does not. `run_shadow` passes it
        the truth as `true_action_hint` and the proposer has to drop it."""
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
        """The tolerant parsing is already tested on its own; this checks that
        it is actually applied to what the SDK returns."""
        prop, _ = proponente1(RespuestasFijas(f"Aqui tienes:\n```json\n{REGLA}\n```"))
        accion, _ = prop.propose(self.caso, true_action_hint=None)
        self.assertEqual(accion, "T2_TECHNICAL")

    def test_una_respuesta_vacia_no_revienta_la_tirada(self):
        """`content: None` is what the SDK returns when the model emits nothing.
        It has to end in ProposalError, which the loop counts and carries on."""
        from harness.proposers import ProposalError

        prop, _ = proponente1(RespuestasFijas(None))
        with self.assertRaises(ProposalError):
            prop.propose(self.caso, true_action_hint=None)

    def test_json_object_solo_en_el_primer_intento(self):
        """Some models do not support `response_format`; the retry removes it
        and relies on the tolerant parser."""
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
        """Three attempts, a single pair of repair messages."""
        from harness.proposers import ProposalError

        prop, cli = proponente1(RespuestasFijas("no es json"))
        with contextlib.suppress(ProposalError):
            prop.propose(self.caso, true_action_hint=None)
        self.assertEqual([len(p["messages"]) for p in cli.peticiones], [2, 4, 4])


# ---------------------------------------------------------------------------
# The request — Anthropic
# ---------------------------------------------------------------------------

class TestPeticionAnthropic(unittest.TestCase):
    """The alternative provider. `run_experiment.py llm --provider anthropic`
    offers it, and until now nobody had exercised it."""

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
        """It is what makes the run cheap: 2000 cases with the same prompt."""
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
# The request — rung 2
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
        """`beats`/`loses_to` is the only thing rung 2 adds to the schema. If
        the payload carries them, the loop has to see them and the engine has to
        judge them.

        The first two cases of the corpus arrive via `chat` and via `email`, so
        one rule per channel covers one each and they are disjoint: the edge the
        second declares against the first is rejected with `no_solapan`, which is
        the verdict repeated across the eight recorded runs.
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
# Replay: the recorded run, whole, without calling anyone
# ---------------------------------------------------------------------------

class TestReplayPeldano1(unittest.TestCase):
    """Snapshot of `results/llm_run.json`: 2000 cases, 632 escalations.

    The responses come from the record itself (see `doubles.py`), so this checks
    the whole chain —request, parsing, validation, arbitration, metrics—
    against the run that produced the published figures.
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
        """The cost is not one call per escalation: the 34 parse failures are
        retried up to three times. The difference is paid for and appears in no
        metric of the record."""
        self.assertTrue(self.guion.agotado)
        self.assertEqual(len(self.cliente.peticiones), 700)
        self.assertEqual(self.res.metrics["llm_calls"], 632)
        self.assertEqual(self.res.metrics["failed_proposals"], 34)

    def test_los_dos_ejes_de_error_siguen_separados(self):
        """The two figures CLAUDE.md orders not to mix."""
        self.assertEqual(self.res.metrics["proposal_action_accuracy"], 0.3877)
        self.assertEqual(self.res.metrics["silent_error_rate"], 0.4839)


class TestReplayPeldano2(unittest.TestCase):
    """Snapshot of `results2/llm_run2_n100.json`: 100 cases, 42 escalations.

    It adds what rung 1 does not have: the neighbourhood in the request and the
    priority edges coming back, with their verdict.
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
# The whole command
# ---------------------------------------------------------------------------

class TestLaTiradaComoLaLanzaElComando(unittest.TestCase):
    """`run_experiment.py llm` from start to finish, including the dump.

    It is the command that costs money, and it is the only piece of the path no
    other test touches: the startup, the provider, the progress and the JSON
    left behind. With `OUT` redirected to a temporary directory: the suite does
    not write to `results*/` and this test checks that too.
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
                                  model=cls.reg["model"], out=None,
                                  overwrite_record=False)
        with sdk_falso(openai=cliente), \
                mock.patch.object(run_experiment, "OUT", Path(cls.tmp.name)), \
                contextlib.redirect_stdout(io.StringIO()) as salida:
            run_experiment.cmd_llm(args)
        cls.salida = salida.getvalue()
        # The name carries the n since Aug 8, 2026: the smoke test and the full
        # run used to write the same file. See harness/record_guard.py.
        cls.escrito = json.loads(
            (Path(cls.tmp.name) / f"llm_run_n{cls.N}.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @staticmethod
    def _huella() -> str:
        return hashlib.sha256(
            (REPO / "results" / "llm_run.json").read_bytes()).hexdigest()

    def test_no_ha_tocado_el_registro_publicado(self):
        """`results/llm_run.json` is the input of rungs 3 and 4 (hard rule 4).
        A test that trampled it would be worse than not having it."""
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
        """The n=50 corpus is the prefix of the n=2000 one, so the rules and the
        decisions for those 50 cases have to come out identical.

        The firing counters do not: in the long run these same rules keep firing
        during the 1950 cases that do not exist here. It is the difference
        between the rule and its history.
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
        """The ceiling warning goes in the run's output, not in the README."""
        self.assertIn("harness.ceiling_check", self.salida)
        self.assertIn("58.75%", self.salida)


if __name__ == "__main__":
    unittest.main()
