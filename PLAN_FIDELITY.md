# PLAN_FIDELITY — would the model have decided as its rules do?

**Status: drafted by Claude on 2026-10-01, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**This plan exists because the founding question was answered through a proxy.**
[`PLAN_REUSE.md`](PLAN_REUSE.md) asked it on rung 2's engine and answered it in
the terms it was signed in. The rules get reused (`U-a`), and about three silent
errors in five come from rules born with the wrong queue (`U-c`). But the split
by birth stands in for something it does not measure: whether a compiled rule
decides a later case the way the model would have, had the case reached it. Its
§12.1 declared that before it ran.
[`FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md) repeats it under *What
Stage C does not settle*, and [`STATUS.md`](STATUS.md) lists it fourth under *What
is open*: *it needs the model's answers on cases the rules decided, so it costs
calls.*

**The question, in its cleanest form.** On a case a compiled rule decided, would
the model, asked afresh, have chosen the same queue? And would it have been right
more often than the rule? If it would, compiling loses capability: the loop froze
an answer the model would not give here. If it would not, the limit is what the
model knows, and compiling only preserves it.

**It was first sighted in rung 1, at counts.** [`PREDICTION.md`](PREDICTION.md),
under *What DOES survive*: `SECURITY_INCIDENT` was right 3 of 3 times when the
case reached the LLM, and 0 of 17 when a compiled rule resolved it. That run is
voided by its engine ceiling, and the counts are seventeen cases of one class.
`PLAN_REUSE.md`'s records are the first where the question can be asked of every
decision, on an engine that executes the hidden policy at 1.0000.

**Nothing has to be re-run to ask it.** The three Stage B records of
`PLAN_REUSE.md` hold every case and every rule with its birth. They also hold
every accepted edge in order and every neighbourhood the proposer was shown. From
them the base can be rebuilt at the moment of any case. The drafter has checked
that the rebuilding reproduces the three runs exactly (§0, *already seen*). What
is bought is only the model's answers.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic and its denominator here, before any call.**
Every figure is on the corpus: `generate_corpus(2000, seed=17)` in arrival order,
the cases of `results_reuse/run_n2000_r{1,2,3}.json`. No row has an
exhaustive-space reading. What is asked is the model, about cases that arrived.

**`F-b` to `F-e` are read on the median over the three bases**, each Stage B run
being one base, and each run's own value is published beside it. **`F-a` is read
pooled** over the 135 births of the three runs. It is about one instrument, not
three bases, and run 2 has 31 births, too few to read alone. Every value is
published with its standard error. For the sampled rows it is finite-population,
over each run's decided cases. For `F-a`, which asks every birth, it is the
model's draws alone. **A verdict within one standard error of its line is
labelled *thin* beside the verdict, and the label does not change the verdict.**
For a median,
the standard error used is the median run's. For `F-e`, a count of exactly 1 is
thin. `U-b` and `U-c` sat on their lines with no such label, and the record had
to say so afterwards.

**Every decision row reads the prompt of §2.1's choice B.** That is prompt v1,
unedited, with the base rebuilt at that case's moment and every rule that matches
the ticket left out. To the model the case is then a coverage impasse, which is
what it would have been had no rule covered it. **Every prompt is asked twice**,
in two passes (§2.2). So every row that compares rule with model has the model's
agreement with itself beside it.

Notation, per decision `t`. `r` is the deciding rule's action and `y` the true
queue, both read off the record. `a₁` and `a₂` are the two fresh answers. An
answer is *valid* when its `action` is one of the eight queues (§5.5).

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **F-a** | **The instrument has not moved since it wrote the rules.** Re-asked a birth prompt verbatim, the model agrees with the answer it gave on 2026-09-30 as often as it agrees with itself now | over the 135 birth escalations of Stage B whose two fresh answers are both valid: `S − A`. `S` is the share whose two fresh answers agree. `A` is the mean, over prompts and draws, of agreement between a fresh answer and the recorded one | **≤ 0.05** | **> 0.05** |
| **F-b** | **Compiled rules decide unlike the model would.** The deciding rule agrees with the model asked afresh markedly less often than the model agrees with itself | over each run's uniform sample of decided cases (§2.3) whose two answers are both valid: `S − A`, where `S` is the share with `a₁ = a₂` and `A` the mean of `½(1[a₁=r] + 1[a₂=r])` | **≥ 0.10** | **< 0.10** |
| **F-c** | **Compiling loses capability.** Asked afresh, the model would have been right more often than the rule that decided the case | the same denominator: the mean of `½(1[a₁=y] + 1[a₂=y])`, minus the share with `r = y` | **> 0** | **≤ 0** |
| **F-d** | **Most of the silent error is the model's own.** On the cases a rule decided wrongly, the model asked afresh would mostly be wrong too. This is `U-c`'s claim, measured instead of proxied, against `U-c`'s line | over the sampled decisions with `r ≠ y` and both answers valid: the mean of `½(1[a₁≠y] + 1[a₂≠y])` | **≥ 0.60** | **< 0.60** |
| **F-e** | **The rarest queue was lost to compilation, not to the model.** Asked about the tickets the rules swallowed, the model names `ONCALL_ESCALATION` | of the 7 `ONCALL_ESCALATION` tickets, all decided by a rule in every run and asked as a census (§2.3): the number on which **both** fresh answers name `ONCALL_ESCALATION` | **≥ 1** | **0** |
| **F-f** | *Reported, not adjudicated.* **What the screen holds, and the model without it** | Stage A, free: the replay, what each design of §2.1 would put on the screen, the concentration of decisions over rules, and two free baselines for the B arm. Stage C: the ticket-only arm, if §2.1 adopts it | — | — |

**Signed by Sergi: ________________________ (date: ______________)**

**Why `F-f` cannot carry a band.** Part of its free half is figures the drafter
has already computed (below). The rest is computable from data already on disk.
The D entry of [`IDEAS.md`](IDEAS.md) settled that case for `D-d`: no honest band
can be written for such a figure. Its paid half, the ticket-only arm, is optional
(§2.1). It is a diagnostic for reading `F-b` to `F-e`, not a claim of its own.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the records publish.** Everything `STATUS.md`, `FINDINGS_REUSE.md` and
  `PLAN_REUSE.md` publish, including every per-run figure of Stage C. That covers
  e2e, silent error and the proposer's accuracy at its escalations (0.4839,
  0.4839 and 0.5476), the two rare-class ledgers and the edges.
- **The three records themselves.** Their `_env`, `gates` and `metrics` blocks,
  and one rule and one case of each, read to learn the format.
- **The hidden policy's source**, read for the rules that route the two rare
  queues (`H01`, `H02`, `H04`, `H05`), and the arrival weights in
  `harness/domain.py`.
- **The escalations of rung 1's `results/llm_run.json` at severity 1**, and its
  answers naming `ONCALL_ESCALATION`.

**And the outputs of a scratch probe the drafter ran on 2026-10-01, which is not
in the tree and owns nothing.** That is the situation
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §3 put itself in, and it is closed
the same way. Stage A's module measures every figure below under the gate, and
its record owns them (`F-f`). A figure that does not reproduce is an erratum to
this section, not a silent edit.

- **The replay.** Each run was rebuilt case by case from its record alone: rules
  at their births, accepted edges in `edge_log` order, fire counts as they accrue.
  In all three runs the rebuild reproduces every outcome, winner and number of
  matched rules. It reproduces every escalation's neighbourhood, ids and kind,
  every edge verdict, and every rule's final counts. **Without the edges it
  diverges on 74, 32 and 122 cases, so the check has teeth.**
- **What v1 would show on each decided case.** There are 1,938, 1,969 and 1,958
  of them, 5,865 in all. Under each design of §2.1:
  - **A.** The deciding rule is on the screen in **5,864 of 5,865** and first in
    the list in **5,498**.
  - **B′.** Another rule that matches the ticket is still on the screen in
    **1,002**. In 1,000 of those, a rule on the screen carries the deciding
    rule's action.
  - **B.** At least one shown rule carries the deciding rule's action in
    **5,398**, and that action is a plurality action of the screen in **3,363**.
    A shown rule's edge annotation cites a hidden rule in **2,154**.
- **How the proposer used its screen at the real births.** Of the 135 births, 132
  had a screen. On the **85 coverage screens**, its answer was some shown rule's
  action in 73 and a plurality action in **61**, and it was right 48 times (16 of
  31, 13 of 25 and 19 of 29). On the **47 conflict screens** the numbers are 47,
  44 and 20. In 72 of the 132 a shown rule's edges cite a rule that is not shown.
- **The concentration of decisions.** 33, 26 and 31 rules decide anything. 8, 5
  and 6 rules decide half the decisions, and 18, 11 and 14 decide four fifths.
  The top five carry 0.41, 0.53 and 0.49 of them.
- **The decided cases crossed by birth and outcome.** This is `U-c`'s split
  recomputed, and it agrees with it:

  | run | born right: rule right | born right: rule wrong | born wrong: rule right | born wrong: rule wrong |
  |---|---|---|---|---|
  | 1 | 518 | 404 | 269 | 747 |
  | 2 | 658 | 433 | 222 | 656 |
  | 3 | 807 | 384 | 219 | 548 |

- **`ONCALL_ESCALATION`.**
  - **The tickets.** All 7 are severity 1: four enterprise (`H04`) and three
    business off hours (`H05`).
  - **Who decided them.** In every run, four were decided by `R0001`,
    *enterprise, any severity → `T1_GENERAL`*, born at case 0. In run 1 that rule
    decided 110 cases and was right on 20. The other three were decided by rules
    sending one product at severity ≤ 3 to `T2_TECHNICAL`.
  - **No base of this plan contains an `ONCALL_ESCALATION` rule.** No proposal in
    any Stage B run, smoke run or August n=100 run named that queue.
  - **Rung 1's proposer**, a different prompt with no base shown, named it on 7
    of its 14 severity-1 escalations. All 7 were free or pro tickets whose true
    queue is `T2_TECHNICAL`. One of them is case 74, and under v1 with a screen,
    run 1 of Stage B sent that same ticket to `T2_TECHNICAL`.
- **`SECURITY_INCIDENT`.** Run 2's rules sent the class's 11 wrong decisions to
  `T2_TECHNICAL` (7), `BILLING_SPECIALIST` (2) and `T1_GENERAL` (2). At the 20
  escalations of the class across the three runs, the proposer chose
  `SECURITY_INCIDENT` 19 times.
- **The prompts' size.** A B prompt has a median of 4,165 to 4,330 characters by
  run, system prompt included. At the births the median is 4,047 to 4,193.
- **The pace of earlier paid sessions**, from their records:
  - Stage D of the pairwise thread: 400 calls in 3,045 s.
  - Its extension: 1,200 calls in 15,087 s.
  - Runs 2 and 3 of Stage B: under about 9 s per call, bounded by their `_env`
    timestamps.
  - Run 1: about thirty minutes for 62 calls.

**Not seen, because nobody has computed them**: any answer of the model on a case
a rule decided, under any prompt; any re-ask of a birth prompt; and the accuracy
of any free baseline on the decided cases. That last means what a model would
score if it copied the plurality or the first rule of its screen. It was left
uncomputed on purpose, so that Stage A can publish it as `F-f`'s baseline without
its author having seen it.

**What the drafter expects, written down so the scoreboard can score it.** **All
five hold.** The drafter trusts `F-d` least, then `F-e`, then `F-c`.

- **`F-a`.** The model, the prompt and the setting are the ones that produced the
  records, days apart. `B-a`, the pairwise thread's row on whether its instrument
  moved, held.
- **`F-b`.** On 3,363 of 5,865 decisions the deciding rule's action is a plurality
  action of the B screen. At 61 of 85 coverage births the proposer answered with
  such an action. A model that answers from its screen that often will part from
  a hidden rule on much of the rest, while mostly agreeing with itself.
  Expected: well above 0.10.
- **`F-c`.** Two pulls, in opposite directions:
  - **Toward a loss.** The broad early rules froze one ticket's answer over many,
    as `R0001` shows, and a model asked about each ticket should do better there.
  - **Toward no loss.** With the deciding rule hidden, the model leans on the
    rules near it, which cover other regions. That should cost it where the
    deciding rule was right.

  The only numbers on record are naive. Take the proposer's accuracy at its
  escalations minus the rules' accuracy where they decide. Over all escalations
  that gives +0.0778, +0.0370 and +0.0236. Over coverage escalations alone it
  gives +0.1100, +0.0731 and +0.1312. Both compare different populations.
  Expected: a positive margin, possibly thin.
- **`F-d`.** Three silent errors in five come from rules born wrong. A model wrong
  about a ticket's queue at birth is likely to be wrong the same way about its
  neighbours. The systematic errors the pairwise thread measured point the same
  way: it follows a fixed queue ranking
  ([`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §2;
  [`FINDINGS3.md`](results3/FINDINGS3.md) §15). But a model right at 48 of 85
  coverage births leaves room for many of the scope errors not to be its own.
  Expected: about the line, a little above it.
- **`F-e`.** The seven tickets are critical, four of them enterprise. The system
  prompt glosses severity 1 as *critica* and lists the queue, and rung 1's
  proposer named it on half its non-security severity-1 escalations. Against
  that, no B screen carries the queue, and the proposer answers from its screen
  most of the time. Case 74 went from `ONCALL_ESCALATION` under rung 1's prompt
  to `T2_TECHNICAL` under v1. Expected: a count of one or two. **This row is
  argued from another prompt's behaviour, the way `U-d` was argued from the
  hidden policy's rules, and `U-d` is the row that was refuted.**

**The drafter's record argues against most of that.** On `STATUS.md`'s scoreboard
18 of 41 adjudicated rows were refuted. The ILP thread's drafter expected all four
of its rows to hold, and one did. The `U` thread's drafter expected four holds out
of five and got three of the five verdicts right. The row it argued from the
hidden policy's own rules was the one refuted. Five expected holds out of five is
that profile, only stronger.

Three things were done about it, rather than said:

1. **Every line is the claim's own edge**, not a number chosen to clear.
   `F-c`'s is the literal *more often*, `F-d`'s is `U-c`'s line, and `F-e`'s is
   `U-d`'s.
2. **The sample size of §2.4 puts `F-c`'s line at least 2.5 standard errors**
   from the smaller naive value.
3. **A verdict inside one standard error of its line is labelled thin in
   advance.**

`F-a` is an argument for continuity, across dates rather than surfaces. The
standing note in `IDEAS.md` was written about surfaces, but it is the nearest
record this drafter has: its arguments for continuity have been the ones that
lost. Sergi should read these bands as more likely too comfortable than too
strict, and tighten them at signature where he disagrees, as he did with `A-b`
and `A-d`.

**How the rows read together.** Split the sampled decisions into four cells:
both right, rule wrong and model right (a *loss*), rule right and model wrong (a
*gain*), and both wrong. Then `F-c` is loss minus gain, and `F-d` is how much of
the rule-wrong mass the model shares. They are not one position taken in two
halves, and every combination reads:

- **Both hold.** Compiling loses a little, and most of what the rules get wrong
  the model would too.
- **`F-c` holds and `F-d` is refuted.** This is the strong form of *compiling
  loses capability*.
- **`F-c` is refuted and `F-d` holds.** This is the clean form of *the limit is
  what the model knows*.
- **Both are refuted.** The rules trade errors with the model.

`F-b` is the half of the question that needs no labels. `F-a` says whose answers
the other three are compared with. If it is refuted, `F-b` to `F-d` are still
adjudicated as signed, and each carries the birth arm's gap beside it, the way
`U-a` carried the share of CONFLICTs.

---

## 1. What is being bought, and what is already paid for

**Already paid for, and free to read: the three Stage B records** of
`PLAN_REUSE.md`, `results_reuse/run_n2000_r{1,2,3}.json`. They are rung 2's loop
over the 2,000 cases of seed 17, with prompt v1 and reasoning off; all 135
proposals parsed. They are inputs, never outputs: nothing under `results_reuse/`
is written by this plan. Without a call they hold everything the prompts need,
and the answers the model gave at the 135 births, which is what `F-a` compares
with.

**Bought: the model's answers, under prompt v1, on prompts rebuilt from those
records.** Nothing about the client moves from Stage B. The client is
`OpenRouterProposer2(model="deepseek/deepseek-v4-flash", prompt_version="v1",
reasoning={"effort": "none"})`, and its `propose` is called as the loop calls it:
temperature 0, 1,200 tokens, `response_format` on the first attempt, two retries.
Hard rule 5 is untouched: no prompt text and no schema change. Two things change:

- **The base each prompt is built from** (§2.1).
- **Nothing the model writes enters any engine.** Its rule is recorded and
  discarded, and only its `action` is read.

Four arms, all sequential, in this order:

| arm | what is asked | prompts | draws | calls |
|---|---|---|---|---|
| smoke | five items of each arm below, at least one birth on a conflict screen | 15 | 1 | 15 |
| births | the 135 birth prompts of Stage B, rebuilt verbatim — `F-a` | 135 | 2 | 270 |
| decisions | per run, 600 decided cases drawn uniformly, plus every `ONCALL_ESCALATION` and `SECURITY_INCIDENT` decision the draw missed — `F-b` to `F-e` | 1,800 + ≈ 42 | 2 | ≈ 3,684 |
| ticket only | the first 100 of each run's draw, once, and the 27 rare-class tickets, twice, under v1 with an empty base — `F-f`, if §2.1 adopts it | ≤ 300 + 27 | 1 or 2 | ≤ 354 |

**Cost: about 4,300 calls, or about 3,950 without the ticket-only arm.** That is
one call per prompt and draw, plus any parse retries. All 135 of Stage B's
proposals parsed, and its prompts were the size of these.

**Time, not money, is the constraint**, and the earlier paid sessions disagree by
a factor of nearly four:

| session | pace | owner |
|---|---|---|
| Stage D, pairwise thread | 7.6 s per call | `results2/pair_judgement_learned.json` |
| its 1,200-call extension | 12.6 s per call | `results2/pair_judgement_1600.json` |
| Stage B, runs 2 and 3 | under about 9 s per call | their records' `_env` timestamps |
| Stage B, run 1 | about 29 s per call: *about thirty minutes* for 62 calls | `FINDINGS_REUSE.md`, Stage B |

**Planned on the longest session, at 12.6 s: about 15 hours of calls,
sequential (hard rule 3).** At Stage D's pace it is 9 hours; at run 1's, 35.
That is why §8 splits Stage B into separate sessions, each committed before the
next.
It is also why a session must survive an interruption without losing what it paid
for.

---

## 2. The choices that have to be made at signature time

Five choices, and none of them moves a band. **Signing §0 adopts the drafter's
choice in each unless the signature line says otherwise.**

### 2.1 What the model is shown when re-asked — the drafter recommends **B**

The four designs below were measured on the records before drafting (§0,
*already seen*). All of them are built with rung 2's own `neighbourhood` and
`render_base_v1`.

- **A — v1 with the base at that moment, as it stands.** This is closest in
  letter to *what it would have answered had the case escalated*, and it is
  unusable. The deciding rule matches the ticket, so it violates no condition and
  sorts first. It is on the screen in 5,864 of 5,865 decisions and first in 5,498.
  It sits under v1's coverage header, *ninguna casa este ticket*, which is then
  false. Agreement would be measured against an answer key printed in the prompt.
- **B′ — the same, with the deciding rule hidden.** Another rule that matches the
  ticket is still on the screen in 1,002 decisions, under the same false header.
  In all but two of them, a rule on the screen carries the hidden rule's action.
- **B — the same, with every rule that matches the ticket hidden.** This is the
  smallest change that makes the case what it would have been had no rule covered
  it: a coverage impasse.
  - **What is on the screen.** The twelve nearest rules of the base at that
    moment, ordered as v1 orders them, under a header that is now true.
  - **What does not change.** The system prompt, the template and the renderer
    are untouched. The screen is of the kind the model saw at every coverage
    birth.
  - **Edges.** They are rendered as v1 renders them, so a shown rule can cite a
    hidden one. That happens on 2,154 of the 5,865 screens. At 72 of the 132 real
    births with a screen, a shown rule already cited a rule that was not shown.
- **C — v1 with an empty base: the ticket only.** This is not a new prompt. It
  is exactly what case 0 saw in every run, *BASE DE REGLAS: vacia*. But it asks
  a different question: what the model knows about the ticket when no compiled
  rule has shaped its screen. That is the alternative to compiling at all. Its
  prompt depends only on the ticket.

**Why B and not C for the rows.** The question is about compilation: whether a
rule's frozen answer is the answer the model would give on a later ticket. B
holds the elicitation constant in kind with the births that wrote the rules: the
same prompt and a screen of nearby rules. What differs between rule and fresh
answer is then the ticket and the moment, which is what compiling freezes. C
changes the information as well, and a gap under C would mix compilation with
context.

**Why C anyway, as a reported arm.** At 61 of 85 coverage births the proposer
answered with a plurality action of its screen, and no base of this plan holds an
`ONCALL_ESCALATION` rule. So under B, part of *the model* is the base it is
shown. A refutation of `F-c`, *the limit is what the model knows*, could then
mean the model or its screen. **The drafter recommends running C once on the
first 100 decisions of each run's draw, and twice on the 27 rare-class tickets.
That is at most 354 calls, about 75 minutes at 12.6 s, reported under `F-f` and
adjudicating nothing.** Dropping C at signature removes those calls and that
reading, and nothing else.

### 2.2 The baseline for agreement — two draws of every prompt, in two passes

The model is not deterministic at temperature 0 (`CLAUDE.md`, Step 3), so
rule–model agreement means nothing alone. **The baseline is exchangeability.**
Suppose a compiled rule's action were just one more draw of what the model says
about this ticket. Then, in expectation, the rule would agree with a fresh answer
exactly as often as two fresh answers agree with each other. `F-b` is the
distance from that. `F-a` applies the same identity to the births, where the
recorded answer *is* such a draw unless the instrument moved.

Every prompt is therefore asked twice, in **two passes over the session's items,
each in its own seeded order**. The two answers to one prompt are separated by a
whole pass rather than sent back to back.

**The cheaper alternative, not recommended.** A second draw on only the first 200
of each run's draw would save about 1,200 calls, about four hours at 12.6 s. It
would cost two things:

- **`F-b`'s denominator would shrink to those 200.**
- **Precision for `F-c` and `F-d` would depend on an unknown.** They lose almost
  nothing only if the model mostly agrees with itself, and how much it does is
  what nobody knows yet.

The drafter recommends two draws on every decision. Then `F-b` to `F-d` share one
denominator, and `F-e` needs two draws anyway. This house's drafting defects have
come from denominators more often than from budgets.

### 2.3 Which decisions — uniform over decisions, per run; the rare classes as a census

The question is about decisions: what the system did on the cases that arrived.
So **the sample is uniform over each run's decided cases, without replacement**,
at a seed declared in §10.

**Why not stratified by deciding rule.** A few rules carry most decisions: 8, 5
and 6 rules decide half of each run's decisions. Stratifying by deciding rule
would spread the calls over the 33, 26 and 31 rules that decide anything. It
would answer a different question, how many rules are faithful, which is how
`reuse_rate` counts. And it would need weights to answer this one.

**What uniform gives.** It is unbiased for each base as it stands, and the
standard error is the finite-population one, because decisions are sampled, not
rules. What the concentration does cost is reach into small rules. So Stage C
publishes per-rule figures for every rule with at least 20 sampled decisions,
outside every denominator, and the split by birth beside every row.

**Each run is drawn independently** rather than at shared case indices. Shared
indices would pair the bases by ticket and make the three values more comparable,
but they would correlate the three values' errors. The median adjudicates, and it
gains more from three independent draws than from comparability.

**The rare classes are a census, counted and never rated** (`PLAN_REUSE.md`
§5.6). Every `ONCALL_ESCALATION` decision is asked: 7 per run, the same seven
tickets. So is every `SECURITY_INCIDENT` decision: 5, 17 and 18. This holds
whether or not the uniform draw reached them. A case reached by both is asked
once and read by both. The census feeds `F-e` and the counts beside it. It
enters the uniform rows' denominators only where the draw reached it.

### 2.4 How many — 600 decisions per run

**Chosen so that `F-c` can be adjudicated, the way `PLAN_PROPOSER_1600.md` chose
1,600.** `F-c`'s line is 0. The smaller of the two naive values of §0 has a median
of +0.0370, and it is the one used here, because it is the harder to separate
from the line.

`F-c`'s per-decision difference lies in [−1, 1] and is non-zero only where the
model and the rule differ in correctness. If they differ on about a third of
decisions, its standard deviation is at most about 0.6. The finite-population
standard error per run is then at most:

| per run | `F-c` | `F-b` | `F-d` | median of three, `F-c` | +0.037 from the line, in median s.e. |
|---|---|---|---|---|---|
| 400 | 0.027 | 0.022 | 0.030 | 0.018 | 2.1 |
| **600** | **0.020** | **0.017** | **0.023** | **0.014** | **2.7** |
| 800 | 0.016 | 0.014 | 0.019 | 0.011 | 3.4 |

This is planning arithmetic, not figures. Three assumptions lie behind it:

- **`F-b`** has a standard deviation of at most 0.5. Its per-decision value is
  near 1 where the model's usual answer differs from the rule and near 0
  elsewhere.
- **`F-d`**: about 54% of decisions are silent errors, as the three runs have it.
- **The median** assumes the three runs share one value.

**600 is the smallest of the three at which the line and the naive value are 2.5
median standard errors apart**, the separation `PLAN_PROPOSER_1600.md` §3 bought.
Each step up costs about 1,200 calls, about four hours at 12.6 s.

**`F-a` has no sample to size.** It asks all 135 births, so its only noise is the
model's draws, and how much noise that is depends on how often the model agrees
with itself, which nobody knows yet. Simulated with every prompt alike, a model
that did not move would still cross the line by chance:

| model agrees with itself | standard error of `S − A` | chance refutation |
|---|---|---|
| 0.94 | 0.018 | under 1 in 100 |
| 0.90 | 0.023 | about 1 in 50 |
| 0.81 | 0.031 | about 1 in 20 |
| 0.65 | 0.039 | about 1 in 10 |

So a refutation of `F-a` weighs less the less the model agrees with itself. Stage
C publishes `S` beside it, so the reader can see which row of this table the run
landed on. The line stays at 0.05, because drift of that size would already be
half of `F-b`'s line.

### 2.5 `PREDICTION.md`

Step 4 of `CLAUDE.md` puts Sergi's own prediction before a long run, by hand.
Hard rule 2 keeps the model out of that file. So this plan drafts no entry there,
and its gate does not look for one. §0 is a different instrument: the drafter's
bands, for the scoreboard. Whether this plan also gets a dated entry in
`PREDICTION.md` is Sergi's to decide.

---

## 3. Reference figures, with the record that owns each

All on the corpus. Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| the six `U` rows | §0 of `PLAN_REUSE.md` | reuse 0.7381; `U-c` 0.6024; `ONCALL_ESCALATION` never escalated | `results_reuse/score.json`, `FINDINGS_REUSE.md` |
| decided cases | 1,938 / 1,969 / 1,958 | per run, `coverage` × 2,000 | `results_reuse/run_n2000_r{1,2,3}.json`, `metrics` |
| the rules' accuracy where they decide | 0.4061 / 0.4469 / 0.5240 | one minus `silent_error_rate` | same |
| the proposer's accuracy at its escalations | 0.4839 / 0.4839 / 0.5476 | `proposal_action_accuracy`, over 62 / 31 / 42 escalations | same |
| the naive comparison | +0.0778 / +0.0370 / +0.0236 | the row above minus the one before. Different populations. **Arithmetic on two figures, owned by neither** | — |
| rung 1's accuracy at its escalations | 0.3877 | the same operation under another engine and prompt; `ARBITRATION_REPORT.md` §7, P1's second objection | `results/llm_run.json` |
| rung 1's rare-class counts | 3/3 and 0/17 | `SECURITY_INCIDENT` right when the case reached the LLM, and when a compiled rule decided it | `PREDICTION.md` |
| the rare classes | 20 and 7 | `SECURITY_INCIDENT` and `ONCALL_ESCALATION` among the 2,000 | `results3/FINDINGS3.md` §2 |
| a queue ranking, followed | 0.8073 | the proposer's pairwise answers follow a fixed ranking of the queues, so its errors are systematic | `results3/FINDINGS3.md` §15 |
| the pace of paid sessions | 7.6 s and 12.6 s per call | 400 calls in 3,045 s; 1,200 in 15,087 s | `results2/pair_judgement_learned.json`, `results2/pair_judgement_1600.json` |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and `harness/dsl.py` and touches neither. If a frozen file
   has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Nothing here is a loop: no rule is added, so no answer
   changes the next prompt, and concurrency would not break semantics the way it
   would in the loop. The calls are sequential anyway. The order of a record is
   part of it, the two passes are defined by time, and the sessions run one after
   another, never side by side.
4. **Seed 17, no regeneration, and `results/llm_run.json` is read-only**, like
   every record under `results_reuse/`. `harness/record_guard.py` guards this
   plan's paid records. The flag that overrides it is not typed without Sergi
   asking.
5. **Do not adjust the prompt or the schema.** v1 stays as it produced Stage B's
   records: not edited, not translated, not reformatted. Which rules are on the
   screen is §2.1's design, signed here. It is the only thing about the prompt
   this plan decides.
6. **If the numbers come out badly, report them.**
7. **The API key goes in the environment.** Load it with `eval "$(grep -m1
   '^export OPENROUTER_API_KEY=' ~/.bashrc)"` and check it with
   `${#OPENROUTER_API_KEY}`. Before any call, read it off OpenRouter's key
   endpoint as an API key and not a management key (§8).

And this plan's own, lettered:

A. **The proposer and the renderer are rung 2's, called and not copied**:
   `OpenRouterProposer2.propose`, `neighbourhood`, `render_base_v1`, `user_msg`
   and `SYSTEM_PROMPT_V1`. A reimplementation would make these answers
   incomparable with the births for a reason that has nothing to do with the
   model.
B. **The Stage B records are inputs, never outputs.** Nothing under
   `results_reuse/` is written by this plan. Every label it reads comes from
   them: `truth`, `correct`, `predicted`, `winner_id`. No module of this plan
   imports the oracle.
C. **Every new record carries `_env` and the reasoning setting.** Every command
   runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded and never executed.**
   No answer of this plan becomes a rule in any engine.

---

## 5. Known traps

**5.1 — The deciding rule on the screen.** Under design A the answer key is in
the prompt (§2.1). The check of §6 that B's screens hold no rule matching the
ticket is what keeps it out. It runs on every prompt, not on a sample.

**5.2 — Copying the screen is not a defect of B: it is part of what is
measured.** At 61 of 85 coverage births the proposer answered with a plurality
action of its screen. B shows the model what a coverage impasse at that moment
would have shown, so an answer copied from the screen is the answer it would have
given. Two things separate the model from its screen:

- **The ticket-only arm**, which is reported, not adjudicated.
- **Stage A's free baselines**, the screen's plurality action and its first
  rule's action, which say what pure copying would score.

**5.3 — Two baselines, for two different noises.** Self-agreement measures the
model against itself on one day. The birth arm measures it against the model of
2026-09-30. The rules were written by the model of 2026-09-30 and are compared
with today's. So `F-b` is read against the first baseline and qualified by the
second.

**5.4 — Exchangeability, and what a negative gap means.** Under perfect fidelity
`S − A` is zero in expectation, not exactly. A negative gap is possible: a rule
that holds the model's usual answer while the model itself wavers. That is a
result, not an error.

**5.5 — Invalid answers.**

- **What counts.** An answer counts if its `action` is one of the eight queues,
  whether or not the rule written with it would validate. That is how the loop
  scores `proposal_action_correct`.
- **What does not.** A failed call, or an action outside the eight, leaves the
  decision out of every denominator that needs it. The count is published.
- **When a run's value is undefined.** If more than 5% of a run's sampled
  decisions lack a valid pair, that run's value is undefined. If no run has one,
  the row is unadjudicable and the record says so.

Stage B parsed 135 of 135 with reasoning off.

**5.6 — Seven tickets.** `F-e` is a count over seven tickets, deliberately: a rate
over seven is noise, and whether the model names the queue at all is an event.
The seven are the same tickets in every run, under three different screens. So
the three runs are not independent draws of `F-e` the way they are of the uniform
rows.

`SECURITY_INCIDENT`'s decisions are counted beside it and not adjudicated. Eleven
of its forty were wrong, all in run 2, so a median over runs cannot read them.

**5.7 — The fire counts order the screen.** v1 breaks ties among equally near
rules by fire count at that moment, then by birth. The replay rebuilds those
counts case by case. §6's check that every recorded neighbourhood reproduces is
what tests it, 135 times, with the edges in.

**5.8 — Long sessions.** A base's session is about 1,230 calls. A session that
dies keeps what it paid for:

- **Answers are appended as they arrive.**
- **A restart under the same protocol resumes**, and the final record says where.
- **A restart is not a re-draw.** No prompt already answered in a pass is asked
  again in that pass.

**5.9 — The model can change under its name, and date is not the only route.**
OpenRouter routes a model name to providers. This plan, like Stage B, does not
pin one. `F-a` measures the combined drift and cannot apportion it.

**5.10 — The rule the model writes is not the question.** Fidelity of scope is
whether its fresh rule would cover the same region as the compiled one. Every
payload is kept, and none of this is scored (§12.4).

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.** Of the last three plans, two had their declared method killed by
a check like these, and one passed. What could be checked before drafting was, so
that a failure would become a fix to this draft rather than a signed amendment:

- **`F-g1`'s record half** passed in `PLAN_REUSE.md`'s own Stage C
  (`FINDINGS_REUSE.md`, Stage C).
- **`F-g2` and the screen half of `F-g3`** passed in the drafter's scratch probe
  (§0).
- **The rest** needs the modules: the suite with them in it, the prompt builders
  against the double's requests, and the draw.

- **F-g1 — The inputs reproduce themselves.** `python3 -m unittest discover` is
  green. Each Stage B record passes `PLAN_REUSE.md`'s own check, with
  `reuse.gates.check_record` called rather than copied:
  - its metrics and fire counts recompute from its cases;
  - every rule has one birth;
  - the corpus redrawn at seed 17 carries the same labels.
- **F-g2 — The replay is exact.** Each run is rebuilt case by case from its
  record alone, and the rebuild reproduces all of the following:
  - every outcome, winner and number of matched rules;
  - every escalation's neighbourhood, ids and kind;
  - every edge verdict, in `edge_log` order;
  - every rule's final fire and correct counts.

  The rebuilt system prompt is byte-identical to the record's `system_prompt`.
  **And the check has teeth**: a test rebuilds without the edges and must see it
  fail.
- **F-g3 — The prompts and the sample are what §2 signs.**
  - **B prompts.** Every one holds no rule that matches its ticket, carries v1's
    coverage header, and never shows the deciding rule.
  - **Ticket-only prompts.** Every one is v1's empty-base rendering.
  - **Birth prompts.** Every one is what the loop sent. The builder is checked
    against the requests rung 2's loop builds when `tests/doubles.py` replays the
    four v1 n=100 records.
  - **Labels.** No prompt builder takes a label.
  - **The draw.** It has 600 distinct decided cases per run, at the seed of §10.
  - **The census.** It holds every `ONCALL_ESCALATION` and `SECURITY_INCIDENT`
    decision of each run.
  - **Every decision row's population is populated.** Each run's draw holds at
    least 100 silent errors for `F-d`, or `F-d` is declared unadjudicable before
    a call is made.
- **F-g4 — The signature**, §10.

---

## 7. Stage A — the draw, the checks and the free readout (free)

**Deliverable.** `fidelity/sample.py` → `results_fidelity/sample.json`.

**What it does.**

- **`F-g1` to `F-g3`.**
- **The draw of §2.3** at `SAMPLE_SEED`, with the census added and the two
  passes' orders at `ORDER_SEED`.
- **The ticket-only subsample**, if adopted.
- **`F-f`'s free half.** Every figure §0 lists as *already seen* from the scratch
  probe, now measured by a module and owned by this record.
- **Two baselines for the B arm, on the sampled decisions.** One is the plurality
  action of the screen, with ties going to the action shown first. The other is
  the first shown rule's action. For each, the record gives its agreement with
  the deciding rule and its accuracy. They are what a model that only copied its
  screen would score: the role the free queue ranking played for `B-b`. Nobody
  has computed their accuracy.

**It produces nothing adjudicable**, and it runs after §0 is signed so that none
of its figures can inform a band.

---

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `fidelity/ask.py` → `results_fidelity/ask_smoke.json`,
`ask_births.json`, `ask_base1.json`, `ask_base2.json`, `ask_base3.json` and, if
adopted, `ask_ticket_only.json`.

**Six sessions, in that order, one after another, or five if §2.1's arm C is
dropped. Each record is committed before the next session starts.** Births come
before the bases, so that the instrument
is measured before most of the spend. `F-a`'s verdict stops nothing, whatever it
is: it qualifies the reading of `F-b` to `F-d` (§0).

**Every session, before any call**, follows the order `reuse/run.py` fixed after
Stage B's first two smoke runs:

1. **`--dry-run`** runs `F-g1` to `F-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`F-g4`).** While `PLAN_FIDELITY.md` carries a blank
   signature line, the module exits here.
3. **The smoke record**, for every session but the smoke run. It must be under
   this plan's protocol (model, prompt, reasoning setting, seed) and show at
   least one valid answer for each kind of prompt the session will ask.
4. **The key**, read off OpenRouter's key endpoint, which is free. The endpoint
   must answer 200 and must not call it a management key. This is
   `reuse.run.key_check`, called rather than copied. A 200 alone proves nothing
   (`CLAUDE.md`, rule 7).
5. **`F-g1` to `F-g3`**, blocking.
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls.** They are sequential. Every call carries
   `reasoning: {"effort": "none"}`, and every record says so.

**The smoke run** asks five items of each arm once, at least one of them a birth
on a conflict screen. It checks the client, the key and the shape of the record,
and adjudicates nothing. Its answers enter no row.

**What each record carries, per call:**

- **Which call.** The arm, the run, the case, the pass and the position in it.
- **The prompt.** A digest of the prompt and the ids on its screen.
- **The answer.** Its `action` and payload, or the failure.
- **The labels.** The deciding rule's action and the true queue, copied from the
  Stage B record and never computed.

---

## 9. Stage C — scoring, and the five adjudications (free)

**Deliverable.** `fidelity/score.py` → `results_fidelity/score.json`, and
`results_fidelity/FINDINGS_FIDELITY.md`, which owns every figure.

- **`F-a`** from the births record, pooled, with each run beside it.
- **`F-b`, `F-c` and `F-d`** per run from its base's record; the median
  adjudicates.
- **`F-e`** from the census.

Each comes with its standard error and, where it applies, the label *thin*.

**Also record, outside every denominator:**

- **The parts of each row.** `S` and `A` separately, and the model's and the
  rules' accuracies, beside one another and never summed.
- **The four cells of §0's decomposition**: both right, loss, gain and both
  wrong, with how often *both wrong* is the same wrong queue.
- **Every row split by the deciding rule's birth**, right or wrong.
- **The proxy against the measurement.** On the silent errors, how often `U-c`'s
  split by birth and `F-d`'s fresh answers agree on whose error it was.
- **Per rule.** Agreement and difference for every rule with at least 20 sampled
  decisions.
- **Disagreement as an alarm.** The rules' error rate where the fresh answers
  disagree with them, and where they agree. Agreement needs no label, so this is
  the precision a deployed system would get from re-asking its own decisions.
  The loop escalates only on coverage or conflict, never on a wrong answer
  ([`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §3, level 3). This is the
  kind of detector [`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §1 says partitioning
  removes. It is recorded, not built.
- **`F-a`'s accuracy beside its agreement.** The recorded answers' accuracy at
  the births, against the fresh answers'.
- **The rare classes, in counts.** The `SECURITY_INCIDENT` census, above all run
  2's eleven wrong decisions, and the `ONCALL_ESCALATION` answers by queue.
- **`F-f`.** Stage A's baselines beside the model. And the ticket-only arm, if
  run: its accuracy, its agreement with the rule and with the B answers on the
  same tickets, and the 27 rare-class tickets' answers, in counts.
- **The run itself.** Failed calls, invalid actions, how many written rules would
  validate, and the pace per session.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `fidelity/sample.py` and `fidelity/score.py` spend nothing.
`fidelity/ask.py` refuses before it constructs the client. **The free stages get
the gate because what it protects is not money** (`PLAN_SENSITIVITY.md` §8).
Stage A's baselines are exactly what would inform `F-c`'s band. Without the gate,
the only thing between them is commit order.

**The gate reads `PLAN_FIDELITY.md` and no other plan, and it counts every
signature line** rather than stopping at the first. Every line starting
`**Signed by Sergi:` must be filled in, and there must be at least one; today
there is one. If a blocking check forces an amendment, the amendment carries its
own line and the minimum rises with it, as `PLAN_REUSE.md`'s did.

**The counting is `reuse/plan.py`'s, reused and not copied.** `gate_signature`
gains the plan's minimum as an argument. Its default leaves `PLAN_REUSE.md`'s gate
exactly as it is. No flag skips the gate. `--dry-run` runs `F-g1` to `F-g3` and
writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The inputs.** `RUNS`, the three Stage B records; `N = 2000`; `SEED = 17`.
- **The client.** `MODEL = "deepseek/deepseek-v4-flash"`; `PROMPT = "v1"`;
  `REASONING = {"effort": "none"}`.
- **The sample.** `DRAWS = 2`; `PER_RUN = 600`; `TICKET_ONLY_PER_RUN = 100`;
  `SMOKE_PER_ARM = 5`.
- **The seeds.** `SAMPLE_SEED = 41` and `ORDER_SEED = 43`. They are distinct
  from every seed a closed thread uses: 17 to 20, 25, and values from 1000 up.
- **The limits.** `MIN_SIGNATURES = 1`; `MAX_INVALID_SHARE = 0.05`;
  `MIN_SILENT_ERRORS = 100`.
- **The five lines of §0**: `0.05`, `0.10`, `0`, `0.60` and `1`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
fidelity/__init__.py
fidelity/plan.py      the gate and the constants of §10
fidelity/replay.py    a Stage B record rebuilt case by case; F-g2
fidelity/prompts.py   birth, B and ticket-only prompts, built with rung 2's own functions
fidelity/sample.py    Stage A: the draw, F-g1 to F-g3, F-f's free half
fidelity/ask.py       Stage B: it spends
fidelity/score.py     Stage C: F-a to F-e, and F-f's arm
results_fidelity/FINDINGS_FIDELITY.md
results_fidelity/sample.json  ask_smoke.json  ask_births.json
results_fidelity/ask_base1.json … ask_base3.json  ask_ticket_only.json  score.json
```

**The plumbing goes in the same commit as the modules**, because each of these
lists has drifted before when it was left for later:

- **`CODE_ROOTS`.** `fidelity` joins it in `harness/provenance.py`, and joins
  the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP`.** `fidelity/ask.py` and `fidelity/prompts.py` join it there,
  since they build a proposer's requests.
- **The guarded writers** in `tests/test_writer_lists.py` grow from four to five.
- **The README's table of writers** gains its rows.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network: their client is `tests/doubles.py`'s fake.

---

## 11. Definition of done

- [ ] Records under `results_fidelity/` with `_env` and the reasoning setting,
      produced with `PYTHONHASHSEED=0`.
- [ ] `F-g1` to `F-g4` passed before any record was written. The key check and
      the smoke run came before the first paid session, and each session's record
      was committed before the next began.
- [ ] The plumbing of §10, and tests pinning the constants, the gate, the replay
      and its teeth, the three prompt builders and the arithmetic of §0; the
      whole suite green.
- [ ] Every figure in prose names its surface (the corpus, always) and its
      denominator, and every comparison across dates names the dates.
- [ ] `results_fidelity/FINDINGS_FIDELITY.md` owns every figure, with a dated
      erratum wherever it corrects something already published. That includes
      `FINDINGS_REUSE.md`'s reading of `U-c` if `F-d` contradicts the proxy, and
      this plan's §0 *already seen* if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `F` thread, five adjudicated rows and
      one reported, and the fourth item of *What is open* is closed or narrowed.
- [ ] `IDEAS.md`: *Fidelity*, in *What `PLAN_REUSE.md` opens*, closed or
      narrowed; the trigger item informed by `F-e`; whatever this plan opens,
      added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan in separate commits; the plan and its
      signature alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **B is the smallest counterfactual, not the true one.** Had the deciding rule
   never covered the case, the rules born after it might have been different too,
   written around a gap it filled. Nothing recorded says how, and B does not try.
2. **It compares the rules with the model of the day it runs.** `F-a` measures how
   far that model is from the one that wrote them. It cannot undo the distance.
3. **It does not adjudicate the model without its screen.** The ticket-only arm is
   reported, on a subsample. So compiled rules may poison later answers through
   the screen, a loss that would not show as any rule's error. Whether they do
   is measured and left unjudged.
4. **It does not measure fidelity of scope.** Whether the model, re-asked, would
   write a rule over the same region is recorded and not scored (§5.10).
5. **One model, one corpus, three bases.** The spread over three bases is the only
   handle on the process that made them, and three is few. `U-b` and `U-c` showed
   how far one run can sit from the other two.
6. **It does not build what it measures.** Disagreement with a fresh answer is a
   label-free alarm, and §9 records how precise it would have been. A trigger
   built on it is another plan. So is any repair of compilation if `F-c` holds:
   under rule 5, that repair starts from this recorded result.
7. **It does not touch what the accepted edges buy**, the material problem, or the
   prompt.
