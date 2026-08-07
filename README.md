# Compilación adaptativa de políticas

Un motor simbólico barato resuelve los casos que cubre; cuando no cubre uno
(*impasse*), un LLM actúa y escribe una regla nueva para que la próxima vez sí lo
cubra. Dominio: triaje de tickets de soporte — 8 atributos, 8 colas, y una
política oculta de 29 reglas repartidas en 8 capas de prioridad.

## Cuatro peldaños cerrados

| peldaño | qué midió | registro |
|---|---|---|
| **1** · techo del motor | el arbitraje por especificidad alcanza **58,75%** con la política perfecta cargada; la tirada con LLM quedó anulada por ese techo | [`results/FINDINGS.md`](results/FINDINGS.md) |
| **2** · prioridad declarada | el motor híbrido (subsunción + prioridad declarada) ejecuta la política estratificada al **100%**, pero el proponente escribe reglas disjuntas y nunca lo ejercita | [`results2/FINDINGS2.md`](results2/FINDINGS2.md) |
| **3** · prioridad por búsqueda | las 577 reglas del peldaño 1 admiten un orden que saca **0,77** en test; el arbitraje las convertía en 0,18 | [`results3/FINDINGS3.md`](results3/FINDINGS3.md) |
| **4** · prioridad por feedback | ese orden **no** se aprende del feedback asimétrico que produce un sistema real | [`results4/FINDINGS4.md`](results4/FINDINGS4.md) |

El hilo que los une: la prioridad de una política por capas no está en la forma
de las reglas, y las tres vías de suministrarla —inferirla de la sintaxis, que la
declare el proponente, aprenderla del comportamiento observado— están medidas y
fallan cada una por una razón distinta.

**La hipótesis original —¿las reglas que escribe un LLM se reutilizan, o memoriza
casos?— sigue sin medirse limpiamente.** [`IDEAS.md`](IDEAS.md) lleva la lista de
lo que queda abierto, incluida la deuda técnica conocida.

> **A partir de "Peldaño 1", este archivo describe la especificación y la
> operativa de ese peldaño.** Siguen siendo válidas como procedimiento, no como
> estado del proyecto.
>
> Antes de citar cualquier cifra, lee las **erratas fechadas** que cada FINDINGS
> lleva en el sitio. Las de los peldaños 3 y 4 están además condicionadas por un
> desempate no determinista en el optimizador, corregido el 6 de agosto de 2026
> y **sin re-correr**: los números publicados son los del código anterior.

---

## Reproducir los cuatro peldaños

**Todo esto cuesta cero llamadas a la API y corre con la biblioteca estándar**,
sin venv. Son las mediciones que sostienen los cuatro registros; al lado de cada
comando, lo que debe imprimir.

```bash
# --- PELDAÑO 1 · el techo del motor y la frontera ------------------------
python3 -m harness.ceiling_check      # especificidad 0.5875 · orden de diseño 1.0000
python3 run_experiment.py frontier    # keep_k(k=4): 113 reglas, err.sil 0.173

# --- PELDAÑO 2 · motor híbrido: subsunción + prioridad declarada ---------
python3 -m peldano2.ceiling_check2    # e2e 1.0000 · 0 conflictos · PARADA 0 -> PASA
python3 -m peldano2.compare_runs results2/llm_run2_*.json   # las 8 tiradas
python3 -m peldano2.note_audit  results2/llm_run2_*.json    # atributos y notas

# --- PELDAÑO 3 · orden por búsqueda sobre el corpus ----------------------
python3 -m peldano3.order_search      # cota 0.9010 · test ~0.77 · gap ~0
python3 -m peldano3.budget_and_balance  # curva de etiquetas y voraz balanceado

# --- PELDAÑO 4 · orden aprendido de un canal de feedback -----------------
python3 -m peldano4.sweep             # barridos de cobertura/asimetría/retardo/ruido
```

Y antes de tocar nada, la suite: **249 pruebas en ~12 s, sin API y sin escribir
en `results*/`.**

```bash
python3 -m unittest discover
```

La corren solas el hook de pre-commit y CI; para activar el hook en tu clon,
una vez:

```bash
git config core.hooksPath .githooks
```

> **Los peldaños 3 y 4 no reproducen sus cifras publicadas al dígito.** El
> desempate del optimizador era no determinista (dependía de `PYTHONHASHSEED`) y
> se corrigió el 6 de agosto de 2026 sin volver a correr nada. Ejemplo real:
> `order_search` imprime hoy `test 0.7713 · GAP 0.0062` donde el registro dice
> `0.7711 · 0.0068`. Las direcciones y las magnitudes se mantienen; los dígitos
> se moverán hasta que se rehagan ambos peldaños, lo que está previsto hacer
> junto con un optimizador serio. Las cotas y los techos —0.9010, 0.5875,
> 1.0000— **no** dependen del voraz y sí reproducen exactamente.

**Lo único que gasta dinero** es el proponente real, que necesita el venv y la
clave (ver *Puesta en marcha*):

```bash
.venv/bin/python run_experiment.py llm --n 100                      # peldaño 1
.venv/bin/python -m peldano2.run2 --n 100 --seed 17 --prompt-version v2   # peldaño 2
```

`peldano2/run2.py` acepta `--prompt-version v1|v2`; ambas versiones del prompt se
conservan en el código y cada tirada guarda íntegro el que usó. El registro del
cambio está en [`results2/CAMBIOS.md`](results2/CAMBIOS.md).

> ⚠️ **Reproducir una cifra sobrescribe su propio registro.** Casi todos los
> scripts de arriba vuelcan su JSON al terminar, sobre el archivo publicado:
>
> | script | archivo que reescribe |
> |---|---|
> | `run_experiment.py frontier` | `results/frontier.json` |
> | `run_experiment.py llm` | **`results/llm_run.json`** ← ver aviso abajo |
> | `harness/subsumption_check.py` | `results/subsumption.json` |
> | `harness/learned_subsumption.py` | `results/learned_subsumption.json` |
> | `peldano2/ceiling_check2.py` | `results2/ceiling2.json` |
> | `peldano2/compare_runs.py` | `results2/comparativa.json` |
> | `peldano2/note_audit.py` | `results2/note_audit.json` |
> | `peldano2/run2.py` | `results2/llm_run2_<tag>.json` |
> | `peldano3/order_search.py` | `results3/order_search.json` |
> | `peldano3/budget_and_balance.py` | `results3/budget_and_balance.json` |
> | `peldano4/sweep.py` | `results4/sweep.json` |
>
> De todo lo que se ejecuta en este README, solo `harness/ceiling_check.py` y
> `run_experiment.py models` no escriben nada.
>
> **El caso grave es `run_experiment.py llm`.** Sobrescribe
> `results/llm_run.json`, que no es solo el registro del peldaño 1: es la base de
> 577 reglas de la que **parten los peldaños 3 y 4**. Re-correrlo destruye la
> entrada de dos peldaños cerrados, y como el proponente no es determinista a
> `temperature 0`, lo que salga no será lo mismo. Si necesitas re-correrlo,
> guarda el original antes con otro nombre.
>
> En los peldaños 1 y 2 el resto del cómputo es determinista y el contenido sale
> idéntico —cambia la fecha de modificación de un registro cerrado, ver
> [`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md)—. En los peldaños 3 y
> 4 **el contenido sí cambia**, porque el arreglo del desempate mueve los
> dígitos.
>
> Y hay una trampa peor: `compare_runs` y `note_audit` reescriben con **lo que
> se les pasa como argumento**. Invocarlos con un archivo en vez de con
> `results2/llm_run2_*.json` reduce el registro de 8 tiradas a 1. No es un
> cambio de dígitos, es pérdida de datos.
>
> Desde el 7 de agosto de 2026 hay un detalle más: cada JSON lleva un bloque
> `_env` con la procedencia (ver *Las pruebas y la procedencia*). Al re-correr
> una cifra que no ha cambiado, `git diff` muestra **solo** el campo
> `recorded_at` moviéndose — que es justamente la comprobación de que sigue
> reproduciendo. Los seis registros deterministas y gratuitos de la tabla ya lo
> llevan: se re-corrieron ese mismo día para ganarlo, con el contenido idéntico
> campo a campo ([`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md)). En
> esa pasada `comparativa.json` y `note_audit.json` adoptaron además su forma
> nueva, `{"_env": …, "rows": […]}` en vez de la lista pelada, con las mismas 8
> filas.
>
> **La salvaguarda es git, y basta.** Después de reproducir cualquier cosa:
> `git status` delata lo que se ha tocado y `git checkout -- <archivo>` lo
> restaura. Los registros se versionan precisamente para esto.

---

## Las pruebas y la procedencia

Dos redes distintas, con propósitos distintos.

### La suite

```bash
python3 -m unittest discover            # 249 pruebas, ~12 s, 0 llamadas a la API
python3 -m unittest tests.test_ceilings -v      # un módulo suelto
```

No necesita venv y **no escribe en `results*/`**: llama a las funciones de
medida, nunca a los `main()` de los scripts, que sí vuelcan su JSON.

Lo que cubre, y por qué esas cosas:

| módulo | qué protege |
|---|---|
| `test_encoding_invariant.py` | las 29 reglas del DSL ≡ sus lambdas, y primera-que-casa ≡ `true_action`, sobre las **134.400** combinaciones. Es la afirmación en que se apoya "fallo de ejecución, no de representación" |
| `test_ceilings.py` | los cuatro techos al dígito: 0,5875 · 0,6315 · 1,0000 · 1,0000, con sus 505 y 737 conflictos y las 199 aristas |
| `test_frontier.py` | la verificación en seco del Paso 1 y el suelo de memorización (0,1176) |
| `test_domain.py` | el corpus: 1743 únicos, 12,85% duplicados, y las 8 clases con sus recuentos |
| `test_dsl.py` | el DSL congelado, incluido el **defecto registrado** (CONFLICT se devuelve antes del desempate por antigüedad), clavado a propósito |
| `test_shadow.py` | la semántica de las métricas, y que el único disparador de escalación sea el impasse — nunca "la respuesta era incorrecta" |
| `test_engine2.py` | máscaras de bits ≡ `Condition.holds`, y los seis veredictos del validador de aristas |
| `test_oracle_separation.py` | que ningún componente del bucle online importe el oráculo, y que `feedback.py` siga siendo el único módulo del peldaño 4 que lo toca |
| `test_order_determinism.py` | que el voraz de los peldaños 3 y 4 dé el mismo orden bajo tres `PYTHONHASHSEED`, con un testigo que confirma que el hash sí se aleatoriza |
| `test_proposal_parsing.py` | el parseo de lo que devuelve el proponente, en sus dos versiones |
| `test_llm_path.py` | la ruta del LLM **entera**, replicando las tiradas registradas sin gastar (ver abajo) |
| `test_provenance.py` | el bloque `_env`, que no filtra la clave, y que ningún escritor de JSON se quede sin él |
| `test_automatizacion.py` | que el hook y el flujo de CI sigan ahí y sigan corriendo lo que dicen |

Si una prueba de *snapshot* falla, el número esperado **no se actualiza**: se
averigua qué cambió y, si el cambio es legítimo, se fecha la errata en el
`FINDINGS` correspondiente. Los peldaños 3 y 4 están cubiertos por determinismo
y no por snapshot, a propósito: sus cifras publicadas son las del código
anterior al arreglo del desempate y están pendientes de re-correr.

### La ruta del LLM, sin gastar

De la ruta que cuesta dinero solo estaba probado el parseo. El resto —armar la
petición, leer la respuesta del SDK, reintentar, validar, meter la regla en la
base, calcular las métricas— ahora se prueba con un **doble que sustituye al
cliente del SDK, no al proponente**: `OpenRouterProposer` y `OpenRouterProposer2`
corren enteros y lo único que no ocurre es la petición HTTP.

Las respuestas no salen de un guion aparte, sino **del propio registro
publicado**, de modo que el replay es la tirada que produjo las cifras:

| registro | qué reproduce, exactamente |
|---|---|
| `results/llm_run.json` | 2000 casos, 632 escalaciones → las 577 reglas, las métricas y los 2000 registros crudos |
| `results2/llm_run2_n100.json` | 100 casos, 42 escalaciones → lo mismo, más las 7 aristas de prioridad con su veredicto |

De ahí sale además una cifra que no está en ningún registro: **632 escalaciones
costaron 700 llamadas**, porque los 34 fallos de parseo se reintentan hasta tres
veces. El texto crudo de las respuestas nunca se guardó; qué parte se
reconstruye verbatim y qué parte es sólo el modo de fallo está enumerado turno a
turno en la cabecera de [`tests/doubles.py`](tests/doubles.py).

### Quién corre la suite

Nadie tiene que acordarse:

```bash
git config core.hooksPath .githooks     # una vez por clon
```

[`.githooks/pre-commit`](.githooks/pre-commit) corre la suite antes de cada
commit —~12 s, sin venv, sin API— y la aborta si falla. Se salta con
`git commit --no-verify`, que tiene sentido en un commit de sólo documentación y
en pocos casos más: si un snapshot falla, el número esperado no se actualiza y
el commit tampoco se fuerza.

[`.github/workflows/pruebas.yml`](.github/workflows/pruebas.yml) hace lo mismo en
cada push y cada PR —incluido lo que se empujó con `--no-verify`— sobre **3.10 y
3.12**: el mínimo que declara este README y el intérprete que produjo los
registros. Y añade un paso que la suite no puede hacer sola: comprobar, después
de correrla, que `results*/` sigue intacto.

Las acciones van clavadas al **SHA completo** con su versión en un comentario al
lado, nunca a una etiqueta: una etiqueta la puede repuntar su dueño hacia otro
código, un commit no. Es la convención del resto de repositorios de esta cuenta.
Para subir una, se resuelve la etiqueta nueva a su commit —
`gh api repos/actions/checkout/commits/vX.Y.Z --jq .sha` — y se cambian SHA y
comentario a la vez; hay una prueba que comprueba que van juntos.

Cada trabajo lleva `timeout-minutes: 10` sobre una suite de ~45 s: no es una
meta de velocidad, es lo que convierte un trabajo colgado en un fallo en vez de
en seis horas de runner. Y las ejecuciones superadas se cancelan… **salvo en
`main`**. Aquí los commits van directos a `main` y el estado del flujo es el
único registro de que ese commit pasó la suite; con `cancel-in-progress: true`
a secas, empujar tres commits seguidos deja los dos primeros en *cancelled*
para siempre — no fallaron, es que nunca llegaron a responder.

Y como un SHA clavado **no envejece ruidosamente** —se queda quieto y en
silencio—, [`.github/dependabot.yml`](.github/dependabot.yml) propone la subida
cada semana. Vigila las acciones y **no** `pip`, a propósito: `openai==2.53.0` y
el cierre transitivo del lock no son una dependencia desactualizada, son la
procedencia del entorno que produjo los registros, y un PR semanal proponiendo
subirlos entrenaría a fusionarlo sin mirar.

### El bloque `_env`

Cada JSON de resultados abre con la procedencia de la cifra:

```json
"_env": {
  "recorded_at": "2026-08-07T14:38:14Z",
  "python": "3.12.3",
  "openai": null,
  "platform": "Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39",
  "pythonhashseed": null,
  "git_commit": "97cabc1f…",
  "git_dirty": false,
  "code_dirty": false,
  "code_digest": "7ef0ec6d89ec4d85",
  "seed": 17
}
```

`pythonhashseed: null` significa **sin fijar**, es decir aleatorio: es
información, no ausencia de ella — cualquier cifra sensible al orden de
iteración de un `set` producida así es sospechosa por construcción, que es
exactamente lo que le pasó al voraz de los peldaños 3 y 4. `code_digest` es un
sha256 del código que produce cifras (`harness/`, `peldano2..4/`,
`run_experiment.py`; las pruebas quedan fuera), así que identifica la versión
aunque el árbol esté sucio o no haya git.

**Hay dos banderas de suciedad y no son redundantes.** `code_dirty` es la que
decide si `git_commit` identifica lo que corrió: con `false`, ese commit **es**
el código. `git_dirty` cubre todo lo demás del árbol, y lo demás no siempre es
inocuo — `learned_subsumption`, `compare_runs` y `note_audit` leen registros de
`results*/` **como entrada**, así que un JSON modificado y sin confirmar también
rompe la trazabilidad sin tocar una línea de código. Por eso el flag ancho no se
acotó: se desdobló (7 de agosto de 2026, al re-correr seis registros seguidos y
descubrir que cada script ensuciaba el árbol para el siguiente con su propia
salida; ver [`results2/NOTA_REGISTRO.md`](results2/NOTA_REGISTRO.md)).

El campo aparece en cada archivo cuando esa cifra se vuelve a correr, así que
llevarlo o no separa hoy los registros en dos:

| lo llevan | siguen sin llevarlo, y por qué |
|---|---|
| `frontier.json`, `subsumption.json`, `learned_subsumption.json`, `ceiling2.json`, `comparativa.json`, `note_audit.json` — re-corridos el 7 de agosto de 2026, contenido idéntico | `llm_run.json`, `llm_run_n100_smoke.json` y las 8 tiradas `llm_run2_*.json`: reproducirlas **cuesta dinero** y no salen iguales (el proponente no es determinista a `temperature 0`) |
| | `order_search.json`, `budget_and_balance.json`, `sweep.json`: son gratis y deterministas, pero re-correrlas **sí mueve dígitos** (arreglo del desempate) y está aplazado a hacerse junto con el optimizador serio |

Dicho de otro modo: lo que falta por llevar `_env` es exactamente lo que no se
puede reproducir gratis o lo que no se debe reproducir todavía.

---

## Peldaño 1

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

## El Paso 0 es obligatorio y bloqueante

```bash
python3 -m harness.ceiling_check
```

Carga la política oculta verdadera en el motor y mide su exactitud sin ningún
LLM. Si el motor no puede ejecutar la política correcta, ninguna medición sobre
reglas aprendidas significa nada. Mientras no dé ~100%, cualquier tirada con LLM
queda anulada de antemano — es lo que pasó con la tirada del 5 de agosto de 2026
(ver [`PREDICTION.md`](PREDICTION.md)).

Cuesta cero llamadas a la API y se vuelve a correr después de **cualquier**
cambio en el DSL, en el arbitraje o en la política oculta.

---

## Puesta en marcha (5 minutos)

Requiere **Python 3.10+**. Comprueba con `python3 --version`.

Todo lo que no llama al LLM —los techos, `frontier` y los peldaños 2, 3 y 4—
funciona **solo con la biblioteca estándar**. El venv hace falta únicamente para
el proponente real.

```bash
git clone https://github.com/sergiparpal/adaptive-triage.git
cd adaptive-triage

# 0. OBLIGATORIO, y antes que nada: techo del motor. 0 llamadas a la API.
#    Si no sale ~100%, PARA: nada de lo que venga despues sera interpretable.
python3 -m harness.ceiling_check

# 1. Comprobar que todo funciona SIN gastar nada
python3 -m unittest discover
python3 run_experiment.py frontier

# 1b. Que la suite se corra sola antes de cada commit. Una vez por clon.
git config core.hooksPath .githooks

# 2. Entorno virtual e instalacion del SDK.
#    OJO: en Debian/Ubuntu `pip install` global falla con
#    "externally-managed-environment" (PEP 668). El venv lo evita, y ademas
#    esta en .gitignore, asi que no ensucia el repo.
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. Clave desde openrouter.ai -> Keys. Va en el entorno, NUNCA en un archivo
#    del repo. Si la exportas en otra terminal, el proceso no la heredara.
export OPENROUTER_API_KEY=sk-or-...        # Windows: set OPENROUTER_API_KEY=...

# 4. (opcional) buscar el slug exacto de un modelo
.venv/bin/python run_experiment.py models deepseek

# 5. Prueba corta primero: ver reglas reales y validar el parseo
.venv/bin/python run_experiment.py llm --n 100

# 6. Rellenar PREDICTION.md, y solo entonces la tirada completa
.venv/bin/python run_experiment.py llm --n 2000
```

**Entorno con el que se produjeron los resultados publicados:** Python 3.12.3,
`openai` 2.53.0, Linux x86_64. `requirements.txt` clava esa versión exacta y
`requirements.lock.txt` guarda el cierre transitivo completo; para reconstruir
el entorno al dígito, instala el lock en vez de `requirements.txt`. Desde el 7
de agosto de 2026 cada JSON de resultados anota además el entorno con el que se
produjo, en su bloque `_env`.

**Proveedor por defecto: OpenRouter.** Modelo por defecto
`deepseek/deepseek-v4-flash`. Alternativas (todas necesitan el venv, porque
llaman al LLM):

```bash
.venv/bin/python run_experiment.py llm --model openai/gpt-5.6-luna
.venv/bin/python run_experiment.py llm --model deepseek/deepseek-v4-flash-0731   # revision fijada
.venv/bin/python run_experiment.py llm --provider anthropic --model claude-haiku-4-5-20251001
```

Con `--provider anthropic` harían falta además el paquete `anthropic` —que
`requirements.txt` deja comentado— y `ANTHROPIC_API_KEY` en lugar de la de
OpenRouter.

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

## Qué NO había aquí en el peldaño 1, deliberadamente

Deriva de concepto, regret respecto a la mejor política representable, ILP como
competidor, detectores de impasse empírico, feedback parcial, ASP, activación,
versionado, reversión.

De esa lista, **el feedback parcial ocurrió**: el peldaño 4 lo implementó como un
canal parametrizado por cobertura, asimetría, retardo y ruido. El resto sigue sin
hacerse, incluido el **ILP como competidor**, que llegó a especificarse como Paso
B del peldaño 3 y no se corrió.

(El peldaño 2 añadió la **prioridad declarada**, que no estaba en esta lista
porque en el peldaño 1 no se había identificado todavía como la pieza que
faltaba.)

Todo lo abierto está en [`IDEAS.md`](IDEAS.md), junto con lo que los cuatro
peldaños abrieron y no resolvieron.

---

## Estructura del repositorio

Los módulos usan imports relativos, así que **cada paquete debe conservar su
carpeta**. Si los archivos quedan planos verás
`ModuleNotFoundError: No module named 'harness'`.

```
adaptive-triage/
├── run_experiment.py        CLI del peldaño 1 (frontier · llm · models)
├── requirements.txt         `openai` clavado, para el proponente real
├── requirements.lock.txt    cierre transitivo del entorno de los registros
├── README.md  CLAUDE.md  IDEAS.md  PREDICTION.md  LICENSE  .gitignore
│
├── harness/                 PELDAÑO 1 — espec. congelada y motor original
│   ├── domain.py            caso, acciones, corpus (semilla 17)   [CONGELADO]
│   ├── hidden_policy.py     las 29 reglas en 8 capas · el ORÁCULO [CONGELADO]
│   ├── dsl.py               esquema de regla y RuleEngine          [CONGELADO]
│   ├── shadow.py            bucle en sombra y métricas             [CONGELADO]
│   ├── cache_baseline.py    baseline de caché semántica            [CONGELADO]
│   ├── proposers.py         mocks keep_k/random_k y proponentes LLM
│   ├── provenance.py        el bloque `_env` que acompaña a cada JSON
│   ├── ceiling_check.py     PASO 0 · techo del motor por especificidad
│   ├── subsumption_check.py orden parcial por subsunción semántica
│   └── learned_subsumption.py  el mismo criterio sobre la base aprendida
│
├── peldano2/                motor híbrido: subsunción + prioridad declarada
│   ├── engine2.py           arbitraje en dos niveles
│   ├── hidden_priority.py   las 29 reglas con sus aristas mínimas
│   ├── ceiling_check2.py    PASO 0 del peldaño 2 (da 100%)
│   ├── proposers2.py        prompts v1/v2 y vecindario acotado
│   └── shadow2.py  run2.py  compare_runs.py  note_audit.py
│
├── peldano3/                orden por búsqueda sobre el corpus, sin LLM
│   ├── order_search.py      cota de cobertura, voraz, partición
│   └── budget_and_balance.py  presupuesto de etiquetas y voraz balanceado
│
├── peldano4/                prioridad aprendida de un canal de feedback
│   ├── feedback.py          el canal; único que consulta el oráculo
│   └── sweep.py             barridos de cobertura, asimetría, retardo, ruido
│
├── tests/                   249 pruebas · `python3 -m unittest discover`
│   ├── fixtures.py          corpus y espacio exhaustivo, construidos una vez
│   ├── doubles.py           el cliente de SDK grabado: la ruta del LLM sin pagar
│   ├── hashseed_child.py    proceso hijo del control de `PYTHONHASHSEED`
│   └── test_*.py            invariantes y snapshots (ver *Las pruebas*)
│
├── .githooks/pre-commit     la suite antes de cada commit (hay que activarlo)
├── .github/workflows/       la suite en cada push y cada PR, en 3.10 y 3.12
├── .github/dependabot.yml   sube las acciones; NO toca los pines de pip
│
└── results/  results2/  results3/  results4/
    Los registros. FINDINGS*.md son las conclusiones con sus erratas
    fechadas; los .json son los datos crudos, para hacer cortes post-hoc
    sin volver a pagar ninguna tirada. Se versionan a propósito: son el
    producto del experimento, no salidas transitorias.
```

**`.venv/` está en `.gitignore`** y se reconstruye entero desde
`requirements.txt`. No lo versiones: el primer commit lo hizo y hubo que purgar
el historial.

Los cinco archivos marcados `[CONGELADO]` definen el experimento. Si crees que
alguno tiene un bug, **párate y dilo**; no lo arregles por tu cuenta. Ver las
reglas duras en [`CLAUDE.md`](CLAUDE.md).
