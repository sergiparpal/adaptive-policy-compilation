"""
STAGE C — the pairwise question, asked where the answer is already known.

--------------------------------------------------------------------------
WHAT IT DOES
--------------------------------------------------------------------------
For each of the 170 labelled pairs of `results2/pair_benchmark.json`, one call:
the witness ticket, exactly two rules that both match it, and the question
*which queue does this ticket go to?*. The correct answer is the winner's
action, known by construction from the hidden policy's layer order.

It tests the change of question where the answer is a lookup. If the model
cannot pick the right queue with the solution key in hand, the format was never
the problem and Stage D is cancelled before a euro reaches the learned base.

--------------------------------------------------------------------------
IT DOES NOT RUN UNTIL P-c IS SIGNED, AND THAT IS A GATE AND NOT A COMMENT
--------------------------------------------------------------------------
`PLAN_PAIRWISE.md` §0: a model may draft a band but may not sign it, and no
stage runs before the rows about its output are signed. §0.1 records what
ignoring that cost — P-a and P-b were spent at zero euros because a free stage
was licensed to run unsigned.

So `gate_signature` reads §0's signature line and refuses to spend if the blanks
are still there. **There is no flag that skips it**: the way past it is to sign
the plan, which is the whole point. Everything the module can do without
spending — building the questions, the leak gates, the position balance — runs
under `--dry-run` regardless, so the instrument can be reviewed before the row
is signed.

--------------------------------------------------------------------------
THREE THINGS THE MODEL MUST NOT SEE, AND THE PLAN NAMES ONLY THE FIRST
--------------------------------------------------------------------------
1. `correct_count`. `Rule2.render()` omits it and
   `tests/test_engine2.py::TestRender` pins that it does. Nothing here changes.

2. **`beats` and `loses_to`.** `render()` appends `[gana a ...]` and
   `[pierde con ...]` whenever those lists are populated — and
   `hidden_priority.build_hidden_engine` populates them with exactly the edges
   this stage is asking the model to reproduce. Rendering the rules off that
   engine would print the answer key inside the question. This module therefore
   builds its own `Rule2` objects from `HIDDEN_DSL`, with both lists empty, and
   never renders one that came out of an engine.

3. **The rule identifiers themselves.** `H01`..`H29` are numbered in layer
   order and the earlier layer is always the winner, so a model that reads
   "lower number means earlier in the manual" scores high without reading a
   single condition. The two rules are therefore shown as **A** and **B**, and
   `gate_no_leak` refuses to spend if any `H`-identifier survives into a
   question. The record maps A and B back.

   The plan does not mention this. It changes what the stage measures — with the
   identifiers left in, a high rate would be evidence about numbering rather
   than about pairwise judgement — and it is recorded here rather than made
   quietly.

**Which of the two is shown first is balanced exactly and at random.** The
benchmark lists the winner first in every pair, so a fixed presentation order
would make "always answer A" a perfect strategy. `winner_positions` deals 85
first and 85 second at seed 17, `gate_position_balance` refuses to spend if that
is not exact, and the record breaks the rate down by position: a gap between the
two IS the position bias, measured rather than assumed away.

--------------------------------------------------------------------------
COUNT CORRECT EDGES. NEVER ACCEPTED EDGES.
--------------------------------------------------------------------------
`PLAN_PAIRWISE.md` §8, and it is the reason the plan exists in this shape. Every
witness is drawn from `ext(A) & ext(B)`, so overlap holds by construction and
`EDGE_DISJOINT` — the verdict that rejected all 14 edges rung 2 ever got —
becomes unreachable. The acceptance rate therefore rises from 0/14 whatever the
model does: it measures the protocol, not the proposer. And `try_edge` cannot
check that the declared winner is the CORRECT one; a false, well-formed edge
enters without resistance.

The verdict histogram is still recorded, because it is free and it is
information about the graph. It lives in its own block, **outside every
denominator**, next to the list of verdicts this protocol makes unreachable and
why. Of the six, only `EDGE_OK` and `EDGE_CYCLE` can ever fire here.

--------------------------------------------------------------------------
TWO DENOMINATORS, AND §0 NAMES THE FIRST
--------------------------------------------------------------------------
An answer is `correct` (the winner's queue), `wrong` (the loser's) or `neither`
(any other queue, off-menu, or unparseable). So there are two rates:

  over_all_pairs        correct / 170          `neither` counts as a failure
  over_two_way_answers  correct / (correct + wrong)

**§0 adjudicates P-c on the first**, amended 2026-08-24 before this stage had
run. The reason is the floor, not a taste for severity: a coin between the two
rules shown ALWAYS commits, so its 0.50 is the same number under either
denominator, and a model answering `neither` has not been beaten by the coin
there — it has declined to play. Scoring on `correct / (correct + wrong)` would
compare it on the subset where it committed against a baseline that commits
everywhere. `FINDINGS3.md` §3 records what unlabelled denominators cost.

Both are written anyway, the second labelled as adjudicating nothing, and the
`neither` tally sits beside them: failing by declining to answer and failing by
answering wrongly are different findings.

Two floors are carried for the reading: **0.3877**, `proposal_action_accuracy`
from `results/llm_run.json`, the same operation under the old framing and too
lenient because that task was an 8-way choice; and **0.50**, a coin between the
two rules shown, which is the real bar.

--------------------------------------------------------------------------
THE PROMPT IS IN SPANISH, DELIBERATELY
--------------------------------------------------------------------------
Model, temperature, `response_format` and `max_retries` are rung 2's so that the
comparison against 0.3877 holds. The prompt is necessarily new — it asks a
different question — but translating it would add a second variable to a
comparison the plan wants held fixed. The module's own prose and output are in
English; the text that reaches the model is not.

--------------------------------------------------------------------------
WHAT IT DOES NOT DO
--------------------------------------------------------------------------
It never imports the oracle: the key is a lookup into the benchmark record,
which carries it openly. It does not touch `proposers2.py` — the client here is
a thin one of its own, reusing only `parse_payload`. It does not launch Stage D
under any outcome; §9's kill switch is reported and acted on by a person.
`--learned` is Stage D and exits saying so.

Usage:
    python3 -m rung2.pair_judgement --hidden --dry-run     # free, spends nothing
    python3 -m rung2.pair_judgement --hidden --limit 10    # the smoke path
    python3 -m rung2.pair_judgement --hidden               # 170 calls, cents
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL
from harness.domain import ACTIONS, Case
from harness.dsl import Condition
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from .engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK,
                      EDGE_SELF, EDGE_UNKNOWN, PriorityEngine, Rule2, Space)
from .proposers2 import ProposalError, parse_payload

REPO = Path(__file__).resolve().parent.parent
PLAN = REPO / "PLAN_PAIRWISE.md"
BENCH = Path("results2/pair_benchmark.json")
OUT = Path("results2")
RECORD = "pair_judgement_hidden.json"
RECORD_SMOKE = "pair_judgement_hidden_smoke.json"

MODEL = "deepseek/deepseek-v4-flash"
TEMPERATURE = 0
MAX_RETRIES = 2
MAX_TOKENS = 400
POSITION_SEED = 17

N_DECLARED = 199
N_CLEAN = 170

SHOWN_AS = ("A", "B")
RULE_ID = re.compile(r"\bH\d{2}\b")

FLOOR_OLD_FRAMING = 0.3877      # results/llm_run.json :: metrics
FLOOR_COIN = 0.50               # a coin between the two rules shown


# ---------------------------------------------------------------------------
# The prompt. Spanish on purpose: see the module header.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""Eres el arbitro de un sistema de triaje de tickets.

Dos reglas del manual casan ESTE ticket y lo mandan a colas DISTINTAS. Ninguna
de las dos esta contenida en la otra, asi que la estructura no decide: hace
falta un criterio.

Tu unica tarea es decir a que cola va este ticket.

NO escribas reglas nuevas. NO propongas cambios en el manual. NO expliques como
deberia arbitrar el motor. Solo la cola.

Las colas posibles son:

{chr(10).join("  " + a for a in ACTIONS)}

Responde UNICAMENTE con un objeto JSON, sin texto alrededor:

  {{"action": "<COLA>", "why": "<una frase, como maximo 30 palabras>"}}

`action` tiene que ser exactamente una de las colas de la lista.
"""

RETRY_MSG = ("Tu respuesta anterior no era JSON valido. Responde UNICAMENTE "
             "con el objeto JSON, sin texto alrededor.")


def question(case: Case, first: Rule2, second: Rule2) -> str:
    """
    The user message. It receives ONLY what the model may see: the ticket and
    two rules already relabelled A and B.

    The key never enters this function by any route — it takes no winner, no
    action and no benchmark row — which is what makes the leak gates below a
    check on the data rather than on the wording.
    """
    return (
        "LAS DOS REGLAS QUE CASAN EL TICKET:\n"
        f"  {first.render()}\n"
        f"  {second.render()}\n\n"
        "TICKET:\n"
        + json.dumps(case.as_dict(), indent=2, default=str)
    )


# ---------------------------------------------------------------------------
# The rules, built clean
# ---------------------------------------------------------------------------

def hidden_rules() -> dict[str, Rule2]:
    """
    The 29 rules as `Rule2`, straight from `HIDDEN_DSL`, with `beats` and
    `loses_to` EMPTY.

    Deliberately not `hidden_priority.build_hidden_engine`, whose rules carry
    the declared edges — `render()` would print them and the question would
    contain its own answer. This is leak 2 of the module header.
    """
    return {
        rid: Rule2(rule_id=rid,
                   conditions=[Condition(attr=a, op=o, value=v)
                               for a, o, v in conds],
                   action=action, born_at=i)
        for i, (rid, conds, action) in enumerate(HIDDEN_DSL)
    }


def shown_rule(rule: Rule2, label: str) -> Rule2:
    """The same rule under a neutral identifier. Leak 3: `H01`..`H29` are
    numbered in layer order and the earlier layer always wins."""
    return Rule2(rule_id=label, conditions=list(rule.conditions),
                 action=rule.action)


def fresh_engine(rules: dict[str, Rule2]) -> PriorityEngine:
    """The 29 rules with subsumption and NO declared edge. What the model's
    answers are fed into, so the verdict histogram is about them."""
    engine = PriorityEngine(space=Space())
    for rid, rule in rules.items():
        engine.add(Rule2(rule_id=rid, conditions=list(rule.conditions),
                         action=rule.action), born_at=rule.born_at,
                   keep_id=True)
    return engine


# ---------------------------------------------------------------------------
# Which of the two goes first
# ---------------------------------------------------------------------------

def winner_positions(n: int, seed: int = POSITION_SEED) -> list[int]:
    """
    Exactly balanced: the winner is shown first in half the pairs and second in
    the other half, dealt at seed 17.

    Balanced rather than merely random, because with 170 draws a fair coin
    lands 85/85 about 6% of the time and any other split leaves the two
    per-position rates measured on different sample sizes for no reason. An odd
    `n` gets the extra pair in position 0.
    """
    pos = [0] * ((n + 1) // 2) + [1] * (n // 2)
    random.Random(seed).shuffle(pos)
    return pos


# ---------------------------------------------------------------------------
# Reading the benchmark
# ---------------------------------------------------------------------------

def load_benchmark(path: Path = BENCH):
    """The clean-witness pairs, and the counts that say it is the right file."""
    if not path.exists():
        raise SystemExit(
            f"\nABORTED: {path} is not there.\n\n"
            "  Stage C runs on the population stage B builds. Run:\n"
            "    PYTHONHASHSEED=0 python3 -m rung2.pair_benchmark\n")
    rec = json.loads(path.read_text())
    pairs = rec["pairs"]
    clean = [p for p in pairs if p["clean"]]
    gate = {
        "what": "the benchmark this stage reads is the one stage B gated: 199 "
                "declared pairs, 170 with a clean witness.",
        "source": str(path),
        "n_declared": len(pairs), "n_clean": len(clean),
        "expected_declared": N_DECLARED, "expected_clean": N_CLEAN,
        "passes": len(pairs) == N_DECLARED and len(clean) == N_CLEAN,
    }
    return clean, [p for p in pairs if not p["clean"]], gate, rec


# ---------------------------------------------------------------------------
# The gates that run before a single call
# ---------------------------------------------------------------------------

def gate_signature(path: Path = PLAN):
    """
    §0 of `PLAN_PAIRWISE.md` must carry a signature. Blanks mean unsigned.

    No flag skips this. The way past it is to sign the plan — and the signature
    commit travels alone, staged by name (hard rule 2 of `CLAUDE.md`).
    """
    line = None
    if path.exists():
        for raw in path.read_text().splitlines():
            if raw.startswith("**Signed by Sergi:"):
                line = raw.strip()
                break
    signed = bool(line) and not re.search(r"_{3,}", line)
    return {
        "what": "the signature line of §0 of PLAN_PAIRWISE.md. P-c governs this "
                "stage's output and a model may not sign it (hard rule 2).",
        "source": str(path),
        "line_found": line is not None,
        "line": line,
        "passes": signed,
    }


def gate_no_leak(questions):
    """
    No rule identifier survives into a question, and no question carries a
    declared-edge annotation.

    Both are leaks that would let a high rate mean something other than
    pairwise judgement, and both are properties of the emitted text, so they are
    checked on the text rather than argued from the construction.
    """
    with_ids = [k for k, q in enumerate(questions) if RULE_ID.search(q)]
    with_edges = [k for k, q in enumerate(questions)
                  if "[gana a" in q or "[pierde con" in q]
    return {
        "what": "every question, checked as text: no H-identifier (they are "
                "numbered in layer order and the earlier layer always wins) and "
                "no `[gana a ...]` / `[pierde con ...]` annotation (Rule2.render "
                "prints them whenever beats/loses_to is populated, and those are "
                "the very edges this stage asks the model to reproduce).",
        "n_questions": len(questions),
        "questions_naming_a_rule_id": with_ids[:10],
        "questions_carrying_a_declared_edge": with_edges[:10],
        "passes": not with_ids and not with_edges,
    }


def gate_position_balance(positions):
    counts = Counter(positions)
    n = len(positions)
    return {
        "what": "the winner is shown first in half the pairs and second in the "
                "other half. The benchmark lists the winner first in every row, "
                "so an unbalanced presentation would make 'always answer the "
                "first' a strategy.",
        "seed": POSITION_SEED,
        "shown_first": counts[0], "shown_second": counts[1],
        "passes": abs(counts[0] - counts[1]) <= (n % 2),
    }


def gate_api_key():
    """Length only. The value is never printed (hard rule 7)."""
    n = len(os.environ.get("OPENROUTER_API_KEY", ""))
    return {
        "what": "OPENROUTER_API_KEY reaches the process environment. Its value "
                "is never read aloud, stored or written; only its length.",
        "length": n,
        "passes": n > 0,
        "how": 'eval "$(grep -m1 \'^export OPENROUTER_API_KEY=\' ~/.bashrc)"',
    }


# ---------------------------------------------------------------------------
# Building the questions
# ---------------------------------------------------------------------------

def build_questions(clean, rules, positions):
    """One row per pair, carrying the question and the key SEPARATELY.

    The question is built by `question()`, which cannot see the key. The key
    travels in the same row because scoring needs it, and never in the same
    function.
    """
    rows = []
    for k, (pair, pos) in enumerate(zip(clean, positions)):
        w, lo = pair["winner"], pair["loser"]
        ids = (w, lo) if pos == 0 else (lo, w)
        first, second = (shown_rule(rules[ids[0]], SHOWN_AS[0]),
                         shown_rule(rules[ids[1]], SHOWN_AS[1]))
        case = Case(**pair["witness"])
        rows.append({
            "index": k,
            "winner": w, "loser": lo,
            "winner_action": pair["winner_action"],
            "loser_action": pair["loser_action"],
            "witness_index": pair["witness_index"],
            "witness": pair["witness"],
            "overlap_cases": pair["overlap_cases"],
            "shown_as": {SHOWN_AS[0]: ids[0], SHOWN_AS[1]: ids[1]},
            "winner_shown_as": SHOWN_AS[pos],
            "question": question(case, first, second),
        })
    return rows


def add_breadth(rows, engine):
    """Whether the winner is the broader or the narrower rule of the pair.

    The two are subsumption-incomparable by construction, so neither contains
    the other and 'broader' is only about size. It is the split that tests the
    `narrow != correct` mechanism directly, and it costs two popcounts.
    """
    for r in rows:
        ew = engine.ext[r["winner"]].bit_count()
        el = engine.ext[r["loser"]].bit_count()
        r["winner_extension"] = ew
        r["loser_extension"] = el
        r["winner_is_broader"] = ew > el


# ---------------------------------------------------------------------------
# The client
# ---------------------------------------------------------------------------

class Judge:
    """Thin client, rung 2's settings. `proposers2.py` is not touched."""

    def __init__(self, model: str = MODEL, max_retries: int = MAX_RETRIES):
        from openai import OpenAI

        self.name = f"openrouter-judge({model})"
        self.model = model
        self.max_retries = max_retries
        self.system_prompt = SYSTEM_PROMPT
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def ask(self, text: str):
        """Returns (payload, attempts). Raises ProposalError if nothing parses."""
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}]
        last: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                kwargs = {"model": self.model, "messages": messages,
                          "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE}
                if attempt == 0:
                    kwargs["response_format"] = {"type": "json_object"}
                resp = self._client.chat.completions.create(**kwargs)
                return parse_payload(resp.choices[0].message.content or ""), attempt + 1
            except Exception as exc:  # noqa: BLE001
                last = exc
                if attempt == 0 and len(messages) == 2:
                    messages = messages + [
                        {"role": "assistant", "content": "..."},
                        {"role": "user", "content": RETRY_MSG}]
        raise ProposalError(str(last))


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def classify(answer, winner_action, loser_action) -> str:
    """Three outcomes, and `neither` is one of them rather than a discard."""
    if answer == winner_action:
        return "correct"
    if answer == loser_action:
        return "wrong"
    return "neither"


def rates(rows):
    """
    Both denominators, both labelled, and §0's choice marked on the row rather
    than left to the reader.

    The adjudicating one is `over_all_pairs`. The other is computed and
    published because the gap between them is information — a run that fails by
    declining to answer is not the run that fails by answering wrongly — and it
    decides nothing.
    """
    c = Counter(r["outcome"] for r in rows)
    two_way = c["correct"] + c["wrong"]
    return {
        "counts": {k: c[k] for k in ("correct", "wrong", "neither")},
        "over_all_pairs": {
            "value": round(c["correct"] / len(rows), 4) if rows else None,
            "denominator": len(rows),
            "adjudicates_P_c": True,
            "what": "`neither` counts as a failure. The rate P-c is adjudicated "
                    "on (§0 of PLAN_PAIRWISE.md, amended 2026-08-24 before this "
                    "stage ran): a coin between the two rules always commits, so "
                    "its 0.50 is the same number under either denominator, and a "
                    "model that answers `neither` has declined to play rather "
                    "than been beaten there.",
        },
        "over_two_way_answers": {
            "value": round(c["correct"] / two_way, 4) if two_way else None,
            "denominator": two_way,
            "adjudicates_P_c": False,
            "what": "only the pairs where the model named one of the two rules' "
                    "queues. The more flattering of the two, and it adjudicates "
                    "nothing: it would compare the model on the subset where it "
                    "committed against a baseline that commits everywhere. "
                    "Published because the gap between the two IS information "
                    "about how the failures fall.",
        },
        "which_adjudicates_P_c": "over_all_pairs. §0 of PLAN_PAIRWISE.md names "
                                 "it, amended 2026-08-24 before this stage had "
                                 "run and before any figure of it existed.",
        "floors": {
            "old_framing_proposal_action_accuracy": FLOOR_OLD_FRAMING,
            "coin_between_the_two_rules_shown": FLOOR_COIN,
        },
    }


def breakdowns(rows):
    def rate(sub):
        c = Counter(r["outcome"] for r in sub)
        tw = c["correct"] + c["wrong"]
        return {"n": len(sub), "correct": c["correct"], "wrong": c["wrong"],
                "neither": c["neither"],
                "correct_over_all": round(c["correct"] / len(sub), 4) if sub else None,
                "wrong_over_two_way": round(c["wrong"] / tw, 4) if tw else None}
    return {
        "by_position_of_the_winner": {
            "what": "a gap between the two IS the position bias, and it is the "
                    "reason the presentation order is balanced at all.",
            "shown_first": rate([r for r in rows if r["winner_shown_as"] == "A"]),
            "shown_second": rate([r for r in rows if r["winner_shown_as"] == "B"]),
        },
        "by_breadth_of_the_winner": {
            "what": "the wrong-edge rate split by whether the CORRECT winner is "
                    "the broader or the narrower rule of the pair. It tests the "
                    "`narrow != correct` mechanism directly: a model crowning "
                    "the narrower rule scores badly exactly where the winner is "
                    "the broader one.",
            "winner_is_broader": rate([r for r in rows if r["winner_is_broader"]]),
            "winner_is_narrower": rate([r for r in rows if not r["winner_is_broader"]]),
        },
        "by_winner_action": {
            a: rate([r for r in rows if r["winner_action"] == a])
            for a in sorted({r["winner_action"] for r in rows})
        },
    }


# ---------------------------------------------------------------------------
# The verdict histogram, outside every denominator
# ---------------------------------------------------------------------------

UNREACHABLE = {
    EDGE_DISJOINT: "every witness comes from ext(A) & ext(B), so the two "
                   "extensions overlap by construction. This is the verdict "
                   "that rejected all 14 edges rung 2 ever got, and this "
                   "protocol makes it impossible.",
    EDGE_CONTRADICTS: "hidden_priority filtered subsumption-comparable pairs "
                      "out upstream, so ext(loser) is never strictly inside "
                      "ext(winner).",
    EDGE_SELF: "the two rules of a pair are always distinct.",
    EDGE_UNKNOWN: "both rules are in the engine before any edge is offered.",
}


def verdict_histogram(rows, engine):
    """
    What `try_edge` says about the edges the answers imply. **Information about
    the graph, never a denominator** (`PLAN_PAIRWISE.md` §8): a witness
    guarantees overlap, so acceptance rises from 0/14 whatever the model does,
    and `try_edge` cannot check that the declared winner is the correct one.

    Fed sequentially into a fresh engine, because whether an edge closes a cycle
    depends on the ones already in.
    """
    hist = Counter()
    for r in rows:
        if r["outcome"] == "neither":
            continue
        named = (r["winner"] if r["outcome"] == "correct" else r["loser"])
        other = (r["loser"] if r["outcome"] == "correct" else r["winner"])
        v = engine.try_edge(named, other)
        r["try_edge_verdict"] = v
        hist[v] += 1
    return {
        "what": "what try_edge returns for the edge each answer implies, fed "
                "sequentially into an engine that starts with subsumption and "
                "no declared edge.",
        "outside_every_denominator": "yes, and deliberately. A witness "
                                     "guarantees overlap, so the acceptance "
                                     "rate measures the protocol and not the "
                                     "proposer; and the validator cannot check "
                                     "that the declared winner is the correct "
                                     "one, so an accepted edge may be false.",
        "counts": dict(sorted(hist.items())),
        "unreachable_here": UNREACHABLE,
        "also_unreachable": {
            "redundant " + EDGE_OK: "engine2.py:302-306 returns EDGE_OK without "
                                    "touching decl_below/decl_above when "
                                    "ext(winner) is strictly inside ext(loser). "
                                    "Filtered upstream like EDGE_CONTRADICTS.",
        },
        "reachable_here": [EDGE_OK, EDGE_CYCLE],
    }


# ---------------------------------------------------------------------------
# The kill switch, reported and never acted on
# ---------------------------------------------------------------------------

def kill_switch(rate):
    """§9 of `PLAN_PAIRWISE.md`, read out. Nothing here launches anything."""
    if rate is None:
        band = "no rate"
    elif rate <= FLOOR_COIN:
        band = ("STOP. The protocol has not beaten a two-way guess. Write it up "
                "as a negative result and go no further; that is a result "
                "(hard rule 6).")
    elif rate <= 0.60:
        band = ("P-c is REFUTED, and Stage D is a decision for Sergi and not "
                "for the agent. The claim failed; whether the residue is worth "
                "300-500 calls is a judgement about money. Report and wait.")
    else:
        band = ("P-c HOLDS and Stage D may run, subject to its own signed rows "
                "P-d and P-e.")
    return {"rate_read": rate, "band": band,
            "note": "reported only. This script launches nothing under any "
                    "outcome, and the denominator this was read on is named "
                    "beside it."}


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--learned" in argv:
        print("--learned is STAGE D of PLAN_PAIRWISE.md: 300-500 calls over the "
              "learned base.\nIt is gated twice — on this stage clearing its "
              "kill switch, and on P-d and P-e\nbeing signed. Not implemented "
              "here.")
        return 2
    if "--hidden" not in argv:
        print(__doc__.strip().split("Usage:")[-1])
        return 2

    dry_run = "--dry-run" in argv
    overwrite = FLAG in argv
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    out = OUT / (RECORD_SMOKE if limit else RECORD)
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])

    t_start = time.time()
    print("=" * 78)
    print("STAGE C — the pairwise question, where the answer is already known")
    print("=" * 78)
    print(f"  model {MODEL} · temperature {TEMPERATURE} · "
          f"max_retries {MAX_RETRIES} · sequential")
    print(f"  {describe()}")

    clean, unclean, g_bench, _rec = load_benchmark()
    rules = hidden_rules()
    engine = fresh_engine(rules)
    positions = winner_positions(len(clean))
    rows = build_questions(clean, rules, positions)
    add_breadth(rows, engine)
    if limit:
        rows = rows[:limit]

    g_leak = gate_no_leak([r["question"] for r in rows])
    g_pos = gate_position_balance([SHOWN_AS.index(r["winner_shown_as"])
                                   for r in rows])
    g_sig = gate_signature()

    print()
    print("GATES — every one of them runs before a single call")
    for name, g in (("benchmark", g_bench), ("no leak", g_leak),
                    ("position balance", g_pos), ("P-c signed", g_sig)):
        print(f"  {name:<20}{'ok' if g['passes'] else 'NO'}")
    if not g_bench["passes"]:
        print(f"\n  STOP: {BENCH} is not the population stage B gated "
              f"({g_bench['n_declared']} declared, {g_bench['n_clean']} clean).")
        return 1
    if not g_leak["passes"]:
        print("\n  STOP: a question carries the answer. See the module header, "
              "leaks 2 and 3.")
        return 1
    if not g_pos["passes"]:
        print(f"\n  STOP: the presentation order is not balanced "
              f"({g_pos['shown_first']} / {g_pos['shown_second']}).")
        return 1

    if dry_run:
        print()
        print("=" * 78)
        print("DRY RUN — nothing is called and nothing is written")
        print("=" * 78)
        print(f"  {len(rows)} questions built · {len(unclean)} pairs without a "
              f"clean witness, outside the denominator")
        print(f"  winner shown first in {g_pos['shown_first']}, second in "
              f"{g_pos['shown_second']}")
        print(f"  P-c signed: {g_sig['passes']}  ({g_sig['line']})")
        print()
        print("  SYSTEM PROMPT")
        for line in SYSTEM_PROMPT.strip().splitlines():
            print(f"    {line}")
        print()
        print(f"  ONE QUESTION (pair {rows[0]['winner']} > {rows[0]['loser']}, "
              f"winner shown as {rows[0]['winner_shown_as']})")
        for line in rows[0]["question"].splitlines():
            print(f"    {line}")
        print(f"\n  cost if run: {len(rows)} calls. Nothing spent here.")
        return 0

    if not g_sig["passes"]:
        print()
        print("  STOP: §0 of PLAN_PAIRWISE.md is unsigned, and P-c governs this")
        print("  stage's output. A model may draft a band and may not sign it")
        print("  (hard rule 2). No flag skips this gate; the way past it is the")
        print("  signature, in its own commit, staged by name.")
        print(f"    line: {g_sig['line']}")
        return 1

    g_key = gate_api_key()
    if not g_key["passes"]:
        print("\n  STOP: OPENROUTER_API_KEY does not reach this process.")
        print(f"    {g_key['how']}")
        return 1
    or_exit(refuse_overwrite, out, overwrite=overwrite,
            exits=("--out OTHER.json      write somewhere else",
                   f"{FLAG}   replace it on purpose"))

    judge = Judge()
    print()
    print(f"  {len(rows)} calls, one per pair, sequential")
    failures = 0
    for k, r in enumerate(rows):
        try:
            payload, attempts = judge.ask(r["question"])
            answer = payload.get("action")
            r["answer"] = answer if answer in ACTIONS else None
            r["off_menu"] = answer is not None and answer not in ACTIONS
            r["raw_answer"] = answer
            r["why"] = str(payload.get("why", ""))[:280]
            r["attempts"] = attempts
            r["parse_failed"] = False
        except ProposalError as exc:
            failures += 1
            r.update({"answer": None, "off_menu": False, "raw_answer": None,
                      "why": "", "attempts": MAX_RETRIES + 1,
                      "parse_failed": True, "error": str(exc)[:200]})
        r["outcome"] = classify(r["answer"], r["winner_action"],
                                r["loser_action"])
        if (k + 1) % 20 == 0 or k + 1 == len(rows):
            print(f"    {k + 1}/{len(rows)}")

    hist = verdict_histogram(rows, engine)
    rate_block = rates(rows)
    payload = {
        "_env": environment(model=MODEL, temperature=TEMPERATURE,
                            max_retries=MAX_RETRIES,
                            position_seed=POSITION_SEED),
        "what":
            "stage C of PLAN_PAIRWISE.md: the pairwise question asked of the "
            "hidden policy's labelled pairs, where the correct winner is known "
            "by construction. One call per pair, sequential.",
        "stage": "C", "population": "hidden policy, clean-witness pairs",
        "partial_run": bool(limit),
        "n_asked": len(rows),
        "n_clean_available": len(clean),
        "n_without_clean_witness": len(unclean),
        "denominator_note":
            "the pairs with no clean witness are outside every denominator, and "
            "they are the pairs where the layer order is invisible on the "
            "surface of the two rules shown. The pairs asked about are "
            "therefore the easier half by construction, and every rate below is "
            "an UPPER estimate of what the proposer would do on all 199 "
            "(results2/FINDINGS2.md, the labelled pair benchmark).",
        "what_the_model_was_not_shown":
            "correct_count (Rule2.render omits it); beats and loses_to (the "
            "rules are built from HIDDEN_DSL with both empty, never off an "
            "engine that carries the declared edges); and the H-identifiers, "
            "which are numbered in layer order — the two rules are shown as A "
            "and B, and gate_no_leak checks the emitted text rather than the "
            "construction.",
        "system_prompt": SYSTEM_PROMPT,
        "prompt_language":
            "Spanish, deliberately. Model, temperature, response_format and "
            "max_retries are rung 2's so the comparison against 0.3877 holds; "
            "translating the prompt would add a second variable to it.",
        "gates": {"benchmark": g_bench, "no_leak": g_leak,
                  "position_balance": g_pos, "signature": g_sig,
                  "api_key": {k: v for k, v in g_key.items() if k != "length"}},
        "rates": rate_block,
        "breakdowns": breakdowns(rows),
        "parse_failures": failures,
        "off_menu_answers": sum(1 for r in rows if r["off_menu"]),
        "try_edge_verdicts": hist,
        "kill_switch": kill_switch(rate_block["over_all_pairs"]["value"]),
        "kill_switch_on_the_non_adjudicating_rate": kill_switch(
            rate_block["over_two_way_answers"]["value"]),
        "pairs_without_a_clean_witness": [
            {"winner": p["winner"], "loser": p["loser"],
             "overlap_cases": p["overlap_cases"]} for p in unclean],
        "answers": rows,
        "seconds": round(time.time() - t_start, 1),
    }
    OUT.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))

    c = rate_block["counts"]
    print()
    print("=" * 78)
    print("OUTCOMES — correct edges, never accepted edges")
    print("=" * 78)
    print(f"  correct {c['correct']}   wrong {c['wrong']}   "
          f"neither {c['neither']}   (parse failures {failures})")
    for key in ("over_all_pairs", "over_two_way_answers"):
        b = rate_block[key]
        mark = "  <- adjudicates P-c" if b["adjudicates_P_c"] else ""
        print(f"  {key:<24}{b['value']}   n={b['denominator']}{mark}")
    print(f"  {payload['kill_switch']['band']}")
    print(f"\n-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
