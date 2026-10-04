# PLAN_EDGES — what the edges declared at write time bought

**Status: drafted by Claude on 2026-10-05, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing is scored and
no record is written until Sergi has signed §0.** The signature has to land
before any figure named here exists, in its own commit, staged by name. Nothing
here costs a call, and §8 says why the gate binds anyway.

**This plan exists because the first declared edges with material were never
scored.** [`PLAN_REUSE.md`](PLAN_REUSE.md) ran rung 2's loop at n=2000, three
times. As the base grew it produced conflicts, and on them the proposer declared
priority edges: the engine accepted 30, 6 and 28
([`FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md), Stage C, point 5). They
are the first declared edges in this project to enter the graph of the loop that
produced them. Rung 2's eight n=100 runs had none accepted, and the pairwise
threads asked for edges offline, over rung 1's base, and compiled them into an
order. [`STATUS.md`](STATUS.md), *What is open*, item 2, says what is missing:
*what those edges buy has not been measured.* [`IDEAS.md`](IDEAS.md) carries it
under `PLAN_REUSE.md` and adds that it is free.

**What it would change.** `STATUS.md`'s headline says that of three ways of
supplying priority, the second — have the proposer declare it — *has been tried
in two forms and supplied almost none of it*. One of those forms is this one,
declaration at write time, and at n=100 it never had material. This plan scores
it with material, on the cases it decided. **None of its figures exists**, so
under [`EXTERNAL_REVIEW.md`](EXTERNAL_REVIEW.md) §5.6 it is pre-registrable,
although it costs nothing.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every row names its statistic and its denominator here, before any figure.**
`W-a` and `W-c` are on the corpus: `generate_corpus(2000, seed=17)` in arrival
order, the cases of `results_reuse/run_n2000_r{1,2,3}.json`, where the edges
decided what they decided. `W-b` reads the exhaustive space, as `B-a` did,
because 29 of the 50 shared regions hold two arriving cases or fewer (§5.7).
`W-d` reports both surfaces.

**Notation.** For each Stage B run `r`:

- **`E_r`, the installed edges**: the edges `try_edge` returned `ok` for *and*
  entered into the declared graph. That leaves out the accepted edges that agree
  with subsumption, which `rung2/engine2.py` accepts without installing (§5.1).
- **`D_r`, the edge-decided cases**: the cases whose recorded outcome is ACTION
  and which the run's rebuild without its declared edges leaves in CONFLICT. The
  rebuild is `fidelity/replay.py`'s, called and not copied (`W-g2`).
- **`E` and `D`** are their unions over the three runs. **Every row is read
  pooled** (§2.1), and each run's own value is published beside it.

| id | claim | statistic, with its denominator | band | refuted by |
|---|---|---|---|---|
| **W-a** | **The edges bought more silent errors than right decisions.** On the cases they decided, they were wrong more often than right | over `D`: the share whose record row is `correct` | **< 0.50** | **≥ 0.50** |
| **W-b** | **Declared at write time, direction is a weaker signal than the pairwise question drew** | over the edges of `E` with a strictly better rule on the exhaustive space: the share whose declared winner is that rule. For an edge `W → L`, a rule's wins are the points of `ext(W) ∩ ext(L)` whose true action is its action, counted as [`FINDINGS3.md`](results3/FINDINGS3.md) §9 counts them. Ties, and edges where neither rule is ever right, are counted apart and outside the denominator | **< 0.60** | **≥ 0.60** |
| **W-c** | **At the decision level, the proposer's directions buy no more than a coin's** | the share of 2,000 coin draws whose right decisions over `D` are at least the proposer's. A draw points every edge of `E` by a fair coin and rebuilds each run with its births and the timing of its edges as recorded (§5.3) | **≥ 0.05** | **< 0.05** |
| **W-d** | *Reported, not adjudicated.* **What reading the three rows needs** | the census of §5.1; each row per run; `W-a`'s errors split into material and direction (§5.9); the oracle's and the inverted directions over `D`; `W-b` by the corpus definition; and each final base with and without its edges, on both surfaces | — | — |

**Signed by Sergi: ________________________ (date: ______________)**

**Standard errors, and the thin label.** `W-a`'s is clustered by the rule that
decided the case, its `winner_id`, because an edge decides its region in
clusters (§5.8). `W-b`'s is binomial over edges. `W-c`'s is the Monte Carlo
error of a share over 2,000 draws. **A verdict within one standard error of its
line is labelled *thin* beside it, and the label does not change the verdict.**
If fewer than 20 edges qualify for `W-b`, it is unadjudicable and says so.

**Why `W-b`'s line is 0.60 and not 0.50.** At a coin's line, a rate no one could
tell from a coin would hold. The pairwise question drew 0.6978 at 400 pairs and
0.7312 at 1,600, both on the space definition ([`FINDINGS3.md`](results3/FINDINGS3.md)
§9 and §11). 0.60 is about halfway between that and a coin. **The populations
differ**: those pairs were drawn from rung 1's 577 rules, and these are the pairs
the proposer chose to declare. So the row is read against 0.60 and nothing else.
The comparison explains where the line sits; it is not part of the claim.

**Why `W-d` cannot carry a band.** Part of it is figures the drafter has already
computed (below). The rest is diagnostics for reading `W-a` to `W-c`, not claims
of their own: the role `F-f` had.

**What the drafter had already seen, declared so that the signature is
auditable.**

- **What the records publish.** Everything `STATUS.md`, `IDEAS.md`,
  `PLAN_REUSE.md` and `FINDINGS_REUSE.md` publish. That covers the edges proposed
  and accepted per run, the `no_solapan` refusals, the CONFLICTs, and each run's
  e2e, silent error and proposal accuracy. `FINDINGS3.md` §9, and §11 through
  `STATUS.md`.
- **Two published figures that bear on this plan directly**, both in
  [`FINDINGS_FIDELITY.md`](results_fidelity/FINDINGS_FIDELITY.md), Stage A:
  - **The rebuild without edges departs on 37, 16 and 61 cases.** That is `D`'s
    size, so `W-a`'s denominator is known: 114.
  - **On its 47 conflict births, the proposer was right 20 times.** Its answer
    was always an action already on the screen, and 44 times the screen's
    plurality.
- **The records' format.** Their top-level keys, a row's, a rule's and the
  metrics block's, and the first entry of run 1's `edge_log`.
- **The code.**
  - `rung2/engine2.py`, `rung2/shadow2.py` and `rung2/proposers2.py`, v1's prompt
    included.
  - `fidelity/replay.py`, `fidelity/plan.py` and `reuse/plan.py`.
  - `rung3/edge_direction.py`'s definitions.
- **A truth-free scratch probe, run on 2026-10-05.** It is not in the tree and
  owns nothing. It read no `truth`, `truth_rule`, `correct`,
  `proposal_action_correct` or `correct_count`, and imported nothing that reaches
  the oracle. `W-d`'s census re-measures every figure below under the gate. A
  figure that does not reproduce is an erratum to this section, not a silent
  edit.
  - **Accepted is not installed.** Run 1 accepted 30 edges and installed 17; the
    other 13 agree with subsumption. Run 2: 6 and 6. Run 3: 28 and 27.
  - **All 50 installed edges join rules with different actions.**
  - **Birth screens.** In runs 1 and 2 every installed edge was born on a
    conflict screen (17 and 6). In run 3, 12 were and 15 were born on a coverage
    screen.
  - **Direction.** The newborn rule wins in 17, 6 and 18 edges. It loses in 0, 0
    and 9, all nine in run 3.
  - **Shared cases.** Corpus cases matched by both rules of an installed edge:
    1 to 18 per edge in run 1, 1 to 8 in run 2, and 0 to 14 in run 3, where 7
    edges share none. A conflict-born edge's count includes its birth ticket.
  - **Shared points.** Space points in the shared region: 200 to 16,800 in run 1,
    420 to 5,040 in run 2, 40 to 16,800 in run 3.
  - **The rebuild.** With its edges it reproduces every outcome and winner.
    Without them, every departure is an ACTION that becomes a CONFLICT: 37, 16
    and 61.
- **Not seen, because nobody has computed them**:
  - any label on `D`, or on a shared region, on either surface;
  - any rule's correct count;
  - any coin, oracle or inverted rebuild;
  - any static reading of the final bases.

**What the drafter expects, written down so the scoreboard can score it.** All
three hold. **The drafter trusts `W-b` least, then `W-c`.**

- **`W-a`.** At a conflict birth the newborn takes the model's answer, right 20
  times in 47. Later cases in the region are decided by that same action. The
  base the edges sit in is right 0.41 to 0.52 of the time it decides, by run.
  Contested regions are where the material problem lives: in the pairwise
  sample, pairs where neither rule is ever right were 17% to 23%. A share near
  0.40 is the expectation. The way it goes wrong is run 3, the run that decides
  best, which carries 61 of the 114 cases.
- **`W-b`.** At conflict births the model took its screen's plurality action 44
  times in 47. That is a vote over rules it wrote itself, not a judgement about
  the region two of them share. The expectation is a rate near a coin. With an
  error near 0.08 on fewer than fifty edges, 0.60 is a little over one deviation
  above it.
- **`W-c`.** To sit above 95% of coins, the proposer's direction would need to be
  right on about two thirds of the clusters where direction matters at all. The
  drafter expects about half.

**The drafter's record argues against comfort.** On `STATUS.md`'s scoreboard 19
of 46 adjudicated rows came out refuted. The last two threads' drafter expected
four holds of five, then five of five, and called three and then four of the five
rows right. Three expected holds out of three is the profile that has gone wrong
before. **These bands are
more likely too comfortable than too strict**, and the signature can tighten them,
as it did `A-b` and `A-d`.

---

## 1. What is being bought, and what is already paid for

**Nothing is bought.** Zero API calls.

**Already paid for, and read as they stand**: `PLAN_REUSE.md`'s three Stage B
records, `results_reuse/run_n2000_r{1,2,3}.json`. They hold every rule with its
birth and the edges it declared there, the whole `edge_log` in the order
`try_edge` met it, and one row per case with its label. **Every corpus label this
plan reads comes from them.**

**The space labels** come from `rung3.order_search_ls.space_truth_masks`, the
route `rung3/edge_direction.py` takes. That module is on the list of those
allowed to see the oracle, and no module of this plan imports the oracle itself.

---

## 2. The choices that have to be made at signature time

Three, and none moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

### 2.1 Pooled, not the median of three runs — the drafter recommends pooled

`PLAN_REUSE.md` and `PLAN_FIDELITY.md` read most rows on the median of the three
runs. Here run 2 has 6 installed edges and 16 edge-decided cases. Its value would
be noise, and it could be the median. Each row is about one instrument,
declaration at write time, not about three bases. That is the reason `F-a` was
read pooled, and it applies here. **The cost is declared in §5.6**: pooled, run
3 carries more than half of every denominator.

### 2.2 2,000 coin draws

The number `FINDINGS3.md` §9 sharpened its null to. Each draw rebuilds three runs
of 2,000 cases, and only `D`'s 114 cases are scored. Minutes.

### 2.3 The thread's name and letter

`PLAN_EDGES.md`, rows `W-a` to `W-d`, for *written*. `E` would have read as Stage
E of `PLAN_PAIRWISE.md`, which is about the same act — declaration at write time
— imposed rather than optional, and is a different plan. The naming is Sergi's
to overrule.

---

## 3. Reference figures, with the record that owns each

All on the corpus unless the row says otherwise. Nothing here is produced by
this plan.

| figure | value | what it is | owning record |
|---|---|---|---|
| edges proposed / accepted | 33/30, 6/6, 36/28 | per run; the rest refused as `no_solapan` | `results_reuse/FINDINGS_REUSE.md`, Stage C, point 5 |
| CONFLICT outcomes | 30, 5, 12 | per run, `U-e`'s statistic | the same, Stage C |
| silent error | 0.5939, 0.5531, 0.4760 | per run, over the cases the rules decided | the same, Stage C |
| the rebuild without edges | 37, 16, 61 | cases departing, per run: `D`'s size | `results_fidelity/FINDINGS_FIDELITY.md`, Stage A |
| conflict births | 47; 20 right | the answer always on the screen, the plurality 44 times | the same, Stage A |
| the pairwise direction rate | 0.6978; 0.7312 | 400 and 1,600 pairs of rung 1's base, space definition | `results3/FINDINGS3.md` §9 and §11 |
| neither rule ever right | 17%, 23% | of the 400 pairs, space and corpus | `results3/FINDINGS3.md` §9 |
| `T2_TECHNICAL` on the space | 36,720 points | the per-class size `W-g1` checks the space labels against | `results3/FINDINGS_ORDERS.md`, part four |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering, so that cross-references point at the right rule.

1. **Do not modify the frozen specification.** If a frozen file has a bug, stop
   and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** Every rebuild is sequential over the 2,000 cases,
   because a rule's birth and its edges change every later decision.
4. **Seed 17, no regeneration, and every record under `results_reuse/` is
   read-only.**
5. **Do not adjust a prompt or a schema.** Nothing here touches either.
6. **If the numbers come out badly, report them.**
7. **No API key is needed**, and none is loaded.

And this plan's own, lettered:

A. **`engine2`, `proposers2`, `shadow2` and `fidelity/replay.py` are called,
   not copied.** A second rebuild that drifted from the one `F-g2` checks would
   score a base that never existed.
B. **The Stage B records are inputs, never outputs.** Nothing under
   `results_reuse/` or `results_fidelity/` is written by this plan.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0` set explicitly.
D. **The constants of §8 are fixed here and pinned by tests**, so that moving one
   after a figure exists is visible in a diff.
E. **No module of this plan imports the oracle**, and the list of modules allowed
   to see it does not grow (§1).
F. **The dry run prints pass or fail and figures already published, never one of
   §0's.**

---

## 5. Known traps

**5.1 — Accepted is not installed.** `engine2.try_edge` returns `ok` for an edge
whose winner's extension sits strictly inside the loser's, *redundant but
consistent*, and installs nothing: subsumption already decides that pair the same
way. `metrics.edges_accepted` counts those edges, and the rules' `beats` and
`loses_to` lists carry them. Of 64 accepted edges, 14 are of that kind. They are inert, and
they are outside every row. `W-d`'s census publishes the split.

**5.2 — An edge can only turn a CONFLICT into a decision, so e2e cannot be the
reading.** It removes rules from the undefeated set. That never adds an action,
and in an acyclic graph never empties the set. So with its edges a case decides
the same action, or decides where it was a CONFLICT. `W-g2` checks that this is
what the records show. In the shadow's accounting an escalation is never a
correct decision. So every edge can only add to e2e, and can only add silent
errors. **What the edges buy is the share right on what they decide**, which is
`W-a`.

**5.3 — First order, not the trajectory.** In the run, an edge-decided case did
not escalate, so no rule was born there. Without the edge it would have
escalated, the model would have written another rule, and every later case could
differ. **Every rebuild here keeps the births and the timing of the edges as
recorded**, and changes only what the edges in force decide. It measures what the
edges decided. It does not measure what the loop would have done without them,
which would take calls (§10). A case the record escalated stays an escalation in
every arm, even where a coin draw would have decided it, and is outside every
row.

**5.4 — The birth ticket is never in `D`.** It sits in the shared region of every
edge born on a conflict screen, and it escalated.

**5.5 — Seven edges can decide nothing on the corpus.** In run 3 seven installed
edges share no arriving case. They enter `W-b`, which reads the space, and decide
none of `D`.

**5.6 — One run dominates the pool.** Run 3 carries 61 of `D`'s 114 cases and 27
of `E`'s 50 edges. Each row's per-run values are published beside the pooled one,
and the reading says whether the pooled value is run 3's.

**5.7 — On the corpus, *better* is mostly undefined.** 29 of the 50 shared
regions hold two arriving cases or fewer, birth ticket included, and seven hold
none. So the corpus definition of the better rule is mostly ties, or one case
against none. That is why `W-b` reads the
space. The corpus definition is reported in `W-d`. Neither definition is the
hidden policy's layer order. Both ignore third rules that defeat the pair over
part of its region, exactly as `FINDINGS3.md` §9's did.

**5.8 — Decisions cluster.** One edge decides every arriving case in its region
that no other rule settles, so `D`'s 114 cases are not 114 independent draws. A
binomial error would overstate how much they say. `W-a`'s error is clustered by
`winner_id`. `W-c` needs no such correction: its null redraws the clusters with
the edges.

**5.9 — Two kinds of wrong, and only one is direction.** On a case of `D`, the
contending actions are those of the undefeated set that the rebuild without edges
returns. If the true queue is none of them, no direction could have been right:
that is the material problem of `FINDINGS3.md` §2, inside the conflict. If it is
one of them, the edge chose another: a direction error. `W-d` splits `W-a`'s
errors that way, and publishes the share of `D` where any direction could have
been right, which is the ceiling for the oracle's arm.

**5.10 — A flipped edge can close a cycle.** The coin's rebuild calls `try_edge`
in `edge_log` order with the drawn direction, so a draw that would close a cycle
is refused, as the engine would refuse it. Each draw's refusals are counted and
published.

---

## 6. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**.

- **W-g1 — The inputs.**
  - The suite is green.
  - Rung 2's engine executes the hidden policy at 1.0000 on the corpus and on
    the space. Both ceilings are measured in memory, `U-g1`'s method, without
    rewriting their records.
  - Each Stage B record reproduces its own metrics, fire counts, births and
    corpus labels: `F-g1`'s check, called.
  - The space labels partition the 134,400 points and give `T2_TECHNICAL` its
    published 36,720.
- **W-g2 — The rebuild, with and without the edges.** With its edges, each run's
  rebuild reproduces its record exactly: `fidelity.replay.check`, `F-g2`.
  Without them, every departure is an ACTION that becomes a CONFLICT, and none is
  anything else. **That is the premise of `D` and of §5.2.** If an edge could
  change an action or undo a decision, `W-a`'s population would not be what §0
  says, and the plan stops.
- **W-g3 — The counterfactual rebuild is the identity where it should be.**
  - Given the declared directions, it reproduces the record's outcome, winner
    and action on every case. So on `D` it decides what the record decided, and
    `W-c`'s count for the proposer is `W-a`'s numerator by construction. The
    stage asserts that equality before it reads a verdict. The dry run never
    reads a label of `D`.
  - Given no installed edge, it reproduces `W-g2`'s rebuild without edges.
  - The coin's first draws decide `D` identically under two values of
    `PYTHONHASHSEED`, by `tests/hashseed_child.py`'s method.
- **W-g4 — The signature**, §8.

> **[NOTE 2026-10-05] Run before signature, with Sergi's leave, and all three
> pass.** `PYTHONHASHSEED=0 python3 -m edges.score --dry-run`, zero API calls,
> nothing written, 70 s.
>
> - **`W-g1`.** Corpus and space at 1.0000, and the suite green. The three
>   records reproduce themselves. The space labels partition the space, with
>   `T2_TECHNICAL` at 36,720.
> - **`W-g2`.** Each run rebuilds exactly. Without its edges it departs only
>   from ACTION to CONFLICT, on 37, 16 and 61 cases.
> - **`W-g3`.** The counterfactual rebuild is the identity on the three runs.
>
> **Two details of method and one addition, none of which moves a band:**
>
> - **Three hash seeds, not two.** `W-g3` compares the coin under 0, 1 and 2,
>   beside a witness that does depend on the hash and changes between them, as
>   `tests/test_order_determinism.py` does.
> - **No duplicates.** `W-g3` also refuses an accepted edge over a pair already
>   installed: a third kind that §5.1 does not name. It finds none, so every
>   accepted edge is installed or consistent with subsumption.
> - ***Never reads a label of `D`*, said precisely.** `W-g1` compares each
>   record's labels with those the frozen loop writes, case by case, which is
>   `F-g1`'s check, and prints pass or fail. No figure is computed from them.
>
> **Timed without reading a label.** The stage's 2,000 coin draws take 2 to 7 s
> a run, and a final base over the whole space 1 to 2 s, so §2.2's *minutes*
> is seconds. The hash check's two constants, three seeds and 25 draws, decide
> no figure. Neither the dry run nor the timing printed anything §0 does not
> already declare. Written by the drafter before §0 was signed: no band moves
> and no row of §0 is touched.

---

## 7. The stage — scoring (free)

**Deliverable.** `edges/score.py` → `results_edges/score.json`, and
`results_edges/FINDINGS_EDGES.md`, which owns every figure.

**What it does.** `W-g1` to `W-g4`, in that order and all blocking. Then, per
run and pooled:

- **The census**: §5.1's split, and the birth screen, direction and shared
  cases and points of every installed edge.
- **`W-a`**: `D`'s share right, with its clustered error.
- **`W-b`**: the better rule of every installed edge over the space, the share
  declared towards it, and the ties and *neither* counted apart.
- **`W-c`**: the proposer's right decisions over `D` against 2,000 coin draws,
  and the inverted and oracle arms beside them. The oracle arm points each edge
  at `W-b`'s better rule where there is one, and as declared where there is not.
- **The rest of `W-d`**: §5.9's split, the corpus definition of `W-b`, and each
  final base with and without its edges, on the corpus and on the space. That
  last reading is the final base as a machine, deciding every case at once, not
  the run. It says so beside every figure.

---

## 8. The gate, and where the code lives

**Every module of this plan that writes a record refuses while §0 is unsigned**,
before it measures, builds or writes anything. **A free stage gets the gate
because what the gate protects is not money** ([`PLAN_SENSITIVITY.md`](PLAN_SENSITIVITY.md)
§8): it is the order of events, that §0 was signed before any figure that could
inform it existed. The gate reads `PLAN_EDGES.md` and no other plan, and counts
signatures rather than stopping at the first. Every line starting
`**Signed by Sergi:` must be filled in, and there must be at least one. The
counting is `reuse/plan.py`'s, called with this plan's path. No flag skips the
gate; `--dry-run` runs `W-g1` to `W-g3` and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:**

- **The inputs.** `RUNS = (1, 2, 3)`, `N = 2000`, `SEED = 17`.
- **The null.** `COIN_DRAWS = 2000` and `COIN_SEED = 47`, one string-seeded
  stream per run, so no draw depends on `PYTHONHASHSEED`.
- **`W-b`'s minimum.** `MIN_QUALIFYING_EDGES = 20`.
- **The three lines of §0.** `0.50`, `0.60` and `0.05`.

**Drafter's proposal for the layout; the naming is Sergi's to overrule:**

```
edges/__init__.py
edges/plan.py      the gate and the constants of this section
edges/rebuild.py   the counterfactual rebuild of W-c, over fidelity/replay.py
edges/gates.py     W-g1 to W-g4
edges/score.py     the stage: W-a to W-d
tests/test_edges.py
results_edges/score.json
results_edges/FINDINGS_EDGES.md
```

**The plumbing, in the same commit as the modules.** Each of these lists has
drifted before when it was left for later:

- `edges` joins `CODE_ROOTS` in `harness/provenance.py`, and the roots the oracle
  scan walks in `tests/test_oracle_separation.py`.
- The guarded writers in `tests/test_writer_lists.py` gain `edges/score.py`.
- The README's table of writers gains its row.

**The list of modules allowed to see the oracle does not grow.**

---

## 9. Definition of done

- [ ] `results_edges/score.json` with `_env`, produced with `PYTHONHASHSEED=0`
      from a clean tree.
- [ ] `W-g1` to `W-g4` passed before any record was written.
- [ ] The plumbing of §8, and tests pinning the constants of §8 and the
      definitions of `E` and `D`; the whole suite green.
- [ ] Every figure in prose names its surface, and every pooled figure has its
      runs beside it.
- [ ] `results_edges/FINDINGS_EDGES.md` owns every figure, with a dated erratum
      wherever it corrects something already published.
- [ ] `STATUS.md`:
  - the scoreboard gains the `W` thread, three adjudicated rows and one
    reported;
  - *What is open*, item 2, gets its answer;
  - the headline's second clause, whichever way the rows come out, says which
    forms have been tried — and this is the first of them, scored with material
    for the first time.
- [ ] `IDEAS.md`: *What the accepted edges buy*, under `PLAN_REUSE.md`, closed,
      and whatever this opens, added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, record and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 10. What this plan cannot settle, declared before it runs

1. **The trajectory.** What the loop would have done without its edges —
   escalated those cases, had the model write other rules, decided later cases
   differently — needs the loop re-run with edges disabled, which costs calls
   and gives different draws (§5.3).
2. **What escalating would have bought instead.** Without its edges, a case of
   `D` would have reached the model on a conflict screen. What the model would
   have answered there is not in any record. `PLAN_FIDELITY.md`'s answers were
   asked with every matching rule hidden, which is a different prompt, so they
   are not that counterfactual and are not read here.
3. **One model, one prompt, three draws.** v1 tells the proposer to declare only
   against rules that overlap its own without containing it, and leaves it free
   not to. **What imposed declaration would buy is Stage E's question** (§11 of
   [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md)), not this one.
4. **The material problem.** No direction fixes a case whose true queue is
   neither contending rule's. §5.9 measures how much of `W-a` that is; it does
   not touch it.
5. **The layer order.** Neither definition of the better rule is the hidden
   policy's priority (§5.7). A direction counted right here means right more
   often over the shared region, and nothing more.
