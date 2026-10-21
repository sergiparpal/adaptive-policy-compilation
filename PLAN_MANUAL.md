# PLAN_MANUAL — the authority channel: the policy, given to the proposer at three levels

> **[CLOSED 2026-10-21] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-10-21, before any figure of the plan existed. All six rows were
> adjudicated the same day: `G-a`, `G-c` and `G-d` on the median of five asks or
> three runs, `G-b` and `G-e` on the difference of two such medians, and `G-f`
> on two pooled rates. **`G-a`, `G-c` and `G-d` hold; `G-b` and `G-e` are
> refuted, thinly, and `G-f` is refuted.** `G-g` is reported. **The figures are
> owned by
> [`results_manual/FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md)**,
> and no result is to be read off this file; the scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-10-21. The line is kept
> unedited and this banner is its correction. The banner touches no line of §0,
> adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-10-21, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §11 says why.

**Opened by Sergi on 2026-10-21**, on the item [`IDEAS.md`](IDEAS.md) carries as
*Give the proposer the manual: the authority channel*, under *What the outside
reading of October 2026 proposes and nothing has run*. Two choices were his
before a line of this was drafted: **both shapes run**, compiled once and in the
loop, and **the drafter writes the prose manual of level 2** (§2.1).

**Priority enters a stratified policy through an external channel, and there
are three:** declaration, feedback and authority
([`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §1, [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md)
§1). Declaration has been tried at every point the project could reach: pair by
pair (`P`, `B`), at write time (`U`, `W`), imposed (`E`, `O`) and drafted blind
(`K`). Feedback was rung 4. **Authority exists only at its perfect limit**: rung
2's ceiling, whose 199 edges come from the known layer order. That is *a
perfect author's declaration*, in [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md)
§3's words, and §9.3 counts the 199 as that author's cost. No prompt
in the tree describes a queue or gives the model any policy. Each lists the
eight bare names and says nothing about them.

**Three failures may be failures of knowledge, and nothing measured so far can
tell.**

- **The proposer partitions instead of stratifying.** Read beyond the keyword,
  `PLAN_BLIND.md`'s `K-a` puts `PLAN_REUSE.md`'s three bases at 1.0000, 1.0000
  and 0.8125.
- **Beyond the keyword its declarations point the way a coin would**, below a
  ranking of the queues that read the answer key (`K-b`, `K-c`). The ranking
  the model states is weaker than that one (`M-b`, `M-c`).
- **Two classes have no material.** In `PLAN_REUSE.md`'s three final bases no
  rule routes a ticket to `ACCOUNT_MANAGER` or to `T3_ENGINEERING`. The
  proposer named `ACCOUNT_MANAGER` on none of the 13 escalations whose truth it
  was. With the ticket alone the model names it on none of 65 held-out decisions
  (`V-e`).

[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §5 leaves the partition's cause
between three candidates: *the framing of the task —one ticket, one rule—, the
specific model, or elicitation by rule-writing in general*. **This plan adds a
fourth, knowledge, and is the first to control it.** It hands the model the
policy at three levels of fidelity and asks it in the two shapes `IDEAS.md`
names:

- **Shape C, compiled once.** One call writes the whole rule base from the
  manual, and the base is checked exactly over the exhaustive space.
- **Shape L, the loop.** `PLAN_REUSE.md`'s loop runs with the manual in the
  proposer's system prompt.

**What it changes in what is measured, said first.** `CHAT_SUMMARY.md` §1 says
the hidden policy *"is THIS company's manual. What is measured is whether a
structured function can be recovered from experience"*. With the manual in the
prompt, the question becomes **whether a policy stated in text survives
compilation**, by one answer or by the impasse loop. That is a different
question, and no figure here continues a rung's.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The arms.** A level `k` is 0, 1, 2 or 3 (§5).

- **`C_k`** is shape C at level `k`: `ASKS = 5` asks. An ask is one call, with
  rung 2's retries, whose answer is installed into rung 2's engine by
  `manual/compile.py`.
- **`L_k`** is shape L at level `k`: `REPS = 3` runs of `PLAN_REUSE.md`'s loop,
  with rung 2's engine, prompt v1, reasoning off, n=2000 and seed 17, the
  manual inserted in the system prompt (§5.4).
- **Level 0 is the same-day control in both shapes.** `L_0`'s system prompt is
  v1's to the byte, so `L_0` is `PLAN_REUSE.md`'s protocol asked again.

**The statistics.** Each is a ratio of integer counts, and **each is compared
with its line exactly, as a fraction**. No rounding enters a verdict.

- **`space(B)`**: the share of the 134,400 points of the exhaustive space that
  base `B` decides right under rung 2's engine. A CONFLICT or an IMPASSE is not
  right. The undefeated masks of `blind.rows.undefeated_masks` are read by
  `reuse.structure.subsumption_on_space`, against
  `rung3.order_search_ls.space_truth_masks`.
- **`corpus(B)`**: the same over the 2,000 cases of seed 17, base `B` read
  whole — every rule present from case 0, as `PLAN_OVERLAP.md` read its bases.
  The truth is the labels of `PLAN_REUSE.md`'s Stage B records.
- **`recall_q(B)`**: of the points of the space whose true queue is `q`, the
  share `B` sends to `q`.
- **`K-a(B)`**: `PLAN_BLIND.md`'s statistic, by `blind.rows.k_a`. It is the
  share of `B`'s rules, keyword rules left apart, that overlap no earlier rule
  of another queue on the half of the space without the keyword. A base with no
  such rule counts at 1.00.
- **What `B` is.** For a loop run, its final base is `edges.rebuild.rebuild`'s
  replay of the record. For a compile ask, it is the answer as installed, and
  list position stands for birth order.
- **`prop(L_k)`**: the proposer's choice of queue at the escalations, pooled
  over the level's three runs. It is right over escalated, a failed proposal
  counting as not right: `proposal_action_accuracy`'s own definition, by
  `rung2.shadow2.compute_metrics2`.

**The unit.** A `C` row reads the **median over the level's valid asks**. An `L`
row reads the **median over the level's three runs**, except `G-f`, which pools
the escalations as `proposal_action_accuracy` is defined. A difference row
subtracts medians.

**Validity, *thin*, and when a row has no value.** All of it is settled here and
not in the scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **An ask is valid** iff its answer parses into a JSON object with a non-empty
  list `rules`. Rules that fail rung 2's validation are rejected and counted, as
  the loop counts them, and the rest are installed. A valid ask whose every rule
  fails installs an empty base and scores 0.
- **Invalid asks** are counted, published with their raw text and
  `finish_reason`, and excluded, never repaired.
- **With fewer than three valid asks at a level a row reads**, that row is
  unadjudicable.
- **A loop run that cannot be completed** leaves its level with fewer runs. The
  rows are read on the runs that exist, and the record names the missing one.
  With fewer than two runs at a level a row reads, that row is unadjudicable.
- **A verdict is labelled *thin*** when one ask or run, put in place of its own
  arm's median, would put the statistic on the other side of the line. For
  `G-f`, the test is dropping any one run of either level. The label does not
  change the verdict.

**Which side had the label**, for every arm and reference. This is the lesson
of §6 of `PLAN_ILP.md`, checked against the prompts this package builds and not
recalled:

| arm or reference | what it is handed | reads a label? |
|---|---|---|
| `C_0`, `L_0` | the eight queue names, as every prompt in the tree | no |
| `C_1`, `L_1` | the catalogue: what each queue is for | no |
| `C_2`, `L_2` | the catalogue and the prose: every live rule's queue, with a real manual's vague words for its thresholds (§5.2) | **in effect, for most tickets**, through prose written by a drafter who knew the policy |
| `C_3`, `L_3` | the 29 rules as text, in their order | **yes**: the label of every case is derivable from the text by first match, as `keep_k` is handed it ([`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §1.5). This is what makes level 3 the bound and not a competitor |
| `PLAN_REUSE.md`'s three bases | the eight names | no |

**No arm sees a training example.** `C` sees no ticket at all. `L` sees the
2,000 arrivals as they come, as every loop has.

| id | claim | statistic, with its denominator and cell | band | refuted by |
|---|---|---|---|---|
| **G-a** | **The model transcribes the policy.** The instrument row: handed the 29 rules, one answer compiles them | the median over `C_3`'s valid asks of `space(B)` | **≥ 0.95** | **< 0.95** |
| **G-b** | **Knowing what the queues are for reaches the two queues no loop base ever routed to** | the median over `C_1`'s valid asks of the mean of `recall_ACCOUNT_MANAGER` and `recall_T3_ENGINEERING` over the space, less the same median over `C_0`'s | **≥ 0.10** | **< 0.10** |
| **G-c** | **With the policy in front of it, the proposer still partitions.** `IDEAS.md`'s reading: the partition then belongs to the elicitation and not to what the model knows | the median over `L_3`'s runs of `K-a` of the final base, beyond the keyword by construction | **> 0.50** | **≤ 0.50** |
| **G-d** | **The loop loses what the text holds.** Compiled once, the policy decides the function better than the loop does with the same text in its prompt | the median over `C_3`'s valid asks of `space(B)`, less the median over `L_3`'s runs of `space` of the final base | **≥ 0.10** | **< 0.10** |
| **G-e** | **A real manual helps the loop where tickets arrive** | the median over `L_2`'s runs of `corpus` of the final base, less the same median over `L_0`'s | **≥ 0.10** | **< 0.10** |
| **G-f** | **Knowing what the queues are for, the proposer picks the right queue more often** | `prop(L_1) − prop(L_0)`, each pooled over its three runs | **≥ 0.10** | **< 0.10** |
| **G-g** | *Reported, not adjudicated.* **What the drafter could not band** | every arm and level on every cell: `space` whole and on each keyword half, `corpus`, the recall of all eight queues on both surfaces, `K-a`, and `O-a` over the whole space. For `C`, each ask's rules installed and rejected, its derived edges by verdict, its inversions (§6.3), its first-match reading, which hidden rules it reproduces to the extension, and the accuracy over each hidden rule's region. For `L`, `PLAN_REUSE.md`'s online set per run: reuse, silent error, online e2e, CONFLICTs, escalations, `prop` by true queue, and the `ONCALL_ESCALATION` and `SECURITY_INCIDENT` escalations and compiled decisions; copies written the same; each hidden rule's region in the final base; `K-b`'s direction beyond the keyword where it has 20 units. `L_0` against `PLAN_REUSE.md`'s 2026-09-30 runs, figure by figure. The span of dates of Stage B. Every call's `call_attempts`, provider and finish reasons included. Every `note`, recorded and not coded | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-21)**

**Why each row, and why these lines.**

- **`G-a` is the instrument.** If the model cannot copy 29 rules into the DSL
  with their order, no reading of levels 1 and 2, or of the loop, separates
  knowledge from anything. 0.95 leaves room for a slip outside the keyword half.
  A slip in one of the three keyword rules costs up to a quarter of the space,
  and that is a failure to transcribe.
- **`G-b` reads the material problem where it has power.** `ACCOUNT_MANAGER` is
  16,440 points of the space and `T3_ENGINEERING` 8,180, against 109 and 117
  corpus cases. It sets level 1 against level 0 *in the same shape*, so what
  moves it is the catalogue's lines and nothing else. 0.10 is a tenth of the
  two classes, which no loop base has ever reached at all.
- **`G-c` takes `K-a`'s line from `PLAN_BLIND.md`**, so that a reading here and
  `K-a`'s there mean the same thing. It is read at level 3 because there
  knowledge is complete and unambiguous: whatever partition survives it is not
  ignorance.
- **`G-d` is read at level 3 for the same reason.** The two arms hold the same
  text, so a gap between them is what the loop's elicitation costs and not what
  a vague word costs. The line is a tenth of the space.
- **`G-e` is the deployment's row.** A real manual is what a company has, and
  the arrivals are what it meets. It is read against `L_0` and not against
  `PLAN_REUSE.md`'s runs, because those are three weeks older and `V-a` found
  the model's answers drifting in twelve days (§6.9).
- **`G-f` reads the material problem in the loop.** There it is the axis
  `CLAUDE.md` Step 5 keeps apart: choosing the wrong queue when proposing.
  `PLAN_REUSE.md`'s three runs pool 68 right of 135. Its line is 0.10, and the
  label marks a verdict that one run carries.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md` and `IDEAS.md`.**
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  They were read through a digest commissioned for this plan. The passages cited
  here were then read directly: `CHAT_SUMMARY.md` §1, §2.2's erratum, §3's
  table, the closing bet and its erratum; `ARBITRATION_REPORT.md` §4's table,
  §5, and §7's P1 and P5; `EXTERNAL_REVIEW.md` §§1.3-1.5 and §5.6.
- **The published figures of §3.** Their per-run values for `PLAN_REUSE.md`,
  `PLAN_EDGES.md`, `PLAN_OVERLAP.md`, `PLAN_AUTHORSHIP.md` and `PLAN_BLIND.md`
  were read from the records by an extraction commissioned for this plan.
- **Figures computed while drafting**, from committed records and the hidden
  policy. `G-g1` recomputes every one of them, and Stage A's record will own
  them.
  - **The hidden policy, rule by rule.** What each rule decides on both
    surfaces. `H21`, `H25` and `H27` decide nothing on either. §5.3's masses by
    how the prose states each rule.
  - **`manual/compile.py`'s derivation.** Applied to the hidden policy written
    as an answer, it gives back the 199 edges, none refused and no inversion,
    and 1.0000 on both surfaces.
  - **The hidden policy's own `K-a`: 0.0769**, 2 of its 26 rules beyond the
    keyword. This is what a stratified policy reads on `G-c`'s statistic.
  - **`PLAN_REUSE.md`'s three final bases through this plan's instrument.**
    `space` 0.3063, 0.2951 and 0.5536; `space` beyond the keyword 0.3125, 0.3464
    and 0.3696; `corpus` 0.4035, 0.4470 and 0.5245. The `space` and `corpus`
    figures reproduce `PLAN_EDGES.md`'s `W-d`. `K-a` reads 1.0000, 1.0000 and
    0.8125, which reproduces `PLAN_BLIND.md`'s baselines.
  - **`recall` of `ACCOUNT_MANAGER` and `T3_ENGINEERING` in those bases is 0 on
    both surfaces**, in all three runs.
  - **`prop` by true queue, pooled.** `ACCOUNT_MANAGER` 0 of 13, `T1_GENERAL` 0
    of 12, `T2_TECHNICAL` 35 of 63, `SECURITY_INCIDENT` 19 of 20. No escalation
    had `T3_ENGINEERING` or `ONCALL_ESCALATION` for its truth.
- **The texts of §5.** The drafter wrote them, knowing the policy (§2.1, §6.8).
- **OpenRouter's public list of models**, read for the model's output limit
  (§11).

**Not seen, because nothing has produced it:**

- any answer to either question, at any level;
- any base the model compiles from a manual;
- any loop run with a manual in its prompt;
- any loop run of the v1 protocol since 2026-09-30.

**What the drafter expects, written down so the scoreboard can score it.**
**`G-a`, `G-d` and `G-e` hold; `G-b`, `G-c` and `G-f` are refuted.** The drafter
trusts `G-a` most, then `G-d`, `G-e`, `G-f` and `G-b`, and `G-c` least.

- **`G-a` holds.** Copying 29 rules with their order is transcription. Shown
  two of the hidden rules as text and a witness ticket, the model already named
  the right winner on 0.8824 of the hidden policy's clean pairs (`FINDINGS2.md`,
  Stage C). That is level 3 in pairwise form.
- **`G-b` is refuted.** The catalogue says little the names do not.
  `ACCOUNT_MANAGER`'s line adds *cuentas clave* and *riesgo de darse de baja*,
  and nothing in it names an attribute. `T3_ENGINEERING`'s adds nothing a
  condition can test. A model writing a whole policy from the names alone will
  already route something to both queues.
- **`G-c` is refuted.** A proposer that copies the rule the manual applies to
  its ticket writes the rules of a stratified policy, and those cross: the
  hidden policy itself reads 0.0769. **The risk to this bet is v1's framing.**
  It tells the proposer it only needs to declare against rules it overlaps, and
  a proposer that knows the policy could write each rule's effective region
  instead, disjoint from the rest. That would hold `G-c`, and read as
  elicitation.
- **`G-d` holds.** This is `U-d`'s mechanism handed the policy. A rule copied
  from a late layer decides its exceptions' region before any of them can
  escalate. A copy of the catch-all, written on the first default ticket,
  covers every ticket after it, and under rung 2's engine nothing impasses
  again. The loop then learns only from CONFLICTs.
- **`G-e` holds.** With the prose the proposer picks more queues right, and most
  of v1's silent error is born with the rules (`U-c`). The bet is that the gain
  survives the broad rules of `G-d`'s mechanism.
- **`G-f` is refuted.** A ticket is eight attributes, and the catalogue
  describes purposes. Nothing in a line maps `T1_GENERAL`'s purpose onto an
  attribute, and `T1_GENERAL` is where the proposer is wrong on every
  escalation.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 42 of 99 adjudicated rows were refuted.
- **The last comparable plan.** `PLAN_RANKING.md`'s drafter expected three holds
  and got two.
- **No band here was set on a development set.** Two lines are taken from
  closed threads' own: `K-a`'s 0.50 and `G-a`'s 0.95, which is the claim's own
  edge. The other four are a tenth of their axis.

**How the rows read together.**

- **`G-a` is refuted.** The model cannot transcribe the policy into the DSL, and
  every other row is read as bounded by that before it is read at all.
- **`G-c` holds.** With the policy in front of it the loop still partitions, and
  the partition belongs to the elicitation: `IDEAS.md`'s stronger result.
  `STATUS.md`'s second open item loses the fourth candidate, and `ARBITRATION_REPORT.md`
  §5's three remain.
- **`G-c` is refuted.** Handed the structure, the proposer crosses. Partition was
  at least partly a matter of knowledge, or of having a template to copy, and
  copying is not inducing. `L_1`'s and `L_2`'s `K-a`, reported, say which.
- **`G-d` holds.** Compilation by impasse loses a policy it is handed. The
  founding loop's limit is not what the model knows.
- **`G-d` is refuted.** Given the policy, the loop gets within a tenth of the
  space of compiling it once. What the loop lost before was knowledge.
- **`G-e` holds.** A company's manual is worth a tenth of the arrivals to the
  loop. The authority channel exists outside its perfect limit.
- **`G-b` and `G-f` are both refuted.** The two classes without material are
  not a matter of knowing what the queues are for. Whether the policy fixes
  them is in `G-g`'s recall of `C_2`, `C_3`, `L_2` and `L_3`.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.**

- **`results_reuse/run_n2000_r{1,2,3}.json`** — `PLAN_REUSE.md`'s three runs.
  They are the 2026-09-30 reference, and their labels are the corpus truth.
  Read-only, hard rule 4.
- **`results_edges/score.json`**, **`results_blind/score.json`**,
  **`results_students/score.json`** and **`results_screen/score.json`** — §3's
  references, which `G-g1` reproduces.
- **`results2/ceiling2.json`** and **`results2/ceiling2_space.json`** — rung 2's
  ceiling, which `G-g1` reproduces through this plan's installer.

**What is bought.**

- **Shape C.** Twenty asks, five per level, plus a smoke run of one ask per
  level.
- **Shape L.** Twelve runs of the loop at n=2000, three per level, plus a smoke
  run of 20 cases at level 3. `PLAN_REUSE.md`'s three runs made 135 calls
  between them, so twelve should make some 400 to 1,200.
- **The price.** At `deepseek/deepseek-v4-flash`'s listed price this is cents.
  It is long: §9 says the loop runs belong in Sergi's terminal.

**What is not bought.**

- No other model, and no other prompt version than v1.
- No question with a ticket and the manual and no rule. The loop's escalations
  ask that, and `G-f` reads it.
- No manual other than the three of §5.

---

## 2. The choices that have to be made at signature time

Each is the drafter's recommendation, and each is Sergi's to overrule. A change
to any of them is a change to §0, and belongs in the same signed commit. The
two choices Sergi made before the drafting, both shapes and the drafter's prose,
are not repeated here.

### 2.1 The three texts — the drafter recommends §5 as written

- **Level 1, the catalogue**, is one line per queue. It is written as a
  deployment's catalogue of its queues: a team and what it handles. It names no
  attribute, no value and no threshold.
- **Level 2 is the catalogue followed by the prose.** The prose names teams, as
  a real manual does, and the catalogue ties each team to its queue. Without it,
  level 2 would add a guess about what *soporte tecnico* means, and that is not
  the ambiguity this level is for.
- **The prose states every rule that decides something.** It gives all five
  thresholds of severity and prior tickets in a real manual's vague words
  (*alta*, *urgente*, *baja*, *no urgentes*, *varias veces*, *bastantes*,
  *muchisimos*), and keeps severity 1, severity 4 and *ningun ticket* exact. It
  leaves the precedence among five of its eight sections to the order they are
  listed in. It omits the
  three hidden rules that decide nothing on either surface. §5.3 says rule by
  rule what it does, and so says where its readings will be lost.
- **Level 3 is the rules as `rung2.engine2.Rule2.render` prints them**, in the
  hidden policy's order, with one sentence saying the first rule that matches
  decides.
- **The drafter wrote level 2 knowing the policy.** That is the condition
  `EXTERNAL_REVIEW.md` §1.3 names — *the same hand wrote the policy, the DSL and
  the engine being evaluated* — extended to the manual. The prose's ambiguity is
  a choice, declared in §5.3, and not a sample of real manuals (§13.1).
- **What is open to change.** Sergi may rewrite any of the three before signing.
  The digests of §5 change with them, and so do the masses of §5.3, which Stage
  A recomputes.

### 2.2 The loop's protocol — the drafter recommends v1, with the manual before the operators

v1 is `PLAN_REUSE.md`'s protocol, so `L_0` is that plan asked again and every
`U` figure has a same-day counterpart. The manual goes in as one block, a header
line and the level's text, just before v1's list of operators: after the queue
names, where a reader meets the queues, and before anything about the DSL.
Nothing else in v1 moves, and `G-g2` checks that.

### 2.3 The compile question — the drafter recommends rung 2's engine, with the list's order standing for the declaration

`manual/prompts.py`'s question reuses v1's blocks word for word, and describes
the engine in two levels. What a rule's cases contain wins first. Where two rules
overlap without containment, the earlier one in the list wins. **That is exactly
the engine `manual/compile.py` installs the answer into**, with
`rung2/hidden_priority.py`'s derivation turning the list into edges. So the
model is told the semantics it is scored under. A global priority integer is
not asked for: `ARBITRATION_REPORT.md` §3 rules it out.

### 2.4 The counts — the drafter recommends five asks and three runs per level

Three runs is `PLAN_REUSE.md`'s count, and it keeps `L_0` comparable with it.
Five asks cost a few cents more than three and put the median of `C` on five
draws.

### 2.5 One day — the drafter recommends the order of §9

The compile session first, then the twelve runs, repetition by repetition. One
order of the four levels is drawn at `ORDER_SEED`, and each repetition rotates
it by one place. So every level stands at a different place in each
repetition, no level is first or last twice, and if Stage B spans two days,
every level has runs on both. The compile passes are ordered the same way, by
their own draw. The record keeps each run's dates, and `G-g` reports the span.

### 2.6 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Nothing here is recomputed by this plan except under `G-g1`, which checks its
recomputation against the record rather than publishing it again.

**Rung 2's ceiling** — [`results2/ceiling2.json`](results2/ceiling2.json) and
[`results2/ceiling2_space.json`](results2/ceiling2_space.json), published by
[`FINDINGS2.md`](results2/FINDINGS2.md):

- 1.0000 on the corpus and on the space, with 199 declared edges and none
  refused.
- Subsumption alone reaches 0.6315 and 0.261176.

**`PLAN_REUSE.md`'s three runs, 2026-09-30** —
[`results_reuse/score.json`](results_reuse/score.json), published by
[`FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md):

| run | online e2e | `prop` | reuse | escalations | CONFLICTs |
|---|---|---|---|---|---|
| 1 | 0.3935 | 0.4839, 30 of 62 | 0.5323 | 62 | 30 |
| 2 | 0.4400 | 0.4839, 15 of 31 | 0.8387 | 31 | 5 |
| 3 | 0.5130 | 0.5476, 23 of 42 | 0.7381 | 42 | 12 |

**The same runs' final bases, read whole** —
[`results_edges/score.json`](results_edges/score.json), `W-d`, published by
[`FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md):

- `corpus`: 0.4035, 0.4470 and 0.5245.
- `space`: 0.30625, 0.29509 and 0.55357.

**`K-a`, by protocol** — [`results_blind/score.json`](results_blind/score.json),
published by [`FINDINGS_BLIND.md`](results_blind/FINDINGS_BLIND.md):

| protocol | run 1 | run 2 | run 3 | median |
|---|---|---|---|---|
| v1 | 1.0000 | 1.0000 | 0.8125 | 1.0000 |
| v1e | 1.0000 | 0.9655 | 0.9667 | 0.9667 |
| v2e | 0.8704 | 1.0000 | 1.0000 | 1.0000 |
| v2b | 0.2500 | 0.2963 | 0.3784 | 0.2963 |

v2b is the base drafted blind: `K-a` held there.

**The two classes.**

- **Rung 1's base** —
  [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §2: for 66.7% of
  `T3_ENGINEERING` and 64.2% of `ACCOUNT_MANAGER` no covering rule carries the
  right queue.
- **Rung 1's proposer** — [`FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md) §3's
  erratum: it named `ACCOUNT_MANAGER` on 1 of the class's 29 escalations.
- **`PLAN_REUSE.md`'s bases on test split 0** —
  [`results_students/score.json`](results_students/score.json), the record and
  not its prose: `ACCOUNT_MANAGER` 0 of 55 and `T3_ENGINEERING` 0 of 57, in every
  run.
- **The model with the ticket alone** —
  [`results_screen/score.json`](results_screen/score.json), `V-e`, published by
  [`FINDINGS_SCREEN.md`](results_screen/FINDINGS_SCREEN.md): `ACCOUNT_MANAGER`
  on none of 65 held-out decisions, 0.0615 with the screen; `T3_ENGINEERING`
  0.0965 and 0.0175 on 57.

**Level 3 in pairwise form, already paid for** —
[`results2/pair_judgement_baselines.json`](results2/pair_judgement_baselines.json),
published by [`FINDINGS2.md`](results2/FINDINGS2.md), Stage C. Shown two hidden
rules and a witness ticket, the model named the right winner on 0.8824 of 170
clean pairs.

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and `harness/ceiling_check.py`'s `HIDDEN_DSL`, and
   touches nothing under `harness/` but `call_record.py`'s installed wrapper.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** The asks are sequential, the loop is sequential, and
   no two runs go side by side.
4. **Seed 17, no regeneration.** Every record of the closed threads is
   read-only. `harness/record_guard.py` guards this plan's paid records, and
   the flag that overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema** once the smoke runs have
   been read. The texts are frozen in §5 and pinned by digest.
6. **If the numbers come out badly, report them.** A manual that buys nothing is
   a result.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`rung2/`, `reuse/`, `edges/`, `blind/` and `rung3/` are called by this plan
   and not edited**, as `overlap/` calls `authorship/`.
   - **The loop is `reuse/run.py`'s**: a fresh `PriorityEngine(space=Space())`,
     `OpenRouterProposer2(model, prompt_version="v1", reasoning=REASONING)` and
     `run_shadow2`, with one change only. The proposer's `system_prompt` is v1
     with the manual inserted.
   - **The final bases are `edges.rebuild.rebuild`'s.**
   - **The scorers are `blind.rows`'s and `reuse.structure`'s.**
   - **The truth** is `rung3.order_search_ls.space_truth_masks` over the space,
     and `PLAN_REUSE.md`'s records over the corpus.
   - **The edges** come from `rung2/hidden_priority.py`'s derivation, applied to
     a list, and `G-g1` holds it to that module's 199.

B. **This plan breaks the oracle's separation on purpose, and only through three
   frozen files.**
   - **The proposer's path imports by name neither the oracle, nor
     `HIDDEN_DSL`, nor `harness.ceiling_check`, nor `rung2.hidden_priority`.**
     That path is `manual/levels.py`, `manual/prompts.py`, `manual/compile.py`,
     `manual/ask.py` and `manual/run.py`.
   - **They join `ONLINE_LOOP` in `tests/test_oracle_separation.py`**, with a
     comment saying why the package is exempt: the policy reaches the model as
     the text §5 prints, pinned by digest, and by no other route. A test adds
     the policy's own names to the forbidden imports of those five modules.
   - **Before spending, `manual/ask.py` and `manual/run.py` call
     `manual/gates.py`**, which rebuilds level 3 from `HIDDEN_DSL` offline. So
     the policy is in their process, and it is not in what they send. Every
     prompt is built from v1, the domain and the three files alone, and a test
     replaces the files and watches only the manual's block change.
   - **The labels** are rule A's.

C. **Every record carries `_env`, the model, the temperature, the reasoning
   setting, the system prompt and `call_attempts`.** Every command runs with
   `PYTHONHASHSEED=0` set explicitly.

D. **The constants of §11 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.

E. **What the model writes is recorded and installed as written.** A rejected
   rule is counted, never repaired, and a `note` is recorded and never coded.

F. **The order of Stage B is §9's**, and the modules refuse a step out of it.

---

## 5. The texts, and what each says of the policy

The files live in `manual/texts/`. They are ASCII and Spanish, as v1 is. A
level's manual is its parts joined by one blank line (`manual/levels.py`):
level 1 is the catalogue, level 2 the catalogue and the prose, and level 3 the
rules.

| file | sha256 |
|---|---|
| `catalogue.txt` | `95cec2fe42aeacebc77c642a634e5fc8d3024da9d6f133aff22cb09b406edff1` |
| `prose.txt` | `dc63a2a144271372ec70af6a9102e3f0996960cdcc75751c1549643ca7438330` |
| `rules.txt` | `bcc9f9818caa18039346e610ad73f30c57b49957dab51f04dfd3b02717c47dcd` |

### 5.1 `catalogue.txt`

```
QUE HACE CADA COLA

T1_GENERAL: primer nivel de soporte. Consultas generales, dudas de uso y peticiones que no necesitan un diagnostico tecnico.
T2_TECHNICAL: soporte tecnico de segundo nivel. Diagnostica y resuelve las incidencias tecnicas del producto.
T3_ENGINEERING: ingenieria. Fallos del producto que necesitan que un ingeniero investigue el codigo o la plataforma.
BILLING_SPECIALIST: especialistas de facturacion. Cobros, facturas y pagos que necesitan la intervencion de una persona.
SECURITY_INCIDENT: respuesta a incidentes de seguridad. Posibles brechas, accesos indebidos o vulnerabilidades.
ACCOUNT_MANAGER: gestor de cuenta. La relacion comercial con las cuentas clave, incluidas las que corren riesgo de darse de baja.
ONCALL_ESCALATION: guardia. Incidentes criticos que no pueden esperar al siguiente turno, a cualquier hora.
SELF_SERVICE_DEFLECT: autoservicio. Se responde con documentacion y respuestas automaticas, sin que intervenga un agente.
```

### 5.2 `prose.txt`

```
COMO ENRUTAMOS LOS TICKETS

1. Seguridad, antes que nada. Si el ticket menciona un problema de seguridad y viene de una cuenta business o enterprise, o tiene severidad alta, es un incidente de seguridad. El resto de menciones de seguridad, de cuentas free o pro con severidad baja, las revisa soporte tecnico.

2. Despues, lo critico. Una incidencia critica (severidad 1) de un cliente enterprise activa la guardia. Si el cliente es business, la guardia solo se activa fuera de horario; en horario la coge ingenieria. Las criticas de la API tambien van a ingenieria, y el resto de criticas a soporte tecnico.

3. Facturacion. Los tickets de facturacion de clientes enterprise los lleva su gestor de cuenta. Si el problema es urgente, o el cliente ya nos ha escrito varias veces este mes, va a un especialista de facturacion. Lo demas de facturacion se resuelve con autoservicio.

4. Cuentas en riesgo. Un cliente enterprise que ha abierto bastantes tickets en el ultimo mes, o un cliente business que ha abierto muchisimos, pasa a su gestor de cuenta.

5. Por producto. Los problemas de la API y de las integraciones van a ingenieria si son de severidad alta, y a soporte tecnico si no. Los de mobile y los de dashboard de severidad alta tambien son de soporte tecnico.

6. Telefono. Las llamadas de clientes free se derivan a autoservicio. Fuera de horario, el telefono lo atiende el primer nivel, salvo a los clientes enterprise.

7. Desvio a autoservicio. Los problemas no urgentes de clientes free se resuelven con autoservicio, y tambien los de severidad minima de clientes que no han abierto ningun ticket en el ultimo mes.

8. Por defecto. Lo que no encaje en nada de lo anterior va al primer nivel.
```

### 5.3 What the prose says of each hidden rule

The masses are the points of the space and the corpus cases each rule decides
under first match. They were computed while drafting, and Stage A recomputes
them.

| rule | decides (space · corpus) | the prose says it |
|---|---|---|
| `H01` keyword, business or enterprise → `SECURITY_INCIDENT` | 33,600 · 9 | §1, exactly |
| `H02` keyword, severity ≤ 2 → `SECURITY_INCIDENT` | 16,800 · 11 | §1, vaguely: *severidad alta* |
| `H03` keyword → `T2_TECHNICAL` | 16,800 · 51 | §1, as the remainder, vaguely: *free o pro con severidad baja* |
| `H04`-`H08` severity 1 → on-call, engineering, technical | 16,800 · 92 | §2, exactly |
| `H09` billing, enterprise → `ACCOUNT_MANAGER` | 2,520 · 26 | §3, exactly |
| `H10` billing, severity ≤ 2 → `BILLING_SPECIALIST` | 2,520 · 85 | §3, vaguely: *urgente* |
| `H11` billing, prior tickets ≥ 3 → `BILLING_SPECIALIST` | 4,320 · 186 | §3, vaguely: *varias veces este mes* |
| `H12` billing → `SELF_SERVICE_DEFLECT` | 720 · 154 | §3, as the remainder |
| `H13` enterprise, prior tickets ≥ 5 → `ACCOUNT_MANAGER` | 7,680 · 34 | §4, vaguely: *bastantes tickets* |
| `H14` business, prior tickets ≥ 8 → `ACCOUNT_MANAGER` | 6,240 · 49 | §4, vaguely: *muchisimos* |
| `H15`, `H17` api or integrations, severity ≤ 2 → `T3_ENGINEERING` | 4,400 · 92 | §5, vaguely: *severidad alta* |
| `H16`, `H18` api or integrations → `T2_TECHNICAL` | 8,800 · 447 | §5, as the remainder |
| `H19` mobile, severity 2 → `T2_TECHNICAL` | 2,200 · 45 | §5, as *mobile de severidad alta*, which §2 makes equivalent. **The sentence attaches ambiguously**: *de severidad alta* may be read as qualifying dashboard alone |
| `H20` dashboard, severity ≤ 2 → `T2_TECHNICAL` | 2,200 · 123 | §5, vaguely: *severidad alta* |
| `H21` Portuguese, severity ≤ 2 → `T2_TECHNICAL` | 0 · 0 | omitted: it decides nothing |
| `H22` phone, free → `SELF_SERVICE_DEFLECT` | 840 · 16 | §6, exactly |
| `H23` phone, off hours, not enterprise → `T1_GENERAL` | 580 · 3 | §6, exactly |
| `H24` free, severity ≥ 3 → `SELF_SERVICE_DEFLECT` | 2,520 · 303 | §7, vaguely: *no urgentes* |
| `H25` free, no prior ticket → `SELF_SERVICE_DEFLECT` | 0 · 0 | omitted: it decides nothing |
| `H26` severity 4, no prior ticket → `SELF_SERVICE_DEFLECT` | 220 · 22 | §7, exactly: *severidad minima*, *ningun ticket* |
| `H27` severity ≤ 2 → `T2_TECHNICAL` | 0 · 0 | omitted: it decides nothing |
| `H28`, `H29` the defaults → `T1_GENERAL` | 4,640 · 252 | §8, merged into one default, exactly in effect |

**Summed by how they are stated.**

| stated | rules | space | corpus |
|---|---|---|---|
| exactly, or as a remainder | 13 | 64,080 (0.4768) | 769 (0.3845) |
| vaguely | 10 | 63,480 (0.4723) | 934 (0.4670) |
| ambiguously | 1 | 2,200 (0.0164) | 45 (0.0225) |
| merged | 2 | 4,640 (0.0345) | 252 (0.1260) |
| omitted | 3 | 0 | 0 |

**And the precedence.**

- §1 is first, by its own words (*antes que nada*).
- §2 is second (*Despues, lo critico*).
- §8 is last (*Lo que no encaje en nada de lo anterior*).
- Between §3 and §7 nothing is said but the order the sections are listed in.
  Under first match that order is the hidden policy's, and the prose never says
  that order decides.

**So the prose holds every live rule, and a perfect reader of it** — one who
read every vague word as the policy means it, and the section order as
precedence — would score 1.0000. Everything level 2 loses against level 3 is
reading.

### 5.4 `rules.txt`

The rules are printed by `rung2.engine2.Rule2.render`, the format in which the
loop shows the proposer its own base. They are in `HIDDEN_DSL`'s order, which is
the hidden policy's, and the catch-all is printed in `HIDDEN_DSL`'s encoding
(§6.4).

```
LAS REGLAS DE LA EMPRESA, EN ORDEN

Se aplica la primera regla de la lista cuyas condiciones casa el ticket.

H01: SI has_security_keyword eq True AND customer_tier in ['business', 'enterprise'] ENTONCES SECURITY_INCIDENT
H02: SI has_security_keyword eq True AND severity lte 2 ENTONCES SECURITY_INCIDENT
H03: SI has_security_keyword eq True ENTONCES T2_TECHNICAL
H04: SI severity eq 1 AND customer_tier eq enterprise ENTONCES ONCALL_ESCALATION
H05: SI severity eq 1 AND customer_tier eq business AND off_hours eq True ENTONCES ONCALL_ESCALATION
H06: SI severity eq 1 AND customer_tier eq business ENTONCES T3_ENGINEERING
H07: SI severity eq 1 AND product eq api ENTONCES T3_ENGINEERING
H08: SI severity eq 1 ENTONCES T2_TECHNICAL
H09: SI product eq billing AND customer_tier eq enterprise ENTONCES ACCOUNT_MANAGER
H10: SI product eq billing AND severity lte 2 ENTONCES BILLING_SPECIALIST
H11: SI product eq billing AND prior_tickets_30d gte 3 ENTONCES BILLING_SPECIALIST
H12: SI product eq billing ENTONCES SELF_SERVICE_DEFLECT
H13: SI customer_tier eq enterprise AND prior_tickets_30d gte 5 ENTONCES ACCOUNT_MANAGER
H14: SI customer_tier eq business AND prior_tickets_30d gte 8 ENTONCES ACCOUNT_MANAGER
H15: SI product eq api AND severity lte 2 ENTONCES T3_ENGINEERING
H16: SI product eq api ENTONCES T2_TECHNICAL
H17: SI product eq integrations AND severity lte 2 ENTONCES T3_ENGINEERING
H18: SI product eq integrations ENTONCES T2_TECHNICAL
H19: SI product eq mobile AND severity eq 2 ENTONCES T2_TECHNICAL
H20: SI product eq dashboard AND severity lte 2 ENTONCES T2_TECHNICAL
H21: SI language eq pt AND severity lte 2 ENTONCES T2_TECHNICAL
H22: SI channel eq phone AND customer_tier eq free ENTONCES SELF_SERVICE_DEFLECT
H23: SI channel eq phone AND off_hours eq True AND customer_tier neq enterprise ENTONCES T1_GENERAL
H24: SI customer_tier eq free AND severity gte 3 ENTONCES SELF_SERVICE_DEFLECT
H25: SI customer_tier eq free AND prior_tickets_30d eq 0 ENTONCES SELF_SERVICE_DEFLECT
H26: SI severity eq 4 AND prior_tickets_30d eq 0 ENTONCES SELF_SERVICE_DEFLECT
H27: SI severity lte 2 ENTONCES T2_TECHNICAL
H28: SI customer_tier in ['business', 'enterprise'] ENTONCES T1_GENERAL
H29: SI severity gte 1 ENTONCES T1_GENERAL
```

### 5.5 Where the manual goes

- **In both shapes, the manual is one block**: the line *MANUAL DE ENRUTAMIENTO
  DE LA EMPRESA (es la politica que hay que seguir):*, a blank line, and the
  level's text.
- **It is inserted just before the line that opens *OPERADORES:***, which
  appears once in each prompt.
- **At level 0 nothing is inserted.** The loop's prompt is then
  `SYSTEM_PROMPT_V1`, and the compile question is §2.3's without a manual.
- **The prompts' digests are Stage A's** and are pinned by the tests.

---

## 6. Known traps

**6.1 — A manual in the prompt changes what is measured.** Rungs 1 to 4 asked
whether a structured function can be recovered from experience. This plan asks
whether a stated one survives compilation. No row here continues a rung's
figure, and no comparison with `PLAN_REUSE.md` reads as *learning*. The only
cross-plan comparison is `G-g`'s drift, `L_0` against the same protocol three
weeks earlier.

**6.2 — Level 3's order is its priority, and level 3 hands over the label.**
Under first match, the order of a list *is* the priority
(`ARBITRATION_REPORT.md` §4's table: *"textual order is the priority"*). So
level 3 gives the model the layer order with the rules, and a model that copies
it has been handed every case's label, as `keep_k` is
(`EXTERNAL_REVIEW.md` §1.5). That is what makes it the bound of §0 and not a
competitor. No row reads level 3 as something the model knew.

**6.3 — The manual's semantics is first match; the engine's is subsumption,
then declaration.**

- **In shape C**, the question states the engine's semantics, with the list's
  order standing for the declaration. The engine's reading and a first-match
  reading of the same list part in two places only.
  - **An inversion**: the list puts a rule above one it strictly contains, with
    another queue. Rung 2's engine lets the contained rule win, and first match
    would not.
  - **A refused edge**: an edge the derivation asks for would close a cycle,
    and the engine refuses it.

  Both are counted, and the first-match reading of every answer is reported
  beside the engine's.
- **In shape L**, the proposer translates the manual's first match into rules
  and declarations, under v1's description of the engine. That translation is
  part of what is measured, not an error to correct.

**6.4 — The catch-all's encoding.** The hidden policy's `H29` is `lambda c:
True`. The DSL needs a condition, so `HIDDEN_DSL` writes it as `severity gte 1`,
and level 3 prints it so. The compile question says a default rule needs a
condition every ticket matches. Under rung 2's engine such a rule needs no edge:
every other rule is strictly inside it, and subsumption puts it last.
[`results/FINDINGS_DEFAULT_RULE.md`](results/FINDINGS_DEFAULT_RULE.md) measured
the catch-all's encoding cost under specificity. **It costs nothing under
subsumption**, and `G-g1` checks that on the hidden policy.

**6.5 — Two surfaces, and the keyword's half.** Three keyword rules decide half
the space and 3.55% of the corpus. Each row names its surface: `G-c` is beyond
the keyword by construction, and `G-g` reports every row's cell on both halves.
`EXTERNAL_REVIEW.md` §4.6 records the ILP inducer as *a method that wins the
arrival distribution and loses the function*. `G-d` is read on the function and
`G-e` on the arrivals, and neither is read on the other's surface.

**6.6 — Each loop asks about different tickets.** `prop(L_k)` is a rate over
the escalations of that level's loop. A manual that changes which tickets
escalate changes the population, which is what `CLAUDE.md` Step 5's axis is in
a deployment. `G-g` reports the rate by true queue, so that a difference made
by the mix can be told from a difference made by the choices.

**6.7 — A broad rule decides its exceptions before they escalate.** This is
`U-d`'s mechanism, and §0's expectation for `G-d` rests on it. Under rung 2's
engine a rule with the whole space for its extension ends every IMPASSE. Stage C
reads off each `L` run's record the case at which its base first covered the
whole space, if it did, and `G-g` reports it.

**6.8 — The drafter wrote level 2 knowing the policy.** Its ambiguity is
declared rule by rule (§5.3), and it is the drafter's choice, not a sample.
`G-e` is a statement about this manual. Whether real manuals look like it is
`ARBITRATION_REPORT.md` §9.1's limit, which `PLAN_SENSITIVITY.md` measured for
the policy's shape and nobody has measured for a manual's prose (§13.1).

**6.9 — Two dates.** `L_0` is today's v1. `PLAN_REUSE.md`'s runs are
2026-09-30's, and `V-a` found the model's answers drifting in twelve days, in
which wrong queue and not in how often right. **Every row reads today's arms
only.** The drift is `G-g`'s, row by row.

**6.10 — The model can change under its name.** OpenRouter routes the name to
providers, and `PLAN_RANKING.md`'s sessions were answered by more than one.
`call_attempts` keeps the provider of every attempt, and `G-g` reports each
arm's mix.

**6.11 — Information in front of the model has not changed what it does
before.** *"With the right information in front of it, it makes the same
mistake"* (`FINDINGS2.md`, quoted in `CHAT_SUMMARY.md` §2.2's erratum). And the
conversation's closing bet: success *"will not come from a smarter model nor a
better prompt"*. A manual is a better prompt. Both are priors against `G-e` and
for `G-c`. The drafter's expectations go against both, and a reader should
weigh them so.

**6.12 — `K-a` reads a compiled base by list position.** A compile answer has no
births, so `K-a` reads its list as birth order. It is reported for `C`, never
adjudicated, and its reference is the hidden policy's 0.0769.

**6.13 — One manual, one model, one prompt, one date.** Everything this plan
says about the authority channel is about these three texts.

---

## 7. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**G-g1 — The instrument reproduces the records.** Blocking in the sense of
`harness.ceiling_check`.

- `python3 -m unittest discover` is green.
- **The installer, on the hidden policy written as an answer.**
  - The derivation gives back `rung2.hidden_priority.build_hidden_engine`'s 199
    edges, pair by pair by position, none refused and no inversion.
  - The base scores 1.0000 on both surfaces. So does its first-match reading,
    and so does `rung2.ceiling_check2_space.measure` over the corpus.
- **Teeth.** The same answer with its layers listed in reverse scores below
  1.0000 on both surfaces.
- **`PLAN_REUSE.md`'s three records, through this plan's instrument.**
  - The three agree on every corpus label.
  - `edges.rebuild`'s final bases, scored by masks, give back `W-d`'s `space`
    and `corpus` in `results_edges/score.json`.
  - The mask scorer and `measure`, case by case, agree on the corpus.
  - `K-a` gives back `results_blind/score.json`'s v1 baselines.
  - `prop` gives back each record's `proposal_action_accuracy`.
- Floats are compared with a tolerance against records written under 3.12.

**G-g2 — The texts and the prompts are §5's.**

- **The three files' digests are §5's.**
- **`rules.txt` is rebuilt from `HIDDEN_DSL`**, character for character, by
  `Rule2.render`. Parsing it back gives `HIDDEN_DSL` again.
- **§5.3's claims about the prose's omissions hold.** `HIDDEN_DSL` without
  `H21`, `H25`, `H27` and `H28` — the three rules the prose omits, and the
  default it merges into `H29` — scores 1.0000 on both surfaces. A perfect
  reader of the prose loses nothing to what it leaves out.
- **`catalogue.txt`** names each of the eight queues of
  `harness.domain.ACTIONS` exactly once, at the head of its own line and in
  `ACTIONS`' order. It holds no attribute name, no digit outside the queue
  names, and no value of a tier, product or channel.
- **`prose.txt`** holds no queue identifier, no rule identifier, no attribute
  name and no operator of the DSL.
- **The prompts.**
  - The loop's prompt at level 0 is `SYSTEM_PROMPT_V1`. So is the system prompt
    `results_reuse/run_n2000_r1.json` stored, byte for byte.
  - At every other level, removing §5.5's block gives v1 back, and likewise for
    the compile question.
- **Teeth.** One character changed in a text moves its digest. No two prompts
  share a digest.

**G-g3 — The paths reproduce, without spending.**

- **Shape C, in memory.** An answer holding the hidden policy goes from parse
  to installation to score, and scores 1.0000. An answer that is not an object,
  has no list or has an empty one is an invalid ask. A rule the DSL refuses is
  rejected and counted, and the rest of its list is installed.
- **The requests, through `tests/doubles.py`'s SDK double**, in
  `tests/test_manual.py`, which `G-g1`'s suite runs.
  - **The compile client** sends the model, temperature, reasoning setting and
    `COMPILE_MAX_TOKENS` of §11, and the level's question. Its rows keep every
    attempt's raw text and finish reasons, a cut answer's included.
  - **The proposer `manual/run.py` builds** sends rung 2's request for v1.
    Against a plain `OpenRouterProposer2`, its system message is the level's
    prompt, and nothing else differs.
- **The schedules.** The compile passes and the loop's order are rebuilt from
  `ORDER_SEED` alone. Each level stands at a different place in each of the
  loop's three repetitions.

**G-g4 — The signature**, §11.

---

## 8. Stage A — the design and the references (free, gated)

**Deliverable.** `manual/sample.py` → `results_manual/sample.json`.

- **`G-g1` to `G-g3`.**
- **The design.**
  - The texts and their digests.
  - Every prompt, by shape and level, with its digest.
  - The compile passes and the loop's order, at `ORDER_SEED`.
- **The references, recomputed by this plan's instrument.**
  - **`PLAN_REUSE.md`'s three bases**: `space`, whole and on each half;
    `corpus`; recall of every queue on both surfaces; `K-a`; `O-a`; and `prop`
    by true queue.
  - **The hidden policy**: its scores, and its `K-a`, 0.0769.
- **§5.3's masses, rule by rule**, and the accuracy of each of
  `PLAN_REUSE.md`'s bases over each hidden rule's region. These are `G-g`'s
  reference columns.

**Every figure of Stage A was seen while drafting** (§0). The gate binds it
anyway, because what it protects is the order of events, and Stage A is where
those figures acquire a record that owns them.

## 9. Stage B — the calls (gated on §0)

**B1, shape C.** `manual/ask.py` writes `results_manual/compile_smoke.json`,
then `results_manual/compile_session.json`.

1. `--dry-run` runs `G-g1` to `G-g3` and stops. It never builds the client.
2. `refuse_unsigned`, before the client is constructed. No flag skips it.
3. `reuse.run.key_check`: an API key OpenRouter accepts, and not a management
   key.
4. **The smoke run**: one ask per level, under its own name. It is read before
   the session for the parse, for `finish_reason` against `COMPILE_MAX_TOKENS`,
   and for the provider.
5. **The session**: `ASKS = 5` passes, each asking the four levels in §2.5's
   order. Sequential.
6. Answers are appended to a git-ignored partial file and the same command
   resumes there. Five failed calls in a row stop the session without recording
   them. An answer that parses into an invalid ask is an answer, and is
   recorded.

**B2, shape L.** `manual/run.py` writes `results_manual/loop_smoke.json`, then
`results_manual/loop_L{k}_r{r}.json`.

1. `--dry-run`, the signature and the key, as in B1.
2. **The smoke run**: 20 cases at level 3, the longest prompt. A run refuses
   unless the smoke record exists under this protocol and shows a proposal that
   parsed and a rule born, as `reuse.run.smoke_check` does.
3. **`--level k --rep r`**: one run, the loop of rule A with level `k`'s prompt.
   It refuses unless the compile session's record exists and every earlier run
   of §2.5's order has its record.
4. **The twelve runs take hours between them.** `PLAN_REUSE.md`'s took from a
   few minutes to thirty each. A command longer than about half an hour
   outlives a background command of the agent's harness, so they run in Sergi's
   terminal, with the key loaded as rule 7 says, one after another.

**Both.**

- `harness/call_record.py`'s recorder is installed on every client. Every row
  or escalation keeps its `call_attempts`.
- `tests/test_call_record.py` is taught `manual/ask.py`'s call site. The loop's
  call site is `rung2/proposers2.py`'s, which is already classified.

## 10. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `manual/score.py` → `results_manual/score.json`.

- **Every valid ask and every run, scored on every cell**, by the instrument of
  §0.
- **`G-a` to `G-f`**, each against its line, exactly, with *thin* and
  *unadjudicable* as §0 defines them.
- **`G-g` in full.**

---

## 11. The gate, and where the code lives

**Four modules write this plan's records, and all four refuse while §0 is
unsigned.** `manual/sample.py` and `manual/score.py` spend nothing.
`manual/ask.py` and `manual/run.py` refuse before they construct a client. **The
free stages get the gate because what it protects is not money** but the order
of events.

**The gate reads `PLAN_MANUAL.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called rather than copied.
`MIN_SIGNATURES = 1` today, for §0. An amendment carries its own line and raises
it.

**Constants fixed here, before any figure exists, not to be tuned afterwards,
and pinned by tests:**

- **The client.**
  - `MODEL` and `REASONING` are imported from `reuse.plan`: the model the
    founding runs used, with `PLAN_REUSE.md` §1's amendment.
  - The loop's client is `OpenRouterProposer2` with its own `max_tokens` of
    1,200 and its two retries.
  - The compile client sends `TEMPERATURE = 0`, `COMPILE_MAX_RETRIES = 2` and
    `COMPILE_MAX_TOKENS = 16000`. A whole base of the hidden policy's size is
    a few thousand tokens. OpenRouter's public list gives this model an output
    limit far above that, read on 2026-10-21.
- **The texts**, by digest (§5). The levels, `LEVELS = (0, 1, 2, 3)`.
- **The loop.** `N = 2000`, `SEED = 17`, `REPS = 3` and `SMOKE_N = 20`, imported
  from `reuse.plan`. `LOOP_SMOKE_LEVEL = 3`.
- **The compile session.** `ASKS = 5`, and one ask per level in the smoke.
- **The order.** `ORDER_SEED = 61`, distinct from every seed a closed thread
  uses (17 to 20, 25, 41, 43, 47, 53, 59, and values from 1000 up). It feeds two
  streams, one string seed each. One draws the order of the compile passes and
  the other the order of the loop's repetitions; each is then rotated one place
  per pass or repetition (§2.5). CPython seeds a string through SHA-512, so
  neither depends on `PYTHONHASHSEED`.
- **The limits.** `MIN_SIGNATURES = 1`; `MIN_VALID_ASKS = 3`; `MIN_RUNS = 2`;
  `MAX_CONSECUTIVE_FAILURES = 5`.
- **The lines of §0.** `G_A_LINE = 95/100`; `G_B_LINE = 1/10`;
  `G_C_LINE = 1/2`, held above; `G_D_LINE = 1/10`; `G_E_LINE = 1/10`;
  `G_F_LINE = 1/10`. They are fractions, and every comparison with them is
  exact.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
manual/__init__.py
manual/plan.py        the gate and the constants of §11
manual/texts/         catalogue.txt  prose.txt  rules.txt — §5, frozen
manual/levels.py      the texts and their digests                 [proposer's path]
manual/prompts.py     the loop's prompt and the compile question    [proposer's path]
manual/compile.py     a compile answer, installed into rung 2       [proposer's path]
manual/instrument.py  the scorers of §0, called from rung 2, 3 and the closed threads
manual/gates.py       G-g1 to G-g4; level 3 rebuilt from HIDDEN_DSL
manual/sample.py      Stage A
manual/ask.py         Stage B1: it spends                            [proposer's path]
manual/run.py         Stage B2: it spends                            [proposer's path]
manual/score.py       Stage C
results_manual/FINDINGS_MANUAL.md
results_manual/sample.json  compile_smoke.json  compile_session.json
               loop_smoke.json  loop_L{0..3}_r{1..3}.json  score.json
tests/test_manual.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `manual` joins it in `harness/provenance.py`, and joins the
  oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP`.** The five modules marked above join it, with rule B's
  comment and the test that adds `HIDDEN_DSL`, `ceiling_check` and
  `hidden_priority` to their forbidden imports.
- **The partial files**, `results_manual/*.partial.jsonl`, join `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by two.
- **The call sites** of `tests/test_call_record.py` grow by one.
- **The README's table of writers** gains its rows.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 12. Definition of done

- [ ] Records under `results_manual/` with `_env`, the model, the temperature,
      the reasoning setting, the system prompt and `call_attempts`, produced
      with `PYTHONHASHSEED=0`.
- [ ] `G-g1` to `G-g4` passed before any record was written. The key check and
      the smoke runs came before the sessions, and each smoke record was
      committed before what it opens began.
- [ ] The plumbing of §11, and tests pinning:
      - the constants, the gate, the texts' digests and the prompts' digests;
      - level 3's rebuild and the leak checks of `G-g2`, with their teeth;
      - the unchanged request;
      - the installer's 199 edges;
      - the exactness of §0's comparisons.
      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, its shape, its level and its
      denominator.
- [ ] `results_manual/FINDINGS_MANUAL.md` owns every figure, with a dated
      erratum wherever it corrects something already published.
- [ ] `STATUS.md`: the scoreboard gains the `G` thread. *What is open* gains or
      loses what this plan settles, its second item first.
- [ ] `IDEAS.md`: *Give the proposer the manual* closed or narrowed, with what
      this plan opens. The rung 3 item *Why the proposer did not write correct
      rules for `T3_ENGINEERING` or `ACCOUNT_MANAGER`* is answered or narrowed.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `G`, and its `TABLES` gains
      `FINDINGS_MANUAL.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits; the plan and its
      signature are alone in theirs.

---

## 13. What this plan cannot settle, declared before it runs

1. **Whether real manuals look like this one.** There is one prose manual,
   written by the hand that wrote the policy, with an ambiguity of its
   drafter's choosing. `G-e` is about it.
2. **Whether another model knows more.** One model, as in every thread.
   `CHAT_SUMMARY.md` §3's *another model* stays open.
3. **A trigger that asks.** If a manual makes the proposer write
   `ONCALL_ESCALATION` rules while asked about other tickets, `G-g` shows it.
   Whether a loop would ask about that queue before a rule swallows it is not
   in the rows.
4. **Declaration beyond the keyword, with a manual.** `K-b`'s instrument is
   reported where it has 20 units. Under v1 it has had none, so this plan may
   say nothing new on direction.
5. **What a manual costs a deployment.** Who writes it, who keeps it current,
   and what happens when the policy changes under it: drift is listed under
   *Prior to the four rungs*, and it is not here.
6. **Shape C at another size.** The compile question is one prompt for a
   29-rule policy. A larger one, or one with more queues, may not fit one
   answer.
7. **The pairwise question with a manual.** `ARBITRATION_REPORT.md` §7's P5
   asks which information buys arbitration, pair by pair, at increasing levels.
   This plan's levels are on the policy's side, not the pair's, and P5 stays
   open.
