# Peldaño 1 — hallazgos

Registro de cierre. 5–6 de agosto de 2026.
Corpus: 2000 casos, semilla 17, 1743 únicos. Política oculta: 29 reglas en 8
capas. Proponente: `deepseek/deepseek-v4-flash` vía OpenRouter.

El peldaño se cierra sin haber medido su hipótesis. La pregunta que se quería
responder —si las reglas que escribe un LLM se reutilizan o memorizan casos— no
llegó a ser medible, porque el motor sobre el que se medía no puede ejecutar la
clase de política que se le pedía ejecutar. Lo que sigue es lo que sí quedó
establecido.

---

## El resultado

**La prioridad en una política estratificada no es recuperable de la forma
sintáctica de las reglas.**

La política oculta es una lista priorizada por capas: overrides de seguridad,
SLO y guardia, facturación, riesgo de fuga, enrutado por producto, idioma y
dotación, deflexión, defectos. Primera coincidencia gana. Su contenido vive en
las condiciones de cada regla; su estructura vive en el orden entre ellas.

El motor recibe las reglas sin ese orden y tiene que reconstruirlo a partir de
lo único que ve: la forma de las reglas. Se probaron tres criterios para hacerlo.
Ninguno funciona, y no por afinar mal un parámetro: fallan por razones
estructurales distintas entre sí.

El DSL no es el culpable. Verificado exhaustivamente sobre las 134.400
combinaciones del espacio de casos que las 29 reglas escritas en el DSL son
equivalentes a sus predicados originales, y que evaluarlas con "primera que casa
gana" reproduce la política exactamente. Fallo de ejecución, no de
representación.

---

## Las tres vías falsadas

Todas las cifras con la política **perfecta** cargada, salvo donde se indique.
Ninguna involucra al LLM.

### 1. Especificidad — número de condiciones

`RuleEngine.decide`: gana la regla con más condiciones; empate con acciones
distintas devuelve CONFLICT.

```
ACTION 1495   IMPASSE 0   CONFLICT 505 (25,3%)
cobertura 0,7475   error silencioso 0,2140 (320 casos)   e2e 0,5875
```

Prioridad y número de condiciones son casi ortogonales en esta política. H24
(capa 6, 2 condiciones) gana a H16, H18 y H03 (capas 4 y 0, 1 condición cada
una) y les roba 246 casos. El catch-all H29 tiene 1 condición y por tanto empata
en especificidad con toda regla de capa de 1 condición, generando conflicto en
vez de ceder.

Demostración de que ninguna función monótona de la especificidad puede
funcionar, usando solo reglas de la propia política: H01 (2 condiciones) debe
ganar a H03 (1), y H16 (1) debe ganar a H24 (2). Las dos exigencias son
incompatibles bajo cualquier criterio monótono en el número de condiciones.

Corolario sobre la frontera del experimento: las reglas de `keep_k(k)` tienen
todas exactamente k condiciones, así que su especificidad es uniforme y el
arbitraje nunca puede invertirlas — el desempate cae en antigüedad, que es la
semántica correcta. Los mocks son estructuralmente inmunes al defecto que
destroza la política real. `keep_k(k=4)` puntúa mejor que la política verdadera
bajo este motor: 0,173 de error silencioso frente a 0,214, y 0,780 de e2e frente
a 0,588. La "región a batir" estaba por encima del techo del sistema.

Reproducible: `python3 -m harness.ceiling_check`.

### 2. Orden de llegada — antigüedad de la regla

Gana la regla más antigua que casa, sin mirar especificidad.

```
orden de diseño     100,0%
orden inverso        12,8%
orden aleatorio      49,3%   (media sobre 200 muestras)
```

El 100% del orden de diseño es una tautología: cargar las reglas en el orden de
la política y decir "gana la más antigua" *es* primera-que-casa. Demuestra que
DSL más orden total bastan para ejecutar la política, y nada más.

Lo que importa es el resto de la curva. El criterio no tiene contenido propio:
transporta el orden que se le dé. Y en una base aprendida el orden de llegada va
sistemáticamente al revés del correcto, porque los primeros casos vienen de la
distribución común y engendran reglas de defecto, mientras las excepciones —que
deben tener prioridad— nacen tarde.

(Las cifras de orden inverso y aleatorio están registradas en `PREDICTION.md`;
el repo solo automatiza el orden de diseño.)

### 3. Subsunción semántica — inclusión de extensiones

`A ≺ B` sii el conjunto de casos que A casa es subconjunto estricto del de B,
calculado sobre el espacio completo de 134.400 combinaciones. No cuenta
condiciones: compara extensiones. Gana la minimal del orden parcial; si las
minimales discrepan en acción, CONFLICT.

Es el único criterio de los tres que no es monótono en el número de condiciones,
así que puede satisfacer a la vez H01 ≺ H03 y la incomparabilidad de H16 con
H24.

**Sobre la política oculta, escrita por un humano:**

```
parejas ordenadas 61 de 406 (15,0%)   contradicciones con el orden de capas: 0
ACTION 1263   CONFLICT 737 (36,9%)
error silencioso 0,0000  (0 de 1263)   e2e 0,6315
```

Cero contradicciones, y de ahí se sigue la soundness: si alguna regla que casa
estuviera estrictamente por debajo de la regla de capa más temprana, esa pareja
contradiría el orden de capas; como no las hay, la regla correcta está siempre
en el conjunto minimal. El motor deja de equivocarse en silencio: o acierta, o
declara que no sabe.

El residuo además está concentrado. 737 casos en 131 conjuntos minimales, y
desempatarlos por frecuencia da:

```
k=10 -> e2e 0,8415     k=20 -> 0,8870     k=50 -> 0,9495     k=131 -> 1,0000
```

con error silencioso 0,0000 en todo el trayecto. No hace falta un orden total
sobre 29 reglas: bastan unas decenas de desempates dirigidos.

**Sobre la base aprendida, 577 reglas escritas por el LLM:**

```
parejas ordenadas 8599 de 166176 (5,17%)
ACTION 160   CONFLICT 1840
casos en que se compromete: 160   de esos, acción equivocada: 85  (53,12%)
cobertura 0,0800   error silencioso 0,5312   e2e 0,0375
residuo: 873 conjuntos minimales; los 10 primeros cubren 122 casos
```

Las tres propiedades desaparecen a la vez. La soundness pasa de 0,00% a 53,12%
de error: peor que una moneda. La cobertura cae al 8%. El residuo pasa de 131
conjuntos concentrados a 873 difusos.

Las reglas responsables de la falta de soundness son estrechas —4 a 6
condiciones, extensión pequeña— y por eso la subsunción las declara minimales y
las deja ganar, con la acción equivocada. Extensión pequeña no significa
correcta.

Reproducible: `python3 -m harness.subsumption_check` y
`python3 -m harness.learned_subsumption`.

---

## La formulación

Los tres criterios son **proxies sintácticos de prioridad autorizada**.

Funcionan en la medida en que un autor haya codificado la prioridad en la forma
de las reglas, y no llevan ninguna señal cuando nadie lo ha hecho. La
especificidad supone que el autor puso más condiciones en lo más prioritario. El
orden de llegada supone que el autor escribió primero lo más prioritario. La
subsunción supone que el autor anidó las excepciones dentro de los defectos.

En la política oculta la tercera suposición se cumple —de ahí el 0,00% de
error— porque quien la escribió puso las excepciones antes que los defectos, que
es como se escriben las políticas por capas sanas. Ese 0,00% no mide una virtud
del criterio: mide una virtud del autor. La base aprendida no tiene autor en ese
sentido, y el mismo criterio produce 53,12% de error.

La compilación por impasse aprende reglas. No tiene ningún mecanismo para
aprender prioridad. En una política estratificada la estructura vive ahí.

---

## Por qué un modelo más capaz no lo arregla

La información necesaria no está en el contexto del proponente.

El proponente ve un ticket y el vocabulario del dominio. No ve la base de reglas
existente, no ve qué reglas ya cubren regiones vecinas, y no ve por qué el caso
que se le presenta llegó hasta él. Con eso no se puede decidir una prioridad
relativa, porque la prioridad es una relación entre reglas y él solo tiene una.

El caso más claro está registrado. La región `product == dashboard AND severity
<= 3` cubre 382 casos (19,1% del corpus) y toca 15 reglas ocultas distintas;
`T1_GENERAL` solo es la verdad en el 21,5% de ella. El caso que originó la regla
que cubre esa región lo resuelve H29, el catch-all `lambda c: True`, tras fallar
28 capas. El proponente ve una respuesta correcta y no puede saber que lo es por
descarte. Generalizó un residuo como si fuera una regla positiva. Ocurrió en las
dos tiradas, de formas distintas: en la de n=100 con la acción correcta y el
alcance equivocado, en la de n=2000 equivocando también la acción.

Ningún aumento de capacidad reconstruye una relación a partir de un solo
operando. Y las cifras que se atribuirían a la capacidad del modelo son
pequeñas: en la tirada anulada, sustituir la acción de cada regla por la verdad
de su caso de origen bajaba el error silencioso de 0,4839 a 0,4298 —5 puntos de
48—, y darle a cada regla su acción óptima lo dejaba todavía en 0,2909. El resto
es alcance, no elección de cola.

---

## Qué queda abierto

Declarar la prioridad en vez de inferirla.

Si la prioridad no es recuperable de la forma de las reglas, la alternativa es
que forme parte de lo que se escribe: un campo en el esquema, una referencia
explícita a la regla de la que ésta es excepción, o cualquier otra
representación que el validador pueda comprobar. Eso obliga a dar al proponente
la base de reglas existente como contexto, porque una prioridad relativa no se
puede declarar sin ver respecto a qué.

Es un problema de autoría, no de arbitraje. Cambia qué se le pide al proponente
y qué se le enseña, no cómo desempata el motor. No está medido: aquí solo queda
registrado que las tres vías de inferencia están falsadas.

---

## Salvedades

**Cotas, no simulaciones.** Las 577 reglas de la base aprendida se escribieron
bajo arbitraje por especificidad. Qué caso escalaba —y por tanto qué regla
nacía— dependía de ese arbitraje. Bajo subsunción desde el primer caso la base
habría sido otra. Lo medido es cómo se comporta esa base con otro arbitraje, no
lo que el bucle habría producido. Además, en esa medición las 577 reglas están
cargadas desde el caso 0, mientras que en la tirada se acumulaban; por eso las
cifras de especificidad en estático (cobertura 0,4290, e2e 0,1825) no coinciden
con las de `results/llm_run.json` (0,684 y 0,353).

**No determinismo a temperature 0.** El corpus es determinista (semilla 17); el
proponente no. Mismo prompt, mismo caso, misma semilla, y las reglas nacidas de
los primeros casos difieren entre la tirada de n=100 y la de n=2000. La prueba
corta no es un prefijo de la larga, y una comparativa entre modelos no tiene al
modelo como única variable salvo que se promedien varias semillas de muestreo.

**Soundness verificada sobre una sola política oculta.** El 0,00% de error de la
subsunción se comprobó sobre las 29 reglas de `hidden_policy.py` y sobre ninguna
otra. Es una propiedad de esa política concreta, no un teorema. No se sabe con
qué frecuencia la cumplen las políticas escritas a mano en general, ni si el
resultado sobrevive a otra estratificación.

**Un solo modelo, una sola tirada.** Las cifras del proponente son de
`deepseek/deepseek-v4-flash` en una ejecución. La tirada quedó anulada por techo
del motor antes de que la comparación entre modelos tuviera sentido.

---

## Genealogía

La compilación por impasse viene del *chunking* de SOAR: cuando la resolución de
un problema se atasca, el sistema resuelve el atasco en un subespacio y compila
el resultado en una regla nueva, de modo que la próxima vez no se atasque.

Lo que aquí se tomó prestado fue el mecanismo de compilación. Lo que no se tomó
fue la estructura que lo hace bien definido. En SOAR los impasses ocurren dentro
de una jerarquía de metas, y la regla compilada nace dentro del contexto de la
submeta que resolvió el atasco; el orden entre alternativas lo fijan preferencias
que a su vez producen reglas. La prioridad está declarada por el sistema, no
inferida de la forma de las producciones.

Aquí la base se hizo una lista plana y el arbitraje un criterio sintáctico
calculado sobre las reglas. La jerarquía de impasses, que es donde vivía la
estructura de prioridad, no se replicó. La estructura que se perdió al aplanar
es exactamente la que los tres criterios intentaron reconstruir después, sin
conseguirlo.

---

## Archivos

```
harness/ceiling_check.py         techo del motor; especificidad y orden de diseño
harness/subsumption_check.py     orden parcial por subsunción, política oculta
harness/learned_subsumption.py   el mismo criterio sobre la base aprendida
results/frontier.json            barrido de mocks y baselines
results/llm_run.json             tirada anulada, n=2000, registros crudos por caso
results/llm_run_n100_smoke.json  prueba corta previa
results/subsumption.json         orden parcial y curva de concentración
results/learned_subsumption.json soundness sobre la base aprendida
PREDICTION.md                    predicción registrada y acta de anulación
```
