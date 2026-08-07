# Aparcadero

Estado a 7 de agosto de 2026. Peldaños 1, 2, 3 y 4 cerrados; ver
`results/FINDINGS.md`, `results2/FINDINGS2.md`, `results3/FINDINGS3.md` y
`results4/FINDINGS4.md`. Esto es una lista de cosas no hechas, sin desarrollar
ninguna y sin orden de prelación.

---

## Ya no está aquí

- **Dar al proponente la base de reglas existente como contexto.** Peldaño 2.
  Redujo el solape entre sus reglas en un factor 10 y dejó sin material al
  mecanismo de prioridad declarada que ese mismo cambio venía a posibilitar.
- **Prioridad por búsqueda sobre el corpus, sin LLM.** Peldaño 3. Cota de
  cobertura 0,90 sobre las 577 reglas del peldaño 1 —cota superior caso a caso,
  no un óptimo alcanzable demostrado, ver la errata de `FINDINGS3.md`— y orden
  buscado 0,77 en test con gap ~0. La búsqueda usa el oráculo.
- **Prioridad aprendida del comportamiento observado.** Peldaño 4, Paso A. Con
  feedback simétrico se recupera casi todo; con el asimétrico, que es el
  realista, quedan +0,067 sobre no aprender nada.

---

## Pendiente y ya especificado

- **ILP (Popper/ILASP) sobre la política oculta y el corpus.** Era el Paso B del
  peldaño 3 y no se corrió. Dos medidas en una: si recupera el orden de capas, y
  como baseline competidor —qué acierto alcanza induciendo reglas él solo, sin
  LLM.
- **Orden online.** Era el Paso B del peldaño 4 y se decidió no correrlo: la
  asimetría ya responde la pregunta y el orden online solo degradaría más. Queda
  anotado que es un problema distinto del Paso A —la base crece mientras se
  ordena, y el feedback llega con retardo sobre decisiones que una versión
  anterior del orden tomó— por si el planteamiento cambia.
- **Re-correr los peldaños 3 y 4 con el desempate arreglado.** El arreglo está
  hecho y verificado —6 de agosto de 2026, iteración sobre lista ordenada,
  resultado idéntico bajo tres `PYTHONHASHSEED`— pero no se re-corrió nada, a
  propósito: hacerlo **junto con** el optimizador serio es lo que permite
  distinguir si la fragilidad venía del desempate o del algoritmo. Las cifras
  registradas son las del código anterior. Cuando se rehaga, la versión antigua
  se conserva al lado, no encima.

---

## Lo que el peldaño 4 abre y no resuelve

- El voraz es un optimizador débil, y eso contamina hacia atrás. Con etiquetas
  perfectas alcanza 0,7574 contra la verdad; con el 30% falsificadas, 0,8337. Un
  optimizador serio (búsqueda local, recocido, exacto sobre los pares que
  compiten) cambiaría todas las cifras de los peldaños 3 y 4. Se desconoce en qué
  dirección y en qué magnitud. Va junto con re-correr ambos peldaños, en
  "Pendiente y ya especificado".
- Si la conclusión sobre la asimetría sobrevive a un optimizador mejor. Es la
  única afirmación del peldaño 4 que importa y descansa sobre un método que se
  sabe débil, aunque su celda ancla sea determinista.
- El punto fijo del aprendizaje por corrección: la señal se agota conforme el
  sistema mejora. No se ha caracterizado dónde está ese punto ni de qué depende.
- Si existe algún régimen en que degradar deliberadamente π₀ para cosechar
  etiquetas compensa. El dato (π₀ peor produce mejor orden) lo sugiere y no se
  ha explorado.
- Si la ausencia de feedback puede usarse de alguna forma. Aquí se decidió no
  interpretarla como acierto; una interpretación probabilística no se ha probado.

---

## Lo que el peldaño 3 abre y no resuelve

- Cuánto del hueco 0,77→0,90 es realmente alcanzable. El 90,1% es una cota
  superior por cobertura caso a caso: garantiza que ningún orden lo supera, no
  que algún orden lo alcance. Haría falta optimización exacta o una cota global
  más fuerte. Ver la errata de `FINDINGS3.md`.
- Si el orden es alcanzable sin etiquetas. El bucle en sombra no tiene canal de
  supervisión por diseño. El peldaño 4 acotó parcialmente esta pregunta y la
  respuesta fue mala.
- Por qué el proponente no escribió reglas correctas para `T3_ENGINEERING` ni
  `ACCOUNT_MANAGER` (66,7% y 64,2% de esas clases sin ninguna regla correcta que
  las cubra). Es problema de material, no de orden, y no tiene explicación.
- Si un proponente al que se le señalan los huecos del techo los rellenaría.
- La función objetivo como superficie de diseño explícita: qué clases se
  protegen, con qué coste en agregado, y quién lo decide.
- Por qué el arbitraje híbrido del peldaño 2 es peor que el orden puro sobre una
  base aprendida (0,7496 frente a 0,7711) pese a ejecutar la política perfecta al
  100%.

---

## Lo que el peldaño 2 abre y no resuelve

- Por qué el proponente particiona en vez de estratificar. Candidatos no
  discriminados: el encuadre de la tarea (un ticket, una regla), el modelo
  concreto, o la elicitación de escritura de reglas en general.
- Si algún prompt o esquema consigue que un proponente que ve la base escriba
  reglas solapadas. Las versiones v1 y v2 acotan un rango; no lo agotan.
- Cómo conseguir una base que produzca conflictos, que es la condición para que
  `EDGE_CONTRADICTS` mida algo. Ocho tiradas y dos conflictos.
- Si n=100 basta. Las bases van de 6 a 40 reglas; el solape podría emerger solo
  al crecer la base.
- El coste de autoría a escala. 199 aristas declaradas para 29 reglas en el
  Paso 0; se desconoce para una base aprendida.
- Qué pasa cuando la subsunción y la declaración se contradicen en una base
  aprendida. Esa decisión de diseño no se ha puesto a prueba ni una vez.
- Los atributos que el proponente no usa: `language` en 0 de 8 tiradas,
  `channel` y `prior_tickets_30d` en 1 de 8.

---

## Deuda técnica

Trabajo pendiente **sobre el repo como software**, no sobre el experimento. Es
de otra naturaleza que el resto de este archivo y por eso va aparte. Real, pero
no cambia ninguna conclusión.

Los tres puntos que había aquí se cerraron el 7 de agosto de 2026. Quedan sus
consecuencias, que son de otro tamaño.

### Hecho

- **Pruebas automatizadas.** `python3 -m unittest discover` corre 186 pruebas en
  ~11 s, sin llamadas a la API y sin escribir en `results*/`. Cubren los dos
  invariantes que sostienen el peldaño 1 —el DSL reproduce las lambdas sobre las
  134.400 combinaciones, y primera-que-casa reproduce `true_action`— y clavan al
  dígito las cifras publicadas: 0,5875 por especificidad, 0,6315 por subsunción,
  1,0000 híbrido, la frontera de los mocks y el corpus. Añaden tres controles
  que no existían: que ningún componente del bucle online importe el oráculo,
  que `feedback.py` siga siendo el único módulo del peldaño 4 que lo toca, y que
  el voraz de los peldaños 3 y 4 no dependa de `PYTHONHASHSEED`.
- **Dependencias fijadas.** `openai==2.53.0`, más `requirements.lock.txt` con el
  cierre transitivo del entorno que produjo los registros. Una prueba impide que
  el `>=` vuelva por descuido.
- **Registro de entorno.** `harness/provenance.py` cuelga un bloque `_env` de
  cada JSON: Python, openai, plataforma, `PYTHONHASHSEED`, commit + dirty y un
  digest del código fuente. Una prueba recorre el repo y suspende si aparece un
  escritor de JSON sin él.

### Lo que eso deja abierto

- **Los registros publicados son anteriores a `_env`.** El campo aparecerá en
  cada archivo cuando esa cifra se vuelva a correr, no antes. No se re-corrió
  nada a propósito: reproducir una cifra sobrescribe su propio registro.
- **`comparativa.json` y `note_audit.json` cambian de forma al re-correrse.**
  Sus escritores pasaron de volcar una lista pelada a volcar
  `{"_env": ..., "rows": [...]}`, que es la única manera de colgarles
  procedencia. Los dos archivos registrados siguen siendo la lista antigua.
- **Los peldaños 3 y 4 están cubiertos por determinismo, no por snapshot.** Sus
  cifras publicadas son las del código anterior al arreglo del desempate y están
  pendientes de re-correr; clavar aquí los valores nuevos crearía una segunda
  cifra oficial que no respalda ningún FINDINGS. Cuando se rehagan ambos
  peldaños, esas pruebas pasan a snapshot.
- **Nadie corre las pruebas automáticamente.** No hay CI ni hook de pre-commit.
- **La ruta del LLM sigue sin prueba de extremo a extremo**, por definición: solo
  está probado el parseo, que es la parte pura. Un doble del proponente que
  devolviera respuestas grabadas cubriría el resto sin gastar.

Lo que **no** está aquí, a propósito: que reproducir una cifra sobrescriba su
propio registro. Es un comportamiento que hay que conocer, no una tarea
pendiente —git ya es la salvaguarda— y está documentado con su tabla completa en
el README.

---

## Anterior a los cuatro peldaños

De esta lista, lo único que se ha tocado es el impasse empírico, y solo en parte.
El resto sigue exactamente donde estaba.

- Peldaño de novedad: atributos o valores nuevos a mitad de corpus
- Deriva de concepto: la política oculta cambia en t=N/2 -> ¿retira reglas?
- Inexpresabilidad -> medir regret vs. mejor política representable
- Impasse empírico: canal de feedback parametrizado (cobertura, retardo, ruido).
  **Parcialmente hecho** en el peldaño 4, en modo offline y con un cuarto
  parámetro —asimetría— que resultó ser el que decide. Queda sin hacer en modo
  online y sin explorar el resto del espacio de parámetros.
- Diagnóstico bajo ambigüedad: ¿deriva o sobre-generalidad? Reparaciones opuestas
- Tirada comparativa con un modelo más capaz, con el MODELO como única variable
  (misma semilla, mismo prompt, mismo esquema, mismo corpus). Requiere promediar
  varias semillas de muestreo: el proponente no es determinista a temperature 0.
- Compilador a ASP (clingo) manteniendo el mismo esquema de entrada
- Promoción por generación dirigida de casos de prueba (generador independiente)
- Contabilidad de coste completa -> ¿existe un tamaño óptimo de base?
