Practical tips
==============

Event execution is generally the bottleneck: keep it O(1) or O(log n)
-----------------------------------------------------------------------

Generally, insertion of new events into the event queue is not the bottleneck. Rather the time it takes to execute the events is the more likely dominant time factor. In an event execution, you can of course do any computation you want. This almost always consists of events modifying state, which consists of data structures whose functions have time complexity (e.g., memory allocation, queue insertion, passing of events).

An event type with a slow runtime which is often inserted/executed can slow down your simulation significantly. E.g., if you have the arrival of packets into a queue of 100000 elements, make sure the queue insertion is O(1) or O(log n) at worse. Discrete-event simulation is not magic, it is only the simulation of time.

However: also do not fill up the event queue unnecessarily
----------------------------------------------------------

Of course, insert events only if it is absolutely necessary. If you blow up your event queue to 1'000'000+ events, the O(log n) insertion for each new event is still going to slow you down.

**The following guidelines should be followed:**

Do not pre-plan all events of a process which is regenerative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example: let's say every 10ms you want to send a message from A to B. Don't insert for the entire duration of the simulation (e.g., 100s) all events (e.g., 10000) but instead insert one, which then at the end of its execution inserts the next one 10ms from then.

Be wary of inserting a far-in-the-future event for a thing which occurs often
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you insert 100'000 events, each of which is scheduled for 1 ms then they only interfere for that 1 ms. If they are schedule for 1000 s, then they increase event insertion duration for the simulation of those whole thousand seconds.

Group events if the model accuracy loss is acceptable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It might be that many events actually happen at slightly different times, but that with some loss of model accuracy, you can group them. You do this by maintaining a list of the things that happened in that time interval, and then having a regenerative event in a time interval (e.g., 10ms) which goes over the list. It's like the efficiency of garbage collection in Java (process in batches).

If you can, leave it to post-processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can always save things in state and then later on process them. This is especially true for collection of logs or statistics: don't for each thing you log something for insert an event at the end of the simulation which processes the logs, but instead keep it in state and save a list of the things. Then in post-processing after the simulation go over the list.

Be careful of events generating events spiraling out of control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Events creating other events is the key concept of discrete event simulation. However, be aware that this does not spiral out of control, don't insert insert new events continuously at a small future time scale. This can event accidentally: zero is a valid future time, indicating it needs to be execute in the same time step as the event being executed right now. An integer division of int a = 10 / 100 will round to a = 0. Discrete event simulation also happens at fixed time granularity, so even if you set an event to 0.3 nanoseconds in the future, if the granularity is 1 nanosecond, the event will either be 0 or 1 ns in the future.

Pre-process/pre-calculate as much as possible
---------------------------------------------

If you have values which you can calculate beforehand which remain the same for each experimental run, it might be worthwhile to pre-calculate these, and then read in the pre-calculated values from file at the start of each run. Depending on the task, the pre-calculation you might want to do on many machines or in a more convenient programming language (with e.g., better libraries available or hardware acceleration).
