# PLAN_REUSE — the founding question, on the engine that can answer it

**Status: drafted by Claude on 2026-09-29, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0**, and the signature has to land
before any figure named here exists — in its own commit, staged by name. That
includes Stage A, which spends nothing: §10 says why.

**This plan exists because the project's own question has never been answered.**
*Do the rules an LLM writes get reused, or does it memorize cases?* is what rung
1 was built to measure ([`README.md`](README.md), *Rung 1*), and every record
since says it is still open: rung 1's run was voided by its engine ceiling
([`PREDICTION.md`](PREDICTION.md)), and [`results/FINDINGS.md`](results/FINDINGS.md),
[`results4/FINDINGS4.md`](results4/FINDINGS4.md) §5 and [`STATUS.md`](STATUS.md),
*What this does not show*, repeat it.

**The configuration that could answer it exists and was never run at length.**
Rung 2's engine — subsumption plus declared priority — executes the hidden
policy at 1.0000 on the corpus and on the exhaustive space, so it passes the
STOP 0 that voided rung 1. With prompt v1 its escalations were coverage impasses
rather than conflicts: none of the four v1 runs produced a CONFLICT. But it was
only ever run at n=100, and [`results2/FINDINGS2.md`](results2/FINDINGS2.md),
*Caveats*, says so: *"Nothing here says what would happen at n=2000."*

**And those eight n=100 runs already carry a figure no record has read.** Found
while drafting this plan. `rung2/run2.py` prints `reuse_rate` right after the
rule count and writes it into every record; no FINDINGS, no analytical document
and no index has cited it since, and `results2/comparison.json`, the record built
over the eight runs, carries their silent error and leaves reuse out. In the eight
records it runs from **0.60 to 1.00** — above the 0.30 of Sergi's stopping
threshold of 2026-08-05, and far above the memorization floor — while the silent
error runs from **0.51 to 0.89** and the proposer chooses the right queue for the
ticket in front of it **0.20 to 0.43** of the time.

**That combination is why reuse cannot be the headline, and the reason is not
new.** The conversation of 2026-08-11 stated it: *"Partitioning does not
eliminate the errors — it eliminates the error detector"*
([`CHAT_SUMMARY.md`](CHAT_SUMMARY.md) §1, and §2.5 for where that framing came
from). A proposer that partitions writes broad disjoint rules; they fire, so they
count as reused, and nothing in the loop can tell that they are wrong. This plan
does not re-derive that; it measures what it costs. **It asks the founding
question in its own terms, because it is owed an answer in them (`U-a`), and then
the two questions that decide what the answer means**: which of the two error
axes `CLAUDE.md` Step 5 keeps apart carries the silent error (`U-c`), and whether,
on the scope axis alone, the rules generalize better than a fixed heuristic that
is handed the right action (`U-b`). That heuristic is the reference
[`harness/proposers.py`](harness/proposers.py) was built to trace — *"the reference
the real LLM is judged against afterwards"* — and that Step 1 of `CLAUDE.md`
declared *"NOT a valid reference while the Step 0 ceiling is not ~100%"*. Under
this engine the ceiling is 1.0000, and `U-g3` checks that the reference carries
over rather than assuming it.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic here, before the run, and every figure is on the
corpus the run saw, in arrival order**: for Stage B,
`generate_corpus(2000, seed=17)`, the same 2,000 cases as rung 1's voided run. The
loop is a shadow over arrivals and has no exhaustive-space reading; none of these
rows has one.

**Every adjudicated row is read on the median over the runs of Stage B** — `R`
repetitions of the same loop over the same corpus, §2 — and each run's own value
is published beside it. With `R = 1` the median is the run.

| id | claim | statistic | band | refuted by |
|---|---|---|---|---|
| **U-a** | **The founding question, in the terms it was signed in on 2026-08-05**: the rules get reused rather than memorizing cases | `reuse_rate`: rules that decide at least one case after the one they were born on, over all rules | **≥ 0.30** | **< 0.30** |
| **U-b** | **Reuse is not induction**: on the scope axis alone, the rules generalize *worse* than a fixed heuristic that is handed the right action | over the rules whose birth escalation chose the correct queue: their pooled silent error minus `F(their reuse rate)`, `F` the `keep_k` frontier on the same corpus (§5.2) | **> 0** | **≤ 0** |
| **U-c** | **The acting axis carries most of the error**: most silent errors are decided by rules whose birth action was already wrong | silent errors decided by rules born with the wrong queue, over all silent errors (§5.3) | **≥ 0.60** | **< 0.60** |
| **U-d** | **Coverage-driven escalation asks about the rarest queue**, which rung 1's conflict-driven loop never did ([`FINDINGS_ILP.md`](results_ilp/FINDINGS_ILP.md) §3) | escalations whose true queue is `ONCALL_ESCALATION`; the corpus holds 7 such cases | **≥ 1** | **0** |
| **U-e** | **The base stays partitioned as it grows**: showing the base keeps overlap suppressed at twenty times the horizon | `CONFLICT` outcomes over the 2,000 cases | **≤ 20** | **> 20** |
| **U-f** | *Reported, not adjudicated.* **Stage A**: the eight n=100 records read for the founding question for the first time | per run and pooled by prompt: `reuse_rate`, the split of the silent error by birth action, and `U-b`'s gap against the `keep_k` frontier on each run's own corpus at n=100 | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-09-29)**

**Why `U-f` cannot carry a band.** Its inputs have been on disk since 2026-08-07
and the drafter has read their top-level metrics, listed below. That is the case
the D entry of [`IDEAS.md`](IDEAS.md) settled for `D-d`: when a figure is
computable from data already on disk, no honest band can be written for it. It is
reported, outside the denominator, and it is the first thing this plan produces.

**What the drafter had already seen, declared so that the signature is
auditable.** The `metrics` block of each of the eight n=100 records —
`reuse_rate` 0.60 to 1.00, `silent_error_rate` 0.51 to 0.89,
`proposal_action_accuracy` 0.20 to 0.43, `e2e_accuracy` 0.08 to 0.42, 6 to 40
rules, 0 or 1 CONFLICTs, final-decile escalation 0.0 to 0.2 — and one rule and
one record of `llm_run2_n100.json`, opened to learn the format. The `keep_k` rows
of [`results/frontier.json`](results/frontier.json). Rung 1's figures in
`PREDICTION.md` and in the metrics of `results/llm_run.json`. The hidden policy's
source, read while checking the two rules that route `ONCALL_ESCALATION`, and the
arrival weights in `harness/domain.py`. **Not seen, because nobody has computed
them**: any split of those silent errors by birth action, any right-born subset,
any frontier gap, any per-class count of those runs' escalations, and every figure
at n=2000 under this engine.

**What the drafter expects, written down so the scoreboard can score it.**
`U-a`, `U-b`, `U-c` and `U-d` hold; **`U-e` is refuted**, and it is the row the
drafter trusts least. The reasoning for `U-e` is mechanical: the proposer is
shown at most `MAX_SHOWN = 12` rules, the nearest to the ticket by violated
conditions (`rung2/proposers2.py`), so once the base outgrows what it is shown it
can overlap rules it never saw — and rung 1 went from 1 CONFLICT at n=100 to 594
at n=2000. For the rest, one line each. `U-a`: the eight runs are already far
above its line at a twentieth of the horizon. `U-c`: a proposer that picks the
right queue about a third of the time writes about two rules in three with the
wrong action, and those rules decide wrongly unless their region happens to share
it.
`U-b`: the heuristic is handed the right action *and* an attribute order that
starts where the hidden policy's first layer does (§12). `U-d`: both rules that
route `ONCALL_ESCALATION` require `severity == 1`, which is 5% of arrivals
(`harness/domain.py`), and the rules of the n=100 bases are written around the
tickets that did arrive — so the first severity-1 enterprise ticket is likely to
find no rule over it.

**The drafter's record argues against most of that.** On `STATUS.md`'s
scoreboard 17 of 36 adjudicated rows came out refuted, and the ILP thread's
drafter expected four holds and got one. Four expected holds out of five is the
profile that went wrong last time. Sergi should read these bands as more likely
too comfortable than too strict, and tighten them at signature if he disagrees,
as he did with `A-b` and `A-d`.

**`U-a`'s reading, not its verdict, depends on `U-e`.** If CONFLICTs come back in
force, escalations stop being coverage impasses and reuse starts measuring the
arbitration again — rung 1's defect, reintroduced by the growth of the base. The
row is adjudicated as signed whatever happens. Stage C publishes beside it the
share of escalations that were CONFLICTs, and above one in four the record
carries rung 1's caveat next to `U-a` instead of letting it read as clean.

---

## 1. What is being bought, and what is already paid for

**Already paid for, and free to read: the eight n=100 records**,
`results2/llm_run2_n100*.json` — four with prompt v1 and four with v2, over the
corpora of seeds 17 to 20 (FINDINGS2, *Caveats*), committed on 2026-08-07. Stage
A reads them and spends nothing.

**Bought: `R` runs of rung 2's loop over the 2,000 cases of seed 17, prompt v1**,
unchanged in every respect that could move a figure: `rung2.engine2`,
`rung2.proposers2` with its v1 prompt, `rung2.shadow2`,
`deepseek/deepseek-v4-flash` and the proposer's own settings. Only the horizon
changes — 2,000 cases instead of 100 — and the number of repetitions.

**Cost.** One call per escalation, plus parse retries. **How many escalations a
run makes is not known and cannot be dry-run**: it depends on the rules the model
writes. The eight n=100 runs escalated 6 to 42 times in their first hundred cases
and ended at a final-decile rate of 0.0 to 0.2, which suggests a few hundred
calls per run of 2,000 — an extrapolation, not a measurement. The hard bound is
one escalation per case, 2,000 per run, each with its retries. Stage D of the
pairwise thread measured 7.6 s per call on a shorter prompt, and v1 shows up to
twelve rules. **Expect under an hour per run and cents at this model's price; the
worst case is most of a day and still cents.** Sequential, hard rule 3.

---

## 2. The choices that have to be made at signature time

Three, and none of them moves a band. **Signing §0 adopts the drafter's choice in
each unless the signature line says otherwise.**

- **The prompt: v1, or v2.** The drafter recommends **v1**. v2 adds the overlap
  arithmetic, resolved by the engine, and an explicit instruction to overlap
  ([`results2/FINDINGS2.md`](results2/FINDINGS2.md)), and the only two CONFLICTs
  of the eight runs are v2's. **Conflicts are what voided rung 1's reuse figure**,
  so a prompt that asks for them re-imports the defect this plan exists to avoid.
  v1 is also the smaller step from rung 1's proposer: the base in view and nothing
  else. Rung 1's own proposer under this engine is not offered — its bases
  overlapped on 17.5% of pairs at n=100 and 32.3% at n=2000 (FINDINGS2, *What is
  verifiable*), and with no declared edges, whatever of that overlap is neither
  nested nor same-action would come back as CONFLICT.
- **`R`, the number of runs.** The drafter recommends **3**. The proposer is not
  deterministic at temperature 0 (`CLAUDE.md`, Step 3), so one run is one draw
  and three give a spread. Same corpus each time: what varies is the sampling,
  not the arrivals. Money is not the constraint at cents a run; time is, and three
  runs is an afternoon.
- **`PREDICTION.md`.** Step 4 of `CLAUDE.md` puts Sergi's own prediction before a
  long run, by hand, and hard rule 2 keeps the model out of that file — so this
  plan drafts no entry there and its gate does not look for one. §0 is a
  different instrument: the drafter's bands, for the scoreboard. Whether this run
  also gets a dated entry in `PREDICTION.md` is Sergi's to decide; the stopping
  threshold he wrote there on 2026-08-05 is already `U-a`'s line.

---

## 3. Reference figures, with the record that owns each

All on the corpus. Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| stopping threshold | reuse < 0.30 | Sergi's line of 2026-08-05: below it, *"this is not inducing anything"* | `PREDICTION.md` |
| memorization floor | 0.1176 | `keep_k(k=8)` at n=2000: rules that match one case exactly, reused only through the corpus's duplicates | `results/frontier.json` |
| the `keep_k` frontier | k = 1 … 8 | reuse and silent error of a heuristic handed the right action; `F` of §5.2 | `results/frontier.json` |
| rung 1's reuse | 0.1577 | voided: 594 of its 632 escalations were CONFLICT | `results/llm_run.json` |
| rung 1's proposal action accuracy | 0.3877 | the acting axis, over those 632 escalations | `results/llm_run.json` |
| rung 2's engine | 1.0000 | the hidden policy executed, corpus and space | `results2/ceiling2.json`, `results2/ceiling2_space.json` |
| the eight n=100 runs | §0 | the metrics blocks the drafter has read | `results2/FINDINGS2.md`, *Caveats*, erratum of 2026-09-29 — read off `results2/llm_run2_n100*.json` |
| the rare classes | 20 and 7 | `SECURITY_INCIDENT` and `ONCALL_ESCALATION` among the 2,000 | `results3/FINDINGS3.md` §2 |

> **[NOTE 2026-09-29] The eight n=100 runs have an owner now, and the row above
> points at it.** When this plan was drafted, no record had read their
> `reuse_rate`, and the header says so. Later the same day
> [`results2/FINDINGS2.md`](results2/FINDINGS2.md) took the eight rows in a dated
> erratum under its n=100 caveat, and `STATUS.md` indexes them. Written by the
> drafter before §0 was signed: no band moves, no row of §0 is touched, and what
> the drafter had seen when drafting is unchanged.

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** Stage A calls `harness/shadow.py`,
   which is part of it, as it stands; if a frozen file has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** The loop is sequential, and so are the runs: one after
   another, never side by side.
4. **Seed 17 for everything bought, no regeneration, and `results/llm_run.json`
   is read-only.** Stage A draws the corpora of seeds 17 to 20 at n=100 only to
   reproduce what the eight runs saw, and `U-g2` checks that it does.
   `harness/record_guard.py` guards this plan's paid records; the flag is not
   typed without Sergi asking.
5. **Do not adjust the prompt or the schema.** v1 as it produced the four v1
   records: not edited, not translated, not reformatted.
6. **If the numbers come out badly, report them.**
7. **The API key goes in the environment.** `eval "$(grep -m1 '^export
   OPENROUTER_API_KEY=' ~/.bashrc)"`, checked with `${#OPENROUTER_API_KEY}`.

And this plan's own, lettered:

A. **The loop is rung 2's, called and not copied.** `engine2`, `proposers2` and
   `shadow2` produced the eight records Stage A reads; a reimplementation would
   make n=100 and n=2000 incomparable for a reason that has nothing to do with
   the proposer.
B. **The eight n=100 records are inputs, never outputs.** Nothing under
   `results2/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §10 are fixed here and pinned by tests**, so that moving
   one after a figure exists is visible in a diff.

---

## 5. Known traps

**5.1 — Reuse counts rules, not decisions, and it is expected to be high.** A
rule that decides one case after its birth counts as reused as fully as one that
decides three hundred. Stage C publishes the distribution of fires beside `U-a` —
median fires per rule, dead rules, the top decile's share — and `U-a` is not to
be read as more than it is: the question in its own terms, owed an answer, and
not a measure of induction.

**5.2 — The two error axes are never summed, and the frontier speaks to one of
them.** Step 5 of `CLAUDE.md`: *the mocks get the correct action for free and the
LLM does not.* So `U-b` compares the frontier only with the LLM's rules whose
birth escalation chose the correct queue, and `U-c` is the other axis.
**`F`, precisely.** Take the points `(reuse_k, silent_error_k)` of `keep_k` for
`k = 1 … 8`, on the same corpus at the same `n`, ordered by reuse. `F(u)` is the
linear interpolation between the two points whose reuse brackets `u`; where two
points share a reuse — at n=2000, `k = 1` and `k = 2` both reuse every rule — the
lower silent error is the point; below the reuse of `keep_k(8)`, `F` is
`keep_k(8)`'s silent error. The right-born subset's **reuse rate** is its share of
rules that decide at least one case after birth, and its **silent error** is
pooled over the cases those rules decide. The gap is computed per run; if a run's
right-born rules decide no case, its gap is undefined and published as such, and
if no run has a gap, `U-b` is unadjudicable and says so.

> **[NOTE 2026-09-29] `F`'s two edges, found while implementing it.** A `keep_k`
> that decides no case has no silent error and says nothing about error, so its
> point is dropped; and beyond the highest reuse, `F` is flat, as it is below the
> lowest. Neither can happen at n=2000 — all eight `keep_k` decide cases there,
> and `keep_k(1)` reuses every rule — so `U-b` is untouched; only `U-f`, at
> n=100, can meet them. Written by the drafter before §0 was signed: no band
> moves and no row of §0 is touched.

**5.3 — A rule's birth is the escalation at its `born_at`.** Failed proposals and
rejected rules produce no rule. A rule whose birth escalation is missing, or
carries no `proposal_action_correct`, is a defect of the record and stops the
scoring: `U-g2` checks the eight old records and Stage C checks the new ones the
same way. A silent error is attributed to the rule that decided it, by
`winner_id`.

**5.4 — The proposer sees at most twelve rules.** At n=100 the bases had 6 to 40
rules, so it saw most of them; at n=2000 it will see a small share. This is the
mechanism the drafter expects to refute `U-e`, and it is a property of the
protocol, not a defect to fix mid-run (rule 5).

**5.5 — The model can change under its name.** The eight n=100 runs are from
early August; Stage B asks weeks later. [`PLAN_PROPOSER_1600.md`](PLAN_PROPOSER_1600.md)
§2 records the same hazard. So n=100 against n=2000 carries the date as an
uncontrolled variable, and every comparison between Stage A and Stage C is
labelled with it.

**5.6 — Seven cases.** `U-d` is a count over seven cases, deliberately: a rate
over seven is noise, and whether the loop asks at all is an event.
`SECURITY_INCIDENT`'s twenty are reported the same way — escalations and compiled
decisions, both counted — and not adjudicated.

---

## 6. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**. Both of the last two plans had their declared method killed by a
check like these, and both carry a signed amendment for it
([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md) §1, [`PLAN_ILP.md`](PLAN_ILP.md) §1).

- **U-g1 — STOP 0 for this engine, again.** `python3 -m rung2.ceiling_check2` and
  `python3 -m rung2.ceiling_check2_space` reproduce 1.0000 on both surfaces, and
  `python3 -m unittest discover` is green — it pins the corpus, the oracle
  separation, and the replay of `llm_run2_n100.json` through rung 2's LLM path.
  The engine is re-measured before a cent is spent on it, which is what Step 0 is
  for.
- **U-g2 — The eight records reproduce themselves.** For each of
  `results2/llm_run2_n100*.json`, every field of its `metrics` block that is a
  function of its `records` and `rules` alone recomputes exactly from them; the
  corpus redrawn at its seed carries the same `truth` and `truth_rule` case by
  case — read off the records the frozen loop writes for `U-g3`, so that no module
  of this plan imports the oracle; and every rule has exactly one birth escalation
  at its `born_at`, carrying a `proposal_action_correct`. A record that does not
  reproduce its own published metrics cannot be split, and Stage A stops.
- **U-g3 — The frontier does not depend on the engine, checked rather than
  argued.** `keep_k` writes `k` equality conditions over the same first `k`
  attributes, so a case can never be matched by two of its rules, and an engine
  that never has to arbitrate cannot matter — specificity and subsumption alike.
  The check: `keep_k(1 … 8)` over the n=2000 corpus reproduces
  `results/frontier.json` exactly, and in no run of it — at n=2000, or at n=100
  over seeds 17 to 20 — is any case matched by more than one rule. If either
  fails, `F` is not the reference §5.2 says it is, and `U-b` is unadjudicable.
- **U-g4 — The signature**, §10.

> **[NOTE 2026-09-29] Run before signature, with Sergi's leave, and all three
> pass.** `python3 -m reuse.run --dry-run`, zero API calls, nothing written:
> `U-g1` — corpus and space at 1.0000, no silent error, no CONFLICT, no IMPASSE,
> and the suite green; `U-g2` — the eight records reproduce themselves, 8 of 8;
> `U-g3` — `keep_k` reproduces `results/frontier.json`, and no case is matched by
> more than one of its rules. The checks were brought forward so that a failure
> would become a fix to this draft rather than a signed amendment, as it did in
> both of the last two plans; none did. One change of method, not of check:
> `U-g1` measures the two ceilings in memory with
> `rung2.ceiling_check2_space.measure` instead of running the two commands,
> which rewrite their own published records. The dry run prints pass or fail
> and figures already published, never one of Stage A. Written by the drafter
> before §0 was signed: no band moves and no row of §0 is touched.

---

## 7. Stage A — the eight records, read for the founding question (free)

**Deliverable.** `reuse/readout.py` → `results_reuse/readout_n100.json`, and
`reuse/frontier.py` → `results_reuse/frontier.json`.

**What it does.** For each of the eight records: `U-g2`; the split of its silent
errors by the birth action of the rule that decided them; the right-born subset's
reuse and silent error; `keep_k(1 … 8)` over that record's own corpus —
`generate_corpus(100, seed)` through the frozen `run_shadow`, exactly as
`run_experiment.py frontier` does at n=2000 — and the gap of §5.2. Per run, then
pooled by prompt. Also each run's escalations by true queue, and **the
memorization floor at n=100** on each corpus, `keep_k(8)`'s reuse there: the
0.1176 of n=2000 is not the floor at a twentieth of the horizon.

**It produces `U-f` and nothing adjudicable**, and it runs after §0 is signed so
that none of its figures can inform a band.

---

## 8. Stage B — the runs (`R` × n=2000, gated on §0)

**Deliverable.** `reuse/run.py` → `results_reuse/run_n2000_r1.json` … `_r{R}.json`,
preceded by `results_reuse/run_n20_smoke.json`.

**Protocol, identical to the four v1 records in every respect but `n`**: the
corpus of seed 17; a fresh `PriorityEngine(space=Space())`;
`OpenRouterProposer2(model, prompt_version="v1")`; `run_shadow2` — called, not
copied (rule A). Every run starts from an empty base and sees no other run's
rules.

**Before the first run, `U-g1` to `U-g4`, all blocking. Then the smoke run**, 20
cases under its own tag: it checks the client, the key and the shape of the
record, costs a handful of calls, and adjudicates nothing.

---

## 9. Stage C — scoring, and the five adjudications (free)

**Deliverable.** `reuse/score.py` → `results_reuse/score.json`, and
`results_reuse/FINDINGS_REUSE.md`, which owns every figure.

`U-a` from each run's metrics. `U-b` and `U-c` from its records and rules, with
the definitions of §5.2 and §5.3. `U-d` and `U-e` from its records. The median
over runs adjudicates; each run's value is published beside it.

**Also record, outside every denominator:**

- the distribution of fires — median per rule, dead rules, the top decile's share
  (§5.1);
- `e2e_accuracy`, `silent_error_rate` and `proposal_action_accuracy`, beside one
  another and never summed (§5.2);
- the escalation curve by decile, and the share of escalations that were
  CONFLICTs — `U-a`'s reading depends on it (§0);
- `SECURITY_INCIDENT`'s escalations and compiled decisions, counted (§5.6);
- edges proposed and accepted, with their `try_edge` verdicts: `EDGE_CONTRADICTS`
  has never fired in a real run, and a base that grows past what the proposer
  sees is its first chance;
- the number of rules, and the spread of every row over the `R` runs.

---

## 10. The gate, and where the code lives

**Two modules write this plan's records, and both refuse to while §0 is
unsigned**: `reuse/readout.py`, which spends nothing, and `reuse/run.py`, which
refuses before it constructs the client. **The free stage gets a gate because
what the gate protects is not money** ([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md)
§8): Stage A's figures are exactly what would inform `U-b`'s and `U-c`'s bands,
and without the gate the only thing between them is commit order.

**It reads `PLAN_REUSE.md` and no other plan, and it counts signatures rather
than stopping at the first**: every line starting `**Signed by Sergi:` must be
filled in, and there must be at least one. Today there is one. If a blocking check
forces an amendment — as it did in both of the last two plans — the amendment
carries its own signature line, and a gate that reads every line cannot report
`ok` over it. No flag skips the gate; `--dry-run` runs `U-g1` to `U-g3` and writes
nothing.

> **[NOTE 2026-09-29] Four modules write, not two, and all four refuse.** The
> paragraph above counts `readout.py` and `run.py`, and the layout below it names
> two more writers: `frontier.py`, whose record holds Stage A's reference points,
> and `score.py`, which writes Stage C's. The implementation gates all four, each
> before it measures, builds or writes anything, and `run.py` before it builds
> the client. Written by the drafter before §0 was signed: no band moves and no
> row of §0 is touched.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:** `N = 2000`, `SEED = 17`, `PROMPT = "v1"`,
`MODEL = "deepseek/deepseek-v4-flash"`, `REPS = 3` unless the signature says
otherwise, and the five lines of §0 — `0.30`, `0`, `0.60`, `1` and `20`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
reuse/__init__.py
reuse/readout.py      Stage A: the eight n=100 records, U-g2, U-f
reuse/frontier.py     keep_k through the frozen loop, n=100 and n=2000, U-g3
reuse/run.py          Stage B: rung 2's loop behind U-g4; it spends
reuse/score.py        Stage C: U-a to U-e, median over runs
results_reuse/FINDINGS_REUSE.md
results_reuse/readout_n100.json  frontier.json  run_n20_smoke.json
results_reuse/run_n2000_r1.json … run_n2000_r{R}.json  score.json
```

**The plumbing, in the same commit as the modules**, because each of these lists
has drifted before when it was left for later: `reuse` joins `CODE_ROOTS` in
`harness/provenance.py` and the oracle scan's roots in
`tests/test_oracle_separation.py`; `reuse/run.py` joins `ONLINE_LOOP` there, since
it is a proposer path; the guarded writers in `tests/test_writer_lists.py` grow
from three to four; and the README's table of writers gains its rows. **The list
of modules allowed to see the oracle does not grow**: every label this plan reads
comes from a record — the frozen loop's for `keep_k`, the runs' own for the LLM —
and none of its modules imports `hidden_policy`.

---

## 11. Definition of done

- [ ] Records under `results_reuse/` with `_env`, produced with
      `PYTHONHASHSEED=0`.
- [ ] `U-g1` to `U-g4` passed before any record was written; the smoke run before
      the first full run.
- [ ] The plumbing of §10, and tests pinning the constants of §10 and the
      definitions of §5.2 and §5.3; the whole suite green.
- [ ] Every figure in prose names its surface — the corpus, here, always — and
      every comparison between n=100 and n=2000 names the date of §5.5.
- [ ] `results_reuse/FINDINGS_REUSE.md` owns every figure, with a dated erratum
      wherever it corrects something already published — **including
      `STATUS.md`, *What this does not show*, and `README.md`, *Rung 1***, which
      say the question has never been measured, whichever way the rows come out.
- [ ] `STATUS.md`: the scoreboard gains the `U` thread — five adjudicated rows
      and one reported — and the entry points at the record.
- [ ] `IDEAS.md`: *Whether n=100 is enough*, in the rung 2 list, closed or
      narrowed by `U-e`; the rare-class item of *Pending and already specified*
      by `U-d`; and whatever this opens, added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 12. What this plan cannot settle, declared before it runs

1. **It does not measure fidelity.** Whether a compiled rule decides a later case
   the way the model would have decided it is the cleanest form of the question,
   and it needs the model's answer on cases the rules decided — more calls and a
   second protocol. The split by birth action (`U-c`) is a proxy for it, not a
   measurement of it, and fidelity is the natural next plan if this one says the
   acting axis dominates.
2. **The frontier is a strong baseline, and that is declared rather than
   hidden.** `keep_k` is handed the right action, and it keeps attributes in the
   order `harness/domain.py` fixes as *"the priority a reasonable analyst would
   give to the attributes"* — which puts `has_security_keyword` first, where the
   hidden policy's first layer sits. A proposer that loses to it has lost to an
   informed heuristic, not to a blind one. `random_k` is not used: its rules
   overlap one another, so under an engine that arbitrates them they conflict
   instead of generalizing — its rows in `results/frontier.json` are almost all
   CONFLICT.
3. **One model, one corpus, `R` draws.** `deepseek/deepseek-v4-flash`, as in every
   paid record. Another model is an item of `IDEAS.md`, not of this plan.
4. **It does not touch the material problem, declared priority or the prompt.**
   `T3_ENGINEERING` and `ACCOUNT_MANAGER` keep their missing rules; edges are
   recorded, not studied; and if the answer is bad, the repair is a different plan
   that starts from this recorded result, which is rule 5.
5. **It cannot rehabilitate reuse as the success criterion.** If `U-a`, `U-b` and
   `U-c` all hold, the finding is that the architecture's founding metric was the
   wrong one: the rules get reused and are wrong, and the loop cannot see it. That
   is a result about the question as much as about the proposer, and the record
   says so rather than reporting `U-a` alone.
