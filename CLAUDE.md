# Context for Claude Code

## What this project is

An experiment on **adaptive policy compilation**: a cheap symbolic engine
resolves the cases it covers; when it fails to cover one (an impasse), an LLM
acts and writes a new rule so that next time it does cover it.

**Four rungs are closed, and none of their figures are in this file.** What is
established, on which surface it was measured, what was withdrawn and why, and
what is open: `STATUS.md`. Each figure it indexes belongs to a FINDINGS record
that owns it and carries its dated errata in place. **Read `STATUS.md` before
proposing anything, and read the erratum before citing any number.**

**No figure belongs in this file, and none is to be added.** This one is loaded
into every session and framed as authority, so a number written here is taken as
fact by a reader who has no reason to click through to the record — and when the
record is corrected by an erratum, the copy here goes stale in silence, with no
test able to catch it. A figure has exactly two homes: the FINDINGS that owns it
and `STATUS.md`, which indexes it. What this file carries instead is the hard
rules, the operating procedure and the mandatory stops.

**The rest of this file describes the operating procedure of rung 1**, which
remains valid as a procedure but **not** as the status of the project.

Read `README.md` before touching anything. `IDEAS.md` keeps the list of what is
open.

**The operating procedure of rungs 2, 3 and 4 is not in this file**, which only
describes that of rung 1. It is in the README, section "Reproducing the four
rungs". Everything in those three rungs costs zero API calls and runs on the
standard library:

    python3 -m peldano2.ceiling_check2      # hybrid engine ceiling
    python3 -m peldano3.order_search        # coverage bound and searched order
    python3 -m peldano4.sweep               # feedback-channel sweeps

The optimizer audit of August 8, 2026 adds four more, also free. The first is
blocking in the same sense as `harness.ceiling_check`: it measures the
instrument before the instrument measures anything else.

    python3 -m peldano3.optimizer_check     # optimizer ceiling: must give 1.0000
    python3 -m peldano3.order_search_ls     # rung 3 with the declared optimizer
    python3 -m peldano4.sweep_ls            # rung 4 with the declared optimizer
    python3 -m peldano3.order_search_ls --full-space-search

The last three are long runs, because the multi-start repeats the search many
times per instance; the README's reproduction block gives their durations before
you launch one. The four originals are left in place and unmodified, so the
pre-audit figures stay reproducible next to the corrected ones.

The scripts still print their output in Spanish; when a block below shows an
expected result, compare the **numbers**.

---

## HARD RULES — non-negotiable

**1. DO NOT modify the frozen specification** without explicit authorization:

    harness/hidden_policy.py    harness/domain.py       harness/dsl.py
    harness/shadow.py           harness/cache_baseline.py

If you think one of them has a bug, **stop and say so**; do not fix it on your
own.

DEFECT RECORDED IN `dsl.py`, ALREADY SUPERSEDED: `RuleEngine.decide` arbitrates
by specificity and returns CONFLICT before applying the age tie-break, which is
left unreachable precisely when it would matter.

**The redesign has already been done, in rung 2**, as a separate package
(`peldano2/engine2.py`: subsumption as the base order + declared priority), and
it executes the perfect policy without error — the figure is in `STATUS.md`. It
was done outside `harness/` precisely so that `dsl.py` would stay frozen.

So `dsl.py` **is still not to be touched**, but for the opposite reason to the
one this note used to give: not because there is work pending there, but because
it is the closed record of rung 1 and its figures must keep reproducing.

**2. DO NOT fill in `PREDICTION.md`.** Sergi fills it in, by hand, before the
long run. A model writing the prediction destroys the purpose of the file. If it
is empty when the long run comes up, **stop and ask for it**.

**A SIGNED PLAN TRAVELS ALONE.** `PREDICTION.md` and any `PLAN_*.md` at the root
go in **their own commit, with their own message**, never staged alongside
anything else. Stage them by name; `git add -A` with one of them edited in the
working tree is how this gets broken. Committing them is not the problem —
committing them accompanied is, because a signature that shares a commit with a
diagnostic is filed under the diagnostic and stops being findable in the log.
That is not hypothetical: on August 13, 2026 Sergi's signature of §0 of
`PLAN_BUDGET_LS.md` arrived inside `b9b0f5f`, a commit about the start-budget
diagnostic whose message never mentions it. Nothing was altered; the act simply
became unauditable from the file's own history.

Since August 14, 2026 `.githooks/pre-commit` refuses that commit. **The guard
does not make this rule safe**: it runs pre-commit and `--no-verify` skips it
whole, which is enough against a wildcard in a hurry and nothing at all against
an agent that reads a rejection and reaches for the flag. Making it binding would
take a server-side hook or a check in CI, disproportionate for a failure that has
happened once and altered nothing. The rule is yours to keep; the guard only
catches the careless version. Only the root counts — `docs/PLAN_x.md` is
documentation about a plan, not a signed one.

**3. DO NOT parallelize the loop.** It is strictly sequential: each new rule
changes whether the next case escalates or not. Concurrency = broken semantics.

**4. DO NOT change the seed (17) or regenerate the corpus.** Determinism is what
makes runs comparable.

For the same reason, **DO NOT overwrite `results/llm_run.json`**. It is not just
the record of rung 1: it is the learned rule base that **rungs 3 and 4 start
from**, and since the proposer is not deterministic at temperature 0, what comes
out will not be the same. If it has to be re-run, the original is saved first
under another name.

Since August 8, 2026 the rule is also enforced by the code, in
`harness/record_guard.py`: `run_experiment.py llm` no longer writes that path —
it writes `results/llm_run_n<N>.json`, so `--n 100` and `--n 2000` no longer
share a file — and if the destination is occupied it aborts before spending a
call, saying what would be lost. The escape hatches are `--out` and
`--overwrite-record`. The same guard covers `peldano2/run2.py`. **The guard is
not authorization**: the norm above still holds, and the flag is not typed
without Sergi asking for it.

**5. DO NOT adjust the prompt or the schema before having a recorded result.**
First you measure, then you iterate.

**6. If the numbers come out badly, DO NOT fix them: report them.** A negative
result is a result. Adjusting until the curve looks nice is exactly the Goodhart
failure this experiment studies; do not reproduce it.

**7. The API key goes in the environment, never in a file in the repo.**
`OPENROUTER_API_KEY` is managed by Sergi. Do not write it, do not read it aloud,
do not store it.

HOW IT ARRIVES, IN PRACTICE — this is recorded because it takes a long detour to
find out. An `export` in Sergi's interactive terminal does **not** reach your
shell: they are different processes. And even though he has it in `~/.bashrc`,
the Debian guard on lines 5-9 of that file does `return` for non-interactive
shells, so his `export` never runs in yours.

What does work, loading it into the process environment without ever printing
it:

    eval "$(grep -m1 '^export OPENROUTER_API_KEY=' ~/.bashrc)"

Check with `${#OPENROUTER_API_KEY}` (the length), never with its value.

---

## Sequence, with mandatory stops

### Preliminary step — The test suite (zero API calls, seconds)

    python3 -m unittest discover

It runs on the standard library and does not write to `results*/`: it calls the
measurement functions, never the `main()`s. It pins the invariants (the DSL
reproduces the lambdas over the whole case space) and the published ceilings,
the frontier and the corpus, watches that no component of the online loop
imports the oracle, and replays the recorded LLM runs — `results/llm_run.json`
and `results2/llm_run2_n100.json` — rule by rule and record by record, without
spending a cent.

The tests added on August 8, 2026 cover the audit's optimizer. They pin that it is
an instrument rather than a figure: that `best_insertion` equals brute force over
every position, that the search really is at a local optimum of its neighbourhood
when it stops, that the mask-based greedy reproduces `order_search.greedy_order`
exactly — so a gain is measured against the record's baseline and not a different
one — and that knowing the optimum cannot leak into the search. **No accuracy
figure from the learned base is pinned there**: the audit's numbers live in the
FINDINGS errata and in `results3/`, and duplicating them in a test would create a
second official figure. The multi-start is also signed across three
`PYTHONHASHSEED` values in `tests/hashseed_child.py`, because the same-process
determinism test is the one that returned a false zero in rung 4.

If something fails here, stop: Steps 0 and 1 would be measuring over a harness
that no longer reproduces. **A failing snapshot is not updated**; you find out
what changed and, if the change is legitimate, you date the erratum in the
FINDINGS that publishes the figure.

**You do not have to remember to launch it.** The `.githooks/pre-commit` hook
runs it before every commit (enable it once with `git config core.hooksPath
.githooks`) and `.github/workflows/pruebas.yml` on every push. If the hook
aborts a commit, `--no-verify` is **not** the default answer: see the previous
paragraph.

The hook now aborts for a second reason, before running anything: a signed plan
staged with company (hard rule 2). There the answer is not `--no-verify` either
— it is to split the commit, which is the whole point of the rejection.

### Step 0 — Engine ceiling (MANDATORY before any LLM run)

    python3 -m harness.ceiling_check

Loads the true hidden policy into the engine and measures its accuracy with no
LLM involved. If the engine cannot execute the correct policy, no measurement
over learned rules means anything.

It costs zero API calls. It is run BEFORE spending a cent, and re-run after ANY
change to the DSL, to the arbitration or to the hidden policy.

**The ceiling measured on Aug 5, 2026 is far below ~100%** — the figure, with
its surface, is in `STATUS.md`, and the record that owns it is
`results/FINDINGS.md`. Specificity-based arbitration cannot execute a policy
prioritized by layers. While it stays there, every LLM run is voided in advance.

**STOP 0.** If the ceiling is not ~100%, stop and say so. Do not go on to
Step 1.

### Step 1 — Dry-run verification

    python3 run_experiment.py frontier

**The result must reproduce the record exactly** (seed 17, n=2000): compare it
against `results/frontier.json`, which `tests/test_frontier.py` pins row by row —
so the preliminary step already checks this without anyone reading a terminal. If
it does not match, something got corrupted in copying: stop and warn.

WARNING: those figures are still reproducible, but they are NOT a valid
reference while the Step 0 ceiling is not ~100%. All keep_k rules have exactly k
conditions, so their specificity is uniform and arbitration can never invert
priorities: the mocks are structurally immune to the defect that destroys the
real policy. In fact keep_k(k=4) scores BETTER than the true policy under this
engine — the comparison is in `results/FINDINGS.md`, route 1. The "region to
beat" is above the system's ceiling.

**STOP 1.** Report whether it matches.

### Step 2 — Dependencies

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt

Only `openai`, pinned in `requirements.txt` (OpenRouter is OpenAI-compatible). To
rebuild the records' environment to the digit, install `requirements.lock.txt`
instead: it carries the full transitive closure.

**The venv is not optional**: on Debian/Ubuntu a global `pip install` fails with
`externally-managed-environment` (PEP 668). The preliminary step and Steps 0 and
1 do not need it — they run on the standard library; from Step 3 onwards, they
do.

Verify that `OPENROUTER_API_KEY` reaches the process environment (see rule 7);
if not, ask Sergi for it — do not manage it yourself.

### Step 3 — Smoke test

    .venv/bin/python run_experiment.py llm --n 100

Costs cents. **Do not judge reuse here**: with 100 cases almost no rule has the
chance to fire twice. This run serves three purposes:

- checking that parsing works (`failed_proposals` and `rejected_rules` low)
- **reading 5-8 rules from `results/llm_run.json` with their `note` field**
- seeing whether the model uses `lte`/`gte`/`in` or only `eq`

WARNING: the model is NOT deterministic at temperature 0. Verified Aug 5, 2026 —
same prompt, same case, same seed, different rules between the run of 100 and
the run of 2000. The smoke test is not a prefix of the full run. This affects any
comparison between models: the model will not be the only variable unless
several sampling seeds are averaged.

**STOP 2.** Paste the rules you read and say whether the model seems to be
inducing structure or transcribing tickets. Wait for an answer before going on.

### Step 4 — Full run

Only if Step 0 gave ~100%, `PREDICTION.md` is filled in and Sergi approves it.

    .venv/bin/python run_experiment.py llm --n 2000

Sequential: count on minutes. Costs cents with `deepseek/deepseek-v4-flash`.

**Before launching it, re-read rule 4.** Since August 8, 2026 this command
writes `results/llm_run_n2000.json` and no longer touches `results/llm_run.json`,
which is the input of rungs 3 and 4; if the destination is already there it
aborts without spending anything.

### Step 5 — Reading

`results/llm_run.json` stores the raw per-case records: slices by class, by rule
or by decile are done **post-hoc, without paying for the run again**.

Memorization floor: `keep_k(k=8)` reaches a reuse rate without inducing
anything, pure effect of the corpus duplicates. Any figure close to it is noise,
not learning — the value is in `STATUS.md`, "What this does not show".

Always separate the two error axes and do not mix them:
`proposal_action_accuracy` measures choosing the wrong queue when proposing; the
silent error measures scope. The mocks get the correct action for free and the
LLM does not.

Pay particular attention to `ONCALL_ESCALATION` and `SECURITY_INCIDENT`. They
are the most critical classes and the rarest — a handful of cases each in 2000 —
so the aggregate hides them. In the voided run, compilation destroyed capability:
SECURITY_INCIDENT was resolved correctly when the case reached the LLM and never
when a compiled rule resolved it. The counts are in `STATUS.md` and in
`PREDICTION.md`.

---

## Current status

**It is in `STATUS.md`**, and it is not restated here: what is established and on
which surface, what was withdrawn and why, and what is open, each figure pointing
at the FINDINGS record that owns it. `IDEAS.md` keeps the parking lot. What
belongs in this file is only what constrains the work, which is the rest of this
section.

### What is still forbidden and what was lifted

DO NOT re-run rung 1 with another syntactic arbitration: it will fail for the
reasons recorded in `results/FINDINGS.md`, where the three routes are falsified
one by one.

**Lifted on August 6, 2026, when rung 2 was opened:** the ban on proposing
redesigns and the exception about `dsl.py`. Sergi lifted them explicitly for that
work. Do not reinstate them on your own, nor assume they are in force; **the
scope of each opening is set by Sergi when he opens it**, and until then the norm
remains not to propose unrequested redesigns.

**The optimizer's constants are not yours to tune.** `MULTISTART_SEED = 17`,
`MULTISTART_STARTS = 64` and `DECLARED_NEIGHBOURHOOD = "move+swap"` in
`peldano3/local_search.py` were fixed before the runs that used them, and the
reasoning for the neighbourhood is recorded next to it. Changing any of them
after seeing a result is rule 6 under another name. The instrument was changed
once, on August 8, 2026, and only because Step 0 showed it failing against a
policy whose optimum is known independently of any of these numbers — that is
what made it legitimate, and it is the only thing that would make it legitimate
again.

**On which surface a figure is measured**, see `STATUS.md`, "Before reading any
figure". Rungs 1 to 4 published corpus figures without labelling them. Do not
continue that: name the surface, and where both are available report both.

What is pending and open is in `IDEAS.md`, including what each rung left
unresolved. Of the original list only the empirical impasse has been touched —
partially, in rung 4 —; concept drift, regret, ILP as a competitor, ASP and real
activation are still undone.
