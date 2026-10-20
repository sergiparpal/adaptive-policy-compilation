# What the rules no label reaches hold, and what deferring them buys — findings

Record opened on October 20, 2026, under [`PLAN_UNREACHED.md`](../PLAN_UNREACHED.md).
The plan, its package, the signature, the record and these findings reached
`main` in pull request #150. Sergi signed §0 on 2026-10-20, before any figure
below existed, in a commit of its own: `e5e844c` on `main`.

The stage's record, [`score.json`](score.json), names in its `_env` the commit
it was written from: `eeee4bc`, the signing commit as it was made and pushed,
with a clean tree. The rebase merge of #150 gave it `e5e844c` on `main`. The two
have the same subject, the same tree and the same `git patch-id --stable`, and
the GitHub API names #150 behind `e5e844c`. The code digest the `_env` records,
`f2942939dd6c99a6`, is the one `main` computes after the merge.

**This record owns every figure in it.**

**A POST-RUN reading was added on 2026-10-21**:
[`keyword_half.json`](keyword_half.json), by `unreached/keyword_half.py`, in its
own section below. Its `_env` names `9da087f`, the commit that wrote its
expectation, as it was made. **That commit was never pushed**: the branch was
rebased onto `main` after pull request #151 merged, and the commit is `e0c8131`
there. The two have the same tree, the same subject and the same `git patch-id
--stable`. The code digest the `_env` records, `d96905fc8bba0313`, is the one
the branch's tip computes. It moves no verdict. It corrects two sentences of
the curve's reading, with dated errata in place.

**The stage adjudicated the five signed rows on 2026-10-20: two hold and three
are refuted, and two are thin.**

- **Where tickets arrive, `R0545` was alone.** The escalations leave 25 rules
  unreached, 22 distinct. Moved alone to the front of the escalations' order,
  `R0545` gains 13 test cases, 12 of them away from its birth ticket. None of
  the other 21 gains away from its birth ticket (`Z-a` refuted), so together
  they hold nothing of the 29 cases between the escalations' order and the whole
  train half's (`Z-b` refuted). Twelve of them change nothing there and nine
  lose.
- **None of the 25 decides a test case in that order.** So moving all of them
  below every rule a label reaches leaves it at 814 of 995 (`Z-d` refuted,
  *thin*). The coin's placements of the same rules run from 798 to 827.
- **Over the function the stake is one rule.** Moved to the front, `R0019`,
  *keyword and severity 1* to `SECURITY_INCIDENT`, gains 5,900 of the 134,400
  points. Every other distinct rule loses or changes nothing, `R0545` among
  them at −820, so the sum is `R0019`'s (`Z-c` holds, on one rule).
- **Deferring the 25 gains 1,560 points over the space**, 74,580 against
  73,020, and the coin's placements run from 65,900 to 77,300 (`Z-e` holds,
  *thin*).
- **Under full supervision there is nothing to move.** The whole train half
  leaves 5 rules unreached, none of them decides a test case, and the back move
  changes neither of its figures. No placement of the coin beats its order on
  either surface. Reported.
- **Along the label curve, deferring is no rule to adopt.** On the optimizer
  audit's twenty orders of random arrivals the back move changes the test count
  by −32 to +9 and the space count by −11,500 to +5,185, and it changes nothing
  in nine of them. Reported.

> **PROVENANCE: PRE-REGISTERED.** `Z-a` to `Z-e` were signed before any of their
> figures existed. **`Z-f` is reported, not adjudicated**, and every figure in it
> is computed here for the first time, except the endpoints and `R0545`'s move
> on the test split, which `Z-g1` reproduced from their records. **One reading
> below was chosen after the verdicts, and it says so where it is made**: the
> rare classes the back move moves along the curve. It reads figures this record
> already holds, and it moves no verdict. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m unreached.score`, on 2026-10-20, from the signing
commit with a clean tree: 645 s, about a third of it the suite inside the first
check, and zero API calls. The record is [`score.json`](score.json). Its `_env`
carries `git_dirty: false` and `code_dirty: false`.

**The blocking checks passed again before any rule was moved.**

- **`Z-g1`.**
  - The suite is green, 1,930 tests.
  - §1's material recomputes: the counts, the table of the 25, the copies and
    the curve's reach.
  - Arrival order reproduces 519 and 42,310.
  - The records hold the endpoints and their starts, and the instrument
    reproduces them:
    - 814, 73,020 and 0, 20, 4 and 0 by rare class with all 316 escalations,
      from `aleatorio 57`;
    - 843, 81,089, 0.8472, 0.6033 and 18, 19, 5 and 0 with all 1,005 train
      cases, from `aleatorio 13`.
  - Both orders are the ones `results_spotcheck/readings.json` kept, and
    `R0545` at the front of the escalations' order gives the count that record
    published.
  - Each of the optimizer audit's twenty draws gives the record's test and space
    shares, to four decimals, and its start.
- **`Z-g2`.** `unreached/moves.py` names no truth, in a name or a string. On the
  toy order the three moves are the plan's permutations.
- **`Z-g3`.** Every labelled case is in the train half, and no test case shares
  a ticket with one.
- **`Z-g4`.** Signed.

The stage refuses to write if a front move's two routes on the test split
disagree, by first match case by case and by masks. They agreed on every rule of
both endpoints and of the curve.

**Notation.** *Test* is corpus test split 0, 995 cases; *space* is the 134,400
combinations. Every count is of decisions right against the truth, `puro` pool.

- **The endpoints.** *The escalations' order* is right on 814 and 73,020. *The
  whole train half's* is right on 843 and 81,089.
- ***The gap*** is the 29 test cases between them, and the 8,069 points.
- **A rule's place** is the number of rules above it in an order.
- **A front move** is one rule moved alone to the front. Its gain on the test
  split splits into its *birth ticket*, the test cases on the ticket it was
  written at, and *away*, the rest.
- **The back move** puts every unreached rule below every reached one, each
  group in the order's own order. **The coin** is 100 seeded placements of the
  same rules among the reached.

---

## The five rows

| row | statistic | value | line | verdict |
|---|---|---|---|---|
| `Z-a` | test: of the 21 other distinct rules no escalation reaches, those whose front move gains away from its birth ticket | **0** | ≥ 1 | **refuted** |
| `Z-b` | test: their front moves' gains away from the birth ticket, a loss as zero, summed | **0** | ≥ 15 | **refuted** |
| `Z-c` | space: the 22 distinct rules' front moves' gains, a loss as zero, summed | **5,900** | ≥ 4,035 | **holds** |
| `Z-d` | test: the escalations' order after the back move | **814** (0.8181) | > 814 | **refuted, thin** |
| `Z-e` | space: the same order | **74,580** (0.5549) | > 73,020 | **holds, thin** |

`Z-d` and `Z-e` are *thin* when their statistic lies inside the range of the
coin's 100 placements on the same surface. **Both are**:
- 814 lies inside 798 to 827;
- 74,580 lies inside 65,900 to 77,300.

`Z-a` to `Z-c` carry no label.

**The drafter expected `Z-a` and `Z-c` to hold and `Z-b`, `Z-d` and `Z-e` to be
refuted, and trusted `Z-c` least, then `Z-d`. Three of five came out as
expected: `Z-a` was refuted and `Z-e` held.** `Z-c` holds on one rule, the one
the drafter named, and `Z-d` is refuted by a tie, the way the drafter said it
might be.

### What the verdicts say

**1. Where tickets arrive, `R0545` was alone.** Of the 22 distinct rules no
escalation reaches, it is the only one whose front move gains on the test split:

| front move, test split | distinct rules | away from the birth ticket |
|---|---|---|
| gains | 1: `R0545`, +13 | 1: `R0545`, +12 |
| changes nothing | 9 | 12 |
| loses | 12 | 9 |

The two other `T3_ENGINEERING` rules do not pay. `R0267`'s two test cases are
wrong whichever rule decides them. `R0570`'s three are right in the order and
wrong under it. `R0019`'s two are right either way.

**2. None of the 25 decides a test case where the escalations' order put
them.** Their places run from 35 to 569 rules down. On every test case one of
them matches, a reached rule above it decides. So the back move cannot change
the test split, and it does not: 814 before and after. The order's own count is
the coin's median: 49 placements are below 814, 47 equal it and 4 are above.

**3. On their own birth tickets, the rules mostly lose.** Every one of the 25
was written at a test-split ticket, from the proposer's answer there. Moved to
the front, a rule decides that ticket with that answer:

| on the birth ticket | distinct rules |
|---|---|
| the move gains | 1: `R0545` |
| no change | 10 |
| the move loses | 11 |

So on those tickets the escalations' order, labelled elsewhere, is right more
often than the answer each rule was written from.

**4. Over the function, one rule holds the stake.**

| rule | what it says | place | front move over the space |
|---|---|---|---|
| `R0019` | keyword and severity 1 → `SECURITY_INCIDENT` | 55 | **+5,900** |
| `R0287` and its three copies | off hours and severity 1 → `ONCALL_ESCALATION` | 68 to 569 | −3,750 |
| `R0016` | three conditions → `T2_TECHNICAL` | 135 | −2,520 |
| `R0448` | three conditions → `T2_TECHNICAL` | 416 | −2,340 |
| `R0545` | api and severity 1 → `T3_ENGINEERING` | 560 | −820 |

Thirteen more distinct rules lose between 6 and 1,315 points, and four change
nothing. `R0019` sits 55 rules down and decides none of its two test cases, both
of which the order gets right. Over the space it would win 5,900 points the
order gives elsewhere. **`Z-c` holds on that one rule**, a form of the rule of
thumb about the security keyword that the declared edges carried in
`FINDINGS_EDGES.md`.

**5. The back move over the space is a placement the coin also reaches.** It
gains 1,560 points over the order's 73,020: 75 placements are below 74,580, 20
equal it and 5 are above. The order's own placement sits in the middle of the
coin: 51 below, 1 equal, 48 above. The record holds the move and not its parts,
so which rules the 1,560 comes from is not read.

**6. Under full supervision there is nothing to move.** The whole train half
leaves 5 rules unreached, and none of them decides a test case in its order. The
back move leaves 843 and 81,089 as they were. On the test split 89 of the coin's
placements equal 843 and none is above it; over the space 74 equal 81,089 and
none is above.

**So the rules no label reaches hold nothing more where tickets arrive than the
one rule already found, and over the function they hold one rule's worth.**
What the escalations leave on the test split, beyond `R0545`'s 13 cases, is not
in the rules they leave unreached. Deferring those rules is worth nothing on the
arrivals, and over the space no more than a reshuffle of them.

---

## The readings of `Z-f`

### Every rule no escalation reaches

In the escalations' order. *Cases* is the test cases the rule matches, *birth*
those on its birth ticket, *decided* those it decides in the order. *Right* is
right decisions on its cases in the order and with the rule at the front. The
four copies are marked.

| rule | queue | place | cases | birth | decided | right: order · moved | gain on test | birth · away | gain over the space |
|---|---|---|---|---|---|---|---|---|---|
| `R0016` | `T2_TECHNICAL` | 135 | 10 | 1 | 0 | 4 · 4 | 0 | 0 · 0 | −2,520 |
| `R0019` | `SECURITY_INCIDENT` | 55 | 2 | 1 | 0 | 2 · 2 | 0 | 0 · 0 | **+5,900** |
| `R0027` | `T2_TECHNICAL` | 491 | 2 | 1 | 0 | 2 · 2 | 0 | 0 · 0 | 0 |
| `R0062` | `T1_GENERAL` | 407 | 1 | 1 | 0 | 1 · 1 | 0 | 0 · 0 | 0 |
| `R0080` | `SELF_SERVICE_DEFLECT` | 178 | 9 | 1 | 0 | 9 · 0 | −9 | −1 · −8 | −120 |
| `R0087` | `T1_GENERAL` | 86 | 1 | 1 | 0 | 0 · 0 | 0 | 0 · 0 | −540 |
| `R0114` | `T2_TECHNICAL` | 108 | 5 | 1 | 0 | 2 · 1 | −1 | 0 · −1 | −1,315 |
| `R0117` | `T1_GENERAL` | 269 | 3 | 1 | 0 | 3 · 0 | −3 | −1 · −2 | −20 |
| `R0150` | `T1_GENERAL` | 72 | 3 | 1 | 0 | 3 · 0 | −3 | −1 · −2 | −80 |
| `R0158` | `T2_TECHNICAL` | 145 | 1 | 1 | 0 | 1 · 0 | −1 | −1 · 0 | −1,165 |
| `R0211` | `T1_GENERAL` | 508 | 2 | 1 | 0 | 2 · 1 | −1 | −1 · 0 | −6 |
| `R0267` | `T3_ENGINEERING` | 290 | 2 | 1 | 0 | 0 · 0 | 0 | 0 · 0 | −660 |
| `R0287` | `ONCALL_ESCALATION` | 134 | 19 | 1 | 0 | 9 · 2 | −7 | −1 · −6 | −3,750 |
| `R0308` | `T2_TECHNICAL` | 377 | 3 | 1 | 0 | 3 · 1 | −2 | −1 · −1 | −950 |
| `R0351` | `SELF_SERVICE_DEFLECT` | 306 | 2 | 1 | 0 | 2 · 0 | −2 | −1 · −1 | −6 |
| `R0357` | `T2_TECHNICAL` | 566 | 6 | 1 | 0 | 6 · 2 | −4 | −1 · −3 | −320 |
| `R0361` | `T2_TECHNICAL` | 97 | 2 | 1 | 0 | 2 · 1 | −1 | −1 · 0 | −590 |
| `R0373` *(copy)* | `ONCALL_ESCALATION` | 281 | 19 | 1 | 0 | 9 · 2 | −7 | −1 · −6 | −3,750 |
| `R0448` | `T2_TECHNICAL` | 416 | 9 | 1 | 0 | 1 · 1 | 0 | 0 · 0 | −2,340 |
| `R0450` | `T2_TECHNICAL` | 157 | 2 | 1 | 0 | 2 · 2 | 0 | 0 · 0 | 0 |
| `R0459` | `T2_TECHNICAL` | 35 | 5 | 1 | 0 | 5 · 5 | 0 | 0 · 0 | 0 |
| `R0493` *(copy)* | `ONCALL_ESCALATION` | 569 | 19 | 1 | 0 | 9 · 2 | −7 | 0 · −7 | −3,750 |
| `R0506` *(copy)* | `ONCALL_ESCALATION` | 68 | 19 | 2 | 0 | 9 · 2 | −7 | 0 · −7 | −3,750 |
| `R0545` | `T3_ENGINEERING` | 560 | 13 | 1 | 0 | 0 · 13 | **+13** | +1 · +12 | −820 |
| `R0570` | `T3_ENGINEERING` | 500 | 3 | 1 | 0 | 3 · 0 | −3 | −1 · −2 | −970 |

The copies make one move. Their splits at the birth ticket differ, because each
was written at a different ticket; the rows count `R0287`'s.

### The whole train half's five

| rule | queue | place | cases | birth | decided | right: order · moved | gain on test | birth · away | gain over the space |
|---|---|---|---|---|---|---|---|---|---|
| `R0087` | `T1_GENERAL` | 370 | 1 | 1 | 0 | 0 · 0 | 0 | 0 · 0 | −435 |
| `R0117` | `T1_GENERAL` | 555 | 3 | 1 | 0 | 3 · 0 | −3 | −1 · −2 | −40 |
| `R0267` | `T3_ENGINEERING` | 120 | 2 | 1 | 0 | 0 · 0 | 0 | 0 · 0 | −660 |
| `R0351` | `SELF_SERVICE_DEFLECT` | 78 | 2 | 1 | 0 | 2 · 0 | −2 | −1 · −1 | −6 |
| `R0361` | `T2_TECHNICAL` | 493 | 2 | 1 | 0 | 2 · 1 | −1 | −1 · 0 | −355 |

No front move gains on either surface.

### The back move and the coin

| endpoint | surface | the order | after the back move | the coin: min · median · max | placements below · equal · above the order | the same, of the back move |
|---|---|---|---|---|---|---|
| escalations | test | 814 | 814 | 798 · 814 · 827 | 49 · 47 · 4 | 49 · 47 · 4 |
| escalations | space | 73,020 | **74,580** | 65,900 · 72,877.5 · 77,300 | 51 · 1 · 48 | 75 · 20 · 5 |
| whole train half | test | 843 | 843 | 838 · 843 · 843 | 11 · 89 · 0 | 11 · 89 · 0 |
| whole train half | space | 81,089 | 81,089 | 80,654 · 81,089 · 81,089 | 26 · 74 · 0 | 26 · 74 · 0 |

On the test split the placement of the 25 alone spreads the escalations' order
over 29 cases, from 798 to 827, with every reached rule in place.

### The curve

The optimizer audit's random arrivals on split 0, searched again; each order
gave the record's shares and start. *Unreached* gives the rules and, after the
slash, the distinct ones. The front moves' *stake* is their gains summed, a loss
as zero, over the distinct rules: an index, since two moves can gain the same
case.

| labels, draw | start | unreached | the order: test · space | back move: test · space | front gains on test: rules · stake | over the space: rules · stake |
|---|---|---|---|---|---|---|
| 10, 0 | greedy | 247/196 | 563 · 44,735 | −5 · −11,090 | 38 · 421 | 35 · 64,939 |
| 10, 1 | greedy | 357/234 | 498 · 35,750 | 0 · 0 | 60 · 1,566 | 64 · 134,002 |
| 10, 2 | greedy | 264/207 | 659 · 45,700 | −32 · −11,500 | 30 · 200 | 30 · 67,720 |
| 10, 3 | greedy | 327/248 | 532 · 69,020 | 0 · 0 | 53 · 443 | 49 · 29,824 |
| 10, 4 | greedy | 305/235 | 491 · 51,330 | 0 · 0 | 66 · 803 | 55 · 32,459 |
| 50, 0 | random 4 | 98/91 | 717 · 47,965 | +3 · +475 | 11 · 32 | 11 · 18,269 |
| 50, 1 | greedy | 117/102 | 769 · 53,660 | −2 · −2,510 | 5 · 45 | 11 · 14,360 |
| 50, 2 | greedy | 115/109 | 574 · 48,575 | −1 · +5,185 | 21 · 165 | 24 · 22,040 |
| 50, 3 | greedy | 107/94 | 708 · 81,235 | 0 · 0 | 6 · 22 | 7 · 5,134 |
| 50, 4 | greedy | 133/108 | 734 · 60,655 | −1 · +3,245 | 10 · 134 | 12 · 15,070 |
| 100, 0 | random 1 | 59/55 | 791 · 58,610 | 0 · +1,250 | 1 · 1 | 5 · 11,665 |
| 100, 1 | greedy | 52/48 | 794 · 53,860 | −2 · −3,355 | 2 · 26 | 5 · 13,680 |
| 100, 2 | greedy | 71/66 | 775 · 75,940 | 0 · +25 | 2 · 16 | 8 · 6,160 |
| 100, 3 | greedy | 64/62 | 751 · 70,300 | 0 · 0 | 5 · 22 | 10 · 15,914 |
| 100, 4 | greedy | 64/58 | 804 · 57,395 | −2 · −8,820 | 0 · 0 | 4 · 8,820 |
| 251, 0 | random 44 | 17/17 | 825 · 75,480 | 0 · 0 | 0 · 0 | 1 · 5,760 |
| 251, 1 | greedy | 18/17 | 829 · 71,255 | 0 · 0 | 0 · 0 | 0 · 0 |
| 251, 2 | greedy | 23/23 | 820 · 72,239 | 0 · 0 | 0 · 0 | 1 · 8,675 |
| 251, 3 | random 14 | 28/27 | 768 · 48,290 | +9 · +120 | 3 · 4 | 5 · 16,664 |
| 251, 4 | random 3 | 18/17 | 802 · 68,850 | 0 · 0 | 1 · 1 | 2 · 20 |

**The fewer the labels, the more the unreached hold**: at ten labels a front
move gains on the test split for 30 to 66 distinct rules, and at 251 for none
to 3. The stake is largest where the orders are weakest, which is what an index
of one-at-a-time gains measures.

**The back move changes something in eleven of the twenty orders, eight of them
started from the greedy.** That start puts the unreached at the tail, so what
the back move undoes there is what the local search's swaps carried up. Where it
changes the test count, it lowers it in seven orders and raises it in two.

> **[ERRATUM 2026-10-21] The greedy start does not put the unreached at the
> tail, and the back move does not undo swaps there.** The record's greedy goes
> on choosing while a labelled case is left undecided. A rule that matches none
> of the cases left scores zero, and the greedy breaks ties by rule id, which is
> birth order. So once nothing scores above zero it takes the rules that score
> zero, earliest-born first, and a labelled case every matching rule gets wrong
> keeps it doing so through most of the base. Rules no label reaches then sit
> near their birth order's places. In all eight orders `R0019` starts between
> places 19 and 29, and no pass lifts it. §1 and §6.8 of the plan assumed the
> same tail. Read POST-RUN, from the greedy's code and the replayed starts, in
> *What the keyword holds over the space*, below. No figure and no verdict
> moves.

### The rare classes

Right decisions on the test split's rare queues, before and after the back move:

| order | `ACCOUNT_MANAGER` | `T3_ENGINEERING` | `SECURITY_INCIDENT` | `ONCALL_ESCALATION` |
|---|---|---|---|---|
| the escalations', and after the back move | 20 | 0 | 4 | 0 |
| the whole train half's, and after the back move | 19 | 18 | 5 | 0 |

**[Read after the verdicts]** Along the curve the back move moves a rare queue in
seven orders, and `SECURITY_INCIDENT` in six of them. In the two orders at ten
labels where it costs most, 5 and 32 test cases and about 11,000 points, the
order loses all 3 of its `SECURITY_INCIDENT` cases. At 50, 1 and at 100, 1 it
loses 2 of 3, and at 50, 4 and at 100, 4 it loses 1 of 2 and 2 of 2; at 50, 4
it also gains one `T3_ENGINEERING` case. The seventh is 50, 2, where it gains
all 3 `ONCALL_ESCALATION` cases. **So where deferring costs most, what it defers
is an unreached `SECURITY_INCIDENT` rule that had been deciding those cases
right.** Both orders started from the greedy, which put it at the tail, so a
swap had carried it up. The record does not name it.

> **[ERRATUM 2026-10-21] Nothing carried it up.** There are two such rules:
> `R0019`, which decides two of the three cases, and `R0067`, the earliest-born
> copy of the keyword rule, which decides the third. The greedy start put them
> at places 19 and 22 and at 65 and 67, and no move or swap lifted either. The
> sentence in bold stands. Read POST-RUN in *What the keyword holds over the
> space*, below.

---

## What this does not settle

- **Another draw of the same labels.** The escalations' order is one draw of the
  multi-start lottery. The coin shows what the placement of the 25 alone does:
  798 to 827 test cases, 65,900 to 77,300 points. Another draw would move the
  reached rules too.
- **The parts of the back move over the space.** The record holds the move's
  1,560 points and not which rules they come from, or where the 25 decide points
  in the order. **[NOTE 2026-10-21] Read POST-RUN**: one rule, `R0459`, the only
  one of the 25 that decides a point of the space there. The 1,560 are its
  keyword points, handed to the keyword rule. *What the keyword holds over the
  space*, below.
- **Why `R0019` leaves 5,900 points.** It sits 55 rules down. Which rules above
  it decide the keyword's severity-1 points, and with which queue, is not read.
  **[NOTE 2026-10-21] Read POST-RUN**: ten rules above the keyword rule's
  highest copy, at place 52, `T2_TECHNICAL` the queue that takes the most. Three
  of them decide no escalation. The same section.
- **Which rules the swaps carried up along the curve.** The record keeps each
  order but not the start it came from, which the declared seed would rebuild,
  so how far each unreached rule moved is not read. The rare-class reading above
  says what the costliest moves deferred, and not which rule it was. **[NOTE
  2026-10-21] Read POST-RUN: none.** The starts were rebuilt and replayed pass
  by pass. The `SECURITY_INCIDENT` rules the back move defers never rose: the
  greedy start put them there, in birth order. The same section, and the two
  errata above.
- **A selection that reaches rules** (§11.3 of the plan). On the arrivals there
  is nothing in the rules the escalations leave unreached to buy, beyond
  `R0545`'s six train tickets. Over the space there is `R0019`'s.
- **The hybrid pool, other splits, other bases and the online loop** (§11 of the
  plan).
- **A sum over rules can rest on one rule.** `Z-c` sums 22 rules' gains and holds
  on one, as `O-c`'s rate over declared edges rested on one declaration
  (`FINDINGS_OVERLAP.md`). A plan that bands a sum over rules should say in §0
  what it reads when one rule carries it.
- **A move cannot change what its rules do not decide.** `Z-d` was settled by a
  count of zero: none of the 25 decides a test case in the order. That count
  reads no truth, only the order and the matching, and the plan chose to read no
  order before signature. A plan that bands a move should count, before
  signature, how much of each surface the moved rules decide, and say in §0 why
  that reading does not inform the band.

---

## What the keyword holds over the space — POST-RUN

> **POST-RUN.** Asked for on 2026-10-20, after the stage, and run on
> 2026-10-21. `unreached/keyword_half.py` wrote its eight-clause expectation in
> its docstring and was committed before the first run, as `9da087f`, rebased
> unchanged to `e0c8131` on its branch. It read this stage's 22 orders and the
> audit stage's 40 from their records. It searched the escalations stage's 29
> again, since that record kept none. Four gates stood before any write:
> - every order is its record's, on both surfaces and on the four rare queues;
> - the masks are one convention: the keyword half is the keyword rule's
>   extension, and the truth by queue partitions the space;
> - two routes agree: every count walked rule by rule is `score_order`'s, and
>   every move summed rule by rule is this stage's figure;
> - every start, rebuilt from the declared seed and replayed pass by pass, ends
>   at the record's order.
>
> Not a signed row; no verdict moves. The record is
> [`keyword_half.json`](keyword_half.json), which keeps the escalations stage's
> 29 orders.

Four questions the records leave open turn on one attribute. Three are in *What
this does not settle*, above:
- why `R0019` leaves 5,900 points;
- which rules the back move's 1,560 come from;
- which rule a swap carried up along the curve.

The fourth is in `FINDINGS_ESCALATIONS.md` and `FINDINGS_SPOTCHECK.md`: why the
space follows `SECURITY_INCIDENT` at the top.

**The keyword half** is the 67,200 points of the space with the security
keyword. The hidden policy's first layer decides all of it: `SECURITY_INCIDENT`
on 50,400 points, and `T2_TECHNICAL` on the 16,800 of the two lower tiers at
severity 3 or 4. Rung 1's base routes to `SECURITY_INCIDENT` with thirteen
rules:
- `R0019`, *the keyword and severity 1*;
- **the keyword rule**, *the keyword* alone, written twelve times.

Only the highest of the twelve copies decides anything. It matches the whole
half, so no rule below it decides a point of the half. Its place is an order's
**copy place**.

### 1. Why `R0019` leaves 5,900 points

In the escalations' order the highest copy is `R0208`, at place 52, three above
`R0019`. It decides 10,900 of `R0019`'s 16,800 points, every one right. Ten rules
above it take the other 5,900 with another queue:

| place | rule | what it says | queue | of `R0019`'s points | escalations it decides: right of |
|---|---|---|---|---|---|
| 0 | `R0155` | billing, free tier, three or more recent tickets | `BILLING_SPECIALIST` | 720 | 25 of 27 |
| 2 | `R0497` | enterprise, billing, severity 4 or less | `ACCOUNT_MANAGER` | 840 | 6 of 6 |
| 6 | `R0411` | severity 1, billing, five or more recent tickets | `T3_ENGINEERING` | 1,280 | 1 of 1 |
| 7 | `R0054` | free tier, integrations, fifteen or more recent tickets | `T3_ENGINEERING` | 240 | 1 of 1 |
| 19 | `R0510` | free tier, dashboard, ten or more recent tickets | `T2_TECHNICAL` | 440 | 1 of 1 |
| 24 | `R0247` | free tier, dashboard, severity 3 or less, five or more | `T2_TECHNICAL` | 200 | 2 of 2 |
| 27 | `R0401` | free tier, billing | `BILLING_SPECIALIST` | 120 | 1 of 1 |
| 34 | `R0483` | api, severity 3 or less, free tier, ten or more | `T2_TECHNICAL` | 440 | none |
| 35 | `R0459` | integrations, by phone | `T2_TECHNICAL` | 780 | none, and no escalation reaches it |
| 51 | `R0485` | mobile, severity 3 or less, free tier | `T2_TECHNICAL` | 840 | none |

- **By queue**: `T2_TECHNICAL` takes 2,700, `T3_ENGINEERING` 1,520, and
  `ACCOUNT_MANAGER` and `BILLING_SPECIALIST` 840 each.
- **Seven of the ten name the free tier.** On the keyword's severity-1 points
  every tier is `SECURITY_INCIDENT` in truth.
- **Seven decide escalations**, and are right on 37 of the 39 they decide. They
  take 3,840 of the 5,900.
- **Three decide no escalation**: `R0483`, `R0485`, and `R0459`, which none
  reaches. They take the other 2,060, and the labels give the search no reason
  for their places.

**In the whole train half's order `R0019` is first**, right on all 16,800
points and on the three train tickets it decides.

So `R0019` leaves its points where nothing in the labels concerns the keyword
at severity 1: no escalation has both. The rules above the copy place take them,
some for tickets they are right on without the keyword, some for nothing the
labels say.

**Over the whole half the escalations' order is right on 34,690 of 67,200
points**: 26,440 `SECURITY_INCIDENT` ones, all the copy's, and 8,250
`T2_TECHNICAL` ones, all taken above it. The whole train half's is right on
39,440: 26,960 and 12,480.

### 2. The back move over the space is one rule

Of the 25 rules no escalation reaches, **only `R0459` decides a point of the
space** in the escalations' order. Every other one sits below rules that take
every point it matches, `R0506` among them, so deferring it changes nothing.

`R0459`, *integrations by phone* to `T2_TECHNICAL`, sits at place 35, above the
copy place. It decides 3,120 points:
- 1,560 with the keyword, all `SECURITY_INCIDENT` in truth, so all wrong;
- 1,560 without it, 360 of them right.

Deferred, it hands the first to the keyword rule, which is right on every one.
The second go to other `T2_TECHNICAL` rules, right on the same 360. **So the
back move's 1,560 is the keyword rule's**: `R0459`'s keyword points, handed to
it. On the other half the move is worth nothing.

### 3. The swaps carried nothing up

At ten labels, draws 0 and 2, the order's three `SECURITY_INCIDENT` test cases
are decided by `R0019`, two of them, and by `R0067`, the earliest-born copy, the
third. **Neither rose in any pass.** The greedy start put `R0019` at places 19
and 22, and `R0067` at 65 and 67. No move or swap lifted either; across the
replay each fell by one place at most.

**[Read from the greedy's code, after the reading]** The record's greedy goes on
choosing while a labelled case is left undecided. A rule that matches none of
the cases left scores zero, and the greedy breaks ties by rule id, which is
birth order. So once nothing scores above zero it takes the rules that score
zero, earliest-born first. A labelled case every matching rule gets wrong keeps
it doing so through most of the base. Rules no label reaches then sit near
their birth order's places, not at the tail. That is the erratum above.

| labels, draw | start | back move: test · space | keyword half · other half | `R0019` starts at |
|---|---|---|---|---|
| 10, 0 | greedy | −5 · −11,090 | −9,425 · −1,665 | 19 |
| 10, 2 | greedy | −32 · −11,500 | −8,830 · −2,670 | 22 |
| 50, 0 | random 4 | +3 · +475 | +220 · +255 | 134 |
| 50, 1 | greedy | −2 · −2,510 | −2,535 · +25 | 24 |
| 50, 2 | greedy | −1 · +5,185 | +4,350 · +835 | 25 |
| 50, 4 | greedy | −1 · +3,245 | +3,405 · −160 | 26 |
| 100, 0 | random 1 | 0 · +1,250 | +1,250 · 0 | 526 |
| 100, 1 | greedy | −2 · −3,355 | −3,355 · 0 | 25 |
| 100, 2 | greedy | 0 · +25 | 0 · +25 | 29 |
| 100, 4 | greedy | −2 · −8,820 | −8,820 · 0 | 26 |
| 251, 3 | random 14 | +9 · +120 | +60 · +60 | 516 |

These are the eleven orders the back move changes; every start was rebuilt and
replayed to the record's order.
- **In the eight that move 1,000 points or more, the keyword half carries most
  of the move.** In five of them the other half moves 160 points or fewer.
- **At 10, 0 the keyword half carries 9,425 of the 11,090; at 10, 2, 8,830 of
  11,500.** `R0019` decides 6,300 points of the space in both orders, every one
  right, and `R0067` 4,685 and 5,310. Deferring the rules no label reaches loses
  11,910 points at 10, 0 and gains 820; at 10, 2 it loses 12,170 and gains 670.
- **On the test split the 32 cases lost at 10, 2 are mostly `T2_TECHNICAL`
  rules** the greedy left in birth order. `R0010` and `R0038`, at places 13 and
  41 from the start on, lose 19 cases each. Others gain back some.

So at ten labels the order the search returns is mostly the greedy's own run in
birth order. The back move undoes that run, and not swaps.

### 4. The space follows the keyword half

| cell | orders | over the space | on the keyword half | on the other half |
|---|---|---|---|---|
| escalations, 10 | 7 | 28,515 to 36,040 | 4,700 to 10,600 | 22,570 to 28,660 |
| escalations, 50 | 7 | 43,455 to 61,810 | 10,010 to 39,275 | 22,535 to 36,040 |
| escalations, 100 | 7 | 49,810 to 71,280 | 16,245 to 38,840 | 32,440 to 38,180 |
| escalations, 251 | 7 | 53,985 to 74,660 | 13,635 to 36,370 | 38,290 to 40,350 |
| audited sets, 10 | 5 | 53,220 to 74,694 | 14,410 to 36,370 | 38,324 to 40,790 |
| audited sets, 50 | 5 | 55,204 to 79,420 | 14,420 to 38,890 | 36,450 to 41,030 |
| audited sets, 100 | 5 | 54,930 to 71,320 | 14,620 to 31,160 | 39,690 to 41,630 |
| audited sets, 251 | 5 | 59,385 to 75,535 | 17,835 to 34,090 | 40,305 to 42,310 |
| the audit alone, 10 | 5 | 37,485 to 78,100 | 7,560 to 50,400 | 24,305 to 31,560 |
| the audit alone, 50 | 5 | 42,750 to 72,590 | 8,370 to 42,200 | 25,730 to 34,380 |
| the audit alone, 100 | 5 | 52,930 to 80,055 | 16,200 to 43,470 | 33,290 to 36,730 |
| the audit alone, 251 | 5 | 57,320 to 75,910 | 19,820 to 38,480 | 35,440 to 39,645 |

Each figure is right decisions. The escalations' cells are the seven sets of
`FINDINGS_ESCALATIONS.md` at each budget, the five random draws, arrival and
crowded. The audit's are `FINDINGS_SPOTCHECK.md`'s five draws at each arm and
budget.

- **In all twelve cells the order with the most points over the space has the
  most on the keyword half**, and so do the random arrivals' four cells beside
  them.
- **Within the cells the keyword half's counts spread nearly 18 times as much as
  the other half's**, in squared deviations from the cell means. Pooled, the
  keyword half carries 1.035 of the cells' spread over the space: all of it,
  with the other half moving slightly against it. Cell by cell it carries 0.89
  to 1.42 of the spread in eleven cells. The twelfth is the escalations at ten
  labels, where it carries 0.55. In the random arrivals' four cells it carries
  0.78 to 0.99.
- **Over the 91 orders read, the keyword half runs from 4,700 right to 50,400**,
  every one of its `SECURITY_INCIDENT` points. The other half runs from 22,535
  to 42,310.

**So the space follows `SECURITY_INCIDENT` at the top because the keyword half
is where orders labelled differently differ over the function.** The test
split's ten `SECURITY_INCIDENT` cases read the same rule on ten tickets. Among
the full search's end orders, which share their labels,
`results3/FINDINGS_ORDERS.md` found that class carrying 57.5% of their
disagreement over the space. Between orders whose labels differ, the keyword
half carries the whole spread of the count.

**[Read after the reading] The five orders with the most keyword points each
hold, among their labels, a ticket with the keyword whose truth is
`SECURITY_INCIDENT`.** Their highest copy is `R0067`, at places 4 to 19. Holding
one is not enough: 29 of the 91 orders do. No escalation is one.

**[Read after the reading] The escalations' shortfall over the function lies in
the keyword half.** `FINDINGS_ESCALATIONS.md`'s `J-e` found that the escalations
buy less over the space than random arrivals, at every budget. Split by the
keyword, the medians of the five random draws on each side:

| labels | over the space: escalations · arrivals | keyword half | other half |
|---|---|---|---|
| 10 | 34,885 · 45,700 | 8,625 · 18,105 | 24,980 · 25,360 |
| 50 | 46,050 · 53,660 | 10,720 · 19,495 | 33,420 · 33,995 |
| 100 | 56,760 · 58,610 | 18,580 · 21,125 | 36,930 · 36,975 |
| 251 | 57,490 · 71,255 | 19,160 · 31,105 | 38,330 · 39,570 |

At every budget the other half's two medians lie within 1,240 points of each
other.

### Two orders that were one, and two that were not

- **The audited sets of draws 0 and 3 at ten decisions are the escalations
  alone's order**, list for list. `FINDINGS_SPOTCHECK.md` left open whether they
  were one order. `results_spotcheck/readings.json` kept both, and this stage's
  record keeps the third.
- **Draw 3 of 251 escalations and the order on all 316 are two orders.**
  `FINDINGS_ESCALATIONS.md` left this open too. Both give 814 and 73,020, from
  start 57, and 303 of their 577 places differ. They agree on both halves too,
  34,690 and 38,330. They split the keyword half differently by truth: 26,860
  `SECURITY_INCIDENT` points and 7,830 `T2_TECHNICAL` ones, against 26,440 and
  8,250. This reading's record keeps both.

### The expectation, clause by clause

| clause | expected | read | verdict |
|---|---|---|---|
| E1 | `T2_TECHNICAL` takes the most of `R0019`'s 5,900 | 2,700; then `T3_ENGINEERING`, 1,520 | holds |
| E2 | every rule taking 500 or more decides an escalation, and is right on three quarters of those | five take 500 or more; `R0459` and `R0485` decide none | **fails** |
| E3 | deferring `R0506` loses points over the space | it decides none; nothing changes | **fails** |
| E4 | the copy place is above every unreached rule, so the keyword half's part of the back move is zero | 52, below `R0459` at 35; the part is all 1,560 | **fails** |
| E5 | at ten labels, the rules deciding the `SECURITY_INCIDENT` test cases made their largest rise in a swap | `R0019` and `R0067`; neither rose in any pass | **fails** |
| E6 | there the keyword half carries the whole of the back move's loss over the space | 9,425 of 11,090, and 8,830 of 11,500 | **fails** |
| E7 | in 9 or more of the 12 cells the top over the space is the top on the keyword half | 12 of 12 | holds |
| E8 | the keyword half spreads more within the cells than the other half | nearly 18 times, in squared deviations | holds |

**Three of eight held.** E7 and E8 held with room; they ask whether the space
follows the keyword half. E1 held. The five that failed bet on how the orders
came to put the keyword's rules where they are:
- that the labels placed every rule above the copy (E2);
- that the on-call rule decided anything there (E3);
- that the copy sat above every rule no escalation reaches (E4);
- that a swap carried the `SECURITY_INCIDENT` rules up (E5), and that the keyword
  half carries all of that loss (E6).

The drafter trusted E4 least and E1 next: E4 failed and E1 held.

### What this reading does not settle

- **How much of a small budget's greedy start is birth order.** It is read here
  from the greedy's code and from where `R0019` and `R0067` start. No record
  counts the picks the greedy makes at zero along the curve. Free.
- **Why `R0483` and `R0485` sit above the copy.** Both decide no escalation, so
  the labels give their places no reason. This reading did not rebuild the
  escalations' start. Free.
- **Whether a labelled `SECURITY_INCIDENT` ticket with the keyword is what lifts
  the copy.** It was read on five orders after the reading, and 29 hold one.
- **The hybrid pool, other splits and other bases**, as for the stage.

---

## Files

```
unreached/plan.py         the gate and §9's constants; §1's material, the table of the 25, the curve's reach
unreached/moves.py        reach, the front move, the back move, the coin, copies; no truth
unreached/gates.py        Z-g1 to Z-g4, blocking, run first
unreached/score.py        the stage: Z-a to Z-e, the readings of Z-f
unreached/keyword_half.py POST-RUN: what the keyword holds over the space
results_unreached/score.json   every figure: both endpoints rule by rule, the coin, the curve, the gates, the orders
results_unreached/keyword_half.json   the reading's figures, the escalations stage's 29 orders, the gates, the expectation
tests/test_unreached.py   how the package counts — and no figure
tests/test_unreached_keyword_half.py  how keyword_half.py counts, and each clause at its edge
```

The instrument is `escalations/instrument.py`'s, called and not copied.
Reproducible, in this order:

```
python3 -m unreached.score --dry-run          # Z-g1..Z-g4, blocking; writes nothing
PYTHONHASHSEED=0 python3 -m unreached.score   # about eleven minutes
PYTHONHASHSEED=0 python3 -m unreached.keyword_half  # POST-RUN; about four minutes
```
