# PLAN_QUEUE_ALONE — the queue asked alone: whether the application loses without a rule to write

**Status: drafted by Claude on 2026-10-24, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**Asked for by Sergi on 2026-10-24**, after `PLAN_APPLY.md` closed and its rows
were read within one provider's answers.

**The item.** `PLAN_APPLY.md` asked `PLAN_MANUAL.md`'s escalations again, with
the manual in the prompt, with and without their screen.

- **The screen is the smaller part.** At level 3, with the 29 rules in the
  prompt, taking the screen away lifts the proposer's choice from 0.5906 to
  0.7031 (`X-b` holds). That recovers about a quarter of what it gets wrong
  with the screen (`X-c` refuted).
- **The rest is the application.** With the rules and no screen the model still
  misroutes three escalated tickets in ten. Compiled once, it writes the same
  rules exactly (`G-a` holds).
- **Read within one provider's answers, POST-RUN, the rows keep their sides.**
  The mix of providers moved none by more than 0.0160
  ([`FINDINGS_APPLY.md`](results_apply/FINDINGS_APPLY.md), *Each row within one
  provider's answers*).

That record's Stage C left the gap as its first item:

> *Why the application loses three tickets in ten. Both arms ask for a rule,
> under a prompt that calls the ticket an impasse. A question asking for the
> queue alone would separate the rule-writing task from the application. That is
> a new prompt, and another plan.*

[`IDEAS.md`](IDEAS.md) carries it first under *What `PLAN_APPLY.md` opens*.
[`STATUS.md`](STATUS.md)'s *What is open* reaches it in its second item: *why
deciding one ticket against the list loses three tickets in ten*.

**Three candidates, each with a reason on record.**

- **The impasse framing.** v1 tells the model it is the system's exception
  component and that the engine could not decide the ticket. The user message
  calls the ticket *en impasse*.
  - `ARBITRATION_REPORT.md` §5 names the operation that framing invites:
    *"find a gap and fill it"*.
  - The notes coded POST-RUN show the list's proposer reading a rule that
    matches its ticket as not covering it
    ([`FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md), *The notes
    beside the rules*).
- **The rule-writing task.** v1 asks for one generalisable rule, its
  conditions, its place among the rules that exist and a note. It does so
  under an empty base: *"BASE DE REGLAS: vacia. Esta es la primera regla."*.
- **The application itself.** Deciding one ticket against a first-match list
  of 29 rules, with reasoning off, is not transcribing the list. Asked plainly,
  the model may lose as much.

**The question, in its cleanest form.** At the escalations of `PLAN_MANUAL.md`'s
loop, with the manual in the prompt and no screen:
- asked only which queue the ticket goes to, is the model right more often than
  when it is asked for a rule?
- how much of what it gets wrong under the rule-writing prompt goes away, and
  how much of that is the impasse framing?
- asked plainly, does it apply the 29 rules nearly as exactly as it transcribes
  them?

**Nothing has to be re-run but the model.** `PLAN_APPLY.md`'s design holds the
population. `apply/population.py` rebuilds it from the twelve loop records: the
decisions, the tickets, and the ticket arm's prompts.

Three arms are bought, all on the day this plan runs and all under one
provider. Every prompt is asked twice.
- **The rule arm, `t`.** This is `PLAN_APPLY.md`'s ticket arm, its prompts byte
  for byte: v1 with the level's manual, and the ticket alone under v1's empty
  base.
- **The impasse arm, `i`.** The same manual and the same framing, asking for the
  queue alone.
- **The plain arm, `q`.** The same manual, asking for the queue alone, with no
  impasse.

Each arm is asked at each level on that level's escalated tickets. It is also
asked at level 0, the names without a manual, on every escalated ticket. That
is how the rules are set against the names on the same tickets.

**What it changes in what is measured, said first.**
- **It installs nothing.** No rule is born, no base grows, and no figure here
  continues a loop's.
- **It reads one axis.** That is the acting axis of `CLAUDE.md` Step 5: the
  queue named for the ticket in front of the model.
- **Two of its three prompts are new.** Hard rule 5 forbids adjusting a prompt
  before a result is recorded. These are not adjustments of v1: they are new
  questions, frozen verbatim in §5.1 and signed with §0. v1 itself is not
  touched.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The surface is the corpus, and the population is the escalations.**
- **Every figure is about tickets that escalated.** They are tickets of
  `generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
  twelve loop runs.
- **No row has an exhaustive-space reading.** What is asked is the model, about
  tickets that arrived and that the loop could not decide.
- **The decisions and the tickets are `PLAN_APPLY.md`'s**, as its §0 counts
  them:

| level | decisions | distinct tickets | ticket prompts asked, per arm |
|---|---|---|---|
| `L₀`, the names | 116 | 70 | 275, every escalated ticket of every level |
| `L₁`, the catalogue | 100 | 81 | 81 |
| `L₂`, and the prose | 242 | 149 | 149 |
| `L₃`, the rules | 320 | 171 | 171 |

- **A decision is an escalation whose screen is not empty.** No screen is shown
  here. The rows still read decisions, as `PLAN_APPLY.md` read its ticket arm,
  so that `acc_t` here is the statistic its 0.7031 was. A ticket weighs as many
  times as the loop escalated it with a screen.
- **The rows read by ticket instead are reported** in `QA-g`.

**The arms and the notation**, per decision at level `k`.

- **`y`** is the true queue: the record row's `truth`.
- **`t₁` and `t₂`** are the rule arm's two answers at the decision's level, in
  pass 1 and pass 2, on the decision's ticket. A ticket that serves several
  decisions of its level lends both to each.
- **`i₁` and `i₂`** are the impasse arm's answers, and **`q₁` and `q₂`** the
  plain arm's, on the same prompt.
- **`t⁰`, `i⁰` and `q⁰`** are the same arms' answers at level 0 on the same
  ticket. At level 0 they are `t`, `i` and `q`.
- **`tᴬ`** is `PLAN_APPLY.md`'s ticket-arm answer on the same prompt, given on
  2026-10-23 or 24, one per pass.
- **`t̄`** is `½(1[t₁=y] + 1[t₂=y])`, and `ī`, `q̄`, `t̄⁰` and `q̄⁰` are defined
  likewise. `acc_t`, `acc_i`, `acc_q`, `acc_t⁰` and `acc_q⁰` are their means
  over a row's decisions.
- **An answer is *valid*** when its `action` is one of the eight queues and
  the provider that served it is the one pinned (§2.3). For the rule arm that
  holds whether or not the rule written with it would validate, as in
  `PLAN_APPLY.md`. **A decision enters a row only with every answer that row
  reads valid.**

**The unit, the error and *thin*.** All of it is settled here and not in the
scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict. It is
`PLAN_APPLY.md`'s, unchanged.

- **Every row is pooled over its level's three runs**, decision by decision.
  The run is not the unit: the question is about the model's answer to a
  prompt, and the runs are unequal.
- **Each run's value is published beside the pooled one**, and adjudicates
  nothing.
- **Every statistic is a ratio of integer counts**, since every mean is of
  multiples of a half. **It is compared with its line exactly, as a fraction.**
  No rounding enters a verdict.
- **The standard error is clustered by ticket**, with `PLAN_APPLY.md`'s formula.
  Decisions on one ticket share its answers.
  - **The formula.** Let a row hold `n` terms on `C` tickets, with `d` a term
    and `d̄` their mean. The variance of the mean is
    `C/(C−1) · Σ over tickets of (Σ over its terms of (d − d̄))² / n²`.
  - **It is a label.** It is a float, and it marks *thin* and never decides.
- **A verdict is labelled *thin*** in either of two cases, and the label does
  not change the verdict:
  - the statistic lies within one standard error of its line;
  - dropping any one run's decisions would put it on the other side.

  `QA-a` reads prompts and not runs, so only the first case applies to it.

**When a row has no value.**
- **A row has none** if more than 5% of its decisions lack the valid answers it
  reads.
- **`QA-a` reads prompts, not decisions.** It has none if fewer than 100 prompts
  hold today's two answers valid and a valid answer of `PLAN_APPLY.md`'s from
  the pinned provider.
- **`QA-c` also has none** if `acc_t` is 1.
- **`QA-d` also has none** if `acc_q − acc_t ≤ 0`. Then there is no gain to
  apportion, and `QA-b` says so.

A row with no value is unadjudicable, and the record says so.

**Which side had the label**, for every arm. This was checked against the
prompts while drafting, and not recalled, as `CLAUDE.md` asks of any plan that
sets a comparison on the proposer:

| arm | what it is handed | reads a label? |
|---|---|---|
| all three at level 0 | the eight queue names, as every prompt in the tree | no |
| all three at level 1 | the catalogue | no |
| all three at level 2 | the catalogue and the prose | in effect, for most tickets (`PLAN_MANUAL.md` §0) |
| all three at level 3 | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."* | **yes**: every ticket's label is derivable from the text by first match |
| `tᴬ` | the rule arm's prompt, on 2026-10-23 and 24 | as the rule arm |

- **The three arms of a row hold the same manual.** No row sets a side that has
  the label against one that has not. `QA-f` sets the rules against the names on
  purpose, as `X-f` did, and it is not a competition.
- **No arm sees an example**, and nothing here is fitted, so nothing reaches a
  test split.
- **No baseline is set against the proposer.** The rule arm is the proposer's
  own prompt. The other two are questions to the same model through the same
  request, and both are the proposer's first task in v1's own words: *"Decidir
  la cola de destino correcta para ESTE ticket."*.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **QA-a** | **The rule arm has not moved since `PLAN_APPLY.md` asked it.** Re-asked under one provider, the ticket arm agrees with that plan's answers from the same provider about as often as it agrees with itself | over the ticket prompts of all four levels that hold today's two answers valid and a valid answer of `PLAN_APPLY.md`'s from the pinned provider: `S − A`. `S` is the share whose two answers today agree. `A` is the mean, over today's two answers and that plan's answers from the pinned provider, of their agreement | **≤ 0.05** | **> 0.05** |
| **QA-b** | **Asked for the queue alone, the model is right more often than when it is asked for a rule**, with the 29 rules in its prompt and no screen | over `L₃`'s decisions: `acc_q − acc_t` | **> 0** | **≤ 0** |
| **QA-c** | **The rule-writing prompt is most of what the model gets wrong with the rules in front of it.** Asking for the queue alone recovers at least half of the answers the rule arm gets wrong | over `L₃`'s decisions: `(acc_q − acc_t) / (1 − acc_t)`. It is compared with its line as `2·acc_q − acc_t − 1` against 0, which is the same comparison | **≥ 1/2** | **< 1/2** |
| **QA-d** | **The impasse framing is most of what the rule-writing prompt costs.** Of the plain arm's gain over the rule arm, the step from the impasse arm to the plain one is at least the step from the rule arm to the impasse one | over `L₃`'s decisions: `(acc_q − acc_i) − (acc_i − acc_t)` | **≥ 0** | **< 0** |
| **QA-e** | **Asked plainly, the model applies the 29 rules nearly as exactly as it transcribes them** | over `L₃`'s decisions: `acc_q` | **≥ 0.90** | **< 0.90** |
| **QA-f** | **What the plain question buys is the list's.** On the same tickets, it gains more over the rule arm with the 29 rules than with the names alone | over `L₃`'s decisions: `(acc_q − acc_t) − (acc_q⁰ − acc_t⁰)` | **> 0** | **≤ 0** |
| **QA-g** | *Reported, not adjudicated.* **What the drafter could not band** | Each level on its decisions: `acc_t`, `acc_i`, `acc_q` and their level-0 counterparts, and every row's statistic at the levels it is not read at, with its parts and per run. The same by ticket instead of by decision. The table by true queue, with `ONCALL_ESCALATION`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER` and `T3_ENGINEERING` in counts. Every answer at `L₃` classified against the 29 rules (§5.6). `S` for each arm, and how often the arms agree with each other. `PLAN_APPLY.md`'s ticket arm, screen arm and loop beside today's arms on the same decisions. Each arm's providers, finish reasons and tokens. The rule arm's `note`, recorded in full and not coded | — | — |

**Signed by Sergi: ____________________ (date: __________)**

**Why each row, and why these lines.**

- **`QA-a` is the instrument row.** Its line is `X-a`'s, `F-a`'s and `V-a`'s.
  - **It reads prompts**, because the ticket arm has no decision of its own.
  - **It reads only that plan's answers from the pinned provider.** Two
    providers give different answers to one prompt more often than one provider
    gives itself (`FINDINGS_APPLY.md`, *Each row within one provider's
    answers*). An anchor read across providers would mostly measure them.
  - It says how far today's rule arm stands for `PLAN_APPLY.md`'s, so that its
    figures can be set beside these. It cannot undo the distance.
- **`QA-b` is read at level 3**, because there the knowledge is complete and the
  text states first match. What the rule-writing prompt costs there is not the
  cost of reading a vague word. Its line is the literal *more often*.
- **`QA-c` answers which part is larger**: the prompt's, or the application's.
  *Most* is read as at least half, so that a tie goes to the claim. Its
  denominator is what the rule arm gets wrong today, not `PLAN_APPLY.md`'s
  0.2969, so the row reads one day's model.
- **`QA-d` apportions the gain between the two parts the arms separate.** Its
  statistic is the difference of the two steps. It holds when the framing's step
  is at least the rule-writing's. With no gain there is nothing to apportion, and
  the row has no value.
- **`QA-e` is the application itself, read against compiling.** Compiled once,
  the same model writes the 29 rules exactly (`G-a`). The line is a tenth below
  exact, `PLAN_MANUAL.md`'s convention of a tenth of its axis.
- **`QA-f` is the control.** If the plain question gained as much with the names
  alone, what it buys would be the question's form and not the list's
  application. It is read on the same tickets, so the mix cancels.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md`**: its opening notes, its scoreboard, *What is open*, and the
  paragraphs on `PLAN_MANUAL.md` and `PLAN_APPLY.md` under *What is
  established*, with their dated notes.
- **`IDEAS.md`**: the sections on the plans from `PLAN_SCREEN.md` to
  `PLAN_APPLY.md`, *What the outside reading of October 2026 proposes* and *What
  `ARBITRATION_REPORT.md` §7 proposes*.
- **The application's thread.** `PLAN_APPLY.md` and `FINDINGS_APPLY.md`, whole,
  with every figure they publish:
  - the six verdicts, with their parts and runs;
  - `X-g`'s tables by level, by screen kind, by true queue and by the rule
    written;
  - the reading within one provider's answers, which this drafter wrote and ran
    on 2026-10-24, POST-RUN. Its cells are in `results_apply/providers.json`,
    every provider's included.

  Also `results_apply/score.json`'s `X-g` by level. The ticket arm's accuracy,
  the names' and the loop's were printed by level while drafting.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  They were not read whole for this plan. The passages it rests on were read
  directly:
  - `ARBITRATION_REPORT.md` §5, its diagnosis;
  - `CHAT_SUMMARY.md`'s header list of errata, and §2.2's erratum of
    2026-08-12, as `PLAN_PAIRWISE.md` §4's rule C asks;
  - `EXTERNAL_REVIEW.md` §5, its sixth point.
- **The code the package will call.** `rung2/proposers2.py`'s v1 and its client,
  `manual/prompts.py`, `apply/prompts.py`, `apply/population.py` and
  `apply/score.py`.
- **The manual's texts.** The rules and the catalogue under `manual/texts/`,
  whole, and the prose's opening.
- **OpenRouter's documentation of provider routing**, and its listing of this
  model's endpoints, read on 2026-10-24 (§2.3).
- **Counts computed while drafting.** None of them reads a label or an answer.
  - **The prompts.** Both new arms were rendered at every level from §5.1's
    texts. Their system prompts run 1,169 and 1,219 characters at level 0 and
    3,476 and 3,526 at level 3, against the rule arm's 2,737 and 5,044.
  - **What the arms differ in.** The plain and impasse arms differ by two
    sentences of the system prompt and the user message's first line, and by
    nothing else. The impasse and rule arms' user messages differ by the
    empty-base line and nothing else. The attributes and actions block is v1's,
    byte for byte.
  - **No prompt in the tree asks for a queue alone.** The tree's prompts ask for
    a rule, a whole base, a ranking of the queues, or the winner between two
    rules.

**Not seen, because nothing has produced it:**

- any answer to a question that asks for a queue alone, in any record of this
  repository;
- any answer served under a pinned provider;
- at level 3, how many of the 29 rules match each escalated ticket, how deep its
  first match lies, and how `PLAN_APPLY.md`'s answers fall in §5.6's classes.

Stage A computes the last after the signature, so that none of it can inform a
band.

**What the drafter expects, written down so the scoreboard can score it.**
**`QA-a`, `QA-b`, `QA-d` and `QA-f` hold; `QA-c` and `QA-e` are refuted.** The
drafter trusts `QA-a` most, then that `QA-e` and `QA-c` are refuted, then
`QA-b` and `QA-f`, and `QA-d` least.

- **`QA-a` holds.** One provider answers both sides. `PLAN_APPLY.md`'s ticket
  arm agreed with itself across its two days 0.9035 of the time where Baidu gave
  both answers. Against it:
  - the request now carries a routing field it did not;
  - this is an argument for continuity, and the standing note in `IDEAS.md`
    says those are the drafter's arguments that lose.
- **`QA-b` holds.** The framing invites the gap-finding reading the notes show,
  and the plain question does not invite it. Against it:
  - **v1's answer opens with the queue** (§5.2). Nothing the model writes about
    the rule comes before it, so the rule-writing apparatus can act only through
    what the model reads.
  - **Information has not helped before.** `CHAT_SUMMARY.md` §2.2's erratum:
    *"With the right information in front of it, it makes the same mistake"*.
- **`QA-c` and `QA-e` are refuted: the application carries the larger part.**
  - **Matching is the work, and nothing here reasons.** Applying the list means
    matching up to eight attributes against up to 29 rules and keeping the
    first that matches, with reasoning off.
  - **Even two rules are not easy.** Shown two hidden rules and a witness
    ticket, the model named the right winner on 0.8824 of 170 pairs
    (`FINDINGS2.md`, Stage C).
  - **These are the hard tickets.** They are the ones the loop could not decide.
  - The drafter's guess is that the plain arm lands near 0.8, which would
    recover about a third of the rule arm's errors.
- **`QA-d` holds.** The framing is what the notes point at. Against it: if the
  gain is small, the two steps are small and the split is noise, so the row may
  well be thin.
- **`QA-f` holds.** With the names alone there is no list to apply, and the plain
  question should change little there. Against it: the rule-writing prompt may
  cost at level 0 too, through the same framing.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 46 of 111 adjudicated rows were refuted.
- **The last plan.** `PLAN_APPLY.md`'s drafter got six of six. Its findings say
  that is a fact about that plan, and not a reason to trust the next drafter
  more.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Every line is the claim's own edge, or a closed thread's: `QA-a`'s is
    `X-a`'s, and `QA-e`'s is `PLAN_MANUAL.md`'s tenth.
  - A verdict a single run carries is labelled *thin* in advance.

**How the rows read together.**

- **`QA-b` and `QA-c` hold.** The prompt is most of the loss. A loop that asked
  for the queue alone, and wrote the rule apart, would apply most of what it was
  given. `QA-d` then says whether it is the framing or the rule.
- **`QA-b` holds and `QA-c` is refuted.** Both cost, and the application carries
  the larger part. `QA-e` says how far the plain question stands from exact.
- **`QA-b` is refuted.** The rule-writing prompt costs nothing on the acting
  axis, and what the loop loses applying the rules is the application's.
  `QA-d` then has no value.
- **`QA-e` holds.** Asked plainly, the model applies the list nearly exactly.
  The loss is then the prompt's, whatever `QA-c` says of its share.
- **`QA-f` is refuted.** The plain question gains as much with the names alone,
  so what it buys is the question's form, not the list.
- **`QA-a` is refuted.** `QA-b` to `QA-f` are still adjudicated as signed. They
  then describe today's model under one provider, and `QA-a`'s gap stands
  beside each.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, hard rule 4:
- **`results_manual/loop_L{0..3}_r{1..3}.json`**, `PLAN_MANUAL.md`'s twelve loop
  runs: the escalations, their tickets, the truth and the loop's answers.
- **`results_apply/sample.json`**: `PLAN_APPLY.md`'s design, every prompt's
  digest and the system prompts.
- **`results_apply/ask_pass1.json` and `ask_pass2.json`**: `tᴬ`, for `QA-a`, with
  the provider of every answer.
- **`results_apply/score.json` and `providers.json`**: §3's references.

**Bought: the model's answers with level `k`'s manual, reasoning off, every call
pinned to one provider.**
- **The rule arm.** Its client is the proposer `manual.run.build_proposer(level)`
  builds, and its `propose` is called as `PLAN_APPLY.md` called it:
  - temperature 0 and 1,200 tokens;
  - `response_format` on the first attempt, and two retries.

  The one change to its request is the provider pin of §2.3. `QA-g2` checks that
  nothing else differs.
- **The impasse and plain arms.** Their client is the package's own, through
  `harness/call_record.py`. It sends the same model, temperature, tokens,
  `response_format`, reasoning setting and pin, and on a failed parse the same
  two retries with v1's retry message.

Three sessions, sequential, in this order:

| session | what is asked | prompts | calls |
|---|---|---|---|
| smoke | at each level, one ticket in each arm, drawn at `ORDER_SEED` | 12 | 12 |
| pass 1 | every prompt of the three arms, 676 each, in one seeded order with the arms interleaved | 2,028 | 2,028 |
| pass 2 | the same prompts, in another seeded order | 2,028 | 2,028 |

**Cost: 4,068 calls, plus any parse retries.** At Baidu's listed price for this
model on 2026-10-24 that is about twenty cents. The estimate takes the rule
arm's tokens as `PLAN_APPLY.md`'s pass 1 recorded them. The new arms' prompts are
taken as shorter by their difference in characters, at three characters a
token, and their answers at fifteen tokens.

**Time.** `PLAN_APPLY.md`'s passes took 79 and 71 minutes for 1,454 asks, about
three seconds an ask. A pass here is 2,028 asks, about 1.7 hours at that pace,
less where the answer is one queue. **Both passes outlive a background command
of the agent's harness**, so they run in Sergi's terminal, as `CLAUDE.md` says.

**What is not bought.**
- **No screen.** The plain question with a screen is §12's.
- **No rule-writing prompt without the impasse framing.** That is the fourth
  cell of the two factors, and §12's.
- **No reasoning, and no other model, provider, manual or loop.**

---

## 2. The choices that have to be made at signature time

Signing §0 adopts the drafter's choice in each unless the signature line says
otherwise. A choice that drops a row is a change to §0, and belongs in the same
signed commit.

### 2.1 The arms — the drafter recommends three

The rule, impasse and plain arms. The impasse arm is what lets `QA-d` apportion
the gain.

**The alternative** is two arms, the rule and plain ones. It drops `QA-d` and
saves 1,352 calls, about half an hour a pass.

### 2.2 The population — the drafter recommends `PLAN_APPLY.md`'s

That is 676 prompts an arm: 275 at level 0, every escalated ticket, and 81, 149
and 171 at levels 1 to 3, each level's own tickets. It keeps `QA-a` on every
prompt that plan asked, and it gives `QA-f` level 0 on level 3's tickets.

- **Less: levels 0, 2 and 3.** Dropping level 1's 81 tickets saves 486 calls and
  drops no row.
- **More: every escalated ticket at every level.** That is 1,100 prompts an arm,
  about 2,500 more calls in all. It would set every level against every other
  on the same tickets, which `PLAN_APPLY.md` §2.2 priced and did not buy.

### 2.3 One provider, pinned — the drafter recommends Baidu

**Every request carries OpenRouter's provider routing, with fallbacks off:**
`{"order": ["baidu"], "allow_fallbacks": false}`. That is the form
OpenRouter's documentation gives for a request served only by one provider, read
on 2026-10-24. Its listing of this model's endpoints names Baidu's as
`baidu/fp8`, served at fp8.

**Why one provider.**
- **Interleaving did not match the providers.** In pass 1 of `PLAN_APPLY.md`,
  Baidu served 0.562 of the screen arm's attempts and 0.719 of the ticket arm's.
- **Two providers part on the answer more often than one provider parts from
  itself** (`FINDINGS_APPLY.md`, *Each row within one provider's answers*).
- **`CLAUDE.md` says what to do about it.** A plan that wants providers matched
  across arms should pin one, or read its rows within each provider, and say so
  in §0. This plan pins.

**Why Baidu.**
- **It served most of what came before.** That is 670 of the loop runs' 792
  attempts, and most of each arm in both of `PLAN_APPLY.md`'s passes.
- **On one prompt it was right as often as the rest.** Against every other
  provider pooled, the difference was −0.0083 on 483 prompts (`providers.json`).

**What the pin costs.** If Baidu does not serve, the request fails rather than
moving. Five failures in a row stop a session without recording them, and the
same command resumes. The smoke run must show every attempt served by Baidu
before pass 1 starts (§8).

**The alternative** is no pin, with the arms interleaved as in `PLAN_APPLY.md`.
Every row would then be read within the provider that served most answers, with
the same decisions read with every answer beside each cut. That is the lesson
`IDEAS.md` drew from that plan's providers. The rows would then rest on fewer
decisions.

### 2.4 Two passes, the arms interleaved — the drafter recommends it

Each pass asks every prompt of the three arms once, in one order drawn at
`ORDER_SEED`. So within a pass the arms share the hours.

### 2.5 This question first

`IDEAS.md` names three other routes under *What `PLAN_APPLY.md` opens*: the
coverage header over an empty list, the conflict screen's gain, and the screen's
effect on the list's breadth. Its section on `PLAN_MANUAL.md` leaves the loop
under v2 with the manual. The drafter put this one first, for three reasons:

- **It asks about the larger part.** Without its screen, the proposer still got
  wrong about three quarters of what it got wrong with it (`X-c` refuted).
- **It needs no screen and no loop.** Every prompt is a ticket alone, rebuilt
  for free.
- **It is a re-ask on one day**, on hundreds of paired decisions.

### 2.6 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

All on the corpus, on `PLAN_APPLY.md`'s decisions. Nothing here is produced by
this plan. `QA-g1` recomputes the `PLAN_APPLY.md` rows and checks them against
their record rather than publishing them again.

| figure | value | owning record |
|---|---|---|
| `PLAN_APPLY.md`'s ticket arm, `acc_t`, on each level's decisions | `L₀` 0.6184 (116), `L₁` 0.46 (100), `L₂` 0.6570 (242), `L₃` 0.7031 (320) | `results_apply/score.json`, `X-g` and the parts of `X-b` and `X-e`, published by `FINDINGS_APPLY.md` |
| its screen arm at `L₃`, `acc_s` | 0.5906 | same, `X-b` |
| the names alone under the rule-writing prompt, on `L₃`'s decisions | 0.4744, on 312 | same, `X-f` |
| the loop's own choice on the same decisions | `L₃` 0.5625, `L₂` 0.6653 | same, `X-g` |
| the rules compiled once | 1.0000 of the space (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| `PLAN_APPLY.md`'s rows on Baidu's answers | `X-b` +0.0996 on 246 decisions; `X-f` +0.2491 on 277 | `results_apply/providers.json`, published by `FINDINGS_APPLY.md` |
| two answers to one ticket-arm prompt agreeing | 0.9035 where Baidu gave both (404 prompts); 0.8477 where Baidu and another provider did (197) | same |
| Baidu against every other provider on one prompt | −0.0083 on 483 prompts | same |
| level 3 in pairwise form | the right winner on 0.8824 of 170 pairs, shown two hidden rules and a witness ticket | `results2/pair_judgement_baselines.json`, published by `FINDINGS2.md`, Stage C |
| the pace | 1,454 asks in 79 and in 71 minutes | `FINDINGS_APPLY.md`, Stage B |
| Baidu's listing for the model | `baidu/fp8`; $0.0406 per million prompt tokens and $0.0812 per million completion tokens | OpenRouter's endpoints listing, read on 2026-10-24. Not a record of this repository |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and touches nothing under `harness/`.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Nothing here is a loop, but the order of a record is
   part of it. The calls are sequential, and the sessions run one after another,
   never side by side.
4. **Seed 17, no regeneration.** Every record under `results_manual/` and
   `results_apply/` is read-only. `harness/record_guard.py` guards this plan's
   paid records, and the flag that overrides it is not typed without Sergi
   asking.
5. **Do not adjust a prompt, a text or the schema.**
   - The rule arm's prompts are `PLAN_APPLY.md`'s, byte for byte.
   - The two new prompts are §5.1's, verbatim, and they are frozen by the
     signature.
   - The texts are `PLAN_MANUAL.md` §5's, pinned by digest.
6. **If the numbers come out badly, report them.** A plain question that changes
   nothing is a result, and so is a rule list the model does not apply.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`apply/`, `manual/`, `fidelity/` and `rung2/` are called by this plan and
   not edited.**
   - The population is `apply.population.build`'s.
   - The rule arm's prompts are `apply.prompts.ticket_ask`'s, and its client is
     `manual.run.build_proposer(level)`.
   - The manual's block is `manual.prompts.block`'s.
   - The answer is parsed by `rung2.proposers2.parse_payload`.
B. **The loop records are inputs, never outputs, and no label reaches a prompt
   or a row Stage B writes.**
   - **Labels join at scoring.** `y` is copied from the records by Stage C, and
     `tᴬ` from `PLAN_APPLY.md`'s records. The rows Stage B writes carry neither.
   - **No module on the proposer's path imports the oracle.** That path is
     `queue_alone/prompts.py` and `queue_alone/ask.py`. They import by name
     neither the oracle, nor `HIDDEN_DSL`, nor `harness.ceiling_check`, nor
     `rung2.hidden_priority`. Both join `ONLINE_LOOP` and the authority
     channel's watch.
   - **The 29 rules are read from level 3's frozen text**, by `QA-g1`, Stage A
     and Stage C, never on the proposer's path. The list of modules allowed to
     see the oracle does not grow.
C. **Every record carries `_env`**, with:
   - the model, the temperature, the reasoning setting and the provider pin;
   - each arm's and level's system-prompt digest;
   - every attempt's `call_attempts`.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded in full and never
   executed.** No rule is installed and no edge is tried, and no stage codes a
   note.
F. **The order of Stage B is §8's**, and the module refuses a session out of
   it.
G. **The provider is pinned on every call.** An answer served by another
   provider is not an answer of this plan. It is recorded and counted as
   invalid, never read.

---

## 5. Known traps

**5.1 — The two new prompts, verbatim.** They are built from v1's own blocks,
word for word where they say the same thing. The texts are in Spanish, as v1's
are, because they are prompt content.

The plain arm's system prompt at level `k`:

```
Eres el componente de enrutamiento de un sistema de triaje de tickets.

Tu tarea: decidir la cola de destino correcta para ESTE ticket.

ATRIBUTOS DISPONIBLES Y SUS DOMINIOS:
<the domains, as v1 writes them>

severity: 1 = critica, 4 = baja.

ACCIONES POSIBLES:
<the eight queues, as v1 writes them>

<at levels 1 to 3, the manual's block, as manual.prompts.block(k) writes it>

Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:

{
  "action": "<accion para este ticket>"
}
```

At level 0 the manual's block and the blank line before it are absent. The
impasse arm's system prompt is the same, with its first two paragraphs
replaced by:

```
Eres el componente de excepcion de un sistema de triaje de tickets.

El motor simbolico no ha podido decidir este ticket. Tu tarea: decidir la cola de destino correcta para ESTE ticket.
```

The user messages:
- **plain arm:** `TICKET:` on its own line, then the ticket as v1 renders it;
- **impasse arm:** `TICKET EN IMPASSE:` on its own line, then the ticket as v1
  renders it;
- **rule arm:** `PLAN_APPLY.md`'s, which is v1's empty-base line, a blank line,
  and the impasse arm's message.

**What each pair of arms differs in**, and so what each step measures.
- **Plain against impasse.** Two sentences of the system prompt (the role, and
  *"El motor simbolico no ha podido decidir este ticket."*) and the user
  message's first line. Nothing else. So `acc_q − acc_i` is the impasse
  framing.
- **Impasse against rule.** Everything v1 says about writing a rule:
  - its items 2 and 3, and the numbering of item 1;
  - the section on how the engine arbitrates, and the operators;
  - the rule's fields in the answer, the sentences on `beats` and `loses_to`,
    and *"La regla DEBE casar el ticket presentado."*;
  - the empty-base line in the user message.

  So `acc_i − acc_t` is the rule-writing apparatus, read as one bundle. §12 says
  what it cannot split.

**5.2 — In every arm, the queue is the first thing the model writes.** v1's
answer opens with `action`, and the new arms' answer is nothing else. So no arm
reasons in its output before it names the queue. Whatever the rule-writing
apparatus does to the queue, it does through what the model reads.

**5.3 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every arm holds
it, and the text states first match. So the rows at level 3 measure what the
model does with a label it holds. None of them reads level 3 as something the
model knew.

**5.4 — The population is each loop's escalations.**
- **They were selected by each run's base**: the tickets no rule covered there,
  or where rules conflicted. They are not the arrivals, and they are harder.
- **Every row compares arms on the same decisions**, so the mix cancels inside a
  row. `acc_q` is not the model's accuracy on the arrivals.

**5.5 — One ticket, several decisions.** A ticket's answers serve every
decision it has at its level, so decisions are not independent draws. That is
why the error is clustered by ticket.

**5.6 — Classify every answer before betting on a mechanism.** That is the
`IDEAS.md` lesson from `blind/cycles.py`, and `PLAN_APPLY.md` §5.6 applied it to
the screen. At level 3 `QA-g` classifies every answer of every arm against the
29 rules, read from the level's frozen text by first match:
- **first**: the queue of the first rule the ticket matches, which is `y`;
- **order**: another queue, given by a rule the ticket also matches, lower in
  the list;
- **matching**: a queue no rule the ticket matches gives.

Beside them, the queue of the matching rule with the most conditions, which is
how rung 1's engine arbitrated. Stage A classifies `PLAN_APPLY.md`'s answers
the same way after the signature. It is reported, and no row bets on it.

**5.7 — One provider is not the model.** Baidu serves this model at fp8 (§3).
Every figure here is that provider's serving of it. `PLAN_APPLY.md`'s answers
were right as often from Baidu as from the rest on one prompt, which is why the
pin is expected to cost the rows little. It does not make Baidu the model.

**5.8 — Two dates, for `QA-a` only.** `tᴬ` is of 2026-10-23 and 24. Every row
but `QA-a` reads today's arms only. `QA-a` measures the distance, and cannot
undo it.

**5.9 — Invalid answers.** As in `PLAN_APPLY.md`, with §0's thresholds, and with
rule G's: an answer from another provider is invalid. Every count of a decision
left out is published.

**5.10 — Long sessions.**
- **A session that dies keeps what it paid for.** Answers are appended to a
  git-ignored partial file, and the same command resumes there.
- **An outage is not answers.** Five failed calls in a row stop a session
  without recording them.
- **A pass belongs in Sergi's terminal**, because it outlives a background
  command of the agent's harness.

**5.11 — The queues are listed in one order in every prompt.** The slot decides
some pairwise answers (`PLAN_PRIMACY.md`). Here every arm lists the eight queues
in v1's order, so the order cancels inside a row and is not varied.

**5.12 — The rule arm's note is recorded whole and not coded.** The new arms
write no note.

**5.13 — Information in front of the model has not changed what it does
before.**
- `CHAT_SUMMARY.md` §2.2's erratum: *"With the right information in front of
  it, it makes the same mistake"*.
- With the rules in its prompt, the proposer still partitions (`G-c`).
- Both are priors against `QA-b`, and a reader should weigh the drafter's
  expectation with them.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**QA-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.
- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_APPLY.md`'s checks.** Its `X-g1` to `X-g3` pass, called through
  `apply.gates.run_checks` and not copied.
- **Its design.** Rebuilt, it is `results_apply/sample.json`'s: the decisions,
  the tickets, and every ticket prompt's digest.
- **Its rows.** `apply.score` gives back `score.json`'s six verdicts from the
  passes.
- **The 29 rules.** Read from level 3's frozen text by first match, they give
  every escalated ticket its truth.
- **No float decides a check.** Values are compared as fractions and labels as
  booleans, so a record written under 3.12 reads the same under 3.10.

**QA-g2 — The prompts are §5.1's, and the request is the loop's.**
- **The rule arm.** Every prompt is `PLAN_APPLY.md`'s ticket arm, digest for
  digest.
- **The new arms.**
  - Each system prompt is §5.1's text at its level.
  - The plain and impasse prompts differ by exactly §5.1's two sentences, and
    their user messages by the first line.
  - The impasse and rule arms' user messages differ by the empty-base line.
  - The attributes and actions block is v1's, byte for byte, and the manual's
    block is `manual.prompts.block`'s.
- **The request.** It is checked through `tests/doubles.py`'s SDK double in the
  package's tests, which `QA-g1`'s suite runs. For each arm at each level, a
  call sends:
  - the model, temperature 0 and 1,200 tokens;
  - `response_format` on the first attempt, and reasoning off;
  - the provider pin of §2.3;
  - the two messages.

  The rule arm's request is `manual.run.build_proposer(level).propose`'s with
  the pin added, and nothing else changed.
- **No builder takes a record's row.**
- **Teeth.** One changed character moves a prompt's digest, and no digest stands
  for two texts.

**QA-g3 — The populations and the schedule are §0's and §1's.**
- **The prompts.** There are 676 an arm: 275 at level 0, and 81, 149 and 171 at
  levels 1 to 3.
- **The passes.** Each holds every prompt of the three arms once, 2,028, in its
  order rebuilt from `ORDER_SEED`. The two orders differ.
- **The smoke.** Its twelve prompts are drawn from those by `ORDER_SEED`.

**QA-g4 — The signature**, §10.

---

## 7. Stage A — the design and the free readout (free, gated)

**Deliverable.** `queue_alone/sample.py` → `results_queue_alone/sample.json`.

- **`QA-g1` to `QA-g3`.**
- **The design.** Every prompt, with its arm, level, ticket, digest and the
  decisions it serves, and the three sessions' orders at `ORDER_SEED`.
- **`QA-g`'s reference columns, computed after the signature.**
  - At level 3, for every decision: how many of the 29 rules its ticket
    matches, where its first match lies, and whether a lower match gives
    another queue.
  - Two copiers scored on the truth. One answers the queue of the matching rule
    with the most conditions; the other the commonest queue among the matching
    rules.
  - `PLAN_APPLY.md`'s ticket and screen arms, classified as in §5.6.

**It produces nothing adjudicable.** It runs after §0 is signed, so that none of
its figures can inform a band.

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `queue_alone/ask.py` → `results_queue_alone/ask_smoke.json`,
`ask_pass1.json` and `ask_pass2.json`. **Three sessions, in that order, one
after another. Each record is committed before the next session starts.**

**Every session, before any call**, follows `PLAN_APPLY.md` §8's order:

1. **`--dry-run`** runs `QA-g1` to `QA-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`QA-g4`).** While `PLAN_QUEUE_ALONE.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.** A pass needs the smoke record, with a valid answer
   from each arm and every attempt served by the pinned provider. Pass 2 also
   needs pass 1's record.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`QA-g1` to `QA-g3`, blocking.** Stage A's record must hold the same design
   and digests.
6. **The destination.** A paid record is never overwritten.
7. **The clients, and the calls.** They are sequential, with reasoning off and
   the pin on every one.

**What each record carries, per call:**
- **Which call**: the session, the pass and the position.
- **What was asked**: the prompt's id, arm, level and digest. Stage A's record
  says which decisions each prompt serves.
- **The answer**: its `action` and its whole payload, or the failure, and every
  attempt's `call_attempts`, provider and finish reasons included.
- **When**: the seconds and the time.
- **No label.** Stage C joins `y` and `tᴬ` (rule B).

## 9. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `queue_alone/score.py` → `results_queue_alone/score.json`, and
`results_queue_alone/FINDINGS_QUEUE_ALONE.md`, which owns every figure.

- **`QA-a` to `QA-f`**, each against its line, exactly, with its clustered
  standard error, *thin* and *unadjudicable* as §0 defines them.
- **Each row's parts and per-run values**, never summed into the verdict.
- **`QA-g` in full**, §5.6's classes included.
- **The run itself**: failed calls, invalid actions, answers from another
  provider, retries, and the pace per session.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `queue_alone/sample.py` and `queue_alone/score.py` spend nothing.
`queue_alone/ask.py` refuses before it constructs a client. **The free stages
get the gate because what it protects is not money.** Stage A counts where each
level-3 ticket's first match lies and how `PLAN_APPLY.md`'s answers fall in
§5.6's classes. Those are exactly what would inform `QA-c`'s and `QA-e`'s bands.

**The gate reads `PLAN_QUEUE_ALONE.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.**
  - `MODEL`, `PROMPT`, `REASONING` and `TEMPERATURE` are imported from
    `manual.plan`, and the rule arm's proposer is `manual.run.build_proposer`.
  - `MAX_TOKENS = 1200` and two retries, the proposer's own.
  - `PROVIDER = {"order": ["baidu"], "allow_fallbacks": False}`, and
    `PROVIDER_NAME = "Baidu"`, the name the response's `provider` field gives.
- **The inputs.** `apply.population.build` and `apply.plan`'s paths, imported and
  not retyped.
- **The arms.** `ARMS = ("t", "i", "q")`, the rule, impasse and plain arms.
- **The populations.**
  - `TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}`.
  - `DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}`.
- **The sessions.**
  - `SESSIONS = ("smoke", "pass1", "pass2")`.
  - `PASSES = 2`.
  - `SMOKE_PER_ARM_AND_LEVEL = 1`.
- **The seed.** `ORDER_SEED = 71`.
  - **It is new.** It is distinct from every seed a closed thread uses: 17 to
    20, 25, 41, 43, 47, 53, 59, 61 and 67, and values from 1000 up.
  - **It feeds three streams**, one string seed per session.
  - **It is hash-free.** CPython seeds a string through SHA-512, so no order
    depends on `PYTHONHASHSEED`.
- **The limits.**
  - `MIN_SIGNATURES = 1` and `MAX_CONSECUTIVE_FAILURES = 5`.
  - `MAX_INVALID_SHARE = Fraction(1, 20)` and `MIN_ANCHOR_PROMPTS = 100`.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `QA_A_MAX_GAP = Fraction(1, 20)`.
  - `QA_B_LINE = 0`, held above.
  - `QA_C_LINE = Fraction(1, 2)`.
  - `QA_D_LINE = 0`, held at or above.
  - `QA_E_LINE = Fraction(9, 10)`.
  - `QA_F_LINE = 0`, held above.

**The names.**
- **The package is `queue_alone/`, not `queue/`.** A package named `queue`
  would shadow the standard library's `queue`, which the standard library itself
  imports.
- **The rows are `QA-a` to `QA-g`, with two letters.** Every single capital
  already names a thread: twenty-six threads, from `A` to `Z`.
  `tests/test_prose_tables.py` reads row names with one capital. The package
  extends its patterns to one or two, with a test that a two-letter name is
  read whole and never as its last letter's row. That lands before any document
  cites these rows.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
queue_alone/__init__.py
queue_alone/plan.py        the gate and the constants of §10
queue_alone/prompts.py     the three arms' prompts                    [proposer's path]
queue_alone/population.py  the prompts and the sessions, on PLAN_APPLY.md's population
queue_alone/rules.py       the 29 rules from level 3's text, for QA-g1 and §5.6
queue_alone/gates.py       QA-g1 to QA-g4
queue_alone/sample.py      Stage A
queue_alone/ask.py         Stage B: it spends                         [proposer's path]
queue_alone/score.py       Stage C, and §5.6's classes
results_queue_alone/FINDINGS_QUEUE_ALONE.md
results_queue_alone/sample.json  ask_smoke.json  ask_pass1.json  ask_pass2.json  score.json
tests/test_queue_alone.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `queue_alone` joins it in `harness/provenance.py`, and joins
  the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The two modules marked above
  join both, with rule B's comment. They send the manual's texts, as
  `apply/prompts.py` and `apply/ask.py` do.
- **The partial files**, `results_queue_alone/*.partial.jsonl`, join
  `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call sites.** The new arms' client is a new call site, classified in
  `tests/test_call_record.py`. The rule arm's pin is added around
  `rung2/proposers2.py`'s client without editing it, and its test says how.
- **The README's table of writers** gains its rows.
- **`tests/test_prose_tables.py`** reads two-letter row names, as above.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_queue_alone/` with `_env`, the model, the
      temperature, the reasoning setting, the provider pin, the system prompts'
      digests and `call_attempts`, produced with `PYTHONHASHSEED=0`.
- [ ] `QA-g1` to `QA-g4` passed before any record was written. The key check
      and the smoke run came before the first pass, and each session's record
      was committed before the next began.
- [ ] Every answer of the smoke run was served by the pinned provider before
      pass 1 began.
- [ ] The plumbing of §10, and tests pinning:
      - the constants and the gate;
      - the two new prompts against §5.1, with their teeth;
      - the rule arm's prompts against `PLAN_APPLY.md`'s digests;
      - the requests, the pin included;
      - §5.6's classes on tickets built by hand;
      - the exactness of §0's comparisons and the clustered error;
      - two-letter row names in `tests/test_prose_tables.py`.
      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface (the corpus, always), its level,
      its arm, its denominator, and the date of each side it compares.
- [ ] `results_queue_alone/FINDINGS_QUEUE_ALONE.md` owns every figure, with a
      dated erratum wherever it corrects something already published. That
      includes this plan's §0 *already seen*, if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `QA` thread. *What is open* narrows
      its second item by what this plan settles.
- [ ] `IDEAS.md`: *Why deciding one ticket against the list loses three in ten*
      is closed or narrowed, with what this plan opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `QA`, and its `TABLES`
      gains `FINDINGS_QUEUE_ALONE.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits; the plan and its
      signature are alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **The rule-writing prompt without the impasse framing.** The two factors
   have four cells, and this plan buys three. So `acc_i − acc_t` is the
   rule-writing apparatus under the framing, read as one bundle. Whether the
   rule's fields, the arbitration section or the empty base does the work is
   not split.
2. **The plain question with a screen.** Whether the screen pulls a plain
   answer as it pulls a rule-writer's (`X-d`) is a new prompt, and another plan.
3. **Reasoning.** Whether a model that reasons applies the list exactly asked
   plainly is a different setting. `PLAN_REUSE.md`'s amendment turned it off for
   the proposer.
4. **The loop.** A loop that asked for the queue alone and wrote the rule apart
   is a new system. So is one that starts from the compiled manual, which
   `IDEAS.md` carries.
5. **Why.** Whether the plain arm's errors are of order or of matching is
   reported (§5.6), and no row bets on it.
6. **The arrivals.** Every figure is about escalated tickets, which are the
   hard ones.
7. **One model, one provider, one manual, two passes, one day.**
