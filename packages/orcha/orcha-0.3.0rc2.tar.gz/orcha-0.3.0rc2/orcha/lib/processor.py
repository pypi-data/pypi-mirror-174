#                                   MIT License
#
#              Copyright (c) 2021 Javier Alonso <jalonso@teldat.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#      copies of the Software, and to permit persons to whom the Software is
#            furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
#                 copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#                                    SOFTWARE.
"""
The class :class:`Processor` is responsible for handing queues, objects and petitions.
Alongside with :class:`Manager <orcha.lib.Manager>`, it's the heart of the orchestrator.
"""
from __future__ import annotations

import errno
import multiprocessing
import random
import typing
from queue import PriorityQueue, Queue
from threading import Event, Lock, Thread

from typing_extensions import final

from orcha import properties
from orcha.interfaces.message import Message
from orcha.interfaces.petition import EmptyPetition, Petition, PetitionState
from orcha.utils.logging_utils import get_logger

if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union

    from orcha.lib import Manager

log = get_logger()


@final
class Processor:
    """
    :class:`Processor` is a **singleton** whose responsibility is to handle and manage petitions
    and signals collaborating with the corresponding :class:`Manager`. This class has multiple
    queues and threads for handling incoming requests. The following graph intends to show how
    it works internally::

        ┌─────────────────┐
        |                 ├───────────────────────────────┐       ╔════════════════╗
        |   Processor()   ├──────┬───────────────┐        ├──────►║ Message thread ║
        |                 |      |               |        |       ╚═════╦══════════╝
        └┬───────┬────────┘      |               |        |         ▲   ║   ╔═══════════════╗
         |       |               |               |        └─────────╫───╫──►║ Signal thread ║
         |       |               |               |                  ║   ║   ╚═══════╦═══════╝
         |       |               |               |                  ║   ║ t   ▲     ║
         |       ▼               |               ▼                  ║   ║ o   ║     ║
         | ┌───────────┐ send(m) |  ┌─────────────────────────┐     ║   ║     ║     ║
         | | Manager() ╞═════════╪═►   Message queue (proxy)   ═════╝   ║ p   ║     ║
         | └─────╥─────┘         ▼  └─────────────────────────┘         ║ e   ║     ║
         |       ║  finish(m)   ┌──────────────────────────┐            ║ t   ║     ║
         |       ╚═════════════►    Signal queue (proxy)    ════════════║═════╝     ║
         |                      └──────────────────────────┘            ║ i         ║
         |                                                              ║ t         ║
         |                                  Priority queue              ║ i         ║
         |                      ┌─────────────────────────┐             ║ o         ║
         |              ╔═══════  Internal petition queue  ◄═══════╦════╝ n         ║
         |              ║       └─────────────────────────┘        ║                ║
         |              ║           ┌─────────────────────────┐    ║                ║
         |              ║        ╔══   Internal signal queue   ◄═══║════════════════╝
         |              ║        ║  └─────────────────────────┘    ║
         |              ║        ║                                 ║      not
         |              ▼        ╚══════╗                          ║ p.condition(p)
         | ╔══════════════════════════╗ ║       ╔══════════════════╩═════╗
         ├►║ Internal petition thread ╠═║══════►║ Petition launch thread ║
         | ╚══════════════════════════╝ ▼       ╚══════════════════╤═════╝
         |       ╔════════════════════════╗                 ▲      |  ┌───────────────────────────┐
         └──────►║ Internal signal thread ╠═════════════════╝      ├─►| manager.start_petition(p) |
                 ╚════════════════════════╝   send SIGTERM         |  └───────────────────────────┘
                                                                   |   ┌─────────────────┐
                                                                   ├──►| p.action(fn, p) |
                                                                   |   └─────────────────┘
                                                                   | ┌────────────────────────────┐
                                                                   └►| manager.finish_petition(p) |
                                                                     └────────────────────────────┘

    Note:
        Ideally, you don't need to create any instance for this class, as it is completely
        managed by :class:`Manager` (in particular, see
        :attr:`processor <orcha.lib.Manager.processor>`). The diagram above is posted for
        informational purposes, as this class is big and can be complex in some situations
        or without knowledge about multiprocessing. Below a detailed explanation on how
        it works is added to the documentation so anyone can understand the followed
        process.

    1. **Queues**

    The point of having four :py:class:`queues <queue.Queue>` is that messages are traveling
    across threads in a safe way. When a message is received from another process, there is
    some "black magic" going underneath the
    :py:class:`BaseManager <multiprocessing.managers.BaseManager>` class involving pipes, queues
    and other synchronization mechanisms.

    With that in mind, take into account that messages are not received (yet) by our
    process but by the manager server running on another IP and port, despite the fact that
    the manager is ours.

    That's why a
    `proxy <https://docs.python.org/3/library/multiprocessing.html#proxy-objects>`_
    object is involved in the entire equation. For summarizing, a proxy object is an object
    that presumably lives in another process. In general, writing or reading data from a
    proxy object causes every other process to notice our action (in terms that a new item
    is now available for everyone, a deletion happens for all of them, etc).

    If we decide to use :py:class:`queues <multiprocessing.Queue>` instead, additions
    or deletions won't be propagated to the rest of the processes as it is a local-only
    object.

    For that reason, there is four queues: two of them have the mission of receiving
    the requests from other processes and once the request is received by us and is
    available on our process, it is then added to an internal priority queue by the
    handler threads (allowing, for example, sorting of the petitions based on their
    priority, which wouldn't be possible on a proxied queue).

    2. **Threads**

    As you may notice, there is almost two threads per queue: one is a **producer** and
    the other one is the **consumer** (following the producer/consumer model). The need
    of so much threads (5 at the time this is being written) is **to not to block** any
    processes and leave the orchestrator free of load.

    As the queues are synchronous, which means that the thread is forced to wait until
    an item is present (see :py:attr:`Queue.get() <queue.Queue.get>`), waiting for petitions
    will pause the entire main thread until all queues are unlocked sequentially, one after
    each other, preventing any other request to arrive and being processed.

    That's the reason why there are two threads just listening to proxied queues and placing
    the requests on another queue. In addition, the execution of the action is also run
    asynchronously in order to not to block the main thread during the processing (this
    also applies to the evaluation of the :attr:`condition <orcha.interfaces.Petition.condition>`
    predicate).

    Each time a new thread is spawned for a :class:`Petition`, it is saved on a list of
    currently running threads. There is another thread running from the start of the
    :class:`Process` which is the **garbage collector**, whose responsibility is to
    check which threads on that list have finished and remove them when that happens.

    Warning:
        When defining your own :attr:`action <orcha.interfaces.Petition.action>`, take special
        care on what you will be running as any deadlock may block the entire pipeline
        forever (which basically is what deadlocks does). Your thread must be error-free
        or must include a proper error handling on the **server manager object**.

        This also applies when calling :func:`shutdown`, as the processor will wait until
        all threads are done. In case there is any deadlock in there, the processor will
        never end and you will have to manually force finish it (which may cause zombie
        processes or memory leaks).

    .. versionadded:: 0.1.7
        Processor now supports an attribute :attr:`look_ahead <orcha.lib.Processor.look_ahead>`
        which allows defining an amount of items that will be pop-ed from the queue,
        modifying the default behavior of just obtaining a single item.

    .. versionadded:: 0.1.8
        Manager calls to :func:`on_start <orcha.lib.Manager.on_start>` and
        :func:`on_finish <orcha.lib.Manager.on_finish>` are performed in a mutex environment,
        so there is no need to do any kind of extra processing at the
        :func:`condition <orcha.interfaces.Petition.condition>` function. Nevertheless, the
        actual action run there should be minimal as it will block any other process.

    .. versionadded:: 0.1.9
        Processor supports a new attribute
        :attr:`notify_watchdog <orcha.lib.Processor.notify_watchdog>`
        that defines if the processor shall create a background thread that takes care of
        notifying systemd about our status and, if dead, to restart us.

    .. versionchanged:: 0.3.0
        There is no ``notify_watchdog`` attribute, behavior is now leveraged to a pluggable.

    Args:
        queue (multiprocessing.Queue, optional): queue in which new :class:`Message` s are
                                                 expected to be. Defaults to :obj:`None`.
        finishq (multiprocessing.Queue, optional): queue in which signals are expected to be.
                                                   Defaults to :obj:`None`.
        manager (:class:`Manager`, optional): manager object used for synchronization and action
                                              calling. Defaults to :obj:`None`.

        look_ahead (:obj:`int`, optional): amount of items to look ahead when querying the queue.
            Having a value higher than 1 allows the processor to access items further in the queue
            if, for any reason, the next one is not available yet to be executed but the second
            one is (i.e.: if you define priorities based on time, allow the second item to be
            executed before the first one). Take special care with this parameter as this may
            cause starvation in processes.

    Raises:
        ValueError: when no arguments are given and the processor has not been initialized yet.
    """

    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if Processor.__instance__ is None:
            instance = object.__new__(cls)
            instance.__must_init__ = True
            Processor.__instance__ = instance
        return Processor.__instance__

    def __init__(
        self,
        queue: Optional[multiprocessing.Queue] = None,
        finishq: Optional[multiprocessing.Queue] = None,
        manager: Optional[Manager] = None,
        look_ahead: int = 1,
    ):
        if self.__must_init__:
            if queue is None:
                raise ValueError("queue must have a value during first initialization")
            if finishq is None:
                raise ValueError("finish queue must have a value during first initialization")
            if manager is None:
                raise ValueError("manager must have a value during first initialization")

            self._lock = Lock()
            self._queue = queue
            self._finishq = finishq
            self.manager = manager
            self.look_ahead = look_ahead
            self._finished = Event()
            self.running = True

            self._internalq = PriorityQueue()
            self._signals = Queue()
            self._threads: List[Thread] = []
            self._petitions: Dict[Union[int, str], Petition] = {}
            self._gc_event = Event()
            self._process_t = Thread(target=self._process)
            self._internal_t = Thread(target=self._internal_process)
            self._finished_t = Thread(target=self._signal_handler)
            self._signal_t = Thread(target=self._internal_signal_handler)
            self._gc_t = Thread(target=self._gc)
            self._process_t.start()
            self._internal_t.start()
            self._finished_t.start()
            self._signal_t.start()
            self._gc_t.start()
            self.__must_init__ = False

    @property
    def running(self) -> bool:
        """Whether if the current processor is running or not"""
        return not self._finished.is_set()

    @running.setter
    def running(self, v: bool):
        if v:
            self._finished.clear()
        else:
            self._finished.set()

    @property
    def look_ahead(self) -> int:
        """Amount of items to look ahead when querying the queue"""
        return self._look_ahead

    @look_ahead.setter
    def look_ahead(self, v: int):
        with self._lock:
            self._look_ahead = v

    def wait(self, n: Optional[float] = None) -> bool:
        """Waits the specified amount of time (in seconds) or until
        the main process is done (it is, until :attr:`running` returns
        :obj:`False`), the default.

        .. versionadded:: 0.2.3

        Args:
            n (:obj:`float`, optional): time to wait, in seconds. Defaults to :obj:`None`.

        Returns:
            :obj:`bool`: the :attr:`running` value after the given time has passed.
        """
        return self._finished.wait(n)

    def is_running(self, m: Union[Message, int, str]) -> bool:
        """
        Checks if the given message is running or not.

        .. versionchanged:: 0.1.6
           Attribute :attr:`m` now supports a :obj:`str` as ID.

        .. versionadded:: 0.2.2
            Renamed from :func:`exists` to :func:`is_running`.

        Args:
            m (:obj:`Message` | :obj:`int` | :obj:`str`]): the message to check or its
                :attr:`id <orcha.interfaces.Message.id>` (if :obj:`int` or :obj:`str`).

        Returns:
            bool: :obj:`True` if running, :obj:`False` if not.

        Note:
            A message is considered to not exist iff **it's not running**, but can
            be enqueued waiting for its turn.
        """
        return self.manager.is_running(m)

    def enqueue(self, m: Message):
        """Shortcut for::

            processor.queue.put(message)

        Args:
            m (Message): the message to enqueue
        """
        self._queue.put(m)

    def finish(self, m: Union[Message, int, str]):
        """Sets a finish signal for the given message.

        .. versionchanged:: 0.1.6
           Attribute :attr:`m` now supports a :obj:`str` as ID.

        Args:
            m (:obj:`Message` | :obj:`int` | :obj:`str`): the message or its
                :attr:`id <orcha.interfaces.Message.id>` (if :obj:`int` or :obj:`str`).
        """
        if isinstance(m, Message):
            m = m.id

        log.debug("received petition for finish message with ID %s", m)
        self._finishq.put(m)

    def _fatal_error(self, function: str, exception: BaseException):
        log.fatal("unhandled exception at %s: %s", function, exception, exc_info=exception)
        log.fatal("finishing orchestrator...")
        self.running = False
        self.manager.shutdown(errno.EINVAL)

    def _process(self):
        if properties.authkey is not None:
            log.debug("fixing internal digest key")
            multiprocessing.current_process().authkey = properties.authkey
        else:
            log.debug("skipping internal digest key fixing as authkey is not defined")

        try:
            while self.running:
                log.debug("waiting for message...")
                m: Optional[Message] = self._queue.get()
                if m is not None:
                    log.debug('converting message "%s" into a petition', m)
                    # make sure petition 'p' always exists
                    p: Optional[Petition] = None
                    try:
                        p = self.manager.on_message_preconvert(m)
                    except Exception as e:
                        log.critical(
                            'exception when trying to convert message "%s"! No errors '
                            "are expected to happen when creating a petition",
                            m,
                        )
                        log.warning(e)
                        continue
                    if p is not None:
                        log.debug("> %s", p)
                        self.manager.on_petition_create(p)
                        if self.is_running(p.id):
                            log.warning("received message (%s) already running", p)
                            if p.queue is not None:
                                p.communicate(f'message with ID "{p.id}" is already running\n')
                                p.finish(1)
                            continue
                    else:
                        log.debug('message "%s" is invalid, skipping...', m)
                        continue
                else:
                    p = EmptyPetition()
                self._petitions[p.id] = p
                if not p.state.is_in_broken_state:
                    p.state = PetitionState.ENQUEUED
                    self._internalq.put(p)
                else:
                    self._do_signal(p.id)
        except Exception as e:
            self._fatal_error("message processor thread", e)

    def _internal_process(self):
        try:
            while self.running:
                log.debug("waiting for internal petition...")
                empty = False
                items_to_enqueue = []
                log.debug("looking ahead %d items", self.look_ahead)
                for i in range(1, self.look_ahead + 1):
                    p: Petition = self._internalq.get()
                    if not isinstance(p, EmptyPetition):
                        log.debug('adding petition "%s" to list of possible petitions', p)
                        items_to_enqueue.append(p)
                    else:
                        log.debug("received empty petition")
                        empty = True
                        break

                    if i > self._internalq.qsize():
                        break

                for item in items_to_enqueue:
                    log.debug('creating thread for petition "%s"', item)
                    launch_t = Thread(target=self._start, args=(item,))
                    launch_t.start()
                    self._threads.append(launch_t)

                if not empty:
                    self.wait(random.uniform(0.5, 5))
            log.debug("internal process handler finished")

        except Exception as e:
            self._fatal_error("petition processor thread", e)

    def _start(self, p: Petition):
        log.debug('launching petition "%s"', p)

        try:
            healthy = self.manager.start_petition(p)
        except Exception as e:
            log.critical("Unable to start petition %s with error: %s", p, e)
            p.state = PetitionState.BROKEN
            healthy = False

        if not healthy and p.state.is_enqueued:
            log.debug('petition "%s" did not satisfy the condition, re-adding to queue', p)
            self._internalq.put(p)
            self._gc_event.set()
            return

        log.debug('petition "%s" satisfied condition', p)
        try:
            if healthy:
                p.action(p)
        except Exception as e:
            log.warning(
                'unhandled exception while running petition "%s" -> "%s"', p, e, exc_info=True
            )
            p.state = PetitionState.BROKEN
        finally:
            log.debug('petition "%s" finished, triggering callbacks', p)
            self._petitions.pop(p.id, None)

            self.manager.finish_petition(p)

            # set garbage collector flag to cleanup ourselves
            self._gc_event.set()

    def _signal_handler(self):
        if properties.authkey is not None:
            log.debug("fixing internal digest key")
            multiprocessing.current_process().authkey = properties.authkey
        else:
            log.debug("skipping internal digest key fixing as authkey is not defined")

        try:
            while self.running:
                log.debug("waiting for finish message...")
                m = self._finishq.get()
                self._signals.put(m)
        except Exception as e:
            self._fatal_error("signal processor thread", e)

    def _do_signal(self, id: Union[int, str]):
        petition = self._petitions[id]
        finish_t = Thread(target=self._finish, args=(id, petition))
        finish_t.start()
        self._threads.append(finish_t)

    def _internal_signal_handler(self):
        try:
            while self.running:
                log.debug("waiting for internal signal...")
                m = self._signals.get()
                if isinstance(m, Message):
                    m = m.id

                if m is not None:
                    log.debug('received signal petition for message with ID "%s"', m)
                    if m not in self._petitions:
                        log.warning('message with ID "%s" not found or not running!', m)
                        continue

                    self._do_signal(m)
        except Exception as e:
            self._fatal_error("signal handler thread", e)

    def _finish(self, id: Union[str, int], p: Petition):
        try:
            if p.state.is_stopped:
                raise ValueError(
                    "Cannot terminate a petition whose state is either FINISHED, PENDING or BROKEN"
                )

            # if we are called, our state is now CANCELLED
            if p.state.is_in_running_state:
                p.state = PetitionState.CANCELLED
            else:
                raise AttributeError(f"Unknown petition state: {p.state}")

            if not p.terminate():
                raise RuntimeError(f'Failed to finish petition instance "{type(p).__name__}"')

        except Exception as e:
            if p.queue is not None:
                p.communicate(f"Failed to finish petition with ID {p.id}\n")
                p.communicate(f"{e}\n")
        finally:
            self.manager.finish_petition(p)
            if p.queue is not None:
                p.finish()

            self._petitions.pop(id, None)
            self._gc_event.set()

    def _gc(self):
        try:
            while self.running:
                self._gc_event.wait()
                self._gc_event.clear()
                for thread in self._threads:
                    if not thread.is_alive():
                        log.debug('pruning thread "%s"', thread)
                        self._threads.remove(thread)
        except Exception as e:
            self._fatal_error("garbage collector thread", e)

    def shutdown(self):
        """
        Finishes all the internal queues and threads, waiting for any pending requests to
        finish (they are not interrupted by default, unless the signal gets propagated).

        This method must be called when finished all the server operations.
        """
        try:
            log.info("finishing processor")
            self.running = False
            self._queue.put(None)
            self._finishq.put(None)

            log.info("waiting for pending processes...")
            self._process_t.join()
            self._internal_t.join()

            log.info("waiting for pending signals...")
            self._finished_t.join()
            self._signal_t.join()

            log.info("finishing all registered petitions...")
            # we need to "cast" the dictionary to a set so we can alter its size while iterating
            for id in set(self._petitions):
                self._do_signal(id)

            log.info("waiting for pending operations...")
            for thread in self._threads:
                thread.join()

            log.info("waiting for garbage collector...")
            self._gc_event.set()
            self._gc_t.join()

            log.info("finished")
        except Exception as e:
            log.critical("unexpected error during shutdown! -> %s", e, exc_info=True)
            raise


__all__ = ["Processor"]
