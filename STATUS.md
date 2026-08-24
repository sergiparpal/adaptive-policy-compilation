# Status

What is known, as of August 24, 2026. **Not a history** — that is the four
`FINDINGS` records, [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md)
and [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), each with its
dated errata in place. Every figure here already exists in one of them.

**The project.** A cheap symbolic engine resolves the cases it covers; on one it
does not cover (an *impasse*), an LLM acts and writes a rule so that next time it
does. Ticket triage: 8 attributes, 8 queues, a hidden policy of 29 rules in 8
priority layers. Four rungs closed, plus an audit of the instrument behind two of
them.

**In one sentence.** The priority of a stratified policy is not in the shape of
its rules; of the three ways of supplying it — infer it from the syntax, have the
proposer declare it, learn it from observed behaviour — the first is falsified,
the second was never exercised, and the third recovers 61% of what full
supervision buys.

---

## Before reading any figure

**Every figure names a surface, and the two are not interchangeable.** The
**corpus** is the modelled arrival distribution, deliberately long-tailed
(`has_security_keyword`: 3% of arrivals against 50% of the attribute space). The
**exhaustive space** is the uniform measure over all 134,400 combinations. The
corpus answers *what would this achieve in deployment* and cannot certify an
optimum — its 2000 draws touch 1743 distinct cases and leave the rest
unconstrained, so an order can be perfect on it and be 0.9455 as a function. The
space answers *is this order the policy*, and weights regions the system will
almost never see. Neither is *the* bound. Rungs 1 to 4 published corpus figures
without saying so; everything below is labelled.

**The sharpest instance measured, 2026-08-15**: two end orders of the same search
disagree on 20.35% of the space and 5.75% of the corpus, and the class carrying
most of that disagreement is not the same class on the two surfaces — 57.5% of it
against 4.6%. Per-class rates do not transfer either, so a figure on one surface
cannot be reweighted into a figure on the other. **Nor does the ordering**: over
the same 2,080 pairs the two surfaces correlate at a Spearman of 0.34, so the
space cannot rank two orders for deployment any more than it can rate them
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), parts two and
three). Name the surface.

**Every finding came from a check costing cents or nothing**, never from the
expensive run. Three failures were caught by a blocking free check, each of which
changed a conclusion:

- **Aug 5** · `harness.ceiling_check`: the engine scores 0.5875 with the
  *perfect* policy loaded. It voided an n=2000 run already paid for
  ([`PREDICTION.md`](PREDICTION.md)).
- **Aug 8** · `rung3.optimizer_check`: the neighbourhood the audit had
  declared, pairwise swaps, cannot solve the 29-rule instance whose optimum is
  1.0000 — 0 of 65 starts reach it.
- **Aug 8** · the same check, on the other surface: the corpus would have
  certified that instrument anyway — orders perfect on its 2000 cases score
  0.9455 and 0.9299 as functions
  ([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 0).

Money bought only rung 1's 577 rules and rung 2's eight runs. Rungs 3 and 4 and
the audit cost zero API calls.

---

## The signed rows, and how they came out

**Twenty-seven rows have been signed before the figures they name existed. This
is their scoreboard**, and it is a fact about the drafter rather than about the
material. It exists because the standing calibration note in
[`IDEAS.md`](IDEAS.md) is *directional* — it tells whoever writes the next entry
which way their bands usually err — and a note like that is worth nothing without
a count behind it.

**The convention, stated before the count so that the count can be checked.**

1. **The `Q` rows count.** They live in §0 of `PLAN_ORDER_METRICS.md` instead of
   `IDEAS.md`, and the regime is the same: drafted by Claude on 2026-08-14 and
   signed by Sergi the same day — *I adopt §0 as drafted, without changes* — where
   the signing commit adds only that line and a pointer in §4, so no row of the
   table moved. Same drafter, same shape of band with its own *refuted by* column,
   same "committed before any figure exists".
2. **Rows marked *reported, not adjudicated* are listed apart and are not in the
   denominator.** There was no band to hit or miss, so they are not calibration
   events — but they are signed rows and they are a fact about the drafter, so
   they are counted separately rather than dropped.
3. **One signed row is one event, with the verdict its own record gives it.**
   `S-d` is one refutation and not two, though the record publishes two readings
   of it; `Q-d` is one though only its second half failed. Splitting rows by
   clause would make the denominator depend on drafting style, and hand the next
   drafter an incentive to write fewer clauses to protect the ratio.

| thread | signed | adjudicated | refuted | dead zone | hold | reported |
|---|---|---|---|---|---|---|
| **Q** · the instrument (§0 of `PLAN_ORDER_METRICS.md`) | 6 | 6 | **2** | 0 | 4 | 0 |
| **S** · the corpus surface | 6 | 6 | **4** | 0 | 2 | 0 |
| **R** · rank transfer | 4 | 3 | **1** | 1 | 1 | 1 |
| **C** · the touched points | 4 | 3 | **0** | 1 | 2 | 1 |
| **D** · the rule level | 4 | 3 | **2** | 0 | 1 | 1 |
| **P** · pairwise judgement (§0 of `PLAN_PAIRWISE.md`) | 3 | 3 | **2** | 0 | 1 | 0 |
| **total** | **27** | **24** | **11** | **2** | **11** | **3** |

**Named, so that the table can be recomputed by hand.** Refuted: `Q-d`, `Q-f`,
`S-a`, `S-b`, `S-c`, `S-d`, `R-a`, `D-a`, `D-c`, `P-d`, `P-e`. Hold: `Q-a`,
`Q-b`, `Q-c`, `Q-e`, `S-e`, `S-f`, `R-c`, `C-b`, `C-c`, `D-b`, `P-c`.
Reported: `R-d`, `C-d`, `D-d`.
**Dead zone: `R-b` and `C-a`** — a row landing between its band and its
refutation line, which is a drafting defect and not a result. **`D` has none**,
because after those two the D entry declared every band's edges to be its own
refutation lines.

**Why the per-thread column and not a single ratio.** The calibration note is
about direction, and one ratio destroys it: `S` at 4 of 6 and `C` at 0 of 3 are
not the same drafting behaviour, and the thread that bet on arrivals *differing*
from the space is the one that stopped being refuted.

**The convention chosen is the milder of the two available, and that is declared
here rather than left to be found later.** With the `Q` rows, 11 of 24 = **45.8%**
refuted; without them, 9 of 18 = **50.0%**. `Q` is in because of the common
drafter and the sample size, not because of the figure — and it moves the figure
3.8 points the flattering way, which is exactly why saying so is not optional.

**Where the verdicts are read from.** The `Q` column comes from *the predictions
of §0, one by one* in the first part of
[`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) — its register table
carries `G1`–`G6` instead — and `S`, `R`, `C` and `D` from the registers of parts
two, three, four and five of the same record; and `P` from the Stage C and
Stage D sections of [`results2/FINDINGS2.md`](results2/FINDINGS2.md) and §8 of
[`results3/FINDINGS3.md`](results3/FINDINGS3.md). All three `P` rows are
adjudicated: the thread is closed.

**Excluded, and this is what makes
the arithmetic reproducible:** `G1`–`G6`, which are the plan's checks and carry no
band; and `S-g`, `C-e` and `D-e`, which the records add as *(not predicted)* and
which nobody signed. **And `P-a` and `P-b` of `PLAN_PAIRWISE.md`, which are
neither**: they were measured on 2026-08-24 *before* anyone signed them, so they
are **spent** — not signed and not adjudicable, in no column of the table and not
in the denominator. §0.1 of that plan records them as outcomes and does not
restore them as predictions. `P-c`, `P-d` and `P-e` are a different case: Sergi
signed them on 2026-08-24, before any figure of theirs existed, and they are in
the table above.

**The only earlier mention of a count does not reconcile with any of this.** The
note inside the D entry says *two of the ten rows signed before today* landed in a
dead zone. The numerator is right and the denominator matches nothing: 20 rows
were signed before that entry and 18 of them adjudicated. It sits inside a signed
prediction block, which is not edited — not even to annotate it — so it stands as
written and this line is the reconciliation.

---

## What is established

**Priority is not recoverable from the syntactic shape of the rules.** Three
criteria falsified, perfect policy loaded, no LLM, on the corpus —
[`results/FINDINGS.md`](results/FINDINGS.md):

- *specificity*: e2e **0.5875**, CONFLICT 25.3%. No monotone function of it can
  work — H01 (2 conditions) must beat H03 (1), H16 (1) must beat H24 (2).
- *arrival order*: 100% in design order, 12.8% reversed, **49.3%** random. It
  carries no signal of its own, and in a learned base it runs backwards: defaults
  are born early, exceptions late.
- *subsumption*: silent error **0.0000** over the hand-written policy, **53.12%**
  over the learned base. A proxy for *authored* priority — the 0.0000 measures a
  virtue of the author.

**Execution failure, not representation failure.** Over the exhaustive space the
29 DSL rules are equivalent to their lambdas, and first-match-wins reproduces the
policy exactly.

**The mechanism for executing declared priority works.** Subsumption plus 199
declared edges: e2e **1.0000**, silent error 0.0000, zero conflicts, zero
impasses, on the corpus — [`results2/FINDINGS2.md`](results2/FINDINGS2.md).

**The proposer does not feed it.** Shown the base, the overlap arithmetic
resolved for it and an explicit instruction to overlap, it writes mostly disjoint
rules and argues disjointness as a merit. Showing it the base *reduced* overlap
tenfold (17.5% of pairs → 1.60%); the instruction recovered part of it (7.25%)
and never reached the starting point. Eight runs, ~200 escalations: **2
conflicts, 14 proposed edges, 0 accepted**. `language` appears in 0 of the 8
bases, `channel` and `prior_tickets_30d` in 1 each, though hidden layers built on
them decide 14.5% of the corpus.

**And the population for asking it the other question now exists, with its answer
key.** The 199 declared edges are published pair by pair, each with a witness
ticket drawn from the region where the two rules compete and the queue the hidden
policy sends that ticket to ([`results2/FINDINGS2.md`](results2/FINDINGS2.md),
*the labelled pair benchmark*;
[`pair_benchmark.json`](results2/pair_benchmark.json)). **170 of the 199 carry
such a witness and 29 do not** — in every one of those an earlier layer owns the
whole overlap, so the correct queue for every ticket in it is neither rule's, and
they are counted outside the denominator. That makes the 170 the easier half by
construction, and any rate measured on them an **upper** estimate of what a
proposer would do on all 199. Nothing has been asked of a model: the stage of
[`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) that does costs money and is gated on a
row nobody has signed.

**The material contained the signal; the arbitration destroyed it.** The same 577
rules that specificity turned into 0.1829 admit an order scoring **0.8530 ±
0.0062 on corpus test** — *the best of 65 starts, and not a converged value; see
the caveat below* — (train 0.8695: overfitting of the order is 0.0165),
against a coverage bound of 0.9010 on the corpus and 0.8784 on the space —
[`results3/FINDINGS3.md`](results3/FINDINGS3.md) §1 and its 2026-08-08 erratum,
[`order_search_ls.json`](results3/order_search_ls.json). That bound is an **upper
bound by per-case coverage**, not a demonstrated attainable optimum. The same
order scores 0.6105 on the space, and a search seeing all 134,400 cases reaches
0.7905 ([`order_search_ls_fullspace.json`](results3/order_search_ls_fullspace.json)).
The search uses the oracle: the material contains the signal, which is not the
same as it being reachable without labels.

**The level is robust to the search budget; the order is not.** These are two
different claims and the figure invites fusing them.

*The level.* Quadrupling the multi-start budget moves the best train score by at
most one case in 1005, in 2 of the 5 splits, and in both of those the test score
falls. **The gap from 0.8530 up to the 0.9010 bound does not close by searching
harder** — more budget stops buying generalization before it stops finding train
improvements.

*The order.* In all fifteen rows measured — three budgets × five splits —
**exactly one start reaches the best train score**. In splits 1 to 3 the best did
not change between 65 and 257 starts, and yet the 192 extra draws never found it
again: the peak is a singleton that the sample spreads around rather than
concentrates on.

**So a reader of the number can rely on it, and a reader of the order inherits a
draw.** That distinction is not academic here: rung 4 consumes orders, not
scores.

**And the draw is now measured in cases, not inferred.** The end orders the
multi-start discards were regenerated — parity exact on all 31 published rows —
and compared as functions over the **exhaustive space**, pure pool
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md),
[`order_metrics.json`](results3/order_metrics.json)). Split 0 at full
supervision: the winner at 65 starts and the winner at 257, **one train case
apart**, decide **11,240 of 134,400 cases differently — 8.36%**; split 4, three
train cases apart, **14,430 — 10.74%**. The 65 end orders are **65 distinct
behavioural signatures**, and so are all 257: no two of them are the same
machine. Positional churn says nothing — a median 99.65% of the rules sit at a
different index between any two of them — and **Kendall tau says nothing
either**, over all pairs or restricted to the 35,457 that can change a decision
(|ρ| ≈ 0.13 both ways). What that kills is the cheap shortcut — a rank statistic
standing in for the exact comparison — and not the premise of the instrument,
which is that decisions are what have to be compared: rank failing even when
restricted is evidence for it. Disagreement concentrates on the **most abundant**
class, `SECURITY_INCIDENT` at 1.53× the overall rate, and is *below* average on
the two scarce ones, where most cases have no correct rule to compete over.

**And on the arrival distribution the same draw costs a fifth of that.** The same
orders and the same instrument, measured over the **corpus** — parity exact on
the same 31 rows ([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md),
part two; [`order_metrics_corpus.json`](results3/order_metrics_corpus.json)). The
2,080 pairs of split 0's 65 end orders pool to **5.75% of the 2000 corpus cases**
against 20.35% of the space, and the winner at 65 against the winner at 257
differs on **33 of 2000 cases, 1.65%**, against 11,240 of 134,400. On the corpus
test half alone, 6.45% and 2.21%. **Where the disagreement falls changes
completely**: `SECURITY_INCIDENT` carries 57.5% of it on the space and **4.6%**
on the corpus, where `SELF_SERVICE_DEFLECT` carries 44.8% — although per case of
its own class `SECURITY_INCIDENT` still runs at **4.57×** the overall corpus rate
and `ONCALL_ESCALATION` at 3.32×. Per-class rates do **not** transfer between the
two surfaces (`T2_TECHNICAL` −81.6%, `BILLING_SPECIALIST` +165.2%), so no
reweighting turns one into the other. What does not change: **all 257 end orders
are still 257 distinct machines on the corpus**, the closest pair differing on 2
cases of 2000 — and not for lack of material, since the average arriving case
carries 74% more live conflicting pairs than the average point of the space.

**And the space does not even RANK what it cannot rate.** The same 2,080 pairs,
joined across the two records by `(i, j)` — no search, no regeneration, 0.07 s
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part three;
[`rank_transfer.json`](results3/rank_transfer.json)). Spearman between a pair's
**corpus** disagreement rate and its **space** rate is **0.3364**, and ties cap
it by at most 5×10⁻⁵, so that is not the explanation. Of the 208 pairs closest on
the space, **45 (21.6%)** are among the 208 closest on the corpus. The per-pair
ratio corpus/space is not one factor: **p75/p25 = 1.880**, extremes 0.047 to
1.767, a factor of **37**. And the pair the space calls the most interchangeable
of all 2,080 sits at **rank 1207 of 2080** on the corpus, above its median. So a
reader who used the space record comparatively — *this pair is further apart than
that one* — was reading the wrong surface, and not merely by a constant: the
ordering does not transfer either.

**And the whole of that shift is WHICH points arrive, not how often.** The same
2,080 pairs again, over the **exhaustive space restricted to the 1,743 points
the corpus touches** — 1.30% of it, each point counted once — with the corpus
contributing a mask and nothing else, so every rate stays in `Space`'s
convention ([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part
four; [`order_metrics_touched.json`](results3/order_metrics_touched.json)).
Pooled over those touched points the pairs disagree on **5.68%**, against
**5.75%** of the 2,000 arrivals and **20.35%** of the whole space: the level
transfers to the arrival distribution *before any class weighting is applied*.
Class reweighting rebuilt on the touched rates gives **0.05828** against the
measured 0.057472, **+1.4%** relative, where the same reweighting on the whole
space gave 0.116685, **+103%** — so **98.6%** of that error is which points get
sampled and 1.4% is their multiplicity. `T2_TECHNICAL` carries 98.5% of it: two
orders disagree on **19.69%** of its 36,720 space points and **3.84%** of the
661 the corpus reaches. What this closes is the *why 3.5×* left open by part two
and the *why 0.28 and not 0.57* left open by part three, which were one question
in two units. What it does **not** do is make the space readable as a deployment
surface: the correction is a measurement over a 1.3% sample that only the corpus
can identify, not a per-class factor, so the space record plus the class
frequencies still does not reach 5.75%.

**And it is not the rules that decide which points those are.** The same 2,080
pairs again, over the **exhaustive space, pure pool**, with the touched mask
entering only through a per-rule aggregate
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part five;
[`order_metrics_rules.json`](results3/order_metrics_rules.json)). A rule's
arrival concentration — the share of the touched points its extension holds over
the share of the space it holds — spans **1,344×** across the 577, and the
predictor built from it, the mean over a pair's disagreement set of the two
winning rules' concentration, reaches a Spearman of **0.4962** against the
measured per-pair ratio and leaves **84.5%** of its spread on a log scale
(p75/p25 1.754 → 1.608). Half the ordering, almost none of the spread. What the same run
does find: a disagreement region is **0.36×** as touched as the rules that win
it, at the median — so the effect is inside a rule's extension, not between rules
— and the chain's *last* link is nearly exact, `κ` against the product of its
conditions' own concentrations giving **0.987**, with `has_security_keyword` at
50% of the space and 4.07% of the touched points. Two by-products: only **25 to
53 rules of 577** hold a territory under any of these orders, and the forbidden
per-case predictor — the arrival density of the disagreement set itself —
correlates **1.0000** with the measured ratio, which is why the run's permutation
test is blocking.

**This caveat applies equally to
[`order_search_ls.json`](results3/order_search_ls.json)**, which produced the
0.8530 with the same optimizer at the same budget, and to every rung 4 figure
from `sweep_ls`. It does not withdraw those figures — they are what the declared
instrument returns — but they are bounded by a draw, not by convergence.
`MULTISTART_STARTS` stays at 64 **because it was declared before the runs that
used it**, and for no reason found here: choosing it by reading test or space
figures would be the failure this project studies, whichever way they came out
([`start_budget_check.json`](results3/start_budget_check.json), FINDINGS_AUDIT
Step 3).

**What an order that searches for nothing scores, on both pools.** The `hibrido`
pool — subsumption plus a declared order, the machine where declared edges live —
had a world record and no floor: nothing measured what *walking* scores there. It
does now, over the full corpus, corpus test (split 0 and the five-split mean) and
the space, with both random-order generators reported separately
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §6,
[`floor_by_pool.json`](results3/floor_by_pool.json)). Three things it settles,
each naming its surface and its pool. **The hybrid floor is not the pure one
minus a constant**: it is below it on the three corpus index sets (by 0.083 to
0.088) and above it on the space (by 0.111). **`born_at` is worse than shuffling
is a pure-pool statement** — over the space it scores 0.3148 against 0.3768 and
0.3864 on `puro`, and 0.4257 against 0.3867 and 0.3903 on `hibrido`. FINDINGS3
§1's 2026-08-08 erratum holds on the pool it was measured on and the sign
reverses on the other; none of its figures moves. **And reversing `born_at` —
the label-free heuristic worth +0.2520 over the space — is worth +0.0116 on the
pool that matters for declaration.** The two
reversed figures [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) cited as *left
unconfirmed* reproduce exactly and now have an owning record; its §2 and its
§9.6 carry the dated erratum. This record **carries no prediction**: the two rows
that predicted it were spent before signature (`PLAN_PAIRWISE.md` §0.1).

**The proposer can pick the right queue between two rules, and most of that is a
queue hierarchy.** Asked 170 times which queue a ticket goes to when two rules
that both match it disagree — the answer known by construction from the hidden
policy's layer order — it answered correctly **150 times, 0.8824** over all 170
with `neither` counting as a failure, against floors of 0.3877 and a 0.50 coin
([`results2/FINDINGS2.md`](results2/FINDINGS2.md), Stage C;
[`pair_judgement_hidden.json`](results2/pair_judgement_hidden.json)). Position
bias is zero — 85 pairs each way, 0.8824 both — and 4 of 170 failed to parse.
**That is the signed row `P-c` holding**, at band `> 0.60`.

**But a fixed order over the eight queues, reading no rule at all, scores
0.9471** — 161 of 170, more than the model got while being shown both rules
([`pair_judgement_baselines.json`](results2/pair_judgement_baselines.json)). That
order is chosen by brute force with the key in hand over all 40,320 permutations,
so it is a winning ticket and not a level; what it bounds is that **at most 9 of
the 170 pairs require reading the rules**. Five queue-pairs appear with both
winners, which is what no ranking of queues can serve. **On those nine the model
is at 5 of 9** — a coin. So the change of question works as a format, and it has
not been shown to supply priority where a hierarchy runs out. Both hold at once
and the second is the one that transfers.

**And it is an upper estimate.** The 29 pairs with no clean witness are outside
the denominator by construction and are the ones where the layer order is
invisible on the surface of the two rules; if all of them were wrong the rate
over the 199 declared edges would be **0.7538**. The pull toward the narrower
rule shows up too: the wrong-edge rate doubles, 0.1212 against 0.0597, when the
rule that should win is the broader one.

**And a ranking of the eight queues, at zero calls, already clears the band the
next stage was going to be judged on.** A total order over the actions induces
one over the 577 rules — sort by the rank of the rule's action, reading no
condition, no extension and no subsumption. The ranking Stage C's answer key
produced over the *hidden* policy's pairs, transferred unchanged, scores
**0.4824** on the `hibrido` pool, corpus test split 0, against P-d's threshold of
0.4632; over the space, 0.5838 against 0.4557
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §7,
[`queue_hierarchy_floor.json`](results3/queue_hierarchy_floor.json)). A hierarchy
picked *blind* is worth 0.3670, below the floor — knowing which ranking to use is
the whole content of the baseline, and Stage C is where that knowledge came from.

**It is strong exactly where P-d measures and nowhere else.** On the `puro` pool
over the corpus the same family is *worse* than arrival order, 0.4291 against
0.5216, and even the best of the 40,320 does not reach the floor. Once
subsumption has pruned the pool, most of what is left to decide is *which
action*, and a ranking of actions is the instrument for that.

The band does not move — it is signed — and what the control took away was the
power of a *hold* to mean anything, since a free lookup table sits above it
already. **In the event it is the refutation that needed the control**: P-d
landed below the floor, and the ranking's 0.4824 is what says the gap is 0.074
rather than a rounding error. See the entry below.

**And the edges the proposer actually wrote make the order worse than doing
nothing.** 400 calls over the learned base bought 344 declared edges — 1.3% of
the 31,850 pairs that could carry one — and the order they induce scores
**0.4080** on the `hibrido` pool at corpus test split 0, against a `born_at`
floor of 0.4332 and a P-d threshold of 0.4632
([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §8,
[`declared_order.json`](results3/declared_order.json)). **`P-d` is refuted**, and
not by falling short of the margin: by landing below the floor.

**It is the model's choices and not the compilation, and that was checked.** The
same pairs, the same compilation, only the direction of each edge changed: a coin
lands at **0.4314** (sd 0.0243, 50 draws), on the floor; the model sits 0.96
deviations below it and **inverting every one of its answers** puts it at 0.4432,
above the floor. Each gap is inside one deviation, so each alone is a sign and
not an effect.

**And asked directly, the direction turns out to be right, which is the more
useful answer.** Of the declared edges on pairs where one rule is strictly better
over the region the two share, **194 of 278 point at it — 0.6978, six standard
errors above a coin** ([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §9,
[`edge_direction.json`](results3/edge_direction.json)). The pairwise question
elicits real information. What it does not survive is compilation: with the null
sharpened to 2,000 draws the model's order sits at the 15th percentile of coins,
and **the oracle's own directions on the same 400 pairs reach only 0.4593, still
under P-d's 0.4632 threshold and still inside the coin distribution**. So **P-d
was not refuted because the proposer chose badly — it was refuted because 344
edges cannot move a 577-rule order across a 0.03 margin, whoever picks their
direction.** §8's `signal with the wrong sign` is withdrawn there by a dated
erratum.

**And the budget that would have worked is now known, for zero calls.** The
oracle's direction is computable offline on all 31,850 pairs, so the channel's
ceiling against budget is free ([`results3/FINDINGS3.md`](results3/FINDINGS3.md)
§10, [`edge_budget.json`](results3/edge_budget.json)). All on P-d's own cell:
**at 400 a perfect chooser, a 70% chooser and a coin are the same number** —
0.4533, 0.4471, 0.4556 against a coin deviation of 0.0239. Both cross P-d's
0.4632 threshold at **800** and a free queue ranking at **1,600**. So P-d was
adjudicated at the one budget in the range where nothing could be distinguished
from anything, and **doubling it would have flipped the verdict**.

**Accuracy does not wash out with volume**: exhausted, a perfect chooser reaches
0.6834 and a 70% chooser 0.5652, and that 0.12 does not close. **And the whole
channel tops out below search**: 0.6834 against the searched order's 0.7678 on
the same cell, flat from 12,800 edges on. Handed every pair and the right answer
to each, pairwise declaration still stops 0.084 short of what the optimizer
finds. The oracle and noisy curves are exact and projected respectively; what the
actual proposer scores above 400 is unmeasured and would take calls.

**`P-e` is refuted too, and by a wide margin.** Behavioural distance from 65 end
orders **regenerated on the hybrid pool** — never the published `puro` ones —
comes out at a median **0.4497** of the exhaustive space against a band of ≤0.25.
The declared order is not inside the cloud; it is a different machine from all 65,
whose own members disagree with one another by up to about 20%.

**And the authorship cost is now measured.** With those 344 edges installed the
engine reaches e2e **0.0673** and **abstains on 89%** of corpus test: 885
CONFLICTs in 995 cases, silent error 0.3909 over the 110 it commits to. Rung 2's
hidden policy needs 199 edges for 29 rules and reaches 1.0000; a 577-rule learned
base is not in that neighbourhood. The mechanism is doing what it should — nobody
told it who wins, so it abstains — which is why the conflict rate is the honest
reading and the e2e is not.

**An ordering problem and a material problem are different things.** Six classes
of eight — 1774 of 2000 cases — are pure ordering. `SECURITY_INCIDENT` (20 cases)
and `ONCALL_ESCALATION` (7) are **100% recoverable** and rung 1 gave **0/17** and
**0/7**. But 66.7% of `T3_ENGINEERING` and 64.2% of `ACCOUNT_MANAGER` have no
correct rule covering them at all; no order saves those. Corpus; FINDINGS3 §2.
Which classes get sacrificed is a choice of objective function, and rung 1's
arbitration was making it undeclared (§3).

**Priority is partly learnable from the feedback a real system gives.** Symmetric
supervision beats born_at by **+0.3273**; asymmetry 0 — feedback only on errors,
the only kind a deployed system produces — by **+0.2011**, 61% of it, on corpus
test ([`results4/FINDINGS4.md`](results4/FINDINGS4.md) §1 erratum,
[`sweep_ls.json`](results4/sweep_ls.json)). On the space the same orders give
0.6157 and 0.5757 against the 0.8784 bound: same direction, larger shortfall. The
learner never sees the truth by any route (the record's wording, "the only module
that imports `true_action`", was corrected — `sweep.py` carries an unused
import).

**Cheap supervision is nearly free, and less free than published.** Under the
audited optimizer the label-budget curve reads 0.8530 / 0.8227 / 0.7771 / 0.7410
/ 0.5767 on **corpus test** for 1005 / 251 / 100 / 50 / 10 labels, pure pool.
The headline ratio 5%/100% falls from 0.9147 to **0.8687**: 50 labels still buy
87% of full supervision, on a full supervision that is now worth more
([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 3;
[`budget_and_balance_ls.json`](results3/budget_and_balance_ls.json)). On the
**exhaustive space** the same orders give 0.6105 down to 0.3310, and low budgets
transfer proportionally worse.

**Caveat on the low-budget rows, added August 15, 2026.** Step 3 reads them as
*the tie-break regularises*: the objective saturates, most starts tie, ties go to
index 0, so the search returns a sane default. Measured as orders, that reading
is too kind. At 10 labels (split 0, draw 0) the **40 orders tying at the best
train score are 40 distinct machines**, disagreeing with one another on a median
**39.2% of the exhaustive space**. The search is not declining to act; it is
choosing arbitrarily among very different answers and landing on a sane default
by accident of the start order. The figures stand — they are what the declared
instrument returns — but anyone who changes the tie-break or the order of the
declared starts changes which of the 40 ships
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md)). **This one
survives the change of surface**: on the corpus those 40 machines still disagree
a median **24.05%** of the 2000 cases, 24.32% of corpus test, against 39.2% of
the space — a fall of 1.6× where full supervision falls by 3.5×.

**Protecting the rare classes costs a quarter of what it looked like.** Balancing
the objective costs the greedy 0.0563 in e2e and buys +0.1735 in balanced
accuracy; under the local search it costs +0.0274 and buys **+0.0576**, corpus
test. Most of what read as objective conflict was search weakness: with no
balancing at all, the local search recovers 19 of 21 attainable ACCOUNT_MANAGER
cases where the greedy recovered 0. On the exhaustive space, macro-recall says
balancing buys the greedy +0.1093 and the local search +0.0201. FINDINGS_AUDIT,
Step 3.

**The signal runs out as the system improves.** Under asymmetric feedback the
volume of labels is proportional to the error rate of the system observed, so
observing a worse π₀ produces a better order. A property of the channel, not of
the learner — the one section of rung 4 the audit left standing (FINDINGS4 §3).

---

## What was withdrawn, and why

The part a reader cannot reconstruct without reading everything in order.

1. **Rung 3's searched order: 0.7713 → 0.8530** (corpus test). The greedy was
   myopic; a multi-start local search recovered 63% of the gap to the bound.
   Cause: the optimizer audit, validated first against a policy whose optimum is
   1.0000 by construction. FINDINGS3 §4 erratum.
2. **Rung 3's 0.9010 stopped being a "ceiling"** and became an upper bound by
   per-case coverage — no order is known to attain it. Cause: re-reading what
   `ceiling()` computes, not a new measurement. FINDINGS3 §1 erratum.
3. **Rung 3's rehabilitation of arrival order was withdrawn.** "born_at already
   scores 0.52" is a corpus artifact: on the space it is *worse* than shuffling,
   0.3148 against 0.3768. Cause: naming the surface for the first time. FINDINGS3
   §1 erratum of 2026-08-08.
4. **Rung 4's "change of regime" in asymmetry was withdrawn**: +0.067 became
   **+0.2011**, the cliff between asymmetry 0.25 and 0.1 vanished, the
   symmetric-to-asymmetric ratio fell from 3.5x to 1.6x. What read as a property
   of the channel was the shape of a weak learner's failure curve. Cause: the same
   optimizer. FINDINGS4 §1 and §5 errata.
5. **Rung 4's "more noise gives better results" is gone.** Falsifying 10% of the
   labels bought +0.060 and now buys +0.0013, inside its spread; the sweep is a
   monotone degradation curve. Cause: the noise was supplying the restarts the
   search lacked. The record diagnosed that mechanism correctly and refused to
   change the method, which is what later made the fix legitimate. FINDINGS4 §4
   erratum.
6. **Rung 3's "at 1% it collapses to 0.5251, the arrival order without searching
   for anything" was withdrawn.** The same greedy, correctly tie-broken, gives
   **0.5732** at 10 labels: that collapse was substantially an artifact of the
   pre-2026-08-06 tie-break, not of the label budget. Measured by running the
   published greedy and the local search side by side against the untouched
   record, which also showed the tie-break to be worth between −0.0166 and
   +0.0481 depending on the fraction — it changes sign twice across the curve.
   Corpus test. FINDINGS3 §4 erratum of 2026-08-13.
7. **Rung 4's anchor cell was not "completely deterministic."** It spreads 0.0111
   across `PYTHONHASHSEED`, and the null test that had ruled tie-break
   instability out permuted a list the argmax never iterated — a true 0.0000 that
   measured nothing. Cause: the tie-break ran over a `set`. Fixed 2026-08-06,
   worth +0.0002, which is what later separated tie-break from algorithm.
   FINDINGS4 §1 and §4 errata.

---

## What is open

Not all of [`IDEAS.md`](IDEAS.md) — the ones that would change a conclusion.

1. **Whether the residue under the coverage bound is slack or search weakness.** A
   search seeing all 134,400 cases still stops 0.0879 below it, down from the
   greedy's 0.1187 — evidence the bound is loose, not proof, since a heuristic
   that misses a bound never distinguishes the two. Exact optimization would
   settle it. FINDINGS3 §4 erratum.
2. **Why the proposer partitions instead of stratifying, and why it wrote nothing
   correct for two classes.** Rung 2's mechanism stays unmeasured until a base
   produces conflicts, and the 66.7%/64.2% material gap has no explanation.
   Undiscriminated: the framing (one ticket, one rule), the model, or rule-writing
   elicitation in general. FINDINGS2, "Why this is NOT a capability failure".
3. **ILP (Popper/ILASP) as a competitor.** Specified as Step B of rung 3, never
   run, still unauthorized. Decides whether the LLM proposer does work a cheaper
   inducer could not.

---

## What this does not show

**The original hypothesis — do the LLM's rules get reused, or does it memorize
cases? — has still never been measured cleanly.** It is the question the project
was built to answer.

Rung 1's **0.158 reuse** describes the arbitration, not the induction: 594 of its
632 escalations (94%) were CONFLICT, exactly what specificity-based arbitration
overproduces, and reuse, rule count, dead rules and the escalation curve are all
products of that loop ([`PREDICTION.md`](PREDICTION.md), "Why the stopping
threshold does not apply"). The engine ceiling underneath it was 0.5875.

Rung 2 built an engine with a 1.0000 ceiling, and then the change that made
declared priority possible — showing the proposer the base — is the one that left
it without material: 2 conflicts in 8 runs.

Whatever measures it next must clear the memorization floor: `keep_k(k=8)`
reaches **0.1176** reuse without inducing anything, purely from the corpus's
12.8% duplicates ([`results/frontier.json`](results/frontier.json)). A figure near
0.118 is noise.
