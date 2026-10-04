# The founding question, on the engine that can answer it — findings

Record opened on September 29, 2026. [`PLAN_REUSE.md`](../PLAN_REUSE.md), §0
signed by Sergi on 2026-09-29 before any figure below existed — `9097ba3` on
`main`. The records' `_env` names `9a52cb1`, the same tree before the rebase
merge rewrote its hash. §1 carries an amendment, signed by Sergi on 2026-09-30,
before any full run existed. **This record owns every figure in it.**

**Stage C adjudicated all five signed rows on 2026-09-30: four hold and one is
refuted.** `U-d` is the refutation: the loop never escalated the rarest queue in
any of the three runs. Two of the holds, `U-b` and `U-c`, sit on their lines.

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Row `U-f` carries no band:
> its inputs have been on disk since 2026-08-07, and the drafter had read their
> metrics blocks before drafting the plan (§0). Zero API calls.
>
> **PROVENANCE, STAGES B AND C: PRE-REGISTERED.** `U-a` to `U-e` were signed
> before any of their figures existed, and the amendment to §1 before any full
> run did.

---

## Stage A — the eight n=100 records, read for the founding question

**What was read.** Rung 2's eight records, `results2/llm_run2_n100*.json` —
prompts v1 and v2, the corpora of seeds 17 to 20, 100 cases each — through
`python3 -m reuse.readout` on 2026-09-29, with `PYTHONHASHSEED=0`, from the
signed commit and a clean tree. The record is
[`readout_n100.json`](readout_n100.json). **Surface: the corpus each run saw, in
arrival order, 100 cases.** Nothing here is measured on the exhaustive space.

**The blocking checks passed before anything was computed.** `U-g1`: the hybrid
engine executes the hidden policy at 1.0000 on the corpus and on the space, and
the suite is green. `U-g2`: all eight records reproduce their own metrics, fire
counts, births and corpus. `U-g3`: `keep_k` reproduces
[`results/frontier.json`](../results/frontier.json), and no case is matched by
two of its rules. `U-g4`: signed.

### The silent error, split by the birth of the rule that made it

The acting axis of §5.2: a rule *born wrong* is one whose birth escalation chose
a queue other than the ticket's true one.

| prompt | seed | rules | reuse | silent error | silent errors | by rules born wrong | share |
|---|---|---|---|---|---|---|---|
| v1 | 17 | 40 | 0.6000 | 0.7241 | 42 | 34 | 0.8095 |
| v1 | 18 | 14 | 0.7857 | 0.7442 | 64 | 56 | 0.8750 |
| v1 | 19 | 12 | 0.8333 | 0.5116 | 44 | 27 | 0.6136 |
| v1 | 20 | 26 | 0.7692 | 0.7361 | 53 | 43 | 0.8113 |
| v2 | 17 | 6 | 0.8333 | 0.7553 | 71 | 34 | 0.4789 |
| v2 | 18 | 9 | 1.0000 | 0.7000 | 63 | 44 | 0.6984 |
| v2 | 19 | 12 | 0.6667 | 0.6023 | 53 | 35 | 0.6604 |
| v2 | 20 | 26 | 0.6154 | 0.8873 | 63 | 54 | 0.8571 |
| **v1 pooled** | | | | | **203** | **160** | **0.7882** |
| **v2 pooled** | | | | | **250** | **167** | **0.6680** |

### The rules born with the right queue, against `keep_k`

The scope axis of §5.2. `F` is the `keep_k` frontier at the subset's reuse, on
the run's own corpus at n=100; pooled, both sides are pooled over the same four
corpora. A negative gap means the rules err *less* than the heuristic at the
same reuse.

| prompt | seed | rules | reused | decided | correct | reuse | silent error | `F` | gap |
|---|---|---|---|---|---|---|---|---|---|
| v1 | 17 | 16 | 8 | 19 | 11 | 0.5000 | 0.4211 | 0.1405 | +0.2806 |
| v1 | 18 | 5 | 5 | 28 | 20 | 1.0000 | 0.2857 | 0.6316 | −0.3459 |
| v1 | 19 | 6 | 6 | 59 | 42 | 1.0000 | 0.2881 | 0.6737 | −0.3855 |
| v1 | 20 | 12 | 7 | 28 | 18 | 0.5833 | 0.3571 | 0.1824 | +0.1748 |
| v2 | 17 | 2 | 2 | 56 | 19 | 1.0000 | 0.6607 | 0.9388 | −0.2781 |
| v2 | 18 | 2 | 2 | 31 | 12 | 1.0000 | 0.6129 | 0.6316 | −0.0187 |
| v2 | 19 | 5 | 4 | 50 | 32 | 0.8000 | 0.3600 | 0.6737 | −0.3137 |
| v2 | 20 | 7 | 5 | 12 | 3 | 0.7143 | 0.7500 | 0.5879 | +0.1621 |
| **v1 pooled** | | **39** | **26** | **134** | **91** | **0.6667** | **0.3209** | **0.4620** | **−0.1411** |
| **v2 pooled** | | **16** | **13** | **149** | **66** | **0.8125** | **0.5570** | **0.7309** | **−0.1738** |

**The memorization floor at n=100**, `keep_k(8)`'s reuse on each corpus: 0.0000
for seeds 17, 19 and 20, and 0.0204 for seed 18.

### What it says

**1. At a hundred cases, the rules are not memorizing.** Reuse runs from 0.60 to
1.00 in all eight runs, where a rule that matches one ticket exactly — reused
only when a duplicate arrives — reaches 0.0000 on three of the four corpora and
0.0204 on the fourth. The 0.1176 of n=2000 is not the floor at this horizon. In
the terms Sergi signed on 2026-08-05, the rules are reused.

**2. Most of the silent error was decided before the rule was written.** Rules
born with the wrong queue made **0.7882** of the silent errors under v1 and
**0.6680** under v2, and seven runs of eight are at 0.60 or above. The exception
is v2 seed 17, at 0.4789: the six-rule base `CHAT_SUMMARY.md` §1 called a silent
disaster. Its two right-born rules decided 56 cases and got 37 of them wrong.

**3. On the scope axis alone, the rules do better than the heuristic at a hundred
cases.** Rules born with the right queue err **0.3209** (v1) and **0.5570** (v2),
where `keep_k` at the same reuse errs 0.4620 and 0.7309. The pooled gaps are
**−0.1411** and **−0.1738**, and five runs of eight are negative. **That is the
opposite of what the drafter expected for `U-b`** (§0 of the plan: *the rules
generalize worse*). `U-f` has no band, so this is not a calibration event. It is
written down before Stage B exists, so that it cannot be written afterwards.

**4. Why it does not settle `U-b`.** The frontier at n=100 is not the frontier at
n=2000. Pooled over these four corpora, `keep_k` errs 0.46 to 0.73 at reuse 0.67
to 0.81. Over 2,000 cases the published frontier reaches reuse 0.7965 at a silent
error of 0.1728 (`keep_k(4)`, `results/frontier.json`). Per run, `F` spans 0.1405
to 0.9388: at a hundred cases the frontier is coarse, and where a run's
right-born reuse lands on it moves `F` more than the rules do. A negative gap here
warns that `U-b`'s band may be wrong. It is not a reading of that band.

**5. The rarest queue never arrived.** No case among the first hundred of seeds
17 to 20 is `ONCALL_ESCALATION`, so `U-d` cannot be read at this horizon.
`SECURITY_INCIDENT` arrived once, in seed 17's corpus: it escalated under v1, and
under v2 a rule decided it, wrongly. These are counts, not rates (§5.6).

**6. The escalations were coverage impasses.** Two of the 155 were CONFLICT, one
each in v2 seeds 18 and 20. `U-a`'s reading at n=100 carries none of rung 1's
caveat.

### What Stage A does not settle

- **The horizon.** A hundred cases is a twentieth of the horizon `U-a` to `U-e`
  are read at. The first hundred cases of seed 17 are the same draws at both
  horizons (`tests/test_reuse.py`), and the proposer that will meet them in Stage
  B is not the same draw.
- **Any verdict.** `U-f` has no band. `U-b` and `U-c` are read on Stage B's runs,
  at n=2000, against the frontier at n=2000.
- **The date.** The eight runs were asked in early August and Stage B asks weeks
  later (§5.5): n=100 against n=2000 carries the date as an uncontrolled variable.
- **Fidelity.** The split by birth is a proxy for whether a compiled rule decides
  as the model would have, not a measurement of it (§12.1).

---

## Stage B

Sergi gave the go-ahead on the spend on 2026-09-30: a 20-case smoke run first,
then three runs of n=2000, prompt v1, seed 17, one after another.

**The first smoke run caught a key OpenRouter does not accept.** `reuse.run
--smoke`, 2026-09-30. The blocking checks passed. Then all 20 escalations failed
with `401 — User not found`, no rule was born, and nothing was generated or
spent. The record is kept as [`run_n20_smoke_401.json`](run_n20_smoke_401.json),
so that the smoke run's own name stays free for the rerun under a working key.

This is the check §8 of the plan describes, doing its job. The loop counts a
failed proposal and carries on, so with that key each full run would have spent
hours producing a record with no model output in it. **Since the same day the
full runs refuse to start without a smoke record, under this plan's protocol,
that shows at least one proposal that parsed and one rule born**
(`reuse/run.py`, step 2b). This record fails that check, and
`tests/test_reuse.py` pins that it does.

**The second smoke run met a management key, and the check refused it as
built.** Also 2026-09-30, after the key in `~/.bashrc` was replaced: the same 20 ×
`401 — User not found`, no rule born, nothing generated or spent, and step 2b
kept the full runs closed. The record is kept as
[`run_n20_smoke_401_management_key.json`](run_n20_smoke_401_management_key.json).
The cause was read off OpenRouter's own key endpoint: the new key is a
**management key**. That kind of key authenticates the endpoint — it answered 200
— and reads the account's credits, but cannot call a model. **So a 200 from that
endpoint is not a check that a key works.** Since the same day `reuse/run.py`
asks the endpoint before the smoke run and before every full run, and refuses a
management key or any answer but 200 (step 2c). That takes a second, where the
smoke run took about twelve minutes to fail.

**The third smoke run, under an API key, passed and showed the model has
changed.** Also 2026-09-30, from `3952e5b`. The key check passed, then the
blocking checks, and step 2b opened the full runs: 15 escalations, 10 rules born.
**But 5 of the 15 proposals came back empty, or cut off in the middle of the
JSON**, against 9 of 155 in the eight August runs, and the 20 cases took about 25
minutes. The record is kept as
[`run_n20_smoke_reasoning_on.json`](run_n20_smoke_reasoning_on.json).

The cause was measured, not guessed. OpenRouter lists reasoning parameters for
`deepseek/deepseek-v4-flash`, and documents that reasoning tokens count against
`max_tokens`: a budget spent on reasoning comes back empty with
`finish_reason: "length"`. The proposer caps each answer at 1,200 tokens. Two
one-line calls on the same day gave 20 reasoning tokens for a six-token reply by
default, and none with `reasoning: {"effort": "none"}`. **The model reasons by
default now.** Whether it did in August is not recorded, and this is §5.5's date
variable with a mechanism found behind it.

**Sergi chose to turn reasoning off**, and §1 of the plan carries the amendment:
every call the proposer makes sends `reasoning: {"effort": "none"}`, and nothing
else moves — no prompt, no schema, no band. The smoke check now compares the
setting, so this record cannot open the full runs, and `tests/test_reuse.py`
pins that it cannot. The gate requires both signatures, §0's and the
amendment's.

**The fourth smoke run, under the signed amendment, passed.** Also 2026-09-30,
from the commit that carries Sergi's signature of the amendment, with the key
check and every blocking check passing first. Its 20 cases gave **14
escalations, 14 proposals parsed and 14 rules born**, and the run took about
five minutes end to end, against about twenty-five for the third. The record is
[`run_n20_smoke.json`](run_n20_smoke.json), and it carries its setting,
`reasoning: {"effort": "none"}`. It opens the three runs.

**The three runs**, 2026-09-30, one after another. Each started from a clean tree
after the key check, the smoke check and every blocking check, and each record
was committed before the next run began. The runs made **62, 31 and 42
escalations**, and **every proposal parsed**: 135 calls, none failed, none
rejected. Run 1 took about thirty minutes; runs 2 and 3 took a few minutes each.
The records are [`run_n2000_r1.json`](run_n2000_r1.json),
[`run_n2000_r2.json`](run_n2000_r2.json) and
[`run_n2000_r3.json`](run_n2000_r3.json).

## Stage C — the five adjudications

`python3 -m reuse.score`, 2026-09-30, `PYTHONHASHSEED=0`, from the commit that
holds run 3, with a clean tree. Every blocking check passed first, and before any
row was read each run's record reproduced its own metrics, fire counts, births and
corpus (§5.3). The record is [`score.json`](score.json). **Surface: the corpus
of seed 17, 2,000 cases in arrival order. Every verdict is read on the median of
the three runs**, and each run's value sits beside it (§0).

| row | statistic | run 1 | run 2 | run 3 | median | band | verdict |
|---|---|---|---|---|---|---|---|
| `U-a` | reuse rate | 0.5323 | 0.8387 | 0.7381 | **0.7381** | ≥ 0.30 | **holds** |
| `U-b` | right-born silent error − `F` | +0.3419 | −0.0815 | +0.0207 | **+0.0207** | > 0 | **holds** |
| `U-c` | silent errors by rules born wrong | 0.6490 | 0.6024 | 0.5880 | **0.6024** | ≥ 0.60 | **holds** |
| `U-d` | `ONCALL_ESCALATION` escalations | 0 | 0 | 0 | **0** | ≥ 1 | **refuted** |
| `U-e` | CONFLICT outcomes | 30 | 5 | 12 | **12** | ≤ 20 | **holds** |

**The drafter expected `U-a` to `U-d` to hold and `U-e` to be refuted** (§0). It
got three of five: **`U-d` was refuted and `U-e` held.** The row the drafter
trusted least held, and the one it argued from the hidden policy's own rules
failed.

### What the verdicts say

**1. The founding question, in its own terms: the rules are reused — with rung
1's caveat, as §0 fixed in advance.** `U-a` holds at 0.7381, far above the 0.30
line and the 0.1176 memorization floor of this horizon. But a median of 0.2857 of
the escalations were CONFLICT (0.4839, 0.1613 and 0.2857 by run), which is above
the one in four at which §0 said the record would carry rung 1's caveat. So part
of what escalated was the arbitration, not coverage, and the reuse figure is not
the clean measure the question was posed for. The verdict stands as signed; its
reading carries the caveat.

**2. Most of the silent error was decided before the rule was written — by a
margin of nothing.** `U-c` holds at 0.6024 against a line of 0.60, and one run of
three is below it (0.5880). About three silent errors in five come from rules born
with the wrong queue: the proposer chose the right queue for the ticket in front
of it 0.4839, 0.4839 and 0.5476 of the time, and roughly half its rules were born
wrong.

> **[ERRATUM 2026-10-04] The reading, not the figure.** `U-c`'s statistic and
> verdict stand. What does not stand is the reading beside them: that the other
> two silent errors in five, made by rules born right, are scope errors the model
> would not make.
>
> [`PLAN_FIDELITY.md`](../PLAN_FIDELITY.md) asked the model afresh on the cases
> the rules decided ([`FINDINGS_FIDELITY.md`](../results_fidelity/FINDINGS_FIDELITY.md),
> Stage C, `F-d`). On the rules' errors it is wrong too 0.7955 of the time, on
> the median of the three runs. On the errors of rules born right it is wrong
> 0.8661, 0.6558 and 0.8596 of the time by run. Case by case, the split by birth
> and its fresh answers agree on whose error it was 0.5507, 0.6171 and 0.5830 of
> the time.
>
> **So most of the silent error is the model's own, more of it than the split
> says, and the split is a poor guide to which.**

**3. On the scope axis alone, the rules err about as much as the heuristic at
their reuse — and the number says more about the frontier than about the rules.**
`U-b` holds at +0.0207 against a line of 0, with one run negative. The rules born
with the right queue err 0.4382, 0.3969 and 0.3224 on the cases they decide. But
the frontier is steep exactly where they land: between reuse 0.7965 (silent error
0.1728) and 0.8966 (0.6088). Run 1's right-born reuse, 0.5667, sits where `F` is
0.0962, so its gap is large. Runs 2 and 3, at 0.8667 and 0.8261, land on the steep
segment, where `F` is 0.4784 and 0.3017. The gap moves more with where the reuse
lands than with the rules' own error — the warning Stage A's §4 gave at n=100. It
is a hold as signed, and it is not a margin.

> **[NOTE 2026-10-04]** Most of the errors this point reads on the scope axis are
> ones the model, asked afresh, would make on those very tickets: see the
> erratum to point 2. `U-b` stands as signed. What its gap measures is less the
> rules' scope than it reads.

**4. The rarest queue was never asked about, in any run.** In all three runs, all
7 `ONCALL_ESCALATION` cases were decided by a rule, and all 7 wrongly every time;
none escalated. So what [`FINDINGS_ILP.md`](../results_ilp/FINDINGS_ILP.md) §3
found — *what the loop never asks about, no method can learn* — is not a property
of rung 1's conflict-driven trigger. A loop that escalates on coverage swallows
the rarest queue too: a broad rule reaches its region before any of its tickets
can escalate. The drafter bet the opposite, from the hidden policy's own
`severity == 1` rules, and lost.

**5. Overlap came back as the base grew, and declared priority got material for
the first time.** `U-e` holds at a median of 12 CONFLICTs, but run 1 had 30. On
those conflicts the proposer declared priority edges, and the engine accepted 30,
6 and 28 of them (33, 6 and 36 proposed; the rest were refused as `no_solapan`).
Rung 2's eight n=100 runs had proposed 14 and had none accepted. The verdict built
to catch a proposer contradicting subsumption, `contradice_subsuncion`, fired in
none of the three runs, so it is still unobserved in a real run.

**Recorded beside the rows and never in a denominator** — counts and rates by
run:

- e2e 0.3935, 0.4400 and 0.5130; silent error 0.5939, 0.5531 and 0.4760.
- Rules: 62, 31 and 42, one per escalation. Median fires per rule: 13, 35 and 24.
  Dead rules: 29, 5 and 11.
- The loop converges early. The first 200 cases escalate at 0.18, 0.14 and 0.155;
  no later decile of any run escalates at more than 0.025.
- `SECURITY_INCIDENT`, 20 cases. Escalated: 15, 3 and 2. Decided by a rule: 5,
  17 and 18. Decided rightly: 5, 6 and 18. Counts, not rates (§5.6): in run 3
  every compiled decision on the class was right, and in run 2 eleven of seventeen
  were wrong.

### What Stage C does not settle

- **Fidelity.** The split by birth is a proxy for whether a compiled rule decides
  as the model would have (§12.1). It is not a measurement of it, and the next
  plan is the one that measures it. **[NOTE 2026-10-04] Measured** by
  `PLAN_FIDELITY.md`: the rules decide unlike the model would, and compiling
  loses it nothing on the cases they decide. The erratum to point 2 says what
  that does to the proxy.
- **The instrument's date.** These runs were asked on 2026-09-30 with reasoning
  off; August's were asked with whatever the model did then, which is not
  recorded (§5.5 and §1's amendment). Stage A's n=100 figures and these are not a
  nested comparison.
- **The spread.** Three draws of one model over one corpus spread widely — reuse
  from 0.53 to 0.84, CONFLICTs from 5 to 30 — and two rows hold within a run of
  their lines. A second set of three would be the check of that, and it is not
  this plan's.
- **The frontier's shape.** `U-b` reads a heuristic whose error jumps between two
  adjacent points of reuse. A finer frontier, or a blind one (§12.2), would read
  the scope axis more steadily, and neither is here.

---

## Files

```
results_reuse/readout_n100.json   Stage A, U-f — the figures of its section
results_reuse/run_n20_smoke_401.json   the first smoke run: 20 × 401, no output
results_reuse/run_n20_smoke_401_management_key.json   the second: a management key
results_reuse/run_n20_smoke_reasoning_on.json   the third: passed, a third empty
results_reuse/run_n20_smoke.json   the fourth, reasoning off: 14 of 14, opens the runs
results_reuse/run_n2000_r1.json … run_n2000_r3.json   Stage B, the three runs
results_reuse/score.json          Stage C: U-a to U-e, per run and on the median
reuse/readout.py                  Stage A
reuse/run.py                      Stage B; 2b waits for a smoke run that worked,
                                  2c refuses a management key before any call
reuse/analysis.py                 §5.2 and §5.3: births, the split, the gap
reuse/frontier.py                 keep_k through the frozen loop; U-g3
reuse/gates.py                    U-g1 to U-g4
reuse/score.py                    Stage C
```
