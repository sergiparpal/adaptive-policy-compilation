# PLAN_FIRST_MATCH — the first match: which rule the model believes applies, and whether reasoning finds it

**Status: drafted by Claude on 2026-10-25, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**Asked for by Sergi on 2026-10-25**, after `PLAN_QUEUE_ALONE.md` closed and its
order errors were read POST-RUN.

**The item.** `PLAN_QUEUE_ALONE.md` asked `PLAN_APPLY.md`'s escalated tickets
again, with the manual in the prompt and no screen, and asked for the queue
alone.

- **Asked plainly, the model still misses one escalated decision in four.** At
  level 3, with the 29 rules in its prompt, it is right on 0.7689 of the
  decisions (`QA-b` holds), short of §0's 0.90 (`QA-e` refuted).
- **What it misses is the list's order.** Of the plain arm's 638 answers at
  level 3, 141 name the queue of a rule the ticket matches lower in the list,
  and 6 a queue no matching rule gives
  ([`FINDINGS_QUEUE_ALONE.md`](results_queue_alone/FINDINGS_QUEUE_ALONE.md),
  *What the model still gets wrong*).
- **Read POST-RUN, the order errors are the next rule.** 134 of those 141 name
  the queue of the second rule the ticket matches, and 135 the runner-up's.
  Every arm sends them there alike. They are neither the catch-all nor the more
  specific rule (*Where the order errors go*).

That reading left the question for this plan:

> *Why the model takes the next rule. Whether it misreads the first rule's
> conditions, or reads the exception as covered by the general rule below it,
> these answers cannot say. A question for the rule that applies would show
> which rule the model believes it is applying.*

[`IDEAS.md`](IDEAS.md) carries it first under *What `PLAN_QUEUE_ALONE.md`
opens*, with the two questions that would narrow it: a question for the rule
that applies, and the plain question with reasoning on.
[`STATUS.md`](STATUS.md)'s *What is open* reaches it at the end of its second
item: *why the model passes over the first rule*.

**Three candidates, each with a reason on record.**

- **It does not find the first match.** It reads the first rule's conditions
  as unmet, or the exception as covered by the general rule after it, and
  believes a lower rule is the one that applies.
  - At three pairs the list puts an exception directly above its general rule:
    `H02` above `H03`, `H15` above `H16` and `H17` above `H18`. Each exception
    adds *severity lte 2* to the general rule's conditions.
  - Under those three the plain arm makes 29 order errors on 36 answers, 12 on
    36 and 13 on 28, and there the next rule is the general one.
- **It finds the first match and names another queue.** The queue it writes is
  pulled from the rule it found toward one the ticket also matches.
- **It does not think it through.** First match over 29 rules is a walk down
  the list. With reasoning off the queue is the first and only thing the model
  writes (`PLAN_QUEUE_ALONE.md` §5.2), so nothing it writes walks the list
  before it names the queue. `PLAN_QUEUE_ALONE.md` §12 left reasoning as its
  third item.

**The question, in its cleanest form.** At the escalations of `PLAN_MANUAL.md`'s
loop, with the 29 rules in the prompt and no screen:
- asked to name the rule that applies before its queue, which rule does the
  model name where it gives a lower rule's queue: the first, or a lower one?
- does naming the rule first make it right more often?
- with reasoning on, does it apply the list nearly exactly?

**Nothing has to be re-run but the model.** `PLAN_QUEUE_ALONE.md`'s design holds
the population. `queue_alone/population.py` rebuilds it from `PLAN_APPLY.md`'s,
which rebuilds it from the twelve loop records.

Three arms are bought, all on the day this plan runs and all under one
provider. Every prompt is asked twice.
- **The plain arm, `q`.** This is `PLAN_QUEUE_ALONE.md`'s plain arm at level 3,
  its prompts byte for byte. It is asked again so that every row compares arms
  asked on one day.
- **The naming arm, `n`.** The same prompt, with one line added to the answer:
  the identifier of the rule that applies, asked before the queue.
- **The reasoning arm, `r`.** The plain arm's prompt byte for byte, with
  reasoning on.

Every arm is asked at level 3 only, on level 3's escalated tickets. Only level 3
hands the model a list whose rules carry identifiers.

**What it changes in what is measured, said first.**
- **It installs nothing.** No rule is born, no base grows, and no figure here
  continues a loop's.
- **It reads one axis.** That is the acting axis of `CLAUDE.md` Step 5: the
  queue named for the ticket in front of the model. The naming arm adds the
  rule the model says applies, read beside its queue.
- **One prompt is new, and one setting.** Hard rule 5 forbids adjusting a prompt
  before a result is recorded. The naming arm's prompt is not an adjustment of
  the plain arm's: it is a new question, frozen verbatim in §5.1 and signed with
  §0. The reasoning arm changes no prompt, only the request's reasoning
  setting and its token budget (§1).
- **The proposer's calls have had reasoning off since `PLAN_REUSE.md` §1's
  amendment**, signed on 2026-09-30. Nothing here moves that setting for any
  other plan. The reasoning arm is a question to the same model, not a change
  to the instrument the closed threads read.

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
  tickets that arrived and that the loop could not decide.
- **The decisions and the tickets are `PLAN_QUEUE_ALONE.md`'s at level 3**, as
  its §0 counts them:

| level | decisions | distinct tickets | ticket prompts asked, per arm |
|---|---|---|---|
| `L₃`, the rules | 320 | 171 | 171 |

- **A decision is an escalation whose screen is not empty**, as in
  `PLAN_APPLY.md` and `PLAN_QUEUE_ALONE.md`. No screen is shown here. The rows
  read decisions, so that `acc_q` here is the statistic `QA-b`'s 0.7689 was. A
  ticket weighs as many times as the loop escalated it with a screen.
- **The rows read by ticket instead are reported** in `FM-g`.

**The arms and the notation**, per decision.

- **`y`** is the true queue: the record row's `truth`.
- **`m₁, m₂, …`** are the rules of level 3's frozen text that the ticket
  matches, in the list's order. `m₁`'s queue is `y`, which `FM-g1` checks on
  every decision. **The runner-up** is the first matching rule whose queue is
  not `y`.
- **`q₁` and `q₂`** are the plain arm's two answers on the decision's ticket, in
  pass 1 and pass 2. A ticket that serves several decisions lends both to each.
- **`n₁` and `n₂`** are the naming arm's queues, and **`ρ₁` and `ρ₂`** the
  rules it names with them. **`r₁` and `r₂`** are the reasoning arm's answers.
- **`qᴬ`** is `PLAN_QUEUE_ALONE.md`'s plain-arm answer on the same prompt, given
  on 2026-10-24, one per pass.
- **`q̄`** is `½(1[q₁=y] + 1[q₂=y])`, and `n̄` and `r̄` are defined likewise.
  `acc_q`, `acc_n` and `acc_r` are their means over a row's decisions.
- **An answer is *valid*** when its `action` is one of the eight queues and the
  provider that served it is the one pinned (§2.4). For the naming arm that
  holds whether or not it names a rule. **A decision enters a row only with
  every answer that row reads valid.**
- **A naming-arm answer *names a rule*** when its `rule` field, stripped of
  surrounding spaces, begins with one of the 29 identifiers `H01` to `H29` and
  no digit follows it. `ρ` is that identifier. Any other field names no rule.

**The classes.**
- **An answer's class** is `PLAN_QUEUE_ALONE.md` §5.6's, by its queue:
  - *first*, the queue of `m₁`, which is `y`;
  - *order*, another queue, given by a lower matching rule;
  - *matching*, a queue no matching rule gives.
- **A named rule's class**, for a naming-arm answer that names a rule:
  - *the first*, when `ρ` is `m₁`;
  - *a lower match*, when `ρ` is a lower matching rule;
  - *unmatched*, when the ticket does not match `ρ`.

**The unit, the error and *thin*.** All of it is settled here and not in the
scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict. It is
`PLAN_QUEUE_ALONE.md`'s, unchanged, with one addition for `FM-c`.

- **Every row is pooled over level 3's three runs**, decision by decision. The
  run is not the unit: the question is about the model's answer to a prompt,
  and the runs are unequal.
- **Each run's value is published beside the pooled one**, and adjudicates
  nothing.
- **`FM-c` reads answers, not decisions.** It reads the naming arm's answers at
  level 3's decisions, two per decision, and its statistic is a ratio of their
  counts.
- **Every statistic is a ratio of integer counts.** **It is compared with its
  line exactly, as a fraction.** No rounding enters a verdict.
- **The standard error is clustered by ticket**, with `PLAN_APPLY.md`'s formula.
  Decisions on one ticket share its answers.
  - **The formula.** Let a row hold `n` terms on `C` tickets, with `d` a term
    and `d̄` their mean. The variance of the mean is
    `C/(C−1) · Σ over tickets of (Σ over its terms of (d − d̄))² / n²`.
  - **For `FM-c` a term is one answer**, 1 if it names a lower match and 0
    otherwise, so its error is that of a mean over answers.
  - **It is a label.** It is a float, and it marks *thin* and never decides.
- **A verdict is labelled *thin*** in either of two cases, and the label does
  not change the verdict:
  - the statistic lies within one standard error of its line;
  - dropping any one run's decisions would put it on the other side.

  `FM-a` reads prompts and not runs, so only the first case applies to it.

**When a row has no value.**
- **A row has none** if more than 5% of its decisions lack the valid answers it
  reads.
- **`FM-a` reads prompts, not decisions.** It has none if fewer than 100 prompts
  hold today's two answers valid and a valid answer of `PLAN_QUEUE_ALONE.md`'s
  from the pinned provider.
- **`FM-c` also has none** in either of two cases:
  - fewer than 20 of the naming arm's order errors name a rule;
  - more than 5% of the naming arm's valid answers at level 3's decisions name
    no rule.

A row with no value is unadjudicable, and the record says so.

**Which side had the label**, for every arm. This was checked against the
prompts while drafting, and not recalled, as `CLAUDE.md` asks of any plan that
sets a comparison on the proposer:

| arm | what it is handed | reads a label? |
|---|---|---|
| all three | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."* | **yes**: every ticket's label is derivable from the text by first match |
| `qᴬ` | the plain arm's prompt, on 2026-10-24 | as the plain arm |

- **The three arms hold the same manual.** No row sets a side that has the
  label against one that has not.
- **No arm sees an example**, and nothing here is fitted, so nothing reaches a
  test split.
- **No baseline is set against the proposer.** All three are questions to the
  same model. The plain arm is `PLAN_QUEUE_ALONE.md`'s, the naming arm adds one
  field to its answer, and the reasoning arm asks it with reasoning on.

**The retry, settled here.** `PLAN_QUEUE_ALONE.md`'s asker retried any failed
attempt with v1's retry message, which tells the model its answer was not
valid JSON. After an upstream 429 there was no answer, and eight answers were
given with that message in the conversation. **Here a failed call is retried
with the same messages, after a wait, and only a failed parse is retried with
v1's message.** Every row says which retries it took.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **FM-a** | **The plain arm has not moved since `PLAN_QUEUE_ALONE.md` asked it.** Re-asked under the same provider, it agrees with that plan's answers about as often as it agrees with itself | over level 3's plain prompts that hold today's two answers valid and a valid answer of `PLAN_QUEUE_ALONE.md`'s from the pinned provider: `S − A`. `S` is the share whose two answers today agree. `A` is the mean, over today's two answers and that plan's answers, of their agreement | **≤ 0.05** | **> 0.05** |
| **FM-b** | **Asked to name the rule that applies before its queue, the model is right more often** than when it is asked for the queue alone | over `L₃`'s decisions: `acc_n − acc_q` | **> 0** | **≤ 0** |
| **FM-c** | **Where it gives a lower rule's queue, the model names a lower rule.** It believes a lower rule applies; it does not find the first match and name another queue | over the naming arm's answers at `L₃`'s decisions that are order errors and name a rule: the share whose named rule is a lower match. It is compared with its line as `2·lower − named` against 0, which is the same comparison | **≥ 1/2** | **< 1/2** |
| **FM-d** | **With reasoning on, the model is right more often** than asked the same question without it | over `L₃`'s decisions: `acc_r − acc_q` | **> 0** | **≤ 0** |
| **FM-e** | **With reasoning on, the model applies the 29 rules nearly as exactly as it transcribes them** | over `L₃`'s decisions: `acc_r` | **≥ 0.90** | **< 0.90** |
| **FM-f** | **Reasoning buys more than naming the rule.** With reasoning on, the model is right more often than when it names the rule first without it | over `L₃`'s decisions: `acc_r − acc_n` | **> 0** | **≤ 0** |
| **FM-g** | *Reported, not adjudicated.* **What the drafter could not band** | Each arm's accuracy, with its runs, and by ticket instead of by decision. Every answer of every arm in §5.6's classes, and each arm's order errors by where they go: the next matching rule, the runner-up, the catch-all, the most specific rule. The naming arm's named rules in their classes, over all its answers and over its order errors; how often its queue is the named rule's; how often a lower name is the next matching rule. On the decisions where today's plain arm makes an order error, what the naming arm names on the same ticket. Each arm's accuracy by the rule that governs the ticket. The table by true queue, with `ONCALL_ESCALATION`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER` and `T3_ENGINEERING` in counts. `S` for each arm, and how often the arms agree with each other. `PLAN_QUEUE_ALONE.md`'s plain arm beside today's on the same decisions. Each arm's providers, finish reasons, tokens, reasoning tokens, seconds and retries by cause. The reasoning arm's reasoning, recorded in full and not coded | — | — |

**Signed by Sergi: ____________________ (date: __________)**

**Why each row, and why these lines.**

- **`FM-a` is the instrument row.** Its line is `X-a`'s, `F-a`'s, `V-a`'s and
  `QA-a`'s.
  - **It reads the plain arm's prompts**, because that arm is asked byte for
    byte as `PLAN_QUEUE_ALONE.md` asked it, under the same pin.
  - It says how far today's plain arm stands for that plan's, so that the
    reading of where its order errors go can be set beside today's arms. It
    cannot undo the distance.
- **`FM-b` reads what naming the rule does to the queue.** Its line is the
  literal *more often*.
- **`FM-c` separates the first two candidates.** *Most* is read as at least
  half, so that a tie goes to the claim, as in `QA-c`.
  - **It reads the naming arm's own order errors.** Naming the rule changes the
    prompt, so the naming arm's errors are not the plain arm's. What the naming
    arm names on the plain arm's errors is reported in `FM-g`.
  - **Its denominator is the order errors that name a rule.** An answer that
    names none says nothing about which rule the model believes applies, and
    §0's second condition keeps such answers from being many.
- **`FM-d` reads what reasoning does to the queue.** Its line is the literal
  *more often*.
- **`FM-e` is the application with reasoning, read against compiling.**
  Compiled once, the same model writes the 29 rules exactly (`G-a`). The line
  is `QA-e`'s, a tenth below exact, so `FM-e` reads directly beside `QA-e`'s
  refutation.
- **`FM-f` sets the two routes against each other.** If naming the rule bought
  as much as reasoning, what the plain arm misses would be one explicit step,
  not a walk down the list.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`STATUS.md`**: its opening notes, its scoreboard's convention and its
  table, *What was withdrawn*, *What is open* with every dated note in it, and
  *What this does not show*.
- **`IDEAS.md`**: its header, *Pending and already specified*, the sections on
  `PLAN_QUEUE_ALONE.md`, `PLAN_APPLY.md` and `PLAN_MANUAL.md`, the deferral
  items under `PLAN_STUDENTS.md`, the second half of *What the outside reading
  of October 2026 proposes*, *Technical debt*, and the standing note on who
  drafts these.
- **The queue-alone thread.** `PLAN_QUEUE_ALONE.md` and
  `FINDINGS_QUEUE_ALONE.md`, whole, with every figure they publish:
  - the six verdicts, with their parts and runs;
  - `QA-g`'s tables by level, by true queue, by §5.6's classes, and its
    agreement figures;
  - *Where the order errors go*, POST-RUN: where each arm's order errors go,
    the rules passed over and followed, and its five clauses.

  **The JSON records of that thread were not read for figures.** The package's
  checks read `sample.json`, both passes, `score.json` and `orders.json`, to
  recompute what they hold and compare it, and print only whether each
  comparison passes. Writing the order check, the drafter listed `orders.json`'s
  keys.
- **`PLAN_REUSE.md` §1's amendment**, which turned reasoning off: the default
  reasoned 20 tokens on a six-token reply, and `{"effort": "none"}` none.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  They were not read whole for this plan. The passages it rests on were read
  directly:
  - `ARBITRATION_REPORT.md` §5, its diagnosis, and §9, its limits;
  - `CHAT_SUMMARY.md`'s header list of errata, and §2.2's erratum of
    2026-08-12, as `PLAN_PAIRWISE.md` §4's rule C asks;
  - `EXTERNAL_REVIEW.md` §5.
- **The code the package calls.** `queue_alone/`'s `plan.py`, `prompts.py`,
  `population.py`, `rules.py`, `gates.py`, `ask.py`, `sample.py`, `score.py`
  and the functions of `orders.py`, and `tests/test_queue_alone.py`;
  `apply/score.py`'s helpers; `harness/call_record.py`;
  `rung2.proposers2.parse_payload`; the constants of `manual/plan.py` and
  `reuse/plan.py`; `tests/doubles.py`.
- **The manual's level-3 text**, `manual/texts/rules.txt`, whole: the 29 rules
  and the first-match sentence.
- **OpenRouter.** Its listing of this model's endpoints and its documentation
  of reasoning tokens, both read on 2026-10-25 (§2.2, §3).
- **Counts computed while drafting.** None of them reads a label or an answer.
  - **The naming arm's prompt.** Rendered at level 3 from §5.1's text, its
    system prompt runs 3,545 characters against the plain arm's 3,476. The two
    differ by one added line of 69 characters, inside the answer's template,
    and by nothing else. The user messages are the same.
  - **No prompt in the tree asks for the rule that applies.** The tree's
    prompts ask for a rule to write, a whole base, a ranking of the queues, the
    winner between two rules, or a queue.
  - **No recorded attempt reasoned.** Of the 7,854 attempt entries under
    `results*/` that carry a `reasoning_tokens` field, all of them recorded
    since 2026-10-16, none is above 0.
  - **The design, as the package builds it.** 171 prompts an arm, every one of
    level 3's 320 decisions served once in each arm, and 342 distinct texts
    behind the 513 prompts, since the plain and reasoning arms share theirs.

**Not seen, because nothing has produced it:**

- any answer to a question that asks for the rule that applies;
- any answer of this model given with reasoning on and recorded with its
  attempts, and any reasoning it wrote. `PLAN_REUSE.md`'s third smoke run
  reasoned by default, and its record keeps neither;
- which identifiers the loop records' declarations and the rule arm's notes
  cite. Both cite the manual's identifiers in places (`IDEAS.md`), and neither
  was read for this plan.

Stage A computes, after the signature, which rules match each decision's ticket
and which is its runner-up. `PLAN_QUEUE_ALONE.md`'s Stage A published their
counts, which the drafter has seen.

**What the drafter expects, written down so the scoreboard can score it.**
**All six hold: `FM-a`, `FM-b`, `FM-c`, `FM-d`, `FM-e` and `FM-f`.** The
drafter trusts `FM-a` most, then `FM-d`, `FM-c`, `FM-f` and `FM-e`, and `FM-b`
least.

- **`FM-a` holds.** One provider answers both sides, and `QA-a` held by
  +0.0062. At level 3 the plain arm's two answers agreed 0.9591 of the time.
  Against it:
  - the retry protocol changed, though only after a failed call;
  - this is an argument for continuity, and the standing note in `IDEAS.md`
    says those are the drafter's arguments that lose.
- **`FM-d` holds.** Reasoning gives the model the walk down the list that a
  queue written as its first token cannot take. Against it: the model reasons
  at temperature 0 on one provider's fp8 serving, and a reasoning model can
  argue its way to the queue its prior favours.
- **`FM-c` holds.** The order errors go to the next rule in nearly every case,
  and every arm sends them there alike, 0.9568 and 0.9574 for the rule and plain
  arms. That reads like a stable belief about which rule applies, not a slip in
  naming the queue of the rule the model found. Against it: the identifier
  comes first, and a model that names the first rule could still drift to
  another queue in the next field.
- **`FM-f` holds.** If `FM-c` holds, naming the rule cannot move a belief about
  which rule applies, and reasoning can.
- **`FM-e` holds, and the drafter trusts it less.** A model that walks 29 rules
  in order against eight attributes should find the first match on nine
  tickets in ten. Against it:
  - **these are the hard tickets**, the ones the loop could not decide;
  - **the three pairs turn on *severity lte 2***, where severity 1 is the most
    critical. A model that reads that condition wrong reads it wrong whether or
    not it reasons;
  - **a truncated answer is invalid.** If reasoning spends the budget on more
    than a twentieth of the decisions, the row has no value rather than a
    verdict;
  - **the line is above a copier that reads no order.** The copier that answers
    the queue of the matching rule with the most conditions is right on 0.8719
    of these decisions.

  The drafter's guess is that the reasoning arm lands near 0.95.
- **`FM-b` holds, and the drafter trusts it least.** Writing the identifier
  first is one step of deliberation, and it ties the queue to a line of the
  list. Against it: if `FM-c` holds, the model names the rule it believes
  applies and writes its queue, and the gain may be nil. Taking the
  rule-writing apparatus away gained the queue 0.0440 (`QA-d`'s parts), so a
  field added to the answer can also cost. The drafter's guess is that the
  naming arm lands near 0.80.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 49 of 117 adjudicated rows were refuted.
- **The last plan.** `PLAN_QUEUE_ALONE.md`'s drafter got five of six, and missed
  the row it trusted least.
- **What was done about it, rather than said.**
  - No band here was set on a development set.
  - Every line is the claim's own edge, or a closed thread's: `FM-a`'s is
    `QA-a`'s, `FM-c`'s half is `QA-c`'s, and `FM-e`'s is `QA-e`'s.
  - A verdict a single run carries is labelled *thin* in advance.

**How the rows read together.**

- **`FM-c` holds.** Made to name the rule, the model names a lower one where it
  gives a lower rule's queue: it does not find the first match. `FM-b` then
  says whether naming the rule moves that, and `FM-d` and `FM-e` whether
  thinking it through does.
- **`FM-c` is refuted.** The model names the first rule and writes another
  queue on most of its order errors: the error is in naming the queue of the
  rule it found. `FM-b` then says whether naming it first recovers part.
- **`FM-d` and `FM-e` hold.** Thinking it through finds the first match, so the
  plain arm's errors are what this model does with a 29-rule list when it does
  not reason. `FM-f` says whether the naming arm already bought part of that.
- **`FM-d` holds and `FM-e` is refuted.** Reasoning helps and leaves more than
  a tenth wrong. Part of the error survives deliberation, and the reasoning the
  record keeps says what the model did, for a reading after the verdicts.
- **`FM-d` is refuted.** The plain arm's errors are not a matter of thinking it
  through.
- **`FM-a` is refuted.** `FM-b` to `FM-f` are still adjudicated as signed. They
  then describe today's model under one provider, and `FM-a`'s gap stands
  beside each. `PLAN_QUEUE_ALONE.md`'s order reading is then a fact about that
  day's answers.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, hard rule 4:
- **`results_manual/loop_L3_r{1..3}.json`**, `PLAN_MANUAL.md`'s three level-3
  loop runs: the escalations, their tickets and the truth. The nine other runs
  are read by `PLAN_APPLY.md`'s and `PLAN_QUEUE_ALONE.md`'s checks, which
  `FM-g1` calls.
- **`results_queue_alone/sample.json`**: `PLAN_QUEUE_ALONE.md`'s design, every
  prompt's digest and the system prompts.
- **`results_queue_alone/ask_pass1.json` and `ask_pass2.json`**: `qᴬ`, for
  `FM-a`, with the provider of every answer.
- **`results_queue_alone/score.json` and `orders.json`**: §3's references.

**Bought: the model's answers with level 3's manual, every call pinned to one
provider.** All three arms go through the package's asker, through
`harness/call_record.py`. Every request sends:
- the model, temperature 0, and `response_format` on the first attempt;
- the provider pin of §2.4;
- **in the plain and naming arms**, reasoning off, `{"effort": "none"}`, and
  1,200 tokens, as `PLAN_QUEUE_ALONE.md`'s plain arm did;
- **in the reasoning arm**, reasoning `{"effort": "high"}` and 16,000 tokens
  (§2.2).

**Two retries, and which one is settled here (§0).**
- **A failed call**, one that raised before any answer came back, is retried
  with the same messages, after 10 seconds and then 30.
- **A failed parse**, an answer that came back and is not a JSON object, is
  retried with v1's retry message, as v1 does.
- **The record keeps the cause of every retry.**

Three sessions, sequential, in this order:

| session | what is asked | prompts | calls |
|---|---|---|---|
| smoke | two tickets in each arm, drawn at `ORDER_SEED` | 6 | 6 |
| pass 1 | every prompt of the three arms, 171 each, in one seeded order with the arms interleaved | 513 | 513 |
| pass 2 | the same prompts, in another seeded order | 513 | 513 |

**Cost: 1,032 calls, plus any retries.** At Baidu's listed price for this model
on 2026-10-25, $0.02226 per million prompt tokens and $0.04452 per million
completion tokens:
- **the prompts** run about 1,200 tokens a call, at three characters a token,
  which is about three cents in all;
- **the plain and naming arms' answers** run under 50 tokens, which is nothing;
- **the reasoning arm's answers are not known**, because nothing recorded has
  reasoned. At the cap of 16,000 tokens on every one of its 342 calls of the
  passes they would cost about 24 cents.

So the run costs under thirty cents at the cap, and a few cents at any length
the drafter expects.

**Time.** `PLAN_QUEUE_ALONE.md`'s passes took 52 and 50 minutes for 2,028 asks,
about 1.5 seconds an ask, so the plain and naming arms take about nine minutes
a pass. **The reasoning arm's pace is not known.** At 30 seconds an ask its 171
asks take about 85 minutes, and the smoke run measures it before pass 1.
**Both passes outlive a background command of the agent's harness**, so they
run in Sergi's terminal, as `CLAUDE.md` says.

**What is not bought.**
- **The naming question with reasoning on.** That is the fourth cell of the two
  factors, and §2.1's alternative.
- **No other level, no screen, no rule-writing prompt.**
- **No other model, provider, manual or loop**, and no other reasoning effort.

---

## 2. The choices that have to be made at signature time

Signing §0 adopts the drafter's choice in each unless the signature line says
otherwise. A choice that drops a row is a change to §0, and belongs in the same
signed commit.

### 2.1 The arms — the drafter recommends three

The plain, naming and reasoning arms. The plain arm is asked again so that every
row compares arms asked on one day: `PLAN_SCREEN.md`'s one row argued from
continuity across dates was the one refuted.

**The alternatives.**
- **Four arms**, adding the naming question with reasoning on. It would say
  which rule the model names after thinking it through, as a field and not as
  reasoning to be read. It adds 342 reasoning calls, about doubling a pass, and
  no row is drafted for it.
- **Two arms.** Dropping the naming arm drops `FM-b`, `FM-c` and `FM-f`.
  Dropping the reasoning arm drops `FM-d`, `FM-e` and `FM-f`.

### 2.2 The reasoning setting — the drafter recommends high effort, with 16,000 tokens

**`{"effort": "high"}`, with `max_tokens` 16,000.**
- **Why high.** The question is whether the walk down the list is a matter of
  thinking it through, so the arm gives the model room to think. OpenRouter's
  documentation, read on 2026-10-25, lists `none`, `minimal`, `low`, `medium`,
  `high`, `xhigh` and `max`. It describes `high` as about 80% of `max_tokens`.
- **Why 16,000 tokens.** Reasoning tokens count against `max_tokens`, and when
  they spend it the answer comes back empty with `finish_reason: "length"`.
  That is how `PLAN_REUSE.md`'s third smoke run lost five proposals in fifteen
  under 1,200. 16,000 is the budget `PLAN_MANUAL.md` gave its compiled answer,
  `COMPILE_MAX_TOKENS`, which wrote 29 rules in one answer. Baidu's endpoint
  allows 131,072.
- **The smoke run must show it fits.** Every reasoning-arm attempt of the smoke
  run reasons and ends `stop` before pass 1 starts (§8).

**The alternative** is `{"effort": "medium"}`, the level OpenRouter documents
for `"enabled": true`. It would ask what this model does with reasoning at its
documented default, and give it less room.

### 2.3 The population — the drafter recommends level 3's tickets alone

That is 171 prompts an arm, on level 3's 320 decisions. It is where the order
errors were read, and the only level whose list carries identifiers.

**The alternative** adds level 0, the names alone, to the plain and reasoning
arms on level 3's tickets. It would test that the reasoning arm's gain is the
list's, as `QA-f` tested the plain question's, and it adds 684 calls, 342 of
them reasoning. The drafter does not recommend it: on these decisions the plain
arm with the names alone was right on 0.4261 (`QA-f`'s parts), so `FM-e`'s line
cannot be reached without the list.

### 2.4 One provider, pinned — the drafter recommends Baidu

**Every request carries OpenRouter's provider routing, with fallbacks off:**
`{"order": ["baidu"], "allow_fallbacks": false}`. That is
`PLAN_QUEUE_ALONE.md`'s pin, imported from its package and not retyped. On
2026-10-25 the listing of this model's endpoints names Baidu's as `baidu/fp8`,
served at fp8. Its supported parameters include `reasoning`,
`reasoning_effort` and `response_format`.

**Why Baidu.**
- **It served every answer `FM-a` reads**: the pin held in both of
  `PLAN_QUEUE_ALONE.md`'s passes.
- **The reasons that plan gave for one provider stand** (its §2.3): two
  providers part on the answer more often than one parts from itself, and
  interleaving does not match them.

**What the pin costs.** If Baidu does not serve, the request fails rather than
moving. Each failed call is retried twice after a wait, five failed asks in a
row stop a session without recording them, and the same command resumes. The
smoke run must show every attempt served by Baidu before pass 1 starts (§8).

**The alternative** is no pin. Every row would then be read within the provider
that served most answers, and `FM-a` would read across providers.

### 2.5 Two passes, the arms interleaved — the drafter recommends it

Each pass asks every prompt of the three arms once, in one order drawn at
`ORDER_SEED`. So within a pass the arms share the hours.

### 2.6 This question first

`IDEAS.md` names other routes under *What `PLAN_QUEUE_ALONE.md` opens*: the
fourth cell, the plain question with a screen, the prose, and
`SECURITY_INCIDENT` under the rules. The drafter put this one first, for three
reasons:

- **It asks about the larger part.** What the plain question leaves is the
  list's order: 141 of its 147 wrong answers at level 3.
- **It needs no screen and no loop.** Every prompt is a ticket alone, rebuilt
  for free.
- **It is a re-ask on one day**, on hundreds of paired decisions.

### 2.7 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

All on the corpus, on level 3's decisions. Nothing here is produced by this
plan. `FM-g1` recomputes the `PLAN_QUEUE_ALONE.md` rows and checks them against
their record rather than publishing them again.

| figure | value | owning record |
|---|---|---|
| `PLAN_QUEUE_ALONE.md`'s arms at `L₃`, on the 318 decisions every row reads | the plain arm 0.7689, the impasse arm 0.7280, the rule arm 0.6840 | `results_queue_alone/score.json`, published by `FINDINGS_QUEUE_ALONE.md` |
| the plain arm's runs at `L₃` | 0.7679, 0.7778 and 0.7576 | same |
| the plain arm's answers at `L₃` in §5.6's classes | 491 first, 141 order and 6 matching, of 638 | same, `QA-g` |
| where the plain arm's order errors go | 134 of 141 to the second matching rule's queue, 135 to the runner-up's, 5 to the catch-all's and 33 to the most specific rule's | `results_queue_alone/orders.json`, published by `FINDINGS_QUEUE_ALONE.md`, POST-RUN |
| the three pairs | under `H02`, 29 order errors on 36 answers; under `H15`, 12 on 36; under `H17`, 13 on 28 | same |
| two answers to one plain prompt agreeing, at `L₃` | 0.9591 | `results_queue_alone/score.json`, `QA-g` |
| the plain arm with the names alone, on `L₃`'s decisions | 0.4261 | same, `QA-f` |
| the copier that answers the most specific matching rule's queue | 0.8719, 279 of 320 | `results_queue_alone/sample.json`, Stage A |
| the rules compiled once | 1.0000 of the space (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| the pace | 2,028 asks in 52 and in 50 minutes | `FINDINGS_QUEUE_ALONE.md`, Stage B |
| reasoning by default | 20 reasoning tokens on a six-token reply; none with `{"effort": "none"}` | `PLAN_REUSE.md` §1's amendment, two calls on 2026-09-30. Not a record |
| Baidu's listing for the model | `baidu/fp8`; $0.02226 per million prompt tokens and $0.04452 per million completion tokens; up to 131,072 completion tokens | OpenRouter's endpoints listing, read on 2026-10-25. Not a record of this repository |

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
4. **Seed 17, no regeneration.** Every record under `results_manual/`,
   `results_apply/` and `results_queue_alone/` is read-only.
   `harness/record_guard.py` guards this plan's paid records, and the flag that
   overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema.**
   - The plain and reasoning arms' prompts are `PLAN_QUEUE_ALONE.md`'s plain
     arm's, byte for byte.
   - The naming arm's prompt is §5.1's, verbatim, and it is frozen by the
     signature.
   - The texts are `PLAN_MANUAL.md` §5's, pinned by digest.
6. **If the numbers come out badly, report them.** A named rule that explains
   nothing is a result, and so is a model that reasons and still misreads the
   list.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **`queue_alone/`, `apply/`, `manual/`, `fidelity/`, `reuse/` and `rung2/`
   are called by this plan and not edited.**
   - The population is `queue_alone.population.build`'s, at level 3.
   - The plain arm's prompts are `queue_alone.prompts`', and the 29 rules are
     `queue_alone.rules`'.
   - The pin, the model, the temperature and reasoning off are
     `queue_alone.plan`'s.
   - The answer is parsed by `rung2.proposers2.parse_payload`.
B. **The loop records are inputs, never outputs, and no label reaches a prompt
   or a row Stage B writes.**
   - **Labels join at scoring.** `y` is copied from the records by Stage C, and
     `qᴬ` from `PLAN_QUEUE_ALONE.md`'s records. The rows Stage B writes carry
     neither.
   - **No module on the proposer's path imports the oracle.** That path is
     `first_match/prompts.py` and `first_match/ask.py`. They import by name
     neither the oracle, nor `HIDDEN_DSL`, nor `harness.ceiling_check`, nor
     `rung2.hidden_priority`. Both join `ONLINE_LOOP` and the authority
     channel's watch.
   - **The 29 rules are read from level 3's frozen text**, by `FM-g1`, Stage A
     and Stage C, never on the proposer's path. The list of modules allowed to
     see the oracle does not grow.
C. **Every record carries `_env`**, with:
   - the model, the temperature, each arm's reasoning setting and token budget,
     and the provider pin;
   - each arm's system-prompt digest;
   - every attempt's `call_attempts`, and the cause of every retry.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded in full and never
   executed.** That is the naming arm's `rule` field and the reasoning arm's
   reasoning, when the response carries it. No stage codes the reasoning.
F. **The order of Stage B is §8's**, and the module refuses a session out of
   it.
G. **The provider is pinned on every call.** An answer served by another
   provider is not an answer of this plan. It is recorded and counted as
   invalid, never read.
H. **A failed call is never answered with v1's retry message.** Only a failed
   parse is (§0).

---

## 5. Known traps

**5.1 — The naming arm's prompt, verbatim.** It is the plain arm's at level 3,
with one line added to the answer's template. The text is in Spanish, as v1's
is, because it is prompt content.

The plain arm's answer, as `PLAN_QUEUE_ALONE.md` §5.1 froze it:

```
Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:

{
  "action": "<accion para este ticket>"
}
```

The naming arm's:

```
Responde UNICAMENTE con un objeto JSON, sin markdown, sin preambulo:

{
  "rule": "<identificador de la regla que se aplica a este ticket>",
  "action": "<accion para este ticket>"
}
```

- **Everything above the answer is the plain arm's**, byte for byte: the role,
  the task, v1's attributes and actions, and the manual's block at level 3.
- **The user message is the plain arm's**: `TICKET:` on its own line, then the
  ticket as v1 renders it.
- **The added line restates no rule of the list.** *"la regla que se aplica"*
  is the manual's own phrase: *"Se aplica la primera regla de la lista cuyas
  condiciones casa el ticket."* It does not say *primera*, so the arm does not
  remind the model of first match more than the plain arm does.

**5.2 — What each arm writes before its queue.**
- **The plain arm writes nothing before it**, as in `PLAN_QUEUE_ALONE.md`.
- **The naming arm writes the rule's identifier first**, if it follows the
  template's order. The record keeps each payload's keys in the order the
  model wrote them, and `FM-g` reports how often `rule` came first.
- **The reasoning arm reasons before it answers**, outside the answer, and its
  answer is the plain arm's single field.

**5.3 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every arm holds
it, and the text states first match. So the rows measure what the model does
with a label it holds. None of them reads level 3 as something the model knew.

**5.4 — The population is level 3's escalations.**
- **They were selected by each run's base**: the tickets no rule covered there,
  or where rules conflicted. They are not the arrivals, and they are harder.
- **Every row compares arms on the same decisions**, so the mix cancels inside a
  row. `acc_r` is not the model's accuracy on the arrivals.

**5.5 — One ticket, several decisions.** A ticket's answers serve every
decision it has, so decisions are not independent draws. That is why the error
is clustered by ticket.

**5.6 — Classify every answer before betting on a mechanism.** That is the
`IDEAS.md` lesson from `blind/cycles.py`, which `PLAN_QUEUE_ALONE.md` §5.6
applied. `FM-g` classifies every answer of every arm against the 29 rules, by
its queue, and every named rule by where it lies against the ticket's matches.
`FM-c` bets on one of those classes only after §0 has named them all.

**5.7 — Naming the rule changes the question.** The naming arm's queue is not
the plain arm's queue with a rule attached: the added field may change which
queue the model writes. That is `FM-b`. So `FM-c` reads the naming arm's own
errors, and what it names on the plain arm's errors is reported.

**5.8 — One provider is not the model.** Baidu serves this model at fp8 (§3).
Every figure here is that provider's serving of it.

**5.9 — Reasoning at temperature 0.** The request sends temperature 0 in every
arm. A provider may not honour it while the model reasons, so the reasoning
arm's two answers may part more often than the plain arm's. `S` is reported for
each arm.

**5.10 — Two dates, for `FM-a` only.** `qᴬ` is of 2026-10-24. Every row but
`FM-a` reads today's arms only. `FM-a` measures the distance, and cannot undo
it.

**5.11 — Invalid answers.** As in `PLAN_QUEUE_ALONE.md`, with §0's thresholds
and rule G's.
- **A reasoning answer cut off by its budget is invalid.** It comes back empty
  with `finish_reason: "length"`, and its reasoning tokens are still billed.
  It is a failed parse, so it is retried with v1's message, as v1 retries one.
- **Every count of a decision left out is published**, with its cause.

**5.12 — The reasoning is recorded, not read.** The response's `reasoning` field
is kept whole on every reasoning-arm row where it came back. No stage codes it.
A reading of it after the verdicts would need a codebook frozen before the
held-out reasoning is read, which is `PLAN_MANUAL.md`'s lesson from its notes.

**5.13 — Long sessions.**
- **A session that dies keeps what it paid for.** Answers are appended to a
  git-ignored partial file, and the same command resumes there.
- **An outage is not answers.** Five failed asks in a row stop a session
  without recording them.
- **A pass belongs in Sergi's terminal**, because it outlives a background
  command of the agent's harness, and a reasoning ask is slow.

**5.14 — The queues are listed in one order in every prompt.** The slot decides
some pairwise answers (`PLAN_PRIMACY.md`). Here every arm lists the eight queues
in v1's order and the 29 rules in the manual's, so both orders cancel inside a
row and neither is varied.

**5.15 — Information in front of the model has not changed what it does
before.** `CHAT_SUMMARY.md` §2.2's erratum: *"With the right information in
front of it, it makes the same mistake"*. An identifier to write is not new
information, which is a prior against `FM-b`.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**FM-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.
- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_QUEUE_ALONE.md`'s checks.** Its `QA-g1` to `QA-g3` pass, called
  through `queue_alone.gates.run_checks` and not copied. They hold the 29 rules
  to the truth of all 790 escalations.
- **Its design.** Rebuilt, it is `results_queue_alone/sample.json`'s: the
  sessions, every prompt's digest and the decisions.
- **Its rows.** `queue_alone.score` gives back `score.json`'s six verdicts from
  its passes.
- **Its order reading.** `queue_alone.orders` gives back `orders.json`'s counts
  and fractions from the same passes.
- **No float decides a check.** Values are compared as fractions and counts as
  integers, so a record written under 3.12 reads the same under 3.10.

**FM-g2 — The prompts are §5.1's, and the requests are §1's.**
- **The plain arm.** Every prompt is `PLAN_QUEUE_ALONE.md`'s plain arm at level
  3, digest for digest.
- **The reasoning arm.** Every prompt is the plain arm's on the same ticket,
  text for text.
- **The naming arm.**
  - Its system prompt is the plain arm's with §5.1's line added, and nothing
    else changed.
  - Its user message is the plain arm's.
  - Its answer asks for `rule` and then `action`, and nothing else.
  - The identifiers an answer is read against, `H01` to `H29`, are the ones
    level 3's text lists, in its order.
- **The requests.** They are checked through `tests/doubles.py`'s SDK double in
  the package's tests, which `FM-g1`'s suite runs. For each arm, a call sends:
  - the model, temperature 0, `response_format` on the first attempt, and the
    pin of §2.4;
  - reasoning off and 1,200 tokens in the plain and naming arms;
  - reasoning `{"effort": "high"}` and 16,000 tokens in the reasoning arm;
  - the two messages.

  A failed call is retried with the same messages, and a failed parse with v1's
  retry message.
- **No builder takes a record's row.**
- **Teeth.** One changed character moves a prompt's digest, and no digest stands
  for two texts. The plain and reasoning arms share their digests, because they
  share their texts.

**FM-g3 — The populations and the schedule are §0's and §1's.**
- **The prompts.** There are 171 an arm, on level 3's 320 decisions.
- **The passes.** Each holds every prompt of the three arms once, 513, in its
  order rebuilt from `ORDER_SEED`. The two orders differ.
- **The smoke.** Its six prompts are two of each arm, distinct, drawn from those
  by `ORDER_SEED`.

**FM-g4 — The signature**, §10.

---

## 7. Stage A — the design and the references (free, gated)

**Deliverable.** `first_match/sample.py` → `results_first_match/sample.json`.

- **`FM-g1` to `FM-g3`.**
- **The design.** Every prompt, with its arm, ticket, digest and the decisions it
  serves, the three sessions' orders at `ORDER_SEED`, and the system prompts.
- **The references, computed after the signature.**
  - For every decision: the identifiers of the rules its ticket matches, in
    order, and its runner-up.
  - `qᴬ` for every plain prompt, with the provider that served it.

**It produces nothing adjudicable.** It runs after §0 is signed, so that none of
its figures can inform a band.

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `first_match/ask.py` → `results_first_match/ask_smoke.json`,
`ask_pass1.json` and `ask_pass2.json`. **Three sessions, in that order, one
after another. Each record is committed before the next session starts.**

**Every session, before any call**, follows `PLAN_QUEUE_ALONE.md` §8's order:

1. **`--dry-run`** runs `FM-g1` to `FM-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`FM-g4`).** While `PLAN_FIRST_MATCH.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.** A pass needs the smoke record under this protocol,
   with:
   - a valid answer from each arm, and every attempt served by the pinned
     provider;
   - every reasoning-arm attempt reasoned, by its reasoning tokens or its
     reasoning, and ended `stop`;
   - no plain-arm or naming-arm attempt reasoned;
   - every valid naming-arm answer naming a rule.

   Pass 2 also needs pass 1's record. If the smoke run fails, the passes do
   not start, and what would change is a signed amendment.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`FM-g1` to `FM-g3`, blocking.** Stage A's record must hold the same design
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
- **No label.** Stage C joins `y` and `qᴬ` (rule B).

## 9. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `first_match/score.py` → `results_first_match/score.json`, and
`results_first_match/FINDINGS_FIRST_MATCH.md`, which owns every figure.

- **`FM-a` to `FM-f`**, each against its line, exactly, with its clustered
  standard error, *thin* and *unadjudicable* as §0 defines them.
- **Each row's parts and per-run values**, never summed into the verdict.
- **`FM-g` in full.**
- **The run itself**: failed calls, invalid actions, answers from another
  provider, retries by cause, reasoning tokens, and the pace per session and
  per arm.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `first_match/sample.py` and `first_match/score.py` spend nothing.
`first_match/ask.py` refuses before it constructs a client. **The free stages
get the gate because what it protects is the order of events, not money.** A
record of this plan written before the signature would be a figure that existed
before its band.

**The gate reads `PLAN_FIRST_MATCH.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own
line and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.**
  - `MODEL`, `PROMPT`, `TEMPERATURE`, `PROVIDER` and `PROVIDER_NAME` are
    imported from `queue_alone.plan`.
  - `REASONING_OFF` is `queue_alone.plan.REASONING`, `{"effort": "none"}`, and
    `MAX_TOKENS = 1200`, the plain arm's.
  - `REASONING_ON = {"effort": "high"}` and `MAX_TOKENS_REASONING = 16000`.
  - `MAX_RETRIES = 2`, and `CALL_RETRY_WAIT = (10, 30)` seconds before a failed
    call's two retries.
  - `settings(arm)` gives each arm's reasoning setting and token budget, the
    two things its request carries that another arm's may not.
- **The inputs.** `queue_alone.population.build` and `queue_alone.plan`'s
  paths, imported and not retyped.
- **The arms.** `ARMS = ("q", "n", "r")`, the plain, naming and reasoning arms.
- **The population.**
  - `LEVEL = 3`.
  - `TICKET_PROMPTS = 171` and `DECISIONS = 320`.
- **The sessions.**
  - `SESSIONS = ("smoke", "pass1", "pass2")`.
  - `PASSES = 2`.
  - `SMOKE_PER_ARM = 2`.
- **The seed.** `ORDER_SEED = 73`.
  - **It is new.** It is distinct from every seed a closed thread uses: 17 to
    20, 25, 41, 43, 47, 53, 59, 61, 67 and 71, and values from 1000 up.
  - **It feeds three streams**, one string seed per session.
  - **It is hash-free.** CPython seeds a string through SHA-512, so no order
    depends on `PYTHONHASHSEED`.
- **The limits.**
  - `MIN_SIGNATURES = 1` and `MAX_CONSECUTIVE_FAILURES = 5`.
  - `MAX_INVALID_SHARE = Fraction(1, 20)` and `MIN_ANCHOR_PROMPTS = 100`.
  - `MIN_NAMED_ORDER_ERRORS = 20` and `MAX_UNNAMED_SHARE = Fraction(1, 20)`.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact.
  - `FM_A_MAX_GAP = Fraction(1, 20)`.
  - `FM_B_LINE = 0`, held above.
  - `FM_C_LINE = Fraction(1, 2)`.
  - `FM_D_LINE = 0`, held above.
  - `FM_E_LINE = Fraction(9, 10)`.
  - `FM_F_LINE = 0`, held above.

**The names.**
- **The package is `first_match/`.** No module of the standard library has that
  name.
- **The rows are `FM-a` to `FM-g`, with two letters.** Every single capital
  already names a thread, and `tests/test_prose_tables.py` reads one or two
  since `PLAN_QUEUE_ALONE.md`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
first_match/__init__.py
first_match/plan.py        the gate and the constants of §10
first_match/prompts.py     the three arms' prompts                    [proposer's path]
first_match/population.py  the prompts and the sessions, on PLAN_QUEUE_ALONE.md's level-3 prompts
first_match/gates.py       FM-g1 to FM-g4
first_match/sample.py      Stage A
first_match/ask.py         Stage B: it spends                         [proposer's path]
first_match/score.py       Stage C, and the named rules' classes
results_first_match/FINDINGS_FIRST_MATCH.md
results_first_match/sample.json  ask_smoke.json  ask_pass1.json  ask_pass2.json  score.json
tests/test_first_match.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `first_match` joins it in `harness/provenance.py`, and joins
  the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The two modules marked above
  join both, with rule B's comment. The plain arm's system prompt carries the
  manual's block, so they send the manual's texts, as `queue_alone/prompts.py`
  and `queue_alone/ask.py` do.
- **The partial files**, `results_first_match/*.partial.jsonl`, join
  `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site.** The asker is a new call site, classified in
  `tests/test_call_record.py`.
- **The README's table of writers** gains its rows, and its table of tests.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_first_match/` with `_env`, the model, the
      temperature, each arm's reasoning setting and token budget, the provider
      pin, the system prompts' digests and `call_attempts`, produced with
      `PYTHONHASHSEED=0`.
- [ ] `FM-g1` to `FM-g4` passed before any record was written. The key check
      and the smoke run came before the first pass, and each session's record
      was committed before the next began.
- [ ] Every attempt of the smoke run was served by the pinned provider, every
      reasoning-arm attempt reasoned and ended `stop`, and every valid
      naming-arm answer named a rule, before pass 1 began.
- [ ] The plumbing of §10, and tests pinning:
      - the constants and the gate;
      - the naming arm's prompt against §5.1, with its teeth;
      - the plain and reasoning arms' prompts against `PLAN_QUEUE_ALONE.md`'s
        digests;
      - the requests in every arm, the pin and the reasoning settings included;
      - the retry by cause;
      - the named rules' classes on tickets built by hand;
      - the exactness of §0's comparisons and the clustered error.
      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface (the corpus, always), its arm, its
      denominator, and the date of each side it compares.
- [ ] `results_first_match/FINDINGS_FIRST_MATCH.md` owns every figure, with a
      dated erratum wherever it corrects something already published. That
      includes this plan's §0 *already seen*, if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `FM` thread. *What is open* narrows
      its second item by what this plan settles.
- [ ] `IDEAS.md`: *Why the model, asked plainly, follows a lower rule* is closed
      or narrowed, with what this plan opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `FM`, and its `TABLES`
      gains `FINDINGS_FIRST_MATCH.md`'s verdict table.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits; the plan and its
      signature are alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **The naming question with reasoning on.** The two factors have four cells,
   and this plan buys three (§2.1).
2. **Which condition the model misreads.** If `FM-c` holds, the model believes
   a lower rule applies. Which of the first rule's conditions it reads as unmet
   is in the reasoning arm's reasoning, for a reading after the verdicts, and
   in no row.
3. **The other levels.** With the prose the plain question did not help
   (`FINDINGS_QUEUE_ALONE.md`, *Every level*). Nothing here asks the prose.
4. **The loop.** A loop whose proposer names the rule that applies, or reasons,
   is a new system, and a plan of its own.
5. **Another effort, another budget, another model.** One reasoning setting is
   bought (§2.2).
6. **The arrivals.** Every figure is about escalated tickets, which are the
   hard ones.
7. **One model, one provider, one manual, two passes, one day.**
