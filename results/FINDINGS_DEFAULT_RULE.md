# The default-rule control — how much of rung 1's 0.5875 is the encoding

Record of August 29, 2026. Item 2 of [`EXTERNAL_REVIEW.md`](../EXTERNAL_REVIEW.md).
Zero API calls, seconds to run, no search and no sampling.

**This record owns three figures**: the corpus row of the control and both rows of
the exhaustive space. The fourth, the published corpus row of the specificity
engine, belongs to [`FINDINGS.md`](FINDINGS.md), route 1, and **does not move** —
it is re-measured here as a blocking gate, through the same two objects that
produced it (`RuleEngine.decide` and `ceiling_check.measure`), before anything
else is printed.

> **PROVENANCE: POST-RUN.** The two corpus rows were run in memory on 2026-08-29
> while `EXTERNAL_REVIEW.md` was being adjudicated, and its §3 prints them under
> the warning that they were owned by nothing and produced by no module in the
> tree. This closes that. **Nothing here is a bet that could have failed**:
> whoever wrote the module had already seen 0.6880, so no band could honestly be
> drafted around it (hard rule 6), it enters no scoreboard in
> [`STATUS.md`](../STATUS.md), and no signed row moves. The convention is
> `edge_direction` and `edge_budget`'s. What this can be worth is the rest: the
> pair is reproducible, owned, labelled by surface, and pinned by a test.

Reproducible: `python3 -m harness.default_rule_control` ·
`results/default_rule_control.json` · `tests/test_default_rule_control.py`.

---

## Why it exists

`H29`, the hidden policy's default, is `lambda c: True`. It has **no conditions**.
`validate_rule_payload` requires at least one, so `ceiling_check.HIDDEN_DSL`
transcribes it as `severity gte 1` — true over the whole domain — and
`RuleEngine.decide` arbitrates by counting conditions. The catch-all therefore
arrives at arbitration with specificity 1 and **ties with every single-condition
layer rule instead of yielding to it**.

[`FINDINGS.md`](FINDINGS.md), route 1, names that mechanism in one sentence and
stops there. Nothing in the repository quantified it, and *this is the first
question a referee asks*: how much of the headline failure is the priority thesis
and how much is a schema requirement.

It is exactly one rule of the 29. Checked rather than assumed: `H29` is the only
rule with a condition that holds for every value in its attribute's declared
domain, and its extension is all 134,400 cases.

---

## The pair, on both surfaces

Perfect policy loaded, 29 rules, no LLM, no learned rule. **Two surfaces because
they answer different questions** ([`STATUS.md`](../STATUS.md), *Before reading
any figure*) — the corpus is the modelled arrival distribution, the space is the
uniform measure over the 134,400 combinations — and rung 1 published corpus
figures without labelling them.

| surface | arbitration | coverage | e2e | CONFLICT | silent errors |
|---|---|---|---|---|---|
| corpus (n=2000, seed 17) | specificity, as published | 0.7475 | **0.5875** | 505 | 320 (0.2140) |
| corpus (n=2000, seed 17) | specificity, catch-all at its true rank | 0.8480 | **0.6880** | 304 | 320 (0.1887) |
| exhaustive space (134,400) | specificity, as published | 0.4621 | **0.2725** | 72,298 | 25,474 (0.4102) |
| exhaustive space (134,400) | specificity, catch-all at its true rank | 0.5354 | **0.3458** | 62,445 | 25,474 (0.3540) |

**The criterion is unchanged.** Most conditions wins; a tie with different actions
is a CONFLICT; a tie with the same action goes to the oldest. What changes is what
is counted: the *effective* specificity of a rule is the number of its conditions
that are not vacuous, which is the DSL's count for 28 of the 29 rules and 0 for
`H29`. It is the same arbitration applied to the policy **as written** instead of
to the transcription the schema forced.

**And it is oracle-free, which is what makes it a control rather than a rigged
criterion.** Vacuity is read off `DOMAINS` and the rule itself — available on a
learned base, available to any engine, no layer order anywhere in it. Handing
`H28` (a defaults-layer rule with a real condition) a lower rank would need the
layer order, and would be giving the criterion the answer it is being tested on.
That line separates correcting an **encoding** artifact from inventing a
**priority** one, and it is not crossed here.

---

## What the control moves

| | corpus | exhaustive space |
|---|---|---|
| published conflicts | 505 | 72,298 |
| of those, the catch-all is a finalist in | 276 | 11,973 |
| resolved once it yields | 201 | 9,853 |
| of those, resolved **correctly** | 201 | 9,853 |
| still in conflict | 304 | 62,445 |
| share of conflicts that were the encoding | **39.8%** | **13.6%** |
| e2e | +0.1005 | +0.0733 |

**The two surfaces disagree about the size and agree about the nature.** Roughly
40% of the corpus's conflicts were the encoding; on the uniform space it is 13.6%.
Citing "about 40%" without its surface would be the defect `STATUS.md` opens
with — the arrival distribution is long-tailed, and the regions where a
single-condition rule is alone with the catch-all are common in deployment and
rare in the space.

**Being in the conflict is not the same as causing it.** 75 of the 276 corpus
conflicts the catch-all takes part in survive its yielding, because the remaining
finalists still disagree.

---

## What the control cannot do, and does not do

**It never changes a decision already taken, and it never resolves a conflict
wrongly.** Both are checked over every case of both surfaces
(`gate_no_action_changes`, `gate_no_resolution_is_wrong`); the module refuses to
publish a row if either fails. They are also a proof, which is why the failure of
one would be a defect in the code and not a finding:

A case can only move where the catch-all is a finalist under the published
encoding, which requires the top specificity to be 1. Give `H29` its true rank and
the finalists become the matching single-condition rules. If they disagree, the
case stays a CONFLICT. If they agree on action A, then the whole matching set is
those rules plus `H29` — nothing with two or more conditions matched, or the top
would not have been 1 — and `H29` is born last, so **first-match-wins picks one of
them and A is the true action**. Nothing is lost either: dropping `H29` from a set
of finalists that already agreed leaves the same action, and where it matched
alone it still wins.

**Hence the silent-error count is identical in all four rows of the table** — 320
on the corpus, 25,474 on the space — and only its denominator moves. The artifact
inflated the rate at which the engine *abstains*. It never made it wrong. Whatever
the 0.5875 is cited for, it cannot be cited as evidence that the encoding produced
silent errors.

---

## By true class, on the corpus — where the gain is, and where it is not

| class | corpus | CONFLICT published | CONFLICT control | correct published | correct control |
|---|---|---|---|---|---|
| T2_TECHNICAL | 726 | 243 | 88 | 176 | 331 |
| SELF_SERVICE_DEFLECT | 495 | 63 | 17 | 426 | 472 |
| BILLING_SPECIALIST | 271 | 121 | 121 | 144 | 144 |
| T1_GENERAL | 255 | 0 | 0 | 255 | 255 |
| T3_ENGINEERING | 117 | 21 | 21 | 95 | 95 |
| ACCOUNT_MANAGER | 109 | 36 | 36 | 73 | 73 |
| SECURITY_INCIDENT | 20 | **17** | **17** | 3 | 3 |
| ONCALL_ESCALATION | 7 | **4** | **4** | 3 | 3 |

**The whole gain is in the two commonest classes, and the two critical rare ones
move by zero.** `SECURITY_INCIDENT` stays in conflict on 17 of its 20 cases and
`ONCALL_ESCALATION` on 4 of its 7 — exactly the classes CLAUDE.md's Step 5 says
the aggregate hides. The same two classes take the whole gain on the exhaustive
space too (`T2_TECHNICAL` 9,678, `SELF_SERVICE_DEFLECT` 175, the other six zero),
so this is not an artifact of the arrival distribution.

An engine that abstains on 85% of its security incidents does not become
deployable because its aggregate rose ten points.

---

## What remains in conflict, which is what the thesis is made of

304 cases on the corpus in 61 distinct finalist sets, 62,445 on the space in 269.
**None of them involves the catch-all**, on either surface. Every one is a set of
rules with *equal effective specificity* and *different actions* — the shape no
criterion monotone in the number of conditions can order.

| cases (corpus) | finalists | conditions | first-match-wins would pick |
|---|---|---|---|
| 95 | H11 vs H24 | 2 | H11 → BILLING_SPECIALIST |
| 37 | H16 vs H28 | 1 | H16 → T2_TECHNICAL |
| 17 | H12 vs H28 | 1 | H12 → SELF_SERVICE_DEFLECT |
| 16 | H18 vs H28 | 1 | H18 → T2_TECHNICAL |
| 12 | H11 vs H14 | 2 | H11 → BILLING_SPECIALIST |

On the space the head of the list is `H01 vs H13` (5,120 cases) and `H01 vs H14`
(3,640): the security override tying with churn risk, both with two conditions.

The impossibility of [`FINDINGS.md`](FINDINGS.md) §2, route 1, is untouched by any
of this, because it is internal to the policy and mentions no encoding: `H01`
(2 conditions) must beat `H03` (1) and `H16` (1) must beat `H24` (2), which no
monotone function of the condition count can satisfy at once. The control does
not weaken it; it removes the one part of the evidence that was not about it.

---

## How to read this, and no further

**The finding survives.** 0.6880 on the corpus, 0.3458 on the space, against the
1.0000 that the same 29 rules reach under first-match-wins
([`FINDINGS.md`](FINDINGS.md), route 2, corpus). Specificity still cannot execute
a policy prioritized by layers, and STOP 0 of CLAUDE.md is not passed by a
corrected encoding.

**Rung 1's frontier corollary survives too.** On the same surface and the same
engine, `keep_k(k=4)` reaches 0.780 e2e ([`FINDINGS.md`](FINDINGS.md), route 1,
corpus, which owns that figure). The corrected ceiling of 0.6880 is still below
it, so *"the region to beat was above the system's ceiling"* is not an artifact of
the catch-all either.

**What does move is what the 505 may be cited for.** Two fifths of it, on the
arrival surface, was a schema requirement rather than the priority thesis. Anyone
quoting the conflict rate as the size of the arbitration failure is quoting a
number with an encoding artifact inside it, and now there is a figure saying how
much.

**What this record does not say.** It does not measure how often policies in
general have the shape that defeats specificity — that is the sensitivity sweep of
[`ARBITRATION_REPORT.md`](../ARBITRATION_REPORT.md) §9.1, written down three times
and still not run ([`EXTERNAL_REVIEW.md`](../EXTERNAL_REVIEW.md) §1.4, item 5). It
does not touch the learned base: every figure here has the perfect policy loaded.
And it is not a proposal to change the DSL — `dsl.py` is frozen, the schema
requirement is a reasonable one, and the artifact it produces is now measured
rather than removed.
