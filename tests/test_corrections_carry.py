"""
`corrections/carry.py` — the POST-RUN reading of how much of the fall the doors
carry, no figure.

What is pinned is the instrument, on one run built by hand over the real space.
Its gateway `G` is a rule of `T2_TECHNICAL` nested in the keyword's rule `U`, and
two doors declared themselves above it:
- `D`, of `ACCOUNT_MANAGER`, whose loss to `U` the record refuses for the cycle
  its own win closes;
- `N`, of `BILLING_SPECIALIST`, above `D`, whose loss to `U` the record refuses
  through `D`;
- `D2`, of `T1_GENERAL`, a second door, refused its loss the same way;
- `M`, above `D2`, refused its loss through it.
Also pinned:
- the replay in the record's order, and with edges left out: each edge it
  tried and what the engine did, and the first edge left out;
- the edges whose verdict differs from the record's, the right sides installed
  and the new doors;
- the doors' edges and the climbs a run gives;
- the five gates on that run, and each failing on its own;
- the expectation's clauses at their edges, pooled, on one door, and over
  nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run, on masks built by hand and on the same run: where a
replay's final base decides otherwise than the record's order, the record
against itself deciding nothing otherwise.
"""

from __future__ import annotations

import unittest
from unittest import mock

from corrections import carry as C
from corrections import fall as fl
from corrections import gateway as gw
from corrections import plan
from harness.ceiling_check import all_cases
from reuse import structure as st
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, Space

SPACE = Space()
CASES = list(all_cases())
T1, T2 = "T1_GENERAL", "T2_TECHNICAL"
BI, AM, SEC = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SECURITY_INCIDENT"
IMP, ERR = plan.IMPASSE, plan.ERROR
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

M_ = SPACE.mask
KW, NOKW = M_["has_security_keyword"][True], M_["has_security_keyword"][False]
SMALL = M_["customer_tier"]["free"] | M_["customer_tier"]["pro"]
LOW = M_["severity"][3] | M_["severity"][4]
BILLING, BUSINESS = M_["product"]["billing"], M_["customer_tier"]["business"]
# The keyword's low-severity tickets of small accounts are T2's, as at H03.
TRUTH = {T2: KW & SMALL & LOW, SEC: KW & ~(SMALL & LOW), BI: NOKW & BILLING,
         AM: NOKW & ~BILLING & BUSINESS, T1: NOKW & ~BILLING & ~BUSINESS}


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(rid, born, action, conds):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": [], "loses_to": [], "dropped_edges": []}


KEYWORD = c_("has_security_keyword", "eq", True)
BIRTHS = [
    (IMP, r_("U", 0, SEC, [KEYWORD])),
    (ERR, r_("G", 1, T2, [KEYWORD, c_("severity", "eq", 4)])),
    (IMP, r_("D", 2, AM, [c_("customer_tier", "eq", "business")])),
    (ERR, r_("N", 3, BI, [c_("product", "eq", "billing")])),
    (IMP, r_("D2", 4, T1, [c_("channel", "eq", "chat")])),
    (ERR, r_("M", 5, BI, [c_("language", "eq", "pt")])),
]
# Each birth's wins before its losses, with the record's verdicts.
EDGES = [(2, "D", "G"), (2, "U", "D", EDGE_CYCLE), (3, "N", "D"), (3, "U", "N", EDGE_CYCLE),
         (4, "D2", "G"), (4, "U", "D2", EDGE_CYCLE), (5, "M", "D2"),
         (5, "U", "M", EDGE_CYCLE)]


def record(births=None, edges=None):
    births = births or BIRTHS
    rows = [{"idx": i, "edge_reasons": [], "truth_rule": "H29"} for i in range(len(births))]
    log = []
    for born, w, l, *why in (edges if edges is not None else EDGES):
        reason = why[0] if why else EDGE_OK
        rows[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    return {"rules": [rule for _, rule in births], "records": rows, "edge_log": log,
            "escalations": [{"idx": rule["born_at"], "kind": cause, "listed": []}
                            for cause, rule in births]}


def gateway_run(gates=("G",), doors=(("D", "G"), ("D2", "G"))):
    born = {r["rule_id"]: r for _, r in BIRTHS}
    return {"gateways": [{"rule_id": g, "born_at": born[g]["born_at"]} for g in gates],
            "doors": [{"door": d, "gateway": g, "kind": gw.DOOR_WIN} for d, g in doors]}


def doors_run(climbs=(("D", "G"), ("D2", "G"))):
    return {"listings": [{"newborn": n, "gateway": g, "side": "climb"} for n, g in climbs]
            + [{"newborn": "N", "gateway": "G", "side": "cede"}]}


def fall_run(rec=None):
    """What `fall.json` keeps of the run: `fall.py`'s curve, and its record order."""
    rec = rec or record()
    steps = fl.replay(rec, SPACE, TRUTH, CASES)["steps"]
    got = fl.order_replay(rec, SPACE, TRUTH, False)
    return {"curve": [{"right": s["right"].bit_count()} for s in steps],
            "added_after_the_first_run": {"orders": {"declared": st._rounded(
                fl.order_summary(got, TRUTH, SPACE.n))}}}


FALL = fall_run()


def read(rec=None, grun=None, drun=None, frun=None):
    return C.read_run(rec or record(), SPACE, TRUTH, grun or gateway_run(), drun or doors_run(),
                      frun or FALL)


def gate(run, k):
    return next(g["passes"] for g in run["gates"] if g["gate"] == k)


def installed(got):
    return [(t["winner"], t["loser"]) for t in got["tried"] if t["installed"]]


class TestTheReplay(unittest.TestCase):

    def test_the_records_order(self):
        got = C.replay(record(), SPACE, TRUTH)
        self.assertEqual(installed(got), [("D", "G"), ("N", "D"), ("D2", "G"), ("M", "D2")])
        self.assertEqual(got["cycles"], 4)
        self.assertIsNone(got["first_skip"])
        self.assertTrue(got["masks_ok"])
        self.assertEqual(len(got["curve"]), len(BIRTHS))
        self.assertEqual(got["curve"], [s["right"] for s in FALL["curve"]])

    def test_without_the_doors_the_right_sides_go_in(self):
        got = C.replay(record(), SPACE, TRUTH, frozenset({("D", "G"), ("D2", "G")}))
        self.assertEqual(installed(got), [("U", "D"), ("N", "D"), ("U", "N"), ("U", "D2"),
                                          ("M", "D2"), ("U", "M")])
        self.assertEqual(got["first_skip"], 2)
        self.assertEqual(got["cycles"], 0)

    def test_one_door_left_out(self):
        got = C.replay(record(), SPACE, TRUTH, frozenset({("D", "G")}))
        self.assertEqual(installed(got), [("U", "D"), ("N", "D"), ("U", "N"), ("D2", "G"),
                                          ("M", "D2")])
        self.assertEqual(got["cycles"], 2)

    def test_what_differs_from_the_record(self):
        base = C.replay(record(), SPACE, TRUTH)
        got = C.replay(record(), SPACE, TRUTH, frozenset({("D", "G"), ("D2", "G")}))
        self.assertEqual(C.against(base, got, {"G"}), {
            "refused_there_installed_here": 4, "installed_there_refused_here": 0,
            "right_sides_installed": 4, "new_doors": []})
        self.assertEqual(C.against(base, base, {"G"})["refused_there_installed_here"], 0)

    def test_a_climb_refused_there_and_installed_here_is_a_new_door(self):
        base = {"action": {"U": SEC, "C": AM}, "tried": [
            {"born_at": 7, "newborn": "C", "winner": "C", "loser": "G", "verdict": EDGE_CYCLE,
             "installed": False},
            {"born_at": 7, "newborn": "C", "winner": "C", "loser": "X", "verdict": EDGE_OK,
             "installed": True}]}
        got = {"tried": [
            {"born_at": 7, "newborn": "C", "winner": "C", "loser": "G", "verdict": EDGE_OK,
             "installed": True},
            {"born_at": 7, "newborn": "C", "winner": "C", "loser": "X", "verdict": EDGE_CYCLE,
             "installed": False}]}
        self.assertEqual(C.against(base, got, {"G"}), {
            "refused_there_installed_here": 1, "installed_there_refused_here": 1,
            "right_sides_installed": 0, "new_doors": [["C", "G"]]})


class TestWhatIsLeftOut(unittest.TestCase):

    def test_the_doors_edges(self):
        grun = gateway_run()
        grun["doors"].append({"door": "R", "gateway": "G", "kind": gw.NESTED})
        self.assertEqual(C.door_edges(grun), [("D", "G"), ("D2", "G")])

    def test_the_climbs(self):
        self.assertEqual(C.climb_edges(record(), {"G": 1}), [("D", "G"), ("D2", "G")])
        self.assertEqual(C.climb_edges(record(), {"G": 4}), [])
        self.assertEqual(C.climb_edges(record(), {}), [])


class TestTheRun(unittest.TestCase):

    def setUp(self):
        self.run = read()

    def test_the_doors_keep_what_the_record_lost(self):
        rec, doors = self.run["summary"]["record"], self.run["replays"][C.DOORS]
        self.assertGreater(rec["fall_points"], 0)
        self.assertGreater(doors["kept"]["points"], 0)
        self.assertEqual(doors["kept"]["points"],
                         doors["final"]["right"] - rec["final"]["right"])
        self.assertEqual(doors["right_sides_installed"], 4)
        self.assertEqual(doors["left_out"], [["D", "G"], ["D2", "G"]])

    def test_the_climbs_replay_is_the_doors_here(self):
        self.assertEqual(self.run["replays"][C.CLIMBS]["final"],
                         self.run["replays"][C.DOORS]["final"])

    def test_one_replay_per_door(self):
        doors = self.run["doors"]
        self.assertEqual(sorted(doors), ["D", "D2"])
        self.assertEqual(doors["D"]["left_out"], [["D", "G"]])
        self.assertEqual(doors["D"]["right_sides_installed"], 2)
        self.assertEqual(doors["D2"]["right_sides_installed"], 2)

    def test_a_run_without_a_gateway_leaves_nothing_out(self):
        run = read(grun=gateway_run(gates=(), doors=()), drun=doors_run(climbs=()))
        self.assertEqual(run["replays"][C.DOORS]["kept"]["points"], 0)
        self.assertEqual(run["doors"], {})
        self.assertTrue(gate(run, 5))


class TestTheGates(unittest.TestCase):

    def test_they_pass_on_the_run(self):
        run = read()
        self.assertEqual([g["gate"] for g in run["gates"]], [1, 2, 3, 4, 5])
        self.assertTrue(all(g["passes"] for g in run["gates"]))

    def test_1_fails_on_another_curve(self):
        frun = fall_run()
        frun["curve"][3]["right"] += 1
        self.assertFalse(gate(read(frun=frun), 1))

    def test_1_fails_on_another_final(self):
        frun = fall_run()
        frun["added_after_the_first_run"]["orders"]["declared"]["refused_for_a_cycle"] += 1
        self.assertFalse(gate(read(frun=frun), 1))

    def test_2_fails_on_a_door_edge_the_record_did_not_install(self):
        self.assertFalse(gate(read(grun=gateway_run(doors=(("D", "G"), ("U", "N")))), 2))

    def test_2_fails_on_other_climbs(self):
        self.assertFalse(gate(read(drun=doors_run(climbs=(("D", "G"),))), 2))

    def test_3_fails_on_a_replay_that_differs_before_its_first_edge_left_out(self):
        real = C.replay

        def shifted(rec, space, truth, skip=frozenset()):
            got = real(rec, space, truth, skip)
            if skip:
                got["curve"] = [got["curve"][0] + 1] + got["curve"][1:]
            return got

        with mock.patch.object(C, "replay", side_effect=shifted):
            self.assertFalse(gate(read(), 3))

    def test_4_fails_on_masks_that_are_not_the_engines(self):
        real = C.replay

        def broken(rec, space, truth, skip=frozenset()):
            got = real(rec, space, truth, skip)
            got["masks_ok"] = not skip
            return got

        with mock.patch.object(C, "replay", side_effect=broken):
            self.assertFalse(gate(read(), 4))

    def test_5_fails_on_a_run_without_a_gateway_that_leaves_an_edge_out(self):
        self.assertFalse(gate(read(grun=gateway_run(gates=())), 5))


def run_of(kept, fall, doors=None):
    return {"summary": {"record": {"fall_points": fall}},
            "replays": {C.DOORS: {"kept": {"points": kept}}},
            "doors": {d: {"kept": {"points": k}} for d, k in (doors or {}).items()}}


def clauses(runs):
    return {c["clause"]: c["holds"] for c in C.read_expectation(runs)}


ALL = ["C1", "C2", "C3", "C4", "C5", "C6"]
L1, L2, L3, N3 = "l_r1", "l_r2", "l_r3", "n_r3"


class TestTheExpectation(unittest.TestCase):

    def test_the_constants(self):
        self.assertEqual(C.L_RUNS, (L1, L2, L3))
        self.assertEqual((C.C5_RUN, C.C5_DOOR, C.C6_RUN), (L2, "R0051", N3))

    def test_every_clause_holds_at_its_line(self):
        runs = {L1: run_of(75, 100), L2: run_of(50, 100, {"R0051": 25}),
                L3: run_of(25, 100), N3: run_of(25, 100)}
        self.assertEqual(clauses(runs), {k: True for k in ALL})
        runs[L1] = run_of(50, 100)
        self.assertFalse(clauses(runs)["C4"])

    def test_every_clause_fails_past_its_line(self):
        runs = {L1: run_of(49, 100), L2: run_of(49, 100, {"R0051": 24}),
                L3: run_of(26, 100), N3: run_of(24, 100)}
        got = clauses(runs)
        self.assertEqual({k: got[k] for k in ("C1", "C2", "C3", "C5", "C6")},
                         {k: False for k in ("C1", "C2", "C3", "C5", "C6")})

    def test_c4_pools_the_three_l_runs(self):
        runs = {L1: run_of(100, 100), L2: run_of(0, 100, {"R0051": 0}), L3: run_of(50, 100),
                N3: run_of(0, 100)}
        self.assertTrue(clauses(runs)["C4"])
        runs[L3] = run_of(49, 100)
        self.assertFalse(clauses(runs)["C4"])

    def test_c3_holds_on_a_run_that_kept_less_than_nothing(self):
        runs = {L3: run_of(-30, 100)}
        self.assertTrue(clauses(runs)["C3"])

    def test_c5_needs_something_kept(self):
        runs = {L2: run_of(0, 100, {"R0051": 0})}
        self.assertFalse(clauses(runs)["C5"])
        runs = {L2: run_of(-10, 100, {"R0051": -5})}
        self.assertFalse(clauses(runs)["C5"])

    def test_a_clause_over_nothing_fails(self):
        got = clauses({})
        self.assertEqual({k: got[k] for k in ALL}, {k: False for k in ALL})


class TestAddedAfterTheFirstRun(unittest.TestCase):
    """Where a replay's final base decides otherwise than the record's order."""

    def test_on_masks_built_by_hand(self):
        # Four points. The record leaves point 1 in a conflict of X and Y; the
        # replay gives it to X, whose queue is not its truth.
        base = {"und": {"A": 0b0011, "B": 0b0110}, "action": {"A": "X", "B": "Y"}}
        got = {"und": {"A": 0b0011, "B": 0b0100}, "action": {"A": "X", "B": "Y"}}
        truth = {"X": 0b0001, "Y": 0b0110, SEC: 0b1000}
        self.assertEqual(C.where(base, got, truth), {
            "gained": 0, "lost": 0, "gained_security": 0, "lost_security": 0,
            "wrong_to_wrong": 1, "conflicts_resolved": 1, "resolved_wrongly": 1,
            "resolved_wrongly_by_queue": {"X:Y": 1}, "decided_to_conflict": 0})
        self.assertEqual(C.where(got, base, truth)["decided_to_conflict"], 1)

    def test_on_the_run(self):
        run = read()
        got = run["replays"][C.DOORS]["added_after_the_first_run"]
        self.assertEqual(got["gained"] - got["lost"], run["replays"][C.DOORS]["kept"]["points"])
        self.assertGreater(got["gained_security"], 0)
        self.assertEqual(sum(got["resolved_wrongly_by_queue"].values()), got["resolved_wrongly"])
        self.assertLessEqual(got["resolved_wrongly"], got["conflicts_resolved"])

    def test_the_record_against_itself(self):
        base = C.replay(record(), SPACE, TRUTH)
        got = C.where(base, base, TRUTH)
        self.assertEqual(got["resolved_wrongly_by_queue"], {})
        self.assertEqual({k: v for k, v in got.items() if k != "resolved_wrongly_by_queue"},
                         {k: 0 for k in got if k != "resolved_wrongly_by_queue"})

    def test_it_moves_no_gate(self):
        self.assertEqual([g["gate"] for g in read()["gates"]], [1, 2, 3, 4, 5])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(C, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                C.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
