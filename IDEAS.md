# Parking lot

Status as of August 8, 2026. Rungs 1, 2, 3 and 4 closed; see
`results/FINDINGS.md`, `results2/FINDINGS2.md`, `results3/FINDINGS3.md` and
`results4/FINDINGS4.md`. The optimizer audit of August 8, 2026
(`results3/FINDINGS_AUDIT.md`)
corrected figures in rungs 3 and 4 in place. This is a list of things not done,
none of them developed and in no order of precedence.

---

## No longer here

- **Give the proposer the existing rule base as context.** Rung 2. It reduced
  the overlap between its rules by a factor of 10 and left the declared-priority
  mechanism — which that same change was meant to enable — with no material.
- **Priority by search over the corpus, without an LLM.** Rung 3. A coverage
  bound over the rules from rung 1 — an upper bound case by case, not a
  demonstrated attainable optimum, see the erratum in `FINDINGS3.md` — and a
  searched order far above what arbitration was extracting. The search uses the
  oracle. **Corrected 2026-08-08** by the audited optimizer, and the bound turns
  out to differ between the two surfaces; the figures are in `STATUS.md`.
- **Priority learned from observed behaviour.** Rung 4, Step A. With symmetric
  feedback almost everything is recovered; with the asymmetric kind, which is the
  realistic one, much less. **Corrected 2026-08-08: substantially more than first
  published, and the "change of regime" was a weak learner's failure curve.**
- **A serious optimizer for the order, and the audit of what the greedy cost.**
  August 8, 2026. Multi-start local search, validated first against the hidden
  policy whose optimum is known by construction. It answered the three questions
  the greedy left open — how much of the gap was search weakness (most of it),
  whether noise still helps (no), whether the asymmetry regime change survives
  (no) — and cost zero API calls. `results3/FINDINGS_AUDIT.md`,
  `results3/optimizer_check.json`, `results3/order_search_ls.json`,
  `results4/sweep_ls.json`.
- **Re-run rungs 3 and 4 with the tie-break fixed.** Done in the same pass, which
  is what made the two effects separable: the tie-break moved the fourth decimal
  and the algorithm moved the second. The fragility was variance, not bias.

---

## Pending and already specified

- **ILP (Popper/ILASP) over the hidden policy and the corpus.** It was Step B of
  rung 3 and was never run. Two measurements in one: whether it recovers the
  layer order, and as a competing baseline — what accuracy it reaches inducing
  rules on its own, without an LLM.
- **Online ordering.** It was Step B of rung 4 and it was decided not to run it:
  the asymmetry already answers the question and online ordering would only
  degrade things further. It is noted that it is a different problem from Step A
  — the base grows while it is being ordered, and feedback arrives with delay
  about decisions an earlier version of the order took — in case the framing
  changes. **The reason for skipping it weakened on 2026-08-08**: asymmetric
  feedback recovers far more of what full supervision does than rung 4 credited
  (see the erratum in `FINDINGS4.md` §1), so "it would only degrade things
  further" now rests on a smaller margin than when it was written.

---

## What rung 4 opens and does not resolve

- ~~The greedy search is a weak optimizer, and that contaminates backwards.~~
  **Closed 2026-08-08.** It did, and upwards: every figure moved in the same
  direction, on rung 3's test and on rung 4's anchor cell alike. See `STATUS.md`,
  "What was withdrawn, and why".
- ~~Whether the conclusion about asymmetry survives a better optimizer.~~
  **Closed 2026-08-08. It does not.** See the erratum in `FINDINGS4.md` §1.
- The fixed point of learning by correction: the signal runs out as the system
  improves. Where that point is and what it depends on has not been
  characterized.
- Whether there exists any regime in which deliberately degrading π₀ to harvest
  labels pays off. The data (a worse π₀ produces a better order) suggests it and
  it has not been explored.
- Whether the absence of feedback can be used in some way. Here it was decided
  not to interpret it as a correct decision; a probabilistic interpretation has
  not been tried.

---

## What rung 3 opens and does not resolve

- How much of the gap between the searched order and the coverage bound is really
  attainable. The bound is an upper bound by per-case coverage: it guarantees that
  no order exceeds it, not that some order reaches it. Exact optimization or a
  stronger global bound would be needed. See the erratum in `FINDINGS3.md`.
  **Partly answered 2026-08-08**: most of the gap was search weakness, and a
  search seeing every case in the exhaustive space still stops short of the bound
  — evidence it is somewhat loose, not proof. Exact optimization is still what
  would settle it.
- **Which surface a figure is measured on, as a standing question.** Opened
  2026-08-08. The corpus is the modelled arrival distribution and the exhaustive
  space is a uniform measure over attribute combinations; they are not
  interchangeable and this project published corpus figures for four rungs
  without saying so. An order fitted to the corpus loses a large share of its
  score carried to the space, and `born_at` reverses against random between the
  two. Every future figure should name its surface.
- Whether the order is attainable without labels. The shadow loop has no
  supervision channel by design. Rung 4 partially bounded this question and the
  answer was bad.
- Why the proposer did not write correct rules for `T3_ENGINEERING` or
  `ACCOUNT_MANAGER` — for roughly two thirds of each, no rule covering the case
  carries the right action (`FINDINGS3.md` §2). It is a material problem, not an
  ordering one, and it has no explanation.
  **Those two thirds now have a measured consequence**, the refutation of Q-f
  (`results3/FINDINGS_ORDERS.md`): where no rule is correct there is nothing to
  compete over, so every order fails those cases alike. Scarcity of material
  produces uniform failure, not variety.
- Whether a proposer that is shown the gaps in the ceiling would fill them.
- The objective function as an explicit design surface: which classes are
  protected, at what cost in aggregate, and who decides.
- Why rung 2's hybrid arbitration is worse than pure ordering over a learned
  base, despite executing the perfect policy without error. It stays worse under
  a competent optimizer, by a wider margin, so it is not a search artifact
  (`FINDINGS3.md` §1 and its 2026-08-08 erratum).
- **Subsumption silences a third of the learned base, and that is a finding about
  subsumption, not about runtime.** Opened 2026-08-08 while measuring why the
  hybrid pool costs so much more to search: once subsumption prunes, **181 of the
  577 rules match nothing at all on the train half**
  (`results3/FINDINGS_AUDIT.md`, Step 1).
  They are rules whose extension is strictly contained in another's, so on every
  case they cover, something else covers it too and outranks them. A third of what
  the proposer wrote is unreachable by construction under that arbitration, before
  any question of order. It is the mechanical form of the ceiling that
  `FINDINGS3.md` measures subsumption as costing, and it says the cost is
  concentrated rather than diffuse. Whether those 181 are redundant or are
  exceptions the arbitration buries is not known.
- **Search budget above the declared 64 buys labels and sells policy.** Opened
  2026-08-13. Raising the multi-start budget to 256 improved the best train score
  in 2 of the 5 splits, and in **2 of those 2** the same order scored worse on
  corpus test and worse over the exhaustive space — mean **−0.0050** and
  **−0.0196** (`results3/FINDINGS_AUDIT.md`, Step 3;
  `results3/start_budget_check.json`, n = 5 splits × 3 budgets). Extra budget
  buys fit to the labelled sample and sells the function. The direction is
  consistent but the sample of *movements* is 2, so what is open is whether it
  survives more splits and other fractions.
  **Falsifiable by measuring ORDERS, not scores.** Every figure above is a score,
  and two orders can score alike and rank rules quite differently. The check is
  to compare the orders a growing budget returns — how many positions move, how
  the rank correlation decays, whether the rules that change places are the ones
  that decide the rare classes — which is also the only way to tell a real
  regression from two draws either side of a plateau.
  **Measured on 2026-08-15** (`results3/FINDINGS_ORDERS.md`, which owns the
  figures). What the instrument settled: the winner at 65 starts and the winner
  at 257 are different machines by a wide margin on both splits where the train
  score moved, so those rows are not two draws either side of a plateau in any
  sense a reader could dismiss. What it did **not** settle: the direction — that
  extra budget buys the labelled sample and sells the function — still rests on
  the same two movements, and the count of positions that move turns out to say
  nothing, because nearly every rule moves between any two end orders. Rank
  correlation decayed as a diagnostic too: it does not track behaviour here even
  restricted to the pairs that can change a decision.
- **The peak of the multi-start is a singleton that spreads, not an optimum that
  concentrates.** Opened 2026-08-13. Across all fifteen measured rows — three
  budgets × five splits — **exactly one start reaches the best train score**, and
  quadrupling the budget only widens the spread of scores rather than gathering
  starts at the top; in splits 1 to 3 the best did not change between 65 and 257
  starts and the 192 extra draws never found it again (`FINDINGS_AUDIT.md`,
  Step 3). A well-behaved landscape would show the opposite: more starts, more
  ties at the maximum.
  What is open is what that costs **any rung that consumes the order rather than
  the score**. Rung 4 does exactly that — it learns an order from feedback and
  hands the order on — so its figures inherit a draw even where the aggregate
  level is stable. Whether the variance is benign (many near-equivalent orders,
  and which one you get does not matter downstream) or load-bearing (the singleton
  encodes the rare-class decisions) is unmeasured, and it is the same question the
  entry above proposes measuring.
  **Measured on 2026-08-15** (`results3/FINDINGS_ORDERS.md`). Not closed,
  sharpened. The variance is **not** benign in the first sense: the end orders
  are all distinct machines — every set measured, up to 257 of them, with no two
  behaviourally identical — and where the objective saturates at 1% the orders
  that tie at the top disagree with each other on a large fraction of the case
  space. So the singleton peak is not one summit among near-copies; it is one
  draw among many genuinely different answers. Whether it is load-bearing in the
  second sense — whether the differences fall where a deployment would feel them
  — is still open: they concentrate on the **most abundant** class, not on the
  scarce ones the entry guessed, and nothing here measures the arrival
  distribution.
  One thing to read carefully before anyone cites "they are all distinct" as
  ruggedness: the freedom the plan identified is **per pair and does not
  compose**. Two rules whose relative order cannot change a decision can be
  swapped freely, but two orders produced by separate searches almost surely
  invert at least one pair that *can* change a decision, and one is enough to
  make them different machines. All-distinct is therefore what that arithmetic
  predicts on its own; the informative quantity is how far apart they are, and
  that is what the record measures.
- **The surface question has its first measurable instance, and it is cheap.**
  Opened 2026-08-15. This is not a second copy of *which surface a figure is
  measured on* above — it is that standing question narrowed, for once, from a
  norm about labelling into a run somebody can go and do.
  Everything `results3/order_metrics.json` holds is the **uniform measure over
  the 134,400 combinations** — figures owned by
  [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) and quoted here
  as pointers, not as a second home: Q-a's **11,240** cases between the winners
  at 65 and 257 starts, Q-b's median **39.2%** across the 40 orders that tie at
  1%, Q-e's median disagreement of **20%** against a median churn of 99.65%.
  None of it is the arrival distribution a deployed system would actually meet.
  What keeps the answer from being a formality is G2, which counted the pairs
  that can change a decision on **both** pools: **33,631** on the corpus against
  **35,457** on the space, out of the same 166,176. The material to disagree
  over is therefore almost the same on either surface, and what is unknown is
  **where it falls** — the corpus is deliberately long-tailed, and disagreement
  that concentrates on a class occupying a large share of the space while being
  rare in arrivals would read very differently in deployment from how the record
  reads now.
  It is settled by running the same instrument over the corpus pool, which
  `order_search_ls.space_pools` and `local_search.build_masks` already build and
  which `order_metrics` accepts unchanged, being pure and taking masks as
  arguments. Minutes, and no new apparatus: that is what makes this worth doing
  rather than merely noting.
  **It informs whichever way it comes out.** If the disagreement survives the
  change of surface, the space figures carry over and the caveat
  `results3/FINDINGS_ORDERS.md` leaves open under *what this does not settle*
  closes. If it collapses, then what that record measures matters less in
  production than it currently suggests — the more interesting of the two
  answers, and just as publishable.
  **The prediction is written and committed BEFORE measuring.** A single run
  does not need a whole `PLAN_*.md`; one dated line in this entry, committed
  before any figure exists, is enough to make it checkable in the log. What is
  not acceptable is writing the number down afterwards and presenting it as what
  was expected — that is the Goodhart failure this project exists to study, and
  avoiding it costs one commit.

  **PREDICTION — 2026-08-15, written before the run.** Drafted by Claude; Sergi
  signs it as it stands, without changes; committed before any of the figures it
  names exists, which is the only thing that makes it worth anything. §6 of
  `PLAN_ORDER_METRICS.md` bans figures from this file beyond a pointer, and a
  prediction is the one exception that justifies itself — the number bet on has
  to be written down or there is no bet — so this is not the rule relaxing. The
  space-side figures used here as yardsticks (the 20.35% overall rate,
  SECURITY_INCIDENT's 57.5% of it, the 1.9% pairwise minimum, the 39.2% median
  of the tied set) are owned by
  [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) and quoted from
  it.
  Two of those yardsticks were referred to loosely when this was signed, and S-a
  and S-b and S-e were sharpened the same day, **still before any measurement
  exists** — which is the only window in which it can be done at all. Saying
  more precisely *what* is being measured, while no number exists to be flattered
  by the choice, is the opposite of moving the goalposts; the log is what makes
  that checkable rather than a claim, since both commits predate the run.

  - **S-a** — The disagreement over the 2,080 pairs of the 65-start set,
    measured on the corpus, falls **between 12% and 20%**. *Refuted* below 10%
    or above 22%. **The quantity that adjudicates is the POOLED rate** — total
    disagreements over total cases, summed across the pairs — which is what
    `FINDINGS_ORDERS.md` publishes as 0.2035 for the space and what the 15.2% of
    S-b was computed from. The per-pair median is reported beside it for
    continuity with Q-e and does **not** adjudicate. On the space the two nearly
    coincide, 19.99% and 20.35%, which is exactly why the distinction has to be
    fixed now rather than argued about on the day.
  - **S-b** — **The bet.** That same pooled rate comes out **above the 15.2%**
    that reweighting the space's per-class rates by the arrival distribution
    gives. The reason: the 577 rules were written looking at the corpus, so the
    typical arriving case carries more rules over it and more pairs competing,
    and that pushes up against a reweighting that pushes down. *Refuted* below
    15.2% — and then the surface is only a change of weights, and the corpus's
    concentration adds no competition of its own.
  - **S-c** — The per-class rates are preserved across surfaces to within
    **±30% relative**, for the classes with 100 or more corpus cases. *Refuted*
    otherwise, and then "surface" is not reweighting at all: the mix of cases
    *within* each class governs too, which is a larger finding than the
    headline.
  - **S-d** — *Calibration.* SECURITY_INCIDENT's share of the total disagreement
    falls from **57.5% to under 3%**. *Refuted* by anything far from that, which
    would mean the per-class rates do not carry across and S-c will already have
    fired.
  - **S-e** — **Over the 32,896 pairs of the 257-start set**, not the 2,080 of
    the 65: pairs at distance 0 on the corpus with distance > 0 on the space
    stay at **zero**, while the pairwise minimum falls from **1.9% of the space
    — the 2,615 cases the record publishes — to under 1% of the corpus**.
    *Refuted* if any such pair appears — and that would be the large finding
    here: two orders distinguishable in principle and identical wherever the
    cases actually arrive are the same machine for deployment purposes. The set
    is the 257 because that is where both space figures are published; the
    65 starts are its prefix, so the smaller set's minimum is greater or equal
    and was never published. It is also the harder test of the two: sixteen
    times the pairs is sixteen times the chances of turning up a pair the corpus
    cannot tell apart.
  - **S-f** — The tied set at 1%, which disagrees a median 39.2% over the space,
    stays **above 20%** over the corpus. The tie is a fact about the training
    signal, not about the surface. *Refuted* below 10%.

  **Not predictions, invariants** — if these fail, something is broken and the
  prediction has not been tested at all: `d(a, a) = 0` on either surface; the 65
  orders are the same objects the record already measured, so the parity gate is
  passed again over the same 31 rows before anything below it is believed; and
  **no new search** — this is re-measuring known orders on another surface.

  **Two conditions for whoever runs it.** The record stores signatures and
  distances, not the 65 orders, so the run is regenerate-with-parity and then
  measure over 2,000 cases instead of 134,400: seven or eight minutes. And the
  surface has to be named precisely — the full corpus is 2,000 cases, but the
  search saw the train half of those, so **both** are measured and published,
  full corpus and test split, each said to be what it is. That matters most for
  S-f, where measuring on what the search fitted would understate the answer by
  construction.

  **MEASURED — 2026-08-15, and four of the six are refuted.** The figures are
  owned by [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part
  two, and by [`order_metrics_corpus.json`](results3/order_metrics_corpus.json);
  what is below is each row against its own threshold and nothing more. Parity
  31/31, the corpus census reproduces G2, `d(a, a) = 0` throughout, no new
  search. Adjudicated on the full corpus, with the test half beside every one of
  them and agreeing on every verdict. 396 s, zero API calls.

  - **S-a REFUTED** — 5.75% pooled, below its 10% refutation line and far below
    the 12–20% band. On the space the same pairs give 20.35%.
  - **S-b REFUTED** — the same 5.75%, against 15.2%. Its stated mechanism is
    **confirmed and does not produce the effect**: the average arriving case
    carries 74% more live conflicting pairs than the average point of the space,
    and disagrees 3.5 times less. Those two figures are **post hoc** — chosen
    after the verdict existed and because S-b had failed — and the record marks
    them so.
  - **S-b's 15.2% does not reconstruct.** Found on reading the entry and
    confirmed on measuring: reweighting the space's per-class rates by the
    arrival distribution, the route the prediction names, gives **11.67%**. It
    landed in the repository in the same commit as the measurement, so the log
    does not separate the two and this is not a note that predates the run. The
    verdict is against 15.2% as written; 5.75% is below both.
  - **S-c REFUTED** — four of the six eligible classes fall outside ±30%
    relative, from −81.6% to +165.2%. Which is the larger finding its own
    refutation clause named: the mix of cases *within* a class governs too.
  - **S-d REFUTED on its stated value** — 4.57% against *under 3%*, from 57.5%
    on the space; pure reweighting predicts 2.67%, and the gap is what S-c
    already fired on. Its refutation condition, *anything far from that*, is not
    a number: both readings are published in the record that owns the figures,
    and the row's own rider — that S-c would already have fired — did occur.
  - **S-e HOLDS**, both clauses — zero pairs of the 32,896 at distance 0 on the
    corpus, and the pairwise minimum at 0.10% against a line of 1%. Read at the
    surface's resolution that is 2 cases of 2000, one case being 0.05%: the
    clause was cleared by 18 cases.
  - **S-f HOLDS** — median 24.05% of the corpus, against a 20% line. The
    low-budget caveat survives the change of surface; the full-supervision
    headline does not.

  **What it settles for the standing question above.** Where the disagreement
  falls changes completely — `SECURITY_INCIDENT` goes from 57.5% of it to 4.6%,
  and the deflection queue from 1.5% to 44.8% — so a space figure cannot be read
  as a deployment figure, in either direction. What it does not settle is why
  the rate collapses by 3.5× when the contested material grows by 74%: about a
  tenth of it is fitting, and the rest is unexplained and deliberately left so.

  - **Whether the space can RANK two orders when it cannot rate them.** Opened
  2026-08-15, after the corpus surface entry above closed. That entry settled two
  things and left this one untouched. The **level** does not transfer: 5.75% over
  the corpus against 20.35% over the space, and not the 11.67% that reweighting
  the per-class rates predicts either. And **where** disagreement falls does not
  transfer: S-c refuted, SECURITY_INCIDENT going from 57.5% of the total to 4.6%
  while SELF_SERVICE_DEFLECT goes from 1.5% to 44.8%.
  Neither says whether the **ordering** of pairs survives, and it is not implied
  by either. A rank is invariant to any monotone transformation, so a level that
  falls by 3.5× is perfectly compatible with an ordering preserved exactly, and
  a per-class composition that moves is compatible with both — what it would take
  to scramble the ordering is for pairs to differ from **each other** in where
  they disagree, which is a different quantity from any measured so far.
  **What turns on it.** `results3/order_metrics.json` is cited to say that one
  pair of orders is further apart than another: Q-a's 11,240 cases between the
  winner at 65 starts and the winner at 257, the factor of 21 between the closest
  and furthest pair. If rank transfers, that use survives the change of surface
  and only the level was wrong. If it does not, the space record cannot even
  **order** two orders for deployment, which is strictly worse than a level shift
  and is the strong form of the reservation
  [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md) leaves open under
  *what this does not settle*.
  **It is a join of two published records, not a run.**
  `order_metrics.json::pairs_split0_starts65` and
  `order_metrics_corpus.json::pairs_split0_starts65_corpus_full` and
  `_corpus_test` hold 2,080 rows each, keyed by the same `i`/`j` over the same 65
  end orders. No search, no regeneration, no new instrument, seconds. The
  257-start matrices are summarized on both sides and would cost a regeneration;
  they are an addition here and adjudicate nothing.

  **PREDICTION — 2026-08-15, written before the join.** Drafted by Claude; Sergi
  signs it as it stands; committed before any of the figures it names exists.
  §6 of `PLAN_ORDER_METRICS.md` bans figures from this file beyond a pointer, and
  a prediction is the exception that justifies itself, as in the entry above.

    **What the drafter had already seen, declared so that the signature is
    auditable.** All of S-a…S-f and their verdicts. The two marginal
    distributions of the very set being predicted, both published: over the
    space, rates from 0.0359 to 0.4112, median 0.1972; over the corpus, 0.0085 to
    0.1255, median 0.0590. Their quantile-by-quantile ratios, computed while
    drafting and therefore declared here: 0.237 at the minimum, 0.255 at p25,
    0.299 at the median, 0.297 at p75, 0.305 at the maximum — near-proportional
    marginals, which raised the drafter's estimate for R-a and settle nothing,
    since a Q–Q relation is between distributions and says nothing about which
    pair sits where. And one extreme point from the corpus side: end orders 47
    and 87, 2 cases of 2,000 apart on the corpus and 6,180 (4.60%) apart on the
    space, while the minimum over that set's 32,896 pairs is 2,615. **That pair
    is not in the set being predicted** — index 87 falls outside the 65-start
    prefix — so it constrains the intuition and not the answer.

    Two structural facts about the matrices, checked while drafting: the `(i, j)`
    key sets are identical across the three, and the rates take 1,834 distinct
    values over the space against 207 over the corpus. The tie load was checked
    for whether it caps R-a and it does not — groups average ten over 2,080, an
    attenuation of order 1e-5 — so it constrains the procedure, not the band.

  - **R-a** — **The headline.** Spearman between the corpus-full rate and the
    space rate, over the 2,080 pairs of `split0_starts65`, lands **between 0.70
    and 0.93**. *Refuted* below 0.55 or above 0.97, and the upper clause will
    rarely fire alone: if R-c is refuted, this one follows it.
    The reason the band sits high. Corpus distance is not a second measurement of
    the same pair, it is an importance-weighted sub-sample of the first: each of
    the 2,000 tickets lands on exactly one of the 134,400 points, so corpus
    disagreement counts the draws that land where the two orders differ. Which
    particular cases were drawn contributes about 9% relative — binomial at a
    rate of 0.0575 over 2,000 — against a spread between pairs of about 42%, read
    off the published IQR of the very set being predicted. Idiosyncratic draw
    cannot be what lowers the correlation. What can is pairs differing from each
    other in *where* they disagree, and these 65 orders come from one
    neighbourhood over one training half at similar scores, which argues they do
    not differ much. **Refutation below 0.55 is therefore the informative
    outcome**: it would mean the pairs specialize far more than their common
    origin suggests.
  - **R-b** — *Where it bites.* Of the 208 pairs closest on the space, **between
    35% and 70%** are among the 208 closest on the corpus. *Refuted* below 20% or
    above 80%. This is the deployment-relevant form: a global correlation can be
    respectable while the extremes — the pairs a reader would call
    interchangeable — swap wholesale.
  - **R-c** — *Calibration.* The per-pair ratio corpus/space is **not a common
    factor**: its p75 over its p25 exceeds **1.30**. *Refuted* below 1.15, and
    then the change of surface is one multiplication for every pair alike. Note
    what that would and would not mean: a single scalar of roughly 0.29 is **not**
    the class-reweighting model, which predicts 0.573. It would say a constant
    exists and no per-class account currently produces it, which is a new
    question and not a reprieve for the route S-b's 15.2% named.
  - **R-d** — *Reported, not adjudicated.* Which pair attains the space minimum
    inside this set and where it ranks on the corpus, and the converse for the
    corpus minimum. It is one draw of 2,080 either way; a threshold on a single
    argmin would not be a bet, and the question that opened this entry is
    answered here as an anecdote beside R-a rather than as its substitute.

  **Not predictions, invariants** — if these fail nothing above was tested: the
  same 2,080 pairs on both sides, matched by `(i, j)` and not by position; both
  matrices read from the published records with **no regeneration and no search**;
  and the gate, which is this question's parity gate — recomputing each record's
  own published summary quantiles for that set from its stored matrix must
  reproduce them exactly before anything below is believed, since that is what
  makes the join about the right rows.

  **One condition for whoever runs it.** `corpus_full` adjudicates and
  `corpus_test` is reported beside it, matching the convention the entry above
  fixed. Test is the honest surface for anything about generalization and the
  wrong one here: it is 995 cases, half the resolution, and rank noise rises as
  the surface shrinks.

  **MEASURED — 2026-08-15. It does not rank either.** Figures owned by
  [`results3/FINDINGS_ORDERS.md`](results3/FINDINGS_ORDERS.md), part three, and
  by [`rank_transfer.json`](results3/rank_transfer.json); below is only each row
  against its own threshold. The gate passed — the three key sets identical, all
  three published summaries reproduced from their own stored matrices — no
  search, no regeneration, **0.07 s**.

  - **R-a REFUTED** — Spearman **0.3364**, against a band of 0.70–0.93 and a
    refutation line at 0.55. Ties are not the explanation: the tie structures cap
    it by at most 5×10⁻⁵, and the measurement falls 0.66 short of that ceiling.
  - **R-b NEITHER** — **45 of 208, 21.6%**: above the 20% refutation line and
    below the 35% band, in the dead zone between them. Robust to the tie-break,
    which can only move it between 20.7% and 21.6%.
  - **R-c HOLDS** — per-pair ratio p75/p25 = **1.880**, against a threshold of
    1.30. The ratio runs from 0.047 to 1.767, a factor of 37 end to end.
  - **R-d** reported: the space's closest pair ranks **1207 of 2080** on the
    corpus; the corpus's closest ranks **111 of 2080** on the space.

  **What it settles, and the one thing that does not fit.** The space cannot
  order two orders for deployment any more than it can rate them — the strong
  form of the reservation, now measured. The entry's own arithmetic checks out
  on the scale it used, 9.06% against 41.92%, both a standard deviation over a
  mean: the comparison was homogeneous and what went undeclared was the scale.
  What does not follow is the inference, and for a reason the decomposition
  cannot see: all 2,080 pairs are scored on the *same* 2,000 tickets, so the
  corpus is one common re-weighting rather than 2,080 independent draws. What is
  left is the alternative the entry named and dismissed — the pairs specialize in
  *where* they disagree, which R-c's factor of 37 measures directly. R-a's own
  text called refutation below 0.55 *the informative outcome*; it is the outcome.

---

## What rung 2 opens and does not resolve

- Why the proposer partitions instead of stratifying. Undiscriminated
  candidates: the framing of the task (one ticket, one rule), the specific model,
  or rule-writing elicitation in general.
- Whether any prompt or schema gets a proposer that sees the base to write
  overlapping rules. Versions v1 and v2 bound a range; they do not exhaust it.
- How to get a base that produces conflicts, which is the condition for
  `EDGE_CONTRADICTS` to measure anything. Eight runs produced almost none.
- Whether n=100 is enough. The bases vary by nearly an order of magnitude in size
  across seeds; overlap might emerge only as the base grows.
- The cost of authorship at scale. What a perfect author declares for the 29
  hidden rules is in `FINDINGS2.md`; for a learned base it is unknown.
- What happens when subsumption and declaration contradict each other in a
  learned base. That design decision has not been put to the test even once.
- The attributes the proposer does not use — `language` above all, in none of the
  eight runs. The audit is in `FINDINGS2.md` §4.

---

## Technical debt

Work pending **on the repo as software**, not on the experiment. It is of a
different nature from the rest of this file and that is why it goes separately.
Real, but it changes no conclusion.

The three items that were here were closed on August 7, 2026, and that same day
two of the five consequences they left open were closed. The three that remain
all have the same root and are not closed by writing code.

### Done

- **Automated tests.** `python3 -m unittest discover` runs in seconds, with no API
  calls and no writes to `results*/`. They cover the two invariants that underpin
  rung 1 — the DSL reproduces the lambdas over the whole case space, and
  first-match-wins reproduces `true_action` — and pin the published ceilings to
  the digit, along with the mock frontier and the corpus. They add three controls
  that
  did not exist: that no component of the online loop imports the oracle, that
  `feedback.py` remains the only module in rung 4 that touches it, and that the
  greedy search of rungs 3 and 4 does not depend on `PYTHONHASHSEED`.
- **Pinned dependencies.** `openai` pinned to an exact version in
  `requirements.txt`, plus `requirements.lock.txt` with the transitive closure of
  the environment that produced the records. A test
  prevents the `>=` from coming back by oversight.
- **Environment record.** `harness/provenance.py` hangs an `_env` block off every
  JSON: Python, openai, platform, `PYTHONHASHSEED`, commit, a digest of the
  source code and **two** dirty flags — `code_dirty`, which is the one that
  decides whether the commit identifies what ran, and `git_dirty` for the rest of
  the tree, which is not harmless either because three writers read records as
  input. A test walks the repo and fails if a JSON writer turns up without
  `_env`.
- **The tests are run by something, not by someone** (August 7, 2026).
  `.githooks/pre-commit` before every commit — enabled with
  `git config core.hooksPath .githooks` — and `.github/workflows/pruebas.yml` on
  every push and every PR, on 3.10 and 3.12: the minimum the README declares and
  the interpreter that produced the records. The workflow additionally checks,
  after running the suite, that `results*/` is still intact, instead of trusting
  that the suite does not write there.
- **The LLM path, tested end to end and without spending** (August 7, 2026). The
  double (`tests/doubles.py`) does not replace the proposer but the **SDK
  client**, one rung lower, so `OpenRouterProposer` and `OpenRouterProposer2` run
  in full — prompt, `response_format`, retries, parsing — and the only thing that
  does not happen is the HTTP request. The responses are derived from the
  published record, not from a separate script: replaying `results/llm_run.json`
  reproduces its rules, its metrics and its raw per-case records exactly, and the
  same for `results2/llm_run2_n100.json` and its priority edges. As a bonus, a
  figure that was nowhere — **what those escalations really cost in calls**, above
  the escalation count because parse failures are retried. It lives where it is
  derived, in the header of `doubles.py`, with the turn-by-turn account of what is
  not recoverable: the raw text was never stored.

### What that leaves open

What remains shares a root: **it is not closed by writing code but by re-running
records**, and what is left to re-run either costs money or is deliberately
deferred.

- **The records still without `_env` are exactly the ones that cannot be
  reproduced for free.** The deterministic, free ones were re-run on August
  7, 2026 and earned it without a single datum changing — in that same pass
  `comparativa.json` and `note_audit.json` adopted their new shape,
  `{"_env": ..., "rows": [...]}`, with the same rows; see
  `results2/NOTA_REGISTRO.md`. Without `_env` there remain `llm_run.json`,
  `llm_run_n100_smoke.json` and the eight `llm_run2_*.json`: reproducing them
  costs money and they would not come out the same, because the proposer is not
  deterministic at `temperature 0`. It will appear in each one when there is a
  reason to pay for it, not before.
- **Rungs 3 and 4 are covered by determinism, not by snapshot, and their three
  records still have no `_env` for the same reason.** Their published figures are
  those of the code prior to the tie-break fix: re-running them is free, but it
  moves digits, and pinning the new values here would create a second official
  figure that no FINDINGS backs.

  **Half-resolved 2026-08-08.** The audit produced four new records that all
  carry `_env` — `optimizer_check.json`, `order_search_ls.json`,
  `order_search_ls_fullspace.json`, `sweep_ls.json` — and the FINDINGS of both
  rungs now publish the corrected figures as dated errata, so the second official
  figure has a document behind it. What is still open is the original three
  records: `order_search.json`, `budget_and_balance.json` and `sweep.json` remain
  pre-tie-break, without `_env`, and are deliberately left that way so the old
  numbers stay reproducible beside the new ones.

  **Closed 2026-08-13 for `budget_and_balance`**, which was the one still never
  re-run: step 3 of the audit measured the label-budget curve and the balanced
  objective with the declared optimizer and wrote `budget_and_balance_ls.json`,
  with `_env` and both surfaces named. The original record is untouched and
  still pre-tie-break, so the three columns — published, greedy-today,
  local-search-today — separate the 2026-08-06 tie-break fix from the optimizer
  for the first time. The figures and the dated erratum are in
  `results3/FINDINGS_AUDIT.md` and `results3/FINDINGS3.md` §4.

- **A test that reads the figures out of `results*/` and fails when a prose table
  disagrees. Considered on August 9, 2026 and deliberately not written.** It would
  work in the idiom of `test_automatizacion.py`, which pins the half of a decision
  that lives in the repository against the half that lives in a file: parse the
  numbers out of the Markdown, look them up in the JSON that owns them, fail on a
  mismatch. It was the alternative to de-duplicating, and the wrong one — it
  guards copies instead of removing them, and a green test on four copies of a
  figure still leaves four places for the next correction to be forgotten in.

  **Why not now.** The same day, the rung figures were removed from `README.md`,
  `CLAUDE.md` and this file, leaving each figure in the record that owns it and in
  `STATUS.md`, which indexes it. With two locations instead of four the drift
  surface is small enough that the test would guard a problem that mostly no
  longer exists, at the cost of a parser over prose — which breaks on reformatting
  and has to be maintained against every rewording.

  **What would make it worth doing:** prose figures creeping back into the
  navigational documents, or a third document that genuinely needs to carry
  numbers. Either restores the drift surface the test was meant to watch.

What is **not** here, on purpose: that reproducing a figure overwrites its own
record. For the deterministic, free ones that is behaviour you have to know
about, not a pending task — git is already the safeguard — and it is documented
with its full table in the README. The exception was closed on August 8, 2026:
the two commands that cost money now refuse to write over an existing record and
their output name carries the `--n`, so the smoke test no longer lands on the
full run's file (`harness/record_guard.py`).

---

## Prior to the four rungs

Of this list, the only thing that has been touched is the empirical impasse, and
only in part. The rest is exactly where it was.

- Novelty rung: new attributes or values halfway through the corpus
- Concept drift: the hidden policy changes at t=N/2 -> does it retire rules?
- Inexpressibility -> measure regret vs. the best representable policy
- Empirical impasse: parameterized feedback channel (coverage, delay, noise).
  **Partially done** in rung 4, in offline mode and with a fourth parameter —
  asymmetry — which turned out to be the deciding one. It remains undone in
  online mode and the rest of the parameter space remains unexplored.
- Diagnosis under ambiguity: drift or over-generality? Opposite repairs
- Comparison run with a more capable model, with the MODEL as the only variable
  (same seed, same prompt, same schema, same corpus). Requires averaging several
  sampling seeds: the proposer is not deterministic at temperature 0.
- Compiler to ASP (clingo) keeping the same input schema
- Promotion by directed test-case generation (independent generator)
- Full cost accounting -> is there an optimal base size?
