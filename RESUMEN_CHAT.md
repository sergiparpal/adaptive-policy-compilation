# Resumen de conversación — 11 de agosto de 2026

**Naturaleza de este documento:** es el resumen de una conversación sobre el
experimento, no un registro oficial. **Ninguna cifra de aquí tiene su hogar en
este archivo**: las figuras citadas pertenecen a los FINDINGS que las poseen y a
`STATUS.md`, que las indexa. Si alguna difiere, manda el registro. Las medidas
nuevas (§2, punto 1) son *probes* ad hoc no oficiales, reproducibles gratis, que
no están grabadas en `results*/` a propósito.

**Revisado el 12 de agosto de 2026.** Cada cifra citada se verificó contra el
registro que la posee y **ninguna había derivado**; el *probe* de §2.1 se
reprodujo exacto. Lo que falló fue la lectura, en tres sitios, y va corregido
abajo con su errata fechada y el texto original conservado, como en los FINDINGS:

- **§2.1** no nombraba su superficie, y sobre la otra la conclusión es mucho más
  fuerte. Se añade la medida que faltaba.
- **§2.2** citaba la mitad favorable de la evidencia de FINDINGS2, y el
  disparador que propone se queda sin material. Se añade la enmienda.
- **§4** encadena figuras de motores distintos: no hay un eslabón roto, hay
  cuatro sin medir.

La tabla de §3 se reordenó por ese motivo. En §1 se añadieron las etiquetas de
pool y superficie que el registro ya lleva y este resumen omitía —
`0.8530` es del **pool puro**, con la subsunción apagada, y ahí empieza el error
de §4.

**Actualizado el 14 de agosto de 2026, solo por estado.** La fila 1 de §3 seguía
pidiendo un experimento ejecutado el día 13, que `STATUS.md` ya había movido
fuera de sus abiertos: va marcada en su sitio, con puntero al registro que la
posee. Esto **no** es una re-verificación del documento —ninguna cifra se volvió
a comprobar—; la revisión del 12 de agosto sigue siendo la última.

---

## 1. Conclusiones a las que se llegó

**Sobre la arquitectura y sus cuatro peldaños:**

- La prioridad de una política estratificada **no está en la forma de las
  reglas**: ni contando condiciones (0.5875 con la política perfecta cargada),
  ni por antigüedad, ni por subsunción semántica. No son métricas malas: la
  información no está ahí. La prioridad es una relación *entre* reglas y solo
  entra por un canal externo: declaración, feedback o autoridad.
- **El mecanismo para ejecutar prioridad declarada funciona perfecto** (e2e
  1.0000, motor híbrido — subsunción + aristas declaradas — **sobre la política
  oculta de 29 reglas**). El problema nunca fue de ejecución; es de fuente:
  nadie suministra la declaración.
- **El proposer particiona en vez de estratificar.** Ver la base redujo el
  solape 10x; la instrucción explícita de solapar (prompt v2) movió los números
  (1.6% → 7.25%) pero no la operación, y las notas presumiendo de disyunción
  subieron del 22% al 55%.
- **El material era mucho mejor de lo que parecía**: las mismas 577 reglas que
  el arbitraje del peldaño 1 convertía en 0.18 admiten un orden de 0.8530
  (**pool puro** — subsunción apagada —, corpus test, optimizador auditado, y la
  búsqueda usa el oráculo). Bajo el motor híbrido esa misma base da **0.7734**.
  Pero dos clases (T3_ENGINEERING, ACCOUNT_MANAGER) carecen de material
  correcto: problema de material, no de orden.
- **Del feedback realista (solo errores) se recupera el 61%** de lo que da la
  supervisión plena, y la señal se autoextingue: cuanto mejor funciona el
  sistema, menos errores comete, menos correcciones llegan, menos aprende.

**Sobre la discusión epistemológica (la política oculta como "verdad"):**

- La política oculta no necesita ser "la correcta del universo": es **el manual
  de ESTA empresa**. Lo que se mide es si una función estructurada se puede
  recuperar de la experiencia, no si la política es buena. El mismo criterio
  con el mismo oráculo da 0% de error sobre la política escrita a mano y 53%
  sobre la base aprendida: la variable es la estructura del material, no el
  autor ni la objetividad de la verdad.
- **El conflicto no es el enemigo: es la alarma.** Particionar no elimina los
  errores — elimina el detector de errores. La partición limpia de 6 reglas con
  error silencioso 0.7553 es la prueba: cero conflictos, desastre silencioso.
- La subsunción falló sobre la base aprendida por dos motivos distintos: casi
  no había anidamiento que detectar (5.17% de los pares), y cuando lo había,
  coronaba reglas estrechas pero equivocadas. **Estrecha ≠ correcta.**

## 2. Lo que añadió la conversación y no estaba explicitado en el proyecto

1. **La medida de "la regla más nueva gana".** El FINDINGS del peldaño 1 decía
   conceptualmente que el orden de llegada corre al revés del correcto, pero
   nunca midió el reverso. Medido en la conversación (probe ad hoc, corpus
   completo, protocolo no oficial): **0.542 contra 0.5115** de born_at y 0.417
   aleatorio. Dirección correcta, magnitud pequeña: las excepciones nacen
   tarde, pero la mayoría de reglas nuevas no son excepciones.

   > **[ERRATA 2026-08-12] Dos cosas: el reverso sí estaba medido sobre otro
   > objeto, y este probe no nombraba su superficie.**
   >
   > **(a)** `results/FINDINGS.md` §2 publica `orden inverso 12.8%` — sobre la
   > **política oculta** cargada en el motor, donde invertir el orden de diseño es
   > catastrófico por construcción. Lo que nunca se había medido es el reverso
   > **sobre la base aprendida**, que es lo que mide este probe. La frase "nunca
   > midió el reverso" es falsa como está escrita y verdadera en su intención.
   >
   > **(b)** El probe reproduce exacto — corpus completo, 2000 casos, pool puro —
   > y añade la desviación que no reportaba:
   >
   > ```
   >   born_at               0.5115
   >   born_at INVERTIDO     0.5420
   >   aleatorio (media 50)  0.4172   desv 0.0711
   > ```
   >
   > La ventaja del reverso es **+0.0305** contra una desviación del orden
   > aleatorio de **0.0711**: menos de media desviación. Sobre el corpus esto no
   > es una mejora, es un signo. Medido sobre el espacio exhaustivo — la
   > superficie que `STATUS.md` obliga a nombrar desde el 8 de agosto, y que la
   > conversación no midió:
   >
   > ```
   >   born_at               0.3148
   >   born_at INVERTIDO     0.5668
   >   aleatorio (media 50)  0.3768   desv 0.1026
   > ```
   >
   > **+0.252, y casi dos desviaciones por encima del aleatorio.** La hipótesis
   > era correcta y estaba defendida sobre la superficie donde es más débil. La
   > lectura honesta se parte en dos: el reverso es una aproximación mucho mejor
   > **a la política**, y apenas mejor como **default de despliegue**, porque el
   > corpus es la distribución de despliegue según el encuadre del propio
   > proyecto. Es exactamente el mecanismo que la errata de `FINDINGS3.md`
   > describe: las reglas nacidas temprano son defaults ajustados a la
   > distribución común, que es lo que el corpus premia y una medida uniforme no.
   >
   > **Lo que la conversación no vio.** 0.5668 **sin una sola etiqueta y sin
   > búsqueda** supera al voraz del registro llevado al espacio (0.4931) y se
   > acerca a la búsqueda local ajustada sobre train del corpus (0.6105), que sí
   > usa el oráculo. Eso dice algo bastante más fuerte que "mejora gratuita sobre
   > born_at": una heurística sin etiquetas recupera la mayor parte de lo que
   > recupera una búsqueda con oráculo, en la superficie que pregunta si el orden
   > *es* la política.
   >
   > Mismo estatus que el probe original: protocolo no oficial, nada escrito en
   > `results*/`.

2. **La propuesta concreta de juicio por pares**: no pedirle al LLM que escriba
   reglas solapadas, sino detectar el conflicto y preguntarle "¿cuál de estas
   dos debe ganar?". La evidencia base está en FINDINGS2 (razona relacionalmente
   cuando tiene dos operandos); el diseño del experimento es síntesis de la
   conversación.

   > **[ERRATA 2026-08-12] La evidencia citada es la mitad favorable, y el
   > disparador propuesto se queda sin material.**
   >
   > FINDINGS2 da dos razones para que el fallo no sea de capacidad. Esto cita la
   > primera — razona relacionalmente: cita reglas por identificador y discute
   > sobre ellas. **La segunda es un experimento y corre en contra**: v2 le
   > entregó la aritmética del solape ya resuelta por el motor y **cinco de las
   > catorce aristas mal propuestas son de v2**, tres de ellas en escalaciones
   > donde el vecindario marcaba explícitamente qué condiciones fallaba cada
   > regla citada. *"Con la información correcta delante, comete el mismo
   > error"* (`results2/FINDINGS2.md`).
   >
   > Peor para este diseño en concreto: las dos únicas veces que un CONFLICTO
   > real llegó al proposer — exactamente la situación que el experimento quiere
   > crear — respondió con **cero aristas** una vez y **falló el parseo** la
   > otra. **0 de 2.** No es refutación (n=2, y la elicitación no era una
   > pregunta directa), pero es lo más cercano que hay a evidencia y no apunta
   > donde este punto dice.
   >
   > Y el disparador se queda seco: **2 conflictos en 8 runs**. Disparar por
   > CONFLICTO en tiempo de ejecución es la misma sequía que dejó a
   > `EDGE_CONTRADICTS` sin medir nada en ocho runs. Tal como está escrito, el
   > experimento **no repara el eslabón: es el eslabón**.
   >
   > **Enmienda, que lo deja más barato y con marcador.** Disparar por **solape
   > de extensiones**, calculado offline sobre los 134,400 casos — el motor ya lo
   > calcula para el vecindario v2 —, no por conflicto en ejecución. Y correrlo
   > **offline sobre la base de 577 reglas que ya está pagada**, donde el orden
   > buscado con oráculo (0.8530, pool puro, corpus test) da un marcador contra
   > el que puntuar el orden que el LLM declare, y born_at (0.5115) da el suelo.
   > Sin bucle de sombra nuevo, sin gasto de corpus y sin depender de conseguir
   > primero una base con solape — que es la dependencia circular que hundía la
   > versión original.

3. **La matriz con la celda vacía**: "base con solape sano + subsunción" es la
   combinación nunca medida — el prompt v2 corrió sobre el motor de subsunción
   pero nunca le dio material (2 conflictos en 8 runs, 0 aristas aceptadas).
4. **La conexión "especificidad medida de otra forma = subsunción"**: el
   refinamiento intuitivo (no contar condiciones sino medir especificidad de
   verdad) es exactamente el camino que el experimento ya recorrió, con su
   razón de fallo documentada.
5. **El encuadre "particionar mata la alarma"**: el diseño tenía el trigger de
   escalación solo por impasse/conflicto; la formulación de que la disyunción
   elimina el mecanismo de detección de errores es de la conversación.

## 3. Qué se podría hacer para seguir (por relación coste/valor)

**Reordenada el 12 de agosto de 2026.** El orden original era 1-6 tal como se
lee ahora en la columna «antes». Cambió por tres motivos: lo que puede
**retirar** una premisa publicada va antes que lo que puede añadir una capacidad;
el juicio por pares baja porque en su forma original dependía de conseguir una
base con solape y en la forma enmendada (§2.2) ya no; y el reverso de born_at
deja de venderse como default de despliegue, que es lo que la errata de §2.1 no
sostiene.

| # | antes | experimento | coste | qué descubriría |
|---|---|---|---|---|
| 1 | 4 | **Re-correr `budget_and_balance`** con el optimizador auditado: **ejecutado el 13 de agosto de 2026**, no pendiente | ya hecho · 0 llamadas | era: si "50 etiquetas bastan" sobrevive, la premisa sobre la que se abrió el peldaño 4. Lo midió el paso 3 de la auditoría — [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md), «Step 3 result — August 13, 2026» —, que es el registro que posee esas cifras |
| 2 | 1 | **Juicio por pares, en la forma enmendada de §2.2**: disparar por solape de extensiones, offline, sobre las 577 reglas ya pagadas | céntimos | si el proposer puede *declarar* prioridad aunque no la *escriba*. Puntuable contra 0.8530 arriba y 0.5115 abajo, sin depender de conseguir una base con solape |
| 3 | 2 | **Otro modelo** (mismo prompt v2, varias semillas promediadas) | céntimos | discrimina "es DeepSeek" vs "es la elicitación"; informativo en ambos casos |
| 4 | 3 | **Mostrar los huecos del techo** al proposer ("aquí no tienes regla correcta") | céntimos | si rellena el material que falta en T3/ACCOUNT_MANAGER (abierto en `IDEAS.md`). Es el único que ataca el problema de material, que ningún mecanismo de prioridad toca |
| 5 | 5 | **ILP (Popper/ILASP) como competidor** | gratis, especificado, no autorizado | si un inductor sin LLM recupera el orden de capas, ¿para qué el proposer? |
| 6 | 6 | **born_at invertido**: ya medido en §2.1, no pendiente. Lo que queda es decidir **qué es** | ya hecho | sobre el espacio, +0.252 sin etiquetas y sin búsqueda; sobre el corpus, dentro del ruido. No es un default de despliegue: es la evidencia más limpia de que born_at codifica la distribución y no la política |

> **[ESTADO 2026-08-14] La fila 1 está ejecutada, y con ella se gastan tres cosas
> que afirmaba.** El paso 3 de la auditoría la corrió el 13 de agosto de 2026;
> sus resultados y su errata fechada viven en
> [`results3/FINDINGS_AUDIT.md`](results3/FINDINGS_AUDIT.md) y en
> [`results3/FINDINGS3.md`](results3/FINDINGS3.md) §4, que son los registros que
> los poseen. Aquí no se copian, por lo que dice la cabecera de este documento.
>
> **(a)** Ya no es «el abierto nº 1 de `STATUS.md`»: ese índice la movió a lo
> establecido y su lista de abiertos empieza ahora por otra cosa. **(b)** Ya no es
> «el único ítem que puede retirar una figura publicada», porque retiró una; el
> resto de la tabla añade capacidad, no la quita. **(c)** La estimación de coste
> que traía la fila —reloj y número de configuraciones— no es la que salió; la
> real está en el registro, sección «What it costs, and what it does not settle».
>
> La fila se deja en su sitio y la tabla sin renumerar: sacarla borraría el motivo
> por el que se reordenó el 12 de agosto, que está escrito justo encima.

## 4. ¿Hay esperanza de que el experimento no termine sin éxito?

Sí, de dos maneras distintas:

**Ya tiene éxito como mapa.** La pregunta original (¿reutiliza o memoriza?)
sigue sin respuesta limpia, pero el proyecto ha delimitado exactamente por qué:
dónde vive la estructura (la prioridad), qué canales la transportan y cuánto
pierde cada uno (declaración: nunca llegó; feedback: 61% y se agota), y qué
parte del problema es de material y no de orden. Un resultado negativo bien
medido es un resultado (regla 6).

**Y hay camino abierto real para el éxito positivo.** La cadena solo tiene un
eslabón roto: *conseguir una base con solape real*. Si el juicio por pares (o
mostrar los huecos, u otro modelo) lo repara, todo lo demás ya está probado y
funciona: el motor híbrido ejecuta al 1.0000, la búsqueda auditada extrae
0.8530 del material, y el canal de feedback aporta su 61%. El experimento no
está muerto: está a **un eslabón** de cerrar la cadena, y por primera vez se
sabe exactamente cuál es.

> **[ERRATA 2026-08-12] Esto encadena figuras que no son encadenables. No hay un
> eslabón sin medir: hay cuatro.** Es la afirmación que más peso carga del
> documento y es la que peor aguanta el contraste con los registros.
>
> **(a) 1.0000 y 0.8530 son motores distintos.** El 1.0000 es el motor **híbrido**
> — subsunción + aristas declaradas — sobre la **política oculta de 29 reglas**.
> El 0.8530 es un orden total **puro**, con la subsunción apagada, sobre las 577
> aprendidas. Bajo el motor híbrido esa misma base da **0.7734**
> (`results3/FINDINGS_AUDIT.md`), y la subsunción deja **181 de las 577 reglas
> sin casar nada** en el train. Reparar el solape no te entrega un motor a 1.0000
> sobre una base aprendida: «por qué el arbitraje híbrido del peldaño 2 es peor
> que el orden puro sobre una base aprendida» sigue abierto en `IDEAS.md`, y la
> auditoría dice que sigue siendo peor con un optimizador competente y por un
> margen más ancho.
>
> **(b) El 61% no es un multiplicador de 0.8530.** Es una ganancia sobre born_at
> (+0.2011 de +0.3273), medida sobre la misma base vieja. Las dos cifras no se
> multiplican ni se componen.
>
> **(c) Las dos se midieron sobre la base del peldaño 1.** Una base nueva con
> solape real es material distinto; ni 0.8530 ni el 61% viajan con ella.
>
> **(d) El problema de material no se mueve.** §1 dice que a T3_ENGINEERING y
> ACCOUNT_MANAGER les falta regla correcta en dos tercios de sus casos, y aquí se
> escribe «todo lo demás ya está probado y funciona». Ningún mecanismo de
> prioridad toca eso.
>
> Y el 0.8530 usa el oráculo, que §1 sí etiqueta y este párrafo suelta.
>
> **Qué queda en pie.** El primer párrafo de esta sección — el éxito como mapa —
> no lo toca nada de esto. La dirección tampoco: hay camino y es barato. Lo que
> no se sostiene es la aritmética, y con ella el «a un eslabón». Cuatro cosas
> sin medir, tres de ellas identificadas, es un sitio bastante mejor que el
> peldaño 1; no es el borde de cerrar la cadena.

Apuesta informada de la conversación: el éxito, si llega, no vendrá de un
modelo más listo ni de un prompt mejor, sino de **cambiar la pregunta que se le
hace al LLM** — de "escribe la regla" a "juzga este par". Es lo más barato de
probar y es lo único que la evidencia del peldaño 2 dice que el proposer ya
sabe hacer.

> **[ERRATA 2026-08-12]** La apuesta sigue siendo razonable y sigue siendo lo más
> barato, pero «lo único que la evidencia del peldaño 2 dice que el proposer ya
> sabe hacer» es más de lo que la evidencia dice: ver la errata de §2.2 — con la
> aritmética resuelta delante repitió el error, y las dos veces que le llegó un
> conflicto de verdad no declaró nada. Apuesta con prior bajo, no conclusión.
