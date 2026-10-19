# PLAN_SPOTCHECK — what a random audit of the system's decisions buys beside the escalations

> **[CLOSED 2026-10-19] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-10-19, before any figure of the plan existed. The five rows were
> adjudicated the same day: **`N-a` and `N-e` hold; `N-b`, `N-c` and `N-d` are
> refuted**, every one but `N-b` thinly, and `N-f` is reported. Fifty audited
> decisions add little to the escalations where tickets arrive. 251 close two
> thirds of the gap to the whole train half, mostly in `T3_ENGINEERING`, which
> an order learns all at once or not at all. Over the function the audited sets
> fall below the escalations alone. **The figures are owned by
> [`results_spotcheck/FINDINGS_SPOTCHECK.md`](results_spotcheck/FINDINGS_SPOTCHECK.md)**,
> and no result is to be read off this file; the scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-10-19. The line is kept
> unedited and this banner is its correction. The banner touches neither §0 nor
> its note, adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-10-19, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §9 says why the gate binds anyway.

**This plan exists because `PLAN_ESCALATIONS.md` found what labels at the
escalations never buy.** Rung 3's search orders the 577 rules from labelled
cases. Handed the truth of all 316 train-half escalations of rung 1, it reaches
814 of the 995 cases of corpus test split 0. That is 29 short of the 843 it
reaches with the truth of all 1,005 train cases, and 18 short in
`T3_ENGINEERING` alone, a queue that escalated 3 times in 316
([`results_escalations/FINDINGS_ESCALATIONS.md`](results_escalations/FINDINGS_ESCALATIONS.md)).
[`IDEAS.md`](IDEAS.md) carries the question in *What `PLAN_ESCALATIONS.md`
opens*: **whether a small random audit of decisions beside the escalations would
buy it.** That plan named the audit as the alternative and did not run it.

**The decisions are where the rare queues went.** Rung 1's engine decided 689 of
the train half's 1,005 cases itself, without escalating, and it only ever decided
four queues: `T2_TECHNICAL`, `BILLING_SPECIALIST`, `SELF_SERVICE_DEFLECT` and
`T1_GENERAL`. So the decisions hold:
- 57 of the train half's 60 `T3_ENGINEERING` tickets;
- all 10 of its `SECURITY_INCIDENT` tickets;
- 42 of its 54 `ACCOUNT_MANAGER` tickets;
- all 4 of its `ONCALL_ESCALATION` tickets.

Every one of them was decided wrong. A reviewer who answers the escalations
never sees those tickets, and one who audits the decisions at random does.

**This plan adds a random audit of the decisions to the escalations' labels**, at
the optimizer audit's label budgets, on split 0, with the same instrument, and
reads it against the two figures it sits between: the escalations alone and the
whole train half. Here *the optimizer audit* is rung 3's audit of August 8, 2026,
whose label-budget search is the instrument. *The audit* is this plan's, a
reviewer's random sample of the system's decisions.

**What it would change.**

- **If fifty audited decisions close half the gap**, a deployment needs the
  escalations' reviewer and a small audit, not a reviewer of everything.
- **If even 251 do not**, the gap is the price of leaving most of the train half
  unlabelled, and an audit that closes it is most of the train half.
- **Whether the audit teaches `T3_ENGINEERING`** is read directly, on the class
  the escalations never teach.

**None of this plan's figures exists**, except its two endpoints, which `N-g1`
reproduces:
- the escalations alone, published by `PLAN_ESCALATIONS.md`;
- the whole train half, published by the optimizer audit.

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
  them. Every audited set holds all of them.
- **The decisions** are the other 689 cases of that train half. Rung 1's loop
  did not escalate them: its engine decided them itself, right on 360 (§1).
- **An audited set at `k`** is the escalations plus `k` decisions drawn at
  random. There are five seeded draws. They are nested: a draw's `k` decisions
  are the first `k` of one shuffle of the 689 (§3).
- **A labelled order** is rung 3's search over the 577 rules, `puro` pool, its
  declared constants, labelled with the **truth** of a set of cases and nothing
  else. It is the optimizer audit's label-budget instrument, called through
  `escalations/instrument.py` and not copied (§3). Its statistic, for an
  audited set at `k`, is the median of the five draws' orders.
- **The escalations alone** give **814** of 995 on test split 0 and **73,020**
  of 134,400 points over the space. They get **0** of the test split's 57
  `T3_ENGINEERING` cases right.
- **The whole train half** gives **843**, 0.6033 of the space and **18** of
  those 57. At `k = 689` an audited set is the whole train half.
- **The gap** is what separates the two on the test split: 843 − 814 = 29 cases.
  Half of it, rounded up, is 15, so its line is **829**.
- **Corpus test split 0** is 995 cases; **the space** is the 134,400
  combinations. Every count is of decisions right against the truth.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **N-a** | **Fifty audited decisions beside the escalations buy something where tickets arrive.** | corpus test split 0, 995 cases: the audited sets at 50, the median of five orders | **> 814** | **≤ 814** |
| **N-b** | **They close half the gap to full supervision.** | the same statistic | **≥ 829** | **< 829** |
| **N-c** | **They teach `T3_ENGINEERING`, which the escalations never teach.** | corpus test split 0's 57 `T3_ENGINEERING` cases: the same five orders, the median count right | **≥ 9** | **< 9** |
| **N-d** | **Over the function they buy something too.** | exhaustive space, 134,400 points: the same five orders, the median count right | **> 73,020** | **≤ 73,020** |
| **N-e** | **251 audited decisions close half the gap.** | corpus test split 0: the audited sets at 251, the median of five orders | **≥ 829** | **< 829** |
| **N-f** | *Reported, not adjudicated.* **What reading the rows needs.** | §8's readings: every audited set and every audit alone at every budget on both surfaces, with each draw; the audit alone beside random escalations and random arrivals; the rare classes; the sets' make-up; the curve as a share of the gap | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-19)**

**One label, and it does not change a verdict.** A median of five draws is noisy,
and the baseline the first rows are read against is one order, not five. **A
verdict is labelled *thin* when its line lies inside the range of the five draws
it is read on**: the five orders' test counts for `N-a`, `N-b` and `N-e`, their
`T3_ENGINEERING` counts for `N-c`, and their space counts for `N-d`.

**What a hold says and what a refutation says.**

- **`N-a` holding** says fifty audited decisions add to what the escalations buy
  where tickets arrive. Refuted, the escalations' 814 is not improved by a small
  audit, as far as five draws can show.
- **`N-b` and `N-e`** read one line at two budgets:
  - both holding says a small audit closes half the gap;
  - `N-b` refuted with `N-e` holding says closing half the gap takes between 50
    and 251 audited decisions;
  - both refuted says even 251 is not enough.
- **`N-c`** reads the class. Holding, the audit teaches what the escalations
  never do. Refuted, fifty decisions hold too few `T3_ENGINEERING` tickets, or
  the class is not learnt from a few.
- **`N-d`** asks whether the gain carries to the space. `IDEAS.md`'s standing
  note says arguments that a quantity carries across surfaces lose.

**Why the lines are where they are.** `N-a` and `N-d` sit at the escalations'
own figures, so they ask whether the audit buys anything. `N-b` and `N-e` sit at
half the gap. `N-c` sits at half of what the whole train half buys in
`T3_ENGINEERING`. None is at the drafter's expectation. Ties go against the claim
in every row.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **The documents.** `STATUS.md`, `IDEAS.md`, `FINDINGS_ESCALATIONS.md` with its
  readings after the verdicts, `FINDINGS_STUDENTS.md`,
  `results3/FINDINGS_AUDIT.md`'s Step 3, and the three analytical documents
  `CLAUDE.md` asks to be read first, earlier in the same session.
- **The records' published figures**, read for this plan:
  - `results_escalations/score.json`: every figure, in particular every
    escalation order's test, space and rare-class counts, and the escalations
    alone, 814, 73,020 and 0 of 57;
  - `results3/budget_and_balance_ls.json`: split 0's rows at every budget, and
    its per-class count on split 0, which gives the whole train half's 18 of
    57 and the 20 any order can reach;
  - `results3/order_search_ls.json` and `results3/floor_by_pool.json`: split
    0's searched row and arrival order.
- **Facts about the material, counted by the drafter** (§1):
  - the decisions' count and outcome, and how many rung 1 decided right;
  - their true queues and the queues decided for them;
  - their keyword tickets and distinct tickets;
  - how many queues and rules match each of them in the final base;
  - for each of the five draws at each budget, how many `T3_ENGINEERING`,
    `SECURITY_INCIDENT` and keyword tickets it holds, and how many decisions it
    holds that rung 1 got wrong.

  None is a score of an order labelled at decisions. The last are counted
  because `PLAN_ESCALATIONS.md`'s `J-d` was banded on a selection whose make-up
  nobody had counted.
- **The code**: `escalations/`, `rung3/budget_and_balance_ls.py`,
  `budget_and_balance.py`, `local_search.py` and `order_search.py`, and
  `reuse/plan.py` for the form of a free plan's gate.
- **The blocking checks' output** (§7), which prints pass or fail and figures
  already published.
- **Not seen, because nobody has computed them**: any order labelled at a set
  holding decisions, at any budget, on either surface, except the whole train
  half; and anything about the audit alone.

**What the drafter expects, written down so the scoreboard can score it.**
`N-a` and `N-e` hold; **`N-b`, `N-c` and `N-d` are refuted**. The drafter trusts
`N-d` least, then `N-e`.

- **`N-a` holds, about two in three.** Rung 1 got wrong 17 to 25 of each draw's
  fifty decisions, and the escalations alone leave the rare queues to chance.
- **`N-b` refuted, about seven in ten.** Half the gap is 15 cases, and 18 of the
  29 are `T3_ENGINEERING`. A draw of fifty holds 2 to 4 of its tickets, beside
  the escalations' 3.
- **`N-c` refuted, about three in five.** That is 5 to 7 `T3_ENGINEERING` labels
  among 366. The escalation orders, labelled with 3, were right on at most 2 of
  57.
- **`N-d` refuted, about even.** The escalations' 73,020 is the top of their own
  orders' spread over the space, so the line starts from a lucky figure. Four
  draws of five hold no `SECURITY_INCIDENT` ticket at fifty, and over the space
  the escalation orders followed that class at the top (`FINDINGS_ESCALATIONS.md`,
  read after its verdicts).
- **`N-e` holds, about three in five.** At 251 a draw holds 16 to 32
  `T3_ENGINEERING` tickets. The optimizer audit's random arrivals rise from 820
  at 251 labels to 843 at 1,005.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 36
of 89 adjudicated rows came out refuted. Here the drafter expects three of five
refuted, because the lines sit where the question puts them and not where the
drafter expects the figures.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls. No loop runs; rung 3's search is re-run
on new sets of labels.

**Already paid for, and read as they stand:**

- `results/llm_run.json`: rung 1's 2,000 records, which say which cases
  escalated, and its 577 rules, through `rung3.order_search.load`.
- `results_escalations/score.json`: the escalations alone and every escalation
  order; `N-g1` reproduces the first.
- `results3/budget_and_balance_ls.json`: the random arrivals' draws on split 0,
  and the per-class count of the whole train half; `N-g1` reproduces the full
  row, its per-class count and the five draws at 50 labels.
- `results3/order_search_ls.json` and `results3/floor_by_pool.json`: the full
  search on split 0 and arrival order.

**The material, as the drafter counted it and `N-g1` recomputes it.**

- **689 decisions** in split 0's train half: every record there whose outcome is
  `ACTION`. At the time, rung 1's engine was right on 360 of them. 616 distinct
  tickets carry them.
- **Their true queues**: `T2_TECHNICAL` 263, `SELF_SERVICE_DEFLECT` 139,
  `BILLING_SPECIALIST` 100, `T1_GENERAL` 74, `T3_ENGINEERING` 57,
  `ACCOUNT_MANAGER` 42, `SECURITY_INCIDENT` 10, `ONCALL_ESCALATION` 4.
- **The queues decided for them**: `T2_TECHNICAL` 388, `BILLING_SPECIALIST` 119,
  `SELF_SERVICE_DEFLECT` 94, `T1_GENERAL` 88, and no other. So every decision on
  a rare queue's ticket was wrong. The 57 `T3_ENGINEERING` tickets were decided
  `T2_TECHNICAL` 50 times, `SELF_SERVICE_DEFLECT` 4 and `BILLING_SPECIALIST` 3.
- **With the escalations**, the train half holds 60 `T3_ENGINEERING` tickets, 57
  of them decisions; 54 `ACCOUNT_MANAGER`, 42 decisions; 10 `SECURITY_INCIDENT`
  and 4 `ONCALL_ESCALATION`, all decisions.
- **The keyword**: 29 of the decisions carry it, all 10 `SECURITY_INCIDENT`
  tickets among them; 8 of the escalations do.
- **How contested**, in the final base: rules of one queue match 27 decisions,
  of two 208, of three 325, of four 124, of five 2 and of six 3. Between 8 and
  145 rules match each, 37 at the median, against the escalations' 14 to 150
  and 57.
- **The reach**: none. Every decision is in the train half, and the split groups
  cases by identity, so no test case shares a ticket with a label.

**The five draws' make-up**, counted before signature. Each cell gives
`T3_ENGINEERING`, `SECURITY_INCIDENT` and keyword tickets, then the decisions
rung 1 got wrong:

| draw | at 10 | at 50 | at 100 | at 251 |
|---|---|---|---|---|
| 0 | 0, 0, 0 · 3 | 3, 0, 3 · 17 | 9, 3, 6 · 47 | 18, 5, 13 · 118 |
| 1 | 1, 1, 1 · 5 | 3, 1, 2 · 20 | 13, 1, 4 · 47 | 22, 2, 8 · 114 |
| 2 | 1, 0, 0 · 5 | 2, 0, 0 · 21 | 10, 0, 2 · 42 | 32, 3, 9 · 119 |
| 3 | 1, 0, 1 · 4 | 4, 0, 2 · 25 | 6, 0, 3 · 47 | 16, 3, 13 · 123 |
| 4 | 1, 0, 0 · 4 | 2, 0, 0 · 21 | 8, 0, 2 · 41 | 20, 2, 9 · 115 |

> **[NOTE 2026-10-19] A count in `PLAN_ESCALATIONS.md` §1, found while counting
> this one.** That plan put the train half's last share of queues matching at 6
> of five queues. It is 3 of five and 3 of six. No row of that plan read it.

**The truth** enters only to label, to score and to count the material. It comes
through modules `tests/test_oracle_separation.py` already allows:
`rung3.order_search.build_tables` and `rung3.order_search_ls.space_pools`, both
reached through `escalations/instrument.py`. No module of this plan imports the
oracle.

---

## 2. The choices that have to be made at signature time

Seven, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 The audit's population is every train-half decision — the drafter recommends it

A reviewer who audits the system checks what it decided itself, whatever it
decided. So the population is the 689 decisions, right or wrong, and not a
random sample of the whole train half, which would draw the escalations twice.

### 2.2 The escalations are all labelled, in every audited set — the drafter recommends it

The reviewer who answers the escalations is assumed, since the loop sends every
one of them somewhere. The audit is what is added. So every audited set holds
all 316, and its baseline is the escalations alone.

### 2.3 The instrument is the optimizer audit's label-budget search — the drafter recommends it

`escalations/instrument.py`'s `read`, which calls
`rung3/budget_and_balance_ls.py`'s pipeline: the record's greedy as start 0,
then the declared multi-start, `MULTISTART_SEED = 17`, 64 starts and
`move+swap`. It is the instrument both endpoints came from, and `N-g1` shows it
reproduces both.

### 2.4 The budgets are the record's — the drafter recommends them

10, 50, 100 and 251 audited decisions, the optimizer audit's own budgets. At all
689 an audited set is the whole train half, which `N-g1` reproduces as the
curve's end. The rows read 50 and 251, as `PLAN_ESCALATIONS.md`'s did.

### 2.5 Five draws, nested — the drafter recommends it

Each draw `d`, in 0 to 4, is one shuffle of the 689 decisions in arrival order
by `random.Random(18000 + d)`. Its audited decisions at `k` are the first `k` of
that shuffle, sorted. **This differs from `PLAN_ESCALATIONS.md`, whose draws were
independent at each budget.** Nesting is what a reviewer who keeps auditing would
produce, and it makes each draw's curve one growing set of labels. Five is the
record's count.

### 2.6 The audit alone is read beside, on the same draws — the drafter recommends it

For each draw and budget the same `k` decisions are also labelled without the
escalations. That is reported, not banded. It says whether a decision is a
better or a worse label than an escalation or a random arrival at the same
budget, and, paired by draw, what the escalations add to the audit.

**A stratified audit was considered and dropped.** Spreading the audit across
the queues the system decided would spread it across four common queues. The
engine decided no rare one, so the stratification would not reach the rare
queues any better than a random draw does.

### 2.7 The thread's name and letter

`PLAN_SPOTCHECK.md`, rows `N-a` to `N-f`, for the *non-escalated* decisions.
"Audit" is kept out of the names because the repository's audit is rung 3's
optimizer audit. `A` to `F`, `H` to `M` and `O` to `Y` are taken. The naming is
Sergi's to overrule.

---

## 3. The selections and the instrument, exactly

**The escalations.** `escalations.selections.escalations` on split 0's train
half: rung 1's records with `escalated` true, in arrival order. 316.

**The decisions.** Rung 1's records with `escalated` false whose case falls in
`rung3.order_search.split(corpus, truth, seed=17)`'s train half, in arrival
order. 689.

**The draws.** For `d` in 0 to 4, the 689 in arrival order are shuffled by
`random.Random(18000 + d).shuffle`, and the audited decisions at `k` are the
first `k`, sorted.

**The sets at budget `k`, draw `d`.**
- `mix|k|d` is the 316 escalations with the `k` audited decisions.
- `audit|k|d` is the `k` audited decisions alone.

There are 40 of them. **No selection reads the truth.** They read case indices,
arrival order and rung 1's `escalated` flag, and `N-g2` checks it, string
literals included.

**The instrument, for a labelled set `S`**, is `escalations/instrument.py`'s
`read`:

1. masks over `S` with the truth, `rung3.local_search.build_masks`, on the `puro`
   pool;
2. the record's greedy over `S`;
3. the declared multi-start from it, `rung3.budget_and_balance_ls.search`;
4. the best order scored by `score_order` on split 0's test half and over
   `space_pools`' `puro` masks, and its right decisions on the test split's four
   rare queues.

---

## 4. The reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | surface | owning record |
|---|---|---|---|
| arrival order | 519 of 995 · 42,310 of 134,400 | test split 0 · space | `results3/floor_by_pool.json` |
| the whole train half, 1,005 labels | 843 · 0.6033 | test split 0 · space | `results3/order_search_ls.json`, split 0, `puro` |
| the same, by rare class | `T3_ENGINEERING` 18 of 57, `ACCOUNT_MANAGER` 19 of 55, `SECURITY_INCIDENT` 5 of 10, `ONCALL_ESCALATION` 0 of 3 | test split 0 | `results3/budget_and_balance_ls.json`, `per_class_split0` |
| the most any order can reach | 20, 21, 10 and 3 of the same | test split 0 | the same |
| the escalations alone, 316 labels | 814 · 73,020 (0.5433) | test split 0 · space | `results_escalations/score.json` |
| the same, by rare class | 0, 20, 4 and 0 | test split 0 | the same |
| random escalations at 10, 50, 100, 251 | medians 559, 737, 794, 816 · 0.2596, 0.3426, 0.4223, 0.4278 | test split 0 · space | the same |
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
   `results_spotcheck/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §9 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow.
F. **The dry run searches no order on a set holding decisions** but the whole
   train half, and no set of escalations but all 316: both figures are
   published. It prints pass or fail and figures already published.
   `tests/test_spotcheck.py` walks `spotcheck/gates.py` to say so.
G. **The comparators are read from their records and never re-drawn.** The
   figures the gate re-runs must equal them.

---

## 6. Known traps

**6.1 — The decisions are the loop's choice too.** Rung 1's specificity engine
decided only four queues, and every rare queue's ticket it decided, it decided
wrong. Another engine decides elsewhere. Every row here is about rung 1's
decisions and rung 1's rules.

**6.2 — The baseline is one order.** The escalations alone are one search, and
over the space its 73,020 is the top of the escalation orders' own spread. A row
read against it carries its luck, and the thin label says where.

**6.3 — The draws are nested.** A draw's 251 holds its 100, its 50 and its 10,
so the budgets are not independent samples.

**6.4 — Every search starts from the same declared starts.** Two sets can land
on one order, as draw 3 of 251 and all 316 seem to have in
`FINDINGS_ESCALATIONS.md`. A plateau in the curve may be that.

**6.5 — `T3_ENGINEERING` has a ceiling.** Only 20 of the test split's 57 cases
are covered by a rule of that queue, so no order is right on more than 20, and
`N-c`'s 9 is close to half of what any order can do.

**6.6 — A check on names misses a subscript.** `PLAN_ESCALATIONS.md`'s `J-g2`
walked names, attributes, arguments and imports, so `r["truth"]` would have
passed it. Its selections never read one, but the check could not have said so.
`N-g2` checks string literals too.

**6.7 — An audit is also error discovery.** Rung 1 got wrong 17 to 25 of each
fifty audited decisions. Whether the order is bought by the errors or by the
labels as such is not separated here. The record reports the count.

**6.8 — The audit alone is not the comparator of any row.** It is reported
beside random escalations and random arrivals at the same budget, whose draws
are independent of it and of each other.

---

## 7. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **N-g1 — The material and the instrument are the records'.**
  - The suite is green.
  - The material of §1 recomputes:
    - the decisions' count and outcome, and how many rung 1 got right;
    - their true and decided queues;
    - their keyword and distinct tickets;
    - their matching counts;
    - each draw's make-up at each budget.
  - Arrival order gives 519 and 42,310.
  - The records hold the figures §4 gives: the escalations alone and the whole
    train half, by rare class too.
  - The instrument reproduces them:
    - all 1,005 train cases give 0.8472, 0.6033 and 18, 19, 5 and 0 by rare
      class;
    - all 316 escalations give 814, 73,020 and 0, 20, 4 and 0;
    - each of the optimizer audit's five draws at 50 labels gives its test and
      space scores to the record's four decimals.
- **N-g2 — The selections read no truth.**
  - Built twice, they are equal.
  - Every audited set holds all 316 escalations and exactly its `k` decisions.
  - Every audit alone is those `k` decisions.
  - A draw's smaller budgets nest inside its larger.
  - The selection module names no truth, in a name or in a string literal.
- **N-g3 — No label reaches the test split.** Every labelled case is in the
  train half, and no test case shares a ticket with one.
- **N-g4 — The signature**, §9.

> **[NOTE 2026-10-19] Run before signature, as for every free plan since
> `PLAN_PRIMACY.md`: the plan, its package and its blocking checks.** The first
> three pass. `PYTHONHASHSEED=0 python3 -m spotcheck.score --dry-run`, zero API
> calls, nothing written, 247 s, most of it the suite. Without the dry run,
> `python3 -m spotcheck.score` exits at the gate in 0.06 s and creates no
> directory.
>
> - **`N-g1`.** The suite is green, 1,881 tests, and green on 3.10 too.
>   - §1's material recomputes, and so does each draw's make-up.
>   - Arrival order gives 519 and 42,310.
>   - The records hold §4's endpoints.
>   - The instrument reproduces them: 0.8472, 0.6033 and 18, 19, 5 and 0 by
>     rare class with all 1,005 train cases; 814, 73,020 and 0, 20, 4 and 0
>     with all 316 escalations.
>   - Each of the optimizer audit's five draws at 50 labels gives the record's
>     four decimals.
> - **`N-g2`.** The 40 labelled sets, built twice, are equal. Each audited set
>   is the escalations and exactly its decisions, and the budgets nest.
>   `selections.py` names no truth in a name or a string.
> - **`N-g3`.** Every labelled case is in the train half, and no test case
>   shares a ticket with one.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 8. The stage — scoring (free)

**Deliverable.** `spotcheck/score.py` → `results_spotcheck/score.json`, and
`results_spotcheck/FINDINGS_SPOTCHECK.md`, which owns every figure.

**What it does.** `N-g1` to `N-g4`, in that order and all blocking. Then, at 10,
50, 100 and 251 audited decisions and for each of the five draws, two orders:
- the audited set's;
- the audit alone's.

Each is scored on test split 0, over the space and on the four rare queues. Then
`N-a` to `N-e`, each with its label.

**N-f, reported:**

- **Every set at every budget on both surfaces**, with each of the five draws,
  between the escalations alone and the whole train half.
- **The audit alone beside random escalations and random arrivals** at the same
  budget, their draws read from `results_escalations/score.json` and
  `results3/budget_and_balance_ls.json`. Paired by draw, the audited set less
  the audit alone: what the escalations add to the audit.
- **The rare classes**: right decisions on `ACCOUNT_MANAGER`, `T3_ENGINEERING`,
  `SECURITY_INCIDENT` and `ONCALL_ESCALATION`, on the test split, for every
  order.
- **The labelled sets' make-up**: the audited decisions' true queues, their
  keyword tickets, and how many of them rung 1 got wrong.
- **The curve** of each audited set as a share of the gap, from 814 to 843, and
  of each audit alone as a share of the gain, from 519 to 843.

---

## 9. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money**
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §8): it is the order of events,
that §0 was signed before any figure that could inform it existed. The gate
reads `PLAN_SPOTCHECK.md` and no other plan, and counts signatures rather than
stopping at the first. Every line starting `**Signed by Sergi:` must be filled
in, and there must be at least one. The counting is `reuse/plan.py`'s, called
with this plan's path. No flag skips the gate; `--dry-run` runs `N-g1` to `N-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The records of §1. `SPLIT = 0`, `SPLIT_SEED = 17`,
  `N_SPACE = 134400`.
- **The sets.** `BUDGETS = (10, 50, 100, 251)`, `N_ESCALATIONS = 316`,
  `N_DECISIONS = 689`, `DRAWS = 5`, `AUDIT_SEED = 18000`; the two arms of §3.
- **The instrument.** Rung 3's declared constants, imported.
- **The lines of §0.** `814`, `829`, `9`, `73,020` and `829`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
spotcheck/__init__.py
spotcheck/plan.py         the gate and the constants of this section
spotcheck/selections.py   the 689 decisions, the nested draws, the two arms
spotcheck/gates.py        N-g1 to N-g4
spotcheck/score.py        the stage: N-a to N-e, the readings of N-f
tests/test_spotcheck.py
results_spotcheck/score.json
results_spotcheck/FINDINGS_SPOTCHECK.md
```

**The plumbing, in the same commit as the modules**: `spotcheck` joins
`CODE_ROOTS` in `harness/provenance.py` and the roots the oracle scan walks in
`tests/test_oracle_separation.py`; the README's table of writers gains
`spotcheck/score.py`'s row, and its list of dry runs gains the command. **The
list of modules allowed to see the oracle does not grow.**

---

## 10. Definition of done

- [ ] `results_spotcheck/score.json` with `_env`, produced with
      `PYTHONHASHSEED=0` from a clean tree.
- [ ] `N-g1` to `N-g4` passed before any record was written.
- [ ] The plumbing of §9, and tests pinning its constants; the whole suite green
      on 3.10 and 3.12.
- [ ] Every figure in prose names its surface.
- [ ] `results_spotcheck/FINDINGS_SPOTCHECK.md` owns every figure.
- [ ] `STATUS.md`: the scoreboard gains the `N` thread, five adjudicated rows
      and one reported. `IDEAS.md`: the item answered as far as the rows go.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 11. What this plan cannot settle, declared before it runs

1. **What a label costs, and who gives it.** The reviewer here is the truth. A
   real one errs.
2. **The online loop.** Labels would arrive while the base grows and the order is
   searched again. Nothing here runs the loop.
3. **An audit of errors only.** Rung 4's channel labels the system's decisions,
   and mostly its errors. That is another channel, and it is not compared here.
4. **Other rules for which decisions to audit.** The system's own margin between
   matching rules, a student's uncertainty, or the proposer's disagreement with
   the rules would read more than a random draw; none is tried.
5. **One split.** Every row is read on split 0, the split both endpoints come
   from. The optimizer audit's curve has five.
