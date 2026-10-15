# What the screen of compiled rules does to the model — findings

Record opened on October 14, 2026, under [`PLAN_SCREEN.md`](../PLAN_SCREEN.md).
Sergi signed §0 on 2026-10-14, before any figure below existed, in a commit of
its own: *PLAN_SCREEN.md signed by Sergi*. Every record names in its `_env` the
commit of the branch it was written on. A rebase merge gives those commits new
hashes on `main` with the same trees. **This record owns every figure in it.**

**Stage C adjudicated all four signed rows on 2026-10-15: three hold and one is
refuted.** `V-a` is the refutation, and it is thin.

- **Without its screen the model is right more often** (`V-b`).
- **The screen pulls the model to its commonest action** (`V-c`). That helps
  where the action is the true queue and costs where it is not (`V-d`), and on
  these bases it is not, about seven times in ten.
- **The model without a screen moved a little in twelve days** (`V-a`), in which
  answer it gives and not in how often it is right. Asked under both arms on
  one day, the pilot shows the same gap.
- **The rarest queues are in the model, on a second day.** With the ticket
  alone, both answers name them on every ticket (`V-e`).

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Row `V-e` carries no band.
> Its pilot half reproduces figures the drafter computed with a scratch probe
> before drafting, which §0 of the plan declares as already seen. Its held-out
> half was computed here for the first time, after the signature. Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `V-a` to `V-d` were signed
> before any of their figures existed, and three of the four bands were set on
> the pilot, a development set. `V-a`'s screen clause was read once,
> provisionally, after the anchor, as Stage B records. Stage C adjudicated it.

---

## Stage A — the checks, the populations and the free readout

**What was run.** `python3 -m screen.sample`, on 2026-10-14, with
`PYTHONHASHSEED=0`, on a clean tree. It took about two and a half minutes,
almost all of it the suite inside `V-g1`. The record is
[`sample.json`](sample.json).

**Surface: the corpus.** That is `generate_corpus(2000, seed=17)` in arrival
order, the decided cases of `PLAN_REUSE.md`'s three Stage B records as
`PLAN_FIDELITY.md` drew them. Nothing here is measured on the exhaustive space.

**Stage A ran twice, and the second run is the record.**

- **The first run**, from the signature's commit, lacked the counts and spreads
  §0 lists as seen, which §7 makes this record's to own. Every figure it did
  carry, the second run gives back. It was discarded before any commit.
- **The module gained them** in *screen/sample.py: Stage A measures the counts
  and spreads §0 lists as seen*. The second run is that commit's.

**The blocking checks passed before anything was computed.**

- **`V-g1`.**
  - The suite was green, 1,599 tests.
  - `PLAN_FIDELITY.md`'s F-g1 to F-g3 passed, and its Stage A record is the
    design they rebuild.
  - Its Stage C, re-run in memory with its own functions, gave back its
    `score.json` to a relative 1e-12.
  - Every one of its session records is under its protocol and behind its Stage
    A record.
- **`V-g2`.** 1,184 ticket-only prompts, every one v1's empty base, and the 301
  that `F-f` asked carry the digests it recorded. The 300 anchor prompts are
  `F-f`'s B prompts, rebuilt to the digest. The plurality is defined on every
  decision.
- **`V-g3`.** The pilot is the first 100 of each draw. The held-out decisions
  are 429, 405 and 425, none of them on a ticket `F-f` asked, and every one of
  their screens shows a rule.
- **`V-g4`.** Signed.

### The counts and the pilot, measured

**Every figure §0 lists as already seen reproduces**, so §0 needs no erratum.
On the pilot, `t` is `F-f`'s one answer without a screen of 2026-10-03, and
`b₁`, `b₂` its two answers with the screen.

| §0's figure | measured |
|---|---|
| tickets in the draw and census; asked by `F-f`; behind the pilot | 1,184; 301; 276 |
| held-out decisions; with two valid answers with the screen | 429 · 405 · 425; 426 · 405 · 423 |
| tickets behind the held-out decisions; serving more than one | 883; 303 |
| rules on a held-out screen | 4 to 12, 12 at the median |
| the pilot's net, `t`'s accuracy less the mean of `b₁`'s and `b₂`'s | +0.130 · +0.030 · +0.025; pooled +0.0617, se 0.028 |
| `t` alone right, against `b₁` alone right | 48 against 29 |
| the plurality is the true queue | 0.26 · 0.40 · 0.24; pooled 0.30 |
| where it is, the screen ahead by | 0.178, on 90 |
| where it is not, the screen behind by | 0.167, on 210 |
| `b₁` is the plurality where `t` is not | 0.534 · 0.660 · 0.243; pooled 0.455, on 178 |
| the spreads: the net, the two cells, the pull | 0.484; 0.429 and 0.476; 0.498 |

The agreements and the table by true queue reproduce as well, figure for
figure. They are in the record's `readout.pilot`.

### The held-out decisions, without a single new answer

Computed here for the first time. These are the figures §10 kept behind the
gate.

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| held-out decisions | 429 | 405 | 425 |
| the screen's plurality is the true queue | 0.3077 | 0.3630 | 0.2847 |
| `V-d`'s cells, plurality right and wrong | 132 and 297 | 147 and 258 | 121 and 304 |

**What it says.**

1. **The held-out screens are the pilot's kind.** Their plurality is the true
   queue on about three decisions in ten, as on the pilot. A copier that
   answered it would be right that often.
2. **Every cell of `V-d` is populated.** The smallest holds 121 decisions,
   against §0's minimum of 50. So no run can lose a value of `V-d` to its
   population; only invalid answers could take one.
3. **The class mix is the draw's, less the rare classes.** Every queue's share of
   the held-out decisions is within 1.7 points of its share of the whole draw.
   No held-out decision is of a rare class, as §2.1 said: `F-f` asked every
   rare-class ticket. The rare classes are `V-e`'s census.

### What Stage A does not settle

Nothing in it is adjudicable. The rows need the answers without a screen, which
Stage B buys. The smoke session goes first, then the anchor, then the ticket-only
session, each on Sergi's word, each record committed before the next.

---

## Stage B

Sergi gave the go-ahead for the smoke session on 2026-10-14, and for nothing
beyond it. Each later session waits for its own go-ahead (§8).

**The smoke session passed and opens the others.** `screen.ask --session smoke`,
2026-10-14, with `PYTHONHASHSEED=0`, from Stage A's commit and a clean tree. The
checks of §8 ran in order before any call.

- **The key** was an API key OpenRouter accepts, not a management key.
- **`V-g1` to `V-g4` passed**, with the suite green at 1,599 tests.
- **Stage A's record held** the same sessions, prompts and decisions the checks
  rebuilt.

What came back:

- **All 10 answers were valid**: five ticket-only prompts and five anchor
  prompts, each in one attempt.
- **Every call carried `reasoning: {"effort": "none"}`**, and so does the record.
- **Every attempt's `finish_reason` was recorded, and all ten were `stop`.** This
  is the first record of the thread to keep one; `PLAN_FIDELITY.md`'s never did.
- **The partial file was gone once the record was written.**

The record is [`ask_smoke.json`](ask_smoke.json). Its answers enter no row, and
none is read here.

**The pace.** The calls took 2.49 s at the median, from 1.96 to 17.51 s, and
39.7 s in all. At that median the anchor's 300 calls would take about 13 minutes
and the ticket-only session's 2,368 about 1.6 hours. Ten calls are few, so the
planning figures stay §1's: about half an hour and 2.5 hours.

**The anchor session: 300 answers of 300 valid.** On Sergi's go-ahead,
`screen.ask --session anchor`, 2026-10-14, `PYTHONHASHSEED=0`, from the smoke
run's commit and a clean tree. It ran as a background command of the agent's
harness. The checks of §8 passed before any call. The record is
[`ask_anchor.json`](ask_anchor.json).

- **No call failed.** Every prompt was answered in one attempt, and every
  `finish_reason` was `stop`.
- **The pace by the wall clock: 16.1 minutes of calling**, 3.21 s per answer,
  inside the half hour a background command lasts. The per-call timer's median
  was 2.79 s, from 1.18 to 15.56 s.
- **The partial file was gone once the record was written.**

**`V-a`'s screen clause, read once the anchor was in, as §8 intends:
provisional.** §8 runs the anchor before the ticket-only session so that the
instrument is measured before most of the spend. So the clause was computed with
Stage C's own function, `screen.score.screen_clause`, on this record:

- **The value.** `S − A = +0.0284`, with a standard error of 0.0174, over 299
  prompts. The two answers of 2026-10-02 or 03 agree with each other 0.9164 of
  the time; the answer of 2026-10-14 agrees with them 0.8880 of the time.
- **Per run**: +0.0101, +0.0400 and +0.0350.
- **Against the line.** At the signed line, ≤ 0.05, it would hold, and not
  thin. `F-a`'s gap was −0.0075 across two days; this one spans eleven or
  twelve.
- **Accuracy.** On the same prompts, the new answers are right 0.4567 of the
  time, and the old ones 0.4632, the mean of two.

**This is not the verdict.** `V-a` has a second clause, about the prompts
without a screen, which the ticket-only session measures, and Stage C
adjudicates both. It is written here because it was known before most of the
spend.

**What the anchor's pace says about the next session.** At 3.21 s per answer,
the ticket-only session's 2,368 calls would take about 2.1 hours by the wall
clock. That outlives a background command, so it runs in Sergi's terminal.

**The ticket-only session: 2,368 answers of 2,368 valid.** On Sergi's go-ahead,
`screen.ask --session ticket_only`, 2026-10-14, `PYTHONHASHSEED=0`, run in
Sergi's terminal from the anchor's commit and a clean tree, in one segment. The
checks of §8 passed before any call. The record is
[`ask_ticket_only.json`](ask_ticket_only.json).

- **What was asked.** The 1,184 tickets, in two passes, each in its own seeded
  order.
- **No call failed.** Every answer was valid in one attempt, and every
  `finish_reason` was `stop`.
- **The pace by the wall clock: 1.45 hours of calling**, 2.2 s per answer. The
  per-call timer's median was 2.05 s, from 0.97 to 33.55 s.
- **The partial file was gone once the record was written.**

**Stage B is complete: 2,678 calls, 2,678 answers valid**, every one in one
attempt and with `finish_reason` `stop`.

---

## Stage C — the four adjudications

**What was run.** `python3 -m screen.score`, on 2026-10-15, with
`PYTHONHASHSEED=0`, from the ticket-only session's commit and a clean tree.

- **Every blocking check passed first**, with the suite green at 1,599 tests.
- **Both paid records** carried this plan's protocol and Stage A's digest.
- **The labels** the ticket-only rows carry agree with `PLAN_FIDELITY.md`'s for
  every decision they serve.

The record is [`score.json`](score.json).

**Surface: the corpus.** That is the held-out decisions of `PLAN_FIDELITY.md`'s
draw over `PLAN_REUSE.md`'s three Stage B runs, seed 17, in arrival order.
`V-b` to `V-d` are read on the median of the three runs, and `V-a` pooled.

Notation as §0's: `t₁`, `t₂` the two answers without a screen, of 2026-10-14;
`b₁`, `b₂` the two with it, of 2026-10-02 or 03; `p` the screen's plurality
action; `y` the true queue.

| row | statistic | run 1 | run 2 | run 3 | value | band | verdict |
|---|---|---|---|---|---|---|---|
| `V-a` | `S − A`, pooled: without a screen, over 301 tickets; with it, over 299 prompts | — | — | — | **+0.0615** (se 0.0191) and **+0.0284** (se 0.0174) | ≤ 0.05, both | **refuted, thin** |
| `V-b` | the accuracy without the screen less the accuracy with it | +0.1279 | +0.0667 | +0.0366 | **+0.0667** (se 0.0191) | > 0 | **holds** |
| `V-c` | where `t₁ ≠ p`: the answers with the screen on `p`, less `t₂` on `p` | 0.3178 | 0.5399 | 0.2500 | **0.3178** (se 0.0266) | ≥ 0.10 | **holds** |
| `V-d` | where `p = y`, the screen ahead; where `p ≠ y`, the screen behind | +0.0573 and +0.2102 | +0.1769 and +0.2054 | +0.1583 and +0.1139 | **+0.1583** (se 0.0310) and **+0.2054** (se 0.0218) | > 0, both | **holds** |

Pooled over the three runs, beside the medians and adjudicating nothing:
`V-b` +0.0774 (se 0.0104), `V-c` 0.3552 (se 0.0158), and `V-d` +0.1319 and
+0.1746 (se 0.0159 and 0.0122).

**The drafter expected all four to hold, and got three.** It trusted `V-b`
least, then `V-a`.

- **`V-a` is the refutation, and it is thin**, as the label §0 fixed in advance
  says.
- **`V-b` held 3.5 standard errors clear of its line**, where the drafter
  expected it to sit within one. The pilot's median run was +0.030; the held-out
  decisions put the median at more than twice that.
- **The three bands set on the pilot all held.** They say the pilot's reading
  generalises to decisions nobody had asked about, not that the drafter foresaw
  it.

### What the verdicts say

**1. The model without a screen moved a little in twelve days, in which answer
it gives, and not in how often it is right.** `V-a`'s first clause is refuted at
+0.0615. On the 301 tickets `F-f` asked on 2026-10-03, the two answers of
2026-10-14 agree with each other 0.9236 of the time, and with the answer of
2026-10-03 only 0.8621 of the time. Its screen clause holds at +0.0284: with a
screen, the model of 2026-10-14 still answers as the one of 2026-10-02 did.

**What moved is which wrong queue it picks.** On the pilot's 300 decisions, the
model without a screen was right 0.5233 of the time on 2026-10-03, with one
answer, and 0.5200 on 2026-10-14, the mean of two. With the screen it was right
0.4617 then, the mean of two, and 0.4567 now, with one. Neither arm's accuracy
moved.

**2. Asked under both arms on one day, the gap is the same.** On 2026-10-14 the
pilot's 300 decisions were asked with the screen, by the anchor, and without it,
by the ticket-only session. Without the screen the model is right 0.5200 of the
time, and with it 0.4567: a gap of +0.0633. Across the two dates the same
decisions gave +0.0617. So the drift `V-a` caught does not carry the screen's
effect, on the one set where both arms share a day. That set is the development
set. On the held-out decisions the arms are twelve days apart, and §0 has `V-b`
to `V-d` carry the anchor's gap beside them, which this paragraph does.

**3. Without its screen the model is right more often.** `V-b` holds at
+0.0667 on the median, and in every run: +0.1279, +0.0667 and +0.0366. Without
the screen the model is right 0.5458, 0.5074 and 0.5260 of the time; with it,
0.4178, 0.4407 and 0.4894. Pooled, +0.0774.

**4. The screen pulls the model to its commonest action.** `V-c` holds at
0.3178. Where the model's own answer is not the screen's plurality action, the
answers with the screen land on that action 0.3178 more often than a second
answer without the screen does: 0.3178, 0.5399 and 0.2500 by run. Of the 700
answers the screen changed on the held-out decisions, pass for pass:

| what the answer with the screen became | all changes | changes that cost | changes that paid |
|---|---|---|---|
| the plurality action | 516 | 257 | 118 |
| the first rule's action, not the plurality's | 73 | 44 | 9 |
| another action on the screen | 87 | 45 | 25 |
| an action the screen does not show | 24 | 9 | 9 |
| **all** | **700** | **355** | **161** |

A change costs where the answer without the screen was right, and pays where the
answer with it is. **Nearly every change goes to an action the screen shows, and
three in four to its commonest.** The plurality, the mechanism `V-c` bet on, is
most of it, and not all: §5.4 of the plan asked for this classification so that
no single mechanism was taken for the whole.

**5. What the screen does follows its plurality.** `V-d` holds in both clauses
and in every run. Where the plurality is the true queue, the screen puts the
model ahead by +0.1583 on the median. Where it is not, the screen puts it behind
by +0.2054. In each base the net is exactly those two, weighted by how often the
plurality is right:

| | run 1 | run 2 | run 3 |
|---|---|---|---|
| the plurality is the true queue | 0.3075 | 0.3630 | 0.2837 |
| the screen ahead where it is | +0.0573 | +0.1769 | +0.1583 |
| the screen behind where it is not | +0.2102 | +0.2054 | +0.1139 |
| the net, `V-b` | +0.1279 | +0.0667 | +0.0366 |

**So the screen's cost is the base's error, carried by deference.** On these
bases the plurality is wrong about seven times in ten, so the screen costs. The
same deference to a base whose plurality is right more often than not would
pay. No base here is one.

**6. The rarest queues are in the model, on a second day.** With the ticket
alone, both answers name `ONCALL_ESCALATION` on all 7 of its tickets, 14
answers of 14, and `SECURITY_INCIDENT` on all 20, 40 of 40. `F-f` read the same
on 2026-10-03.

### Recorded beside the rows, and never in a denominator

- **The held-out decisions by true queue**, the mean of two answers in each arm:

  | true queue | decisions | without the screen | with it |
  |---|---|---|---|
  | `T2_TECHNICAL` | 464 | 0.789 | 0.916 |
  | `SELF_SERVICE_DEFLECT` | 311 | 0.291 | 0.076 |
  | `T1_GENERAL` | 186 | 0.151 | 0.003 |
  | `BILLING_SPECIALIST` | 171 | 0.997 | 0.640 |
  | `ACCOUNT_MANAGER` | 65 | 0.000 | 0.062 |
  | `T3_ENGINEERING` | 57 | 0.096 | 0.018 |

  The screen helps where the bases mostly decide right, `T2_TECHNICAL`, and
  costs most where the model alone already knows the queue,
  `BILLING_SPECIALIST`. **`ACCOUNT_MANAGER` is the model's**: with the ticket
  alone it names the queue on none of the class's 65 held-out decisions. The
  screen is not what loses that class.
- **`finish_reason`.** Every one of the 2,678 calls ended `stop`, in one attempt.
  No answer came back empty or cut off, where `PLAN_FIDELITY.md`'s sessions lost
  13 of 4,295.
- **Tickets serving decisions in more than one run.** Of the 883 tickets behind
  the held-out decisions, 594 serve one run, 252 two and 37 three, as §5.1
  warned.

### What Stage C does not settle

- **Why the model defers.** Whether it trusts what reads as compiled policy, or
  follows whatever list it is given, these answers cannot say. A screen of rules
  drawn at random, or of the hidden policy's nearest rules, would separate them.
- **Whether a better base would turn the cost into a gain.** `V-d`'s first clause
  reads the screen where its plurality happens to be right. No base here is
  right more often than not.
- **The loops.** `PLAN_AUTHORSHIP.md`'s and `PLAN_BLIND.md`'s figures came from
  loops. This record says the screen costs the model on re-asked decisions, not
  how much of those loops' differences it explains.
- **What moved in twelve days.** OpenRouter routes the model's name to
  providers, and no record of the thread keeps which one answered.
- **One model, one corpus, three bases.**

---

## Files

```
results_screen/sample.json       Stage A: the checks, the populations, the
                                 sessions with every prompt's digest, and V-e's
                                 free half
results_screen/ask_smoke.json    Stage B, the smoke session: 10 of 10 valid;
                                 it opens the other sessions and enters no row
results_screen/ask_anchor.json   Stage B, the anchor: the 300 pilot B prompts
                                 once, 300 of 300 valid; V-a's screen clause
results_screen/ask_ticket_only.json   Stage B, the ticket-only session: 1,184
                                 tickets twice, 2,368 of 2,368 valid
results_screen/score.json        Stage C: V-a to V-d, the pooled values, V-e
```
