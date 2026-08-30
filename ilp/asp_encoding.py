"""
THE INDUCER — an ordered decision list, chosen by clingo under the objective §1
of `PLAN_ILP.md` declares.

--------------------------------------------------------------------------
THE ENCODING, AND WHY IT IS THIS ONE
--------------------------------------------------------------------------
The obvious encoding pre-enumerates candidate bodies and gives the solver
`covers(body, case)`. On the real training set that is **839,070 bodies over 316
cases** — hundreds of millions of ground atoms, and clingo never gets to search.

So the solver chooses **conditions per rule slot** instead of choosing among
bodies. The search space is the same; the grounding is linear in the number of
conditions rather than combinatorial:

    holds(T,C)        224 x |cases|, computed in Python and passed as facts
    use(S,T)          K x 224 choices
    nothold(S,C)      K x |cases|
    covers(S,C)       K x |cases|

With `K` slots and 316 cases that is tens of thousands of atoms rather than
hundreds of millions.

**First-match-wins is the slot order**, which is what makes the output a decision
list and not a rule set: slot `S` decides case `C` when it covers `C` and no
lower-numbered slot does. The proposer never supplied that order and rungs 3 and 4
had to search for it; here it falls out of the same optimisation.

--------------------------------------------------------------------------
THE OBJECTIVE, DECLARED IN §1 AND NOT TUNED AFTERWARDS
--------------------------------------------------------------------------
Lexicographic, in clingo priority order:

    @3  maximise correctly classified training cases
    @2  minimise the number of slots used
    @1  minimise the total number of conditions

**`I-d`'s band reads the second of those**, so the plan says in advance that
`I-d` measures this encoding as much as it measures induction, and that it is the
weakest of the four rows as a test.

--------------------------------------------------------------------------
TWO THINGS THAT ARE NOT KNOBS
--------------------------------------------------------------------------
**Symmetry breaking is sound, not heuristic.** Used slots are constrained to be a
prefix (`:- used(S), not used(S-1)`), which removes the K! relabelling of the same
list without removing any list.

**`MAX_SLOTS` is a cap on the search, and whether it binds is reported.** If the
best list found uses every slot, the number is a fact about the cap and
`result["hit_the_cap"]` says so — the same discipline as `I-g4` reporting whether
optimality was proved rather than assumed.

`clingo` is imported lazily. Nothing else in this repository depends on it, the
test suite skips what needs it, and `requirements-ilp.txt` says why it is not in
`requirements.txt`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from harness.domain import ACTIONS

from .language import MAX_CONDITIONS, language

# Declared before any figure exists. The cap is generous — the hidden policy is
# 29 rules and the learned base is 577 — and whether it binds is reported.
MAX_SLOTS = 40
DEFAULT_TIME_LIMIT = 300.0        # seconds; recorded in the record's `_env`


@dataclass
class Induced:
    """What the inducer returns: an ordered list of (body, action)."""

    rules: list[tuple[tuple[int, ...], str]] = field(default_factory=list)
    proved_optimal: bool = False
    exhausted_search: bool = False
    accuracy_objective_proved: bool = False   # all training cases correct: @3 is
                                              # at its maximum whether or not the
                                              # parsimony objectives are proved
    hit_the_cap: bool = False
    train_correct: int = 0
    n_train: int = 0
    seconds: float = 0.0
    models: int = 0
    cost: tuple = ()

    @property
    def n_rules(self) -> int:
        return len(self.rules)

    @property
    def n_conditions(self) -> int:
        return sum(len(body) for body, _a in self.rules)


PROGRAM = """
slot(1..k).

% A slot is either unused or carries one action and 1..m conditions with
% distinct attributes.
{ used(S) } :- slot(S).
1 { act(S,A) : action(A) } 1 :- used(S).
1 { use(S,T) : cond(T) } m :- used(S).
:- use(S,_), not used(S).
:- act(S,_), not used(S).
:- use(S,T1), use(S,T2), T1 < T2, attr(T1,A), attr(T2,A).

% Sound symmetry breaking: the used slots are a prefix.
:- used(S), S > 1, not used(S-1).

% Coverage. A slot covers a case when none of its conditions fails on it.
nothold(S,C) :- use(S,T), case(C), not holds(T,C).
covers(S,C) :- used(S), case(C), not nothold(S,C).

% First match wins: the slot order is the list order.
earlier(S,C) :- covers(S2,C), slot(S), S2 < S.
fired(S,C) :- covers(S,C), not earlier(S,C).
correct(C) :- fired(S,C), act(S,A), example(C,A).

#maximize { 1@3,C : correct(C) }.
#minimize { 1@2,S : used(S) }.
#minimize { 1@1,S,T : use(S,T) }.

#show use/2.
#show act/2.
"""


def _facts(holds: list[int], labels: list[str], n_cases: int) -> str:
    """`holds/2` only where the condition is true, which is what keeps the
    grounding to the size the docstring claims."""
    lang = language()
    out = [f"action({_sym(a)})." for a in sorted(ACTIONS)]
    out += [f"case({c})." for c in range(n_cases)]
    out += [f"cond({t})." for t in range(len(lang))]
    out += [f"attr({t},{_sym(lang[t][0])})." for t in range(len(lang))]
    for t, mask in enumerate(holds):
        for c in range(n_cases):
            if (mask >> c) & 1:
                out.append(f"holds({t},{c}).")
    out += [f"example({c},{_sym(a)})." for c, a in enumerate(labels)]
    return "\n".join(out)


def _sym(name: str) -> str:
    """ASP constants are lowercase; the mapping is reversed on the way out."""
    return f"c_{name.lower()}"


def _unsym(sym: str) -> str:
    return sym[2:].upper()


def induce(holds: list[int], labels: list[str], n_cases: int,
           max_slots: int = MAX_SLOTS,
           max_conditions: int = MAX_CONDITIONS,
           time_limit: float = DEFAULT_TIME_LIMIT,
           threads: int = 1) -> Induced:
    """Optimise a decision list over the given labelled cases.

    `holds` is one bitmask per condition of `language()`, LSB-first over the
    cases; `labels[c]` is the true action of case `c`. **No other input exists**:
    the inducer never sees the hidden rules, the layer order, the test split or
    the learned base — `I-g3` checks that on this signature."""
    import clingo                      # lazy: see the module docstring

    t0 = time.time()
    program = (PROGRAM.replace("1..k", f"1..{max_slots}")
                      .replace("} m :-", f"}} {max_conditions} :-"))
    ctl = clingo.Control([f"--parallel-mode={threads}"])
    ctl.add("base", [], _facts(holds, labels, n_cases))
    ctl.add("base", [], program)
    ctl.ground([("base", [])])

    best: dict = {}
    models = 0

    def on_model(model):
        nonlocal best, models
        models += 1
        use: dict[int, list[int]] = {}
        act: dict[int, str] = {}
        for sym in model.symbols(shown=True):
            if sym.name == "use":
                use.setdefault(sym.arguments[0].number, []).append(
                    sym.arguments[1].number)
            elif sym.name == "act":
                act[sym.arguments[0].number] = _unsym(sym.arguments[1].name)
        best = {"use": use, "act": act, "cost": tuple(model.cost)}

    with ctl.solve(on_model=on_model, async_=True) as handle:
        handle.wait(time_limit)
        handle.cancel()
        res = handle.get()

    rules = []
    if best:
        for slot in sorted(best["use"]):
            rules.append((tuple(sorted(best["use"][slot])), best["act"][slot]))

    out = Induced(
        rules=rules,
        proved_optimal=bool(res.satisfiable and res.exhausted),
        exhausted_search=bool(res.exhausted),
        hit_the_cap=len(rules) == max_slots,
        n_train=n_cases,
        seconds=round(time.time() - t0, 2),
        models=models,
        cost=best.get("cost", ()),
    )
    out.train_correct = score(out, holds, labels, n_cases)["correct"]
    out.accuracy_objective_proved = out.train_correct == n_cases
    return out


def score(induced: Induced, holds: list[int], labels: list[str],
          n_cases: int) -> dict:
    """First-match-wins over the induced list, on any set of cases.

    Used for training and for every surface a row is read on, so the training
    figure and the test figure are produced by the same code."""
    from .language import body_extension

    full = (1 << n_cases) - 1
    remaining = full
    per_action: dict[str, int] = {}
    for body, action in induced.rules:
        hit = body_extension(body, holds, full) & remaining
        if hit:
            per_action[action] = per_action.get(action, 0) | hit
            remaining &= ~hit

    truth: dict[str, int] = {}
    for c, a in enumerate(labels):
        truth[a] = truth.get(a, 0) | (1 << c)

    correct = sum((m & truth.get(a, 0)).bit_count()
                  for a, m in per_action.items())
    decided = sum(m.bit_count() for m in per_action.values())
    return {
        "n": n_cases,
        "decided": decided,
        "undecided": n_cases - decided,
        "correct": correct,
        "accuracy_end_to_end": correct / n_cases if n_cases else 0.0,
        "per_action": {a: m.bit_count() for a, m in per_action.items()},
        "correct_by_action": {a: (m & truth.get(a, 0)).bit_count()
                              for a, m in per_action.items()},
    }


def as_dsl(induced: Induced) -> list[dict]:
    """The induced list in the frozen DSL's own payload shape, so the record
    carries rules that `validate_rule_payload` would accept."""
    lang = language()
    out = []
    for i, (body, action) in enumerate(induced.rules):
        out.append({
            "rule_id": f"L{i + 1:02d}",
            "conditions": [
                {"attr": lang[t][0], "op": lang[t][1],
                 "value": list(lang[t][2]) if lang[t][1] == "in" else lang[t][2]}
                for t in body],
            "action": action,
        })
    return out
