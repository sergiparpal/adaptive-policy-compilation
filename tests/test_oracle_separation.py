"""
ORACLE SEPARATION, checked over the imports.

`hidden_policy.py` declares itself thus: "this module is the ORACLE. It exists
to label the corpus and to measure offline. It must NEVER be consulted by the
rule engine, by the proposer or by any component of the online loop".

It is the claim on which the figures meaning anything depends, and until now it
lived only in a docstring. These tests make it mechanical: they read each
module's AST and look at who imports what. An import is enough to fail —it does
not need to be used— because an unused import is exactly what was in
`rung4/sweep.py` until August 6, 2026, contradicting in writing what
`FINDINGS4.md` claimed.

The same control covers the other end: in rung 4, `feedback.py` must remain the
ONLY module that touches the oracle. If it stops being so, "learning from
feedback" becomes full supervision under another name and the rung does not
measure what it says it measures.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ORACLE = {"hidden_policy", "true_action", "true_rule_id"}

# Components of the online loop: they see the case, decide and propose. None of
# them may consult the true policy.
ONLINE_LOOP = [
    "harness/dsl.py",
    "harness/domain.py",
    "harness/proposers.py",
    "rung2/engine2.py",
    "rung2/proposers2.py",
    "rung2/hidden_priority.py",
    # Added 2026-08-24 with stage C of PLAN_PAIRWISE.md. It puts a ticket and
    # two rules in front of a model and asks which queue the ticket goes to, so
    # it is a proposer path and belongs on this side of the line. It SCORES the
    # answers too, and the key for that is a lookup into
    # results2/pair_benchmark.json — which carries it openly — never the oracle.
    # If that ever changes route, this is what says so.
    "rung2/pair_judgement.py",
    # Added 2026-09-29 with PLAN_REUSE.md. It builds rung 2's proposer and runs
    # its loop, so it is a proposer path. The loop it calls labels the record,
    # as it always has; the module itself reads the oracle through nothing.
    "reuse/run.py",
    # Added 2026-10-02 with PLAN_FIDELITY.md. `prompts.py` builds rung 2's
    # proposer requests on a rebuilt base, and `ask.py` sends them, so both are
    # proposer paths. The labels they carry into a record are copied from
    # PLAN_REUSE.md's records, never computed.
    "fidelity/prompts.py",
    "fidelity/ask.py",
    # Added 2026-10-05 with PLAN_AUTHORSHIP.md. `protocol.py` builds v1e's
    # requests, `loop.py` runs rung 2's loop with v1e's proposal path, and
    # `run.py` sends the requests, so all three are proposer paths. The loop is
    # handed its labels, read off PLAN_REUSE.md's records; it computes none.
    "authorship/protocol.py",
    "authorship/loop.py",
    "authorship/run.py",
    # Added 2026-10-06 with PLAN_OVERLAP.md, for the same reasons: `protocol.py`
    # builds v2e's requests, `loop.py` runs rung 2's loop with v2e's proposal
    # path, and `run.py` sends the requests. The loop is handed its labels, read
    # off PLAN_REUSE.md's records; it computes none.
    "overlap/protocol.py",
    "overlap/loop.py",
    "overlap/run.py",
    # Added 2026-10-10 with PLAN_BLIND.md, for the same reasons: `protocol.py`
    # builds v2b's requests, `loop.py` runs rung 2's loop with v2b's proposal
    # path, and `run.py` sends the requests. The loop is handed its labels, read
    # off PLAN_REUSE.md's records; it computes none.
    "blind/protocol.py",
    "blind/loop.py",
    "blind/run.py",
    # Added 2026-10-14 with PLAN_SCREEN.md. `ask.py` sends rung 2's proposer
    # requests, built by `fidelity/prompts.py`, which is watched above. The
    # labels it carries into a record are copied from PLAN_REUSE.md's records,
    # never computed.
    "screen/ask.py",
    # Added 2026-10-17 with PLAN_RANKING.md. `ask.py` puts one question in
    # front of the model, the eight queue names and nothing else, so it is a
    # proposer path. `question.py` builds that question from
    # `harness.domain.ACTIONS` alone, and its M-g2 checks the built string. The
    # scores are computed by `instrument.py` with rung 3's instance builders,
    # which label the cells as every rung 3 figure has been labelled; no module
    # of the package imports the oracle itself.
    "ranking/question.py",
    "ranking/ask.py",
    # Added 2026-10-21 with PLAN_MANUAL.md, and the one package that breaks the
    # separation ON PURPOSE (§4, rule B of the plan). It hands the model the
    # policy, at three levels, as text: three files under `manual/texts/`,
    # frozen before the signature and pinned by digest. That text is the ONLY
    # route by which the policy reaches the proposer. These five modules build
    # and send its requests, so they import neither the oracle nor any name that
    # carries the policy in code — `TestTheAuthorityChannel` below adds those
    # names to their forbidden imports. The checks they run before spending
    # (`manual/gates.py`) rebuild level 3 from `HIDDEN_DSL` offline, and send
    # nothing; the scores are `manual/instrument.py`'s, which labels as rung 3
    # does. No module of the package imports the oracle itself.
    "manual/levels.py",
    "manual/prompts.py",
    "manual/compile.py",
    "manual/ask.py",
    "manual/run.py",
    # Added 2026-10-23 with PLAN_APPLY.md, which asks `PLAN_MANUAL.md`'s
    # escalations again with the same frozen texts in the system prompt (§4,
    # rule B of the plan). These two modules build and send its requests: the
    # system prompt is `manual.prompts.loop_system_prompt`, called, and the
    # user message is rung 2's around a screen `fidelity` rebuilds. They are on
    # the same channel, so `TestTheAuthorityChannel` watches them too. The
    # labels enter only at scoring, from the loop records (`apply/score.py`).
    "apply/prompts.py",
    "apply/ask.py",
    # Added 2026-10-24 with PLAN_QUEUE_ALONE.md, which asks PLAN_APPLY.md's
    # tickets again with the same frozen texts in the system prompt (§4, rule B
    # of the plan). These two modules build and send its requests: the rule
    # arm's prompts are `apply.prompts`', called, and the impasse and plain
    # arms' system prompts carry the manual's block through
    # `manual.prompts.block`. They are on the same channel, so
    # `TestTheAuthorityChannel` watches them too. The labels enter only at
    # scoring (`queue_alone/score.py`), and §5.6's classes read the 29 rules
    # from level 3's frozen text (`queue_alone/rules.py`), never the oracle.
    "queue_alone/prompts.py",
    "queue_alone/ask.py",
    # Added 2026-10-25 with PLAN_FIRST_MATCH.md, which asks PLAN_QUEUE_ALONE.md's
    # level-3 tickets again with the same frozen texts in the system prompt (§4,
    # rule B of the plan). These two modules build and send its requests: every
    # arm's system prompt is `queue_alone.prompts`' plain arm's, called, which
    # carries the manual's block through `manual.prompts.block`. They are on the
    # same channel, so `TestTheAuthorityChannel` watches them too. The labels
    # enter only at scoring (`first_match/score.py`), and the rules a ticket
    # matches are read from level 3's frozen text (`queue_alone/rules.py`),
    # never the oracle.
    "first_match/prompts.py",
    "first_match/ask.py",
    # Added 2026-10-25 with PLAN_REASONED_RULE.md, which asks PLAN_QUEUE_ALONE.md's
    # level-3 rule and plain prompts again, with and without reasoning, and the
    # same frozen texts in every system prompt (§4, rule B of the plan). These
    # two modules build and send its requests: every arm's prompts are
    # `queue_alone.prompts`', called, which carry the manual's block through
    # `apply.prompts` and `manual.prompts.block`, and the asker is
    # `first_match/ask.py`'s. They are on the same channel, so
    # `TestTheAuthorityChannel` watches them too. The labels enter only at
    # scoring (`reasoned_rule/score.py`), and the rules a ticket matches, and the
    # list's first match over the space, are read from level 3's frozen text
    # (`queue_alone/rules.py`), never the oracle.
    "reasoned_rule/prompts.py",
    "reasoned_rule/ask.py",
]

# The names that carry the hidden policy in code without being the oracle's
# own: its DSL transcription, the module that holds it, and the edges derived
# from its layer order. The authority channel's proposer path may import none.
POLICY_IN_CODE = {"HIDDEN_DSL", "ceiling_check", "hidden_priority"}
AUTHORITY_CHANNEL = ONLINE_LOOP[-13:]


def imports_of(path: Path) -> set[str]:
    """Names imported by the module: both the module and the symbols."""
    tree = ast.parse(path.read_text(), filename=str(path))
    names: set[str] = set()
    for nodo in ast.walk(tree):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                names.update(a.name.split("."))
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.module:
                names.update(nodo.module.split("."))
            for a in nodo.names:
                names.add(a.name)
    return names


class TestTheOnlineLoopDoesNotSeeTheOracle(unittest.TestCase):

    def test_no_online_component_imports_the_policy(self):
        for rel in ONLINE_LOOP:
            with self.subTest(rel):
                filtered = imports_of(REPO / rel) & ORACLE
                self.assertEqual(filtered, set(),
                                 f"{rel} importa del oraculo: {filtered}")

    def test_the_watched_files_exist(self):
        """If somebody renames a module, the test above would silently stop
        watching it."""
        for rel in ONLINE_LOOP:
            with self.subTest(rel):
                self.assertTrue((REPO / rel).is_file(), f"falta {rel}")

    def test_who_may_see_it(self):
        """Measuring offline and labelling the record do consult the oracle. The
        test pins the list so that growing it is a decision, not an oversight."""
        allowed_names = {
            "harness/shadow.py",            # labels the record, does not decide
            "harness/cache_baseline.py",    # baseline: caches the truth as if the LLM gave it
            "harness/ceiling_check.py",     # offline measurement
            "harness/subsumption_check.py",
            "harness/learned_subsumption.py",
            # offline: the default-rule control, added 2026-08-29. It measures
            # the same ceiling as `ceiling_check.py` with the catch-all at its
            # true rank, so it needs `true_action` to score — and only to score.
            # The RANKING it introduces is oracle-free by construction: vacuity
            # is read off DOMAINS and the rule itself. That is what makes it a
            # control on the encoding rather than a criterion handed the answer,
            # and it is stated in the module's docstring.
            "harness/default_rule_control.py",
            "run_experiment.py",
            "rung2/shadow2.py",
            "rung2/ceiling_check2.py",
            # offline: the same ceiling on the exhaustive space, added
            # 2026-08-29. It scores, and only scores: the engine it measures is
            # built by hidden_priority from the layer order, which is where this
            # rung's knowledge of the truth already lived and openly.
            "rung2/ceiling_check2_space.py",
            # offline: the labelled pair benchmark. Added 2026-08-24, and
            # deliberately. It imports true_action and true_rule_id to build the
            # KEY of a benchmark — which of two rules the hidden policy makes win
            # over the region where they compete, and which earlier-layer rule
            # owns that region when neither does. It decides nothing, no component
            # of the online loop imports it, and the key it writes is in the record
            # openly: that is what makes it a benchmark rather than a leak.
            "rung2/pair_benchmark.py",
            "rung3/order_search.py",
            "rung3/budget_and_balance.py",
            "rung3/optimizer_check.py",   # offline: the optimizer's own ceiling
            # offline: the weighted optimizer's ceiling. Added 2026-08-13, and
            # deliberately: it first tried to count the classes off the masks to
            # avoid this import, and the masks give the per-class CEILING, which
            # equals the class size only where every case is winnable — true of
            # the hidden policy, false of the 577 rules by 98 cases in 1005.
            # Avoiding the oracle bought nothing and cost a defect the gate
            # could not see.
            "rung3/optimizer_check_wt.py",
            "rung3/order_search_ls.py",   # offline: labels the two instances
            "rung4/feedback.py",
            # offline: the ILP instances, added 2026-08-30. It LABELS the
            # examples — the supervision the plan declares, and which the
            # proposer never received: it decided each queue itself (§5's
            # erratum of FINDINGS_ILP.md, 2026-10-10) — and it is deliberately
            # the only module in `ilp/` that may. `induce.py` takes bitmasks and
            # nothing else, `I-g3` checks that on its signature and on its
            # imports, and `tests/test_ilp.py` pins it: a competitor that could
            # see the hidden rules would not be a competitor.
            "ilp/instances.py",
        }
        found = set()
        for root in ("harness", "rung2", "rung3", "rung4", "sensitivity",
                     "ilp", "reuse", "fidelity", "edges", "primacy", "why",
                     "authorship", "overlap", "blind", "screen", "bound",
                     "ranking", "students", "escalations",
                     "spotcheck", "unreached", "manual", "apply",
                     "queue_alone", "first_match", "reasoned_rule"):
            for f in (REPO / root).rglob("*.py"):
                if "__pycache__" in f.parts:
                    continue
                if imports_of(f) & ORACLE:
                    found.add(str(f.relative_to(REPO)))
        if imports_of(REPO / "run_experiment.py") & ORACLE:
            found.add("run_experiment.py")
        found.discard("harness/hidden_policy.py")
        self.assertEqual(found, allowed_names)


class TestTheAuthorityChannel(unittest.TestCase):
    """`PLAN_MANUAL.md` gives the proposer the policy, and says by which route.
    These tests hold it to that route: the frozen text, and nothing in code."""

    def test_the_thirteen_modules_are_the_ones_watched(self):
        """`PLAN_MANUAL.md`'s five, since 2026-10-23 `PLAN_APPLY.md`'s two, since
        2026-10-24 `PLAN_QUEUE_ALONE.md`'s two, and since 2026-10-25
        `PLAN_FIRST_MATCH.md`'s two and `PLAN_REASONED_RULE.md`'s two, which
        send the same texts again."""
        self.assertEqual(AUTHORITY_CHANNEL, ["manual/levels.py", "manual/prompts.py",
                                             "manual/compile.py", "manual/ask.py",
                                             "manual/run.py", "apply/prompts.py",
                                             "apply/ask.py", "queue_alone/prompts.py",
                                             "queue_alone/ask.py", "first_match/prompts.py",
                                             "first_match/ask.py", "reasoned_rule/prompts.py",
                                             "reasoned_rule/ask.py"])

    def test_no_proposer_path_module_imports_the_policy_in_code(self):
        for rel in AUTHORITY_CHANNEL:
            with self.subTest(rel):
                found = imports_of(REPO / rel) & (ORACLE | POLICY_IN_CODE)
                self.assertEqual(found, set(), f"{rel} importa la politica: {found}")

    def test_the_policy_reaches_the_prompts_only_through_the_frozen_files(self):
        """Every prompt the package sends is a function of v1, the domain and
        the three files: replacing the files' contents changes the manual
        block, and nothing else in the prompt."""
        from unittest import mock

        from manual import levels, prompts

        texts = {"catalogue": "A", "prose": "B", "rules": "C"}
        with mock.patch.object(levels, "part", side_effect=lambda name: texts[name]):
            self.assertEqual(prompts.block(3), prompts.MANUAL_HEADER + "\n\nC")
            self.assertEqual(prompts.block(2), prompts.MANUAL_HEADER + "\n\nA\n\nB")
            self.assertNotIn("H01", prompts.loop_system_prompt(3))
            self.assertNotIn("H01", prompts.compile_system_prompt(3))

    def test_plan_apply_sends_the_manual_only_through_the_frozen_files(self):
        """`PLAN_APPLY.md`'s prompts carry the level's text as the loop's did,
        and nothing of the policy besides: replacing the files changes the
        system prompt's block, in both arms, and the user message not at all."""
        from unittest import mock

        from apply import prompts as aprompts
        from harness.domain import generate_corpus
        from manual import levels, prompts

        case = generate_corpus(1, seed=17)[0]
        before = aprompts.ticket_ask("t", 3, case)
        texts = {"catalogue": "A", "prose": "B", "rules": "C"}
        with mock.patch.object(levels, "part", side_effect=lambda name: texts[name]):
            after = aprompts.ticket_ask("t", 3, case)
            self.assertIn(prompts.MANUAL_HEADER + "\n\nC", after.system)
            self.assertNotIn("H01", after.system)
            self.assertEqual(after.user, before.user)


class TestTheRung4Channel(unittest.TestCase):
    """The channel is the artefact that contains the risk: if the oracle slips
    in somewhere else, rung 4 measures full supervision."""

    def test_feedback_is_the_only_rung_4_module_touching_the_oracle(self):
        tocan = {f.name for f in (REPO / "rung4").glob("*.py")
                 if imports_of(f) & ORACLE}
        self.assertEqual(tocan, {"feedback.py"})

    def test_the_learner_does_not_receive_the_truth(self):
        """`greedy_from_reports` only sees {case -> reported action}: its
        signature does not admit the true labels by any route."""
        import inspect

        from rung4.sweep import greedy_from_reports

        params = list(inspect.signature(greedy_from_reports).parameters)
        self.assertEqual(params, ["rules", "pool", "reported", "action", "born"])
        self.assertNotIn("truth", params)

    def test_the_channel_emits_less_than_the_truth(self):
        """Its output is strictly poorer: a subset of the cases, and with noise.
        With coverage 0 it emits nothing."""
        from harness.domain import generate_corpus
        from rung4.feedback import Channel

        corpus = generate_corpus(50, seed=17)
        window = list(range(50))
        decisions = {i: "T1_GENERAL" for i in window}
        empty = Channel(coverage=0.0, seed=1).observe(corpus, window, decisions)
        self.assertEqual(empty, {})
        full_one = Channel(coverage=1.0, asymmetry=1.0, seed=1).observe(
            corpus, window, decisions)
        self.assertLessEqual(len(full_one), len(window))

    def test_the_asymmetry_conditions_the_labels_on_the_errors(self):
        """With asymmetry 0 only INCORRECT decisions are observed. It is what
        keeps the channel from being the oracle, and what makes the labelled set
        not i.i.d."""
        from harness.domain import generate_corpus
        from harness.hidden_policy import true_action
        from rung4.feedback import Channel

        corpus = generate_corpus(200, seed=17)
        window = list(range(200))
        decisions = {i: true_action(corpus[i]) for i in window}   # perfect pi0
        rep = Channel(coverage=1.0, asymmetry=0.0, seed=1).observe(
            corpus, window, decisions)
        self.assertEqual(rep, {}, "una pi0 que no falla no genera etiqueta alguna")


if __name__ == "__main__":
    unittest.main()
