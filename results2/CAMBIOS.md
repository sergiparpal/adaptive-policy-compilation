# Changelog — rung 2

> The prompt fragments quoted below are the **literal Spanish text** that lives
> in `rung2/proposers2.py`; the v2 is built by literal substitution over the
> v1, so they are reproduced verbatim. An English rendering follows each one in
> italics.

## v1 → v2 (August 6, 2026)

Two changes, authorized by Sergi, in this order and only after measuring the
control.

### Motive: the prompt confound, isolated with 4 runs

Before changing anything, 3 additional n=100 runs were done with the v1 prompt
**intact**, varying only the corpus sampling seed (18, 19, 20). Together with the
original one (seed 17):

```
base                          rules cond/rule  overlap%  ov.diff%   nest  CONF
RUNG 1  n=100 (16 rules)         16      2.94      17.5       8.3      1     -
RUNG 1  n=2000 (577)            577      3.06      32.3      21.3   8599     -
RUNG 2  n=100 seed 17            40      3.73       2.9       2.8      0     0
RUNG 2  n=100 seed 18            14      2.86       2.2       0.0      2     0
RUNG 2  n=100 seed 19            12      3.00       1.5       1.5      0     0
RUNG 2  n=100 seed 20            26      2.92       0.0       0.0      0     0
```

Conclusion: **the effect of the v1 prompt is real and systematic, but it is not
the one that had been diagnosed.** The number of conditions per rule did NOT
change relative to rung 1 (2.86–3.00 in three of the four; seed 17, at 3.73, is
the outlier). What changed is the **overlap**, which fell from 17.5% to 0.0–2.9%,
an order of magnitude, in all four runs.

The model does not narrow the rules: it **tiles** them. With the same condition
density it picks attribute combinations that tessellate the space instead of
stacking on top of it. Without overlap there is no conflict (0 in all four runs),
and without conflict declared priority cannot be measured: the mechanism sits
inert.

Data in `comparativa.json`.

### Change 1 — how overlap is framed in the prompt

The v1 said:

> Por eso solo necesitas declarar prioridad frente a reglas que se solapan con la
> tuya sin que una contenga a la otra. Si tu regla es un caso particular de otra,
> no declares nada: el nivel 1 ya lo resuelve.

> *So you only need to declare priority against rules that overlap yours without
> one containing the other. If your rule is a particular case of another one,
> declare nothing: level 1 already resolves it.*

It reads as an incentive to **avoid** overlap. The v2 replaces it with:

> El solape entre reglas es NORMAL y es lo que se espera. Una regla que no se
> solapa con ninguna otra cubre solo el rincón del que nació y no generaliza
> nada. Escribe la regla al nivel de abstracción que creas correcto AUNQUE pise
> a otras, y usa `beats` / `loses_to` para decir quién manda donde se pisen. No
> estreches una regla ni le añadas condiciones para esquivar a otra: eso no
> resuelve el conflicto, lo esconde.
>
> Si tu regla es un caso particular de otra (todo caso que casa la tuya casa
> también la otra), no declares nada: el nivel 1 ya lo resuelve solo.
>
> Cuidado con la aritmética de conjuntos: dos reglas que mencionan los mismos
> atributos pueden no compartir ni un solo caso. El motor te marca abajo, para
> cada regla, qué condiciones incumple este ticket y qué pares son disjuntos.
> Esos datos están calculados sobre el espacio completo de casos: fíate de ellos
> antes que de tu propia estimación.

> *Overlap between rules is NORMAL and is what is expected. A rule that does not
> overlap any other covers only the corner it was born in and generalizes
> nothing. Write the rule at the level of abstraction you think correct EVEN IF
> it treads on others, and use `beats` / `loses_to` to say who rules where they
> tread on each other. Do not narrow a rule or add conditions to it to dodge
> another one: that does not resolve the conflict, it hides it.*
>
> *If your rule is a particular case of another (every case matching yours also
> matches the other), declare nothing: level 1 already resolves it on its own.*
>
> *Careful with set arithmetic: two rules mentioning the same attributes may not
> share a single case. Below, for each rule, the engine marks which conditions
> this ticket fails and which pairs are disjoint. That data is computed over the
> complete case space: trust it over your own estimate.*

**The rest of the prompt is identical word for word.** The v2 is built by literal
substitution over the v1 (`SYSTEM_PROMPT_V1.replace(...)`) with an `assert` that
fails if the substitution does not apply, so it cannot diverge silently.

### Change 2 — the neighbourhood supplies the set arithmetic

Under v1 the proposer miscalculated the overlap, and did so systematically:

- `R0035` claimed overlap "in business+severity4" between a `billing` rule and an
  `integrations` one, which are disjoint: they do not share a single case.
- `R0036` **wrote** that `off_hours` is mutually exclusive and declared the edge
  anyway.
- `R0014` ordered itself against an `off_hours=true` rule while being
  `off_hours=false` itself.

It is not that it ignored the overlap: it confuses "they share attributes" with
"they share cases". A set-arithmetic failure was completely masking the
measurement of whether it knows how to declare priority.

The v2 neighbourhood adds, all of it computed by the engine over the 134,400
combinations and none of it derivable by the proposer:

- per rule shown, whether it **matches the ticket** (overlap guaranteed with any
  rule that gets written) or **which conditions the ticket fails**;
- the **size of the extension** of each rule;
- the **disjoint pairs** among the rules shown;
- the inference rule stated once: if you fix an attribute that rule R fails, your
  rule and R end up disjoint and declaring priority has no effect.

`correct_count` is still not shown: it belongs to the oracle.

### What did NOT change

Engine, rule schema, validator, corpus seed for the main comparison (17), model
(`deepseek/deepseek-v4-flash`), cap of 12 rules in the neighbourhood,
neighbourhood selection criterion, and the invariants of the experiment (pure
shadow, oracle separation, escalation only by impasse or conflict, sequential
loop).

### Reproducing

```bash
python3 -m rung2.run2 --n 100 --seed 17 --prompt-version v1 --tag n100
python3 -m rung2.run2 --n 100 --seed 17 --prompt-version v2 --tag n100_v2
python3 -m rung2.compare_runs results2/llm_run2_*.json
```

Each run stores its `prompt_version` and the full text of the `system_prompt` it
used, so no figure is left orphaned from the version that produced it.
