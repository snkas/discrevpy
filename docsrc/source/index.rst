discrevpy: minimalist discrete event simulator
==============================================

.. image:: https://github.com/snkas/discrevpy/workflows/build/badge.svg
   :alt: build
   :target: https://github.com/snkas/discrevpy/actions?query=workflow%3Abuild+branch%3Amaster

.. image:: https://codecov.io/gh/snkas/discrevpy/branch/master/graph/badge.svg
   :alt: codecov
   :target: https://codecov.io/gh/snkas/discrevpy

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :alt: license: MIT
   :target: https://github.com/snkas/discrevpy/blob/master/LICENSE

.. image:: https://img.shields.io/github/v/release/snkas/discrevpy
   :alt: GitHub release version
   :target: https://github.com/snkas/discrevpy/releases

.. image:: https://img.shields.io/pypi/v/discrevpy?color=blue
   :alt: PyPI version
   :target: https://pypi.org/project/discrevpy/

**discrevpy** is a minimalist discrete event simulator in Python. It makes use of function/method
callbacks in its event execution. The discrevpy simulator does not implement any message passing
and is thus exclusively single-threaded.

.. toctree::
   short_examples
   long_examples
   api_reference
   what_is_discrete_event_simulation
   practical_tips
   memory_usage
   development
   MIT license <https://github.com/snkas/discrevpy/blob/master/LICENSE>
   GitHub repository <https://github.com/snkas/discrevpy>
   :hidden:
   :name: title
   :maxdepth: 2


Installation
------------

**Python version: 3.7+**

.. code-block:: text

   python3 -m pip install discrevpy


Getting started
---------------

**Example usage:**

.. code-block:: python

    from discrevpy import simulator

    def something(value):
      print("t=" + str(simulator.now()) + ": something() with value " + str(value))

    simulator.ready()
    simulator.schedule(44, something, "ABC")
    simulator.schedule(967, something, "XYZ")
    simulator.end(10000)
    simulator.run()
    simulator.reset()

**Next steps:**

* :doc:`View some short examples <short_examples>`
* :doc:`View more in-depth longer examples <long_examples>`
* :doc:`Explore the API <api_reference>`
* :doc:`Learn more about discrete event simulation <what_is_discrete_event_simulation>`
* :doc:`Read some tips to help you speed up your simulations <practical_tips>`
* :doc:`Understand better the memory usage overhead of discrevpy <memory_usage>`

**Development:**

* :doc:`Read the module development instructions <development>`
* `Browse the GitHub repository <https://github.com/snkas/discrevpy>`_
* `View the MIT license <https://github.com/snkas/discrevpy/blob/master/LICENSE>`_
