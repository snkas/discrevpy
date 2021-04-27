# The MIT License (MIT)
#
# Copyright (c) 2021 snkas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The discrevpy module defines a global minimalist discrete event simulator.
In simplest terms: it maintains an event queue of callbacks
ordered by their scheduled discrete simulation time.
"""

import heapq
from enum import Enum
from typing import Union
from types import FunctionType, MethodType, LambdaType, BuiltinFunctionType, BuiltinMethodType


class Simulator:
    """
    Discrete event simulator class.
    """

    class _State(Enum):
        """
        Enumeration for the state of the simulator.
        """
        INIT = 1        # Initialized
        READY = 2       # Ready (initial events can be scheduled)
        RUNNING = 3     # Run is in progress (events can be scheduled during)
        FINISHED = 4    # Run has finished

    def __init__(self) -> None:
        """
        Initializes a Simulator instance.
        """

        self.__state: Simulator._State = Simulator._State.INIT
        self.__now: int = 0
        self.__event_id: int = 0
        # Heap of 6-tuples: (time, priority, event_id, callback, args, kwargs)
        self.__event_heap: list = []
        self.__end_time: Union[int, None] = None

    def ready(self) -> None:
        """
        Ready the simulator such that initial events can be scheduled.
        """

        # Simulator must be in initialized state
        if self.__state != Simulator._State.INIT:
            raise ValueError(
                "Can only become READY when the simulator is INIT "
                "(current: " + str(self.__state.name) + ")"
            )

        # Proceed to ready state
        self.__state = Simulator._State.READY

    def end(self, delay: int = 0) -> None:
        """
        Set when the simulator should end even if there are still
        events in the event heap.

        If the delay is zero (or if no delay argument is provided)
        the current event will be the last event executed if the
        simulator is RUNNING. Zero delay is not permitted when the
        simulator is in READY state.

        If there are multiple end() calls, the end() call resulting in
        the earliest end time will be the end time. As such, an end()
        call cannot be undone.

        :param delay:    (Optional; default: 0)
                         Delay from current simulation time (now) to end the simulation
        """

        # Simulator must be in either ready or running state
        if self.__state != Simulator._State.READY and self.__state != Simulator._State.RUNNING:
            raise ValueError(
                "Scheduling end can only be done when the state is READY or RUNNING "
                "(current: " + str(self.__state.name) + ")"
            )

        # The end delay must be an integer
        if not isinstance(delay, int):
            raise ValueError("End delay must be an integer")

        # The end delay must be non-negative
        if delay < 0:
            raise ValueError("End delay must be non-negative")

        # Zero delay end in READY state is not permitted
        if self.__state == Simulator._State.READY and delay == 0:
            raise ValueError("Cannot schedule end with zero delay in READY state")

        # Set the end time
        if self.__end_time is None:

            # If there is not yet an end time, it is directly set
            self.__end_time = self.__now + delay

        else:

            # If there is already an end time, the new end time is the minimum
            # of the current time plus the delay specified in this function and the
            # existing end time
            self.__end_time = min(
                self.__end_time,
                self.__now + delay
            )

    def schedule(
            self,
            delay: int,
            callback: Union[
                FunctionType,
                MethodType,
                LambdaType,
                BuiltinFunctionType,
                BuiltinMethodType
            ],
            *args,
            **kwargs
    ) -> None:
        """
        Schedule an event in the simulation with default priority (0).

        :param delay:       Delay from current simulation time (now)
        :param callback:    Callback: it must be a function or method
        :param args:        (Optional) Positional arguments passed to the callback
        :param kwargs:      (Optional) Keyword arguments passed to the callback
        """
        self.schedule_with_priority(delay, 0, callback, *args, **kwargs)

    def schedule_with_priority(
            self,
            delay: int,
            priority: int,
            callback: Union[
                FunctionType,
                MethodType,
                LambdaType,
                BuiltinFunctionType,
                BuiltinMethodType
            ],
            *args,
            **kwargs
    ) -> None:
        """
        Schedule an event in the simulation with a certain priority.

        If there are multiple events in one time moment, the priority determines which goes first.
        The lower the priority, the earlier it is executed in its time moment. If the priority of
        two events is equal, the final arbitration is on which event was scheduled first.

        :param delay:       Delay from current simulation time (now)
        :param priority:    Priority
        :param callback:    Callback: it must be a function or method
        :param args:        (Optional) Positional arguments passed to the callback
        :param kwargs:      (Optional) Keyword arguments passed to the callback
        """

        # Simulator must be in either ready or running state
        if self.__state != Simulator._State.READY and self.__state != Simulator._State.RUNNING:
            raise ValueError(
                "Scheduling can only be done when the state is READY or RUNNING "
                "(current: " + str(self.__state.name) + ")"
            )

        # The delay must be an integer
        if not isinstance(delay, int):
            raise ValueError("Delay must be an integer")

        # The callback must be either a function or a method
        # Note: LambdaType equals FunctionType according to documentation
        # Note: BuiltinMethodType equals BuiltinFunctionType according to documentation
        if (
                not isinstance(callback, FunctionType) and
                not isinstance(callback, MethodType) and
                not isinstance(callback, LambdaType) and
                not isinstance(callback, BuiltinFunctionType) and
                not isinstance(callback, BuiltinMethodType)
        ):
            raise ValueError("Callback must be a function or a method")

        # The priority must be an integer
        if not isinstance(priority, int):
            raise ValueError("Priority must be an integer")

        # Events can only be scheduled in the current time moment (now) or later
        if delay < 0:
            raise ValueError("Delay must be non-negative: %d" % delay)

        # Insert into the event heap
        # (event id is incremented such that it is unique for every event)
        heapq.heappush(
            self.__event_heap,
            (self.__now + delay, priority, self.__event_id, callback, args, kwargs)
        )
        self.__event_id += 1

    def run(self) -> None:
        """
        Run the simulation.

        If there is an end time (specified via end()), the simulation will
        end at that time moment. Else, if there is NO end time specified, the
        simulation will run until there are no more events.
        """

        # Simulator must be in ready state
        if self.__state != Simulator._State.READY:
            raise ValueError(
                "Run can only be started when the state is READY "
                "(current: " + str(self.__state.name) + ")"
            )

        # Now it is running
        self.__state = Simulator._State.RUNNING

        # Event loop
        next_event = None if len(self.__event_heap) == 0 else self.__event_heap[0]  # Peek
        while (
                next_event is not None
                and (self.__end_time is None or next_event[0] < self.__end_time)
        ):
            heapq.heappop(self.__event_heap)
            self.__now = next_event[0]
            next_event[3](*next_event[4], **next_event[5])
            next_event = None if len(self.__event_heap) == 0 else self.__event_heap[0]  # Peek

        # Finish
        if self.__end_time is not None:
            self.__now = self.__end_time
        self.__state = Simulator._State.FINISHED

    def reset(self) -> None:
        """
        Reset the simulator such that it can be run again.
        This means current time (now) is set to 0, the event heap
        is emptied and any end time is unset.
        """

        # Simulator must be in finished state
        if self.__state != Simulator._State.FINISHED:
            raise ValueError(
                "Reset can only be performed when the state is FINISHED "
                "(current: " + str(self.__state.name) + ")"
            )

        # Reset all internal variables
        self.__state = Simulator._State.INIT
        self.__now = 0
        self.__event_id = 0
        # Heap of 6-tuples: (time, priority, event_id, callback, args, kwargs)
        self.__event_heap = []
        self.__end_time = None

    def now(self) -> int:
        """
        Retrieve current simulation time. Before the simulation is run, this will return 0.
        After the simulation is run, it will return the time of the last executed event if there
        was no end time, else it will return the end time.

        :return: Current simulation time (int)
        """
        return self.__now

    def is_init(self) -> bool:
        """
        Check whether the simulator is initialized.
        When the simulator is INIT, it is NOT possible to schedule events.
        The simulator can be put into READY state by calling ready().

        :return: True iff the simulator is INIT (bool)
        """
        return self.__state == Simulator._State.INIT

    def is_ready(self) -> bool:
        """
        Check whether the simulator is ready.
        When the simulator is READY, it is possible to schedule events.
        The simulator can be put into RUNNING state by calling run().

        :return: True iff the simulator is READY (bool)
        """
        return self.__state == Simulator._State.READY

    def is_running(self) -> bool:
        """
        Check whether the simulator is currently running.
        When the simulator is RUNNING, it is possible to schedule events.
        After the run ends the simulator becomes FINISHED.

        :return: True iff the simulator is RUNNING (bool)
        """
        return self.__state == Simulator._State.RUNNING

    def is_finished(self) -> bool:
        """
        Check whether the simulator has been run and is finished.
        When the simulator is FINISHED, it is NOT possible to schedule events.
        The simulator can be put into INIT state by calling reset().

        :return: True iff the simulator is FINISHED (bool)
        """
        return self.__state == Simulator._State.FINISHED

    def event_heap_size(self) -> int:
        """
        Retrieve the current size of the event heap.

        If the simulator is FINISHED and the run ended
        due to an end time having been set (via end()),
        the event heap can still have events in it.
        In INIT state, the event heap size is always zero.

        :return: Number of events in the event heap (int)
        """
        return len(self.__event_heap)


# Single global simulator
simulator: Simulator = Simulator()
