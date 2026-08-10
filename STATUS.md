# Status

What is known, as of August 9, 2026. **Not a history** — that is the four
`FINDINGS` records and [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), each with its dated
errata in place. Every figure here already exists in one of them.

**The project.** A cheap symbolic engine resolves the cases it covers; on one it
does not cover (an *impasse*), an LLM acts and writes a rule so that next time it
does. Ticket triage: 8 attributes, 8 queues, a hidden policy of 29 rules in 8
priority layers. Four rungs closed, plus an audit of the instrument behind two of
them.

**In one sentence.** The priority of a stratified policy is not in the shape of
its rules; of the three ways of supplying it — infer it from the syntax, have the
proposer declare it, learn it from observed behaviour — the first is falsified,
the second was never exercised, and the third recovers 61% of what full
supervision buys.

---

## Before reading any figure

**Every figure names a surface, and the two are not interchangeable.** The
**corpus** is the modelled arrival distribution, deliberately long-tailed
(`has_security_keyword`: 3% of arrivals against 50% of the attribute space). The
**exhaustive space** is the uniform measure over all 134,400 combinations. The
corpus answers *what would this achieve in deployment* and cannot certify an
optimum — its 2000 draws touch 1743 distinct cases and leave the rest
unconstrained, so an order can be perfect on it and be 0.9455 as a function. The
space answers *is this order the policy*, and weights regions the system will
almost never see. Neither is *the* bound. Rungs 1 to 4 published corpus figures
without saying so; everything below is labelled.

**Every finding came from a check costing cents or nothing**, never from the
expensive run. Three failures were caught by a blocking free check, each of which
changed a conclusion:

- **Aug 5** · `harness.ceiling_check`: the engine scores 0.5875 with the
  *perfect* policy loaded. It voided an n=2000 run already paid for
  ([`PREDICTION.md`](PREDICTION.md)).
- **Aug 8** · `peldano3.optimizer_check`: the neighbourhood the audit had
  declared, pairwise swaps, cannot solve the 29-rule instance whose optimum is
  1.0000 — 0 of 65 starts reach it.
- **Aug 8** · the same check, on the other surface: the corpus would have
  certified that instrument anyway — orders perfect on its 2000 cases score
  0.9455 and 0.9299 as functions
  ([`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), Step 0).

Money bought only rung 1's 577 rules and rung 2's eight runs. Rungs 3 and 4 and
the audit cost zero API calls.

---

## What is established

**Priority is not recoverable from the syntactic shape of the rules.** Three
criteria falsified, perfect policy loaded, no LLM, on the corpus —
[`results/FINDINGS.md`](results/FINDINGS.md):

- *specificity*: e2e **0.5875**, CONFLICT 25.3%. No monotone function of it can
  work — H01 (2 conditions) must beat H03 (1), H16 (1) must beat H24 (2).
- *arrival order*: 100% in design order, 12.8% reversed, **49.3%** random. It
  carries no signal of its own, and in a learned base it runs backwards: defaults
  are born early, exceptions late.
- *subsumption*: silent error **0.0000** over the hand-written policy, **53.12%**
  over the learned base. A proxy for *authored* priority — the 0.0000 measures a
  virtue of the author.

**Execution failure, not representation failure.** Over the exhaustive space the
29 DSL rules are equivalent to their lambdas, and first-match-wins reproduces the
policy exactly.

**The mechanism for executing declared priority works.** Subsumption plus 199
declared edges: e2e **1.0000**, silent error 0.0000, zero conflicts, zero
impasses, on the corpus — [`results2/FINDINGS2.md`](results2/FINDINGS2.md).

**The proposer does not feed it.** Shown the base, the overlap arithmetic
resolved for it and an explicit instruction to overlap, it writes mostly disjoint
rules and argues disjointness as a merit. Showing it the base *reduced* overlap
tenfold (17.5% of pairs → 1.60%); the instruction recovered part of it (7.25%)
and never reached the starting point. Eight runs, ~200 escalations: **2
conflicts, 14 proposed edges, 0 accepted**. `language` appears in 0 of the 8
bases, `channel` and `prior_tickets_30d` in 1 each, though hidden layers built on
them decide 14.5% of the corpus.

**The material contained the signal; the arbitration destroyed it.** The same 577
rules that specificity turned into 0.1829 admit an order scoring **0.8530 ±
0.0062 on corpus test** (train 0.8695: overfitting of the order is 0.0165),
against a coverage bound of 0.9010 on the corpus and 0.8784 on the space —
[`results3/FINDINGS3.md`](results3/FINDINGS3.md) §1 and its 2026-08-08 erratum,
[`order_search_ls.json`](results3/order_search_ls.json). That bound is an **upper
bound by per-case coverage**, not a demonstrated attainable optimum. The same
order scores 0.6105 on the space, and a search seeing all 134,400 cases reaches
0.7905 ([`order_search_ls_fullspace.json`](results3/order_search_ls_fullspace.json)).
The search uses the oracle: the material contains the signal, which is not the
same as it being reachable without labels.

**An ordering problem and a material problem are different things.** Six classes
of eight — 1774 of 2000 cases — are pure ordering. `SECURITY_INCIDENT` (20 cases)
and `ONCALL_ESCALATION` (7) are **100% recoverable** and rung 1 gave **0/17** and
**0/7**. But 66.7% of `T3_ENGINEERING` and 64.2% of `ACCOUNT_MANAGER` have no
correct rule covering them at all; no order saves those. Corpus; FINDINGS3 §2.
Which classes get sacrificed is a choice of objective function, and rung 1's
arbitration was making it undeclared (§3).

**Priority is partly learnable from the feedback a real system gives.** Symmetric
supervision beats born_at by **+0.3273**; asymmetry 0 — feedback only on errors,
the only kind a deployed system produces — by **+0.2011**, 61% of it, on corpus
test ([`results4/FINDINGS4.md`](results4/FINDINGS4.md) §1 erratum,
[`sweep_ls.json`](results4/sweep_ls.json)). On the space the same orders give
0.6157 and 0.5757 against the 0.8784 bound: same direction, larger shortfall. The
learner never sees the truth by any route (the record's wording, "the only module
that imports `true_action`", was corrected — `sweep.py` carries an unused
import).

**The signal runs out as the system improves.** Under asymmetric feedback the
volume of labels is proportional to the error rate of the system observed, so
observing a worse π₀ produces a better order. A property of the channel, not of
the learner — the one section of rung 4 the audit left standing (FINDINGS4 §3).

---

## What was withdrawn, and why

The part a reader cannot reconstruct without reading everything in order.

1. **Rung 3's searched order: 0.7713 → 0.8530** (corpus test). The greedy was
   myopic; a multi-start local search recovered 63% of the gap to the bound.
   Cause: the optimizer audit, validated first against a policy whose optimum is
   1.0000 by construction. FINDINGS3 §4 erratum.
2. **Rung 3's 0.9010 stopped being a "ceiling"** and became an upper bound by
   per-case coverage — no order is known to attain it. Cause: re-reading what
   `ceiling()` computes, not a new measurement. FINDINGS3 §1 erratum.
3. **Rung 3's rehabilitation of arrival order was withdrawn.** "born_at already
   scores 0.52" is a corpus artifact: on the space it is *worse* than shuffling,
   0.3148 against 0.3768. Cause: naming the surface for the first time. FINDINGS3
   §1 erratum of 2026-08-08.
4. **Rung 4's "change of regime" in asymmetry was withdrawn**: +0.067 became
   **+0.2011**, the cliff between asymmetry 0.25 and 0.1 vanished, the
   symmetric-to-asymmetric ratio fell from 3.5x to 1.6x. What read as a property
   of the channel was the shape of a weak learner's failure curve. Cause: the same
   optimizer. FINDINGS4 §1 and §5 errata.
5. **Rung 4's "more noise gives better results" is gone.** Falsifying 10% of the
   labels bought +0.060 and now buys +0.0013, inside its spread; the sweep is a
   monotone degradation curve. Cause: the noise was supplying the restarts the
   search lacked. The record diagnosed that mechanism correctly and refused to
   change the method, which is what later made the fix legitimate. FINDINGS4 §4
   erratum.
6. **Rung 4's anchor cell was not "completely deterministic."** It spreads 0.0111
   across `PYTHONHASHSEED`, and the null test that had ruled tie-break
   instability out permuted a list the argmax never iterated — a true 0.0000 that
   measured nothing. Cause: the tie-break ran over a `set`. Fixed 2026-08-06,
   worth +0.0002, which is what later separated tie-break from algorithm.
   FINDINGS4 §1 and §4 errata.

---

## What is open

Not all of [`IDEAS.md`](IDEAS.md) — the ones that would change a conclusion.

1. **`budget_and_balance` was never re-run with the audited optimizer**
   ([`results3/budget_and_balance.json`](results3/budget_and_balance.json)). The
   only figure of rungs 3 and 4 still produced entirely by the superseded greedy,
   and the source of *50 labels are enough to order* — the premise rung 4 was
   opened on. Both its results would move: the label-budget curve and the
   balanced-vs-total objective comparison. Decides whether cheap supervision is
   really nearly free, and what protecting the rare critical classes costs.
2. **Whether the residue under the coverage bound is slack or search weakness.** A
   search seeing all 134,400 cases still stops 0.0879 below it, down from the
   greedy's 0.1187 — evidence the bound is loose, not proof, since a heuristic
   that misses a bound never distinguishes the two. Exact optimization would
   settle it. FINDINGS3 §4 erratum.
3. **Why the proposer partitions instead of stratifying, and why it wrote nothing
   correct for two classes.** Rung 2's mechanism stays unmeasured until a base
   produces conflicts, and the 66.7%/64.2% material gap has no explanation.
   Undiscriminated: the framing (one ticket, one rule), the model, or rule-writing
   elicitation in general. FINDINGS2, "Why this is NOT a capability failure".
4. **ILP (Popper/ILASP) as a competitor.** Specified as Step B of rung 3, never
   run, still unauthorized. Decides whether the LLM proposer does work a cheaper
   inducer could not.

---

## What this does not show

**The original hypothesis — do the LLM's rules get reused, or does it memorize
cases? — has still never been measured cleanly.** It is the question the project
was built to answer.

Rung 1's **0.158 reuse** describes the arbitration, not the induction: 594 of its
632 escalations (94%) were CONFLICT, exactly what specificity-based arbitration
overproduces, and reuse, rule count, dead rules and the escalation curve are all
products of that loop ([`PREDICTION.md`](PREDICTION.md), "Why the stopping
threshold does not apply"). The engine ceiling underneath it was 0.5875.

Rung 2 built an engine with a 1.0000 ceiling, and then the change that made
declared priority possible — showing the proposer the base — is the one that left
it without material: 2 conflicts in 8 runs.

Whatever measures it next must clear the memorization floor: `keep_k(k=8)`
reaches **0.1176** reuse without inducing anything, purely from the corpus's
12.8% duplicates ([`results/frontier.json`](results/frontier.json)). A figure near
0.118 is noise.
