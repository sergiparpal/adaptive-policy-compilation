"""
`corrections/forgotten.py` — the POST-RUN reading of why the final base forgets
its corrections, no figure.

What is pinned is the instrument, on a run built by hand: thirteen cases, twelve
rules and one declared edge, with six labelled points. Each class and each loss
falls on a point chosen for it:
- a point kept;
- a point never born, its one report left unplaced;
- a point never right, its correction broader than the rule that erred there;
- a point taken back by containment, then arriving again unreported;
- a point taken back by an edge;
- a point taken back by a conflict.
Also pinned:
- why a born report does not leave its point right, for each reason;
- the final ways of the forgotten points;
- the five gates on that run, and each failing on its own;
- the expectation's clauses at their edges, and a clause over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from unittest import mock

from corrections import forgotten as G
from corrections import plan
from edges import rebuild as erb
from fidelity.replay import rule_from
from harness.domain import Case
from rung2.engine2 import EDGE_OK, PriorityEngine, Space

SPACE = Space()
T1, T2, T3 = "T1_GENERAL", "T2_TECHNICAL", "T3_ENGINEERING"
BI, AM, SS = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SELF_SERVICE_DEFLECT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}


def r_(rid, born, action, **conds):
    return {"rule_id": rid, "born_at": born, "action": action,
            "conditions": [{"attr": a, "op": "eq", "value": v} for a, v in conds.items()]}


def ticket(**over):
    base = dict(has_security_keyword=False, severity=3, customer_tier="free",
                product="api", channel="portal", prior_tickets_30d=0,
                off_hours=False, language="en")
    base.update(over)
    return Case(**base)


# The corpus: the case at each index, its true queue, and what the run did there.
#   cause, verdict: the escalation, if any; rule: the rule born there, if any.
CASES = [
    # 0: an impasse; a broad rule of T2 for api tickets.
    (ticket(severity=4), T2, "IMPASSE", "nacida", r_("R1", 0, T2, product="api")),
    # 1: R1 errs; the correction for T3 is nested inside it, right at birth.
    (ticket(severity=1), T3, "ERROR", "nacida", r_("R2", 1, T3, product="api", severity=1)),
    # 2: an impasse; a narrow rule of billing.
    (ticket(product="billing", channel="email"), BI, "IMPASSE", "nacida",
     r_("R3", 2, BI, product="billing", channel="email")),
    # 3: R3 errs; the correction for AM is broader than R3, so R3 keeps the ticket.
    (ticket(product="billing", channel="email", severity=2), AM, "ERROR", "nacida",
     r_("R4", 3, AM, product="billing")),
    # 4: an impasse; its rule is nested inside R2 and takes ticket 1 back.
    (ticket(product="mobile", severity=2), T1, "IMPASSE", "nacida",
     r_("R5", 4, AM, product="api", severity=1, channel="portal")),
    # 5: an impasse; a broad rule of T1 for mobile tickets.
    (ticket(product="mobile"), T1, "IMPASSE", "nacida", r_("R6", 5, T1, product="mobile")),
    # 6: R6 errs; the correction for SS is nested inside it, right at birth.
    (ticket(product="mobile", channel="chat"), SS, "ERROR", "nacida",
     r_("R7", 6, SS, product="mobile", channel="chat")),
    # 7: an impasse; its rule crosses R7 and is declared above it.
    (ticket(product="dashboard", channel="chat"), T2, "IMPASSE", "nacida",
     r_("R8", 7, T2, channel="chat", severity=3)),
    # 8: an impasse; a broad rule of T1 for integrations tickets.
    (ticket(product="integrations"), T1, "IMPASSE", "nacida",
     r_("R9", 8, T1, product="integrations")),
    # 9: R9 errs; the correction for T2 is nested inside it, right at birth.
    (ticket(product="integrations", off_hours=True), T2, "ERROR", "nacida",
     r_("R10", 9, T2, product="integrations", off_hours=True)),
    # 10: an impasse; its rule crosses R10 with no edge: ticket 9 in conflict.
    (ticket(product="dashboard", off_hours=True), BI, "IMPASSE", "nacida",
     r_("R11", 10, BI, off_hours=True, language="en")),
    # 11: R9 errs; the answer is left unplaced, and nothing is born.
    (ticket(product="integrations", channel="email"), AM, "ERROR", "sin_situar", None),
    # 12: R4 errs; the correction for billing is nested inside it, and kept.
    (ticket(product="billing", channel="phone"), BI, "ERROR", "nacida",
     r_("R12", 12, BI, product="billing", channel="phone")),
    # 13: ticket 1 again, decided wrong by R5 and not reported.
    (ticket(severity=1), T3, None, None, None),
]
EDGES = [("R8", "R7", EDGE_OK)]
ERRED = {1: "R1", 3: "R3", 6: "R6", 9: "R9", 11: "R9", 12: "R4"}
CORPUS = [c for c, *_ in CASES]
TRUTH = [t for _, t, *_ in CASES]


def record():
    rules, rows, escalations = [], [], []
    for idx, (case, truth, cause, verdict, rule) in enumerate(CASES):
        row = {"idx": idx, "truth": truth, "cause": cause, "escalated": cause is not None,
               "edge_reasons": [], "engine_rule": ERRED.get(idx),
               "reported": True if cause == "ERROR" else (False if idx == 13 else None)}
        rows.append(row)
        if rule is not None:
            rules.append(rule)
        if cause is not None:
            escalations.append({"idx": idx, "kind": cause, "verdict": verdict,
                                "rule_id": rule["rule_id"] if rule else None})
    for w, l, why in EDGES:
        born = max(r["born_at"] for r in rules if r["rule_id"] in (w, l))
        rows[born]["edge_reasons"].append(why)
    handed = {str(i): TRUTH[i] for i, (_, _, cause, _, _) in enumerate(CASES)
              if cause == "ERROR"}
    return {"rules": rules, "records": rows, "edge_log": [list(e) for e in EDGES],
            "escalations": escalations, "reports_handed": handed}


STAGE_C = {"runs": {"corpus": {"labelled": [1, 7]}},
           "curve_last": {"learners": {"labels": 6, "distinct_tickets": 6}}}


def read(rec=None, stage_c=STAGE_C):
    rec = rec or record()
    final = erb.rebuild(rec, CORPUS, SPACE).engine
    return G.read_run(rec, CORPUS, SPACE, stage_c, truth=TRUTH, final=final)


def point_at(run, idx):
    """The labelled point whose first report is case `idx`."""
    return next(x for x in run["points"] if x["reports"][0]["idx"] == idx)


class TestTheClasses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.got = read()

    def test_each_point_in_its_class(self):
        got = {x["reports"][0]["idx"]: x["class"] for x in self.got["points"]}
        self.assertEqual(got, {1: G.TAKEN_BACK, 3: G.NEVER_RIGHT, 6: G.TAKEN_BACK,
                               9: G.TAKEN_BACK, 11: G.NEVER_BORN, 12: G.KEPT})

    def test_the_last_losses(self):
        how = {i: point_at(self.got, i)["last_loss"] for i in (1, 6, 9)}
        self.assertEqual({i: (h["how"], h["born_at"], h["rule_id"], h["action"], h["cause"])
                          for i, h in how.items()},
                         {1: (G.BY_CONTAINMENT, 4, "R5", AM, "IMPASSE"),
                          6: (G.BY_EDGE, 7, "R8", T2, "IMPASSE"),
                          9: (G.CONFLICT, 10, "R11", BI, "IMPASSE")})
        self.assertEqual(how[1]["before"], ["R2"])
        self.assertEqual(how[1]["after"], ["R5"])
        self.assertEqual(how[9]["after"], ["R10", "R11"])

    def test_right_after_the_report_and_never_right(self):
        self.assertTrue(point_at(self.got, 1)["right_after_first_report"])
        self.assertFalse(point_at(self.got, 3)["right_after_first_report"])
        self.assertFalse(point_at(self.got, 11)["right_after_first_report"])

    def test_why_the_never_right_correction_did_not_take(self):
        (why,) = point_at(self.got, 3)["at_born_reports"]
        self.assertEqual(why["why"], G.NESTED)
        self.assertEqual(why["nested"], ["R3"])
        self.assertTrue(why["erred_is_nested"])
        self.assertTrue(why["erred_beats_it"])

    def test_the_never_born_point_keeps_its_verdict(self):
        pt = point_at(self.got, 11)
        self.assertEqual(pt["reports"], [{"idx": 11, "verdict": "sin_situar",
                                          "rule_id": None}])
        self.assertEqual(pt["at_born_reports"], [])

    def test_arriving_again_after_the_loss(self):
        self.assertEqual(point_at(self.got, 1)["after_last_loss"],
                         {"arrivals": 1, "reported": 0, "escalated": 0})
        self.assertEqual(point_at(self.got, 6)["after_last_loss"]["arrivals"], 0)
        self.assertEqual(point_at(self.got, 1)["arrivals"], [1, 13])

    def test_the_final_ways(self):
        got = {i: point_at(self.got, i)["final_way"] for i in (1, 3, 6, 9, 11)}
        self.assertEqual(got, {1: "outranked_by_containment", 3: "outranked_by_containment",
                               6: "outranked_by_edge", 9: "conflict", 11: "unwritten"})
        self.assertNotIn("final_way", point_at(self.got, 12))

    def test_the_summary(self):
        s = self.got["summary"]
        self.assertEqual(s["classes"], {G.KEPT: 1, G.NEVER_BORN: 1, G.NEVER_RIGHT: 1,
                                        G.TAKEN_BACK: 3})
        self.assertEqual(s["forgotten"], 5)
        self.assertEqual(s["last_losses"], {G.BY_CONTAINMENT: 1, G.BY_EDGE: 1, G.CONFLICT: 1})
        self.assertEqual(s["last_loss_newborn_cause"], {"IMPASSE": 3})
        self.assertEqual(s["taken_back_arrived_again"], 1)
        self.assertEqual(s["taken_back_reported_again"], 0)
        # Born reports at 1, 3, 6, 9 and 12; all but 3 left their point right.
        self.assertEqual((s["born_reports"], s["born_reports_right"]), (5, 4))
        self.assertEqual(s["why_not"], {G.NESTED: 1})
        self.assertEqual(s["never_born_verdicts"], {"sin_situar": 1})
        self.assertEqual(s["births_by_cause"], {"IMPASSE": 7, "ERROR": 5})
        self.assertEqual(s["losses_in_all"], 3)
        self.assertEqual(s["kept_after_a_loss"], 0)

    def test_the_gates_pass(self):
        self.assertTrue(all(g["passes"] for g in self.got["gates"]), self.got["gates"])
        self.assertEqual(self.got["labelled_arrivals"], [1, 7])
        self.assertEqual((self.got["labels"], self.got["labelled_points"]), (6, 6))


class TestTheGatesFail(unittest.TestCase):

    def gate(self, run, n):
        return next(g["passes"] for g in run["gates"] if g["gate"] == n)

    def test_gate_1_on_another_base(self):
        rec = record()
        other = erb.rebuild(rec, CORPUS, SPACE).engine
        other.add(rule_from(r_("RX", 13, T1, product="dashboard")), born_at=13, keep_id=True)
        run = G.read_run(rec, CORPUS, SPACE, STAGE_C, truth=TRUTH, final=other)
        self.assertFalse(self.gate(run, 1))

    def test_gate_2_on_another_count(self):
        bad = {**STAGE_C, "curve_last": {"learners": {"labels": 7, "distinct_tickets": 6}}}
        self.assertFalse(self.gate(read(stage_c=bad), 2))

    def test_gate_3_on_another_figure(self):
        bad = {**STAGE_C, "runs": {"corpus": {"labelled": [2, 7]}}}
        self.assertFalse(self.gate(read(stage_c=bad), 3))

    def test_gate_4_on_a_final_base_that_decides_otherwise(self):
        rec = record()
        other = erb.rebuild(rec, CORPUS, SPACE).engine
        other.try_edge("R10", "R11")     # in this base ticket 9 is right again
        run = G.read_run(rec, CORPUS, SPACE, STAGE_C, truth=TRUTH, final=other)
        self.assertFalse(self.gate(run, 4))

    def test_gate_5_on_a_born_verdict_naming_no_rule(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 12)
        esc["rule_id"] = "R99"
        self.assertFalse(self.gate(read(rec), 5))

    def test_a_label_that_is_not_the_reported_case_is_refused(self):
        rec = record()
        rec["reports_handed"]["3"] = T1
        with self.assertRaises(Exception):
            read(rec)


class TestWhyNot(unittest.TestCase):

    def engine(self, *rules, edges=()):
        eng = PriorityEngine(space=SPACE)
        for r in rules:
            eng.add(rule_from(r), born_at=r["born_at"], keep_id=True)
        for w, l in edges:
            self.assertEqual(eng.try_edge(w, l), EDGE_OK)
        return eng

    def test_not_matching(self):
        eng = self.engine(r_("A", 0, T2, product="api"), r_("B", 1, T3, product="mobile"))
        self.assertEqual(G.why_not(eng, ticket(), T3, "B", "A")["why"], G.NOT_MATCHING)

    def test_wrong_queue(self):
        eng = self.engine(r_("A", 0, T2, product="api"), r_("B", 1, T1, product="api",
                                                             severity=3))
        self.assertEqual(G.why_not(eng, ticket(), T3, "B", "A")["why"], G.WRONG_QUEUE)

    def test_beaten_by_an_edge(self):
        eng = self.engine(r_("A", 0, T2, product="api", channel="portal"),
                          r_("B", 1, T3, product="api", severity=3), edges=[("A", "B")])
        got = G.why_not(eng, ticket(), T3, "B", "A")
        self.assertEqual((got["why"], got["erred_beats_it"]), (G.EDGE, True))

    def test_a_conflict(self):
        eng = self.engine(r_("A", 0, T2, product="api", channel="portal"),
                          r_("B", 1, T3, product="api", severity=3))
        got = G.why_not(eng, ticket(), T3, "B", "A")
        self.assertEqual(got["why"], G.CONFLICT)
        self.assertEqual(got["beside"], [{"rule_id": "A", "action": T2}])

    def test_right(self):
        eng = self.engine(r_("A", 0, T2, product="api"),
                          r_("B", 1, T3, product="api", severity=3))
        self.assertEqual(G.why_not(eng, ticket(), T3, "B", "A"),
                         {"rule_id": "B", "right": True, "why": None})


def summary(**over):
    base = {"classes": {G.KEPT: 10, G.NEVER_BORN: 3, G.NEVER_RIGHT: 4, G.TAKEN_BACK: 5},
            "forgotten": 12, "born_reports": 20, "born_reports_right": 15,
            "last_losses": {G.BY_CONTAINMENT: 2, G.BY_EDGE: 1, G.CONFLICT: 2},
            "last_loss_newborn_cause": {"ERROR": 3, "IMPASSE": 2},
            "births_by_cause": {"ERROR": 6, "IMPASSE": 4},
            "taken_back_arrived_again": 1}
    base.update(over)
    return {"summary": base}


class TestTheExpectation(unittest.TestCase):

    def clauses(self, *runs):
        return {c["clause"]: c["holds"] for c in G.read_expectation(
            {f"l_r{i}": r for i, r in enumerate(runs, 1)})}

    def test_at_the_edges(self):
        # 3 of 12 never born and 5 of 12 taken back; 15 of 20 right at birth;
        # 3 of 5 alone; 3/5 of the takers at a reported error against 6/10 of
        # the births; 4 of 5 not seen again.
        self.assertEqual(self.clauses(summary(), summary()),
                         {"F1": True, "F2": True, "F3": True, "F4": True, "F5": True,
                          "F6": True})

    def test_just_below_each_edge(self):
        below = summary(classes={G.KEPT: 10, G.NEVER_BORN: 2, G.NEVER_RIGHT: 5,
                                 G.TAKEN_BACK: 5},
                        born_reports_right=14,
                        last_losses={G.BY_CONTAINMENT: 1, G.BY_EDGE: 0, G.CONFLICT: 4},
                        last_loss_newborn_cause={"ERROR": 2, "IMPASSE": 3},
                        taken_back_arrived_again=2)
        got = self.clauses(summary(), below)
        self.assertEqual(got, {"F1": False, "F2": True, "F3": False, "F4": False,
                               "F5": False, "F6": False})

    def test_f2_in_each_run(self):
        few = summary(classes={G.KEPT: 10, G.NEVER_BORN: 6, G.NEVER_RIGHT: 4,
                               G.TAKEN_BACK: 2})
        self.assertFalse(self.clauses(summary(), few)["F2"])

    def test_a_share_over_nothing_fails(self):
        none = summary(classes={G.KEPT: 10, G.NEVER_BORN: 0, G.NEVER_RIGHT: 0,
                                G.TAKEN_BACK: 0}, forgotten=0, born_reports=0,
                       born_reports_right=0,
                       last_losses={G.BY_CONTAINMENT: 0, G.BY_EDGE: 0, G.CONFLICT: 0},
                       last_loss_newborn_cause={}, taken_back_arrived_again=0)
        got = self.clauses(none)
        self.assertEqual(set(got.values()), {False})

    def test_the_lines(self):
        self.assertEqual((G.F1_SHARE, G.F2_SHARE, G.F3_SHARE, G.F4_SHARE, G.F6_SHARE),
                         (Fraction(1, 4), Fraction(1, 4), Fraction(3, 4), Fraction(1, 2),
                          Fraction(3, 4)))


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(G, "read_all") as reads, \
                mock.patch.object(G, "record_path") as path:
            with self.assertRaises(SystemExit):
                G.main([])
            reads.assert_not_called()
            path.return_value.write_text.assert_not_called()

    def test_the_record_lands_in_the_plan_s_directory(self):
        self.assertEqual(G.record_path(), plan.OUT / "forgotten.json")


if __name__ == "__main__":
    unittest.main()
