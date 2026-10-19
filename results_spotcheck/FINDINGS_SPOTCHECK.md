# What a random audit of the system's decisions buys beside the escalations — findings

Record opened on October 19, 2026, under [`PLAN_SPOTCHECK.md`](../PLAN_SPOTCHECK.md).
The plan and its package reached `main` in pull request #142, and the signature
and the record below in #143. Sergi signed §0 on 2026-10-19, before any figure
below existed, in a commit of its own: `63beac7` on `main`.

The stage's record, [`score.json`](score.json), names in its `_env` the commit
it was written from: `2c8afbe`, the signing commit as it was made. **That commit
was never pushed.** #142 was merged while the stage ran, so the four commits
made after it were rebased onto `main` and pushed as #143, where the signing
commit is `7497aac`. The rebase merge of #143 gave it `63beac7` on `main`. The
three have the same subject, the same tree and the same `git patch-id
--stable`. The code digest the `_env` records, `8559939020da9b13`, is the one
#143's tip computes.

**This record owns every figure in it.**

**A POST-RUN reading was added on 2026-10-19**: [`readings.json`](readings.json),
by `spotcheck/readings.py`, in its own section below. It reached `main` in pull
request #146. Its `_env` names `6379e0f`, the branch commit that wrote its
expectation, and that commit is `cde21d9` on `main`. The two have the same
tree, the same subject and the same `git patch-id --stable`. The reading's code
digest, `88d69d06a4cf09d1`, is its own. It moves no verdict.

**The stage adjudicated the five signed rows on 2026-10-19: two hold and three
are refuted, and four of the five are thin.**

- **Fifty audited decisions beside the escalations buy four cases where tickets
  arrive.** On corpus test split 0, the five orders labelled with the truth of
  all 316 escalations and fifty random decisions are right on 806 to 827 of 995
  cases, 818 at the median. The escalations alone are right on 814 (`N-a` holds,
  *thin*). That is 14% of the 29 cases between the escalations alone and the
  whole train half, not half (`N-b` refuted).
- **251 audited decisions close two thirds of that gap.** Their median is 833,
  every draw between 828 and 835 (`N-e` holds, *thin*). At 100 it is 826.
- **`T3_ENGINEERING` is learnt all at once or not at all.** At fifty audited
  decisions the orders are right on 19, 0, 2, 1 and 13 of the test split's 57
  cases of that queue, 2 at the median (`N-c` refuted, *thin*). At 251 every
  draw is right on 13 to 19. The number of the class's tickets in a draw does
  not decide it: one ticket among ten decisions gave 13, and three among fifty
  gave none.
- **Over the space the audited sets are below the escalations alone at every
  budget from fifty on.** At fifty their median is 57,890 of the 134,400 points,
  against 73,020 (`N-d` refuted, *thin*), and at 251 it is 62,905. The whole
  train half is at 81,089. The escalations alone were the high figure the plan
  said they were.
- **Alone, the decisions are the worst labels of the three on the test split.**
  Fifty of them give 694 at the median, against fifty random escalations' 737
  and fifty random arrivals' 717. They are below both at every budget. Reported.

> **PROVENANCE: PRE-REGISTERED.** `N-a` to `N-e` were signed before any of their
> figures existed. **`N-f` is reported, not adjudicated**, and every figure in it
> is computed here for the first time, except the endpoints, which `N-g1`
> reproduced from their records. **Three readings below were chosen after the
> verdicts, and each says so where it is made**: what the audit buys class by
> class, the space shares beside `SECURITY_INCIDENT`, and the orders that are
> the escalations' own. They read figures this record already holds, and none
> moves a verdict. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m spotcheck.score`, on 2026-10-19, from the signing
commit with a clean tree: 880 s, about a sixth of it the suite inside the first
check, and zero API calls. The record is [`score.json`](score.json). Its `_env`
carries `git_dirty: false` and `code_dirty: false`.

**The blocking checks passed again before any order was searched on a set
holding decisions.**

- **`N-g1`.**
  - The suite is green, 1,881 tests.
  - The material of §1 recomputes, and so does each draw's make-up.
  - Arrival order reproduces 519 and 42,310.
  - The records hold the endpoints, and the instrument reproduces them by rare
    class too:
    - 0.8472, 0.6033 and 18, 19, 5 and 0 with all 1,005 train cases;
    - 814, 73,020 and 0, 20, 4 and 0 with all 316 escalations.
  - Each of the optimizer audit's five draws at 50 labels gives the record's
    four decimals.
- **`N-g2`.** The 40 labelled sets, built twice, are equal. Each audited set is
  the escalations and exactly its decisions, and the budgets nest.
  `selections.py` names no truth in a name or a string.
- **`N-g3`.** Every labelled case is in the train half, and no test case shares
  a ticket with one.
- **`N-g4`.** Signed.

**Notation.** *Test* is corpus test split 0, 995 cases; *space* is the 134,400
combinations. Every count is of decisions right against the truth.

- **The endpoints.** *The escalations alone* are right on 814 and 73,020. *The
  whole train half* is right on 843 and 81,089, a share of 0.6033.
- ***The gap*** is the 29 test cases between them. A *share of the gap* is a
  count less 814, over 29.
- **The sets.**
  - *An audited set at `k`* is the 316 escalations with `k` decisions of a
    draw.
  - *The audit alone at `k`* is those `k` decisions alone.
  - The draws are nested: a draw's 251 holds its 100, 50 and 10.
- **The comparators.** *Random escalations* and *random arrivals* at `k` are
  the draws of `results_escalations/score.json` and of the optimizer audit's
  record.

---

## The five rows

| row | statistic | value | line | verdict |
|---|---|---|---|---|
| `N-a` | test: the audited sets at 50, the median of five orders | **818** (0.8221) | > 814 | **holds, thin** |
| `N-b` | the same | **818** | ≥ 829 | **refuted** |
| `N-c` | test, 57 `T3_ENGINEERING` cases: the same five orders, the median count right | **2** | ≥ 9 | **refuted, thin** |
| `N-d` | space: the same five orders, the median count right | **57,890** (0.4307) | > 73,020 | **refuted, thin** |
| `N-e` | test: the audited sets at 251, the median of five orders | **833** (0.8372) | ≥ 829 | **holds, thin** |

The five draws each row is read on, in draw order:

| row | draws 0 to 4 |
|---|---|
| `N-a`, `N-b` | 824, 813, 806, 818, 827 |
| `N-c` | 19, 0, 2, 1, 13 |
| `N-d` | 79,420, 66,020, 57,230, 57,890, 55,204 |
| `N-e` | 828, 835, 833, 832, 833 |

A verdict is *thin* when its line lies inside the range of its five draws.
**Four are**:
- 814 lies inside 806 to 827;
- 9 inside 0 to 19;
- 73,020 inside 55,204 to 79,420;
- 829 inside 828 to 835.

Only `N-b`'s line, 829, is above all five of its draws.

**The drafter expected `N-a` and `N-e` to hold and `N-b`, `N-c` and `N-d` to be
refuted, and trusted `N-d` least, then `N-e`. All five came out as expected,
four of them thinly.** `N-a` and `N-e` hold by four cases each, with draws on
the other side of their lines.

### What the verdicts say

**1. A small audit buys little on top of the escalations.**

| audited decisions | the median | share of the gap |
|---|---|---|
| 10 | 814 | nothing |
| 50 | 818 | 14% |
| 100 | 826 | 41% |
| 251 | 833 | 66% |

At ten, two of the five orders are the escalations' own by every count the
record keeps (§*Two orders are the escalations' own*, below). So closing half
the gap takes between 50 and 251 audited decisions (`N-b` refuted, `N-e`
holds), and at the medians between 100 and 251.

**2. Most of what the audit buys is `T3_ENGINEERING`. [Read after the
verdicts]** The orders were set beside the escalations alone class by class. At
251 the five orders gain 14 to 21 test cases, and 13 to 19 of them in
`T3_ENGINEERING` alone:

| draw at 251 | cases gained | `T3_ENGINEERING` | other rare queues | the four common queues |
|---|---|---|---|---|
| 0 | 14 | 15 | 0 | −1 |
| 1 | 21 | 19 | −5 | +7 |
| 2 | 19 | 17 | 0 | +2 |
| 3 | 18 | 13 | −3 | +8 |
| 4 | 19 | 18 | −2 | +3 |

Each other rare queue moves by at most four either way. The whole train half's
29 cases split into 18 in `T3_ENGINEERING`, nothing net in the other three rare
queues, −1 and +1, and 11 in the four common ones. So at 251 the audit has bought nearly all
of the `T3_ENGINEERING` the whole train half buys, and a median 3 of its 11 in
the common queues.

**3. `T3_ENGINEERING` is all or nothing, and it is the tickets, not their
number.** Across all 40 orders, 35 are right on 2 or fewer of the 57 cases or on
13 or more. The other five are at 5, 9 or 10, all at 100 or 251 decisions. The
draws' make-up, counted in §1 of the plan before signature, does not order them:
- draw 4 holds one `T3_ENGINEERING` ticket among its first ten decisions, and
  both of its orders at ten are right on 13;
- draw 1 holds three among its first fifty, and both of its orders at fifty are
  right on none.

| audited decisions | the audited sets | the audit alone |
|---|---|---|
| 10 | 0, 0, 1, 0, 13 | 0, 0, 0, 1, 13 |
| 50 | 19, 0, 2, 1, 13 | 14, 0, 0, 2, 13 |
| 100 | 14, 13, 5, 9, 14 | 14, 13, 5, 10, 13 |
| 251 | 15, 19, 17, 13, 18 | 19, 18, 17, 10, 18 |

So `N-c`'s line, 9, falls between the two clusters. At fifty decisions three
draws of five are below it; at 100 and 251 the median is above it, at 13 and
17.

**4. Over the space, the escalations alone were the high figure.** At ten
decisions the audited sets' median is the escalations' own 73,020. From fifty on
it falls below:

| audited decisions | the median over the space |
|---|---|
| 50 | 57,890 |
| 100 | 58,250 |
| 251 | 62,905 |
| the whole train half | 81,089 |

The plan's §6.2 named that risk: one search, whose space score is the top of the
escalation orders' own spread.

**[Read after the verdicts]** As in `FINDINGS_ESCALATIONS.md`, the space follows
`SECURITY_INCIDENT` at the top. Of the eight cells of arm and budget, seven
have, as their highest share of the space, an order among those right on the
most of the test split's ten `SECURITY_INCIDENT` cases. At 251 the audited sets
tie three orders at 3. The exception is the audit alone at 251, where the second
highest order holds the most, five. At fifty, a draw holds at most one
`SECURITY_INCIDENT` ticket.

**5. Alone, the decisions are the worst labels of the three on the test split.**

| labels | the audit alone | random escalations | random arrivals |
|---|---|---|---|
| 10 | **530** | 559 | 532 |
| 50 | **694** | 737 | 717 |
| 100 | **766** | 794 | 791 |
| 251 | **795** | 816 | 820 |

These are the medians of five draws each. At 10 the audit alone is two cases
below the arrivals. The decisions are 69% of the train half, and the arrivals
sit between them and the escalations at 10, 50 and 100. Over the space the audit
alone's medians are 0.3214, 0.3958, 0.4174 and 0.4819: above the escalations'
at 10, 50 and 251, and below the arrivals' at every budget.

**So a reviewer who answers the escalations and audits a few decisions at random
buys little more than the escalations buy.** Half the gap takes more than fifty
audited decisions, and what the audit buys is mostly the one queue the
escalations never teach. Where tickets arrive, a decision is worth less per
label than an escalation.

---

## The readings of `N-f`

### Every set at every budget, on the test split

Right decisions of 995, draws in draw order.

| decisions | audited sets: draws | median | share of the gap | the audit alone: draws | median |
|---|---|---|---|---|---|
| 10 | 814, 814, 799, 814, 828 | **814** | 0.00 | 596, 488, 694, 515, 530 | **530** |
| 50 | 824, 813, 806, 818, 827 | **818** | 0.14 | 559, 694, 723, 673, 738 | **694** |
| 100 | 823, 829, 812, 826, 826 | **826** | 0.41 | 742, 766, 710, 785, 820 | **766** |
| 251 | 828, 835, 833, 832, 833 | **833** | 0.66 | 795, 799, 827, 724, 790 | **795** |

**All 689, the whole train half: 843.**

### Every set at every budget, over the space

Right points of 134,400.

| decisions | audited sets: draws | median | the audit alone: draws | median |
|---|---|---|---|---|
| 10 | 73,020, 74,694, 53,220, 73,020, 55,210 | **73,020** | 47,245, 78,100, 39,120, 43,190, 37,485 | **43,190** |
| 50 | 79,420, 66,020, 57,230, 57,890, 55,204 | **57,890** | 47,380, 72,590, 53,935, 53,200, 42,750 | **53,200** |
| 100 | 71,320, 68,620, 54,930, 58,250, 55,124 | **58,250** | 60,300, 80,055, 54,925, 56,100, 52,930 | **56,100** |
| 251 | 63,970, 62,905, 75,535, 59,385, 62,689 | **62,905** | 75,910, 64,770, 75,645, 57,320, 59,980 | **64,770** |

**All 689: 81,089.** Arrival order is 42,310.

### What the escalations add to the audit

Paired by draw, the audited set less the audit alone, on the test split:

| decisions | draws 0 to 4 |
|---|---|
| 10 | 218, 326, 105, 299, 298 |
| 50 | 265, 119, 83, 145, 89 |
| 100 | 81, 63, 102, 41, 6 |
| 251 | 33, 36, 6, 108, 43 |

### The rare classes

Right decisions on the test split's four rare queues. `T3_ENGINEERING` is in
the third reading above. For the audited sets:

| queue | test cases | escalations alone | audited sets, every budget | whole train half |
|---|---|---|---|---|
| `ACCOUNT_MANAGER` | 55 | 20 | 16 to 20 | 19 |
| `SECURITY_INCIDENT` | 10 | 4 | 0 to 8 | 5 |
| `ONCALL_ESCALATION` | 3 | 0 | 0 or 1 | 0 |

The audit alone ranges wider:
- `ACCOUNT_MANAGER`: 0 to 20 of 55, and 0 in most of its orders;
- `SECURITY_INCIDENT`: 0 to 10, all ten in one order at ten decisions;
- `ONCALL_ESCALATION`: 0 to 2.

Every order's count is in the record.

### The labelled sets' make-up

The audited decisions' make-up is §1's table of the plan, counted before
signature, and the record's counts agree with it. At every budget about half of
the audited decisions are ones rung 1 got wrong: 17 to 25 of fifty, and 114 to
123 of 251.

### Two orders are the escalations' own

**[Read after the verdicts]** At ten decisions, the audited sets of draws 0 and 3
give the escalations alone's 814 test cases and 73,020 points. They have the
same four rare-class counts, and they come from the same start, the
multi-start's random start 57. Draw 1's audited set gives 814 from that start
too, with 74,694 points. The record keeps each order's scores and not the order,
so whether they are one order is not recorded. As in `FINDINGS_ESCALATIONS.md`,
the same declared start lands different label sets on what looks like the same
order.

---

## What this does not settle

- **What a label costs, and who gives it.** The reviewer here is the truth. A
  real one errs (§11.1 of the plan).
- **The online loop.** The order is searched once, at the end, on the final
  base, and a deployed audit would arrive while it grows (§11.2).
- **Which tickets teach `T3_ENGINEERING`.** The record shows that the tickets
  matter and their number does not, and it does not say which. A reading of
  draw 4's one ticket at ten decisions, and of draw 1's three at fifty, would.
  **[NOTE 2026-10-19, later] Read POST-RUN**: six of the train half's 60 carry
  the class, the ones a single rule matches. *Which tickets teach
  `T3_ENGINEERING`*, below.
- **An audit aimed at the rare queues.** The engine decided only four queues,
  so a reviewer cannot aim at a rare queue by the system's decision. Another
  signal might, such as the margin between matching rules or a student's
  uncertainty, and none is tried (§11.4).
- **An audit of errors only.** That is rung 4's channel, and it is not compared
  here (§11.3).
- **Why the space follows `SECURITY_INCIDENT`.** Read after the verdicts, on ten
  test cases, here and in `FINDINGS_ESCALATIONS.md`. Neither record splits the
  space by the keyword.
- **One split.** Every row is read on split 0 (§11.5).

---

## Which tickets teach `T3_ENGINEERING` — POST-RUN

> **POST-RUN.** Asked for on 2026-10-19, after the stage.
> `spotcheck/readings.py` wrote its eight-clause expectation in its docstring
> and was committed before the first run, as `6379e0f` on its branch and
> `cde21d9` on `main`. It searched the stage's 40 orders and
> the two endpoints again, behind two gates:
> - every order is the record's, on both surfaces and on the four rare queues;
> - two routes agree on the class, by first match and by masks.
>
> Not a signed row; no verdict moves. The record is
> [`readings.json`](readings.json), which keeps every order.

**The class turns on one rule: `R0545`, *severity 1 on the api product*.** It
is a `T3_ENGINEERING` rule written at arrival 1,939 of 2,000, from a ticket of
the test split.
- **On the test split** it matches 13 cases, every one of them
  `T3_ENGINEERING`: 13 of the 20 that any order can reach.
- **In the train half** it matches seven tickets, all of them decisions rung 1
  got wrong, as `T2_TECHNICAL`. Six are `T3_ENGINEERING`: cases 58, 153, 181,
  1,053, 1,485 and 1,664. One is `ONCALL_ESCALATION`: case 1,432.

**An order learns the class when those 13 cases go to a `T3_ENGINEERING`
rule.** In 18 of the 22 orders that learn it, `R0545` decides all 13. In the
other four, among them the whole train half's, `R0489` sits above it and takes
three of the 13. That is a broader rule of the same queue, *severity 2 or less,
off hours, five or more recent tickets*. In two of the four `R0116`, another
rule of that queue, takes one more. Both get them right, so `R0545` decides 9
or 10. In 21 of the 22, all 13 cases are right.

**Where the class is not learnt, `R0545` sits below rules of other queues.**
In all 15 such orders it decides none of the 13. Its 13 cases come up 195 times
across those orders:
- 134 go to `T2_TECHNICAL` rules;
- 58 go to `ONCALL_ESCALATION` ones, 49 of them to `R0029`, *severity 1 without
  the keyword*, written at arrival 74;
- 3 go to another `T3_ENGINEERING` rule.

In the escalations alone's order, 560 of the 577 rules sit above it.

**Moved to the front, it makes every one of the 42 orders learn the class**,
right on 13 to 19 of the 57. It costs nothing on the test split, where it
matches no ticket of another queue. Each of the 15 orders that did not learn
the class gains 12 or 13 test cases.

**So the search leaves `R0545` where its start put it unless a label reaches
it.**
- **No order whose labels hold none of its six `T3_ENGINEERING` tickets learns
  the class**: 17 orders.
- **22 of the 25 orders that hold one do.** The other three hold the
  `ONCALL_ESCALATION` ticket 1,432 too: draw 3's audited set at 100, and its
  audit alone at 100 and at 251. In each, an `ONCALL_ESCALATION` rule placed
  above `R0545` takes four of its 13 cases.

**Which tickets teach it.**
- **The escalations hold none of the six.** So nothing in their labels lifts
  it, and the escalations alone are right on none of the 57.
- **Draw 4's one `T3_ENGINEERING` ticket** among its first ten decisions is case
  153, one of the six. Draw 1's three among its first fifty are not.
- **A draw holds one of the six** from ten decisions on in one draw of five,
  from fifty in two, from 100 in four and from 251 in all five.

So *the number of the class's tickets does not decide it*, in the third reading
above, comes to this: six of the train half's 60 `T3_ENGINEERING` tickets carry
the class, and the other 54 do not.

### The expectation, clause by clause

| clause | expected | read | verdict |
|---|---|---|---|
| E1 | the key rule decides at least 13 of the whole train half's 18 | 9 | **fails** |
| E2 | at least 13 in every order that learns the class | 13 in 18 of the 22; 9, 9, 9 and 10 in four | **fails** |
| E3 | none in every order that does not; two thirds or more of the cases it loses to `T2_TECHNICAL` | none in 15; 134 of the 192 it loses | holds |
| E4 | moved to the front, every order learns the class | 13 to 19 of 57 | holds |
| E5 | and every order that did not gains on the whole test split | +12 or +13 | holds |
| E6 | none of the escalations' three is matched by the key rule, and draw 4's one at ten is | none; it is | holds |
| E7 | none of draw 1's three at fifty is | none | holds |
| E8 | no order without one learns; four in five with one do | 0 of 17; 22 of 25 | holds |

**Six of eight held.** The two that failed bet that one rule decides the class's
cases alone. A second rule of the same queue shares them in four orders, and the
cases are right either way. The drafter trusted E5 least, and it held, because
`R0545` matches nothing on the test split but its own queue's tickets.

---

## Files

```
spotcheck/plan.py         the gate and the constants of §9; §1's material and the draws' make-up
spotcheck/selections.py   the 689 decisions, the nested draws, the two arms; no truth
spotcheck/gates.py        N-g1 to N-g4, blocking, run first
spotcheck/score.py        the stage: N-a to N-e, the readings of N-f
spotcheck/readings.py     POST-RUN: which tickets teach T3_ENGINEERING
results_spotcheck/score.json      the stage's figures, every set, its make-up, the endpoints, the gates
results_spotcheck/readings.json   the reading's figures and orders, behind two gates, and the expectation
tests/test_spotcheck.py           how the package counts — and no figure
tests/test_spotcheck_readings.py  how readings.py counts, and each clause at its edge
```

The instrument is `escalations/instrument.py`'s, called and not copied.
Reproducible, in this order:

```
python3 -m spotcheck.score --dry-run          # N-g1..N-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m spotcheck.score   # about fifteen minutes
PYTHONHASHSEED=0 python3 -m spotcheck.readings  # POST-RUN; about eleven minutes
```
