# Adaptive policy compilation

A cheap symbolic engine resolves the cases it covers; when it fails to cover one
(an *impasse*), an LLM acts and writes a new rule so that next time it does cover
it. Domain: support-ticket triage — 8 attributes, 8 queues, and a hidden policy
of 29 rules spread over 8 priority layers.

> **Note on language.** The prose of this repository is in English; the code is
> not. Module, package and field names stay as they are (`peldano2/` = rung 2),
> and the scripts still print their tables in Spanish. When a block below shows
> expected output, compare the **numbers**, not the words.

## Four closed rungs

| rung | what it measured | record |
|---|---|---|
| **1** · engine ceiling | specificity-based arbitration reaches **58.75%** with the perfect policy loaded; the LLM run was voided by that ceiling | [`results/FINDINGS.md`](results/FINDINGS.md) |
| **2** · declared priority | the hybrid engine (subsumption + declared priority) executes the layered policy at **100%**, but the proposer writes disjoint rules and never exercises it | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |
| **3** · priority by search | the 577 rules from rung 1 admit an order that scores **0.77** on test; arbitration was turning them into 0.18 | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) |
| **4** · priority from feedback | that order is **not** learnable from the asymmetric feedback a real system produces | [`results4/FINDINGS4.md`](results4/FINDINGS4.md) |

The thread that ties them together: the priority of a layered policy is not in
the shape of the rules, and the three ways of supplying it — infer it from the
syntax, have the proposer declare it, learn it from observed behaviour — have
all been measured and each fails for a different reason.

**The original hypothesis — do the rules an LLM writes get reused, or does it
memorize cases? — still has not been measured cleanly.** [`IDEAS.md`](IDEAS.md)
keeps the list of what remains open, including the known technical debt.

> **From "Rung 1" onwards, this file describes the specification and the
> operating procedure of that rung.** They remain valid as procedure, not as
> project status.
>
> Before citing any figure, read the **dated errata** each FINDINGS carries in
> place. Those of rungs 3 and 4 are additionally conditioned by a
> non-deterministic tie-break in the optimizer, fixed on August 6, 2026 and
> **not re-run**: the published numbers are those of the earlier code.

---

## Reproducing the four rungs

**All of this costs zero API calls and runs on the standard library**, no venv.
These are the measurements that underpin the four records; next to each command,
what it should print.

```bash
# --- RUNG 1 · the engine ceiling and the frontier ------------------------
python3 -m harness.ceiling_check      # specificity 0.5875 · design order 1.0000
python3 run_experiment.py frontier    # keep_k(k=4): 113 rules, silent err. 0.173

# --- RUNG 2 · hybrid engine: subsumption + declared priority -------------
python3 -m peldano2.ceiling_check2    # e2e 1.0000 · 0 conflicts · STOP 0 -> PASS
python3 -m peldano2.compare_runs results2/llm_run2_*.json   # the 8 runs
python3 -m peldano2.note_audit  results2/llm_run2_*.json    # attributes and notes

# --- RUNG 3 · order by search over the corpus ----------------------------
python3 -m peldano3.order_search      # bound 0.9010 · test ~0.77 · gap ~0
python3 -m peldano3.budget_and_balance  # label curve and balanced greedy

# --- RUNG 4 · order learned from a feedback channel ----------------------
python3 -m peldano4.sweep             # coverage/asymmetry/delay/noise sweeps
```

And before touching anything, the test suite: **249 tests in ~12 s, no API and
no writes to `results*/`.**

```bash
python3 -m unittest discover
```

The pre-commit hook and CI run it on their own; to enable the hook in your
clone, once:

```bash
git config core.hooksPath .githooks
```

> **Rungs 3 and 4 do not reproduce their published figures to the digit.** The
> optimizer's tie-break was non-deterministic (it depended on `PYTHONHASHSEED`)
> and was fixed on August 6, 2026 without re-running anything. Real example:
> `order_search` today prints `test 0.7713 · GAP 0.0062` where the record says
> `0.7711 · 0.0068`. Directions and magnitudes hold; the digits will move until
> both rungs are redone, which is planned to happen together with a serious
> optimizer. The bounds and the ceilings — 0.9010, 0.5875, 1.0000 — do **not**
> depend on the greedy search and do reproduce exactly.

**The only thing that costs money** is the real proposer, which needs the venv
and the key (see *Getting started*):

```bash
.venv/bin/python run_experiment.py llm --n 100                      # rung 1
.venv/bin/python -m peldano2.run2 --n 100 --seed 17 --prompt-version v2   # rung 2
```

`peldano2/run2.py` accepts `--prompt-version v1|v2`; both versions of the prompt
are kept in the code and every run stores in full the one it used. The record of
the change is in [`results2/CAMBIOS.md`](results2/CAMBIOS.md).

> ⚠️ **Reproducing a figure overwrites its own record.** Nearly all the scripts
> above dump their JSON on finishing, over the published file:
>
> | script | file it rewrites |
> |---|---|
> | `run_experiment.py frontier` | `results/frontier.json` |
> | `run_experiment.py llm` | **`results/llm_run.json`** ← see warning below |
> | `harness/subsumption_check.py` | `results/subsumption.json` |
> | `harness/learned_subsumption.py` | `results/learned_subsumption.json` |
> | `peldano2/ceiling_check2.py` | `results2/ceiling2.json` |
> | `peldano2/compare_runs.py` | `results2/comparativa.json` |
> | `peldano2/note_audit.py` | `results2/note_audit.json` |
> | `peldano2/run2.py` | `results2/llm_run2_<tag>.json` |
> | `peldano3/order_search.py` | `results3/order_search.json` |
> | `peldano3/budget_and_balance.py` | `results3/budget_and_balance.json` |
> | `peldano4/sweep.py` | `results4/sweep.json` |
>
> Of everything executed in this README, only `harness/ceiling_check.py` and
> `run_experiment.py models` write nothing.
>
> **The serious case is `run_experiment.py llm`.** It overwrites
> `results/llm_run.json`, which is not just the record of rung 1: it is the base
> of 577 rules that **rungs 3 and 4 start from**. Re-running it destroys the
> input of two closed rungs, and since the proposer is not deterministic at
> `temperature 0`, what comes out will not be the same. If you need to re-run
> it, save the original under another name first.
>
> In rungs 1 and 2 the rest of the computation is deterministic and the content
> comes out identical — what changes is the modification date of a closed record,
> see [`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md). In rungs 3 and 4
> **the content does change**, because the tie-break fix moves the digits.
>
> And there is a worse trap: `compare_runs` and `note_audit` rewrite with
> **whatever they are passed as an argument**. Invoking them with one file
> instead of with `results2/llm_run2_*.json` shrinks the record from 8 runs to 1.
> That is not a change of digits, it is data loss.
>
> Since August 7, 2026 there is one more detail: each JSON carries an `_env`
> block with the provenance (see *The tests and the provenance*). When you
> re-run a figure that has not changed, `git diff` shows **only** the
> `recorded_at` field moving — which is precisely the check that it still
> reproduces. The six deterministic, free records in the table already carry it:
> they were re-run that same day to earn it, with the content identical field by
> field ([`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md)). In that pass
> `comparativa.json` and `note_audit.json` also adopted their new shape,
> `{"_env": …, "rows": […]}` instead of the bare list, with the same 8 rows.
>
> **The safeguard is git, and it is enough.** After reproducing anything:
> `git status` gives away what was touched and `git checkout -- <file>` restores
> it. The records are versioned precisely for this.

---

## The tests and the provenance

Two different nets, with different purposes.

### The test suite

```bash
python3 -m unittest discover            # 249 tests, ~12 s, 0 API calls
python3 -m unittest tests.test_ceilings -v      # a single module
```

It needs no venv and **does not write to `results*/`**: it calls the measurement
functions, never the scripts' `main()`, which do dump their JSON.

What it covers, and why those things:

| module | what it protects |
|---|---|
| `test_encoding_invariant.py` | the 29 DSL rules ≡ their lambdas, and first-match-wins ≡ `true_action`, over the **134,400** combinations. This is the claim that "execution failure, not representation failure" rests on |
| `test_ceilings.py` | the four ceilings to the digit: 0.5875 · 0.6315 · 1.0000 · 1.0000, with their 505 and 737 conflicts and the 199 edges |
| `test_frontier.py` | the dry-run verification of Step 1 and the memorization floor (0.1176) |
| `test_domain.py` | the corpus: 1743 unique, 12.85% duplicates, and the 8 classes with their counts |
| `test_dsl.py` | the frozen DSL, including the **recorded defect** (CONFLICT is returned before the age tie-break), pinned on purpose |
| `test_shadow.py` | the semantics of the metrics, and that the only escalation trigger is the impasse — never "the answer was incorrect" |
| `test_engine2.py` | bitmasks ≡ `Condition.holds`, and the six verdicts of the edge validator |
| `test_oracle_separation.py` | that no component of the online loop imports the oracle, and that `feedback.py` remains the only module in rung 4 that touches it |
| `test_order_determinism.py` | that the greedy search of rungs 3 and 4 gives the same order under three `PYTHONHASHSEED` values, with a witness confirming that hashing really is randomized |
| `test_proposal_parsing.py` | the parsing of what the proposer returns, in both versions |
| `test_llm_path.py` | the **whole** LLM path, replaying the recorded runs without spending (see below) |
| `test_provenance.py` | the `_env` block, that it does not leak the key, and that no JSON writer is left without one |
| `test_automatizacion.py` | that the hook and the CI workflow are still there and still run what they say they run |

If a *snapshot* test fails, the expected number **is not updated**: you find out
what changed and, if the change is legitimate, you date the erratum in the
corresponding `FINDINGS`. Rungs 3 and 4 are covered by determinism rather than
by snapshot, on purpose: their published figures are those of the code prior to
the tie-break fix and are pending a re-run.

### The LLM path, without spending

Of the path that costs money, only the parsing was tested. The rest — building
the request, reading the SDK's response, retrying, validating, inserting the
rule into the base, computing the metrics — is now tested with a **double that
replaces the SDK client, not the proposer**: `OpenRouterProposer` and
`OpenRouterProposer2` run in full and the only thing that does not happen is the
HTTP request.

The responses do not come from a separate script but **from the published record
itself**, so that the replay is the run that produced the figures:

| record | what it reproduces, exactly |
|---|---|
| `results/llm_run.json` | 2000 cases, 632 escalations → the 577 rules, the metrics and the 2000 raw records |
| `results2/llm_run2_n100.json` | 100 cases, 42 escalations → the same, plus the 7 priority edges with their verdict |

That also yields a figure that is in no record: **632 escalations cost 700
calls**, because the 34 parse failures are retried up to three times. The raw
text of the responses was never stored; which part is reconstructed verbatim and
which part is only the failure mode is enumerated turn by turn in the header of
[`tests/doubles.py`](tests/doubles.py).

### Who runs the suite

Nobody has to remember:

```bash
git config core.hooksPath .githooks     # once per clone
```

[`.githooks/pre-commit`](.githooks/pre-commit) runs the suite before every
commit — ~12 s, no venv, no API — and aborts it on failure. It is skipped with
`git commit --no-verify`, which makes sense for a documentation-only commit and
in few other cases: if a snapshot fails, the expected number is not updated and
the commit is not forced either.

[`.github/workflows/pruebas.yml`](.github/workflows/pruebas.yml) does the same on
every push and every PR — including what was pushed with `--no-verify` — on
**3.10 and 3.12**: the minimum this README declares and the interpreter that
produced the records. And it adds a step the suite cannot do on its own: check,
after running it, that `results*/` is still intact.

The actions are pinned to the **full SHA** with their version in a comment
alongside, never to a tag: a tag can be repointed by its owner at other code, a
commit cannot. It is the convention of the rest of the repositories in this
account. To bump one, resolve the new tag to its commit —
`gh api repos/actions/checkout/commits/vX.Y.Z --jq .sha` — and change SHA and
comment together; there is a test that checks they travel together.

Each job carries `timeout-minutes: 10` over a ~45 s suite: it is not a speed
target, it is what turns a hung job into a failure instead of six hours of
runner. And superseded runs are cancelled… **except on `main`**. Here commits go
straight to `main` and the workflow status is the only record that a given
commit passed the suite; with a plain `cancel-in-progress: true`, pushing three
commits in a row leaves the first two *cancelled* forever — they did not fail,
they simply never got to answer.

And since a pinned SHA **does not age noisily** — it sits still and silent —
[`.github/dependabot.yml`](.github/dependabot.yml) proposes the bump every week.
It watches the actions and **not** `pip`, on purpose: `openai==2.53.0` and the
lock's transitive closure are not an outdated dependency, they are the
provenance of the environment that produced the records, and a weekly PR
proposing to bump them would train the habit of merging without looking.

### The `_env` block

Each results JSON opens with the provenance of the figure:

```json
"_env": {
  "recorded_at": "2026-08-07T14:38:14Z",
  "python": "3.12.3",
  "openai": null,
  "platform": "Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39",
  "pythonhashseed": null,
  "git_commit": "97cabc1f…",
  "git_dirty": false,
  "code_dirty": false,
  "code_digest": "7ef0ec6d89ec4d85",
  "seed": 17
}
```

`pythonhashseed: null` means **unset**, that is, random: it is information, not
the absence of it — any figure sensitive to the iteration order of a `set`
produced that way is suspect by construction, which is exactly what happened to
the greedy search of rungs 3 and 4. `code_digest` is a sha256 of the code that
produces figures (`harness/`, `peldano2..4/`, `run_experiment.py`; the tests are
left out), so it identifies the version even if the tree is dirty or there is no
git.

**There are two dirty flags and they are not redundant.** `code_dirty` is the
one that decides whether `git_commit` identifies what ran: with `false`, that
commit **is** the code. `git_dirty` covers everything else in the tree, and
everything else is not always harmless — `learned_subsumption`, `compare_runs`
and `note_audit` read records from `results*/` **as input**, so a modified and
uncommitted JSON also breaks traceability without touching a line of code. That
is why the broad flag was not narrowed: it was split in two (August 7, 2026,
while re-running six records back to back and discovering that each script
dirtied the tree for the next one with its own output; see
[`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md)).

The field appears in each file when that figure is re-run, so carrying it or not
splits the records today into two groups:

| they carry it | still without it, and why |
|---|---|
| `frontier.json`, `subsumption.json`, `learned_subsumption.json`, `ceiling2.json`, `comparativa.json`, `note_audit.json` — re-run on August 7, 2026, identical content | `llm_run.json`, `llm_run_n100_smoke.json` and the 8 `llm_run2_*.json` runs: reproducing them **costs money** and they do not come out the same (the proposer is not deterministic at `temperature 0`) |
| | `order_search.json`, `budget_and_balance.json`, `sweep.json`: they are free and deterministic, but re-running them **does move digits** (the tie-break fix) and it is deferred to be done together with the serious optimizer |

Put another way: what is still missing `_env` is exactly what cannot be
reproduced for free or what must not be reproduced yet.

---

## Rung 1

Static world · realizable hidden policy · **pure shadow** (no rule is ever
activated).

The single objective of this rung: **measure the reuse rate and the silent error**
of the rules an LLM writes. Nothing else. If reuse comes out low, the
architecture does not hold up and we stop.

**That objective was not met.** The run was voided by the engine ceiling before
reuse was interpretable, and it still has not been measured cleanly. What was
established is in the four records above.

---

## Frozen specification

**Case** — 8 attributes, sampled with a long-tail distribution:

| attribute | domain |
|---|---|
| `has_security_keyword` | bool (3% True) |
| `severity` | 1..4 (1=critical, 5%) |
| `customer_tier` | free / pro / business / enterprise (50/30/15/5) |
| `product` | dashboard / billing / api / mobile / integrations |
| `channel` | portal / email / chat / phone (phone 5%) |
| `prior_tickets_30d` | 0..20, truncated geometric |
| `off_hours` | bool (28%) |
| `language` | en / es / pt / de / fr |

**Actions** — 8 queues: `T1_GENERAL`, `T2_TECHNICAL`, `T3_ENGINEERING`,
`BILLING_SPECIALIST`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER`,
`ONCALL_ESCALATION`, `SELF_SERVICE_DEFLECT`.

**Hidden policy** — 29 rules prioritized into 8 layers (security overrides →
SLO/on-call → billing → churn risk → product → language/staffing → deflection →
defaults). First match wins. A hierarchical structure with real exceptions, not
independent rules.

**Expressible in the DSL, NOT executable by the engine.** The distinction was
verified on August 5, 2026 and is central to reading everything else:

- **Representation: correct.** Verified exhaustively over the **134,400
  combinations of the case space** that the 29 rules written in the DSL are
  equivalent to their original predicates, and that evaluating them with "first
  match wins" reproduces `true_action` exactly. The DSL loses nothing.
- **Execution: broken.** With those same 29 rules loaded into `RuleEngine` and no
  LLM involved, the engine reaches **58.75% accuracy** and declares **CONFLICT on
  25.3%** of the cases. Specificity-based arbitration cannot execute a policy
  prioritized by layers: in this policy, priority and number of conditions are
  nearly orthogonal.

The "rung 1 condition" (realizable hidden policy) holds at the level of
representation and fails at the level of execution. Reproducible for free with
`python3 -m harness.ceiling_check`.

**Rule schema** — the proposer never emits code:

```json
{"action": "T3_ENGINEERING",
 "conditions": [{"attr": "product", "op": "eq", "value": "api"},
                {"attr": "severity", "op": "lte", "value": 2}],
 "note": "..."}
```

Operators: `eq`, `neq`, `lte`, `gte`, `in`. `lte`/`gte` only over `severity` and
`prior_tickets_30d`.

**Engine** — three outcomes: `ACTION`, `IMPASSE` (coverage), `CONFLICT`
(logical). Conflicts resolved by specificity; a tie with different actions →
escalation.

**Escalation trigger** — *only* a coverage impasse or a conflict. **Never** "the
answer was incorrect". That restriction is what makes the silent error
measurable.

---

## Invariants of the experiment

1. **Oracle separation.** `hidden_policy.py` labels the record. Neither the
   engine nor the proposer ever consults it.
2. **Pure shadow.** No rule is activated. Tickets are independent, so the shadow
   is exact, not an approximation.
3. **The proposer does not touch the base.** It emits a payload; a deterministic
   validator accepts or rejects it.
4. **Fixed corpus.** Seed 17. It is not regenerated between variants.

---

## Step 0 is mandatory and blocking

```bash
python3 -m harness.ceiling_check
```

Loads the true hidden policy into the engine and measures its accuracy with no
LLM involved. If the engine cannot execute the correct policy, no measurement
over learned rules means anything. Until it gives ~100%, any LLM run is voided
in advance — which is what happened to the run of August 5, 2026 (see
[`PREDICTION.md`](PREDICTION.md)).

It costs zero API calls and is re-run after **any** change to the DSL, to the
arbitration or to the hidden policy.

---

## Getting started (5 minutes)

Requires **Python 3.10+**. Check with `python3 --version`.

Everything that does not call the LLM — the ceilings, `frontier` and rungs 2, 3
and 4 — works **with the standard library alone**. The venv is needed only for
the real proposer.

```bash
git clone https://github.com/sergiparpal/adaptive-triage.git
cd adaptive-triage

# 0. MANDATORY, and before anything else: the engine ceiling. 0 API calls.
#    If it does not give ~100%, STOP: nothing that follows will be interpretable.
python3 -m harness.ceiling_check

# 1. Check that everything works WITHOUT spending anything
python3 -m unittest discover
python3 run_experiment.py frontier

# 1b. Make the suite run by itself before every commit. Once per clone.
git config core.hooksPath .githooks

# 2. Virtual environment and SDK installation.
#    CAREFUL: on Debian/Ubuntu a global `pip install` fails with
#    "externally-managed-environment" (PEP 668). The venv avoids it, and it is
#    also in .gitignore, so it does not dirty the repo.
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. Key from openrouter.ai -> Keys. It goes in the environment, NEVER in a file
#    in the repo. If you export it in another terminal, the process will not
#    inherit it.
export OPENROUTER_API_KEY=sk-or-...        # Windows: set OPENROUTER_API_KEY=...

# 4. (optional) look up the exact slug of a model
.venv/bin/python run_experiment.py models deepseek

# 5. Smoke test first: see real rules and validate the parsing
.venv/bin/python run_experiment.py llm --n 100

# 6. Fill in PREDICTION.md, and only then the full run
.venv/bin/python run_experiment.py llm --n 2000
```

**Environment in which the published results were produced:** Python 3.12.3,
`openai` 2.53.0, Linux x86_64. `requirements.txt` pins that exact version and
`requirements.lock.txt` stores the full transitive closure; to rebuild the
environment to the digit, install the lock instead of `requirements.txt`. Since
August 7, 2026 each results JSON additionally records the environment it was
produced with, in its `_env` block.

**Default provider: OpenRouter.** Default model `deepseek/deepseek-v4-flash`.
Alternatives (all of them need the venv, because they call the LLM):

```bash
.venv/bin/python run_experiment.py llm --model openai/gpt-5.6-luna
.venv/bin/python run_experiment.py llm --model deepseek/deepseek-v4-flash-0731   # pinned revision
.venv/bin/python run_experiment.py llm --provider anthropic --model claude-haiku-4-5-20251001
```

With `--provider anthropic` you would additionally need the `anthropic` package
— which `requirements.txt` leaves commented out — and `ANTHROPIC_API_KEY`
instead of the OpenRouter one.

Having the proposer NOT be Claude is preferable: the harness and the hidden
policy were written by Claude, and it is better for the proposer to come from
another family.

**Cost.** Only escalations cost a call. With V4 Flash at around $0.09/$0.18 per
million tokens and a few hundred escalations at ~1,100 input tokens and ~200
output tokens, the full run costs cents. Verify it with `--n 100`.

**Duration.** The loop is **strictly sequential** and cannot be parallelized:
each new rule changes whether the next case escalates or not. Count on a few
minutes for 2000 cases, not seconds.

**Robustness.** Cheap models return dirty JSON. The parser tolerates markdown
fences, preambles and epilogues; unrecoverable failures are counted in
`failed_proposals` and invalid schemas in `rejected_rules`, without aborting the
run. If those two numbers come out high, the problem is the prompt, not the
architecture.

**Determinism: there is none.** The corpus is deterministic (seed 17), but the
proposer is not, not even at `temperature 0`. Verified on August 5, 2026: same
prompt, same case, same seed, and the rules born from the first cases differ
between the n=100 run and the n=2000 one. Two consequences:

- **the smoke test is not a prefix of the full run** — do not extrapolate from
  one to the other;
- **a comparison between models does not have the model as its only variable**
  unless several sampling seeds are averaged per model.

---

## How to read the frontier

The `keep_k` mocks do not "generalize": **they partition the case space into a
grid** by fixing the k most informative attributes with `eq`. They are therefore
a semantic cache parameterized by granularity — the mandatory baseline, already
included.

The LLM has an advantage the mocks do not have: it can use `lte`, `gte`, `in`
and choose thresholds.

**The frontier is NOT a region to beat.** It was in the original specification;
the ceiling verification (Step 0) invalidated it as a reference, and the
threshold that used to be set here is withdrawn:

- **The mocks are structurally immune to the engine's defect.** All the rules of
  `keep_k(k)` have exactly k conditions. With uniform specificity, arbitration
  can never invert priorities, and the tie-break falls to `born_at`, which is the
  correct semantics. The hidden policy, by contrast, mixes rules of 1 to 3
  conditions in which the *less* specific rule usually has *more* priority —
  exactly the case arbitration resolves backwards.
- **`keep_k(k=4)` scores better than the true policy under this engine:** 0.173
  silent error versus 0.214, and 0.780 end-to-end accuracy versus 0.588. A crude
  grid beats the oracle, and not by being a better policy: by not suffering the
  priority inversions arbitration imposes.

That is: the "region to beat" was **above the ceiling of the system itself**.
Measuring against it would have measured the mock's immunity to the defect, not
the proposer's inductive capacity. No new threshold is set until Step 0 gives
~100%.

The `frontier` figures remain reproducible and serve to check that nothing got
corrupted in copying. They are not usable as a quality reference.

Reference: majority class 36.3%. Hidden policy: 29 rules.

---

## Before running `llm`: fill in PREDICTION.md

This is not ceremony. Without a threshold written in advance, any result is
going to look promising.

---

## What was deliberately NOT here in rung 1

Concept drift, regret against the best representable policy, ILP as a
competitor, empirical impasse detectors, partial feedback, ASP, activation,
versioning, rollback.

Of that list, **partial feedback happened**: rung 4 implemented it as a channel
parameterized by coverage, asymmetry, delay and noise. The rest is still
undone, including **ILP as a competitor**, which was specified as Step B of
rung 3 and never run.

(Rung 2 added **declared priority**, which was not on this list because in
rung 1 it had not yet been identified as the missing piece.)

Everything open is in [`IDEAS.md`](IDEAS.md), together with what the four rungs
opened and did not resolve.

---

## Repository structure

The modules use relative imports, so **each package must keep its folder**. If
the files end up flat you will see
`ModuleNotFoundError: No module named 'harness'`.

```
adaptive-triage/
├── run_experiment.py        rung 1 CLI (frontier · llm · models)
├── requirements.txt         `openai` pinned, for the real proposer
├── requirements.lock.txt    transitive closure of the records' environment
├── README.md  CLAUDE.md  IDEAS.md  PREDICTION.md  LICENSE  .gitignore
│
├── harness/                 RUNG 1 — frozen spec and original engine
│   ├── domain.py            case, actions, corpus (seed 17)          [FROZEN]
│   ├── hidden_policy.py     the 29 rules in 8 layers · the ORACLE    [FROZEN]
│   ├── dsl.py               rule schema and RuleEngine               [FROZEN]
│   ├── shadow.py            shadow loop and metrics                  [FROZEN]
│   ├── cache_baseline.py    semantic cache baseline                  [FROZEN]
│   ├── proposers.py         keep_k/random_k mocks and LLM proposers
│   ├── provenance.py        the `_env` block attached to every JSON
│   ├── ceiling_check.py     STEP 0 · ceiling of the specificity engine
│   ├── subsumption_check.py partial order by semantic subsumption
│   └── learned_subsumption.py  the same criterion over the learned base
│
├── peldano2/                hybrid engine: subsumption + declared priority
│   ├── engine2.py           two-level arbitration
│   ├── hidden_priority.py   the 29 rules with their minimal edges
│   ├── ceiling_check2.py    STEP 0 of rung 2 (gives 100%)
│   ├── proposers2.py        v1/v2 prompts and bounded neighbourhood
│   └── shadow2.py  run2.py  compare_runs.py  note_audit.py
│
├── peldano3/                order by search over the corpus, no LLM
│   ├── order_search.py      coverage bound, greedy search, split
│   └── budget_and_balance.py  label budget and balanced greedy
│
├── peldano4/                priority learned from a feedback channel
│   ├── feedback.py          the channel; the only one that consults the oracle
│   └── sweep.py             coverage, asymmetry, delay and noise sweeps
│
├── tests/                   249 tests · `python3 -m unittest discover`
│   ├── fixtures.py          corpus and exhaustive space, built once
│   ├── doubles.py           the recorded SDK client: the LLM path without paying
│   ├── hashseed_child.py    child process for the `PYTHONHASHSEED` control
│   └── test_*.py            invariants and snapshots (see *The tests*)
│
├── .githooks/pre-commit     the suite before every commit (must be enabled)
├── .github/workflows/       the suite on every push and PR, on 3.10 and 3.12
├── .github/dependabot.yml   bumps the actions; does NOT touch the pip pins
│
└── results/  results2/  results3/  results4/
    The records. FINDINGS*.md are the conclusions with their dated
    errata; the .json files are the raw data, for post-hoc slicing
    without paying for any run again. They are versioned on purpose:
    they are the product of the experiment, not transient output.
```

**`.venv/` is in `.gitignore`** and is rebuilt entirely from
`requirements.txt`. Do not version it: the first commit did, and the history had
to be purged.

The five files marked `[FROZEN]` define the experiment. If you think one of them
has a bug, **stop and say so**; do not fix it on your own. See the hard rules in
[`CLAUDE.md`](CLAUDE.md).
