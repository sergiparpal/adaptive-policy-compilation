"""
`G-g1` to `G-g4` of `PLAN_MANUAL.md` §7: the blocking checks, all free.

They run before any record of the plan is written, and **any failure stops the
plan before a figure exists**. They were written and run before the signature,
so that a failure would become a fix to the draft rather than a signed
amendment.

  G-g1  The instrument reproduces the records. The suite is green. The
        hidden policy, written as a compile answer and installed by
        `manual/compile.py`, derives `rung2.hidden_priority`'s 199 edges pair
        by pair, refuses none, has no inversion, and scores 1.0000 on both
        surfaces, by masks, by first match and by `measure`; listed in reverse
        it scores below. `PLAN_REUSE.md`'s three records agree on every corpus
        label, and through this plan's instrument give back `W-d`'s `space` and
        `corpus`, `K-a`'s v1 baselines and each record's
        `proposal_action_accuracy`.
  G-g2  The texts and the prompts are §5's: the digests; the rules rebuilt
        from `HIDDEN_DSL` character for character and parsed back; the prose's
        omissions costing nothing; the catalogue and the prose holding nothing
        they should not; the loop's level-0 prompt v1's to the byte, and every
        other prompt its level-0 prompt plus §5.5's block.
  G-g3  The paths, without spending: a compile answer from parse to score, the
        invalid ones classified, the schedules of §2.5. The requests themselves
        are checked through `tests/doubles.py`'s SDK double in
        `tests/test_manual.py`, which `G-g1`'s suite runs.
  G-g4  The signature (`manual/plan.py`). It does not block a dry run, which
        writes nothing; it blocks every write.

**This module is offline.** It reads `HIDDEN_DSL` to rebuild level 3 and to
build the reference answer, and it sends nothing. The proposer's path imports
none of it by name (§4, rule B).
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import statistics
from dataclasses import dataclass
from typing import Any

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import ACTIONS, ATTRIBUTES, DOMAINS
from harness.dsl import Condition
from reuse.gates import run_suite
from rung2.ceiling_check2_space import measure
from rung2.engine2 import Rule2
from rung2.hidden_priority import build_hidden_engine
from rung2.proposers2 import SYSTEM_PROMPT_V1

from . import compile as C
from . import instrument as I
from . import levels, plan, prompts

TOLERANCE = 2e-6     # the records publish four to six places; 3.10 and 3.12 may differ by one

RULES_HEADER = ("LAS REGLAS DE LA EMPRESA, EN ORDEN\n\n"
                "Se aplica la primera regla de la lista cuyas condiciones casa el ticket.\n\n")

# §5.3: what the prose omits, and the default it merges into H29.
OMITTED = ("H21", "H25", "H27", "H28")


@dataclass
class Checks:
    gg1: dict
    gg2: dict
    gg3: dict
    gg4: dict

    @property
    def blocking_pass(self) -> bool:
        return self.gg1["passes"] and self.gg2["passes"] and self.gg3["passes"]

    def summary(self) -> dict[str, Any]:
        """What a record carries about the checks it was written behind."""
        return {"G-g1": self.gg1, "G-g2": self.gg2, "G-g3": self.gg3, "G-g4": self.gg4}


def close(a: float, b: float) -> bool:
    return abs(a - b) <= TOLERANCE


# ---------------------------------------------------------------------------
# The hidden policy, as an answer and as text
# ---------------------------------------------------------------------------

def hidden_answer(drop: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    """`HIDDEN_DSL` written as a compile answer's list of rules."""
    return [{"conditions": [{"attr": a, "op": o, "value": v} for a, o, v in conds],
             "action": action, "note": rid}
            for rid, conds, action in HIDDEN_DSL if rid not in drop]


def render_rules() -> str:
    """Level 3, rebuilt: §5.4's header and `Rule2.render` of every hidden rule."""
    lines = []
    for rid, conds, action in HIDDEN_DSL:
        rule = Rule2(rule_id=rid, action=action,
                     conditions=[Condition(attr=a, op=o, value=v) for a, o, v in conds])
        lines.append(rule.render())
    return RULES_HEADER + "\n".join(lines) + "\n"


LINE = re.compile(r"^(H\d\d): SI (.+) ENTONCES ([A-Z0-9_]+)$")


def parse_rules(text: str) -> list[tuple[str, list[tuple[str, str, Any]], str]]:
    """Level 3 read back into `HIDDEN_DSL`'s shape. A value is a Python literal
    when it reads as one, and a bare word otherwise, as `Rule2.render` prints
    strings unquoted."""
    out = []
    for line in text.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        conds = []
        for part in m.group(2).split(" AND "):
            attr, op, raw = part.split(" ", 2)
            try:
                value = ast.literal_eval(raw)
            except (ValueError, SyntaxError):
                value = raw
            conds.append((attr, op, value))
        out.append((m.group(1), conds, m.group(3)))
    return out


# ---------------------------------------------------------------------------
# G-g1
# ---------------------------------------------------------------------------

def installer_on_the_policy() -> dict[str, Any]:
    space = I.space()
    hid = C.install(hidden_answer(), space)
    heng, declared, _ = build_hidden_engine(space)
    pos_h = {r.rule_id: i for i, r in enumerate(heng.rules)}
    pos_m = dict(zip((r.rule_id for r in hid.rules), hid.positions))
    mine = {(pos_m[w], pos_m[l]) for w, l, why in hid.engine.edge_log if why == "ok"}
    theirs = {(pos_h[w], pos_h[l]) for w, l in declared}
    refused = [list(e) for e in hid.engine.edge_log if e[2] != "ok"]
    sp, co = I.over_space(hid.engine), I.over_corpus(hid.engine)
    fm = I.first_match_over_space(hid.rules)
    by_case = measure(hid.engine, list(I.corpus()), "corpus", "hybrid")
    rev = C.install(list(reversed(hidden_answer())), space)
    rev_sp, rev_co = I.over_space(rev.engine), I.over_corpus(rev.engine)
    return {
        "edges": len(mine), "same_edges_as_hidden_priority": mine == theirs,
        "refused": refused, "inversions": len(C.inversions(hid)),
        "space": sp["e2e"], "corpus": co["e2e"], "first_match_space": fm["e2e"],
        "measure_corpus": by_case["accuracy_end_to_end"],
        "reversed": {"space": rev_sp["e2e"], "corpus": rev_co["e2e"],
                     "refused": sum(1 for e in rev.engine.edge_log if e[2] != "ok"),
                     "inversions": len(C.inversions(rev))},
        "passes": (mine == theirs and len(mine) == 199 and not refused
                   and not C.inversions(hid) and sp["e2e"] == 1 and co["e2e"] == 1
                   and fm["e2e"] == 1 and by_case["accuracy_end_to_end"] == 1.0
                   and rev_sp["e2e"] < 1 and rev_co["e2e"] < 1),
    }


def reuse_through_the_instrument() -> dict[str, Any]:
    recs = I.reuse_records()
    truths = [tuple(r["truth"] for r in sorted(rec["records"], key=lambda r: r["idx"]))
              for rec in recs]
    edges = json.loads(plan.EDGES_SCORE.read_text())
    blind = json.loads(plan.BLIND_SCORE.read_text())
    k_a_published = blind["baselines"]["baselines"]["v1"]["k_a"]
    runs = []
    for k, rec in enumerate(recs, start=1):
        eng = I.final_engine(rec)
        static = edges["runs"][f"run{k}"]["static"]
        sp, co = I.over_space(eng), I.over_corpus(eng)
        by_case = measure(eng, list(I.corpus()), "corpus", "hybrid")
        k_a = I.partition(rec["rules"])
        prop = I.proposals(rec)
        row = {
            "run": k,
            "space": sp["e2e"], "space_published": static["space"]["with_edges"]["e2e"],
            "corpus": co["e2e"], "corpus_published": static["corpus"]["with_edges"]["e2e"],
            "corpus_by_case": by_case["accuracy_end_to_end"],
            "k_a": k_a, "k_a_published": k_a_published[k - 1],
            "prop": prop["rate"],
            "prop_published": rec["metrics"]["proposal_action_accuracy"],
        }
        row["passes"] = (close(row["space"], row["space_published"])
                         and close(row["corpus"], row["corpus_published"])
                         and co["correct"] == by_case["correct"]
                         and close(k_a, row["k_a_published"])
                         and round(prop["rate"], 4) == row["prop_published"])
        runs.append(row)
    return {"labels_agree": truths[0] == truths[1] == truths[2], "runs": runs,
            "passes": truths[0] == truths[1] == truths[2] and all(r["passes"] for r in runs)}


def gate_gg1(suite: bool = True) -> dict[str, Any]:
    installer = installer_on_the_policy()
    reuse = reuse_through_the_instrument()
    tests = run_suite() if suite else {"ran": False, "passes": None}
    return {"what": "the instrument reproduces the hidden policy and PLAN_REUSE.md's "
                    "records; the suite green",
            "installer": installer, "reuse": reuse, "suite": tests,
            "passes": installer["passes"] and reuse["passes"]
                      and tests["passes"] is not False}


# ---------------------------------------------------------------------------
# G-g2
# ---------------------------------------------------------------------------

def words(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_]+", text))


def catalogue_check(text: str) -> dict[str, Any]:
    lines = [l for l in text.splitlines() if ":" in l]
    heads = [l.split(":", 1)[0] for l in lines]
    w = words(text)
    values = {str(v) for a in ("customer_tier", "product", "channel") for v in DOMAINS[a]}
    leaks = sorted((w & set(ATTRIBUTES)) | (w & values))
    # A digit outside the queue identifiers, which carry their own (T1, T2, T3).
    digits = bool(re.search(r"\d", re.sub(r"\b(" + "|".join(ACTIONS) + r")\b", "", text)))
    return {"queues_in_order": heads == list(ACTIONS), "leaks": leaks, "digits": digits,
            "passes": heads == list(ACTIONS) and not leaks and not digits}


def prose_check(text: str) -> dict[str, Any]:
    w = words(text)
    leaks = sorted((w & set(ACTIONS)) | (w & set(ATTRIBUTES))
                   | (w & {"eq", "neq", "lte", "gte", "in"}))
    ids = sorted(set(re.findall(r"\b[HR]\d{2,4}\b", text)))
    return {"leaks": leaks, "rule_ids": ids, "passes": not leaks and not ids}


def prompts_check() -> dict[str, Any]:
    reuse_prompt = json.loads(plan.REUSE_RUNS[0].read_text())["system_prompt"]
    loop0 = prompts.loop_system_prompt(0)
    out: dict[str, Any] = {
        "loop0_is_v1": loop0 == SYSTEM_PROMPT_V1,
        "loop0_is_plan_reuse_s": loop0 == reuse_prompt,
        "block_only": {},
    }
    for lv in levels.LEVELS[1:]:
        piece = "\n\n" + prompts.block(lv)
        out["block_only"][lv] = {
            "loop": prompts.loop_system_prompt(lv).replace(piece, "", 1) == loop0,
            "compile": (prompts.compile_system_prompt(lv).replace(piece, "", 1)
                        == prompts.compile_system_prompt(0)),
        }
    digests = [d for shape in prompts.prompt_digests().values() for d in shape.values()]
    out["distinct_digests"] = len(set(digests)) == len(digests)
    out["passes"] = (out["loop0_is_v1"] and out["loop0_is_plan_reuse_s"]
                     and all(v["loop"] and v["compile"] for v in out["block_only"].values())
                     and out["distinct_digests"])
    return out


def gate_gg2() -> dict[str, Any]:
    digests = levels.digests()
    rules = levels.part("rules")
    parsed = parse_rules(rules)
    expected = [(rid, [tuple(c) for c in conds], action) for rid, conds, action in HIDDEN_DSL]
    space = I.space()
    merged = C.install(hidden_answer(drop=OMITTED), space)
    omissions = {"dropped": list(OMITTED), "rules_left": len(merged.rules),
                 "space": I.over_space(merged.engine)["e2e"],
                 "corpus": I.over_corpus(merged.engine)["e2e"]}
    flipped = rules.replace("H01", "H00", 1)
    teeth = hashlib.sha256(flipped.encode("ascii")).hexdigest() != plan.DIGESTS["rules"]
    cat, pro = catalogue_check(levels.part("catalogue")), prose_check(levels.part("prose"))
    pr = prompts_check()
    out = {
        "what": "the texts are §5's, and every prompt is its level-0 prompt plus §5.5's block",
        "digests": digests, "digests_are_section_5s": digests == plan.DIGESTS,
        "rules_rebuilt": rules == render_rules(),
        "rules_parse_back": parsed == expected,
        "omissions_cost_nothing": omissions,
        "catalogue": cat, "prose": pro, "prompts": pr, "teeth": teeth,
    }
    out["passes"] = (out["digests_are_section_5s"] and out["rules_rebuilt"]
                     and out["rules_parse_back"]
                     and omissions["space"] == 1 and omissions["corpus"] == 1
                     and cat["passes"] and pro["passes"] and pr["passes"] and teeth)
    return out


# ---------------------------------------------------------------------------
# G-g3
# ---------------------------------------------------------------------------

def compile_path_check() -> dict[str, Any]:
    space = I.space()
    raw, why = C.rules_of({"rules": hidden_answer(), "note": "la politica"})
    inst = C.install(raw, space)
    score = I.over_space(inst.engine)["e2e"]
    bad = hidden_answer()[:3] + [{"conditions": [{"attr": "severity", "op": "gt", "value": 2}],
                                  "action": "T1_GENERAL"}]
    with_bad = C.install(bad, space)
    invalid = {"not_an_object": C.rules_of("texto")[1] is not None,
               "no_list": C.rules_of({"note": "x"})[1] is not None,
               "empty_list": C.rules_of({"rules": []})[1] is not None}
    return {"valid": why is None, "score": score,
            "a_bad_rule_is_rejected_and_counted": (len(with_bad.rules), len(with_bad.rejected)),
            "invalid_asks_are_invalid": invalid,
            "passes": (why is None and score == 1 and len(with_bad.rules) == 3
                       and len(with_bad.rejected) == 1 and all(invalid.values()))}


def schedule_check() -> dict[str, Any]:
    session = plan.compile_schedule("session")
    smoke = plan.compile_schedule("smoke")
    loop = plan.loop_schedule()
    per_pass = {p: [lv for q, lv in session if q == p] for p in range(1, plan.ASKS + 1)}
    per_rep = {r: [lv for q, lv in loop if q == r] for r in range(1, plan.REPS + 1)}
    places = {lv: [per_rep[r].index(lv) for r in per_rep] for lv in plan.LEVELS}
    out = {
        "compile_session": session, "compile_smoke": smoke, "loop": loop,
        "compile_passes_hold_every_level": all(sorted(v) == list(plan.LEVELS)
                                               for v in per_pass.values()),
        "smoke_holds_every_level": sorted(lv for _, lv in smoke) == list(plan.LEVELS),
        "loop_reps_hold_every_level": all(sorted(v) == list(plan.LEVELS)
                                          for v in per_rep.values()),
        "each_level_at_a_different_place_each_rep": all(len(set(v)) == len(v)
                                                        for v in places.values()),
        "rebuilt_from_the_seed": (session == plan.compile_schedule("session")
                                  and loop == plan.loop_schedule()),
    }
    out["passes"] = all(v for k, v in out.items() if isinstance(v, bool))
    return out


def gate_gg3() -> dict[str, Any]:
    cp, sc = compile_path_check(), schedule_check()
    return {"what": "the compile path from parse to score; the invalid asks; the schedules. "
                    "The requests are tests/test_manual.py's, through the SDK double",
            "compile_path": cp, "schedules": sc, "passes": cp["passes"] and sc["passes"]}


# ---------------------------------------------------------------------------
# All four
# ---------------------------------------------------------------------------

def run_checks(suite: bool = True) -> Checks:
    return Checks(gg1=gate_gg1(suite=suite), gg2=gate_gg2(), gg3=gate_gg3(),
                  gg4=plan.gate_signature())


def report(checks: Checks) -> None:
    def mark(g: dict) -> str:
        return "PASS" if g["passes"] else "FAIL"

    g1, g2, g3, g4 = checks.gg1, checks.gg2, checks.gg3, checks.gg4
    ins = g1["installer"]
    print(f"\nG-g1 {mark(g1)}  installer: {ins['edges']} edges, same as hidden_priority "
          f"{ins['same_edges_as_hidden_priority']}, refused {len(ins['refused'])}, "
          f"inversions {ins['inversions']}; space {ins['space']} corpus {ins['corpus']} "
          f"first match {ins['first_match_space']} measure {ins['measure_corpus']}; "
          f"reversed space {ins['reversed']['space']:.4f} corpus {ins['reversed']['corpus']:.4f}")
    for r in g1["reuse"]["runs"]:
        print(f"      PLAN_REUSE run {r['run']}: space {r['space']:.5f} ({r['space_published']}) "
              f"corpus {r['corpus']:.4f} ({r['corpus_published']}) K-a {r['k_a']:.4f} "
              f"({r['k_a_published']}) prop {r['prop']:.4f} ({r['prop_published']}) "
              f"{'ok' if r['passes'] else 'MISMATCH'}")
    s = g1["suite"]
    print(f"      labels agree {g1['reuse']['labels_agree']}; suite "
          f"{'not run' if not s.get('ran') else s.get('result')}")
    print(f"G-g2 {mark(g2)}  digests {g2['digests_are_section_5s']}, rules rebuilt "
          f"{g2['rules_rebuilt']}, parse back {g2['rules_parse_back']}, omissions "
          f"{g2['omissions_cost_nothing']['space']}/{g2['omissions_cost_nothing']['corpus']}, "
          f"catalogue {g2['catalogue']['passes']}, prose {g2['prose']['passes']}, "
          f"prompts {g2['prompts']['passes']}, teeth {g2['teeth']}")
    print(f"G-g3 {mark(g3)}  compile path {g3['compile_path']['passes']}, "
          f"schedules {g3['schedules']['passes']}")
    print(f"G-g4 {'SIGNED' if g4['passes'] else 'UNSIGNED'}  {g4['found']} signature "
          f"line(s), {g4['unsigned']} blank")
    print(f"\nblocking checks: {'PASS' if checks.blocking_pass else 'FAIL'}")
