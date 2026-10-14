# PLAN_SCREEN — what the screen of compiled rules does to the model

**Status: drafted by Claude on 2026-10-14, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §10 says why.

**This plan exists because `PLAN_FIDELITY.md` found a sign it was not built to
judge.** Its `F-f`, reported and not adjudicated, asked the model about 300
drawn decisions with the ticket alone, beside the answers it gave with its
screen of compiled rules. Without the screen it was right more often in every
run, 0.5233 against 0.4600 pooled. It also named both rare queues on every one
of their tickets. [`FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md)
calls that *a sign in a consistent direction, not a measured effect*: one answer
per arm, 100 cases a run, no standard error. §12.3 of
[`PLAN_FIDELITY.md`](PLAN_FIDELITY.md) had declared the gap before it ran:
*compiled rules may poison later answers through the screen, a loss that would
not show as any rule's error.* [`STATUS.md`](STATUS.md) lists it fourth under
*What is open*. [`IDEAS.md`](IDEAS.md) carries it in three sections:

- **Under `PLAN_FIDELITY.md`**: what a screen of compiled rules does to the
  model.
- **Under `PLAN_AUTHORSHIP.md`**: what the screen and the date did to the loop's
  own figures.
- **Under `PLAN_BLIND.md`**: why the loop's figures rose under v2b.

**The question, in its cleanest form.** On a case a compiled rule decided, does
showing the model the compiled rules nearest the ticket make it right less often
than the ticket alone would? And if it does, through what?

**Why the rows ask about the *through what*.** The drafter read `F-f`'s 300 pairs
in aggregate before drafting (§0, *already seen*). The gap is not spread evenly:

- **Where the screen's commonest action is the true queue, the screen helps the
  model; where it is not, the screen costs it.**
- **On those decisions the commonest action was the true queue three times in
  ten.**
- **Where the model's own answer differs from that action, its answer with the
  screen is that action nearly half the time.**

So the cost `F-f` saw may be the base's error, carried into the model's answers by
deference. Its sign would then belong to the base rather than to the model.
`V-c` and `V-d` bet on that, and `V-b` on the net.

**Nothing has to be re-run but the model without its screen.**
`PLAN_FIDELITY.md`'s Stage B records hold its 1,841 screen prompts, each asked
twice, with every label. Two things are bought:

- **Two answers without a screen** on each of the 1,184 tickets its draw and
  census hold.
- **One re-ask of 300 screen prompts**, to check that the old answers are still
  the model's.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic and its denominator here, before any call.**
Every figure is on the corpus: `generate_corpus(2000, seed=17)` in arrival order,
the decided cases of `results_reuse/run_n2000_r{1,2,3}.json` as
`PLAN_FIDELITY.md` drew them. No row has an exhaustive-space reading. What is
asked is the model, about cases that arrived.

**Two populations, fixed here.** §2.1 says why.

- **The pilot** is the 300 decisions `F-f` paired: the first 100 of each run's
  uniform draw. The drafter has read them in aggregate (*already seen*, below).
  They are the development set. They feed `V-a` and the readings of `V-e`, and
  no other row.
- **The held-out decisions** are positions 100 to 599 of each run's uniform draw,
  less every decision whose ticket `PLAN_FIDELITY.md`'s ticket-only session
  asked. That leaves 429, 405 and 425. Nobody has an answer without a screen on
  any of their tickets. `V-b` to `V-d` are read on them and on nothing else.

**A ticket is its attributes**, `Case.key()`, as `PLAN_FIDELITY.md` keyed its
ticket-only arm. The corpus repeats tickets, and two cases with the same
attributes get the same prompt without a screen, so they are one ticket. Every
count of tickets in this plan is by key.

**`V-b` to `V-d` are read on the median over the three bases.** Each run's value
is published beside it, with its finite-population standard error over that
run's decided cases. **`V-a` is read pooled**: it is about one instrument, not
three bases. **A verdict within one standard error of its line is labelled
*thin*** beside the verdict, and the label does not change the verdict. For a
median, the standard error used is the median run's. The pooled value of every
median row is published beside it and adjudicates nothing.

**When a run has no value, and what the median then is.** `PLAN_AUTHORSHIP.md`'s
`E-c` left this to its scorer and lost its verdict to it, so it is settled here.

- **A run has no value** for `V-b` if more than 5% of its held-out decisions lack
  the four valid answers below. For `V-c`, if fewer than 100 of its decisions
  have `t₁ ≠ p`. For a clause of `V-d`, if that clause's cell holds fewer than 50
  decisions.
- **The median is over the runs that have a value**: the middle one of three, the
  mean of two. Over two, the standard error that decides *thin* is the larger of
  the two runs'. With fewer than two, the row is unadjudicable, and the record
  says so. For `V-d`, each clause is taken on its own; if either is
  unadjudicable, so is the row.

**Notation**, per held-out decision.

- **A B prompt** is `PLAN_FIDELITY.md`'s design B: prompt v1 with the base at the
  case's moment, every rule that matches the ticket left out.
- **`y`** is the true queue, read off `PLAN_FIDELITY.md`'s record.
- **`b₁` and `b₂`** are its two answers to the decision's B prompt, given on
  2026-10-02 or 03.
- **`t₁` and `t₂`** are the two answers without a screen that this plan buys, on
  the decision's ticket, in pass 1 and pass 2. A ticket that serves more than one
  decision lends both to each.
- **`p`** is the screen's plurality action: `fidelity.prompts.plurality` on the B
  prompt, the commonest action shown, a tie going to the action shown first.
- **An answer is *valid*** as in `PLAN_FIDELITY.md` §5.5. **A decision enters a
  row only with all four answers valid.**

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **V-a** | **The instrument has not moved since `PLAN_FIDELITY.md` asked.** Re-asked verbatim, the model agrees with its answers of 2026-10-02 and 03 as often as with itself | Two clauses, `S − A` each, and both must hold. *Ticket only*: over the 301 tickets `F-f` asked on 2026-10-03, `S` is the share whose two new answers agree and `A` the mean agreement of a new answer with an answer of 2026-10-03. *Screen*: over the 300 pilot B prompts, each re-asked once, `S` is the share whose two old answers agree and `A` the mean agreement of the new answer with each of them | **≤ 0.05**, both | **> 0.05**, either |
| **V-b** | **Without its screen the model is right more often.** The item `STATUS.md` lists fourth, adjudicated | Per run, over the held-out decisions: the mean of `½(1[t₁=y] + 1[t₂=y]) − ½(1[b₁=y] + 1[b₂=y])` | **> 0** | **≤ 0** |
| **V-c** | **The screen moves the model to its plurality.** Where the model's own answer is not the screen's plurality action, the screen makes it that action markedly more often than a second answer without the screen does | Per run, over the held-out decisions with `t₁ ≠ p`: the mean of `½(1[b₁=p] + 1[b₂=p]) − 1[t₂=p]`. It reads no label | **≥ 0.10** | **< 0.10** |
| **V-d** | **What the screen does to accuracy follows its plurality.** Where the plurality is the true queue the screen helps the model, and where it is not the screen costs it | Per run, over the held-out decisions. *Clause 1*, on those with `p = y`: `½(1[b₁=y] + 1[b₂=y]) − ½(1[t₁=y] + 1[t₂=y])`. *Clause 2*, on those with `p ≠ y`: the same with the sign reversed. Each clause on its own median, and both must hold | **> 0**, both | **≤ 0**, either |
| **V-e** | *Reported, not adjudicated.* **What the drafter could not band** | The rare classes in counts. The table by true queue. The pilot asked on one day under both arms. Each base's net beside its share `p = y`. Every changed answer classified by what the screen changed it to. `finish_reason` on every call | — | — |

**Signed by Sergi: ________________________ (date: ______________)**

**Why `V-e` cannot carry a band.**

- **The rare-class counts repeat published figures**: 40 of 40 and 14 of 14
  without a screen.
- **The share `p = y` and the table by queue** are computable from records on
  disk once the answers exist, and the pilot's half of them is in *already
  seen*.
- **`finish_reason` has no claim attached.** It is recorded so that a failed or
  empty answer here has a cause on record. The three threads that met such
  answers in `IDEAS.md` never had one.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the records publish.** Everything `STATUS.md`, `IDEAS.md`,
  `FINDINGS_FIDELITY.md` and `PLAN_FIDELITY.md` publish. That covers:
  - `F-f`'s table;
  - the model's accuracy with its screen over each run's drawn decisions,
    0.4224, 0.4617 and 0.4908, and its agreement with itself there, 0.8921,
    0.9083 and 0.9498;
  - `F-e`'s counts, and the rare classes without a screen.

  So the B arm's accuracy over each run's whole draw is known. On the held-out
  decisions it was not computed.
- **The records themselves**: `results_fidelity/sample.json` and the Stage B
  session records, read for their format and for the counts below.
- **The outputs of a scratch probe the drafter ran on 2026-10-14, which is not in
  the tree and owns nothing.** It read aggregates only, never a ticket's answers
  one by one. Stage A's module measures every figure below under the gate, and
  its record owns them (`V-e`). A figure that does not reproduce is an erratum to
  this section, not a silent edit. On the 300 pilot decisions, with the one
  answer without a screen of 2026-10-03 (`t`) against the two with it:
  - **The net.** Without the screen: 0.52, 0.51 and 0.54. With it, the mean of
    two answers: 0.39, 0.48 and 0.515. The difference is +0.130, +0.030 and
    +0.025, each with a standard error near 0.05; pooled, +0.0617 with 0.028.
    Against the first answer with the screen alone, `t` alone was right on 48
    decisions and `b₁` alone on 29: 21 to 8, 15 to 12 and 12 to 9 by run.
  - **The plurality.** It is the true queue on 0.26, 0.40 and 0.24 of the
    decisions, 0.30 pooled.
    - **Where it is** (n 90), `b₁` is right 0.944 of the time and `t` 0.767. The
      screen is ahead by 0.178: by 0.077, 0.250 and 0.167 by run, on 26, 40
      and 24.
    - **Where it is not** (n 210), `t` is right 0.419 and `b₁` 0.252. The screen
      is behind by 0.167: by 0.203, 0.217 and 0.092 by run, on 74, 60 and 76.
  - **The pull.** Where `t ≠ p` (n 178), `b₁ = p` on 0.455: 0.534, 0.660 and
    0.243 by run. Where `t = p` (n 122), on 0.975. **The baseline `V-c`
    subtracts, a second answer without the screen, has never been asked**,
    except on the 27 rare-class tickets.
  - **Agreement.** The two answers with the screen agree on 0.9164. `t` agrees
    with `b₁` on 0.6433. `t` agrees with the deciding rule on 0.6467, and `b₁` on
    0.7300. `b₁` is an action shown on its screen on 0.963 of decisions, `t` on
    0.887. The true queue is shown on 246 of the 300 screens.
  - **By true queue**, pooled, `t`'s accuracy minus `b₁`'s:

    | true queue | decisions | `t` − `b₁` |
    |---|---|---|
    | `T2_TECHNICAL` | 113 | −0.204 |
    | `SELF_SERVICE_DEFLECT` | 68 | +0.279 |
    | `BILLING_SPECIALIST` | 46 | +0.435, `t` right on every one |
    | `T1_GENERAL` | 33 | +0.182 |
    | `T3_ENGINEERING` | 21 | 0, both right on 2 |
    | `ACCOUNT_MANAGER` | 17 | −0.176, `t` right on none and `b₁` on 3 |
- **The counts that size this plan**, which read no label.
  - The draw and census hold 1,184 distinct tickets, among them all 301 that
    `F-f` asked. The pilot's 300 decisions are on 276 of them.
  - The held-out decisions number 429, 405 and 425. Of them, 426, 405 and 423
    have two valid answers with the screen. They are on 883 tickets, of which
    303 serve more than one decision.
  - No held-out screen is empty. They show 4 to 12 rules, 12 at the median.
  - The probe's per-decision spreads, which §2.2 plans on: 0.484 for `V-b`'s
    difference, 0.429 and 0.476 in `V-d`'s two cells, and 0.498 for the raw
    pull.

**Not seen, because nobody has computed them**:

- any answer without a screen on a held-out ticket;
- any second answer without a screen on a ticket that is not rare;
- anything about the held-out decisions that needs both a label and their
  screens, the share `p = y` among them above all. Stage A computes that after
  the signature, so that it cannot inform a band.

**What the drafter expects, written down so the scoreboard can score it.** **All
four hold.** The drafter trusts `V-b` least, then `V-a`, then `V-d`, then `V-c`.

- **`V-a`.** `F-a` held across two days, at an `S − A` of −0.0075. The gap here is
  about two weeks, and OpenRouter routes a model name to providers this plan does
  not pin (`PLAN_FIDELITY.md` §5.9). This is an argument for continuity across
  dates, and the standing note in `IDEAS.md` says this drafter's arguments for
  continuity are the ones that lose.
- **`V-b`.** The pilot's median run is +0.030, about one and a half planning
  standard errors from the line (§2.2), and run 1 carried most of the pooled gap.
  Expected: holds, thin. A refutation would say that `F-f`'s sign was mostly one
  base's.
- **`V-c`.** The raw pull was 0.455 pooled and 0.243 in its lowest run, before a
  baseline nobody has measured. Two answers with the screen disagree on 0.08 of
  decisions, and only part of a disagreement lands on `p`, so the baseline should
  be a few points. Expected: far above 0.10 on the median. Its verdict is the
  least uncertain of the four, and its value is what the record should read.
- **`V-d`.** Both clauses held in every run of the pilot, the smallest at +0.077
  on 26 decisions. Clause 1 is the weaker: where the plurality is right, the
  model without its screen is already right three times in four.

**The drafter's record argues against most of that.**

- **The scoreboard.** On `STATUS.md`'s, 28 of 66 adjudicated rows were refuted.
- **The last plans.** `PLAN_FIDELITY.md`'s drafter expected five holds and got
  four. The ILP thread's expected four and got one.
- **This plan.** Four expected holds out of four is that profile again.
- **The development set.** Three of these four bands were set on one, as
  `PLAN_WHY.md`'s were. So a hold says that a reading of the pilot generalises,
  not that its drafter foresaw anything. The scoreboard should mark the thread
  so.

Three things were done about it, rather than said:

1. **Every line is the claim's own edge.**
   - `V-a`'s is `F-a`'s.
   - `V-b`'s is the literal *more often*.
   - `V-c`'s is `F-b`'s for *markedly*.
   - `V-d`'s are the literal signs.
2. **`V-b` to `V-d` are read only on decisions whose tickets nobody has asked
   without a screen.**
3. **A verdict inside one standard error of its line is labelled thin in
   advance.**

**How the rows read together.**

- **`V-c`** says whether the model defers to its screen. It is the half of the
  question that needs no labels.
- **`V-d`** says what deference does to its accuracy.
- **`V-b`** says what it comes to on these bases.
- **`V-a`** says whether the answers with the screen, two weeks old, can stand
  for today's.

Every combination reads:

- **All hold.** The screen costs the model accuracy, through deference to a base
  that is mostly wrong where it decides. The same deference to a base right more
  often would pay. Compiling's cost then lies in what the screen does to the next
  answer, and its sign belongs to the base.
- **`V-c` and `V-d` hold, `V-b` is refuted.** The model defers, and on the
  held-out decisions what it gains and loses by it comes to nothing or to a gain.
  `F-f`'s sign was mostly run 1's base.
- **`V-c` is refuted and `V-b` holds.** The screen costs, but not by pulling the
  model to its plurality. `V-d` and `V-e`'s classification of the changed
  answers then say where to look.
- **`V-c` and `V-b` are both refuted.** No effect of the screen that this
  instrument can see. `F-f`'s sign was noise, and the fourth item of *What is
  open* closes the other way.
- **`V-a` is refuted.** `V-b` to `V-d` are still adjudicated as signed. Each
  carries the anchor's gap beside it, the way `F-b` to `F-d` would have carried
  `F-a`'s.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read: `PLAN_FIDELITY.md`'s records.**

- **`results_fidelity/sample.json`**: the draw and every prompt's digest.
- **`ask_base{1,2,3}.json` and `ask_ticket_only.json`**: the answers.

They are inputs, never outputs: nothing under `results_fidelity/` is written by
this plan. Every answer with the screen that `V-b` to `V-d` read is in them,
with its labels.

**Bought: the model's answers, under prompt v1, on prompts `PLAN_FIDELITY.md`'s
own builders make.** The client is `PLAN_FIDELITY.md`'s, unchanged:
`OpenRouterProposer2(model="deepseek/deepseek-v4-flash", prompt_version="v1",
reasoning={"effort": "none"})`. Its `propose` is called as rung 2's loop calls
it: temperature 0, 1,200 tokens, `response_format` on the first attempt, two
retries.

- **Hard rule 5 is untouched.** No prompt text and no schema change. The
  ticket-only prompt is v1's empty-base rendering, which is what case 0 saw in
  every run.
- **One thing is added, and it changes no request.** The SDK client is wrapped so
  that each attempt's `finish_reason` is recorded. A test checks against
  `tests/doubles.py` that every request is byte for byte what `PLAN_FIDELITY.md`
  sent.

Three sessions, sequential, in this order:

| session | what is asked | prompts | draws | calls |
|---|---|---|---|---|
| smoke | five ticket-only prompts and five anchor prompts | 10 | 1 | 10 |
| anchor | the 300 pilot B prompts, rebuilt verbatim — `V-a`'s screen clause | 300 | 1 | 300 |
| ticket only | every ticket of `PLAN_FIDELITY.md`'s draw and census, under v1 with an empty base — `V-a`'s first clause, `V-b` to `V-e` | 1,184 | 2 | 2,368 |

**Cost: 2,678 calls, plus any parse retries.** That is about three fifths of
`PLAN_FIDELITY.md`'s Stage B. All of its 328 ticket-only calls returned a valid
answer, so retries should be few.

**Time.** At `PLAN_FIDELITY.md`'s own pace by the wall clock:

- **Ticket only**: 3.8 s an answer, so about 2.5 hours.
- **Anchor**: 4.5 to 5.9 s an answer, so about half an hour.

About 3 hours in all. At the slowest pace on record, 12.6 s a call, it is about
9.4 hours. **Both long sessions outlive a background command of the agent's
harness**, which ends at about half an hour. So they run in Sergi's terminal, as
`CLAUDE.md` says.

---

## 2. The choices that have to be made at signature time

**None of the choices below moves a band.** Signing §0 adopts the drafter's
choice in each unless the signature line says otherwise. §2.2 is not a choice.
It is the constraint the others work inside.

### 2.1 The held-out decisions — the drafter recommends the strict set

**Strict, as §0 defines it.** Positions 100 to 599 of each draw, less every
decision whose ticket `F-f` asked: 429, 405 and 425 decisions.

**Positional, the alternative.** Positions 100 to 599, all 1,500. It adds about
240 decisions and shrinks each run's standard error by about 8%. But 176 of its
1,059 tickets were asked without a screen on 2026-10-03, and their answers are in
the aggregates the drafter has read. The pilot is a development set. A held-out
set that shares about one ticket in six with it would be one only in part.

**What the strict set gives up**: the 27 rare-class tickets, all of which `F-f`
asked. They are a census, counted and never rated, in `V-e`.

### 2.2 How many — fixed by the draw

**The held-out decisions cannot grow without new calls with the screen.** The
answers with the screen exist only for `PLAN_FIDELITY.md`'s 600 drawn decisions
a run. So the sizes are what they are. This is what they buy, at the pilot's
shares and spreads:

| row | per run, about | planning s.e. a run | the pilot, by run | the pilot's median run, in planning s.e. |
|---|---|---|---|---|
| `V-b` | 405 to 429 decisions | 0.021 | +0.130 · +0.030 · +0.025 | 1.4 from 0 |
| `V-c` | 200 to 300 with `t₁ ≠ p` | 0.03 | 0.534 · 0.660 · 0.243, raw | about 14 above 0.10, before the baseline |
| `V-d`, clause 1 | 100 to 160 with `p = y` | 0.035 | +0.077 · +0.250 · +0.167 | 4.8 from 0 |
| `V-d`, clause 2 | 240 to 320 with `p ≠ y` | 0.025 | +0.203 · +0.217 · +0.092 | 8.1 from 0 |

This is planning arithmetic, not figures. Three assumptions lie behind it:

- **The spreads are the pilot's**, with one answer without a screen: 0.484 a
  decision for `V-b`, 0.429 and 0.476 in `V-d`'s cells, 0.498 for the raw pull.
  Two answers should lower them a little.
- **The pilot's shares stand in for the held-out set's**: of `t ≠ p`, and of
  `p = y`. Stage A measures them after the signature.
- **The pilot's per-run values are not truths.** Each carries a standard error
  near 0.05. `V-b`'s row is the one where that matters: a median run of +0.030
  could be a true zero.

### 2.3 The median, with the pooled value beside it

`PLAN_FIDELITY.md` read its decision rows on the median of three bases, and so
does this plan. **It matters more here than there.** In the pilot one base
carried most of the gap, +0.130 against +0.030 and +0.025. A pooled verdict could
be one base's; a median needs two of three. The pooled value is published beside
every median row and adjudicates nothing.

### 2.4 The anchor session — the drafter recommends it, at 300 calls

The answers with the screen that `V-b` to `V-d` read are two weeks older than the
answers they are set against.

- **`V-a`'s first clause** measures the drift on prompts without a screen, for
  free, inside the ticket-only session.
- **Only the anchor** measures it on prompts with one.

**Dropping it** saves 300 calls and about half an hour. It also removes `V-a`'s
second clause and the pilot read on one day in `V-e`, and leaves the old answers
assumed current.

**Why not re-ask every held-out decision with its screen instead**, which would
put both arms on one day? It adds about 2,500 calls and four hours, to settle
what the anchor tests for an eighth of that. If `V-a` fails, that is the next plan.

### 2.5 No placebo arm — the drafter recommends against one

`FINDINGS_FIDELITY.md` leaves open *whether any context would do the same, or
only a screen of compiled rules*. A screen of filler the length of twelve rules
would ask that. **`V-c` asks it more cheaply**: a pull toward the screen's own
plurality action is a pull toward what the screen says, which filler cannot
exert. If `V-c` holds, the next question is about content. That would be a
screen of rules drawn at random from the base, or of the hidden policy's nearest
rules, and it is another plan.

### 2.6 `PREDICTION.md`

As in `PLAN_FIDELITY.md` §2.5: this plan drafts no entry there, and its gate does
not look for one. Whether it gets a dated entry is Sergi's to decide.

---

## 3. Reference figures, with the record that owns each

All on the corpus. Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| `F-f`, matched on the same 300 decisions | 0.5233 / 0.4600 / 0.4267 | without the screen, with it, and the deciding rule; one answer per arm | `results_fidelity/score.json`, `FINDINGS_FIDELITY.md` |
| the same, by run | 0.52 · 0.51 · 0.54 against 0.39 · 0.48 · 0.51 | without and with the screen | same |
| the model with its screen, over each run's draw | 0.4224 · 0.4617 · 0.4908 | `F-c`'s model half: the mean of two answers | same |
| its agreement with itself there | 0.8921 · 0.9083 · 0.9498 | `F-b`'s `S` | same |
| `F-a` | −0.0075 (se 0.0191) | the instrument from 2026-09-30 to 10-02 | same |
| `ONCALL_ESCALATION`, both answers | 3 · 0 · 2 of 7 tickets with the screen; 14 of 14 answers without | `F-e`, and `F-f`'s rare half | same |
| `SECURITY_INCIDENT` without the screen | 40 of 40 answers | `F-f`'s rare half | same |
| the loop's end to end, median | 0.5075 under v2b, 0.4400 under v1 | v2b drafts its first call with no base shown | `results_blind/score.json`, `FINDINGS_BLIND.md` |
| the proposer's action accuracy, median | 0.5521 under v2b, 0.4839 under v1, 0.4380 under v1e | the right queue for the ticket in front of it | `FINDINGS_BLIND.md`, from `FINDINGS_OVERLAP.md`'s baselines |
| the pace of `PLAN_FIDELITY.md`'s sessions | 3.8 s ticket only, 4.5 to 5.9 s with a screen | per answer, by the wall clock | `FINDINGS_FIDELITY.md`, Stage B |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads
   `harness/domain.py` and `harness/dsl.py` and touches neither. If a frozen file
   has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Nothing here is a loop. But the order of a record is
   part of it, the two passes are defined by time, and the sessions run one after
   another, never side by side.
4. **Seed 17, no regeneration.** Every record under `results/`, `results_reuse/`
   and `results_fidelity/` is read-only. `harness/record_guard.py` guards this
   plan's paid records, and the flag that overrides it is not typed without
   Sergi asking.
5. **Do not adjust the prompt or the schema.** v1 stays as it produced every
   record this plan reads. Which rules a screen shows is `PLAN_FIDELITY.md`'s
   design B, signed there. This plan shows the same screens, or none.
6. **If the numbers come out badly, report them.**
7. **The API key goes in the environment.** Load it without printing it and
   check it by its length. Before any call, read it off OpenRouter's key endpoint
   as an API key and not a management key (§8).

And this plan's own, lettered:

A. **`fidelity/` is called by this plan and not edited**, as `overlap/` calls
   `authorship/`. The prompts come from `fidelity.prompts`, the replay from
   `fidelity.replay`, and the plurality from `fidelity.prompts.plurality`. The
   proposer and renderer behind them are rung 2's. A reimplementation would make
   these answers incomparable with `PLAN_FIDELITY.md`'s for a reason that has
   nothing to do with the screen.
B. **`PLAN_FIDELITY.md`'s records are inputs, never outputs.** Every label is
   copied from them: `truth` and the deciding rule's action. No module of this
   plan imports the oracle.
C. **Every new record carries `_env`, the reasoning setting and
   `finish_reason`.** Every command runs with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.
E. **What the model writes beyond its `action` is recorded and never executed.**

---

## 5. Known traps

**5.1 — One ticket, several decisions.** A ticket that serves two decisions lends
its two answers without a screen to both: 303 of the 883 tickets behind the
held-out decisions do. So the three runs' values share answers and are not
independent draws, as `F-e`'s seven tickets were not. The median adjudicates
anyway. Stage C publishes how many tickets serve decisions in more than one run.

**5.2 — Two dates in one comparison.** `V-b` to `V-d` set answers of 2026-10-02
and 03 against answers of the day this plan runs. `V-a` is what licenses that,
and it cannot undo it.

**5.3 — The held-out set is not quite uniform.** It is the uniform draw less the
decisions whose tickets `F-f` asked, and those include every rare-class ticket.
The finite-population standard error treats it as uniform over the run's decided
cases, which is close and not exact. Stage C publishes the held-out decisions'
class mix beside the draw's.

**5.4 — `p` is a function of the screen, not of the model.** It is the commonest
action shown, ties to the first shown, as `PLAN_FIDELITY.md`'s Stage A defined
its copier. A model may follow another shown action, the first rule's above all.
**So `V-e` classifies every decision where the two arms' answers differ by what
the screen changed the answer to**: `p`, the first shown action, another shown
action, or an action not shown. This is the lesson of `blind/cycles.py` in
`IDEAS.md`: classify every failure before betting on one mechanism.

**5.5 — Why `t₂` is `V-c`'s baseline.** Suppose the screen did nothing. Then an
answer with it and a second answer without it would be exchangeable draws of the
same answer, given `t₁`, and `V-c` would be zero in expectation. The passes are
in separate seeded orders, so `t₁` and `t₂` are exchangeable too. Which one
conditions is fixed by the pass, not chosen afterwards.

**5.6 — Invalid answers.** As `PLAN_FIDELITY.md` §5.5, with the thresholds of
§0. Every count of a decision left out is published.

**5.7 — The rare classes.** Seven `ONCALL_ESCALATION` tickets and twenty
`SECURITY_INCIDENT` ones are asked twice in the ticket-only session and counted
in `V-e`. Whether the model names `ONCALL_ESCALATION` from the ticket alone is
the fact the trigger item in `IDEAS.md` rests on. This plan measures it on a
second day.

**5.8 — The model can change under its name.** OpenRouter routes the name to
providers, and this plan pins none, as `PLAN_FIDELITY.md` did not. `V-a`
measures the combined drift and cannot apportion it.

**5.9 — A coverage screen, not a conflict screen.** Design B hides every rule
that matches the ticket, so every screen here is the one a coverage impasse
shows. A CONFLICT shows the rules that disagree. How the model treats that screen
this plan does not measure.

**5.10 — Long sessions.** As `PLAN_FIDELITY.md` §5.8, with its machinery called.
Answers are appended as they arrive, and a restart resumes. Five failed calls in
a row stop the session without recording them.

---

## 6. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

- **V-g1 — The inputs reproduce themselves.**
  - `python3 -m unittest discover` is green.
  - `PLAN_FIDELITY.md`'s Stage C, re-run in memory with `fidelity.score`'s own
    functions on its records, gives back `results_fidelity/score.json`: every
    verdict, every per-run value and the `F-f` block.
  - Every session record carries `sample.json`'s digest.
- **V-g2 — The prompts are `PLAN_FIDELITY.md`'s.**
  - **Ticket only.** For every one of the 1,184 tickets,
    `fidelity.prompts.ticket_only` builds a prompt that passes
    `check_ticket_only`. For the 301 `F-f` asked, its digest is the one
    `sample.json` recorded.
  - **Anchor.** Each of the 300 pilot B prompts, rebuilt by `fidelity`'s replay,
    has the digest `sample.json` recorded and passes `check_hidden`.
  - **The plurality.** `p` is computed for every held-out decision and every
    pilot decision, from the rebuilt prompt.
  - **Teeth.** A test changes one shown rule of one prompt and must see its digest
    move.
  - **Labels.** No prompt builder takes one.
- **V-g3 — The populations are §0's.**
  - The pilot is the first 100 of each draw.
  - The held-out set is 429, 405 and 425 decisions, and none of their tickets is
    among the 301.
  - Each held-out screen shows at least one rule.
  - At most 5% of each run's held-out decisions lack two valid answers with the
    screen.
  - The ticket-only session holds every ticket of the pilot, the held-out set and
    the census, each in both passes.
- **V-g4 — The signature**, §10.

---

## 7. Stage A — the populations and the free readout (free)

**Deliverable.** `screen/sample.py` → `results_screen/sample.json`.

- **`V-g1` to `V-g3`.**
- **The sessions**, and the two passes' orders at `ORDER_SEED`.
- **`V-e`'s free half.** Every figure §0 lists from the scratch probe, now
  measured by a module and owned by this record.
- **What the probe did not compute**, on the held-out decisions:
  - the share `p = y`, per run;
  - the size of each `V-d` cell;
  - the class mix;
  - the accuracy of the copier that answers `p`.

**It produces nothing adjudicable**, and it runs after §0 is signed, so that none
of its figures can inform a band.

---

## 8. Stage B — the calls (gated on §0)

**Deliverable.** `screen/ask.py` → `results_screen/ask_smoke.json`,
`ask_anchor.json` and `ask_ticket_only.json`.

**Three sessions, in that order, one after another. Each record is committed
before the next session starts.** The anchor comes before the ticket-only
session, so that the instrument is measured before most of the spend. `V-a`'s
verdict stops nothing, whatever it is: it qualifies the reading of `V-b` to `V-d`
(§0).

**Every session, before any call**, follows `PLAN_FIDELITY.md` §8's order:

1. **`--dry-run`** runs `V-g1` to `V-g3` and stops. It builds no client and needs
   no key.
2. **The signature (`V-g4`).** While `PLAN_SCREEN.md` carries a blank signature
   line, the module exits here.
3. **The smoke record**, for every session but the smoke run. It must be under
   this plan's protocol, with a valid answer of each kind the session will ask.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`V-g1` to `V-g3`**, blocking. Stage A's record must hold the same sessions
   and digests.
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls.** They are sequential, with
   `reasoning: {"effort": "none"}` on every one.

**What each record carries, per call:**

- **Which call**: the session, the pass and the position.
- **What was asked**: the item, its ticket and the decisions it serves; the
  prompt's digest and shown ids.
- **The answer**: its `action` and payload, or the failure; the number of
  attempts and each attempt's `finish_reason`.
- **When**: the seconds and the time.
- **The labels**, copied from `PLAN_FIDELITY.md`'s records.

---

## 9. Stage C — scoring, and the four adjudications (free)

**Deliverable.** `screen/score.py` → `results_screen/score.json`, and
`results_screen/FINDINGS_SCREEN.md`, which owns every figure.

- **`V-a`** pooled, each clause with its parts.
- **`V-b`, `V-c` and `V-d`** per run; the median adjudicates.

Each comes with its standard error and, where it applies, the label *thin*.

**Also record, outside every denominator:**

- **The parts of each row**: the accuracies with and without the screen, side by
  side and never summed.
- **The pooled value** of every median row.
- **`V-e`.**
  - The rare classes, in counts, by the queue named.
  - The table by true queue, on the held-out decisions.
  - The pilot read on one day: the anchor's answer against the two new answers
    without a screen, beside the pilot's old figures.
  - Each base's `V-b` beside its share `p = y` and its two `V-d` cells, which
    compose it exactly.
  - The changed answers classified as §5.4 says.
  - `finish_reason` by outcome: valid, invalid, failed.
- **The run itself**: failed calls, invalid actions, the held-out tickets that
  serve more than one run, and the pace per session.

---

## 10. The gate, and where the code lives

**Three modules write this plan's records, and all three refuse while §0 is
unsigned.** `screen/sample.py` and `screen/score.py` spend nothing.
`screen/ask.py` refuses before it constructs the client. **The free stages get
the gate because what it protects is not money.** Stage A's share `p = y` on the
held-out decisions is exactly what would inform `V-b`'s and `V-d`'s bands.

**The gate reads `PLAN_SCREEN.md` and no other plan, and it counts every
signature line**, with `reuse/plan.py`'s counting called with this plan's path
and minimum. No flag skips it.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The inputs.** `PLAN_FIDELITY.md`'s records, and its `RUNS`, `N` and `SEED`,
  imported from `fidelity.plan` and not retyped.
- **The client.** `fidelity.plan`'s `MODEL`, `PROMPT` and `REASONING`, imported.
- **The populations.** `PILOT_PER_RUN = 100`, which is
  `fidelity.plan.TICKET_ONLY_PER_RUN`, and the held-out set as §0 defines it.
- **The sessions.** `TICKET_ONLY_DRAWS = 2`; `ANCHOR_DRAWS = 1`;
  `SMOKE_PER_ARM = 5`.
- **The seed.** `ORDER_SEED = 53`. It is distinct from every seed a closed thread
  uses: 17 to 20, 25, 41, 43, 47, and values from 1000 up.
- **The limits.** `MIN_SIGNATURES = 1`; `MAX_INVALID_SHARE = 0.05`;
  `MIN_PULL_POPULATION = 100`; `MIN_CELL = 50`.
- **The lines of §0**: `0.05`, `0`, `0.10`, and `0` for each clause of `V-d`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
screen/__init__.py
screen/plan.py      the gate and the constants of §10
screen/sample.py    Stage A: the populations, V-g1 to V-g3, V-e's free half
screen/ask.py       Stage B: it spends
screen/score.py     Stage C: V-a to V-d, and V-e
results_screen/FINDINGS_SCREEN.md
results_screen/sample.json  ask_smoke.json  ask_anchor.json
results_screen/ask_ticket_only.json  score.json
tests/test_screen.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `screen` joins it in `harness/provenance.py`, and joins the
  oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP`.** `screen/ask.py` joins it.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The README's table of writers** gains its rows.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 11. Definition of done

- [ ] Records under `results_screen/` with `_env`, the reasoning setting and
      `finish_reason`, produced with `PYTHONHASHSEED=0`.
- [ ] `V-g1` to `V-g4` passed before any record was written. The key check and
      the smoke run came before the first paid session, and each session's
      record was committed before the next began.
- [ ] The plumbing of §10, and tests pinning the constants, the gate, the
      populations, the prompts against `PLAN_FIDELITY.md`'s digests and their
      teeth, the unchanged request, and the arithmetic of §0; the whole suite
      green.
- [ ] Every figure in prose names its surface (the corpus, always), its
      denominator and, wherever it compares two arms, the date of each.
- [ ] `results_screen/FINDINGS_SCREEN.md` owns every figure, with a dated
      erratum wherever it corrects something already published. That includes
      this plan's §0 *already seen* if Stage A does not reproduce it.
- [ ] `STATUS.md`: the scoreboard gains the `V` thread, marked as banded on a
      development set, and the fourth item of *What is open* is closed or
      narrowed.
- [ ] `IDEAS.md`: the screen items under `PLAN_FIDELITY.md`, `PLAN_AUTHORSHIP.md`
      and `PLAN_BLIND.md`, and the trigger item, closed or narrowed. The empty
      answers informed by `finish_reason`. Whatever this plan opens, added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **Why the model defers.** Whether it trusts what reads as compiled policy, or
   follows whatever list it is given, `V-c` cannot say. A screen of random
   rules, or of the hidden policy's, would be the next plan (§2.5).
2. **Whether a better base would turn the cost into a gain.** `V-d`'s first clause
   reads the screen where its plurality happens to be right. No base here is
   right more often than not, and this plan builds none.
3. **The loops.** `PLAN_BLIND.md`'s and `PLAN_AUTHORSHIP.md`'s figures came from
   loops, with births, repair rounds and placements. This plan re-asks decided
   cases. It can say whether the screen costs the model. It cannot say how much
   of those loops' differences that explains.
4. **The dates.** `V-a` measures how far today's model is from the one of
   2026-10-02. It cannot undo the distance.
5. **One model, one corpus, three bases.**
6. **The trigger.** If `V-b` to `V-d` hold, they say what a trigger should not
   show the model, and `V-e` says whether the rarest queue is still in it. A
   trigger is still another plan.
7. **The two classes without correct rules.** The table by queue reports them.
   The pilot already says that the model, with the ticket alone, named
   `ACCOUNT_MANAGER` on none of its 17 decisions. So the screen is not what
   loses that class.
8. **Conflict screens** (§5.9).
