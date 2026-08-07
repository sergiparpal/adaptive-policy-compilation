"""
Pruebas del arnes.

QUE CUBREN, Y POR QUE ESAS Y NO OTRAS

Este repositorio no es una biblioteca: es un experimento cuyo producto son
CIFRAS. Lo que hay que proteger no es una API, son los numeros que los
`FINDINGS` citan y que deben seguir reproduciendo. De ahi las dos familias:

  * INVARIANTES — propiedades que deben ser ciertas por construccion. La
    principal: las 29 reglas escritas en el DSL son equivalentes a los
    predicados de `hidden_policy` sobre las 134.400 combinaciones del espacio,
    y evaluarlas con primera-que-casa reproduce la politica exactamente. Es la
    afirmacion sobre la que descansa todo el peldano 1 ("fallo de ejecucion, no
    de representacion").

  * SNAPSHOTS — las cifras publicadas, clavadas al digito: techo por
    especificidad 0,5875, subsuncion sola 0,6315, hibrido 1,0000, la frontera
    de los mocks y las estadisticas del corpus. Si una de estas pruebas falla,
    la respuesta correcta NO es actualizar el numero esperado: es averiguar que
    cambio y, si el cambio es legitimo, fechar la errata en el `FINDINGS`
    correspondiente, que es como este proyecto registra las correcciones.

REGLA DE LA SUITE: ninguna prueba escribe en `results*/`. Los registros son el
producto del experimento y solo los reescribe quien corre el experimento a
proposito. Por eso las pruebas llaman a las funciones de medida y nunca a los
`main()` de los scripts, que si vuelcan su JSON.

Los peldanos 3 y 4 estan cubiertos por DETERMINISMO, no por snapshot: sus
cifras publicadas son las del codigo anterior al arreglo del desempate del 6 de
agosto de 2026 y estan pendientes de re-correr. Clavar aqui los valores nuevos
crearia una segunda cifra oficial que no respalda ningun FINDINGS.

    python3 -m unittest discover -v       # todo, cero llamadas a la API
"""
