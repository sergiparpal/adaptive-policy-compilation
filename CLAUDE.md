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

---

## REGLAS DURAS — no negociables

**1. NO modificar la especificación congelada** sin autorización explícita:

    harness/hidden_policy.py    harness/domain.py       harness/dsl.py
    harness/shadow.py           harness/cache_baseline.py

Si crees que alguno tiene un bug, **párate y dilo**; no lo arregles por tu cuenta.

EXCEPCIÓN REGISTRADA: `dsl.py` tiene un defecto confirmado. `RuleEngine.decide`
arbitra por especificidad y devuelve CONFLICT antes de aplicar el desempate por
antigüedad, que queda inalcanzable justo cuando importaría. Está pendiente de
rediseño, no de parche. No lo toques hasta que Sergi lo autorice.

**2. NO rellenar `PREDICTION.md`.** Lo rellena Sergi, a mano, antes de la tirada
larga. Que un modelo escriba la predicción destruye el propósito del archivo. Si
está vacío cuando toque la tirada larga, **para y pídeselo**.

**3. NO paralelizar el bucle.** Es estrictamente secuencial: cada regla nueva
cambia si el caso siguiente escala o no. Concurrencia = semántica rota.

**4. NO cambiar la semilla (17) ni regenerar el corpus.** El determinismo es lo
que hace comparables las tiradas.

**5. NO ajustar prompt ni esquema antes de tener un resultado registrado.**
Primero se mide, luego se itera.

**6. Si los números salen mal, NO los arregles: repórtalos.** Un resultado
negativo es un resultado. Ajustar hasta que la curva quede bonita es exactamente
el fallo de Goodhart que este experimento estudia; no lo reproduzcas.

**7. La clave de API va en el entorno, nunca en un archivo del repo.**
`OPENROUTER_API_KEY` la exporta Sergi en su shell. No la escribas, no la leas en
voz alta, no la guardes.

---

## Secuencia, con paradas obligatorias

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

### Paso 1 — Estructura y verificación en seco

Comprueba que los módulos están dentro de `harness/` (con `__init__.py`). Si
quedaron planos, muévelos. Luego:

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

    pip install -r requirements.txt

Solo `openai` (OpenRouter es compatible con OpenAI). Verifica que
`OPENROUTER_API_KEY` existe en el entorno; si no, pídesela a Sergi — no la
gestiones tú.

### Paso 3 — Prueba corta

    python3 run_experiment.py llm --n 100

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

    python3 run_experiment.py llm --n 2000

Secuencial: cuenta minutos. Cuesta céntimos con `deepseek/deepseek-v4-flash`.

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

## Estado actual (5 de agosto de 2026)

El peldaño 1 tal como está especificado está MUERTO. La tirada de n=2000 quedó
anulada por techo del motor; ver `PREDICTION.md` para el registro completo.

Hallazgo de fondo: ningún criterio sintáctico recupera esta política. H01 (2
condiciones) debe ganar a H03 (1); H16 (1) debe ganar a H24 (2) — ninguna
función monótona de la especificidad satisface ambas. Y el arbitraje por orden
de llegada tampoco: mismas 29 reglas, orden de diseño 100%, orden inverso 12,8%,
orden aleatorio 49,3% de media sobre 200 muestras. En una base aprendida el
orden de llegada va al revés del correcto, porque los primeros casos vienen de
la distribución común y engendran reglas de defecto, mientras las excepciones
nacen tarde.

La compilación por impasse aprende reglas, pero no tiene ningún mecanismo para
aprender PRIORIDAD. En una política estratificada la estructura vive ahí.

El DSL no es el culpable: verificado exhaustivamente sobre las 134.400
combinaciones del espacio de casos que las 29 reglas en DSL son equivalentes a
sus lambdas y que primera-que-casa las reproduce exactamente. Fallo de
ejecución, no de representación.

NO re-corras el peldaño 1 con otro arbitraje sintáctico: fallará por lo anterior.
NO propongas rediseños no solicitados. El siguiente paso lo decide Sergi.

Todo lo demás —deriva de concepto, regret, ILP como competidor, detectores de
impasse empírico, ASP, activación real— está en `IDEAS.md` y no se toca.
