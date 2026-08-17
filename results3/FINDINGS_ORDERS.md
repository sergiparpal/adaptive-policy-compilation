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

**Where the per-class truth comes from, which the census gate does not cover.**
S-c and S-d divide by class, and there are two sources of truth in this
repository in **different bit conventions**: `build_masks` puts case `idxs[k]`
at bit k, while `order_search_ls.space_truth_masks` is the space's truth in
`Space`'s convention, case k at bit n−1−k. Every per-class figure below comes
from **`inst["truth"]`** — the label list `order_search.build_tables` produced
once for the 2000 cases — sliced into one mask per class **over the indices
actually measured**, in `build_masks`' convention. `space_truth_masks` is used
for nothing here; had it been, the totals would still have added up and every
per-class number would have been noise of the right shape. The G2 census gate
cannot see this: it pins the rule masks M, and a pair count never looks at a
label. What sees it is
[`tests/test_order_metrics_corpus.py`](../tests/test_order_metrics_corpus.py):
the class masks **partition** each of the three measured surfaces — pairwise
disjoint, union exactly `full`, bit counts summing to n — and
`W[r] == M[r] & truth[action[r]]` holds over all 577 rules on each, which is the
identity `build_masks` builds W by and which the reversed convention fails. That
last part is checked too, so the first is not passing vacuously.

**Exactly what was measured, and which of it adjudicates.** Three surfaces:
corpus full (2000), corpus test (995 for split 0, 1002 for split 4), and the
exhaustive space, the last only for S-e's first clause, which compares the two
surfaces pair by pair. Five 32,896-pair matrices: split 0 and split 4 on each
corpus surface, and split 0 on the space.

| set | surface | what it decides |
|---|---|---|
| `split0_starts65` | corpus full | **S-a, S-b, S-c, S-d**, all four pooled over its 2,080 pairs |
| `split0_starts257` | corpus full + space | **S-e**, both clauses |
| `b_tied_split0_draw0` | corpus full | **S-f** |
| the same three | corpus test | nothing; reported beside every one of them |
| `split0_starts129`, `split4_starts65/129/257` | both corpus surfaces | **nothing** — every prediction names split 0. Split 4 is the other split `start_budget_check` saw the train score move on, and is reported so that no figure rests on one split |
| `b_all65_split0_draw0` | both corpus surfaces | nothing; the containing set of S-f's 40 |
| the 25 tied sets of the 1% band | corpus full | nothing; context for S-f |
| `cited_pairs` | both corpus surfaces | nothing; the winner at 65 against the winner at 257, in full |
| `competition_census` | all three | nothing, and **post hoc** — see below |

The additions are additions. None of them entered a verdict, and the record
carries the same list under `sets_measured`.

---

## The predictions of `IDEAS.md`, one by one

| # | verdict | measured |
|---|---|---|
| **S-a** | **REFUTED**, and not narrowly | Pooled over the 2,080 pairs of split 0's 65 end orders: **5.75%** of the full corpus, **6.45%** of test. Predicted band 12–20%, refutation line 10%. The same pairs pool to **20.35%** of the space. |
| **S-b** | **REFUTED** | The same 5.75% against the 15.2% the bet named — and below the **11.67%** that the reweighting it describes actually produces. The direction is the opposite of the bet: the corpus subtracts disagreement rather than adding it. |
| **S-c** | **REFUTED** | Of the six classes with ≥100 corpus cases, **four** fall outside ±30% relative: `T2_TECHNICAL` **−81.6%**, `BILLING_SPECIALIST` **+165.2%**, `T3_ENGINEERING` −42.7%, `ACCOUNT_MANAGER` −42.0%. Inside: `T1_GENERAL` −29.9% and `SELF_SERVICE_DEFLECT` +10.3%. |
| **S-d** | **REFUTED on its stated value.** Its refutation condition is not a number and both readings are published below | `SECURITY_INCIDENT`'s share of the total disagreement falls from **57.5% to 4.57%** (5.06% on test) against a stated line of *under 3%*. Pure reweighting predicts **2.67%**, which is where the 3% came from. |
| **S-e** | **HOLDS**, both clauses | Of the 32,896 pairs of the 257-start set, **zero** sit at distance 0 on the corpus — so none can sit at 0 here and above 0 on the space. The pairwise minimum falls from **2,615 cases (1.9%)** to **2 of 2000 (0.10%)**, and to 1 of 995 on test. |
| **S-f** | **HOLDS** | The 40 orders tying at the best train score at 1% disagree a median **24.05%** of the full corpus (481 cases) and **24.32%** of test (242 cases), against a 20% line and a 10% refutation. |

### S-a and S-b: the collapse, and the mechanism that is not the reason for it

The headline is one number: **20.35% of the space, 5.75% of the corpus**, the
same 2,080 pairs of the same 65 orders. A factor of 3.5. The per-pair median
moves with it, 19.72% to 5.90%, so this is not one outlier pair dragging a pooled
figure.

**S-b argued from a premise, and the premise is true.** It reasoned that the 577
rules were written looking at the corpus, so the typical arriving case carries
more rules and more competing pairs than the typical point of the space.

**The two figures that follow are POST HOC and are a different kind of figure
from the adjudicated ones.** They were chosen and instrumented on 2026-08-15
*after* all six verdicts already existed, and *because* S-b had failed with a
mechanism written into it. The order is on the record: an earlier run of the
same module, without `competition()` in it at all (14:08:24Z, `code_digest
3bb4662a607fc9a0`), produced the six verdicts; the census was then written and
the module re-run whole (14:17:16Z, `code_digest 99184aa53d866fac`), reproducing
all six and adding it. That earlier record was overwritten by this one and is
not itself on the record, so what a reader can check is the code in this commit,
not that run — **and this record's `code_digest` therefore covers code written
after the verdicts existed.** The figures are kept because they separate *the
premise was false* from *the premise was true and the effect does not appear*,
which is the finding; they are marked because a quantity chosen after seeing a
refutation cannot be read as one named before it. Measured on the same masks:

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
cases, so the two pooled rates this record publishes fix the third **by
arithmetic on them and not by a measurement** — the train half was never
measured. From `pooled_full × 2000 = pooled_train × 1005 + pooled_test × 995`,
5.75% over 2000 and 6.45% over the 995 test cases put the 1005 fitted ones at
**5.06%**, a derived number and marked as one wherever it appears. The orders do
agree more where the objective looked — by 1.39 points — but the distance from
the space to the unfitted half is 13.9 points, so fitting accounts for roughly
**10%** of the gap and the change of surface for the rest.

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

**Where that sits in the log, plainly.** The failure to reconstruct was found on
reading the entry, before this run existed, and it was **not committed before the
record**: it reached the repository inside the same commit as the module and the
measurement, so the log does not separate the two and cannot be made to. It is
recorded here and in `IDEAS.md` as a finding of this work, not as a note that
predates it — that window closed when the two landed together.

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

**S-d has two lines in it and they do not agree, so the row is quoted rather
than summarized.** Verbatim:

> **S-d** — *Calibration.* SECURITY_INCIDENT's share of the total disagreement
> falls from **57.5% to under 3%**. *Refuted* by anything far from that, which
> would mean the per-class rates do not carry across and S-c will already have
> fired.

| reading | line | verdict on 4.57% |
|---|---|---|
| the stated value | *under 3%* | **REFUTED** |
| the refutation clause as written | *anything far from that* | **not decidable from the row**: 4.57% arrives from 57.5%, a fall of 12.6×, and lands 1.6 points above the line |

**The first is what was applied, and the reason is not that it is the harsher
one.** It is that the point value is the only half of the row a reader can check
mechanically — an adjective is not a threshold, and reading one charitably after
seeing the number is adjudication by charity, in whichever direction it lands.
And the clause carries its own rider: *which would mean the per-class rates do
not carry across and S-c will already have fired*. That condition **occurred** —
S-c is refuted on four of its six eligible classes — so both halves of the row
point the same way, and the verdict rests on the row rather than on a choice
between its halves. A reader who takes *far from that* as the operative line
should read this as S-d not refuted, and everything needed to do so is above and
in the record under `predictions["S-d"]["readings"]`.

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
identical wherever cases actually arrive, does not occur at this scale.
Predicted *under 1%*, measured **0.10%**.

**But read the second clause at the resolution the surface has.** The minimum is
**2 cases of 2000**, and on a surface of 2000 cases **one case is 0.05%**. The 1%
line the prediction drew is 20 cases; the measurement cleared it by **18 cases**,
and the closest pair of end orders is **two arriving tickets away** from being
the same machine in deployment — which is the finding S-e itself names as the
large one, missed by a margin that counts in single cases. It is coarser still
than that: the 2000 draws touch 1,743 distinct cases, so two disagreements need
not even be two distinct cases. On corpus test the minimum is 1 case of 995,
which is the smallest a non-zero distance can be.

**The pair is identified, by a re-run authorized for that and nothing else.**
The full run stored the minimum and not the pair, the 257-order matrices being
summarized rather than kept. Sergi lifted the no-re-run rule on 2026-08-15,
**after these verdicts existed**, to recover an index — a pointer into a set
already measured, not a quantity. The condition was that nothing already
published may move, and nothing did: both gates passed again, parity 31/31 and
the G2 census, and all twelve published set summaries and both minima reproduced
exactly before anything was written. The record says the same under
`authorization`, with its own `_env_amendment`.

**It is one pair, not two.** End orders **47 and 87** of split 0's 257 starts
attain the minimum on *both* corpus surfaces. Nothing guaranteed that — the two
argmins are over different surfaces and could have been different pairs.

**And the two cases are two distinct tickets, not one drawn twice**, which is
the question this section raised:

| | true class | order 47 | order 87 |
|---|---|---|---|
| corpus case 577 | `T2_TECHNICAL` | `SECURITY_INCIDENT` | `SELF_SERVICE_DEFLECT` |
| corpus case 854 | `SELF_SERVICE_DEFLECT` | `SELF_SERVICE_DEFLECT` | `BILLING_SPECIALIST` |

On corpus test only 854 survives — 577 sits in the fitted half — which is why
that surface's minimum is 1 case, the smallest a non-zero distance can be.

**Three things read off it.** *One of the two cases is two ways of being wrong*:
on 577 neither order is right, so half of what separates the closest pair of
machines in this material is not a difference in quality at all. *The pair
closest on arrivals is not the pair closest on the space*: these two differ on
**6,180 cases, 4.60%** of the uniform surface, while the minimum over the same
32,896 pairs there is 2,615 — being nearly indistinguishable in deployment puts
a pair nowhere near the bottom of the other surface's ranking, which is S-c's
point at the level of a single pair. And *Q-e at its extreme*: **99.13% of the
577 rules sit at a different index** between two orders that decide the same
thing on 1,998 of 2,000 arriving tickets.

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
| **S-b** | That rate above the 15.2% of a pure reweighting. | **REFUTED**: 5.75%, below the 15.2% written and below the 11.67% reconstructed. Its stated mechanism is confirmed, by a post-hoc measurement, and does not produce the effect. |
| **S-c** | Per-class rates preserved to ±30% relative. | **REFUTED**: 4 of 6 eligible classes outside, from −81.6% to +165.2%. |
| **S-d** | `SECURITY_INCIDENT`'s share of the disagreement under 3%. | **REFUTED on the stated value**: 4.57%, against 2.67% modelled and 57.5% on the space. Its refutation clause — *anything far from that* — is not a number; both readings are published and the row's own rider fired. |
| **S-e** | No pair identical on the corpus and different on the space; pairwise minimum under 1%. | **HOLDS**: zero such pairs, minimum 0.10% — two cases of 2000, clearing a 20-case line by 18. The pair is orders 47 and 87, two distinct tickets, 6,180 cases apart over the space. |
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
gate, and the parity gate is exact on all 31 rows. **That digest covers code
written after the six verdicts existed** — `competition()`, added because S-b
had failed — which is why the census it produces is marked post hoc above and in
the record's `post_hoc` field.

**One authorized re-run, 397 s, after all of the above.** It regenerated down
the same path, passed both gates again and located S-e's minimum pairs; it
carries its own `_env_amendment` in the record, beside the `_env` of the run
that produced the figures. It wrote two things into the file — the pair
identities and the authorization — and changed nothing else, which the mode
verified before writing rather than after.

**The record was annotated by hand after the run, with strings and nothing
else.** `truth_provenance`, `post_hoc`, `sets_measured`, `record_annotations`,
S-b's `competition_is_post_hoc`, S-d's `clause_verbatim` and `readings`, and a
rewrite of S-d's `refutation_note`, which had paraphrased a clause that needed
quoting. No measured value was touched and the claim is checkable rather than
asserted: `git diff b964823 -- results3/order_metrics_corpus.json` is those
string additions and nothing else. The module holds the same text as constants
and emits it, so a fresh run would reproduce the file — except its `code_digest`,
which identifies the code as it stood when the numbers were computed.

---

## What the corpus part does not settle

- ~~**Why 3.5×.** Not scarcity of contested material — the corpus carries 74%
  more live conflicting pairs per case — and only about a tenth of it is
  fitting. What accounts for the rest is unmeasured, and this record declines to
  invent it after the fact. **The rank part states the same gap as a ratio**:
  0.28 measured against the 0.57 reweighting predicts, an overestimate of 2.03×,
  which is the same 2.03× as 11.67% against 5.75% because the two differ only by
  a multiplication by the space's pooled rate. One open question in two units,
  not two.~~
  **Answered 2026-08-16**, in part four of this record: it is **which points
  arrive, not how often each is drawn**. The 2,000 draws reach 1.30% of the
  space, and reweighting rebuilt on the rate over just those points gives
  0.05828 against the measured 0.057472 — 98.6% of the deficit is that step
  alone. What replaces this item is narrower and is in part four's own list: why
  disagreement concentrates in the part of the space arrivals never visit.
- **Whether "corpus" means deployment.** It is a modelled arrival distribution
  with a seed, not observed traffic. Everything here says the two surfaces
  disagree; nothing here says the corpus is the right one.
- **Where S-b's 15.2% came from.** Nothing in this run reconstructs it, and the
  prediction is not edited to match what does.
- **The other three splits at full supervision.** Splits 0 and 4 are measured
  because they are the two `start_budget_check` saw the train score move on.
  Whether the 3.5× is stable across the other three is not known.
- ~~Which pair attains S-e's minimum, and what it does on the space.~~
  **Answered 2026-08-15** by the authorized re-run: orders 47 and 87, on both
  corpus surfaces, 6,180 cases apart over the space. What that leaves open is
  the converse, which is not the same question and was not measured: **whether
  the pair closest on the SPACE is anywhere near closest on the corpus.** The
  2,615-case minimum belongs to some other pair, and where that pair sits among
  arrivals is unknown.

---

# Rank transfer — R-a to R-d

August 15, 2026. **This part owns the figures below.** It is not a third
measurement: it is a **join of the two records above**, over the 2,080 pairs of
the 65 end orders of split 0, matched by `(i, j)`. No search, no regeneration,
no new instrument, zero API calls, **0.07 s**. Both records were opened read
only and neither was rewritten. Prediction: `IDEAS.md`, the entry *Whether the
space can RANK two orders when it cannot rate them*, committed alone and without
code before any of these numbers existed — commit `73719ec`, landed in **PR
#22**; these figures arrived in **PR #23**, which is what makes the order of the
two checkable in the log rather than asserted here. Record:
[`rank_transfer.json`](rank_transfer.json).

**The question the two parts above left open.** The corpus part settled that the
*level* does not transfer — 5.75% against 20.35% — and that *where* the
disagreement falls does not either. Neither implies anything about the
**ordering**: a rank is invariant to any monotone transformation, so a level
falling by 3.5× is perfectly compatible with an ordering preserved exactly. What
turns on it is whether `order_metrics.json` can be read comparatively at all —
*this pair is further apart than that one* — once the surface is wrong for
deployment.

**It cannot.** ρ = 0.34.

---

## The gate

Blocking, and it is this question's parity gate. The three `(i, j)` key sets are
**identical**, 2,080 keys each, no duplicates, indices 0..64, `i < j` throughout,
and 2080 = 65·64/2. And `resumen()` over each matrix's own stored rates
reproduces **exactly** the summary that matrix's own record already publishes
for the set — all three.

**The gate was first run before the prediction was committed, and that does not
contaminate it.** It reproduces summaries already published and computes no
quantity R-a to R-d adjudicates on: no Spearman, no decile overlap, no ratio
quantile, no argmin. What it can establish is only that the join is over the
rows it claims — which is a fact about the two files, not about an answer. It
was re-run in the run that produced these figures, and that is the result the
record carries.

---

## The predictions of `IDEAS.md`, one by one

| # | verdict | measured |
|---|---|---|
| **R-a** | **REFUTED, and not narrowly** | Spearman between the corpus-full rate and the space rate over the 2,080 pairs: **0.3364**. Predicted band 0.70–0.93, refutation line 0.55 — it lands **0.21 below the refutation line** and less than half way to the band. Corpus test: 0.3325. |
| **R-b** | **NEITHER**, and 3.4 pairs from refuted | **45 of 208, 21.6%**. The band was 35–70% and the refutation line 20%, so it falls in the dead zone between them. Robust to the tie-break: over every way of breaking it the overlap is 43 to 45, **20.7% to 21.6%**, never reaching the band. |
| **R-c** | **HOLDS** | The per-pair ratio corpus/space has **p75/p25 = 1.880**, against a threshold of 1.30 and a refutation line at 1.15. It is not one factor by a wide margin: the ratio runs from **0.047 to 1.767**, a factor of **37** end to end. |
| **R-d** | *reported, not adjudicated* | The space's closest pair, **(53, 56)** at 3.59%, ranks **1207 of 2080** on the corpus. The corpus's closest pair, **(22, 43)** at 0.85%, ranks **111 of 2080** on the space. |

### R-a, and why ties are not the explanation

The entry declares that the drafter checked the tie load and concluded it does
not cap the band. That claim is now checkable rather than inherited:

| surface | distinct rate values | largest tie group | mean group size | values appearing once |
|---|---|---|---|---|
| exhaustive space | 1,834 | 3 | 1.13 | 1,613 |
| corpus, all 2000 | 207 | 27 | 10.05 | 21 |
| corpus test half | 119 | 44 | 17.48 | 9 |

The corpus rate is a count out of 2,000, so it is coarse by construction, and
2,080 pairs land on 207 values. That could in principle cap a rank correlation,
so the ceiling is measured: pairing the two multisets comonotonically — k-th
smallest with k-th smallest, which no arrangement beats — gives a maximum
attainable Spearman of **1.0000**, i.e. **an attenuation of at most 5×10⁻⁵**.
That bound carries the instrument's own resolution: `order_metrics_run.spearman`
rounds to four decimals, so 1.0000 means ≥ 0.99995, and resolving it finer would
take a second rank correlation — the instrument change this record declines to
make halfway through. It does not need resolving. **Ties cost at most 5×10⁻⁵ and
the measurement falls 0.66 short of the ceiling.**

### R-b, and where the arbitrariness actually is

208 is exactly a tenth of 2,080, and the closest pairs are the deployment-
relevant end: they are the pairs a reader would call interchangeable. Of the 208
closest on the space, **45** are among the 208 closest on the corpus.

The boundary is worth stating because the set could have been partly arbitrary
and is not. On the space the 208th value is attained by **one** pair, so that
side is exact. On the corpus the boundary rate 0.026 is shared by **14** pairs
of which 5 fit, so 9 were excluded by the declared `(i, j)` tie-break. Varying
that tie-break over every possibility moves the overlap only between **43 and
45** — 20.7% to 21.6% — so the verdict does not depend on it. On corpus test the
same bounds are 41 to 47, 19.7% to 22.6%, which straddles the 20% line: **there**
the tie-break would decide between REFUTED and NEITHER, and it is one more
reason that surface is reported and does not adjudicate.

### R-c, and what a common factor would have meant

Refuting R-c would have meant the change of surface is one multiplication for
every pair alike. It is not, and not by a little: **p75/p25 = 1.880**, and the
extremes run from 0.047 to 1.767 — one pair disagrees on 1.77× as much of the
corpus as of the space, another on a twenty-first of it. The pooled ratio is
0.282 and the median per-pair ratio 0.292, so the *centre* is stable while the
per-pair spread is enormous. That is the same shape S-c found per class, now per
pair, and it is the mechanism R-a's refutation needed: pairs differ from one
another in **where** they disagree, so re-weighting the surface re-ranks them.

**The centre is stable and it is also wrong by a factor of two**, which this
section reported without saying. Against the pooled 0.2825 and the median
per-pair 0.2920, class reweighting predicts **0.5735** — 0.1167 over 0.203451,
both already published. It **overestimates the centre by 2.03×**.

**And that is not a second open question beside S-b's. It is the same one in
other units.** Multiply either column back by the space's pooled rate:

| | ratio to the space | level on the corpus |
|---|---|---|
| class reweighting predicts | 0.5735 | **0.1167** — the figure S-b named and did not reach |
| measured | 0.2825 | **0.0575** |
| overestimate | **2.03×** | **2.03×** |

The factor is *identical* in the two columns because the space rate cancels:
0.5735 × 0.203451 = 0.1167 and 0.2825 × 0.203451 = 0.0575, so dividing by it is
a bijection between the two readings. **Why is the common factor 0.28 rather than
0.57** and **why did the corpus rate come out at 5.75% instead of the 11.67%
reweighting predicted** are one question asked twice, once as a ratio and once as
a level. That is arithmetic on figures already published, not a new measurement.

What R-c adds to it is that the gap is not an artefact of averaging: the centre
that reweighting misses by 2.03× is *stable* across pairs, while the spread
around it — p75/p25 = 1.880, extremes a factor of 37 — is a separate fact and is
what re-ranks them. A per-class account that produced 0.28 would close the level
and the ratio at once, and would still owe an explanation of the spread.

### R-d, an anecdote in both directions

One draw of 2,080 either way, and the two directions do not behave alike.

- **Space → corpus.** The most interchangeable pair on the space, **(53, 56)** at
  3.59% of 134,400, sits at **rank 1207 of 2080** on the corpus, with 1192 pairs
  strictly below it. Its corpus rate, 6.35%, is *above* the corpus median of
  5.90%. The pair the space nominates as the two orders hardest to tell apart is,
  on arrivals, slightly **worse** than typical.
- **Corpus → space.** The most interchangeable pair on the corpus, **(22, 43)**
  at 0.85% — 17 tickets of 2,000 — ranks **111 of 2080** on the space, inside the
  top 5.3%. It is also corpus test's minimum.

So the failure is not symmetric on this one draw: a pair that is close on
arrivals tends to be close as a function, while a pair close as a function says
little about arrivals. Two anecdotes are not a distribution, which is exactly why
R-d was written as reported and not adjudicated.

---

## The drafter's own arithmetic, checked

The entry argues the correlation must be high: which particular cases were drawn
contributes about **9%** relative, against a between-pair spread of about **42%**,
so idiosyncratic draw cannot be what lowers it. **Both halves check out on the
scale the entry used, its comparison was homogeneous, and the conclusion still
does not follow.**

| quantity | scale | value |
|---|---|---|
| draw noise, the entry's 9% | sd / mean | **9.06%** — closed form √((1−p)/np) at the pooled rate 0.0575 over 2,000 draws, not a measurement |
| between-pair spread, **the entry's 42%** | sd / mean, as IQR/1.349 over the mean | **41.92%** on the corpus |
| the same spread, another scale | IQR / median | **55.08%** on the corpus |
| the space, on that second scale | IQR / median | **43.83%** |
| the space, on the entry's scale | sd / mean | **31.49%** |

**What the entry did not do is declare its scale — it did not cite the wrong
surface.** Its 42% is the coefficient of variation *over the corpus*, IQR/1.349
over the mean, and that is the same normalization as its 9%: both are a standard
deviation over a mean, and the mean of the per-pair rates is exactly the pooled
rate, since every pair divides by the same 2,000 cases. So the comparison it
made was apples to apples, 9.06% against 41.92%, a ratio of 4.6.

The second row of that table is a **different scale**, 1.31× larger here — which
is 1.349 times the set's mean over its median — and the resemblance between the
space's 43.83% on it and the corpus's 41.92% on the entry's scale is a
**coincidence of two scales on two surfaces**: on the entry's own scale the space
gives 31.49%, so 42% could not have been a space figure. An earlier draft of this
section read it as one, which was wrong and is corrected here rather than
quietly.

**The conclusion still does not follow, and the reason is mine rather than the
entry's.** Sampling being small against between-pair spread would settle it only
if each pair drew its own corpus. It does not: all 2,080 pairs are scored on the
**same** 2,000 tickets, so what the corpus does to them is a single common
re-weighting, not 2,080 independent draws. A common re-weighting moves pairs
together — and cancels further in a rank than in a level — so the drafter's
decomposition measures a quantity that does not enter the question it was raised
to answer.

**So the arithmetic is right, and the inference it supports is not**, and the
entry itself says what that leaves: *what can lower the correlation is pairs
differing from each other in where they disagree, and these 65 orders come from
one neighbourhood over one training half at similar scores, which argues they do
not differ much*. They differ much. R-a's own text calls refutation below 0.55
**the informative outcome** — *it would mean the pairs specialize far more than
their common origin suggests* — and that is the outcome.

---

## What this changes elsewhere

**The comparative readings of `order_metrics.json` do not survive to
deployment.** That record is cited to say one pair of orders is further apart
than another — Q-a's 11,240 cases, the factor of 21 between the closest and
furthest pair. Those remain true *of the space*. What is now measured is that
the space's ordering of pairs carries a Spearman of 0.34 to the arrival
distribution, and that its most interchangeable pair is mid-table there. **A
reader who used the space record to decide which two orders are safest to swap
was reading the wrong surface, and not only by a constant.**

**It is the strong form of the reservation, and it is now the measured one.**
The corpus part closed *what this does not settle* on the level and on the
composition. This closes it on the ordering, which was the last reading under
which the space figures could have been used comparatively for deployment.

**What it does not touch.** Every space figure is what it always was, measured on
the surface it names. Nothing above is withdrawn, and the space remains the
surface that answers *is this order the policy* — a question about the function,
where the arrival distribution has no standing.

---

## The register, third part

| id | finding | status |
|---|---|---|
| **R-a** | Spearman corpus vs space over the 2,080 pairs, between 0.70 and 0.93. | **REFUTED**: 0.3364, below the 0.55 line. Ties cap it by at most 5×10⁻⁵, so that is not the explanation. |
| **R-b** | Of the 208 closest on the space, 35–70% among the 208 closest on the corpus. | **NEITHER**: 45 of 208, 21.6%, in the dead zone between band and refutation. Robust to the tie-break, 20.7–21.6%. |
| **R-c** | The per-pair ratio is not a common factor: p75/p25 above 1.30. | **HOLDS**: 1.880, extremes 0.047 to 1.767. |
| **R-d** | Reported, not adjudicated. | Space's closest pair ranks 1207/2080 on the corpus; the corpus's ranks 111/2080 on the space. |

---

## What the rank part does not settle

- **The 257-order sets.** Both records summarize those matrices rather than
  store them, so this join is over the 65-order set of split 0 only. Whether
  ρ = 0.34 is stable at 257 orders, or on split 4, would cost a regeneration and
  was not done.
- **Whether 0.34 is a lot or a little for a deployment decision.** It is far
  below what was predicted and clearly above zero; the two surfaces agree more
  than chance and much less than a reader of either would assume. What margin a
  real decision needs is not a question this material answers.
- ~~**Why the centre is 0.28 and not the 0.57 reweighting predicts — which is
  S-b's gap and not a second one.** The two differ by a multiplication by the
  space's pooled rate and by nothing else, so part two's *Why 3.5×* and this are
  a single open question: an answer to either is an answer to both, and the
  record should not be read as carrying two.~~
  **Answered 2026-08-16**, in part four, and as one item because it was one:
  reweighting on the rate over the touched points alone gives a ratio of 0.2865
  against the measured 0.2825, where reweighting on the whole space gave 0.5735.
- **Why the pairs specialize around that centre.** A separate question from the
  one above, and the one R-c opens on its own: the per-pair ratio spans a factor
  of 37, and nothing here says what distinguishes a pair whose ratio is 0.05 from
  one whose ratio is 1.77. The class-level account of S-c is the obvious place to
  look and was not looked at.
  **Narrowed 2026-08-16, not closed** (part four, C-d): the spread lives at the
  same step as the level. On a log scale 89% of it is already there in
  `touched/space`, p75/p25 = 1.754 of the 1.880, while the multiplicity step
  contributes 1.066. So the question is why pairs differ from each other over
  *which 1.3% of the space is sampled*, and `touched/space` still spans a factor
  of 30.

---

# The touched points — C-a to C-d

August 16, 2026. **This part of the record owns the touched-point figures.**
Same 577 rules, same 65 end orders of split 0, same 2,080 pairs, same
instrument: what changes is that the exhaustive space is restricted to the
**1,743 points the corpus actually reaches**. Prediction: `IDEAS.md`, the entry
*The whole 2.03× gap is one class, and the question is why its arrivals are
cleaner*, drafted, signed and committed before `touched(c)` existed for any
class. These figures arrived afterwards, in **PR #27**, which is what makes the
order of the two checkable in the log rather than asserted here. Record:
[`order_metrics_touched.json`](order_metrics_touched.json). Zero API calls,
343 s.

**Two hold, one lands in its dead zone, one is reported.** And the open question
parts two and three both ended on — *why 3.5×*, *why 0.28 and not 0.57* — is
answered: **it is which points arrive, not how often each is drawn.**

---

## The two steps, and why only one of them was unmeasured

Class reweighting corrects for how often a class arrives and assumes the rate
*within* a class transfers. It does not, and `R-c` measured the size of the
failure without locating it: the centre of the corpus/space ratio is 0.2825
where reweighting predicts 0.5735, an overestimate of **2.03×** — the same 2.03×
as 11.67% against 5.75%, in other units.

The corpus reaches the space twice over, and the two can be separated:

| step | what it is | measured before today |
|---|---|---|
| **which** points arrive | the 2,000 draws land on 1,743 of the 134,400 points, **1.30%** of the space, concentrated on common attribute combinations | **no** |
| **how often** each is drawn | the multiplicity of those 1,743 points: 1,538 drawn once, 165 twice, 31 three times, 7 four times, one five and one six | yes — it is the difference between `touched` and `arrivals` |

So three rates per class over the same 2,080 pairs, and only the middle one is
new:

| rate | surface | denominator | provenance |
|---|---|---|---|
| `all(c)` | the whole space | every point of the class | **published**, first part of this record |
| `touched(c)` | the touched points | the class's points the corpus reaches, **each counted once** | **new** |
| `arrivals(c)` | the corpus | the class's 2,000 draws, **with multiplicity** | **published**, second part of this record |

**The corpus contributes a mask and nothing else.** Every rate above is computed
in `Space`'s bit convention, case k at bit n−1−k, from
`order_search_ls.space_truth_masks` and the space pools. `arrivals(c)` is *read*
from [`order_metrics_corpus.json`](order_metrics_corpus.json) rather than
recomputed, so no corpus mask is built in this run at all and the two
conventions never meet — which is why this question is structurally safer than
the corpus one, where the whole per-class apparatus had to be rebuilt in the
other convention.

## The gates, and there are four

**PARITY: 31 of 31 rows exact**, the same gate and the same two records as parts
one and two — 883 / 0.8786 / 0.8472 / 0.6033 at split 0 and 65 starts, 884 /
0.8796 / 0.8442 / 0.5776 at 257, all six budget rows, and 25 of 25 band cells.
**No new search**: every order comes out of `run_full_supervision` and
`run_band_1pct` of `order_metrics_run.py`, imported and called unchanged.

**THE PUBLISHED `all(c)`: eight of eight identical**, and the overall rate with
them — 0.203451. Parity compares four scores per row; this compares the
per-class behaviour the question is actually about, and it is the gate the entry
named as its second invariant.

**THE MATRIX: 2,080 of 2,080 per-pair distances identical** to
`order_metrics.json::pairs_split0_starts65`, joined on `(i, j)` and never on
position. It is what makes the per-pair half of C-d a re-weighting of the
published matrix rather than a second, unrelated one.

**THE MASK: 1,743 bits exactly**, the figure part two publishes for the distinct
cases the 2,000 draws touch; every corpus case maps into the enumeration
(a case outside it raises rather than being dropped); and the class masks
partition both the space and the touched mask.

**One caveat about that last gate, stated rather than left implicit.**
Partitioning does **not** catch a mask built in the wrong convention:
intersecting a partition with any mask partitions that mask, so the reversed
mask would have 1,743 bits and eight class masks summing to 1,743 too, and every
figure below would be noise of the right shape. What catches it is a count that
has to agree by two routes — `(truth_space[c] & touched).bit_count()` against
the number of **distinct corpus cases labelled c**, the first from the oracle's
labelling of the space and the second from the corpus label list. That is pinned
in [`tests/test_order_metrics_touched.py`](../tests/test_order_metrics_touched.py),
which also **shows** the reversed convention failing it rather than assuming it
would.

---

## The three rates, by class

Ordered by each class's contribution to the 0.059213 the reweighting
overestimates by. `f(c) = (all − touched) / (all − arrivals)` is the fraction of
the class's fall carried by *which* points arrive.

| class | space n | touched n | corpus n | p(c) | `all(c)` | `touched(c)` | `arrivals(c)` | `f(c)` | share of the deficit |
|---|---|---|---|---|---|---|---|---|---|
| `T2_TECHNICAL` | 36,720 | 661 | 726 | 0.3630 | 0.196859 | **0.038432** | 0.036190 | **0.986** | **98.5%** |
| `T3_ENGINEERING` | 8,180 | 105 | 117 | 0.0585 | 0.094743 | 0.060449 | 0.054249 | 0.847 | 4.0% |
| `ACCOUNT_MANAGER` | 16,440 | 108 | 109 | 0.0545 | 0.091590 | 0.050592 | 0.053110 | **1.065** | 3.5% |
| `T1_GENERAL` | 5,220 | 229 | 255 | 0.1275 | 0.042567 | 0.031030 | 0.029842 | 0.907 | 2.7% |
| `SECURITY_INCIDENT` | 50,400 | 20 | 20 | 0.0100 | 0.312125 | 0.262644 | 0.262644 | **1.000** | 0.8% |
| `ONCALL_ESCALATION` | 6,300 | 7 | 7 | 0.0035 | 0.217836 | 0.191003 | 0.191003 | **1.000** | 0.2% |
| `SELF_SERVICE_DEFLECT` | 4,300 | 379 | 495 | 0.2475 | 0.094261 | 0.104436 | 0.103952 | 1.050 | −4.1% |
| `BILLING_SPECIALIST` | 6,840 | 234 | 271 | 0.1355 | 0.015135 | 0.036428 | 0.040140 | 0.852 | −5.7% |

**The entry's own arithmetic reproduces exactly.** It declared, as what the
drafter had already seen, the eight `arrivals/all` ratios (0.184 for
`T2_TECHNICAL` through 2.652 for `BILLING_SPECIALIST`) and `T2_TECHNICAL` at
**98.5%** of the deficit. Recomputed here from the regenerated orders: 98.5%,
and every ratio to the digit it gave. Nothing in this run contradicts what the
entry says it derived.

**The headline is one line of that table.** `T2_TECHNICAL` falls from 19.69% of
its space cases to 3.62% of its arrivals, and **0.038432** of that fall is
already there when the only thing that has changed is *which* points are
counted, each exactly once. Of the 0.059213 the reweighting overestimates by,
**0.058406 — 98.6% — is the which-points step**, and 0.000808 is multiplicity.

## The predictions of `IDEAS.md`, one by one

| # | verdict | measured |
|---|---|---|
| **C-a** | **NEITHER** — above its band, inside its refutation line | `f(T2_TECHNICAL)` = **0.986**, against a band of 0.60–0.95 and refutation outside 0.40–1.10. The direction is the one the entry's own calibration note suspected: the band was too *low*. |
| **C-b** | **HOLDS**, 8 of 8 | The sign of `touched(c) − all(c)` matches the sign of `arrivals(c) − all(c)` in **every** class, against a threshold of 6. `BILLING_SPECIALIST` and `SELF_SERVICE_DEFLECT`, the two the row names, both go **up** as it required. Two of the eight matches are degenerate — see below — and it is 6 of 6 without them. |
| **C-c** | **HOLDS** | Reweighting rebuilt with `touched(c)`: **0.05828**, against a band of 0.043–0.072 and the measured corpus rate of 0.057472 — **+1.4% relative**. The original reweighting gave 0.116685. |
| **C-d** | *reported* | Per-pair ratio `touched/space`: p75/p25 = **1.754**, against R-c's **1.880** for `arrivals/space`. The residual step `arrivals/touched` gives **1.066**. The spread does not shrink; it moves to the same step the level did. |

### C-a, and a band that could not accommodate its own hypothesis

`f(T2_TECHNICAL) = 0.986` says the fall is **essentially all** which-points. The
row asked for 0.60–0.95 and refuted outside 0.40–1.10, so the measurement sits
in the dead zone between them, 0.036 above the band.

**Worth seeing why, because it is a fact about how the row was drawn and not a
reinterpretation of it.** The hypothesis the entry states is that reweighting
overestimates *because* the corpus touches concentrated points; the strongest
form of that hypothesis is that multiplicity contributes nothing at all, which
is `f = 1`. That value is **outside the band as written**. A prediction whose own
mechanism, taken to completion, cannot make it hold is a prediction whose band
was drawn short — and the entry's calibration note said so in advance, in the
opposite direction from its four losses: *this band may be too low*. It was, by
one dead zone. **That is one instance and not a trend**, exactly as the note
itself insists; the band is not edited, and the verdict is NEITHER.

**Three classes give `f > 1`,** which the row explicitly allowed for — *nothing
forces `touched` to sit between the other two, so `f` outside `[0, 1]` is
possible and is a result, not an error*. `ACCOUNT_MANAGER` is the clearest:
which-points takes it from 0.0916 to 0.0506, *below* its arrival rate of 0.0531,
and multiplicity moves it back up. Its 109 draws land on 108 distinct points, so
**one ticket drawn twice** is what that reversal is made of. At 109 corpus cases
a single duplicate is about 1% of the class's weight, and it is enough to put `f`
on the far side of 1.

### C-b, and the two classes where the split is degenerate

Eight of eight, and the two the row names as the test of whether the story is
about which points at all — `BILLING_SPECIALIST` at ×2.65 and
`SELF_SERVICE_DEFLECT` at ×1.10 — both rise under `touched` as required:
0.0151 → 0.0364 and 0.0943 → 0.1044. The mechanism is general, not a fact about
`T2_TECHNICAL`.

**Two of the eight matches are free, and are reported as such.**
`SECURITY_INCIDENT` draws 20 tickets onto 20 distinct points and
`ONCALL_ESCALATION` 7 onto 7, so for those two classes the multiplicity step is
the identity map: `touched(c) = arrivals(c)` **exactly**, 0.262644 and 0.191003,
and their signs cannot fail to match. Their `f = 1.000` is arithmetic, not
measurement. Excluding both, C-b is **6 of 6** — still above its threshold of 6
and far above its refutation line of 4 — so the row survives the strictest
reading of itself. It is worth knowing which classes carry it, though: the two
scarcest, and the two rung 1 resolved 0 of 17 and 0 of 7 times, contribute
nothing to it.

### C-c, and the gap that closes with it

**0.05828 against a measured 0.057472.** Reweighting with `touched(c)` in place
of `all(c)` — the same class weights, the same eight classes, one column
swapped — reconstructs the corpus rate to within **+1.4% relative**, where the
original reweighting was out by **+103%**.

| | ratio to the space rate | level on the corpus |
|---|---|---|
| class reweighting on `all(c)` | 0.5735 | **0.116685** |
| class reweighting on `touched(c)` | 0.2865 | **0.05828** |
| measured on arrivals | 0.2825 | **0.057472** |

The weights are the right ones by two published identities, checked rather than
asserted: the same weights on `arrivals(c)` give back **0.057472**, the pooled
corpus rate, and on `all(c)` they give back **0.116685**, the figure part two
publishes. So the whole of the 2.03× is one modelling error, and it is not about
class frequencies: **it is that the rate within a class does not transfer
because the corpus samples 1.3% of the class, not a uniform slice of it.**

**And the unweighted figure says the same thing more bluntly.** Pooled over the
1,743 touched points with every point counted **once**, the 2,080 pairs disagree
on **5.68%** — against 5.75% on the arrival distribution and 20.35% on the
space. The per-pair median is 5.74% against the corpus's 5.90% and the space's
19.72%. Restricting the surface to the touched points reproduces the corpus
level *before any weighting is applied at all*.

### C-d, reported: the spread moves, it does not shrink

R-c left a second question beside the level — the per-pair ratio spans a factor
of 37, and nothing said what distinguishes a pair whose ratio is 0.05 from one
whose ratio is 1.77. C-d asks whether the same explanation covers it.

| per-pair ratio | min | p25 | median | p75 | max | p75/p25 | max/min |
|---|---|---|---|---|---|---|---|
| `touched / space` — **which points** | 0.0544 | 0.2039 | 0.2849 | 0.3576 | 1.6284 | **1.754** | 29.96 |
| `arrivals / space` — R-c's own, reproduced | 0.0474 | 0.1971 | 0.2920 | 0.3705 | 1.7670 | **1.880** | 37.30 |
| `arrivals / touched` — **how often** | 0.8715 | 0.9756 | 1.0129 | 1.0395 | 1.1494 | **1.066** | 1.32 |

**R-c's row reproduces bit for bit** — every quantile of `arrivals/space`
matches the published one to the last decimal, which is the check that this
file's ratio instrument is the one that produced 1.880.

**No threshold is applied to any of this; C-d adjudicates nothing.** What it
says is that the spread is **localized, not explained**: on a log scale
**89%** of it is already present at the which-points step, and the multiplicity
step contributes a p75/p25 of 1.066 across all 2,080 pairs. So the answer to
*does the same explanation cover the spread* is that the spread lives at the
same step as the level — which narrows R-c's open question from *why do pairs
specialize between the two surfaces* to *why do pairs specialize over which
1.3% of the space is sampled*. It does not close it: `touched/space` still runs
from 0.054 to 1.63, a factor of 30, and nothing here says what distinguishes
those pairs.

**And no pair collapses.** Of the 2,080, **zero** disagree on nothing over the
touched points; the minimum is **17 cases of 1,743** and the maximum 213. That
is S-e's question asked of this surface, and it comes out the same way the
corpus answered it.

---

## What this settles for the standing question

**The open question parts two and three both ended on is answered.** *Why 3.5×*
and *why 0.28 and not the 0.57 reweighting predicts* are one question in two
units, and the answer is **which points arrive**: 98.6% of the deficit, and a
reconstruction accurate to 1.4% relative once `all(c)` is replaced by
`touched(c)`. The residual — the 1.4% multiplicity carries and the 1.4% C-c
still misses — is the same order as the arithmetic's own resolution and is not a
second mechanism.

**What it does not do is rehabilitate the space as a deployment surface.**
Nothing here recovers a per-class account that turns space figures into corpus
figures, because the correction is not per class: `touched(c)` is a measurement
over a 1.3% sample of each class that only the corpus can identify. A reader
holding `order_metrics.json` and the class frequencies still cannot get to
5.75%; they need the mask.

## What this changes elsewhere

**Part two's *Why 3.5×* closes, and part three's *why 0.28 and not 0.57* closes
with it** — they were one item and are struck as one. What replaces them is
narrower and is entered in the register below: why disagreement concentrates in
the part of the space the corpus does *not* touch, and why pairs differ from
each other in that.

**Part two's reading of S-c is confirmed and sharpened.** S-c's refutation
clause said that failing would mean *the mix of cases within each class governs
too*. It does, and the mix is now named: not an arbitrary re-weighting inside
the class, but the 1.3% of it a long-tailed sampler reaches. `T2_TECHNICAL`
disagreeing on 19.69% of its 36,720 space points and 3.84% of the 661 the corpus
reaches is the whole of that finding in one row.

**Nothing above is withdrawn.** Every space figure is what it always was, on the
surface it names.

---

## The register, fourth part

| id | finding | status |
|---|---|---|
| **C-a** | `f(T2_TECHNICAL)`, the fraction of the fall carried by which points, between 0.60 and 0.95. | **NEITHER**: 0.986, above the band and inside the 1.10 refutation line. The hypothesis' own limit, `f = 1`, was outside the band as written. |
| **C-b** | The signs of `touched − all` and `arrivals − all` agree in at least 6 of 8 classes. | **HOLDS**: 8 of 8, and 6 of 6 excluding the two classes where `touched = arrivals` identically. The two classes the row names both rise. |
| **C-c** | Reweighting on `touched(c)` between 0.043 and 0.072. | **HOLDS**: 0.05828 against a measured 0.057472, +1.4% relative, where reweighting on `all(c)` was +103%. |
| **C-d** | Reported, not adjudicated. | `touched/space` p75/p25 = 1.754 against R-c's 1.880; `arrivals/touched` = 1.066. 89% of the spread on a log scale is already at the which-points step. |
| **C-e** | *(not predicted)* Whether the unweighted touched surface reproduces the corpus level on its own. | **IT DOES**: 5.68% pooled over the 1,743 points, each counted once, against 5.75% on 2,000 draws — before any class weighting. |

**The stopping condition the entry signed with the prediction, quoted verbatim
and applied by nobody here:**

> **The stopping condition for this thread.** If C-a, C-b and C-c all hold, the
> audit thread closes and the next entries go back to the domain. Any other
> outcome — a refutation, or a row landing between its band and its refutation
> line — permits one successor entry and no more, and that successor carries no
> stopping condition of its own because this one is it.

C-b and C-c hold; C-a landed between its band and its refutation line. What
follows from that is not this record's to decide, and no successor entry is
written here.

## Provenance of the touched part

**Cost: 343 s in one process, zero API calls.** Regeneration is 338 s of it
(135.6 s and 117.0 s for the two 257-start searches, 85.3 s for the whole 1%
band); the measuring is under 5 s, because the pairwise sweep runs once over 65
orders rather than 257 and no Kendall tau is computed.

**`code_dirty: false` and `git_dirty: false`** — the first record in this thread
to run on a clean tree. The instrument was committed **before the run**, in its
own commit carrying no figure, which is why. What identifies the code is
`code_digest 59d413ab37c58038`; what identifies the **orders** is neither that
nor the commit, it is the parity gate, and the parity gate is exact on all 31
rows.

**The `_env.git_commit` in the record is a branch commit that the merge
rewrites.** `main` is protected and merges by rebase, so the SHA the run stamped
does not survive onto `main`. That is why this section cites **PR #27** and no
SHA: the commit in the record identifies the tree the figures were computed on,
and the PR is what a reader can follow.

## What the touched part does not settle

- **Why disagreement lives where the corpus does not go.** This is the question
  the answer creates, and it is now the sharp one: two orders disagree on 19.69%
  of `T2_TECHNICAL`'s space points and 3.84% of the 661 the corpus reaches, so
  the disagreement is concentrated in the 98% of the class arrivals never
  visit. What distinguishes those points — which attributes, which rules
  competing over them — is not measured here.
  **Narrowed 2026-08-16 by part five, and one level down.** It is not that the
  rules whose territories change hands are the rarely-touched ones: a predictor
  built from exactly that correlates **0.4962** with the measured ratio. What it
  does put a size on is the effect itself — a disagreement region is measured at
  **0.36×** the arrival concentration of the rules that win it, at the median. So
  the question survives, asked of the *part* of a rule's extension rather than of
  the rule.
- **Why pairs specialize over that sample.** R-c's spread is not closed, only
  relocated: `touched/space` still spans a factor of 30 across the 2,080 pairs.
  The class-level account is not enough, per part three's own note, and it is
  still the obvious place to look.
  **Not the rule level either, 2026-08-16** (part five, D-b): dividing each
  pair's ratio by the rule-level prediction leaves **84.5%** of the spread on a
  log scale, p75/p25 falling only from 1.754 to 1.608.
- **Whether 1,743 points is enough to measure anything about a rare class.**
  `SECURITY_INCIDENT` has 20 touched points of 50,400 and `ONCALL_ESCALATION` 7
  of 6,300. Their `touched(c)` is a rate over 20 and 7 cases and their `f` is
  arithmetic rather than measurement; a second corpus with another seed would
  move them and nothing here bounds by how much.
- **The other three splits, and the 257-order set.** Measured on split 0's 65
  end orders because that is the set both published matrices hold. Whether
  98.6% is stable at 257 orders, or on split 4, would cost a regeneration of the
  larger matrices and was not done.
- **Whether "corpus" means deployment.** Unchanged from part two: it is a
  modelled arrival distribution with a seed. What is now known is that the gap
  between it and the uniform space is a sampling fact about *which* combinations
  it visits — which makes the answer inherit whatever the sampler gets wrong.

---

# The rule level — D-a to D-d

August 16, 2026. **This part of the record owns the rule-level figures.** Same
577 rules, same 65 end orders of split 0, same 2,080 pairs. What changes is that
each pair's ratio is no longer only measured: it is **predicted**, from a
quantity defined on rules, and scored against the ratio part four published.
Prediction: `IDEAS.md`, the entry *Where the 30× spread comes from, at the level
the order actually operates on*, drafted, signed and committed before any
territory existed — the one successor the C entry's stopping condition permits.
These figures arrived afterwards, in **PR #29**, which is what makes the order of
the two checkable in the log rather than asserted here. Record:
[`order_metrics_rules.json`](order_metrics_rules.json). Zero API calls, 346 s.

**One holds, two are refuted, one is reported — and the chain fails at the link
nobody was betting on.** The rule level carries about half of the ordering
(**ρ = 0.4962** against a band of 0.75–0.97) and almost none of the spread. The
*last* link, from the attribute marginals to `κ_r`, is the tight one: **0.987**.

---

## The chain the entry drew, and where it breaks

The entry proposed three links: a pair's ratio ← the arrival concentration of the
rules whose territories change hands ← the attribute marginals ← the generator.
Two of them are measured here and the third was declared before any of this
started.

| link | what it relates | measured |
|---|---|---|
| pair ← rules | `ρ̂`, the mean over `D_ij` of the two winners' `κ`, against the measured `touched/space` | Spearman **0.4962** (D-a), and the residual keeps **84.5%** of the spread on a log scale (D-b) |
| rules ← attributes | `κ_r` against `∏ c(cond)`, the same concentration computed per condition | Spearman **0.987**, `κ/κ̂` p75/p25 = **1.118** (D-d) |
| attributes ← generator | `has_security_keyword` at 50% of the space and 4.07% of the touched points | declared in `STATUS.md` since 8 August, not measured here |

So the mechanism the entry named is **available and does not operate**: the
attribute skew explains `κ` almost exactly, and `κ` explains half the ordering of
the pairs and essentially none of their spread.

---

## The trap, and the test that is not a promise

**The forbidden predictor is not merely correlated with the answer; it is the
answer.** A pair's measured ratio is `(|D_ij ∩ T| / 1743) / (|D_ij| / 134400)`,
the arrival density of its own disagreement set. Computed under the name
`rho_tilde` and reported beside `ρ̂`: Spearman **1.0000** against the measured
ratio, agreeing to **2.8×10⁻⁵**, which is the resolution the published rates
carry. Per-case access to `T` scores 1 by construction and measures nothing.

`IDEAS.md` therefore requires a test: *permuting `T` within each rule's extension
must leave `ρ̂` unchanged for every pair.* It ran **before any verdict was
computed**, in two arms, because the literal one passes for a reason that does
not separate the two predictors.

| arm | what it does | `κ` | `ρ̂` | the per-case quantity |
|---|---|---|---|---|
| **PERM-1**, literal | permutes `T` inside the **atoms** of the 577 extensions — exactly the permutations that preserve every extension setwise. **2,928 bits of `T` moved** | identical, 577 of 577 | identical, 2,080 of 2,080 | **moves on 0 pairs** |
| **PERM-2**, with teeth | 200 cancelling pairs of moves that hold all 577 counts `\|M_r ∩ T\|` exactly while `T` changes which atoms it sits in. **800 bits moved** | identical, 577 of 577 | identical, 2,080 of 2,080 | **moves on 1,980 of 2,080 pairs**, by up to 18 cases |

**Why the literal arm cannot catch a cheat, said here rather than left for a
reader to notice.** Under first-match-wins a winner is constant on an atom — two
cases matched by exactly the same rules cannot be decided differently — so every
territory and every `D_ij` is a **union of atoms**, and `|D_ij ∩ T|` is invariant
under PERM-1 exactly as `ρ̂` is. The tautology passes that arm as cleanly as the
predictor does. PERM-2 is the arm that separates them, and its 1,980 moved pairs
are what say the test could have failed.

The construction is arithmetic, not sampling: if atom `B` is matched by exactly
`A`'s rules plus `r`, moving a touched point from `A` to `B` raises rule `r`'s
count by one and no other's; doing the same downwards elsewhere for the same `r`
cancels it. Every one of the 577 counts is where it was, so `κ` cannot move, and
a predictor reading `T` per case must. `tests/test_order_metrics_rules.py` pins
both arms on instances small enough to check by hand, including a toy where
PERM-1 demonstrably fails to notice the cheat.

---

## The gates, and there are six

**THE MASK: 1,743 bits**, the same object part four built, inside the space.

**KAPPA: the five numbers the entry declared it had derived come back exactly** —
min **0.0229**, p25 **0.8105**, median **1.6265**, p75 **3.3046**, max
**30.8434** over the 577 rules of the pure pool, every one of them with a
non-empty extension. It is the gate that pins the **pool** and the mask together:
the hybrid masks, another corpus or another pool move it.

**PARITY: 31 of 31 rows exact**, the same gate and the same two records as parts
one, two and four — 883 / 0.8786 / 0.8472 / 0.6033 at split 0 and 65 starts, 884
/ 0.8796 / 0.8442 / 0.5776 at 257, all six budget rows, and 25 of 25 band cells.
**No new search**: every order comes out of `run_full_supervision` and
`run_band_1pct` of `order_metrics_run.py`, imported and called unchanged.

**THE MATRIX: the 2,080 measured ratios are READ and reproduced, never
re-measured.** They come from
[`order_metrics_touched.json`](order_metrics_touched.json), joined on `(i, j)`;
their summary comes back identical to the one that record publishes, p75/p25
**1.754326** and max/min **29.959769** included; and the two counts each ratio is
built from — `|D|` over the space and `|D ∩ T|` — come back identical from the
regenerated orders on all 2,080 pairs, which is what says the read rows are about
*these* orders.

**THE TERRITORIES: 65 of 65 orders**, pairwise disjoint, covering the whole
space, **nothing undecided**, and equal by two independent routes — the mask
sweep `order_metrics.winners` every other figure in this thread rests on, and the
atom route this part computes with.

**THE PERMUTATION TEST**, above, blocking and run before any verdict.

**One thing the arrangement turns up on its way past.** The 577 extensions cut
the space into **4,121 atoms**, sizes 1 to 420, median 25 — and under any of the
65 end orders only **25 to 53 rules hold a territory at all**. Everything two
orders can disagree about is decided by a few dozen rules of 577, which is the
resolution `ρ̂` has to work at and was not known before this run.

---

## The predictions of `IDEAS.md`, one by one

| # | verdict | measured |
|---|---|---|
| **D-a** | **REFUTED**, on the informative side | Spearman between `ρ̂` and the measured ratio over the 2,080 pairs: **0.4962**, against a band of 0.75–0.97 whose lower edge is its refutation line. Clearly above zero, and two thirds of the way to the band's lower edge. |
| **D-b** | **HOLDS** | The residual `ρ / ρ̂` has p75/p25 = **1.60765**, against a threshold of 1.20. But see below: it holds at the opposite end of its own meaning. |
| **D-c** | **REFUTED**, and not narrowly | Of the **478** pairs below the 0.1952 class floor, **0** have `ρ̂` below it — and so do **0 of all 2,080**, because `ρ̂`'s minimum is 0.3085. The row asked for three quarters. |
| **D-d** | *reported, not adjudicated* | Spearman between `κ_r` and `∏ c(cond)` over the 577 rules: **0.987**. The ratio `κ/κ̂` has median exactly **1.000** and p75/p25 = **1.118**. |

### D-a, and what half a correlation means here

**0.4962.** The entry's own text names the reading: *below is the informative
side — it would mean the heterogeneity inside a rule's territory dominates the
differences between rules, and the explanation lives beneath the rule level, in
the attributes directly.* That is the outcome, and D-a and D-b were declared *a
single position taken in two halves*, so **the entry is wrong** and says so
itself: rules explain some of it, not most of it.

**Where the predictor loses.** `ρ̂` is a mean of per-rule concentrations over the
cases of `D_ij`; the measured ratio is the concentration of `D_ij` itself. The
two are not on the same scale, and the gap is the finding rather than a defect of
the units: the residual `ρ / ρ̂` has a median of **0.3630**, so a disagreement
region is measured at **0.36×** the arrival concentration of the rules that win
it. Disagreement lives in the rarely-touched *part* of a rule's extension, not in
rarely-touched rules — which is part four's open question (*why disagreement
lives where the corpus does not go*) with a number on it for the first time.

### D-b, which holds at the far end of its own meaning

The row's refutation clause reads: *refuted at or below 1.20, which would say the
rule level closes the spread completely and nothing is left inside the
territories.* Nothing of the sort happened. The measured ratio's own spread is
p75/p25 = 1.754326 and the residual's is **1.60765**, so on a log scale
**84.5%** of the spread survives dividing by the prediction — arithmetic on two
figures this record publishes, not a third measurement.

**So D-b is a threshold that cannot fail on the side it was drawn for.** It was
built to catch a rule level that explained everything, and it passes identically
whether rules explain most of the spread or almost none of it. Read with D-a it
says what it can: the spread is not at the rule level. Read on its own it says
very little, and that is a fact about how the row was drawn, in the same family
as C-a's band that could not accommodate its own hypothesis.

### D-c, refuted by a scale the row did not check

**0 of 478**, and 0 of all 2,080. The floor is the smallest of the eight class
ratios `touched(c)/all(c)`, **0.195226** — `T2_TECHNICAL` — and `ρ̂` never goes
below **0.3085** anywhere in the set. The row asked whether the pairs that fall
below the class floor do so *because* the rules whose territories change hands
are rarely-touched ones. They do not: no combination of winners in this material
produces a mean `κ` that low, because a mean of 25 to 53 rules' concentrations
sits near the middle of `κ`'s distribution however the pairs are chosen.

Derived from the 2,080 rows the record stores, and not a second measurement:
`ρ̂` runs 0.3085 / 0.6999 / 0.7816 / 0.8824 / 1.7424 (min, p25, median, p75, max)
against the measured ratio's 0.0544 / 0.2039 / 0.2849 / 0.3576 / 1.6284. **The
predictor is a factor of 2.7 above the quantity it predicts at the median and
spans a fifth of its range** — p75/p25 1.261 against 1.754, max/min 5.65 against
29.96. A row comparing the two against one absolute threshold was comparing
quantities that share a definition of *concentration* and nothing else.

### D-d, reported: the last link is the tight one

`κ̂(r) = ∏ c(cond)`, where `c(cond)` is the same concentration computed for a
one-condition rule, is what `κ_r` would be if the attributes in `r`'s conditions
were independent under both measures. Over the 577 rules and the 69 distinct
conditions they use: **Spearman 0.987**, `κ/κ̂` with median exactly **1.000**,
p25 0.9444, p75 1.0562 — p75/p25 = **1.118** — and tails at 0.3926 and 25.46.

The generator's skew is visible directly in the conditions:

| condition | share of the space | share of the touched points | `c(cond)` |
|---|---|---|---|
| `has_security_keyword = True` | 0.5000 | 0.0407 | **0.0815** |
| `channel = phone` | 0.2500 | 0.0539 | 0.2157 |
| `severity = 1` | 0.2500 | 0.0545 | 0.2180 |
| `prior_tickets_30d = 0` | 0.0476 | 0.1377 | **2.8916** |
| `language = en` | 0.2000 | 0.5663 | 2.8313 |

`STATUS.md` has recorded since 8 August that `has_security_keyword` is 3% of
arrivals against 50% of the attribute space; here it is 4.07% of the 1,743
touched points, and it is the single most rarefied condition of the 69. **So the
chain's last link is not in question — it is nearly exact.** What fails is the
first one, and it fails inside the territories.

---

## What this settles, and what it opens

**The spread is not a rule-level fact.** The entry's hypothesis was that a pair's
ratio is the arrival concentration of the rules whose territories change hands,
and that the 1,344× range of `κ` was what could cover a 30× spread in the pairs.
The range is there — though its ceiling is not reachable, see the erratum below —
and the mechanism does not operate: half the ordering and essentially none of the
spread. What is left is what D-a's own refutation clause
names — the heterogeneity **inside** a territory dominates the differences
between territories.

**And that heterogeneity now has a size.** A disagreement region is 0.36× as
touched as the rules that win it, at the median, with a residual spanning 0.075
to 1.11. Whatever distinguishes a pair whose ratio is 0.054 from one whose ratio
is 1.63 lives below the rule, in which *part* of a rule's extension the two
orders happen to fight over — **a reading of 0.4962 and not a measured result;
see the first two bullets of *what this part does not settle*, corrected
2026-08-16**, since a `κ` conditioned on the order would test the same thing
without leaving the rule level.

**Nothing above is withdrawn.** Every figure in parts one to four is what it
always was, on the surface it names. This part adds a predictor and reports that
it fails, which changes no measurement any of them made.

---

## Erratum, 2026-08-16 — the ceiling of `κ` holds no territory

Record: [`territory_holders.json`](territory_holders.json), landed in **PR #30**.

**What is corrected: a reading, not a value.** This part uses `κ`'s range over
the 577 rules — 1,344×, ceiling **30.8434** — as the illustration that the
mechanism D-a proposed was *available*, which is the argument the entry it
adjudicates makes against the 12.3× of the class ratios. The rule at that ceiling
is **`R0327`**, and it **wins not one case** under any of the 65 end orders. Under
first-match-wins a rule with no territory enters `ρ̂` nowhere, so the ceiling that
illustrates the argument is a value the predictor can never read. Measured: the
union of the 65 territory sets is **406 of 577** rules, and over that union `κ`
runs **0.0229** (`R0019`) to **25.7028** (`R0062`) — a ceiling 1.20× lower than
the pool's, and a floor that is the pool's own.

**The scope is literal.** *Zero of the 65 end orders of split 0 at full
supervision* — the set every matrix in this record holds. **Not "never"**:
`R0327`'s extension is not empty, some other order over these same rules could
give it a territory, and nothing here measures that. The same literalness applies
to the 406: it is a union over these 65 machines, not a statement about which
rules are reachable in principle.

**The argument survives, and it survives inside a single machine.** The range
that bears on D-a is not the pool's but the one available **within one order**,
since `ρ̂` averages the `κ` of the rules that actually win the cases of a pair.
Measured across the 65: median **651×**, minimum **183×**, maximum 1,120×. The
weakest is order 0 — the greedy's end order, 25 rules — where `κ` still runs
0.0815 to 14.94. The entry asked whether the mechanism could cover a 30× spread
where 12.3× could not; the answer is yes by a factor of six in the *worst* of the
65 machines. **So this reinforces D-a's refutation and does not attenuate it**:
`ρ̂` had two to three orders of magnitude of variation available in every machine
and still reached 0.4962.

**No verdict moves, and no figure does either.** `κ`'s values are untouched —
this run reads them from [`order_metrics_rules.json`](order_metrics_rules.json)
and never recomputes them, gated on their still reproducing the five-number
summary published beside them. D-a REFUTED, D-b HOLDS, D-c REFUTED, D-d reported:
each stands on the number that decided it, and D-e's 25–53 stands with its
complement added — **171 of the 577 rules hold territory in none of the 65
orders**, `R0327` among them. `STATUS.md`'s copy of the range is scoped *across
the 577* and stays exact as written.

**Provenance, which is not what the rest of this part has.** This is a **post-run
audit finding**: the fact was read off `order_metrics_rules.json` after PR #29
published it, and the instrument was written afterwards by someone who already
knew what it would say. It is not a prediction that could have failed, and the
two commits of PR #29 have the opposite property in the log. What it can be worth
instead is that the primitive is exact and the gates blocking: parity **31/31**,
`κ` read and reproducing its published summary, and `n_rules_with_territory`
identical **order by order** to `gates.territories.per_order` of the record it
corrects. 343 s, zero API calls, clean tree, `code_digest ccd2ad259f5d8198`.

---

## The register, fifth part

| id | finding | status |
|---|---|---|
| **D-a** | Spearman between `ρ̂` and the measured ratio, between 0.75 and 0.97. | **REFUTED**: 0.4962, below the band's lower edge, which is its refutation line. The informative side, by the row's own text. |
| **D-b** | The residual `ρ / ρ̂` still spans p75/p25 above 1.20. | **HOLDS**: 1.60765 — and 84.5% of the original spread on a log scale, so it holds at the end of its range opposite to the one it was drawn to catch. |
| **D-c** | At least three quarters of the 478 pairs below the class floor have `ρ̂` below it too. | **REFUTED**: 0 of 478, and 0 of all 2,080; `ρ̂`'s minimum is 0.3085 against a floor of 0.1952. |
| **D-d** | Reported, not adjudicated. | `κ_r` against the product of its conditions' concentrations: Spearman **0.987**, ratio p75/p25 **1.118**. The last link of the chain is nearly exact. |
| **D-e** | *(not predicted)* What the predictor's inputs actually are. | **25 to 53 rules of 577 hold a territory** under any of the 65 end orders, over 4,121 atoms. Everything two orders disagree about is decided by a few dozen rules. The union over the 65 is **406**, and the erratum above names which rule is not in it. |

**The entry carries no stopping condition, and its absence is deliberate**: the
C entry granted one successor and said that successor would carry none. This
record adds none either, and takes no decision from the outcome.

---

## Provenance of the rule-level part

**Cost: 346 s in one process, zero API calls.** Regeneration is 339 s of it
(135.2 s and 118.1 s for the two 257-start searches, 86.2 s for the whole 1%
band); the arrangement, the territories, the 2,080-pair sweep and the whole
permutation test are under 5 s together, because a pair is summed over 4,121
atoms instead of 134,400 cases.

**`code_dirty: false` and `git_dirty: false`.** The instrument was committed
before the run, in its own commit carrying no figure, as part four's was. What
identifies the code is `code_digest 7c79e8de11c1cb97`; what identifies the
**orders** is neither that nor the commit, it is the parity gate, and the parity
gate is exact on all 31 rows. The `_env.git_commit` is a branch commit that the
rebase merge rewrites, which is why this section cites **PR #29** and no SHA.

**One figure of the entry's own arithmetic does not reproduce, and it is
rounding.** The entry gives `κ`'s range as **1,344×**; that is max over min on
the unrounded values, and the record's `range_factor` is **1,346.9** because the
gate computes it from the four-decimal summary it compares against. The five
numbers themselves are exact.

## What the rule-level part does not settle

- **What distinguishes the part of a rule's extension where two orders fight.**
  It is **one of the two places the spread can live**, and nothing here describes
  it: not which attributes, not whether it is the same region for every pair.
  **Corrected 2026-08-16.** This bullet said it was *the only place left*, which
  is wrong and is the sentence being withdrawn. `κ` is defined over `M_r`, the
  whole extension, while `ρ̂` applies it to the cases `r` **wins** under one
  order — a different subset of `M_r` in every one of the 65. So a rule whose
  extension is touched at the pool average can hold a territory that is not, and
  the gap that opens there is still at the rule level: closing it takes
  conditioning `κ` on the order, not descending beneath the rule.
- **How much of the 0.4962 is that extension-versus-territory gap, and how much
  is heterogeneity inside the territory.** The two are different quantities and
  this run separates neither: `ρ̂` reads one `κ` per rule, computed over the whole
  extension, so the shortfall it leaves is their sum. That is why D-a's clause —
  *the explanation lives beneath the rule level, in the attributes directly* — is
  **a reasonable reading of 0.4962 and not a result measured here**, and this
  record does not upgrade it. Separating them means scoring a second predictor,
  `κ` conditioned on the territory, against a matrix already seen; that is
  governed by §0 of `PLAN_ORDER_METRICS.md` exactly as the bullet below is, and it
  is not to be tried on this data after the fact.
- **Whether a finer rule-level predictor would do better.** `ρ̂` is the one the
  entry defined — a case-weighted mean of two winners' `κ` — and trying others
  on this data after seeing 0.4962 is what §0 of `PLAN_ORDER_METRICS.md` exists
  to prevent. What is measured is that *this* one fails, not that the rule level
  is exhausted.
- **The other three splits, and the 257-order set.** Measured on split 0's 65 end
  orders because that is the set every matrix in this record holds. Unchanged
  from part four.
- **Why only a few dozen rules hold territory.** D-e is a by-product of the
  gates, not a question anybody asked. Whether 25–53 is a fact about
  first-match-wins over a uniform space, about the 577 rules, or about the
  orders the search returns is not measured.
  **Bounded 2026-08-16 by the erratum above, not explained**: the union over the
  65 orders is 406 rules, so which few dozen win is largely a fact about the
  order and not about a fixed subset of the pool — and 171 rules win nothing
  under any of them.
