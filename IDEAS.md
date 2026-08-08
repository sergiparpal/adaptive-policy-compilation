# Parking lot

Status as of August 8, 2026. Rungs 1, 2, 3 and 4 closed; see
`results/FINDINGS.md`, `results2/FINDINGS2.md`, `results3/FINDINGS3.md` and
`results4/FINDINGS4.md`. The optimizer audit of August 8, 2026 (`PLAN_AUDIT.md`)
corrected figures in rungs 3 and 4 in place. This is a list of things not done,
none of them developed and in no order of precedence.

---

## No longer here

- **Give the proposer the existing rule base as context.** Rung 2. It reduced
  the overlap between its rules by a factor of 10 and left the declared-priority
  mechanism — which that same change was meant to enable — with no material.
- **Priority by search over the corpus, without an LLM.** Rung 3. Coverage bound
  0.90 over the 577 rules from rung 1 — an upper bound case by case, not a
  demonstrated attainable optimum, see the erratum in `FINDINGS3.md` — and a
  searched order of 0.77 on test with gap ~0. The search uses the oracle.
  **Corrected 2026-08-08: 0.8530 with a competent optimizer, and the bound over
  the exhaustive space is 0.8784, not 0.9010.**
- **Priority learned from observed behaviour.** Rung 4, Step A. With symmetric
  feedback almost everything is recovered; with the asymmetric kind, which is the
  realistic one, +0.067 over learning nothing remains. **Corrected 2026-08-08:
  +0.2011, and the "change of regime" was a weak learner's failure curve.**
- **A serious optimizer for the order, and the audit of what the greedy cost.**
  August 8, 2026. Multi-start local search, validated first against the hidden
  policy whose optimum is known by construction. It answered the three questions
  the greedy left open — how much of the gap was search weakness (63%), whether
  noise still helps (no), whether the asymmetry regime change survives (no) — and
  cost zero API calls. `PLAN_AUDIT.md`, `results3/optimizer_check.json`,
  `results3/order_search_ls.json`, `results4/sweep_ls.json`.
- **Re-run rungs 3 and 4 with the tie-break fixed.** Done in the same pass, which
  is what made the two effects separable: the tie-break was worth **+0.0002** on
  test and the algorithm **+0.0817**. The fragility was variance, not bias.

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
  feedback recovers 61% of what full supervision does, not 29%, so "it would only
  degrade things further" now rests on a smaller margin than when it was written.

---

## What rung 4 opens and does not resolve

- ~~The greedy search is a weak optimizer, and that contaminates backwards.~~
  **Closed 2026-08-08.** It did, and upwards: every figure moved in the same
  direction, +0.0817 on rung 3's test and +0.134 on rung 4's anchor cell.
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

- How much of the 0.77→0.90 gap is really attainable. The 90.1% is an upper bound
  by per-case coverage: it guarantees that no order exceeds it, not that some
  order reaches it. Exact optimization or a stronger global bound would be
  needed. See the erratum in `FINDINGS3.md`. **Partly answered 2026-08-08**: 63%
  of it was search weakness. A search seeing all 134,400 cases still stops 0.0879
  under the space bound, down from the greedy's 0.1187 — evidence the bound is
  somewhat loose, not proof. Exact optimization is still what would settle it.
- **Which surface a figure is measured on, as a standing question.** Opened
  2026-08-08. The corpus is the modelled arrival distribution and the exhaustive
  space is a uniform measure over attribute combinations; they are not
  interchangeable and this project published corpus figures for four rungs
  without saying so. An order fitted to the corpus loses 0.180 carried to the
  space, and `born_at` reverses against random between the two. Every future
  figure should name its surface.
- Whether the order is attainable without labels. The shadow loop has no
  supervision channel by design. Rung 4 partially bounded this question and the
  answer was bad.
- Why the proposer did not write correct rules for `T3_ENGINEERING` or
  `ACCOUNT_MANAGER` (66.7% and 64.2% of those classes with not a single correct
  rule covering them). It is a material problem, not an ordering one, and it has
  no explanation.
- Whether a proposer that is shown the gaps in the ceiling would fill them.
- The objective function as an explicit design surface: which classes are
  protected, at what cost in aggregate, and who decides.
- Why rung 2's hybrid arbitration is worse than pure ordering over a learned base
  (0.7496 versus 0.7711) despite executing the perfect policy at 100%. It stays
  worse under a competent optimizer — 0.7734 against 0.8530 — so it is not a
  search artifact.
- **Subsumption silences a third of the learned base, and that is a finding about
  subsumption, not about runtime.** Opened 2026-08-08 while measuring why the
  hybrid pool costs 8x more to search: once subsumption prunes, **181 of the 577
  rules match nothing at all on the train half**. They are rules whose extension
  is strictly contained in another's, so on every case they cover, something else
  covers it too and outranks them. A third of what the proposer wrote is
  unreachable by construction under that arbitration, before any question of
  order. It is the mechanical form of what `FINDINGS3.md` measures as "subsumption
  costs 0.047 of ceiling", and it says the cost is concentrated rather than
  diffuse. Whether those 181 are redundant or are exceptions the arbitration
  buries is not known.

---

## What rung 2 opens and does not resolve

- Why the proposer partitions instead of stratifying. Undiscriminated
  candidates: the framing of the task (one ticket, one rule), the specific model,
  or rule-writing elicitation in general.
- Whether any prompt or schema gets a proposer that sees the base to write
  overlapping rules. Versions v1 and v2 bound a range; they do not exhaust it.
- How to get a base that produces conflicts, which is the condition for
  `EDGE_CONTRADICTS` to measure anything. Eight runs and two conflicts.
- Whether n=100 is enough. The bases range from 6 to 40 rules; overlap might
  emerge only as the base grows.
- The cost of authorship at scale. 199 declared edges for 29 rules in Step 0;
  unknown for a learned base.
- What happens when subsumption and declaration contradict each other in a
  learned base. That design decision has not been put to the test even once.
- The attributes the proposer does not use: `language` in 0 of 8 runs, `channel`
  and `prior_tickets_30d` in 1 of 8.

---

## Technical debt

Work pending **on the repo as software**, not on the experiment. It is of a
different nature from the rest of this file and that is why it goes separately.
Real, but it changes no conclusion.

The three items that were here were closed on August 7, 2026, and that same day
two of the five consequences they left open were closed. The three that remain
all have the same root and are not closed by writing code.

### Done

- **Automated tests.** `python3 -m unittest discover` runs 315 tests in ~17 s,
  with no API calls and no writes to `results*/`. They cover the two invariants
  that underpin rung 1 — the DSL reproduces the lambdas over the 134,400
  combinations, and first-match-wins reproduces `true_action` — and pin the
  published figures to the digit: 0.5875 by specificity, 0.6315 by subsumption,
  1.0000 hybrid, the mock frontier and the corpus. They add three controls that
  did not exist: that no component of the online loop imports the oracle, that
  `feedback.py` remains the only module in rung 4 that touches it, and that the
  greedy search of rungs 3 and 4 does not depend on `PYTHONHASHSEED`.
- **Pinned dependencies.** `openai==2.53.0`, plus `requirements.lock.txt` with
  the transitive closure of the environment that produced the records. A test
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
  reproduces its 577 rules, its metrics and its 2000 raw records exactly, and the
  same for `results2/llm_run2_n100.json` and its priority edges. As a bonus, a
  figure that was nowhere: the 632 escalations cost **700 calls**, because the 34
  parse failures are retried. What is not recoverable — the raw text was never
  stored — is enumerated turn by turn in the header of `doubles.py`.

### What that leaves open

What remains shares a root: **it is not closed by writing code but by re-running
records**, and what is left to re-run either costs money or is deliberately
deferred.

- **Ten records still have no `_env`, and they are the ones that cannot be
  reproduced for free.** The six deterministic, free ones were re-run on August
  7, 2026 and earned it without a single datum changing — in that same pass
  `comparativa.json` and `note_audit.json` adopted their new shape,
  `{"_env": ..., "rows": [...]}`, with the same 8 rows; see
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
  numbers stay reproducible beside the new ones. `budget_and_balance` was not
  re-run with the new optimizer at all — the label-budget curve and the balanced
  objective are still greedy figures, and both would move.

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
