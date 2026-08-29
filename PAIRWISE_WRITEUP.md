# The pairwise question — what changing the question bought, and what it did not

**What this is.** The write-up of the two closed threads that changed the question
put to the proposer, from *write a rule* to *which of these two rules wins this
ticket?* — [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md), closed 2026-08-24, and
[`PLAN_PROPOSER_1600.md`](PLAN_PROPOSER_1600.md), closed 2026-08-26. Seven signed
rows adjudicated, 1,770 API calls, and everything else free. It is item 4 of
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md)'s plan, which called it *the actual
deliverable*.

**What this is not.** It **owns no figure.** Every number below names the record
that owns it, the **surface** it was measured on (corpus / exhaustive space) and,
where an order is scored, the **pool** (`puro` / `hibrido`). Where this document
and a record disagree, the record wins. Nothing here was measured for it: the
write-up adds no step, which is the whole argument for doing it before adding
one.

**The three documents that precede it were read first**, as `CLAUDE.md` and §4
rule C of [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) require:
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md),
[`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) with its four errata, and
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md). The second of them is where this
experiment was proposed, and §1 below is what became of its bet.

---

## 0. The result, in one page

> **The proposer answers the pairwise question well, and the answer contains
> almost no priority.**

Both halves are measured, on two bases and at three budgets, and the mechanism
joining them is measured too.

**It works at the pair level.** On the hidden policy's 170 labelled pairs it
answers correctly **0.8824** of the time; on the learned base it points at the
better rule **0.7312** of the time at 1,600 pairs — fifteen standard errors above
a coin ([`results2/FINDINGS2.md`](results2/FINDINGS2.md) Stage C,
[`results3/FINDINGS3.md`](results3/FINDINGS3.md) §11).

**It is lost at the order level.** Compiled into an order and run on the machine
that consumes declared edges, those same answers score **0.4804** — `hibrido`
pool, corpus test split 0 — which is **0.40 deviations** above a coin on the same
edges, and level with a free ranking of the eight queues that reads no rule at all
(§11 of the same record).

**The two are one claim, not two, because the mechanism is measured.** The
proposer's competence *is* that queue ranking: it follows one on **0.8073** of the
1,479 pairs it answered, 23.6 deviations above chance. It is near-excellent
(**0.8647**) exactly on the pairs a free ranking already answers and near-chance
(**0.6391**) exactly on the pairs that carry the information a ranking does not
have — and on that second side, where **all** the available order lives, the order
it produces is **0.58 deviations below a coin** (§11 `B-d`, §12, §15).

**Four things that could have been blamed instead, and were each ruled out by a
free measurement:** the budget (§10, §14), the compilation (§13), the selection of
which edges to keep (§14), and the instrument (§11 `B-a` — the direction rate is
the same at 400 and at 1,600).

**What it cost to find out:** 1,770 API calls across three runs. Every one of the
ten sections that interpret them cost zero.

---

## 1. Where the bet came from, and how it was hedged

The experiment was not designed after the fact to explain a failure. It was
proposed on 2026-08-11 in [`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §2.2, as the answer
to a specific dead end: rung 2 had built an engine that executes declared priority
perfectly and never received any priority to execute — **2 conflicts and 0 accepted
edges in eight runs** ([`results2/FINDINGS2.md`](results2/FINDINGS2.md)). The
proposal was to stop asking the model to *write* overlapping rules and start asking
it to *judge* pairs.

**That document then argued against its own proposal, twice, before anything ran.**
Its erratum of 2026-08-12 records that the evidence cited for it was the favourable
half: prompt v2 had handed the model the overlap arithmetic already resolved and
*"with the right information in front of it, it makes the same mistake"*; and the
only two times a real conflict reached the proposer it produced zero edges once and
failed the parse the other — **0 of 2**. Its closing erratum downgrades the bet
explicitly: *"Bet with a low prior, not conclusion."*

**A second correction reshaped what the bet could even be scored against.** The
erratum of 2026-08-17 caught the scoreboard reading the wrong pool: declared edges
are consumed by the **hybrid** engine, so scoring them against `0.8530` — a
**pure**-pool figure with subsumption switched off — inflates the bar by about
0.08. The floor for the right pool did not exist at all and had to be measured
first. That is why the thread opens with a stage that measures nothing new about
the model (§6 of [`results3/FINDINGS3.md`](results3/FINDINGS3.md)).

So the thread began with a hedged bet, a corrected scoreboard and a floor that had
to be built. **What follows is what the bet returned.**

---

## 2. What was asked, three times

| stage | base | population | calls | record |
|---|---|---|---|---|
| **C** | the hidden policy, 29 rules | 170 pairs with a clean witness, out of the 199 declared edges | 170 | [`FINDINGS2.md`](results2/FINDINGS2.md) Stage C |
| **D** | the learned base, 577 rules | 400 pairs sampled at seed 17 from the 31,850 that could carry an edge | 400 | [`FINDINGS2.md`](results2/FINDINGS2.md) Stage D |
| **B** | the same base | 1,600 pairs — Stage D's 400 plus 1,200 more, **nested** | 1,200 | [`FINDINGS3.md`](results3/FINDINGS3.md) §11 |

The model is `deepseek/deepseek-v4-flash` at temperature 0, sequential, in all
three. The question is always the same shape: a ticket, two rules that both match
it, and *which queue does this go to?*

**Stage C is the one with an answer key.** The hidden policy's layer order says who
wins, and a witness ticket is drawn from `ext(A) ∩ ext(B)` — the region where the
two rules actually compete. On the learned base there is no such key and none is
invented: `PLAN_PAIRWISE.md` §10 says so before the calls, and Stage D reports what
the edges *do*, never a correct-edge rate.

**A third object appears later and is not a label.** §9 defines a different truth
for a pair — over the cases the two rules share, whose action is the true one more
often — computable offline from the frozen policy. It is not the layer order and it
is never called one. It is what makes a *direction* rate measurable on a base whose
priority nobody ever wrote.

**The population is a constant fraction of the quadratic.** Of the 166,176 pairs of
577 rules, 112,556 have disjoint extensions, 8,599 are already ordered by
subsumption and 13,171 agree on the action; **31,850 remain — 19.2%**
([`FINDINGS2.md`](results2/FINDINGS2.md) Stage D). Stage D's 400 is 1.3% of that
and the 1,600 is 4.6%. Those two percentages do more work in this write-up than any
other pair of numbers.

---

## 3. The two levels, and why they are one claim

### It works at the pair level

```
Stage C · hidden policy · 170 labelled pairs
  correct                                    0.8824   (150/170, `neither` a failure)
  a coin between the two rules shown         0.5000
  proposal_action_accuracy, rung 1's mocks   0.3877
```

**`P-c` holds**, signed at `> 0.60` before the run. Position bias is exactly zero:
the winner was shown first in 85 pairs and second in 85, and the rate is 0.8824
both ways. Four parse failures in 170, no answer outside the eight queues.
([`FINDINGS2.md`](results2/FINDINGS2.md) Stage C.)

On the learned base there is no key, so what is measured is the **direction** rate:
of the declared edges on pairs where one rule is strictly better over the region
the two share, how many point at it.

```
                    n      rate      vs a coin      surface
Stage D   400      278    0.6978      +6.60 sd      space definition
Stage B  1600     1105    0.7312     +15.37 sd      space definition
Stage B  1600     1093    0.6715           —        corpus definition
```

**`B-a` holds**: `|0.7312 − 0.6978| = 0.0334`, inside the signed 0.05. Quadrupling
the sample moved the rate by two standard errors. **Whatever goes wrong later, it
is not that the instrument moved.**
([`FINDINGS3.md`](results3/FINDINGS3.md) §9, §11.)

### It is lost at the order level

Every row below is `hibrido` pool, corpus test split 0 — the cell `P-d` and `B-b`
were signed on. `hibrido` is subsumption as a non-overridable base level with an
order on top; `puro` is first-match-wins with subsumption off. **They are different
machines and their figures never chain.**

```
  born_at floor — a budget of zero                        0.4332
  Stage D · 344 edges from 400 calls                      0.4080     BELOW the floor
  P-d's threshold (floor + 0.03)                          0.4632
  a free ranking of the eight queues, as a lookup         0.4824
  Stage B · 1,310 edges installed of 1,479, from 1,600    0.4804
  the oracle's own directions on those same 1,600 pairs   0.5246
  the searched order, best of 65 starts, uses the oracle  0.7678
```

**`P-d` is refuted** — the edges did not fail to add enough, they made the order
worse than doing nothing. **`B-b` is refuted by 0.0020**, where a coin on the same
edges has sd 0.0319: after 1,200 calls the compiled order and a free ranking of
eight queues are **the same number**. **`B-c` is refuted** by −0.74 of the
projection's own deviations, which §8 of its plan had asked to be distinguished
from a three-deviation miss.
([`FINDINGS3.md`](results3/FINDINGS3.md) §8, §11; floor owned by §6, ranking by
§7.)

### Why this is one claim and not two

A rate **15 deviations** above a coin produces an order **0.40 deviations** above
one. The two facts sit at different levels of the same pipeline, and stating either
alone misleads: *"the model is good at pairwise priority"* is true and worthless;
*"pairwise judgement does not work"* is false about the answers and true about the
product. What joins them is §4 and §5.

---

## 4. The baseline that makes the order level readable

**A fixed total order over the eight queues, reading no rule, no ticket and no
condition.** It induces an order over the rules — sort each rule by the rank of its
action — and it costs nothing.

It was not an afterthought. It appeared in Stage C as an embarrassment:

```
Stage C · the same 170 labelled pairs
  the best of all 40,320 queue orders     0.9471   (161/170)
  the model, shown both rules             0.8824   (150/170)
  those 40,320 orders: mean 0.5000, sd 0.1346
```

**That 0.9471 is a world record and must be read as one** — chosen by brute force
with the answer key in hand, the same kind of object as the best of 65 search
starts. What it legitimately bounds is the thing worth knowing: **at most 9 of the
170 pairs require reading the rules at all.** On those nine — the queue-pairs that
appear with *both* winners, so no ranking can serve both directions — the model is
at **5 of 9**. A coin.
([`FINDINGS2.md`](results2/FINDINGS2.md) Stage C.)

Because Stage C said that, the same control was built for the learned base
**before** Stage D spent anything: all 40,320 hierarchies scored on the pool where
declared edges live.

```
hibrido                     floor   P-d threshold   queue ranking   best/40320    mean
  full corpus              0.4285         0.4585          0.4805       0.5240   0.3676
  corpus test, split 0     0.4332         0.4632          0.4824       0.5266   0.3670
  corpus test, 5 splits    0.4315         0.4615          0.4806       0.5250   0.3658
  space                    0.4257         0.4557          0.5838       0.5997   0.3180
```

`best/40320` is again a maximum taken with the labels in hand; a hierarchy picked
blind is worth **0.3670**, *below* the arrival floor. Knowing which ranking to use
is the whole content of the baseline, and Stage C is where that knowledge came
from.

**It clears `P-d`'s band on all four surfaces, at zero calls** — and §7 says so
before the calls were made, adding that this *takes away the band's power to
discriminate* rather than refuting it. The band stayed as signed, because moving it
after seeing a baseline would be hard rule 6 wearing a different hat.

**And the ranking is strong exactly on the machine being measured, not in general.**
On the `puro` pool over the corpus it scores 0.4291 against arrival order's 0.5216 —
*worse* than doing nothing, and even the best of the 40,320 does not reach the
floor. Once subsumption has pruned the pool, most of what is left to decide is
*which action*, and a ranking of actions is precisely the instrument for that.
([`FINDINGS3.md`](results3/FINDINGS3.md) §7.)

---

## 5. The mechanism — where the order lives, and where the errors fall

### `B-d`: the errors concentrate exactly where they cost most

Split the 1,600 pairs by whether a fixed queue ranking *could* answer them at all. A
pair it cannot answer is one whose queue-pair appears with both better-rules. The
split is a property of the oracle and the sample, **fixed and gated before a single
call was made**.

```
surface   side           n     direction rate
space     reachable     451        0.8647
space     unreachable   654        0.6391      difference −0.2256
corpus    reachable     293        0.9181
corpus    unreachable   800        0.5813      difference −0.3368
```

**`B-d` holds.** The proposer is near-excellent precisely where a free lookup table
already gets the answer, and drops toward chance precisely where the information a
ranking does not have would have to come from.
([`FINDINGS3.md`](results3/FINDINGS3.md) §11.)

### And the rate on the informative side is worth nothing at the order level

`B-d` measures a *rate* per side. A rate is not a score, so each side was compiled
independently through a fresh engine and read against a coin on **its own rows** —
sizes differ, and a subset with more edges scores higher for having more edges.

```
side           rows  edges    model     coin      sd     devs   oracle  o devs
reachable       451    421   0.4392   0.4288  0.0195   +0.53   0.4442   +0.79
unreachable     654    600   0.4251   0.4423  0.0296   −0.58   0.5407   +3.33
no_side         374    345   0.4553   0.4495  0.0282   +0.20   0.4332   −0.58
all            1479   1310   0.4804   0.4692  0.0266   +0.42   0.5357   +2.49
```

Two things, and they finish the argument:

1. **Every bit of available order lives on the side a ranking cannot answer.** A
   perfect chooser scores **+3.33 deviations** there and **+0.79** on the reachable
   side, where its headroom over the proposer is **0.0050** — five ten-thousandths.
   `B-b` could not have been won on the reachable side however good the proposer was
   on it.
2. **On the side that matters the proposer is indistinguishable from random**
   (−0.58 deviations; the honest phrase is *no better than a coin*, not *worse than
   one*), with headroom **0.1156** — twenty-three times the other side's.

So getting 64% of the informative directions right buys no more order than getting
them at random, **because a ranking-shaped error is not a random error**: when the
proposer is wrong on a pair a ranking cannot answer, it is wrong in the direction
the ranking would have chosen, and correlated errors of that kind cancel the correct
answers instead of adding to them.
([`FINDINGS3.md`](results3/FINDINGS3.md) §12, POST-RUN.)

### The competence, named directly

§15 asked what the proposer is actually doing, with four hypotheses declared before
the measurement.

```
follows a fixed queue ranking   0.8073   +23.64 deviations
names the broader rule          0.6038    +7.98
names `rule_b`                  0.5281    +2.16
names the rule shown first      0.5416    +3.20
```

A marginal cannot separate *"it prefers broad rules"* from *"it follows a ranking"*,
because the two coincide on 922 of the 1,479 pairs. **The 557 pairs where they point
in opposite directions decide it**: there it follows the ranking 0.7702 of the time
and names the broader rule 0.2298. Breadth is not a preference of its own; it rides
on the ranking.

The `rule_b` asymmetry that had been open since Stage D — 203/162, surviving
quadrupling at 781/698 — **was never an effect**: the ranking favours the later-born
rule on 0.5260 of these pairs, and a ranking-follower at 0.8073 predicts naming `b`
at 0.5160 against an observed 0.5281, a residual of +0.93 standard errors.
([`FINDINGS3.md`](results3/FINDINGS3.md) §15, POST-RUN.)

---

## 6. Four things that could have been blamed, and were not

Each was ruled out by a free measurement rather than by argument.

**The budget — ruled out as the explanation, not as a variable.** §10 computes the
channel's ceiling as a function of budget offline, because the oracle's direction is
computable for all 31,850 pairs. It shows the channel *does* pay with more edges,
that `P-d` would have held at 800, and that **at 400 a perfect chooser, a 70%
chooser and a coin are the same number** — 0.4533, 0.4471 and 0.4556 against a coin
deviation of 0.0239. Stage D landed on the flat part of the curve. But the budget
does not explain the 1,600: there the proposer was measured rather than projected,
and it tied a free lookup table. **Where budget does bite is somewhere else** — it
narrows what `B-b`'s refutation means rather than excusing the proposer, and that
is the last item in this section.

**The compilation — ruled out, and it had been protecting the score.** The
cycle-refusing topological sort silently discarded 169 of 1,479 declared edges, by
arrival accident. §13 replaces it with a minimum feedback arc set, which keeps every
edge and minimises violations — a strictly better compilation at its own stated job,
in all three arms.

```
arm        edges   violations topo -> mfas    topo     mfas      gain
model       1479          129 -> 66         0.4804   0.4332   −0.0472
oracle      1105           24 ->  5         0.5357   0.5457   +0.0100
coin        1479          376 -> 201        0.4985   0.4362   −0.0623
born_at floor                               0.4332
```

**The mechanism works when the input carries signal** — the oracle gains from
honouring 19 more of its own edges. **The model behaves like the coin**: honoured
faithfully, its edges are *worse* than not honouring them, and its MFAS order lands
on the `born_at` floor to the digit while differing from arrival order in 576 of 577
positions. The instrument was gated first: an earlier version lost to the baseline
at the baseline's own objective and the run now blocks unless `mfas ≤ topological`.
([`FINDINGS3.md`](results3/FINDINGS3.md) §13, POST-RUN with a written expectation.)

**The selection of what to compile — ruled out.** If accidental dropping helped,
deliberate dropping might help more. Every filter is read against a random drop of
the same size, because *"drop edges until the score improves"* is hard rule 6 with a
hat on. Every filter lands within **0.7 deviations** of its own control, in both
compilations. Nothing there is a selection effect.

**The instrument — ruled out by `B-a`**, above: the direction rate is the same at
400 and at 1,600.

**What §14 also found, which narrows a signed row without moving it.** A **perfect
follower of that same queue ranking**, answering all 1,479 pairs, compiles to
**0.4402** — while the same ranking applied as a **lookup over all 577 rules**
scores 0.4824. **1,479 pairs is 4.6% of the 31,850 that could carry an edge**: a
lookup orders every rule, the same ranking as sparse edges orders 4.6% of the pairs
and leaves the rest at arrival order. They are not the same object.

> So `B-b`'s 0.4824 **was not reachable through this channel at 1,600 pairs by any
> ranking-following strategy, perfect play included** — and the proposer's 0.4804 is
> in fact *above* the perfect follower's 0.4402. `B-b` is refuted exactly as signed
> and the verdict stands; what it *means* is narrower than it reads. It was read as
> *the proposer failed to beat a free baseline*; it is at least as much *the channel
> cannot express that baseline at this budget*.

([`FINDINGS3.md`](results3/FINDINGS3.md) §14, POST-RUN with a written expectation.)

---

## 7. What the engine does with the edges

The order-level scores above treat the edges as a permutation. The other reading is
to install them in the engine that consumes them and run it.

```
hibrido · corpus test, 995 cases       344 edges     1,310 edges
                                     (budget 400)  (budget 1,600)
  e2e                                     0.0673         0.1819
  CONFLICT rate                           0.8894         0.7236
  IMPASSE rate                            0.0000         0.0000
  silent error, over cases it commits     0.3909         0.3418
  cases it commits to                        110            275
```

**With 344 edges installed the engine abstains on 89% of the corpus.** That is not a
failure of the edges' quality — it is the authorship cost showing its true size.
Rung 2 reaches e2e 1.0000 with 199 edges over **29** rules; here 400 calls buy 1.1%
of the pairs that need one, over **577**. The conflict rate is the honest reading:
the mechanism abstains, which is what it should do when nobody has told it who wins.
More edges resolve more cases — CONFLICT falls 0.17 and e2e nearly triples — and the
newly resolved cases are wrong about a third of the time.
([`FINDINGS3.md`](results3/FINDINGS3.md) §8, §11.)

---

## 8. The seven signed rows

All seven were signed by Sergi in their own commit, before the figures existed; the
`B` rows before a single one of the 1,200 calls was made, with the gate in
`rung2/pair_judgement.py` refusing to run otherwise.

| row | claim, in short | band | measured | verdict |
|---|---|---|---|---|
| `P-c` | the pairwise rate on labelled pairs beats a coin | `> 0.60` | 0.8824 | **holds** |
| `P-d` | the declared order beats the `hibrido` floor by 0.03 | `> 0.4632` | 0.4080 | **refuted** |
| `P-e` | that order is inside the behavioural cloud of the 65 | `≤ 25%` distance | 45.0% | **refuted** |
| `B-a` | the direction rate is stable between budgets | `\|Δ\| ≤ 0.05` | 0.0334 | **holds** |
| `B-b` | the order beats a free queue ranking | `> 0.4824` | 0.4804 | **refuted** |
| `B-c` | it reaches the projection from its own accuracy | `≥ 0.4981` | 0.4804 | **refuted** |
| `B-d` | its errors concentrate where a ranking is silent | unreachable `<` reachable | 0.6391 vs 0.8647 | **holds** |

**Three hold, four refuted.** The drafter's own expectation, recorded before the
`B` calls, was three of four right — it expected `B-b` to hold.

Two of these deserve their caveat carried beside them rather than only in the
record. **`B-b` is refuted by 0.0020** against a coin sd of 0.0319, and §14 narrows
what that means (§6 above). **`P-d` was refuted at the one budget in its range where
nothing could have been distinguished from anything** (§10). Neither caveat moves a
verdict, and neither was allowed to: a band is not edited after its figure exists.

**Not signed rows, and not on any scoreboard:** §§9, 10, 12, 13, 14 and 15 are
POST-RUN. They carry expectations where they had them and declare `provenance` in
their records. A measurement that could not have surprised its author is worth less
than one that could, and the difference is recorded rather than assumed.

---

## 9. What this says beyond this repository

**1. Elicitation quality and product quality are different variables, and the gap
between them is measurable.** A 0.73 pairwise accuracy that compiles to an order
0.40 deviations above a coin is not a contradiction; it is what happens when the
accurate part of a signal is redundant with something free and the errors fall on
the informative part. **Any protocol that scores an LLM on the questions it answers,
rather than on the artefact its answers build, can miss this entirely.**

**2. A baseline that reads none of the input is the control that makes the rest
readable.** The queue ranking costs nothing, was available before any call, and it
is what turns *"0.8824 correct"* into *"at most 9 of 170 pairs require reading the
rules"*. Without it, every figure in this thread has a flattering reading.

**3. Correlated errors do not behave like noisy ones.** §10's projection assumed
errors flipped independently at a uniform rate and overshot by 0.0177; `B-d` is the
direct measurement of that assumption, and it is false. Errors that concentrate on
the informative pairs buy less order than the same number of errors spread evenly.

**4. There is one bias here that is a property of the elicitation and not of this
domain.** The proposer applies its own ranking **0.8534** of the time when the
favoured rule is shown first and **0.7623** when it is shown second — nine points,
+3.50 deviations. It is an accuracy effect and not a taste, presentation order was
balanced exactly by construction, and it would show up in any pairwise elicitation
protocol. Why the second slot costs nine points is unexplained here and is the
sharpest thing the thread leaves open.
([`FINDINGS3.md`](results3/FINDINGS3.md) §15.)

**5. Negative results survive better when the apparatus is gated.** Three of the
readings above were only trustworthy because an instrument was validated before it
was believed: the six-row reproduction gate of the floor (§6), the `mfas ≤
topological` gate that caught this thread's own search losing to its baseline (§13),
and the split fixed and gated before the calls (`B-d`).

---

## 10. Limits

**One base, one model, one prompt.** All of it is `deepseek-v4-flash` at
temperature 0 over the 577 rules rung 1 produced under specificity-based
arbitration. A base born under another arbitration would be different material, and
`results/FINDINGS.md` already warns that measurements over this one are bounds, not
simulations of the loop.

**The material problem is untouched and it is large.** Of the 1,600 pairs, **282**
have no right winner among the two rules shown under the space definition and
**409** under the corpus one — between a sixth and a quarter. For `T3_ENGINEERING`
and `ACCOUNT_MANAGER` no correct rule exists at all. **No edge, no order and no
budget recovers a case whose true action is a third queue.**

**The channel has a ceiling and it is below what search reaches.** An exhausted
pairwise channel with a *perfect* chooser reaches **0.6834** on the cell above,
where the searched order reaches **0.7678** — and that searched order uses the
oracle, and is the best of 65 starts, which
[`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) establishes is a
winning ticket rather than a level: the 65 end orders are 65 distinct behavioural
machines. The pairwise channel is not an alternative route to what search finds.

**One rejection verdict has still never been seen working.** `EDGE_CONTRADICTS` has
not fired in any real run, and this protocol cannot make it: the population filters
subsumption-comparable pairs out precisely so no call is wasted on one. The caveat
`PLAN_PAIRWISE.md` §5.3 records stands untouched.

**The 1,200 calls are not reproducible.** The proposer is not deterministic at
temperature 0, and `harness/record_guard.py` guards those records for that reason.
Everything derived from them is free and reproducible to the digit.

---

## 11. Surfaces and pools — how to read any number above

**Two surfaces.** The **corpus** is the modelled arrival distribution, deliberately
long-tailed; the **exhaustive space** is the uniform measure over all 134,400
combinations. They answer different questions and neither is *the* bound — over the
same 2,080 pairs they correlate at a Spearman of 0.34, so the space cannot rank two
orders for deployment any more than it can rate them
([`STATUS.md`](STATUS.md), *Before reading any figure*).

**Two pools, and they are the load-bearing label of this thread.** `puro` is
first-match-wins with subsumption off; `hibrido` is subsumption as a
non-overridable base level with an order on top. They are different machines. The
same reversal of arrival order gains **+0.2520** on `puro` over the space and
**+0.0116** on `hibrido`; the `hibrido` floor is *below* the `puro` one on the three
corpus surfaces and *above* it over the space. Scoring a hybrid result against a
pure figure inflates the bar by about 0.08, which is the error
[`CHAT_SUMMARY.md`](CHAT_SUMMARY.md)'s erratum of 2026-08-17 caught in its own
scoreboard.

**Everything scored as an order in this document is `hibrido` / corpus test split
0** unless the line says otherwise — the cell `P-d` and `B-b` were signed on. The
pair-level rates name their surface on each line, because the space and corpus
definitions of *better rule* disagree: 0.7312 against 0.6715 at 1,600.

**Where each figure lives**

| what | record that owns it |
|---|---|
| the labelled pair benchmark, Stage C, Stage D | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |
| the floor by pool, the queue-ranking baseline | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §§6–7 |
| `P-d`, `P-e`, the direction control, the budget curve | same record, §§8–10 |
| `B-a`–`B-d`, the 1,600-pair run | same record, §11 |
| the side decomposition, MFAS, dropping, the asymmetry | same record, §§12–15 |
| the surfaces, the pools, the signed-row scoreboard | [`STATUS.md`](STATUS.md) |

Every command that reproduces the free half is in
[`README.md`](README.md), *Reproducing the four rungs*, and in
[`CLAUDE.md`](CLAUDE.md). Nothing in this document needs to be re-run to be
checked against its source: every figure is in one of the records the table above
names, under the section named beside it.
