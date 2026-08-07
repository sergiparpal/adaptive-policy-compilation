"""
Que la suite la corra alguien sin que haya que acordarse.

Tener 249 pruebas y depender de que uno se acuerde de lanzarlas es tener menos
pruebas de las que parece. Hay dos redes, y cubren momentos distintos:

  * `.githooks/pre-commit`, antes de cada commit, en local.
  * `.github/workflows/pruebas.yml`, en cada push y cada PR, incluido lo que se
    empujo con `--no-verify`.

Esto vigila que las dos sigan ahi y sigan corriendo lo que dicen correr. Es
poca cosa, pero es exactamente el tipo de fallo que no avisa: un hook sin
permiso de ejecucion o un flujo renombrado no dan error, simplemente dejan de
correr y nadie se entera hasta que hace falta.

Lo que NO se comprueba aqui es que el hook este instalado: `core.hooksPath` es
configuracion local de cada clon y en CI no esta puesto. La instruccion de
instalarlo va en el README y en la cabecera del propio hook.
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")

REPO = Path(__file__).resolve().parent.parent

HOOK = REPO / ".githooks" / "pre-commit"
FLUJO = REPO / ".github" / "workflows" / "pruebas.yml"
DEPENDABOT = REPO / ".github" / "dependabot.yml"

SUITE = "unittest discover"


class TestElHookDePreCommit(unittest.TestCase):

    def test_existe(self):
        self.assertTrue(HOOK.is_file(), f"falta {HOOK.relative_to(REPO)}")

    def test_es_ejecutable(self):
        """Sin el bit de ejecucion git lo ignora en silencio."""
        self.assertTrue(os.access(HOOK, os.X_OK), "el hook no es ejecutable")

    def test_corre_la_suite(self):
        self.assertIn(SUITE, HOOK.read_text())

    def test_dice_como_instalarse(self):
        """El hook se versiona pero no se activa solo: `core.hooksPath` es
        configuracion de cada clon."""
        self.assertIn("core.hooksPath", HOOK.read_text())

    def test_no_necesita_el_venv(self):
        """Si el hook dependiera de `.venv`, un clon recien hecho no podria
        confirmar nada. La suite corre con la biblioteca estandar."""
        self.assertNotIn(".venv", HOOK.read_text())


class TestElFlujoDeCI(unittest.TestCase):

    def setUp(self):
        self.texto = FLUJO.read_text()

    def test_existe(self):
        self.assertTrue(FLUJO.is_file(), f"falta {FLUJO.relative_to(REPO)}")

    def test_corre_la_suite(self):
        self.assertIn(SUITE, self.texto)

    def test_se_dispara_en_push_y_en_pull_request(self):
        for evento in ("push:", "pull_request:"):
            with self.subTest(evento):
                self.assertIn(evento, self.texto)

    def test_cubre_el_minimo_de_python_que_declara_el_README(self):
        """Si alguien sube el suelo en el README, la matriz tiene que seguirle.
        Al reves tambien: una matriz que no incluya el minimo declarado deja la
        afirmacion del README sin comprobar."""
        readme = (REPO / "README.md").read_text()
        minimo = re.search(r"Python (\d+\.\d+)\+", readme)
        self.assertIsNotNone(minimo, "el README ya no declara version minima")
        self.assertIn(f'"{minimo.group(1)}"', self.texto)

    def test_comprueba_que_la_suite_no_escribe_en_los_registros(self):
        """La suite lo afirma en su docstring; el flujo lo verifica despues de
        correrla, que es la unica forma de que la afirmacion no envejezca."""
        self.assertIn("git status --porcelain -- results", self.texto)

    def test_las_acciones_van_clavadas_a_un_sha_completo(self):
        """Una etiqueta la puede repuntar su dueño hacia otro codigo; un commit
        no. Es la convencion del resto de repositorios de esta cuenta, y aqui
        entro tarde: este flujo nacio con `@v4` y estuvo un dia en `@v7`."""
        refs = re.findall(r"^\s*- uses: (\S+)@(\S+)", self.texto, re.M)
        self.assertTrue(refs, "el flujo ya no usa ninguna accion")
        for accion, ref in refs:
            with self.subTest(accion):
                self.assertRegex(ref, SHA,
                                 f"{accion} va por etiqueta, no por commit")

    def test_cada_sha_lleva_su_version_al_lado(self):
        """El SHA solo es legible si dice de que version es. Sin el comentario,
        subir una accion obliga a resolver el hash para saber de donde partes."""
        for linea in self.texto.splitlines():
            if "- uses:" in linea:
                with self.subTest(linea.strip()[:40]):
                    self.assertRegex(linea, r"@[0-9a-f]{40} # v\d+\.\d+\.\d+$")

    def _cuerpo_del_trabajo(self, trabajo: str) -> str:
        """Desde la cabecera del trabajo hasta la del siguiente.

        El corte busca la siguiente clave con DOS espacios de sangria, que es
        la del trabajo que viene. Partir por `\\n  ` a secas no vale: las lineas
        de dentro del trabajo van a cuatro, y empiezan por esos dos.
        """
        resto = self.texto.split(f"\n  {trabajo}:\n", 1)[1]
        siguiente = re.search(r"^  [A-Za-z0-9_-]+:", resto, re.M)
        return resto[: siguiente.start()] if siguiente else resto

    def test_cada_trabajo_tiene_tope_de_tiempo(self):
        """Sin tope, un trabajo colgado corre hasta el limite de la plataforma.
        No es una meta de velocidad; es que un cuelgue falle en vez de arder."""
        trabajos = re.findall(r"^  ([A-Za-z0-9_-]+):$",
                              self.texto.split("\njobs:\n", 1)[1], re.M)
        self.assertTrue(trabajos, "el flujo ya no declara ningun trabajo")
        for trabajo in trabajos:
            with self.subTest(trabajo):
                self.assertIn("timeout-minutes:",
                              self._cuerpo_del_trabajo(trabajo))

    def test_main_no_se_cancela_nunca(self):
        """Aqui los commits van directos a main y el estado del flujo es el
        unico registro de que ese commit paso la suite. Un
        `cancel-in-progress: true` a secas deja en "cancelled" a todo commit
        adelantado por el siguiente: no fallaron, es que nunca respondieron.
        La excepcion es la decision; simplificarla la borraria en silencio."""
        self.assertIn("cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}",
                      self.texto)


class TestDependabot(unittest.TestCase):
    """Lo que impide que el pin por SHA se fosilice.

    Un SHA clavado no envejece ruidosamente: se queda quieto y en silencio. El
    pin y esta vigilancia son una sola decision partida en dos archivos, y
    quitar la mitad de abajo no rompe nada visible.
    """

    def setUp(self):
        self.texto = DEPENDABOT.read_text()

    def test_existe(self):
        self.assertTrue(DEPENDABOT.is_file(),
                        f"falta {DEPENDABOT.relative_to(REPO)}")

    def test_vigila_las_acciones_de_CI(self):
        self.assertIn("package-ecosystem: github-actions", self.texto)

    def test_NO_vigila_pip_a_proposito(self):
        """La ausencia es la decision, no un olvido.

        `openai==2.53.0` y el cierre transitivo del lock no son una dependencia
        desactualizada: son la procedencia del entorno que produjo los
        registros. Un PR semanal proponiendo subirlos entrenaria a fusionarlo
        sin mirar, que es el descuido que el lock existe para impedir.
        """
        self.assertNotIn("package-ecosystem: pip", self.texto)
        self.assertIn("requirements.lock.txt", self.texto,
                      "si se deja pip fuera, el motivo va escrito al lado")


if __name__ == "__main__":
    unittest.main()
