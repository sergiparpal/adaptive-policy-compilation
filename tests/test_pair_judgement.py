"""
THE GATES OF `pair_judgement`, AND ABOVE ALL THE THREE LEAKS IT CLOSES.

The stage has not run. There is no figure to pin here and there will not be one
until P-c is signed and the calls are paid for; what this file can be worth is
that the instrument does not hand the model its own answer, that the gates
standing between it and the money are blocking, and that the settings are rung
2's so the comparison the plan wants held actually holds.

The three leaks, in the order they would have gone unnoticed:

  1. `correct_count` — already guarded by `tests/test_engine2.py::TestRender`.
     Nothing here changes it.
  2. `beats` / `loses_to` — `Rule2.render()` prints them, and
     `hidden_priority.build_hidden_engine` populates them with exactly the edges
     this stage asks the model to reproduce. One test below renders a rule off
     that engine and asserts it DOES leak, so the guard is known to be guarding
     something real rather than a hypothesis.
  3. the `H`-identifiers, which are numbered in layer order while the earlier
     layer always wins. A model reading "lower number first" would score high
     without reading a condition.

Nothing here makes a network call: the client is exercised through
`tests.doubles.fake_sdk`, and `main()` is never called without `--dry-run`.
"""

from __future__ import annotations

import inspect
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from harness.domain import ACTIONS, Case
from rung2.hidden_priority import build_hidden_engine
from rung2.pair_judgement import (FLOOR_COIN, MAX_RETRIES, MAX_TOKENS, MODEL,
                                  POSITION_SEED, SHOWN_AS, TEMPERATURE,
                                  Judge, add_breadth, breakdowns,
                                  build_questions, classify, fresh_engine,
                                  gate_no_leak, gate_position_balance,
                                  gate_signature, hidden_rules, kill_switch,
                                  load_benchmark, question, rates, shown_rule,
                                  verdict_histogram, winner_positions)
from rung2.proposers2 import ProposalError
from tests.doubles import FakeOpenAIClient, FixedResponses, fake_sdk

SIGNED = "**Signed by Sergi: Sergi Parpal (date: 2026-08-24)**"
BLANK = "**Signed by Sergi: ______________________ (date: __________)**"


# ---------------------------------------------------------------------------
# The three leaks
# ---------------------------------------------------------------------------

class TestTheLeaksAreClosed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rules = hidden_rules()
        cls.clean, cls.unclean, _g, _rec = load_benchmark()
        cls.rows = build_questions(
            cls.clean, cls.rules, winner_positions(len(cls.clean)))

    def test_the_rules_this_module_builds_carry_no_declared_edge(self):
        for rid, rule in self.rules.items():
            with self.subTest(rid):
                self.assertEqual(rule.beats, [])
                self.assertEqual(rule.loses_to, [])

    def test_a_rule_off_the_hidden_engine_really_would_leak(self):
        """The guard guards something real. `build_hidden_engine` populates
        `beats` with the very edges this stage asks the model to reproduce, and
        `render()` prints them."""
        engine, _declared, _stats = build_hidden_engine()
        leaky = [r for r in engine.rules if r.beats or r.loses_to]
        self.assertTrue(leaky, "the hidden engine declares no edge at all")
        rendered = leaky[0].render()
        self.assertTrue("[gana a" in rendered or "[pierde con" in rendered)

    def test_shown_rule_keeps_the_content_and_drops_everything_else(self):
        rule = self.rules["H01"]
        shown = shown_rule(rule, "A")
        self.assertEqual(shown.rule_id, "A")
        self.assertEqual(shown.action, rule.action)
        self.assertEqual([c.as_dict() for c in shown.conditions],
                         [c.as_dict() for c in rule.conditions])
        self.assertEqual(shown.beats, [])
        self.assertEqual(shown.loses_to, [])

    def test_no_question_names_a_rule_identifier(self):
        """Leak 3. H01..H29 are numbered in layer order and the earlier layer
        always wins."""
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertNotIn(r["winner"], r["question"])
                self.assertNotIn(r["loser"], r["question"])

    def test_no_question_carries_a_declared_edge_annotation(self):
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertNotIn("[gana a", r["question"])
                self.assertNotIn("[pierde con", r["question"])

    def test_no_question_carries_the_oracle_derived_count(self):
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertNotIn("correct_count", r["question"])

    def test_the_question_cannot_receive_the_key_by_any_route(self):
        """Its signature does not admit a winner, an action or a benchmark row.
        The same control `tests/test_oracle_separation.py` puts on rung 4's
        learner."""
        params = list(inspect.signature(question).parameters)
        self.assertEqual(params, ["case", "first", "second"])

    def test_both_rules_and_the_ticket_do_reach_the_question(self):
        """The counterpart: closing the leaks must not have emptied the
        question."""
        r = self.rows[0]
        self.assertIn("A: SI", r["question"])
        self.assertIn("B: SI", r["question"])
        self.assertIn(r["winner_action"], r["question"])
        self.assertIn(r["loser_action"], r["question"])
        self.assertIn('"severity"', r["question"])


class TestTheNoLeakGate(unittest.TestCase):

    def test_it_passes_on_a_clean_question(self):
        rules = hidden_rules()
        q = question(Case(has_security_keyword=True, severity=1,
                          customer_tier="enterprise", product="api",
                          channel="portal", prior_tickets_30d=0,
                          off_hours=False, language="en"),
                     shown_rule(rules["H01"], "A"),
                     shown_rule(rules["H04"], "B"))
        self.assertTrue(gate_no_leak([q])["passes"])

    def test_an_identifier_that_survives_stops_the_run(self):
        g = gate_no_leak(["A: SI severity eq 1 ENTONCES T1_GENERAL",
                          "H03: SI has_security_keyword eq True ENTONCES T2_TECHNICAL"])
        self.assertFalse(g["passes"])
        self.assertEqual(g["questions_naming_a_rule_id"], [1])

    def test_a_declared_edge_annotation_stops_the_run(self):
        g = gate_no_leak(["A: SI severity eq 1 ENTONCES T1_GENERAL  [gana a B]"])
        self.assertFalse(g["passes"])
        self.assertEqual(g["questions_carrying_a_declared_edge"], [0])

    def test_it_looks_at_the_text_and_not_at_the_construction(self):
        """A hand-written string with no rule object behind it still fails. The
        gate is a check on what would be sent."""
        self.assertFalse(gate_no_leak(["... H29 ..."])["passes"])


# ---------------------------------------------------------------------------
# The signature gate
# ---------------------------------------------------------------------------

class TestTheSignatureGate(unittest.TestCase):
    """No flag skips it, so it has to be right."""

    def plan(self, tmp, line):
        p = Path(tmp) / "PLAN_PAIRWISE.md"
        p.write_text(f"# plan\n\n| id | claim |\n\n{line}\n\nrest\n")
        return p

    def test_the_blank_line_is_unsigned(self):
        with TemporaryDirectory() as tmp:
            g = gate_signature(self.plan(tmp, BLANK))
            self.assertTrue(g["line_found"])
            self.assertFalse(g["passes"])

    def test_a_filled_line_is_signed(self):
        with TemporaryDirectory() as tmp:
            g = gate_signature(self.plan(tmp, SIGNED))
            self.assertTrue(g["passes"])
            self.assertEqual(g["line"], SIGNED)

    def test_a_half_filled_line_is_still_unsigned(self):
        """A name and no date, or a date and no name, leaves the other blank —
        and blanks are what the guard reads."""
        half = "**Signed by Sergi: Sergi Parpal (date: __________)**"
        with TemporaryDirectory() as tmp:
            self.assertFalse(gate_signature(self.plan(tmp, half))["passes"])

    def test_a_missing_line_is_unsigned(self):
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "PLAN_PAIRWISE.md"
            p.write_text("# plan with no signature block\n")
            g = gate_signature(p)
            self.assertFalse(g["line_found"])
            self.assertFalse(g["passes"])

    def test_a_missing_file_is_unsigned(self):
        with TemporaryDirectory() as tmp:
            self.assertFalse(gate_signature(Path(tmp) / "absent.md")["passes"])

    def test_the_verdict_on_the_real_plan_follows_its_own_line(self):
        """
        The durable contract, and it holds signed or unsigned: the gate finds
        §0's line in the real plan, and its verdict is what that line says.

        It replaces `test_the_real_plan_is_still_unsigned`, which asserted the
        plan had not been signed yet. That one was a scaffold with a designed
        expiry — it existed so that signing would show up in the suite instead
        of only in a terminal, and on 2026-08-24 it did exactly that, failing
        the commit that carried the signature. Pinning "still unsigned" any
        longer would have meant pinning a state the project is supposed to leave.

        What is worth keeping is that the gate can still FIND the line. If §0's
        signature block is renamed or removed, `line_found` goes false, the gate
        refuses to spend, and this says which of the two happened.
        """
        g = gate_signature()
        self.assertTrue(g["line_found"], "§0's signature line is gone")
        self.assertEqual(g["passes"], "___" not in g["line"])


# ---------------------------------------------------------------------------
# Which of the two goes first
# ---------------------------------------------------------------------------

class TestThePresentationOrder(unittest.TestCase):
    """The benchmark lists the winner first in every row, so an unbalanced
    order would make `always answer the first` a strategy."""

    def test_the_split_is_exact_over_the_170(self):
        pos = winner_positions(170)
        self.assertEqual(pos.count(0), 85)
        self.assertEqual(pos.count(1), 85)

    def test_it_is_deterministic_at_the_declared_seed(self):
        self.assertEqual(winner_positions(170), winner_positions(170))
        self.assertEqual(POSITION_SEED, 17)

    def test_another_seed_deals_differently(self):
        self.assertNotEqual(winner_positions(170),
                            winner_positions(170, seed=18))

    def test_an_odd_population_gives_the_extra_pair_to_the_first_position(self):
        pos = winner_positions(9)
        self.assertEqual(pos.count(0), 5)
        self.assertEqual(pos.count(1), 4)

    def test_the_gate_passes_on_a_balanced_deal(self):
        self.assertTrue(gate_position_balance(winner_positions(170))["passes"])

    def test_the_gate_fails_when_the_winner_is_always_first(self):
        g = gate_position_balance([0] * 170)
        self.assertFalse(g["passes"])
        self.assertEqual(g["shown_first"], 170)

    def test_the_gate_fails_on_a_split_that_is_merely_close(self):
        self.assertFalse(gate_position_balance([0] * 87 + [1] * 83)["passes"])

    def test_a_prefix_of_the_full_deal_is_not_balanced(self):
        """Why `--limit` truncates the POPULATION and not the rows. The first
        ten of a deal balanced over 170 come out 4/6 on the declared seed, and a
        smoke path built that way would fail its own gate before spending
        anything. This is the shape of the defect, pinned so it cannot come
        back."""
        prefix = winner_positions(170)[:10]
        self.assertFalse(gate_position_balance(prefix)["passes"])

    def test_a_truncated_population_is_balanced_over_what_it_asks(self):
        for n in (10, 11, 40, 170):
            with self.subTest(n=n):
                self.assertTrue(
                    gate_position_balance(winner_positions(n))["passes"])

    def test_the_rows_agree_with_the_deal(self):
        rules = hidden_rules()
        clean, _u, _g, _r = load_benchmark()
        pos = winner_positions(len(clean))
        rows = build_questions(clean, rules, pos)
        for r, p in zip(rows, pos):
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertEqual(r["winner_shown_as"], SHOWN_AS[p])
                self.assertEqual(r["shown_as"][SHOWN_AS[p]], r["winner"])
                other = SHOWN_AS[1 - p]
                self.assertEqual(r["shown_as"][other], r["loser"])


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

class TestTheThreeOutcomes(unittest.TestCase):

    def test_the_winners_queue_is_a_correct_edge(self):
        self.assertEqual(classify("SECURITY_INCIDENT", "SECURITY_INCIDENT",
                                  "ONCALL_ESCALATION"), "correct")

    def test_the_losers_queue_is_a_wrong_edge(self):
        self.assertEqual(classify("ONCALL_ESCALATION", "SECURITY_INCIDENT",
                                  "ONCALL_ESCALATION"), "wrong")

    def test_a_third_queue_is_neither(self):
        self.assertEqual(classify("T1_GENERAL", "SECURITY_INCIDENT",
                                  "ONCALL_ESCALATION"), "neither")

    def test_no_answer_at_all_is_neither_and_not_a_discard(self):
        self.assertEqual(classify(None, "SECURITY_INCIDENT",
                                  "ONCALL_ESCALATION"), "neither")


def _rows(correct, wrong, neither, **kw):
    out = []
    for outcome, n in (("correct", correct), ("wrong", wrong),
                       ("neither", neither)):
        for _ in range(n):
            out.append({"outcome": outcome, "winner_shown_as": "A",
                        "winner_is_broader": True,
                        "winner_action": "SECURITY_INCIDENT", **kw})
    return out


class TestTheTwoDenominators(unittest.TestCase):
    """§0 names the first, so the record must carry both and mark which."""

    def test_both_rates_are_computed(self):
        r = rates(_rows(60, 30, 10))
        self.assertAlmostEqual(r["over_all_pairs"]["value"], 0.6)
        self.assertEqual(r["over_all_pairs"]["denominator"], 100)
        self.assertEqual(r["over_two_way_answers"]["value"], round(60 / 90, 4))
        self.assertEqual(r["over_two_way_answers"]["denominator"], 90)

    def test_neither_counts_as_a_failure_in_the_adjudicating_one(self):
        """The whole reason §0 picked it: a coin between the two rules always
        commits, so a model that declines to answer has not been beaten there —
        it has declined to play."""
        with_neither = rates(_rows(60, 30, 10))["over_all_pairs"]["value"]
        without = rates(_rows(60, 30, 0))["over_all_pairs"]["value"]
        self.assertLess(with_neither, without)

    def test_neither_is_free_in_the_one_that_adjudicates_nothing(self):
        """The counterpart, and the reason it does not adjudicate: the two-way
        rate is blind to a refusal to commit."""
        a = rates(_rows(60, 30, 10))["over_two_way_answers"]["value"]
        b = rates(_rows(60, 30, 0))["over_two_way_answers"]["value"]
        self.assertEqual(a, b)

    def test_exactly_one_of_the_two_adjudicates_and_it_is_named(self):
        r = rates(_rows(60, 30, 10))
        self.assertTrue(r["over_all_pairs"]["adjudicates_P_c"])
        self.assertFalse(r["over_two_way_answers"]["adjudicates_P_c"])
        self.assertTrue(r["which_adjudicates_P_c"].startswith("over_all_pairs"))

    def test_the_adjudicating_rate_is_never_the_flattering_one(self):
        """Whatever the run looks like, the rate P-c is read on is at most the
        other. If that ever inverted, the choice §0 made would have stopped
        being the strict one."""
        for c, w, n in ((60, 30, 10), (5, 5, 160), (170, 0, 0), (0, 0, 170)):
            with self.subTest(f"{c}/{w}/{n}"):
                r = rates(_rows(c, w, n))
                strict = r["over_all_pairs"]["value"]
                loose = r["over_two_way_answers"]["value"]
                if loose is not None:
                    self.assertLessEqual(strict, loose)

    def test_both_floors_travel_with_the_rates(self):
        f = rates(_rows(1, 1, 1))["floors"]
        self.assertEqual(f["coin_between_the_two_rules_shown"], 0.50)
        self.assertEqual(f["old_framing_proposal_action_accuracy"], 0.3877)

    def test_an_all_neither_run_has_no_two_way_rate_rather_than_a_zero(self):
        r = rates(_rows(0, 0, 5))
        self.assertEqual(r["over_all_pairs"]["value"], 0.0)
        self.assertIsNone(r["over_two_way_answers"]["value"])


class TestTheBreakdowns(unittest.TestCase):

    def test_the_position_split_separates_the_two_positions(self):
        rows = (_rows(10, 0, 0) + [dict(r, winner_shown_as="B")
                                   for r in _rows(0, 10, 0)])
        b = breakdowns(rows)["by_position_of_the_winner"]
        self.assertEqual(b["shown_first"]["correct"], 10)
        self.assertEqual(b["shown_second"]["wrong"], 10)

    def test_the_breadth_split_reports_the_wrong_edge_rate(self):
        rows = (_rows(2, 8, 0)
                + [dict(r, winner_is_broader=False) for r in _rows(8, 2, 0)])
        b = breakdowns(rows)["by_breadth_of_the_winner"]
        self.assertAlmostEqual(b["winner_is_broader"]["wrong_over_two_way"], 0.8)
        self.assertAlmostEqual(b["winner_is_narrower"]["wrong_over_two_way"], 0.2)


class TestTheKillSwitch(unittest.TestCase):
    """§9. Reported, never acted on."""

    def test_at_or_below_the_coin_it_stops(self):
        self.assertIn("STOP", kill_switch(0.50)["band"])
        self.assertIn("STOP", kill_switch(0.49)["band"])

    def test_between_the_coin_and_the_band_it_refutes_and_waits(self):
        self.assertIn("REFUTED", kill_switch(0.55)["band"])
        self.assertIn("REFUTED", kill_switch(0.60)["band"])

    def test_above_the_band_it_holds(self):
        self.assertIn("HOLDS", kill_switch(0.601)["band"])

    def test_the_coin_is_the_kill_switch_and_not_the_refutation_line(self):
        """§9 keeps the two apart: P-c is refuted at 0.60, its band's own edge,
        and the switch sits lower. A rate of 0.55 refutes without stopping."""
        self.assertEqual(FLOOR_COIN, 0.50)
        self.assertNotIn("STOP", kill_switch(0.55)["band"])

    def test_it_launches_nothing(self):
        params = list(inspect.signature(kill_switch).parameters)
        self.assertEqual(params, ["rate"])


# ---------------------------------------------------------------------------
# The verdict histogram
# ---------------------------------------------------------------------------

class TestTheVerdictHistogramIsOutsideEveryDenominator(unittest.TestCase):

    def test_the_rates_do_not_read_a_verdict(self):
        """The same rows, before and after the histogram writes its verdicts
        into them, give the same rates. §8: count correct edges, never accepted
        ones."""
        rules = hidden_rules()
        clean, _u, _g, _r = load_benchmark()
        rows = build_questions(clean[:20], rules, winner_positions(20))
        for r in rows:
            r["outcome"] = "correct"
        before = rates(rows)
        verdict_histogram(rows, fresh_engine(rules))
        self.assertTrue(any("try_edge_verdict" in r for r in rows))
        self.assertEqual(before, rates(rows))

    def test_it_names_the_verdicts_this_protocol_cannot_reach(self):
        rules = hidden_rules()
        h = verdict_histogram([], fresh_engine(rules))
        self.assertIn("no_solapan", h["unreachable_here"])
        self.assertIn("contradice_subsuncion", h["unreachable_here"])
        self.assertEqual(h["reachable_here"], ["ok", "cierra_ciclo"])

    def test_an_answer_of_neither_declares_no_edge(self):
        rules = hidden_rules()
        clean, _u, _g, _r = load_benchmark()
        rows = build_questions(clean[:5], rules, winner_positions(5))
        for r in rows:
            r["outcome"] = "neither"
        h = verdict_histogram(rows, fresh_engine(rules))
        self.assertEqual(h["counts"], {})
        self.assertFalse(any("try_edge_verdict" in r for r in rows))

    def test_the_engine_it_is_fed_starts_with_no_declared_edge(self):
        engine = fresh_engine(hidden_rules())
        self.assertEqual({rid for rid, s in engine.decl_below.items() if s}, set())
        self.assertEqual({rid for rid, s in engine.decl_above.items() if s}, set())


# ---------------------------------------------------------------------------
# The settings, and the client
# ---------------------------------------------------------------------------

class TestTheSettingsAreRung2s(unittest.TestCase):
    """The comparison against 0.3877 only holds if the model and the sampling
    are the ones that produced it."""

    def test_the_model_and_retries_match_the_rung_2_proposer(self):
        from rung2.proposers2 import OpenRouterProposer2

        sig = inspect.signature(OpenRouterProposer2.__init__)
        self.assertEqual(MODEL, sig.parameters["model"].default)
        self.assertEqual(MAX_RETRIES, sig.parameters["max_retries"].default)

    def test_the_temperature_is_zero(self):
        self.assertEqual(TEMPERATURE, 0)


class TestTheClient(unittest.TestCase):
    """Exercised through the SDK double: no network, no key, no cent."""

    def ask(self, *texts):
        client = FakeOpenAIClient(FixedResponses(*texts))
        with fake_sdk(openai=client):
            judge = Judge()
            try:
                return judge.ask("question"), client, None
            except ProposalError as exc:
                return None, client, exc

    def test_a_parsable_answer_costs_one_call(self):
        (payload, attempts), client, _e = self.ask(
            '{"action": "SECURITY_INCIDENT", "why": "the keyword"}')
        self.assertEqual(payload["action"], "SECURITY_INCIDENT")
        self.assertEqual(attempts, 1)
        self.assertEqual(len(client.peticiones), 1)

    def test_the_first_call_asks_for_a_json_object(self):
        _r, client, _e = self.ask('{"action": "T1_GENERAL"}')
        self.assertEqual(client.peticiones[0]["response_format"],
                         {"type": "json_object"})
        self.assertEqual(client.peticiones[0]["temperature"], TEMPERATURE)
        self.assertEqual(client.peticiones[0]["model"], MODEL)
        self.assertEqual(client.peticiones[0]["max_tokens"], MAX_TOKENS)

    def test_unparsable_text_is_retried_with_an_explicit_correction(self):
        (payload, attempts), client, _e = self.ask(
            "not json at all", '{"action": "T2_TECHNICAL"}')
        self.assertEqual(payload["action"], "T2_TECHNICAL")
        self.assertEqual(attempts, 2)
        self.assertEqual(len(client.peticiones), 2)
        self.assertNotIn("response_format", client.peticiones[1])
        self.assertEqual(len(client.peticiones[1]["messages"]), 4)

    def test_it_gives_up_after_the_declared_retries(self):
        _r, client, exc = self.ask("no", "still no", "no again", "and again")
        self.assertIsInstance(exc, ProposalError)
        self.assertEqual(len(client.peticiones), MAX_RETRIES + 1)

    def test_the_system_prompt_lists_the_eight_queues_and_asks_for_one(self):
        _r, client, _e = self.ask('{"action": "T1_GENERAL"}')
        system = client.peticiones[0]["messages"][0]["content"]
        for a in ACTIONS:
            with self.subTest(a):
                self.assertIn(a, system)
        self.assertIn('"action"', system)

    def test_the_request_carries_no_rule_identifier(self):
        rules = hidden_rules()
        clean, _u, _g, _r = load_benchmark()
        row = build_questions(clean[:1], rules, [0])[0]
        client = FakeOpenAIClient(FixedResponses('{"action": "T1_GENERAL"}'))
        with fake_sdk(openai=client):
            Judge().ask(row["question"])
        sent = str(client.peticiones[0]["messages"])
        self.assertNotIn(row["winner"], sent)
        self.assertNotIn(row["loser"], sent)


# ---------------------------------------------------------------------------
# The population it will be asked of
# ---------------------------------------------------------------------------

class TestThePopulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rules = hidden_rules()
        cls.clean, cls.unclean, cls.gate, _rec = load_benchmark()
        cls.rows = build_questions(cls.clean, cls.rules,
                                   winner_positions(len(cls.clean)))
        add_breadth(cls.rows, fresh_engine(cls.rules))

    def test_it_reads_the_population_stage_b_gated(self):
        self.assertTrue(self.gate["passes"])
        self.assertEqual(len(self.clean), 170)
        self.assertEqual(len(self.unclean), 29)

    def test_the_29_are_carried_but_never_asked_about(self):
        asked = {(r["winner"], r["loser"]) for r in self.rows}
        for p in self.unclean:
            with self.subTest(f"{p['winner']}>{p['loser']}"):
                self.assertNotIn((p["winner"], p["loser"]), asked)

    def test_every_witness_is_matched_by_both_rules(self):
        """The question is only answerable if both rules really fire on the
        ticket. Stage B asserts it when it writes the witness; this asserts it
        again on the object actually sent."""
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                case = Case(**r["witness"])
                self.assertTrue(self.rules[r["winner"]].matches(case))
                self.assertTrue(self.rules[r["loser"]].matches(case))

    def test_the_two_queues_shown_are_always_different(self):
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                self.assertNotEqual(r["winner_action"], r["loser_action"])

    def test_neither_extension_contains_the_other(self):
        """Subsumption-incomparable by construction, so `broader` is only about
        size and the split means what it says."""
        engine = fresh_engine(self.rules)
        for r in self.rows:
            with self.subTest(f"{r['winner']}>{r['loser']}"):
                ew, el = engine.ext[r["winner"]], engine.ext[r["loser"]]
                self.assertNotEqual(ew | el, ew)
                self.assertNotEqual(ew | el, el)

    def test_the_breadth_split_has_both_sides(self):
        """If every winner were the broader rule the split would test nothing."""
        sides = {r["winner_is_broader"] for r in self.rows}
        self.assertEqual(sides, {True, False})


if __name__ == "__main__":
    unittest.main()
