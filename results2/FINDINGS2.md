# Peldaño 2 — hallazgo

Registro. 6 de agosto de 2026. Corpus n=100, semillas 17/18/19/20, modelo
`deepseek/deepseek-v4-flash`, ocho tiradas (cuatro por versión de prompt).

---

## El resultado central

**El cambio introducido para POSIBILITAR la prioridad declarada es el que la hizo
imposible de medir.**

El peldaño 1 concluyó que la prioridad no es recuperable de la forma sintáctica
de las reglas, y que la información necesaria no estaba en el contexto del
proponente: veía un ticket y ninguna otra regla. El peldaño 2 le dio esa
información — la base de reglas existente — y un campo del esquema para declarar
prioridad.

Darle la base **redujo el solape entre sus reglas en un factor 10**: de 17,5% de
las parejas sin base a la vista, a 1,6% con ella. Sin solape no hay conflicto, y
sin conflicto no hay prioridad que declarar. El mecanismo nunca recibió material
que lo ejercitara:

```
ocho tiradas · ~200 escalaciones
  conflictos totales      2
  aristas propuestas     14
  aristas ACEPTADAS       0
  EDGE_CONTRADICTS        0
```

`EDGE_CONTRADICTS` —el contador diseñado en este peldaño para detectar si el
proponente declara prioridades que contradicen la subsunción— no ha medido nada,
en ninguna de las ocho tiradas. No porque el proponente acertara: porque nunca se
llegó a la situación en la que ese contador puede incrementarse.

## Dos afirmaciones distintas, que no deben confundirse

**Primera: el motor híbrido ejecuta correctamente una política por capas.** El
Paso 0 cargó las 29 reglas de la política oculta con sus relaciones de prioridad
declaradas —61 parejas ordenadas por subsunción más 199 aristas declaradas
mínimas, derivadas del orden de capas— y midió sobre el corpus de 2000 con
semilla 17:

```
arbitraje                               e2e   err.sil  CONFLICT  IMPASSE
especificidad (peldaño 1)            0.5875    0.2140       505        0
subsunción sola (peldaño 1)          0.6315    0.0000       737        0
HIBRIDO (peldaño 2)                  1.0000    0.0000         0        0
```

2000 ACTION, 2000 aciertos, cero errores silenciosos, cero conflictos. El
rediseño del arbitraje **funciona**. Reproducible sin gastar nada con
`python3 -m peldano2.ceiling_check2`.

**Segunda: no llega material que lo ejercite.** Esto es lo que estas ocho tiradas
miden, y es independiente de lo anterior. Un mecanismo correcto al que no le
llegan entradas no queda refutado por ello; queda sin medir.

Confundir las dos afirmaciones sería leer este registro como "el arbitraje
híbrido no funciona", que es lo contrario de lo que dice el Paso 0.

## El resultado sobre el comportamiento del proponente

**Un proponente al que se le da la base de reglas existente, la información
exacta de solape, y la instrucción explícita de solapar, escribe reglas
mayoritariamente disjuntas y lo argumenta como mérito. Trata la base como una
partición a completar, no como una jerarquía con excepciones.**

Una precisión sobre esa formulación, porque los números no la sostienen en su
forma fuerte: la instrucción explícita **sí tuvo efecto medible**. El solape
subió de 1,60% de media (v1) a 7,25% (v2). Lo que no cambió es la naturaleza del
comportamiento ni su consecuencia. La forma exacta del hallazgo es:

> Enseñarle la base **reduce** el solape respecto a no enseñársela. Sin base a la
> vista (peldaño 1) escribía reglas que se solapaban el 17,5% de las parejas; con
> la base delante, el 1,6%. Instruirle explícitamente a solapar recupera parte
> del terreno (7,25%) pero no llega ni a la mitad del punto de partida, y en
> ocho tiradas **nunca** produjo material suficiente para ejercitar el mecanismo
> de prioridad declarada.

---

## Lo verificable

### 1. El solape se derrumba al enseñarle la base, con la misma densidad de reglas

```
base                           reglas  cond/regla  solape%  sol.dif%  anid  CONF
PELDAÑO 1  n=100 (sin base)        16        2.94     17.5       8.3     1     1
PELDAÑO 1  n=2000 (sin base)      577        3.06     32.3      21.3  8599   594

PELDAÑO 2  v1  semilla 17          40        3.73      2.9       2.8     0     0
PELDAÑO 2  v1  semilla 18          14        2.86      2.2       0.0     2     0
PELDAÑO 2  v1  semilla 19          12        3.00      1.5       1.5     0     0
PELDAÑO 2  v1  semilla 20          26        2.92      0.0       0.0     0     0

PELDAÑO 2  v2  semilla 17           6        2.33     13.3       6.7     2     0
PELDAÑO 2  v2  semilla 18           9        2.89     11.1       5.6     2     1
PELDAÑO 2  v2  semilla 19          12        3.67      1.5       0.0     1     0
PELDAÑO 2  v2  semilla 20          26        3.54      3.1       0.3     9     1
```

`solape%` y `sol.dif%` son porcentajes sobre el total de parejas de la base;
`anid` es un recuento de parejas anidadas; `CONF` los conflictos que el motor
declaró durante la tirada. Las columnas `CONF` del peldaño 1 vienen de su motor
por especificidad y no son comparables con las del peldaño 2, que salen del motor
híbrido: se listan solo para situar el orden de magnitud.

Dispersión entre tiradas del mismo prompt:

```
        condiciones/regla        solape %              conflictos
v1      media 3,13  desv 0,35    media 1,60  desv 1,10    0 0 0 0
v2      media 3,11  desv 0,54    media 7,25  desv 5,04    0 1 0 1
```

**La densidad de condiciones es idéntica en las tres poblaciones** (2,94 sin base;
3,13 con base v1; 3,11 con base v2). No estrecha las reglas. Lo que cambia es
dónde las coloca: elige combinaciones de atributos que embaldosan el espacio en
vez de apilarse sobre él.

El número de reglas varía de 6 a 40 con prompt idéntico, así que esa magnitud es
ruido y no se usa para nada aquí.

### 2. Las notas argumentan la disjunción, y lo hacen más bajo la v2

```
notas que argumentan disjunción explícitamente
  v1:  8/40 (20%)   5/14 (36%)   2/12 (17%)   4/26 (15%)     media 22%
  v2:  5/6  (83%)   4/9  (44%)   7/12 (58%)   9/26 (35%)     media 55%
```

El recuento es por marcadores literales y es tosco. Las citas son la prueba.
**Todas las siguientes son notas v2**, escritas bajo un prompt que dice *"El
solape entre reglas es NORMAL y es lo que se espera"* y *"No estreches una regla
ni le añadas condiciones para esquivar a otra: eso no resuelve el conflicto, lo
esconde"*:

```
[v2 s17 R0003]  free AND severity eq 4 -> T1_GENERAL          (0 aciertos de 21)
  "Al restringir el tier y la severidad, la regla es DISJUNTA con las existentes
   (R0001/R0002 se centran en enterprise/dashboard y severidad...)"

[v2 s18 R0002]  billing AND severity lte 3 AND pro -> T2_TECHNICAL   (0 de 5)
  "...cubriendo casos similares SIN SOLAPAMIENTO con reglas existentes"

[v2 s18 R0005]  billing AND severity eq 4 -> BILLING_SPECIALIST      (2 de 7)
  "NO SE SOLAPA con reglas existentes porque todas requieren severity <=3 o tier free."

[v2 s18 R0006]  pro|business|enterprise AND sev eq 4 AND product neq billing
  "Esta regla llena ese vacío y ES DISJUNTA DE TODAS las reglas existentes por
   severidad o producto."

[v2 s19 R0002]  free AND product neq billing AND no-security -> T1_GENERAL  (0 de 33)
  "La regla es DISJUNTA con R0001 (product=billing) y NO SE SOLAPA con ninguna otra"

[v2 s19 R0005]  pro|business AND sev in [2,3] AND integrations
  "...llenando el VACÍO dejado por las reglas existentes... NO HAY SOLAPAMIENTO
   porque product es disjunto de los ya cubiertos."

[v2 s20 R0005]  pro|business AND billing AND off_hours AND sev in [2,3]
  "NO SE SOLAPA con reglas existentes (todas requieren free)."
```

El patrón es siempre el mismo: identifica un hueco de la partición, lo rellena, y
presenta la ausencia de solape como justificación de la regla. La base no es para
él una pila de capas donde la nueva regla tiene que situarse; es un mosaico
incompleto.

### 3. El mecanismo de prioridad nunca recibió material

```
ocho tiradas · ~200 escalaciones
  aristas propuestas          14
  aristas ACEPTADAS            0
  EDGE_CONTRADICTS             0
  conflictos totales           2
```

Las 14 aristas propuestas cayeron todas por `no_solapan`: citan reglas cuya
extensión no intersecta la de la regla nueva. `EDGE_CONTRADICTS` —el instrumento
diseñado para detectar si el proponente contradice la subsunción— **no ha medido
nada en ninguna de las ocho tiradas**, porque nunca se llegó a la situación donde
la subsunción tiene algo que decir.

Las dos únicas ocasiones en que el motor sí produjo un conflicto:

```
v2 semilla 18, caso 35: CONFLICT entre R0001 y R0005
  el proponente respondió con acción T1_GENERAL y CERO aristas
  (verdad: SELF_SERVICE_DEFLECT)

v2 semilla 20, caso 65: CONFLICT entre R0013 y R0017
  la propuesta falló al parsear; no hubo regla ni aristas
```

Dos oportunidades en ocho tiradas. Una desaprovechada, una perdida por un JSON
mal formado.

### 4. Los atributos que nunca usa

```
atributo               tiradas (de 8) en que aparece
severity                8/8
customer_tier           8/8
product                 8/8
has_security_keyword    5/8
off_hours               2/8
prior_tickets_30d       1/8
channel                 1/8
language                0/8
```

`language` no aparece en ninguna de las ocho bases. `channel` y
`prior_tickets_30d` en una cada uno. La política oculta tiene capas enteras
construidas sobre esos atributos: H11/H13/H14/H25/H26 dependen de
`prior_tickets_30d` y deciden el 14,5% del corpus; H22/H23 dependen de `channel`;
H21 de `language`.

El caso extremo es la v2 con semilla 17: seis reglas que usan solo
`customer_tier`, `severity` y `product` (dos veces). Una partición de dos
dimensiones sobre una política de ocho capas, con cobertura 0,940 y error
silencioso 0,7553.

---

## Por qué esto NO es un fallo de capacidad del modelo

Hay dos razones, y la segunda es un experimento.

**Primera: razona relacionalmente en cuanto se le da con qué.** En el peldaño 1
las notas describían el ticket presentado. En el peldaño 2, con la base delante,
citan reglas por identificador y argumentan sobre ellas:

```
[v1 s17 R0017]  "...se requiere atención técnica (T2) en lugar de general (T1)
                 porque la severidad es más crítica que la del caso R0014 (severity=3)"
[v1 s17 R0014]  "...Debe perder contra R0012 que cubre off_hours=true con prioridad."
[v2 s17 R0029]  "...Esta regla es un caso particular de las reglas de T2_TECHNICAL,
                 pero al ser más específica y de mayor prioridad, el nivel 1 la resuelve"
```

Ese último es correcto: entiende que la subsunción resuelve el anidamiento sin
declaración. La facultad de razonar sobre prioridad entre reglas está presente.

**Segunda: se le quitó su otro error y el comportamiento no cambió.** Bajo la v1
calculaba mal las extensiones de forma sistemática — afirmaba solape entre
`billing` e `integrations`, que son disjuntos; escribía que `off_hours` es
mutuamente excluyente y declaraba la arista igualmente. Se podía sostener que el
problema era aritmético, no conceptual.

La v2 le entrega esa aritmética resuelta por el motor: por cada regla mostrada,
qué condiciones incumple el ticket, el tamaño de su extensión, qué pares son
disjuntos, y la regla de inferencia enunciada. Todo calculado sobre las 134.400
combinaciones y nada de ello derivable por él.

Resultado: **cinco de las catorce aristas mal propuestas son de la v2**, las tres
en escalaciones donde el vecindario marcaba explícitamente qué condiciones
incumplía el ticket para cada regla citada. Con la información correcta delante,
comete el mismo error.

No es que no pueda calcular el solape. Es que la operación que ejecuta —encontrar
un hueco y rellenarlo— no requiere calcularlo, y esa es la operación que hace
aunque se le pida otra.

---

## Salvedades

**Un modelo.** Todo es `deepseek/deepseek-v4-flash`. No se sabe si otro modelo,
o uno más capaz, particiona igual.

**Tiradas de n=100.** Bases de 6 a 40 reglas. El número de reglas varía tanto
entre semillas con prompt idéntico que esa magnitud es ruido; las conclusiones se
apoyan en el solape, en los atributos y en las notas, que sí son estables. Nada
aquí dice qué pasaría a n=2000.

**No determinismo a temperature 0.** Verificado en el peldaño 1: mismo prompt,
mismo caso, misma semilla, reglas distintas. Por eso cada configuración se corrió
con cuatro corpus distintos en vez de uno, y por eso el número de reglas no se
usa como evidencia.

**El motor no es el problema.** Ver arriba, "Dos afirmaciones distintas": el Paso
0 da e2e 1,0000 con la política perfecta cargada. Nada de lo que sigue en este
registro pone eso en duda.

**El coste de autoría no está medido en una base aprendida.** Las 199 aristas del
Paso 0 son lo que declara un autor perfecto para 29 reglas. Cuántas harían falta
para una base aprendida, y si un proponente podría producirlas, es justamente lo
que estas ocho tiradas no han llegado a poner a prueba.

---

## Archivos

```
peldano2/engine2.py            motor híbrido: subsunción + prioridad declarada
peldano2/hidden_priority.py    las 29 reglas con sus aristas mínimas derivadas
peldano2/ceiling_check2.py     PASO 0 — techo del motor
peldano2/proposers2.py         prompts v1 y v2, vecindario v1 y v2
peldano2/shadow2.py            bucle en sombra
peldano2/run2.py               CLI de tiradas
peldano2/compare_runs.py       comparativa entre tiradas
peldano2/note_audit.py         atributos usados y notas que argumentan disjunción

results2/ceiling2.json         techo del Paso 0
results2/llm_run2_n100*.json   las ocho tiradas, cada una con su prompt íntegro
results2/comparativa.json      tabla comparativa
results2/note_audit.json       auditoría de notas y atributos
results2/CAMBIOS.md            registro del cambio v1 -> v2
results2/NOTA_REGISTRO.md      por qué cambió el mtime de results/subsumption.json
```

Los textos íntegros de ambos prompts están dentro de cada `llm_run2_*.json`, en
el campo `system_prompt`, junto a las cifras que produjeron.
