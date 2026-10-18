# PLAN_ESCALATIONS — what a reviewer's labels at the escalations buy the order

**Status: drafted by Claude on 2026-10-18, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §9 says why the gate binds anyway.

**This plan exists because one figure of `PLAN_STUDENTS.md` opened a question
nothing in the repository answers.** Rung 3's search orders the 577 rules from
labelled cases. Handed the true queue of the 286 train-half escalations whose
proposal named a queue, it reaches 814 of the 995 cases of corpus test split 0.
That is 91% of what the same search gains over arrival order with the truth of
all 1,005 train cases. Handed the proposer's answers at the same tickets, it
falls below arrival
([`results_students/FINDINGS_STUDENTS.md`](results_students/FINDINGS_STUDENTS.md)).
So the order is in the truth of the labels, and a deployment could buy that
truth: a reviewer who labels each ticket the system escalates.
[`IDEAS.md`](IDEAS.md) carries the question in *What `PLAN_STUDENTS.md` opens*:
**how few such labels buy how much, and which escalations to label first.**

**A curve already exists for labels drawn at random.** Rung 3's audit searched
the same order from the truth of 10, 50, 100 and 251 train cases drawn at random,
five draws each, on each of five splits
([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 3). **This plan
draws the same budgets from the escalations instead**, on split 0, with the same
instrument, and sets each against that record's own draws. The escalations are
not a sample of the arrivals: they are where the loop asked. On rung 1 nearly
all of them are CONFLICTs, and none is `SECURITY_INCIDENT` in truth. Whether that
makes a label worth more or less than one drawn at random is the question.

**What it would change.**

- **If a few dozen labels at the escalations buy most of the order**, a deployed
  system needs a reviewer for a small share of what it escalates.
- **If an escalation is worth less than a random arrival**, the system's own
  escalations are the wrong place to buy labels: a reviewer should audit a
  random sample of decisions instead, which is not what an impasse loop asks.
- **Which escalations to label first** is answered for three rules that read no
  truth: in the order they come, at random, and the most crowded first.

**None of this plan's figures exists**, except the one `PLAN_STUDENTS.md`
published, which `J-g1` reproduces. Under
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable, although
it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic, its denominator and its surface here, before
any figure.**

- **The escalations** are the 316 cases of rung 1's record that escalated and
  fall in the train half of rung 3's split 0: every escalation, whatever its
  proposal did (§2.1).
- **A labelled order** is rung 3's search over the 577 rules, `puro` pool, its
  declared constants, labelled with the **truth** of a set of cases and nothing
  else. It is the label-budget instrument of the audit's Step 3, called and not
  copied (§3).
- **Random arrivals at `k`** are that record's own five draws of `k` train cases
  on split 0, read as they are: their median is **532, 717, 791 and 820** of 995
  at 10, 50, 100 and 251 labels, and **0.3993** of the space at 50
  ([`results3/budget_and_balance_ls.json`](results3/budget_and_balance_ls.json)).
- **Random escalations at `k`** are five seeded draws of `k` of the 316, and
  their statistic is the median of the five orders.
- **The gain** is what the search adds to arrival order with the truth of all
  1,005 train cases on split 0: from **519** to **843** of 995, 324 cases.
- **Corpus test split 0** is 995 cases; **the space** is the 134,400
  combinations. Every count is of decisions right against the truth.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **J-a** | **Fifty labels at the escalations buy half the gain, where tickets arrive.** | corpus test split 0, 995 cases: random escalations at 50, the median of five orders | **≥ 681** | **< 681** |
| **J-b** | **At fifty labels, an escalation is worth more than a random arrival.** | the same statistic, against random arrivals at 50, 717 | **> 717** | **≤ 717** |
| **J-c** | **At 251 labels, it is worth less.** | corpus test split 0: random escalations at 251, against random arrivals at 251, 820 | **< 820** | **≥ 820** |
| **J-d** | **Labelling the most crowded escalations first beats labelling them at random.** | corpus test split 0: the order labelled at the 50 escalations the most rules match, against `J-a`'s median | **above it** | **at or below it** |
| **J-e** | **Over the function, the escalations buy less than random arrivals.** | exhaustive space: random escalations at 50, the median share at four decimals, against random arrivals' 0.3993 | **< 0.3993** | **≥ 0.3993** |
| **J-f** | *Reported, not adjudicated.* **What reading the rows needs.** | §8's readings: every selection at every budget on both surfaces, with each draw; all 316; the labelled sets' make-up; the rare classes; the published curve beside | — | — |

**Signed by Sergi: ____________________ (date: __________)**

**One label, and it does not change a verdict.** A median of five draws is
noisy, and the published curve's draws spread widely: at 50 labels they run from
574 to 769 of 995. **A verdict is labelled *thin* when its line lies inside the
range of the draws it is read on**: for `J-a`, the five escalation orders; for
`J-b`, `J-c` and `J-e`, when each side's median lies inside the other side's
range; for `J-d`, when the crowded order lies inside the five random ones.

**What a hold says and what a refutation says.**

- **`J-a` holding** says a reviewer who labels fifty escalations at random buys
  at least half of what full supervision buys this order on the arrivals.
  Refuted, the escalations' labels are worth less per label than a budget
  curve read off random cases would suggest.
- **`J-b` and `J-c`** read the same comparison at two budgets. Both holding
  says the escalations are the better place to buy a few labels and the worse
  place to buy many, a crossover. `J-b` refuted with `J-c` holding says they are
  the worse place at both.
- **`J-d`** answers *which first* for one rule against random order. Arrival
  order, the rule a reviewer labelling as tickets come would follow, is
  reported beside it.
- **`J-e`** asks whether the comparison carries to the space. `IDEAS.md`'s
  standing note says arguments that a quantity carries across surfaces lose,
  and this row bets on the other side.

**Why the lines are where they are.** `J-a`'s is half the gain, 519 + 162. The
others are the comparators' own figures, so each row asks which of two sets of
labels buys more, and nothing else. Ties go against the claim in every row.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **The documents.** `STATUS.md`, `IDEAS.md`, `FINDINGS_STUDENTS.md` with its
  POST-RUN readings, `results3/FINDINGS_AUDIT.md`'s Step 3, `FINDINGS3.md` §4,
  and the three analytical documents `CLAUDE.md` asks to be read first, earlier
  in the same session.
- **The records' published figures**, read for this plan:
  - `results3/budget_and_balance_ls.json`: split 0's rows at every budget, each
    draw's test and space scores, and the record's summaries;
  - `results_students/score.json`: the order on the truth at the 286 named
    escalations, 814 and 73,420, and the other orders of its rules' side;
  - `results3/order_search_ls.json` and `results3/floor_by_pool.json`: split 0's
    searched row and arrival order.
- **Facts about the material, counted by the drafter** (§1): the escalations'
  count, outcomes, true queues and distinct tickets; how many queues and how
  many rules match each of them in the final base, against the whole train
  half; their keyword tickets; and, for the record's draws at 10 and 50 labels,
  how many keyword tickets and escalations each holds. That last showed the
  draw at 50 with the most keyword tickets, four, to be the one that scores
  0.6044 over the space. None is a score of an order labelled at escalations.
- **The code**: `rung3/budget_and_balance_ls.py`, `budget_and_balance.py`,
  `local_search.py` and `order_search.py`; `students/`; `bound/` and
  `reuse/plan.py`, for the form of a free plan's gate.
- **The blocking checks' output** (§8), which prints pass or fail and figures
  already published.
- **Not seen, because nobody has computed them**: any order labelled at a set of
  escalations other than the 286 named ones, at any budget, on either surface;
  the order labelled at all 316; anything about the crowded or the arrival
  selection.

**What the drafter expects, written down so the scoreboard can score it.**
`J-a`, `J-c`, `J-d` and `J-e` hold; **`J-b` is refuted**. The drafter trusts
`J-d` least, then `J-b`.

- **`J-a`, about seven in ten.** Random arrivals at 50 reach 717, and four of
  their five draws clear 681. A draw of 50 escalations is as contested as one of
  arrivals: in the final base, nearly every train case is matched by rules of
  two to four queues, escalation or not.
- **`J-b` refuted, about six in ten.** The escalations are no more contested
  than the train half by that measure, and their queues are skewed. 114 of the
  316 are `SELF_SERVICE_DEFLECT` in truth, against a quarter of the arrivals,
  and none is `SECURITY_INCIDENT` or `ONCALL_ESCALATION`.
- **`J-c`, about two in three.** The 286 named escalations reach 814, below the
  arrivals' 820 at fewer labels. 251 of the 316 hold less.
- **`J-d`, about even, leaning to a hold.** A ticket the most rules match is one
  where the order's choice decides the most, and those tickets crowd the
  common regions the test split is made of.
- **`J-e`, about two in three.** No escalation is `SECURITY_INCIDENT`, and their
  8 keyword tickets are all other queues, so their labels never teach the
  keyword rule first. 10 of the train half's 37 keyword tickets are
  `SECURITY_INCIDENT`, and half the space carries the keyword.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 35
of 84 adjudicated rows came out refuted. **These bands are more likely too
comfortable than too strict**, and the signature can tighten them.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls. No loop runs; rung 3's search is re-run
on new sets of labels.

**Already paid for, and read as they stand:**

- `results/llm_run.json`: rung 1's 2,000 records, which say which cases
  escalated, and its 577 rules, through `rung3.order_search.load`.
- `results3/budget_and_balance_ls.json`: the random arrivals' draws, split 0's
  rows read as published; `J-g1` reproduces ten of them.
- `results_students/score.json`: the order on the truth at the 286 named
  escalations, which `J-g1` reproduces.
- `results3/order_search_ls.json` and `results3/floor_by_pool.json`: the full
  search on split 0 and arrival order.

**The material, as the drafter counted it and `J-g1` recomputes it.**

- **316 escalations** in split 0's train half: 300 on a CONFLICT and 16 on an
  impasse. 294 distinct tickets carry them.
- **Their true queues**: `SELF_SERVICE_DEFLECT` 114, `T2_TECHNICAL` 99,
  `T1_GENERAL` 53, `BILLING_SPECIALIST` 35, `ACCOUNT_MANAGER` 12,
  `T3_ENGINEERING` 3. None is `SECURITY_INCIDENT` or `ONCALL_ESCALATION`.
- **How contested they are**, in the final base: rules of one queue match 1 of
  them, of two 58, of three 157, of four 99 and of five 1. Over the whole train
  half the shares are close: 28, 266, 482, 223 and 6 of 1,005.
- **How crowded**: between 14 and 150 rules match each, 57 at the median.
- **The keyword**: 8 of the 316 carry it, and 37 of the train half's 1,005.
- **The reach**: none. Every escalation is in the train half, and the split
  groups cases by identity, so no test case shares a ticket with a label.

**The truth** enters only to label and to score, and only through modules
`tests/test_oracle_separation.py` already allows: `rung3.order_search.build_tables`
and `rung3.order_search_ls.space_pools`. No module of this plan imports the
oracle.

---

## 2. The choices that have to be made at signature time

Seven, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 The population is every train-half escalation — the drafter recommends it

A reviewer labels the ticket the system escalated, whatever the proposer did
with it. So the population is all 316, and not only the 286 whose proposal named
a queue. The 286 are where `PLAN_STUDENTS.md`'s figure came from, and `J-g1`
reproduces it.

### 2.2 The instrument is the audit's label-budget search — the drafter recommends it

`rung3/budget_and_balance_ls.py`'s pipeline: the record's greedy as start 0,
then the declared multi-start, `MULTISTART_SEED = 17`, 64 starts and
`move+swap`. Its functions are called with a set of labelled cases where the
record calls them with a random draw. Nothing else moves. It is the instrument
the random arrivals' figures came from, so the comparison is like for like, and
`J-g1` shows it reproduces both those figures and `PLAN_STUDENTS.md`'s.

### 2.3 The comparator is the record's own draws, not new ones — the drafter recommends it

The random arrivals at each budget are the five draws of
`results3/budget_and_balance_ls.json` on split 0, read as published. Drawing new
ones would put a second figure beside a published one. `J-g1` re-runs ten of them
to show the instrument is the record's.

### 2.4 The budgets are the record's — the drafter recommends them

10, 50, 100 and 251 labels, the curve's own, and all 316 beside them. The rows
read 50 and 251. 50 is the budget rung 4 was opened on (*50 labels are enough to
order*, re-measured by the audit's Step 3), and 251 is the largest the
escalations can fill short of all of them.

### 2.5 Five draws, as the record's — the drafter recommends it

Each random selection is drawn five times, with `random.Random(17000 + d)` for
`d` in 0 to 4, sampled without replacement and sorted. Five is the record's
count, so the two medians are of the same size.

### 2.6 Three selection rules that read no truth — the drafter recommends them

- **random**: five draws, as above.
- **arrival**: the first `k` escalations in the order they came, what a reviewer
  labelling as tickets arrive and stopping at `k` would label. Reported.
- **crowded**: the `k` escalations the most rules of the final base match,
  ties to the earlier. `J-d` reads it at 50.

**A rule by contest was considered and dropped.** Ordering the escalations by
how many queues their matching rules name would not separate them: the counts
of §1 put most of them, and most of the train half, at three or four.

### 2.7 The thread's name and letter

`PLAN_ESCALATIONS.md`, rows `J-a` to `J-f`, for the reviewer's *judgement*. `A`
to `F`, `H`, `I`, `K`, `L`, `M`, `O` to `Y` are taken. The naming is Sergi's to
overrule.

---

## 3. The selections and the instrument, exactly

**The escalations.** Rung 1's records with `escalated` true whose case falls in
`rung3.order_search.split(corpus, truth, seed=17)`'s train half, in arrival
order. 316.

**The selections at budget `k`.** `random` draws `k` of the 316 with
`random.Random(17000 + d).sample`, `d` in 0 to 4, and sorts them. `arrival` takes
the first `k`. `crowded` sorts the 316 by the number of the 577 rules matching
the case, most first and the earlier case first on a tie, and takes `k`. At
`k = 316` every selection is the same set, read once. **No selection reads the
truth**: they read case indices, arrival order and the matching rules, and
`J-g2` checks it.

**The instrument, for a labelled set `S`:**

1. masks over `S` with the truth, `rung3.local_search.build_masks` on the `puro`
   pool;
2. the record's greedy over `S`, `rung3.budget_and_balance.greedy`;
3. the declared multi-start from it, `rung3.budget_and_balance_ls.search`;
4. the best order scored by `score_order` on split 0's test half and over
   `space_pools`' `puro` masks.

This is `budget_and_balance_ls.run_config` with `S` where it draws. `J-g1` checks
that the record's own draws, passed through it, give the record's figures.

---

## 4. The reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | surface | owning record |
|---|---|---|---|
| arrival order | 519 of 995 · 42,310 of 134,400 | test split 0 · space | `results3/floor_by_pool.json` |
| the search on all 1,005 train cases | 843 · 0.6033 | test split 0 · space | `results3/order_search_ls.json`, split 0, `puro` |
| random arrivals at 10, 50, 100, 251 | medians 532, 717, 791, 820 · 0.3400, 0.3993, 0.4361, 0.5302 | test split 0 · space | `results3/budget_and_balance_ls.json`, split 0 |
| the same, five-split means | 0.5767, 0.7410, 0.7771, 0.8227 | corpus test | `results3/FINDINGS_AUDIT.md`, Step 3 |
| the order on the truth at the 286 named escalations | 814 · 73,420 | test split 0 · space | `results_students/score.json` |
| the order on the proposer's answers at the same 286 | 483 · 61,305 | test split 0 · space | the same |

The space medians are published to four decimals, so `J-e` reads its own median
at the same precision.

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

A. **The audit's instrument is called, not copied**: `rung3/budget_and_balance_ls`,
   `budget_and_balance`, `local_search` and `order_search`. A second construction
   that drifted from the first would set two different searches side by side.
B. **The records are inputs, never outputs.** Nothing outside
   `results_escalations/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §9 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow.
F. **The dry run searches no order on a set of escalations** but the 286 named,
   whose figure is published. It prints pass or fail and figures already
   published. `tests/test_escalations.py` walks `escalations/gates.py` to say so.
G. **The random arrivals are never re-drawn for a row.** Their figures are the
   record's, and the ten the gate re-runs must equal them.

---

## 6. Known traps

**6.1 — The escalations are the loop's choice.** Rung 1's specificity engine
escalated its CONFLICTs; another engine escalates elsewhere. `PLAN_REUSE.md`'s
loop, on rung 2's engine, escalated coverage impasses, few of them. Every row
here is about rung 1's escalations and rung 1's rules, **selective labels** in
`IDEAS.md`'s term.

**6.2 — The order is searched once, at the end, on the final base.** A deployed
reviewer's labels would arrive while the base grows, and the order would be
searched again as they do. The `crowded` rule counts the final base's rules too.

**6.3 — Five draws make a noisy median.** The record's draws at 50 run from 574
to 769 of 995. §0's *thin* label says where a verdict lies inside that spread,
and §8 reports every draw.

**6.4 — The random arrivals hold escalations too.** A random train case is an
escalation about one time in three: the record's draws at 50 hold 11 to 19 of
them. So the comparison is between the escalations and the train half, of which
they are a third, not between disjoint sets.

**6.5 — Copies.** 316 escalations carry 294 tickets, so a draw can hold two
labels of one ticket, as the record's draws can hold two copies of a case. Both
are counted as the record counts them.

**6.6 — The space is read at four decimals on the comparator's side.** The
record publishes its space scores so. `J-e` rounds its own median the same way.

**6.7 — `IDEAS.md`'s 91% is one subset.** It is the 286 named escalations, of
the train half's 316. The rows read draws of the 316.

---

## 7. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **J-g1 — The material and the instrument are the records'.**
  - The suite is green.
  - The material of §1 recomputes: 316 escalations, 300 on a CONFLICT, 294
    distinct tickets, their true queues, their keyword tickets and their
    matching counts.
  - Arrival order gives 519 and 42,310.
  - The instrument reproduces the record's split-0 rows: with all 1,005 train
    cases, 0.8472 and 0.6033; with each of the record's five draws at 10 labels
    and at 50, its test and space scores to the record's four decimals.
  - On the 286 named escalations it reproduces `PLAN_STUDENTS.md`'s 814 and
    73,420.
- **J-g2 — The selections read no truth.** Built twice, they are equal. Every
  set has its size and lies inside the 316. The selection module reads no
  truth, and a test walks its syntax tree to say so.
- **J-g3 — No label reaches the test split.** Every selected case is in the
  train half, and no test case shares a ticket with one.
- **J-g4 — The signature**, §9.

> **[NOTE 2026-10-18] Run before signature, as for every free plan since
> `PLAN_PRIMACY.md`: the plan, its package and its blocking checks.** The first
> three pass. `PYTHONHASHSEED=0 python3 -m escalations.score --dry-run`, zero API
> calls, nothing written, 263 s, most of it the suite. Without the dry run,
> `python3 -m escalations.score` exits at the gate in 0.05 s and creates no
> directory.
>
> - **`J-g1`.** The suite is green, 1,854 tests, and green on 3.10 too. §1's
>   material recomputes, and arrival order gives 519 and 42,310. The instrument
>   reproduces the audit record's split-0 rows: 0.8472 and 0.6033 with all 1,005
>   train cases, and each of its ten draws at 10 and 50 labels to the record's
>   four decimals. On the 286 named escalations it gives `PLAN_STUDENTS.md`'s 814
>   and 73,420.
> - **`J-g2`.** The 29 labelled sets, built twice, are equal; each has its size
>   and lies inside the 316; `selections.py` names no truth.
> - **`J-g3`.** Every labelled case is in the train half, and no test case
>   shares a ticket with one.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 8. The stage — scoring (free)

**Deliverable.** `escalations/score.py` → `results_escalations/score.json`, and
`results_escalations/FINDINGS_ESCALATIONS.md`, which owns every figure.

**What it does.** `J-g1` to `J-g4`, in that order and all blocking. Then, at 10,
50, 100 and 251 labels, the random selection's five orders, the arrival order's
and the crowded order's, and the order on all 316; each scored on test split 0
and over the space. Then `J-a` to `J-e`, each with its label.

**J-f, reported:**

- **Every selection at every budget on both surfaces**, with each of the five
  draws, beside the random arrivals' five, and the order on all 316.
- **The labelled sets' make-up**: their outcomes, their true queues and their
  keyword tickets, for every selection.
- **The rare classes**: right decisions on `ACCOUNT_MANAGER`, `T3_ENGINEERING`,
  `SECURITY_INCIDENT` and `ONCALL_ESCALATION`, on the test split, for every
  order the stage searches.
- **The curve** of each selection as a share of the gain, beside the random
  arrivals'.

---

## 9. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money**
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §8): it is the order of events,
that §0 was signed before any figure that could inform it existed. The gate
reads `PLAN_ESCALATIONS.md` and no other plan, and counts signatures rather than
stopping at the first. Every line starting `**Signed by Sergi:` must be filled
in, and there must be at least one. The counting is `reuse/plan.py`'s, called
with this plan's path. No flag skips the gate; `--dry-run` runs `J-g1` to `J-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The records of §1. `SPLIT = 0`, `SPLIT_SEED = 17`,
  `N_SPACE = 134400`.
- **The selections.** `BUDGETS = (10, 50, 100, 251)`, `N_ESCALATIONS = 316`,
  `DRAWS = 5`, `DRAW_SEED = 17000`; the three rules of §2.6.
- **The instrument.** Rung 3's declared constants, imported.
- **The lines of §0.** `681`, `717`, `820` and `0.3993`; `J-d` reads `J-a`'s
  median.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
escalations/__init__.py
escalations/plan.py         the gate and the constants of this section
escalations/selections.py   the 316, and the three rules at each budget
escalations/instrument.py   the audit's search on a labelled set, both surfaces
escalations/gates.py        J-g1 to J-g4
escalations/score.py        the stage: J-a to J-e, the readings of J-f
tests/test_escalations.py
results_escalations/score.json
results_escalations/FINDINGS_ESCALATIONS.md
```

**The plumbing, in the same commit as the modules**: `escalations` joins
`CODE_ROOTS` in `harness/provenance.py` and the roots the oracle scan walks in
`tests/test_oracle_separation.py`; the README's table of writers gains
`escalations/score.py`'s row, and its list of dry runs gains the command. **The
list of modules allowed to see the oracle does not grow.**

---

## 10. Definition of done

- [ ] `results_escalations/score.json` with `_env`, produced with
      `PYTHONHASHSEED=0` from a clean tree.
- [ ] `J-g1` to `J-g4` passed before any record was written.
- [ ] The plumbing of §9, and tests pinning its constants; the whole suite green
      on 3.10 and 3.12.
- [ ] Every figure in prose names its surface.
- [ ] `results_escalations/FINDINGS_ESCALATIONS.md` owns every figure.
- [ ] `STATUS.md`: the scoreboard gains the `J` thread, five adjudicated rows
      and one reported. `IDEAS.md`: the item answered as far as the rows go.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 11. What this plan cannot settle, declared before it runs

1. **What a label costs, and who gives it.** The reviewer here is the truth.
   A real one errs, and a reviewer's error rate would need its own model.
2. **The online loop.** Labels would arrive while the base grows and the order is
   searched again (§6.2). Nothing here runs the loop.
3. **Other loops' escalations.** `PLAN_REUSE.md`'s are coverage impasses on rung
   2's engine, whose bases are small and decided by subsumption and edges, not
   by a searched order. A plan on them would need another instrument.
4. **Rung 4's channel.** It labels the system's decisions, and mostly its
   errors. It is not compared here.
5. **Other rules for which first.** A student's uncertainty, or the proposer's
   answer disagreeing with the rules' decision, would read more than the rules;
   neither is tried.
