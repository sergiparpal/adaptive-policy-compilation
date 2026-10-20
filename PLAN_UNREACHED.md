# PLAN_UNREACHED — what the rules no label reaches hold, and what deferring them buys

> **[CLOSED 2026-10-20] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-10-20, before any figure of the plan existed. The five rows were
> adjudicated the same day: **`Z-c` and `Z-e` hold; `Z-a`, `Z-b` and `Z-d` are
> refuted**, `Z-d` and `Z-e` thinly, and `Z-f` is reported. Where tickets
> arrive, `R0545` was the only rule no escalation reaches whose move pays, and
> none of the 25 decides a test case in the escalations' order. Over the
> function one rule holds the stake, *keyword and severity 1* to
> `SECURITY_INCIDENT`, and deferring the 25 gains no more than a reshuffle of
> them. **The figures are owned by
> [`results_unreached/FINDINGS_UNREACHED.md`](results_unreached/FINDINGS_UNREACHED.md)**,
> and no result is to be read off this file; the scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-10-20. The line is kept
> unedited and this banner is its correction. The banner touches neither §0 nor
> its note, adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-10-20, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §9 says why the gate binds anyway.

**This plan exists because one rule decided a class, and no label reached it.**
Read POST-RUN after `PLAN_SPOTCHECK.md`'s stage, `T3_ENGINEERING` turns on one
rule of rung 1's base: `R0545`, *severity 1 on the api product*
([`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md),
*Which tickets teach `T3_ENGINEERING`*). No escalation matches it, so the order
labelled with the escalations' truth left it where its start put it: 560 of the
577 rules sit above it there, and the order is right on none of the test split's
57 `T3_ENGINEERING` cases. Moved to the front, it makes every order of that
stage learn the class, costs nothing on the test split, and gains 12 or 13 test
cases in each order that had not learnt it. [`IDEAS.md`](IDEAS.md) carries the
question in *What `PLAN_SPOTCHECK.md` opens*: **how many other rules no label
reaches there are in rung 1's base, and what moving each would buy on either
surface.**

**Why the search cannot place them.** Rung 3's search orders the 577 rules to
decide right as many labelled cases as it can, first match wins. A rule no
labelled case matches never decides one, so its place never changes the
objective. The local search applies no move on a tie, so such a rule is never
moved for itself: it stays where the start put it, and moves only when a swap of
another rule carries it. The start is the record's greedy, which puts every such
rule at the tail in arrival order, or one of 64 shuffles. **Both endpoints this
plan reads came from a shuffle**: the escalations' order from `aleatorio 57` and
the whole train half's from `aleatorio 13`
([`results_escalations/score.json`](results_escalations/score.json),
[`results_spotcheck/score.json`](results_spotcheck/score.json)). In both, the
rules no label reaches sit where a random permutation put them.

**What the material says before any figure** (§1, counted without the truth or
any order):

- **The escalations leave 25 rules unreached, 22 distinct.** Four of them are
  one rule written four times, *severity 1 off hours* to `ONCALL_ESCALATION`.
  `R0545` is one of the 25.
- **The whole train half leaves 5**, all among the 25.
- **Every one of the 25 was written at a test-split ticket, and matches it.**
  Every rule of the base matches the case it was written at, and the 286 written
  in the train half were all written at an escalation, so the escalations reach
  them all. What no escalation reaches can only have been written in the test
  split.

**What it would change.**

- **If the rules no escalation reaches hold half the gap** between the
  escalations' order and the whole train half's, what the escalations leave is
  mostly a matter of which rules a label reaches, not of how many labels there
  are. A reviewer who labelled one ticket per unreached rule would buy it; that
  selection is not run here.
- **If deferring them raises the escalations' order**, a convention that reads no
  truth recovers part of what the start's placement costs. Then every
  label-budget figure the thread cites understates what its labels buy.
- **If neither**, `R0545` was singular and the rest of the unreached are a
  lottery that costs little either way.
- **Over the space** the same questions are asked of the function. There the
  test split's birth tickets weigh nothing, and the broad unreached rules match a
  great deal.

**None of this plan's figures exists**, except what the gate reproduces:
- the two endpoints, published by the optimizer audit and `PLAN_ESCALATIONS.md`;
- `R0545`'s move to the front of the escalations' order on the test split,
  published by the reading above.

Under [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable,
although it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic, its denominator and its surface here, before
any figure.**

- **The escalations** are the 316 cases of rung 1's record that escalated and
  fall in the train half of rung 3's split 0, as `PLAN_ESCALATIONS.md` defined
  them. **The whole train half** is that half's 1,005 cases.
- **A labelled order** is rung 3's search over the 577 rules, `puro` pool, its
  declared constants, labelled with the **truth** of a set of cases and nothing
  else. It is the optimizer audit's label-budget instrument, called through
  `escalations/instrument.py` and not copied (§3).
- **The escalations' order** is right on **814** of 995 test cases and **73,020**
  of 134,400 points. **The whole train half's** is right on **843** and
  **81,089**.
- **Reach.** A rule is *reached* by a labelled set when it matches one of the
  set's cases in the `puro` pool, and *unreached* otherwise. The escalations
  leave **25** rules unreached, **22 distinct**. **The key rule** is `R0545`,
  one of them, whose move on the test split is published. **The others** are
  the 21 distinct rules besides it.
- **Copies**: rules written the same, conditions and queue, make the same move
  and are counted once, under the earliest-born.
- **A front move** is one rule moved alone to the front of an order, every other
  rule as it was. Its **gain** is the moved order's count right less the order's
  own, on one surface. **On the test split a gain is read away from the rule's
  birth ticket**: the test cases whose ticket is the one the rule was written at
  are left out (§2.3).
- **The back move** puts every unreached rule below every reached one, each
  group in the order's own order. It reads no truth.
- **The coin** is 100 seeded placements of the same unreached rules at random
  places among the reached ones, which keep their order (§3).
- **The gap**:
  - on the test split it is 843 − 814 = **29** cases, and half of it, rounded
    up, is **15**;
  - over the space it is 81,089 − 73,020 = **8,069** points, and half of it is
    **4,035**.
- **Corpus test split 0** is 995 cases; **the space** is the 134,400
  combinations. Every count is of decisions right against the truth.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **Z-a** | **Besides `R0545`, another rule no escalation reaches pays where tickets arrive.** | corpus test split 0: of the 21 other distinct rules no escalation reaches, the number whose front move in the escalations' order gains away from its birth ticket | **≥ 1** | **0** |
| **Z-b** | **Together they hold half the gap to the whole train half.** | corpus test split 0: the same 21, what each front move gains away from its birth ticket, a loss counted as zero, summed | **≥ 15** | **< 15** |
| **Z-c** | **Over the function, the rules no escalation reaches hold half that gap.** | exhaustive space, 134,400 points: the 22 distinct rules, `R0545` included, what each front move gains, a loss counted as zero, summed | **≥ 4,035** | **< 4,035** |
| **Z-d** | **Deferring them buys something where tickets arrive, without the truth.** | corpus test split 0, 995 cases: the escalations' order after the back move, its count right | **> 814** | **≤ 814** |
| **Z-e** | **Deferring them buys something over the function.** | exhaustive space, 134,400 points: the same order, its count right | **> 73,020** | **≤ 73,020** |
| **Z-f** | *Reported, not adjudicated.* **What reading the rows needs.** | §8's readings: every unreached rule of both endpoints, its place, what it decides and its front move on both surfaces, split at its birth ticket; `R0545` over the space; the back move and the coin for both endpoints on both surfaces; the curve of the optimizer audit's random arrivals; the rare classes | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-20)**

**One label, and it does not change a verdict.** `Z-d` and `Z-e` read one order
after one move, and the order's own placement of the unreached rules is one draw.
**`Z-d` and `Z-e` are labelled *thin* when their statistic lies inside the range
of the coin's 100 placements** on the same surface: then the back move does
nothing a reshuffle of the same rules does not. `Z-a` to `Z-c` carry no label.
Each is one deterministic reading of one order, and §6.2 says what that leaves.

**What a hold says and what a refutation says.**

- **`Z-a` holding** says `R0545` is not alone: another rule the escalations never
  reach pays on tickets other than its own. Refuted, on the arrivals it is the
  only rule no escalation reaches whose move pays away from the ticket it was
  written at.
- **`Z-b`** asks how much. Holding, the others hold half of what the 689 labels
  beyond the escalations buy, and what the escalations leave is mostly reach.
  Refuted, `R0545` aside, what they leave is not in the rules they leave
  unreached.
- **`Z-c`** asks the same over the function. `IDEAS.md`'s standing note says
  arguments that a quantity carries across surfaces lose, and this row argues
  nothing across them: its line is the space's own gap.
- **`Z-d` and `Z-e`** ask whether a convention that reads no truth, *what no
  label vouches for goes last*, is worth anything against the start's placement.
  Holding, it is, on that surface. Refuted, the start's placement costs nothing
  there, or deferring costs more than it saves.

**Why the lines are where they are.** `Z-a` sits at one rule: the question is
whether there are others. `Z-b` and `Z-c` sit at half the gap on each surface,
as `N-b` and `N-e` did. `Z-d` and `Z-e` sit at the order's own figures, so they
ask whether the move buys anything. None is at the drafter's expectation. Ties go
against the claim in every row.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **The documents.** `CLAUDE.md`, `STATUS.md`, `IDEAS.md` whole, `README.md`'s
  sections on the writers, the tests and the `_env` block, `PLAN_SPOTCHECK.md`
  whole, `FINDINGS_SPOTCHECK.md` from *What this does not settle* to its end,
  `EXTERNAL_REVIEW.md` §5, and the three analytical documents `CLAUDE.md` asks
  to be read first, in the same session.
- **The records' published figures**, read for this plan:
  - `results_escalations/score.json`: the escalations' order, 814 and 73,020 and
    its rare classes, and the start each of its 29 orders came from;
  - `results_spotcheck/score.json`: both endpoints, among them the whole train
    half's 843 and 81,089, and the start each of its 40 orders came from;
  - `results3/budget_and_balance_ls.json`: split 0's rows at every budget, with
    the start each came from, and its per-class count on split 0;
  - `results_spotcheck/readings.json`: its fields and how many orders it keeps,
    and **not its orders**.
- **What `FINDINGS_SPOTCHECK.md` published about `R0545`**: its text, its birth
  at arrival 1,939 in the test split, its 13 test cases, all
  `T3_ENGINEERING`, and its seven train tickets; 560 rules above it in the
  escalations' order; and its move to the front gaining 12 or 13 test cases in
  each order that had not learnt the class, the escalations' order among them.
- **Facts about the material, counted by the drafter** (§1), from matching, the
  halves, rung 1's escalated flag, birth indices, queues, ticket keys and
  extensions:
  - where every rule was written, and that each matches its birth case;
  - which rules the escalations, the whole train half and each draw of the
    curve leave unreached, with their queues, conditions and copies;
  - how many test cases and space points each matches, and how many of its test
    cases are its birth ticket.

  None reads the truth, and none reads an order.
- **The code**: `escalations/`, `spotcheck/`, `rung3/budget_and_balance_ls.py`,
  `budget_and_balance.py`, `local_search.py`, `order_search.py` and
  `order_search_ls.py`, and `reuse/plan.py` for the form of a free plan's gate.
- **The blocking checks' output** (§7), which prints pass or fail and figures
  already published.
- **Not seen, because nobody has computed them**:
  - where any unreached rule sits in any order but `R0545` in the escalations';
  - which test cases or points any of them decides there;
  - whether any of them is right on any case or point;
  - any front move but `R0545`'s on the test split;
  - any back move and any coin;
  - `R0545` over the space.

  The hidden policy's rules were not read for this draft.

**What the drafter expects, written down so the scoreboard can score it.**
**`Z-a` and `Z-c` hold; `Z-b`, `Z-d` and `Z-e` are refuted.** The drafter trusts
`Z-c` least, then `Z-d`.

- **`Z-a` holds, about four in five.** The escalations' order is right on none
  of the 57 `T3_ENGINEERING` cases and on 4 of the 10 `SECURITY_INCIDENT` ones.
  The others include two `T3_ENGINEERING` rules and a `SECURITY_INCIDENT` one,
  with four test cases away from their birth tickets between them.
- **`Z-b` refuted, about nine in ten.** Away from their birth tickets the 21
  match 71 test cases, 18 of them the `ONCALL_ESCALATION` rule's, for a queue
  with 3 test cases. The order is right on four test cases in five.
- **`Z-c` holds, about three in five.** *Keyword and severity 1* to
  `SECURITY_INCIDENT` and *severity 1 off hours* to `ONCALL_ESCALATION` each
  match 16,800 points. `SECURITY_INCIDENT` is the truth on 50,400 points of the
  space, three quarters of the half that carries the keyword (`FINDINGS3.md`
  §17). The order gets 6 of the test split's 10 wrong, so it may decide the
  keyword's points otherwise.
- **`Z-d` refuted, about one in two.** `R0545` decides none of its 13 test cases
  in that order. Where the other 24 sit is the shuffle's. A test case is matched
  by dozens of rules, so they may decide nothing, and a tie refutes.
- **`Z-e` refuted, about three in five.** If the broad unreached rules are right
  over the function, as `Z-c` bets, deferring them costs points there.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 39
of 94 adjudicated rows came out refuted. Here the drafter expects three of five
refuted, because the lines sit where the question puts them and not where the
drafter expects the figures.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls. No loop runs; rung 3's search is re-run
on sets of labels whose orders are already published, and their rules are
moved.

**Already paid for, and read as they stand:**

- `results/llm_run.json`: rung 1's 2,000 records, which say which cases
  escalated, and its 577 rules, through `rung3.order_search.load`.
- `results_escalations/score.json`: the escalations' order, which `Z-g1`
  reproduces.
- `results_spotcheck/score.json`: the whole train half's order, which `Z-g1`
  reproduces.
- `results_spotcheck/readings.json`: both endpoints' orders as that reading kept
  them, and `R0545`'s move to the front of the escalations' order; `Z-g1`
  checks both against the instrument.
- `results3/budget_and_balance_ls.json`: the random arrivals' twenty draws on
  split 0 and the whole train half's per-class count; `Z-g1` reproduces every
  draw.
- `results3/floor_by_pool.json`: arrival order.

**The material, as the drafter counted it and `Z-g1` recomputes it.**

- **Births.** 291 of the 577 rules were written at a test-split ticket and 286
  at a train-half one. **Every rule matches the case it was written at.** All
  286 of the train half's were written at an escalation, so the escalations
  reach every one of them.
- **The escalations leave 25 rules unreached**, all written in the test split:
  `T2_TECHNICAL` 10, `T1_GENERAL` 5, `ONCALL_ESCALATION` 4, `T3_ENGINEERING` 3,
  `SELF_SERVICE_DEFLECT` 2, `SECURITY_INCIDENT` 1.
  - They match 162 test cases between them, 26 of them their birth tickets, on
    90 distinct test cases. **No test case is matched by unreached rules
    alone.**
  - Over the space they match 132,728 points, counted rule by rule.
- **The whole train half leaves 5**, all among the 25: `R0087`, `R0117`,
  `R0267`, `R0351` and `R0361`. They match 10 test cases, 5 of them their birth
  tickets, and 5,882 points.
- **Copies.** `R0287`, `R0373`, `R0493` and `R0506` are one rule, *severity 1
  off hours* to `ONCALL_ESCALATION`, so the 25 are 22 distinct rules. No other
  two are written the same.

**The 25 rules**, counted before signature. *Test* is the test cases each
matches; *birth* those of them on its birth ticket; *space* its points; *full*
whether the whole train half leaves it unreached too:

| rule | queue | written at | conditions | test | birth | space | full |
|---|---|---|---|---|---|---|---|
| `R0016` | `T2_TECHNICAL` | 35 | 3 | 10 | 1 | 10,080 | |
| `R0019` | `SECURITY_INCIDENT` | 44 | 2 | 2 | 1 | 16,800 | |
| `R0027` | `T2_TECHNICAL` | 71 | 4 | 2 | 1 | 840 | |
| `R0062` | `T1_GENERAL` | 291 | 8 | 1 | 1 | 6 | |
| `R0080` | `SELF_SERVICE_DEFLECT` | 426 | 5 | 9 | 1 | 120 | |
| `R0087` | `T1_GENERAL` | 506 | 4 | 1 | 1 | 1,050 | yes |
| `R0114` | `T2_TECHNICAL` | 757 | 4 | 5 | 1 | 2,520 | |
| `R0117` | `T1_GENERAL` | 778 | 5 | 3 | 1 | 40 | yes |
| `R0150` | `T1_GENERAL` | 937 | 6 | 3 | 1 | 160 | |
| `R0158` | `T2_TECHNICAL` | 992 | 3 | 1 | 1 | 1,680 | |
| `R0211` | `T1_GENERAL` | 1,211 | 8 | 2 | 1 | 40 | |
| `R0267` | `T3_ENGINEERING` | 1,402 | 3 | 2 | 1 | 3,520 | yes |
| `R0287` | `ONCALL_ESCALATION` | 1,439 | 2 | 19 | 1 | 16,800 | |
| `R0308` | `T2_TECHNICAL` | 1,517 | 4 | 3 | 1 | 2,520 | |
| `R0351` | `SELF_SERVICE_DEFLECT` | 1,586 | 7 | 2 | 1 | 12 | yes |
| `R0357` | `T2_TECHNICAL` | 1,602 | 6 | 6 | 1 | 640 | |
| `R0361` | `T2_TECHNICAL` | 1,608 | 5 | 2 | 1 | 1,260 | yes |
| `R0373` | `ONCALL_ESCALATION` | 1,628 | 2 | 19 | 1 | 16,800 | |
| `R0448` | `T2_TECHNICAL` | 1,778 | 3 | 9 | 1 | 6,720 | |
| `R0450` | `T2_TECHNICAL` | 1,784 | 4 | 2 | 1 | 2,400 | |
| `R0459` | `T2_TECHNICAL` | 1,795 | 2 | 5 | 1 | 6,720 | |
| `R0493` | `ONCALL_ESCALATION` | 1,863 | 2 | 19 | 1 | 16,800 | |
| `R0506` | `ONCALL_ESCALATION` | 1,884 | 2 | 19 | 2 | 16,800 | |
| `R0545` | `T3_ENGINEERING` | 1,939 | 2 | 13 | 1 | 6,720 | |
| `R0570` | `T3_ENGINEERING` | 1,980 | 3 | 3 | 1 | 1,680 | |

**The curve's reach.** The rules no label reaches in each of the optimizer
audit's draws of random arrivals on split 0:

| labels | draw 0 | draw 1 | draw 2 | draw 3 | draw 4 | winners from the greedy start |
|---|---|---|---|---|---|---|
| 10 | 247 | 357 | 264 | 327 | 305 | 5 of 5 |
| 50 | 98 | 117 | 115 | 107 | 133 | 4 of 5 |
| 100 | 59 | 52 | 71 | 64 | 64 | 4 of 5 |
| 251 | 17 | 18 | 23 | 28 | 18 | 2 of 5 |

The last column is the record's `best_from`. Where the winner came from the
greedy start, the unreached rules began at the tail.

**The truth** enters only to label, to score and to read the moves. It comes
through modules `tests/test_oracle_separation.py` already allows:
`rung3.order_search.build_tables` and `rung3.order_search_ls.space_pools`, both
reached through `escalations/instrument.py`. No module of this plan imports the
oracle.

---

## 2. The choices that have to be made at signature time

Eight, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 The rows read the escalations' order — the drafter recommends it

The escalations are the labels a deployed loop would have, and their order is
where `R0545` was found unreached. The whole train half's order is read the same
way and reported: it leaves only 5 rules unreached, with 10 test cases between
them, too few to carry a row on the arrivals.

### 2.2 Reach is read in the `puro` pool — the drafter recommends it

The instrument's masks are built on the `puro` pool, so that is the pool in
which a label reaches a rule. The hybrid pool silences rules by subsumption
before any label is read, which is another phenomenon (§11.1).

### 2.3 On the test split a front move is read away from the rule's birth ticket — the drafter recommends it

Every one of the 25 was written at a test-split ticket, by the proposer, from its
own answer. Moved to the front, a rule decides that ticket with that answer, and
that is the proposer's answer and not something a label failed to reach. So
`Z-a` and `Z-b` leave out of each move the test cases on its birth ticket, which
the material counts at 26 of 162. The record reports every move split at the
birth ticket and whole. Over the space the birth tickets are 25 points of
134,400, and `Z-c` reads every point.

### 2.4 The back move keeps the order's own order — the drafter recommends it

The reached rules keep the searched order and the unreached follow in theirs.
No test case is matched by unreached rules alone (§1), so on the test split the
unreached rules' order among themselves decides nothing. Over the space it may,
and keeping the searched order adds no criterion. The greedy start's convention,
arrival order at the tail, was considered and dropped for that reason.

### 2.5 The coin is 100 placements, seeded from 19000 — the drafter recommends it

Placement `d` uses `random.Random(19000 + d)`: a shuffle of the unreached rules,
then a sample of the slots they take. 100 bounds the range the thin label reads.
The seed follows `PLAN_ESCALATIONS.md`'s 17000 and `PLAN_SPOTCHECK.md`'s 18000.

### 2.6 The curve is reported, on the record's own draws — the drafter recommends it

The optimizer audit's twenty draws of random arrivals at 10, 50, 100 and 251
labels are searched again and read like the endpoints, without the coin. They say
how many rules no label reaches, and what moving them buys, as the labels
shrink. No row reads them, because most of their winners came from the greedy
start, where the unreached began at the tail.

### 2.7 Copies are counted once — the drafter recommends it

Four of the 25 are one rule. Their moves are the same move, and counting it four
times would make one rule's gain four rules'. The earliest-born, `R0287`, stands
for them.

### 2.8 The thread's name and letter

`PLAN_UNREACHED.md`, rows `Z-a` to `Z-f`. `A` to `F`, `H` to `W` and `Y` are
taken; `G`, `X` and `Z` are free. `Z` reads as *zero labels*. The naming is
Sergi's to overrule.

---

## 3. The orders and the moves, exactly

**The labelled sets.**

- The escalations: `escalations.selections.escalations` on split 0's train half,
  rung 1's records with `escalated` true. 316 cases.
- The whole train half: 1,005 cases.
- The curve: `escalations/instrument.py`'s `record_draw(inst, k, d)` for `k` in
  10, 50, 100 and 251 and `d` in 0 to 4, the optimizer audit's own draws.

**The orders.** For a labelled set `S`, `escalations/instrument.py`'s
`labelled_order`:

1. masks over `S` with the truth, `rung3.local_search.build_masks`, on the `puro`
   pool;
2. the record's greedy over `S`;
3. the declared multi-start from it, `rung3.budget_and_balance_ls.search`.

Its best order is read on split 0's test half and over `space_pools`' `puro`
masks by `score_order`.

**Reach**, in `unreached/moves.py`: the rules no case of `S` matches,
`matched[i]` being the `puro` pool, in the base's order.

**The moves**, in `unreached/moves.py`, each a permutation of a searched order:
- `front(order, rid)`: `rid` first, every other rule as it was;
- `back(order, unreached)`: the reached rules in the order's order, then the
  unreached in theirs;
- `coin(order, unreached, d)`: the unreached shuffled by
  `random.Random(19000 + d)`, then placed at slots sampled by the same generator
  among the reached, which keep their order.

**A front move's gain** is read two ways, which must agree or the stage writes
nothing:
- by masks, as the difference of two `score_order` counts;
- case by case, by first match over the test cases the rule matches, split
  between those on its birth ticket and the rest.

`Z-a` and `Z-b` read the second route's part away from the birth ticket. Over
the space a gain is read by masks.

**Copies**: `moves.distinct` keeps one rule per text, conditions and queue, the
earliest-born.

**The birth ticket** of a rule: the test cases whose ticket key is that of the
corpus case at its `born_at`.

---

## 4. The reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | surface | owning record |
|---|---|---|---|
| arrival order | 519 of 995 · 42,310 of 134,400 | test split 0 · space | `results3/floor_by_pool.json` |
| the whole train half, 1,005 labels | 843 · 81,089 (0.6033), from `aleatorio 13` | test split 0 · space | `results3/order_search_ls.json`, split 0, `puro`; `results_spotcheck/score.json` |
| the same, by rare class | `T3_ENGINEERING` 18 of 57, `ACCOUNT_MANAGER` 19 of 55, `SECURITY_INCIDENT` 5 of 10, `ONCALL_ESCALATION` 0 of 3 | test split 0 | `results3/budget_and_balance_ls.json`, `per_class_split0` |
| the most any order can reach | 20, 21, 10 and 3 of the same | test split 0 | the same |
| the escalations' order, 316 labels | 814 · 73,020 (0.5433), from `aleatorio 57` | test split 0 · space | `results_escalations/score.json` |
| the same, by rare class | 0, 20, 4 and 0 | test split 0 | the same |
| `R0545` at the front of the escalations' order | 12 or 13 more test cases right, as in every order that had not learnt the class | test split 0 | `results_spotcheck/readings.json` |
| random arrivals at 10, 50, 100, 251 | medians 532, 717, 791, 820 · 0.3400, 0.3993, 0.4361, 0.5302 | test split 0 · space | `results3/budget_and_balance_ls.json`, split 0 |

---

## 5. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** Nothing here touches it.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise the loop.** Nothing here runs it.
4. **Seed 17, no regeneration, and every record this plan reads is read-only.**
5. **Do not adjust a prompt or a schema.** Nothing here touches either.
6. **If the numbers come out badly, report them.**
7. **No API key is needed**, and none is loaded.

And this plan's own, lettered:

A. **The instrument is called, not copied**: `escalations/instrument.py`, and
   through it `rung3/budget_and_balance_ls`, `budget_and_balance`,
   `local_search` and `order_search`.
B. **The records are inputs, never outputs.** Nothing outside
   `results_unreached/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §9 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow.
F. **The dry run applies no move to a searched order but `R0545`'s front move
   in the escalations' order**, whose count is published, and scores no back
   move and no coin. It prints pass or fail and figures already published.
   `tests/test_unreached.py` walks `unreached/gates.py` to say so.
G. **The moves read no truth.** `unreached/moves.py` names none, in a name or a
   string literal, and `Z-g2` checks it before any record.

---

## 6. Known traps

**6.1 — The rules reach the test split by birth.** Every one of the 25 was
written at a test-split ticket and matches it. `Z-g3` checks that no *label*
reaches the test split, and that is all it can check: the base was written over
all 2,000 arrivals, as in every rung 3 figure. A front move decides a rule's
birth ticket with the proposer's own answer, which is why `Z-a` and `Z-b` read
away from it, and why the record reports both parts.

**6.2 — Each row reads one order.** The escalations' order is one draw of the
multi-start lottery, from `aleatorio 57`. Where its unreached rules sit, and so
what a front move changes, is that draw's. The coin brackets the back move's
rows; the front moves have no bracket. Another draw of the same labels would
place them elsewhere.

**6.3 — A front move is not a method.** It is read with the truth, one rule at a
time, so `Z-a` to `Z-c` measure what the unreached rules hold, not what a
system could take. Their gains do not add: two moves can gain the same case, so
the sums of `Z-b` and `Z-c` are indices of the stake and no order anyone can
build. The back move is the only move here that reads no truth.

**6.4 — The front is one place of 577.** A rule may gain more lower down, below
a rule of its own queue that shares its right cases. No other place is tried.

**6.5 — Copies multiply a move.** Four of the 25 are one rule. The rows count
distinct rules; the record lists every rule, the copies marked.

**6.6 — The space weighs what the arrivals barely touch.** Four distinct
unreached rules have two conditions, `R0019`, `R0287`, `R0459` and `R0545`. They
match 6,720 to 16,800 points each, against 2 to 19 test cases. A row over the
space can turn on one of them.

**6.7 — `R0545` is named because the reading after `PLAN_SPOTCHECK.md` found
it.** Its move on the test split is published, so `Z-a` and `Z-b` leave it out.
Over the space nothing about it has been read, and `Z-c` keeps it.

**6.8 — Small budgets start from the greedy.** Where the winner came from the
greedy start, the unreached rules began at the tail, in arrival order, and the
back move changes little but what swaps carried. That is most of the curve below
251 labels, and why it is reported only.

**6.9 — The `puro` pool only.** The hybrid pool's subsumption silences rules
before any label is read: 181 of the 577 match nothing on the train half there
(`results3/FINDINGS_AUDIT.md`, Step 1). That is another machine.

---

## 7. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **Z-g1 — The material and the instrument are the records'.**
  - The suite is green.
  - The material of §1 recomputes: the counts, the table of the 25, the copies,
    and the curve's reach.
  - Arrival order gives 519 and 42,310.
  - The records hold the figures §4 gives: both endpoints, their starts, and the
    whole train half's rare classes.
  - The instrument reproduces both endpoints: 814, 73,020 and 0, 20, 4 and 0 by
    rare class from `aleatorio 57`; 843, 81,089, 0.8472, 0.6033 and 18, 19, 5
    and 0 from `aleatorio 13`.
  - Both orders are the ones `results_spotcheck/readings.json` kept.
  - `R0545` at the front of the escalations' order gives the count that record
    published.
  - Each of the optimizer audit's twenty draws gives the record's test and
    space shares, to four decimals, and its start.
- **Z-g2 — The moves read no truth.**
  - `unreached/moves.py` names no truth, in a name or in a string literal.
  - On a toy order built by hand, the front move, the back move and the coin
    are the permutations §3 defines.
  - The coin is seeded, and its placements keep the reached rules' order.
  - Reach is read off matching, and copies are rules written the same.
- **Z-g3 — No label reaches the test split.** Every labelled case of every
  order read is in the train half, and no test case shares a ticket with one.
- **Z-g4 — The signature**, §9.

> **[NOTE 2026-10-20] Run before signature, as for every free plan since
> `PLAN_PRIMACY.md`: the plan, its package and its blocking checks.** The first
> three pass. `PYTHONHASHSEED=0 python3 -m unreached.score --dry-run`, zero API
> calls, nothing written, 596 s, 212 of them the suite. Without the dry run,
> `python3 -m unreached.score` exits at the gate and creates no directory.
>
> - **`Z-g1`.** The suite is green, 1,930 tests, and green on 3.10 too.
>   - §1's material recomputes: the counts, the table of the 25, the copies and
>     the curve's reach.
>   - Arrival order gives 519 and 42,310.
>   - The records hold §4's endpoints and their starts.
>   - The instrument reproduces them: 814, 73,020 and 0, 20, 4 and 0 by rare
>     class from `aleatorio 57`; 843, 81,089, 0.8472, 0.6033 and 18, 19, 5 and 0
>     from `aleatorio 13`. Both orders are the ones
>     `results_spotcheck/readings.json` kept.
>   - `R0545` at the front of the escalations' order gives the count that
>     record published.
>   - Each of the optimizer audit's twenty draws gives the record's test and
>     space shares, to four decimals, and its start.
> - **`Z-g2`.** `moves.py` names no truth in a name or a string. On the toy
>   order the three moves are §3's permutations, the coin is seeded and keeps
>   the reached rules' order, reach is read off matching, and copies are rules
>   written the same.
> - **`Z-g3`.** Every labelled case is in the train half, and no test case
>   shares a ticket with one.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 8. The stage — scoring (free)

**Deliverable.** `unreached/score.py` → `results_unreached/score.json`, and
`results_unreached/FINDINGS_UNREACHED.md`, which owns every figure.

**What it does.** `Z-g1` to `Z-g4`, in that order and all blocking. Then, for
each endpoint:
- its unreached rules;
- for every one of them, its place in the order, the test cases it matches and
  decides there, and its front move on both surfaces, split at its birth ticket
  on the test split;
- the back move, and the coin's 100 placements, on both surfaces;
- the rare classes, for the order and after the back move.

Then the curve's twenty orders, read the same way without the coin. Then `Z-a` to
`Z-e`, each with its label. **It refuses to write if the two routes of a front
move ever disagree.**

**Z-f, reported:**

- **Every unreached rule of both endpoints**: its queue, birth, place, what it
  decides, and its front move whole, on its birth ticket, away from it and over
  the space. The copies are marked.
- **`R0545` over the space**, and on the test split as published.
- **The back move and the coin** for both endpoints on both surfaces, with where
  the order and the back move fall among the coin's placements.
- **The curve**: for each draw, its start, how many rules no label reaches, the
  back move on both surfaces, and the stake of the front moves.
- **The rare classes** of each endpoint, before and after the back move.

---

## 9. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money**
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §8): it is the order of events,
that §0 was signed before any figure that could inform it existed. The gate
reads `PLAN_UNREACHED.md` and no other plan, and counts signatures rather than
stopping at the first. Every line starting `**Signed by Sergi:` must be filled
in, and there must be at least one. The counting is `reuse/plan.py`'s, called
with this plan's path. No flag skips the gate; `--dry-run` runs `Z-g1` to `Z-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The records of §1. `SPLIT = 0`, `SPLIT_SEED = 17`,
  `N_SPACE = 134400`, `N_TEST = 995`.
- **The orders and the rule.** The two endpoints; `KEY_RULE = "R0545"`;
  `BUDGETS = (10, 50, 100, 251)` and `DRAWS = 5`, the record's.
- **The coin.** `COIN_DRAWS = 100`, `COIN_SEED = 19000`.
- **The material.** §1's counts, its table of the 25, the copies and the curve's
  reach.
- **The instrument.** Rung 3's declared constants, imported.
- **The lines of §0.** `1`, `15`, `4,035`, `814` and `73,020`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
unreached/__init__.py
unreached/plan.py         the gate and the constants of this section
unreached/moves.py        reach, the front move, the back move, the coin, copies; no truth
unreached/gates.py        Z-g1 to Z-g4
unreached/score.py        the stage: Z-a to Z-e, the readings of Z-f
tests/test_unreached.py
results_unreached/score.json
results_unreached/FINDINGS_UNREACHED.md
```

**The plumbing, in the same commit as the modules**: `unreached` joins
`CODE_ROOTS` in `harness/provenance.py` and the roots the oracle scan walks in
`tests/test_oracle_separation.py`; the README's table of writers gains
`unreached/score.py`'s row, and its list of dry runs gains the command. **The
list of modules allowed to see the oracle does not grow.**

---

## 10. Definition of done

- [ ] `results_unreached/score.json` with `_env`, produced with
      `PYTHONHASHSEED=0` from a clean tree.
- [ ] `Z-g1` to `Z-g4` passed before any record was written.
- [ ] The plumbing of §9, and tests pinning its constants; the whole suite green
      on 3.10 and 3.12.
- [ ] Every figure in prose names its surface.
- [ ] `results_unreached/FINDINGS_UNREACHED.md` owns every figure.
- [ ] `STATUS.md`: the scoreboard gains the `Z` thread, five adjudicated rows
      and one reported. `IDEAS.md`: the item answered as far as the rows go.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 11. What this plan cannot settle, declared before it runs

1. **The hybrid pool.** Subsumption silences rules there before any label is
   read. Whether those rules are redundant or buried exceptions is `IDEAS.md`'s
   item on rung 3, and another plan's.
2. **Where else a rule would pay.** Only the front is tried, one rule at a time.
   The best place for each, and the best placement of all together, is a search
   with the truth, and not run.
3. **A selection that reaches rules.** Labelling one ticket per unreached rule,
   or the tickets that reach the most of them, is what a hold of `Z-b` would
   recommend. It is a rule for which cases to label, and needs its own plan.
4. **Rules written in the train half.** Every rule no escalation reaches was
   written in the test split, by construction, so how such rules behave when
   written elsewhere cannot be read here.
5. **Other splits, other bases and the online loop.** Every row is read on split
   0's two endpoints, over rung 1's base, with the order searched once on the
   final base.
