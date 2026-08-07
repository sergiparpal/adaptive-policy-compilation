# Registro de cambios — peldaño 2

## v1 → v2 (6 de agosto de 2026)

Dos cambios, autorizados por Sergi, en este orden y solo tras medir el control.

### Motivo: el confound del prompt, aislado con 4 tiradas

Antes de cambiar nada se corrieron 3 tiradas adicionales de n=100 con el prompt
v1 **intacto**, variando solo la semilla de muestreo del corpus (18, 19, 20).
Junto con la original (semilla 17):

```
base                           reglas cond/regla  solape%  sol.dif%   anid  CONF
PELDANO 1  n=100 (16 reglas)       16      2.94     17.5       8.3      1     -
PELDANO 1  n=2000 (577)           577      3.06     32.3      21.3   8599     -
PELDANO 2  n=100 semilla 17        40      3.73      2.9       2.8      0     0
PELDANO 2  n=100 semilla 18        14      2.86      2.2       0.0      2     0
PELDANO 2  n=100 semilla 19        12      3.00      1.5       1.5      0     0
PELDANO 2  n=100 semilla 20        26      2.92      0.0       0.0      0     0
```

Conclusión: **el efecto del prompt v1 es real y sistemático, pero no es el que se
había diagnosticado.** El número de condiciones por regla NO cambió respecto al
peldaño 1 (2,86–3,00 en tres de las cuatro; la semilla 17, con 3,73, es el
outlier). Lo que cambió es el **solape**, que cayó de 17,5% a 0,0–2,9%, un orden
de magnitud, en las cuatro tiradas.

El modelo no estrecha las reglas: las **embaldosa**. Con la misma densidad de
condiciones elige combinaciones de atributos que tselan el espacio en vez de
apilarse sobre él. Sin solape no hay conflicto (0 en las cuatro tiradas), y sin
conflicto la prioridad declarada no puede medirse: el mecanismo queda inerte.

Datos en `comparativa.json`.

### Cambio 1 — encuadre del solape en el prompt

La v1 decía:

> Por eso solo necesitas declarar prioridad frente a reglas que se solapan con la
> tuya sin que una contenga a la otra. Si tu regla es un caso particular de otra,
> no declares nada: el nivel 1 ya lo resuelve.

Se lee como incentivo a **evitar** el solape. La v2 lo sustituye por:

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

**El resto del prompt es idéntico palabra por palabra.** La v2 se construye por
sustitución literal sobre la v1 (`SYSTEM_PROMPT_V1.replace(...)`) con un `assert`
que falla si la sustitución no aplica, de modo que no puede divergir en silencio.

### Cambio 2 — el vecindario aporta la aritmética de conjuntos

En la v1 el proponente calculaba mal el solape, y de forma sistemática:

- `R0035` afirmó solape "en business+severity4" entre una regla de `billing` y
  otra de `integrations`, que son disjuntas: no comparten ni un caso.
- `R0036` **escribió** que `off_hours` es mutuamente excluyente y declaró la
  arista igualmente.
- `R0014` se ordenó contra una regla `off_hours=true` siendo ella `off_hours=false`.

No es que ignorase el solape: confunde "comparten atributos" con "comparten
casos". Un fallo de aritmética de conjuntos tapaba por completo la medición de
si sabe declarar prioridad.

El vecindario v2 añade, todo calculado por el motor sobre las 134.400
combinaciones y nada de ello derivable por el proponente:

- por regla mostrada, si **casa el ticket** (solape garantizado con cualquier
  regla que se escriba) o **qué condiciones incumple el ticket**;
- el **tamaño de la extensión** de cada regla;
- los **pares disjuntos** entre las reglas mostradas;
- la regla de inferencia enunciada una vez: si fijas un atributo que la regla R
  incumple, tu regla y R quedan disjuntas y declarar prioridad no tiene efecto.

Sigue sin mostrarse `correct_count`: es del oráculo.

### Qué NO cambió

Motor, esquema de regla, validador, semilla del corpus para la comparación
principal (17), modelo (`deepseek/deepseek-v4-flash`), tope de 12 reglas en el
vecindario, criterio de selección del vecindario, y los invariantes del
experimento (sombra pura, separación del oráculo, escalación solo por impasse o
conflicto, bucle secuencial).

### Reproducir

```bash
python3 -m peldano2.run2 --n 100 --seed 17 --prompt-version v1 --tag n100
python3 -m peldano2.run2 --n 100 --seed 17 --prompt-version v2 --tag n100_v2
python3 -m peldano2.compare_runs results2/llm_run2_*.json
```

Cada tirada guarda su `prompt_version` y el texto íntegro del `system_prompt`
que usó, así que ninguna cifra queda huérfana de la versión que la produjo.
