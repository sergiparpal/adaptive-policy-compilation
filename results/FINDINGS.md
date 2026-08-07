# Rung 1 — findings

Closing record. August 5-6, 2026.
Corpus: 2000 cases, seed 17, 1743 unique. Hidden policy: 29 rules in 8 layers.
Proposer: `deepseek/deepseek-v4-flash` via OpenRouter.

The rung closes without having measured its hypothesis. The question it set out
to answer — whether the rules an LLM writes get reused or memorize cases — never
became measurable, because the engine it was being measured on cannot execute
the class of policy it was being asked to execute. What follows is what was
established.

---

## The result

**Priority in a stratified policy is not recoverable from the syntactic shape of
the rules.**

The hidden policy is a list prioritized by layers: security overrides, SLO and
on-call, billing, churn risk, product routing, language and staffing, deflection,
defaults. First match wins. Its content lives in the conditions of each rule; its
structure lives in the order between them.

The engine receives the rules without that order and has to reconstruct it from
the only thing it sees: the shape of the rules. Three criteria for doing so were
tried. None works, and not through mistuning a parameter: they fail for
structurally different reasons.

The DSL is not the culprit. Verified exhaustively over the 134,400 combinations
of the case space that the 29 rules written in the DSL are equivalent to their
original predicates, and that evaluating them with "first match wins" reproduces
the policy exactly. An execution failure, not a representation failure.

---

## The three falsified routes

All figures with the **perfect** policy loaded, except where indicated. None
involves the LLM.

### 1. Specificity — number of conditions

`RuleEngine.decide`: the rule with the most conditions wins; a tie with different
actions returns CONFLICT.

```
ACTION 1495   IMPASSE 0   CONFLICT 505 (25.3%)
coverage 0.7475   silent error 0.2140 (320 cases)   e2e 0.5875
```

Priority and number of conditions are nearly orthogonal in this policy. H24
(layer 6, 2 conditions) beats H16, H18 and H03 (layers 4 and 0, 1 condition
each) and steals 246 cases from them. The catch-all H29 has 1 condition and
therefore ties on specificity with every single-condition layer rule, generating
a conflict instead of yielding.

Proof that no monotone function of specificity can work, using only rules from
the policy itself: H01 (2 conditions) must beat H03 (1), and H16 (1) must beat
H24 (2). The two requirements are incompatible under any criterion monotone in
the number of conditions.

Corollary about the experiment's frontier: the rules of `keep_k(k)` all have
exactly k conditions, so their specificity is uniform and arbitration can never
invert them — the tie-break falls to age, which is the correct semantics. The
mocks are structurally immune to the defect that destroys the real policy.
`keep_k(k=4)` scores better than the true policy under this engine: 0.173 silent
error versus 0.214, and 0.780 e2e versus 0.588. The "region to beat" was above
the system's ceiling.

Reproducible: `python3 -m harness.ceiling_check`.

### 2. Arrival order — age of the rule

The oldest matching rule wins, without looking at specificity.

```
design order      100.0%
reverse order      12.8%
random order       49.3%   (mean over 200 samples)
```

The 100% of the design order is a tautology: loading the rules in the policy's
order and saying "the oldest wins" *is* first-match-wins. It shows that the DSL
plus a total order suffice to execute the policy, and nothing more.

What matters is the rest of the curve. The criterion has no content of its own:
it transports whatever order it is given. And in a learned base the arrival order
runs systematically backwards from the correct one, because the first cases come
from the common distribution and beget default rules, while the exceptions —
which must have priority — are born late.

(The reverse- and random-order figures are recorded in `PREDICTION.md`; the repo
only automates the design order.)

### 3. Semantic subsumption — inclusion of extensions

`A ≺ B` iff the set of cases A matches is a strict subset of B's, computed over
the full space of 134,400 combinations. It does not count conditions: it compares
extensions. The minimal element of the partial order wins; if the minimal
elements disagree on the action, CONFLICT.

It is the only one of the three criteria that is not monotone in the number of
conditions, so it can simultaneously satisfy H01 ≺ H03 and the incomparability of
H16 with H24.

**Over the hidden policy, written by a human:**

```
ordered pairs 61 of 406 (15.0%)   contradictions with the layer order: 0
ACTION 1263   CONFLICT 737 (36.9%)
silent error 0.0000  (0 of 1263)   e2e 0.6315
```

Zero contradictions, and soundness follows from that: if some matching rule were
strictly below the earliest-layer rule, that pair would contradict the layer
order; since there are none, the correct rule is always in the minimal set. The
engine stops being wrong silently: either it is right, or it declares that it
does not know.

The residue is also concentrated. 737 cases in 131 minimal sets, and breaking
ties by frequency gives:

```
k=10 -> e2e 0.8415     k=20 -> 0.8870     k=50 -> 0.9495     k=131 -> 1.0000
```

with silent error 0.0000 all the way. A total order over 29 rules is not needed:
a few dozen targeted tie-breaks suffice.

**Over the learned base, 577 rules written by the LLM:**

```
ordered pairs 8599 of 166176 (5.17%)
ACTION 160   CONFLICT 1840
cases where it commits: 160   of those, wrong action: 85  (53.12%)
coverage 0.0800   silent error 0.5312   e2e 0.0375
residue: 873 minimal sets; the first 10 cover 122 cases
```

The three properties disappear at once. Soundness goes from 0.00% to 53.12%
error: worse than a coin. Coverage drops to 8%. The residue goes from 131
concentrated sets to 873 diffuse ones.

The rules responsible for the lack of soundness are narrow — 4 to 6 conditions,
small extension — and that is why subsumption declares them minimal and lets them
win, with the wrong action. A small extension does not mean a correct one.

Reproducible: `python3 -m harness.subsumption_check` and
`python3 -m harness.learned_subsumption`.

---

## The formulation

The three criteria are **syntactic proxies for authored priority**.

They work to the extent that an author encoded the priority in the shape of the
rules, and they carry no signal when nobody did. Specificity assumes the author
put more conditions on what has more priority. Arrival order assumes the author
wrote the highest-priority thing first. Subsumption assumes the author nested the
exceptions inside the defaults.

In the hidden policy the third assumption holds — hence the 0.00% error —
because whoever wrote it put the exceptions before the defaults, which is how
healthy layered policies are written. That 0.00% does not measure a virtue of the
criterion: it measures a virtue of the author. The learned base has no author in
that sense, and the same criterion produces 53.12% error.

Compilation by impasse learns rules. It has no mechanism whatsoever for learning
priority. In a stratified policy the structure lives there.

---

## Why a more capable model does not fix it

The necessary information is not in the proposer's context.

The proposer sees a ticket and the domain vocabulary. It does not see the
existing rule base, it does not see which rules already cover neighbouring
regions, and it does not see why the case presented to it got as far as it. With
that, a relative priority cannot be decided, because priority is a relation
between rules and it has only one.

The clearest case is on record. The region `product == dashboard AND severity
<= 3` covers 382 cases (19.1% of the corpus) and touches 15 distinct hidden
rules; `T1_GENERAL` is the truth in only 21.5% of it. The case that originated
the rule covering that region is resolved by H29, the catch-all `lambda c: True`,
after 28 layers fail. The proposer sees a correct answer and cannot know that it
is correct by elimination. It generalized a residue as if it were a positive
rule. It happened in both runs, in different ways: in the n=100 one with the
correct action and the wrong scope, in the n=2000 one getting the action wrong
too.

No increase in capability reconstructs a relation from a single operand. And the
figures that would be attributed to the model's capability are small: in the
voided run, replacing each rule's action with the truth of its originating case
lowered the silent error from 0.4839 to 0.4298 — 5 points out of 48 — and giving
each rule its optimal action still left it at 0.2909. The rest is scope, not
queue choice.

---

## What remains open

Declaring the priority instead of inferring it.

If priority is not recoverable from the shape of the rules, the alternative is
for it to be part of what gets written: a field in the schema, an explicit
reference to the rule this one is an exception to, or any other representation
the validator can check. That forces giving the proposer the existing rule base
as context, because a relative priority cannot be declared without seeing what it
is relative to.

It is an authorship problem, not an arbitration one. It changes what the proposer
is asked for and what it is shown, not how the engine breaks ties. It is not
measured: all that is recorded here is that the three inference routes are
falsified.

---

## Caveats

**Bounds, not simulations.** The 577 rules of the learned base were written under
specificity-based arbitration. Which case escalated — and therefore which rule
was born — depended on that arbitration. Under subsumption from the first case
the base would have been another one. What was measured is how that base behaves
under a different arbitration, not what the loop would have produced. Also, in
that measurement the 577 rules are loaded from case 0, whereas in the run they
accumulated; that is why the static specificity figures (coverage 0.4290, e2e
0.1825) do not match those of `results/llm_run.json` (0.684 and 0.353).

**Non-determinism at temperature 0.** The corpus is deterministic (seed 17); the
proposer is not. Same prompt, same case, same seed, and the rules born from the
first cases differ between the n=100 run and the n=2000 one. The smoke test is
not a prefix of the full run, and a comparison between models does not have the
model as its only variable unless several sampling seeds are averaged.

**Soundness verified over a single hidden policy.** Subsumption's 0.00% error was
checked over the 29 rules of `hidden_policy.py` and over no other. It is a
property of that specific policy, not a theorem. How often hand-written policies
satisfy it in general is unknown, as is whether the result survives a different
stratification.

**One model, one run.** The proposer figures come from
`deepseek/deepseek-v4-flash` in a single execution. The run was voided by the
engine ceiling before comparing models made any sense.

---

## Lineage

Compilation by impasse comes from SOAR's *chunking*: when problem solving gets
stuck, the system resolves the impasse in a subspace and compiles the result into
a new rule, so that next time it does not get stuck.

What was borrowed here was the compilation mechanism. What was not borrowed was
the structure that makes it well defined. In SOAR the impasses occur within a
goal hierarchy, and the compiled rule is born within the context of the subgoal
that resolved the impasse; the order among alternatives is fixed by preferences
which in turn produce rules. Priority is declared by the system, not inferred
from the shape of the productions.

Here the base was made a flat list and the arbitration a syntactic criterion
computed over the rules. The impasse hierarchy, which is where the priority
structure lived, was not replicated. The structure lost in flattening is exactly
what the three criteria then tried to reconstruct, without succeeding.

---

## Files

```
harness/ceiling_check.py         engine ceiling; specificity and design order
harness/subsumption_check.py     partial order by subsumption, hidden policy
harness/learned_subsumption.py   the same criterion over the learned base
results/frontier.json            sweep of mocks and baselines
results/llm_run.json             voided run, n=2000, raw per-case records
results/llm_run_n100_smoke.json  prior smoke test
results/subsumption.json         partial order and concentration curve
results/learned_subsumption.json soundness over the learned base
PREDICTION.md                    recorded prediction and voiding statement
```
