# Priority arbitration in `adaptive-policy-compilation`

A report on the question *"which rule wins when several match and disagree?"*, written
against the repository's records as of `STATUS.md` (2026-08-16).

**Convention, and this report applies it to itself.** Every figure names two things: its
**surface** —**corpus** (arrival distribution, n=2000, seed 17) or **space** (the 134,400
combinations, uniform measure)— and the **record that owns it**. The two surfaces are not
interchangeable and do not even rank the same. **This report publishes no figure for the
first time**: they all live in a `FINDINGS` with its erratum beside it and in `STATUS.md`,
which indexes them; here they are only cited with their pointer. What is **established**
goes with its record; what is **proposed** goes marked as such and with a falsifiable
prediction, never mixed with what is measured.

---

## 0. The answer, in one page

The priority of a stratified policy **is not a datum derivable from the rules: it is
external information that somebody has to supply**. The only legitimate question is who, in
what format and when they are asked. Out of that comes a four-step ladder, in this order and
no other:

1. **What the semantics dictates.** If `ext(A) ⊊ ext(B)` and they disagree on action, A
   wins. It is derived, not declared, and **partial**: over the 29 rules it orders 61 of the
   406 pairs, 15%. But **it is not free**: over a hand-written policy it is sound and
   costless; over the learned base of 577 rules it *lowers the coverage bound itself* from
   0.9010 to 0.8540 and the searched order from 0.8530 to 0.7734 (corpus test), because it
   takes correct rules out of the running. §3, level 1. **This correction is not this
   report's**: erratum (a) of §4 of `CHAT_SUMMARY.md` made it on August 12, 2026, and here
   it was re-derived by another route without knowing that.
2. **The residue is declared, in referential edges between concrete pairs**, never in a
   global integer. Measured: subsumption plus 199 minimal edges over the hidden policy give
   e2e **1.0000**, silent error 0.0000, zero conflicts, zero impasses **over the corpus** —
   over the space that engine has never been measured.
3. **If nobody declares, it is searched, learned or inherited from the structure.** Search
   over labelled cases: **0.8530** (corpus test) against a coverage bound of 0.9010.
   Learning from asymmetric feedback —the only kind a deployed system produces—:
   **+0.2011** over `born_at`, 61% of what full supervision buys (corpus test). And below
   the two, **a channel with no labels and no oracle** that this report did not contemplate:
   reversing the birth order of the learned base gives 0.5668 over the space, above the
   record's greedy carried there and close to a search that does see the oracle. §2, and
   read it with the warning it carries: it is the only figure in this document with no
   record that owns it.
4. **When nothing resolves it, abstain.** `CONFLICT` is not an engine failure: it is the
   only way for the error to be measurable instead of silent. And it is not a concession:
   **a base that never enters conflict does not make fewer errors, it makes them in
   silence**, with a measured case that demonstrates it (§3, level 3).

And two warnings worth as much as the ladder:

- **The execution mechanism is not the bottleneck.** Rung 2's engine already gives 1.0000
  over the corpus with a perfect author. What is missing is **material**: in eight runs the
  proposer generated 2 conflicts and 14 edges, none accepted.
- **The order is not identified by the objective.** Orders that score the same are
  different machines. That makes the *verification* problem harder than the arbitration
  one, and no arbiter architecture solves it.

---

## 1. What the question is exactly

Given a case, the engine computes the set of rules that match and returns one of three
outputs: `IMPASSE` (none matches → a **coverage** problem), `ACTION` (one wins) or
`CONFLICT` (several match and disagree → a **priority** problem). This report's question is
the third output, and it is worth not confusing it with the first: they are two distinct
deficiencies and a system can have perfect coverage and broken priority.

The separation the project makes and that any redesign has to sustain:

> **Representation ≠ execution.** Over the space's 134,400 combinations, the 29 rules
> written in the DSL are equivalent to their original predicates, and evaluating them with
> *first-match-wins* reproduces the exact policy. The DSL loses nothing. What was failing
> was the arbiter.

That verification —pinned by `tests/test_encoding_invariant.py`, not merely published— is
what turns "the system is going wrong" into "the system **executes badly a policy it
represents well**", which is a much stronger and much more actionable claim. Any arbitration
diagnosis ought to start by reproducing it: if the representation is not clean, you do not
know what you are measuring.

---

## 2. What was falsified: priority is not in the shape of the rules

Three syntactic criteria, with the **perfect** policy loaded and no LLM involved (corpus,
`results/FINDINGS.md`):

| criterion | result | why it fails |
|---|---|---|
| **Specificity** (the one with most conditions wins) | e2e 0.5875, silent err. 0.2140, CONFLICT 25.3% | priority and number of conditions are nearly orthogonal |
| **Arrival order** | 100% in design order, 12.8% reversed, **49.3%** random — **all three over the hidden policy**, not over a learned base | it has no content of its own: it carries whatever order you give it |
| **Subsumption** | silent err. **0.0000** (hand-written policy) / **53.12%** (learned base) | it measures a virtue of the **author**, not of the criterion |

**Specificity's impossibility is a proof, not a measurement.** Within the policy itself: H01
(2 conditions) must beat H03 (1), and H16 (1) must beat H24 (2). No monotone function of the
number of conditions satisfies both. It is not a badly set hyperparameter; it is a
representational impossibility.

**The generalizable form of the failure**, which is what one carries to another domain:
*specificity works if and only if the exceptions are **refinements** of the rules they
override.* It inverts as soon as the policy has a layer of **broad overrides** on top
—security, compliance, on-call—, which by nature are written with few conditions, while the
narrow special-case rules live at the bottom. It is worth saying with the right vocabulary:
**at the top there are broad overrides, not defaults**; the defaults are at the bottom and
are sometimes the most specific in the base. That is the normal shape of a business policy,
not a pathology of the case study.

**The diagnostic signature, which is exportable.** Under the specificity engine,
`keep_k(k=4)` —a coarse grid of 4-condition rules— **beats the hidden policy**. Not by being
a better policy: by being immune to the inversion, since with uniform specificity the arbiter
can never invert and the tie-break falls to `born_at`. Hence the practical rule:

> **If a dumb baseline beats your oracle, your arbiter is inverting priorities. It is not
> the policy that is wrong.**

**The arrival-order row misleads if it is read without its label.** The 12.8% is what the
reversed order scores **with the hidden policy loaded into the engine**, where reversing the
design order is catastrophic by construction: it is a tautology backwards, not a measurement
of the criterion. The measurement that matters —reversing the birth order of the **learned
base**— says something very different, and it comes out in favour:

```
                         corpus       space
  born_at                0.5115       0.3148
  born_at REVERSED       0.5420       0.5668
  random (mean of 50)    0.4172       0.3768   sd 0.0711 / 0.1026
```

Over the corpus the advantage is half a deviation: a sign, not an improvement. Over the
space it is **+0.252 and almost two deviations**, and that figure leaves the reversed order
**above the record's greedy carried onto the space (0.4931) and close to the local search
fitted on the corpus train (0.6105), which does use the oracle**. Without a single label and
without searching anything.

> **A warning about these figures, and it is the only one of its kind in the document.**
> They come from an ad hoc *probe* in `CHAT_SUMMARY.md` §2.1, whose own header declares them
> unofficial protocol and not recorded in `results*/`. **They have no record that owns
> them**, and the script that produces them is not in the tree. Its three baselines do
> verify: 0.3148 and 0.3768 are exact against the `FINDINGS3.md` erratum; 0.5115 and 0.4172
> are *full corpus* and must not be mixed with the record's 0.5216 / 0.4227, which are
> corpus *test*. The two figures of the reversed order are the ones left unconfirmed.
> Reproducing them costs minutes and zero calls.

> **[ERRATUM 2026-08-24] Measured. All six reproduce, the block now has an owning record, and
> the strongest of the six is a PURE-POOL figure.**
>
> `rung3/floor_by_pool.py` → `results3/floor_by_pool.json`, run with `PYTHONHASHSEED=0`, zero
> API calls. Its six-row gate reproduces every baseline this warning already accepted, and the
> two it left unconfirmed come out exactly as cited: **0.5420** over the full corpus and
> **0.5668** over the space, both pure pool. The paragraph above stands as written. The
> sentence "they have no record that owns them" no longer holds for any of the six, and
> §9's point 6 carries its own erratum saying so.
>
> **What the new record adds, and it qualifies the reading rather than the figures.** The
> comparison chain above is pure-pool throughout and internally consistent — 0.4931 is the
> record's greedy carried onto the space and 0.6105 the local search fitted on corpus train,
> both `puro`. Over the **hybrid** pool, which is the machine where declared edges live, the
> same reversal is worth almost nothing:
>
> ```
>                                        puro    hibrido
>   born_at, space                     0.3148     0.4257
>   born_at REVERSED, space            0.5668     0.4373
>   gain from reversing               +0.2520    +0.0116
> ```
>
> The shape survives the change of pool and the magnitude does not: on `hibrido` the reversed
> order still sits above the greedy carried onto the space (0.4332) and below the local search
> (0.4970), but it clears the greedy by 0.0041 instead of 0.0737. **"Without a single label
> and without searching anything" is a statement about the pure pool.** The two pools are
> different machines and their figures never chain, so this neither corrects the paragraph
> above nor extends it — it says which machine it is about. `results3/FINDINGS3.md` §6 owns
> the figures.

What it means, carefully: **arrival order does not lack signal, it lacks a sign.** The rules
born early are defaults fitted to the common distribution —what the corpus rewards and a
uniform measure does not—, so reversing it is a much better approximation *to the policy*
and barely better as a *deployment default*. Rung 1's conclusion about this criterion still
stands as it was written, over the object it was written about; what does not hold is
extending it to "age is good for nothing".

**Subsumption's trap deserves a paragraph of its own** because it is the finding easiest to
misread. The 0.0000 over the hand-written policy does not validate the criterion: it
validates the author, who respected the convention "narrow rule = exception to the broad
one". A proposer that writes ticket by ticket does not respect it —a narrow rule of its own
can be an overfitted default— and there the same criterion gives 53.12% silent error.

**That 53.12% has to be cited with its denominator**, because without it it reads as four
times worse than it is and as four times better at once. Over the learned base, subsumption
only commits on **160 of 2000 cases** (coverage 0.0800); the 53.12% is **85 errors over
those 160**, and the resulting e2e is 0.0375. That is: the criterion does not turn reckless,
it turns mute, and when it speaks it is wrong more often than a coin.

And they are **two** failures, not one, and it is worth not fusing them because they have
different remedies: over the learned base there is hardly any nesting to detect —**5.17% of
the pairs**, against 15% for the hand-written policy— and, when there is, it crowns narrow
and wrong rules. **Narrow ≠ correct.** The semantic level does not only get it wrong over a
base with no author: it orders relatively less than over one with an author. **Subsumption
is not free; it is free conditional on a discipline of authorship.** Proposal **P3** comes
out of that.

---

## 3. The correct shape of the answer

The arbitration that works is **a semantic partial order plus a declared totalization**,
both in the same graph, plus abstention.

### Level 1 — Subsumption

`A ≺ B` if `ext(A) ⊊ ext(B)`, computed as a bitmask over the exhaustive space. It is
derived, not declared. It is **partial**: 61 of 406 pairs over 29 rules.

**And it is not a free level: it is a design decision with a measured price.** This was
established by erratum (a) of §4 of `CHAT_SUMMARY.md`, dated August 12, 2026, against a
document claiming to be "one link" from closing the chain; here it was re-derived from the
records by another route and without knowing it, which serves as cross-confirmation and not
as a new finding. Over the learned base of 577 rules, switching subsumption on as a
non-overridable level costs this (`results3/FINDINGS3.md` §1 and its erratum of 2026-08-08;
`results3/order_search_ls.json`):

| pool | coverage bound (corpus) | searched order (corpus test) | the same order over the space |
|---|---|---|---|
| pure (total order only) | 0.9010 | **0.8530** | 0.6105 |
| hybrid (subsumption + order) | 0.8540 | **0.7734** | 0.4970 |

The 0.047 is lost **in the bound**, not in the search: subsumption takes correct rules out
of the running before there is any order at all. The mechanism is told in
`results3/FINDINGS_AUDIT.md`, step 1: once subsumption prunes, **181 of the 577 rules match
absolutely nothing** on the train. A third of what the proposer wrote is unreachable by
construction, before any question of order. And it is not optimizer weakness: the hybrid
stays below under the audited optimizer, by a wider margin than under the greedy.

That leaves level 1 in a more uncomfortable and more honest place than "non-negotiable":

> **Over a base with a discipline of authorship, subsumption is free and sound order. Over a
> learned base without that discipline, it is a filter that costs 0.047 of bound and
> silences a third of the rules.** If it is kept non-overridable —and there are reasons to
> keep it, it is the only part of the order derived from the semantics— it has to be kept
> *knowing the price*, and that price is what P3 tries to stop paying.

Why it still deserves to be the base level despite the price: it is the only one no proposer
can fake, the only one that does not have to be verified against anything, and the one that
gives the 61 pairs without spending a single question. What does not hold is presenting it
as costless.

### Level 2 — Referential edges, not integers

`{"beats": ["R0007"], "loses_to": ["R0021"]}`. The four reasons why this beats a
`priority: 17` **are those of `rung2/engine2.py`'s docstring**, not a new derivation by
this report; they are reproduced because they are the design's justification and it is
useful to have them where it is discussed:

1. **An integer demands a global decision from a local observation.** The proposer sees a
   ticket and a handful of rules. It is the same demand that already failed in rung 1 under
   another name.
2. **The information that is missing is partial, not total.** They are relations between
   pairs. A global ranking is an answer to a question nobody asked.
3. **A reference is mechanically verifiable.** An integer is **unfalsifiable**: any number
   passes any validator.
4. **A reference composes; an integer competes.** If the integer says A>B and subsumption
   says B≺A, there is no non-arbitrary way to arbitrate between the two arbitrations.

That fourth point is what disqualifies mixed schemes of the `priority_layer` + `overrides`
kind: they introduce two authorities over the same pair.

**What exactly the validator checks** (verified against `rung2/engine2.py:220` and
`try_edge`, not inferred): six verdicts, five of rejection and one of acceptance —
`EDGE_SELF` (self-reference), `EDGE_UNKNOWN` (the cited rule does not exist),
`EDGE_DISJOINT` (the extensions do not intersect: the edge would be inert),
`EDGE_CONTRADICTS` (subsumption already says the opposite), `EDGE_CYCLE` (it would close a
cycle) and `EDGE_OK`. A detail that is not obvious: `EDGE_OK` is also returned when
`ext(winner) ⊊ ext(loser)`, that is when the edge is redundant with subsumption but
consistent with it; it is accepted and adds nothing to the graph.

**And what the validator cannot check, which is what matters for §7:** that the declared
winner is the correct one. Existence, overlap, non-contradiction and acyclicity are
properties of the graph; the truth of the edge is not in the graph. A false, well-formed
edge goes in without resistance.

### Level 3 — Abstention

If after both levels there remain undefeated rules that disagree → `CONFLICT` and
escalation. **The escalation trigger is only coverage or conflict, never "the answer was
incorrect"**, and that restriction is exactly what makes the silent error measurable. A tie
resolved blindly is an invisible error; a declared conflict is a countable event and the
signal that feeds the learning.

**And this is not an aesthetic preference for prudence: there is a measured case where the
price of not abstaining can be seen.** The formulation is from `CHAT_SUMMARY.md` §1 and the
figure from `results2/FINDINGS2.md` §4:

> **Partitioning does not eliminate the errors: it eliminates the error detector.**

The v2 base with seed 17 is **six rules** that partition the space cleanly using only three
attributes. Coverage 0.940. **Zero conflicts** in the whole run — and silent error
**0.7553**. Three out of every four decisions wrong, without the system emitting a single
signal that there was anything to decide.

That is level 3's entire argument, and it is worth having it in this form and not the
abstract one: **the number of conflicts is not a cost to be minimized**. A base that never
enters conflict may be a base that has stopped looking. And since the silent error can only
be measured with the oracle —which in production does not exist— the conflict count is the
only instrument a deployed system has for knowing it is lost.

### What is measured, and on which surface

Subsumption + 199 minimal declared edges: **e2e 1.0000, silent error 0.0000, zero conflicts,
zero impasses** — **over the corpus of 2000**, which is all `rung2/ceiling_check2.py`
measures. Over the exhaustive space that engine **has never been measured**. By this
report's header convention, and in view of what §6 demonstrates about transfer between
surfaces, the correct formulation is not "the mechanism is closed" but:

> **The mechanism executes a perfect author's declaration without error over the arrival
> distribution.** That it does so as a function over the 134,400 combinations as well is
> plausible —the declared order derives from the layer order, and *first-match-wins* is
> verified over the whole space— but it is not measured, and measuring it costs zero calls.

Two implementation details worth writing down because they are not obvious:

- **Transitivity comes free.** If A beats B and B beats C, both end up defeated and only A
  remains undefeated; there is no need to compute the transitive closure.
- **The edges are global but their effect is local.** `decide` only considers the defeats
  *among the rules that matched in this case*. The same rule can be undefeated in one case
  and defeated in another: priority is a graph, not a table of absolute merits.

---

## 4. Where this fits in the tradition

Rungs 1 and 2, together, are an empirical replication of why defeasible logics carry an
**explicit superiority relation** and why Drools has `salience`: the criteria that
reconstruct priority from the shape of the rules fall over on a stratified policy, and the
one that holds up is the one that declares it.

A precision about that replication, so as not to claim more than there was: the three
criteria falsified here were **specificity, arrival order and subsumption**, and that is not
exactly the classic trio of production systems —where the canonical three are refraction,
recency and specificity—. Subsumption is not an OPS5 strategy: it is a semantic criterion
this project added and which turned out to be the only one of the three with soundness over
a well-written policy. The coincidence with the tradition is in the conclusion, not in the
set of criteria tested.

| mechanism | origin | what it does with conflict | where it breaks |
|---|---|---|---|
| Specificity | OPS5, CLIPS, Jess | the one with most conditions wins | inverts with broad overrides (rung 1) |
| Recency / age | OPS5 (LEX/MEA) | the most recent or the oldest wins | on a learned base it runs **backwards** |
| First-applicable | XACML, iptables, ACL lists | the first in the list wins | textual order **is** the priority; inserting in the middle breaks the semantics |
| `salience` | Drools | explicit integer; tie → LIFO | unfalsifiable; competes with any other criterion |
| Superiority relation `>` | defeasible logic (Nute, Antoniou) | edges between concrete rules | it has to be declared: somebody has to write it |
| Preferences in ASP | asprin, LPOD | order over models | expressive and expensive; outside the cheap engine's scope |
| Result combination | XACML (`deny-overrides`…), Cerbos | combines **decisions**, not rules | does not express hierarchy between rules |
| **Subsumption + edges + abstention** | this repository | `ACTION` if the undefeated agree; if not, `CONFLICT` | requires computable extensions; over a learned base it costs bound; the `CONFLICT` is a burden if nobody fills it |

A precision worth not losing: **XACML's combining algorithms are not comparable with
subsumption**. `deny-overrides` combines policy *results*; subsumption orders *rules*. They
are objects of a different type, and the analogy "subsumption is the non-negotiable denial"
confuses more than it clarifies.

What the repository adds to the picture and was not there: **the measurement of how much is
left to declare** once the semantics has said its part (85% of the pairs over the hidden
policy), the finding that this residue is *small in edges* but *nobody produces it
automatically*, and **the price of the semantic level over a base with no author**, which is
the part none of the traditions above measures because they all assume a base written by
somebody.

---

## 5. The bottleneck is not the mechanism: it is the material

The mechanism is the visible and elegant part, and that is why it takes the attention. The
records point somewhere else.

Rung 2 built the engine that executes declared priority (1.0000, corpus) **and in the same
movement eliminated the material that exercises it**. Showing the base to the proposer
dropped the overlap between its rules from 17.5% of the pairs to **1.60%**; instructing it
explicitly to overlap recovered it to 7.25%, without reaching half the starting point. With
no overlap there is no conflict, and with no conflict there is no priority to declare:

```
eight runs · ~200 escalations
  total conflicts         2
  edges proposed         14
  edges ACCEPTED          0
  EDGE_CONTRADICTS        0
```

**And it is not a capability failure of the model.** It reasons relationally as soon as it
has something to reason with: it cites rules by identifier, argues that one should lose
against another, and even correctly identifies that subsumption resolves a nesting with no
need for a declaration. Prompt v2 hands it the overlap arithmetic already resolved by the
engine —which conditions the ticket fails for each rule, the size of each extension, which
pairs are disjoint— and **five of the fourteen badly proposed edges are still from v2**.

The correct diagnosis is more uncomfortable than "it cannot compute the overlap": **the
operation it performs —find a gap and fill it— does not require computing it**, and it is
the operation it performs even when it is asked for another. It treats the base as an
incomplete mosaic, not as a stack of layers.

*(`STATUS.md` keeps the why of that as an open question and without discriminating between
three candidates: the framing of the task —one ticket, one rule—, the specific model, or
elicitation by rule-writing in general. The claim "it is not capability" is supported by
`FINDINGS2`'s two arguments; nobody has the explanation.)*

A design consequence, and it is the one that orders everything else:

> **Every additional layer of arbitration architecture is capability added to a mechanism
> that already executes without error and without being fed.** Before deciding better who
> wins the conflict, one has to get a base where the rules step on each other.

**With a reservation that has to be made explicit, because that sentence invites reading
more than it says.** "Getting a base with overlap" sounds like the last link of a chain
whose remainder is tested, and it is not: **neither the 0.8530 nor the feedback's 61%
travels with a new base**. Both were measured over rung 1's 577 rules; a base with real
overlap is different material, and what a searched order or a feedback channel would extract
from it is unmeasured. Erratum (c) of §4 of `CHAT_SUMMARY.md` points it out, written on
August 12, 2026 against a document claiming to be "one link" from closing the chain. The
defensible claim is more modest and still suffices: **with no overlap there is not even an
experiment**.

### The word "material" means two things and it is worth not fusing them

What is above is **overlap material**: rules that compete, without which there is no edge to
declare. There is a second material problem, of another nature and measured separately
(`results3/FINDINGS3.md` §2, corpus): for **66.7% of `T3_ENGINEERING` and 64.2% of
`ACCOUNT_MANAGER` no correct rule covering the case exists**. There what is missing is not
overlap, it is a rule, and no order, no edge and no arbiter recovers them. Six classes out
of eight —1774 of 2000 cases— are indeed a pure ordering problem; those two are not.

The distinction matters for reading any proposal: P1 and P2 attack the overlap material, and
do not touch the second. Nothing in this report touches it.

### And the biggest gap is not one of arbitration

It is worth saying even though it falls outside the report's scope: the project's original
question —whether the rules the LLM writes are reused or memorize cases— **still has not
been measured cleanly** (`STATUS.md`, "What this does not show"). Rung 1's 0.158 reuse
describes the arbitration, not the induction, because 594 of its 632 escalations were
CONFLICT. A report on arbitration can close arbitration and leave the project just as far
from its own hypothesis.

### Corollary about an unvalidated instrument

`EDGE_CONTRADICTS` has never incremented in any run, not because the proposer gets it right
but because the situation in which it can increment was never reached. Any conclusion
resting on it rests on a counter nobody has seen work.

---

## 6. Underneath everything: the order is not identified

This is the result that gets the least attention and the one that most constrains what can
be built on top of it.

Over the exhaustive space, two end orders of the same search **one train case apart** decide
**11,240 of 134,400 cases (8.36%)** differently; in another split, three cases apart,
10.74%. The 65 end orders are **65 distinct behavioural signatures**: no two of them are the
same machine, and the same holds for the 257. And with a low budget it is brutal: with 10
labels, the **40 orders that tie on the best train score disagree with one another on a
median of 39.2% of the space** (24.05% of the corpus). The search is not abstaining; it is
choosing arbitrarily among very different answers and landing on a sensible default by
accident of the order of starts.

Three consequences, and none is cosmetic:

1. **The level is a result; the order is a lottery.** A reader of the figure 0.8530 can
   trust it —with the caveat `STATUS.md` attaches to it: it is the best of 65 starts,
   bounded by a lottery and not by convergence—. A reader of the order inherits the whole
   draw. And rung 4 consumes orders, not figures.
2. **Verification is harder than arbitration.** A verifier checking acyclicity, invariants
   and the absence of regressions over historical cases **certifies all 40 just as
   cheerfully**. The objective does not identify the answer, so the verifier's authority is
   smaller than its name suggests. Any design that puts "the verifier is the authority" in
   its central principle has to say what it verifies against.
3. **The surface is not a measurement detail.** The same 2,080 pairs pool to 20.35% of the
   space and 5.75% of the corpus, and the classes that carry the disagreement are different
   ones (`SECURITY_INCIDENT` 57.5% on the space, 4.6% on the corpus). Worse: **the order
   does not transfer either** —Spearman corpus↔space of **0.3364**— so the space cannot even
   rank two orders for deployment. A decent rank statistic is **not** evidence of transfer;
   it is necessary, not sufficient.

**And the fourth part of that record says exactly where the gap comes from**, which is what
makes point 3 actionable instead of merely alarming. Measuring the same 2,080 pairs over the
space **restricted to the 1,743 points the corpus touches** —1.30% of the space, each point
counted once— the pairs disagree on **5.68%**, against 5.75% for the arrivals and 20.35% for
the whole space. That is: **the level transfers to the arrival distribution before applying
any class weight**, and 98.6% of the gap is *which points are sampled*, not how many times.
Which closes one door and opens another: there is no per-class factor that turns one surface
into the other —reweighting by class leaves +1.4% over the touched points and +103% over the
whole space—, so the space's record plus the class frequencies **still does not reach**
5.75%. Only the corpus identifies the correction.

---

## 7. Proposals

**Nothing in this section is measured, and none of these predictions is signed.** The
repository's convention for a prediction to count is strict: a band with its refutation
line, written and signed **before the figure exists**, and signed by Sergi —a model drafting
the prediction destroys the file's purpose (hard rule 2 of `CLAUDE.md`). What follows are
directional drafts: to enter `STATUS.md`'s scoreboard each one is missing the numeric band
and the signature.

**Ordered by a borrowed criterion, which is better than the one they came with.**
`CHAT_SUMMARY.md` §3 orders its experiments like this: *what can **withdraw** a published
premise comes before what can **add** a capability*. Under that rule P1 goes first —a null
result withdraws the thesis that declaration is the missing channel, which is the premise on
which rung 2 was opened— and P4 and P5 go last, because they add instrument. By what they
attack: P1 and P2 the overlap material, P3 the price of level 1, P4 identifiability, P5 the
instrument.

### P1 · Pairwise judgement triggered by **offline overlap**, over the base already paid for

Not asking the proposer to write rules that step on each other —which is what eight runs say
it does not do—, but **detecting the pairs that step on each other and asking it which one
wins**. With two protocol decisions that are the whole proposal:

**Where the pairs come from: from the extension overlap computed offline**, over the 134,400
combinations, not from a conflict at run time. The engine already computes that overlap for
v2's neighbourhood. Triggering on conflict at run time is the same drought that left
`EDGE_CONTRADICTS` measuring nothing in eight runs: **2 conflicts**. An experiment that needs
conflicts to get started does not repair the broken link — it *is* the broken link.

**Over which base: rung 1's 577 rules, which are already paid for.** No new shadow loop, no
new corpus, and no dependence on first getting a base with overlap, which is the circular
dependency that sinks the naive version of this idea.

*(Both decisions are the amended form `CHAT_SUMMARY.md` §2.2 proposes, whose erratum of
August 12, 2026 identified the circularity before this report did.)*

**And how the question is materialized:** instead of "do R3 and R7 overlap and which one
wins?", **build a ticket from `ext(R3) ∩ ext(R7)` and ask for the queue**. The answer *is*
the edge, and the witness is an `&` of two integers: deterministic and free.

**Three objections that have to be put up front, because they come out of the record and
they are hard.**

*First, and it is the one that points most directly at the target:* the only two times a
real conflict reached the proposer —exactly the situation this experiment manufactures— it
answered with **zero edges** once and **failed the parse** the other. **0 of 2.** With n=2
and the elicitation not being a direct question it is not a refutation, but it is the closest
thing to evidence there is and it does not point in favour.

*Second: the target operation is not demonstrated either.* `results/llm_run.json` measures
exactly that —a ticket in front, the queue to be decided— in `proposal_action_accuracy` =
**0.3877** over 632 escalations, 594 of them CONFLICT. The premise "it is the operation it
demonstrably answers" is false as it stands: it is another operation that also fails, only
it fails differently.

*Third: the obvious metric is degenerate.* The 14 rejected edges fell **all** to
`no_solapan` [*they do not overlap*]. A witness extracted from the intersection guarantees
overlap by construction, so `EDGE_DISJOINT` stops being reachable and the acceptance rate
rises from 0/14 whatever the model does. And since the validator cannot check that the
winner is the correct one (§3, level 2), what would be produced at 39% accuracy are
**accepted and false edges**: turning a visible rejection into a silent error, which is the
exact conversion this project exists to avoid.

**The scoreboard, and its pool has to be labelled or it is worth nothing.** The output is
scored as an order, not as an acceptance rate. But **against what depends on which engine
consumes it**, and confusing that is chaining figures from different engines:

| if the edges are consumed in… | ceiling with oracle, same base | bound | floor |
|---|---|---|---|
| the **hybrid** engine (subsumption + edges) — the default case, because it is where the edges live | **0.7734** | 0.8540 | `born_at` over the hybrid pool: **not measured** |
| a **pure** total order, if the edges are compiled to an order and subsumption is switched off | 0.8530 | 0.9010 | `born_at` 0.5115 (full corpus) |

Corpus test except the floor. Scoring a hybrid result against 0.8530 would be inflating the
bar by ~0.08 by reading the wrong pool. **The floor of the row that matters is unmeasured
and measuring it is free**: it is the experiment's first step, not a detail.

**And a caveat that has only existed since August 15:** 0.7734 and 0.8530 are *the best of
65 starts*, and the 65 end orders are 65 distinct machines (§6). Comparing a declared order
against that maximum is comparing it against a winning ticket. The honest comparison is
against the **distribution** of the 65, and that material is already regenerated in
`results3/order_metrics.json`.

*Cost:* cents — one call per contending pair that is chosen for sampling.
*Falsifiable predictions, and there are two because they measure different things:*

1. *With truth, cheap:* over the 29 hidden rules the winner of each pair is known by
   construction (§7, P5). If the rate of **correct** edges per witness does not clearly beat
   the baseline 0.3877, the format of the question was not the problem and P1 is refuted
   right there, before touching the learned base.
2. *Without truth, the one that decides:* the order resulting from the declared edges over
   the 577 rules scores above the `born_at` floor of its own pool and within the
   distribution of the 65 starts. If it lands on the floor, declaration contributes no
   channel; if it lands between floor and distribution, it contributes and is not enough,
   which is a result and not a tie.

### P2 · **Deferred** elicitation, over the live subgraph

Not declaring priority when the rule is born, but when two rules contend over a real case.
*It is the same impasse discipline that already governs the calls to the LLM, applied to
arbitration: pay only when you have to pay.*

**The cost argument, corrected.** The strong version —"the cost is not O(N²)"— does not
follow from the repository's figures. Of the learned base's 166,176 pairs, **35,457 can
change a decision over the space** (33,631 over the corpus): that is 21.3%, a **constant
fraction of the quadratic**, not a lower order. And the other datum that invites optimism has
to be read carefully: only **25 to 53 rules of 577 own territory** under a given order, but
that is *per order*, and the union over the 65 end orders is **406 of 577**. Which rules
decide anything depends on the lottery §6 documents.

What does support the proposal is more modest and is still sufficient: the 21.3% is an
**upper bound on what can matter**, not a count of what will matter —there are contending
pairs that change no decision because nothing they match survives the rules above them—, and
over observed traffic the set that really gets to contend is one more sieve. The difference
between O(N²) declared up front and O(pairs that contend over real traffic) is empirical and
unmeasured.

*Falsifiable prediction:* the number of edges needed to reach a given e2e grows sublinearly
in the size of the base. **The band is missing**: without it, "sublinear" gets adjudicated
by eye.

### P3 · Imposing the discipline of authorship instead of assuming it

Subsumption gives 53.12% silent error over the learned base —over the 8% of cases where it
commits— because the convention "narrow rule = exception" is not honoured. Instead of
abandoning the criterion or inferring better, **restrict the form**: the validator rejects a
rule that overlaps another without declaring whether it is an *exception to* or a *default
under* each of the ones it steps on. The engine already knows exactly which those are.

This turns an inference problem into a declaration one **with a bounded number of questions,
locally answerable**. It is the proposal that convinces me most of the five, because it is
the only one that attacks a measured cause instead of a symptom.

*Two predictions, and they are different: the second is the one that matters and the one
nobody has posed.*

1. *Soundness:* the silent error of subsumption over a base produced this way falls well
   below 53.12%, **at comparable or greater coverage** —without that condition the
   prediction fulfils itself by making the criterion even more mute.
2. *Bound:* the 0.047 gap between the hybrid bound (0.8540) and the pure one (0.9010)
   narrows. This is the one that decides whether level 1 stops having a price or merely
   stops lying. If soundness improves and the bound does not move, P3 fixes half the problem
   and subsumption still costs a third of the base.

### P4 · Restricting the hypothesis class to **k-stratified** orders

Right now the search runs over total orders of 577 rules. Searching over assignments to *k*
strata (sweeping *k*) does three things: it shrinks the space, it regularizes, and —the
decisive one— **within a stratum ties are not broken by index: they are declared undecidable
and escalate**. That turns the identifiability problem from invisible into measurable: the
number of undetermined pairs becomes an **output** of the system instead of a hidden
property of the order of starts.

**That is P4's value and it does not depend on any conjecture about the truth.** What does
depend, and it is the weak link: the hidden policy has 8 layers over **29** rules, and the
search runs over **577 learned rules** whose relation to those layers is unknown —in fact
rung 2 documents that the proposer partitions instead of stratifying—. That the score
flattens near *k*≈8 over the learned base does not follow from the truth having 8 strata.

*Falsifiable prediction, with that reservation declared:* sweeping *k*, the number of
distinct behavioural machines collapses relative to the current 65 and 257, and the test
score does not fall appreciably until small *k*. If the number of machines does not
collapse, stratification is not the missing structure. **Where the score flattens is data,
not prediction**: if it flattened at 8 it would be a coincidence worth looking at, not a
confirmation.

### P5 · Benchmark of conflicts with known winner

A set of conflicting pairs with winner and scope known by construction, measured at
increasing levels of information (rules only / + examples / + counterexamples / +
provenance). It serves to answer something that cannot be answered now: **which information
contributes real value to arbitration**, instead of assuming it.

**And it is considerably cheaper than it looks, because the substrate is already built.**
`rung2/hidden_priority.py` classifies the hidden policy's 406 pairs into four disjoint
boxes: 112 with disjoint extensions, 61 already ordered by subsumption, 34 with the same
action (it does not matter who wins) and **199 declared edges with known winner**, derived
from the layer order. That is a labelled benchmark, today, at zero cost. What is missing is
not building it: it is the protocol of information levels and the bands.

Two conditions so that it does not turn into a dashboard of blunt metrics: the bands are
signed before the figure exists, and the rows without a band go listed separately and
outside the denominator —the convention the predictions thread already uses.

---

## 8. What I rule out, and why

- **A global priority integer** (with or without edges alongside): unfalsifiable, it demands
  a global decision from a local observation, and it competes with subsumption instead of
  composing.
- **An adversarial critic embodied in an LLM**: the counterexample inside
  `ext(A) ∩ ext(B)` is **enumerated** exactly with the bitmasks that already exist. Putting
  a model where a deterministic procedure suffices inverts the project's whole economy
  —cheap symbolic first, LLM only on impasse.
- **Scoped contextual priority** (`A > B if region=EU`): it is a real generalization and a
  valid one for other domains, but here the truth **is** a total order by layers, so it adds
  capability outside the truth, not just outside the hypothesis class. It also breaks the
  acyclicity check, which today is a trivial and cheap DFS. Reserve it for a domain where it
  has been shown to be needed.
- **Any multi-stage arbitration pipeline** —detector, deterministic arbiter, LLM arbiter,
  critic, verifier, graph, compiler, runtime— **built before having material**: it is rung 2
  again, at a larger scale. Building the apparatus and discovering that nothing comes down
  the pipe already happened once, it is documented, and it cost the project's only mechanism
  that works without error. The temptation is strong precisely because arbitration is the
  part that lets itself be designed without data.

---

## 9. Limits of this report

1. **The hidden policy may be adversarial to specificity by construction.** In it, priority
   and number of conditions are nearly orthogonal *by design*. That makes the falsification
   correct —one counterexample is enough to knock down "specificity is reliable"— but it
   says nothing about how often real policies have that shape. Distinguishing "falsified as
   a general criterion" from "its failure rate measured in the domain" deserves to be
   written down.

   There is a partial answer to this worth recording, from `CHAT_SUMMARY.md` §1: **the
   hidden policy does not have to be "the right one in the universe", it is THIS company's
   manual**, and what is measured is whether a structured function is recovered from
   experience, not whether the policy is good. That defuses the objection for what the
   experiment measures and does not defuse it for the generalization: how often real manuals
   have broad overrides on top is still unmeasured here and anywhere else in this
   repository.
2. **The hybrid engine's 1.0000 is a corpus figure.** Over the exhaustive space that engine
   has not been measured, and this report has argued in §6 that the two surfaces do not even
   rank the same. It is the cheapest pending check of all the ones named here.
3. **The 199 edges are the authorship cost of a perfect author over 29 rules.** How many
   would be needed over a learned base, and whether a proposer could produce them, is
   exactly what the eight runs never got to put to the test. P2 suggests the real cost is
   lower than the quadratic extrapolation, but that is unmeasured and §7 itself tones the
   argument down.
4. **One model, eight runs of n=100.** All of rung 2 is `deepseek-v4-flash`. Whether another
   model partitions the same way is unknown, and the number of rules varies so much between
   seeds with an identical prompt that that quantity is noise.
5. **The price of level 1 is measured over a single learned base.** The 0.047 of bound and
   the 181 silenced rules are properties of the 577 rules that rung 1 produced under
   specificity-based arbitration. A base born under another arbitration would be another
   one, and `FINDINGS` already warns that those measurements are bounds, not simulations of
   the loop.
6. **Two figures in this report have no record that owns them**, and they are the only ones:
   the 0.5420 and the 0.5668 of reversed `born_at` over the learned base (§2). They come
   from a *probe* that `CHAT_SUMMARY.md` §2.1 declares unofficial and that is not in
   `results*/`; the script that produces it does not exist in the tree. Its space baselines
   do verify exactly against `FINDINGS3.md`. They are cited with that warning in place, and
   if they ever support a conclusion they have to be measured first — it costs minutes and
   zero calls.

   > **[ERRATUM 2026-08-24] Zero, now.** Both were measured by `rung3/floor_by_pool.py` and
   > both reproduce exactly; `results3/floor_by_pool.json` owns them, along with the two
   > full-corpus baselines (0.5115 and 0.4172) that the same probe had left unowned. The
   > condition this point set — measure them before they support a conclusion — is met. What
   > it did not anticipate is that 0.5668 is a **pure-pool** figure: on the hybrid pool the
   > same reversal gains 0.0116 rather than 0.2520. The erratum in §2 carries that.

7. **This report has executed nothing.** It is a reading of the records, with the figures
   checked against the `FINDINGS` that owns each one —except the two of the previous point—
   and against the code where the code was the source (the validator's six verdicts, the
   locality of the edges, `ceiling_check2`'s surface). Everything in section 7 is unmeasured
   and is marked as such.
8. **Part of what is corrected here was already corrected.** The price of level 1, the
   circularity of the conflict trigger and the warning that the figures do not travel with a
   new base are the three errata `CHAT_SUMMARY.md` issued against itself on August 12, 2026.
   This report reached all three by another route and without knowing them. That two
   independent readings of the same records converge is evidence in favour of the
   conclusions; it is also a warning that **this repository already contains analysis that a
   new document may be repeating**, and that reading `CHAT_SUMMARY.md` comes before writing
   the next one.
