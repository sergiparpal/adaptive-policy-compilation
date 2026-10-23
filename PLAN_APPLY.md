# PLAN_APPLY — the rules applied ticket by ticket: what the screen costs, and what is the application's own

**Status: drafted by Claude on 2026-10-23, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**Asked for by Sergi on 2026-10-23.** [`IDEAS.md`](IDEAS.md) names two routes
with calls under *What `PLAN_MANUAL.md` opens*: the loop under v2 with the
manual in its prompt, and asking the escalated tickets again with the manual and
no screen. He asked for a plan on one of them. The drafter chose the second, and
§2.5 says why. The choice is his to overrule.

**The item.** `PLAN_MANUAL.md` handed the model the hidden policy as text.

- **Compiled once, the model transcribes the 29 rules exactly** (`G-a`).
- **In the loop, the same rules in its system prompt did not carry over to the
  escalations.** The proposer named the right queue at 183 of 323 escalations,
  0.5666. With the prose it named it at 164 of 245, 0.6694
  ([`FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md), *The proposer's
  choice of queue*).

That record's Stage C left the gap open as its item 2:

> *Why the proposer applies the rules at 0.5666. Asking the escalated tickets
> again with the manual and no screen would separate the screen's pull from the
> application itself. Calls.*

`IDEAS.md` carries it as *Why the proposer applies the rules it was given four
times in ten wrongly*. [`STATUS.md`](STATUS.md)'s *What is open* reaches it
twice: its second item names *why the loop loses what it knows*, and its fourth
*why the model defers*.

**Two candidates, each with a measured reason behind it.**

- **The screen.** Every escalation showed the proposer rules of the base beside
  the ticket.
  - `PLAN_SCREEN.md` measured that such a screen pulls the model's answer to
    the screen's commonest action. That costs it wherever that action is wrong
    (`V-b` to `V-d`).
  - It measured that without a manual, on decided cases re-asked, and never on
    an escalation's own screen.
- **The application itself.** Deciding one ticket against a list of 29 rules is
  not copying the list. The notes beside the rules, coded POST-RUN on
  2026-10-23, show two things in the held-out runs at level 3:
  - **Finding the right rule is not enough.** When a note cites the rule that
    governs its ticket, the proposer names that rule's queue 50 times in 67.
  - **It misreads coverage.** It reads a listed rule that matches the ticket as
    not covering it, because the rule does not name the ticket's values:
    *"La regla H28 (business/enterprise -> T1_GENERAL) es la más cercana, pero
    no cubre severity 4 específicamente"*. No screen supplies that reading.

**The question, in its cleanest form.** At the escalations of `PLAN_MANUAL.md`'s
loop, with the manual in the prompt:
- how much of what the proposer gets wrong goes away when the screen does?
- without a screen, do the rules reach the ticket's answer at all?

**Nothing has to be re-run but the model.**
- **The loop records hold the rest.** The twelve loop records hold every
  escalation, its ticket, its truth and the answer the loop recorded.
- **The screens are rebuilt from the records alone**, and the rebuild was
  checked while drafting (§0).

Two arms are bought, both on the day this plan runs, and every prompt is asked
twice:
- **the screen arm**: each escalation's own prompt, rebuilt verbatim, screen and
  all;
- **the ticket arm**: the same system prompt with the ticket alone, under v1's
  empty-base rendering. That is what case 0 saw in every run.

The ticket arm is also asked at level 0, the names without a manual, on every
escalated ticket of every level. That is how the rules are set against the names
on the same tickets.

**What it changes in what is measured, said first.**
- **It installs nothing.** This plan asks the model: no rule is born, no base
  grows, and no figure here continues a loop's.
- **It reads one axis.** That is the acting axis of `CLAUDE.md` Step 5: the
  queue named for the ticket in front of the model.
- **The rule beside each answer is recorded and not installed.** Its breadth is
  reported and never adjudicated.

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
- **Each level's escalations are its own loop's** (§5.3).

**The decisions.** A *decision* is an escalation of
`results_manual/loop_L{k}_r{r}.json` whose screen is not empty: its level `k`,
its run `r` and its case. There are 778:

| level | escalations | with an empty screen | decisions | on a coverage screen | on a conflict screen | distinct tickets |
|---|---|---|---|---|---|---|
| `L₀`, the names | 119 | 3 | 116 | 105 | 11 | 70 |
| `L₁`, the catalogue | 103 | 3 | 100 | 63 | 37 | 81 |
| `L₂`, and the prose | 245 | 3 | 242 | 167 | 75 | 149 |
| `L₃`, the rules | 323 | 3 | 320 | 250 | 70 | 171 |

- **The empty screens are case 0 of every run.** There the escalation's prompt
  is the ticket arm's prompt, so the decision enters no row.
- **A ticket is its attributes, `Case.key()`**, as `PLAN_SCREEN.md` keyed its
  own. The last column counts each level's distinct escalated tickets, case 0's
  included. Over the twelve runs there are 275.

**The arms and the notation**, per decision.

- **`y`** is the true queue: the record row's `truth`.
- **`ℓ`** is the loop's answer: the row's `predicted`, given on 2026-10-21.
- **`s₁` and `s₂`** are the screen arm's two answers. They are bought on the
  decision's own escalation prompt, rebuilt verbatim, in pass 1 and pass 2.
- **`t₁` and `t₂`** are the ticket arm's two answers at the decision's level.
  They are bought on the decision's ticket alone, under its level's system
  prompt, in pass 1 and pass 2. A ticket that serves several decisions of its
  level lends both to each.
- **`u₁` and `u₂`** are the ticket arm's two answers at level 0, on the same
  ticket. At level 0 they are `t₁` and `t₂`.
- **`p`** is the screen's plurality action: `fidelity.prompts.plurality` on the
  rebuilt prompt. It is the commonest action shown, a tie going to the action
  shown first.
- **`s̄`** is `½(1[s₁=y] + 1[s₂=y])`, and `t̄` and `ū` are defined likewise.
  `acc_s`, `acc_t` and `acc_u` are their means over a row's decisions.
- **An answer is *valid*** when its `action` is one of the eight queues, whether
  or not the rule written with it would validate. That is `PLAN_FIDELITY.md`
  §5.5, and it is how the loop scored `proposal_action_correct`. **A decision
  enters a row only with every answer that row reads valid.**

**The unit, the error and *thin*.** All of it is settled here and not in the
scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **Every row is pooled over its level's three runs**, decision by decision, as
  `G-f` pooled the escalations. The run is not the unit, for two reasons:
  - the question is about the model's answer to a prompt;
  - the runs are unequal, from 12 escalations to 136.
- **Each run's value is published beside the pooled one**, and adjudicates
  nothing.
- **Every statistic is a ratio of integer counts**, since `s̄`, `t̄` and `ū` are
  multiples of a half. **It is compared with its line exactly, as a fraction.**
  No rounding enters a verdict.
- **The standard error is clustered by ticket.** Decisions on one ticket share
  its ticket arm's answers, and at every level some tickets escalate in more
  than one run: 31, 18, 80 and 97 of them.
  - **The formula.** Let a row hold `n` decisions on `C` tickets, with `d` a
    decision's term and `d̄` their mean. The variance of the mean is
    `C/(C−1) · Σ over tickets of (Σ over its decisions of (d − d̄))² / n²`.
  - **It is a label.** It is a float, and it marks *thin* and never decides.
- **A verdict is labelled *thin*** in either of two cases, and the label does
  not change the verdict:
  - the statistic lies within one standard error of its line;
  - dropping any one run's decisions would put it on the other side.

**When a row has no value.**
- **A row has none** if more than 5% of its decisions lack the valid answers it
  reads.
- **`X-d` also has none** if fewer than 100 of its decisions have `t₁ ≠ p`.
- **`X-c` also has none** if `acc_s` is 1.

A row with no value is unadjudicable, and the record says so.

**Which side had the label**, for every arm. This was checked against the
prompts the package builds, and not recalled, as `CLAUDE.md` asks of any plan
that sets a comparison on the proposer:

| arm | what it is handed | reads a label? |
|---|---|---|
| both arms at level 0, and so `u` | the eight queue names, as every prompt in the tree | no |
| both arms at level 1 | the catalogue | no |
| both arms at level 2 | the catalogue and the prose | in effect, for most tickets (`PLAN_MANUAL.md` §0) |
| both arms at level 3 | the 29 rules, in order | **yes**: every ticket's label is derivable from the text by first match (`PLAN_MANUAL.md` §6.2) |
| `ℓ`, the loop's answer | what the screen arm is handed, on 2026-10-21 | as the screen arm |

- **Both arms of a row hold the same text.** No row sets a side that has the
  label against one that has not. The exception is `X-f`, which measures exactly
  what the rules add to the names on the same tickets. That is its point, and it
  is not a competition.
- **No arm sees an example**, and nothing here is fitted, so nothing reaches a
  test split.
- **No baseline is set against the proposer.** Both arms are the proposer, with
  the loop's own client and request, and the screen arm's prompt is the loop's
  own.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **X-a** | **The instrument has not moved since the loop asked.** Re-asked its own escalation prompt, the model agrees with the answer the loop recorded on 2026-10-21 about as often as it agrees with itself | over the decisions of all four levels, pooled: `S − A`. `S` is the share whose two answers `s₁` and `s₂` agree. `A` is the mean of `½(1[s₁=ℓ] + 1[s₂=ℓ])` | **≤ 0.05** | **> 0.05** |
| **X-b** | **With the rules in its prompt, the proposer is right more often without its screen** | over `L₃`'s decisions: `acc_t − acc_s` | **> 0** | **≤ 0** |
| **X-c** | **The screen is most of what the proposer gets wrong with the rules in front of it.** Taking the screen away recovers at least half of the answers it gets wrong with it | over `L₃`'s decisions: `(acc_t − acc_s) / (1 − acc_s)`. It is compared with its line as `2·acc_t − acc_s − 1` against 0, which is the same comparison | **≥ 1/2** | **< 1/2** |
| **X-d** | **The screen still pulls the model to its plurality with the rules in the prompt.** Where the model's own answer is not the screen's plurality action, the screen makes it that action markedly more often than a second answer without the screen does | over `L₃`'s decisions with `t₁ ≠ p`: the mean of `½(1[s₁=p] + 1[s₂=p]) − 1[t₂=p]`. It reads no label | **≥ 0.10** | **< 0.10** |
| **X-e** | **With the prose in its prompt, the proposer is right more often without its screen** | over `L₂`'s decisions: `acc_t − acc_s` | **> 0** | **≤ 0** |
| **X-f** | **Without a screen, the rules reach the ticket's answer.** On the same tickets, the model with the 29 rules is right at least a tenth more often than with the names alone | over `L₃`'s decisions: `acc_t − acc_u` | **≥ 0.10** | **< 0.10** |
| **X-g** | *Reported, not adjudicated.* **What the drafter could not band** | Each level on its decisions: `acc_s`, `acc_t`, `acc_u`, the loop's own accuracy on the same decisions, and every row's statistic with its parts and per run. Every row's statistic at the levels it is not read at. Coverage and conflict screens apart. The table by true queue, with `ONCALL_ESCALATION`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER` and `T3_ENGINEERING` in counts. Every decision where the two arms' answers differ, classified by what the screen changed the answer to (§5.6). `X-a` by level. The rule written beside each answer: whether it validates, and its breadth off the keyword, by arm and level. `u` against `PLAN_SCREEN.md`'s ticket-only answers where a ticket is shared. Each arm's providers, finish reasons and tokens. Every `note`, recorded in full and not coded | — | — |

**Signed by Sergi: ____________________ (date: __________)**

**Why each row, and why these lines.**

- **`X-a` is the instrument row.** Its line is `F-a`'s and `V-a`'s. It is
  pooled because it is about one instrument, not four levels. It says how far
  today's screen arm stands for the loop's answers. It cannot undo the distance.
- **`X-b` is read at level 3** because there the knowledge is complete and
  unambiguous: what the screen costs there is not the cost of reading a vague
  word. Its line is the literal *more often*, `V-b`'s.
- **`X-c` is the row that answers which candidate is larger.** *Most* is read
  as at least half, so that a tie goes to the claim. Its denominator is what the
  screen arm gets wrong today, not the loop's 0.5666 of 2026-10-21, so the row
  reads one day's model.
- **`X-d` asks whether authority in the prompt removes the deference `V-c`
  measured without it.** Its line is `V-c`'s *markedly*, and it reads no label.
  Its baseline is `V-c`'s too (`PLAN_SCREEN.md` §5.5). Were the screen to do
  nothing, an answer with it and a second answer without it would be
  exchangeable given `t₁`. The two passes are drawn in separate orders, so which
  answer conditions is fixed by the pass, not chosen afterwards.
- **`X-e` is the deployment's text.** A company has prose, not its rules as
  code. Its line is the literal one.
- **`X-f` says whether the rules reach a ticket's answer at all** when nothing
  else is shown. Its line is a tenth of its axis, `PLAN_MANUAL.md`'s convention.
  It is read on the same tickets, so the mix that `PLAN_MANUAL.md` §6.6 could
  not separate from the choice cancels.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md` and `IDEAS.md`**, whole.
- **The manual's thread.** `PLAN_MANUAL.md` and `FINDINGS_MANUAL.md`, whole,
  with every figure and quotation they publish:
  - the proposer's choice of queue by level and by queue;
  - the six verdicts;
  - the three readings and the coded notes.

  Also `results_manual/score.json`'s `G-g`, where the choice of queue by level
  and by true queue sits. Its first two levels were printed while drafting,
  queue by queue, with some counts `FINDINGS_MANUAL.md` does not publish.
- **The screen's thread.** `PLAN_SCREEN.md`, and the verdict table of
  `FINDINGS_SCREEN.md`. Also `PLAN_FIDELITY.md`'s §5.5 and its pace.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  - They were read through a digest commissioned for this plan, with
    `PLAN_PAIRWISE.md` §4's rule C.
  - The passages cited here were then read directly:
    - `ARBITRATION_REPORT.md` §5's diagnosis;
    - `CHAT_SUMMARY.md` §2.2's erratum of 2026-08-12;
    - `EXTERNAL_REVIEW.md` §5.6, its sixth point.
- **The code the package will call.** `rung2/proposers2.py`,
  `fidelity/prompts.py`, `fidelity/replay.py`, `manual/prompts.py`,
  `manual/run.py`, and `manual/notes.py`'s docstring.
- **Counts computed while drafting.** None of them reads a label.
  - **The decisions**: the table above, by level, run and screen kind.
  - **The tickets**: the distinct tickets by level and over the twelve runs, how
    many escalate in more than one run, and the 25 that only levels 0 and 1
    escalated.
  - **Shared tickets.** 183 of the 275 tickets are among the 1,184 that
    `PLAN_SCREEN.md` asked with the ticket alone under v1. So their level-0
    prompt here is that plan's prompt.
  - **Shared texts.** 13 of the 1,454 asks have the same text as another ask,
    all of them early escalations in two or three runs of one level.
  - **The replay.** `fidelity.replay.check` rebuilds all twelve records with no
    departure. That covers every outcome, winner and number of matched rules,
    every escalation's shown ids and kind, every edge verdict, and every rule's
    final counts.
    - **The system prompts.** Each record's system prompt is
      `manual.prompts.loop_system_prompt` of its level, byte for byte.
    - **What `check` flags.** It flags levels 1 to 3 as *not v1*, because it was
      written for `PLAN_REUSE.md`'s records. This plan's gate compares each
      record with its own level's prompt instead (§6).

**Not seen, because nothing has produced it:**

- any answer to a prompt of either arm, at any level;
- any answer without a screen with a manual in the prompt;
- the loop's accuracy on these decisions split by screen kind or by run;
- `p` on any decision, and so how often it is the true queue or the loop's
  answer.

Stage A computes those after the signature, so that none of them can inform a
band.

**What the drafter expects, written down so the scoreboard can score it.**
**`X-a`, `X-b`, `X-d`, `X-e` and `X-f` hold; `X-c` is refuted.** The drafter
trusts `X-f` most, then `X-b`, `X-d`, `X-a` and `X-e`, and `X-c` least.

- **`X-a` holds.** The gap is a few days, and `V-a`'s screen clause held over
  twelve, at +0.0284. Against it:
  - its ticket-only clause failed over the same twelve days;
  - eight providers answered the loop runs under one name;
  - this is an argument for continuity, and the standing note in `IDEAS.md` says
    those are the drafter's arguments that lose.
- **`X-b` holds.** The screen pulls the model to its plurality (`V-c`). On the
  bases `PLAN_SCREEN.md` read, the plurality was the true queue about three
  times in ten. A level-3 base decides about a third of the function (`G-d`),
  and a screen is the rules nearest a ticket that none of them decides.
- **`X-c` is refuted: the application carries the larger part.**
  - **The notes say so.** Even when a note names the rule that governs the
    ticket, the proposer names that rule's queue three times in four.
  - **The misreading needs no screen.** It reads a listed rule as covering only
    the values the rule names.
  - **Both arms frame an impasse.** `ARBITRATION_REPORT.md` §5's *"find a gap
    and fill it"* is in the ticket arm too (§5.2).
  - **Information has not helped before.** `CHAT_SUMMARY.md` §2.2's erratum:
    *"With the right information in front of it, it makes the same mistake"*.
- **`X-d` holds.** `V-c` read 0.3178 at the median, three times its line,
  without a manual. The rules give the model a reason to resist its screen, and
  the bet is that they do not remove two thirds of the pull.
- **`X-e` holds**, by `X-b`'s mechanism. Against it: at level 2 the proposer was
  already right two times in three in the loop, so the room is smaller.
- **`X-f` holds.** Compiled once, the same model writes the rules exactly
  (`G-a`). One ticket against them should land far more than a tenth above the
  names alone. Against it: in the loop the rules lifted the choice only from
  0.5210 under the names to 0.5666, though on other tickets and with a screen.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 45 of 105 adjudicated rows were refuted.
- **The last plan.** `PLAN_MANUAL.md`'s drafter got four of six rows right, and
  the row it trusted least went the other way.
- **This plan.** Five expected holds of six is the profile that scoreboard
  warns of.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Every line is the claim's own edge, or a closed thread's: `X-a`'s is
    `F-a`'s, and `X-d`'s is `V-c`'s.
  - A verdict a single run carries is labelled *thin* in advance.

**How the rows read together.**

- **`X-b` and `X-c` hold.** The screen is most of the loss. A loop that asked
  without its screen would apply most of what it was given, and the elicitation's
  cost on the acting axis is the screen.
- **`X-b` holds and `X-c` is refuted.** Both cost, and the application carries
  the larger part. `X-f` then says whether the rules reach the ticket at all.
- **`X-b` is refuted.** With the rules in front of it the screen costs the
  proposer nothing, and what it gets wrong is the application's.
- **`X-d`** says whether authority in the prompt removes deference:
  - **if it holds**, the model defers to its screen even with the policy in
    front of it;
  - **if it is refuted**, the rules dissolve the pull `V-c` measured.
- **`X-f` is refuted.** Without a screen, the rules lift the ticket's answer by
  less than a tenth over the names. The model does not apply the text ticket by
  ticket, and the policy reaches its answers only compiled.
- **`X-e`** is the same question with the prose, and it reads alone.
- **`X-a` is refuted.** `X-b` to `X-f` are still adjudicated as signed. They
  then describe today's model, and `X-a`'s gap stands beside each.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, hard rule 4:
- **`results_manual/loop_L{0..3}_r{1..3}.json`**, `PLAN_MANUAL.md`'s twelve loop
  runs. They hold the escalations, their screens by replay, the truth and the
  loop's answers.
- **`results_manual/sample.json`** and **`results_manual/score.json`**: the
  prompts' digests, and the choice of queue by level.
- **`results_screen/score.json`** and **`results_screen/ask_ticket_only.json`**:
  §3's references, and level-0 answers given on 2026-10-14 to 183 of the 275
  tickets.

**Bought: the model's answers under v1 with level `k`'s manual, reasoning off.**
- **The client.** It is the proposer `manual/run.py` builds for level `k`, and
  its `propose` is called as the loop called it:
  - temperature 0 and 1,200 tokens;
  - `response_format` on the first attempt, and two retries.
- **Hard rule 5 is untouched.**
  - The screen arm's prompts are the loop's, rebuilt.
  - The ticket arm's prompts are what case 0 saw at each level.
  - No text is new.

Three sessions, sequential, in this order:

| session | what is asked | prompts | calls |
|---|---|---|---|
| smoke | at each level, one decision's prompt and one ticket alone, drawn at `ORDER_SEED` | 8 | 8 |
| pass 1 | every screen-arm prompt, 778, and every ticket-arm prompt, 676, in one seeded order with the arms interleaved | 1,454 | 1,454 |
| pass 2 | the same prompts, in another seeded order | 1,454 | 1,454 |

**The ticket-arm prompts are 676**: 275 at level 0, which are every escalated
ticket of every level, and 81, 149 and 171 at levels 1 to 3, each level's own
tickets.

**Cost: 2,916 calls, plus any parse retries.** That is cents at
`deepseek/deepseek-v4-flash`'s listed price. In the twelve loop runs every
proposal parsed, 788 of 790 on the first attempt (`FINDINGS_MANUAL.md`, Stage
B).

**Time, a pass at each pace on record:**
- **`PLAN_FIDELITY.md`'s pace by the wall clock**, 3.8 s an answer with the
  ticket alone and 4.5 to 5.9 s with a screen: 1.7 to 2.0 hours.
- **The loop runs' own pace**, 790 escalations in 78 minutes with the engine
  included: about 2.4 hours.
- **The slowest pace on record**, 12.6 s a call: about 5 hours.

**Both passes outlive a background command of the agent's harness**, which ends
at about half an hour. So they run in Sergi's terminal, as `CLAUDE.md` says.

**What is not bought.**
- **No question for the queue alone.** Every prompt asks for a rule, as the loop
  did (§5.2, §12).
- **No ticket arm across levels 1 to 3.** Each of those levels asks only its own
  tickets; level 0 asks all of them. §2.2 prices the full cross.
- **No other model, prompt version, manual or loop.**

---

## 2. The choices that have to be made at signature time

Signing §0 adopts the drafter's choice in each unless the signature line says
otherwise. A choice that drops a row is a change to §0, and belongs in the same
signed commit.

### 2.1 The population — the drafter recommends every escalation with a screen

Every decision of all four levels: 778. The rows read levels 2 and 3. Levels 0
and 1 cost about 640 calls, an hour of the two passes:
- 216 decisions, about 430 calls of the screen arm;
- level 1's 81 tickets, about 160 calls of the ticket arm;
- 25 tickets only they escalated, 50 calls of level 0's ticket arm.

They buy two things:
- **the same-day control**: what the screen does on an escalation's own screen
  with no manual, conflict screens included, which `PLAN_SCREEN.md` never asked;
- **`X-a` on all four levels.**

**The alternative** is levels 2 and 3 only. It keeps every row, since level 0's
ticket arm is still asked on their tickets for `X-f`, and loses the control.

### 2.2 The ticket alone — the drafter recommends each level's tickets, and level 0 on all

Levels 1 to 3 ask their own tickets, and level 0 asks all 275: 676 prompts. That
is what `X-f` needs, and it gives every level's `acc_t − acc_u` on its own
tickets, reported.

- **More: every escalated ticket at every level.** That is 1,100 prompts
  instead of 676, about 850 more calls and 1.3 more hours. It would set every
  level against every other on the same tickets, without a screen, on both axes:
  - the queue named;
  - the breadth of the rule written.

  That is the mix `PLAN_MANUAL.md` §6.6 could not separate from the choice. It is
  also the mix the notes' reading split only in part.
- **Less: level 0 only on its own tickets.** That saves about 410 calls and
  drops `X-f`.

### 2.3 Two passes, the arms interleaved — the drafter recommends it

Each pass asks every prompt of both arms once, in one order drawn at
`ORDER_SEED`. So within a pass the two arms share the hours and the providers.

**The alternative** is a session per arm, which is how `PLAN_SCREEN.md` ran. It
would put the arms at different hours, and the providers OpenRouter routes the
name to change within a day (§5.9).

### 2.4 No anchor session

The screen arm re-asks the loop's own prompts, so it is its own anchor. `X-a`
costs no call.

### 2.5 This route, and not the loop under v2

`IDEAS.md` names the other route with calls under *What `PLAN_MANUAL.md` opens*:
the loop under v2 with the manual in its prompt. The drafter chose this one, for
four reasons:

- **It is a re-ask, so both arms are asked on one day.** `PLAN_SCREEN.md` set
  answers twelve days apart and had to license them with `V-a`.
- **Its unit is hundreds of paired decisions, not three runs a level.** The
  spread between runs made `G-b` and `G-e` thin.
- **It spends nothing on the loop.** The loop's prompts are already paid for and
  rebuilt for free.
- **It is the acting axis**, where the loop's gap is plainest: 0.5666 against
  1.0000.

The v2 loop asks about the partition, the scope axis, and stays open (§12).

### 2.6 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

All on the corpus. Nothing here is produced by this plan. `X-g1` recomputes the
first two rows and checks them against their record rather than publishing them
again.

| figure | value | owning record |
|---|---|---|
| the proposer's choice at the escalations, pooled by level | `L₀` 62 of 119, 0.5210; `L₁` 34 of 103, 0.3301; `L₂` 164 of 245, 0.6694; `L₃` 183 of 323, 0.5666 | `results_manual/score.json`, `G-g`, published by `FINDINGS_MANUAL.md` |
| the same at `L₃`, by true queue | `T3_ENGINEERING` 8 of 36; `T2_TECHNICAL` 67 of 114; `ACCOUNT_MANAGER` 16 of 31; `ONCALL_ESCALATION` 9 of 9 | same |
| the same at `L₂`, by true queue | `ACCOUNT_MANAGER` 57 of 63; `T3_ENGINEERING` 9 of 24; `ONCALL_ESCALATION` 6 of 9 | same |
| the rules compiled once | `G-a`: 1.0000 of the space, at the median of five asks, each at 1 | same |
| the notes, held out, at `L₃` | 67 of the 90 notes that cite a hidden rule cite the one governing their ticket, and name its queue 50 times; the 23 that cite only other rules name it once | `results_manual/notes.json`, published by `FINDINGS_MANUAL.md`, *The notes beside the rules* |
| `V-b`, the screen's net cost without a manual | +0.0667 (se 0.0191), the median of three bases | `results_screen/score.json`, published by `FINDINGS_SCREEN.md` |
| `V-c`, the pull | 0.3178 (se 0.0266) | same |
| `V-d`, where the plurality is right and where it is not | +0.1583 and +0.2054 | same |
| `V-a`, the instrument over twelve days | +0.0615 without a screen and +0.0284 with one, against 0.05: refuted, thin | same |
| level 3 in pairwise form | shown two hidden rules and a witness ticket, the right winner on 0.8824 of 170 clean pairs | `results2/pair_judgement_baselines.json`, published by `FINDINGS2.md`, Stage C |
| the loop runs' providers | Baidu on 670 of 792 attempts; eight providers under one name | `results_manual/loop_L{k}_r{r}.json`, published by `FINDINGS_MANUAL.md`, Stage B |
| the pace | 3.8 s with the ticket alone, 4.5 to 5.9 s with a screen; the loop runs 790 escalations in 78 minutes | `FINDINGS_FIDELITY.md` and `FINDINGS_MANUAL.md`, Stage B |

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
   `results_screen/` is read-only. `harness/record_guard.py` guards this plan's
   paid records, and the flag that overrides it is not typed without Sergi
   asking.
5. **Do not adjust a prompt, a text or the schema.**
   - The screen arm's prompts are the loop's, and the ticket arm's are case 0's.
   - The texts are `PLAN_MANUAL.md` §5's, pinned by digest.
6. **If the numbers come out badly, report them.** A screen that costs nothing
   is a result, and so is a rule list the model does not apply.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`manual/`, `fidelity/` and `rung2/` are called by this plan and not
   edited**, as `overlap/` calls `authorship/`.
   - The client is `manual.run.build_proposer(level)`.
   - The system prompts are `manual.prompts.loop_system_prompt`.
   - The moments are `fidelity.replay.Replay`'s.
   - The screen arm's prompts are `fidelity.prompts.birth`'s, under the level's
     system prompt.
   - The empty base is `fidelity.prompts.EMPTY_BASE`.
   - The plurality is `fidelity.prompts.plurality`.

   A reimplementation would make these answers incomparable with the loop's for
   a reason that has nothing to do with the screen.
B. **The loop records are inputs, never outputs, and no label reaches a prompt
   or a row Stage B writes.**
   - **Labels join at scoring.** `y` and `ℓ` are copied from the records by
     Stage C. The rows Stage B writes carry neither.
   - **No builder receives a record's row.** The replay reads each row's
     `correct` to keep each rule's counts, as the loop did, and no prompt shows a
     count.
   - **The checks read one label, offline.** `X-g1` sets the loop's choice of
     queue against `PLAN_MANUAL.md`'s `G-g`, before anything is spent, and sends
     nothing.
   - **No module imports the oracle.** The proposer's path is
     `apply/prompts.py` and `apply/ask.py`. It imports by name neither the
     oracle, nor `HIDDEN_DSL`, nor `harness.ceiling_check`, nor
     `rung2.hidden_priority`.
   - **Both join `ONLINE_LOOP`** with `PLAN_MANUAL.md`'s comment. The policy
     reaches the model as the frozen texts, by `manual.levels`, and by no other
     route.
C. **Every record carries `_env`**, with:
   - the model, the temperature and the reasoning setting;
   - each level's system-prompt digest;
   - every attempt's `call_attempts`.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded in full and never
   executed.** No rule is installed, no edge is tried, and no stage of this plan
   codes a note.
F. **The order of Stage B is §8's**, and the module refuses a session out of
   it.

---

## 5. Known traps

**5.1 — The screen is everything the two prompts do not share.**
- **A screen-arm prompt carries the rules shown and a header above them.**
  - On a coverage screen the header is *"REGLAS PROXIMAS de la base (ninguna
    casa este ticket; se listan las que menos condiciones incumplen):"*.
  - On a conflict screen it is *"REGLAS EN CONFLICTO sobre este ticket. Todas
    casan el ticket y ninguna derrota a las demas..."*.
- **A ticket-arm prompt carries** *"BASE DE REGLAS: vacia. Esta es la primera
  regla."*.
- **So `acc_t − acc_s` measures the screen as the loop rendered it, header
  included, against an empty base.** It cannot say whether the rules shown or
  the sentence above them does the work.
- **The coverage header is worth naming.** It tells the proposer that no rule of
  the base matches the ticket, and under the list its notes say that no rule
  matches. Whether the one leads to the other is §12's.

**5.2 — The ticket arm still frames an impasse.**
- **The framing is in both arms.** The system prompt says the engine could not
  decide the ticket and asks for one generalisable rule. The user message calls
  the ticket *en impasse*.
- **That is the operation `ARBITRATION_REPORT.md` §5 names**: *"find a gap and
  fill it"*.
- **So what this plan calls application is application inside the rule-writing
  task.** A question that asks for the queue alone is not asked (§12).

**5.3 — The population is each loop's escalations.**
- **They are selected by each run's base**: the tickets no rule covered there, or
  where rules conflicted. They are not the arrivals.
- **They differ in mix between levels** (`PLAN_MANUAL.md` §6.6).
- **Every row compares arms on the same decisions**, so the mix cancels inside a
  row.
- **Levels are set against each other only through level 0's ticket arm on the
  same tickets.**

**5.4 — One ticket, several decisions.** A ticket's two ticket-arm answers serve
every decision it has at its level. So decisions are not independent draws,
which is why the error is clustered by ticket (§0).

**5.5 — Two dates.** `ℓ` is 2026-10-21's. Every row but `X-a` reads today's arms
only. `X-a` measures the distance, and cannot undo it.

**5.6 — `p` is a function of the screen, not of the model.**
- **What it is drawn from.** On a conflict screen it is the action of a rule
  that matches the ticket. On a coverage screen it is the action of rules that
  do not.
- **The model may follow another action shown**, the first rule's above all.
- **So `X-g` classifies every decision where the two arms' answers differ** by
  what the screen changed the answer to: `p`, the first action shown, another
  action shown, or an action not shown. This is `PLAN_SCREEN.md` §5.4, and
  `blind/cycles.py`'s lesson in `IDEAS.md`: classify every failure before betting
  on one mechanism.

**5.7 — Conflict screens.** 193 of the 778 decisions have one, 70 of them at
level 3.
- **They show rules that match the ticket**, which no screen in
  `PLAN_SCREEN.md` did (its §5.9).
- **The rows pool both kinds**, and `X-g` reads each apart.

**5.8 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Both arms hold
it, so the rows at level 3 measure what the model does with a label it holds.
None of them reads level 3 as something the model knew.

**5.9 — The model can change under its name.**
- **The loop runs were served by eight providers** (§3).
- **Each pass interleaves the arms in one order**, so whatever providers serve
  a pass's hours serve both arms alike.
- **`X-g` reports each arm's mix.** No row is read by provider.

**5.10 — Information in front of the model has not changed what it does
before.**
- **The proposer has erred with the right information shown.**
  `CHAT_SUMMARY.md` §2.2's erratum: *"With the right information in front of
  it, it makes the same mistake"*.
- **It partitioned with the policy in front of it.** With the rules in its
  prompt, the proposer still partitions (`G-c`).
- **Both are priors that the application carries the loss**, against `X-c`. The
  drafter's expectation goes with them, and a reader should weigh it so.

**5.11 — Invalid answers.** As in `PLAN_FIDELITY.md` §5.5, with §0's
thresholds. Every count of a decision left out is published.

**5.12 — Long sessions.**
- **A session that dies keeps what it paid for.** Answers are appended to a
  git-ignored partial file, and the same command resumes there.
- **An outage is not answers.** Five failed calls in a row stop a session
  without recording them.
- **A pass belongs in Sergi's terminal**, because it outlives a background
  command of the agent's harness.

**5.13 — The notes are not read.**
- **They are recorded in full.** Every answer's `note` is recorded whole, where a
  loop record cut it at 280 characters.
- **No stage codes them** (rule E).
- **A reading across the arms would meet §5.1.** An empty base makes *no rule
  matches* literally true of the base.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**X-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.

- **The suite.** `python3 -m unittest discover` is green.
- **The replay.** `fidelity.replay.Replay` rebuilds each of the twelve loop
  records with no departure:
  - every outcome, winner and number of matched rules;
  - every escalation's shown ids and kind;
  - every edge verdict, in the order of the `edge_log`;
  - every rule's final counts.
- **The system prompts.** Each record's is its level's, byte for byte. Its digest
  is the one `results_manual/sample.json` recorded for that level.
- **The loop's choice.** Pooled by level, it comes back from the records'
  `proposal_action_correct` as `results_manual/score.json`'s `G-g` holds it,
  queue by queue.
- **Floats** are compared with a tolerance against records written under 3.12.

**X-g2 — The prompts are the loop's.**

- **The screen arm.**
  - Every decision's prompt is built by `fidelity.prompts.birth` at its moment,
    under its level's system prompt.
  - Its shown ids and kind are the row's `shown_ids` and `shown_kind`, and it
    is not empty.
- **The ticket arm.**
  - Every prompt is its level's system prompt with v1's empty-base rendering,
    and passes `fidelity.prompts.check_ticket_only`.
  - **Teeth.** At each level, the ticket arm's prompt for case 0's ticket is,
    byte for byte, the prompt of that level's empty-screen escalations.
- **The request.** Through `tests/doubles.py`'s SDK double, a call for each arm
  at each level sends exactly what `manual.run.build_proposer(level).propose`
  sends:
  - the model, temperature 0 and 1,200 tokens;
  - `response_format` on the first attempt, and reasoning off;
  - the two messages.
- **Level 0 is `PLAN_SCREEN.md`'s prompt.** On the 183 tickets that plan asked
  with the ticket alone, level 0's ticket-arm prompt carries the digest that
  plan recorded.
- **The plurality.** `p` is computed for every decision, from its rebuilt
  prompt.
- **No builder takes a record's row.**
- **Teeth.** One changed shown rule moves its prompt's digest, and no digest
  stands for two texts. Thirteen asks share their text with another: early in a
  run, two runs' bases can be the same. Each is still its own decision, asked
  on its own.

**X-g3 — The populations and the schedule are §0's and §1's.**

- **The decisions.** There are 778: 116, 100, 242 and 320 by level, and 193 on
  conflict screens. The 12 empty screens are left out.
- **The ticket-arm prompts.** There are 676: 275 at level 0, and 81, 149 and 171
  at levels 1 to 3.
- **The passes.** Each holds every prompt of both arms once, 1,454, in its
  order rebuilt from `ORDER_SEED`. The two orders differ.
- **The smoke.** Its eight prompts are drawn from those by `ORDER_SEED`.

**X-g4 — The signature**, §10.

---

## 7. Stage A — the design and the free readout (free, gated)

**Deliverable.** `apply/sample.py` → `results_apply/sample.json`.

- **`X-g1` to `X-g3`.**
- **The design.**
  - The decisions, with their level, run, case, screen kind and ticket.
  - Every prompt's digest.
  - The three sessions' orders at `ORDER_SEED`.
- **`X-g`'s reference columns, computed after the signature.**
  - The loop's own accuracy on the decisions, by level, run, screen kind and
    true queue.
  - `p` on every decision, and how often it is the true queue and how often the
    loop's answer.
  - Two copiers scored on the truth: one answers `p`, and one the first action
    shown.
  - The decisions' class mix.

**It produces nothing adjudicable.** It runs after §0 is signed so that none of
its figures can inform a band.

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `apply/ask.py` → `results_apply/ask_smoke.json`,
`ask_pass1.json` and `ask_pass2.json`. **Three sessions, in that order, one after
another. Each record is committed before the next session starts.**

**Every session, before any call**, follows `PLAN_SCREEN.md` §8's order:

1. **`--dry-run`** runs `X-g1` to `X-g3` and stops. It builds no client and needs
   no key.
2. **The signature (`X-g4`).** While `PLAN_APPLY.md` carries a blank signature
   line, the module exits here.
3. **What comes before it.** A pass needs the smoke record, under this
   protocol, with a valid answer from each arm. Pass 2 also needs pass 1's
   record.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`X-g1` to `X-g3`, blocking.** Stage A's record must hold the same design and
   digests.
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls.** They are sequential, with reasoning off on
   every one.

**What each record carries, per call:**

- **Which call**: the session, the pass and the position.
- **What was asked**:
  - its id, which names the decision or the ticket, and Stage A's record says
    which decisions each ask serves;
  - the arm and the level;
  - the prompt's digest and the ids shown.
- **The answer**:
  - its `action` and its whole payload, or the failure;
  - every attempt's `call_attempts`, provider and finish reasons included.
- **When**: the seconds and the time.
- **No label.** Stage C joins `y` and `ℓ` from the loop records (rule B).

## 9. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `apply/score.py` → `results_apply/score.json`, and
`results_apply/FINDINGS_APPLY.md`, which owns every figure.

- **`X-a` to `X-f`**, each against its line, exactly, with its clustered
  standard error, *thin* and *unadjudicable* as §0 defines them.
- **Each row's parts and per-run values**, never summed into the verdict.
- **`X-g` in full.**
- **The run itself**: failed calls, invalid actions, retries, and the pace per
  session.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `apply/sample.py` and `apply/score.py` spend nothing. `apply/ask.py`
refuses before it constructs a client. **The free stages get the gate because
what it protects is not money.** Stage A counts how often a decision's plurality
is the true queue, and how often it is the loop's answer. Those two shares are
exactly what would inform `X-b`'s and `X-d`'s bands.

**The gate reads `PLAN_APPLY.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.**
  - `MODEL`, `PROMPT` and `REASONING` are imported from `manual.plan`, and the
    proposer is `manual.run.build_proposer`.
  - It keeps its own `max_tokens` of 1,200 and its two retries.
- **The inputs.** `manual.plan`'s `LEVELS`, `REPS`, `N`, `SEED` and `loop_path`,
  imported and not retyped.
- **The populations.**
  - `DECISIONS = {0: 116, 1: 100, 2: 242, 3: 320}`.
  - `CONFLICT_DECISIONS = {0: 11, 1: 37, 2: 75, 3: 70}`.
  - `EMPTY_SCREENS = 12`.
  - `TICKET_PROMPTS = {0: 275, 1: 81, 2: 149, 3: 171}`.
  - `SHARED_WITH_SCREEN = 183`.
- **The sessions.**
  - `SESSIONS = ("smoke", "pass1", "pass2")`.
  - `PASSES = 2`.
  - `SMOKE_PER_ARM_AND_LEVEL = 1`.
- **The seed.** `ORDER_SEED = 67`.
  - **It is new.** It is distinct from every seed a closed thread uses: 17 to
    20, 25, 41, 43, 47, 53, 59 and 61, and values from 1000 up.
  - **It feeds three streams**, one string seed per session.
  - **It is hash-free.** CPython seeds a string through SHA-512, so no order
    depends on `PYTHONHASHSEED`.
- **The limits.**
  - `MIN_SIGNATURES = 1` and `MAX_CONSECUTIVE_FAILURES = 5`.
  - `MAX_INVALID_SHARE = Fraction(1, 20)` and `MIN_PULL_POPULATION = 100`.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `X_A_MAX_GAP = Fraction(1, 20)`.
  - `X_B_LINE = 0`, held above.
  - `X_C_LINE = Fraction(1, 2)`.
  - `X_D_LINE = Fraction(1, 10)`.
  - `X_E_LINE = 0`, held above.
  - `X_F_LINE = Fraction(1, 10)`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
apply/__init__.py
apply/plan.py        the gate and the constants of §10
apply/population.py  the decisions and the tickets, from the loop records and the replay
apply/prompts.py     both arms' prompts, and p                       [proposer's path]
apply/gates.py       X-g1 to X-g4
apply/sample.py      Stage A
apply/ask.py         Stage B: it spends                              [proposer's path]
apply/score.py       Stage C
results_apply/FINDINGS_APPLY.md
results_apply/sample.json  ask_smoke.json  ask_pass1.json  ask_pass2.json  score.json
tests/test_apply.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `apply` joins it in `harness/provenance.py`, and joins the
  oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP`.** The two modules marked above join it, with rule B's comment
  and a test that adds `HIDDEN_DSL`, `ceiling_check` and `hidden_priority` to
  their forbidden imports.
- **The partial files**, `results_apply/*.partial.jsonl`, join `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site** is `rung2/proposers2.py`'s, which `tests/test_call_record.py`
  already classifies, as for `manual/run.py`.
- **The README's table of writers** gains its rows.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_apply/` with `_env`, the model, the temperature, the
      reasoning setting, the system prompts' digests and `call_attempts`,
      produced with `PYTHONHASHSEED=0`.
- [ ] `X-g1` to `X-g4` passed before any record was written. The key check and
      the smoke run came before the first pass, and each session's record was
      committed before the next began.
- [ ] The plumbing of §10, and tests pinning:
      - the constants and the gate;
      - the populations;
      - the replay of the twelve records;
      - the prompts against the loop's, with their teeth;
      - the unchanged request;
      - the exactness of §0's comparisons and the clustered error.
      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface (the corpus, always), its level,
      its arm, its denominator, and the date of each side it compares.
- [ ] `results_apply/FINDINGS_APPLY.md` owns every figure, with a dated erratum
      wherever it corrects something already published. That includes this
      plan's §0 *already seen*, if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `X` thread. *What is open* narrows
      its second and fourth items by what this plan settles.
- [ ] `IDEAS.md`:
      - *Why the proposer applies the rules it was given four times in ten
        wrongly* is closed or narrowed, with what this plan opens;
      - `PLAN_SCREEN.md`'s *Conflict screens* item gets `X-g`'s reading.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `X`, and its `TABLES` gains
      `FINDINGS_APPLY.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits; the plan and its
      signature are alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **Which part of the screen does the work**: the rules shown, or the header
   above them (§5.1). A ticket-arm prompt that kept the coverage header over an
   empty list is not a state the loop ever produced. It would be a new prompt,
   and so another plan.
2. **Application outside the rule-writing task** (§5.2). A question that asks
   for the queue alone is a new prompt, and another plan.
3. **Why the list's proposer reads a matching rule as not covering its ticket.**
   The notes are recorded and not coded (§5.13).
4. **The loop.** This plan re-asks. Whether a loop that asked without its screen
   would compile what it is told is a run. `IDEAS.md` carries two forms of it:
   random escalation asked without a screen, and a loop that starts from the
   compiled manual.
5. **The scope axis.** The breadth of the rules written is reported. Whether the
   list narrows rules without a screen, on the same tickets as the prose, needs
   §2.2's larger cross.
6. **The partition.** The loop under v2 with the manual stays open (§2.5).
7. **One model, one manual, three runs a level, one day**, and providers this
   plan does not pin.
