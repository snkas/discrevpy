Examples
========

.. toctree::
   :maxdepth: 2
   :hidden:

No callback arguments
---------------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

    def something():
        print("t=" + str(simulator.now()) + ": something() was called")

    simulator.ready()
    simulator.schedule(100, something)
    simulator.run()
    simulator.reset()

**Output:**

.. code-block:: text

    t=100: something() was called


One callback argument
---------------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

    def something(value):
        print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

    simulator.ready()
    simulator.schedule(100, something, "ABC")
    simulator.run()
    simulator.reset()

**Output:**

.. code-block:: text

    t=100: something() with value: ABC


Many callback arguments
-----------------------
**Code:**

.. code-block:: python

    from discrevpy import simulator

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

**Output:**

.. code-block:: text

    t=0: something() with: val1=ABC, val2=1, abc3=4, xyz=83
    t=77: something() with: val1=363, val2=here, abc3=4, xyz=28


Set an end time
---------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

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

**Output:**

.. code-block:: text

    t=100: something() with value: ABC
    t=120: something() with value: DEF


End while running
-----------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

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
    print("Number of events not executed: " + str(simulator.event_heap_size()))
    simulator.reset()

**Output:**

.. code-block:: text

    t=100: something() with value: ABC
    t=120: something() with value: DEF
    t=140: we_are_done() with value: XYZ
    End time: 140
    Number of events not executed: 2


Schedule within a callback
--------------------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

    def something(value):
        print("t=" + str(simulator.now()) + ": something() with value: " + str(value))
        simulator.schedule(200, something, "XYZ")  # 200 time units in the future from now

    simulator.ready()
    simulator.schedule(200, something, "ABC")
    simulator.end(1001)
    simulator.run()
    simulator.reset()

**Output:**

.. code-block:: text

    t=200: something() with value: ABC
    t=400: something() with value: XYZ
    t=600: something() with value: XYZ
    t=800: something() with value: XYZ
    t=1000: something() with value: XYZ


Multiple events in the same time moment with priority
-----------------------------------------------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

    def something(value):
        print("t=" + str(simulator.now()) + ": something() with value: " + str(value))

    simulator.ready()
    simulator.schedule_with_priority(100, 77, something, "XYZ")  # Priority of 77
    simulator.schedule_with_priority(100, 44, something, "ABC")  # Priority of 44
    simulator.run()
    simulator.reset()

**Output:**

.. code-block:: text

    t=100: something() with value: ABC
    t=100: something() with value: XYZ


Instance method as callback (object-oriented)
---------------------------------------------

**Code:**

.. code-block:: python

    from discrevpy import simulator

    class Example:

        def __init__(self, x):
            self.x = x

        def something(self, value):
            print("t=" + str(simulator.now()) + ": instance of class Example (x=" + str(self.x) + ") something() with value: " + str(value))

    abc = Example("Test")

    simulator.ready()
    simulator.schedule(55, abc.something, "ABCDEF")
    simulator.run()
    simulator.reset()

**Output:**

.. code-block:: text

    t=55: instance of class Example (x=Test) something() with value: ABCDEF
