# PLAN_RANKING — the ranking of the queues, asked of the model

> **[CLOSED 2026-10-17] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-10-17, before any figure of the plan existed. All five rows were
> adjudicated the same day, on the median of 24 valid asks. **`M-a` holds;
> `M-b`, `M-c` and `M-d` are refuted; `M-e` holds, thinly.** `M-f` is reported.
> **The figures are owned by
> [`results_ranking/FINDINGS_RANKING.md`](results_ranking/FINDINGS_RANKING.md)**,
> and no result is to be read off this file; the scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-10-17. The line is kept
> unedited and this banner is its correction. The banner touches no line of §0,
> adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-10-17, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**This plan exists because a baseline that beat almost everything was never
asked of the model.** A total order over the eight queues induces an order over
the 577 rules of rung 1 — sort each rule by the rank of its action, reading no
condition, no extension and no subsumption. That family of 40,320 orders has
been the strongest free competitor in the project:

- it cleared `P-d`'s threshold at zero calls, which is what took the power away
  from a hold of that row (`FINDINGS3.md` §7);
- it tied the order compiled from 1,600 paid pairwise answers, which is how
  `B-b` came to be refuted by 0.0020 (`FINDINGS3.md` §11);
- it pointed the pairs of `PLAN_BLIND.md` better than the proposer's own
  declarations, which is how `K-c` and `K-e` came to be refuted
  (`FINDINGS_BLIND.md`).

**The ranking used in all three is Stage C's, and it read the answer key.** It
was chosen by brute force over the 40,320 permutations with the hidden policy's
labels in hand, over that policy's pairs
([`rung2/pair_judgement_baselines.py`](rung2/pair_judgement_baselines.py)). It
reads no rule and no label of the base it is applied to, and that is all: the
erratum of 2026-10-16 in `FINDINGS_BLIND.md` and in `IDEAS.md` says so, against
the sentence that had called it truth-free. **A deployed system cannot get that
ranking.** It has to get one from a source that reads no truth, and the model
itself is such a source. Nobody has asked it.

[`IDEAS.md`](IDEAS.md) carries this as *Ask the model for its ranking of the
queues*, under *What the outside reading of October 2026 proposes and nothing
has run*. It is also the open end of the erratum in that file's `PLAN_BLIND.md`
section — *the ranking as the rule for which edge yields* — and it reaches
`PLAN_WHY.md`'s question from another side.

**The question, in its cleanest form.** Asked for one total order over the eight
queues and nothing else, does the model state the ranking it has been measured
against, and the one it answers pair by pair as if it held?

**What is asked.** One question, with no ticket, no rule and no description of
any queue, answered a few times with the queues presented in permuted orders,
because the presentation slot decides some pairwise answers
(`PLAN_PRIMACY.md`). Cents.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic, its denominator and its cell here, before any
call.** There are two surfaces and two pools in this project and they never
chain (`STATUS.md`, *Before reading any figure*). **The adjudicated cell of
`M-b` and `M-c` is the `hibrido` pool at corpus test split 0** — the cell `P-d`
and `B-b` were read on, which is the only reason to prefer it. The `puro` pool,
the five-split mean, the full corpus and the exhaustive space are reported for
every row that has them (`M-f`), and no row is adjudicated on more than its own
cell.

**Which side had a label, for every reference this plan compares against.** The
lesson of §6 of `PLAN_ILP.md`, checked against the code and not recalled:

| reference | fitted on | reads a label? |
|---|---|---|
| `best` over the 40,320 | the cell it is read on | **yes**, the cell's own labels. A winning ticket, not a level |
| `stage_c` | the **hidden** policy's 170 pairs | **yes**, that policy's answer key — not this base's |
| `mean` over the 40,320 | nothing | no. This is the level a ranking picked blind is worth |
| `born_at` | nothing | no. Arrival order, the floor every order is read against |
| **the stated ranking**, this plan's | nothing | **no.** One question, no ticket, no rule, no label |

**The unit of adjudication is one answer, not an aggregate.** The claim is what
*one question* buys, so `M-b` to `M-e` are read on the **median over the valid
asks**, and the mean, the spread, the per-presentation table and the Borda
aggregate of all asks are reported beside them (`M-f`). An aggregate chosen
after the answers are in would be a fit; a median of single answers is what a
deployment would get from asking once.

**When a row has no value, what *thin* is, and at what precision a read line is
met.** Settled here and not in the scorer, which is where `PLAN_AUTHORSHIP.md`'s
`E-c` lost its verdict.

- **With fewer than four valid asks, `M-b` to `M-e` are unadjudicable**, and the
  record says so. `M-a` is adjudicated whatever the count.
- **A verdict is labelled *thin*** when at least one valid ask falls on the other
  side of its line from the median. The label does not change the verdict.
- **A reading compared with a line read from a record is compared at the six
  places that record publishes.** On the signed cell one case is 1/995, about a
  thousand units of the sixth place; on `K-b`'s units a reading is a mean of 65
  shares.
  So the rounding decides nothing, except that a reading equal to its line stays
  equal: an ask that states Stage C's own order meets `M-c` exactly, and an ask
  whose reading on `K-b`'s units equals the declarations' does not meet `M-e`.
  Neither turns on a margin the rounding invents.

**Notation.**

- **An ask** is one question: the eight queue names in one presentation order,
  answered once.
- **A stated ranking** `r` is an ask's answer: a list of the eight queue names.
- **An ask is *valid*** iff its answer is a permutation of exactly the eight
  queues of `harness.domain.ACTIONS` — no omission, no repetition, no invented
  name, no tie. Whitespace around a name is stripped and nothing else is
  forgiven: a lower-cased name is invalid. Invalid asks are counted, published
  with their raw text and excluded, never repaired.
- **`score(r, cell)`** is the accuracy of the order `r` induces over the 577
  rules on that cell, by `rung3.queue_hierarchy_floor.hierarchy_order` and
  `rung3.floor_by_pool.floor`. The intra-class tie-break provably cannot move
  it, and `M-g1` checks that it does not.
- **`predicts(r, answers)`** is the share of the model's own pairwise answers
  that `r` names: of the two queues on offer, the one `r` ranks higher.

| id | claim | statistic, with its denominator and cell | band | refuted by |
|---|---|---|---|---|
| **M-a** | **The model states a total order, and the presentation slot does not decide it.** The instrument row | Two clauses, both must hold. *Validity*: the share of the asks that are valid, over all asks of the session. *Slot*: `W − A`, where `W` is the mean agreement in pairwise direction between the two passes of the **same** presentation, over the 28 queue pairs, and `A` the same between asks of **different** presentations | *Validity* **≥ 0.90**; *slot* **≤ 0.05** | *Validity* **< 0.90**; *slot* **> 0.05** |
| **M-b** | **One free question reaches what 400 paid calls did not.** The stated ranking clears the threshold `P-d` was signed against | the median over valid asks of `score(r, hibrido · corpus test split 0)`, against that cell's `born_at` floor plus `P_D_MARGIN`, both **read** from [`results3/queue_hierarchy_floor.json`](results3/queue_hierarchy_floor.json) and not retyped | **> 0.4632** | **≤ 0.4632** |
| **M-c** | **And it reaches the ranking that read the answer key.** One question against brute force over 40,320 with the labels in hand | the same median, against that cell's published `stage_c`, read from the same record | **≥ 0.4824** | **< 0.4824** |
| **M-d** | **What it states is what it does.** Its stated ranking predicts its own pairwise answers at least as well as a ranking fitted on the hidden policy's key does | `predicts(r, ·) − predicts(stage_c, ·)` over the answers of [`results2/pair_judgement_1600.json`](results2/pair_judgement_1600.json) that are valid and name one of the two queues on offer; `r` the median ask by that statistic | **≥ 0.00** | **< 0.00** |
| **M-e** | **`K-c`'s refutation does not rest on a ranking that read a key.** A ranking the model stated, reading no truth, still points `PLAN_BLIND.md`'s pairs better than the proposer's declarations did | the median over valid asks of that ask's reading of `blind.rows.direction` on `K-b`'s units — beyond the keyword, over the space, each older rule counted once, 65 units — against the declarations' published reading, read from [`results_blind/score.json`](results_blind/score.json) | **> 0.5460** | **≤ 0.5460** |
| **M-f** | *Reported, not adjudicated.* **What the drafter could not band** | every ask's answer and `why` sentence; the per-presentation table; the stated rankings' percentile in the 40,320 of each cell; every cell of `M-b` to `M-e` on the `puro` pool, the five splits, the full corpus and the space; the Borda aggregate of the asks and its own scores; the revealed ranking of the paid records beside the stated one, queue pair by queue pair, and what it scores as a lookup on every cell; `predicts` on the hidden policy's 170 pairs; `M-e` on the corpus cell; `call_attempts` per ask, with provider and both finish reasons | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-17)**

**Why `M-f` cannot carry a band.**

- **The percentiles, the other cells and the Borda aggregate** are functions of
  answers that do not exist yet, and the drafter has no quantity to bet on for
  any of them that is not already `M-b` to `M-e` on its own cell. The standing
  note in `IDEAS.md` is that this drafter's arguments for a quantity carrying
  across surfaces lose (`H-d`), and betting `M-b` on four cells would be that
  argument four times.
- **The `why` sentences** are `PLAN_WHY.md`'s instrument, and that plan froze
  its codebook on a development set before coding anything. There is no
  development set here — the session is 24 answers — so they are reported and
  not coded.
- **`call_attempts` has no claim attached.** It is recorded because every paid
  writer since 2026-10-16 records it (`harness/call_record.py`), and because
  `V-a`'s drift could not be apportioned for the lack of it.

**What the drafter had already seen, declared so that the signature is
auditable.** This is the weak point of this plan and it is stated first rather
than last.

- **Everything `STATUS.md`, `IDEAS.md`, `FINDINGS3.md` §§7-15,
  `FINDINGS_BLIND.md` and the plans of the pairwise threads publish.** That
  includes every figure of §3 below.
- **`results3/queue_hierarchy_floor.json` in full**: the floor, `stage_c`,
  `best`, `mean`, `sd` and `worst` of all fourteen (pool, surface) cells, under
  both tie-breaks.
- **`results2/pair_judgement_baselines.json` in full**: the 170 pairs, the
  model's 0.8824, the hierarchy family's 0.9471 best and 0.5000 mean, the
  decomposition into the 161 a hierarchy answers and the 9 it cannot, the five
  reversible queue pairs, and the model's own consistency — 27 queue pairs
  answered, 9 of them not always the same way.
- **`results_blind/score.json`'s rows and its `directions` block**: `K-b`'s
  0.546026 on 65 units, the Stage C ranking's 0.721911 on the same units,
  `K-e`'s 0.586147 and the ranking's 0.684818 on 66 units.
- **`results2/pair_judgement_1600.json`'s `revealed_hierarchy` block**, which
  the drafter read on 2026-10-17 while drafting: **the per-queue-pair counts of
  which side the model named, 25 queue pairs, 15 of them varying, constant on
  0.40**. **This is the part a reader should weigh.** It does not give the
  stated ranking, which nobody has asked, and it does give the drafter the shape
  of the model's revealed preferences on the learned base — that `SECURITY_INCIDENT`
  won every pair it appeared in, that `ONCALL_ESCALATION` won nearly every one,
  and that `SELF_SERVICE_DEFLECT` was named over `T1_GENERAL` 113 times against
  42. Two of the three queue positions where Stage C's order is not common sense
  are therefore not a surprise to this drafter. **No prediction rate was
  computed from that block**, and Stage A computes every one of them after the
  signature, under `M-g3`, so that none of them can inform a band.
- **The scorer and the two instruments, read as code**:
  `rung3/queue_hierarchy_floor.py`, `rung3/floor_by_pool.py`,
  `blind/rows.py`'s `direction` and `stage_c_names`, and
  `rung2/pair_judgement.py`'s client and system prompt.

**Not seen, because nobody has computed it**:

- any ranking the model states, in any presentation;
- what any ranking other than Stage C's scores on any cell of
  `queue_hierarchy_floor`, the published `best`, `mean` and `worst` apart;
- what any ranking predicts of the model's own pairwise answers, Stage C's
  included, on the 1,600 or on the 170;
- `blind.rows.direction` under any `predict` other than the three
  `results_blind/score.json` publishes.

**[NOTE 2026-10-17, writing the package, before any signature] One *not seen*
item was published, and the drafter had not read where.** The bands were
drafted from `STATUS.md`, `IDEAS.md` and the records listed above, without
reading `FINDINGS3.md` §§14-15 themselves; the first bullet of *already seen*
claimed more than had been read. Writing `ranking/`, the drafter read them.
They publish two things this plan's rows touch:

- **The model's revealed ranking**: Copeland over the 1,479 declared answers of
  the learned base, by `rung3/edge_dropping.py`, stored in
  `results3/edge_dropping.json`: `ONCALL_ESCALATION`, `SECURITY_INCIDENT`,
  `T3_ENGINEERING`, `BILLING_SPECIALIST`, `ACCOUNT_MANAGER`,
  `SELF_SERVICE_DEFLECT`, `T2_TECHNICAL`, `T1_GENERAL`.
- **What it predicts of those answers**: 1,194 of 1,479, the record's
  `consistent` filter.

So the third *not seen* item is false for that one ranking, and `M-g3` now
reproduces the 1,194 as its check on `predicts`. Nothing else in the list
moves. **What §14 does not publish is what that ranking scores as a lookup.**
It publishes what a perfect follower of it scores when 1,479 answers are
compiled as edges, 0.4402 and 0.4302 on the signed cell, which is the channel's
object and not this family's. And its sentence *the same ranking applied as a
lookup over all 577 rules scores 0.4824* gives Stage C's figure: the record
and the code both call it `stage_c` (`edge_dropping.py`'s
`QUEUE_RANKING_REFERENCE`, "stage_c row"). Stage A computes the revealed
ranking's lookup score after the signature, and `FINDINGS_RANKING.md` owns the
erratum §14 then needs, if it needs one. Stage C's agreement with the 1,479
answers is computed nowhere. The bands and the expectation below were written
before this note and are left as they were.

**What the drafter expects, written down so the scoreboard can score it.**
**Three hold and two are refuted.** The drafter trusts `M-e` most, then `M-b`,
then `M-a`, then `M-c`, then `M-d`.

- **`M-a` holds.** The question has one obviously ordered end — a security
  incident over a deflection — and the stated orders should agree there whatever
  the presentation. The clause at risk is the slot's: `L-a` and `L-b` found the
  slot deciding pairwise answers, and here the model writes the whole list, so
  the first-named queue may anchor the top of it. A refutation of this clause
  would be the more interesting outcome and it would not void `M-b` to `M-e`,
  which are read on the median ask either way.
- **`M-b` holds.** The revealed block says the model puts both rare queues at
  the top and `SELF_SERVICE_DEFLECT` above `T1_GENERAL`, which is most of what
  separates Stage C's order from a blind draw. The drafter has seen that, and
  says so above.
- **`M-c` is refuted, thinly.** Stage C's order is the maximum over 40,320 taken
  with a key, and its middle — `ACCOUNT_MANAGER` over `T3_ENGINEERING` over
  `BILLING_SPECIALIST` over `T2_TECHNICAL` — is where common sense has least to
  say. One misplacement in the middle costs a few points, and the gap between
  `stage_c` and `best` on the signed cell is 0.0442.
- **`M-d` is refuted.** This is `PLAN_WHY.md`'s gap: the model's revealed
  preferences vary on 15 of 25 queue pairs, so no total order fits its answers,
  and a stated order has no reason to be the best-fitting one. Stage C's order
  is not fitted to those answers either, but it is fitted to the truth, and on
  the clean pairs the model agreed with the truth 0.8824 of the time. A hold
  here would say that what the model states is a better account of what it does
  than a ranking of the truth is, which would be a result worth the plan on its
  own.
- **`M-e` holds.** `K-c` was refuted by 0.1759, which is a wide margin for a
  substitution to close, and the ranking's advantage there comes from the same
  two queues the revealed block puts at the top.

**The drafter's record argues against part of that.**

- **The scoreboard.** On `STATUS.md`'s, 30 of 74 adjudicated rows were refuted.
- **The last plans.** `PLAN_SCREEN.md`'s drafter expected four holds and got
  three; `PLAN_BOUND.md`'s expected four and got three; `PLAN_FIDELITY.md`'s
  expected five and got four; the ILP thread's expected four and got one.
- **This plan expects three of five**, which is the first draft of this drafter's
  that expects more refutations than one. That is not a virtue: it is what
  *already seen* above buys, and a reader should discount `M-b` accordingly.
- **No band here was set on a development set**, unlike `PLAN_WHY.md`'s and three
  of `PLAN_SCREEN.md`'s. Three of the five lines are figures published in records
  that own them, read by the code rather than retyped; the other two are 0.90,
  0.05 and 0.00, which are the claims' own edges.

**How the rows read together.**

- **`M-b` and `M-c` hold.** A free question buys the whole baseline. Every row of
  this project that was refuted by Stage C's ranking keeps its verdict, and the
  erratum of 2026-10-16 is answered: a deployment can have that ranking for one
  call. The project's strongest free competitor becomes a competitor it can
  actually field.
- **`M-b` holds and `M-c` is refuted.** The model knows most of the ranking and
  not the part the key supplied. The gap between the two is then exactly the
  price of the answer key, measured for the first time.
- **`M-b` is refuted.** The ranking the project has been measuring against is
  not one the model has; it was the key's, and the three refutations it produced
  rest on a baseline no deployment could field. That does not move `P-d`, `B-b`,
  `K-c` or `K-e`, which are signed and adjudicated — it moves what they mean,
  and `STATUS.md` would have to say so beside each.
- **`M-d` holds.** What the proposer states and what it does agree at the level
  of the queues, which is the opposite of `PLAN_WHY.md`'s finding at the level of
  the sentence beside each answer.
- **`M-e` is refuted.** `K-c`'s refutation did rest on the key. The declarations
  beat every ranking the model can state, and *beyond the keyword the
  declarations are a coin's* becomes a statement about Stage C's ranking rather
  than about rankings.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.**

- **`results/llm_run.json`** — rung 1's 577 rules, the base every score here is
  computed over. Read-only, hard rule 4.
- **`results2/pair_judgement_1600.json`** and
  **`results2/pair_judgement_hidden.json`** — the model's pairwise answers, 1,600
  on the learned base and 170 clean ones on the hidden policy. `M-d` reads them.
- **`results_blind/`'s records** — `M-e`'s pairs and units.
- **`results3/queue_hierarchy_floor.json`** — the family's floors, `best`, `mean`
  and `stage_c`, which three of the five lines are read from.

**What is bought: one question, asked 24 times.** Twelve presentation orders,
each asked twice, plus a smoke run of two asks. Fewer than thirty calls at
`deepseek/deepseek-v4-flash`, which is cents — the cheapest paid stage of any
thread in this project.

**What is not bought.** No ticket is shown, no rule is shown, no queue is
described and no policy is given. A prompt that described the queues would be
the authority channel of `IDEAS.md`, which is a different plan with a different
result (§12.1).

---

## 2. The choices that have to be made at signature time

Each is the drafter's recommendation, and each is Sergi's to overrule. A change
to any of them is a change to §0 and belongs in the same signed commit.

### 2.1 The semantics of the question — the drafter recommends arbitration

A ranking elicited as *priority* and a ranking elicited as *who wins when two
rules disagree* need not be the same object, and only the second is what the
scorer applies. **The question is therefore the pairwise system prompt's
question asked once in general**: two rules of the manual match a ticket and
send it to different queues, neither contains the other, so which queue wins —
for every pair at once. It names the eight queues and nothing else, as
`rung2/pair_judgement.py`'s system prompt does.

The alternative — *rank these queues by priority* — is a question about the
domain rather than about arbitration, and it would make `M-d` compare two
different questions. It is worth asking some day; it is not this plan.

### 2.2 How many asks — the drafter recommends twelve presentations, twice

Twelve is enough for `M-a`'s two agreement rates to mean something over 28 queue
pairs and small enough to stay in the cents. **Presentation 1 is
`harness.domain.ACTIONS`'s own order**, the one every prompt in the tree has
used, so that one ask is comparable with the pairwise thread's conditions. The
other eleven are drawn at `PRESENTATION_SEED` and fixed in Stage A, before any
call.

### 2.3 The unit — the drafter recommends the median ask

Stated in §0: the median over valid asks, with the Borda aggregate reported.
Adjudicating on an aggregate would answer a question nobody asked — what the
model's answers *pooled* are worth — and it would let a selection in.

### 2.4 The cell — the drafter recommends `hibrido` at corpus test split 0

Because `P-d` and `B-b` were read there, and because the signed lines of `M-b`
and `M-c` are those rows' own numbers. Everything else is `M-f`.

### 2.5 Whether `M-e` may substitute into a closed thread — the drafter says it reads, it does not re-adjudicate

`K-c`'s verdict is signed, adjudicated and published. `M-e` reads the same
instrument with a different `predict` and says what that verdict rests on.
`FINDINGS_RANKING.md` owns `M-e`'s figure; `FINDINGS_BLIND.md` gains a dated
note pointing at it, and `K-c` keeps its verdict whatever `M-e` does.

### 2.6 `PREDICTION.md`

Not touched. It is rung 1's long run and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Nothing here is recomputed by this plan except under `M-g1` and `M-g3`, which
check the recomputation against the record rather than publishing it again.

**The hierarchy family over rung 1's 577 rules** —
[`results3/queue_hierarchy_floor.json`](results3/queue_hierarchy_floor.json),
published by [`FINDINGS3.md`](results3/FINDINGS3.md) §7. `born_at` floors are
read from [`floor_by_pool.json`](results3/floor_by_pool.json), which owns them.

| cell | `born_at` | `+0.03` | `stage_c` | `best` | `mean` |
|---|---|---|---|---|---|
| `hibrido` · corpus test split 0 | 0.4332 | **0.4632** | **0.4824** | 0.5266 | 0.3670 |
| `hibrido` · space | 0.4257 | — | 0.5838 | 0.5997 | 0.3180 |
| `puro` · corpus full | 0.5115 | — | 0.4285 | 0.4995 | 0.3234 |
| `puro` · space | 0.3148 | — | 0.5756 | 0.6058 | 0.2898 |

The `puro` row is why no row is adjudicated there: over the corpus the whole
family, `best` included, is below arrival order.

**The compiled orders this ranking was compared with** —
[`FINDINGS3.md`](results3/FINDINGS3.md) §§8 and 11. The 400-call declared order
scored 0.4080 on the signed cell (`P-d` refuted, below the floor); the 1,600-call
order scored 0.4804 against the ranking's 0.4824 (`B-b` refuted by 0.0020).
§14 of the same record narrows what `B-b` means and moves no figure.

**The pairwise answers** —
[`results2/pair_judgement_baselines.json`](results2/pair_judgement_baselines.json),
published by [`FINDINGS2.md`](results2/FINDINGS2.md), Stage C. On the hidden
policy's 170 clean pairs the model scored 0.8824; the best of the 40,320
hierarchies 0.9471 on 161 of them, the mean 0.5000. Of the 27 queue pairs the
model answered, 9 were not always answered the same way.
[`pair_judgement_1600.json`](results2/pair_judgement_1600.json)'s
`revealed_hierarchy` reports 25 queue pairs on the learned base, 15 varying.

**`PLAN_BLIND.md`'s pairs** —
[`results_blind/score.json`](results_blind/score.json), published by
[`FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md). Beyond the keyword, over
the space, on 65 older rules counted once: the declarations read 0.546026 and
Stage C's ranking 0.721911, so `K-c` read −0.175885. On the corpus, 66 units,
0.586147 against 0.684818.

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` for the eight queue names and touches nothing under
   `harness/` but `call_record.py`'s installed wrapper. If a frozen file has a
   bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** The asks are sequential, and the order of a record is
   part of it.
4. **Seed 17, no regeneration.** Every record under `results/`, `results2/`,
   `results3/` and `results_blind/` is read-only.
   `harness/record_guard.py` guards this plan's paid record, and the flag that
   overrides it is not typed without Sergi asking.
5. **Do not adjust the prompt or the schema** once the smoke run has been read.
   The question is fixed in Stage A and pinned by a test.
6. **If the numbers come out badly, report them.** A stated ranking that scores
   below the blind mean is a result.
7. **The API key goes in the environment.** Load it without printing it, check it
   by its length, and read it off OpenRouter's key endpoint as an API key and not
   a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`rung3/`, `rung2/` and `blind/` are called by this plan and not edited**, as
   `overlap/` calls `authorship/`. The scorer is
   `rung3.queue_hierarchy_floor.hierarchy_order` with `rung3.floor_by_pool.floor`;
   the pools come from `rung3.order_search.build_tables` and
   `rung3.order_search_ls.space_pools`, never rebuilt here (`CLAUDE.md`'s note on
   rung 3's hybrid pool); the prediction instrument is `blind.rows.direction` with
   this plan's `predict`; the revealed ranking is `rung3.edge_dropping`'s
   `revealed_ranking`; the client is `rung2.pair_judgement.Judge`'s settings —
   model, temperature, maximum tokens and retries — imported, **with reasoning
   off**, `PLAN_REUSE.md`'s `REASONING`, imported from where its amendment of
   2026-09-30 put it. The judge never sent that setting, because in August it
   did not need to: the hosted model has reasoned by default since, and
   reasoning tokens count against the judge's 400. A reimplementation of any of
   them would make these figures incomparable with the records they are read
   against.
B. **No module of this plan imports the oracle**, and the question is built from
   `harness.domain.ACTIONS` alone. Every label `M-d` and `M-e` need is read from a
   committed record.
C. **The record carries `_env`, the model, the temperature and `call_attempts`.**
   Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff. Three of the five lines are
   read from the records that own them, so that no figure of this project gets a
   second home in Python.
E. **What the model writes beyond its ranking is recorded and never executed.**

---

## 5. Known traps

**5.1 — The elicited order and the scored order are two objects.** The scorer
applies a ranking as *who wins a contested ticket*. §2.1 fixes the question to
ask exactly that. A reader who finds the stated order odd as a *priority* order
is reading it as the other object.

**5.2 — Position, label and the order of the names were one variable in the
pairwise answers** (`FINDINGS_PRIMACY.md`). Here they come apart: the answer is a
list, so no slot carries a label, and the only presentation variable is the order
the eight names are offered in. That is what `M-a`'s slot clause measures, and it
is a floor on the effect rather than its size, because a single question cannot
separate the first-named queue from the first-ranked one.

**5.3 — Two dates in one comparison.** `M-d` sets a ranking stated in October
2026 against answers given in August 2026, and `M-e` against pairs answered in
October. The standing note in `IDEAS.md` is that this drafter's arguments for
continuity across dates lose (`V-a` refuted). **This plan does not argue
continuity**: it measures what today's model states against what the record
holds, and `M-f` publishes `call_attempts` so that a later plan can apportion a
drift this one cannot.

**5.4 — The intra-class tie-break cannot move a score, and that is a proof.**
Under a class-grouped order the winner of a case is the first matching rule,
which belongs to the highest-ranked action among those of the rules that match
it, and every rule in that class carries that action. `M-g1` computes both
tie-breaks and refuses if they disagree, as `gate_tiebreak_irrelevant` does.

**5.5 — `best` is a winning ticket and `mean` is the level.** The maximum over
40,320 was taken with the cell's labels in hand. No row is read against it; it
bounds the family, and the percentile in `M-f` is reported for the same reason.

**5.6 — A ranking's score is not a rule's score.** This family reads which queue
a rule sends a ticket to and nothing else. It is strong on `hibrido`, where
subsumption has already pruned the pool and what is left is mostly *which
action*, and worse than arrival order on `puro` over the corpus. §3's table
carries both.

**5.7 — Invalid answers.** A tie, a missing queue, a repetition, an invented name
or unparseable JSON makes an ask invalid. The count, the raw text and the
`finish_reason` of every one are published. If validity falls below 0.90, `M-a`
is refuted and `M-b` to `M-e` are still read on the valid asks, with their count
beside them; below four valid asks they are unadjudicable and the record says so.

**5.8 — The model can change under its name.** OpenRouter routes a name to
providers and this plan pins none, as no plan in this project has.
`call_attempts` keeps the generation id, the provider and both finish reasons.

**5.9 — `M-e` substitutes a ranking into a closed thread's instrument.** It reads
`blind.rows.direction` with a different `predict` on the same rows. It
re-adjudicates nothing (§2.5), and the 65 units are 65 older rules, not 65
independent pairs: `O-c`'s lesson is that a rate over declared edges can rest on
one declaration, which is why `M-f` publishes the reading by declared winner and
the largest unit beside it.

**5.10 — One question is cheap and one question is one draw.** Twenty-four asks
of one question are not twenty-four questions. Everything this plan says about
the model's ranking is about one prompt, at one temperature, on one date.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

- **M-g1 — The scorer reproduces the record.** Blocking in the sense of
  `harness.ceiling_check`: it measures the instrument before the instrument
  measures anything else.
  - `python3 -m unittest discover` is green.
  - For every cell this plan reads, `hierarchy_order` and `floor`, re-run in
    memory over `results/llm_run.json`, give back
    `results3/queue_hierarchy_floor.json`'s `stage_c`, `best`, `mean` and
    `worst` to the digit, and `floor_by_pool.json`'s `born_at`.
  - Both tie-breaks agree on every cell.
  - Floats are compared with a tolerance, and the suite runs on 3.10 before this
    gate is pushed: on 3.10 `V-g1` refused a record 3.12 had written for a unit
    in the last place.
- **M-g2 — The question reads nothing but the eight names.**
  - Every built question contains the eight queue names of
    `harness.domain.ACTIONS`, each exactly once, and no other queue name.
  - It contains no ticket, no rule, no condition, no label and no description of
    any queue. The check is on the built string, against the attribute names and
    values of `harness/domain.py` and against every rule id of
    `results/llm_run.json`.
  - **Teeth.** Changing one presentation's order moves that question's digest,
    and no two presentations share a digest.
  - The twelve presentations are presentation 1 = `ACTIONS` and eleven draws at
    `PRESENTATION_SEED`, reproducible from the seed alone.
- **M-g3 — The prediction and substitution paths reproduce.**
  - **The populations are the records' own.** The learned base's declared
    answers, by `rung2.pair_judgement.classify_learned`, are 1,479: the record's
    own `declared` count, 1,600 rows less the 121 without an edge
    (`FINDINGS3.md` §11's erratum: 117 parse failures and 4 that parsed without
    an action). The hidden policy's two-way answers are 166: its 170 less its 4
    parse failures. No pair offers one queue twice, and no answer names a
    queue not on offer.
  - `rung2.pair_judgement.revealed_hierarchy` over those rows gives back the
    record's `revealed_hierarchy` block, 25 queue pairs and 15 varying, and
    `rung3.edge_dropping.revealed_ranking` gives back `edge_dropping.json`'s
    revealed ranking and its Copeland scores.
  - **`predicts`, applied to that revealed ranking, gives back the 1,194 of
    1,479** `edge_dropping.json` keeps as `consistent`. It is the only rate of a
    ranking over these answers that any record publishes, and **the only one
    the dry run computes**: what Stage C's ranking predicts of them is Stage A's.
  - Over the edge rows `results_blind/score.json` stores, `blind.rows` gives
    back that record's `directions` on both keys, for the declarations, for
    Stage C's ranking and for the newborn rule: 0.546026 on 65 units and
    0.586147 on 66 for the declarations, `K-b`'s and `K-e`'s verdicts, and
    0.721911 and 0.684818 for Stage C's ranking. And the `predict` this plan
    builds from a ranking names the rule `blind.rows.stage_c_names` names on
    every row, when the ranking is Stage C's.
- **M-g4 — The signature**, §10.

---

## 7. Stage A — the questions and the free readout (free, gated)

**Deliverable.** `ranking/sample.py` → `results_ranking/sample.json`.

- **`M-g1` to `M-g3`.**
- **The twelve presentations**, with their digests, at `PRESENTATION_SEED`.
- **The references**, read from the records that own them: the five lines of §0,
  of which three are read and two are the claims' own edges.
- **The revealed ranking of the paid records.** On the learned base it is
  `rung3/edge_dropping.py`'s, Copeland over the 1,479 declared answers,
  recomputed under `M-g3` rather than redefined. On the hidden policy's pairs
  it is the same Copeland over the 166 two-way answers. Each comes with its
  queue pairs, what it predicts of both sets of answers, its reading on `K-b`'s
  pairs, and **what it scores as a lookup on every cell**, which no record
  computes. **This is computed after the signature and not before**, which is
  the whole reason the free stage is gated: the revealed ranking's lookup score
  is the closest thing to `M-b`'s answer that exists without paying, and knowing
  it would inform `M-b`'s and `M-c`'s lines. It is also what settles §14's
  sentence (§0, the note of 2026-10-17).
- **What Stage C's ranking predicts of both sets of answers**, `M-d`'s baseline,
  beside its published scores and readings.
- **`M-f`'s free half.**

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `ranking/ask.py` → `results_ranking/ask_smoke.json`, then
`results_ranking/ask_session.json`.

1. `--dry-run` runs `M-g1` to `M-g3` and stops. It never builds the client.
2. `refuse_unsigned` before the client is constructed. No flag skips it.
3. `reuse.run.key_check`: an API key OpenRouter accepts, and not a management
   key. A 200 alone proves nothing.
4. **The smoke run**, two asks, under its own name, read before the session —
   for the parse, for `finish_reason`, and for whether `provider` arrives, which
   OpenRouter does not document.
5. **The session**, 24 asks, sequential, pass 1 then pass 2, each pass in its own
   order at `PRESENTATION_SEED`.
6. Answers are appended to a git-ignored partial file as they arrive and the same
   command resumes there. Five failed calls in a row stop the session without
   recording them: an outage is not answers.
7. `harness/call_record.py`'s recorder is installed, each ask keeps its
   `call_attempts`, and `tests/test_call_record.py` is taught this call site.

## 9. Stage C — scoring, and the five adjudications (free)

**Deliverable.** `ranking/score.py` → `results_ranking/score.json`.

- **`M-a`** from the asks alone: validity, and `W − A` over the 28 queue pairs.
- **`M-b` and `M-c`**: every valid ask scored on every cell, the median on the
  signed one, the percentile in the 40,320 reported.
- **`M-d`**: `predicts` on the 1,600, with the 170 beside it.
- **`M-e`**: `blind.rows.direction` with each valid ask's ranking as `predict`,
  and the median of the readings.
- **`M-f`** in full.
- **The verdicts**, each against its line, with *thin* and *unadjudicable* as
  §0 defines them.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `ranking/sample.py` and `ranking/score.py` spend nothing.
`ranking/ask.py` refuses before it constructs the client. **The free stages get
the gate because what it protects is not money** but the order of events (§7).

**The gate reads `PLAN_RANKING.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum rather than copied. `MIN_SIGNATURES = 1` today, §0's; an amendment
carries its own line and raises it. A gate that stopped at the first line would
report `ok` over an unsigned amendment, which is why `CLAUDE.md` says not to copy
`rung2/pair_judgement.py`'s gate into a plan that may carry more than one.

**Constants fixed here, before any figure exists, not to be tuned afterwards,
and pinned by tests:**

- **The client**, imported from `rung2.pair_judgement` and not retyped: `MODEL`,
  `TEMPERATURE`, `MAX_RETRIES`, `MAX_TOKENS`. And `REASONING`, imported from
  `reuse.plan` (§4, rule A).
- **The queues**, `harness.domain.ACTIONS`, imported.
- **The session.** `PRESENTATIONS = 12`; `PASSES = 2`; `SMOKE_ASKS = 2`;
  `PRESENTATION_SEED = 59`, distinct from every seed a closed thread uses (17 to
  20, 25, 41, 43, 47, 53, and values from 1000 up). It feeds two streams, one
  string seed each, as `screen/plan.py`'s `order_rng` does: one draws the eleven
  presentations, the other orders each pass. CPython seeds a string through
  SHA-512, so neither stream depends on `PYTHONHASHSEED`.
- **The limits.** `MIN_SIGNATURES = 1`; `MIN_VALID_SHARE = 0.90`;
  `MIN_VALID_ASKS = 4`; `MAX_CONSECUTIVE_FAILURES = 5`.
- **The lines of §0.** `M_A_MAX_SLOT_GAP = 0.05`, `M_D_MIN_GAP = 0.0` and
  `MIN_VALID_SHARE` are the claims' own edges. **`M-b`'s, `M-c`'s and `M-e`'s
  are read from the records that own them** — `queue_hierarchy_floor.json`'s
  floor plus `rung3.queue_hierarchy_floor.P_D_MARGIN`, the same record's
  `stage_c`, and `results_blind/score.json`'s `K-b` reading — and the record of
  this plan publishes the three values it read, so a reader can check them
  without running anything. `LINE_PLACES = 6`, the precision they are met at
  (§0).

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
ranking/__init__.py
ranking/plan.py        the gate and the constants of §10
ranking/question.py    the question, the presentations, validity, M-g2
ranking/instrument.py  the cells, a score, predicts, the revealed ranking, K-b's pairs
ranking/gates.py       M-g1 to M-g4
ranking/sample.py      Stage A: the presentations, the lines, the free readout
ranking/ask.py         Stage B: it spends
ranking/score.py       Stage C: M-a to M-e, and M-f
results_ranking/FINDINGS_RANKING.md
results_ranking/sample.json  ask_smoke.json  ask_session.json  score.json
tests/test_ranking.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `ranking` joins it in `harness/provenance.py`, and joins the
  oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP`.** `ranking/question.py` and `ranking/ask.py` join it.
- **The partial file**, `results_ranking/*.partial.jsonl`, joins `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call sites** of `tests/test_call_record.py` grow by one, or that test
  fails on a call site nobody classified.
- **The README's table of writers** gains its rows.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_ranking/` with `_env`, the model, the temperature
      and `call_attempts`, produced with `PYTHONHASHSEED=0`.
- [ ] `M-g1` to `M-g4` passed before any record was written. The key check and
      the smoke run came before the session, and the smoke record was committed
      before the session began.
- [ ] The plumbing of §10, and tests pinning the constants, the gate, the
      presentations and their digests, the three lines read from their records,
      the leak checks of `M-g2` with their teeth, the unchanged request, and the
      arithmetic of §0; the whole suite green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, its pool and its denominator.
- [ ] `results_ranking/FINDINGS_RANKING.md` owns every figure, with a dated
      erratum wherever it corrects something already published — including this
      plan's §0 *already seen* if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `M` thread; *What is open* gains or
      loses what this plan settles.
- [ ] `IDEAS.md`: *Ask the model for its ranking of the queues* closed or
      narrowed, and the erratum's open end under `PLAN_BLIND.md` — *the ranking
      as the rule for which edge yields* — answered or narrowed. Whatever this
      plan opens, added.
- [ ] `FINDINGS_BLIND.md` gains a dated note beside its erratum pointing at
      `M-e`, and `K-c` keeps its verdict.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **Whether the model knows what the queues are for.** It is given eight bare
   names, as every prompt in this project is. A stated ranking that scores badly
   does not distinguish a model that lacks the knowledge from a prompt that never
   supplied it. That is the authority channel of `IDEAS.md`, with its three
   levels of manual, and it is a different plan.
2. **Whether a ranking is the right instrument.** This family decides by the
   queue alone. The nine pairs of the hidden policy's benchmark that no queue
   ordering reaches, and `B-d`'s population on the learned base, stay out of
   reach of anything this plan measures.
3. **Where a ranking cannot answer.** `K-f` split the pairs into the queue pairs
   a ranking can and cannot answer. A ranking stated by the model is still a
   ranking, so it says nothing new on the second side.
4. **One model, one prompt, one date, twenty-four asks.**
5. **The two classes without correct rules.** A ranking that puts
   `ONCALL_ESCALATION` at the top changes nothing about a loop that never
   escalates one (`U-d`), and nothing about a model that names
   `ACCOUNT_MANAGER` on none of its held-out decisions (`PLAN_SCREEN.md`).
6. **The yielding rule.** If `M-e` holds, a ranking the model states can stand
   where Stage C's stood as *which edge of a cycle yields*. Whether it holds on
   other bases needs bases with cycles, which means new runs of the loop.
7. **What a ranking is worth under another engine.** Every score here is rung
   2's first-match over rung 1's base, on rung 3's pools. Rung 4's objective and
   the online loop are not in the rows.
