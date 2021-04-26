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


class TestCallback(unittest.TestCase):

    def test_args_ref_object(self):
        simulator.ready()

        def x(v):
            self.assertEqual(v[4], 789)

        z = {
            4: 99
        }
        val = (z,)
        simulator.schedule(0, x, *val)
        z[4] = 789  # This dictionary was passed as positional argument, so this *is* still referred to
        simulator.run()
        simulator.reset()

    def test_kwargs_ref_object(self):
        simulator.ready()

        def x(v=(10, 33, 10, 3, 66)):
            self.assertEqual(v[4], 123)

        z = {
            4: 99
        }
        val = {
            "v": z
        }
        simulator.schedule(0, x, **val)
        z[4] = 123  # This dictionary was passed as keyword argument, so this *is* still referred to
        simulator.run()
        simulator.reset()

    def test_zero_arguments(self):
        self.test_zero_arguments_info = []

        def something():
            self.test_zero_arguments_info.append(simulator.now())

        simulator.ready()
        simulator.schedule(0, something)
        simulator.schedule(15, something)
        simulator.schedule(200, something)
        simulator.schedule(45, something)
        simulator.schedule(3, something)
        simulator.schedule(5747, something)
        simulator.schedule(200, something)
        simulator.schedule(0, something)
        simulator.schedule(577394743, something)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_zero_arguments_info, [0, 0, 3, 15, 45, 200, 200, 5747, 577394743])

    def test_one_argument(self):
        self.test_one_argument_info = []

        def something(arg1):
            self.test_one_argument_info.append((simulator.now(), arg1))

        simulator.ready()
        simulator.schedule(0, something, 285)
        simulator.schedule(15, something, "abc")
        simulator.schedule(200, something, 2894242)
        simulator.schedule(45, something, -289424)
        simulator.schedule(3, something, "xyz")
        simulator.schedule(5747, something, 0)
        simulator.schedule(200, something, -1)
        simulator.schedule_with_priority(0, -100, something, 1)
        simulator.schedule(577394743, something, 1902892859)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_one_argument_info, [
            (0, 1),
            (0, 285),
            (3, "xyz"),
            (15, "abc"),
            (45, -289424),
            (200, 2894242),
            (200, -1),
            (5747, 0),
            (577394743, 1902892859)
        ])

    def test_many_arguments(self):
        self.test_many_arguments_info = []

        def something(arg1, arg2, arg3="def", arg4=2384):
            self.test_many_arguments_info.append((simulator.now(), arg1, arg2, arg3, arg4))

        simulator.ready()
        simulator.schedule(0, something, 285, 92948)
        simulator.schedule(15, something, "abc", "xyz", arg3=88)
        simulator.schedule(200, something, 2894242, 462626, arg4=8282)
        simulator.schedule(45, something, -289424, 928295, arg4=33, arg3=11)
        # 3rd/4th positional argument used for known arguments
        simulator.schedule(3, something, "xyz", 82835, 99, 88)
        # 3rd positional argument used for known argument
        simulator.schedule(5747, something, 0, "test", "here")
        simulator.schedule(200, something, -1, "abc")
        simulator.schedule_with_priority(0, -100, something, "abc", 28825)
        simulator.schedule(577394743, something, 1902892859, 8252852985)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_many_arguments_info, [
            (0, "abc", 28825, "def", 2384),
            (0, 285, 92948, "def", 2384),
            (3, "xyz", 82835, 99, 88),
            (15, "abc", "xyz", 88, 2384),
            (45, -289424, 928295, 11, 33),
            (200, 2894242, 462626, "def", 8282),
            (200, -1, "abc", "def", 2384),
            (5747, 0, "test", "here", 2384),
            (577394743, 1902892859, 8252852985, "def", 2384)
        ])

    def test_function_in_function(self):
        self.test_function_in_function_info = []

        def something(value, xyz):
            def x(v):
                self.test_function_in_function_info.append((simulator.now(), xyz, v))
            simulator.schedule(1000, x, value)

        simulator.ready()
        something("Here!", 36362)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_function_in_function_info, [(1000, 36362, "Here!")])

    def test_with_builtin_method(self):

        self.test_with_builtin_method_info = []

        simulator.ready()
        simulator.schedule(100, self.test_with_builtin_method_info.append, 566)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_with_builtin_method_info, [566])

    def test_with_builtin_function(self):

        class X:
            def __init__(self, init_val):
                self.__val = init_val

            def __len__(self):
                self.__val += 7834
                return 1

            def get_val(self):
                return self.__val

        obj = X(40000)
        self.assertEqual(obj.get_val(), 40000)
        simulator.ready()
        simulator.schedule(0, len, obj)
        simulator.schedule(100, len, obj)
        simulator.schedule(1200, len, obj)
        simulator.schedule(34895829589258925256226, len, obj)
        simulator.run()
        simulator.reset()
        self.assertEqual(obj.get_val(), 40000 + 4 * 7834)

    def test_with_lambda_function(self):

        self.test_with_lambda_function_info = []

        def something(val1, val2):
            self.test_with_lambda_function_info.append(val1 + val2)
            self.assertEqual(val1, 28425)
            self.assertEqual(val2, 566)
            return 400

        simulator.ready()
        simulator.schedule(100, lambda x: x + something(28425, x), 566)
        simulator.run()
        simulator.reset()

        self.assertEqual(self.test_with_lambda_function_info, [(28425 + 566)])
