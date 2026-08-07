# Notas de registro

## 6 de agosto de 2026 — `results/subsumption.json` cambió de fecha durante el Paso 1 del peldaño 2

El Paso 1 del peldaño 2 exige comprobar que el peldaño 1 sigue reproduciendo.
Esa comprobación se hace corriendo los scripts originales:

    python3 -m harness.ceiling_check
    python3 -m harness.subsumption_check

`ceiling_check` no escribe nada. `subsumption_check` **sí**: termina volcando
`results/subsumption.json`. Al re-correrlo, el archivo se reescribió.

**No se perdió nada.** El cómputo es enteramente determinista —corpus fijo con
semilla 17, política oculta congelada, espacio exhaustivo de 134.400
combinaciones— y el contenido reescrito es idéntico al anterior. Verificado
campo a campo tras la reescritura:

    order.ordered_pairs                        61
    order.possible_pairs                      406
    order.incomparable_pairs                  345
    order.contradictions_with_layer_order       0
    arbitration.subsumption.action           1263
    arbitration.subsumption.conflict          737
    arbitration.subsumption.correct          1263
    arbitration.subsumption.e2e            0.6315
    arbitration.subsumption.silent_error      0.0
    concentration_curve k=10                0.8415
    concentration_curve k=20                0.8870
    concentration_curve k=50                0.9495

Lo único que cambió es el `mtime`: de 6 ago 14:20 a 6 ago 16:23.

## Por qué queda constancia

El peldaño 1 es registro cerrado y sus cifras deben seguir reproduciendo. Una
fecha de modificación posterior al cierre, sin explicación, es indistinguible de
una manipulación. Queda anotado aquí que el cambio lo produjo la verificación y
no una reejecución con parámetros distintos.

Todo lo que produce el peldaño 2 va a `results2/` y no toca `results/`.

## Cómo re-verificar sin volver a escribir

    python3 -m harness.subsumption_check | head -20

La salida por pantalla contiene las mismas cifras; el volcado a disco es un
efecto secundario del script del peldaño 1 que no se corrige aquí, porque
`harness/` es registro cerrado y modificarlo tendría el mismo problema que se
quiere evitar.

---

## 7 de agosto de 2026 — seis registros re-corridos para que ganen su `_env`

Ese día se añadió `harness/provenance.py`, que cuelga un bloque `_env` de cada
JSON con el intérprete, la plataforma, `PYTHONHASHSEED`, el commit y un digest
del código. Ningún registro publicado lo llevaba: el campo aparece cuando la
cifra se vuelve a correr, y no se había re-corrido nada.

Se re-corrieron **los seis que son deterministas y cuestan cero llamadas a la
API**, que son exactamente aquellos en los que reproducir no puede cambiar nada:

    python3 run_experiment.py frontier                          # results/frontier.json
    python3 -m harness.subsumption_check                        # results/subsumption.json
    python3 -m harness.learned_subsumption                      # results/learned_subsumption.json
    python3 -m peldano2.ceiling_check2                          # results2/ceiling2.json
    python3 -m peldano2.compare_runs results2/llm_run2_*.json   # results2/comparativa.json
    python3 -m peldano2.note_audit  results2/llm_run2_*.json    # results2/note_audit.json

**No cambió ni un dato.** Verificado por comparación estructural contra la
versión en git, no a ojo: para los cuatro primeros, el objeto entero menos la
clave `_env` es igual al publicado; para los dos últimos, las filas bajo `rows`
son iguales a la lista publicada, las 8, en el mismo orden.

Los dos últimos sí **cambiaron de forma**, que era lo previsto y la razón de que
se re-corrieran: sus escritores pasaron de volcar una lista pelada a volcar
`{"_env": …, "rows": […]}`, que es la única manera de colgarles procedencia. Se
invocaron con el glob de las ocho tiradas; llamarlos con un archivo suelto
habría reducido el registro de 8 a 1, que es pérdida de datos y no un cambio de
dígitos.

### Lo que NO se re-corrió, y por qué

- `results/llm_run.json`, `results/llm_run_n100_smoke.json` y las ocho
  `results2/llm_run2_*.json`: reproducirlas cuesta dinero y **no saldrían
  iguales** —el proponente no es determinista a `temperature 0`—. Además
  `llm_run.json` es la base de 577 reglas de la que parten los peldaños 3 y 4
  (regla dura 4).
- `results3/order_search.json`, `results3/budget_and_balance.json` y
  `results4/sweep.json`: son gratis y deterministas, pero re-correrlas **sí
  mueve los dígitos**, porque el arreglo del desempate del 6 de agosto todavía
  no está incorporado a sus cifras publicadas. Está aplazado a propósito, para
  hacerse junto con el optimizador serio.

### El `git_dirty` de estos seis, y una trampa al re-correrlos en tanda

Los seis dicen `git_dirty: false` y `git_commit: 97cabc1`, con el mismo
`code_digest` `7ef0ec6d89ec4d85`. Es decir: ese commit identifica exactamente el
código que produjo las seis cifras.

Costó dos intentos, y el motivo merece quedar anotado porque le va a pasar a
cualquiera que repita esto. **Correr los seis seguidos no da `git_dirty: false`
más que en el primero**: cada script deja su JSON modificado, así que el árbol
que ve el segundo ya está sucio, y el tercero más. En la primera pasada sólo
`frontier.json` salió limpio y los otros cinco dijeron `true`.

El flag no mentía, pero medía lo que no importa: lo que ensuciaba el árbol eran
*registros*, no código. La forma correcta es correr cada script desde un árbol
limpio, apartar su JSON y restaurar el árbol antes del siguiente:

    for cada script:
        comprobar que `git status --porcelain` está vacío
        correr el script
        copiar su JSON a un temporal
        git checkout -- results results2
    al final, poner los seis en su sitio de una vez

Así cada bloque `_env` dice la verdad sobre el código que corrió, que es para lo
que existe el campo.

### Por qué el commit que citan no es el que los contiene

Un registro no puede llevar dentro el hash del commit que lo transporta. Los
seis se produjeron con el árbol limpio en `97cabc1` y se confirmaron en el
commit siguiente, que sólo toca estos seis JSON y esta nota: ni una línea de
`harness/`, `peldano2..4/` ni `run_experiment.py`. Por eso `code_digest` sigue
siendo el mismo en los dos commits, y `git_commit: 97cabc1` sigue identificando
el código con exactitud.
