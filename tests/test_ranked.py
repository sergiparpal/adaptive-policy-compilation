"""
The `PLAN_RANKED.md` instrument, before any of its figures exists.

What is pinned:

* The constants, with the client, the pin, the level, the texts and the at-once
  asks imported from `PLAN_CORRECTIONS.md`; the two arms and their engines; the
  seed the next prime after 109; §0's lines as exact fractions; the schedule;
  the sessions; and the gate counting every signature line, without pinning
  whether the plan is signed.
* **The count.** Before any vote the ranking is the domain's order. Every
  citation is a vote, a rule and a side, whatever the engine did with the edge.
  A citation of a rule not yet born never counts. The ranking is the one
  `corrections.online.Agreement` chooses.
* **The decision.** Arm K's engine decides as rung 2's does, and where rung 2's
  returns CONFLICT, by its ranking. It overrides `decide` and nothing else.
* **The loop**, on a corpus built by hand with a scripted proposer: arm L asks
  at a CONFLICT and arm K decides it; a reported error hands its own label in
  both arms; arm K's record keeps what its engine did, and the check on it
  catches a log that is not its births'.
* The readings over the space against the engine's decisions; the two designs
  set aside; the sessions' design; Stage C's exact lines, medians, thin labels,
  counts of runs and every reason a row has no value; nothing built, asked or
  written unsigned.

**No figure of the plan's runs.** The figures §0 declares as computed while
drafting are recomputed by `RK-g2`, which this file runs.
"""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path
from unittest import mock

from harness.domain import ACTIONS, Case
from harness.dsl import Condition

from corrections import declared as DC
from corrections import online as cr_online
from corrections import plan as cr_plan
from manual import instrument as MI
from reasoned_loop import protocol as p
from rung2.engine2 import PriorityEngine, Rule2

from ranked import ask, gates, loop, plan, run, sample, score, setaside
from ranked import engine as E
from ranked import reading as R

REPO = Path(__file__).resolve().parent.parent
F = Fraction
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
SEC, ONC, AM = "SECURITY_INCIDENT", "ONCALL_ESCALATION", "ACCOUNT_MANAGER"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1, "what": "", "source": ""}


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


def case(**kw) -> Case:
    base = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
            "product": "dashboard", "channel": "email", "prior_tickets_30d": 1,
            "off_hours": False, "language": "en"}
    return Case(**{**base, **kw})


def rule(action: str, *conds, **cited) -> Rule2:
    return Rule2(rule_id="R?", conditions=[Condition(a, o, v) for a, o, v in conds],
                 action=action, **cited)


def payload(action: str, *conds) -> dict:
    return {"action": action,
            "conditions": [{"attr": a, "op": o, "value": v} for a, o, v in conds],
            "beats": [], "loses_to": [], "note": "una regla"}


class Script:
    """A proposer double: at each case it writes the rule the script names, and
    places it against each listed rule as the script says, above it by
    default."""

    name = "script"

    def __init__(self, rules: dict[int, dict], sides: dict[int, dict[str, str]]):
        self.rules, self.sides = rules, sides
        self.reports: dict[int, str] = {}
        self.asked: list[tuple[int, int, str | None]] = []

    def first(self, case_, idx: int) -> p.Answer:
        self.asked.append((idx, 0, self.reports.get(idx)))
        pl = dict(self.rules[idx])
        return p.Answer(pl["action"], pl, None, "stop", 1)

    def placement(self, case_, draft, message: str, idx: int, listed=None) -> p.Answer:
        self.asked.append((idx, 1, self.reports.get(idx)))
        side = self.sides.get(idx, {})
        pl = dict(draft.payload,
                  beats=[r for r in listed if side.get(r, "beats") == "beats"],
                  loses_to=[r for r in listed if side.get(r) == "loses_to"])
        return p.Answer(draft.action, pl, None, "stop", 1)


# A base that leaves rung 2's engine a CONFLICT. The third rule declares itself
# above the second and below the first, the second already beats the first, and
# so its loss closes a cycle and is refused. Where the first and the third match
# and the second does not, both stand undefeated.
CORPUS = [case(product="api"), case(customer_tier="business"),
          case(product="mobile", severity=1), case(product="api", severity=1),
          case(product="api", severity=1, language="es")]
LABELS = [(T2, "H16"), (T1, "H28"), (ONC, "H04"), (T3, "H07"), (T3, "H07")]
RULES = {0: payload(T2, ("product", "eq", "api")),
         1: payload(T1, ("customer_tier", "eq", "business")),
         2: payload(ONC, ("severity", "eq", 1)),
         3: payload(T3, ("product", "eq", "api"), ("severity", "eq", 1))}
SIDES = {2: {"R0001": "loses_to"}}
SILENT, REPORTED = [0.9] * len(CORPUS), [0.0] * len(CORPUS)


def looped(arm: str, draws: list[float]):
    """One arm's loop over the hand-built corpus, and what it leaves."""
    engine = loop.engine_for(arm, MI.space())
    prop = Script(RULES, SIDES)
    res = loop.run_loop(CORPUS, LABELS, engine, prop, arm, draws)
    rec = json.loads(json.dumps({"arm": arm, "reports_handed": loop.reports_handed(prop),
                                 "ranked": loop.ranked_part(engine),
                                 **loop.record_of(res, engine)}, default=str))
    return rec, prop, engine


# ---------------------------------------------------------------------------
# 1. The constants, the schedule and the gate
# ---------------------------------------------------------------------------

class TestTheConstants(unittest.TestCase):

    def test_the_client_the_level_and_the_texts_are_plan_corrections(self):
        for name in ("MODEL", "TEMPERATURE", "REASONING", "MAX_TOKENS", "MAX_RETRIES",
                     "CALL_RETRY_WAIT", "RATE_LIMITED", "RATE_LIMIT_WAIT", "PROVIDER",
                     "PROVIDER_NAME", "LEVEL", "COVERAGE", "N", "SEED", "STREAMS"):
            with self.subTest(name):
                self.assertEqual(getattr(plan, name), getattr(cr_plan, name))
        self.assertEqual(plan.PROVIDER, {"order": ["deepinfra/fp8"], "allow_fallbacks": False})
        self.assertEqual((plan.LEVEL, plan.TEXTS_OF, cr_plan.LABELLED), (1, "l", "l"))
        self.assertEqual(plan.settings(), cr_plan.settings())
        self.assertEqual(plan.at_once_settings(), cr_plan.at_once_settings())

    def test_the_arms_and_their_engines(self):
        self.assertEqual(plan.ARMS, ("l", "k"))
        self.assertEqual((plan.CONTROL, plan.RANKED), ("l", "k"))
        self.assertEqual(plan.ENGINE, {"l": "rung2", "k": "ranked"})
        self.assertEqual(run.engine_rule("l"), None)
        self.assertEqual(run.engine_rule("k"), {"vote": plan.VOTE, "tie": plan.TIE,
                                                "decides": plan.DECIDES})
        self.assertIn("CONFLICT", plan.DECIDES)
        self.assertEqual((plan.REPS, plan.SMOKE_N, plan.SMOKE_ARMS, plan.MAX_ESCALATIONS),
                         (3, 30, ("l", "k"), 400))

    def test_the_seed_is_the_next_prime_after_109_and_no_other_threads(self):
        def prime(n: int) -> bool:
            return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
        self.assertEqual(plan.ORDER_SEED, next(n for n in range(110, 200) if prime(n)))
        self.assertNotIn(plan.ORDER_SEED, (83, 89, 97, 101, 103, 107, cr_plan.ORDER_SEED))

    def test_the_lines_are_section_0s_as_fractions(self):
        self.assertEqual(plan.LINES, {"RK-b": F(1, 10), "RK-c": F(1, 2), "RK-d": F(0),
                                      "RK-e": F(1, 2), "RK-f": F(9, 10)})
        self.assertTrue(all(isinstance(v, Fraction) for v in plan.LINES.values()))
        self.assertEqual(plan.ROWS, ("RK-a", "RK-b", "RK-c", "RK-d", "RK-e", "RK-f"))

    def test_the_schedule_alternates_from_the_drawn_arm(self):
        order = plan.schedule()
        self.assertEqual([list(x) for x in order], plan.DECLARED["schedule"])
        self.assertEqual(order[0], ("l", 1))
        self.assertTrue(all(a != b for (a, _), (b, _) in zip(order, order[1:])))

    def test_a_session_after_every_run_and_the_at_once_constants(self):
        self.assertEqual(plan.sessions(), ("smoke", "prior", "l_r1", "k_r1", "l_r2", "k_r2",
                                           "l_r3", "k_r3"))
        for name in ("CHECKPOINTS", "ASKS_PER_CHECKPOINT", "PRIOR_ASKS", "SMOKE_ASKS",
                     "WORKERS", "MAX_REASKS", "AT_ONCE_MAX_TOKENS"):
            self.assertEqual(getattr(plan, name), getattr(cr_plan, name))
        self.assertEqual(plan.checkpoints(45), [10, 20, 40, 45])

    def test_both_arms_read_plan_corrections_draws(self):
        for arm in plan.ARMS:
            for rep in (1, 2, 3, None):
                self.assertEqual(plan.channel_of(arm, rep), cr_plan.channel_of("l", rep))
        with self.assertRaises(ValueError):
            plan.stream("n", 1)

    def test_the_records_land_in_their_directory(self):
        with TempOut() as d:
            self.assertEqual(plan.run_path("k", 2), d / "loop_k_r2.json")
            self.assertEqual(plan.smoke_path("l"), d / "loop_smoke_l.json")
            self.assertEqual(plan.partial_path(plan.tag("k", None)),
                             d / "loop_smoke_k.partial.jsonl")
            self.assertEqual(plan.ask_path("k_r3"), d / "atonce_k_r3.json")
            self.assertEqual(plan.ask_partial_path("prior"), d / "atonce_prior.partial.jsonl")
            for bad in (lambda: plan.run_path("k", 4), lambda: plan.ask_path("n_r1")):
                with self.assertRaises(ValueError):
                    bad()
        self.assertEqual(plan.OUT, Path("results_ranked"))


class TestTheGateCountsEverySignature(unittest.TestCase):

    def test_every_line_is_counted_and_one_is_needed(self):
        signed = "**Signed by Sergi: Sergi Parpal (date: 2026-11-19)**\n"
        blank = "**Signed by Sergi: ________ (date: ________)**\n"
        cases = ((blank, False), (signed, True), (signed + blank, False),
                 (signed * 2, True), ("no signature line at all\n", False))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "PLAN.md"
            for text, ok in cases:
                path.write_text(text)
                with self.subTest(text=text):
                    self.assertEqual(plan.gate_signature(path)["passes"], ok)

    def test_the_plan_carries_its_one_signature_line(self):
        """§0's, and no other. Whether it is filled in is not pinned."""
        self.assertEqual(plan.gate_signature(REPO / "PLAN_RANKED.md")["found"],
                         plan.MIN_SIGNATURES)

    def test_the_gate_reads_this_plan(self):
        self.assertEqual(plan.PLAN, Path("PLAN_RANKED.md"))


# ---------------------------------------------------------------------------
# 2. The count
# ---------------------------------------------------------------------------

class TestTheCount(unittest.TestCase):

    def test_before_any_vote_the_ranking_is_the_domains_order(self):
        t = E.Tally()
        self.assertEqual(t.ranking, tuple(ACTIONS))
        self.assertEqual(t.state, (0, 0, plan.N_RANKINGS))
        self.assertEqual(len(E.rankings()), plan.N_RANKINGS)
        self.assertEqual(E.RankedEngine(space=MI.space()).ranking, tuple(ACTIONS))

    def test_a_vote_takes_the_earliest_ranking_that_agrees(self):
        t = E.Tally()
        t.born({"rule_id": "R0001", "action": T1, "born_at": 0})
        t.born({"rule_id": "R0002", "action": SEC, "born_at": 1, "beats": ["R0001"]})
        self.assertEqual(t.votes, Counter({(SEC, T1): 1}))
        self.assertLess(t.ranking.index(SEC), t.ranking.index(T1))
        agreeing = [r for r in E.rankings() if r.index(SEC) < r.index(T1)]
        self.assertEqual(t.ranking, agreeing[0])
        self.assertEqual(t.state[1:], (1, len(agreeing)))
        self.assertEqual(t.log[-1], {"rule_id": "R0002", "born_at": 1, "ranking": t.state[0],
                                     "agreeing": 1, "tied": len(agreeing), "votes": 1})

    def test_it_is_the_replays_count(self):
        """`corrections.online.Agreement`, on votes drawn at random."""
        rng = random.Random(17)
        mine, theirs = E.Tally(), cr_online.Agreement(list(E.rankings()))
        for k in range(40):
            a, b = rng.sample(ACTIONS, 2)
            v = Counter({(a, b): rng.randint(1, 5)})
            mine.count({"rule_id": f"R{k:04d}", "born_at": k}, v)
            theirs.add(v)
            self.assertEqual(mine.state, theirs.chosen())

    def test_every_citation_is_a_vote_a_rule_and_a_side(self):
        queue = {"R0001": T1, "R0002": T2, "R0003": SEC, "R0004": T1}
        r = {"action": T1, "beats": ["R0002"], "loses_to": ["R0003"],
             "dropped_edges": ["loses_to:R0002:cierra_ciclo", "beats:R0003",
                               "beats:R0004:cierra_ciclo", "beats:R0099"]}
        # Installed, refused for a cycle and outside the round all count; a rule of
        # its own queue and a rule the base does not hold do not. One rule cited on
        # both sides is two votes.
        self.assertEqual(E.votes_of_rule(r, queue),
                         Counter({(T1, T2): 1, (T2, T1): 1, (SEC, T1): 1, (T1, SEC): 1}))
        again = rule(T1, ("severity", "eq", 2), beats=["R0002"], loses_to=["R0003"],
                     dropped_edges=list(r["dropped_edges"]))
        self.assertEqual(E.votes_of_rule(again, queue), E.votes_of_rule(r, queue))

    def test_a_citation_of_a_rule_not_yet_born_never_counts(self):
        t = E.Tally()
        t.born({"rule_id": "R0001", "action": T1, "born_at": 0, "beats": ["R0002"]})
        t.born({"rule_id": "R0002", "action": T2, "born_at": 1})
        self.assertEqual(sum(t.votes.values()), 0)
        rec = {"rules": [{"rule_id": "R0002", "action": T2, "born_at": 1},
                         {"rule_id": "R0001", "action": T1, "born_at": 0, "beats": ["R0002"]}]}
        self.assertEqual(E.tally_of(rec).log, t.log)


# ---------------------------------------------------------------------------
# 3. The decision
# ---------------------------------------------------------------------------

def conflicted(cls=E.RankedEngine, **kw):
    """Two crossing rules of two queues and no edge between them."""
    eng = cls(space=MI.space(), **kw)
    eng.add(rule(T2, ("product", "eq", "api")), born_at=0)
    eng.add(rule(ONC, ("severity", "eq", 1)), born_at=1)
    return eng


class TestTheDecision(unittest.TestCase):

    def test_where_rung_2_would_ask_the_ranking_decides(self):
        eng = conflicted(keep_log=True)
        both = case(product="api", severity=1)
        self.assertEqual(PriorityEngine.decide(eng, both)[0], "CONFLICT")
        outcome, winner, involved = eng.decide(both)
        self.assertEqual((outcome, winner.action, len(involved)), ("ACTION", T2, 2))
        self.assertEqual(eng.case_log[-1], {"by": E.RANKING, "ranking": 0, "queues": [T2, ONC],
                                            "runner_up": ONC, "votes_for": 0,
                                            "votes_against": 0})
        # A third rule's answer votes the other way, and the decision follows.
        eng.add(rule(ONC, ("severity", "eq", 1), ("product", "eq", "mobile"),
                     beats=["R0001"]), born_at=2)
        self.assertEqual(eng.decide(both)[1].action, ONC)
        self.assertEqual(eng.case_log[-1]["votes_for"], 1)
        self.assertEqual(eng.tally.log[-1]["votes"], 1)

    def test_everywhere_else_it_is_rung_2s_engine(self):
        eng = conflicted(keep_log=True)
        eng.add(rule(T3, ("product", "eq", "api"), ("customer_tier", "eq", "business")),
                born_at=2)
        self.assertEqual(eng.try_edge("R0002", "R0001"), "ok")
        for c in (case(product="api"), case(severity=1), case(product="api", severity=1),
                  case(product="api", customer_tier="business"), case()):
            with self.subTest(c):
                self.assertEqual(eng.decide(c)[:2], PriorityEngine.decide(eng, c)[:2])
        self.assertEqual([x["by"] for x in eng.case_log],
                         [E.RUNG2, E.RUNG2, E.RUNG2, E.RUNG2, None])

    def test_it_overrides_decide_and_nothing_else(self):
        self.assertTrue(gates.decide_alone())
        for name in ("add", "try_edge", "beats_me", "wins_over"):
            self.assertIs(getattr(E.RankedEngine, name), getattr(PriorityEngine, name))

    def test_its_decision_is_the_space_as_read(self):
        got = gates.decides_as_claimed(conflicted())
        self.assertGreater(got["conflicts"], 0)
        self.assertTrue(all(v for v in got.values() if isinstance(v, bool)), got)


# ---------------------------------------------------------------------------
# 4. The loop, on a corpus built by hand
# ---------------------------------------------------------------------------

class TestTheLoop(unittest.TestCase):

    def test_arm_l_asks_at_the_conflict_and_arm_k_decides_it(self):
        rec_l, _, _ = looped("l", SILENT)
        rec_k, _, eng = looped("k", SILENT)
        self.assertEqual([e["kind"] for e in rec_l["escalations"]],
                         ["IMPASSE", "IMPASSE", "IMPASSE", "CONFLICT"])
        self.assertEqual([e["kind"] for e in rec_k["escalations"]], ["IMPASSE"] * 3)
        self.assertIn("loses_to:R0001:cierra_ciclo", rec_k["rules"][2]["dropped_edges"])
        self.assertEqual([(r["outcome"], r["predicted"], r["cause"]) for r in rec_k["records"][3:]],
                         [("ACTION", T2, None)] * 2)
        def written(rec):
            return [{k: r[k] for k in ("rule_id", "action", "conditions", "born_at", "beats",
                                       "loses_to", "dropped_edges")} for r in rec["rules"][:3]]
        self.assertEqual(written(rec_l), written(rec_k))
        self.assertIsNone(rec_l["ranked"])
        kept = rec_k["ranked"]
        self.assertEqual([c["by"] for c in kept["cases"]], [None, None, None, E.RANKING,
                                                           E.RANKING])
        self.assertEqual(kept["final"]["n_votes"], 3)
        self.assertEqual((kept["vote"], kept["tie"], kept["decides"]),
                         (plan.VOTE, plan.TIE, plan.DECIDES))
        self.assertEqual(score.taken_by_the_ranking(rec_k),
                         {"cases": 2, "right": 0, "wrong_reported": 0, "wrong_silent": 2,
                          "on_a_tie": 0})
        self.assertEqual(eng.final(), kept["final"])

    def test_a_reported_error_hands_its_own_label_in_both_arms(self):
        rec_k, prop, _ = looped("k", REPORTED)
        self.assertEqual([e["kind"] for e in rec_k["escalations"]],
                         ["IMPASSE", "IMPASSE", "IMPASSE", "ERROR"])
        self.assertEqual(rec_k["reports_handed"], {"3": T3})
        self.assertEqual([a for a in prop.asked if a[0] == 3], [(3, 0, T3), (3, 1, T3)])
        self.assertTrue(run.handed_check(rec_k)[0])
        self.assertEqual(score.taken_by_the_ranking(rec_k)["wrong_reported"], 1)
        self.assertEqual(score.engines_decision(rec_k["records"][3]), T2)
        self.assertEqual(rec_k["records"][4]["predicted"], T3)
        rec_l, prop_l, _ = looped("l", REPORTED)
        self.assertEqual(rec_l["reports_handed"], {})        # arm l asked: no error to report
        self.assertTrue(run.handed_check(rec_l)[0])

    def test_an_arm_is_handed_its_own_engine(self):
        for arm, cls in (("l", E.RankedEngine), ("k", PriorityEngine)):
            with self.assertRaises(ValueError):
                loop.run_loop(CORPUS, LABELS, cls(space=MI.space()), Script(RULES, SIDES), arm,
                              SILENT)
        with self.assertRaises(ValueError):
            loop.engine_for("n", MI.space())

    def test_the_check_on_arm_ks_record(self):
        rec_k, _, _ = looped("k", SILENT)
        rec_l, _, _ = looped("l", SILENT)
        self.assertTrue(run.ranked_check(rec_k)[0], run.ranked_check(rec_k))
        self.assertTrue(run.ranked_check(rec_l)[0])
        tampered = json.loads(json.dumps(rec_k))
        tampered["ranked"]["log"][-1]["ranking"] += 1
        self.assertFalse(run.ranked_check(tampered)[0])
        short = json.loads(json.dumps(rec_k))
        short["ranked"]["cases"].pop()
        self.assertFalse(run.ranked_check(short)[0])
        self.assertFalse(run.ranked_check({**rec_l, "ranked": rec_k["ranked"]})[0])
        self.assertFalse(run.ranked_check({**rec_k, "ranked": None})[0])


# ---------------------------------------------------------------------------
# 5. The readings, and the designs set aside
# ---------------------------------------------------------------------------

class TestTheReadings(unittest.TestCase):

    def test_a_record_read_after_every_birth(self):
        rec_k, _, eng = looped("k", SILENT)
        got = R.as_it_went(rec_k, MI.space(), MI.space_truth())
        self.assertTrue(got["sound"])
        self.assertEqual([c["rule_id"] for c in got["curve"]], ["R0001", "R0002", "R0003"])
        self.assertTrue(all(c["ranked"] >= c["rung2"] for c in got["curve"]))
        self.assertGreater(got["curve"][-1]["conflict"], 0)
        self.assertEqual(got["tally"].final(), rec_k["ranked"]["final"])
        self.assertEqual(R.summary(got["curve"], "ranked")["final"], got["curve"][-1]["ranked"])
        self.assertEqual(R.at_case(got["curve"], 1)["rule_id"], "R0002")
        self.assertIsNone(R.at_case(got["curve"], -1))

    def test_the_conflicts_a_run_asked_about(self):
        rec_l, _, _ = looped("l", SILENT)
        asked = list(R.asked_conflicts(rec_l, CORPUS, MI.space()))
        self.assertEqual([(a["idx"], a["queues"], a["decided"], a["truth"]) for a in asked],
                         [(3, [T2, ONC], T2, T3)])
        self.assertEqual(gates.first_call_right(rec_l), 1)

    def test_a_final_base_as_arm_ks_engine(self):
        rec_k, _, live = looped("k", SILENT)
        again = R.engine_of(MI.final_engine(rec_k), rec_k)
        self.assertEqual(again.final(), live.final())
        for c in CORPUS:
            self.assertEqual(again.decide(c)[1].action, live.decide(c)[1].action)

    def test_a_point_and_the_two_readings(self):
        space = MI.space()
        self.assertEqual(R.point_of(CORPUS[0], space).bit_count(), 1)
        queues = {q: 0 for q in ACTIONS}
        queues[T2], queues[ONC] = 0b0111, 0b1100
        got = R.read(queues, tuple(ACTIONS), {T2: 0b0011, ONC: 0b1100})
        self.assertEqual((got["conflict"], got["rung2"], got["ranked"]), (0b0100, 0b1011, 0b1011))
        flipped = tuple(reversed(ACTIONS))
        self.assertEqual(R.read(queues, flipped, {T2: 0b0011, ONC: 0b1100})["ranked"], 0b1111)


class TestTheDesignsSetAside(unittest.TestCase):

    def test_the_whole_base_in_the_rankings_order_and_no_edge_read(self):
        total = conflicted(setaside.Total)
        self.assertEqual(total.try_edge("R0002", "R0001"), "ok")
        both = case(product="api", severity=1)
        self.assertEqual(PriorityEngine.decide(total, both)[1].action, ONC)
        self.assertEqual(total.decide(both)[1].action, T2)       # the domain's order
        total.add(rule(T3, ("product", "eq", "api"), ("severity", "eq", 1)), born_at=2)
        self.assertEqual(total.decide(both)[1].action, T3)       # the nested rule first
        self.assertEqual(total.order[0], "R0003")

    def test_a_rule_written_again_votes_again_under_one_count_alone(self):
        votes = {}
        for count in (setaside.EVERY, setaside.DISTINCT):
            total = conflicted(setaside.Total, count=count)
            for k in (2, 3):
                total.add(rule(ONC, ("severity", "eq", 1), beats=["R0001"]), born_at=k)
            total.refresh()
            votes[count] = total.tally.votes[(ONC, T2)]
        self.assertEqual(votes, {setaside.EVERY: 2, setaside.DISTINCT: 1})


# ---------------------------------------------------------------------------
# 6. The at-once asks
# ---------------------------------------------------------------------------

class TestTheAtOnceAsks(unittest.TestCase):

    def test_the_design_of_each_session(self):
        rec = {"records": [{"idx": i, "truth": T3} for i in range(45)],
               "escalations": [{"idx": i, "kind": "ERROR"} for i in range(45)],
               "reports_handed": {str(i): T3 for i in range(45)}}
        self.assertEqual([a.id for a in ask.design("prior")],
                         [f"prior:0:{k}" for k in range(1, 6)])
        self.assertEqual([(a.checkpoint, len(a.labelled)) for a in ask.design("smoke", rec)],
                         [(0, 0), (45, 45)])
        for session in ("l_r2", "k_r2"):
            asks = ask.design(session, rec)
            self.assertEqual([a.checkpoint for a in asks],
                             [j for j in (10, 20, 40, 45) for _ in range(3)])
            self.assertEqual(asks[0].id, f"{session}:10:1")
        with self.assertRaises(ValueError):
            ask.design("n_r1", rec)
        with self.assertRaises(ask.NotHanded):
            ask.design("smoke", {**rec, "escalations": [], "reports_handed": {}})

    def test_where_a_session_reads_its_labels(self):
        with TempOut() as d:
            self.assertEqual(ask.source_of("smoke"), d / "loop_smoke_l.json")
            self.assertIsNone(ask.source_of("prior"))
            self.assertEqual(ask.source_of("k_r3"), d / "loop_k_r3.json")
            self.assertEqual(ask.source_of("l_r1"), d / "loop_l_r1.json")
            self.assertEqual(ask.protocol_header("k_r1", "x")["session"], "k_r1")
            self.assertEqual(ask.protocol_header("k_r1", "x")["plan"], "PLAN_RANKED.md")


# ---------------------------------------------------------------------------
# 7. Stage C
# ---------------------------------------------------------------------------

def a_run(rep, space, ranking=(SEC, T1), security=F(2, 3), oncall=F(1, 2), taken=F(3, 5)):
    return {"rep": rep, "space": F(space), "ranking": list(ranking), "security": security,
            "oncall": oncall, "taken": taken}


class TestStageC(unittest.TestCase):

    def test_the_median_rows_with_their_thin_labels(self):
        runs = {"k": [a_run(1, "3/4"), a_run(2, "7/10"), a_run(3, "3/5")],
                "l": [a_run(1, "11/20"), a_run(2, "2/5"), a_run(3, "14/25")]}
        b = score.row("RK-b", runs, {})
        self.assertEqual((b["verdict"], b["value"]["fraction"], b["thin"]),
                         (score.HOLDS, "3/20", True))
        steady = {"k": [a_run(k, "4/5") for k in (1, 2, 3)],
                  "l": [a_run(k, "1/2") for k in (1, 2, 3)]}
        self.assertEqual(score.row("RK-b", steady, {})["thin"], False)
        self.assertEqual(score.row("RK-c", runs, {})["verdict"], score.HOLDS)
        self.assertEqual(score.row("RK-e", runs, {})["value"]["fraction"], "3/5")
        f = score.row("RK-f", runs, {})
        self.assertEqual((f["verdict"], f["line"]["fraction"]), (score.REFUTED, "9/10"))
        edge = {"k": [a_run(k, "3/5") for k in (1, 2)], "l": [a_run(k, "1/2") for k in (1, 2)]}
        self.assertEqual(score.row("RK-b", edge, {})["verdict"], score.HOLDS)   # at the line

    def test_the_count_of_runs_that_put_security_first(self):
        runs = {"k": [a_run(1, "1/2"), a_run(2, "1/2"), a_run(3, "1/2")], "l": []}
        a = score.row("RK-a", runs, {})
        self.assertEqual((a["verdict"], a["value"], a["thin"]), (score.HOLDS, [3, 3], False))
        runs["k"][1] = a_run(2, "1/2", ranking=(T1, SEC))
        self.assertEqual(score.row("RK-a", runs, {})["verdict"], score.REFUTED)
        self.assertEqual(score.row("RK-a", {"k": runs["k"][:1], "l": []}, {})["verdict"],
                         score.NO_VALUE)
        self.assertEqual(score.row("RK-a", {"k": [runs["k"][0], runs["k"][2]], "l": []},
                                   {})["value"], [2, 2])

    def test_the_difference_from_at_once_and_its_reasons_for_no_value(self):
        runs = {"k": [a_run(1, "3/4"), a_run(2, "7/10"), a_run(3, "3/5")], "l": []}
        extra = {"k_r1": {"at_once_all": F(7, 10)}, "k_r2": {"at_once_all": F(13, 20)},
                 "k_r3": {"at_once_all": F(4, 5)}}
        d = score.row("RK-d", runs, extra)
        self.assertEqual((d["verdict"], d["value"]["fraction"], d["thin"]),
                         (score.HOLDS, "1/20", True))
        extra["k_r1"]["at_once_all"] = None
        self.assertEqual(score.row("RK-d", runs, extra)["verdict"], score.REFUTED)
        extra["k_r2"]["at_once_all"] = None
        none = score.row("RK-d", runs, extra)
        self.assertEqual((none["verdict"], none["per_run"]["1"]), (score.NO_VALUE, None))

    def test_a_row_without_two_runs_with_a_value_has_none(self):
        runs = {"k": [a_run(1, "3/4", taken=None), a_run(2, "7/10", taken=None),
                      a_run(3, "3/5")],
                "l": [a_run(1, "1/2")]}
        self.assertEqual(score.row("RK-e", runs, {})["verdict"], score.NO_VALUE)
        self.assertEqual(score.row("RK-b", runs, {})["verdict"], score.NO_VALUE)
        self.assertEqual(score.row("RK-c", runs, {})["verdict"], score.HOLDS)

    def test_what_the_engine_decided_at_a_case(self):
        self.assertEqual(score.engines_decision({"cause": "ERROR", "engine_action": T2,
                                                 "predicted": T3}), T2)
        self.assertEqual(score.engines_decision({"cause": None, "engine_action": None,
                                                 "predicted": T3}), T3)
        self.assertIsNone(score.taken_by_the_ranking({"records": []}))


# ---------------------------------------------------------------------------
# 8. Nothing is built, asked or written unsigned
# ---------------------------------------------------------------------------

class TestNothingUnsigned(unittest.TestCase):

    def test_every_writer_refuses_unsigned(self):
        with TempOut() as d, mock.patch.object(plan, "gate_signature", return_value=UNSIGNED):
            for argv, main in ((["--smoke", "--arm", "l"], run.main),
                               (["--rep", "1", "--arm", "k"], run.main),
                               (["--session", "prior"], ask.main),
                               ([], sample.main), ([], score.main)):
                with self.subTest(argv=argv, main=main.__module__):
                    with mock.patch.object(gates, "run_checks") as checks:
                        with self.assertRaises(SystemExit):
                            main(argv)
                        checks.assert_not_called()
            self.assertEqual(list(d.iterdir()), [])

    def test_the_turn(self):
        with TempOut():
            self.assertEqual(run.next_step(), "ranked.run --smoke --arm l")
            self.assertEqual(run.sessions_before("k", 2),
                             ["smoke", "prior", "l_r1", "k_r1", "l_r2"])
            self.assertFalse(run.turn_check("l", 1)[0])
            self.assertFalse(ask.turn_check("smoke")[0])


class TestTheGates(unittest.TestCase):

    def test_the_cheap_checks_pass(self):
        self.assertTrue(gates.texts()["passes"], gates.texts())
        self.assertTrue(gates.requests()["passes"])
        self.assertTrue(gates.the_pool_is_for_asks())
        self.assertTrue(gates.step_zero()["passes"])

    def test_the_declared_figures_come_back(self):
        """§0's figures 2 to 7, recomputed from the closed records and the corpus."""
        got = gates.drafting()
        self.assertTrue(got["passes"], got)

    def test_a_closed_run_replayed_under_both_arms(self):
        online = json.loads(cr_online.record_path().read_text())
        declared = json.loads(DC.record_path().read_text())
        got = gates.replays(3, online, declared)
        self.assertTrue(got["passes"], got)


if __name__ == "__main__":
    unittest.main()
