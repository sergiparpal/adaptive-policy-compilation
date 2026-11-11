"""
THE ASKS OF A SESSION, SEVERAL AT A TIME. For asks only, and for the plans to
come: no plan uses it yet. `PLAN_HALVES.md`'s sessions run one at a time, as
signed, and nothing here touches them.

--------------------------------------------------------------------------
WHAT IT IS FOR, AND WHAT IT IS NEVER FOR
--------------------------------------------------------------------------
An ask session sends prompts fixed before it starts, and Stage A keeps each
one's digest. Nothing the model answers is installed, executed or shown to a
later prompt. The calls are independent, so the order in which they come back
changes no prompt and no answer. Rule 3 of `PLAN_FIDELITY.md` said so, and kept
its calls sequential anyway, as a choice. Every ask plan since has run its
sessions one call at a time, for hours.

A loop is the opposite case, and hard rule 3 forbids this module there. Every
rule a loop installs changes whether the next case escalates, so the order of
its calls is the experiment. `tests/test_ask_pool.py` fails if a loop's runner,
or a module that drives an engine, imports this one.

--------------------------------------------------------------------------
WHAT IT KEEPS FROM THE SEQUENTIAL LOOP
--------------------------------------------------------------------------
  * **The order of dispatch is the session's seeded order.** At most `workers`
    asks are in flight, and the next one leaves only when one comes back. The
    arms stay interleaved as the seed interleaved them.
  * **Each ask's row is its own call's.** Every ask in flight holds a worker of
    its own: its asker, its client and its recorder, built by the caller's
    `make_worker` before the first ask. A worker is never shared, because
    `harness.call_record.CallRecorder` keeps one list of attempts, and
    `reasoned_loop.protocol.Live.ask` takes it before and after each call. Two
    calls in flight on one recorder would trade attempts, and a row's `valid`
    reads its attempts' provider.
  * **One writer.** The calling thread keeps the rows, one whole line at a
    time, through the caller's `keep`. No worker writes.
  * **The resume.** An id the partial file already holds is not asked again,
    wherever it stood. The rows come back sorted by position.
  * **The breaker.** A run of `max_failures` failed asks stops the session as an
    outage, read in the order the asks come back. Those failures are not kept,
    so a resume asks them again. Fewer failures followed by an answer are kept,
    as answers the model did not give, and so are failures left at the end.
  * **With one worker, it is the sequential loop.** It writes the same rows, in
    the same order, to the partial file. `tests/test_ask_pool.py` holds it to
    `halves/ask.py`'s loop, called and not edited.

--------------------------------------------------------------------------
WHAT IT CHANGES, WHICH A PLAN THAT USES IT SAYS IN ITS §0
--------------------------------------------------------------------------
  1. **The seconds.** A row's `seconds` are measured with up to `workers` calls
     in flight on the provider. A pace read off them prices a session at that
     concurrency. It is not comparable with a pace read one call at a time.
  2. **The order of the partial file.** Its lines, and `asked_at`, follow the
     order the answers came back in, not the seeded order. The record is sorted
     by position.
  3. **The provider's load.** The provider receives `workers` requests at once,
     and may refuse some for the rate. While any worker waits, nothing new is
     dispatched: the pool narrows to the calls in flight until the wait ends. A
     wait is a call retried after a wait, or a call refused for the rate and
     waited out.
     - **How refusals are counted.** The `openai` client retries a refused call
       twice on its own, with its own backoff, before the recorder sees
       anything. So a count of refusals read off `call_attempts` counts calls
       refused three times in a row, not refusals.
  4. **A stop drains.** A stop is the breaker tripping, or a call raising: an
     outage, a rate limit through every wait, or an interrupt. After it,
     nothing more is dispatched, and the asks in flight are waited for. The
     answers among them are kept and the failures are not; then the stop is
     raised. An interrupt during that wait abandons it.
  5. **The answers.** At temperature 0 they already vary from call to call,
     partly with what the provider batches each request with. A session's own
     calls add to that batching, which other users' traffic changes all the
     time anyway, and nothing in the dispatch favours an arm. That is an
     argument from construction, not a measurement. A plan that wants a
     measurement buys it.

A plan that uses it declares, before signature:
  * `workers`, and why;
  * that its sessions are asks;
  * that it reads seconds at that concurrency;
  * that its smoke run measures pace and refusals for the rate at that
    concurrency, and that it falls back to one call at a time if the smoke run
    meets a refusal;
  * how the breaker reads failures in a row.

--------------------------------------------------------------------------
WHAT THE CALLER GIVES IT
--------------------------------------------------------------------------
  order          the session's ids, in its seeded order
  done           the rows the partial file already holds (`open_partial`)
  ask_one        (worker, position, id) -> row; a failed ask is a row whose
                 `failure` is not None, and anything it raises stops the session
  make_worker    (sleep) -> worker. The worker's asker must sleep through
                 `sleep`, so that a wait holds the dispatch
  keep           row -> None, one whole line, flushed
  workers        how many asks may be in flight
  max_failures   the breaker
  outage         what to raise when the breaker trips, given its message

Every row carries `id` and `position`. A plan's `ask()` then reads as
`halves/ask.py`'s does, with its loop replaced:

    def ask(session, design, make_live, partial, header, workers,
            clock=time.monotonic):
        done, resumed = open_partial(partial, header)

        def ask_one(live, position, aid):
            a = design.asks[aid]
            t0 = clock()
            try:
                got = live.ask(a.messages())
                failure, attempts = None, list(got.call_attempts or [])
            except ProposalError as exc:
                got, failure = exc, str(exc)[:300]
                attempts = list(getattr(exc, "call_attempts", []) or [])
            row = row_of(session, position, a, None if failure else got,
                         failure, attempts, clock() - t0)
            if failure is not None:
                row["finish_reason"] = getattr(got, "finish_reason", None)
            return row

        with partial.open("a") as f:
            def keep(row):
                f.write(json.dumps(row) + "\\n")
                f.flush()
            rows = ask_pool.run(design.sessions[session], done, ask_one,
                                make_live, keep, workers=workers,
                                max_failures=plan.MAX_CONSECUTIVE_FAILURES,
                                outage=Outage)
        return rows, [now()] if resumed else []

Here `make_live` is `lambda sleep: build_live(sleep=sleep)`.
"""

from __future__ import annotations

import queue
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Sequence

POLL = 1.0   # seconds between looks for an answer, and at a held dispatch


class Hold:
    """How many workers are waiting inside a call. While any is, nothing new is
    dispatched."""

    def __init__(self, sleep: Callable[[float], None]):
        self._sleep = sleep
        self._lock = threading.Lock()
        self._waiting = 0

    def sleep(self, seconds: float) -> None:
        with self._lock:
            self._waiting += 1
        try:
            self._sleep(seconds)
        finally:
            with self._lock:
                self._waiting -= 1

    @property
    def held(self) -> bool:
        with self._lock:
            return self._waiting > 0


def failed(row: dict[str, Any]) -> bool:
    """A failed ask: the call never gave an answer that parsed."""
    return row.get("failure") is not None


def by_position(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: r["position"])


def _next(answers: queue.Queue, timeout: float) -> Future:
    """The next ask to come back, in the order they come back, or `queue.Empty`
    after `timeout`."""
    return answers.get(timeout=timeout)


def run(order: Sequence[str], done: Sequence[dict[str, Any]],
        ask_one: Callable[[Any, int, str], dict[str, Any]],
        make_worker: Callable[[Callable[[float], None]], Any],
        keep: Callable[[dict[str, Any]], None], *, workers: int, max_failures: int,
        outage: Callable[[str], BaseException],
        progress: Callable[[dict[str, Any], int, int], None] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        poll: float = POLL) -> list[dict[str, Any]]:
    """Every ask of `order` that `done` does not hold, at most `workers` at a
    time. Returns `done` and the new rows, sorted by position. A stop raises
    once the asks in flight are back."""
    if workers < 1:
        raise ValueError(f"workers must be at least 1, not {workers}")
    if max_failures < 1:
        raise ValueError(f"max_failures must be at least 1, not {max_failures}")
    rows = list(done)
    asked = {r["id"] for r in rows}
    todo = [(position, aid) for position, aid in enumerate(order) if aid not in asked]
    if not todo:
        return by_position(rows)

    hold = Hold(sleep)
    slots = min(workers, len(todo))
    free: queue.SimpleQueue = queue.SimpleQueue()
    for _ in range(slots):
        free.put(make_worker(hold.sleep))

    def task(position: int, aid: str) -> dict[str, Any]:
        worker = free.get_nowait()    # never empty: no more asks in flight than workers
        try:
            return ask_one(worker, position, aid)
        finally:
            free.put(worker)

    answers: queue.Queue = queue.Queue()  # the asks, as they come back
    inflight: set[Future] = set()
    pending: list[dict[str, Any]] = []   # failures not yet known to be isolated
    stop: BaseException | None = None    # the first stop: raised once the drain ends
    tripped: str | None = None           # the breaker's message
    nxt = 0
    pool = ThreadPoolExecutor(max_workers=slots, thread_name_prefix="ask")
    try:
        while True:
            while (stop is None and tripped is None and nxt < len(todo)
                   and len(inflight) < slots and not hold.held):
                position, aid = todo[nxt]
                nxt += 1
                fut = pool.submit(task, position, aid)
                inflight.add(fut)
                fut.add_done_callback(answers.put)
            if not inflight:
                break
            try:
                fut = _next(answers, poll)
            except queue.Empty:
                continue                  # a held dispatch is looked at again
            except KeyboardInterrupt as exc:
                if stop is not None:
                    raise                 # a second stop abandons the drain
                stop = exc
                continue
            inflight.discard(fut)
            try:
                row = fut.result()
            except BaseException as exc:  # noqa: BLE001 — raised once drained
                if stop is None:
                    stop = exc
                continue
            if failed(row):
                pending.append(row)
                if stop is None and tripped is None and len(pending) >= max_failures:
                    tripped = (f"{len(pending)} asks in a row failed, the last with: "
                               f"{row['failure']}")
                continue
            if stop is None and tripped is None:
                for r in pending:
                    keep(r)
                    rows.append(r)
                pending = []
            keep(row)
            rows.append(row)
            if progress is not None:
                progress(row, len(rows), len(order))
    except BaseException:
        pool.shutdown(wait=False, cancel_futures=True)
        raise
    pool.shutdown(wait=True)
    if stop is not None:
        raise stop
    if tripped is not None:
        raise outage(tripped)
    for r in pending:
        keep(r)
        rows.append(r)
    return by_position(rows)
