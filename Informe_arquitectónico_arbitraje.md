# El arbitraje de prioridad en `adaptive-policy-compilation`

Informe sobre la pregunta *"¿qué regla gana cuando varias casan y discrepan?"*, escrito
contra los registros del repositorio a fecha de `STATUS.md` (2026-08-16).

**Convención, y este informe la cumple sobre sí mismo.** Toda cifra nombra dos cosas: su
**superficie** —**corpus** (distribución de llegada, n=2000, semilla 17) o **espacio** (las
134.400 combinaciones, medida uniforme)— y el **registro que la posee**. Las dos
superficies no son intercambiables y ni siquiera rankean igual. **Este informe no publica
ninguna cifra por primera vez**: todas viven en un `FINDINGS` con su erratum al lado y en
`STATUS.md`, que las indexa; aquí sólo se citan con su puntero. Lo **establecido** va con su
registro; lo **propuesto** va marcado como tal y con una predicción falsable, nunca mezclado
con lo medido.

---

## 0. La respuesta, en una página

La prioridad de una política estratificada **no es un dato derivable de las reglas: es
información externa que alguien tiene que suministrar**. La única pregunta legítima es
quién, en qué formato y cuándo se le pregunta. De ahí sale una escalera de cuatro
escalones, en este orden y no en otro:

1. **Lo que dicta la semántica.** Si `ext(A) ⊊ ext(B)` y discrepan en acción, gana A. Es
   derivado, no declarado, y **parcial**: sobre las 29 reglas ordena 61 de los 406 pares, un
   15%. Pero **no es gratis, y esa es la corrección más importante de este informe**: sobre
   una política escrita a mano es sólido y sin coste; sobre la base aprendida de 577 reglas
   *baja la propia cota de cobertura* de 0.9010 a 0.8540 y el orden buscado de 0.8530 a
   0.7734 (corpus test), porque retira reglas correctas de la puja. §3, nivel 1.
2. **El residuo se declara, en aristas referenciales entre pares concretos**, nunca en un
   entero global. Medido: subsunción más 199 aristas mínimas sobre la política oculta dan
   e2e **1.0000**, error silencioso 0.0000, cero conflictos, cero impasses **sobre el
   corpus** — sobre el espacio ese motor no se ha medido nunca.
3. **Si nadie declara, se busca o se aprende.** Búsqueda sobre casos etiquetados:
   **0.8530** (corpus test) frente a una cota de cobertura de 0.9010. Aprendizaje desde
   feedback asimétrico —el único que un sistema desplegado produce—: **+0.2011** sobre
   `born_at`, el 61% de lo que compra la supervisión total (corpus test).
4. **Cuando nada resuelve, abstenerse.** `CONFLICT` no es un fallo del motor: es la única
   forma de que el error sea medible en vez de silencioso.

Y dos advertencias que valen tanto como la escalera:

- **El mecanismo de ejecución no es el cuello de botella.** El motor del peldaño 2 ya da
  1.0000 sobre el corpus con un autor perfecto. Lo que falta es **material**: en ocho
  ejecuciones el proponente generó 2 conflictos y 14 aristas, ninguna aceptada.
- **El orden no está identificado por el objetivo.** Órdenes que puntúan igual son
  máquinas distintas. Eso hace el problema de *verificación* más duro que el de
  arbitraje, y ninguna arquitectura de árbitro lo resuelve.

---

## 1. Qué pregunta es exactamente

Dado un caso, el motor calcula el conjunto de reglas que casan y devuelve una de tres
salidas: `IMPASSE` (ninguna casa → problema de **cobertura**), `ACTION` (una gana) o
`CONFLICT` (varias casan y discrepan → problema de **prioridad**). La pregunta de este
informe es la tercera salida, y conviene no confundirla con la primera: son dos carencias
distintas y un sistema puede tener cobertura perfecta y prioridad rota.

La separación que hace el proyecto y que hay que sostener en cualquier rediseño:

> **Representación ≠ ejecución.** Sobre las 134.400 combinaciones del espacio, las 29
> reglas escritas en el DSL son equivalentes a sus predicados originales, y evaluarlas con
> *first-match-wins* reproduce la política exacta. El DSL no pierde nada. Lo que fallaba
> era el árbitro.

Esa verificación —fijada por `tests/test_encoding_invariant.py`, no sólo publicada— es lo
que convierte "el sistema va mal" en "el sistema **ejecuta mal una política que representa
bien**", que es una afirmación mucho más fuerte y mucho más accionable. Cualquier
diagnóstico de arbitraje debería empezar por reproducirla: si la representación no está
limpia, no se sabe qué se está midiendo.

---

## 2. Lo falsado: la prioridad no está en la forma de las reglas

Tres criterios sintácticos, con la política **perfecta** cargada y sin LLM de por medio
(corpus, `results/FINDINGS.md`):

| criterio | resultado | por qué falla |
|---|---|---|
| **Especificidad** (gana la de más condiciones) | e2e 0.5875, err. silencioso 0.2140, CONFLICT 25.3% | prioridad y nº de condiciones son casi ortogonales |
| **Orden de llegada** | 100% en orden de diseño, 12.8% invertido, **49.3%** aleatorio | no tiene contenido propio: transporta el orden que le des |
| **Subsunción** | err. silencioso **0.0000** (política escrita a mano) / **53.12%** (base aprendida) | mide una virtud del **autor**, no del criterio |

**La imposibilidad de la especificidad es una prueba, no una medición.** Dentro de la
propia política: H01 (2 condiciones) debe ganar a H03 (1), y H16 (1) debe ganar a H24 (2).
Ninguna función monótona del número de condiciones satisface ambas. No es un
hiperparámetro mal puesto; es una imposibilidad de representación.

**La forma generalizable del fallo**, que es lo que se lleva uno a otro dominio: *la
especificidad funciona si y solo si las excepciones son **refinamientos** de las reglas que
anulan.* Se invierte en cuanto la política tiene una capa de **overrides anchos** encima
—seguridad, cumplimiento, on-call—, que por naturaleza se escriben con pocas condiciones,
mientras las reglas estrechas de caso especial viven abajo. Vale la pena decirlo con el
vocabulario correcto: **arriba hay overrides anchos, no defaults**; los defaults están al
fondo y a veces son los más específicos de la base. Esa es la forma normal de una política
de negocio, no una patología del caso de estudio.

**La firma diagnóstica, que es exportable.** Bajo el motor de especificidad, `keep_k(k=4)`
—una rejilla burda de reglas de 4 condiciones— **supera a la política oculta**. No por ser
mejor política: por ser inmune a la inversión, ya que con especificidad uniforme el árbitro
nunca puede invertir y el desempate cae a `born_at`. De ahí la regla práctica:

> **Si una baseline tonta supera a tu oráculo, tu árbitro está invirtiendo prioridades. No
> es la política la que está mal.**

**La trampa de la subsunción merece un párrafo aparte** porque es el hallazgo más fácil de
malinterpretar. El 0.0000 sobre la política escrita a mano no valida el criterio: valida
al autor, que respetaba el convenio "regla estrecha = excepción a la ancha". Un proponente
que escribe ticket a ticket no lo respeta —una regla estrecha suya puede ser un default
sobreajustado— y ahí el mismo criterio da 53.12% de error silencioso.

**Ese 53.12% hay que citarlo con su denominador**, porque sin él se lee como cuatro veces
peor de lo que es y como cuatro veces mejor a la vez. Sobre la base aprendida la subsunción
sólo se compromete en **160 de 2000 casos** (cobertura 0.0800); el 53.12% son **85 errores
sobre esos 160**, y el e2e resultante es 0.0375. Es decir: el criterio no se vuelve
temerario, se vuelve mudo, y cuando habla se equivoca más que una moneda. **La subsunción
no es gratis; es gratis condicionada a una disciplina de autoría.** De eso sale la
propuesta **P3**.

---

## 3. La forma correcta de la respuesta

El arbitraje que funciona es **un orden parcial semántico más una totalización declarada**,
ambos en el mismo grafo, más abstención.

### Nivel 1 — Subsunción

`A ≺ B` si `ext(A) ⊊ ext(B)`, calculado como máscara de bits sobre el espacio exhaustivo.
Es derivado, no declarado. Es **parcial**: 61 de 406 pares sobre 29 reglas.

**Y no es un nivel gratuito: es una decisión de diseño con precio medido.** Sobre la base
aprendida de 577 reglas, activar la subsunción como nivel no sobrescribible cuesta esto
(`results3/FINDINGS3.md` §1 y su erratum de 2026-08-08; `results3/order_search_ls.json`):

| pool | cota por cobertura (corpus) | orden buscado (corpus test) | el mismo orden sobre el espacio |
|---|---|---|---|
| puro (sólo orden total) | 0.9010 | **0.8530** | 0.6105 |
| híbrido (subsunción + orden) | 0.8540 | **0.7734** | 0.4970 |

Los 0.047 se pierden **en la cota**, no en la búsqueda: la subsunción retira reglas
correctas de la puja antes de que haya orden ninguno. El mecanismo está contado en
`results3/FINDINGS_AUDIT.md`, paso 1: una vez la subsunción poda, **181 de las 577 reglas
no casan absolutamente nada** sobre el train. Un tercio de lo que el proponente escribió es
inalcanzable por construcción, antes de cualquier pregunta de orden. Y no es debilidad del
optimizador: el híbrido sigue por debajo bajo el optimizador auditado, con un margen mayor
que bajo el voraz.

Eso deja el nivel 1 en un sitio más incómodo y más honesto que "no se negocia":

> **Sobre una base con disciplina de autoría, la subsunción es orden gratis y sólido. Sobre
> una base aprendida sin esa disciplina, es un filtro que cuesta 0.047 de cota y silencia un
> tercio de las reglas.** Si se conserva no sobrescribible —y hay razones para conservarlo,
> es la única parte del orden derivada de la semántica— hay que conservarlo *sabiendo el
> precio*, y ese precio es lo que P3 intenta dejar de pagar.

Por qué sigue mereciendo ser el nivel base pese al precio: es el único que ningún
proponente puede falsear, el único que no hay que verificar contra nada, y el que da los 61
pares sin gastar una sola pregunta. Lo que no se sostiene es presentarlo como sin coste.

### Nivel 2 — Aristas referenciales, no enteros

`{"beats": ["R0007"], "loses_to": ["R0021"]}`. Las cuatro razones por las que esto derrota
a un `priority: 17` **son las del docstring de `peldano2/engine2.py`**, no una derivación
nueva de este informe; se reproducen porque son la justificación del diseño y conviene
tenerlas donde se discute:

1. **Un entero exige una decisión global desde una observación local.** El proponente ve
   un ticket y un puñado de reglas. Es la misma exigencia que ya falló en el peldaño 1 con
   otro nombre.
2. **La información que falta es parcial, no total.** Son relaciones entre pares. Un
   ranking global es una respuesta a una pregunta que nadie hizo.
3. **Una referencia es mecánicamente verificable.** Un entero es **infalsificable**:
   cualquier número pasa cualquier validador.
4. **Una referencia compone; un entero compite.** Si el entero dice A>B y la subsunción
   dice B≺A, no hay forma no arbitraria de arbitrar entre los dos arbitrajes.

Ese cuarto punto es el que descalifica los esquemas mixtos del tipo `priority_layer` +
`overrides`: introducen dos autoridades sobre el mismo par.

**Qué comprueba exactamente el validador** (verificado contra `peldano2/engine2.py:220` y
`try_edge`, no inferido): seis verdictos, cinco de rechazo y uno de aceptación —
`EDGE_SELF` (auto-referencia), `EDGE_UNKNOWN` (la regla citada no existe), `EDGE_DISJOINT`
(las extensiones no se cortan: la arista sería inerte), `EDGE_CONTRADICTS` (la subsunción
ya dice lo contrario), `EDGE_CYCLE` (cerraría un ciclo) y `EDGE_OK`. Detalle que no es
obvio: `EDGE_OK` se devuelve además cuando `ext(ganador) ⊊ ext(perdedor)`, es decir cuando
la arista es redundante con la subsunción pero consistente con ella; se acepta y no añade
nada al grafo.

**Y lo que el validador no puede comprobar, que es lo que importa para el §7:** que el
ganador declarado sea el correcto. Existencia, solape, no-contradicción y aciclicidad son
propiedades del grafo; la verdad de la arista no está en el grafo. Una arista falsa y bien
formada entra sin resistencia.

### Nivel 3 — Abstención

Si tras ambos niveles quedan reglas invictas que discrepan → `CONFLICT` y escalación. **El
disparador de escalación es sólo cobertura o conflicto, nunca "la respuesta fue
incorrecta"**, y esa restricción es exactamente lo que hace medible el error silencioso.
Un empate resuelto a ciegas es un error invisible; un conflicto declarado es un evento
contable y la señal que alimenta el aprendizaje.

### Lo medido, y sobre qué superficie

Subsunción + 199 aristas mínimas declaradas: **e2e 1.0000, error silencioso 0.0000, cero
conflictos, cero impasses** — **sobre el corpus de 2000**, que es lo único que
`peldano2/ceiling_check2.py` mide. Sobre el espacio exhaustivo ese motor **no se ha medido
nunca**. Por el convenio de la cabecera de este informe, y a la vista de lo que el §6
demuestra sobre transferencia entre superficies, la formulación correcta no es "el
mecanismo está cerrado" sino:

> **El mecanismo ejecuta sin error la declaración de un autor perfecto sobre la
> distribución de llegada.** Que lo haga también como función sobre las 134.400
> combinaciones es plausible —el orden declarado deriva del orden de capas, y
> *first-match-wins* sí está verificado sobre todo el espacio— pero no está medido, y
> medirlo cuesta cero llamadas.

Dos detalles de implementación que vale la pena dejar escritos porque no son obvios:

- **La transitividad sale gratis.** Si A vence a B y B vence a C, ambas quedan derrotadas
  y sólo A permanece invicta; no hace falta calcular el cierre transitivo.
- **Las aristas son globales pero su efecto es local.** `decide` sólo considera las
  derrotas *entre las reglas que casaron en este caso*. La misma regla puede ser invicta en
  un caso y derrotada en otro: la prioridad es un grafo, no una tabla de méritos absolutos.

---

## 4. Dónde encaja esto en la tradición

El peldaño 1 y el 2, juntos, son una réplica empírica de por qué las lógicas rebatibles
llevan una **relación de superioridad explícita** y por qué Drools tiene `salience`: los
criterios que reconstruyen la prioridad desde la forma de las reglas caen sobre una
política estratificada, y el que aguanta es el que la declara.

Una precisión sobre esa réplica, para no reclamar más de lo que hubo: los tres criterios
falsados aquí fueron **especificidad, orden de llegada y subsunción**, y ese no es
exactamente el trío clásico de los sistemas de producción —donde la terna canónica es
refracción, recencia y especificidad—. La subsunción no es una estrategia OPS5: es un
criterio semántico que este proyecto añadió y que resultó ser el único de los tres con
soundness sobre una política bien escrita. La coincidencia con la tradición es en la
conclusión, no en el conjunto de criterios probados.

| mecanismo | origen | qué hace con el conflicto | dónde se rompe |
|---|---|---|---|
| Especificidad | OPS5, CLIPS, Jess | gana la de más condiciones | invierte con overrides anchos (peldaño 1) |
| Recencia / antigüedad | OPS5 (LEX/MEA) | gana la más reciente o la más antigua | en una base aprendida corre **hacia atrás** |
| First-applicable | XACML, iptables, listas de ACL | gana la primera de la lista | el orden textual **es** la prioridad; insertar en medio rompe la semántica |
| `salience` | Drools | entero explícito; empate → LIFO | infalsificable; compite con cualquier otro criterio |
| Relación de superioridad `>` | lógica rebatible (Nute, Antoniou) | aristas entre reglas concretas | hay que declararla: alguien tiene que escribirla |
| Preferencias en ASP | asprin, LPOD | orden sobre modelos | expresivo y caro; fuera del alcance del motor barato |
| Combinación de resultados | XACML (`deny-overrides`…), Cerbos | combina **decisiones**, no reglas | no expresa jerarquía entre reglas |
| **Subsunción + aristas + abstención** | este repositorio | `ACTION` si las invictas acuerdan; si no, `CONFLICT` | requiere extensiones calculables; sobre base aprendida cuesta cota; el `CONFLICT` es carga si nadie lo rellena |

Una precisión que conviene no perder: **los algoritmos de combinación de XACML no son
comparables con la subsunción**. `deny-overrides` combina *resultados* de políticas;
la subsunción ordena *reglas*. Son objetos de tipo distinto, y la analogía "la subsunción
es la denegación no negociable" confunde más de lo que aclara.

Lo que el repositorio aporta al cuadro y no estaba: **la medida de cuánto queda por
declarar** una vez la semántica ha dicho lo suyo (85% de los pares sobre la política
oculta), la constatación de que ese residuo es *pequeño en aristas* pero *no lo produce
nadie automáticamente*, y **el precio del nivel semántico sobre una base sin autor**, que
es la parte que ninguna de las tradiciones de arriba mide porque todas suponen una base
escrita por alguien.

---

## 5. El cuello de botella no es el mecanismo: es el material

El mecanismo es la parte visible y elegante, y por eso se lleva la atención. Los registros
señalan a otro sitio.

El peldaño 2 construyó el motor que ejecuta prioridad declarada (1.0000, corpus) **y en el
mismo movimiento eliminó el material que lo ejercita**. Mostrarle la base al proponente bajó
el solape entre sus reglas de 17.5% de los pares a **1.60%**; instruirle explícitamente a
solapar lo recuperó hasta 7.25%, sin llegar a la mitad del punto de partida. Sin solape no
hay conflicto, y sin conflicto no hay prioridad que declarar:

```
ocho runs · ~200 escalaciones
  conflictos totales      2
  aristas propuestas     14
  aristas ACEPTADAS       0
  EDGE_CONTRADICTS        0
```

**Y no es un fallo de capacidad del modelo.** Razona relacionalmente en cuanto tiene con
qué: cita reglas por identificador, argumenta que una debe perder contra otra, e incluso
identifica correctamente que la subsunción resuelve un anidamiento sin necesidad de
declaración. La v2 del prompt le entrega la aritmética de solape ya resuelta por el motor
—qué condiciones falla el ticket para cada regla, tamaño de cada extensión, qué pares son
disjuntos— y **cinco de las catorce aristas mal propuestas siguen siendo de v2**.

El diagnóstico correcto es más incómodo que "no sabe calcular el solape": **la operación
que ejecuta —encontrar un hueco y rellenarlo— no requiere calcularlo**, y es la operación
que ejecuta incluso cuando se le pide otra. Trata la base como un mosaico incompleto, no
como una pila de capas.

*(`STATUS.md` mantiene el porqué de eso como pregunta abierta y sin discriminar entre tres
candidatos: el encuadre de la tarea —un ticket, una regla—, el modelo concreto, o la
elicitación por escritura de reglas en general. La afirmación "no es capacidad" está
sostenida por los dos argumentos de `FINDINGS2`; la explicación no la tiene nadie.)*

Consecuencia de diseño, y es la que ordena todo lo demás:

> **Toda capa adicional de arquitectura de arbitraje es capacidad añadida a un mecanismo
> que ya ejecuta sin error y sin alimentar.** Antes de decidir mejor quién gana el
> conflicto hay que conseguir una base donde las reglas se pisen.

### La palabra "material" significa dos cosas y conviene no fundirlas

Lo de arriba es **material de solape**: reglas que compiten, sin las cuales no hay arista
que declarar. Hay un segundo problema de material, de otra naturaleza y medido aparte
(`results3/FINDINGS3.md` §2, corpus): para **66.7% de `T3_ENGINEERING` y 64.2% de
`ACCOUNT_MANAGER` no existe ninguna regla correcta que cubra el caso**. Ahí no falta
solape, falta regla, y ningún orden, ninguna arista y ningún árbitro los recupera. Seis
clases de ocho —1774 de 2000 casos— sí son problema puro de ordenación; esas dos no.

La distinción importa para leer cualquier propuesta: P1 y P2 atacan el material de solape,
y no tocan el segundo. Nada en este informe lo toca.

### Y el hueco mayor no es de arbitraje

Conviene decirlo aunque quede fuera del alcance del informe: la pregunta original del
proyecto —si las reglas que escribe el LLM se reutilizan o memorizan casos— **sigue sin
medirse limpiamente** (`STATUS.md`, "What this does not show"). El 0.158 de reutilización
del peldaño 1 describe el arbitraje, no la inducción, porque 594 de sus 632 escalaciones
fueron CONFLICT. Un informe sobre arbitraje puede cerrar el arbitraje y dejar el proyecto
igual de lejos de su propia hipótesis.

### Corolario sobre un instrumento no validado

`EDGE_CONTRADICTS` nunca ha incrementado en ninguna ejecución, no porque el proponente
acierte sino porque la situación en que puede incrementar no se alcanzó. Cualquier
conclusión que se apoye en él está apoyada en un contador que nadie ha visto funcionar.

---

## 6. Por debajo de todo: el orden no está identificado

Este es el resultado que menos atención recibe y el que más restringe lo que se puede
construir encima.

Sobre el espacio exhaustivo, dos órdenes finales de la misma búsqueda **a un caso de train
de distancia** deciden distinto **11.240 de 134.400 casos (8.36%)**; en otro split, a tres
casos, 10.74%. Los 65 órdenes finales son **65 firmas de comportamiento distintas**: no hay
dos que sean la misma máquina, y lo mismo vale para los 257. Y con presupuesto bajo es
brutal: con 10 etiquetas, los **40 órdenes que empatan en el mejor score de train discrepan
entre sí en una mediana del 39.2% del espacio** (24.05% del corpus). La búsqueda no se está
absteniendo; está eligiendo arbitrariamente entre respuestas muy distintas y aterrizando en
un default sensato por accidente del orden de arranques.

Tres consecuencias, y ninguna es cosmética:

1. **El nivel es un resultado; el orden es un sorteo.** Un lector de la cifra 0.8530 puede
   fiarse de ella —con la salvedad que `STATUS.md` le adjunta: es el mejor de 65 arranques,
   acotada por un sorteo y no por convergencia—. Un lector del orden hereda la extracción
   entera. Y el peldaño 4 consume órdenes, no cifras.
2. **La verificación es más dura que el arbitraje.** Un verificador que compruebe
   aciclicidad, invariantes y ausencia de regresiones sobre casos históricos **certifica a
   los 40 con la misma alegría**. El objetivo no identifica la respuesta, así que la
   autoridad del verificador es menor de lo que su nombre sugiere. Cualquier diseño que
   ponga "el verificador es la autoridad" en su principio central tiene que decir contra
   qué verifica.
3. **La superficie no es un detalle de medición.** Los mismos 2.080 pares agrupan a 20.35%
   del espacio y 5.75% del corpus, y las clases que cargan la discrepancia son otras
   (`SECURITY_INCIDENT` 57.5% en el espacio, 4.6% en el corpus). Peor: **el orden tampoco
   transfiere** —Spearman corpus↔espacio de **0.3364**— así que el espacio no puede ni
   rankear dos órdenes para despliegue. Un estadístico de rango decente **no** es evidencia
   de transferencia; es necesario, no suficiente.

**Y la cuarta parte de ese registro dice de dónde sale exactamente la brecha**, que es lo
que hace accionable el punto 3 en vez de sólo alarmante. Medidos los mismos 2.080 pares
sobre el espacio **restringido a los 1.743 puntos que el corpus toca** —1.30% del espacio,
cada punto contado una vez— los pares discrepan en **5.68%**, contra 5.75% de las llegadas
y 20.35% del espacio entero. Es decir: **el nivel transfiere a la distribución de llegada
antes de aplicar ningún peso de clase**, y el 98.6% de la brecha es *qué puntos se
muestrean*, no cuántas veces. Lo cual cierra una puerta y abre otra: no existe un factor
por clase que convierta una superficie en la otra —reponderar por clase deja +1.4% sobre
los puntos tocados y +103% sobre el espacio entero—, así que el registro del espacio más
las frecuencias de clase **sigue sin llegar** a 5.75%. La corrección sólo la identifica el
corpus.

---

## 7. Propuestas

**Nada de esta sección está medido, y ninguna de estas predicciones está firmada.** El
convenio del repositorio para que una predicción cuente es estricto: banda con su línea de
refutación, escrita y firmada **antes de que exista la cifra**, y firmada por Sergi —un
modelo redactando la predicción destruye el propósito del archivo (regla dura 2 de
`CLAUDE.md`). Lo que sigue son borradores direccionales: para entrar en el marcador de
`STATUS.md` a cada uno le falta la banda numérica y la firma.

Ordenadas por lo que atacan: P1 y P2 van al material de solape, P3 al precio del nivel 1,
P4 a la identificabilidad, P5 al instrumento.

### P1 · Elicitación por **caso testigo**, no por aritmética abstracta

En vez de preguntar "¿se solapan R3 y R7 y quién gana?", **materializar un ticket de
`ext(R3) ∩ ext(R7)` y preguntar la cola**. La respuesta *es* la arista. El motor ya enumera
las 134.400 combinaciones con máscaras de bits, así que el testigo es una operación
determinista y gratis.

*Por qué podría funcionar:* convierte una relación abstracta entre extensiones, que el
proponente falla, en un ticket concreto.

**Dos objeciones que hay que poner delante, porque salen del registro y son duras.**

*Primera: la operación de destino tampoco está demostrada.* `results/llm_run.json` mide
exactamente eso —un ticket delante, la cola por decidir— en
`proposal_action_accuracy` = **0.3877** sobre 632 escalaciones. Y la comparación es
especialmente pertinente, no analógica: 594 de esas 632 escalaciones fueron CONFLICT, es
decir casos de contienda, que es justo lo que un testigo materializa. La premisa "es la
operación que demostradamente contesta" es falsa tal cual: es otra operación que también
falla, sólo que falla distinto.

*Segunda: la métrica obvia es degenerada.* Las 14 aristas rechazadas cayeron **todas** por
`no_solapan`. Un testigo extraído de la intersección garantiza solape por construcción, así
que `EDGE_DISJOINT` deja de ser alcanzable y la tasa de aceptación sube desde 0/14 haga lo
que haga el modelo. Y como el validador no puede comprobar que el ganador sea el correcto
(§3, nivel 2), lo que P1 produciría con un 39% de acierto son **aristas aceptadas y
falsas**: convertir un rechazo visible en un error silencioso, que es la conversión exacta
que este proyecto existe para evitar.

*Coste:* una llamada por par contendiente. *Predicción falsable, corregida:* **medir
corrección de la arista contra el orden de capas, no aceptación**. Sobre las 29 reglas
ocultas el ganador de cada par es conocido por construcción, así que el experimento es
barato y tiene verdad: si la tasa de aristas *correctas* por testigo no supera claramente
la tasa base de `proposal_action_accuracy`, el formato de la pregunta no era el problema y
P1 queda refutada. Si la supera, hace falta un segundo experimento antes de creerse nada:
el mismo protocolo sobre una base aprendida, donde no hay verdad contra la que comprobar,
para ver si el validador deja pasar más basura de la que filtra.

### P2 · Elicitación **diferida**, sobre el subgrafo vivo

No declarar prioridad al nacer la regla, sino cuando dos reglas contienden sobre un caso
real. *Es la misma disciplina de impasse que ya gobierna las llamadas al LLM, aplicada al
arbitraje: pagar sólo cuando hay que pagar.*

**El argumento de coste, corregido.** La versión fuerte —"el coste no es O(N²)"— no se
sigue de las cifras del repositorio. De los 166.176 pares de la base aprendida, **35.457
pueden cambiar una decisión sobre el espacio** (33.631 sobre el corpus): eso es el 21.3%,
una **fracción constante de la cuadrática**, no un orden menor. Y el otro dato que invita a
optimismo hay que leerlo con cuidado: sólo **25 a 53 reglas de 577 poseen territorio** bajo
un orden dado, pero eso es *por orden*, y la unión sobre los 65 órdenes finales es **406 de
577**. Qué reglas deciden algo depende del sorteo que documenta el §6.

Lo que sí sostiene la propuesta es más modesto y sigue siendo suficiente: el 21.3% es una
**cota superior de lo que puede importar**, no un conteo de lo que importará —hay pares
contendientes que no cambian ninguna decisión porque nada de lo que casan sobrevive a las
reglas de encima—, y sobre tráfico observado el conjunto que llega a contender de verdad es
otra criba más. La diferencia entre O(N²) declarado por adelantado y O(pares que contienden
sobre tráfico real) es empírica y está sin medir.

*Predicción falsable:* el número de aristas necesarias para alcanzar un e2e dado crece
sublinealmente en el tamaño de la base. **Falta la banda**: sin ella, "sublineal" se
adjudica a ojo.

### P3 · Imponer la disciplina de autoría en vez de suponerla

La subsunción da 53.12% de error silencioso sobre base aprendida —sobre el 8% de casos en
que se compromete— porque el convenio "regla estrecha = excepción" no se cumple. En lugar
de abandonar el criterio o de inferir mejor, **restringir la forma**: el validador rechaza
una regla que solape con otra sin declarar si es *excepción a* o *default bajo* cada una de
las que pisa. El motor ya sabe exactamente cuáles son.

Esto convierte un problema de inferencia en uno de declaración **con número de preguntas
acotado y localmente contestables**. Es la propuesta que más me convence de las cinco,
porque es la única que ataca una causa medida en vez de un síntoma.

*Dos predicciones, y son distintas: la segunda es la que importa y es la que nadie ha
planteado.*

1. *Soundness:* el error silencioso de la subsunción sobre una base así producida cae muy
   por debajo del 53.12%, **a cobertura comparable o mayor** —sin esa condición la
   predicción se cumple sola volviendo el criterio aún más mudo.
2. *Cota:* la brecha de 0.047 entre la cota híbrida (0.8540) y la pura (0.9010) se estrecha.
   Esta es la que decide si el nivel 1 deja de tener precio o simplemente deja de mentir. Si
   la soundness mejora y la cota no se mueve, P3 arregla medio problema y la subsunción
   sigue costando un tercio de la base.

### P4 · Restringir la clase de hipótesis a órdenes **k-estratificados**

Ahora se busca sobre órdenes totales de 577 reglas. Buscar sobre asignaciones a *k*
estratos (barriendo *k*) hace tres cosas: reduce el espacio, regulariza, y —lo decisivo—
**dentro de un estrato los empates no se rompen por índice: se declaran indecidibles y
escalan**. Eso convierte el problema de identificabilidad de invisible en medible: el número
de pares indeterminados pasa a ser una **salida** del sistema en lugar de una propiedad
oculta del orden de arranques.

**Ese es el valor de P4 y no depende de ninguna conjetura sobre la verdad.** Lo que sí
depende, y es el eslabón flojo: la política oculta tiene 8 capas sobre **29** reglas, y la
búsqueda corre sobre **577 reglas aprendidas** cuya relación con esas capas es desconocida
—de hecho el peldaño 2 documenta que el proponente particiona en vez de estratificar—. Que
el score aplane cerca de *k*≈8 sobre la base aprendida no se sigue de que la verdad tenga 8
estratos.

*Predicción falsable, con esa reserva declarada:* barriendo *k*, el número de máquinas de
comportamiento distintas colapsa respecto a las 65 y 257 actuales, y el score de test no
cae apreciablemente hasta *k* pequeño. Si el número de máquinas no colapsa, la
estratificación no es la estructura que falta. **Dónde aplana el score es dato, no
predicción**: si aplanara en 8 sería una coincidencia que valdría la pena mirar, no una
confirmación.

### P5 · Benchmark de conflictos con ganador conocido

Un conjunto de pares en conflicto con ganador y ámbito conocidos por construcción, medido a
niveles crecientes de información (sólo reglas / + ejemplos / + contraejemplos / +
procedencia). Sirve para responder algo que ahora no se puede: **qué información aporta
valor real al arbitraje**, en vez de suponerlo.

**Y es bastante más barato de lo que parece, porque el sustrato ya está construido.**
`peldano2/hidden_priority.py` clasifica los 406 pares de la política oculta en cuatro cajas
disjuntas: 112 de extensiones disjuntas, 61 ya ordenados por subsunción, 34 con la misma
acción (da igual quién gane) y **199 aristas declaradas con ganador conocido**, derivadas
del orden de capas. Eso es un benchmark etiquetado, hoy, a coste cero. Lo que falta no es
construirlo: es el protocolo de niveles de información y las bandas.

Dos condiciones para que no se convierta en un tablero de métricas sin filo: las bandas se
firman antes de que exista la cifra, y las filas sin banda van listadas aparte y fuera del
denominador —la convención que ya usa el hilo de predicciones.

---

## 8. Lo que descarto, y por qué

- **Entero de prioridad global** (con o sin aristas al lado): infalsificable, exige decisión
  global desde observación local, y compite con la subsunción en lugar de componer.
- **Crítico adversarial encarnado en un LLM**: el contraejemplo dentro de
  `ext(A) ∩ ext(B)` se **enumera** exactamente con las máscaras de bits que ya existen.
  Poner un modelo donde basta un procedimiento determinista invierte la economía entera del
  proyecto —simbólico barato primero, LLM sólo en impasse.
- **Prioridad contextual con ámbito** (`A > B si region=EU`): es una generalización real y
  válida para otros dominios, pero aquí la verdad **es** un orden total por capas, así que
  añade capacidad fuera de la verdad, no sólo fuera de la clase de hipótesis. Además rompe
  el chequeo de aciclicidad, que hoy es un DFS trivial y barato. Reservarlo para un dominio
  donde se haya demostrado que hace falta.
- **Cualquier pipeline de arbitraje de varias etapas** —detector, árbitro determinista,
  árbitro LLM, crítico, verificador, grafo, compilador, runtime— **construido antes de tener
  material**: es el peldaño 2 otra vez, a mayor escala. Construir el aparato y descubrir que
  no llega nada por la tubería ya ocurrió una vez, está documentado, y costó el único
  mecanismo del proyecto que funciona sin error. La tentación es fuerte precisamente porque
  el arbitraje es la parte que se deja diseñar sin datos.

---

## 9. Límites de este informe

1. **La política oculta puede ser adversarial a la especificidad por construcción.** En
   ella prioridad y número de condiciones son casi ortogonales *por diseño*. Eso hace
   correcta la falsación —basta un contraejemplo para tumbar "la especificidad es
   fiable"— pero no dice nada sobre con qué frecuencia las políticas reales tienen esa
   forma. Distinguir "falsado como criterio general" de "medida su tasa de fallo en el
   dominio" merece quedar escrito.
2. **El 1.0000 del motor híbrido es una cifra de corpus.** Sobre el espacio exhaustivo ese
   motor no se ha medido, y este informe ha sostenido en el §6 que las dos superficies ni
   siquiera rankean igual. Es la comprobación pendiente más barata de todas las que aquí se
   nombran.
3. **Las 199 aristas son el coste de autoría de un autor perfecto sobre 29 reglas.**
   Cuántas harían falta sobre una base aprendida, y si un proponente podría producirlas,
   es exactamente lo que las ocho ejecuciones nunca llegaron a poner a prueba. P2 sugiere
   que el coste real es menor que la extrapolación cuadrática, pero eso está por medir y el
   propio §7 rebaja el argumento.
4. **Un modelo, ocho ejecuciones de n=100.** Todo el peldaño 2 es `deepseek-v4-flash`. Que
   otro modelo particione igual es desconocido, y el número de reglas varía tanto entre
   semillas con prompt idéntico que esa cantidad es ruido.
5. **El precio del nivel 1 está medido sobre una sola base aprendida.** Los 0.047 de cota y
   las 181 reglas silenciadas son propiedades de las 577 reglas que produjo el peldaño 1
   bajo arbitraje por especificidad. Una base nacida bajo otro arbitraje sería otra, y
   `FINDINGS` ya avisa de que esas mediciones son cotas, no simulaciones del bucle.
6. **Este informe no ha ejecutado nada.** Es una lectura de los registros, con las cifras
   contrastadas contra el `FINDINGS` que posee cada una y contra el código donde el código
   era la fuente (los seis verdictos del validador, la localidad de las aristas, la
   superficie de `ceiling_check2`). Todo lo de la sección 7 está sin medir y así está
   marcado.
