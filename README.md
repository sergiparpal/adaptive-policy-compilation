# Compilación adaptativa de políticas — Peldaño 1

> **Este archivo documenta el PELDAÑO 1, que no es el estado actual del
> proyecto.** Hay cuatro peldaños cerrados:
>
> | peldaño | registro |
> |---|---|
> | 1 · techo del motor y tirada anulada | [`results/FINDINGS.md`](results/FINDINGS.md) |
> | 2 · prioridad declarada, motor híbrido | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |
> | 3 · prioridad por búsqueda sobre el corpus | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) |
> | 4 · prioridad aprendida de un canal de feedback | [`results4/FINDINGS4.md`](results4/FINDINGS4.md) |
>
> Los cuatro llevan erratas fechadas en el sitio; léelas antes de citar cifras.
> `IDEAS.md` lleva lo que queda abierto.

Mundo estático · política oculta realizable · **sombra pura** (ninguna regla se activa jamás).

Objetivo único de este peldaño: **medir la tasa de reutilización y el error silencioso** de las reglas que escribe un LLM. Nada más. Si la reutilización sale baja, la arquitectura no se sostiene y se para.

**Ese objetivo no se cumplió.** La tirada quedó anulada por techo del motor antes de que la reutilización fuera interpretable, y sigue sin medirse limpiamente. Lo que sí quedó establecido está en los cuatro registros de arriba.

---

## Especificación congelada

**Caso** — 8 atributos, muestreados con distribución de cola larga:

| atributo | dominio |
|---|---|
| `has_security_keyword` | bool (3% True) |
| `severity` | 1..4 (1=crítica, 5%) |
| `customer_tier` | free / pro / business / enterprise (50/30/15/5) |
| `product` | dashboard / billing / api / mobile / integrations |
| `channel` | portal / email / chat / phone (phone 5%) |
| `prior_tickets_30d` | 0..20, geométrica truncada |
| `off_hours` | bool (28%) |
| `language` | en / es / pt / de / fr |

**Acciones** — 8 colas: `T1_GENERAL`, `T2_TECHNICAL`, `T3_ENGINEERING`, `BILLING_SPECIALIST`, `SECURITY_INCIDENT`, `ACCOUNT_MANAGER`, `ONCALL_ESCALATION`, `SELF_SERVICE_DEFLECT`.

**Política oculta** — 29 reglas priorizadas en 8 capas (overrides de seguridad → SLO/guardia → facturación → riesgo de fuga → producto → idioma/dotación → deflexión → defectos). Primera coincidencia gana. Estructura jerárquica con excepciones reales, no reglas independientes.

**Expresable en el DSL, NO ejecutable por el motor.** La distinción se verificó el
5 de agosto de 2026 y es central para leer todo lo demás:

- **Representación: correcta.** Comprobado exhaustivamente sobre las **134.400
  combinaciones del espacio de casos** que las 29 reglas escritas en el DSL son
  equivalentes a sus predicados originales, y que evaluarlas con "primera que casa
  gana" reproduce `true_action` exactamente. El DSL no pierde nada.
- **Ejecución: rota.** Con esas mismas 29 reglas cargadas en `RuleEngine` y ningún
  LLM de por medio, el motor alcanza **58,75% de exactitud** y declara **CONFLICT
  en el 25,3%** de los casos. El arbitraje por especificidad no puede ejecutar una
  política priorizada por capas: en esta política, prioridad y número de
  condiciones son casi ortogonales.

La "condición del peldaño 1" (política oculta realizable) se cumple a nivel de
representación y se incumple a nivel de ejecución. Reproducible sin gastar nada
con `python3 -m harness.ceiling_check`.

**Esquema de regla** — el proponente nunca emite código:

```json
{"action": "T3_ENGINEERING",
 "conditions": [{"attr": "product", "op": "eq", "value": "api"},
                {"attr": "severity", "op": "lte", "value": 2}],
 "note": "..."}
```

Operadores: `eq`, `neq`, `lte`, `gte`, `in`. `lte`/`gte` solo sobre `severity` y `prior_tickets_30d`.

**Motor** — tres resultados: `ACTION`, `IMPASSE` (cobertura), `CONFLICT` (lógico). Conflictos por especificidad; empate con acciones distintas → escalación.

**Disparador de escalación** — *solo* impasse de cobertura o conflicto. **Nunca** "la respuesta era incorrecta". Esa restricción es lo que hace medible el error silencioso.

---

## Invariantes del experimento

1. **Separación del oráculo.** `hidden_policy.py` etiqueta el registro. Ni el motor ni el proponente lo consultan jamás.
2. **Sombra pura.** Ninguna regla se activa. Los tickets son independientes, así que la sombra es exacta, no una aproximación.
3. **El proponente no toca la base.** Emite payload; un validador determinista lo acepta o lo rechaza.
4. **Corpus fijo.** Semilla 17. No se regenera entre variantes.

---

## Uso

```bash
python3 -m harness.ceiling_check           # PASO 0: techo del motor, 0 llamadas
python run_experiment.py frontier          # barrido de mocks + baselines, 0 llamadas
export OPENROUTER_API_KEY=...
python run_experiment.py llm --n 2000      # proponente real
```

`pip install -r requirements.txt` (solo `openai`) para el último; los dos primeros
no necesitan nada ni gastan llamadas. El proveedor por defecto es **OpenRouter**;
con `--provider anthropic` harían falta el paquete `anthropic` y
`ANTHROPIC_API_KEY` en su lugar.

**El Paso 0 es obligatorio y bloqueante.** Carga la política oculta verdadera en el
motor y mide su exactitud sin ningún LLM. Si el motor no puede ejecutar la política
correcta, ninguna medición sobre reglas aprendidas significa nada. Mientras no dé
~100%, cualquier tirada con LLM queda anulada de antemano — es lo que pasó con la
tirada del 5 de agosto de 2026 (ver `PREDICTION.md`).


---

## Puesta en marcha (5 minutos)

Requiere **Python 3.10+**. Comprueba con `python3 --version`.

```bash
cd adaptive_triage

# 0. OBLIGATORIO, y antes que nada: techo del motor. 0 llamadas a la API.
#    Si no sale ~100%, PARA: nada de lo que venga despues sera interpretable.
python3 -m harness.ceiling_check

# 1. Comprobar que todo funciona SIN gastar nada
python3 run_experiment.py frontier

# 2. Instalar el SDK (OpenRouter es compatible con OpenAI)
pip install -r requirements.txt

# 3. Clave desde openrouter.ai -> Keys
export OPENROUTER_API_KEY=sk-or-...        # Windows: set OPENROUTER_API_KEY=...

# 4. (opcional) buscar el slug exacto de un modelo
python3 run_experiment.py models deepseek

# 5. Prueba corta primero: ver reglas reales y validar el parseo
python3 run_experiment.py llm --n 100

# 6. Rellenar PREDICTION.md, y solo entonces la tirada completa
python3 run_experiment.py llm --n 2000
```

**Proveedor por defecto: OpenRouter.** Modelo por defecto
`deepseek/deepseek-v4-flash`. Alternativas:

```bash
python3 run_experiment.py llm --model openai/gpt-5.6-luna
python3 run_experiment.py llm --model deepseek/deepseek-v4-flash-0731   # revision fijada
python3 run_experiment.py llm --provider anthropic --model claude-haiku-4-5-20251001
```

Que el proponente NO sea Claude es preferible: el arnes y la politica oculta
los escribio Claude, y conviene que el proponente venga de otra familia.

**Coste.** Solo las escalaciones cuestan una llamada. Con V4 Flash alrededor de
$0.09/$0.18 por millon de tokens y unos cientos de escalaciones a ~1.100 tokens
de entrada y ~200 de salida, la tirada completa cuesta centimos. Verificalo con
`--n 100`.

**Duracion.** El bucle es **estrictamente secuencial** y no se puede
paralelizar: cada regla nueva cambia si el caso siguiente escala o no. Cuenta
unos minutos para 2000 casos, no segundos.

**Robustez.** Los modelos baratos devuelven JSON sucio. El parser tolera vallas
markdown, preambulos y epilogos; los fallos irrecuperables se cuentan en
`failed_proposals` y los esquemas invalidos en `rejected_rules`, sin abortar la
tirada. Si esos dos numeros salen altos, el problema es el prompt, no la
arquitectura.

**Determinismo: no lo hay.** El corpus sí es determinista (semilla 17), pero el
proponente no, ni siquiera a `temperature 0`. Verificado el 5 de agosto de 2026:
mismo prompt, mismo caso, misma semilla, y las reglas nacidas de los primeros
casos difieren entre la tirada de n=100 y la de n=2000. Dos consecuencias:

- **la prueba corta no es un prefijo de la larga** — no extrapoles de una a otra;
- **una comparativa entre modelos no tiene al modelo como única variable** salvo
  que se promedien varias semillas de muestreo por modelo.

---

## Cómo leer la frontera

Los mocks `keep_k` no "generalizan": **parten el espacio de casos en una rejilla** fijando los k atributos más informativos con `eq`. Son por tanto una caché semántica parametrizada por granularidad — el baseline obligatorio, ya incorporado.

El LLM tiene una ventaja que los mocks no tienen: puede usar `lte`, `gte`, `in` y elegir umbrales.

**La frontera NO es una región a batir.** Lo fue en la especificación original; la
verificación del techo (Paso 0) la invalidó como referencia, y el umbral que había
aquí fijado queda retirado:

- **Los mocks son estructuralmente inmunes al defecto del motor.** Todas las reglas
  de `keep_k(k)` tienen exactamente k condiciones. Con especificidad uniforme el
  arbitraje no puede invertir prioridades nunca, y el desempate cae en `born_at`,
  que es la semántica correcta. La política oculta, en cambio, mezcla reglas de 1 a
  3 condiciones en las que la regla *menos* específica suele tener *más* prioridad
  — justo el caso que el arbitraje resuelve al revés.
- **`keep_k(k=4)` puntúa mejor que la política verdadera bajo este motor:** 0.173
  de error silencioso frente a 0.214, y 0.780 de exactitud extremo a extremo frente
  a 0.588. Una rejilla cruda supera al oráculo, y no por ser mejor política: por no
  sufrir las inversiones de prioridad que el arbitraje impone.

Es decir: la "región a batir" estaba **por encima del techo del propio sistema**.
Medir contra ella habría medido la inmunidad del mock al defecto, no la capacidad
de inducción del proponente. No se fija ningún umbral nuevo hasta que el Paso 0 dé
~100%.

Las cifras de `frontier` siguen siendo reproducibles y sirven para comprobar que
nada se corrompió al copiar. No sirven como referencia de calidad.

Referencia: clase mayoritaria 36.3%. Política oculta: 29 reglas.

---

## Antes de correr `llm`: rellena PREDICTION.md

No es ceremonia. Sin umbral escrito de antemano, cualquier resultado va a parecer prometedor.

---

## Qué NO hay aquí, deliberadamente

Deriva de concepto, regret respecto a la mejor política representable, ILP como competidor, detectores de impasse empírico, feedback parcial, ASP, activación, versionado, reversión. Todo eso está en `IDEAS.md` y no se toca hasta tener la primera curva del LLM.

---

## Estructura de archivos (importante)

Los modulos usan imports relativos, asi que **deben estar dentro de `harness/`**.
Si al descargarlos quedaron planos, veras
`ModuleNotFoundError: No module named 'harness'`. Estructura correcta:

```
adaptive_triage/
├── run_experiment.py
├── requirements.txt
├── README.md
├── PREDICTION.md
├── IDEAS.md
└── harness/
    ├── __init__.py
    ├── domain.py
    ├── dsl.py
    ├── hidden_policy.py
    ├── proposers.py
    ├── shadow.py
    └── cache_baseline.py
```

Arreglo rapido si quedaron planos:

```bash
mkdir -p harness
mv domain.py dsl.py hidden_policy.py proposers.py shadow.py cache_baseline.py harness/
touch harness/__init__.py
```
