# What the proposer's rules buy over a learner fitted to its answers — findings

Record opened on October 18, 2026, under [`PLAN_STUDENTS.md`](../PLAN_STUDENTS.md).
The plan, its package, the signature and the record below reached `main`
together, in pull request #136. Sergi signed §0 on 2026-10-18, before any figure
below existed, in a commit of its own: `424c4ab` on `main`, merged from
`e151c6e`.

The stage's record, [`score.json`](score.json), names in its `_env` the commit it
was written from: `e151c6e`, the signing commit on the branch. A rebase merge
gave it a new hash on `main`, `424c4ab`. The two have the same subject, the same
tree and the same `git patch-id --stable`.

**This record owns every figure in it.**

**A POST-RUN reading was added on 2026-10-18**: [`readings.json`](readings.json),
by `students/readings.py`, in its own section below. It reached `main` in pull
request #138. Its `_env` names `7575986`, the branch commit that wrote its
expectation, and that commit is `42ba325` on `main`: the same tree, the same
subject and the same `git patch-id --stable`. Its code digest,
`329454f4fbfef552`, is its own. It moves no verdict.

**The stage adjudicated the five signed rows on 2026-10-18: three hold and two
are refuted.**

- **Where tickets arrive, the rules beat every student trained on their own
  answers.** On corpus test split 0, a pruned decision tree on rung 1's 579
  answers is right on 470 of 995 cases. The 577 rules written from those answers
  are right on 519 in the order they were born (`T-a` holds). The logistic
  regression gets 466 and the cache 434, so the tree is the best of the three
  (`T-b` holds). Neither verdict is *thin*.
- **Over the function the tree beats the rules in arrival order and loses to
  them read newest first.** It is right on 59,466 of the space's 134,400 points,
  against arrival order's 42,310 (`T-c` holds) and reversed arrival's 76,180.
- **The proposer's answers do not order its rules; the truth at the same tickets
  does.** Rung 3's search, labelled with the answers of the 286 train-half
  escalations, orders the rules to 483 on the test split, below arrival order
  (`T-d` refuted). The same search on the truth of those same 286 tickets
  reaches 814: 91% of the searched order's gain over arrival, which used the
  truth of all 1,005 train cases.
- **On `PLAN_REUSE.md`'s loop the tree ties the base.** Per run, the tree on the
  run's answers less the run's final base under rung 2's engine is +1, +28 and
  −50 test cases. The median is +1 (`T-e` refuted, *thin*).

> **PROVENANCE: PRE-REGISTERED.** `T-a` to `T-e` were signed before any of their
> figures existed. **`T-f` is reported, not adjudicated**, and every figure in it
> is computed here for the first time. Nothing in this record was selected after
> the verdicts. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m students.score`, on 2026-10-18, from the signing
commit with a clean tree: 328 s, and zero API calls. The record is
[`score.json`](score.json). Its `_env` carries `git_dirty: false` and
`code_dirty: false`.

**The blocking checks passed again before any student was trained on the
answers.**

- **`T-g1`.**
  - The suite is green, 1,821 tests.
  - Every count of the plan's §1 recomputes.
  - Arrival order reproduces 519 and 42,310, and its reverse 544 and 76,180.
  - Rung 1's own engine reproduces 0.1829, and rung 3's search with the truth
    the published row: 0.8786, 0.8472 and 0.6033.
  - The three bases of `PLAN_REUSE.md` rebuild with no case decided otherwise.
- **`T-g2`.**
  - Handed the truth of the whole space, the tree scores 134,400 of 134,400
    with 59 leaves, and the folds prune none.
  - Its leaves are valid rules, disjoint and covering, and the frozen engine
    executes them as the tree predicts.
  - The cache's three frontier rows reproduce.
  - The regression's gradient matches finite differences to 5e−8.
  - No mask route disagrees with its student.
- **`T-g3`.** Every set's labels are the records' `predicted`. They differ from
  the truth exactly where the records mark the proposal wrong: 334 of rung 1's
  579.
- **`T-g4`.** Signed.

**And every second route of the plan's rule G agreed.** The tree's predictions
matched the frozen engine running its rules, on every test case. Every space
mask matched point-by-point prediction, and every order's count matched
`score_order`'s. Rung 1's engine and each base's regions matched decisions taken
case by case. A disagreement would have stopped the stage before it wrote
anything.

**Notation.** *Test* is corpus test split 0, 995 cases; *space* is the 134,400
combinations. Every count is of decisions right against the truth, and an
engine's CONFLICT or IMPASSE is not right. *Arrival* is rung 1's 577 rules
first-match by birth on rung 3's `puro` pool, and *reversed* the same rules
newest first. The students on *all* the answers are read against the rules,
which were written from all of them.

---

## The five rows

| row | statistic | value | line | discordance `b`, `c` | verdict |
|---|---|---|---|---|---|
| `T-a` | test: the tree on rung 1's 579 answers | **470** (0.4724) | < 519 | 84, 133 | **holds** |
| `T-b` | test: the best of the three students on the same answers, the tree | **470** | < 519 | 84, 133 | **holds** |
| `T-c` | space: the tree of `T-a` | **59,466** (0.4425) | > 42,310 | — | **holds** |
| `T-d` | test: rung 3's search on the 286 train-half answers | **483** (0.4854) | > 519 | 101, 137 | **refuted** |
| `T-e` | test: the median over `PLAN_REUSE.md`'s runs of the tree less the base | **+1** | < 0 | 10, 9 | **refuted, thin** |

`b` counts the cases only the row's artefact gets right, and `c` the cases only
its comparator does. A verdict is *thin* when `|b − c| < 2·√(b + c)`. Only
`T-e`'s is.

**`T-e`, run by run.** On the test split:

| run | answers | tree | base | difference | `b`, `c` | thin |
|---|---|---|---|---|---|---|
| 1 | 62 | 404 | 403 | **+1** | 10, 9 | yes |
| 2 | 31 | 476 | 448 | +28 | 141, 113 | yes |
| 3 | 42 | 476 | 526 | −50 | 28, 78 | no |

**The drafter expected `T-a`, `T-b`, `T-c` and `T-e` to hold and `T-d` to be
refuted, and trusted `T-e` least. Four of five came out as expected. The one
that did not is `T-e`, the one trusted least.**

### What the verdicts say

**1. On the arrivals, the rule bodies carry something the answers alone do not.**
The tree and the rules hold the same 579 answers, and the rules hold the scope
the proposer gave each one too. On the test split the rules in arrival order are
right on 49 more cases than the tree. They are right on 133 cases the tree gets
wrong, and the tree on 84 the rules get wrong. The regression and the cache fall
shorter still. **The case for rules written one ticket at a time survives its
cheapest competitors on the arrivals, the symbolic one included.** It does not
say the rules are good: arrival order is 0.5216 of the test split, and the
searched order 0.8472.

**2. Over the function it is the order that costs the rules, not their bodies.**
The tree beats arrival order over the space by 17,156 points, and reversed
arrival beats the tree by 16,714. Read newest first, the same rules beat all
three students of rung 1's answers on both surfaces: 544 of 995 and 76,180 of
134,400. §0 named this reading before the run: *a tree beating arrival order
over the function and losing to its reverse would say the order costs the rules
there, not their bodies*. It is what happened.

**3. The gain from searching the order was the oracle's, and it was the truth of
the labels, not their number.** On the same 286 tickets, the same search scores
483 on the test split labelled with the proposer's answers, and 814 labelled
with the truth. The proposer's answers order its rules 36 cases below arrival.
The truth at those 286 escalations recovers 295 of the 324 cases the full search
gains over arrival, which had the truth of 1,005 train cases. Over the space the
answers do order the rules above arrival, 61,305 against 42,310. On the test
split the one class where they help an order is `SECURITY_INCIDENT`, 9 of 10
against arrival's 3; the record does not split the space by class.

**4. On `PLAN_REUSE.md`'s loop the rules do not beat a tree on their answers.**
That loop's bases have 31 to 62 rules, written by a proposer that saw the base,
and the trees learn from 31 to 62 answers. One run goes each way and the median
run is a tie: a difference of one case, with 19 cases where the two disagree on
who is right. Over the space the trees beat all three bases (the readings
below).

---

## The readings of `T-f`

### Every student on every set

Right decisions. The train halves are the answers whose ticket falls in split
0's train half, and they reach no test case.

| set | answers | tree | logistic | cache | tree | logistic | cache |
|---|---|---|---|---|---|---|---|
| | | *test* | | | *space* | | |
| rung 1, all | 579 | **470** | 466 | 434 | **59,466** | 57,987 | 37,101 |
| rung 1, train half | 286 | 500 | 458 | 395 | 44,450 | 43,787 | 30,962 |
| `PLAN_REUSE.md` run 1, all | 62 | 404 | 365 | 355 | 71,800 | 70,080 | 57,597 |
| run 1, train half | 33 | 350 | 344 | 313 | 70,320 | 69,123 | 55,025 |
| run 2, all | 31 | 476 | 378 | 346 | 75,480 | 69,111 | 51,486 |
| run 2, train half | 12 | 480 | 348 | 331 | 75,000 | 58,985 | 48,947 |
| run 3, all | 42 | 476 | 468 | 391 | 75,480 | 74,776 | 51,175 |
| run 3, train half | 21 | 476 | 400 | 395 | 75,480 | 59,825 | 45,569 |

- **The tree is the best student on every set and surface.** The logistic
  regression is close behind it on rung 1's answers and on run 3's. The cache,
  `harness/cache_baseline.py`'s retrieval over the answers, is last everywhere.
  Over the space on rung 1's answers it is below arrival order, 37,101 against
  42,310.
- **On rung 1, the tree on the 286 train-half answers beats the tree on all
  579: 500 against 470 on the test split.** That is the reach, below. Against
  arrival order the train-half tree is short by 19 cases, *thin* (`b`, `c` = 79,
  98). Over the space it is barely above arrival, 44,450.
- **Sizes.** The tree on rung 1's 579 answers has 25 leaves, pruned from 196,
  and the one on the train half 8 of 100. The `PLAN_REUSE.md` trees have 2 to 6
  leaves. The tree on all of run 2's answers and both of run 3's score alike on
  both surfaces, 476 and 75,480. The record holds their sizes and not their
  rules.

### The reach

On rung 1's 579 answers, 347 test cases share a ticket with an answer, and 648
do not. On the 347 each student holds the proposer's answer for that very ticket.

| on the test split | the 347 | the 648 | all 995 |
|---|---|---|---|
| tree, all answers | 146 | 324 | 470 |
| logistic, all answers | 146 | 320 | 466 |
| cache, all answers | 154 | 280 | 434 |
| arrival | 173 | 346 | 519 |
| reversed arrival | 171 | 373 | 544 |
| the order on the 286 answers | 150 | 333 | 483 |
| the order on the truth at those 286 | 310 | 504 | 814 |

**Arrival order is ahead of the tree on both parts**, by 27 cases on the 347 and
by 22 on the 648. On the 347 the cache, which returns the answer it holds for
the ticket, is right on 154. The answers themselves are right there less than
half the time, and smoothing them, as the tree and the regression do, loses a
few more. The record does not split the train-half students' test cases this
way.

### The same students, handed the truth

The same tickets, labelled with their true queue: what the labels cost. These
are references and never a row.

| set | tree | logistic | cache | tree | logistic | cache |
|---|---|---|---|---|---|---|
| | *test* | | | *space* | | |
| rung 1, all | 954 | 918 | 706 | 72,400 | 66,150 | 41,900 |
| rung 1, train half | 894 | 850 | 573 | 55,640 | 54,242 | 31,751 |
| run 1, all | 625 | 512 | 454 | 101,675 | 71,613 | 62,168 |
| run 1, train half | 364 | 369 | 403 | 36,720 | 65,874 | 54,429 |
| run 2, all | 364 | 370 | 411 | 36,720 | 40,422 | 45,683 |
| run 2, train half | 364 | 367 | 318 | 36,720 | 36,932 | 39,866 |
| run 3, all | 716 | 558 | 424 | 75,580 | 43,023 | 41,670 |
| run 3, train half | 364 | 366 | 410 | 36,720 | 36,782 | 39,080 |

- **With the truth, the tree on rung 1's 286 train-half tickets is right on 894
  test cases**, above the searched order over the 577 rules, 843, which used
  the truth of 1,005 train cases. With the proposer's answers on the same
  tickets it is right on 500. On these tickets the labels cost the tree 394
  cases: handed the truth, a tree on the escalations' tickets beats the best
  order of the rules, and handed the answers it loses to their arrival order.
- **Handed the truth of all 579, it reaches 954**, but 347 of those test cases
  share a ticket with a labelled example. On the other 648 it is right on 607.
- **The inducer of `FINDINGS_ILP.md` handed the truth scored 877 on all 632 and
  772 and 759 on the 316** (`results_ilp/compare.json`). The pruned tree is the
  stronger learner on the same kind of material.
- Four of the `PLAN_REUSE.md` trees, handed 12 to 33 true labels, pruned to a
  single leaf: the majority queue, `T2_TECHNICAL`, right on 364 test cases and
  36,720 points of the space. The trees handed rung 1's truth pruned nothing:
  40 leaves on all 579 tickets and 29 on the train half.

### The rules' other executions

| execution of rung 1's 577 rules | test | space | abstains, test · space |
|---|---|---|---|
| arrival | 519 | 42,310 | 0 · 0 |
| reversed arrival | 544 | 76,180 | 0 · 0 |
| rung 1's own engine, specificity | 182 | 16,429 | 564 · 54,693 |
| the order on the 286 train-half answers | 483 | 61,305 | 0 · 0 |
| the order on all 579 answers | 510 | 59,540 | 0 · 0 |
| the order on the truth at the 286 | 814 | 73,420 | 0 · 0 |
| the searched order, published | 843 | 0.6033 | — |

The first-match orders never abstain. Every case and point some rule matches
is decided, and the 577 rules leave no point of the space unmatched
(`results3/order_search_ls.json`).

**And `PLAN_REUSE.md`'s bases**, each under rung 2's engine with its installed
edges, and the same rules in arrival order:

| run | rules | base, test | base, space | abstains, test · space | arrival, test | arrival, space |
|---|---|---|---|---|---|---|
| 1 | 62 | 403 | 41,160 | 6 · 34,440 | 411 | 36,540 |
| 2 | 31 | 448 | 39,660 | 1 · 11,340 | 453 | 35,880 |
| 3 | 42 | 526 | 74,400 | 1 · 2,520 | 523 | 40,360 |

On the test split the engine and arrival order differ by at most eight cases.
Over the space the engine abstains on 34,440, 11,340 and 2,520 points, and is
still right on more of them than arrival order, in every run.

### The rare classes

Right decisions on the test split, out of 55 `ACCOUNT_MANAGER`, 57
`T3_ENGINEERING`, 10 `SECURITY_INCIDENT` and 3 `ONCALL_ESCALATION` cases:

| | `ACCOUNT_MANAGER` | `T3_ENGINEERING` | `SECURITY_INCIDENT` | `ONCALL_ESCALATION` |
|---|---|---|---|---|
| tree, rung 1's answers | 0 | 0 | 7 | **3** |
| logistic | 0 | 2 | 8 | 0 |
| cache | 0 | 2 | 5 | 0 |
| arrival | 0 | 0 | 3 | 0 |
| reversed arrival | 0 | 0 | 10 | 1 |
| rung 1's own engine | 0 | 0 | 0 | 0 |
| the order on the 286 answers | 0 | 0 | 9 | 0 |
| the order on all 579 answers | 0 | 15 | 9 | 2 |
| the order on the truth at the 286 | 20 | 0 | 4 | 0 |
| tree handed the truth, all 579 | 44 | 52 | 3 | 0 |

- **The tree on the proposer's answers decides all three `ONCALL_ESCALATION`
  cases right, and no execution of the rules gets more than two.** Two of its
  leaves send severity-1 tickets to that queue: every one outside billing, and
  those in billing off hours. They hold the 7 answers that named it, all on
  `T2_TECHNICAL` tickets in truth (`results_ilp/labels.json`). They send every
  other severity-1 ticket they cover there too, and the record does not count
  what that costs beyond these four classes. The tree handed the truth gets
  none of the three: its examples hold no `ONCALL_ESCALATION` ticket, because
  none ever escalated.
- **`ACCOUNT_MANAGER` is lost to every student of the answers**, which name it
  twice, and to every execution of the rules that reads no truth. The order on
  the truth at the 286 gets 20 of 55, and the tree handed the truth 44.
- **`SECURITY_INCIDENT` is where the answers help an order**: 9 of 10 for the
  order on the answers, against arrival's 3.

### The tree written in the DSL

The tree on rung 1's 579 answers, as the frozen DSL's rules: 25 rules, one per
leaf, disjoint and covering, in [`score.json`](score.json) as
`the_tree_in_the_dsl`, each with its queue and its training counts. The broad
ones:

- `has_security_keyword eq False AND severity gte 2 AND product eq billing →
  BILLING_SPECIALIST`: 106 of the 131 answers at that leaf name that queue;
- three leaves sending security-keyword tickets to `SECURITY_INCIDENT`: in
  billing, at severities 2 and 3, and at severity 4 on the free tier;
- `severity eq 1 AND product neq billing → ONCALL_ESCALATION`, 5 of its 8
  answers, and the same queue for severity 1 in billing off hours, 2 of 2;
- severities 2 and 3 outside billing and without the keyword, in five leaves,
  four of them to `T2_TECHNICAL`;
- the rest of severity 4 split by tier, product, prior tickets, channel, off
  hours and language into `T1_GENERAL`, `T2_TECHNICAL` and
  `SELF_SERVICE_DEFLECT`, in thirteen leaves.

**It is a partition, the shape the proposer writes when it sees the base**,
learned from its answers.

### The floor

The proposer's commonest answer, answered everywhere: `T2_TECHNICAL`, right on
364 of 995 test cases and 36,720 of 134,400 points. On run 1 of `PLAN_REUSE.md`
the commonest answer is `SECURITY_INCIDENT`: 10 test cases and 50,400 points.
On rung 1's 579 answers every student is above the floor on both surfaces. On
its train half the cache falls below it over the space, 30,962.

---

## What this does not settle

- **Three students, and we wrote them.** `T-g2` makes a loss readable: the tree
  recovers the policy when it is there, the cache is the frozen file's, and the
  regression reaches its optimum. A stronger learner, boosted trees for
  instance, would need a dependency pinned apart, and might do better.
- **What the `ONCALL_ESCALATION` leaves cost.** The record counts four rare
  classes and the totals. How many severity-1 tickets the two leaves send there
  that are `T2_TECHNICAL` or `T3_ENGINEERING` in truth is not split out.
  **[NOTE 2026-10-18] Read POST-RUN**: 40 of their 45 test cases, and they cost
  the tree 17 cases against arrival. *Three readings after the verdicts*,
  below.
- **Why the train-half tree beats the all-answers tree.** The reach explains
  the direction: on the 347 cases the all-answers tree holds the proposer's own
  answer, and the proposer was right on fewer than half of them. The record
  does not split the train-half tree's cases the same way, so it does not
  measure how much of the 30 cases that is. **[NOTE 2026-10-18] Read
  POST-RUN**: 18 of the 30, below.
- **What the `PLAN_REUSE.md` trees are.** The record holds their sizes and
  scores, not their rules. Runs 2 and 3 give trees that score alike on both
  surfaces; whether they are the same partition is not recorded. **[NOTE
  2026-10-18] Read POST-RUN**: three of them are one rule of thumb of three
  lines, and all six split on the keyword first, below.
- **Deferral, cost and the loop.** The students are offline and trained on the
  loop's escalations. A cascade would have escalated other tickets, and their
  answers do not exist (§2.5 and §12 of the plan).
- **One corpus, one policy, one proposer.** The answers come from one model, in
  two loops under prompts that differ.

---

## Three readings after the verdicts — POST-RUN

> **PROVENANCE: POST-RUN.** Asked for on 2026-10-18, after the stage. The
> expectation was written in `students/readings.py`'s docstring and committed
> before the first run. Not a signed row, not on `STATUS.md`'s scoreboard, not a
> calibration event.

`PYTHONHASHSEED=0 python3 -m students.readings`, once, on 2026-10-18, from a clean
tree at the commit that wrote its expectation: `42ba325` on `main`, merged from
`7575986` in pull request #138. Its code digest is `329454f4fbfef552`. 28 s,
zero API calls. The record is
[`readings.json`](readings.json). It refits the stage's students with the
stage's own `read_students`, and three gates passed before anything was read:

- every refitted student scores on both surfaces what `score.json` says, and
  the tree on rung 1's answers writes its 25 rules again, rule for rule;
- arrival order and its reverse are the record's, on both surfaces;
- the two `ONCALL_ESCALATION` leaves cover, over the space, exactly the points
  by true queue that the docstring derived from the hidden policy before the
  run. `tests/test_students_readings.py` recomputes that derivation by brute
  force.

**All ten clauses of the expectation held.**

### What the `ONCALL_ESCALATION` leaves cost

The two leaves are `L015`, *severity 1 outside billing*, and `L024`, *severity
1 in billing, off hours, without the keyword*.

| | cases or points | true queues | tree | arrival | reversed |
|---|---|---|---|---|---|
| test split 0, `L015` | 41 | `T2_TECHNICAL` 22, `T3_ENGINEERING` 14, `ONCALL_ESCALATION` 3, `SECURITY_INCIDENT` 2 | 3 | 20 | 21 |
| test split 0, `L024` | 4 | `T2_TECHNICAL` 4 | 0 | 0 | 0 |
| space, `L015` | 26,880 | `SECURITY_INCIDENT` 13,440, `T2_TECHNICAL` 5,040, `ONCALL_ESCALATION` 5,040, `T3_ENGINEERING` 3,360 | 5,040 | 11,340 | 18,060 |
| space, `L024` | 1,680 | `T2_TECHNICAL` 840, `ONCALL_ESCALATION` 840 | 840 | 0 | 0 |

- **On the test split the leaves cost the tree 17 cases against arrival
  order**: arrival is right on 20 of their 45 cases and the tree on 3. That is
  a third of the tree's 49-case gap. 40 of the 45 are `T2_TECHNICAL` or
  `T3_ENGINEERING` in truth.
- **Over the space they cost it 5,460 points against arrival and 12,180
  against its reverse.** The tree is right on 5,880 of their 28,560 points:
  every `ONCALL_ESCALATION` point among them, which is 5,880 of the space's
  6,300. The other 420 fall in `L025`.
- **On `L024`'s points no execution of the rules is right at all**, on the test
  split or over the space: severity 1 in billing, off hours, half of it
  `ONCALL_ESCALATION` and half `T2_TECHNICAL`.

So the tree buys the queue the rules never reach with the severity-1 tickets of
the other queues. **On both surfaces the trade is a loss**, and where tickets
arrive it is a third of the tree's gap.

### The train half on the reach's partition

| on the test split | the 347 | the 648 | all 995 |
|---|---|---|---|
| tree, train half | 164 | 336 | 500 |
| tree, all answers | 146 | 324 | 470 |
| logistic, train half | 145 | 313 | 458 |
| logistic, all answers | 146 | 320 | 466 |
| cache, train half | 137 | 258 | 395 |
| cache, all answers | 154 | 280 | 434 |
| arrival | 173 | 346 | 519 |

- **Of the train-half tree's 30-case lead over the all-answers tree, 18 cases
  are on the 347 and 12 on the 648.** The reach is most of it. The rest goes
  with the train-half tree's being coarser: 8 leaves against 25.
- **For the cache, the answers it holds are worth 17 cases on the 347.** There
  the proposer's own answer for the ticket beats the nearest train-half
  ticket's. The logistic regression hardly moves on the 347.
- **Arrival order is ahead of every student on both parts**, the train-half
  tree included: by 9 cases on the 347 and by 10 on the 648.

### What the `PLAN_REUSE.md` trees are

| set | leaves | its rules, every condition after the first read without the keyword |
|---|---|---|
| run 1, all | 6 | the keyword → `SECURITY_INCIDENT`; severities 1 to 3 → `T2_TECHNICAL`; severity 4: free → `SELF_SERVICE_DEFLECT`, otherwise billing → `BILLING_SPECIALIST`, otherwise enterprise → `T1_GENERAL` and pro and business → `T2_TECHNICAL` |
| run 1, train half | 2 | the keyword → `SECURITY_INCIDENT`; the rest → `T2_TECHNICAL` |
| run 2, all | 3 | the keyword → `SECURITY_INCIDENT`; billing → `BILLING_SPECIALIST`; the rest → `T2_TECHNICAL` |
| run 2, train half | 4 | the keyword → `SECURITY_INCIDENT`; enterprise → `T1_GENERAL`; billing → `BILLING_SPECIALIST`; the rest → `T2_TECHNICAL` |
| run 3, all | 3 | as run 2, all |
| run 3, train half | 3 | as run 2, all |

- **The trees on all of run 2's answers, all of run 3's and the train half of
  run 3's decide every point of the space alike.** They are one rule of thumb
  of three lines.
- **All six split on the security keyword first and send it to
  `SECURITY_INCIDENT`.** That is the rule of thumb `FINDINGS_EDGES.md` found
  behind nearly every edge the proposer declared on that loop.
- **On the test split the three-line rule beats run 2's base and loses to run
  3's; over the space it beats both** (the run-by-run table of `T-e` and the
  bases' table above).

### The expectation, clause by clause

| clause | reading | |
|---|---|---|
| A1 · the leaves decide 30 to 50 test cases | 45 | holds |
| A2 · two thirds of them `T2_TECHNICAL` or `T3_ENGINEERING` | 40 of 45 | holds |
| A3 · arrival at least 10 ahead on them | 20 against 3 | holds |
| A4 · arrival ahead on their points over the space | 11,340 against 5,880 | holds |
| B1 · the train-half tree ahead on the 347 | 164 against 146 | holds |
| B2 · more than half of its lead on the 347 | 164, above 161 | holds |
| B3 · the train-half cache behind on the 347 | 137 against 154 | holds |
| C1 · three trees decide alike | yes | holds |
| C2 · the keyword, billing, the rest | yes | holds |
| C3 · run 1 sends the keyword to `SECURITY_INCIDENT` | every point | holds |

The drafter trusted A4 least, and it held.

---

## Files

```
students/plan.py         the gate and the constants of §3 and §10
students/material.py     the answers by set, their reach, the truth's route
students/tree.py         growth, cost-complexity pruning, the folds, the DSL rules
students/logistic.py     the softmax, L-BFGS, the folds
students/cache.py        the retrieval, its online protocol, its masks
students/rules.py        arrival order, rung 1's engine, the order on new labels, the bases
students/gates.py        T-g1 to T-g4, blocking, run first
students/score.py        the stage: T-a to T-e, the readings of T-f
students/readings.py     POST-RUN: the three readings the stage left open
results_students/score.json      the stage's figures, the tree in the DSL, the gates
results_students/readings.json   the readings' figures, behind three gates, and the expectation
tests/test_students.py           how the package counts — and no figure
tests/test_students_readings.py  how readings.py counts, and the derivation by brute force
```

Reproducible, in this order:

```
python3 -m students.score --dry-run           # T-g1..T-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m students.score    # about five and a half minutes
PYTHONHASHSEED=0 python3 -m students.readings # POST-RUN; under half a minute
```
