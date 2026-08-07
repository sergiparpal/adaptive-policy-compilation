# Peldaño 4 — hallazgo

Registro. 6 de agosto de 2026. Base: las 577 reglas del peldaño 1, el corpus de
2000 casos con semilla 17 y las mismas particiones del peldaño 3. Cero llamadas
al LLM. Solo el Paso A; el Paso B (orden online) no se corrió.

Referencias del peldaño 3, en test: oráculo completo 0,7707 · 5% de etiquetas
0,7049 · 1% de etiquetas 0,5251 · born_at 0,5216 · aleatorio 0,4227 · techo
0,8995.

---

## 1. El resultado central

**El límite de viabilidad no está en la cobertura, ni en el retardo, ni en el
ruido. Está en la asimetría, y no es un límite gradual sino un cambio de
régimen.**

Con feedback simétrico —el canal confirma tanto aciertos como errores— el orden
aprendido bate a born_at en toda la barrida de cobertura, hasta el extremo:

```
cobertura  etiquetas   test e2e   vs born_at
      1.0       1010     0.7564      +0.2348
      0.5        500     0.7520      +0.2304
     0.25        245     0.7803      +0.2587
      0.1         99     0.7399      +0.2183
     0.05         52     0.7087      +0.1871
     0.02         19     0.6393      +0.1177
```

**Con 19 etiquetas todavía saca +0,118 sobre no aprender nada.** El retardo es
casi gratis offline: de 0 a 400 casos va de 0,7564 a 0,7540.

En cuanto el canal deja de confirmar aciertos, el régimen cambia:

```
asimetría  etiquetas   test e2e   vs born_at
      1.0       1010     0.7564      +0.2348
      0.5        751     0.7954      +0.2738
     0.25        622     0.7117      +0.1901
      0.1        544     0.6185      +0.0969
      0.0        498     0.5887      +0.0671
```

La celda `cobertura=1, asimetría=0, retardo=0, ruido=0` es **completamente
determinista** —sin ningún sorteo— y da **0,5887**: el mejor caso posible de un
canal realista, con feedback sobre todos los errores y ninguno perdido, aporta
**+0,067** sobre no aprender nada. El oráculo completo daba +0,235.

> **[ERRATA 2026-08-06]** "Completamente determinista" es **falso**. El canal sí
> lo es en esa celda —no consume ningún sorteo— pero el voraz que consume su
> salida no: los tres voraces (`order_search.py`, `budget_and_balance.py`,
> `sweep.py`) resolvían el argmax iterando sobre un `set` de identificadores,
> cuyo orden depende de `PYTHONHASHSEED`. Medido sobre cinco semillas de hash,
> esa misma celda da:
>
> ```
> PYTHONHASHSEED   0      1      2      7     42
>                0.5991 0.5880 0.5971 0.5988 0.5937      amplitud 0.0111
> ```
>
> El 0,5887 registrado es uno de esos valores, no el único posible. **La
> dirección del hallazgo sobrevive**: en el peor hash el margen sobre born_at
> (0,5216) sigue siendo **+0,066**, y las 24 celdas del régimen realista siguen
> muy por debajo del régimen simétrico. Lo que no sobrevive es la palabra
> "determinista" ni el dígito concreto.
>
> El desempate se corrigió el 6 de agosto de 2026 (iteración sobre lista
> ordenada). **Los peldaños 3 y 4 NO se re-corrieron**: se hará junto con el
> optimizador serio, para poder distinguir si la fragilidad era del desempate o
> del algoritmo. Todas las cifras de estos documentos son las del código
> anterior al arreglo.
>
> **Sobre el margen de 14,5x** que se usó al defender que el hallazgo sobrevive:
> comparaba `a=1` medido bajo **un solo hash** contra la media de cinco hashes de
> `a=0`. La dirección aguanta y el peor caso también, pero el ratio no es limpio
> y no debe citarse como si lo fuera.

Las 24 celdas del régimen realista (asimetría 0) caen entre **0,5448 y 0,6509**,
y con cobertura 0,1 la mejora (+0,023 a +0,047) queda dentro de su propia
desviación.

**La supervisión simétrica es exactamente lo que este peldaño existía para no
suponer.** El peldaño 3 midió 0,7049 con el 5% de etiquetas y de ahí salió la
hipótesis de que un canal pobre bastaría. La hipótesis se sostiene mientras el
canal sea un muestreo insesgado de etiquetas. Deja de sostenerse en cuanto el
canal es lo que un sistema real produce.

---

## 2. El canal como artefacto separado

El riesgo declarado al abrir el peldaño: en un entorno sintético "feedback del
entorno" y "política oculta" son la misma función, y sin acotar el canal esto
mide supervisión completa con otro nombre.

Contención: **`peldano4/feedback.py` es el único módulo del peldaño que importa
`true_action`.** Emite `{caso -> acción reportada}` y nada más. El aprendiz no
recibe la verdad, ni si la decisión fue correcta, ni qué casos quedaron sin
observar. La verdad reaparece solo en la evaluación, que es medición y no
supervisión, igual que en los tres peldaños anteriores.

> **[ERRATA 2026-08-06]** "Único módulo que importa `true_action`" es
> literalmente falso: `peldano4/sweep.py:36` también lo importa. El import
> **está sin usar** (cero llamadas en el archivo), pero la afirmación tal como
> está escrita no es cierta y no debe sostenerse por su intención.
>
> **La separación sustantiva sí se mantiene**, y es lo que importa: el aprendiz
> es `greedy_from_reports`, que recibe únicamente `reported` y no tiene acceso a
> la verdad por ninguna vía. `sweep.py` maneja verdades a través de
> `build_tables` para dos usos que no son supervisión —evaluar el orden
> resultante y calcular la tasa de error de π₀ que se reporta— y nunca se las
> pasa al aprendiz.
>
> Redacción correcta: *`feedback.py` es el único módulo que consulta el oráculo
> para producir la señal de aprendizaje; el aprendiz no lo ve por ninguna vía.*

El canal no observa etiquetas sueltas sino **resultados de decisiones**, lo que
obliga a que exista una política de referencia π₀ decidiendo mientras se observa.
Sin eso, "qué fracción de decisiones recibe resultado" no significa nada. En un
sistema real el ciclo es: el ticket se enruta, alguien lo recibe, y si la cola no
era la suya lo reasigna; la reasignación es el feedback y trae la acción correcta.

| parámetro | qué es | a qué corresponde |
|---|---|---|
| `coverage` c | p(feedback \| decisión incorrecta) | no todo ticket mal enrutado se reasigna: algunos se resuelven igual en la cola equivocada, otros se cierran, otros nadie los toca |
| `asymmetry` a | p(feedback \| correcta) = c·a | **el parámetro que impide que el canal sea el oráculo.** Nadie manda un mensaje diciendo "este ticket estaba bien enrutado". Con a=0 el conjunto etiquetado queda condicionado a que π₀ se equivocara: no es i.i.d., y esa dependencia es la que tendría un sistema desplegado |
| `delay` d | el resultado del caso i solo es utilizable si i+d cae en la ventana | la reasignación ocurre horas o días después, con muchos tickets de por medio |
| `noise` e | con probabilidad e la acción reportada es otra | quien reasigna también se equivoca, o aplica una convención local que no es la política |

**Decisión declarada, no omisión:** la ausencia de feedback **no** se interpreta
como "fue correcto". Sería tentador porque duplicaría la señal, pero con
cobertura parcial la ausencia es ambigua —puede ser acierto o puede ser que nadie
miró— y asumir lo primero inyectaría información que el entorno no da.

---

## 3. El techo estructural: la señal se agota conforme el sistema mejora

```
π₀ observada                    errores de π₀   etiquetas   test e2e
born_at        (0,5216 en test)         49,4%         248     0,5817
especificidad  (0,1829 en test)         54,4%         273     0,7320
```

(c=0,5 · a=0 · d=0 · e=0,1)

**Observar un sistema peor produce un orden mejor.** No es una curiosidad del
montaje: es una propiedad del aprendizaje por feedback de errores.

Con asimetría baja las etiquetas solo llegan de los fallos. El volumen de señal
es proporcional a la tasa de error del sistema observado. Un sistema que ya
funciona bien deja de generar la señal que necesitaría para seguir mejorando, y
lo hace exactamente en la región donde quedan los casos difíciles. El aprendizaje
por corrección tiene un punto fijo que no coincide con el óptimo, y lo tiene por
construcción del canal, no por debilidad del aprendiz.

Es el mismo fenómeno, visto desde el otro lado, que hacía medible el error
silencioso: el sistema no puede pedir ayuda sobre lo que resuelve con confianza.

---

## 4. La contaminación del ruido, y su consecuencia metodológica

En el barrido, **más ruido daba mejores resultados**: 0,7564 con etiquetas
limpias, 0,8198 con el 10% falsificadas. Eso es imposible como efecto de
supervisión, así que se diagnosticó antes de reportar nada.

**Descartada la inestabilidad por desempates.** Con etiquetas idénticas y 12
órdenes de iteración distintos del voraz: media 0,7518, **desviación 0,0000**,
rango 0,7518–0,7518. El método es determinista dado el conjunto etiquetado.

> **[ERRATA 2026-08-06] El test nulo no probaba lo que decía probar, y este es
> el error más informativo de los cuatro.**
>
> El test permutaba la lista `rules` que se pasa al voraz. Pero el bucle del
> argmax itera sobre `left = set(ids)`, y el orden de iteración de un `set` de
> cadenas lo determinan sus **hashes**, no el orden de inserción de la lista de
> origen. Es decir: se permutó una cosa que no afectaba al desempate, salió
> 0,0000 de varianza, y se interpretó ese cero como prueba de determinismo.
>
> **El 0,0000 era correcto y no medía nada.** Un resultado nulo solo descarta
> algo si el instrumento podía haberlo detectado, y este no podía.
>
> Repetido correctamente —variando `PYTHONHASHSEED`, que es lo que gobierna el
> desempate real— el voraz **sí** es sensible al desempate: ~0,011 de amplitud
> en la celda ancla del apartado 1.
>
> Esto **no invalida el diagnóstico del ruido** que sigue abajo, que es de otro
> orden de magnitud (0,7574 → 0,8337 contra la verdad, frente a 0,011 por
> desempate) y se apoya en la comparación train-vs-etiquetas contra
> train-vs-verdad, no en el test nulo. Lo que sí hace es reforzar su conclusión:
> el voraz es un optimizador débil, y ahora se sabe que lo es también frente a
> perturbaciones tan pequeñas como el orden de iteración.

El diagnóstico real (24 tiradas por fila):

```
ruido   TRAIN vs etiquetas   TRAIN vs VERDAD   TEST vs verdad
  0.0            0.7574           0.7574          0.7564
  0.1            0.7462           0.8259          0.8163
  0.3            0.5996           0.8337          0.8171
  0.5            0.4250           0.7398          0.7004
```

El objetivo que el voraz optimiza baja como debe (0,7574 → 0,5996). El orden
resultante, medido contra la verdad, **sube** (0,7574 → 0,8337). Con etiquetas
perfectas el voraz se queda en 0,7574 contra la verdad; con el 30% falsificadas
llega a 0,8337.

**El voraz con etiquetas limpias cae en un óptimo local malo y el ruido lo saca
de él**, funcionando como reinicio aleatorio. Es coherente con lo medido en el
peldaño 3: buscando el orden sobre el propio test quedaban 0,1187 por debajo del
techo. El voraz es un optimizador débil, y perturbar su objetivo lo mejora.

**Consecuencia metodológica:** cualquier parámetro del canal que inyecte
aleatoriedad actúa en parte como mejora de la búsqueda y no como degradación de
la supervisión. Los barridos de ruido y de cobertura con asimetría 1 **no se
pueden leer como curvas de degradación**. Por eso el resultado central se ancla
en la celda determinista (c=1, a=0, d=0, e=0) y en el rango completo de las 24
celdas del régimen realista, no en las curvas contaminadas.

No se corrigió el método. Cambiar el optimizador después de ver los números es
exactamente el fallo que este experimento estudia.

---

## 5. Qué dejan los cuatro peldaños respecto a la arquitectura original

La arquitectura era: un motor simbólico barato resuelve lo que cubre; cuando no
cubre un caso, un LLM actúa y escribe una regla para que la próxima vez sí lo
cubra. La hipótesis a medir: si esas reglas se reutilizan o si el modelo memoriza
casos.

**Esa hipótesis sigue sin medirse.** El peldaño 1 quedó anulado por el techo del
motor, y su reutilización de 0,158 describía el arbitraje, no la inducción.

Lo que sí quedó establecido, en orden:

- **La prioridad es la pieza que falta, y no está en la forma de las reglas.**
  Tres criterios sintácticos falsados: especificidad (0,5875 con la política
  perfecta cargada), orden de llegada (100% en orden de diseño, 12,8% inverso,
  49,3% aleatorio) y subsunción (0% de error sobre la política escrita a mano,
  53,12% sobre la base aprendida). Son proxies de prioridad autorizada: funcionan
  en la medida en que un autor la codificó en la forma, y no llevan señal cuando
  nadie lo hizo.

- **El mecanismo para ejecutarla existe y funciona.** Subsunción más 199 aristas
  declaradas ejecutan la política de ocho capas al 100%: e2e 1,0000, error
  silencioso 0,0000, cero conflictos, cero impasses.

- **El proponente no la suministra.** Con la base delante, la aritmética de
  solape resuelta por el motor y la instrucción explícita de solapar, escribe
  reglas mayoritariamente disjuntas y lo argumenta como mérito. Ocho tiradas, dos
  conflictos, cero aristas aceptadas. El cambio introducido para posibilitar la
  prioridad es el que la dejó sin material que medir.

- **El material del proponente era mucho mejor de lo que parecía.** Techo 0,90
  sobre las mismas 577 reglas que el arbitraje convertía en 0,18.
  `SECURITY_INCIDENT` y `ONCALL_ESCALATION` son 100% recuperables y dieron 0/17 y
  0/7. Y qué clases se sacrifican resultó ser una elección de función objetivo
  que nadie había declarado.

- **La prioridad tampoco se aprende del feedback que un sistema real da.** Con
  supervisión simétrica se recupera casi todo (+0,235); con la asimétrica, que es
  la única realista, quedan +0,067, y la señal se agota conforme el sistema
  mejora.

Las tres vías de suministrar prioridad —inferirla de la sintaxis, hacer que el
proponente la declare, aprenderla del comportamiento observado— están medidas, y
cada una falla por una razón distinta. La compilación por impasse aprende reglas;
la estructura de una política estratificada no vive en las reglas.

---

## Archivos

```
peldano4/feedback.py    el canal; único módulo que importa true_action
peldano4/sweep.py       barridos, rejilla realista y sensibilidad a π₀
results4/sweep.json     todas las celdas medidas
```

Reproducible con `python3 -m peldano4.sweep`. Cero llamadas a la API.

El Paso B —orden online, con la base creciendo y el feedback llegando con
retardo— no se corrió: la asimetría responde la pregunta que el peldaño existía
para responder, y el orden online solo la degradaría más.
