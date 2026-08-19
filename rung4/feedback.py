"""
The feedback channel, as a separate artefact.

THE RISK THIS MODULE EXISTS TO CONTAIN
--------------------------------------
In a synthetic environment "environment feedback" and "hidden policy" are the
same function. If the channel is not bounded, measuring "learning from feedback"
is measuring full supervision under another name.

Containment: this module is the ONLY one in rung 4 that imports `true_action`.
Its output is a dictionary {case index -> reported action}, strictly poorer than
the truth, and the learner sees nothing else. The truth reappears only in the
EVALUATION, which is measurement and not supervision, just as in the three
previous rungs.

WHAT THE CHANNEL OBSERVES
-------------------------
Not loose labels: OUTCOMES OF DECISIONS. It therefore requires a reference
policy pi0 to be deciding while the observation happens. Without that, the
question "what fraction of decisions receives an outcome" means nothing.

In a real triage system the cycle is: the ticket is routed, someone receives it,
and if the queue was not theirs they reassign it. The reassignment is the
feedback, and it brings the correct action with it.

PARAMETERS, AND WHAT THEY CORRESPOND TO
---------------------------------------
`coverage` c
    p(feedback exists | the decision was INCORRECT). In a real system most
    misrouted tickets get reassigned, but not all: some are resolved anyway in
    the wrong queue, others are closed, others nobody touches.

`asymmetry` a
    p(feedback exists | the decision was CORRECT) = c * a.
    THIS IS THE PARAMETER THAT KEEPS THE CHANNEL FROM BEING THE ORACLE. A real
    system learns about its ERRORS, not about its correct decisions: nobody
    sends a message saying "this ticket was routed correctly". With a = 1 the
    channel is an unbiased sample of labels, which is what rung 3 measured and
    is NOT realistic. With a = 0 only errors are observed, and the labelled set
    is conditioned on pi0 having been wrong: it is not i.i.d., and that
    dependency is exactly the one a deployed system would have.

`delay` d
    The outcome of case i is only usable if i + d falls within the observation
    window. It corresponds to the reassignment happening hours or days later,
    when many more tickets have already come in. Offline this translates into
    the last d cases of the window not having produced feedback yet.

`noise` e
    With probability e the reported action is not the true one but another at
    random. It corresponds to whoever reassigns also making mistakes, or
    reassigning by a local convention that is not the policy.

WHAT IS NOT MODELLED, AND WHY
-----------------------------
The ABSENCE of feedback is not interpreted as "it was correct". It would be
tempting —it would double the signal— but with partial coverage the absence is
ambiguous: it may mean a correct decision or it may mean nobody looked. Assuming
the former would inject information the environment does not give. Recorded as a
decision, not as an omission.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict

from harness.domain import ACTIONS
from harness.hidden_policy import true_action    # THE ONLY oracle import


@dataclass(frozen=True)
class Channel:
    coverage: float = 1.0      # p(feedback | incorrect decision)
    asymmetry: float = 1.0     # p(feedback | correct) = coverage * asymmetry
    delay: int = 0             # cases of delay
    noise: float = 0.0         # prob. that the reported action is another one
    seed: int = 17

    def label(self) -> str:
        return (f"c={self.coverage:g} a={self.asymmetry:g} "
                f"d={self.delay} e={self.noise:g}")

    def as_dict(self) -> dict:
        return asdict(self)

    def observe(self, corpus, window, decisions, window_end=None) -> dict[int, str]:
        """
        window       indices of observable cases (the learning window)
        decisions    {index -> action pi0 took}
        window_end   last index whose feedback could already have arrived;
                     by default, the maximum of the window

        Returns {index -> reported action}. Nothing else. The learner receives
        neither the truth nor whether the decision was correct: only the
        reported action, which may be wrong with probability `noise`.
        """
        if window_end is None:
            window_end = max(window) if window else 0
        rng = random.Random(self.seed)
        out: dict[int, str] = {}
        for i in window:
            if i + self.delay > window_end:
                continue                                  # has not arrived yet
            truth = true_action(corpus[i])
            was_wrong = decisions.get(i) != truth
            p = self.coverage if was_wrong else self.coverage * self.asymmetry
            if rng.random() >= p:
                continue                                  # nobody reported it
            if rng.random() < self.noise:
                alt = [a for a in ACTIONS if a != truth]
                out[i] = rng.choice(alt)
            else:
                out[i] = truth
        return out
