# Recorded prediction

Date: August 5, 2026
Run: n=2000, deepseek/deepseek-v4-flash, seed 17

| quantity                  | prediction | result |
|---------------------------|------------|--------|
| reuse                     |    0.70    |  0.158 |
| number of rules           |     200    |    577 |
| silent error              |    0.30    |  0.484 |
| escalation, last decile   |    0.20    |  0.670 |

Stopping threshold: if reuse < 0.30, this is not inducing anything and the
project gets rethought.

An informed prediction, not a blind one: made after seeing the n=100 run, the
analysis of R0002 (covers 19.1% of the corpus, born from a case resolved by the
catch-all H29) and the blind spot around prior_tickets_30d (decides 14.5% of the
corpus, used 0 times in 47 conditions).

Against Claude's prediction (0.5-0.7 reuse, excess rules): I predict higher reuse
and fewer rules.

The run is voided by the engine ceiling.

## Voiding — verified on August 5, 2026

The run does NOT measure the hypothesis. With the perfect hidden policy loaded
(29 rules, no LLM), the engine reaches 58.75% accuracy and declares CONFLICT on
25.3% of the cases. The silent-error ceiling was ~0.41 even if the model had
induced the exact policy. It obtained 0.484: it came within ~7 points of an
unreachable ceiling.

Cause: `RuleEngine.decide` arbitrates by specificity (number of conditions). The
hidden policy is a list prioritized by layers, and priority and specificity are
nearly orthogonal in it. Aggravating factor: `decide` returns CONFLICT before
applying the age tie-break, so the tie-break is unreachable precisely when it
would matter. That turns 83.2% into 58.75%.

The DSL is NOT the culprit: verified exhaustively over the 134,400 combinations
of the case space that the 29 rules in the DSL are equivalent to their lambdas
and that first-match-wins reproduces them exactly. An execution failure, not a
representation failure.

### Why the stopping threshold does not apply

594 of 632 escalations (94%) were CONFLICT, which is exactly what this
arbitration overproduces. Conflict → new rule → more overlap → more conflict.
Reuse, number of rules, dead rules, the escalation curve and both action
counterfactuals are products of that loop. The 0.158 does not measure whether
the LLM induces or memorizes.

### What DOES survive (independent of the arbitration)

- Generalization from the residue: the region `dashboard AND severity<=3` touches
  15 hidden rules and T1_GENERAL is the truth in only 21.5% of it. The
  originating case is resolved by H29, the catch-all. The proposer sees a correct
  answer and cannot know that it is correct by elimination. It happened in both
  runs, in different ways.
- Attribute blindness: prior_tickets_30d in 6.3% of the conditions written
  against the 14.5% of cases it decides; language in 0.2% despite H21 existing.
- Compilation destroyed capability: SECURITY_INCIDENT, 3/3 correct when the case
  reached the LLM, 0/17 when a compiled rule resolved it.

### The underlying design failure

No syntactic criterion recovers this policy. Demonstration with the hidden rules
themselves: H01 (2 conditions) must beat H03 (1); H16 (1) must beat H24 (2). No
monotone function of specificity satisfies both. And arrival-order arbitration
does not work either: same 29 rules, design order 100%, reverse order 12.8%,
random order 49.3% on average over 200 samples. In a learned base the arrival
order runs backwards from the correct one, because the first cases come from the
common distribution and beget default rules, while the exceptions are born late.

CONCLUSION: compilation by impasse learns rules, but has no mechanism whatsoever
for learning priority. In a stratified policy the structure lives in the
priority. It is a limitation of the design, not of the model or the engine.

### Process errors, for the record

- I (Sergi) took realizability for granted without verifying it.
- Claude wrote in the README that the policy was "entirely expressible in the
  DSL" having checked only the conditions, not the resolution semantics. It also
  predicted that random_k's conflict storm "probably would not bite" with a real
  LLM. It was the dominant mechanism.
- ChatGPT warned of exactly this risk (the hidden truth must be expressible in
  the DSL, otherwise the failure is uninterpretable). The warning was accepted
  and the check was not implemented.
- The defect was found by a verification that cost zero API calls and that
  should have been run BEFORE the run: load the true policy into the engine and
  measure its ceiling.
