# PLAN_PRIMACY — where the slot decides

**Status: drafted by Claude on 2026-10-05, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §8 says why the gate binds anyway.

**This plan exists because §15 of [`FINDINGS3.md`](results3/FINDINGS3.md) left
the position effect open, and its erratum of 2026-10-05 changed what is open.**
§15 measured that the proposer follows its own queue ranking 0.8534 of the time
when the rule that ranking favours is listed first and 0.7623 when it is listed
second, and asked why the second slot costs nine points. The erratum says three
things that reshape the question:

- **The nine points are the first-listed rate read through the ranking.** They
  cannot tell a taste for the first slot from a loss in the second. What the
  randomised deal licenses is a floor: the slot decided the direction of at least
  about one edge in eleven. Whether that costs accuracy on net is not identified.
- **It has been seen on one population of two.** Stage C, the same prompt over
  the hidden policy's pairs, named the rule listed first in 84 of 166 answers.
- **Why cannot be answered from the answers paid for.** The rule listed first is
  always labelled `A`, and its queue is the first queue the question names.

[`IDEAS.md`](IDEAS.md) carries the item as free to attack. **What the answers
already paid for can still say is where the slot decides**, and whether it does
anything to an answer besides deciding which rule it names.

**What it would change.** Whether the slot acts as a tiebreaker where the
proposer is undecided, which is what the literature on position bias in model
judges would predict, or as a pull of its own that acts regardless; and whether
it disturbs the answers' form. Either way it sharpens what
[`STATUS.md`](STATUS.md) says about the effect, and tells the paid follow-up of
§10 where to look. **None of its figures exists**, so under
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable, although
it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic and its denominator here, before any figure.**
They all read `results2/pair_judgement_1600.json`, the 1,600 answers
`PLAN_PROPOSER_1600.md` paid for: 1,479 that declared an edge and 121 that did
not. **No surface applies to `L-a` or `L-b`**: they are properties of what was
said, and no truth enters them. Where the truth enters `L-c`, the block names
the definition of the better rule.

**Notation.** For a row, the **rule listed first** is the one shown as `A`. Its
**queue pair** is its two rules' queues; they always differ (`L-g3`). On a set of
declared answers with a reference rule chosen without looking at the slot, the
**slot effect `d`** is the share naming the reference when it is listed first,
minus the share naming it when it is listed second (§5.4). A queue pair's
**favoured queue** is the one named more often among its declared answers
(§5.3).

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **L-a** | **Where the proposer is undecided, the slot breaks the tie.** On the one queue pair it splits almost evenly, the slot decides at least a fifth of the answers | over the declared answers on `SELF_SERVICE_DEFLECT vs T2_TECHNICAL` (§2.1): `d` with `SELF_SERVICE_DEFLECT` as the reference. Either queue gives the same value | **d ≥ 0.20** | **d < 0.20** |
| **L-b** | **Where the slot and the proposer's favourite disagree, the answers do not break more often.** Whether the favoured rule is listed first or second does not change how often an answer yields no edge | over the 1,600 rows whose queue pair has a favoured queue: the share with no edge when the favoured rule is listed second, minus the share when it is listed first | **\|difference\| < 0.025** | **\|difference\| ≥ 0.025** |
| **L-c** | *Reported, not adjudicated.* **What reading the two rows needs** | §7's readings: the first-listed rate and `d` overall; on B-d's two sides and on the pairs with no strictly better rule, under both definitions; by batch; by queue pair; by the breadth of the rule listed first; on Stage C. `L-b`'s split into parse failures and the rest, and the retries. On `L-a`'s queue pair, how often the answer names the better rule | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-05)**

**Standard errors, and the thin label.** `L-a`'s and `L-b`'s are the unpooled
error of a difference of two shares. **A verdict within one standard error of its
line is labelled *thin* beside it, and the label does not change the verdict.**
If either slot of `L-a`'s queue pair holds fewer than 20 declared answers, it is
unadjudicable and says so.

**Why `L-a`'s line is 0.20.** Three readings of the effect predict different
values on a pair the proposer splits evenly, and 0.20 separates the third from
the other two.

- **A uniform pull.** The pull calibrated on §15's two rates is half the gap
  between their log-odds, about 0.30. On a pair the proposer is truly undecided
  about, it gives a `d` of about 0.15.
- **A split by content.** If the proposer sends each ticket where its content
  says, the slot has little left to decide and `d` falls towards 0.
- **A tiebreaker.** If the proposer falls back on the rule listed first when it
  cannot decide, `d` rises well above 0.15.

So a hold says the slot decides more where the proposer is undecided than a
uniform pull would. A refutation says the pull is uniform, or the content
decides.

**Why `L-b`'s line is 0.025.** 121 of the 1,600 rows yielded no edge. At that
rate the error of the difference is about 0.013, so 0.025 is about two errors.
No effect at all would hold about nineteen times in twenty, and an effect of
three points would usually refute.

**Why `L-c` cannot carry a band.** Its readings say where the effect sits and
what the two rows need to be read. None has a line that would change a
conclusion, and Stage C's is already published by the erratum.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the records publish.** Everything `STATUS.md`, `IDEAS.md`,
  `PAIRWISE_WRITEUP.md` and §§11–15 of `FINDINGS3.md` publish, and Stage C of
  `results2/FINDINGS2.md`. And the erratum to §15, which the drafter wrote on
  2026-10-05: the arithmetic, the floor, Stage C's 84 of 166, and the confound.
- **The records' published blocks.**
  - `results3/answer_asymmetry.json`, whole.
  - `results3/edge_direction_1600.json`'s position block: 801 of 1,479, and the
    direction rate by where `rule_a` was listed, 0.7143 and 0.7473.
  - `results2/pair_judgement_hidden.json`'s three breakdowns.
  - `results2/pair_sample_1600.json`'s B-d split and its census of verdicts.
  - The 1,600 record's counts of answers by kind and **its per-queue-pair counts,
    which is where §2.1's selection comes from**.
- **The records' format.** Their top-level keys, an answer row's keys, the
  prompt, one question's text, and the fields of one entry of the truth.
- **What the 121 rows with no edge are.** 117 are parse failures: 35 among the
  400 reused answers and 82 among the 1,200 new ones. The other 4 parsed without
  an action, and none named a third queue. The values `attempts` takes, 1 to 3,
  but not how often.
- **The blocking checks' output** (§6), which prints pass or fail and figures
  already published.
- **The code.** `rung2/pair_judgement.py`, its prompt and its deal included;
  `rung3/answer_asymmetry.py`; `rung3/edge_dropping.revealed_ranking`; `edges/`;
  `reuse/plan.py`.
- **Not seen, because nobody has computed them**:
  - any slot split on any queue pair;
  - `d` or the first-listed rate on any subset but §15's split and Stage C;
  - the share with no edge, or the retries, by slot;
  - anything of `L-c`.

**What the drafter expects, written down so the scoreboard can score it.** Both
hold. **The drafter trusts `L-a` least.**

- **`L-a`.** The pair the proposer splits evenly is one the truth splits too: it
  is on B-d's unreachable side under both definitions. So the even split could be
  content, the proposer tracking which tickets go where, or the slot deciding a
  tie. About two fifths of the declared answers sit on queue pairs the proposer
  answers the same way nine times in ten or more. There the slot can decide
  almost nothing, so the overall floor of about 0.09 has to sit on the rest. The
  literature on position bias in model judges finds it on close calls. The
  drafter expects `d` near 0.25. A split by content would put it near 0, which
  is why this is the row trusted least.
- **`L-b`.** 117 of the 121 rows with no edge are parse failures: a matter of the
  answer's form, not its choice. Nothing in the records suggests the slot reaches
  that far.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 21
of 49 adjudicated rows came out refuted. The last thread's drafter expected all
three of its rows to hold, and one did. **These bands are more likely too
comfortable than too strict**, and the signature can tighten them, as it did
`A-b` and `A-d`.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls.

**Already paid for, and read as they stand:**

- `results2/pair_judgement_1600.json`, the 1,600 answers. 400 of them are Stage
  D's of `PLAN_PAIRWISE.md`, reused, and 1,200 were asked by
  `PLAN_PROPOSER_1600.md`'s Stage B.
- `results2/pair_judgement_learned.json`, Stage D's own record, which carries
  the deal of the 400.
- `results2/pair_judgement_hidden.json`, Stage C: the same prompt over the hidden
  policy's 170 pairs.
- `results2/pair_sample_1600.json`, the truth per pair under both definitions
  and B-d's split, computed before any call.
- `results3/edge_direction_1600.json` and `results3/answer_asymmetry.json`, read
  only for the figures `L-g1` reproduces.

**The truth** is read from `pair_sample_1600.json`, which carries it per pair.
No module of this plan imports the oracle.

---

## 2. The choices that have to be made at signature time

Three, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 `L-a`'s queue pair, chosen after reading the record's counts — the drafter recommends the one pair

The rule is the queue pairs with at least 30 declared answers whose majority
share is below 0.60. Over the record's own per-queue-pair counts it picks exactly
one, `SELF_SERVICE_DEFLECT vs T2_TECHNICAL`, at 86 against 82, and `L-g3` checks
that it still does. **The selection read the counts and no slot.** The
alternative is the three most evenly split pairs, adding two at 0.729. That has
more power and asks a different question, since those pairs have clear
majorities.

### 2.2 Parse failures count as rows with no edge — the drafter recommends counting them

117 of the 121 rows with no edge are parse failures. Without them `L-b` would
read four rows, which is no statistic. A parse failure is the only way this
record shows an answer gone wrong in form, and form is what `L-b` asks about.

### 2.3 The thread's name and letter

`PLAN_PRIMACY.md`, rows `L-a` to `L-c`, for the rule *listed* first. `P`, `F` and
`S` are taken. The naming is Sergi's to overrule.

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| the first-listed rate | 801 of 1,479, +3.20 | over the declared edges of the 1,600 answers | `results3/FINDINGS3.md` §11 and §15 |
| §15's split | 0.8534 (n 730), 0.7623 (n 749) | adherence to the proposer's own ranking, by where its favourite was listed | the same, §15 |
| the floor | +0.0911, se 0.026; 0.0832 without the ranking | a lower bound on the share of edges whose direction the slot decided | the same, §15, erratum of 2026-10-05 |
| Stage D | 197 of 365 | the first-listed rate at 400 | the same, §11 |
| Stage C | 84 of 166 | the same prompt over the hidden policy's pairs | the same, §15, erratum; `results2/pair_judgement_hidden.json` |
| B-d | 0.8647 (n 451), 0.6391 (n 654) | the direction rate where a ranking can and cannot answer, space definition | the same, §11 |
| `L-a`'s queue pair | 86 and 82 | its declared answers, by queue | `results2/pair_judgement_1600.json` |
| no edge | 121 of 1,600 | answers that declared no edge | the same |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** If a frozen file has a bug, stop
   and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise the loop.** Nothing here runs it.
4. **Seed 17, no regeneration, and every record this plan reads is read-only.**
5. **Do not adjust a prompt or a schema.** Nothing here touches either.
6. **If the numbers come out badly, report them.**
7. **No API key is needed**, and none is loaded.

And this plan's own, lettered:

A. **`rung2/pair_judgement.py`'s deal and `rung3/answer_asymmetry.py`'s
   functions are called, not copied.** A second deal that drifted from the first
   would check a randomisation that never happened.
B. **The records are inputs, never outputs.** Nothing under `results2/` or
   `results3/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §8 are fixed here and pinned by tests**, so that moving one
   after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow (§1).
F. **The dry run prints pass or fail and figures already published, never one of
   §0's.** `primacy/gates.py`, which it runs, does not reach the statistics of
   §0's rows, and a test checks that it does not.

---

## 5. Known traps

**5.1 — Position, label and the order of the queue names are one variable
here.** The rule listed first is always labelled `A`, and its queue is the first
queue the question names. No answer separates them. Whatever this plan finds
about the slot is about the three together.

**5.2 — Any gap is the first-listed rate restated.** That is the erratum to §15:
adherence to the ranking by where its favourite was listed is fixed by the
ranking's rate and the first-listed rate. So §0 states its rows on the slot
effect directly, never on adherence to a ranking fitted to the same answers.

**5.3 — The favoured queue, and why `L-b` reads rows with no edge.** A queue
pair's favoured queue is computed from its declared answers. A row with no edge
contributes nothing to it, so for `L-b` the favoured queue is exogenous. Read on
declared answers, adherence to the favoured queue by slot would be partly the
slot's own work, which is why no row reads it.

**5.4 — `d` is a lower bound, not the share.** The slot was dealt by a seeded
shuffle of a balanced list, which reads no rule (`L-g2`). So `d` estimates the
share of answers the slot pulled towards the first rule minus the share it pulled
towards the second. That is at most the share it decided. On one queue pair `d`
is the same whichever queue is the reference.

**5.5 — `d` is read on declared answers, a subset the slot could shape.** If the
slot changed which answers yield no edge, it would change `d`'s population.
`L-b` measures whether it does.

**5.6 — Where the proposer is unanimous, the slot decides nothing by
construction.** So comparing queue pairs by how evenly they split would be
circular: the split is partly the slot's own work. `L-a` reads one queue pair
against a fixed line instead. `L-c`'s readings by queue pair carry the same
caution, and say so.

**5.7 — Two batches, two dates, one model.** The 400 reused answers were given
on 2026-08-24 and the 1,200 on 2026-08-25. Each batch was dealt and balanced on
its own. The proposer is not deterministic at temperature 0. `L-c` reads each
batch.

**5.8 — The record's `parse_failures` counts calls, not rows.** Its 82 are the
failures of the 1,200 calls that run made. The 400 reused rows carry Stage D's
35, so the rows hold 117. `FINDINGS3.md` §11's table divides the 82 by 1,600.
That slip lies outside this plan's question and is reported, not corrected here.
`L-g1` reproduces each batch against its own record.

**5.9 — No edge is almost always a parse failure.** Of the 121, 117 are parse
failures and 4 parsed without an action; none named a third queue. `L-b` is
therefore about the answers' form.

**5.10 — Two definitions of the better rule, neither of them the layer order.**
Where `L-c` reads the truth it uses `rung3/edge_direction.py`'s definitions, the
rule right more often over the shared region on the space or on the corpus. It
reports both and picks neither.

---

## 6. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **L-g1 — The inputs.**
  - The suite is green.
  - The 1,600 record reproduces its own counts: answers by kind, parse failures
    per batch against each batch's record (§5.8), accepted edges, and the
    per-queue-pair counts.
  - The published position figures reproduce from its rows: 801 of 1,479, and
    §15's split, by `rung3.answer_asymmetry`'s own functions.
  - Stage C's breakdown by the winner's position reproduces from its rows.
  - The truth lines up with the answers row by row. B-d's split reproduces its
    published counts under both definitions, and its declared edges on each side
    on the space.
- **L-g2 — The deal.** Every slot is `winner_positions`' seeded deal and nothing
  else. The 1,200 new answers carry `winner_positions(1200)`. The 400 reused are
  Stage D's own rows, which carry `winner_positions(400)`. Stage C carries
  `winner_positions(170)`. **That is the premise of every lower bound here.** If
  any slot was not the shuffle, `d` is not what §5.4 says, and the plan stops.
- **L-g3 — The definitions.**
  - Each row's two rules send the ticket to different queues.
  - The rule listed first is `shown_as["A"]`, labelled `A`, its queue named
    first in the question (§5.1).
  - Every answer is consistent with the edge it declared.
  - §2.1's rule picks exactly `L-a`'s queue pair, with the record's split.
  - Every queue pair has a favoured queue, and the rows `L-b` counts apart are
    counted.
- **L-g4 — The signature**, §8.

> **[NOTE 2026-10-05] Run before signature, as the option Sergi chose that day
> provides: the plan, its package and its blocking checks. All three pass.**
> `PYTHONHASHSEED=0 python3 -m primacy.score --dry-run`, zero API calls, nothing
> written, 65 s, nearly all of it the suite. Without the dry run,
> `python3 -m primacy.score` exits at the gate in 0.05 s and creates no
> directory.
>
> - **`L-g1`.** The suite is green, 1,234 tests. The record reproduces its own
>   counts. 801 of 1,479 and §15's 623 of 730 and 571 of 749 reproduce, as does
>   Stage C's 75, 7 and 3 and 75, 9 and 1. The truth lines up. B-d reproduces
>   1,194, 481 and 713 on the space and 1,184, 308 and 876 on the corpus, and 451
>   and 654 declared.
> - **`L-g2`.** All 1,200, 400 and 170 slots are the deal.
> - **`L-g3`.** Every row is well formed. §2.1 picks the one pair, at 86 and 82.
>   No queue pair ties, and no row is counted apart.
>
> **Two things the checks found in the records, neither of which moves a band.**
>
> - **`parse_failures` counts calls.** The first draft of `L-g1` compared all the
>   rows' parse failures with the record's 82 and failed. That is §5.8.
> - **Four rows parsed without an action.** The first draft of `L-g3` called
>   them inconsistent. The code records such a payload with no answer and no raw
>   answer, so they are that, and §5.9 counts them.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0
> is touched.

---

## 7. The stage — scoring (free)

**Deliverable.** `primacy/score.py` → `results_primacy/score.json`, and
`results_primacy/FINDINGS_PRIMACY.md`, which owns every figure.

**What it does.** `L-g1` to `L-g4`, in that order and all blocking. Then:

- **`L-a`**: `d` on `L-a`'s queue pair, its error, and the answers in each slot.
- **`L-b`**: the share with no edge by the favoured rule's slot, its error, and
  the rows counted apart.
- **`L-c`**:
  - the first-listed rate overall, with twice it minus one, and `d` with
    `rule_a` and with the favoured rule as references;
  - under both definitions of the better rule, the first-listed rate and `d`
    with the better rule as reference, on B-d's reachable and unreachable sides
    and on all strict pairs; and the first-listed rate on the pairs with no
    strictly better rule;
  - by batch, the first-listed rate and `d`;
  - by queue pair, for every pair with at least 30 declared answers, its
    majority share, the first-listed rate and `d`, with §5.6's caution;
  - by whether the rule listed first is the broader or the narrower one, the
    first-listed rate, with equal extensions counted apart;
  - on Stage C, the first-listed rate and `d` with the winner as reference;
  - `L-b`'s rows split into parse failures and the rest, and the share of
    answered rows that needed a retry, by the favoured rule's slot;
  - on `L-a`'s queue pair, how often the answer names the better rule, under
    both definitions.

---

## 8. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money** ([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md)
§8): it is the order of events, that §0 was signed before any figure that could
inform it existed. The gate reads `PLAN_PRIMACY.md` and no other plan, and counts
signatures rather than stopping at the first. Every line starting
`**Signed by Sergi:` must be filled in, and there must be at least one. The
counting is `reuse/plan.py`'s, called with this plan's path. No flag skips the
gate; `--dry-run` runs `L-g1` to `L-g3` and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** The six records of §1. `N_ROWS = 1600`, `N_REUSED = 400`,
  `N_FRESH = 1200`, `N_HIDDEN = 170`, `POSITION_SEED = 17`.
- **`L-a`.** `L_A_QUEUE_PAIR = (SELF_SERVICE_DEFLECT, T2_TECHNICAL)`, picked by
  `L_A_SELECT_MIN_ROWS = 30` and `L_A_SELECT_BELOW = 0.60`;
  `L_A_MIN_SIDE = 20`.
- **The readings.** `READING_MIN_ROWS = 30`.
- **The two lines of §0.** `0.20` and `0.025`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
primacy/__init__.py
primacy/plan.py      the gate and the constants of this section
primacy/rows.py      the definitions of §0 and the statistics, pure functions
primacy/gates.py     L-g1 to L-g4
primacy/score.py     the stage: L-a, L-b, L-c
tests/test_primacy.py
results_primacy/score.json
results_primacy/FINDINGS_PRIMACY.md
```

**The plumbing, in the same commit as the modules.** Each of these lists has
drifted before when it was left for later:

- `primacy` joins `CODE_ROOTS` in `harness/provenance.py`, and the roots the
  oracle scan walks in `tests/test_oracle_separation.py`.
- `tests/test_writer_lists.py` names the new root.
- The README's table of writers gains `primacy/score.py`'s row.

**The list of modules allowed to see the oracle does not grow.**

---

## 9. Definition of done

- [ ] `results_primacy/score.json` with `_env`, produced with `PYTHONHASHSEED=0`
      from a clean tree.
- [ ] `L-g1` to `L-g4` passed before any record was written.
- [ ] The plumbing of §8, and tests pinning the constants of §8 and the
      definitions of §0; the whole suite green.
- [ ] Every figure in prose says whether the truth enters it, and if so under
      which definition.
- [ ] `results_primacy/FINDINGS_PRIMACY.md` owns every figure, with a dated
      erratum wherever it corrects something already published.
- [ ] `STATUS.md`:
  - the scoreboard gains the `L` thread, two adjudicated rows and one reported;
  - the position entry gets what the rows found, beside its erratum.
- [ ] `IDEAS.md`: the position item answered as far as these records go, and the
      paid follow-up of §10 carried with its price.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 10. What this plan cannot settle, declared before it runs

1. **Why the slot decides.** Position, label and the order of the queue names
   never come apart in an answer paid for (§5.1).
2. **The share the slot decides.** Only a floor is identified (§5.4). Each pair
   was asked in one order.
3. **Whether it costs accuracy on net.** The same reason.
4. **Other models, prompts and populations.** One model and one prompt. Stage C
   is the only other population, and its 166 answers cannot tell its rate from
   the learned base's.
5. **The paid follow-up, specified and not authorised.** It would take N of the
   1,600 pairs and re-ask each three ways:
   - **reversed**, the other rule listed first;
   - **again, unchanged**, as a control, because the model is not deterministic;
   - **relabelled**, the original order with the labels swapped, so the rule
     listed first is `B`.

   The hosted model now reasons by default, which `PLAN_REUSE.md` found on
   2026-09-30, so every call would turn reasoning off, as that plan's amendment
   did. What it would buy:
   - flips under reversal against flips in the control give the share the slot
     decides, not a floor;
   - the relabelled arm separates position from label;
   - the accuracy of answers that survive both orders against those that do not
     says what asking both orders is worth.

   At N = 400 that is 1,200 calls. That costs cents, and about six hours in
   Sergi's terminal at the August runs' 19 seconds a call. **It needs its own plan
   and signature; nothing here authorises it.**
