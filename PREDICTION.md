# Predicción registrada

Fecha: 5 de agosto de 2026
Tirada: n=2000, deepseek/deepseek-v4-flash, semilla 17

| magnitud                  | predicción | resultado |
|---------------------------|------------|-----------|
| reutilización             |    0,70    |   0,158   |
| nº de reglas              |     200    |     577   |
| error silencioso          |    0,30    |   0,484   |
| escalación último decil   |    0,20    |   0,670   |

Umbral de parada: si la reutilización < 0,30 , esto no está induciendo y el
proyecto se replantea.

Predicción informada, no ciega: hecha tras ver la tirada de n=100, el análisis
de R0002 (cubre el 19,1% del corpus, nació de un caso resuelto por el catch-all
H29) y el punto ciego de prior_tickets_30d (decide el 14,5% del corpus, usado 0
veces en 47 condiciones).

Frente a la predicción de Claude (0,5-0,7 de reutilización, exceso de reglas):
predigo reutilización más alta y menos reglas.

La tirada queda anulada por techo del motor.

## Anulación — verificada el 5 de agosto de 2026

La tirada NO mide la hipótesis. Con la política oculta perfecta cargada (29
reglas, ningún LLM), el motor alcanza 58,75% de exactitud y declara CONFLICT en
el 25,3% de los casos. El techo de error silencioso era ~0,41 aunque el modelo
hubiera inducido la política exacta. Obtuvo 0,484: quedó a ~7 puntos de un techo
inalcanzable.

Causa: `RuleEngine.decide` arbitra por especificidad (nº de condiciones). La
política oculta es una lista priorizada por capas, y prioridad y especificidad
son casi ortogonales en ella. Agravante: `decide` devuelve CONFLICT antes de
aplicar el desempate por antigüedad, así que el desempate es inalcanzable justo
cuando importaría. Eso convierte 83,2% en 58,75%.

El DSL NO es el culpable: verificado exhaustivamente sobre las 134.400
combinaciones del espacio de casos que las 29 reglas en DSL son equivalentes a
sus lambdas y que primera-que-casa las reproduce exactamente. Fallo de
ejecución, no de representación.

### Por qué el umbral de parada no se aplica

594 de 632 escalaciones (94%) fueron CONFLICT, que es justo lo que este
arbitraje sobreproduce. Conflicto → regla nueva → más solapamiento → más
conflicto. Reutilización, nº de reglas, reglas muertas, curva de escalación y
ambos contrafactuales de acción son productos de ese bucle. El 0,158 no mide si
el LLM induce o memoriza.

### Qué SÍ sobrevive (independiente del arbitraje)

- Generalización desde el residuo: la región `dashboard AND severity<=3` toca 15
  reglas ocultas y T1_GENERAL solo es verdad en el 21,5%. El caso de origen lo
  resuelve H29, el catch-all. El proponente ve una respuesta correcta y no puede
  saber que lo es por descarte. Ocurrió en las dos tiradas, de formas distintas.
- Ceguera atributiva: prior_tickets_30d en 6,3% de las condiciones escritas
  frente al 14,5% de casos que decide; language en 0,2% pese a existir H21.
- La compilación destruyó capacidad: SECURITY_INCIDENT, 3/3 aciertos cuando el
  caso llegó al LLM, 0/17 cuando lo resolvió una regla compilada.

### El fallo de diseño de fondo

Ningún criterio sintáctico recupera esta política. Demostración con las propias
reglas ocultas: H01 (2 condiciones) debe ganar a H03 (1); H16 (1) debe ganar a
H24 (2). Ninguna función monótona de la especificidad satisface ambas. Y el
arbitraje por orden de llegada tampoco: mismas 29 reglas, orden de diseño 100%,
orden inverso 12,8%, orden aleatorio 49,3% de media sobre 200 muestras. En una
base aprendida el orden de llegada va al revés del correcto, porque los primeros
casos vienen de la distribución común y engendran reglas de defecto, mientras
las excepciones nacen tarde.

CONCLUSIÓN: la compilación por impasse aprende reglas, pero no tiene ningún
mecanismo para aprender prioridad. En una política estratificada la estructura
vive en la prioridad. Es una limitación del diseño, no del modelo ni del motor.

### Errores de proceso, para el registro

- Yo (Sergi) di por buena la realizabilidad sin verificarla.
- Claude escribió en el README que la política era "enteramente expresable en el
  DSL" habiendo comprobado solo las condiciones, no la semántica de resolución.
  También predijo que la tormenta de conflictos de random_k "probablemente no
  mordería" con un LLM real. Fue el mecanismo dominante.
- ChatGPT advirtió exactamente de este riesgo (la verdad oculta debe ser
  expresable en el DSL, si no el fracaso es ininterpretable). Se aceptó la
  advertencia y no se implementó la comprobación.
- El defecto lo encontró una verificación que costó cero llamadas a la API y que
  debió correrse ANTES de la tirada: cargar la política verdadera en el motor y
  medir su techo.
