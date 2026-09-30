# The founding question, on the engine that can answer it — findings

Record opened on September 29, 2026. [`PLAN_REUSE.md`](../PLAN_REUSE.md), §0
signed by Sergi on 2026-09-29 before any figure below existed — `9097ba3` on
`main`. The records' `_env` names `9a52cb1`, the same tree before the rebase
merge rewrote its hash. **This record owns every figure in it**, and it grows by
stage: Stage A is below; Stages B and C are appended when they run. **Nothing
here is adjudicated yet.**

> **PROVENANCE, STAGE A: REPORTED, NOT ADJUDICATED.** Row `U-f` carries no band:
> its inputs have been on disk since 2026-08-07, and the drafter had read their
> metrics blocks before drafting the plan (§0). Zero API calls.

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

## Stage C

Not run. It scores `U-a` to `U-e` on the median over Stage B's three runs.

---

## Files

```
results_reuse/readout_n100.json   Stage A, U-f — the figures of its section
results_reuse/run_n20_smoke_401.json   the first smoke run: 20 × 401, no output
results_reuse/run_n20_smoke_401_management_key.json   the second: a management key
results_reuse/run_n20_smoke_reasoning_on.json   the third: passed, a third empty
results_reuse/run_n20_smoke.json   the fourth, reasoning off: 14 of 14, opens the runs
reuse/readout.py                  Stage A
reuse/run.py                      Stage B; 2b waits for a smoke run that worked,
                                  2c refuses a management key before any call
reuse/analysis.py                 §5.2 and §5.3: births, the split, the gap
reuse/frontier.py                 keep_k through the frozen loop; U-g3
reuse/gates.py                    U-g1 to U-g4
```
