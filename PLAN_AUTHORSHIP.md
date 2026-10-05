# PLAN_AUTHORSHIP — Stage E: the discipline of authorship, imposed at write time

**Status: drafted by Claude on 2026-10-05, unsigned.** Under hard rule 2 of
`CLAUDE.md` a model may draft a band and may not sign it. **Nothing runs and no
record is written until Sergi has signed §0**, and the signature has to land
before any figure named here exists, in its own commit, staged by name. Stage B
spends. Stages A and C do not, and §11 says why the gate binds them anyway.

**This plan exists because one form of the project's second way has never been
run.** `STATUS.md` names three ways of supplying the priority of a stratified
policy: infer it from the syntax of the rules, have the proposer declare it, or
learn it from observed behaviour. The second has been tried in two forms.
Declaration *offered* at write time, which rung 2's v1 prompt allows and
`PLAN_REUSE.md` ran at n=2000, and declaration *asked for* pair by pair, which
the pairwise threads ran at 400 and 1,600 pairs. **The third form, declaration
*imposed* at write time, is Stage E of [`PLAN_PAIRWISE.md`](PLAN_PAIRWISE.md)
§11**, proposal P3 of [`ARBITRATION_REPORT.md`](ARBITRATION_REPORT.md) §7. It
has a specification, two predictions written in August and no signature. Its
idea: *the validator rejects a rule that overlaps another without declaring
whether it is an exception to it or a default under it.*

**Its baseline was measured first, and it changed what Stage E can test.**
[`results_reuse/FINDINGS_REUSE.md`](results_reuse/FINDINGS_REUSE.md), *The three
bases, read for Stage E*, read `PLAN_REUSE.md`'s three final bases, the loop
Stage E would modify. Three of its findings reshape this plan.

1. **P3's second prediction has nothing to measure on this loop.** It promised
   that the 0.047 gap between the hybrid and pure coverage bounds would narrow.
   On these bases the gap is zero, or 0.0005, on the corpus, and at most 0.006
   over the space. **It is not carried as a row.**
2. **The room for an order is over the function, not where tickets arrive.** On
   the corpus, subsumption alone already sits within 0.01 to 0.04 of what any
   order over its pool could reach. Over the space it sits 0.19 to 0.46 below
   it. **The row that asks whether declaration supplies order is read over the
   space**, and the corpus is reported beside it.
3. **The proposer declared priority on copies.** v1 answers every escalation
   with a rule that must match the ticket, and it has no way to order two rules
   already in the base. So on a CONFLICT the proposer rewrote the rule it wanted
   to win and hung the edge on the copy: 35 of the 64 accepted edges arrived
   that way. **A discipline imposed on that protocol would travel on copies
   too**, so §5 gives it a vehicle and refuses copies.

**What it would change.** If declaration imposed at write time orders what
subsumption leaves, the second clause of `STATUS.md`'s headline changes: the
second way would have supplied priority in its third form, on the surface where
an order has room. If it does not, the second way has been tried in all three
forms, and the clause stands on that surface too. **Either way the rows
also say whether the discipline changes the base itself**, its nesting and the
soundness of subsumption over it, which is what P3 was written to buy.

---

## 0. Predictions — bands and refutation lines

Drafted, unsigned. One row is one event. **A band's edge is its own refutation
line**, so band and refutation partition the axis and nothing can fall between
them.

**Every adjudicated row is read on the median over the `R` runs of Stage B**,
each run's own value published beside it. **Every row names its surface.** The
final bases are read as `reuse/structure.py` reads `PLAN_REUSE.md`'s: whole,
from case 0, every rule present. The baseline beside each row is that module's
reading of `PLAN_REUSE.md`'s three bases, and every line below is set against it.

| id | claim | statistic, and surface | band | refuted by |
|---|---|---|---|---|
| **E-a** | **The discipline nests the base**: made to place every rule it writes, the proposer writes exceptions inside the rules they override | nested pairs over all pairs, `reuse/structure.py`'s `nested_share`, of each final base. Pairs carry no surface. Baseline median 0.0160 over distinct rules, the comparison, since v1e refuses copies; 0.0194 with them | **≥ 0.05** | **< 0.05** |
| **E-b** | **Subsumption becomes sound at the same coverage**: P3's first prediction, re-anchored to this loop | subsumption alone over each final base, **full corpus**: its silent error, and its coverage. Baseline medians 0.5521 and 0.966 | **silent error ≤ 0.45 and coverage ≥ 0.90** | **silent error > 0.45, or coverage < 0.90** |
| **E-c** | **Imposed declaration orders what subsumption leaves, over the function** | the share of the order's room the installed edges fill, **exhaustive space**: (end to end with every installed edge − end to end of subsumption alone) / (hybrid bound − end to end of subsumption alone), on each final base. Baseline 0.3000, 0.3833 and 0.7806, median 0.3833 | **≥ 0.50** | **< 0.50** |
| **E-d** | **Made to declare against every rule it overlaps, the proposer contradicts subsumption** | `contradice_subsuncion` verdicts, pooled over the runs. In every run the repository has made, this count is zero | **≥ 1** | **0** |
| **E-e** | *Reported, not adjudicated.* What the rows rest on, and what they could hide | per run, beside the baseline: E-c on the full corpus; E-a to E-c with the edges of each channel alone (§5.3); the online figures of the loop, `PLAN_REUSE.md`'s set; calls, repair rounds and rejections by reason; overlap among distinct rules, and born rules that overlap nothing; declarations by verdict; `ONCALL_ESCALATION` and `SECURITY_INCIDENT` escalations | — | — |

**Signed by Sergi: Sergi Parpal (date: 2026-10-05)**

**Why E-c is a share and not a score.** A final base written under another
protocol is another base, and its end to end mixes what its rules carry with how
they are ordered (`CHAT_SUMMARY.md` §4, erratum (c): figures do not travel with
a new base). The share divides what the installed edges add over subsumption
alone by what an order over that base could add at most, and the hybrid bound is
a bound per case, not an attainable optimum, so the share is a floor. It reads
the declarations' contribution in the units of each base's own room. A room of
zero leaves the share undefined; if the median is undefined, E-c is
unadjudicable and the record says so.

**Why E-c is read over the space.** On the corpus the baseline's room is 22, 11
and 35 cases of 2,000, and a share over 11 cases is a coin. Over the space the
room is 0.19 to 0.46 of 134,400 points, and that is where the baseline's edges
did their work: +0.07 to +0.36 of end to end over the function against +0.004 to
+0.016 on the arrivals ([`results_edges/FINDINGS_EDGES.md`](results_edges/FINDINGS_EDGES.md)).
The corpus share is reported in E-e, and the record names the surface of every
figure.

**What the drafter had already seen, declared so that the signature is
auditable.** Everything `results_reuse/structure.json` publishes, which is every
figure of the baseline above, and the whole of `FINDINGS_REUSE.md`. From
`FINDINGS_EDGES.md`, each final base's end to end with and without its edges on
both surfaces; the three baseline shares of E-c were computed from that table
and `structure.json` while drafting, and `E-g2` recomputed them exactly before
signature, 0.3000, 0.3833 and 0.7806 over the space and 0.2326, 0.3636 and
0.4429 on the corpus (§7's note). And the baseline's nesting over
distinct rules, computed while drafting because the copies inflate it: 0.0160,
0.0277 and 0.0043, where the copies alone made 54 of run 1's 63 nested pairs.
`FINDINGS_FIDELITY.md`,
`FINDINGS_WHY.md`, `FINDINGS_PRIMACY.md`, and §§11 to 18 of
[`results3/FINDINGS3.md`](results3/FINDINGS3.md). The v1 prompt and the loop's
proposal path, `rung2/proposers2.py` and `rung2/shadow2.py`, read to write §5.
`ARBITRATION_REPORT.md` §§3, 5, 7, 8 and 9 and `CHAT_SUMMARY.md` §§3 and 4.
**Not seen, because nothing has produced them**: any answer to the protocol of
§5, any base it writes, and every figure of Stage B.

**What the drafter expects, written down so the scoreboard can score it.**
**E-c and E-d hold; E-a and E-b are refuted.** One line each.

- **E-c.** With a declaration on every overlap and a way to order rules already
  in conflict, most conflicts get an edge. The proposer's direction is right
  about three times in four over the function, 0.7556 at write time (`W-b`) and
  0.7312 pair by pair (`B-a`). The baseline's median share, 0.3833, came from 50
  installed edges.
- **E-d.** The discipline asks for a declaration on every nested pair, and one
  narrower rule called a default, once in three runs, holds the row. v1 told the
  proposer not to declare on nested pairs, which is where the verdict can fire.
- **E-a.** A declaration does not need nesting to work: an exception can overlap
  the rule it overrides without being inside it, and with an order answer
  available, a conflict needs no new rule at all. The proposer partitions
  (`FINDINGS2.md`), and nothing here asks it to stop.
- **E-b.** On the corpus subsumption already sits at what the rules allow, and
  `FINDINGS_FIDELITY.md` places most of their errors in the model itself (`F-d`).
  A discipline about how rules are placed does not change which queue the model
  picks.

**The drafter's record argues against trusting that.** On `STATUS.md`'s
scoreboard 22 of 55 adjudicated rows came out refuted, 22 of 51 without the `Y`
rows, whose bands were set on a development set. Its standing calibration note
says this drafter underestimates how violently a change of surface changes
things, and the third clause of `FINDINGS3.md` §17's expectation went wrong
exactly that way this week. The fourth of `reuse/structure.py`'s went wrong
another way: it missed a mechanism, the copies. **The row the drafter trusts
least is E-c**, which bets on the surface where the baseline's edges did best
and on a direction rate measured on other edges. Sergi should read these bands
as more likely too comfortable than too strict, and tighten them at signature if
he disagrees.

---

## 1. What is being bought, and what is already paid for

**Already paid for, and free to read: the baseline.** `PLAN_REUSE.md`'s three
runs, `results_reuse/run_n2000_r{1,2,3}.json`, and their reading in
`results_reuse/structure.json`. `E-g2` reproduces both before anything is bought.

**Bought: a smoke run and `R` runs of rung 2's loop over the 2,000 cases of seed
17, under the protocol of §5.** Everything else is `PLAN_REUSE.md`'s Stage B as
it ran: `rung2.engine2`, `deepseek/deepseek-v4-flash` with
`reasoning: {"effort": "none"}`, temperature 0, `max_tokens` 1,200, the same
retries, an empty base at the start of every run, and no run seeing another's
rules.

**Cost.** One call per escalation, one more per repair round (§5.2), and parse
retries. `PLAN_REUSE.md`'s three runs made 62, 31 and 42 escalations, 135 calls,
none failed. **How many this protocol makes is not known and cannot be
dry-run.** Rejected rules leave their region uncovered, and repair rounds add
calls, both of which push the count up. Order answers resolve conflicts, which
pushes it down. The drafter's estimate is two to three times the baseline, a few
hundred calls in all: cents at this model's price. **Time is the constraint.**
`PLAN_REUSE.md`'s run 1 took about thirty minutes, and a run here may take one to
two hours. **A run that long outlives a background command of the agent's
harness**, so Stage B's runs go in Sergi's terminal, with the key loaded as
`CLAUDE.md`'s rule 7 says.

---

## 2. The choices that have to be made at signature time

None of them moves a band. **Signing §0 adopts the drafter's choice in each
unless the signature line says otherwise.**

- **The order answer on a CONFLICT (§5.3): admitted, or not.** The drafter
  recommends **admitted**. Without it the discipline travels on copies, or, once
  copies are refused, on narrower rules written only to carry an edge. **The
  cost is purity**: ordering two rules that already conflict is deferred
  elicitation, P2 of `ARBITRATION_REPORT.md` §7, not authorship. E-e reports
  every row with each channel's edges alone, so the order answer's share is
  visible. Refusing it makes Stage E P3 and nothing else, and makes E-a more
  likely to hold and E-c less likely.
- **Repair rounds, `K`: 0, 1 or 2.** The drafter recommends **1**: one second
  chance, with the missing rules listed. At 0 a rule that misses one overlap is
  refused outright and the discipline mostly measures how often the proposer
  guesses the engine's overlap set. At 2 the worst case costs three calls per
  escalation.
- **`R`, the number of runs.** **3**, as `PLAN_REUSE.md`: the baseline is three
  runs, and three draws give a spread.
- **A control on the date.** `PLAN_REUSE.md`'s runs were asked on 2026-09-30.
  Three more v1 runs on the same day as Stage B would hold the model's date
  fixed, and double the cost. The drafter recommends **no**: `F-a` found the
  instrument unmoved between 2026-09-30 and 2026-10-04, at −0.0075.
- **`PREDICTION.md`.** Step 4 of `CLAUDE.md` puts Sergi's own prediction before a
  long run, and hard rule 2 keeps the model out of that file. This plan drafts no
  entry there and its gate does not look for one.

---

## 3. Reference figures, with the record that owns each

| figure | value | what it is | owning record |
|---|---|---|---|
| baseline, per run | §0 | `PLAN_REUSE.md`'s three final bases, read whole: nesting, subsumption alone, bounds, copies | `results_reuse/structure.json` |
| baseline end to end with edges | 0.3063, 0.2951, 0.5536 over the space; 0.4035, 0.4470, 0.5245 on the corpus | each final base with its installed edges | `results_edges/score.json`, tabled in `results_edges/FINDINGS_EDGES.md` |
| the copies and what they carried | 35 of 64 accepted edges | later copies, every one born on a CONFLICT | `results_reuse/structure.json`, `post_run` |
| the hand-written policy | nested 0.1502, subsumption silent error 0.0000 | the author's discipline P3 tries to impose | `results/subsumption.json` |
| rung 1's base | nested 0.0517, subsumption silent error 0.5312 at coverage 0.0800 | P3's original anchor, corpus | `results/learned_subsumption.json` |
| direction of declared edges | 0.7556 at write time, 0.7312 pair by pair | over the function, space definition | `results_edges/FINDINGS_EDGES.md`, `results3/FINDINGS3.md` §11 |
| `contradice_subsuncion` | 0 | in every run the repository has made | `results_reuse/FINDINGS_REUSE.md`, `results2/FINDINGS2.md` |
| rung 2's engine | 1.0000 | the hidden policy with its 199 edges, corpus and space | `results2/ceiling2_space.json` |

---

## 4. Non-negotiable rules

`CLAUDE.md`'s own numbering.

1. **Do not modify the frozen specification.** Nothing under `harness/` that the
   rule names is touched. If a frozen file has a bug, stop and say so.
2. **Do not fill in or edit `PREDICTION.md`, and do not sign this plan.** A
   signed plan travels alone, staged by name, in its own commit.
3. **Do not parallelise.** The loop is sequential, and so are the runs: one after
   another, never side by side.
4. **Seed 17, no regeneration, and every paid record guarded.** Nothing under
   `results/`, `results2/` or `results_reuse/` is written by this plan.
   `harness/record_guard.py` guards Stage B's records, and the flag is not typed
   without Sergi asking.
5. **The prompt is fixed before signature.** This plan changes v1, which hard
   rule 5 allows because `PLAN_REUSE.md` recorded a result under it. The changes
   are §5's and only those. Their text is frozen by a fingerprint in the package
   before signature, and `E-g3` checks it. **After signature, nothing in it
   moves.**
6. **If the numbers come out badly, report them.**
7. **The API key goes in the environment**, loaded as rule 7 says, and the key
   endpoint is asked before any call. A management key is refused.

And this plan's own, lettered:

A. **The engine is rung 2's, called and not copied.** `rung2.engine2` and
   `try_edge` decide and validate exactly as they did for the baseline. Level 1
   stays non-overridable: a declaration that contradicts subsumption is refused
   and recorded, as v1's are (§6.8).
B. **The loop differs from `rung2/shadow2.py` only in the proposal path**, and
   `E-g3` checks it: with §5's changes switched off, the new loop reproduces a
   recorded v1 run case by case.
C. **Every new record carries `_env`**, and every figure-producing command runs
   with `PYTHONHASHSEED=0`.
D. **The constants of §11 are fixed here and pinned by tests.**

---

## 5. The protocol, v1e: v1 and four changes

**Everything not named here is v1 as it produced `PLAN_REUSE.md`'s records**:
the system prompt, the neighbourhood of at most `MAX_SHOWN = 12` rules, the base
rendering, the answer's fields, the rule that it must match the ticket, and the
model's settings. The draft wording below is the drafter's. The package freezes
it, at fingerprint `72b611ad60c0278e`, and Sergi may change it before signing and
not after.

**5.1 — The paragraph on what to declare.** v1 says: *"solo necesitas declarar
prioridad frente a reglas que se solapan con la tuya sin que una contenga a la
otra. Si tu regla es un caso particular de otra, no declares nada: el nivel 1 ya
lo resuelve."* v1e replaces it with:

> *Tienes que situar tu regla frente a TODA regla existente con la que se
> solape, la contenga o no: si tu regla es una EXCEPCION a ella, de modo que la
> tuya manda donde casen las dos, ponla en `beats`; si es un caso GENERAL por
> debajo de ella, de modo que la otra manda, ponla en `loses_to`. Si tu regla
> esta contenida en otra, el nivel 1 ya la hace ganar: declararla excepcion lo
> confirma, y declararla caso general lo contradice, y el motor lo registrara.
> Una regla que se solape con otra sin situarse frente a ella se te devolvera
> con la lista de las que faltan.*

**5.2 — The validator, after parsing and before the rule is installed.** v1
checks that the conditions are valid and match the ticket. v1e adds, in order:

1. **A copy is refused.** If the rule's extension equals an existing rule's, it
   is refused as `copia`, and the record names the rule it copies. Equal
   extension covers rules written the same and rules written differently that
   cover the same tickets, the two definitions of `rung3/identical_rules.py`.
2. **Every overlapped rule must be placed.** `O` is the set of existing rules
   whose extension intersects the new rule's, which the engine computes exactly.
   Every rule of `O` must be cited in `beats` or `loses_to`.
3. **One repair round, `K = 1`.** If some rules of `O` are not placed, the loop
   answers once, in the same conversation, listing each missing rule with its id,
   conditions and queue, in a seeded random order recorded with the call:

   > *Tu regla se solapa con estas reglas existentes, frente a las que no te has
   > situado: [lista]. Responde de nuevo con el mismo formato y cita cada una en
   > `beats` o `loses_to`, o cambia la regla.*

   The second answer is validated from the start, as a new proposal: a changed
   rule has its own `O`, and on a CONFLICT the answer may be an order answer
   (§5.3). If it still leaves a rule of its `O` unplaced, the rule is refused as
   `sin_situar`. A refused rule is not installed, and the case keeps the
   proposer's answer as its decision, as v1 does with a rule it rejects.
4. **Citations.** v1 lets `beats` and `loses_to` cite only the rules shown. v1e
   lets them cite the rules shown and the rules listed in a repair round.
5. **Installation is v1's.** The rule is added, and each declaration goes
   through `try_edge`. Its verdict is recorded, and a refused edge is dropped
   while the rule stays.

**5.3 — The order answer, on a CONFLICT only.** The escalation shows the rules
in conflict, as v1 does, and v1e adds one paragraph to what it shows. A copy can
only be written on a CONFLICT, since a rule copying another covers the ticket,
so the warning against copies goes here too:

> *Si este ticket ha escalado porque varias reglas existentes chocan, puedes, en
> lugar de escribir una regla nueva, ordenarlas entre si. Responde entonces
> {"action": "<cola para este ticket>", "order": [{"winner": "<id>", "loser":
> "<id>"}], "note": "<una frase>"}, citando solo reglas de la lista. No escribas
> una copia de una regla existente: una regla que cubre exactamente los mismos
> casos que otra se rechaza.*

Each pair goes through `try_edge`, and its verdict is recorded. No rule is born.
The case keeps `action` as its decision. An order answer to an IMPASSE has
nothing to order and is refused as `orden_sin_conflicto`, keeping its `action`
as v1 keeps a refused rule's. **Every installed edge is tagged with its
channel**, `write` for a declaration that came with a rule and `order` for one
that came with an order answer. E-e reads every row with each channel's edges
alone.

**5.4 — What every call records**, beyond what v1 records: the round, the
`finish_reason`, the overlapped set `O` and the rules still unplaced, the
listing order of a repair round, the answer's form, rule or order, and the
verdict of every declaration. The empty answers of `PLAN_FIDELITY.md` and the
parse failures of `FINDINGS3.md` §11 are open because no `finish_reason` was
kept.

---

## 6. Known traps

**6.1 — The protocol is a bundle.** The discipline, the order answer and the
copy refusal change together, and E-a to E-c read the bundle, not the
discipline alone. §2's first choice is how the signer trades purity against a
vehicle, and E-e's split by channel is what the record can still separate.

**6.2 — The screen grows.** A repair round puts more rules in front of the model.
`FINDINGS_FIDELITY.md` found a sign that a screen of compiled rules costs the
model accuracy, measured on a hundred cases a run. So the proposer's action
accuracy is reported beside the baseline's, and a fall is read as a possible
cost of the screen, not of the discipline alone.

**6.3 — A proposer can obey by partitioning.** A rule that overlaps nothing needs
no declaration. E-e reports the share of born rules that overlap nothing and the
overlap among distinct rules. **A fall in CONFLICTs is not a success**: conflict
is the alarm, and partitioning removes the detector (`ARBITRATION_REPORT.md` §3,
level 3).

**6.4 — The date.** The baseline was asked on 2026-09-30. `F-a` found the
instrument unmoved four days later. Every comparison with the baseline is
labelled with both dates.

**6.5 — The listing order.** In `PLAN_PRIMACY.md`'s answers the rule listed
first won more often than its merits explain. A repair round's list is shuffled
with a fixed seed and the order recorded, so a slot effect on declarations can
be read afterwards. It adjudicates nothing.

**6.6 — The corpus room is a handful of cases**, §0. E-c is read over the space
for that reason. A corpus share that moves a lot over 11 cases is not a finding.

**6.7 — Read whole, not as it grew.** E-a to E-c read each final base from case
0, as the baseline does. The loop's own online figures — what it decided while
the base grew — are reported in E-e and adjudicate nothing.

**6.8 — Level 1 is not overridable here.** A declaration that a contained rule
is a default under its container is refused by `try_edge` as
`contradice_subsuncion` and recorded: that is E-d. Letting declarations override
subsumption would be another engine and another plan.

**6.9 — The rarest queue.** The escalation trigger is v1's, and `U-d` found it
never asks about `ONCALL_ESCALATION`. E-e counts it again and expects zero.

---

## 7. Blocking checks, before any record is written

All free, all run by `--dry-run`, and **any failure stops the plan before a
figure exists**. They are brought forward to before signature, as
`PLAN_REUSE.md` did with Sergi's leave, so that a failure becomes a fix to this
draft rather than a signed amendment.

- **E-g1 — STOP 0, for the engine and for the declaration path.** The hidden
  policy loaded into `rung2.engine2`, with its 199 edges entered as v1e's
  declarations through the same translation the loop uses, executes at 1.0000
  with no silent error, no CONFLICT and no IMPASSE, on the corpus and over the
  space. And `python3 -m unittest discover` is green.
- **E-g2 — The baseline reproduces.** `reuse/structure.py`'s profiles of the
  three final bases recompute and equal `results_reuse/structure.json`, and each
  base's end to end with its installed edges, rebuilt from its record, equals
  what `results_edges/score.json` publishes, exactly, on both surfaces. So E-c's
  baseline shares and E-a's nesting over distinct rules are the ones §0
  declares, to the fourth decimal.
- **E-g3 — The loop and the validator do what §5 says, and nothing else.**
  - With §5's changes switched off, the new loop, replaying the proposals of a
    recorded v1 run, reproduces that run's records case by case.
  - With them on, the validator applied to `PLAN_REUSE.md`'s recorded proposals
    refuses as copies exactly the 44 later copies `structure.json` lists.
  - The labels the loop reads (§11) agree case by case across
    `PLAN_REUSE.md`'s three records and with rung 1's record of the same
    corpus.
  - The prompt's changed paragraphs and the repair message hash to the
    fingerprint the package declares.
- **E-g4 — The signature**, §11.

**And before Stage B's runs, Stage B's own checks**, `PLAN_REUSE.md`'s as they
ended: the key endpoint answers 200 for a key that is not a management key; a
smoke run of 20 cases under this protocol shows at least one proposal parsed and
one rule born, and its record carries every field of §5.4. A full run refuses
without that smoke record.

> **[NOTE 2026-10-05] Run before signature, and all three pass.**
> `python3 -m authorship.run --dry-run`, zero API calls, nothing written.
> `E-g1`: the hidden policy's 199 edges entered through v1e's declaration path,
> all accepted, and 1.0000 on corpus and space, with the suite green. `E-g2`: the
> three bases reproduce `structure.json` and `results_edges/score.json` exactly.
> `E-g3`: the labels agree, the smoke corpus is the head of the full one, all
> three v1 runs replay through the loop record by record, the copy check finds
> exactly the 44, and the texts hash to `72b611ad60c0278e`.
>
> **One correction came out of `E-g2`.** The drafter had computed E-c's baseline
> shares from `FINDINGS_EDGES.md`'s table, rounded to four decimals, and each came
> out one too high in the fourth decimal. §0 now carries the exact ones, 0.3000,
> 0.3833 and 0.7806, and the median 0.3833. No band moves and no row's claim
> changes. Written by the drafter before §0 was signed.

---

## 8. Stage A — the baseline (free)

**It is already measured.** `results_reuse/structure.json` and
`FINDINGS_EDGES.md`'s table are the baseline, and `E-g2` reproduces them. Stage A
writes no record of its own, and nothing it reads can inform a band §0 has not
already set.

---

## 9. Stage B — the runs (`R` × n=2000, gated on §0)

**Deliverable.** `authorship/run.py` → `results_authorship/run_n2000_r1.json` …
`_r{R}.json`, preceded by `results_authorship/run_n20_smoke.json`.

**Protocol.** The corpus of seed 17; a fresh `PriorityEngine(space=Space())`; the
proposer with v1e; the loop of §5. Every run starts from an empty base.
Sequential, one after another, in Sergi's terminal. **A run that dies keeps what
it paid for**: answers are appended to a git-ignored partial file and the same
command resumes there, as `fidelity/ask.py` does, and a run of failed calls
stops the run without recording them.

---

## 10. Stage C — scoring (free)

**Deliverable.** `authorship/score.py` → `results_authorship/score.json`, and
`results_authorship/FINDINGS_AUTHORSHIP.md`, which owns every figure.

For each run: the final base profiled by `reuse/structure.py`'s instrument, for
E-a and E-b; the final base rebuilt with every installed edge, then with each
channel's alone, its end to end over the space and on the corpus, for E-c and
E-e; the declarations' verdicts, for E-d. The median over runs adjudicates, and
each run's value is published beside it.

**Also recorded, outside every denominator**, E-e's list:

- the loop's online figures, beside the baseline's: `reuse_rate`, silent error,
  `proposal_action_accuracy` and `e2e_accuracy`, never summed;
- calls, repair rounds and refusals by reason, with `finish_reason` counts;
- the share of born rules that overlap nothing, and overlap among distinct rules
  (§6.3);
- declarations by verdict and by channel;
- `ONCALL_ESCALATION` and `SECURITY_INCIDENT` escalations and compiled decisions;
- the spread of every row over the `R` runs.

---

## 11. The gate, and where the code lives

**Every module that writes this plan's records refuses while §0 is unsigned**,
the free ones too, and `authorship/run.py` refuses before it constructs the
client. **The free stages get a gate because what it protects is not money**
(`PLAN_SENSITIVITY.md` §8): Stage C's figures are what the rows are, and without
the gate only commit order stands between them and a band.

**It reads `PLAN_AUTHORSHIP.md` and no other plan, and it counts signatures**:
every line starting `**Signed by Sergi:` must be filled in, and there must be at
least one. If a blocking check forces an amendment, the amendment carries its
own signature line. No flag skips the gate; `--dry-run` runs `E-g1` to `E-g3`
and writes nothing.

**Constants fixed here, before any figure exists, not to be tuned afterwards and
pinned by tests:** `N = 2000`, `SEED = 17`, `MODEL =
"deepseek/deepseek-v4-flash"`, `REASONING = {"effort": "none"}`, `MAX_SHOWN = 12`,
`REPAIR_ROUNDS = 1`, `LISTING_SEED = 17`, `REPS = 3`, `SMOKE_N = 20`, unless the
signature says otherwise; and §0's lines, `0.05`, `0.45` with `0.90`, `0.50`
and `1`.

Drafter's proposal for the layout; the naming is Sergi's to overrule:

```
authorship/__init__.py
authorship/plan.py       the gate, the constants, §0's lines
authorship/protocol.py   v1e: §5's paragraphs and repair message, the validator,
                         the order answer, the fingerprint
authorship/loop.py       rung 2's loop with v1e's proposal path; engine2 called
authorship/gates.py      E-g1 to E-g4
authorship/run.py        Stage B, its smoke and key checks; spends; guarded
authorship/score.py      Stage C: E-a to E-d, and E-e
results_authorship/FINDINGS_AUTHORSHIP.md  run_n20_smoke.json
results_authorship/run_n2000_r1.json … run_n2000_r{R}.json  score.json
```

**The plumbing goes in the same commit as the modules**, because each of these
lists has drifted before when it was left for later. `authorship` joins
`CODE_ROOTS` in `harness/provenance.py` and the oracle scan's roots.
`protocol.py`, `loop.py` and `run.py` join `ONLINE_LOOP`, since they are
proposer paths. The guarded writers in `tests/test_writer_lists.py` grow from
five to six, and the README's table of writers gains its rows. **The list of
modules allowed to see the oracle does not grow.** `rung2/shadow2.py` labels its
records by importing it, and a proposer path may not. So the loop takes each
case's label from `PLAN_REUSE.md`'s records of the same corpus, which `E-g3`
checks against one another and against rung 1's, and scoring reads labels off
the records and off `rung3`'s instruments.

---

## 12. Definition of done

- [ ] Records under `results_authorship/` with `_env`, produced with
      `PYTHONHASHSEED=0`.
- [ ] `E-g1` to `E-g4` passed before any record was written; Stage B's key check
      and smoke run before the first full run.
- [ ] The plumbing of §11, and tests pinning its constants, §5's validator on
      small worlds, and the definitions of E-a to E-c; the whole suite green.
- [ ] Every figure in prose names its surface, and every comparison with the
      baseline names both dates.
- [ ] `results_authorship/FINDINGS_AUTHORSHIP.md` owns every figure, with a dated
      erratum wherever it corrects something already published.
- [ ] `STATUS.md`: the scoreboard gains the `E` thread, four adjudicated rows and
      one reported, and its headline's second clause is revisited whichever way
      E-c comes out.
- [ ] `IDEAS.md`: Stage E, in the pairwise section, closed or narrowed; the item
      on subsumption against declaration in the rung 2 list, by E-d; and whatever
      this opens, added.
- [ ] This plan indexed in `README.md` and `CLAUDE.md` once it is signed and
      operative, and not before.
- [ ] Code, records and this plan in separate commits; the plan and its signature
      alone in theirs.

---

## 13. What this plan cannot settle, declared before it runs

1. **The discipline alone.** It is run as a bundle with its vehicle and a copy
   refusal (§6.1). E-e separates the channels' edges, not the protocols.
2. **P3's second prediction.** It has nothing to measure on this loop, so it is
   not carried. On a base with nesting to prune it might, and that base would be
   another plan's.
3. **The material.** No declaration changes which queue the model writes, and
   `T3_ENGINEERING` and `ACCOUNT_MANAGER` keep their missing rules. E-b is the
   row that would show otherwise.
4. **A trigger that would ask about the rarest queue.** v1's trigger is kept, and
   none is specified.
5. **Whether level 1 should yield to a declaration.** E-d counts the
   contradictions. It does not ask what overriding subsumption would buy.
6. **One model, one corpus, `R` draws.** `deepseek/deepseek-v4-flash`, as every
   paid record. v2's overlap arithmetic is not tried; another model is an item of
   `IDEAS.md`.
