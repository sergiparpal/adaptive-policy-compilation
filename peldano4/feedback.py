"""
El canal de feedback, como artefacto separado.

RIESGO QUE ESTE MODULO EXISTE PARA CONTENER
-------------------------------------------
En un entorno sintetico "feedback del entorno" y "politica oculta" son la misma
funcion. Si el canal no esta acotado, medir "aprender del feedback" es medir
supervision completa con otro nombre.

Contencion: este modulo es el UNICO del peldano 4 que importa `true_action`. Su
salida es un diccionario {indice de caso -> accion reportada} estrictamente mas
pobre que la verdad, y el aprendiz no ve nada mas. La verdad vuelve a aparecer
solo en la EVALUACION, que es medicion y no supervision, igual que en los tres
peldanos anteriores.

QUE OBSERVA EL CANAL
--------------------
No etiquetas sueltas: RESULTADOS DE DECISIONES. Hace falta, por tanto, una
politica de referencia pi0 que este decidiendo mientras se observa. Sin eso, la
pregunta "que fraccion de decisiones recibe resultado" no significa nada.

En un sistema real de triaje el ciclo es: el ticket se enruta, alguien lo
recibe, y si la cola no era la suya lo reasigna. La reasignacion es el feedback,
y trae consigo la accion correcta.

PARAMETROS, Y A QUE CORRESPONDEN
--------------------------------
`coverage` c
    p(hay feedback | la decision fue INCORRECTA). En un sistema real la mayoria
    de tickets mal enrutados se reasignan, pero no todos: algunos se resuelven
    igual en la cola equivocada, otros se cierran, otros nadie los toca.

`asymmetry` a
    p(hay feedback | la decision fue CORRECTA) = c * a.
    ESTE ES EL PARAMETRO QUE IMPIDE QUE EL CANAL SEA EL ORACULO. Un sistema real
    entera de sus ERRORES, no de sus aciertos: nadie manda un mensaje diciendo
    "este ticket estaba bien enrutado". Con a = 1 el canal es un muestreo
    insesgado de etiquetas, que es lo que midio el peldano 3 y NO es realista.
    Con a = 0 solo se observan errores, y el conjunto etiquetado queda
    condicionado a que pi0 se equivocara: no es i.i.d., y esa dependencia es
    exactamente la que tendria un sistema desplegado.

`delay` d
    El resultado del caso i solo es utilizable si i + d cae dentro de la ventana
    de observacion. Corresponde a que la reasignacion ocurre horas o dias
    despues, cuando ya han entrado muchos tickets mas. Offline se traduce en que
    los ultimos d casos de la ventana no han producido feedback todavia.

`noise` e
    Con probabilidad e la accion reportada no es la verdadera sino otra al azar.
    Corresponde a que quien reasigna tambien se equivoca, o reasigna segun una
    convencion local que no es la politica.

QUE NO SE MODELA, Y POR QUE
---------------------------
No se interpreta la AUSENCIA de feedback como "fue correcto". Seria tentador
—duplicaria la senal— pero con cobertura parcial la ausencia es ambigua: puede
significar acierto o puede significar que nadie miro. Asumir lo primero
inyectaria informacion que el entorno no da. Queda anotado como decision, no
como omision.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict

from harness.domain import ACTIONS
from harness.hidden_policy import true_action    # UNICO import del oraculo


@dataclass(frozen=True)
class Channel:
    coverage: float = 1.0      # p(feedback | decision incorrecta)
    asymmetry: float = 1.0     # p(feedback | correcta) = coverage * asymmetry
    delay: int = 0             # casos de retardo
    noise: float = 0.0         # prob. de que la accion reportada sea otra
    seed: int = 17

    def label(self) -> str:
        return (f"c={self.coverage:g} a={self.asymmetry:g} "
                f"d={self.delay} e={self.noise:g}")

    def as_dict(self) -> dict:
        return asdict(self)

    def observe(self, corpus, window, decisions, window_end=None) -> dict[int, str]:
        """
        window       indices de casos observables (la ventana de aprendizaje)
        decisions    {indice -> accion que tomo pi0}
        window_end   ultimo indice del que ya ha podido llegar feedback;
                     por defecto, el maximo de la ventana

        Devuelve {indice -> accion reportada}. Nada mas. El aprendiz no recibe
        ni la verdad ni si la decision fue correcta: solo la accion reportada,
        que puede estar equivocada con probabilidad `noise`.
        """
        if window_end is None:
            window_end = max(window) if window else 0
        rng = random.Random(self.seed)
        out: dict[int, str] = {}
        for i in window:
            if i + self.delay > window_end:
                continue                                  # aun no ha llegado
            truth = true_action(corpus[i])
            was_wrong = decisions.get(i) != truth
            p = self.coverage if was_wrong else self.coverage * self.asymmetry
            if rng.random() >= p:
                continue                                  # nadie reporto nada
            if rng.random() < self.noise:
                alt = [a for a in ACTIONS if a != truth]
                out[i] = rng.choice(alt)
            else:
                out[i] = truth
        return out
