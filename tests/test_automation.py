"""
That something runs the suite without anyone having to remember.

Having hundreds of tests and depending on someone remembering to launch them is
having fewer tests than it looks. There are two nets, covering different moments:

  * `.githooks/pre-commit`, before every commit, locally.
  * `.github/workflows/tests.yml`, on every push and every PR, including what
    was pushed with `--no-verify`.

This watches that both are still there and still run what they say they run. It
is a small thing, but it is exactly the kind of failure that gives no warning: a
hook without the execute bit or a renamed workflow raise no error, they simply
stop running and nobody notices until it matters.

Since August 7, 2026 there is a third net, and it does not live in this
repository: a GitHub ruleset protects `main` —PR required, no force-push, no
deletion— and requires the status check `ci-complete`. That check is the
aggregate job at the end of the workflow, so half of that decision IS here and
can be broken from here: renaming the job blocks every merge, silently and
forever. That is what `test_the_check_the_ruleset_requires_exists` watches.

Since August 14, 2026 the hook carries a second job besides running the suite: it
refuses a commit that mixes a signed plan with anything else. That one is
*executed* here rather than read —`TestThePlanGuard` runs the real hook over
throwaway repositories— because a guard pinned by a substring is a guard whose
behaviour nobody checks.

What is NOT checked here is that the hook is installed: `core.hooksPath` is
local configuration per clone and is not set in CI. Nor is the ruleset, which
lives in the repository settings and not in a versioned file. The instruction to
install the hook is in the README and in the header of the hook itself.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")

REPO = Path(__file__).resolve().parent.parent

HOOK = REPO / ".githooks" / "pre-commit"
WORKFLOW = REPO / ".github" / "workflows" / "tests.yml"
DEPENDABOT = REPO / ".github" / "dependabot.yml"

SUITE = "unittest discover"


class TestThePreCommitHook(unittest.TestCase):

    def test_exists(self):
        self.assertTrue(HOOK.is_file(), f"falta {HOOK.relative_to(REPO)}")

    def test_is_executable(self):
        """Without the execute bit git ignores it silently."""
        self.assertTrue(os.access(HOOK, os.X_OK), "el hook no es ejecutable")

    def test_runs_the_suite(self):
        self.assertIn(SUITE, HOOK.read_text())

    def test_says_how_to_install_itself(self):
        """The hook is versioned but does not enable itself: `core.hooksPath`
        is per-clone configuration."""
        self.assertIn("core.hooksPath", HOOK.read_text())

    def test_does_not_need_the_venv(self):
        """If the hook depended on `.venv`, a fresh clone could not commit
        anything. The suite runs on the standard library."""
        self.assertNotIn(".venv", HOOK.read_text())


class TestThePlanGuard(unittest.TestCase):
    """That the hook still refuses a signed plan committed accompanied.

    This one is not pinned by reading the file. `TestThePreCommitHook` can
    check that the CI half exists because it cannot run GitHub Actions from
    here; the hook it CAN run, and a guard whose only test is
    `assertIn("PLAN_", texto)` passes just as happily over a guard that has been
    broken into always letting everything through.

    So the real hook is run over throwaway repositories. Two details make that
    cheap and safe: the hook resolves its own root with `git rev-parse
    --show-toplevel`, so from another repository it reads that other index and
    never this one; and `python3` is masked with a stub, so the pass cases do
    not relaunch this very suite from inside itself.

    What the guard is for is in the hook's header and in the README: on
    2026-08-13 the §0 signature arrived inside a commit about the start-budget
    diagnostic, and stopped being findable in the log.
    """

    HOOK = HOOK

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="guarda-de-planes-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

        # The stub lives outside the repository, where no `git add` can reach
        # it. It stands in for the suite: reaching it means the guard let the
        # commit through.
        binario = self.tmp / "bin"
        binario.mkdir()
        (binario / "python3").write_text("#!/bin/sh\necho SUITE-LANZADA\n")
        (binario / "python3").chmod(0o755)

        # Neither the user's global config nor the system's: this repository
        # sets `core.hooksPath`, and inheriting it would run the hook again on
        # the fixture's own commit.
        self.env = dict(
            os.environ,
            PATH=f"{binario}{os.pathsep}{os.environ['PATH']}",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_SYSTEM=os.devnull,
        )

    def _git(self, root: Path, *order: str):
        return subprocess.run(("git",) + order, cwd=root, env=self.env,
                              check=True, capture_output=True, text=True)

    def _repo(self, with_history: bool = True) -> Path:
        root = self.tmp / f"repo{len(list(self.tmp.iterdir()))}"
        root.mkdir()
        self._git(root, "init", "-q")
        self._git(root, "config", "user.email", "prueba@example.invalid")
        self._git(root, "config", "user.name", "prueba")
        if with_history:
            (root / "semilla.txt").write_text("semilla\n")
            self._git(root, "add", "semilla.txt")
            self._git(root, "commit", "-q", "-m", "semilla")
        return root

    def _commit(self, *paths: str, with_history: bool = True):
        """Stage those paths in a fresh repository and run the real hook."""
        root = self._repo(with_history)
        for path in paths:
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(f"contenido de {path}\n")
            self._git(root, "add", "--", path)
        return subprocess.run([str(self.HOOK)], cwd=root, env=self.env,
                              capture_output=True, text=True)

    def _rejected(self, output):
        self.assertEqual(output.returncode, 1, output.stderr or output.stdout)
        self.assertIn("mezcla un plan firmado", output.stderr)
        self.assertNotIn("SUITE-LANZADA", output.stdout)

    def _aceptado(self, output):
        self.assertEqual(output.returncode, 0, output.stderr or output.stdout)
        self.assertNotIn("mezcla un plan firmado", output.stderr)
        self.assertIn("SUITE-LANZADA", output.stdout,
                      "no llego a la suite: paro antes por otro motivo")

    def test_refuses_a_plan_accompanied_by_code(self):
        """The 2026-08-13 case, which is the one that has already happened."""
        self._rejected(self._commit("PLAN_BUDGET_LS.md",
                                    "rung3/local_search.py"))

    def test_refuses_PREDICTION_accompanied(self):
        """Hard rule 2 of `CLAUDE.md`: the prediction is Sergi's, and it is
        written before the long run. Same reason, same treatment."""
        self._rejected(self._commit("PREDICTION.md", "run_experiment.py"))

    def test_refuses_even_when_the_companion_is_prose(self):
        """It is not about code. A signature swept in next to a README edit is
        just as unfindable."""
        self._rejected(self._commit("PLAN_AUDIT.md", "README.md"))

    def test_the_message_names_both_sides(self):
        """A guard that says no without saying to what is a guard people
        disable."""
        output = self._commit("PLAN_BUDGET_LS.md", "rung3/local_search.py")
        self.assertIn("PLAN_BUDGET_LS.md", output.stderr)
        self.assertIn("rung3/local_search.py", output.stderr)

    def test_lets_the_plan_through_alone(self):
        """Sergi's signing commit. The guard forbids the company, not the
        act."""
        self._aceptado(self._commit("PLAN_BUDGET_LS.md"))

    def test_lets_several_plans_through_together(self):
        """Deliberate, and this is where it is written down: a commit carrying
        only plans is still filed as a plan commit, which is all the guard is
        protecting. Nothing hides behind them."""
        self._aceptado(self._commit("PLAN_BUDGET_LS.md", "PREDICTION.md"))

    def test_lets_a_commit_without_plans_through(self):
        """The common case has to stay free: the guard is not a toll on every
        commit."""
        self._aceptado(self._commit("rung3/local_search.py", "README.md"))

    def test_a_plan_in_a_subdirectory_does_not_count(self):
        """Anchored to the root. `docs/PLAN_algo.md` is documentation about a
        plan, not a signed one, and blocking it would teach people to reach for
        `--no-verify` — which is the same hole with extra steps."""
        self._aceptado(self._commit("docs/PLAN_algo.md",
                                    "rung3/local_search.py"))

    def test_does_not_break_on_the_first_commit(self):
        """Without HEAD there is nothing to diff the index against, and the
        hook runs under `set -e`: the empty tree is the fallback. A clone that
        cannot commit anything at all would get the hook uninstalled the same
        afternoon."""
        self._aceptado(self._commit("rung3/local_search.py",
                                    with_history=False))
        self._rejected(self._commit("PLAN_BUDGET_LS.md", "run_experiment.py",
                                    with_history=False))


class TestTheCIWorkflow(unittest.TestCase):

    def setUp(self):
        self.text = WORKFLOW.read_text()

    def test_exists(self):
        self.assertTrue(WORKFLOW.is_file(), f"falta {WORKFLOW.relative_to(REPO)}")

    def test_runs_the_suite(self):
        self.assertIn(SUITE, self.text)

    def test_fires_on_push_and_on_pull_request(self):
        for event in ("push:", "pull_request:"):
            with self.subTest(event):
                self.assertIn(event, self.text)

    def test_covers_the_python_minimum_the_README_declares(self):
        """If somebody raises the floor in the README, the matrix has to follow.
        And the other way round: a matrix that does not include the declared
        minimum leaves the README's claim unchecked."""
        readme = (REPO / "README.md").read_text()
        minimum = re.search(r"Python (\d+\.\d+)\+", readme)
        self.assertIsNotNone(minimum, "el README ya no declara version minima")
        self.assertIn(f'"{minimum.group(1)}"', self.text)

    def test_checks_the_suite_does_not_write_to_the_records(self):
        """The suite claims it in its docstring; the workflow verifies it after
        running it, which is the only way the claim does not go stale."""
        self.assertIn("git status --porcelain -- results", self.text)

    def test_the_actions_are_pinned_to_a_full_sha(self):
        """A tag can be repointed by its owner at other code; a commit cannot.
        It is the convention of the rest of the repositories in this account,
        and it arrived late here: this workflow was born with `@v4` and spent a
        day on `@v7`."""
        refs = re.findall(r"^\s*- uses: (\S+)@(\S+)", self.text, re.M)
        self.assertTrue(refs, "el flujo ya no usa ninguna accion")
        for action_taken, ref in refs:
            with self.subTest(action_taken):
                self.assertRegex(ref, SHA,
                                 f"{action_taken} va por etiqueta, no por commit")

    def test_each_sha_carries_its_version_alongside(self):
        """A SHA is only readable if it says which version it is. Without the
        comment, bumping an action forces you to resolve the hash to know where
        you are starting from."""
        for line in self.text.splitlines():
            if "- uses:" in line:
                with self.subTest(line.strip()[:40]):
                    self.assertRegex(line, r"@[0-9a-f]{40} # v\d+\.\d+\.\d+$")

    def _job_body(self, job: str) -> str:
        """From the job's header to the next one's.

        The cut looks for the next key with TWO spaces of indentation, which is
        the next job's. Splitting on a bare `\\n  ` does not work: the lines
        inside the job are indented by four, and they start with those two.
        """
        resto = self.text.split(f"\n  {job}:\n", 1)[1]
        next = re.search(r"^  [A-Za-z0-9_-]+:", resto, re.M)
        return resto[: next.start()] if next else resto

    def test_each_job_has_a_time_cap(self):
        """Without a cap, a hung job runs to the platform limit. It is not a
        speed target; it is so that a hang fails instead of burning."""
        jobs = re.findall(r"^  ([A-Za-z0-9_-]+):$",
                          self.text.split("\njobs:\n", 1)[1], re.M)
        self.assertTrue(jobs, "el flujo ya no declara ningun trabajo")
        for job in jobs:
            with self.subTest(job):
                self.assertIn("timeout-minutes:",
                              self._job_body(job))

    def test_main_is_never_cancelled(self):
        """Commits reach main one after another and the workflow status is the
        only record that a commit passed the suite. A plain
        `cancel-in-progress: true` leaves every commit overtaken by the next one
        as "cancelled": they did not fail, they simply never answered. The
        exception is the decision; simplifying it would erase it silently.

        The premise changed on August 7, 2026 —commits used to go straight to
        main and now arrive by merge— and the exception survives it: what it
        protects is the run on main, not the route the commit took."""
        self.assertIn("cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}",
                      self.text)

    def test_the_check_the_ruleset_requires_exists(self):
        """`ci-complete` is the required status check of the ruleset that
        protects `main`. It is one decision split across two places, and only
        one of them is in this repository: renaming the job here leaves the
        ruleset waiting forever for a check that nobody reports, which does not
        fail anything — it blocks every merge, in silence.

        It aggregates on purpose instead of the ruleset requiring the matrix
        legs: `suite (3.10)` stops existing the day the floor moves, and a
        required check that never reports again is unsatisfiable."""
        body = self._job_body("ci-complete")
        self.assertIn("needs: [suite]", body)
        self.assertIn("if: always()", body)
        self.assertIn("contains(needs.*.result, 'failure')", body)


class TestDependabot(unittest.TestCase):
    """What keeps the SHA pin from fossilizing.

    A pinned SHA does not age noisily: it sits still and silent. The pin and
    this watch are a single decision split across two files, and removing the
    bottom half breaks nothing visible.
    """

    def setUp(self):
        self.text = DEPENDABOT.read_text()

    def test_exists(self):
        self.assertTrue(DEPENDABOT.is_file(),
                        f"falta {DEPENDABOT.relative_to(REPO)}")

    def test_watches_the_CI_actions(self):
        self.assertIn("package-ecosystem: github-actions", self.text)

    def test_does_NOT_watch_pip_on_purpose(self):
        """The absence is the decision, not an oversight.

        `openai==2.53.0` and the lock's transitive closure are not an outdated
        dependency: they are the provenance of the environment that produced the
        records. A weekly PR proposing to bump them would train the habit of
        merging without looking, which is the carelessness the lock exists to
        prevent.
        """
        self.assertNotIn("package-ecosystem: pip", self.text)
        self.assertIn("requirements.lock.txt", self.text,
                      "si se deja pip fuera, el motivo va escrito al lado")


if __name__ == "__main__":
    unittest.main()
