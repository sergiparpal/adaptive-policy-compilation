# The ranking of the queues, asked of the model — findings

Record opened on October 17, 2026, under [`PLAN_RANKING.md`](../PLAN_RANKING.md).
Sergi signed §0 on 2026-10-17, before any figure below existed, in a commit of
its own: *PLAN_RANKING.md signed by Sergi*. Every record names in its `_env` the
commit of the branch it was written on. A rebase merge gives those commits new
hashes on `main` with the same trees. **This record owns every figure in it.**

**All three stages ran on 2026-10-17, and the five rows are adjudicated: `M-a`
holds, `M-b`, `M-c` and `M-d` are refuted, and `M-e` holds, thin.** Asked for
its ranking, the model states a priority order. As an arbitration order it
scores below arrival order and below a blind draw, and it predicts the model's
own pairwise answers far worse than the ranking that read the hidden policy's
key. The smoke session's answers enter no row.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Every figure below was
> computed after the signature, by the free stage §10 kept behind the gate,
> because the revealed ranking's lookup score is the closest thing to `M-b`'s
> answer that exists without paying. Zero API calls.

---

## Stage A — the checks and the free readout

**What was run.** `python3 -m ranking.sample`, on 2026-10-17, with
`PYTHONHASHSEED=0`, on a clean tree at the signature's commit. It took about
eight minutes: `M-g1`'s enumeration of the 40,320 hierarchies on every cell and
under both tie-breaks, then the suite inside it. The record is
[`sample.json`](sample.json).

**Surfaces.** Rung 1's 577 rules on both of rung 3's pools, over the corpus
(the full 2,000 cases and the test half of each of the five splits) and over
the exhaustive space of 134,400 cases. **The signed cell is the `hibrido` pool
at corpus test split 0**, 995 cases, where `P-d` and `B-b` were read. Every
other cell is reported and adjudicates nothing (§0).

**The blocking checks passed before anything was computed.**

- **`M-g1`.** The 28 rows of
  [`queue_hierarchy_floor.json`](../results3/queue_hierarchy_floor.json),
  measured again with rung 3's own enumeration, differ in nothing. Both
  tie-breaks agree on all 14 cells, and `floor_by_pool.json`'s born_at floors
  come back. The suite was green, 1,738 tests.
- **`M-g2`.** Each of the twelve presentations' requests carries the eight queue
  names once and nothing else, and a changed order moves the digest.
- **`M-g3`.** The populations are the records' own: 1,479 declared answers on
  the learned base and 166 two-way answers on the hidden policy's pairs. The
  revealed ranking and its 1,194 of 1,479 come back. `K-b`'s, `K-e`'s and Stage
  C's readings come back on 65 and 66 units.
- **`M-g4`.** Signed.

**Every figure §0 lists as already seen reproduces**, the two of its note of
2026-10-17 included, so §0 needs no erratum beyond that note. The three lines
§0 reads from records were read as 0.463166 for `M-b`, 0.482412 for `M-c` and
0.546026 on 65 units for `M-e`.

### The revealed ranking as a lookup — the figure `FINDINGS3.md` §14 did not compute

The model's revealed ranking on the learned base is `rung3/edge_dropping.py`'s:
Copeland over the 1,479 declared answers, `ONCALL_ESCALATION`,
`SECURITY_INCIDENT`, `T3_ENGINEERING`, `BILLING_SPECIALIST`, `ACCOUNT_MANAGER`,
`SELF_SERVICE_DEFLECT`, `T2_TECHNICAL`, `T1_GENERAL`. Applied as a lookup over
the 577 rules, with Stage C's ranking and the family's references beside it:

| cell | born_at | blind mean | best of 40,320 | Stage C | **revealed** | hidden-policy revealed |
|---|---|---|---|---|---|---|
| `hibrido` · corpus test split 0 | 0.4332 | 0.3670 | 0.5266 | 0.4824 | **0.4693** | 0.4824 |
| `hibrido` · five-split mean | — | — | — | 0.4806 | 0.4675 | 0.4806 |
| `hibrido` · full corpus | 0.4285 | 0.3676 | 0.5240 | 0.4805 | 0.4685 | 0.4805 |
| `hibrido` · space | 0.4257 | 0.3180 | 0.5997 | 0.5838 | 0.5037 | 0.5769 |
| `puro` · corpus test split 0 | 0.5216 | 0.3215 | 0.5015 | 0.4291 | 0.4131 | 0.4281 |
| `puro` · full corpus | 0.5115 | 0.3234 | 0.4995 | 0.4285 | 0.4170 | 0.4275 |
| `puro` · space | 0.3148 | 0.2898 | 0.6058 | 0.5756 | 0.4196 | 0.5621 |

`best` read the cell's labels and is a winning ticket, not a level. `Stage C`
read the hidden policy's key. The two revealed rankings read no label (§0's
table of who had one). Every split is in the record.

**What it says.**

1. **On the signed cell the revealed ranking scores 0.4693, 467 cases of 995,
   not 0.4824.** The 0.4824 is Stage C's ranking, 480 cases. So `FINDINGS3.md`
   §14's sentence *the same ranking applied as a lookup over all 577 rules
   scores 0.4824* gives one ranking's figure to another. Read on one ranking,
   §14's comparison is 0.4402 as sparse edges against 0.4693 as a lookup. That
   section now carries a dated erratum in place.
2. **It is below Stage C's ranking on every cell**, by 13 cases on the signed
   one. The gap is widest over the space, 0.5037 against 0.5838 on the hybrid
   pool, and 0.4196 against 0.5756 on the pure one.
3. **On the signed cell it clears `P-d`'s threshold by six cases**: 467
   against the 461 that 0.463166 needs. That is context for `M-b` and not a
   verdict. `M-b` reads the rankings the model states, and none exists yet.
4. **The 1,600-call compiled order sits between the two rankings.** Its 0.4804
   on this cell (`FINDINGS3.md` §11) is above the model's own revealed
   ranking's lookup and below only the ranking that read a key.

### The hidden policy's revealed ranking

The same Copeland over the 166 two-way answers of the hidden policy's pairs:
`SECURITY_INCIDENT`, `ONCALL_ESCALATION`, `T3_ENGINEERING`, `ACCOUNT_MANAGER`,
`BILLING_SPECIALIST`, `T2_TECHNICAL`, `SELF_SERVICE_DEFLECT`, `T1_GENERAL`.

- **It is one adjacent swap from Stage C's ranking**, of `T3_ENGINEERING` and
  `ACCOUNT_MANAGER`, the hierarchy Stage C chose over the same pairs with
  their key in hand.
- **It ties Stage C's ranking on every hybrid corpus cell** and on `K-b`'s pairs.
  It differs on the pure pool and over the space, 0.5769 against 0.5838 on the
  hybrid pool.

So on the hidden policy's pairs the model's own answers already imply nearly
the key's ranking. On the learned base they imply another: `ONCALL_ESCALATION`
above `SECURITY_INCIDENT`, and `SELF_SERVICE_DEFLECT` above `T2_TECHNICAL`.

### `M-d`'s baseline, and the readings on `K-b`'s pairs

What each ranking predicts of the model's pairwise answers, counted as `M-d`
counts them:

| ranking | learned base, of 1,479 | hidden policy, of 166 |
|---|---|---|
| Stage C | **1,190**, 0.8046 | 149, 0.8976 |
| revealed, learned base | 1,194, 0.8073 (published, §14) | 124, 0.7470 |
| revealed, hidden policy | 1,192, 0.8059 | 149, 0.8976 |

- **`M-d` holds for an ask whose ranking predicts at least 1,190 of the
  1,479.** It is the median ask that is read.
- **The ranking that read the hidden policy's key predicts the model's
  learned-base answers within four of the model's own revealed ranking.**

On `K-b`'s 65 units, beyond the keyword over the space:

| | reading |
|---|---|
| the declarations, `K-b` | 0.5460 |
| revealed ranking, learned base | 0.5563 |
| Stage C's ranking, and the hidden policy's revealed ranking | 0.7219 |

**`M-e`'s line is the declarations' 0.5460.** The revealed ranking clears it by
0.0103, and Stage C's by 0.1759.

### What Stage A does not settle

Nothing in it is adjudicable. The rows need the rankings the model states,
which Stage B buys, and each step runs on Sergi's word:

1. The smoke run goes first: two asks, read before the session.
2. Then the session: twenty-four asks.
3. Each record is committed before the next step begins.

---

## Stage B

Sergi gave the go-ahead for each session on 2026-10-17, the smoke session's
first, and the session's after the smoke record was committed (§8).

**The smoke session passed and opens the session.** `ranking.ask --session
smoke`, 2026-10-17, with `PYTHONHASHSEED=0`, from the commit of *An erratum to
FINDINGS3.md §14* on a clean tree. The checks of §8 ran in order before any
call:

- **The key** was an API key OpenRouter accepts, not a management key.
- **`M-g1` to `M-g4` passed**, with the suite green at 1,738 tests.
- **Stage A's record held** the same presentations, digests and pass orders the
  checks rebuilt.

What came back, from presentations 1 and 2:

- **Both answers were valid rankings**, each in one attempt.
- **Every call carried `reasoning: {"effort": "none"}`, and no attempt spent a
  reasoning token.** The answers took 106 and 96 completion tokens of the 400
  allowed. The judge's budget, which the amendment to §1 of `PLAN_REUSE.md`
  found reasoning could spend, holds with the setting off.
- **Both finish reasons were `stop`**, normalised and native.
- **`provider` arrives, and it was not one provider.** The first call was served
  by Baidu and the second by GMICloud, under one model name. OpenRouter does not
  document the field. Each attempt also keeps its generation id, the documented
  route to the same fact. This is the first record of the project to carry a
  provider. The session's 24 calls will say how many providers one model name
  meets in one session, which is §5.8's trap counted rather than assumed.
- **The partial file was gone once the record was written.**

The record is [`ask_smoke.json`](ask_smoke.json). Its answers enter no row, and
none is read here.

**The pace.** The calls took 4.75 s and 13.43 s, 15 s in all. At that pace the
session's 24 calls take a few minutes, after the eight minutes of checks that
come first.

**The session ran in full, and every answer is a valid ranking.** `ranking.ask
--session session`, 2026-10-17, with `PYTHONHASHSEED=0`, from the smoke
record's commit on a clean tree. The same checks ran first: the smoke record
under this protocol, the key, `M-g1` to `M-g4` with the suite green at 1,738
tests, and Stage A's record.

- **24 asks, 24 valid rankings, each in one attempt.** That covers twelve
  presentations, each in both passes, in the passes' seeded orders. No call
  failed and none was retried.
- **No reasoning token was spent.** The answers took 97 to 112 completion tokens,
  104.5 at the median.
- **Every finish reason was `stop`**, normalised and native.
- **Two providers served one model name**: Baidu answered 18 calls and GMICloud
  6, three in each pass. `model` came back `deepseek/deepseek-v4-flash` on every
  call. So the session's answers come from two providers, and `M-a`'s two
  passes of one presentation need not come from the same one. Stage C reports
  that beside `M-a`.
- **The calls took 2.24 s at the median**, from 1.56 to 14.08 s, 89 s in all.
  The partial file was gone once the record was written.

The record is [`ask_session.json`](ask_session.json). Every row keeps its
presentation, its pass and position, the answer's text and its parsed
ranking, and each attempt's generation id, provider, finish reasons and tokens.

---

## Stage C — the five adjudications

**What was run.** `python3 -m ranking.score`, on 2026-10-17, with
`PYTHONHASHSEED=0`, from the session record's commit on a clean tree. `M-g1` to
`M-g4` passed again, with the suite green at 1,738 tests. It refused nothing:
the session record is under this protocol and behind Stage A's record. The
record is [`score.json`](score.json).

**The unit is one valid ask, and all 24 are valid**, so every row is read on
the median of 24: the mean of the twelfth and thirteenth values. Every value is
in the record.

| row | statistic | line | reading | the 24 asks | verdict |
|---|---|---|---|---|---|
| M-a | validity; `W − A` over the 28 queue pairs | ≥ 0.90; ≤ 0.05 | 1.0000; 0.0271, `W` 0.9702 and `A` 0.9432 | — | **holds** |
| M-b | the median score on `hibrido` · corpus test split 0 | > 0.4632 | **0.3367** | 0.2131 to 0.3698 | **refuted** |
| M-c | the same | ≥ 0.4824 | **0.3367** | the same | **refuted** |
| M-d | the median `predicts(r) − predicts(stage_c)`, over 1,479 answers | ≥ 0.00 | **−0.1724** | −0.3185 to −0.0663 | **refuted** |
| M-e | the median reading on `K-b`'s 65 units | > 0.5460 | **0.5496** | 0.4709 to 0.5642 | **holds, thin** |

**The drafter expected three holds and two refutations, and got two holds and
three refutations.** Four of the five verdicts went as expected. The miss is
`M-b`, the row §0 itself said was weakened by what the drafter had seen. The
drafter expected `M-c` to be refuted thinly, and it was refuted by 0.1457.

### What the model states

**Six distinct rankings in 24 asks, and one of them 14 times**:
`SECURITY_INCIDENT`, `ONCALL_ESCALATION`, `T3_ENGINEERING`, `T2_TECHNICAL`,
`T1_GENERAL`, `BILLING_SPECIALIST`, `ACCOUNT_MANAGER`, `SELF_SERVICE_DEFLECT`.
The Borda aggregate of the 24 is that ranking.

- **`SECURITY_INCIDENT` is first in all 24, and `SELF_SERVICE_DEFLECT` is last in
  all 24.** The variation is in the middle: where `ONCALL_ESCALATION` falls,
  and the order of the specialist queues among themselves.
- **Every one of the 24 `why` sentences names a priority**: "prioridad por
  criticidad", "por severidad y urgencia", "by severity and escalation path".
  The technical tiers come in escalation order, above the specialist queues,
  and deflection comes last.

**It is a priority order, and the question asked for an arbitration order.**
§2.1 put the pairwise judge's question to the model in general: two rules match
a ticket and send it to different queues, so which queue wins. The answer is the
other object, which §5.1 named as the trap. A priority order is not wrong as a
priority order. As the order that decides a contested ticket, it is what the
rows read.

### What it is worth as a lookup

| cell | born_at | blind mean | Stage C | revealed | **stated, median ask** | its percentile in the 40,320 |
|---|---|---|---|---|---|---|
| `hibrido` · corpus test split 0 | 0.4332 | 0.3670 | 0.4824 | 0.4693 | **0.3367** | 0.36 |
| `hibrido` · five-split mean | — | — | 0.4806 | 0.4675 | 0.3312 | — |
| `hibrido` · full corpus | 0.4285 | 0.3676 | 0.4805 | 0.4685 | 0.3345 | — |
| `hibrido` · space | 0.4257 | 0.3180 | 0.5838 | 0.5037 | 0.5157 | 0.89 |
| `puro` · corpus test split 0 | 0.5216 | 0.3215 | 0.4291 | 0.4131 | 0.2794 | 0.26 |
| `puro` · full corpus | 0.5115 | 0.3234 | 0.4285 | 0.4170 | 0.2825 | — |
| `puro` · space | 0.3148 | 0.2898 | 0.5756 | 0.4196 | 0.4993 | 0.88 |

The revealed ranking's figures are Stage A's. Stage C's ranking sits at the 0.93
percentile of the signed cell.

- **On the signed cell the stated ranking wins 335 cases of 995.** That is 96
  fewer than arrival order and 145 fewer than Stage C's ranking. **A ranking
  picked blind does better on average**: the stated one sits at the 0.36
  percentile of the 40,320.
- **Over the space it is good: the 0.89 percentile on the hybrid pool**, above
  the model's revealed ranking and below Stage C's. The surfaces differ in how
  often the top of the order decides. Half the space carries the security
  keyword and 71 of the corpus's 2,000 cases do. The stated ranking agrees with
  Stage C's at the top and disagrees in the middle, where the corpus is
  decided.

### What it states against what it does

**`M-d` is refuted by 17 points.** The median stated ranking predicts 935 of
the model's 1,479 declared answers, 0.6322. Stage C's ranking predicts 1,190 of
them and the model's own revealed ranking 1,194 (Stage A). On the hidden policy's
166 two-way answers the gap is −0.1446: 125 against Stage C's 149.

The stated rankings agree with the revealed one on 21 of the 28 queue pairs at
the median, and with Stage C's on the same 21. The disagreement is concentrated
where the pairwise answers are most one-sided:

- **`BILLING_SPECIALIST` against `T1_GENERAL`.** Pairwise, the model named
  `BILLING_SPECIALIST` 167 times and `T1_GENERAL` 13
  (`pair_judgement_1600.json`'s `revealed_hierarchy`). Asked for its ranking,
  it put `T1_GENERAL` above `BILLING_SPECIALIST` in 22 of 24 asks.
- **`SELF_SERVICE_DEFLECT` against `T1_GENERAL`.** Pairwise, the model named
  `SELF_SERVICE_DEFLECT` 113 times and `T1_GENERAL` 42. Asked for its ranking,
  it put `SELF_SERVICE_DEFLECT` last every time.

So what the model says the order is and the order its answers follow are
different orders. That is `PLAN_WHY.md`'s gap between what the proposer says and
what it does, reached at the level of the queues. Here the stated object is
worse than the done one: 0.3367 as a lookup against the revealed ranking's
0.4693.

### `M-e`, and the corpus beside it

On `K-b`'s 65 units, beyond the keyword over the space, the median stated
ranking reads 0.5496 against the declarations' 0.5460. **It holds by 0.0036,
and it is thin**: one ask, presentation 9 in pass 2, reads 0.4709. So on the
surface `K-c` was adjudicated on, its refutation survives a ranking the model
states, by a hair. A ranking that read no key still points those pairs no worse
than the declarations did.

**On the corpus the reading goes the other way.** On `K-e`'s 66 units the
stated ranking reads 0.5202, below the declarations' 0.5861 and Stage C's
0.6848. That is reported and adjudicates nothing. A reader who takes `M-e` for
*a truth-free ranking beats the declarations* should read both.

### `M-a`, and the providers

**The model states a total order every time, and the slot does not decide
it.** All 24 answers are valid. Two passes of one presentation agree on
0.9702 of the queue pairs, and asks of different presentations on 0.9432, a gap
of 0.0271 against a line of 0.05.

Two facts sit beside the row:

- **Every presentation was served by one provider in both passes**: three of
  them by GMICloud (2, 5 and 9) and nine by Baidu. So `W` is read within a
  provider, and part of `A` across two. This record cannot apportion the gap
  between the slot and the provider.
- **One provider, one presentation and temperature 0 still give two answers.**
  The two passes differ on five of the twelve presentations, including
  presentation 9 under GMICloud.

### What the verdicts say

- **Asking the model for its ranking does not buy the baseline.** On the cell
  `P-d` and `B-b` were read on, the ranking it states is worth less than
  arrival order and less than a blind draw. The model's competence at
  arbitrating queues is in its pairwise answers, not in what it states about
  them.
- **The erratum of 2026-10-16 stands without a remedy from this route.**
  Neither ranking the model gives, stated or revealed, reaches the 0.4824 of
  the ranking fitted with the key. Wherever that ranking stands as a rule, it
  still stands with a key behind it.
- **`K-c`'s refutation survives on its own surface, thinly**, and the corpus
  reading does not carry it.

### What Stage C does not settle

1. **Whether another question elicits the arbitration order.** The answer read
   the question as a priority question. A question with an example of two
   contending rules, or §2.1's pairwise question asked about a list of queue
   pairs, could elicit the other object. Calls, and a plan of their own.
2. **Whether the priority reading is the model's or the prompt's.** The system
   prompt says "gana la que va antes en el orden", and the answers explain
   themselves by criticality. These answers cannot separate the two.
3. **The provider.** Whether the slot gap, the five presentations whose passes
   differ, or the one ask that made `M-e` thin belong to a provider, 24 calls
   cannot say.
4. **One model, one prompt, one date, twenty-four asks**, as §12 declared.

---

## Files

```
results_ranking/sample.json      Stage A: the checks, the twelve presentations
                                 with their digests and the order of each pass,
                                 the five lines, the revealed rankings, Stage
                                 C's baseline
results_ranking/ask_smoke.json   Stage B's smoke session: two asks, every attempt
                                 with its provider, finish reasons and tokens
results_ranking/ask_session.json Stage B's session: twenty-four asks, twelve
                                 presentations in two passes, as the smoke's
results_ranking/score.json       Stage C: the five verdicts with every ask's
                                 value, and M-f
```
