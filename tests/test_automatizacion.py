"""
That something runs the suite without anyone having to remember.

Having 249 tests and depending on someone remembering to launch them is having
fewer tests than it looks. There are two nets, covering different moments:

  * `.githooks/pre-commit`, before every commit, locally.
  * `.github/workflows/pruebas.yml`, on every push and every PR, including what
    was pushed with `--no-verify`.

This watches that both are still there and still run what they say they run. It
is a small thing, but it is exactly the kind of failure that gives no warning: a
hook without the execute bit or a renamed workflow raise no error, they simply
stop running and nobody notices until it matters.

What is NOT checked here is that the hook is installed: `core.hooksPath` is
local configuration per clone and is not set in CI. The instruction to install
it is in the README and in the header of the hook itself.
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
        """Without the execute bit git ignores it silently."""
        self.assertTrue(os.access(HOOK, os.X_OK), "el hook no es ejecutable")

    def test_corre_la_suite(self):
        self.assertIn(SUITE, HOOK.read_text())

    def test_dice_como_instalarse(self):
        """The hook is versioned but does not enable itself: `core.hooksPath`
        is per-clone configuration."""
        self.assertIn("core.hooksPath", HOOK.read_text())

    def test_no_necesita_el_venv(self):
        """If the hook depended on `.venv`, a fresh clone could not commit
        anything. The suite runs on the standard library."""
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
        """If somebody raises the floor in the README, the matrix has to follow.
        And the other way round: a matrix that does not include the declared
        minimum leaves the README's claim unchecked."""
        readme = (REPO / "README.md").read_text()
        minimo = re.search(r"Python (\d+\.\d+)\+", readme)
        self.assertIsNotNone(minimo, "el README ya no declara version minima")
        self.assertIn(f'"{minimo.group(1)}"', self.texto)

    def test_comprueba_que_la_suite_no_escribe_en_los_registros(self):
        """The suite claims it in its docstring; the workflow verifies it after
        running it, which is the only way the claim does not go stale."""
        self.assertIn("git status --porcelain -- results", self.texto)

    def test_las_acciones_van_clavadas_a_un_sha_completo(self):
        """A tag can be repointed by its owner at other code; a commit cannot.
        It is the convention of the rest of the repositories in this account,
        and it arrived late here: this workflow was born with `@v4` and spent a
        day on `@v7`."""
        refs = re.findall(r"^\s*- uses: (\S+)@(\S+)", self.texto, re.M)
        self.assertTrue(refs, "el flujo ya no usa ninguna accion")
        for accion, ref in refs:
            with self.subTest(accion):
                self.assertRegex(ref, SHA,
                                 f"{accion} va por etiqueta, no por commit")

    def test_cada_sha_lleva_su_version_al_lado(self):
        """A SHA is only readable if it says which version it is. Without the
        comment, bumping an action forces you to resolve the hash to know where
        you are starting from."""
        for linea in self.texto.splitlines():
            if "- uses:" in linea:
                with self.subTest(linea.strip()[:40]):
                    self.assertRegex(linea, r"@[0-9a-f]{40} # v\d+\.\d+\.\d+$")

    def _cuerpo_del_trabajo(self, trabajo: str) -> str:
        """From the job's header to the next one's.

        The cut looks for the next key with TWO spaces of indentation, which is
        the next job's. Splitting on a bare `\\n  ` does not work: the lines
        inside the job are indented by four, and they start with those two.
        """
        resto = self.texto.split(f"\n  {trabajo}:\n", 1)[1]
        siguiente = re.search(r"^  [A-Za-z0-9_-]+:", resto, re.M)
        return resto[: siguiente.start()] if siguiente else resto

    def test_cada_trabajo_tiene_tope_de_tiempo(self):
        """Without a cap, a hung job runs to the platform limit. It is not a
        speed target; it is so that a hang fails instead of burning."""
        trabajos = re.findall(r"^  ([A-Za-z0-9_-]+):$",
                              self.texto.split("\njobs:\n", 1)[1], re.M)
        self.assertTrue(trabajos, "el flujo ya no declara ningun trabajo")
        for trabajo in trabajos:
            with self.subTest(trabajo):
                self.assertIn("timeout-minutes:",
                              self._cuerpo_del_trabajo(trabajo))

    def test_main_no_se_cancela_nunca(self):
        """Here commits go straight to main and the workflow status is the only
        record that a commit passed the suite. A plain
        `cancel-in-progress: true` leaves every commit overtaken by the next one
        as "cancelled": they did not fail, they simply never answered. The
        exception is the decision; simplifying it would erase it silently."""
        self.assertIn("cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}",
                      self.texto)


class TestDependabot(unittest.TestCase):
    """What keeps the SHA pin from fossilizing.

    A pinned SHA does not age noisily: it sits still and silent. The pin and
    this watch are a single decision split across two files, and removing the
    bottom half breaks nothing visible.
    """

    def setUp(self):
        self.texto = DEPENDABOT.read_text()

    def test_existe(self):
        self.assertTrue(DEPENDABOT.is_file(),
                        f"falta {DEPENDABOT.relative_to(REPO)}")

    def test_vigila_las_acciones_de_CI(self):
        self.assertIn("package-ecosystem: github-actions", self.texto)

    def test_NO_vigila_pip_a_proposito(self):
        """The absence is the decision, not an oversight.

        `openai==2.53.0` and the lock's transitive closure are not an outdated
        dependency: they are the provenance of the environment that produced the
        records. A weekly PR proposing to bump them would train the habit of
        merging without looking, which is the carelessness the lock exists to
        prevent.
        """
        self.assertNotIn("package-ecosystem: pip", self.texto)
        self.assertIn("requirements.lock.txt", self.texto,
                      "si se deja pip fuera, el motivo va escrito al lado")


if __name__ == "__main__":
    unittest.main()
