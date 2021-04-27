Memory usage
============

Base sizes for each event
-------------------------

*Note: values below are from a 64-bit system using Python 3.7*

Every callback event is a tuple of 6 entries. A base tuple object is 56 byte.
Object references in Python are 8 byte each, so each tuple is ``56 + 6 * 8 =`` 104 byte in total.

The objects that each of the entries refers to are the following:

* *time* : integer
* *priority* : integer
* *event_id* : integer
* *callback* : method or function
* *args* : tuple
* *kwargs* : dict

Integers are variable in size. For 0, the size is 24 byte.
For relatively small numbers (e.g., 1) the size is 28 byte.
Python maintains a pool to prevent excessive allocation of
commonly used immutable objects.

An empty tuple is 56 byte and a N-item tuples is ``56 + N * 8`` byte.

Some preliminary measurements indicate that a function is 144 byte and a method is 72 byte.

An empty or small number of key-values dict is 248 byte.
The more key-values are added, the larger it becomes.


Example case analysis
---------------------

Below is an analysis of the memory size it allocates for every event
assuming the callback has 2 positional integer arguments:

.. code-block:: text

    Origin           Size (byte)

    main tuple       56 + 6 * 8   (always)
    time (int)       28           (assuming time is not in integer pool)
    priority (int)   0            (assuming priority is 0, so in the integer pool)
    event_id (int)   28           (assuming event_id is not in integer pool)
    callback         0            (function or method is generally re-used)
    args (tuple)     56 + 2 * 8   (two positional arguments)
    args[0] (int)    28           (assuming not in integer pool)
    args[1] (int)    28           (assuming not in integer pool)
    kwargs (dict)    248          (always (minimum))
                     ---

    Total:           536

It can be verified with the following test script (requires ``python3 -m pip install guppy3``):

.. code-block:: python

    import unittest
    import random
    from guppy import hpy
    from discrevpy import simulator

    class TestMemory(unittest.TestCase):

        def test_memory_size(self):

            def x(a, b):
                pass

            simulator.ready()
            random.seed(29106970)
            for i in range(1000000):
                v1 = random.randint(0, 1000000000)
                v2 = random.randint(0, 1000000000)
                t = random.randint(0, 1000000000)
                simulator.schedule(t, x, v1, v2)
            print(hpy().heap())
            simulator.run()
            simulator.reset()

... and then running it using: ``python3 -m pytest -s -k test_memory_size``
