"""
`corrections/byqueue.py` — the POST-RUN reading of what makes an answer read a
keyword rule by its queue, no figure.

What is pinned is the instrument, on one run built by hand over the real space,
its lists in v1c's seeded shuffle. Its gateway `G` is a rule of `T2_TECHNICAL`
on the keyword, and its rounds that listed it hold:
- a cede `A`, whose loss to `G` was installed and shows in later lists;
- two listings of the same draft, `B` climbing and `C` ceding;
- a climb `D` whose list shows `A` ceding to the gateway.
Also pinned:
- a draft's key, a call's reasoning tokens, and each listing's slot,
  precedent and reasoning per listed rule;
- the pairs of the same draft, the climb rates by a feature, the lower
  medians, and the placements against keyword rules by queue;
- the five gates on that run, and each failing on its own;
- the expectation's clauses at their edges and over nothing;
- that the writer refuses unsigned before it reads or writes.
"""

from __future__ import annotations

import copy
import unittest
from fractions import Fraction
from unittest import mock

from corrections import byqueue as Q
from corrections import plan
from reasoned_loop import protocol as rp
from rung2.engine2 import EDGE_CYCLE, EDGE_OK, Space

F = Fraction
SPACE = Space()
T1, T2 = "T1_GENERAL", "T2_TECHNICAL"
BI, AM, SEC, SS = "BILLING_SPECIALIST", "ACCOUNT_MANAGER", "SECURITY_INCIDENT", "SELF_SERVICE_DEFLECT"
IMP, ERR = plan.IMPASSE, plan.ERROR
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
CLIMB, CEDE = Q.CLIMB, Q.CEDE


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


KEYWORD = c_("has_security_keyword", "eq", True)
BILLING = c_("product", "eq", "billing")


def r_(rid, born, action, conds, beats=(), loses_to=()):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to), "dropped_edges": []}


# born_at, cause, rule, the rules its round lists, its reasoning tokens.
BIRTHS = [
    (0, IMP, r_("U", 0, SEC, [KEYWORD]), [], None),
    (1, ERR, r_("G", 1, T2, [KEYWORD, c_("severity", "eq", 4)]), [], None),
    (2, ERR, r_("A", 2, AM, [c_("customer_tier", "eq", "business")], loses_to=["U", "G"]),
     ["U", "G"], 400),
    (3, ERR, r_("B", 3, BI, [BILLING], beats=["G"], loses_to=["U"]), ["U", "G", "A"], 900),
    (4, ERR, r_("C", 4, BI, [BILLING], loses_to=["U", "G"]), ["U", "G", "A"], 300),
    (5, IMP, r_("D", 5, SS, [c_("severity", "eq", 4), c_("customer_tier", "eq", "free")],
                beats=["G"], loses_to=["U"]), ["U", "G", "A"], 600),
]
# The edges each birth tried, its wins before its losses, with the record's verdicts.
EDGES = [(2, "U", "A"), (2, "G", "A"), (3, "B", "G"), (3, "U", "B"), (3, "B", "A"),
         (4, "U", "C"), (4, "G", "C"), (4, "C", "A", EDGE_CYCLE), (5, "D", "G"), (5, "U", "D"),
         (5, "D", "A")]


def record(births=None, edges=None):
    births = births or BIRTHS
    rows = [{"idx": b, "edge_reasons": []} for b, *_ in births]
    by = {r["idx"]: r for r in rows}
    log = []
    for born, w, l, *why in (edges if edges is not None else EDGES):
        reason = why[0] if why else EDGE_OK
        by[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    escs = []
    for born, cause, rule, listed, toks in births:
        order = rp.listing(sorted(listed), born, 0) if listed else []
        calls = [{"round": 0, "listed": list(order)}]
        if listed:
            calls.append({"round": 1, "call_attempts": [{"reasoning_tokens": toks}]})
        escs.append({"idx": born, "kind": cause, "listed": order, "calls": calls})
    return {"rules": [b[2] for b in births], "records": rows, "edge_log": log,
            "escalations": escs}


def doors_run(sides=None):
    sides = sides or {"A": CEDE, "B": CLIMB, "C": CEDE, "D": CLIMB}
    cause = {b[2]["rule_id"]: b[1] for b in BIRTHS}
    born = {b[2]["rule_id"]: b[0] for b in BIRTHS}
    return {"listings": [{"born_at": born[n], "newborn": n, "gateway": "G", "side": s,
                          "cause": cause[n]} for n, s in sides.items()]}


def read(rec=None, drun=None, tag=None):
    return Q.read_run(rec or record(), drun or doors_run(), SPACE, tag=tag)


def gate(run, k):
    return next(g["passes"] for g in run["gates"] if g["gate"] == k)


class TestOneListing(unittest.TestCase):

    def test_a_drafts_key(self):
        a = r_("X", 0, BI, [BILLING, c_("severity", "eq", 4)])
        b = r_("Y", 1, BI, [c_("severity", "eq", 4), BILLING])
        self.assertEqual(Q.draft_key(a), Q.draft_key(b))
        self.assertNotEqual(Q.draft_key(a), Q.draft_key({**b, "action": T1}))

    def test_a_calls_reasoning_tokens(self):
        self.assertEqual(Q.reasoning_tokens({"call_attempts": [{"reasoning_tokens": 3},
                                                               {"reasoning_tokens": 4}]}), 7)
        self.assertIsNone(Q.reasoning_tokens({"call_attempts": [{"reasoning_tokens": None}]}))
        self.assertIsNone(Q.reasoning_tokens({"call_attempts": []}))
        self.assertIsNone(Q.reasoning_tokens(None))

    def test_the_rows(self):
        rec = record()
        rows = {r["newborn"]: r for r in Q.rows_of(rec, doors_run())}
        self.assertEqual(list(rows), ["A", "B", "C", "D"])
        for n, r in rows.items():
            listed = next(e["listed"] for e in rec["escalations"] if e["idx"] == r["born_at"])
            self.assertEqual(r["slot"], listed.index("G"))
            self.assertEqual(r["before_every_security"], r["slot"] < listed.index("U"))
            self.assertEqual(r["first_half"], r["slot"] * 2 < len(listed))
        self.assertEqual(rows["A"]["ceded_shown"], [])
        self.assertEqual(rows["D"]["ceded_shown"], ["A"])
        self.assertEqual(rows["D"]["climbed_shown"], [])
        self.assertEqual(rows["B"]["per_rule"], F(900, 3))
        self.assertEqual(rows["B"]["draft"], rows["C"]["draft"])


def row(side, draft="x", gateway="G", before=None, ceded=0, per=None):
    return {"side": side, "draft": draft, "gateway": gateway, "before_every_security": before,
            "ceded_shown": ceded, "per_rule": per}


class TestWhatTheRowsGive(unittest.TestCase):

    def test_the_same_drafts(self):
        rows = [row(CLIMB, "x"), row(CEDE, "x"), row(CEDE, "x"), row(CEDE, "y"), row(CLIMB, "z"),
                row(CLIMB, "z")]
        got = Q.same_drafts(rows)
        self.assertEqual((got["drafts"], got["repeated"], got["both_ways"]), (3, 2, 1))
        self.assertEqual((got["pairs"], got["disagree"]), (4, 2))
        p = F(3, 6)
        self.assertEqual(got["expected"]["fraction"], str(4 * 2 * p * (1 - p)))

    def test_a_draft_listed_two_gateways_is_two_drafts(self):
        got = Q.same_drafts([row(CLIMB, "x", "G"), row(CEDE, "x", "H")])
        self.assertEqual((got["drafts"], got["pairs"]), (2, 0))
        self.assertIsNone(got["expected"])

    def test_a_rate_by_a_feature(self):
        got = Q.by([row(CLIMB, before=True), row(CEDE, before=True), row(CEDE, before=False)],
                   lambda r: r["before_every_security"])
        self.assertEqual({k: (v["climbs"], v["of"]) for k, v in got.items()},
                         {"true": (1, 2), "false": (0, 1)})

    def test_the_lower_medians(self):
        got = Q.medians([row(CLIMB, per=F(1)), row(CLIMB, per=F(3)), row(CEDE, per=F(2)),
                         row(CEDE, per=None)])
        self.assertEqual((got[CLIMB]["fraction"], got[CEDE]["fraction"]), ("1", "2"))

    def test_the_keyword_placements(self):
        got = Q.keyword_placements(record(), SPACE)
        self.assertEqual(got, {T2: {CEDE: 2, CLIMB: 2}})


class TestTheGates(unittest.TestCase):

    def test_they_pass_on_the_run(self):
        run = read()
        self.assertEqual([g["gate"] for g in run["gates"]], [1, 2, 3, 4])
        self.assertTrue(all(g["passes"] for g in run["gates"]))

    def test_1_rebuilds_the_listings_from_the_record(self):
        self.assertEqual(Q.rebuilt(record(), {"G"}),
                         [(2, "A", "G", CEDE), (3, "B", "G", CLIMB), (4, "C", "G", CEDE),
                          (5, "D", "G", CLIMB)])
        self.assertEqual(Q.rebuilt(record(), set()), [])

    def test_1_fails_on_a_listing_left_out(self):
        drun = doors_run()
        drun["listings"] = drun["listings"][1:]
        self.assertFalse(gate(read(drun=drun), 1))

    def test_1_fails_on_another_side(self):
        self.assertFalse(gate(read(drun=doors_run({"A": CEDE, "B": CEDE, "C": CEDE,
                                                   "D": CLIMB})), 1))

    def test_2_fails_on_a_list_out_of_its_shuffle(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 5)
        esc["listed"] = list(reversed(esc["listed"]))
        if esc["listed"] == rp.listing(sorted(esc["listed"]), 5, 0):
            esc["listed"] = esc["listed"][1:] + esc["listed"][:1]
        self.assertFalse(gate(read(rec=rec), 2))

    def test_3_fails_on_a_call_without_its_reasoning_tokens(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 4)
        esc["calls"][-1]["call_attempts"] = []
        self.assertFalse(gate(read(rec=rec), 3))

    def test_4_fails_on_a_precedent_the_log_refused(self):
        edges = [e if e[:3] != (2, "G", "A") else (2, "G", "A", EDGE_CYCLE) for e in EDGES]
        self.assertFalse(gate(read(rec=record(edges=edges)), 4))

    def test_5_reads_the_development_set(self):
        dev = Q.development(Q.rows_of(record(), doors_run()))
        tag = Q.DEVELOPMENT_RUNS[0]
        with mock.patch.object(Q, "DEVELOPMENT", {tag: dev}):
            self.assertTrue(gate(read(tag=tag), 5))
        with mock.patch.object(Q, "DEVELOPMENT", {tag: {**dev, "climbs": 9}}):
            self.assertFalse(gate(read(tag=tag), 5))
        self.assertEqual((dev["pairs"], dev["disagree"]), (1, 1))
        self.assertEqual((dev["no_precedent"], dev["precedent"]), ([0, 1], [2, 3]))


def jrow(side, draft="x", before=None, ceded=0, per=None):
    return {**row(side, draft, "G", before, ceded),
            "per_rule": None if per is None else {"fraction": str(per)}}


def run_of(rows, pairs=0, disagree=0, expected=None):
    return {"rows": rows, "summary": {"same_drafts": {
        "pairs": pairs, "disagree": disagree,
        "expected": None if expected is None else {"fraction": str(expected)}}}}


L2, L3 = Q.HELD_OUT


class TestTheExpectation(unittest.TestCase):

    def clauses(self, runs):
        return {c["clause"]: c["holds"] for c in Q.read_expectation(runs)}

    def test_the_runs(self):
        self.assertEqual(Q.DEVELOPMENT_RUNS, ("l_r1", "n_r3"))
        self.assertEqual(Q.HELD_OUT, ("l_r2", "l_r3"))

    def test_every_clause_holds_at_its_line(self):
        # B1: 2 pairs disagree of the 4 expected. B2: 1/5 before against 1/10 after.
        # B3: 1/5 with no cede shown against 1/10 with one. B4: medians 5 and 4.
        rows = ([jrow(CLIMB, before=True, per=F(5))] + [jrow(CEDE, before=True, per=F(4))] * 4
                + [jrow(CLIMB, before=False, ceded=1, per=F(5))]
                + [jrow(CEDE, before=False, ceded=1, per=F(4))] * 9)
        runs = {L2: run_of(rows[:7], 3, 2, F(4)), L3: run_of(rows[7:], 2, 0, F(0))}
        self.assertEqual(self.clauses(runs),
                         {"B1": True, "B2": True, "B3": True, "B4": True})

    def test_every_clause_fails_past_its_line(self):
        rows = ([jrow(CLIMB, before=True, per=F(6))] * 3 + [jrow(CEDE, before=True, per=F(4))] * 2
                + [jrow(CLIMB, before=False, ceded=1, per=F(6))]
                + [jrow(CEDE, before=False, ceded=1, per=F(4))] * 9)
        runs = {L2: run_of(rows, 4, 1, F(4))}
        self.assertEqual(self.clauses(runs), {"B1": False, "B2": False, "B3": True, "B4": False})
        rows2 = ([jrow(CLIMB, before=True, ceded=1, per=F(4))] + [jrow(CEDE, before=True)] * 3
                 + [jrow(CEDE, before=False, ceded=0)] * 4)
        self.assertFalse(self.clauses({L2: run_of(rows2, 1, 1, F(1))})["B3"])

    def test_the_development_set_is_left_out(self):
        rows = [jrow(CLIMB, before=True)] * 5
        runs = {"l_r1": run_of(rows, 10, 0, F(5)), L2: run_of([], 0, 0, None)}
        self.assertEqual(self.clauses(runs), {k: False for k in ("B1", "B2", "B3", "B4")})

    def test_a_clause_over_nothing_fails(self):
        self.assertEqual(self.clauses({}), {k: False for k in ("B1", "B2", "B3", "B4")})


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(Q, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                Q.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
