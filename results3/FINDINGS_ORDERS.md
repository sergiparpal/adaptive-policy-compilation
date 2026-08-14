# Findings — the orders, not the scores

August 15, 2026. **This record owns the figures below.** They are not part of
the optimizer audit ([`FINDINGS_AUDIT.md`](FINDINGS_AUDIT.md)): that audit was
about a search, and this is about what the search returns. Plan:
[`PLAN_ORDER_METRICS.md`](../PLAN_ORDER_METRICS.md), §0 drafted and committed
before any number existed and signed unchanged. Record:
[`order_metrics.json`](order_metrics.json). The instrument and its step 0
arrived in PR #13; the regeneration and these figures in PR #15. Zero API calls.

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
| **Q-d** | **REFUTED** | Over the 32,896 pairs of split 0: Spearman of global tau against distance **−0.1361**, of tau restricted to the 35,457 conflicting pairs **−0.1349**. The restricted metric does **not** beat the global one, which is the refutation verbatim. Split 4 says the same: −0.078 against −0.062. |
| **Q-e** | **HOLDS** | Median churn **99.65%** of rules at a different index; median disagreement **19.99%**. **30,775 of 32,896 pairs (93.6%)** move more than 60% of the rules while disagreeing on less than 30% of the space. |
| **Q-f** | **REFUTED, and in the opposite direction** | Pooled over the 2,080 pairs of split 0's 65 end orders, overall rate **0.2035**; **ACCOUNT_MANAGER 0.0916 (0.45×)** and **T3_ENGINEERING 0.0947 (0.47×)**, both *below* the overall rate, which is the stated refutation. Disagreement concentrates instead on **SECURITY_INCIDENT, 0.3121 (1.53×)**. |

### Q-d, and what exactly is refuted

The design premise — that a rank statistic can be repaired by restricting it to
the pairs that can matter — is wrong on this instance. It is not that the
restricted tau is bad and the global one good: **both are near zero**, and both
correlate with behaviour at |ρ| ≈ 0.13.

The mechanism is visible in the record. Across the 32,896 pairs the median
global tau is **0.0339** and the median restricted tau **0.0423**: these end
orders are mutually rank-uncorrelated, essentially random permutations of one
another, while their behavioural distances spread from 4,830 to 55,269 cases. A
statistic with no variance cannot track a quantity with plenty, and restricting
it to a fifth of the pairs does not create any. Added to that, PR #13's finding
that conflicting pairs can be inert means the restriction does not even isolate
the pairs that actually decided anything **in these orders**.

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
disagree on a case that two rules with different actions both match; where two
thirds of a class has no correct rule at all (`FINDINGS3.md` §2:
`ACCOUNT_MANAGER` 64.2%, `T3_ENGINEERING` 66.7%), there is little competition
over those cases and therefore little to disagree about — the orders are
uniformly wrong there rather than differently wrong. `SECURITY_INCIDENT`, the
largest class on the uniform surface with 50,400 of 134,400 cases, is where the
proposer wrote most and where the orders fight.

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

**G4 — and no free lunch either, on the real instance.** Zero pairs, in any set,
sit at behavioural distance 0 with a positive positional distance. The property
that motivated the whole instrument — two orders differing only in
non-conflicting pairs are the same machine — is real, pinned on toys and on the
29 hidden rules, and **has no instance among these end orders**. Four fifths of
each permutation is free, and no two of these orders differ only in the free
part. This is a negative result and it sharpens Q-e rather than softening it:
churn wildly overstates difference, but it never overstates it to the point of
zero.

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
| **G4** | Any pair with behavioural distance 0 and positional distance > 0. | **NONE**, in any set. The property holds on toys and on the hidden policy and has no instance here. |
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

---

## What this does not settle

- **Whether any rank statistic tracks behaviour on this material.** Q-d refutes
  the one §0 proposed. Both taus sit near zero over mutually uncorrelated
  permutations, so the honest next question is whether the failure is the
  statistic or the range, and neither this record nor the plan answers it.
- **Why 65 draws give 65 machines.** That the landscape has no plateaus the
  objective can see is measured; what shape it has instead is not.
- **What any of this costs downstream.** Rung 4 consumes orders. That its
  figures inherit a draw was already recorded; that the draw is worth ~8% of the
  space between two orders one train case apart is new, and what it does to a
  learned policy in deployment is unmeasured.
- **The corpus surface.** Everything here is the uniform measure over 134,400
  cases. Two orders that disagree on 20% of the space need not disagree on 20%
  of the arrival distribution, and this record does not say which.
