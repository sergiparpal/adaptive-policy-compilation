# Context for Claude Code

## What this project is

An experiment on **adaptive policy compilation**: a cheap symbolic engine
resolves the cases it covers; when it fails to cover one (an impasse), an LLM
acts and writes a new rule so that next time it does cover it.

**There are four closed rungs.** The rest of this file describes the operating
procedure of rung 1, which remains valid as a procedure but **not** as the
status of the project:

| rung | what it measured | record |
|---|---|---|
| 1 | the specificity engine gives 58.75% with the perfect policy loaded; the run was voided | `results/FINDINGS.md` |
| 2 | hybrid engine (subsumption + declared priority) at 100%, but the proposer writes disjoint rules and does not exercise it | `results2/FINDINGS2.md` |
| 3 | the 577 rules from rung 1 admit an order that scores **0.8530** on corpus test; bound 0.9010 on corpus, 0.8784 over the case space | `results3/FINDINGS3.md` |
| 4 | that order IS partly learned from asymmetric feedback: +0.2011, not the +0.067 first published | `results4/FINDINGS4.md` |

**Every FINDINGS carries dated errata in place.** The optimizer audit of August
8, 2026 (`PLAN_AUDIT.md`) rewrote figures in rungs 3 and 4: the greedy search
was weak, and fixing it moved rung 3's test from 0.7713 to 0.8530 and withdrew
rung 4's "change of regime". The tie-break fix of August 6 was worth +0.0002;
the algorithm was worth +0.0817. **Read the errata before citing any number.**

**Every figure names a surface, and the two are not interchangeable.** The
CORPUS is the modelled arrival distribution — deliberately long-tailed, so
`has_security_keyword` is 3% of arrivals against 50% of the attribute space. The
EXHAUSTIVE SPACE is the uniform measure over all 134,400 combinations. The
corpus answers "what would this achieve in deployment" and cannot certify an
optimum: 2000 draws touch 1743 distinct cases and leave the rest unconstrained,
so an order can be perfect on it and be 0.9455 as a function. The space answers
"is this order the policy" and weights regions the system will almost never see.
Rungs 1 to 4 published corpus figures without saying so. Do not swap one for the
other silently.

**The original hypothesis — do the LLM's rules get reused or does it memorize
cases? — still has not been measured.** Rung 1 was voided by the engine ceiling
and its reuse figure of 0.158 described the arbitration, not the induction.

Read `README.md` before touching anything, and the "Current status" block at the
end of this file before proposing anything. `IDEAS.md` keeps the list of what is
open.

**The operating procedure of rungs 2, 3 and 4 is not in this file**, which only
describes that of rung 1. It is in the README, section "Reproducing the four
rungs". Everything in those three rungs costs zero API calls and runs on the
standard library:

    python3 -m peldano2.ceiling_check2      # hybrid engine ceiling: 100%
    python3 -m peldano3.order_search        # coverage bound and searched order
    python3 -m peldano4.sweep               # feedback-channel sweeps

The optimizer audit of August 8, 2026 adds four more, also free. The first is
blocking in the same sense as `harness.ceiling_check`: it measures the
instrument before the instrument measures anything else.

    python3 -m peldano3.optimizer_check     # optimizer ceiling: must give 1.0000
    python3 -m peldano3.order_search_ls     # rung 3 with the declared optimizer
    python3 -m peldano4.sweep_ls            # rung 4 with the declared optimizer
    python3 -m peldano3.order_search_ls --full-space-search   # ~3.3 h

`order_search_ls` takes ~33 min and `sweep_ls` ~42 min: the multi-start runs 65
searches per instance. The four originals are left in place and unmodified, so
the pre-audit figures stay reproducible next to the corrected ones.

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
it gives 100% with the perfect policy loaded. It was done outside `harness/`
precisely so that `dsl.py` would stay frozen.

So `dsl.py` **is still not to be touched**, but for the opposite reason to the
one this note used to give: not because there is work pending there, but because
it is the closed record of rung 1 and its figures must keep reproducing.

**2. DO NOT fill in `PREDICTION.md`.** Sergi fills it in, by hand, before the
long run. A model writing the prediction destroys the purpose of the file. If it
is empty when the long run comes up, **stop and ask for it**.

**3. DO NOT parallelize the loop.** It is strictly sequential: each new rule
changes whether the next case escalates or not. Concurrency = broken semantics.

**4. DO NOT change the seed (17) or regenerate the corpus.** Determinism is what
makes runs comparable.

For the same reason, **DO NOT overwrite `results/llm_run.json`**. It is not just
the record of rung 1: it is the base of 577 rules that **rungs 3 and 4 start
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

### Preliminary step — The test suite (zero calls, ~12 s)

    python3 -m unittest discover

315 tests on the standard library. They do not write to `results*/`: they call
the measurement functions, never the `main()`s. They pin the invariants (the DSL
reproduces the lambdas over the 134,400 combinations) and the published figures
(0.5875 · 0.6315 · 1.0000, the frontier and the corpus), watch that no component
of the online loop imports the oracle, and replay the recorded LLM runs —
`results/llm_run.json` and `results2/llm_run2_n100.json` — rule by rule and
record by record, without spending a cent.

The 26 added on August 8, 2026 cover the audit's optimizer. They pin that it is
an instrument rather than a figure: that `best_insertion` equals brute force over
every position, that the search really is at a local optimum of its neighbourhood
when it stops, that the mask-based greedy reproduces `order_search.greedy_order`
exactly — so a gain is measured against the record's baseline and not a different
one — and that knowing the optimum cannot leak into the search. **No accuracy
figure from the 577 rules is pinned there**: the audit's numbers live in the
FINDINGS errata and in `results3/`, and duplicating them in a test would create a
second official figure. The multi-start is also signed across three
`PYTHONHASHSEED` values in `tests/hashseed_child.py`, because the same-process
determinism test is the one that returned a false 0.0000 in rung 4.

If something fails here, stop: Steps 0 and 1 would be measuring over a harness
that no longer reproduces. **A failing snapshot is not updated**; you find out
what changed and, if the change is legitimate, you date the erratum in the
FINDINGS that publishes the figure.

**You do not have to remember to launch it.** The `.githooks/pre-commit` hook
runs it before every commit (enable it once with `git config core.hooksPath
.githooks`) and `.github/workflows/pruebas.yml` on every push. If the hook
aborts a commit, `--no-verify` is **not** the default answer: see the previous
paragraph.

### Step 0 — Engine ceiling (MANDATORY before any LLM run)

    python3 -m harness.ceiling_check

Loads the true hidden policy into the engine and measures its accuracy with no
LLM involved. If the engine cannot execute the correct policy, no measurement
over learned rules means anything.

It costs zero API calls. It is run BEFORE spending a cent, and re-run after ANY
change to the DSL, to the arbitration or to the hidden policy.

**Current measured ceiling (Aug 5, 2026): 58.75% accuracy, 25.3% CONFLICT.**
Specificity-based arbitration cannot execute a policy prioritized by layers.
While that number is not ~100%, every LLM run is voided in advance.

**STOP 0.** If the ceiling is not ~100%, stop and say so. Do not go on to
Step 1.

### Step 1 — Dry-run verification

    python3 run_experiment.py frontier

**Expected result, exact** (seed 17, n=2000). If it does not match, something
got corrupted in copying: stop and warn.

    corpus: 2000 cases, 1743 unique, 12.8% duplicates
    keep_k(k=4)   113 rules   reuse 0.796   sil.err 0.173   escal 0.057
    keep_k(k=5)   304 rules   reuse 0.724   sil.err 0.157   escal 0.152
    cache(d<=2)   211         —             sil.err 0.448   escal 0.105

WARNING: these figures are still reproducible, but they are NOT a valid
reference while the Step 0 ceiling is not ~100%. All keep_k rules have exactly k
conditions, so their specificity is uniform and arbitration can never invert
priorities: the mocks are structurally immune to the defect that destroys the
real policy. In fact keep_k(k=4) scores BETTER than the true policy under this
engine (0.173 versus 0.214 silent error). The "region to beat" is above the
system's ceiling.

**STOP 1.** Report whether it matches.

### Step 2 — Dependencies

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt

Only `openai`, pinned to `openai==2.53.0` (OpenRouter is OpenAI-compatible). To
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

Memorization floor: `keep_k(k=8)` gets 0.118 reuse without inducing anything,
pure effect of the corpus duplicates. Any figure close to 0.118 is noise, not
learning.

Always separate the two error axes and do not mix them:
`proposal_action_accuracy` measures choosing the wrong queue when proposing; the
silent error measures scope. The mocks get the correct action for free and the
LLM does not.

Pay particular attention to `ONCALL_ESCALATION` (7 cases out of 2000) and
`SECURITY_INCIDENT` (20). They are the most critical classes and the rarest; the
aggregate hides them. In the voided run, compilation destroyed capability:
SECURITY_INCIDENT gave 3/3 correct when the case reached the LLM and 0/17 when a
compiled rule resolved it.

---

## Current status (August 8, 2026)

Four closed rungs plus an audit of the instrument that measured two of them. The
thread that ties them together: **the priority of a layered policy is not in the
shape of the rules**, and the three ways of supplying it have been measured. Two
fail. The third — learning it from observed behaviour — works better than rung 4
concluded, and the correction came from auditing the optimizer, not from new
data.

**Rung 1 — infer it from the syntax. Fails.** No syntactic criterion recovers
this policy. H01 (2 conditions) must beat H03 (1); H16 (1) must beat H24 (2) —
no monotone function of specificity satisfies both. Arrival-order arbitration
does not work either: same 29 rules, design order 100%, reverse order 12.8%,
random order 49.3% on average over 200 samples. In a learned base the arrival
order runs backwards from the correct one, because the first cases come from the
common distribution and beget default rules, while the exceptions are born late.
The n=2000 run was voided by the engine ceiling; see `PREDICTION.md`.

The DSL is not the culprit: verified exhaustively over the 134,400 combinations
of the case space that the 29 rules in the DSL are equivalent to their lambdas
and that first-match-wins reproduces them exactly. An execution failure, not a
representation failure.

**Rung 2 — have the proposer declare it. The mechanism works; the proposer does
not feed it.** Subsumption plus 199 declared edges execute the policy at 100%.
But with the base in front of it, the overlap arithmetic resolved and an explicit
instruction to overlap, the proposer writes mostly disjoint rules and argues it
as a merit. Eight runs, two conflicts, zero accepted edges.

**Rung 3 — search for it over the corpus. The material did contain it.** The
same 577 rules that arbitration was turning into 0.18 admit an order that scores
**0.8530 on corpus test** with a gap of 0.017. `SECURITY_INCIDENT` and
`ONCALL_ESCALATION` are 100% recoverable and gave 0/17 and 0/7. But the search
uses the oracle.

**Rung 4 — learn it from observed behaviour. Partly, with real feedback.** With
symmetric supervision +0.3273; with the asymmetric kind, which is the only one a
real system produces, **+0.2011** — 61% of it, not the 29% first published. What
survives of rung 4 is that the signal runs out as the system improves, which is a
property of the channel. What does not survive is the change of regime.

**The audit, August 8, 2026.** The greedy search of rungs 3 and 4 was weak, and
three signs had said so: noise improved it, searching over its own test set left
0.12 under the bound, and the tie-break moved it by 0.011. Validating the
replacement against the hidden policy — where the optimum is 1.0000 by
construction — turned out to matter: pairwise swaps, the neighbourhood the plan
specified, cannot solve even the 29-rule instance (0.9356, and 0/65 starts reach
the optimum). Multi-start relocation does. Of the corrections that followed, 63%
of rung 3's gap was search weakness and rung 4's headline was mostly the shape
of a weak learner's failure curve.

Compilation by impasse learns rules, and learns priority from error feedback
better than rung 4 credited — but still short: +0.2011 against a corpus bound of
0.9010 and a space bound of 0.8784. In a stratified policy the structure lives in
the priority, and it is only partly recoverable from behaviour.

**The original hypothesis — do the LLM's rules get reused or does it memorize
cases? — still has not been measured cleanly.**

### What is still forbidden and what was lifted

DO NOT re-run rung 1 with another syntactic arbitration: it will fail for the
reasons above.

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

**On which surface a figure is measured**, see the block at the top of this file.
Rungs 1 to 4 published corpus figures without labelling them. Do not continue
that: name the surface, and where both are available report both.

What is pending and open is in `IDEAS.md`, including what each rung left
unresolved. Of the original list only the empirical impasse has been touched —
partially, in rung 4 —; concept drift, regret, ILP as a competitor, ASP and real
activation are still undone.
