# PLAN_PLACEMENT — the placement round that lists only what the engine can still order, beside v1b, under half the errors reported

> **[CLOSED 2026-11-08] Executed in full, with §0 signed.** Sergi signed §0 on
> 2026-11-07, before any figure of the plan existed. All six rows were
> adjudicated on 2026-11-08.
> - **`PL-a`, `PL-b`, `PL-c` and `PL-d` hold**, `PL-c` thinly, as every hold of
>   it is.
> - **`PL-e` is refuted, thinly, and `PL-f` is refuted.**
> - `PL-g` is reported.
>
> **The figures are owned by
> [`results_placement/FINDINGS_PLACEMENT.md`](results_placement/FINDINGS_PLACEMENT.md)**,
> and no result is to be read off this file. The scoreboard is in
> [`STATUS.md`](STATUS.md).
>
> **Two estimates of this file were far from what happened.** §1 expected a v1c
> run to make fewer calls than a v1b run, and at the medians v1c's runs made
> more. §1 gave the runs' time at Baidu's pace, and DeepInfra's was slower. The
> findings give both.
>
> **The line immediately below says `unsigned`.** That was this file's status
> while it was drafted, and it has been false since 2026-11-07. The line is
> kept unedited and this banner is its correction. The banner touches no line
> of §0, adds no signature line, and travels alone.

**Status: drafted by Claude on 2026-11-07, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0.** The signature has to land before
any figure named here exists, in its own commit, staged by name. That includes
Stage A, which spends nothing: §11 says why. Corrected before signature on
2026-11-07, where the package written to it showed the draft inexact. Each
correction is dated in place, and no row and no line moved.

**Asked for by Sergi on 2026-11-07**, on the item [`STATUS.md`](STATUS.md)'s
*What is open* ends its second item on: *a round that lists only what the engine
can still order*. [`IDEAS.md`](IDEAS.md) carries it under *What
`PLAN_REASONED_LOOP.md` opens* as *a placement round that asks only for what the
engine can order*. Two choices were his before this was drafted, each made after
the drafter showed him the free reading below:

- **The trigger and the arms.** Both arms run `PLAN_CHANNEL.md`'s channel arm, at
  coverage 1/2. One runs v1b and one the new round, three runs each,
  alternating. Run `k` of each arm reads the draws of `PLAN_CHANNEL.md`'s run
  `c r{k}`.
- **What the new round leaves out.** Rules nested with the draft, and rules whose
  shared region with the draft third rules already govern when the round is
  listed.

**The provider follows from the first choice** by the rule agreed with Sergi on
2026-11-06, which `IDEAS.md` records under *What `PLAN_CHANNEL.md` opens*.
Every arm runs inside the plan, so DeepInfra's fp8 endpoint is pinned, with a
small same-day bridge of prompts asked of Baidu and of DeepInfra (§2.6, §2.8,
§5.5). It is his to sign.

**The item.** v1b's placement round lists `O`: every rule of another queue whose
extension meets the draft's over the space. It asks for the draft placed against
each, and refuses an answer that leaves one without a side. A refused rule is
not born (`reasoned_loop.loop.propose_v1b`; `PLAN_REASONED_LOOP.md` §5.2). Read
POST-RUN, that list holds two kinds of rule against which a side can decide
nothing.

- **Rules nested with the draft.** Two texts the proposer reads disagree about them.
  - **Level 3's system prompt** says: *"Por eso solo necesitas declarar
    prioridad frente a reglas que se solapan con la tuya sin que una contenga a
    la otra. Si tu regla es un caso particular de otra, no declares nada: el
    nivel 1 ya lo resuelve."*
  - **The placement message** says: *"Situala frente a cada una de la lista."*
  - **What a side against one adds.** By `rung2/engine2.py`'s `try_edge`, a side
    that puts the narrower rule on top is accepted as redundant and enters
    nothing. One that puts it below is refused as contradicting containment.
  - **What leaving one out costs** is the birth. With reasoning on, the proposer
    follows the system prompt. 56 of `PLAN_REASONED_LOOP.md`'s 95 unplaced
    escalations left out only nested rules, and a nested rule was left out about
    seven times as often as a crossing one (`FINDINGS_REASONED_LOOP.md`, *Where
    the unplaced answers come from*).
  - **What it cost a run.** In `PLAN_CHANNEL.md`'s c r1 the keyword's default, a
    rule of `T2_TECHNICAL` born at case 238, contained every draft of
    `SECURITY_INCIDENT`. Each broad draft's answer left it out, and each was
    refused. The run decided 0.7201 of the space, and recalled 0.3238 of the
    queue (`FINDINGS_CHANNEL.md`, *Why c r1 lost `SECURITY_INCIDENT`*).
- **Rules whose conflict with the draft the base already decides.** A point of a
  pair's shared region is *governed* when a rule other than the two beats each
  of them there. On a governed point an edge between the two decides nothing,
  whichever way it points.
  - **How much of the list it was.** In `PLAN_REASONED_LOOP.md`'s error arm,
    more than a quarter of the listed pairs' shared region was governed before
    the draft placed itself, on the half without the keyword
    (`FINDINGS_REASONED_LOOP.md`, *Why the error arm's edges sit on regions third
    rules govern*).
  - **What such an edge still does.** It decides nothing, but it enters the
    graph `try_edge` searches for cycles. In c r2 the engine refused two right
    edges for closing a cycle through rules that do not match the contested
    points, and the run lost 640 points of `ONCALL_ESCALATION` there
    (`FINDINGS_CHANNEL.md`, *Why c r2 recalled less `ONCALL_ESCALATION` than its
    draws allow*).

`PLAN_CHANNEL.md` kept both defects in both its arms on purpose (its §6.7). This
plan mends both in one arm and keeps them in the other.

**None of this is new analysis, and the plan's part is the instrument.**
`ARBITRATION_REPORT.md` already says that containment orders a nested pair
*"without spending a single question"* (§3, level 1), and that a side against
containment is refused (§3, level 2). Its note of 2026-10-06 in §5 records the
one earlier protocol that asked on nested pairs, `PLAN_AUTHORSHIP.md`'s. Its P2
says that *"there are contending pairs that change no decision because nothing
they match survives the rules above them"* (§7). §8 says that what the masks
can enumerate is not a question for the model. What this plan adds is a round
that asks accordingly, run beside the one that does not.

**What the drafter found before drafting, and why this design.** All of it is
free, and none of it reads an answer this plan buys. §0 gives the figures and
their provenance.

- **On v1b's own answers, the new round would have taken most refusals away.**
  - **The count.** Across the twelve runs of `PLAN_REASONED_LOOP.md` and
    `PLAN_CHANNEL.md`, 208 of 878 placement rounds ended unplaced, and every one
    of them was answered.
  - **The method.** Each base was rebuilt as it stood before each draft, and
    each recorded answer was set against the list the new round would have sent.
  - **What came out.** 124 of the 208 answers would have been complete, 122 of
    them from leaving out the nested rules alone.
- **In c r1 it would have taken the broad drafts.** The new round would have
  accepted 6 of c r1's 9 unplaced answers on `SECURITY_INCIDENT`, among them the
  three drafts of 16,800 points or more. It would still have refused c r2's draft
  of `H04`'s region whole, at case 1951: the rule that answer left out crosses
  the draft and is not governed.
- **It changes nothing a proposer that never errs compiles.**
  - **The hidden policy.** Through the new round it installs 192 edges where v1b
    installed 199, and still decides 134,400 of 134,400 points and 2,000 of 2,000
    cases.
  - **The transcriber.** Under each of `PLAN_CHANNEL.md`'s draws it compiles
    exactly what it compiles under v1b, in three calls a run fewer.
- **It is not expected to widen the births.**
  - **Breadth did not decide refusal.** Under v1b, a draft that is its governing
    rule's region was refused no more often than one that is not: 54 of 247,
    against 154 of 631.
  - **So refusal did not make the births narrow**, and the new round leaves the
    first call, where breadth is drawn, as it is.

**The question, in its cleanest form.** With level 3's manual in the prompt,
reasoning on, and the channel at coverage 1/2:

- does a round that lists only what the engine can still order leave fewer
  answers unplaced?
- does the loop then compile the policy, in the median run and in every run?
- does it cost anything against v1b, within one period?
- does v1b compile the policy again, on a new period and a new provider?
- does the new round compile the rarest queue?

**Two arms.** Both run `PLAN_CHANNEL.md`'s channel arm. That is
`PLAN_REASONED_LOOP.md`'s loop on rung 2's engine, at n=2000 and seed 17, with
level 3's manual and reasoning on. A case escalates on an IMPASSE or a CONFLICT,
and on a wrong decision whose draw falls below 1/2. Each arm has three runs, the
arms alternate, and every call goes to one provider.

- **v1b** is `PLAN_CHANNEL.md`'s channel arm, called and not changed, on DeepInfra.
- **v1c** is v1b with one change, to the placement round's list (§5.2). It lists
  a rule of another queue that the draft meets only when both hold:
  1. neither extension strictly contains the other;
  2. some point of their shared region is not governed when the round is
     listed.

  A round whose list comes out empty is not sent, and the draft is born at once,
  as under v1b when the draft meets no rule of another queue. Every text is
  v1b's, byte for byte.

The arms send the same texts and the same first calls. They differ only in which
rules the placement round lists.

**What it changes in what is measured, said first.**

- **The arms differ in the list, and in nothing else the proposer is handed.**
  v1c's list is a subset of v1b's. An answer is held to v1c's list exactly as v1b
  holds one to its own: the same rule, and a side for every listed rule.
- **What v1c leaves out could decide nothing.**
  - **A nested rule.** Containment orders the pair whichever side an answer
    gives.
  - **A governed rule.** No rule and no edge is ever removed from the base, so a
    point governed at listing is governed at every later case. An edge between
    the two would never decide one.
  - **What it does change.** The edges v1c never asks for never enter the graph
    that `try_edge` searches for cycles. So v1c changes the graph as well as the
    asks, and no row separates the two (§6.11).
- **It gives up one signal.** Under v1b, a side against containment is refused
  and counted. It is the only way a proposer can say that level 1 ordered a
  nested pair wrongly. Under v1c that count cannot rise.
  - **What the counter has meant so far.** It fired 8 times under
    `PLAN_AUTHORSHIP.md`, and 1, 5 and 1 times in `PLAN_CHANNEL.md`'s channel
    runs. Of `PLAN_AUTHORSHIP.md`'s eight, seven were between rules of one
    queue, and on the eighth level 1 was right on every point
    (`ARBITRATION_REPORT.md` §5, notes of 2026-10-06).
  - **What it could never do.** No such side was ever installed, under either
    protocol: the engine refuses it.
- **The round now touches coverage as well as order.** `ARBITRATION_REPORT.md`
  §5 separates the material an order can recover from the regions no correct rule
  covers. v1b's refusal decides whether a rule is born at all, so the round reads
  on the second kind too, and per-queue recall reads the protocol as well as the
  proposer.
- **A refusal taken away can be an error born.** Under v1b a refused draft leaves
  its region to escalate again. Under v1c the draft is born, and if it is wrong,
  its decisions stand until the channel reports them. That is the conversion of a
  visible refusal into a silent error that `ARBITRATION_REPORT.md` §7 warns of in
  its third objection to P1, and `PL-g` counts it (§6.19).
- **The pairing fixes which cases can be reported, not which are.** Run `k` of
  both arms reads one set of draws. The bases differ between the arms, and so do
  their wrong decisions (§6.5).
- **The provider is new for this loop.** Every paid thread since
  `PLAN_QUEUE_ALONE.md` pinned Baidu.
  - **Within the plan,** both arms run on DeepInfra, so every row is read within
    one provider.
  - **Across plans,** every comparison with `PLAN_CHANNEL.md`'s runs crosses
    dates and providers. It is reported, in `PL-g`, beside the bridge.
- **v1b's two defects are kept in its arm on purpose.** It is the comparator, and
  it is `PLAN_CHANNEL.md`'s channel arm.
- **In `CHAT_SUMMARY.md` §1's terms**, priority enters only through an external
  channel: declaration, feedback or authority. Both arms hold the authority
  channel, the manual, and the same feedback, the channel. This plan changes what
  the declaration channel asks, and nothing else.
- **Both arms break rung 2's invariant**, as `PLAN_CHANNEL.md`'s did. The trigger
  reads the truth of every arrival, and acts on half the wrong decisions. Neither
  the label nor the fact that the base erred reaches the proposer.
- **Reasoning is on**, as in `PLAN_REASONED_LOOP.md` and `PLAN_CHANNEL.md`,
  against `PLAN_REUSE.md` §1's amendment, for this plan's calls only.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The runs.** `R = 3` runs per arm. Each run is `PLAN_REUSE.md`'s loop over the
2,000 cases of `generate_corpus(2000, seed=17)`, with a fresh rung 2 engine. Its
trigger is `PLAN_CHANNEL.md`'s channel at coverage 1/2. Run `k` of either arm
reads the draws of `PLAN_CHANNEL.md`'s `c r{k}`. The arms alternate, as §2.4
sets.

**The statistics.** Each is a ratio of integer counts. **Each is compared with its
line exactly, as a fraction.** No rounding enters a verdict.

- **`B`, `space(B)`, `recall_q(B)` and `calls(r)`** are `PLAN_CHANNEL.md`'s,
  computed by the same functions.
  - **`B`** is a run's final base, rebuilt from the record and held to the
    engine the run ended with.
  - **`space(B)`** is the share of the 134,400 points that `B` decides right
    under rung 2's engine, by `manual.instrument.over_space`. A CONFLICT or an
    IMPASSE is not right.
  - **`recall_q(B)`** is the share of the points whose true queue is `q` that
    `B` sends to `q`.
  - **`calls(r)`** counts one call per escalation, and one per placement round
    sent. An attempt retried inside a call is not another call.
- **`refused(r)`.** Of run `r`'s escalations, the share that ended *unplaced*
  with an answer.
  - **Such an escalation** had its placement call come back, and the answer kept
    the draft's rule but left a listed rule without a side, so the rule was not
    born.
  - **A placement call that never came back** is refused as unplaced too
    (`PLAN_REASONED_LOOP.md` §5.2), and is not counted here: it is a failure,
    not an omission.
  - **The denominator** is every escalation of the run. A round v1c does not
    send cannot end unplaced, and still counts in the denominator.
- **The median** of three runs is the middle one, and of two runs their mean.

**The unit, *thin*, and when a row has no value.** All of it is settled here and
not in the scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **Every adjudicated row but `PL-c` reads medians over an arm's runs.**
- **A verdict on a median is labelled *thin*** when any one run of an arm the
  row reads, put in place of that arm's median, would put the statistic on the
  other side of its line. That is `PLAN_MANUAL.md`'s test, as `PLAN_CHANNEL.md`
  applied it. The label does not change the verdict.
- **`PL-c` counts runs, and its *thin* is the same test read on a count.**
  - Its verdict is thin when moving one run to the other side of 0.90 would
    change it.
  - So a hold of `PL-c`, which needs all three runs, is always thin, and the
    record says so in advance.
  - A refutation is thin when exactly one run falls below the line.
- **What a spread between runs as wide as a line does.**
  `PLAN_CHANNEL.md`'s channel runs decided 0.7201 to 0.9872 of the space.
  - That spread, 0.2671, is more than five times `PL-d`'s line, so `PL-d`'s
    verdict may well be thin whichever way it falls. *Thin* is how the record
    says so.
  - No line was widened to absorb that spread, and none will be.
- **What one run does to `PL-f`.** The draws of run 2 make no `H05` ticket
  reportable (`PLAN_CHANNEL.md` §0, figure 3). Under the standing trigger no
  ticket of the queue ever escalated otherwise, and `H05` governs a third of the
  queue's points. Unless the proposer writes `H05`'s region from another ticket,
  `PL-f` holds only if v1c's runs 1 and 3 both reach its line.
- **A run is complete** when it reaches case 2,000, or the cap of §1.
  - A run that cannot be completed leaves its arm with fewer runs. The rows read
    the runs that exist, and the record names the missing one.
  - A row that reads an arm with fewer than two runs has no value.
  - **`PL-c` has a value only with three complete v1c runs.**
  - **`PL-a` has no value if v1b's median `refused(r)` is 0.**
- **A row with no value is unadjudicable**, and the record says so.

**Which side had the label**, for every arm and reference. This was checked
against the prompts and the code while drafting, and not recalled, as `CLAUDE.md`
asks of any plan that sets a comparison on the proposer:

| who | what it is handed | reads a label? |
|---|---|---|
| the proposer, both arms | the 29 rules in order, under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."*; the ticket; for a placement round, its draft and the listed rules | **yes, in effect**: every ticket's label is derivable from the text by first match (`PLAN_MANUAL.md` §6.2) |
| the trigger, both arms | the truth of every arrival, and one draw per case fixed before the run | **yes**: whether the base's decision is right. It acts only where it is wrong and the draw is below 1/2. Nothing of it reaches the proposer |
| v1c's list | the base's extensions, its containments and its declared edges, and the draft's extension | **no**: it reads no label, no draw and no policy |
| the bridge (§5.5) | the first call both arms send: level 3's system prompt and the ticket, under v2b's `BLIND_BASE` | **yes, in effect**, as the proposer: the text, never the label |
| the transcriber references (§5.6) | level 3's text, applied by first match; the truth and the draws, as the trigger reads them | yes |

- **No arm sees an example.** The loop sees the arrivals as they come, as every
  loop has.
- **No baseline is fitted to the proposer's answers.** The references are
  mechanical, and they read the text, the truth or the draws, never an answer.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **PL-a** | **The new round takes at least a quarter of the refusals away**, within one period | the median over v1c's runs of `refused(r)`, over the median over v1b's runs | **≤ 3/4** | **> 3/4** |
| **PL-b** | **Under the new round, half the reports compile the policy**: `CH-a`, under v1c | the median over v1c's runs of `space(B)` | **≥ 0.90** | **< 0.90** |
| **PL-c** | **Under the new round, every run compiles it** | the number of v1c's runs whose `space(B)` is at least 0.90, of three | **3** | **2 or fewer** |
| **PL-d** | **The new round costs at most a twentieth of the function**, within one period | the median over v1b's runs of `space(B)`, less the median over v1c's runs | **≤ 0.05** | **> 0.05** |
| **PL-e** | **v1b compiles the policy again, on a new period and provider**: `CH-a` replicated | the median over v1b's runs of `space(B)` | **≥ 0.90** | **< 0.90** |
| **PL-f** | **Under the new round, half the reports compile the rarest queue**: `CH-c`, under v1c | the median over v1c's runs of `recall_ONCALL_ESCALATION(B)` over the space | **≥ 0.90** | **< 0.90** |
| **PL-g** | *Reported, not adjudicated.* **What the drafter could not band** | Every run of both arms on every surface: `space` whole and on each keyword half, `corpus(B)` read whole, the recall of all eight queues on both surfaces, `K-a`, and `cover(r)`. The placement rounds, by arm: the rounds sent and not sent, the sizes of `O` and of the list, every rule left out by its reason, and every verdict. Every unplaced answer, by the relation of what it left out. Citations of `H01` to `H29`. Edges by the engine's verdict, every edge against containment, and every right edge refused for closing a cycle. The CONFLICT escalations, counted as a quantity and not as a cost. The births that are their governing rule's region, and those that are a listed rule's. Every v1c birth whose round left a rule out, by whether its queue is right. `refused(r)` and `calls(r)` by run, and the escalations by cause and over time. Each run beside the transcriber under its own draws and protocol. The rare queues by escalation and verdict, with the supply each run's draws leave. `RL-e`'s direction and the Stage C ranking's on this plan's runs, by arm. This plan's v1b runs beside `PLAN_CHANNEL.md`'s c runs, and its v1c runs beside them too, run for run under the same draws, across dates and providers. The bridge: each provider's first calls against the label, against the governing rule's region and against each other, and Baidu's against `PLAN_CHANNEL.md`'s recorded drafts of the same tickets. The calls: providers, finish reasons, tokens, reasoning tokens over the attempts that reached the model, seconds by round, retries by cause, and the rate limits met. The reasoning, recorded whole and not coded | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-11-07)**

**Why each row, and why these lines.**

- **`PL-a` reads the defect where it acts.** v1c changes which rules are listed,
  so the first thing it can change is how often an answer leaves one without a
  side. Two hypotheses predict different ratios.
  - **If the proposer's omissions follow the texts**, it leaves out what the
    system prompt says needs no side. v1c takes those omissions away. The ratio
    then falls near what the drafting reading found on v1b's own answers in
    `PLAN_CHANNEL.md`'s channel runs: 474/992, 0.4778.
  - **If they follow the list**, the proposer leaves out some share of whatever
    is listed, and the ratio stays near 1. Twelve of `PLAN_REASONED_LOOP.md`'s
    unplaced escalations point that way: they placed only the nested rules,
    reading `beats` and `loses_to` as containment. Under v1c they would have
    nothing to place.
  - **The line is the midpoint, 3/4**, as `CH-f`'s was.
  - **The list makes part of a hold mechanical.** An answer cannot leave out a
    rule it is not shown. `ARBITRATION_REPORT.md` §7's third objection to P1
    warned of a filter that raises an acceptance rate *"whatever the model
    does"*. So a hold of `PL-a` says how the proposer reads the round, and
    nothing about what the loop compiles. The rows that read the truth are
    `PL-b` to `PL-f`.
- **`PL-b` is `CH-a`, under v1c.** Its statistic and line are `CH-a`'s, which are
  `RL-d`'s: within a tenth of the space of compiling the policy once (`G-a`).
- **`PL-c` asks what a median cannot.** The defect bites a run all at once, when a
  broad rule of another queue is born before a queue's broad drafts. c r1's
  default was one; `PLAN_REASONED_LOOP.md`'s e r3 wrote another, a catch-all, at
  case 1.
  - **Why a median misses it.** A median of three is blind to one run that loses
    a queue. That is how `CH-a` held while c r1 decided 0.7201.
  - **The lesson it follows.** `PLAN_SPOTCHECK.md`'s `N-c` left it: band how
    many runs get a quantity a run gets all at once or not at all.
  - **The line on each run is `CH-a`'s, 0.90.** v1b reached it in two of
    `PLAN_CHANNEL.md`'s three channel runs.
- **`PL-d` is the plan's comparison.** The arms differ in the list and nothing
  else, within one period, under one provider.
  - **The line is `CH-b`'s, a twentieth**, and it bounds a cost; it is not a bet
    on a gain.
  - **v1c is not expected to raise the median run.** v1b's median run did not
    lose a queue in `PLAN_CHANNEL.md`. What v1c is expected to change, the run
    that loses one, is `PL-c`'s.
  - **A hold does not rule out a cost of that size**, with three runs an arm and
    a spread between runs of 0.27. The record says so beside the verdict,
    whichever it is.
- **`PL-e` makes `PL-d`'s comparator this plan's own runs.** It replicates
  `CH-a` on a new period and a new provider, and its line is `CH-a`'s.
  - **Its band was drafted after `CH-a`'s figures were seen.** What it
    pre-registers is the new runs' figure, which does not exist
    (`EXTERNAL_REVIEW.md` §5.6).
  - **But a replication surprises its author less than a first measurement**
    (`EXTERNAL_REVIEW.md` §3). The scoreboard should read its verdict as a
    replication, as it reads `CH-d`'s and `CH-e`'s.
- **`PL-f` is `CH-c`, under v1c.** Its statistic and line are `CH-c`'s. Read
  *What one run does to `PL-f`*, above, before reading the verdict.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **`CLAUDE.md`**, whole.
- **`STATUS.md`**: what it read and did not.
  - **Read:** the list of its sections; its opening, to the erratum of
    2026-09-28; *What is open*, with every dated note in it; and the
    scoreboard's opening, its table, its totals and the paragraphs after them.
  - **Not read:** *What is established*, *What was withdrawn* and *What this does
    not show*.
- **`IDEAS.md`**:
  - its header, *Pending and already specified* and *What `PLAN_CHANNEL.md`
    opens*, whole;
  - *What `PLAN_REASONED_LOOP.md` opens*, from *Why the loop's proposer writes
    narrow rules* to *Reasoning in the loop apart from v1b*;
  - *What the outside reading of October 2026 proposes*, from *A label model
    over the learned base* to the end of the section;
  - *What `ARBITRATION_REPORT.md` §7 proposes* and *Prior to the four rungs*,
    whole;
  - the titles of the items in every other section.
- **The channel thread.**
  - `PLAN_CHANNEL.md`, whole.
  - `FINDINGS_CHANNEL.md`:
    - its opening, to Stage A;
    - *The six runs*;
    - Stage C from its table of verdicts to *The recall of the eight queues*;
    - from *The drafts, the verdicts and the placement rounds* to *What Stage C
      does not settle*;
    - both POST-RUN sections, whole.
- **The reasoned-loop thread.**
  - `PLAN_REASONED_LOOP.md`'s list of sections, and its §5.1 and §5.2.
  - `FINDINGS_REASONED_LOOP.md`'s list of sections, and its two POST-RUN
    sections *Where the unplaced answers come from* and *Why the error arm's
    edges sit on regions third rules govern*, whole.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  A subagent of the drafter read all three whole for this plan, with every dated
  erratum and note. It reported every passage bearing on the plan, with its
  place.
  - **What it found absent.** No passage of the three bears on thin rows,
    medians of three runs, providers or placement rounds. Those rules are
    `CLAUDE.md`'s, and this plan follows them there.
  - **What the drafter read directly**, the passages this plan rests on:
    - `ARBITRATION_REPORT.md` §3: its level 1 on what containment gives
      *"without spending a single question"*, its level 2 on what the validator
      checks and cannot, and its level 3 on the trigger and the error detector;
    - its §5: the paragraph on the two kinds of material, and the notes of
      2026-10-06 on the declarations level 1 refused;
    - its §7: the third objection to P1, P2's corrected cost argument, and P3
      with its note of 2026-10-06;
    - its §8 paragraph on the critic;
    - `EXTERNAL_REVIEW.md` §1.5 on `keep_k`'s hint, §3 on figures seen before a
      band, and §4.2 on a control's invariants checked over the space;
    - `CHAT_SUMMARY.md` §1, on the three channels and on the signal that
      extinguishes itself.
- **The code read.**
  - **Whole:** `rung2/engine2.py`, `blind/protocol.py`,
    `reasoned_loop/protocol.py`, `reasoned_loop/loop.py`, `channel/loop.py` and
    `channel/plan.py`.
  - **The validator's parts:**
    - `authorship/protocol.py`'s `overlapped`, `citations` and `unplaced`;
    - `authorship/loop.py`'s `install_declarations`;
    - `blind/loop.py`'s docstring and its `_failed_call`, `_refused`, `_born` and
      `_a_rule`;
    - `overlap/protocol.py`'s `split_overlapped`.
  - **The POST-RUN readers:**
    - `reasoned_loop/governed.py`'s docstring, `replay` and `governed`;
    - `reasoned_loop/decided.py`'s `defeaters`;
    - `reasoned_loop/unplaced.py`'s `relation` and `rows_of`;
    - `reasoned_loop/references.py`'s `Transcriber` and `hidden_through_path`;
    - `reasoned_loop/score.py`'s `births_against_the_list`;
    - `edges/rebuild.py`'s `births` and `edges_by_birth`.
  - **The channel's:** `channel/references.py`'s transcriber, and
    `channel/run.py`'s docstring.
  - **The constants:**
    - those of `reasoned_loop/plan.py` and `first_match/plan.py`;
    - `queue_alone/plan.py`'s pin;
    - `reuse/plan.py`'s `gate_signature`.
  - **The system prompt.** `manual.prompts.loop_system_prompt(3)`'s paragraphs
    on declaration, and its schema.
  - **The tests:**
    - `tests/test_prose_tables.py`'s `THREADS`;
    - `tests/test_call_record.py`'s list of call sites;
    - `tests/test_oracle_separation.py`'s `ONLINE_LOOP` from `PLAN_CHANNEL.md`'s
      entries on, and `AUTHORITY_CHANNEL`.
- **Records read for a figure.**
  - **The twelve loop records** of `PLAN_REASONED_LOOP.md` and
    `PLAN_CHANNEL.md`: every escalation's calls, `O`, list, draft, answer and
    verdict, and every record's rules and `edge_log`, to rebuild its bases.
  - **`PLAN_CHANNEL.md`'s labels**, through `channel.plan.labels`, to find the
    bridge's rare tickets.
  - **The hidden policy's path**: `results_reasoned_loop/sample.json`'s and
    `results_channel/sample.json`'s reference to it.
- **Other sources.**
  - **The agreement on the provider**, of 2026-11-06, as `IDEAS.md` records it
    under *What `PLAN_CHANNEL.md` opens*.
  - **The listings read that day**, as the agent's notes keep them. They are not
    records of this repository.
  - **Which records name DeepInfra.** A search of `results_*/` for the
    `provider` field found it in `results_apply/` and `results_manual/`, from
    before the pin.

**Figures computed while drafting**, on 2026-11-07, from `d30d426` on `main`,
by scripts kept outside the tree. Stage A recomputes the first eight, and its
record will own them. None of them reads an answer this plan buys. Figures 1 to
4 read answers `PLAN_REASONED_LOOP.md` and `PLAN_CHANNEL.md` paid for, by masks.

1. **The new round's list on v1b's recorded rounds.**
   - **How it was read.** Each base was rebuilt in birth order, its edges tried
     after each birth in `edge_log` order, as `edges/rebuild.py` pairs them.
   - **The replay check.** At every one of the 878 rounds, the rebuilt base's
     `O` was the recorded one.
   - **What was set beside it.** Each listed rule was classed against its draft
     by masks, and each recorded answer was set against the list v1c would have
     sent.

   | plan | run | escalations | rounds | rules listed | inside the draft | containing it | equal to it | crossing it | of the crossing or equal, wholly governed | v1c's list | rounds v1c would not send | unplaced | of them, complete against v1c's list |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   | `PLAN_REASONED_LOOP.md` | i r1 | 41 | 29 | 113 | 11 | 0 | 0 | 102 | 13 | 89 | 2 | 3 | 1 |
   | | i r2 | 28 | 17 | 48 | 4 | 0 | 0 | 44 | 4 | 40 | 2 | 3 | 0 |
   | | i r3 | 18 | 17 | 34 | 0 | 0 | 0 | 34 | 0 | 34 | 0 | 2 | 0 |
   | | e r1 | 99 | 90 | 1,026 | 24 | 69 | 8 | 925 | 169 | 764 | 2 | 21 | 14 |
   | | e r2 | 120 | 113 | 1,392 | 127 | 87 | 21 | 1,157 | 243 | 935 | 6 | 28 | 15 |
   | | e r3 | 102 | 100 | 848 | 40 | 160 | 7 | 641 | 96 | 552 | 13 | 38 | 28 |
   | `PLAN_CHANNEL.md` | e r1 | 90 | 81 | 735 | 55 | 41 | 0 | 639 | 92 | 547 | 5 | 22 | 15 |
   | | e r2 | 95 | 87 | 799 | 61 | 48 | 10 | 680 | 162 | 528 | 4 | 14 | 8 |
   | | e r3 | 106 | 102 | 940 | 40 | 84 | 15 | 801 | 78 | 738 | 3 | 18 | 8 |
   | | c r1 | 79 | 68 | 502 | 9 | 53 | 3 | 437 | 29 | 411 | 4 | 16 | 12 |
   | | c r2 | 131 | 119 | 1,271 | 82 | 106 | 83 | 1,000 | 207 | 876 | 1 | 34 | 20 |
   | | c r3 | 62 | 55 | 478 | 27 | 46 | 1 | 404 | 60 | 345 | 3 | 9 | 3 |
   | | **all** | **971** | **878** | **8,186** | **480** | **694** | **148** | **6,864** | **1,153** | **5,859** | **45** | **208** | **124** |

   - **Every unplaced answer was answered.** At all 208, the placement call came
     back.
   - **The two exclusions apart.** Leaving out the nested rules alone would have
     made 122 answers complete, and left 42 rounds unsent. Leaving out the
     governed ones as well adds 2 complete answers and 3 unsent rounds.
   - **A rule wholly governed** is a crossing or equal one whose shared region
     with the draft is governed at every point, at listing (§2.2).
   - **`PL-a`'s reading on v1b's own answers.** The table's `refused(r)` is its
     unplaced count over its escalations.
     - `PLAN_CHANNEL.md`'s channel runs refused 16 of 79, 34 of 131 and 9 of 62
       escalations: a median of 16/79.
     - Against v1c's lists, 4 of 79, 14 of 131 and 6 of 62 would have been left:
       a median of 6/62.
     - The ratio is 474/992, 0.4778. It is read on v1b's trajectories, whose
       bases v1c's would not have kept.
2. **By the draft's queue**, over the twelve runs:

   | queue | unplaced | complete against v1c's list |
   |---|---|---|
   | `SECURITY_INCIDENT` | 26 | 17 |
   | `ONCALL_ESCALATION` | 14 | 3 |
   | `ACCOUNT_MANAGER` | 18 | 14 |
   | `T3_ENGINEERING` | 28 | 19 |
   | `T2_TECHNICAL` | 63 | 36 |
   | `SELF_SERVICE_DEFLECT` | 32 | 18 |
   | `T1_GENERAL` | 19 | 12 |
   | `BILLING_SPECIALIST` | 8 | 5 |

3. **The two rarest queues in `PLAN_CHANNEL.md`'s channel runs.**
   - **c r1's 9 unplaced answers on `SECURITY_INCIDENT`.**
     - **Taken.** v1c's lists would have taken those at cases 599, 770, 1063,
       1264, 1871 and 1961. They include the three broad drafts, at 1063, 1264
       and 1871.
     - **Left.** At 448, 580 and 751 the answers also left out crossing rules
       that v1c lists.
   - **c r1's one unplaced answer on `ONCALL_ESCALATION`**, at case 257, would
     have been taken.
   - **c r2's draft of `H04`'s region whole**, at case 1951, would not. It left
     out `R0022`, which crosses the draft and is not governed.
   - **The rest of the two queues' unplaced answers.** c r2's at 580 would have
     been taken. Its answer at 155, and c r3's at 402, 954 and 1432, left out
     crossing rules v1c lists.
4. **The breadth of drafts and births**, over the twelve runs.
   - **The drafts.** Of the 878 rounds, 247 had a draft that is its governing
     rule's region.
   - **Their refusals.** 54 of those 247 ended unplaced, 0.2186, against 154 of
     the other 631, 0.2441.
   - **The births.** Of the 664 births after a round, 193 were their governing
     rule's region.
   - **What v1c would have taken.** 37 of the 54 broad drafts' refusals.
5. **The hidden policy through v1c's path**, as `PLAN_REASONED_LOOP.md` §5.6 runs
   it through v1b's.
   - **The rounds.** All 29 rules are born. The 27 that meet a rule of another
     queue would have v1b list 253 rules; v1c lists 192 of them. It leaves out 54
     nested with their draft and 7 governed, and does not send 2 rounds.
   - **The edges.** 192 are installed, against v1b's 199.
   - **What it decides.** 134,400 of 134,400 points, and 2,000 of 2,000 cases.
6. **The transcriber through v1c's path.**
   - **Under each of `PLAN_CHANNEL.md`'s three draws** it escalates, compiles and
     decides exactly as under v1b:
     - 23, 22 and 23 escalations;
     - 134,380, 132,280 and 134,380 points;
     - 1,999, 1,996 and 1,999 cases.
   - **Its calls** are 42, 40 and 42, against 45, 43 and 45.
   - **Under the smoke draws**, over their 30 cases:
     - 9 escalations, and 16 calls against 17;
     - 49,420 points under both protocols;
     - its 8 rounds list 10 of v1b's 20 rules, and 1 round is not sent.
7. **The schedule.** `ORDER_SEED` draws v1c first, so the order is v1c r1, v1b r1,
   v1c r2, v1b r2, v1c r3, v1b r3.
8. **The bridge's tickets.**
   - **The seeds** were fixed by rule before any draw was computed (§11). These
     are the first and only draws computed under them; no seed was tried and set
     aside.
   - **The 20 of `SECURITY_INCIDENT`**: cases 44, 155, 342, 402, 448, 580, 599,
     676, 739, 751, 770, 1063, 1235, 1264, 1514, 1704, 1802, 1871, 1961 and 1998.
   - **The 7 of `ONCALL_ESCALATION`**: cases 257, 710, 954, 982, 1432, 1783 and
     1951.
   - **20 of the 27** escalated in some channel run of `PLAN_CHANNEL.md`.
   - **The 13 drawn** from the 175 other distinct tickets those runs escalated:
     - the cases are 18, 19, 29, 42, 55, 65, 265, 449, 513, 529, 658, 794 and
       881;
     - their queues are 4 of `T2_TECHNICAL`, 4 of `SELF_SERVICE_DEFLECT`, 2 each
       of `T3_ENGINEERING` and `BILLING_SPECIALIST`, and 1 of `ACCOUNT_MANAGER`.
   - **The order.** DeepInfra is asked first at 22 tickets, and Baidu at 18.

**[Added before signature, 2026-11-07] What writing the package showed.** The
package was written, and its checks run, before the signature, as §7 asks.

- **The code read** adds:
  - `channel/run.py`, `gates.py`, `sample.py`, `references.py` and `score.py`,
    whole;
  - `reasoned_loop/score.py`'s `read_run`, `placements_of`,
    `births_against_the_list` and `rare_of`, and `reasoned_loop/gates.py`'s
    `same_engine` and `hidden_policy`;
  - `authorship/run.py`'s `open_partial` and `Resumable`, and
    `first_match/ask.py`'s `Asker`;
  - `tests/test_channel.py`'s helpers and its tests of the gate, the trigger, the
    resume, the order of events and the smoke check, and the lists of
    `tests/test_writer_lists.py` and `tests/test_oracle_separation.py`.
- **`PL-g1` to `PL-g3` pass**, with the suite green, in `python3 -m
  placement.run --dry-run`. They print pass or fail, and every figure §0 declares
  that they read comes back as declared.
- **What `PL-g2`'s last check found.** 182 rules were left out on the hidden
  policy's path and the transcriber's v1c runs:
  - 61 on the path: 54 inside their draft and 7 governed;
  - 121 on the runs, the smoke draws' included.

  None of them changes which rules are undefeated at any point.
- **Stage A's reading was run in memory, and nothing was written.** Every one of
  figures 1 to 8 came back as declared, figure 4 included.
- **Stage C's scorer was run in memory on the transcriber's six runs**, to test
  the code, and nothing was written.
  - **`PL-a` has no value there**, as §0 provides: a proposer that never errs
    leaves no listed rule out, so v1b's median `refused(r)` is 0.
  - **`PL-b` to `PL-f` hold**, `PL-c` and `PL-f` thinly. `PL-c` is thin by
    construction. `PL-f` is thin because the transcriber recalls 2/3 of
    `ONCALL_ESCALATION` under run 2's draws.
- **OpenRouter's endpoint listing was read** (§2.8).
- **[Added before signature, 2026-11-07, later] What `PL-g` reads as a right
  edge refused for a cycle.** §0 named it and did not define it.
  - **The definition.** An edge the engine refused for closing a cycle is
    right when its declared winner is the better rule over the pair's shared
    region. That is `rung3/edge_direction.py`'s `verdict`, as `RL-e` reads a
    placed edge. Ties, regions neither rule is ever right on, and pairs of one
    queue are counted apart. It is read on the whole space and on the half
    without the keyword.
  - **Beside each**, the points of the shared region the final base leaves both
    rules undefeated on. Of those, it counts the ones where the winner's queue
    is the truth.
  - **Tested on `PLAN_CHANNEL.md`'s three channel runs.** It gives back that
    record's 5, 84 and 26 edges refused for closing a cycle. In c r2 it gives
    back the two edges over `R0075`, both right, and the 640 contested points
    `FINDINGS_CHANNEL.md` names.
  - **What it also showed**, which no record had published: 1, 44 and 14 of
    those edges are right on the whole space. `PL-g` reports them beside this
    plan's runs, and they inform no band.

**Not seen, because nothing has produced it:**

- any loop run under v1c, with any proposer but the transcriber;
- any call to DeepInfra under the pin. So DeepInfra's pace, its rate limits, its
  `provider` field and its reasoning are all unseen;
- any v1b run on DeepInfra, or on the new period;
- the bridge;
- any base either arm compiles here.

**What the drafter expects, written down so the scoreboard can score it.** **Five
hold and one is refuted.** The drafter trusts `PL-a` most, then `PL-b`, `PL-d`,
`PL-e` and `PL-c`, and expects `PL-f` to be refuted.

- **`PL-a` holds.** On v1b's own answers the ratio is 0.4778. 122 of the 124
  refusals v1c would take away are nested rules left out, as the system prompt
  says.
  - *Against it:* a proposer that reads `beats` and `loses_to` as containment
    will have nothing nested to place.
- **`PL-b` holds.** `CH-a` held at 0.9499, and v1c takes away the route by which
  c r1 lost `SECURITY_INCIDENT`.
  - *Against it:* a new provider, and c r2's weakness without the keyword,
    where its base decided 0.8997.
- **`PL-d` holds.** v1c changes nothing the transcriber compiles. The drafter
  expects it to raise the worst run, not to lower the median.
  - *Against it:* a spread between runs of 0.27.
- **`PL-e` holds, thinly.** `CH-a` held thinly, and c r1's loss can recur under
  v1b: whether the default comes before the broad drafts is partly the draft's
  draw.
  - *Against it:* the same draw may not come again, and the provider is new.
- **`PL-c` holds, and thinly, as every hold of it is.** Under c r1's draws, v1c
  would have taken the broad drafts c r1 drew.
  - *Against it:* all three runs must reach the line. A run can lose the policy
    by another route: a crossing rule left out, or a right edge refused for a
    cycle.
- **`PL-f` is refuted.**
  - *The reasons:*
    - the draws of run 2 cannot report `H05`;
    - on v1b's answers, v1c would have taken only 3 of the queue's 14 refusals;
    - c r2's draft of `H04`'s region whole would still have been refused.
  - *Against it:* v1c would have taken c r1's refusal at 257. And a run that
    writes `H05`'s region from an `H04` ticket needs no `H05` report.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 55 of 140 adjudicated rows were refuted.
- **The last two plans.**
  - `PLAN_CHANNEL.md`'s drafter expected five rows to hold and `CH-c` to be
    refuted, and that is how they came out.
  - `PLAN_REASONED_LOOP.md`'s drafter expected all seven rows to hold, and four
    did.
- **What was done about it, rather than said.**
  - **No development set.** No band here was set on one.
  - **Inherited lines.** Every line but `PL-a`'s is a closed thread's own:
    - `PL-b`'s, `PL-c`'s per run and `PL-e`'s are `CH-a`'s;
    - `PL-f`'s is `CH-c`'s;
    - `PL-d`'s is `CH-b`'s.
  - **`PL-a`'s line** is the midpoint of the two hypotheses it separates, as
    `CH-f`'s was.
  - **Thin, declared in advance.** A verdict one run carries is labelled *thin*
    in advance. `PL-c`'s holds are thin by construction, and `PL-f`'s dependence
    on two runs is declared above.

Sergi should read the bands as more likely too comfortable than too strict, and
tighten them at signature if he disagrees.

**How the rows read together.**

- **`PL-a`, `PL-b`, `PL-c` and `PL-d` hold.** The round's refusals were the
  protocol's, and listing only what the engine can still order takes them away at
  no cost. No run loses the policy. The defect `PLAN_CHANNEL.md` kept on purpose
  is then why its c r1 did.
- **`PL-a` holds and `PL-c` is refuted.** v1c takes the refusals away and a run
  still loses the policy. `PL-g` says by which route. The drafter expects a
  crossing rule left out, or a right edge refused for a cycle.
- **`PL-a` is refuted.** The proposer's omissions follow the list, not the texts:
  it leaves out a share of whatever is listed. The defect is then the proposer's
  reading of `beats` and `loses_to`, and a round that asks for less does not mend
  it.
- **`PL-d` is refuted.** The new round costs the policy. `PL-g` says where. It
  also says whether the change in the graph, the edges v1c never asks for, is
  where the cost came from.
- **`PL-e` is refuted.** v1b did not compile the policy again on the new period
  and provider. `PL-d` then reads against a weaker comparator. `PL-g` sets both
  periods side by side, with the bridge.
- **`PL-f` is refuted and `PL-b` holds.** The rarest queue needs more than the
  round, and `STATUS.md`'s third item stays at the supply of rare tickets.
- **`PL-f` holds.** For the first time, half the reports compile
  `ONCALL_ESCALATION` in the median run.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, under hard rule 4:

- **`results_channel/`**: `PLAN_CHANNEL.md`'s six runs, its Stage A, its Stage C
  and its two POST-RUN readings. Its draws are this plan's. `PL-g` sets its
  channel runs beside both arms.
- **`results_reasoned_loop/`**: `PLAN_REASONED_LOOP.md`'s six runs and its
  POST-RUN readings, which the drafting reading read.
- **`results_reuse/run_n2000_r{1,2,3}.json`**: the corpus labels, as
  `manual.instrument` and the trigger read them.
- **`results_manual/score.json`**: the rules compiled once, `C₃` (§3).

**Bought.** Two arms of three loop runs each, at n=2000. One smoke run of 30
cases under v1c. And the bridge: 40 first calls, each asked of two providers.

- **Every call goes through `PLAN_REASONED_LOOP.md`'s proposer.** So it also goes
  through `PLAN_FIRST_MATCH.md`'s asker and `harness/call_record.py`.
- **The request is that plan's in everything but the pin:**
  - the model, `deepseek/deepseek-v4-flash`;
  - temperature 0, and `response_format` on the first attempt;
  - reasoning `{"effort": "high"}` and 16,000 tokens.
- **The pins.** The runs carry DeepInfra's (§2.8). The bridge's Baidu asks carry
  Baidu's, `PLAN_QUEUE_ALONE.md`'s.

**The calls.** One per escalation, and a second when the placement round has
rules to list. What `PLAN_CHANNEL.md`'s channel runs made, read off its record:

| run | escalations | calls | from first launch to record |
|---|---|---|---|
| `c r1` | 79 | 147 | 1 h 33 min |
| `c r2` | 131 | 250 | 8 h 44 min, through three outages |
| `c r3` | 62 | 117 | 1 h 20 min |

- **Why a v1c run should make fewer calls than a v1b run.** A round whose list is
  empty is not sent: three a run, for the transcriber. And a refusal taken away
  is a draft born, not a ticket asked about again. Under the channel the better
  base also errs less, and so is reported less (`CHAT_SUMMARY.md` §1).
- **The smoke run measures DeepInfra's pace before the first run.** It rests on
  the few escalations 30 cases make, and the findings will say how far the
  estimate was.

**The cap.** A run stops at its 400th escalation, at most 800 calls. Its record
says so, its final base is the base at that case, and the rows read it as a run
(§0). No run of `PLAN_CHANNEL.md` came near it.

**The money.** **At DeepInfra's listing as read on 2026-11-06**, $0.09 per million
prompt tokens and $0.18 per million completion tokens:

- **The runs.** `PLAN_CHANNEL.md`'s three channel runs' tokens would have cost
  $0.11 to $0.26 a run there. So this plan's six runs should cost about a dollar.
- **The rest.** The bridge and the smoke run should cost a few cents more.
- **At the cap.** With every call spending its 16,000 tokens, the six would cost
  under fifteen dollars.
- **That listing is not a record of this repository.** The price is read off the
  smoke run's bills, by generation id, before the first run, and the findings
  give the bills.

**The time.** `PLAN_CHANNEL.md`'s channel runs that met no outage took 1 h 20 min
and 1 h 33 min on Baidu.

- **DeepInfra's pace is unknown**, and the smoke run measures it.
- **If it is Baidu's**, the six runs take about eight to twelve hours, one after
  another, and the bridge about an hour.
- **§5.4 says how a run waits out a refusal and resumes**, and §2.7 where the runs
  are launched.

**What is not bought.**

- **The error arm or the impasse arm under v1c.** Sergi chose the channel.
- **The two exclusions apart.** One arm carries both. The drafting reading
  apportions the refusals between them, and Stage C classes every round by what
  each left out. What each does to the graph is not separated (§13).
- **Another coverage, a delay, noise or asymmetry.**
- **A round that accepts a partial placement**, leaving an unplaced pair to
  conflict (§2.3).
- **Placement prompts in the bridge.** It asks first calls only (§2.6).
- **Any other level, screen, model, effort or budget.**

---

## 2. The choices that have to be made at signature time

Each is the drafter's recommendation, and each is Sergi's to overrule. A choice
that changes a row is a change to §0, and belongs in the same signed commit. The
two choices Sergi made before the drafting, the arms and what the list leaves
out, are not repeated here.

### 2.1 Every text is v1b's, byte for byte — the drafter recommends it

v1c sends v1b's four texts: the system prompt, the user message, the placement
message and the retry message. It fills the placement message with its own list.

- **The first line stays true.** *"Tu regla se solapa con estas reglas existentes
  de OTRA cola"* is true of every rule v1c lists.
- **It is no longer exhaustive.** It is not true of every rule the draft meets.

**The alternative** adds a sentence to the placement message: that the list
leaves out the rules nested with the draft, and the conflicts the base already
decides. It would make the arms differ in a text as well as in a list.

### 2.2 Governed is read at listing, with the draft's containment only — the drafter recommends it

Take the draft `D` and a rule `R` of `O`. A point of their shared region is
governed at listing when both hold:

- a rule of the base other than `R` matches the point, and its extension lies
  strictly inside `D`'s, so it beats `D` there by containment;
- a rule of the base other than `D` matches the point and beats `R`, by
  containment or by a declared edge.

Before its answer, containment is the only relation `D` has. This is
`reasoned_loop/governed.py`'s *at listing*, read over the whole space rather than
over the half without the keyword.

- **A rule that is defeated still defeats**, because the engine reads every
  matched rule's edges. So one third rule beating `R` is not enough. `D` must be
  beaten there too.

**The alternative** would also count the edges the answer is about to declare.
The round cannot know them before it asks.

### 2.3 A listed rule left without a side still refuses the birth — the drafter recommends it

v1c changes the list and keeps v1b's validator. If the answer leaves out a rule
v1c lists, it is still unplaced, and the rule is not born. That is c r2's draft
of `H04`'s region at case 1951, which v1c would still have refused.

**The alternative** would install the rule with the sides it gave, and leave each
unplaced pair to conflict where both rules match, to escalate there later. That is
`ARBITRATION_REPORT.md` §7's P2, deferred elicitation, brought to the moment of
writing. It would be a second change, and another plan.

### 2.4 Three runs an arm, the arms alternating, and the cap — the drafter recommends it

- **Three runs** is `PLAN_CHANNEL.md`'s count.
- **The order.** `ORDER_SEED` draws which arm runs first, and then the arms
  alternate, one run of each in every repetition. Run `k` of both arms reads the
  draws of `c r{k}`. If Stage B spans two days or more, both arms have runs on
  each.
- **The cap** is 400 escalations a run, as `PLAN_CHANNEL.md`'s.

### 2.5 The smoke run is 30 cases under v1c, on DeepInfra — the drafter recommends it

v1c and the provider are this plan's two new paths. The smoke run reads
`PLAN_CHANNEL.md`'s smoke draws, and must show, before the bridge and the first
run:

- every attempt that reached the model served by DeepInfra, reasoned, and ended
  `stop`, with the `provider` field it carries;
- the rate limits it met, and the waits they cost;
- a rule born, a placement round answered, and a round that left a rule out for
  being nested or governed. Under the smoke draws the transcriber's eight rounds
  list 10 of the 20 rules v1b lists, and one is not sent;
- the trigger's record: for every wrong decision, its draw and whether it
  escalated.

**The alternative** smokes v1b on DeepInfra. `PLAN_CHANNEL.md`'s smoke run
already tried that path, on Baidu.

### 2.6 The bridge is 40 first calls, asked of each provider once — the drafter recommends it

The agreement of 2026-11-06 asks for *a small same-day bridge: some prompts asked
of Baidu and of DeepInfra, to measure what the provider changes*.

- **What it asks.** The first call is blind. For a given ticket it is one request
  in every run, in either arm, on either provider: level 3's system prompt and
  the ticket under `BLIND_BASE`. It is also where a draft's breadth is drawn. So
  the bridge asks first calls.
- **Which tickets.**
  - **The 27 of the two rarest queues.** `PLAN_CHANNEL.md`'s runs lost points of
    both.
  - **13 drawn by `BRIDGE_SEED`** from the other distinct tickets that
    `PLAN_CHANNEL.md`'s channel runs escalated.
  - **The recorded drafts.** 20 of the 27, and all of the 13, have a draft
    recorded by those runs on Baidu.
- **When.** Once the smoke run is read, and before the first run. The two
  providers alternate ticket by ticket, in an order `BRIDGE_SEED` draws.
  - **An outage.** A call refused for the rate through every wait stops the
    bridge unrecorded. It resumes from its partial file between runs, never
    beside one.
  - **Its record** gives each ask's hour.
- **What it reads.** Reported, in `PL-g`:
  - each answer's queue against the label;
  - its extension against the governing rule's region;
  - the two providers' answers against each other;
  - Baidu's against the drafts `PLAN_CHANNEL.md` recorded for the same tickets.

**The alternatives**, neither recommended:

- **Each prompt twice of each provider**, which would set a provider's spread
  beside the providers' difference. It doubles the bridge.
- **Placement prompts as well, rebuilt from `PLAN_CHANNEL.md`'s records.** They
  would rest on a rebuild of the bases, not on the recorded request.

### 2.7 Where the runs are launched — Sergi's choice; the drafter has no recommendation

- **In Sergi's terminal**, where a run outlives no harness.
- **Or by the agent, at Sergi's request, detached from its harness**, as
  `PLAN_REASONED_LOOP.md`'s and `PLAN_CHANNEL.md`'s runs were. A supervisor:
  - runs them one at a time, and resumes a run an outage has stopped;
  - commits each record before the next run starts;
  - retries a failed push and goes on;
  - never passes the overwrite flag.

Either way the order is §2.4's, and no two runs are ever side by side.

### 2.8 The pin is DeepInfra's fp8 endpoint — by the rule agreed on 2026-11-06

The pin is `{"order": ["deepinfra/fp8"], "allow_fallbacks": false}`, and nothing
falls back across providers.

**Before the signature, the package reads OpenRouter's endpoint listing for the
model**, which spends nothing. The listing must name a DeepInfra endpoint at fp8,
under that tag, that takes the 16,000-token budget and reasoning.

- **[Done before signature, 2026-11-07]** The listing names DeepInfra's endpoint
  under `deepinfra/fp8`, at fp8. It takes `reasoning` and `response_format`, and
  up to 393,216 completion tokens, at $0.09 and $0.18 per million prompt and
  completion tokens.
- **The same listing gave Baidu's endpoint**, `baidu/fp8`, at $0.04424 and
  $0.08848 that day: its price had fallen back since 2026-11-06.
- **Both were read that day**, and neither is a record of this repository.

If the listing had not named that endpoint, the alternatives were:

- **Another fp8 endpoint listed on 2026-11-06**, GMICloud's or StreamLake's, with
  the same bridge.
- **Baidu for both arms.** It would keep the rows inside the provider of the
  earlier plans and make the bridge unnecessary. But Baidu refused for the rate
  through most of 2026-11-06, UTC.

**The prices of 2026-11-06**, as read that day and not as records of this
repository, per million prompt and completion tokens:

- DeepInfra: $0.09 and $0.18;
- GMICloud: $0.091 and $0.182;
- StreamLake: $0.083 and $0.165;
- Baidu: $0.14 and $0.28.

### 2.9 Everything else is `PLAN_CHANNEL.md`'s, as signed

All of this is `PLAN_CHANNEL.md`'s, §2.6 and §5.3:

- the first call is blind at every escalation;
- a refused rule is not born, and a copy is born;
- the reasoning setting is `PLAN_FIRST_MATCH.md`'s, on both calls;
- a failed call is retried by cause, and a call refused for the rate is waited
  out;
- a run resumes from its partial file.

Changing any of them would make this plan's v1b arm another arm than that plan's
channel arm.

### 2.10 `PREDICTION.md`

Not touched. It is rung 1's long run, and this plan is not it (hard rule 2).

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan. `PL-g1` recomputes what it checks against
its record, rather than publishing it again.

| figure | value | owning record |
|---|---|---|
| the 29 rules compiled once, `C₃` | 1.0000 of the space, in every ask (`G-a`) | `results_manual/score.json`, published by `FINDINGS_MANUAL.md` |
| `PLAN_CHANNEL.md`'s channel arm, 2026-11-05 and 06 | `space` 0.7201, 0.9499 and 0.9872, median 0.9499 (`CH-a`, held thinly); `recall_ONCALL` 2/3, 128/315 and 14/15, median 2/3 (`CH-c`, refuted thinly); `recall_SECURITY` 0.3238, 1 and 0.9746; calls 147, 250 and 117 | `results_channel/score.json`, published by `FINDINGS_CHANNEL.md` |
| its error arm | `space` 0.9798, 0.9811 and 0.9868, median 0.9811 (`CH-d`, held) | same |
| its placement rounds | 113 of its 563 escalations unplaced; lists of a median of 5 to 9 rules by run; 1, 5 and 1 edges against containment in the channel runs | same |
| c r1's loss | 34,080 of `SECURITY_INCIDENT`'s 50,400 points lost, 0.9014 of them unwritten; 9 of the queue's 13 escalations unplaced, 8 of them leaving out the keyword's default | `results_channel/lost.json`, published by the same |
| c r2's loss on `ONCALL_ESCALATION` | 1,640 of the 4,200 points its draws let it reach: 1,000 never written, and 640 contested behind two right edges refused for closing a cycle | `results_channel/oncall.json`, published by the same |
| `PLAN_REASONED_LOOP.md`'s unplaced answers | 56 of 95 unplaced escalations left out only nested rules; a nested rule was left out 0.3867 of the times it was listed, a crossing one 0.0537 | `results_reasoned_loop/unplaced.json`, published by `FINDINGS_REASONED_LOOP.md` |
| the governed share of its error arm's pairs | 0.2879 of the strict pairs' shared region governed at listing, and 0.1277 by the answer, on the half without the keyword | `results_reasoned_loop/governed.json`, published by the same |
| the transcriber under `PLAN_CHANNEL.md`'s draws, through v1b | 23, 22 and 23 escalations; 45, 43 and 45 calls; 134,380, 132,280 and 134,380 points | `results_channel/sample.json`, published by `FINDINGS_CHANNEL.md` |
| the hidden policy through v1b's path | 29 rules born, 253 declarations, 199 edges, 1.0000 on both surfaces | `results_channel/sample.json` and `results_reasoned_loop/sample.json` |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** This plan reads `harness/domain.py`
   and `harness/ceiling_check.py`, and edits no frozen file. Under `harness/` it
   touches only `provenance.py`'s list of code roots, which is plumbing (§11).
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A signed
   plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Each run is strictly sequential: a rule born at case
   `t` decides case `t+1`. The runs go one after another, never side by side, and
   each run's record is committed before the next starts. The bridge is never
   asked beside a run.
4. **Seed 17, no regeneration.** Every record under `results_channel/`,
   `results_reasoned_loop/`, `results_manual/` and `results_reuse/` is
   read-only. `harness/record_guard.py` guards this plan's paid records, and the
   flag that overrides it is not typed without Sergi asking.
5. **Do not adjust a prompt, a text or the schema.** Every text is
   `PLAN_REASONED_LOOP.md` §5.1's, byte for byte, in both arms, and `PL-g2`
   checks each by digest. Once the smoke run has been read, nothing moves.
6. **If the numbers come out badly, report them.** A round that takes no refusal
   away is a result, and so is a v1b arm that does not compile the policy again.
7. **The API key goes in the environment.** It is loaded without printing,
   checked by its length, and read off OpenRouter's key endpoint as an API key
   and not a management key before any call (`reuse.run.key_check`).

And this plan's own, lettered:

A. **Called and not edited:** `channel/`, `reasoned_loop/`, `first_match/`,
   `queue_alone/`, `blind/`, `authorship/`, `manual/`, `reuse/`, `edges/` and
   `rung2/`.
   - **v1b's escalation** is `reasoned_loop.loop.propose_v1b`, called.
   - **v1c's escalation** is this plan's: `propose_v1b`'s steps, copied, with
     the list changed. With both exclusions turned off it gives back
     `propose_v1b`'s record, and `PL-g1` holds it to that.
   - **The loop** is `channel.loop.run_loop`, copied with the escalation as an
     argument, because that function names its own. Under v1b, served run
     `c r1`'s answers, it gives back that run's record case for case (`PL-g1`).
   - **The trigger and the draws** are `channel/`'s: `channel.loop.escalates`
     and `channel.plan.draws`, called.
   - **The transcriber** is `reasoned_loop.references.Transcriber`. The
     instrument is `manual.instrument`'s.
   - **The asker** is `reasoned_loop.protocol.Asker`, subclassed with a pin of
     the caller's choosing in its request, and nothing else changed.

B. **No label reaches a prompt.**
   - **The trigger reads the corpus labels, handed in**, as `PLAN_CHANNEL.md`'s
     did: from `PLAN_REUSE.md`'s records, never from the oracle.
   - **v1c's list reads the base and the draft, and nothing else**: extensions,
     containments and declared edges. It reads no label, no draw and no policy.
   - **No module on the proposer's path imports the oracle.**
     - That path is `placement/protocol.py`, `placement/loop.py` and
       `placement/run.py`, with the modules they call.
     - None of them imports by name the oracle, `HIDDEN_DSL`,
       `harness.ceiling_check`, `rung2.hidden_priority` or `rung4.feedback`.
     - All three join `ONLINE_LOOP` and the authority channel's watch.
   - **The draws read no label.** They are `PLAN_CHANNEL.md`'s, drawn from its
     seed strings alone.

C. **Every record carries `_env`**, with:
   - the model, the temperature, the reasoning setting, the token budget and the
     provider pin;
   - the protocol, the arm, the run, the coverage, the draws' seed string and
     their digest, and the digests of the four texts;
   - every call's `call_attempts`, and the cause of every retry;
   - for every round of either arm, `O`. For v1c, also its list, and every rule
     left out with its reason: inside the draft, containing it, or governed.

   Every command runs with `PYTHONHASHSEED=0` set explicitly.

D. **The constants of §11 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.

E. **What the model writes is recorded whole**, as `PLAN_REASONED_LOOP.md`'s rule
   E says: every call's payload with its keys in the order written, and its
   reasoning. No stage codes a note or the reasoning.

F. **The order of Stage B is §9's**, and the module refuses a run out of it.

G. **The provider is pinned on every call.** The smoke run and the runs carry
   DeepInfra's pin, and each half of the bridge its own provider's. A call that
   another provider served is recorded and counted, and its answer still decides
   its case, as in `PLAN_REASONED_LOOP.md`'s rule G.

H. **A failed call is never answered with v1's retry message.** Only a failed
   parse is (`PLAN_FIRST_MATCH.md`'s rule).

I. **The trigger reads the truth, and nothing else decides by it.**
   - **The engine** never decides by a label, and v1c's list reads none.
   - **The proposer** never sees a label, and is never told that the base erred,
     in either arm.
   - **The loop** also reads the label to score what was decided, into the
     record, as rung 2's loop always has (`PLAN_CHANNEL.md`'s rule I, as
     corrected before its signature).

---

## 5. The protocol

### 5.1 v1b, unchanged

The v1b arm's texts, escalation, placement round and validator are
`PLAN_REASONED_LOOP.md` §5.1 and §5.2's. They are called from `reasoned_loop/`,
not copied. Its trigger is `PLAN_CHANNEL.md`'s channel arm.

### 5.2 v1c: the list

At an escalation, the first call is v1b's: blind, and the same request. Suppose
the draft is a valid rule that matches its ticket. Let `D` be its extension and
`a` its queue, read on the base as it stands before the draft is born.

- **`O`** is v1b's: every rule of the base whose queue is not `a` and whose
  extension meets `D` (`overlap.protocol.split_overlapped`). Rules of `a` are
  never listed, in either arm.
- **v1c's list** holds each rule `R` of `O` for which both of these hold:
  1. **Neither contains the other strictly.** `R`'s extension is not strictly
     inside `D`, and `D` is not strictly inside `R`'s. A rule equal to the draft
     stays: containment cannot order two equal extensions, and only a declared
     edge can.
  2. **Their conflict is still open somewhere.** Some point of `R ∩ D` is not
     governed at listing, as §2.2 defines it.
- **The order of the list** is v2b's seeded order: `blind.protocol.listing`,
  with `LISTING_SEED`.
- **An empty list sends no placement call.** The draft is born at once with no
  declaration. Every citation its first call carried is dropped, as under v1b
  when `O` is empty.
- **Otherwise the round is v1b's, over v1c's list.** The placement message is
  `PLACEMENT_TEMPLATE`, filled by `blind.protocol.placement_message` with v1c's
  list. The answer must:
  - be a rule that passes rung 2's validator and matches the ticket;
  - be the draft's rule (`blind.protocol.same_rule`);
  - give a side to every listed rule.

  A citation of a rule not listed is dropped before `try_edge`, as v1b drops
  one. A refused rule is not born, and the case keeps the proposer's last answer
  as its decision.
- **What the record keeps of the round**: `O`, v1c's list, and each rule of `O`
  left out, with its reason. It keeps the answer and the rules it left without a
  side, as v1b's record does.

**Why the two exclusions decide nothing.**

- **A nested rule.** By `try_edge`, a side that puts the narrower rule on top is
  accepted as redundant and installs no edge. One that puts it below is refused
  as contradicting containment. Containment orders the pair whichever side is
  given.
- **A governed rule.** Once a point is governed it stays governed, because no
  rule and no edge ever leaves the base. At every point of `R ∩ D`, a third rule
  beats each of the two. So an edge between them never changes which rules are
  undefeated there.
- **What `PL-g2` checks of both, before any figure exists.** It takes the hidden
  policy's path and the transcriber's runs, and classifies each rule v1c leaves
  out as above. Then it adds each omitted edge to the final base, either way
  where the engine would take it. Every decision of the base must stay as it was,
  at every point of the space. That is `EXTERNAL_REVIEW.md` §4.2's practice for
  a control's invariants: proved, then checked over all 134,400 points.

### 5.3 The trigger

Both arms run `PLAN_CHANNEL.md`'s channel arm, called and not copied
(`PLAN_CHANNEL.md` §5.2, with its corrections before signature).

- **What it is.** `channel.loop.escalates`, at coverage 1/2.
- **Its draws.** `channel.plan.draws("r{k}")` for run `k`, and
  `channel.plan.draws("smoke")` for the smoke run.
- **What it does.** A wrong decision whose draw is below 1/2 escalates as an
  `ERROR`. One whose draw is 1/2 or above stands, and its rule is counted as
  fired.

### 5.4 What a run records, and how it resumes

- **What it records** is `PLAN_CHANNEL.md` §5.3's record, with the protocol. For
  v1c it adds §5.2's record of every round.
- **How it resumes** is `PLAN_REASONED_LOOP.md` §5.5's, with both its signed
  amendments, called and not copied.
  - **A call refused for the rate on every attempt is waited out**, after each
    wait of `RATE_LIMIT_WAIT`.
  - **Once every wait is spent, it is an outage.** The run stops unrecorded, and
    the same command resumes from the git-ignored partial file.
  - **A call served from the partial file keeps the seconds the file kept.**
- **The partial file's header carries the protocol and the draws**, so a run
  cannot resume under another of either.
- **Both are tested before the first run**, on runs built by hand, as `CLAUDE.md`
  asks of a plan whose runs resume.

### 5.5 The bridge

- **The prompts.** The first call of each of §0's 40 tickets:
  `reasoned_loop.protocol.messages_for(case)`, level 3's system prompt and the
  ticket under `BLIND_BASE`. It is the request both arms send at that ticket.
- **The asks.** One to Baidu, under `PLAN_QUEUE_ALONE.md`'s pin, and one to
  DeepInfra, under this plan's. Otherwise each is `PLAN_REASONED_LOOP.md`'s
  request:
  - reasoning on, 16,000 tokens and temperature 0;
  - `response_format` on the first attempt;
  - the retry by cause, and the waits.
- **The order.** Ticket by ticket, in case order. `BRIDGE_SEED` draws which
  provider is asked first at each ticket.
- **The record**, `results_placement/bridge.json`, keeps each answer whole: its
  payload with its keys in order, its reasoning, its `call_attempts` and its
  hour.
- **It decides nothing.** No row reads it, and nothing it answers reaches a run.

### 5.6 The references Stage A computes

- **The transcriber** runs through this plan's loop under both protocols, with
  each run's draws and the smoke run's. It shows what each protocol, and each
  draw, allows a proposer that never errs (§6.13).
- **The hidden policy through both paths**, as `PLAN_REASONED_LOOP.md` §5.6 runs
  it through v1b's.
- **The drafting reading**, §0's figures 1 to 4, recomputed from the records.

---

## 6. Known traps

**6.1 — Every error escalation is told it is an impasse.** v1 calls the model the
system's exception component, and the user message labels the ticket *TICKET EN
IMPASSE*. On an error escalation both are false: the engine decided, wrongly.
Both arms keep the prompts, so that the list is their only difference
(`PLAN_CHANNEL.md` §6.1).

**6.2 — Level 3 hands over the label** (`PLAN_MANUAL.md` §6.2). Every row
measures what the loop compiles from a policy it holds as text.

**6.3 — The trigger reads the truth.** The channel asks where its base is wrong
and a draw says the error was reported. In a deployment the report comes from the
world. Here the corpus labels stand in for it, as rung 4's channel read the
oracle.

**6.4 — The online figures are corrected online.** A reported error's decision is
replaced by the proposer's answer, and an unreported one stands. They are
reported, and no row reads them.

**6.5 — The draws fix which cases can be reported, not which are.** Run `k` of
both arms reads one set of draws, so a case reportable in one is reportable in
the other.

- **What still differs.** Which of those cases the base decides wrongly depends
  on the base. The bases part from the first refusal one arm makes and the other
  does not.
- **So the pairing** takes the channel's luck out of the contrast between the
  arms. It does not make the runs replicas.

**6.6 — `SECURITY_INCIDENT` weighs 3/8 of the space.** `space(B)` moves with its
recall more than with any other queue's. Every space figure in `PL-g` is split by
the keyword, as `PLAN_UNREACHED.md`'s findings ask.

**6.7 — v1b's two defects are kept in the v1b arm.** It lists rules nested with
the draft and rules whose conflict the base already decides, and pays for both in
refusals.

**6.8 — v1c's list is shorter, and the placement message does not say so.**
*"Tu regla se solapa con estas reglas existentes de OTRA cola"* is true of every
listed rule. A proposer may read the list as every rule the draft meets. It can
cite no other under either protocol, because a citation outside the list is
dropped.

**6.9 — A round whose list is empty is not sent.** The draft is born at once and
the first call's citations are dropped, as under v1b when `O` is empty. So v1c
makes fewer calls by construction: three a run, for the transcriber. `calls(r)`
reads that, and no row adjudicates it.

**6.10 — Governed at listing is a floor.** It counts the draft's containments
and the base's relations, not the edges the answer will declare (§2.2).

- **What v1c leaves out for governance** could never decide a point.
- **What it lists** could still decide none: a rule whose conflict the answer
  itself settles is still listed.

**6.11 — A rule left out still matters to cycles.** An edge v1c never asks for
never enters the graph `try_edge` searches when it refuses an edge for closing a
cycle.

- **The cycle check is global, and the decision is local.** `try_edge` follows
  every edge and every containment, through any rule. `decide` reads only the
  rules that match the case.
- **So an edge that decides nothing** can still make a later edge close a cycle,
  right or wrong.
- **v1c changes the graph as well as the asks.** Its effect on the refused edges
  is read in `PL-g`, never adjudicated.

**6.12 — c r1's loss was partly the draft's draw.** There, the keyword's default
came before any broad draft of `SECURITY_INCIDENT`. The same ticket draws
different drafts in different runs. So the v1b arm may lose no queue at all, and
`PL-c` reads v1c's runs alone for that reason.

**6.13 — What the transcriber is not.** It writes the governing rule and places
it right every time, so it never leaves a listed rule out. Under v1c it compiles
what it compiles under v1b, in fewer calls. It bounds nothing about the model.
It shows what each protocol and each draw allow a proposer that never errs.

**6.14 — A new provider for the loop.** No call of this loop has gone to DeepInfra.

- **What may differ.** It may honour temperature 0 differently while the model
  reasons, and its rate limits are unknown. Its fp8 is not Baidu's fp8.
- **What reads within it**: the rows. Every comparison with the earlier plans
  crosses it.
- **What measures it.** The smoke run and the bridge measure what they can, and
  each run's values are published.

**6.15 — The bridge reads first calls only.** A provider's placement answers,
where `PL-a` acts, are not bridged. `PL-a` reads within one provider, and needs no
bridge.

**6.16 — Back-to-back runs leave `git_dirty` true**, because each finds the
earlier records not yet committed. Rule 3 of §4 commits each record before the
next run, and `code_dirty` is what identifies the code.

**6.17 — A resumed record's `started_at` is its last launch's.** A run's span is
taken from its first launch, as `PLAN_CHANNEL.md`'s findings do.

**6.18 — What the runs' commits may show.** A supervisor's commit message written
from a record can print a row's inputs.

- **What may show.** Each run's message may give its escalations, its calls, its
  verdicts by kind and its rounds sent. So it may give `refused(r)`'s counts,
  which are `PL-a`'s inputs.
- **What may not.** No message gives a base's `space`, a recall or a ratio, and
  none is computed before Stage C.
- **What the findings do.** They name what was seen before Stage C.

**6.19 — A refusal taken away can be an error born.** Under v1b a refused draft
leaves its ticket's region to escalate again. Under v1c the draft is born. If it
is wrong, its decisions are wrong silently until the channel reports one, which
it does half the time.

- **Which warning this is.** `ARBITRATION_REPORT.md` §7's third objection to P1
  warns of turning a visible rejection into a silent error.
- **What `PL-g` counts.** Every v1c birth whose round left a rule out, by
  whether its queue is right.
- **What the rows read.** `PL-b` to `PL-f` read the truth over the space, so what
  such births cost is in them.

---

## 7. Blocking checks, before any record is written

All are free and all run by `--dry-run`. **Any failure stops the plan before a
figure exists.**

**PL-g1 — The inputs reproduce themselves.** Blocking in the sense of
`harness.ceiling_check`.

- **The suite.** `python3 -m unittest discover` is green.
- **`PLAN_CHANNEL.md`'s verdicts.** `CH-a` to `CH-f` come back from its records,
  through its scorer, called and not copied.
- **This plan's loop under v1b is `PLAN_CHANNEL.md`'s channel arm.** A replay
  double serves run `c r1`'s answers, each at the case and round that run asked
  for it, and refuses any other call. Under it, this plan's loop under v1b gives
  back that run's record case for case: its rules, causes, verdicts and edges.
  - **[Corrected before signature, 2026-11-07] How the check reads that.** A paid
    record's seconds cannot be replayed. So the check runs both loops on the
    replay, this plan's under v1b and `channel.loop.run_loop`, each with a clock
    that reads 0. It holds their records to each other, part by part.
  - **It also holds the replay to the run**: its rules and causes are `c r1`'s,
    case for case. That is how `PLAN_CHANNEL.md`'s `CH-g1` reads its own replay.
- **v1c with both exclusions turned off is v1b.** On the same replay,
  `propose_v1c` gives back the same record.
  - **[Corrected before signature, 2026-11-07]** The same record but for the one
    key v1c adds to a first call's row, `left_out`. The check takes that key out
    before it compares.
- **The draws are `PLAN_CHANNEL.md`'s.** Each run's draws and the smoke run's,
  rebuilt through `channel.plan`, have the digests that `PLAN_CHANNEL.md`'s
  records carry.
- **The labels.** The corpus labels the trigger reads agree with
  `manual.instrument.corpus_truth` on every case.
- **No float decides a check.** Values are compared as fractions, and counts as
  integers.

**PL-g2 — The protocol is §5's.**

- **The texts.** Each of the four matches `PLAN_REASONED_LOOP.md` §5.1's source
  by digest, in both arms.
- **The requests.** Checked through `tests/doubles.py`'s SDK double:
  - the reasoning setting, the budget and temperature 0;
  - `response_format` on the first attempt;
  - the pin: DeepInfra's for the runs, and each provider's for the bridge.

  Every key but the pin is `reasoned_loop.protocol.Asker`'s.
  - **[Corrected before signature, 2026-11-07] Where each half is read.** The
    gate reads the request off `placement.protocol.request_with`. That calls
    `reasoned_loop.protocol.Asker`'s request without building a client, and
    the gate compares every key but the pin.
  - **The SDK double** sends the request in `tests/test_placement.py`, which
    `PL-g1`'s suite runs. `PLAN_CHANNEL.md`'s requests were checked the same way,
    in that plan's tests.
- **v1c's list on v1b's recorded rounds** gives back §0's figures 1 to 3.
- **The hidden policy through v1c's path** gives back §0's figure 5. Through
  v1b's path it gives back its 199 edges and 1.0000 on both surfaces.
- **The transcriber** gives back §0's figure 6 under both protocols.
- **What v1c leaves out decides nothing.** This is checked on the hidden policy's
  path and on the transcriber's runs.
  - **The classes.** Every rule a round left out is nested with its draft or
    governed at listing, as §5.2 defines them.
  - **The edges.** Adding each omitted edge to the final base, either way where
    `try_edge` would take it, leaves `decide` unchanged at every point of the
    space.
  - **[Corrected before signature, 2026-11-07] It is read through the
    undefeated sets, which is stronger.** An omitted edge `try_edge` would take
    changes which rules are undefeated only where both rules match and the loser
    is not already beaten. The check finds no such point. Undefeated sets that do
    not move are decisions that do not move.

**PL-g3 — The schedule is §2.4's and §9's.**

- The six runs' order is rebuilt from `ORDER_SEED`.
- The smoke run is 30 cases under v1c, with `PLAN_CHANNEL.md`'s smoke draws.
- The bridge's tickets and its order of providers are rebuilt from
  `BRIDGE_SEED`, and are §0's figure 8.
- The cap is 400 escalations.

**PL-g4 — The signature**, §11.

---

## 8. Stage A — the references (free, gated)

**Deliverable.** `placement/sample.py` → `results_placement/sample.json`.

- **`PL-g1` to `PL-g3`.**
- **The references, recomputed and owned by this record:**
  - §0's figures 1 to 8;
  - the transcriber under both protocols and every draw;
  - the hidden policy through both paths.

**It produces nothing adjudicable.** It runs after §0 is signed, so that a figure
§0 did not declare cannot inform a band. If one of §0's declared figures does not
come back, Stage A's findings carry an erratum to §0, dated, and no band moves.

## 9. Stage B — the runs (gated on §0)

**Deliverable.** `placement/run.py` writes, in order:

1. `results_placement/loop_smoke.json`;
2. `bridge.json`;
3. the six runs, `loop_{v1b,v1c}_r{1..3}.json`, in §2.4's order.

**Each record is committed before the next run starts.**

**Before any call, for every run and for the bridge:**

1. **`--dry-run`** runs `PL-g1` to `PL-g3` and stops. It builds no client and
   needs no key.
2. **The signature (`PL-g4`).** While `PLAN_PLACEMENT.md` carries a blank
   signature line, the module exits here.
3. **What comes before it.**
   - **Stage A's record.**
   - **For the bridge and the runs, the smoke record**, with what §2.5 asks of
     it.
   - **For a run, every run before it** in §2.4's order. The bridge is not
     waited for (§2.6).

   If the smoke run fails, nothing after it starts, and what would change is a
   signed amendment.
4. **The key**, by `reuse.run.key_check`, called rather than copied.
5. **`PL-g1` to `PL-g3`, blocking.**
6. **The destination.** A paid record is never overwritten.
7. **The client, and the calls**, sequential, under hard rule 3.

**The smoke run's pace, rate limits and bills are reported before the bridge and
the first run**, by call and by round. They decide nothing, and no row reads the
smoke run's answers.

## 10. Stage C — scoring, and the six adjudications (free)

**Deliverable.** `placement/score.py` → `results_placement/score.json`, and
`results_placement/FINDINGS_PLACEMENT.md`, which owns every figure.

- **`PL-a` to `PL-f`**, each against its line, exactly. Each carries *thin* and
  *unadjudicable* as §0 defines them.
- **Each row's per-run values**, never summed into the verdict.
- **`PL-g` in full**, and the bridge with it.
- **The runs themselves:**
  - failed calls, refusals by verdict, and answers from another provider;
  - retries by cause, and attempts refused for the rate;
  - reasoning tokens over the attempts that reached the model;
  - the pace by run and by round, over the calls that met no refusal as well as
    over all.

---

## 11. The gate, and where the code lives

**Every module of this package that writes a record refuses while §0 is
unsigned.**

- **What spends.** `placement/sample.py` and `placement/score.py` spend nothing.
  `placement/run.py` refuses before it constructs a client.
- **Why the free stages get the gate too.** What it protects is the order of
  events, not money. A record of this plan written before the signature would be
  a figure that existed before its band.

**The gate reads `PLAN_PLACEMENT.md` and no other plan, and it counts every
signature line.** It calls `reuse/plan.py`'s counting with this plan's path and
minimum. `MIN_SIGNATURES = 1` today, for §0. An amendment carries its own line
and raises it. No flag skips the gate.

**Constants fixed here, before any figure exists, not to be tuned afterwards, and
pinned by tests:**

- **The client.** Imported from `reasoned_loop/plan.py`, and so from
  `first_match/plan.py`, and not retyped:
  - `MODEL`, `TEMPERATURE`, `REASONING` and `MAX_TOKENS`;
  - `MAX_RETRIES` and `CALL_RETRY_WAIT`;
  - `RATE_LIMITED` and `RATE_LIMIT_WAIT`.
- **The pins.**
  - **This plan's.** `PROVIDER = {"order": ["deepinfra/fp8"], "allow_fallbacks":
    False}`, and `PROVIDER_NAME = "DeepInfra"`, to be held to the smoke run's
    `provider` field.
  - **The bridge's.** `BRIDGE_PINS` holds this pin and `queue_alone/plan.py`'s,
    imported, under `"deepinfra"` and `"baidu"`.
- **The protocol.** `PROTOCOLS = ("v1b", "v1c")`, `LEVEL = 3`, and
  `SYSTEM_PROMPT_SHA16 = "7b883f03a863d647"`, imported from
  `reasoned_loop/plan.py`.
- **The arms.** `ARMS = ("v1b", "v1c")`, in that order, because `ORDER_SEED`'s
  draw picks from it. `COVERAGE = Fraction(1, 2)` for both, imported from
  `channel/plan.py` as its channel arm's.
- **The runs.**
  - `REPS = 3`, `N = 2000` and `SEED = 17`;
  - `SMOKE_N = 30` and `SMOKE_ARM = "v1c"`;
  - `MAX_ESCALATIONS = 400` and `MAX_CONSECUTIVE_FAILURES = 5`.
- **The draws** are `PLAN_CHANNEL.md`'s, through `channel.plan.draws`: `"r1"` to
  `"r3"` for run `k` of both arms, and `"smoke"` for the smoke run. No new draw
  seed is drawn.
- **The seeds.** `ORDER_SEED = 101` and `BRIDGE_SEED = 103`.
  - **They are new**, and were fixed by rule: the next two primes after
    `PLAN_CHANNEL.md`'s 97. Every closed thread's seeds are 17 to 20, 25, 41,
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89 and 97, and values from 1000 up.
  - **`ORDER_SEED` draws one thing**: which arm runs first, from
    `f"PLAN_PLACEMENT/order/{ORDER_SEED}"`.
  - **`BRIDGE_SEED` draws two things.** The 13 tickets come from
    `f"PLAN_PLACEMENT/bridge/{BRIDGE_SEED}"`. At each ticket, the provider asked
    first comes from `f"PLAN_PLACEMENT/bridge/{BRIDGE_SEED}/{idx}"`.
  - **Both are string seeds**, through SHA-512, and depend on no
    `PYTHONHASHSEED`.
  - **The placement listing is not these seeds'.** It keeps v2b's
    `LISTING_SEED`, through `blind.protocol.listing`.
- **The bridge.** `BRIDGE_TICKETS = 40`, `BRIDGE_DRAWN = 13`, and `BRIDGE_ASKS =
  1` to each provider.
- **`DECLARED`** holds the figures §0 lists as computed while drafting, as
  `channel/plan.py`'s holds that plan's.
- **The lines of §0.** They are fractions, and every comparison with them is
  exact. `PL-a`'s and `PL-d`'s hold at or below their lines, and every other at
  or above.
  - `PL_A_LINE = Fraction(3, 4)`.
  - `PL_B_LINE = Fraction(9, 10)`.
  - `PL_C_LINE = Fraction(9, 10)` on each run, and `PL_C_RUNS = 3`.
  - `PL_D_LINE = Fraction(1, 20)`.
  - `PL_E_LINE = Fraction(9, 10)`.
  - `PL_F_LINE = Fraction(9, 10)`.

**The names.**

- **The package is `placement/`.** No module of the standard library has that
  name.
- **The rows are `PL-a` to `PL-g`, with two letters.** Every single capital
  already names a thread, and `QA`, `FM`, `RR`, `RL` and `CH` are taken.
- **The protocol is v1c**: v1b with one change, to the list.
- **The arms are named by their protocols**, `v1b` and `v1c`. A single letter
  would collide with `PLAN_CHANNEL.md`'s `c`, whose runs this plan names beside
  its own.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
placement/__init__.py
placement/plan.py        the gate, the constants of §11, the bridge's tickets
placement/protocol.py    v1c's list and escalation, and the asker with a pin    [proposer's path]
placement/loop.py        the loop with a channel and a protocol, calling channel's trigger   [proposer's path]
placement/references.py  the drafting reading, the transcriber and the hidden policy through both paths
placement/gates.py       PL-g1 to PL-g4
placement/sample.py      Stage A
placement/run.py         Stage B: the smoke run, the bridge and the runs; it spends   [proposer's path]
placement/score.py       Stage C
results_placement/FINDINGS_PLACEMENT.md
results_placement/sample.json  loop_smoke.json  bridge.json  loop_{v1b,v1c}_r{1..3}.json  score.json
tests/test_placement.py
```

**The plumbing goes in the same commit as the modules:**

- **`CODE_ROOTS`.** `placement` joins it in `harness/provenance.py`, and joins
  the oracle scan's roots in `tests/test_oracle_separation.py`.
- **`ONLINE_LOOP` and the authority channel.** The three modules marked above
  join both, with rule B's comment, and the watched count grows by three. Every
  call sends the manual's text.
- **The partial files**, `results_placement/*.partial.jsonl`, join `.gitignore`.
- **The guarded writers** in `tests/test_writer_lists.py` grow by one.
- **The call site.** The asker subclasses `reasoned_loop.protocol.Asker` in its
  request only. So it asks through `first_match/ask.py`'s asker, which is
  already a classified call site and carries the call recorder.
  `tests/test_call_record.py`'s list should not grow. If it does, the package
  classifies the new site before the signature.
- **The README's table of writers** gains its rows, and so does its table of
  tests.

**The list of modules allowed to see the oracle does not grow.** Tests touch no
network.

---

## 12. Definition of done

- [ ] Records under `results_placement/` with `_env`. Each carries:
      - the model, the temperature, the reasoning setting, the budget and the
        pin;
      - the protocol, the arm, the run, the coverage, and the draws' seed
        string and digest;
      - the texts' digests and `call_attempts`;
      - v1c's rounds, as rule C says.

      All were produced with `PYTHONHASHSEED=0`.
- [ ] `PL-g1` to `PL-g4` passed before any record was written. The key check
      and the smoke run came before the bridge and the first run, and each run's
      record was committed before the next began.
- [ ] Before the signature, OpenRouter's endpoint listing named the pinned
      endpoint (§2.8).
- [ ] Before the first run, the smoke run showed what §2.5 asks of it, and its
      bills were read.
- [ ] The plumbing of §11, and tests pinning:
      - the constants, the seeds and the gate;
      - v1c's list, on bases built by hand: a nested rule left out either way,
        an equal one kept, a governed one left out, a partly governed one kept,
        and an empty list sending no call;
      - that v1c with both exclusions off is v1b, and that the loop under v1b
        is `PLAN_CHANNEL.md`'s;
      - that the list reads no label: labels and draws that leave every cause
        unchanged leave every list unchanged;
      - the resume, that a resumed record keeps each call's own seconds, and
        that a run cannot resume under another protocol or other draws;
      - the bridge's tickets and order, rebuilt from their seed strings;
      - the exactness of §0's comparisons, *thin* on medians and on `PL-c`'s
        count, and each row's conditions for having no value;
      - the gate's verdicts on fake plans, and the count of signature lines,
        never whether this plan is signed.

      The transcriber's figures and the drafting reading's are `PL-g2`'s and
      Stage A's, never a test's, because no test runs the loop over the corpus.

      The whole suite is green on 3.10 and 3.12.
- [ ] Every figure in prose names its surface, its arm, its denominator and its
      runs.
- [ ] `results_placement/FINDINGS_PLACEMENT.md` owns every figure, with a dated
      erratum wherever it corrects something already published. That includes
      this plan's §0 *already seen*, if Stage A does not reproduce it, and §1's
      estimates of the pace, the calls and the money.
- [ ] `STATUS.md`: the scoreboard gains the `PL` thread. *What is open* narrows
      its second item by what this plan settles, and its third if `PL-f` or
      `PL-g` bears on it.
- [ ] `IDEAS.md`: *A placement round that asks only for what the engine can
      order* is struck or narrowed, with what this plan opens.
- [ ] `tests/test_prose_tables.py`'s `THREADS` gains `PL`, and its `TABLES` gains
      `FINDINGS_PLACEMENT.md`'s verdict table, once Stage C has written its
      record.
- [ ] This plan is indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan are in separate commits. The plan and its
      signature are each alone in their commits.

---

## 13. What this plan cannot settle, declared before it runs

1. **Which exclusion does what.** One arm carries both.
   - **The refusals.** On v1b's answers, 122 of the 124 refusals v1c takes away
     are nested rules left out (§0, figure 1). Stage C classes every round by
     what each exclusion left out.
   - **The graph.** What each exclusion does to the graph, and so to the edges
     refused for a cycle, is not separated.
2. **The error arm and the impasse arm under v1c.** Neither is run.
   `PLAN_REASONED_LOOP.md`'s e r3 wrote a catch-all at case 1 and left 38
   escalations unplaced. On its own answers, v1c would have taken 28 of them; no
   run tests that.
3. **Why the loop writes narrow rules.** The drafting reading says refusal did
   not select narrow births, and v1c leaves the first call as it is. A re-ask of
   the loop's first calls under the re-ask's line, which `IDEAS.md` carries, is
   another plan.
4. **A crossing rule left out.** v1c keeps v1b's refusal for it (§2.3), so c r2's
   draft of `H04`'s region whole would still have been refused. A round that
   accepts a partial placement is another plan.
5. **A right edge refused for a cycle.** v1c changes which edges enter the
   graph, not the rule that refuses one. Which edge of a cycle should yield is
   free on the records, and not read here.
6. **A nested pair level 1 orders wrongly.** No round can reach it: the engine
   refuses a side against containment, under v1b as under v1c. v1c stops asking,
   and gives up only the count of such sides (*What it changes*, above).
7. **The manual's identifiers.** The system prompt's *"la lista de arriba"* lets
   the proposer cite `H01` to `H29`, which no base holds. Each such citation is
   dropped, in both arms.
8. **The supply of rare tickets.** The draws are `PLAN_CHANNEL.md`'s, so run 2
   cannot report `H05` in either arm.
9. **The comparison across plans.** This plan's runs, set beside
   `PLAN_CHANNEL.md`'s, cross dates and providers. The bridge reads first calls
   only.
10. **One model, one provider, one manual, one arrival order, one coverage, and
    three runs an arm.**
