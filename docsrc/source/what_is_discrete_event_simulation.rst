What is discrete event simulation?
==================================

.. toctree::
   :maxdepth: 1
   :hidden:


Goal
----

You want to simulate a real physical system. The first idea would be to calculate what the system does at a fixed time step, however at a small time step this would take too long and potentially many of the steps will have nothing happening. As such, we make use of discrete event simulation. In discrete event simulation, you only do something if there is something meaningful: an event occurs. The simulation hops from event to event, and simulation time progresses as such.


Key terminology
---------------

* **Physical time:** time in the physical system (definition from [1]).

* **Simulation time:** abstraction used by the simulation to model physical time (definition from [1]).

* **Wallclock time:** time during the execution of the simulation program (definition from [1]).

* **Event:** something occurs at a certain point in time. In the simulation, an event is represented by a data structure with at least two fields:

  * *Simulation timestamp (integer):* at what time moment (in simulation time) it needs to be executed.

  * *Function to execute:* the action which is performed, which can modify state and/or insert future events into the event queue.

* **Event queue:** a priority queue of events, ordered by the simulation time.

* **Simulation state:** abstraction used by the simulation to model the physical state (definition based on [1]).

[1] Definitions from the book: Parallel and Distributed Simulation Systems. Richard M. Fujimoto.


Discrete-event simulation in 9 lines
------------------------------------

The mechanism of discrete-event simulation can be condensed to a small piece of pseudo-code:

.. code-block:: text
   :linenos:

    initial state S
    event_queue Q
    insert_first_events(Q)
    current_simulation_time = 0
    while (Q.not_empty()) {
        next_event = Q.pop()
        current_simulation_time = next_event.T
        next_event.execute()
    }

Explanation of each line:

1. The state, which the simulation is centered around.
2. Event queue Q contains events ordered by time, each event has (time T, function to execute (with parameters)).
3. If the event queue is empty, line 5 will just exit immediately. As such, at least one initial event must be scheduled.
4. Initial simulation time is zero (can be any, though zero is generally the only logical one).
5. As long as there events, keep the loop going (of course, it is also possible to make this slightly more sophisticated to have a end time irrespective of whether the are still events scheduled by peeking into the queue.
6. The ``Q.pop()`` will return the event with the lowest time T.
7. The simulation hops from event to event.
8. In its execution, a function can insert future events into Q and modify state S.
9. (Closing bracket)

The discrevpy simulator resembles the above pseudo-code quite closely.


Example use case
----------------

Consider the following example: we have a graph of nodes, and want to answer the question *"How long does it take for a message from node 1 to reach node 2?"*. Moreover, we want to know afterwards how many messages were forwarded by each node.

**Topology sketch**

.. code-block:: text

  Node 1 -- (travel time: 204ms) -- Node 0 -- (travel time: 222867ms) -- Node 2

**Simulation setup and execution walk-through**

1. Initial state are the nodes. Each node *i* has a counter of how many packets it has forwarded, initially set to zero for all. Each node knows how to forward.

2. Before the simulation start you insert into the event queue an event that a message M (destination: 2, content: *"Hello world!"*) arrives at node 1 at t=100ms.

3. The simulation is started.

4. At t=100ms, node 1 receives M. It knows node 0 is the next hop. It increments its forward counter, and inserts another event into the event queue when message M arrives at node 0 with delay 204ms.

5. At t=304ms, node 0 receives M. It knows node 2 is the next hop. It increments its forward counter, and inserts another event into the event queue when message M arrives at node 2 with delay 222867ms.

6. At t=223171ms, node 2 receives M. It sees it is the destination and prints the message.

7. There are no other events, so the simulation is ended.

**Expected final state**

* Node 0: forward counter = 1.
* Node 1: forward counter = 1.
* Node 2: forward_counter = 0; received message at t=223171ms.


Implementation of the use case in discrevpy
-------------------------------------------

**Code:**

.. code-block:: python

     from discrevpy import simulator

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


**Output:**

.. code-block:: text

   t=100: node 1 forward message {'dst_node_id': 2, 'content': 'Hello world!'} to node 0
   t=304: node 0 forward message {'dst_node_id': 2, 'content': 'Hello world!'} to node 2
   t=223171: node 2 received message with content 'Hello world!'
   Node 0 forward counter: 1
   Node 1 forward counter: 1
   Node 2 forward counter: 0


Modeling statements
-------------------


You need initial events
^^^^^^^^^^^^^^^^^^^^^^^

Initially of course you have to insert first event(s) into the event queue Q (else the while loop exits immediately).


New events can only be schedule in the future
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current simulation time increases (weakly) ascending, as it jumps from one event's simulation-timestamp to the next's using the while loop. As such as a hard constraint, it is impossible to insert events with a simulation-timestamp less than the current simulation time.


Time is discrete: the current simulation time jumps to the next event time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the above example, there was only something executed at t=100ms, t=304ms, and t=223171ms. For instance, at t=50ms nothing was executed, because there was no event scheduled at that time.


Events manipulate state
^^^^^^^^^^^^^^^^^^^^^^^

Events are there to manipulate state. The insertion of new events is to space out when these state manipulations happen (in other words: the modeling of physical time in simulation time). "State" effectively means "variables which exist during the simulation". Examples for state are: a counter on a node which for how many packets a node has forwarded, or a queue of packets of which each is waiting for the event which dequeues it.

If you want to model something which would take time in the physical system, you determine how much simulation time you want it to be, and then insert an event in the future


Wallclock time can be much longer than simulation time, or the other way around
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above example simulated 223171ms simulation time. However, in wallclock time executing this will literally have taken less than a 1ms. If the event execution's computations would have been very difficult (let's say matrix factorization of a billion x billion matrix) it could have also been the other way around.


You decide what part of the physical system to model in the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The duration of executing an event in wallclock time can be arbitrarily long, yet no simulation time will pass. For example, instead of having simple pre-calculated constant travel time values, we could also do a very complicated calculation based on many other variables (traffic, type of car, whatever the physical system is).

Moreover, we can even model the time it takes to decide something. For example, we could model that looking up what the next hop is takes 50ms in simulation time. To accomplish this e.g., we can add an extra method ``def forward_lookup_done(self, message, next_hop, travel_duration)`` and  instead schedule that in the ``receive`` and have the extra method schedule the ``receive`` at the next hop.


Wallclock time ≠ physical time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The wallclock time is the time it takes to simulate on the computer you are running the simulation on. Generally, this is NOT the physical system you are modeling, and even if it is, the timings can be significantly off as it is only a model (and also, the computer can have other applications running which influence it).

Using wallclock time to determine simulation time is bad modeling and results in unreproducible experiments and platform dependency
