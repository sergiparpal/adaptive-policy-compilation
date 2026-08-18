# Conversation summary — August 11, 2026

**Nature of this document:** it is the summary of a conversation about the
experiment, not an official record. **No figure here has its home in this
file**: the figures cited belong to the FINDINGS that own them and to
`STATUS.md`, which indexes them. If any of them differs, the record wins. The new
measurements (§2, item 1) are unofficial ad hoc *probes*, reproducible for free,
deliberately not recorded in `results*/`.

**Reviewed on August 12, 2026.** Every figure cited was verified against the
record that owns it and **none had drifted**; the §2.1 *probe* reproduced
exactly. What failed was the reading, in three places, and it goes corrected
below with its dated erratum and the original text preserved, as in the FINDINGS:

- **§2.1** did not name its surface, and on the other one the conclusion is much
  stronger. The missing measurement is added.
- **§2.2** cited the favourable half of FINDINGS2's evidence, and the trigger it
  proposes is left without material. The amendment is added.
- **§4** chains figures from different engines: there is no broken link, there
  are four unmeasured ones.

The §3 table was reordered for that reason. In §1 the pool and surface labels
that the record already carries and this summary omitted were added —
`0.8530` is from the **pure pool**, with subsumption off, and that is where §4's
error starts.

**Updated on August 14, 2026, for status only.** Row 1 of §3 was still asking for
an experiment executed on the 13th, which `STATUS.md` had already moved out of
its open items: it goes marked in place, with a pointer to the record that owns
it. This is **not** a re-verification of the document —no figure was checked
again—; the August 12 review is still the last one.

**Corrected on August 17, 2026, in one place: the scoreboard of row 2 of §3.** No
figure was checked again here either; what fails is again the reading, and it is
the same one §4 dismantles three sections below — the scoreboard does not name
its pool, and by default it names the wrong one. It goes with its erratum in
place. Added as well is the caveat that the order metrics of August 15 and 16
impose on any single-number scoreboard, which did not exist when the row was
written.

---

## 1. Conclusions that were reached

**On the architecture and its four rungs:**

- The priority of a stratified policy **is not in the shape of the rules**:
  neither by counting conditions (0.5875 with the perfect policy loaded), nor by
  age, nor by semantic subsumption. They are not bad metrics: the information is
  not there. Priority is a relation *between* rules and enters only through an
  external channel: declaration, feedback or authority.
- **The mechanism for executing declared priority works perfectly** (e2e 1.0000,
  hybrid engine — subsumption + declared edges — **over the hidden policy of 29
  rules**). The problem was never execution; it is source: nobody supplies the
  declaration.
- **The proposer partitions instead of stratifying.** Seeing the base cut the
  overlap 10x; the explicit instruction to overlap (prompt v2) moved the numbers
  (1.6% → 7.25%) but not the operation, and the notes boasting of disjointness
  rose from 22% to 55%.
- **The material was much better than it looked**: the same 577 rules that rung
  1's arbitration turned into 0.18 admit an order of 0.8530 (**pure pool** —
  subsumption off —, corpus test, audited optimizer, and the search uses the
  oracle). Under the hybrid engine that same base gives **0.7734**. But two
  classes (T3_ENGINEERING, ACCOUNT_MANAGER) lack correct material: a material
  problem, not an ordering one.
- **From realistic feedback (errors only) 61% is recovered** of what full
  supervision gives, and the signal self-extinguishes: the better the system
  works, the fewer errors it makes, the fewer corrections arrive, the less it
  learns.

**On the epistemological discussion (the hidden policy as "the truth"):**

- The hidden policy does not need to be "the right one in the universe": it is
  **THIS company's manual**. What is measured is whether a structured function
  can be recovered from experience, not whether the policy is good. The same
  criterion with the same oracle gives 0% error over the hand-written policy and
  53% over the learned base: the variable is the structure of the material, not
  the author nor the objectivity of the truth.
- **Conflict is not the enemy: it is the alarm.** Partitioning does not eliminate
  the errors — it eliminates the error detector. The clean partition of 6 rules
  with silent error 0.7553 is the proof: zero conflicts, silent disaster.
- Subsumption failed over the learned base for two distinct reasons: there was
  hardly any nesting to detect (5.17% of the pairs), and when there was, it
  crowned narrow but wrong rules. **Narrow ≠ correct.**

## 2. What the conversation added and was not spelled out in the project

1. **The measurement of "the newest rule wins".** Rung 1's FINDINGS said
   conceptually that arrival order runs backwards from the correct one, but it
   never measured the reverse. Measured in the conversation (ad hoc probe, full
   corpus, unofficial protocol): **0.542 against 0.5115** for born_at and 0.417
   random. Right direction, small magnitude: exceptions are born late, but most
   new rules are not exceptions.

   > **[ERRATUM 2026-08-12] Two things: the reverse WAS measured, over another
   > object, and this probe did not name its surface.**
   >
   > **(a)** `results/FINDINGS.md` §2 publishes `reverse order 12.8%` — over the
   > **hidden policy** loaded into the engine, where reversing the design order is
   > catastrophic by construction. What had never been measured is the reverse
   > **over the learned base**, which is what this probe measures. The sentence
   > "never measured the reverse" is false as written and true in its intent.
   >
   > **(b)** The probe reproduces exactly — full corpus, 2000 cases, pure pool —
   > and adds the deviation it did not report:
   >
   > ```
   >   born_at               0.5115
   >   born_at REVERSED      0.5420
   >   random (mean of 50)   0.4172   sd 0.0711
   > ```
   >
   > The advantage of the reverse is **+0.0305** against a deviation of the random
   > order of **0.0711**: less than half a deviation. On the corpus this is not an
   > improvement, it is a sign. Measured over the exhaustive space — the surface
   > `STATUS.md` has required naming since August 8, and which the
   > conversation did not measure:
   >
   > ```
   >   born_at               0.3148
   >   born_at REVERSED      0.5668
   >   random (mean of 50)   0.3768   sd 0.1026
   > ```
   >
   > **+0.252, and almost two deviations above random.** The hypothesis was
   > correct and was being defended on the surface where it is weakest. The honest
   > reading splits in two: the reverse is a much better approximation **to the
   > policy**, and barely better as a **deployment default**, because the corpus is
   > the deployment distribution according to the project's own framing. It is
   > exactly the mechanism the `FINDINGS3.md` erratum describes: the rules born
   > early are defaults fitted to the common distribution, which is what the corpus
   > rewards and a uniform measure does not.
   >
   > **What the conversation did not see.** 0.5668 **without a single label and
   > without any search** beats the record's greedy carried onto the space (0.4931)
   > and comes close to the local search fitted on the corpus train (0.6105), which
   > does use the oracle. That says something considerably stronger than "a free
   > improvement over born_at": a label-free heuristic recovers most of what a
   > search with an oracle recovers, on the surface that asks whether the order
   > *is* the policy.
   >
   > Same status as the original probe: unofficial protocol, nothing written to
   > `results*/`.

2. **The concrete proposal of pairwise judgement**: not asking the LLM to write
   overlapping rules, but detecting the conflict and asking it "which of these
   two should win?". The base evidence is in FINDINGS2 (it reasons relationally
   when it has two operands); the design of the experiment is a synthesis of the
   conversation.

   > **[ERRATUM 2026-08-12] The evidence cited is the favourable half, and the
   > proposed trigger is left without material.**
   >
   > FINDINGS2 gives two reasons for the failure not being one of capability. This
   > cites the first — it reasons relationally: it cites rules by identifier and
   > argues about them. **The second is an experiment and it runs against**: v2
   > handed it the arithmetic of the overlap already resolved by the engine and
   > **five of the fourteen badly proposed edges are from v2**, three of them in
   > escalations where the neighbourhood explicitly marked which conditions each
   > cited rule failed. *"With the right information in front of it, it makes the
   > same mistake"* (`results2/FINDINGS2.md`).
   >
   > Worse for this design in particular: the only two times a real CONFLICT
   > reached the proposer — exactly the situation the experiment wants to create —
   > it answered with **zero edges** once and **failed the parse** the other.
   > **0 of 2.** It is not a refutation (n=2, and the elicitation was not a direct
   > question), but it is the closest thing to evidence there is and it does not
   > point where this item says.
   >
   > And the trigger runs dry: **2 conflicts in 8 runs**. Triggering on CONFLICT at
   > run time is the same drought that left `EDGE_CONTRADICTS` measuring nothing in
   > eight runs. As written, the experiment **does not repair the link: it is the
   > link**.
   >
   > **Amendment, which leaves it cheaper and with a scoreboard.** Trigger on
   > **extension overlap**, computed offline over the 134,400 cases — the engine
   > already computes it for the v2 neighbourhood —, not on conflict at run time.
   > And run it **offline over the base of 577 rules that is already paid for**,
   > where the order searched with the oracle (0.8530, pure pool, corpus test)
   > gives a scoreboard to score the order the LLM declares against, and born_at
   > (0.5115) gives the floor. No new shadow loop, no corpus spend and no
   > dependence on first getting a base with overlap — which is the circular
   > dependency that sank the original version.

3. **The matrix with the empty cell**: "base with healthy overlap + subsumption"
   is the combination never measured — prompt v2 ran on the subsumption engine
   but never gave it material (2 conflicts in 8 runs, 0 edges accepted).
4. **The connection "specificity measured another way = subsumption"**: the
   intuitive refinement (not counting conditions but measuring specificity for
   real) is exactly the path the experiment already walked, with its reason for
   failure documented.
5. **The framing "partitioning kills the alarm"**: the design had the escalation
   trigger only on impasse/conflict; the formulation that disjointness eliminates
   the error detection mechanism comes from the conversation.

## 3. What could be done to carry on (by cost/value ratio)

**Reordered on August 12, 2026.** The original order was 1-6, just as it now
reads in the "was" column. It changed for three reasons: what can **withdraw** a
published premise comes before what can add a capability; pairwise judgement
drops because in its original form it depended on getting a base with overlap and
in the amended form (§2.2) it no longer does; and reversed born_at stops being
sold as a deployment default, which is what the §2.1 erratum does not support.

| # | was | experiment | cost | what it would discover |
|---|---|---|---|---|
| 1 | 4 | **Re-run `budget_and_balance`** with the audited optimizer: **executed on August 13, 2026**, not pending | already done · 0 calls | it was: whether "50 labels are enough" survives, the premise on which rung 4 was opened. Step 3 of the audit measured it — [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), "Step 3 result — August 13, 2026" —, which is the record that owns those figures |
| 2 | 1 | **Pairwise judgement, in §2.2's amended form**: trigger on extension overlap, offline, over the 577 rules already paid for | cents | whether the proposer can *declare* priority even if it does not *write* it. Scoreable against 0.8530 above and 0.5115 below, without depending on getting a base with overlap |
| 3 | 2 | **Another model** (same prompt v2, several seeds averaged) | cents | discriminates "it is DeepSeek" vs "it is the elicitation"; informative either way |
| 4 | 3 | **Show the ceiling's gaps** to the proposer ("here you have no correct rule") | cents | whether it fills in the material missing in T3/ACCOUNT_MANAGER (open in `IDEAS.md`). It is the only one that attacks the material problem, which no priority mechanism touches |
| 5 | 5 | **ILP (Popper/ILASP) as a competitor** | free, specified, not authorized | if an inducer with no LLM recovers the layer order, what is the proposer for? |
| 6 | 6 | **born_at reversed**: already measured in §2.1, not pending. What is left is deciding **what it is** | already done | on the space, +0.252 with no labels and no search; on the corpus, within the noise. It is not a deployment default: it is the cleanest evidence that born_at encodes the distribution and not the policy |

> **[STATUS 2026-08-14] Row 1 is executed, and with it three of the things it
> claimed are spent.** Step 3 of the audit ran it on August 13, 2026; its results
> and its dated erratum live in
> [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md) and in
> [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §4, which are the records that
> own them. They are not copied here, for what this document's header says.
>
> **(a)** It is no longer "`STATUS.md`'s open item nº 1": that index moved it to
> the established and its list of open items now starts with something else.
> **(b)** It is no longer "the only item that can withdraw a published figure",
> because it withdrew one; the rest of the table adds capability, it does not take
> it away. **(c)** The cost estimate the row carried —clock and number of
> configurations— is not the one that came out; the real one is in the record,
> section "What it costs, and what it does not settle".
>
> The row is left in place and the table unrenumbered: taking it out would erase
> the reason it was reordered on August 12, which is written just above.

> **[ERRATUM 2026-08-17] Row 2 commits in its scoreboard the error §4 corrects.**
> The row says pairwise judgement is *"scoreable against 0.8530 above and 0.5115
> below"*. **Neither of the two figures carries its pool, and by default they are
> the ones of the wrong pool.**
>
> `0.8530` is a **pure** total order, with subsumption off. But what this
> experiment produces are **declared edges**, and edges are consumed in the
> **hybrid** engine, which is the one that has them. Over that same base and that
> same pool, the order searched with the oracle gives **0.7734** and the coverage
> bound is **0.8540**, not 0.9010 (`results3/order_search_ls.json`; owned by
> `results3/FINDINGS3.md` §1 with its erratum and `results3/FINDINGS_AUDIT.md`).
> Scoring a hybrid result against 0.8530 inflates the bar by some **0.08** by
> reading another engine's surface — which is, under another name, the chaining of
> figures from different engines that §4's erratum (a) dismantles. Written three
> sections before dismantling it.
>
> The floor has the same problem and is worse besides: `born_at` **0.5115** is
> pure pool and full corpus. **Over the hybrid pool it is not measured.**
> Measuring it is free and it is the experiment's first step, not a presentation
> detail.
>
> **The correct scoreboard, then, depends on which engine consumes the output:**
>
> | if the edges are consumed in… | ceiling with oracle | bound | floor |
> |---|---|---|---|
> | the **hybrid** engine (subsumption + edges) — the default case | **0.7734** | 0.8540 | **not measured** |
> | a **pure** total order, compiling the edges to an order and switching subsumption off | 0.8530 | 0.9010 | 0.5115 |
>
> Corpus test except the floor, which is full corpus. The row is left as written,
> with this erratum beside it, for the same reason row 1 was left.
>
> **[ADDED 2026-08-17] And a single-number scoreboard is weaker than could be
> known on August 12.** The order metrics of August 15 and 16
> (`results3/FINDINGS_ORDERS.md`, which owns them) establish that 0.8530 and
> 0.7734 are **the best of 65 starts**, and that the 65 end orders are **65
> distinct behavioural machines**. Comparing a declared order against that maximum
> is comparing it against a winning ticket, not against a level. The honest
> comparison is against the **distribution** of the 65, which is already
> regenerated in `results3/order_metrics.json` and costs nothing to read again.
> This does not withdraw the row: it makes it cheaper, because a comparison
> against a distribution tolerates an intermediate result and one against a
> maximum does not.

## 4. Is there hope that the experiment does not end without success?

Yes, in two different ways:

**It already succeeds as a map.** The original question (does it reuse or
memorize?) still has no clean answer, but the project has delimited exactly why:
where the structure lives (priority), which channels carry it and how much each
one loses (declaration: never arrived; feedback: 61% and it runs out), and which
part of the problem is material and not ordering. A well-measured negative result
is a result (rule 6).

**And there is a real open path to positive success.** The chain has only one
broken link: *getting a base with real overlap*. If pairwise judgement (or
showing the gaps, or another model) repairs it, everything else is already tested
and works: the hybrid engine executes at 1.0000, the audited search extracts
0.8530 from the material, and the feedback channel contributes its 61%. The
experiment is not dead: it is **one link** away from closing the chain, and for
the first time it is known exactly which one.

> **[ERRATUM 2026-08-12] This chains figures that are not chainable. There is not
> one unmeasured link: there are four.** It is the claim that carries the most
> weight in the document and it is the one that holds up worst against the
> records.
>
> **(a) 1.0000 and 0.8530 are different engines.** The 1.0000 is the **hybrid**
> engine — subsumption + declared edges — over the **hidden policy of 29 rules**.
> The 0.8530 is a **pure** total order, with subsumption off, over the 577 learned
> ones. Under the hybrid engine that same base gives **0.7734**
> (`results3/FINDINGS_AUDIT.md`), and subsumption leaves **181 of the 577 rules
> matching nothing** on the train. Repairing the overlap does not hand you an
> engine at 1.0000 over a learned base: "why rung 2's hybrid arbitration is worse
> than the pure order over a learned base" is still open in `IDEAS.md`, and the
> audit says it stays worse with a competent optimizer and by a wider margin.
>
> **(b) The 61% is not a multiplier of 0.8530.** It is a gain over born_at
> (+0.2011 of +0.3273), measured over the same old base. The two figures neither
> multiply nor compose.
>
> **(c) Both were measured over rung 1's base.** A new base with real overlap is
> different material; neither 0.8530 nor the 61% travels with it.
>
> **(d) The material problem does not move.** §1 says T3_ENGINEERING and
> ACCOUNT_MANAGER lack a correct rule in two thirds of their cases, and here it is
> written that "everything else is already tested and works". No priority
> mechanism touches that.
>
> And the 0.8530 uses the oracle, which §1 does label and this paragraph drops.
>
> **What is left standing.** The first paragraph of this section — success as a
> map — none of this touches. Nor the direction: there is a path and it is cheap.
> What does not hold is the arithmetic, and with it the "one link away". Four
> unmeasured things, three of them identified, is a considerably better place than
> rung 1; it is not the edge of closing the chain.

Informed bet from the conversation: success, if it comes, will not come from a
smarter model nor a better prompt, but from **changing the question that is put
to the LLM** — from "write the rule" to "judge this pair". It is the cheapest
thing to try and it is the only thing rung 2's evidence says the proposer already
knows how to do.

> **[ERRATUM 2026-08-12]** The bet is still reasonable and is still the cheapest,
> but "the only thing rung 2's evidence says the proposer already knows how to do"
> is more than the evidence says: see the §2.2 erratum — with the arithmetic
> resolved in front of it, it repeated the mistake, and the two times a real
> conflict reached it, it declared nothing. Bet with a low prior, not conclusion.
