# PLAN_HALVES — which half of v2b's base paragraph makes the loop's first call cut

**Status: drafted by Claude on 2026-11-10, completed against its package the
same day, unsigned.** Under hard rule 2 of `CLAUDE.md` a model may draft a band
and may not sign it. **Nothing runs and no record is written until Sergi has
signed §0.** The signature has to land before any figure named here exists, in
its own commit, staged by name. That includes Stage A, which spends nothing: §10
says why.

- **Sergi made §2's choices on 2026-11-10**: the four texts as written, the 136
  tickets, two passes and then the rarest queue's session, and the sessions
  launched by the agent through a supervisor.
- **§§5 to 11 are written against `halves/`**, which follows in its own commit.
- **What the three analytical documents changed** is set out in §0, under *What
  the three documents say*.

Each later correction is dated in place.

**Asked for by Sergi on 2026-11-10**, the day the drafter proposed it, after the
third POST-RUN reading of `PLAN_WHOLE.md`'s records. [`IDEAS.md`](IDEAS.md)
carries it under *What `PLAN_WHOLE.md` opens*, in the later note on its first
item: *"Which half of v2b's paragraph does it: that the base is not shown, or
that overlapping rules of another queue will be listed. A first call with the
first half alone, set beside v2b on one day, would separate the halves. Calls."*
[`STATUS.md`](STATUS.md)'s *What is open* ends its second item on it. The
reading is the last section of
[`results_whole/FINDINGS_WHOLE.md`](results_whole/FINDINGS_WHOLE.md), *Whether
the blind paragraph is why the loop's first call cuts*.

**The provider follows from the design**, by the rule agreed with Sergi on
2026-11-06, which `IDEAS.md` records under *What `PLAN_CHANNEL.md` opens*. Every
arm runs inside the plan, so DeepInfra's fp8 endpoint is pinned. No adjudicated
row sets an answer against another provider's, so there is no bridge (§2.6). It
is his to sign.

**The item.** The loop's first call writes its ticket's governing region about
half as often as the same model asked the same ticket under an empty base, and
the two prompts differ in one paragraph.

- **The comparison.** `whole/paragraph.py` set `PLAN_REASONED_RULE.md`'s
  reasoning rule arm `w` beside the loops' first calls, at the tickets both
  answered. Both send level 3's system prompt, its impasse frame included, the
  same ticket, the same model, and reasoning at high effort with 16,000 tokens.
  They differ in the paragraph that stands where the base would be.
  - **The rule arm's** is the empty base: *"BASE DE REGLAS: vacia. Esta es la
    primera regla."*
  - **The loops'** is v2b's `BLIND_BASE`: the base is not shown, and a rule that
    overlaps rules of another queue will be listed afterwards.
- **What it found.** At each loop group's shared tickets, the empty base held
  its ticket's part in 0.8229 to 0.8533 of its right-queue answers, and v2b's
  paragraph in 0.3692 to 0.3968. The four gaps lie within 0.0543 of one another,
  two groups on Baidu and two on DeepInfra. Under T1, which asks for the region
  whole and still says that overlapping rules of another queue will be listed,
  v1d's first calls held it in 0.5918 at their 60 shared tickets.
- **What it could not separate**, as the reading itself says:
  - **the period.** The rule arm was asked on 2026-10-25, and the loops ran
    between 2026-10-31 and 2026-11-10;
  - **which half of v2b's paragraph does it.**
- **Why it matters for the loop.** The cut is where the rarest queue is lost.
  - **What the cuts cost.** Under v1c the cuts cost mostly `H04`'s and `H05`'s
    points, whose tickets escalate too rarely for a later draft to write their
    region whole (`FINDINGS_PLACEMENT.md`, *What the cuts cost*).
  - **What the cuts say.** At the queue's tickets every cut's note frames the
    draft as the end of a conflict between the governing rule and a crossing
    rule of another queue, which the draft lies inside and beats by containment
    (`FINDINGS_WHOLE.md`, *Why v1d cut at the rarest queue's tickets*).

**None of this is new analysis, and the plan's part is the instrument.** The
readings are the analysis, and they are POST-RUN. What this plan adds is the two
halves asked apart, beside the two whole paragraphs, in one period, of one
provider, with bands signed before any of its figures exists.

**The two halves.** v2b's paragraph is two clauses joined by a semicolon:

```
BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues.
```

- **The hidden half**, v2b's first half, is everything before the semicolon: the
  base is not shown in this step, and the model is to write its rule for this
  ticket.
- **The overlap half** is the clause after it: if the rule overlaps existing
  rules of ANOTHER queue, they will be listed afterwards.

**Four arms**, the two halves crossed with the two base paragraphs. Each arm is
the loop's first call at a ticket, byte for byte but for the paragraph. §2.1
gives the exact texts.

- **`e`, the empty base.** Its prompts are `PLAN_REASONED_RULE.md`'s arm `w`'s,
  byte for byte, at every ticket that arm asked.
- **`v`, v2b's paragraph**, both halves. Its prompts are the loops' first calls,
  byte for byte.
- **`h`, the hidden half alone**: v2b's paragraph up to its semicolon, closed by
  a full stop.
- **`o`, the overlap half on the empty base**: the empty base, with v2b's clause
  after it.

**The question, in its cleanest form.** At tickets the reasoning loops
escalated, with level 3's manual in the system prompt and reasoning on, of one
provider and in one period:

- does the paragraph's gap hold when both paragraphs are asked in one period,
  interleaved?
- which half of v2b's paragraph costs more of the region: that the base is not
  shown, or that overlapping rules of another queue will be listed?
- does the hidden half cost it on its own, set where the empty base stood?
- does the overlap half cost it even when the base is said to be empty?
- at the rarest queue's seven tickets, does dropping the overlap half give the
  region back?

**What it changes in what is measured, said first.**

- **It installs nothing.** No loop runs, no rule is born and no base grows. Every
  row reads the first call's answer alone, classed as `PLAN_WHOLE.md`'s Stage C
  classed a first-call draft.
- **Asked alone, the first call is what it is in the loop.** At every escalation,
  whatever its cause, a v1b or v1c loop sends a fresh request of two messages:
  the system prompt, and the user message over v2b's paragraph, which carries
  nothing of the base (`reasoned_loop/protocol.py`, `Resumable.first`). So arm
  `v`'s prompt at a ticket is the first call every such loop sends there. What
  the ask does not carry is the rest of the loop: no row reads what a base
  compiles, or what the placement round does with a draft.
- **Only `h` and `v` can be sent in a blind loop.** A loop's base is empty only
  before its first birth, and a blind first call never says so. So `e` and `o`
  are diagnostic, and `h` is the candidate text for the loop plan that would
  follow (§12).
- **`o`'s two sentences do not sit together.** The base is empty and the rule is
  the first, yet existing rules of another queue will be listed if the rule
  overlaps them. How the model reads the two is part of what is measured, and
  the reasoning is recorded whole.
- **Each half is two sentences, and so is the empty base.** `h` says that the
  base is not shown in this step, and asks for a rule for this ticket. `e` says
  that the base is empty, and that the rule is the first. So `e` against `h`
  sets v2b's first half against the empty base's paragraph, not the hiding
  alone, and every row that reads that difference reads both sentences of each.
- **The level-1 sentence stays in every arm.** Level 3's system prompt says
  *"Por eso solo necesitas declarar prioridad frente a reglas que se solapan con
  la tuya sin que una contenga a la otra. Si tu regla es un caso particular de
  otra, no declares nada: el nivel 1 ya lo resuelve."* It also asks the model to
  place its rule among the rules that exist.
  - **Rung 2 read that sentence as an incentive to avoid overlap**: *"which reads
    as an incentive to AVOID overlap"* (`rung2/proposers2.py`, v2's comment).
  - **Every arm's paragraph is read beside it.** This plan measures the
    paragraph with the sentence present, and does not separate the two (§12).
- **The gap is split along one path.** `HV-c` reads it along `e` → `h` → `v`,
  the path that ends at a text a loop can send. The other path, `e` → `o` → `v`,
  splits it the same way only if the halves do not interact. `HV-e` reads its
  first step, and `HV-g` reports the interaction.
- **A count can move without the operation.** Rung 2's v2 replaced the level-1
  sentence with one that told the proposer not to cut: *"No estreches una regla
  ni le añadas condiciones para esquivar a otra: eso no resuelve el conflicto, lo
  esconde."* That instruction *"moved the numbers (1.6% → 7.25%) but not the
  operation"* (`CHAT_SUMMARY.md` §1). `HV-g` reports every answer's class, a cut
  by a listed rule or another narrowing, so that a moved share can be read as a
  moved operation or not.
- **Whole is breadth, not correctness.** The share reads an answer's extension
  against its ticket's governing region. *"Narrow ≠ correct"*
  (`ARBITRATION_REPORT.md` §2, which `CHAT_SUMMARY.md` §1 repeats), and whole is
  not right either. No row reads whether a base decides right: that is the loop
  plan's.
- **A share can rise by construction.**
  - **What it counts.** `W` counts a draft wider than its part as whole. It
    leaves answers of the wrong queue, and answers naming no valid rule, out of
    its denominator.
  - **How an arm can game it.** It can raise its share by drafting wider than the
    governing region, or by losing the right queue where it would have cut.
  - **What `HV-g` does.** It reports both, by arm, and a hold carried by either is
    read as such. A rate a construction moves *"rises from 0/14 whatever the model
    does"* (`ARBITRATION_REPORT.md` §7, P1's third objection).
- **Reasoning is on**, as in every loop since `PLAN_REASONED_LOOP.md`, against
  `PLAN_REUSE.md` §1's amendment, for this plan's calls only.
- **Hard rule 5 allows two new texts.** `h` and `o` are v2b's and the empty
  base's own words, cut or joined at v2b's semicolon, after both have recorded
  results. Their bytes are fixed before signature (§2.1), and after it nothing
  in them moves.
- **Every adjudicated row is read within one provider and one period** but
  `HV-a`, the instrument row, which sets today's `v` beside the loops' first
  calls on the same provider, across dates. Every comparison with Baidu's
  records, the rule arm's included, is reported in `HV-g`.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**The tickets are the corpus's, and each answer is read over the space.**

- **Every figure is about tickets of `generate_corpus(2000, seed=17)`** that a
  reasoning loop escalated.
- **Each answer's class reads its region over the 134,400 points of the space**,
  as `whole/paragraph.py` reads it. A draft that leaves out only points no corpus
  ticket carries is not whole. No row reads the arrivals instead.
- **The tickets, `T`, are 136** (§2.2):
  - **133** of `PLAN_REASONED_RULE.md`'s 171 tickets: those a first call of one
    of the five loop groups `whole/paragraph.py` reads met;
  - **and 954, 982 and 1432**, the three of `ONCALL_ESCALATION`'s seven tickets
    that are not among the 171. A loop's first call met each of them.
- **`T₇`** is the rarest queue's seven tickets: 257, 710, 954, 982, 1432, 1783
  and 1951.

**The asks, the classes and the notation.**

- **A prompt is an arm at a ticket**: 4 × 136 = 544 prompts.
- **Pass 1 and pass 2** each ask every prompt once, the arms interleaved (§2.3).
  **The rarest queue's session** asks each of the 28 prompts at `T₇` four times
  more.
- **An answer is valid** when the call came back, after its retries, with a
  payload that parses, from the pinned provider. A failed call, an answer cut
  off past repair and an answer from another provider are invalid. They are
  counted and reported, and never classed.
- **A valid answer's class** is `placement/cost.py`'s `draft_class`, called
  through `whole/paragraph.py`'s `classed`, as `PLAN_WHOLE.md`'s Stage C classed
  a first-call draft: *whole*, *cut by one* listed rule, *cut by two*, *other*,
  *wrong queue* or *no rule*.
  - **Its part** is the points of its ticket's governing rule's region whose true
    queue is that rule's. The governing rule is the first listed rule whose
    region holds the ticket.
  - **It is *whole*** when it names the governing rule's queue and every point of
    its part lies in its extension. A draft wider than the part is whole too.
- **`W_x`**, for arm `x` over a set of answers, is `H_x / R_x`.
  - `R_x` counts its valid answers of the right queue that name a valid rule:
    every class but *wrong queue* and *no rule*.
  - `H_x` counts those classed *whole*.
- **`W_x` with no superscript** reads both passes, at every ticket of `T`.
  **`W_x⁷`** reads both passes and the rarest queue's session, at the tickets of
  `T₇`.

**The unit, the error and *thin*.** All of it is settled here and not in the
scorer, which is where `PLAN_AUTHORSHIP.md`'s `E-c` lost its verdict.

- **Every row pools the answers it reads**, over its tickets and its sessions.
  The ticket is the cluster: its answers share its region and its governing
  rule.
- **Every statistic is a ratio of integer counts, and is compared with its line
  exactly, as a fraction.** No rounding enters a verdict.
- **The standard error is clustered by ticket.**
  - **The formula.** For a statistic `Σ c_x W_x` over arms, ticket `t`
    contributes `u_t = Σ c_x (h_{x,t} − W_x r_{x,t}) / R_x`, where `h_{x,t}`
    and `r_{x,t}` are its counts. The variance is `C/(C−1) · Σ_t u_t²` over the
    row's `C` tickets.
  - **`HV-a`'s statistic is a mean over tickets**, and its error is that mean's.
  - **It is a label.** It is a float, and it marks *thin* and never decides.
- **A verdict is labelled *thin*** in either of two cases, and the label does not
  change the verdict:
  - the statistic lies within one standard error of its line, or of the nearer
    edge of `HV-a`'s band;
  - read on pass 1 alone or on pass 2 alone, it falls on the other side. For
    `HV-f`, read with any one of `T₇`'s tickets left out, it falls on the other
    side.

**When a row has no value.**

- **A row has none** if more than a twentieth of the answers it reads are
  invalid. *[Changed before signature, 2026-11-10.]* The draft counted the
  prompts that lacked a valid answer in a pass. At `HV-f`'s fourteen prompts a
  pass, one invalid answer would have taken the row's value.
- **`HV-a` has none** if fewer than 50 tickets carry a right-queue answer both
  today, under `v`, and among the DeepInfra loops' first calls.
- **`HV-c` has none** if `W_e − W_v ≤ 1/10`. There is then too little gap to
  divide between the halves.
- **`HV-f` has none** if fewer than five of `T₇`'s tickets carry a right-queue
  answer under both `h` and `v`.
- **A row with no value is unadjudicable**, and the record says so.

**Two rows read one difference.** `HV-c` and `HV-d` both read `W_e − W_h`.
- **`HV-c`** holds when it is under half the gap `W_e − W_v`.
- **`HV-d`** holds when it is at least a tenth.

They are not independent, and both can hold only if the gap is over a fifth.

**The interaction is reported, not banded.** `(W_h − W_v) − (W_e − W_o)` reads
four arms, so its error is about the sum of four arms' errors. By §1's estimate
that is some six to eight hundredths, against effects of that order.
`PLAN_REASONED_RULE.md`'s `RR-d` crossed two factors and came out thin for that
reason. Its lesson asks a plan to size such a row against the noise of four
arms, and these sessions are not sized for it.

**What the sessions' commits may show.** If the agent launches the sessions
(§2.5), a supervisor commits each record with a message written from it. It may
give each session's asks, failures, retries and seconds, which no row reads. No
message gives a class, a share or a row, and none is computed before Stage C.

**Which side had the label**, for every arm and reference. This was checked
against the prompts and the code while the package was written, and not
recalled, as `CLAUDE.md` asks of any plan that sets a comparison on the
proposer. `HV-g1` and `HV-g2` hold the texts and the asker's path to it:

| who | what it is handed | reads a label? |
|---|---|---|
| all four arms | level 3's system prompt, with the 29 rules in order under *"Se aplica la primera regla de la lista cuyas condiciones casa el ticket."*; the ticket; the arm's paragraph, which names no queue and no rule | **yes, in effect**: every ticket's label is derivable from the text by first match (`PLAN_MANUAL.md` §6.2) |
| the references: `PLAN_REASONED_RULE.md`'s arm `w`, and the loops' first calls | the same, under `e`'s paragraph or `v`'s | as the arms |
| Stage C's classes | the policy's 29 regions over the space, and the true queue of every point | **yes**: they are what every class is read against. Nothing of them reaches a prompt |

- **No arm sees an example**, and nothing here is fitted, so nothing reaches a
  test split.
- **No baseline is set against the proposer.** The four arms are the proposer's
  own first call, with one paragraph changed.

**The retry, settled here.** It is the loops' own: `PLAN_FIRST_MATCH.md`'s asker,
as `PLAN_REASONED_LOOP.md` calls it.

- **A failed call** is retried with the same messages, after a wait. **A failed
  parse** is retried with v1's retry message.
- **A refusal for the rate** is waited out. Once every wait is spent it is an
  outage: the session stops unrecorded, and the same command resumes it from its
  partial file.
- **Every row says which retries it took.**

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **HV-a** | **Asked alone, v2b's paragraph writes the region as often as the loops' first calls did, on the same provider** | over the tickets of `T` where `v` named the right queue today and a first call of `PLAN_PLACEMENT.md`'s six runs or `PLAN_WHOLE.md`'s three v1c runs did too: the mean of `v`'s share at the ticket, both passes, less those first calls' share there | **from −1/10 to 1/10** | **below −1/10, or above 1/10** |
| **HV-b** | **The paragraph's gap is not the period's**: in one period, of one provider, the empty base writes the region at least a fifth more often than v2b's paragraph | `W_e − W_v` | **≥ 1/5** | **< 1/5** |
| **HV-c** | **The overlap half costs more of the region than the hidden half** | `W_h − (W_e + W_v)/2`: how far the hidden half alone lies above the midpoint of the empty base and v2b's paragraph | **> 0** | **≤ 0** |
| **HV-d** | **v2b's first half costs the region too**, set in place of the empty base, without the overlap half | `W_e − W_h` | **≥ 1/10** | **< 1/10** |
| **HV-e** | **The overlap half costs the region even when the base is said to be empty** | `W_e − W_o` | **≥ 1/10** | **< 1/10** |
| **HV-f** | **At the rarest queue's tickets, the first call without the overlap half writes the region at least a fifth more often than with it** | `W_h⁷ − W_v⁷` | **≥ 1/5** | **< 1/5** |
| **HV-g** | *Reported, not adjudicated.* **What the drafter could not band** | Each arm's `W` by pass and by session, pooled and by ticket, by governing rule and by true queue. Every valid answer by class, and by breadth against its governing region: the region itself, wider, or neither. The interaction, `(W_h − W_v) − (W_e − W_o)`. Each arm's share of answers of the wrong queue and of answers naming no valid rule. How often a prompt's two answers in the passes share a class, by arm, and at `T₇` the spread of its six. Each arm's answers at each ticket of `T₇`, by class and by the rule a cut is by. How many answers declare `beats` or `loses_to`, and how many of those cite the manual's identifiers. `e` beside `PLAN_REASONED_RULE.md`'s arm `w` at the 133 tickets it asked, and `v` beside each loop group at its tickets, across dates and providers. The calls: providers, finish reasons, tokens, reasoning tokens over the attempts that reached the model, seconds, and retries by cause. The notes and the reasoning, recorded whole and not coded | — | — |

**Signed by Sergi: ________ (date: ________)**

**Why each row, and why these lines.**

- **`HV-a` is the instrument row.** It says how far today's asks stand for the
  loop's first call, on the provider that served it.
  - **Arm `v`'s prompt is that first call**, byte for byte, under the same
    request and pin. What separates them is the date, and that the loops asked a
    ticket as often as they escalated it, from once to nine times.
  - **So it reads ticket by ticket**: each ticket's two answers today beside the
    loops' share there, and the mean of the differences. A pooled share would
    weigh each side's tickets differently.
  - **Its line is a tenth.** The four v2b groups' shares at their shared tickets
    lay from 0.3692 to 0.3968, on two providers and over ten days. A tenth is
    several times that spread.
  - **Earlier instrument rows read agreement answer by answer** (`RR-a`, `FM-a`).
    The loops asked each ticket a varying number of times, so a share by ticket
    is what they can be set beside.
- **`HV-b` settles the period.** The reading set answers asked on 2026-10-25
  beside first calls made over the next fortnight. Here both paragraphs are asked
  in one period, interleaved, of one provider. **Its line is a fifth**, under
  half the smallest gap the reading found, 0.4298. A hold says the paragraph
  carries at least that much of the gap with the period held fixed.
- **`HV-a` and `HV-b` replicate figures the drafter had seen.**
  - **What they pre-register** is this period's figure, which does not exist.
  - **But a replication surprises its author less.** *"A measurement that could
    not have surprised its author is worth less than one that could"*
    (`EXTERNAL_REVIEW.md` §3).
  - **So the scoreboard should read both verdicts as replications**, as it reads
    `PL-e`'s and `WR-e`'s.
- **`HV-c` is the plan's question.** Along `e` → `h` → `v`, the gap `W_e − W_v`
  is the sum of two parts: the hidden half's, `W_e − W_h`, and the overlap
  half's, `W_h − W_v`. The overlap half's part is the larger exactly when `W_h`
  lies above the midpoint of `W_e` and `W_v`.
  - **Its line is the literal *more***, so a tie goes against the claim.
  - **With too little gap to divide it has no value**, settled above.
- **`HV-d` asks whether v2b's first half costs anything on its own**, set where
  the empty base stood. If it does, a loop that drops the overlap half still
  loses part of the region to the first half, and the next text has to answer
  that too. It reads both of each paragraph's sentences, not the hiding alone
  (said first, above). **A tenth** is about the smallest difference two passes
  over 136 tickets are sized to see: some two standard errors, as the drafter
  estimates them from binomial counts and not from any record (§1).
- **`HV-e` asks whether the overlap half acts on its own.** Told the base is
  empty and its rule is the first, the model has no listed rule to fear. If the
  clause still costs a tenth, it acts whatever the base paragraph says. If not,
  it acts only beside the hidden half, and the halves interact.
- **`HV-f` reads the comparison the loop plan would act on, where the loop
  loses.** `PLAN_WHOLE.md`'s lesson: *"A text can move the drafts and miss the
  tickets a row reads"*. There T1 raised the share of whole drafts overall, and
  the rarest queue's recall fell run for run (`WR-f`).
  - **It sets `h` beside `v`**, because those are the two texts a loop can send.
  - **Its line is a fifth.** The rarest queue's rules escalate one to three times
    a run, so a first call there that writes the region whole only a little more
    often would not compile the queue.
  - **Its seven tickets make it likely thin**, and *thin* reads it with each
    ticket left out in turn.

**What the drafter had already seen, declared so that the signature is
auditable.** The drafter wrote `FINDINGS_WHOLE.md`'s three POST-RUN sections and
their modules on 2026-11-10, in an earlier session, and proposed this plan at
its end. In the session that drafted this file it read:

- **`CLAUDE.md`**, whole.
- **`STATUS.md`**: what it read and did not.
  - **Read:** the list of its sections; *What is open* and *What this does not
    show*, whole; the scoreboard's heading, its convention, its table to `QA`'s
    row, and its total.
  - **Not read:** *Before reading any figure*, *What is established*, *What was
    withdrawn*, and the scoreboard's later rows and notes.
- **`IDEAS.md`**: its header; the first line of every item in every section,
  listed by a script; *Pending and already specified*; *What `PLAN_WHOLE.md`
  opens*, *What `PLAN_PLACEMENT.md` opens* and *What `PLAN_CHANNEL.md` opens*,
  whole; *What the outside reading of November 2026 proposes*, whole; the
  October section from its label model to its end; *What `ARBITRATION_REPORT.md`
  §7 proposes*; five items of *What `PLAN_FIRST_MATCH.md` opens*; *Technical
  debt*'s *What that leaves open*; and *Prior to the four rungs*.
- **The whole-region thread.**
  - **`FINDINGS_WHOLE.md`**: its list of sections; its Stage B, to the table of
    the six runs; its POST-RUN sections on the rarest queue's tickets and on the
    blind paragraph, whole; and its POST-RUN section on `SECURITY_INCIDENT` from
    its third part on.
  - **`PLAN_WHOLE.md`**: its first draft, whole, from its commit; and the final
    file's banner, status line and §0, whole.
- **The reasoned-rule thread.** `PLAN_REASONED_RULE.md` from its opening to the
  end of §0, and the `started_at`, `finished_at`, `provider`, `settings` and row
  keys of its two passes' records, with the seconds of arm `w`'s rows. No answer
  of the arm was read.
- **`PLAN_BLIND.md`**: a passage of its non-negotiable rules, on what hard rule 5
  allows.
- **The three analytical documents `CLAUDE.md` asks a new one to read first.**
  None has changed since 2026-11-01.
  - **For the draft**, the drafter read the passages it rests on directly:
    `ARBITRATION_REPORT.md` §5; `CHAT_SUMMARY.md`'s header, with its list of
    errata, and §1; `EXTERNAL_REVIEW.md` §3 and §5. It also read
    `PLAN_WHOLE.md`'s account of all three, which a subagent read whole on
    2026-11-09.
  - **Before signature**, a subagent of the drafter read all three whole for
    this plan on 2026-11-10, with every dated erratum and note. The drafter read
    its report, checked against the files each quote this plan uses, and read
    `rung2/proposers2.py`'s v2 text and comment, which the report pointed to.
    What bears on the plan is set out below, under *What the three documents
    say*.
- **The code read.**
  - **Whole:** `whole/paragraph.py`.
  - **In part:** `blind/protocol.py`'s texts; `whole/protocol.py`'s texts and the
    head of `messages_for`; `reasoned_loop/protocol.py`'s docstring, texts,
    `messages_for` and `Resumable.first`; `reasoned_loop/loop.py`'s
    `propose_v1b` and the case record; `placement/protocol.py`'s docstring;
    `placement/plan.py`'s request; `reasoned_rule/plan.py`'s `settings`;
    `reasoned_rule/population.py`'s docstring and `Design`; `placement/cost.py`'s
    `draft_class`; `whole/references.py`'s `_world`, `breadth`, `first_drafts`
    and `whole_of`; `rung2/proposers2.py`'s `render_base_v1` and `user_msg`.
  - **Level 3's system prompt**, `manual.prompts.loop_system_prompt(3)`, printed
    whole, and one first-call user message under v2b's paragraph, at case 710.
  - **`tests/test_prose_tables.py`'s `THREADS`**, for a prefix no thread uses.
  - **Writing the package, after the draft was committed.**
    - **Whole:** `reasoned_rule/`'s `plan.py`, `prompts.py`, `ask.py` and
      `gates.py`.
    - **In part:** `reasoned_rule/population.py`; `first_match/ask.py`'s
      helpers; `reasoned_loop/protocol.py`'s `Asker`, `Live` and
      `RateLimited`; `placement/protocol.py`'s `request_with` and `Asker`;
      `placement/run.py`'s opening and its bridge; `authorship/protocol.py`'s
      `Answer` and `ProposalFailed`; `fidelity/ask.py`'s `open_partial`;
      `spotcheck/gates.py`'s `N-g2` and `escalations/gates.py`'s names;
      `reuse/gates.py`'s `run_suite`; `whole/score.py`'s verdicts and `main`,
      and `whole/sample.py`'s `main`; `harness/domain.py`'s `Case`.
    - **The tests and the plumbing:** `tests/test_reasoned_rule.py`'s helpers,
      gate tests and Stage B tests; `tests/doubles.py`'s
      `OpenRouterShapedClient`; `tests/test_oracle_separation.py`,
      `tests/test_writer_lists.py`, `harness/provenance.py`'s `CODE_ROOTS`, the
      README's table of writers and `.gitignore`.

**Figures computed while drafting**, on 2026-11-10, from the records as `main`
holds them at `41b3ce4`, by scripts kept outside the tree. Stage A recomputes
them, and its record will own them. **None of them reads an answer's class**,
and none reads an answer this plan buys. All four were seen before §0's lines
were drawn.

1. **The tickets.**
   - `PLAN_REASONED_RULE.md`'s arm `w` asked 171 tickets, two answers each.
   - The five loop groups' first calls met 216, 316, 250, 171 and 108 tickets,
     545 in all. Of the 171, they met 91, 96, 88, 78 and 60: 133 in all, and 131
     for the four groups under v2b's paragraph.
   - The rarest queue's seven tickets are 257, 710, 954, 982, 1432, 1783 and
     1951, governed by `H05`, `H05`, `H04`, `H04`, `H04`, `H05` and `H04`. Four
     of them, 257, 710, 1783 and 1951, are among the 171, and a loop's first call
     met all seven.
2. **The tickets' governing rules**, which read the policy's first match on each
   ticket, and so its label. Over the 133, by queue: `T2_TECHNICAL` 48,
   `T1_GENERAL` 20, `SECURITY_INCIDENT` 19, `SELF_SERVICE_DEFLECT` 15,
   `ACCOUNT_MANAGER` 11, `T3_ENGINEERING` 11, `BILLING_SPECIALIST` 5 and
   `ONCALL_ESCALATION` 4. `T` adds three of `H04`'s. Every one of the corpus's 20
   tickets of `SECURITY_INCIDENT` but one is among the 133.
3. **`HV-a`'s tickets.** 102 tickets of `T` were escalated by `PLAN_PLACEMENT.md`'s
   six runs or `PLAN_WHOLE.md`'s three v1c runs, 405 escalations in all, from one
   to nine a ticket. On Baidu, 117 tickets and 523 escalations.
4. **The pace on DeepInfra**, read off every first call's seconds and attempts:

   | first calls of | calls | seconds, median / mean | reasoning tokens, median | completion tokens, median / mean | prompt tokens |
   |---|---|---|---|---|---|
   | `PLAN_PLACEMENT.md`'s six runs | 500 | 77.2 / 89.4 | 4,881 | 5,142 / 5,630 | 1,762 |
   | `PLAN_WHOLE.md`'s v1c runs | 244 | 95.1 / 114.3 | 5,053 | 5,258 / 5,682 | 1,762 |
   | `PLAN_WHOLE.md`'s v1d runs | 161 | 111.6 / 130.5 | 4,910 | 5,200 / 5,594 | 1,857 |

   One attempt of a first call in `PLAN_PLACEMENT.md`'s runs reached the budget
   of 16,000 completion tokens.

**[Added before signature, 2026-11-10] What writing the package showed.** The
package was written, and its checks run, before the signature, as §6 asks.

- **`HV-g1` to `HV-g3` pass**, with the suite green, in `python3 -m halves.ask
  --dry-run`. They print whether each check passes, and no figure.
- **§0's four figures came back as declared.** Stage A's `figures` recomputed
  them in memory, printed only which did not come back, none, and wrote
  nothing.
- **The instrument came back.** `whole/paragraph.py`'s classes gave back its
  record's counts, group by group, from the closed answers. Only whether each
  group agreed was printed.
- **Stage C's scorer ran only on what nobody answered.** It read rows written by
  hand, and one rule written by hand at every ask of every session. No answer of
  the model was classed for this plan, and no reference class was printed.
- **It changed one rule of §0.** A row's invalid answers are counted over the
  answers it reads, not over the prompts a pass (above).
- **It found one trap.** The gates may not name the record guard (§5).

**What the three documents say.** A subagent of the drafter read
`ARBITRATION_REPORT.md`, `CHAT_SUMMARY.md` and `EXTERNAL_REVIEW.md` whole for this
plan on 2026-11-10.
- **Their newest entries** are of 2026-10-06, 2026-08-17 and 2026-10-16. So none
  names v2b, the blind loops, the first call, level 3, reasoning, providers or
  periods, and what bears here bears by analogy.
- **Each quote below was checked against its file.** What bears on the plan, and
  what the plan did with it:

- **An instruction against a cut has moved counts and not the operation.**
  `CHAT_SUMMARY.md` §1, with v2's own text in `rung2/proposers2.py`. Cited in *A
  count can move without the operation*, said first.
- **The level-1 sentence was read as an incentive to avoid overlap.** That is
  `rung2/proposers2.py`'s comment on v1.
  - **Rung 2's v1 changed two things from rung 1's prompt.** It showed the base,
    which `ARBITRATION_REPORT.md` §5 credits with the fall in overlap *"from
    17.5% of the pairs to **1.60%**"*. And it added that sentence, which rung 1's
    prompt, `harness/proposers.py`, does not carry.
  - **The sentence is in every arm here.** So it is now said first, and kept in
    §12.
- **The operation has survived a change of text before.** *"the operation it
  performs —find a gap and fill it— does not require computing it, and it is
  the operation it performs even when it is asked for another"*
  (`ARBITRATION_REPORT.md` §5).
  - **It warns against `HV-c` and `HV-f`.**
  - **A cut is not that partition.** It nests inside a crossing rule, which
    orders by containment, a layer rather than a tile of a mosaic.
- **The model has reasoned its way to containment before.** It *"even correctly
  identifies that subsumption resolves a nesting with no need for a
  declaration"* (`ARBITRATION_REPORT.md` §5), and the system prompt tells it so in
  every arm. Cited against `HV-c` in the drafter's expectations.
- **A cost announced for overlapping made this proposer overlap less.** *"the
  proposer met the discipline by overlapping less"* (`ARBITRATION_REPORT.md` §7,
  P3's note of 2026-10-06). That was with the base in view. It bears for `HV-c`
  and `HV-e`.
- **Narrow is not correct.** `ARBITRATION_REPORT.md` §2 is the phrase's origin.
  Cited in *Whole is breadth, not correctness*, said first.
- **A rate a construction moves.** `ARBITRATION_REPORT.md` §7, P1's third
  objection, and P3's condition, *"at comparable or greater coverage"*. Cited in
  *A share can rise by construction*, said first.
- **A replication surprises its author less.** `EXTERNAL_REVIEW.md` §3. `HV-a`
  and `HV-b` are to be read as replications.
- **Classify an item by whether its figure exists.** `EXTERNAL_REVIEW.md` §5,
  point 6.
  - **Every row here meets it.** None of their figures exists.
  - **The interaction has no figure either.** It is reported rather than banded,
    for its noise, as §0 now says.
- **A figure names its surface.** `ARBITRATION_REPORT.md`'s header and §6, and
  `CHAT_SUMMARY.md` §2.1's erratum. §0 now names both: the tickets are the
  corpus's, and every class reads the space.
- **Figures do not travel between machines.** `CHAT_SUMMARY.md` §4's erratum.
  - **The four gaps share one side.** All four set the rule arm's answers, asked
    of Baidu on 2026-10-25, beside their loops.
  - **So their spread shows the loops' side held, not `e`'s.** `HV-b`'s
    expectation now says so.
- **A drafter's bet on which part moves has failed before.**
  - *"the drafter had the sign of ρ backwards"* (`EXTERNAL_REVIEW.md` §4, item
    5).
  - *"right about the surface and wrong about which row would move"*
    (`ARBITRATION_REPORT.md` §9, point 2's erratum).

  Cited in the drafter's record.
- **A refutation near the noise can be a non-detection.** *"untestable, not ruled
  out"* (`EXTERNAL_REVIEW.md` §4, item 4's note of 2026-10-05). *How the rows read
  together* now reads `HV-d` and `HV-f` that way.
- **The model's explanations are not its reasons.** It names the broader rule
  *"against what its own explanations say"* (`EXTERNAL_REVIEW.md` §2). Cited
  against `HV-c`, whose case rests on the cuts' notes.
- **A count of rules is noise between seeds.** *"the number of rules varies so
  much between seeds with an identical prompt that that quantity is noise"*
  (`ARBITRATION_REPORT.md` §9, point 4). It bears for the two passes and each
  prompt's agreement with itself.
- **One argument against the design in principle.** `CHAT_SUMMARY.md` §4 bet that
  success *"will not come from a smarter model nor a better prompt, but from
  **changing the question**"*. Its erratum lowered that to *"Bet with a low
  prior, not conclusion."* `h` is a better prompt for the same question, and the
  plan does not answer the bet beyond running the test.
- **Nothing bears on providers or periods**, nor on an arm whose sentences
  contradict each other.

**Not seen, because nothing has produced it:**

- any answer under `h` or `o`;
- any answer under `e` from DeepInfra, or at 954, 982 and 1432;
- any answer asked in this plan's period.

**Not looked at, though it exists:** the class of any recorded answer at any
single ticket, the rule arm's and the loops' alike, beyond what
`FINDINGS_WHOLE.md` and `FINDINGS_PLACEMENT.md` publish. The first publishes the
first calls at `T₇` in `PLAN_WHOLE.md`'s runs, which the drafter read there. The
second publishes them on `PLAN_PLACEMENT.md`'s bridge, which the drafter read as
`IDEAS.md` and `STATUS.md` summarise it. Stage A reads the rest.

**What the drafter expects, written down so the scoreboard can score it.**
**`HV-a`, `HV-b`, `HV-c`, `HV-d` and `HV-e` hold, and `HV-f` is refuted.** The
drafter trusts `HV-b` most, then `HV-a`, `HV-c`, `HV-e` and `HV-d`. **The bet is
`HV-c`.**

- **`HV-b` holds.** The paragraph is the one difference between the two prompts,
  and the gap was 0.43 to 0.48 wherever it was read.
  - *Against it:* the rule arm and the loops were never asked in one period, and
    that is the confound the row exists to remove.
  - *And:* the four gaps share one side. Each sets the rule arm's answers, asked
    of Baidu on 2026-10-25, beside its loops. So their spread of 0.0543 shows
    that the loops' shares held, not that `e`'s would on DeepInfra in another
    period, and that is what the row risks.
- **`HV-a` holds.** Same text, same request, same provider. `PLAN_PLACEMENT.md`'s
  first calls and `PLAN_WHOLE.md`'s v1c first calls, two periods apart, lay
  0.0235 apart at their shared tickets.
  - *Against it:* the loops' share at a ticket rests on one to nine answers, and
    DeepInfra's answers at one ticket change from ask to ask
    (`FINDINGS_PLACEMENT.md`, *Whether the cut is the provider's*).
- **`HV-c` holds.** At the rarest queue's tickets every cut's note frames the
  draft as the end of a conflict with a crossing rule of another queue, won by
  containment with no side declared. Of the four paragraphs, only those that
  carry the overlap half speak of rules of another queue.
  - *Against it:* under v2b's paragraph the narrow drafts that are no cut rose
    about as much as the cuts did. About a third of the loops' right-queue first
    calls are *other*, against about a seventh of the rule arm's answers
    (`FINDINGS_WHOLE.md`'s table of classes). The first half may carry those.
  - *And:* the system prompt speaks of the rules that exist in every arm, and
    tells the model that a nested rule needs no declaration. The model has
    reasoned its way to containment before (`ARBITRATION_REPORT.md` §5).
  - *And:* the case rests on the cuts' notes, and the model's explanations are
    not its reasons. It has named the broader rule *"against what its own
    explanations say"* (`EXTERNAL_REVIEW.md` §2).
  - *And:* the account that gives the cut to the overlap half is the drafter's
    own, written in `whole/paragraph.py`, and never tested. That reading's four
    clauses read the paragraph whole.
- **`HV-e` holds.** The overlap half invites the model to look for rules of
  another queue that its rule meets, and the manual lists them.
  - *Against it:* the empty base says the rule is the first, and a model that
    reasons may set the clause aside as moot.
- **`HV-d` holds, and the drafter trusts it least.** Told the base exists and is
  hidden, under a system prompt that says the engine could not decide the
  ticket, the model may take the manual's rules for the base's and cut against
  them. And `e` tells it its rule is the first, which `h` does not.
  - *Against it:* the same untested account gives the cut to the overlap half.
  - *And:* its line is about two standard errors, so a cost of a tenth may go
    unseen.
- **`HV-f` is refuted.** On DeepInfra no first call recorded at 1432 held its
  part, under v2b's paragraph or under T1, and every one `PLAN_WHOLE.md`
  recorded there cut by `H07`'s product. On `PLAN_PLACEMENT.md`'s bridge both
  providers cut alike at 982 and 1432. T1 still says that overlapping rules will
  be listed, and its first calls cut at six of the queue's eight tickets. The
  drafter expects `h` to gain there less than a fifth.
  - *Against it:* if the overlap half is what cuts there, the tickets where `v`
    cuts most are where `h` gains most.

**The drafter's record argues against trusting that.**

- **The scoreboard.** On `STATUS.md`'s, 60 of 152 adjudicated rows were refuted.
- **The last plan.** `PLAN_WHOLE.md`'s drafter expected all six of its rows to
  hold, and three did.
- **Bets on which part moves.** *"the drafter had the sign of ρ backwards"*
  (`EXTERNAL_REVIEW.md` §4, item 5). A point was *"right about the surface and
  wrong about which row would move"* (`ARBITRATION_REPORT.md` §9, point 2's
  erratum). `HV-c` is a bet of that kind.
- **What was done about it, rather than said.**
  - **No development set.** No band here was set on one.
  - **The lines.** `HV-a`'s, `HV-d`'s and `HV-e`'s tenth is about the smallest
    difference the sessions are sized to see. `HV-b`'s and `HV-f`'s fifth is
    under half the smallest gap the reading found. `HV-c`'s is the literal
    *more*.
  - **Thin, declared in advance.** A verdict one pass carries, or one ticket of
    `T₇`, is labelled *thin*.

Sergi should read the bands as more likely too comfortable than too strict, and
tighten them at signature if he disagrees.

**How the rows read together.**

- **A refutation near its line can be a non-detection.** `HV-d`'s and `HV-e`'s
  lines lie about two standard errors from zero, and `HV-f`'s about two of its
  own. A row refuted there may be *"untestable, not ruled out"*
  (`EXTERNAL_REVIEW.md` §4, item 4's note), and the readings below say so.
- **`HV-b` and `HV-c` hold, and `HV-d` is refuted.** The overlap half carries the
  gap. v2b's first half costs less than a tenth, or less than these sessions can
  see. The loop plan that follows sends `h` beside v1c.
- **`HV-b`, `HV-c` and `HV-d` hold.** Both halves cost, the overlap half more.
  Dropping it gives back most of the gap and not all, and the first half needs a
  text of its own.
- **`HV-c` is refuted and `HV-d` holds.** v2b's first half carries at least half
  the gap. A blind loop cannot send an empty base, so the next text must say
  something else about the base it hides. Dropping the overlap half alone would
  not be enough.
- **`HV-b` is refuted.** Much of the gap the reading found was the period's. With
  a gap of a tenth or less, `HV-c` has no value, and the reading is corrected in
  place.
- **`HV-e` holds.** The overlap half cuts on its own, whatever the base paragraph
  says. **Refuted while `HV-c` holds**, it cuts only beside the hidden half: the halves
  interact, and `HV-g` gives by how much.
- **`HV-f` holds.** At the rarest queue's tickets too, dropping the overlap half
  gives the region back, and the loop plan has reason to expect the queue.
  **Refuted while `HV-c` holds**, the text moves the drafts and misses the
  tickets that carry the queue, as T1 did, or the gain there was too small for
  seven tickets to show. The loop plan would then read the queue first, and the
  cut there is not the paragraph's alone.
- **`HV-a` is refuted.** Today's model under v2b's paragraph does not write the
  region as the loops' first calls did. The other rows are still adjudicated as
  signed. They then describe this period's model on this provider, and `HV-a`'s
  gap stands beside each.

---

## 1. What is bought, and what is already paid for

**Already paid for, and free to read.** Read-only, under hard rule 4:

- `PLAN_REASONED_RULE.md`'s two passes, whose arm `w` is `e` at 133 of `T`'s
  tickets, asked of Baidu on 2026-10-25;
- the first calls of `PLAN_REASONED_LOOP.md`'s, `PLAN_CHANNEL.md`'s,
  `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s runs, which are `v` at the tickets
  they escalated, and T1 under v1d;
- `whole/paragraph.py`'s reading of both, `results_whole/paragraph.json`.

**Bought:** 1,208 asks of the first call, on DeepInfra's fp8 endpoint, with
reasoning on at high effort and 16,000 tokens.

- **The smoke run:** 8 asks, two tickets an arm (§2.4).
- **Pass 1 and pass 2:** 544 asks each.
- **The rarest queue's session:** 112 asks, the 28 prompts at `T₇` four times
  each.
- **The money.** `PLAN_WHOLE.md`'s smoke run was billed $0.0194 for 25 attempts,
  at $0.080 per million prompt tokens with completion at twice that
  (`FINDINGS_WHOLE.md`, Stage B). At that price a first call of 1,762 prompt
  tokens and 5,200 completion tokens costs about a tenth of a cent. **The
  drafter expects one to two dollars for the plan.** The smoke run's bills are
  read by generation id before the first pass.
- **The time.** First calls on DeepInfra took a mean of 89 to 131 seconds, by
  plan and arm (§0's figure 4), one at a time. At those paces 1,208 asks take 30
  to 44 hours: **a day and a half to two days**, one session after another. The
  smoke run's pace rests on eight asks, and the record says how few. §2.3 gives a
  design at about half the time.
- **The precision**, as the drafter estimates it from binomial counts and not
  from any record. Two passes give each arm about 260 right-queue answers over
  136 tickets. A difference between two arms then carries a standard error of
  some four to five hundredths, clustered by ticket. At `T₇`, about 40 answers an
  arm give a difference an error of a tenth or more. Stage A's record gives the error
  the references carry, read off their answers.

---

## 2. The choices that have to be made at signature time

### 2.1 The four texts — Sergi chose them as written on 2026-11-10

Each stands where the base would be, at the head of the first call's user
message. `rung2.proposers2.user_msg` appends the ticket after it, as in every
loop. Each ends with a newline.

- **`e`, the empty base**, `rung2/proposers2.py`'s, as `PLAN_REASONED_RULE.md`'s
  arm `w` sent it:

  ```
  BASE DE REGLAS: vacia. Esta es la primera regla.
  ```

- **`v`, v2b's paragraph**, `blind/protocol.py`'s `BLIND_BASE`, as every v1b and
  v1c first call sent it:

  ```
  BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
  ticket; si se solapa con reglas existentes de OTRA cola, se te listaran despues.
  ```

- **`h`, the hidden half alone**: `v` up to its semicolon, with a full stop in
  the semicolon's place. That full stop is the one byte not taken from `v`.

  ```
  BASE DE REGLAS: no se te muestra en este paso. Escribe tu regla para este
  ticket.
  ```

- **`o`, the overlap half on the empty base**: `e`'s line with its last full stop
  made a semicolon, and `v`'s clause on the next line, byte for byte. In `v` the
  clause follows the semicolon and a space on one line; here a line break stands
  in that space.

  ```
  BASE DE REGLAS: vacia. Esta es la primera regla;
  si se solapa con reglas existentes de OTRA cola, se te listaran despues.
  ```

**Why the drafter recommends these.** `h` is a recorded text cut at its
semicolon, and `o` two recorded texts joined at one, so no word in either is
new.

**What they cost.** `o` is a text no loop could send, and its two sentences do
not sit together (§5). A text written for `o` from scratch would read better,
and would share less with `v`.

**The alternative** is three arms, `e`, `v` and `h`. `HV-b`, `HV-c`, `HV-d` and
`HV-f` keep their meaning, `HV-e` goes, and the plan costs a quarter less.

### 2.2 The tickets — Sergi chose the 136 on 2026-11-10

`T` is the rule arm's 133 tickets that a reasoning loop's first call met, with
the three of the rarest queue's tickets the rule arm did not ask.

- **Why these.** The loops' first calls met 545 tickets in all. The 133 are the
  ones where `e` was asked before, so `e` and `v` can each be set beside a record
  at the same tickets (`HV-a`, `HV-g`). The three added complete `T₇`, which
  `HV-f` reads.
- **The alternative** is every one of the rule arm's 171 tickets, with the same
  three. That adds 38 tickets that only `PLAN_MANUAL.md`'s loop, with reasoning
  off, escalated, and a quarter more time.

### 2.3 Two passes, then the rarest queue's session — Sergi chose it on 2026-11-10

Pass 1, then pass 2, each asking the 544 prompts once, in its own seeded order,
the arms interleaved. Then the rarest queue's session asks the 28 prompts at
`T₇` four times each, in its own seeded order. One session at a time, never side
by side.

- **Why two passes.** They are every ask plan's, `PLAN_FIRST_MATCH.md`'s and
  `PLAN_REASONED_RULE.md`'s among them. They halve the part of the error that a
  single ask carries at a ticket, give each prompt's agreement with itself, and
  mark *thin* by pass.
- **Why the rarest queue's session.** `T₇` holds seven tickets. With two answers
  a prompt there, `HV-f` would read fourteen answers an arm.
- **The alternative** is one pass, then the rarest queue's session at five asks
  a prompt: about 690 asks, 17 to 25 hours. *Thin* then reads the error alone,
  and no prompt's agreement with itself is measured outside `T₇`.

### 2.4 The smoke run — the drafter recommends two tickets an arm

Eight asks: for each arm two tickets, drawn at a fixed seed from `T` outside
`T₇`. It checks the pin, the texts, the records and the resume, and measures the
price and the pace. No row reads its answers.

### 2.5 Where the sessions are launched — Sergi chose the agent, through a supervisor, on 2026-11-10

By the agent, through a supervisor detached from the agent's harness, one
session at a time, as `PLAN_WHOLE.md` §2.5 allowed. A pass lasts many hours,
longer than a background command of the agent's harness survives. §8 says what
the supervisor does.

### 2.6 The pin is DeepInfra's fp8 endpoint, with no bridge — by the rule agreed on 2026-11-06

Every arm runs inside the plan. `HV-a` sets today's `v` beside first calls
DeepInfra served. Every comparison with Baidu's records, `e`'s with the rule arm's
included, is reported only. DeepInfra met no refusal for the rate in
`PLAN_PLACEMENT.md`'s or `PLAN_WHOLE.md`'s runs.

### 2.7 Everything else is the loop's first call, as v1c sends it

- **The texts:** the system prompt, `manual.prompts.loop_system_prompt(3)`, and
  the user message, `rung2.proposers2.user_msg` over the arm's paragraph.
- **The request:** the model, the temperature, the reasoning setting and the
  budget, and `response_format` on the first attempt.
- **The asker:** the retries by cause and the waits, the partial file, the
  resume, and each call's own seconds.

All are `PLAN_WHOLE.md`'s v1c first call, called and not changed, with
`placement/plan.py`'s pin.

### 2.8 `PREDICTION.md`

Untouched. It is rung 1's, and Sergi's.

---

## 3. Reference figures, with the record that owns each

| figure | value | owner |
|---|---|---|
| the rule arm's whole share at each loop group's shared tickets | 0.8229 to 0.8533 | `results_whole/FINDINGS_WHOLE.md`, *Whether the blind paragraph is why the loop's first call cuts* |
| the v2b loops' first calls' share there | 0.3692 to 0.3968 | the same |
| the four gaps, and their spread | 0.4298 to 0.4841; 0.0543 | the same |
| v1d's first calls under T1, at their 60 shared tickets | 0.5918, against the rule arm's 0.8522 there | the same |
| the rule arm's 342 answers over its 171 tickets, by class | 262 whole, 17 cut by one rule, 48 other, 15 of the wrong queue | the same |
| the rarest queue's first calls in `PLAN_WHOLE.md`'s runs | v1c whole at 4 of 7, v1d at 2 of 8; every cut at 1432 by `H07`'s product | the same, *Why v1d cut at the rarest queue's tickets* |
| the bridge at the rarest queue's tickets | Baidu held the part at five tickets and DeepInfra at three; both cut alike at 982 and 1432 | `results_placement/FINDINGS_PLACEMENT.md`, *Whether the cut is the provider's* |
| a first call's price and pace on DeepInfra | $0.080 per million prompt tokens, completion at twice; a median of 77.1 seconds in the smoke run | `results_whole/FINDINGS_WHOLE.md`, Stage B |

The figures the drafter computed (§0) have no owner yet. Stage A recomputes them,
and its record will own them.

---

## 4. Non-negotiable rules

- **No model signs.** The signature line above is Sergi's, and it lands in its
  own commit, staged by name.
- **The sessions are sequential**, one at a time, and never side by side.
- **The seed is 17, the corpus is not regenerated, and no record is
  overwritten.** Every writer goes through `harness/record_guard.py`, and the
  overwrite flag is not typed without Sergi asking.
- **The key stays in the environment**, is never printed, and is checked against
  OpenRouter's key endpoint before any call. A management key is refused.
- **No text moves after a figure exists.** §2.1's bytes are fixed before
  signature.
- **If the numbers come out badly, report them.**

---

## 5. Known traps

- **`o` contradicts itself.** It says the base is empty and the rule is the
  first, and then speaks of existing rules of another queue. A model that
  reasons may resolve it either way, and `HV-e` reads whichever it does. The
  reasoning is kept whole, and is not coded by any stage.
- **The texts could leak the policy in code.** They name neither a queue nor a
  rule (`HV-g1`), and reach the proposer through the frozen route only.
  `tests/test_oracle_separation.py` watches `halves/prompts.py` and
  `halves/ask.py` as the authority channel.
- **The first call does not know why its ticket escalated.** It is the same
  message at an impasse, a conflict or a reported error, in the loop and here
  (`reasoned_loop/protocol.py`, `Resumable.first`). Every first call is told the
  ticket is an impasse, and at the rarest queue's tickets most escalations were
  reported errors (`FINDINGS_WHOLE.md`).
- **The corpus repeats tickets.** About an eighth of its tickets are literal
  duplicates, so two tickets of `T` may carry the same attributes, and an arm the
  same prompt at both. A digest may then repeat across tickets; what it may not
  do is stand for two texts (`HV-g1`). Each ticket is still its own cluster in
  the error.
- **A wider draft holds its part too.** `HV-g` reports breadth, so a hold carried
  by drafts wider than the region can be seen.
- **The classes read the policy.** Stage C reads each ticket's governing rule and
  the true queue of every point, through `whole/paragraph.py`. The asker reads
  no label, no class and no policy (`HV-g2`).
- **An answer cut off at 16,000 tokens is invalid** unless its retry parses. One
  attempt of a first call in `PLAN_PLACEMENT.md`'s runs reached the budget.
- **DeepInfra's answers at one ticket change from ask to ask**
  (`FINDINGS_PLACEMENT.md`). The passes and the rarest queue's session measure
  that spread, which a single ask a ticket would hide.
- **Without the overlap half the first call may declare against the manual's
  identifiers.** The system prompt lets `beats` and `loses_to` cite rules of
  *"la lista de arriba"*, and the manual's list is above. In a loop the engine
  drops such a declaration (`PLAN_MANUAL.md`). `HV-g` counts them.
- **The rarest queue's session asks prompts the passes ask too.** Its
  repetitions are separate asks of the same prompt, with ids of their own, and
  only `HV-f` and `HV-g` read them. The rows over `T` read the passes alone, so
  a ticket of `T₇` weighs there as much as any other.
- **A call refused for the rate is waited out, not failed.**
  `reasoned_loop.protocol.Live` asks it again after each wait of
  `plan.RATE_LIMIT_WAIT`, and once every wait is spent the session stops
  unrecorded. `PLAN_PLACEMENT.md`'s and `PLAN_WHOLE.md`'s runs met no such
  refusal on DeepInfra.
- **A resumed session keeps each answer's own seconds.** The partial file keeps
  every row whole, its seconds included, and a resume serves the rows it holds
  without asking them again.
- **The gates may not name the record guard.** `tests/test_writer_lists.py` counts
  every module that names it as a guarded writer. So `HV-g3` reads only that the
  partial files are ignored, and that test pins the guard on `halves/ask.py`.
- **A test must not pin whether the plan is signed** (`PLAN_APPLY.md`'s lesson).
  `tests/test_halves.py` pins the count of signature lines, and the gate's
  verdicts on fake plans.
- **A float recomputed on 3.10 can differ from 3.12's in the last place.**
  Verdicts are fractions. The standard errors are floats, and only mark *thin*.

---

## 6. Blocking checks, before any record is written

`halves/gates.py`. Every writer runs them before it writes, and so does `python3
-m halves.ask --dry-run`, which builds no client and needs no key. They print
whether each check passes, and no figure.

- **`HV-g1`, the texts.**
  - **`e` is the rule arm's.** At every one of the 133 tickets the rule arm
    asked, `e`'s prompt carries the digest `PLAN_REASONED_RULE.md` recorded for
    its arm `w` there, in both passes. The rule arm's system prompt is the
    loop's.
  - **`v` is the loop's.** `v`'s messages are `reasoned_loop.protocol.messages_for`
    at every ticket of `T`. Every record of the five loop groups carries, by
    digest, the loop's system prompt and its group's paragraph.
  - **The halves.** `h` and `o` are cut and joined from `v` and `e` as §2.1 says,
    `v` comes back from them, the four differ, and none names a queue or a rule.
  - **One paragraph apart.** Every arm's message is `v`'s with the paragraph
    replaced, and every repetition asks its prompt's messages.
  - **No builder takes a row**, no digest stands for two texts, and one changed
    character moves a digest.
  - **The suite is green.**
- **`HV-g2`, the request and the instrument.**
  - **The request.** Built without a client by `placement.protocol.request_with`,
    it is the model, the messages, 16,000 tokens, temperature 0, reasoning at
    high effort and DeepInfra's pin, with `response_format` on the first
    attempt only. `PLAN_PLACEMENT.md`'s six records and `PLAN_WHOLE.md`'s three
    v1c records carry the same model, temperature, settings and pin.
  - **No label on the asker's path.** No module on it names a label, in a name
    or a string literal, by `N-g2`'s names: `halves/plan.py`, `prompts.py`,
    `population.py` and `ask.py`.
  - **The instrument.** `whole/paragraph.py`'s classes give back its record's
    counts from the closed answers, group by group. `PLAN_WHOLE.md`'s first calls
    are classed as its Stage C classed them.
- **`HV-g3`, the design.**
  - **The tickets.** `T` comes back from the closed records: 133 shared
    tickets, and 954, 982 and 1432 added. `T₇` is the corpus's seven tickets of
    `ONCALL_ESCALATION` by level 3's list, and a loop's first call met each.
  - **The asks.** 136 prompts an arm. Each pass holds every prompt once, in its
    order rebuilt from `ORDER_SEED`, and the two orders differ. The rarest
    queue's session holds its 28 prompts four times each. The smoke run holds
    two distinct prompts of each arm, outside `T₇`.
  - **The partial files** are ignored by git.
- **`HV-g4`, the signature.** It does not block a dry run, which writes nothing;
  it blocks every write.

---

## 7. Stage A — the design and the references (free, gated)

`PYTHONHASHSEED=0 python3 -m halves.sample` writes `results_halves/sample.json`:

- **the design**: `T`, every ask with its digest, and the four sessions in their
  orders; the texts, their digests and the fingerprint;
- **each ticket's governing rule** and its queue;
- **the references, ticket by ticket, classed**:
  - the rule arm's answers at the 133 tickets it asked;
  - each loop group's first calls at the tickets of `T` it escalated;
  - `HV-a`'s comparator, the DeepInfra loops' first calls under v2b's paragraph,
    pooled;
- **§0's four figures**, recomputed, and which of them did not come back as §0
  declares them.

Every session of Stage B checks that the record holds the design it rebuilds.

---

## 8. Stage B — the asks (gated on §0)

```
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session smoke
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session pass1
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session pass2
PYTHONHASHSEED=0 .venv/bin/python -m halves.ask --session oncall
```

- **The order.** The smoke run, then pass 1, pass 2 and the rarest queue's
  session, one at a time. Each session out of its turn refuses before the key.
  - **A pass** needs a smoke record in which every arm holds a valid answer, and
    every attempt that reached the model was served by DeepInfra, reasoned and
    ended `stop`.
  - **Pass 2** needs pass 1's record, and **the rarest queue's session** needs
    pass 2's.
- **Before any call**, each launch checks the signature, the turn, the key,
  `HV-g1` to `HV-g3` and Stage A's record. It refuses to write over a paid
  record.
- **The smoke run's bills** are read by generation id before pass 1, and its
  pace is set beside §1's.
- **Who launches them.** The agent, as Sergi chose (§2.5), through a supervisor
  detached from the agent's harness.
  - **What it does.** It runs the sessions one at a time, and commits each
    record alone, through the pre-commit hook.
  - **Pushing.** It pushes each record to one pull request, and retries a push
    that times out.
  - **Resuming.** It resumes a session an outage stopped.
  - **What it never does.** It never passes the overwrite flag and never skips
    the hook.
  - **Checking it is up.** A check that matches its process by command line runs
    apart from the command that launches it.
- **What the commits may show** (§0): each session's asks, failures, retries
  and seconds, and no class, share or row.

---

## 9. Stage C — scoring, and the six adjudications (free)

`PYTHONHASHSEED=0 python3 -m halves.score` reads the three records and Stage A's,
holds each to its session's asks and to this protocol, and classes every valid
answer. It writes `results_halves/score.json`.
- **`HV-a` to `HV-f`**, each with its statistic as a fraction, its line, its
  standard error, its *thin* and the readings *thin* reads, or its reason for
  having no value.
- **`HV-g`.**

The findings go to `results_halves/FINDINGS_HALVES.md`, which will own every
figure.

---

## 10. The gate, and where the code lives

`halves/` calls the packages below and edits none of them: `whole/`,
`placement/`, `reasoned_loop/`, `first_match/`, `fidelity/`, `authorship/`,
`reasoned_rule/`, `queue_alone/`, `escalations/`, `reuse/` and `rung2/`.

| module | what it does |
|---|---|
| `halves/plan.py` | the gate and the constants: the request, the pin, the tickets, the sessions, the limits and §0's lines |
| `halves/prompts.py` | the four arms' texts and messages; on the proposer's path |
| `halves/population.py` | the asks and the sessions; on the proposer's path, and it opens no record |
| `halves/gates.py` | `HV-g1` to `HV-g4`; offline |
| `halves/sample.py` | Stage A |
| `halves/ask.py` | Stage B, the only module that spends; guarded |
| `halves/score.py` | Stage C |
| `tests/test_halves.py` | the constants, the texts, the gate, the design, the request through the SDK double, Stage B on the double, and Stage C on rows written by hand |

- **The gate** reads `PLAN_HALVES.md` and no other plan, and counts every
  signature line, by `reuse/plan.py`'s count, called. **The free stages get the
  gate too**: what it protects is the order of events, not money.
- **The registries.**
  - **Code roots.** `harness/provenance.py`'s `CODE_ROOTS` carries `halves`.
  - **The authority channel.** `tests/test_oracle_separation.py` watches
    `halves/prompts.py` and `halves/ask.py`.
  - **Guarded writers.** `tests/test_writer_lists.py` counts `halves/ask.py`
    among them, and the README's table lists the three writers.
  - **Partial files.** `.gitignore` ignores them.

---

## 11. Definition of done

- **The records**, each in its own commit: `results_halves/sample.json`, the
  smoke record, the two passes' records, the rarest queue's session's, and
  `score.json`.
- **`results_halves/FINDINGS_HALVES.md`**, which owns every figure: the six
  verdicts and `HV-g`, the calls and the bills, and what the drafter's
  expectation got right and wrong.
- **The indexes.**
  - **`STATUS.md`.** The scoreboard gains `HV`'s row, *What is open* the notes on
    its second and third items, and its named lists.
  - **`IDEAS.md`.** A section on what this plan opens.
  - **`README.md` and `CLAUDE.md`.** The thread's entry and its commands.
  - **`tests/test_prose_tables.py`.** It adds `HV` to `THREADS`, and the
    FINDINGS to `TABLES`.
- **This file** gains a closing banner, which touches no line of §0 and travels
  alone.

---

## 12. What this plan cannot settle, declared before it runs

1. **What a loop compiles under `h`**, and whether it compiles the rarest queue.
   That is the loop plan this one would precede, with whichever text the rows
   favour beside v1c.
2. **Why a half cuts.** The notes and the reasoning are recorded whole, and no
   stage codes them.
3. **Texts beyond the halves.** T1 without the overlap half, a clause that says
   what the listing is for, and a paragraph that says the base exists and orders
   nested rules by containment are other plans.
4. **The system prompt's level-1 sentence**, which stays byte for byte in every
   arm, and which rung 2 read as an incentive to avoid overlap (said first).
5. **Tickets the reasoning loops never escalated**, and the 38 of the rule arm's
   that only the loop without reasoning escalated.
6. **The arrivals.** Every class reads the space. Whether a draft holds its
   part's corpus tickets, a weaker reading, is not read.
7. **One model, one provider, one manual and one period.**
