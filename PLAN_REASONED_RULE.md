# PLAN_REASONED_RULE — the rule written with reasoning on: whether reasoning carries into the queue a rule-writer chooses

**Status: drafted by Claude on 2026-10-25, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**Asked for by Sergi on 2026-10-25**, after `PLAN_FIRST_MATCH.md` closed: the
cheap half of the loop with reasoning on, before any loop runs.

**The item.** `PLAN_FIRST_MATCH.md` asked level 3's escalated tickets again,
with the 29 rules in the prompt and no screen, for the queue alone.

- **With reasoning on, the model applies the list on every escalated
  decision.** It is right on all 320 of level 3's decisions, on both answers
  (`FM-e` holds).
- **Without it, it is right on 0.7422 of them**, and where it errs on the order
  it believes a lower rule applies (`FM-c` holds)
  ([`FINDINGS_FIRST_MATCH.md`](results_first_match/FINDINGS_FIRST_MATCH.md)).
- **That is not the question the loop asks.** The loop's proposer is asked for
  a rule, under v1's impasse framing, and it has asked with reasoning off since
  `PLAN_REUSE.md` §1's amendment of 2026-09-30. Asked for a rule on the same
  tickets, with the rules and no screen and reasoning off, the model was right
  on 0.6840 of the decisions `PLAN_QUEUE_ALONE.md`'s rows read
  ([`FINDINGS_QUEUE_ALONE.md`](results_queue_alone/FINDINGS_QUEUE_ALONE.md)).

That record's Stage C left this as its fourth item:

> *The loop with reasoning on. The loop's proposer writes rules with reasoning
> off and 1,200 tokens. Whether reasoning carries into the rule-writing prompt,
> and into what the loop compiles, is a new run under a larger budget, and a
> plan.*

[`IDEAS.md`](IDEAS.md) carries it first under *What `PLAN_FIRST_MATCH.md`
opens*, with its cheap half first: *`PLAN_QUEUE_ALONE.md`'s rule arm asked with
reasoning on, on the same tickets, would say whether reasoning carries into the
queue a rule-writer chooses, before any loop runs.* [`STATUS.md`](STATUS.md)'s
*What is open* ends its second item on it.

**Three candidates, each with a reason on record.**

- **Reasoning carries.** What reasoning buys the plain question is the walk
  down the list (`FM-d`, `FM-e`). Nothing in the rule-writing prompt stops the
  model from taking that walk: the reasoning comes before the answer, and the
  answer opens with the queue.
- **The rule-writing task takes the reasoning.** v1 asks for a queue, one
  generalisable rule, its place among the rules that exist, and a note. A model
  that reasons may spend its thinking on the rule and not on the list.
- **The framing turns the reasoning against the list.** v1 tells the model that
  the engine could not decide the ticket.
  - `ARBITRATION_REPORT.md` §5 names the operation that framing invites: *"find
    a gap and fill it"*.
  - The notes coded POST-RUN show the list's proposer reading a rule that
    matches its ticket as not covering it
    ([`FINDINGS_MANUAL.md`](results_manual/FINDINGS_MANUAL.md), *The notes
    beside the rules*).
  - A model that reasons from that framing may argue that the list does not
    settle the ticket, and decide it by its own judgement.

**The question, in its cleanest form.** At the escalations of `PLAN_MANUAL.md`'s
loop, with the 29 rules in the prompt and no screen:
- asked for a rule with reasoning on, is the model right more often than
  without?
- does it then apply the list nearly as exactly as it transcribes it?
- does reasoning shrink what asking for a rule costs the queue?

**Nothing has to be re-run but the model.** `PLAN_QUEUE_ALONE.md`'s design holds
the population. `queue_alone/population.py` rebuilds it from `PLAN_APPLY.md`'s,
which rebuilds it from the twelve loop records.

Four arms are bought, all on the day this plan runs and all under one
provider. Every prompt is asked twice.
- **The rule arm, `t`.** This is `PLAN_QUEUE_ALONE.md`'s rule arm at level 3,
  its prompts byte for byte, with reasoning off. It is asked again so that
  every row compares arms asked on one day.
- **The reasoning rule arm, `w`.** The rule arm's prompt byte for byte, with
  reasoning on. It is the only arm no closed plan has asked.
- **The plain arm, `q`.** `PLAN_QUEUE_ALONE.md`'s plain arm at level 3, which is
  `PLAN_FIRST_MATCH.md`'s plain arm, with reasoning off.
- **The reasoning arm, `r`.** `PLAN_FIRST_MATCH.md`'s reasoning arm: the plain
  arm's prompt with reasoning on.

The four are two factors crossed: what is asked, a rule or the queue alone, and
whether the model reasons. Every arm is asked at level 3 only, on level 3's
escalated tickets.

**What it changes in what is measured, said first.**
- **It installs nothing.** No rule is born, no base grows, and no figure here
  continues a loop's.
- **It reads one axis.** That is the acting axis of `CLAUDE.md` Step 5: the
  queue named for the ticket in front of the model. The rules the two rule arms
  write are read beside it and reported, never adjudicated (§5.10).
- **No prompt is new.** Every arm's prompt is a closed plan's, byte for byte,
  so hard rule 5 is not engaged. What is new is one setting on one prompt:
  reasoning on, for the rule-writing prompt.
- **The proposer's calls have had reasoning off since `PLAN_REUSE.md` §1's
  amendment**, signed on 2026-09-30. Nothing here moves that setting for any
  other plan or loop. The amendment turned reasoning off for two reasons:
  reasoning spent the answer's 1,200 tokens, and off was the drafter's best
  estimate of the instrument August measured. It did not find that reasoning
  writes worse rules, and nothing since has asked.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The surface is the corpus, and the population is the escalations.**
- **Every figure is about tickets that escalated.** They are tickets of
  `generate_corpus(2000, seed=17)` that escalated in one of `PLAN_MANUAL.md`'s
  three level-3 loop runs.
- **No row has an exhaustive-space reading.** What is asked is the model, about
  tickets that arrived and that the loop could not decide. Only `RR-e`'s
  reading of the rules written is over the space, and it is reported.
- **The decisions and the tickets are `PLAN_FIRST_MATCH.md`'s**, which are
  `PLAN_QUEUE_ALONE.md`'s at level 3:

| level | decisions | the tickets they lie on | ticket prompts asked, per arm |
|---|---|---|---|
| `L₃`, the rules | 320 | 170 | 171 |

- **A decision is an escalation whose screen is not empty**, as in
  `PLAN_APPLY.md`, `PLAN_QUEUE_ALONE.md` and `PLAN_FIRST_MATCH.md`. No screen is
  shown here. The rows read decisions, so that `acc_t` here is the statistic
  `QA-b`'s 0.6840 was. A ticket weighs as many times as the loop escalated it
  with a screen.
- **The 171st prompt serves no decision.** Ticket 0 escalated before any rule
  existed, so it never had a screen. `RR-a`, which reads prompts, reads it.
- **The rows read by ticket instead are reported** in `RR-e`.

**The arms and the notation**, per decision.

- **`y`** is the true queue: the record row's `truth`.
- **`m₁, m₂, …`** are the rules of level 3's frozen text that the ticket
  matches, in the list's order. `m₁`'s queue is `y`, which `RR-g1` checks on
  every decision through the closed plans' checks. **The runner-up** is the
  first matching rule whose queue is not `y`.
- **`t₁` and `t₂`** are the rule arm's two answers on the decision's ticket, in
  pass 1 and pass 2. A ticket that serves several decisions lends both to each.
- **`w₁` and `w₂`** are the reasoning rule arm's answers, **`q₁` and `q₂`** the
  plain arm's, and **`r₁` and `r₂`** the reasoning arm's.
- **`tᴬ`** is `PLAN_QUEUE_ALONE.md`'s rule-arm answer on the same prompt, given
  on 2026-10-24, one per pass.
- **`t̄`** is `½(1[t₁=y] + 1[t₂=y])`, and `w̄`, `q̄` and `r̄` are defined
  likewise. `acc_t`, `acc_w`, `acc_q` and `acc_r` are their means over a row's
  decisions.
- **An answer is *valid*** when its `action` is one of the eight queues and the
  provider that served it is the one pinned (§2.4). For the two rule arms that
  holds whether or not the rule written with it would validate, as in
  `PLAN_APPLY.md` and `PLAN_QUEUE_ALONE.md`. **A decision enters a row only with
  every answer that row reads valid.**

**The classes.** An answer's class is `PLAN_QUEUE_ALONE.md` §5.6's, by its
queue: *first*, the queue of `m₁`, which is `y`; *order*, another queue, given
by a lower matching rule; *matching*, a queue no matching rule gives. Every
answer of every arm is classed in `RR-e`, and no row bets on a class.

**The unit, the error and *thin*.** All of it is settled here and not in the
scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict. It is
`PLAN_QUEUE_ALONE.md`'s and `PLAN_FIRST_MATCH.md`'s, unchanged.

- **Every row is pooled over level 3's three runs**, decision by decision. The
  run is not the unit: the question is about the model's answer to a prompt,
  and the runs are unequal.
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

  `RR-a` reads prompts and not runs, so only the first case applies to it.

**When a row has no value.**
- **A row has none** if more than 5% of its decisions lack the valid answers it
  reads.
- **`RR-a` reads prompts, not decisions.** It has none if fewer than 100 prompts
  hold today's two answers valid and a valid answer of `PLAN_QUEUE_ALONE.md`'s
  from the pinned provider.
- **`RR-d` also has none** if `acc_q − acc_t ≤ 0`. Without reasoning, asking for
  a rule then costs the queue nothing, and there is no cost for reasoning to
  shrink. That is `QA-d`'s condition, for the same reason.

A row with no value is unadjudicable, and the record says so.

**Which side had the label**, for every arm. This was checked against the
prompts while drafting, and not recalled, as `CLAUDE.md` asks of any plan that
sets a comparison on the proposer:

| arm | what it is handed | reads a label? |
|---|---|---|
| all four | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."* | **yes**: every ticket's label is derivable from the text by first match |
| `tᴬ` | the rule arm's prompt, on 2026-10-24 | as the rule arm |

- **The four arms hold the same manual.** No row sets a side that has the label
  against one that has not.
- **No arm sees an example**, and nothing here is fitted, so nothing reaches a
  test split.
- **No baseline is set against the proposer.** The two rule arms are the
  proposer's own prompt, with and without reasoning. The other two are
  questions to the same model through the same request.

**The retry, settled here.** It is `PLAN_FIRST_MATCH.md`'s. **A failed call is
retried with the same messages, after a wait, and only a failed parse is
retried with v1's message**, which tells the model its answer was not valid
JSON. `PLAN_QUEUE_ALONE.md`'s rule arm retried any failed attempt with that
message, and today's rule arm does not, so their requests differ after a
failed call and nowhere else. Every row says which retries it took.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **RR-a** | **The rule arm has not moved since `PLAN_QUEUE_ALONE.md` asked it.** Re-asked under the same provider, it agrees with that plan's answers about as often as it agrees with itself | over level 3's rule prompts that hold today's two answers valid and a valid answer of `PLAN_QUEUE_ALONE.md`'s from the pinned provider: `S − A`. `S` is the share whose two answers today agree. `A` is the mean, over today's two answers and that plan's answers, of their agreement | **≤ 0.05** | **> 0.05** |
| **RR-b** | **With reasoning on, the model asked for a rule chooses the right queue more often** than asked the same prompt without it | over `L₃`'s decisions: `acc_w − acc_t` | **> 0** | **≤ 0** |
| **RR-c** | **With reasoning on, the model asked for a rule applies the 29 rules nearly as exactly as it transcribes them** | over `L₃`'s decisions: `acc_w` | **≥ 0.90** | **< 0.90** |
| **RR-d** | **Reasoning shrinks what asking for a rule costs the queue.** With reasoning on, the rule-writing prompt falls short of the plain question by less than it does without | over `L₃`'s decisions: `(acc_r − acc_w) − (acc_q − acc_t)` | **< 0** | **≥ 0** |
| **RR-e** | *Reported, not adjudicated.* **What the drafter could not band** | Each arm's accuracy, with its runs, and by ticket instead of by decision. Every answer of every arm in §5.6's classes, and each arm's order errors by where they go: the next matching rule, the runner-up, the catch-all, the most specific rule. Each arm's accuracy by the rule that governs the ticket. The table by true queue, with `ONCALL_ESCALATION`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER` and `T3_ENGINEERING` in counts. `S` for each arm, and how often the arms agree with each other. `PLAN_QUEUE_ALONE.md`'s rule arm, and `PLAN_FIRST_MATCH.md`'s plain and reasoning arms, each beside today's on the same decisions. **The rules the two rule arms write**, over every valid answer to every rule prompt: whether each validates under rung 2's validator and why not; whether it matches its ticket; its conditions; its region over the space, and the share of that region where the list's first match gives the rule's queue, with how many rules get all of it; whether its region is one of the 29 rules', and whether that rule governs its ticket; how many answers declare `beats` or `loses_to`, and how many of those cite the list's identifiers. Each arm's providers, finish reasons, tokens, reasoning tokens, seconds and retries by cause. The reasoning of the two reasoning arms and the notes of the two rule arms, recorded in full and not coded | — | — |

**Signed by Sergi: ____________________ (date: __________)**

**Why each row, and why these lines.**

- **`RR-a` is the instrument row.** Its line is `X-a`'s, `F-a`'s, `V-a`'s,
  `QA-a`'s and `FM-a`'s.
  - **It reads the rule arm's prompts**, because that arm is asked byte for
    byte as `PLAN_QUEUE_ALONE.md` asked it, under the same pin, and the
    reasoning rule arm shares them.
  - It says how far today's rule arm stands for that plan's, so that what that
    plan read of it can be set beside today's arms. It cannot undo the
    distance.
- **`RR-b` reads what reasoning does to the queue a rule-writer chooses.** Its
  line is the literal *more often*. It is `FM-d` asked of the rule-writing
  prompt.
- **`RR-c` is the application with reasoning, read against compiling.**
  Compiled once, the same model writes the 29 rules exactly (`G-a`). The line is
  `QA-e`'s and `FM-e`'s, a tenth below exact, so `RR-c` reads directly beside
  `FM-e`'s hold on the plain question.
- **`RR-d` crosses the two factors.** Without reasoning, asking for a rule costs
  the queue `acc_q − acc_t`; with it, `acc_r − acc_w`. The row asks whether the
  second is smaller. Its line is the literal *less*, so a tie goes against the
  claim: a cost that stays the same has not shrunk. With no cost to shrink the
  row has no value, settled above and not in the scorer.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md`**: its opening notes, the scoreboard with its convention, its
  table and its named lists, *What is open* with every dated note in it, and
  *What this does not show*. Not *What is established*, nor *What was
  withdrawn*.
- **`IDEAS.md`**: its header and *No longer here*, *Pending and already
  specified*, the sections on `PLAN_FIRST_MATCH.md`, `PLAN_QUEUE_ALONE.md`,
  `PLAN_APPLY.md`, `PLAN_MANUAL.md` and `PLAN_UNREACHED.md`, *What the outside
  reading of October 2026 proposes*, *What `ARBITRATION_REPORT.md` §7
  proposes*, *What rung 4 opens*, *Technical debt*'s *What that leaves open*,
  and *Prior to the four rungs*.
- **The first-match thread.** `PLAN_FIRST_MATCH.md` and
  `FINDINGS_FIRST_MATCH.md`, whole, with every figure they publish:
  - the six verdicts, with their parts and runs;
  - `FM-g`'s tables by arm, by named rule, by governing rule and by true queue,
    its agreement figures, and Stage B's tokens, seconds and costs.
- **The queue-alone thread.** `PLAN_QUEUE_ALONE.md` from its opening to the end
  of §5, and `FINDINGS_QUEUE_ALONE.md` whole, with every figure it publishes:
  - the six verdicts, with their parts and runs;
  - `QA-g`'s tables by level, by true queue and by §5.6's classes, and its
    agreement figures;
  - *Where the order errors go*, POST-RUN.
- **No JSON record of either thread was read for a figure.** The drafter listed
  the keys of `results_reuse/run_n20_smoke_reasoning_on.json` (below), and
  counted the attempt entries of every record under `results*/` that carry a
  `reasoning_tokens` field (below). Neither reads a label or an answer.
- **`PLAN_REUSE.md` §1's amendment**, whole: the default reasoned 20 tokens on
  a six-token reply and none with `{"effort": "none"}`, and its third smoke run
  lost 5 of 15 proposals under 1,200 tokens.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  They were not read whole for this plan. The passages it rests on were read
  directly:
  - `ARBITRATION_REPORT.md` §5, its diagnosis, and §9, its limits;
  - `CHAT_SUMMARY.md`'s header list of errata, and §2.2's erratum of
    2026-08-12, as `PLAN_PAIRWISE.md` §4's rule C asks;
  - `EXTERNAL_REVIEW.md` §5.
- **The code the package calls.**
  - `rung2/proposers2.py`, whole: v1, `user_msg`, `parse_payload` and
    `OpenRouterProposer2`, whose request caps an answer at 1,200 tokens;
  - `rung2/engine2.py`'s `Space` and `validate_conditions`;
  - `manual/run.py`'s `build_proposer`, and `manual/prompts.py` whole;
  - `apply/prompts.py`;
  - `queue_alone/`'s `plan.py`, `prompts.py`, `population.py`, `rules.py` and
    `ask.py`;
  - `first_match/`'s `plan.py`, `prompts.py`, `population.py`, `ask.py`,
    `gates.py`, `sample.py` and `score.py`, and the list of
    `tests/test_first_match.py`'s tests;
  - `rung3/order_search_ls.space_truth_masks`, `manual/gates.py`'s
    `installer_on_the_policy`, and the space helpers of `manual/instrument.py`;
  - the registries the plumbing joins: `harness/provenance.py`'s `CODE_ROOTS`,
    `tests/test_oracle_separation.py`, `tests/test_writer_lists.py`,
    `tests/test_call_record.py` and `tests/test_prose_tables.py`.
  - **Writing the package, after the draft above was committed**:
    `queue_alone/score.py`'s `answer`, `Prompt`, `anchor_term` and
    `adjudicate_anchor`; `apply/score.py`'s helpers and its `rules_written`;
    `queue_alone/gates.py`'s `same_verdict`; `reuse/gates.py`'s `run_suite`;
    `harness/dsl.py`'s `Condition`; `tests/doubles.py`'s SDK double; and
    `tests/test_first_match.py`, whole.
- **The package's checks, run before the signature.** They recompute
  `PLAN_FIRST_MATCH.md`'s six verdicts from its passes and compare them with
  its record, and, through that plan's checks, `PLAN_QUEUE_ALONE.md`'s. They
  print only whether each comparison passes.
- **One rule read against one ticket, while writing `reasoned_rule/shape.py`.**
  To try the reading, the drafter read a rule written by hand, *product eq api*
  to `T2_TECHNICAL`, against ticket 0's case. That printed the rule that governs
  ticket 0, which serves no decision, and how much of that rule's region over
  the space the list sends to `T2_TECHNICAL`. Neither is an answer of the model,
  and neither bears on a band. Every test reads rules and tickets built by hand.
- **The manual's level-3 text**, `manual/texts/rules.txt`, whole: the 29 rules
  and the first-match sentence.
- **OpenRouter.** Not read for this plan. Its listing of this model's
  endpoints and its documentation of reasoning were read on 2026-10-25 by
  `PLAN_FIRST_MATCH.md`'s drafter, and §3 cites that reading.
- **Counts computed while drafting.** None of them reads a label or an answer.
  - **The prompts.** At level 3 the rule arm's system prompt runs 5,044
    characters and its user message about 270; the plain arm's run 3,476 and
    about 210. The rule and plain prompts of level 3 carry 342 distinct texts,
    and the rule prompts serve each of the 320 decisions once.
  - **No recorded attempt reasoned on a rule-writing prompt.** Of the 8,886
    attempt entries under `results*/` that carry a `reasoning_tokens` field,
    344 are above 0, and all of them are `PLAN_FIRST_MATCH.md`'s reasoning arm:
    171 in each pass and 2 in its smoke run, all on the plain prompt.
  - **`PLAN_REUSE.md`'s third smoke run keeps no attempt and no reasoning.** Its
    record, `results_reuse/run_n20_smoke_reasoning_on.json`, carries neither
    `call_attempts` nor a `reasoning` or `reasoning_tokens` field anywhere.
  - **The design, as the package builds it.** 684 prompts, 171 an arm, every one
    of level 3's 320 decisions served once in each arm, and 342 distinct texts
    behind them, since each reasoning arm shares its texts with its quiet arm.

**Not seen, because nothing has produced it:**

- any answer to the rule-writing prompt given with reasoning on and recorded
  with its attempts, and any reasoning written before a rule;
- how long the model reasons before writing a rule, and so the reasoning rule
  arm's pace and cost (§1);
- which rule the model writes with reasoning on, and which identifiers it
  cites.

Stage A computes, after the signature, which rules match each decision's ticket
and which is its runner-up. `PLAN_FIRST_MATCH.md`'s Stage A published their
counts, which the drafter has seen.

**What the drafter expects, written down so the scoreboard can score it.**
**All four hold: `RR-a`, `RR-b`, `RR-c` and `RR-d`.** The drafter trusts `RR-a`
most, then `RR-b` and `RR-c`, and `RR-d` least.

- **`RR-a` holds.** One provider answers both sides, and `QA-a` and `FM-a` held,
  by +0.0062 and −0.0117. At level 3 the rule arm's two answers agreed 0.8969
  of the time. Against it:
  - the retry protocol changed, though only after a failed call;
  - this is an argument for continuity, and the standing note in `IDEAS.md`
    says those are the drafter's arguments that lose.
- **`RR-b` holds.** The rule arm's first task, in v1's own words, is *"Decidir
  la cola de destino correcta para ESTE ticket"*, and the manual's block calls
  the list *"la politica que hay que seguir"*. A model that reasons before it
  answers can take the walk down the list that `FM-d` measured, whatever it
  writes after the queue. Against it: the rule-writing task and the impasse
  framing each took about half of what the plain question gained without
  reasoning (`QA-d`'s parts), and reasoning can serve them as well as the list.
- **`RR-c` holds.** The plain question with reasoning was right on every
  decision, and the rule arm asks the same question first. Against it:
  - **these are the hard tickets**, the ones the loop could not decide;
  - **the framing tells the model the engine could not decide the ticket.** A
    model that reasons from it may argue that no rule of the list covers the
    ticket, which is what the notes under the list say (§5.7);
  - **v1 describes another arbitration than the manual's** (§5.8), and a model
    that reasons may weigh it;
  - **a truncated answer is invalid.** A rule is longer than a queue, so the
    reasoning rule arm's answer needs more room after its reasoning. If more
    than a twentieth of the decisions come back cut off, the row has no value
    rather than a verdict.

  The drafter's guess is that the reasoning rule arm lands near 0.97.
- **`RR-d` holds, and the drafter trusts it least.** If `RR-c` holds near 0.97
  and the reasoning arm is near exact again, the cost with reasoning is a few
  hundredths. Without reasoning it was 0.0849 on 2026-10-24 (`QA-b`). Against
  it:
  - **the comparison is a difference of differences**, so its noise is the sum
    of four arms', and a few hundredths may not clear it: the row may well be
    thin;
  - **today's cost without reasoning is not yesterday's.** If today's rule arm
    lands nearer the plain arm, there is less to shrink, and with none the row
    has no value;
  - **the framing may cost more under reasoning, not less**, by the third
    candidate above.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 50 of 123 adjudicated rows were refuted.
- **The last two plans.** `PLAN_QUEUE_ALONE.md`'s drafter and
  `PLAN_FIRST_MATCH.md`'s each got five rows of six, and each missed the row it
  trusted least.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Every line is the claim's own edge, or a closed thread's: `RR-a`'s is
    `QA-a`'s and `FM-a`'s, and `RR-c`'s is `QA-e`'s and `FM-e`'s.
  - `RR-d`'s condition for having no value is `QA-d`'s.
  - A verdict a single run carries is labelled *thin* in advance.

**How the rows read together.**

- **`RR-b` and `RR-c` hold.** Reasoning carries into the queue a rule-writer
  chooses: asked for a rule with reasoning on, the model applies the list it was
  handed. A loop that reasons would choose its queues at the escalations nearly
  as the list says. What it would compile is a further question: `RR-e` reads
  the rules written, and the loop is a plan of its own.
- **`RR-b` holds and `RR-c` is refuted.** Reasoning helps the rule-writer and
  leaves more than a tenth wrong. `RR-d` then says whether asking for a rule is
  what holds it back, and the reasoning the record keeps says what the model
  did, for a reading after the verdicts.
- **`RR-b` is refuted.** Reasoning does not carry into the rule-writing prompt:
  the task or the framing takes it. A loop that reasons, asked as v1 asks, would
  not choose its queues better, and its plan would have to ask for the queue
  apart from the rule.
- **`RR-d` holds.** With reasoning on, asking for a rule costs the queue less
  than without. **`RR-d` is refuted.** It costs as much or more, so a loop that
  reasons should still ask for the queue apart from the rule.
- **`RR-a` is refuted.** `RR-b` to `RR-d` are still adjudicated as signed. They
  then describe today's model under one provider, and `RR-a`'s gap stands
  beside each.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, hard rule 4:
- **`results_manual/loop_L3_r{1..3}.json`**, `PLAN_MANUAL.md`'s three level-3
  loop runs: the escalations, their tickets and the truth. The nine other runs
  are read by the closed plans' checks, which `RR-g1` calls.
- **`results_queue_alone/sample.json`**: `PLAN_QUEUE_ALONE.md`'s design, every
  prompt's digest and the system prompts.
- **`results_queue_alone/ask_pass1.json` and `ask_pass2.json`**: `tᴬ`, for
  `RR-a`, with the provider of every answer.
- **`results_queue_alone/score.json` and `orders.json`**, and
  **`results_first_match/sample.json`, `ask_pass1.json`, `ask_pass2.json` and
  `score.json`**: §3's references, and what `RR-g1` recomputes.

**Bought: the model's answers with level 3's manual, every call pinned to one
provider.** All four arms go through one asker, `PLAN_FIRST_MATCH.md`'s, with
this plan's settings in its request, and through `harness/call_record.py`.
Every request sends:
- the model, temperature 0, and `response_format` on the first attempt;
- the provider pin of §2.4;
- **in the rule and plain arms**, reasoning off, `{"effort": "none"}`, and
  1,200 tokens, as `PLAN_QUEUE_ALONE.md`'s rule and plain arms did;
- **in the reasoning rule and reasoning arms**, reasoning `{"effort": "high"}`
  and 16,000 tokens, as `PLAN_FIRST_MATCH.md`'s reasoning arm did (§2.2).

**Two retries, `PLAN_FIRST_MATCH.md`'s (§0).**
- **A failed call**, one that raised before any answer came back, is retried
  with the same messages, after 10 seconds and then 30.
- **A failed parse**, an answer that came back and is not a JSON object, is
  retried with v1's retry message, as v1 does.
- **The record keeps the cause of every retry.**

Three sessions, sequential, in this order:

| session | what is asked | prompts | calls |
|---|---|---|---|
| smoke | two tickets in each arm, drawn at `ORDER_SEED` | 8 | 8 |
| pass 1 | every prompt of the four arms, 171 each, in one seeded order with the arms interleaved | 684 | 684 |
| pass 2 | the same prompts, in another seeded order | 684 | 684 |

**Cost: 1,376 calls, plus any retries.** At Baidu's listed price for this model
on 2026-10-25, $0.02226 per million prompt tokens and $0.04452 per million
completion tokens:
- **the prompts.** `PLAN_FIRST_MATCH.md`'s passes sent about 1,280 prompt
  tokens a plain prompt, about 2.9 characters a token. At that rate a rule
  prompt runs about 1,830 tokens, and the two passes send about 2.1 million,
  about five cents;
- **the rule arm's answers** ran 109 to 154 tokens in `PLAN_QUEUE_ALONE.md`'s
  smoke run, and the plain arm's under 20, which together is under a cent;
- **the reasoning arm's answers** reasoned 45 to 1,061 tokens in
  `PLAN_FIRST_MATCH.md`'s passes;
- **the reasoning rule arm's answers are not known**, because nothing recorded
  has reasoned before a rule. At the cap of 16,000 tokens on every one of the
  684 reasoning calls of the passes, the two reasoning arms would cost about 49
  cents.

So the run costs under sixty cents at the cap, and under ten at any length the
drafter expects.

**Time.** `PLAN_FIRST_MATCH.md`'s plain asks took about a second, and its
reasoning asks 3.7 to 4 seconds at the median. **The reasoning rule arm's pace
is not known.** At fifteen seconds an ask its 171 asks take about 43 minutes,
and a pass about an hour. **The smoke run measures it before pass 1**, as
`PLAN_FIRST_MATCH.md`'s findings ask of a setting nothing has recorded, and
the findings will say how far this estimate was. **Both passes outlive a
background command of the agent's harness**, so they run in Sergi's terminal,
as `CLAUDE.md` says.

**What is not bought.**
- **The impasse arm with reasoning.** `PLAN_QUEUE_ALONE.md`'s impasse arm split
  the rule-writing prompt's cost into the framing's and the apparatus's.
  Without it, this plan reads the rule-writing prompt as one bundle (§12).
- **The naming question with reasoning on**, `PLAN_FIRST_MATCH.md`'s fourth
  cell.
- **No other level, no screen, no loop.**
- **No other model, provider, manual, effort or budget.**

---

## 2. The choices that have to be made at signature time

Signing §0 adopts the drafter's choice in each unless the signature line says
otherwise. A choice that drops a row is a change to §0, and belongs in the same
signed commit.

### 2.1 The arms — the drafter recommends four

The rule and reasoning rule arms, and the plain and reasoning arms beside them.
The rule arm is asked again so that every row compares arms asked on one day:
`PLAN_SCREEN.md`'s one row argued from continuity across dates was the one
refuted. The plain and reasoning arms are asked again for the same reason, and
they are what lets `RR-d` set the rule-writing prompt's cost with reasoning
beside its cost without.

**The alternatives.**
- **Two arms**, the rule and reasoning rule arms. It drops `RR-d` and saves 684
  calls, about fifteen minutes a pass. `RR-b` and `RR-c` stand as drafted.
- **Three arms**, dropping the plain arm. `RR-d` would need its cost without
  reasoning from `PLAN_QUEUE_ALONE.md`'s record, read across dates, which this
  draft does not offer. It would be redrafted, and that is a change to §0.

### 2.2 The reasoning setting — the drafter recommends `PLAN_FIRST_MATCH.md`'s

**`{"effort": "high"}`, with `max_tokens` 16,000**, imported from
`first_match/plan.py` and not retyped.
- **So the reasoning arm is `PLAN_FIRST_MATCH.md`'s**, prompt for prompt and
  setting for setting, and the reasoning rule arm differs from it in its prompt
  alone.
- **Why 16,000 tokens.** Reasoning tokens count against `max_tokens`, and when
  they spend it the answer comes back empty with `finish_reason: "length"`.
  That is how `PLAN_REUSE.md`'s third smoke run lost five proposals in fifteen
  under 1,200. A rule needs more room after the reasoning than a queue does, and
  `PLAN_FIRST_MATCH.md`'s longest reasoning was 1,061 tokens.
- **The smoke run must show it fits.** Every attempt of both reasoning arms in
  the smoke run reasons and ends `stop` before pass 1 starts (§8).

**The alternative** is `{"effort": "medium"}`, the level OpenRouter documents for
`"enabled": true`. The reasoning arm would then no longer be
`PLAN_FIRST_MATCH.md`'s, and `RR-c` would read beside `FM-e` across a change of
setting.

### 2.3 The population — the drafter recommends level 3's tickets alone

That is 171 prompts an arm, on level 3's 320 decisions: where `FM-e` was read,
and the only level whose list states first match over rules with identifiers.

**The alternative** adds level 2, the prose, to the two rule arms. It would ask
whether reasoning carries where the policy is vague, and it adds 596 calls, 298
of them reasoning. The drafter does not recommend it: level 2's rows would need
their own anchor and their own lines, and no closed plan has asked the prose
with reasoning, so there is nothing to set them beside.

### 2.4 One provider, pinned — the drafter recommends Baidu

**Every request carries OpenRouter's provider routing, with fallbacks off:**
`{"order": ["baidu"], "allow_fallbacks": false}`. That is
`PLAN_QUEUE_ALONE.md`'s pin, imported through `PLAN_FIRST_MATCH.md`'s package
and not retyped. On 2026-10-25 the listing of this model's endpoints named
Baidu's as `baidu/fp8`, served at fp8, with `reasoning`, `reasoning_effort` and
`response_format` among its supported parameters (`PLAN_FIRST_MATCH.md` §2.4).

**Why Baidu.**
- **It served every answer `RR-a` reads**, and every answer of
  `PLAN_FIRST_MATCH.md`'s passes: the pin held in both closed plans.
- **The reasons `PLAN_QUEUE_ALONE.md` gave for one provider stand** (its §2.3):
  two providers part on the answer more often than one parts from itself, and
  interleaving does not match them.

**What the pin costs.** If Baidu does not serve, the request fails rather than
moving. Each failed call is retried twice after a wait, five failed asks in a
row stop a session without recording them, and the same command resumes. The
smoke run must show every attempt served by Baidu before pass 1 starts (§8).

**The alternative** is no pin. Every row would then be read within the provider
that served most answers, and `RR-a` would read across providers.

### 2.5 Two passes, the arms interleaved — the drafter recommends it

Each pass asks every prompt of the four arms once, in one order drawn at
`ORDER_SEED`. So within a pass the arms share the hours.

### 2.6 This question before the loop

`IDEAS.md` puts the cheap half first, and the drafter agrees, for three
reasons:

- **It decides whether the loop is worth its budget.** If `RR-b` is refuted, a
  loop that reasons, asked as v1 asks, would choose its queues no better, and
  its plan would have to change the question before it spent.
- **It prices the loop.** How long the model reasons before a rule, and how
  much room the answer needs after it, is what a loop's budget has to fit, and
  nothing has recorded it.
- **It is a re-ask on one day**, on hundreds of paired decisions, with no screen
  and no loop.

### 2.7 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Every accuracy below is on the corpus, on level 3's decisions, except `G-a`'s,
which is over the space. The other rows are counts of tokens, time and price.
Nothing here is produced by this plan. `RR-g1` recomputes `PLAN_FIRST_MATCH.md`'s rows
and, through its checks, `PLAN_QUEUE_ALONE.md`'s, and checks them against their
records rather than publishing them again.

| figure | value | owning record |
|---|---|---|
| `PLAN_QUEUE_ALONE.md`'s arms at `L₃`, on the 318 decisions every row reads | the rule arm 0.6840, the impasse arm 0.7280, the plain arm 0.7689 | `results_queue_alone/score.json`, published by `FINDINGS_QUEUE_ALONE.md` |
| what the plain question gained, and its two steps | +0.0849 (`QA-b`); 0.0440 from the rule arm to the impasse arm, and 0.0409 from the impasse arm to the plain arm (`QA-d`'s parts) | same |
| the rule arm at `L₃`, on the decisions where its own two answers are valid | 0.6859, on 320 | same, `QA-g` |
| the rule arm's answers at `L₃` in §5.6's classes | 439 first, 139 order and 62 matching, of 640 | same, `QA-g` |
| where the rule arm's order errors go | 133 of 139 to the runner-up's queue, 131 to the second matching rule's | `results_queue_alone/orders.json`, published by `FINDINGS_QUEUE_ALONE.md`, POST-RUN |
| two answers to one rule-arm prompt agreeing, at `L₃` | 0.8969 | `results_queue_alone/score.json`, `QA-g` |
| `PLAN_FIRST_MATCH.md`'s arms at `L₃`, on 320 decisions | the plain arm 0.7422, the naming arm 0.6078, the reasoning arm 1.0000 | `results_first_match/score.json`, published by `FINDINGS_FIRST_MATCH.md` |
| the copier that answers the most specific matching rule's queue | 0.8719, 279 of 320 | `results_queue_alone/sample.json`, Stage A |
| the rules compiled once | 1.0000 of the space (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| the reasoning arm's reasoning | 45 to 1,061 tokens in pass 1, median 349; 49 to 855 in pass 2, median 322; 3.97 and 3.7 seconds an ask at the median | `FINDINGS_FIRST_MATCH.md`, Stage B |
| the pace and the prompts | `PLAN_FIRST_MATCH.md`: 513 asks a pass in 16 to 17.5 minutes, 1.31 million prompt tokens over both passes. `PLAN_QUEUE_ALONE.md`: the rule arm's completions 109 to 154 tokens in its smoke run | `FINDINGS_FIRST_MATCH.md` and `FINDINGS_QUEUE_ALONE.md`, Stage B |
| reasoning by default under the rule prompt | 5 of 15 proposals came back empty or cut off under 1,200 tokens | `PLAN_REUSE.md` §1's amendment, from its third smoke run. Its record keeps no attempt |
| Baidu's listing for the model | `baidu/fp8`; $0.02226 per million prompt tokens and $0.04452 per million completion tokens; up to 131,072 completion tokens | OpenRouter's endpoints listing, read on 2026-10-25 by `PLAN_FIRST_MATCH.md`'s drafter. Not a record of this repository |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and edits no frozen file. Under `harness/` it touches
   only `provenance.py`'s list of code roots, which is plumbing (§10).
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Nothing here is a loop, but the order of a record is
   part of it. The calls are sequential, and the sessions run one after another,
   never side by side.
4. **Seed 17, no regeneration.** Every record under `results_manual/`,
   `results_apply/`, `results_queue_alone/` and `results_first_match/` is
   read-only. `harness/record_guard.py` guards this plan's paid records, and the
   flag that overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema.**
   - The two rule arms' prompts are `PLAN_QUEUE_ALONE.md`'s rule arm's at level
     3, byte for byte.
   - The plain and reasoning arms' prompts are `PLAN_QUEUE_ALONE.md`'s plain
     arm's at level 3, byte for byte, which are `PLAN_FIRST_MATCH.md`'s.
   - The texts are `PLAN_MANUAL.md` §5's, pinned by digest.
6. **If the numbers come out badly, report them.** A model that reasons and
   still writes the wrong queue is a result, and so is one whose reasoning
   changes nothing.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`first_match/`, `queue_alone/`, `apply/`, `manual/`, `fidelity/`, `reuse/`
   and `rung2/` are called by this plan and not edited.**
   - The population is `queue_alone.population.build`'s, at level 3.
   - The rule arms' prompts are `queue_alone.prompts`' rule arm's, and the
     plain arms' its plain arm's. The 29 rules are `queue_alone.rules`'.
   - The model, the temperature, the pin, both reasoning settings and both
     budgets are `first_match.plan`'s.
   - The asker is `first_match.ask.Asker`, with this plan's settings in its
     request, so the retry of §0 is that plan's, called and not copied.
   - The answer is parsed by `rung2.proposers2.parse_payload`, and a rule is
     read by `rung2.engine2.validate_conditions` and `rung2.engine2.Space`.
B. **The loop records are inputs, never outputs, and no label reaches a prompt
   or a row Stage B writes.**
   - **Labels join at scoring.** `y` is copied from the records by Stage C, and
     `tᴬ` from `PLAN_QUEUE_ALONE.md`'s records. The rows Stage B writes carry
     neither.
   - **No module on the proposer's path imports the oracle.** That path is
     `reasoned_rule/prompts.py` and `reasoned_rule/ask.py`. They import by name
     neither the oracle, nor `HIDDEN_DSL`, nor `harness.ceiling_check`, nor
     `rung2.hidden_priority`. Both join `ONLINE_LOOP` and the authority
     channel's watch.
   - **The 29 rules are read from level 3's frozen text**, by `RR-g1`, Stage A
     and Stage C, never on the proposer's path. `RR-g1` holds the text's first
     match to the policy over the space through `rung3.order_search_ls`, a
     module already allowed to see the oracle. The list of such modules does
     not grow.
C. **Every record carries `_env`**, with:
   - the model, the temperature, each arm's reasoning setting and token budget,
     and the provider pin;
   - each arm's system-prompt digest;
   - every attempt's `call_attempts`, and the cause of every retry.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded in full and never
   executed.** That is the rule, its edges and its note, and the reasoning when
   the response carries it. No rule is installed and no edge is tried. Stage C
   reads each rule's conditions against the space for `RR-e`, and no stage
   codes a note or the reasoning.
F. **The order of Stage B is §8's**, and the module refuses a session out of
   it.
G. **The provider is pinned on every call.** An answer served by another
   provider is not an answer of this plan. It is recorded and counted as
   invalid, never read.
H. **A failed call is never answered with v1's retry message.** Only a failed
   parse is (§0).

---

## 5. Known traps

**5.1 — The prompts, and what each pair of arms differs in.** No prompt is new.
- **The rule arm and the reasoning rule arm** send `PLAN_QUEUE_ALONE.md`'s rule
  arm's prompt at level 3: v1 with the manual's block, and v1's empty base
  around the ticket. They differ in the request's reasoning setting and token
  budget, and in nothing else. So `acc_w − acc_t` is reasoning, on the
  rule-writing prompt.
- **The plain arm and the reasoning arm** send `PLAN_QUEUE_ALONE.md`'s plain
  arm's prompt at level 3, and differ in the same two things. So
  `acc_r − acc_q` is reasoning on the plain question, which `FM-d` read.
- **The rule arm and the plain arm** differ as `PLAN_QUEUE_ALONE.md` §5.1 says:
  the impasse framing, and everything v1 says about writing a rule. So
  `acc_q − acc_t` is what asking for a rule costs the queue, read as one
  bundle, and `acc_r − acc_w` is the same with reasoning. `RR-d` is their
  difference.

**5.2 — What each arm writes before its queue.**
- **The rule and plain arms write nothing before it.** v1's answer opens with
  `action`, and the plain arm's answer is nothing else.
- **The two reasoning arms reason before they answer**, outside the answer.
  Then the reasoning rule arm's answer opens with `action`, if the model
  follows v1's template. The record keeps each payload's keys in the order the
  model wrote them, and `RR-e` reports how often `action` came first.

**5.3 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every arm holds
it, and the text states first match. So the rows measure what the model does
with a label it holds. None of them reads level 3 as something the model knew.

**5.4 — The population is level 3's escalations.**
- **They were selected by each run's base**: the tickets no rule covered there,
  or where rules conflicted. They are not the arrivals, and they are harder.
- **Every row compares arms on the same decisions**, so the mix cancels inside a
  row. `acc_w` is not the model's accuracy on the arrivals.

**5.5 — One ticket, several decisions.** A ticket's answers serve every
decision it has, so decisions are not independent draws. That is why the error
is clustered by ticket.

**5.6 — Classify every answer before betting on a mechanism.** That is the
`IDEAS.md` lesson from `blind/cycles.py`, which `PLAN_QUEUE_ALONE.md` §5.6
applied. `RR-e` classifies every answer of every arm against the 29 rules, by
its queue. No row bets on a class.

**5.7 — The rule arms are told the engine could not decide.** v1 calls the
model the system's exception component, says *"El motor simbolico no ha podido
decidir este ticket"*, and calls the ticket *en impasse*. Its user message says
why, if the model reads it so: *"BASE DE REGLAS: vacia. Esta es la primera
regla."* A model that reasons may read the framing as the list failing the
ticket, which is the third candidate, and decide by its own judgement. That is
the drafter's main reason to trust `RR-c` and `RR-d` less.

**5.8 — v1 describes another arbitration than the manual's.** Its section on how
the engine arbitrates describes rung 2's engine: containment first, then
declared priority. The manual states first match. Both are in the rule arms'
prompt and neither is in the plain arms'. They are part of the rule-writing
apparatus, read as one bundle (§5.1).

**5.9 — A rule arm may cite the manual's identifiers.** The loop's proposer
declared priority against them as if they were rules of the base
(`PLAN_MANUAL.md`). Here the base is empty, so `beats` and `loses_to` can name
nothing v1 allows. They are recorded, never tried, and `RR-e` counts the
answers that cite `H01` to `H29`.

**5.10 — A rule read alone is not a rule compiled.** `RR-e` reads each rule
alone over the space, as the first rule of an empty base, which is what v1
tells the model it is. In a loop it would meet the rules born before it, and
what it decides there depends on them. So `RR-e` bounds nothing about a loop,
and no row is drafted on it.
- **A narrower rule is right over its region more easily.** A rule that fixes
  every attribute of its ticket is right on its whole region whenever its queue
  is. So the share of its region a rule gets right is read beside its region's
  size, never alone. That is the lesson that a fill rewards resolving.
- **The region is read against the list's first match**, which `RR-g1` holds to
  the policy over the whole space.

**5.11 — One provider is not the model.** Baidu serves this model at fp8 (§3).
Every figure here is that provider's serving of it.

**5.12 — Reasoning at temperature 0.** The request sends temperature 0 in every
arm. A provider may not honour it while the model reasons, so a reasoning arm's
two answers may part more often than its arm without reasoning. `S` is reported
for each arm.

**5.13 — Two dates, for `RR-a` and for what is set beside.** `tᴬ` is of
2026-10-24. Every row but `RR-a` reads today's arms only. `RR-a` measures the
distance, and cannot undo it. `RR-e` sets the closed plans' arms beside today's,
on two other dates, and adjudicates nothing.

**5.14 — Invalid answers.** As in `PLAN_FIRST_MATCH.md`, with §0's thresholds and
rule G's.
- **A reasoning answer cut off by its budget is invalid.** It comes back empty
  or cut short with `finish_reason: "length"`, and its reasoning tokens are
  still billed. It is a failed parse, so it is retried with v1's message, as v1
  retries one.
- **Every count of a decision left out is published**, with its cause.

**5.15 — The reasoning and the notes are recorded, not read.** The response's
`reasoning` field is kept whole on every reasoning-arm row where it came back,
and every rule arm's payload whole, its note with it. No stage codes either. A
reading of them after the verdicts would need a codebook frozen before the
held-out text is read, which is `PLAN_MANUAL.md`'s lesson from its notes.

**5.16 — Long sessions.**
- **A session that dies keeps what it paid for.** Answers are appended to a
  git-ignored partial file, and the same command resumes there.
- **An outage is not answers.** Five failed asks in a row stop a session
  without recording them.
- **A pass belongs in Sergi's terminal**, because it outlives a background
  command of the agent's harness, and a reasoning ask before a rule is slow.

**5.17 — The queues are listed in one order in every prompt.** The slot decides
some pairwise answers (`PLAN_PRIMACY.md`). Here every arm lists the eight queues
in v1's order and the 29 rules in the manual's, so both orders cancel inside a
row and neither is varied.

**5.18 — Information in front of the model has not changed what it does before,
and reasoning has.** `CHAT_SUMMARY.md` §2.2's erratum: *"With the right
information in front of it, it makes the same mistake"*. With the rules in the
loop's prompt the proposer still partitioned (`G-c`). Reasoning is not new
information, and on the plain question it changed what the model does
(`FM-d`). Both are priors a reader should weigh beside the drafter's
expectation.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**RR-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.
- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_FIRST_MATCH.md`'s checks.** Its `FM-g1` to `FM-g3` pass, called
  through `first_match.gates.run_checks` and not copied. They call
  `PLAN_QUEUE_ALONE.md`'s, which hold the 29 rules to the truth of all 790
  escalations and give back that plan's six verdicts and order reading from its
  passes.
- **Its design.** Rebuilt, it is `results_first_match/sample.json`'s.
- **Its rows.** `first_match.score` gives back `score.json`'s six verdicts from
  its passes.
- **The list's first match over the space.** The 29 rules of level 3's text,
  applied in order to the 134,400 points of the space, give every point the
  queue `rung3.order_search_ls.space_truth_masks` gives it.
- **No float decides a check.** Values are compared as fractions and counts as
  integers, so a record written under 3.12 reads the same under 3.10.

**RR-g2 — The prompts are the closed plans', and the requests are §1's.**
- **The rule arm.** Every prompt is `PLAN_QUEUE_ALONE.md`'s rule arm at level 3,
  digest for digest, and every one of that arm's level-3 prompts is here.
- **The plain arm.** Every prompt is `PLAN_QUEUE_ALONE.md`'s plain arm at level
  3, digest for digest, and `PLAN_FIRST_MATCH.md`'s plain and reasoning arms
  carry the same digests.
- **The reasoning arms.** Every reasoning rule arm prompt is the rule arm's on
  the same ticket, text for text, and every reasoning arm prompt the plain
  arm's.
- **The texts.** The two rule arms send the rule prompt, which asks for a rule's
  conditions and edges, under v1's empty base; the other two send the plain
  prompt. Every arm's system prompt holds the 29 identifiers of level 3's list.
- **The requests.** They are checked through `tests/doubles.py`'s SDK double in
  the package's tests, which `RR-g1`'s suite runs:
  - the rule arm's request is `PLAN_QUEUE_ALONE.md`'s rule arm's, the
    proposer's own with the pin;
  - the plain and reasoning arms' are `PLAN_FIRST_MATCH.md`'s plain and
    reasoning arms';
  - the reasoning rule arm's is the rule arm's with the reasoning arm's setting
    and budget, and nothing else changed.

  A failed call is retried with the same messages, and a failed parse with v1's
  retry message.
- **No builder takes a record's row.**
- **Teeth.** One changed character moves a prompt's digest, and no digest stands
  for two texts. The 684 prompts carry 342 texts, since each reasoning arm
  shares its texts with the arm it reasons for.

**RR-g3 — The population and the schedule are §0's and §1's.**
- **The prompts.** There are 171 an arm, on level 3's 320 decisions, and each
  decision is served once in every arm.
- **The passes.** Each holds every prompt of the four arms once, 684, in its
  order rebuilt from `ORDER_SEED`. The two orders differ.
- **The smoke.** Its eight prompts are two of each arm, distinct, drawn from
  those by `ORDER_SEED`.

**RR-g4 — The signature**, §10.

---

## 7. Stage A — the design and the references (free, gated)

**Deliverable.** `reasoned_rule/sample.py` → `results_reasoned_rule/sample.json`.

- **`RR-g1` to `RR-g3`.**
- **The design.** Every prompt, with its arm, ticket, digest and the decisions it
  serves, the three sessions' orders at `ORDER_SEED`, each arm's system prompt
  and each arm's settings.
- **The references, computed after the signature.**
  - For every decision: the identifiers of the rules its ticket matches, in
    order, and its runner-up.
  - `tᴬ` for every rule prompt, with the provider that served it.

**It produces nothing adjudicable.** It runs after §0 is signed, so that none of
its figures can inform a band.

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `reasoned_rule/ask.py` → `results_reasoned_rule/ask_smoke.json`,
`ask_pass1.json` and `ask_pass2.json`. **Three sessions, in that order, one
after another. Each record is committed before the next session starts.**

**Every session, before any call**, follows `PLAN_FIRST_MATCH.md` §8's order:

1. **`--dry-run`** runs `RR-g1` to `RR-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`RR-g4`).** While `PLAN_REASONED_RULE.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.** A pass needs the smoke record under this protocol,
   with:
   - a valid answer from each arm, and every attempt served by the pinned
     provider;
   - every attempt of both reasoning arms reasoned, by its reasoning tokens or
     its reasoning, and ended `stop`;
   - no attempt of the rule or plain arms reasoned.

   Pass 2 also needs pass 1's record. If the smoke run fails, the passes do
   not start, and what would change is a signed amendment.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`RR-g1` to `RR-g3`, blocking.** Stage A's record must hold the same design
   and digests.
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls.** They are sequential, with each arm's reasoning
   setting and the pin on every one.

**What each record carries, per call:**
- **Which call**: the session, the pass and the position.
- **What was asked**: the prompt's id, arm and digest. Stage A's record says
  which decisions each prompt serves.
- **The answer**: its `action`, its whole payload with its keys in the order
  written, and the reasoning when the response carries it. Or the failure.
- **The attempts**: every attempt's `call_attempts`, provider, finish reasons
  and tokens included, and the cause of every retry.
- **When**: the seconds and the time.
- **No label.** Stage C joins `y` and `tᴬ` (rule B).

## 9. Stage C — scoring, and the four adjudications (free)

**Deliverable.** `reasoned_rule/score.py` → `results_reasoned_rule/score.json`,
and `results_reasoned_rule/FINDINGS_REASONED_RULE.md`, which owns every figure.

- **`RR-a` to `RR-d`**, each against its line, exactly, with its clustered
  standard error, *thin* and *unadjudicable* as §0 defines them.
- **Each row's parts and per-run values**, never summed into the verdict.
- **`RR-e` in full**, the rules written included.
- **The run itself**: failed calls, invalid actions, answers from another
  provider, retries by cause, reasoning tokens, and the pace per session and
  per arm.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `reasoned_rule/sample.py` and `reasoned_rule/score.py` spend
nothing. `reasoned_rule/ask.py` refuses before it constructs a client. **The
free stages get the gate because what it protects is the order of events, not
money.** A record of this plan written before the signature would be a figure
that existed before its band.

**The gate reads `PLAN_REASONED_RULE.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.**
  - `MODEL`, `PROMPT`, `TEMPERATURE`, `PROVIDER` and `PROVIDER_NAME` are
    imported from `first_match.plan`, which takes them from `queue_alone.plan`.
  - `REASONING_OFF`, `{"effort": "none"}`, and `MAX_TOKENS = 1200` are
    `first_match.plan`'s, the rule and plain arms' own.
  - `REASONING_ON`, `{"effort": "high"}`, and `MAX_TOKENS_REASONING = 16000`
    are `first_match.plan`'s, its reasoning arm's.
  - `MAX_RETRIES = 2`, and `CALL_RETRY_WAIT = (10, 30)` seconds before a failed
    call's two retries, `first_match.plan`'s.
  - `settings(arm)` gives each arm's reasoning setting and token budget, the
    two things its request carries that another arm's may not.
- **The inputs.** `queue_alone.population.build` and the closed plans' paths,
  imported and not retyped.
- **The arms.** `ARMS = ("t", "w", "q", "r")`: the rule, reasoning rule, plain
  and reasoning arms. `REASONING_ARMS = ("w", "r")` and `QUIET_ARMS = ("t", "q")`
  say which of them reason.
- **The population.**
  - `LEVEL = 3`.
  - `TICKET_PROMPTS = 171` and `DECISIONS = 320`.
- **The sessions.**
  - `SESSIONS = ("smoke", "pass1", "pass2")`.
  - `PASSES = 2`.
  - `SMOKE_PER_ARM = 2`.
- **The seed.** `ORDER_SEED = 79`.
  - **It is new.** It is distinct from every seed a closed thread uses: 17 to
    20, 25, 41, 43, 47, 53, 59, 61, 67, 71 and 73, and values from 1000 up.
  - **It feeds three streams**, one string seed per session.
  - **It is hash-free.** CPython seeds a string through SHA-512, so no order
    depends on `PYTHONHASHSEED`.
- **The limits.**
  - `MIN_SIGNATURES = 1` and `MAX_CONSECUTIVE_FAILURES = 5`.
  - `MAX_INVALID_SHARE = Fraction(1, 20)` and `MIN_ANCHOR_PROMPTS = 100`.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `RR_A_MAX_GAP = Fraction(1, 20)`.
  - `RR_B_LINE = 0`, held above.
  - `RR_C_LINE = Fraction(9, 10)`.
  - `RR_D_LINE = 0`, held below.

**The names.**
- **The package is `reasoned_rule/`.** No module of the standard library has
  that name.
- **The rows are `RR-a` to `RR-e`, with two letters.** Every single capital
  already names a thread, and `tests/test_prose_tables.py` reads one or two
  since `PLAN_QUEUE_ALONE.md`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
reasoned_rule/__init__.py
reasoned_rule/plan.py        the gate and the constants of §10
reasoned_rule/prompts.py     the four arms' prompts                     [proposer's path]
reasoned_rule/population.py  the prompts and the sessions, on PLAN_QUEUE_ALONE.md's level-3 prompts
reasoned_rule/gates.py       RR-g1 to RR-g4
reasoned_rule/sample.py      Stage A
reasoned_rule/ask.py         Stage B: it spends                         [proposer's path]
reasoned_rule/shape.py       the rules written, read against the 29 rules over the space
reasoned_rule/score.py       Stage C
results_reasoned_rule/FINDINGS_REASONED_RULE.md
results_reasoned_rule/sample.json  ask_smoke.json  ask_pass1.json  ask_pass2.json  score.json
tests/test_reasoned_rule.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `reasoned_rule` joins it in `harness/provenance.py`, and
  joins the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The two modules marked above
  join both, with rule B's comment. Every arm's system prompt carries the
  manual's block, so they send the manual's texts, as `first_match/prompts.py`
  and `first_match/ask.py` do.
- **The partial files**, `results_reasoned_rule/*.partial.jsonl`, join
  `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site.** `reasoned_rule/ask.py` sends its requests through
  `first_match/ask.py`'s asker, which is already a classified call site and
  carries the call recorder. It makes no call of its own, so
  `tests/test_call_record.py`'s list of call sites does not grow. Every row
  still keeps its `call_attempts`.
- **The README's table of writers** gains its rows, and its table of tests.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_reasoned_rule/` with `_env`, the model, the
      temperature, each arm's reasoning setting and token budget, the provider
      pin, the system prompts' digests and `call_attempts`, produced with
      `PYTHONHASHSEED=0`.
- [ ] `RR-g1` to `RR-g4` passed before any record was written. The key check
      and the smoke run came before the first pass, and each session's record
      was committed before the next began.
- [ ] Every attempt of the smoke run was served by the pinned provider, every
      attempt of both reasoning arms reasoned and ended `stop`, and no attempt
      of the other two reasoned, before pass 1 began.
- [ ] The plumbing of §10, and tests pinning:
      - the constants and the gate;
      - the four arms' prompts against the closed plans' digests;
      - the requests in every arm, the pin and the reasoning settings included;
      - the retry by cause;
      - the reading of the rules written, on rules and tickets built by hand;
      - the exactness of §0's comparisons, `RR-d`'s condition for having no
        value, and the clustered error.
      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface (the corpus, except `RR-e`'s
      reading of the rules over the space), its arm, its denominator, and the
      date of each side it compares.
- [ ] `results_reasoned_rule/FINDINGS_REASONED_RULE.md` owns every figure, with
      a dated erratum wherever it corrects something already published. That
      includes this plan's §0 *already seen*, if Stage A does not reproduce it,
      and §1's estimates of the reasoning rule arm's pace and cost.
- [ ] `STATUS.md`: the scoreboard gains the `RR` thread. *What is open* narrows
      its second item by what this plan settles.
- [ ] `IDEAS.md`: *The loop with reasoning on* is narrowed, with what this plan
      opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `RR`, and its `TABLES`
      gains `FINDINGS_REASONED_RULE.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits; the plan and its
      signature are alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **The loop.** What a loop that reasons compiles is not read here. `RR-e`
   reads the rules written one at a time, as first rules of an empty base, and
   a loop is a plan of its own, under a budget this plan measures.
2. **Which part of the rule-writing prompt reasoning reaches.** Without the
   impasse arm, the framing and the apparatus are read as one bundle (§1).
3. **The naming question with reasoning on**, `PLAN_FIRST_MATCH.md`'s fourth
   cell.
4. **The screen with reasoning on.** `PLAN_SCREEN.md` and `PLAN_APPLY.md`
   measured deference with reasoning off. Nothing here shows a screen.
5. **The other levels.** Nothing here asks the prose or the names with
   reasoning (§2.3).
6. **Another effort, another budget, another model.** One reasoning setting is
   bought (§2.2).
7. **The arrivals.** Every figure is about escalated tickets, which are the
   hard ones.
8. **One model, one provider, one manual, two passes, one day.**
