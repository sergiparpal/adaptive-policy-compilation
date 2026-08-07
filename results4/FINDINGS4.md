# Rung 4 — finding

Record. August 6, 2026. Base: the 577 rules from rung 1, the corpus of 2000 cases
with seed 17 and the same splits as rung 3. Zero LLM calls. Step A only; Step B
(online ordering) was not run.

References from rung 3, on test: full oracle 0.7707 · 5% of labels 0.7049 · 1% of
labels 0.5251 · born_at 0.5216 · random 0.4227 · ceiling 0.8995.

---

## 1. The central result

**The viability limit is not in the coverage, nor in the delay, nor in the noise.
It is in the asymmetry, and it is not a gradual limit but a change of regime.**

With symmetric feedback — the channel confirms both correct decisions and errors
— the learned order beats born_at across the whole coverage sweep, to the very
end:

```
coverage     labels   test e2e   vs born_at
      1.0      1010     0.7564      +0.2348
      0.5       500     0.7520      +0.2304
     0.25       245     0.7803      +0.2587
      0.1        99     0.7399      +0.2183
     0.05        52     0.7087      +0.1871
     0.02        19     0.6393      +0.1177
```

**With 19 labels it still gets +0.118 over learning nothing.** Delay is almost
free offline: from 0 to 400 cases it goes from 0.7564 to 0.7540.

As soon as the channel stops confirming correct decisions, the regime changes:

```
asymmetry    labels   test e2e   vs born_at
      1.0      1010     0.7564      +0.2348
      0.5       751     0.7954      +0.2738
     0.25       622     0.7117      +0.1901
      0.1       544     0.6185      +0.0969
      0.0       498     0.5887      +0.0671
```

The cell `coverage=1, asymmetry=0, delay=0, noise=0` is **completely
deterministic** — with no draw of any kind — and gives **0.5887**: the best
possible case of a realistic channel, with feedback on every error and none lost,
contributes **+0.067** over learning nothing. The full oracle gave +0.235.

> **[ERRATUM 2026-08-06]** "Completely deterministic" is **false**. The channel
> is deterministic in that cell — it consumes no draw — but the greedy search
> that consumes its output is not: the three greedy searches
> (`order_search.py`, `budget_and_balance.py`, `sweep.py`) resolved the argmax by
> iterating over a `set` of identifiers, whose order depends on
> `PYTHONHASHSEED`. Measured over five hash seeds, that same cell gives:
>
> ```
> PYTHONHASHSEED   0      1      2      7     42
>                0.5991 0.5880 0.5971 0.5988 0.5937      spread 0.0111
> ```
>
> The recorded 0.5887 is one of those values, not the only possible one. **The
> direction of the finding survives**: at the worst hash the margin over born_at
> (0.5216) is still **+0.066**, and the 24 cells of the realistic regime remain
> far below the symmetric regime. What does not survive is the word
> "deterministic" or the specific digit.
>
> The tie-break was fixed on August 6, 2026 (iteration over a sorted list).
> **Rungs 3 and 4 were NOT re-run**: that will be done together with the serious
> optimizer, so as to distinguish whether the fragility was in the tie-break or
> in the algorithm. All the figures in these documents are those of the code
> prior to the fix.
>
> **About the 14.5x margin** used when arguing that the finding survives: it
> compared `a=1` measured under **a single hash** against the mean of five hashes
> of `a=0`. The direction holds and so does the worst case, but the ratio is not
> clean and must not be cited as if it were.

The 24 cells of the realistic regime (asymmetry 0) fall between **0.5448 and
0.6509**, and at coverage 0.1 the improvement (+0.023 to +0.047) lies within its
own standard deviation.

**Symmetric supervision is exactly what this rung existed in order not to
assume.** Rung 3 measured 0.7049 with 5% of the labels and from there came the
hypothesis that a poor channel would suffice. The hypothesis holds as long as the
channel is an unbiased sample of labels. It stops holding as soon as the channel
is what a real system produces.

---

## 2. The channel as a separate artefact

The risk declared when the rung was opened: in a synthetic environment
"environment feedback" and "hidden policy" are the same function, and without
bounding the channel this measures full supervision under another name.

Containment: **`peldano4/feedback.py` is the only module in the rung that imports
`true_action`.** It emits `{case -> reported action}` and nothing else. The
learner receives neither the truth, nor whether the decision was correct, nor
which cases went unobserved. The truth reappears only in the evaluation, which is
measurement and not supervision, just as in the three previous rungs.

> **[ERRATUM 2026-08-06]** "The only module that imports `true_action`" is
> literally false: `peldano4/sweep.py:36` imports it too. The import **is unused**
> (zero calls in the file), but the claim as written is not true and must not be
> defended by its intent.
>
> **The substantive separation does hold**, and that is what matters: the learner
> is `greedy_from_reports`, which receives only `reported` and has no access to
> the truth by any route. `sweep.py` handles truths through `build_tables` for two
> uses that are not supervision — evaluating the resulting order and computing the
> reported error rate of π₀ — and never passes them to the learner.
>
> Correct wording: *`feedback.py` is the only module that consults the oracle in
> order to produce the learning signal; the learner does not see it by any route.*

The channel does not observe loose labels but **outcomes of decisions**, which
requires a reference policy π₀ to be deciding while the observation happens.
Without that, "what fraction of decisions receives an outcome" means nothing. In
a real system the cycle is: the ticket gets routed, someone receives it, and if
the queue was not theirs they reassign it; the reassignment is the feedback and
it brings the correct action.

| parameter | what it is | what it corresponds to |
|---|---|---|
| `coverage` c | p(feedback \| incorrect decision) | not every misrouted ticket gets reassigned: some are resolved anyway in the wrong queue, others are closed, others nobody touches |
| `asymmetry` a | p(feedback \| correct) = c·a | **the parameter that keeps the channel from being the oracle.** Nobody sends a message saying "this ticket was routed correctly". With a=0 the labelled set is conditioned on π₀ having been wrong: it is not i.i.d., and that dependency is the one a deployed system would have |
| `delay` d | the outcome of case i is usable only if i+d falls within the window | the reassignment happens hours or days later, with many tickets in between |
| `noise` e | with probability e the reported action is a different one | whoever reassigns also makes mistakes, or applies a local convention that is not the policy |

**A declared decision, not an omission:** the absence of feedback is **not**
interpreted as "it was correct". It would be tempting because it would double the
signal, but with partial coverage the absence is ambiguous — it may be a correct
decision or it may be that nobody looked — and assuming the former would inject
information the environment does not give.

---

## 3. The structural ceiling: the signal runs out as the system improves

```
π₀ observed                     errors of π₀   labels   test e2e
born_at        (0.5216 on test)        49.4%      248     0.5817
specificity    (0.1829 on test)        54.4%      273     0.7320
```

(c=0.5 · a=0 · d=0 · e=0.1)

**Observing a worse system produces a better order.** This is not a quirk of the
setup: it is a property of learning from error feedback.

With low asymmetry the labels arrive only from failures. The volume of signal is
proportional to the error rate of the observed system. A system that already works
well stops generating the signal it would need in order to keep improving, and it
does so exactly in the region where the hard cases remain. Learning by correction
has a fixed point that does not coincide with the optimum, and it has it by
construction of the channel, not through weakness of the learner.

It is the same phenomenon, seen from the other side, that made the silent error
measurable: the system cannot ask for help about what it resolves confidently.

---

## 4. The noise contamination, and its methodological consequence

In the sweep, **more noise gave better results**: 0.7564 with clean labels,
0.8198 with 10% falsified. That is impossible as an effect of supervision, so it
was diagnosed before reporting anything.

**Instability from tie-breaks ruled out.** With identical labels and 12 different
iteration orders for the greedy search: mean 0.7518, **standard deviation
0.0000**, range 0.7518–0.7518. The method is deterministic given the labelled set.

> **[ERRATUM 2026-08-06] The null test did not prove what it said it proved, and
> this is the most informative of the four errors.**
>
> The test permuted the `rules` list passed to the greedy search. But the argmax
> loop iterates over `left = set(ids)`, and the iteration order of a `set` of
> strings is determined by their **hashes**, not by the insertion order of the
> source list. That is: something that did not affect the tie-break was permuted,
> a variance of 0.0000 came out, and that zero was interpreted as proof of
> determinism.
>
> **The 0.0000 was correct and measured nothing.** A null result only rules
> something out if the instrument could have detected it, and this one could not.
>
> Repeated correctly — varying `PYTHONHASHSEED`, which is what governs the real
> tie-break — the greedy search **is** sensitive to the tie-break: ~0.011 of
> spread in the anchor cell of section 1.
>
> This **does not invalidate the noise diagnosis** that follows below, which is
> of another order of magnitude (0.7574 → 0.8337 against the truth, versus 0.011
> from tie-breaks) and rests on the train-vs-labels versus train-vs-truth
> comparison, not on the null test. What it does do is reinforce its conclusion:
> the greedy search is a weak optimizer, and it is now known to be weak even
> against perturbations as small as the iteration order.

The real diagnosis (24 runs per row):

```
noise   TRAIN vs labels   TRAIN vs TRUTH   TEST vs truth
  0.0           0.7574           0.7574          0.7564
  0.1           0.7462           0.8259          0.8163
  0.3           0.5996           0.8337          0.8171
  0.5           0.4250           0.7398          0.7004
```

The objective the greedy search optimizes goes down as it should (0.7574 →
0.5996). The resulting order, measured against the truth, **goes up** (0.7574 →
0.8337). With perfect labels the greedy search stays at 0.7574 against the truth;
with 30% falsified it reaches 0.8337.

**The greedy search with clean labels falls into a bad local optimum and the
noise pulls it out**, acting as a random restart. This is consistent with what was
measured in rung 3: searching for the order over the test set itself still left
0.1187 below the ceiling. The greedy search is a weak optimizer, and perturbing
its objective improves it.

**Methodological consequence:** any channel parameter that injects randomness
acts partly as an improvement to the search and not as a degradation of the
supervision. The noise and coverage sweeps with asymmetry 1 **cannot be read as
degradation curves**. That is why the central result is anchored in the
deterministic cell (c=1, a=0, d=0, e=0) and in the full range of the 24 cells of
the realistic regime, not in the contaminated curves.

The method was not corrected. Changing the optimizer after seeing the numbers is
exactly the failure this experiment studies.

---

## 5. What the four rungs leave regarding the original architecture

The architecture was: a cheap symbolic engine resolves what it covers; when it
fails to cover a case, an LLM acts and writes a rule so that next time it does
cover it. The hypothesis to measure: whether those rules get reused or whether
the model memorizes cases.

**That hypothesis still has not been measured.** Rung 1 was voided by the engine
ceiling, and its reuse figure of 0.158 described the arbitration, not the
induction.

What was established, in order:

- **Priority is the missing piece, and it is not in the shape of the rules.**
  Three syntactic criteria falsified: specificity (0.5875 with the perfect policy
  loaded), arrival order (100% in design order, 12.8% reversed, 49.3% random) and
  subsumption (0% error over the hand-written policy, 53.12% over the learned
  base). They are proxies for authored priority: they work to the extent that an
  author encoded it in the shape, and they carry no signal when nobody did.

- **The mechanism for executing it exists and works.** Subsumption plus 199
  declared edges execute the eight-layer policy at 100%: e2e 1.0000, silent error
  0.0000, zero conflicts, zero impasses.

- **The proposer does not supply it.** With the base in front of it, the overlap
  arithmetic resolved by the engine and the explicit instruction to overlap, it
  writes mostly disjoint rules and argues it as a merit. Eight runs, two
  conflicts, zero accepted edges. The change introduced to make priority possible
  is the one that left it with no material to measure.

- **The proposer's material was far better than it looked.** Ceiling 0.90 over
  the same 577 rules that arbitration was turning into 0.18.
  `SECURITY_INCIDENT` and `ONCALL_ESCALATION` are 100% recoverable and gave 0/17
  and 0/7. And which classes get sacrificed turned out to be a choice of
  objective function that nobody had declared.

- **Priority is not learned from the feedback a real system gives either.** With
  symmetric supervision almost everything is recovered (+0.235); with the
  asymmetric kind, which is the only realistic one, +0.067 remains, and the signal
  runs out as the system improves.

The three ways of supplying priority — infer it from the syntax, have the
proposer declare it, learn it from observed behaviour — have been measured, and
each fails for a different reason. Compilation by impasse learns rules; the
structure of a stratified policy does not live in the rules.

---

## Files

```
peldano4/feedback.py    the channel; only module that imports true_action
peldano4/sweep.py       sweeps, realistic grid and sensitivity to π₀
results4/sweep.json     every measured cell
```

Reproducible with `python3 -m peldano4.sweep`. Zero API calls.

Step B — online ordering, with the base growing and feedback arriving with delay
— was not run: the asymmetry answers the question the rung existed to answer, and
online ordering would only degrade it further.
