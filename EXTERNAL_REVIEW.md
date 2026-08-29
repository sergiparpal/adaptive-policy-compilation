# External review, August 29, 2026 — adjudicated against the code

**What this is.** A review of the project written from outside it, by a model that
had only the repository's public tree, contrasted line by line against the code
and the records, plus the plan that came out of the contrast.

**What this is not.** It **owns no figure**. Every number below names the record
that owns it, its surface (corpus / exhaustive space) and, where the pairwise
thread is involved, its pool (`puro` / `hibrido`). **Where this document and a
record disagree, the record wins.** Errata are dated and carried in place, never
edited away — the convention of the two documents that precede it.

**The two that precede it were read first**, as `CLAUDE.md` and §4 rule C of
[`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) require:
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) and
[`CHAT_SUMMARY.md`](CHAT_SUMMARY.md). That reading changed this document's
conclusion, and §1.4 records how.

---

## 0. The answer, in one page

An outside reader with the tree and no records produced four claims worth
keeping, three factual errors, and one recommendation that would have destroyed
the most publishable material in the repository. Adjudicating it against the code
produced one thing neither the reviewer nor this repository had: **a number
saying how much of rung 1's central failure is an encoding artifact of the
default rule rather than the thesis it is cited for.**

The corrected order of work is: settle a documentation contradiction (**done** —
the hidden policy was written by Claude, and `results/FINDINGS.md` carries the
dated erratum), measure the default-rule control (free, minutes), measure the hybrid
ceiling on the space (free, already named as pending by
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §9.2), **write up the pairwise
thread** — which is the part with the shape of a paper — and only then the
sensitivity sweep and ILP, which reinforce the frame rather than block it.

---

## 1. What the review got right, and what it got wrong

### 1.1 What survives contrast with the code

- **The Soar lineage.** Impasse-driven rule compilation is Soar chunking with an
  LLM in the subgoal slot. Correct, and [`results/FINDINGS.md`](results/FINDINGS.md)
  §Lineage already says it and says it more sharply: what was borrowed is the
  compilation mechanism, what was not is the goal hierarchy and the preferences,
  and *"Priority is declared by the system, not inferred from the shape of the
  productions"* is the diagnosis of the failure, not just the citation.
- **Step 0 as a method.** Load the correct policy into your engine and measure
  with no LLM; if it does not execute it, nothing measured over learned rules
  means anything. It voided a paid n=2000 run. This generalizes past the domain
  and is cheap enough that its absence elsewhere is a finding about the genre.
- **Representation / execution separated exhaustively.** Verified live:
  `verify_encoding()` walks all **134,400** combinations and confirms the 29 DSL
  rules equal their lambdas and that first-match-wins reproduces `true_action`
  ([`harness/ceiling_check.py:129`](harness/ceiling_check.py:129)). Not sampled.
  The failure is entirely in arbitration.
- **The audit that withdrew its own author's finding.** Built, validated against
  a policy whose optimum is 1.0000 by construction, and it withdrew rung 4's
  "change of regime" and moved rung 3 from 0.7713 to 0.8530 (corpus test);
  originals left in place beside the corrected ones. `STATUS.md`, *What was
  withdrawn, and why*, entries 1 and 4.

### 1.2 The three factual errors

1. **"Ninguna de esas piezas mueve una cifra."** False, and the sentence it
   contradicts was in the version the reviewer read: `STATUS.md` at commit
   `1d50a1a` line 35 already said *"Three failures were caught by a blocking free
   check, each of which changed a conclusion"*, and the withdrawal list was
   already there. It also contradicts the same message three paragraphs earlier,
   which praised the optimizer audit as one of the four valuable findings. **This
   is the error with no mitigation**, and the reviewer ranked it second.

2. **"Ninguna es sobre LLMs" / "deja de intentar que el proyecto diga algo sobre
   LLMs."** False, and the recommendation would have discarded the cleanest
   material in the repository — see §2. **Partly excused by the version read**:
   at `1d50a1a`, [`results3/FINDINGS3.md`](results3/FINDINGS3.md) stopped at §5,
   so §§11–15, `B-d`, the primacy effect and the 0.8647/0.6391 split did not
   exist. What did exist was rung 2's proposer characterization, which is enough
   to make the claim wrong and not enough to make the recommendation reckless.
   **This is the error the reviewer's version most excuses, and it ranked it
   first.**

3. **"La escribió un modelo"** — see §1.3, where the error turns out not to be
   the reviewer's.

### 1.3 The contradiction the review exposed by being wrong about it

The reviewer said the hidden policy was written by a model; the first adjudication
called that false, citing [`results/FINDINGS.md:107`](results/FINDINGS.md:107),
*"Over the hidden policy, written by a human"*. **That adjudication was wrong.**
[`README.md:718`](README.md:718) says, and said in the version the reviewer read:

> Having the proposer NOT be Claude is preferable: the harness and the hidden
> policy were written by Claude, and it is better for the proposer to come from
> another family.

So the claim was correctly sourced, and what exists is **a contradiction inside
the repository, load-bearing in both places**: the README uses it to justify the
proposer's family, and `FINDINGS.md` uses "written by a human" to read the
subsumption silent error of 0.0000 as *"a virtue of the author"*.

**Settled by Sergi on 2026-08-29: Claude wrote it.** `README.md:718` states the
fact and `results/FINDINGS.md:107` is false. A **dated erratum** now sits beside
that figure rather than a silent edit, per the repository's convention for a line
that interprets a figure.

The scope of the defect turned out to be one line. Every other place in the
repository — `STATUS.md`, `ARBITRATION_REPORT.md`, `CHAT_SUMMARY.md`,
`PLAN_PAIRWISE.md`, `results2/FINDINGS2.md`, `results4/FINDINGS4.md` and this
same record's own limits section — says **hand-written**, meaning *authored* as
against *accumulated by the run*, and under that meaning all of them stand as
written. No figure moves and `STATUS.md` needs no change.

**The reviewer's own restatement is what survives, and it is now the sharper
version**: the objection was never "a model wrote it", it was "the same hand wrote
the policy, the DSL and the engine being evaluated". That is the state of affairs,
and it makes `ARBITRATION_REPORT.md` §9.1's limit stricter than §9.1 states it —
which is the argument for item 5 of the plan.

### 1.4 The recommendation that was already in the repository, for the third time

The review's headline proposal — parameterize the correlation between priority
layer and condition count, and turn the finding into a curve — is a restatement of
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §9.1, which already states the
limit, already gives `CHAT_SUMMARY.md` §1's partial answer to it, and already
draws the distinction the review draws: *"Distinguishing 'falsified as a general
criterion' from 'its failure rate measured in the domain' deserves to be written
down."*

§9.8 of that report records that it re-derived three of `CHAT_SUMMARY.md`'s
corrections by another route without knowing them, and warns that the next
document may be repeating analysis the repository already contains. **This is the
third time**, now from a reader who had never seen either document. That
convergence is evidence for the objection's seriousness. It is not new analysis,
and the review's contribution here is the **instrument** — turning a written-down
limit into a measured curve — not the observation.

### 1.5 Two corrections the review made to the adjudication, both accepted

- **The impossibility is stronger than any curve, and the curve still answers
  something.** `H01` (2 conditions) must beat `H03` (1) and `H16` (1) must beat
  `H24` (2): incompatible under any criterion monotone in the number of
  conditions ([`results/FINDINGS.md`](results/FINDINGS.md) §2, route 1). No sweep
  touches that. What a sweep answers is **how frequent such pairs are in
  realistic policies** — generalization, not validity. Measured here for the
  record and owned by nothing: Spearman between layer and condition count over the
  29 rules is **−0.18**, mildly inverse rather than orthogonal.
- **The mock's asterisk does not void the comparison.** `keep_k` is handed the
  correct action by the oracle (`true_action_hint`,
  [`harness/proposers.py:87`](harness/proposers.py:87)), which disqualifies it as
  a deployable competitor and **is exactly what makes the comparison clean**: rule
  quality is fixed by construction, so what varies is arbitration alone. The
  citable form is therefore not *"a baseline can beat the ground truth"* but *"a
  rule set of uniform specificity is immune to a specificity tie-break that a
  stratified one is not"* — which is the version that generalizes.

### 1.6 The version read, established

The reviewer's account reconciles exactly. Its tree — `peldano2/`, `peldano3/`,
`peldano4/`, `RESUMEN_CHAT.md`, no `PLAN_PAIRWISE.md` — and its commit counter of
31 are commit `1d50a1a`, **2026-08-12**. The rename is `fa28d22`, 2026-08-19;
[`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md) was added 2026-08-24 in `cca6722`. A
charge that the review had skipped the pairwise thread was withdrawn: it did not
exist.

---

## 2. The synthesis neither side stated

Joining what the review dismissed with what it never saw gives one claim, and it
is a claim **about LLMs**:

> **The proposer distinguishes priority when asked about two rules, and cannot
> turn that ability into a declared order an executor can use.**

Both halves are measured, and the mechanism is measured too:

- **It works at the pair level.** Direction rate **0.7312** at 1,600 pairs
  (n 1105, space definition) against 0.6978 at 400 — 15 deviations above a coin
  ([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §11).
- **It is lost in compilation.** The order those edges compile into scores
  **0.4804** on `hibrido` / corpus test split 0, **0.40 deviations** above a
  coin, level with a free queue ranking that reads no rule (same record, §11).
- **The ceiling it is aimed at is conditional.** Rung 2's 1.0000 uses 199 edges
  derived from the *known* layer order —
  [`rung2/hidden_priority.py:4`](rung2/hidden_priority.py:4), *"Here we do know
  the layer order"*. With proposer-written edges over the learned base: e2e
  **0.0673**, abstention on **89%** of corpus test
  ([`results3/FINDINGS3.md`](results3/FINDINGS3.md) §8). Eight rung-2 runs gave 2
  conflicts and 0 accepted edges ([`results2/FINDINGS2.md`](results2/FINDINGS2.md)).
- **And the mechanism is named.** It names the **broader** rule 0.6038 of the
  time (7.98σ), against what its own explanations say; it follows a fixed queue
  ranking 0.8073 of the time (23.64σ); it has a primacy effect costing accuracy,
  0.8534 versus 0.7623 (+3.50σ) — §15. And `B-d`: **0.8647** where a free queue
  ranking already answers, **0.6391** where it cannot (n 451 and 654) — §11. Its
  accurate part is redundant with a free baseline and its errors concentrate
  exactly where that baseline is silent.

That is negative, mechanical, pre-registered in part, and has the baseline the
review spent three messages asking for. It is the opposite of *"the project says
nothing about LLMs"*, and it is the part with the shape of a paper.

---

## 3. The one new measurement, and why it is not yet a figure

**The default rule ties with every one-condition layer rule, and that is a large
part of rung 1's headline failure.** The DSL requires at least one condition, so
`H29` (`lambda c: True`) is encoded as `severity gte 1`
([`harness/ceiling_check.py:44`](harness/ceiling_check.py:44)) and therefore ties
on specificity with every single-condition rule instead of yielding to it.
[`results/FINDINGS.md:54`](results/FINDINGS.md:54) names this mechanism. **Nothing
in the repository quantifies it.**

Run in memory during the adjudication, reusing `Rule.matches` from the frozen DSL
exactly as `ceiling_check.py` does for its alternative arbitration — nothing
written, nothing frozen touched:

| arbitration, perfect policy loaded, corpus n=2000 | coverage | e2e | conflicts |
|---|---|---|---|
| specificity, as published | 0.7475 | 0.5875 | 505 |
| specificity, catch-all given its true rank | 0.8480 | 0.6880 | 304 |

**Read it as follows and no further.** The finding survives: 0.6880 is nowhere
near 1.0000, and the impossibility proof of §1.5 is untouched. But roughly 40% of
the conflicts were an encoding artifact of the default rule rather than the
priority/specificity thesis the 0.5875 is cited for, and *this is the first
question a referee asks.*

**These two rows are not figures.** They are owned by no record and produced by
no module in the tree — the situation
[`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §9.6 put itself in and then
closed. They are cited here with that warning in place, and **if they are ever to
support a conclusion they must be measured by a module first**. That is item 2 of
the plan.

**And they can never carry a signed band.** The number was seen before any band
could be drafted, so whatever record owns it declares `provenance: POST-RUN`, the
convention `edge_direction` and `edge_budget` already use, and it does not enter
`STATUS.md`'s scoreboard. A measurement that could not have surprised its author
is worth less than one that could, and that difference gets recorded rather than
assumed.

---

## 4. The plan, in order

**Ordered by a criterion borrowed twice already**, from `CHAT_SUMMARY.md` §3 by
way of `ARBITRATION_REPORT.md` §7: *what can withdraw or qualify a published
premise comes before what adds a capability.*

**Nothing here is a signed prediction.** Bands are undrafted, and a model may
draft one but may not sign it (hard rule 2). Items 4 and 5 are the only two whose
figures do not yet exist and which therefore *can* be pre-registered; items 2 and
3 are post-run and item 3 is a write-up.

### 1 · Settle the authorship contradiction · free · ~~one word~~ **DONE 2026-08-29**

§1.3. Sergi settled it: Claude wrote the hidden policy, so `README.md:718` states
the fact and `results/FINDINGS.md:107` is false. The erratum is dated and in place
beside the figure it heads; no figure moved and no other document needed touching.
It found the defect in the first pass an outside reader made, which is the
argument for item 6 of §5.

### 2 · The default-rule control · free · minutes · POST-RUN

§3. A module that measures the ceiling under specificity with the default rule
given its true rank, alongside the published encoding, so the pair is
reproducible and owned. It belongs to the same family as `rung3.optimizer_check`:
**it measures the instrument, not the material.**

Constraints, all of them binding: `harness/` stays frozen (hard rule 1), so the
alternative ranking lives in the new module and reuses `Rule.matches`, exactly as
`ceiling_check.py` does today; the record declares `provenance: POST-RUN`; the
published 0.5875 does **not** move, and the new number sits beside it. A test pins
both, so neither drifts.

*Why first among the measurements:* it costs minutes, it is the first objection a
referee raises, and having it answered with a number before the question is asked
is worth more than the sweep that answers a broader version of it later.

### 3 · The hybrid ceiling on the exhaustive space · free · minutes

**Not this document's idea.** [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md)
§9.2: rung 2's 1.0000 is a corpus figure, the hybrid engine has never been
measured over the 134,400 combinations, and that report calls it *"the cheapest
pending check of all the ones named here"*. It carries no erratum, so it is still
open. `rung2/ceiling_check2.py` already builds the engine and already constructs
`Space()`; what is missing is the second index set and a record that owns the
figure.

*Why here:* §2's claim leans on the 1.0000, and the repository's own sharpest
result is that the two surfaces neither rate nor rank alike
([`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), parts two and
three; Spearman 0.34 over 2,080 pairs). An unlabelled ceiling is the one thing
`STATUS.md`'s *Before reading any figure* says not to leave standing.

### 4 · Write up the pairwise thread · free · the actual deliverable

§2. The material is complete: `PLAN_PAIRWISE.md` and `PLAN_PROPOSER_1600.md`
closed, seven signed rows adjudicated, §§6–15 of
[`results3/FINDINGS3.md`](results3/FINDINGS3.md) written, every record in
`results2/` and `results3/`. Zero further calls.

What the write-up has to carry, because it is what makes it worth reading: the
pair-level result **and** the compilation-level result as one claim rather than
two; the free queue-ranking baseline that makes the second interpretable; `B-d`
as the mechanism; §14's narrowing of `B-b` (a perfect follower of the queue
ranking scores 0.4402 at this budget because 1,479 pairs are 4.6% of the 31,850
that could carry an edge — the row stays refuted as signed and means something
narrower than it reads); and the surface/pool labels on every number.

*Why before the sweep:* the sweep strengthens rung 1's frame. This is the result.
`ARBITRATION_REPORT.md` §8's last rule-out — do not build more apparatus before
having material — and the reviewer's independent "rung 5" warning converge here:
**the value already present is extracted by writing it, not by adding a step.**

### 5 · The sensitivity sweep · free, deterministic · pre-registrable

§1.4 and §1.5. Parameterize the correlation between priority layer and condition
count over a family of synthetic policies, and plot engine accuracy against it.
It answers **generalization, not validity** — how often the falsifying shape
occurs, not whether specificity fails, which is settled by impossibility.

What it costs that the review did not price: `harness/hidden_policy.py` is frozen
(hard rule 1) and the corpus is frozen (hard rule 4), so the family lives in a new
package outside `harness/`, as `rung2/` did, and each synthetic policy needs its
own labelling. Free and deterministic, but not an afternoon of `sed`.

**This one can and should be pre-registered**: its figures do not exist, so a
`PLAN_*.md` with bands and refutation lines, signed by Sergi in its own commit
before anything runs, is available here in a way it was not for item 2. That plan
travels alone (hard rule 2; `.githooks/pre-commit` rejects the accompanied
version).

### 6 · ILP as a competitor · free, specified, **not authorized**

Step B of rung 3, never run. `STATUS.md` lists it open and *still unauthorized*,
which under this repository's convention means the scope is Sergi's to open, not
a task to pick up. Recorded here as the reviewer independently reached it, and
left where `STATUS.md` has it.

---

## 5. What this document does not do, and what it owes

1. **It has executed one thing**, the two rows of §3, and they are declared
   unowned there. Everything else is a reading of records and of code, each figure
   attributed to the record that owns it.
2. **It could not settle §1.3 by itself.** Which of the two documents stated the
   fact is not derivable from the tree — git authorship reads the same either
   way. Sergi closed it on 2026-08-29 and the erratum is in place; the limit
   recorded here is that this document had no way to reach that answer alone.
3. **The reviewer's two literature citations** (RimRule, ANNEAL) were not
   verified. They are external to the repository and nothing here rests on them.
4. **This document is the third re-derivation of §9.1**, by the reviewer's route,
   and says so in §1.4 rather than presenting the sweep as new. The next document
   reads these three before it is written.
5. **It is indexed, in the same commit that adds it.** The two analytical
   documents that precede it were indexed nowhere until commit `e1d1db3` fixed
   exactly that, and landing a third unindexed one would repeat the defect that
   commit closed. It is in `README.md`'s structure tree and in its section, whose
   title is now *Three documents that read the records instead of adding to
   them*; `CLAUDE.md`'s pointer names all three. **`PLAN_SENSITIVITY.md` is
   deliberately not indexed yet**: it is unsigned, and the repository indexes a
   plan when it is operative.
6. **One process observation, which is the reviewer's and is worth keeping.** The
   contrast that produced §3 came from handing an outside reading to something
   with repository access and instructions to verify. It found an encoding
   artifact in a headline figure that neither party would have found alone. It is
   worth repeating against what this repository writes, not only against what
   comes in from outside.
