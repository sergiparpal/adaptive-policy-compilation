# Context for Claude Code

## What this project is

An experiment on **adaptive policy compilation**: a cheap symbolic engine
resolves the cases it covers; when it fails to cover one (an impasse), an LLM
acts and writes a new rule so that next time it does cover it.

**Four rungs and two further threads are closed, and none of their figures are in
this file.** What is established, on which surface it was measured, what was
withdrawn and why, and what is open: `STATUS.md`. Each figure it indexes belongs
to a FINDINGS record that owns it and carries its dated errata in place. **Read
`STATUS.md` before proposing anything, and read the erratum before citing any
number.**

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

**Before writing a new analytical document, read the three that already exist.**
`ARBITRATION_REPORT.md` — which rule wins when several match and disagree —
`CHAT_SUMMARY.md` — the conversation of August 11, 2026, with the errata it has
issued against itself since — and `EXTERNAL_REVIEW.md` — the 2026-08-29 reading
from outside the project, adjudicated against the code, with the plan that came
out of it. None owns a figure, all carry their errata in place, and the record
wins wherever one disagrees with it. §9.8 of the first records that it re-derived
three of the second's corrections by another route without knowing them; §4, rule
C of `PLAN_PAIRWISE.md` makes reading them a step and not a suggestion. **It has
now happened twice** — §1.4 of the third restates a limit §9.1 of the first
already carried — so **do not make it a fourth time.** They are indexed nowhere
but the README's structure tree and the section *Three documents that read the
records instead of adding to them*, which is why the pointer is here.

**The operating procedure of rungs 2, 3 and 4 is not in this file**, which only
describes that of rung 1. It is in the README, section "Reproducing the four
rungs". Everything in those three rungs costs zero API calls and runs on the
standard library:

    python3 -m rung2.ceiling_check2      # hybrid engine ceiling
    python3 -m rung2.ceiling_check2_space  # the same, on the exhaustive space
    python3 -m rung3.order_search        # coverage bound and searched order
    python3 -m rung4.sweep               # feedback-channel sweeps

The optimizer audit of August 8, 2026 adds four more, also free. The first is
blocking in the same sense as `harness.ceiling_check`: it measures the
instrument before the instrument measures anything else.

    python3 -m rung3.optimizer_check     # optimizer ceiling: must give 1.0000
    python3 -m rung3.order_search_ls     # rung 3 with the declared optimizer
    python3 -m rung4.sweep_ls            # rung 4 with the declared optimizer
    python3 -m rung3.order_search_ls --full-space-search

**The pairwise-judgement thread of `PLAN_PAIRWISE.md` closed on August 24, 2026**
with three signed rows adjudicated. Its procedure is the plan itself; its
write-ups are `results2/FINDINGS2.md` (Stages C and D) and `results3/FINDINGS3.md`
§§6-10. **`PAIRWISE_WRITEUP.md` presents that thread and the next one as a single
result** — it owns no figure and is not one of the three analytical documents
above; it is what those fifteen sections say when read together. Almost all of it
is free:

    python3 -m rung3.floor_by_pool          # blocking six-row reproduction gate
    python3 -m rung2.pair_benchmark         # the labelled pairs and witnesses
    python3 -m rung3.queue_hierarchy_floor  # what a queue ranking alone scores
    python3 -m rung2.pair_judgement_baselines
    python3 -m rung3.declared_order         # the three scorings and the control
    python3 -m rung3.edge_direction
    python3 -m rung3.edge_budget

**A second thread, `PLAN_PROPOSER_1600.md`, closed on August 26, 2026** with four
more signed rows — the first of the two that were signed *before* the calls rather
than written after them. Its write-up is `results3/FINDINGS3.md` §11, which also
carries a dated erratum to §10. Its scoring is free and reads answers already paid
for:

    python3 -m rung2.pair_sample_1600       # the nested 1,600-pair sample, gated
    python3 -m rung3.edge_direction --source results2/pair_judgement_1600.json \
        --out results3/edge_direction_1600.json --split results2/pair_sample_1600.json
    python3 -m rung3.declared_order --source results2/pair_judgement_1600.json \
        --out results3/declared_order_1600.json --split results2/pair_sample_1600.json \
        --accuracy results3/edge_direction_1600.json

**The sensitivity sweep of `PLAN_SENSITIVITY.md` closed on August 29, 2026** with
five signed rows adjudicated — the first pre-registered work outside the pairwise
threads. Its record is `results_sensitivity/FINDINGS_SENSITIVITY.md`. Free, two
minutes, and the first command is blocking in the same sense as
`harness.ceiling_check`: it killed the plan's original family design before any
row was read, which is why §1 of that plan carries a signed amendment.

    python3 -m sensitivity.generator_check   # A-g1..A-g4; must pass first
    python3 -m sensitivity.sweep             # refuses to write while unsigned

**That gate counts signatures rather than stopping at the first.** The plan has
two — §0's table and §1's amendment — and a gate that read only the first would
find §0 signed and report `ok` over an unsigned §1. Do not copy
`gate_signature` from `rung2/pair_judgement.py` into a plan with more than one.

**ILP as a competitor closed on August 30, 2026**, opened by Sergi and
pre-registered as `PLAN_ILP.md`. Four signed rows; its record is
`results_ilp/FINDINGS_ILP.md`. Free, seconds, and the first command is blocking:
it killed the search method the plan itself declared, which is why §1 of that plan
carries a signed amendment.

    python3 -m ilp.induce_check   # I-g1..I-g4; must pass first
    python3 -m ilp.compare        # refuses to write while unsigned
    python3 -m ilp.labels         # POST-HOC: who had the labels (FINDINGS_ILP §5)
    python3 -m ilp.margin         # POST-RUN: where the +0.0342 comes from (§1)
    python3 -m ilp.chosen         # POST-RUN: the inducer on the proposer's queues

**`requirements-ilp.txt` is not `requirements.txt` and must not be merged into
it.** That file is the environment the paid records were produced with. The
inducer runs on the standard library; `clingo` is pinned separately and is needed
only to reproduce the encoding `I-g1` rejected.

**Three follow-ups closed that thread's remaining routes**, §§12-14 of the same
record, all free and all POST-RUN — they carry expectations but no signed row, so
none of them is on `STATUS.md`'s scoreboard:

    python3 -m rung3.edge_sides         # what each side of the split BUYS
    python3 -m rung3.mfas_compilation   # the answers, or the compilation?
    python3 -m rung3.edge_dropping      # does deliberate dropping beat chance
    python3 -m rung3.answer_asymmetry   # why it names rule_b more often (§15)
    python3 -m rung3.filter_headroom    # what §14's instrument could show (§16)
    python3 -m rung3.filter_space       # §16's cuts over the space (§17)
    python3 -m rung3.identical_rules    # rules written twice (§18)

**§16 qualifies §14.** It measures what a perfect, oracle-chosen selection of the
same edges scores against chance on §14's cell, and it barely moves the order. So
§14's *nothing chooses better than chance* means the selection was untestable at
this budget, not ruled out. Read §16 before citing §14 as an elimination.

**§17 qualifies §16 in turn.** Over the space, §16's one lead, dropping the
edges whose stated reason is a queue's importance, reverses, and moves the order
further than any selection moved it on the corpus: those are the edges that
name `SECURITY_INCIDENT` the winner. And §16's oracle is the best selection *by
direction*, not the best selection: over the space truth-free cuts land on both
sides of the band it draws. Read §17 before citing §16's lead or its ceiling.

**§14 narrows a signed row without moving it.** `B-b` was signed against a free
queue ranking's 0.4824, and §14 measures that a *perfect* follower of that ranking
scores about 0.44 at this budget, because 1,600 pairs is 4.6% of the 31,850 that
could carry an edge. The row stays refuted exactly as signed; what it means is
narrower than it reads, and `STATUS.md` says so beside the row rather than only in
the FINDINGS.

**The exception is `rung2/pair_judgement.py`, which spends** — and since
2026-09-29 so does `reuse/run.py`, since 2026-10-02 `fidelity/ask.py`, since
2026-10-05 `authorship/run.py`, and since 2026-10-06 `overlap/run.py`, all four
below. It refuses to run while §0 of **the
plan that governs the run** is
unsigned — `PLAN_PAIRWISE.md` for Stage D, `PLAN_PROPOSER_1600.md` for a
`--sample` run — a gate that stops before the client is even constructed, with no
flag that skips it, and `--dry-run` builds every question, runs every gate and
spends nothing. **The plan is an argument because there is more than one**: until
2026-08-25 the gate read `PLAN_PAIRWISE.md` whatever it was gating, so a 1,600-pair
run would have found that closed thread's signature, reported `ok`, and spent
1,200 calls on rows nobody had signed. A gate that reads the wrong file is worse
than no gate, because it is believed.

Do not remove that gate and do not sign any plan: hard rule 2 below, and §0 of
each plan restates it. A model may draft a band and may not sign it.

**`PLAN_REUSE.md` closed on 2026-09-30: the founding question, on rung 2's
engine.** Six signed rows: five adjudicated, one reported. Sergi signed §0 on
2026-09-29 and an amendment to §1 on 2026-09-30, each before any figure it
governs existed. The amendment says the proposer's calls do not reason: the hosted
model now reasons by default and spends the answer's budget on it. The record is
`results_reuse/FINDINGS_REUSE.md`, and `STATUS.md` indexes its figures. **Stages A
and C are free and reproduce from the committed records. Stage B spent**: its
records are guarded, and a re-run neither overwrites them nor gives the same draws
back, so a paid run does not start without Sergi asking for it. The first command
is blocking and writes nothing. Every writer in `reuse/` refuses while the plan
carries a blank signature line; the gate reads `PLAN_REUSE.md` and no other plan,
counts every such line, and requires both signatures:

    python3 -m reuse.run --dry-run            # U-g1..U-g4; must pass first
    python3 -m reuse.readout                  # Stage A, free
    python3 -m reuse.score                    # Stage C, free, from the runs
    python3 -m reuse.structure                # POST-RUN: the bases, read for Stage E
    .venv/bin/python -m reuse.run --smoke     # Stage B: spends — only if asked
    .venv/bin/python -m reuse.run --rep 1     # then 2, then 3 — never side by side

The last three are long runs, because the multi-start repeats the search many
times per instance; the README's reproduction block gives their durations before
you launch one. The four originals are left in place and unmodified, so the
pre-audit figures stay reproducible next to the corrected ones.

**`PLAN_FIDELITY.md` closed on 2026-10-04: the founding question in its cleanest
form.** Six signed rows: five adjudicated, one reported. Sergi signed §0 on
2026-10-02, before any figure it governs existed. It asked whether a compiled
rule decides a later case the way the model would have. It re-asked the model,
under prompt v1 and with reasoning off, on prompts rebuilt from
`PLAN_REUSE.md`'s Stage B records, with every rule that matches the ticket hidden.
The record is `results_fidelity/FINDINGS_FIDELITY.md`, and `STATUS.md` indexes
its figures. **Stages A and C are free and reproduce from the committed records.
Stage B spent**: its records are guarded, and a re-run neither overwrites them
nor gives the same answers back, so a paid session does not start without Sergi
asking for it. Every writer in `fidelity/` refuses while the plan carries a blank
signature line; the gate reads `PLAN_FIDELITY.md` and no other plan and counts
every such line. The first command is blocking and writes nothing:

    python3 -m fidelity.ask --dry-run                   # F-g1..F-g4; must pass first
    python3 -m fidelity.sample                          # Stage A, free
    python3 -m fidelity.score                           # Stage C, free, from the sessions
    .venv/bin/python -m fidelity.ask --session smoke    # Stage B: spends — only if asked
    .venv/bin/python -m fidelity.ask --session births   # then base1, base2, base3, ticket_only

**A session that dies keeps what it paid for.** Answers are appended to a
git-ignored partial file, and the same command resumes there. A run of failed
calls stops a session without recording them, because an outage is not answers.
**A session longer than about half an hour outlives a background command of the
agent's harness**, which ends it at that limit. Run long sessions in Sergi's
terminal, with the key loaded as rule 7 says.

**`PLAN_EDGES.md` closed on 2026-10-05: what the edges the proposer declared at
write time bought.** Four signed rows: three adjudicated, one reported. Sergi
signed §0 on 2026-10-05, before any figure it governs existed. It scored the
edges `PLAN_REUSE.md`'s engine installed in Stage B: on the cases they decided,
against a coin over their directions, and over the function. The record is
`results_edges/FINDINGS_EDGES.md`, and `STATUS.md` indexes its figures.
**Everything in it is free** and reproduces from the committed records. Both
writers in `edges/` refuse while the plan carries a blank signature line, and
the gate reads `PLAN_EDGES.md` and no other plan. The first command is blocking
and writes nothing:

    python3 -m edges.score --dry-run   # W-g1..W-g4; must pass first
    python3 -m edges.score             # the census, W-a to W-c, W-d
    python3 -m edges.readings          # POST-RUN readings of the stage's record

**Its `W-c` counts right decisions, and that rewards resolving.** A flipped edge
leaves its conflict open instead of handing it to the other rule, so a coin
decides fewer cases, not worse ones. The record says so beside the verdict. A
coin control over declared edges should compare accuracy among the cases each
arm resolves. Do not copy that statistic.

**`PLAN_PRIMACY.md` closed on 2026-10-05: where the presentation slot decides
the pairwise answers.** Three signed rows: two adjudicated, one reported. Sergi
signed §0 on 2026-10-05, before any figure it governs existed. It read the
answers `PLAN_PROPOSER_1600.md` paid for, with the truth per pair, after checking
that every slot was the seeded deal. The record is
`results_primacy/FINDINGS_PRIMACY.md`, and `STATUS.md` indexes its figures.
**Everything in it is free** and reproduces from the committed records. Its one
writer refuses while the plan carries a blank signature line, and the gate reads
`PLAN_PRIMACY.md` and no other plan. The first command is blocking and writes
nothing:

    python3 -m primacy.score --dry-run   # L-g1..L-g4; must pass first
    python3 -m primacy.score             # L-a, L-b, the readings of L-c

**In those answers, position, label and the order of the queue names are one
variable.** The rule listed first is always labelled `A`, and its queue is named
first. No reading of them can say why the slot decides, only where, and every
share it reports is a floor. **And its `L-a` chose where to look by an aggregate
split, and the effect was elsewhere.** A plan that looks for a position effect
should select by something that bears on each pair. Do not copy that selection.

**`PLAN_WHY.md` closed on 2026-10-05: what the proposer says it is doing,
against what it does.** Five signed rows: four adjudicated, one reported. Sergi
signed §0 on 2026-10-05, before any held-out sentence was coded. It coded the
sentence the proposer wrote beside each pairwise answer, with a codebook frozen
on a development set, and read the batch answered the next day. The record is
`results_why/FINDINGS_WHY.md`, and `STATUS.md` indexes its figures. **Everything
in it is free** and reproduces from the committed records. Its one writer refuses
while the plan carries a blank signature line, and the gate reads `PLAN_WHY.md`
and no other plan. The first command is blocking and writes nothing:

    python3 -m why.score --dry-run   # Y-g1..Y-g4; must pass first
    python3 -m why.score             # Y-a to Y-d, the readings of Y-e

**Its bands were set on a development set, so its holds say a reading
generalises, not that the drafter foresaw anything.** The scoreboard marks the
row so and gives the ratios without it. A plan built the same way should say so
in its §0, as this one did. **And anchor a codebook's patterns**:
`m[aá]s condiciones` matched inside *"mismas condiciones"*.

**`PLAN_AUTHORSHIP.md` closed on 2026-10-06: Stage E, declaration imposed at
write time.** Five signed rows: three adjudicated, one reported, and one signed
and not adjudicated. Sergi signed §0 on 2026-10-05, before any figure it governs
existed. It ran `PLAN_REUSE.md`'s loop under a protocol that refuses a rule
overlapping another until the proposer declares it an exception to it or a
default under it. The record is `results_authorship/FINDINGS_AUTHORSHIP.md`, and
`STATUS.md` indexes its figures. **Stage C is free and reproduces from the
committed records. Stage B spent**: its records are guarded, and a re-run
neither overwrites them nor gives the same rules back, so a paid run does not
start without Sergi asking for it. Both writers in `authorship/` refuse while
the plan carries a blank signature line, and the gate reads `PLAN_AUTHORSHIP.md`
and no other plan. The first command is blocking and writes nothing:

    python3 -m authorship.run --dry-run            # E-g1..E-g4; must pass first
    PYTHONHASHSEED=0 python3 -m authorship.score   # Stage C, free, from the runs
    PYTHONHASHSEED=0 python3 -m authorship.refused # POST-RUN: the refused declarations
    .venv/bin/python -m authorship.run --smoke     # Stage B: spends — only if asked
    .venv/bin/python -m authorship.run --rep 1     # then 2, then 3 — never side by side

**Its `E-c` was decided by the scorer, not by §0.** The proposer met the
discipline by not overlapping, and one run left the order no room. §0 said only
that such a run has no share. What one such run does to a median of three was
settled in `authorship/score.py`, before the signature, and under any other
reading of that median the row would hold. A plan that adjudicates a median of
a statistic a run can leave undefined should settle that in §0 itself. **And a
plan that charges a proposer for overlapping should expect it to stop.**

**`PLAN_OVERLAP.md` closed on 2026-10-07: Stage E asked again, with the proposer
told to overlap.** Four signed rows: three adjudicated, one reported. Sergi
signed §0 on 2026-10-06, before any figure it governs existed. It ran
`PLAN_REUSE.md`'s loop under v2e: rung 2's v2, which tells the proposer that
overlap is normal, with `PLAN_AUTHORSHIP.md`'s discipline asked only where the
queues differ. The record is `results_overlap/FINDINGS_OVERLAP.md`, and
`STATUS.md` indexes its figures. **Stage C is free and reproduces from the
committed records. Stage B spent**: its records are guarded, and a re-run
neither overwrites them nor gives the same rules back, so a paid run does not
start without Sergi asking for it. Both writers in `overlap/` refuse while the
plan carries a blank signature line, and the gate reads `PLAN_OVERLAP.md` and no
other plan. `authorship/` is called by it and not edited. The first command is
blocking and writes nothing:

    python3 -m overlap.run --dry-run            # O-g1..O-g4; must pass first
    PYTHONHASHSEED=0 python3 -m overlap.score   # Stage C, free, from the runs
    PYTHONHASHSEED=0 python3 -m overlap.readings  # POST-RUN: the run that overlapped
    PYTHONHASHSEED=0 python3 -m overlap.readings_v1  # POST-RUN: the same, over v1
    .venv/bin/python -m overlap.run --smoke     # Stage B: spends — only if asked
    .venv/bin/python -m overlap.run --rep 1     # then 2, then 3 — never side by side

**Its `O-c` holds on one rule of thumb.** Read after the verdicts, nearly all of
its strict pairs are a single declaration about the security keyword, installed
against dozens of rules and counted once per edge. A rate over declared edges
can rest on one declaration: a plan that reads one should say in §0 how it
weighs edges that share a winner. **And §0's rule for a run without room did its
work**: a run had none, and the verdict needed no reading.

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
(`rung2/engine2.py`: subsumption as the base order + declared priority), and
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
`PLAN_BUDGET_LS.md` arrived inside `18d6c7e` (`b9b0f5f` on its branch, before
PR #7's rebase merge), a commit about the start-budget diagnostic whose message
never mentions it. Nothing was altered; the act simply became unauditable from
the file's own history.

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
`--overwrite-record`. The same guard covers `rung2/run2.py` and, since August 24,
2026, `rung2/pair_judgement.py`, whose two records cost 570 calls between them —
and, since 2026-09-29, `reuse/run.py`, since 2026-10-02, `fidelity/ask.py`, since
2026-10-05, `authorship/run.py`, and since 2026-10-06, `overlap/run.py`.
**The guard is not authorization**: the norm above still holds, and the flag is
not typed without Sergi asking for it.

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

**A key that loads and authenticates can still be unable to call a model.**
OpenRouter's *management* keys answer its key endpoint (`/api/v1/key`) with a
200 and read the account's credits, and every completion call refuses them with
`401 — User not found`. That cost two smoke runs of `PLAN_REUSE.md` on
2026-09-30. `reuse/run.py` now asks that endpoint first and refuses a
management key. For any other paid command, read `is_management_key` off the
same endpoint before spending: a 200 alone proves nothing.

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
.githooks`) and `.github/workflows/tests.yml` on every push. If the hook
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

**Part of that ceiling's conflict rate is an encoding artifact, and since
2026-08-29 there is a control that says how much.** The catch-all is
`lambda c: True`, the DSL requires at least one condition, and the engine counts
conditions. `python3 -m harness.default_rule_control` measures the same ceiling
with the catch-all at its true rank, on both surfaces, and makes the published row
a blocking gate so it cannot move quietly. Free, seconds, POST-RUN; the record
that owns its figures is `results/FINDINGS_DEFAULT_RULE.md`. **It does not lift
STOP 0** and it changes nothing above: the corrected ceiling is still nowhere near
~100%.

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
`rung3/local_search.py` were fixed before the runs that used them, and the
reasoning for the neighbourhood is recorded next to it. Changing any of them
after seeing a result is rule 6 under another name. The instrument was changed
once, on August 8, 2026, and only because Step 0 showed it failing against a
policy whose optimum is known independently of any of these numbers — that is
what made it legitimate, and it is the only thing that would make it legitimate
again.

**A signed band is not a constant you may edit.** `P_D_MARGIN` and `P_E_BAND` in
`rung3/declared_order.py` are transcriptions of rows Sergi signed in §0 of
`PLAN_PAIRWISE.md` before any of their figures existed, and a test says so
precisely so that moving one is visible. Both rows came out **refuted**. Nudging
either constant would turn a refutation into a hold by editing a line of Python,
which is hard rule 6 in its purest form. The same goes for the seeds and draw
counts of that thread — `POSITION_SEED`, `SAMPLE_SEED`, `SHUFFLE_SEED`,
`DIRECTION_SEED`, `N_DIRECTION_DRAWS` — all fixed before the runs that used them.

**Two of that thread's records are post-run and say so.** `edge_direction` and
`edge_budget` carry a `provenance` field declaring they were written after P-d
and P-e were adjudicated, by someone who had already seen the result. Nothing in
them is a bet that could have failed. If you add to that thread, keep the field:
a measurement that could not have surprised its author is worth less than one
that could, and the record is where that difference is recorded rather than
assumed.

**On which surface a figure is measured**, see `STATUS.md`, "Before reading any
figure". Rungs 1 to 4 published corpus figures without labelling them. Do not
continue that: name the surface, and where both are available report both. The
pairwise thread adds a third label that is just as load-bearing: **which pool**,
`puro` or `hibrido`. They are different machines and their figures never chain.

What is pending and open is in `IDEAS.md`, including what each rung left
unresolved and what the pairwise thread opened. What rung 1 left out on purpose
is in the README, *What was deliberately NOT here in rung 1*, which says what of
it has been done since. It is not restated here: the copy this paragraph carried
still called ILP as a competitor undone five weeks after `PLAN_ILP.md` closed.
