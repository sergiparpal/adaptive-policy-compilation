# Nota de registro — 6 de agosto de 2026

## `results/subsumption.json` cambió de fecha durante el Paso 1 del peldaño 2

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
