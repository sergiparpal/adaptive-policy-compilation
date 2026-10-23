"""
`manual/notes.py`, the POST-RUN reading of the notes the proposer wrote beside
its rules in `PLAN_MANUAL.md`'s twelve loop runs: why the list makes it write
narrower rules, and why the catalogue makes it exclude the keyword.

WHAT IS PINNED HERE, AND WHY.
  * The codebook's fingerprint, written here a second time, so that an edit to a
    pattern after the commit that froze it shows in two places.
  * What each code matches and what it does not. The anchors keep a pattern
    from matching inside another word, as `PLAN_WHY.md`'s `m[aá]s condiciones`
    matched inside *"mismas condiciones"*. The boilerplate *no necesita declarar
    prioridad* is not a precedence. `H30` and `h12` are not hidden rules.
  * The sets: development is the first run, held-out the second and third.
  * Breadth: a birth narrow at its cut, the split read on the narrow rate, a
    code's mix and the tickets' mix on their common support, all on births built
    by hand.
  * The nesting in a cited rule on masks, and the citations' counts.
  * The keyword: a condition that admits only tickets with it, a run's rules
    read with their kind, their ticket's keyword and the rules shown, and a
    level's reading of them.
  * Each clause of the expectation at its edge.
  * The writer refusing unsigned before it reads a record, and an argument
    printing the docstring.

**No figure of the reading is pinned here**, and no test reads a loop record.
"""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from manual import notes as N
from manual import plan
from manual import readings as R

UNSIGNED = {"passes": False, "found": 1, "unsigned": 1}
KW = "has_security_keyword"


class TestTheNamesAndLines(unittest.TestCase):

    def test_the_names_it_reads_by(self):
        self.assertEqual(N.record_path(), Path("results_manual/notes.json"))
        self.assertEqual(N.NOTE_CUT, 280)
        self.assertEqual(N.NARROW_BANDS, ("b1", "b2"))
        self.assertEqual((N.LOW, N.HIGH), (2, 3))

    def test_the_sets_split_the_runs_by_repetition(self):
        self.assertEqual(N.SETS, {"development": (1,), "held_out": (2, 3),
                                  "all": (1, 2, 3)})
        self.assertEqual([N.set_of(r) for r in (1, 2, 3)],
                         ["development", "held_out", "held_out"])

    def test_the_expectations_lines(self):
        self.assertEqual(N.A1_RATIO, 2)
        self.assertEqual(N.A3_NESTED, Fraction(2, 3))
        self.assertEqual(N.A4_MIX, Fraction(1, 2))
        self.assertEqual((N.B1_MENTION, N.B2_MENTION, N.B3_PRECEDENCE, N.B4_MENTION,
                          N.B5_MENTION),
                         (Fraction(3, 4), Fraction(1, 10), Fraction(1, 2),
                          Fraction(1, 10), Fraction(1, 2)))


class TestTheCodebook(unittest.TestCase):

    def test_the_fingerprint_is_pinned(self):
        self.assertEqual(N.digest(), "bea660598e6499b7")
        self.assertEqual(N.CODEBOOK_DIGEST, "bea660598e6499b7")

    def test_the_ten_codes(self):
        self.assertEqual(set(N.CODES), {"hidden", "policy", "inside", "spec", "narrow",
                                        "widen", "gap", "analogy", "precedence",
                                        "keyword"})

    def test_each_code_on_notes_it_should_match(self):
        should = {
            "hidden": ["La regla H20 cubre el caso", "H04-H06"],
            "policy": ["Según la política, los de API van a ingeniería",
                       "lo dice el manual", "va a autoservicio (punto 3)",
                       "according to the policy"],
            "inside": ["La regla propuesta es un caso particular de H28",
                       "es un subcaso de H20", "es un sub-caso", "un subconjunto de R0010",
                       "This rule is a specific case of severity 1"],
            "spec": ["es más específica que R0010", "por ser mas especifica",
                     "a more specific rule"],
            "narrow": ["Se crea una regla específica para billing",
                       "Regla especifica para API con severidad alta",
                       "captura este perfil exacto"],
            "widen": ["La regla es generalizable", "La regla se abstrae a enterprise",
                      "Regla general para integraciones", "cualquier cliente business",
                      "cubre este caso y otros análogos", "captura el caso general"],
            "gap": ["Ninguna regla existente casa exactamente",
                    "No hay reglas existentes que cubran este perfil",
                    "No encaja en ninguna regla existente", "dejando un hueco",
                    "esta nueva regla es complementaria",
                    "las reglas existentes no cubren este caso", "no existing rule covers"],
            "analogy": ["Por analogía con R0005", "siguiendo el patrón de otras reglas",
                        "coherente con el patrón", "(similar a R0004 para severity 2)"],
            "precedence": ["La seguridad tiene prioridad absoluta",
                           "debe prevalecer sobre R0047", "la política prioriza la seguridad",
                           "la seguridad es prioritaria", "debe imponerse sobre la otra",
                           "debe aplicarse primero", "security takes precedence"],
            "keyword": ["sin keyword de seguridad", "has_security_keyword=true",
                        "no va a SECURITY_INCIDENT", "sin palabra clave"],
        }
        for c, phrases in should.items():
            for p in phrases:
                self.assertIn(c, N.code(p), (c, p))

    def test_the_anchors_keep_a_pattern_inside_its_word(self):
        should_not = {
            "spec": ["mismas condiciones", "es más general"],
            "keyword": ["la inseguridad del cliente"],
            "precedence": ["no necesita declarar prioridad", "no se declaran prioridades",
                           "sin prioridad alta"],
            "policy": ["se hizo manualmente", "es políticamente neutro"],
            "inside": ["un caso particularmente raro"],
            "hidden": ["H30", "H00", "h12", "SH12", "H1 y H2"],
            "widen": ["el nivel de abstracción elegido"],
            "gap": ["H28 no cubre severity 4"],
        }
        for c, phrases in should_not.items():
            for p in phrases:
                self.assertNotIn(c, N.code(p), (c, p))
        self.assertEqual(N.code("mismas condiciones"), frozenset())

    def test_hidden_is_case_sensitive_and_the_rest_are_not(self):
        self.assertNotIn("hidden", N.code("h20"))
        self.assertIn("analogy", N.code("POR ANALOGÍA CON R0001"))

    def test_the_cited_rules_in_order_once(self):
        self.assertEqual(N.cited("H28 (enterprise) y H29; otra vez H28; H30 y h12 no"),
                         ("H28", "H29"))
        self.assertEqual(N.cited("H04-H06"), ("H04", "H06"))
        self.assertEqual(N.cited(""), ())


class TestBreadth(unittest.TestCase):

    CUTS = [240.0, 840.0, 1680.0]

    def test_a_birth_is_narrow_up_to_the_second_cut(self):
        self.assertEqual([N.narrow(p, self.CUTS) for p in (1, 240, 840, 841, 5000)],
                         [True, True, True, False, False])

    def test_the_split_read_on_the_narrow_rate(self):
        items = [({"narrow": True}, "x"), ({"narrow": False}, "x"), ({"narrow": True}, "y")]
        s = N.narrow_split(items, ("x", "y"))
        self.assertEqual((s["births"], s["alone"], s["k_a"]), (3, 2, Fraction(2, 3)))
        self.assertEqual(N.shown_split(s),
                         {"births": 3, "narrow": 2, "narrow_share": Fraction(2, 3),
                          "parts": {"x": {"births": 2, "narrow": 1},
                                    "y": {"births": 1, "narrow": 1}}})

    def test_a_codes_births_beside_the_rest(self):
        bs = [{"codes": ["inside"], "narrow": True, "points_outside": 100},
              {"codes": ["inside", "gap"], "narrow": False, "points_outside": 900},
              {"codes": [], "narrow": True, "points_outside": 50}]
        c = N.by_code(bs)["inside"]
        self.assertEqual(c["with"], {"births": 2, "narrow": 1, "narrow_share": Fraction(1, 2),
                                     "points_median": 500.0})
        self.assertEqual(c["without"], {"births": 1, "narrow": 1, "narrow_share": 1,
                                        "points_median": 50})
        self.assertEqual(N.by_code([])["gap"]["with"]["points_median"], None)

    def test_a_codes_mix_split_exactly(self):
        def births(spec):
            return [{"codes": ["inside"] if w else [], "narrow": n} for w, n in spec]
        low = births([(True, True), (False, True), (False, False), (False, False)])
        high = births([(True, True), (True, True), (True, True), (False, False)])
        m = N.code_mix(low, high, "inside")
        self.assertEqual(m["gap"], Fraction(1, 4))
        self.assertEqual(m["low_rates_on_high_mix"], Fraction(5, 6))
        self.assertEqual(m["mix_share_low_rates"], Fraction(4, 3))
        self.assertEqual(m["high_rates_on_low_mix"], Fraction(1, 4))
        self.assertEqual(m["mix_share_high_rates"], Fraction(2))

    def test_the_tickets_mix_reads_the_common_support(self):
        low = [{"truth": "A", "narrow": True}, {"truth": "B", "narrow": False},
               {"truth": "B", "narrow": True}]
        high = [{"truth": "B", "narrow": True}, {"truth": "C", "narrow": True},
                {"truth": "C", "narrow": False}]
        m = N.ticket_mix(low, high)
        self.assertEqual(m["queues"], ["B"])
        self.assertEqual(m["dropped"], {"low": 1, "high": 2})
        self.assertEqual((m["low"]["births"], m["high"]["births"]), (2, 1))
        self.assertEqual(m["gap"], Fraction(1, 2))
        # One queue left: the mix carries none of the gap, under either reading.
        self.assertEqual((m["mix_share_low_rates"], m["mix_share_high_rates"]), (0, 0))

    def test_cuts_compared_with_a_tolerance(self):
        self.assertTrue(N.same_cuts([240.0, 840.0], [240.0 + 1e-13, 840.0]))
        self.assertFalse(N.same_cuts([240.0, 840.0], [241.0, 840.0]))
        self.assertFalse(N.same_cuts([240.0], [240.0, 840.0]))


class TestCitations(unittest.TestCase):

    HIDDEN = {"H01": {"ext": 0b0001}, "H02": {"ext": 0b0011}, "H03": {"ext": 0b1000}}

    def coded(self):
        births = [{"rule_id": "R1", "born_at": 0, "queue": "Q", "truth": "Q",
                   "ticket_rule": "H01", "right_queue": True, "crosses": False,
                   "points_outside": 2},
                  {"rule_id": "R2", "born_at": 1, "queue": "P", "truth": "Q",
                   "ticket_rule": "H03", "right_queue": False, "crosses": True,
                   "points_outside": 5},
                  {"rule_id": "R3", "born_at": 2, "queue": "Q", "truth": "Q",
                   "ticket_rule": "H01", "right_queue": True, "crosses": False,
                   "points_outside": 1}]
        notes = {"R1": "es un caso particular de H02 y de H01", "R2": "H01 aplica",
                 "R3": "ninguna regla existente"}
        ext = {"R1": 0b0010, "R2": 0b0010, "R3": 0b0100}
        return N.births_coded(births, notes, ext, self.HIDDEN, [1.0, 2.0, 3.0])

    def test_a_birth_nested_in_a_rule_its_note_cites(self):
        b1, b2, b3 = self.coded()
        self.assertEqual((b1["cited"], b1["codes"]), (["H02", "H01"], ["hidden", "inside"]))
        self.assertTrue(b1["nested_in_cited"] and b1["cites_ticket_rule"] and b1["narrow"])
        self.assertFalse(b2["nested_in_cited"] or b2["cites_ticket_rule"] or b2["narrow"])
        self.assertEqual((b3["cited"], b3["nested_in_cited"]), ([], False))

    def test_the_citations_counted(self):
        c = N.citations(self.coded())
        self.assertEqual({k: c[k] for k in ("births", "citing", "nested_in_cited",
                                            "inside_citing", "inside_nested",
                                            "cites_ticket_rule")},
                         {"births": 3, "citing": 2, "nested_in_cited": 1,
                          "inside_citing": 1, "inside_nested": 1, "cites_ticket_rule": 1})
        self.assertEqual(c["right_queue"], {"cites_ticket_rule": [1, 1], "does_not": [0, 1]})
        self.assertEqual(c["most_cited"], [("H01", 2), ("H02", 1)])


class TestTheKeyword(unittest.TestCase):

    def toy(self):
        def rule(rid, born, action, note, conds, beats=()):
            return {"rule_id": rid, "born_at": born, "action": action, "note": note,
                    "conditions": conds, "beats": list(beats), "loses_to": [],
                    "dropped_edges": []}
        record = {"rules": [
            rule("R0001", 0, "T1_GENERAL", "sin keyword de seguridad",
                 [{"attr": KW, "op": "eq", "value": False}]),
            rule("R0002", 1, "SECURITY_INCIDENT", "La seguridad tiene prioridad absoluta",
                 [{"attr": KW, "op": "eq", "value": True}], beats=["R0001"]),
            rule("R0003", 2, "T2_TECHNICAL", "Por analogía con R0001",
                 [{"attr": "severity", "op": "eq", "value": 2}])],
            "records": [{"idx": 0, "shown_ids": []}, {"idx": 1, "shown_ids": ["R0001"]},
                        {"idx": 2, "shown_ids": ["R0001", "R0002"]}]}
        ext = {"R0001": 0b0011, "R0002": 0b1100, "R0003": 0b0101}
        corpus = [SimpleNamespace(has_security_keyword=k) for k in (False, True, False)]
        return N.rules_read(record, ext, 0b0011, corpus)

    def test_conditions_that_admit_only_true(self):
        yes = [{"attr": KW, "op": "eq", "value": True},
               {"attr": KW, "op": "neq", "value": False},
               {"attr": KW, "op": "in", "value": [True]}]
        no = [{"attr": KW, "op": "eq", "value": False},
              {"attr": KW, "op": "in", "value": [False, True]},
              {"attr": "off_hours", "op": "eq", "value": True}]
        self.assertTrue(all(N.admits_only_true(c) for c in yes))
        self.assertFalse(any(N.admits_only_true(c) for c in no))

    def test_a_runs_rules_read(self):
        r1, r2, r3 = self.toy()
        self.assertEqual([r["rule_id"] for r in (r1, r2, r3)], ["R0001", "R0002", "R0003"])
        self.assertEqual((r1["keyword_rule"], r1["excludes"], r1["ticket_keyword"],
                          r1["shown_excluding"], r1["declared"], r1["codes"]),
                         (False, True, False, False, False, ["keyword"]))
        self.assertEqual((r2["keyword_rule"], r2["excludes"], r2["ticket_keyword"],
                          r2["shown_excluding"], r2["declared"], r2["codes"]),
                         (True, False, True, True, True, ["keyword", "precedence"]))
        self.assertEqual((r3["keyword_rule"], r3["excludes"], r3["shown_excluding"],
                          r3["shown"], r3["codes"]),
                         (False, False, True, ["R0001", "R0002"], ["analogy"]))

    def test_a_levels_keyword_reading(self):
        b = N.level_b(self.toy())
        self.assertEqual((b["rules"], b["excludes"], b["keyword_rules"]), (3, 1, 1))
        self.assertEqual(b["ordinary"], {"rules": 2, "mention": 1,
                                         "excludes": {"rules": 1, "mention": 1},
                                         "does_not": {"rules": 1, "mention": 0}})
        self.assertEqual(b["excluding"], {"rules": 1, "mention": 1})
        self.assertEqual(b["keyword_rule_notes"],
                         {"rules": 1, "precedence": 1, "mention": 1, "declared": 1})
        self.assertEqual(b["imitation"],
                         {"shown_excluding": {"rules": 2, "excludes": 0},
                          "none_shown_excluding": {"rules": 1, "excludes": 1}})


def drafted(**over):
    """A world where every clause holds; `over` replaces one piece. Paths run
    through the dicts with `__`."""
    def codes(**c):
        out = {}
        for k in N.CODES:
            wb, wn, ob, on = c.get(k, (0, 0, 10, 5))
            out[k] = {"with": {"births": wb, "narrow": wn, "narrow_share": R.share(wn, wb)},
                      "without": {"births": ob, "narrow": on,
                                  "narrow_share": R.share(on, ob)}}
        return out
    A = {"levels": {
        "2": {"births": 20, "codes": codes(inside=(2, 1, 18, 6), policy=(10, 2, 10, 5)),
              "citations": {"inside_citing": 0, "inside_nested": 0}},
        "3": {"births": 20, "codes": codes(inside=(4, 3, 16, 8)),
              "citations": {"inside_citing": 3, "inside_nested": 2}}},
        "ticket_mix": {"gap": Fraction(1, 5), "mix_share_low_rates": Fraction(1, 4),
                       "mix_share_high_rates": Fraction(2, 5)}}
    B = {"levels": {
        "1": {"excluding": {"rules": 4, "mention": 3},
              "ordinary": {"rules": 6, "mention": 3},
              "imitation": {"shown_excluding": {"rules": 4, "excludes": 3},
                            "none_shown_excluding": {"rules": 4, "excludes": 1}}},
        "2": {"ordinary": {"rules": 11, "mention": 1},
              "keyword_rule_notes": {"rules": 4, "precedence": 2}},
        "3": {"ordinary": {"rules": 20, "mention": 1}}}}
    world = {"A": A, "B": B}
    for path, value in over.items():
        node = world
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    return {e["clause"]: e["holds"] for e in N.read_expectation(world["A"], world["B"])}


class TestTheExpectationAtItsEdges(unittest.TestCase):

    def test_every_clause_holds_on_the_drafted_world(self):
        self.assertEqual(drafted(), {c: True for c in (
            "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "B6")})

    def test_a1_at_twice_and_never_on_nothing(self):
        self.assertFalse(drafted(A__levels__3__codes__inside__with__births=3)["A1"])
        self.assertFalse(drafted(A__levels__2__codes__inside__with__births=0,
                                 A__levels__3__codes__inside__with__births=0)["A1"])
        self.assertTrue(drafted(A__levels__2__codes__inside__with__births=0,
                                A__levels__3__codes__inside__with__births=1)["A1"])

    def test_a2_and_a5_are_strict(self):
        self.assertFalse(drafted(
            A__levels__3__codes__inside__with__narrow_share=Fraction(1, 2))["A2"])
        self.assertFalse(drafted(
            A__levels__2__codes__policy__with__narrow_share=Fraction(1, 2))["A5"])
        self.assertFalse(drafted(
            A__levels__2__codes__policy__with__narrow_share=None)["A5"])

    def test_a3_at_two_thirds_and_never_on_nothing(self):
        self.assertFalse(drafted(A__levels__3__citations={"inside_citing": 2,
                                                          "inside_nested": 1})["A3"])
        self.assertFalse(drafted(A__levels__3__citations={"inside_citing": 0,
                                                          "inside_nested": 0})["A3"])

    def test_a4_needs_a_positive_gap_and_both_shares_under_a_half(self):
        self.assertFalse(drafted(A__ticket_mix__gap=Fraction(0))["A4"])
        self.assertFalse(drafted(A__ticket_mix__gap=Fraction(-1, 5))["A4"])
        self.assertFalse(drafted(A__ticket_mix__mix_share_high_rates=Fraction(1, 2))["A4"])
        self.assertFalse(drafted(A__ticket_mix__mix_share_low_rates=None)["A4"])

    def test_b1_b3_and_b5_at_their_lines_and_never_on_nothing(self):
        self.assertFalse(drafted(B__levels__1__excluding={"rules": 3, "mention": 2})["B1"])
        self.assertFalse(drafted(B__levels__1__excluding={"rules": 0, "mention": 0})["B1"])
        self.assertFalse(drafted(B__levels__2__keyword_rule_notes={"rules": 3,
                                                                   "precedence": 1})["B3"])
        self.assertFalse(drafted(B__levels__2__keyword_rule_notes={"rules": 0,
                                                                   "precedence": 0})["B3"])
        self.assertFalse(drafted(B__levels__1__ordinary={"rules": 5, "mention": 2})["B5"])

    def test_b2_and_b4_are_strict_at_a_tenth(self):
        self.assertFalse(drafted(B__levels__2__ordinary={"rules": 10, "mention": 1})["B2"])
        self.assertFalse(drafted(B__levels__3__ordinary={"rules": 20, "mention": 2})["B4"])
        self.assertFalse(drafted(B__levels__3__ordinary={"rules": 0, "mention": 0})["B4"])

    def test_b6_is_strict_and_needs_both_groups(self):
        same = {"shown_excluding": {"rules": 4, "excludes": 1},
                "none_shown_excluding": {"rules": 4, "excludes": 1}}
        self.assertFalse(drafted(B__levels__1__imitation=same)["B6"])
        empty = {"shown_excluding": {"rules": 4, "excludes": 3},
                 "none_shown_excluding": {"rules": 0, "excludes": 0}}
        self.assertFalse(drafted(B__levels__1__imitation=empty)["B6"])


class TestNothingIsReadUnsigned(unittest.TestCase):

    def test_the_writer_refuses_before_reading_a_record(self):
        with mock.patch.object(plan, "gate_signature", return_value=UNSIGNED), \
             mock.patch.object(R, "load_runs",
                               side_effect=AssertionError("read")) as read:
            with self.assertRaises(SystemExit):
                N.main([])
        read.assert_not_called()

    def test_an_argument_prints_the_docstring(self):
        with mock.patch("builtins.print"):
            self.assertEqual(N.main(["--help"]), 2)


if __name__ == "__main__":
    unittest.main()
