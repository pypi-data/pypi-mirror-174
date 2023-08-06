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
:class:`Petition` defines the behavior of the module that calls the service.
This type must be recoverable from a :class:`Message` object, as petitions
cannot be sent from clients to servers and vice versa.
"""
from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum, auto, unique
from functools import total_ordering
from queue import Queue

from typing_extensions import final

from orcha.interfaces.types import Bool
from orcha.utils import nop, nopr
from orcha.utils.cmd import kill_proc_tree

if typing.TYPE_CHECKING:
    from typing import Any, Callable, Optional, Union

    from typing_extensions import Self


@unique
class PetitionState(IntEnum):
    """
    Class that contains the logic for determining the status of a
    petition, allowing to determine if the state is valid. For example, a
    running petition shouldn't be run again; a cancelled petition shouldn't
    be started, etc.

    .. versionadded:: 0.2.2
    """

    PENDING = 0
    """The petition has just been created"""
    ENQUEUED = auto()
    """The petition is already enqueued waiting for running"""
    RUNNING = auto()
    """The petition has been started and it's running"""
    FINISHED = auto()
    """Petition processing has been done"""
    CANCELLED = auto()
    """If the petition has been cancelled before finishing processing"""
    BROKEN = auto()
    """The petition failed to initialize or got an unexpected error while running

    .. versionadded:: 0.2.5
    """
    DONE = auto()
    """The petition is done, no further processing is needed.

    .. versionadded:: 0.3.0
    """

    @property
    def is_enqueued(self) -> bool:
        """Checks if the petition is enqueued"""
        return self == self.ENQUEUED

    @property
    def is_running(self) -> bool:
        """Checks if the petition is running"""
        return self == self.RUNNING

    @property
    def has_finished(self) -> bool:
        """Checks if the petition has finished"""
        return self == self.FINISHED

    @property
    def has_been_cancelled(self) -> bool:
        """Checks if the petition has been cancelled"""
        return self == self.CANCELLED

    @property
    def is_broken(self) -> bool:
        """Checks if the petition is broken"""
        return self == self.BROKEN

    @property
    def is_stopped(self) -> bool:
        """Checks if the petition is stopped"""
        return self in STOPPED_STATES

    @property
    def is_in_running_state(self) -> bool:
        """Checks if the petition is in a running state"""
        return self in RUNNING_STATES

    @property
    def is_in_broken_state(self) -> bool:
        """Checks if the petition is in a broken state"""
        return self in BROKEN_STATES

    @property
    def is_done(self) -> bool:
        """Checks if the petition is done"""
        return self == self.DONE


STOPPED_STATES = {
    PetitionState.PENDING,
    PetitionState.FINISHED,
    PetitionState.BROKEN,
}
"""Set of states in which :class:`petitions <orcha.interfaces.Petition>` are
considered to be stopped, it is, not running or in a pre-running state.

.. versionadded:: 0.2.5
"""

RUNNING_STATES = {
    PetitionState.RUNNING,
    PetitionState.ENQUEUED,
}
"""Set of states in which :class:`petitions <orcha.interfaces.Petition>` are
considered to be running, it is, already enqueued or running.

.. versionadded:: 0.2.5
"""

BROKEN_STATES = {
    PetitionState.BROKEN,
}
"""Set of states in which :class:`petitions <orcha.interfaces.Petition>` are
considered to be broken, it is, failed during execution, start, etc.

.. versionadded:: 0.2.5
"""


@total_ordering
@dataclass
class Petition(ABC):
    """Class that represents a petition that should be executed on the server.
    This class must have the ability to being created from an existing
    :class:`Message`, as this is the only item that can be exchanged during
    inner process communication.

    It is composed by multiple attributes:

     - :attr:`priority` defines the priority of the petition.
     - :attr:`id` is a unique identifier for the petition.
     - :attr:`queue` is a :py:class:`Queue <multiprocessing.Queue>` that can
       be sent across processes.
     - :attr:`action` represents the callable that will be executed.
     - :attr:`condition` is a predicate which defines whether the petition
       can be run or not.
     - :attr:`state` is the internal state of the petition, defined by the
       enum :class:`PetitionState`.

    This class is intended to be a stub so your implementation must inherit
    from this one.

    .. versionchanged:: 0.1.9
        We define our own equality and comparison operators, there is no need
        in subclasses declaring fields as ``compare=False``. It is only checked
        the ID (for equality/inequality tests) and the priority (for comparison
        tests).

    .. versionadded:: 0.2.0
        This class now defines a :func:`terminate` which is abstract and should
        be overridden by all subclasses that inherit from :class:`Petition`. Such
        function allows defining a custom behavior when a finish message is
        received.

        .. warning::
            This is a breaking change - all existing projects should migrate
            their own :class:`Petition` subclasses to the new definition.

    .. versionadded:: 0.2.2
        Petition now have an internal state that is managed by the processor
        that owns it (so the manager also). This internal state is intended to be
        used for deciding if a petition should be run or not. By default, its
        state is :obj:`PENDING <PetitionState.PENDING>`.

    :see: :py:func:`field <dataclasses.field>`
    """

    priority: float = field(init=False)
    """
    Priority of the petition. It is an integer whose value is used for comparing
    across other petitions. The lower the value is, the higher the priority gets.
    Items with the same priority may keep input order, but it is not guaranteed.
    """

    id: Union[int, str] = field(compare=False)
    """
    Unique identifier for this petition. This value must directly be extracted from
    :attr:`Message.id`.

    .. versionchanged:: 0.1.6
       Accept :obj:`str` as unique ID identifier also.
    """

    queue: Optional[Queue] = field(compare=False, repr=False)
    """
    :class:`Queue <multiprocessing.Queue>` used for process communication. Actually,
    this queue is used as a one-sided pipe in which the server puts the messages of
    the :attr:`action` and finishes with a known exit code (i.e.: :obj:`None`, ``int``, ...).

    Warning:
        This queue **must** be a
        `proxy object <https://docs.python.org/3/library/multiprocessing.html#proxy-objects>`_
        which addresses a memory location on a
        :py:class:`Manager <multiprocessing.managers.BaseManager>`. You can decide
        to use your own queue given by :py:mod:`multiprocessing` but it probably won't work.
        It is better to use the exposed manager for obtaining a queue once the client is
        initialized: :attr:`Manager.manager <orcha.lib.manager.Manager.manager>`.

    .. versionchanged:: 0.3.0
        :attr:`queue` can be :obj:`None`.
    """

    action: Callable[[Self], None] = field(compare=False, repr=False)
    """
    The action to be called when the petition is pop from the queue. It is a function with the
    form::

        def action(p: Petition) -> None

    Notice that the action will
    be built on "server side", meaning that this attribute will default to :obj:`None` at the
    beginning (functions cannot be shared across processes).

    As a :class:`Petition` is built from :class:`Message`, use the :attr:`Message.extras` for
    defining how the petition will behave when :attr:`action` is called.

    .. versionchanged:: 0.2.4
        :attr:`action` type hinting was changed from :obj:`NoReturn <typing.NoReturn>` to
        :obj:`None`, as the function does return but no value.

    .. versionchanged:: 0.3.0
        :attr:`action` no longer receives ``cb`` (callback) argument.
    """

    condition: Callable[[Self], Bool] = field(compare=False, repr=False)
    """
    Predicate that decides whether the request should be processed or not. It is a function
    with the form::

        def predicate(p: Petition) -> SupportsBool

    If your petitions do not require any particular condition, you can always define an
    empty predicate which always returns :obj:`True`::

        petition = Petition(..., condition=lambda _: True)

    .. versionchanged:: 0.3.0
        Typing signature for this predicate has changed for returning
        :obj:`orcha.interfaces.SupportsBool`, which allows better customization
        and better integration with the new pluggable interface.
    """

    state: PetitionState = field(compare=False, init=False, default=PetitionState.PENDING)
    """
    Petition's state that indicates current step in the processing queue. Available
    states are defined at :class:`PetitionState` enumerate.
    """

    def communicate(self, message: Any, blocking: bool = True):
        """
        Communicates with the source process by sending a message through the internal queue.

        Args:
            message (any): a valid item that can be put on a :class:`queue.Queue`.
            blocking (:obj:`bool`): whether to block or not while putting the item on the queue.

        Raises:
            queue.Full: if the queue has exceeded its maximum capacity and ``blocking`` is set
                        to :obj:`True`.
            :obj:`AttributeError`: if the :attr:`queue` is :obj:`None`.
        """
        if self.queue is None:
            raise AttributeError(f"Queue is not initialized for petition {type(self).__name__}")

        try:
            self.queue.put(message, block=blocking)
        except ValueError:
            pass

    def communicate_nw(self, message: Any):
        """
        Communicates with the source process by sending a message through the internal queue
        without waiting.

        Args:
            message (any): a valid item that can be put on a :class:`queue.Queue`.

        Raises:
            queue.Full: if the queue has exceeded its maximum capacity.
            :obj:`AttributeError`: if the :attr:`queue` is :obj:`None`.
        """
        if self.queue is None:
            raise AttributeError(f"Queue is not initialized for petition {type(self).__name__}")

        try:
            self.queue.put_nowait(message)
        except ValueError:
            pass

    def finish(self, ret: Optional[int] = None):
        """
        Notifies to the listening process that the corresponding action has finished.

        Args:
            ret (int | None): return code of the operation, if any.

        Raises:
            :obj:`AttributeError`: if the :attr:`queue` is :obj:`None`.
        """
        if self.queue is None:
            raise AttributeError(f"Queue is not initialized for petition {type(self).__name__}")

        try:
            self.queue.put(ret)
        except ValueError:
            pass

    @abstractmethod
    def terminate(self) -> bool:
        """
        Function that is called every time a finish request is received
        for killing the process itself. One can use either the received PID, if any,
        or a saved argument at the running class instance.

        Returns:
            :obj:`bool`: that indicates if the operation has been successful or not.

        .. versionadded:: 0.2.0

        .. versionchanged:: 0.2.2
            This function now has a body which must be called always from child classes.
            Such body ensures petition state is valid and sets the new one, which will
            be :obj:`CANCELLED <PetitionState.CANCELLED>`.

        .. versionchanged:: 0.3.0
            :meth:`terminate` does not require anymore any parameter, is up to the
            developer to define its own behavior.
        """

    def __eq__(self, __o: object) -> bool:
        # ensure we are comparing against our class or a subclass of ours
        if not isinstance(__o, Petition):
            raise NotImplementedError()

        sid = self.id
        oid = __o.id

        # if IDs are not strings, convert them so we can truly compare
        if not isinstance(sid, str):
            sid = str(sid)

        if not isinstance(oid, str):
            oid = str(oid)

        return sid == oid

    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, Petition):
            raise NotImplementedError()

        # we check equality for the priorities
        return self.priority < __o.priority


@final
@dataclass(init=False)
class EmptyPetition(Petition):
    """
    Empty petition which will run always the latest (as its priority is ``inf``).
    This petition is used in :class:`Manager` for indicating that there won't be
    any new petitions after this one, so the :class:`Processor` can shut down.

    Note:
        This class accepts no parameters, and you can use it whenever you want for
        debugging purposes. Notice that it is immutable, which means that no attribute
        can be altered, added or removed once it has been initialized.
    """

    priority = float("inf")
    id = -1
    queue = None
    action = nop
    condition = nopr(True)
    terminate = nopr(True)

    # pylint: disable=super-init-not-called
    def __init__(self):
        ...


@dataclass
class SignalingPetition(Petition):
    """
    :class:`Petition` that finishes the running process by sending a signal (which used
    to be the default).

    It behaves exactly the same as its parent class, the only difference is that a
    signal is issued when a finish message is received.

    One can define which :attr:`signal` to send and whether to also :attr:`kill_parent`
    by issuing the signal to it.

    .. versionadded:: 0.2.0

    .. versionchanged:: 0.2.1
        Attributes do not have a default value, allowing subclasses to have also non-default
        attributes.

    .. versionchanged:: 0.3.0
        :attr:`pid` is now mandatory for finishing on-going petition
    """

    signal: int = field(compare=False)
    """
    The signal number to send to the process when finishing. Notice that the value here
    should be valid within the host architecture the orchestrator is running on.
    """

    kill_parent: bool = field(compare=False)
    """
    Whether to send the specific signal to the parent also (it is, the PID itself, not only
    its children). If unsure, set to :obj:`True`.
    """

    pid: Optional[int] = field(compare=False, init=False, default=None)
    """
    PID of the process to send the signal to. Can change during execution to match the
    actual running process and is :obj:`None` by default, meaning that you **must** set
    the value during :meth:`action` or any related call.

    .. versionadded:: 0.3.0
    """

    def terminate(self) -> bool:
        """Sends the specified signal to the process and/or its parent.

        Raises:
            :obj:`ValueError`: if the :attr:`pid` is :obj:`None`.

        Returns:
            :obj:`bool`: :obj:`True` if all children have been signaled correctly,
                :obj:`False` otherwise.

        .. versionchanged:: 0.3.0
            :meth:`terminate` does not require anymore ``pid`` parameter.
        """
        if self.pid is None:
            raise ValueError(f'Petition of type "{type(self).__name__}" requires a valid PID')

        return kill_proc_tree(self.pid, self.kill_parent, self.signal)


__all__ = [
    "EmptyPetition",
    "Petition",
    "SignalingPetition",
    "PetitionState",
    "STOPPED_STATES",
    "RUNNING_STATES",
    "BROKEN_STATES",
]
