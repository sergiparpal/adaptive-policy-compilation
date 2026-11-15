"""
`corrections/doors.py` — the POST-RUN reading of why the doors declared
themselves above the gateway, no figure.

What is pinned is the instrument, on one run built by hand over the real space.
Its gateway is a rule of `T2_TECHNICAL` nested in the keyword's security rule,
and its rounds that listed it hold an answer of every kind:
- a climb the engine installed, above the gateway and above another keyword
  rule of another queue, below the security rule, its loss refused;
- a climb refused for a cycle, read the same way;
- a climb above the security rule and below the other keyword rule;
- a cede below every keyword rule, whose ticket lies inside the gateway;
- a cede refused for a cycle, above the other keyword rule;
- a cede whose round listed no other keyword rule;
- a round after the gateway that did not list it.
Also pinned:
- a rule's region, a keyword rule, a ticket's point, and what an answer did with
  a set of rules;
- the listings, a round that listed two gateways counted once for each, and
  every placement by kind;
- the five gates on that run, and each failing on its own;
- the expectation's clauses at their edges, on the held-out runs alone, and over
  nothing;
- that the writer refuses unsigned before it reads or writes.
Added after the first run, on the same run and on one where a climb is above
every rule of its list and a round lists a rule of the gateway's queue outside
the keyword: what each answer did with its whole list and with that queue, and
each side by both.
"""

from __future__ import annotations

import copy
import unittest
from unittest import mock

from corrections import doors as D
from corrections import plan
from fidelity.replay import rule_from
from harness.domain import Case
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, Space

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BI, AM, SEC, SS = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SECURITY_INCIDENT", "SELF_SERVICE_DEFLECT"
IMP, ERR, CON = plan.IMPASSE, plan.ERROR, "CONFLICT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
KW = SPACE.mask["has_security_keyword"][True]


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


KEYWORD = c_("has_security_keyword", "eq", True)
SEV4 = c_("severity", "eq", 4)
FREE = c_("customer_tier", "eq", "free")


def r_(rid, born, action, conds, beats=(), loses_to=(), dropped=()):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to), "dropped_edges": list(dropped)}


def cy(side, rid):
    return f"{side}:{rid}:{EDGE_CYCLE}"


# U is the keyword's security rule, and contains the gateway G; Q is a security
# rule that does not. K is a keyword rule of another queue than SECURITY_INCIDENT.
BIRTHS = [
    (IMP, r_("U", 0, SEC, [KEYWORD]), []),
    (IMP, r_("K", 1, T2, [KEYWORD, FREE]), []),
    (IMP, r_("Q", 2, SEC, [KEYWORD, c_("severity", "lte", 2)]), []),
    (ERR, r_("G", 3, T2, [KEYWORD, SEV4]), []),
    (CON, r_("D", 4, AM, [c_("customer_tier", "eq", "business"),
                         c_("prior_tickets_30d", "gte", 20)],
             beats=["G", "K"], loses_to=["Q"], dropped=[cy("loses_to", "U")]),
     ["U", "K", "Q", "G"]),
    (ERR, r_("C", 5, BI, [c_("product", "eq", "billing")], beats=["K", "D"],
             loses_to=["U", "Q"], dropped=[cy("beats", "G")]),
     ["U", "K", "Q", "G", "D"]),
    (ERR, r_("E", 6, SS, [FREE, SEV4], loses_to=["U", "K", "G"]), ["U", "K", "G"]),
    (CON, r_("H", 7, SS, [FREE, SEV4, c_("prior_tickets_30d", "eq", 0)], beats=["U"],
             loses_to=["K"], dropped=[cy("beats", "G")]),
     ["U", "K", "G"]),
    (ERR, r_("M", 8, T1, [SEV4, c_("channel", "eq", "chat")], beats=["K"], loses_to=["U"],
             dropped=[cy("loses_to", "G")]),
     ["U", "K", "G"]),
    (IMP, r_("Z", 9, BI, [c_("product", "eq", "api")], loses_to=["U"]), ["U"]),
    (ERR, r_("W", 10, T3, [c_("product", "eq", "mobile")], beats=["D"], loses_to=["G", "U"]),
     ["U", "G", "D"]),
]


def ticket(**kw):
    base = dict(has_security_keyword=False, severity=3, customer_tier="pro", product="dashboard",
                channel="portal", prior_tickets_30d=1, off_hours=False, language="en")
    base.update(kw)
    return Case(**base)


# Each birth's ticket matches its rule; E's lies inside the gateway.
CORPUS = [
    ticket(has_security_keyword=True, severity=1),
    ticket(has_security_keyword=True, customer_tier="free"),
    ticket(has_security_keyword=True, severity=2),
    ticket(has_security_keyword=True, severity=4),
    ticket(customer_tier="business", prior_tickets_30d=20),
    ticket(product="billing"),
    ticket(customer_tier="free", severity=4, has_security_keyword=True),
    ticket(customer_tier="free", severity=4, prior_tickets_30d=0),
    ticket(severity=4, channel="chat"),
    ticket(product="api"),
    ticket(product="mobile"),
]

SAID = {"beats:cierra_ciclo": 2, "beats:ok": 1, "loses_to:cierra_ciclo": 1, "loses_to:ok": 2}


def record(births=None):
    births = births if births is not None else BIRTHS
    return {"rules": [r for _, r, _ in births],
            "escalations": [{"idx": r["born_at"], "kind": cause, "listed": list(listed)}
                            for cause, r, listed in births]}


def gateway_run(gates=("G",), doors=(("D", "G"),), said=None):
    born = {r["rule_id"]: r for _, r, _ in BIRTHS}
    return {"gateways": [{"rule_id": g, "born_at": born[g]["born_at"],
                          "action": born[g]["action"], "conditions": born[g]["conditions"]}
                         for g in gates],
            "doors": [{"door": d, "gateway": g, "kind": D.gw.DOOR_WIN} for d, g in doors],
            "added_after_the_first_run": {"answers": {
                "rounds_that_listed_a_gateway": dict(SAID if said is None else said)}}}


def read(rec=None, grun=None, tag=None):
    return D.read_run(rec or record(), grun or gateway_run(), SPACE, CORPUS, tag=tag)


def gate(run, k):
    return next(g["passes"] for g in run["gates"] if g["gate"] == k)


class TestRegions(unittest.TestCase):

    def test_a_rules_region_is_its_conditions(self):
        ext = D.extensions(record(), SPACE)
        self.assertEqual(ext["G"], SPACE.extension(rule_from(BIRTHS[3][1]).conditions))
        self.assertEqual(ext["G"].bit_count(), SPACE.n // 8)

    def test_a_keyword_rule_lies_inside_the_keyword_half(self):
        ext = D.extensions(record(), SPACE)
        self.assertTrue(D.keyword_rule(ext["K"], KW))
        self.assertTrue(D.keyword_rule(ext["G"], KW))
        self.assertFalse(D.keyword_rule(ext["E"], KW))
        self.assertFalse(D.keyword_rule(0, KW))

    def test_a_ticket_is_one_point_of_its_rule(self):
        ext = D.extensions(record(), SPACE)
        p = D.point(SPACE, CORPUS[6])
        self.assertEqual(p.bit_count(), 1)
        self.assertTrue(p & ext["E"] and p & ext["G"])
        self.assertFalse(D.point(SPACE, CORPUS[7]) & ext["G"])


class TestWhatAnAnswerDid(unittest.TestCase):

    def test_a_side(self):
        said = {"G": ("beats", EDGE_CYCLE), "U": ("loses_to", EDGE_OK)}
        self.assertEqual(D.side_of(said, "G"), D.CLIMB)
        self.assertEqual(D.side_of(said, "U"), D.CEDE)
        self.assertEqual(D.side_of(said, "K"), D.NO_SIDE)

    def test_every_rule_of_a_set(self):
        said = {"A": ("beats", EDGE_OK), "B": ("beats", EDGE_CYCLE), "C": ("loses_to", EDGE_OK)}
        self.assertEqual(D.toward(said, ["A", "B"]), D.ABOVE)
        self.assertEqual(D.toward(said, ["C"]), D.BELOW)
        self.assertEqual(D.toward(said, ["A", "C"]), D.MIXED)
        self.assertEqual(D.toward(said, ["A", "X"]), D.MIXED)
        self.assertEqual(D.toward(said, []), D.NONE_LISTED)

    def test_a_size(self):
        self.assertEqual(D.size_of(0b1, 0b11), D.NARROWER)
        self.assertEqual(D.size_of(0b111, 0b11), D.BROADER)
        self.assertEqual(D.size_of(0b10, 0b01), D.EQUAL)


class TestTheListings(unittest.TestCase):

    def setUp(self):
        self.run = read()
        self.by = {l["newborn"]: l for l in self.run["listings"]}

    def test_every_round_after_the_gateway_that_listed_it(self):
        self.assertEqual(list(self.by), ["D", "C", "E", "H", "M", "W"])
        self.assertEqual({k: l["side"] for k, l in self.by.items()},
                         {"D": D.CLIMB, "C": D.CLIMB, "E": D.CEDE, "H": D.CLIMB,
                          "M": D.CEDE, "W": D.CEDE})
        self.assertEqual(self.by["C"]["said"], ["beats", EDGE_CYCLE])
        self.assertEqual(self.by["M"]["said"], ["loses_to", EDGE_CYCLE])

    def test_the_other_keyword_rules(self):
        self.assertEqual(self.by["D"]["keyword_rules"], ["K"])
        self.assertEqual({k: l["keyword_toward"] for k, l in self.by.items()},
                         {"D": D.ABOVE, "C": D.ABOVE, "H": D.BELOW, "E": D.BELOW,
                          "M": D.ABOVE, "W": D.NONE_LISTED})

    def test_the_security_rules_contain_the_gateway(self):
        self.assertEqual(self.by["D"]["security_rules"], ["U"])
        self.assertEqual({k: l["security_toward"] for k, l in self.by.items()},
                         {"D": D.BELOW, "C": D.BELOW, "H": D.ABOVE, "E": D.BELOW,
                          "M": D.BELOW, "W": D.BELOW})
        self.assertEqual(self.by["D"]["security_losses"], {"U": EDGE_CYCLE})
        self.assertEqual(self.by["C"]["security_losses"], {"U": EDGE_OK})
        self.assertEqual(self.by["H"]["security_losses"], {})

    def test_the_newborn_against_the_gateway(self):
        self.assertEqual({k: l["size"] for k, l in self.by.items()},
                         {"D": D.NARROWER, "C": D.BROADER, "E": D.NARROWER, "H": D.NARROWER,
                          "M": D.NARROWER, "W": D.BROADER})
        self.assertEqual([k for k, l in self.by.items() if l["inside"]], ["E"])
        self.assertTrue(all(l["crosses"] for l in self.by.values()))
        self.assertEqual(self.by["D"]["shared"], 200)

    def test_a_round_that_listed_two_gateways_is_counted_once_for_each(self):
        run = read(grun=gateway_run(gates=("K", "G")))
        both = [l for l in run["listings"] if l["newborn"] == "D"]
        self.assertEqual([l["gateway"] for l in both], ["K", "G"])
        self.assertTrue(all(l["keyword_rules"] == [] for l in run["listings"]))

    def test_every_placement_by_kind(self):
        self.assertEqual(self.run["summary"]["placements"], {
            "gateway:cede": 3, "gateway:climb": 3, "keyword:cede": 2, "keyword:climb": 3,
            "outside:climb": 2, "security:cede": 8, "security:climb": 1})

    def test_the_summary(self):
        s = self.run["summary"]
        self.assertEqual(s["sides"], {D.CEDE: 3, D.CLIMB: 3})
        self.assertEqual(s["said"], SAID)
        self.assertEqual(s["installed"], [["D", "G"]])
        self.assertEqual(s["inside"], {D.CLIMB: {"false": 3}, D.CEDE: {"false": 2, "true": 1}})
        self.assertEqual(s["queue"][D.CLIMB], {AM: 1, BI: 1, SS: 1})


class TestTheGates(unittest.TestCase):

    def test_they_pass_on_the_run(self):
        self.assertTrue(all(g["passes"] for g in read()["gates"]))
        self.assertEqual([g["gate"] for g in read()["gates"]], [1, 2, 3, 4])

    def test_1_fails_on_other_listings(self):
        self.assertFalse(gate(read(grun=gateway_run(said={**SAID, "beats:ok": 2})), 1))

    def test_2_fails_on_other_doors(self):
        self.assertFalse(gate(read(grun=gateway_run(doors=())), 2))
        self.assertFalse(gate(read(grun=gateway_run(doors=(("D", "G"), ("H", "G")))), 2))

    def test_3_fails_on_a_newborn_nested_in_its_gateway(self):
        births = copy.deepcopy(BIRTHS)
        births[6][1]["conditions"] = [KEYWORD, SEV4, FREE]
        self.assertFalse(gate(read(rec=record(births)), 3))

    def test_3_fails_on_a_newborn_of_the_gateways_queue(self):
        births = copy.deepcopy(BIRTHS)
        births[6][1]["action"] = T2
        self.assertFalse(gate(read(rec=record(births)), 3))

    def test_4_fails_on_an_installed_door_that_kept_its_loss(self):
        births = copy.deepcopy(BIRTHS)
        births[4][1]["loses_to"] = ["Q", "U"]
        births[4][1]["dropped_edges"] = []
        self.assertFalse(gate(read(rec=record(births)), 4))

    def test_5_reads_the_development_set(self):
        dev = D.development(read())
        with mock.patch.object(D, "DEVELOPMENT", dev):
            self.assertTrue(gate(read(tag=D.DEVELOPMENT_RUN), 5))
        with mock.patch.object(D, "DEVELOPMENT", {**dev, "climbs": 4}):
            self.assertFalse(gate(read(tag=D.DEVELOPMENT_RUN), 5))
        self.assertEqual(dev["climbs_above_every_keyword_rule"], 2)
        self.assertEqual(dev["climbs_with_keyword_rules"], 3)
        self.assertEqual(dev["keyword_placed"], 5)


def listing(side, kw=None, sec=None):
    return {"side": side, "keyword_rules": ["K"] if kw else [],
            "keyword_toward": kw or D.NONE_LISTED,
            "security_rules": ["U"] if sec else [], "security_toward": sec or D.NONE_LISTED}


def run_of(listings, kw_below=3, kw_climb=1):
    return {"listings": listings,
            "summary": {"placements": {"keyword:cede": kw_below, "keyword:climb": kw_climb}}}


def line(n_yes, n_no, side, yes, no, kind):
    """`n_yes` listings of `side` that did `yes` with every rule of `kind`, and
    `n_no` that did `no`."""
    key = "kw" if kind == D.KEYWORD else "sec"
    return ([listing(side, **{key: yes}) for _ in range(n_yes)]
            + [listing(side, **{key: no}) for _ in range(n_no)])


def at_the_line():
    held = (line(3, 1, D.CLIMB, D.ABOVE, D.MIXED, D.KEYWORD)
            + line(3, 1, D.CEDE, D.BELOW, D.ABOVE, D.KEYWORD)
            + line(3, 1, D.CLIMB, D.BELOW, D.ABOVE, D.SECURITY))
    n3 = (line(3, 1, D.CLIMB, D.ABOVE, D.BELOW, D.KEYWORD)
          + line(3, 1, D.CLIMB, D.BELOW, D.MIXED, D.SECURITY))
    return held, n3


def clauses(runs):
    return {c["clause"]: c["holds"] for c in D.read_expectation(runs)}


ALL = ["F1", "F2", "F3", "F4", "F5", "F6"]


class TestTheExpectation(unittest.TestCase):

    def test_the_runs(self):
        self.assertEqual(D.DEVELOPMENT_RUN, "l_r1")
        self.assertEqual(D.HELD_OUT, ("l_r2", "l_r3"))
        self.assertEqual(D.CONTROL, "n_r3")

    def test_every_clause_holds_at_its_line(self):
        held, n3 = at_the_line()
        runs = {"l_r2": run_of(held[:6], 2, 1), "l_r3": run_of(held[6:], 1, 0),
                D.CONTROL: run_of(n3)}
        self.assertEqual(clauses(runs), {k: True for k in ALL})

    def test_every_clause_fails_below_its_line(self):
        held = (line(2, 1, D.CLIMB, D.ABOVE, D.MIXED, D.KEYWORD)
                + line(2, 1, D.CEDE, D.BELOW, D.ABOVE, D.KEYWORD)
                + line(2, 1, D.CLIMB, D.BELOW, D.ABOVE, D.SECURITY))
        n3 = (line(2, 1, D.CLIMB, D.ABOVE, D.BELOW, D.KEYWORD)
              + line(2, 1, D.CLIMB, D.BELOW, D.MIXED, D.SECURITY))
        runs = {"l_r2": run_of(held, 2, 1), "l_r3": run_of([], 0, 0), D.CONTROL: run_of(n3)}
        self.assertEqual(clauses(runs), {k: False for k in ALL})

    def test_the_development_set_is_left_out(self):
        held, n3 = at_the_line()
        dev = line(0, 9, D.CLIMB, D.ABOVE, D.BELOW, D.KEYWORD)
        runs = {"l_r1": run_of(dev, 0, 9), "l_r2": run_of(held, 3, 1),
                "l_r3": run_of([], 0, 0), D.CONTROL: run_of(n3)}
        self.assertEqual(clauses(runs), {k: True for k in ALL})

    def test_a_listing_without_the_rules_is_not_read(self):
        held, n3 = at_the_line()
        held = held + [listing(D.CLIMB), listing(D.CEDE)]
        runs = {"l_r2": run_of(held, 3, 1), D.CONTROL: run_of(n3 + [listing(D.CLIMB)])}
        self.assertEqual(clauses(runs), {k: True for k in ALL})

    def test_a_clause_over_nothing_fails(self):
        self.assertEqual(clauses({"l_r2": run_of([], 0, 0)}), {k: False for k in ALL})


class TestAddedAfterTheFirstRun(unittest.TestCase):
    """The whole list and the gateway's queue, on the run and on one where H is
    above every rule of its list, and a round lists a rule of the gateway's
    queue outside the keyword, P."""

    def other(self):
        births = copy.deepcopy(BIRTHS)
        births[7][1]["beats"] = ["U", "K"]
        births[7][1]["loses_to"] = []
        births += [(IMP, r_("P", 11, T2, [c_("product", "eq", "api")]), []),
                   (ERR, r_("V", 12, BI, [c_("channel", "eq", "phone")], beats=["G", "P"],
                            loses_to=["U"]), ["U", "G", "P"])]
        corpus = CORPUS + [ticket(product="api"), ticket(channel="phone")]
        return D.read_run(record(births), gateway_run(), SPACE, corpus)

    def test_the_whole_list(self):
        got = {l["newborn"]: l["added_after_the_first_run"]["list_toward"]
               for l in read()["listings"]}
        self.assertEqual(got, {"D": D.MIXED, "C": D.MIXED, "E": D.BELOW, "H": D.MIXED,
                               "M": D.MIXED, "W": D.MIXED})
        by = {l["newborn"]: l["added_after_the_first_run"] for l in self.other()["listings"]}
        self.assertEqual(by["H"]["list_toward"], D.ABOVE)

    def test_the_gateways_queue_outside_the_keyword(self):
        self.assertTrue(all(l["added_after_the_first_run"]["queue_rules"] == []
                            for l in read()["listings"]))
        by = {l["newborn"]: l["added_after_the_first_run"] for l in self.other()["listings"]}
        self.assertEqual(by["V"]["queue_rules"], ["P"])
        self.assertEqual(by["V"]["queue_toward"], D.ABOVE)
        self.assertEqual(by["E"]["queue_toward"], D.NONE_LISTED)

    def test_each_side_by_both(self):
        got = self.other()["added_after_the_first_run"]
        self.assertEqual(got["climbs"], {"above_every:above_every": 1,
                                         "below_every:mixed": 3})
        self.assertEqual(got["queue_toward"][D.CLIMB], {D.ABOVE: 1, D.NONE_LISTED: 3})
        self.assertEqual(got["list_toward"][D.CEDE], {D.BELOW: 1, D.MIXED: 2})

    def test_it_moves_no_gate(self):
        self.assertEqual([g["gate"] for g in read()["gates"]], [1, 2, 3, 4])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(D, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                D.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
