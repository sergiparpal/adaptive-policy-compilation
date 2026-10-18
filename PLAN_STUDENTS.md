# PLAN_STUDENTS — what the proposer's rules buy over a learner fitted to its answers

> **[CLOSED 2026-10-18] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-10-18, before any figure of the plan existed. The five rows were
> adjudicated the same day: **`T-a`, `T-b` and `T-c` hold; `T-d` and `T-e` are
> refuted**, `T-e` thinly, and `T-f` is reported. Where tickets arrive the rules
> beat every student of their answers. Over the function the tree beats them in
> arrival order and loses to them read newest first. **The figures are owned by
> [`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md)**,
> and no result is to be read off this file; the scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-10-18. The line is kept
> unedited and this banner is its correction. The banner touches neither §0 nor
> its note, adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-10-18, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §10 says why the gate binds anyway.

**This plan exists because the cheapest competitor the proposer has has never
been run on its own answers.** At every escalation the proposer did two things:
it named a queue for the ticket, and it wrote a rule whose body says which
tickets that queue is for. The loop keeps both. Every figure the repository
holds for the rules credits the pair. **None separates them.** The question is
what the rule bodies add over a cheap learner trained on the queues alone, from
the same tickets and labelled the same way.

[`IDEAS.md`](IDEAS.md) carries the item, from the outside reading of October
2026: *students on the proposer's own answers*, the baseline the survey ranks
first, after Cache & Distil and Online Cascade Learning. **One such student has
run.** §8 of [`results_ilp/FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md) trained
`PLAN_ILP.md`'s inducer on the queues the proposer chose, and the proposer's
rules in arrival order beat it. That was one unregularised inducer, which fits
noisy labels case by case. §8 names that limit, and this plan answers it.

**What it would change.**

- **If a pruned decision tree on the same answers matches the rules where
  tickets arrive**, the rule bodies add nothing a tree fitted to the queues does
  not, and the tree is symbolic too: its leaves are rules in this repository's
  own DSL. The case for rules written one ticket at a time would then have to
  rest on something other than being symbolic. That is `T-a`.
- **If it does not**, the bodies carry something the answers alone do not
  recover, on this corpus and with this proposer. The founding mechanism would
  then beat its cheapest symbolic competitor on matched information, which
  nothing in the repository shows today.
- **Either way, the surface matters.** §8 of `FINDINGS_ILP.md` found its student
  losing on the arrivals and winning as a function. `T-c` asks whether a
  regularised learner splits the same way.

**And the rules get the same treatment.** A student is fitted to the answers,
and the rules in arrival order are fitted to nothing. `T-d` gives the rules that
step too: rung 3's search, with the proposer's answers where it had the truth.
That also says how much of the gap between arrival order and the searched order
the oracle paid for, which `IDEAS.md` asks and nothing has measured.

**None of this plan's figures exists**, so under
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable, although
it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic, its denominator and its surface here, before
any figure.**

- **The answers** are the queues the proposer named at the escalations of a run,
  each with its ticket (§1). On rung 1's record they are **579**: the
  escalations whose proposal named a queue, as `ilp/chosen.py` reads them.
- **A student** is one of three learners declared in §3: the **tree**, the
  **logistic** regression and the **cache**'s nearest-neighbour retrieval. Each
  is trained on tickets and answers and nothing else.
- **The rules in arrival order** are the run's rules executed first-match by
  birth, on rung 3's `puro` pool: **519** of the 995 cases of corpus test split 0
  and **42,310** of the space's 134,400 points
  ([`results3/floor_by_pool.json`](results3/floor_by_pool.json), 0.521608 and
  0.314807).
- **Corpus test split 0** is rung 3's split of the corpus of seed 17, seed 17:
  995 cases. **The space** is the 134,400 combinations. Every count is of
  decisions that are right against the truth. A case an engine leaves in
  CONFLICT or IMPASSE counts as not right, as in every end-to-end figure in the
  repository. A student always answers.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **T-a** | **A tree on the proposer's answers does not match its rules where tickets arrive.** | corpus test split 0, 995 cases: right decisions of the pruned tree trained on rung 1's 579 answers, against the rules in arrival order's 519 | **tree < 519** | **tree ≥ 519** |
| **T-b** | **No student matches them.** | the same denominator: the most right decisions among the three students, each trained on the 579 answers | **best < 519** | **best ≥ 519** |
| **T-c** | **Over the function, the tree beats them.** | exhaustive space, 134,400 points: right decisions of the tree of `T-a`, against the rules in arrival order's 42,310 | **tree > 42,310** | **tree ≤ 42,310** |
| **T-d** | **Ordered with the proposer's own answers, the rules do better than in arrival order.** | corpus test split 0: right decisions of rung 3's search over the 577 rules, `puro` pool, its declared constants, labelled with the answers of the 286 escalations in split 0's train half, against 519 | **order > 519** | **order ≤ 519** |
| **T-e** | **On `PLAN_REUSE.md`'s loop the tree does not match the base either.** | corpus test split 0: per run, the tree trained on that run's answers (62, 31 and 42) less the run's final base under rung 2's engine with its installed edges, in right decisions; the median of the three runs | **median < 0** | **median ≥ 0** |
| **T-f** | *Reported, not adjudicated.* **What reading the rows needs.** | §9's readings: every student on every set and surface; the same students handed the truth; the rules' other executions; the rare classes; the reach; the tree written in the DSL; the discordance behind each label | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-18)**

**One label, and it does not change a verdict.** `T-a`, `T-b`, `T-d` and `T-e`
compare two artefacts on the same 995 cases. For each, the record gives the
discordant cases: `b`, where only the first is right, and `c`, where only the
second is. **A verdict is labelled *thin* when `|b − c| < 2·√(b + c)`**, about
two standard errors of a paired difference. `T-b` is labelled on its best
student and `T-e` on its median run. `T-c` is read on the whole space, a fixed
population, and carries no label.

**What a hold says and what a refutation says.**

- **`T-a` holding** says the rule bodies carry something a tree fitted to the
  same answers does not recover, where tickets arrive. It does not say the rules
  are good: arrival order is 0.5216 of the test split, and the oracle-searched
  order 0.8472.
- **`T-a` refuted** says the answers alone suffice, on the arrivals, for a
  learner that is itself a rule base. It does not say the loop is useless,
  since both artefacts need the loop's calls to exist (§12.4).
- **`T-c`** is read beside the rules' best order that reads no truth, reversed
  arrival, which reaches 76,180 over the space. A tree beating arrival order
  over the function and losing to its reverse would say the order costs the
  rules there, not their bodies.
- **`T-d` holding** says the proposer's answers, the only labels a deployment
  has, can order its rules beyond their arrival. Refuted, it says the gain from
  searching the order was the oracle's.

**Why the lines are where they are.** Every line is a comparator's own figure,
so each row asks which of two artefacts is right more often, and nothing else.
Ties go to the student in `T-a`, `T-b` and `T-e`: *matches* means at least as
many right. They go against the claim in `T-c` and `T-d`, whose claims say
*beats*.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **The documents.** `STATUS.md` with its scoreboard and *What is open*;
  `IDEAS.md` entire; `ARBITRATION_REPORT.md`, `CHAT_SUMMARY.md` and
  `EXTERNAL_REVIEW.md`, read before this plan was drafted, as `CLAUDE.md`
  requires; [`PLAN_ILP.md`](PLAN_ILP.md) and `FINDINGS_ILP.md` with every
  erratum, §§7 and 8 included; [`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md)
  entire; [`results_screen/FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md)'s
  Stage C; `PLAN_BOUND.md`, as the form a free plan takes.
- **The records' published figures**, read for this plan:
  - `results3/floor_by_pool.json`: every floor, both pools, every surface;
  - `results3/order_search_ls.json`: split 0's two rows;
  - `results3/order_search.json`: `references_split0`, rung 1's own engine at
    0.1829 among them;
  - `results/frontier.json`: the three cache rows and `keep_k`'s;
  - `results_ilp/labels.json`: the proposer's queues by true class;
  - `results_ilp/chosen.json`: the four lists on the proposer's queues, 424,
    437, 451 and 413 of 995, and their space figures;
  - `results_reuse/structure.json`, through `FINDINGS_REUSE.md`'s tables.
- **Facts about the material, counted by the drafter** (§1): how many answers,
  how many right, how many in each half, their queues, their reach into the test
  split, and the test split's class counts. None is a score of any student or
  order.
- **The code**: `ilp/`, `harness/` (the domain, the DSL, the cache, the policy,
  the proposers), `rung2/engine2.py`, `rung3/`'s order search, local search and
  floors, `edges/rebuild.py`, `reuse/plan.py`, `bound/`, and the tests that keep
  the oracle out and the writers listed.
- **The blocking checks' output** (§8), which prints pass or fail and figures
  already published or known by construction.
- **Not seen, because nobody has computed them**: any student's figure, on any
  set or surface; the order searched on the answers; the order searched on the
  truth at the same 286 tickets; the `PLAN_REUSE.md` bases' scores on test split
  0 or over the space under rung 2's engine; rung 1's own engine over the space.

**What the drafter expects, written down so the scoreboard can score it.**
`T-a`, `T-b`, `T-c` and `T-e` hold; **`T-d` is refuted**. The drafter trusts
`T-e` least, then `T-b`.

- **`T-a`, about seven in ten.** The answers are right on 245 of the 579, and
  their errors are systematic. Of the 200 `SELF_SERVICE_DEFLECT` tickets whose
  proposal named a queue, 37 were named that queue. A learner that reproduces
  the answers reproduces those confusions. On the 347 test cases its tickets
  reach, it is right about where the proposer was: 124 of the 293 test-half
  answers are right. The unregularised inducer on the same answers scored 424 and
  437 of 995. Pruning should lift that, by an amount the drafter guesses at 20 to
  60 cases, short of 519.
- **`T-b`, about six in ten.** The cache returns the proposer's own answer on
  every test case its tickets reach, so it inherits the answers' accuracy there
  and is the weakest of the three. The logistic regression is a smoother version
  of the same answers, and the drafter does not see where it would find 519.
- **`T-c`, about four in five.** The answers send security-keyword tickets to
  `SECURITY_INCIDENT`: 13 of them name that queue. Half of the space carries the
  keyword, and three quarters of that half is `SECURITY_INCIDENT`.
  `FINDINGS_ILP.md` §8 traced its student's win over the space to that one
  mapping. If pruning keeps the split, the tree clears 42,310. If it does not,
  the drafter guesses it lands below 0.30 of the space, and the row fails.
- **`T-d` refuted, about six in ten.** Fitting the order to the answers promotes
  the rules that agree with the proposer's commonest queues, `T2_TECHNICAL` and
  `T1_GENERAL`, over the rules that would decide a ticket otherwise. Two things
  argue the other way. The later of two identical rules is the better one more
  often (`FINDINGS3.md` §18). And reversed arrival, which favours later rules,
  reaches 544.
- **`T-e`, about even, leaning to a hold.** The bases were written from these
  answers by a proposer that saw the base, and their rules are broad. The tree
  has 31 to 62 answers to learn from, and 29 of run 1's 62 name
  `SECURITY_INCIDENT`, most of them the queue of a copy written to hang an edge
  on.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 33
of 79 adjudicated rows came out refuted. **These bands are more likely too
comfortable than too strict**, and the signature can tighten them.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls. No loop runs; one search is re-run, rung
3's own, on new labels.

**Already paid for, and read as they stand:**

- `results/llm_run.json`: rung 1's 2,000 records and 577 rules. **The answers
  are its 579 escalations whose proposal named a queue**: 632 escalated, 34
  proposals failed and 19 named none. `ilp/chosen.py`'s `chosen` reads them, and
  this plan calls it. 245 of the 579 are right.
- `results_reuse/run_n2000_r1.json` to `_r3.json`: `PLAN_REUSE.md`'s three runs.
  **Their answers are their escalations**: 62, 31 and 42, every proposal parsed,
  right on 30, 15 and 23. Their bases are rebuilt by `edges/rebuild.py`'s
  `rebuild`, which `PLAN_EDGES.md`'s `W-g3` holds equal to the records.
- The comparators' published figures: `results3/floor_by_pool.json`,
  `results3/order_search_ls.json`, `results3/order_search.json`,
  `results/frontier.json`, `results_ilp/chosen.json` and
  `results_ilp/compare.json`.

**The material, by set.** These are the counts the drafter took from the
records, and `T-g1` recomputes them before anything else runs:

```
                       answers  right  train half  test half  reach into test split 0
rung 1                     579    245         286        293      347 of 995
PLAN_REUSE.md run 1         62     30          33         29       32
PLAN_REUSE.md run 2         31     15          12         19       22
PLAN_REUSE.md run 3         42     23          21         21       25
```

The **reach** is the number of test cases whose ticket is identical to a
training ticket, which `CLAUDE.md` asks a baseline to declare. **A train half
reaches nothing**: rung 3's split groups cases by identity.

**Their queues.** Rung 1's answers name every queue: `T2_TECHNICAL` 245,
`T1_GENERAL` 129, `BILLING_SPECIALIST` 107, `SELF_SERVICE_DEFLECT` 63,
`SECURITY_INCIDENT` 13, `T3_ENGINEERING` 13, `ONCALL_ESCALATION` 7 and
`ACCOUNT_MANAGER` 2. Each of `PLAN_REUSE.md`'s runs names five:
`T1_GENERAL`, `T2_TECHNICAL`, `SELF_SERVICE_DEFLECT`, `BILLING_SPECIALIST` and
`SECURITY_INCIDENT`, the last on 29, 7 and 10 of them. 545 distinct tickets
carry rung 1's 579 answers, and 12 of them carry more than one answer.

**Corpus test split 0, by true class**: `T2_TECHNICAL` 364,
`SELF_SERVICE_DEFLECT` 242, `BILLING_SPECIALIST` 136, `T1_GENERAL` 128,
`T3_ENGINEERING` 57, `ACCOUNT_MANAGER` 55, `SECURITY_INCIDENT` 10,
`ONCALL_ESCALATION` 3.

**The truth** enters only to score, and only through modules
`tests/test_oracle_separation.py` already allows: `ilp.instances.truths` for the
corpus, and `rung3.order_search.build_tables` and
`rung3.order_search_ls.space_truth_masks` for rung 3's masks and the space. No
module of this plan imports the oracle.

---

## 2. The choices that have to be made at signature time

Seven, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 The banded training sets are all the answers — the drafter recommends them

The rules were written from every answer, including the 293 whose tickets fall
in the test half. A student trained on the 286 of the train half would be handed
less than the rules had. **So the matched set is all the answers, and the rows
read it.** The train halves are reported beside every figure.

Matched means the same answers, not the same advantage. On the 347 test cases
it reaches, a student trained on all 579 holds the proposer's answer for that
very ticket, and the proposer was right on fewer than half of them. The rules
hold the same answers, through the rules born on those tickets. **No student is
handed the truth of any test case**, which is what made `FINDINGS_ILP.md`'s
+0.0342 an answer key (§7 of that record). §9 reports the 347 and the 648 apart.

### 2.2 The rules' side of `T-a` to `T-c` is arrival order — the drafter recommends it

- **It is how the loop left them**: the order they were compiled in, and the
  order §8 of `FINDINGS_ILP.md` set its student against.
- **It reads no truth and no label.**
- **Reversed arrival is better on both surfaces**, 544 and 76,180. It was found
  by looking (`CHAT_SUMMARY.md` §2.1), and nothing in a deployment would choose
  it over arrival without a measurement. It is reported beside every row.

The alternative is reversed arrival on every row. It would make `T-a` and `T-b`
easier to hold and `T-c` easier to refute.

### 2.3 `T-d`'s order is rung 3's protocol with the labels changed — the drafter recommends it

Rung 3 searched on the train half's labelled cases and scored on the test half.
Here the labelled cases are the 286 answers of the train half, labelled by the
proposer, and nothing else moves: the same pool, the same masks, the same
search, the same declared constants and tail. **That is `IDEAS.md`'s entry as
written.** The same search on all 579 answers is reported beside it. So is the
search on the truth of the same 286 tickets, which separates what the labels
cost from what having only 286 of them costs.

### 2.4 Three students, declared now, and the tree is the headline — the drafter recommends it

- **The tree**, because it is symbolic. A pruned tree is a partition of the
  space into rules of this DSL, the shape the proposer writes when it sees the
  base (`FINDINGS2.md`). If any student matching the rules would move the
  argument, it is this one.
- **The logistic regression**, the standard learner on one-hot categorical
  data, as a learner that is not a rule base.
- **The cache's retrieval**: `harness/cache_baseline.py`'s distance and
  tie-break, over a store of the answers. That file calls the cache *the null
  hypothesis of the whole project*, and it caches the truth *as if the LLM had
  given it*. This is the first time the cache holds what the LLM gave.

**No other learner is tried, and none is added after a figure exists.** `T-b`'s
*best* is a maximum over these three, fixed here.

### 2.5 Deferral's free half is left out — the drafter recommends it

`IDEAS.md`'s entry carries a free half of deferral: at the engine's own call
budget, where would a margin rule send its escalations, and are the seven
`ONCALL_ESCALATION` arrivals among them? **A static reading cannot say it.** A
cascade defers on what its own student is unsure of. That student would be
trained on the answers to its own deferrals, which are not the engine's
escalations, and those answers do not exist. A margin read off a student trained
on the engine's escalations says where that student is unsure. It says nothing
about what a cascade would have asked or learned. The question belongs with the
paid half, in a plan of its own (§12.2).

### 2.6 `PLAN_REUSE.md`'s loop is in, on one row — the drafter recommends it

It is the founding question's own loop, on the engine whose ceiling is 1.0000,
and `IDEAS.md` names its records. **Its material is thin and declared thin**:
31 to 62 answers a run; 29 of run 1's 62 name `SECURITY_INCIDENT`, most of them
a copy's queue; and five queues a run. `T-e` is the row the drafter trusts least. The alternative is to
report it and band nothing on it.

### 2.7 The thread's name and letter

`PLAN_STUDENTS.md`, rows `T-a` to `T-f`, for the *teacher* whose answers the
students learn. `A` to `F`, `H`, `I`, `K`, `L`, `M`, `O` to `S` and `U` to `Y`
are taken. The naming is Sergi's to overrule.

---

## 3. The students, exactly

Each is a function from tickets and labels to a predictor, and it reads nothing
else: no truth, no rule, no test case, no hidden policy. **Every choice below is
fixed here and pinned by a test**, and none is tuned after a figure exists.

**The folds, shared by both students that choose a parameter.** Five folds,
grouped by ticket: the training set's distinct tickets, sorted, are shuffled by
`random.Random(17)` and dealt in turn. Copies of a ticket never sit on both sides
of a fold. A training set of fewer than five distinct tickets would not be
foldable, and none is.

### 3.1 The tree

- **Splits.** Binary, over the attributes in `harness.domain.ATTRIBUTES` order:
  `attr lte t` for the two numeric attributes, at every value of the domain but
  the last; `attr eq True` for the two booleans; `attr eq v` for every value of
  the other four. A split's left branch is where the condition holds.
- **Growth.** A node is split while it is impure and some split separates its
  tickets. The split chosen is the one with the lowest weighted Gini impurity of
  the two children, computed exactly in rationals. Ties go to the first split in
  the order above. A node whose tickets are all identical stays a leaf.
- **Leaves.** A leaf answers the plurality of its labels. Ties go to the label
  more common in the whole training set, then to `ACTIONS` order.
- **Pruning.** Minimal cost-complexity pruning (Breiman et al., 1984), with
  `R(t)` the training labels misclassified at `t`. Weakest-link pruning gives the
  full tree's sequence of subtrees and its values `α₀ = 0 < α₁ < … < α_K`.
  `α` is chosen by the five folds: each fold grows and prunes its own tree, and
  each `k` is scored by the held-out labels misclassified by the fold's subtree at
  `β_k = √(α_k·α_{k+1})`, with `β_K = ∞`. The comparison is done exactly, on
  `β_k²`. **The `k` with the fewest misclassified wins; ties go to the larger
  `k`**, the smaller tree. The tree is the full tree's subtree `T_k`.
- **The tree is a rule base.** Each leaf is written as one rule of the DSL, with
  the conditions on its path merged to at most one per attribute, so that no
  rule passes the frozen validator's limit of eight:
  - `eq` for a single value;
  - for a numeric attribute, `lte` or `gte` for a range open on one side, and
    `in` over its values for a range bounded on both;
  - for any other attribute, `neq` for one value left out, and `in` over the
    values left for several.

  A root that is a leaf is written `severity gte 1`, the repository's catch-all.
  **The leaves are disjoint and cover the space**, so every engine in the
  repository decides them alike. `T-g2` checks that the frozen
  `harness.dsl.RuleEngine` executes them as the tree predicts.

### 3.2 The logistic regression

- **Features.** One indicator per value of every attribute, 47, in `DOMAINS`
  order, and a constant.
- **Classes.** The queues present in the training labels, in `ACTIONS` order.
  Every fold uses the same classes.
- **Objective.** The mean negative log-likelihood of the softmax plus
  `(λ/2)·‖W‖²` over every weight, the constant's included. With `λ > 0` it is
  strictly convex, so its minimum is unique, and the optimiser decides only how
  close it gets.
- **`λ`** from `10^(k/2)`, `k = −8, …, 2`, eleven values from `1e−4` to `10`,
  chosen by the five folds: the lowest mean held-out log-loss wins, and ties go
  to the larger `λ`.
- **Optimiser.** L-BFGS with ten pairs and Armijo backtracking, until every
  component of the gradient is at most `1e−7` in absolute value or 5,000
  iterations have run. Within a fold the grid is walked from the largest `λ`
  down, each fit starting from the previous one's weights. The final fit, on
  every example at the chosen `λ`, starts from zero. Since each fit's minimum is
  unique, the start changes how many iterations a fit takes and nothing else.
  `T-g2` checks the gradient of every fit the dry run makes, and the stage
  records the largest final gradient of every fit it makes.
- **Prediction.** The class of highest probability; ties go to `ACTIONS` order.

### 3.3 The cache

- **Distance.** The number of attributes on which two tickets differ, the
  frozen `harness/cache_baseline.py`'s `_dist`.
- **The store.** The training tickets in arrival order, each with its label.
- **Prediction.** The label of the first stored ticket at the smallest
  distance. **There is no maximum distance**: the student always answers.

The online cache stores only what it escalates and abstains beyond a distance.
**This is its retrieval, not its protocol.** `T-g2` shows that the distance and
the tie-break are the frozen file's: the same code, run through the online
protocol with the truth, reproduces `results/frontier.json`'s three cache rows.

### 3.4 How the students are scored

On corpus test split 0, case by case. Over the space, through the masks of
`rung2.engine2.Space`, in its bit convention:

- the tree, by its leaves' extensions;
- the cache, by each stored ticket's distance classes, built from the
  per-attribute masks;
- the logistic regression, point by point.

`T-g2` checks each mask route against the point-by-point prediction on a sample
of the space.

---

## 4. The rules' side, and the reference figures

### 4.1 What executes the rules

- **Arrival order**: rung 1's 577 rules first-match by birth on the `puro` pool,
  scored by `rung3.local_search.score_order` over `build_masks` on the test split
  and over `space_pools`. `T-g1` reproduces 519 and 42,310.
- **The order searched on the answers** (`T-d`): `rung3.order_search_ls.search`,
  the greedy and then the declared multi-start, over the `puro` pool's masks
  labelled with the proposer's queues at the 286 train-half answers. Scored the
  same way. `T-g1` runs the same call on split 0's train half with the truth and
  reproduces the published row.
- **`PLAN_REUSE.md`'s bases** (`T-e`): each run's engine as the run left it,
  every rule born and every edge installed. It is the engine at the end of
  `edges.rebuild.rebuild`, run with the declared directions. Test cases are
  decided by its `decide`. Over the space, each rule's undefeated region is its
  extension less those of the rules that beat it, and a point is decided where
  its undefeated rules agree. `T-g1` checks that the rebuild decides every case
  of its run as the record did, and that the region route decides every corpus
  case as `decide` does.

### 4.2 Reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | surface | owning record |
|---|---|---|---|
| rung 1's rules in arrival order | 519 of 995 · 42,310 of 134,400 | test split 0 · space | `results3/floor_by_pool.json` (0.521608, 0.314807) |
| the same, reversed | 544 · 76,180 | test split 0 · space | the same (0.546734, 0.566815) |
| rung 1's own engine, specificity | 0.1829 | test split 0 | `results3/order_search.json`, `references_split0` |
| the searched order, with the truth | 843 · 0.6033 | test split 0 · space | `results3/order_search_ls.json`, split 0, `puro` |
| the inducer on the proposer's queues | 424 and 437 (579), 451 and 413 (286) · 0.4425 to 0.4628 | test split 0 · space | `results_ilp/chosen.json` |
| the inducer handed the truth | 877 and 877 (632), 772 and 759 (316) | test split 0 | `results_ilp/compare.json` |
| the model asked with the ticket alone | 0.5458, 0.5074, 0.5260 | `PLAN_FIDELITY.md`'s held-out decisions over `PLAN_REUSE.md`'s bases | `results_screen/score.json` |
| the corpus's majority class | 0.363 | the 2,000 | `results/frontier.json` |

**The ticket-alone figures are context, not a comparator.** They come from
another prompt, another date and another population. They say roughly what a
student that learned the model's answers perfectly could reach on arrivals like
these.

---

## 5. `CLAUDE.md`'s four conditions for a baseline set against the proposer

1. **Which side had the label.** Neither. **Every label a student is trained on
   is a queue the proposer chose**, read off the record as `predicted`. Every
   queue a rule carries is the proposer's too. The truth enters only to score,
   on both sides alike. The references *handed the truth* in §9 are labelled
   so and are never a row.
2. **Checked against the code, not recalled.** Rung 1's
   `OpenRouterProposer.propose` drops the `true_action_hint` the loop passes it,
   and `tests/test_llm_path.py` pins that the truth never reaches the prompt.
   Rung 2's `propose(case, base_text)` admits no truth at all. `T-g3` checks,
   for every student the stage trains on answers, that its labels are the
   record's `predicted` exactly. Where the record marks a proposal wrong, they
   differ from the truth.
3. **How far the training examples reach into the test split.** All the
   answers: 347 of 995 test cases on rung 1, and 32, 22 and 25 on
   `PLAN_REUSE.md`'s runs. The train halves: none. Through answers, never
   through the truth (§2.1).
4. **The control on the proposer's answers.** It is the design: every row trains
   on them. The students handed the truth at the same tickets are reported
   beside, which says what the labels cost.

---

## 6. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** `harness/cache_baseline.py` and
   `harness/dsl.py` are called, never edited. If a frozen file has a bug, stop
   and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise the loop.** Nothing here runs it.
4. **Seed 17, no regeneration, and every record this plan reads is read-only.**
5. **Do not adjust a prompt or a schema.** Nothing here touches either.
6. **If the numbers come out badly, report them.**
7. **No API key is needed**, and none is loaded.

And this plan's own, lettered:

A. **The repository's functions are called, not copied**: `ilp.chosen.chosen`
   for rung 1's answers; `ilp.instances` for the corpus, the split and the
   truth; `rung3.order_search`, `rung3.local_search` and `rung3.order_search_ls`
   for the pool, the masks, the search and the space; `edges.rebuild.rebuild` for
   `PLAN_REUSE.md`'s bases; `harness.dsl` to write and execute the tree;
   `harness.cache_baseline.run_cache_baseline` in the cache's check. A second
   construction that drifted from the first would score something no record
   describes.
B. **The records are inputs, never outputs.** Nothing outside
   `results_students/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §3 and §10 are fixed here and pinned by tests**, so that
   moving one after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow (§1).
F. **The dry run trains no student on the proposer's answers, searches no order
   on them, and rebuilds no base's score.** It prints pass or fail and figures
   already published or known by construction. `tests/test_students.py` walks
   `students/gates.py`'s syntax tree to say so.
G. **Every route to a figure is checked against a second route** before the
   figure is believed:
   - the tree against its own rules under the frozen engine, on every test case;
   - every student's space masks against point-by-point prediction;
   - every order's count against `score_order`'s;
   - rung 1's engine and each base's regions against a decision taken case by
     case, on the test split and on 2,000 points of the space.

   A disagreement stops the stage before anything is written. It would mean
   the instrument is wrong, not that a row came out one way.

---

## 7. Known traps

**7.1 — The answers are not a sample of the arrivals.** They are where the loop
asked, which the rules chose: on rung 1, 594 of the 632 escalations were
CONFLICTs. A student learns the proposer's answers where the loop asked, exactly
as the rules did. That is the matched information, and it is also why neither
side has seen most of `T3_ENGINEERING` (six answers) or any `ONCALL_ESCALATION`
ticket. **Selective labels**, in `IDEAS.md`'s term, on both sides alike.

**7.2 — On the 347 test cases its tickets reach, a student holds the
proposer's own answer.** The cache returns it. The tree and the regression
smooth it. On those tickets the proposer was right less than half the time, so
this reach lowers a student's score as often as it raises it. §9 reports the
347 and the 648 apart, as `FINDINGS_ILP.md` §7 did.

**7.3 — Abstention counts as not right, and only the engines abstain.** Rung 1's
own engine abstains on much of what arrives: in the run's last tenth 0.67 of
the arrivals escalated, and over the run 594 of the 632 escalations were
CONFLICTs (`results/llm_run.json`).
That is why it scores 0.1829, and why it is reported rather than banded. `PLAN_REUSE.md`'s bases
decide nearly every arrival, so `T-e` is little moved by it. Over the space they
abstain much more, and §9 reports how much.

**7.4 — A student cannot predict a queue nobody named.** No student of
`PLAN_REUSE.md`'s answers can predict `T3_ENGINEERING`, `ACCOUNT_MANAGER` or
`ONCALL_ESCALATION`. Rung 1's answers name `ACCOUNT_MANAGER` twice. The rules
have the same limit, through the same answers.

**7.5 — The cache here is its retrieval, not its protocol** (§3.3). A cache
running its own loop would escalate other tickets, and their answers do not
exist.

**7.6 — The space is not the arrivals.** Half of it carries the security keyword,
against 3% of arrivals. **Every row that bet a quantity would carry across a
change of surface lost** (`IDEAS.md`, rung 3's standing note). `T-a` and `T-c`
together bet the other way: that the sign of the comparison changes with the
surface. That side has won once, `S-e`, and lost once on its direction, `H-d`.

**7.7 — Twelve tickets carry two answers.** Each student treats them by its own
rule: the plurality of a leaf, the likelihood's sum, the first stored. The rules
carry both, as two rules.

**7.8 — `T-b`'s maximum is over three students fixed in §2.4.** It is a declared
statistic, not a selection after the fact. Read it with that in mind all the
same: of three draws, the best is likelier to clear a line than any one of them.

**7.9 — `PLAN_REUSE.md`'s answers are not rung 1's.** The proposer saw the base,
was asked under v1, and on a CONFLICT answered with a copy of the rule it wanted
to win. Its queue at those escalations is its answer, and the students learn it
as such.

---

## 8. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **T-g1 — The material and the comparators are the records'.**
  - The suite is green.
  - Rung 1's answers are 579, 245 of them right, as `results_ilp/labels.json`
    counts them, with its per-class counts. 286 fall in the train half, as
    `results_ilp/chosen.json` says.
  - `PLAN_REUSE.md`'s answers are 62, 31 and 42, and their right counts are
    each record's own `proposal_action_accuracy`.
  - The reach of §1 recomputes, for every set.
  - Arrival order reproduces 519 of 995 and 42,310 of 134,400, and its reverse
    544 and 76,180.
  - Rung 3's search, run here with the truth on split 0's train half, reproduces
    the published `puro` row: 0.8786, 0.8472 and 0.6033. **The order of `T-d` is
    that call with its labels changed.**
  - Each `PLAN_REUSE.md` base, rebuilt, decides every case of its run as the
    record did. The region route decides all 2,000 corpus cases as `decide` does,
    for every base.
  - `rung3.order_search.eval_specificity` reproduces 0.1829, and rung 1's engine
    over the space, as masks, decides every corpus case as it does.
- **T-g2 — Each student gives the answer where it is known.**
  - **The tree recovers the policy.** Handed the truth of all 134,400 points, the
    declared procedure, growth and pruning by the five folds, returns a tree
    that scores 134,400 of 134,400. Its leaves validate under
    `harness.dsl.validate_rule_payload`, and their masks are pairwise disjoint
    and cover the space. The frozen `RuleEngine`, run on the corpus and on
    2,000 seeded points, decides each by exactly one of them, with no CONFLICT
    and no IMPASSE, as the tree does.
  - **The cache is the frozen file's.** Its online protocol, run with the
    truth at distances 0, 1 and 2, reproduces `results/frontier.json`'s three
    cache rows, and the frozen `run_cache_baseline` gives the same.
  - **The regression reaches its optimum.** On seeded synthetic instances, the
    analytic gradient matches central finite differences, every fit ends with
    its gradient within tolerance, and two fits give identical weights.
  - **Every mask route matches point-by-point prediction** on 2,000 seeded
    points of the space, for each student, on synthetic labels.
- **T-g3 — Nothing a student reads holds the truth.** The labels each set will
  hand a student are the record's `predicted`, exactly. They differ from the
  truth on every answer the record marks wrong, 334 of rung 1's 579 and 32, 16
  and 19 of `PLAN_REUSE.md`'s. The functions that fit take tickets and labels,
  and their signatures admit nothing else. No module of `students/` imports the
  oracle.
- **T-g4 — The signature**, §10.

> **[NOTE 2026-10-18] Run before signature, as for every free plan since
> `PLAN_PRIMACY.md`: the plan, its package and its blocking checks.** The first
> three pass. `PYTHONHASHSEED=0 python3 -m students.score --dry-run`, zero API
> calls, nothing written, 200 s, most of it the suite. Without the dry run,
> `python3 -m students.score` exits at the gate in 0.06 s and creates no
> directory.
>
> - **`T-g1`.** The suite is green, 1,821 tests, and green on 3.10 too. Every
>   count of §1 recomputes, and rung 1's answers are `labels.json`'s, class by
>   class. Arrival order gives 519 and 42,310, and its reverse 544 and 76,180.
>   Rung 1's own engine gives 0.1829. The search with the truth gives 0.8786,
>   0.8472 and 0.6033. The three bases rebuild with no case decided otherwise,
>   and every mask route of the rules' side decides every corpus case as its
>   engine does.
> - **`T-g2`.** Handed the truth of the space, the tree scores 134,400 of
>   134,400 with 59 leaves, and the folds prune none of them. The leaves are
>   valid rules, disjoint and covering, and the frozen engine executes them as
>   the tree predicts. The cache's three rows reproduce at distances 0, 1 and
>   2. The gradient matches finite differences to 5e−8, every synthetic fit
>   converges, and no mask route disagrees with its student.
> - **`T-g3`.** Every set's labels are the record's `predicted`, and they differ
>   from the truth exactly where the record marks the proposal wrong.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 9. The stage — scoring (free)

**Deliverable.** `students/score.py` → `results_students/score.json`, and
`results_students/FINDINGS_STUDENTS.md`, which owns every figure.

**What it does.** `T-g1` to `T-g4`, in that order and all blocking. Then:

- the three students on rung 1's two sets and on each `PLAN_REUSE.md` run's
  two sets, scored on corpus test split 0 and over the space;
- the order searched on the answers;
- each `PLAN_REUSE.md` base under rung 2's engine, on both surfaces;
- `T-a` to `T-e`, each with its discordance and its label.

**T-f, reported:**

- **Every student on every set and surface**, with the train halves beside the
  banded sets.
- **The same students handed the truth** at the same tickets, labelled so.
  Beside them, the inducer's published figures handed the queues and the truth.
- **The rules' other executions**: reversed arrival; rung 1's own engine, on
  the test split as published and over the space, with its abstentions; the
  order searched on all 579 answers; the order searched on the truth at the
  same 286 tickets; the published searched order; each `PLAN_REUSE.md` base in
  arrival order.
- **The rare classes**: right decisions on `ACCOUNT_MANAGER`,
  `T3_ENGINEERING`, `SECURITY_INCIDENT` and `ONCALL_ESCALATION`, on the test
  split, for every student and every execution of the rules.
- **The reach**: on rung 1's 579, every figure on the 347 test cases its tickets
  reach and on the other 648.
- **The tree written in the DSL**: its rules, each with its queue and its
  training counts, and the size of every tree.
- **Agreement and discordance**: how often each student decides a test case as
  the rules in arrival order do, and the `b` and `c` behind each label.
- **The majority answer**: the proposer's commonest queue, answered everywhere,
  as a floor below every student.

---

## 10. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money**
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §8): it is the order of events,
that §0 was signed before any figure that could inform it existed. The gate
reads `PLAN_STUDENTS.md` and no other plan, and counts signatures rather than
stopping at the first. Every line starting `**Signed by Sergi:` must be filled
in, and there must be at least one. The counting is `reuse/plan.py`'s, called
with this plan's path. No flag skips the gate; `--dry-run` runs `T-g1` to `T-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The records of §1. `N_CORPUS = 2000`, `CORPUS_SEED = 17`,
  `SPLIT_SEED = 17`, `N_SPACE = 134400`, `REUSE_RUNS = (1, 2, 3)`.
- **The folds.** `FOLDS = 5`, `FOLD_SEED = 17`.
- **The tree.** Gini, exact; the splits and tie-breaks of §3.1; pruning by
  cost-complexity, the fewest held-out errors, ties to the smaller tree.
- **The regression.** `LAMBDAS = 10^(k/2)` for `k = −8 … 2`; `LBFGS_MEMORY = 10`,
  `ARMIJO = 1e−4`, `GRADIENT_TOL = 1e−7`, `MAX_ITER = 5000`.
- **The cache.** No maximum distance; the first stored wins a tie.
- **The checks.** `MASK_CHECK_SEED = 17`, `MASK_CHECK_POINTS = 2000`;
  `SYNTHETIC_SEED = 17`.
- **The lines of §0.** `519`, `42,310` and `0` (`T-e`'s median difference);
  the thin label's `2`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
students/__init__.py
students/plan.py        the gate and the constants of this section
students/material.py    the answers by set, their reach, and the truth's route
students/tree.py        growth, cost-complexity pruning, the folds, the DSL rules
students/logistic.py    the softmax, L-BFGS, the folds
students/cache.py       the retrieval, its online protocol, and its masks
students/rules.py       arrival order, the order on the answers, the bases of PLAN_REUSE.md
students/gates.py       T-g1 to T-g4
students/score.py       the stage: T-a to T-e, the readings of T-f
tests/test_students.py
results_students/score.json
results_students/FINDINGS_STUDENTS.md
```

**The plumbing, in the same commit as the modules.** Each of these lists has
drifted before when it was left for later:

- `students` joins `CODE_ROOTS` in `harness/provenance.py`, and the roots the
  oracle scan walks in `tests/test_oracle_separation.py`.
- The README's table of writers gains `students/score.py`'s row, and its list of
  dry runs gains `students/score.py --dry-run`.

**The list of modules allowed to see the oracle does not grow.**

---

## 11. Definition of done

- [ ] `results_students/score.json` with `_env`, produced with
      `PYTHONHASHSEED=0` from a clean tree.
- [ ] `T-g1` to `T-g4` passed before any record was written, and every second
      route of rule G agreed.
- [ ] The plumbing of §10, and tests pinning the constants of §3 and §10; the
      whole suite green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, and its pool or engine where an
      execution of rules is scored.
- [ ] `results_students/FINDINGS_STUDENTS.md` owns every figure, with a dated
      erratum wherever it corrects something already published.
- [ ] `STATUS.md`: the scoreboard gains the `T` thread, five adjudicated rows
      and one reported; *What is open* gets what the students showed.
- [ ] `IDEAS.md`: the entry answered as far as the rows go, and what §12 leaves.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **Three students, and we wrote them.** `T-g2` makes a loss readable: the tree
   recovers the policy when it is there, the cache is the frozen file's, and the
   regression reaches its optimum. Even so, these students losing is not
   distillation losing. Boosted trees or a larger model would need a dependency
   pinned apart, as `requirements-ilp.txt` pins `clingo`.
2. **Deferral, both halves.** The cascade's own escalations would not be the
   engine's, and their answers do not exist (§2.5). An online cascade at equal
   calls to the loop is a paid plan.
3. **One corpus, one policy, one proposer.** The answers come from one model,
   in two loops under prompts that differ, rung 1's and `PLAN_REUSE.md`'s.
4. **What the rules cost.** Both artefacts need the loop's calls to exist, so
   nothing here prices the loop. A student trained on the answers has the same
   bill as the rules, and the plan compares what each does with it.
5. **What the rules are for besides accuracy.** Their notes, their reuse counts,
   the edges hung on them. The tree is a rule base too, and §9 prints it, but
   whether it reads as well to a person is not a figure.
6. **The truth-free order the rules could have.** `T-d` is one way to order
   them with the answers. A label model over their agreements is another, and it
   is a separate item in `IDEAS.md`.
