"""
PLAN_MANUAL.md — the package that executes it.

WHAT IS PINNED HERE, AND WHY.
  * The constants of §11 and the lines of §0, so that moving one after a figure
    exists is visible in a diff. That the model and reasoning off are
    `PLAN_REUSE.md`'s, imported rather than retyped (rule A). That the lines
    are fractions, and every comparison with them exact.
  * The gate: it reads every signature line, and every writer of the package,
    the free ones too, exits on an unsigned plan before it measures, builds or
    writes anything. `manual/ask.py` and `manual/run.py` exit before they build
    a client.
  * The texts against §5's digests, the rules rebuilt from `HIDDEN_DSL` and
    parsed back, and the leak checks of `G-g2` with their teeth. Every prompt's
    digest, and every prompt as its level-0 prompt plus the manual's block.
  * The installer on the hidden policy, and its teeth: a reversed list, a rule
    the DSL refuses, an inversion by hand.
  * The instrument against `PLAN_REUSE.md`'s published figures.
  * The order of Stage B, drawn and rotated, and a run out of its turn refused.
  * The requests, through the SDK double: the compile client's settings, and
    the loop's proposer differing from v1's only in its system message.
  * Stage B end to end through the double, including resuming and stopping on
    an outage; Stage C's verdicts, thin labels and exactness by hand, and end
    to end over records the double wrote.

**No test here writes under `results*/` and none spends.** Every client is the
SDK double, or something that fails the test if it is ever built. Every record
a test writes lands in a temporary directory that `plan.OUT` is pointed at.
**No figure of the plan is computed**: the only answers ever scored are the
double's.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import generate_corpus
from reuse import plan as reuse_plan
from rung2.engine2 import PriorityEngine, Space
from rung2.proposers2 import SYSTEM_PROMPT_V1, OpenRouterProposer2
from rung2.shadow2 import run_shadow2

from blind import rows as brows
from manual import ask, gates, levels, plan, prompts, run, sample, score
from manual import compile as C
from manual import instrument as I
from tests.doubles import FixedResponses, OpenRouterShapedClient, fake_sdk, ticket_of

REPO = Path(__file__).resolve().parent.parent
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}
SIGNED = {"passes": True, "found": 1, "unsigned": 0, "what": "", "source": ""}
API_KEY = (200, {"data": {"is_management_key": False, "is_provisioning_key": False}})
F = Fraction

PROMPT_DIGESTS = {
    "loop": {
        0: "71fa68073837d5380158ddaa25554d9dfaa7a6317f7f26eb13e41be2cbe72f84",
        1: "fb72980e84c9aa16d62b4aa8f2a9921908ced394f8d883b40c3e92f3a9527c08",
        2: "76b6371c3130964350f6700faae200178d5c47a6a208389a0f9c97a8d6090b6b",
        3: "7b883f03a863d647e310d8975065451654584b4371961ab1a4b3562b81421dcd",
    },
    "compile": {
        0: "6b7281eb11c229c1b6e3c311e0e66b5de422db86834d508da5a62884517c0784",
        1: "fb6af1748467d1eb0eed66ef1e304da7e2dd70e62f02d32f3fea2fd729c3cdaa",
        2: "239493973ef5ae02e5c92cf638881e58b7f479ab9d2907ea715b7805ddbc71c0",
        3: "cfa58d8e03a028e249658ef17ab0f1ef8ecf2679540f95e7c830e15aadaface6",
    },
}


def fake_checks(passes: bool = True) -> gates.Checks:
    g = {"passes": passes}
    return gates.Checks(gg1=g, gg2=g, gg3=g, gg4=SIGNED)


class TempOut:
    """Points `plan.OUT` at a temporary directory for the block."""

    def __enter__(self) -> Path:
        self._d = tempfile.TemporaryDirectory()
        self._p = mock.patch.object(plan, "OUT", Path(self._d.name))
        self._p.start()
        return Path(self._d.name)

    def __exit__(self, *exc) -> None:
        self._p.stop()
        self._d.cleanup()


def hidden_json() -> str:
    return json.dumps({"rules": gates.hidden_answer(), "note": "la politica"})


# ---------------------------------------------------------------------------
# The constants
# ---------------------------------------------------------------------------

class TestTheConstantsAreTheDraftedOnes(unittest.TestCase):

    def test_the_client_is_plan_reuses(self):
        self.assertEqual(plan.MODEL, reuse_plan.MODEL)
        self.assertIs(plan.REASONING, reuse_plan.REASONING)
        self.assertEqual(plan.REASONING, {"effort": "none"})
        self.assertEqual((plan.TEMPERATURE, plan.PROMPT), (0, "v1"))
        self.assertEqual((plan.COMPILE_MAX_TOKENS, plan.COMPILE_MAX_RETRIES), (16000, 2))

    def test_the_loop_is_plan_reuses(self):
        self.assertEqual((plan.N, plan.SEED, plan.REPS, plan.SMOKE_N), (2000, 17, 3, 20))
        self.assertEqual((plan.N, plan.SEED, plan.REPS, plan.SMOKE_N),
                         (reuse_plan.N, reuse_plan.SEED, reuse_plan.REPS, reuse_plan.SMOKE_N))
        self.assertEqual(plan.LOOP_SMOKE_LEVEL, 3)

    def test_the_session_and_the_limits(self):
        self.assertEqual(plan.ASKS, 5)
        self.assertEqual(plan.LEVELS, (0, 1, 2, 3))
        self.assertEqual((plan.MIN_SIGNATURES, plan.MIN_VALID_ASKS, plan.MIN_RUNS,
                          plan.MAX_CONSECUTIVE_FAILURES), (1, 3, 2, 5))

    def test_the_seed_is_one_no_closed_thread_uses(self):
        self.assertEqual(plan.ORDER_SEED, 61)
        self.assertNotIn(plan.ORDER_SEED, {17, 18, 19, 20, 25, 41, 43, 47, 53, 59})
        self.assertLess(plan.ORDER_SEED, 1000)

    def test_the_lines_are_section_0s_as_fractions(self):
        lines = {"G_A_LINE": F(95, 100), "G_B_LINE": F(1, 10), "G_C_LINE": F(1, 2),
                 "G_D_LINE": F(1, 10), "G_E_LINE": F(1, 10), "G_F_LINE": F(1, 10)}
        for name, value in lines.items():
            with self.subTest(name):
                self.assertIsInstance(getattr(plan, name), Fraction)
                self.assertEqual(getattr(plan, name), value)

    def test_the_digests_are_the_files_and_section_5s(self):
        self.assertEqual(plan.DIGESTS, levels.digests())
        text = (REPO / "PLAN_MANUAL.md").read_text()
        for name, d in plan.DIGESTS.items():
            with self.subTest(name):
                self.assertIn(f"`{name}.txt` | `{d}`", text)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_MANUAL.md"))

    def test_where_the_records_land(self):
        self.assertEqual(plan.compile_path("session"), Path("results_manual/compile_session.json"))
        self.assertEqual(plan.loop_path(2, 3), Path("results_manual/loop_L2_r3.json"))
        self.assertEqual(plan.loop_smoke_path(), Path("results_manual/loop_smoke.json"))
        with self.assertRaises(ValueError):
            plan.loop_path(4, 1)
        with self.assertRaises(ValueError):
            plan.compile_path("pilot")


class TestTheGateCountsEverySignature(unittest.TestCase):

    def gate(self, text: str | None) -> dict:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            if text is not None:
                p.write_text(text)
            return plan.gate_signature(p)

    def test_no_plan_no_pass(self):
        self.assertFalse(self.gate(None)["passes"])

    def test_the_drafted_line_does_not_pass(self):
        self.assertFalse(self.gate(
            "**Signed by Sergi: ____________________ (date: __________)**\n")["passes"])

    def test_the_plan_as_drafted_does_not_pass(self):
        g = plan.gate_signature()
        if g["passes"]:
            self.skipTest("PLAN_MANUAL.md is signed")
        self.assertEqual((g["found"], g["unsigned"]), (1, 1))

    def test_one_signed_line_passes(self):
        self.assertTrue(self.gate(
            "**Signed by Sergi: Sergi Parpal (date: 2026-10-22)**\n")["passes"])

    def test_a_signed_table_does_not_cover_an_unsigned_amendment(self):
        g = self.gate("**Signed by Sergi: Sergi Parpal (date: 2026-10-22)**\n\n"
                      "**Signed by Sergi: ________ (date: ______)**\n")
        self.assertEqual((g["found"], g["unsigned"], g["passes"]), (2, 1, False))

    def test_refuse_unsigned_exits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PLAN.md"
            p.write_text("**Signed by Sergi: ______ (date: ______)**\n")
            with self.assertRaises(SystemExit):
                plan.refuse_unsigned("a test", p)


# ---------------------------------------------------------------------------
# The texts and the prompts
# ---------------------------------------------------------------------------

class TestTheTexts(unittest.TestCase):

    def test_the_levels_are_their_parts(self):
        self.assertIsNone(levels.text(0))
        cat, pro, rul = (levels.part(n).rstrip("\n") for n in levels.FILES)
        self.assertEqual(levels.text(1), cat)
        self.assertEqual(levels.text(2), cat + "\n\n" + pro)
        self.assertEqual(levels.text(3), rul)

    def test_g_g2_passes(self):
        g = gates.gate_gg2()
        self.assertTrue(g["passes"], g)

    def test_the_rules_are_rebuilt_and_parse_back(self):
        self.assertEqual(levels.part("rules"), gates.render_rules())
        parsed = gates.parse_rules(levels.part("rules"))
        self.assertEqual(parsed, [(r, [tuple(c) for c in cs], a) for r, cs, a in HIDDEN_DSL])

    def test_the_catalogue_check_has_teeth(self):
        cat = levels.part("catalogue")
        self.assertTrue(gates.catalogue_check(cat)["passes"])
        for leak in ("\nnota: severity", "\nnota: 3 tickets", "\nnota: clientes enterprise"):
            with self.subTest(leak):
                self.assertFalse(gates.catalogue_check(cat + leak)["passes"])
        lines = cat.splitlines()
        swapped = "\n".join(lines[:2] + [lines[3], lines[2]] + lines[4:])
        self.assertFalse(gates.catalogue_check(swapped)["queues_in_order"])

    def test_the_prose_check_has_teeth(self):
        pro = levels.part("prose")
        self.assertTrue(gates.prose_check(pro)["passes"])
        for leak in (" T2_TECHNICAL", " H16", " prior_tickets_30d", " gte 3"):
            with self.subTest(leak):
                self.assertFalse(gates.prose_check(pro + leak)["passes"])

    def test_a_changed_text_fails_g_g2(self):
        real = levels.part

        def changed(name):
            t = real(name)
            return t.replace("bastantes", "cinco o mas") if name == "prose" else t

        with mock.patch.object(levels, "part", side_effect=changed), \
             mock.patch.object(levels, "digest",
                               side_effect=lambda n: "0" * 64 if n == "prose"
                               else plan.DIGESTS[n]):
            self.assertFalse(gates.gate_gg2()["passes"])


class TestThePrompts(unittest.TestCase):

    def test_every_digest_is_pinned(self):
        self.assertEqual(prompts.prompt_digests(), PROMPT_DIGESTS)

    def test_level_0_is_v1_and_plan_reuses(self):
        rec = json.loads(reuse_plan.run_path(1).read_text())
        self.assertEqual(prompts.loop_system_prompt(0), SYSTEM_PROMPT_V1)
        self.assertEqual(prompts.loop_system_prompt(0), rec["system_prompt"])

    def test_every_other_prompt_is_level_0_plus_the_block(self):
        for lv in (1, 2, 3):
            piece = "\n\n" + prompts.block(lv)
            with self.subTest(lv):
                self.assertEqual(prompts.loop_system_prompt(lv).replace(piece, "", 1),
                                 SYSTEM_PROMPT_V1)
                self.assertEqual(prompts.compile_system_prompt(lv).replace(piece, "", 1),
                                 prompts.compile_system_prompt(0))

    def test_the_block_sits_just_before_the_operators(self):
        for lv in (1, 2, 3):
            for p in (prompts.loop_system_prompt(lv), prompts.compile_system_prompt(lv)):
                with self.subTest(lv):
                    end = p.index(prompts.block(lv)) + len(prompts.block(lv))
                    self.assertTrue(p[end:].startswith(prompts.ANCHOR))
                    self.assertLess(p.index("ACCIONES POSIBLES:"), p.index(prompts.block(lv)))

    def test_the_anchor_appears_once(self):
        self.assertEqual(SYSTEM_PROMPT_V1.count(prompts.ANCHOR), 1)
        self.assertEqual(prompts.COMPILE_PROMPT.count(prompts.ANCHOR), 1)
        with self.assertRaises(ValueError):
            prompts.insert("sin ancla", 1)

    def test_the_compile_question_reuses_v1s_blocks(self):
        for piece in ("ATRIBUTOS DISPONIBLES Y SUS DOMINIOS:", "severity: 1 = critica, 4 = baja.",
                      "ACCIONES POSIBLES:", "  - lte y gte SOLO sobre severity y prior_tickets_30d",
                      "  - in requiere una lista de valores del dominio",
                      "Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:"):
            with self.subTest(piece):
                self.assertIn(piece, SYSTEM_PROMPT_V1)
                self.assertIn(piece, prompts.COMPILE_PROMPT)

    def test_the_messages(self):
        m = prompts.compile_messages(2)
        self.assertEqual([x["role"] for x in m], ["system", "user"])
        self.assertEqual(m[1]["content"], prompts.COMPILE_USER)


# ---------------------------------------------------------------------------
# The installer
# ---------------------------------------------------------------------------

class TestTheInstaller(unittest.TestCase):

    def test_the_hidden_policy_gives_back_its_199_edges(self):
        r = gates.installer_on_the_policy()
        self.assertTrue(r["passes"], r)
        self.assertEqual(r["edges"], 199)

    def test_a_reversed_list_falls_and_says_why(self):
        rev = C.install(list(reversed(gates.hidden_answer())), I.space())
        self.assertGreater(sum(1 for e in rev.engine.edge_log if e[2] != "ok"), 0)
        self.assertGreater(len(C.inversions(rev)), 0)
        self.assertLess(I.over_space(rev.engine)["e2e"], 1)

    def test_a_rule_the_dsl_refuses_is_rejected_and_counted(self):
        r = gates.compile_path_check()
        self.assertTrue(r["passes"], r)
        inst = C.install([{"conditions": [], "action": "T1_GENERAL"},
                          {"conditions": [{"attr": "severity", "op": "eq", "value": 1}],
                           "action": "T2_TECHNICAL"}], I.space())
        self.assertEqual(inst.positions, [1])
        self.assertEqual(inst.rejected[0]["position"], 0)
        self.assertEqual(inst.summary()["rules_rejected"], 1)

    def test_what_makes_an_ask_invalid(self):
        self.assertIsNone(C.rules_of({"rules": [{}]})[1])
        for bad in ("texto", None, {"note": "x"}, {"rules": []}, {"rules": "H01"}):
            with self.subTest(bad):
                self.assertIsNotNone(C.rules_of(bad)[1])

    def test_an_inversion_by_hand(self):
        """A default listed above the exception it contains: rung 2's engine lets
        the exception win, and first match would not."""
        ans = [{"conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                "action": "T1_GENERAL"},
               {"conditions": [{"attr": "has_security_keyword", "op": "eq", "value": True}],
                "action": "SECURITY_INCIDENT"}]
        inst = C.install(ans, I.space())
        self.assertEqual(len(C.inversions(inst)), 1)
        engine_reading = I.over_space(inst.engine)
        first_match = I.first_match_over_space(inst.rules)
        truth = I.space_truth()
        self.assertEqual(engine_reading["recall"]["SECURITY_INCIDENT"]["right"],
                         truth["SECURITY_INCIDENT"].bit_count())
        self.assertEqual(first_match["correct"], truth["T1_GENERAL"].bit_count())


# ---------------------------------------------------------------------------
# The instrument
# ---------------------------------------------------------------------------

class TestTheInstrument(unittest.TestCase):

    def test_plan_reuse_comes_back(self):
        r = gates.reuse_through_the_instrument()
        self.assertTrue(r["passes"], r)

    def test_k_a_exact_is_k_a(self):
        for rec in I.reuse_records():
            with self.subTest(rec.get("rep")):
                self.assertEqual(float(I.k_a_exact(rec["rules"])), I.partition(rec["rules"]))
        hid = C.install(gates.hidden_answer(), I.space())
        self.assertEqual(I.k_a_exact([r.as_dict() for r in hid.rules]), F(1, 13))

    def test_k_a_reads_a_base_without_a_rule_beyond_the_keyword_as_one(self):
        kw = C.install(gates.hidden_answer()[:3], I.space())
        self.assertEqual(I.k_a_exact([r.as_dict() for r in kw.rules]), F(1))

    def test_macro_recall_by_hand(self):
        scored = {"recall": {"ACCOUNT_MANAGER": {"right": 1, "of": 4},
                             "T3_ENGINEERING": {"right": 1, "of": 2}}}
        self.assertEqual(I.macro_recall(scored), F(3, 8))

    def test_the_regions_partition_both_surfaces(self):
        regions = I.hidden_regions()
        union = 0
        for reg in regions.values():
            self.assertEqual(union & reg["mask"], 0)
            union |= reg["mask"]
        self.assertEqual(union.bit_count(), I.space().n)
        self.assertEqual(sum(len(r["cases"]) for r in regions.values()), plan.N)
        self.assertEqual([k for k, r in regions.items() if not r["mask"]],
                         ["H21", "H25", "H27"])

    def test_the_hidden_policy_is_right_on_every_region(self):
        hid = C.install(gates.hidden_answer(), I.space())
        for rid, row in I.by_region(hid.engine).items():
            with self.subTest(rid):
                self.assertEqual(row["space"][0], row["space"][1])
                self.assertEqual(row["corpus"][0], row["corpus"][1])
        self.assertEqual(len(I.reproduces(hid.engine)), 29)


# ---------------------------------------------------------------------------
# The order of Stage B
# ---------------------------------------------------------------------------

class TestTheOrder(unittest.TestCase):

    def test_the_drawn_orders_are_pinned(self):
        self.assertEqual(plan.base_order("compile"), [1, 0, 2, 3])
        self.assertEqual(plan.base_order("loop"), [0, 1, 3, 2])

    def test_the_schedules(self):
        self.assertTrue(gates.schedule_check()["passes"])
        loop = plan.loop_schedule()
        self.assertEqual(len(loop), 12)
        for lv in plan.LEVELS:
            places = [[l for r_, l in loop if r_ == r].index(lv) for r in (1, 2, 3)]
            with self.subTest(lv):
                self.assertEqual(len(set(places)), 3)
                self.assertLessEqual(places.count(0), 1)
                self.assertLessEqual(places.count(3), 1)
        session = plan.compile_schedule("session")
        self.assertEqual(len(session), plan.ASKS * 4)
        self.assertEqual(plan.compile_schedule("smoke"), [(1, lv) for lv in plan.base_order("compile")])

    def test_the_orders_do_not_depend_on_pythonhashseed(self):
        code = "from manual import plan; print(plan.compile_schedule('session'), plan.loop_schedule())"
        outs = set()
        for seed in ("0", "1", "2"):
            p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                               cwd=REPO, env={**os.environ, "PYTHONHASHSEED": seed})
            outs.add(p.stdout)
        self.assertEqual(len(outs), 1)


class TestARunWaitsForItsTurn(unittest.TestCase):

    def test_no_compile_session_no_run(self):
        with TempOut():
            ok, why = run.turn_check(*plan.loop_schedule()[0][::-1])
            self.assertFalse(ok)
            self.assertIn("compile session", why)

    def test_a_run_out_of_its_turn_is_refused(self):
        with TempOut() as d:
            (d / "compile_session.json").write_text("{}")
            (r1, l1), (r2, l2) = plan.loop_schedule()[:2]
            self.assertFalse(run.turn_check(l2, r2)[0])
            self.assertTrue(run.turn_check(l1, r1)[0])
            self.assertEqual(run.next_run(), (l1, r1))
            plan.loop_path(l1, r1).write_text("{}")
            self.assertTrue(run.turn_check(l2, r2)[0])
            self.assertEqual(run.next_run(), (l2, r2))

    def test_the_loop_smoke_check(self):
        good = {**run.protocol(plan.LOOP_SMOKE_LEVEL, plan.SMOKE_N),
                "metrics": {"escalations": 5, "failed_proposals": 1, "n_rules": 4}}
        with TempOut():
            self.assertFalse(run.smoke_check()[0])
            for rec, ok in ((good, True), ({**good, "level": 0}, False),
                            ({**good, "metrics": {"escalations": 2, "failed_proposals": 2,
                                                  "n_rules": 0}}, False),
                            ({**good, "metrics": {"escalations": 2, "failed_proposals": 0,
                                                  "n_rules": 0}}, False)):
                plan.loop_smoke_path().parent.mkdir(parents=True, exist_ok=True)
                plan.loop_smoke_path().write_text(json.dumps(rec))
                with self.subTest(rec.get("level"), metrics=rec["metrics"]):
                    self.assertEqual(run.smoke_check()[0], ok)

    def test_the_compile_smoke_check(self):
        with TempOut():
            self.assertFalse(ask.smoke_check()[0])
            p = plan.compile_path("smoke")
            p.parent.mkdir(parents=True, exist_ok=True)
            for rows, over, ok in (([{"valid": True}], {}, True),
                                   ([{"valid": False}], {}, False),
                                   ([{"valid": True}], {"max_tokens": 1200}, False)):
                p.write_text(json.dumps({**ask.protocol(), **over, "rows": rows}))
                with self.subTest(rows=rows, over=over):
                    self.assertEqual(ask.smoke_check()[0], ok)


# ---------------------------------------------------------------------------
# Nothing is built or written unsigned
# ---------------------------------------------------------------------------

class TestNothingIsBuiltOrWrittenUnsigned(unittest.TestCase):

    def refuses(self, main, argv: list[str]) -> None:
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(ask, "Compiler",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(run, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write:
            with self.assertRaises(SystemExit):
                main(argv)
        checks.assert_not_called()
        client.assert_not_called()
        proposer.assert_not_called()
        write.assert_not_called()

    def test_stage_b_refuses_before_anything(self):
        for s in plan.COMPILE_SESSIONS:
            with self.subTest(s):
                self.refuses(ask.main, ["--session", s])
        self.refuses(run.main, ["--smoke"])
        self.refuses(run.main, ["--level", "0", "--rep", "1"])

    def test_the_free_writers_refuse_too(self):
        self.refuses(sample.main, [])
        self.refuses(score.main, [])

    def test_the_dry_runs_build_no_client_need_no_key_and_write_nothing(self):
        with mock.patch.dict(os.environ), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(ask, "Compiler",
                               side_effect=AssertionError("client built")) as client, \
             mock.patch.object(run, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer, \
             mock.patch.object(Path, "write_text",
                               side_effect=AssertionError("wrote")) as write, \
             mock.patch("builtins.print"):
            os.environ.pop("OPENROUTER_API_KEY", None)
            for main in (ask.main, run.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 0)
        fetch.assert_not_called()
        client.assert_not_called()
        proposer.assert_not_called()
        write.assert_not_called()

    def test_a_failed_check_fails_the_dry_run(self):
        with mock.patch.object(gates, "run_checks", return_value=fake_checks(False)), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            for main in (ask.main, run.main, sample.main, score.main):
                with self.subTest(main.__module__):
                    self.assertEqual(main(["--dry-run"]), 1)

    def test_a_run_refuses_before_the_key_the_checks_or_the_proposer(self):
        with TempOut(), \
             mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch("reuse.run.fetch_key_info",
                        side_effect=AssertionError("asked")) as fetch, \
             mock.patch.object(gates, "run_checks",
                               side_effect=AssertionError("checks ran")) as checks, \
             mock.patch.object(run, "build_proposer",
                               side_effect=AssertionError("proposer built")) as proposer:
            with self.assertRaises(SystemExit):
                run.main(["--level", "0", "--rep", "1"])
        fetch.assert_not_called()
        checks.assert_not_called()
        proposer.assert_not_called()


# ---------------------------------------------------------------------------
# The requests, through the SDK double
# ---------------------------------------------------------------------------

class TestTheRequests(unittest.TestCase):

    def test_the_compile_client_sends_section_11s_settings(self):
        client = OpenRouterShapedClient(FixedResponses(hidden_json()))
        with fake_sdk(openai=client):
            comp = ask.Compiler()
            payload, texts = comp.ask(2)
        req = client.peticiones[0]
        self.assertEqual(req["model"], plan.MODEL)
        self.assertEqual(req["temperature"], 0)
        self.assertEqual(req["max_tokens"], 16000)
        self.assertEqual(req["extra_body"], {"reasoning": {"effort": "none"}})
        self.assertEqual(req["response_format"], {"type": "json_object"})
        self.assertEqual(req["messages"], prompts.compile_messages(2))
        self.assertEqual(len(payload["rules"]), 29)
        self.assertEqual(texts, [hidden_json()])

    def test_a_retry_drops_the_json_mode_and_says_rung_2s_words(self):
        client = OpenRouterShapedClient(FixedResponses("no es json", hidden_json()))
        with fake_sdk(openai=client):
            comp = ask.Compiler()
            payload, texts = comp.ask(3)
        self.assertEqual(len(client.peticiones), 2)
        self.assertNotIn("response_format", client.peticiones[1])
        self.assertEqual(client.peticiones[1]["messages"][-1]["content"], prompts.RETRY_MSG)
        self.assertEqual(texts, ["no es json", hidden_json()])
        attempts = comp.calls.take()
        self.assertEqual([a["provider"] for a in attempts],
                         [OpenRouterShapedClient.PROVIDER] * 2)

    def test_the_loop_proposer_differs_from_v1s_only_in_the_system_message(self):
        case = generate_corpus(1, seed=17)[0]
        answer = json.dumps({"action": "T1_GENERAL", "conditions": [
            {"attr": "severity", "op": "eq", "value": case.severity}], "note": "x"})
        for lv in plan.LEVELS:
            mine, plain_ = (OpenRouterShapedClient(FixedResponses(answer)) for _ in range(2))
            with fake_sdk(openai=mine):
                p = run.build_proposer(lv)
                p.propose(case, "BASE DE REGLAS: vacia. Esta es la primera regla.\n")
            with fake_sdk(openai=plain_):
                q = OpenRouterProposer2(model=plan.MODEL, prompt_version="v1",
                                        reasoning=plan.REASONING)
                q.propose(case, "BASE DE REGLAS: vacia. Esta es la primera regla.\n")
            a, b = mine.peticiones[0], plain_.peticiones[0]
            with self.subTest(lv):
                self.assertEqual(a["messages"][0]["content"], prompts.loop_system_prompt(lv))
                self.assertEqual(a["messages"][1:], b["messages"][1:])
                self.assertEqual({k: v for k, v in a.items() if k != "messages"},
                                 {k: v for k, v in b.items() if k != "messages"})
                if lv == 0:
                    self.assertEqual(a, b)


# ---------------------------------------------------------------------------
# Stage B end to end, through the double
# ---------------------------------------------------------------------------

def compile_script(kwargs: dict) -> str:
    system = kwargs["messages"][0]["content"]
    if "H01: SI" in system:
        return hidden_json()
    if "QUE HACE CADA COLA" in system:
        return json.dumps({"rules": [
            {"conditions": [{"attr": "customer_tier", "op": "eq", "value": "enterprise"}],
             "action": "ACCOUNT_MANAGER"},
            {"conditions": [{"attr": "severity", "op": "gte", "value": 1}],
             "action": "T1_GENERAL"}]})
    return json.dumps({"rules": [{"conditions": [{"attr": "severity", "op": "gte", "value": 1}],
                                  "action": "T2_TECHNICAL"}]})


def loop_script(kwargs: dict) -> str:
    t = ticket_of(kwargs)
    return json.dumps({"action": "T2_TECHNICAL", "beats": [], "loses_to": [], "note": "x",
                       "conditions": [{"attr": "product", "op": "eq", "value": t["product"]},
                                      {"attr": "severity", "op": "eq", "value": t["severity"]}]})


def header(session: str) -> dict:
    return {"protocol": ask.protocol(), "session": session, "sample_sha256": "x"}


class TestStageBEndToEnd(unittest.TestCase):

    def test_the_compile_session_through_the_double(self):
        client = OpenRouterShapedClient(compile_script)
        with TempOut(), fake_sdk(openai=client), mock.patch("builtins.print"):
            rows, resumed = ask.ask("session", ask.Compiler(),
                                    plan.compile_partial("session"), header("session"))
        self.assertEqual(resumed, [])
        self.assertEqual([(r["pass"], r["level"]) for r in rows], plan.compile_schedule("session"))
        self.assertTrue(all(r["valid"] and r["call_attempts"] for r in rows))
        self.assertEqual({r["level"]: r["rules_in_answer"] for r in rows}[3], 29)

    def test_a_session_stops_on_an_outage_and_resumes_where_it_stopped(self):
        calls = {"n": 0}

        def flaky(kwargs):
            calls["n"] += 1
            if 6 <= calls["n"]:
                raise ConnectionError("network down")
            return compile_script(kwargs)

        with TempOut(), mock.patch("builtins.print"):
            with fake_sdk(openai=OpenRouterShapedClient(flaky)):
                with self.assertRaises(ask.Outage):
                    ask.ask("session", ask.Compiler(), plan.compile_partial("session"),
                            header("session"))
            kept = plan.compile_partial("session").read_text().splitlines()
            self.assertEqual(len(kept), 1 + 5)          # the header and five answers
            with fake_sdk(openai=OpenRouterShapedClient(compile_script)):
                rows, resumed = ask.ask("session", ask.Compiler(),
                                        plan.compile_partial("session"), header("session"))
        self.assertEqual(len(resumed), 1)
        self.assertEqual(sorted((r["pass"], r["level"]) for r in rows),
                         sorted(plan.compile_schedule("session")))

    def test_the_loop_sends_the_levels_prompt_on_every_call(self):
        for lv in (0, 3):
            client = OpenRouterShapedClient(loop_script)
            with fake_sdk(openai=client):
                res = run_shadow2(generate_corpus(30, seed=17), PriorityEngine(space=Space()),
                                  run.build_proposer(lv))
            with self.subTest(lv):
                self.assertGreater(len(client.peticiones), 0)
                self.assertTrue(all(r["messages"][0]["content"] == prompts.loop_system_prompt(lv)
                                    for r in client.peticiones))
                self.assertEqual(len(res.calls), res.metrics["escalations"])


# ---------------------------------------------------------------------------
# Stage C
# ---------------------------------------------------------------------------

class TestStageCArithmetic(unittest.TestCase):

    def test_single(self):
        r = score.single([F(96, 100)] * 5, plan.G_A_LINE, 3)
        self.assertEqual((r["verdict"], r["thin"]), ("holds", False))
        r = score.single([F(96, 100)] * 4 + [F(94, 100)], plan.G_A_LINE, 3)
        self.assertEqual((r["verdict"], r["thin"]), ("holds", True))
        r = score.single([F(94, 100)] * 3 + [F(99, 100)] * 2, plan.G_A_LINE, 3)
        self.assertEqual((r["verdict"], r["thin"]), ("refuted", True))
        self.assertEqual(score.single([F(1)] * 2, plan.G_A_LINE, 3)["verdict"], "unadjudicable")

    def test_g_cs_line_is_held_above(self):
        self.assertEqual(score.single([F(1, 2)] * 3, plan.G_C_LINE, 2, above=True)["verdict"],
                         "refuted")
        self.assertEqual(score.single([F(51, 100)] * 3, plan.G_C_LINE, 2, above=True)["verdict"],
                         "holds")

    def test_a_difference_is_exact(self):
        """0.6 - 0.5 is below 0.1 in floating point, and at it in fractions."""
        self.assertLess(0.6 - 0.5, 0.1)
        r = score.difference([F(6, 10)] * 3, [F(5, 10)] * 3, plan.G_E_LINE, 3, 3)
        self.assertEqual((r["verdict"], r["statistic"], r["thin"]), ("holds", F(1, 10), False))

    def test_a_difference_is_thin_when_one_value_crosses(self):
        r = score.difference([F(70, 100), F(60, 100), F(55, 100)], [F(1, 2)] * 3,
                             plan.G_E_LINE, 2, 2)
        self.assertEqual((r["verdict"], r["thin"]), ("holds", True))
        self.assertEqual(score.difference([F(1)] * 2, [F(1)] * 3, plan.G_D_LINE, 3, 2)["verdict"],
                         "unadjudicable")

    def test_the_pooled_difference(self):
        def runs(*pairs):
            return [{"prop": {"right": a, "escalations": b}} for a, b in pairs]
        r = score.pooled_difference(runs((60, 100), (60, 100), (60, 100)),
                                    runs((50, 100), (50, 100), (50, 100)), plan.G_F_LINE)
        self.assertEqual((r["verdict"], r["statistic"], r["thin"]), ("holds", F(1, 10), False))
        r = score.pooled_difference(runs((90, 100), (55, 100), (55, 100)),
                                    runs((50, 100), (50, 100), (50, 100)), plan.G_F_LINE)
        self.assertEqual((r["verdict"], r["thin"]), ("holds", True))
        self.assertEqual(score.pooled_difference(runs((1, 2)), runs((1, 2), (1, 2)),
                                                 plan.G_F_LINE)["verdict"], "unadjudicable")

    def test_plain_renders_fractions(self):
        self.assertEqual(score.plain({1: [F(1, 3)]}),
                         {"1": [{"fraction": "1/3", "value": 1 / 3}]})

    def test_first_full_cover(self):
        rules = [{"rule_id": "R0001", "born_at": 3, "action": "T2_TECHNICAL",
                  "conditions": [{"attr": "severity", "op": "eq", "value": 1}]},
                 {"rule_id": "R0002", "born_at": 9, "action": "T1_GENERAL",
                  "conditions": [{"attr": "severity", "op": "gte", "value": 1}]}]
        self.assertEqual(score.first_full_cover({"rules": rules}), 9)
        self.assertIsNone(score.first_full_cover({"rules": rules[:1]}))


class TestStageCEndToEnd(unittest.TestCase):
    """Records written by the double, scored by Stage C, in a temporary
    directory. The verdicts are the double's and mean nothing about the model."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = TempOut()
        cls.out = cls.tmp.__enter__()
        try:
            with fake_sdk(openai=OpenRouterShapedClient(compile_script)), \
                 mock.patch("builtins.print"):
                rows, _ = ask.ask("session", ask.Compiler(), plan.compile_partial("session"),
                                  header("session"))
            plan.compile_path("session").write_text(json.dumps({"rows": rows}))
            for rep, lv in plan.loop_schedule():
                engine = PriorityEngine(space=Space())
                with fake_sdk(openai=OpenRouterShapedClient(loop_script)):
                    res = run_shadow2(generate_corpus(60, seed=17), engine,
                                      run.build_proposer(lv))
                plan.loop_path(lv, rep).write_text(json.dumps({
                    "_env": {"recorded_at": "t"}, "level": lv, "rep": rep, "started_at": "t",
                    "metrics": res.metrics, "rules": [r.as_dict() for r in res.rules],
                    "edge_log": engine.edge_log, "records": [vars(r) for r in res.records],
                    "calls": res.calls}, default=str))
        except BaseException:
            cls.tmp.__exit__(None, None, None)
            raise

    @classmethod
    def tearDownClass(cls):
        cls.tmp.__exit__(None, None, None)

    def test_the_six_rows_come_out(self):
        asks, runs, missing = score.load()
        v = score.verdicts(asks, runs)
        self.assertEqual(missing, [])
        self.assertEqual(set(v), {"G-a", "G-b", "G-c", "G-d", "G-e", "G-f"})
        self.assertEqual((v["G-a"]["verdict"], v["G-a"]["statistic"]), ("holds", F(1)))
        self.assertEqual(v["G-b"]["verdict"], "holds")       # the double's level 1 names AM
        self.assertEqual(v["G-d"]["verdict"], "holds")       # the double's loop writes narrow rules
        self.assertEqual([len(runs[lv]) for lv in plan.LEVELS], [3, 3, 3, 3])

    def test_the_writer_writes_where_plan_out_points(self):
        with mock.patch.object(plan, "gate_signature", return_value=SIGNED), \
             mock.patch.object(gates, "run_checks", return_value=fake_checks()), \
             mock.patch.object(gates, "report"), mock.patch("builtins.print"):
            self.assertEqual(score.main([]), 0)
        rec = json.loads(plan.score_path().read_text())
        self.assertTrue(str(plan.score_path()).startswith(str(self.out)))
        self.assertEqual(rec["verdicts"]["G-a"]["statistic"], {"fraction": "1/1", "value": 1.0})
        self.assertIn("drift", rec["G-g"])


if __name__ == "__main__":
    unittest.main()
