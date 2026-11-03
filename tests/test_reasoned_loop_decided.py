"""
`reasoned_loop/decided.py` — the POST-RUN reading of what each placed edge
decides, no figure.

What is pinned is the instrument, on small worlds worked by hand: the masks the
base is read by against the fill's count, one edge reversed by masks against the
engine's reinstall, a reversal that would close a cycle, an edge whose pair
verdict and point verdict agree, one where a third rule governs the region its
pair verdict is read on and the two part, one that decides nothing, the room's
right points no single reversal changes, the readings on rows built by hand,
the expectation's clauses at their edges, and that the writer refuses unsigned
before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

from authorship import gates as egates
from authorship import protocol as e
from blind import readings as breadings
from blind import rows as brows
from reasoned_loop import decided, plan
from rung2.engine2 import EDGE_OK, Space

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
SI = "SECURITY_INCIDENT"
HIT, MISS, TIE, NEITHER = brows.HIT, brows.MISS, brows.TIE, brows.NEITHER
UNSIGNED = {"passes": False, "found": 3, "unsigned": 1}


def r_(rid, born, action, **conds):
    cs = []
    for a, x in conds.items():
        op = "in" if isinstance(x, list) else "eq"
        cs.append({"attr": a, "op": op, "value": x})
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": cs}


def record(rules, log):
    return {"rules": rules, "edge_log": [(w, l, EDGE_OK) for w, l in log],
            "edge_channels": [e.WRITE] * len(log), "records": []}


def ext(rule):
    return brows.ext_of(rule, SPACE)


A = r_("A", 0, T1, product="billing")
B = r_("B", 1, T2, customer_tier="free")
SHARED = ext(A) & ext(B)


def world(rules, log, tmask):
    rec = record(rules, log)
    engine, problems = egates.rebuild_final(rec, SPACE)
    assert not problems
    stage_c = {"edges": brows.edge_rows(rec, engine, tmask, SPACE.full)}
    return rec, engine, decided.read_run(rec, stage_c, on=(SPACE, tmask, SPACE.full))


def truth(**masks):
    out = {q: 0 for q in (T1, T2, T3, SI)}
    out.update(masks)
    return out


class TestTheMasks(unittest.TestCase):

    def setUp(self):
        # C, of B's queue, lies inside both A and B, on three channels of four.
        self.C = r_("C", 2, T2, product="billing", customer_tier="free",
                    channel=["email", "chat", "phone"])
        portal = SHARED & ~ext(self.C)
        self.tmask = truth(**{T1: (ext(A) & ~ext(B)) | portal,
                              T2: (ext(B) & ~portal)})
        self.rec = record([A, B, self.C], [("A", "B")])
        self.engine, _ = egates.rebuild_final(self.rec, SPACE)

    def test_right_within_is_the_fill_s_count(self):
        und = brows.undefeated_masks(self.engine)
        action = {r.rule_id: r.action for r in self.engine.rules}
        self.assertEqual(decided.right_within(und, action, self.tmask, SPACE.full),
                         breadings.decided_and_right(self.engine, self.tmask, SPACE.full)[1])

    def test_a_reversal_by_masks_is_the_reinstall(self):
        und = brows.undefeated_masks(self.engine)
        action = {r.rule_id: r.action for r in self.engine.rules}
        by_masks = decided.right_within(decided.reversed_undefeated(self.engine, und, "A", "B"),
                                        action, self.tmask, SPACE.full)
        ok, reinstalled = decided.reinstalled_right(self.rec, "A", "B",
                                                    on=(SPACE, self.tmask, SPACE.full))
        self.assertTrue(ok)
        self.assertEqual(by_masks, reinstalled)
        self.assertNotEqual(by_masks, breadings.decided_and_right(
            self.engine, self.tmask, SPACE.full)[1])

    def test_a_reversal_that_would_close_a_cycle(self):
        # A over B, A over C and C over B: B over A closes A -> C -> B -> A.
        C = r_("C", 2, T3, channel="email")
        rec = record([A, B, C], [("A", "B"), ("A", "C"), ("C", "B")])
        engine, problems = egates.rebuild_final(rec, SPACE)
        self.assertEqual(problems, [])
        self.assertTrue(decided.closes_cycle(engine, "A", "B"))
        self.assertFalse(decided.closes_cycle(engine, "C", "B"))
        self.assertFalse(decided.closes_cycle(engine, "A", "C"))

    def test_the_gate_reads_the_engine_and_needs_one_edge(self):
        run = decided.read_run(self.rec, {"edges": brows.edge_rows(
            self.rec, self.engine, self.tmask, SPACE.full)}, on=(SPACE, self.tmask, SPACE.full))
        g = decided.reversal_gate(self.rec, run, on=(SPACE, self.tmask, SPACE.full))
        self.assertEqual((g["checked"], g["tried"], g["passes"]), (1, 1, True))
        run["rows"] = [{**r, "rl_e": False} for r in run["rows"]]
        g = decided.reversal_gate(self.rec, run, on=(SPACE, self.tmask, SPACE.full))
        self.assertEqual((g["checked"], g["passes"]), (0, False))


class TestOneEdge(unittest.TestCase):

    def test_no_third_rule_the_verdicts_agree(self):
        # B's queue is right on the shared region, and A was put over B.
        tmask = truth(**{T1: ext(A) & ~ext(B), T2: ext(B)})
        _, _, run = world([A, B], [("A", "B")], tmask)
        (row,) = run["rows"]
        self.assertTrue(row["rl_e"])
        self.assertEqual((row["pair"], row["free"], row["point"]), (MISS, MISS, MISS))
        self.assertEqual((row["gains"], row["losses"], row["governed"], row["shared"]),
                         (0, SHARED.bit_count(), 0, SHARED.bit_count()))
        self.assertEqual(row["losses_room"], SHARED.bit_count())
        self.assertFalse(row["closes_cycle"])
        self.assertEqual(row["ranking_names"], "B")   # T2 ranks above T1
        self.assertEqual(run["pivotal"], {"room_right": 0, "pivotal": 0,
                                          "by_no_single_reversal": 0})

    def test_a_third_rule_governs_where_the_pair_is_read(self):
        # C, of B's queue, decides three quarters of the shared region right
        # whichever way A and B are ordered. On the last quarter A is right.
        C = r_("C", 2, T2, product="billing", customer_tier="free",
               channel=["email", "chat", "phone"])
        portal = SHARED & ~ext(C)
        tmask = truth(**{T1: (ext(A) & ~ext(B)) | portal, T2: ext(B) & ~portal})
        _, _, run = world([A, B, C], [("A", "B")], tmask)
        (row,) = run["rows"]
        self.assertEqual((row["pair"], row["free"], row["point"]), (MISS, HIT, HIT))
        self.assertEqual(row["governed"], (SHARED & ext(C)).bit_count())
        self.assertEqual((row["gains"], row["losses"]), (portal.bit_count(), 0))
        self.assertEqual(run["room_points"], portal.bit_count())
        self.assertEqual(run["pivotal"], {"room_right": portal.bit_count(),
                                          "pivotal": portal.bit_count(),
                                          "by_no_single_reversal": 0})

    def test_a_third_rule_over_the_whole_region_leaves_nothing_to_decide(self):
        C = r_("C", 2, T3, product="billing", customer_tier="free")
        tmask = truth(**{T1: ext(A) & ~ext(B), T2: ext(B) & ~ext(A), T3: SHARED})
        _, _, run = world([A, B, C], [("A", "B")], tmask)
        (row,) = run["rows"]
        self.assertEqual((row["pair"], row["point"]), (NEITHER, NEITHER))
        self.assertEqual((row["governed"], row["gains"], row["losses"]),
                         (SHARED.bit_count(), 0, 0))

    def test_a_point_two_edges_decide_together(self):
        # A and D, both T1 and crossing, are each put over B. Where all three
        # match, reversing either edge alone leaves B defeated by the other.
        D = r_("D", 2, T1, severity=1)
        both = ext(A) & ext(D) & ext(B)
        tmask = truth(**{T1: ext(A) | ext(D), T2: ext(B) & ~(ext(A) | ext(D))})
        _, _, run = world([A, B, D], [("A", "B"), ("D", "B")], tmask)
        rows = {(r["winner"], r["loser"]): r for r in run["rows"]}
        alone = (ext(A) & ext(B) & ~ext(D)).bit_count()
        self.assertEqual((rows[("A", "B")]["point"], rows[("A", "B")]["gains"]), (HIT, alone))
        self.assertEqual(rows[("A", "B")]["governed"], 0)
        room = (ext(B) & (ext(A) | ext(D))).bit_count()
        self.assertEqual(run["pivotal"], {"room_right": room, "pivotal": room - both.bit_count(),
                                          "by_no_single_reversal": both.bit_count()})


def row(older, pair, point, queues=(T1, T2), gains=0, losses=0, governed=0, shared=4,
        free=None):
    return {"winner": "N", "loser": older, "older": older, "younger": "N", "queues": queues,
            "same_queue": False, "keyword": False, "rl_e": True, "pair": pair,
            "free": free or pair, "point": point, "gains": gains, "losses": losses,
            "gains_room": gains, "losses_room": losses, "governed": governed,
            "shared": shared, "closes_cycle": False}


class TestTheReadings(unittest.TestCase):

    def test_the_crosstab_and_the_direction_three_ways(self):
        rows = [row("A", HIT, HIT), row("B", MISS, HIT, governed=3),
                row("C", MISS, NEITHER, governed=4), row("D", TIE, MISS)]
        x = decided.crosstab(rows)
        self.assertEqual((x[HIT][HIT], x[MISS][HIT], x[MISS][NEITHER], x[TIE][MISS]),
                         (1, 1, 1, 1))
        pair = decided.by_older([rows], "pair")
        point = decided.by_older([rows], "point")
        self.assertEqual((pair["units"], pair["declared_exact"]), (3, Fraction(1, 3)))
        self.assertEqual((point["units"], point["declared_exact"]), (3, Fraction(2, 3)))
        # T2 ranks above T1: the ranking names the loser, right where it is better.
        self.assertEqual(point["ranking_exact"], Fraction(1, 3))
        strict = decided.by_older([rows], "pair", keep=lambda r: decided.strict(r, "point"))
        self.assertEqual((strict["units"], strict["declared_exact"]), (2, Fraction(1, 2)))

    def test_points_and_governance_by_pair(self):
        rows = [row("A", HIT, HIT, gains=6), row("B", HIT, NEITHER),
                row("C", MISS, HIT, gains=2, governed=3), row("D", MISS, NEITHER, governed=4)]
        p = decided.points_by_pair(rows)
        self.assertEqual((p[HIT]["edges"], p[HIT]["changing"], p[HIT]["gains"]), (2, 1, 6))
        self.assertEqual(p[HIT]["mean_changed_exact"], 3)
        self.assertEqual(p[MISS]["mean_changed_exact"], 1)
        g = decided.governed_by_pair(rows)
        self.assertEqual(g[HIT]["median_exact"], 0)
        self.assertEqual(g[MISS]["median_exact"], Fraction(7, 8))
        self.assertEqual((g[MISS]["all_governed"], g[HIT]["none_governed"]), (1, 2))


class TestTheExpectation(unittest.TestCase):

    def arms(self, missing_b, missing, point_e, rank_e, point_i, rank_i, gov_b, gov_a,
             mean_b, mean_a):
        def arm(point, rank):
            return {"crosstab": {MISS: {HIT: missing - missing_b, MISS: missing_b, TIE: 0,
                                        NEITHER: 0}},
                    "direction": {"point": {"units": 10, "declared": None, "ranking": None,
                                            "declared_exact": point, "ranking_exact": rank}},
                    "governed_by_pair": {MISS: {"median_share": None, "median_exact": gov_b},
                                         HIT: {"median_share": None, "median_exact": gov_a}},
                    "points_by_pair": {MISS: {"mean_changed": None, "mean_changed_exact": mean_b},
                                       HIT: {"mean_changed": None, "mean_changed_exact": mean_a}}}
        return {"e": arm(point_e, rank_e), "i": arm(point_i, rank_i)}

    def test_clause_by_clause_at_their_edges(self):
        F = Fraction
        x = decided.read_expectation(self.arms(1, 3, F(9, 10), F(8, 10), F(1, 2), F(3, 5),
                                               F(1, 2), F(1, 4), F(2), F(5)))
        self.assertEqual([c["holds"] for c in x], [True] * 5)
        x = decided.read_expectation(self.arms(2, 4, F(89, 100), F(9, 10), F(1, 2), F(1, 2),
                                               F(1, 4), F(1, 4), F(5), F(5)))
        self.assertEqual([c["holds"] for c in x], [False] * 5)

    def test_a_reading_without_value_does_not_hold(self):
        x = decided.read_expectation(self.arms(0, 0, None, None, None, None, None, None,
                                               None, None))
        self.assertEqual([c["holds"] for c in x], [False] * 5)


class TestAddedAfterTheFirstRun(unittest.TestCase):
    """A over B, A over C and C over B. B over A closes the cycle A -> C -> B,
    and where all three match the reversed relation leaves no rule undefeated."""

    def setUp(self):
        self.C = r_("C", 2, T3, channel="email")
        a, b, c = ext(A), ext(B), ext(self.C)
        self.tmask = truth(**{T1: a, T2: b & ~a, T3: c & ~a & ~b})
        self.on = (SPACE, self.tmask, SPACE.full)
        self.rec, self.engine, self.run = world([A, B, self.C],
                                                [("A", "B"), ("A", "C"), ("C", "B")],
                                                self.tmask)
        self.all3 = a & b & c
        self.ab_only = a & b & ~c

    def test_the_points_a_reversal_leaves_without_a_rule(self):
        und = brows.undefeated_masks(self.engine)
        self.assertEqual(decided.without_a_rule(self.engine, und, SPACE.full), 0)
        flipped = decided.reversed_undefeated(self.engine, und, "A", "B")
        self.assertEqual(decided.without_a_rule(self.engine, flipped, SPACE.full), self.all3)

    def test_taking_an_edge_out(self):
        und = brows.undefeated_masks(self.engine)
        out = decided.removed_undefeated(self.engine, und, "A", "B")
        self.assertEqual(out["A"], und["A"])
        self.assertEqual(out["B"], ext(B) & ~ext(self.C))

    def test_an_edge_read_again(self):
        again = {(x["winner"], x["loser"]): x for x in decided.read_again(self.run, on=self.on)}
        ab = again[("A", "B")]
        self.assertEqual((ab["gains_cycle"], ab["point_discounted"]),
                         (self.all3.bit_count(), HIT))
        # Taken out, A and B are left in conflict where C does not match.
        self.assertEqual((ab["gains_alt"], ab["losses_alt"], ab["point_alt"]),
                         (self.ab_only.bit_count(), 0, HIT))
        rows = {(r["winner"], r["loser"]): r for r in self.run["rows"]}
        self.assertTrue(rows[("A", "B")]["closes_cycle"])
        self.assertEqual(rows[("A", "B")]["gains"], (ext(A) & ext(B)).bit_count())
        # A reversal the engine would accept is its own alternative.
        ac = again[("A", "C")]
        self.assertFalse(rows[("A", "C")]["closes_cycle"])
        self.assertEqual((ac["gains_alt"], ac["losses_alt"], ac["gains_cycle"]),
                         (rows[("A", "C")]["gains"], rows[("A", "C")]["losses"], 0))
        m = decided.merged(self.run, decided.read_again(self.run, on=self.on))
        by = {(r["winner"], r["loser"]): r for r in m}
        self.assertEqual(by[("A", "B")]["gains_discounted"], self.ab_only.bit_count())

    def test_the_arm_and_the_clauses_read_again(self):
        rows = [{**row("A", HIT, HIT, gains=6), "gains_cycle": 6, "gains_discounted": 0,
                 "point_discounted": NEITHER, "gains_alt": 2, "losses_alt": 0, "point_alt": HIT},
                {**row("B", MISS, MISS, losses=3), "gains_cycle": 0, "gains_discounted": 0,
                 "point_discounted": MISS, "gains_alt": 0, "losses_alt": 3, "point_alt": MISS}]
        got = decided.added_readings([rows])
        self.assertEqual((got["gains"], got["gains_cycle"]), (6, 6))
        self.assertEqual(got["discounted"]["crosstab"][HIT][NEITHER], 1)
        self.assertEqual(got["alternative"]["crosstab"][MISS][MISS], 1)
        self.assertEqual(got["alternative"]["points_by_pair"][HIT]["mean_changed_exact"], 2)
        self.assertEqual(got["discounted"]["direction"]["declared_exact"], 0)
        arms = {a: decided.arm_readings([rows]) for a in plan.ARMS}
        again = decided.clauses_again(arms, {a: got for a in plan.ARMS})
        self.assertEqual(sorted(again), ["alternative", "discounted"])
        self.assertEqual([c["clause"] for c in again["alternative"]],
                         ["D1", "D2", "D3", "D4", "D5"])


class TestTheRecordComesBack(unittest.TestCase):

    def test_gate_5(self):
        import json
        import tempfile
        body = {"_env": {"git_commit": "new"}, "gates": [1, 2], "arms": {"x": 0.1234567},
                "added": [1]}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "decided.json"
            self.assertTrue(decided.comes_back(body, path)["passes"])
            path.write_text(json.dumps({"_env": {"git_commit": "old"}, "gates": [1],
                                        "arms": {"x": 0.123457}}))
            got = decided.comes_back(body, path)
            self.assertEqual((got["passes"], got["earlier"], got["differ"]), (True, "old", []))
            path.write_text(json.dumps({"_env": {}, "arms": {"x": 0.2}}))
            self.assertEqual(decided.comes_back(body, path)["differ"], ["arms"])


class TestTheRecord(unittest.TestCase):

    def test_exact_fractions_stay_out_of_the_record(self):
        got = decided.plain({"a": {"declared": {"fraction": "1/2", "value": 0.5},
                                   "declared_exact": Fraction(1, 2)}, "b": [{"x_exact": 1}]})
        self.assertEqual(got, {"a": {"declared": {"fraction": "1/2", "value": 0.5}},
                               "b": [{}]})

    def test_the_lines_are_the_plan_s(self):
        self.assertEqual(decided.D2_LINE, plan.RL_E_LINE)
        self.assertEqual(decided.D1_LINE, Fraction(1, 2))


class TestUnsigned(unittest.TestCase):

    def test_it_refuses_before_reading_or_writing(self):
        for argv in ([], ["--dry-run"]):
            with self.subTest(argv=argv), \
                 mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                 mock.patch.object(Path, "read_text",
                                   side_effect=AssertionError("read")) as read, \
                 mock.patch.object(Path, "write_text",
                                   side_effect=AssertionError("wrote")) as write:
                with self.assertRaises(SystemExit):
                    decided.main(argv)
                read.assert_not_called()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
