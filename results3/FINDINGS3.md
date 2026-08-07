# Peldaño 3 — hallazgo

Registro. 6 de agosto de 2026. Base: las 577 reglas que el LLM escribió en el
peldaño 1 (`results/llm_run.json`). Corpus de 2000 casos, semilla 17. Cero
llamadas al LLM en todo el peldaño.

---

## 1. El resultado central

**En el peldaño 1 el material contenía la señal y el arbitraje la destruía.**

Las 577 reglas cubren los 2000 casos —ni uno queda sin regla que lo case— y en
el **90,1%** alguna de las reglas que casan tiene la acción correcta. Ese número
es el techo exacto de cualquier orden total: si ninguna regla que cubre un caso
tiene la acción correcta, ningún orden lo salva. Sale sin buscar nada.

> **[ERRATA 2026-08-06]** El 90,1% es una **cota superior por cobertura por
> caso**, no un óptimo global demostrado. `ceiling()` comprueba, caso a caso,
> que exista *alguna* regla correcta entre las que lo cubren. No comprueba que
> exista **un solo orden total** capaz de hacer ganar simultáneamente a la regla
> correcta en todos esos casos, que es una condición estrictamente más fuerte.
> Como cota superior es válida —ningún orden puede superarla— pero el máximo
> realmente alcanzable por algún orden puede ser menor. Llamarla "techo" a secas
> induce a leerla como alcanzable. Ver la errata del apartado 4.

Buscando un orden sobre la mitad del corpus y evaluándolo sobre la otra mitad,
nunca vista por el orden:

```
              train              test               GAP
puro       0.7779±0.0275     0.7711±0.0352     0.0068±0.0203
híbrido    0.7848±0.0080     0.7496±0.0093     0.0351±0.0118
```

**El gap es esencialmente cero.** Dos de las cinco particiones lo tienen
negativo (−0,0161 y −0,0090), y la dispersión entre particiones (±0,0352) es
cinco veces el gap medio (0,0068): el sobreajuste del orden no es detectable por
encima del ruido de partición.

Contra las referencias, todo en test:

```
techo                                       0.8995
orden buscado (voraz), puro                 0.7518
orden buscado (voraz), híbrido              0.7317
orden de llegada (born_at)                  0.5216
orden aleatorio (media de 50)               0.4227
arbitraje por especificidad                 0.1829
subsunción sola (conflicto = fallo)         0.0412
```

Cuatro veces la especificidad. Y el orden de llegada —que el peldaño 1 dio por
inservible— ya saca 0,52: el arbitraje por especificidad era peor que no ordenar
casi nada.

Las dos clases críticas son **100% recuperables**: `SECURITY_INCIDENT` (20 casos)
y `ONCALL_ESCALATION` (7). En el peldaño 1 dieron **0/17** y **0/7**. Las reglas
correctas estaban escritas. El motor nunca las dejó ganar.

El arbitraje híbrido del peldaño 2 es **peor** que el orden puro sobre una base
aprendida (0,7496 frente a 0,7711) y es el único con gap consistente. La
subsunción cuesta 0,047 de techo: elimina de la puja reglas correctas. Coherente
con lo medido en el peldaño 1, donde sobre una base aprendida no resultó sound.

---

## 2. Problema de orden y problema de material son cosas distintas

Los peldaños 1 y 2 los medían juntos. Separados, con el techo por clase:

```
clase                   corpus  techo  irrecuperable        naturaleza del fallo
T2_TECHNICAL               726    714       12   1.7%       orden
SELF_SERVICE_DEFLECT       495    457       38   7.7%       orden
BILLING_SPECIALIST         271    271        0   0.0%       orden
T1_GENERAL                 255    255        0   0.0%       orden
SECURITY_INCIDENT           20     20        0   0.0%       orden
ONCALL_ESCALATION            7      7        0   0.0%       orden
T3_ENGINEERING             117     39       78  66.7%       MATERIAL
ACCOUNT_MANAGER            109     39       70  64.2%       MATERIAL
```

- **Problema de orden.** El material está escrito y lo que decide si se
  aprovecha es el arbitraje, o la función objetivo. Seis clases de ocho, 1774 de
  los 2000 casos.
- **Problema de material.** Dos tercios de `T3_ENGINEERING` y de
  `ACCOUNT_MANAGER` no tienen ni una sola regla correcta que los cubra. Ningún
  orden, ninguna función objetivo y ningún arbitraje los salva. Ahí el
  proponente no escribió lo que hacía falta.

La distinción importa porque las reparaciones son opuestas: una se arregla en el
motor y la otra solo en el proponente. Medidas juntas, ambas se leían como "el
LLM no funciona".

---

## 3. La perilla no declarada

Qué clases se sacrifican es una elección de función objetivo, y en el peldaño 1
la estaba fijando el arbitraje sin que nadie la hubiera puesto ahí.

El voraz por defecto maximiza aciertos totales. La variante balanceada pesa cada
caso por 1/|clase| en train, de modo que cada clase aporta lo mismo:

```
objetivo                   e2e test   acierto balanceado
aciertos totales             0.7707               0.5241
balanceado por clase         0.7150               0.6936
                             -5,6 pts             +17,0 pts
```

Por clase, en test (partición 0):

```
clase                     test  techo   total  balanc.   % techo tot  % techo bal
T2_TECHNICAL               364    357     318      295           89%          83%
SELF_SERVICE_DEFLECT       242    220     191      157           87%          71%
BILLING_SPECIALIST         136    136      90      110           66%          81%
T1_GENERAL                 128    128     128      128          100%         100%
T3_ENGINEERING              57     20      14        5           70%          25%
ACCOUNT_MANAGER             55     21       0        5            0%          24%
SECURITY_INCIDENT           10     10       7       10           70%         100%
ONCALL_ESCALATION            3      3       0        3            0%         100%
```

Por **5,6 puntos de agregado**, `ONCALL_ESCALATION` pasa de 0/3 a **3/3** y
`SECURITY_INCIDENT` de 7/10 a **10/10** — las dos clases críticas al 100% de su
techo. `BILLING_SPECIALIST` mejora de 66% a 81%.

Lo pagan `SELF_SERVICE_DEFLECT` (87% → 71%), `T2_TECHNICAL` (89% → 83%) y sobre
todo **`T3_ENGINEERING`, que empeora de 70% a 25%**. Balancear no es gratis ni es
uniformemente mejor: redistribuye, y una de las clases que pierde es una de las
que menos techo tenía.

El punto no es que el balanceado sea preferible. Es que la elección existe, es
explícita en la función objetivo, y antes se estaba tomando sin declararla. Los
0/17 de `SECURITY_INCIDENT` del peldaño 1 no eran una propiedad del sistema: eran
la consecuencia no declarada de maximizar aciertos totales con un arbitraje que
además lo hacía mal.

---

## 4. Salvedades

Todas necesarias para que el resultado no se lea como más de lo que es.

**La búsqueda usa el oráculo.** El voraz elige cada regla contando aciertos y
fallos contra `true_action` sobre los casos de train. Es supervisión que el bucle
en sombra no tiene nunca: su único disparador es impasse o conflicto, jamás "la
respuesta era incorrecta". Lo demostrado es que **el material contiene la señal**,
no que sea alcanzable sin etiquetas.

**Las 50 etiquetas compran el orden, no el material.** Con supervisión parcial
—muestreo aleatorio simple del train, porque estratificar exigiría conocer las
etiquetas que se racionan— la curva aguanta:

```
 fracción  etiquetas    test e2e     desv      min      max
     100%       1005      0.7707   0.0374   0.7425   0.8430
      25%        251      0.7681   0.0326   0.7290   0.8522
      10%        100      0.7488   0.0352   0.6500   0.8053
       5%         50      0.7049   0.0535   0.5596   0.8241
       1%         10      0.5251   0.0628   0.3850   0.6577
```

Al 25% la pérdida es 0,0026, prácticamente gratis. Al 5% —50 casos, el 2,5% del
corpus— quedan 0,7049, el 78% del techo. Al 1% se desploma a 0,5251, que es el
orden de llegada sin buscar nada. Pero **esas 50 etiquetas no son la supervisión
total del sistema**: las 577 reglas costaron 632 llamadas al LLM sobre el corpus
completo, ya pagadas. Decir "funciona con 50 etiquetas" omitiría ese coste.

**Varianza alta con presupuesto bajo.** Al 5%, desviación 0,0535 y rango
0,5596–0,8241. La media aguanta; un sorteo concreto de 50 etiquetas puede dar
0,56.

**El voraz no tiene garantía global.** Es el voraz clásico de listas de decisión:
óptimo en cada paso local sobre los casos vivos, sin razón de aproximación
conocida para este objetivo, y sin búsqueda local posterior. Medido: buscando el
orden **sobre el propio test** queda todavía a **0,1187** de media por debajo del
techo. Casi todo el hueco entre 0,77 y 0,90 es debilidad del método de búsqueda,
no falta de generalización.

> **[ERRATA 2026-08-06]** La última frase no está demostrada. Lo medido es que
> el voraz, buscando sobre el propio test, se queda a 0,1187 de la cota. Eso
> separa limpiamente búsqueda de generalización —el hueco no viene de evaluar
> fuera de muestra— pero **no establece que esos 0,1187 sean alcanzables por
> orden alguno**. La cota es por cobertura caso a caso (ver errata del apartado
> 1) y el máximo real sobre órdenes totales puede estar por debajo. La
> afirmación correcta es: *el hueco entre 0,77 y 0,90 no se explica por falta de
> generalización; cuánto de él es debilidad del voraz y cuánto es cota
> inalcanzable queda sin medir.* Haría falta optimización exacta o una cota
> global más fuerte.
>
> Evidencia adicional posterior de que el voraz es débil, aunque tampoco acota
> el óptimo: en el peldaño 4 resultó que perturbar su objetivo con ruido lo
> mejora contra la verdad (0,7574 → 0,8337), y que cambiar el desempate mueve el
> resultado ~0,011.

**Las reglas se aprendieron sobre el corpus completo.** `born_at` va de 0 a 1998.
El test no son datos no vistos por las reglas; son datos no vistos por el orden.
La partición controla el sobreajuste del orden y solo ese. El gap de un sistema
entero sería mayor. Por eso la partición se agrupó por identidad de caso: el
23,1% del corpus tiene un gemelo exacto y una partición al azar habría premiado
memorizar.

---

## 5. Qué reescribe del peldaño 1

`results/FINDINGS.md` es registro cerrado y **no se modifica**. Se corrige por
encima, no por dentro. Lo que cambia es esto:

**El titular no era "el LLM no induce estructura reutilizable". Era "el LLM
inducía estructura y el motor la destruía".**

Lo que sigue en pie de aquel registro, sin tocar:

- la prioridad en una política estratificada no es recuperable de la forma
  sintáctica de las reglas; las tres vías (especificidad, orden de llegada,
  subsunción) siguen falsadas
- el techo del motor del peldaño 1 con la política perfecta cargada: 58,75%
- la formulación de proxy sintáctico de prioridad autorizada
- la generalización desde el residuo del catch-all
- la ceguera atributiva del proponente

Lo que queda re-encuadrado:

- **El material era mucho mejor de lo que cualquier métrica de aquella tirada
  sugería.** Reutilización 0,158, error silencioso 0,484 y e2e 0,353 describían
  lo que el arbitraje extraía, no lo que las reglas contenían. El techo de esas
  mismas reglas es 0,90.
- **"La compilación destruyó capacidad"** era cierto y ahora es más preciso: no
  es que las reglas compiladas fueran malas, es que las correctas existían y
  nunca ganaban. `SECURITY_INCIDENT` es 100% recuperable y dio 0/17.
- **El umbral de parada** (reutilización < 0,30) se aplicó a una cifra que ya
  estaba anulada por el techo del motor. Este peldaño no lo rehabilita —la
  reutilización sigue sin medirse limpiamente— pero confirma que detener el
  proyecto por aquel 0,158 habría sido detenerlo por una medición del arbitraje.

Lo que este peldaño **no** demuestra: que el bucle pueda encontrar ese orden. La
búsqueda ve etiquetas; el bucle no. Sigue abierto.

---

## Archivos

```
peldano3/order_search.py         techo exacto, búsqueda voraz, partición, referencias
peldano3/budget_and_balance.py   presupuesto de etiquetas y voraz balanceado

results3/order_search.json       techos, cinco particiones, orden hallado
results3/budget_and_balance.json curva de supervisión y comparación de objetivos
```

Reproducible con `python3 -m peldano3.order_search` y
`python3 -m peldano3.budget_and_balance`. Cero llamadas a la API.

El Paso B —ILP (Popper/ILASP) como medidor del orden de capas y como competidor
que induce reglas por su cuenta— no se ha corrido. Queda sin autorizar.
