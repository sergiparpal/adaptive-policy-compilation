"""
`corrections/conditions.py` — the POST-RUN reading of what makes an answer read
the list by its conditions, no figure.

What is pinned is the instrument, on one run built by hand, each round's list in
v1c's seeded shuffle. Three rules are born without a list: `U` and `V` of
SECURITY_INCIDENT on the keyword, and `X` of T2_TECHNICAL. Five newborns are
listed rules:
- `A`, of BILLING_SPECIALIST, cedes to `U` and `V`, and its reasoning weighs
  the queue;
- `B`, a draft of four conditions, climbs over `U`, reasoning little and only
  of conditions;
- `C` cedes to `U`, and its list shows `A` ceding to `U`;
- `D` climbs over `U`, its list showing `B` above `U`, and reasons long;
- `E`, of SECURITY_INCIDENT, is not read.
Also pinned:
- the length bins, the passages, and a side;
- each round's order, precedent, reasoning and codes;
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

from corrections import conditions as C
from corrections import plan
from reasoned_loop import protocol as rp
from rung2.engine2 import EDGE_CYCLE, EDGE_OK

F = Fraction
T1, T2, BI, SS, SEC = ("T1_GENERAL", "T2_TECHNICAL", "BILLING_SPECIALIST",
                       "SELF_SERVICE_DEFLECT", "SECURITY_INCIDENT")
IMP, ERR, CON = plan.IMPASSE, plan.ERROR, "CONFLICT"
UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
CLIMB, CEDE, OTHER = C.CLIMB, C.CEDE, C.OTHER


def c_(attr, op, value):
    return {"attr": attr, "op": op, "value": value}


KEYWORD = c_("has_security_keyword", "eq", True)


def r_(rid, born, action, conds, beats=(), loses_to=()):
    return {"rule_id": rid, "born_at": born, "action": action, "conditions": list(conds),
            "beats": list(beats), "loses_to": list(loses_to), "dropped_edges": []}


# born_at, cause, rule, the rules its round lists, its reasoning, its reasoning tokens.
BIRTHS = [
    (0, IMP, r_("U", 0, SEC, [KEYWORD]), [], None, None),
    (1, IMP, r_("V", 1, SEC, [KEYWORD, c_("severity", "eq", 1)]), [], None, None),
    (2, IMP, r_("X", 2, T2, [c_("product", "eq", "api")]), [], None, None),
    (4, ERR, r_("A", 4, BI, [c_("product", "eq", "billing")], beats=["X"], loses_to=["U", "V"]),
     ["U", "V", "X"],
     "U: security incidents take priority, so we lose to U.\nV: the same.\n"
     "X is an API rule, and ours is more specific.", 900),
    (5, IMP, r_("B", 5, T2, [c_("customer_tier", "eq", "free"), c_("severity", "eq", 2),
                             c_("product", "eq", "mobile"), c_("channel", "eq", "chat")],
                beats=["U"]), ["U"],
     "U requires only the keyword.\nOur rule is more specific: it adds conditions.\n"
     "So it beats U.", 300),
    (6, CON, r_("C", 6, T1, [c_("customer_tier", "eq", "pro")], beats=["X", "A"],
                loses_to=["U"]), ["U", "X", "A"],
     "Rule U is critical security.\nWe lose to U.\n\nX and A are below us.", 1500),
    (7, ERR, r_("D", 7, SS, [c_("product", "eq", "mobile"), c_("off_hours", "eq", True)],
                beats=["U", "B"]), ["U", "B"],
     "U has one condition, so it is more general.\nOurs is the exception.\n"
     "We beat U and B.", 2000),
    (8, CON, r_("E", 8, SEC, [KEYWORD, c_("channel", "eq", "email")], beats=["X"]), ["X"],
     "X: security first.", 400),
]
# The edges each birth tried, with the record's verdicts.
EDGES = [(4, "A", "X"), (4, "U", "A"), (4, "V", "A"), (5, "B", "U"), (6, "C", "X"),
         (6, "C", "A"), (6, "U", "C"), (7, "D", "U"), (7, "D", "B"), (8, "E", "X")]


def record(births=None, edges=None):
    births = births or BIRTHS
    rows = [{"idx": b[0], "edge_reasons": []} for b in births]
    by = {r["idx"]: r for r in rows}
    log = []
    for born, w, l, *why in (edges if edges is not None else EDGES):
        reason = why[0] if why else EDGE_OK
        by[born]["edge_reasons"].append(reason)
        log.append([w, l, reason])
    escs = []
    for born, cause, rule, listed, text, toks in births:
        order = rp.listing(sorted(listed), born, 0) if listed else []
        calls = [{"round": 0, "listed": list(order)}]
        if listed:
            calls.append({"round": 1, "reasoning": text,
                          "call_attempts": [{"reasoning_tokens": toks}]})
        escs.append({"idx": born, "kind": cause, "listed": order, "calls": calls})
    return {"rules": [copy.deepcopy(b[2]) for b in births], "records": rows, "edge_log": log,
            "escalations": escs}


TOWARD = {"A": C.BELOW, "B": C.ABOVE, "C": C.BELOW, "D": C.ABOVE}
SECURITY = {"A": 2, "B": 1, "C": 1, "D": 1}


def above_run(toward=None):
    toward = toward or TOWARD
    born = {b[2]["rule_id"]: (b[0], b[2]["action"]) for b in BIRTHS}
    rows = [{"born_at": born[n][0], "newborn": n, "queue": born[n][1], "security": SECURITY[n],
             "security_toward": t} for n, t in toward.items()]
    rows.append({"born_at": 8, "newborn": "E", "queue": SEC, "security": 0,
                 "security_toward": C.dr.NONE_LISTED})
    return {"rounds": rows}


def read(rec=None, arun=None, tag=None):
    return C.read_run(rec or record(), arun or above_run(), tag=tag)


def gate(run, k):
    return next(g["passes"] for g in run["gates"] if g["gate"] == k)


def by_newborn(rows):
    return {r["newborn"]: r for r in rows}


class TestOneRound(unittest.TestCase):

    def test_the_length_bins(self):
        self.assertEqual([C.length_bin(n) for n in (1, 3, 4, 8, 9, 20, 21, 50, 51, 140)],
                         ["1-3", "1-3", "4-8", "4-8", "9-20", "9-20", "21-50", "21-50", "51+",
                          "51+"])
        with self.assertRaises(ValueError):
            C.length_bin(0)

    def test_the_passages(self):
        text = "a\nR001 is security\nb\nc\nd\nR0010 is not\ne"
        self.assertEqual(C.passages(text, ["R001"]), "R001 is security\nb\nc")
        self.assertEqual(C.passages(text, ["R0010"]), "R0010 is not\ne")
        self.assertEqual(C.passages(text, ["R9"]), "")

    def test_a_side(self):
        self.assertEqual([C.side_of(t) for t in (C.ABOVE, C.BELOW, C.MIXED)],
                         [CLIMB, CEDE, OTHER])

    def test_the_rounds(self):
        rec = record()
        rows = by_newborn(C.rounds(rec))
        self.assertEqual(sorted(rows), ["A", "B", "C", "D"])
        self.assertEqual({k: r["side"] for k, r in rows.items()},
                         {"A": CEDE, "B": CLIMB, "C": CEDE, "D": CLIMB})
        for e in rec["escalations"]:
            if e["idx"] in (4, 5, 6, 7):
                r = next(x for x in rows.values() if x["born_at"] == e["idx"])
                secs = [x for x in e["listed"] if x in ("U", "V")]
                self.assertEqual(r["opens"], e["listed"][0] in secs)
                self.assertEqual(r["opens_expected"], F(len(secs), len(e["listed"])))
        self.assertEqual((rows["C"]["ceding_shown"], rows["C"]["climbing_shown"]), (1, 0))
        self.assertEqual((rows["D"]["ceding_shown"], rows["D"]["climbing_shown"]), (0, 1))
        self.assertEqual({k: (r["priority"], r["conditions_code"], r["conditions_no_priority"])
                          for k, r in rows.items()},
                         {"A": (True, True, False), "B": (False, True, True),
                          "C": (True, False, False), "D": (False, True, True)})
        self.assertEqual({k: (r["reasoning_tokens"], r["bin"]) for k, r in rows.items()},
                         {"A": (900, "1-3"), "B": (300, "1-3"), "C": (1500, "1-3"),
                          "D": (2000, "1-3")})


class TestWhatTheRoundsGive(unittest.TestCase):

    def rows(self):
        return C.rounds(record())

    def test_the_opening(self):
        rows = self.rows()
        got = C.opening(rows)
        self.assertEqual(got["rounds"], 4)
        self.assertEqual(got["opens"], sum(r["opens"] for r in rows))
        self.assertEqual(F(got["expected"]["fraction"]), F(2, 3) + 1 + F(1, 3) + F(1, 2))

    def test_the_medians_and_the_climbs_below_them(self):
        rows = self.rows()
        self.assertEqual(C.medians(rows), {"1-3": 900})
        self.assertEqual(C.below_median(rows), (1, 2))
        lone = [{**r, "bin": "51+"} if r["newborn"] == "D" else r for r in rows]
        self.assertEqual(C.below_median(lone), (1, 1))

    def test_the_codes(self):
        rows = self.rows()
        self.assertEqual(C.coded(rows, CLIMB, "conditions_no_priority"), (2, 2))
        self.assertEqual(C.coded(rows, CEDE, "priority"), (2, 2))

    def test_the_summary(self):
        s = C.summary(self.rows())
        self.assertEqual(s["sides"], {CLIMB: 2, CEDE: 2, OTHER: 0})
        self.assertEqual(s["cede_medians"], {"1-3": 900})
        self.assertEqual((s["climbs_below_median"]["part"], s["climbs_below_median"]["of"]),
                         (1, 2))
        self.assertEqual({k: (v["part"], v["of"]) for k, v in s["codes"][CEDE].items()},
                         {"passage": (2, 2), "priority": (2, 2), "conditions_code": (1, 2),
                          "conditions_no_priority": (0, 2)})

    def test_the_also_read_part(self):
        al = C.also(self.rows())
        self.assertEqual(al["by_climbing_shown"],
                         {"none": {"climbs": 1, "of": 3}, "some": {"climbs": 1, "of": 1}})
        self.assertEqual(al["by_cause"], {CON: {"climbs": 0, "of": 1},
                                          ERR: {"climbs": 1, "of": 2},
                                          IMP: {"climbs": 1, "of": 1}})
        self.assertEqual(sum(v["of"] for v in al["by_length_and_precedent"].values()), 4)
        self.assertEqual(al["by_length_and_precedent"]["1-3/a_third_or_more"],
                         {"climbs": 0, "of": 1})
        self.assertEqual([(c["newborn"], c["cede_median"]) for c in al["climbs"]],
                         [("B", 900), ("D", 900)])

    def test_the_development_counts(self):
        dev = C.development(self.rows())
        self.assertEqual(dev["rounds"], 4)
        self.assertEqual(dev["sides"], {CLIMB: 2, CEDE: 2, OTHER: 0})
        self.assertEqual(dev["climbs_below_median"], [1, 2])
        self.assertEqual((dev["climbs_conditions_no_priority"], dev["cedes_conditions_no_priority"],
                          dev["climbs_priority"], dev["cedes_priority"]),
                         ([2, 2], [0, 2], [0, 2], [2, 2]))
        self.assertIsInstance(dev["climbs_open"][1], float)


class TestTheGates(unittest.TestCase):

    def test_they_pass_on_the_run(self):
        run = read()
        self.assertEqual([g["gate"] for g in run["gates"]], [1, 2, 3, 4])
        self.assertTrue(all(g["passes"] for g in run["gates"]))

    def test_1_fails_on_another_side(self):
        self.assertFalse(gate(read(arun=above_run({**TOWARD, "D": C.MIXED})), 1))

    def test_1_fails_on_a_round_left_out(self):
        self.assertFalse(gate(read(arun=above_run({k: v for k, v in TOWARD.items()
                                                   if k != "B"})), 1))

    def test_2_fails_on_a_list_out_of_its_shuffle(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 4)
        esc["listed"] = list(reversed(esc["listed"]))
        if esc["listed"] == rp.listing(sorted(esc["listed"]), 4, 0):
            esc["listed"] = esc["listed"][1:] + esc["listed"][:1]
        self.assertFalse(gate(read(rec=rec), 2))

    def test_3_fails_on_a_call_without_its_reasoning_tokens_or_its_reasoning(self):
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 6)
        esc["calls"][-1]["call_attempts"] = []
        self.assertFalse(gate(read(rec=rec), 3))
        rec = record()
        esc = next(e for e in rec["escalations"] if e["idx"] == 5)
        esc["calls"][-1]["reasoning"] = ""
        self.assertFalse(gate(read(rec=rec), 3))

    def test_4_fails_on_a_precedent_the_log_refused(self):
        edges = [e if e[:3] != (4, "U", "A") else (4, "U", "A", EDGE_CYCLE) for e in EDGES]
        self.assertFalse(gate(read(rec=record(edges=edges)), 4))

    def test_5_reads_the_development_set(self):
        dev = C.development(C.rounds(record()))
        tag = C.DEVELOPMENT_RUNS[0]
        with mock.patch.object(C, "DEVELOPMENT", {tag: dev}):
            self.assertTrue(gate(read(tag=tag), 5))
        with mock.patch.object(C, "DEVELOPMENT", {tag: {**dev, "rounds": 9}}):
            self.assertFalse(gate(read(tag=tag), 5))
        self.assertEqual([g["gate"] for g in read(tag="l_r2")["gates"]], [1, 2, 3, 4])


def row(side, opens=False, exp="1/2", bin_="4-8", toks=100, cnp=False):
    return {"side": side, "opens": opens, "opens_expected": exp, "bin": bin_,
            "reasoning_tokens": toks, "conditions_no_priority": cnp}


L2, L3 = C.HELD_L
N1, N2 = C.HELD_N
CEDES = [row(CEDE, toks=t) for t in (100, 200, 300)]


class TestTheExpectation(unittest.TestCase):

    def verdicts(self, by_tag):
        runs = {t: {"rounds": list(v)} for t, v in by_tag.items()}
        return {c["clause"]: c["holds"] for c in C.read_expectation(runs)}

    def test_the_runs(self):
        self.assertEqual(C.DEVELOPMENT_RUNS, ("l_r1", "n_r3"))
        self.assertEqual(C.HELD_OUT, ("l_r2", "l_r3", "n_r1", "n_r2"))

    def test_c1_at_its_line(self):
        climbs = [row(CLIMB, opens=True)] + [row(CLIMB)] * 3
        self.assertTrue(self.verdicts({L2: climbs})["C1"])
        self.assertFalse(self.verdicts({L2: [row(CLIMB)] * 4})["C1"])
        self.assertFalse(self.verdicts({L2: [row(CLIMB, opens=True, exp="0")]})["C1"])

    def test_c2_and_c5_at_their_line(self):
        ok = CEDES + [row(CLIMB, toks=150), row(CLIMB, toks=150), row(CLIMB, toks=250)]
        got = self.verdicts({L2: ok, N1: ok})
        self.assertEqual((got["C2"], got["C5"]), (True, True))
        past = CEDES + [row(CLIMB, toks=150), row(CLIMB, toks=250), row(CLIMB, toks=250)]
        got = self.verdicts({L2: ok, N1: past})
        self.assertEqual(got["C5"], False)
        got = self.verdicts({L2: past, N2: past})
        self.assertEqual((got["C2"], got["C5"]), (False, False))
        # A climb whose length of list has no cede is left out.
        got = self.verdicts({L3: ok + [row(CLIMB, bin_="51+", toks=9000)], N2: ok})
        self.assertEqual((got["C2"], got["C5"]), (True, True))
        self.assertFalse(self.verdicts({L2: ok})["C5"])

    def test_c3_and_c4_at_their_line(self):
        rows = ([row(CLIMB, cnp=True), row(CLIMB)] + [row(CEDE, cnp=True)]
                + [row(CEDE)] * 9)
        got = self.verdicts({N2: rows})
        self.assertEqual((got["C3"], got["C4"]), (True, True))
        rows = [row(CLIMB)] * 2 + [row(CEDE, cnp=True)] * 2 + [row(CEDE)] * 8
        got = self.verdicts({N2: rows})
        self.assertEqual((got["C3"], got["C4"]), (False, False))

    def test_the_development_set_is_left_out(self):
        rows = CEDES + [row(CLIMB, opens=True, toks=1, cnp=True)] * 3
        got = self.verdicts({"l_r1": rows, "n_r3": rows})
        self.assertEqual(got, {k: False for k in ("C1", "C2", "C3", "C4", "C5")})

    def test_a_clause_over_nothing_fails(self):
        got = {c["clause"]: c["holds"] for c in C.read_expectation({})}
        self.assertEqual(got, {k: False for k in ("C1", "C2", "C3", "C4", "C5")})


class TestAddedAfterTheFirstRun(unittest.TestCase):
    """Whether the reasoning names a listed security rule only in lines that
    enumerate the list."""

    def test_a_line_that_enumerates(self):
        listed = ["U", "X", "A", "B"]
        self.assertTrue(C.enumerated_only("All: U, X, A.\nPut them in beats.", listed, ["U"]))
        self.assertFalse(C.enumerated_only("All: U, X, A.\nU is security.", listed, ["U"]))
        self.assertFalse(C.enumerated_only("U and X.", listed, ["U"]))
        self.assertFalse(C.enumerated_only("X, A and B.", listed, ["U"]))
        self.assertTrue(C.enumerated_only("U, X, A, B", ["U", "X", "A", "B", "Y", "Z"], ["U"]))
        self.assertFalse(C.enumerated_only("U, X, A", ["U", "X", "A", "B", "Y", "Z", "W"], ["U"]))

    def test_on_the_run(self):
        run = read()
        self.assertEqual(run["added_after_the_first_run"],
                         {CEDE: {"named_apart": 2}, CLIMB: {"named_apart": 2}})
        births = [b if b[2]["rule_id"] != "C" else
                  (b[0], b[1], b[2], b[3], "In order: U, X and A.\nAll below us.", b[5])
                  for b in BIRTHS]
        run = read(rec=record(births))
        self.assertEqual(run["added_after_the_first_run"][CEDE],
                         {"enumerated_only": 1, "named_apart": 1})
        self.assertEqual([g["gate"] for g in run["gates"]], [1, 2, 3, 4])


class TestTheWriter(unittest.TestCase):

    def test_it_refuses_unsigned_before_it_reads_or_writes(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
                mock.patch.object(C, "read_all", side_effect=AssertionError("read")):
            with self.assertRaises(SystemExit) as got:
                C.main([])
        self.assertIn("unsigned", str(got.exception))


if __name__ == "__main__":
    unittest.main()
