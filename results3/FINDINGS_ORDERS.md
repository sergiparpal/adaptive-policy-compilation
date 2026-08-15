# Findings — the orders, not the scores

August 15, 2026. **This record owns the figures below.** They are not part of
the optimizer audit ([`FINDINGS_AUDIT.md`](FINDINGS_AUDIT.md)): that audit was
about a search, and this is about what the search returns. Plan:
[`PLAN_ORDER_METRICS.md`](../PLAN_ORDER_METRICS.md), §0 drafted and committed
before any number existed and signed unchanged. Record:
[`order_metrics.json`](order_metrics.json). The instrument and its step 0
arrived in PR #13; the regeneration and these figures in PR #17, PR #15 having
landed them once and PR #16 having reverted that whole. Zero API calls.

**The revert was editorial, and the diff says so rather than this sentence
doing it.** Both landings carry the same measurements: `git diff 21b3293 HEAD --
results3/order_metrics.json` is empty and the `code_digest` inside that record
reads `1ffac0092a1f6c06` either way, while `git diff d4381fe HEAD --
results3/FINDINGS_ORDERS.md` is the entire change and is confined to how Q-d,
Q-f and G4 are read. (`21b3293` and `d4381fe` are the two commits PR #15 landed;
they stay on `main`, followed by PR #16's reverts of them.)

**Surface.** Every distance, signature and per-class rate here is over the
**exhaustive space** of 134,400 cases, **pure pool**. The `train`, `test` and
`space` figures of the parity gate are the surfaces of the records being
reproduced: the labelled subset, corpus test, and that same space.

---

## Why there was nothing to read (G1)

Four rungs compared permutations of 577 rules by looking at a scalar. **No
record in `results*/` held an order produced by the audited optimizer.**
`multistart` searched from 65 starts, returned the winner, and dropped the other
64 inside its loop. A scan of every JSON in `results*/` finds exactly one
complete order stored anywhere: `order_search.json::best_order_split0_pure`, 577
ids, which is the **superseded rung-3 greedy**.

So the orders behind rungs 3 and 4 could not be inspected; they had to be
produced again and then shown to be the same objects. That is what the parity
gate below does, and it is the reason this work is a regeneration rather than a
query.

---

## What can matter at all (G2)

Under first-match-wins the relative order of two rules can change a decision only
if **both match a common case and they prescribe different actions**. Over the
577 rules:

| surface / pool | pairs | co-match | conflicting | % |
|---|---|---|---|---|
| exhaustive space, pure | 166,176 | 53,620 | **35,457** | 21.3% |
| exhaustive space, hybrid | 166,176 | 13,064 | 9,239 | 5.6% |
| corpus n=2000, pure | 166,176 | 51,499 | 33,631 | 20.2% |
| corpus n=2000, hybrid | 166,176 | 9,572 | 6,355 | 3.8% |

Roughly **four fifths of the permutation is free** on the pure pool, and
nineteen twentieths on the hybrid one, where subsumption has already silenced
181 rules. This is what makes a rank statistic over all pairs a poor summary,
and it is the premise the instrument was designed on.

**Being a conflicting pair is necessary and not sufficient**, recorded in PR #13
before any of the figures below existed. Over the 29 hidden rules, several
adjacent conflicting pairs change no decision at all: they co-match somewhere in
the space and nowhere that survives the rules above them. The 35,457 is
therefore an upper bound on the pairs that can matter, not a count of
differences that will happen — and it is why Q-d's premise was already limping
before Q-d was measured.

---

## What was regenerated, and how it is known to be the same thing (G6)

Full supervision on splits 0 and 4 at budgets 65 / 129 / 257 starts, against
[`start_budget_check.json`](start_budget_check.json); and the **whole 1% band**,
5 splits × 5 draws, against
[`budget_and_balance_ls.json`](budget_and_balance_ls.json).

**The parity gate passes on all 31 rows.** Every `train_score`, `train`, `test`
and `space` equals the published value exactly — 883/0.8786/0.8472/0.6033 at
split 0 and 65 starts, 884/0.8796/0.8442/0.5776 at 257, and so on for all six
budget rows; 25 of 25 band cells reproduce, the cell Q-b is evaluated on
included. Nothing in this record would be about the published orders if it did
not.

**The nested-prefix shortcut was checked, not argued.** The 65 and 129 budgets
are read off one 257-start run per split, since `declared_starts` draws its
shuffles in sequence. An independent 65-start run on split 0 returns the same
best score 883, from the same index 14, with the **same order rule for rule**,
and all 65 rows carry the same end scores. The shortcut turns 237 s of search
into 137 s per split and answers three budgets with one run.

**The undecided branch is identically zero**, as predicted in PR #13: no pair in
any set has a single case left undecided by either order. Both pools cover the
whole space and the corpus record publishes `cases_without_matching_rule: 0`, so
behavioural distance here reduces to agree/disagree, and the third category
exists for toys and truncated orders.

---

## The predictions of §0, one by one

| # | verdict | measured |
|---|---|---|
| **Q-a** | **HOLDS** | Split 0, winner at 65 starts against winner at 257: **11,240** cases of the space decided differently (8.36%), against a predicted floor of 6,910 and an arithmetic floor of 3,455. Split 4: **14,430** (10.74%). |
| **Q-b** | **HOLDS, and by a wide margin** | At 1% (split 0, draw 0), the **40** orders tying at the best train score — 780 pairs — have a median pairwise disagreement of **52,744 cases, 39.2%** of the space, against a predicted 20% and a refutation line at 5%. Range 18,250 to 86,110. |
| **Q-c** | **HOLDS** | The 65 end orders at full supervision are **65 distinct behavioural signatures**, and so are all 257. Best against runner-up: **15,955** cases (11.87%) while **2 train cases** apart. |
| **Q-d** | **REFUTED — but only its second half; the first is confirmed** | Over the 32,896 pairs of split 0: global tau against behavioural distance, Spearman **−0.1361**, so |ρ| **< 0.5** and the first clause — *a rank statistic over all pairs tracks behaviour poorly* — is **CONFIRMED**. Restricted to the 35,457 conflicting pairs: **−0.1349**, nowhere near the > 0.8 predicted and **not better than the global one**, which is the refutation verbatim. Split 4 the same: −0.078 against −0.062. |
| **Q-e** | **HOLDS** | Median churn **99.65%** of rules at a different index; median disagreement **19.99%**. **30,775 of 32,896 pairs (93.6%)** move more than 60% of the rules while disagreeing on less than 30% of the space. |
| **Q-f** | **REFUTED, and in the opposite direction** | Pooled over the 2,080 pairs of split 0's 65 end orders, overall rate **0.2035**; **ACCOUNT_MANAGER 0.0916 (0.45×)** and **T3_ENGINEERING 0.0947 (0.47×)**, both *below* the overall rate, which is the stated refutation. Disagreement concentrates instead on **SECURITY_INCIDENT, 0.3121 (1.53×)**. |

### Q-d, and what exactly is refuted

**The two halves came out differently and must be read separately.** Q-d
predicted that a rank statistic over all pairs would track behaviour poorly, and
that restricting it to the pairs that can change a decision would rescue it.
The first half is **confirmed** — |ρ| = 0.1361, well under the 0.5 it named. The
second is **refuted**: the restricted statistic reaches 0.1349, not the 0.8 it
needed, and does not beat the metric it was supposed to rescue.

**§0 wrote that this refutation would mean "the design premise of this
instrument is wrong". That inference is mistaken, and this record says so
instead of inheriting it.** The premise of the instrument is that two orders
must be compared by the decisions they produce rather than by the ranks they
assign — which is why `behavioural_distance` exists at all and is computed
exactly, one bitmask sweep per order. A rank statistic failing to track
behaviour *even after it is given only the pairs that can matter* is evidence
**for** that premise, not against it. What the refutation kills is the cheap
shortcut §0 hoped for beside it: that a corrected tau could stand in for the
exact comparison when the exact comparison was inconvenient. It cannot — and at
0.15 ms per decision vector it never needed to.

**Which of the two failure modes it is: dispersed, not degenerate.** An earlier
draft of this section said a statistic with no variance cannot track one with
plenty. That explanation is wrong — Spearman is a rank correlation and needs no
spread of magnitude — and the measurement says the opposite of it. Over the
32,896 pairs of split 0:

| | distinct values | modal value | p25 | median | p75 | IQR | range |
|---|---|---|---|---|---|---|---|
| tau, all pairs | **9,772** | 16 pairs (0.05%) | 0.0147 | 0.0339 | 0.0530 | **0.0383** | −0.0821 … 0.1475 |
| tau, conflicting pairs | **3,456** | 34 pairs (0.10%) | 0.0177 | 0.0423 | 0.0670 | **0.0492** | −0.0980 … 0.1915 |
| behavioural distance | — | — | 21,940 | 26,860 | 32,630 | **10,690** | 2,615 … 56,565 |

There are no ties to speak of: no tau value covers more than a tenth of a
percent of the pairs. **Both quantities vary; they simply do not vary
together.** That is a different and stronger finding than degeneracy would have
been — a degenerate statistic could be fixed by a finer one, and this cannot.

**How much rank signal there was to track: almost none.** For two
**independent** permutations of n elements, Kendall tau has mean 0 and standard
deviation √( 2(2n+5) / (9n(n−1)) ), which at n = 577 is **σ = 0.0278**. That is
closed form on the number of rules, not a new measurement, and it is the
yardstick the table was missing. Against it the global tau's median of 0.0339 is
**1.22 σ**, and its interquartile range runs from **0.53 σ to 1.90 σ**. In rank
terms these end orders are barely distinguishable from independent random
permutations of one another — while their behavioural distance covers a **factor
of 21**, from 2,615 to 56,565 cases.

So Q-d's failure, said with a magnitude: it is not that rank follows behaviour
badly here. It is that **there was almost no rank signal to follow**, and a
quantity whose middle half sits between half a sigma and two sigma of pure
independence cannot track one that moves by a factor of 21. The tails do reach
further — the extremes of the global row are −2.95 σ and +5.30 σ — which is why
the claim is about how little the bulk moves, not about every pair.

The yardstick covers the **global row only**. That closed form is derived for
tau over all C(n,2) pairs of a permutation; over an arbitrary subset — the
35,457 conflicting pairs, which overlap in a dependence structure of their own —
neither the variance nor the null it comes from carries over, and this record
does not stretch it to a row it does not cover.

**The distinct-value counts, meanwhile, compare nothing — and that is arithmetic
rather than evidence.** Tau over a pair set P takes values only in multiples of
2/|P|, so computing it over 35,457 pairs instead of 166,176 makes its grid
**4.69× coarser by construction**, whether or not the restriction rescues
anything. Measured against the grid each one actually has, the restricted
statistic fills **more** of it rather than less: 3,456 of the ~5,130 values
available across its observed range, against 9,772 of ~19,080 for the global one
— **67% against 51%**. An earlier draft read the smaller count as a blunter
instrument; it is the same instrument on a coarser ruler, and the count settles
nothing either way.

What does survive is PR #13's finding that conflicting pairs can be inert: the
restriction does not even isolate the pairs that decided anything **in these
particular orders**, only those that could decide something in some order. That
is the argument against the rescue clause, and it stands on its own.

*Where those figures come from.* Every quantile in the table is already in
[`order_metrics.json`](order_metrics.json) under `sets.split0_starts257`. Only
the distinct-value counts and the modal frequencies were added afterwards, by
regenerating split 0 down the same deterministic path and tallying the two tau
columns over all 32,896 pairs; that re-run returns **the same winner at 65 and
the same winner at 257 that the record stores**, rule for rule, and reproduces
both Spearman figures to the digit, which is how the tally is known to be about
these pairs and not about a second sample. The σ yardstick is closed form on
n = 577 and the grid arithmetic is 2/|P| on two pair counts already published
above: neither involves a measurement at all.

**Q-d was measured exactly as written**, with the same 35,457-pair set §0
declared, after that weakness was already on the record. Re-specifying it to,
say, the conflicting pairs inside the coverage length would have been changing
the instrument once the premise limped, which is what §0 exists to prevent. What
the refutation licenses is a future question, not a retrofit: whether any rank
statistic tracks behaviour here at all.

### Q-f, and why the bet ran backwards

§0 reasoned that disagreement would concentrate where material is scarce.
Measured, it concentrates where material is **abundant and contested**.

The mechanism is the same arithmetic as G2, read per class. Two orders can only
disagree on a case that two rules with different actions both match; where most
of a class has no correct rule at all there is nothing to compete over, so the
orders are uniformly wrong there rather than differently wrong.
`SECURITY_INCIDENT`, the largest class on the uniform surface with 50,400 of
134,400 cases, is where the proposer wrote most and where the orders fight.

**That mechanism has a second source, measured by another route and published
before this work.** The per-class ceilings of
[`budget_and_balance_ls.json`](budget_and_balance_ls.json)`::per_class_split0`
count, case by case on **corpus test**, how many cases of each class any rule
could get right: **ACCOUNT_MANAGER 21 of 55** and **T3_ENGINEERING 20 of 57** —
61.8% and 64.9% with no correct rule covering them, against 0% for five of the
remaining six classes. `FINDINGS3.md` §2 reaches 64.2% and 66.7% for the same
two classes on the whole corpus. So the material gap this explanation rests on
is not inferred from the disagreement rates it explains: it was counted
independently, on a different surface, by a script that knows nothing about
orders.

The two surfaces agree on which classes are starved and are not interchangeable
about anything else: the ceilings are corpus test, the disagreement rates are
the uniform space.

On the single pair Q-a names, ACCOUNT_MANAGER does reach 1.64× the overall rate
— but T3_ENGINEERING is at 0.35×, so even the reading most favourable to the
prediction refutes it. Both are in the record.

---

## What the numbers say about the orders themselves

**G3 — there is no clustering to find.** Every set measured is entirely
distinct: 257 signatures from 257 end orders on both splits, 129 from 129, 65
from 65, **40 from the 40 tied orders** at 1%, and 65 from the 65 end orders of
that whole 1% cell. Not one behavioural collision anywhere. The multi-start does
not converge on a few machines that its score cannot tell apart; it produces a
different machine every time.

**G4 — the freedom is per pair, and it does not compose.** Zero pairs, in any
set, sit at behavioural distance 0 with a positive positional distance. That is
not the property of §0 failing; it is the property being stated precisely.

Each of the 130,719 non-conflicting pairs can be inverted on its own without
changing a decision, and that is exactly what P2 pins on a toy and P3 recovers
over the 29 hidden rules. What does **not** follow is that two orders drawn
independently will differ *only* in free pairs. There are 35,457 conflicting
pairs; two permutations produced by separate searches will almost surely invert
at least one of them, and inverting one is enough to make them different
machines. So both statements are true at once, and neither weakens the other:
**four fifths of any single permutation is free, and no two of these 257 end
orders are behaviourally identical.**

That composition failure is also why G3 comes out the way it does. All 257
signatures being distinct is not evidence of a rugged landscape by itself — it
is what a per-pair freedom that does not compose predicts, and the interesting
figure is not *that* they differ but *by how much*, which is Q-a, Q-b and Q-e.

**G5 — the greedy's end order sits inside the cloud.** Distances from the end
order of start 0, which is the record's greedy, to the other 64 at split 0:
median 25,022 against 26,620 for all other pairs, inside the 21,450–33,080
interquartile range of the cloud. Split 4: 24,872 against 29,322. It is
marginally *more* typical than average, not an outlier — so what the tie-break
at index 0 returns is not a peculiar order, merely one of many.

**Agreeing for different reasons.** Secondary, and with the caveat P2 records:
rule-level agreement is contained in behavioural agreement, so what it measures
is the shortfall. On the Q-a pair the two orders agree on 123,160 cases and fire
the same rule on 64,260 of them — **58,900 cases, 47.8% of their agreement, are
agreements for different reasons**. Explainability and behaviour are not the
same question, and the gap between them is about half.

---

## What this changes elsewhere

**The low-budget rows of the audit's step 3 need a caveat, and Q-b supplies
it.** [`FINDINGS_AUDIT.md`](FINDINGS_AUDIT.md) reads them as *the tie-break
regularises*: the objective saturates, most starts tie, ties go to index 0,
index 0 is the greedy, so the search returns something sane and cannot lose.
That reading is too kind. At (split 0, draw 0) the 40 tied orders are **40
distinct machines** that disagree with each other on a median 39% of the space,
and the tie-break picks among them by index. The search is not declining to act;
it is choosing arbitrarily among very different answers and landing on a sane
default **by accident of the start order**. Anyone who changes the tie-break, or
the order of the declared starts, changes which of 40 machines ships.

That is a caveat on how those rows are read, not a withdrawal: the figures
`FINDINGS_AUDIT.md` publishes are what the declared instrument returns, and they
still are.

**And the same caveat, at full supervision, has a number now.** `STATUS.md`
already said a reader of the score can rely on it while a reader of the order
inherits a draw. The draw is worth **11,240 cases of the space between the
winner at 65 starts and the winner at 257** on split 0, and 14,430 on split 4,
for train differences of 1 and 3 cases.

**None of this is an argument about `MULTISTART_STARTS`.** It stays 64 because
it was declared before the runs that used it. The 257-start rows are a
diagnostic in exactly the sense `start_budget_check` declared, and a measurement
of how much behaviour hides under a score is not a reason to move a constant —
in either direction.

---

## The register

| id | finding | status |
|---|---|---|
| **G1** | No record in `results*/` holds an order from the audited optimizer; the only stored order is the superseded rung-3 greedy in `order_search.json`. | **CONFIRMED**, by scanning every JSON in `results*/`. Worth changing for future runs: `multistart(keep_orders=True)` now exists and costs nothing when unused, so a run that wants its orders on the record can have them. Reported, not retrofitted — no published record is rewritten. |
| **G2** | Of 166,176 pairs, 53,620 co-match and 35,457 conflict on the space. | **REPRODUCED** digit for digit, and extended to the other three surface/pool combinations above. |
| **G3** | Whether the 65 end orders cluster into few behavioural classes or are all distinct. | **ALL DISTINCT**, in every set measured, up to 257 of 257. |
| **G4** | Any pair with behavioural distance 0 and positional distance > 0. | **NONE**, in any set — and that is a refinement of §0's freedom, not a failure of it. The freedom is per pair and does not compose: with 35,457 conflicting pairs, two independently produced orders almost surely invert at least one, and one is enough. Both hold at once, which is also why G3 reads as it does. |
| **G5** | Where the greedy start's end order sits relative to the random starts'. | **INSIDE THE CLOUD**, marginally more typical than average, on both splits. |
| **G6** | Anything the parity gate turns up. | **NOTHING**: 31 of 31 rows exact, and the prefix shortcut reproduces an independent run rule for rule. The one thing it does turn up is a provenance note, below. |

---

## Provenance, and one flag that reads badly on its own

The record carries **`code_dirty: true`** at commit `2a598530`, and that is
honest rather than alarming: the runner that produced it,
`peldano3/order_metrics_run.py`, was untracked when it ran, which is what the
flag is for. What identifies the code is **`code_digest 1ffac0092a1f6c06`**,
which is a digest of content and therefore survives the rebase that renames
every commit on merge — the commit SHA does not, as PR #13's description found
out. What identifies the **orders** is neither: it is the parity gate, and the
parity gate is exact.

**Cost: 717 s in one process, zero API calls.** Regeneration 380 s — 137.7 s and
118.5 s for the two 257-start searches, 90.2 s for the whole 1% band, 34.0 s for
the shortcut check — which is §5's *≈ 6 min* almost exactly. The measuring took
the other 314 s, where §5 said "seconds". Its estimate was right about the
distances (32,896 of them cost 3 s) and wrong about Kendall tau: the restricted
tau costs 4 ms a pair, and it alone is 260 s of this run. One decision vector
over the space costs 0.15 ms, not the 0.6 ms probed.

**What the 840 KB of the record are.** Two stored matrices and nothing else of
consequence: the 2,080 pairs of split 0's 65 end orders take **477 KB (56.9%)**
and the 780 pairs of the tied set at 1% take **179 KB (21.3%)** — 78% between
them, at ten fields a pair. The five orders the findings cite are 37 KB (4.4%)
and the per-set summaries 32 KB (3.8%); everything else is under 1% each. Each
matrix is stored **once, as one triangle**: 2,080 rows is exactly 65·64/2, every
row has `i < j`, and no `(j, i)` appears — so there is no duplicate half to
drop. The 257-order matrices are not stored at all, only summarized, which is
what keeps this file at 840 KB instead of 11 MB.

---

## What this does not settle

- **Whether any rank statistic tracks behaviour on this material.** Q-d refutes
  the one §0 proposed, and refutes the easy excuse for it: both taus are
  dispersed, with thousands of distinct values and no ties worth the name, so
  the failure is not a range artefact that a finer statistic would repair. What
  a *different* statistic — weighted by how many cases each conflicting pair
  actually decides, say — would do is unmeasured, and is not something to try
  after the fact on this data.
- **Why 65 draws give 65 machines.** That the landscape has no plateaus the
  objective can see is measured; what shape it has instead is not.
- **What any of this costs downstream.** Rung 4 consumes orders. That its
  figures inherit a draw was already recorded; that the draw is worth ~8% of the
  space between two orders one train case apart is new, and what it does to a
  learned policy in deployment is unmeasured.
- **The corpus surface.** Everything above is the uniform measure over 134,400
  cases. Two orders that disagree on 20% of the space need not disagree on 20%
  of the arrival distribution, and this record did not say which.
  **Answered on 2026-08-15 by the section below**, which is part of this same
  record: they do not. The rate is 5.75%, and where it falls changes completely.

---

# The corpus surface — S-a to S-f

August 15, 2026. **This part of the record owns the corpus figures**;
everything above it is the exhaustive space, and the two are not
interchangeable about anything. Same 577 rules, same orders, same instrument:
the surface is the only thing that changes. Prediction: `IDEAS.md`, the entry
*The surface question has its first measurable instance*, drafted and committed
before any of these numbers existed (PR #18, PR #19, PR #20). These figures
arrived afterwards, in **PR #21**, which is what makes the order of the two
checkable in the log rather than asserted here. Record:
[`order_metrics_corpus.json`](order_metrics_corpus.json). Zero API calls, 396 s.

It is a separate record from [`order_metrics.json`](order_metrics.json) and a
section of the same findings, on purpose. Two records because they are two
surfaces and a run that overwrote the first would destroy the comparison; one
document because it is one question.

**Four of the six are refuted.** That is the result, and it is published as one.

---

## The two surfaces, named

| surface | cases | what it is |
|---|---|---|
| **corpus, all 2000** | 2,000 | the modelled arrival distribution, whole. What the entry means by *the corpus*, and what these predictions adjudicate on. The search saw the train half of it. |
| **corpus test half** | 995 (split 0), 1002 (split 4) | the same distribution with the fitted half removed. Reported beside every figure below. |
| exhaustive space | 134,400 | the uniform measure, for comparison. Owned by the first part of this record. |

Every verdict below came out the same on both corpus surfaces. Where the
numbers differ they differ in size, never in sign, and both are printed.

## The gates

**Parity: 31 of 31 rows exact**, the same gate as the first part and against the
same two records — 883 / 0.8786 / 0.8472 / 0.6033 at split 0 and 65 starts,
884 / 0.8796 / 0.8442 / 0.5776 at 257, all six budget rows, and 25 of 25 band
cells. **No new search**: every order comes out of `run_full_supervision` and
`run_band_1pct` of `order_metrics_run.py`, imported and called unchanged. The
prefix shortcut is not revalidated — it was checked against an independent
65-start run when it was introduced.

**The corpus census reproduces G2 exactly**: 166,176 pairs, 51,499 co-matching,
**33,631 conflicting** over the corpus pure pool. That is the one published
figure that pins the *masks* rather than the orders, and the masks are what this
run changes.

**The invariants hold.** `d(a, a) = 0` on all seven set-and-surface
combinations measured; `undecided_either` is 0 everywhere, on the corpus as on
the space. Had any of these failed, the prediction would not have been tested at
all.

---

## The predictions of `IDEAS.md`, one by one

| # | verdict | measured |
|---|---|---|
| **S-a** | **REFUTED**, and not narrowly | Pooled over the 2,080 pairs of split 0's 65 end orders: **5.75%** of the full corpus, **6.45%** of test. Predicted band 12–20%, refutation line 10%. The same pairs pool to **20.35%** of the space. |
| **S-b** | **REFUTED** | The same 5.75% against the 15.2% the bet named — and below the **11.67%** that the reweighting it describes actually produces. The direction is the opposite of the bet: the corpus subtracts disagreement rather than adding it. |
| **S-c** | **REFUTED** | Of the six classes with ≥100 corpus cases, **four** fall outside ±30% relative: `T2_TECHNICAL` **−81.6%**, `BILLING_SPECIALIST` **+165.2%**, `T3_ENGINEERING` −42.7%, `ACCOUNT_MANAGER` −42.0%. Inside: `T1_GENERAL` −29.9% and `SELF_SERVICE_DEFLECT` +10.3%. |
| **S-d** | **REFUTED**, narrowly, and in exactly the way S-c predicts | `SECURITY_INCIDENT`'s share of the total disagreement falls from **57.5% to 4.57%** (5.06% on test) against a line of *under 3%*. Pure reweighting predicts **2.67%**, which is where the 3% came from. |
| **S-e** | **HOLDS**, both clauses | Of the 32,896 pairs of the 257-start set, **zero** sit at distance 0 on the corpus — so none can sit at 0 here and above 0 on the space. The pairwise minimum falls from **2,615 cases (1.9%)** to **2 of 2000 (0.10%)**, and to 1 of 995 on test. |
| **S-f** | **HOLDS** | The 40 orders tying at the best train score at 1% disagree a median **24.05%** of the full corpus (481 cases) and **24.32%** of test (242 cases), against a 20% line and a 10% refutation. |

### S-a and S-b: the collapse, and the mechanism that is not the reason for it

The headline is one number: **20.35% of the space, 5.75% of the corpus**, the
same 2,080 pairs of the same 65 orders. A factor of 3.5. The per-pair median
moves with it, 19.72% to 5.90%, so this is not one outlier pair dragging a pooled
figure.

**S-b argued from a premise, and the premise is true.** It reasoned that the 577
rules were written looking at the corpus, so the typical arriving case carries
more rules and more competing pairs than the typical point of the space. Measured
on the same masks:

| surface | rules matching the average case | conflicting pairs live on it |
|---|---|---|
| exhaustive space | 37.82 | 416.50 |
| corpus, all 2000 | **50.25** | **724.43** |
| corpus test, split 0 | 49.94 | 702.63 |

The average arriving case carries **33% more rules** and **74% more contested
pairs** than the average point of the space — and disagreement is **3.5 times
lower** there. So the collapse is not scarcity of material to disagree over. That
is the informative half of this refutation: *more competition, less
disagreement*, and the two quantities do not move together at all.

**How much of it is fitting: about a tenth.** Train and test partition the 2000
cases, so the two pooled rates this record publishes fix the third by arithmetic
rather than by a new measurement: 5.75% over 2000 and 6.45% over the 995 test
cases put the 1005 fitted ones at **5.06%**. The orders do agree more where the
objective looked — by 1.39 points — but the surface effect is 13.9 points, so
fitting accounts for roughly **10%** of the gap and the change of surface for
the rest.

**Why the other 90%, this record does not say.** It bounds it from two sides —
not scarcity, not mainly fitting — and stops there. Anything further would be an
explanation invented after the fact for a number already in hand, which is what
§0 of the plan exists to prevent.

**One yardstick does not reconstruct, and it is reported rather than repaired.**
S-b's 15.2% is described as *reweighting the space's per-class rates by the
arrival distribution*. Done with the rates this record publishes and the corpus
class sizes, that sum is **11.67%**, not 15.2%, and no other reading tried gets
there — the tied set at 1% gives 28.03%, the Q-a pair 4.29%. Where the number
came from is unknown. It changes no verdict: 5.75% is below both. The line
adjudicated against is the one the prediction wrote, 15.2%, because moving a
threshold to a reconstruction after seeing the measurement is the failure this
project studies, and it would not have helped here anyway.

### S-c and S-d: where the disagreement falls, which was the actual question

The entry asked it plainly — the material to disagree over is nearly the same on
either surface, *what is unknown is where it falls*. It falls somewhere else.

| class | corpus n | corpus rate | ×overall | space rate | rel. change | share of corpus disagreement | share of space disagreement |
|---|---|---|---|---|---|---|---|
| `SELF_SERVICE_DEFLECT` | 495 | 0.1040 | 1.81 | 0.0943 | +10.3% | **44.8%** | 1.5% |
| `T2_TECHNICAL` | 726 | 0.0362 | 0.63 | 0.1969 | **−81.6%** | 22.9% | 26.4% |
| `BILLING_SPECIALIST` | 271 | 0.0401 | 0.70 | 0.0151 | **+165.2%** | 9.5% | 0.4% |
| `T1_GENERAL` | 255 | 0.0298 | 0.52 | 0.0426 | −29.9% | 6.6% | 0.8% |
| `T3_ENGINEERING` | 117 | 0.0542 | 0.94 | 0.0947 | −42.7% | 5.5% | 2.8% |
| `ACCOUNT_MANAGER` | 109 | 0.0531 | 0.92 | 0.0916 | −42.0% | 5.0% | 5.5% |
| `SECURITY_INCIDENT` | 20 | 0.2626 | **4.57** | 0.3121 | −15.9% | 4.6% | **57.5%** |
| `ONCALL_ESCALATION` | 7 | 0.1910 | **3.32** | 0.2178 | −12.3% | 1.2% | 5.0% |

Read the last two columns first. On the uniform space, **57.5% of everything two
end orders disagree about is `SECURITY_INCIDENT`** — a class that is 37.5% of
the space and 1% of arrivals. On the corpus that share is **4.6%**, and the
disagreement is concentrated instead on `SELF_SERVICE_DEFLECT`, 24.75% of
arrivals and 3.2% of the space. The reading of `FINDINGS_ORDERS`' Q-f — *the
orders fight where the proposer wrote most* — is a fact about the uniform
measure and does not survive to the arrival distribution.

**S-c is the larger finding its own refutation clause anticipated.** It predicted
per-class rates would carry across, and said that failing would mean the mix of
cases *within* a class governs too. It fails, and by a lot: the same class,
`T2_TECHNICAL`, disagrees on 19.69% of its space cases and 3.62% of its corpus
cases — and it is the largest class of the corpus (726 of 2000) and the second
largest of the space (36,720 of 134,400), so this is not a small-sample effect.
`BILLING_SPECIALIST` moves the other way, ×2.65. Two orders differ not on
*a class* but on a region, and which part of a class the surface samples decides
whether that region is in it.

**S-d then follows arithmetically, and it is worth seeing why it missed.**
`SECURITY_INCIDENT`'s own rate carries across almost intact, −15.9% — which
would have been *inside* S-c's ±30% band had the class been eligible for it, and
it is not: 20 corpus cases against the 100 S-c requires. What does not carry is
the denominator: the overall
rate collapsed by 3.5×, so a class whose rate barely moved keeps a larger share
than reweighting predicts — 4.57% measured against 2.67% modelled. The direction
of S-d was right and the magnitude was off by 70% relative, and the reason is
precisely the classes S-c caught.

**The deployment reading, which is not the same as the aggregate.** Two end
orders differ on 5.75% of arrivals, and 45% of that lands on the deflection
queue. But per case of the class, `SECURITY_INCIDENT` runs at **4.57×** the
overall rate and `ONCALL_ESCALATION` at **3.32×** — the two classes rung 1
resolved 0 of 17 and 0 of 7 times. Rare in traffic and disproportionately exposed
to which of 65 orders shipped: a small share of a small number, and the wrong
place for either.

### S-e and S-f: what the change of surface does not touch

**S-e holds, and by a factor of ten on its second clause.** No pair of the 32,896
is behaviourally identical on the corpus — not one — so the case the prediction
called *the large finding here*, two orders distinguishable in principle and
identical wherever cases actually arrive, does not occur at this scale. The
closest pair differs on **2 cases of 2000**; on the space the closest differ on
2,615 of 134,400. Predicted *under 1%*, measured 0.10%.

**And G3 and G4 carry across untouched.** 257 distinct behavioural signatures
from 257 end orders, on both corpus surfaces and both splits; 65 of 65; 40 of 40
for the tied set. Zero pairs anywhere at behavioural distance 0 with positional
distance above 0. The multi-start still produces a different machine every time,
and the freedom per pair still does not compose. What changed is the size of the
difference, not its existence.

**S-f holds, and the low-budget caveat survives the surface.** At 10 labels the
40 tied orders disagree a median 39.2% of the space and **24.05% of the corpus**
— a fall of 1.6×, against 3.5× at full supervision. The whole 1% band behaves the
same way: across the 25 cells the corpus median runs 22.1% to 35.8% against the
space's 30.4% to 44.9%, and the cell S-f names is not the extreme of either.
So *the search is choosing arbitrarily among very different answers* remains true
of what a deployed system would meet, and the caveat that section leaves on
`FINDINGS_AUDIT`'s step 3 does not need weakening.

**That contrast is the shape of the whole result.** Where supervision is full the
change of surface divides the disagreement by 3.5; where the objective saturates
at 1% it divides it by 1.6. The better the orders are fitted, the more the
surface flatters them.

---

## What this changes in the first part of this record

**The headline draw, translated.** `STATUS.md` and the section above quote 11,240
cases — 8.36% of the space — between the winner at 65 starts and the winner at
257, one train case apart. On the corpus that same pair differs on **33 of 2000
cases, 1.65%**, and on 22 of 995 test cases, 2.21%. Split 4, three train cases
apart: 14,430 (10.74%) becomes **50 of 2000, 2.50%**, and 33 of 1002, 3.29%.

**Nothing above is withdrawn.** Every space figure is what it always was, and it
was always labelled as the uniform measure. What the corpus adds is that a reader
who took 8.36% as *what shipping the other order would cost* was reading the
wrong surface by a factor of five.

**Explainability diverges more, not less.** On the Q-a pair the two orders agree
on 1,967 corpus cases and fire the same rule on 677 of them: **65.6% of their
agreements are agreements for different reasons**, against 47.8% on the space.
The gap between behaviour and attribution is wider where the cases actually
arrive.

---

## The register, second part

| id | finding | status |
|---|---|---|
| **S-a** | The disagreement of the 65-start set, on the corpus, between 12% and 20%. | **REFUTED**: 5.75% pooled, below the 10% refutation line. |
| **S-b** | That rate above the 15.2% of a pure reweighting. | **REFUTED**: 5.75%, below the 15.2% written and below the 11.67% reconstructed. Its stated mechanism is confirmed and does not produce the effect. |
| **S-c** | Per-class rates preserved to ±30% relative. | **REFUTED**: 4 of 6 eligible classes outside, from −81.6% to +165.2%. |
| **S-d** | `SECURITY_INCIDENT`'s share of the disagreement under 3%. | **REFUTED**: 4.57%, against 2.67% modelled and 57.5% on the space. |
| **S-e** | No pair identical on the corpus and different on the space; pairwise minimum under 1%. | **HOLDS**: zero such pairs, minimum 0.10%. |
| **S-f** | The tied set at 1% still above 20% on the corpus. | **HOLDS**: median 24.05% full corpus, 24.32% test. |
| **S-g** | *(not predicted)* Whether the distinctness findings survive the surface. | **THEY DO**: 257 of 257, 65 of 65, 40 of 40 distinct machines; zero identical-behaviour pairs. |

---

## Provenance of the corpus part

**Cost: 396 s in one process, zero API calls** — against the *seven or eight
minutes* the entry estimated. Regeneration is 342 s of it (137.5 s and 118.2 s
for the two 257-start searches, 86.5 s for the whole 1% band), and the measuring
51 s: five 32,896-pair matrices on three surfaces, the tied set, the whole band
on the corpus, and the two censuses. It is cheap for the reason the entry gave —
2,000-bit masks instead of 134,400 — and because no Kendall tau is computed, tau
having been the 260 s that dominated the first part.

**`code_dirty: true` at commit `a7e2d2a6`, for the same reason as the first
part**: the runner that produced this record, `peldano3/order_metrics_corpus.py`,
was untracked when it ran. What identifies the code is `code_digest
99184aa53d866fac`; what identifies the **orders** is neither, it is the parity
gate, and the parity gate is exact on all 31 rows.

---

## What the corpus part does not settle

- **Why 3.5×.** Not scarcity of contested material — the corpus carries 74% more
  live conflicting pairs per case — and only about a tenth of it is fitting.
  What accounts for the rest is unmeasured, and this record declines to invent
  it after the fact.
- **Whether "corpus" means deployment.** It is a modelled arrival distribution
  with a seed, not observed traffic. Everything here says the two surfaces
  disagree; nothing here says the corpus is the right one.
- **Where S-b's 15.2% came from.** Nothing in this run reconstructs it, and the
  prediction is not edited to match what does.
- **The other three splits at full supervision.** Splits 0 and 4 are measured
  because they are the two `start_budget_check` saw the train score move on.
  Whether the 3.5× is stable across the other three is not known.
