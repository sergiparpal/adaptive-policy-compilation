# The ranking of the queues, asked of the model — findings

Record opened on October 17, 2026, under [`PLAN_RANKING.md`](../PLAN_RANKING.md).
Sergi signed §0 on 2026-10-17, before any figure below existed, in a commit of
its own: *PLAN_RANKING.md signed by Sergi*. Every record names in its `_env` the
commit of the branch it was written on. A rebase merge gives those commits new
hashes on `main` with the same trees. **This record owns every figure in it.**

**Stage A and the smoke session ran on 2026-10-17, and nothing is adjudicated
yet.** The five rows wait for the session's answers. The smoke session's answers
enter no row.

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

Sergi gave the go-ahead for the smoke session on 2026-10-17, and for nothing
beyond it. The session waits for its own go-ahead (§8).

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

---

## Files

```
results_ranking/sample.json      Stage A: the checks, the twelve presentations
                                 with their digests and the order of each pass,
                                 the five lines, the revealed rankings, Stage
                                 C's baseline
results_ranking/ask_smoke.json   Stage B's smoke session: two asks, every attempt
                                 with its provider, finish reasons and tokens
```
