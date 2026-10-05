# What the proposer says it is doing, against what it does — findings

Record opened on October 5, 2026, under [`PLAN_WHY.md`](../PLAN_WHY.md). Sergi
signed §0 on 2026-10-05, before any held-out sentence was coded, in a commit of
its own: *PLAN_WHY.md signed by Sergi*. The stage's record,
[`score.json`](score.json), names that commit in its `_env` as `8144fa2`, its hash
on the branch it was made on. A rebase merge gives it a new hash on `main` with
the same tree, so it is named here by its subject. **This record owns every
figure in it, the development figures included.**

**The stage adjudicated all four signed rows on 2026-10-05, and all four hold.**
They were set on a development set from the same model a day earlier, so what
the four holds say is that the readings generalise from 365 sentences to 1,114.
They say nothing about the drafter's foresight; §0 of the plan said so before the
stage ran.

- **When the proposer says the rule it names is more specific, that rule is the
  narrower one about half the time** (`Y-a`).
- **Its "specific" is not a count of conditions** (`Y-b`). **It is a categorical
  or exact condition the other rule lacks**: a product, an exact value
  (`Y-c`).
- **The reason it gives does not tell its right answers from its wrong ones**
  (`Y-d`).
- **It almost never says that the order decided**, though the slot decides at
  least one answer in twelve. 8 of the 1,114 sentences give the list's order as
  the reason, and all 8 name the rule listed first (post-run).

> **PROVENANCE: PRE-REGISTERED ON A HELD-OUT BATCH.** `Y-a` to `Y-d` were signed
> before any held-out sentence was coded, with bands set on a development set
> whose figures §0 declares. **`Y-e` is reported, not adjudicated.** Everything
> labelled **POST-RUN** below was read after the verdicts existed, by someone who
> had seen them, and is a reading, not a bet. That covers the codebook's precision
> checked by hand, the order sentences, and the comparisons with development
> beyond §0's. Zero API calls.

---

## What was run

`PYTHONHASHSEED=0 python3 -m why.score`, on 2026-10-05, from the signing commit
with a clean tree: 65 s, nearly all of it the suite, and zero API calls. The
record is [`score.json`](score.json).

**The blocking checks passed again before any held-out sentence was coded.**

- **`Y-g1`.** The suite is green, 1,272 tests. The 1,600 record reproduces its
  own counts, Stage D's record is its development batch with every `why` equal,
  and the truth lines up.
- **`Y-g2`.** 400 and 1,200 answers, no pair shared. 365 development sentences,
  166 of Stage C, and 1,114 held out.
- **`Y-g3`.** The codebook is `65e1732a08fd32c0`, and it reproduces every
  development figure the plan declares, Stage D's and Stage C's.
- **`Y-g4`.** Signed.

**The held-out set** is the batch answered on 2026-08-25. It holds 1,114 answers
that named one of their two rules, each with its `why`.

---

## The four rows

| row | statistic | held out | error | band | development | verdict |
|---|---|---|---|---|---|---|
| `Y-a` | answers coded `spec` whose named rule is narrower | 339 of 645, **0.5256** | 0.0197 | 0.45 to 0.62 | 92 of 172, 0.5349 | **holds** |
| `Y-b` | `spec` without `count`, named rule with more conditions | 161 of 585, **0.2752** | 0.0185 | < 0.33 | 37 of 147, 0.2517 | **holds** |
| `Y-c` | categorical edge: `spec` without `count`, minus answers not coded `spec` | 0.7658 (448/585) − 0.4435 (208/469) = **+0.3223** | 0.0289 | ≥ 0.15 | +0.2632 | **holds** |
| `Y-d` | naming the better rule, space: `spec`, minus not `spec` | 0.7395 (369/499) − 0.7470 (245/328) = **−0.0075** | 0.0310 | \|·\| < 0.06 | −0.0187 | **holds** |

None is thin: each is more than one error from every line it has. **The drafter
expected all four to hold**, and trusted `Y-d` least, then `Y-a`. Every held-out
value lies within about one standard error of its development value, counting
both sets' errors; `Y-c` is the farthest, at 1.0.

### What the verdicts say

**1. The specificity claim is true of the extension about half the time.**
Across all held-out answers the named rule is the narrower 439 times in 1,114,
0.3941. Among those that argue specificity it is 0.5256. So the claim leans
towards the narrower rule, and still names the broader one, or an equal one, 306
times in 645. §15 of [`FINDINGS3.md`](../results3/FINDINGS3.md) said in one
sentence that the proposer claims specificity and names the broader rule. That
sentence now has its measure: about half the time, against a base of four in ten.

**2. It is not counting conditions.** Outside the sentences that count them
explicitly, the named rule lists more conditions 0.2752 of the time, against
0.2244 across all held-out answers.

**3. It is pointing at a categorical or exact condition.** Among those same
sentences, the named rule carries a condition the other lacks 0.7658 of the time.
That means a product the other does not name, an exact severity against a range,
or more `eq` conditions. Among answers that do not argue specificity it is
0.4435. **For this proposer, "more specific" describes how a rule is written,
what it names and how exactly. It does not describe what the rule covers.**

**4. The reason does not mark the right answers.** On pairs with a strictly better
rule on the space, answers that argue specificity name it 0.7395 of the time and
the rest 0.7470. The stated reason carries no signal of correctness, so read as a
filter it would join the truth-free selections that §14 of `FINDINGS3.md` found
no better than chance. That was read at the pair level; the order level is §10.5
of the plan, and not run.

---

## What the sentences say — `Y-e`, reported

**The census**, held out against development (Stage D):

| | held out (1,114) | development (365) |
|---|---|---|
| `spec`, specificity | 645 (0.579) | 172 (0.471) |
| `count`, counts conditions | 61 | 25 |
| `queue`, a queue's importance | 378 (0.339) | 130 (0.356) |
| `match`, an exact or complete match | 134 | 42 |
| `order`, order or a default | 9 | 3 |
| `prio`, a verb of precedence | 438 | 170 |
| no reason code | 149 (0.134) | 73 (0.200) |
| Spanish / English / Chinese | 780 / 311 / 23 | 245 / 115 / 5 |

**The labels.** A sentence that names one label only names the chosen rule's in
510 of 511 cases; 195 name both and 408 neither.

**The direction rate by code.** On each definition, the share of answers naming
the better rule among those with one:

| code | space | corpus |
|---|---|---|
| `spec` | 0.7395 (499) | 0.7177 (503) |
| `queue` | 0.8008 (261) | 0.6300 (227) |
| `match` | 0.7010 (97) | 0.7255 (102) |
| `count` | 0.5682 (44) | 0.5238 (42) |
| `order` | 0.5000 (8) | 0.4286 (7) |
| no reason code | 0.7238 (105) | 0.7373 (118) |
| all held-out answers | 0.7424 (827) | 0.6860 (812) |

- **When it counts conditions it is right about as often as a coin.** That is
  rung 1's criterion, specificity read off the number of conditions. 25 of 44 on
  the space, and with development's 10 of 19, 35 of 63, 0.556: within one
  standard error of a coin. *Pooled post-run.*
- **The security reasons are wrong more often on the arrivals.** Against the rest,
  `queue` answers are right +0.0852 more often on the space (error 0.0312) and
  0.0777 less often on the corpus (error 0.0372). On the corpus the sign is the
  same as development's, which was −0.2284. On the space it is not: development
  measured −0.0520. *Post-run.* The corpus side is the security keyword's
  divergence between the two surfaces, which
  [`FINDINGS_EDGES.md`](../results_edges/FINDINGS_EDGES.md) measured on declared
  edges. The space side does not replicate.

**By B-d's side**, on the space: `spec` is argued on 190 of 335 answers where a
fixed ranking can answer, 309 of 492 where it cannot, and 146 of 287 pairs with
no strictly better rule. `queue` is argued on 123, 138 and 117 of them.

**Quotations** are in [`score.json`](score.json), five per code and five `spec`
sentences whose named rule is not the narrower, for instance:

> *"Regla A: enterprise, severity 4, 5 prior tickets; más específica que B."*
> (index 0, the broader rule named)
>
> *"La regla B es más específica al requerir severity 4, mientras que A solo pide
> severity gte 3."* (index 1490, the broader rule named)

---

## The order, said aloud — POST-RUN

*Read after the verdicts.* Nine held-out sentences carry the `order` code.
**Eight are genuine appeals to the list's order, and every one of them names the
rule listed first**:

> *"Ambas reglas aplican; se prioriza la regla A por aparecer primero en el
> manual."* (24)
>
> *"Ambas reglas casan, se aplica la primera (A) por orden de precedencia."* (561)
>
> *"Both rules match equally; arbitrating to first matching rule's queue."* (1420)

The ninth, *"security incident handled first"* (1587), is the pattern `\bfirst\b`
matching something else.

**So the proposer says the slot decided in 8 answers of 1,114, under one in a
hundred.** [`FINDINGS_PRIMACY.md`](../results_primacy/FINDINGS_PRIMACY.md)
measures that the slot decides at least one answer in twelve. The slot works
almost entirely without being named.

**Three of the eight concern rules with identical conditions.** The learned base
holds pairs of rules whose conditions are the same, written in another order,
with different queues: `R0147` and `R0435`, `R0164` and `R0447`, both
`T1_GENERAL` against `SELF_SERVICE_DEFLECT`. Of the 1,600 pairs, 5 are like
that, all in the held-out batch, as the conditions listed in each question
confirm.

- **The proposer named the rule listed first in 4 of the 5.** Three of those
  gave the order as the reason: *"Ambas reglas tienen las mismas condiciones,
  pero la A aparece primero en el manual."* (815).
- **The fourth called one of two identical rules the more specific one**: *"Ambas
  reglas son idénticas; BILLING_SPECIALIST es la más específica y especializada
  en billing."* (68). That is what `Y-c` says "specific" means, with nothing in
  the conditions to support it.
- **The fifth named the rule listed second**, and gave its queue as the reason.

Five pairs are an anecdote. They are also the one place in the record where the
content gives the proposer nothing to go on.

---

## The codebook, checked by hand — POST-RUN

The codebook was frozen before signature and is not edited. What reading the
held-out sentences found about it:

- **`count`**: 60 of its 61 sentences count conditions. The other, 815, says
  *"las mismas condiciones"*. The pattern `m[aá]s condiciones` has no word
  boundary and matches inside *mismas*. The same sentence is therefore also
  coded `spec`, which moves `Y-a` by at most one answer in 645. It is outside
  `Y-b` and `Y-c`, which exclude `count`.
- **`spec`**: of a sample of 30 of the 585 sentences coded `spec` without
  `count`, drawn with `random.Random(17)`, all 30 argue that the rule the answer
  named is the more specific.
- **`order`**: 8 of 9 genuine, above.
- **Coverage**: 149 held-out sentences, 0.134, carry no reason code. In
  development the share was 0.200.

---

## What this settles, and what it does not

**It answers what §15 left as one sentence.**

- **What the proposer means by specific**: a rule that names a product or an
  exact value, not one that covers less or lists more. The claim is true of the
  extension about half the time.
- **Whether its stated reason marks its right answers**: it does not, on the
  space. And when it reasons the way rung 1's engine did, by counting conditions,
  it is right about as often as a coin.
- **Whether it says what the slot does**: almost never. 8 answers in 1,114 name
  the order, all for the rule listed first.

**What it does not settle**, as §10 of the plan declared before it ran:

- **Whether the stated reasons cause the answers.** A `why` is written with its
  answer, and agreement between them is a correlation.
- **Phrasings the codebook does not know.** 13.4% carry no reason code.
- **Other models and prompts.** One model, one prompt.
- **What a `why`-based selection does to the compiled order.** It would be free,
  §14's question at the order level, and it would need its own row.

---

## Files

```
results_why/score.json   the checks, Y-a to Y-d, every reading of Y-e, the
                         quotations, and every held-out row with its codes
why/plan.py              the gate, the codebook's fingerprint, the development
                         figures, §0's four lines
why/codebook.py          the frozen codebook
why/rows.py              the rows and §0's statistics
why/gates.py             Y-g1 to Y-g4
why/score.py             the stage
```

Reproducible with `PYTHONHASHSEED=0 python3 -m why.score`, about a minute, zero
API calls. `--dry-run` runs the checks and writes nothing.
