# Where the slot decides — findings

Record opened on October 5, 2026, under [`PLAN_PRIMACY.md`](../PLAN_PRIMACY.md).
Sergi signed §0 on 2026-10-05, before any figure below existed, in a commit of
its own: *PLAN_PRIMACY.md signed by Sergi*. The stage's record,
[`score.json`](score.json), names that commit in its `_env` as `63b901c`, its
hash on the branch it was made on. A rebase merge gives it a new hash on `main`
with the same tree, so it is named here by its subject. **This record owns every
figure in it.**

**The stage adjudicated both signed rows on 2026-10-05: one holds and one is
refuted, thinly.**

- **On the queue pair the proposer splits evenly, the slot decides at least an
  eighth of the answers, not the fifth the row bet** (`L-a` is refuted, thin).
- **The slot decides which rule an answer names and nothing else this record
  can see.** Whether the favoured rule is listed first or second does not
  change how often an answer yields no edge, nor how often it needed more than
  one call (`L-b` holds).
- **The effect is the same on both sides of B-d, in both batches, and whichever
  rule is the broader one.** It does not sit where a ranking cannot answer, so
  it explains none of B-d's gap.
- **Most of it sits on one queue pair, `T1_GENERAL vs T2_TECHNICAL`, where the
  slot decides at least a fifth of the answers.** Outside that pair the rest are
  within noise of a coin (post-run).

> **PROVENANCE: PRE-REGISTERED.** `L-a` and `L-b` were signed before any of their
> figures existed. **`L-c` is reported, not adjudicated**. Two of its figures were
> already published, the overall first-listed rate and Stage C's, and the rest
> are computed here for the first time. Everything labelled **POST-RUN** below
> was selected or derived after the verdicts existed, by someone who had seen
> them, and is a reading, not a bet. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m primacy.score`, on 2026-10-05, from the signing
commit with a clean tree: 65 s, nearly all of it the suite, and zero API calls.
The record is [`score.json`](score.json).

**The blocking checks passed again before any figure of §0 was computed.**

- **`L-g1`.** The suite is green, 1,234 tests. The 1,600 record reproduces its
  own counts, and the published figures reproduce from its rows: 801 of 1,479
  edges naming the rule listed first, and §15's 623 of 730 and 571 of 749. So do
  Stage C's breakdown by position, the truth row by row, and B-d's split on both
  definitions.
- **`L-g2`.** Every slot is `winner_positions`' seeded deal: all 1,200, 400 and
  170.
- **`L-g3`.** Every row is well formed. §2.1's rule picks exactly
  `SELF_SERVICE_DEFLECT vs T2_TECHNICAL`, at 86 against 82. No queue pair ties,
  so no row is counted apart.
- **`L-g4`.** Signed.

**Notation**, the plan's. The **slot effect `d`** is the share of declared
answers naming a reference rule when it is listed first, minus the share naming
it when it is listed second. The slot was dealt at random, so `d` is a lower
bound on the share of answers the slot decided (§5.4 of the plan).

---

## The two rows

| row | statistic | first slot | second slot | value | error | band | verdict |
|---|---|---|---|---|---|---|---|
| `L-a` | answers naming `SELF_SERVICE_DEFLECT`, by where its rule was listed | 43 of 74, 0.5811 | 43 of 94, 0.4574 | **d = +0.1236** | 0.0770 | d ≥ 0.20 | **refuted, thin** |
| `L-b` | rows with no edge, by where the favoured rule was listed | 62 of 793, 0.0782 | 59 of 807, 0.0731 | **−0.0051** (second minus first) | 0.0132 | \|·\| < 0.025 | **holds** |

`L-a` is thin: 0.0764 from its line, against an error of 0.0770. The label does
not change the verdict. `L-b` is 0.0199 from its line, more than its error.

**The drafter expected both to hold, and trusted `L-a` least. It was refuted.**
One of two called right: the row trusted more.

### What the verdicts say

**1. On the evenly split pair, the slot decides an eighth of the answers or
more, and the row cannot say how much more.** `L-a` is refuted at +0.1236. Its
error is wide enough to hold a slot that decides almost nothing and one that
decides a fifth. Within it sit both the uniform pull §0 calibrated at about 0.15
and the line itself. What it does exclude is a strong tiebreaker: a
`d` of 0.30 would sit 2.3 errors above what was measured.

**And on this pair the proposer's answers carry no truth at all.** Of its
declared answers on pairs with a strictly better rule, it names that rule 65
times in 129 on the space definition, 0.5039, and 85 times in 163 on the corpus
definition, 0.5215. Its even split is not content it tracks, at least none the
hidden policy rewards, and the slot decides at least an eighth of it.

**2. The slot does not reach the answer's form.** `L-b` holds at −0.0051. With
the favoured rule listed second, 59 of 807 rows yielded no edge, 0.0731. With it
listed first, 62 of 793, 0.0782. Split further:

- **Parse failures**: 55 with the favoured rule listed second, 62 with it listed
  first.
- **The four answers that parsed without an action** all came with the favoured
  rule listed second, 4 against 0. Four is too few to read.
- **Answers that needed more than one call**: 232 of 748 with the favoured rule
  listed second, 224 of 731 with it first, +0.0037 with an error of 0.0240. A
  first call can fail for any reason, so this is not a parse-failure rate.

**So the slot does not shape which answers declare an edge**, which is what §5.5
of the plan said `d`'s population needed.

---

## Where the slot decides — `L-c`, reported

**Overall.** `d` is +0.0823, error 0.0259, with `rule_a` as the reference: 374
of 728 answers name `rule_a` when it is listed first, 324 of 751 when it is
listed second. With the favoured queue's rule as the reference it is +0.0903,
error 0.0203. These are the floor the erratum of 2026-10-05 to `FINDINGS3.md`
§15 derived from published counts, 0.0832 and 0.0911, now measured directly.
`rule_a` is a reference fixed by birth before any answer was given; the favoured
queue is computed from the answers themselves (§5.3 of the plan). About one
answer in twelve.

**By B-d's side, with the better rule as the reference.**

| definition | reachable | unreachable | difference |
|---|---|---|---|
| space | +0.0575 (se 0.0325; 214/240 vs 176/211) | +0.0811 (se 0.0374; 212/311 vs 206/343) | +0.024 |
| corpus | +0.0644 (se 0.0316; 136/143 vs 133/150) | +0.0812 (se 0.0348; 247/397 vs 218/403) | +0.017 |

On both definitions the difference is under half its own error, 0.0495 on the
space and 0.0470 on the corpus. **The slot does not decide more where a fixed
ranking cannot answer.** So it explains
no measurable part of `B-d`'s gap, 0.8647 against 0.6391 on the space
([`FINDINGS3.md`](../results3/FINDINGS3.md) §11). On the pairs with no strictly
better rule the first-listed rate is 203 of 374, 0.5428, on the space, and 216
of 386, 0.5596, on the corpus: no different from the rest.

**By batch, with `rule_a` as the reference.** Stage D's 400, answered on
2026-08-24: +0.0767, error 0.0519. The 1,200 answered on 2026-08-25: +0.0839,
error 0.0298. **The effect replicates across the two dates.**

**By the breadth of the rule listed first.** With the broader rule listed first,
the proposer names the rule listed first 471 times in 733, 0.6426. With the
narrower one first, 319 times in 727, 0.4388. That is §15's preference for the
broader rule, not an interaction. Read with the broader rule as the reference,
it is named 0.6426 of the time when listed first and 408 of 727, 0.5612, when
listed second: **`d` = +0.0814, error 0.0255, the overall effect.** The proposer
does not read the list as a default followed by its exception. Equal extensions,
20 rows, are counted apart.

**On Stage C**, the same prompt over the hidden policy's pairs: 84 of 166
two-way answers name the rule listed first, 0.5060, and with the winner as the
reference `d` is +0.0218, error 0.0457 (75 of 82 against 75 of 84). That is
consistent with zero and with the learned base's 0.08 alike, as the erratum to
§15 said.

**By queue pair**, the eleven with at least 30 declared answers, with each pair's
alphabetically first queue as the reference:

| queue pair | answers | majority | `d` | error |
|---|---|---|---|---|
| `T1_GENERAL vs T2_TECHNICAL` | 361 | 0.756 | **+0.2256** | 0.0441 |
| `BILLING_SPECIALIST vs T1_GENERAL` | 180 | 0.928 | +0.0508 | 0.0380 |
| `SELF_SERVICE_DEFLECT vs T2_TECHNICAL` | 168 | 0.512 | +0.1236 | 0.0770 |
| `SELF_SERVICE_DEFLECT vs T1_GENERAL` | 155 | 0.729 | +0.0433 | 0.0715 |
| `SECURITY_INCIDENT vs T2_TECHNICAL` | 123 | 1.000 | 0 | — |
| `BILLING_SPECIALIST vs SELF_SERVICE_DEFLECT` | 118 | 0.729 | −0.1048 | 0.0845 |
| `BILLING_SPECIALIST vs SECURITY_INCIDENT` | 75 | 0.973 | +0.0036 | 0.0374 |
| `ONCALL_ESCALATION vs T2_TECHNICAL` | 60 | 0.967 | +0.0690 | 0.0471 |
| `SECURITY_INCIDENT vs T1_GENERAL` | 55 | 1.000 | 0 | — |
| `BILLING_SPECIALIST vs T2_TECHNICAL` | 40 | 0.800 | +0.0614 | 0.1297 |
| `SECURITY_INCIDENT vs SELF_SERVICE_DEFLECT` | 31 | 1.000 | 0 | — |

On the three unanimous pairs `d` is zero by construction (§5.6 of the plan). On
those pairs the slot decided nothing.

---

## The concentration — POST-RUN

*Read after the verdicts, and picked out because it is the largest. Not a row
and not a bet.*

**`T1_GENERAL vs T2_TECHNICAL` carries most of the effect.** It has 361 declared
answers, 273 of them naming `T2_TECHNICAL`. With the `T1_GENERAL` rule listed
first, the proposer names `T1_GENERAL` 63 times in 175, 0.36. With it listed
second, 25 times in 186, 0.13. **`d` = +0.2256, error 0.0441: the slot decides at
least a fifth of this pair's answers**, 5.1 errors from zero. A search over
eleven pairs does not produce that by chance.

**Outside it, the rest is within noise of a coin.** The record counts 801 of
1,479 answers naming the rule listed first overall, and 224 of 361 on this pair.
So the other 1,118 declared answers name the rule listed first 577 times, 0.5161,
1.08 deviations from a coin. Half of those answers, 576 by the 1,600 record's
own per-queue-pair counts, sit on pairs the proposer answers the same way nine
times in ten or more, where the slot can decide almost nothing. On the other
non-unanimous pairs the signs are mixed.

**What it says about `L-a`.** The row looked where the aggregate split was even,
and the effect is on a pair that leans three to one. **An even aggregate split
did not mark where the slot decides.** On `SELF_SERVICE_DEFLECT vs T2_TECHNICAL`
the proposer is undecided against the truth and the slot decides an eighth or
more. On `T1_GENERAL vs T2_TECHNICAL` it mostly answers `T2_TECHNICAL`, and the
slot moves a fifth of its answers. The refutation stands as signed. It does not
refute the tiebreaker reading, and nothing here supports it: what the records
show is one pair of generic support queues, which is not a mechanism.

---

## What this settles, and what it does not

**It answers what the answers already paid for can say about the position
effect.**

- **The slot decides which rule is named, and nothing else the record sees.**
  No-edge answers and calls needed are the same whichever slot holds the
  favoured rule.
- **Where it decides.** Not more where a ranking cannot answer, not differently
  by breadth, the same in both batches, and mostly on `T1_GENERAL vs
  T2_TECHNICAL` (post-run).
- **`L-a`'s bet is refuted as signed, thinly**: on the evenly split pair the slot
  decides an eighth of the answers or more, not demonstrably a fifth.

**What it does not settle**, as §10 of the plan declared before it ran:

- **Why the slot decides.** Position, label and the order of the queue names
  never come apart in an answer paid for.
- **How much it decides.** Every figure here is a floor. Each pair was asked in
  one order.
- **Whether it costs accuracy on net.** The same reason.
- **Why `T1_GENERAL vs T2_TECHNICAL`.** It was found after the verdicts. If the
  paid follow-up of §10.5 of the plan is ever run, this pair is where it has the
  power to see something: a fifth of its answers or more move with the slot.
- **Other models and prompts.** One model, one prompt.

---

## Files

```
results_primacy/score.json   the checks, L-a, L-b and every reading of L-c
primacy/plan.py              the gate and §8's constants; §0's two lines
primacy/rows.py              §0's definitions and statistics, pure functions
primacy/gates.py             L-g1 to L-g4
primacy/score.py             the stage
```

Reproducible with `PYTHONHASHSEED=0 python3 -m primacy.score`, about a minute,
zero API calls. `--dry-run` runs the checks and writes nothing.
