"""
The environment record that accompanies every results JSON.

It includes the check that really matters: that the `_env` block does not leak
the API key (hard rule 7). Only one environment variable is read,
`PYTHONHASHSEED`, and this test pins that in case somebody adds another without
thinking.

The last two classes hold that debt closed from both ends. The first walks the
code looking for JSON writers and requires all of them to hang their `_env`: it
is what prevents the next script added from producing records without
provenance again, which is how the original debt came about. The second walks
the records themselves and pins the thirteen that will never carry one.

The hand list of writers that used to live here is gone: it under-listed the tree
for six days without anyone noticing (F1 and F7 of the optimizer audit), and
`tests/test_writer_lists.py` derives it instead.
"""

from __future__ import annotations

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

# Imported, not repeated. A second copy of this tuple is the defect F1 is about:
# when `sensitivity` and `ilp` were added, two places had to be edited and only a
# failing test caught the second. `tests/test_writer_lists.py` derives from it.
from harness.provenance import CODE_ROOTS


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
    """**`WRITERS` was deleted on 2026-08-30 and this class kept only the half
    that was already derived.** The hand list under-listed the tree — finding F1
    of `results3/FINDINGS_AUDIT.md` — and what it asserted is now asserted over
    every writer by `tests/test_writer_lists.py`, which also checks that the
    README table still mirrors the tree."""

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


def records_without_env(root: Path) -> set[str]:
    """Every JSON record under `results*/` whose top level carries no `_env`,
    as a path relative to `root`."""
    without = set()
    for p in root.glob("results*/**/*.json"):
        record = json.loads(p.read_text(encoding="utf-8"))
        if not (isinstance(record, dict) and "_env" in record):
            without.add(p.relative_to(root).as_posix())
    return without


class TestTheRecordsWithoutEnv(unittest.TestCase):
    """**Thirteen records carry no `_env`, and on 2026-10-20 Sergi closed that
    by decision: they never will.** This class pins the list in both directions.

    Ten cost money and would not come out the same, because the proposer is not
    deterministic at `temperature 0`: a new run would be another record, and
    `results/llm_run.json` is the base rungs 3 and 4 and most later threads
    start from (hard rule 4).
    Three are free and are kept as published, before the 2026-08-06 tie-break
    fix, beside the audit's `_ls` records. All thirteen entered git in the first
    commit, after they were produced, so no commit identifies the code that
    wrote them, and a block added now would be invented. `IDEAS.md`, *Technical
    debt*, gives the reasons.

    A fourteenth record without `_env` is a writer that dropped it. The class
    above only finds writers that use `write_text(json.dumps(...))`; this one
    finds the record, however it was written. One of the thirteen gaining a
    block means it was re-run or rewritten, which is a decision to record in
    `results2/RECORD_NOTES.md` and here, not a fix.
    """

    LEGACY = {
        # Rung 1, paid.
        "results/llm_run.json",
        "results/llm_run_n100_smoke.json",
        # Rung 2's eight runs at n=100, paid.
        "results2/llm_run2_n100.json",
        "results2/llm_run2_n100_seed18.json",
        "results2/llm_run2_n100_seed19.json",
        "results2/llm_run2_n100_seed20.json",
        "results2/llm_run2_n100_v2.json",
        "results2/llm_run2_n100_v2_seed18.json",
        "results2/llm_run2_n100_v2_seed19.json",
        "results2/llm_run2_n100_v2_seed20.json",
        # Free, kept as published before the tie-break fix.
        "results3/budget_and_balance.json",
        "results3/order_search.json",
        "results4/sweep.json",
    }

    def test_the_records_without_env_are_exactly_the_thirteen(self):
        self.assertEqual(records_without_env(REPO), self.LEGACY,
                         "the records without _env are no longer the thirteen")

    def test_it_finds_a_record_however_it_was_written(self):
        """Read off the record, not the source: a bare list, a block nested
        below the top level and a subdirectory all count as without, and a
        session's `.partial.jsonl` is not a record."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "results9" / "sub").mkdir(parents=True)
            (root / "results9" / "ok.json").write_text('{"_env": {}, "x": 1}')
            (root / "results9" / "bare.json").write_text("[1, 2]")
            (root / "results9" / "nested.json").write_text('{"rows": [{"_env": {}}]}')
            (root / "results9" / "sub" / "deep.json").write_text('{"x": 1}')
            (root / "results9" / "a.partial.jsonl").write_text('{"x": 1}\n')
            self.assertEqual(records_without_env(root), {
                "results9/bare.json", "results9/nested.json", "results9/sub/deep.json"})


if __name__ == "__main__":
    unittest.main()
