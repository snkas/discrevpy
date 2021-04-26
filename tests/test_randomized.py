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
import random


def random_schedule_test(
        test_instance,
        seed,
        max_time,
        num_events,
        min_priority,
        max_priority
):

    result = []

    def x(val):
        result.append((simulator.now(), val))

    random.seed(seed)
    simulator.ready()
    expectation = []
    for i in range(num_events):
        t = random.randint(0, max_time)
        p = random.randint(min_priority, max_priority)
        v = random.randint(-50000, 100000)
        simulator.schedule_with_priority(t, p, x, v)
        expectation.append((t, p, i, v))
    expectation = sorted(expectation)
    expectation = list(map(lambda a: (a[0], a[3]), expectation))
    simulator.run()
    test_instance.assertEqual(result, expectation)
    simulator.reset()


class TestRandomized(unittest.TestCase):

    def test_randomized(self):
        random.seed(8849866351611827)
        seeds = []
        for i in range(5):
            seeds.append(random.randint(-1000000, 1000000))
        for seed in seeds:
            random_schedule_test(self, seed, 0, 1000, 0, 0)       # One time moment, all the same priority (0)
            random_schedule_test(self, seed, 0, 1000, -10, 10)    # One time moment, varying priority [-10, 10]
            random_schedule_test(self, seed, 1, 1000, 0, 0)       # Two time moments, all the same priority (0)
            random_schedule_test(self, seed, 1, 1000, -100, -10)  # Two time moments, varying priority [-100, -10]
            random_schedule_test(self, seed, 2, 1000, 0, 0)       # Three time moments, all the same priority (0)
            random_schedule_test(self, seed, 2, 1000, 65, 3662)   # Three time moments, varying priority [65, 3662]
            random_schedule_test(self, seed, 5, 1000, 66, 66)     # Six time moments, all the same priority (66)
            random_schedule_test(self, seed, 5, 1000, -10, 66)    # Six time moments, varying priority [-10, 66]
            random_schedule_test(self, seed, 100, 1000, -7, -7)   # 101 time moments, all the same priority (-7)
            random_schedule_test(self, seed, 100, 1000, 0, 10)    # 101 time moments, varying priority [0, 10]
