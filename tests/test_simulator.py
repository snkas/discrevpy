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

import unittest
from discrevpy import simulator


class TestSimulator(unittest.TestCase):

    def test_normal(self):

        self.test_normal_counter = 0

        def x(val):
            self.test_normal_counter += val

        self.assertEqual(simulator.event_heap_size(), 0)
        simulator.ready()
        simulator.schedule(100, x, 57)
        simulator.schedule(100, x, 473)
        simulator.schedule(200, x, 88)
        simulator.end(200)
        simulator.run()
        self.assertEqual(self.test_normal_counter, 57 + 473)
        self.assertEqual(simulator.now(), 200)
        self.assertTrue(simulator.is_finished())
        self.assertEqual(simulator.event_heap_size(), 1)
        simulator.reset()
        self.assertEqual(simulator.event_heap_size(), 0)

    def test_normal_just(self):

        self.test_normal_counter = 0

        def x(val):
            self.test_normal_counter += val

        simulator.ready()
        simulator.schedule(100, x, 57)
        simulator.schedule(100, x, 473)
        simulator.schedule(199, x, 88)
        simulator.end(200)
        simulator.run()
        self.assertEqual(self.test_normal_counter, 57 + 473 + 88)
        self.assertEqual(simulator.now(), 200)
        self.assertTrue(simulator.is_finished())
        self.assertEqual(simulator.event_heap_size(), 0)
        simulator.reset()
        self.assertEqual(simulator.event_heap_size(), 0)

    def test_normal_not(self):

        self.test_normal_counter = 0

        def x(val):
            self.test_normal_counter -= val

        simulator.ready()
        simulator.schedule(100, x, 57)
        simulator.schedule(153, x, 245)
        simulator.schedule(199, x, 88)
        simulator.end(156)
        simulator.run()
        self.assertEqual(self.test_normal_counter, - 57 - 245)
        self.assertEqual(simulator.now(), 156)
        self.assertTrue(simulator.is_finished())
        self.assertEqual(simulator.event_heap_size(), 1)
        simulator.reset()
        self.assertEqual(simulator.event_heap_size(), 0)

    def test_end_one(self):

        self.test_end_one_counter = 0

        def x(val):
            self.test_end_one_counter += val

        simulator.ready()
        simulator.schedule(10, x, 57)
        simulator.end(100)
        simulator.run()
        self.assertEqual(self.test_end_one_counter, 57)
        self.assertEqual(simulator.now(), 100)
        self.assertTrue(simulator.is_finished())
        simulator.reset()

    def test_end_override(self):

        self.test_end_two_override_counter = 22

        def x(val):
            self.test_end_two_override_counter += val

        simulator.ready()
        simulator.schedule(57, x, 67)
        simulator.end(100)
        simulator.end(57)
        simulator.end(100)
        simulator.run()
        self.assertEqual(self.test_end_two_override_counter, 22)
        self.assertEqual(simulator.now(), 57)
        self.assertTrue(simulator.is_finished())
        simulator.reset()

    def test_end_in_event(self):

        self.test_end_in_event_counter = 22

        def x(val):
            self.test_end_in_event_counter += val

        def y():
            simulator.end(5)

        simulator.ready()
        simulator.schedule(60, x, 22)
        simulator.schedule(70, y)
        simulator.schedule(70, x, 3)
        simulator.schedule(71, y)
        simulator.schedule(74, x, 5)
        simulator.schedule(75, x, 22)
        simulator.schedule(76, x, 22)
        simulator.schedule(888, x, 22)
        simulator.schedule(999, x, 22)
        simulator.schedule(8953, x, 22)
        simulator.end(1000)
        simulator.run()
        self.assertEqual(self.test_end_in_event_counter, 22 + 22 + 3 + 5)
        self.assertEqual(simulator.now(), 75)
        self.assertTrue(simulator.is_finished())
        self.assertEqual(simulator.event_heap_size(), 5)
        simulator.reset()

    def test_end_in_same_event(self):

        self.test_end_in_same_event_counter = 0

        def x():
            self.test_end_in_same_event_counter += 100

        def y():
            self.test_end_in_same_event_counter += 3

        def z():
            self.test_end_in_same_event_counter += 5

            self.assertFalse(simulator.is_init())
            self.assertFalse(simulator.is_ready())
            self.assertTrue(simulator.is_running())
            self.assertFalse(simulator.is_finished())

            simulator.end()  # End after this event has been executed

            self.assertFalse(simulator.is_init())
            self.assertFalse(simulator.is_ready())
            self.assertTrue(simulator.is_running())
            self.assertFalse(simulator.is_finished())

        simulator.ready()
        simulator.schedule_with_priority(70, 5, x)
        simulator.schedule_with_priority(70, 5, x)
        simulator.schedule_with_priority(70, 20, y)
        simulator.schedule_with_priority(70, 10, z)
        simulator.run()
        self.assertEqual(self.test_end_in_same_event_counter, 100 + 100 + 5)
        self.assertEqual(simulator.now(), 70)
        self.assertTrue(simulator.is_finished())
        self.assertEqual(simulator.event_heap_size(), 1)
        simulator.reset()
        self.assertTrue(simulator.is_init())
        self.assertFalse(simulator.is_ready())
        self.assertFalse(simulator.is_running())
        self.assertFalse(simulator.is_finished())
        self.assertEqual(simulator.now(), 0)
        self.assertEqual(simulator.event_heap_size(), 0)

    def test_stage_transitions(self):

        self.assertTrue(simulator.is_init())
        self.assertFalse(simulator.is_ready())
        self.assertFalse(simulator.is_running())
        self.assertFalse(simulator.is_finished())

        simulator.ready()

        self.assertFalse(simulator.is_init())
        self.assertTrue(simulator.is_ready())
        self.assertFalse(simulator.is_running())
        self.assertFalse(simulator.is_finished())

        def check_running():
            self.assertFalse(simulator.is_init())
            self.assertFalse(simulator.is_ready())
            self.assertTrue(simulator.is_running())
            self.assertFalse(simulator.is_finished())
            self.assertEqual(simulator.now(), 0)

        simulator.schedule(0, check_running)
        simulator.end(100000)
        simulator.run()
        self.assertEqual(simulator.now(), 100000)

        self.assertFalse(simulator.is_init())
        self.assertFalse(simulator.is_ready())
        self.assertFalse(simulator.is_running())
        self.assertTrue(simulator.is_finished())

        simulator.reset()

        self.assertTrue(simulator.is_init())
        self.assertFalse(simulator.is_ready())
        self.assertFalse(simulator.is_running())
        self.assertFalse(simulator.is_finished())

    def test_run_empty_with_end_time(self):
        simulator.ready()
        self.assertEqual(simulator.now(), 0)
        self.assertFalse(simulator.is_finished())
        simulator.end(68483)
        simulator.run()
        self.assertEqual(simulator.now(), 68483)
        self.assertTrue(simulator.is_finished())
        simulator.reset()

    def test_run_empty_no_end_time(self):
        simulator.ready()
        self.assertEqual(simulator.now(), 0)
        self.assertFalse(simulator.is_finished())
        simulator.run()
        self.assertEqual(simulator.now(), 0)
        self.assertTrue(simulator.is_finished())
        simulator.reset()

    def test_invalid_state_errors(self):

        # Invalid reset()
        try:
            simulator.ready()
            simulator.reset()
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Reset can only be performed when the state is FINISHED (current: READY)")
            simulator.run()
            simulator.reset()

        # Invalid run()
        try:
            simulator.run()
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Run can only be started when the state is READY (current: INIT)")
            simulator.ready()
            simulator.run()
            simulator.reset()

        # Invalid ready()
        try:
            simulator.ready()
            simulator.ready()
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Can only become READY when the simulator is INIT (current: READY)")
            simulator.run()
            simulator.reset()

        # Invalid schedule (not in READY or RUNNING state)
        try:
            def x():
                pass
            simulator.schedule(10, x)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Scheduling can only be done when the state is READY or RUNNING (current: INIT)")

        # Invalid end() in INIT state
        try:
            simulator.end()
            self.fail()
        except ValueError as e:
            self.assertEqual(
                str(e),
                "Scheduling end can only be done when the state is READY or RUNNING (current: INIT)"
            )

        # Invalid end() in FINISHED state
        try:
            simulator.ready()
            simulator.run()
            simulator.end()
            self.fail()
        except ValueError as e:
            self.assertEqual(
                str(e),
                "Scheduling end can only be done when the state is READY or RUNNING (current: FINISHED)"
            )
            simulator.reset()

    def test_invalid_schedule_errors(self):

        # Schedule delay is not an integer
        try:
            def x():
                pass
            simulator.ready()
            simulator.schedule("abc", x)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Delay must be an integer")
            simulator.run()
            simulator.reset()

        # Schedule delay is a negative integer
        try:
            def x():
                pass
            simulator.ready()
            simulator.schedule(-10, x)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Delay must be non-negative: -10")
            simulator.run()
            simulator.reset()

        # Callback is not a method or function
        try:
            simulator.ready()
            simulator.schedule(5, 25)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Callback must be a function or a method")
            simulator.run()
            simulator.reset()

        # Priority is not an integer
        try:
            def x():
                pass
            simulator.ready()
            simulator.schedule_with_priority(10, "abc", x)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Priority must be an integer")
            simulator.run()
            simulator.reset()

    def test_end_errors(self):

        # End delay is not an integer
        try:
            simulator.ready()
            simulator.end(6.7)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "End delay must be an integer")
            simulator.run()
            simulator.reset()

        # End delay is a negative integer
        try:
            simulator.ready()
            simulator.end(-10)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "End delay must be non-negative")
            simulator.end(100)
            simulator.run()
            simulator.reset()

        # Zero end delay (I)
        try:
            simulator.ready()
            simulator.end()
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Cannot schedule end with zero delay in READY state")
            simulator.run()
            simulator.reset()

        # Zero end delay (II)
        try:
            simulator.ready()
            simulator.end(0)
            self.fail()
        except ValueError as e:
            self.assertEqual(str(e), "Cannot schedule end with zero delay in READY state")
            simulator.run()
            simulator.reset()
