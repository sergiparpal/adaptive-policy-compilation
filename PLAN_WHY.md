# PLAN_WHY — what the proposer says it is doing, against what it does

**Status: drafted by Claude on 2026-10-05, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any held-out figure named here exists, in its own commit, staged by name.
Nothing here costs a call, and §8 says why the gate binds anyway.

**This plan exists because §15 of [`FINDINGS3.md`](results3/FINDINGS3.md) left the
proposer's own words unread.** Beside each pairwise answer the proposer wrote one
sentence, its `why`. §15 quoted one, *"La regla A es mas especifica..."*, and
noted that the proposer says it prefers the more specific rule while naming the
broader one 0.6038 of the time. It called that *one sentence and not a
measurement*: *a proper treatment of the why texts would be its own work*.
[`IDEAS.md`](IDEAS.md) carries it as *a real item nobody has opened*. Nothing in
the repository reads those sentences systematically.

**What it would change.** Two things the project has assumed and not measured.
- **Whether the proposer's account of its choice is true, and in what sense.** If
  "more specific" means fewer points of the space, the claim can be checked. If it
  means something else, the record should say what.
- **Whether the reason it gives tells its right answers from its wrong ones.** If
  it does, the `why` is a free filter for declared edges. If it does not, it joins
  the truth-free selections that §14 of `FINDINGS3.md` found no better than
  chance.

**None of its held-out figures exists**, so under
[`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable, although it
costs nothing.

**The design is development and held-out, and Sergi chose it on 2026-10-05.**
Coding text takes a codebook, and building one means reading text, which spends
whatever is read. So the codebook was built and frozen on a development set:
- the 365 `why` sentences of the 400 answers Stage D of `PLAN_PAIRWISE.md` paid
  for, answered on 2026-08-24;
- the 166 of Stage C, the hidden policy's pairs.

Every row of §0 is adjudicated on the 1,114 sentences of the batch answered on
2026-08-25, none of which the drafter has read. The alternatives, a codebook
written without reading anything and a post-run reading without a plan, were put
to Sergi and declined.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic and its denominator here, before any figure.**
Every row reads the held-out set: the 1,114 answers of the batch of 2026-08-25
that named one of their two rules, each with its `why`. **No surface applies to
`Y-a`, `Y-b` or `Y-c`**: they are properties of what was said and of the two
rules shown. `Y-d` reads the exhaustive space's definition of the better rule.

**Notation**, the codebook's (`why/codebook.py`, §8):

- **`spec`**: the sentence argues specificity, in Spanish, English or the Chinese
  forms the development set showed. More specific, more restrictive, more
  concrete, more conditions. **`count`** is the part of it that counts
  conditions explicitly.
- **The named rule** is the one the answer named. A `spec` sentence is read as a
  claim about it (§5.2).
- **Narrower**: the named rule matches strictly fewer of the space's 134,400
  points than the other.
- **More conditions**: it lists strictly more conditions in the question the
  proposer saw.
- **A categorical edge**: the named rule carries a categorical or exact condition
  the other lacks. Any one of three counts: a condition on `product` the other
  does not have; an exact severity where the other has a range; more `eq`
  conditions than the other.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **Y-a** | **When the proposer says the rule it names is more specific, the claim is true of the extension about half the time** | over the held-out answers coded `spec`: the share whose named rule is narrower | **0.45 ≤ share ≤ 0.62** | **< 0.45 or > 0.62** |
| **Y-b** | **Its specificity is not a count of conditions** | over the held-out answers coded `spec` and not `count`: the share whose named rule has more conditions | **< 0.33** | **≥ 0.33** |
| **Y-c** | **It is a categorical or exact condition the other rule lacks** | over the same answers: the share with a categorical edge, minus the same share over the held-out answers not coded `spec` | **≥ 0.15** | **< 0.15** |
| **Y-d** | **The reason it gives does not tell its right answers from its wrong ones** | over the held-out answers on pairs with a strictly better rule on the space: the share naming it among answers coded `spec`, minus the same share among answers not coded `spec` | **\|difference\| < 0.06** | **\|difference\| ≥ 0.06** |
| **Y-e** | *Reported, not adjudicated.* **What reading the four rows needs** | §7's readings: the census of codes, labels and languages; the direction rate by code under both definitions; the codes by B-d's side; the labels against the named rule; every `order` sentence and five quotations per code; every held-out row with its codes; the development figures beside them | — | — |

**Signed by Sergi: ________________________ (date: ______________)**

**Standard errors, and the thin label.** `Y-a`'s and `Y-b`'s are binomial; `Y-c`'s
and `Y-d`'s are the unpooled error of a difference of two shares. **A verdict
within one standard error of a line is labelled *thin* beside it, and the label
does not change the verdict.** A row with fewer than 50 answers in any of its
groups is unadjudicable and says so.

**Where the lines come from.** `Y-a` to `Y-c` were set from the development set,
Stage D's 365 answers, at about two standard errors from what that set measured,
counting the development set's error and the held-out set's. `Y-d` is a null:
its line is about two of the held-out difference's errors from zero.

- **`Y-a`.** If the claim were true of the extension, the share would sit near 1.
  If it were a word with no tie to the extension, it would sit at the share among
  all answers, 0.389 in development. Development measured 0.535, 92 of 172.
- **`Y-b`.** Development measured 0.252, 37 of 147. The share among all answers
  is 0.216, and among answers not coded `spec`, 0.088.
- **`Y-c`.** Development measured +0.263: 0.735 against 0.472.
- **`Y-d`.** Development measured −0.019: 0.688 against 0.707.

**What this design means for the scoreboard, declared before it counts.** These
are bands set on a development set from the same model and prompt, answered a
day apart. **They are bets that a reading generalises from 365 answers to 1,114,
not bets that test the drafter's foresight.** If nothing differs between the
batches, `Y-a` to `Y-c` each hold about nineteen times in twenty, `Y-d` about nine
in ten at the difference development measured, and all four together about
three times in four. `STATUS.md`'s scoreboard counts them like
any row. The record says beside each verdict that it was set on development.

**Why `Y-e` cannot carry a band.** Its readings say what the four rows need to be
read: which reasons the proposer gives, where, in which language, and what they
look like. None has a line that would change a conclusion.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the records publish**: everything `STATUS.md`, `IDEAS.md`,
  `PAIRWISE_WRITEUP.md`, §§11–15 of `FINDINGS3.md`, Stage C of
  `results2/FINDINGS2.md` and `results_primacy/FINDINGS_PRIMACY.md` publish.
- **Every development sentence, read in full**: Stage D's 365 and Stage C's 166.
  Each was read beside the slot of the named rule, whether it is the broader one
  and how many conditions each rule lists, and the development figures above
  were computed from them. They were read from the two records that hold nothing
  else, `results2/pair_judgement_learned.json` and
  `results2/pair_judgement_hidden.json`.
- **The held-out set's form, not its content**: 1,200 answers, 1,114 of them
  declared and every one with a `why`. It shares no pair with the development
  batch, and no sentence is truncated at the record's 280 characters.
- **The blocking checks' output** (§6), which prints pass or fail, counts the
  records publish and development figures.
- **Not seen, because nobody has computed them**:
  - any held-out sentence;
  - any held-out code, statistic or quotation;
  - anything of `Y-e` on the held-out set.

**What the drafter expects, written down so the scoreboard can score it.** All
four hold. **The drafter trusts `Y-d` least**: a null with a margin of two errors,
where a small real difference would be enough to refute it. Then `Y-a`, whose band
is two-sided.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls.

**Already paid for, and read as they stand:**

- `results2/pair_judgement_1600.json`: the 1,600 answers with their `why`. 400
  are Stage D's, reused, which is the development batch. 1,200 were asked by
  `PLAN_PROPOSER_1600.md`'s Stage B, and they are the held-out batch.
- `results2/pair_judgement_learned.json`: Stage D's own record, the development
  batch, which `Y-g1` checks against the 1,600 record row by row.
- `results2/pair_judgement_hidden.json`: Stage C, development too.
- `results2/pair_sample_1600.json`: the truth per pair under both definitions,
  and B-d's split.
- `results3/edge_direction_1600.json`: read only for `Y-g1`.

**The truth** is read from `pair_sample_1600.json`, which carries it per pair.
No module of this plan imports the oracle.

---

## 2. The choices that have to be made at signature time

Three, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 A `spec` sentence is read as a claim about the named rule — the drafter recommends it

In development every one of the 172 claims was about the rule the answer named,
which is what the sentence is for: it explains the choice. The alternative is to
count a claim only when the sentence names the named rule's label. That would
drop most of them, since 164 of the 365 development sentences name neither label.

### 2.2 `Y-d` reads the space's definition, and the corpus's goes to `Y-e` — the drafter recommends it

That is `B-a`'s and `W-b`'s choice. On the corpus, *better* is mostly the
security keyword's divergence between the two surfaces, which `PLAN_EDGES.md`
already measured. Development shows it again in `queue`'s direction rate: 0.663
on the space and 0.471 on the corpus. It is reported, not adjudicated.

### 2.3 The thread's name and letter

`PLAN_WHY.md`, rows `Y-a` to `Y-e`, for *why*. The naming is Sergi's to overrule.

---

## 3. Reference figures, with the record that owns each

Nothing here is produced by this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| names the broader rule | 0.6038 | over the 1,479 declared edges, by extension | `results3/FINDINGS3.md` §15 |
| follows its own ranking | 0.8073 | the same edges | the same |
| `H1`, specificity | refuted | breadth rides on the ranking | the same |
| the direction rate | 0.7312 (n 1105) | the 1,600 answers, space definition | the same, §11 |
| `B-d` | 0.8647 (n 451), 0.6391 (n 654) | where a fixed ranking can and cannot answer | the same, §11 |
| truth-free selection | within 0.7 deviations of chance | §14's dropping rules | the same, §14 |
| the slot | about one answer in twelve, at least | the share it decides | `results_primacy/FINDINGS_PRIMACY.md` |

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

A. **Every feature is read off what the proposer was shown**: the conditions as
   listed in its question, the extensions the record carries. Nothing it was not
   shown enters a row except the truth, in `Y-d` and `Y-e`.
B. **The records are inputs, never outputs.** Nothing under `results2/` or
   `results3/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The codebook is frozen.** Its fingerprint and the development figures it
   produces are pinned in §8 and by tests, so that an edit to a pattern after a
   held-out figure exists is visible in a diff and fails `Y-g3`.
E. **No module of this plan imports the oracle**, and the list of modules
   allowed to see it does not grow (§1).
F. **The dry run never codes a held-out sentence.** `why/gates.py` builds rows
   from the development set only, and a test watches every sentence handed to
   the codebook during the checks.

---

## 5. Known traps

**5.1 — Three languages, one codebook.** The prompt is Spanish. The development
sentences came back in Spanish 245 times, English 115 and Chinese 5 in Stage D.
Every pattern carries the Spanish and English forms, and the Chinese ones the
development set showed. A phrasing the codebook does not know escapes its code.
**The count orients and the quotation is the evidence**, as
`rung2/note_audit.py` puts it, so `Y-e` quotes as well as counts.

**5.2 — `spec` is read as a claim about the named rule.** §2.1. A held-out
sentence that called the *other* rule more specific would be miscounted. `Y-e`
quotes the `spec` sentences whose named rule is not the narrower, so a reader
can check what they say.

**5.3 — Three meanings of "specific", three references.** Extension is how much
of the space a rule matches, from the record's `extension_a` and `extension_b`.
Conditions are counted as listed in the question. The categorical edge is §0's
union of three features. `Y-a`, `Y-b` and `Y-c` read one each, and none of them
is the hidden policy's priority.

**5.4 — The categorical edge was built after reading development.** It is a
development finding, put together from what the sentences say: *"especifica
producto billing"*, *"severity 4 exacta"*. `Y-c` asks whether it holds on
sentences nobody has read.

**5.5 — `Y-d` is not accuracy against the layer order.** It reads the better rule
over the shared region, `rung3/edge_direction.py`'s definition, as every
direction rate since §9 of `FINDINGS3.md` has.

**5.6 — The two batches are alike, which is why the bands are likely to hold.**
One model, one prompt, a day apart. The slot effect was the same in both
(`results_primacy/FINDINGS_PRIMACY.md`). §0 declares what that means for the
scoreboard.

**5.7 — Labels are matched case-sensitively.** *"la atención"* is not rule `A`.
When a development sentence names one label only, it is the named rule's, all
144 times.

**5.8 — `prio` is a verb of conclusion, not a reason.** *"…so it takes
precedence"* follows a specificity argument as often as a security one. It is
counted and reported, and no row reads it.

**5.9 — Stage C is another population.** The hidden policy's pairs, read as
development, its figures declared in §8 and reported beside the held-out ones.
They are never pooled with the learned base's.

---

## 6. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **Y-g1 — The inputs.**
  - The suite is green.
  - The 1,600 record reproduces its own counts, by `primacy.gates.own_counts`.
  - Stage D's own record is the development batch of the 1,600 record, row for
    row, `why` included.
  - The truth lines up with the answers row by row, by
    `primacy.gates.truth_lines_up`.
- **Y-g2 — The split.** The development batch, Stage D's 400 answers, and the
  held-out batch, the 1,200, partition the 1,600 and share no pair. Stage C has
  its 170. It counts the answers each part has with a `why`, and reads none of
  the held-out ones.
- **Y-g3 — The codebook.** Its fingerprint is the one §8 pins. On the development
  set it reproduces every development figure §8 declares, for Stage D and for
  Stage C. **If either fails, the codebook is not the one §0 was drafted on**, and
  the plan stops.
- **Y-g4 — The signature**, §8.

> **[NOTE 2026-10-05] Run before signature, as the design Sergi chose that day
> provides: the plan, its package and its blocking checks. All three pass.**
> `PYTHONHASHSEED=0 python3 -m why.score --dry-run`, zero API calls, nothing
> written, 67 s, nearly all of it the suite. Without the dry run,
> `python3 -m why.score` exits at the gate and creates no directory.
>
> - **`Y-g1`.** The suite is green, 1,272 tests. The record reproduces its own
>   counts, Stage D's record is the development batch with every `why` equal,
>   and the truth lines up.
> - **`Y-g2`.** 400 and 1,200 answers, no pair shared. 365 development sentences,
>   166 of Stage C, and 1,114 held out, none of them read.
> - **`Y-g3`.** The codebook is `65e1732a08fd32c0`, and it reproduces every
>   development figure of §8, Stage D's and Stage C's.
>
> Written by the drafter before §0 was signed: no band moves and no row of §0 is
> touched.

---

## 7. The stage — scoring (free)

**Deliverable.** `why/score.py` → `results_why/score.json`, and
`results_why/FINDINGS_WHY.md`, which owns every figure.

**What it does.** `Y-g1` to `Y-g4`, in that order and all blocking. Then, on the
held-out set:

- **`Y-a` to `Y-d`**, each with its error and its groups' sizes, and the verdict
  with its thin label.
- **`Y-e`**:
  - the census of codes, labels and languages;
  - the shares among all held-out answers: narrower, more conditions,
    categorical edge, and the direction rate on both definitions;
  - the direction rate by code on both definitions, and `queue` against the rest
    on each;
  - the codes on B-d's two sides and on the pairs with no strictly better rule;
  - the labels against the named rule: its own only, the other's only, both,
    neither;
  - every `order` sentence, five quotations per code, and five `spec` sentences
    whose named rule is not the narrower;
  - every held-out row with its codes and features, and the development figures
    of Stage D and Stage C beside them.

---

## 8. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money** ([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md)
§8): it is the order of events, that §0 was signed before any held-out figure
that could inform it existed. The gate reads `PLAN_WHY.md` and no other plan, and
counts signatures rather than stopping at the first. Every line starting
`**Signed by Sergi:` must be filled in, and there must be at least one. The
counting is `reuse/plan.py`'s, called with this plan's path. No flag skips the
gate; `--dry-run` runs `Y-g1` to `Y-g3` and writes nothing.

**Constants fixed here, before any held-out figure exists, not to be tuned
afterwards and pinned by tests:**

- **The inputs and the split.** The five records of §1. The development batch
  `stage_d`, the held-out batch `this_run`: 400 and 1,200 answers, and Stage C's
  170.
- **The codebook.** `CODEBOOK_DIGEST = 65e1732a08fd32c0`, the fingerprint of
  `why/codebook.py`'s patterns.
- **The development figures `Y-g3` reproduces.**
  - Stage D: 365 sentences, coded `spec` 172, `count` 25, `queue` 130, `prio`
    170, `match` 42 and `order` 3. `Y-a` 92 of 172, `Y-b` 37 of 147, `Y-c` 108 of
    147 against 91 of 193, `Y-d` 95 of 138 against 99 of 140.
  - Stage C: 166 sentences, coded `spec` 44, `count` 1, `queue` 87, `prio` 78,
    `match` 10 and `order` 1. `Y-a` 21 of 44, `Y-b` 12 of 43, `Y-c` 30 of 43
    against 58 of 122, `Y-d` 40 of 44 against 110 of 122.
- **The four lines of §0.** `0.45` to `0.62`, `0.33`, `0.15` and `0.06`.
  `MIN_ROWS = 50`.
- **The readings.** `QUOTES_PER_CODE = 5`.

**The layout**, built before signature so that the checks could run first; the
naming is Sergi's to overrule:

```
why/__init__.py
why/plan.py        the gate and the constants of this section
why/codebook.py    the frozen codebook, pure functions
why/rows.py        the rows and §0's statistics, pure functions
why/gates.py       Y-g1 to Y-g4
why/score.py       the stage: Y-a to Y-d, Y-e
tests/test_why.py
results_why/score.json
results_why/FINDINGS_WHY.md
```

**The plumbing, in the same commit as the modules.**

- `why` joins `CODE_ROOTS` in `harness/provenance.py`, and the roots the oracle
  scan walks in `tests/test_oracle_separation.py`.
- `tests/test_writer_lists.py` names the new root.
- The README's table of writers gains `why/score.py`'s row.

**The list of modules allowed to see the oracle does not grow.**

---

## 9. Definition of done

- [ ] `results_why/score.json` with `_env`, produced with `PYTHONHASHSEED=0` from
      a clean tree.
- [ ] `Y-g1` to `Y-g4` passed before any held-out sentence was coded.
- [ ] The plumbing of §8, and tests pinning the constants of §8; the whole suite
      green.
- [ ] Every figure in prose says whether the truth enters it, and under which
      definition.
- [ ] `results_why/FINDINGS_WHY.md` owns every figure, the development ones
      included, with a dated erratum wherever it corrects something already
      published.
- [ ] `STATUS.md`:
  - the scoreboard gains the `Y` thread, four adjudicated rows and one reported,
    marked as set on development;
  - §15's one sentence on the `why` texts gets its measurement beside it.
- [ ] `IDEAS.md`: the item closed, and whatever this opens, added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 10. What this plan cannot settle, declared before it runs

1. **Whether the stated reasons cause the answers.** A `why` is written with the
   answer, and agreement between what it says and what the answer does is a
   correlation. Nothing here intervenes on the reason.
2. **Phrasings the codebook does not know.** §5.1. The quotations are there so a
   reader can see what was missed.
3. **Other models and prompts.** One model, one prompt.
4. **Why the slot decides.** The sentences name the chosen rule by its label, and
   the label is the slot (`results_primacy/FINDINGS_PRIMACY.md`). They cannot
   separate the two either.
5. **What a `why`-based selection does to the compiled order.** `Y-d` reads the
   pair level. Whether keeping or dropping edges by their stated reason moves the
   order is §14's question at the order level. It would be free, and it would
   need its own row.
