"""
`corrections/gateway.py` — the POST-RUN reading of why so many rules sit above
the gateway, no figure.

What is pinned is the instrument, on one run built by hand over the real space,
read as `corrections/fall.py` and `corrections/paths.py` read it first. Its
gateway is a rule of `T2_TECHNICAL` nested in the keyword's rule, born at a
ticket of `H03`, and it has a rule above it of every entry and a door of every
kind:
- a rule of `ACCOUNT_MANAGER` the gateway's answer put above it, and a rule
  nested inside it, both born before it;
- a rule of `ACCOUNT_MANAGER` that declared itself above it, and a rule nested
  inside that one;
- a rule above that one by its own declared win;
- a rule whose declared win puts it above that one, and that brings up an older
  rule it declared itself below, and an older rule nested inside it;
- two newborns refused their right side against the keyword's rule, one that
  shares no point with the gateway and one that does.
Also pinned:
- the gateways a run gives, what reaches them, the depths, the distance and
  the entry of a rule;
- the six gates on that run, and each failing on its own;
- the expectation's clauses at their edges, and over nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run, on the same run with its rounds' lists: what an
answer declared, the gateway's and the doors' answers, every round that listed
the gateway by what its answer declared of it, and every round.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import fall as fl
from corrections import gateway as GW
from corrections import paths as pt
from corrections import plan
from edges import rebuild as erb
from fidelity.replay import rule_from
from harness.ceiling_check import all_cases
from harness.domain import Case
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, PriorityEngine, Space

F = Fraction
SPACE = Space()
CASES = list(all_cases())
N_POINTS = SPACE.n
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BI, AM, SEC = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SECURITY_INCIDENT"
OC, SS = "ONCALL_ESCALATION", "SELF_SERVICE_DEFLECT"
IMP, ERR = plan.IMPASSE, plan.ERROR
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}

KW = SPACE.mask["has_security_keyword"][True]
NOKW = SPACE.mask["has_security_keyword"][False]
SMALL = SPACE.mask["customer_tier"]["free"] | SPACE.mask["customer_tier"]["pro"]
LOW = SPACE.mask["severity"][3] | SPACE.mask["severity"][4]
# The keyword's low-severity tickets of small accounts are T2's, as at H03.
TRUTH = {T2: KW & SMALL & LOW, SEC: KW & ~(SMALL & LOW), T1: NOKW}


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


def r_(rid, born, action, conds, beats=(), loses_to=(), refused=()):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to),
            "dropped_edges": [f"loses_to:{x}:{EDGE_CYCLE}" for x in refused]}


KEYWORD = c_("has_security_keyword", "eq", True)
CHAT = c_("channel", "eq", "chat")

RUN = {
    "births": [
        (IMP, r_("U", 0, SEC, [KEYWORD])),
        (IMP, r_("T", 1, T1, [c_("has_security_keyword", "eq", False)])),
        (IMP, r_("P", 2, AM, [c_("customer_tier", "eq", "enterprise")])),
        (IMP, r_("Y", 3, BI, [KEYWORD, c_("severity", "eq", 4), CHAT])),
        (ERR, r_("X", 4, T2, [KEYWORD, c_("severity", "gte", 3)], loses_to=["P"])),
        (IMP, r_("W", 5, AM, [CHAT], beats=["X"])),
        (IMP, r_("V", 6, BI, [c_("product", "eq", "api"), CHAT])),
        (IMP, r_("S", 7, T3, [c_("product", "eq", "mobile")], beats=["W"])),
        (IMP, r_("R", 8, SS, [c_("product", "eq", "billing"), c_("customer_tier", "eq", "free")])),
        (ERR, r_("B", 9, BI, [c_("product", "eq", "billing")], beats=["W"], loses_to=["T"])),
        (ERR, r_("N", 10, OC, [c_("severity", "eq", 1), c_("off_hours", "eq", True)],
                 beats=["W"], refused=["U"])),
        (ERR, r_("M", 11, BI, [c_("language", "eq", "pt")], beats=["W"], refused=["U"])),
    ],
    "edges": [(4, "P", "X"), (5, "W", "X"), (7, "S", "W"), (9, "B", "W"), (9, "T", "B"),
              (10, "N", "W"), (10, "U", "N", EDGE_CYCLE), (11, "M", "W"),
              (11, "U", "M", EDGE_CYCLE)],
    "h03": {4},
}


def ticket():
    return Case(has_security_keyword=False, severity=3, customer_tier="free",
                product="api", channel="portal", prior_tickets_30d=0, off_hours=False,
                language="en")


def record(run, edges=None, listed=None):
    births = run["births"]
    rows = [{"idx": i, "edge_reasons": [],
             "truth_rule": "H03" if i in run["h03"] else "H29"} for i in range(len(births))]
    log = []
    for born, w, l, *why in (edges if edges is not None else run["edges"]):
        reason = why[0] if why else EDGE_OK
        rows[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    listed = listed or {}
    return {"rules": [rule for _, rule in births], "records": rows, "edge_log": log,
            "escalations": [{"idx": rule["born_at"], "kind": cause, "verdict": "nacida",
                             "rule_id": rule["rule_id"],
                             "listed": listed.get(rule["born_at"], [])}
                            for cause, rule in births]}


def final_of(rec):
    return erb.rebuild(rec, [ticket() for _ in rec["rules"]], SPACE).engine


def paths_run(rec):
    """`corrections/paths.py`'s reading of the run, read on `corrections/fall.py`'s,
    as `paths.json` keeps it."""
    final = final_of(rec)
    steps = fl.replay(rec, SPACE, TRUTH, CASES)["steps"]
    share = {"space": {"fraction": str(F(steps[-1]["right"].bit_count(), N_POINTS))}}
    fall = fl.read_run(rec, SPACE, TRUTH, CASES, share, final=final)
    return pt.read_run(rec, SPACE, TRUTH, CASES, fall, final=final)


def read(rec=None, paths=None, final_rec=None):
    rec = rec or record(RUN)
    return GW.read_run(rec, SPACE, TRUTH, CASES, paths or paths_run(rec),
                       final=final_of(final_rec or rec))


def gate(got, k):
    return next(g for g in got["gates"] if g["gate"] == k)["passes"]


def engine_of(rec, upto=None):
    engine = PriorityEngine(space=SPACE)
    born, by_birth = erb.births(rec), erb.edges_by_birth(rec)
    for idx in sorted(born):
        if upto is not None and idx > upto:
            break
        engine.add(rule_from(born[idx]), born_at=idx, keep_id=True)
        for e in by_birth.get(idx, []):
            engine.try_edge(e.winner, e.loser)
    return engine


class TestTheGateways(unittest.TestCase):

    def test_the_gateways_are_the_rules_above_even_crossings_born_at_h03(self):
        rules = [{"rule_id": "A", "action": T2, "born_at": 9, "ticket_rule": "H03"},
                 {"rule_id": "B", "action": SEC, "born_at": 3, "ticket_rule": "H03"},
                 {"rule_id": "C", "action": BI, "born_at": 5, "ticket_rule": "H12"},
                 {"rule_id": "D", "action": T1, "born_at": 4, "ticket_rule": "H03"}]
        got = GW.gateways_of({"added_after_the_first_run": {"rules_above_even": rules}})
        self.assertEqual([g["rule_id"] for g in got], ["D", "A"])

    def test_the_run_s_gateway_is_its_nested_rule_of_t2(self):
        got = paths_run(record(RUN))
        self.assertEqual([g["rule_id"] for g in GW.gateways_of(got)], ["X"])


class TestTheGraph(unittest.TestCase):

    def setUp(self):
        self.engine = engine_of(record(RUN))

    def test_what_reaches_the_gateway(self):
        self.assertEqual(GW.above(self.engine, ["X"]),
                         {"P", "Y", "W", "V", "S", "R", "B", "T", "N", "M"})
        self.assertEqual(GW.above(self.engine, ["X"], {("W", "X")}), {"P", "Y"})
        self.assertEqual(GW.above(self.engine, ["W", "X"]),
                         {"P", "Y", "V", "S", "R", "B", "T", "N", "M"})

    def test_the_depths(self):
        got = GW.depths(self.engine, ["X"])
        self.assertEqual(got, {"X": 0, "P": 1, "Y": 1, "W": 1, "V": 2, "S": 2, "B": 2,
                               "N": 2, "M": 2, "T": 3, "R": 3})

    def test_the_distance(self):
        self.assertEqual(GW.distance(self.engine, "T", {"X"}), 3)
        self.assertEqual(GW.distance(self.engine, "X", {"X"}), 0)
        self.assertIsNone(GW.distance(self.engine, "U", {"X"}))

    def test_the_entry_of_a_rule(self):
        engine = engine_of(record(RUN), upto=9)
        now = GW.above(engine, ["X"])
        self.assertEqual(GW.entry_of(engine, "B", "B", ["X"], now), {"class": GW.OWN_WINS})
        self.assertEqual(GW.entry_of(engine, "T", "B", ["X"], now),
                         {"class": GW.BROUGHT, "through": GW.BY_LOSSES, "bridge": "B"})
        self.assertEqual(GW.entry_of(engine, "R", "B", ["X"], now),
                         {"class": GW.BROUGHT, "through": GW.BY_REGION, "bridge": "B"})
        self.assertEqual(GW.entry_of(engine, "U", "B", ["X"], now), {"class": GW.OTHER})


class TestTheRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.got = read()

    def test_all_six_gates_pass(self):
        self.assertEqual([g["passes"] for g in self.got["gates"]], [True] * 6)

    def test_the_rules_above_and_their_entries(self):
        s = self.got["summary"]
        self.assertEqual((s["gateways"], s["first_gateway_born_at"], s["rules"]), (["X"], 4, 12))
        self.assertEqual((s["born_after"], s["above"], s["above_born_after"]), (7, 10, 7))
        self.assertEqual(s["entries"], {GW.CONTAINMENT: 1, GW.OWN_WINS: 5, GW.BROUGHT: 2,
                                        GW.AT_GATEWAY: 2})
        self.assertEqual(s["through"], {"at_gateway:by_losses": 1, "at_gateway:by_region": 1,
                                        "brought:by_losses": 1, "brought:by_region": 1})
        self.assertEqual(s["depth"], {"1": 3, "2": 5, "3": 2})
        self.assertEqual(s["above_by_queue"], {AM: 2, BI: 4, T3: 1, SS: 1, T1: 1, OC: 1})
        e = self.got["entries"]
        self.assertEqual({x: (v["class"], v.get("through"), v.get("bridge"), v["at"])
                          for x, v in e.items()},
                         {"P": (GW.AT_GATEWAY, GW.BY_LOSSES, "X", 4),
                          "Y": (GW.AT_GATEWAY, GW.BY_REGION, "X", 4),
                          "W": (GW.OWN_WINS, None, None, 5),
                          "V": (GW.CONTAINMENT, None, None, 6),
                          "S": (GW.OWN_WINS, None, None, 7),
                          "B": (GW.OWN_WINS, None, None, 9),
                          "T": (GW.BROUGHT, GW.BY_LOSSES, "B", 9),
                          "R": (GW.BROUGHT, GW.BY_REGION, "B", 9),
                          "N": (GW.OWN_WINS, None, None, 10),
                          "M": (GW.OWN_WINS, None, None, 11)})
        self.assertEqual(self.got["curve"], [[4, 2], [5, 3], [6, 4], [7, 5], [8, 5], [9, 8],
                                             [10, 9], [11, 10]])

    def test_the_doors(self):
        got = [(d["door"], d["kind"], d["installed_at"], d["verdict"], d["carries"], d["alone"])
               for d in self.got["doors"]]
        self.assertEqual(got, [("P", GW.GATEWAY_LOSS, 4, pt.EVEN, 1, 1),
                               ("W", GW.DOOR_WIN, 5, pt.WRONG, 9, 8),
                               ("Y", GW.NESTED, None, pt.WRONG, 1, 0)])
        self.assertEqual(self.got["summary"]["doors"]["edges"],
                         {GW.NESTED: 1, GW.GATEWAY_LOSS: 1, GW.DOOR_WIN: 1})

    def test_the_rules_each_birth_brought(self):
        got = [(b["bridge"], b["entry"], b["brought"], b[GW.BY_LOSSES], b[GW.BY_REGION])
               for b in self.got["bridges"]]
        self.assertEqual(got, [("X", None, 2, 1, 1), ("B", GW.OWN_WINS, 2, 1, 1)])

    def test_the_pairs_through_the_gateway(self):
        s = self.got["summary"]["pairs"]
        self.assertEqual(s, {"pairs": 2, "points": 2835 + 1701, "meets": 1701, "misses": 2835,
                             "distance": {"2": 2835 + 1701}})
        got = [(nb["newborn"], nb["meets"], nb["distance"], nb["wins"], nb["wins_above"],
                nb["nearest_win"], nb["above_then"], nb["doors_then"], nb["points"])
               for nb in self.got["newborns"]]
        self.assertEqual(got, [("N", False, 2, 1, 1, 1, 9, 3, 2835),
                               ("M", True, 2, 1, 1, 1, 10, 3, 1701)])

    def test_what_the_newborn_s_answer_said_of_the_gateway(self):
        """M meets the gateway, is listed it, and declares itself below it: the
        edge closes the same cycle, and decides none of the pair's points."""
        births = list(RUN["births"])
        births[11] = (ERR, r_("M", 11, BI, [c_("language", "eq", "pt")], beats=["W"],
                              refused=["U", "X"]))
        run = {**RUN, "births": births, "edges": RUN["edges"] + [(11, "X", "M", EDGE_CYCLE)]}
        got = read(record(run, listed={11: ["U", "X"]}))
        self.assertEqual([g["passes"] for g in got["gates"]], [True] * 6)
        nb = next(x for x in got["newborns"] if x["newborn"] == "M")
        self.assertEqual((nb["said"], nb["listed"]),
                         ({"X": ["loses_to", EDGE_CYCLE]}, {"X": True}))
        nb = next(x for x in got["newborns"] if x["newborn"] == "N")
        self.assertEqual((nb["said"], nb["listed"]), ({"X": None}, {"X": False}))


class TestTheGates(unittest.TestCase):

    def test_gate_1_fails_on_another_base(self):
        got = read(final_rec=record(RUN, edges=RUN["edges"][1:]))
        self.assertFalse(gate(got, 1))
        self.assertTrue(all(gate(got, k) for k in (2, 3, 4, 5, 6)))

    def test_gate_2_fails_off_paths_json_s_pairs(self):
        paths = paths_run(record(RUN))
        paths["pairs"][0]["points"] += 1
        self.assertFalse(gate(read(paths=paths), 2))

    def test_gate_2_fails_on_a_gateway_off_the_keyword(self):
        paths = paths_run(record(RUN))
        g = paths["added_after_the_first_run"]["rules_above_even"][0]
        g["conditions"] = g["conditions"][1:]
        self.assertFalse(gate(read(paths=paths), 2))

    def test_gate_3_fails_on_an_edge_without_the_newborn(self):
        edges = RUN["edges"][:5] + [(9, "V", "P")] + RUN["edges"][5:]
        rec = record(RUN, edges=edges)
        self.assertFalse(gate(read(rec=rec, paths=paths_run(record(RUN))), 3))

    def test_gate_4_fails_when_a_rule_leaves(self):
        above = GW.above
        calls = []

        def shrinking(engine, gates, skip=None):
            got = above(engine, gates, skip)
            calls.append(1)
            return got - {"P"} if len(calls) == 3 else got

        with mock.patch.object(GW, "above", side_effect=shrinking):
            got = read()
        self.assertFalse(gate(got, 4))

    def test_gate_5_fails_when_a_newborn_does_not_reach_its_gateway(self):
        with mock.patch.object(GW, "distance", return_value=None):
            got = read()
        self.assertFalse(gate(got, 5))
        self.assertTrue(all(gate(got, k) for k in (1, 2, 3, 4, 6)))

    def test_gate_6_fails_on_an_entry_outside_the_classes(self):
        entry_of = GW.entry_of

        def unclassed(engine, x, *a, **k):
            got = entry_of(engine, x, *a, **k)
            return {"class": GW.OTHER} if x == "S" else got

        with mock.patch.object(GW, "entry_of", side_effect=unclassed):
            got = read()
        self.assertFalse(gate(got, 6))
        self.assertTrue(all(gate(got, k) for k in (1, 2, 3, 4, 5)))


class TestWhatTheAnswersDeclared(unittest.TestCase):
    """Added after the first run."""

    @classmethod
    def setUpClass(cls):
        births = list(RUN["births"])
        births[11] = (ERR, r_("M", 11, BI, [c_("language", "eq", "pt")], beats=["W"],
                              refused=["U", "X"]))
        run = {**RUN, "births": births, "edges": RUN["edges"] + [(11, "X", "M", EDGE_CYCLE)]}
        cls.got = read(record(run, listed={4: ["P"], 5: ["X"], 9: ["W", "T", "X"],
                                           10: ["U", "W"], 11: ["U", "X"]}))
        cls.answers = cls.got["added_after_the_first_run"]["answers"]

    def test_the_sides_of_one_answer(self):
        rule = r_("M", 11, BI, [], beats=["W"], loses_to=["T"], refused=["U", "X"])
        self.assertEqual(GW.sides(rule), {"wins": 1, "losses": 3,
                                          "by_verdict": {"beats:ok": 1, "loses_to:ok": 1,
                                                         f"loses_to:{EDGE_CYCLE}": 2}})

    def test_the_gateway_s_and_the_doors_answers(self):
        self.assertEqual([(a["rule_id"], a["listed"], a["wins"], a["losses"])
                          for a in self.answers["gateways"]], [("X", 1, 0, 1)])
        self.assertEqual([(a["rule_id"], a["listed"], a["wins"], a["losses"])
                          for a in self.answers["doors"]],
                         [("P", 0, 0, 0), ("Y", 0, 0, 0), ("W", 1, 1, 0)])

    def test_every_round_that_listed_the_gateway(self):
        self.assertEqual(self.answers["rounds_that_listed_a_gateway"],
                         {"beats:ok": 1, f"loses_to:{EDGE_CYCLE}": 1, "none:none": 1})

    def test_every_round(self):
        self.assertEqual(self.answers["every_round"],
                         {"rounds": 5, "wins": 4, "losses": 5, "without_a_loss": 1,
                          "by_verdict": {"beats:ok": 4, "loses_to:ok": 2,
                                         f"loses_to:{EDGE_CYCLE}": 3}})

    def test_it_moves_nothing_else(self):
        self.assertEqual([g["passes"] for g in self.got["gates"]], [True] * 6)
        self.assertEqual(self.got["summary"]["entries"], read()["summary"]["entries"])


def summary(born_after=100, above_born_after=50, above=100, own=50, deep=50,
            gateway_loss=5, door_win=5, points=100, misses=50):
    return {"born_after": born_after, "above_born_after": above_born_after, "above": above,
            "entries": {GW.OWN_WINS: own},
            "depth": {"1": above - deep, "2": deep},
            "doors": {"edges": {GW.NESTED: 3, GW.GATEWAY_LOSS: gateway_loss,
                                GW.DOOR_WIN: door_win}},
            "pairs": {"points": points, "misses": misses}}


def clauses(l_runs, n3=None):
    runs = {plan.tag(plan.LABELLED, k): {"summary": s} for k, s in enumerate(l_runs, start=1)}
    if n3 is not None:
        runs[GW.D6_RUN] = {"summary": n3}
    return {c["clause"]: c["holds"] for c in GW.read_expectation(runs)}


ALL = ("D1", "D2", "D3", "D4", "D5", "D6")


class TestTheExpectation(unittest.TestCase):

    def test_every_clause_holds_at_its_line(self):
        self.assertEqual(clauses([summary()] * 3, summary()), {k: True for k in ALL})

    def test_d1_to_d5_pool_l_s_runs(self):
        low = summary(above_born_after=49, own=49, deep=49, door_win=4, misses=49)
        got = clauses([low, summary(), summary()], summary())
        self.assertEqual([got[k] for k in ALL[:5]], [False] * 5)
        high = summary(above_born_after=51, own=51, deep=51, door_win=6, misses=51)
        got = clauses([low, high, summary()], summary())
        self.assertEqual([got[k] for k in ALL[:5]], [True] * 5)

    def test_d4_leaves_the_nested_doors_out(self):
        self.assertTrue(clauses([summary(gateway_loss=5, door_win=5)] * 3, summary())["D4"])
        self.assertFalse(clauses([summary(gateway_loss=6, door_win=5)] * 3, summary())["D4"])

    def test_d6_reads_n_r3_alone(self):
        self.assertFalse(clauses([summary()] * 3, summary(above_born_after=49))["D6"])
        self.assertFalse(clauses([summary()] * 3)["D6"])

    def test_a_clause_over_nothing_fails(self):
        nothing = summary(born_after=0, above_born_after=0, above=0, own=0, deep=0,
                          gateway_loss=0, door_win=0, points=0, misses=0)
        self.assertEqual(clauses([nothing] * 3, nothing), {k: False for k in ALL})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(GW, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                GW.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
