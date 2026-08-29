"""
The environment record that accompanies every results JSON.

It includes the check that really matters: that the `_env` block does not leak
the API key (hard rule 7). Only one environment variable is read,
`PYTHONHASHSEED`, and this test pins that in case somebody adds another without
thinking.

The last class walks the code looking for JSON writers and requires all of them
to hang their `_env`. It is what prevents the next script added from producing
records without provenance again, which is how the original debt came about.
"""

from __future__ import annotations

import importlib
import json
import re
import unittest
from pathlib import Path
from unittest import mock

from harness import provenance
from harness.provenance import code_digest, describe, environment

REPO = Path(__file__).resolve().parent.parent

KEYS = {"recorded_at", "python", "openai", "platform", "pythonhashseed",
        "git_commit", "git_dirty", "code_dirty", "code_digest"}

# Modules that dump a results JSON. The list is in the README, in the table
# "reproducing a figure overwrites its own record".
WRITERS = [
    "run_experiment",
    "harness.subsumption_check",
    "harness.learned_subsumption",
    "rung2.ceiling_check2",
    "rung2.compare_runs",
    "rung2.note_audit",
    "rung2.run2",
    "rung3.order_search",
    "rung3.budget_and_balance",
    "rung4.sweep",
    # Added 2026-08-15 with the module. It does not close F1 of the optimizer
    # audit — this list still under-lists the writers the README table carries —
    # it only keeps the newest one from joining the omission.
    "rung3.order_metrics_run",
    # The same instrument on the corpus surface, added 2026-08-15. A separate
    # writer because it is a separate record: it must never land on
    # order_metrics.json, which owns the space figures.
    "rung3.order_metrics_corpus",
    # The join of those two records, added 2026-08-15. It writes a record and
    # reads two, so it belongs here; adding it widens what this test covers,
    # which is the only direction this list is ever allowed to move.
    "rung3.rank_transfer",
    # The space restricted to the points the corpus touches, added 2026-08-16.
    # A fourth writer for the same reason as the second: it must never land on
    # order_metrics.json or order_metrics_corpus.json, which own the two
    # surfaces it compares.
    "rung3.order_metrics_touched",
    # The same 2,080 pairs read at the level of the rules, added 2026-08-16. A
    # fifth writer and a fifth record: it reads three of the four above and
    # rewrites none of them. Adding it here widens what this test covers, which
    # is the only direction this list is ever allowed to move.
    "rung3.order_metrics_rules",
    # Who holds territory, added 2026-08-16 with the audit note on part five.
    # A sixth writer: it reads order_metrics_rules.json — kappa included, which
    # it never recomputes — and writes territory_holders.json, correcting the
    # reading of a figure rather than any of its values.
    "rung3.territory_holders",
    # The default-rule control, added 2026-08-29 with the module. A seventh
    # writer and the first one under `harness/` on this list: it writes
    # results/default_rule_control.json and reads nothing, and it is here for
    # the same reason as the six above — this list only ever grows.
    "harness.default_rule_control",
    # The hybrid ceiling on the exhaustive space, added 2026-08-29. An eighth
    # writer and a separate record: it must never land on results2/ceiling2.json,
    # which owns the corpus figures of rung 2's Step 0.
    "rung2.ceiling_check2_space",
    # The sensitivity family, added 2026-08-29 with the package. Two writers, and
    # they are separate records on purpose: the gate's verdict must be readable
    # without the sweep, since the gate is what says whether the sweep may run.
    "sensitivity.generator_check",
    "sensitivity.sweep",
]

CODE_ROOTS = ("harness", "rung2", "rung3", "rung4", "sensitivity",
               "run_experiment.py")


class TestEnvironment(unittest.TestCase):

    def test_carries_the_declared_keys(self):
        self.assertEqual(set(environment()), KEYS)

    def test_is_json_serializable(self):
        json.dumps(environment())

    def test_the_timestamp_is_UTC_in_seconds(self):
        self.assertRegex(environment()["recorded_at"],
                         r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_accepts_extra_fields(self):
        e = environment(seed=17, n=2000)
        self.assertEqual(e["seed"], 17)
        self.assertEqual(e["n"], 2000)

    def test_the_extras_can_overwrite(self):
        self.assertEqual(environment(python="3.99")["python"], "3.99")

    def test_picks_up_PYTHONHASHSEED(self):
        with mock.patch.dict("os.environ", {"PYTHONHASHSEED": "7"}):
            self.assertEqual(environment()["pythonhashseed"], "7")

    def test_without_PYTHONHASHSEED_it_stays_null(self):
        """`null` means "unset", that is, random. It is information."""
        with mock.patch.dict("os.environ", clear=True):
            self.assertIsNone(environment()["pythonhashseed"])

    def test_does_NOT_leak_the_API_key(self):
        fake = "sk-or-v1-000ESTOESUNSECRETO000"
        with mock.patch.dict("os.environ", {"OPENROUTER_API_KEY": fake,
                                            "ANTHROPIC_API_KEY": fake}):
            dump = json.dumps(environment())
        self.assertNotIn(fake, dump)
        self.assertNotIn("API_KEY", dump)

    def test_describe_is_one_line(self):
        line = describe()
        self.assertNotIn("\n", line)
        self.assertIn("python", line)


class TestCodeDigest(unittest.TestCase):

    def test_is_stable_across_calls(self):
        self.assertEqual(code_digest(), code_digest())

    def test_has_the_declared_length(self):
        self.assertEqual(len(code_digest()), provenance.DIGEST_CHARS)

    def test_changes_if_the_code_changes(self):
        with mock.patch.object(provenance, "REPO", Path(self.tmp)):
            one = code_digest()
            (Path(self.tmp) / "harness" / "x.py").write_text("y = 2\n")
            two = code_digest()
        self.assertNotEqual(one, two)

    def test_does_not_depend_on_the_root_directory_name(self):
        """The digest is of the content: moving the repo does not change it."""
        with mock.patch.object(provenance, "REPO", Path(self.tmp)):
            one = code_digest()
        other = Path(self.tmp2)
        (other / "harness").mkdir(parents=True)
        (other / "harness" / "x.py").write_text("y = 1\n")
        (other / "run_experiment.py").write_text("pass\n")
        with mock.patch.object(provenance, "REPO", other):
            two = code_digest()
        self.assertEqual(one, two)

    def test_does_not_include_the_tests(self):
        """Changing a test changes no figure; the digest must not move because
        of it."""
        self.assertNotIn("tests", provenance.CODE_ROOTS)

    def test_with_no_sources_it_returns_None(self):
        with mock.patch.object(provenance, "REPO", Path(self.empty)):
            self.assertIsNone(code_digest())

    def setUp(self):
        import tempfile

        self._dirs = [tempfile.TemporaryDirectory() for _ in range(3)]
        self.tmp, self.tmp2, self.empty = (d.name for d in self._dirs)
        (Path(self.tmp) / "harness").mkdir()
        (Path(self.tmp) / "harness" / "x.py").write_text("y = 1\n")
        (Path(self.tmp) / "run_experiment.py").write_text("pass\n")

    def tearDown(self):
        for d in self._dirs:
            d.cleanup()


class TestGit(unittest.TestCase):

    def test_outside_a_repo_it_does_not_blow_up(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(provenance, "REPO", Path(tmp)):
                e = environment()
        self.assertIsNone(e["git_commit"])
        self.assertIsNone(e["git_dirty"])
        self.assertIsNone(e["code_dirty"])

    def test_inside_the_repo_there_is_a_commit(self):
        e = environment()
        self.assertRegex(e["git_commit"], r"^[0-9a-f]{40}$")
        self.assertIsInstance(e["git_dirty"], bool)
        self.assertIsInstance(e["code_dirty"], bool)


class TestTheTwoDirtyFlags(unittest.TestCase):
    """`git_dirty` and `code_dirty` are not redundant, and the difference
    matters.

    Only `code_dirty` decides whether `git_commit` identifies the code that ran.
    `git_dirty` covers the rest, which is not always harmless: three writers
    read records from `results*/` as INPUT. Splitting them (Aug 7, 2026) came
    out of re-running six records back to back, where each script dirtied the
    tree for the next one with its own output.

    A fake repo is set up because the distinction cannot be provoked in the real
    one without dirtying it.
    """

    def setUp(self):
        import subprocess
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "harness").mkdir()
        (self.repo / "harness" / "x.py").write_text("y = 1\n")
        (self.repo / "results").mkdir()
        (self.repo / "results" / "cifra.json").write_text("{}\n")

        def git(*args):
            subprocess.run(("git", "-C", str(self.repo), *args),
                           check=True, capture_output=True)

        git("init", "-q")
        git("add", "-A")
        git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base")

    def tearDown(self):
        self._tmp.cleanup()

    def _env(self):
        with mock.patch.object(provenance, "REPO", self.repo):
            return environment()

    def test_with_a_clean_tree_both_are_false(self):
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (False, False))

    def test_a_modified_record_dirties_the_tree_but_not_the_code(self):
        """The batch case: one script's output does not invalidate the next
        one's commit, and until now the two looked the same."""
        (self.repo / "results" / "cifra.json").write_text('{"a": 1}\n')
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, False))

    def test_modified_code_dirties_both(self):
        (self.repo / "harness" / "x.py").write_text("y = 2\n")
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, True))

    def test_an_untracked_code_file_also_counts(self):
        """A new module without `git add` changes what runs just as a modified
        one does, and the digest already picks it up; the flag must too."""
        (self.repo / "harness" / "nuevo.py").write_text("z = 3\n")
        e = self._env()
        self.assertEqual((e["git_dirty"], e["code_dirty"]), (True, True))

    def test_the_readable_line_tells_the_two_cases_apart(self):
        with mock.patch.object(provenance, "REPO", self.repo):
            self.assertNotIn("sucio", describe())
            (self.repo / "results" / "cifra.json").write_text('{"a": 1}\n')
            self.assertIn("+arbol-sucio", describe())
            (self.repo / "harness" / "x.py").write_text("y = 2\n")
            self.assertIn("+codigo-sucio", describe())


class TestEveryWriterRecordsEnvironment(unittest.TestCase):

    def test_the_known_writers_import_environment(self):
        for name in WRITERS:
            with self.subTest(name):
                mod = importlib.import_module(name)
                self.assertIn("environment", vars(mod),
                              f"{name} no importa harness.provenance.environment")

    def test_no_JSON_writer_is_left_without_env(self):
        """Discovers NEW writers: any `write_text(json.dumps(...))` in the code
        must carry its `_env` block alongside."""
        without_env = []
        for root in CODE_ROOTS:
            p = REPO / root
            files = [p] if p.is_file() else [
                f for f in p.rglob("*.py") if "__pycache__" not in f.parts]
            for f in files:
                src = f.read_text()
                if re.search(r"write_text\(\s*json\.dumps", src) and '"_env"' not in src:
                    without_env.append(str(f.relative_to(REPO)))
        self.assertEqual(without_env, [], f"escriben JSON sin procedencia: {without_env}")


if __name__ == "__main__":
    unittest.main()
