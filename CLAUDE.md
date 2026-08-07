# Contexto para Claude Code

## Qué es este proyecto

Experimento sobre **compilación adaptativa de políticas**: un motor simbólico
barato resuelve los casos que cubre; cuando no cubre uno (impasse), un LLM actúa
y escribe una regla nueva para que la próxima vez sí lo cubra.

**Hay cuatro peldaños cerrados.** El resto de este archivo describe la operativa
del peldaño 1, que sigue siendo válida como procedimiento pero **no** como estado
del proyecto:

| peldaño | qué midió | registro |
|---|---|---|
| 1 | el motor por especificidad da 58,75% con la política perfecta cargada; la tirada quedó anulada | `results/FINDINGS.md` |
| 2 | motor híbrido (subsunción + prioridad declarada) al 100%, pero el proponente escribe reglas disjuntas y no lo ejercita | `results2/FINDINGS2.md` |
| 3 | las 577 reglas del peldaño 1 admiten un orden que saca 0,77 en test; cota de cobertura 0,90 | `results3/FINDINGS3.md` |
| 4 | ese orden no se aprende del feedback asimétrico que da un sistema real | `results4/FINDINGS4.md` |

**Cada FINDINGS lleva erratas fechadas en el sitio.** Los peldaños 3 y 4 tienen
cifras cuestionadas por un desempate no determinista, corregido el 6 de agosto de
2026 y **sin re-correr**. Léelas antes de citar cualquier número.

**La hipótesis original —¿las reglas del LLM se reutilizan o memoriza casos?—
sigue sin medirse limpiamente.** El peldaño 1 quedó anulado por techo del motor y
su reutilización de 0,158 describía el arbitraje, no la inducción.

Lee `README.md` antes de tocar nada, y el bloque "Estado actual" al final de este
archivo antes de proponer nada. `IDEAS.md` lleva la lista de lo abierto.

**La operativa de los peldaños 2, 3 y 4 no está en este archivo**, que solo
describe la del 1. Está en el README, sección "Reproducir los cuatro peldaños".
Todo lo de esos tres peldaños cuesta cero llamadas a la API y corre con la
biblioteca estándar:

    python3 -m peldano2.ceiling_check2      # techo del motor híbrido: 100%
    python3 -m peldano3.order_search        # cota de cobertura y orden buscado
    python3 -m peldano4.sweep               # barridos del canal de feedback

---

## REGLAS DURAS — no negociables

**1. NO modificar la especificación congelada** sin autorización explícita:

    harness/hidden_policy.py    harness/domain.py       harness/dsl.py
    harness/shadow.py           harness/cache_baseline.py

Si crees que alguno tiene un bug, **párate y dilo**; no lo arregles por tu cuenta.

DEFECTO REGISTRADO EN `dsl.py`, YA SUPERADO: `RuleEngine.decide` arbitra por
especificidad y devuelve CONFLICT antes de aplicar el desempate por antigüedad,
que queda inalcanzable justo cuando importaría.

**El rediseño ya se hizo, en el peldaño 2**, como paquete aparte
(`peldano2/engine2.py`: subsunción como orden base + prioridad declarada), y da
100% con la política perfecta cargada. Se hizo fuera de `harness/` precisamente
para que `dsl.py` siguiera congelado.

Así que `dsl.py` **se sigue sin tocar**, pero por el motivo contrario al que
decía esta nota antes: no porque quede trabajo pendiente ahí, sino porque es
registro cerrado del peldaño 1 y sus cifras deben seguir reproduciendo.

**2. NO rellenar `PREDICTION.md`.** Lo rellena Sergi, a mano, antes de la tirada
larga. Que un modelo escriba la predicción destruye el propósito del archivo. Si
está vacío cuando toque la tirada larga, **para y pídeselo**.

**3. NO paralelizar el bucle.** Es estrictamente secuencial: cada regla nueva
cambia si el caso siguiente escala o no. Concurrencia = semántica rota.

**4. NO cambiar la semilla (17) ni regenerar el corpus.** El determinismo es lo
que hace comparables las tiradas.

Por la misma razón, **NO sobrescribas `results/llm_run.json`**. No es solo el
registro del peldaño 1: es la base de 577 reglas de la que **parten los peldaños
3 y 4**. `run_experiment.py llm` lo reescribe, y como el proponente no es
determinista a temperature 0, lo que salga no será lo mismo. Si hay que
re-correrlo, se guarda el original antes con otro nombre.

**5. NO ajustar prompt ni esquema antes de tener un resultado registrado.**
Primero se mide, luego se itera.

**6. Si los números salen mal, NO los arregles: repórtalos.** Un resultado
negativo es un resultado. Ajustar hasta que la curva quede bonita es exactamente
el fallo de Goodhart que este experimento estudia; no lo reproduzcas.

**7. La clave de API va en el entorno, nunca en un archivo del repo.**
`OPENROUTER_API_KEY` la gestiona Sergi. No la escribas, no la leas en voz alta,
no la guardes.

CÓMO LLEGA, EN LA PRÁCTICA — está registrado porque cuesta un rodeo largo
descubrirlo. Un `export` en la terminal interactiva de Sergi **no** llega a tu
shell: son procesos distintos. Y aunque la tenga en `~/.bashrc`, la guarda de
Debian en las líneas 5-9 de ese archivo hace `return` para shells no
interactivas, así que su `export` nunca se ejecuta en la tuya.

Lo que sí funciona, cargándola en el entorno del proceso sin imprimirla nunca:

    eval "$(grep -m1 '^export OPENROUTER_API_KEY=' ~/.bashrc)"

Comprueba con `${#OPENROUTER_API_KEY}` (la longitud), nunca con su valor.

---

## Secuencia, con paradas obligatorias

### Paso previo — La suite (cero llamadas, ~12 s)

    python3 -m unittest discover

247 pruebas con la biblioteca estándar. No escriben en `results*/`: llaman a las
funciones de medida, nunca a los `main()`. Clavan los invariantes (el DSL
reproduce las lambdas sobre las 134.400 combinaciones) y las cifras publicadas
(0,5875 · 0,6315 · 1,0000, la frontera y el corpus), vigilan que ningún
componente del bucle online importe el oráculo, y replican las tiradas
registradas del LLM —`results/llm_run.json` y `results2/llm_run2_n100.json`—
regla a regla y registro a registro, sin gastar un céntimo.

Si algo falla aquí, para: los Pasos 0 y 1 medirían sobre un arnés que ya no
reproduce. **Un snapshot que falla no se actualiza**; se averigua qué cambió y,
si el cambio es legítimo, se fecha la errata en el FINDINGS que publica la cifra.

**No hace falta acordarse de lanzarla.** El hook `.githooks/pre-commit` la corre
antes de cada commit (se activa una vez con `git config core.hooksPath
.githooks`) y `.github/workflows/pruebas.yml` en cada push. Si el hook aborta un
commit, `--no-verify` **no** es la respuesta por defecto: ver el párrafo
anterior.

### Paso 0 — Techo del motor (OBLIGATORIO antes de cualquier tirada con LLM)

    python3 -m harness.ceiling_check

Carga la política oculta verdadera en el motor y mide su exactitud sin ningún
LLM de por medio. Si el motor no puede ejecutar la política correcta, ninguna
medición sobre reglas aprendidas significa nada.

Cuesta cero llamadas a la API. Se corre ANTES de gastar un céntimo, y se vuelve
a correr después de CUALQUIER cambio en el DSL, en el arbitraje o en la política
oculta.

**Techo actual medido (5 ago 2026): 58,75% de exactitud, 25,3% de CONFLICT.**
El arbitraje por especificidad no puede ejecutar una política priorizada por
capas. Mientras ese número no sea ~100%, toda tirada con LLM queda anulada de
antemano.

**PARADA 0.** Si el techo no es ~100%, para y dilo. No sigas al Paso 1.

### Paso 1 — Verificación en seco

    python3 run_experiment.py frontier

**Resultado esperado, exacto** (semilla 17, n=2000). Si no coincide, algo se
corrompió al copiar: para y avisa.

    corpus: 2000 casos, 1743 únicos, 12.8% duplicados
    keep_k(k=4)   113 reglas   reuso 0.796   err.sil 0.173   escal 0.057
    keep_k(k=5)   304 reglas   reuso 0.724   err.sil 0.157   escal 0.152
    cache(d<=2)   211          —             err.sil 0.448   escal 0.105

ADVERTENCIA: estas cifras siguen siendo reproducibles, pero NO son una
referencia válida mientras el techo del Paso 0 no sea ~100%. Todas las reglas de
keep_k tienen exactamente k condiciones, así que su especificidad es uniforme y
el arbitraje nunca puede invertir prioridades: los mocks son estructuralmente
inmunes al defecto que destroza la política real. De hecho keep_k(k=4) puntúa
MEJOR que la política verdadera bajo este motor (0.173 frente a 0.214 de error
silencioso). La "región a batir" está por encima del techo del sistema.

**PARADA 1.** Reporta si coincide.

### Paso 2 — Dependencias

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt

Solo `openai`, clavado en `openai==2.53.0` (OpenRouter es compatible con
OpenAI). Para reconstruir el entorno de los registros al dígito, instala
`requirements.lock.txt` en su lugar: lleva el cierre transitivo completo.

**El venv no es opcional**: en Debian/Ubuntu `pip install` global falla con
`externally-managed-environment` (PEP 668). El Paso previo y los Pasos 0 y 1 no
lo necesitan —van con la biblioteca estándar—; del Paso 3 en adelante, sí.

Verifica que `OPENROUTER_API_KEY` llega al entorno del proceso (ver regla 7); si
no, pídesela a Sergi — no la gestiones tú.

### Paso 3 — Prueba corta

    .venv/bin/python run_experiment.py llm --n 100

Cuesta céntimos. **No juzgues la reutilización aquí**: con 100 casos casi ninguna
regla tiene ocasión de dispararse dos veces. Esta tirada sirve para tres cosas:

- que el parseo funcione (`failed_proposals` y `rejected_rules` bajos)
- **leer 5-8 reglas de `results/llm_run.json` con su campo `note`**
- ver si el modelo usa `lte`/`gte`/`in` o solo `eq`

AVISO: el modelo NO es determinista a temperature 0. Verificado el 5 ago 2026 —
mismo prompt, mismo caso, misma semilla, reglas distintas entre la tirada de 100
y la de 2000. La prueba corta no es un prefijo de la larga. Esto afecta a
cualquier comparativa entre modelos: el modelo no será la única variable a menos
que se promedien varias semillas de muestreo.

**PARADA 2.** Pega las reglas leídas y di si el modelo parece inducir estructura
o transcribir tickets. Espera respuesta antes de seguir.

### Paso 4 — Tirada completa

Solo si el Paso 0 dio ~100%, `PREDICTION.md` está relleno y Sergi lo aprueba.

    .venv/bin/python run_experiment.py llm --n 2000

Secuencial: cuenta minutos. Cuesta céntimos con `deepseek/deepseek-v4-flash`.

**Antes de lanzarlo, releer la regla 4**: este comando sobrescribe
`results/llm_run.json`, que es la entrada de los peldaños 3 y 4.

### Paso 5 — Lectura

`results/llm_run.json` guarda los registros crudos por caso: cortes por clase,
por regla o por decil se hacen **post-hoc, sin volver a pagar la tirada**.

Suelo de memorización: `keep_k(k=8)` saca 0.118 de reutilización sin inducir
nada, puro efecto de los duplicados del corpus. Cualquier cifra cercana a 0.118
es ruido, no aprendizaje.

Separa siempre los dos ejes de error y no los mezcles: `proposal_action_accuracy`
mide elegir mal la cola al proponer; el error silencioso mide alcance. Los mocks
reciben la acción correcta gratis y el LLM no.

Presta atención especial a `ONCALL_ESCALATION` (7 casos de 2000) y
`SECURITY_INCIDENT` (20). Son las clases más críticas y las más raras; el
agregado las esconde. En la tirada anulada, la compilación destruyó capacidad:
SECURITY_INCIDENT dio 3/3 aciertos cuando el caso llegó al LLM y 0/17 cuando lo
resolvió una regla compilada.

---

## Estado actual (7 de agosto de 2026)

Cuatro peldaños cerrados. El hilo que los une: **la prioridad de una política por
capas no está en la forma de las reglas**, y las tres vías de suministrarla están
medidas y fallan cada una por una razón distinta.

**Peldaño 1 — inferirla de la sintaxis. Falla.** Ningún criterio sintáctico
recupera esta política. H01 (2 condiciones) debe ganar a H03 (1); H16 (1) debe
ganar a H24 (2) — ninguna función monótona de la especificidad satisface ambas.
El arbitraje por orden de llegada tampoco: mismas 29 reglas, orden de diseño
100%, orden inverso 12,8%, orden aleatorio 49,3% de media sobre 200 muestras. En
una base aprendida el orden de llegada va al revés del correcto, porque los
primeros casos vienen de la distribución común y engendran reglas de defecto,
mientras las excepciones nacen tarde. La tirada de n=2000 quedó anulada por techo
del motor; ver `PREDICTION.md`.

El DSL no es el culpable: verificado exhaustivamente sobre las 134.400
combinaciones del espacio de casos que las 29 reglas en DSL son equivalentes a
sus lambdas y que primera-que-casa las reproduce exactamente. Fallo de
ejecución, no de representación.

**Peldaño 2 — que la declare el proponente. El mecanismo funciona; el proponente
no lo alimenta.** Subsunción más 199 aristas declaradas ejecutan la política al
100%. Pero con la base delante, la aritmética de solape resuelta y la instrucción
explícita de solapar, el proponente escribe reglas mayoritariamente disjuntas y
lo argumenta como mérito. Ocho tiradas, dos conflictos, cero aristas aceptadas.

**Peldaño 3 — buscarla sobre el corpus. El material sí la contenía.** Las mismas
577 reglas que el arbitraje convertía en 0,18 admiten un orden que saca 0,77 en
test con gap ~0. `SECURITY_INCIDENT` y `ONCALL_ESCALATION` son 100% recuperables
y dieron 0/17 y 0/7. Pero la búsqueda usa el oráculo.

**Peldaño 4 — aprenderla del comportamiento observado. No con feedback real.**
Con supervisión simétrica se recupera casi todo (+0,235); con la asimétrica, que
es la única que un sistema real produce, quedan +0,067, y la señal se agota
conforme el sistema mejora.

La compilación por impasse aprende reglas, pero no tiene ningún mecanismo para
aprender PRIORIDAD. En una política estratificada la estructura vive ahí.

**La hipótesis original —¿las reglas del LLM se reutilizan o memoriza casos?—
sigue sin medirse limpiamente.**

### Qué sigue prohibido y qué se levantó

NO re-corras el peldaño 1 con otro arbitraje sintáctico: fallará por lo anterior.

**Levantado el 6 de agosto de 2026, al abrir el peldaño 2:** la prohibición de
proponer rediseños y la excepción sobre `dsl.py`. Sergi las levantó
explícitamente para ese trabajo. No las restablezcas por tu cuenta ni las des por
vigentes; **el alcance de cada apertura lo fija Sergi al abrirla**, y hasta
entonces la norma sigue siendo no proponer rediseños no solicitados.

Lo pendiente y lo abierto está en `IDEAS.md`, incluido lo que cada peldaño dejó
sin resolver. De la lista original solo se ha tocado el impasse empírico
—parcialmente, en el peldaño 4—; deriva de concepto, regret, ILP como competidor,
ASP y activación real siguen sin hacerse.
