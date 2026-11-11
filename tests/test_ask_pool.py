"""
`harness/ask_pool.py`: the asks of a session, several at a time.

  * **With one worker it is `halves/ask.py`'s loop**, called and not edited. It
    writes the same partial file, line for line, and the same record, through
    the real asker under an SDK double. That holds for answers, isolated
    failures, the breaker, an interrupt and the resume.
  * **With several workers, the same rows by position.** Each row carries its
    own call's attempts. There are never more asks in flight than workers, and
    they leave in the seeded order.
  * **A worker serves one ask at a time.** The test shows what two calls in
    flight on one recorder do.
  * **The stops.** The breaker reads failures in the order they come back. A
    stop drains the asks in flight and keeps their answers, not their failures.
    A second interrupt abandons the drain, and a wait inside a call holds the
    dispatch.
  * **No loop imports it** (hard rule 3).

No call is made: the only answers are the doubles'.
"""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from authorship import run as erun
from halves import ask, plan, population
from harness import ask_pool
from harness.call_record import CallRecorder
from rung2.proposers2 import ProposalError
from tests.doubles import fake_sdk

REPO = Path(__file__).resolve().parent.parent
SESSION = "pass1"
TIMING = ("seconds", "asked_at")      # what a row says about when, not what
RULE = {"action": "T2_TECHNICAL", "conditions": [{"attr": "severity", "op": "eq", "value": 1}],
        "beats": [], "loses_to": [], "note": "una regla"}
WAIT = 5.0                            # the longest any test waits on another thread


def no_wait(seconds: float) -> None:
    """The asker's waits, skipped."""


def key_of(messages) -> str:
    return hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()[:12]


class ByContent:
    """An SDK double whose every response depends on its request alone, so the
    order the calls are made in changes nothing it returns. Its generation id
    names the request, and every response is served by the pinned provider,
    with reasoning. A request whose messages are in `refuse` raises, as a
    dropped connection does. Safe across threads. `jitter` delays each response
    by up to that many seconds, fixed by the request, so that answers come back
    out of the order they were asked in."""

    def __init__(self, refuse=(), jitter: float = 0.0):
        self.refuse = set(refuse)
        self.jitter = jitter
        self.lock = threading.Lock()
        self.count: dict[str, int] = {}
        self.built_with: dict = {}
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        key = key_of(kwargs["messages"])
        with self.lock:
            n = self.count[key] = self.count.get(key, 0) + 1
        if self.jitter:
            time.sleep(int(key[:4], 16) / 0xFFFF * self.jitter)
        if key in self.refuse:
            raise ConnectionError("the double refuses this request")
        message = SimpleNamespace(content=json.dumps(RULE), reasoning="H04 casa el ticket.")
        return SimpleNamespace(
            id=f"gen-{key}-{n}", provider=plan.PROVIDER_NAME, model=kwargs.get("model"),
            system_fingerprint=None,
            choices=[SimpleNamespace(message=message, finish_reason="stop",
                                     native_finish_reason="stop")],
            usage=SimpleNamespace(prompt_tokens=100, completion_tokens=20, total_tokens=120,
                                  completion_tokens_details=SimpleNamespace(
                                      reasoning_tokens=321)))


class Interrupting:
    """A `Live` that raises after `n` asks, as a ^C does."""

    def __init__(self, inner, n: int):
        self.inner, self.n, self.k = inner, n, 0

    def ask(self, messages):
        self.k += 1
        if self.k == self.n:
            raise KeyboardInterrupt
        return self.inner.ask(messages)


def header(session: str) -> dict:
    return {"protocol": json.loads(json.dumps(ask.protocol())), "session": session,
            "sample_sha256": "x"}


def sequential(design, live, partial: Path):
    """`halves/ask.py`'s loop, called."""
    return ask.ask(SESSION, design, live, partial, header(SESSION))


def live_maker(sleep):
    return ask.build_live(sleep=sleep)


def pooled(design, make_worker, partial: Path, workers: int):
    """`halves/ask.py`'s `ask`, with its loop replaced by the pool, as the
    module's docstring writes it."""
    done, resumed = ask.open_partial(partial, header(SESSION))

    def ask_one(live, position, aid):
        a = design.asks[aid]
        t0 = time.monotonic()
        try:
            got = live.ask(a.messages())
            failure, attempts = None, list(got.call_attempts or [])
        except ProposalError as exc:
            got, failure = exc, str(exc)[:300]
            attempts = list(getattr(exc, "call_attempts", []) or [])
        row = ask.row_of(SESSION, position, a, None if failure else got, failure, attempts,
                         time.monotonic() - t0)
        if failure is not None:
            row["finish_reason"] = getattr(got, "finish_reason", None)
        return row

    with partial.open("a") as f:
        def keep(row):
            f.write(json.dumps(row) + "\n")
            f.flush()
        rows = ask_pool.run(design.sessions[SESSION], done, ask_one, make_worker, keep,
                            workers=workers, max_failures=plan.MAX_CONSECUTIVE_FAILURES,
                            outage=ask.Outage, sleep=no_wait, poll=0.005)
    return rows, ([ask.now()] if resumed else [])


def strip(row: dict) -> dict:
    return {k: v for k, v in row.items() if k not in TIMING}


def lines(partial: Path) -> list[dict]:
    out = [json.loads(line) for line in partial.read_text().splitlines()]
    return out[:1] + [strip(r) for r in out[1:]]


# ---------------------------------------------------------------------------
# Through the real asker, under the SDK double
# ---------------------------------------------------------------------------

class TestThroughTheRealAsker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        full = population.build()
        cls.design = dataclasses.replace(
            full, sessions={s: v[:12] for s, v in full.sessions.items()})
        cls.order = cls.design.sessions[SESSION]

    def keys(self, positions) -> set[str]:
        return {key_of(self.design.asks[self.order[i]].messages()) for i in positions}

    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.d = Path(self._d.name)
        quiet = mock.patch("builtins.print")
        quiet.start()
        self.addCleanup(quiet.stop)
        self.addCleanup(self._d.cleanup)

    def test_one_worker_writes_what_the_sequential_loop_writes(self):
        refuse = self.keys((2, 7))
        with fake_sdk(openai=ByContent(refuse)):
            seq, _ = sequential(self.design, ask.build_live(sleep=no_wait), self.d / "seq")
        with fake_sdk(openai=ByContent(refuse)):
            one, _ = pooled(self.design, live_maker, self.d / "one", workers=1)
        self.assertEqual(lines(self.d / "one"), lines(self.d / "seq"))
        self.assertEqual([strip(r) for r in one], [strip(r) for r in seq])
        self.assertEqual([r["position"] for r in seq if r["failure"]], [2, 7])
        self.assertEqual(sum(1 for r in seq if r["valid"]), len(self.order) - 2)

    def test_the_breaker_trips_where_the_loop_trips(self):
        refuse = self.keys(range(len(self.order)))
        with fake_sdk(openai=ByContent(refuse)):
            with self.assertRaises(ask.Outage) as seq:
                sequential(self.design, ask.build_live(sleep=no_wait), self.d / "seq")
        with fake_sdk(openai=ByContent(refuse)):
            with self.assertRaises(ask.Outage) as one:
                pooled(self.design, live_maker, self.d / "one", workers=1)
        self.assertEqual(str(one.exception), str(seq.exception))
        self.assertEqual(lines(self.d / "one"), lines(self.d / "seq"))
        self.assertEqual(len(lines(self.d / "one")), 1)      # the header, and no failure

    def test_an_interrupt_and_the_resume_leave_what_the_loop_leaves(self):
        with fake_sdk(openai=ByContent()):
            with self.assertRaises(KeyboardInterrupt):
                sequential(self.design, Interrupting(ask.build_live(sleep=no_wait), 4),
                           self.d / "seq")
            seq, seq_resumed = sequential(self.design, ask.build_live(sleep=no_wait),
                                          self.d / "seq")
        with fake_sdk(openai=ByContent()):
            with self.assertRaises(KeyboardInterrupt):
                pooled(self.design, lambda sleep: Interrupting(live_maker(sleep), 4),
                       self.d / "one", workers=1)
            self.assertEqual(len(lines(self.d / "one")), 4)  # the header and three rows
            one, one_resumed = pooled(self.design, live_maker, self.d / "one", workers=1)
        self.assertEqual(lines(self.d / "one"), lines(self.d / "seq"))
        self.assertEqual([strip(r) for r in one], [strip(r) for r in seq])
        self.assertEqual((len(one_resumed), len(seq_resumed)), (1, 1))

    def test_several_workers_give_the_same_rows_by_position(self):
        refuse = self.keys((2, 7))
        with fake_sdk(openai=ByContent(refuse)):
            one, _ = pooled(self.design, live_maker, self.d / "one", workers=1)
        with fake_sdk(openai=ByContent(refuse, jitter=0.02)):
            four, _ = pooled(self.design, live_maker, self.d / "four", workers=4)
        self.assertEqual([strip(r) for r in four], [strip(r) for r in one])
        as_text = lambda p: sorted(json.dumps(r, sort_keys=True) for r in lines(p)[1:])
        self.assertEqual(as_text(self.d / "four"), as_text(self.d / "one"))
        self.assertEqual(lines(self.d / "four")[0], lines(self.d / "one")[0])

    def test_each_row_keeps_its_own_calls_attempts(self):
        refuse = self.keys((2, 7))
        with fake_sdk(openai=ByContent(refuse, jitter=0.02)):
            rows, _ = pooled(self.design, live_maker, self.d / "four", workers=4)
        for r in rows:
            with self.subTest(r["id"]):
                key = key_of(self.design.asks[r["id"]].messages())
                if r["failure"] is None:
                    self.assertTrue(r["valid"])
                    self.assertEqual([a["generation_id"] for a in r["call_attempts"]],
                                     [f"gen-{key}-1"])
                else:
                    self.assertEqual([a["error"] for a in r["call_attempts"]],
                                     ["ConnectionError"] * (plan.MAX_RETRIES + 1))

    def test_an_interrupted_pool_resumes_where_it_stopped(self):
        """Several workers leave the partial file out of order, and the resume
        asks only what it does not hold."""
        with fake_sdk(openai=ByContent(jitter=0.02)), \
             mock.patch.object(ask_pool, "_next", interrupt_on(3)):
            with self.assertRaises(KeyboardInterrupt):
                pooled(self.design, live_maker, self.d / "four", workers=4)
        held = {r["id"] for r in lines(self.d / "four")[1:]}
        self.assertTrue(held)
        client = ByContent()
        with fake_sdk(openai=client):
            rows, resumed = pooled(self.design, live_maker, self.d / "four", workers=4)
        self.assertEqual([r["id"] for r in rows], self.order)
        self.assertEqual(len(resumed), 1)
        asked_again = {aid for aid in self.order
                       if client.count.get(key_of(self.design.asks[aid].messages()))}
        self.assertEqual(asked_again, set(self.order) - held)


def interrupt_on(n: int):
    """The pool's look for the next answer, interrupted at its `n`-th look, as
    a ^C in the calling thread."""
    real, seen = ask_pool._next, {"n": 0}

    def look(*args, **kwargs):
        seen["n"] += 1
        if seen["n"] == n:
            raise KeyboardInterrupt
        return real(*args, **kwargs)
    return look


# ---------------------------------------------------------------------------
# The pool alone, over asks that are rows written by hand
# ---------------------------------------------------------------------------

class Outage(Exception):
    pass


def row(aid: str, position: int, failure: str | None = None) -> dict:
    return {"id": aid, "position": position, "failure": failure}


def ids(n: int) -> list[str]:
    return [f"a{i}" for i in range(n)]


class Worker:
    def __init__(self, sleep):
        self.sleep = sleep
        self.busy = False


def bare(order, ask_one, *, workers: int, done=(), max_failures: int = 5,
         sleep=no_wait, make_worker=Worker):
    kept: list[dict] = []
    rows = ask_pool.run(order, list(done), ask_one, make_worker, kept.append,
                        workers=workers, max_failures=max_failures, outage=Outage,
                        sleep=sleep, poll=0.005)
    return rows, kept


class Starts:
    """Which asks started, in what order, and how many were ever in flight."""

    def __init__(self):
        self.lock = threading.Lock()
        self.order: list[int] = []
        self.now = self.most = 0

    def enter(self, position: int) -> None:
        with self.lock:
            self.order.append(position)
            self.now += 1
            self.most = max(self.most, self.now)

    def leave(self) -> None:
        with self.lock:
            self.now -= 1


class TestTheDispatch(unittest.TestCase):

    def test_never_more_in_flight_than_workers_and_they_leave_in_order(self):
        k, order = 3, ids(20)
        starts, together = Starts(), threading.Barrier(3, timeout=WAIT)

        def ask_one(w, position, aid):
            starts.enter(position)
            if position < k:
                together.wait()           # the first three are in flight at once
            time.sleep(0.001)
            starts.leave()
            return row(aid, position)

        rows, kept = bare(order, ask_one, workers=k)
        self.assertEqual(starts.most, k)
        self.assertEqual(set(starts.order[:k]), set(range(k)))
        for i, position in enumerate(starts.order):
            self.assertLess(position, i + k)       # never ahead of the seeded order
        self.assertEqual([r["id"] for r in rows], order)
        self.assertEqual(len(kept), len(order))

    def test_one_worker_leaves_in_the_seeded_order(self):
        starts = Starts()

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            return row(aid, position)

        bare(ids(9), ask_one, workers=1)
        self.assertEqual(starts.order, list(range(9)))

    def test_a_worker_serves_one_ask_at_a_time(self):
        built: list[Worker] = []

        def make(sleep):
            built.append(Worker(sleep))
            return built[-1]

        def ask_one(w, position, aid):
            if w.busy:
                raise AssertionError("a worker was handed two asks at once")
            w.busy = True
            time.sleep(0.002)
            w.busy = False
            return row(aid, position)

        bare(ids(16), ask_one, workers=4, make_worker=make)
        self.assertEqual(len(built), 4)
        built.clear()
        bare(ids(2), ask_one, workers=4, make_worker=make)
        self.assertEqual(len(built), 2)            # no more workers than asks

    def test_two_calls_in_flight_on_one_recorder_trade_attempts(self):
        """Why a worker is never shared. This is what `Live.ask` does around
        each call, for two calls in flight on one recorder."""
        inner = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
            create=lambda **kw: SimpleNamespace(id=kw["tag"]))))
        rec = CallRecorder(inner)
        rec.take()                                   # call A starts
        rec.chat.completions.create(tag="gen-A")     # A's answer comes back
        rec.take()                                   # call B starts, and wipes A's attempt
        rec.chat.completions.create(tag="gen-B")     # B's answer comes back
        a, b = rec.take(), rec.take()                # A ends, then B
        self.assertEqual([x["generation_id"] for x in a], ["gen-B"])
        self.assertEqual(b, [])

    def test_a_resume_asks_only_what_the_file_does_not_hold(self):
        done = [row("a5", 5), row("a1", 1)]          # left out of order by several workers
        starts = Starts()

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            return row(aid, position)

        rows, kept = bare(ids(8), ask_one, workers=3, done=done)
        self.assertEqual(sorted(starts.order), [0, 2, 3, 4, 6, 7])
        self.assertEqual([r["id"] for r in rows], ids(8))
        self.assertEqual(len(kept), 6)

    def test_a_session_already_asked_builds_nothing(self):
        def never(*args):
            raise AssertionError("nothing is left to ask")

        rows, kept = bare(ids(2), never, workers=4, done=[row("a1", 1), row("a0", 0)],
                          make_worker=never)
        self.assertEqual([r["id"] for r in rows], ["a0", "a1"])
        self.assertEqual(kept, [])

    def test_it_refuses_no_worker_and_no_breaker(self):
        with self.assertRaises(ValueError):
            bare(ids(2), None, workers=0)
        with self.assertRaises(ValueError):
            bare(ids(2), None, workers=2, max_failures=0)


class TestTheStops(unittest.TestCase):

    def test_isolated_and_trailing_failures_are_kept(self):
        fail = {1, 4, 9}

        def ask_one(w, position, aid):
            return row(aid, position, "refused" if position in fail else None)

        rows, kept = bare(ids(10), ask_one, workers=3)
        self.assertEqual([r["id"] for r in rows], ids(10))
        self.assertEqual({r["position"] for r in rows if r["failure"]}, fail)
        self.assertEqual(len(kept), 10)

    def test_the_breaker_reads_failures_as_they_come_back(self):
        k, first_failure, most = 3, 4, 5
        starts, lock, answered = Starts(), threading.Lock(), {"n": 0}
        all_answered = threading.Event()
        kept_rows: list[dict] = []

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            if position < first_failure:
                with lock:
                    answered["n"] += 1
                    if answered["n"] == first_failure:
                        all_answered.set()
                return row(aid, position)
            self.assertTrue(all_answered.wait(WAIT))  # failures come back after every answer
            time.sleep(0.02)
            return row(aid, position, "refused")

        with self.assertRaises(Outage) as stop:
            ask_pool.run(ids(30), [], ask_one, Worker, kept_rows.append, workers=k,
                         max_failures=most, outage=Outage, sleep=no_wait, poll=0.005)
        self.assertEqual(str(stop.exception), "5 asks in a row failed, the last with: refused")
        self.assertEqual(sorted(r["id"] for r in kept_rows), ids(first_failure))
        # Dispatched before the trip: the answers and four failures back, and
        # no more than `k` asks in flight beside them.
        self.assertLessEqual(max(starts.order), first_failure + most + k - 2)

    def test_the_breaker_keeps_the_answers_in_flight_and_not_the_failures(self):
        failures = threading.Semaphore(0)
        kept_rows: list[dict] = []

        def ask_one(w, position, aid):
            if position != 5:
                failures.release()
                return row(aid, position, "refused")
            for _ in range(5):                       # comes back after the breaker trips
                self.assertTrue(failures.acquire(timeout=WAIT))
            time.sleep(0.1)
            return row(aid, position)

        with self.assertRaises(Outage):
            ask_pool.run(ids(12), [], ask_one, Worker, kept_rows.append, workers=6,
                         max_failures=5, outage=Outage, sleep=no_wait, poll=0.005)
        self.assertEqual([r["id"] for r in kept_rows], ["a5"])

    def test_a_call_that_raises_stops_the_dispatch_and_drains(self):
        raised = threading.Event()
        outage = erun.Outage("the double's outage")
        starts, kept_rows = Starts(), []

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            if position == 2:
                raised.set()
                raise outage
            self.assertTrue(raised.wait(WAIT))
            time.sleep(0.1)
            return row(aid, position)

        with self.assertRaises(erun.Outage) as stop:
            ask_pool.run(ids(10), [], ask_one, Worker, kept_rows.append, workers=3,
                         max_failures=5, outage=Outage, sleep=no_wait, poll=0.005)
        self.assertIs(stop.exception, outage)
        self.assertEqual(sorted(starts.order), [0, 1, 2])
        self.assertEqual(sorted(r["id"] for r in kept_rows), ["a0", "a1"])

    def test_an_interrupt_drains_the_asks_in_flight(self):
        starts = Starts()

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            return row(aid, position)

        with mock.patch.object(ask_pool, "_next", interrupt_on(1)):
            with self.assertRaises(KeyboardInterrupt):
                bare(ids(10), ask_one, workers=3)
        self.assertEqual(sorted(starts.order), [0, 1, 2])

    def test_an_interrupt_keeps_what_comes_back_after_it(self):
        kept_rows: list[dict] = []

        def ask_one(w, position, aid):
            return row(aid, position)

        with mock.patch.object(ask_pool, "_next", interrupt_on(1)):
            with self.assertRaises(KeyboardInterrupt):
                ask_pool.run(ids(10), [], ask_one, Worker, kept_rows.append, workers=3,
                             max_failures=5, outage=Outage, sleep=no_wait, poll=0.005)
        self.assertEqual(sorted(r["id"] for r in kept_rows), ["a0", "a1", "a2"])

    def test_a_second_interrupt_abandons_the_drain(self):
        release = threading.Event()
        kept_rows: list[dict] = []

        def ask_one(w, position, aid):
            release.wait(WAIT)
            return row(aid, position)

        def always(*args, **kwargs):
            raise KeyboardInterrupt

        try:
            with mock.patch.object(ask_pool, "_next", always):
                with self.assertRaises(KeyboardInterrupt):
                    ask_pool.run(ids(10), [], ask_one, Worker, kept_rows.append,
                                 workers=3, max_failures=5, outage=Outage, sleep=no_wait,
                                 poll=0.005)
        finally:
            release.set()
        self.assertEqual(kept_rows, [])

    def test_a_wait_inside_a_call_holds_the_dispatch(self):
        entered, release = threading.Event(), threading.Event()
        together = threading.Barrier(3, timeout=WAIT)
        starts, out = Starts(), {}

        def waiting(seconds):
            entered.set()
            release.wait(WAIT)

        def ask_one(w, position, aid):
            starts.enter(position)
            starts.leave()
            if position < 3:
                together.wait()              # the three slots fill before anyone waits
            if position == 1:
                w.sleep(60)                  # a retry's wait, through the worker's sleep
            elif position in (0, 2):
                entered.wait(WAIT)           # they come back once the wait has begun
            return row(aid, position)

        def session():
            out["rows"], out["kept"] = bare(ids(8), ask_one, workers=3, sleep=waiting)

        t = threading.Thread(target=session)
        t.start()
        try:
            self.assertTrue(entered.wait(WAIT))
            time.sleep(0.1)                  # 0 and 2 come back while 1 waits
            held = sorted(starts.order)
        finally:
            release.set()
            t.join(WAIT)
        self.assertFalse(t.is_alive())
        self.assertEqual(held, [0, 1, 2])     # nothing left while a worker waited
        self.assertEqual([r["id"] for r in out["rows"]], ids(8))


# ---------------------------------------------------------------------------
# Hard rule 3: no loop imports it
# ---------------------------------------------------------------------------

ENGINES = ("rung2.engine2", "harness.shadow", "harness.dsl")
LOOP_NAMES = ("run.py", "run2.py", "run_experiment.py", "loop.py")
SKIP = {".git", ".venv", "tests", "scratch", "__pycache__"}


def imports_of(source: str) -> set[str]:
    out: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            out |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            out.add(node.module)
            out |= {f"{node.module}.{a.name}" for a in node.names}
    return out


def a_loop_with_the_pool(name: str, source: str) -> bool:
    """A loop's runner, or a module that drives an engine, importing the pool."""
    found = imports_of(source)
    if "harness.ask_pool" not in found:
        return False
    return name in LOOP_NAMES or any(m == e or m.startswith(e + ".")
                                     for m in found for e in ENGINES)


class TestNoLoopImportsIt(unittest.TestCase):

    def test_no_module_of_the_tree_does(self):
        offenders = [str(p.relative_to(REPO)) for p in REPO.rglob("*.py")
                     if not SKIP & set(p.relative_to(REPO).parts)
                     and a_loop_with_the_pool(p.name, p.read_text())]
        self.assertEqual(offenders, [])

    def test_the_check_bites(self):
        self.assertTrue(a_loop_with_the_pool("run.py", "from harness import ask_pool\n"))
        self.assertTrue(a_loop_with_the_pool(
            "score.py", "import rung2.engine2\nfrom harness.ask_pool import run\n"))
        self.assertTrue(a_loop_with_the_pool("loop.py", "import harness.ask_pool\n"))
        self.assertFalse(a_loop_with_the_pool("ask.py", "from harness import ask_pool\n"))
        self.assertFalse(a_loop_with_the_pool("run.py", "from harness import call_record\n"))


if __name__ == "__main__":
    unittest.main()
