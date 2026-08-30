"""
The guard against overwriting the records that cannot be regenerated.

WHAT IT IS PROTECTING, AND WHY IT NEEDS ITS OWN TESTS

Until August 8, 2026 `run_experiment.py llm` wrote `results/llm_run.json`
whatever `--n` it was given, so `llm --n 100` — the cheap command the
getting-started recommends — destroyed the 2000-case record that is the input
of rungs 3 and 4. Money and non-determinism make that loss irreversible.

Three families here, and they answer different questions:

  * THE GUARD in isolation: what it refuses, what it lets through and what it
    says when it refuses. The message is part of the contract — a guard that
    aborts without saying what would be lost only teaches people to reach for
    the flag.

  * THE DESTINATIONS: that the naming rule no longer collides across `--n`, and
    that the guard fires from inside the commands BEFORE spending a call. That
    last one is the whole point: aborting after 632 calls would be worse than
    not guarding.

  * WHAT MUST NOT BE GUARDED: the deterministic, free records. Re-running them
    is the reproducibility check and a guard there would obstruct it. Rungs 3
    and 4 are pending a re-run with a serious optimizer, and that too must stay
    unobstructed.

Like the rest of the suite, this module writes nothing to `results*/`: it works
in temporary directories and the last class checks precisely that.
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
from unittest import mock

import run_experiment
from harness.record_guard import (
    FLAG,
    RecordExists,
    describe,
    refuse_overwrite,
    refuse_shrink,
)
from rung2 import compare_runs, note_audit, run2

REPO = Path(__file__).resolve().parent.parent

# A record with everything the message quotes, in the shape rung 1 writes.
RECORD_PATH = {
    "_env": {"recorded_at": "2026-08-06T01:31:12Z", "n": 2000, "seed": 17},
    "model": "deepseek/deepseek-v4-flash",
    "metrics": {"n_rules": 577, "llm_calls": 632},
    "rules": [{"rule_id": f"r{i}"} for i in range(577)],
    "records": [{}] * 2000,
}


# One row of `compare_runs`, with the keys its report prints. It stands in for
# `analyse` so that no test has to read the eight real runs.
ROW = {
    "file": "llm_run2_n100.json", "seed": 17, "prompt_version": "v1",
    "n_rules": 30, "mean_conditions": 2.0, "cond_hist": {2: 30},
    "overlap_pct": 1.0, "overlapping_diff_action": 0, "nested_pairs": 0,
    "conflicts": 0, "impasses": 0, "edges_proposed": 0, "edges_accepted": 0,
    "edge_reasons": {}, "coverage": 0.5, "silent_error_rate": 0.1,
    "e2e": 0.5, "mean_ext_size": 100,
}


class WithTempDir(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name: str, dato) -> Path:
        p = self.dir / name
        p.write_text(json.dumps(dato))
        return p


# ---------------------------------------------------------------------------
# The guard on the destination
# ---------------------------------------------------------------------------

class TestDestinationRefusal(WithTempDir):

    def test_a_free_destination_passes_without_noise(self):
        destination = self.dir / "no_existe.json"
        self.assertEqual(refuse_overwrite(destination, overwrite=False), destination)

    def test_an_occupied_destination_aborts(self):
        p = self.write("llm_run.json", RECORD_PATH)
        with self.assertRaises(RecordExists):
            refuse_overwrite(p, overwrite=False)

    def test_with_the_explicit_flag_it_lets_through(self):
        p = self.write("llm_run.json", RECORD_PATH)
        self.assertEqual(refuse_overwrite(p, overwrite=True), p)

    def test_deletes_and_copies_nothing_when_aborting(self):
        """Refuse by default and make NO automatic copy: silent backups pile up
        and people stop looking at them."""
        p = self.write("llm_run.json", RECORD_PATH)
        before = sorted(x.name for x in self.dir.iterdir())
        fingerprint = hashlib.sha256(p.read_bytes()).hexdigest()
        with self.assertRaises(RecordExists):
            refuse_overwrite(p, overwrite=False)
        self.assertEqual(sorted(x.name for x in self.dir.iterdir()), before)
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), fingerprint)

    def test_a_directory_as_destination_also_aborts(self):
        (self.dir / "carpeta").mkdir()
        with self.assertRaises(RecordExists):
            refuse_overwrite(self.dir / "carpeta", overwrite=False)

    def test_an_unreadable_json_does_not_disable_the_guard(self):
        """An unreadable file is still a file that would be lost. The failure
        degrades the description, it does not lift the refusal."""
        p = self.dir / "roto.json"
        p.write_text("{esto no es JSON")
        with self.assertRaises(RecordExists) as e:
            refuse_overwrite(p, overwrite=False)
        self.assertIn("no se pudo leer como JSON", str(e.exception))


class TestTheMessageSaysWhatWouldBeLost(WithTempDir):
    """A guard that aborts without saying what is at stake only teaches people
    to type the flag."""

    def message(self, dato=RECORD_PATH, name="llm_run.json") -> str:
        p = self.write(name, dato)
        with self.assertRaises(RecordExists) as e:
            refuse_overwrite(p, overwrite=False,
                             exits=("--out OTRO", f"{FLAG} a proposito"))
        return str(e.exception)

    def test_names_the_file(self):
        self.assertIn("llm_run.json", self.message())

    def test_carries_date_model_cases_rules_and_calls(self):
        m = self.message()
        self.assertIn("2026-08-06T01:31:12Z", m)
        self.assertIn("deepseek/deepseek-v4-flash", m)
        self.assertIn("2000", m)
        self.assertIn("577", m)
        self.assertIn("632", m)

    def test_offers_both_ways_out(self):
        m = self.message()
        self.assertIn("--out", m)
        self.assertIn(FLAG, m)

    def test_explains_that_it_cannot_be_regenerated(self):
        self.assertIn("determinista", self.message())

    def test_the_flag_is_not_called_force(self):
        """It must name what it does, so that it does not get typed out of
        habit."""
        self.assertEqual(FLAG, "--overwrite-record")
        self.assertNotIn("--force", self.message())


class TestDescriptionOfRealRecords(unittest.TestCase):
    """Against the records on disk, read-only. Two of them —the ones that cost
    money— have no `_env`, which is exactly the case the description has to
    survive."""

    def test_the_rung_1_record_is_described_in_full(self):
        lineas = dict(describe(REPO / "results" / "llm_run.json"))
        self.assertEqual(lineas["modelo"], "deepseek/deepseek-v4-flash")
        self.assertEqual(lineas["casos"], "2000")
        self.assertEqual(lineas["reglas"], "577")
        self.assertEqual(lineas["llamadas al modelo"], "632")

    def test_without_an_env_block_it_uses_the_file_date_and_says_so(self):
        """An mtime is weaker evidence than a `recorded_at` and must not pass
        for one."""
        lineas = dict(describe(REPO / "results" / "llm_run.json"))
        self.assertIn("no lleva bloque _env", lineas["registrado"])

    def test_the_rung_2_record_is_described_in_full(self):
        lineas = dict(describe(REPO / "results2" / "llm_run2_n100.json"))
        self.assertEqual(lineas["casos"], "100")
        self.assertEqual(lineas["semilla"], "17")


# ---------------------------------------------------------------------------
# The guard on the number of rows
# ---------------------------------------------------------------------------

class TestShrinkRefusal(WithTempDir):
    """`compare_runs` and `note_audit` rewrite with whatever they are passed as
    an argument. The destination never changes, so the other check cannot see
    this one: what shrinks is the record."""

    def eight_rows(self) -> Path:
        return self.write("comparison.json", {
            "_env": {}, "rows": [{"file": f"llm_run2_{i}.json"} for i in range(8)]})

    def test_eight_rows_by_eight_pass(self):
        refuse_shrink(self.eight_rows(), [{}] * 8, overwrite=False)

    def test_more_rows_pass(self):
        refuse_shrink(self.eight_rows(), [{}] * 9, overwrite=False)

    def test_one_row_out_of_eight_aborts(self):
        with self.assertRaises(RecordExists) as e:
            refuse_shrink(self.eight_rows(), [{}], overwrite=False)
        self.assertIn("8", str(e.exception))
        self.assertIn("llm_run2_0.json", str(e.exception))

    def test_with_the_explicit_flag_it_shrinks(self):
        refuse_shrink(self.eight_rows(), [{}], overwrite=True)

    def test_with_no_previous_record_there_is_nothing_to_shrink(self):
        refuse_shrink(self.dir / "no_existe.json", [{}], overwrite=False)

    def test_the_old_bare_list_shape_does_not_blow_up(self):
        """Before Aug 7, 2026 these two records were a bare list. Nothing on
        disk is like that any more, but a guard that crashed on an old file
        would be worse than the loss it prevents."""
        p = self.write("viejo.json", [{"file": "a"}, {"file": "b"}])
        refuse_shrink(p, [{}], overwrite=False)


# ---------------------------------------------------------------------------
# The destinations of the commands
# ---------------------------------------------------------------------------

class TestTheOutputNameNoLongerCollides(unittest.TestCase):

    def path(self, **kw) -> Path:
        args = argparse.Namespace(n=2000, seed=17, out=None)
        vars(args).update(kw)
        return run_experiment.llm_out_path(args)

    def test_the_smoke_test_and_the_long_run_write_different_files(self):
        """The defect this whole change comes from."""
        self.assertNotEqual(self.path(n=100), self.path(n=2000))

    def test_the_n_goes_in_the_name(self):
        self.assertEqual(self.path(n=100).name, "llm_run_n100.json")
        self.assertEqual(self.path(n=2000).name, "llm_run_n2000.json")

    def test_the_seed_appears_only_when_it_is_not_the_pinned_one(self):
        self.assertEqual(self.path(n=100, seed=17).name, "llm_run_n100.json")
        self.assertEqual(self.path(n=100, seed=18).name,
                         "llm_run_n100_seed18.json")

    def test_no_default_invocation_points_at_the_published_record(self):
        """`results/llm_run.json` is the input of rungs 3 and 4. Since Aug 8,
        2026 it is no longer the destination of anything: reaching it takes
        `--out` AND the flag."""
        for n in (50, 100, 500, 2000):
            self.assertNotEqual(self.path(n=n).name, "llm_run.json")

    def test_out_overrides_everything_else(self):
        self.assertEqual(self.path(out="/tmp/x.json"), Path("/tmp/x.json"))


class TestTheRung2Label(unittest.TestCase):
    """The same defect on the other paid command, and worse: the rung 2 line
    the README recommends —`--n 100 --seed 17 --prompt-version v2`— wrote on
    top of the v1 record with that same name."""

    def test_reproduces_the_names_already_on_disk(self):
        for expected, (n, seed, v) in {
            "n100": (100, 17, "v1"),
            "n100_v2": (100, 17, "v2"),
            "n100_seed18": (100, 18, "v1"),
            "n100_v2_seed18": (100, 18, "v2"),
        }.items():
            with self.subTest(expected):
                self.assertEqual(run2.default_tag(n, seed, v), expected)

    def test_the_files_it_names_exist(self):
        """Not decoration: it is what makes the naming rule the same one the
        eight recorded runs already follow."""
        for tag in ("n100", "n100_v2", "n100_seed18", "n100_v2_seed18"):
            with self.subTest(tag):
                self.assertTrue(
                    (REPO / "results2" / f"llm_run2_{tag}.json").exists())

    def test_the_prompt_version_no_longer_collides(self):
        self.assertNotEqual(run2.default_tag(100, 17, "v1"),
                            run2.default_tag(100, 17, "v2"))


class TestAbortsBeforeSpending(WithTempDir):
    """The check runs at STARTUP. Aborting after 632 calls would be worse than
    not guarding at all, so what is measured here is that nobody was called."""

    def test_llm_aborts_without_building_the_proposer(self):
        (self.dir / "llm_run_n100.json").write_text(json.dumps(RECORD_PATH))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=None, overwrite_record=False)
        with mock.patch.object(run_experiment, "OUT", self.dir), \
                mock.patch.object(run_experiment, "run_shadow") as run, \
                mock.patch.object(run_experiment, "generate_corpus") as corpus, \
                self.assertRaises(SystemExit) as e:
            run_experiment.cmd_llm(args)
        run.assert_not_called()
        corpus.assert_not_called()
        self.assertIn("ABORTADO", str(e.exception))

    def test_llm_with_the_flag_does_not_abort(self):
        """The escape hatch has to work; otherwise the guard is a wall."""
        (self.dir / "llm_run_n100.json").write_text(json.dumps(RECORD_PATH))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=None, overwrite_record=True)
        with mock.patch.object(run_experiment, "OUT", self.dir), \
                mock.patch.object(run_experiment, "generate_corpus",
                                  side_effect=RuntimeError("paso la guarda")), \
                self.assertRaises(RuntimeError):
            run_experiment.cmd_llm(args)

    def test_run2_aborts_without_building_the_proposer(self):
        (self.dir / "llm_run2_n100.json").write_text(json.dumps(RECORD_PATH))
        argv = ["--n", "100"]
        with mock.patch.object(run2, "OUT", self.dir), \
                mock.patch.object(run2, "run_shadow2") as run, \
                mock.patch.object(run2, "OpenRouterProposer2") as prop, \
                mock.patch("sys.argv", ["run2", *argv]), \
                self.assertRaises(SystemExit) as e:
            run2.main()
        run.assert_not_called()
        prop.assert_not_called()
        self.assertIn("ABORTADO", str(e.exception))

    def test_the_llm_guard_looks_at_the_destination_not_the_flag(self):
        """`--out` onto an occupied file aborts just the same, otherwise it
        would be the way around the guard."""
        taken = self.dir / "otro.json"
        taken.write_text(json.dumps(RECORD_PATH))
        args = argparse.Namespace(n=100, seed=17, provider="openrouter",
                                  model=None, out=str(taken),
                                  overwrite_record=False)
        with mock.patch.object(run_experiment, "generate_corpus") as corpus, \
                self.assertRaises(SystemExit):
            run_experiment.cmd_llm(args)
        corpus.assert_not_called()


class TestShrinkingFromTheCommands(WithTempDir):

    def prepare(self, module):
        record = self.dir / "registro.json"
        record.write_text(json.dumps(
            {"_env": {}, "rows": [{"file": f"r{i}.json"} for i in range(8)]}))
        return mock.patch.object(module, "RECORD", record)

    def test_compare_runs_with_a_single_file_aborts(self):
        with self.prepare(compare_runs), \
                mock.patch.object(compare_runs, "analyse", return_value={}), \
                self.assertRaises(SystemExit) as e:
            compare_runs.main(["results2/llm_run2_n100.json"])
        self.assertIn("MAS PEQUENO", str(e.exception))

    def test_note_audit_with_a_single_file_aborts(self):
        with self.prepare(note_audit), \
                mock.patch.object(note_audit, "audit", return_value={}), \
                self.assertRaises(SystemExit) as e:
            note_audit.main(["results2/llm_run2_n100.json"])
        self.assertIn("MAS PEQUENO", str(e.exception))

    def test_aborts_before_printing_the_report(self):
        """Otherwise it prints a report suggesting everything went fine and
        then dies."""
        with self.prepare(compare_runs), \
                mock.patch.object(compare_runs, "analyse", return_value={}), \
                contextlib.redirect_stdout(io.StringIO()) as output, \
                self.assertRaises(SystemExit):
            compare_runs.main(["uno.json"])
        self.assertEqual(output.getvalue(), "")

    def test_the_flag_does_not_slip_in_as_a_filename(self):
        seen = []
        with self.prepare(compare_runs), \
                mock.patch.object(compare_runs, "analyse",
                                  side_effect=lambda p, s: seen.append(p) or ROW), \
                contextlib.redirect_stdout(io.StringIO()):
            compare_runs.main(["uno.json", FLAG])
        self.assertEqual(seen, [Path("uno.json")])


# ---------------------------------------------------------------------------
# What must NOT be guarded
# ---------------------------------------------------------------------------

class TestWhatIsLeftUnguarded(unittest.TestCase):
    """Three levels, and only one needs a guard.

    Re-running the deterministic, free records IS the reproducibility check:
    that only `recorded_at` moves is the signal that everything still holds. And
    `order_search`, `budget_and_balance` and `sweep` are pending a re-run with a
    serious optimizer — that work is planned and the guard must not obstruct it.

    **`FREE` was deleted on 2026-08-30.** It named six free writers of the
    forty the tree holds — finding F1 of `results3/FINDINGS_AUDIT.md` — and
    what it asserted is now asserted over every unguarded writer by
    `tests/test_writer_lists.py::TestOnlyWhatCostsMoneyIsGuarded`. What stays
    here is the one check a per-module derivation cannot make: `frontier` and
    `llm` are the same file with different answers.
    """

    def test_frontier_is_not_guarded(self):
        """`run_experiment.py frontier` shares a module with `llm`, so it is
        checked by behaviour and not by import: it costs nothing and rewrites
        its own record on purpose."""
        import inspect

        source = inspect.getsource(run_experiment.cmd_frontier)
        self.assertNotIn("refuse_overwrite", source)


class TestTheSuiteDoesNotWriteToResults(unittest.TestCase):
    """The suite rule, checked for this module in particular: everything above
    works in temporary directories."""

    RECORDS = ("results", "results2", "results3", "results4")

    def test_the_records_are_still_intact(self):
        for d in self.RECORDS:
            for f in sorted((REPO / d).glob("*.json")):
                with self.subTest(f.name):
                    # If any test above had written here, the mtime would have
                    # moved past the start of the process.
                    self.assertLess(f.stat().st_mtime, _START, f)


_START = __import__("time").time()


if __name__ == "__main__":
    unittest.main()
