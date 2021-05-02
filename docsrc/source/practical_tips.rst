Practical tips
==============

Speed up event execution: the most likely bottleneck
----------------------------------------------------

Generally, insertion of new events into the event queue is not the bottleneck.
Rather the time it takes to execute the events is the more likely dominant time factor.
In an event execution, any arbitrary computation can be done. However, although
simulation time does not progress within the event's execution, wallclock time does
-- which in the end we use to ascribe a simulation "being slow". As such, any
algorithm or data structure interaction performed in an event execution should
have its time complexity thoughtfully considered.

* **Strive for O(1) or O(log n) time complexity**

  An event type with a slow runtime (especially if frequently inserted/executed) can
  slow down a simulation significantly. For instance, if there is an arrival
  of packets into a queue of 100000 elements, it is prudent that the queue insertion
  is O(1) or O(log n) at worse.  Similarly, allocating or deallocating large amounts
  of memory can be time consuming. Discrete event simulation is not magic, it is
  merely the simulation of time.

* **Pre-process/pre-calculate as much as possible**

  If there are values which can be calculated beforehand which are independent of the
  simulation outcome itself, it is often worthwhile to separately generate these
  and load them in at the start of each run. For example, if the simulation involves
  shortest path routing over a graph, one can calculate the routing state in advance
  (e.g., using Floyd-Warshall). Depending on the task, the pre-calculation might possibly be
  parallelizable over many machines, or could be done with a more convenient framework
  or programming language (with e.g., better libraries available or hardware acceleration).


Regulate event queue size
-------------------------

Insertion into the event queue is O(log n), and as such is likely not the bottleneck.
Of course, if the event queue becomes increasingly large, e.g., reaching 1'000'000 or more events,
it can become a substantial overhead. Irrespective of whether it is event execution or event insertion
which is the dominant time factor, the key mantra is the same: **only insert events if it is necessary.**

* **Do not pre-plan all events of a process which is regenerative**

  For instance, suppose every 1ms a message from A to B is sent. Don't insert for the entire
  duration of the simulation (e.g., 100s) all events (e.g., 100'000) but instead insert one, which
  at the end of its execution inserts the next one 1ms in the future.

* **Be wary of inserting many far-in-the-future events**

  For example, if there are 200'000 events occurring at t=100s, and they are scheduled at the start of the
  simulation, then for the entire simulation time interval of [0, 100s), insertion into the event queue will be slow.
  If it is possible, one could group these 200'000 events together by scheduling a single event at t=99s which only
  at that moment schedules the 200'000 events.

* **Group or aggregate events if the model accuracy loss (if any) is acceptable**

  It might be too time consuming to update the state at the finest time granularity desirable.
  At the cost of model accuracy, one can instead operate at coarser time granularity, possibly
  grouping together or aggregating the changes that occurred. For example, one can have
  a regenerative event in a simulation time interval (e.g., 10ms) that applies the changes in batch.

* **Leave as much as possible to post-processing**

  One can always save data in memory and after the simulation is run process them. This is especially true for the
  collection of logs or statistics. In post-processing, one can go over the stored data in a manner more efficient
  (e.g., parallelized over many machines) or convenient (e.g., using another framework or programming language).

* **Be careful of events generating events spiraling out of control**

  Events creating other events is a key concept of discrete event simulation. However, be aware that
  this does not spiral out of control: it is not recommended to insert new events continuously at a very
  small future time scale. This can even occur accidentally: zero is a valid future time, indicating
  it needs to be execute in the same time step as the event being executed right now. One might use
  an integer division (e.g., ``d = 10 // 100``) (or floor operation) to calculate delay, which will round down to zero
  -- thus if it always schedules itself again in the future this can lead to an infinite loop as
  simulation time never progresses. Discrete event simulation time has a fixed time granularity (known in advance):
  if the granularity is 1 nanosecond then it is impossible to schedule an event 0.3 nanoseconds in the future:
  it must be either 0 or 1 ns.
