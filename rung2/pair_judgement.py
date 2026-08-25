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

    # Stage B of PLAN_PROPOSER_1600.md. `--sample` names the population Stage A
    # built and gated; `--reuse` or `--reask-all` is §2's choice and has no
    # default; the signature gate reads THAT plan's §0 and not the closed
    # thread's. All of it is refused while §0 is unsigned, and --dry-run builds
    # every question and spends nothing.
    python3 -m rung2.pair_judgement --learned --budget 1600 \
        --sample results2/pair_sample_1600.json --reuse --dry-run
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from harness.ceiling_check import HIDDEN_DSL, all_cases
from harness.domain import ACTIONS, Case
from harness.dsl import Condition
from harness.provenance import describe, environment
from harness.record_guard import FLAG, or_exit, refuse_overwrite

from .engine2 import (EDGE_CONTRADICTS, EDGE_CYCLE, EDGE_DISJOINT, EDGE_OK,
                      EDGE_SELF, EDGE_UNKNOWN, PriorityEngine, Rule2, Space,
                      strictly_below)
# The bit convention has ONE home and this is not it. `pair_benchmark` owns
# `lowest_case_index` and its MSB-first reasoning; importing it keeps a single
# source for the rule that decides which case a witness is. The import brings no
# oracle name into this module — `tests/test_oracle_separation.py` walks the AST
# of this file and would say so — and `engine2.py`, also on the online-loop list,
# already reaches into `harness.ceiling_check` the same way.
from .pair_benchmark import lowest_case_index
from .proposers2 import ProposalError, parse_payload

REPO = Path(__file__).resolve().parent.parent
PLAN = REPO / "PLAN_PAIRWISE.md"
# The pairwise thread closed on 2026-08-24 with §0 of PLAN_PAIRWISE.md SIGNED.
# That signature must not carry a second, larger run: PLAN_PROPOSER_1600.md asks
# a different question at a different budget, its rows are its own, and the
# --sample path below gates on ITS §0 and never on the closed thread's.
PLAN_1600 = REPO / "PLAN_PROPOSER_1600.md"
BENCH = Path("results2/pair_benchmark.json")
OUT = Path("results2")
RECORD = "pair_judgement_hidden.json"
RECORD_SMOKE = "pair_judgement_hidden_smoke.json"
RECORD_LEARNED = "pair_judgement_learned.json"
RECORD_LEARNED_SMOKE = "pair_judgement_learned_smoke.json"
RECORD_1600 = "pair_judgement_1600.json"
RECORD_1600_SMOKE = "pair_judgement_1600_smoke.json"

LEARNED = Path("results/llm_run.json")
# The population of stage D, measured 2026-08-24 and again by this module every
# time it runs: pairs of the 577 learned rules whose extensions OVERLAP, that are
# subsumption-INCOMPARABLE, and whose actions DIFFER — the same three conditions
# hidden_priority.py applies. 31,850 of the 166,176 pairs, 19.2%. A constant
# fraction of the quadratic, not a lower order.
GATE_POPULATION = 31850
N_LEARNED_RULES = 577
DEFAULT_BUDGET = 400
SAMPLE_SEED = 17

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
# The learned base — stage D's population
# ---------------------------------------------------------------------------

def learned_rules(path: Path = LEARNED):
    """
    The 577 rules of rung 1 as `Rule2`, read-only and built clean.

    The record carries no `beats` or `loses_to` — rung 1 had no declared
    priority — so there is nothing to strip here, unlike the hidden engine. They
    are still built rather than borrowed, so that no engine's state can reach a
    rendered rule by accident.
    """
    d = json.loads(path.read_text())
    out = {}
    for r in d["rules"]:
        out[r["rule_id"]] = Rule2(
            rule_id=r["rule_id"],
            conditions=[Condition(c["attr"], c["op"], c["value"])
                        for c in r["conditions"]],
            action=r["action"], born_at=r["born_at"])
    return out


def learned_population(rules, space):
    """
    Every pair that could take a declared edge, in a deterministic order.

    The three conditions are `hidden_priority.py`'s, applied to the learned base:
    the extensions overlap (they can compete), subsumption leaves them
    incomparable (nothing else resolves it), and the actions differ (otherwise it
    does not matter who wins).

    **The subsumption filter is not optional.** `PLAN_PAIRWISE.md` §10 records
    what dropping it costs: on a subsumption-comparable pair no declared edge can
    enter the graph whichever way the model answers — `try_edge` returns
    `EDGE_CONTRADICTS` for the broader rule and a redundant `EDGE_OK` that
    mutates nothing for the narrower — so about one call in ten would be spent on
    an answer that is inert by construction, and one of those wasted calls would
    score as an acceptance.
    """
    ids = sorted(rules)
    ext = {rid: space.extension(rules[rid].conditions) for rid in ids}
    pairs = []
    # All four boxes exist even when empty. A Counter drops the zeros, and a
    # record that omits a box reads as though the condition was never applied —
    # and `gate_population` would raise instead of reporting the miss.
    stats = Counter({"disjoint": 0, "subsumption_comparable": 0,
                     "same_action": 0})
    for i, a in enumerate(ids):
        ea = ext[a]
        for b in ids[i + 1:]:
            eb = ext[b]
            if ea & eb == 0:
                stats["disjoint"] += 1
                continue
            if strictly_below(ea, eb) or strictly_below(eb, ea):
                stats["subsumption_comparable"] += 1
                continue
            if rules[a].action == rules[b].action:
                stats["same_action"] += 1
                continue
            pairs.append((a, b))
    stats["population"] = len(pairs)
    return pairs, ext, dict(stats)


def sample_population(pairs, budget, seed=SAMPLE_SEED):
    """A deterministic sample at seed 17, kept in the population's own order so
    the record reads the same way whatever the budget."""
    if budget >= len(pairs):
        return list(pairs)
    picked = set(random.Random(seed).sample(range(len(pairs)), budget))
    return [p for k, p in enumerate(pairs) if k in picked]


def load_sample(path: Path):
    """
    The pairs Stage A of `PLAN_PROPOSER_1600.md` built, **identity only**.

    Its record carries two blocks and this reads one of them. `pairs` is which
    two rules and where they came from; `oracle` is which of the two gets more of
    the shared region right, and this module — on the online-loop list of
    `tests/test_oracle_separation.py` — never reads it. The projection to tuples
    happens here, at the boundary, so nothing downstream can reach a field this
    function did not hand over.
    """
    if not path.exists():
        raise SystemExit(
            f"\nABORTED: {path} is not there.\n\n"
            "  The 1,600-pair population is built by Stage A. Run:\n"
            "    PYTHONHASHSEED=0 python3 -m rung2.pair_sample_1600\n")
    rec = json.loads(path.read_text())
    return [(r["rule_a"], r["rule_b"]) for r in rec["pairs"]], rec


def gate_sample_record(rec, path, budget):
    """
    The sample handed in is Stage A's, it passed its own gates, and it is the
    size the budget claims.

    Every one of these is a way to spend 1,200 calls on the wrong population, and
    the last one is the quiet one: `--budget 1600` with a 400-pair file asks 400
    questions and writes a record that says 1,600.
    """
    gates = rec.get("gates") or {}
    failed = sorted(k for k, g in gates.items() if not g.get("passes"))
    n = len(rec.get("pairs") or [])
    return {
        "what": "the file --sample names is Stage A's record, every gate in it "
                "passed, and it holds exactly the budget's worth of pairs.",
        "source": str(path),
        "plan_named_by_the_record": rec.get("plan"),
        "expected_plan": PLAN_1600.name,
        "n_pairs": n, "expected": budget,
        "gates_that_failed": failed,
        "passes": (rec.get("plan") == PLAN_1600.name and not failed
                   and n == budget and bool(gates)),
    }


def gate_population(stats, n_rules):
    total = n_rules * (n_rules - 1) // 2
    got = (stats["disjoint"] + stats["subsumption_comparable"]
           + stats["same_action"] + stats["population"])
    return {
        "what": "the three conditions of hidden_priority.py applied to the 577 "
                "learned rules. The population is what PLAN_PAIRWISE.md §10 "
                "measured on 2026-08-24 and budgeted stage D on.",
        "boxes": stats, "n_pairs": total, "boxes_total": got,
        "expected_population": GATE_POPULATION,
        "fraction": round(stats["population"] / total, 4),
        "passes": (got == total and stats["population"] == GATE_POPULATION
                   and n_rules == N_LEARNED_RULES),
    }


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

def gate_signature(path: Path = PLAN, rows: str = "P-c"):
    """
    §0 of the plan that governs this run must carry a signature. Blanks mean
    unsigned.

    No flag skips this. The way past it is to sign the plan — and the signature
    commit travels alone, staged by name (hard rule 2 of `CLAUDE.md`).

    **The plan is an argument because there is more than one.** §0 of
    `PLAN_PAIRWISE.md` was signed on 2026-08-24 and adjudicated; a run under
    `PLAN_PROPOSER_1600.md` that checked the closed thread's signature would find
    it valid and spend 1,200 calls on rows nobody has signed. A gate that reads
    the wrong file is worse than no gate, because it reports `ok`.
    """
    line = None
    if path.exists():
        for raw in path.read_text().splitlines():
            if raw.startswith("**Signed by Sergi:"):
                line = raw.strip()
                break
    signed = bool(line) and not re.search(r"_{3,}", line)
    return {
        "what": f"the signature line of §0 of {path.name}. {rows} governs this "
                f"stage's output and a model may not sign it (hard rule 2).",
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
# Stage D — the learned base, where there is no truth
# ---------------------------------------------------------------------------

def build_learned_questions(pairs, rules, ext, positions, cases, n):
    """
    One row per sampled pair. There is **no winner here and no key**: the row
    carries the two rules and the witness, and what the model says is the only
    thing that will decide an edge.

    The witness is the lowest-indexed case of `ext(a) & ext(b)`, deterministic
    and non-empty by construction — overlap is what put the pair in the
    population. Unlike stage C it is not restricted to any action, because there
    is nothing to restrict it to.
    """
    rows = []
    for k, ((a, b), pos) in enumerate(zip(pairs, positions)):
        inter = ext[a] & ext[b]
        idx = lowest_case_index(inter, n)
        ids = (a, b) if pos == 0 else (b, a)
        first = shown_rule(rules[ids[0]], SHOWN_AS[0])
        second = shown_rule(rules[ids[1]], SHOWN_AS[1])
        case = cases[idx]
        if not rules[a].matches(case) or not rules[b].matches(case):
            raise AssertionError(
                f"witness {idx} of {a}/{b} is not matched by both rules: the "
                f"bit convention is wrong (see the module header)")
        ea, eb = ext[a].bit_count(), ext[b].bit_count()
        rows.append({
            "index": k, "rule_a": a, "rule_b": b,
            "action_a": rules[a].action, "action_b": rules[b].action,
            "born_a": rules[a].born_at, "born_b": rules[b].born_at,
            "extension_a": ea, "extension_b": eb,
            "a_is_broader": ea > eb,
            "overlap_cases": inter.bit_count(),
            "witness_index": idx, "witness": case.as_dict(),
            "shown_as": {SHOWN_AS[0]: ids[0], SHOWN_AS[1]: ids[1]},
            "a_shown_as": SHOWN_AS[pos],
            "question": question(case, first, second),
        })
    return rows


def classify_learned(answer, row):
    """
    Three outcomes and none of them is right or wrong.

    There is no truth for these pairs, so what an answer produces is an EDGE or
    nothing. `PLAN_PAIRWISE.md` §10 says it in one line and this record repeats
    it: no correct-edge rate exists here.
    """
    if answer == row["action_a"] and answer != row["action_b"]:
        return "a_beats_b"
    if answer == row["action_b"] and answer != row["action_a"]:
        return "b_beats_a"
    return "none"


def learned_verdicts(rows, engine):
    """The same histogram as stage C, and outside every denominator for the same
    reason: a witness guarantees overlap and the validator cannot check that the
    declared winner is the correct one — here there is not even a correct one."""
    hist = Counter()
    for r in rows:
        if r["declared"] == "none":
            continue
        w = r["rule_a"] if r["declared"] == "a_beats_b" else r["rule_b"]
        loser = r["rule_b"] if r["declared"] == "a_beats_b" else r["rule_a"]
        v = engine.try_edge(w, loser)
        r["try_edge_verdict"] = v
        r["declared_winner"] = w
        r["declared_loser"] = loser
        hist[v] += 1
    return {
        "what": "what try_edge returns for the edge each answer implies, fed "
                "sequentially into an engine that starts with subsumption and no "
                "declared edge.",
        "outside_every_denominator":
            "yes. The population was filtered so that EDGE_DISJOINT and "
            "EDGE_CONTRADICTS cannot fire, so acceptance measures the protocol; "
            "and there is no truth here, so an accepted edge is not a correct "
            "one under any reading.",
        "counts": dict(sorted(hist.items())),
        "unreachable_here": UNREACHABLE,
        "reachable_here": [EDGE_OK, EDGE_CYCLE],
    }


def revealed_hierarchy(rows):
    """
    What the answers say about the queues, independent of the rules.

    Stage C found the proposer's competence is largely a fixed ranking of the
    eight queues (`results2/pair_judgement_baselines.json`). This is the same
    question asked of the learned base, and it needs no labels: for each
    unordered pair of queues, how often each side was named. A model applying a
    ranking is constant on every one of them.

    It measures a TENDENCY, not a score. Whether the order those answers compile
    into beats a queue ranking is a different question, and it is scored
    elsewhere against `results3/queue_hierarchy_floor.json`.
    """
    byp = defaultdict(Counter)
    for r in rows:
        if r["declared"] == "none":
            continue
        w = r["action_a"] if r["declared"] == "a_beats_b" else r["action_b"]
        loser = r["action_b"] if r["declared"] == "a_beats_b" else r["action_a"]
        byp[tuple(sorted((w, loser)))][w] += 1
    varying = {k: dict(v) for k, v in byp.items() if len(v) > 1}
    return {
        "what": "for each unordered pair of queues, how often each side was "
                "named the winner. A proposer applying a fixed ranking is "
                "constant on every one of them.",
        "n_queue_pairs": len(byp),
        "n_varying": len(varying),
        "constant_fraction": round(1 - len(varying) / len(byp), 4) if byp else None,
        "per_queue_pair": {" vs ".join(k): dict(v) for k, v in sorted(byp.items())},
    }


UNMADE_CHOICE = """
ABORTADO: --sample sin --reuse ni --reask-all.

  §2 de PLAN_PROPOSER_1600.md deja esta eleccion para el momento de la firma y
  dice que no es del redactor. No hay valor por defecto a proposito: las dos
  opciones cuestan dinero distinto y compran cosas distintas.

    --reuse       1.200 llamadas. Las 400 de la etapa D se reaprovechan, el
                  anidamiento es exacto y las fechas no lo son.
    --reask-all   1.600 llamadas. Una sola fecha, y las 400 pasan a ser una
                  REPLICA de la etapa D bajo protocolo identico: cuanto se
                  mueven las respuestas de un proponente entre dos dias.
"""


def main_learned(argv) -> int:
    dry_run = "--dry-run" in argv
    overwrite = FLAG in argv
    budget = DEFAULT_BUDGET
    if "--budget" in argv:
        budget = int(argv[argv.index("--budget") + 1])
    sample_path = None
    if "--sample" in argv:
        sample_path = Path(argv[argv.index("--sample") + 1])
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    reuse, reask = "--reuse" in argv, "--reask-all" in argv

    if sample_path is None:
        smoke = budget < 50
        out = OUT / (RECORD_LEARNED_SMOKE if smoke else RECORD_LEARNED)
    else:
        if reuse == reask:
            print(UNMADE_CHOICE)
            return 2
        smoke = limit is not None
        out = OUT / (RECORD_1600_SMOKE if smoke else RECORD_1600)
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])

    t_start = time.time()
    print("=" * 78)
    if sample_path is None:
        print("STAGE D — the pairwise question over the learned base, where "
              "there is no truth")
    else:
        print("STAGE B of PLAN_PROPOSER_1600 — the same question at the budget "
              "that discriminates")
    print("=" * 78)
    print(f"  model {MODEL} · temperature {TEMPERATURE} · "
          f"max_retries {MAX_RETRIES} · sequential")
    print(f"  {describe()}")

    space = Space()
    rules = learned_rules()
    pairs, ext, stats = learned_population(rules, space)
    g_pop = gate_population(stats, len(rules))
    cases = list(all_cases())

    # Stage D's output is governed by P-d and P-e, and Stage C's — `main`, not
    # this function — by P-c. The gate has always read the same file; until
    # 2026-08-25 it also always said `P-c`, in a record that was Stage D's.
    plan, governs, g_sample = PLAN, "P-d/P-e", None
    held, held_date = {}, None
    if sample_path is None:
        sampled = sample_population(pairs, budget)
        to_ask = sampled
    else:
        plan, governs = PLAN_1600, "B-a to B-d"
        sampled, sample_rec = load_sample(sample_path)
        if "--budget" not in argv:
            budget = len(sampled)
        g_sample = gate_sample_record(sample_rec, sample_path, budget)
        if reuse:
            base = json.loads((OUT / RECORD_LEARNED).read_text())
            held = {(r["rule_a"], r["rule_b"]): r for r in base["answers"]}
            held_date = (base.get("_env") or {}).get("recorded_at")
        to_ask = [p for p in sampled if p not in held]
        if limit:
            # Truncate the POPULATION before dealing, never the rows after.
            # Stage C found this on its own first smoke path: dealing over the
            # whole population and keeping a prefix leaves whatever split that
            # prefix happens to have, and the balance the gate demands is a
            # property of the pairs actually asked about.
            to_ask, held = to_ask[:limit], {}
            sampled = to_ask

    positions = winner_positions(len(to_ask))
    fresh = build_learned_questions(to_ask, rules, ext, positions, cases,
                                    space.n)

    if sample_path is None:
        rows = fresh
    else:
        # In the sample's order, which is the population's own — the same order
        # Stage D asked in. `try_edge` is fed sequentially and whether an edge
        # closes a cycle depends on the ones already in, so the order the rows
        # are written in is part of the measurement and not presentation.
        by_pair = {(r["rule_a"], r["rule_b"]): r for r in fresh}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows = []
        for k, pair in enumerate(sampled):
            reused = pair in held
            r = dict(held[pair]) if reused else by_pair[pair]
            r["index"] = k
            r["answer_from"] = "stage_d" if reused else "this_run"
            r["answered_at"] = held_date if reused else now
            rows.append(r)

    g_leak = gate_no_leak([r["question"] for r in rows])
    g_pos = gate_position_balance([SHOWN_AS.index(r["a_shown_as"])
                                   for r in rows])
    g_sig = gate_signature(plan, governs)

    print()
    print("POPULATION GATE — the three conditions over the 577 rules")
    for k, v in stats.items():
        print(f"  {k:<26}{v:>8}")
    print(f"  {'of the pairs':<26}{g_pop['n_pairs']:>8}   "
          f"population {g_pop['fraction']:.1%}, expected {GATE_POPULATION}"
          f"{'  ok' if g_pop['passes'] else '  NO'}")
    print()
    print("GATES — every one of them runs before a single call")
    checks = [("no leak", g_leak), ("position balance", g_pos),
              (f"{governs} signed", g_sig)]
    if g_sample is not None:
        checks.insert(0, ("the sample", g_sample))
    for name, g in checks:
        print(f"  {name:<20}{'ok' if g['passes'] else 'NO'}")
    if not g_pop["passes"]:
        print("\n  STOP: this is not the population §10 budgeted for.")
        return 1
    if g_sample is not None and not g_sample["passes"]:
        print(f"\n  STOP: {sample_path} is not Stage A's gated record for "
              f"{PLAN_1600.name} at {budget} pairs "
              f"(it holds {g_sample['n_pairs']}, plan "
              f"{g_sample['plan_named_by_the_record']}, failed gates "
              f"{g_sample['gates_that_failed']}).")
        return 1
    if not g_leak["passes"]:
        print("\n  STOP: a question names a rule or carries a declared edge.")
        return 1
    if not g_pos["passes"]:
        print(f"\n  STOP: presentation order not balanced "
              f"({g_pos['shown_first']} / {g_pos['shown_second']}).")
        return 1

    if dry_run:
        print()
        print(f"  DRY RUN — {len(rows)} questions built, nothing called, "
              f"nothing written")
        if sample_path is None:
            print(f"  sampled {len(sampled)} of {len(pairs)} at seed "
                  f"{SAMPLE_SEED}")
        else:
            print(f"  {len(rows)} pairs from {sample_path}, "
                  f"{len(held)} answers already held, "
                  f"{len(fresh)} to ask   ({'reuse' if reuse else 'reask-all'})")
        print(f"  {governs} signed: {g_sig['passes']}   ({plan.name})")
        print()
        r = rows[0]
        print(f"  ONE QUESTION ({r['rule_a']} / {r['rule_b']}, "
              f"{r['rule_a']} shown as {r['a_shown_as']})")
        for line in r["question"].splitlines():
            print(f"    {line}")
        print(f"\n  cost if run: {len(fresh)} calls. Nothing spent here.")
        return 0

    if not g_sig["passes"]:
        print(f"\n  STOP: §0 of {plan.name} is unsigned. {governs} govern")
        print("  this stage's output and a model may not sign them.")
        return 1
    g_key = gate_api_key()
    if not g_key["passes"]:
        print(f"\n  STOP: OPENROUTER_API_KEY does not reach this process.\n"
              f"    {g_key['how']}")
        return 1
    or_exit(refuse_overwrite, out, overwrite=overwrite,
            exits=("--out OTHER.json      write somewhere else",
                   f"{FLAG}   replace it on purpose"))

    judge = Judge()
    print()
    print(f"  {len(fresh)} calls, one per unanswered pair, sequential")
    if held:
        print(f"  {len(held)} answers reused from Stage D, dated "
              f"{held_date} — §2 of the plan, and §5.5: the date is not held "
              f"fixed and every row says which one it carries")
    failures = 0
    asked = 0
    for k, r in enumerate(rows):
        if r.get("answer_from") == "stage_d":
            # Verbatim, down to `declared`. Recomputing it would give the same
            # answer today and would be a second implementation of the thing
            # that produced the record.
            continue
        asked += 1
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
        r["declared"] = classify_learned(r["answer"], r)
        if asked % 50 == 0 or asked == len(fresh):
            print(f"    {asked}/{len(fresh)}")

    engine = PriorityEngine(space=space)
    for rid in sorted(rules):
        engine.add(Rule2(rule_id=rid, conditions=list(rules[rid].conditions),
                         action=rules[rid].action),
                   born_at=rules[rid].born_at, keep_id=True)
    hist = learned_verdicts(rows, engine)
    counts = Counter(r["declared"] for r in rows)
    accepted = [(r["declared_winner"], r["declared_loser"]) for r in rows
                if r.get("try_edge_verdict") == EDGE_OK]

    payload = {
        "_env": environment(model=MODEL, temperature=TEMPERATURE,
                            max_retries=MAX_RETRIES,
                            position_seed=POSITION_SEED,
                            sample_seed=SAMPLE_SEED, budget=budget),
        "what":
            "stage D of PLAN_PAIRWISE.md: the pairwise question asked of the 577 "
            "learned rules of rung 1. One call per sampled pair, sequential.",
        "stage": "D", "population": "learned base, results/llm_run.json",
        "there_is_no_truth_here":
            "no correct-edge rate exists for these pairs and none is computed. "
            "The hidden policy's layer order says nothing about rules it never "
            "wrote. What is measured is what the declared edges DO — as a hybrid "
            "engine, as an order, and as a machine — and that measurement lives "
            "in its own record.",
        "partial_run": smoke,
        "n_population": len(pairs), "n_sampled": len(rows),
        "sample": f"deterministic at seed {SAMPLE_SEED}, budget {budget}",
        "gates": {"population": g_pop, "no_leak": g_leak,
                  "position_balance": g_pos, "signature": g_sig},
        "system_prompt": SYSTEM_PROMPT,
        "what_the_model_was_not_shown":
            "the same three as stage C: correct_count, beats/loses_to, and the "
            "rule identifiers. The learned base numbers its rules in birth "
            "order, which does not encode priority the way the hidden policy's "
            "layers do — but they are hidden anyway, so the two stages ask the "
            "same question in the same shape.",
        "declared": dict(counts),
        "parse_failures": failures,
        "off_menu_answers": sum(1 for r in rows if r["off_menu"]),
        "n_edges_accepted": len(accepted),
        "accepted_edges": [list(e) for e in accepted],
        "try_edge_verdicts": hist,
        "revealed_hierarchy": revealed_hierarchy(rows),
        "answers": rows,
        "seconds": round(time.time() - t_start, 1),
    }
    if sample_path is not None:
        payload["gates"]["sample"] = g_sample
        payload.update({
            "plan": PLAN_1600.name, "stage": "B",
            "what":
                "Stage B of PLAN_PROPOSER_1600.md: the pairwise question of "
                "Stage D asked over 1,600 pairs instead of 400, because "
                "results3/FINDINGS3.md §10 showed that at 400 a perfect chooser, "
                "a 70%-accurate one and a coin are the same number. Same prompt, "
                "same model, same settings — rule 5 of its §4.",
            "sample_record": str(sample_path),
            "answers_reused": len(held),
            "calls_made": asked,
            "the_choice_of_§2":
                ("reuse: the 400 of Stage D were not re-asked, so the nesting is "
                 "exact and the dates are not"
                 if reuse else
                 "reask-all: every pair was asked on one date, and the 400 are a "
                 "replication of Stage D under an identical protocol"),
            "the_date_is_not_held_fixed":
                "each row carries `answered_at`, the date the answer it holds "
                "came from. §5.5 of the plan: whichever option was taken, any "
                "comparison between the two halves is labelled with it.",
        })
    OUT.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))

    rv = payload["revealed_hierarchy"]
    print()
    print("=" * 78)
    print("WHAT CAME BACK — no correct-edge rate exists here")
    print("=" * 78)
    print(f"  edges declared {counts['a_beats_b'] + counts['b_beats_a']}   "
          f"no edge {counts['none']}   (parse failures {failures})")
    print(f"  accepted by try_edge {len(accepted)}   "
          f"verdicts {hist['counts']}")
    print(f"  revealed hierarchy: constant on "
          f"{rv['n_queue_pairs'] - rv['n_varying']} of {rv['n_queue_pairs']} "
          f"queue-pairs ({rv['constant_fraction']:.1%})")
    print(f"\n-> {out}")
    return 0


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--learned" in argv:
        return main_learned(argv)
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
    n_clean_total = len(clean)
    # Truncate the POPULATION before dealing, never the rows after. Dealing over
    # 170 and then keeping the first ten leaves whatever split that prefix
    # happens to have — 4/6 on the declared seed — and the balance the gate
    # demands is a property of the pairs actually asked about, not of a
    # population the run never reaches. Found by the gate itself on the first
    # smoke path, before a single call was spent.
    if limit:
        clean = clean[:limit]
    rules = hidden_rules()
    engine = fresh_engine(rules)
    positions = winner_positions(len(clean))
    rows = build_questions(clean, rules, positions)
    add_breadth(rows, engine)

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
        "n_clean_available": n_clean_total,
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
