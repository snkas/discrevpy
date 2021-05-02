Long examples
=============

4x100m relay
------------

**Description:**

We want to simulate a 4x100m relay, and are interested in predicting the finish time.
For each athlete in the relay, we look up their personal best time on the individual 100m
and calculate their speed in meter per second.
In this example, we choose the four athletes at the time of writing (May 1st, 2021) holding the world record on the 4x100m relay [WR]_:

1. Nesta Carter: ``100m / 9.78s =`` 10.2 m/s [WA1]_
2. Michael Frater: ``100m / 9.88s =`` 10.1 m/s [WA2]_
3. Yohan Blake: ``100m / 9.69s =`` 10.3 m/s [WA3]_
4. Usain Bolt: ``100m / 9.58s =`` 10.4 m/s [WA4]_

Of course, this is an example, so yes: we could just add their times together and get an answer.
However, as a model becomes more and more complex to account for new factors, discrete event
simulation is a useful tool to maintain an overview.
For this example, one could extend the model to include varying wind conditions over time, reaction times, technological improvements in shoes, etc.: whatever factors might be influential.

The smallest simulation time unit we set to 1 nanosecond (1 second = 1e9 nanoseconds).
Be aware that floating point operations (such as the time calculation in this example) can be
less accurate than the simulation time precision as it depends on the number of significant
digits (not on the number of decimal digits, in which we define our simulation time unit).
See the `floating point arithmetic documentation <https://docs.python.org/3/tutorial/floatingpoint.html>`_
for more information. Keep in mind that our speed estimates only have three significant digits.

**Code:**

.. code-block:: python

    from discrevpy import simulator

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

**Output:**

.. code-block:: text

    Simulating a 4x100m relay
    Athlete 0 receives stick and starts run at t=0s
    Athlete 1 receives stick and starts run at t=9.8s
    Athlete 2 receives stick and starts run at t=19.7s
    Athlete 3 receives stick and starts run at t=29.4s
    Last athlete finished: 4x100m relay in 39s

**References:**

.. [WR] https://www.worldathletics.org/records/all-time-toplists/relays/4x100-metres-relay/outdoor/men/senior
   (accessed May 1st, 2021)

.. [WA1] https://www.worldathletics.org/athletes/jamaica/nesta-carter-14201894
   (accessed May 1st, 2021)

.. [WA2] https://www.worldathletics.org/athletes/jamaica/michael-frater-14202005
   (accessed May 1st, 2021)

.. [WA3] https://www.worldathletics.org/athletes/jamaica/yohan-blake-14201842
   (accessed May 1st, 2021)

.. [WA4] https://www.worldathletics.org/athletes/jamaica/usain-bolt-14201847
   (accessed May 1st, 2021)
