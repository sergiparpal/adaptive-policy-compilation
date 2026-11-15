"""
`corrections/above.py` — the POST-RUN reading of why some answers put their
newborn above every rule of their list, no figure.

What is pinned is the instrument, on one run built by hand over the real space.
Four rules are born without a list: `U` and `V` of SECURITY_INCIDENT on the
keyword, `O` of ONCALL_ESCALATION, and `X` of T2_TECHNICAL. Five newborns are
listed rules, each round in v1c's seeded shuffle:
- `A`, of BILLING_SPECIALIST, below `U`, `V` and `O`, at a reported error whose
  ticket `O` matches;
- `B`, a draft of four conditions of T2_TECHNICAL, above `U` alone, at an
  impasse, with a note that reads it by its conditions;
- `C`, of T1_GENERAL, above `X`, which matches its ticket;
- `D`, of T1_GENERAL, below `O` and above `X`, at a reported error whose ticket
  `X` matches;
- `E`, of SECURITY_INCIDENT, above `X`.
Also pinned:
- the queues put first, a round's note, and the cell of a narrow draft against
  a short block;
- each round's sets and what its answer did with them, and the placements by
  the ticket;
- what the rounds give, the also-read part, and the development counts;
- the five gates on that run, and each failing on its own;
- the expectation's clauses at their edges and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import unittest
from fractions import Fraction
from unittest import mock

from corrections import above as A
from corrections import plan
from harness.domain import Case
from reasoned_loop import protocol as rp
from rung2.engine2 import Space

F = Fraction
SPACE = Space()
T1, T2 = "T1_GENERAL", "T2_TECHNICAL"
BI, SEC, ONC = "BILLING_SPECIALIST", "SECURITY_INCIDENT", "ONCALL_ESCALATION"
IMP, ERR, CON = plan.IMPASSE, plan.ERROR, "CONFLICT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
ABOVE, BELOW, MIXED, NONE_LISTED = A.ABOVE, A.BELOW, A.MIXED, A.NONE_LISTED


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


KEYWORD = c_("has_security_keyword", "eq", True)


def r_(rid, born, action, conds, beats=(), loses_to=(), note=""):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to), "dropped_edges": [],
            "note": note}


# born_at, cause, rule, the rules its round lists, the placement call's note.
BIRTHS = [
    (0, IMP, r_("U", 0, SEC, [KEYWORD]), [], None),
    (1, IMP, r_("V", 1, SEC, [KEYWORD, c_("severity", "eq", 1)]), [], None),
    (2, IMP, r_("O", 2, ONC, [c_("severity", "eq", 1), c_("off_hours", "eq", True)]), [], None),
    (3, IMP, r_("X", 3, T2, [c_("product", "eq", "api")]), [], None),
    (4, ERR, r_("A", 4, BI, [c_("product", "eq", "billing")], loses_to=["U", "V", "O"]),
     ["U", "V", "O"], "Security first, then the on-call rule."),
    (5, IMP, r_("B", 5, T2, [c_("customer_tier", "eq", "free"), c_("severity", "eq", 2),
                             c_("product", "eq", "mobile"), c_("channel", "eq", "chat")],
                beats=["U"]), ["U"], "This rule is more specific: it adds conditions."),
    (6, CON, r_("C", 6, T1, [c_("customer_tier", "eq", "free")], beats=["X"]), ["X"], "Mine."),
    (7, ERR, r_("D", 7, T1, [c_("customer_tier", "eq", "pro")], beats=["X"], loses_to=["O"]),
     ["O", "X"], "On call wins; the API rule does not."),
    (8, CON, r_("E", 8, SEC, [KEYWORD, c_("channel", "eq", "email")], beats=["X"]), ["X"],
     "Security comes first."),
]
BASE = {"has_security_keyword": False, "severity": 3, "customer_tier": "pro",
        "product": "dashboard", "channel": "email", "prior_tickets_30d": 0, "off_hours": False,
        "language": "en"}
TICKETS = {
    4: {"product": "billing", "severity": 1, "off_hours": True},
    5: {"customer_tier": "free", "severity": 2, "product": "mobile", "channel": "chat"},
    6: {"customer_tier": "free", "product": "api"},
    7: {"customer_tier": "pro", "product": "api"},
    8: {"has_security_keyword": True, "channel": "email", "product": "api"},
}
CORPUS = [Case(**{**BASE, **TICKETS.get(i, {})}) for i in range(9)]


def record(births=None):
    births = births or BIRTHS
    escs = []
    for born, cause, rule, listed, note in births:
        order = rp.listing(sorted(listed), born, 0) if listed else []
        calls = [{"round": 0, "listed": list(order)}]
        if listed:
            calls.append({"round": 1, "payload": {
                "action": rule["action"], "conditions": rule["conditions"],
                "beats": list(rule["beats"]), "loses_to": list(rule["loses_to"]),
                "note": note}})
        escs.append({"idx": born, "kind": cause, "listed": order, "calls": calls})
    return {"rules": [copy.deepcopy(b[2]) for b in births], "escalations": escs}


def read(rec=None, tag=None):
    return A.read_run(rec or record(), SPACE, CORPUS, tag=tag)


def gate(run, k):
    return next(g["passes"] for g in run["gates"] if g["gate"] == k)


def by_newborn(run):
    return {r["newborn"]: r for r in run["rounds"]}


class TestOneRound(unittest.TestCase):

    def test_the_queues_put_first(self):
        self.assertEqual(A.first_queues(SEC), set())
        self.assertEqual(A.first_queues(ONC), {SEC})
        self.assertEqual(A.first_queues(T2), {SEC, ONC})

    def test_a_rounds_note(self):
        rule = {"note": "the rule's own"}
        call = {"idx": 1, "calls": [{"round": 0}, {"round": 1, "payload": {"note": "whole"}}]}
        self.assertEqual(A.note_of(call, rule), "whole")
        self.assertEqual(A.note_of({"calls": [{"round": 0}]}, rule), "the rule's own")
        self.assertEqual(A.note_of({}, {}), "")

    def test_the_cell_of_a_narrow_draft_against_a_short_block(self):
        self.assertTrue(A.narrow_short({"conditions": 4, "security": 2}))
        self.assertFalse(A.narrow_short({"conditions": 3, "security": 1}))
        self.assertFalse(A.narrow_short({"conditions": 5, "security": 3}))

    def test_the_rounds(self):
        rows = by_newborn(read())
        self.assertEqual(sorted(rows), ["A", "B", "C", "D", "E"])
        a, b, c, d, e = (rows[k] for k in "ABCDE")
        self.assertEqual((a["list_toward"], a["security"], a["security_toward"], a["oncall"],
                          a["oncall_toward"], a["first"], a["first_toward"]),
                         (BELOW, 2, BELOW, 1, BELOW, 3, BELOW))
        self.assertEqual((a["ticket"], a["ticket_toward"], a["placed"]),
                         (1, BELOW, {"ticket": {"cede": 1}, "elsewhere": {"cede": 2}}))
        self.assertEqual(a["codes"], {"conditions": False, "security": True})
        self.assertEqual((b["list_toward"], b["security_toward"], b["oncall_toward"],
                          b["conditions"], b["cause"], b["codes"]),
                         (ABOVE, ABOVE, NONE_LISTED, 4, IMP,
                          {"conditions": True, "security": False}))
        self.assertEqual((b["ticket"], b["placed"]),
                         (0, {"ticket": {}, "elsewhere": {"climb": 1}}))
        self.assertEqual((c["list_toward"], c["ticket_toward"]), (ABOVE, ABOVE))
        self.assertEqual((d["list_toward"], d["oncall_toward"], d["ticket_toward"], d["placed"]),
                         (MIXED, BELOW, ABOVE, {"ticket": {"climb": 1}, "elsewhere": {"cede": 1}}))
        self.assertEqual((e["queue"], e["list_toward"], e["first"]), (SEC, ABOVE, 0))


class TestWhatTheRoundsGive(unittest.TestCase):

    def test_the_groups(self):
        rows = by_newborn(read())
        self.assertEqual({k: A.group(r) for k, r in rows.items()},
                         {"A": "security_listed", "B": "security_listed", "C": "neither_listed",
                          "D": "oncall_listed", "E": "newborn_security"})

    def test_the_summary(self):
        s = read()["summary"]
        self.assertEqual(s["rounds"], 5)
        self.assertEqual(s["list_toward"], {ABOVE: 3, BELOW: 1, MIXED: 1})
        self.assertEqual(s["security_block"], {BELOW: 1})
        self.assertEqual(s["oncall_block"], {})
        self.assertEqual(s["above_every_security"], {"rounds": 1, "list_toward": {ABOVE: 1}})
        self.assertEqual({k: (v["hits"], v["of"]) for k, v in s["narrow_short"].items()},
                         {"narrow_short": (1, 1), "others": (0, 1)})
        self.assertEqual(s["placements_by_cause"],
                         {CON: {"ticket:climb": 2}, ERR: {"elsewhere:cede": 3, "ticket:cede": 1,
                                                          "ticket:climb": 1},
                          IMP: {"elsewhere:climb": 1}})

    def test_the_also_read_part(self):
        al = read()["also_read"]
        self.assertEqual({s: {k: (v["hits"], v["of"]) for k, v in d.items()}
                          for s, d in al["codes"].items()},
                         {ABOVE: {"conditions": (1, 1), "security": (0, 1)},
                          BELOW: {"conditions": (0, 1), "security": (1, 1)}})
        self.assertEqual({k: (v["hits"], v["of"]) for k, v in al["above_security_by_cause"].items()},
                         {ERR: (0, 1), IMP: (1, 1)})
        self.assertEqual({k: (v["hits"], v["of"])
                          for k, v in al["above_security_by_conditions"].items()},
                         {"1": (0, 1), "4": (1, 1)})
        self.assertEqual({k: (v["hits"], v["of"]) for k, v in al["above_security_by_block"].items()},
                         {"1": (1, 1), "2": (0, 1)})
        self.assertEqual(al["drafts_above_security_listed_again"], {})

    def test_a_draft_listed_again(self):
        rows = [{"queue": T2, "security": 1, "security_toward": s, "draft": "d", "cause": ERR,
                 "conditions": 2, "codes": {"conditions": False, "security": False}}
                for s in (ABOVE, BELOW, BELOW)]
        self.assertEqual(A.also(rows)["drafts_above_security_listed_again"],
                         {"d": {ABOVE: 1, BELOW: 2}})
        self.assertEqual(A.also(rows[1:])["drafts_above_security_listed_again"], {})

    def test_the_development_counts(self):
        dev = A.development(read()["rounds"])
        self.assertEqual(dev, {
            "rounds": 5, "above_every": 3, "newborn_security": 1, "newborn_security_above": 1,
            "security_listed": 2, "block_rounds": 1, "block_mixed": 0,
            "above_every_security": 1, "above_every_security_and_list": 1,
            "no_oncall": [1, 1], "oncall": [0, 1], "narrow_short": [1, 1], "others": [0, 1],
            "ticket_at_errors": [1, 2], "elsewhere_at_errors": [0, 3]})


class TestTheGates(unittest.TestCase):

    def test_they_pass_on_the_run(self):
        run = read()
        self.assertEqual([g["gate"] for g in run["gates"]], [1, 2, 3, 4])
        self.assertTrue(all(g["passes"] for g in run["gates"]))

    def test_1_fails_on_a_call_that_declared_otherwise(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 5)
        esc["calls"][-1]["payload"].update({"beats": [], "loses_to": ["U"]})
        self.assertFalse(gate(read(rec=rec), 1))
        self.assertTrue(all(gate(read(rec=rec), k) for k in (2, 3, 4)))

    def test_1_reads_a_refused_edge_as_declared(self):
        rec = record()
        rule = next(r for r in rec["rules"] if r["rule_id"] == "D")
        rule["beats"] = []
        rule["dropped_edges"] = ["beats:X:cycle"]
        self.assertTrue(gate(read(rec=rec), 1))

    def test_2_fails_on_a_listed_rule_of_the_newborns_queue(self):
        rec = record()
        next(r for r in rec["rules"] if r["rule_id"] == "X")["action"] = T1
        self.assertFalse(gate(read(rec=rec), 2))

    def test_2_fails_on_a_listed_rule_that_contains_the_newborn(self):
        births = [b if b[2]["rule_id"] != "E" else
                  (8, CON, r_("E", 8, SEC, [KEYWORD, c_("product", "eq", "api")], beats=["X"]),
                   ["X"], "")
                  for b in BIRTHS]
        self.assertFalse(gate(read(rec=record(births)), 2))

    def test_3_fails_on_a_listed_rule_without_a_side(self):
        rec = record()
        next(r for r in rec["rules"] if r["rule_id"] == "D")["beats"] = []
        esc = next(e for e in rec["escalations"] if e["idx"] == 7)
        esc["calls"][-1]["payload"]["beats"] = []
        run = read(rec=rec)
        self.assertFalse(gate(run, 3))
        self.assertTrue(gate(run, 1))

    def test_4_fails_on_a_list_out_of_its_shuffle(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 4)
        esc["listed"] = list(reversed(esc["listed"]))
        if esc["listed"] == rp.listing(sorted(esc["listed"]), 4, 0):
            esc["listed"] = esc["listed"][1:] + esc["listed"][:1]
        self.assertFalse(gate(read(rec=rec), 4))

    def test_5_reads_the_development_set(self):
        dev = A.development(read()["rounds"])
        tag = A.DEVELOPMENT_RUNS[0]
        with mock.patch.object(A, "DEVELOPMENT", {tag: dev}):
            self.assertTrue(gate(read(tag=tag), 5))
        with mock.patch.object(A, "DEVELOPMENT", {tag: {**dev, "rounds": 9}}):
            self.assertFalse(gate(read(tag=tag), 5))
        self.assertEqual([g["gate"] for g in read(tag="l_r2")["gates"]], [1, 2, 3, 4])


def row(queue=T2, security=0, toward=NONE_LISTED, oncall=0, listed=MIXED, cause=ERR,
        conditions=2, ticket=None):
    return {"queue": queue, "security": security, "security_toward": toward, "oncall": oncall,
            "list_toward": listed, "cause": cause, "conditions": conditions,
            "placed": {"ticket": dict(ticket or {}), "elsewhere": {}}}


L2, L3 = A.HELD_OUT
N1, N2 = A.CONTROL


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, held=(), ctrl=(), where=(L2, N1)):
        runs = {where[0]: {"rounds": list(held)}, where[1]: {"rounds": list(ctrl)}}
        return {c["clause"]: c["holds"] for c in A.read_expectation(runs)}

    def test_the_runs(self):
        self.assertEqual(A.DEVELOPMENT_RUNS, ("l_r1", "n_r3"))
        self.assertEqual(A.HELD_OUT, ("l_r2", "l_r3"))
        self.assertEqual(A.CONTROL, ("n_r1", "n_r2"))

    def test_e1_at_its_line(self):
        blocks = [row(security=2, toward=BELOW)] * 18 + [row(security=3, toward=ABOVE)]
        self.assertTrue(self.verdicts(blocks + [row(security=2, toward=MIXED)])["E1"])
        self.assertFalse(self.verdicts(blocks[1:] + [row(security=2, toward=MIXED)] * 2)["E1"])
        # A block of one rule, or a newborn of SECURITY_INCIDENT, is not read.
        self.assertFalse(self.verdicts([row(security=1, toward=ABOVE),
                                        row(queue=SEC, security=2, toward=MIXED)])["E1"])

    def test_e2_at_its_line(self):
        without = [row(queue=T1, listed=ABOVE)] * 3 + [row(queue=T1)] * 7
        with_ = [row(queue=T1, oncall=1, listed=ABOVE)] + [row(queue=T1, oncall=1)] * 9
        self.assertTrue(self.verdicts(without + with_)["E2"])
        self.assertFalse(self.verdicts(without + with_[:1] * 2 + with_[2:])["E2"])
        self.assertTrue(self.verdicts(without + with_[1:])["E2"])
        self.assertFalse(self.verdicts(without)["E2"])
        self.assertFalse(self.verdicts([row(queue=T1)] * 3 + with_[1:])["E2"])
        # A newborn of ONCALL_ESCALATION, or a list with a security rule, is not read.
        self.assertFalse(self.verdicts([row(queue=ONC, listed=ABOVE),
                                        row(queue=T1, security=1, oncall=1)])["E2"])

    def test_e3_at_its_line(self):
        self.assertTrue(self.verdicts([row(ticket={"climb": 9, "cede": 1})])["E3"])
        self.assertFalse(self.verdicts([row(ticket={"climb": 8, "cede": 2})])["E3"])
        self.assertFalse(self.verdicts([row(cause=CON, ticket={"climb": 9})])["E3"])

    def test_e4_and_e6_at_their_line(self):
        cell = [row(security=1, toward=ABOVE, conditions=4)] * 3 + \
            [row(security=2, toward=BELOW, conditions=5)] * 7
        others = [row(security=1, toward=ABOVE, conditions=3)] + \
            [row(security=3, toward=BELOW, conditions=4)] * 9
        got = self.verdicts(cell + others, cell + others)
        self.assertEqual((got["E4"], got["E6"]), (True, True))
        past = cell + others[:1] * 2 + others[2:]
        got = self.verdicts(past, past)
        self.assertEqual((got["E4"], got["E6"]), (False, False))
        self.assertFalse(self.verdicts(others)["E4"])
        self.assertFalse(self.verdicts(cell)["E4"])

    def test_e5_at_its_line(self):
        above = [row(security=1, toward=ABOVE, listed=ABOVE)] * 3
        self.assertTrue(self.verdicts(ctrl=above + [row(security=2, toward=ABOVE)])["E5"])
        self.assertFalse(self.verdicts(ctrl=above[1:] + [row(security=2, toward=ABOVE)] * 2)["E5"])
        self.assertFalse(self.verdicts(held=above)["E5"])

    def test_the_development_set_is_left_out(self):
        rows = ([row(security=2, toward=BELOW)] * 20 + [row(ticket={"climb": 10})]
                + [row(security=1, toward=ABOVE, listed=ABOVE, conditions=4)])
        got = self.verdicts(rows, rows, where=A.DEVELOPMENT_RUNS)
        self.assertEqual(got, {k: False for k in ("E1", "E2", "E3", "E4", "E5", "E6")})

    def test_a_clause_over_nothing_fails(self):
        got = {c["clause"]: c["holds"] for c in A.read_expectation({})}
        self.assertEqual(got, {k: False for k in ("E1", "E2", "E3", "E4", "E5", "E6")})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(A, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                A.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
