# What a reviewer's labels at the escalations buy the order — findings

Record opened on October 19, 2026, under [`PLAN_ESCALATIONS.md`](../PLAN_ESCALATIONS.md).
Sergi signed §0 on 2026-10-19, before any figure below existed, in a commit of
its own: *PLAN_ESCALATIONS.md signed by Sergi*. The stage's record,
[`score.json`](score.json), names that commit in its `_env` as `5dd9072`, its
hash on the branch it was made on. A rebase merge gives it a new hash on `main`
with the same tree, so it is named here by its subject. **This record owns every
figure in it.**

**The stage adjudicated the five signed rows on 2026-10-19: four hold and one is
refuted.**

- **Fifty labels at the escalations buy two thirds of the gain where tickets
  arrive.** On corpus test split 0, the five orders labelled with the truth of
  fifty escalations drawn at random are right on 703 to 799 of 995 cases, 737
  at the median. Arrival order is right on 519 and the full search on 843, so
  that is 67% of the gain (`J-a` holds). Every draw clears half of it.
- **There, an escalation is worth about what a random train case is worth.**
  The audit's five draws of fifty train cases give 717 at the median (`J-b`
  holds, *thin*). At 251 labels the escalations give 816 and the arrivals 820
  (`J-c` holds). Both differences lie inside the spread of the arrivals' own
  draws.
- **Labelling the most crowded escalations first buys almost nothing there.**
  The fifty escalations the most rules match give 523, four cases above arrival
  order (`J-d` refuted). 49 of them are `SELF_SERVICE_DEFLECT` or
  `BILLING_SPECIALIST` tickets in truth. Labelling the first fifty as they came
  gives 708.
- **Over the function, the escalations buy less than random arrivals at every
  budget.** At fifty labels their median is 0.3426 of the exhaustive space,
  against the arrivals' 0.3993 (`J-e` holds).
- **Labelling every escalation buys 91% of the gain on the test split, no more
  than 251 of them do.** All 316 give 814, the figure `PLAN_STUDENTS.md`
  published for the 286 whose proposal named a queue. They fall 29 test cases
  short of the full search, and 18 short in one class alone,
  `T3_ENGINEERING`, which the loop almost never asked about. Reported.

> **PROVENANCE: PRE-REGISTERED.** `J-a` to `J-e` were signed before any of their
> figures existed. **`J-f` is reported, not adjudicated**, and every figure in it
> is computed here for the first time, except the 286 named escalations' figure,
> which `PLAN_STUDENTS.md` published. **Three readings below were chosen after
> the verdicts, and each says so where it is made**: the overlap of the draws at
> 251 labels, the space shares beside one class, and the rare classes beside the
> audit's record. They read figures this record or a published one already
> holds, and none moves a verdict. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m escalations.score`, on 2026-10-19, from the signing
commit with a clean tree: 707 s, about a third of it the suite inside the first
check, and zero API calls. The record is [`score.json`](score.json). Its `_env`
carries `git_dirty: false` and `code_dirty: false`.

**The blocking checks passed again before any order was searched on a set of
escalations.**

- **`J-g1`.**
  - The suite is green, 1,854 tests.
  - The material of §1 recomputes: 316 escalations, 300 on a CONFLICT and 16 on
    an impasse, carried by 294 distinct tickets.
  - Arrival order reproduces 519 and 42,310.
  - The instrument reproduces the audit record's split-0 rows to its four
    decimals: 0.8472 and 0.6033 with all 1,005 train cases, and each of its five
    draws at 10 labels and at 50.
  - On the 286 named escalations it reproduces `PLAN_STUDENTS.md`'s 814 and
    73,420.
- **`J-g2`.** The 29 labelled sets, built twice, are equal. Each has its size
  and lies inside the 316, and `selections.py` names no truth.
- **`J-g3`.** Every labelled case is in the train half, and no test case shares a
  ticket with one.
- **`J-g4`.** Signed.

**Notation.** *Test* is corpus test split 0, 995 cases; *space* is the 134,400
combinations. Every count is of decisions right against the truth. *Arrival
order* is rung 1's 577 rules first-match by birth on rung 3's `puro` pool, right
on 519 and 42,310. *The gain* is what the search adds to it with the truth of all
1,005 train cases: from 519 to 843 on test, 324 cases. A *share of the gain* is a
count less 519, over 324.

The sets:
- *random escalations at `k`* are five seeded draws of `k` of the 316;
- *random arrivals at `k`* are the audit record's five draws of `k` train cases
  on split 0, read as published and never re-drawn;
- *arrival* is the first `k` escalations as they came;
- *crowded* is the `k` escalations the most rules match.

---

## The five rows

| row | statistic | value | line | verdict |
|---|---|---|---|---|
| `J-a` | test: random escalations at 50, the median of five orders | **737** (0.7407) | ≥ 681 | **holds** |
| `J-b` | the same, against random arrivals at 50 | **737** | > 717 | **holds, thin** |
| `J-c` | test: random escalations at 251, against random arrivals at 251 | **816** (0.8201) | < 820 | **holds** |
| `J-d` | test: the 50 most crowded escalations, against `J-a`'s median | **523** (0.5256) | > 737 | **refuted** |
| `J-e` | space: random escalations at 50, the median share | **0.3426** | < 0.3993 | **holds** |

The draws each row is read on:

| row | the row's side | the comparator's side |
|---|---|---|
| `J-a`, `J-b` | 703, 730, 737, 775, 799 | 574, 708, 717, 734, 769 |
| `J-c` | 810, 814, 816, 817, 817 | 768, 802, 820, 825, 829 |
| `J-d` | 523 | `J-a`'s five, 703 to 799 |
| `J-e` | 0.3233, 0.3317, 0.3426, 0.3835, 0.4552 | 0.3569, 0.3614, 0.3993, 0.4513, 0.6044 |

A verdict is *thin* when its line lies inside the range of the draws it is read
on: for `J-a`, its five orders; for `J-d`, the five random ones. For `J-b`,
`J-c` and `J-e` it is thin when each side's median lies inside the other side's
range. **Only `J-b`'s is.** In the others:
- `J-a`'s line, 681, is below all five of its draws;
- `J-c`'s comparator median, 820, is above all five escalation draws;
- `J-e`'s median, 0.3426, is below all five of the arrivals' draws.

**The drafter expected `J-a`, `J-c`, `J-d` and `J-e` to hold and `J-b` to be
refuted, and trusted `J-d` least, then `J-b`. Three of five came out as
expected. The two that did not are the two trusted least: `J-b` held, thinly,
and `J-d` was refuted far from its line.**

### What the verdicts say

**1. Fifty labels at the escalations buy two thirds of the gain where tickets
arrive.** A reviewer who labels fifty escalations drawn at random hands the
search the truth of 50 of the train half's 1,005 cases. The order it finds is
right on 737 test cases at the median, 218 of the 324 the full search gains over
arrival. Every one of the five draws clears half the gain. At 100 labels the
median is 794, 85% of it.

**2. There, an escalation is worth about what a random train case is worth, and
five draws cannot tell them apart.** `J-b` and `J-c` both held, which §0 read as
a crossover: the escalations the better place to buy a few labels and the worse
place to buy many. The differences are 20 test cases at 50 labels and 4 at 251.
Both lie inside the spread of the comparator's own draws, which run from 574 to
769 at 50 and from 768 to 829 at 251. `J-b` is labelled thin and `J-c` is not.

**[Read after the verdicts]** Why one is thin and the other is not is a
property of the draws, not of the result. At 251 labels of 316, any two draws of escalations share 195
to 204 cases, so their five orders cannot spread as five draws of 251 from 1,005
train cases do: they run from 810 to 817. §0's label asks each median to lie
inside the other's range, and a side whose draws barely differ almost never
contains the other's median. At 10 and 100 labels, reported, the escalations
give 559 against 532 and 794 against 791. **So the crossover is in the medians,
and the draws do not establish it.**

**3. Which first: neither rule that reads no truth beats a random draw on the
arrivals, and the most crowded is the worse.** The fifty escalations the most
rules match are two queues' tickets: 28 are `SELF_SERVICE_DEFLECT` in truth, 21
`BILLING_SPECIALIST` and one `T2_TECHNICAL`. Each random draw holds 15 to 18
`T2_TECHNICAL` tickets. Labelled first, those fifty leave the order four cases
above arrival order on the test split. The drafter's reason for `J-d` was that
the tickets the most rules match crowd the common regions the test split is made
of. That was wrong: they crowd two of them.

Labelling as tickets come does better than that, and still worse than a random
draw. The first fifty give 708, below four of the five random draws. They hold
all sixteen impasses, which all came early in the run. The first ten are nine
impasses and one CONFLICT, and give 451, below arrival order itself. **On the
test split both rules are below the random median at every budget**: arrival at
451, 708, 759 and 809, crowded at 512, 523, 720 and 800, against 559, 737, 794
and 816.

**Over the space the most crowded rank the other way.** Among the sets of
escalations at their budget, they give the highest share of the space at 50
labels, 0.4599, and at 251, 0.5555. The second is above the order on all 316,
0.5433. So the rule that buys almost nothing where tickets arrive buys the most
over the function. The two surfaces disagree about which order is better
elsewhere too ([`results3/FINDINGS_ORDERS.md`](../results3/FINDINGS_ORDERS.md)),
and here they disagree about which labels to buy.

**4. Over the function, the escalations buy less than random arrivals at every
budget.** At fifty labels their median share of the space is 0.3426, below all
five of the arrivals' draws, whose median is 0.3993 (`J-e` holds). The other
budgets, reported:

| labels | escalations | arrivals |
|---|---|---|
| 10 | 0.2596 | 0.3400 |
| 100 | 0.4223 | 0.4361 |
| 251 | 0.4278 | 0.5302 |

At ten labels all five orders labelled at escalations are below arrival order
over the space, 0.3148. Four of the five arrivals' draws are above it.

So the comparison does not carry across surfaces: ahead on the arrivals at fifty
labels, thinly, and behind over the function. The drafter had bet that it would
carry, by expecting `J-b` refuted beside `J-e` holding. `IDEAS.md`'s standing
note says such arguments lose, and this one lost on `J-b`, thinly.

**[Read after the verdicts]** Over the space the order follows one class at the
top. At 50, 100 and 251 labels, one set's order is right on the most of the test
split's ten `SECURITY_INCIDENT` cases, and that set has the highest share of the
space at its budget:

| labels | set | `SECURITY_INCIDENT` right | space |
|---|---|---|---|
| 50 | crowded | 8 of 10 | 0.4599 |
| 100 | random, draw 1 | 8 of 10 | 0.5304 |
| 251 | crowded | 6 of 10 | 0.5555 |

At 10 labels it does not. That class's tickets carry the security keyword. The
keyword is on half the space and 3% of arrivals, and it is what the drafter's
reason for `J-e` named: no escalation is `SECURITY_INCIDENT` in truth. The
record does not split the space by the keyword, so this is a pattern on ten test
cases, not a measurement over the space.

**5. Labelling every escalation buys 91% of the gain on the test split, and most
of the shortfall is one class the loop almost never asked about.** The order on
all 316 is right on 814 test cases, the figure the 286 escalations whose
proposal named a queue gave `PLAN_STUDENTS.md`. Over the space it is right on
73,020 points, 400 fewer than those 286. So labelling the thirty whose proposal
failed leaves the count where tickets arrive where it was, and costs 400 points
over the function.

**[Read after the verdicts]** The order on all 316 is 29 test cases short of
the full search's 843, and 18 short in `T3_ENGINEERING` alone:
- no order labelled at escalations is right on more than 2 of the test split's
  57 `T3_ENGINEERING` cases, and the one on all 316 is right on none;
- the full search is right on 18, by the audit's own per-class count, so every
  one of those 18 is a case the order on all 316 gets wrong;
- the escalations hold 3 `T3_ENGINEERING` tickets of 316.

---

## The readings of `J-f`

### Every selection at every budget, on the test split

Each cell is right decisions of 995, with its share of the gain where it helps.
Random draws are listed in draw order, 0 to 4.

| labels | random escalations: draws | median | share | random arrivals: draws | median | share | arrival | crowded |
|---|---|---|---|---|---|---|---|---|
| 10 | 559, 518, 577, 590, 435 | **559** | 0.12 | 563, 498, 659, 532, 491 | **532** | 0.04 | 451 (−0.21) | 512 (−0.02) |
| 50 | 799, 703, 730, 775, 737 | **737** | 0.67 | 717, 769, 574, 708, 734 | **717** | 0.61 | 708 (0.58) | 523 (0.01) |
| 100 | 799, 775, 794, 804, 794 | **794** | 0.85 | 791, 794, 775, 751, 804 | **791** | 0.84 | 759 (0.74) | 720 (0.62) |
| 251 | 810, 817, 817, 814, 816 | **816** | 0.92 | 825, 829, 820, 768, 802 | **820** | 0.93 | 809 (0.90) | 800 (0.87) |

**All 316: 814, 0.91 of the gain.** At ten labels two of the five escalation
orders, and two of the arrivals', are below arrival order.

### Every selection at every budget, over the space

Each cell is a share of the 134,400 points. Arrival order is 0.3148.

| labels | random escalations: draws | median | random arrivals: draws | median | arrival | crowded |
|---|---|---|---|---|---|---|
| 10 | 0.2608, 0.2414, 0.2682, 0.2596, 0.2122 | **0.2596** | 0.3328, 0.2660, 0.3400, 0.5135, 0.3819 | **0.3400** | 0.2373 | 0.2323 |
| 50 | 0.3426, 0.4552, 0.3835, 0.3317, 0.3233 | **0.3426** | 0.3569, 0.3993, 0.3614, 0.6044, 0.4513 | **0.3993** | 0.3925 | 0.4599 |
| 100 | 0.4468, 0.5304, 0.3833, 0.4223, 0.4079 | **0.4223** | 0.4361, 0.4007, 0.5650, 0.5231, 0.4270 | **0.4361** | 0.3907 | 0.3706 |
| 251 | 0.4017, 0.4188, 0.4615, 0.5433, 0.4278 | **0.4278** | 0.5616, 0.5302, 0.5375, 0.3593, 0.5123 | **0.5302** | 0.4236 | 0.5555 |

**All 316: 73,020 points, 0.5433.** The full search is 0.6033.

**Two sets give the same two scores.** The order on draw 3 of 251 and the order
on all 316 are both right on 814 test cases and 73,020 points. Both came from
the multi-start's random start 57. The record keeps each order's scores and not
the order, so whether they are one order is not recorded.

**Every order fits nearly all of its labels.** At fifty, 49 or 50 of 50; on all
316, 304. So what separates the sets is what their labels say about the rest,
not how well the search meets them.

### The labelled sets' make-up

At fifty labels, with all 316 beside them:

| set | CONFLICT | impasse | keyword | `SELF_SERVICE_DEFLECT` | `T2_TECHNICAL` | `T1_GENERAL` | `BILLING_SPECIALIST` | `ACCOUNT_MANAGER` | `T3_ENGINEERING` |
|---|---|---|---|---|---|---|---|---|---|
| random, draw 0 | 48 | 2 | 1 | 12 | 18 | 12 | 6 | 1 | 1 |
| random, draw 1 | 48 | 2 | 2 | 20 | 17 | 9 | 4 | 0 | 0 |
| random, draw 2 | 50 | 0 | 0 | 24 | 15 | 10 | 1 | 0 | 0 |
| random, draw 3 | 48 | 2 | 2 | 20 | 16 | 4 | 7 | 3 | 0 |
| random, draw 4 | 48 | 2 | 1 | 16 | 15 | 13 | 5 | 0 | 1 |
| arrival | 34 | 16 | 2 | 19 | 17 | 9 | 3 | 2 | 0 |
| crowded | 49 | 1 | 1 | 28 | 1 | 0 | 21 | 0 | 0 |
| all 316 | 300 | 16 | 8 | 114 | 99 | 53 | 35 | 12 | 3 |

**The crowded sets are skewed at every budget**:
- at 10, 5 `SELF_SERVICE_DEFLECT` and 5 `BILLING_SPECIALIST`;
- at 100, 62 and 24 of those two queues, and 13 `T2_TECHNICAL`;
- at 251, 113 of the 114 `SELF_SERVICE_DEFLECT` escalations, all 35
  `BILLING_SPECIALIST` ones, and all 8 keyword tickets.

No set holds a `SECURITY_INCIDENT` or `ONCALL_ESCALATION` ticket, because no
escalation is one. Every set's make-up at every budget is in the record.

### The rare classes

Right decisions on the test split. The orders labelled at escalations are the
29 this stage searched. **[Read after the verdicts]** The last three columns
come from other records, which published them:
- arrival order, from
  [`results_students/score.json`](../results_students/score.json);
- the full search and the most any order can reach, from the audit's per-class
  count on split 0 in
  [`results3/budget_and_balance_ls.json`](../results3/budget_and_balance_ls.json).

| class | test cases | orders labelled at escalations | on all 316 | arrival order | full search | any order can reach |
|---|---|---|---|---|---|---|
| `SECURITY_INCIDENT` | 10 | 0 to 8 | 4 | 3 | 5 | 10 |
| `ACCOUNT_MANAGER` | 55 | 0 to 21 | 20 | 0 | 19 | 21 |
| `T3_ENGINEERING` | 57 | 0 to 2 | 0 | 0 | 18 | 20 |
| `ONCALL_ESCALATION` | 3 | 0 to 2 | 0 | 0 | 0 | 3 |

Two of these classes the escalations do teach:
- **`ACCOUNT_MANAGER`.** The 12 escalations of that queue buy more of it than
  the full search does. The order on all 316 is right on 20 of the 21 any order
  can reach, and the full search on 19.
- **`SECURITY_INCIDENT`.** It is taught without a ticket of its own: up to 8 of
  10, by the crowded fifty and by draw 1 of 100.

**`T3_ENGINEERING` is what they never teach.** Its 3 tickets among the 316 leave
it at 2 or fewer of 57, where the full search reaches 18.

**`ONCALL_ESCALATION`**: one order, draw 4 of 10, is right on 2 of its 3 test
cases. That order is the worst of all 29 on both surfaces, 435 and 0.2122.

---

## What this does not settle

- **What a label costs, and who gives it.** The reviewer here is the truth. A
  real one errs, and a reviewer's error rate would need its own model (§11.1 of
  the plan).
- **The online loop.** A deployed reviewer's labels would arrive while the base
  grows, and the order would be searched again as they did. Here the order is
  searched once, at the end, on the final base. `crowded` counts the final
  base's rules too (§6.2 and §11.2).
- **Whether the escalations are worth more than random arrivals at a small
  budget.** At 10 and 50 labels their median is ahead, and at 50 the label is
  thin. Five draws on one split cannot say. The audit's curve has five splits,
  and this plan read one.
- **Why the space follows `SECURITY_INCIDENT`.** Read after the verdicts on ten
  test cases. The record does not split the space by the keyword.
- **Other rules for which first.** A student's uncertainty, or the proposer's
  answer disagreeing with the rules' decision, would read more than the rules,
  and neither is tried (§11.5). Nor is a rule that spreads the labels across
  queues, which is what the crowded rule failed to do.
- **Other loops' escalations.** `PLAN_REUSE.md`'s are coverage impasses on rung
  2's engine. Its bases are small and decided by subsumption and edges, not by a
  searched order, so a plan on them would need another instrument (§11.3).
- **Rung 4's channel.** It labels the system's decisions, and mostly its errors.
  It is not compared here (§11.4).

---

## Files

```
escalations/plan.py         the gate and the constants of §9; §1's material and §0's lines
escalations/selections.py   the 316 escalations and the three rules that choose; no truth
escalations/instrument.py   the audit's label-budget search, on a given labelled set
escalations/gates.py        J-g1 to J-g4, blocking, run first
escalations/score.py        the stage: J-a to J-e, the readings of J-f
results_escalations/score.json   the stage's figures, every selection and its make-up, the gates
tests/test_escalations.py        how the package counts — and no figure
```

Reproducible, in this order:

```
python3 -m escalations.score --dry-run          # J-g1..J-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m escalations.score   # about twelve minutes
```
