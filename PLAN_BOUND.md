# PLAN_BOUND — how much of the residue is slack

**Status: drafted by Claude on 2026-10-16, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §8 says why the gate binds anyway.

**This plan exists because [`STATUS.md`](STATUS.md)'s first open item has no
measurement behind it.** Rung 3's coverage bound counts, case by case, whether
some rule matching a case gets it right. It is a valid upper bound on every
order, and no order is known to reach it: the erratum to §1 of
[`results3/FINDINGS3.md`](results3/FINDINGS3.md). The audited search, seeing all
134,400 cases of the space, stops 0.0879 below it on the pure pool, and the
record's two figures put the hybrid pool 0.0974 below its own. *A heuristic that
misses a bound never distinguishes the two*: the gap could be slack in the bound
or weakness in the search. `STATUS.md` says exact optimisation would settle it.

[`IDEAS.md`](IDEAS.md) carries a cheaper first step, from the outside reading of
October 2026. It needs no solver. A case with exactly one right rule is decided
right only if that rule precedes every wrong rule matching it. If such hard
edges close a cycle, one of the cases behind it is lost under every order. A
packing of cycles that share no case counts those losses validly. **This plan
runs that step and bets on what it finds.** It generalises the hard edge so that
cases with several right rules can join a cycle too (§3). And it corrects
`IDEAS.md`'s description of the hybrid pool, which describes rung 2's engine and
not the code behind rung 3's figures (§2.1).

**What it would change.**

- **If the certificate closes most of the residue**, most of what the search
  missed is unattainable by any order. The searched figures then sit close to
  the best any order can do, and the coverage bound overstates what is
  attainable by at least `ν`.
- **If the certified bound meets the searched score**, the search found an
  optimal order and the residue is settled, on that instance.
- **If it closes little**, the question stays open. The certificate is a floor
  on the slack, never an estimate of it (§5.1), and the next step is the solver
  §10 names.

The audit's records say both today. *The bound was not loose* heads the 2026-08-08
erratum to `FINDINGS3.md` §4 and answers `FINDINGS_AUDIT.md`'s first question.
*Somewhat loose* follows a few paragraphs later in each. **None of this plan's
figures exists**, so under [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is
pre-registrable, although it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic, its denominator and its surface here, before
any figure.** On each instance:

- `CB` is the coverage bound in cases.
- `A` is the best score a published search reached.
- `ν` is the number of cases the certificate shows every order loses.
- `TB = CB − ν` is the certified bound.
- The **residue** is `CB − A`, and the **share** is `ν / (CB − A)`: how much of
  the residue the certificate shows is slack. An instance with no residue counts
  as share 1, and none has one today (§3.3).

The instances are the ones rung 3's audited search ran on, built by the functions
that built them (§1). The **pure** pool is first-match over the rules that match
a case. The **hybrid** pool is first-match over the rules no matching rule
strictly subsumes, which is `rung3/order_search.build_tables`' `undef` (§2.1).

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **H-a** | **Over the space, most of the pure pool's residue is slack.** | exhaustive space, pure pool: the share, with `CB` the count behind 0.8784 and `A` the direct search's 0.7905 | **share ≥ 0.50** | **share < 0.50** |
| **H-b** | **The same holds for the hybrid pool.** | exhaustive space, hybrid pool: the share, with `CB` behind 0.8531 and `A` the direct search's 0.7557 | **share ≥ 0.50** | **share < 0.50** |
| **H-c** | **The certificate settles neither pool over the space.** | on each pool of the space, whether `TB / 134,400` rounded to four decimals equals `A`, which is published to four | **met on neither** | **met on either** |
| **H-d** | **On the corpus, where each order was fitted, at least three quarters of the residue is slack.** | corpus, the train half of each of the five splits, both pools: the median of the ten shares, with `A` the best train count any record publishes (§2.3). The median of ten is the mean of the fifth and sixth | **median ≥ 0.75** | **median < 0.75** |
| **H-e** | *Reported, not adjudicated.* **What reading the rows needs.** | §7's readings: per instance, the structure the certificate rests on, `ν` by cycle length and by start, the certified bound and the residue it leaves; the certificate itself | — | — |

**Signed by Sergi: ________________________ (date: ______________)**

**No standard errors.** Every figure is a count over a fixed instance, and none
is an estimate. **One label replaces them.** On the space, `A` is published to
four decimals, so the residue is known to ±0.00005 and each share to a small
range. **A share whose range reaches both sides of its line is labelled *thin*,
and the label does not change the verdict.** The corpus's `A` is an exact count
(§2.3), so H-d has no such range.

**What a hold says and what a refutation says.** The certificate is a floor on
the slack (§5.1). A hold of H-a says at least half of the space's residue is
unattainable by any order. That means the search falls short of the best order
by at most the other half. **A refutation does not say the residue is search
weakness.** It says the certificate could not show it was slack, which leaves
the question where `STATUS.md` has it.

**Why H-a and H-b's line is 0.50.** `STATUS.md`'s item asks whether the residue
is slack or search. Half is the line where the answer the certificate can give
turns from *mostly slack, shown* to *not shown*.

**Why H-c is a row.** Meeting would settle the item on that instance, and it
needs two things to be exact at once: the search optimal and the packing tight.
A row says whether the drafter thought that likely before anyone looked.

**Why H-d's line is 0.75.** The corpus's train halves are where each order was
searched for, and their residues are tens of cases, against thousands over the
space. The drafter expects more of each of them to be forced, for the reasons
under *What the drafter expects*. **0.75 says the surface changes the answer,
not only its size.** Every row of the `S` and `R` threads that bet a quantity
would carry across a change of surface lost, and the one that bet it would
break held (`IDEAS.md`, rung 3's standing note). This row argues that it
breaks, and sets the line high enough to be refuted if it does not.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the documents publish.** `STATUS.md`'s *What is open* and scoreboard,
  `IDEAS.md`'s open items, `results3/FINDINGS3.md` §18's count and
  `results3/FINDINGS_ORDERS.md`'s census of pairs, read directly. And a
  subagent's survey, made for this plan, of every passage in the project's
  documents on the bound, exact methods, cycles and hard edges, with its
  quotations: `FINDINGS3.md` §§1, 4 and 13 and their errata, `FINDINGS_AUDIT.md`,
  `ARBITRATION_REPORT.md`, `CHAT_SUMMARY.md`, `EXTERNAL_REVIEW.md` and the plans.
  It found that nothing in the tree computes a loss under every order for the
  577 rules.
- **The records' published figures**, read for this plan:
  - `results3/order_search_ls_fullspace.json`: everything but its rows per
    split, that is both pools' bounds on the corpus and the space, the direct
    search's scores and its summaries;
  - `results3/order_search_ls.json`: the bounds, and each split's train, test
    and space scores for both pools;
  - `results3/order_search.json`: each split's train and test ceilings;
  - `results3/start_budget_check.json`: its summary and the pure pool's train
    counts at 65, 129 and 257 starts.
- **One fact about the 577 rules the drafter counted itself.** The conditions
  of `results/llm_run.json`, by attribute. `language`
  appears in 3 conditions of the 1,763; the hidden policy uses it in one rule,
  `H21`. That bears on how many truths share a pool over the space (§5.6).
- **The code.** `rung3/order_search.py`, `order_search_ls.py`,
  `local_search.py` and `optimizer_check.py`; `rung2/engine2.Space`;
  `harness/hidden_policy.py`'s use of `language`; `reuse/plan.py`; `primacy/`.
- **The blocking checks' output** (§6). It prints pass or fail and figures
  already published: the bounds, the searched scores, and, for `H-g2` and
  `H-g3`, the hidden policy's figures and synthetic instances'.
- **The synthetic experiments that chose the method** (§5.7). None used rung 1's
  rules.
- **Not seen, because nobody has computed them**, on any instance built from the
  577 rules:
  - any `ν` or cycle;
  - the number of signatures, of nodes, or of cases with one right rule;
  - how many cases share a pool with a case of another truth.

  `H-g1` builds the signatures to score random orders through them, and prints
  only whether they agree with `score_order`.

**What the drafter expects, written down so the scoreboard can score it.** All
four hold. **The drafter trusts H-a and H-b least.**

- **H-a and H-b.** Expected shares between a half and four fifths. Three reasons
  push them up:
  - the space is dense in conflict: 35,457 of the 166,176 pairs of rules match a
    common case and disagree on the pure pool (`FINDINGS_ORDERS.md`);
  - rung 1 wrote 93 pairs of identical rules with different queues, and they
    reach 30,670 points of the space (`FINDINGS3.md` §18): each such pair can
    close two-case cycles over its territory;
  - the rules almost never test `language` and the policy does, so points that
    differ only in it share a pool and some differ in truth.

  Two push them down:
  - over the space a case is matched by many rules, often several right ones,
    and such a case joins a cycle only if all its right rules are wrong for the
    next case;
  - the greedy packing reached the exact loss on 86% to 89% of small synthetic
    instances, but nothing is known about its tightness at this size.

  The hybrid pool has a quarter of the pure pool's conflicting pairs, 9,239, and
  a larger residue. That could mean more of its residue is search: the drafter
  does not know which way that cuts, and sets the same line.
- **H-c.** Not met on either pool. The declared search is known to stop short
  of an optimum: given four times the starts, it improved its best train score
  in 2 of 5 splits, and the multi-start's peak is a single start that spreads
  (`IDEAS.md`, rung 3). And the packing is greedy.
- **H-d.** A median near 0.85. The residues are 23 to 56 cases. Those that two
  tickets with the same pool and different truths explain are certified exactly
  by two-case cycles. The searched counts are the best of up to four searches.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 29
of 70 adjudicated rows came out refuted. **These bands are more likely too
comfortable than too strict**, and the signature can tighten them.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls, and no search is re-run.

**Already paid for, and read as they stand:**

- `results/llm_run.json`, rung 1's 577 rules, through
  `rung3.order_search.load`.
- `results3/order_search_ls_fullspace.json`, the direct search over the space:
  both pools' bounds and scores.
- `results3/order_search_ls.json`, the declared search on each split's train
  half: both pools' train scores.
- `results3/start_budget_check.json`, the same search at 65, 129 and 257 starts
  on the pure pool: train counts.
- `results3/order_search.json`, each split's train ceilings, which `H-g1`
  reproduces.

**The truth** enters through `rung3.order_search.build_tables` and
`rung3.order_search_ls.space_truth_masks`, which
`tests/test_oracle_separation.py` already lists among the modules allowed to see
it. No module of this plan imports the oracle.

---

## 2. The choices that have to be made at signature time

Four, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 The hybrid pool is rung 3's masks, not rung 2's engine — the drafter recommends the masks

`IDEAS.md`'s entry says that in the hybrid pool *subsumption's edges join the
graph and cannot yield*. That is rung 2's engine. Rung 3's `hibrido` figures,
the 0.8531 and 0.7557 above among them, come from its undefeated pool:
`rung3/order_search.build_tables` on the corpus, and
`rung3/order_search_ls.space_pools` over the space, which
`tests/test_local_search.py` holds equal to it. It cuts each case's pool down to
the rules no matching rule strictly subsumes, and the order then decides among
those with no constraint. **A rule and one it strictly subsumes are never in
the same pool**, so their relative order never changes a score. An edge forcing
it would close cycles that cost nothing.

The counterexample, which `tests/test_bound.py` pins:

- D's extension is strictly inside A's;
- on case 1 the pool is {A, C} and only A is right;
- on case 2 the pool is {C, D} and only C is right.

The edges A→C, C→D and D→A close a ring, and the order A, C, D wins both
cases. **The certificate takes the hybrid instance's masks as the search did.**
Building rung 2's semantics instead would bound a different machine, against
which no search has been run.

### 2.2 The space is read at its published precision — the drafter recommends it

The direct search's scores are published to four decimals: about ±7 cases of
134,400. The exact counts would need the search re-run, about 2.7 hours for both
pools, to recover figures that are already published. **H-c's *met* is
therefore met at the published precision**, and §0's *thin* label carries the
rounding into H-a and H-b. The alternative is to re-run the search first, so
that H-c reads exact counts.

### 2.3 The corpus's searched score is the best any record publishes — the drafter recommends it

The pure pool has four searches on each split: the declared 65 starts, and the
budget diagnostic's 65, 129 and 257. The hybrid pool has the declared one.
`A` is the best of what exists, so the residue is the smallest any record
leaves. With about a thousand train cases, four decimals name exactly one count,
and `H-g1` checks that they do. The alternative is the declared 65 starts alone,
which would leave larger residues and count the budget diagnostic's gains as
slack the certificate had to find.

### 2.4 The thread's name and letter

`PLAN_BOUND.md`, rows `H-a` to `H-e`, for the *hard* edges. `A` to `F`, `I`, `K`,
`L`, `O` to `S` and `U` to `Y` are taken. The naming is Sergi's to overrule.

---

## 3. The certificate, and the reference figures

### 3.1 The argument

For a case `c`, let `R(c)` be the rules of its pool that get it right and `X(c)`
the ones that get it wrong. Under an order, `c` is right iff the first rule of
`R(c)` comes before every rule of `X(c)`.

**A cycle is a sequence of cases `c_1, …, c_m`, `m ≥ 2`, with `R(c_{i+1})`
inside `X(c_i)` for every `i`, indices modulo `m`.** No order gets them all
right. If `c_i` is right, the first rule of `R(c_i)` precedes every rule of
`X(c_i)`, so every rule of `R(c_{i+1})`, so the first of them. Around the cycle
that is a strict order that comes back to its start. `IDEAS.md`'s hard edges are
the case `|R(c)| = 1`. Containment lets a case with several right rules join a
cycle too, and it reduces to the hard edge when `R` has one rule.

**Cases with the same `R` and `X` are decided alike by every order.** They form a
*signature*, and its number of cases is its capacity. A **packing** gives each
cycle a multiplicity `y > 0`, so that each signature's cycles add up to at most
its capacity. Then every order loses at least the sum of the `y`, which is `ν`.

Fix an order. Each cycle has a signature the order gets wrong, and all of that
signature's cases are lost. Charge the cycle's `y` to that signature. Each lost
signature is charged at most its capacity, and its capacity is cases lost.

**The certificate is the list of cycles with their multiplicities**, each cycle
written as one case per signature. `verify` checks it from the masks alone:

- every case's pattern is rebuilt from the masks;
- every containment and every capacity is checked;
- the sum is recomputed;
- and nothing of the finder's is used.

`tests/test_bound.py` walks `verify`'s calls to say so. On instances small
enough to enumerate every order, the certified bound has never fallen below the
exact optimum (`H-g3`).

### 3.2 The finder

A greedy packing over a graph whose nodes are the distinct `R`s of the contested
cases. Node `A` points to node `B` through a signature with `R = A` whose `X`
contains `B`. The four steps are in `bound/certificate.py`'s header, fixed before
any figure:

1. cycle lengths in increasing order, the shortest through each node first;
2. each edge's label chosen as the one that labels the fewest edges, then the
   one with most capacity left;
3. until no strongly connected component is left;
4. seventeen starts, the nodes in index order and then sixteen seeded shuffles,
   keeping the largest `ν`.

Rules with the same masks are merged into one class first (§5.5). **Validity
does not depend on any of these choices.** Every start produces a certificate
`verify` would accept, and only the size of `ν` depends on them.

### 3.3 Reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| coverage bound, space | 0.8784 pure, 0.8531 hybrid | the share of the 134,400 points some rule of the pool gets right | `results3/order_search_ls_fullspace.json`; `FINDINGS3.md` §4 erratum |
| direct search, space | 0.7905 pure, 0.7557 hybrid | the declared multi-start, searched over the whole space | the same; `FINDINGS_AUDIT.md` |
| the residue, space | 0.0879 pure | the gap `STATUS.md`'s first open item asks about | `STATUS.md`, *What is open* |
| train ceilings | 0.8970 to 0.9108 pure, 0.8560 to 0.8627 hybrid | each split's coverage bound on its train half | `results3/order_search.json` |
| searched train counts | 867 to 884 pure, 802 to 830 hybrid | the best train score any record publishes, per split | `results3/order_search_ls.json`, `results3/start_budget_check.json` |
| conflicting pairs | 35,457 pure, 9,239 hybrid, of 166,176 | pairs of rules that match a common point and disagree, over the space | `results3/FINDINGS_ORDERS.md` |
| identical rules, different queues | 93 pairs; 30,670 points reached | written the same, sent to different queues | `results3/FINDINGS3.md` §18 |

The hybrid residue over the space, 0.0974, is the record's two figures
subtracted. No document states it.

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** If a frozen file has a bug, stop
   and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise the loop.** Nothing here runs it.
4. **Seed 17, no regeneration, and every record this plan reads is read-only.**
5. **Do not adjust a prompt or a schema.** Nothing here touches either.
6. **If the numbers come out badly, report them.**
7. **No API key is needed**, and none is loaded.

And this plan's own, lettered:

A. **Rung 3's functions are called, not copied**: `load`, `build_tables`,
   `split`, `subsumption_below`, `space_pools` and `build_masks`, and
   `score_order` to check the decomposition. A second construction that drifted
   from the first would bound an instance no search was run on.
B. **The records are inputs, never outputs.** Nothing under `results/` or
   `results3/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §8 are fixed here and pinned by tests**, so that moving one
   after a figure exists is visible in a diff. That includes the finder's.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow (§1).
F. **The dry run prints pass or fail and figures already published, and never
   packs a cycle on rung 1's rules.** `bound/gates.py` builds a certificate only
   for the hidden policy and synthetic instances, and a test walks its syntax
   tree to say so.
G. **The certificate is checked before it is believed.** `verify` rebuilds every
   case's pattern and every capacity from the masks, by a route that shares
   nothing with the finder but the masks. And the certified bound must stay at or
   above a score some order reached. **Either failure stops the stage before
   anything is written**, because it would mean the instrument is wrong, not
   that a row came out one way.

---

## 5. Known traps

**5.1 — The certificate is a floor on the slack, never an estimate of it.**
Every order loses at least `ν` coverable cases, and may lose more for reasons no
packing of cycles sees. A small share says the certificate could not show the
residue was slack. It does not say the residue is search weakness. Only `TB`
meeting `A` settles anything, and then on that instance alone.

**5.2 — `A` is not an optimum.** The search improved its best train score in
2 of 5 splits when given four times the starts. So the residue mixes slack with
search weakness by construction, and a perfect certificate would still read a
share below 1 wherever the search fell short. A share is about the pair, the
certificate and the search, and §0 reads it that way.

**5.3 — The hybrid pool is not rung 2's engine** (§2.1). Rung 3's `hibrido`
bound is lower than the pure one because subsumption removes right rules from
pools, the loss `ARBITRATION_REPORT.md` places *in the bound*. That loss is
already in `CB` and is not counted again.

**5.4 — The space's `A` has four decimals** (§2.2). `met` is met at that
precision, and the *thin* label of §0 carries the rounding into the shares.

**5.5 — Interchangeable rules are merged, and that changes no optimum.** Rules
with the same mask and the same right cases decide every case alike whichever
comes first. Rung 1 wrote 307 of its 577 rules with a copy. One class per
distinct pair of masks makes the graph smaller and the certificate no weaker.

**5.6 — Cases that share a pool are decided alike.** That is
`FINDINGS_ORDERS.md`'s *a winner is constant on an atom*. Where such cases have
two truths, every order loses the smaller side, and two-case cycles certify
exactly that. Where they have three or more, cycles can certify at most half
the cases, and the exact loss is everything but the largest truth. The packing
leaves that difference on the table. Over the space the drafter expects pools
shared across truths mostly through `language`, which the rules almost never
test. That gives two truths where it matters (§0). The atom's exact loss was
tried on the synthetic data of §5.7 and gained between −1% and +1%, so it is
not in the finder. It is named in §10.

**5.7 — The finder's choices were made on synthetic data, before the plan
existed.** The label rule and the starts of step 4 in `bound/certificate.py`'s
header were compared on two sets of synthetic data:

- 3,000 random instances small enough to enumerate every order;
- three synthetic bases of 577 rules over the real space, their conditions
  drawn from random tickets and their actions from the truth or at random.

On the small instances the packing reached the exact loss in 2,318 of 3,000
with the most-capacity label in index order, and in 2,590 with the rule and
starts adopted. On the three synthetic bases the adopted finder certified 1.7%,
3.5% and 6.5% more than the first version, in 7 to 58 seconds. **None of it
touched rung 1's rules.** `H-g3` re-runs the comparison's validity half on its
own seeded instances.

**5.8 — The corpus counts duplicates, the space counts each point once.** On the
corpus a case and its twin have the same pool and the same truth, so they are
one signature with capacity two. The certificate counts cases, as the score
does.

---

## 6. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **H-g1 — The instances are the record's.**
  - The suite is green.
  - Every instance's coverage bound, rebuilt here, is the published one: 0.8784
    and 0.8531 over the space, each split's train ceiling to the last digit.
  - Every published searched score is at or under its bound. Every corpus score
    is a whole number of cases that four decimals name uniquely.
  - The signatures the certificate rests on score three random orders exactly as
    `score_order` does, on all twelve instances. **What the certificate bounds is
    what the search maximised.**
- **H-g2 — The one instance whose optimum is known.** On the hidden policy's pure
  pool the design order wins every case, on the corpus and on the space. So no
  cycle can exist there, and the certificate must find none. On its hybrid pool
  over the space the certificate must verify, and stay at or above the design
  order and the greedy order.
- **H-g3 — Validity where every order can be enumerated.** On 2,000 seeded
  random instances of at most seven rules:
  - the certified bound is never below the exact optimum;
  - `verify` accepts every certificate;
  - it refuses every certificate with a multiplicity inflated past a capacity.
- **H-g4 — The signature**, §8.

> **[NOTE 2026-10-17] Run before signature, as for every free plan since
> `PLAN_PRIMACY.md`: the plan, its package and its blocking checks.** The first
> three pass. `PYTHONHASHSEED=0 python3 -m bound.score --dry-run`, zero API
> calls, nothing written, 105 s, nearly all of it the suite. Without the dry
> run, `python3 -m bound.score` exits at the gate in 0.06 s and creates no
> directory.
>
> - **`H-g1`.** The suite is green, 1,671 tests, and green on 3.10 too. All
>   twelve instances reproduce their published bounds, and their signatures
>   score random orders as `score_order` does. The searched train counts are
>   884, 874, 879, 867 and 871 on the pure pool and 830, 819, 826, 809 and 802
>   on the hybrid one.
> - **`H-g2`.** On the hidden policy the certificate finds no cycle, on the
>   space's two pools and on the corpus's pure pool. It verifies, and the design
>   order wins every case.
> - **`H-g3`.** 0 invalid of 2,000. 1,770 tight, 1,174 with cycles, and all 1,174
>   inflated certificates refused.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 7. The stage — scoring (free)

**Deliverable.** `bound/score.py` → `results_bound/score.json`, and
`results_bound/FINDINGS_BOUND.md`, which owns every figure.

**What it does.** `H-g1` to `H-g4`, in that order and all blocking. Then, on the
twelve instances:

- the certificate, `verify` on it, and the check that `TB` stays at or above
  `A`;
- `CB`, `A`, `ν`, `TB`, the residue before and after, the share, and whether it
  met;
- H-a to H-d.

**H-e, reported:**

- **The structure the certificate rests on, per instance:**
  - the classes;
  - the uncontested and contested cases;
  - the signatures, and those with one right class with their cases;
  - the nodes and the cycles.
- **`ν` by cycle length, and by start**, with the start kept. The spread across
  the seventeen starts is the packing's own variance.
- **The certified bound as a share**, beside the coverage bound and `A`, on the
  surface each is measured on.
- **The certificate itself**: each cycle's multiplicity and one case per
  signature, so that anyone can run `verify` on it.

---

## 8. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money**
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §8): it is the order of events,
that §0 was signed before any figure that could inform it existed. The gate
reads `PLAN_BOUND.md` and no other plan, and counts signatures rather than
stopping at the first. Every line starting `**Signed by Sergi:` must be filled
in, and there must be at least one. The counting is `reuse/plan.py`'s, called
with this plan's path. No flag skips the gate; `--dry-run` runs `H-g1` to `H-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The five records of §1. `POOLS = (puro, hibrido)`,
  `N_SPLITS = 5`, `SPLIT_SEED = 17`, `N_SPACE = 134400`.
- **The finder.** `FINDER_SEED = 17`, `FINDER_STARTS = 16`; the label rule and the
  order of cycle lengths in `bound/certificate.py`'s header.
- **The checks.** `PLUMBING_SEED = 17`, `PLUMBING_ORDERS = 3`;
  `BRUTE_SEED = 17`, `BRUTE_INSTANCES = 2000`, `BRUTE_MAX_RULES = 7`.
- **The lines of §0.** `0.50`, `0.50` and `0.75`; `SPACE_PLACES = 4`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
bound/__init__.py
bound/plan.py          the gate and the constants of this section
bound/certificate.py   the argument, the finder, verify, and brute force
bound/instances.py     the twelve instances, the hidden policy's, and what the records publish
bound/gates.py         H-g1 to H-g4
bound/score.py         the stage: H-a to H-d, the readings of H-e
tests/test_bound.py
results_bound/score.json
results_bound/FINDINGS_BOUND.md
```

**The plumbing, in the same commit as the modules.** Each of these lists has
drifted before when it was left for later:

- `bound` joins `CODE_ROOTS` in `harness/provenance.py`, and the roots the oracle
  scan walks in `tests/test_oracle_separation.py`.
- `tests/test_writer_lists.py` names the new root.
- The README's table of writers gains `bound/score.py`'s row, and its list of
  dry runs gains `bound/score.py --dry-run`.

**The list of modules allowed to see the oracle does not grow.**

---

## 9. Definition of done

- [ ] `results_bound/score.json` with `_env`, produced with `PYTHONHASHSEED=0`
      from a clean tree.
- [ ] `H-g1` to `H-g4` passed before any record was written; every certificate
      verified, and none below a searched score.
- [ ] The plumbing of §8, and tests pinning the constants of §8 and the argument
      of §3 by hand; the whole suite green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface and its pool.
- [ ] `results_bound/FINDINGS_BOUND.md` owns every figure, with a dated erratum
      wherever it corrects something already published, including any wording
      that reads the bound on these instances as attainable.
- [ ] `STATUS.md`:
  - the scoreboard gains the `H` thread, four adjudicated rows and one reported;
  - the first open item gets what the certificate showed, on each surface and
    pool.
- [ ] `IDEAS.md`:
  - the entry answered as far as the certificate goes;
  - §2.1's correction to its description of the hybrid pool;
  - what §10 leaves.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 10. What this plan cannot settle, declared before it runs

1. **The remainder.** Whatever lies between `TB` and `A` is slack the certificate
   cannot see, search weakness, or both (§5.1, §5.2). Three steps would narrow
   it, in increasing cost:
   - **A stronger certificate.** The atom's exact loss of §5.6. Or the exact
     least loss over small blocks of rules: by dynamic programming over subsets,
     it is a lower bound for the cases whose right rules all lie in the block.
     Both are free and stay certified.
   - **A longer search**, which moves `A`. `MULTISTART_STARTS` is declared and
     not tunable (`CLAUDE.md`). A search run for this purpose would be a new
     instrument, with its own check before any figure.
   - **Exact optimisation.** A MIP or MaxSAT over pairwise order variables,
     restricted to the pairs that overlap, as `IDEAS.md` names it, reporting the
     solver's gap if it does not converge. It needs a solver the standard library
     does not have, pinned apart as `requirements-ilp.txt` pins `clingo`.
2. **The test halves.** No order was searched there, so a bound on them says
   nothing about the search.
3. **Other bases.** The certificate runs on any instance. `PLAN_REUSE.md`'s and
   later bases are not in the rows, and their partition leaves little overlap to
   bound.
4. **Rung 4's figures.** Its sweeps use the same optimizer on labels that are
   not the truth. A bound there would bound a different objective.
5. **The attainable side `IDEAS.md` names.** `rung3/mfas_compilation.py`
   compiles declared edges into an order; it keeps untouched rules in arrival
   order and has no restarts (`FINDINGS3.md` §13). The audited search already
   reaches the best published scores, so the minimum-feedback-arc-set route is
   not run here.
