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


class TestExamples(unittest.TestCase):

    def test_readme(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value " + str(value))

        simulator.ready()
        simulator.schedule(44, something, "ABC")
        simulator.schedule(967, something, "XYZ")
        simulator.end(10000)
        simulator.run()
        simulator.reset()

    def test_example_use_case(self):

        class Node:

            def __init__(self, node_id, forward_table, all_nodes):
                self.__node_id = node_id
                self.__forward_counter = 0
                self.__forward_table = forward_table
                self.__all_nodes = all_nodes  # Reference to list of all nodes

            def receive(self, message):
                if message["dst_node_id"] == self.__node_id:
                    print("t=%d: node %d received message with content '%s'" % (
                        simulator.now(),
                        self.__node_id,
                        message["content"]
                    ))
                else:
                    (next_hop, travel_duration) = self.__forward_table[message["dst_node_id"]]
                    simulator.schedule(travel_duration, self.__all_nodes[next_hop].receive, message)
                    self.__forward_counter += 1
                    print("t=%d: node %d forward message %s to node %d" % (
                        simulator.now(),
                        self.__node_id,
                        str(message),
                        next_hop
                    ))

            def get_forward_counter(self):
                return self.__forward_counter

        def main():

            # Instantiate state (the nodes)
            nodes = []
            node0 = Node(0, {1: (1, 204), 2: (2, 222867)}, nodes)
            node1 = Node(1, {0: (0, 204), 2: (0, 204)}, nodes)
            node2 = Node(2, {0: (0, 222867), 1: (0, 222867)}, nodes)
            nodes.append(node0)
            nodes.append(node1)
            nodes.append(node2)

            # Setup and run simulator
            simulator.ready()
            message = {
                "dst_node_id": 2,
                "content": "Hello world!"
            }
            simulator.schedule(100, nodes[1].receive, message)
            simulator.run()
            simulator.reset()

            # Show results
            print("Node 0 forward counter: %d" % node0.get_forward_counter())
            print("Node 1 forward counter: %d" % node1.get_forward_counter())
            print("Node 2 forward counter: %d" % node2.get_forward_counter())

        main()

    def test_schedule_event_without_callback_arguments(self):
        def something():
            print("t=" + str(simulator.now()) + ": something() was called")

        simulator.ready()
        simulator.schedule(100, something)
        simulator.run()
        simulator.reset()

    def test_schedule_event_with_one_callback_argument(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

        simulator.ready()
        simulator.schedule(100, something, "ABC")
        simulator.run()
        simulator.reset()

    def test_schedule_event_with_many_callback_arguments(self):
        def something(val1, val2, abc3, xyz=28):
            print(
                "t=" + str(simulator.now()) + ": something() with: val1="
                + str(val1) + ", val2=" + str(val2) + ", abc3=" + str(abc3) + ", xyz=" + str(xyz)
            )

        simulator.ready()
        simulator.schedule(0, something, "ABC", 1, 4, xyz=83)
        simulator.schedule(77, something, 363, "here", 4)
        simulator.run()
        simulator.reset()

    def test_set_end_time(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

        simulator.ready()
        simulator.schedule(100, something, "ABC")
        simulator.schedule(120, something, "DEF")
        simulator.schedule(160, something, "GHI")
        # End time is 160, meaning that only events scheduled
        # for t in [0, 160) are executed (thus excluding t = 160)
        simulator.end(160)
        simulator.run()
        simulator.reset()

    def test_end_within_event_while_running(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

        def we_are_done(value):
            print("t=" + str(simulator.now()) + ": we_are_done() with value: " + str(value))
            simulator.end()

        simulator.ready()
        simulator.schedule(100, something, "ABC")
        simulator.schedule(120, something, "DEF")
        simulator.schedule(140, we_are_done, "XYZ")
        simulator.schedule(160, something, "TEST")
        simulator.schedule(700, something, "GHI")
        simulator.end(1000)
        simulator.run()
        print("End time: " + str(simulator.now()))
        simulator.reset()

    def test_schedule_another_event_in_callback(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value: " + str(value))
            simulator.schedule(200, something, "XYZ")  # 100 time units in the future from now

        simulator.ready()
        simulator.schedule(200, something, "ABC")
        simulator.end(1001)
        simulator.run()
        simulator.reset()

    def test_schedule_multiple_events_in_same_time_ordered(self):
        def something(value):
            print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

        simulator.ready()
        simulator.schedule_with_priority(100, 77, something, "XYZ")  # Priority of 77
        simulator.schedule_with_priority(100, 44, something, "ABC")  # Priority of 44
        simulator.run()
        simulator.reset()

    def test_schedule_event_with_callback_an_instance_method(self):
        class Example:

            def __init__(self, x):
                self.x = x

            def something(self, value):
                print("t=" + str(simulator.now()) + ": instance of class Example (x=" + str(self.x)
                      + ") something() with value: " + str(value))

        abc = Example("Test")

        simulator.ready()
        simulator.schedule(55, abc.something, "ABCDEF")
        simulator.run()
        simulator.reset()

    def test_inspecting_the_event_heap(self):
        print("")

        def something():
            print("t=" + str(simulator.now()) + ": something() was called")
            print(simulator._Simulator__event_heap)

        simulator.ready()
        simulator.schedule(100, something)
        simulator.schedule(106, something)
        simulator.schedule(107, something)
        print(simulator._Simulator__event_heap)
        simulator.run()
        simulator.reset()

    def test_4x100m_relay(self):

        def relay_finished():
            print("Last athlete finished: 4x100m relay in %.3gs" % (simulator.now() / 1e9))

        class Athlete:
            def __init__(self, idx, athletes, speed_m_per_s):
                self.idx = idx
                self.athletes = athletes
                self.speed_m_per_s = speed_m_per_s

            def receive_stick_and_run(self):
                print("Athlete %d receives stick and starts run at t=%.3gs" % (self.idx, simulator.now() / 1e9))
                if self.idx != len(self.athletes) - 1:
                    simulator.schedule(
                        int(100.0 / self.speed_m_per_s * 1e9),
                        self.athletes[self.idx + 1].receive_stick_and_run
                    )
                else:
                    simulator.schedule(
                        int(100.0 / self.speed_m_per_s * 1e9),
                        relay_finished
                    )

        athletes = []
        athletes.append(Athlete(0, athletes, 10.2))  # Nesta Carter
        athletes.append(Athlete(1, athletes, 10.1))  # Michael Frater
        athletes.append(Athlete(2, athletes, 10.3))  # Yohan Blake
        athletes.append(Athlete(3, athletes, 10.4))  # Usain Bolt
        # All Athlete instances will now have a complete athletes list
        # because Python objects are passed by reference

        simulator.ready()
        simulator.schedule(0, athletes[0].receive_stick_and_run)
        print("Simulating a 4x100m relay")
        simulator.run()
        simulator.reset()
